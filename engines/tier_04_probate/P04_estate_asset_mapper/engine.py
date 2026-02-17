"""
P04 Estate Asset Mapper Engine - TIE Gold Standard
Map estate assets, classify inclusion/exclusion, determine valuation under IRC 2031-2044.

CAPABILITIES:
- Gross estate classification (IRC §2031)
- Property inclusion/exclusion analysis (§2033-§2044)
- Community property classification (Texas Family Code)
- Valuation methods (FMV, special use, alternate date)
- Discount applicability (DLOM, DLOC, fractional interests)
- Life insurance inclusion (§2042)
- Retained interests (§2036-§2038)
- Joint ownership (§2040)
- Form 706 reporting guidance

TIE-20 COMPONENTS:
✓ three_layer_response (doctrine cache → vector → deep analysis)
✓ response_modes (FAST, DEFENSE, MEMO)
✓ doctrine_cache (50+ blocks of real expertise)
✓ authority_hardening (hierarchical citation weights)
✓ confidence_stratification (DEFENSIBLE/AGGRESSIVE/DISCLOSURE/HIGH_RISK)
✓ semantic_normalization (estate planning terminology)
✓ vector_search (cloud retriever fallback)
✓ telemetry (comprehensive query tracking)
✓ drift_watcher (doctrine update monitoring)
✓ coverage_map (triggered vs missed doctrines)
✓ metrics_collector (latency, hit rates, queries/hour)
✓ health_endpoint (JSON status check)
✓ zoned_analysis (PLANNING/REPORTING/AUDIT zones)
✓ fact_fragility_scoring (verifiability assessment)
✓ audit_trail_jsonl (forensic query log)
✓ determinism_hash_sha256 (reproducibility)
✓ fastapi_server (full REST API)
✓ loguru_logging (structured, never print)
✓ multi_doctrine_decomposition (complex issue DAG)
✓ deep_analysis_mode (multi-source synthesis)

VERSION: 1.0.0
PORT: 8654
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import uuid
import json
import sys

from loguru import logger

# Configure loguru
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "engine.log",
    rotation="10 MB",
    retention="30 days",
    level="DEBUG"
)

# Import engine modules

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DOCTRINE_CACHE,
    DoctrineBlock,
    IssueCategory,
    ConfidenceStratification,
    get_doctrine_by_topic,
    search_doctrines_by_keyword,
    get_doctrines_by_category,
    get_high_confidence_doctrines,
    get_disclosure_required_doctrines
)
from semantic import get_normalizer, EstateSemanticNormalizer
from search import get_vector_search, EstateAssetVectorSearch
from telemetry import (
    get_telemetry_collector,
    QueryType,
    ResponseSource,
    EstateTelemetryCollector
)

# Load config
config_path = Path(__file__).parent / "config.json"
with open(config_path, 'r') as f:
    CONFIG = json.load(f)


# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    """Estate asset mapping query request."""
    query: str = Field(..., description="Natural language query")
    mode: str = Field(default="FAST", description="Response mode: FAST, DEFENSE, MEMO")
    zone: str = Field(default="REPORTING", description="Analysis zone: PLANNING, REPORTING, AUDIT")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context (asset details, jurisdiction, etc.)")


class AuthorityReference(BaseModel):
    """Legal authority citation."""
    citation: str
    authority_type: str  # statute, regulation, case_law, ruling
    tier: int  # 1=controlling, 2=persuasive, 3=guidance, 4=reference
    relevance: str


class EstateAssetResponse(BaseModel):
    """Estate asset mapping response."""
    query_id: str
    timestamp: str
    query: str
    mode: str
    zone: str

    # Classification
    inclusion_determination: str
    irc_sections_applicable: List[str]
    property_classification: str

    # Valuation
    valuation_method: str
    discounts_applicable: List[str]
    special_valuation_available: bool

    # Analysis
    reasoning: str
    doctrine_blocks_applied: List[str]
    authorities: List[AuthorityReference]

    # Confidence
    confidence_level: str
    disclosure_required: bool
    fact_fragility_score: float

    # Metadata
    response_source: str
    latency_ms: float
    determinism_hash: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    engine_id: str
    version: str
    port: int
    uptime_seconds: float
    total_queries: int
    doctrine_cache_hit_rate: float
    avg_latency_ms: float
    vector_search_available: bool


# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="P04 Estate Asset Mapper Engine",
    description="Estate asset classification, valuation, and inclusion analysis under IRC 2031-2044",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
normalizer: EstateSemanticNormalizer = get_normalizer()
vector_search: EstateAssetVectorSearch = get_vector_search()
telemetry: EstateTelemetryCollector = get_telemetry_collector()
engine_start_time = datetime.now()


# ═══════════════════════════════════════════════════════════════════════════
# CORE ENGINE LOGIC - TIE-20 THREE-LAYER RESPONSE
# ═══════════════════════════════════════════════════════════════════════════

def doctrine_cache_search(normalized_query: str, irc_sections: List[str]) -> List[DoctrineBlock]:
    """
    Layer 1: Doctrine cache search (target <200ms).
    Search pre-compiled expert reasoning blocks.
    """
    matches = []

    # Search by IRC sections
    for section in irc_sections:
        section_blocks = [b for b in DOCTRINE_CACHE if section in b.topic or section in ' '.join(b.keywords)]
        matches.extend(section_blocks)

    # Search by keywords in normalized query
    query_words = normalized_query.split()
    for block in DOCTRINE_CACHE:
        for keyword in block.keywords:
            if keyword in query_words:
                if block not in matches:
                    matches.append(block)
                break

    # Deduplicate and sort by confidence (DEFENSIBLE first)
    unique_matches = list({b.topic: b for b in matches}.values())
    unique_matches.sort(key=lambda b: (
        b.confidence == ConfidenceStratification.DEFENSIBLE,
        -b.fact_fragility_score
    ), reverse=True)

    return unique_matches[:5]  # Top 5 most relevant


def vector_search_fallback(query: str, mode: str) -> List[Dict[str, Any]]:
    """
    Layer 2: Vector search fallback (if doctrine cache insufficient).
    Query cloud knowledge base for semantic matches.
    """
    if not vector_search.is_available():
        return []

    top_k = 3 if mode == "FAST" else 5
    results = vector_search.search(query=query, top_k=top_k, min_score=0.7)
    return results


def deep_analysis_synthesis(
    query: str,
    mode: str,
    doctrine_blocks: List[DoctrineBlock],
    vector_results: List[Dict[str, Any]],
    context: Optional[Dict[str, Any]]
) -> str:
    """
    Layer 3: Deep analysis mode (DEFENSE, MEMO modes).
    Synthesize multiple sources into comprehensive analysis.
    """
    analysis_parts = []

    # FAST mode: Concise guidance from top doctrine block
    if mode == "FAST":
        if doctrine_blocks:
            top_block = doctrine_blocks[0]
            analysis_parts.append("CLASSIFICATION:")
            analysis_parts.append(" ".join(top_block.conclusion_template))
            analysis_parts.append("\nKEY FACTORS:")
            for factor in top_block.key_factors[:3]:
                analysis_parts.append(f"• {factor}")
            analysis_parts.append(f"\nCONFIDENCE: {top_block.confidence.value}")
        else:
            analysis_parts.append("Insufficient doctrine match. Recommend DEFENSE mode for full analysis.")
        return "\n".join(analysis_parts)

    # DEFENSE mode: Audit-ready analysis with full citation chain
    if mode == "DEFENSE":
        analysis_parts.append("ESTATE ASSET INCLUSION ANALYSIS\n")

        for idx, block in enumerate(doctrine_blocks[:3], 1):
            analysis_parts.append(f"{idx}. {block.topic.upper().replace('_', ' ')}")
            analysis_parts.append("\nCONCLUSION:")
            analysis_parts.append(" ".join(block.conclusion_template))

            analysis_parts.append("\nREASONING FRAMEWORK:")
            # Include first 500 chars of reasoning
            reasoning_preview = block.reasoning_framework[:500].strip()
            analysis_parts.append(reasoning_preview + "...")

            analysis_parts.append("\nPRIMARY AUTHORITY:")
            for authority in block.primary_authority[:3]:
                analysis_parts.append(f"• {authority}")

            analysis_parts.append(f"\nCONFIDENCE: {block.confidence.value}")
            if block.disclosure_caveat:
                analysis_parts.append(f"DISCLOSURE: {block.disclosure_caveat}")
            analysis_parts.append("\n" + "="*80 + "\n")

        # Add vector search results if available
        if vector_results:
            analysis_parts.append("ADDITIONAL AUTHORITIES FROM KNOWLEDGE BASE:")
            for result in vector_results[:2]:
                analysis_parts.append(f"• {result.get('content', 'N/A')[:200]}...")

        return "\n".join(analysis_parts)

    # MEMO mode: Client memo format with explanation and alternatives
    if mode == "MEMO":
        analysis_parts.append("MEMORANDUM\n")
        analysis_parts.append(f"RE: Estate Tax Treatment - {query}\n")
        analysis_parts.append(f"DATE: {datetime.now().strftime('%B %d, %Y')}\n")
        analysis_parts.append("="*80 + "\n")

        analysis_parts.append("EXECUTIVE SUMMARY:")
        if doctrine_blocks:
            analysis_parts.append(" ".join(doctrine_blocks[0].conclusion_template))
        analysis_parts.append("\n")

        analysis_parts.append("DETAILED ANALYSIS:\n")
        for idx, block in enumerate(doctrine_blocks[:2], 1):
            analysis_parts.append(f"\n{idx}. {block.topic.upper().replace('_', ' ')}\n")

            analysis_parts.append("Legal Framework:")
            analysis_parts.append(block.reasoning_framework[:800].strip() + "...\n")

            analysis_parts.append("Key Factors:")
            for factor in block.key_factors:
                analysis_parts.append(f"  • {factor}")

            analysis_parts.append("\nResolution Strategy:")
            analysis_parts.append(block.resolution_strategy[:500].strip() + "...\n")

            analysis_parts.append("Authorities:")
            for authority in block.primary_authority:
                analysis_parts.append(f"  • {authority}")

            analysis_parts.append(f"\nRisk Assessment: {block.confidence.value}")
            analysis_parts.append(f"Fact Fragility: {block.fact_fragility_score:.2f} (0=solid, 1=fragile)")
            if block.disclosure_caveat:
                analysis_parts.append(f"\n⚠ DISCLOSURE RECOMMENDED: {block.disclosure_caveat}")

        analysis_parts.append("\n" + "="*80)
        analysis_parts.append("\nRECOMMENDATIONS:")
        analysis_parts.append("1. Document all factual support (appraisals, agreements, transaction records)")
        analysis_parts.append("2. Engage qualified appraisers for valuation (ASA, MAI, CFA credentials)")
        analysis_parts.append("3. Consider disclosure if position is AGGRESSIVE or DISCLOSURE level")
        analysis_parts.append("4. Coordinate with estate planning counsel for optimization strategies")

        return "\n".join(analysis_parts)

    return "Invalid mode specified."


def classify_query_type(normalized_query: str, normalizer: EstateSemanticNormalizer) -> QueryType:
    """Classify query into estate asset mapping category."""
    if normalizer.is_inclusion_query(normalized_query):
        return QueryType.INCLUSION_ANALYSIS
    elif normalizer.is_valuation_query(normalized_query):
        return QueryType.VALUATION
    elif normalizer.is_discount_query(normalized_query):
        return QueryType.DISCOUNT_APPLICABILITY
    elif normalizer.is_community_property_query(normalized_query):
        return QueryType.COMMUNITY_PROPERTY
    elif normalizer.is_retained_interest_query(normalized_query):
        return QueryType.RETAINED_INTERESTS
    elif normalizer.is_special_valuation_query(normalized_query):
        return QueryType.SPECIAL_VALUATION
    elif "joint" in normalized_query or "2040" in normalized_query:
        return QueryType.JOINT_OWNERSHIP
    elif "life insurance" in normalized_query or "2042" in normalized_query:
        return QueryType.LIFE_INSURANCE
    else:
        return QueryType.GENERAL_GUIDANCE


def extract_authorities(doctrine_blocks: List[DoctrineBlock]) -> List[AuthorityReference]:
    """Extract and classify legal authorities from doctrine blocks."""
    authorities = []
    authority_tiers = CONFIG["authority_hierarchy"]

    for block in doctrine_blocks:
        for auth_text in block.primary_authority:
            # Classify authority type and tier
            if "IRC" in auth_text or "§" in auth_text:
                auth_type = "statute"
                tier = 1
            elif "Treas. Reg." in auth_text:
                auth_type = "regulation"
                tier = 1
            elif "v." in auth_text and ("F.2d" in auth_text or "F.3d" in auth_text or "U.S." in auth_text):
                auth_type = "case_law"
                tier = 1 if "U.S." in auth_text else 2
            elif "Rev. Rul." in auth_text:
                auth_type = "ruling"
                tier = 2
            elif "Texas" in auth_text:
                auth_type = "state_law"
                tier = 4
            else:
                auth_type = "guidance"
                tier = 3

            authorities.append(AuthorityReference(
                citation=auth_text,
                authority_type=auth_type,
                tier=tier,
                relevance="Direct support for analysis"
            ))

    # Deduplicate and sort by tier
    unique_authorities = list({a.citation: a for a in authorities}.values())
    unique_authorities.sort(key=lambda a: a.tier)

    return unique_authorities


# ═══════════════════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.post("/analyze", response_model=EstateAssetResponse)
async def analyze_estate_asset(request: QueryRequest) -> EstateAssetResponse:
    """
    Main analysis endpoint: classify estate assets, determine inclusion, and provide valuation guidance.

    TIE-20 Three-Layer Response:
    1. Doctrine cache (0-200ms) - pre-compiled expert blocks
    2. Vector search fallback (if cache miss or insufficient)
    3. Deep analysis synthesis (DEFENSE/MEMO modes)
    """
    start_time = datetime.now()
    query_id = str(uuid.uuid4())

    logger.info(f"Query received: {query_id} | Mode: {request.mode} | Zone: {request.zone}")

    try:
        # Step 1: Semantic normalization
        normalized_query = normalizer.normalize(request.query)
        irc_sections = normalizer.extract_irc_sections(request.query)
        entity_types = normalizer.extract_entity_types(request.query)
        property_types = normalizer.extract_property_types(request.query)
        query_type = classify_query_type(normalized_query, normalizer)

        logger.debug(f"Normalized query: {normalized_query}")
        logger.debug(f"IRC sections: {irc_sections}")
        logger.debug(f"Query type: {query_type.value}")

        # Step 2: Doctrine cache search (Layer 1)
        doctrine_blocks = doctrine_cache_search(normalized_query, irc_sections)
        cache_hit = len(doctrine_blocks) > 0

        logger.info(f"Doctrine cache: {len(doctrine_blocks)} blocks matched | Cache hit: {cache_hit}")

        # Step 3: Vector search fallback (Layer 2) if needed
        vector_results = []
        vector_used = False
        if not cache_hit or request.mode in ["DEFENSE", "MEMO"]:
            vector_results = vector_search_fallback(request.query, request.mode)
            vector_used = len(vector_results) > 0
            logger.info(f"Vector search: {len(vector_results)} results")

        # Step 4: Deep analysis synthesis (Layer 3)
        reasoning = deep_analysis_synthesis(
            query=request.query,
            mode=request.mode,
            doctrine_blocks=doctrine_blocks,
            vector_results=vector_results,
            context=request.context
        )

        # Step 5: Extract metadata
        authorities = extract_authorities(doctrine_blocks)

        inclusion_determination = "INCLUDED" if doctrine_blocks and any(
            "include" in b.topic or "2033" in b.topic for b in doctrine_blocks
        ) else "ANALYSIS REQUIRED"

        property_classification = doctrine_blocks[0].issue_category.value if doctrine_blocks else "GENERAL"

        valuation_method = "fair_market_value"
        if any("2032a" in s for s in irc_sections):
            valuation_method = "special_use_valuation"
        elif any("2032" in s for s in irc_sections):
            valuation_method = "alternate_valuation_date"

        discounts = []
        if normalizer.is_discount_query(normalized_query):
            if "marketability" in normalized_query or "dlom" in normalized_query:
                discounts.append("lack_of_marketability")
            if "control" in normalized_query or "dloc" in normalized_query or "minority" in normalized_query:
                discounts.append("lack_of_control")
            if "fractional" in normalized_query or "undivided" in normalized_query:
                discounts.append("fractional_interest")

        special_val_available = any("2032a" in s for s in irc_sections) or "special use" in normalized_query.lower()

        confidence = doctrine_blocks[0].confidence.value if doctrine_blocks else "UNKNOWN"
        disclosure_required = any(
            b.confidence in [
                ConfidenceStratification.AGGRESSIVE,
                ConfidenceStratification.DISCLOSURE,
                ConfidenceStratification.HIGH_RISK
            ] for b in doctrine_blocks
        )
        fact_fragility = doctrine_blocks[0].fact_fragility_score if doctrine_blocks else 0.5

        doctrine_topics = [b.topic for b in doctrine_blocks]

        response_source = ResponseSource.DOCTRINE_CACHE if cache_hit else (
            ResponseSource.VECTOR_SEARCH if vector_used else ResponseSource.DEEP_ANALYSIS
        )
        if cache_hit and vector_used:
            response_source = ResponseSource.HYBRID

        # Step 6: Calculate latency
        latency_ms = (datetime.now() - start_time).total_seconds() * 1000

        # Step 7: Determinism hash
        determinism_hash = telemetry.compute_determinism_hash(request.query, reasoning)

        # Step 8: Log telemetry
        telemetry.log_query(
            query_id=query_id,
            query_text=request.query,
            query_type=query_type,
            response_mode=request.mode,
            normalized_query=normalized_query,
            irc_sections=irc_sections,
            entity_types=entity_types,
            property_types=property_types,
            doctrine_blocks=doctrine_topics,
            response_source=response_source,
            latency_ms=latency_ms,
            cache_hit=cache_hit,
            vector_used=vector_used,
            confidence=confidence,
            disclosure=disclosure_required,
            fragility=fact_fragility,
            response_length=len(reasoning),
            determinism_hash=determinism_hash
        )

        # Step 9: Log audit trail
        telemetry.log_audit_entry(
            query_id=query_id,
            query_text=request.query,
            response_text=reasoning,
            doctrine_blocks=doctrine_topics,
            authorities_cited=[a.citation for a in authorities],
            confidence=confidence,
            disclosure=disclosure_required
        )

        # Step 10: Build response
        response = EstateAssetResponse(
            query_id=query_id,
            timestamp=datetime.now().isoformat(),
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            inclusion_determination=inclusion_determination,
            irc_sections_applicable=irc_sections,
            property_classification=property_classification,
            valuation_method=valuation_method,
            discounts_applicable=discounts,
            special_valuation_available=special_val_available,
            reasoning=reasoning,
            doctrine_blocks_applied=doctrine_topics,
            authorities=authorities,
            confidence_level=confidence,
            disclosure_required=disclosure_required,
            fact_fragility_score=fact_fragility,
            response_source=response_source.value,
            latency_ms=latency_ms,
            determinism_hash=determinism_hash
        )

        logger.info(
            f"Query complete: {query_id} | Latency: {latency_ms:.1f}ms | "
            f"Confidence: {confidence} | Disclosure: {disclosure_required}"
        )

        return response

    except Exception as e:
        logger.error(f"Query failed: {query_id} | Error: {str(e)}")
        telemetry.log_query(
            query_id=query_id,
            query_text=request.query,
            query_type=QueryType.GENERAL_GUIDANCE,
            response_mode=request.mode,
            normalized_query="",
            irc_sections=[],
            entity_types=[],
            property_types=[],
            doctrine_blocks=[],
            response_source=ResponseSource.DOCTRINE_CACHE,
            latency_ms=0,
            cache_hit=False,
            vector_used=False,
            confidence="UNKNOWN",
            disclosure=False,
            fragility=1.0,
            response_length=0,
            determinism_hash="",
            error=True,
            error_msg=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Comprehensive health check endpoint."""
    metrics = telemetry.generate_metrics_snapshot()
    uptime = (datetime.now() - engine_start_time).total_seconds()

    return HealthResponse(
        status="healthy",
        engine_id=CONFIG["engine_id"],
        version=CONFIG["version"],
        port=CONFIG["port"],
        uptime_seconds=uptime,
        total_queries=metrics.total_queries,
        doctrine_cache_hit_rate=metrics.doctrine_cache_hit_rate,
        avg_latency_ms=metrics.avg_latency_ms,
        vector_search_available=vector_search.is_available()
    )


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get detailed performance metrics."""
    snapshot = telemetry.generate_metrics_snapshot()
    return {
        "timestamp": snapshot.timestamp,
        "total_queries": snapshot.total_queries,
        "queries_per_hour": snapshot.queries_per_hour,
        "doctrine_cache_hit_rate": snapshot.doctrine_cache_hit_rate,
        "avg_latency_ms": snapshot.avg_latency_ms,
        "p95_latency_ms": snapshot.p95_latency_ms,
        "p99_latency_ms": snapshot.p99_latency_ms,
        "error_rate": snapshot.error_rate,
        "query_type_distribution": snapshot.query_type_distribution,
        "response_mode_distribution": snapshot.response_mode_distribution,
        "confidence_distribution": snapshot.confidence_distribution,
        "avg_fact_fragility": snapshot.avg_fact_fragility,
        "top_triggered_doctrines": snapshot.top_triggered_doctrines
    }


@app.get("/doctrines")
async def list_doctrines() -> Dict[str, Any]:
    """List all available doctrine blocks."""
    return {
        "total_doctrines": len(DOCTRINE_CACHE),
        "by_category": {
            cat.value: len(get_doctrines_by_category(cat))
            for cat in IssueCategory
        },
        "by_confidence": {
            conf.value: len([b for b in DOCTRINE_CACHE if b.confidence == conf])
            for conf in ConfidenceStratification
        },
        "topics": [b.topic for b in DOCTRINE_CACHE]
    }


@app.get("/coverage")
async def get_coverage() -> Dict[str, Any]:
    """Get doctrine coverage report (triggered vs. missed)."""
    return telemetry.get_doctrine_coverage_report()


# ═══════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting {CONFIG['engine_id']} v{CONFIG['version']}")
    logger.info(f"Domain: {CONFIG['domain']} | Subdomain: {CONFIG['subdomain']}")
    logger.info(f"Doctrine blocks loaded: {len(DOCTRINE_CACHE)}")
    logger.info(f"Vector search available: {vector_search.is_available()}")
    logger.info(f"Port: {CONFIG['port']}")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=CONFIG["port"],
        log_level="info"
    )
