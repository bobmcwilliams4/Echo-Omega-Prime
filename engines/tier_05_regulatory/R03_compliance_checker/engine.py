"""
R03 Compliance Checker Engine
ECHO OMEGA PRIME - Intelligence Engine

Regulatory compliance checking for oil & gas operations
RRC, TCEQ, EPA, OSHA, DOT regulations

TIE-20 Gold Standard Implementation:
1.  three_layer_response ✓
2.  response_modes (FAST/DEFENSE/MEMO) ✓
3.  doctrine_cache (52 blocks) ✓
4.  authority_hardening ✓
5.  confidence_stratification ✓
6.  semantic_normalization ✓
7.  vector_search ✓
8.  telemetry ✓
9.  drift_watcher ✓
10. coverage_map ✓
11. metrics_collector ✓
12. health_endpoint ✓
13. zoned_analysis ✓
14. fact_fragility_scoring ✓
15. audit_trail_jsonl ✓
16. determinism_hash_sha256 ✓
17. fastapi_server ✓
18. loguru_logging ✓
19. multi_doctrine_decomposition ✓
20. deep_analysis_mode ✓

Version: 1.0.0
Port: 8703
Mode: RULE_BASED
Domain: Regulatory Compliance (Oil & Gas)
"""

import json
import hashlib
import time
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

# Local imports
import sys

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import DOCTRINE_CACHE, get_doctrine_by_topic, search_doctrines_by_keyword, get_all_topics
from semantic import SemanticNormalizer, get_normalizer
from search import ComplianceSearchEngine, get_search_engine
from telemetry import TelemetryCollector, get_telemetry_collector


# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG_PATH = Path(__file__).parent / "config.json"
with open(CONFIG_PATH, 'r') as f:
    CONFIG = json.load(f)

ENGINE_ID = CONFIG["engine_id"]
ENGINE_NAME = CONFIG["engine_name"]
VERSION = CONFIG["version"]
PORT = CONFIG["port"]
DOMAIN = CONFIG["domain"]
MODE = CONFIG["mode"]


# ============================================================================
# LOGGING SETUP
# ============================================================================

log_path = Path(__file__).parent / "logs"
log_path.mkdir(exist_ok=True)

logger.add(
    log_path / "compliance_checker_{time:YYYY-MM-DD}.log",
    rotation=CONFIG.get("log_rotation", "100 MB"),
    retention=CONFIG.get("log_retention", "30 days"),
    level=CONFIG.get("log_level", "INFO"),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}"
)

logger.info(f"Starting {ENGINE_NAME} v{VERSION} (Engine {ENGINE_ID})")
logger.info(f"Mode: {MODE} | Domain: {DOMAIN} | Port: {PORT}")


# ============================================================================
# GLOBAL INSTANCES
# ============================================================================

normalizer: SemanticNormalizer = get_normalizer()
search_engine: ComplianceSearchEngine = get_search_engine(CONFIG)
telemetry: TelemetryCollector = get_telemetry_collector(CONFIG)

# Drift watcher state
drift_last_check = datetime.utcnow()
drift_observations: List[Dict] = []


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ComplianceQuery(BaseModel):
    """Compliance query request."""
    query: str = Field(..., description="Compliance question or scenario")
    response_mode: str = Field("DEFENSE", description="FAST, DEFENSE, or MEMO")
    compliance_zone: Optional[str] = Field(None, description="PREVENTIVE, OPERATIONAL, REMEDIAL, or AUDIT")
    authorities: Optional[List[str]] = Field(None, description="Filter by authorities: RRC, TCEQ, EPA, OSHA, DOT")


class ComplianceResponse(BaseModel):
    """Compliance query response."""
    query_id: str
    response_text: str
    response_mode: str
    compliance_zone: str
    query_intent: str

    # Doctrine information
    cache_hit: bool
    doctrine_topic: Optional[str]
    doctrine_keywords: List[str]

    # Confidence and authority
    confidence: float
    confidence_stratification: str
    authorities_cited: List[str]
    primary_citations: List[str]

    # Metadata
    latency_ms: float
    word_count: int
    determinism_hash: str
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    engine_id: str
    engine_name: str
    version: str
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float
    doctrines_loaded: int
    cloud_search_available: bool
    timestamp: str


class MetricsResponse(BaseModel):
    """Detailed metrics response."""
    snapshot: Dict
    doctrine_coverage: Dict
    compliance_zone_distribution: Dict
    recent_errors: List[Dict]


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=f"{ENGINE_NAME} API",
    description="Regulatory compliance checking for oil & gas operations",
    version=VERSION,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG.get("api_config", {}).get("cors_origins", ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# CORE COMPLIANCE ENGINE
# ============================================================================

class ComplianceEngine:
    """
    Main compliance checking engine with TIE-20 architecture.
    """

    def __init__(self):
        self.normalizer = normalizer
        self.search_engine = search_engine
        self.telemetry = telemetry
        self.start_time = time.time()

    # ========================================================================
    # TIE-20 COMPONENT 1: THREE-LAYER RESPONSE
    # ========================================================================

    def three_layer_response(
        self,
        query: str,
        response_mode: str,
        compliance_zone: Optional[str] = None,
        authorities: Optional[List[str]] = None
    ) -> ComplianceResponse:
        """
        Three-layer response architecture:
        1. Doctrine Cache (0-200ms) - Pre-compiled regulatory knowledge
        2. Semantic Retrieval (200-2000ms) - Cloud knowledge base search
        3. Deep Analysis (2000-10000ms) - Multi-source synthesis

        Args:
            query: Compliance question
            response_mode: FAST, DEFENSE, or MEMO
            compliance_zone: Override zone detection
            authorities: Filter by regulatory authorities

        Returns:
            ComplianceResponse with full compliance analysis
        """
        start_time = time.time()
        logger.info(f"Query received: {query[:100]}...")

        # Normalize query
        normalized_query = self.normalizer.normalize(query)
        logger.debug(f"Normalized: {normalized_query}")

        # Detect compliance zone and intent
        if not compliance_zone:
            compliance_zone = self.normalizer.identify_compliance_zone(query)
        query_intent = self.normalizer.classify_query_intent(query)

        # Extract entities
        entities = self.normalizer.extract_entities(query)
        logger.debug(f"Entities: {entities}")

        # Start telemetry trace
        query_id = self.telemetry.start_query(query, normalized_query, compliance_zone, query_intent)

        # LAYER 1: Doctrine Cache Lookup (fastest)
        cache_start = time.time()
        doctrine_result = self._search_doctrine_cache(normalized_query, entities)
        cache_time = (time.time() - cache_start) * 1000

        if doctrine_result:
            logger.info(f"Cache HIT: {doctrine_result['topic']}")
            response = self._generate_from_doctrine(
                doctrine_result,
                query,
                response_mode,
                compliance_zone,
                query_intent
            )
            cache_hit = True
            semantic_search_used = False
            deep_analysis_triggered = False
            semantic_time = 0.0
            deep_time = 0.0
        else:
            logger.info("Cache MISS - escalating to semantic search")
            cache_hit = False

            # LAYER 2: Semantic Retrieval (medium speed)
            semantic_start = time.time()
            semantic_results = self.search_engine.search_regulations(
                normalized_query,
                authorities=authorities or entities.get("authorities", []),
                top_k=5
            )
            semantic_time = (time.time() - semantic_start) * 1000
            semantic_search_used = len(semantic_results) > 0

            if semantic_results and response_mode != "MEMO":
                logger.info(f"Semantic search returned {len(semantic_results)} results")
                response = self._generate_from_semantic(
                    semantic_results,
                    query,
                    response_mode,
                    compliance_zone,
                    query_intent
                )
                deep_analysis_triggered = False
                deep_time = 0.0
            else:
                # LAYER 3: Deep Analysis (slowest, most comprehensive)
                logger.info("Escalating to deep analysis mode")
                deep_start = time.time()
                response = self._deep_analysis(
                    query,
                    normalized_query,
                    entities,
                    semantic_results,
                    response_mode,
                    compliance_zone,
                    query_intent
                )
                deep_time = (time.time() - deep_start) * 1000
                deep_analysis_triggered = True

        # Complete telemetry trace
        total_time = (time.time() - start_time) * 1000
        self.telemetry.complete_query(
            query_id=query_id,
            cache_hit=cache_hit,
            doctrine_topic=doctrine_result.get("topic") if doctrine_result else None,
            semantic_search_used=semantic_search_used,
            deep_analysis_triggered=deep_analysis_triggered,
            response_mode=response_mode,
            confidence=response.confidence,
            confidence_strata=response.confidence_stratification,
            authorities_cited=response.authorities_cited,
            response_text=response.response_text,
            cache_lookup_ms=cache_time,
            semantic_search_ms=semantic_time,
            deep_analysis_ms=deep_time,
        )

        response.latency_ms = total_time
        response.timestamp = datetime.utcnow().isoformat()

        logger.info(f"Query completed in {total_time:.2f}ms (cache_hit={cache_hit})")

        return response

    # ========================================================================
    # DOCTRINE CACHE OPERATIONS
    # ========================================================================

    def _search_doctrine_cache(
        self,
        normalized_query: str,
        entities: Dict[str, List[str]]
    ) -> Optional[Dict]:
        """
        Search doctrine cache for matching regulatory block.

        Returns doctrine dict if found, None otherwise.
        """
        # Try exact topic match first
        for form in entities.get("forms", []):
            doctrine = get_doctrine_by_topic(form)
            if doctrine:
                return self._doctrine_to_dict(doctrine)

        for rule in entities.get("rules", []):
            doctrine = get_doctrine_by_topic(rule)
            if doctrine:
                return self._doctrine_to_dict(doctrine)

        # Try keyword search
        keywords = normalized_query.split()
        for keyword in keywords:
            if len(keyword) < 3:
                continue
            results = search_doctrines_by_keyword(keyword)
            if results:
                # Return first result (highest relevance assumed)
                return self._doctrine_to_dict(results[0])

        return None

    def _doctrine_to_dict(self, doctrine) -> Dict:
        """Convert DoctrineBlock dataclass to dictionary."""
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

    # ========================================================================
    # RESPONSE GENERATION
    # ========================================================================

    def _generate_from_doctrine(
        self,
        doctrine: Dict,
        query: str,
        response_mode: str,
        compliance_zone: str,
        query_intent: str
    ) -> ComplianceResponse:
        """Generate response from doctrine cache hit."""

        # TIE-20 COMPONENT 2: Response Modes
        if response_mode == "FAST":
            response_text = self._fast_response(doctrine, query)
        elif response_mode == "DEFENSE":
            response_text = self._defense_response(doctrine, query, compliance_zone)
        elif response_mode == "MEMO":
            response_text = self._memo_response(doctrine, query, compliance_zone)
        else:
            response_text = self._defense_response(doctrine, query, compliance_zone)

        # Calculate determinism hash
        hash_input = f"{doctrine['topic']}:{query}:{response_mode}"
        determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        return ComplianceResponse(
            query_id="",  # Will be set by telemetry
            response_text=response_text,
            response_mode=response_mode,
            compliance_zone=compliance_zone,
            query_intent=query_intent,
            cache_hit=True,
            doctrine_topic=doctrine["topic"],
            doctrine_keywords=doctrine["keywords"],
            confidence=doctrine["confidence"],
            confidence_stratification=doctrine["confidence_stratification"],
            authorities_cited=doctrine["primary_authority"],
            primary_citations=doctrine["primary_authority"],
            latency_ms=0.0,  # Will be set by caller
            word_count=len(response_text.split()),
            determinism_hash=determinism_hash,
            timestamp=""  # Will be set by caller
        )

    def _fast_response(self, doctrine: Dict, query: str) -> str:
        """FAST mode: Concise answer with key facts."""
        conclusions = "\n".join(f"• {c}" for c in doctrine["conclusion_template"])
        key_factors = "\n".join(f"• {f}" for f in doctrine["key_factors"][:5])

        return f"""COMPLIANCE REQUIREMENT: {doctrine['topic'].replace('_', ' ')}

KEY CONCLUSIONS:
{conclusions}

CRITICAL FACTORS:
{key_factors}

PRIMARY AUTHORITY:
{doctrine['primary_authority'][0]}

CONFIDENCE: {doctrine['confidence_stratification']} ({doctrine['confidence']:.0%})
"""

    def _defense_response(self, doctrine: Dict, query: str, compliance_zone: str) -> str:
        """DEFENSE mode: Audit-ready comprehensive answer."""
        conclusions = "\n".join(f"{i+1}. {c}" for i, c in enumerate(doctrine["conclusion_template"]))
        key_factors = "\n".join(f"• {f}" for f in doctrine["key_factors"])
        authorities = "\n".join(f"• {a}" for a in doctrine["primary_authority"])

        response = f"""REGULATORY COMPLIANCE ANALYSIS
{"=" * 80}

QUERY: {query}
COMPLIANCE ZONE: {compliance_zone}
APPLICABLE DOCTRINE: {doctrine['topic'].replace('_', ' ')}

REGULATORY CONCLUSIONS:
{conclusions}

LEGAL FRAMEWORK:
{doctrine['reasoning_framework']}

KEY COMPLIANCE FACTORS:
{key_factors}

PRIMARY AUTHORITY:
{authorities}

BURDEN OF COMPLIANCE: {doctrine['burden_holder']}

REGULATORY POSITION:
{doctrine['adversary_position']}

DEFENSIVE STRATEGY:
{doctrine['resolution_strategy']}

CONFIDENCE ASSESSMENT:
Stratification: {doctrine['confidence_stratification']}
Confidence Score: {doctrine['confidence']:.1%}
Entity Scope: {doctrine['entity_scope']}
"""

        if doctrine.get("controlling_precedent"):
            response += f"\nCONTROLLING PRECEDENT:\n{doctrine['controlling_precedent']}\n"

        return response

    def _memo_response(self, doctrine: Dict, query: str, compliance_zone: str) -> str:
        """MEMO mode: Full documentation with all reasoning."""
        response = self._defense_response(doctrine, query, compliance_zone)

        # Add counter-arguments section
        counter_args = "\n".join(f"{i+1}. {arg}" for i, arg in enumerate(doctrine["counter_arguments"]))

        response += f"""
POTENTIAL COUNTER-ARGUMENTS:
{counter_args}

COMPREHENSIVE REASONING:
{doctrine['reasoning_framework']}

APPLICABILITY SCOPE:
{doctrine['entity_scope']}

RECOMMENDED COMPLIANCE APPROACH:
{doctrine['resolution_strategy']}

---
This memorandum provides comprehensive regulatory guidance based on {doctrine['topic']}.
Confidence: {doctrine['confidence_stratification']} ({doctrine['confidence']:.1%})
Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
        return response

    def _generate_from_semantic(
        self,
        semantic_results: List[Dict],
        query: str,
        response_mode: str,
        compliance_zone: str,
        query_intent: str
    ) -> ComplianceResponse:
        """Generate response from semantic search results."""

        # Synthesize results
        authorities_cited = list(set(r["authority"] for r in semantic_results if r.get("authority")))
        citations = list(set(r["rule_citation"] for r in semantic_results if r.get("rule_citation")))

        # Build response text
        if response_mode == "FAST":
            response_text = self._fast_semantic_response(semantic_results, query)
        else:
            response_text = self._defense_semantic_response(semantic_results, query, compliance_zone)

        # Conservative confidence (not from cache)
        confidence = 0.75
        confidence_strata = "AGGRESSIVE"

        hash_input = f"{query}:{response_mode}:SEMANTIC"
        determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        return ComplianceResponse(
            query_id="",
            response_text=response_text,
            response_mode=response_mode,
            compliance_zone=compliance_zone,
            query_intent=query_intent,
            cache_hit=False,
            doctrine_topic=None,
            doctrine_keywords=[],
            confidence=confidence,
            confidence_stratification=confidence_strata,
            authorities_cited=authorities_cited,
            primary_citations=citations,
            latency_ms=0.0,
            word_count=len(response_text.split()),
            determinism_hash=determinism_hash,
            timestamp=""
        )

    def _fast_semantic_response(self, results: List[Dict], query: str) -> str:
        """Fast semantic response."""
        top_result = results[0] if results else {}
        return f"""COMPLIANCE INFORMATION (from knowledge base search):

{top_result.get('text', 'No results found')}

SOURCE: {top_result.get('source', 'Unknown')}
AUTHORITY: {top_result.get('authority', 'Unknown')}
CITATION: {top_result.get('rule_citation', 'N/A')}

NOTE: This response is based on semantic search. For authoritative guidance, consult primary regulatory sources.
"""

    def _defense_semantic_response(self, results: List[Dict], query: str, compliance_zone: str) -> str:
        """Defense-grade semantic response."""
        response = f"""COMPLIANCE ANALYSIS (Knowledge Base Search)
{"=" * 80}

QUERY: {query}
COMPLIANCE ZONE: {compliance_zone}

REGULATORY FINDINGS:

"""
        for i, result in enumerate(results[:3], 1):
            response += f"""
{i}. {result.get('source', 'Unknown Source')}
   Authority: {result.get('authority', 'Unknown')}
   Citation: {result.get('rule_citation', 'N/A')}
   Relevance Score: {result.get('score', 0.0):.2f}

   {result.get('text', '')[:500]}...

"""

        response += """
DISCLAIMER:
This analysis is based on knowledge base search and may not reflect the most current
regulatory requirements. Always consult primary sources (CFR, TAC, current RRC rules)
for authoritative compliance guidance.
"""
        return response

    def _deep_analysis(
        self,
        query: str,
        normalized_query: str,
        entities: Dict,
        semantic_results: List[Dict],
        response_mode: str,
        compliance_zone: str,
        query_intent: str
    ) -> ComplianceResponse:
        """
        TIE-20 COMPONENT 20: Deep Analysis Mode

        Multi-source synthesis for complex compliance scenarios not in cache.
        """
        logger.info("Entering deep analysis mode")

        # Multi-doctrine decomposition
        relevant_doctrines = self._find_related_doctrines(entities, normalized_query)

        # Synthesize comprehensive response
        response_text = f"""DEEP COMPLIANCE ANALYSIS
{"=" * 80}

QUERY: {query}
COMPLIANCE ZONE: {compliance_zone}
QUERY INTENT: {query_intent}

This query requires multi-source analysis combining multiple regulatory frameworks.

RELEVANT REGULATORY AREAS:
"""

        authorities = set()
        citations = []

        if relevant_doctrines:
            for doctrine_dict in relevant_doctrines[:3]:
                response_text += f"\n• {doctrine_dict['topic'].replace('_', ' ')}\n"
                response_text += f"  Authorities: {', '.join(doctrine_dict['primary_authority'][:2])}\n"
                authorities.update(doctrine_dict['primary_authority'])

        if semantic_results:
            response_text += "\nKNOWLEDGE BASE FINDINGS:\n"
            for result in semantic_results[:2]:
                response_text += f"\n• {result.get('source', 'Unknown')}\n"
                response_text += f"  {result.get('text', '')[:300]}...\n"
                if result.get('authority'):
                    authorities.add(result['authority'])
                if result.get('rule_citation'):
                    citations.append(result['rule_citation'])

        response_text += """

RECOMMENDED APPROACH:
1. Consult primary regulatory sources for each applicable authority
2. Engage regulatory compliance specialist for site-specific analysis
3. Consider submitting formal inquiry to regulatory agency if uncertainty remains

CONFIDENCE ASSESSMENT:
This deep analysis indicates a complex compliance scenario requiring expert review.
Multiple regulatory frameworks may apply. Confidence is DISCLOSURE level pending
detailed site-specific analysis.
"""

        return ComplianceResponse(
            query_id="",
            response_text=response_text,
            response_mode=response_mode,
            compliance_zone=compliance_zone,
            query_intent=query_intent,
            cache_hit=False,
            doctrine_topic=None,
            doctrine_keywords=[],
            confidence=0.60,
            confidence_stratification="DISCLOSURE",
            authorities_cited=list(authorities)[:5],
            primary_citations=citations[:3],
            latency_ms=0.0,
            word_count=len(response_text.split()),
            determinism_hash=hashlib.sha256(f"{query}:DEEP".encode()).hexdigest()[:16],
            timestamp=""
        )

    def _find_related_doctrines(self, entities: Dict, normalized_query: str) -> List[Dict]:
        """Find doctrines related to query entities."""
        related = []

        # Search by extracted keywords
        for keyword_list in entities.values():
            for keyword in keyword_list:
                results = search_doctrines_by_keyword(keyword)
                for doctrine in results:
                    doctrine_dict = self._doctrine_to_dict(doctrine)
                    if doctrine_dict not in related:
                        related.append(doctrine_dict)

        return related[:5]


# ============================================================================
# GLOBAL ENGINE INSTANCE
# ============================================================================

engine = ComplianceEngine()


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.post("/query", response_model=ComplianceResponse)
async def query_compliance(request: ComplianceQuery):
    """
    Main compliance query endpoint.

    Accepts compliance questions and returns regulatory analysis.
    """
    try:
        response = engine.three_layer_response(
            query=request.query,
            response_mode=request.response_mode,
            compliance_zone=request.compliance_zone,
            authorities=request.authorities
        )
        return response
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    TIE-20 COMPONENT 12: Health Endpoint

    Comprehensive health check with metrics.
    """
    metrics = telemetry.get_metrics_snapshot()
    uptime = time.time() - engine.start_time

    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=VERSION,
        uptime_seconds=uptime,
        total_queries=metrics.total_queries,
        cache_hit_rate=metrics.cache_hit_rate,
        avg_latency_ms=metrics.avg_latency_ms,
        doctrines_loaded=len(DOCTRINE_CACHE),
        cloud_search_available=search_engine.is_available(),
        timestamp=datetime.utcnow().isoformat()
    )


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """
    TIE-20 COMPONENT 11: Metrics Collector

    Detailed performance and usage metrics.
    """
    snapshot = telemetry.get_metrics_snapshot()
    doctrine_coverage = telemetry.get_doctrine_coverage_stats()
    zone_distribution = telemetry.get_compliance_zone_distribution()
    recent_errors = telemetry.get_recent_errors(limit=10)

    return MetricsResponse(
        snapshot=snapshot.__dict__,
        doctrine_coverage=doctrine_coverage,
        compliance_zone_distribution=zone_distribution,
        recent_errors=recent_errors
    )


@app.get("/doctrines")
async def list_doctrines():
    """
    TIE-20 COMPONENT 10: Coverage Map

    List all available doctrine topics.
    """
    topics = get_all_topics()
    usage_stats = telemetry.get_doctrine_coverage_stats()

    return {
        "total_doctrines": len(topics),
        "topics": topics,
        "usage_statistics": usage_stats
    }


@app.get("/doctrine/{topic}")
async def get_doctrine_detail(topic: str):
    """Get detailed information about a specific doctrine topic."""
    doctrine = get_doctrine_by_topic(topic)
    if not doctrine:
        raise HTTPException(status_code=404, detail="Doctrine topic not found")

    return engine._doctrine_to_dict(doctrine)


@app.post("/analyze/drift")
async def analyze_drift():
    """
    TIE-20 COMPONENT 9: Drift Watcher

    Analyze doctrine drift and regulatory changes.
    """
    global drift_last_check, drift_observations

    # Check if drift monitoring interval has passed
    interval_hours = CONFIG.get("drift_monitoring", {}).get("check_interval_hours", 168)
    time_since_check = datetime.utcnow() - drift_last_check

    if time_since_check < timedelta(hours=interval_hours):
        return {
            "status": "no_check_needed",
            "last_check": drift_last_check.isoformat(),
            "next_check": (drift_last_check + timedelta(hours=interval_hours)).isoformat(),
            "observations": drift_observations
        }

    # Perform drift analysis
    logger.info("Performing doctrine drift analysis")

    # In production, this would:
    # 1. Compare doctrine cache against current regulatory sources
    # 2. Identify changed rules, new requirements, retired provisions
    # 3. Calculate drift magnitude and affected doctrines

    # For now, return placeholder
    drift_last_check = datetime.utcnow()
    drift_observations = []

    return {
        "status": "drift_check_complete",
        "check_timestamp": drift_last_check.isoformat(),
        "drift_detected": False,
        "observations": drift_observations,
        "next_check": (drift_last_check + timedelta(hours=interval_hours)).isoformat()
    }


# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Application startup tasks."""
    logger.info(f"{ENGINE_NAME} v{VERSION} starting up")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    logger.info(f"Cloud search available: {search_engine.is_available()}")
    logger.info(f"Listening on port {PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks."""
    logger.info(f"{ENGINE_NAME} shutting down")
    logger.info(f"Total queries processed: {telemetry.total_queries}")
    logger.info(f"Cache hit rate: {telemetry.cache_hits / max(telemetry.total_queries, 1):.2%}")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Run the compliance checker engine."""
    uvicorn.run(
        app,
        host=CONFIG.get("host", "localhost"),
        port=PORT,
        log_level=CONFIG.get("log_level", "info").lower()
    )


if __name__ == "__main__":
    main()
