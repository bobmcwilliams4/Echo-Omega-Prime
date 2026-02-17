"""
LM04 Mineral Interest Tracker - Main Engine
============================================

Comprehensive mineral interest tracking engine for oil & gas landman operations.

Core capabilities:
- Mineral interest ownership tracking through time
- Working Interest (WI), Royalty Interest (RI), ORRI, NPRI, MI tracking
- Decimal interest calculations with 10-place precision
- Net mineral acres (NMA) calculations
- WI to NRI conversion (working interest to net revenue interest)
- DOI (Division of Interest) title opinion integration
- Pooled interest allocation and carried interest treatment
- Back-in provisions and farmout interest tracking
- Revenue distribution and interest reconciliation
- Conveyance chain analysis (mineral deeds, royalty deeds, assignments)
- Probate and heirship tracing
- Temporal conflict detection (overlapping interests)
- Executive rights tracking and separation
- Life estate mineral interests and reversionary interests
- Texas Dormant Mineral Act compliance (5-year dormancy)
- Fractional interest normalization and reconciliation
- Interest sum validation (must equal 1.0 per tract)
- Full audit trail with SHA-256 deterministic hashing

Engine ID: LM04
Port: 8434
Mode: DET (Deterministic)
Authority: 5.0
Version: 1.0.0

Author: ECHO OMEGA PRIME Build System
Commander: Bobby Don McWilliams II
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import sqlite3
import sys
import time
import traceback
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import httpx
from fastapi import FastAPI, HTTPException, Query as QueryParam
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field, validator

# Add _shared to path for cloud retriever
APPS_SHARED_PATH = Path(__file__).resolve().parents[3] / "APPS" / "_SHARED"
if APPS_SHARED_PATH.exists():
    sys.path.insert(0, str(APPS_SHARED_PATH))


# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DoctrineBlock,
    DoctrineCategory,
    DoctrineAuthority,
    Jurisdiction,
    MineralInterestDoctrineCache,
    get_doctrine_cache,
    search_doctrines,
    get_doctrines_by_category,
    get_doctrine_stats,
)
from semantic import (
    SemanticTerm,
    MineralSemanticDictionary,
    get_semantic_dictionary,
    lookup_term,
    search_terms,
    normalize_interest_type,
    extract_interest_types_from_text,
)
from search import (
    SearchCriteria,
    SearchResult,
    SearchResponse,
    MineralInterestSearchEngine,
    get_search_engine,
    search_interests,
    search_by_owner,
    search_by_tract,
    get_tract_summary,
)
from telemetry import (
    TelemetryCollector,
    DriftWatcher,
    CoverageMap,
    MetricsCollector,
    AuditTrail,
    QueryTrace,
    QueryPhase,
    ConflictType,
    InterestOperation,
)

# Try cloud retriever import
try:
    from cloud_retriever import CloudKnowledgeRetriever
    CLOUD_RETRIEVER_AVAILABLE = True
except ImportError:
    logger.warning("CloudKnowledgeRetriever not available — cloud retrieval disabled")
    CLOUD_RETRIEVER_AVAILABLE = False


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ENGINE_ID = "LM04"
ENGINE_NAME = "Mineral Interest Tracker"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8435
ENGINE_MODE = "DET"
ENGINE_AUTHORITY = 5.0

PRECISION = 10
QUANTIZE_SPEC = Decimal("0.0000000001")
ROUNDING = ROUND_HALF_UP
UNITY = Decimal("1.0000000000")
ZERO = Decimal("0.0000000000")
TOLERANCE = Decimal("0.0000010000")
INTEREST_SUM_MAX = Decimal("1.0001000000")
INTEREST_SUM_MIN = Decimal("0.9999000000")

NMA_PRECISION = 8
NMA_QUANTIZE = Decimal("0.00000001")

ENGINE_ROOT = Path(__file__).parent
CONFIG_PATH = ENGINE_ROOT / "config.json"
DB_PATH = ENGINE_ROOT / "lm04_mineral_interests.db"
AUDIT_PATH = ENGINE_ROOT / "lm04_audit_trail.jsonl"

BANNED_PHRASES = [
    "this is not legal advice",
    "consult an attorney",
    "i am not a lawyer",
    "for informational purposes only",
]

EPISTEMIC_DISCLAIMER = (
    "DISCLOSURE: This analysis is produced by the LM04 Mineral Interest Tracker "
    "operating in DET (deterministic) mode. All decimal interest calculations "
    "use 10-place precision with ROUND_HALF_UP. Net mineral acres use 8-place precision. "
    "Results are derived from the doctrine cache and input data provided. "
    "Verify against original recorded instruments and title opinions."
)


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def convert_fraction_to_decimal(fraction_str: str) -> Decimal:
    """Convert fraction string like '1/2' to decimal."""
    if "/" not in fraction_str:
        return Decimal(fraction_str).quantize(QUANTIZE_SPEC, ROUNDING)

    parts = fraction_str.split("/")
    if len(parts) != 2:
        raise ValueError(f"Invalid fraction format: {fraction_str}")

    numerator = Decimal(parts[0].strip())
    denominator = Decimal(parts[1].strip())

    if denominator == 0:
        raise ValueError("Division by zero in fraction")

    return (numerator / denominator).quantize(QUANTIZE_SPEC, ROUNDING)


def convert_decimal_to_fraction(decimal_val: Decimal) -> str:
    """Convert decimal to fraction string (simplified)."""
    # Simple implementation for common fractions
    common_fractions = {
        Decimal("0.5"): "1/2",
        Decimal("0.25"): "1/4",
        Decimal("0.125"): "1/8",
        Decimal("0.0625"): "1/16",
        Decimal("0.333333"): "1/3",
        Decimal("0.666667"): "2/3",
    }

    for dec, frac in common_fractions.items():
        if abs(decimal_val - dec) < Decimal("0.000001"):
            return frac

    return str(decimal_val)


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class InterestType(str, Enum):
    """Types of mineral interests."""
    WI = "WI"  # Working Interest
    RI = "RI"  # Royalty Interest
    ORRI = "ORRI"  # Overriding Royalty Interest
    NPRI = "NPRI"  # Non-Participating Royalty Interest
    MI = "MI"  # Mineral Interest
    TERM_MI = "TERM_MI"  # Term Mineral Interest
    LIFE_ESTATE_MI = "LIFE_ESTATE_MI"  # Life Estate Mineral Interest
    FSD = "FSD"  # Fee Simple Determinable Minerals
    EXEC_RIGHT = "EXEC_RIGHT"  # Executive Right
    NMI = "NMI"  # Non-Executive Mineral Interest


class ConveyanceType(str, Enum):
    """Types of conveyances."""
    MINERAL_DEED = "mineral_deed"
    ROYALTY_DEED = "royalty_deed"
    ASSIGNMENT = "assignment"
    PROBATE_ORDER = "probate_order"
    HEIRSHIP_AFFIDAVIT = "heirship_affidavit"
    PARTITION_DEED = "partition_deed"
    QUITCLAIM_DEED = "quitclaim_deed"
    WARRANTY_DEED = "warranty_deed"
    SPECIAL_WARRANTY_DEED = "special_warranty_deed"
    GIFT_DEED = "gift_deed"
    TRUST_TRANSFER = "trust_transfer"
    COURT_ORDER = "court_order"
    TAX_SALE = "tax_sale"
    FORECLOSURE = "foreclosure"
    MERGER = "merger"
    CORRECTION_DEED = "correction_deed"
    RESERVATION = "reservation"


class ResponseMode(str, Enum):
    """Response modes for queries."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class MineralOwner:
    """Represents a mineral interest owner."""
    owner_id: str
    owner_name: str
    interest_type: InterestType
    decimal_interest: Decimal
    net_mineral_acres: Decimal
    tract_id: str
    effective_date: date
    expiration_date: Optional[date] = None
    executive_rights: bool = False
    bears_costs: bool = False
    receives_revenue: bool = True
    vesting_instrument: Optional[str] = None
    recording_info: Optional[str] = None
    conveyance_chain: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)


@dataclass
class Tract:
    """Represents a tract of land."""
    tract_id: str
    legal_description: str
    county: str
    state: str = "TX"
    gross_acres: Decimal = Decimal("0")
    net_acres: Decimal = Decimal("0")
    section: Optional[str] = None
    township: Optional[str] = None
    range: Optional[str] = None
    abstract: Optional[str] = None
    survey: Optional[str] = None
    owners: List[MineralOwner] = field(default_factory=list)


@dataclass
class Conveyance:
    """Represents a conveyance of mineral interests."""
    conveyance_id: str
    conveyance_type: ConveyanceType
    grantor: str
    grantee: str
    interest_conveyed: Decimal
    interest_type: InterestType
    tract_id: str
    effective_date: date
    recording_date: Optional[date] = None
    instrument_number: Optional[str] = None
    book_page: Optional[str] = None
    consideration: Optional[str] = None
    legal_description: Optional[str] = None
    executive_rights_included: bool = False
    subject_to_leases: bool = True


@dataclass
class InterestCalculation:
    """Result of an interest calculation."""
    calculation_id: str
    operation: InterestOperation
    inputs: Dict[str, Any]
    result: Decimal
    net_mineral_acres: Optional[Decimal] = None
    formula_used: str = ""
    calculation_steps: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ConflictReport:
    """Report of detected conflicts."""
    conflict_id: str
    conflict_type: ConflictType
    severity: str
    tract_id: str
    owners_involved: List[str]
    description: str
    detected_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    resolution_suggestions: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class QueryRequest(BaseModel):
    """Request model for mineral interest queries."""
    query: str = Field(..., min_length=10, max_length=5000)
    tract_id: Optional[str] = None
    owner_name: Optional[str] = None
    interest_type: Optional[InterestType] = None
    effective_date: Optional[str] = None
    mode: ResponseMode = ResponseMode.FAST
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    include_chain: bool = False
    include_conflicts: bool = True
    include_calculations: bool = True


class CalculationRequest(BaseModel):
    """Request for interest calculation."""
    operation: InterestOperation
    gross_acres: Optional[Decimal] = None
    mineral_interest_decimal: Optional[Decimal] = None
    royalty_fraction: Optional[str] = None
    working_interest_decimal: Optional[Decimal] = None
    net_revenue_interest_decimal: Optional[Decimal] = None
    pooled_acres: Optional[Decimal] = None
    tract_acres: Optional[Decimal] = None
    carried_interest: Optional[Decimal] = None
    revenue_amount: Optional[Decimal] = None


class ConveyanceRequest(BaseModel):
    """Request to record a conveyance."""
    grantor: str
    grantee: str
    conveyance_type: ConveyanceType
    interest_conveyed: str  # Fraction like "1/2" or decimal "0.5000000000"
    interest_type: InterestType
    tract_id: str
    effective_date: str
    recording_date: Optional[str] = None
    instrument_number: Optional[str] = None
    book_page: Optional[str] = None
    executive_rights_included: bool = False


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    engine_id: str
    version: str
    port: int
    mode: str
    authority: float
    doctrines_loaded: int
    database_connected: bool
    cloud_retriever: bool
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float


class QueryResponse(BaseModel):
    """Response model for queries."""
    trace_id: str
    query: str
    mode: str
    analysis: str
    interests_found: List[Dict[str, Any]]
    calculations: List[Dict[str, Any]]
    conflicts: List[Dict[str, Any]]
    chain_of_title: List[Dict[str, Any]]
    doctrines_matched: List[str]
    latency_ms: float
    disclosure: str
    sha256_hash: str


class MetricsResponse(BaseModel):
    """Metrics response."""
    total_queries: int
    avg_latency_ms: float
    error_rate: float
    cache_hit_rate: float
    total_interests_calculated: int
    total_chains_analyzed: int
    total_conflicts_detected: int
    conflict_rate: float
    top_interest_types: List[Tuple[str, int]]
    top_operations: List[Tuple[str, int]]
    top_conflicts: List[Tuple[str, int]]


# ---------------------------------------------------------------------------
# TIE Component 1: Three-Layer Response
# ---------------------------------------------------------------------------

class ThreeLayerResponse:
    """Three-layer response system: Doctrine Cache → Semantic → Deep Analysis."""

    def __init__(
        self,
        doctrine_cache: MineralInterestDoctrineCache,
        search_engine: MineralInterestSearchEngine,
        cloud_retriever: Optional[Any] = None,
    ) -> None:
        self._doctrine_cache = doctrine_cache
        self._search_engine = search_engine
        self._cloud_retriever = cloud_retriever

    def respond(
        self,
        query: str,
        mode: ResponseMode,
        trace: QueryTrace,
        tract_id: Optional[str] = None,
        owner_name: Optional[str] = None,
        interest_type: Optional[InterestType] = None,
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Execute three-layer response."""
        trace.enter_phase(QueryPhase.DOCTRINE_LOOKUP)

        # Layer 1: Doctrine Cache (0-200ms)
        matched_doctrine_dicts = search_doctrines(query)
        if matched_doctrine_dicts and mode == ResponseMode.FAST:
            analysis = self._synthesize_doctrines(matched_doctrine_dicts, mode)
            trace.doctrines_matched = [d["block_id"] for d in matched_doctrine_dicts]
            trace.cache_hit = True
            return analysis, matched_doctrine_dicts

        # Layer 2: Semantic Retrieval
        trace.enter_phase(QueryPhase.CLOUD_RETRIEVAL)
        cloud_results = []
        if self._cloud_retriever and tract_id:
            try:
                cloud_results = self._cloud_retriever.search(
                    query=query,
                    filters={"tract_id": tract_id} if tract_id else {},
                    limit=5,
                )
                trace.cloud_sources = [r.get("source", "") for r in cloud_results]
            except Exception as e:
                logger.error(f"Cloud retrieval error: {e}")
                trace.record_error(f"Cloud retrieval failed: {str(e)}")

        # Layer 3: Deep Analysis
        trace.enter_phase(QueryPhase.SYNTHESIS)
        analysis = self._deep_analysis(query, matched_doctrine_dicts, cloud_results, mode)
        trace.doctrines_matched = [d["block_id"] for d in matched_doctrine_dicts]
        return analysis, matched_doctrine_dicts

    def _synthesize_doctrines(self, doctrines: List[Dict[str, Any]], mode: ResponseMode) -> str:
        """Synthesize doctrine blocks into analysis."""
        if not doctrines:
            return "No applicable doctrines found in cache."

        lines = []
        for doc in doctrines[:5]:  # Top 5 most relevant
            lines.append(f"**{doc['title']}** ({doc['authority']})")
            lines.append(doc['content'])
            if doc.get('key_principles'):
                lines.append("Key Principles:")
                for principle in doc['key_principles'][:3]:
                    lines.append(f"  - {principle}")
            lines.append("")

        return "\n".join(lines)

    def _deep_analysis(
        self,
        query: str,
        doctrines: List[Dict[str, Any]],
        cloud_results: List[Dict[str, Any]],
        mode: ResponseMode,
    ) -> str:
        """Perform deep analysis combining all sources."""
        lines = []

        if doctrines:
            lines.append("## DOCTRINE ANALYSIS")
            lines.append(self._synthesize_doctrines(doctrines, mode))

        if cloud_results:
            lines.append("## RECORDED INSTRUMENTS")
            for result in cloud_results[:3]:
                lines.append(f"- {result.get('instrument_type', 'Unknown')}: {result.get('description', '')}")

        if not doctrines and not cloud_results:
            lines.append("No doctrine matches or cloud results found. ")
            lines.append("This query may require manual title examination.")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# TIE Component 2: Response Modes
# ---------------------------------------------------------------------------

def apply_response_mode(analysis: str, mode: ResponseMode) -> str:
    """Apply response mode formatting."""
    if mode == ResponseMode.FAST:
        return analysis[:2000]  # Truncate for speed
    elif mode == ResponseMode.DEFENSE:
        return f"AUDIT-READY ANALYSIS:\n\n{analysis}\n\nAll calculations are deterministic and reproducible."
    elif mode == ResponseMode.MEMO:
        return f"MEMORANDUM\n\nFROM: LM04 Mineral Interest Tracker\nRE: Mineral Interest Analysis\n\n{analysis}"
    return analysis


# ---------------------------------------------------------------------------
# TIE Component 4: Authority Hardening
# ---------------------------------------------------------------------------

AUTHORITY_WEIGHTS = {
    DoctrineAuthority.CONSTITUTIONAL: 10.0,
    DoctrineAuthority.STATUTORY: 8.0,
    DoctrineAuthority.CASE_LAW_SUPREME: 7.0,
    DoctrineAuthority.CASE_LAW_APPELLATE: 6.0,
    DoctrineAuthority.REGULATORY: 5.0,
    DoctrineAuthority.TREATISE: 3.0,
    DoctrineAuthority.PRACTICE_GUIDE: 2.0,
    DoctrineAuthority.INDUSTRY_STANDARD: 1.0,
}


def rank_doctrines_by_authority(doctrines: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Rank doctrines by authority level."""
    return sorted(doctrines, key=lambda d: AUTHORITY_WEIGHTS.get(DoctrineAuthority(d["authority"]), 0), reverse=True)


# ---------------------------------------------------------------------------
# TIE Component 5: Confidence Stratification
# ---------------------------------------------------------------------------

class ConfidenceLevel(str, Enum):
    """Confidence levels for mineral interest determinations."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


def stratify_confidence(
    interest_sum: Decimal,
    has_conflicts: bool,
    has_probate_gaps: bool,
    dormant_mineral_risk: bool,
) -> ConfidenceLevel:
    """Stratify confidence based on risk factors."""
    if has_conflicts or interest_sum > INTEREST_SUM_MAX or interest_sum < INTEREST_SUM_MIN:
        return ConfidenceLevel.HIGH_RISK
    if has_probate_gaps or dormant_mineral_risk:
        return ConfidenceLevel.DISCLOSURE
    if interest_sum > Decimal("1.0000500000") or interest_sum < Decimal("0.9999500000"):
        return ConfidenceLevel.AGGRESSIVE
    return ConfidenceLevel.DEFENSIBLE


# ---------------------------------------------------------------------------
# TIE Component 12: Health Endpoint
# ---------------------------------------------------------------------------

def create_health_response(
    start_time: float,
    telemetry: TelemetryCollector,
    db_connected: bool,
    doctrine_count: int,
) -> HealthResponse:
    """Create health check response."""
    uptime = datetime.now().timestamp() - start_time
    summary = telemetry.summary()
    return HealthResponse(
        status="healthy" if db_connected else "degraded",
        engine_id=ENGINE_ID,
        version=ENGINE_VERSION,
        port=ENGINE_PORT,
        mode=ENGINE_MODE,
        authority=ENGINE_AUTHORITY,
        doctrines_loaded=doctrine_count,
        database_connected=db_connected,
        cloud_retriever=CLOUD_RETRIEVER_AVAILABLE,
        uptime_seconds=round(uptime, 2),
        total_queries=summary["total_queries"],
        avg_latency_ms=summary["avg_latency_ms"],
    )


# ---------------------------------------------------------------------------
# TIE Component 16: Determinism Hash (SHA-256)
# ---------------------------------------------------------------------------

def compute_deterministic_hash(data: Dict[str, Any]) -> str:
    """Compute SHA-256 hash for reproducibility."""
    canonical = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Database Initialization
# ---------------------------------------------------------------------------

def init_database(db_path: Path) -> sqlite3.Connection:
    """Initialize SQLite database."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-64000")

    # Tracts table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tracts (
            tract_id TEXT PRIMARY KEY,
            legal_description TEXT NOT NULL,
            county TEXT NOT NULL,
            state TEXT DEFAULT 'TX',
            gross_acres TEXT NOT NULL,
            net_acres TEXT NOT NULL,
            section TEXT,
            township TEXT,
            range TEXT,
            abstract TEXT,
            survey TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Owners table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS owners (
            owner_id TEXT PRIMARY KEY,
            owner_name TEXT NOT NULL,
            interest_type TEXT NOT NULL,
            decimal_interest TEXT NOT NULL,
            net_mineral_acres TEXT NOT NULL,
            tract_id TEXT NOT NULL,
            effective_date TEXT NOT NULL,
            expiration_date TEXT,
            executive_rights INTEGER DEFAULT 0,
            bears_costs INTEGER DEFAULT 0,
            receives_revenue INTEGER DEFAULT 1,
            vesting_instrument TEXT,
            recording_info TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tract_id) REFERENCES tracts(tract_id)
        )
    """)

    # Conveyances table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conveyances (
            conveyance_id TEXT PRIMARY KEY,
            conveyance_type TEXT NOT NULL,
            grantor TEXT NOT NULL,
            grantee TEXT NOT NULL,
            interest_conveyed TEXT NOT NULL,
            interest_type TEXT NOT NULL,
            tract_id TEXT NOT NULL,
            effective_date TEXT NOT NULL,
            recording_date TEXT,
            instrument_number TEXT,
            book_page TEXT,
            consideration TEXT,
            legal_description TEXT,
            executive_rights_included INTEGER DEFAULT 0,
            subject_to_leases INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tract_id) REFERENCES tracts(tract_id)
        )
    """)

    # Conflicts table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conflicts (
            conflict_id TEXT PRIMARY KEY,
            conflict_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            tract_id TEXT NOT NULL,
            owners_involved TEXT NOT NULL,
            description TEXT NOT NULL,
            detected_at TEXT DEFAULT CURRENT_TIMESTAMP,
            resolution_suggestions TEXT,
            FOREIGN KEY (tract_id) REFERENCES tracts(tract_id)
        )
    """)

    # Calculations table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS calculations (
            calculation_id TEXT PRIMARY KEY,
            operation TEXT NOT NULL,
            inputs TEXT NOT NULL,
            result TEXT NOT NULL,
            net_mineral_acres TEXT,
            formula_used TEXT,
            calculation_steps TEXT,
            warnings TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    logger.info(f"Database initialized at {db_path}")
    return conn


# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="Mineral Interest Tracker for oil & gas landman operations",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
START_TIME = datetime.now().timestamp()
DOCTRINE_CACHE: Optional[MineralInterestDoctrineCache] = None
SEMANTIC_DICT: Optional[MineralSemanticDictionary] = None
DB_CONN: Optional[sqlite3.Connection] = None
TELEMETRY: TelemetryCollector = TelemetryCollector()
DRIFT_WATCHER: DriftWatcher = DriftWatcher()
COVERAGE_MAP: Optional[CoverageMap] = None
METRICS: MetricsCollector = MetricsCollector()
AUDIT_TRAIL: AuditTrail = AuditTrail(AUDIT_PATH)
SEARCH_ENGINE: Optional[MineralInterestSearchEngine] = None
CLOUD_RETRIEVER: Optional[Any] = None
THREE_LAYER: Optional[ThreeLayerResponse] = None


@app.on_event("startup")
async def startup():
    """Initialize engine on startup."""
    global DOCTRINE_CACHE, SEMANTIC_DICT, DB_CONN, COVERAGE_MAP, SEARCH_ENGINE, CLOUD_RETRIEVER, THREE_LAYER

    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")

    # Build doctrine cache
    DOCTRINE_CACHE = get_doctrine_cache()
    stats = get_doctrine_stats()
    logger.info(f"Loaded {stats['total_blocks']} doctrine blocks")

    # Initialize semantic dictionary
    SEMANTIC_DICT = get_semantic_dictionary()

    # Initialize coverage map
    all_topics = set(DOCTRINE_CACHE._blocks.keys())
    COVERAGE_MAP = CoverageMap(all_topics)

    # Initialize database
    DB_CONN = init_database(DB_PATH)

    # Initialize search engine
    SEARCH_ENGINE = get_search_engine(DB_PATH)

    # Initialize cloud retriever
    if CLOUD_RETRIEVER_AVAILABLE:
        try:
            CLOUD_RETRIEVER = CloudKnowledgeRetriever(
                r2_bucket="echo-prime-knowledge",
                index_name="landman_intelligence",
            )
            logger.info("Cloud retriever initialized")
        except Exception as e:
            logger.warning(f"Cloud retriever init failed: {e}")

    # Initialize three-layer response
    THREE_LAYER = ThreeLayerResponse(DOCTRINE_CACHE, SEARCH_ENGINE, CLOUD_RETRIEVER)

    logger.info(f"{ENGINE_NAME} ready on port {ENGINE_PORT}")


@app.on_event("shutdown")
async def shutdown():
    """Clean shutdown."""
    if DB_CONN:
        DB_CONN.close()
    logger.info(f"{ENGINE_NAME} shutdown complete")


# ---------------------------------------------------------------------------
# TIE Component 17: FastAPI Server
# ---------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse)
async def health():
    """TIE Component 12: Health endpoint."""
    stats = get_doctrine_stats()
    doctrine_count = stats["total_blocks"]
    db_connected = DB_CONN is not None
    return create_health_response(START_TIME, TELEMETRY, db_connected, doctrine_count)


@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    """Main query endpoint."""
    trace_id = str(uuid.uuid4())
    trace = TELEMETRY.start_query(req.query, req.session_id, req.mode.value, trace_id)

    try:
        trace.enter_phase(QueryPhase.VALIDATED)

        # Extract interest types from query
        interest_types = []
        for int_type in InterestType:
            if int_type.value.lower() in req.query.lower():
                interest_types.append(int_type.value)
                trace.interest_types_analyzed.append(int_type.value)

        # Three-layer response
        analysis, doctrines = THREE_LAYER.respond(
            req.query,
            req.mode,
            trace,
            req.tract_id,
            req.owner_name,
            req.interest_type,
        )

        # Apply response mode
        analysis = apply_response_mode(analysis, req.mode)

        # Search for interests
        trace.enter_phase(QueryPhase.CHAIN_ANALYSIS)
        interests_found = []
        if req.tract_id and DB_CONN:
            cursor = DB_CONN.execute(
                "SELECT * FROM owners WHERE tract_id = ?",
                (req.tract_id,)
            )
            interests_found = [dict(zip([d[0] for d in cursor.description], row)) for row in cursor.fetchall()]
            trace.interests_calculated = len(interests_found)

        # Conflict detection
        conflicts = []
        if req.include_conflicts and req.tract_id and DB_CONN:
            trace.enter_phase(QueryPhase.CONFLICT_DETECTION)
            conflict_start = time.monotonic()
            # Simple conflict detection: check if interests sum > 1.0
            cursor = DB_CONN.execute(
                "SELECT SUM(CAST(decimal_interest AS REAL)) as total FROM owners WHERE tract_id = ?",
                (req.tract_id,)
            )
            row = cursor.fetchone()
            total_interest = Decimal(str(row[0])) if row and row[0] else ZERO
            if total_interest > INTEREST_SUM_MAX:
                conflicts.append({
                    "conflict_type": "interest_sum_over",
                    "severity": "high",
                    "description": f"Total interests ({total_interest}) exceed 1.0",
                })
            conflict_latency = (time.monotonic() - conflict_start) * 1000
            METRICS.record_conflict_detection_latency(conflict_latency)
            trace.conflicts_detected = [c["conflict_type"] for c in conflicts]

        # Chain of title
        chain = []
        if req.include_chain and req.owner_name and DB_CONN:
            cursor = DB_CONN.execute(
                "SELECT * FROM conveyances WHERE grantee = ? OR grantor = ? ORDER BY effective_date",
                (req.owner_name, req.owner_name)
            )
            chain = [dict(zip([d[0] for d in cursor.description], row)) for row in cursor.fetchall()]
            trace.chains_analyzed = 1

        # Record doctrines in coverage map
        for doc in doctrines:
            COVERAGE_MAP.record_trigger(doc["block_id"])

        trace.enter_phase(QueryPhase.COMPLETE)
        TELEMETRY.record_trace(trace)
        AUDIT_TRAIL.log_query(trace)

        # Compute deterministic hash
        response_data = {
            "query": req.query,
            "mode": req.mode.value,
            "analysis": analysis,
            "interests_found": interests_found,
            "conflicts": conflicts,
            "chain": chain,
            "doctrines": [d.block_id for d in doctrines],
        }
        sha256_hash = compute_deterministic_hash(response_data)

        return QueryResponse(
            trace_id=trace_id,
            query=req.query,
            mode=req.mode.value,
            analysis=analysis,
            interests_found=interests_found,
            calculations=[],  # Populated by calculate endpoint
            conflicts=conflicts,
            chain_of_title=chain,
            doctrines_matched=[d["block_id"] for d in doctrines],
            latency_ms=trace.total_latency_ms,
            disclosure=EPISTEMIC_DISCLAIMER,
            sha256_hash=sha256_hash,
        )

    except Exception as e:
        trace.record_error(str(e))
        TELEMETRY.record_trace(trace)
        logger.error(f"Query error: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/calculate")
async def calculate(req: CalculationRequest):
    """Interest calculation endpoint."""
    calc_id = str(uuid.uuid4())
    op_start = time.monotonic()

    try:
        result = None
        steps = []

        if req.operation == InterestOperation.DECIMAL_CONVERSION:
            if req.royalty_fraction:
                result = convert_fraction_to_decimal(req.royalty_fraction)
                steps.append(f"Convert {req.royalty_fraction} to decimal: {result}")

        elif req.operation == InterestOperation.NET_ACRES_CALCULATION:
            if req.gross_acres and req.mineral_interest_decimal:
                result = (req.gross_acres * req.mineral_interest_decimal).quantize(NMA_QUANTIZE, ROUNDING)
                steps.append(f"NMA = {req.gross_acres} × {req.mineral_interest_decimal} = {result}")

        elif req.operation == InterestOperation.WI_NRI_CONVERSION:
            if req.working_interest_decimal and req.royalty_fraction:
                royalty_decimal = convert_fraction_to_decimal(req.royalty_fraction)
                result = (req.working_interest_decimal * (Decimal("1.0") - royalty_decimal)).quantize(QUANTIZE_SPEC, ROUNDING)
                steps.append(f"NRI = WI × (1 - Royalty) = {req.working_interest_decimal} × (1 - {royalty_decimal}) = {result}")

        elif req.operation == InterestOperation.POOLED_ALLOCATION:
            if req.tract_acres and req.pooled_acres and req.mineral_interest_decimal:
                allocation = (req.tract_acres / req.pooled_acres).quantize(QUANTIZE_SPEC, ROUNDING)
                result = (allocation * req.mineral_interest_decimal).quantize(QUANTIZE_SPEC, ROUNDING)
                steps.append(f"Allocation = {req.tract_acres} / {req.pooled_acres} = {allocation}")
                steps.append(f"Pooled Interest = {allocation} × {req.mineral_interest_decimal} = {result}")

        elif req.operation == InterestOperation.REVENUE_DISTRIBUTION:
            if req.revenue_amount and req.net_revenue_interest_decimal:
                result = (req.revenue_amount * req.net_revenue_interest_decimal).quantize(Decimal("0.01"), ROUNDING)
                steps.append(f"Revenue = {req.revenue_amount} × {req.net_revenue_interest_decimal} = ${result}")

        if result is None:
            raise ValueError(f"Missing required inputs for {req.operation.value}")

        op_latency = (time.monotonic() - op_start) * 1000
        METRICS.record_operation_latency(req.operation, op_latency)

        calculation = InterestCalculation(
            calculation_id=calc_id,
            operation=req.operation,
            inputs=req.dict(exclude_none=True),
            result=result,
            calculation_steps=steps,
        )

        # Store in database
        if DB_CONN:
            DB_CONN.execute(
                "INSERT INTO calculations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    calc_id,
                    req.operation.value,
                    json.dumps(calculation.inputs),
                    str(calculation.result),
                    str(calculation.net_mineral_acres) if calculation.net_mineral_acres else None,
                    calculation.formula_used,
                    json.dumps(calculation.calculation_steps),
                    json.dumps(calculation.warnings),
                    calculation.timestamp,
                ),
            )
            DB_CONN.commit()

        AUDIT_TRAIL.log_calculation(req.operation, calculation.__dict__)

        return {
            "calculation_id": calc_id,
            "operation": req.operation.value,
            "result": str(result),
            "steps": steps,
            "latency_ms": round(op_latency, 2),
        }

    except Exception as e:
        METRICS.record_calculation_error(str(e))
        logger.error(f"Calculation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/conveyance")
async def record_conveyance(req: ConveyanceRequest):
    """Record a mineral interest conveyance."""
    conv_id = str(uuid.uuid4())

    try:
        # Parse interest
        if "/" in req.interest_conveyed:
            interest_decimal = convert_fraction_to_decimal(req.interest_conveyed)
        else:
            interest_decimal = Decimal(req.interest_conveyed).quantize(QUANTIZE_SPEC, ROUNDING)

        # Parse dates
        effective_date = datetime.fromisoformat(req.effective_date).date()
        recording_date = datetime.fromisoformat(req.recording_date).date() if req.recording_date else None

        conveyance = Conveyance(
            conveyance_id=conv_id,
            conveyance_type=req.conveyance_type,
            grantor=req.grantor,
            grantee=req.grantee,
            interest_conveyed=interest_decimal,
            interest_type=req.interest_type,
            tract_id=req.tract_id,
            effective_date=effective_date,
            recording_date=recording_date,
            instrument_number=req.instrument_number,
            book_page=req.book_page,
            executive_rights_included=req.executive_rights_included,
        )

        # Store in database
        if DB_CONN:
            DB_CONN.execute(
                "INSERT INTO conveyances VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    conv_id,
                    conveyance.conveyance_type.value,
                    conveyance.grantor,
                    conveyance.grantee,
                    str(conveyance.interest_conveyed),
                    conveyance.interest_type.value,
                    conveyance.tract_id,
                    conveyance.effective_date.isoformat(),
                    conveyance.recording_date.isoformat() if conveyance.recording_date else None,
                    conveyance.instrument_number,
                    conveyance.book_page,
                    conveyance.consideration,
                    conveyance.legal_description,
                    1 if conveyance.executive_rights_included else 0,
                    1 if conveyance.subject_to_leases else 0,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            DB_CONN.commit()

        logger.info(f"Recorded conveyance {conv_id}: {req.grantor} → {req.grantee}")

        return {
            "conveyance_id": conv_id,
            "status": "recorded",
            "interest_decimal": str(interest_decimal),
        }

    except Exception as e:
        logger.error(f"Conveyance error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/metrics", response_model=MetricsResponse)
async def metrics():
    """TIE Component 11: Metrics endpoint."""
    summary = TELEMETRY.summary()
    conflict_report = TELEMETRY.conflict_report()

    return MetricsResponse(
        total_queries=summary["total_queries"],
        avg_latency_ms=summary["avg_latency_ms"],
        error_rate=summary["error_rate"],
        cache_hit_rate=summary["cache_hit_rate"],
        total_interests_calculated=summary["total_interests_calculated"],
        total_chains_analyzed=summary["total_chains_analyzed"],
        total_conflicts_detected=summary["total_conflicts_detected"],
        conflict_rate=conflict_report["conflict_rate"],
        top_interest_types=summary["top_interest_types"],
        top_operations=summary["top_operations"],
        top_conflicts=summary["top_conflicts"],
    )


@app.get("/doctrines")
async def doctrines(category: Optional[str] = None):
    """List all doctrine blocks."""
    if category:
        return {
            "category": category,
            "doctrines": get_doctrines_by_category(category),
        }
    stats = get_doctrine_stats()
    return {
        "total": stats["total_blocks"],
        "categories": list(stats["categories"].keys()),
    }


@app.get("/coverage")
async def coverage():
    """TIE Component 10: Coverage map."""
    return COVERAGE_MAP.get_coverage()


@app.get("/drift")
async def drift():
    """TIE Component 9: Drift watcher report."""
    return DRIFT_WATCHER.get_drift_report()


@app.get("/conflicts/{tract_id}")
async def get_conflicts(tract_id: str):
    """Get conflicts for a tract."""
    conflicts = []
    if DB_CONN:
        cursor = DB_CONN.execute(
            "SELECT * FROM conflicts WHERE tract_id = ?",
            (tract_id,)
        )
        conflicts = [dict(zip([d[0] for d in cursor.description], row)) for row in cursor.fetchall()]
    return {"tract_id": tract_id, "conflicts": conflicts}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Launching {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")
