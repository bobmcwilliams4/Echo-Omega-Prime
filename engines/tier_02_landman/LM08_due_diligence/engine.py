"""
LM08 Due Diligence Engine
===========================
TIE Gold Standard engine for oil & gas acquisition due diligence intelligence.

Engine ID: LM08
Name: Due Diligence
Port: 8508
Version: 1.0.0
TIE Standard: TIE-20 Gold (all 20 mandatory components)

Domain Coverage:
  - Title due diligence checklist and methodology
  - Environmental due diligence (Phase I/II ESA, ASTM E1527-21)
  - Regulatory compliance audit
  - Production history analysis and decline curve review
  - Reserve estimation review (SEC vs PRMS classifications)
  - Lease status verification (HBP, non-producing, expiring)
  - Lien and encumbrance search
  - Pending litigation review
  - Preferential purchase rights (ROFR) analysis
  - Consent to assign requirements
  - Change of control provisions
  - Area of mutual interest (AMI) agreements
  - Deficiency identification and cure requirements
  - Purchase and sale agreement (PSA) review
  - Representations and warranties analysis
  - Indemnification provisions
  - Title defect assertion and cure period
  - Net revenue interest vs working interest verification
  - Suspense account analysis
  - Operator qualification review

TIE-20 Components:
  1.  three_layer_response
  2.  response_modes
  3.  doctrine_cache
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

import hashlib
import json
import os
import sys
import time
import uuid
from contextlib import asynccontextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from loguru import logger

# ─────────────────────────────────────────────────────────────────────────────
# LOGURU CONFIGURATION (TIE-18: loguru_logging)
# ─────────────────────────────────────────────────────────────────────────────
LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LM08_due_diligence/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level:<8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
)
logger.add(
    LOG_DIR / "engine.log",
    rotation="50 MB",
    retention="30 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} | {message}",
)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
ENGINE_ID = "LM08"
ENGINE_NAME = "Due Diligence"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8508
ENGINE_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LM08_due_diligence")

BANNED_PHRASES = [
    "I think",
    "I believe",
    "probably",
    "maybe",
    "it seems",
    "in my opinion",
    "I would guess",
    "I feel",
    "it appears that",
    "you should consider",
    "one might argue",
    "it could be said",
]

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS FROM SIBLING MODULES
# ─────────────────────────────────────────────────────────────────────────────
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DOCTRINE_CACHE,
    ConfidenceLevel,
    DoctrineBlock,
    IssueCategory,
    PositionZone,
    get_doctrine_by_topic,
    get_doctrine_cache,
    get_doctrine_topics,
    get_doctrines_by_category,
    search_doctrines,
)
from search import DueDiligenceSearchEngine, SearchResult
from semantic import DueDiligenceSemanticNormalizer, NormalizationResult, SemanticDomain
from telemetry import (
    AuditTrail,
    CoverageMap,
    DriftWatcher,
    DueDiligenceTelemetry,
    ErrorDomain,
    MetricsCollector,
    QueryPhase,
    QueryTrace,
)

# ─────────────────────────────────────────────────────────────────────────────
# CLOUD KNOWLEDGE RETRIEVER INTEGRATION
# ─────────────────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))
try:
    from cloud_retriever import CognitionCloudRetriever, CloudKnowledge, retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
    logger.info("Cloud retriever available — Cognition Cloud integration enabled")
except ImportError:
    _CLOUD_AVAILABLE = False
    logger.warning("cloud_retriever not available — running without cloud knowledge")

# ─────────────────────────────────────────────────────────────────────────────
# PYDANTIC MODELS FOR ALL I/O
# ─────────────────────────────────────────────────────────────────────────────
try:
    from pydantic import BaseModel, Field
except ImportError:
    logger.warning("Pydantic not available — using dataclass fallback")
    from dataclasses import dataclass as BaseModel  # type: ignore[assignment]

    def Field(default: Any = None, **kwargs: Any) -> Any:  # type: ignore[misc]
        return default


class ResponseMode(str, Enum):
    """Response modes for the engine."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class QueryRequest(BaseModel):
    """Input model for a due diligence query."""
    query: str = Field(..., description="The due diligence question or scenario")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    position_zone: Optional[str] = Field(default=None, description="BUYER, SELLER, or NEUTRAL")
    issue_categories: Optional[List[str]] = Field(default=None, description="Filter by issue categories")
    max_doctrines: int = Field(default=5, description="Maximum doctrine blocks to return")
    include_authorities: bool = Field(default=True, description="Include primary authorities")
    include_counter_arguments: bool = Field(default=True, description="Include counter-arguments")
    deep_analysis: bool = Field(default=False, description="Enable deep analysis mode")


class DoctrineResponse(BaseModel):
    """A single doctrine match in the response."""
    topic: str = Field(..., description="Doctrine topic identifier")
    conclusion: str = Field(..., description="Conclusion template")
    confidence: str = Field(..., description="Confidence level")
    issue_category: str = Field(..., description="Issue category")
    position_zone: str = Field(..., description="Position zone")
    key_factors: List[str] = Field(default_factory=list, description="Key factors")
    authorities: List[str] = Field(default_factory=list, description="Primary authorities")
    counter_arguments: List[str] = Field(default_factory=list, description="Counter-arguments")
    resolution_strategy: str = Field(default="", description="Resolution strategy")
    interaction_edges: List[str] = Field(default_factory=list, description="Related doctrine topics")


class AnalysisLayer(BaseModel):
    """Response layer from three-layer analysis."""
    layer: str = Field(..., description="Layer name: doctrine_cache, semantic_retrieval, or deep_analysis")
    latency_ms: float = Field(..., description="Processing latency in milliseconds")
    results_count: int = Field(default=0, description="Number of results from this layer")
    doctrines: List[DoctrineResponse] = Field(default_factory=list, description="Matched doctrines")


class FragilityScore(BaseModel):
    """Fact fragility scoring for a conclusion."""
    verifiability: float = Field(..., description="How verifiable is the factual basis (0-1)")
    recharacterization_risk: float = Field(..., description="Risk that facts could be recharacterized (0-1)")
    testimony_dependence: float = Field(..., description="Dependence on testimonial evidence (0-1)")
    document_dependence: float = Field(..., description="Dependence on documentary evidence (0-1)")
    overall_fragility: float = Field(..., description="Overall fragility score (0-1)")
    assessment: str = Field(..., description="Narrative assessment of fragility")


class DecomposedIssue(BaseModel):
    """A decomposed issue from multi-doctrine decomposition."""
    issue_id: str = Field(..., description="Unique issue identifier")
    category: str = Field(..., description="Issue category")
    description: str = Field(..., description="Issue description")
    doctrines_applicable: List[str] = Field(default_factory=list, description="Applicable doctrines")
    interaction_graph: List[str] = Field(default_factory=list, description="Related issues")
    resolution_priority: int = Field(default=0, description="Resolution priority (1=highest)")


class QueryResponse(BaseModel):
    """Complete response to a due diligence query."""
    engine_id: str = Field(default=ENGINE_ID)
    engine_version: str = Field(default=ENGINE_VERSION)
    query: str = Field(..., description="Original query text")
    mode: str = Field(..., description="Response mode used")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    layers: List[AnalysisLayer] = Field(default_factory=list, description="Three-layer analysis results")
    total_latency_ms: float = Field(default=0.0, description="Total processing time")
    confidence_level: str = Field(default="DEFENSIBLE", description="Overall confidence")
    position_zone: str = Field(default="NEUTRAL", description="Analysis position zone")
    decomposed_issues: List[DecomposedIssue] = Field(default_factory=list, description="Multi-doctrine decomposition")
    fragility_score: Optional[FragilityScore] = Field(default=None, description="Fact fragility assessment")
    disclosure_caveat: str = Field(default="", description="Epistemic guardrail disclosure")
    determinism_hash: str = Field(default="", description="SHA-256 determinism hash")
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    issue_categories_triggered: List[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    """Health check response model."""
    engine_id: str = Field(default=ENGINE_ID)
    engine_name: str = Field(default=ENGINE_NAME)
    version: str = Field(default=ENGINE_VERSION)
    status: str = Field(default="healthy")
    uptime_seconds: float = Field(default=0.0)
    doctrine_count: int = Field(default=0)
    issue_categories: int = Field(default=0)
    semantic_terms: int = Field(default=0)
    search_index_docs: int = Field(default=0)
    telemetry_summary: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ─────────────────────────────────────────────────────────────────────────────
# AUTHORITY HARDENING (TIE-4)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class AuthoritySource:
    """An authority source with weight and conflict resolution priority."""
    level: int
    name: str
    weight: float
    description: str


AUTHORITY_HIERARCHY: List[AuthoritySource] = [
    AuthoritySource(1, "State Statutes & Regulations", 1.0,
                    "Enacted statutes and promulgated regulations with force of law"),
    AuthoritySource(2, "Federal Regulations (EPA, BLM, SEC)", 0.95,
                    "Federal regulatory requirements applicable to oil and gas operations"),
    AuthoritySource(3, "State Court Decisions", 0.90,
                    "Appellate and supreme court decisions interpreting statutes and common law"),
    AuthoritySource(4, "AAPL Standards & Model Forms", 0.85,
                    "Industry standards from American Association of Professional Landmen"),
    AuthoritySource(5, "Industry Practice & Custom", 0.75,
                    "Widely accepted practices in oil and gas acquisition transactions"),
    AuthoritySource(6, "Treatises & Commentary", 0.65,
                    "Academic and practitioner treatises (Williams & Meyers, Kuntz, etc.)"),
]


def resolve_authority_conflict(authorities: List[str]) -> Tuple[str, float]:
    """Resolve conflicting authorities by hierarchy weight.

    Args:
        authorities: List of authority citation strings.

    Returns:
        Tuple of (winning authority name, confidence weight).
    """
    if not authorities:
        return ("No authority cited", 0.0)

    best_weight = 0.0
    best_authority = authorities[0]
    for auth_str in authorities:
        auth_lower = auth_str.lower()
        for source in AUTHORITY_HIERARCHY:
            if any(keyword in auth_lower for keyword in source.name.lower().split()):
                if source.weight > best_weight:
                    best_weight = source.weight
                    best_authority = auth_str
                break
    return (best_authority, best_weight)


def compute_authority_score(doctrine: DoctrineBlock) -> float:
    """Compute an authority score for a doctrine block based on its cited authorities.

    Args:
        doctrine: The doctrine block to score.

    Returns:
        Authority score between 0.0 and 1.0.
    """
    if not doctrine.primary_authority:
        return 0.3

    total_weight = 0.0
    matched = 0
    for auth in doctrine.primary_authority:
        auth_lower = auth.lower()
        for source in AUTHORITY_HIERARCHY:
            keywords = source.name.lower().split()
            if any(kw in auth_lower for kw in keywords):
                total_weight += source.weight
                matched += 1
                break
        else:
            total_weight += 0.5
            matched += 1

    return min(total_weight / max(matched, 1), 1.0)


# ─────────────────────────────────────────────────────────────────────────────
# CONFIDENCE STRATIFICATION (TIE-5)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ConfidenceAssessment:
    """Assessment of confidence in a conclusion."""
    level: ConfidenceLevel
    score: float
    authority_score: float
    doctrine_coverage: float
    fragility_factor: float
    reasoning: str

    @property
    def stratification_label(self) -> str:
        """Return human-readable stratification label."""
        labels = {
            ConfidenceLevel.DEFENSIBLE: "Position is well-supported by authority and practice; suitable for reliance.",
            ConfidenceLevel.AGGRESSIVE: "Position has support but involves judgment calls; disclose basis to client.",
            ConfidenceLevel.DISCLOSURE: "Position requires full disclosure of uncertainty and alternative interpretations.",
            ConfidenceLevel.HIGH_RISK: "Position involves significant risk of adverse outcome; proceed with caution.",
        }
        return labels.get(self.level, "Unknown confidence level.")


def assess_confidence(
    doctrine: DoctrineBlock,
    query_specificity: float = 0.7,
    fact_completeness: float = 0.8,
) -> ConfidenceAssessment:
    """Assess confidence in a doctrine-based conclusion.

    Args:
        doctrine: The doctrine block being applied.
        query_specificity: How specific the query is to the doctrine (0-1).
        fact_completeness: How complete the factual basis is (0-1).

    Returns:
        ConfidenceAssessment with level and scores.
    """
    authority_score = compute_authority_score(doctrine)
    doctrine_coverage = query_specificity * 0.6 + fact_completeness * 0.4
    fragility_factor = 1.0 - (len(doctrine.counter_arguments) * 0.05)
    fragility_factor = max(fragility_factor, 0.3)

    composite = (authority_score * 0.4 + doctrine_coverage * 0.35 + fragility_factor * 0.25)

    if composite >= 0.80:
        level = ConfidenceLevel.DEFENSIBLE
        reasoning = (
            f"Authority score ({authority_score:.2f}) and doctrine coverage ({doctrine_coverage:.2f}) "
            f"support a defensible position. Counter-argument exposure is manageable."
        )
    elif composite >= 0.60:
        level = ConfidenceLevel.AGGRESSIVE
        reasoning = (
            f"Authority is present ({authority_score:.2f}) but query specificity or factual completeness "
            f"reduces confidence. Position involves professional judgment."
        )
    elif composite >= 0.40:
        level = ConfidenceLevel.DISCLOSURE
        reasoning = (
            f"Significant uncertainty exists. Authority score ({authority_score:.2f}) and coverage "
            f"({doctrine_coverage:.2f}) suggest disclosure of alternatives is required."
        )
    else:
        level = ConfidenceLevel.HIGH_RISK
        reasoning = (
            f"Low authority ({authority_score:.2f}) and coverage ({doctrine_coverage:.2f}). "
            f"Position carries substantial risk. Recommend conservative approach."
        )

    return ConfidenceAssessment(
        level=level,
        score=round(composite, 4),
        authority_score=round(authority_score, 4),
        doctrine_coverage=round(doctrine_coverage, 4),
        fragility_factor=round(fragility_factor, 4),
        reasoning=reasoning,
    )


# ─────────────────────────────────────────────────────────────────────────────
# ZONED ANALYSIS (TIE-13)
# ─────────────────────────────────────────────────────────────────────────────

class AnalysisZone(str, Enum):
    """Analysis zones — never blur perspectives."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


@dataclass
class ZonedResult:
    """Result scoped to a specific analysis zone."""
    zone: AnalysisZone
    position: PositionZone
    content: str
    caveats: List[str]
    applicable_doctrines: List[str]


def apply_zoned_analysis(
    query: str,
    doctrines: List[DoctrineBlock],
    zone: AnalysisZone = AnalysisZone.PLANNING,
    position: PositionZone = PositionZone.NEUTRAL,
) -> ZonedResult:
    """Apply zoned analysis to a query with position-specific framing.

    Args:
        query: The original query text.
        doctrines: Matched doctrine blocks.
        zone: The analysis zone (PLANNING, REPORTING, AUDIT).
        position: The position zone (BUYER, SELLER, NEUTRAL).

    Returns:
        ZonedResult with zone-appropriate content.
    """
    applicable = [d.topic for d in doctrines]
    caveats: List[str] = []

    if zone == AnalysisZone.PLANNING:
        content_parts = []
        for d in doctrines:
            if position == PositionZone.BUYER:
                content_parts.append(
                    f"[BUYER PLANNING] {d.topic}: {d.conclusion_template} "
                    f"Resolution: {d.resolution_strategy}"
                )
            elif position == PositionZone.SELLER:
                content_parts.append(
                    f"[SELLER PLANNING] {d.topic}: Adversary position: {d.adversary_position} "
                    f"Counter-arguments available: {len(d.counter_arguments)}"
                )
            else:
                content_parts.append(
                    f"[NEUTRAL PLANNING] {d.topic}: {d.conclusion_template}"
                )
        content = "\n\n".join(content_parts)
        caveats.append("Planning analysis — not a legal opinion. Verify with counsel.")

    elif zone == AnalysisZone.REPORTING:
        content_parts = []
        for d in doctrines:
            content_parts.append(
                f"[REPORTING] {d.topic}\n"
                f"  Category: {d.issue_category.value}\n"
                f"  Confidence: {d.confidence.value} — {d.confidence_stratification}\n"
                f"  Conclusion: {d.conclusion_template}\n"
                f"  Key Factors: {'; '.join(d.key_factors[:4])}\n"
                f"  Burden: {d.burden_holder}"
            )
        content = "\n\n".join(content_parts)
        caveats.append("Reporting zone — factual summary for documentation purposes.")

    elif zone == AnalysisZone.AUDIT:
        content_parts = []
        for d in doctrines:
            content_parts.append(
                f"[AUDIT] {d.topic}\n"
                f"  Authority: {'; '.join(d.primary_authority)}\n"
                f"  Controlling Precedent: {d.controlling_precedent}\n"
                f"  Counter-Arguments ({len(d.counter_arguments)}): "
                f"{'; '.join(d.counter_arguments[:3])}\n"
                f"  Adversary Position: {d.adversary_position}\n"
                f"  Confidence Stratification: {d.confidence_stratification}"
            )
        content = "\n\n".join(content_parts)
        caveats.append("Audit zone — full adversarial analysis for litigation readiness.")

    else:
        content = "Unknown zone."

    return ZonedResult(
        zone=zone,
        position=position,
        content=content,
        caveats=caveats,
        applicable_doctrines=applicable,
    )


# ─────────────────────────────────────────────────────────────────────────────
# FACT FRAGILITY SCORING (TIE-14)
# ─────────────────────────────────────────────────────────────────────────────

def compute_fact_fragility(
    doctrine: DoctrineBlock,
    factual_basis: str = "",
) -> FragilityScore:
    """Compute fact fragility score for a doctrine application.

    Args:
        doctrine: The doctrine block being applied.
        factual_basis: Description of the factual basis (if provided).

    Returns:
        FragilityScore with component scores and assessment.
    """
    # Verifiability: how much depends on verifiable records vs. subjective judgment
    verifiability = 0.8  # Default: most due diligence is record-based
    if doctrine.issue_category in (
        IssueCategory.PRODUCTION_ANALYSIS,
        IssueCategory.RESERVE_ESTIMATION,
    ):
        verifiability = 0.6  # Engineering judgment involved
    elif doctrine.issue_category in (
        IssueCategory.REPS_WARRANTIES,
        IssueCategory.INDEMNIFICATION,
    ):
        verifiability = 0.7  # Contract interpretation

    # Recharacterization risk: how easily could facts be recharacterized
    recharacterization_risk = len(doctrine.counter_arguments) * 0.08
    recharacterization_risk = min(recharacterization_risk, 0.8)

    # Testimony dependence: how much relies on testimony vs. documents
    testimony_dependence = 0.2  # Default low — most due diligence is documentary
    if "knowledge" in doctrine.reasoning_framework.lower():
        testimony_dependence = 0.4
    if "interview" in doctrine.reasoning_framework.lower():
        testimony_dependence = 0.5

    # Document dependence
    document_dependence = 1.0 - testimony_dependence

    # Overall fragility
    overall = (
        (1.0 - verifiability) * 0.3
        + recharacterization_risk * 0.3
        + testimony_dependence * 0.2
        + (1.0 - document_dependence) * 0.2
    )

    if overall < 0.3:
        assessment = (
            "Low fragility. The factual basis is primarily documentary and verifiable. "
            "Conclusions are robust against adversarial challenge."
        )
    elif overall < 0.5:
        assessment = (
            "Moderate fragility. Some elements depend on interpretation or judgment. "
            "Document the basis for key conclusions and preserve supporting records."
        )
    elif overall < 0.7:
        assessment = (
            "Elevated fragility. Significant reliance on subjective judgment or testimonial "
            "evidence. Consider obtaining corroborating documentation or expert opinions."
        )
    else:
        assessment = (
            "High fragility. Conclusions are highly dependent on judgment, interpretation, "
            "or contested facts. Recommend full disclosure of uncertainty and alternative "
            "interpretations."
        )

    return FragilityScore(
        verifiability=round(verifiability, 3),
        recharacterization_risk=round(recharacterization_risk, 3),
        testimony_dependence=round(testimony_dependence, 3),
        document_dependence=round(document_dependence, 3),
        overall_fragility=round(overall, 3),
        assessment=assessment,
    )


# ─────────────────────────────────────────────────────────────────────────────
# MULTI-DOCTRINE DECOMPOSITION (TIE-19)
# ─────────────────────────────────────────────────────────────────────────────

def decompose_query(
    query: str,
    matched_doctrines: List[DoctrineBlock],
) -> List[DecomposedIssue]:
    """Decompose a complex query into individual issues with doctrine mapping.

    Args:
        query: The original query text.
        matched_doctrines: Doctrine blocks matched to the query.

    Returns:
        List of DecomposedIssue objects with interaction graphs.
    """
    if not matched_doctrines:
        return []

    issues: List[DecomposedIssue] = []
    categories_seen: Dict[str, List[str]] = {}

    for i, doctrine in enumerate(matched_doctrines):
        cat = doctrine.issue_category.value
        if cat not in categories_seen:
            categories_seen[cat] = []
        categories_seen[cat].append(doctrine.topic)

    priority = 1
    for cat, topics in categories_seen.items():
        interaction_graph = []
        for topic_name in topics:
            d = get_doctrine_by_topic(topic_name)
            if d and d.interaction_edges:
                interaction_graph.extend(d.interaction_edges)

        issues.append(DecomposedIssue(
            issue_id=f"ISSUE-{priority:03d}",
            category=cat,
            description=f"Due diligence analysis for {cat.replace('_', ' ').lower()} "
                        f"covering {len(topics)} doctrine(s): {', '.join(topics)}",
            doctrines_applicable=topics,
            interaction_graph=list(set(interaction_graph)),
            resolution_priority=priority,
        ))
        priority += 1

    return issues


# ─────────────────────────────────────────────────────────────────────────────
# EPISTEMIC GUARDRAILS
# ─────────────────────────────────────────────────────────────────────────────

def apply_epistemic_guardrails(text: str) -> Tuple[str, List[str]]:
    """Apply epistemic guardrails to response text.

    Scans for banned phrases and removes or flags them.

    Args:
        text: Response text to check.

    Returns:
        Tuple of (cleaned text, list of violations found).
    """
    violations: List[str] = []
    cleaned = text
    for phrase in BANNED_PHRASES:
        if phrase.lower() in cleaned.lower():
            violations.append(f"Banned phrase detected: '{phrase}'")
            # Replace with authoritative language
            cleaned = cleaned.replace(phrase, "The analysis indicates")
            cleaned = cleaned.replace(phrase.capitalize(), "The analysis indicates")
            cleaned = cleaned.replace(phrase.lower(), "the analysis indicates")
    return cleaned, violations


def generate_disclosure_caveat(
    confidence: ConfidenceLevel,
    categories: List[str],
) -> str:
    """Generate an appropriate disclosure caveat based on confidence and categories.

    Args:
        confidence: The confidence level of the analysis.
        categories: Issue categories involved.

    Returns:
        Disclosure caveat string.
    """
    if confidence == ConfidenceLevel.DEFENSIBLE:
        return (
            "This analysis is based on established authority and standard industry practice. "
            "However, specific facts and applicable jurisdiction may affect the conclusions. "
            "This is not legal advice — consult qualified counsel for specific transactions."
        )
    elif confidence == ConfidenceLevel.AGGRESSIVE:
        return (
            "This analysis involves professional judgment and positions that, while supportable, "
            "may be challenged. The basis for each conclusion should be documented and disclosed "
            "to the decision-maker. This is not legal advice."
        )
    elif confidence == ConfidenceLevel.DISCLOSURE:
        return (
            "DISCLOSURE REQUIRED: This analysis involves significant uncertainty. Alternative "
            "interpretations exist and should be presented. The decision-maker must be informed "
            "of the risk that a different conclusion may be reached. This is not legal advice."
        )
    else:
        return (
            "HIGH RISK NOTICE: This analysis involves substantial uncertainty and risk of "
            "adverse outcome. All alternative interpretations and counter-arguments must be "
            "fully disclosed. Proceed only with informed consent of the decision-maker. "
            "This is not legal advice."
        )


# ─────────────────────────────────────────────────────────────────────────────
# DETERMINISM HASH (TIE-16)
# ─────────────────────────────────────────────────────────────────────────────

def compute_determinism_hash(
    query: str,
    mode: str,
    doctrines_matched: List[str],
    confidence: str,
) -> str:
    """Compute SHA-256 determinism hash for reproducibility.

    Args:
        query: The original query text.
        mode: Response mode used.
        doctrines_matched: List of matched doctrine topics.
        confidence: Confidence level string.

    Returns:
        SHA-256 hex digest (64 characters).
    """
    raw = json.dumps({
        "engine_id": ENGINE_ID,
        "engine_version": ENGINE_VERSION,
        "query": query,
        "mode": mode,
        "doctrines_matched": sorted(doctrines_matched),
        "confidence": confidence,
    }, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ─────────────────────────────────────────────────────────────────────────────
# DEEP ANALYSIS MODE (TIE-20)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class DeepAnalysisResult:
    """Result of deep analysis combining multiple sources."""
    synthesis: str
    reasoning_chain: List[str]
    authorities_consulted: List[str]
    counter_arguments_addressed: List[str]
    risk_assessment: str
    recommended_actions: List[str]
    confidence_assessment: ConfidenceAssessment
    fragility_score: FragilityScore


def perform_deep_analysis(
    query: str,
    matched_doctrines: List[DoctrineBlock],
    search_results: List[SearchResult],
    position: PositionZone = PositionZone.NEUTRAL,
) -> DeepAnalysisResult:
    """Perform deep multi-source analysis for complex queries.

    Combines doctrine cache hits, search results, and adversarial reasoning
    into a comprehensive analysis.

    Args:
        query: The original query text.
        matched_doctrines: Doctrine blocks matched from cache.
        search_results: Additional results from vector/text search.
        position: Analysis position zone.

    Returns:
        DeepAnalysisResult with full synthesis.
    """
    reasoning_chain: List[str] = []
    authorities: List[str] = []
    counter_args: List[str] = []
    actions: List[str] = []

    # Step 1: Aggregate doctrine reasoning
    reasoning_chain.append(f"Query analyzed: '{query[:200]}'")
    reasoning_chain.append(f"Position zone: {position.value}")
    reasoning_chain.append(f"Doctrine blocks matched: {len(matched_doctrines)}")
    reasoning_chain.append(f"Search results supplementing: {len(search_results)}")

    for i, d in enumerate(matched_doctrines):
        reasoning_chain.append(
            f"Doctrine {i+1} [{d.topic}]: {d.issue_category.value} | "
            f"Confidence: {d.confidence.value}"
        )
        authorities.extend(d.primary_authority)
        counter_args.extend(d.counter_arguments)
        if d.resolution_strategy:
            actions.append(f"[{d.topic}] {d.resolution_strategy}")

    # Step 2: Search result integration
    for sr in search_results:
        reasoning_chain.append(
            f"Search hit: {sr.title} (score={sr.score:.3f}, domain={sr.domain})"
        )

    # Step 3: Synthesize
    synthesis_parts = []
    for d in matched_doctrines:
        if position == PositionZone.BUYER:
            synthesis_parts.append(
                f"{d.conclusion_template} From the buyer's perspective, "
                f"the key risk factors are: {'; '.join(d.key_factors[:3])}. "
                f"The burden of proof rests with: {d.burden_holder}."
            )
        elif position == PositionZone.SELLER:
            synthesis_parts.append(
                f"The seller's position: {d.adversary_position} "
                f"Supporting arguments: {'; '.join(d.counter_arguments[:2])}."
            )
        else:
            synthesis_parts.append(
                f"{d.conclusion_template} Key factors: {'; '.join(d.key_factors[:3])}."
            )

    synthesis = " ".join(synthesis_parts) if synthesis_parts else "Insufficient data for synthesis."

    # Step 4: Risk assessment
    if matched_doctrines:
        avg_counter_args = sum(len(d.counter_arguments) for d in matched_doctrines) / len(matched_doctrines)
        if avg_counter_args > 6:
            risk = "HIGH — Multiple counter-arguments indicate significant adversarial exposure."
        elif avg_counter_args > 4:
            risk = "MODERATE — Counter-arguments exist but are manageable with proper documentation."
        else:
            risk = "LOW — Limited counter-argument exposure; position is well-supported."
    else:
        risk = "INDETERMINATE — Insufficient doctrine coverage to assess risk."

    # Step 5: Confidence and fragility
    if matched_doctrines:
        best_doctrine = matched_doctrines[0]
        confidence = assess_confidence(best_doctrine)
        fragility = compute_fact_fragility(best_doctrine)
    else:
        confidence = ConfidenceAssessment(
            level=ConfidenceLevel.HIGH_RISK,
            score=0.2,
            authority_score=0.0,
            doctrine_coverage=0.0,
            fragility_factor=0.5,
            reasoning="No doctrine matched — confidence is low.",
        )
        fragility = FragilityScore(
            verifiability=0.3,
            recharacterization_risk=0.7,
            testimony_dependence=0.5,
            document_dependence=0.5,
            overall_fragility=0.7,
            assessment="High fragility due to absence of doctrine support.",
        )

    return DeepAnalysisResult(
        synthesis=synthesis,
        reasoning_chain=reasoning_chain,
        authorities_consulted=list(set(authorities)),
        counter_arguments_addressed=list(set(counter_args)),
        risk_assessment=risk,
        recommended_actions=actions,
        confidence_assessment=confidence,
        fragility_score=fragility,
    )


# ─────────────────────────────────────────────────────────────────────────────
# THE ENGINE CORE
# ─────────────────────────────────────────────────────────────────────────────

class DueDiligenceEngine:
    """The LM08 Due Diligence Intelligence Engine.

    Implements all 20 TIE components for oil & gas acquisition due diligence.
    """

    def __init__(self) -> None:
        self._start_time = time.time()
        self._query_count = 0

        # TIE-6: Semantic Normalization
        self._normalizer = DueDiligenceSemanticNormalizer()

        # TIE-7: Vector Search
        self._search_engine = DueDiligenceSearchEngine()

        # TIE-8, TIE-9, TIE-10, TIE-11, TIE-15: Telemetry suite
        self._telemetry = DueDiligenceTelemetry(LOG_DIR)

        # TIE-3: Doctrine Cache — index for search fallback
        self._index_doctrines()

        logger.info(
            "DueDiligenceEngine initialized | doctrines={} | semantic_terms={} | port={}",
            len(DOCTRINE_CACHE),
            self._normalizer.get_registry_stats()["total_canonical_terms"],
            ENGINE_PORT,
        )

    def _index_doctrines(self) -> None:
        """Index all doctrine blocks into the search engine and register with coverage map."""
        for topic, block in DOCTRINE_CACHE.items():
            self._search_engine.index_doctrine(
                doc_id=topic,
                title=topic.replace("_", " ").title(),
                content=f"{block.conclusion_template} {block.reasoning_framework} "
                        f"{' '.join(block.keywords)} {' '.join(block.key_factors)}",
                domain=block.issue_category.value,
            )
            self._telemetry.coverage.register_doctrine(
                doctrine_id=topic,
                topic=topic,
                domain=block.issue_category.value,
            )
            # Set baseline drift hash
            raw = f"{block.topic}|{block.conclusion_template}|{block.reasoning_framework}"
            content_hash = hashlib.sha256(raw.encode()).hexdigest()
            self._telemetry.drift.set_baseline(topic, content_hash)

    # ─── THREE-LAYER RESPONSE (TIE-1) ───────────────────────────────────

    def _layer_1_doctrine_cache(
        self,
        query: str,
        normalized_terms: List[NormalizationResult],
        category_filter: Optional[List[str]] = None,
        max_results: int = 5,
    ) -> Tuple[List[DoctrineBlock], float]:
        """Layer 1: Doctrine Cache lookup (0-200ms target).

        Args:
            query: Original query text.
            normalized_terms: Semantically normalized terms.
            category_filter: Optional category filter.
            max_results: Maximum results to return.

        Returns:
            Tuple of (matched doctrines, latency_ms).
        """
        start = time.perf_counter()
        matched: List[DoctrineBlock] = []
        seen_topics: set = set()

        # Direct keyword match
        query_words = set(query.lower().split())
        for topic, block in DOCTRINE_CACHE.items():
            if category_filter and block.issue_category.value not in category_filter:
                continue
            keyword_overlap = len(query_words & set(kw.lower() for kw in block.keywords))
            if keyword_overlap >= 2 and topic not in seen_topics:
                matched.append(block)
                seen_topics.add(topic)

        # Normalized term match
        for norm in normalized_terms:
            if norm.confidence >= 0.5:
                canonical = norm.canonical
                if canonical in DOCTRINE_CACHE and canonical not in seen_topics:
                    block = DOCTRINE_CACHE[canonical]
                    if not category_filter or block.issue_category.value in category_filter:
                        matched.append(block)
                        seen_topics.add(canonical)

        # Search by keywords from normalized terms
        search_keywords = [n.canonical for n in normalized_terms if n.confidence >= 0.5]
        if search_keywords:
            keyword_results = search_doctrines(search_keywords)
            for block in keyword_results:
                if block.topic not in seen_topics:
                    if not category_filter or block.issue_category.value in category_filter:
                        matched.append(block)
                        seen_topics.add(block.topic)

        latency = (time.perf_counter() - start) * 1000
        logger.debug("Layer 1 doctrine cache | matches={} | latency={:.2f}ms", len(matched), latency)
        return matched, latency

    def _layer_2_semantic_retrieval(
        self,
        query: str,
        category_filter: Optional[str] = None,
        max_results: int = 5,
    ) -> Tuple[List[SearchResult], float]:
        """Layer 2: Semantic retrieval via search index.

        Args:
            query: Original query text.
            category_filter: Optional domain filter.
            max_results: Maximum results.

        Returns:
            Tuple of (search results, latency_ms).
        """
        start = time.perf_counter()
        results = self._search_engine.search(
            query_text=query,
            domain=category_filter,
            max_results=max_results,
            min_score=0.2,
        )
        latency = (time.perf_counter() - start) * 1000
        logger.debug("Layer 2 semantic retrieval | results={} | latency={:.2f}ms", len(results), latency)
        return results, latency

    def _layer_3_deep_analysis(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        search_results: List[SearchResult],
        position: PositionZone,
    ) -> Tuple[DeepAnalysisResult, float]:
        """Layer 3: Deep analysis combining all sources.

        Args:
            query: Original query text.
            doctrines: Doctrine blocks from layer 1.
            search_results: Results from layer 2.
            position: Position zone for analysis.

        Returns:
            Tuple of (deep analysis result, latency_ms).
        """
        start = time.perf_counter()
        result = perform_deep_analysis(query, doctrines, search_results, position)
        latency = (time.perf_counter() - start) * 1000
        logger.debug("Layer 3 deep analysis | latency={:.2f}ms", latency)
        return result, latency

    # ─── MAIN QUERY PROCESSOR ────────────────────────────────────────────

    def process_query(self, request: QueryRequest) -> QueryResponse:
        """Process a due diligence query through the three-layer pipeline.

        Args:
            request: The query request with parameters.

        Returns:
            Complete QueryResponse with all analysis layers.
        """
        self._query_count += 1
        trace_id = str(uuid.uuid4())
        trace = QueryTrace(trace_id=trace_id, query_text=request.query)
        total_start = time.perf_counter()

        # Parse position zone
        position = PositionZone.NEUTRAL
        if request.position_zone:
            try:
                position = PositionZone(request.position_zone.upper())
            except ValueError:
                position = PositionZone.NEUTRAL

        # ── Phase 1: Semantic Normalization (TIE-6) ──
        norm_start = time.perf_counter()
        query_terms = request.query.split()
        bigrams = [f"{query_terms[i]} {query_terms[i+1]}" for i in range(len(query_terms) - 1)]
        trigrams = [f"{query_terms[i]} {query_terms[i+1]} {query_terms[i+2]}"
                    for i in range(len(query_terms) - 2)]
        all_terms = trigrams + bigrams + query_terms
        normalized = self._normalizer.normalize_batch(all_terms)
        norm_latency = (time.perf_counter() - norm_start) * 1000
        trace.add_phase(QueryPhase.NORMALIZED, norm_latency, {"terms_normalized": len(normalized)})

        # ── Phase 2: Layer 1 — Doctrine Cache (TIE-3) ──
        trace.add_phase(QueryPhase.DOCTRINE_LOOKUP, 0)
        doctrines, l1_latency = self._layer_1_doctrine_cache(
            request.query,
            normalized,
            category_filter=request.issue_categories,
            max_results=request.max_doctrines,
        )
        trace.add_phase(QueryPhase.DOCTRINE_LOOKUP, l1_latency, {"hits": len(doctrines)})
        trace.doctrine_hits = [d.topic for d in doctrines]

        layer_1 = AnalysisLayer(
            layer="doctrine_cache",
            latency_ms=round(l1_latency, 2),
            results_count=len(doctrines),
            doctrines=[self._doctrine_to_response(d, request) for d in doctrines],
        )

        # ── Phase 3: Layer 2 — Semantic Retrieval (TIE-7) ──
        category_domain = request.issue_categories[0] if request.issue_categories else None
        search_results, l2_latency = self._layer_2_semantic_retrieval(
            request.query,
            category_filter=category_domain,
            max_results=request.max_doctrines,
        )
        trace.add_phase(QueryPhase.VECTOR_SEARCH, l2_latency, {"results": len(search_results)})

        # Convert search results to doctrine responses where possible
        l2_doctrines: List[DoctrineResponse] = []
        for sr in search_results:
            doctrine = get_doctrine_by_topic(sr.doc_id)
            if doctrine and doctrine.topic not in trace.doctrine_hits:
                l2_doctrines.append(self._doctrine_to_response(doctrine, request))
                trace.doctrine_hits.append(doctrine.topic)

        layer_2 = AnalysisLayer(
            layer="semantic_retrieval",
            latency_ms=round(l2_latency, 2),
            results_count=len(l2_doctrines),
            doctrines=l2_doctrines,
        )

        # ── Phase 4: Layer 3 — Deep Analysis (TIE-20) ──
        layers = [layer_1, layer_2]
        fragility_score: Optional[FragilityScore] = None
        deep_result: Optional[DeepAnalysisResult] = None

        if request.deep_analysis or request.mode == ResponseMode.MEMO:
            deep_result, l3_latency = self._layer_3_deep_analysis(
                request.query, doctrines, search_results, position,
            )
            trace.add_phase(QueryPhase.DEEP_ANALYSIS, l3_latency)

            layer_3 = AnalysisLayer(
                layer="deep_analysis",
                latency_ms=round(l3_latency, 2),
                results_count=1,
                doctrines=[],
            )
            layers.append(layer_3)
            fragility_score = deep_result.fragility_score

        elif doctrines:
            fragility_score = compute_fact_fragility(doctrines[0])

        # ── Phase 5: Confidence Assessment (TIE-5) ──
        if doctrines:
            confidence = assess_confidence(doctrines[0])
            confidence_level = confidence.level.value
        else:
            confidence_level = ConfidenceLevel.HIGH_RISK.value

        # ── Phase 6: Multi-Doctrine Decomposition (TIE-19) ──
        decomposed = decompose_query(request.query, doctrines)

        # ── Phase 7: Epistemic Guardrails ──
        categories_triggered = list(set(d.issue_category.value for d in doctrines))
        disclosure = generate_disclosure_caveat(
            ConfidenceLevel(confidence_level),
            categories_triggered,
        )

        # ── Phase 8: Determinism Hash (TIE-16) ──
        det_hash = compute_determinism_hash(
            request.query,
            request.mode.value,
            [d.topic for d in doctrines],
            confidence_level,
        )

        trace.response_mode = request.mode.value
        trace.confidence_level = confidence_level
        trace.issue_categories = categories_triggered

        total_latency = (time.perf_counter() - total_start) * 1000
        trace.add_phase(QueryPhase.COMPLETED, 0)

        # Record to telemetry
        self._telemetry.record_query(trace)

        # Record coverage gaps
        if not doctrines:
            self._telemetry.coverage.record_gap(
                request.query,
                category_domain or "unknown",
            )

        response = QueryResponse(
            query=request.query,
            mode=request.mode.value,
            layers=layers,
            total_latency_ms=round(total_latency, 2),
            confidence_level=confidence_level,
            position_zone=position.value,
            decomposed_issues=decomposed,
            fragility_score=fragility_score,
            disclosure_caveat=disclosure,
            determinism_hash=det_hash,
            trace_id=trace_id,
            issue_categories_triggered=categories_triggered,
        )

        logger.info(
            "Query processed | trace={} | mode={} | doctrines={} | confidence={} | latency={:.1f}ms",
            trace_id[:8], request.mode.value, len(doctrines), confidence_level, total_latency,
        )
        return response

    def _doctrine_to_response(
        self,
        doctrine: DoctrineBlock,
        request: QueryRequest,
    ) -> DoctrineResponse:
        """Convert a DoctrineBlock to a DoctrineResponse based on request parameters.

        Args:
            doctrine: The doctrine block to convert.
            request: The query request (controls what fields to include).

        Returns:
            DoctrineResponse model.
        """
        resp = DoctrineResponse(
            topic=doctrine.topic,
            conclusion=doctrine.conclusion_template,
            confidence=doctrine.confidence.value,
            issue_category=doctrine.issue_category.value,
            position_zone=doctrine.position_zone.value,
            key_factors=doctrine.key_factors,
            interaction_edges=doctrine.interaction_edges,
        )

        if request.include_authorities:
            resp.authorities = doctrine.primary_authority

        if request.include_counter_arguments:
            resp.counter_arguments = doctrine.counter_arguments

        if request.mode in (ResponseMode.DEFENSE, ResponseMode.MEMO):
            resp.resolution_strategy = doctrine.resolution_strategy

        return resp

    # ─── ZONED ANALYSIS API (TIE-13) ────────────────────────────────────

    def analyze_zoned(
        self,
        query: str,
        zone: str = "PLANNING",
        position: str = "NEUTRAL",
        categories: Optional[List[str]] = None,
    ) -> ZonedResult:
        """Perform zoned analysis for a specific zone and position.

        Args:
            query: The query text.
            zone: Analysis zone (PLANNING, REPORTING, AUDIT).
            position: Position zone (BUYER, SELLER, NEUTRAL).
            categories: Optional category filters.

        Returns:
            ZonedResult scoped to the specified zone.
        """
        # Get doctrines
        query_terms = query.split()
        normalized = self._normalizer.normalize_batch(query_terms)
        doctrines, _ = self._layer_1_doctrine_cache(query, normalized, category_filter=categories)

        try:
            analysis_zone = AnalysisZone(zone.upper())
        except ValueError:
            analysis_zone = AnalysisZone.PLANNING

        try:
            position_zone = PositionZone(position.upper())
        except ValueError:
            position_zone = PositionZone.NEUTRAL

        return apply_zoned_analysis(query, doctrines, analysis_zone, position_zone)

    # ─── HEALTH ENDPOINT (TIE-12) ───────────────────────────────────────

    def get_health(self) -> HealthResponse:
        """Return comprehensive engine health status.

        Returns:
            HealthResponse with all status indicators.
        """
        uptime = time.time() - self._start_time
        metrics = self._telemetry.metrics.get_metrics()
        search_metrics = self._search_engine.get_metrics()
        semantic_stats = self._normalizer.get_registry_stats()

        return HealthResponse(
            status="healthy",
            uptime_seconds=round(uptime, 1),
            doctrine_count=len(DOCTRINE_CACHE),
            issue_categories=len(IssueCategory),
            semantic_terms=semantic_stats["total_canonical_terms"],
            search_index_docs=search_metrics["index_stats"]["total_documents"],
            telemetry_summary={
                "total_queries": metrics["total_queries"],
                "error_rate": metrics["error_rate"],
                "avg_latency_ms": metrics["latency"]["average_ms"],
                "doctrine_hit_rate": metrics["doctrine"]["hit_rate"],
                "coverage": self._telemetry.coverage.get_coverage_report()["coverage_pct"],
            },
        )

    # ─── TELEMETRY REPORT ────────────────────────────────────────────────

    def get_telemetry_report(self) -> Dict[str, Any]:
        """Return full telemetry report.

        Returns:
            Complete telemetry data from all subsystems.
        """
        return self._telemetry.get_full_report()

    # ─── DOCTRINE INVENTORY ──────────────────────────────────────────────

    def get_doctrine_inventory(self) -> Dict[str, Any]:
        """Return inventory of all doctrine blocks.

        Returns:
            Dictionary with doctrine statistics and listing.
        """
        inventory: Dict[str, List[Dict[str, Any]]] = {}
        for topic, block in DOCTRINE_CACHE.items():
            cat = block.issue_category.value
            if cat not in inventory:
                inventory[cat] = []
            inventory[cat].append({
                "topic": topic,
                "keywords": block.keywords,
                "confidence": block.confidence.value,
                "position_zone": block.position_zone.value,
                "authority_count": len(block.primary_authority),
                "counter_argument_count": len(block.counter_arguments),
                "key_factor_count": len(block.key_factors),
                "interaction_edges": block.interaction_edges,
            })

        return {
            "engine_id": ENGINE_ID,
            "total_doctrines": len(DOCTRINE_CACHE),
            "total_categories": len(inventory),
            "categories": inventory,
        }

    # ─── SEARCH API ──────────────────────────────────────────────────────

    def search(
        self,
        query: str,
        domain: Optional[str] = None,
        max_results: int = 10,
    ) -> List[SearchResult]:
        """Direct search API for the engine.

        Args:
            query: Search query text.
            domain: Optional domain filter.
            max_results: Maximum results.

        Returns:
            List of SearchResult objects.
        """
        return self._search_engine.search(query, domain=domain, max_results=max_results)

    # ─── SEMANTIC NORMALIZATION API ──────────────────────────────────────

    def normalize_term(self, term: str) -> NormalizationResult:
        """Normalize a single term.

        Args:
            term: The term to normalize.

        Returns:
            NormalizationResult with canonical form.
        """
        return self._normalizer.normalize(term)

    def normalize_batch(self, terms: List[str]) -> List[NormalizationResult]:
        """Normalize a batch of terms.

        Args:
            terms: List of terms to normalize.

        Returns:
            List of NormalizationResult objects.
        """
        return self._normalizer.normalize_batch(terms)


# ─────────────────────────────────────────────────────────────────────────────
# FASTAPI SERVER (TIE-17)
# ─────────────────────────────────────────────────────────────────────────────

try:
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    import uvicorn

    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    logger.warning("FastAPI not available — HTTP server disabled")


def create_app() -> Any:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI app instance.
    """
    if not FASTAPI_AVAILABLE:
        raise RuntimeError("FastAPI is not installed. Run: pip install fastapi uvicorn")

    engine: Optional[DueDiligenceEngine] = None

    @asynccontextmanager
    async def lifespan(app: Any) -> Any:
        nonlocal engine
        logger.info("LM08 Due Diligence Engine starting on port {}", ENGINE_PORT)
        engine = DueDiligenceEngine()
        app.state.engine = engine
        yield
        logger.info("LM08 Due Diligence Engine shutting down")
        if _CLOUD_AVAILABLE:
            try:
                from cloud_retriever import get_cloud_retriever
                await get_cloud_retriever().close()
                logger.info("Cloud retriever closed")
            except Exception as e:
                logger.warning(f"Cloud retriever cleanup failed: {e}")

    app = FastAPI(
        title="LM08 Due Diligence Engine",
        description=(
            "TIE Gold Standard engine for oil & gas acquisition due diligence intelligence. "
            "Covers title examination, environmental compliance, regulatory audit, production analysis, "
            "reserve estimation, lease verification, lien search, litigation review, PSA analysis, "
            "and 19 issue categories."
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

    @app.get("/health")
    async def health() -> Dict[str, Any]:
        """TIE-12: Health endpoint returning comprehensive JSON status."""
        if engine is None:
            raise HTTPException(status_code=503, detail="Engine not initialized")
        h = engine.get_health()
        return {
            "engine_id": h.engine_id,
            "engine_name": h.engine_name,
            "version": h.version,
            "status": h.status,
            "uptime_seconds": h.uptime_seconds,
            "doctrine_count": h.doctrine_count,
            "issue_categories": h.issue_categories,
            "semantic_terms": h.semantic_terms,
            "search_index_docs": h.search_index_docs,
            "telemetry_summary": h.telemetry_summary,
            "timestamp": h.timestamp,
        }

    @app.post("/query")
    async def query_endpoint(request: QueryRequest) -> Dict[str, Any]:
        """Process a due diligence query through the three-layer pipeline."""
        if engine is None:
            raise HTTPException(status_code=503, detail="Engine not initialized")
        try:
            # ─────────────────────────────────────────────────────────────────────
            # CLOUD KNOWLEDGE RETRIEVAL
            # ─────────────────────────────────────────────────────────────────────
            cloud_data = {}
            cloud_citations = []
            if _CLOUD_AVAILABLE:
                try:
                    q = request.query or request.prompt or ""
                    cloud = await retrieve_cloud_knowledge(q, category="due_diligence")
                    cloud_data = {
                        "records": len(cloud.clauses) + len(cloud.graph_nodes) + len(cloud.crystals),
                        "merged_context": cloud.merged_text(3000),
                        "sources_succeeded": cloud.sources_succeeded,
                        "retrieval_time_ms": cloud.retrieval_time_ms,
                    }
                    cloud_citations = cloud.citation_list()
                    logger.info(f"Cloud retrieval: {cloud_data['records']} records in {cloud_data['retrieval_time_ms']}ms")
                except Exception as e:
                    logger.warning(f"Cloud retrieval failed: {e}")

            # ─────────────────────────────────────────────────────────────────────
            # LOCAL ENGINE PROCESSING
            # ─────────────────────────────────────────────────────────────────────
            response = engine.process_query(request)
            result = {
                "engine_id": response.engine_id,
                "engine_version": response.engine_version,
                "query": response.query,
                "mode": response.mode,
                "timestamp": response.timestamp,
                "total_latency_ms": response.total_latency_ms,
                "confidence_level": response.confidence_level,
                "position_zone": response.position_zone,
                "determinism_hash": response.determinism_hash,
                "trace_id": response.trace_id,
                "disclosure_caveat": response.disclosure_caveat,
                "issue_categories_triggered": response.issue_categories_triggered,
                "cloud_knowledge": cloud_data,
                "cloud_citations": cloud_citations,
                "layers": [],
                "decomposed_issues": [],
            }

            for layer in response.layers:
                layer_dict = {
                    "layer": layer.layer,
                    "latency_ms": layer.latency_ms,
                    "results_count": layer.results_count,
                    "doctrines": [],
                }
                for d in layer.doctrines:
                    layer_dict["doctrines"].append({
                        "topic": d.topic,
                        "conclusion": d.conclusion,
                        "confidence": d.confidence,
                        "issue_category": d.issue_category,
                        "position_zone": d.position_zone,
                        "key_factors": d.key_factors,
                        "authorities": d.authorities,
                        "counter_arguments": d.counter_arguments,
                        "resolution_strategy": d.resolution_strategy,
                        "interaction_edges": d.interaction_edges,
                    })
                result["layers"].append(layer_dict)

            for issue in response.decomposed_issues:
                result["decomposed_issues"].append({
                    "issue_id": issue.issue_id,
                    "category": issue.category,
                    "description": issue.description,
                    "doctrines_applicable": issue.doctrines_applicable,
                    "interaction_graph": issue.interaction_graph,
                    "resolution_priority": issue.resolution_priority,
                })

            if response.fragility_score:
                fs = response.fragility_score
                result["fragility_score"] = {
                    "verifiability": fs.verifiability,
                    "recharacterization_risk": fs.recharacterization_risk,
                    "testimony_dependence": fs.testimony_dependence,
                    "document_dependence": fs.document_dependence,
                    "overall_fragility": fs.overall_fragility,
                    "assessment": fs.assessment,
                }

            return result
        except Exception as e:
            logger.error("Query processing error: {}", e)
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/query/zoned")
    async def zoned_query(
        query: str,
        zone: str = "PLANNING",
        position: str = "NEUTRAL",
    ) -> Dict[str, Any]:
        """TIE-13: Zoned analysis endpoint."""
        if engine is None:
            raise HTTPException(status_code=503, detail="Engine not initialized")
        result = engine.analyze_zoned(query, zone, position)
        return {
            "zone": result.zone.value,
            "position": result.position.value,
            "content": result.content,
            "caveats": result.caveats,
            "applicable_doctrines": result.applicable_doctrines,
        }

    @app.get("/doctrines")
    async def list_doctrines() -> Dict[str, Any]:
        """Return doctrine inventory."""
        if engine is None:
            raise HTTPException(status_code=503, detail="Engine not initialized")
        return engine.get_doctrine_inventory()

    @app.get("/doctrines/{topic}")
    async def get_doctrine(topic: str) -> Dict[str, Any]:
        """Return a specific doctrine block by topic."""
        doctrine = get_doctrine_by_topic(topic)
        if doctrine is None:
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
            "confidence": doctrine.confidence.value,
            "confidence_stratification": doctrine.confidence_stratification,
            "controlling_precedent": doctrine.controlling_precedent,
            "issue_category": doctrine.issue_category.value,
            "position_zone": doctrine.position_zone.value,
            "interaction_edges": doctrine.interaction_edges,
        }

    @app.get("/doctrines/category/{category}")
    async def get_doctrines_by_cat(category: str) -> Dict[str, Any]:
        """Return doctrines filtered by issue category."""
        try:
            cat = IssueCategory(category)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category: {category}. Valid: {[c.value for c in IssueCategory]}",
            )
        doctrines = get_doctrines_by_category(cat)
        return {
            "category": category,
            "count": len(doctrines),
            "doctrines": [
                {
                    "topic": d.topic,
                    "confidence": d.confidence.value,
                    "keywords": d.keywords,
                    "conclusion_template": d.conclusion_template[:200],
                }
                for d in doctrines
            ],
        }

    @app.get("/search")
    async def search_endpoint(
        q: str = Query(..., description="Search query"),
        domain: Optional[str] = Query(default=None, description="Domain filter"),
        max_results: int = Query(default=10, ge=1, le=50),
    ) -> Dict[str, Any]:
        """TIE-7: Search endpoint for doctrine retrieval."""
        if engine is None:
            raise HTTPException(status_code=503, detail="Engine not initialized")
        results = engine.search(q, domain=domain, max_results=max_results)
        return {
            "query": q,
            "domain": domain,
            "results_count": len(results),
            "results": [
                {
                    "doc_id": r.doc_id,
                    "title": r.title,
                    "score": r.score,
                    "domain": r.domain,
                    "keywords_matched": r.keywords_matched,
                    "content_preview": r.content[:300],
                }
                for r in results
            ],
        }

    @app.get("/normalize")
    async def normalize_endpoint(
        term: str = Query(..., description="Term to normalize"),
    ) -> Dict[str, Any]:
        """TIE-6: Semantic normalization endpoint."""
        if engine is None:
            raise HTTPException(status_code=503, detail="Engine not initialized")
        result = engine.normalize_term(term)
        return {
            "original": result.original,
            "canonical": result.canonical,
            "domain": result.domain.value,
            "confidence": result.confidence,
            "aliases_matched": result.aliases_matched,
            "context_hints": result.context_hints,
            "determinism_hash": result.determinism_hash,
        }

    @app.post("/normalize/batch")
    async def normalize_batch_endpoint(terms: List[str]) -> Dict[str, Any]:
        """Batch semantic normalization."""
        if engine is None:
            raise HTTPException(status_code=503, detail="Engine not initialized")
        results = engine.normalize_batch(terms)
        return {
            "count": len(results),
            "results": [
                {
                    "original": r.original,
                    "canonical": r.canonical,
                    "domain": r.domain.value,
                    "confidence": r.confidence,
                }
                for r in results
            ],
        }

    @app.get("/telemetry")
    async def telemetry_endpoint() -> Dict[str, Any]:
        """TIE-8: Full telemetry report."""
        if engine is None:
            raise HTTPException(status_code=503, detail="Engine not initialized")
        return engine.get_telemetry_report()

    @app.get("/telemetry/metrics")
    async def metrics_endpoint() -> Dict[str, Any]:
        """TIE-11: Metrics collector output."""
        if engine is None:
            raise HTTPException(status_code=503, detail="Engine not initialized")
        return engine._telemetry.metrics.get_metrics()

    @app.get("/telemetry/drift")
    async def drift_endpoint() -> Dict[str, Any]:
        """TIE-9: Drift watcher report."""
        if engine is None:
            raise HTTPException(status_code=503, detail="Engine not initialized")
        return engine._telemetry.drift.get_drift_report()

    @app.get("/telemetry/coverage")
    async def coverage_endpoint() -> Dict[str, Any]:
        """TIE-10: Coverage map report."""
        if engine is None:
            raise HTTPException(status_code=503, detail="Engine not initialized")
        return engine._telemetry.coverage.get_coverage_report()

    @app.get("/categories")
    async def list_categories() -> Dict[str, Any]:
        """Return all issue categories."""
        return {
            "categories": [
                {"value": c.value, "name": c.name}
                for c in IssueCategory
            ],
            "count": len(IssueCategory),
        }

    @app.get("/authority-hierarchy")
    async def authority_hierarchy() -> Dict[str, Any]:
        """TIE-4: Authority hierarchy definition."""
        return {
            "hierarchy": [
                {
                    "level": a.level,
                    "name": a.name,
                    "weight": a.weight,
                    "description": a.description,
                }
                for a in AUTHORITY_HIERARCHY
            ],
        }

    @app.get("/confidence-levels")
    async def confidence_levels() -> Dict[str, Any]:
        """TIE-5: Confidence level definitions."""
        return {
            "levels": [
                {"value": c.value, "name": c.name}
                for c in ConfidenceLevel
            ],
        }

    @app.get("/")
    async def root() -> Dict[str, Any]:
        """Engine identity and capabilities."""
        return {
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "port": ENGINE_PORT,
            "tie_standard": "TIE-20 Gold",
            "domain": "oil_gas_acquisition_due_diligence",
            "endpoints": [
                "/health", "/query", "/query/zoned", "/doctrines",
                "/doctrines/{topic}", "/doctrines/category/{category}",
                "/search", "/normalize", "/normalize/batch",
                "/telemetry", "/telemetry/metrics", "/telemetry/drift",
                "/telemetry/coverage", "/categories", "/authority-hierarchy",
                "/confidence-levels",
            ],
            "issue_categories": len(IssueCategory),
            "doctrine_count": len(DOCTRINE_CACHE),
        }

    return app


# ─────────────────────────────────────────────────────────────────────────────
# ENTRYPOINT
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# DUE DILIGENCE CHECKLIST GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

class ChecklistPriority(str, Enum):
    """Priority levels for checklist items."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class ChecklistItem:
    """A single item on the due diligence checklist."""
    item_id: str
    category: str
    description: str
    priority: ChecklistPriority
    responsible_party: str
    data_sources: List[str]
    deadline_offset_days: int
    dependencies: List[str]
    completion_criteria: str
    status: str = "PENDING"
    notes: str = ""


@dataclass
class DueDiligenceChecklist:
    """Complete due diligence checklist for an acquisition."""
    transaction_name: str
    effective_date: str
    closing_target_date: str
    items: List[ChecklistItem]
    generated_at: str = ""
    total_items: int = 0
    categories: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.generated_at = datetime.now(timezone.utc).isoformat()
        self.total_items = len(self.items)
        for item in self.items:
            self.categories[item.category] = self.categories.get(item.category, 0) + 1


def generate_due_diligence_checklist(
    transaction_name: str = "Oil & Gas Acquisition",
    effective_date: str = "",
    closing_target: str = "",
) -> DueDiligenceChecklist:
    """Generate a comprehensive due diligence checklist covering all 19 issue categories.

    Args:
        transaction_name: Name of the transaction.
        effective_date: Transaction effective date.
        closing_target: Target closing date.

    Returns:
        Complete DueDiligenceChecklist with prioritized items.
    """
    items: List[ChecklistItem] = []
    item_num = 1

    # TITLE DUE DILIGENCE
    title_items = [
        ("Obtain all title opinions, abstracts, and title files from seller", ChecklistPriority.CRITICAL,
         "Title attorney", ["Data room", "County records"], 5, [],
         "All existing title opinions and abstracts received and catalogued"),
        ("Engage title examination firm and establish examination scope", ChecklistPriority.CRITICAL,
         "Buyer's counsel", ["PSA title standard"], 7, [],
         "Title examination firm engaged with agreed scope of work and timeline"),
        ("Conduct independent chain of title examination for all properties", ChecklistPriority.CRITICAL,
         "Title attorney", ["County records", "State land office"], 30, ["DD-001", "DD-002"],
         "Chain of title traced from sovereign to current owner for all properties"),
        ("Identify and document all title defects per PSA standard", ChecklistPriority.CRITICAL,
         "Title attorney", ["Title opinions", "County records"], 35, ["DD-003"],
         "All title defects documented in standard defect notice format"),
        ("Verify mineral severance history and outstanding mineral interests", ChecklistPriority.HIGH,
         "Title attorney", ["Deed records", "Mineral ownership records"], 25, ["DD-003"],
         "All mineral severances identified and quantified"),
        ("Verify NRI and WI for each well against division orders and title opinions", ChecklistPriority.CRITICAL,
         "Landman", ["Division orders", "Revenue statements", "Title opinions"], 30, ["DD-003"],
         "NRI/WI reconciled for all wells within tolerance threshold"),
        ("Review all pooling designations and unit agreements", ChecklistPriority.HIGH,
         "Landman", ["County records", "RRC records"], 20, ["DD-003"],
         "All pooling and unitization verified for validity and compliance"),
        ("Obtain and review all division orders currently on file", ChecklistPriority.HIGH,
         "Landman", ["Operators", "Purchasers"], 15, [],
         "Current division orders obtained for all properties"),
    ]

    for desc, priority, responsible, sources, deadline, deps, criteria in title_items:
        items.append(ChecklistItem(
            item_id=f"DD-{item_num:03d}",
            category="TITLE_DUE_DILIGENCE",
            description=desc,
            priority=priority,
            responsible_party=responsible,
            data_sources=sources,
            deadline_offset_days=deadline,
            dependencies=deps,
            completion_criteria=criteria,
        ))
        item_num += 1

    # ENVIRONMENTAL COMPLIANCE
    env_items = [
        ("Commission Phase I ESA per ASTM E1527-21 with O&G scope expansion", ChecklistPriority.CRITICAL,
         "Environmental consultant", ["State records", "Site reconnaissance"], 30, [],
         "Phase I ESA report delivered with findings classified as REC/HREC/CREC"),
        ("Commission Phase II ESA for any identified RECs", ChecklistPriority.HIGH,
         "Environmental consultant", ["Phase I findings"], 60, ["DD-009"],
         "Phase II results quantifying contamination extent and remediation cost"),
        ("Evaluate P&A liability for all wells (active, inactive, shut-in, TA)", ChecklistPriority.CRITICAL,
         "Petroleum engineer", ["Well list", "Regulatory records", "Recent P&A costs"], 25, [],
         "P&A cost estimated per well with aggregate liability quantified"),
        ("Assess NORM exposure and disposal compliance", ChecklistPriority.HIGH,
         "Environmental consultant", ["State regulations", "Operator records"], 30, [],
         "NORM assessment complete with disposal compliance verified"),
        ("Review produced water disposal compliance and SWD capacity", ChecklistPriority.HIGH,
         "Environmental engineer", ["UIC permits", "Injection records"], 25, [],
         "Disposal capacity verified adequate; seismicity risk assessed"),
        ("Verify pit closure compliance and surface remediation status", ChecklistPriority.MEDIUM,
         "Environmental consultant", ["State records", "Site inspection"], 30, [],
         "All pit closures verified compliant; pending remediation identified"),
    ]

    for desc, priority, responsible, sources, deadline, deps, criteria in env_items:
        items.append(ChecklistItem(
            item_id=f"DD-{item_num:03d}",
            category="ENVIRONMENTAL_COMPLIANCE",
            description=desc,
            priority=priority,
            responsible_party=responsible,
            data_sources=sources,
            deadline_offset_days=deadline,
            dependencies=deps,
            completion_criteria=criteria,
        ))
        item_num += 1

    # REGULATORY AUDIT
    reg_items = [
        ("Search state oil and gas commission for violations and enforcement actions", ChecklistPriority.CRITICAL,
         "Regulatory specialist", ["State database", "RRC/OCC records"], 15, [],
         "All violations identified and quantified; pending enforcement documented"),
        ("Verify drilling permit and completion report compliance for all wells", ChecklistPriority.HIGH,
         "Regulatory specialist", ["State well files"], 20, [],
         "All permits verified current; missing reports identified"),
        ("Review flaring compliance and methane emissions regulations", ChecklistPriority.HIGH,
         "Environmental engineer", ["State records", "Air permits"], 20, [],
         "Flaring compliance verified; emission reduction requirements identified"),
        ("Verify financial assurance (bonding) adequacy and transfer requirements", ChecklistPriority.HIGH,
         "Regulatory specialist", ["State bonding records"], 15, [],
         "Bond amounts verified adequate; transfer or new bond requirements identified"),
        ("Review federal lease compliance (if applicable) — BLM, ONRR, NEPA", ChecklistPriority.HIGH,
         "Federal lease specialist", ["BLM records", "ONRR records"], 25, [],
         "Federal lease compliance verified; assignment processing initiated"),
        ("Assess antitrust/HSR filing requirements", ChecklistPriority.CRITICAL,
         "Buyer's counsel", ["Transaction value", "Market data"], 10, [],
         "HSR applicability determined; filing timeline established"),
    ]

    for desc, priority, responsible, sources, deadline, deps, criteria in reg_items:
        items.append(ChecklistItem(
            item_id=f"DD-{item_num:03d}",
            category="REGULATORY_AUDIT",
            description=desc,
            priority=priority,
            responsible_party=responsible,
            data_sources=sources,
            deadline_offset_days=deadline,
            dependencies=deps,
            completion_criteria=criteria,
        ))
        item_num += 1

    # PRODUCTION ANALYSIS
    prod_items = [
        ("Obtain independent production data from state regulatory database", ChecklistPriority.CRITICAL,
         "Petroleum engineer", ["State production database"], 10, [],
         "Production data obtained for all wells; reconciled against seller's data"),
        ("Perform independent decline curve analysis for all producing wells", ChecklistPriority.CRITICAL,
         "Petroleum engineer", ["Production data", "Well completion data"], 25, ["DD-021"],
         "Independent DCA completed; EUR estimated for all wells"),
        ("Compare seller's reserve report to independent analysis", ChecklistPriority.CRITICAL,
         "Petroleum engineer", ["Seller's reserve report", "Independent DCA"], 30, ["DD-022"],
         "Reserve comparison completed; variances identified and quantified"),
        ("Evaluate gas balancing positions for all multi-party wells", ChecklistPriority.MEDIUM,
         "Production accountant", ["Gas balancing statements", "Operator records"], 20, [],
         "Gas imbalances quantified and allocated"),
        ("Review artificial lift efficiency and operational upside", ChecklistPriority.MEDIUM,
         "Petroleum engineer", ["Well files", "Equipment records"], 20, [],
         "Artificial lift assessed; recompletion and optimization opportunities identified"),
    ]

    for desc, priority, responsible, sources, deadline, deps, criteria in prod_items:
        items.append(ChecklistItem(
            item_id=f"DD-{item_num:03d}",
            category="PRODUCTION_ANALYSIS",
            description=desc,
            priority=priority,
            responsible_party=responsible,
            data_sources=sources,
            deadline_offset_days=deadline,
            dependencies=deps,
            completion_criteria=criteria,
        ))
        item_num += 1

    # LEASE STATUS
    lease_items = [
        ("Verify HBP status for all leases beyond primary term", ChecklistPriority.CRITICAL,
         "Landman", ["Production records", "Lease files"], 20, [],
         "HBP verified for all post-primary term leases; marginal leases flagged"),
        ("Create lease expiration schedule and identify approaching expirations", ChecklistPriority.CRITICAL,
         "Landman", ["Lease files", "County records"], 15, [],
         "Expiration schedule complete; leases requiring immediate action identified"),
        ("Verify shut-in royalty payment compliance for non-producing leases", ChecklistPriority.HIGH,
         "Landman", ["Payment records", "Lease files"], 20, [],
         "Shut-in royalty payments verified current and in correct amounts"),
        ("Verify continuous drilling obligation compliance", ChecklistPriority.HIGH,
         "Landman", ["Drilling records", "Lease files"], 20, [],
         "Continuous drilling compliance verified for all applicable leases"),
    ]

    for desc, priority, responsible, sources, deadline, deps, criteria in lease_items:
        items.append(ChecklistItem(
            item_id=f"DD-{item_num:03d}",
            category="LEASE_STATUS",
            description=desc,
            priority=priority,
            responsible_party=responsible,
            data_sources=sources,
            deadline_offset_days=deadline,
            dependencies=deps,
            completion_criteria=criteria,
        ))
        item_num += 1

    # LIEN & ENCUMBRANCE
    lien_items = [
        ("Conduct UCC search at state Secretary of State level", ChecklistPriority.CRITICAL,
         "Buyer's counsel", ["State SOS records"], 10, [],
         "All UCC filings identified and evaluated"),
        ("Conduct county real property lien search in all relevant counties", ChecklistPriority.CRITICAL,
         "Title company", ["County records"], 15, [],
         "All real property liens identified including mortgages and deeds of trust"),
        ("Search federal and state tax lien records", ChecklistPriority.HIGH,
         "Buyer's counsel", ["IRS records", "State tax records"], 10, [],
         "All tax liens identified and status verified"),
        ("Obtain lien release commitments from seller's lenders", ChecklistPriority.CRITICAL,
         "Buyer's counsel", ["Seller's lender"], 30, [],
         "Lien release letters obtained or committed before closing"),
    ]

    for desc, priority, responsible, sources, deadline, deps, criteria in lien_items:
        items.append(ChecklistItem(
            item_id=f"DD-{item_num:03d}",
            category="LIEN_ENCUMBRANCE",
            description=desc,
            priority=priority,
            responsible_party=responsible,
            data_sources=sources,
            deadline_offset_days=deadline,
            dependencies=deps,
            completion_criteria=criteria,
        ))
        item_num += 1

    # LITIGATION REVIEW
    lit_items = [
        ("Search federal (PACER) and state court records for pending litigation", ChecklistPriority.CRITICAL,
         "Buyer's counsel", ["PACER", "State court records"], 15, [],
         "All pending litigation identified with exposure estimated"),
        ("Review seller's litigation log and demand letter files", ChecklistPriority.HIGH,
         "Buyer's counsel", ["Seller's counsel"], 20, [],
         "Seller's known litigation and threatened claims documented"),
        ("Evaluate insurance coverage for pending claims", ChecklistPriority.HIGH,
         "Insurance advisor", ["Insurance policies", "Claims records"], 20, [],
         "Coverage verified for pending claims; gaps identified"),
    ]

    for desc, priority, responsible, sources, deadline, deps, criteria in lit_items:
        items.append(ChecklistItem(
            item_id=f"DD-{item_num:03d}",
            category="LITIGATION_REVIEW",
            description=desc,
            priority=priority,
            responsible_party=responsible,
            data_sources=sources,
            deadline_offset_days=deadline,
            dependencies=deps,
            completion_criteria=criteria,
        ))
        item_num += 1

    # PREFERENTIAL RIGHTS & CONSENT
    ppr_items = [
        ("Compile complete PPR/ROFR inventory from all contracts", ChecklistPriority.CRITICAL,
         "Landman", ["JOAs", "Contracts", "Leases"], 15, [],
         "All PPR provisions identified with holder, scope, and election period"),
        ("Develop value allocation methodology for PPR notices", ChecklistPriority.HIGH,
         "Financial advisor", ["Reserve report", "Property values"], 20, [],
         "Defensible allocation methodology prepared"),
        ("Issue PPR notices and track election responses", ChecklistPriority.CRITICAL,
         "Seller's counsel", ["PPR inventory"], 25, ["DD-038", "DD-039"],
         "All PPR notices issued; election period tracked; responses documented"),
        ("Identify and compile all consent-to-assign requirements", ChecklistPriority.CRITICAL,
         "Landman", ["JOAs", "Leases", "Contracts"], 15, [],
         "All consent requirements identified with standard and timeline"),
        ("Initiate consent process for material contracts", ChecklistPriority.HIGH,
         "Seller's counsel", ["Consent inventory"], 20, ["DD-041"],
         "Consent requests delivered; responses tracked"),
    ]

    for desc, priority, responsible, sources, deadline, deps, criteria in ppr_items:
        items.append(ChecklistItem(
            item_id=f"DD-{item_num:03d}",
            category="PREFERENTIAL_RIGHTS_CONSENT",
            description=desc,
            priority=priority,
            responsible_party=responsible,
            data_sources=sources,
            deadline_offset_days=deadline,
            dependencies=deps,
            completion_criteria=criteria,
        ))
        item_num += 1

    # PSA & COMMERCIAL
    psa_items = [
        ("Review all midstream contracts (gathering, processing, transportation)", ChecklistPriority.CRITICAL,
         "Commercial analyst", ["Data room contracts"], 20, [],
         "All midstream terms evaluated; MVC exposure quantified"),
        ("Evaluate commodity hedging positions and transfer/termination", ChecklistPriority.HIGH,
         "Financial advisor", ["Hedge book", "ISDA agreements"], 15, [],
         "Hedge positions valued; transfer/termination approach agreed"),
        ("Review PSA settlement methodology and prepare settlement model", ChecklistPriority.CRITICAL,
         "Financial advisor", ["PSA", "Revenue/expense data"], 25, [],
         "Settlement model built and tested; preliminary adjustments estimated"),
        ("Analyze suspense accounts and resolution timeline", ChecklistPriority.HIGH,
         "Revenue accountant", ["Suspense reports", "Division order files"], 20, [],
         "Suspense quantified by cause and age; resolution cost estimated"),
        ("Evaluate insurance coverage adequacy and transition needs", ChecklistPriority.MEDIUM,
         "Insurance advisor", ["Insurance policies"], 20, [],
         "Coverage reviewed; post-closing insurance plan developed"),
        ("Conduct employee/labor due diligence (if entity purchase)", ChecklistPriority.MEDIUM,
         "HR consultant", ["Employee census", "Benefit plans"], 20, [],
         "Employee obligations quantified; key personnel retention planned"),
        ("Review tax considerations and structure optimization", ChecklistPriority.HIGH,
         "Tax advisor", ["Tax records", "Transaction structure"], 20, [],
         "Tax implications analyzed; purchase price allocation modeled"),
    ]

    for desc, priority, responsible, sources, deadline, deps, criteria in psa_items:
        items.append(ChecklistItem(
            item_id=f"DD-{item_num:03d}",
            category="PSA_COMMERCIAL",
            description=desc,
            priority=priority,
            responsible_party=responsible,
            data_sources=sources,
            deadline_offset_days=deadline,
            dependencies=deps,
            completion_criteria=criteria,
        ))
        item_num += 1

    return DueDiligenceChecklist(
        transaction_name=transaction_name,
        effective_date=effective_date,
        closing_target_date=closing_target,
        items=items,
    )


# ─────────────────────────────────────────────────────────────────────────────
# INTERACTION GRAPH ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class InteractionEdge:
    """An edge in the doctrine interaction graph."""
    source: str
    target: str
    relationship: str
    weight: float


@dataclass
class GraphAnalysis:
    """Analysis of the doctrine interaction graph."""
    total_nodes: int
    total_edges: int
    connected_components: int
    hub_doctrines: List[Dict[str, Any]]
    isolated_doctrines: List[str]
    critical_path: List[str]
    adjacency: Dict[str, List[str]]


def analyze_interaction_graph() -> GraphAnalysis:
    """Analyze the doctrine interaction graph to identify hubs, isolation, and critical paths.

    Returns:
        GraphAnalysis with structural metrics and findings.
    """
    adjacency: Dict[str, List[str]] = {}
    in_degree: Dict[str, int] = {}
    out_degree: Dict[str, int] = {}
    all_nodes: set = set()

    for topic, block in DOCTRINE_CACHE.items():
        all_nodes.add(topic)
        adjacency[topic] = block.interaction_edges
        out_degree[topic] = len(block.interaction_edges)
        for edge in block.interaction_edges:
            all_nodes.add(edge)
            in_degree[edge] = in_degree.get(edge, 0) + 1

    for node in all_nodes:
        if node not in adjacency:
            adjacency[node] = []
        if node not in in_degree:
            in_degree[node] = 0
        if node not in out_degree:
            out_degree[node] = 0

    total_edges = sum(len(edges) for edges in adjacency.values())

    # Hub doctrines: highest combined in+out degree
    hub_scores = []
    for node in all_nodes:
        total_degree = in_degree.get(node, 0) + out_degree.get(node, 0)
        hub_scores.append({
            "topic": node,
            "in_degree": in_degree.get(node, 0),
            "out_degree": out_degree.get(node, 0),
            "total_degree": total_degree,
        })
    hub_scores.sort(key=lambda x: x["total_degree"], reverse=True)

    # Isolated doctrines: no incoming or outgoing edges
    isolated = [n for n in all_nodes if in_degree.get(n, 0) == 0 and out_degree.get(n, 0) == 0]

    # Connected components (simple BFS)
    visited: set = set()
    components = 0
    for node in all_nodes:
        if node not in visited:
            components += 1
            queue = [node]
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                for neighbor in adjacency.get(current, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
                # Also check reverse edges
                for source, edges in adjacency.items():
                    if current in edges and source not in visited:
                        queue.append(source)

    # Critical path: longest path in the DAG (approximate via topological sort)
    critical_path: List[str] = []
    if hub_scores:
        # Start from highest-hub node, follow longest outgoing chain
        start = hub_scores[0]["topic"]
        current = start
        path_visited: set = set()
        while current and current not in path_visited:
            critical_path.append(current)
            path_visited.add(current)
            neighbors = adjacency.get(current, [])
            if not neighbors:
                break
            # Pick neighbor with highest out-degree
            best_next = None
            best_degree = -1
            for n in neighbors:
                if n not in path_visited and out_degree.get(n, 0) > best_degree:
                    best_degree = out_degree.get(n, 0)
                    best_next = n
            current = best_next

    return GraphAnalysis(
        total_nodes=len(all_nodes),
        total_edges=total_edges,
        connected_components=components,
        hub_doctrines=hub_scores[:10],
        isolated_doctrines=isolated,
        critical_path=critical_path,
        adjacency=adjacency,
    )


# ─────────────────────────────────────────────────────────────────────────────
# RISK MATRIX GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class RiskItem:
    """A single risk item in the due diligence risk matrix."""
    risk_id: str
    category: str
    description: str
    likelihood: str  # LOW, MEDIUM, HIGH
    impact: str  # LOW, MEDIUM, HIGH, CRITICAL
    risk_score: int  # 1-16
    mitigation: str
    doctrine_reference: str
    responsible_party: str


def generate_risk_matrix(
    query_responses: Optional[List[QueryResponse]] = None,
) -> List[RiskItem]:
    """Generate a risk matrix from due diligence findings.

    Args:
        query_responses: Optional list of prior query responses to analyze.

    Returns:
        List of RiskItem objects sorted by risk score.
    """
    risk_items: List[RiskItem] = []
    risk_num = 1

    # Generate baseline risk items from doctrine coverage
    baseline_risks = [
        ("TITLE_DUE_DILIGENCE", "Undisclosed mineral reservations reducing NRI below scheduled interest",
         "MEDIUM", "HIGH", 8, "Independent mineral chain analysis and NRI verification",
         "mineral_severance_analysis", "Title attorney"),
        ("TITLE_DUE_DILIGENCE", "Chain of title gap preventing delivery of marketable title",
         "MEDIUM", "CRITICAL", 12, "Early title examination with curative timeline",
         "chain_of_title_gap_analysis", "Title attorney"),
        ("ENVIRONMENTAL_COMPLIANCE", "Undisclosed environmental contamination (RECs) discovered post-closing",
         "MEDIUM", "HIGH", 8, "Phase I ESA with O&G expansion; Phase II for identified RECs",
         "phase_i_esa_scope_and_limitations", "Environmental consultant"),
        ("ENVIRONMENTAL_COMPLIANCE", "P&A liability significantly exceeding seller's ARO accrual",
         "HIGH", "HIGH", 12, "Independent P&A cost estimation; purchase price adjustment",
         "plugging_abandonment_liability", "Petroleum engineer"),
        ("REGULATORY_AUDIT", "Outstanding regulatory violations with pending penalties",
         "MEDIUM", "MEDIUM", 6, "State database search; compliance file review",
         "regulatory_compliance_audit", "Regulatory specialist"),
        ("PRODUCTION_ANALYSIS", "Seller's reserve estimates significantly overstating EUR",
         "MEDIUM", "CRITICAL", 12, "Independent DCA and reserve estimation",
         "production_decline_curve_review", "Petroleum engineer"),
        ("LEASE_STATUS", "Lease termination for failure to produce in paying quantities",
         "LOW", "CRITICAL", 8, "Production vs. lifting cost analysis for all HBP leases",
         "held_by_production_analysis", "Landman"),
        ("LEASE_STATUS", "Key lease expiration during diligence or shortly after closing",
         "MEDIUM", "HIGH", 8, "Lease expiration schedule; drilling plan coordination",
         "lease_expiration_risk", "Landman"),
        ("LIEN_ENCUMBRANCE", "Undisclosed liens or security interests on acquired assets",
         "LOW", "HIGH", 6, "Comprehensive UCC and real property lien search",
         "lien_encumbrance_search", "Buyer's counsel"),
        ("PREFERENTIAL_RIGHTS", "PPR exercise cherry-picking highest-value assets",
         "MEDIUM", "HIGH", 8, "Defensible allocation methodology; PPR exercise cap",
         "rofr_preferential_purchase_rights", "Financial advisor"),
        ("PSA_REVIEW", "Closing adjustment disputes reducing net value to buyer",
         "HIGH", "MEDIUM", 9, "Detailed settlement methodology agreed pre-signing",
         "closing_adjustments_methodology", "Financial advisor"),
        ("INDEMNIFICATION", "Insufficient indemnification coverage for pre-closing liabilities",
         "MEDIUM", "HIGH", 8, "Negotiate adequate cap, basket, and survival; escrow",
         "indemnification_provisions", "Buyer's counsel"),
        ("SUSPENSE_ANALYSIS", "Large suspense balances indicating unresolved title issues",
         "MEDIUM", "MEDIUM", 6, "Suspense analysis linked to NRI verification",
         "suspense_account_analysis", "Revenue accountant"),
        ("NRI_WI_VERIFICATION", "Systematic NRI discrepancy across multiple wells",
         "MEDIUM", "CRITICAL", 12, "Independent NRI calculation from title data",
         "nri_working_interest_verification", "Landman"),
    ]

    for cat, desc, likelihood, impact, score, mitigation, doctrine, responsible in baseline_risks:
        risk_items.append(RiskItem(
            risk_id=f"RISK-{risk_num:03d}",
            category=cat,
            description=desc,
            likelihood=likelihood,
            impact=impact,
            risk_score=score,
            mitigation=mitigation,
            doctrine_reference=doctrine,
            responsible_party=responsible,
        ))
        risk_num += 1

    risk_items.sort(key=lambda r: r.risk_score, reverse=True)
    return risk_items


# ─────────────────────────────────────────────────────────────────────────────
# ADDITIONAL FASTAPI ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────

def _add_extended_endpoints(app: Any, engine_ref: Any) -> None:
    """Add extended endpoints to the FastAPI app.

    Args:
        app: The FastAPI app instance.
        engine_ref: Reference to the engine (via app.state).
    """
    if not FASTAPI_AVAILABLE:
        return

    @app.get("/checklist")
    async def checklist_endpoint(
        transaction_name: str = Query(default="Oil & Gas Acquisition"),
        effective_date: str = Query(default=""),
        closing_target: str = Query(default=""),
    ) -> Dict[str, Any]:
        """Generate a comprehensive due diligence checklist."""
        checklist = generate_due_diligence_checklist(
            transaction_name=transaction_name,
            effective_date=effective_date,
            closing_target=closing_target,
        )
        return {
            "transaction_name": checklist.transaction_name,
            "effective_date": checklist.effective_date,
            "closing_target_date": checklist.closing_target_date,
            "generated_at": checklist.generated_at,
            "total_items": checklist.total_items,
            "categories": checklist.categories,
            "items": [
                {
                    "item_id": item.item_id,
                    "category": item.category,
                    "description": item.description,
                    "priority": item.priority.value,
                    "responsible_party": item.responsible_party,
                    "data_sources": item.data_sources,
                    "deadline_offset_days": item.deadline_offset_days,
                    "dependencies": item.dependencies,
                    "completion_criteria": item.completion_criteria,
                    "status": item.status,
                }
                for item in checklist.items
            ],
        }

    @app.get("/risk-matrix")
    async def risk_matrix_endpoint() -> Dict[str, Any]:
        """Generate a due diligence risk matrix."""
        risks = generate_risk_matrix()
        return {
            "total_risks": len(risks),
            "critical_risks": sum(1 for r in risks if r.impact == "CRITICAL"),
            "high_risks": sum(1 for r in risks if r.impact == "HIGH"),
            "risks": [
                {
                    "risk_id": r.risk_id,
                    "category": r.category,
                    "description": r.description,
                    "likelihood": r.likelihood,
                    "impact": r.impact,
                    "risk_score": r.risk_score,
                    "mitigation": r.mitigation,
                    "doctrine_reference": r.doctrine_reference,
                    "responsible_party": r.responsible_party,
                }
                for r in risks
            ],
        }

    @app.get("/interaction-graph")
    async def interaction_graph_endpoint() -> Dict[str, Any]:
        """Analyze the doctrine interaction graph."""
        analysis = analyze_interaction_graph()
        return {
            "total_nodes": analysis.total_nodes,
            "total_edges": analysis.total_edges,
            "connected_components": analysis.connected_components,
            "hub_doctrines": analysis.hub_doctrines,
            "isolated_doctrines": analysis.isolated_doctrines,
            "critical_path": analysis.critical_path,
            "adjacency_list": {k: v for k, v in analysis.adjacency.items() if v},
        }

    @app.get("/semantic/stats")
    async def semantic_stats() -> Dict[str, Any]:
        """Return semantic normalizer statistics."""
        eng = app.state.engine
        if eng is None:
            return {"error": "Engine not initialized"}
        return eng._normalizer.get_registry_stats()

    @app.get("/search/metrics")
    async def search_metrics() -> Dict[str, Any]:
        """Return search engine metrics."""
        eng = app.state.engine
        if eng is None:
            return {"error": "Engine not initialized"}
        return eng._search_engine.get_metrics()


# ─────────────────────────────────────────────────────────────────────────────
# ENTRYPOINT
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    """Launch the LM08 Due Diligence Engine."""
    if not FASTAPI_AVAILABLE:
        logger.error("FastAPI not available. Install with: pip install fastapi uvicorn")
        sys.exit(1)

    app = create_app()
    _add_extended_endpoints(app, None)
    logger.info("Starting LM08 Due Diligence Engine on port {}", ENGINE_PORT)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        access_log=False,
    )


if __name__ == "__main__":
    main()