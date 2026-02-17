"""
LM16 Wind/Solar Lease Intelligence Engine
==========================================
TIE Gold Standard engine for renewable energy land acquisition:
wind and solar lease negotiation, structure analysis, royalty
calculations, surface use conflicts, tax incentive analysis,
and landowner protection.

Engine: LM16 | Port: 8516 | Version: 1.0.0

TIE-20 Components:
  1.  three_layer_response
  2.  response_modes (FAST, DEFENSE, MEMO)
  3.  doctrine_cache (32+ blocks)
  4.  authority_hardening
  5.  confidence_stratification
  6.  semantic_normalization
  7.  vector_search
  8.  telemetry
  9.  drift_watcher
  10. coverage_map
  11. metrics_collector
  12. health_endpoint
  13. zoned_analysis
  14. fact_fragility_scoring
  15. audit_trail_jsonl
  16. determinism_hash_sha256
  17. fastapi_server
  18. loguru_logging
  19. multi_doctrine_decomposition
  20. deep_analysis_mode
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import sys
import time
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

# Ensure _shared is in path for cloud_retriever
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Local imports
# ---------------------------------------------------------------------------
from doctrines import (
    DoctrineBlock,
    ConfidenceLevel,
    IssueCategory,
    EntityScope,
    BurdenHolder,
    INTERACTION_GRAPH,
    build_doctrine_cache,
)
from semantic import (
    ConceptDomain,
    NormalizedQuery,
    SemanticNormalizer,
    get_normalizer,
)
from search import (
    BM25SearchEngine,
    IndexedDocument,
    SearchResponse,
    SearchResult,
    get_search_engine,
)
from telemetry import (
    DriftObservation,
    ErrorDomain,
    HealthReport,
    LatencyTimer,
    MetricsSnapshot,
    QueryTrace,
    QueryTier,
    ResponseMode,
    TelemetryCollector,
    get_collector,
)

# Cloud retriever integration
try:
    from cloud_retriever import CognitionCloudRetriever, CloudKnowledge, retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
except ImportError:
    _CLOUD_AVAILABLE = False
    logger.warning("cloud_retriever not available — running without cloud knowledge")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID: str = "LM16"
ENGINE_NAME: str = "Wind/Solar Lease Intelligence Engine"
ENGINE_VERSION: str = "1.0.0"
ENGINE_PORT: int = 8516
ENGINE_DIR: Path = Path(__file__).parent

BANNED_PHRASES: list[str] = [
    "this is not legal advice",
    "consult an attorney",
    "I'm not a lawyer",
    "this is for informational purposes only",
    "you should seek professional advice",
    "this does not constitute legal advice",
    "disclaimer",
]

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------
LOG_DIR: Path = ENGINE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>LM16</cyan> | {message}",
)
logger.add(
    LOG_DIR / "engine.log",
    level="DEBUG",
    rotation="10 MB",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {message}",
)


# ---------------------------------------------------------------------------
# Pydantic Models — Request / Response
# ---------------------------------------------------------------------------
class AnalysisZone(str, Enum):
    """Analysis zones for position separation."""
    NEGOTIATION = "NEGOTIATION"
    DUE_DILIGENCE = "DUE_DILIGENCE"
    COMPLIANCE = "COMPLIANCE"
    DISPUTE = "DISPUTE"


class QueryRequest(BaseModel):
    """Incoming query request."""
    query: str = Field(..., min_length=5, max_length=5000, description="The lease analysis query")
    mode: str = Field(default="FAST", description="Response mode: FAST, DEFENSE, or MEMO")
    zone: str = Field(default="NEGOTIATION", description="Analysis zone")
    entity_perspective: str = Field(default="landowner", description="Perspective entity")
    max_doctrines: int = Field(default=5, ge=1, le=20, description="Max doctrine blocks to return")
    include_authorities: bool = Field(default=True, description="Include authority citations")
    include_counter_arguments: bool = Field(default=True, description="Include counter-arguments")
    deep_analysis: bool = Field(default=False, description="Enable deep analysis mode")


class AuthorityCitation(BaseModel):
    """A single authority citation with weight."""
    citation: str
    authority_type: str = "primary"
    weight: float = 1.0
    jurisdiction: str = "Texas"


class DoctrineMatch(BaseModel):
    """A matched doctrine block in the response."""
    topic: str
    confidence: str
    confidence_score: float
    conclusion: str
    reasoning: str
    key_factors: list[str]
    authorities: list[AuthorityCitation]
    burden_holder: str
    adversary_position: str
    counter_arguments: list[str]
    resolution_strategy: str
    fragility_score: float
    issue_category: str
    interaction_edges: list[str]


class DecompositionNode(BaseModel):
    """A node in the multi-doctrine decomposition."""
    issue_category: str
    doctrines: list[str]
    strata: str = ""
    dependencies: list[str] = Field(default_factory=list)
    resolution_order: int = 0


class AnalysisResponse(BaseModel):
    """Complete analysis response."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    query: str
    mode: str
    zone: str
    entity_perspective: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    determinism_hash: str = ""
    tier_used: str = ""
    latency_ms: float = 0.0
    confidence_level: str = ""
    confidence_score: float = 0.0
    doctrines_matched: list[DoctrineMatch] = Field(default_factory=list)
    decomposition: list[DecompositionNode] = Field(default_factory=list)
    deep_analysis: Optional[str] = None
    epistemic_warnings: list[str] = Field(default_factory=list)
    coverage_gaps: list[str] = Field(default_factory=list)
    search_fallback_used: bool = False
    trace_id: str = Field(default_factory=lambda: uuid4().hex[:16])
    cloud_knowledge: dict[str, Any] = Field(default_factory=dict)
    cloud_citations: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Authority Hardening
# ---------------------------------------------------------------------------
AUTHORITY_WEIGHTS: dict[str, float] = {
    "constitution": 1.0,
    "statute": 0.95,
    "supreme_court": 0.90,
    "appellate_court": 0.80,
    "regulation": 0.75,
    "irs_notice": 0.70,
    "revenue_ruling": 0.70,
    "ercot_protocol": 0.65,
    "puct_rule": 0.65,
    "industry_standard": 0.50,
    "model_lease": 0.45,
    "guidance": 0.40,
    "commentary": 0.30,
}


def classify_authority(citation: str) -> tuple[str, float]:
    """Classify an authority citation and assign weight."""
    citation_lower = citation.lower()
    if "constitution" in citation_lower or "const." in citation_lower:
        return "constitution", AUTHORITY_WEIGHTS["constitution"]
    if any(x in citation_lower for x in ["u.s.c.", "irc sec", "tex. tax code", "tex. property code",
                                           "tex. natural resources", "tex. utilities code",
                                           "tex. local government", "tex. estates code",
                                           "pub. l."]):
        return "statute", AUTHORITY_WEIGHTS["statute"]
    if "tex. 19" in citation_lower or "tex. 20" in citation_lower or "s.w.2d" in citation_lower or "s.w.3d" in citation_lower:
        return "supreme_court", AUTHORITY_WEIGHTS["supreme_court"]
    if "t.c. memo" in citation_lower or "t.c." in citation_lower:
        return "appellate_court", AUTHORITY_WEIGHTS["appellate_court"]
    if "cfr" in citation_lower or "reg." in citation_lower:
        return "regulation", AUTHORITY_WEIGHTS["regulation"]
    if "notice" in citation_lower:
        return "irs_notice", AUTHORITY_WEIGHTS["irs_notice"]
    if "rev. rul" in citation_lower or "rev. proc" in citation_lower:
        return "revenue_ruling", AUTHORITY_WEIGHTS["revenue_ruling"]
    if "ercot" in citation_lower:
        return "ercot_protocol", AUTHORITY_WEIGHTS["ercot_protocol"]
    if "puct" in citation_lower:
        return "puct_rule", AUTHORITY_WEIGHTS["puct_rule"]
    if any(x in citation_lower for x in ["nfpa", "ansi", "iec", "ul "]):
        return "industry_standard", AUTHORITY_WEIGHTS["industry_standard"]
    if "model" in citation_lower or "awea" in citation_lower or "seia" in citation_lower:
        return "model_lease", AUTHORITY_WEIGHTS["model_lease"]
    if "guidance" in citation_lower or "guide" in citation_lower:
        return "guidance", AUTHORITY_WEIGHTS["guidance"]
    return "commentary", AUTHORITY_WEIGHTS["commentary"]


def harden_authorities(authorities: list[str]) -> list[AuthorityCitation]:
    """Convert raw authority strings to weighted citations."""
    result: list[AuthorityCitation] = []
    for auth in authorities:
        auth_type, weight = classify_authority(auth)
        jurisdiction = "Texas"
        if any(x in auth.lower() for x in ["irc", "u.s.c.", "cfr", "pub. l.", "irs", "epa",
                                              "usfws", "nepa", "bgepa", "esa", "faa"]):
            jurisdiction = "Federal"
        if any(x in auth.lower() for x in ["nfpa", "ansi", "iec", "awea", "seia"]):
            jurisdiction = "National/Industry"
        result.append(AuthorityCitation(
            citation=auth,
            authority_type=auth_type,
            weight=weight,
            jurisdiction=jurisdiction,
        ))
    result.sort(key=lambda x: x.weight, reverse=True)
    return result


# ---------------------------------------------------------------------------
# Confidence Stratification
# ---------------------------------------------------------------------------
def compute_confidence_score(
    doctrine: DoctrineBlock,
    query_match_strength: float,
    authority_strength: float,
) -> tuple[str, float]:
    """Compute confidence level and numeric score for a doctrine match."""
    base_confidence_map: dict[str, float] = {
        ConfidenceLevel.DEFENSIBLE.value: 0.85,
        ConfidenceLevel.AGGRESSIVE.value: 0.60,
        ConfidenceLevel.DISCLOSURE.value: 0.45,
        ConfidenceLevel.HIGH_RISK.value: 0.25,
    }
    base = base_confidence_map.get(doctrine.confidence, 0.50)
    weighted = (base * 0.50) + (query_match_strength * 0.30) + (authority_strength * 0.20)
    score = round(min(max(weighted, 0.0), 1.0), 4)

    if score >= 0.75:
        level = ConfidenceLevel.DEFENSIBLE.value
    elif score >= 0.55:
        level = ConfidenceLevel.AGGRESSIVE.value
    elif score >= 0.35:
        level = ConfidenceLevel.DISCLOSURE.value
    else:
        level = ConfidenceLevel.HIGH_RISK.value

    return level, score


# ---------------------------------------------------------------------------
# Fact Fragility Scoring
# ---------------------------------------------------------------------------
def compute_fragility_score(doctrine: DoctrineBlock) -> float:
    """
    Score how fragile a doctrine's factual basis is.
    Higher score = more fragile/vulnerable to challenge.
    Scale: 0.0 (rock solid) to 1.0 (extremely fragile).
    """
    score = 0.0

    # Authority-based fragility
    if not doctrine.primary_authority:
        score += 0.30
    else:
        auth_types = [classify_authority(a)[0] for a in doctrine.primary_authority]
        if "constitution" in auth_types or "statute" in auth_types:
            score += 0.05
        elif "supreme_court" in auth_types:
            score += 0.10
        elif "regulation" in auth_types:
            score += 0.15
        else:
            score += 0.25

    # Confidence-based fragility
    conf_fragility: dict[str, float] = {
        ConfidenceLevel.DEFENSIBLE.value: 0.05,
        ConfidenceLevel.AGGRESSIVE.value: 0.20,
        ConfidenceLevel.DISCLOSURE.value: 0.35,
        ConfidenceLevel.HIGH_RISK.value: 0.50,
    }
    score += conf_fragility.get(doctrine.confidence, 0.25)

    # Counter-argument strength
    counter_count = len(doctrine.counter_arguments)
    if counter_count >= 5:
        score += 0.15
    elif counter_count >= 3:
        score += 0.10
    else:
        score += 0.05

    # Issue category fragility (market-based > statutory-based)
    market_categories = {
        IssueCategory.PAYMENT_STRUCTURE.value,
        IssueCategory.LANDOWNER_PROTECTION.value,
        IssueCategory.RESOURCE_ASSESSMENT.value,
    }
    if doctrine.issue_category in market_categories:
        score += 0.10

    return round(min(score, 1.0), 4)


# ---------------------------------------------------------------------------
# Epistemic Guardrails
# ---------------------------------------------------------------------------
def apply_epistemic_guardrails(
    doctrines: list[DoctrineBlock],
    query: str,
    zone: str,
) -> list[str]:
    """Generate epistemic warnings based on analysis context."""
    warnings: list[str] = []

    high_risk = [d for d in doctrines if d.confidence == ConfidenceLevel.HIGH_RISK.value]
    if high_risk:
        topics = ", ".join(d.topic for d in high_risk)
        warnings.append(
            f"HIGH_RISK positions identified on: {topics}. "
            "These positions have substantial litigation or regulatory challenge risk."
        )

    disclosure = [d for d in doctrines if d.confidence == ConfidenceLevel.DISCLOSURE.value]
    if disclosure:
        topics = ", ".join(d.topic for d in disclosure)
        warnings.append(
            f"DISCLOSURE required for: {topics}. "
            "Material uncertainty requiring explicit disclosure to client."
        )

    if zone == AnalysisZone.DISPUTE.value:
        warnings.append(
            "DISPUTE ZONE: Analysis reflects adversarial posture. Verify all "
            "factual representations independently before reliance."
        )

    cross_jurisdiction = any(
        "Federal" in a or "federal" in a.lower()
        for d in doctrines
        for a in d.primary_authority
    )
    if cross_jurisdiction:
        warnings.append(
            "Cross-jurisdictional analysis: Federal and Texas state authorities "
            "may interact. Confirm preemption and conflict-of-law positions."
        )

    return warnings


# ---------------------------------------------------------------------------
# Zoned Analysis
# ---------------------------------------------------------------------------
def validate_zone_consistency(
    zone: str,
    doctrines: list[DoctrineBlock],
) -> list[str]:
    """Ensure doctrine conclusions are appropriate for the analysis zone."""
    warnings: list[str] = []
    if zone == AnalysisZone.COMPLIANCE.value:
        aggressive = [d for d in doctrines if d.confidence == ConfidenceLevel.AGGRESSIVE.value]
        if aggressive:
            warnings.append(
                "ZONE CONFLICT: Aggressive positions included in COMPLIANCE zone. "
                "Review appropriateness of aggressive interpretations for compliance analysis."
            )
    if zone == AnalysisZone.NEGOTIATION.value:
        dispute_topics = [d for d in doctrines if "conflict" in d.topic or "dispute" in d.topic]
        if dispute_topics:
            warnings.append(
                "ZONE NOTE: Dispute-related doctrines referenced in NEGOTIATION zone. "
                "Consider whether adversarial framing is appropriate for negotiation context."
            )
    return warnings


# ---------------------------------------------------------------------------
# Multi-Doctrine Decomposition
# ---------------------------------------------------------------------------
def decompose_issues(
    matched_doctrines: list[DoctrineBlock],
) -> list[DecompositionNode]:
    """Decompose matched doctrines into categorized nodes with dependency ordering."""
    category_groups: dict[str, list[str]] = defaultdict(list)
    for d in matched_doctrines:
        category_groups[d.issue_category].append(d.topic)

    nodes: list[DecompositionNode] = []
    resolution_order = 0

    priority_order = [
        IssueCategory.TEXAS_REGULATORY.value,
        IssueCategory.ENVIRONMENTAL_COMPLIANCE.value,
        IssueCategory.ERCOT_INTERCONNECTION.value,
        IssueCategory.ACCOMMODATION_DOCTRINE.value,
        IssueCategory.OIL_GAS_COEXISTENCE.value,
        IssueCategory.WIND_LEASE_STRUCTURE.value,
        IssueCategory.SOLAR_LEASE_STRUCTURE.value,
        IssueCategory.EASEMENT_STRUCTURE.value,
        IssueCategory.PAYMENT_STRUCTURE.value,
        IssueCategory.SURFACE_USE.value,
        IssueCategory.SHADOW_FLICKER_NOISE.value,
        IssueCategory.LANDOWNER_PROTECTION.value,
        IssueCategory.DECOMMISSIONING.value,
        IssueCategory.TAX_INCENTIVE.value,
        IssueCategory.TRANSMISSION.value,
        IssueCategory.BATTERY_STORAGE.value,
        IssueCategory.FINANCING.value,
        IssueCategory.AGRICULTURAL.value,
        IssueCategory.ESTATE_PLANNING.value,
        IssueCategory.RESOURCE_ASSESSMENT.value,
    ]

    for category in priority_order:
        if category in category_groups:
            deps: list[str] = []
            for topic in category_groups[category]:
                edges = INTERACTION_GRAPH.get(topic, [])
                deps.extend(edges)
            deps = list(set(deps))

            nodes.append(DecompositionNode(
                issue_category=category,
                doctrines=category_groups[category],
                strata=_categorize_stratum(category),
                dependencies=deps,
                resolution_order=resolution_order,
            ))
            resolution_order += 1

    return nodes


def _categorize_stratum(category: str) -> str:
    """Assign a stratum level to an issue category."""
    regulatory = {
        IssueCategory.TEXAS_REGULATORY.value,
        IssueCategory.ENVIRONMENTAL_COMPLIANCE.value,
        IssueCategory.ERCOT_INTERCONNECTION.value,
    }
    structural = {
        IssueCategory.WIND_LEASE_STRUCTURE.value,
        IssueCategory.SOLAR_LEASE_STRUCTURE.value,
        IssueCategory.EASEMENT_STRUCTURE.value,
        IssueCategory.ACCOMMODATION_DOCTRINE.value,
        IssueCategory.OIL_GAS_COEXISTENCE.value,
    }
    economic = {
        IssueCategory.PAYMENT_STRUCTURE.value,
        IssueCategory.TAX_INCENTIVE.value,
        IssueCategory.FINANCING.value,
    }
    operational = {
        IssueCategory.SURFACE_USE.value,
        IssueCategory.SHADOW_FLICKER_NOISE.value,
        IssueCategory.LANDOWNER_PROTECTION.value,
        IssueCategory.DECOMMISSIONING.value,
        IssueCategory.BATTERY_STORAGE.value,
        IssueCategory.TRANSMISSION.value,
    }
    if category in regulatory:
        return "REGULATORY"
    if category in structural:
        return "STRUCTURAL"
    if category in economic:
        return "ECONOMIC"
    if category in operational:
        return "OPERATIONAL"
    return "ANCILLARY"


# ---------------------------------------------------------------------------
# Determinism Hash
# ---------------------------------------------------------------------------
def compute_determinism_hash(
    query: str,
    mode: str,
    zone: str,
    matched_topics: list[str],
    confidence_level: str,
) -> str:
    """Compute SHA-256 determinism hash for reproducibility."""
    payload = json.dumps({
        "engine_id": ENGINE_ID,
        "engine_version": ENGINE_VERSION,
        "query": query,
        "mode": mode,
        "zone": zone,
        "matched_topics": sorted(matched_topics),
        "confidence_level": confidence_level,
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Deep Analysis Mode
# ---------------------------------------------------------------------------
def generate_deep_analysis(
    query: str,
    matched_doctrines: list[DoctrineBlock],
    zone: str,
    entity_perspective: str,
) -> str:
    """Generate comprehensive deep analysis synthesizing all matched doctrines."""
    if not matched_doctrines:
        return "No doctrines matched for deep analysis."

    sections: list[str] = []

    # Header
    sections.append(f"DEEP ANALYSIS: Wind/Solar Lease — {zone} Zone")
    sections.append(f"Perspective: {entity_perspective.upper()}")
    sections.append(f"Query: {query}")
    sections.append("=" * 72)

    # Issue identification
    categories = list(set(d.issue_category for d in matched_doctrines))
    sections.append(f"\nISSUES IDENTIFIED ({len(categories)} categories):")
    for cat in categories:
        cat_doctrines = [d for d in matched_doctrines if d.issue_category == cat]
        sections.append(f"  - {cat}: {', '.join(d.topic for d in cat_doctrines)}")

    # Doctrine synthesis
    sections.append("\nDOCTRINE SYNTHESIS:")
    for i, doctrine in enumerate(matched_doctrines, 1):
        sections.append(f"\n{i}. {doctrine.topic.upper()}")
        sections.append(f"   Confidence: {doctrine.confidence}")
        sections.append(f"   Conclusion: {doctrine.conclusion_template}")
        sections.append(f"   Reasoning: {doctrine.reasoning_framework[:300]}...")
        if doctrine.primary_authority:
            sections.append(f"   Authorities: {'; '.join(doctrine.primary_authority[:3])}")

    # Interaction analysis
    sections.append("\nINTERACTION ANALYSIS:")
    for doctrine in matched_doctrines:
        edges = INTERACTION_GRAPH.get(doctrine.topic, [])
        triggered_edges = [e for e in edges if any(d.topic == e for d in matched_doctrines)]
        if triggered_edges:
            sections.append(f"  {doctrine.topic} -> {', '.join(triggered_edges)}")

    # Risk assessment
    sections.append("\nRISK ASSESSMENT:")
    high_risk = [d for d in matched_doctrines if d.confidence in
                 (ConfidenceLevel.HIGH_RISK.value, ConfidenceLevel.DISCLOSURE.value)]
    if high_risk:
        for d in high_risk:
            fragility = compute_fragility_score(d)
            sections.append(f"  RISK: {d.topic} (confidence={d.confidence}, fragility={fragility})")
            sections.append(f"    Adversary position: {d.adversary_position[:200]}")
    else:
        sections.append("  All matched doctrines at DEFENSIBLE or AGGRESSIVE confidence.")

    # Recommended actions
    sections.append("\nRECOMMENDED ACTIONS:")
    for i, doctrine in enumerate(matched_doctrines, 1):
        sections.append(f"  {i}. {doctrine.resolution_strategy[:200]}")

    return "\n".join(sections)


# ---------------------------------------------------------------------------
# Coverage Map
# ---------------------------------------------------------------------------
class CoverageMap:
    """Track doctrine coverage — which topics have been triggered vs missed."""

    def __init__(self, all_topics: list[str]) -> None:
        self._all_topics: set[str] = set(all_topics)
        self._triggered: dict[str, int] = defaultdict(int)
        self._query_count: int = 0

    def record_hit(self, topic: str) -> None:
        """Record a doctrine topic being triggered."""
        self._triggered[topic] += 1
        self._query_count += 1

    def get_coverage(self) -> dict[str, Any]:
        """Return coverage statistics."""
        triggered = set(self._triggered.keys())
        missed = self._all_topics - triggered
        ratio = len(triggered) / len(self._all_topics) if self._all_topics else 0.0
        return {
            "total_doctrines": len(self._all_topics),
            "triggered": len(triggered),
            "missed": len(missed),
            "coverage_ratio": round(ratio, 4),
            "triggered_list": sorted(triggered),
            "missed_list": sorted(missed),
            "hit_counts": dict(self._triggered),
            "total_queries": self._query_count,
        }


# ---------------------------------------------------------------------------
# Drift Watcher
# ---------------------------------------------------------------------------
class DriftWatcher:
    """Monitor for doctrine drift — changes in confidence patterns over time."""

    def __init__(self) -> None:
        self._confidence_history: dict[str, list[tuple[str, float]]] = defaultdict(list)
        self._observations: list[DriftObservation] = []

    def record_confidence(self, topic: str, confidence: str, score: float) -> Optional[DriftObservation]:
        """Record a confidence measurement and check for drift."""
        history = self._confidence_history[topic]
        history.append((confidence, score))

        if len(history) < 10:
            return None

        recent_scores = [s for _, s in history[-10:]]
        older_scores = [s for _, s in history[-20:-10]] if len(history) >= 20 else [s for _, s in history[:10]]

        if not older_scores:
            return None

        recent_avg = sum(recent_scores) / len(recent_scores)
        older_avg = sum(older_scores) / len(older_scores)
        delta = recent_avg - older_avg

        if abs(delta) > 0.15:
            drift_type = "confidence_increase" if delta > 0 else "confidence_decrease"
            severity = "HIGH" if abs(delta) > 0.25 else "MEDIUM"
            observation = DriftObservation(
                doctrine_topic=topic,
                drift_type=drift_type,
                description=f"Confidence {drift_type.split('_')[1]} of {abs(delta):.2f} over last 20 queries",
                severity=severity,
                previous_confidence=round(older_avg, 4),
                current_confidence=round(recent_avg, 4),
                delta=round(delta, 4),
                recommended_action=f"Review doctrine '{topic}' for authority changes or new precedent",
            )
            self._observations.append(observation)
            return observation
        return None


# ---------------------------------------------------------------------------
# Core Engine
# ---------------------------------------------------------------------------
class WindSolarLeaseEngine:
    """
    Core engine implementing all TIE-20 components for wind/solar lease analysis.
    """

    def __init__(self) -> None:
        logger.info("Initializing {name} v{ver}", name=ENGINE_NAME, ver=ENGINE_VERSION)

        # Build doctrine cache
        self._doctrines: list[DoctrineBlock] = build_doctrine_cache()
        self._doctrine_map: dict[str, DoctrineBlock] = {d.topic: d for d in self._doctrines}
        logger.info("Doctrine cache loaded: {n} blocks", n=len(self._doctrines))

        # Semantic normalizer
        self._normalizer: SemanticNormalizer = get_normalizer()

        # Search engine
        self._search_engine: BM25SearchEngine = get_search_engine()
        self._index_doctrines()

        # Telemetry
        self._telemetry: TelemetryCollector = get_collector()

        # Coverage map
        self._coverage: CoverageMap = CoverageMap(
            [d.topic for d in self._doctrines]
        )

        # Drift watcher
        self._drift: DriftWatcher = DriftWatcher()

        logger.info("{name} initialized successfully", name=ENGINE_NAME)

    def _index_doctrines(self) -> None:
        """Index all doctrines for BM25 search."""
        documents: list[IndexedDocument] = []
        for d in self._doctrines:
            doc = IndexedDocument(
                doc_id=d.topic,
                topic=d.topic,
                keywords=d.keywords,
                text=(
                    d.conclusion_template + " " +
                    d.reasoning_framework + " " +
                    " ".join(d.key_factors) + " " +
                    d.adversary_position + " " +
                    " ".join(d.counter_arguments) + " " +
                    d.resolution_strategy
                ),
                authority_refs=d.primary_authority,
                domain=d.issue_category,
                confidence=d.confidence,
            )
            documents.append(doc)
        self._search_engine.index_documents(documents)
        logger.info("Search index built: {n} documents", n=len(documents))

    # -------------------------------------------------------------------
    # TIE Component 1: Three-Layer Response
    # -------------------------------------------------------------------
    def analyze(self, request: QueryRequest) -> AnalysisResponse:
        """
        Three-layer response system:
        Layer 1: Doctrine cache lookup (0-50ms)
        Layer 2: Semantic search fallback (50-200ms)
        Layer 3: Deep analysis synthesis (200-2000ms)
        """
        start_time = time.perf_counter()
        trace = QueryTrace(
            query_text=request.query,
            response_mode=request.mode,
            zone=request.zone,
        )
        trace.compute_query_hash()

        # Cloud knowledge retrieval
        cloud_data = {}
        cloud_citations = []
        if _CLOUD_AVAILABLE:
            try:
                cloud = asyncio.run(retrieve_cloud_knowledge(request.query, category="renewable_energy"))
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
            # Normalize query
            with LatencyTimer(self._telemetry, "normalization") as norm_timer:
                normalized = self._normalizer.normalize_query(request.query)

            # Layer 1: Doctrine cache
            with LatencyTimer(self._telemetry, "doctrine_cache") as cache_timer:
                cache_matches = self._match_doctrines_from_cache(normalized)

            if cache_matches:
                trace.tier_used = QueryTier.DOCTRINE_CACHE.value
                trace.cache_hit = True
                matched_doctrines = cache_matches[:request.max_doctrines]
                search_fallback = False
            else:
                # Layer 2: Semantic search fallback
                with LatencyTimer(self._telemetry, "semantic_retrieval") as search_timer:
                    search_response = self._search_engine.combined_search(
                        query=request.query,
                        keywords=normalized.keywords,
                        max_results=request.max_doctrines,
                    )
                matched_doctrines = [
                    self._doctrine_map[r.topic]
                    for r in search_response.results
                    if r.topic in self._doctrine_map
                ]
                trace.tier_used = QueryTier.SEMANTIC_RETRIEVAL.value
                trace.cache_hit = False
                search_fallback = True

            # Build response
            doctrine_matches: list[DoctrineMatch] = []
            matched_topics: list[str] = []
            overall_confidence_score = 0.0

            for i, doctrine in enumerate(matched_doctrines):
                match_strength = 1.0 - (i * 0.1)
                auth_citations = harden_authorities(doctrine.primary_authority)
                auth_strength = (
                    max(a.weight for a in auth_citations) if auth_citations else 0.3
                )
                conf_level, conf_score = compute_confidence_score(
                    doctrine, match_strength, auth_strength
                )
                fragility = compute_fragility_score(doctrine)

                self._coverage.record_hit(doctrine.topic)
                drift_obs = self._drift.record_confidence(doctrine.topic, conf_level, conf_score)
                if drift_obs:
                    self._telemetry.record_drift(drift_obs)

                dm = DoctrineMatch(
                    topic=doctrine.topic,
                    confidence=conf_level,
                    confidence_score=conf_score,
                    conclusion=doctrine.conclusion_template,
                    reasoning=doctrine.reasoning_framework if request.mode != "FAST" else doctrine.reasoning_framework[:300],
                    key_factors=doctrine.key_factors,
                    authorities=auth_citations if request.include_authorities else [],
                    burden_holder=doctrine.burden_holder,
                    adversary_position=doctrine.adversary_position if request.include_counter_arguments else "",
                    counter_arguments=doctrine.counter_arguments if request.include_counter_arguments else [],
                    resolution_strategy=doctrine.resolution_strategy,
                    fragility_score=fragility,
                    issue_category=doctrine.issue_category,
                    interaction_edges=doctrine.interaction_edges,
                )
                doctrine_matches.append(dm)
                matched_topics.append(doctrine.topic)
                overall_confidence_score = max(overall_confidence_score, conf_score)

            # Confidence level from best match
            if overall_confidence_score >= 0.75:
                overall_level = ConfidenceLevel.DEFENSIBLE.value
            elif overall_confidence_score >= 0.55:
                overall_level = ConfidenceLevel.AGGRESSIVE.value
            elif overall_confidence_score >= 0.35:
                overall_level = ConfidenceLevel.DISCLOSURE.value
            else:
                overall_level = ConfidenceLevel.HIGH_RISK.value

            # Multi-doctrine decomposition
            decomposition = decompose_issues(matched_doctrines)

            # Epistemic guardrails
            epistemic_warnings = apply_epistemic_guardrails(
                matched_doctrines, request.query, request.zone
            )
            zone_warnings = validate_zone_consistency(request.zone, matched_doctrines)
            epistemic_warnings.extend(zone_warnings)

            # Coverage gaps
            coverage = self._coverage.get_coverage()
            coverage_gaps = coverage.get("missed_list", [])[:5]

            # Deep analysis (Layer 3)
            deep_text = None
            if request.deep_analysis or request.mode == "MEMO":
                with LatencyTimer(self._telemetry, "deep_analysis"):
                    deep_text = generate_deep_analysis(
                        request.query, matched_doctrines, request.zone, request.entity_perspective
                    )
                    trace.tier_used = QueryTier.DEEP_ANALYSIS.value

            # Determinism hash
            det_hash = compute_determinism_hash(
                request.query, request.mode, request.zone,
                matched_topics, overall_level,
            )

            # Calculate total latency
            total_latency = (time.perf_counter() - start_time) * 1000

            # Build response
            response = AnalysisResponse(
                query=request.query,
                mode=request.mode,
                zone=request.zone,
                entity_perspective=request.entity_perspective,
                determinism_hash=det_hash,
                tier_used=trace.tier_used,
                latency_ms=round(total_latency, 2),
                confidence_level=overall_level,
                confidence_score=round(overall_confidence_score, 4),
                doctrines_matched=doctrine_matches,
                decomposition=decomposition,
                deep_analysis=deep_text,
                epistemic_warnings=epistemic_warnings,
                coverage_gaps=coverage_gaps,
                search_fallback_used=search_fallback,
                trace_id=trace.trace_id,
                cloud_knowledge=cloud_data,
                cloud_citations=cloud_citations,
            )

            # Record telemetry
            trace.doctrine_topics_matched = matched_topics
            trace.confidence_level = overall_level
            trace.confidence_score = overall_confidence_score
            trace.latency_ms = total_latency
            trace.determinism_hash = det_hash
            trace.authority_count = sum(len(dm.authorities) for dm in doctrine_matches)
            trace.fragility_score = (
                max(dm.fragility_score for dm in doctrine_matches) if doctrine_matches else 0.0
            )
            self._telemetry.record_query(trace)

            return response

        except Exception as exc:
            trace.error_domain = ErrorDomain.UNKNOWN.value
            trace.error_message = str(exc)
            trace.latency_ms = (time.perf_counter() - start_time) * 1000
            self._telemetry.record_query(trace)
            logger.error("Analysis failed: {err}", err=str(exc))
            raise

    def _match_doctrines_from_cache(
        self,
        normalized: NormalizedQuery,
    ) -> list[DoctrineBlock]:
        """Match doctrines directly from cache using normalized concepts and keywords."""
        scored: list[tuple[float, DoctrineBlock]] = []

        for doctrine in self._doctrines:
            score = 0.0

            # Concept matching
            for concept in normalized.canonical_concepts:
                if concept in doctrine.topic or any(concept in kw for kw in doctrine.keywords):
                    score += 0.40

            # Keyword matching
            doctrine_keywords_lower = {k.lower() for k in doctrine.keywords}
            query_keywords = {k.lower() for k in normalized.keywords}
            keyword_overlap = doctrine_keywords_lower & query_keywords
            if keyword_overlap:
                score += 0.30 * (len(keyword_overlap) / max(len(doctrine_keywords_lower), 1))

            # Domain matching
            for domain in normalized.domains:
                domain_name = domain.value if hasattr(domain, 'value') else str(domain)
                if domain_name in doctrine.issue_category:
                    score += 0.20

            # Topic substring matching
            for kw in normalized.keywords:
                if kw in doctrine.topic:
                    score += 0.10

            if score >= 0.20:
                scored.append((score, doctrine))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored]

    def get_health(self) -> HealthReport:
        """Get engine health report."""
        return self._telemetry.get_health_report(doctrine_count=len(self._doctrines))

    def get_metrics(self) -> MetricsSnapshot:
        """Get engine metrics snapshot."""
        return self._telemetry.get_metrics_snapshot()

    def get_coverage(self) -> dict[str, Any]:
        """Get doctrine coverage statistics."""
        return self._coverage.get_coverage()


# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------
engine: Optional[WindSolarLeaseEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize engine on startup."""
    global engine
    logger.info("Starting {name} on port {port}", name=ENGINE_NAME, port=ENGINE_PORT)
    engine = WindSolarLeaseEngine()
    logger.info("{name} ready", name=ENGINE_NAME)
    yield
    logger.info("{name} shutting down", name=ENGINE_NAME)
    if _CLOUD_AVAILABLE:
        try:
            from cloud_retriever import cleanup_cloud_resources
            await cleanup_cloud_resources()
            logger.info("Cloud resources cleaned up")
        except Exception as e:
            logger.warning(f"Cloud cleanup failed: {e}")


app = FastAPI(
    title=ENGINE_NAME,
    description="TIE Gold Standard engine for wind and solar lease analysis",
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
# API Endpoints
# ---------------------------------------------------------------------------
@app.get("/health")
async def health_endpoint() -> dict[str, Any]:
    """Comprehensive health check endpoint."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    report = engine.get_health()
    return report.model_dump()


@app.get("/metrics")
async def metrics_endpoint() -> dict[str, Any]:
    """Engine metrics snapshot."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    metrics = engine.get_metrics()
    return metrics.model_dump()


@app.get("/coverage")
async def coverage_endpoint() -> dict[str, Any]:
    """Doctrine coverage statistics."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine.get_coverage()


@app.get("/doctrines")
async def list_doctrines() -> dict[str, Any]:
    """List all available doctrine topics."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return {
        "engine_id": ENGINE_ID,
        "doctrine_count": len(engine._doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "issue_category": d.issue_category,
                "confidence": d.confidence,
                "keywords": d.keywords,
                "authority_count": len(d.primary_authority),
            }
            for d in engine._doctrines
        ],
    }


@app.get("/doctrine/{topic}")
async def get_doctrine(topic: str) -> dict[str, Any]:
    """Get a specific doctrine block by topic."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    doctrine = engine._doctrine_map.get(topic)
    if not doctrine:
        raise HTTPException(status_code=404, detail=f"Doctrine '{topic}' not found")
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
        "issue_category": doctrine.issue_category,
        "interaction_edges": doctrine.interaction_edges,
    }


@app.post("/analyze")
async def analyze_endpoint(request: QueryRequest) -> dict[str, Any]:
    """Primary analysis endpoint — three-layer response."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    # Validate mode
    valid_modes = {"FAST", "DEFENSE", "MEMO"}
    if request.mode.upper() not in valid_modes:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid mode: {request.mode}. Must be one of {valid_modes}",
        )
    request.mode = request.mode.upper()

    # Validate zone
    valid_zones = {"NEGOTIATION", "DUE_DILIGENCE", "COMPLIANCE", "DISPUTE"}
    if request.zone.upper() not in valid_zones:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid zone: {request.zone}. Must be one of {valid_zones}",
        )
    request.zone = request.zone.upper()

    response = engine.analyze(request)
    return response.model_dump()


@app.post("/analyze/fast")
async def analyze_fast(query: str = Query(..., min_length=5)) -> dict[str, Any]:
    """Quick analysis endpoint — FAST mode, NEGOTIATION zone."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    request = QueryRequest(query=query, mode="FAST", zone="NEGOTIATION")
    response = engine.analyze(request)
    return response.model_dump()


@app.post("/analyze/defense")
async def analyze_defense(query: str = Query(..., min_length=5)) -> dict[str, Any]:
    """Defense analysis endpoint — DEFENSE mode with full authorities."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    request = QueryRequest(
        query=query, mode="DEFENSE", zone="NEGOTIATION",
        include_authorities=True, include_counter_arguments=True,
    )
    response = engine.analyze(request)
    return response.model_dump()


@app.post("/analyze/memo")
async def analyze_memo(query: str = Query(..., min_length=5)) -> dict[str, Any]:
    """Full memo analysis — MEMO mode with deep analysis."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    request = QueryRequest(
        query=query, mode="MEMO", zone="NEGOTIATION",
        include_authorities=True, include_counter_arguments=True,
        deep_analysis=True, max_doctrines=10,
    )
    response = engine.analyze(request)
    return response.model_dump()


@app.get("/traces")
async def get_traces(limit: int = Query(default=50, ge=1, le=500)) -> dict[str, Any]:
    """Get recent query traces."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    traces = engine._telemetry.get_recent_traces(limit)
    return {
        "engine_id": ENGINE_ID,
        "trace_count": len(traces),
        "traces": [t.model_dump() for t in traces],
    }


@app.get("/errors")
async def get_errors(limit: int = Query(default=100, ge=1, le=500)) -> dict[str, Any]:
    """Get recent error log."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    errors = engine._telemetry.get_error_log(limit)
    return {
        "engine_id": ENGINE_ID,
        "error_count": len(errors),
        "errors": errors,
    }


@app.get("/drift")
async def get_drift(limit: int = Query(default=50, ge=1, le=200)) -> dict[str, Any]:
    """Get drift observations."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    observations = engine._telemetry.get_drift_observations(limit)
    return {
        "engine_id": ENGINE_ID,
        "observation_count": len(observations),
        "observations": [o.model_dump() for o in observations],
    }


@app.get("/interaction-graph")
async def get_interaction_graph() -> dict[str, Any]:
    """Get the doctrine interaction graph."""
    return {
        "engine_id": ENGINE_ID,
        "node_count": len(INTERACTION_GRAPH),
        "edges": INTERACTION_GRAPH,
    }


# ---------------------------------------------------------------------------
# Response Formatters — Mode-Specific Output
# ---------------------------------------------------------------------------
class ResponseFormatter:
    """Format analysis responses according to the selected mode."""

    @staticmethod
    def format_fast(response: AnalysisResponse) -> dict[str, Any]:
        """FAST mode: concise answer with key terms and critical provisions."""
        summary_lines: list[str] = []
        for dm in response.doctrines_matched[:3]:
            summary_lines.append(f"[{dm.confidence}] {dm.topic}: {dm.conclusion[:200]}")

        return {
            "engine_id": response.engine_id,
            "mode": "FAST",
            "query": response.query,
            "confidence": response.confidence_level,
            "score": response.confidence_score,
            "summary": "\n".join(summary_lines),
            "key_topics": [dm.topic for dm in response.doctrines_matched],
            "top_factors": (
                response.doctrines_matched[0].key_factors[:5]
                if response.doctrines_matched else []
            ),
            "resolution": (
                response.doctrines_matched[0].resolution_strategy
                if response.doctrines_matched else ""
            ),
            "latency_ms": response.latency_ms,
            "determinism_hash": response.determinism_hash,
        }

    @staticmethod
    def format_defense(response: AnalysisResponse) -> dict[str, Any]:
        """DEFENSE mode: full analysis with authority citations and risk assessment."""
        doctrine_details: list[dict[str, Any]] = []
        for dm in response.doctrines_matched:
            doctrine_details.append({
                "topic": dm.topic,
                "confidence": dm.confidence,
                "score": dm.confidence_score,
                "conclusion": dm.conclusion,
                "reasoning": dm.reasoning,
                "key_factors": dm.key_factors,
                "authorities": [
                    {
                        "citation": a.citation,
                        "type": a.authority_type,
                        "weight": a.weight,
                        "jurisdiction": a.jurisdiction,
                    }
                    for a in dm.authorities
                ],
                "burden_holder": dm.burden_holder,
                "adversary_position": dm.adversary_position,
                "counter_arguments": dm.counter_arguments,
                "resolution_strategy": dm.resolution_strategy,
                "fragility_score": dm.fragility_score,
                "issue_category": dm.issue_category,
                "interaction_edges": dm.interaction_edges,
            })

        risk_assessment: list[dict[str, Any]] = []
        for dm in response.doctrines_matched:
            if dm.fragility_score > 0.40:
                risk_assessment.append({
                    "topic": dm.topic,
                    "fragility": dm.fragility_score,
                    "confidence": dm.confidence,
                    "risk_level": "HIGH" if dm.fragility_score > 0.60 else "MEDIUM",
                    "primary_risk": dm.adversary_position[:200],
                })

        return {
            "engine_id": response.engine_id,
            "mode": "DEFENSE",
            "query": response.query,
            "zone": response.zone,
            "entity_perspective": response.entity_perspective,
            "overall_confidence": response.confidence_level,
            "overall_score": response.confidence_score,
            "doctrine_count": len(doctrine_details),
            "doctrines": doctrine_details,
            "risk_assessment": risk_assessment,
            "epistemic_warnings": response.epistemic_warnings,
            "decomposition": [n.model_dump() for n in response.decomposition],
            "latency_ms": response.latency_ms,
            "determinism_hash": response.determinism_hash,
            "trace_id": response.trace_id,
        }

    @staticmethod
    def format_memo(response: AnalysisResponse) -> dict[str, Any]:
        """MEMO mode: complete memorandum with background, analysis, conclusion."""
        # Build formal memo structure
        memo_sections: dict[str, str] = {}

        # Header
        memo_sections["header"] = (
            f"MEMORANDUM\n"
            f"RE: {response.query}\n"
            f"Date: {response.timestamp}\n"
            f"Analysis Zone: {response.zone}\n"
            f"Entity Perspective: {response.entity_perspective}\n"
            f"Confidence: {response.confidence_level} ({response.confidence_score:.2%})\n"
            f"Engine: {response.engine_id} v{response.engine_version}"
        )

        # Background / Issue Identification
        issues = list(set(dm.issue_category for dm in response.doctrines_matched))
        memo_sections["issues_presented"] = (
            f"Issues Presented ({len(issues)}):\n" +
            "\n".join(f"  {i+1}. {cat.replace('_', ' ').title()}"
                      for i, cat in enumerate(issues))
        )

        # Analysis
        analysis_parts: list[str] = []
        for i, dm in enumerate(response.doctrines_matched, 1):
            part = (
                f"\n{'='*60}\n"
                f"{i}. {dm.topic.replace('_', ' ').upper()}\n"
                f"{'='*60}\n\n"
                f"Confidence: {dm.confidence} ({dm.confidence_score:.2%})\n"
                f"Fragility Score: {dm.fragility_score:.2%}\n"
                f"Burden: {dm.burden_holder}\n\n"
                f"CONCLUSION:\n{dm.conclusion}\n\n"
                f"ANALYSIS:\n{dm.reasoning}\n\n"
                f"KEY FACTORS:\n" +
                "\n".join(f"  - {f}" for f in dm.key_factors) +
                f"\n\nAUTHORITIES:\n" +
                "\n".join(
                    f"  [{a.authority_type.upper()}] {a.citation} (weight: {a.weight})"
                    for a in dm.authorities
                ) +
                f"\n\nADVERSARY POSITION:\n{dm.adversary_position}\n\n"
                f"COUNTER-ARGUMENTS:\n" +
                "\n".join(f"  {j}. {ca}" for j, ca in enumerate(dm.counter_arguments, 1)) +
                f"\n\nRECOMMENDED STRATEGY:\n{dm.resolution_strategy}"
            )
            analysis_parts.append(part)
        memo_sections["analysis"] = "\n".join(analysis_parts)

        # Decomposition
        if response.decomposition:
            decomp_text = "ISSUE DECOMPOSITION:\n"
            for node in response.decomposition:
                decomp_text += (
                    f"\n  Order {node.resolution_order}: {node.issue_category} "
                    f"[{node.strata}]\n"
                    f"    Doctrines: {', '.join(node.doctrines)}\n"
                    f"    Dependencies: {', '.join(node.dependencies) or 'None'}\n"
                )
            memo_sections["decomposition"] = decomp_text

        # Deep analysis
        if response.deep_analysis:
            memo_sections["deep_analysis"] = response.deep_analysis

        # Warnings
        if response.epistemic_warnings:
            memo_sections["warnings"] = (
                "EPISTEMIC WARNINGS:\n" +
                "\n".join(f"  ! {w}" for w in response.epistemic_warnings)
            )

        # Coverage gaps
        if response.coverage_gaps:
            memo_sections["coverage_gaps"] = (
                "COVERAGE GAPS (doctrines not triggered):\n" +
                "\n".join(f"  - {g}" for g in response.coverage_gaps)
            )

        return {
            "engine_id": response.engine_id,
            "mode": "MEMO",
            "memo": memo_sections,
            "raw_response": response.model_dump(),
            "determinism_hash": response.determinism_hash,
            "trace_id": response.trace_id,
        }


# ---------------------------------------------------------------------------
# Lease Payment Calculator
# ---------------------------------------------------------------------------
class PaymentScenario(BaseModel):
    """Input for lease payment calculation."""
    project_type: str = Field(..., description="wind or solar")
    total_acreage: float = Field(..., gt=0, description="Total leased acreage")
    capacity_mw: float = Field(..., gt=0, description="Project capacity in MW")
    payment_structure: str = Field(
        default="per_acre",
        description="per_acre, per_mw, revenue_share, or hybrid",
    )
    per_acre_rate: float = Field(default=0.0, ge=0, description="Annual $/acre")
    per_mw_rate: float = Field(default=0.0, ge=0, description="Annual $/MW")
    revenue_share_pct: float = Field(default=0.0, ge=0, le=100, description="Gross revenue %")
    escalation_rate: float = Field(default=2.0, ge=0, le=10, description="Annual escalation %")
    initial_term_years: int = Field(default=30, ge=10, le=50, description="Operations term years")
    estimated_capacity_factor: float = Field(default=0.0, ge=0, le=1.0, description="0-1 capacity factor")
    estimated_ppa_price: float = Field(default=0.0, ge=0, description="$/MWh PPA price")
    signing_bonus: float = Field(default=0.0, ge=0, description="One-time signing bonus $")
    option_payment_annual: float = Field(default=0.0, ge=0, description="Annual option payment $")
    option_years: int = Field(default=0, ge=0, le=10, description="Option period years")


class PaymentProjection(BaseModel):
    """Output from lease payment calculation."""
    project_type: str
    payment_structure: str
    total_acreage: float
    capacity_mw: float
    initial_term_years: int
    escalation_rate: float
    signing_bonus: float
    total_option_payments: float
    year_1_payment: float
    year_10_payment: float
    year_20_payment: float
    year_30_payment: float
    total_lease_payments: float
    total_all_payments: float
    avg_annual_payment: float
    avg_payment_per_acre: float
    avg_payment_per_mw: float
    npv_at_5pct: float
    npv_at_8pct: float
    payment_schedule: list[dict[str, Any]]
    comparison_notes: list[str]


def calculate_lease_payments(scenario: PaymentScenario) -> PaymentProjection:
    """Calculate comprehensive lease payment projections."""
    schedule: list[dict[str, Any]] = []
    total_lease = 0.0

    for year in range(1, scenario.initial_term_years + 1):
        escalation_multiplier = (1 + scenario.escalation_rate / 100) ** (year - 1)

        if scenario.payment_structure == "per_acre":
            base = scenario.per_acre_rate * scenario.total_acreage
        elif scenario.payment_structure == "per_mw":
            base = scenario.per_mw_rate * scenario.capacity_mw
        elif scenario.payment_structure == "revenue_share":
            if scenario.estimated_capacity_factor > 0 and scenario.estimated_ppa_price > 0:
                annual_mwh = scenario.capacity_mw * 8760 * scenario.estimated_capacity_factor
                annual_revenue = annual_mwh * scenario.estimated_ppa_price
                base = annual_revenue * (scenario.revenue_share_pct / 100)
            else:
                base = 0.0
        elif scenario.payment_structure == "hybrid":
            # Minimum per-acre with revenue share kicker
            per_acre_base = scenario.per_acre_rate * scenario.total_acreage
            if scenario.estimated_capacity_factor > 0 and scenario.estimated_ppa_price > 0:
                annual_mwh = scenario.capacity_mw * 8760 * scenario.estimated_capacity_factor
                annual_revenue = annual_mwh * scenario.estimated_ppa_price
                revenue_payment = annual_revenue * (scenario.revenue_share_pct / 100)
                base = max(per_acre_base, revenue_payment)
            else:
                base = per_acre_base
        else:
            base = scenario.per_acre_rate * scenario.total_acreage

        annual_payment = round(base * escalation_multiplier, 2)
        total_lease += annual_payment

        schedule.append({
            "year": year,
            "base_payment": round(base, 2),
            "escalation_multiplier": round(escalation_multiplier, 4),
            "annual_payment": annual_payment,
            "cumulative": round(total_lease, 2),
        })

    # Option period payments
    total_option = scenario.option_payment_annual * scenario.option_years

    # Total all payments
    total_all = scenario.signing_bonus + total_option + total_lease

    # NPV calculations
    def npv(rate: float) -> float:
        pv = scenario.signing_bonus
        for entry in schedule:
            pv += entry["annual_payment"] / ((1 + rate) ** entry["year"])
        return round(pv, 2)

    # Year-specific payments
    def payment_at_year(y: int) -> float:
        for entry in schedule:
            if entry["year"] == y:
                return entry["annual_payment"]
        return 0.0

    # Comparison notes
    notes: list[str] = []
    if scenario.project_type == "wind":
        if scenario.per_acre_rate > 0 and scenario.per_acre_rate < 30:
            notes.append("Per-acre rate below typical wind lease range ($30-$80/acre)")
        if scenario.per_acre_rate > 80:
            notes.append("Per-acre rate above typical wind lease range ($30-$80/acre)")
        if scenario.per_mw_rate > 0 and scenario.per_mw_rate < 3000:
            notes.append("Per-MW rate below typical wind range ($3,000-$8,000/MW)")
        if scenario.per_mw_rate > 8000:
            notes.append("Per-MW rate above typical wind range ($3,000-$8,000/MW)")
    elif scenario.project_type == "solar":
        if scenario.per_acre_rate > 0 and scenario.per_acre_rate < 300:
            notes.append("Per-acre rate below typical solar lease range ($300-$1,500/acre)")
        if scenario.per_acre_rate > 1500:
            notes.append("Per-acre rate above typical solar lease range ($300-$1,500/acre)")

    if scenario.revenue_share_pct > 0 and scenario.revenue_share_pct < 2:
        notes.append("Revenue share below typical range (2-6%)")
    if scenario.revenue_share_pct > 6:
        notes.append("Revenue share above typical range (2-6%)")

    if scenario.escalation_rate < 1.5:
        notes.append("Escalation rate below recommended minimum (1.5-2% CPI floor)")
    if scenario.escalation_rate > 4:
        notes.append("Escalation rate above typical caps (3-4%)")

    avg_annual = total_lease / scenario.initial_term_years if scenario.initial_term_years > 0 else 0
    avg_per_acre = avg_annual / scenario.total_acreage if scenario.total_acreage > 0 else 0
    avg_per_mw = avg_annual / scenario.capacity_mw if scenario.capacity_mw > 0 else 0

    return PaymentProjection(
        project_type=scenario.project_type,
        payment_structure=scenario.payment_structure,
        total_acreage=scenario.total_acreage,
        capacity_mw=scenario.capacity_mw,
        initial_term_years=scenario.initial_term_years,
        escalation_rate=scenario.escalation_rate,
        signing_bonus=scenario.signing_bonus,
        total_option_payments=total_option,
        year_1_payment=payment_at_year(1),
        year_10_payment=payment_at_year(10),
        year_20_payment=payment_at_year(20),
        year_30_payment=payment_at_year(30),
        total_lease_payments=round(total_lease, 2),
        total_all_payments=round(total_all, 2),
        avg_annual_payment=round(avg_annual, 2),
        avg_payment_per_acre=round(avg_per_acre, 2),
        avg_payment_per_mw=round(avg_per_mw, 2),
        npv_at_5pct=npv(0.05),
        npv_at_8pct=npv(0.08),
        payment_schedule=schedule,
        comparison_notes=notes,
    )


# ---------------------------------------------------------------------------
# Negotiation Position Generator
# ---------------------------------------------------------------------------
class NegotiationPosition(BaseModel):
    """A structured negotiation position with supporting analysis."""
    position_id: str = Field(default_factory=lambda: uuid4().hex[:12])
    topic: str
    perspective: str
    opening_position: str
    target_position: str
    walkaway_position: str
    key_leverage_points: list[str]
    supporting_authorities: list[str]
    risk_factors: list[str]
    negotiation_tactics: list[str]
    common_developer_responses: list[str]
    recommended_counter_responses: list[str]


class NegotiationRequest(BaseModel):
    """Request for negotiation position generation."""
    topics: list[str] = Field(..., min_length=1, max_length=10)
    perspective: str = Field(default="landowner")
    aggressiveness: str = Field(default="moderate", description="conservative, moderate, aggressive")


def generate_negotiation_positions(
    request: NegotiationRequest,
    doctrine_map: dict[str, DoctrineBlock],
) -> list[NegotiationPosition]:
    """Generate negotiation positions for specified topics."""
    positions: list[NegotiationPosition] = []

    for topic in request.topics:
        doctrine = doctrine_map.get(topic)
        if not doctrine:
            continue

        # Scale positions by aggressiveness
        if request.aggressiveness == "aggressive":
            opening_modifier = "Maximum protection: "
            target_modifier = "Strong protection: "
            walkaway_modifier = "Minimum acceptable: "
        elif request.aggressiveness == "conservative":
            opening_modifier = "Reasonable request: "
            target_modifier = "Acceptable compromise: "
            walkaway_modifier = "Essential minimum: "
        else:
            opening_modifier = "Opening position: "
            target_modifier = "Target outcome: "
            walkaway_modifier = "Bottom line: "

        # Extract leverage points from doctrine
        leverage = []
        if doctrine.counter_arguments:
            leverage.extend(doctrine.counter_arguments[:3])
        if doctrine.primary_authority:
            leverage.append(f"Legal authority: {doctrine.primary_authority[0]}")
        leverage.append(f"Industry standard supports this position ({doctrine.confidence})")

        # Common developer responses
        dev_responses = [
            doctrine.adversary_position[:200],
            "Project economics don't support this provision",
            "Lender requirements prevent this accommodation",
            "Industry standard does not include this term",
            "This would delay the project timeline",
        ]

        # Counter-responses
        counters = [
            doctrine.resolution_strategy[:200],
            "Competing developers have agreed to these terms",
            "Reasonable landowner protections do not impair project viability",
            "Lender concerns can be addressed through SNDA provisions",
            "Investment in landowner relationship reduces long-term dispute risk",
        ]

        # Tactics based on topic
        tactics = [
            "Present multiple comparable lease offers showing market terms",
            "Focus on mutual benefit and long-term relationship",
            "Reference specific authority citations to establish legitimacy",
            "Propose alternative structures that achieve same protection",
            "Use silence strategically after presenting key demands",
        ]

        positions.append(NegotiationPosition(
            topic=topic,
            perspective=request.perspective,
            opening_position=f"{opening_modifier}{doctrine.conclusion_template[:200]}",
            target_position=f"{target_modifier}{doctrine.resolution_strategy[:200]}",
            walkaway_position=f"{walkaway_modifier}Minimum {doctrine.key_factors[0] if doctrine.key_factors else 'acceptable standard'}",
            key_leverage_points=leverage,
            supporting_authorities=doctrine.primary_authority[:3],
            risk_factors=[f"Fragility: {compute_fragility_score(doctrine):.2%}"] + doctrine.counter_arguments[:2],
            negotiation_tactics=tactics,
            common_developer_responses=dev_responses[:3],
            recommended_counter_responses=counters[:3],
        ))

    return positions


# ---------------------------------------------------------------------------
# Lease Comparison Engine
# ---------------------------------------------------------------------------
class LeaseTermComparison(BaseModel):
    """Comparison of a single lease term across offers."""
    term: str
    description: str
    offer_values: dict[str, str]
    best_offer: str
    worst_offer: str
    industry_standard: str
    analysis: str
    importance: str  # critical, important, desirable, standard


class LeaseComparisonRequest(BaseModel):
    """Request for lease comparison analysis."""
    offers: dict[str, dict[str, Any]] = Field(
        ...,
        description="Named offers with term:value pairs",
    )
    project_type: str = Field(default="wind", description="wind or solar")
    perspective: str = Field(default="landowner")


class LeaseComparisonResponse(BaseModel):
    """Complete lease comparison result."""
    engine_id: str = ENGINE_ID
    project_type: str
    offer_count: int
    comparisons: list[LeaseTermComparison]
    overall_ranking: list[dict[str, Any]]
    recommendation: str
    warnings: list[str]


# Standard terms database for comparison
STANDARD_LEASE_TERMS: dict[str, dict[str, Any]] = {
    "option_period_years": {
        "description": "Initial option period duration",
        "wind_standard": "3-5 years",
        "solar_standard": "3-5 years",
        "importance": "critical",
        "landowner_preference": "shorter",
    },
    "option_extensions": {
        "description": "Number and duration of option extensions",
        "wind_standard": "1-2 extensions of 1 year each",
        "solar_standard": "1-2 extensions of 1 year each",
        "importance": "important",
        "landowner_preference": "fewer",
    },
    "option_payment_per_acre": {
        "description": "Annual option period payment per acre",
        "wind_standard": "$10-$30/acre",
        "solar_standard": "$50-$200/acre",
        "importance": "important",
        "landowner_preference": "higher",
    },
    "operations_term_years": {
        "description": "Operations period duration",
        "wind_standard": "25-35 years",
        "solar_standard": "25-35 years",
        "importance": "critical",
        "landowner_preference": "shorter",
    },
    "renewal_options": {
        "description": "Renewal term options after initial operations",
        "wind_standard": "1-2 renewals of 5-10 years",
        "solar_standard": "1-2 renewals of 5-10 years",
        "importance": "important",
        "landowner_preference": "fewer with renegotiation",
    },
    "per_acre_annual_rate": {
        "description": "Annual per-acre lease payment",
        "wind_standard": "$30-$80/acre",
        "solar_standard": "$300-$1,500/acre",
        "importance": "critical",
        "landowner_preference": "higher",
    },
    "per_mw_annual_rate": {
        "description": "Annual per-MW capacity payment",
        "wind_standard": "$3,000-$8,000/MW",
        "solar_standard": "N/A (per-acre preferred)",
        "importance": "critical",
        "landowner_preference": "higher",
    },
    "revenue_share_pct": {
        "description": "Percentage of gross revenue",
        "wind_standard": "2-6%",
        "solar_standard": "2-6%",
        "importance": "critical",
        "landowner_preference": "higher",
    },
    "escalation_rate": {
        "description": "Annual payment escalation rate",
        "wind_standard": "CPI with 2% floor, no cap",
        "solar_standard": "CPI with 2% floor, no cap",
        "importance": "critical",
        "landowner_preference": "higher floor, no cap",
    },
    "signing_bonus": {
        "description": "One-time signing bonus",
        "wind_standard": "$1,000-$5,000/turbine site",
        "solar_standard": "$50-$200/acre",
        "importance": "desirable",
        "landowner_preference": "higher",
    },
    "decommissioning_bond": {
        "description": "Financial assurance for decommissioning",
        "wind_standard": "125% of removal cost at COD",
        "solar_standard": "125% of removal cost at COD",
        "importance": "critical",
        "landowner_preference": "higher percentage, posted early",
    },
    "dwelling_setback_feet": {
        "description": "Minimum distance from occupied structures",
        "wind_standard": "1,500 feet",
        "solar_standard": "500 feet",
        "importance": "important",
        "landowner_preference": "greater distance",
    },
    "property_line_setback": {
        "description": "Minimum distance from property lines",
        "wind_standard": "1.1x tip height",
        "solar_standard": "100-300 feet",
        "importance": "important",
        "landowner_preference": "greater distance",
    },
    "assignment_consent": {
        "description": "Landowner consent for lease assignment",
        "wind_standard": "Consent required, not unreasonably withheld",
        "solar_standard": "Consent required, not unreasonably withheld",
        "importance": "important",
        "landowner_preference": "consent required with creditworthiness standards",
    },
    "agricultural_indemnification": {
        "description": "Developer indemnification for ag exemption rollback",
        "wind_standard": "Full developer indemnification",
        "solar_standard": "Full developer indemnification",
        "importance": "critical",
        "landowner_preference": "full indemnification",
    },
    "insurance_additional_insured": {
        "description": "Landowner named as additional insured",
        "wind_standard": "Yes, on CGL and umbrella",
        "solar_standard": "Yes, on CGL and umbrella",
        "importance": "important",
        "landowner_preference": "included",
    },
    "cessation_of_operations_months": {
        "description": "Months of non-production triggering termination right",
        "wind_standard": "12-24 months",
        "solar_standard": "12-24 months",
        "importance": "important",
        "landowner_preference": "shorter period",
    },
    "hunting_rights_reserved": {
        "description": "Landowner retention of hunting rights",
        "wind_standard": "Reserved outside safety zones",
        "solar_standard": "Reserved outside fenced areas",
        "importance": "desirable",
        "landowner_preference": "maximum retention",
    },
    "road_maintenance": {
        "description": "Developer obligation for road construction and maintenance",
        "wind_standard": "Developer builds and maintains to county standards",
        "solar_standard": "Developer builds and maintains",
        "importance": "standard",
        "landowner_preference": "developer responsibility",
    },
}


def compare_lease_offers(request: LeaseComparisonRequest) -> LeaseComparisonResponse:
    """Compare multiple lease offers against industry standards."""
    comparisons: list[LeaseTermComparison] = []
    offer_scores: dict[str, float] = {name: 0.0 for name in request.offers}
    warnings: list[str] = []

    for term_key, standard in STANDARD_LEASE_TERMS.items():
        offer_values: dict[str, str] = {}
        best_offer_name = ""
        worst_offer_name = ""

        for offer_name, offer_terms in request.offers.items():
            val = offer_terms.get(term_key, "Not specified")
            offer_values[offer_name] = str(val)

        # Determine industry standard based on project type
        industry_std = (
            standard.get(f"{request.project_type}_standard", "N/A")
        )

        # Simple scoring (presence vs absence)
        for offer_name, val in offer_values.items():
            if val != "Not specified" and val != "N/A":
                importance_score = {
                    "critical": 3.0,
                    "important": 2.0,
                    "desirable": 1.0,
                    "standard": 0.5,
                }.get(standard["importance"], 1.0)
                offer_scores[offer_name] += importance_score

        # Determine best and worst (simplified — presence-based)
        specified = {k: v for k, v in offer_values.items() if v not in ("Not specified", "N/A")}
        if specified:
            best_offer_name = list(specified.keys())[0]
            worst_offer_name = list(specified.keys())[-1] if len(specified) > 1 else ""

        comparisons.append(LeaseTermComparison(
            term=term_key,
            description=standard["description"],
            offer_values=offer_values,
            best_offer=best_offer_name,
            worst_offer=worst_offer_name,
            industry_standard=industry_std,
            analysis=f"Industry standard: {industry_std}. Importance: {standard['importance']}.",
            importance=standard["importance"],
        ))

    # Overall ranking
    ranked = sorted(offer_scores.items(), key=lambda x: x[1], reverse=True)
    overall_ranking = [
        {"rank": i + 1, "offer": name, "score": round(score, 2)}
        for i, (name, score) in enumerate(ranked)
    ]

    # Generate recommendation
    if ranked:
        best_name = ranked[0][0]
        recommendation = (
            f"Based on term coverage analysis, '{best_name}' scores highest with "
            f"{ranked[0][1]:.1f} points across {len(STANDARD_LEASE_TERMS)} evaluated terms. "
            f"Detailed negotiation should focus on critical terms where this offer "
            f"deviates from industry standards."
        )
    else:
        recommendation = "Insufficient offer data for ranking."

    # Generate warnings for missing critical terms
    for offer_name, offer_terms in request.offers.items():
        for term_key, standard in STANDARD_LEASE_TERMS.items():
            if standard["importance"] == "critical" and term_key not in offer_terms:
                warnings.append(
                    f"CRITICAL TERM MISSING in '{offer_name}': {standard['description']} ({term_key})"
                )

    return LeaseComparisonResponse(
        project_type=request.project_type,
        offer_count=len(request.offers),
        comparisons=comparisons,
        overall_ranking=overall_ranking,
        recommendation=recommendation,
        warnings=warnings,
    )


# ---------------------------------------------------------------------------
# Decommissioning Cost Estimator
# ---------------------------------------------------------------------------
class DecommissioningEstimateRequest(BaseModel):
    """Request for decommissioning cost estimation."""
    project_type: str = Field(..., description="wind or solar")
    capacity_mw: float = Field(..., gt=0)
    turbine_count: int = Field(default=0, ge=0, description="Number of wind turbines")
    acreage: float = Field(default=0, gt=0, description="Solar array acreage")
    turbine_hub_height_m: float = Field(default=100, description="Turbine hub height in meters")
    foundation_type: str = Field(default="spread", description="spread or pile")
    road_miles: float = Field(default=0, ge=0)
    underground_cable_miles: float = Field(default=0, ge=0)
    substation_count: int = Field(default=1, ge=0)
    state: str = Field(default="TX")


class DecommissioningEstimate(BaseModel):
    """Decommissioning cost estimation result."""
    project_type: str
    capacity_mw: float
    component_costs: dict[str, float]
    total_removal_cost: float
    estimated_salvage_value: float
    net_decommissioning_cost: float
    recommended_bond_amount: float
    bond_multiple: float
    restoration_timeline_months: int
    cost_per_mw: float
    notes: list[str]


def estimate_decommissioning_cost(request: DecommissioningEstimateRequest) -> DecommissioningEstimate:
    """Estimate decommissioning costs for wind or solar projects."""
    costs: dict[str, float] = {}
    salvage = 0.0
    notes: list[str] = []

    if request.project_type == "wind":
        # Wind turbine removal costs
        per_turbine_removal = 350000.0  # Average removal cost per turbine
        if request.turbine_hub_height_m > 120:
            per_turbine_removal *= 1.25  # Larger crane needed
            notes.append("Hub height >120m requires larger crane, +25% removal cost")

        costs["turbine_removal"] = round(per_turbine_removal * request.turbine_count, 2)

        # Foundation removal (to 4 feet below grade)
        per_foundation = 35000.0 if request.foundation_type == "spread" else 50000.0
        costs["foundation_removal"] = round(per_foundation * request.turbine_count, 2)

        # Road removal
        costs["road_removal"] = round(request.road_miles * 50000, 2)  # $50K/mile

        # Underground cable removal
        costs["cable_removal"] = round(request.underground_cable_miles * 30000, 2)

        # Substation removal
        costs["substation_removal"] = round(request.substation_count * 250000, 2)

        # Site restoration
        costs["site_restoration"] = round(request.turbine_count * 15000, 2)

        # Project management and contingency (15%)
        subtotal = sum(costs.values())
        costs["project_management_contingency"] = round(subtotal * 0.15, 2)

        # Salvage value (steel, copper)
        salvage_per_turbine = 45000.0  # Conservative scrap value
        salvage = round(salvage_per_turbine * request.turbine_count, 2)
        notes.append(f"Salvage estimate: ${salvage_per_turbine:,.0f}/turbine (conservative steel scrap)")

        restoration_months = 18

    else:  # solar
        # Panel removal and recycling
        panels_per_mw = 2500  # Approximate panel count per MW
        total_panels = panels_per_mw * request.capacity_mw
        costs["panel_removal_recycling"] = round(total_panels * 20, 2)  # $20/panel

        # Racking/mounting removal
        costs["racking_removal"] = round(total_panels * 4, 2)  # $4/panel

        # Inverter and transformer removal
        costs["inverter_transformer_removal"] = round(request.capacity_mw * 8000, 2)

        # Underground cable removal
        costs["cable_removal"] = round(request.underground_cable_miles * 25000, 2)

        # Substation removal
        costs["substation_removal"] = round(request.substation_count * 200000, 2)

        # Fence removal
        if request.acreage > 0:
            fence_perimeter_ft = (request.acreage * 43560) ** 0.5 * 4  # Approximate
            costs["fence_removal"] = round(fence_perimeter_ft * 3, 2)  # $3/ft
        else:
            costs["fence_removal"] = 0

        # Site restoration (grading, topsoil, revegetation)
        costs["site_restoration"] = round(request.acreage * 8000, 2)  # $8K/acre

        # Road removal
        costs["road_removal"] = round(request.road_miles * 40000, 2)

        # Project management and contingency (15%)
        subtotal = sum(costs.values())
        costs["project_management_contingency"] = round(subtotal * 0.15, 2)

        # Salvage value (minimal for degraded panels)
        salvage = round(request.capacity_mw * 2000, 2)  # Minimal panel scrap
        notes.append("Solar panel salvage value is minimal for end-of-life degraded panels")

        restoration_months = 24

    total_removal = round(sum(costs.values()), 2)
    net_cost = round(total_removal - salvage, 2)
    # Recommend 125% bond, credit salvage at max 50%
    adjusted_salvage = min(salvage, total_removal * 0.25)  # Cap salvage credit at 25%
    bond_amount = round((total_removal - adjusted_salvage) * 1.25, 2)
    cost_per_mw = round(net_cost / request.capacity_mw, 2) if request.capacity_mw > 0 else 0

    notes.append(f"Bond recommendation: 125% of net cost after capped salvage credit")
    notes.append(f"Salvage credit capped at 25% of total removal cost (${adjusted_salvage:,.2f})")

    return DecommissioningEstimate(
        project_type=request.project_type,
        capacity_mw=request.capacity_mw,
        component_costs=costs,
        total_removal_cost=total_removal,
        estimated_salvage_value=salvage,
        net_decommissioning_cost=net_cost,
        recommended_bond_amount=bond_amount,
        bond_multiple=1.25,
        restoration_timeline_months=restoration_months,
        cost_per_mw=cost_per_mw,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Setback Calculator
# ---------------------------------------------------------------------------
class SetbackRequest(BaseModel):
    """Request for setback distance calculations."""
    project_type: str = Field(..., description="wind or solar")
    turbine_hub_height_m: float = Field(default=100, description="Turbine hub height meters")
    rotor_diameter_m: float = Field(default=150, description="Rotor diameter meters")
    county: str = Field(default="", description="Texas county for regulation lookup")


class SetbackResult(BaseModel):
    """Setback calculation results."""
    project_type: str
    turbine_tip_height_m: float
    turbine_tip_height_ft: float
    setbacks: dict[str, dict[str, Any]]
    county_regulation: str
    notes: list[str]


COUNTY_SETBACK_OVERRIDES: dict[str, dict[str, int]] = {
    "nolan": {"dwelling_ft": 2000, "property_line_ft": 1000, "road_ft": 500},
    "taylor": {"dwelling_ft": 1500, "property_line_ft": 1000, "road_ft": 500},
    "shackelford": {"dwelling_ft": 2000, "property_line_ft": 1100, "road_ft": 500},
    "callahan": {"dwelling_ft": 1500, "property_line_ft": 900, "road_ft": 500},
    "fisher": {"dwelling_ft": 1500, "property_line_ft": 800, "road_ft": 500},
    "jones": {"dwelling_ft": 1500, "property_line_ft": 1000, "road_ft": 500},
    "coke": {"dwelling_ft": 1500, "property_line_ft": 1000, "road_ft": 500},
    "sterling": {"dwelling_ft": 1500, "property_line_ft": 800, "road_ft": 500},
}


def calculate_setbacks(request: SetbackRequest) -> SetbackResult:
    """Calculate recommended setback distances."""
    tip_height_m = request.turbine_hub_height_m + (request.rotor_diameter_m / 2)
    tip_height_ft = round(tip_height_m * 3.28084, 1)
    notes: list[str] = []

    if request.project_type == "wind":
        # Standard setbacks
        property_line_ft = round(tip_height_ft * 1.1, 0)
        dwelling_ft = max(1500, property_line_ft * 2.5)
        road_ft = max(500, tip_height_ft * 1.1)
        noise_ft = max(1000, dwelling_ft * 0.75)

        setbacks = {
            "property_line": {
                "distance_ft": property_line_ft,
                "distance_m": round(property_line_ft / 3.28084, 1),
                "basis": "1.1x tip height",
                "required": True,
            },
            "occupied_dwelling": {
                "distance_ft": dwelling_ft,
                "distance_m": round(dwelling_ft / 3.28084, 1),
                "basis": "Maximum of 1,500 ft or 2.5x property line setback",
                "required": True,
            },
            "public_road": {
                "distance_ft": road_ft,
                "distance_m": round(road_ft / 3.28084, 1),
                "basis": "Maximum of 500 ft or 1.1x tip height",
                "required": True,
            },
            "noise_boundary": {
                "distance_ft": noise_ft,
                "distance_m": round(noise_ft / 3.28084, 1),
                "basis": "45 dBA contour at non-participating residence",
                "required": True,
            },
            "shadow_flicker": {
                "distance_ft": round(dwelling_ft * 1.5, 0),
                "distance_m": round(dwelling_ft * 1.5 / 3.28084, 1),
                "basis": "30 hours/year maximum flicker at receptor",
                "required": True,
            },
        }

        # County override check
        county_lower = request.county.lower().strip()
        county_reg = "No county-specific regulation identified"
        if county_lower in COUNTY_SETBACK_OVERRIDES:
            county_data = COUNTY_SETBACK_OVERRIDES[county_lower]
            county_reg = f"{request.county} County has adopted wind energy regulations"
            for key, county_val in county_data.items():
                if key in setbacks:
                    current = setbacks[key]["distance_ft"]
                    if county_val > current:
                        setbacks[key]["distance_ft"] = county_val
                        setbacks[key]["distance_m"] = round(county_val / 3.28084, 1)
                        notes.append(
                            f"County regulation increases {key} from {current:.0f} to {county_val} ft"
                        )

        if tip_height_ft > 600:
            notes.append(f"FAA notification required for structures over 200 ft AGL (tip height: {tip_height_ft:.0f} ft)")

    else:  # solar
        setbacks = {
            "property_line": {
                "distance_ft": 150,
                "distance_m": round(150 / 3.28084, 1),
                "basis": "Minimum 100-300 ft from property lines",
                "required": True,
            },
            "occupied_dwelling": {
                "distance_ft": 500,
                "distance_m": round(500 / 3.28084, 1),
                "basis": "Minimum 500 ft from occupied structures",
                "required": True,
            },
            "public_road": {
                "distance_ft": 100,
                "distance_m": round(100 / 3.28084, 1),
                "basis": "Minimum 100 ft from public roads with screening",
                "required": True,
            },
            "vegetative_buffer": {
                "distance_ft": 50,
                "distance_m": round(50 / 3.28084, 1),
                "basis": "25-50 ft vegetative screening along property lines",
                "required": True,
            },
            "water_feature": {
                "distance_ft": 200,
                "distance_m": round(200 / 3.28084, 1),
                "basis": "200 ft from water wells, streams, wetlands",
                "required": True,
            },
        }
        county_reg = "Solar setbacks primarily contractual in Texas"
        notes.append("Texas has no statewide solar setback requirements")

    return SetbackResult(
        project_type=request.project_type,
        turbine_tip_height_m=tip_height_m if request.project_type == "wind" else 0,
        turbine_tip_height_ft=tip_height_ft if request.project_type == "wind" else 0,
        setbacks=setbacks,
        county_regulation=county_reg,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Tax Incentive Analyzer
# ---------------------------------------------------------------------------
class TaxIncentiveRequest(BaseModel):
    """Request for tax incentive analysis."""
    project_type: str = Field(..., description="wind or solar")
    capacity_mw: float = Field(..., gt=0)
    total_project_cost: float = Field(..., gt=0, description="Total project cost in dollars")
    placed_in_service_year: int = Field(default=2026, ge=2024, le=2035)
    meets_prevailing_wage: bool = Field(default=True)
    meets_apprenticeship: bool = Field(default=True)
    domestic_content: bool = Field(default=False)
    energy_community: bool = Field(default=False)
    low_income_community: bool = Field(default=False)
    estimated_annual_mwh: float = Field(default=0, ge=0)
    credit_election: str = Field(default="auto", description="ptc, itc, or auto")


class TaxIncentiveAnalysis(BaseModel):
    """Tax incentive analysis result."""
    project_type: str
    capacity_mw: float
    total_project_cost: float
    elected_credit: str
    base_credit_rate: str
    effective_credit_rate: str
    bonus_adders: list[dict[str, Any]]
    total_credit_value: float
    credit_per_mw: float
    macrs_depreciation_value: float
    total_federal_benefit: float
    effective_subsidy_rate: float
    ptc_analysis: Optional[dict[str, Any]]
    itc_analysis: Optional[dict[str, Any]]
    recommendation: str
    notes: list[str]


def analyze_tax_incentives(request: TaxIncentiveRequest) -> TaxIncentiveAnalysis:
    """Analyze federal tax incentives for renewable energy project."""
    notes: list[str] = []
    bonus_adders: list[dict[str, Any]] = []

    # Determine base credit rates
    meets_labor = request.meets_prevailing_wage and request.meets_apprenticeship
    ptc_base = 0.0275 if meets_labor else 0.003  # $/kWh (2024 value, inflation adjusted)
    itc_base = 0.30 if meets_labor else 0.06  # Percentage

    # Bonus adders
    total_bonus_pct = 0.0
    if request.domestic_content:
        total_bonus_pct += 0.10
        bonus_adders.append({"type": "Domestic Content", "value": "10%", "qualified": True})
    if request.energy_community:
        total_bonus_pct += 0.10
        bonus_adders.append({"type": "Energy Community", "value": "10%", "qualified": True})
    if request.low_income_community:
        total_bonus_pct += 0.10
        bonus_adders.append({"type": "Low-Income Community", "value": "10%", "qualified": True})

    # PTC calculation (10-year credit)
    ptc_annual = request.estimated_annual_mwh * ptc_base * 1000  # Convert $/kWh to $/MWh
    ptc_10yr = ptc_annual * 10
    ptc_with_bonus = ptc_10yr * (1 + total_bonus_pct / (0.30 if meets_labor else 0.06))

    ptc_analysis = {
        "base_rate_per_kwh": ptc_base,
        "annual_credit": round(ptc_annual, 2),
        "10_year_total": round(ptc_10yr, 2),
        "with_bonuses": round(ptc_with_bonus, 2),
        "npv_at_8pct": round(sum(
            ptc_annual / (1.08 ** yr) for yr in range(1, 11)
        ), 2),
    }

    # ITC calculation (one-time credit)
    itc_rate = itc_base + total_bonus_pct
    itc_credit = request.total_project_cost * itc_rate
    itc_analysis = {
        "base_rate": itc_base,
        "effective_rate": itc_rate,
        "credit_amount": round(itc_credit, 2),
        "recapture_period_years": 5,
        "basis_reduction": round(itc_credit * 0.50, 2),
    }

    # MACRS depreciation value (5-year, approximate 40% PV of tax shield at 21% rate)
    bonus_dep_pct = max(0, 1.0 - (request.placed_in_service_year - 2026) * 0.20)
    if request.placed_in_service_year <= 2026:
        bonus_dep_pct = 1.0
    depreciable_basis = request.total_project_cost
    if itc_rate > 0:
        depreciable_basis -= itc_credit * 0.50  # ITC basis reduction

    macrs_value = round(depreciable_basis * 0.21 * 0.90 * bonus_dep_pct, 2)  # Approximate PV of tax shield

    # Credit election logic
    if request.credit_election == "auto":
        if ptc_analysis["npv_at_8pct"] > itc_credit:
            elected = "PTC"
            total_credit = ptc_with_bonus
            notes.append("PTC elected: NPV exceeds ITC value")
        else:
            elected = "ITC"
            total_credit = itc_credit
            notes.append("ITC elected: Upfront credit exceeds PTC NPV")
    elif request.credit_election == "ptc":
        elected = "PTC"
        total_credit = ptc_with_bonus
    else:
        elected = "ITC"
        total_credit = itc_credit

    total_federal = total_credit + macrs_value
    subsidy_rate = total_federal / request.total_project_cost if request.total_project_cost > 0 else 0

    if not meets_labor:
        notes.append("WARNING: Not meeting prevailing wage/apprenticeship reduces credit by ~80%")
    if bonus_dep_pct < 1.0:
        notes.append(f"Bonus depreciation at {bonus_dep_pct:.0%} for {request.placed_in_service_year}")

    effective_rate = f"{itc_rate:.0%}" if elected == "ITC" else f"{ptc_base*100:.2f} cents/kWh"

    return TaxIncentiveAnalysis(
        project_type=request.project_type,
        capacity_mw=request.capacity_mw,
        total_project_cost=request.total_project_cost,
        elected_credit=elected,
        base_credit_rate=f"{itc_base:.0%}" if elected == "ITC" else f"{ptc_base*100:.2f} cents/kWh",
        effective_credit_rate=effective_rate,
        bonus_adders=bonus_adders,
        total_credit_value=round(total_credit, 2),
        credit_per_mw=round(total_credit / request.capacity_mw, 2),
        macrs_depreciation_value=macrs_value,
        total_federal_benefit=round(total_federal, 2),
        effective_subsidy_rate=round(subsidy_rate, 4),
        ptc_analysis=ptc_analysis,
        itc_analysis=itc_analysis,
        recommendation=f"Elect {elected} for this project configuration.",
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Additional API Endpoints
# ---------------------------------------------------------------------------
@app.post("/analyze/formatted")
async def analyze_formatted(request: QueryRequest) -> dict[str, Any]:
    """Analysis endpoint with mode-specific formatting."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    request.mode = request.mode.upper()
    request.zone = request.zone.upper()
    response = engine.analyze(request)

    formatter = ResponseFormatter()
    if request.mode == "FAST":
        return formatter.format_fast(response)
    elif request.mode == "DEFENSE":
        return formatter.format_defense(response)
    elif request.mode == "MEMO":
        return formatter.format_memo(response)
    return response.model_dump()


@app.post("/calculate/payments")
async def calculate_payments_endpoint(scenario: PaymentScenario) -> dict[str, Any]:
    """Calculate lease payment projections."""
    projection = calculate_lease_payments(scenario)
    return projection.model_dump()


@app.post("/calculate/decommissioning")
async def calculate_decommissioning_endpoint(
    request: DecommissioningEstimateRequest,
) -> dict[str, Any]:
    """Estimate decommissioning costs."""
    estimate = estimate_decommissioning_cost(request)
    return estimate.model_dump()


@app.post("/calculate/setbacks")
async def calculate_setbacks_endpoint(request: SetbackRequest) -> dict[str, Any]:
    """Calculate recommended setback distances."""
    result = calculate_setbacks(request)
    return result.model_dump()


@app.post("/calculate/tax-incentives")
async def calculate_tax_incentives_endpoint(
    request: TaxIncentiveRequest,
) -> dict[str, Any]:
    """Analyze federal tax incentives for renewable energy project."""
    analysis = analyze_tax_incentives(request)
    return analysis.model_dump()


@app.post("/compare/leases")
async def compare_leases_endpoint(request: LeaseComparisonRequest) -> dict[str, Any]:
    """Compare multiple lease offers."""
    comparison = compare_lease_offers(request)
    return comparison.model_dump()


@app.post("/negotiate/positions")
async def negotiate_positions_endpoint(request: NegotiationRequest) -> dict[str, Any]:
    """Generate negotiation positions for specified topics."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    positions = generate_negotiation_positions(request, engine._doctrine_map)
    return {
        "engine_id": ENGINE_ID,
        "perspective": request.perspective,
        "aggressiveness": request.aggressiveness,
        "position_count": len(positions),
        "positions": [p.model_dump() for p in positions],
    }


@app.get("/standard-terms")
async def get_standard_terms(
    project_type: str = Query(default="wind", description="wind or solar"),
) -> dict[str, Any]:
    """Get standard lease terms database for comparison."""
    terms: list[dict[str, Any]] = []
    for key, term in STANDARD_LEASE_TERMS.items():
        terms.append({
            "term": key,
            "description": term["description"],
            "standard": term.get(f"{project_type}_standard", "N/A"),
            "importance": term["importance"],
            "landowner_preference": term["landowner_preference"],
        })
    return {
        "engine_id": ENGINE_ID,
        "project_type": project_type,
        "term_count": len(terms),
        "terms": terms,
    }


@app.get("/county-regulations")
async def get_county_regulations() -> dict[str, Any]:
    """Get known county wind energy regulation overrides."""
    return {
        "engine_id": ENGINE_ID,
        "county_count": len(COUNTY_SETBACK_OVERRIDES),
        "counties": {
            county: {
                "dwelling_setback_ft": data["dwelling_ft"],
                "property_line_setback_ft": data["property_line_ft"],
                "road_setback_ft": data["road_ft"],
            }
            for county, data in COUNTY_SETBACK_OVERRIDES.items()
        },
        "note": "Texas has no statewide wind/solar setback law. These are known county regulations.",
    }


@app.get("/issue-categories")
async def get_issue_categories() -> dict[str, Any]:
    """Get all issue categories and their doctrine counts."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    cat_counts: dict[str, int] = defaultdict(int)
    for d in engine._doctrines:
        cat_counts[d.issue_category] += 1
    return {
        "engine_id": ENGINE_ID,
        "category_count": len(cat_counts),
        "categories": [
            {"category": cat, "doctrine_count": count}
            for cat, count in sorted(cat_counts.items())
        ],
    }


@app.get("/authority-weights")
async def get_authority_weights() -> dict[str, Any]:
    """Get the authority weight hierarchy."""
    return {
        "engine_id": ENGINE_ID,
        "weights": AUTHORITY_WEIGHTS,
        "description": "Higher weight = stronger legal authority. Scale 0.0 to 1.0.",
    }


@app.get("/info")
async def get_engine_info() -> dict[str, Any]:
    """Get comprehensive engine information."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "doctrine_count": len(engine._doctrines),
        "issue_categories": len(set(d.issue_category for d in engine._doctrines)),
        "interaction_edges": sum(len(v) for v in INTERACTION_GRAPH.values()),
        "authority_levels": len(AUTHORITY_WEIGHTS),
        "standard_terms_tracked": len(STANDARD_LEASE_TERMS),
        "county_regulations_tracked": len(COUNTY_SETBACK_OVERRIDES),
        "tie_components": [
            "three_layer_response", "response_modes", "doctrine_cache",
            "authority_hardening", "confidence_stratification",
            "semantic_normalization", "vector_search", "telemetry",
            "drift_watcher", "coverage_map", "metrics_collector",
            "health_endpoint", "zoned_analysis", "fact_fragility_scoring",
            "audit_trail_jsonl", "determinism_hash_sha256", "fastapi_server",
            "loguru_logging", "multi_doctrine_decomposition", "deep_analysis_mode",
        ],
        "endpoints": [
            "/health", "/metrics", "/coverage", "/doctrines", "/doctrine/{topic}",
            "/analyze", "/analyze/fast", "/analyze/defense", "/analyze/memo",
            "/analyze/formatted", "/calculate/payments", "/calculate/decommissioning",
            "/calculate/setbacks", "/calculate/tax-incentives", "/compare/leases",
            "/negotiate/positions", "/standard-terms", "/county-regulations",
            "/issue-categories", "/authority-weights", "/traces", "/errors",
            "/drift", "/interaction-graph", "/info",
        ],
    }


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    logger.info("Launching {name} on port {port}", name=ENGINE_NAME, port=ENGINE_PORT)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )