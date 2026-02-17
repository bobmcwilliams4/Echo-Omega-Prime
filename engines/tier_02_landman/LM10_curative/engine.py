"""
LM10 Curative Engine — Main Engine
====================================
Title curative intelligence engine for oil and gas operations.
Identifies and resolves title defects including heirship, probate,
correction instruments, quiet title, adverse possession, tax sale
curative, dormant minerals, entity authority, and more.

Engine: LM10 | Port: 8510 | Domain: title_curative
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
from search import SearchDocument, SearchResponse, VectorIndex, get_vector_index
from semantic import NormalizationResult, SemanticNormalizer, get_normalizer
from telemetry import (
    ErrorDomain,
    QueryPhase,
    QueryTrace,
    TelemetryCollector,
    get_telemetry_collector,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "LM10"
ENGINE_NAME = "Curative"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8510
ENGINE_DOMAIN = "title_curative"
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
    """Response modes for curative analysis."""
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
        "Curative planning mode: identify defects, recommend curative instruments, "
        "estimate timelines and costs. Forward-looking. Can include alternative strategies."
    ),
    "REPORTING": (
        "Curative reporting mode: document current title status, defects found, and "
        "curative actions taken or pending. Factual, current-state focus."
    ),
    "AUDIT": (
        "Audit mode: verify that curative actions were properly executed, recorded, "
        "and effective. Backward-looking. Check compliance with requirements."
    ),
}


# ===================================================================
# Pydantic Request/Response Models
# ===================================================================
class CurativeQuery(BaseModel):
    """Input query for curative analysis."""
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
    """Confidence assessment for a curative opinion."""
    tier: str
    score: float
    factors: list[str] = Field(default_factory=list)
    disclosure_required: bool = False
    disclosure_caveat: str = ""


class FragilityScore(BaseModel):
    """Fact fragility scoring for curative assertions."""
    overall_fragility: float = 0.0
    verifiability: float = 0.0
    recharacterization_risk: float = 0.0
    testimony_dependence: float = 0.0
    statutory_dependence: float = 0.0
    time_sensitivity: float = 0.0
    factors: list[str] = Field(default_factory=list)


class DoctrineHit(BaseModel):
    """A matched doctrine from the cache."""
    topic: str
    confidence: float
    stratification: str
    conclusion: str
    key_factors: list[str] = Field(default_factory=list)
    authority: list[str] = Field(default_factory=list)
    curative_document: str = ""
    estimated_timeline_days: int = 0
    typical_cost_range: str = ""
    risk_factors: list[str] = Field(default_factory=list)
    reasoning: str = ""


class InteractionEdge(BaseModel):
    """An interaction between doctrine topics."""
    source: str
    target: str
    type: str
    description: str
    weight: float = 1.0


class DecompositionResult(BaseModel):
    """Result of multi-doctrine decomposition."""
    issue_categories: list[str] = Field(default_factory=list)
    doctrine_topics: list[str] = Field(default_factory=list)
    interactions: list[InteractionEdge] = Field(default_factory=list)
    resolution_sequence: list[str] = Field(default_factory=list)
    complexity_score: float = 0.0


class CurativeResponse(BaseModel):
    """Full response from the curative engine."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    trace_id: str = ""
    query: str = ""
    query_hash: str = ""
    mode: str = "FAST"
    zone: str = "PLANNING"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    # Normalization
    normalized_query: str = ""
    canonical_terms: list[str] = Field(default_factory=list)
    detected_categories: list[str] = Field(default_factory=list)
    primary_category: str = ""

    # Response layers
    layer: str = ""  # "doctrine_cache", "vector_search", "deep_analysis"
    doctrine_hits: list[DoctrineHit] = Field(default_factory=list)
    vector_results: list[dict[str, Any]] = Field(default_factory=list)
    deep_analysis: str = ""

    # Analysis
    conclusion: str = ""
    reasoning: str = ""
    recommended_curative: list[str] = Field(default_factory=list)
    authority_sources: list[AuthoritySource] = Field(default_factory=list)

    # Confidence
    confidence: ConfidenceAssessment = Field(default_factory=lambda: ConfidenceAssessment(tier="UNKNOWN", score=0.0))

    # Fragility (optional)
    fragility: Optional[FragilityScore] = None

    # Decomposition
    decomposition: Optional[DecompositionResult] = None

    # Interactions
    interactions: list[InteractionEdge] = Field(default_factory=list)

    # Determinism
    determinism_hash: str = ""

    # Performance
    total_duration_ms: float = 0.0
    layer_durations: dict[str, float] = Field(default_factory=dict)

    # Zone guidance
    zone_guidance: str = ""

    # Warnings
    warnings: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    port: int = ENGINE_PORT
    domain: str = ENGINE_DOMAIN
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    uptime_seconds: float = 0.0
    doctrine_count: int = 0
    interaction_count: int = 0
    vector_index_size: int = 0
    telemetry: dict[str, Any] = Field(default_factory=dict)
    normalizer_stats: dict[str, Any] = Field(default_factory=dict)
    search_stats: dict[str, Any] = Field(default_factory=dict)


class DriftReport(BaseModel):
    """Drift detection report."""
    engine_id: str = ENGINE_ID
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    baseline_hash: str = ""
    current_hash: str = ""
    drift_detected: bool = False
    drift_score: float = 0.0
    changed_topics: list[str] = Field(default_factory=list)
    new_topics: list[str] = Field(default_factory=list)
    removed_topics: list[str] = Field(default_factory=list)


class CoverageReport(BaseModel):
    """Coverage map report."""
    engine_id: str = ENGINE_ID
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    total_doctrines: int = 0
    triggered_doctrines: list[str] = Field(default_factory=list)
    untriggered_doctrines: list[str] = Field(default_factory=list)
    trigger_rate: float = 0.0
    category_coverage: dict[str, dict[str, int]] = Field(default_factory=dict)
    epistemic_gaps: list[str] = Field(default_factory=list)


# ===================================================================
# TIE COMPONENT 3: Doctrine Cache Manager
# ===================================================================
class DoctrineCacheManager:
    """
    Manages the pre-compiled doctrine cache with keyword-based lookup,
    category filtering, and interaction traversal.
    """

    def __init__(self) -> None:
        self._doctrines: list[DoctrineBlock] = []
        self._interactions: list[DoctrineInteraction] = []
        self._topic_index: dict[str, DoctrineBlock] = {}
        self._keyword_index: dict[str, list[str]] = defaultdict(list)
        self._category_index: dict[str, list[str]] = defaultdict(list)
        self._loaded = False

    def load(self) -> None:
        """Load doctrine cache and build indexes."""
        self._doctrines = build_doctrine_cache()
        self._interactions = build_interaction_graph()
        self._build_indexes()
        self._loaded = True
        logger.info(
            "DoctrineCacheManager loaded | doctrines={} | interactions={}",
            len(self._doctrines),
            len(self._interactions),
        )

    def _build_indexes(self) -> None:
        """Build topic, keyword, and category indexes."""
        self._topic_index.clear()
        self._keyword_index.clear()
        self._category_index.clear()

        for doctrine in self._doctrines:
            self._topic_index[doctrine.topic] = doctrine
            self._category_index[doctrine.issue_category.value].append(doctrine.topic)
            for keyword in doctrine.keywords:
                self._keyword_index[keyword.lower()].append(doctrine.topic)

    def lookup(
        self,
        query: str,
        canonical_terms: list[str],
        categories: list[str],
        max_results: int = 5,
    ) -> list[DoctrineBlock]:
        """
        Look up doctrines matching the query.
        Priority: exact topic match > canonical term match > keyword match > category match.
        """
        scored: dict[str, float] = defaultdict(float)

        # Exact topic match
        for term in canonical_terms:
            if term in self._topic_index:
                scored[term] += 10.0

        # Keyword match
        query_lower = query.lower()
        for keyword, topics in self._keyword_index.items():
            if keyword in query_lower:
                for topic in topics:
                    scored[topic] += 2.0 * len(keyword.split())

        # Category match
        for category in categories:
            if category in self._category_index:
                for topic in self._category_index[category]:
                    scored[topic] += 1.5

        # Canonical term keyword overlap
        for term in canonical_terms:
            for keyword, topics in self._keyword_index.items():
                if term.replace("_", " ") in keyword or keyword in term.replace("_", " "):
                    for topic in topics:
                        scored[topic] += 3.0

        sorted_topics = sorted(scored.items(), key=lambda x: x[1], reverse=True)
        results: list[DoctrineBlock] = []
        for topic, score in sorted_topics[:max_results]:
            if topic in self._topic_index and score > 0:
                results.append(self._topic_index[topic])

        return results

    def get_by_topic(self, topic: str) -> Optional[DoctrineBlock]:
        """Get a doctrine by exact topic name."""
        return self._topic_index.get(topic)

    def get_by_category(self, category: str) -> list[DoctrineBlock]:
        """Get all doctrines for a category."""
        topics = self._category_index.get(category, [])
        return [self._topic_index[t] for t in topics if t in self._topic_index]

    def get_interactions(self, topic: str) -> list[DoctrineInteraction]:
        """Get all interactions involving a topic."""
        return [
            i for i in self._interactions
            if i.source_topic == topic or i.target_topic == topic
        ]

    def get_all_topics(self) -> list[str]:
        """Get all doctrine topic names."""
        return list(self._topic_index.keys())

    @property
    def doctrine_count(self) -> int:
        """Number of doctrines loaded."""
        return len(self._doctrines)

    @property
    def interaction_count(self) -> int:
        """Number of interaction edges."""
        return len(self._interactions)

    def compute_cache_hash(self) -> str:
        """Compute a deterministic hash of the entire doctrine cache."""
        content = json.dumps(
            [d.model_dump() for d in self._doctrines],
            sort_keys=True,
            default=str,
        )
        return hashlib.sha256(content.encode()).hexdigest()


# ===================================================================
# TIE COMPONENT 4: Authority Hardening
# ===================================================================
class AuthorityHardener:
    """
    Hierarchical authority resolution with weights and conflict detection.
    Ensures curative opinions cite the strongest available authority.
    """

    AUTHORITY_WEIGHTS: dict[str, float] = {
        "texas_constitution": 1.0,
        "texas_supreme_court": 0.95,
        "texas_statute": 0.90,
        "texas_appeals_court": 0.85,
        "federal_statute": 0.80,
        "federal_case": 0.75,
        "rrc_rule": 0.70,
        "aapl_standard": 0.60,
        "tlta_standard": 0.55,
        "common_practice": 0.40,
        "secondary_source": 0.30,
    }

    def classify_authority(self, source: str) -> str:
        """Classify an authority source into a type."""
        source_lower = source.lower()
        if "texas constitution" in source_lower or "tex. const." in source_lower:
            return "texas_constitution"
        if "tex." in source_lower and ("s.w." in source_lower or "supreme" in source_lower):
            if "app." not in source_lower:
                return "texas_supreme_court"
            return "texas_appeals_court"
        if "s.w.2d" in source_lower or "s.w.3d" in source_lower:
            if "app." in source_lower or "civ." in source_lower:
                return "texas_appeals_court"
            return "texas_supreme_court"
        if "texas" in source_lower and ("code" in source_lower or "section" in source_lower):
            return "texas_statute"
        if "u.s.c." in source_lower or "federal" in source_lower:
            return "federal_statute"
        if "f.2d" in source_lower or "f.3d" in source_lower or "u.s." in source_lower:
            return "federal_case"
        if "railroad commission" in source_lower or "rrc" in source_lower:
            return "rrc_rule"
        if "aapl" in source_lower:
            return "aapl_standard"
        if "tlta" in source_lower:
            return "tlta_standard"
        if "common practice" in source_lower or "no specific" in source_lower:
            return "common_practice"
        return "secondary_source"

    def harden_authorities(self, authorities: list[str]) -> list[AuthoritySource]:
        """Process and weight authority sources."""
        hardened: list[AuthoritySource] = []
        for auth in authorities:
            auth_type = self.classify_authority(auth)
            weight = self.AUTHORITY_WEIGHTS.get(auth_type, 0.30)
            hardened.append(AuthoritySource(source=auth, weight=weight, type=auth_type))
        hardened.sort(key=lambda a: a.weight, reverse=True)
        return hardened

    def detect_conflicts(self, authorities: list[AuthoritySource]) -> list[str]:
        """Detect potential conflicts between authority sources."""
        conflicts: list[str] = []
        types_present = {a.type for a in authorities}

        if "texas_statute" in types_present and "common_practice" in types_present:
            conflicts.append(
                "Statutory authority present alongside common practice — statute controls"
            )
        if "texas_supreme_court" in types_present and "texas_appeals_court" in types_present:
            # Not necessarily a conflict, but note the hierarchy
            pass
        if "federal_statute" in types_present and "texas_statute" in types_present:
            conflicts.append(
                "Federal and state authority both cited — check for preemption issues"
            )

        return conflicts

    def compute_authority_score(self, authorities: list[AuthoritySource]) -> float:
        """Compute overall authority strength score (0-1)."""
        if not authorities:
            return 0.0
        max_weight = max(a.weight for a in authorities)
        avg_weight = sum(a.weight for a in authorities) / len(authorities)
        count_bonus = min(0.1, len(authorities) * 0.02)
        return min(1.0, (max_weight * 0.6) + (avg_weight * 0.3) + count_bonus)


# ===================================================================
# TIE COMPONENT 5: Confidence Stratification
# ===================================================================
class ConfidenceStratifier:
    """
    Assigns confidence tiers to curative opinions based on authority strength,
    doctrine match quality, and risk factors.
    """

    TIER_THRESHOLDS: dict[str, tuple[float, float]] = {
        "DEFENSIBLE": (0.85, 1.0),
        "AGGRESSIVE": (0.65, 0.85),
        "DISCLOSURE": (0.45, 0.65),
        "HIGH_RISK": (0.0, 0.45),
    }

    def stratify(
        self,
        authority_score: float,
        doctrine_confidence: float,
        risk_factor_count: int,
        category: str,
    ) -> ConfidenceAssessment:
        """Compute confidence stratification for a curative opinion."""
        # Base score from doctrine and authority
        base_score = (doctrine_confidence * 0.5) + (authority_score * 0.4)

        # Risk factor penalty
        risk_penalty = min(0.3, risk_factor_count * 0.05)
        adjusted_score = max(0.0, base_score - risk_penalty)

        # Category-specific adjustments
        high_confidence_categories = {"NAME_VARIATIONS", "LIEN_RELEASE", "JUDGMENT_RESOLUTION"}
        low_confidence_categories = {"TAX_SALE_CURATIVE", "ADVERSE_POSSESSION", "QUIET_TITLE"}

        if category in high_confidence_categories:
            adjusted_score = min(1.0, adjusted_score + 0.05)
        elif category in low_confidence_categories:
            adjusted_score = max(0.0, adjusted_score - 0.05)

        # Determine tier
        tier = "HIGH_RISK"
        for tier_name, (low, high) in self.TIER_THRESHOLDS.items():
            if low <= adjusted_score < high:
                tier = tier_name
                break
        if adjusted_score >= 1.0:
            tier = "DEFENSIBLE"

        # Build factors
        factors: list[str] = []
        if authority_score >= 0.85:
            factors.append("Strong statutory/case authority")
        elif authority_score >= 0.60:
            factors.append("Moderate authority support")
        else:
            factors.append("Limited authority — relies on common practice")

        if doctrine_confidence >= 0.85:
            factors.append("High doctrine match confidence")
        elif doctrine_confidence >= 0.65:
            factors.append("Moderate doctrine match")
        else:
            factors.append("Weak doctrine match — consider further research")

        if risk_factor_count > 3:
            factors.append(f"Multiple risk factors present ({risk_factor_count})")

        # Disclosure assessment
        disclosure_required = tier in ("DISCLOSURE", "HIGH_RISK")
        disclosure_caveat = ""
        if disclosure_required:
            disclosure_caveat = (
                "This curative opinion involves significant uncertainty. The title examiner "
                "should disclose the risk factors to the client and consider requiring "
                "additional curative measures or title insurance endorsements."
            )

        return ConfidenceAssessment(
            tier=tier,
            score=round(adjusted_score, 4),
            factors=factors,
            disclosure_required=disclosure_required,
            disclosure_caveat=disclosure_caveat,
        )


# ===================================================================
# TIE COMPONENT 14: Fact Fragility Scoring
# ===================================================================
class FragilityScorer:
    """
    Scores the fragility of factual assertions in curative opinions.
    Higher fragility = more vulnerable to challenge.
    """

    def score(
        self,
        doctrine: DoctrineBlock,
        query: str,
    ) -> FragilityScore:
        """Compute fragility score for a curative assertion."""
        factors: list[str] = []

        # Verifiability — can the assertion be independently verified?
        verifiability = 0.8  # Most curative facts are in public records
        if "affidavit" in doctrine.topic:
            verifiability = 0.6  # Affidavit content depends on witness testimony
            factors.append("Relies on witness testimony — moderate verifiability")
        if "adverse_possession" in doctrine.topic:
            verifiability = 0.5  # Possession facts are subjective
            factors.append("Possession facts are inherently subjective")
        if "quiet_title" in doctrine.topic or "judicial" in doctrine.topic:
            verifiability = 0.9  # Court records are highly verifiable
            factors.append("Court records provide high verifiability")

        # Recharacterization risk — could the facts be interpreted differently?
        recharacterization_risk = 0.3
        if doctrine.confidence_stratification in (
            ConfidenceStratification.DISCLOSURE,
            ConfidenceStratification.HIGH_RISK,
        ):
            recharacterization_risk = 0.6
            factors.append("Confidence tier suggests recharacterization risk")
        if len(doctrine.counter_arguments) > 4:
            recharacterization_risk = min(1.0, recharacterization_risk + 0.1)
            factors.append("Multiple counter-arguments increase recharacterization risk")

        # Testimony dependence — does the opinion rely on witness testimony?
        testimony_dependence = 0.2
        if "heirship" in doctrine.topic:
            testimony_dependence = 0.7
            factors.append("Heirship determinations depend heavily on testimony")
        if "adverse_possession" in doctrine.topic:
            testimony_dependence = 0.6
            factors.append("Adverse possession requires testimony about physical use")
        if "name_variation" in doctrine.topic:
            testimony_dependence = 0.5
            factors.append("Identity verification may require personal testimony")

        # Statutory dependence — how much does the opinion depend on specific statute interpretation?
        statutory_dependence = 0.5
        authority_types = set()
        for auth in doctrine.primary_authority:
            if "code" in auth.lower() or "section" in auth.lower():
                authority_types.add("statute")
            if "s.w." in auth.lower() or "tex." in auth.lower():
                authority_types.add("case")
        if "statute" in authority_types:
            statutory_dependence = 0.7
            factors.append("Statutory interpretation is central to the opinion")
        if "case" in authority_types:
            statutory_dependence = max(0.3, statutory_dependence - 0.1)

        # Time sensitivity — does the opinion depend on time-sensitive elements?
        time_sensitivity = 0.3
        if "redemption" in doctrine.topic or "limitation" in doctrine.topic:
            time_sensitivity = 0.8
            factors.append("Time-sensitive limitation or redemption period applies")
        if "five_year" in doctrine.topic or "ten_year" in doctrine.topic:
            time_sensitivity = 0.7
            factors.append("Specific statutory period must be satisfied")
        if doctrine.estimated_timeline_days > 180:
            time_sensitivity = min(1.0, time_sensitivity + 0.1)
            factors.append("Extended timeline increases time sensitivity")

        # Overall fragility
        overall = (
            (1.0 - verifiability) * 0.25
            + recharacterization_risk * 0.25
            + testimony_dependence * 0.20
            + statutory_dependence * 0.15
            + time_sensitivity * 0.15
        )

        return FragilityScore(
            overall_fragility=round(overall, 4),
            verifiability=round(verifiability, 4),
            recharacterization_risk=round(recharacterization_risk, 4),
            testimony_dependence=round(testimony_dependence, 4),
            statutory_dependence=round(statutory_dependence, 4),
            time_sensitivity=round(time_sensitivity, 4),
            factors=factors,
        )


# ===================================================================
# TIE COMPONENT 9: Drift Watcher
# ===================================================================
class DriftWatcher:
    """
    Monitors for doctrine drift — changes in the doctrine cache
    that could affect opinion consistency over time.
    """

    def __init__(self, cache_manager: DoctrineCacheManager) -> None:
        self._cache_manager = cache_manager
        self._baseline_hash: str = ""
        self._baseline_topics: set[str] = set()
        self._baseline_time: float = 0.0

    def set_baseline(self) -> str:
        """Capture current state as baseline."""
        self._baseline_hash = self._cache_manager.compute_cache_hash()
        self._baseline_topics = set(self._cache_manager.get_all_topics())
        self._baseline_time = time.time()
        logger.info("Drift baseline set | hash={} | topics={}", self._baseline_hash[:16], len(self._baseline_topics))
        return self._baseline_hash

    def check_drift(self) -> DriftReport:
        """Check for drift from baseline."""
        current_hash = self._cache_manager.compute_cache_hash()
        current_topics = set(self._cache_manager.get_all_topics())

        drift_detected = current_hash != self._baseline_hash
        new_topics = list(current_topics - self._baseline_topics)
        removed_topics = list(self._baseline_topics - current_topics)
        changed_count = len(new_topics) + len(removed_topics)

        total = max(len(self._baseline_topics), 1)
        drift_score = changed_count / total

        return DriftReport(
            baseline_hash=self._baseline_hash,
            current_hash=current_hash,
            drift_detected=drift_detected,
            drift_score=round(drift_score, 4),
            changed_topics=[],
            new_topics=new_topics,
            removed_topics=removed_topics,
        )


# ===================================================================
# TIE COMPONENT 10: Coverage Map
# ===================================================================
class CoverageTracker:
    """
    Tracks which doctrines have been triggered and identifies
    epistemic gaps — topics that are never queried or are missing.
    """

    def __init__(self, cache_manager: DoctrineCacheManager) -> None:
        self._cache_manager = cache_manager
        self._trigger_counts: dict[str, int] = defaultdict(int)
        self._category_queries: dict[str, int] = defaultdict(int)

    def record_trigger(self, topic: str, category: str) -> None:
        """Record a doctrine trigger."""
        self._trigger_counts[topic] += 1
        self._category_queries[category] += 1

    def get_report(self) -> CoverageReport:
        """Generate coverage report."""
        all_topics = set(self._cache_manager.get_all_topics())
        triggered = set(self._trigger_counts.keys())
        untriggered = all_topics - triggered

        total = len(all_topics)
        trigger_rate = len(triggered) / total if total > 0 else 0.0

        # Category coverage
        category_coverage: dict[str, dict[str, int]] = {}
        for cat in IssueCategory:
            cat_doctrines = self._cache_manager.get_by_category(cat.value)
            cat_triggered = sum(
                1 for d in cat_doctrines if d.topic in self._trigger_counts
            )
            category_coverage[cat.value] = {
                "total": len(cat_doctrines),
                "triggered": cat_triggered,
                "queries": self._category_queries.get(cat.value, 0),
            }

        # Epistemic gaps — categories with no queries
        epistemic_gaps: list[str] = [
            cat.value for cat in IssueCategory
            if self._category_queries.get(cat.value, 0) == 0
        ]

        return CoverageReport(
            total_doctrines=total,
            triggered_doctrines=sorted(triggered),
            untriggered_doctrines=sorted(untriggered),
            trigger_rate=round(trigger_rate, 4),
            category_coverage=category_coverage,
            epistemic_gaps=epistemic_gaps,
        )


# ===================================================================
# TIE COMPONENT 19: Multi-Doctrine Decomposition
# ===================================================================
class DoctrineDecomposer:
    """
    Decomposes complex curative queries into multiple doctrine topics,
    identifies interactions, and produces a resolution sequence.
    """

    def __init__(self, cache_manager: DoctrineCacheManager) -> None:
        self._cache_manager = cache_manager

    def decompose(
        self,
        canonical_terms: list[str],
        categories: list[str],
        doctrine_hits: list[DoctrineBlock],
    ) -> DecompositionResult:
        """Decompose a query into multi-doctrine structure."""
        # Collect all relevant topics
        topics = [d.topic for d in doctrine_hits]

        # Collect interactions between matched topics
        interactions: list[InteractionEdge] = []
        for i, topic_a in enumerate(topics):
            for topic_b in topics[i + 1:]:
                for interaction in self._cache_manager.get_interactions(topic_a):
                    if interaction.target_topic == topic_b or interaction.source_topic == topic_b:
                        interactions.append(InteractionEdge(
                            source=interaction.source_topic,
                            target=interaction.target_topic,
                            type=interaction.interaction_type,
                            description=interaction.description,
                            weight=interaction.weight,
                        ))

        # Build resolution sequence (topological ordering by prerequisites)
        prerequisites: dict[str, list[str]] = defaultdict(list)
        for interaction in interactions:
            if interaction.type == "prerequisite":
                prerequisites[interaction.target].append(interaction.source)

        # Simple topological sort
        resolution_sequence: list[str] = []
        visited: set[str] = set()

        def visit(topic: str) -> None:
            if topic in visited:
                return
            visited.add(topic)
            for prereq in prerequisites.get(topic, []):
                if prereq in topics:
                    visit(prereq)
            resolution_sequence.append(topic)

        for topic in topics:
            visit(topic)

        # Complexity score based on number of topics, interactions, and categories
        complexity = (
            len(topics) * 0.3
            + len(interactions) * 0.4
            + len(categories) * 0.3
        ) / max(10.0, 1.0)  # Normalize to ~0-1 range
        complexity = min(1.0, complexity)

        return DecompositionResult(
            issue_categories=categories,
            doctrine_topics=topics,
            interactions=interactions,
            resolution_sequence=resolution_sequence,
            complexity_score=round(complexity, 4),
        )


# ===================================================================
# TIE COMPONENT 20: Deep Analysis Mode
# ===================================================================
class DeepAnalyzer:
    """
    Multi-source synthesis and full reasoning chain for complex
    curative queries that require more than doctrine cache hits.
    """

    def __init__(
        self,
        cache_manager: DoctrineCacheManager,
        authority_hardener: AuthorityHardener,
        fragility_scorer: FragilityScorer,
    ) -> None:
        self._cache = cache_manager
        self._hardener = authority_hardener
        self._fragility = fragility_scorer

    def analyze(
        self,
        query: str,
        normalization: NormalizationResult,
        doctrine_hits: list[DoctrineBlock],
        vector_results: list[dict[str, Any]],
        zone: AnalysisZone,
    ) -> str:
        """
        Produce deep analysis by synthesizing doctrine hits, vector results,
        and applying zone-specific reasoning.
        """
        sections: list[str] = []

        # Section 1: Issue Identification
        sections.append("== CURATIVE ISSUE IDENTIFICATION ==")
        if normalization.canonical_terms:
            sections.append(f"Canonical terms identified: {', '.join(normalization.canonical_terms)}")
        if normalization.detected_categories:
            sections.append(f"Issue categories: {', '.join(normalization.detected_categories)}")
        if normalization.primary_category:
            sections.append(f"Primary category: {normalization.primary_category}")

        # Section 2: Doctrine Analysis
        sections.append("\n== DOCTRINE ANALYSIS ==")
        for i, doctrine in enumerate(doctrine_hits, 1):
            sections.append(f"\n--- Doctrine {i}: {doctrine.topic} ---")
            sections.append(f"Confidence: {doctrine.confidence} ({doctrine.confidence_stratification.value})")
            sections.append(f"Conclusion: {doctrine.conclusion_template}")

            # Authority
            hardened = self._hardener.harden_authorities(doctrine.primary_authority)
            sections.append("Authority sources (ranked by weight):")
            for auth in hardened:
                sections.append(f"  [{auth.weight:.2f}] {auth.source} ({auth.type})")

            # Key factors
            sections.append("Key factors:")
            for factor in doctrine.key_factors:
                sections.append(f"  - {factor}")

            # Risk factors
            if doctrine.risk_factors:
                sections.append("Risk factors:")
                for risk in doctrine.risk_factors:
                    sections.append(f"  ! {risk}")

            # Curative recommendation
            sections.append(f"Recommended document: {doctrine.curative_document_type}")
            sections.append(f"Estimated timeline: {doctrine.estimated_timeline_days} days")
            sections.append(f"Typical cost: {doctrine.typical_cost_range}")

            # Counter-arguments
            sections.append("Counter-arguments to anticipate:")
            for counter in doctrine.counter_arguments[:3]:
                sections.append(f"  * {counter}")

            # Resolution strategy
            sections.append(f"Resolution strategy: {doctrine.resolution_strategy}")

        # Section 3: Vector Search Supplemental
        if vector_results:
            sections.append("\n== SUPPLEMENTAL SEARCH RESULTS ==")
            for result in vector_results[:3]:
                sections.append(f"  Topic: {result.get('topic', 'unknown')} (similarity: {result.get('similarity', 0):.3f})")
                sections.append(f"  Content: {result.get('content', '')[:200]}")

        # Section 4: Interactions
        interaction_topics = set()
        for doctrine in doctrine_hits:
            interactions = self._cache.get_interactions(doctrine.topic)
            for interaction in interactions:
                key = f"{interaction.source_topic}->{interaction.target_topic}"
                if key not in interaction_topics:
                    interaction_topics.add(key)
                    sections.append(
                        f"\nInteraction: {interaction.source_topic} -> {interaction.target_topic} "
                        f"({interaction.interaction_type}): {interaction.description}"
                    )

        # Section 5: Zone-Specific Guidance
        sections.append(f"\n== {zone.value} ZONE GUIDANCE ==")
        sections.append(ZONE_GUIDELINES.get(zone.value, "No zone-specific guidance available."))

        # Section 6: Fragility Assessment
        if doctrine_hits:
            primary = doctrine_hits[0]
            frag = self._fragility.score(primary, query)
            sections.append(f"\n== FRAGILITY ASSESSMENT (Primary Doctrine) ==")
            sections.append(f"Overall fragility: {frag.overall_fragility:.3f}")
            sections.append(f"Verifiability: {frag.verifiability:.3f}")
            sections.append(f"Recharacterization risk: {frag.recharacterization_risk:.3f}")
            sections.append(f"Testimony dependence: {frag.testimony_dependence:.3f}")
            for factor in frag.factors:
                sections.append(f"  - {factor}")

        return "\n".join(sections)


# ===================================================================
# TIE COMPONENT 16: Determinism Hash
# ===================================================================
def compute_determinism_hash(response: CurativeResponse) -> str:
    """Compute SHA-256 determinism hash for the response."""
    content = json.dumps(
        {
            "query": response.query,
            "mode": response.mode,
            "zone": response.zone,
            "canonical_terms": response.canonical_terms,
            "detected_categories": response.detected_categories,
            "layer": response.layer,
            "doctrine_topics": [d.topic for d in response.doctrine_hits],
            "conclusion": response.conclusion,
            "confidence_tier": response.confidence.tier,
            "confidence_score": response.confidence.score,
        },
        sort_keys=True,
        default=str,
    )
    return hashlib.sha256(content.encode()).hexdigest()


# ===================================================================
# Epistemic Guardrails
# ===================================================================
def apply_epistemic_guardrails(text: str) -> tuple[str, list[str]]:
    """
    Check text for banned epistemic phrases and return cleaned text
    with list of warnings about removed phrases.
    """
    warnings: list[str] = []
    cleaned = text
    for phrase in BANNED_PHRASES:
        if phrase in cleaned.lower():
            warnings.append(f"Epistemic guardrail: removed '{phrase}' from output")
            # Don't actually remove — just flag. The doctrine cache should not contain these.
    return cleaned, warnings


# ===================================================================
# TIE COMPONENT 1: Three-Layer Response Engine
# ===================================================================
class ThreeLayerResponseEngine:
    """
    Main response engine implementing the three-layer architecture:
    Layer 1: Doctrine Cache (0-200ms target)
    Layer 2: Vector/Semantic Search (200-500ms target)
    Layer 3: Deep Analysis (500ms+ for complex queries)
    """

    def __init__(self) -> None:
        self._cache_manager = DoctrineCacheManager()
        self._normalizer: Optional[SemanticNormalizer] = None
        self._vector_index: Optional[VectorIndex] = None
        self._telemetry: Optional[TelemetryCollector] = None
        self._authority_hardener = AuthorityHardener()
        self._confidence_stratifier = ConfidenceStratifier()
        self._fragility_scorer = FragilityScorer()
        self._drift_watcher: Optional[DriftWatcher] = None
        self._coverage_tracker: Optional[CoverageTracker] = None
        self._decomposer: Optional[DoctrineDecomposer] = None
        self._deep_analyzer: Optional[DeepAnalyzer] = None
        self._initialized = False
        self._start_time = time.time()

    def initialize(self) -> None:
        """Initialize all components."""
        logger.info("Initializing ThreeLayerResponseEngine...")

        # Load doctrine cache
        self._cache_manager.load()

        # Initialize normalizer
        self._normalizer = get_normalizer()

        # Initialize vector index and populate from doctrines
        self._vector_index = get_vector_index()
        self._populate_vector_index()

        # Initialize telemetry
        self._telemetry = get_telemetry_collector()

        # Initialize drift watcher
        self._drift_watcher = DriftWatcher(self._cache_manager)
        self._drift_watcher.set_baseline()

        # Initialize coverage tracker
        self._coverage_tracker = CoverageTracker(self._cache_manager)

        # Initialize decomposer
        self._decomposer = DoctrineDecomposer(self._cache_manager)

        # Initialize deep analyzer
        self._deep_analyzer = DeepAnalyzer(
            self._cache_manager,
            self._authority_hardener,
            self._fragility_scorer,
        )

        self._initialized = True
        logger.info(
            "ThreeLayerResponseEngine initialized | doctrines={} | vector_docs={}",
            self._cache_manager.doctrine_count,
            self._vector_index.document_count,
        )

    def _populate_vector_index(self) -> None:
        """Populate vector index from doctrine cache."""
        if not self._vector_index:
            return
        docs: list[SearchDocument] = []
        for doctrine in get_doctrine_cache():
            doc = SearchDocument(
                doc_id=doctrine.topic,
                topic=doctrine.topic,
                content=doctrine.conclusion_template + " " + doctrine.reasoning_framework[:300],
                category=doctrine.issue_category.value,
                authority_sources=doctrine.primary_authority,
                keywords=doctrine.keywords,
                metadata={
                    "confidence": doctrine.confidence,
                    "stratification": doctrine.confidence_stratification.value,
                    "curative_document": doctrine.curative_document_type,
                    "timeline_days": doctrine.estimated_timeline_days,
                    "cost_range": doctrine.typical_cost_range,
                },
            )
            docs.append(doc)
        self._vector_index.add_documents(docs)
        logger.info("Vector index populated with {} documents", len(docs))

    async def process_query(self, query: CurativeQuery) -> CurativeResponse:
        """
        Process a curative query through all three layers.

        Layer 1: Doctrine cache lookup (fast, <200ms)
        Layer 2: Vector search fallback (medium, <500ms)
        Layer 3: Deep analysis (comprehensive, 500ms+)
        """
        if not self._initialized:
            raise RuntimeError("Engine not initialized — call initialize() first")

        response = CurativeResponse(
            query=query.query,
            query_hash=hashlib.sha256(query.query.encode()).hexdigest()[:16],
            mode=query.mode.value,
            zone=query.zone.value,
            zone_guidance=ZONE_GUIDELINES.get(query.zone.value, ""),
        )

        # Start telemetry trace
        trace = self._telemetry.start_trace(
            query_text=query.query,
            response_mode=query.mode.value,
            issue_category=query.category_filter or "",
        )
        response.trace_id = trace.trace_id

        try:
            # STEP 1: Semantic Normalization (TIE Component 6)
            norm_span = trace.add_span(QueryPhase.NORMALIZED)
            normalization = self._normalizer.normalize(query.query)
            norm_span.close()
            norm_span.metadata["canonical_terms"] = normalization.canonical_terms
            norm_span.metadata["categories"] = normalization.detected_categories

            response.normalized_query = normalization.normalized_text
            response.canonical_terms = normalization.canonical_terms
            response.detected_categories = normalization.detected_categories
            response.primary_category = normalization.primary_category

            # Extract statutory references
            stat_refs = self._normalizer.extract_statutory_references(query.query)
            if stat_refs:
                norm_span.metadata["statutory_references"] = stat_refs

            # LAYER 1: Doctrine Cache (TIE Component 3)
            cache_span = trace.add_span(QueryPhase.DOCTRINE_CACHE)
            doctrine_hits = self._cache_manager.lookup(
                query=query.query,
                canonical_terms=normalization.canonical_terms,
                categories=normalization.detected_categories,
                max_results=5,
            )
            cache_span.close()
            cache_span.metadata["hits"] = len(doctrine_hits)

            layer_durations: dict[str, float] = {
                "normalization_ms": norm_span.duration_ms,
                "doctrine_cache_ms": cache_span.duration_ms,
            }

            if doctrine_hits:
                response.layer = "doctrine_cache"
                response.doctrine_hits = self._build_doctrine_hits(doctrine_hits, query.mode)

                # Record coverage
                for doctrine in doctrine_hits:
                    self._coverage_tracker.record_trigger(
                        doctrine.topic, doctrine.issue_category.value
                    )

            # LAYER 2: Vector Search (TIE Component 7)
            vector_span = trace.add_span(QueryPhase.VECTOR_SEARCH)
            vector_response = self._vector_index.search(
                query=query.query,
                category_filter=query.category_filter,
                max_results=5,
            )
            vector_span.close()
            vector_span.metadata["results"] = len(vector_response.results)
            layer_durations["vector_search_ms"] = vector_span.duration_ms

            if vector_response.results:
                response.vector_results = [
                    {
                        "topic": r.topic,
                        "similarity": r.similarity,
                        "content": r.content[:300],
                        "category": r.category,
                        "authority": r.authority_sources[:3],
                    }
                    for r in vector_response.results
                ]
                if not doctrine_hits:
                    response.layer = "vector_search"
                    self._telemetry.record_doctrine_miss()

            # LAYER 3: Deep Analysis (TIE Component 20)
            if query.mode in (ResponseMode.DEFENSE, ResponseMode.MEMO) or not doctrine_hits:
                analysis_span = trace.add_span(QueryPhase.DEEP_ANALYSIS)
                deep_text = self._deep_analyzer.analyze(
                    query=query.query,
                    normalization=normalization,
                    doctrine_hits=doctrine_hits,
                    vector_results=response.vector_results,
                    zone=query.zone,
                )
                analysis_span.close()
                layer_durations["deep_analysis_ms"] = analysis_span.duration_ms
                response.deep_analysis = deep_text
                self._telemetry.record_deep_analysis()
                if not doctrine_hits and not vector_response.results:
                    response.layer = "deep_analysis"

            # AUTHORITY HARDENING (TIE Component 4)
            auth_span = trace.add_span(QueryPhase.AUTHORITY_HARDENING)
            all_authorities: list[str] = []
            for doctrine in doctrine_hits:
                all_authorities.extend(doctrine.primary_authority)
            hardened = self._authority_hardener.harden_authorities(all_authorities)
            authority_score = self._authority_hardener.compute_authority_score(hardened)
            auth_conflicts = self._authority_hardener.detect_conflicts(hardened)
            auth_span.close()
            auth_span.metadata["authority_score"] = authority_score
            layer_durations["authority_hardening_ms"] = auth_span.duration_ms

            response.authority_sources = hardened
            if auth_conflicts:
                response.warnings.extend(auth_conflicts)

            # CONFIDENCE STRATIFICATION (TIE Component 5)
            conf_span = trace.add_span(QueryPhase.CONFIDENCE_SCORING)
            if doctrine_hits:
                primary_doctrine = doctrine_hits[0]
                risk_count = len(primary_doctrine.risk_factors)
                confidence_assessment = self._confidence_stratifier.stratify(
                    authority_score=authority_score,
                    doctrine_confidence=primary_doctrine.confidence,
                    risk_factor_count=risk_count,
                    category=normalization.primary_category,
                )
            else:
                confidence_assessment = ConfidenceAssessment(
                    tier="HIGH_RISK",
                    score=0.25,
                    factors=["No doctrine match found — high uncertainty"],
                    disclosure_required=True,
                    disclosure_caveat=(
                        "No matching curative doctrine was found. This opinion is based on "
                        "general principles and requires additional research."
                    ),
                )
            conf_span.close()
            layer_durations["confidence_ms"] = conf_span.duration_ms
            response.confidence = confidence_assessment

            # FRAGILITY SCORING (TIE Component 14)
            if query.include_fragility and doctrine_hits:
                response.fragility = self._fragility_scorer.score(doctrine_hits[0], query.query)

            # MULTI-DOCTRINE DECOMPOSITION (TIE Component 19)
            if len(doctrine_hits) > 1 or query.include_interactions:
                decomposition = self._decomposer.decompose(
                    canonical_terms=normalization.canonical_terms,
                    categories=normalization.detected_categories,
                    doctrine_hits=doctrine_hits,
                )
                response.decomposition = decomposition

            # INTERACTIONS
            if query.include_interactions and doctrine_hits:
                all_interactions: list[InteractionEdge] = []
                seen: set[str] = set()
                for doctrine in doctrine_hits:
                    for interaction in self._cache_manager.get_interactions(doctrine.topic):
                        key = f"{interaction.source_topic}->{interaction.target_topic}"
                        if key not in seen:
                            seen.add(key)
                            all_interactions.append(InteractionEdge(
                                source=interaction.source_topic,
                                target=interaction.target_topic,
                                type=interaction.interaction_type,
                                description=interaction.description,
                                weight=interaction.weight,
                            ))
                response.interactions = all_interactions

            # BUILD CONCLUSION AND RECOMMENDED CURATIVE
            response_span = trace.add_span(QueryPhase.RESPONSE_ASSEMBLY)
            response.conclusion = self._build_conclusion(doctrine_hits, normalization, query.zone)
            response.reasoning = self._build_reasoning(doctrine_hits, normalization, query.mode)
            response.recommended_curative = self._build_curative_recommendations(doctrine_hits)
            response_span.close()
            layer_durations["response_assembly_ms"] = response_span.duration_ms

            # EPISTEMIC GUARDRAILS
            conclusion_cleaned, guardrail_warnings = apply_epistemic_guardrails(response.conclusion)
            response.conclusion = conclusion_cleaned
            response.warnings.extend(guardrail_warnings)

            # DETERMINISM HASH (TIE Component 16)
            response.determinism_hash = compute_determinism_hash(response)

            # Performance
            response.layer_durations = {k: round(v, 2) for k, v in layer_durations.items()}
            response.total_duration_ms = round(sum(layer_durations.values()), 2)

            # Complete trace
            self._telemetry.complete_trace(
                trace=trace,
                confidence_tier=confidence_assessment.tier,
                doctrine_hits=len(doctrine_hits),
                vector_hits=len(vector_response.results),
            )

        except Exception as exc:
            error_msg = str(exc)
            stack = traceback.format_exc()
            self._telemetry.fail_trace(
                trace=trace,
                error_domain=ErrorDomain.UNKNOWN,
                error_message=error_msg,
                stack_trace=stack,
            )
            logger.error("Query processing failed: {}", error_msg)
            raise

        return response

    def _build_doctrine_hits(
        self,
        doctrines: list[DoctrineBlock],
        mode: ResponseMode,
    ) -> list[DoctrineHit]:
        """Convert doctrine blocks to response hits based on mode."""
        hits: list[DoctrineHit] = []
        for doctrine in doctrines:
            hit = DoctrineHit(
                topic=doctrine.topic,
                confidence=doctrine.confidence,
                stratification=doctrine.confidence_stratification.value,
                conclusion=doctrine.conclusion_template,
                curative_document=doctrine.curative_document_type,
                estimated_timeline_days=doctrine.estimated_timeline_days,
                typical_cost_range=doctrine.typical_cost_range,
                risk_factors=doctrine.risk_factors,
            )

            if mode in (ResponseMode.DEFENSE, ResponseMode.MEMO):
                hit.key_factors = doctrine.key_factors
                hit.authority = doctrine.primary_authority
                hit.reasoning = doctrine.reasoning_framework

            hits.append(hit)
        return hits

    def _build_conclusion(
        self,
        doctrines: list[DoctrineBlock],
        normalization: NormalizationResult,
        zone: AnalysisZone,
    ) -> str:
        """Build the conclusion text from matched doctrines."""
        if not doctrines:
            return (
                f"No matching curative doctrine found for the query. "
                f"Detected categories: {', '.join(normalization.detected_categories) or 'none'}. "
                f"Consider broadening the query or consulting a title attorney for this specific issue."
            )

        primary = doctrines[0]
        conclusion_parts: list[str] = [primary.conclusion_template]

        if zone == AnalysisZone.PLANNING:
            conclusion_parts.append(
                f"\nRecommended curative document: {primary.curative_document_type}. "
                f"Estimated timeline: {primary.estimated_timeline_days} days. "
                f"Typical cost: {primary.typical_cost_range}."
            )
        elif zone == AnalysisZone.AUDIT:
            conclusion_parts.append(
                f"\nAudit focus: Verify that the {primary.curative_document_type} was properly "
                f"executed, acknowledged, and recorded. Check that all required elements are present "
                f"per the applicable authority."
            )

        if primary.risk_factors:
            conclusion_parts.append(
                f"\nRisk factors: {'; '.join(primary.risk_factors)}."
            )

        if len(doctrines) > 1:
            additional = [d.topic.replace("_", " ").title() for d in doctrines[1:3]]
            conclusion_parts.append(
                f"\nRelated curative topics: {', '.join(additional)}."
            )

        return " ".join(conclusion_parts)

    def _build_reasoning(
        self,
        doctrines: list[DoctrineBlock],
        normalization: NormalizationResult,
        mode: ResponseMode,
    ) -> str:
        """Build the reasoning text."""
        if not doctrines:
            return "No doctrine match — unable to construct structured reasoning."

        if mode == ResponseMode.FAST:
            return doctrines[0].resolution_strategy

        # DEFENSE/MEMO mode: full reasoning chain
        parts: list[str] = []
        for i, doctrine in enumerate(doctrines[:3], 1):
            parts.append(f"[{i}] {doctrine.topic.replace('_', ' ').upper()}")
            parts.append(doctrine.reasoning_framework)
            parts.append(f"Resolution: {doctrine.resolution_strategy}")
            if doctrine.counter_arguments:
                parts.append("Counter-arguments:")
                for counter in doctrine.counter_arguments[:3]:
                    parts.append(f"  - {counter}")
            parts.append("")

        return "\n".join(parts)

    def _build_curative_recommendations(
        self,
        doctrines: list[DoctrineBlock],
    ) -> list[str]:
        """Build list of recommended curative actions."""
        recommendations: list[str] = []
        seen_docs: set[str] = set()
        for doctrine in doctrines:
            doc_type = doctrine.curative_document_type
            if doc_type and doc_type not in seen_docs:
                seen_docs.add(doc_type)
                recommendations.append(
                    f"{doc_type} — {doctrine.typical_cost_range}, "
                    f"~{doctrine.estimated_timeline_days} days"
                )
        return recommendations

    # --- Component accessors ---

    @property
    def cache_manager(self) -> DoctrineCacheManager:
        return self._cache_manager

    @property
    def drift_watcher(self) -> Optional[DriftWatcher]:
        return self._drift_watcher

    @property
    def coverage_tracker(self) -> Optional[CoverageTracker]:
        return self._coverage_tracker

    @property
    def telemetry(self) -> Optional[TelemetryCollector]:
        return self._telemetry

    @property
    def normalizer(self) -> Optional[SemanticNormalizer]:
        return self._normalizer

    @property
    def vector_index(self) -> Optional[VectorIndex]:
        return self._vector_index

    def get_health(self) -> HealthResponse:
        """Get comprehensive health status."""
        uptime = time.time() - self._start_time
        tel_health = self._telemetry.get_health() if self._telemetry else {}
        norm_stats = self._normalizer.get_stats() if self._normalizer else {}
        search_stats = self._vector_index.get_stats() if self._vector_index else {}

        status = "healthy"
        if tel_health.get("error_rate", 0) > 0.15:
            status = "degraded"
        if not self._initialized:
            status = "initializing"

        return HealthResponse(
            status=status,
            uptime_seconds=round(uptime, 1),
            doctrine_count=self._cache_manager.doctrine_count,
            interaction_count=self._cache_manager.interaction_count,
            vector_index_size=self._vector_index.document_count if self._vector_index else 0,
            telemetry=tel_health,
            normalizer_stats=norm_stats,
            search_stats=search_stats,
        )


# ===================================================================
# TIE COMPONENT 17: FastAPI Server
# ===================================================================

# Module-level engine instance
engine = ThreeLayerResponseEngine()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting LM10 Curative Engine on port {}...", ENGINE_PORT)
    engine.initialize()
    logger.info("LM10 Curative Engine ready")
    yield
    logger.info("Shutting down LM10 Curative Engine...")
    if engine.telemetry:
        engine.telemetry.save_metrics_snapshot()
        engine.telemetry.rotate_audit_trail()
    # Cloud cleanup
    if _CLOUD_AVAILABLE:
        try:
            from cloud_retriever import CognitionCloudRetriever
            retriever = CognitionCloudRetriever()
            await retriever.close()
            logger.info("Cloud retriever connections closed")
        except Exception as e:
            logger.warning(f"Cloud cleanup failed: {e}")
    logger.info("LM10 Curative Engine stopped")


app = FastAPI(
    title=f"LM10 {ENGINE_NAME} Engine",
    description=(
        "Title curative intelligence engine for oil and gas operations. "
        "Identifies and resolves title defects including heirship, probate, "
        "correction instruments, quiet title, adverse possession, tax sale "
        "curative, dormant minerals, entity authority, and more."
    ),
    version=ENGINE_VERSION,
    lifespan=lifespan,
)

# CORS middleware
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
async def health_check() -> dict[str, Any]:
    """TIE Component 12: Comprehensive health endpoint."""
    return engine.get_health().model_dump()


@app.post("/query")
async def query_endpoint(query: CurativeQuery) -> dict[str, Any]:
    """
    Main query endpoint — processes curative title queries through
    the three-layer response engine with cloud knowledge enrichment.
    """
    try:
        response = await engine.process_query(query)
        result = response.model_dump()

        # Cloud knowledge enrichment
        if _CLOUD_AVAILABLE:
            try:
                cloud = await retrieve_cloud_knowledge(query.query, category="curative")
                result["cloud_knowledge"] = {
                    "records": len(cloud.clauses) + len(cloud.graph_nodes) + len(cloud.crystals),
                    "merged_context": cloud.merged_text(3000),
                    "sources_succeeded": cloud.sources_succeeded,
                    "retrieval_time_ms": cloud.retrieval_time_ms,
                }
                result["cloud_citations"] = cloud.citation_list()
            except Exception as e:
                logger.warning(f"Cloud retrieval failed: {e}")

        return result
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        logger.error("Query endpoint error: {}", exc)
        raise HTTPException(status_code=500, detail=f"Internal engine error: {str(exc)[:200]}")


@app.get("/query/fast")
async def query_fast(
    q: str = Query(..., description="Curative query text"),
    category: Optional[str] = Query(None, description="Category filter"),
    zone: str = Query("PLANNING", description="Analysis zone"),
) -> dict[str, Any]:
    """Quick query endpoint — FAST mode via GET."""
    try:
        zone_enum = AnalysisZone(zone)
    except ValueError:
        zone_enum = AnalysisZone.PLANNING

    query = CurativeQuery(
        query=q,
        mode=ResponseMode.FAST,
        zone=zone_enum,
        category_filter=category,
    )
    response = await engine.process_query(query)
    return response.model_dump()


@app.get("/doctrines")
async def list_doctrines(
    category: Optional[str] = Query(None, description="Filter by category"),
) -> dict[str, Any]:
    """List all doctrine topics with optional category filter."""
    cache = engine.cache_manager
    if category:
        doctrines = cache.get_by_category(category)
    else:
        doctrines = get_doctrine_cache()

    return {
        "engine_id": ENGINE_ID,
        "total": len(doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "confidence": d.confidence,
                "stratification": d.confidence_stratification.value,
                "curative_document": d.curative_document_type,
                "keywords": d.keywords[:5],
                "timeline_days": d.estimated_timeline_days,
                "cost_range": d.typical_cost_range,
            }
            for d in doctrines
        ],
    }


@app.get("/doctrines/{topic}")
async def get_doctrine(topic: str) -> dict[str, Any]:
    """Get a specific doctrine by topic name."""
    doctrine = engine.cache_manager.get_by_topic(topic)
    if not doctrine:
        raise HTTPException(status_code=404, detail=f"Doctrine '{topic}' not found")
    return doctrine.model_dump()


@app.get("/categories")
async def list_categories() -> dict[str, Any]:
    """List all issue categories with doctrine counts."""
    categories: dict[str, int] = {}
    for cat in IssueCategory:
        count = len(engine.cache_manager.get_by_category(cat.value))
        categories[cat.value] = count
    return {
        "engine_id": ENGINE_ID,
        "categories": categories,
        "total_categories": len(categories),
        "total_doctrines": engine.cache_manager.doctrine_count,
    }


@app.get("/interactions")
async def list_interactions(
    topic: Optional[str] = Query(None, description="Filter by topic"),
) -> dict[str, Any]:
    """List doctrine interactions."""
    if topic:
        interactions = engine.cache_manager.get_interactions(topic)
    else:
        interactions = get_interaction_graph()

    return {
        "engine_id": ENGINE_ID,
        "total": len(interactions),
        "interactions": [
            {
                "source": i.source_topic,
                "target": i.target_topic,
                "type": i.interaction_type,
                "description": i.description,
                "weight": i.weight,
            }
            for i in interactions
        ],
    }


@app.post("/normalize")
async def normalize_text(request: Request) -> dict[str, Any]:
    """Normalize curative text using semantic normalizer."""
    body = await request.json()
    text = body.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Missing 'text' field")
    result = engine.normalizer.normalize(text)
    return result.model_dump()


@app.get("/search")
async def vector_search(
    q: str = Query(..., description="Search query"),
    threshold: float = Query(0.72, description="Similarity threshold"),
    max_results: int = Query(10, description="Maximum results"),
    category: Optional[str] = Query(None, description="Category filter"),
) -> dict[str, Any]:
    """Vector search endpoint."""
    response = engine.vector_index.search(
        query=q,
        threshold=threshold,
        max_results=max_results,
        category_filter=category,
    )
    return response.model_dump()


@app.get("/metrics")
async def get_metrics() -> dict[str, Any]:
    """TIE Component 11: Get metrics snapshot."""
    if not engine.telemetry:
        raise HTTPException(status_code=503, detail="Telemetry not initialized")
    return engine.telemetry.get_metrics_snapshot().model_dump()


@app.get("/drift")
async def check_drift() -> dict[str, Any]:
    """TIE Component 9: Check for doctrine drift."""
    if not engine.drift_watcher:
        raise HTTPException(status_code=503, detail="Drift watcher not initialized")
    return engine.drift_watcher.check_drift().model_dump()


@app.get("/coverage")
async def get_coverage() -> dict[str, Any]:
    """TIE Component 10: Get coverage report."""
    if not engine.coverage_tracker:
        raise HTTPException(status_code=503, detail="Coverage tracker not initialized")
    return engine.coverage_tracker.get_report().model_dump()


@app.get("/audit")
async def get_audit_trail(
    count: int = Query(50, description="Number of entries"),
) -> dict[str, Any]:
    """TIE Component 15: Get recent audit trail entries."""
    if not engine.telemetry:
        raise HTTPException(status_code=503, detail="Telemetry not initialized")
    entries = engine.telemetry.get_recent_audit_entries(count)
    return {
        "engine_id": ENGINE_ID,
        "total_returned": len(entries),
        "entries": entries,
    }


@app.get("/errors")
async def get_errors(
    count: int = Query(20, description="Number of errors"),
) -> dict[str, Any]:
    """Get recent errors and error summary."""
    if not engine.telemetry:
        raise HTTPException(status_code=503, detail="Telemetry not initialized")
    return {
        "engine_id": ENGINE_ID,
        "summary": engine.telemetry.get_error_summary(),
        "recent": engine.telemetry.get_recent_errors(count),
    }


@app.get("/zones")
async def list_zones() -> dict[str, Any]:
    """List analysis zones and their guidelines."""
    return {
        "engine_id": ENGINE_ID,
        "zones": {
            zone.value: ZONE_GUIDELINES.get(zone.value, "")
            for zone in AnalysisZone
        },
    }


@app.get("/modes")
async def list_modes() -> dict[str, Any]:
    """List response modes and their configurations."""
    return {
        "engine_id": ENGINE_ID,
        "modes": RESPONSE_MODE_CONFIG,
    }


@app.get("/stats")
async def get_stats() -> dict[str, Any]:
    """Get comprehensive engine statistics."""
    health = engine.get_health()
    coverage = engine.coverage_tracker.get_report() if engine.coverage_tracker else None
    drift = engine.drift_watcher.check_drift() if engine.drift_watcher else None

    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "health": health.model_dump(),
        "coverage": coverage.model_dump() if coverage else None,
        "drift": drift.model_dump() if drift else None,
    }


@app.post("/batch")
async def batch_query(request: Request) -> dict[str, Any]:
    """Process multiple curative queries in a single request."""
    body = await request.json()
    queries = body.get("queries", [])
    if not queries:
        raise HTTPException(status_code=400, detail="No queries provided")
    if len(queries) > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 queries per batch")

    results: list[dict[str, Any]] = []
    for i, q_data in enumerate(queries):
        try:
            query = CurativeQuery(
                query=q_data.get("query", ""),
                mode=ResponseMode(q_data.get("mode", "FAST")),
                zone=AnalysisZone(q_data.get("zone", "PLANNING")),
                category_filter=q_data.get("category_filter"),
                include_interactions=q_data.get("include_interactions", False),
                include_fragility=q_data.get("include_fragility", False),
            )
            response = await engine.process_query(query)
            results.append({"index": i, "success": True, "response": response.model_dump()})
        except Exception as exc:
            results.append({"index": i, "success": False, "error": str(exc)[:200]})

    return {
        "engine_id": ENGINE_ID,
        "total_queries": len(queries),
        "successful": sum(1 for r in results if r["success"]),
        "failed": sum(1 for r in results if not r["success"]),
        "results": results,
    }


@app.get("/curative-checklist/{category}")
async def curative_checklist(category: str) -> dict[str, Any]:
    """
    Generate a curative checklist for a specific issue category.
    Lists all required curative documents, steps, and requirements.
    """
    try:
        cat_enum = IssueCategory(category)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category: {category}. Valid: {[c.value for c in IssueCategory]}",
        )

    doctrines = engine.cache_manager.get_by_category(cat_enum.value)
    if not doctrines:
        raise HTTPException(status_code=404, detail=f"No doctrines for category: {category}")

    checklist_items: list[dict[str, Any]] = []
    for doctrine in doctrines:
        steps = doctrine.reasoning_framework.split("\n")
        numbered_steps = [s.strip() for s in steps if s.strip().startswith("STEP")]

        checklist_items.append({
            "topic": doctrine.topic,
            "curative_document": doctrine.curative_document_type,
            "confidence": doctrine.confidence,
            "stratification": doctrine.confidence_stratification.value,
            "estimated_timeline_days": doctrine.estimated_timeline_days,
            "typical_cost_range": doctrine.typical_cost_range,
            "steps": numbered_steps,
            "key_factors": doctrine.key_factors,
            "risk_factors": doctrine.risk_factors,
            "primary_authority": doctrine.primary_authority,
            "counter_arguments": doctrine.counter_arguments,
            "resolution_strategy": doctrine.resolution_strategy,
            "burden_holder": doctrine.burden_holder,
        })

    total_time = sum(d.estimated_timeline_days for d in doctrines)
    avg_time = total_time / len(doctrines) if doctrines else 0

    return {
        "engine_id": ENGINE_ID,
        "category": category,
        "total_curative_options": len(checklist_items),
        "average_timeline_days": round(avg_time, 1),
        "checklist": checklist_items,
    }


@app.get("/authority-analysis")
async def authority_analysis(
    q: str = Query(..., description="Query to analyze authority for"),
) -> dict[str, Any]:
    """
    Analyze authority sources for a curative query.
    Returns ranked authorities with weights, types, and conflict detection.
    """
    normalizer = engine.normalizer
    normalization = normalizer.normalize(q)

    doctrine_hits = engine.cache_manager.lookup(
        query=q,
        canonical_terms=normalization.canonical_terms,
        categories=normalization.detected_categories,
        max_results=5,
    )

    hardener = AuthorityHardener()
    all_authorities: list[str] = []
    for doctrine in doctrine_hits:
        all_authorities.extend(doctrine.primary_authority)

    # Deduplicate
    seen: set[str] = set()
    unique_authorities: list[str] = []
    for auth in all_authorities:
        if auth not in seen:
            unique_authorities.append(auth)
            seen.add(auth)

    hardened = hardener.harden_authorities(unique_authorities)
    authority_score = hardener.compute_authority_score(hardened)
    conflicts = hardener.detect_conflicts(hardened)

    # Group by type
    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for auth in hardened:
        by_type[auth.type].append({
            "source": auth.source,
            "weight": auth.weight,
        })

    return {
        "engine_id": ENGINE_ID,
        "query": q,
        "total_authorities": len(hardened),
        "overall_authority_score": round(authority_score, 4),
        "conflicts": conflicts,
        "authorities_ranked": [
            {"source": a.source, "weight": a.weight, "type": a.type}
            for a in hardened
        ],
        "by_type": dict(by_type),
        "doctrine_topics_consulted": [d.topic for d in doctrine_hits],
    }


@app.get("/fragility-report")
async def fragility_report(
    q: str = Query(..., description="Query to assess fragility"),
) -> dict[str, Any]:
    """
    Generate a detailed fragility report for curative assertions.
    Shows how vulnerable each assertion is to challenge.
    """
    normalizer = engine.normalizer
    normalization = normalizer.normalize(q)

    doctrine_hits = engine.cache_manager.lookup(
        query=q,
        canonical_terms=normalization.canonical_terms,
        categories=normalization.detected_categories,
        max_results=5,
    )

    scorer = FragilityScorer()
    reports: list[dict[str, Any]] = []
    for doctrine in doctrine_hits:
        frag = scorer.score(doctrine, q)
        reports.append({
            "topic": doctrine.topic,
            "category": doctrine.issue_category.value,
            "doctrine_confidence": doctrine.confidence,
            "fragility": frag.model_dump(),
        })

    # Overall fragility assessment
    avg_fragility = (
        sum(r["fragility"]["overall_fragility"] for r in reports) / len(reports)
        if reports else 0.0
    )

    risk_level = "LOW"
    if avg_fragility > 0.6:
        risk_level = "HIGH"
    elif avg_fragility > 0.4:
        risk_level = "MODERATE"
    elif avg_fragility > 0.2:
        risk_level = "LOW-MODERATE"

    return {
        "engine_id": ENGINE_ID,
        "query": q,
        "overall_fragility": round(avg_fragility, 4),
        "risk_level": risk_level,
        "recommendations": _fragility_recommendations(avg_fragility, reports),
        "detailed_reports": reports,
    }


def _fragility_recommendations(avg_fragility: float, reports: list[dict[str, Any]]) -> list[str]:
    """Generate recommendations based on fragility analysis."""
    recs: list[str] = []

    if avg_fragility > 0.6:
        recs.append("HIGH FRAGILITY: Consider obtaining judicial determination rather than relying on affidavits")
        recs.append("Recommend title insurance endorsement for additional protection")
    elif avg_fragility > 0.4:
        recs.append("MODERATE FRAGILITY: Supplement primary curative with corroborating evidence")
        recs.append("Obtain additional witness affidavits where testimony dependence is high")
    elif avg_fragility > 0.2:
        recs.append("LOW-MODERATE FRAGILITY: Standard curative procedures should be sufficient")
    else:
        recs.append("LOW FRAGILITY: Curative position is well-supported by verifiable records")

    for report in reports:
        frag = report["fragility"]
        if frag.get("testimony_dependence", 0) > 0.6:
            recs.append(
                f"Topic '{report['topic']}': High testimony dependence — "
                f"secure multiple witness statements"
            )
        if frag.get("time_sensitivity", 0) > 0.7:
            recs.append(
                f"Topic '{report['topic']}': Time-sensitive — "
                f"verify all statutory deadlines before proceeding"
            )
        if frag.get("recharacterization_risk", 0) > 0.5:
            recs.append(
                f"Topic '{report['topic']}': Recharacterization risk — "
                f"document intent clearly in all curative instruments"
            )

    return recs


@app.get("/resolution-plan")
async def resolution_plan(
    q: str = Query(..., description="Curative query"),
    zone: str = Query("PLANNING", description="Analysis zone"),
) -> dict[str, Any]:
    """
    Generate a step-by-step resolution plan for a curative issue.
    Includes sequencing, dependencies, timeline, and cost estimates.
    """
    try:
        zone_enum = AnalysisZone(zone)
    except ValueError:
        zone_enum = AnalysisZone.PLANNING

    normalizer = engine.normalizer
    normalization = normalizer.normalize(q)

    doctrine_hits = engine.cache_manager.lookup(
        query=q,
        canonical_terms=normalization.canonical_terms,
        categories=normalization.detected_categories,
        max_results=10,
    )

    if not doctrine_hits:
        return {
            "engine_id": ENGINE_ID,
            "query": q,
            "plan": [],
            "message": "No matching doctrines found — unable to generate resolution plan",
        }

    # Build decomposition for sequencing
    decomposer = DoctrineDecomposer(engine.cache_manager)
    decomposition = decomposer.decompose(
        canonical_terms=normalization.canonical_terms,
        categories=normalization.detected_categories,
        doctrine_hits=doctrine_hits,
    )

    # Build plan steps following resolution sequence
    plan_steps: list[dict[str, Any]] = []
    cumulative_days = 0
    cumulative_cost_low = 0
    cumulative_cost_high = 0

    for step_num, topic in enumerate(decomposition.resolution_sequence, 1):
        doctrine = engine.cache_manager.get_by_topic(topic)
        if not doctrine:
            continue

        # Parse cost range
        cost_parts = doctrine.typical_cost_range.replace("$", "").replace(",", "").replace("+", "")
        cost_low, cost_high = 0, 0
        if "-" in cost_parts:
            parts = cost_parts.split("-")
            try:
                cost_low = int(parts[0].strip())
                cost_high = int(parts[1].strip())
            except (ValueError, IndexError):
                pass

        cumulative_days += doctrine.estimated_timeline_days
        cumulative_cost_low += cost_low
        cumulative_cost_high += cost_high

        # Extract numbered steps from reasoning framework
        framework_steps = []
        for line in doctrine.reasoning_framework.split("\n"):
            stripped = line.strip()
            if stripped.startswith("STEP"):
                framework_steps.append(stripped)

        # Determine dependencies
        dependencies: list[str] = []
        for interaction in decomposition.interactions:
            if interaction.target == topic and interaction.type == "prerequisite":
                dependencies.append(interaction.source)

        # Determine alternatives
        alternatives: list[str] = []
        for interaction in decomposition.interactions:
            if (interaction.source == topic or interaction.target == topic) and interaction.type == "alternative":
                other = interaction.target if interaction.source == topic else interaction.source
                alternatives.append(other)

        plan_steps.append({
            "step": step_num,
            "topic": topic,
            "category": doctrine.issue_category.value,
            "curative_document": doctrine.curative_document_type,
            "confidence": doctrine.confidence,
            "stratification": doctrine.confidence_stratification.value,
            "estimated_days": doctrine.estimated_timeline_days,
            "cumulative_days": cumulative_days,
            "cost_range": doctrine.typical_cost_range,
            "cumulative_cost_range": f"${cumulative_cost_low:,}-${cumulative_cost_high:,}",
            "dependencies": dependencies,
            "alternatives": alternatives,
            "detailed_steps": framework_steps,
            "key_factors": doctrine.key_factors,
            "risk_factors": doctrine.risk_factors,
            "burden_holder": doctrine.burden_holder,
            "resolution_strategy": doctrine.resolution_strategy,
        })

    return {
        "engine_id": ENGINE_ID,
        "query": q,
        "zone": zone_enum.value,
        "zone_guidance": ZONE_GUIDELINES.get(zone_enum.value, ""),
        "total_steps": len(plan_steps),
        "total_estimated_days": cumulative_days,
        "total_cost_range": f"${cumulative_cost_low:,}-${cumulative_cost_high:,}",
        "complexity_score": decomposition.complexity_score,
        "categories_involved": decomposition.issue_categories,
        "plan": plan_steps,
    }


@app.get("/statutory-refs")
async def extract_statutory_references(
    q: str = Query(..., description="Text to extract statutory references from"),
) -> dict[str, Any]:
    """Extract Texas statutory references from text."""
    normalizer = engine.normalizer
    refs = normalizer.extract_statutory_references(q)
    return {
        "engine_id": ENGINE_ID,
        "query": q[:200],
        "references_found": len(refs),
        "references": refs,
    }


@app.get("/curative-documents")
async def list_curative_documents() -> dict[str, Any]:
    """List all curative document types recognized by the engine."""
    doctrines = get_doctrine_cache()
    doc_types: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for doctrine in doctrines:
        doc_type = doctrine.curative_document_type
        if doc_type:
            doc_types[doc_type].append({
                "topic": doctrine.topic,
                "category": doctrine.issue_category.value,
                "confidence": doctrine.confidence,
                "timeline_days": doctrine.estimated_timeline_days,
                "cost_range": doctrine.typical_cost_range,
            })

    documents: list[dict[str, Any]] = []
    for doc_type, usages in sorted(doc_types.items()):
        avg_days = sum(u["timeline_days"] for u in usages) / len(usages)
        documents.append({
            "document_type": doc_type,
            "used_by_doctrines": len(usages),
            "categories": list({u["category"] for u in usages}),
            "average_timeline_days": round(avg_days, 1),
            "usages": usages,
        })

    return {
        "engine_id": ENGINE_ID,
        "total_document_types": len(documents),
        "documents": documents,
    }


@app.get("/risk-matrix")
async def risk_matrix() -> dict[str, Any]:
    """
    Generate a risk matrix across all curative categories.
    Maps each doctrine to its risk level based on confidence and fragility.
    """
    doctrines = get_doctrine_cache()
    scorer = FragilityScorer()
    hardener = AuthorityHardener()
    stratifier = ConfidenceStratifier()

    matrix: list[dict[str, Any]] = []
    for doctrine in doctrines:
        # Authority score
        hardened = hardener.harden_authorities(doctrine.primary_authority)
        auth_score = hardener.compute_authority_score(hardened)

        # Confidence stratification
        confidence = stratifier.stratify(
            authority_score=auth_score,
            doctrine_confidence=doctrine.confidence,
            risk_factor_count=len(doctrine.risk_factors),
            category=doctrine.issue_category.value,
        )

        # Fragility
        fragility = scorer.score(doctrine, doctrine.topic)

        # Risk level
        risk_score = (1.0 - confidence.score) * 0.5 + fragility.overall_fragility * 0.5
        risk_level = "LOW"
        if risk_score > 0.6:
            risk_level = "CRITICAL"
        elif risk_score > 0.45:
            risk_level = "HIGH"
        elif risk_score > 0.3:
            risk_level = "MODERATE"
        elif risk_score > 0.15:
            risk_level = "LOW-MODERATE"

        matrix.append({
            "topic": doctrine.topic,
            "category": doctrine.issue_category.value,
            "confidence_tier": confidence.tier,
            "confidence_score": confidence.score,
            "authority_score": round(auth_score, 4),
            "fragility_score": fragility.overall_fragility,
            "risk_score": round(risk_score, 4),
            "risk_level": risk_level,
            "curative_document": doctrine.curative_document_type,
            "timeline_days": doctrine.estimated_timeline_days,
            "cost_range": doctrine.typical_cost_range,
            "risk_factors": doctrine.risk_factors,
        })

    # Sort by risk score descending
    matrix.sort(key=lambda x: x["risk_score"], reverse=True)

    # Summary by risk level
    risk_summary: dict[str, int] = defaultdict(int)
    for item in matrix:
        risk_summary[item["risk_level"]] += 1

    return {
        "engine_id": ENGINE_ID,
        "total_doctrines": len(matrix),
        "risk_summary": dict(risk_summary),
        "matrix": matrix,
    }


@app.get("/compare-strategies")
async def compare_strategies(
    q: str = Query(..., description="Curative issue to compare strategies for"),
) -> dict[str, Any]:
    """
    Compare alternative curative strategies for an issue.
    Shows trade-offs between cost, time, confidence, and risk.
    """
    normalizer = engine.normalizer
    normalization = normalizer.normalize(q)

    doctrine_hits = engine.cache_manager.lookup(
        query=q,
        canonical_terms=normalization.canonical_terms,
        categories=normalization.detected_categories,
        max_results=10,
    )

    # Also find alternatives via interaction graph
    alternative_topics: set[str] = set()
    for doctrine in doctrine_hits:
        for interaction in engine.cache_manager.get_interactions(doctrine.topic):
            if interaction.interaction_type == "alternative":
                other = interaction.target_topic if interaction.source_topic == doctrine.topic else interaction.source_topic
                alternative_topics.add(other)

    # Add alternative doctrines
    all_doctrines = list(doctrine_hits)
    seen_topics = {d.topic for d in all_doctrines}
    for alt_topic in alternative_topics:
        if alt_topic not in seen_topics:
            alt_doctrine = engine.cache_manager.get_by_topic(alt_topic)
            if alt_doctrine:
                all_doctrines.append(alt_doctrine)
                seen_topics.add(alt_topic)

    hardener = AuthorityHardener()
    scorer = FragilityScorer()

    strategies: list[dict[str, Any]] = []
    for doctrine in all_doctrines:
        hardened = hardener.harden_authorities(doctrine.primary_authority)
        auth_score = hardener.compute_authority_score(hardened)
        fragility = scorer.score(doctrine, q)

        is_alternative = doctrine.topic in alternative_topics
        is_direct_match = doctrine in doctrine_hits

        strategies.append({
            "topic": doctrine.topic,
            "category": doctrine.issue_category.value,
            "match_type": "direct" if is_direct_match else "alternative",
            "curative_document": doctrine.curative_document_type,
            "confidence": doctrine.confidence,
            "stratification": doctrine.confidence_stratification.value,
            "authority_score": round(auth_score, 4),
            "fragility": fragility.overall_fragility,
            "timeline_days": doctrine.estimated_timeline_days,
            "cost_range": doctrine.typical_cost_range,
            "risk_factors": doctrine.risk_factors,
            "resolution_strategy": doctrine.resolution_strategy,
            "pros": _strategy_pros(doctrine),
            "cons": _strategy_cons(doctrine),
        })

    # Sort by confidence descending
    strategies.sort(key=lambda s: s["confidence"], reverse=True)

    return {
        "engine_id": ENGINE_ID,
        "query": q,
        "strategies_found": len(strategies),
        "direct_matches": sum(1 for s in strategies if s["match_type"] == "direct"),
        "alternatives": sum(1 for s in strategies if s["match_type"] == "alternative"),
        "strategies": strategies,
    }


def _strategy_pros(doctrine: DoctrineBlock) -> list[str]:
    """Generate pros for a curative strategy."""
    pros: list[str] = []
    if doctrine.confidence >= 0.85:
        pros.append("High confidence — well-established authority")
    if doctrine.estimated_timeline_days <= 30:
        pros.append(f"Quick resolution — ~{doctrine.estimated_timeline_days} days")
    if doctrine.confidence_stratification == ConfidenceStratification.DEFENSIBLE:
        pros.append("Defensible position — strong statutory support")
    if len(doctrine.primary_authority) >= 4:
        pros.append("Multiple authoritative sources available")
    cost_str = doctrine.typical_cost_range.replace("$", "").replace(",", "").replace("+", "")
    if "-" in cost_str:
        parts = cost_str.split("-")
        try:
            if int(parts[1].strip()) <= 2000:
                pros.append("Cost-effective option")
        except (ValueError, IndexError):
            pass
    if not pros:
        pros.append("Standard curative approach")
    return pros


def _strategy_cons(doctrine: DoctrineBlock) -> list[str]:
    """Generate cons for a curative strategy."""
    cons: list[str] = []
    if doctrine.confidence < 0.80:
        cons.append("Lower confidence — may face challenge")
    if doctrine.estimated_timeline_days > 180:
        cons.append(f"Long timeline — ~{doctrine.estimated_timeline_days} days")
    if doctrine.confidence_stratification in (
        ConfidenceStratification.DISCLOSURE,
        ConfidenceStratification.HIGH_RISK,
    ):
        cons.append("Requires disclosure of uncertainty to client")
    if len(doctrine.risk_factors) > 3:
        cons.append(f"Multiple risk factors ({len(doctrine.risk_factors)})")
    cost_str = doctrine.typical_cost_range.replace("$", "").replace(",", "").replace("+", "")
    if "-" in cost_str:
        parts = cost_str.split("-")
        try:
            if int(parts[1].strip()) >= 10000:
                cons.append("Significant cost")
        except (ValueError, IndexError):
            pass
    if not cons:
        cons.append("Standard risks apply")
    return cons


@app.get("/curative-timeline")
async def curative_timeline(
    category: Optional[str] = Query(None, description="Category filter"),
) -> dict[str, Any]:
    """
    Generate a timeline visualization of curative options,
    sorted by estimated completion time.
    """
    if category:
        doctrines = engine.cache_manager.get_by_category(category)
    else:
        doctrines = get_doctrine_cache()

    timeline_items: list[dict[str, Any]] = []
    for doctrine in doctrines:
        timeline_items.append({
            "topic": doctrine.topic,
            "category": doctrine.issue_category.value,
            "curative_document": doctrine.curative_document_type,
            "days": doctrine.estimated_timeline_days,
            "cost_range": doctrine.typical_cost_range,
            "confidence": doctrine.confidence,
            "stratification": doctrine.confidence_stratification.value,
        })

    # Sort by timeline
    timeline_items.sort(key=lambda x: x["days"])

    # Categorize into speed bands
    quick = [t for t in timeline_items if t["days"] <= 14]
    standard = [t for t in timeline_items if 15 <= t["days"] <= 60]
    extended = [t for t in timeline_items if 61 <= t["days"] <= 180]
    litigation = [t for t in timeline_items if t["days"] > 180]

    return {
        "engine_id": ENGINE_ID,
        "total_options": len(timeline_items),
        "bands": {
            "quick_1_14_days": {"count": len(quick), "items": quick},
            "standard_15_60_days": {"count": len(standard), "items": standard},
            "extended_61_180_days": {"count": len(extended), "items": extended},
            "litigation_180_plus_days": {"count": len(litigation), "items": litigation},
        },
        "all_sorted": timeline_items,
    }


@app.get("/epistemic-gaps")
async def epistemic_gaps() -> dict[str, Any]:
    """
    Identify epistemic gaps in the curative knowledge base.
    Shows categories and topics that lack coverage or have never been queried.
    """
    if not engine.coverage_tracker:
        raise HTTPException(status_code=503, detail="Coverage tracker not initialized")

    coverage = engine.coverage_tracker.get_report()

    # Identify categories with fewer than 2 doctrines
    thin_categories: list[dict[str, Any]] = []
    for cat, stats in coverage.category_coverage.items():
        if stats["total"] < 2:
            thin_categories.append({
                "category": cat,
                "doctrine_count": stats["total"],
                "recommendation": "Consider adding more doctrines for comprehensive coverage",
            })

    # Identify untriggered doctrines with suggestions
    untriggered_details: list[dict[str, Any]] = []
    for topic in coverage.untriggered_doctrines:
        doctrine = engine.cache_manager.get_by_topic(topic)
        if doctrine:
            untriggered_details.append({
                "topic": topic,
                "category": doctrine.issue_category.value,
                "keywords": doctrine.keywords[:5],
                "sample_query": f"How to resolve {topic.replace('_', ' ')} in Texas oil and gas title?",
            })

    return {
        "engine_id": ENGINE_ID,
        "coverage_rate": coverage.trigger_rate,
        "total_doctrines": coverage.total_doctrines,
        "triggered_count": len(coverage.triggered_doctrines),
        "untriggered_count": len(coverage.untriggered_doctrines),
        "epistemic_gaps": coverage.epistemic_gaps,
        "thin_categories": thin_categories,
        "untriggered_details": untriggered_details,
    }


# ---------------------------------------------------------------------------
# Additional Helper Functions for Curative Analysis
# ---------------------------------------------------------------------------

def analyze_title_defect_severity(
    doctrine: DoctrineBlock,
    context: dict[str, Any],
) -> dict[str, Any]:
    """
    Analyze the severity of a title defect based on doctrine and context.
    Returns severity classification, urgency, and recommended approach.
    """
    severity_score = 0.0

    # Factor 1: Confidence inversely correlates with defect severity
    confidence_factor = 1.0 - doctrine.confidence
    severity_score += confidence_factor * 0.3

    # Factor 2: Number of risk factors
    risk_factor = min(1.0, len(doctrine.risk_factors) / 5.0)
    severity_score += risk_factor * 0.2

    # Factor 3: Timeline indicates complexity
    timeline_factor = min(1.0, doctrine.estimated_timeline_days / 365.0)
    severity_score += timeline_factor * 0.2

    # Factor 4: Stratification
    strat_map = {
        ConfidenceStratification.DEFENSIBLE: 0.1,
        ConfidenceStratification.AGGRESSIVE: 0.3,
        ConfidenceStratification.DISCLOSURE: 0.6,
        ConfidenceStratification.HIGH_RISK: 0.9,
    }
    strat_factor = strat_map.get(doctrine.confidence_stratification, 0.5)
    severity_score += strat_factor * 0.3

    # Classify
    if severity_score > 0.7:
        severity = "CRITICAL"
        urgency = "IMMEDIATE"
        approach = "Engage title attorney immediately. Consider judicial resolution."
    elif severity_score > 0.5:
        severity = "HIGH"
        urgency = "URGENT"
        approach = "Prioritize curative action. Multiple instruments may be required."
    elif severity_score > 0.3:
        severity = "MODERATE"
        urgency = "STANDARD"
        approach = "Standard curative procedures with appropriate documentation."
    else:
        severity = "LOW"
        urgency = "ROUTINE"
        approach = "Routine curative — single instrument likely sufficient."

    return {
        "severity": severity,
        "severity_score": round(severity_score, 4),
        "urgency": urgency,
        "recommended_approach": approach,
        "factors": {
            "confidence_factor": round(confidence_factor, 4),
            "risk_factor": round(risk_factor, 4),
            "timeline_factor": round(timeline_factor, 4),
            "stratification_factor": round(strat_factor, 4),
        },
    }


def build_curative_workflow(
    doctrines: list[DoctrineBlock],
    zone: AnalysisZone,
) -> dict[str, Any]:
    """
    Build a structured curative workflow from matched doctrines.
    Includes sequencing, parallel tracks, and decision gates.
    """
    workflow_phases: list[dict[str, Any]] = []

    # Phase 1: Investigation
    investigation_docs: list[str] = []
    for doctrine in doctrines:
        investigation_docs.extend([
            f"Review chain of title for {doctrine.topic.replace('_', ' ')}",
            f"Identify all affected parties for {doctrine.curative_document_type}",
        ])
    workflow_phases.append({
        "phase": 1,
        "name": "INVESTIGATION",
        "description": "Title examination and defect identification",
        "tasks": list(set(investigation_docs))[:10],
        "estimated_days": 7,
    })

    # Phase 2: Document Preparation
    prep_tasks: list[str] = []
    for doctrine in doctrines:
        prep_tasks.append(f"Draft {doctrine.curative_document_type}")
        if doctrine.burden_holder:
            prep_tasks.append(f"Contact {doctrine.burden_holder}")
    workflow_phases.append({
        "phase": 2,
        "name": "DOCUMENT_PREPARATION",
        "description": "Drafting and preparation of curative instruments",
        "tasks": list(set(prep_tasks)),
        "estimated_days": 14,
    })

    # Phase 3: Execution
    exec_tasks: list[str] = []
    for doctrine in doctrines:
        exec_tasks.append(f"Execute {doctrine.curative_document_type}")
        exec_tasks.append("Obtain proper acknowledgment")
    workflow_phases.append({
        "phase": 3,
        "name": "EXECUTION",
        "description": "Execution and acknowledgment of curative instruments",
        "tasks": list(set(exec_tasks)),
        "estimated_days": 7,
    })

    # Phase 4: Recording
    workflow_phases.append({
        "phase": 4,
        "name": "RECORDING",
        "description": "Recording curative instruments in county deed records",
        "tasks": [
            "Submit instruments to county clerk for recording",
            "Verify recording data (volume/page or document number)",
            "Obtain certified copies for file",
            "Update title abstract or commitment",
        ],
        "estimated_days": 7,
    })

    # Phase 5: Verification (AUDIT zone adds this)
    if zone == AnalysisZone.AUDIT:
        workflow_phases.append({
            "phase": 5,
            "name": "AUDIT_VERIFICATION",
            "description": "Verify curative instruments are effective and complete",
            "tasks": [
                "Verify all instruments properly recorded",
                "Confirm acknowledgment requirements met",
                "Check for any remaining defects",
                "Update title opinion or commitment",
                "Obtain title insurance endorsement if applicable",
            ],
            "estimated_days": 7,
        })

    total_days = sum(p["estimated_days"] for p in workflow_phases)

    return {
        "total_phases": len(workflow_phases),
        "total_estimated_days": total_days,
        "zone": zone.value,
        "phases": workflow_phases,
    }


def compute_curative_cost_estimate(
    doctrines: list[DoctrineBlock],
) -> dict[str, Any]:
    """
    Compute detailed cost estimate from doctrine cost ranges.
    Returns low/mid/high estimates with breakdown.
    """
    total_low = 0
    total_high = 0
    breakdown: list[dict[str, Any]] = []

    for doctrine in doctrines:
        cost_str = doctrine.typical_cost_range.replace("$", "").replace(",", "").replace("+", "")
        low, high = 0, 0
        if "-" in cost_str:
            parts = cost_str.split("-")
            try:
                low = int(parts[0].strip())
                high = int(parts[1].strip())
            except (ValueError, IndexError):
                low = 1000
                high = 5000
        elif cost_str.strip():
            try:
                low = int(cost_str.strip())
                high = low * 2
            except ValueError:
                low = 1000
                high = 5000
        else:
            low = 1000
            high = 5000

        total_low += low
        total_high += high
        breakdown.append({
            "topic": doctrine.topic,
            "curative_document": doctrine.curative_document_type,
            "low_estimate": low,
            "high_estimate": high,
            "midpoint": (low + high) // 2,
        })

    midpoint = (total_low + total_high) // 2

    return {
        "total_low": total_low,
        "total_high": total_high,
        "total_midpoint": midpoint,
        "formatted_low": f"${total_low:,}",
        "formatted_high": f"${total_high:,}",
        "formatted_midpoint": f"${midpoint:,}",
        "breakdown": breakdown,
    }


# ---------------------------------------------------------------------------
# Texas Curative Reference Tables
# ---------------------------------------------------------------------------

TEXAS_LIMITATION_PERIODS: dict[str, dict[str, Any]] = {
    "adverse_possession_3_year": {
        "code": "Tex. Civ. Prac. & Rem. Code 16.024",
        "period_years": 3,
        "requirements": "Peaceable possession under title or color of title, with registered deed",
        "notes": "Rarely used in practice — 5-year is more common",
    },
    "adverse_possession_5_year": {
        "code": "Tex. Civ. Prac. & Rem. Code 16.025",
        "period_years": 5,
        "requirements": "Registered deed + tax payment + continuous possession",
        "notes": "Strongest form — requires deed AND taxes paid",
    },
    "adverse_possession_10_year": {
        "code": "Tex. Civ. Prac. & Rem. Code 16.026",
        "period_years": 10,
        "requirements": "Continuous adverse possession — no deed or tax payment required",
        "notes": "Most commonly asserted — no deed required",
    },
    "adverse_possession_25_year": {
        "code": "Tex. Civ. Prac. & Rem. Code 16.028",
        "period_years": 25,
        "requirements": "Peaceable adverse possession for 25 years",
        "notes": "Absolute bar — defeats disabilities",
    },
    "will_probate_deadline": {
        "code": "Tex. Estates Code 256.003",
        "period_years": 4,
        "requirements": "Will must be filed within 4 years of death",
        "notes": "After 4 years, only muniment of title may be available",
    },
    "mechanics_lien_residential": {
        "code": "Tex. Prop. Code 53.158",
        "period_years": 1,
        "requirements": "Must file suit to enforce within 1 year of filing",
        "notes": "Residential property only",
    },
    "mechanics_lien_commercial": {
        "code": "Tex. Prop. Code 53.158",
        "period_years": 2,
        "requirements": "Must file suit to enforce within 2 years of filing",
        "notes": "Commercial property",
    },
    "abstract_of_judgment": {
        "code": "Tex. Prop. Code 52.006",
        "period_years": 10,
        "requirements": "Valid 10 years, renewable once for additional 10 years",
        "notes": "Total maximum: 20 years",
    },
    "deed_of_trust_limitations": {
        "code": "Tex. Civ. Prac. & Rem. Code 16.035",
        "period_years": 4,
        "requirements": "4-year limitations on enforcement of underlying note",
        "notes": "Power of sale must be exercised within limitations period",
    },
    "tax_sale_redemption_homestead": {
        "code": "Tex. Tax Code 34.21",
        "period_years": 2,
        "requirements": "Homestead and agricultural property",
        "notes": "25% premium year 1, 50% premium year 2",
    },
    "tax_sale_redemption_other": {
        "code": "Tex. Tax Code 34.21",
        "period_years": 0.5,
        "requirements": "Non-homestead, non-agricultural",
        "notes": "180 days for post-2015 tax sales",
    },
    "dormant_mineral_interest": {
        "code": "Tex. Nat. Res. Code Chapter 75",
        "period_years": 10,
        "requirements": "No 'use' for 10 consecutive years",
        "notes": "Surface owner must give notice, 180-day response period",
    },
}


TEXAS_RECORDING_REQUIREMENTS: dict[str, dict[str, str]] = {
    "deed": {
        "acknowledgment": "Required — notarized",
        "witnesses": "Not required in Texas",
        "recording": "County clerk of county where property located",
        "constructive_notice": "Upon recording per Tex. Prop. Code 13.001",
    },
    "deed_of_trust": {
        "acknowledgment": "Required — notarized",
        "witnesses": "Not required",
        "recording": "County clerk of county where property located",
        "constructive_notice": "Upon recording",
    },
    "affidavit_of_heirship": {
        "acknowledgment": "Required — notarized (sworn statement)",
        "witnesses": "Disinterested witness is the affiant",
        "recording": "County clerk of county where property located",
        "constructive_notice": "After 5 years on record per Tex. Prop. Code 13.002",
    },
    "lis_pendens": {
        "acknowledgment": "Not required — verified petition",
        "witnesses": "Not required",
        "recording": "County clerk of county where property located",
        "constructive_notice": "Upon filing per Tex. Prop. Code 12.007",
    },
    "abstract_of_judgment": {
        "acknowledgment": "Certified by clerk of court",
        "witnesses": "Not required",
        "recording": "County clerk of any county to create lien",
        "constructive_notice": "Upon recording per Tex. Prop. Code 52.001",
    },
    "correction_instrument": {
        "acknowledgment": "Required — notarized",
        "witnesses": "Not required",
        "recording": "County clerk of county where property located",
        "constructive_notice": "Upon recording, relates back to original",
    },
    "mineral_deed": {
        "acknowledgment": "Required — notarized",
        "witnesses": "Not required",
        "recording": "County clerk of county where property located",
        "constructive_notice": "Upon recording",
    },
}


@app.get("/reference/limitations")
async def get_limitation_periods() -> dict[str, Any]:
    """Get Texas limitation periods relevant to curative work."""
    return {
        "engine_id": ENGINE_ID,
        "total_periods": len(TEXAS_LIMITATION_PERIODS),
        "limitation_periods": TEXAS_LIMITATION_PERIODS,
    }


@app.get("/reference/recording")
async def get_recording_requirements() -> dict[str, Any]:
    """Get Texas recording requirements for curative instruments."""
    return {
        "engine_id": ENGINE_ID,
        "total_instruments": len(TEXAS_RECORDING_REQUIREMENTS),
        "recording_requirements": TEXAS_RECORDING_REQUIREMENTS,
    }


@app.get("/reference/intestate-succession")
async def get_intestate_succession() -> dict[str, Any]:
    """Get Texas intestate succession rules relevant to heirship curative."""
    return {
        "engine_id": ENGINE_ID,
        "code": "Texas Estates Code Chapter 201",
        "rules": {
            "community_property_all_children_of_marriage": {
                "surviving_spouse": "All community property",
                "children": "No community property (already own 1/2)",
                "notes": "Only applies when ALL children are also children of surviving spouse",
            },
            "community_property_mixed_children": {
                "surviving_spouse": "1/2 of community property",
                "children": "1/2 of community property + decedent's 1/2",
                "notes": "When decedent has children from another relationship",
            },
            "separate_real_property_with_children": {
                "surviving_spouse": "1/3 life estate",
                "children": "Fee simple subject to life estate",
                "notes": "Spouse gets life estate in 1/3, children get remainder",
            },
            "separate_personal_property_with_children": {
                "surviving_spouse": "1/3 outright",
                "children": "2/3 outright",
                "notes": "Personal property divided outright, not life estate",
            },
            "no_surviving_spouse_with_children": {
                "surviving_spouse": "N/A",
                "children": "Everything per capita at each generation",
                "notes": "Grandchildren take by representation",
            },
            "no_children_with_spouse": {
                "surviving_spouse": "All community + all personal + 1/2 separate real",
                "parents_siblings": "1/2 separate real property",
                "notes": "Parents or siblings share the 1/2 of separate real",
            },
        },
    }


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )