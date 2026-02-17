"""
LM22 Coal/Mineral Specific Engine — Production Architecture
TIE Gold Standard landman intelligence engine for coal, hard rock, and specialty mineral operations.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert reasoning for coal/mineral
    Layer 2: Semantic Retrieval (200-700ms) - Fast RAG on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-source synthesis

Response Modes:
    FAST: Doctrine-driven, minimal citations, sub-2 seconds
    DEFENSE: Structured reasoning, audit-ready, burden analysis
    MEMO: Long-form, citation-heavy, firm documentation

Domain Coverage:
    Coal leasing (SMCRA), mining permits, broad form deeds, CBM ownership,
    split mineral estates, hardrock mining claims (1872 Mining Law),
    uranium/NRC licensing, reclamation bonding, geothermal leasing,
    lithium/rare earth, carbon sequestration pore space, helium extraction,
    aggregate/sand/gravel, limestone quarrying, severance taxes

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Port: 8522
Engine: LM22
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import asyncio
import hashlib
import json
import sys
import time
import uuid
from pathlib import Path
from loguru import logger

# Ensure _shared is in path for cloud_retriever
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

# Internal modules
from doctrines import (
    DoctrineBlock,
    ALL_DOCTRINES,
    get_all_doctrines,
    get_doctrine_by_topic,
    search_doctrines as keyword_search_doctrines,
    get_doctrine_topics,
    get_doctrine_count,
)
from semantic import (
    normalize_semantics,
    NormalizationResult,
    get_all_domains,
    get_synonym_count,
    get_canonical_count,
)
from search import (
    DoctrineSearchEngine,
    SearchResult,
    get_search_engine,
    search_doctrines as vector_search_doctrines,
    get_search_stats,
)
from telemetry import (
    get_telemetry,
    trace_query,
    complete_trace,
    log_error,
    record_doctrine_mutation,
    ErrorDomain,
    ResponseLayer,
    MutationType,
    MutationOrigin,
    TelemetryEngine,
    QueryTrace,
)

# Cloud retriever integration
try:
    from cloud_retriever import CognitionCloudRetriever, CloudKnowledge, retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
except ImportError:
    _CLOUD_AVAILABLE = False
    logger.warning("cloud_retriever not available — running without cloud knowledge")


# ==============================================================================
# CONFIGURATION
# ==============================================================================

ENGINE_ID = "LM22"
ENGINE_NAME = "Coal/Mineral Specific"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8522
ENGINE_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LM22_coal_mineral_specific")
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "lm22_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)

AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"

# Epistemic guardrails — banned phrases for professional output
BANNED_PHRASES = [
    "i think",
    "i believe",
    "in my opinion",
    "you should probably",
    "it might be",
    "i'm not sure",
    "this is not legal advice",
    "consult an attorney",
    "i would suggest",
    "it depends",
]


# ==============================================================================
# ENUMS
# ==============================================================================

class ResponseMode(str, Enum):
    """Response formatting mode."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class PositionZone(str, Enum):
    """Position zone — never blur between zones."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class ConfidenceLevel(str, Enum):
    """Confidence stratification."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class IssueCategory(str, Enum):
    """Coal/mineral issue classification categories."""
    COAL_REGULATION = "coal_regulation"
    COAL_MINING = "coal_mining"
    MINERAL_ESTATES = "mineral_estates"
    HARDROCK_MINING = "hardrock_mining"
    MINING_CLAIMS = "mining_claims"
    MINERAL_LEASING = "mineral_leasing"
    URANIUM = "uranium"
    RECLAMATION = "reclamation"
    SURFACE_RIGHTS = "surface_rights"
    GEOTHERMAL = "geothermal"
    CRITICAL_MINERALS = "critical_minerals"
    CARBON_STORAGE = "carbon_storage"
    SPECIALTY_GAS = "specialty_gas"
    CONSTRUCTION_MINERALS = "construction_minerals"
    TAXATION = "taxation"
    TRESPASS = "trespass"
    ENVIRONMENTAL = "environmental"
    SUPPORT_DOCTRINE = "support_doctrine"


# ==============================================================================
# PYDANTIC MODELS — ALL I/O
# ==============================================================================

class QueryRequest(BaseModel):
    """Incoming query request."""
    query: str = Field(..., min_length=3, max_length=5000, description="Coal/mineral domain query")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    zone: PositionZone = Field(default=PositionZone.PLANNING, description="Position zone")
    context: Optional[str] = Field(default=None, max_length=3000, description="Additional context")
    include_authorities: bool = Field(default=True, description="Include authority citations")
    include_counter_arguments: bool = Field(default=False, description="Include adversary positions")
    max_doctrines: int = Field(default=3, ge=1, le=10, description="Max doctrines to consider")
    trace_id: Optional[str] = Field(default=None, description="External trace ID for correlation")


class AuthorityReference(BaseModel):
    """A legal authority citation."""
    citation: str
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    authority_type: str = "statute"


class DoctrineResult(BaseModel):
    """A matched doctrine in the response."""
    topic: str
    confidence: str
    confidence_stratification: str
    conclusion: str
    key_factors: List[str]
    authorities: List[AuthorityReference]
    burden_holder: str
    resolution_strategy: str
    match_score: float = 0.0
    match_source: str = "cache"


class FactFragilityScore(BaseModel):
    """Fact fragility assessment."""
    verifiability: float = Field(ge=0.0, le=1.0)
    recharacterization_risk: float = Field(ge=0.0, le=1.0)
    testimony_dependence: float = Field(ge=0.0, le=1.0)
    overall_fragility: float = Field(ge=0.0, le=1.0)
    assessment: str = ""


class ZonedAnalysis(BaseModel):
    """Position-zone-specific analysis."""
    zone: str
    zone_guidance: str
    risk_factors: List[str]
    recommended_actions: List[str]


class DeepAnalysisResult(BaseModel):
    """Deep analysis layer output."""
    synthesis: str
    issue_categories: List[str]
    interaction_edges: List[Dict[str, str]]
    multi_doctrine_decomposition: List[str]
    reasoning_chain: List[str]


class QueryResponse(BaseModel):
    """Full query response."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    trace_id: str
    query: str
    mode: str
    zone: str
    timestamp: str
    response_layer: str
    total_latency_ms: float
    normalization: Dict[str, Any]
    doctrines: List[DoctrineResult]
    zoned_analysis: Optional[ZonedAnalysis] = None
    fact_fragility: Optional[FactFragilityScore] = None
    deep_analysis: Optional[DeepAnalysisResult] = None
    determinism_hash: str
    disclosure_caveat: Optional[str] = None
    counter_arguments: Optional[List[str]] = None
    cloud_knowledge: Dict[str, Any] = Field(default_factory=dict)
    cloud_citations: List[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    """Health check response."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    status: str = "healthy"
    port: int = ENGINE_PORT
    uptime_seconds: float
    doctrine_count: int
    synonym_count: int
    canonical_count: int
    domain_count: int
    search_stats: Dict[str, Any]
    telemetry_summary: Dict[str, Any]
    timestamp: str


# ==============================================================================
# METRICS COLLECTOR
# ==============================================================================

class MetricsCollector:
    """Lightweight metrics for operational awareness."""

    def __init__(self) -> None:
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0
        self._max_latencies: int = 200

    def record_query(self, latency_ms: float, doctrine_hit: bool) -> None:
        """Record a completed query."""
        now = time.time()
        self.latencies.append(latency_ms)
        if len(self.latencies) > self._max_latencies:
            self.latencies.pop(0)
        self.queries.append(now)
        cutoff = now - 3600
        self.queries = [t for t in self.queries if t > cutoff]
        if doctrine_hit:
            self.doctrine_hits += 1
        else:
            self.doctrine_misses += 1

    def record_error(self, error_msg: str) -> None:
        """Record an error."""
        self.errors.append(time.time())
        self.last_error = f"{datetime.now(timezone.utc).isoformat()}: {error_msg[:200]}"
        cutoff = time.time() - 86400
        self.errors = [t for t in self.errors if t > cutoff]

    def query_start(self) -> None:
        self.active_queries += 1

    def query_end(self) -> None:
        self.active_queries = max(0, self.active_queries - 1)

    def get_latency_stats(self) -> Dict[str, float]:
        if not self.latencies:
            return {"avg_ms": 0.0, "p95_ms": 0.0, "last_ms": 0.0}
        sorted_lat = sorted(self.latencies)
        p95_idx = int(len(sorted_lat) * 0.95)
        return {
            "avg_ms": round(sum(self.latencies) / len(self.latencies), 2),
            "p95_ms": round(sorted_lat[min(p95_idx, len(sorted_lat) - 1)], 2),
            "last_ms": round(self.latencies[-1], 2),
        }

    def get_error_stats(self) -> Dict[str, Any]:
        now = time.time()
        last_hour = sum(1 for t in self.errors if t > now - 3600)
        return {
            "last_hour": last_hour,
            "last_24h": len(self.errors),
            "last_error": self.last_error,
        }

    def get_doctrine_hit_rate(self) -> float:
        total = self.doctrine_hits + self.doctrine_misses
        return round(self.doctrine_hits / total, 4) if total > 0 else 0.0

    def get_queries_per_hour(self) -> float:
        now = time.time()
        last_hour = sum(1 for t in self.queries if t > now - 3600)
        return float(last_hour)


# ==============================================================================
# DOCTRINE DRIFT WATCHER
# ==============================================================================

class DoctrineDriftWatcher:
    """Detect and track doctrine drift over time."""

    def __init__(self) -> None:
        self._baseline_hashes: Dict[str, str] = {}
        self._drift_events: List[Dict[str, Any]] = []
        self._initialize_baselines()

    def _initialize_baselines(self) -> None:
        """Compute baseline hashes for all doctrine blocks."""
        for doctrine in get_all_doctrines():
            hash_input = (
                doctrine.topic
                + doctrine.conclusion_template
                + doctrine.confidence
                + doctrine.controlling_precedent
            )
            self._baseline_hashes[doctrine.topic] = hashlib.sha256(
                hash_input.encode("utf-8")
            ).hexdigest()[:16]

    def check_drift(self) -> List[Dict[str, Any]]:
        """Check all doctrines for drift from baseline."""
        drift_found: List[Dict[str, Any]] = []
        for doctrine in get_all_doctrines():
            hash_input = (
                doctrine.topic
                + doctrine.conclusion_template
                + doctrine.confidence
                + doctrine.controlling_precedent
            )
            current_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:16]
            baseline = self._baseline_hashes.get(doctrine.topic)
            if baseline and current_hash != baseline:
                event = {
                    "topic": doctrine.topic,
                    "baseline_hash": baseline,
                    "current_hash": current_hash,
                    "detected_at": datetime.now(timezone.utc).isoformat(),
                }
                drift_found.append(event)
                self._drift_events.append(event)
        return drift_found

    def get_drift_events(self) -> List[Dict[str, Any]]:
        """Return all recorded drift events."""
        return self._drift_events

    def get_baseline_count(self) -> int:
        """Return number of baselined doctrines."""
        return len(self._baseline_hashes)


# ==============================================================================
# DOCTRINE COVERAGE MAP
# ==============================================================================

class DoctrineCoverageMap:
    """Track triggered vs missed doctrines. Detect epistemic gaps."""

    def __init__(self) -> None:
        self._triggered: Dict[str, int] = {}
        self._missed: List[str] = []
        self._gap_queries: List[str] = []

    def record_hit(self, topic: str) -> None:
        """Record a doctrine cache hit."""
        self._triggered[topic] = self._triggered.get(topic, 0) + 1

    def record_miss(self, query: str) -> None:
        """Record a query that missed all doctrines."""
        self._missed.append(query)
        if len(self._missed) > 200:
            self._missed = self._missed[-100:]
        self._gap_queries.append(query)
        if len(self._gap_queries) > 100:
            self._gap_queries = self._gap_queries[-50:]

    def get_coverage_report(self) -> Dict[str, Any]:
        """Generate coverage report."""
        all_topics = set(get_doctrine_topics())
        triggered_topics = set(self._triggered.keys())
        untriggered = all_topics - triggered_topics
        total = len(all_topics)
        covered = len(triggered_topics)
        return {
            "total_doctrines": total,
            "triggered_doctrines": covered,
            "untriggered_doctrines": list(untriggered),
            "coverage_pct": round((covered / max(total, 1)) * 100, 1),
            "trigger_counts": dict(sorted(self._triggered.items(), key=lambda x: -x[1])),
            "recent_misses": self._missed[-20:],
            "epistemic_gaps": self._gap_queries[-10:],
        }


# ==============================================================================
# AUTHORITY HARDENING
# ==============================================================================

AUTHORITY_HIERARCHY: Dict[str, float] = {
    "us_supreme_court": 1.0,
    "federal_statute": 0.95,
    "federal_circuit_court": 0.9,
    "federal_regulation": 0.85,
    "state_supreme_court": 0.8,
    "state_statute": 0.75,
    "state_regulation": 0.7,
    "administrative_decision": 0.65,
    "ibla_decision": 0.6,
    "restatement": 0.55,
    "treatise": 0.5,
    "law_review": 0.4,
    "agency_guidance": 0.35,
    "industry_practice": 0.25,
}


def classify_authority(citation: str) -> tuple[str, float]:
    """Classify an authority citation and assign weight."""
    citation_lower = citation.lower()

    if "u.s." in citation_lower and any(x in citation_lower for x in ["supreme", "s. ct.", "u.s. "]):
        if any(c.isdigit() for c in citation_lower):
            return "us_supreme_court", 1.0

    if "usc" in citation_lower.replace(" ", "") or "u.s.c." in citation_lower:
        return "federal_statute", 0.95

    if any(x in citation_lower for x in ["f.2d", "f.3d", "f.4th", "f. supp"]):
        return "federal_circuit_court", 0.9

    if "cfr" in citation_lower.replace(" ", "") or "c.f.r." in citation_lower:
        return "federal_regulation", 0.85

    if any(x in citation_lower for x in ["s.w.2d", "s.w.3d", "s.e.2d", "n.w.2d", "p.2d", "p.3d", "a.2d", "a.3d", "so.2d"]):
        return "state_supreme_court", 0.8

    if any(x in citation_lower for x in ["stat.", "code", "§", "ann."]):
        return "state_statute", 0.75

    if "ibla" in citation_lower or "l.d." in citation_lower:
        return "ibla_decision", 0.6

    if "restatement" in citation_lower:
        return "restatement", 0.55

    if "pub. l." in citation_lower:
        return "federal_statute", 0.95

    if any(x in citation_lower for x in ["nureg", "secretarial order", "directive"]):
        return "agency_guidance", 0.35

    return "industry_practice", 0.25


def harden_authorities(authorities: List[str]) -> List[AuthorityReference]:
    """Convert raw authority strings to weighted AuthorityReference objects."""
    refs: List[AuthorityReference] = []
    for auth in authorities:
        auth_type, weight = classify_authority(auth)
        refs.append(AuthorityReference(citation=auth, weight=weight, authority_type=auth_type))
    refs.sort(key=lambda r: -r.weight)
    return refs


# ==============================================================================
# CONFIDENCE STRATIFICATION
# ==============================================================================

def stratify_confidence(confidence: str, zone: PositionZone) -> str:
    """Apply zone-specific confidence modification."""
    base_levels = {
        "DEFENSIBLE": 0,
        "AGGRESSIVE": 1,
        "DISCLOSURE": 2,
        "HIGH_RISK": 3,
    }
    zone_adjustments = {
        PositionZone.PLANNING: 0,
        PositionZone.REPORTING: 0,
        PositionZone.AUDIT: 1,  # Shift toward more conservative in audit
    }
    level = base_levels.get(confidence, 1) + zone_adjustments.get(zone, 0)
    level_names = ["DEFENSIBLE", "AGGRESSIVE", "DISCLOSURE", "HIGH_RISK"]
    return level_names[min(level, len(level_names) - 1)]


# ==============================================================================
# FACT FRAGILITY SCORING
# ==============================================================================

def score_fact_fragility(doctrine: DoctrineBlock, query: str) -> FactFragilityScore:
    """Score the fragility of facts underlying a doctrine application."""
    # Verifiability: How easily can the key facts be independently verified?
    authority_count = len(doctrine.primary_authority)
    verifiability = min(1.0, authority_count / 5.0)

    # Recharacterization risk: Could the facts be recharacterized by an adversary?
    risk_keywords = ["ambiguous", "unclear", "varies", "depends", "contested", "disputed"]
    rechar_hits = sum(1 for kw in risk_keywords if kw in doctrine.conclusion_template.lower())
    recharacterization_risk = min(1.0, rechar_hits * 0.25)

    # Testimony dependence: Does the position rely on witness testimony vs documentary evidence?
    testimony_keywords = ["survey", "witness", "testimony", "oral", "belief", "intent"]
    testimony_hits = sum(
        1 for kw in testimony_keywords
        if kw in doctrine.reasoning_framework.lower() or kw in query.lower()
    )
    testimony_dependence = min(1.0, testimony_hits * 0.2)

    overall = round((recharacterization_risk * 0.4 + testimony_dependence * 0.3 + (1.0 - verifiability) * 0.3), 3)

    confidence_map = {
        "DEFENSIBLE": "Low fragility — strong documentary support",
        "AGGRESSIVE": "Moderate fragility — position supportable but challengeable",
        "DISCLOSURE": "Elevated fragility — material uncertainty present",
        "HIGH_RISK": "High fragility — substantial contrary authority exists",
    }
    assessment = confidence_map.get(doctrine.confidence, "Fragility assessment unavailable")

    return FactFragilityScore(
        verifiability=round(verifiability, 3),
        recharacterization_risk=round(recharacterization_risk, 3),
        testimony_dependence=round(testimony_dependence, 3),
        overall_fragility=overall,
        assessment=assessment,
    )


# ==============================================================================
# ZONED ANALYSIS
# ==============================================================================

ZONE_GUIDANCE: Dict[PositionZone, Dict[str, Any]] = {
    PositionZone.PLANNING: {
        "guidance": (
            "Pre-transaction advisory mode. Maximize optionality. Identify all available "
            "positions and their risk profiles. Recommend structure that achieves client "
            "objectives with acceptable risk. Consider alternative extraction methods, "
            "ownership structures, and regulatory pathways."
        ),
        "risk_factors": [
            "Regulatory change risk during project development timeline",
            "Title defect risk in mineral chain of title",
            "Environmental liability exposure from historical contamination",
            "Community opposition and permitting delay risk",
            "Commodity price volatility affecting project economics",
        ],
        "actions": [
            "Conduct comprehensive title examination",
            "Obtain phase I environmental site assessment",
            "Engage regulatory counsel in all applicable jurisdictions",
            "Model project economics under multiple commodity price scenarios",
            "Identify and engage key stakeholders early",
        ],
    },
    PositionZone.REPORTING: {
        "guidance": (
            "Post-transaction compliance mode. Report what exists. Ensure accurate "
            "disclosure of mineral estate interests, production volumes, royalty calculations, "
            "and tax obligations. No aggressive positions — compliance with reporting standards."
        ),
        "risk_factors": [
            "Inaccurate production reporting triggering penalties",
            "Underpayment of royalties creating breach of lease",
            "Failure to file required regulatory reports",
            "Incorrect severance tax calculations",
            "Incomplete disclosure of environmental liabilities",
        ],
        "actions": [
            "Verify production metering accuracy",
            "Reconcile royalty calculations with lease terms",
            "File all required regulatory reports on schedule",
            "Calculate and remit severance taxes accurately",
            "Maintain complete records for audit defense",
        ],
    },
    PositionZone.AUDIT: {
        "guidance": (
            "Under examination defensive posture. Every statement must be supportable. "
            "Cite controlling authority. Acknowledge contrary positions where required. "
            "Do not volunteer information beyond what is requested. Maintain all privileges."
        ),
        "risk_factors": [
            "Examiner may recharacterize transactions",
            "Penalty exposure for positions without substantial authority",
            "Privilege waiver from inadvertent disclosure",
            "Extension of examination to related parties or periods",
            "Referral for criminal investigation in extreme cases",
        ],
        "actions": [
            "Assemble complete documentary support for every position",
            "Prepare detailed chronology of relevant events",
            "Identify and preserve all privileged communications",
            "Respond only to specific requests — do not volunteer",
            "Engage specialized mineral audit counsel",
        ],
    },
}


def perform_zoned_analysis(zone: PositionZone, doctrine: DoctrineBlock) -> ZonedAnalysis:
    """Generate zone-specific analysis for a doctrine application."""
    zone_config = ZONE_GUIDANCE.get(zone, ZONE_GUIDANCE[PositionZone.PLANNING])
    return ZonedAnalysis(
        zone=zone.value,
        zone_guidance=zone_config["guidance"],
        risk_factors=zone_config["risk_factors"],
        recommended_actions=zone_config["actions"],
    )


# ==============================================================================
# MULTI-DOCTRINE DECOMPOSITION
# ==============================================================================

# Issue interaction graph — which issues commonly co-occur
ISSUE_INTERACTION_EDGES: List[Dict[str, str]] = [
    {"from": "coal_regulation", "to": "reclamation", "relationship": "SMCRA requires reclamation for all coal mining"},
    {"from": "coal_regulation", "to": "surface_rights", "relationship": "Surface owner consent required for federal coal under non-federal surface"},
    {"from": "mineral_estates", "to": "surface_rights", "relationship": "Split estate creates surface use conflicts"},
    {"from": "mineral_estates", "to": "trespass", "relationship": "Boundary uncertainty leads to subsurface trespass"},
    {"from": "hardrock_mining", "to": "mining_claims", "relationship": "1872 Mining Law governs hardrock claims"},
    {"from": "mining_claims", "to": "mineral_leasing", "relationship": "Locatable vs leasable classification is threshold issue"},
    {"from": "coal_mining", "to": "support_doctrine", "relationship": "Underground mining triggers support obligations"},
    {"from": "coal_mining", "to": "environmental", "relationship": "Coal mining triggers acid mine drainage concerns"},
    {"from": "uranium", "to": "environmental", "relationship": "Uranium mining requires NRC environmental review"},
    {"from": "geothermal", "to": "mineral_leasing", "relationship": "Geothermal Steam Act parallels Mineral Leasing Act"},
    {"from": "critical_minerals", "to": "hardrock_mining", "relationship": "Lithium/REE are locatable hardrock minerals"},
    {"from": "carbon_storage", "to": "mineral_estates", "relationship": "Pore space ownership depends on mineral severance analysis"},
    {"from": "carbon_storage", "to": "surface_rights", "relationship": "Surface owner typically owns pore space"},
    {"from": "specialty_gas", "to": "mineral_estates", "relationship": "Helium ownership depends on deed construction"},
    {"from": "construction_minerals", "to": "surface_rights", "relationship": "Aggregate classification as surface vs mineral estate"},
    {"from": "taxation", "to": "mineral_leasing", "relationship": "Severance tax affects lease economics and valuation"},
    {"from": "reclamation", "to": "environmental", "relationship": "Reclamation standards serve environmental protection"},
    {"from": "coal_mining", "to": "taxation", "relationship": "Coal severance taxes vary by state and mining method"},
    {"from": "critical_minerals", "to": "carbon_storage", "relationship": "Lithium from geothermal brine overlaps CCS geology"},
    {"from": "support_doctrine", "to": "trespass", "relationship": "Subsidence may constitute trespass on adjacent land"},
]


def decompose_multi_doctrine(
    primary_doctrine: DoctrineBlock,
    all_results: List[SearchResult],
) -> DeepAnalysisResult:
    """Decompose a query into multi-doctrine analysis with interaction graph."""
    issue_categories = set()
    interaction_edges: List[Dict[str, str]] = []
    decomposition_steps: List[str] = []
    reasoning_chain: List[str] = []

    # Classify primary doctrine
    primary_domain = _classify_doctrine_domain(primary_doctrine)
    issue_categories.add(primary_domain)

    # Find interacting issues
    for edge in ISSUE_INTERACTION_EDGES:
        if edge["from"] == primary_domain or edge["to"] == primary_domain:
            interaction_edges.append(edge)
            other = edge["to"] if edge["from"] == primary_domain else edge["from"]
            issue_categories.add(other)

    # Build decomposition
    decomposition_steps.append(
        f"Primary issue: {primary_doctrine.topic} (domain: {primary_domain})"
    )
    for edge in interaction_edges:
        decomposition_steps.append(
            f"Connected issue: {edge['from']} → {edge['to']}: {edge['relationship']}"
        )

    # Build reasoning chain
    reasoning_chain.append(f"1. Identify primary doctrine: {primary_doctrine.topic}")
    reasoning_chain.append(f"2. Assess confidence level: {primary_doctrine.confidence}")
    reasoning_chain.append(f"3. Evaluate controlling precedent: {primary_doctrine.controlling_precedent}")
    reasoning_chain.append(f"4. Check burden of proof: {primary_doctrine.burden_holder}")

    if len(all_results) > 1:
        reasoning_chain.append(
            f"5. Consider {len(all_results) - 1} related doctrine(s) for multi-doctrine analysis"
        )
        for idx, result in enumerate(all_results[1:], start=1):
            reasoning_chain.append(
                f"   5.{idx}. {result.doctrine.topic} (score={result.relevance_score})"
            )

    reasoning_chain.append(f"6. Apply position zone constraints")
    reasoning_chain.append(f"7. Score fact fragility")
    reasoning_chain.append(f"8. Generate determinism hash for reproducibility")

    # Synthesis
    synthesis_parts = [
        f"This query engages {len(issue_categories)} issue categories across the coal/mineral domain.",
        f"The primary doctrine ({primary_doctrine.topic}) is supported by {len(primary_doctrine.primary_authority)} authorities.",
        f"Confidence level: {primary_doctrine.confidence}.",
    ]
    if interaction_edges:
        synthesis_parts.append(
            f"{len(interaction_edges)} interaction edges connect this issue to related doctrines."
        )
    synthesis = " ".join(synthesis_parts)

    return DeepAnalysisResult(
        synthesis=synthesis,
        issue_categories=sorted(issue_categories),
        interaction_edges=interaction_edges,
        multi_doctrine_decomposition=decomposition_steps,
        reasoning_chain=reasoning_chain,
    )


def _classify_doctrine_domain(doctrine: DoctrineBlock) -> str:
    """Classify a doctrine into an issue category."""
    topic = doctrine.topic.lower()
    domain_map = {
        "smcra": "coal_regulation",
        "primacy": "coal_regulation",
        "broad_form": "mineral_estates",
        "cbm": "mineral_estates",
        "coal_bed": "mineral_estates",
        "general_mining": "hardrock_mining",
        "lode": "mining_claims",
        "placer": "mining_claims",
        "split_mineral": "mineral_estates",
        "trespass": "trespass",
        "lateral": "support_doctrine",
        "subjacent": "support_doctrine",
        "uranium": "uranium",
        "reclamation": "reclamation",
        "bonding": "reclamation",
        "surface_owner": "surface_rights",
        "geothermal": "geothermal",
        "lithium": "critical_minerals",
        "rare_earth": "critical_minerals",
        "carbon": "carbon_storage",
        "pore_space": "carbon_storage",
        "helium": "specialty_gas",
        "aggregate": "construction_minerals",
        "limestone": "construction_minerals",
        "severance_tax": "taxation",
        "assessment": "mining_claims",
        "maintenance": "mining_claims",
        "patent": "mining_claims",
        "mining_lease": "mineral_leasing",
    }
    for key, domain in domain_map.items():
        if key in topic:
            return domain
    return "coal_regulation"


# ==============================================================================
# EPISTEMIC GUARDRAILS
# ==============================================================================

def apply_epistemic_guardrails(text: str) -> str:
    """Remove banned hedging phrases from professional output."""
    result = text
    for phrase in BANNED_PHRASES:
        # Case-insensitive replacement
        lower = result.lower()
        idx = lower.find(phrase)
        while idx != -1:
            result = result[:idx] + result[idx + len(phrase):]
            lower = result.lower()
            idx = lower.find(phrase)
    # Clean up double spaces
    while "  " in result:
        result = result.replace("  ", " ")
    return result.strip()


def generate_disclosure_caveat(confidence: str, zone: PositionZone) -> Optional[str]:
    """Generate disclosure caveat if required by confidence level and zone."""
    if confidence in ("DISCLOSURE", "HIGH_RISK"):
        if zone == PositionZone.AUDIT:
            return (
                "DISCLOSURE: This position involves material uncertainty. Substantial authority "
                "exists both for and against this position. Formal disclosure may be required "
                "under applicable reporting standards. Consult specialized mineral counsel before "
                "asserting this position in an audit context."
            )
        return (
            "NOTE: This analysis involves areas of legal uncertainty. The applicable authorities "
            "do not provide a clear resolution. The position taken should be documented with "
            "supporting rationale, and the client should be advised of the risk of adverse "
            "determination."
        )
    return None


# ==============================================================================
# DETERMINISM HASH
# ==============================================================================

def compute_determinism_hash(query: str, mode: str, zone: str, doctrines_used: List[str]) -> str:
    """Compute SHA-256 determinism hash for response reproducibility."""
    hash_input = json.dumps({
        "engine": ENGINE_ID,
        "version": ENGINE_VERSION,
        "query": query,
        "mode": mode,
        "zone": zone,
        "doctrines": sorted(doctrines_used),
    }, sort_keys=True)
    return hashlib.sha256(hash_input.encode("utf-8")).hexdigest()


# ==============================================================================
# THREE-LAYER RESPONSE ENGINE
# ==============================================================================

class CoalMineralEngine:
    """
    Main three-layer response engine for coal/mineral domain queries.
    Layer 1: Doctrine Cache (0-200ms)
    Layer 2: Semantic Retrieval (200-700ms)
    Layer 3: Deep Analysis (on-demand)
    """

    def __init__(self) -> None:
        self._doctrines = get_all_doctrines()
        self._keyword_index: Dict[str, List[DoctrineBlock]] = {}
        self._metrics = MetricsCollector()
        self._drift_watcher = DoctrineDriftWatcher()
        self._coverage_map = DoctrineCoverageMap()
        self._search_engine = get_search_engine()
        self._telemetry = get_telemetry()
        self._start_time = time.time()
        self._build_keyword_index()
        logger.info(
            f"CoalMineralEngine initialized: {len(self._doctrines)} doctrines, "
            f"{len(self._keyword_index)} keywords indexed"
        )

    def _build_keyword_index(self) -> None:
        """Build keyword-to-doctrine index for Layer 1 cache lookups."""
        for doctrine in self._doctrines:
            for kw in doctrine.keywords:
                kw_lower = kw.lower().strip()
                if kw_lower not in self._keyword_index:
                    self._keyword_index[kw_lower] = []
                self._keyword_index[kw_lower].append(doctrine)

    # --------------------------------------------------------------------------
    # LAYER 1: DOCTRINE CACHE
    # --------------------------------------------------------------------------

    def _layer1_doctrine_cache(self, query: str, norm: NormalizationResult) -> Optional[DoctrineBlock]:
        """Layer 1: Fast doctrine cache lookup (target <200ms)."""
        query_lower = query.lower()

        # Direct topic match
        for doctrine in self._doctrines:
            if doctrine.topic == norm.canonical_form:
                logger.debug(f"L1 cache hit (topic match): {doctrine.topic}")
                return doctrine

        # Keyword match — find doctrine with most keyword hits
        best_doctrine: Optional[DoctrineBlock] = None
        best_score = 0
        for kw, doctrines in self._keyword_index.items():
            if kw in query_lower:
                for d in doctrines:
                    score = sum(1 for k in d.keywords if k.lower() in query_lower)
                    if score > best_score:
                        best_score = score
                        best_doctrine = d

        if best_doctrine and best_score >= 2:
            logger.debug(f"L1 cache hit (keyword, score={best_score}): {best_doctrine.topic}")
            return best_doctrine

        # Normalized term match
        for doctrine in self._doctrines:
            if norm.normalized_term in doctrine.topic or doctrine.topic in norm.normalized_term:
                logger.debug(f"L1 cache hit (normalized): {doctrine.topic}")
                return doctrine

        return None

    # --------------------------------------------------------------------------
    # LAYER 2: SEMANTIC RETRIEVAL
    # --------------------------------------------------------------------------

    def _layer2_semantic_retrieval(self, query: str, max_results: int = 3) -> List[SearchResult]:
        """Layer 2: Semantic search retrieval (target <700ms)."""
        results = self._search_engine.search(query, top_k=max_results, min_score=0.15)
        logger.debug(f"L2 semantic retrieval: {len(results)} results for '{query[:50]}'")
        return results

    # --------------------------------------------------------------------------
    # LAYER 3: DEEP ANALYSIS
    # --------------------------------------------------------------------------

    def _layer3_deep_analysis(
        self,
        query: str,
        primary: DoctrineBlock,
        all_results: List[SearchResult],
        zone: PositionZone,
    ) -> DeepAnalysisResult:
        """Layer 3: Deep multi-doctrine analysis."""
        analysis = decompose_multi_doctrine(primary, all_results)
        logger.debug(f"L3 deep analysis: {len(analysis.issue_categories)} categories, "
                      f"{len(analysis.interaction_edges)} edges")
        return analysis

    # --------------------------------------------------------------------------
    # MAIN QUERY HANDLER
    # --------------------------------------------------------------------------

    def process_query(self, request: QueryRequest) -> QueryResponse:
        """Process a coal/mineral domain query through the three-layer architecture."""
        start_time = time.perf_counter()
        self._metrics.query_start()

        # Start telemetry trace
        trace = self._telemetry.trace_query(request.query)

        # Cloud knowledge retrieval
        cloud_data = {}
        cloud_citations = []
        if _CLOUD_AVAILABLE:
            try:
                cloud = asyncio.run(retrieve_cloud_knowledge(request.query, category="coal_mineral"))
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
            # Step 1: Semantic normalization
            norm_span = trace.add_span("semantic_normalization")
            norm = normalize_semantics(request.query)
            norm_span.complete({"canonical": norm.canonical_form, "confidence": norm.confidence})

            # Step 2: Layer 1 — Doctrine cache
            cache_span = trace.add_span("doctrine_cache_lookup")
            cached = self._layer1_doctrine_cache(request.query, norm)
            cache_span.complete({"hit": cached is not None, "topic": cached.topic if cached else None})

            response_layer = ResponseLayer.DOCTRINE_CACHE
            primary_doctrine: Optional[DoctrineBlock] = cached
            all_search_results: List[SearchResult] = []

            if cached:
                self._coverage_map.record_hit(cached.topic)
            else:
                # Step 3: Layer 2 — Semantic retrieval
                search_span = trace.add_span("semantic_retrieval")
                all_search_results = self._layer2_semantic_retrieval(
                    request.query, max_results=request.max_doctrines
                )
                if all_search_results:
                    primary_doctrine = all_search_results[0].doctrine
                    self._coverage_map.record_hit(primary_doctrine.topic)
                    response_layer = ResponseLayer.SEMANTIC_RETRIEVAL
                else:
                    self._coverage_map.record_miss(request.query)
                search_span.complete({
                    "results": len(all_search_results),
                    "top_topic": primary_doctrine.topic if primary_doctrine else None,
                })

            # If no doctrine found at all, return error
            if primary_doctrine is None:
                elapsed = (time.perf_counter() - start_time) * 1000
                self._metrics.query_end()
                self._metrics.record_query(elapsed, False)
                log_error(ErrorDomain.DOCTRINE_LOOKUP, f"No doctrine match for: {request.query}", trace)
                complete_trace(trace, ResponseLayer.ERROR_FALLBACK, False)
                raise HTTPException(
                    status_code=404,
                    detail={
                        "error": "No matching doctrine found",
                        "query": request.query,
                        "normalized": norm.canonical_form,
                        "suggestion": "Try more specific coal/mineral terminology",
                    },
                )

            # Step 4: Apply confidence stratification
            effective_confidence = stratify_confidence(primary_doctrine.confidence, request.zone)

            # Step 5: Harden authorities
            authorities = harden_authorities(primary_doctrine.primary_authority)

            # Step 6: Build doctrine results
            doctrines_used: List[str] = [primary_doctrine.topic]
            doctrine_results: List[DoctrineResult] = [
                DoctrineResult(
                    topic=primary_doctrine.topic,
                    confidence=effective_confidence,
                    confidence_stratification=primary_doctrine.confidence_stratification,
                    conclusion=apply_epistemic_guardrails(primary_doctrine.conclusion_template),
                    key_factors=primary_doctrine.key_factors,
                    authorities=authorities if request.include_authorities else [],
                    burden_holder=primary_doctrine.burden_holder,
                    resolution_strategy=primary_doctrine.resolution_strategy,
                    match_score=1.0 if cached else (all_search_results[0].relevance_score if all_search_results else 0.0),
                    match_source="cache" if cached else "semantic",
                ),
            ]

            # Add secondary doctrines from search results
            for sr in all_search_results[1:request.max_doctrines]:
                secondary_conf = stratify_confidence(sr.doctrine.confidence, request.zone)
                secondary_auth = harden_authorities(sr.doctrine.primary_authority)
                doctrines_used.append(sr.doctrine.topic)
                doctrine_results.append(
                    DoctrineResult(
                        topic=sr.doctrine.topic,
                        confidence=secondary_conf,
                        confidence_stratification=sr.doctrine.confidence_stratification,
                        conclusion=apply_epistemic_guardrails(sr.doctrine.conclusion_template),
                        key_factors=sr.doctrine.key_factors,
                        authorities=secondary_auth if request.include_authorities else [],
                        burden_holder=sr.doctrine.burden_holder,
                        resolution_strategy=sr.doctrine.resolution_strategy,
                        match_score=sr.relevance_score,
                        match_source=sr.match_source,
                    ),
                )

            # Step 7: Zoned analysis
            zoned = perform_zoned_analysis(request.zone, primary_doctrine)

            # Step 8: Fact fragility
            fragility = score_fact_fragility(primary_doctrine, request.query)

            # Step 9: Deep analysis (MEMO mode or multiple doctrines)
            deep: Optional[DeepAnalysisResult] = None
            if request.mode == ResponseMode.MEMO or len(doctrine_results) > 1:
                analysis_span = trace.add_span("deep_analysis")
                deep = self._layer3_deep_analysis(
                    request.query, primary_doctrine, all_search_results, request.zone,
                )
                analysis_span.complete({"categories": len(deep.issue_categories)})
                if not cached:
                    response_layer = ResponseLayer.DEEP_ANALYSIS

            # Step 10: Counter arguments
            counter_args: Optional[List[str]] = None
            if request.include_counter_arguments:
                counter_args = primary_doctrine.counter_arguments

            # Step 11: Disclosure caveat
            caveat = generate_disclosure_caveat(effective_confidence, request.zone)

            # Step 12: Determinism hash
            det_hash = compute_determinism_hash(
                request.query, request.mode.value, request.zone.value, doctrines_used,
            )

            # Step 13: Build response
            elapsed = (time.perf_counter() - start_time) * 1000

            response = QueryResponse(
                trace_id=trace.trace_id,
                query=request.query,
                mode=request.mode.value,
                zone=request.zone.value,
                timestamp=datetime.now(timezone.utc).isoformat(),
                response_layer=response_layer.value,
                total_latency_ms=round(elapsed, 2),
                normalization={
                    "original": norm.original_term,
                    "normalized": norm.normalized_term,
                    "canonical": norm.canonical_form,
                    "domain": norm.domain,
                    "confidence": norm.confidence,
                },
                doctrines=doctrine_results,
                zoned_analysis=zoned,
                fact_fragility=fragility,
                deep_analysis=deep,
                determinism_hash=det_hash,
                disclosure_caveat=caveat,
                cloud_knowledge=cloud_data,
                cloud_citations=cloud_citations,
                counter_arguments=counter_args,
            )

            # Record metrics
            self._metrics.query_end()
            self._metrics.record_query(elapsed, cached is not None)

            # Complete telemetry trace
            complete_trace(
                trace,
                response_layer,
                doctrine_hit=cached is not None,
                doctrine_topic=primary_doctrine.topic,
                confidence=effective_confidence,
                response_mode=request.mode.value,
            )

            logger.info(
                f"Query processed: '{request.query[:60]}' → {primary_doctrine.topic} "
                f"({response_layer.value}, {elapsed:.1f}ms)"
            )

            return response

        except HTTPException:
            self._metrics.query_end()
            raise
        except Exception as exc:
            self._metrics.query_end()
            self._metrics.record_error(str(exc))
            log_error(ErrorDomain.UNKNOWN, str(exc), trace)
            complete_trace(trace, ResponseLayer.ERROR_FALLBACK, False)
            logger.exception(f"Query processing error: {exc}")
            raise HTTPException(status_code=500, detail={"error": str(exc)})

    # --------------------------------------------------------------------------
    # HEALTH & METRICS
    # --------------------------------------------------------------------------

    def get_health(self) -> HealthResponse:
        """Generate comprehensive health check."""
        uptime = time.time() - self._start_time
        return HealthResponse(
            status="healthy",
            port=ENGINE_PORT,
            uptime_seconds=round(uptime, 1),
            doctrine_count=get_doctrine_count(),
            synonym_count=get_synonym_count(),
            canonical_count=get_canonical_count(),
            domain_count=len(get_all_domains()),
            search_stats=get_search_stats(),
            telemetry_summary=self._telemetry.get_full_metrics(),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def get_metrics(self) -> Dict[str, Any]:
        """Return operational metrics."""
        return {
            "latency": self._metrics.get_latency_stats(),
            "errors": self._metrics.get_error_stats(),
            "doctrine_hit_rate": self._metrics.get_doctrine_hit_rate(),
            "queries_per_hour": self._metrics.get_queries_per_hour(),
            "active_queries": self._metrics.active_queries,
            "coverage": self._coverage_map.get_coverage_report(),
            "drift": {
                "baseline_count": self._drift_watcher.get_baseline_count(),
                "drift_events": len(self._drift_watcher.get_drift_events()),
            },
        }


# ==============================================================================
# FASTAPI APPLICATION
# ==============================================================================

# Global engine instance
_engine: Optional[CoalMineralEngine] = None


def get_engine() -> CoalMineralEngine:
    """Get or create the global engine instance."""
    global _engine
    if _engine is None:
        _engine = CoalMineralEngine()
    return _engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown."""
    logger.info(f"LM22 Coal/Mineral Specific Engine starting on port {ENGINE_PORT}")
    engine = get_engine()
    logger.info(
        f"Engine ready: {get_doctrine_count()} doctrines, "
        f"{get_synonym_count()} synonyms, "
        f"{get_canonical_count()} canonical forms"
    )
    yield
    logger.info("LM22 Coal/Mineral Specific Engine shutting down")
    if _CLOUD_AVAILABLE:
        try:
            from cloud_retriever import cleanup_cloud_resources
            await cleanup_cloud_resources()
            logger.info("Cloud resources cleaned up")
        except Exception as e:
            logger.warning(f"Cloud cleanup failed: {e}")


app = FastAPI(
    title=f"LM22 {ENGINE_NAME} Engine",
    description=(
        "TIE Gold Standard landman intelligence engine for coal, hard rock, and specialty "
        "mineral land operations. Covers SMCRA, broad form deeds, CBM ownership, hardrock "
        "mining claims, uranium/NRC licensing, reclamation, geothermal, lithium/rare earth, "
        "carbon sequestration pore space, helium, aggregate, and severance taxes."
    ),
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


# ==============================================================================
# API ENDPOINTS
# ==============================================================================

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Comprehensive health check endpoint."""
    engine = get_engine()
    health = engine.get_health()
    return health.model_dump()


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint — engine identity."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": str(ENGINE_PORT),
        "status": "operational",
        "doctrines": str(get_doctrine_count()),
    }


@app.post("/query")
async def query_endpoint(request: QueryRequest) -> Dict[str, Any]:
    """Main query endpoint — three-layer response architecture."""
    engine = get_engine()
    response = engine.process_query(request)
    return response.model_dump()


@app.get("/doctrines")
async def list_doctrines() -> Dict[str, Any]:
    """List all available doctrines."""
    doctrines = get_all_doctrines()
    return {
        "count": len(doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence,
                "controlling_precedent": d.controlling_precedent,
                "entity_scope": d.entity_scope,
            }
            for d in doctrines
        ],
    }


@app.get("/doctrines/{topic}")
async def get_doctrine(topic: str) -> Dict[str, Any]:
    """Get a specific doctrine by topic."""
    doctrine = get_doctrine_by_topic(topic)
    if not doctrine:
        raise HTTPException(status_code=404, detail=f"Doctrine not found: {topic}")
    return {
        "topic": doctrine.topic,
        "keywords": doctrine.keywords,
        "conclusion_template": doctrine.conclusion_template,
        "reasoning_framework": doctrine.reasoning_framework,
        "key_factors": doctrine.key_factors,
        "primary_authority": doctrine.primary_authority,
        "burden_holder": doctrine.burden_holder,
        "adversary_position": doctrine.adversary_position,
        "counter_arguments": doctrine.counter_arguments,
        "resolution_strategy": doctrine.resolution_strategy,
        "entity_scope": doctrine.entity_scope,
        "confidence": doctrine.confidence,
        "confidence_stratification": doctrine.confidence_stratification,
        "controlling_precedent": doctrine.controlling_precedent,
    }


@app.get("/search")
async def search_endpoint(q: str, top_k: int = 5) -> Dict[str, Any]:
    """Search doctrines by query."""
    results = vector_search_doctrines(q, top_k=top_k)
    return {
        "query": q,
        "results": [
            {
                "topic": r.doctrine.topic,
                "relevance_score": r.relevance_score,
                "match_source": r.match_source,
                "matched_terms": r.matched_terms,
                "confidence": r.doctrine.confidence,
            }
            for r in results
        ],
    }


@app.get("/metrics")
async def metrics_endpoint() -> Dict[str, Any]:
    """Operational metrics."""
    engine = get_engine()
    return engine.get_metrics()


@app.get("/coverage")
async def coverage_endpoint() -> Dict[str, Any]:
    """Doctrine coverage report."""
    engine = get_engine()
    return engine._coverage_map.get_coverage_report()


@app.get("/drift")
async def drift_endpoint() -> Dict[str, Any]:
    """Check for doctrine drift."""
    engine = get_engine()
    drift_events = engine._drift_watcher.check_drift()
    return {
        "baseline_count": engine._drift_watcher.get_baseline_count(),
        "drift_detected": len(drift_events) > 0,
        "drift_events": drift_events,
        "historical_events": engine._drift_watcher.get_drift_events(),
    }


@app.get("/telemetry")
async def telemetry_endpoint() -> Dict[str, Any]:
    """Full telemetry metrics."""
    telem = get_telemetry()
    return telem.get_full_metrics()


@app.get("/audit")
async def audit_endpoint(limit: int = 50) -> Dict[str, Any]:
    """Audit trail — recent query traces."""
    telem = get_telemetry()
    entries = telem.get_audit_trail(limit=limit)
    return {"count": len(entries), "entries": entries}


@app.get("/domains")
async def domains_endpoint() -> Dict[str, Any]:
    """List semantic domains."""
    return {
        "domains": get_all_domains(),
        "count": len(get_all_domains()),
    }


@app.get("/normalize")
async def normalize_endpoint(term: str) -> Dict[str, Any]:
    """Normalize a term through the semantic dictionary."""
    result = normalize_semantics(term)
    return {
        "original": result.original_term,
        "normalized": result.normalized_term,
        "canonical": result.canonical_form,
        "domain": result.domain,
        "confidence": result.confidence,
        "synonyms_matched": result.synonyms_matched,
        "context_hints": result.context_hints,
    }


@app.get("/interactions")
async def interactions_endpoint() -> Dict[str, Any]:
    """Issue interaction graph."""
    return {
        "edges": ISSUE_INTERACTION_EDGES,
        "count": len(ISSUE_INTERACTION_EDGES),
        "categories": sorted(set(
            [e["from"] for e in ISSUE_INTERACTION_EDGES]
            + [e["to"] for e in ISSUE_INTERACTION_EDGES]
        )),
    }


@app.get("/authorities")
async def authorities_endpoint() -> Dict[str, Any]:
    """Authority hierarchy weights."""
    return {
        "hierarchy": AUTHORITY_HIERARCHY,
        "levels": len(AUTHORITY_HIERARCHY),
    }


# ==============================================================================
# EXTENDED MINERAL CLASSIFICATION FRAMEWORK
# ==============================================================================
# Comprehensive mineral classification for federal disposition purposes.
# Critical for determining whether a mineral is locatable, leasable, or salable.

MINERAL_CLASSIFICATION: Dict[str, Dict[str, Any]] = {
    # LOCATABLE MINERALS — 1872 Mining Law (30 USC 22-54)
    "gold": {"disposition": "locatable", "claim_type": "lode_or_placer", "federal_royalty": 0.0, "notes": "Most common locatable mineral"},
    "silver": {"disposition": "locatable", "claim_type": "lode_or_placer", "federal_royalty": 0.0, "notes": "Often found with lead/zinc"},
    "copper": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Porphyry copper = lode claim"},
    "lead": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Mississippi Valley Type deposits"},
    "zinc": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Often coproduced with lead"},
    "uranium": {"disposition": "locatable", "claim_type": "lode_or_placer", "federal_royalty": 0.0, "notes": "Also requires NRC source material license"},
    "molybdenum": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Climax-type and porphyry deposits"},
    "tungsten": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Critical mineral; scheelite/wolframite"},
    "platinum": {"disposition": "locatable", "claim_type": "lode_or_placer", "federal_royalty": 0.0, "notes": "Stillwater Complex (MT) primary source"},
    "palladium": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Coproduced with platinum"},
    "rare_earth_elements": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Critical mineral; Mountain Pass (CA)"},
    "lithium_hardrock": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Spodumene, lepidolite in pegmatites"},
    "beryllium": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Topaz Mountain (UT); critical mineral"},
    "cobalt": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Usually byproduct of copper/nickel mining"},
    "nickel": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Eagle Mine (MI); laterite deposits"},
    "tin": {"disposition": "locatable", "claim_type": "lode_or_placer", "federal_royalty": 0.0, "notes": "Cassiterite deposits"},
    "chromium": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Stillwater Complex; critical mineral"},
    "manganese": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Critical mineral; limited US production"},
    "vanadium": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Colorado Plateau carnotite deposits"},
    "antimony": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Stibnite (ID); critical mineral"},
    "barite": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Drilling mud weight additive; uncommon variety"},
    "fluorspar": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Fluorite; acid-grade = locatable"},
    "mica": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Sheet mica = uncommon variety"},
    "feldspar": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Ceramic/glass grade may be uncommon"},

    # LEASABLE MINERALS — Mineral Leasing Act (30 USC 181-287)
    "coal": {"disposition": "leasable", "claim_type": "federal_lease", "federal_royalty": 0.125, "notes": "Surface 12.5%, underground 8%"},
    "oil": {"disposition": "leasable", "claim_type": "federal_lease", "federal_royalty": 0.1667, "notes": "IRA 2022 raised from 12.5% to 16.67%"},
    "natural_gas": {"disposition": "leasable", "claim_type": "federal_lease", "federal_royalty": 0.1667, "notes": "IRA 2022 raised from 12.5% to 16.67%"},
    "phosphate": {"disposition": "leasable", "claim_type": "federal_lease", "federal_royalty": 0.05, "notes": "Florida, Idaho primary sources"},
    "sodium": {"disposition": "leasable", "claim_type": "federal_lease", "federal_royalty": 0.02, "notes": "Trona deposits (WY)"},
    "potassium": {"disposition": "leasable", "claim_type": "federal_lease", "federal_royalty": 0.02, "notes": "Potash deposits (NM)"},
    "sulfur": {"disposition": "leasable", "claim_type": "federal_lease", "federal_royalty": 0.05, "notes": "Frasch process extraction"},
    "geothermal": {"disposition": "leasable", "claim_type": "federal_lease", "federal_royalty": 0.0175, "notes": "Geothermal Steam Act of 1970"},
    "oil_shale": {"disposition": "leasable", "claim_type": "federal_lease", "federal_royalty": 0.05, "notes": "Green River Formation (CO, UT, WY)"},
    "gilsonite": {"disposition": "leasable", "claim_type": "federal_lease", "federal_royalty": 0.05, "notes": "Natural asphalt; Uinta Basin (UT)"},

    # SALABLE MINERALS — Materials Act (30 USC 601-604)
    "sand_common": {"disposition": "salable", "claim_type": "materials_contract", "federal_royalty": "sale_price", "notes": "Common variety construction sand"},
    "gravel_common": {"disposition": "salable", "claim_type": "materials_contract", "federal_royalty": "sale_price", "notes": "Common variety construction gravel"},
    "stone_common": {"disposition": "salable", "claim_type": "materials_contract", "federal_royalty": "sale_price", "notes": "Crushed stone, rip-rap"},
    "pumice_common": {"disposition": "salable", "claim_type": "materials_contract", "federal_royalty": "sale_price", "notes": "Lightweight aggregate"},
    "cinder_common": {"disposition": "salable", "claim_type": "materials_contract", "federal_royalty": "sale_price", "notes": "Volcanic cinder"},
    "clay_common": {"disposition": "salable", "claim_type": "materials_contract", "federal_royalty": "sale_price", "notes": "Common brick and fill clay"},
    "petrified_wood": {"disposition": "salable", "claim_type": "materials_contract", "federal_royalty": "sale_price", "notes": "Reclassified from locatable in 1962"},

    # AMBIGUOUS / CONTESTED CLASSIFICATION
    "lithium_brine": {"disposition": "contested", "claim_type": "varies_by_state", "federal_royalty": "TBD", "notes": "Brine: mineral or water? State-dependent"},
    "helium": {"disposition": "special_statute", "claim_type": "helium_act", "federal_royalty": "special", "notes": "Helium Act; reserved to US on federal lands"},
    "limestone_uncommon": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Chemical-grade, dimension stone = uncommon variety"},
    "bentonite": {"disposition": "contested", "claim_type": "varies", "federal_royalty": "varies", "notes": "Some varieties locatable, others salable"},
    "zeolite": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Industrial applications may be uncommon variety"},
    "perlite": {"disposition": "locatable", "claim_type": "lode", "federal_royalty": 0.0, "notes": "Expanded perlite = uncommon variety"},
    "diatomite": {"disposition": "locatable", "claim_type": "lode_or_placer", "federal_royalty": 0.0, "notes": "Filter-grade = uncommon variety"},
}


# ==============================================================================
# RECLAMATION PHASE RELEASE REQUIREMENTS
# ==============================================================================

RECLAMATION_PHASE_RELEASE: Dict[str, Dict[str, Any]] = {
    "phase_1": {
        "name": "Phase I — Rough Backfilling and Grading",
        "release_pct": 0.60,
        "requirements": [
            "Backfilling and grading completed to approximate original contour",
            "All highwalls, spoil piles, and coal refuse disposed of or stabilized",
            "Drainage control structures installed and functional",
            "Topsoil segregated and stockpiled for redistribution",
            "Sediment control measures in place and effective",
        ],
        "bond_released": "Up to 60% of total bond",
        "inspection": "Regulatory authority inspection and written approval required",
        "typical_timeline": "1-3 years after mining completion",
    },
    "phase_2": {
        "name": "Phase II — Revegetation Establishment",
        "release_pct": 0.25,
        "requirements": [
            "Topsoil redistributed and amendments applied",
            "Revegetation seeded/planted with approved species mix",
            "Vegetation established and growing (not just germinated)",
            "Erosion control measures functional",
            "No significant rill or gully erosion",
            "Post-mining land use capability demonstrated",
        ],
        "bond_released": "Up to 25% of total bond (cumulative 85%)",
        "inspection": "Growing season inspection by regulatory authority",
        "typical_timeline": "2-4 years after Phase I release",
    },
    "phase_3": {
        "name": "Phase III — Final Release",
        "release_pct": 0.15,
        "requirements": [
            "Revegetation responsibility period completed (5 years eastern US, 10 years western arid)",
            "Vegetation meets productivity or ground cover standards",
            "No water quality violations from the permitted area",
            "All post-mining structures stable and functional",
            "Approved post-mining land use established",
            "No subsidence damage requiring repair (underground mining)",
            "All monitoring obligations satisfied",
        ],
        "bond_released": "Final 15% — full bond release",
        "inspection": "Final bond release inspection with public notice and comment period",
        "typical_timeline": "5-10 years after Phase II release (total 8-17 years from mining)",
    },
}


# ==============================================================================
# NRC LICENSING PATHWAY FOR URANIUM
# ==============================================================================

NRC_URANIUM_LICENSING_PATHWAY: Dict[str, Dict[str, Any]] = {
    "conventional_mine_mill": {
        "license_type": "Source Material License (10 CFR Part 40)",
        "regulatory_body": "NRC or Agreement State",
        "nepa_requirement": "Environmental Impact Statement (EIS) typical",
        "estimated_timeline_years": "5-7",
        "financial_assurance": "Required for full site decommissioning",
        "key_regulations": ["10 CFR Part 40", "10 CFR Part 20 (radiation protection)", "40 CFR Part 192 (EPA standards)"],
        "steps": [
            "1. Pre-application consultation with NRC/agreement state",
            "2. Submit license application with Environmental Report",
            "3. NRC acceptance review (6-12 months)",
            "4. NRC technical review (12-24 months)",
            "5. NEPA environmental review and EIS (18-36 months, may overlap)",
            "6. Public hearings if contested",
            "7. License issuance with conditions",
            "8. Construction and operations",
            "9. Decommissioning and license termination",
        ],
    },
    "in_situ_recovery": {
        "license_type": "Source Material License (10 CFR Part 40) + Class III/V UIC permit",
        "regulatory_body": "NRC (or Agreement State) + EPA (or delegated state)",
        "nepa_requirement": "Environmental Assessment (EA) or EIS depending on scale",
        "estimated_timeline_years": "3-5",
        "financial_assurance": "Required for aquifer restoration and site decommissioning",
        "key_regulations": [
            "10 CFR Part 40", "NUREG-1569 (ISR Standard Review Plan)",
            "40 CFR Part 146 (UIC program)", "40 CFR Part 192",
        ],
        "steps": [
            "1. Baseline groundwater characterization (12-24 months of data)",
            "2. Pre-application consultation with NRC and EPA/state",
            "3. Submit license application with Environmental Report",
            "4. Submit UIC permit application to EPA/state concurrently",
            "5. NRC technical and environmental review (12-24 months)",
            "6. Aquifer exemption request if needed (EPA)",
            "7. Public hearings if contested",
            "8. License and UIC permit issuance",
            "9. Wellfield construction and operation",
            "10. Aquifer restoration (years to decades)",
            "11. Decommissioning and license termination",
        ],
    },
    "heap_leach": {
        "license_type": "Source Material License (10 CFR Part 40)",
        "regulatory_body": "NRC or Agreement State",
        "nepa_requirement": "EIS typically required",
        "estimated_timeline_years": "5-7",
        "financial_assurance": "Required for heap closure and site decommissioning",
        "key_regulations": ["10 CFR Part 40", "10 CFR Part 20", "40 CFR Part 192", "State mine permit"],
        "steps": [
            "1. Pre-application consultation",
            "2. Submit license application",
            "3. State mining permit application (concurrent)",
            "4. NRC technical review",
            "5. NEPA review and EIS",
            "6. License issuance",
            "7. Construction and operations",
            "8. Heap rinsing and closure",
            "9. Decommissioning",
        ],
    },
}


# ==============================================================================
# GEOTHERMAL RESOURCE CLASSIFICATION
# ==============================================================================

GEOTHERMAL_RESOURCE_TYPES: Dict[str, Dict[str, str]] = {
    "hydrothermal_vapor": {
        "description": "Steam-dominated reservoirs producing dry or superheated steam",
        "example": "The Geysers, California",
        "temperature_range": ">240°C",
        "power_technology": "Dry steam plant",
        "leasing": "Geothermal Steam Act competitive lease in KGRA",
    },
    "hydrothermal_liquid": {
        "description": "Hot water reservoirs with temperatures above 150°C",
        "example": "Salton Sea, California; Dixie Valley, Nevada",
        "temperature_range": "150-240°C",
        "power_technology": "Flash steam or binary cycle plant",
        "leasing": "Geothermal Steam Act competitive or noncompetitive",
    },
    "low_temperature": {
        "description": "Warm water resources for direct use applications",
        "example": "Boise, Idaho district heating; greenhouse operations",
        "temperature_range": "30-150°C",
        "power_technology": "Direct use (heating, agriculture, aquaculture) or binary cycle",
        "leasing": "Geothermal Steam Act direct use lease (simplified)",
    },
    "enhanced_geothermal": {
        "description": "Engineered reservoirs in hot dry rock requiring hydraulic stimulation",
        "example": "DOE FORGE project, Milford, Utah",
        "temperature_range": ">150°C (at depth)",
        "power_technology": "Binary cycle after reservoir creation",
        "leasing": "Geothermal Steam Act; DOE research partnerships",
    },
    "geopressured": {
        "description": "Deep sedimentary formations with abnormal fluid pressure and dissolved methane",
        "example": "Gulf Coast geopressured-geothermal zone",
        "temperature_range": "150-200°C",
        "power_technology": "Hybrid thermal + methane recovery",
        "leasing": "Complex — may overlap oil/gas leasing jurisdiction",
    },
    "coproduced": {
        "description": "Hot water produced as byproduct of oil and gas operations",
        "example": "Produced water from deep wells in TX, WY, ND",
        "temperature_range": "80-150°C",
        "power_technology": "Binary cycle utilizing existing produced water",
        "leasing": "Under existing oil/gas lease — geothermal rights may be separate",
    },
}


# ==============================================================================
# MINING SAFETY (MSHA) KEY REQUIREMENTS
# ==============================================================================

MSHA_KEY_REQUIREMENTS: Dict[str, Dict[str, Any]] = {
    "mine_id": {
        "requirement": "Every mine must have an MSHA Mine ID number",
        "authority": "30 CFR Part 41",
        "penalty_for_noncompliance": "Civil penalty up to $70,117 per violation",
    },
    "training": {
        "requirement": "40 hours new miner training; 8 hours annual refresher; task training for new tasks",
        "authority": "30 CFR Part 46 (surface non-coal), Part 48 (coal/underground)",
        "penalty_for_noncompliance": "Civil penalty plus withdrawal order if imminent danger",
    },
    "inspection_frequency": {
        "underground_coal": "4 complete inspections per year (quarterly)",
        "surface_coal": "2 complete inspections per year (semi-annual)",
        "underground_metal_nonmetal": "4 per year",
        "surface_metal_nonmetal": "2 per year",
        "authority": "30 USC 813",
    },
    "roof_control_plan": {
        "requirement": "Underground mines must have approved roof control plan",
        "authority": "30 CFR Part 75, Subpart C",
        "notes": "Roof falls are leading cause of underground mine fatalities",
    },
    "ventilation_plan": {
        "requirement": "Underground coal mines must have approved ventilation plan",
        "authority": "30 CFR Part 75, Subpart D",
        "notes": "Methane monitoring, airflow requirements, bleeder systems",
    },
    "emergency_response": {
        "requirement": "Emergency response plan, refuge alternatives, communications",
        "authority": "MINER Act of 2006 (Pub. L. 109-236)",
        "notes": "Post-Sago mine disaster requirements",
    },
    "pattern_of_violations": {
        "requirement": "Mines with pattern of S&S violations subject to potential closure",
        "authority": "30 USC 814(e)",
        "notes": "Pattern of violations can lead to withdrawal order for entire mine",
    },
}


# ==============================================================================
# EXTENDED INLINE DOCTRINE REFERENCE — QUICK LOOKUP TABLES
# ==============================================================================
# These tables provide fast reference data for common coal/mineral queries
# without needing to load full doctrine blocks.

# State-by-state coal regulatory primacy status
STATE_COAL_PRIMACY: Dict[str, Dict[str, Any]] = {
    "AL": {"has_primacy": True, "agency": "Alabama Surface Mining Commission", "bond_type": "conventional", "aml_fee": True},
    "AK": {"has_primacy": True, "agency": "AK Dept of Natural Resources", "bond_type": "conventional", "aml_fee": True},
    "AR": {"has_primacy": True, "agency": "AR Dept of Environmental Quality", "bond_type": "conventional", "aml_fee": True},
    "CO": {"has_primacy": True, "agency": "CO Div of Reclamation, Mining & Safety", "bond_type": "conventional", "aml_fee": True},
    "IL": {"has_primacy": True, "agency": "IL Dept of Natural Resources", "bond_type": "conventional", "aml_fee": True},
    "IN": {"has_primacy": True, "agency": "IN Dept of Natural Resources", "bond_type": "conventional", "aml_fee": True},
    "IA": {"has_primacy": True, "agency": "IA Dept of Agriculture & Land Stewardship", "bond_type": "conventional", "aml_fee": True},
    "KS": {"has_primacy": True, "agency": "KS Dept of Health & Environment", "bond_type": "conventional", "aml_fee": True},
    "KY": {"has_primacy": True, "agency": "KY Energy & Environment Cabinet", "bond_type": "pool/conventional", "aml_fee": True},
    "LA": {"has_primacy": True, "agency": "LA Dept of Natural Resources", "bond_type": "conventional", "aml_fee": True},
    "MD": {"has_primacy": True, "agency": "MD Dept of Environment", "bond_type": "conventional", "aml_fee": True},
    "MO": {"has_primacy": True, "agency": "MO Dept of Natural Resources", "bond_type": "conventional", "aml_fee": True},
    "MT": {"has_primacy": True, "agency": "MT Dept of Environmental Quality", "bond_type": "conventional", "aml_fee": True},
    "NM": {"has_primacy": True, "agency": "NM Mining & Minerals Division", "bond_type": "conventional", "aml_fee": True},
    "ND": {"has_primacy": True, "agency": "ND Public Service Commission", "bond_type": "conventional", "aml_fee": True},
    "OH": {"has_primacy": True, "agency": "OH Dept of Natural Resources", "bond_type": "conventional", "aml_fee": True},
    "OK": {"has_primacy": True, "agency": "OK Dept of Mines", "bond_type": "conventional", "aml_fee": True},
    "PA": {"has_primacy": True, "agency": "PA Dept of Environmental Protection", "bond_type": "pool/conventional", "aml_fee": True},
    "TX": {"has_primacy": True, "agency": "TX Railroad Commission", "bond_type": "conventional", "aml_fee": True},
    "UT": {"has_primacy": True, "agency": "UT Div of Oil, Gas & Mining", "bond_type": "conventional", "aml_fee": True},
    "VA": {"has_primacy": True, "agency": "VA Dept of Energy", "bond_type": "conventional", "aml_fee": True},
    "WV": {"has_primacy": True, "agency": "WV Dept of Environmental Protection", "bond_type": "pool/conventional", "aml_fee": True},
    "WY": {"has_primacy": True, "agency": "WY Dept of Environmental Quality", "bond_type": "conventional", "aml_fee": True},
}

# State-by-state broad form deed doctrine
STATE_BROAD_FORM_DEED_DOCTRINE: Dict[str, Dict[str, str]] = {
    "KY": {
        "doctrine": "reformed",
        "key_case": "Ward v. Harding, 860 S.W.2d 280 (Ky. 1993)",
        "rule": "1988 constitutional amendment requires surface owner consent for surface mining under broad form deeds",
        "effective_date": "1988-11-08",
    },
    "WV": {
        "doctrine": "reasonable_use",
        "key_case": "Buffalo Mining Co. v. Martin, 165 W.Va. 10 (1980)",
        "rule": "Mineral owner has reasonable use right; surface owner protected from wanton or unnecessary destruction",
        "effective_date": "1980",
    },
    "VA": {
        "doctrine": "broad_form",
        "key_case": "Various — Virginia retains traditional broad form doctrine",
        "rule": "Mineral owner retains expansive surface use rights under traditional broad form doctrine",
        "effective_date": "common_law",
    },
    "PA": {
        "doctrine": "accommodation_modified",
        "key_case": "Pennsylvania Coal Co. v. Mahon, 260 U.S. 393 (1922)",
        "rule": "Accommodation doctrine with Bituminous Mine Subsidence Act protections for occupied structures",
        "effective_date": "1966_act",
    },
    "TX": {
        "doctrine": "accommodation",
        "key_case": "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
        "rule": "Accommodation doctrine — mineral owner must use least intrusive method if alternatives exist",
        "effective_date": "1971",
    },
}

# Coal bed methane ownership by state
STATE_CBM_OWNERSHIP: Dict[str, Dict[str, str]] = {
    "federal": {
        "rule": "CBM is part of gas estate, not coal estate",
        "key_case": "Amoco Production Co. v. Southern Ute Indian Tribe, 526 U.S. 865 (1999)",
        "owner": "gas_estate",
    },
    "PA": {
        "rule": "CBM owned by coal estate while adsorbed in coal seam",
        "key_case": "US Steel Mining Co. v. Hoge, 468 A.2d 1380 (Pa. 1983)",
        "owner": "coal_estate",
    },
    "WV": {
        "rule": "CBM presumed part of gas estate",
        "key_case": "Continental Resources v. Howard, 218 W.Va. 313 (2005)",
        "owner": "gas_estate",
    },
    "VA": {
        "rule": "CBM follows gas estate under Amoco rationale",
        "key_case": "CONSOL Energy Inc. v. Virginia Crews, 285 Va. 131 (2013)",
        "owner": "gas_estate",
    },
    "WY": {
        "rule": "CBM is gas for purposes of oil/gas lease",
        "key_case": "Newman v. RAG Wyoming Land Co., 53 P.3d 540 (Wyo. 2002)",
        "owner": "gas_estate",
    },
}

# State severance tax rates for coal
STATE_COAL_SEVERANCE_TAXES: Dict[str, Dict[str, Any]] = {
    "WY": {"surface_rate": 0.07, "underground_rate": 0.0375, "base": "gross_value", "notes": "Highest producer state"},
    "WV": {"surface_rate": 0.05, "underground_rate": 0.05, "base": "gross_value", "notes": "Additional local coal severance taxes may apply"},
    "MT": {"surface_rate": "variable", "underground_rate": "variable", "base": "varies_by_type_and_btu", "notes": "Complex rate schedule based on coal type, BTU, and mining method"},
    "PA": {"surface_rate": 0.0, "underground_rate": 0.0, "base": "none", "notes": "No severance tax; Act 54 impact fee for oil/gas only"},
    "IL": {"surface_rate": 0.0, "underground_rate": 0.0, "base": "none", "notes": "No state coal severance tax"},
    "KY": {"surface_rate": 0.045, "underground_rate": 0.045, "base": "gross_value", "notes": "4.5% of gross value or min 50 cents/ton"},
    "VA": {"surface_rate": 0.02, "underground_rate": 0.02, "base": "gross_receipts", "notes": "2% of gross receipts; additional local coal road tax"},
    "AL": {"surface_rate": 0.135, "underground_rate": 0.135, "base": "per_ton", "notes": "$0.135 per ton surface; $0.205 underground"},
    "OH": {"surface_rate": 0.10, "underground_rate": 0.10, "base": "per_ton", "notes": "$0.10 per ton"},
    "IN": {"surface_rate": 0.0, "underground_rate": 0.0, "base": "none", "notes": "No coal severance tax"},
    "CO": {"surface_rate": "variable", "underground_rate": "variable", "base": "varies", "notes": "Metallic minerals 2.25%, coal rates vary by county"},
    "TX": {"surface_rate": 0.0, "underground_rate": 0.0, "base": "none", "notes": "No coal-specific severance tax; lignite operations taxed differently"},
    "ND": {"surface_rate": "variable", "underground_rate": "variable", "base": "varies", "notes": "Coal conversion tax + severance; combined ~$1.04/ton"},
    "NM": {"surface_rate": 0.0075, "underground_rate": 0.0075, "base": "taxable_value", "notes": "Resources excise tax + conservation tax"},
    "UT": {"surface_rate": "variable", "underground_rate": "variable", "base": "varies", "notes": "Mining severance varies by mineral type"},
}

# Pore space ownership statutes by state
STATE_PORE_SPACE_STATUTES: Dict[str, Dict[str, str]] = {
    "WY": {"statute": "Wyo. Stat. § 34-1-152", "year": "2008", "owner": "surface", "notes": "First state to enact pore space statute"},
    "MT": {"statute": "Mont. Code Ann. § 82-11-180", "year": "2009", "owner": "surface", "notes": "Surface owner owns pore space"},
    "ND": {"statute": "N.D. Cent. Code § 38-22", "year": "2009", "owner": "surface", "notes": "Comprehensive CCS framework including unitization"},
    "LA": {"statute": "La. Rev. Stat. § 30:1101", "year": "2009", "owner": "surface", "notes": "Pore space belongs to surface owner; force pooling available"},
    "TX": {"statute": "Tex. Nat. Res. Code § 27.041", "year": "2009", "owner": "surface_implied", "notes": "Not explicit statute but implied through UIC framework"},
    "OK": {"statute": "Okla. Stat. tit. 27A § 3-5-109", "year": "2018", "owner": "surface", "notes": "CCS Geologic Storage of CO2 Act"},
    "WV": {"statute": "W.Va. Code § 22-11B", "year": "2022", "owner": "surface", "notes": "Carbon Dioxide Sequestration Working Interest Act"},
    "IL": {"statute": "20 ILCS 1110/5 (CCS legislation)", "year": "2011", "owner": "surface", "notes": "Clean Coal FutureGen project framework"},
    "IN": {"statute": "Ind. Code § 14-39-1", "year": "2011", "owner": "surface", "notes": "CO2 underground storage provisions"},
    "KS": {"statute": "K.S.A. § 55-1636", "year": "2020", "owner": "surface", "notes": "CCS permitting framework"},
}

# Mining claim annual maintenance fee schedule
MINING_CLAIM_MAINTENANCE: Dict[str, Any] = {
    "maintenance_fee_per_claim": 165.00,
    "assessment_work_per_claim": 100.00,
    "fee_due_date": "September 1 (noon)",
    "assessment_year": "September 1 to September 1",
    "affidavit_due_date": "December 30",
    "small_miner_threshold": 10,
    "patent_price_lode_per_acre": 5.00,
    "patent_price_placer_per_acre": 2.50,
    "patent_moratorium_since": 1994,
    "lode_claim_max_length_ft": 1500,
    "lode_claim_max_width_ft": 600,
    "placer_claim_max_acres_individual": 20,
    "placer_claim_max_acres_association": 160,
    "association_min_persons": 8,
    "mill_site_max_acres": 5,
}

# Critical minerals list (USGS 2022 final)
CRITICAL_MINERALS_LIST: List[Dict[str, str]] = [
    {"mineral": "Aluminum", "primary_use": "Transportation, packaging", "domestic_production": "limited"},
    {"mineral": "Antimony", "primary_use": "Flame retardants, ammunition", "domestic_production": "none"},
    {"mineral": "Arsenic", "primary_use": "Pressure-treated wood, semiconductors", "domestic_production": "none"},
    {"mineral": "Barite", "primary_use": "Oil/gas drilling, medical", "domestic_production": "moderate"},
    {"mineral": "Beryllium", "primary_use": "Aerospace, defense electronics", "domestic_production": "sole_source_UT"},
    {"mineral": "Bismuth", "primary_use": "Pharmaceuticals, chemicals", "domestic_production": "none"},
    {"mineral": "Cesium", "primary_use": "Research, drilling fluids", "domestic_production": "none"},
    {"mineral": "Chromium", "primary_use": "Stainless steel, aerospace", "domestic_production": "none"},
    {"mineral": "Cobalt", "primary_use": "Batteries, superalloys", "domestic_production": "byproduct_only"},
    {"mineral": "Fluorspar", "primary_use": "Steel, aluminum, chemical production", "domestic_production": "limited"},
    {"mineral": "Gallium", "primary_use": "Semiconductors, LEDs", "domestic_production": "none"},
    {"mineral": "Germanium", "primary_use": "Fiber optics, infrared", "domestic_production": "recycled_only"},
    {"mineral": "Graphite", "primary_use": "Batteries, lubricants, refractories", "domestic_production": "one_mine_AL"},
    {"mineral": "Hafnium", "primary_use": "Nuclear reactors, superalloys", "domestic_production": "byproduct"},
    {"mineral": "Indium", "primary_use": "LCD screens, semiconductors", "domestic_production": "recycled_only"},
    {"mineral": "Lithium", "primary_use": "Batteries, glass, ceramics", "domestic_production": "one_mine_NV"},
    {"mineral": "Manganese", "primary_use": "Steel production", "domestic_production": "none"},
    {"mineral": "Nickel", "primary_use": "Stainless steel, batteries", "domestic_production": "one_mine_MI"},
    {"mineral": "Niobium", "primary_use": "Steel alloys, superconductors", "domestic_production": "none"},
    {"mineral": "Platinum Group", "primary_use": "Catalytic converters, electronics", "domestic_production": "one_mine_MT"},
    {"mineral": "Rare Earth Elements", "primary_use": "Magnets, catalysts, electronics", "domestic_production": "one_mine_CA"},
    {"mineral": "Rubidium", "primary_use": "Research, electronic", "domestic_production": "none"},
    {"mineral": "Scandium", "primary_use": "Aluminum alloys, solid oxide fuel cells", "domestic_production": "none"},
    {"mineral": "Tantalum", "primary_use": "Capacitors, surgical implants", "domestic_production": "none"},
    {"mineral": "Tellurium", "primary_use": "Solar cells, thermoelectrics", "domestic_production": "byproduct"},
    {"mineral": "Tin", "primary_use": "Solder, tin plate", "domestic_production": "none"},
    {"mineral": "Titanium", "primary_use": "Aerospace, pigments", "domestic_production": "moderate"},
    {"mineral": "Tungsten", "primary_use": "Cutting tools, ammunition", "domestic_production": "limited"},
    {"mineral": "Vanadium", "primary_use": "Steel alloys, batteries", "domestic_production": "byproduct"},
    {"mineral": "Zinc", "primary_use": "Galvanizing, alloys", "domestic_production": "moderate"},
    {"mineral": "Zirconium", "primary_use": "Nuclear fuel cladding, ceramics", "domestic_production": "moderate"},
]

# Federal mineral leasing royalty rates
FEDERAL_ROYALTY_RATES: Dict[str, Dict[str, Any]] = {
    "coal_surface": {"rate": 0.125, "base": "gross_value", "authority": "30 USC 207"},
    "coal_underground": {"rate": 0.08, "base": "gross_value", "authority": "30 USC 207"},
    "oil": {"rate": 0.1667, "base": "production_value", "authority": "IRA 2022 amendment"},
    "gas": {"rate": 0.1667, "base": "production_value", "authority": "IRA 2022 amendment"},
    "phosphate": {"rate": 0.05, "base": "gross_value", "authority": "30 USC 211"},
    "sodium": {"rate": 0.02, "base": "gross_value", "authority": "30 USC 262"},
    "potassium": {"rate": 0.02, "base": "gross_value", "authority": "30 USC 262"},
    "sulfur": {"rate": 0.05, "base": "gross_value", "authority": "30 USC 271"},
    "geothermal_electricity_yr1_10": {"rate": 0.0175, "base": "gross_proceeds", "authority": "30 USC 1004"},
    "geothermal_electricity_yr11_plus": {"rate": 0.035, "base": "gross_proceeds", "authority": "30 USC 1004"},
    "geothermal_direct_use": {"rate": 0.10, "base": "gross_proceeds", "authority": "30 USC 1004"},
    "hardrock_locatable": {"rate": 0.0, "base": "none", "authority": "30 USC 22 (no federal royalty)"},
}

# SMCRA lands unsuitable for mining (30 USC 1272)
SMCRA_UNSUITABLE_LANDS: List[Dict[str, str]] = [
    {"category": "National Park System", "authority": "30 USC 1272(e)(1)", "prohibition": "Absolute — no surface coal mining"},
    {"category": "National Wildlife Refuge System", "authority": "30 USC 1272(e)(1)", "prohibition": "Absolute — no surface coal mining"},
    {"category": "National Trail System", "authority": "30 USC 1272(e)(1)", "prohibition": "Absolute — no surface coal mining"},
    {"category": "National Wilderness Preservation System", "authority": "30 USC 1272(e)(1)", "prohibition": "Absolute — no surface coal mining"},
    {"category": "Wild and Scenic Rivers", "authority": "30 USC 1272(e)(1)", "prohibition": "Absolute — no surface coal mining"},
    {"category": "National Recreation Areas", "authority": "30 USC 1272(e)(2)", "prohibition": "Subject to valid existing rights"},
    {"category": "Federal lands within National Forests", "authority": "30 USC 1272(e)(2)", "prohibition": "Subject to consent and compatibility"},
    {"category": "Publicly owned parks", "authority": "30 USC 1272(e)(3)", "prohibition": "Within 100 feet of public building/park"},
    {"category": "Occupied dwellings", "authority": "30 USC 1272(e)(4)", "prohibition": "Within 300 feet unless waived"},
    {"category": "Public roads", "authority": "30 USC 1272(e)(4)", "prohibition": "Within 100 feet of public road right-of-way"},
    {"category": "Cemeteries", "authority": "30 USC 1272(e)(5)", "prohibition": "Within 100 feet of cemetery"},
    {"category": "Alluvial valley floors", "authority": "30 USC 1272(b)(1)", "prohibition": "West of 100th meridian if irrigated agriculture dependent"},
]


# ==============================================================================
# RESPONSE MODE FORMATTERS
# ==============================================================================

class FastModeFormatter:
    """Format responses in FAST mode — concise, doctrine-driven."""

    @staticmethod
    def format(response: QueryResponse) -> Dict[str, Any]:
        """Format for FAST mode consumption."""
        primary = response.doctrines[0] if response.doctrines else None
        return {
            "answer": primary.conclusion if primary else "No doctrine match",
            "confidence": primary.confidence if primary else "UNKNOWN",
            "key_factors": primary.key_factors[:3] if primary else [],
            "top_authority": primary.authorities[0].citation if primary and primary.authorities else None,
            "latency_ms": response.total_latency_ms,
            "determinism_hash": response.determinism_hash,
        }


class DefenseModeFormatter:
    """Format responses in DEFENSE mode — audit-ready, structured."""

    @staticmethod
    def format(response: QueryResponse) -> Dict[str, Any]:
        """Format for DEFENSE mode consumption."""
        sections: List[Dict[str, Any]] = []

        for doctrine in response.doctrines:
            section = {
                "topic": doctrine.topic,
                "position": doctrine.conclusion,
                "confidence": doctrine.confidence,
                "stratification": doctrine.confidence_stratification,
                "burden": doctrine.burden_holder,
                "key_factors": doctrine.key_factors,
                "authorities": [
                    {"citation": a.citation, "weight": a.weight, "type": a.authority_type}
                    for a in doctrine.authorities
                ],
                "resolution": doctrine.resolution_strategy,
            }
            sections.append(section)

        result: Dict[str, Any] = {
            "defense_analysis": sections,
            "zone": response.zone,
            "zone_guidance": response.zoned_analysis.zone_guidance if response.zoned_analysis else None,
            "risk_factors": response.zoned_analysis.risk_factors if response.zoned_analysis else [],
            "recommended_actions": response.zoned_analysis.recommended_actions if response.zoned_analysis else [],
            "fact_fragility": response.fact_fragility.model_dump() if response.fact_fragility else None,
            "disclosure_caveat": response.disclosure_caveat,
            "determinism_hash": response.determinism_hash,
            "latency_ms": response.total_latency_ms,
        }

        return result


class MemoModeFormatter:
    """Format responses in MEMO mode — full documentation."""

    @staticmethod
    def format(response: QueryResponse) -> Dict[str, Any]:
        """Format for MEMO mode consumption — comprehensive memorandum."""
        memo_sections: List[Dict[str, Any]] = []

        # Executive summary
        primary = response.doctrines[0] if response.doctrines else None
        executive_summary = {
            "section": "EXECUTIVE SUMMARY",
            "content": primary.conclusion if primary else "Analysis pending — no matching doctrine identified.",
            "confidence": primary.confidence if primary else "N/A",
        }
        memo_sections.append(executive_summary)

        # Issue identification
        if response.deep_analysis:
            issues_section = {
                "section": "ISSUE IDENTIFICATION",
                "categories": response.deep_analysis.issue_categories,
                "decomposition": response.deep_analysis.multi_doctrine_decomposition,
                "interaction_graph": response.deep_analysis.interaction_edges,
            }
            memo_sections.append(issues_section)

        # Authority analysis
        for idx, doctrine in enumerate(response.doctrines):
            authority_section = {
                "section": f"AUTHORITY ANALYSIS — {doctrine.topic.upper().replace('_', ' ')}",
                "position": doctrine.conclusion,
                "confidence": doctrine.confidence,
                "stratification": doctrine.confidence_stratification,
                "key_factors": doctrine.key_factors,
                "authorities": [
                    {"citation": a.citation, "weight": a.weight, "type": a.authority_type}
                    for a in doctrine.authorities
                ],
                "burden_of_proof": doctrine.burden_holder,
                "resolution_strategy": doctrine.resolution_strategy,
            }
            memo_sections.append(authority_section)

        # Risk assessment
        risk_section = {
            "section": "RISK ASSESSMENT",
            "fact_fragility": response.fact_fragility.model_dump() if response.fact_fragility else None,
            "zone_analysis": response.zoned_analysis.model_dump() if response.zoned_analysis else None,
            "disclosure_required": response.disclosure_caveat is not None,
            "disclosure_caveat": response.disclosure_caveat,
        }
        memo_sections.append(risk_section)

        # Counter arguments
        if response.counter_arguments:
            counter_section = {
                "section": "COUNTER ARGUMENTS AND ADVERSE AUTHORITY",
                "arguments": response.counter_arguments,
            }
            memo_sections.append(counter_section)

        # Reasoning chain
        if response.deep_analysis:
            reasoning_section = {
                "section": "REASONING CHAIN",
                "steps": response.deep_analysis.reasoning_chain,
                "synthesis": response.deep_analysis.synthesis,
            }
            memo_sections.append(reasoning_section)

        return {
            "memorandum": memo_sections,
            "metadata": {
                "engine": ENGINE_ID,
                "version": ENGINE_VERSION,
                "query": response.query,
                "mode": "MEMO",
                "zone": response.zone,
                "timestamp": response.timestamp,
                "determinism_hash": response.determinism_hash,
                "latency_ms": response.total_latency_ms,
                "doctrines_analyzed": len(response.doctrines),
            },
        }


# ==============================================================================
# BATCH QUERY PROCESSOR
# ==============================================================================

class BatchQueryRequest(BaseModel):
    """Request for processing multiple queries in batch."""
    queries: List[QueryRequest] = Field(..., min_length=1, max_length=50)
    parallel: bool = Field(default=False, description="Process in parallel (future)")


class BatchQueryResponse(BaseModel):
    """Response for batch query processing."""
    total: int
    successful: int
    failed: int
    results: List[Dict[str, Any]]
    total_latency_ms: float


def process_batch_queries(batch: BatchQueryRequest) -> BatchQueryResponse:
    """Process a batch of queries sequentially."""
    engine = get_engine()
    results: List[Dict[str, Any]] = []
    successful = 0
    failed = 0
    start = time.perf_counter()

    for req in batch.queries:
        try:
            response = engine.process_query(req)
            results.append({"status": "success", "response": response.model_dump()})
            successful += 1
        except HTTPException as exc:
            results.append({"status": "error", "query": req.query, "error": str(exc.detail)})
            failed += 1
        except Exception as exc:
            results.append({"status": "error", "query": req.query, "error": str(exc)})
            failed += 1

    elapsed = (time.perf_counter() - start) * 1000
    return BatchQueryResponse(
        total=len(batch.queries),
        successful=successful,
        failed=failed,
        results=results,
        total_latency_ms=round(elapsed, 2),
    )


@app.post("/batch")
async def batch_endpoint(batch: BatchQueryRequest) -> Dict[str, Any]:
    """Batch query processing endpoint."""
    result = process_batch_queries(batch)
    return result.model_dump()


# ==============================================================================
# FORMATTED QUERY ENDPOINTS
# ==============================================================================

@app.post("/query/fast")
async def query_fast(request: QueryRequest) -> Dict[str, Any]:
    """Query with FAST mode formatting."""
    request.mode = ResponseMode.FAST
    engine = get_engine()
    response = engine.process_query(request)
    return FastModeFormatter.format(response)


@app.post("/query/defense")
async def query_defense(request: QueryRequest) -> Dict[str, Any]:
    """Query with DEFENSE mode formatting."""
    request.mode = ResponseMode.DEFENSE
    engine = get_engine()
    response = engine.process_query(request)
    return DefenseModeFormatter.format(response)


@app.post("/query/memo")
async def query_memo(request: QueryRequest) -> Dict[str, Any]:
    """Query with MEMO mode formatting — full memorandum."""
    request.mode = ResponseMode.MEMO
    request.include_counter_arguments = True
    engine = get_engine()
    response = engine.process_query(request)
    return MemoModeFormatter.format(response)


# ==============================================================================
# REFERENCE DATA ENDPOINTS
# ==============================================================================

@app.get("/reference/primacy")
async def reference_primacy() -> Dict[str, Any]:
    """State coal regulatory primacy status reference."""
    return {
        "states": STATE_COAL_PRIMACY,
        "total_primacy_states": len(STATE_COAL_PRIMACY),
    }


@app.get("/reference/broad-form-deeds")
async def reference_broad_form() -> Dict[str, Any]:
    """State broad form deed doctrine reference."""
    return {
        "states": STATE_BROAD_FORM_DEED_DOCTRINE,
        "total_states": len(STATE_BROAD_FORM_DEED_DOCTRINE),
    }


@app.get("/reference/cbm-ownership")
async def reference_cbm() -> Dict[str, Any]:
    """State CBM ownership rules reference."""
    return {
        "jurisdictions": STATE_CBM_OWNERSHIP,
        "total": len(STATE_CBM_OWNERSHIP),
    }


@app.get("/reference/severance-taxes")
async def reference_severance_taxes() -> Dict[str, Any]:
    """State coal severance tax rates reference."""
    return {
        "states": STATE_COAL_SEVERANCE_TAXES,
        "total_states": len(STATE_COAL_SEVERANCE_TAXES),
    }


@app.get("/reference/pore-space")
async def reference_pore_space() -> Dict[str, Any]:
    """State pore space ownership statutes reference."""
    return {
        "states": STATE_PORE_SPACE_STATUTES,
        "total_states": len(STATE_PORE_SPACE_STATUTES),
    }


@app.get("/reference/claim-maintenance")
async def reference_claim_maintenance() -> Dict[str, Any]:
    """Mining claim maintenance requirements reference."""
    return MINING_CLAIM_MAINTENANCE


@app.get("/reference/critical-minerals")
async def reference_critical_minerals() -> Dict[str, Any]:
    """USGS critical minerals list reference."""
    return {
        "minerals": CRITICAL_MINERALS_LIST,
        "total": len(CRITICAL_MINERALS_LIST),
        "source": "USGS 2022 Final List",
    }


@app.get("/reference/royalty-rates")
async def reference_royalty_rates() -> Dict[str, Any]:
    """Federal mineral leasing royalty rates reference."""
    return {
        "rates": FEDERAL_ROYALTY_RATES,
        "total_categories": len(FEDERAL_ROYALTY_RATES),
    }


@app.get("/reference/unsuitable-lands")
async def reference_unsuitable_lands() -> Dict[str, Any]:
    """SMCRA lands unsuitable for mining reference."""
    return {
        "categories": SMCRA_UNSUITABLE_LANDS,
        "total_categories": len(SMCRA_UNSUITABLE_LANDS),
        "authority": "30 USC 1272",
    }


# ==============================================================================
# COMPARATIVE ANALYSIS ENDPOINT
# ==============================================================================

class CompareRequest(BaseModel):
    """Request to compare doctrines across jurisdictions."""
    topic: str = Field(..., description="Doctrine topic to compare")
    jurisdictions: List[str] = Field(default=["federal", "KY", "WV", "PA", "VA", "TX"],
                                     description="Jurisdictions to compare")


@app.post("/compare")
async def compare_jurisdictions(request: CompareRequest) -> Dict[str, Any]:
    """Compare doctrine application across jurisdictions."""
    topic = request.topic.lower()
    results: Dict[str, Any] = {"topic": request.topic, "jurisdictions": {}}

    if "broad form" in topic or "broad_form" in topic:
        for jur in request.jurisdictions:
            jur_upper = jur.upper()
            if jur_upper in STATE_BROAD_FORM_DEED_DOCTRINE:
                results["jurisdictions"][jur_upper] = STATE_BROAD_FORM_DEED_DOCTRINE[jur_upper]
            else:
                results["jurisdictions"][jur_upper] = {"doctrine": "not_specifically_addressed", "notes": "Check general mineral estate law"}

    elif "cbm" in topic or "coal bed" in topic or "coalbed" in topic:
        for jur in request.jurisdictions:
            jur_key = jur.lower() if jur.lower() == "federal" else jur.upper()
            if jur_key in STATE_CBM_OWNERSHIP:
                results["jurisdictions"][jur_key] = STATE_CBM_OWNERSHIP[jur_key]
            else:
                results["jurisdictions"][jur_key] = {"rule": "not_specifically_addressed", "notes": "Check general gas estate law"}

    elif "severance" in topic or "tax" in topic:
        for jur in request.jurisdictions:
            jur_upper = jur.upper()
            if jur_upper in STATE_COAL_SEVERANCE_TAXES:
                results["jurisdictions"][jur_upper] = STATE_COAL_SEVERANCE_TAXES[jur_upper]
            else:
                results["jurisdictions"][jur_upper] = {"rate": "unknown", "notes": "Not in reference database"}

    elif "pore space" in topic or "carbon" in topic or "ccs" in topic:
        for jur in request.jurisdictions:
            jur_upper = jur.upper()
            if jur_upper in STATE_PORE_SPACE_STATUTES:
                results["jurisdictions"][jur_upper] = STATE_PORE_SPACE_STATUTES[jur_upper]
            else:
                results["jurisdictions"][jur_upper] = {"statute": "none", "notes": "No specific pore space statute; apply common law"}

    elif "primacy" in topic:
        for jur in request.jurisdictions:
            jur_upper = jur.upper()
            if jur_upper in STATE_COAL_PRIMACY:
                results["jurisdictions"][jur_upper] = STATE_COAL_PRIMACY[jur_upper]
            else:
                results["jurisdictions"][jur_upper] = {"has_primacy": False, "notes": "OSMRE federal program applies"}

    else:
        results["error"] = f"Comparative analysis not available for topic: {request.topic}"
        results["available_topics"] = ["broad_form_deeds", "cbm_ownership", "severance_taxes", "pore_space", "primacy"]

    return results


# ==============================================================================
# ENGINE SUMMARY ENDPOINT
# ==============================================================================

@app.get("/summary")
async def engine_summary() -> Dict[str, Any]:
    """Complete engine summary — all capabilities and reference data counts."""
    engine = get_engine()
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "architecture": "Three-Layer (Doctrine Cache → Semantic Retrieval → Deep Analysis)",
        "response_modes": ["FAST", "DEFENSE", "MEMO"],
        "position_zones": ["PLANNING", "REPORTING", "AUDIT"],
        "confidence_levels": ["DEFENSIBLE", "AGGRESSIVE", "DISCLOSURE", "HIGH_RISK"],
        "tie_components": 20,
        "doctrine_count": get_doctrine_count(),
        "doctrine_topics": get_doctrine_topics(),
        "semantic_synonyms": get_synonym_count(),
        "semantic_canonical_forms": get_canonical_count(),
        "semantic_domains": get_all_domains(),
        "issue_categories": [e.value for e in IssueCategory],
        "interaction_edges": len(ISSUE_INTERACTION_EDGES),
        "authority_hierarchy_levels": len(AUTHORITY_HIERARCHY),
        "reference_data": {
            "primacy_states": len(STATE_COAL_PRIMACY),
            "broad_form_deed_states": len(STATE_BROAD_FORM_DEED_DOCTRINE),
            "cbm_ownership_jurisdictions": len(STATE_CBM_OWNERSHIP),
            "severance_tax_states": len(STATE_COAL_SEVERANCE_TAXES),
            "pore_space_statute_states": len(STATE_PORE_SPACE_STATUTES),
            "critical_minerals": len(CRITICAL_MINERALS_LIST),
            "federal_royalty_categories": len(FEDERAL_ROYALTY_RATES),
            "unsuitable_land_categories": len(SMCRA_UNSUITABLE_LANDS),
        },
        "endpoints": [
            "GET /", "GET /health", "GET /summary",
            "POST /query", "POST /query/fast", "POST /query/defense", "POST /query/memo",
            "POST /batch", "POST /compare",
            "GET /doctrines", "GET /doctrines/{topic}",
            "GET /search?q=", "GET /normalize?term=",
            "GET /metrics", "GET /coverage", "GET /drift", "GET /telemetry", "GET /audit",
            "GET /domains", "GET /interactions", "GET /authorities",
            "GET /reference/primacy", "GET /reference/broad-form-deeds",
            "GET /reference/cbm-ownership", "GET /reference/severance-taxes",
            "GET /reference/pore-space", "GET /reference/claim-maintenance",
            "GET /reference/critical-minerals", "GET /reference/royalty-rates",
            "GET /reference/unsuitable-lands", "GET /reference/mineral-classification",
            "GET /reference/reclamation-phases", "GET /reference/nrc-licensing",
            "GET /reference/geothermal-types", "GET /reference/msha-requirements",
            "GET /classify-mineral", "GET /classify-authority",
        ],
    }


# ==============================================================================
# ADDITIONAL REFERENCE ENDPOINTS
# ==============================================================================

@app.get("/reference/mineral-classification")
async def reference_mineral_classification() -> Dict[str, Any]:
    """Federal mineral disposition classification reference."""
    locatable = {k: v for k, v in MINERAL_CLASSIFICATION.items() if v["disposition"] == "locatable"}
    leasable = {k: v for k, v in MINERAL_CLASSIFICATION.items() if v["disposition"] == "leasable"}
    salable = {k: v for k, v in MINERAL_CLASSIFICATION.items() if v["disposition"] == "salable"}
    contested = {k: v for k, v in MINERAL_CLASSIFICATION.items() if v["disposition"] in ("contested", "special_statute")}
    return {
        "total_minerals": len(MINERAL_CLASSIFICATION),
        "locatable": {"count": len(locatable), "minerals": locatable},
        "leasable": {"count": len(leasable), "minerals": leasable},
        "salable": {"count": len(salable), "minerals": salable},
        "contested": {"count": len(contested), "minerals": contested},
    }


@app.get("/reference/reclamation-phases")
async def reference_reclamation_phases() -> Dict[str, Any]:
    """SMCRA reclamation phase release requirements reference."""
    return {
        "phases": RECLAMATION_PHASE_RELEASE,
        "total_phases": len(RECLAMATION_PHASE_RELEASE),
        "authority": "30 USC 1269 and 30 CFR Part 800",
    }


@app.get("/reference/nrc-licensing")
async def reference_nrc_licensing() -> Dict[str, Any]:
    """NRC uranium licensing pathway reference."""
    return {
        "pathways": NRC_URANIUM_LICENSING_PATHWAY,
        "total_pathways": len(NRC_URANIUM_LICENSING_PATHWAY),
        "authority": "10 CFR Part 40 (Atomic Energy Act)",
    }


@app.get("/reference/geothermal-types")
async def reference_geothermal_types() -> Dict[str, Any]:
    """Geothermal resource type classification reference."""
    return {
        "resource_types": GEOTHERMAL_RESOURCE_TYPES,
        "total_types": len(GEOTHERMAL_RESOURCE_TYPES),
        "authority": "30 USC 1001-1028 (Geothermal Steam Act)",
    }


@app.get("/reference/msha-requirements")
async def reference_msha() -> Dict[str, Any]:
    """MSHA key safety requirements reference."""
    return {
        "requirements": MSHA_KEY_REQUIREMENTS,
        "total_categories": len(MSHA_KEY_REQUIREMENTS),
        "authority": "30 USC 801-966 (Federal Mine Safety and Health Act)",
    }


@app.get("/classify-mineral")
async def classify_mineral_endpoint(mineral: str) -> Dict[str, Any]:
    """Classify a mineral by federal disposition type."""
    mineral_lower = mineral.lower().replace(" ", "_").replace("-", "_")
    # Direct match
    if mineral_lower in MINERAL_CLASSIFICATION:
        return {"mineral": mineral, "classification": MINERAL_CLASSIFICATION[mineral_lower]}
    # Partial match
    for key, value in MINERAL_CLASSIFICATION.items():
        if mineral_lower in key or key in mineral_lower:
            return {"mineral": mineral, "matched_key": key, "classification": value}
    return {
        "mineral": mineral,
        "classification": None,
        "message": "Mineral not found in classification database. Check if it is a common variety (salable) or uncommon variety (locatable).",
        "guidance": "Apply the McClarty common variety test: does the deposit have unique properties giving it special value?",
    }


@app.get("/classify-authority")
async def classify_authority_endpoint(citation: str) -> Dict[str, Any]:
    """Classify a legal authority citation by type and weight."""
    auth_type, weight = classify_authority(citation)
    return {
        "citation": citation,
        "authority_type": auth_type,
        "weight": weight,
        "hierarchy_position": list(AUTHORITY_HIERARCHY.keys()).index(auth_type) + 1 if auth_type in AUTHORITY_HIERARCHY else None,
        "total_hierarchy_levels": len(AUTHORITY_HIERARCHY),
    }


# ==============================================================================
# CHAIN OF TITLE ANALYSIS HELPER
# ==============================================================================

class ChainOfTitleRequest(BaseModel):
    """Request for mineral chain of title analysis guidance."""
    state: str = Field(..., description="State abbreviation (e.g., WV, KY, PA)")
    mineral_type: str = Field(..., description="Mineral type (coal, oil_gas, all_minerals)")
    has_broad_form_deed: bool = Field(default=False)
    severance_date: Optional[str] = Field(default=None, description="Date of original mineral severance")
    proposed_operation: Optional[str] = Field(default=None, description="Proposed mining/extraction operation")


@app.post("/title-analysis")
async def title_analysis_guidance(request: ChainOfTitleRequest) -> Dict[str, Any]:
    """Generate mineral chain of title analysis guidance."""
    guidance: Dict[str, Any] = {
        "state": request.state.upper(),
        "mineral_type": request.mineral_type,
        "analysis_steps": [],
        "key_issues": [],
        "recommended_searches": [],
        "applicable_doctrines": [],
    }

    # Standard title examination steps
    guidance["analysis_steps"] = [
        "1. Obtain certified copies of all deeds in the chain of title from patent/sovereign to present",
        "2. Identify the original severance deed separating minerals from surface",
        "3. Trace all subsequent mineral conveyances, reservations, and exceptions",
        "4. Identify any fractional mineral interests and calculate net mineral acres",
        "5. Check for outstanding mineral leases, options, or encumbrances",
        "6. Verify payment of property taxes on mineral estate (dormant minerals acts)",
        "7. Check for adverse possession claims or prescriptive rights",
        "8. Review probate records for inherited mineral interests",
        "9. Check bankruptcy records for any mineral interests acquired by trustees",
        "10. Verify corporate succession for any corporate mineral owners",
    ]

    # State-specific considerations
    state_upper = request.state.upper()
    if state_upper in STATE_BROAD_FORM_DEED_DOCTRINE:
        bfd = STATE_BROAD_FORM_DEED_DOCTRINE[state_upper]
        guidance["applicable_doctrines"].append({
            "doctrine": "broad_form_deed",
            "state_rule": bfd["rule"],
            "key_case": bfd["key_case"],
        })

    if state_upper in STATE_CBM_OWNERSHIP:
        cbm = STATE_CBM_OWNERSHIP[state_upper]
        guidance["applicable_doctrines"].append({
            "doctrine": "cbm_ownership",
            "state_rule": cbm["rule"],
            "key_case": cbm["key_case"],
        })

    # Broad form deed issues
    if request.has_broad_form_deed:
        guidance["key_issues"].extend([
            "Broad form deed present — analyze exact conveyance language",
            f"Apply {state_upper} broad form deed doctrine to determine surface use rights",
            "Evaluate whether proposed extraction method was contemplated at time of severance",
            "Check for express surface damage waiver or compensation provisions",
        ])

    # Mineral-type-specific searches
    if request.mineral_type == "coal":
        guidance["recommended_searches"].extend([
            "Search for SMCRA permit history on the tract",
            "Check for outstanding reclamation obligations or bond forfeitures",
            "Verify coal severance tax payment history",
            "Search for acid mine drainage liens or environmental liens",
            "Check OSMRE Applicant Violator System (AVS) for permit block issues",
        ])
    elif request.mineral_type in ("oil_gas", "oil", "gas"):
        guidance["recommended_searches"].extend([
            "Search state oil and gas commission for well permits and production records",
            "Check for pooling or unitization orders affecting the tract",
            "Verify royalty payment history and any underpayment claims",
            "Search for orphan well designation or plugging obligations",
        ])
    elif request.mineral_type == "all_minerals":
        guidance["recommended_searches"].extend([
            "Determine which specific minerals are included in 'all minerals' grant",
            f"Apply {state_upper} mineral classification doctrine (surface substance vs mineral)",
            "Evaluate whether sand, gravel, limestone, and caliche are included",
            "Check for helium, CBM, and geothermal resource ownership under the grant",
        ])

    # Severance date analysis
    if request.severance_date:
        guidance["key_issues"].append(
            f"Original severance date: {request.severance_date} — analyze mineral rights "
            f"in context of mining technology and legal doctrine as of that date"
        )

    return guidance


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting LM22 {ENGINE_NAME} on port {ENGINE_PORT}")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )