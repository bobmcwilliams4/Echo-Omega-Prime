"""
P07 Fiduciary Duty Intelligence Engine
TIE-20 Compliant Rule-Based Engine

Comprehensive fiduciary duty analysis for executors, trustees, and guardians under Texas law.
Covers breach analysis, surcharge liability, removal grounds, and all core fiduciary obligations.

Port: 8657
Version: 1.0.0
Mode: Rule-Based
Domain: Fiduciary Law
Jurisdiction: Texas
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import hashlib
import json
import sys
import uvicorn

from loguru import logger

# Import engine components

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import FIDUCIARY_DOCTRINES, DoctrineBlock
from semantic import FiduciarySemanticNormalizer
from search import FiduciaryVectorSearch
from telemetry import (
    FiduciaryTelemetry,
    QueryMetrics,
    DriftObservation,
    CoverageGap,
    QueryLayer,
    IssueCategory
)

# Configuration
CONFIG_PATH = Path(__file__).parent / "config.json"
with CONFIG_PATH.open("r") as f:
    CONFIG = json.load(f)

# Initialize FastAPI
app = FastAPI(
    title="P07 Fiduciary Duty Intelligence Engine",
    version="1.0.0",
    description="TIE-20 compliant fiduciary duty analysis engine"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG["api_settings"]["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize components
semantic_normalizer = FiduciarySemanticNormalizer()
vector_search = FiduciaryVectorSearch(CONFIG)
telemetry = FiduciaryTelemetry(CONFIG)

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "engine.log",
    rotation="100 MB",
    retention="90 days",
    level="DEBUG"
)


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """Request model for fiduciary duty query"""
    query: str = Field(..., description="Fiduciary duty question or scenario")
    response_mode: str = Field(default="DEFENSE", description="Response mode: FAST, DEFENSE, or MEMO")
    position_zone: Optional[str] = Field(default="AUDIT", description="Position zone: PLANNING, REPORTING, or AUDIT")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class DoctrineMatch(BaseModel):
    """Doctrine block match"""
    topic: str
    confidence: str
    relevance_score: float
    conclusion: str
    reasoning: str
    authorities: List[str]


class QueryResponse(BaseModel):
    """Response model for fiduciary duty query"""
    query_id: str
    timestamp: str
    query: str
    response_text: str
    response_mode: str
    position_zone: str
    layer_used: str
    doctrine_matches: List[DoctrineMatch]
    issue_categories: List[str]
    confidence_level: str
    citations: List[str]
    authorities: List[str]
    key_factors: List[str]
    counter_arguments: List[str]
    resolution_strategy: str
    determinism_hash: str
    latency_ms: float
    metadata: Dict[str, Any]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    health_score: int
    engine_id: str
    version: str
    uptime_seconds: float
    total_queries: int
    error_rate: float
    performance_metrics: Dict[str, Any]
    coverage_metrics: Dict[str, Any]
    drift_metrics: Dict[str, Any]
    recommendations: List[str]


# ============================================================================
# CORE ENGINE LOGIC - TIE-20 COMPONENTS
# ============================================================================

class FiduciaryDutyEngine:
    """Main fiduciary duty intelligence engine with TIE-20 components"""

    def __init__(self):
        self.doctrines = FIDUCIARY_DOCTRINES
        self.semantic = semantic_normalizer
        self.search = vector_search
        self.telemetry = telemetry
        self.config = CONFIG

        # Build doctrine index
        self.doctrine_index = self._build_doctrine_index()

        logger.info(f"Fiduciary Duty Engine initialized with {len(self.doctrines)} doctrine blocks")

    def _build_doctrine_index(self) -> Dict[str, List[DoctrineBlock]]:
        """Build searchable index of doctrines by keywords"""
        index = {}
        for doctrine in self.doctrines:
            for keyword in doctrine.keywords:
                if keyword not in index:
                    index[keyword] = []
                index[keyword].append(doctrine)
        return index

    def three_layer_response(
        self,
        query: str,
        response_mode: str = "DEFENSE",
        position_zone: str = "AUDIT",
        context: Optional[Dict[str, Any]] = None
    ) -> QueryResponse:
        """
        TIE-20 Component #1: Three-layer response system
        Layer 1: Doctrine Cache (0-200ms)
        Layer 2: Semantic Retrieval (200-2000ms)
        Layer 3: Deep Analysis (2000-8000ms)
        """
        start_time = datetime.utcnow()
        query_id = self._generate_query_id(query)

        # Normalize query
        normalized_query = self.semantic.normalize_query(query)
        key_concepts = self.semantic.identify_key_concepts(query)

        # Layer 1: Doctrine Cache
        cache_start = datetime.utcnow()
        doctrine_matches = self._search_doctrine_cache(normalized_query, key_concepts)
        cache_latency = (datetime.utcnow() - cache_start).total_seconds() * 1000

        layer_used = None
        response_text = ""
        retrieval_latency = 0.0
        analysis_latency = 0.0

        if doctrine_matches and cache_latency < self.config["telemetry"]["latency_thresholds_ms"]["doctrine_cache"]:
            # Cache hit - use doctrine cache
            layer_used = QueryLayer.DOCTRINE_CACHE.value
            response_text = self._format_doctrine_response(
                doctrine_matches, response_mode, position_zone, query
            )
            logger.info(f"Cache hit: {len(doctrine_matches)} doctrines matched in {cache_latency:.0f}ms")

        elif response_mode == "DEFENSE":
            # Layer 2: Semantic Retrieval
            retrieval_start = datetime.utcnow()
            layer_used = QueryLayer.SEMANTIC_RETRIEVAL.value
            semantic_results = self.search.search(query, top_k=5)
            response_text = self._format_semantic_response(
                doctrine_matches, semantic_results, response_mode, position_zone, query
            )
            retrieval_latency = (datetime.utcnow() - retrieval_start).total_seconds() * 1000
            logger.info(f"Semantic retrieval: {len(semantic_results)} results in {retrieval_latency:.0f}ms")

        else:  # MEMO mode or cache miss requiring deep analysis
            # Layer 3: Deep Analysis
            analysis_start = datetime.utcnow()
            layer_used = QueryLayer.DEEP_ANALYSIS.value
            response_text = self._deep_analysis_mode(
                query, normalized_query, doctrine_matches, context
            )
            analysis_latency = (datetime.utcnow() - analysis_start).total_seconds() * 1000
            logger.info(f"Deep analysis completed in {analysis_latency:.0f}ms")

        # Extract metadata
        issue_categories = self._identify_issue_categories(query, doctrine_matches)
        confidence_level = self._assess_confidence(doctrine_matches, layer_used)
        citations = self._extract_citations(doctrine_matches)
        authorities = self._extract_authorities(doctrine_matches)
        key_factors = self._extract_key_factors(doctrine_matches)
        counter_arguments = self._extract_counter_arguments(doctrine_matches)
        resolution_strategy = self._synthesize_resolution_strategy(doctrine_matches)

        # Apply epistemic guardrails
        response_text = self._apply_epistemic_guardrails(
            response_text, confidence_level, issue_categories
        )

        # Generate determinism hash
        determinism_hash = telemetry.generate_determinism_hash(query, response_text)

        # Calculate total latency
        total_latency = (datetime.utcnow() - start_time).total_seconds() * 1000

        # Build response
        response = QueryResponse(
            query_id=query_id,
            timestamp=datetime.utcnow().isoformat(),
            query=query,
            response_text=response_text,
            response_mode=response_mode,
            position_zone=position_zone,
            layer_used=layer_used,
            doctrine_matches=self._format_doctrine_matches(doctrine_matches),
            issue_categories=issue_categories,
            confidence_level=confidence_level,
            citations=citations,
            authorities=authorities,
            key_factors=key_factors,
            counter_arguments=counter_arguments,
            resolution_strategy=resolution_strategy,
            determinism_hash=determinism_hash,
            latency_ms=total_latency,
            metadata={
                "doctrines_triggered": len(doctrine_matches),
                "cache_latency_ms": cache_latency,
                "retrieval_latency_ms": retrieval_latency,
                "analysis_latency_ms": analysis_latency,
                "key_concepts": key_concepts
            }
        )

        # Record telemetry
        self._record_telemetry(response, cache_latency, retrieval_latency, analysis_latency)

        return response

    def _search_doctrine_cache(
        self,
        normalized_query: str,
        key_concepts: List[str]
    ) -> List[DoctrineBlock]:
        """Search doctrine cache for matching blocks"""
        matches = []
        scored_doctrines = []

        for doctrine in self.doctrines:
            score = 0.0

            # Keyword matching
            for keyword in doctrine.keywords:
                if keyword.lower() in normalized_query:
                    score += 1.0

            # Concept matching
            for concept in key_concepts:
                if concept in doctrine.keywords:
                    score += 0.5

            # Topic matching
            if doctrine.topic.replace("_", " ") in normalized_query:
                score += 2.0

            if score > 0:
                scored_doctrines.append((doctrine, score))

        # Sort by score and return top matches
        scored_doctrines.sort(key=lambda x: x[1], reverse=True)
        matches = [d[0] for d in scored_doctrines[:5]]

        return matches

    def _format_doctrine_response(
        self,
        doctrines: List[DoctrineBlock],
        response_mode: str,
        position_zone: str,
        query: str
    ) -> str:
        """Format response from doctrine cache matches"""
        if response_mode == "FAST":
            # Concise response (150 tokens target)
            if doctrines:
                primary = doctrines[0]
                return f"{' '.join(primary.conclusion_template)}\n\nKey Authority: {primary.primary_authority[0]}"
            return "No matching doctrine found. Further analysis required."

        elif response_mode == "DEFENSE":
            # Audit-ready response (800 tokens target)
            sections = []

            # Executive summary
            if doctrines:
                sections.append("FIDUCIARY DUTY ANALYSIS\n")
                sections.append(' '.join(doctrines[0].conclusion_template))

            # Applicable doctrines
            sections.append("\n\nAPPLICABLE LEGAL FRAMEWORK:")
            for i, doctrine in enumerate(doctrines[:3], 1):
                sections.append(f"\n{i}. {doctrine.topic.replace('_', ' ').title()}")
                sections.append(f"   Standard: {doctrine.confidence}")
                sections.append(f"   Authority: {doctrine.primary_authority[0]}")

            # Key factors
            sections.append("\n\nKEY FACTORS FOR ANALYSIS:")
            all_factors = []
            for doctrine in doctrines:
                all_factors.extend(doctrine.key_factors[:3])
            for i, factor in enumerate(list(set(all_factors))[:5], 1):
                sections.append(f"{i}. {factor}")

            # Burden allocation
            if doctrines:
                sections.append(f"\n\nBURDEN OF PROOF: {doctrines[0].burden_holder}")

            return '\n'.join(sections)

        else:  # MEMO mode
            # Full memorandum (2000 tokens target)
            sections = []

            sections.append("MEMORANDUM\n")
            sections.append(f"RE: Fiduciary Duty Analysis\n")
            sections.append(f"DATE: {datetime.utcnow().strftime('%B %d, %Y')}\n")

            sections.append("\nQUESTION PRESENTED:")
            sections.append(query)

            sections.append("\n\nBRIEF ANSWER:")
            if doctrines:
                sections.append(' '.join(doctrines[0].conclusion_template))

            sections.append("\n\nDISCUSSION:")
            for i, doctrine in enumerate(doctrines[:3], 1):
                sections.append(f"\n{i}. {doctrine.topic.replace('_', ' ').title()}")
                sections.append(f"\n{doctrine.reasoning_framework}")
                sections.append(f"\nKey Factors:")
                for factor in doctrine.key_factors[:5]:
                    sections.append(f"  - {factor}")
                sections.append(f"\nPrimary Authority:")
                for auth in doctrine.primary_authority:
                    sections.append(f"  - {auth}")

            sections.append("\n\nCONCLUSION:")
            if doctrines:
                sections.append(f"{doctrines[0].resolution_strategy}")

            return '\n'.join(sections)

    def _format_semantic_response(
        self,
        doctrine_matches: List[DoctrineBlock],
        semantic_results: List[Dict[str, Any]],
        response_mode: str,
        position_zone: str,
        query: str
    ) -> str:
        """Format response combining doctrine cache and semantic retrieval"""
        sections = []

        sections.append("FIDUCIARY DUTY ANALYSIS (Semantic Retrieval)\n")

        # Include doctrine matches if any
        if doctrine_matches:
            sections.append("Relevant Doctrine:")
            sections.append(' '.join(doctrine_matches[0].conclusion_template))

        # Add semantic retrieval results
        sections.append("\n\nAdditional Authority:")
        for i, result in enumerate(semantic_results[:3], 1):
            sections.append(f"\n{i}. {result['content']}")
            sections.append(f"   Source: {result['source']}")
            if result.get('citations'):
                sections.append(f"   Citations: {', '.join(result['citations'][:2])}")

        # Synthesis
        sections.append("\n\nANALYSIS:")
        sections.append("Based on the applicable statutory framework and case law, ")
        sections.append("the fiduciary's conduct should be evaluated against the relevant duty standards. ")

        if doctrine_matches:
            sections.append(f"\n\nKey Factors: {', '.join(doctrine_matches[0].key_factors[:5])}")

        return ''.join(sections)

    def _deep_analysis_mode(
        self,
        query: str,
        normalized_query: str,
        doctrine_matches: List[DoctrineBlock],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """
        TIE-20 Component #20: Deep analysis mode
        Multi-source synthesis with full reasoning chain
        """
        sections = []

        sections.append("COMPREHENSIVE FIDUCIARY DUTY ANALYSIS\n")
        sections.append("="* 60)

        # Multi-doctrine decomposition
        issue_categories = self._identify_issue_categories(query, doctrine_matches)
        sections.append(f"\n\nISSUE CATEGORIZATION:")
        for category in issue_categories:
            sections.append(f"  - {category}")

        # Doctrine interaction analysis
        if len(doctrine_matches) > 1:
            sections.append("\n\nDOCTRINE INTERACTION ANALYSIS:")
            sections.append("Multiple fiduciary duties implicated. Interaction effects:")
            for i, doctrine in enumerate(doctrine_matches[:3], 1):
                sections.append(f"\n  {i}. {doctrine.topic.replace('_', ' ').title()}")
                sections.append(f"     Confidence: {doctrine.confidence_stratification}")

        # Detailed reasoning framework
        sections.append("\n\nDETAILED REASONING FRAMEWORK:")
        if doctrine_matches:
            primary = doctrine_matches[0]
            sections.append(primary.reasoning_framework)

        # Fact fragility scoring
        sections.append("\n\nFACT-DEPENDENT ANALYSIS:")
        sections.append("The following factual elements are critical to the outcome:")
        if doctrine_matches:
            for i, factor in enumerate(doctrine_matches[0].key_factors[:7], 1):
                sections.append(f"  {i}. {factor}")

        # Adversarial analysis
        sections.append("\n\nADVERSARIAL POSITIONS:")
        if doctrine_matches:
            sections.append(f"\nBeneficiary Position: {doctrine_matches[0].adversary_position}")
            sections.append(f"\nFiduciary Counter-Arguments:")
            for i, counter in enumerate(doctrine_matches[0].counter_arguments, 1):
                sections.append(f"  {i}. {counter}")

        # Resolution strategy
        sections.append("\n\nRESOLUTION STRATEGY:")
        if doctrine_matches:
            sections.append(doctrine_matches[0].resolution_strategy)

        # Authority compilation
        sections.append("\n\nCOMPREHENSIVE AUTHORITY:")
        all_authorities = []
        for doctrine in doctrine_matches:
            all_authorities.extend(doctrine.primary_authority)
        for i, auth in enumerate(list(set(all_authorities))[:10], 1):
            sections.append(f"  {i}. {auth}")

        return '\n'.join(sections)

    def _identify_issue_categories(
        self,
        query: str,
        doctrines: List[DoctrineBlock]
    ) -> List[str]:
        """Identify issue categories from query and matched doctrines"""
        categories = set()

        # Map doctrine topics to categories
        category_map = {
            "executor": "EXECUTOR_DUTIES",
            "trustee": "TRUSTEE_DUTIES",
            "guardian": "GUARDIAN_DUTIES",
            "breach": "BREACH_ANALYSIS",
            "surcharge": "SURCHARGE_LIABILITY",
            "removal": "REMOVAL_GROUNDS",
            "self_dealing": "SELF_DEALING",
            "conflict": "CONFLICT_INTEREST",
            "investment": "INVESTMENT_PRUDENCE",
            "accounting": "ACCOUNTING_DISCLOSURE",
            "corporate": "CORPORATE_FIDUCIARY",
            "exculpatory": "EXCULPATORY_CLAUSES"
        }

        query_lower = query.lower()
        for keyword, category in category_map.items():
            if keyword in query_lower:
                categories.add(category)

        for doctrine in doctrines:
            topic_lower = doctrine.topic.lower()
            for keyword, category in category_map.items():
                if keyword in topic_lower:
                    categories.add(category)

        return list(categories) if categories else ["EXECUTOR_DUTIES"]

    def _assess_confidence(self, doctrines: List[DoctrineBlock], layer: str) -> str:
        """Assess overall confidence level"""
        if not doctrines:
            return "HIGH_RISK"

        # Use primary doctrine's confidence
        primary_confidence = doctrines[0].confidence

        # Downgrade if deep analysis layer (more uncertain)
        if layer == QueryLayer.DEEP_ANALYSIS.value and primary_confidence == "DEFENSIBLE":
            return "AGGRESSIVE"

        return primary_confidence

    def _extract_citations(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract all citations from matched doctrines"""
        citations = []
        for doctrine in doctrines:
            citations.extend(doctrine.primary_authority)
            if doctrine.controlling_precedent:
                citations.append(doctrine.controlling_precedent)
        return list(set(citations))

    def _extract_authorities(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract primary authorities"""
        authorities = []
        for doctrine in doctrines[:3]:
            authorities.extend(doctrine.primary_authority[:2])
        return list(set(authorities))

    def _extract_key_factors(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract key factors from doctrines"""
        factors = []
        for doctrine in doctrines[:2]:
            factors.extend(doctrine.key_factors[:5])
        return list(set(factors))[:10]

    def _extract_counter_arguments(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract counter-arguments from doctrines"""
        counters = []
        for doctrine in doctrines[:2]:
            counters.extend(doctrine.counter_arguments[:3])
        return list(set(counters))[:8]

    def _synthesize_resolution_strategy(self, doctrines: List[DoctrineBlock]) -> str:
        """Synthesize resolution strategy from matched doctrines"""
        if not doctrines:
            return "Conduct comprehensive factual investigation and legal research."
        return doctrines[0].resolution_strategy

    def _apply_epistemic_guardrails(
        self,
        response_text: str,
        confidence_level: str,
        issue_categories: List[str]
    ) -> str:
        """
        Apply epistemic guardrails to ensure appropriate disclosure
        """
        guardrails = self.config.get("epistemic_guardrails", {})

        disclosures = []

        # Novel duty theory warning
        if confidence_level == "HIGH_RISK" and guardrails.get("flag_novel_duty_theories"):
            disclosures.append(
                "\n\n[DISCLOSURE: This analysis involves novel or unsettled duty theories. "
                "Outcome uncertain pending further case law development.]"
            )

        # Exculpatory clause impact
        if "EXCULPATORY_CLAUSES" in issue_categories and guardrails.get("disclose_exculpatory_clause_impact"):
            disclosures.append(
                "\n\n[NOTE: Exculpatory clauses may limit liability. Review trust instrument carefully.]"
            )

        # Corporate trustee standard
        if "CORPORATE_FIDUCIARY" in issue_categories and guardrails.get("warn_corporate_trustee_higher_standard"):
            disclosures.append(
                "\n\n[NOTE: Corporate fiduciaries held to higher professional standard. "
                "Industry best practices and expertise expected.]"
            )

        return response_text + ''.join(disclosures)

    def _format_doctrine_matches(self, doctrines: List[DoctrineBlock]) -> List[DoctrineMatch]:
        """Format doctrine matches for response"""
        return [
            DoctrineMatch(
                topic=d.topic,
                confidence=d.confidence,
                relevance_score=1.0 / (i + 1),  # Simple scoring
                conclusion=' '.join(d.conclusion_template),
                reasoning=d.reasoning_framework[:500],
                authorities=d.primary_authority
            )
            for i, d in enumerate(doctrines)
        ]

    def _generate_query_id(self, query: str) -> str:
        """Generate unique query ID"""
        timestamp = datetime.utcnow().isoformat()
        combined = f"{timestamp}_{query}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def _record_telemetry(
        self,
        response: QueryResponse,
        cache_latency: float,
        retrieval_latency: float,
        analysis_latency: float
    ) -> None:
        """Record query metrics to telemetry system"""
        metrics = QueryMetrics(
            query_id=response.query_id,
            timestamp=response.timestamp,
            query_text=response.query,
            query_hash=hashlib.sha256(response.query.encode()).hexdigest(),
            layer_used=response.layer_used,
            response_mode=response.response_mode,
            issue_categories=response.issue_categories,
            doctrines_triggered=[d.topic for d in response.doctrine_matches],
            confidence_level=response.confidence_level,
            total_latency_ms=response.latency_ms,
            cache_latency_ms=cache_latency,
            retrieval_latency_ms=retrieval_latency,
            analysis_latency_ms=analysis_latency,
            response_length=len(response.response_text),
            citations_count=len(response.citations),
            cache_hit=response.layer_used == QueryLayer.DOCTRINE_CACHE.value,
            error=None
        )

        self.telemetry.record_query(metrics)


# Initialize engine
engine = FiduciaryDutyEngine()


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.post("/query", response_model=QueryResponse)
async def query_fiduciary_duty(request: QueryRequest):
    """
    Analyze fiduciary duty question

    Returns comprehensive analysis with doctrine matches, authorities, and resolution strategy.
    """
    try:
        logger.info(f"Query received: {request.query[:100]}")

        response = engine.three_layer_response(
            query=request.query,
            response_mode=request.response_mode,
            position_zone=request.position_zone or "AUDIT",
            context=request.context
        )

        logger.info(f"Query processed: {response.query_id} in {response.latency_ms:.0f}ms")
        return response

    except Exception as e:
        logger.error(f"Query processing failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Comprehensive health check with performance metrics
    """
    try:
        health = telemetry.get_health_status()

        return HealthResponse(
            status=health["status"],
            health_score=health["health_score"],
            engine_id=CONFIG["engine_id"],
            version=CONFIG["version"],
            uptime_seconds=(datetime.utcnow() - telemetry.session_start).total_seconds(),
            total_queries=telemetry.total_queries,
            error_rate=health["metrics_summary"]["error_rate"],
            performance_metrics=health["metrics_summary"],
            coverage_metrics=health["coverage_summary"],
            drift_metrics=health["drift_summary"],
            recommendations=health["recommendations"]
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Get current performance metrics"""
    try:
        return JSONResponse(content=telemetry.get_performance_metrics())
    except Exception as e:
        logger.error(f"Metrics retrieval failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/coverage")
async def get_coverage():
    """Get doctrine coverage statistics"""
    try:
        return JSONResponse(content=telemetry.get_doctrine_coverage())
    except Exception as e:
        logger.error(f"Coverage retrieval failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/drift")
async def get_drift_analysis():
    """Get doctrine drift analysis"""
    try:
        return JSONResponse(content=telemetry.get_drift_analysis())
    except Exception as e:
        logger.error(f"Drift analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    try:
        doctrines_list = [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence,
                "entity_scope": d.entity_scope,
                "primary_authority": d.primary_authority[0] if d.primary_authority else None
            }
            for d in FIDUCIARY_DOCTRINES
        ]
        return JSONResponse(content={"total": len(doctrines_list), "doctrines": doctrines_list})
    except Exception as e:
        logger.error(f"Doctrine listing failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/categories")
async def list_categories():
    """List issue categories with stats"""
    try:
        categories = [
            {
                "category": cat,
                "query_count": telemetry.category_counts.get(cat, 0)
            }
            for cat in CONFIG["issue_categories"]
        ]
        return JSONResponse(content={"categories": categories})
    except Exception as e:
        logger.error(f"Category listing failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint with engine info"""
    return {
        "engine": CONFIG["engine_name"],
        "version": CONFIG["version"],
        "domain": CONFIG["domain"],
        "jurisdiction": CONFIG["jurisdiction"],
        "mode": CONFIG["mode"],
        "port": CONFIG["port"],
        "doctrine_count": len(FIDUCIARY_DOCTRINES),
        "endpoints": [
            "/query",
            "/health",
            "/metrics",
            "/coverage",
            "/drift",
            "/doctrines",
            "/categories"
        ]
    }


# ============================================================================
# STARTUP AND SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Engine startup"""
    logger.info("="* 60)
    logger.info(f"P07 Fiduciary Duty Engine v{CONFIG['version']} starting...")
    logger.info(f"Port: {CONFIG['port']}")
    logger.info(f"Mode: {CONFIG['mode']}")
    logger.info(f"Doctrines loaded: {len(FIDUCIARY_DOCTRINES)}")
    logger.info("="* 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Engine shutdown"""
    logger.info("Fiduciary Duty Engine shutting down...")

    # Export final metrics
    metrics_export_path = Path(__file__).parent / "final_metrics.json"
    telemetry.export_metrics(metrics_export_path)
    logger.info(f"Final metrics exported to {metrics_export_path}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=CONFIG["port"],
        reload=False,
        log_level="info"
    )
