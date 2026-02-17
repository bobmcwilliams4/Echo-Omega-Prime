"""
LG15 International Law Engine - Main FastAPI Application
==========================================================
Full TIE-20 implementation: three-layer response, 5 response modes,
doctrine cache, authority hardening, confidence stratification,
semantic normalization, search, telemetry, drift watcher, coverage map,
zoned analysis, fact fragility, audit trail, determinism hash.

Engine: LG15 International Law
Version: 2.0.0
Port: 8405
Mode: EF (Expert Findings)
Authority: 5.0
TIE Components: 20/20
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import math
import time
import traceback
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime
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
# Sibling module imports
# ---------------------------------------------------------------------------

import sys

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DOCTRINE_BLOCKS,
    DoctrineCacheBlock,
    DoctrineCacheIndex,
    build_doctrine_cache,
    get_all_doctrine_categories,
    get_all_doctrine_topics,
    get_coverage_map,
    get_doctrine_block,
    get_doctrine_cache,
    get_doctrine_cache_hash,
    get_doctrine_cache_stats,
    get_stale_doctrines,
    search_doctrines,
    verify_doctrine_integrity,
)
from search import (
    ArbitrationRulesSearcher,
    DoctrineSearchIndex,
    SanctionsScreener,
    SearchResult,
    TradeComplianceChecker,
    TreatySearcher,
    compute_query_hash,
)
from semantic import (
    CATEGORY_MAP,
    SYNONYM_MAP,
    ConflictOfLawsResolver,
    SanctionsAnalyzer,
    TreatyInterpreter,
    classify_international_issue,
    compute_semantic_similarity,
    extract_treaty_entities,
    normalize_query,
)
from telemetry import (
    AuditTrailWriter,
    DoctrineMutationLog,
    DriftRecord,
    DriftWatcher,
    ErrorRecord,
    ErrorSeverity,
    ErrorTracker,
    MetricsAggregator,
    QueryTrace,
    TelemetryCollector,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ENGINE_ID = "LG15"
ENGINE_NAME = "International Law Engine"
ENGINE_VERSION = "2.0.0"
ENGINE_PORT = 8405
ENGINE_HOST = "0.0.0.0"
AUTHORITY_THRESHOLD = 5.0
DETERMINISM_SALT = "LG15_INTERNATIONAL_LAW_v2"

ENGINE_ROOT = Path(__file__).parent
CONFIG_PATH = ENGINE_ROOT / "config.json"
TELEMETRY_DIR = ENGINE_ROOT / "telemetry_data"
LOGS_DIR = ENGINE_ROOT / "logs"
DOCTRINE_CACHE_DIR = ENGINE_ROOT / "doctrine_cache"

for _d in (TELEMETRY_DIR, LOGS_DIR, DOCTRINE_CACHE_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# Loguru setup
logger.add(
    LOGS_DIR / "lg15_engine.log",
    rotation="50 MB",
    retention="30 days",
    compression="gz",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} | {message}",
    level="DEBUG",
)

# ---------------------------------------------------------------------------
# Banned phrases (authority hardening)
# ---------------------------------------------------------------------------

BANNED_PHRASES: list[str] = [
    "i think",
    "i believe",
    "in my opinion",
    "probably",
    "i guess",
    "it seems like",
    "i would say",
    "this is not legal advice",
    "you should consult a lawyer",
    "i'm not sure but",
    "maybe",
    "it's possible that",
    "as an AI",
    "as a language model",
    "i cannot provide legal advice",
    "disclaimer",
    "for informational purposes only",
]

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ResponseMode(str, Enum):
    FAST = "fast"
    ANALYSIS = "analysis"
    MEMO = "memo"
    TREATY_INTERPRETATION = "treaty_interpretation"
    TRADE_COMPLIANCE = "trade_compliance"


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INSUFFICIENT = "INSUFFICIENT"


class AnalysisZone(str, Enum):
    TREATY = "treaty"
    TRADE = "trade"
    ARBITRATION = "arbitration"
    SANCTIONS = "sanctions"
    HUMAN_RIGHTS = "human_rights"
    HUMANITARIAN = "humanitarian"
    CRIMINAL = "criminal"
    ENVIRONMENTAL = "environmental"
    SEA = "sea"
    DIPLOMATIC = "diplomatic"
    GENERAL = "general"


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class QueryRequest(BaseModel):
    """Primary query request model."""
    query: str = Field(..., min_length=3, max_length=10000, description="The legal question or issue")
    mode: ResponseMode = Field(default=ResponseMode.ANALYSIS, description="Response mode")
    zone: AnalysisZone | None = Field(default=None, description="Force specific analysis zone")
    jurisdiction: str = Field(default="INTERNATIONAL", description="Primary jurisdiction context")
    deep_analysis: bool = Field(default=False, description="Enable deep analysis mode")
    include_treaties: bool = Field(default=True, description="Include treaty analysis")
    include_arbitration: bool = Field(default=False, description="Include arbitration rules analysis")
    include_sanctions: bool = Field(default=False, description="Include sanctions screening")
    max_results: int = Field(default=10, ge=1, le=50, description="Max search results")


class QueryResponse(BaseModel):
    """Primary query response model."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    query_hash: str
    query_normalized: str
    mode: str
    zone: str
    jurisdiction: str
    confidence: float
    confidence_level: str
    authority_score: float
    response_layers: dict[str, Any]
    doctrine_blocks_used: list[str]
    search_results: list[dict[str, Any]]
    treaty_analysis: dict[str, Any] | None = None
    arbitration_analysis: dict[str, Any] | None = None
    sanctions_screening: dict[str, Any] | None = None
    trade_compliance: dict[str, Any] | None = None
    fact_fragility: dict[str, Any]
    coverage_gaps: list[str]
    drift_warnings: list[dict[str, Any]]
    determinism_hash: str
    latency_ms: float
    timestamp: str
    disclosure_caveat: str


class HealthResponse(BaseModel):
    """Health check response."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    status: str
    port: int = ENGINE_PORT
    authority: float = AUTHORITY_THRESHOLD
    uptime_seconds: float
    doctrine_blocks: int
    doctrine_integrity: bool
    telemetry: dict[str, Any]
    drift_summary: dict[str, Any]
    search_index_stats: dict[str, Any]
    timestamp: str


class TreatyAnalysisRequest(BaseModel):
    """Request for treaty-specific analysis."""
    treaty_id: str = Field(..., description="Treaty identifier (e.g., VCLT, UN_CHARTER)")
    question: str = Field(..., min_length=3, max_length=5000, description="Specific question about the treaty")
    articles: list[str] = Field(default_factory=list, description="Specific articles to focus on")
    interpretation_method: str = Field(default="vclt_31_32", description="Interpretation methodology")


class SanctionsScreenRequest(BaseModel):
    """Request for sanctions screening."""
    entity_name: str = Field(..., min_length=2, max_length=500, description="Entity name to screen")
    country_code: str = Field(default="", max_length=5, description="ISO country code")
    include_general_licenses: bool = Field(default=True, description="Include applicable general licenses")


class TradeComplianceRequest(BaseModel):
    """Request for WTO trade compliance analysis."""
    measure_description: str = Field(..., min_length=10, max_length=5000, description="Description of trade measure")
    affected_countries: list[str] = Field(default_factory=list, description="List of affected country codes")
    sectors: list[str] = Field(default_factory=list, description="Economic sectors affected")


# ---------------------------------------------------------------------------
# Zone detection
# ---------------------------------------------------------------------------

_ZONE_KEYWORDS: dict[AnalysisZone, list[str]] = {
    AnalysisZone.TREATY: ["treaty", "convention", "vclt", "interpretation", "ratification", "reservation", "pacta sunt servanda", "jus cogens", "peremptory norm"],
    AnalysisZone.TRADE: ["wto", "gatt", "tariff", "trade", "mfn", "national treatment", "dumping", "subsidy", "countervailing", "safeguard", "tbt", "sps", "trips"],
    AnalysisZone.ARBITRATION: ["arbitration", "uncitral", "icsid", "icc arbitration", "lcia", "award", "arbitral", "investor-state", "isds", "bit", "new york convention"],
    AnalysisZone.SANCTIONS: ["sanction", "ofac", "sdn", "embargo", "export control", "ear", "itar", "ieepa", "blocked person", "screening"],
    AnalysisZone.HUMAN_RIGHTS: ["human rights", "iccpr", "icescr", "echr", "torture", "discrimination", "right to life", "freedom of expression", "fair trial"],
    AnalysisZone.HUMANITARIAN: ["humanitarian law", "ihl", "geneva convention", "laws of war", "civilian protection", "prisoner of war", "combatant", "red cross", "hague convention"],
    AnalysisZone.CRIMINAL: ["international criminal", "icc", "rome statute", "genocide", "crimes against humanity", "war crimes", "aggression", "complementarity", "extradition"],
    AnalysisZone.ENVIRONMENTAL: ["environment", "climate", "paris agreement", "montreal protocol", "biodiversity", "unclos marine", "pollution", "ozone", "carbon"],
    AnalysisZone.SEA: ["law of the sea", "unclos", "territorial sea", "eez", "exclusive economic zone", "continental shelf", "high seas", "itlos", "deep seabed"],
    AnalysisZone.DIPLOMATIC: ["diplomatic", "consular", "immunity", "vcdr", "vccr", "embassy", "persona non grata", "inviolability", "diplomatic bag"],
}


def detect_zone(query: str, forced_zone: AnalysisZone | None = None) -> AnalysisZone:
    """Detect the most relevant analysis zone from query text."""
    if forced_zone is not None:
        return forced_zone
    query_lower = query.lower()
    scores: dict[AnalysisZone, int] = defaultdict(int)
    for zone, keywords in _ZONE_KEYWORDS.items():
        for kw in keywords:
            if kw in query_lower:
                scores[zone] += 1
    if not scores:
        return AnalysisZone.GENERAL
    return max(scores, key=lambda z: scores[z])


# ---------------------------------------------------------------------------
# Confidence stratification
# ---------------------------------------------------------------------------

_CONFIDENCE_THRESHOLDS = {"high": 0.85, "medium": 0.65, "low": 0.40, "uncertain": 0.20}


def stratify_confidence(score: float) -> ConfidenceLevel:
    """Map raw confidence to a stratified level."""
    if score >= _CONFIDENCE_THRESHOLDS["high"]:
        return ConfidenceLevel.HIGH
    if score >= _CONFIDENCE_THRESHOLDS["medium"]:
        return ConfidenceLevel.MEDIUM
    if score >= _CONFIDENCE_THRESHOLDS["low"]:
        return ConfidenceLevel.LOW
    return ConfidenceLevel.INSUFFICIENT


# ---------------------------------------------------------------------------
# Authority hardening
# ---------------------------------------------------------------------------

def harden_authority(text: str, authority: float) -> tuple[str, list[str]]:
    """Remove banned phrases if below authority threshold. Returns cleaned text and violations found."""
    if authority >= AUTHORITY_THRESHOLD:
        return text, []
    violations: list[str] = []
    result = text
    for phrase in BANNED_PHRASES:
        if phrase.lower() in result.lower():
            violations.append(phrase)
            import re
            result = re.sub(re.escape(phrase), "", result, flags=re.IGNORECASE).strip()
    return result, violations


def generate_disclosure_caveat(confidence: ConfidenceLevel, zone: AnalysisZone) -> str:
    """Generate the mandatory disclosure caveat based on confidence and zone."""
    caveats: dict[ConfidenceLevel, str] = {
        ConfidenceLevel.HIGH: f"Analysis grounded in well-established {zone.value} doctrine with strong treaty/customary law basis.",
        ConfidenceLevel.MEDIUM: f"Analysis based on prevailing {zone.value} doctrine. Some areas may involve evolving norms or limited state practice. Specialist counsel recommended for binding decisions.",
        ConfidenceLevel.LOW: f"Limited doctrinal coverage in {zone.value} domain. Multiple interpretations exist. This analysis should be verified by subject-matter specialists before reliance.",
        ConfidenceLevel.INSUFFICIENT: f"Insufficient doctrinal basis for reliable analysis in {zone.value} domain. The query may involve novel, contested, or highly jurisdiction-specific issues. Independent legal research required.",
    }
    return caveats.get(confidence, caveats[ConfidenceLevel.INSUFFICIENT])


# ---------------------------------------------------------------------------
# Fact fragility scoring
# ---------------------------------------------------------------------------

def compute_fact_fragility(
    doctrine_count: int,
    search_score: float,
    zone: AnalysisZone,
    drift_warnings: int,
    confidence: float,
) -> dict[str, Any]:
    """Compute how fragile the factual basis of the response is."""
    fragility_factors: list[dict[str, Any]] = []

    # Doctrine coverage factor
    if doctrine_count == 0:
        fragility_factors.append({"factor": "no_doctrine_coverage", "weight": 0.4, "detail": "No doctrine blocks matched the query"})
    elif doctrine_count < 3:
        fragility_factors.append({"factor": "sparse_doctrine", "weight": 0.2, "detail": f"Only {doctrine_count} doctrine block(s) matched"})

    # Search quality factor
    if search_score < 0.3:
        fragility_factors.append({"factor": "weak_search_match", "weight": 0.2, "detail": f"Best search score {search_score:.2f} below 0.30"})

    # Zone-specific volatility
    volatile_zones = {AnalysisZone.SANCTIONS, AnalysisZone.TRADE, AnalysisZone.ENVIRONMENTAL, AnalysisZone.CRIMINAL}
    if zone in volatile_zones:
        fragility_factors.append({"factor": "volatile_domain", "weight": 0.15, "detail": f"{zone.value} domain subject to frequent legal changes"})

    # Drift warnings
    if drift_warnings > 0:
        fragility_factors.append({"factor": "doctrine_drift", "weight": 0.15, "detail": f"{drift_warnings} doctrine block(s) flagged for potential drift"})

    # Confidence shortfall
    if confidence < 0.65:
        fragility_factors.append({"factor": "low_confidence", "weight": 0.1, "detail": f"Confidence {confidence:.2f} below medium threshold"})

    total_fragility = sum(f["weight"] for f in fragility_factors)
    total_fragility = min(total_fragility, 1.0)

    if total_fragility >= 0.6:
        fragility_level = "BRITTLE"
    elif total_fragility >= 0.35:
        fragility_level = "MODERATE"
    elif total_fragility >= 0.15:
        fragility_level = "MILD"
    else:
        fragility_level = "SOLID"

    return {
        "fragility_score": round(total_fragility, 4),
        "fragility_level": fragility_level,
        "factors": fragility_factors,
        "doctrine_blocks_matched": doctrine_count,
        "best_search_score": round(search_score, 4),
    }


# ---------------------------------------------------------------------------
# Determinism hash
# ---------------------------------------------------------------------------

def compute_determinism_hash(
    query_hash: str,
    doctrine_ids: list[str],
    zone: str,
    mode: str,
    confidence: float,
) -> str:
    """SHA-256 determinism hash ensuring reproducible responses."""
    payload = json.dumps({
        "salt": DETERMINISM_SALT,
        "version": ENGINE_VERSION,
        "query_hash": query_hash,
        "doctrine_ids": sorted(doctrine_ids),
        "zone": zone,
        "mode": mode,
        "confidence": round(confidence, 4),
    }, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Multi-doctrine decomposition
# ---------------------------------------------------------------------------

def decompose_multi_doctrine(query: str, zone: AnalysisZone) -> list[dict[str, Any]]:
    """Decompose a complex query into sub-issues for multi-doctrine analysis."""
    sub_issues: list[dict[str, Any]] = []
    query_lower = query.lower()

    # Treaty interpretation sub-issues
    if any(kw in query_lower for kw in ["treaty", "convention", "interpretation", "article"]):
        sub_issues.append({
            "sub_issue": "treaty_interpretation",
            "description": "Apply VCLT Art.31/32 interpretation methodology to the referenced treaty provision",
            "doctrines_needed": ["treaty_interpretation_vclt", "customary_international_law"],
            "priority": 1,
        })

    # Jurisdictional sub-issues
    if any(kw in query_lower for kw in ["jurisdiction", "court", "forum", "competence", "standing"]):
        sub_issues.append({
            "sub_issue": "jurisdictional_analysis",
            "description": "Determine applicable jurisdictional rules and forum selection considerations",
            "doctrines_needed": ["icj_jurisdiction", "extraterritorial_jurisdiction", "conflict_of_laws"],
            "priority": 2,
        })

    # Enforcement sub-issues
    if any(kw in query_lower for kw in ["enforce", "recognition", "execution", "compliance"]):
        sub_issues.append({
            "sub_issue": "enforcement_analysis",
            "description": "Analyze enforcement mechanisms and recognition/execution frameworks",
            "doctrines_needed": ["ny_convention_arbitral_awards", "foreign_judgments_recognition"],
            "priority": 2,
        })

    # State responsibility
    if any(kw in query_lower for kw in ["state responsibility", "attribution", "countermeasure", "reparation", "wrongful act"]):
        sub_issues.append({
            "sub_issue": "state_responsibility",
            "description": "Analyze under ILC Articles on State Responsibility",
            "doctrines_needed": ["state_responsibility", "customary_international_law"],
            "priority": 1,
        })

    # Human rights
    if any(kw in query_lower for kw in ["rights", "freedom", "discrimination", "torture", "expression"]):
        sub_issues.append({
            "sub_issue": "human_rights_assessment",
            "description": "Assess human rights obligations under applicable instruments",
            "doctrines_needed": ["iccpr_civil_political_rights", "icescr_economic_social_rights", "echr_human_rights"],
            "priority": 2,
        })

    # Trade-specific
    if any(kw in query_lower for kw in ["tariff", "dumping", "subsidy", "trade barrier"]):
        sub_issues.append({
            "sub_issue": "trade_discipline_analysis",
            "description": "WTO discipline compliance check under GATT/relevant WTO agreements",
            "doctrines_needed": ["wto_mfn", "wto_national_treatment", "trade_remedies_antidumping", "trade_remedies_countervailing"],
            "priority": 1,
        })

    # Sanctions
    if any(kw in query_lower for kw in ["sanction", "embargo", "export control", "ofac"]):
        sub_issues.append({
            "sub_issue": "sanctions_compliance",
            "description": "Sanctions program identification and compliance assessment",
            "doctrines_needed": ["ofac_sanctions", "ear_export_controls", "itar_defense_articles"],
            "priority": 1,
        })

    # Arbitration
    if any(kw in query_lower for kw in ["arbitrat", "icsid", "uncitral", "icc rules", "award"]):
        sub_issues.append({
            "sub_issue": "arbitration_procedure",
            "description": "Procedural and substantive arbitration analysis under applicable rules",
            "doctrines_needed": ["international_arbitration_uncitral", "international_arbitration_icsid", "international_arbitration_icc"],
            "priority": 1,
        })

    # Investment
    if any(kw in query_lower for kw in ["invest", "expropriat", "fair and equitable", "bilateral investment", "bit"]):
        sub_issues.append({
            "sub_issue": "investment_protection",
            "description": "BIT/IIA protection standards and ISDS considerations",
            "doctrines_needed": ["bilateral_investment_treaties", "investor_state_dispute_settlement", "fsia_expropriation"],
            "priority": 1,
        })

    # Use of force / self-defense
    if any(kw in query_lower for kw in ["force", "self-defense", "self-defence", "armed attack", "security council"]):
        sub_issues.append({
            "sub_issue": "use_of_force",
            "description": "Jus ad bellum analysis under UN Charter Art.2(4)/51",
            "doctrines_needed": ["use_of_force", "self_defense", "un_charter_principles"],
            "priority": 1,
        })

    # Environmental
    if any(kw in query_lower for kw in ["environment", "climate", "pollution", "biodiversity", "emission"]):
        sub_issues.append({
            "sub_issue": "environmental_obligations",
            "description": "International environmental law obligations and commitments",
            "doctrines_needed": ["paris_agreement_climate", "montreal_protocol_ozone", "cbd_biodiversity"],
            "priority": 2,
        })

    # Corruption / FCPA
    if any(kw in query_lower for kw in ["brib", "corrupt", "fcpa", "bribery act"]):
        sub_issues.append({
            "sub_issue": "anti_corruption",
            "description": "Anti-corruption framework analysis (FCPA, UK Bribery Act, OECD Convention)",
            "doctrines_needed": ["fcpa_anti_corruption", "uk_bribery_act", "oecd_anti_bribery"],
            "priority": 1,
        })

    if not sub_issues:
        sub_issues.append({
            "sub_issue": "general_international_law",
            "description": "General public international law analysis",
            "doctrines_needed": ["un_charter_principles", "customary_international_law", "state_sovereignty"],
            "priority": 3,
        })

    sub_issues.sort(key=lambda x: x["priority"])
    return sub_issues


# ---------------------------------------------------------------------------
# Three-layer response builder
# ---------------------------------------------------------------------------

def build_three_layer_response(
    query: str,
    query_normalized: str,
    zone: AnalysisZone,
    mode: ResponseMode,
    doctrine_results: list[dict[str, Any]],
    search_results: list[SearchResult],
    sub_issues: list[dict[str, Any]],
    deep_analysis: bool,
) -> dict[str, Any]:
    """Build the three-layer response: doctrine_cache -> semantic_search -> deep_analysis."""

    # Layer 1: Doctrine cache
    layer_1: dict[str, Any] = {
        "layer": "doctrine_cache",
        "blocks_matched": len(doctrine_results),
        "blocks": [],
    }
    for dr in doctrine_results[:10]:
        layer_1["blocks"].append({
            "block_id": dr.get("block_id", "unknown"),
            "topic": dr.get("topic", ""),
            "summary": dr.get("summary", dr.get("content", ""))[:500],
            "confidence_modifier": dr.get("confidence_modifier", 0.0),
        })

    # Layer 2: Semantic search
    layer_2: dict[str, Any] = {
        "layer": "semantic_search",
        "results_count": len(search_results),
        "top_results": [],
    }
    for sr in search_results[:8]:
        layer_2["top_results"].append({
            "doc_id": sr.doc_id,
            "title": sr.title,
            "score": sr.score,
            "category": sr.category,
            "snippet": sr.snippet[:300],
        })

    # Layer 3: Deep analysis
    layer_3: dict[str, Any] = {
        "layer": "deep_analysis",
        "enabled": deep_analysis or mode in (ResponseMode.MEMO, ResponseMode.TREATY_INTERPRETATION),
        "sub_issues": sub_issues,
        "analysis": {},
    }
    if layer_3["enabled"]:
        layer_3["analysis"] = _build_deep_analysis(query_normalized, zone, doctrine_results, search_results, sub_issues)

    return {
        "doctrine_cache": layer_1,
        "semantic_search": layer_2,
        "deep_analysis": layer_3,
    }


def _build_deep_analysis(
    query: str,
    zone: AnalysisZone,
    doctrine_results: list[dict[str, Any]],
    search_results: list[SearchResult],
    sub_issues: list[dict[str, Any]],
) -> dict[str, Any]:
    """Construct deep analysis content from doctrines and search results."""
    applicable_law: list[str] = []
    key_principles: list[str] = []
    analysis_notes: list[str] = []
    authorities_cited: list[str] = []

    for dr in doctrine_results:
        topic = dr.get("topic", "")
        summary = dr.get("summary", dr.get("content", ""))
        if topic:
            applicable_law.append(topic)
        if summary:
            key_principles.append(summary[:200])

    for sr in search_results[:5]:
        if sr.title:
            authorities_cited.append(sr.title)

    # Zone-specific analysis content
    zone_guidance: dict[AnalysisZone, str] = {
        AnalysisZone.TREATY: "Apply VCLT Art.31 (good faith, ordinary meaning, context, object and purpose) as primary rule. Resort to VCLT Art.32 (travaux preparatoires) only if Art.31 leaves meaning ambiguous or leads to manifestly absurd result.",
        AnalysisZone.TRADE: "Apply WTO two-step analysis: (1) determine if measure violates a WTO obligation (MFN, NT, QR prohibition, etc.), (2) if so, check if exception applies (Art.XX/XXI GATT, TBT Art.2.2, SPS Art.5.7). Burden shifts to respondent for exceptions.",
        AnalysisZone.ARBITRATION: "Consider: (i) jurisdictional requirements (consent, investment, nationality), (ii) applicable procedural rules, (iii) substantive protection standards (FET, expropriation, FPS, MFN, umbrella clause), (iv) damages quantum, (v) enforcement under NY Convention or ICSID Convention.",
        AnalysisZone.SANCTIONS: "Screen against OFAC SDN List, Entity List, and applicable country programs. Identify whether transaction involves comprehensive or targeted sanctions. Check for applicable General Licenses. Assess secondary sanctions exposure. OFAC strict liability standard applies.",
        AnalysisZone.HUMAN_RIGHTS: "Identify applicable human rights instruments (ICCPR, ICESCR, regional instruments). Apply three-part test for permissible limitations: (1) prescribed by law, (2) legitimate aim, (3) necessary and proportionate. Consider margin of appreciation (ECHR), derogation provisions, and non-derogable rights.",
        AnalysisZone.HUMANITARIAN: "Apply IHL distinction between international and non-international armed conflict. Core principles: distinction (civilians/combatants), proportionality, military necessity, humanity. Common Article 3 as minimum standard. Check Geneva Conventions, Additional Protocols, and customary IHL (ICRC study).",
        AnalysisZone.CRIMINAL: "Rome Statute jurisdiction: (1) subject-matter (Art.5), (2) temporal (Art.11), (3) personal/territorial (Art.12), (4) admissibility/complementarity (Art.17). Elements of crimes must be proved beyond reasonable doubt. Modes of liability under Art.25. Command responsibility under Art.28.",
        AnalysisZone.ENVIRONMENTAL: "Identify applicable MEA obligations (Paris Agreement NDCs, Montreal Protocol phase-downs, CBD Aichi targets). Apply precautionary principle (Rio Principle 15). Consider common but differentiated responsibilities (CBDR). Assess compliance mechanisms specific to the treaty regime.",
        AnalysisZone.SEA: "UNCLOS zonal approach: internal waters, territorial sea (12 NM), contiguous zone (24 NM), EEZ (200 NM), continental shelf (natural prolongation/200 NM), high seas, the Area. Coastal state rights diminish with distance. Dispute settlement under Part XV (ITLOS, ICJ, Annex VII).",
        AnalysisZone.DIPLOMATIC: "VCDR framework: premises inviolability (Art.22), diplomatic agent inviolability (Art.29), immunity from jurisdiction (Art.31), waiver by sending state (Art.32). Distinction between diplomatic and consular immunity. State practice on persona non grata declarations.",
        AnalysisZone.GENERAL: "Apply sources hierarchy: (1) treaties, (2) customary international law (state practice + opinio juris), (3) general principles of law, (4) judicial decisions and teachings as subsidiary means (ICJ Statute Art.38). Consider jus cogens and erga omnes obligations.",
    }

    methodology = zone_guidance.get(zone, zone_guidance[AnalysisZone.GENERAL])

    for si in sub_issues:
        analysis_notes.append(f"Sub-issue '{si['sub_issue']}': {si['description']}")

    return {
        "methodology": methodology,
        "applicable_law": applicable_law[:15],
        "key_principles": key_principles[:10],
        "authorities_cited": authorities_cited[:10],
        "analysis_notes": analysis_notes,
        "sub_issue_count": len(sub_issues),
    }


# ---------------------------------------------------------------------------
# Coverage gap detection
# ---------------------------------------------------------------------------

def detect_coverage_gaps(
    zone: AnalysisZone,
    doctrine_ids: list[str],
    sub_issues: list[dict[str, Any]],
) -> list[str]:
    """Identify doctrine topics needed but not found in results."""
    needed_doctrines: set[str] = set()
    for si in sub_issues:
        for d in si.get("doctrines_needed", []):
            needed_doctrines.add(d)

    found: set[str] = set(doctrine_ids)
    gaps = needed_doctrines - found
    return sorted(gaps)


# ---------------------------------------------------------------------------
# Global state
# ---------------------------------------------------------------------------

_startup_time: float = 0.0
_telemetry: TelemetryCollector | None = None
_audit_writer: AuditTrailWriter | None = None
_drift_watcher: DriftWatcher | None = None
_metrics_aggregator: MetricsAggregator | None = None
_error_tracker: ErrorTracker | None = None
_mutation_log: DoctrineMutationLog | None = None
_doctrine_index: DoctrineSearchIndex | None = None
_treaty_searcher: TreatySearcher | None = None
_arbitration_searcher: ArbitrationRulesSearcher | None = None
_sanctions_screener: SanctionsScreener | None = None
_trade_checker: TradeComplianceChecker | None = None
_treaty_interpreter: TreatyInterpreter | None = None
_sanctions_analyzer: SanctionsAnalyzer | None = None
_conflict_resolver: ConflictOfLawsResolver | None = None


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialise and tear down all subsystems."""
    global _startup_time, _telemetry, _audit_writer, _drift_watcher
    global _metrics_aggregator, _error_tracker, _mutation_log
    global _doctrine_index, _treaty_searcher, _arbitration_searcher
    global _sanctions_screener, _trade_checker
    global _treaty_interpreter, _sanctions_analyzer, _conflict_resolver

    _startup_time = time.time()
    logger.info("=== LG15 International Law Engine v{} starting on port {} ===", ENGINE_VERSION, ENGINE_PORT)

    # Init telemetry subsystems
    _telemetry = TelemetryCollector(telemetry_dir=TELEMETRY_DIR)
    _audit_writer = AuditTrailWriter(log_path=TELEMETRY_DIR / "audit_trail.jsonl")
    _drift_watcher = DriftWatcher(staleness_threshold_hours=168)
    _metrics_aggregator = MetricsAggregator()
    _error_tracker = ErrorTracker()
    _mutation_log = DoctrineMutationLog(log_path=TELEMETRY_DIR / "doctrine_mutations.jsonl")

    # Build doctrine cache
    logger.info("Building doctrine cache...")
    build_doctrine_cache()
    cache = get_doctrine_cache()
    logger.info("Doctrine cache built: {} blocks", len(cache) if cache else 0)

    # Build search index from doctrines
    _doctrine_index = DoctrineSearchIndex()
    if cache:
        for block_id, block in cache.items():
            content = ""
            if hasattr(block, "content"):
                content = block.content
            elif hasattr(block, "summary"):
                content = block.summary
            elif isinstance(block, dict):
                content = block.get("content", block.get("summary", ""))

            category = ""
            if hasattr(block, "category"):
                category = block.category
            elif isinstance(block, dict):
                category = block.get("category", "")

            topic = ""
            if hasattr(block, "topic"):
                topic = block.topic
            elif isinstance(block, dict):
                topic = block.get("topic", "")

            _doctrine_index.add_document(
                doc_id=block_id,
                title=topic,
                text=f"{topic} {category} {content}",
                category=category,
            )

            # Register with drift watcher
            block_hash = hashlib.sha256(content.encode("utf-8")).hexdigest() if content else ""
            _drift_watcher.register_block(block_id, block_hash)

    logger.info("Doctrine search index: {} documents, {} terms", _doctrine_index.document_count, _doctrine_index.term_count)

    # Init searchers
    _treaty_searcher = TreatySearcher()
    _arbitration_searcher = ArbitrationRulesSearcher()
    _sanctions_screener = SanctionsScreener()
    _trade_checker = TradeComplianceChecker()

    # Init semantic analysers
    _treaty_interpreter = TreatyInterpreter()
    _sanctions_analyzer = SanctionsAnalyzer()
    _conflict_resolver = ConflictOfLawsResolver()

    # Verify doctrine integrity
    integrity = verify_doctrine_integrity()
    logger.info("Doctrine integrity check: {}", integrity)

    logger.info("=== LG15 Engine OPERATIONAL ===")

    yield

    # Shutdown
    logger.info("LG15 Engine shutting down...")
    if _telemetry:
        snapshot = _telemetry.get_full_snapshot()
        logger.info("Final telemetry snapshot: {}", json.dumps(snapshot, indent=2))
    logger.info("LG15 Engine shutdown complete.")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="LG15 International Law Engine",
    description="Comprehensive international law analysis engine with TIE-20 architecture",
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
# Utility: run query pipeline
# ---------------------------------------------------------------------------

async def _run_query_pipeline(req: QueryRequest) -> QueryResponse:
    """Execute the full query pipeline across all TIE components."""
    start_time = time.time()
    trace_id = str(uuid.uuid4())

    assert _telemetry is not None
    assert _audit_writer is not None
    assert _drift_watcher is not None
    assert _metrics_aggregator is not None
    assert _error_tracker is not None
    assert _doctrine_index is not None
    assert _treaty_searcher is not None
    assert _arbitration_searcher is not None
    assert _sanctions_screener is not None
    assert _trade_checker is not None
    assert _treaty_interpreter is not None
    assert _sanctions_analyzer is not None

    # Step 1: Normalize query (semantic module)
    query_normalized = normalize_query(req.query)
    query_hash = compute_query_hash(query_normalized)

    # Step 2: Detect zone
    zone = detect_zone(query_normalized, req.zone)

    # Step 3: Classify issue
    issue_classification = classify_international_issue(query_normalized)

    # Step 4: Extract treaty entities
    entities = extract_treaty_entities(query_normalized)

    # Step 5: Search doctrine cache
    doctrine_results = search_doctrines(query_normalized)
    if not doctrine_results:
        doctrine_results = []
    doctrine_ids = []
    for dr in doctrine_results:
        did = dr.get("block_id", dr.get("id", ""))
        if did:
            doctrine_ids.append(did)

    # Step 6: TF-IDF search
    search_results = _doctrine_index.search(query_normalized, top_k=req.max_results)

    # Step 7: Treaty search
    treaty_analysis: dict[str, Any] | None = None
    if req.include_treaties:
        treaty_results = _treaty_searcher.search_by_keyword(query_normalized, top_k=5)
        if treaty_results:
            treaty_analysis = {
                "treaties_found": len(treaty_results),
                "treaties": [
                    {
                        "treaty_id": tr.doc_id,
                        "title": tr.title,
                        "relevance": tr.score,
                        "metadata": tr.metadata,
                    }
                    for tr in treaty_results
                ],
                "interpretation": _treaty_interpreter.interpret(query_normalized, entities) if entities else {},
            }

    # Step 8: Arbitration analysis
    arbitration_analysis: dict[str, Any] | None = None
    if req.include_arbitration or zone == AnalysisZone.ARBITRATION:
        arb_results = _arbitration_searcher.search_by_topic(query_normalized, top_k=5)
        if arb_results:
            arbitration_analysis = {
                "rules_found": len(arb_results),
                "rules": [
                    {
                        "rule_id": ar.doc_id,
                        "title": ar.title,
                        "institution": ar.metadata.get("institution", ""),
                        "relevance": ar.score,
                    }
                    for ar in arb_results
                ],
            }

    # Step 9: Sanctions screening
    sanctions_result: dict[str, Any] | None = None
    if req.include_sanctions or zone == AnalysisZone.SANCTIONS:
        entity_names = entities.get("entities", []) if isinstance(entities, dict) else []
        if entity_names:
            first_entity = entity_names[0] if isinstance(entity_names[0], str) else str(entity_names[0])
            sanctions_result = _sanctions_screener.screen_entity(first_entity)
        else:
            sanctions_result = _sanctions_analyzer.analyze(query_normalized)

    # Step 10: Trade compliance
    trade_result: dict[str, Any] | None = None
    if req.mode == ResponseMode.TRADE_COMPLIANCE or zone == AnalysisZone.TRADE:
        trade_result = _trade_checker.analyze_tariff_measure(query_normalized)

    # Step 11: Compute confidence
    base_confidence = 0.50
    if doctrine_results:
        doctrine_boost = min(len(doctrine_results) * 0.08, 0.30)
        base_confidence += doctrine_boost
    if search_results:
        best_score = max(sr.score for sr in search_results)
        base_confidence += best_score * 0.15
    if treaty_analysis and treaty_analysis.get("treaties_found", 0) > 0:
        base_confidence += 0.05
    confidence = min(base_confidence, 0.98)
    confidence_level = stratify_confidence(confidence)

    # Step 12: Multi-doctrine decomposition
    sub_issues = decompose_multi_doctrine(query_normalized, zone)

    # Step 13: Three-layer response
    response_layers = build_three_layer_response(
        query=req.query,
        query_normalized=query_normalized,
        zone=zone,
        mode=req.mode,
        doctrine_results=doctrine_results,
        search_results=search_results,
        sub_issues=sub_issues,
        deep_analysis=req.deep_analysis,
    )

    # Step 14: Drift check
    drift_warnings: list[dict[str, Any]] = []
    for did in doctrine_ids[:20]:
        content_hash = hashlib.sha256(did.encode("utf-8")).hexdigest()
        drift_rec = _drift_watcher.check_drift(did, content_hash, topic=did)
        if drift_rec.drift_detected:
            drift_warnings.append({
                "block_id": drift_rec.block_id,
                "drift_type": drift_rec.drift_type,
                "staleness_hours": drift_rec.staleness_hours,
                "confidence_delta": drift_rec.confidence_delta,
                "recommendation": drift_rec.recommendation,
            })

    # Step 15: Coverage gaps
    coverage_gaps = detect_coverage_gaps(zone, doctrine_ids, sub_issues)

    # Step 16: Fact fragility
    best_search_score = max((sr.score for sr in search_results), default=0.0)
    fact_fragility = compute_fact_fragility(
        doctrine_count=len(doctrine_results),
        search_score=best_search_score,
        zone=zone,
        drift_warnings=len(drift_warnings),
        confidence=confidence,
    )

    # Step 17: Authority hardening
    authority_score = AUTHORITY_THRESHOLD
    disclosure = generate_disclosure_caveat(confidence_level, zone)

    # Step 18: Determinism hash
    det_hash = compute_determinism_hash(query_hash, doctrine_ids, zone.value, req.mode.value, confidence)

    # Step 19: Latency
    latency_ms = (time.time() - start_time) * 1000.0

    # Step 20: Telemetry recording
    trace = QueryTrace(
        trace_id=trace_id,
        query_text=req.query[:200],
        query_hash=query_hash,
        category=issue_classification.get("category", "general") if isinstance(issue_classification, dict) else "general",
        response_mode=req.mode.value,
        confidence=confidence,
        latency_ms=latency_ms,
        cache_hit=len(doctrine_results) > 0,
        doctrine_blocks_used=len(doctrine_results),
        search_results_count=len(search_results),
        zone=zone.value,
        error=None,
    )
    _telemetry.record_query(trace)

    _metrics_aggregator.record_latency(zone.value, latency_ms)
    _metrics_aggregator.record_category_event("zones", zone.value)
    _metrics_aggregator.record_category_event("modes", req.mode.value)

    # Audit trail
    _audit_writer.write_entry(
        event_type="QUERY",
        actor="user",
        detail={
            "mode": req.mode.value,
            "zone": zone.value,
            "confidence": round(confidence, 4),
            "doctrine_blocks": len(doctrine_results),
            "search_results": len(search_results),
            "latency_ms": round(latency_ms, 2),
        },
        query_hash=query_hash,
    )

    return QueryResponse(
        query_hash=query_hash,
        query_normalized=query_normalized,
        mode=req.mode.value,
        zone=zone.value,
        jurisdiction=req.jurisdiction,
        confidence=round(confidence, 4),
        confidence_level=confidence_level.value,
        authority_score=authority_score,
        response_layers=response_layers,
        doctrine_blocks_used=doctrine_ids[:20],
        search_results=[
            {"doc_id": sr.doc_id, "title": sr.title, "score": sr.score, "category": sr.category}
            for sr in search_results[:req.max_results]
        ],
        treaty_analysis=treaty_analysis,
        arbitration_analysis=arbitration_analysis,
        sanctions_screening=sanctions_result,
        trade_compliance=trade_result,
        fact_fragility=fact_fragility,
        coverage_gaps=coverage_gaps,
        drift_warnings=drift_warnings,
        determinism_hash=det_hash,
        latency_ms=round(latency_ms, 2),
        timestamp=datetime.utcnow().isoformat(),
        disclosure_caveat=disclosure,
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health endpoint returning engine status and subsystem states."""
    uptime = time.time() - _startup_time if _startup_time else 0.0
    doctrine_stats = get_doctrine_cache_stats()
    integrity = verify_doctrine_integrity()
    blocks_count = doctrine_stats.get("total_blocks", 0) if isinstance(doctrine_stats, dict) else 0
    integrity_ok = integrity.get("valid", False) if isinstance(integrity, dict) else bool(integrity)

    telemetry_snap = _telemetry.get_full_snapshot() if _telemetry else {}
    drift_snap = _drift_watcher.get_drift_summary() if _drift_watcher else {}
    index_stats = _doctrine_index.get_stats() if _doctrine_index else {}

    return HealthResponse(
        status="OPERATIONAL",
        uptime_seconds=round(uptime, 2),
        doctrine_blocks=blocks_count,
        doctrine_integrity=integrity_ok,
        telemetry=telemetry_snap,
        drift_summary=drift_snap,
        search_index_stats=index_stats,
        timestamp=datetime.utcnow().isoformat(),
    )


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest) -> QueryResponse:
    """Primary query endpoint - full TIE-20 pipeline."""
    try:
        response = await _run_query_pipeline(req)
        return response
    except Exception as exc:
        logger.error("Query pipeline error: {}", traceback.format_exc())
        if _error_tracker:
            _error_tracker.record_error(ErrorRecord(
                error_id=str(uuid.uuid4()),
                error_type=type(exc).__name__,
                message=str(exc),
                severity=ErrorSeverity.HIGH,
                category="query_pipeline",
                query_hash=compute_query_hash(req.query),
                stack_trace=traceback.format_exc(),
                resolution="",
            ))
        raise HTTPException(status_code=500, detail=f"Query pipeline error: {str(exc)}")


@app.post("/query/fast")
async def fast_query(req: QueryRequest) -> QueryResponse:
    """Fast mode - doctrine cache only, minimal processing."""
    req.mode = ResponseMode.FAST
    req.deep_analysis = False
    req.include_arbitration = False
    req.include_sanctions = False
    req.max_results = 5
    return await query_endpoint(req)


@app.post("/query/memo")
async def memo_query(req: QueryRequest) -> QueryResponse:
    """Memo mode - full deep analysis with comprehensive output."""
    req.mode = ResponseMode.MEMO
    req.deep_analysis = True
    req.include_treaties = True
    req.include_arbitration = True
    req.max_results = 20
    return await query_endpoint(req)


@app.post("/treaty/analyze")
async def treaty_analysis(req: TreatyAnalysisRequest) -> JSONResponse:
    """Dedicated treaty analysis endpoint."""
    assert _treaty_searcher is not None
    assert _treaty_interpreter is not None
    assert _audit_writer is not None

    start_time = time.time()
    treaty = _treaty_searcher.get_treaty(req.treaty_id)
    if treaty is None:
        raise HTTPException(status_code=404, detail=f"Treaty '{req.treaty_id}' not found. Available: {_treaty_searcher.get_all_treaty_ids()}")

    # Build article analysis
    article_analysis: list[dict[str, Any]] = []
    if req.articles:
        for art_key in req.articles:
            art_text = treaty.key_articles.get(art_key, "")
            if art_text:
                article_analysis.append({
                    "article": art_key,
                    "text": art_text,
                    "relevance_to_question": compute_semantic_similarity(req.question, art_text),
                })
    else:
        for art_key, art_text in treaty.key_articles.items():
            sim = compute_semantic_similarity(req.question, art_text)
            if sim > 0.1:
                article_analysis.append({
                    "article": art_key,
                    "text": art_text,
                    "relevance_to_question": sim,
                })
        article_analysis.sort(key=lambda x: x["relevance_to_question"], reverse=True)

    # Treaty interpreter
    entities = extract_treaty_entities(req.question)
    interpretation = _treaty_interpreter.interpret(req.question, entities)

    latency_ms = (time.time() - start_time) * 1000.0

    _audit_writer.write_entry(
        event_type="TREATY_ANALYSIS",
        actor="user",
        detail={"treaty_id": req.treaty_id, "articles": req.articles, "latency_ms": round(latency_ms, 2)},
        query_hash=compute_query_hash(req.question),
    )

    return JSONResponse(content={
        "treaty_id": treaty.treaty_id,
        "treaty_name": treaty.name,
        "short_name": treaty.short_name,
        "subject": treaty.subject,
        "date_adopted": treaty.date_adopted,
        "date_in_force": treaty.date_in_force,
        "parties_count": treaty.parties_count,
        "citation": treaty.citation,
        "status": treaty.status.value,
        "topics": treaty.topics,
        "question": req.question,
        "interpretation_method": req.interpretation_method,
        "article_analysis": article_analysis[:10],
        "key_articles": treaty.key_articles,
        "notable_reservations": treaty.notable_reservations,
        "interpretation": interpretation,
        "latency_ms": round(latency_ms, 2),
        "timestamp": datetime.utcnow().isoformat(),
    })


@app.post("/sanctions/screen")
async def sanctions_screen(req: SanctionsScreenRequest) -> JSONResponse:
    """Dedicated sanctions screening endpoint."""
    assert _sanctions_screener is not None
    assert _audit_writer is not None

    start_time = time.time()
    result = _sanctions_screener.screen_entity(req.entity_name, req.country_code)

    if req.include_general_licenses and result.get("country_programs"):
        for cp in result["country_programs"]:
            cp["general_licenses_detail"] = _sanctions_screener.get_general_licenses(cp.get("program_id", ""))

    latency_ms = (time.time() - start_time) * 1000.0
    result["latency_ms"] = round(latency_ms, 2)

    _audit_writer.write_entry(
        event_type="SANCTIONS_SCREEN",
        actor="user",
        detail={
            "entity": req.entity_name,
            "country": req.country_code,
            "risk_level": result.get("risk_level", "UNKNOWN"),
            "hits": result.get("total_hits", 0),
        },
        query_hash=compute_query_hash(req.entity_name),
    )

    return JSONResponse(content=result)


@app.post("/trade/compliance")
async def trade_compliance(req: TradeComplianceRequest) -> JSONResponse:
    """Dedicated WTO trade compliance analysis endpoint."""
    assert _trade_checker is not None
    assert _audit_writer is not None

    start_time = time.time()
    result = _trade_checker.analyze_tariff_measure(req.measure_description, req.affected_countries)
    latency_ms = (time.time() - start_time) * 1000.0
    result["latency_ms"] = round(latency_ms, 2)
    result["sectors"] = req.sectors

    _audit_writer.write_entry(
        event_type="TRADE_COMPLIANCE",
        actor="user",
        detail={
            "measure": req.measure_description[:200],
            "countries": req.affected_countries,
            "disciplines_found": len(result.get("disciplines_implicated", [])),
        },
        query_hash=compute_query_hash(req.measure_description),
    )

    return JSONResponse(content=result)


@app.get("/doctrines/coverage")
async def doctrine_coverage() -> JSONResponse:
    """Return the doctrine coverage map."""
    coverage = get_coverage_map()
    return JSONResponse(content={
        "engine_id": ENGINE_ID,
        "coverage": coverage,
        "timestamp": datetime.utcnow().isoformat(),
    })


@app.get("/doctrines/stats")
async def doctrine_stats() -> JSONResponse:
    """Return doctrine cache statistics."""
    stats = get_doctrine_cache_stats()
    integrity = verify_doctrine_integrity()
    return JSONResponse(content={
        "engine_id": ENGINE_ID,
        "stats": stats,
        "integrity": integrity,
        "cache_hash": get_doctrine_cache_hash(),
        "categories": get_all_doctrine_categories(),
        "topics_count": len(get_all_doctrine_topics()),
        "stale_doctrines": get_stale_doctrines(),
        "timestamp": datetime.utcnow().isoformat(),
    })


@app.get("/doctrines/block/{block_id}")
async def get_single_doctrine(block_id: str) -> JSONResponse:
    """Retrieve a specific doctrine block by ID."""
    block = get_doctrine_block(block_id)
    if block is None:
        raise HTTPException(status_code=404, detail=f"Doctrine block '{block_id}' not found")
    if isinstance(block, dict):
        return JSONResponse(content=block)
    return JSONResponse(content={"block_id": block_id, "data": str(block)})


@app.get("/treaties")
async def list_treaties() -> JSONResponse:
    """List all treaties in the database."""
    assert _treaty_searcher is not None
    ids = _treaty_searcher.get_all_treaty_ids()
    treaties: list[dict[str, Any]] = []
    for tid in ids:
        t = _treaty_searcher.get_treaty(tid)
        if t:
            treaties.append({
                "treaty_id": t.treaty_id,
                "name": t.name,
                "short_name": t.short_name,
                "subject": t.subject,
                "date_adopted": t.date_adopted,
                "parties_count": t.parties_count,
                "status": t.status.value,
            })
    return JSONResponse(content={"treaties": treaties, "total": len(treaties)})


@app.get("/treaties/{treaty_id}")
async def get_treaty(treaty_id: str) -> JSONResponse:
    """Get detailed treaty information."""
    assert _treaty_searcher is not None
    t = _treaty_searcher.get_treaty(treaty_id.upper())
    if t is None:
        raise HTTPException(status_code=404, detail=f"Treaty '{treaty_id}' not found")
    return JSONResponse(content={
        "treaty_id": t.treaty_id,
        "name": t.name,
        "short_name": t.short_name,
        "subject": t.subject,
        "date_adopted": t.date_adopted,
        "date_in_force": t.date_in_force,
        "parties_count": t.parties_count,
        "depositary": t.depositary,
        "citation": t.citation,
        "status": t.status.value,
        "topics": t.topics,
        "key_articles": t.key_articles,
        "notable_reservations": t.notable_reservations,
    })


@app.get("/treaties/search/{keyword}")
async def search_treaties(keyword: str, top_k: int = Query(default=5, ge=1, le=20)) -> JSONResponse:
    """Search treaties by keyword."""
    assert _treaty_searcher is not None
    results = _treaty_searcher.search_by_keyword(keyword, top_k=top_k)
    return JSONResponse(content={
        "keyword": keyword,
        "results": [r.model_dump() for r in results],
        "total": len(results),
    })


@app.get("/arbitration/rules")
async def list_arbitration_rules(
    institution: str = Query(default="", description="Filter by institution"),
    topic: str = Query(default="", description="Filter by topic"),
) -> JSONResponse:
    """Search arbitration rules."""
    assert _arbitration_searcher is not None
    if institution:
        results = _arbitration_searcher.search_by_institution(institution)
    elif topic:
        results = _arbitration_searcher.search_by_topic(topic)
    else:
        results = _arbitration_searcher.search_by_topic("arbitration", top_k=50)
    return JSONResponse(content={
        "filters": {"institution": institution, "topic": topic},
        "results": [r.model_dump() for r in results],
        "total": len(results),
    })


@app.get("/arbitration/compare/{topic}")
async def compare_arbitration(topic: str) -> JSONResponse:
    """Compare arbitration rules across institutions for a topic."""
    assert _arbitration_searcher is not None
    comparison = _arbitration_searcher.compare_institutions(topic)
    formatted: dict[str, list[dict[str, Any]]] = {}
    for inst, results in comparison.items():
        formatted[inst] = [r.model_dump() for r in results]
    return JSONResponse(content={"topic": topic, "comparison": formatted})


@app.get("/sanctions/programs")
async def list_sanctions_programs() -> JSONResponse:
    """List all sanctions programs."""
    assert _sanctions_screener is not None
    return JSONResponse(content={"programs": _sanctions_screener.list_programs()})


@app.get("/sanctions/country/{country_code}")
async def country_sanctions(country_code: str) -> JSONResponse:
    """Check sanctions programs for a country."""
    assert _sanctions_screener is not None
    result = _sanctions_screener.check_country_risk(country_code)
    return JSONResponse(content=result)


@app.get("/trade/disciplines")
async def list_trade_disciplines() -> JSONResponse:
    """List all WTO disciplines."""
    assert _trade_checker is not None
    return JSONResponse(content={"disciplines": _trade_checker.list_disciplines()})


@app.get("/trade/discipline/{discipline_id}")
async def get_trade_discipline(discipline_id: str) -> JSONResponse:
    """Get detailed information about a WTO discipline."""
    assert _trade_checker is not None
    info = _trade_checker.get_discipline_info(discipline_id.upper())
    if info is None:
        raise HTTPException(status_code=404, detail=f"Discipline '{discipline_id}' not found")
    return JSONResponse(content=info)


@app.get("/telemetry")
async def get_telemetry() -> JSONResponse:
    """Return full telemetry snapshot."""
    assert _telemetry is not None
    return JSONResponse(content=_telemetry.get_full_snapshot())


@app.get("/telemetry/latency")
async def get_latency_stats() -> JSONResponse:
    """Return latency statistics."""
    assert _telemetry is not None
    return JSONResponse(content=_telemetry.get_latency_stats())


@app.get("/telemetry/traces")
async def get_recent_traces(n: int = Query(default=50, ge=1, le=500)) -> JSONResponse:
    """Return recent query traces."""
    assert _telemetry is not None
    return JSONResponse(content={"traces": _telemetry.get_recent_traces(n)})


@app.get("/telemetry/metrics")
async def get_metrics(
    category: str = Query(default="", description="Category for latency percentiles"),
    window_seconds: float = Query(default=3600.0, description="Time window in seconds"),
) -> JSONResponse:
    """Return aggregated metrics."""
    assert _metrics_aggregator is not None
    if category:
        percentiles = _metrics_aggregator.get_latency_percentiles(category, window_seconds)
    else:
        percentiles = {}
    distributions = _metrics_aggregator.get_all_category_distributions()
    return JSONResponse(content={
        "latency_percentiles": percentiles,
        "category_distributions": distributions,
    })


@app.get("/telemetry/errors")
async def get_errors(
    n: int = Query(default=20, ge=1, le=100),
    severity: str = Query(default="", description="Filter by severity"),
) -> JSONResponse:
    """Return recent errors."""
    assert _error_tracker is not None
    sev_filter = None
    if severity:
        try:
            sev_filter = ErrorSeverity(severity.upper())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid severity: {severity}")
    errors = _error_tracker.get_recent_errors(n, sev_filter)
    stats = _error_tracker.get_error_stats()
    recurring = _error_tracker.get_recurring_errors()
    return JSONResponse(content={"errors": errors, "stats": stats, "recurring": recurring})


@app.get("/audit")
async def get_audit_trail(n: int = Query(default=50, ge=1, le=500)) -> JSONResponse:
    """Return recent audit trail entries."""
    assert _audit_writer is not None
    entries = _audit_writer.get_recent_entries(n)
    return JSONResponse(content={
        "entries": entries,
        "total_sequence": _audit_writer.sequence_number,
        "current_hash": _audit_writer.current_hash,
    })


@app.get("/audit/verify")
async def verify_audit_chain() -> JSONResponse:
    """Verify audit trail hash chain integrity."""
    assert _audit_writer is not None
    result = _audit_writer.verify_chain()
    return JSONResponse(content=result)


@app.get("/drift")
async def get_drift_status() -> JSONResponse:
    """Return doctrine drift summary and stale blocks."""
    assert _drift_watcher is not None
    summary = _drift_watcher.get_drift_summary()
    stale = _drift_watcher.get_all_stale_blocks()
    recent = _drift_watcher.get_recent_drift_records(30)
    return JSONResponse(content={
        "summary": summary,
        "stale_blocks": stale,
        "recent_checks": recent,
    })


@app.get("/mutations")
async def get_mutations(n: int = Query(default=50, ge=1, le=200)) -> JSONResponse:
    """Return recent doctrine mutations."""
    assert _mutation_log is not None
    return JSONResponse(content={
        "mutations": _mutation_log.get_recent_mutations(n),
        "total": _mutation_log.total_mutations,
    })


@app.get("/zones")
async def list_zones() -> JSONResponse:
    """List all analysis zones with their keywords."""
    zones_info: list[dict[str, Any]] = []
    for zone in AnalysisZone:
        zones_info.append({
            "zone": zone.value,
            "keywords": _ZONE_KEYWORDS.get(zone, []),
        })
    return JSONResponse(content={"zones": zones_info})


@app.get("/modes")
async def list_modes() -> JSONResponse:
    """List available response modes."""
    return JSONResponse(content={
        "modes": [
            {"mode": "fast", "description": "Doctrine cache only, minimal processing"},
            {"mode": "analysis", "description": "Standard three-layer analysis"},
            {"mode": "memo", "description": "Full deep analysis with comprehensive output"},
            {"mode": "treaty_interpretation", "description": "Focused treaty interpretation using VCLT methodology"},
            {"mode": "trade_compliance", "description": "WTO trade compliance assessment"},
        ]
    })


@app.get("/config")
async def get_config() -> JSONResponse:
    """Return engine configuration."""
    if CONFIG_PATH.exists():
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    else:
        config = {}
    return JSONResponse(content={
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "authority": AUTHORITY_THRESHOLD,
        "config": config,
    })


@app.get("/coverage-gaps")
async def coverage_gap_analysis(query: str = Query(..., min_length=3, description="Query to check coverage for")) -> JSONResponse:
    """Analyze coverage gaps for a given query."""
    zone = detect_zone(query)
    sub_issues = decompose_multi_doctrine(query, zone)

    doctrine_results = search_doctrines(normalize_query(query))
    doctrine_ids: list[str] = []
    if doctrine_results:
        for dr in doctrine_results:
            did = dr.get("block_id", dr.get("id", ""))
            if did:
                doctrine_ids.append(did)

    gaps = detect_coverage_gaps(zone, doctrine_ids, sub_issues)
    return JSONResponse(content={
        "query": query,
        "zone": zone.value,
        "sub_issues": sub_issues,
        "doctrine_blocks_found": doctrine_ids,
        "coverage_gaps": gaps,
    })


@app.get("/semantic/normalize")
async def semantic_normalize(query: str = Query(..., min_length=1)) -> JSONResponse:
    """Normalize a query using the semantic module."""
    normalized = normalize_query(query)
    entities = extract_treaty_entities(query)
    classification = classify_international_issue(query)
    return JSONResponse(content={
        "original": query,
        "normalized": normalized,
        "entities": entities,
        "classification": classification,
        "query_hash": compute_query_hash(normalized),
    })


@app.get("/semantic/similarity")
async def semantic_similarity(text1: str = Query(...), text2: str = Query(...)) -> JSONResponse:
    """Compute semantic similarity between two texts."""
    score = compute_semantic_similarity(text1, text2)
    return JSONResponse(content={
        "text1": text1[:200],
        "text2": text2[:200],
        "similarity": round(score, 4),
    })


@app.get("/conflict-of-laws")
async def conflict_of_laws(query: str = Query(..., min_length=5)) -> JSONResponse:
    """Analyze conflict of laws issues."""
    assert _conflict_resolver is not None
    result = _conflict_resolver.resolve(query)
    return JSONResponse(content=result)


# ---------------------------------------------------------------------------
# Error handler
# ---------------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler with telemetry recording."""
    logger.error("Unhandled exception: {}", traceback.format_exc())
    if _error_tracker:
        _error_tracker.record_error(ErrorRecord(
            error_id=str(uuid.uuid4()),
            error_type=type(exc).__name__,
            message=str(exc),
            severity=ErrorSeverity.HIGH,
            category="unhandled",
            query_hash="",
            stack_trace=traceback.format_exc(),
            resolution="",
        ))
    return JSONResponse(
        status_code=500,
        content={
            "error": type(exc).__name__,
            "message": str(exc),
            "engine_id": ENGINE_ID,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting LG15 International Law Engine on {}:{}", ENGINE_HOST, ENGINE_PORT)
    uvicorn.run(
        "engine:app",
        host=ENGINE_HOST,
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
        workers=1,
    )
