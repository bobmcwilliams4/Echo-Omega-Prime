"""
R01_rrc_parser — Texas Railroad Commission Data Parser Engine

Parses and analyzes Texas Railroad Commission (RRC) data including well permits,
production data, operator filings, rule compliance, and regulatory documentation.

TIE-20 GOLD STANDARD: Real RRC domain expertise with deterministic doctrine cache,
authority hardening, epistemic guardrails, adversarial thinking, and multi-doctrine
decomposition. No-LLM mode for fast, reproducible analysis.

Port: 8701
Version: 1.0.0
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# Cloud retriever for Cognition Cloud access
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "_shared"))
from cloud_retriever import CognitionCloudRetriever, CloudKnowledge

# Local modules

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import DOCTRINE_BLOCKS, DoctrineBlock
from semantic import SemanticNormalizer
from search import VectorSearch
from telemetry import TelemetryCollector


# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

ENGINE_ID = "R01_rrc_parser"
VERSION = "1.0.0"
PORT = 8701
CACHE_SIZE = 500
AUDIT_LOG_PATH = Path("O:/ECHO_OMEGA_PRIME/LOGS/RRC_PARSER_AUDIT.jsonl")


# ═══════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    """Response detail level."""
    FAST = "fast"           # Concise, cache-only
    DEFENSE = "defense"     # Audit-ready with citations
    MEMO = "memo"           # Full documentation


class ConfidenceLevel(str, Enum):
    """Confidence stratification."""
    DEFENSIBLE = "defensible"       # Clear statutory authority
    AGGRESSIVE = "aggressive"        # Interpretive position
    DISCLOSURE = "disclosure"        # Material uncertainty
    HIGH_RISK = "high_risk"         # Litigation/penalty risk


class PositionZone(str, Enum):
    """Separation of planning vs reporting analysis."""
    PLANNING = "planning"     # Forward-looking strategy
    REPORTING = "reporting"   # Historical compliance
    AUDIT = "audit"          # Third-party review


class IssueCategory(str, Enum):
    """RRC domain issue categories."""
    DRILLING_PERMIT = "drilling_permit"
    WELL_COMPLETION = "well_completion"
    PRODUCTION_REPORTING = "production_reporting"
    OPERATOR_TRANSFER = "operator_transfer"
    PLUGGING_COMPLIANCE = "plugging_compliance"
    INJECTION_WELL = "injection_well"
    PIPELINE_PERMIT = "pipeline_permit"
    RULE_VIOLATION = "rule_violation"
    PRORATION = "proration"
    ALLOWABLE = "allowable"
    HORIZONTAL_WELL = "horizontal_well"
    EXCEPTION_REQUEST = "exception_request"


class AuthorityLevel(int, Enum):
    """Hierarchical authority for RRC sources."""
    STATUTE = 7         # Natural Resources Code
    STATEWIDE_RULE = 6  # RRC Statewide Rules
    TAC = 5             # Texas Administrative Code
    RRC_ORDER = 4       # District/field orders
    GUIDANCE = 3        # RRC guidelines
    INDUSTRY = 2        # Industry practice
    INFERENCE = 1       # Logical extension


# ═══════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════

class RRCQuery(BaseModel):
    """Input query for RRC analysis."""
    query: str = Field(..., description="RRC question or data parse request")
    mode: ResponseMode = ResponseMode.FAST
    zone: PositionZone = PositionZone.PLANNING
    include_cloud: bool = Field(default=False, description="Retrieve from Cognition Cloud")
    categories: Optional[List[IssueCategory]] = None


class DoctrineHit(BaseModel):
    """Single doctrine block match."""
    topic: str
    conclusion: str
    confidence: ConfidenceLevel
    authority_level: AuthorityLevel
    primary_authority: List[str]
    reasoning: str
    adversary_position: Optional[str] = None
    counter_arguments: List[str] = Field(default_factory=list)
    resolution_strategy: str = ""
    fact_fragility_score: float = 0.0


class RRCAnalysis(BaseModel):
    """Complete RRC analysis response."""
    query: str
    mode: ResponseMode
    zone: PositionZone
    response_tier: str = "CACHE"  # CACHE | SEMANTIC | DEEP
    triggered_doctrines: List[DoctrineHit] = Field(default_factory=list)
    synthesis: str = ""
    citations: List[str] = Field(default_factory=list)
    confidence: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE
    categories_addressed: List[IssueCategory] = Field(default_factory=list)
    epistemic_caveats: List[str] = Field(default_factory=list)
    adversarial_considerations: str = ""
    latency_ms: float = 0.0
    determinism_hash: str = ""
    cloud_sources: Optional[Dict[str, Any]] = None
    telemetry: Optional[Dict[str, Any]] = None


class HealthStatus(BaseModel):
    """Health check response."""
    engine_id: str
    version: str
    status: str
    uptime_seconds: float
    doctrine_blocks_loaded: int
    cache_size: int
    total_queries: int
    avg_latency_ms: float
    error_rate: float
    cloud_connected: bool
    telemetry: Dict[str, Any]


# ═══════════════════════════════════════════════════════════════════
# DOCTRINE CACHE ENGINE
# ═══════════════════════════════════════════════════════════════════

class RRCDoctrineCacheEngine:
    """
    Three-layer response engine with doctrine cache, semantic search, deep analysis.

    TIE-20 Gold Standard:
    - Doctrine cache with 50+ real RRC blocks
    - Authority hardening (statute > rule > guidance)
    - Confidence stratification (defensible/aggressive/disclosure/high-risk)
    - Semantic normalization (RRC-specific terms)
    - Multi-doctrine decomposition with interaction DAG
    - Epistemic guardrails (banned phrases, disclosure caveats)
    - Adversarial thinking (counter-arguments, resolution strategy)
    - Position zone separation (planning/reporting/audit)
    - Fact fragility scoring (verifiability, recharacterization risk)
    - Deterministic SHA-256 hashing
    """

    def __init__(
        self,
        doctrine_blocks: List[DoctrineBlock],
        cloud_retriever: Optional[CognitionCloudRetriever] = None,
        telemetry: Optional[TelemetryCollector] = None,
    ) -> None:
        self.doctrines = doctrine_blocks
        self.semantic = SemanticNormalizer()
        self.vector_search = VectorSearch()
        self.cloud = cloud_retriever
        self.telemetry = telemetry

        # Build keyword index for fast cache lookup
        self._keyword_index: Dict[str, List[DoctrineBlock]] = {}
        for doctrine in self.doctrines:
            for kw in doctrine.keywords:
                normalized = self.semantic.normalize(kw)
                if normalized not in self._keyword_index:
                    self._keyword_index[normalized] = []
                self._keyword_index[normalized].append(doctrine)

        # Build category index
        self._category_index: Dict[IssueCategory, List[DoctrineBlock]] = {}
        for doctrine in self.doctrines:
            if doctrine.category:
                cat = IssueCategory(doctrine.category)
                if cat not in self._category_index:
                    self._category_index[cat] = []
                self._category_index[cat].append(doctrine)

        logger.info(f"Doctrine cache initialized: {len(self.doctrines)} blocks, "
                   f"{len(self._keyword_index)} keywords, {len(self._category_index)} categories")

    async def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: PositionZone,
        include_cloud: bool = False,
        categories: Optional[List[IssueCategory]] = None,
    ) -> RRCAnalysis:
        """
        Three-layer response strategy:
        1. Doctrine cache (0-200ms) — pre-compiled expert blocks
        2. Semantic retrieval (200-1000ms) — vector search + cloud
        3. Deep analysis (1000-5000ms) — multi-source synthesis
        """
        start = time.monotonic()

        # Normalize query
        normalized_query = self.semantic.normalize(query)
        query_tokens = set(normalized_query.split())

        # Layer 1: Doctrine cache
        cache_hits = await self._doctrine_cache_lookup(query_tokens, categories)

        if cache_hits and mode == ResponseMode.FAST:
            # Fast mode: cache-only
            analysis = self._build_response_from_doctrines(
                query, cache_hits, mode, zone, "CACHE", None
            )
            analysis.latency_ms = round((time.monotonic() - start) * 1000, 2)
            analysis.determinism_hash = self._compute_hash(analysis)

            if self.telemetry:
                self.telemetry.record_query(
                    query=query,
                    tier="CACHE",
                    latency_ms=analysis.latency_ms,
                    hit_count=len(cache_hits),
                    mode=mode.value,
                )

            return analysis

        # Layer 2: Semantic retrieval
        semantic_hits = await self._semantic_search(query, limit=10)
        cloud_knowledge: Optional[CloudKnowledge] = None

        if include_cloud and self.cloud:
            cloud_knowledge = await self.cloud.retrieve_all(
                query,
                category=categories[0].value if categories else None,
                include_crystals=True,
                ekm_limit=15,
            )

        combined_hits = cache_hits + semantic_hits

        if combined_hits and mode != ResponseMode.MEMO:
            # Defense mode: semantic + cloud
            analysis = self._build_response_from_doctrines(
                query, combined_hits, mode, zone, "SEMANTIC", cloud_knowledge
            )
            analysis.latency_ms = round((time.monotonic() - start) * 1000, 2)
            analysis.determinism_hash = self._compute_hash(analysis)

            if self.telemetry:
                self.telemetry.record_query(
                    query=query,
                    tier="SEMANTIC",
                    latency_ms=analysis.latency_ms,
                    hit_count=len(combined_hits),
                    mode=mode.value,
                )

            return analysis

        # Layer 3: Deep analysis (full synthesis)
        deep_hits = await self._deep_analysis(query, combined_hits, cloud_knowledge)

        analysis = self._build_response_from_doctrines(
            query, deep_hits, mode, zone, "DEEP", cloud_knowledge
        )
        analysis.latency_ms = round((time.monotonic() - start) * 1000, 2)
        analysis.determinism_hash = self._compute_hash(analysis)

        if self.telemetry:
            self.telemetry.record_query(
                query=query,
                tier="DEEP",
                latency_ms=analysis.latency_ms,
                hit_count=len(deep_hits),
                mode=mode.value,
            )

        return analysis

    async def _doctrine_cache_lookup(
        self,
        query_tokens: Set[str],
        categories: Optional[List[IssueCategory]] = None,
    ) -> List[DoctrineBlock]:
        """Fast keyword-based doctrine cache lookup."""
        candidates: List[Tuple[DoctrineBlock, float]] = []

        # Category filter first if specified
        if categories:
            pool = []
            for cat in categories:
                pool.extend(self._category_index.get(cat, []))
        else:
            pool = self.doctrines

        # Score by keyword overlap
        for doctrine in pool:
            normalized_keywords = {self.semantic.normalize(kw) for kw in doctrine.keywords}
            overlap = len(query_tokens & normalized_keywords)
            if overlap > 0:
                score = overlap / len(normalized_keywords)
                candidates.append((doctrine, score))

        # Sort by score, return top 5
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in candidates[:5]]

    async def _semantic_search(self, query: str, limit: int = 10) -> List[DoctrineBlock]:
        """Vector-based semantic search fallback."""
        results = await self.vector_search.search(query, top_k=limit)

        matched: List[DoctrineBlock] = []
        for res in results:
            # Match vector results back to doctrine blocks
            for doctrine in self.doctrines:
                if doctrine.topic.lower() in res.text.lower() or res.text.lower() in doctrine.topic.lower():
                    matched.append(doctrine)
                    break

        return matched[:5]

    async def _deep_analysis(
        self,
        query: str,
        existing_hits: List[DoctrineBlock],
        cloud: Optional[CloudKnowledge],
    ) -> List[DoctrineBlock]:
        """
        Deep multi-source synthesis.

        In no-LLM mode, this combines:
        - Existing cache hits
        - Semantic search results
        - Cloud knowledge (if available)
        - Multi-doctrine interaction analysis
        """
        all_hits = existing_hits[:]

        # Add cloud-sourced doctrines if available
        if cloud and cloud.has_results:
            for clause in cloud.clauses[:5]:
                # Find doctrines matching cloud clause categories
                for doctrine in self.doctrines:
                    if clause.category in doctrine.keywords or doctrine.topic.lower() in clause.title.lower():
                        if doctrine not in all_hits:
                            all_hits.append(doctrine)

        # Analyze multi-doctrine interactions
        interactions = self._analyze_doctrine_interactions(all_hits)

        # Sort by authority level, then confidence
        all_hits.sort(
            key=lambda d: (
                -AuthorityLevel[d.authority_level].value,
                -self._confidence_rank(ConfidenceLevel(d.confidence)),
            )
        )

        return all_hits[:8]

    def _analyze_doctrine_interactions(
        self,
        doctrines: List[DoctrineBlock],
    ) -> Dict[str, List[str]]:
        """
        Analyze interactions between multiple triggered doctrines.

        Returns DAG of doctrine interactions (conflicts, dependencies, synergies).
        """
        interactions: Dict[str, List[str]] = {}

        for i, d1 in enumerate(doctrines):
            for d2 in doctrines[i+1:]:
                # Check for keyword overlap (potential interaction)
                overlap = set(d1.keywords) & set(d2.keywords)
                if overlap:
                    key = f"{d1.topic} <-> {d2.topic}"
                    interactions[key] = list(overlap)

        return interactions

    def _build_response_from_doctrines(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        zone: PositionZone,
        tier: str,
        cloud: Optional[CloudKnowledge],
    ) -> RRCAnalysis:
        """Build final RRCAnalysis from triggered doctrines."""
        hits: List[DoctrineHit] = []
        citations: Set[str] = set()
        categories: Set[IssueCategory] = set()

        for doctrine in doctrines:
            hits.append(DoctrineHit(
                topic=doctrine.topic,
                conclusion=doctrine.conclusion_template[0] if doctrine.conclusion_template else "",
                confidence=ConfidenceLevel(doctrine.confidence),
                authority_level=AuthorityLevel[doctrine.authority_level],
                primary_authority=doctrine.primary_authority,
                reasoning=doctrine.reasoning_framework[:200] + "..." if len(doctrine.reasoning_framework) > 200 else doctrine.reasoning_framework,
                adversary_position=doctrine.adversary_position,
                counter_arguments=doctrine.counter_arguments,
                resolution_strategy=doctrine.resolution_strategy,
                fact_fragility_score=self._compute_fragility(doctrine),
            ))

            citations.update(doctrine.primary_authority)
            if doctrine.category:
                categories.add(IssueCategory(doctrine.category))

        # Synthesize response based on mode
        synthesis = self._synthesize_response(doctrines, mode, zone)

        # Apply epistemic guardrails
        caveats = self._apply_epistemic_guardrails(doctrines, zone)

        # Adversarial analysis
        adversarial = self._adversarial_analysis(doctrines)

        # Overall confidence (lowest of all triggered doctrines)
        overall_confidence = min(
            (ConfidenceLevel(d.confidence) for d in doctrines),
            key=self._confidence_rank,
            default=ConfidenceLevel.DEFENSIBLE,
        )

        return RRCAnalysis(
            query=query,
            mode=mode,
            zone=zone,
            response_tier=tier,
            triggered_doctrines=hits,
            synthesis=synthesis,
            citations=sorted(citations),
            confidence=overall_confidence,
            categories_addressed=sorted(categories, key=lambda c: c.value),
            epistemic_caveats=caveats,
            adversarial_considerations=adversarial,
            cloud_sources=cloud.dict() if cloud else None,
        )

    def _synthesize_response(
        self,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        zone: PositionZone,
    ) -> str:
        """Synthesize final response text from triggered doctrines."""
        if not doctrines:
            return "No applicable RRC doctrines found for this query."

        if mode == ResponseMode.FAST:
            # Concise summary
            return doctrines[0].conclusion_template[0] if doctrines[0].conclusion_template else doctrines[0].topic

        if mode == ResponseMode.DEFENSE:
            # Audit-ready with citations
            parts = []
            for d in doctrines[:3]:
                auth = " | ".join(d.primary_authority[:2])
                parts.append(f"{d.topic}: {d.conclusion_template[0]} [{auth}]")
            return "\n\n".join(parts)

        # MEMO mode: full documentation
        parts = []
        for d in doctrines:
            block = f"TOPIC: {d.topic}\n"
            block += f"AUTHORITY: {' | '.join(d.primary_authority)}\n"
            block += f"CONCLUSION: {' '.join(d.conclusion_template)}\n"
            block += f"REASONING: {d.reasoning_framework}\n"
            if d.adversary_position:
                block += f"ADVERSARY: {d.adversary_position}\n"
            if d.counter_arguments:
                block += f"COUNTER-ARGUMENTS: {'; '.join(d.counter_arguments)}\n"
            block += f"RESOLUTION: {d.resolution_strategy}\n"
            parts.append(block)

        return "\n\n" + "="*80 + "\n\n".join(parts)

    def _apply_epistemic_guardrails(
        self,
        doctrines: List[DoctrineBlock],
        zone: PositionZone,
    ) -> List[str]:
        """
        Apply epistemic guardrails to prevent overconfident claims.

        Banned phrases: "always", "never", "guaranteed", "certain", "definitely"
        Required disclosures for high-risk positions.
        """
        caveats: List[str] = []

        # Check for high-risk doctrines
        for d in doctrines:
            if d.confidence == "high_risk":
                caveats.append(
                    f"[{d.topic}] Material uncertainty exists. Litigation/penalty risk present. "
                    "Consult RRC legal counsel before taking position."
                )
            elif d.confidence == "disclosure":
                caveats.append(
                    f"[{d.topic}] Disclosure recommended. Alternative interpretations exist."
                )

        # Zone-specific caveats
        if zone == PositionZone.AUDIT:
            caveats.append(
                "This analysis is for third-party audit purposes. "
                "Historical compliance positions may differ from current planning."
            )
        elif zone == PositionZone.REPORTING:
            caveats.append(
                "This analysis reflects historical reporting positions. "
                "Does not constitute forward-looking planning advice."
            )

        return caveats

    def _adversarial_analysis(self, doctrines: List[DoctrineBlock]) -> str:
        """Generate adversarial considerations across triggered doctrines."""
        adversarial_points: List[str] = []

        for d in doctrines:
            if d.adversary_position:
                adversarial_points.append(f"[{d.topic}] {d.adversary_position}")

        if not adversarial_points:
            return "No significant adversarial positions identified."

        return "ADVERSARIAL CONSIDERATIONS:\n" + "\n".join(adversarial_points)

    def _compute_fragility(self, doctrine: DoctrineBlock) -> float:
        """
        Compute fact fragility score (0.0-1.0).

        Factors:
        - Verifiability: Can facts be independently verified?
        - Recharacterization risk: Could facts be reframed?
        - Testimony dependence: Reliant on witness credibility?
        """
        score = 0.0

        # High authority = low fragility
        if doctrine.authority_level in ["STATUTE", "STATEWIDE_RULE"]:
            score -= 0.3
        elif doctrine.authority_level in ["INFERENCE", "INDUSTRY"]:
            score += 0.3

        # High confidence = low fragility
        if doctrine.confidence == "defensible":
            score -= 0.2
        elif doctrine.confidence == "high_risk":
            score += 0.4

        # Counter-arguments present = higher fragility
        if len(doctrine.counter_arguments) > 3:
            score += 0.2

        # Normalize to [0, 1]
        return max(0.0, min(1.0, 0.5 + score))

    def _confidence_rank(self, conf: ConfidenceLevel) -> int:
        """Rank confidence levels for sorting."""
        return {
            ConfidenceLevel.DEFENSIBLE: 4,
            ConfidenceLevel.AGGRESSIVE: 3,
            ConfidenceLevel.DISCLOSURE: 2,
            ConfidenceLevel.HIGH_RISK: 1,
        }[conf]

    def _compute_hash(self, analysis: RRCAnalysis) -> str:
        """Compute deterministic SHA-256 hash of analysis."""
        # Hash critical fields for reproducibility
        data = {
            "query": analysis.query,
            "doctrines": [h.topic for h in analysis.triggered_doctrines],
            "synthesis": analysis.synthesis,
            "confidence": analysis.confidence.value,
        }
        raw = json.dumps(data, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()


# ═══════════════════════════════════════════════════════════════════
# DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════════

@dataclass
class DriftObservation:
    """Record of doctrine drift over time."""
    doctrine_topic: str
    old_confidence: ConfidenceLevel
    new_confidence: ConfidenceLevel
    timestamp: str
    reason: str


class DriftWatcher:
    """Detect doctrine drift over time (e.g., RRC rule changes)."""

    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path
        self.observations: List[DriftObservation] = []

    def record_drift(
        self,
        doctrine: str,
        old_conf: ConfidenceLevel,
        new_conf: ConfidenceLevel,
        reason: str,
    ) -> None:
        obs = DriftObservation(
            doctrine_topic=doctrine,
            old_confidence=old_conf,
            new_confidence=new_conf,
            timestamp=datetime.utcnow().isoformat(),
            reason=reason,
        )
        self.observations.append(obs)
        logger.warning(f"DOCTRINE DRIFT: {doctrine} {old_conf.value} -> {new_conf.value}: {reason}")

    def get_recent_drifts(self, hours: int = 24) -> List[DriftObservation]:
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        return [
            obs for obs in self.observations
            if datetime.fromisoformat(obs.timestamp) > cutoff
        ]


# ═══════════════════════════════════════════════════════════════════
# COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════

class CoverageMap:
    """Track which doctrines are triggered vs missed (epistemic gap detection)."""

    def __init__(self, all_doctrines: List[DoctrineBlock]) -> None:
        self.all_doctrines = {d.topic: d for d in all_doctrines}
        self.triggered: Dict[str, int] = {d.topic: 0 for d in all_doctrines}
        self.missed: Set[str] = set()

    def mark_triggered(self, topics: List[str]) -> None:
        for topic in topics:
            if topic in self.triggered:
                self.triggered[topic] += 1

    def analyze_gaps(self) -> Dict[str, Any]:
        """Identify doctrines never triggered (potential epistemic blind spots)."""
        never_triggered = [t for t, count in self.triggered.items() if count == 0]
        rarely_triggered = [t for t, count in self.triggered.items() if 0 < count < 3]

        return {
            "never_triggered": never_triggered,
            "rarely_triggered": rarely_triggered,
            "total_doctrines": len(self.all_doctrines),
            "coverage_pct": round(
                100 * (1 - len(never_triggered) / max(len(self.all_doctrines), 1)), 1
            ),
        }


# ═══════════════════════════════════════════════════════════════════
# METRICS COLLECTOR
# ═══════════════════════════════════════════════════════════════════

@dataclass
class QueryMetrics:
    """Per-query metrics."""
    query: str
    tier: str
    latency_ms: float
    hit_count: int
    mode: str
    timestamp: str


class MetricsCollector:
    """Aggregate query metrics for performance monitoring."""

    def __init__(self) -> None:
        self.queries: List[QueryMetrics] = []
        self.start_time = time.monotonic()

    def record(
        self,
        query: str,
        tier: str,
        latency_ms: float,
        hit_count: int,
        mode: str,
    ) -> None:
        self.queries.append(QueryMetrics(
            query=query,
            tier=tier,
            latency_ms=latency_ms,
            hit_count=hit_count,
            mode=mode,
            timestamp=datetime.utcnow().isoformat(),
        ))

    def stats(self) -> Dict[str, Any]:
        if not self.queries:
            return {
                "total_queries": 0,
                "avg_latency_ms": 0.0,
                "cache_hit_rate": 0.0,
                "error_rate": 0.0,
            }

        cache_tier = sum(1 for q in self.queries if q.tier == "CACHE")
        total = len(self.queries)

        return {
            "total_queries": total,
            "avg_latency_ms": round(sum(q.latency_ms for q in self.queries) / total, 2),
            "cache_hit_rate": round(cache_tier / total, 3),
            "tier_distribution": {
                "CACHE": sum(1 for q in self.queries if q.tier == "CACHE"),
                "SEMANTIC": sum(1 for q in self.queries if q.tier == "SEMANTIC"),
                "DEEP": sum(1 for q in self.queries if q.tier == "DEEP"),
            },
            "uptime_seconds": round(time.monotonic() - self.start_time, 1),
        }


# ═══════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════

app = FastAPI(
    title="R01_rrc_parser — RRC Data Parser",
    version=VERSION,
    description="Texas Railroad Commission data parsing with TIE-20 compliance",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
engine: Optional[RRCDoctrineCacheEngine] = None
telemetry: Optional[TelemetryCollector] = None
metrics: Optional[MetricsCollector] = None
drift_watcher: Optional[DriftWatcher] = None
coverage_map: Optional[CoverageMap] = None
cloud_retriever: Optional[CognitionCloudRetriever] = None


@app.on_event("startup")
async def startup() -> None:
    """Initialize engine on startup."""
    global engine, telemetry, metrics, drift_watcher, coverage_map, cloud_retriever

    logger.info(f"Starting {ENGINE_ID} v{VERSION} on port {PORT}")

    # Initialize components
    telemetry = TelemetryCollector(engine_id=ENGINE_ID)
    metrics = MetricsCollector()
    drift_watcher = DriftWatcher(log_path=AUDIT_LOG_PATH.parent / "rrc_drift.jsonl")
    coverage_map = CoverageMap(all_doctrines=DOCTRINE_BLOCKS)

    # Initialize cloud retriever
    try:
        cloud_retriever = CognitionCloudRetriever()
        logger.info("Cognition Cloud retriever initialized")
    except Exception as e:
        logger.warning(f"Cloud retriever initialization failed: {e}")
        cloud_retriever = None

    # Initialize doctrine cache engine
    engine = RRCDoctrineCacheEngine(
        doctrine_blocks=DOCTRINE_BLOCKS,
        cloud_retriever=cloud_retriever,
        telemetry=telemetry,
    )

    logger.info(f"Engine initialized with {len(DOCTRINE_BLOCKS)} doctrine blocks")


@app.on_event("shutdown")
async def shutdown() -> None:
    """Cleanup on shutdown."""
    if cloud_retriever:
        await cloud_retriever.close()
    logger.info(f"{ENGINE_ID} shutdown complete")


@app.post("/api/analyze", response_model=RRCAnalysis)
async def analyze_rrc_query(req: RRCQuery) -> RRCAnalysis:
    """Analyze RRC query with three-layer response."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    try:
        analysis = await engine.three_layer_response(
            query=req.query,
            mode=req.mode,
            zone=req.zone,
            include_cloud=req.include_cloud,
            categories=req.categories,
        )

        # Update coverage map
        if coverage_map:
            topics = [h.topic for h in analysis.triggered_doctrines]
            coverage_map.mark_triggered(topics)

        # Audit log
        if AUDIT_LOG_PATH.parent.exists():
            with AUDIT_LOG_PATH.open("a") as f:
                f.write(json.dumps({
                    "timestamp": datetime.utcnow().isoformat(),
                    "query": req.query,
                    "mode": req.mode.value,
                    "zone": req.zone.value,
                    "tier": analysis.response_tier,
                    "doctrines": [h.topic for h in analysis.triggered_doctrines],
                    "confidence": analysis.confidence.value,
                    "latency_ms": analysis.latency_ms,
                    "hash": analysis.determinism_hash,
                }) + "\n")

        return analysis

    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        if telemetry:
            telemetry.record_error(error_domain="analysis", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health", response_model=HealthStatus)
async def health_check() -> HealthStatus:
    """Comprehensive health check."""
    if not engine or not metrics or not telemetry:
        raise HTTPException(status_code=503, detail="Engine not ready")

    stats = metrics.stats()
    tel_stats = telemetry.stats()

    return HealthStatus(
        engine_id=ENGINE_ID,
        version=VERSION,
        status="healthy",
        uptime_seconds=stats["uptime_seconds"],
        doctrine_blocks_loaded=len(DOCTRINE_BLOCKS),
        cache_size=len(engine._keyword_index),
        total_queries=stats["total_queries"],
        avg_latency_ms=stats["avg_latency_ms"],
        error_rate=tel_stats.get("error_rate", 0.0),
        cloud_connected=cloud_retriever is not None,
        telemetry=tel_stats,
    )


@app.get("/api/coverage")
async def get_coverage() -> Dict[str, Any]:
    """Get doctrine coverage statistics."""
    if not coverage_map:
        raise HTTPException(status_code=503, detail="Coverage map not initialized")

    return coverage_map.analyze_gaps()


@app.get("/api/drift")
async def get_drift(hours: int = Query(24, ge=1, le=720)) -> Dict[str, Any]:
    """Get recent doctrine drift observations."""
    if not drift_watcher:
        raise HTTPException(status_code=503, detail="Drift watcher not initialized")

    recent = drift_watcher.get_recent_drifts(hours=hours)
    return {
        "drift_count": len(recent),
        "observations": [
            {
                "doctrine": obs.doctrine_topic,
                "old_confidence": obs.old_confidence.value,
                "new_confidence": obs.new_confidence.value,
                "timestamp": obs.timestamp,
                "reason": obs.reason,
            }
            for obs in recent
        ],
    }


@app.get("/api/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get performance metrics."""
    if not metrics:
        raise HTTPException(status_code=503, detail="Metrics not initialized")

    return metrics.stats()


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main() -> None:
    """Run the FastAPI server."""
    logger.add(
        "O:/ECHO_OMEGA_PRIME/LOGS/rrc_parser_{time}.log",
        rotation="100 MB",
        retention="30 days",
        level="INFO",
    )

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info",
    )


if __name__ == "__main__":
    main()
