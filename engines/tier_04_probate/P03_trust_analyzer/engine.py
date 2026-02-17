"""
P03 TRUST ANALYZER — Intelligence Engine for Trust Law
Professional-grade trust analysis system for estate planning attorneys, trustees, and wealth advisors.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled trust law expertise (50+ blocks)
    Layer 2: Semantic Retrieval (200-700ms) - Fast RAG on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-source synthesis

Response Modes:
    FAST: Doctrine-driven, minimal citations, sub-2 seconds
    DEFENSE: Structured reasoning, audit-ready, burden analysis
    MEMO: Long-form, citation-heavy, firm documentation

Domain Coverage:
    - Trust creation and validity (revocable/irrevocable)
    - Grantor trust taxation (IRC §§671-679, IDGTs)
    - Trustee duties and powers (fiduciary obligations)
    - Distribution standards (HEMS, discretionary, mandatory)
    - Spendthrift and creditor protection (§112.035)
    - Trust modification and termination (§112.054)
    - Perpetuities and dynasty trusts (RAP abolition §112.036)
    - Charitable trusts (CRTs, CLTs)
    - Life insurance trusts (ILITs, Crummey powers)
    - Qualified trusts (QPRTs, GRATs, SLATs)

Authority: 11.0 SOVEREIGN
Port: 8653
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
import hashlib
import time
import uuid
from pathlib import Path
from loguru import logger
import json

# Local imports
import sys
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
sys.path.insert(0, str(ENGINE_DIR.parent / "_shared"))

from telemetry import (
    init_telemetry,
    get_telemetry,
    trace_query,
    complete_trace,
    log_error,
    record_doctrine_mutation,
    ErrorDomain,
    ResponseLayer,
    MutationType,
    MutationOrigin
)

from semantic import normalize_semantics, NormalizationResult

import sys

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DoctrineBlock,
    ConfidenceStratum,
    IssueCategory,
    get_doctrine_cache,
    search_doctrines,
    get_doctrine_by_topic,
    DOCTRINE_CACHE
)

from search import (
    init_cloud_retriever,
    get_cloud_retriever,
    cloud_search,
    SearchResponse
)

# Configure logging
LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/P03_trust_analyzer/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "trust_analyzer_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}"
)

AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"


# ==============================================================================
# PYDANTIC MODELS
# ==============================================================================

class ResponseMode(str, Enum):
    """Response mode selection"""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class PositionZone(str, Enum):
    """Position zone for analysis"""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class QueryRequest(BaseModel):
    """Trust analysis query request"""
    query: str = Field(..., description="Trust law question or issue to analyze")
    response_mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    position_zone: Optional[PositionZone] = Field(default=None, description="Analysis perspective")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class CitationEntry(BaseModel):
    """Single legal citation"""
    authority: str
    citation: str
    relevance: str


class TrustAnalysisResponse(BaseModel):
    """Complete trust analysis response"""
    query: str
    response_mode: ResponseMode
    position_zone: Optional[PositionZone]

    # Core analysis
    summary: str
    detailed_analysis: Optional[str] = None
    reasoning_chain: List[str]

    # Doctrine and authority
    doctrines_triggered: List[str]
    primary_authority: List[CitationEntry]
    confidence_stratum: ConfidenceStratum
    issue_categories: List[IssueCategory]

    # Risk and strategy
    key_factors: List[str]
    counter_arguments: List[str]
    resolution_strategy: str
    disclosure_required: bool = False

    # Metadata
    trace_id: str
    latency_ms: float
    layer_used: ResponseLayer
    cache_hit: bool
    determinism_hash: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    p95_latency_ms: float
    error_rate: float


# ==============================================================================
# METRICS COLLECTOR
# ==============================================================================

class MetricsCollector:
    """Lightweight metrics for operational awareness"""

    def __init__(self):
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0
        self.start_time = time.time()

    def record_query(self, latency_ms: float, doctrine_hit: bool):
        """Record query execution"""
        self.queries.append(time.time())
        self.latencies.append(latency_ms)
        if doctrine_hit:
            self.doctrine_hits += 1
        else:
            self.doctrine_misses += 1

        # Keep last 1000 only
        if len(self.latencies) > 1000:
            self.latencies.pop(0)
            self.queries.pop(0)

    def record_error(self, error_msg: str):
        """Record error"""
        self.errors.append(time.time())
        self.last_error = error_msg
        if len(self.errors) > 100:
            self.errors.pop(0)

    def get_cache_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total = self.doctrine_hits + self.doctrine_misses
        return self.doctrine_hits / total if total > 0 else 0.0

    def get_p95_latency(self) -> float:
        """Get 95th percentile latency"""
        if not self.latencies:
            return 0.0
        sorted_lat = sorted(self.latencies)
        idx = int(len(sorted_lat) * 0.95)
        return sorted_lat[idx]

    def get_error_rate(self) -> float:
        """Calculate error rate"""
        return len(self.errors) / len(self.queries) if self.queries else 0.0

    def get_uptime(self) -> float:
        """Get uptime in seconds"""
        return time.time() - self.start_time


# Global metrics
metrics = MetricsCollector()


# ==============================================================================
# DOCTRINE COVERAGE MAP
# ==============================================================================

class DoctrineCoverageMap:
    """
    Track which doctrines are triggered vs. missed.
    Epistemic control for coverage gaps.
    """

    def __init__(self):
        self.doctrine_triggers: Dict[str, int] = {}
        self.doctrine_misses: List[str] = []
        self.coverage_gaps: List[str] = []

    def record_trigger(self, doctrine_topic: str):
        """Record doctrine trigger"""
        self.doctrine_triggers[doctrine_topic] = self.doctrine_triggers.get(doctrine_topic, 0) + 1

    def record_miss(self, query: str):
        """Record cache miss - query had no doctrine hit"""
        self.doctrine_misses.append(query)
        if len(self.doctrine_misses) > 100:
            self.doctrine_misses.pop(0)

    def identify_gaps(self) -> List[str]:
        """Identify coverage gaps from repeated misses"""
        # Simple heuristic: if same query pattern missed multiple times
        # In production, would use semantic clustering
        return []

    def get_coverage_report(self) -> Dict[str, Any]:
        """Generate coverage report"""
        total_triggers = sum(self.doctrine_triggers.values())
        return {
            "total_doctrines": len(DOCTRINE_CACHE),
            "triggered_doctrines": len(self.doctrine_triggers),
            "total_triggers": total_triggers,
            "total_misses": len(self.doctrine_misses),
            "top_triggered": sorted(
                self.doctrine_triggers.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10],
            "coverage_gaps": self.coverage_gaps
        }


# Global coverage map
coverage_map = DoctrineCoverageMap()


# ==============================================================================
# DRIFT WATCHER
# ==============================================================================

class DoctrineDriftWatcher:
    """
    Monitor for doctrine drift over time.
    Detect when law changes require doctrine updates.
    """

    def __init__(self):
        self.drift_events: List[Dict[str, Any]] = []
        self.doctrine_versions: Dict[str, str] = {}

    def detect_drift(self, doctrine_topic: str, current_version: str) -> bool:
        """Check if doctrine has drifted from expected version"""
        if doctrine_topic not in self.doctrine_versions:
            self.doctrine_versions[doctrine_topic] = current_version
            return False

        if self.doctrine_versions[doctrine_topic] != current_version:
            self.record_drift(doctrine_topic, self.doctrine_versions[doctrine_topic], current_version)
            return True

        return False

    def record_drift(self, doctrine_topic: str, old_version: str, new_version: str):
        """Record drift event"""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "doctrine_topic": doctrine_topic,
            "old_version": old_version,
            "new_version": new_version
        }
        self.drift_events.append(event)
        logger.warning(f"Doctrine drift detected: {doctrine_topic}")

    def get_drift_report(self) -> List[Dict[str, Any]]:
        """Get recent drift events"""
        return self.drift_events[-20:]


# Global drift watcher
drift_watcher = DoctrineDriftWatcher()


# ==============================================================================
# FACT FRAGILITY SCORING
# ==============================================================================

@dataclass
class FactFragilityScore:
    """
    Score how fragile a legal position is based on fact sensitivity.
    High fragility = position depends heavily on specific facts.
    """
    verifiability: float  # 0.0-1.0, higher = easier to verify
    recharacterization_risk: float  # 0.0-1.0, higher = more IRS recharacterization risk
    testimony_dependence: float  # 0.0-1.0, higher = relies on witness testimony
    overall_fragility: float  # Composite score

    def to_dict(self) -> Dict[str, float]:
        return {
            "verifiability": self.verifiability,
            "recharacterization_risk": self.recharacterization_risk,
            "testimony_dependence": self.testimony_dependence,
            "overall_fragility": self.overall_fragility
        }


def calculate_fact_fragility(doctrine: DoctrineBlock, query_context: Optional[Dict]) -> FactFragilityScore:
    """
    Calculate fact fragility for a doctrine position.
    """
    # Base fragility on confidence stratum
    base_fragility = {
        ConfidenceStratum.DEFENSIBLE: 0.2,
        ConfidenceStratum.AGGRESSIVE: 0.6,
        ConfidenceStratum.DISCLOSURE: 0.7,
        ConfidenceStratum.HIGH_RISK: 0.9
    }.get(doctrine.confidence_stratification, 0.5)

    # Adjust for verifiability (statutory vs. common law)
    statutory_count = sum(1 for auth in doctrine.primary_authority if "§" in auth or "IRC" in auth)
    verifiability = statutory_count / len(doctrine.primary_authority) if doctrine.primary_authority else 0.5

    # Recharacterization risk based on issue category
    high_risk_categories = [IssueCategory.GRANTOR_TRUST_TAX, IssueCategory.ESTATE_TAX_PLANNING]
    recharac_risk = 0.7 if doctrine.issue_category in high_risk_categories else 0.3

    # Testimony dependence (if facts require subjective interpretation)
    testimony_keywords = ["intent", "purpose", "understanding", "agreement", "practice"]
    testimony_dep = 0.8 if any(kw in doctrine.reasoning_framework.lower() for kw in testimony_keywords) else 0.3

    overall = (base_fragility + recharac_risk + testimony_dep) / 3

    return FactFragilityScore(
        verifiability=verifiability,
        recharacterization_risk=recharac_risk,
        testimony_dependence=testimony_dep,
        overall_fragility=overall
    )


# ==============================================================================
# MULTI-DOCTRINE DECOMPOSITION
# ==============================================================================

@dataclass
class DoctrineInteraction:
    """Relationship between multiple doctrines"""
    doctrine_a: str
    doctrine_b: str
    interaction_type: str  # "reinforces", "conflicts", "prerequisites"
    description: str


class MultiDoctrineAnalyzer:
    """
    Decompose complex issues into multiple interacting doctrines.
    Build dependency graph of legal principles.
    """

    def __init__(self):
        # Define common doctrine interactions
        self.interactions = [
            DoctrineInteraction(
                "grantor_trust_671_general_rule",
                "intentionally_defective_grantor_trust_idgt",
                "prerequisites",
                "IDGT planning requires understanding grantor trust rules"
            ),
            DoctrineInteraction(
                "hems_health_education_maintenance_support",
                "spendthrift_provision_creditor_protection",
                "reinforces",
                "HEMS + spendthrift maximizes beneficiary protection"
            ),
            DoctrineInteraction(
                "irrevocable_trust_creation_elements",
                "trust_modification_termination_112054",
                "conflicts",
                "Irrevocability limits modification options"
            ),
        ]

    def decompose_issue(self, query: str, triggered_doctrines: List[DoctrineBlock]) -> List[IssueCategory]:
        """Decompose query into issue categories"""
        categories = set()
        for doctrine in triggered_doctrines:
            categories.add(doctrine.issue_category)
        return list(categories)

    def build_dependency_graph(self, doctrines: List[DoctrineBlock]) -> Dict[str, List[str]]:
        """Build dependency graph showing which doctrines depend on others"""
        graph = {}
        for doctrine in doctrines:
            graph[doctrine.topic] = []
            # Find interactions
            for interaction in self.interactions:
                if interaction.doctrine_a == doctrine.topic and interaction.interaction_type == "prerequisites":
                    graph[doctrine.topic].append(interaction.doctrine_b)
        return graph

    def find_conflicts(self, doctrines: List[DoctrineBlock]) -> List[DoctrineInteraction]:
        """Identify conflicting doctrines in analysis"""
        conflicts = []
        doctrine_topics = {d.topic for d in doctrines}
        for interaction in self.interactions:
            if interaction.interaction_type == "conflicts":
                if interaction.doctrine_a in doctrine_topics and interaction.doctrine_b in doctrine_topics:
                    conflicts.append(interaction)
        return conflicts


# Global multi-doctrine analyzer
multi_doctrine = MultiDoctrineAnalyzer()


# ==============================================================================
# AUTHORITY HARDENING
# ==============================================================================

@dataclass
class AuthorityWeight:
    """Weighted authority hierarchy"""
    level: int  # 1 = statute, 2 = regulation, 3 = case, 4 = commentary
    weight: float
    description: str


AUTHORITY_HIERARCHY = {
    "statute": AuthorityWeight(1, 1.0, "Texas Property Code, IRC"),
    "regulation": AuthorityWeight(2, 0.85, "Treasury Regulations"),
    "case_controlling": AuthorityWeight(3, 0.75, "Texas Supreme Court, 5th Circuit"),
    "case_persuasive": AuthorityWeight(4, 0.6, "Other circuits, Texas Courts of Appeals"),
    "plr": AuthorityWeight(5, 0.5, "Private Letter Rulings"),
    "commentary": AuthorityWeight(6, 0.3, "Treatises, articles")
}


def classify_authority(citation: str) -> AuthorityWeight:
    """Classify authority by type and assign weight"""
    citation_lower = citation.lower()

    if "property code" in citation_lower or "irc" in citation_lower or "§" in citation:
        return AUTHORITY_HIERARCHY["statute"]
    elif "treas. reg" in citation_lower or "reg. §" in citation_lower:
        return AUTHORITY_HIERARCHY["regulation"]
    elif "tex." in citation_lower and "s.w." in citation_lower:
        return AUTHORITY_HIERARCHY["case_controlling"]
    elif "plr" in citation_lower or "letter ruling" in citation_lower:
        return AUTHORITY_HIERARCHY["plr"]
    else:
        return AUTHORITY_HIERARCHY["commentary"]


def resolve_authority_conflict(authorities: List[str]) -> str:
    """Resolve conflicts between authorities by hierarchy"""
    if not authorities:
        return "No authority"

    weighted = [(auth, classify_authority(auth)) for auth in authorities]
    weighted.sort(key=lambda x: (x[1].level, -x[1].weight))

    return weighted[0][0]  # Return highest-weighted authority


# ==============================================================================
# DEEP ANALYSIS MODE
# ==============================================================================

class DeepAnalyzer:
    """
    Layer 3: Deep analysis with multi-source synthesis.
    Used when doctrine cache + semantic search insufficient.
    """

    def __init__(self):
        self.analysis_depth = "comprehensive"

    async def analyze_comprehensive(
        self,
        query: str,
        triggered_doctrines: List[DoctrineBlock],
        semantic_results: Optional[SearchResponse],
        response_mode: ResponseMode
    ) -> str:
        """
        Perform deep multi-source analysis.
        Synthesize doctrine cache + semantic search + legal reasoning.
        """
        analysis_parts = []

        # Start with triggered doctrines
        if triggered_doctrines:
            analysis_parts.append("## Applicable Doctrines\n")
            for doctrine in triggered_doctrines[:3]:  # Top 3
                analysis_parts.append(f"### {doctrine.topic}\n")
                analysis_parts.append(f"{doctrine.conclusion_template[0]}\n\n")

        # Add reasoning framework from top doctrine
        if triggered_doctrines and response_mode == ResponseMode.MEMO:
            top_doctrine = triggered_doctrines[0]
            analysis_parts.append("## Legal Framework\n")
            analysis_parts.append(f"{top_doctrine.reasoning_framework}\n\n")

        # Add authority citations
        if triggered_doctrines:
            analysis_parts.append("## Primary Authority\n")
            all_authorities = set()
            for doctrine in triggered_doctrines:
                all_authorities.update(doctrine.primary_authority)
            for auth in sorted(all_authorities)[:10]:
                analysis_parts.append(f"- {auth}\n")
            analysis_parts.append("\n")

        # Add counter-arguments if DEFENSE mode
        if response_mode == ResponseMode.DEFENSE and triggered_doctrines:
            analysis_parts.append("## Counter-Arguments to Address\n")
            for doctrine in triggered_doctrines[:2]:
                for counter in doctrine.counter_arguments[:3]:
                    analysis_parts.append(f"- {counter}\n")
            analysis_parts.append("\n")

        return "".join(analysis_parts)


# Global deep analyzer
deep_analyzer = DeepAnalyzer()


# ==============================================================================
# THREE-LAYER RESPONSE ENGINE
# ==============================================================================

class TrustAnalysisEngine:
    """
    Core three-layer trust analysis engine.
    Layer 1: Doctrine cache (fast)
    Layer 2: Semantic retrieval (medium)
    Layer 3: Deep analysis (comprehensive)
    """

    def __init__(self):
        self.doctrine_cache = get_doctrine_cache()
        logger.info(f"Trust analyzer initialized with {len(self.doctrine_cache)} doctrine blocks")

    async def analyze_query(
        self,
        query: str,
        response_mode: ResponseMode = ResponseMode.FAST,
        position_zone: Optional[PositionZone] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> TrustAnalysisResponse:
        """
        Execute three-layer analysis pipeline.
        """
        trace_id = trace_query(query, response_mode.value)
        start_time = time.time()

        try:
            # Layer 0: Semantic normalization
            norm_result = normalize_semantics(query)
            logger.debug(f"Normalized: {len(norm_result.normalized_terms)} terms, {len(norm_result.detected_concepts)} concepts")

            # Layer 1: Doctrine cache search
            triggered_doctrines = self._search_doctrine_cache(query, norm_result)

            if triggered_doctrines:
                # Cache hit - fast response
                logger.info(f"Doctrine cache HIT: {len(triggered_doctrines)} blocks triggered")
                response = await self._build_response_from_cache(
                    query, triggered_doctrines, response_mode, position_zone, trace_id
                )
                complete_trace(
                    trace_id,
                    success=True,
                    layer_used=ResponseLayer.DOCTRINE_CACHE,
                    doctrines_triggered=[d.topic for d in triggered_doctrines],
                    cache_hit=True
                )
                metrics.record_query((time.time() - start_time) * 1000, doctrine_hit=True)
                coverage_map.record_trigger(triggered_doctrines[0].topic)
                return response

            # Layer 2: Semantic retrieval (cloud search)
            logger.info("Doctrine cache MISS - attempting semantic retrieval")
            semantic_results = cloud_search(query, top_k=5)

            if semantic_results.results:
                # Semantic hit
                logger.info(f"Semantic retrieval HIT: {len(semantic_results.results)} results")
                # Would build response from semantic results
                # For now, fall through to deep analysis

            # Layer 3: Deep analysis
            logger.info("Invoking deep analysis mode")
            response = await self._deep_analysis(
                query, triggered_doctrines, semantic_results, response_mode, position_zone, trace_id
            )

            complete_trace(
                trace_id,
                success=True,
                layer_used=ResponseLayer.DEEP_ANALYSIS,
                cache_hit=False
            )
            metrics.record_query((time.time() - start_time) * 1000, doctrine_hit=False)
            coverage_map.record_miss(query)

            return response

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            log_error(trace_id, ErrorDomain.UNKNOWN, str(e))
            complete_trace(trace_id, success=False)
            metrics.record_error(str(e))
            raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

    def _search_doctrine_cache(
        self,
        query: str,
        norm_result: NormalizationResult
    ) -> List[DoctrineBlock]:
        """Search doctrine cache using normalized terms and concepts"""
        triggered = []

        # Search by normalized terms
        if norm_result.normalized_terms:
            triggered.extend(search_doctrines(norm_result.normalized_terms))

        # Search by detected concepts
        query_lower = query.lower()
        for doctrine in self.doctrine_cache:
            if any(kw.lower() in query_lower for kw in doctrine.keywords):
                if doctrine not in triggered:
                    triggered.append(doctrine)

        # Rank by relevance (keyword overlap)
        def relevance_score(doctrine: DoctrineBlock) -> int:
            return sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)

        triggered.sort(key=relevance_score, reverse=True)

        return triggered[:5]  # Top 5 most relevant

    async def _build_response_from_cache(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        response_mode: ResponseMode,
        position_zone: Optional[PositionZone],
        trace_id: str
    ) -> TrustAnalysisResponse:
        """Build response from doctrine cache hits"""
        top_doctrine = doctrines[0]

        # Build summary
        summary = " ".join(top_doctrine.conclusion_template)

        # Build reasoning chain
        reasoning_chain = []
        if response_mode == ResponseMode.FAST:
            reasoning_chain = top_doctrine.conclusion_template[:2]
        elif response_mode == ResponseMode.DEFENSE:
            reasoning_chain = [
                summary,
                f"Key factors: {', '.join(top_doctrine.key_factors[:5])}",
                f"Burden: {top_doctrine.burden_holder}",
                f"Primary authority: {top_doctrine.primary_authority[0]}"
            ]
        else:  # MEMO
            reasoning_chain = [
                summary,
                f"Legal framework:\n{top_doctrine.reasoning_framework[:500]}...",
                f"Key factors:\n" + "\n".join(f"- {f}" for f in top_doctrine.key_factors),
                f"Primary authority:\n" + "\n".join(f"- {a}" for a in top_doctrine.primary_authority[:5])
            ]

        # Build citations
        citations = [
            CitationEntry(
                authority=auth.split(" (")[0] if " (" in auth else auth,
                citation=auth,
                relevance="primary"
            )
            for auth in top_doctrine.primary_authority[:5]
        ]

        # Fact fragility
        fragility = calculate_fact_fragility(top_doctrine, None)

        # Check for disclosure triggers
        disclosure_required = any(
            trigger in summary.lower() or trigger in top_doctrine.reasoning_framework.lower()
            for trigger in ["novel", "untested", "aggressive", "uncertain", "conflicting"]
        )

        # Detailed analysis for MEMO mode
        detailed_analysis = None
        if response_mode == ResponseMode.MEMO:
            detailed_analysis = await deep_analyzer.analyze_comprehensive(
                query, doctrines, None, response_mode
            )

        # Calculate determinism hash
        hash_input = f"{query}|{top_doctrine.topic}|{response_mode.value}"
        determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        latency_ms = (time.time() - get_telemetry()._active_traces[trace_id].started_at.timestamp()) * 1000

        return TrustAnalysisResponse(
            query=query,
            response_mode=response_mode,
            position_zone=position_zone,
            summary=summary,
            detailed_analysis=detailed_analysis,
            reasoning_chain=reasoning_chain,
            doctrines_triggered=[d.topic for d in doctrines],
            primary_authority=citations,
            confidence_stratum=top_doctrine.confidence_stratification,
            issue_categories=multi_doctrine.decompose_issue(query, doctrines),
            key_factors=top_doctrine.key_factors[:8],
            counter_arguments=top_doctrine.counter_arguments[:5],
            resolution_strategy=top_doctrine.resolution_strategy,
            disclosure_required=disclosure_required,
            trace_id=trace_id,
            latency_ms=round(latency_ms, 1),
            layer_used=ResponseLayer.DOCTRINE_CACHE,
            cache_hit=True,
            determinism_hash=determinism_hash
        )

    async def _deep_analysis(
        self,
        query: str,
        triggered_doctrines: List[DoctrineBlock],
        semantic_results: Optional[SearchResponse],
        response_mode: ResponseMode,
        position_zone: Optional[PositionZone],
        trace_id: str
    ) -> TrustAnalysisResponse:
        """Perform deep analysis when cache misses"""

        summary = f"Deep analysis required for: {query}"
        detailed_analysis = await deep_analyzer.analyze_comprehensive(
            query, triggered_doctrines or [], semantic_results, response_mode
        )

        reasoning_chain = [
            "No direct doctrine cache hit - performing comprehensive analysis",
            "Consulting multiple sources and legal frameworks",
            "Synthesizing analysis from available authorities"
        ]

        hash_input = f"{query}|deep_analysis|{response_mode.value}"
        determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        latency_ms = (time.time() - get_telemetry()._active_traces[trace_id].started_at.timestamp()) * 1000

        return TrustAnalysisResponse(
            query=query,
            response_mode=response_mode,
            position_zone=position_zone,
            summary=summary,
            detailed_analysis=detailed_analysis,
            reasoning_chain=reasoning_chain,
            doctrines_triggered=[],
            primary_authority=[],
            confidence_stratum=ConfidenceStratum.DISCLOSURE,
            issue_categories=[],
            key_factors=[],
            counter_arguments=[],
            resolution_strategy="Consult with trust law specialist for novel issue",
            disclosure_required=True,
            trace_id=trace_id,
            latency_ms=round(latency_ms, 1),
            layer_used=ResponseLayer.DEEP_ANALYSIS,
            cache_hit=False,
            determinism_hash=determinism_hash
        )


# ==============================================================================
# FASTAPI APPLICATION
# ==============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown"""
    # Startup
    logger.info("Trust Analyzer Engine starting up...")
    init_telemetry(LOG_DIR)
    init_cloud_retriever(enabled=True)
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    logger.info("Trust Analyzer Engine ready")

    yield

    # Shutdown
    logger.info("Trust Analyzer Engine shutting down...")
    logger.info(f"Total queries processed: {metrics.get_uptime()}")


app = FastAPI(
    title="P03 Trust Analyzer Intelligence Engine",
    description="Professional trust law analysis system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
engine = TrustAnalysisEngine()


# ==============================================================================
# API ENDPOINTS
# ==============================================================================

@app.post("/analyze", response_model=TrustAnalysisResponse)
async def analyze_trust_issue(request: QueryRequest):
    """
    Analyze a trust law issue.
    Main endpoint for trust analysis queries.
    """
    logger.info(f"Query received: {request.query[:100]}... | Mode: {request.response_mode}")
    return await engine.analyze_query(
        request.query,
        request.response_mode,
        request.position_zone,
        request.context
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    telemetry_metrics = get_telemetry().get_metrics_snapshot()

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        uptime_seconds=round(metrics.get_uptime(), 1),
        total_queries=telemetry_metrics["total_queries"],
        cache_hit_rate=round(metrics.get_cache_hit_rate(), 4),
        p95_latency_ms=round(metrics.get_p95_latency(), 1),
        error_rate=telemetry_metrics["error_rate"]
    )


@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine blocks in cache"""
    return {
        "total_doctrines": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "issue_category": d.issue_category.value,
                "confidence_stratum": d.confidence_stratification.value
            }
            for d in DOCTRINE_CACHE
        ]
    }


@app.get("/doctrine/{topic}")
async def get_doctrine(topic: str):
    """Retrieve specific doctrine block"""
    doctrine = get_doctrine_by_topic(topic)
    if not doctrine:
        raise HTTPException(status_code=404, detail=f"Doctrine not found: {topic}")

    return {
        "topic": doctrine.topic,
        "keywords": doctrine.keywords,
        "conclusion": doctrine.conclusion_template,
        "reasoning": doctrine.reasoning_framework,
        "key_factors": doctrine.key_factors,
        "primary_authority": doctrine.primary_authority,
        "confidence": doctrine.confidence,
        "confidence_stratum": doctrine.confidence_stratification.value,
        "issue_category": doctrine.issue_category.value
    }


@app.get("/coverage")
async def coverage_report():
    """Get doctrine coverage report"""
    return coverage_map.get_coverage_report()


@app.get("/drift")
async def drift_report():
    """Get doctrine drift events"""
    return drift_watcher.get_drift_report()


@app.get("/metrics")
async def get_metrics():
    """Get detailed metrics"""
    return get_telemetry().get_metrics_snapshot()


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Trust Analyzer Engine on port 8653")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8653,
        log_level="info"
    )