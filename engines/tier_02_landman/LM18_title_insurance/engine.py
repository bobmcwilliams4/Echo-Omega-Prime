"""
LM18 Title Insurance Engine — Main Engine
==========================================
TIE Gold Standard intelligence engine for title insurance underwriting, policy analysis,
commitment review, endorsements, claims, rate regulation, and curative requirements.

Covers: Title commitment review, Schedule A/B-I/B-II analysis, owner's vs lender's policies,
ALTA endorsements (8.1 Environmental, 9 Comprehensive, 19 Contiguity), title plant/abstract search,
chain of title examination, title defect types (wild deed, forged deed, gaps, heirship, entity authority),
lien priority rules, mechanic's lien vs deed of trust priority, claims handling, rate regulation (TDI),
mineral reservation exceptions, curative requirements, escrow/closing procedures.

Engine: LM18 | Port: 8518 | Domain: title_insurance
Version: 1.0.0 | TIE Gold Standard | 20 Components

TIE-20 Components:
 1.  three_layer_response      2.  response_modes
 3.  doctrine_cache            4.  authority_hardening
 5.  confidence_stratification 6.  semantic_normalization
 7.  vector_search             8.  telemetry
 9.  drift_watcher            10.  coverage_map
11.  metrics_collector        12.  health_endpoint
13.  zoned_analysis           14.  fact_fragility_scoring
15.  audit_trail_jsonl        16.  determinism_hash_sha256
17.  fastapi_server           18.  loguru_logging
19.  multi_doctrine_decomposition
20.  deep_analysis_mode
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import traceback
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

# Add _shared to path for cloud_retriever access
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Cloud knowledge integration
# ---------------------------------------------------------------------------
try:
    from cloud_retriever import CognitionCloudRetriever, CloudKnowledge, retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
except ImportError:
    _CLOUD_AVAILABLE = False
    logger.warning("cloud_retriever not available — running without cloud knowledge")

# ---------------------------------------------------------------------------
# Local imports
# ---------------------------------------------------------------------------
from doctrines import (
    ConfidenceStratification,
    DoctrineBlock,
    DoctrineInteraction,
    IssueCategory,
    PositionZone,
    build_doctrine_cache,
    build_interaction_graph,
    find_doctrine_by_topic,
    find_doctrines_by_category,
    find_doctrines_by_keyword,
    get_doctrine_cache,
    get_interaction_graph,
    get_interactions_for_topic,
)
from search import SearchDocument, SearchResponse, VectorIndex, get_vector_index, initialize_index_from_doctrines
from semantic import NormalizationResult, SemanticNormalizer, get_normalizer
from telemetry import (
    ErrorDomain,
    QueryPhase,
    QueryTrace,
    TelemetryCollector,
    complete_trace,
    get_telemetry_collector,
    record_error,
    start_trace,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "LM18"
ENGINE_NAME = "Title Insurance"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8518
ENGINE_DOMAIN = "title_insurance"
ENGINE_DIR = Path(__file__).parent
CONFIG_PATH = ENGINE_DIR / "config.json"

# Logging configuration
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.remove()
logger.add(sys.stderr, level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{function}:{line} | {message}")
logger.add(
    LOG_DIR / "engine_{time:YYYY-MM-DD}.log",
    rotation="50 MB",
    retention="90 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} | {message}",
)

# Audit trail
AUDIT_TRAIL_PATH = LOG_DIR / "audit_trail.jsonl"

# ---------------------------------------------------------------------------
# Banned phrases (epistemic guardrails)
# ---------------------------------------------------------------------------
BANNED_PHRASES: list[str] = [
    "i think",
    "probably",
    "i believe",
    "in my opinion",
    "it seems like",
    "i would guess",
    "most likely",
    "i assume",
    "generally speaking",
    "it depends",
    "you should consult",
    "this is not legal advice",
    "i'm not a lawyer",
    "every situation is different",
]


# ===================================================================
# TIE COMPONENT 2: Response Modes
# ===================================================================
class ResponseMode(str, Enum):
    """Response modes for title insurance analysis."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


RESPONSE_MODE_CONFIG: dict[str, dict[str, Any]] = {
    "FAST": {"max_tokens": 800, "include_citations": False, "doctrine_depth": "summary"},
    "DEFENSE": {"max_tokens": 4000, "include_citations": True, "doctrine_depth": "full"},
    "MEMO": {"max_tokens": 12000, "include_citations": True, "doctrine_depth": "exhaustive"},
}


# ===================================================================
# TIE COMPONENT 13: Zoned Analysis
# ===================================================================
class AnalysisZone(str, Enum):
    """Analysis zones — PLANNING, REPORTING, AUDIT. Never blur."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


ZONE_GUIDELINES: dict[str, str] = {
    "PLANNING": (
        "Title insurance planning mode: evaluate insurability, identify required endorsements, "
        "recommend curative actions, estimate premiums. Forward-looking."
    ),
    "REPORTING": (
        "Title reporting mode: document current title status, commitment requirements, exceptions, "
        "policy coverage. Factual, current-state focus."
    ),
    "AUDIT": (
        "Audit mode: verify policy issuance compliance, commitment satisfaction, premium calculation, "
        "claims handling. Backward-looking review."
    ),
}


# ===================================================================
# Pydantic Request/Response Models
# ===================================================================
class TitleQuery(BaseModel):
    """Input query for title insurance analysis."""
    query: str
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    category_filter: Optional[str] = None
    include_interactions: bool = False
    include_fragility: bool = False
    client_id: str = ""


class AuthoritySource(BaseModel):
    """A cited authority source."""
    source: str
    weight: float = 1.0
    type: str = "statute"  # statute, case, regulation, standard


class ConfidenceAssessment(BaseModel):
    """Confidence assessment for title insurance opinion."""
    tier: str
    score: float
    reasoning: str
    disclosure_required: bool = False


class FragilityScore(BaseModel):
    """Fact fragility scoring for title insurance analysis."""
    verifiability: float = Field(ge=0.0, le=1.0)
    recharacterization_risk: float = Field(ge=0.0, le=1.0)
    testimony_dependence: float = Field(ge=0.0, le=1.0)
    overall_fragility: float = Field(ge=0.0, le=1.0)
    risk_factors: list[str] = Field(default_factory=list)


class DoctrineReference(BaseModel):
    """Reference to a triggered doctrine."""
    topic: str
    category: str
    confidence: str
    conclusion: str
    key_factors: list[str]
    authority_sources: list[AuthoritySource]


class TitleResponse(BaseModel):
    """Response from title insurance analysis."""
    query_id: str
    query: str
    mode: str
    zone: str
    conclusion: str
    reasoning: str
    doctrines_applied: list[DoctrineReference]
    confidence: ConfidenceAssessment
    fragility: Optional[FragilityScore] = None
    authority_sources: list[AuthoritySource]
    interactions: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    disclosure_caveat: Optional[str] = None
    determinism_hash: str
    response_time_ms: float
    cache_hit: bool = False
    cloud_enhanced: bool = False


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    engine_id: str
    engine_name: str
    version: str
    uptime_seconds: float
    doctrine_count: int
    total_queries: int
    cache_hit_rate: float
    avg_response_time_ms: float
    cloud_available: bool


class MetricsResponse(BaseModel):
    """Metrics endpoint response."""
    engine_id: str
    metrics: dict[str, Any]
    timestamp: str


class DoctrineListResponse(BaseModel):
    """Doctrine list response."""
    total_doctrines: int
    categories: dict[str, int]
    doctrines: list[dict[str, Any]]


class CoverageMapResponse(BaseModel):
    """Coverage map response showing doctrine triggering statistics."""
    total_doctrines: int
    triggered_count: int
    never_triggered_count: int
    triggered_doctrines: dict[str, int]
    coverage_percentage: float
    epistemic_gaps: list[str]


# ===================================================================
# TIE COMPONENT 14: Fact Fragility Scoring
# ===================================================================
def calculate_fragility(query: str, doctrines: list[DoctrineBlock]) -> FragilityScore:
    """
    Calculate fact fragility score for title insurance analysis.

    Args:
        query: User query
        doctrines: Applied doctrine blocks

    Returns:
        FragilityScore with risk assessment
    """
    # Verifiability: Can facts be verified by public records?
    verifiable_indicators = ["recorded", "filed", "deed", "mortgage", "lien", "survey", "plat", "schedule"]
    unverifiable_indicators = ["oral", "unrecorded", "verbal agreement", "understanding", "intended"]

    verifiable_count = sum(1 for ind in verifiable_indicators if ind in query.lower())
    unverifiable_count = sum(1 for ind in unverifiable_indicators if ind in query.lower())

    verifiability = min(1.0, verifiable_count / 3) - (unverifiable_count * 0.2)
    verifiability = max(0.0, min(1.0, verifiability))

    # Recharacterization risk: Can facts be interpreted differently?
    ambiguous_terms = ["may", "could", "might", "unclear", "disputed", "alleged", "claimed"]
    ambiguous_count = sum(1 for term in ambiguous_terms if term in query.lower())
    recharacterization_risk = min(1.0, ambiguous_count * 0.25)

    # Testimony dependence: Does analysis rely on witness statements vs documents?
    testimony_indicators = ["stated", "testified", "affidavit", "sworn statement", "witness"]
    testimony_count = sum(1 for ind in testimony_indicators if ind in query.lower())
    testimony_dependence = min(1.0, testimony_count * 0.3)

    # Overall fragility (higher = more fragile)
    overall_fragility = (
        (1.0 - verifiability) * 0.4 +
        recharacterization_risk * 0.3 +
        testimony_dependence * 0.3
    )

    risk_factors = []
    if verifiability < 0.5:
        risk_factors.append("Low verifiability - facts not easily confirmed by public records")
    if recharacterization_risk > 0.5:
        risk_factors.append("High recharacterization risk - ambiguous or disputed facts")
    if testimony_dependence > 0.5:
        risk_factors.append("High testimony dependence - relies on witness statements vs documents")
    if any("wild deed" in d.topic for d in doctrines):
        risk_factors.append("Wild deed risk - deed from stranger to title")
    if any("forged" in d.topic for d in doctrines):
        risk_factors.append("Forgery risk - signature authenticity questioned")
    if any("gap" in d.topic for d in doctrines):
        risk_factors.append("Gap in title - missing link in chain")

    return FragilityScore(
        verifiability=round(verifiability, 3),
        recharacterization_risk=round(recharacterization_risk, 3),
        testimony_dependence=round(testimony_dependence, 3),
        overall_fragility=round(overall_fragility, 3),
        risk_factors=risk_factors
    )


# ===================================================================
# TIE COMPONENT 4: Authority Hardening
# ===================================================================
def load_authority_hierarchy() -> list[dict[str, Any]]:
    """Load authority hierarchy from config."""
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r") as f:
            config = json.load(f)
        return config.get("authority_hierarchy", [])
    return []


AUTHORITY_HIERARCHY = load_authority_hierarchy()


def resolve_authority_conflict(sources: list[str]) -> AuthoritySource:
    """
    Resolve conflict between multiple authority sources.

    Args:
        sources: List of authority source names

    Returns:
        Highest-weighted authority source
    """
    hierarchy_map = {item["source"]: item for item in AUTHORITY_HIERARCHY}

    best_source = None
    best_weight = 0.0

    for source_name in sources:
        for hier_source_name, hier_data in hierarchy_map.items():
            if hier_source_name in source_name.lower() or source_name.lower() in hier_source_name:
                if hier_data["weight"] > best_weight:
                    best_weight = hier_data["weight"]
                    best_source = source_name
                    break

    if best_source:
        return AuthoritySource(source=best_source, weight=best_weight, type="statute")
    else:
        return AuthoritySource(source=sources[0] if sources else "unknown", weight=0.5, type="unknown")


# ===================================================================
# TIE COMPONENT 10: Coverage Map
# ===================================================================
class CoverageMap:
    """Track which doctrines are triggered and identify epistemic gaps."""

    def __init__(self):
        self.triggered_counts: dict[str, int] = defaultdict(int)
        self.total_queries = 0

    def record_trigger(self, doctrine_topic: str) -> None:
        """Record that a doctrine was triggered."""
        self.triggered_counts[doctrine_topic] += 1

    def increment_query_count(self) -> None:
        """Increment total query count."""
        self.total_queries += 1

    def get_coverage_report(self) -> CoverageMapResponse:
        """Generate coverage map report."""
        all_doctrines = get_doctrine_cache()
        total = len(all_doctrines)
        triggered = len(self.triggered_counts)
        never_triggered = total - triggered

        coverage_pct = (triggered / total * 100) if total > 0 else 0.0

        # Identify epistemic gaps (never-triggered doctrines)
        all_topics = {d.topic for d in all_doctrines}
        triggered_topics = set(self.triggered_counts.keys())
        never_triggered_topics = all_topics - triggered_topics

        epistemic_gaps = list(never_triggered_topics)

        return CoverageMapResponse(
            total_doctrines=total,
            triggered_count=triggered,
            never_triggered_count=never_triggered,
            triggered_doctrines=dict(self.triggered_counts),
            coverage_percentage=round(coverage_pct, 2),
            epistemic_gaps=epistemic_gaps
        )


_COVERAGE_MAP = CoverageMap()


# ===================================================================
# TIE COMPONENT 16: Determinism Hash (SHA-256)
# ===================================================================
def compute_determinism_hash(query: str, doctrines: list[DoctrineBlock], mode: str, zone: str) -> str:
    """
    Compute SHA-256 hash for query reproducibility.

    Args:
        query: User query
        doctrines: Applied doctrines
        mode: Response mode
        zone: Analysis zone

    Returns:
        SHA-256 hash (hex)
    """
    hash_input = {
        "query": query.lower().strip(),
        "doctrines": sorted([d.topic for d in doctrines]),
        "mode": mode,
        "zone": zone,
        "engine_version": ENGINE_VERSION,
    }

    hash_string = json.dumps(hash_input, sort_keys=True)
    return hashlib.sha256(hash_string.encode()).hexdigest()


# ===================================================================
# TIE COMPONENT 15: Audit Trail (JSONL)
# ===================================================================
def write_audit_trail(query_id: str, query: str, response: TitleResponse) -> None:
    """
    Write query and response to audit trail.

    Args:
        query_id: Unique query identifier
        query: User query
        response: Title response
    """
    audit_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query_id": query_id,
        "query": query,
        "mode": response.mode,
        "zone": response.zone,
        "conclusion": response.conclusion,
        "doctrines_applied": [d.topic for d in response.doctrines_applied],
        "confidence_tier": response.confidence.tier,
        "determinism_hash": response.determinism_hash,
        "response_time_ms": response.response_time_ms,
    }

    with AUDIT_TRAIL_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(audit_entry) + "\n")


# ===================================================================
# TIE COMPONENT 19: Multi-Doctrine Decomposition
# ===================================================================
def decompose_query(query: str) -> dict[str, Any]:
    """
    Decompose query into issue categories and identify doctrine interactions.

    Args:
        query: User query

    Returns:
        Decomposition analysis
    """
    query_lower = query.lower()

    # Identify categories
    categories = []
    if any(term in query_lower for term in ["commitment", "schedule a", "schedule b", "preliminary report"]):
        categories.append(IssueCategory.COMMITMENT_REVIEW)
    if any(term in query_lower for term in ["owner's policy", "lender's policy", "coverage", "insured"]):
        categories.append(IssueCategory.POLICY_COVERAGE)
    if any(term in query_lower for term in ["endorsement", "alta", "8.1", "9", "19"]):
        categories.append(IssueCategory.ENDORSEMENT_ANALYSIS)
    if any(term in query_lower for term in ["lien", "mortgage", "deed of trust", "priority", "mechanic"]):
        categories.append(IssueCategory.LIEN_ANALYSIS)
    if any(term in query_lower for term in ["mineral", "royalty", "surface", "executive rights"]):
        categories.append(IssueCategory.MINERAL_EXCLUSION)
    if any(term in query_lower for term in ["claim", "loss", "coverage", "duty to defend"]):
        categories.append(IssueCategory.CLAIMS_LOSS)
    if any(term in query_lower for term in ["premium", "rate", "tdi", "promulgated", "simultaneous issue"]):
        categories.append(IssueCategory.RATE_REGULATION)
    if any(term in query_lower for term in ["curative", "corrective deed", "affidavit", "quiet title"]):
        categories.append(IssueCategory.CURATIVE_REQUIREMENTS)

    if not categories:
        categories.append(IssueCategory.POLICY_COVERAGE)  # Default

    # Identify strata (complexity levels)
    strata = []
    if len(query_lower.split()) < 10:
        strata.append("SIMPLE")
    elif len(query_lower.split()) < 30:
        strata.append("MODERATE")
    else:
        strata.append("COMPLEX")

    if any(term in query_lower for term in ["and", "also", "additionally", "furthermore"]):
        strata.append("MULTI_ISSUE")

    return {
        "categories": [cat.value for cat in categories],
        "strata": strata,
        "category_count": len(categories),
    }


# ===================================================================
# TIE COMPONENT 1: Three-Layer Response
# ===================================================================
def three_layer_response(
    query: str,
    mode: ResponseMode,
    zone: AnalysisZone,
    category_filter: Optional[str],
    trace: QueryTrace
) -> TitleResponse:
    """
    Execute three-layer response: doctrine cache → vector search → deep analysis.

    Args:
        query: User query
        mode: Response mode
        zone: Analysis zone
        category_filter: Optional category filter
        trace: Query trace for telemetry

    Returns:
        TitleResponse with analysis result
    """
    start_time = time.time()

    # Layer 1: Doctrine Cache (0-200ms)
    normalizer = get_normalizer()
    norm_result = normalizer.normalize(query)
    trace.add_phase(QueryPhase.NORMALIZED, (time.time() - start_time) * 1000)

    cache_start = time.time()
    cache_doctrines = find_doctrines_by_keyword(norm_result.normalized)
    if category_filter:
        try:
            cat_enum = IssueCategory(category_filter)
            cache_doctrines = [d for d in cache_doctrines if d.category == cat_enum]
        except ValueError:
            pass

    cache_hit = len(cache_doctrines) > 0
    trace.cache_hit = cache_hit
    trace.add_phase(QueryPhase.CACHE_LOOKUP, (time.time() - cache_start) * 1000, metadata={"hit": cache_hit, "count": len(cache_doctrines)})

    applied_doctrines = cache_doctrines[:3] if cache_doctrines else []

    # Layer 2: Vector Search (200-500ms fallback)
    if not cache_hit:
        vector_start = time.time()
        index = get_vector_index()
        if index.model_available:
            search_response = index.search(
                query=norm_result.normalized,
                top_k=3,
                similarity_threshold=0.72,
                category_filter=category_filter
            )
            trace.vector_search_used = True
            trace.add_phase(QueryPhase.VECTOR_SEARCH, (time.time() - vector_start) * 1000, metadata={"results": len(search_response.results)})

            # Retrieve doctrines from search results
            for doc in search_response.results:
                doctrine = find_doctrine_by_topic(doc.metadata.get("topic", ""))
                if doctrine:
                    applied_doctrines.append(doctrine)

    # Layer 3: Cloud Retrieval (optional deep enhancement)
    cloud_enhanced = False
    if _CLOUD_AVAILABLE and len(applied_doctrines) < 2:
        cloud_start = time.time()
        try:
            cloud_knowledge = retrieve_cloud_knowledge(query, domain="title_insurance", max_results=2)
            if cloud_knowledge:
                cloud_enhanced = True
                trace.cloud_retrieval_used = True
                trace.add_phase(QueryPhase.CLOUD_RETRIEVAL, (time.time() - cloud_start) * 1000, metadata={"results": len(cloud_knowledge)})
        except Exception as e:
            logger.warning(f"Cloud retrieval failed: {e}")

    # If no doctrines found, use fallback
    if not applied_doctrines:
        all_doctrines = get_doctrine_cache()
        applied_doctrines = all_doctrines[:2]  # Fallback to first 2 doctrines

    # Record doctrine triggering for coverage map
    for doctrine in applied_doctrines:
        _COVERAGE_MAP.record_trigger(doctrine.topic)
        trace.doctrines_triggered.append(doctrine.topic)

    _COVERAGE_MAP.increment_query_count()

    # Build response
    response_start = time.time()
    conclusion_parts = []
    reasoning_parts = []
    all_authorities = []
    recommendations = []

    for doctrine in applied_doctrines:
        # Select conclusion template
        conclusion_template = doctrine.conclusion_templates[0] if doctrine.conclusion_templates else "Analysis based on {topic}."
        try:
            conclusion_parts.append(conclusion_template.format(topic=doctrine.topic.replace("_", " ")))
        except (KeyError, ValueError, IndexError):
            # Template has placeholders beyond {topic} — use raw template
            conclusion_parts.append(conclusion_template.replace("{", "").replace("}", ""))

        # Add reasoning framework excerpt
        reasoning_excerpt = doctrine.reasoning_framework[:500] if len(doctrine.reasoning_framework) > 500 else doctrine.reasoning_framework
        reasoning_parts.append(f"**{doctrine.topic.replace('_', ' ').title()}:** {reasoning_excerpt}")

        # Collect authorities
        for auth in doctrine.primary_authority:
            all_authorities.append(AuthoritySource(source=auth, weight=0.9, type="statute"))

        # Generate recommendations based on doctrine
        if doctrine.resolution_strategy:
            recommendations.append(doctrine.resolution_strategy[:200])

    conclusion = " ".join(conclusion_parts)
    reasoning = "\n\n".join(reasoning_parts)

    # Resolve authority conflicts
    if all_authorities:
        primary_authority = resolve_authority_conflict([a.source for a in all_authorities])
        all_authorities.insert(0, primary_authority)

    # Confidence assessment
    if applied_doctrines:
        confidence_tier = applied_doctrines[0].confidence.value
        confidence_score = 0.95 if confidence_tier == "DEFENSIBLE" else 0.85 if confidence_tier == "AGGRESSIVE" else 0.75
    else:
        confidence_tier = "DISCLOSURE"
        confidence_score = 0.6

    confidence = ConfidenceAssessment(
        tier=confidence_tier,
        score=confidence_score,
        reasoning=f"Analysis based on {len(applied_doctrines)} doctrine(s) with {confidence_tier} confidence tier.",
        disclosure_required=(confidence_tier in ["DISCLOSURE", "HIGH_RISK"])
    )

    # Fragility scoring
    fragility = calculate_fragility(query, applied_doctrines)

    # Doctrine references
    doctrine_refs = []
    for doctrine in applied_doctrines:
        doctrine_refs.append(DoctrineReference(
            topic=doctrine.topic,
            category=doctrine.category.value,
            confidence=doctrine.confidence.value,
            conclusion=doctrine.conclusion_templates[0] if doctrine.conclusion_templates else "",
            key_factors=doctrine.key_factors[:5],
            authority_sources=[AuthoritySource(source=a, weight=0.9) for a in doctrine.primary_authority[:3]]
        ))

    # Interactions
    interactions = []
    if len(applied_doctrines) > 1:
        for doctrine in applied_doctrines:
            doctrine_interactions = get_interactions_for_topic(doctrine.topic)
            for interaction in doctrine_interactions:
                interactions.append(f"{interaction.interaction_type}: {interaction.topic_a} ↔ {interaction.topic_b}")

    # Determinism hash
    determinism_hash = compute_determinism_hash(query, applied_doctrines, mode.value, zone.value)

    # Disclosure caveat
    disclosure_caveat = None
    if confidence.disclosure_required:
        disclosure_caveat = "This analysis is preliminary and should be reviewed by legal counsel before reliance for underwriting or policy issuance."

    trace.add_phase(QueryPhase.RESPONSE_BUILT, (time.time() - response_start) * 1000)

    response_time_ms = (time.time() - start_time) * 1000

    response = TitleResponse(
        query_id=trace.trace_id,
        query=query,
        mode=mode.value,
        zone=zone.value,
        conclusion=conclusion,
        reasoning=reasoning,
        doctrines_applied=doctrine_refs,
        confidence=confidence,
        fragility=fragility,
        authority_sources=all_authorities[:5],
        interactions=interactions[:5],
        recommendations=recommendations[:3],
        disclosure_caveat=disclosure_caveat,
        determinism_hash=determinism_hash,
        response_time_ms=round(response_time_ms, 2),
        cache_hit=cache_hit,
        cloud_enhanced=cloud_enhanced
    )

    trace.confidence_tier = confidence_tier
    trace.response_tokens = len(conclusion.split()) + len(reasoning.split())

    return response


# ===================================================================
# TIE COMPONENT 20: Deep Analysis Mode
# ===================================================================
def deep_analysis_mode(query: str, zone: AnalysisZone, trace: QueryTrace) -> TitleResponse:
    """
    Deep analysis mode: exhaustive multi-source synthesis.

    Args:
        query: User query
        zone: Analysis zone
        trace: Query trace

    Returns:
        TitleResponse with exhaustive analysis
    """
    logger.info(f"Deep analysis mode triggered for query: {query[:50]}")

    # Decompose query
    decomposition = decompose_query(query)
    trace.add_phase(QueryPhase.DEEP_ANALYSIS, 0.0, metadata=decomposition)

    # Gather all relevant doctrines from all identified categories
    all_doctrines = []
    for category_str in decomposition["categories"]:
        try:
            category = IssueCategory(category_str)
            category_doctrines = find_doctrines_by_category(category)
            all_doctrines.extend(category_doctrines)
        except ValueError:
            pass

    # Deduplicate
    seen_topics = set()
    unique_doctrines = []
    for doctrine in all_doctrines:
        if doctrine.topic not in seen_topics:
            unique_doctrines.append(doctrine)
            seen_topics.add(doctrine.topic)

    # Limit to top 5 for deep analysis
    applied_doctrines = unique_doctrines[:5]

    # Build exhaustive response
    conclusion_parts = []
    reasoning_parts = []
    all_authorities = []
    recommendations = []
    interactions = []

    for doctrine in applied_doctrines:
        _COVERAGE_MAP.record_trigger(doctrine.topic)
        trace.doctrines_triggered.append(doctrine.topic)

        # Full conclusion
        for template in doctrine.conclusion_templates[:2]:
            try:
                conclusion_parts.append(template.format(topic=doctrine.topic.replace("_", " ")))
            except (KeyError, ValueError, IndexError):
                conclusion_parts.append(template.replace("{", "").replace("}", ""))

        # Full reasoning framework
        reasoning_parts.append(f"## {doctrine.topic.replace('_', ' ').title()}\n\n{doctrine.reasoning_framework}")

        # All authorities
        for auth in doctrine.primary_authority:
            all_authorities.append(AuthoritySource(source=auth, weight=0.9, type="statute"))

        # Resolution strategy as recommendation
        if doctrine.resolution_strategy:
            recommendations.append(f"{doctrine.topic.replace('_', ' ').title()}: {doctrine.resolution_strategy}")

        # Interactions
        doctrine_interactions = get_interactions_for_topic(doctrine.topic)
        for interaction in doctrine_interactions:
            interactions.append(f"{interaction.interaction_type}: {interaction.topic_a} ↔ {interaction.topic_b} — {interaction.resolution_rule}")

    conclusion = " ".join(conclusion_parts)
    reasoning = "\n\n".join(reasoning_parts)

    # Confidence
    confidence_tier = ConfidenceStratification.DEFENSIBLE.value
    confidence_score = 0.95

    confidence = ConfidenceAssessment(
        tier=confidence_tier,
        score=confidence_score,
        reasoning=f"Deep analysis across {len(applied_doctrines)} doctrines in {len(decomposition['categories'])} categories.",
        disclosure_required=False
    )

    # Fragility
    fragility = calculate_fragility(query, applied_doctrines)

    # Doctrine refs
    doctrine_refs = []
    for doctrine in applied_doctrines:
        doctrine_refs.append(DoctrineReference(
            topic=doctrine.topic,
            category=doctrine.category.value,
            confidence=doctrine.confidence.value,
            conclusion=" ".join(doctrine.conclusion_templates[:2]),
            key_factors=doctrine.key_factors,
            authority_sources=[AuthoritySource(source=a, weight=0.9) for a in doctrine.primary_authority]
        ))

    # Determinism hash
    determinism_hash = compute_determinism_hash(query, applied_doctrines, ResponseMode.MEMO.value, zone.value)

    response_time_ms = sum(p.duration_ms for p in trace.phases)

    response = TitleResponse(
        query_id=trace.trace_id,
        query=query,
        mode=ResponseMode.MEMO.value,
        zone=zone.value,
        conclusion=conclusion,
        reasoning=reasoning,
        doctrines_applied=doctrine_refs,
        confidence=confidence,
        fragility=fragility,
        authority_sources=all_authorities[:10],
        interactions=interactions,
        recommendations=recommendations,
        disclosure_caveat=None,
        determinism_hash=determinism_hash,
        response_time_ms=round(response_time_ms, 2),
        cache_hit=False,
        cloud_enhanced=False
    )

    trace.confidence_tier = confidence_tier
    trace.response_tokens = len(conclusion.split()) + len(reasoning.split())

    return response


# ===================================================================
# TIE COMPONENT 9: Drift Watcher
# ===================================================================
class DriftWatcher:
    """Monitor doctrine drift over time."""

    def __init__(self):
        self.baseline_hashes: dict[str, str] = {}
        self.drift_detected: dict[str, bool] = {}

    def set_baseline(self, doctrines: list[DoctrineBlock]) -> None:
        """Set baseline hashes for doctrines."""
        for doctrine in doctrines:
            doctrine_str = json.dumps({
                "topic": doctrine.topic,
                "reasoning_framework": doctrine.reasoning_framework,
                "key_factors": doctrine.key_factors,
                "primary_authority": doctrine.primary_authority,
            }, sort_keys=True)
            self.baseline_hashes[doctrine.topic] = hashlib.sha256(doctrine_str.encode()).hexdigest()

    def check_drift(self, doctrines: list[DoctrineBlock]) -> dict[str, bool]:
        """Check for drift from baseline."""
        for doctrine in doctrines:
            doctrine_str = json.dumps({
                "topic": doctrine.topic,
                "reasoning_framework": doctrine.reasoning_framework,
                "key_factors": doctrine.key_factors,
                "primary_authority": doctrine.primary_authority,
            }, sort_keys=True)
            current_hash = hashlib.sha256(doctrine_str.encode()).hexdigest()

            if doctrine.topic in self.baseline_hashes:
                self.drift_detected[doctrine.topic] = (current_hash != self.baseline_hashes[doctrine.topic])
            else:
                self.drift_detected[doctrine.topic] = False

        return self.drift_detected


_DRIFT_WATCHER = DriftWatcher()


# ===================================================================
# FastAPI Lifespan
# ===================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager for startup/shutdown."""
    # Startup
    logger.info(f"Starting {ENGINE_NAME} Engine v{ENGINE_VERSION} on port {ENGINE_PORT}")

    # Build doctrine cache
    doctrines = build_doctrine_cache()
    logger.info(f"Doctrine cache built: {len(doctrines)} doctrines")

    # Build interaction graph
    interactions = build_interaction_graph()
    logger.info(f"Interaction graph built: {len(interactions)} interactions")

    # Initialize vector index
    initialize_index_from_doctrines(doctrines)
    logger.info("Vector index initialized")

    # Set drift baseline
    _DRIFT_WATCHER.set_baseline(doctrines)
    logger.info("Drift watcher baseline set")

    # Initialize telemetry
    telemetry = get_telemetry_collector(engine_id=ENGINE_ID)
    logger.info("Telemetry collector initialized")

    app.state.start_time = time.time()

    yield

    # Shutdown
    logger.info("Shutting down Title Insurance Engine")
    telemetry.flush()


# ===================================================================
# TIE COMPONENT 17: FastAPI Server
# ===================================================================
app = FastAPI(
    title=f"{ENGINE_NAME} Engine",
    description="TIE Gold Standard title insurance intelligence engine",
    version=ENGINE_VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===================================================================
# TIE COMPONENT 12: Health Endpoint
# ===================================================================
@app.get("/health", response_model=HealthResponse)
async def health_check(request: Request):
    """Health check endpoint."""
    telemetry = get_telemetry_collector()
    metrics = telemetry.get_metrics()

    uptime = time.time() - request.app.state.start_time

    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=ENGINE_VERSION,
        uptime_seconds=round(uptime, 2),
        doctrine_count=len(get_doctrine_cache()),
        total_queries=metrics["total_queries"],
        cache_hit_rate=metrics["cache_hit_rate"],
        avg_response_time_ms=metrics["avg_duration_ms"],
        cloud_available=_CLOUD_AVAILABLE
    )


# ===================================================================
# Main Query Endpoint
# ===================================================================
@app.post("/query", response_model=TitleResponse)
async def query_endpoint(query_input: TitleQuery):
    """
    Main query endpoint for title insurance analysis.

    Args:
        query_input: TitleQuery with query text and parameters

    Returns:
        TitleResponse with analysis result
    """
    telemetry = get_telemetry_collector()
    trace = start_trace(
        query=query_input.query,
        mode=query_input.mode.value,
        zone=query_input.zone.value,
        client_id=query_input.client_id
    )

    try:
        # Detect if deep analysis needed
        decomposition = decompose_query(query_input.query)
        use_deep_analysis = (
            query_input.mode == ResponseMode.MEMO or
            decomposition["category_count"] > 2 or
            "COMPLEX" in decomposition["strata"]
        )

        if use_deep_analysis:
            response = deep_analysis_mode(query_input.query, query_input.zone, trace)
        else:
            response = three_layer_response(
                query=query_input.query,
                mode=query_input.mode,
                zone=query_input.zone,
                category_filter=query_input.category_filter,
                trace=trace
            )

        # Write audit trail
        write_audit_trail(trace.trace_id, query_input.query, response)

        complete_trace(trace)

        return response

    except Exception as e:
        logger.error(f"Query failed: {e}\n{traceback.format_exc()}")
        record_error(trace, ErrorDomain.INVALID_INPUT, str(e))
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(e))


# ===================================================================
# TIE COMPONENT 11: Metrics Collector Endpoint
# ===================================================================
@app.get("/metrics", response_model=MetricsResponse)
async def metrics_endpoint():
    """Get engine performance metrics."""
    telemetry = get_telemetry_collector()
    metrics = telemetry.get_metrics()

    return MetricsResponse(
        engine_id=ENGINE_ID,
        metrics=metrics,
        timestamp=datetime.now(timezone.utc).isoformat()
    )


# ===================================================================
# Doctrines Endpoint
# ===================================================================
@app.get("/doctrines", response_model=DoctrineListResponse)
async def doctrines_endpoint(category: Optional[str] = Query(None)):
    """List all doctrines, optionally filtered by category."""
    doctrines = get_doctrine_cache()

    if category:
        try:
            cat_enum = IssueCategory(category)
            doctrines = find_doctrines_by_category(cat_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

    # Count by category
    category_counts = defaultdict(int)
    for doctrine in get_doctrine_cache():
        category_counts[doctrine.category.value] += 1

    doctrine_dicts = []
    for doctrine in doctrines:
        doctrine_dicts.append({
            "topic": doctrine.topic,
            "category": doctrine.category.value,
            "confidence": doctrine.confidence.value,
            "keywords": doctrine.keywords,
            "primary_authority": doctrine.primary_authority[:3],
        })

    return DoctrineListResponse(
        total_doctrines=len(doctrines),
        categories=dict(category_counts),
        doctrines=doctrine_dicts
    )


# ===================================================================
# TIE COMPONENT 10: Coverage Map Endpoint
# ===================================================================
@app.get("/coverage", response_model=CoverageMapResponse)
async def coverage_endpoint():
    """Get doctrine coverage map showing triggering statistics."""
    return _COVERAGE_MAP.get_coverage_report()


# ===================================================================
# Drift Check Endpoint
# ===================================================================
@app.get("/drift")
async def drift_check_endpoint():
    """Check for doctrine drift from baseline."""
    doctrines = get_doctrine_cache()
    drift_status = _DRIFT_WATCHER.check_drift(doctrines)

    drifted_topics = [topic for topic, drifted in drift_status.items() if drifted]

    return {
        "total_doctrines": len(doctrines),
        "drifted_count": len(drifted_topics),
        "drifted_topics": drifted_topics,
        "drift_detected": len(drifted_topics) > 0
    }


# ===================================================================
# Main Entry Point
# ===================================================================
if __name__ == "__main__":
    import uvicorn

    logger.info(f"Launching {ENGINE_NAME} Engine on port {ENGINE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")