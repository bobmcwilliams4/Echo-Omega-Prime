"""
E07 — Query Interpreter Engine
================================
TIER: ENT (Enterprise) | MODE: HYB (Hybrid) | AUTH: 11.0 SOVEREIGN | PORT: 8607

Natural-language query interpretation engine for the ECHO OMEGA PRIME oil & gas
land management platform.  Takes free-text questions about title, leases, minerals,
regulatory matters, production data, and risk — classifies intent, extracts
structured parameters (county, legal description, operator, API#, dates, parties),
expands abbreviations, detects jurisdiction, scores confidence, and recommends
downstream engine routing.

Rule-based core with optional LLM-assist fallback via CognitionCloudRetriever.

TIE-20 Compliant: All 20 mandatory components implemented.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import sys
import time
import uuid
from collections import Counter, OrderedDict, defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, Union

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field, field_validator

# ─────────────────────────────────────────────────────────────────────────────
# PATH SETUP — must precede local imports
# ─────────────────────────────────────────────────────────────────────────────
ENGINE_DIR = Path(__file__).resolve().parent
ENGINES_DIR = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINE_DIR))
sys.path.insert(0, str(ENGINES_DIR))

try:
    from _shared.cloud_retriever import CognitionCloudRetriever
except ImportError:
    CognitionCloudRetriever = None  # type: ignore[assignment,misc]
    logger.warning("CognitionCloudRetriever unavailable — cloud knowledge disabled")

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
ENGINE_ID = "E07"
ENGINE_NAME = "Query Interpreter"
ENGINE_VERSION = "1.0.0"
ENGINE_TIER = "ENT"
ENGINE_MODE = "HYB"
ENGINE_PORT = 8607
AUTHORITY_LEVEL = 11.0

AUDIT_LOG_PATH = ENGINE_DIR / "audit_trail.jsonl"
DOCTRINE_CACHE_PATH = ENGINE_DIR / "doctrine_cache.json"
SEMANTIC_DICT_PATH = ENGINE_DIR / "semantic_dict.json"
COVERAGE_MAP_PATH = ENGINE_DIR / "coverage_map.json"
DRIFT_LOG_PATH = ENGINE_DIR / "drift_log.jsonl"

MAX_QUERY_LENGTH = 10_000
MIN_CONFIDENCE = 0.15
HIGH_CONFIDENCE_THRESHOLD = 0.80
DEEP_ANALYSIS_THRESHOLD = 0.40
LRU_CACHE_SIZE = 512

# ─────────────────────────────────────────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────────────────────────────────────────

class ResponseMode(str, Enum):
    """Three-tier response mode per TIE standard."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class QueryIntent(str, Enum):
    """Classified intents that a user query can map to."""
    TITLE_SEARCH = "TITLE_SEARCH"
    LEASE_ANALYSIS = "LEASE_ANALYSIS"
    MINERAL_CALC = "MINERAL_CALC"
    REGULATORY = "REGULATORY"
    PRODUCTION = "PRODUCTION"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"
    COMPARISON = "COMPARISON"
    REVENUE_PROJECTION = "REVENUE_PROJECTION"
    DOCUMENT_REQUEST = "DOCUMENT_REQUEST"
    CHAIN_OF_TITLE = "CHAIN_OF_TITLE"
    RIGHT_OF_WAY = "RIGHT_OF_WAY"
    WATER_RIGHTS = "WATER_RIGHTS"
    GENERAL = "GENERAL"
    UNKNOWN = "UNKNOWN"


class ConfidenceLevel(str, Enum):
    """Stratified confidence per TIE epistemic standard."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    """Zoned analysis per TIE — never blur zones."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class AuthorityLevel(str, Enum):
    """Hierarchical authority for query interpretation context."""
    STATUTORY = "STATUTORY"
    REGULATORY = "REGULATORY"
    JUDICIAL = "JUDICIAL"
    AGENCY_GUIDANCE = "AGENCY_GUIDANCE"
    INDUSTRY_PRACTICE = "INDUSTRY_PRACTICE"
    INTERNAL_POLICY = "INTERNAL_POLICY"


# ─────────────────────────────────────────────────────────────────────────────
# PYDANTIC MODELS — ALL I/O typed
# ─────────────────────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    """Incoming query from a user or upstream engine."""
    query: str = Field(..., min_length=1, max_length=MAX_QUERY_LENGTH, description="Free-text question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="FAST | DEFENSE | MEMO")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Optional prior context")
    session_id: Optional[str] = Field(default=None, description="Session tracking")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="PLANNING | REPORTING | AUDIT")
    include_routing: bool = Field(default=True, description="Include downstream engine routing suggestions")
    include_expansion: bool = Field(default=True, description="Include query expansion info")
    deep_analysis: bool = Field(default=False, description="Force deep analysis even on high-confidence hits")

    @field_validator("query")
    @classmethod
    def strip_query(cls, v: str) -> str:
        return v.strip()


class ExtractedEntity(BaseModel):
    """A single extracted entity from the query."""
    entity_type: str = Field(..., description="COUNTY | SECTION | TOWNSHIP | RANGE | OPERATOR | API_NUMBER | INSTRUMENT | DATE | PARTY | STATE | BLOCK | SURVEY | ABSTRACT | WELL_NAME | ACREAGE")
    value: str
    original_span: Optional[str] = Field(default=None, description="Original text that produced this entity")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class RoutingRecommendation(BaseModel):
    """Which downstream engine should handle this query."""
    engine_id: str
    engine_name: str
    relevance_score: float = Field(ge=0.0, le=1.0)
    reason: str
    port: int


class QueryExpansion(BaseModel):
    """Abbreviation expansions and synonym normalizations applied."""
    original_term: str
    expanded_term: str
    expansion_type: str  # ABBREVIATION | SYNONYM | NORMALIZATION


class InterpretationResult(BaseModel):
    """Full interpretation of a single query."""
    query_id: str
    original_query: str
    normalized_query: str
    primary_intent: QueryIntent
    secondary_intents: List[QueryIntent] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_level: ConfidenceLevel
    entities: List[ExtractedEntity] = Field(default_factory=list)
    jurisdiction: Optional[Dict[str, Any]] = None
    routing: List[RoutingRecommendation] = Field(default_factory=list)
    expansions: List[QueryExpansion] = Field(default_factory=list)
    analysis_zone: AnalysisZone
    authority_chain: List[str] = Field(default_factory=list)
    doctrine_hits: List[str] = Field(default_factory=list)
    deep_analysis: Optional[Dict[str, Any]] = None
    determinism_hash: str = ""
    latency_ms: float = 0.0
    mode: ResponseMode = ResponseMode.FAST
    timestamp: str = ""


class QueryResponse(BaseModel):
    """Top-level API response."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    result: InterpretationResult
    telemetry: Dict[str, Any] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    """Health endpoint response."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    status: str = "healthy"
    uptime_seconds: float = 0.0
    queries_processed: int = 0
    cache_size: int = 0
    cloud_retriever_available: bool = False
    doctrine_count: int = 0
    intent_coverage: Dict[str, int] = Field(default_factory=dict)
    timestamp: str = ""


# ─────────────────────────────────────────────────────────────────────────────
# ABBREVIATION EXPANSION DICTIONARY
# ─────────────────────────────────────────────────────────────────────────────

ABBREVIATION_MAP: Dict[str, str] = {
    "twp": "township",
    "sec": "section",
    "rng": "range",
    "blk": "block",
    "rrc": "railroad commission",
    "glc": "general land office",
    "glo": "general land office",
    "bpo": "before payout",
    "apo": "after payout",
    "nri": "net revenue interest",
    "wri": "working interest",
    "wi": "working interest",
    "ri": "royalty interest",
    "orri": "overriding royalty interest",
    "npri": "non-participating royalty interest",
    "nmi": "net mineral interest",
    "hw": "horizontal well",
    "vw": "vertical well",
    "ogm": "oil gas and mineral",
    "ogml": "oil gas and mineral lease",
    "mol": "mineral owners lease",
    "row": "right of way",
    "bop": "blowout preventer",
    "api": "american petroleum institute",
    "mcf": "thousand cubic feet",
    "mmcf": "million cubic feet",
    "bbl": "barrel",
    "boe": "barrel of oil equivalent",
    "bopd": "barrels of oil per day",
    "mcfd": "thousand cubic feet per day",
    "ip": "initial production",
    "eur": "estimated ultimate recovery",
    "psi": "pounds per square inch",
    "td": "total depth",
    "pbtd": "plugged back total depth",
    "frac": "hydraulic fracturing",
    "perf": "perforation",
    "csg": "casing",
    "tbg": "tubing",
    "wh": "wellhead",
    "swp": "spacing unit pooling",
    "dpu": "drilling and production unit",
    "pud": "proved undeveloped",
    "pdp": "proved developed producing",
    "dnp": "proved developed non-producing",
    "susp": "suspended well",
    "p&a": "plugged and abandoned",
    "ta": "temporarily abandoned",
    "si": "shut in",
    "dept": "department",
    "comm": "commission",
    "dist": "district",
    "co": "county",
    "st": "state",
    "tx": "texas",
    "nm": "new mexico",
    "ok": "oklahoma",
    "nd": "north dakota",
    "pa": "pennsylvania",
    "wv": "west virginia",
    "la": "louisiana",
    "ks": "kansas",
    "mt": "montana",
    "wy": "wyoming",
    "co_state": "colorado",
    "ut": "utah",
    "oh": "ohio",
    "ar": "arkansas",
    "ms": "mississippi",
    "al": "alabama",
    "tceq": "texas commission on environmental quality",
    "epa": "environmental protection agency",
    "ferc": "federal energy regulatory commission",
    "blm": "bureau of land management",
    "onrr": "office of natural resources revenue",
    "doe": "department of energy",
    "uic": "underground injection control",
    "npdes": "national pollutant discharge elimination system",
    "nepa": "national environmental policy act",
    "cercla": "comprehensive environmental response compensation and liability act",
    "rcra": "resource conservation and recovery act",
    "tsca": "toxic substances control act",
    "osha": "occupational safety and health administration",
    "msha": "mine safety and health administration",
    "dot": "department of transportation",
    "phmsa": "pipeline and hazardous materials safety administration",
}

# ─────────────────────────────────────────────────────────────────────────────
# SEMANTIC NORMALIZATION TABLE
# ─────────────────────────────────────────────────────────────────────────────

SEMANTIC_NORMALIZATION: Dict[str, str] = {
    "deed": "conveyance",
    "warranty deed": "general warranty deed",
    "special warranty deed": "limited warranty deed",
    "quitclaim deed": "quitclaim conveyance",
    "quit claim": "quitclaim conveyance",
    "grant deed": "grant conveyance",
    "bargain and sale": "bargain and sale deed",
    "mineral deed": "mineral conveyance",
    "royalty deed": "royalty conveyance",
    "correction deed": "corrective instrument",
    "oil and gas lease": "ogml",
    "oil gas lease": "ogml",
    "paid up lease": "paid-up oil and gas lease",
    "top lease": "top lease (secondary term lease)",
    "shut-in royalty": "shut-in royalty payment",
    "habendum clause": "term clause",
    "granting clause": "grant of rights",
    "pooling clause": "unitization/pooling provision",
    "pugh clause": "depth severance/pugh clause",
    "force majeure": "force majeure provision",
    "after-acquired title": "after-acquired interest doctrine",
    "estoppel by deed": "estoppel by deed doctrine",
    "rule against perpetuities": "RAP / rule against perpetuities",
    "adverse possession": "adverse possession / limitations",
    "laches": "equitable defense of laches",
    "prescription": "prescriptive rights",
    "title opinion": "title examination opinion",
    "run sheet": "title abstract run sheet",
    "abstract of title": "title abstract",
    "chain of title": "title chain examination",
    "curative": "curative instrument / title curative",
    "affidavit of heirship": "heirship affidavit",
    "probate": "probate proceeding",
    "partition": "partition action",
    "condemnation": "eminent domain / condemnation",
    "easement": "easement / servitude",
    "right of way": "right-of-way easement",
    "surface damage": "surface use/damage provision",
    "accommodation doctrine": "surface owner accommodation doctrine",
    "dominant mineral estate": "dominant estate (mineral)",
    "executive rights": "executive right to lease",
    "bonus": "lease bonus payment",
    "delay rental": "delay rental payment",
    "primary term": "lease primary term",
    "secondary term": "lease secondary term (production)",
    "cessation of production": "temporary cessation clause",
    "dry hole clause": "dry hole / continuous drilling clause",
    "continuous drilling": "continuous development clause",
    "retained acreage": "retained acreage provision",
    "entirety clause": "entirety / Mother Hubbard clause",
    "unit": "spacing or pooling unit",
    "proration unit": "proration / allocation unit",
    "field rules": "field rules / special field rules",
    "statewide rules": "general conservation rules / Rule 37/38",
    "rule 37": "RRC Rule 37 (spacing exception)",
    "rule 38": "RRC Rule 38 (density exception)",
    "p-5 form": "RRC Form P-5 organization report",
    "w-1 form": "RRC Form W-1 drilling permit",
    "w-2 form": "RRC Form W-2 oil well potential test",
    "g-1 form": "RRC Form G-1 gas well potential test",
    "h-10 form": "RRC Form H-10 disposal/injection permit",
}

# ─────────────────────────────────────────────────────────────────────────────
# INTENT KEYWORD PATTERNS — the doctrine cache for query classification
# ─────────────────────────────────────────────────────────────────────────────

class DoctrinePattern:
    """A single doctrine-cache entry mapping keywords and regex patterns to intents."""

    __slots__ = (
        "pattern_id", "intent", "keywords", "regex_patterns", "weight",
        "description", "authority", "counter_signals", "required_entities",
    )

    def __init__(
        self,
        pattern_id: str,
        intent: QueryIntent,
        keywords: List[str],
        regex_patterns: List[str],
        weight: float = 1.0,
        description: str = "",
        authority: AuthorityLevel = AuthorityLevel.INDUSTRY_PRACTICE,
        counter_signals: Optional[List[str]] = None,
        required_entities: Optional[List[str]] = None,
    ) -> None:
        self.pattern_id = pattern_id
        self.intent = intent
        self.keywords = [k.lower() for k in keywords]
        self.regex_patterns = [re.compile(p, re.IGNORECASE) for p in regex_patterns]
        self.weight = weight
        self.description = description
        self.authority = authority
        self.counter_signals = [c.lower() for c in (counter_signals or [])]
        self.required_entities = required_entities or []

    def score(self, text_lower: str, entities_found: Set[str]) -> float:
        """Score how well this pattern matches the given text."""
        kw_hits = sum(1 for k in self.keywords if k in text_lower)
        rx_hits = sum(1 for rx in self.regex_patterns if rx.search(text_lower))
        counter = sum(1 for c in self.counter_signals if c in text_lower)
        entity_bonus = sum(0.1 for req in self.required_entities if req in entities_found)

        raw = (kw_hits * 0.25 + rx_hits * 0.35 + entity_bonus) * self.weight
        penalty = counter * 0.15
        return max(0.0, raw - penalty)


# ── Build the doctrine cache ────────────────────────────────────────────────

def _build_doctrine_cache() -> List[DoctrinePattern]:
    """Construct 30+ doctrine patterns covering all oil & gas query intents."""
    patterns: List[DoctrinePattern] = []

    # ── TITLE_SEARCH patterns ────────────────────────────────────────────
    patterns.append(DoctrinePattern(
        pattern_id="TS01",
        intent=QueryIntent.TITLE_SEARCH,
        keywords=["title", "deed", "conveyance", "ownership", "grantor", "grantee",
                   "vesting", "chain of title", "abstract", "run sheet"],
        regex_patterns=[
            r"\btitle\s+(?:search|exam|check|review|opinion)\b",
            r"\bwho\s+owns\b",
            r"\bcurrent\s+owner\b",
            r"\bchain\s+of\s+title\b",
            r"\btitle\s+to\s+(?:the\s+)?(?:minerals?|surface|land)\b",
        ],
        weight=1.2,
        description="Queries about ownership, title examination, deed review, vesting analysis",
        authority=AuthorityLevel.JUDICIAL,
        counter_signals=["lease", "royalty rate", "production volume", "regulation"],
    ))

    patterns.append(DoctrinePattern(
        pattern_id="TS02",
        intent=QueryIntent.TITLE_SEARCH,
        keywords=["owner", "ownership", "vested", "record owner", "title holder",
                   "fee simple", "life estate", "remainder interest"],
        regex_patterns=[
            r"\bwho\s+(?:is|are)\s+the\s+(?:current\s+)?(?:mineral\s+)?owners?\b",
            r"\brecord\s+(?:title\s+)?owners?\b",
            r"\bfee\s+simple\s+(?:absolute|determinable|defeasible)\b",
        ],
        weight=1.0,
        description="Ownership-specific queries, fee simple analysis, record title",
        authority=AuthorityLevel.STATUTORY,
    ))

    patterns.append(DoctrinePattern(
        pattern_id="TS03",
        intent=QueryIntent.TITLE_SEARCH,
        keywords=["heirship", "probate", "intestate", "descent", "distribution",
                   "will", "estate", "decedent", "heir"],
        regex_patterns=[
            r"\bheirship\b",
            r"\bintestates?\s+succession\b",
            r"\bprobate\s+(?:of|the)?\s*(?:will|estate)\b",
            r"\bwho\s+inherit(?:ed|s)?\b",
        ],
        weight=1.1,
        description="Heirship and probate title inquiries",
        authority=AuthorityLevel.STATUTORY,
    ))

    # ── LEASE_ANALYSIS patterns ──────────────────────────────────────────
    patterns.append(DoctrinePattern(
        pattern_id="LA01",
        intent=QueryIntent.LEASE_ANALYSIS,
        keywords=["lease", "lessee", "lessor", "primary term", "secondary term",
                   "habendum", "royalty clause", "pooling clause", "pugh clause"],
        regex_patterns=[
            r"\b(?:oil\s+(?:and\s+)?gas\s+)?lease\s+(?:analysis|review|terms?|expir|renew)\b",
            r"\blease\s+(?:is|has|will)\s+(?:expir|terminat)\b",
            r"\bprimary\s+term\b",
            r"\bsecondary\s+term\b",
            r"\broyalty\s+(?:rate|percentage|clause)\b",
        ],
        weight=1.2,
        description="Oil and gas lease term analysis, clause interpretation, expiration checks",
        authority=AuthorityLevel.JUDICIAL,
        counter_signals=["production data", "well count"],
    ))

    patterns.append(DoctrinePattern(
        pattern_id="LA02",
        intent=QueryIntent.LEASE_ANALYSIS,
        keywords=["top lease", "held by production", "hbp", "cessation", "shut-in",
                   "delay rental", "bonus", "paid-up", "continuous operations"],
        regex_patterns=[
            r"\bheld\s+by\s+production\b",
            r"\btop\s+lease\b",
            r"\bcessation\s+of\s+(?:production|operations)\b",
            r"\bshut[\s-]?in\s+(?:royalty|payment|well)\b",
        ],
        weight=1.1,
        description="Lease maintenance, HBP status, cessation clause, shut-in analysis",
        authority=AuthorityLevel.JUDICIAL,
    ))

    patterns.append(DoctrinePattern(
        pattern_id="LA03",
        intent=QueryIntent.LEASE_ANALYSIS,
        keywords=["assignment", "farm-out", "farmout", "sublease", "overriding royalty",
                   "working interest assignment", "partial assignment"],
        regex_patterns=[
            r"\bassignment\s+of\s+(?:oil\s+(?:and\s+)?gas\s+)?lease\b",
            r"\bfarm[\s-]?out\s+(?:agreement|letter)\b",
            r"\boverrid(?:e|ing)\s+royalty\b",
        ],
        weight=1.0,
        description="Lease assignments, farm-outs, ORRI carve-outs",
        authority=AuthorityLevel.INDUSTRY_PRACTICE,
    ))

    # ── MINERAL_CALC patterns ────────────────────────────────────────────
    patterns.append(DoctrinePattern(
        pattern_id="MC01",
        intent=QueryIntent.MINERAL_CALC,
        keywords=["mineral interest", "royalty interest", "working interest",
                   "net revenue interest", "net mineral interest", "decimal interest",
                   "fractional interest", "undivided interest"],
        regex_patterns=[
            r"\b(?:what|calculate|compute)\s+(?:is\s+)?(?:the\s+)?(?:net\s+)?(?:mineral|royalty|revenue|working)\s+interest\b",
            r"\b\d+/\d+\s+(?:mineral|royalty|interest)\b",
            r"\bdecimal\s+interest\b",
            r"\b(?:nri|nmi|wi|ri|orri|npri)\s*(?:=|is|of)\b",
        ],
        weight=1.3,
        description="Mineral interest calculations, NRI/NMI, decimal conversions, fractional interests",
        authority=AuthorityLevel.INDUSTRY_PRACTICE,
        counter_signals=["regulation", "permit"],
        required_entities=["PARTY", "ACREAGE"],
    ))

    patterns.append(DoctrinePattern(
        pattern_id="MC02",
        intent=QueryIntent.MINERAL_CALC,
        keywords=["non-participating royalty", "npri", "executive rights",
                   "bonus interest", "rental interest", "surface rights"],
        regex_patterns=[
            r"\bnon[\s-]?participating\s+royalty\b",
            r"\bexecutive\s+right\b",
            r"\bsurface\s+(?:vs|versus|and)\s+mineral\b",
        ],
        weight=1.1,
        description="NPRI, executive rights analysis, surface vs mineral estate",
        authority=AuthorityLevel.STATUTORY,
    ))

    # ── REGULATORY patterns ──────────────────────────────────────────────
    patterns.append(DoctrinePattern(
        pattern_id="RG01",
        intent=QueryIntent.REGULATORY,
        keywords=["permit", "rule 37", "rule 38", "spacing", "density",
                   "railroad commission", "rrc", "tceq", "epa", "compliance"],
        regex_patterns=[
            r"\brule\s+3[78]\b",
            r"\bspacing\s+(?:exception|rule|requirement|unit)\b",
            r"\bdrilling\s+permit\b",
            r"\bw[\s-]?1\s+(?:form|permit|application)\b",
            r"\bcompliance\s+(?:with|issue|check|violation)\b",
        ],
        weight=1.2,
        description="Regulatory compliance, drilling permits, spacing rules, RRC matters",
        authority=AuthorityLevel.REGULATORY,
    ))

    patterns.append(DoctrinePattern(
        pattern_id="RG02",
        intent=QueryIntent.REGULATORY,
        keywords=["injection", "disposal", "uic", "h-10", "saltwater disposal",
                   "environmental", "flaring", "venting", "emissions"],
        regex_patterns=[
            r"\b(?:disposal|injection)\s+(?:well|permit|authorization)\b",
            r"\bh[\s-]?10\s+(?:form|permit)\b",
            r"\bflar(?:e|ing)\s+(?:permit|report|exception)\b",
            r"\bemissions?\s+(?:report|limit|standard)\b",
        ],
        weight=1.1,
        description="Environmental regulatory, disposal wells, emissions compliance",
        authority=AuthorityLevel.REGULATORY,
    ))

    patterns.append(DoctrinePattern(
        pattern_id="RG03",
        intent=QueryIntent.REGULATORY,
        keywords=["plugging", "abandonment", "p&a", "bond", "bonding",
                   "orphan well", "financial assurance", "decommission"],
        regex_patterns=[
            r"\bplug(?:ging|ged)?\s+(?:and\s+)?abandon\b",
            r"\borphan\s+well\b",
            r"\bfinancial\s+(?:assurance|security|bond)\b",
            r"\bdecommission\b",
        ],
        weight=1.0,
        description="Well plugging, abandonment, bonding, orphan wells",
        authority=AuthorityLevel.REGULATORY,
    ))

    # ── PRODUCTION patterns ──────────────────────────────────────────────
    patterns.append(DoctrinePattern(
        pattern_id="PD01",
        intent=QueryIntent.PRODUCTION,
        keywords=["production", "barrels", "mcf", "boe", "decline curve",
                   "ip rate", "eur", "producing", "cumulative production"],
        regex_patterns=[
            r"\bproduction\s+(?:data|history|volume|rate|report|decline)\b",
            r"\bhow\s+much\s+(?:oil|gas)\s+(?:is|was|has)\b",
            r"\binitial\s+production\b",
            r"\bdecline\s+(?:curve|rate|analysis)\b",
            r"\bcumulative\s+(?:production|output)\b",
        ],
        weight=1.2,
        description="Production data queries, decline curves, IP rates, EUR",
        authority=AuthorityLevel.AGENCY_GUIDANCE,
        required_entities=["OPERATOR", "API_NUMBER"],
    ))

    patterns.append(DoctrinePattern(
        pattern_id="PD02",
        intent=QueryIntent.PRODUCTION,
        keywords=["well status", "active well", "inactive", "shut-in", "temporarily abandoned",
                   "drilling", "completing", "spud date", "completion date"],
        regex_patterns=[
            r"\bwell\s+(?:status|condition|state)\b",
            r"\bspud\s+date\b",
            r"\bcompletion\s+date\b",
            r"\b(?:is|was)\s+the\s+well\s+(?:active|producing|shut[\s-]?in)\b",
        ],
        weight=1.0,
        description="Well status inquiries, operational state, spud/completion dates",
        authority=AuthorityLevel.AGENCY_GUIDANCE,
    ))

    # ── RISK_ASSESSMENT patterns ─────────────────────────────────────────
    patterns.append(DoctrinePattern(
        pattern_id="RA01",
        intent=QueryIntent.RISK_ASSESSMENT,
        keywords=["risk", "defect", "cloud on title", "outstanding interest",
                   "adverse claim", "litigation", "lis pendens", "judgment lien"],
        regex_patterns=[
            r"\brisk\s+(?:assessment|analysis|factor|score|flag)\b",
            r"\btitle\s+defect\b",
            r"\bcloud\s+on\s+title\b",
            r"\badverse\s+(?:claim|possession|interest)\b",
            r"\blis\s+pendens\b",
        ],
        weight=1.3,
        description="Risk flagging, title defects, clouds, adverse claims, liens",
        authority=AuthorityLevel.JUDICIAL,
    ))

    patterns.append(DoctrinePattern(
        pattern_id="RA02",
        intent=QueryIntent.RISK_ASSESSMENT,
        keywords=["lien", "tax lien", "mechanic lien", "judgment", "encumbrance",
                   "mortgage", "deed of trust", "foreclosure"],
        regex_patterns=[
            r"\b(?:tax|mechanic'?s?|judgment|federal)\s+lien\b",
            r"\bencumbrance\b",
            r"\bdeed\s+of\s+trust\b",
            r"\bforeclosure\b",
        ],
        weight=1.1,
        description="Liens, encumbrances, mortgages, deed of trust analysis",
        authority=AuthorityLevel.STATUTORY,
    ))

    # ── COMPARISON patterns ──────────────────────────────────────────────
    patterns.append(DoctrinePattern(
        pattern_id="CP01",
        intent=QueryIntent.COMPARISON,
        keywords=["compare", "comparison", "difference", "versus", "vs",
                   "side by side", "contrast", "before and after", "amendment"],
        regex_patterns=[
            r"\bcompar(?:e|ison|ing)\s+(?:the\s+)?(?:lease|deed|document|version)\b",
            r"\bdifferen(?:ce|t)\s+between\b",
            r"\b(?:before|old)\s+(?:vs?\.?|versus|and)\s+(?:after|new)\b",
            r"\bamendment\s+(?:changes|analysis|review)\b",
        ],
        weight=1.0,
        description="Document comparison, amendment analysis, version differencing",
        authority=AuthorityLevel.INDUSTRY_PRACTICE,
    ))

    # ── REVENUE_PROJECTION patterns ──────────────────────────────────────
    patterns.append(DoctrinePattern(
        pattern_id="RV01",
        intent=QueryIntent.REVENUE_PROJECTION,
        keywords=["revenue", "royalty payment", "income", "cash flow",
                   "payout", "net revenue", "gross revenue", "price deck",
                   "economic analysis", "rate of return"],
        regex_patterns=[
            r"\brevenue\s+(?:projection|estimate|forecast|calculation)\b",
            r"\broyalty\s+(?:payment|income|revenue)\b",
            r"\bnet\s+(?:present\s+)?value\b",
            r"\bcash\s+flow\s+(?:analysis|projection|forecast)\b",
            r"\brate\s+of\s+return\b",
            r"\bprice\s+deck\b",
        ],
        weight=1.1,
        description="Revenue and royalty income projections, economic analysis",
        authority=AuthorityLevel.INDUSTRY_PRACTICE,
        required_entities=["ACREAGE", "OPERATOR"],
    ))

    # ── DOCUMENT_REQUEST patterns ────────────────────────────────────────
    patterns.append(DoctrinePattern(
        pattern_id="DR01",
        intent=QueryIntent.DOCUMENT_REQUEST,
        keywords=["document", "instrument", "filing", "recording", "record",
                   "certified copy", "file number", "volume", "page"],
        regex_patterns=[
            r"\b(?:get|find|retrieve|show|pull)\s+(?:the\s+)?(?:document|instrument|deed|lease|filing)\b",
            r"\bvolume\s+\d+\s*,?\s*page\s+\d+\b",
            r"\bfile\s+(?:number|no\.?|#)\s*\d+\b",
            r"\binstrument\s+(?:number|no\.?|#)\s*\d+\b",
            r"\brecording\s+(?:information|data|reference)\b",
        ],
        weight=1.0,
        description="Document retrieval requests by instrument number, volume/page, file number",
        authority=AuthorityLevel.INDUSTRY_PRACTICE,
    ))

    # ── CHAIN_OF_TITLE patterns ──────────────────────────────────────────
    patterns.append(DoctrinePattern(
        pattern_id="CT01",
        intent=QueryIntent.CHAIN_OF_TITLE,
        keywords=["chain of title", "title chain", "conveyance history",
                   "link in chain", "root of title", "patent", "sovereign grant"],
        regex_patterns=[
            r"\bchain\s+of\s+title\b",
            r"\btitle\s+chain\b",
            r"\bconveyance\s+history\b",
            r"\broot\s+of\s+title\b",
            r"\bsovereign\s+(?:grant|patent)\b",
        ],
        weight=1.2,
        description="Full chain of title analysis from sovereign to present",
        authority=AuthorityLevel.JUDICIAL,
    ))

    # ── RIGHT_OF_WAY patterns ────────────────────────────────────────────
    patterns.append(DoctrinePattern(
        pattern_id="RW01",
        intent=QueryIntent.RIGHT_OF_WAY,
        keywords=["right of way", "easement", "pipeline", "road", "access",
                   "surface use", "accommodation", "surface damage", "ingress",
                   "egress", "utility easement", "pipeline easement"],
        regex_patterns=[
            r"\bright[\s-]?of[\s-]?way\b",
            r"\b(?:pipeline|road|utility|access)\s+easement\b",
            r"\bsurface\s+(?:use|damage|access|owner)\b",
            r"\baccommodation\s+doctrine\b",
            r"\bingress\s+(?:and\s+)?egress\b",
        ],
        weight=1.1,
        description="Right-of-way, easement, surface use, accommodation doctrine queries",
        authority=AuthorityLevel.JUDICIAL,
    ))

    # ── WATER_RIGHTS patterns ────────────────────────────────────────────
    patterns.append(DoctrinePattern(
        pattern_id="WR01",
        intent=QueryIntent.WATER_RIGHTS,
        keywords=["water rights", "water well", "groundwater", "surface water",
                   "water district", "aquifer", "water permit", "produced water",
                   "disposal water", "recycled water"],
        regex_patterns=[
            r"\bwater\s+(?:right|permit|well|source|disposal|recycl)\b",
            r"\bgroundwater\s+(?:conservation|district|permit)\b",
            r"\baquifer\b",
            r"\bproduced\s+water\b",
        ],
        weight=1.0,
        description="Water rights, groundwater, produced water disposal, water district",
        authority=AuthorityLevel.STATUTORY,
    ))

    # ── GENERAL catch-all pattern ────────────────────────────────────────
    patterns.append(DoctrinePattern(
        pattern_id="GEN01",
        intent=QueryIntent.GENERAL,
        keywords=["what is", "explain", "define", "how does", "tell me about",
                   "overview", "summary", "help", "information"],
        regex_patterns=[
            r"\b(?:what\s+is|explain|define|describe)\s+(?:a|an|the)?\s+\w+",
            r"\bhow\s+does\b",
            r"\btell\s+me\s+(?:about|more)\b",
        ],
        weight=0.5,
        description="General information requests and educational queries",
        authority=AuthorityLevel.INDUSTRY_PRACTICE,
    ))

    # Additional specialized patterns for depth
    patterns.append(DoctrinePattern(
        pattern_id="TS04",
        intent=QueryIntent.TITLE_SEARCH,
        keywords=["reservation", "exception", "mineral reservation",
                   "surface reservation", "retained interest", "reserved unto"],
        regex_patterns=[
            r"\breservation\s+(?:of|in|clause)\b",
            r"\bexception\s+(?:of|to|clause)\b",
            r"\breserved?\s+(?:unto|to|by)\s+(?:the\s+)?(?:grantor|seller)\b",
        ],
        weight=1.0,
        description="Reservation/exception clause analysis in deeds",
        authority=AuthorityLevel.JUDICIAL,
    ))

    patterns.append(DoctrinePattern(
        pattern_id="MC03",
        intent=QueryIntent.MINERAL_CALC,
        keywords=["pooling", "unitization", "allocation", "tract participation",
                   "cost-free", "carried interest", "back-in"],
        regex_patterns=[
            r"\bpooling\s+(?:order|election|declaration|unit)\b",
            r"\bunitization\s+(?:agreement|order)\b",
            r"\btract\s+(?:participation|allocation)\s+factor\b",
            r"\bcost[\s-]?free\s+interest\b",
        ],
        weight=1.0,
        description="Pooling/unitization interest calculations, allocation factors",
        authority=AuthorityLevel.REGULATORY,
    ))

    patterns.append(DoctrinePattern(
        pattern_id="RA03",
        intent=QueryIntent.RISK_ASSESSMENT,
        keywords=["bankruptcy", "receivership", "insolvency", "unpaid royalty",
                   "audit", "suspense", "underpayment", "overpayment"],
        regex_patterns=[
            r"\bbankruptcy\s+(?:of|by|filing)\b",
            r"\breceivership\b",
            r"\bunpaid\s+royalt(?:y|ies)\b",
            r"\bsuspense\s+(?:account|funds|balance)\b",
        ],
        weight=1.0,
        description="Financial risk, bankruptcy, royalty suspense, audit risk",
        authority=AuthorityLevel.STATUTORY,
    ))

    patterns.append(DoctrinePattern(
        pattern_id="PD03",
        intent=QueryIntent.PRODUCTION,
        keywords=["completion", "frac", "stimulation", "lateral length", "proppant",
                   "perforation", "stage count", "formation", "zone", "pay zone"],
        regex_patterns=[
            r"\bcompletion\s+(?:design|report|data|method)\b",
            r"\bfrac\s+(?:design|job|stage|report|data)\b",
            r"\blateral\s+(?:length|section)\b",
            r"\bpay\s+zone\b",
        ],
        weight=0.9,
        description="Completion and stimulation data queries",
        authority=AuthorityLevel.AGENCY_GUIDANCE,
    ))

    patterns.append(DoctrinePattern(
        pattern_id="RV02",
        intent=QueryIntent.REVENUE_PROJECTION,
        keywords=["division order", "decimal", "pay deck", "suspense",
                   "check stub", "royalty statement", "severance tax"],
        regex_patterns=[
            r"\bdivision\s+order\b",
            r"\broyalty\s+(?:statement|check|payment)\b",
            r"\bseverance\s+tax\b",
            r"\bpay\s+deck\b",
        ],
        weight=1.0,
        description="Division orders, royalty payment, severance tax analysis",
        authority=AuthorityLevel.INDUSTRY_PRACTICE,
    ))

    return patterns


# ─────────────────────────────────────────────────────────────────────────────
# ENTITY EXTRACTION PATTERNS (compiled regex)
# ─────────────────────────────────────────────────────────────────────────────

ENTITY_PATTERNS: List[Tuple[str, re.Pattern[str], Optional[str]]] = [
    # County detection (Texas focus + common oil states)
    ("COUNTY", re.compile(
        r"\b(Reeves|Midland|Ector|Martin|Howard|Andrews|Loving|Ward|Winkler|Pecos|"
        r"Upton|Crane|Glasscock|Reagan|Crockett|Lea|Eddy|Chaves|Roosevelt|"
        r"Permian|Delaware|Val Verde|Brewster|Culberson|Jeff Davis|Presidio|"
        r"Terrell|Sutton|Schleicher|Tom Green|Irion|Sterling|Coke|Mitchell|"
        r"Scurry|Borden|Dawson|Gaines|Yoakum|Terry|Lynn|Garza|Kent|Fisher|"
        r"Nolan|Taylor|Jones|Haskell|Stonewall|Throckmorton|Young|Jack|"
        r"Stephens|Palo Pinto|Parker|Tarrant|Johnson|Hood|Somervell|Erath|"
        r"Comanche|Hamilton|Coryell|McLennan|Limestone|Robertson|Leon|"
        r"Brazos|Grimes|Washington|Burleson|Lee|Milam|Falls|Bell|"
        r"Webb|Zapata|Jim Hogg|Starr|Hidalgo|Willacy|Cameron|"
        r"Karnes|DeWitt|Gonzales|Lavaca|Jackson|Matagorda|Wharton|"
        r"Colorado|Fayette|Austin|Fort Bend|Brazoria|Galveston|"
        r"Harris|Montgomery|Liberty|Chambers|Jefferson|Orange|"
        r"Rusk|Gregg|Smith|Upshur|Wood|Henderson|Anderson|Cherokee|"
        r"Nacogdoches|Angelina|Panola|Harrison|Marion|Cass|Bowie|"
        r"Titus|Morris|Camp|Franklin|Hopkins|Delta|Lamar|Red River|"
        r"Caddo|Grady|Roosevelt_NM|Bernalillo|San Juan)\b"
        r"\s*(?:county|co\.?)?",
        re.IGNORECASE,
    ), None),

    # State detection
    ("STATE", re.compile(
        r"\b(Texas|New Mexico|Oklahoma|North Dakota|Louisiana|Pennsylvania|"
        r"West Virginia|Colorado|Wyoming|Montana|Utah|Kansas|Ohio|Arkansas|"
        r"Mississippi|Alabama|California)\b",
        re.IGNORECASE,
    ), None),

    # Section/Township/Range
    ("SECTION", re.compile(
        r"\b(?:sec(?:tion)?\.?\s*#?\s*)(\d{1,4})\b", re.IGNORECASE
    ), None),
    ("TOWNSHIP", re.compile(
        r"\b(?:twp?\.?\s*#?\s*)(\d{1,3}[NS]?)\b", re.IGNORECASE
    ), None),
    ("RANGE", re.compile(
        r"\b(?:r(?:ng|ange)?\.?\s*#?\s*)(\d{1,3}[EW]?)\b", re.IGNORECASE
    ), None),
    ("BLOCK", re.compile(
        r"\b(?:bl(?:oc)?k\.?\s*#?\s*)([A-Z0-9\-]+)\b", re.IGNORECASE
    ), None),
    ("SURVEY", re.compile(
        r"\b(?:survey\.?\s*#?\s*)([\w\-]+(?:\s+(?:survey|grant))?)\b", re.IGNORECASE
    ), None),
    ("ABSTRACT", re.compile(
        r"\b(?:a(?:bst(?:ract)?)?\.?\s*#?\s*)(\d{1,6})\b", re.IGNORECASE
    ), None),

    # API well number (XX-XXX-XXXXX or XX-XXX-XXXXX-XX-XX)
    ("API_NUMBER", re.compile(
        r"\b(\d{2}[\s\-]?\d{3}[\s\-]?\d{5}(?:[\s\-]?\d{2}){0,2})\b"
    ), None),

    # Instrument number
    ("INSTRUMENT", re.compile(
        r"\b(?:inst(?:rument)?\.?\s*(?:no\.?|number|#)\s*)([\w\-]+)\b", re.IGNORECASE
    ), None),

    # Volume/Page
    ("INSTRUMENT", re.compile(
        r"\b(?:vol(?:ume)?\.?\s*)(\d+)\s*[,/]\s*(?:pg\.?|page\.?\s*)(\d+)\b", re.IGNORECASE
    ), "vol_page"),

    # Date patterns
    ("DATE", re.compile(
        r"\b(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})\b"
    ), None),
    ("DATE", re.compile(
        r"\b((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
        r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
        r"\s+\d{1,2},?\s+\d{4})\b", re.IGNORECASE
    ), None),

    # Operator name (after keywords like "operator", "by", "from")
    ("OPERATOR", re.compile(
        r"\b(?:operator|operated\s+by|lessee|grantee)\s*:?\s+([A-Z][A-Za-z\s&.']+(?:LLC|Inc|Corp|LP|Ltd|Co|Company|Operating|Energy|Resources|Petroleum|Oil|Gas))\b"
    ), None),

    # Party names (grantor/grantee patterns)
    ("PARTY", re.compile(
        r"\b(?:grantor|grantee|lessor|lessee|assignor|assignee|mortgagor|mortgagee|"
        r"buyer|seller|trustor|trustee|beneficiary)\s*:?\s+([A-Z][A-Za-z\s.,']+)\b"
    ), None),

    # Acreage
    ("ACREAGE", re.compile(
        r"\b(\d+(?:\.\d+)?)\s*(?:acres?|ac\.?)\b", re.IGNORECASE
    ), None),

    # Well name
    ("WELL_NAME", re.compile(
        r"\b([A-Z][A-Za-z\s.']+\s+(?:Well|Unit|#)\s*(?:No\.?\s*)?[A-Z0-9\-]+(?:\s*[A-Z0-9]+)?)\b"
    ), None),
]


# ─────────────────────────────────────────────────────────────────────────────
# JURISDICTION DETECTION
# ─────────────────────────────────────────────────────────────────────────────

STATE_COUNTY_MAP: Dict[str, List[str]] = {
    "texas": [
        "reeves", "midland", "ector", "martin", "howard", "andrews", "loving",
        "ward", "winkler", "pecos", "upton", "crane", "glasscock", "reagan",
        "crockett", "val verde", "brewster", "culberson", "jeff davis", "presidio",
        "terrell", "sutton", "schleicher", "tom green", "irion", "sterling",
        "coke", "mitchell", "scurry", "borden", "dawson", "gaines", "yoakum",
        "terry", "lynn", "garza", "kent", "fisher", "nolan", "taylor", "jones",
        "webb", "zapata", "jim hogg", "starr", "hidalgo", "willacy", "cameron",
        "karnes", "dewitt", "gonzales", "lavaca", "jackson", "matagorda", "wharton",
        "harris", "montgomery", "liberty", "jefferson", "rusk", "gregg", "smith",
    ],
    "new mexico": ["lea", "eddy", "chaves", "roosevelt", "san juan"],
    "oklahoma": ["texas", "cimarron", "beaver", "harper", "woodward", "major",
                  "garfield", "blaine", "canadian", "grady", "mcclain", "carter",
                  "stephens", "comanche", "caddo"],
    "north dakota": ["williams", "mountrail", "mckenzie", "dunn", "stark", "billings"],
    "louisiana": ["caddo", "bossier", "desoto", "red river", "sabine", "natchitoches"],
    "pennsylvania": ["washington", "greene", "fayette", "westmoreland", "allegheny"],
    "west virginia": ["marshall", "wetzel", "tyler", "doddridge", "ritchie", "harrison"],
    "colorado": ["weld", "garfield", "mesa", "rio blanco", "moffat", "jackson"],
    "wyoming": ["campbell", "converse", "natrona", "fremont", "sublette", "sweetwater"],
}


def detect_jurisdiction(entities: List[ExtractedEntity], text_lower: str) -> Dict[str, Any]:
    """Detect state and county from extracted entities and text context."""
    result: Dict[str, Any] = {"state": None, "county": None, "confidence": 0.0, "source": "none"}

    counties_found = [e.value.lower() for e in entities if e.entity_type == "COUNTY"]
    states_found = [e.value.lower() for e in entities if e.entity_type == "STATE"]

    # Direct state mention
    if states_found:
        result["state"] = states_found[0].title()
        result["confidence"] = 0.9
        result["source"] = "explicit_state"

    # Direct county mention
    if counties_found:
        county = counties_found[0]
        result["county"] = county.title()
        # Try to infer state from county
        if not result["state"]:
            for state, county_list in STATE_COUNTY_MAP.items():
                if county in county_list:
                    result["state"] = state.title()
                    result["confidence"] = 0.85
                    result["source"] = "county_state_inference"
                    break
        else:
            result["confidence"] = 0.95
            result["source"] = "explicit_both"

    # Basin/region inference
    if not result["state"]:
        basin_signals = {
            "permian basin": ("Texas", 0.75),
            "delaware basin": ("Texas", 0.70),
            "midland basin": ("Texas", 0.75),
            "eagleford": ("Texas", 0.80),
            "eagle ford": ("Texas", 0.80),
            "haynesville": ("Louisiana", 0.75),
            "bakken": ("North Dakota", 0.80),
            "marcellus": ("Pennsylvania", 0.70),
            "utica": ("Ohio", 0.70),
            "barnett": ("Texas", 0.75),
            "wolfcamp": ("Texas", 0.75),
            "spraberry": ("Texas", 0.80),
            "bone spring": ("Texas", 0.75),
            "niobrara": ("Colorado", 0.70),
            "powder river": ("Wyoming", 0.75),
            "dj basin": ("Colorado", 0.70),
            "scoop": ("Oklahoma", 0.75),
            "stack": ("Oklahoma", 0.75),
            "merge": ("Oklahoma", 0.70),
            "anadarko": ("Oklahoma", 0.70),
        }
        for basin, (state, conf) in basin_signals.items():
            if basin in text_lower:
                result["state"] = state
                result["confidence"] = conf
                result["source"] = f"basin_inference:{basin}"
                break

    # RRC mention → Texas
    if not result["state"] and ("rrc" in text_lower or "railroad commission" in text_lower):
        result["state"] = "Texas"
        result["confidence"] = 0.70
        result["source"] = "regulatory_body_inference:rrc"

    return result


# ─────────────────────────────────────────────────────────────────────────────
# ENGINE ROUTING MAP
# ─────────────────────────────────────────────────────────────────────────────

ENGINE_ROUTING: Dict[QueryIntent, List[Dict[str, Any]]] = {
    QueryIntent.TITLE_SEARCH: [
        {"engine_id": "LM01", "engine_name": "Title Examination", "port": 8401, "relevance": 0.95},
        {"engine_id": "LM05", "engine_name": "Chain of Title", "port": 8405, "relevance": 0.85},
        {"engine_id": "E01", "engine_name": "Document Classifier", "port": 8601, "relevance": 0.60},
    ],
    QueryIntent.LEASE_ANALYSIS: [
        {"engine_id": "LM02", "engine_name": "Lease Analysis", "port": 8402, "relevance": 0.95},
        {"engine_id": "LM04", "engine_name": "Lease Negotiation", "port": 8404, "relevance": 0.70},
        {"engine_id": "E04", "engine_name": "Risk Flagger", "port": 8604, "relevance": 0.55},
    ],
    QueryIntent.MINERAL_CALC: [
        {"engine_id": "LM03", "engine_name": "Mineral Interest Calculator", "port": 8403, "relevance": 0.95},
        {"engine_id": "LM16", "engine_name": "Decimal Interest", "port": 8416, "relevance": 0.90},
        {"engine_id": "TX01", "engine_name": "Individual Tax", "port": 8501, "relevance": 0.50},
    ],
    QueryIntent.REGULATORY: [
        {"engine_id": "LM07", "engine_name": "Regulatory Filing", "port": 8407, "relevance": 0.95},
        {"engine_id": "R01", "engine_name": "Regulatory Compliance", "port": 8701, "relevance": 0.90},
        {"engine_id": "R03", "engine_name": "Environmental Compliance", "port": 8703, "relevance": 0.70},
    ],
    QueryIntent.PRODUCTION: [
        {"engine_id": "LM09", "engine_name": "Production Analysis", "port": 8409, "relevance": 0.95},
        {"engine_id": "LM22", "engine_name": "Decline Curve", "port": 8422, "relevance": 0.85},
        {"engine_id": "E06", "engine_name": "Report Generator", "port": 8606, "relevance": 0.50},
    ],
    QueryIntent.RISK_ASSESSMENT: [
        {"engine_id": "E04", "engine_name": "Risk Flagger", "port": 8604, "relevance": 0.95},
        {"engine_id": "LM01", "engine_name": "Title Examination", "port": 8401, "relevance": 0.75},
        {"engine_id": "E05", "engine_name": "Due Diligence Aggregator", "port": 8605, "relevance": 0.80},
    ],
    QueryIntent.COMPARISON: [
        {"engine_id": "E03", "engine_name": "Comparison Analyzer", "port": 8603, "relevance": 0.95},
        {"engine_id": "E01", "engine_name": "Document Classifier", "port": 8601, "relevance": 0.60},
    ],
    QueryIntent.REVENUE_PROJECTION: [
        {"engine_id": "LM17", "engine_name": "Revenue Distribution", "port": 8417, "relevance": 0.95},
        {"engine_id": "E04", "engine_name": "Financial Reporting", "port": 8604, "relevance": 0.70},
        {"engine_id": "TX01", "engine_name": "Individual Tax", "port": 8501, "relevance": 0.65},
    ],
    QueryIntent.DOCUMENT_REQUEST: [
        {"engine_id": "E01", "engine_name": "Document Classifier", "port": 8601, "relevance": 0.90},
        {"engine_id": "E02", "engine_name": "Summary Generator", "port": 8602, "relevance": 0.70},
    ],
    QueryIntent.CHAIN_OF_TITLE: [
        {"engine_id": "LM05", "engine_name": "Chain of Title", "port": 8405, "relevance": 0.95},
        {"engine_id": "LM01", "engine_name": "Title Examination", "port": 8401, "relevance": 0.85},
        {"engine_id": "LIE", "engine_name": "Legal Intelligence Engine", "port": 8800, "relevance": 0.60},
    ],
    QueryIntent.RIGHT_OF_WAY: [
        {"engine_id": "LM06", "engine_name": "Right of Way", "port": 8406, "relevance": 0.95},
        {"engine_id": "LM14", "engine_name": "Easement Analyzer", "port": 8414, "relevance": 0.85},
    ],
    QueryIntent.WATER_RIGHTS: [
        {"engine_id": "LM13", "engine_name": "Water Rights", "port": 8413, "relevance": 0.95},
        {"engine_id": "R03", "engine_name": "Environmental Compliance", "port": 8703, "relevance": 0.70},
    ],
    QueryIntent.GENERAL: [
        {"engine_id": "LIE", "engine_name": "Legal Intelligence Engine", "port": 8800, "relevance": 0.60},
        {"engine_id": "LMIE", "engine_name": "Landman Intelligence Engine", "port": 8801, "relevance": 0.55},
    ],
    QueryIntent.UNKNOWN: [
        {"engine_id": "LIE", "engine_name": "Legal Intelligence Engine", "port": 8800, "relevance": 0.40},
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# AUTHORITY HIERARCHY (weights for conflict resolution)
# ─────────────────────────────────────────────────────────────────────────────

AUTHORITY_WEIGHTS: Dict[AuthorityLevel, float] = {
    AuthorityLevel.STATUTORY: 1.0,
    AuthorityLevel.REGULATORY: 0.9,
    AuthorityLevel.JUDICIAL: 0.85,
    AuthorityLevel.AGENCY_GUIDANCE: 0.70,
    AuthorityLevel.INDUSTRY_PRACTICE: 0.55,
    AuthorityLevel.INTERNAL_POLICY: 0.40,
}


# ─────────────────────────────────────────────────────────────────────────────
# METRICS COLLECTOR
# ─────────────────────────────────────────────────────────────────────────────

class MetricsCollector:
    """Track latency, hit rates, error counts, intent distribution."""

    def __init__(self) -> None:
        self.total_queries: int = 0
        self.total_errors: int = 0
        self.intent_counts: Dict[str, int] = defaultdict(int)
        self.latency_samples: List[float] = []
        self.doctrine_hit_counts: Dict[str, int] = defaultdict(int)
        self.entity_type_counts: Dict[str, int] = defaultdict(int)
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.cloud_fallbacks: int = 0
        self.start_time: float = time.time()

    def record_query(self, intent: str, latency_ms: float, doctrine_hits: List[str],
                     entity_types: List[str], cache_hit: bool, cloud_fallback: bool) -> None:
        self.total_queries += 1
        self.intent_counts[intent] += 1
        self.latency_samples.append(latency_ms)
        if len(self.latency_samples) > 10_000:
            self.latency_samples = self.latency_samples[-5_000:]
        for d in doctrine_hits:
            self.doctrine_hit_counts[d] += 1
        for et in entity_types:
            self.entity_type_counts[et] += 1
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        if cloud_fallback:
            self.cloud_fallbacks += 1

    def record_error(self) -> None:
        self.total_errors += 1

    def snapshot(self) -> Dict[str, Any]:
        avg_latency = sum(self.latency_samples) / len(self.latency_samples) if self.latency_samples else 0.0
        p95_latency = sorted(self.latency_samples)[int(len(self.latency_samples) * 0.95)] if len(self.latency_samples) > 20 else avg_latency
        uptime = time.time() - self.start_time
        return {
            "total_queries": self.total_queries,
            "total_errors": self.total_errors,
            "error_rate": self.total_errors / max(1, self.total_queries),
            "avg_latency_ms": round(avg_latency, 2),
            "p95_latency_ms": round(p95_latency, 2),
            "intent_distribution": dict(self.intent_counts),
            "top_doctrine_hits": dict(sorted(self.doctrine_hit_counts.items(), key=lambda x: -x[1])[:10]),
            "entity_type_counts": dict(self.entity_type_counts),
            "cache_hit_rate": self.cache_hits / max(1, self.cache_hits + self.cache_misses),
            "cloud_fallbacks": self.cloud_fallbacks,
            "uptime_seconds": round(uptime, 1),
            "queries_per_hour": round(self.total_queries / max(1, uptime / 3600), 1),
        }


# ─────────────────────────────────────────────────────────────────────────────
# COVERAGE MAP — track triggered/missed doctrines
# ─────────────────────────────────────────────────────────────────────────────

class CoverageMap:
    """Track which doctrine patterns have been triggered, detect epistemic gaps."""

    def __init__(self) -> None:
        self.triggered: Dict[str, int] = defaultdict(int)
        self.missed_queries: List[Dict[str, Any]] = []

    def record_hit(self, pattern_id: str) -> None:
        self.triggered[pattern_id] += 1

    def record_miss(self, query: str, best_score: float) -> None:
        self.missed_queries.append({
            "query": query[:200],
            "best_score": best_score,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        if len(self.missed_queries) > 500:
            self.missed_queries = self.missed_queries[-250:]

    def snapshot(self) -> Dict[str, Any]:
        return {
            "triggered_patterns": dict(self.triggered),
            "total_triggered": sum(self.triggered.values()),
            "unique_patterns_triggered": len(self.triggered),
            "missed_queries_count": len(self.missed_queries),
            "recent_misses": self.missed_queries[-5:],
        }


# ─────────────────────────────────────────────────────────────────────────────
# DRIFT WATCHER — detect doctrine drift over time
# ─────────────────────────────────────────────────────────────────────────────

class DriftWatcher:
    """Detect changes in query patterns and intent distribution over time."""

    def __init__(self) -> None:
        self.window_size: int = 100
        self.recent_intents: List[str] = []
        self.baseline_distribution: Dict[str, float] = {}
        self.drift_alerts: List[Dict[str, Any]] = []
        self.drift_threshold: float = 0.15

    def observe(self, intent: str) -> Optional[Dict[str, Any]]:
        self.recent_intents.append(intent)
        if len(self.recent_intents) > self.window_size * 3:
            self.recent_intents = self.recent_intents[-self.window_size * 2:]

        if len(self.recent_intents) < self.window_size:
            return None

        # Compute current window distribution
        window = self.recent_intents[-self.window_size:]
        total = len(window)
        current_dist = {k: v / total for k, v in Counter(window).items()}

        # Set baseline if not established
        if not self.baseline_distribution:
            self.baseline_distribution = current_dist.copy()
            return None

        # Check for drift
        all_keys = set(self.baseline_distribution.keys()) | set(current_dist.keys())
        max_shift = 0.0
        shifted_intent = ""
        for k in all_keys:
            base_val = self.baseline_distribution.get(k, 0.0)
            curr_val = current_dist.get(k, 0.0)
            shift = abs(curr_val - base_val)
            if shift > max_shift:
                max_shift = shift
                shifted_intent = k

        if max_shift > self.drift_threshold:
            alert = {
                "type": "INTENT_DRIFT",
                "intent": shifted_intent,
                "baseline_pct": round(self.baseline_distribution.get(shifted_intent, 0.0) * 100, 1),
                "current_pct": round(current_dist.get(shifted_intent, 0.0) * 100, 1),
                "shift_pct": round(max_shift * 100, 1),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self.drift_alerts.append(alert)
            if len(self.drift_alerts) > 100:
                self.drift_alerts = self.drift_alerts[-50:]
            logger.warning("Doctrine drift detected: {}", alert)
            return alert

        return None

    def snapshot(self) -> Dict[str, Any]:
        return {
            "baseline": self.baseline_distribution,
            "recent_window_size": len(self.recent_intents),
            "alerts_count": len(self.drift_alerts),
            "recent_alerts": self.drift_alerts[-5:],
        }


# ─────────────────────────────────────────────────────────────────────────────
# LRU CACHE for fast repeat-query handling
# ─────────────────────────────────────────────────────────────────────────────

class LRUCache:
    """Least-recently-used cache with max size."""

    def __init__(self, capacity: int = LRU_CACHE_SIZE) -> None:
        self._cache: OrderedDict[str, Any] = OrderedDict()
        self._capacity = capacity

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        return None

    def put(self, key: str, value: Any) -> None:
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        while len(self._cache) > self._capacity:
            self._cache.popitem(last=False)

    def size(self) -> int:
        return len(self._cache)

    def clear(self) -> None:
        self._cache.clear()


# ─────────────────────────────────────────────────────────────────────────────
# AUDIT TRAIL
# ─────────────────────────────────────────────────────────────────────────────

class AuditTrail:
    """Append-only JSONL audit log for every query processed."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, entry: Dict[str, Any]) -> None:
        entry["_audit_ts"] = datetime.now(timezone.utc).isoformat()
        entry["_engine"] = ENGINE_ID
        try:
            with self._path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str) + "\n")
        except OSError as exc:
            logger.error("Audit trail write failed: {}", exc)


# ─────────────────────────────────────────────────────────────────────────────
# QUERY INTERPRETER CORE
# ─────────────────────────────────────────────────────────────────────────────

class QueryInterpreter:
    """Main interpretation engine — classifies intent, extracts entities,
    expands abbreviations, detects jurisdiction, scores confidence, routes
    to downstream engines, and optionally falls back to cloud LLM."""

    def __init__(self) -> None:
        self.doctrine_cache: List[DoctrinePattern] = _build_doctrine_cache()
        self.metrics = MetricsCollector()
        self.coverage = CoverageMap()
        self.drift_watcher = DriftWatcher()
        self.cache = LRUCache(LRU_CACHE_SIZE)
        self.audit = AuditTrail(AUDIT_LOG_PATH)
        self.cloud_retriever: Optional[Any] = None
        self._init_cloud_retriever()
        logger.info(
            "QueryInterpreter initialized: {} doctrine patterns, cache capacity {}",
            len(self.doctrine_cache), LRU_CACHE_SIZE,
        )

    def _init_cloud_retriever(self) -> None:
        if CognitionCloudRetriever is not None:
            try:
                self.cloud_retriever = CognitionCloudRetriever()
                logger.info("CognitionCloudRetriever connected for deep-analysis fallback")
            except Exception as exc:
                logger.warning("CognitionCloudRetriever init failed: {}", exc)
                self.cloud_retriever = None

    # ── Abbreviation expansion ───────────────────────────────────────────

    def expand_abbreviations(self, query: str) -> Tuple[str, List[QueryExpansion]]:
        """Expand known abbreviations in the query. Returns expanded text and list of expansions."""
        expansions: List[QueryExpansion] = []
        words = query.split()
        expanded_words: List[str] = []

        for word in words:
            word_lower = word.lower().strip(".,;:!?()[]")
            if word_lower in ABBREVIATION_MAP:
                expanded = ABBREVIATION_MAP[word_lower]
                expansions.append(QueryExpansion(
                    original_term=word,
                    expanded_term=expanded,
                    expansion_type="ABBREVIATION",
                ))
                expanded_words.append(expanded)
            else:
                expanded_words.append(word)

        return " ".join(expanded_words), expansions

    # ── Semantic normalization ───────────────────────────────────────────

    def normalize_semantics(self, text: str) -> Tuple[str, List[QueryExpansion]]:
        """Normalize legal terms to canonical forms."""
        expansions: List[QueryExpansion] = []
        normalized = text.lower()

        for original_term, canonical in SEMANTIC_NORMALIZATION.items():
            if original_term in normalized:
                expansions.append(QueryExpansion(
                    original_term=original_term,
                    expanded_term=canonical,
                    expansion_type="NORMALIZATION",
                ))
                normalized = normalized.replace(original_term, canonical)

        return normalized, expansions

    # ── Entity extraction ────────────────────────────────────────────────

    def extract_entities(self, text: str) -> List[ExtractedEntity]:
        """Extract structured entities from the query text."""
        entities: List[ExtractedEntity] = []
        seen: Set[Tuple[str, str]] = set()

        for entity_type, pattern, variant in ENTITY_PATTERNS:
            for match in pattern.finditer(text):
                if variant == "vol_page":
                    vol = match.group(1)
                    page = match.group(2)
                    value = f"Vol. {vol}, Pg. {page}"
                else:
                    value = match.group(1) if match.lastindex and match.lastindex >= 1 else match.group(0)

                value = value.strip().rstrip(",.")
                key = (entity_type, value.lower())
                if key in seen:
                    continue
                seen.add(key)

                entities.append(ExtractedEntity(
                    entity_type=entity_type,
                    value=value,
                    original_span=match.group(0).strip(),
                    confidence=0.90 if entity_type in ("API_NUMBER", "INSTRUMENT", "SECTION") else 0.80,
                ))

        return entities

    # ── Intent classification ────────────────────────────────────────────

    def classify_intent(self, text_lower: str, entities: List[ExtractedEntity]) -> Tuple[
        QueryIntent, List[QueryIntent], float, List[str]
    ]:
        """Score all doctrine patterns against the query and return ranked intents."""
        entity_types: Set[str] = {e.entity_type for e in entities}
        scores: Dict[QueryIntent, float] = defaultdict(float)
        hits_by_intent: Dict[QueryIntent, List[str]] = defaultdict(list)

        for pattern in self.doctrine_cache:
            score = pattern.score(text_lower, entity_types)
            if score > 0:
                scores[pattern.intent] += score * AUTHORITY_WEIGHTS.get(pattern.authority, 0.5)
                hits_by_intent[pattern.intent].append(pattern.pattern_id)
                self.coverage.record_hit(pattern.pattern_id)

        if not scores:
            self.coverage.record_miss(text_lower[:200], 0.0)
            return QueryIntent.UNKNOWN, [], 0.0, []

        sorted_intents = sorted(scores.items(), key=lambda x: -x[1])
        primary_intent = sorted_intents[0][0]
        primary_score = sorted_intents[0][1]

        # Normalize score to 0-1 range (heuristic cap)
        max_theoretical = 3.0  # practical ceiling for combined pattern scores
        confidence = min(1.0, primary_score / max_theoretical)

        # Secondary intents — those scoring at least 40% of primary
        secondary = [
            intent for intent, sc in sorted_intents[1:]
            if sc >= primary_score * 0.40
        ]

        # Collect all doctrine hit IDs for primary
        doctrine_hits = hits_by_intent.get(primary_intent, [])

        if confidence < MIN_CONFIDENCE:
            self.coverage.record_miss(text_lower[:200], confidence)
            return QueryIntent.UNKNOWN, secondary, confidence, doctrine_hits

        return primary_intent, secondary, confidence, doctrine_hits

    # ── Confidence stratification ────────────────────────────────────────

    @staticmethod
    def stratify_confidence(confidence: float, entity_count: int, jurisdiction_conf: float) -> ConfidenceLevel:
        """Map raw confidence to epistemic stratification level."""
        adjusted = confidence * 0.6 + (min(entity_count, 5) / 5) * 0.25 + jurisdiction_conf * 0.15
        if adjusted >= 0.80:
            return ConfidenceLevel.DEFENSIBLE
        elif adjusted >= 0.55:
            return ConfidenceLevel.AGGRESSIVE
        elif adjusted >= 0.35:
            return ConfidenceLevel.DISCLOSURE
        else:
            return ConfidenceLevel.HIGH_RISK

    # ── Authority chain ──────────────────────────────────────────────────

    def build_authority_chain(self, doctrine_hits: List[str]) -> List[str]:
        """Build an authority chain from the doctrine patterns that fired."""
        authorities: List[str] = []
        seen_levels: Set[str] = set()
        for pattern in self.doctrine_cache:
            if pattern.pattern_id in doctrine_hits:
                level = pattern.authority.value
                if level not in seen_levels:
                    seen_levels.add(level)
                    authorities.append(f"{level}: {pattern.description}")
        # Sort by authority weight (strongest first)
        level_order = {al.value: w for al, w in AUTHORITY_WEIGHTS.items()}
        authorities.sort(key=lambda a: -level_order.get(a.split(":")[0], 0))
        return authorities

    # ── Routing ──────────────────────────────────────────────────────────

    @staticmethod
    def get_routing(intent: QueryIntent, secondary_intents: List[QueryIntent]) -> List[RoutingRecommendation]:
        """Return downstream engine routing recommendations."""
        all_intents = [intent] + secondary_intents
        seen_engines: Set[str] = set()
        recommendations: List[RoutingRecommendation] = []

        for idx, q_intent in enumerate(all_intents):
            intent_discount = 1.0 if idx == 0 else 0.6
            routes = ENGINE_ROUTING.get(q_intent, [])
            for route in routes:
                eid = route["engine_id"]
                if eid in seen_engines:
                    continue
                seen_engines.add(eid)
                recommendations.append(RoutingRecommendation(
                    engine_id=eid,
                    engine_name=route["engine_name"],
                    relevance_score=round(route["relevance"] * intent_discount, 3),
                    reason=f"Primary intent {q_intent.value}" if idx == 0 else f"Secondary intent {q_intent.value}",
                    port=route["port"],
                ))

        recommendations.sort(key=lambda r: -r.relevance_score)
        return recommendations[:8]

    # ── Determinism hash ─────────────────────────────────────────────────

    @staticmethod
    def compute_determinism_hash(query: str, intent: str, entities: List[Dict[str, Any]]) -> str:
        """SHA-256 determinism hash for reproducibility."""
        payload = json.dumps({
            "query": query,
            "intent": intent,
            "entities": entities,
            "engine": ENGINE_ID,
            "version": ENGINE_VERSION,
        }, sort_keys=True, default=str)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    # ── Deep analysis (cloud fallback) ───────────────────────────────────

    async def deep_analysis(self, query: str, intent: QueryIntent, entities: List[ExtractedEntity],
                            jurisdiction: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Use CognitionCloudRetriever for deeper analysis when confidence is low."""
        if self.cloud_retriever is None:
            return {"source": "unavailable", "reason": "CognitionCloudRetriever not loaded"}

        try:
            search_query = f"{intent.value}: {query}"
            category = "oil_gas" if intent in (
                QueryIntent.PRODUCTION, QueryIntent.LEASE_ANALYSIS, QueryIntent.MINERAL_CALC
            ) else "legal"

            results = await self.cloud_retriever.retrieve_all(search_query, category=category)
            self.metrics.cloud_fallbacks += 1

            if not results:
                return {"source": "cloud", "found": False, "reason": "No cloud results for this query"}

            # Package cloud results
            cloud_data: Dict[str, Any] = {
                "source": "cloud",
                "found": True,
                "result_count": len(results) if isinstance(results, list) else 1,
                "summary": str(results)[:2000] if results else "No data",
                "suggested_refinement": f"Query matched {intent.value} with cloud knowledge augmentation",
            }

            return cloud_data

        except Exception as exc:
            logger.error("Deep analysis cloud fallback failed: {}", exc)
            return {"source": "cloud", "found": False, "error": str(exc)}

    # ── Main interpret method ────────────────────────────────────────────

    async def interpret(self, request: QueryRequest) -> InterpretationResult:
        """Full query interpretation pipeline."""
        start_time = time.time()
        query_id = str(uuid.uuid4())

        # Step 1: Check cache
        cache_key = f"{request.query.lower().strip()}:{request.mode.value}:{request.zone.value}"
        cached = self.cache.get(cache_key)
        if cached is not None and not request.deep_analysis:
            cached_result: InterpretationResult = cached
            cached_result.query_id = query_id
            cached_result.latency_ms = round((time.time() - start_time) * 1000, 2)
            self.metrics.record_query(
                cached_result.primary_intent.value, cached_result.latency_ms,
                cached_result.doctrine_hits, [e.entity_type for e in cached_result.entities],
                cache_hit=True, cloud_fallback=False,
            )
            return cached_result

        # Step 2: Expand abbreviations
        expanded_query, abbrev_expansions = self.expand_abbreviations(request.query)

        # Step 3: Semantic normalization
        normalized_query, semantic_expansions = self.normalize_semantics(expanded_query)
        all_expansions = abbrev_expansions + semantic_expansions

        # Step 4: Entity extraction (on original + expanded for best coverage)
        entities = self.extract_entities(request.query)
        expanded_entities = self.extract_entities(expanded_query)
        # Merge, dedup
        seen_keys: Set[Tuple[str, str]] = {(e.entity_type, e.value.lower()) for e in entities}
        for ee in expanded_entities:
            key = (ee.entity_type, ee.value.lower())
            if key not in seen_keys:
                seen_keys.add(key)
                entities.append(ee)

        # Step 5: Intent classification
        primary_intent, secondary_intents, confidence, doctrine_hits = self.classify_intent(
            normalized_query, entities,
        )

        # Step 6: Jurisdiction detection
        jurisdiction = detect_jurisdiction(entities, normalized_query)

        # Step 7: Confidence stratification
        confidence_level = self.stratify_confidence(confidence, len(entities), jurisdiction.get("confidence", 0.0))

        # Step 8: Authority chain
        authority_chain = self.build_authority_chain(doctrine_hits)

        # Step 9: Routing
        routing: List[RoutingRecommendation] = []
        if request.include_routing:
            routing = self.get_routing(primary_intent, secondary_intents)

        # Step 10: Expansions filtering
        if not request.include_expansion:
            all_expansions = []

        # Step 11: Deep analysis (if forced or low confidence)
        deep_result: Optional[Dict[str, Any]] = None
        cloud_fallback = False
        if request.deep_analysis or (confidence < DEEP_ANALYSIS_THRESHOLD and request.mode != ResponseMode.FAST):
            deep_result = await self.deep_analysis(request.query, primary_intent, entities, jurisdiction)
            cloud_fallback = True

        # Step 12: Zone-specific adjustments
        if request.zone == AnalysisZone.AUDIT:
            # In AUDIT zone, always include full authority chain and deep analysis
            if not deep_result and self.cloud_retriever is not None:
                deep_result = await self.deep_analysis(request.query, primary_intent, entities, jurisdiction)
                cloud_fallback = True

        # Step 13: DEFENSE mode adds extra context
        if request.mode == ResponseMode.DEFENSE:
            for entity in entities:
                entity.confidence = round(entity.confidence, 4)

        # Step 14: MEMO mode triggers full documentation
        memo_extras: Optional[Dict[str, Any]] = None
        if request.mode == ResponseMode.MEMO and deep_result is None:
            memo_extras = {
                "memo_note": "Full memorandum-grade interpretation",
                "doctrine_patterns_evaluated": len(self.doctrine_cache),
                "entity_extraction_passes": 2,
                "normalization_applied": len(semantic_expansions) > 0,
                "abbreviations_expanded": len(abbrev_expansions),
                "zone": request.zone.value,
                "jurisdiction_analysis": jurisdiction,
            }
            if deep_result is None:
                deep_result = memo_extras

        # Step 15: Determinism hash
        det_hash = self.compute_determinism_hash(
            request.query, primary_intent.value,
            [{"type": e.entity_type, "value": e.value} for e in entities],
        )

        latency_ms = round((time.time() - start_time) * 1000, 2)

        result = InterpretationResult(
            query_id=query_id,
            original_query=request.query,
            normalized_query=normalized_query,
            primary_intent=primary_intent,
            secondary_intents=secondary_intents,
            confidence=round(confidence, 4),
            confidence_level=confidence_level,
            entities=entities,
            jurisdiction=jurisdiction,
            routing=routing,
            expansions=all_expansions,
            analysis_zone=request.zone,
            authority_chain=authority_chain,
            doctrine_hits=doctrine_hits,
            deep_analysis=deep_result,
            determinism_hash=det_hash,
            latency_ms=latency_ms,
            mode=request.mode,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        # Step 16: Cache the result
        self.cache.put(cache_key, result)

        # Step 17: Metrics
        self.metrics.record_query(
            primary_intent.value, latency_ms, doctrine_hits,
            [e.entity_type for e in entities],
            cache_hit=False, cloud_fallback=cloud_fallback,
        )

        # Step 18: Drift watcher
        drift_alert = self.drift_watcher.observe(primary_intent.value)
        if drift_alert:
            logger.warning("Drift alert recorded: {}", drift_alert)

        # Step 19: Audit trail
        self.audit.log({
            "query_id": query_id,
            "query": request.query[:500],
            "intent": primary_intent.value,
            "confidence": round(confidence, 4),
            "confidence_level": confidence_level.value,
            "entities_count": len(entities),
            "jurisdiction": jurisdiction.get("state"),
            "mode": request.mode.value,
            "zone": request.zone.value,
            "latency_ms": latency_ms,
            "cache_hit": False,
            "cloud_fallback": cloud_fallback,
            "doctrine_hits": doctrine_hits,
        })

        return result


# ─────────────────────────────────────────────────────────────────────────────
# FACT FRAGILITY SCORING
# ─────────────────────────────────────────────────────────────────────────────

def compute_fact_fragility(result: InterpretationResult) -> Dict[str, Any]:
    """Score the fragility of the interpretation — how likely it is to change
    with new information or recharacterization."""
    factors: Dict[str, float] = {}

    # Entity-driven stability: more entities = less fragile
    entity_factor = min(1.0, len(result.entities) / 5.0)
    factors["entity_grounding"] = round(entity_factor, 3)

    # Jurisdiction certainty
    juris_conf = result.jurisdiction.get("confidence", 0.0) if result.jurisdiction else 0.0
    factors["jurisdiction_certainty"] = round(juris_conf, 3)

    # Intent confidence
    factors["intent_confidence"] = round(result.confidence, 3)

    # Multi-intent ambiguity penalty
    ambiguity_penalty = len(result.secondary_intents) * 0.1
    factors["ambiguity_penalty"] = round(min(0.5, ambiguity_penalty), 3)

    # Doctrine coverage — more hits = more grounded
    doctrine_factor = min(1.0, len(result.doctrine_hits) / 4.0)
    factors["doctrine_coverage"] = round(doctrine_factor, 3)

    # Overall fragility: 0 = rock solid, 1 = extremely fragile
    stability = (
        entity_factor * 0.20 +
        juris_conf * 0.15 +
        result.confidence * 0.30 +
        doctrine_factor * 0.20 +
        (1.0 - ambiguity_penalty) * 0.15
    )
    fragility = round(1.0 - stability, 4)

    return {
        "fragility_score": fragility,
        "stability_score": round(stability, 4),
        "factors": factors,
        "assessment": (
            "ROCK_SOLID" if fragility < 0.20 else
            "STABLE" if fragility < 0.40 else
            "MODERATE" if fragility < 0.60 else
            "FRAGILE" if fragility < 0.80 else
            "EXTREMELY_FRAGILE"
        ),
    }


# ─────────────────────────────────────────────────────────────────────────────
# MULTI-DOCTRINE DECOMPOSITION
# ─────────────────────────────────────────────────────────────────────────────

def decompose_multi_doctrine(result: InterpretationResult) -> Dict[str, Any]:
    """Break a complex query into sub-issues by doctrine category with interaction edges."""
    categories: Dict[str, List[str]] = defaultdict(list)

    # Map doctrine hits to categories
    doctrine_category_map = {
        "TS": "TITLE",
        "LA": "LEASE",
        "MC": "MINERAL_INTEREST",
        "RG": "REGULATORY",
        "PD": "PRODUCTION",
        "RA": "RISK",
        "CP": "COMPARISON",
        "RV": "REVENUE",
        "DR": "DOCUMENT",
        "CT": "CHAIN_OF_TITLE",
        "RW": "RIGHT_OF_WAY",
        "WR": "WATER",
        "GEN": "GENERAL",
    }

    for hit_id in result.doctrine_hits:
        prefix = hit_id[:2] if len(hit_id) >= 2 else hit_id
        cat = doctrine_category_map.get(prefix, "OTHER")
        categories[cat].append(hit_id)

    # Define interaction edges between categories
    interaction_edges = []
    cat_set = set(categories.keys())
    edge_map = {
        ("TITLE", "MINERAL_INTEREST"): "Ownership affects interest calculations",
        ("TITLE", "LEASE"): "Title defects may invalidate lease",
        ("TITLE", "RISK"): "Title issues generate risk flags",
        ("LEASE", "REVENUE"): "Lease terms determine royalty rates",
        ("LEASE", "PRODUCTION"): "Lease status depends on production",
        ("MINERAL_INTEREST", "REVENUE"): "Interest decimals drive revenue splits",
        ("PRODUCTION", "REVENUE"): "Production volumes determine revenue",
        ("REGULATORY", "PRODUCTION"): "Regulatory compliance affects operations",
        ("RISK", "REVENUE"): "Risk factors discount projected revenue",
        ("CHAIN_OF_TITLE", "TITLE"): "Chain gaps create title issues",
        ("RIGHT_OF_WAY", "REGULATORY"): "ROW permits require regulatory approval",
        ("WATER", "REGULATORY"): "Water usage is heavily regulated",
    }

    for (c1, c2), reason in edge_map.items():
        if c1 in cat_set and c2 in cat_set:
            interaction_edges.append({"from": c1, "to": c2, "relationship": reason})

    return {
        "categories": dict(categories),
        "category_count": len(categories),
        "interaction_edges": interaction_edges,
        "complexity": (
            "SIMPLE" if len(categories) <= 1 else
            "MODERATE" if len(categories) <= 3 else
            "COMPLEX"
        ),
    }


# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL STATE
# ─────────────────────────────────────────────────────────────────────────────

_interpreter: Optional[QueryInterpreter] = None
_start_time: float = time.time()


def get_interpreter() -> QueryInterpreter:
    global _interpreter
    if _interpreter is None:
        _interpreter = QueryInterpreter()
    return _interpreter


# ─────────────────────────────────────────────────────────────────────────────
# FASTAPI APPLICATION
# ─────────────────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    logger.info("E07 Query Interpreter starting on port {}", ENGINE_PORT)
    get_interpreter()
    logger.info("E07 Query Interpreter ready — {} doctrine patterns loaded", len(get_interpreter().doctrine_cache))
    yield
    logger.info("E07 Query Interpreter shutting down")


app = FastAPI(
    title=f"{ENGINE_ID} — {ENGINE_NAME}",
    version=ENGINE_VERSION,
    description="Natural-language query interpreter for oil & gas land management. "
                "Classifies intent, extracts entities, expands abbreviations, detects "
                "jurisdiction, routes to downstream engines.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check() -> HealthResponse:
    """Comprehensive health check."""
    interp = get_interpreter()
    metrics = interp.metrics.snapshot()
    return HealthResponse(
        status="healthy",
        uptime_seconds=round(time.time() - _start_time, 1),
        queries_processed=metrics["total_queries"],
        cache_size=interp.cache.size(),
        cloud_retriever_available=interp.cloud_retriever is not None,
        doctrine_count=len(interp.doctrine_cache),
        intent_coverage=metrics["intent_distribution"],
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/query", response_model=QueryResponse, tags=["query"])
async def interpret_query(request: QueryRequest) -> QueryResponse:
    """Main query interpretation endpoint."""
    interp = get_interpreter()

    try:
        result = await interp.interpret(request)
        telemetry: Dict[str, Any] = {
            "latency_ms": result.latency_ms,
            "cache_hit": False,
            "doctrine_patterns_evaluated": len(interp.doctrine_cache),
            "entities_extracted": len(result.entities),
            "fragility": compute_fact_fragility(result),
            "decomposition": decompose_multi_doctrine(result),
        }

        return QueryResponse(result=result, telemetry=telemetry)

    except Exception as exc:
        interp.metrics.record_error()
        logger.error("Query interpretation failed: {}", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Interpretation error: {str(exc)}",
        )


@app.get("/metrics", tags=["telemetry"])
async def get_metrics() -> Dict[str, Any]:
    """Return engine metrics snapshot."""
    interp = get_interpreter()
    return interp.metrics.snapshot()


@app.get("/coverage", tags=["telemetry"])
async def get_coverage() -> Dict[str, Any]:
    """Return coverage map — triggered/missed doctrine patterns."""
    interp = get_interpreter()
    return interp.coverage.snapshot()


@app.get("/drift", tags=["telemetry"])
async def get_drift() -> Dict[str, Any]:
    """Return drift watcher state."""
    interp = get_interpreter()
    return interp.drift_watcher.snapshot()


@app.get("/doctrines", tags=["introspection"])
async def list_doctrines() -> Dict[str, Any]:
    """List all doctrine cache patterns."""
    interp = get_interpreter()
    patterns = []
    for p in interp.doctrine_cache:
        patterns.append({
            "pattern_id": p.pattern_id,
            "intent": p.intent.value,
            "keywords": p.keywords[:5],
            "weight": p.weight,
            "authority": p.authority.value,
            "description": p.description,
        })
    return {
        "engine_id": ENGINE_ID,
        "total_patterns": len(patterns),
        "patterns": patterns,
    }


@app.get("/intents", tags=["introspection"])
async def list_intents() -> Dict[str, Any]:
    """List all supported intents and their routing targets."""
    intent_info = []
    for intent in QueryIntent:
        routes = ENGINE_ROUTING.get(intent, [])
        intent_info.append({
            "intent": intent.value,
            "downstream_engines": [r["engine_id"] for r in routes],
            "description": next(
                (p.description for p in get_interpreter().doctrine_cache if p.intent == intent),
                "No description",
            ),
        })
    return {"intents": intent_info, "total": len(intent_info)}


@app.post("/batch", tags=["query"])
async def batch_interpret(queries: List[QueryRequest]) -> Dict[str, Any]:
    """Batch-interpret multiple queries in parallel."""
    if len(queries) > 50:
        raise HTTPException(status_code=400, detail="Max 50 queries per batch")

    interp = get_interpreter()
    start = time.time()

    tasks = [interp.interpret(q) for q in queries]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    processed: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []
    for i, res in enumerate(results):
        if isinstance(res, Exception):
            errors.append({"index": i, "error": str(res)})
        else:
            processed.append({
                "index": i,
                "query_id": res.query_id,
                "intent": res.primary_intent.value,
                "confidence": res.confidence,
                "entities_count": len(res.entities),
                "routing_count": len(res.routing),
            })

    return {
        "total": len(queries),
        "processed": len(processed),
        "errors": len(errors),
        "results": processed,
        "error_details": errors,
        "total_latency_ms": round((time.time() - start) * 1000, 2),
    }


@app.post("/expand", tags=["utility"])
async def expand_text(request: Dict[str, str]) -> Dict[str, Any]:
    """Expand abbreviations and normalize semantics in text."""
    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="text field required")

    interp = get_interpreter()
    expanded, abbr_exp = interp.expand_abbreviations(text)
    normalized, sem_exp = interp.normalize_semantics(expanded)

    return {
        "original": text,
        "expanded": expanded,
        "normalized": normalized,
        "abbreviation_expansions": [e.model_dump() for e in abbr_exp],
        "semantic_normalizations": [e.model_dump() for e in sem_exp],
    }


@app.post("/entities", tags=["utility"])
async def extract_entities_endpoint(request: Dict[str, str]) -> Dict[str, Any]:
    """Extract entities from text without full interpretation."""
    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="text field required")

    interp = get_interpreter()
    entities = interp.extract_entities(text)
    return {
        "text": text[:500],
        "entities": [e.model_dump() for e in entities],
        "total": len(entities),
    }


@app.post("/jurisdiction", tags=["utility"])
async def detect_jurisdiction_endpoint(request: Dict[str, str]) -> Dict[str, Any]:
    """Detect jurisdiction from text."""
    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="text field required")

    interp = get_interpreter()
    entities = interp.extract_entities(text)
    jurisdiction = detect_jurisdiction(entities, text.lower())
    return {"text": text[:500], "jurisdiction": jurisdiction, "entities_used": len(entities)}


@app.post("/cache/clear", tags=["admin"])
async def clear_cache() -> Dict[str, str]:
    """Clear the interpretation cache."""
    interp = get_interpreter()
    size_before = interp.cache.size()
    interp.cache.clear()
    logger.info("Cache cleared: {} entries removed", size_before)
    return {"status": "cleared", "entries_removed": str(size_before)}


# ─────────────────────────────────────────────────────────────────────────────
# ENTRYPOINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logger.add(
        ENGINE_DIR / "e07_query_interpreter.log",
        rotation="50 MB",
        retention="30 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} | {message}",
    )
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
    )
