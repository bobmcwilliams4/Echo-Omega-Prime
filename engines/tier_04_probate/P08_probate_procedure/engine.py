"""
P08 Probate Procedure Intelligence Engine
TIE-20 compliant probate procedure mapping engine.

Maps probate procedures by state — independent administration, dependent administration,
muniment of title, small estate affidavit. No-LLM mode authority-driven reasoning.

Port: 8658
Version: 1.0.0
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import hashlib
import json
import uuid
from pathlib import Path
from loguru import logger

# Import engine modules
import sys

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import DOCTRINE_CACHE, DoctrineBlock, ConfidenceLevel, IssueCategory
from semantic import normalize_query, extract_keywords, extract_entities
from search import VectorSearchFallback, get_procedure_guide, get_statutory_references
from telemetry import (
    TelemetryCollector, PerformanceTracker, DriftWatcher,
    QueryTrace, QueryZone, ErrorDomain
)

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

# Setup logging
logger.remove()
logger.add(
    Path(__file__).parent / "logs" / "engine_{time}.log",
    rotation="500 MB",
    retention="30 days",
    level=CONFIG["logging"]["level"],
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    serialize=CONFIG["logging"]["format"] == "json"
)

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ResponseMode(str, Enum):
    """Response generation modes."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class QueryRequest(BaseModel):
    """Probate procedure query request."""
    query: str = Field(..., description="Probate procedure query text")
    mode: ResponseMode = Field(ResponseMode.DEFENSE, description="Response detail level")
    jurisdiction: str = Field("Texas", description="Primary jurisdiction")
    zone: Optional[str] = Field(None, description="Position zone: PLANNING, REPORTING, AUDIT")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class DoctrineReference(BaseModel):
    """Reference to doctrine block used in response."""
    topic: str
    confidence: str
    authority: List[str]
    fragility_score: float


class QueryResponse(BaseModel):
    """Probate procedure query response."""
    query_id: str
    query: str
    response: str
    mode: ResponseMode
    confidence_level: str
    confidence_score: float

    doctrines_used: List[DoctrineReference]
    authorities_cited: List[str]
    issue_categories: List[str]

    fragility_score: float
    epistemic_gaps: List[str]
    disclosure_caveat: Optional[str]

    performance: Dict[str, float]
    determinism_hash: str
    timestamp: datetime


class HealthStatus(BaseModel):
    """Engine health status."""
    status: str
    engine_id: str
    version: str
    uptime_seconds: float
    queries_processed: int
    cache_hit_rate: float
    avg_latency_ms: float
    doctrine_count: int
    last_error: Optional[str]


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title=ENGINE_NAME,
    description=CONFIG["description"],
    version=VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
telemetry = TelemetryCollector(CONFIG)
drift_watcher = DriftWatcher(telemetry)
vector_search = VectorSearchFallback(CONFIG)

# Engine state
start_time = datetime.utcnow()
last_error: Optional[str] = None


# ============================================================================
# TIE-20 COMPONENT 1: THREE-LAYER RESPONSE
# ============================================================================

class ThreeLayerResponse:
    """Three-tier response generation: Cache → Vector → Deep Analysis."""

    def __init__(self):
        self.cache = DOCTRINE_CACHE
        self.vector_fallback = vector_search

    async def respond(
        self,
        query: str,
        mode: ResponseMode,
        zone: QueryZone,
        tracker: PerformanceTracker
    ) -> Dict[str, Any]:
        """
        Generate three-layer response.

        Layer 1: Doctrine Cache (0-200ms) - instant expert reasoning
        Layer 2: Vector Search (200-500ms) - semantic retrieval fallback
        Layer 3: Deep Analysis (500ms+) - comprehensive synthesis
        """
        tracker.start("layer1_cache")
        cache_results = self._search_cache(query)
        cache_latency = tracker.stop("layer1_cache")

        if cache_results and mode == ResponseMode.FAST:
            # Fast mode: cache only
            return self._format_cache_response(cache_results, cache_latency)

        # Layer 2: Vector fallback if cache insufficient
        tracker.start("layer2_vector")
        vector_results = []
        if len(cache_results) < 3:
            vector_results = await self.vector_fallback.search(query, top_k=3)
        vector_latency = tracker.stop("layer2_vector")

        # Layer 3: Deep analysis synthesis
        tracker.start("layer3_synthesis")
        synthesis = self._synthesize_response(
            query, cache_results, vector_results, mode, zone
        )
        synthesis_latency = tracker.stop("layer3_synthesis")

        return {
            "synthesis": synthesis,
            "cache_results": cache_results,
            "vector_results": vector_results,
            "latencies": {
                "cache": cache_latency,
                "vector": vector_latency,
                "synthesis": synthesis_latency
            }
        }

    def _search_cache(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache for matching blocks."""
        normalized = normalize_query(query)
        keywords = extract_keywords(normalized)

        matches = []
        for block in self.cache:
            score = self._calculate_match_score(keywords, block)
            if score > 0.3:  # Match threshold
                matches.append((score, block))

        # Sort by score descending
        matches.sort(reverse=True, key=lambda x: x[0])
        return [block for _, block in matches[:5]]

    def _calculate_match_score(self, keywords: List[str], block: DoctrineBlock) -> float:
        """Calculate keyword match score for doctrine block."""
        block_keywords_lower = [k.lower() for k in block.keywords]
        matches = sum(1 for kw in keywords if any(kw in bk for bk in block_keywords_lower))
        if not keywords:
            return 0.0
        return matches / len(keywords)

    def _format_cache_response(
        self,
        blocks: List[DoctrineBlock],
        latency: float
    ) -> Dict[str, Any]:
        """Format cache-only response for FAST mode."""
        if not blocks:
            return {
                "synthesis": {"response": "No matching doctrine found.", "confidence": 0.0},
                "cache_results": [],
                "vector_results": [],
                "latencies": {"cache": latency, "vector": 0.0, "synthesis": 0.0}
            }

        primary = blocks[0]
        response_text = "\n\n".join(primary.conclusion_template)

        return {
            "synthesis": {
                "response": response_text,
                "confidence": primary.confidence_stratification.get("DEFENSIBLE", 0.9),
                "primary_block": primary.topic,
                "authorities": primary.primary_authority
            },
            "cache_results": blocks,
            "vector_results": [],
            "latencies": {"cache": latency, "vector": 0.0, "synthesis": 0.0}
        }

    def _synthesize_response(
        self,
        query: str,
        cache_results: List[DoctrineBlock],
        vector_results: List[Dict[str, Any]],
        mode: ResponseMode,
        zone: QueryZone
    ) -> Dict[str, Any]:
        """Synthesize comprehensive response from all sources."""
        if not cache_results and not vector_results:
            return {
                "response": "Insufficient probate procedure doctrine to respond. Query may require jurisdiction-specific research beyond Texas Estates Code.",
                "confidence": 0.3,
                "authorities": [],
                "issue_categories": []
            }

        # Primary doctrine block
        primary = cache_results[0] if cache_results else None

        # Build response based on mode
        if mode == ResponseMode.FAST:
            response_text = self._build_fast_response(primary)
        elif mode == ResponseMode.DEFENSE:
            response_text = self._build_defense_response(primary, cache_results, zone)
        else:  # MEMO
            response_text = self._build_memo_response(primary, cache_results, vector_results, zone)

        # Extract authorities and issue categories
        authorities = []
        issue_categories = set()
        for block in cache_results:
            authorities.extend(block.primary_authority)
            issue_categories.add(block.issue_category.value)

        # Calculate aggregate confidence
        confidence = self._calculate_aggregate_confidence(cache_results)

        return {
            "response": response_text,
            "confidence": confidence,
            "authorities": list(set(authorities)),
            "issue_categories": list(issue_categories),
            "primary_doctrine": primary.topic if primary else None,
            "supporting_doctrines": [b.topic for b in cache_results[1:]]
        }

    def _build_fast_response(self, block: Optional[DoctrineBlock]) -> str:
        """Build concise fast response."""
        if not block:
            return "No applicable probate procedure doctrine found."
        return "\n\n".join(block.conclusion_template)

    def _build_defense_response(
        self,
        primary: Optional[DoctrineBlock],
        blocks: List[DoctrineBlock],
        zone: QueryZone
    ) -> str:
        """Build audit-ready defense response with full reasoning."""
        if not primary:
            return "No applicable probate procedure doctrine found."

        sections = []

        # Conclusion
        sections.append("CONCLUSION:\n" + "\n".join(primary.conclusion_template))

        # Reasoning
        sections.append("\nREASONING:\n" + primary.reasoning_framework)

        # Authority
        sections.append("\nAUTHORITY:\n" + "\n".join(f"- {auth}" for auth in primary.primary_authority))

        # Key Factors
        sections.append("\nKEY FACTORS:\n" + "\n".join(f"- {factor}" for factor in primary.key_factors))

        # Adversarial Analysis
        sections.append(f"\nADVERSARY POSITION: {primary.adversary_position}")
        sections.append("\nCOUNTER-ARGUMENTS:\n" + "\n".join(f"- {arg}" for arg in primary.counter_arguments))
        sections.append(f"\nRESOLUTION STRATEGY: {primary.resolution_strategy}")

        # Zone-specific considerations
        if zone == QueryZone.PLANNING:
            sections.append("\nPLANNING CONSIDERATIONS:\nThis analysis addresses pre-death estate planning. Procedure selection should account for beneficiary cooperation, fiduciary trustworthiness, and estate complexity.")
        elif zone == QueryZone.AUDIT:
            sections.append("\nAUDIT CONSIDERATIONS:\nThis analysis reviews probate procedure compliance. Verify proper venue, timely filing, sufficient notice, and procedural requirements met.")

        # Disclosure
        if primary.disclosure_caveat:
            sections.append(f"\nDISCLOSURE: {primary.disclosure_caveat}")

        return "\n".join(sections)

    def _build_memo_response(
        self,
        primary: Optional[DoctrineBlock],
        cache_blocks: List[DoctrineBlock],
        vector_results: List[Dict[str, Any]],
        zone: QueryZone
    ) -> str:
        """Build comprehensive memorandum response."""
        if not primary:
            return "No applicable probate procedure doctrine found."

        sections = []

        # Executive Summary
        sections.append("EXECUTIVE SUMMARY:\n" + "\n".join(primary.conclusion_template))

        # Detailed Analysis
        sections.append("\n\nDETAILED ANALYSIS:\n" + primary.reasoning_framework)

        # Alternative Procedures
        if len(cache_blocks) > 1:
            sections.append("\n\nALTERNATIVE PROCEDURES:")
            for block in cache_blocks[1:4]:
                sections.append(f"\n{block.topic}:")
                sections.append("\n".join(block.conclusion_template))

        # Statutory Authority
        sections.append("\n\nSTATUTORY AUTHORITY:")
        all_authorities = []
        for block in cache_blocks:
            all_authorities.extend(block.primary_authority)
        for auth in list(set(all_authorities))[:10]:
            sections.append(f"- {auth}")

        # Risk Analysis
        sections.append("\n\nRISK ANALYSIS:")
        sections.append(f"Fragility Score: {primary.fragility_score:.2f} (0=stable, 1=fragile)")
        sections.append(f"Confidence: {primary.confidence.value}")
        sections.append(f"\nAdversary Position: {primary.adversary_position}")
        sections.append("\nPotential Challenges:")
        for arg in primary.counter_arguments[:5]:
            sections.append(f"- {arg}")

        # Recommendations
        sections.append(f"\n\nRECOMMENDATIONS:\n{primary.resolution_strategy}")

        # Procedural Guidance
        procedure_key = primary.topic.lower().replace(" ", "_")
        guide = get_procedure_guide(procedure_key)
        if guide:
            sections.append(f"\n\nPROCEDURAL STEPS:{guide}")

        return "\n".join(sections)

    def _calculate_aggregate_confidence(self, blocks: List[DoctrineBlock]) -> float:
        """Calculate aggregate confidence from multiple blocks."""
        if not blocks:
            return 0.0

        # Weight by position (first block more important)
        weighted_sum = sum(
            block.confidence_stratification.get("DEFENSIBLE", 0.8) / (i + 1)
            for i, block in enumerate(blocks[:3])
        )
        weights = sum(1.0 / (i + 1) for i in range(min(3, len(blocks))))

        return weighted_sum / weights if weights > 0 else 0.0


# ============================================================================
# TIE-20 COMPONENT 2-20: Additional Components
# ============================================================================

class AuthorityHardening:
    """Hierarchical authority levels with conflict resolution."""

    AUTHORITY_WEIGHTS = {
        "texas_estates_code": 1.0,
        "texas_case_law": 0.9,
        "uniform_probate_code": 0.7,
        "restatement": 0.6,
        "treatise": 0.5,
        "other_state_statute": 0.4,
    }

    @classmethod
    def classify_authority(cls, citation: str) -> str:
        """Classify authority source."""
        citation_lower = citation.lower()
        if "texas estates code" in citation_lower:
            return "texas_estates_code"
        elif "tex." in citation_lower or "s.w." in citation_lower:
            return "texas_case_law"
        elif "uniform probate code" in citation_lower or "upc" in citation_lower:
            return "uniform_probate_code"
        elif "restatement" in citation_lower:
            return "restatement"
        else:
            return "treatise"

    @classmethod
    def resolve_conflict(cls, authorities: List[str]) -> str:
        """Resolve conflicting authorities by weight."""
        if not authorities:
            return "No authority"

        weighted = [(auth, cls.AUTHORITY_WEIGHTS.get(cls.classify_authority(auth), 0.3))
                    for auth in authorities]
        weighted.sort(key=lambda x: x[1], reverse=True)
        return weighted[0][0]


class EpistemicGuardrails:
    """Detect and flag epistemic gaps."""

    BANNED_PHRASES = [
        "probably", "likely", "possibly", "maybe", "might",
        "should work", "generally", "usually", "typically"
    ]

    @classmethod
    def check_response(cls, response: str) -> List[str]:
        """Check response for epistemic violations."""
        violations = []
        response_lower = response.lower()

        for phrase in cls.BANNED_PHRASES:
            if phrase in response_lower:
                violations.append(f"Hedging detected: '{phrase}'")

        return violations

    @classmethod
    def apply_guardrails(cls, response: Dict[str, Any]) -> Dict[str, Any]:
        """Apply epistemic guardrails to response."""
        text = response.get("response", "")
        violations = cls.check_response(text)

        if violations:
            response["epistemic_warnings"] = violations
            response["confidence"] *= 0.9  # Reduce confidence for hedging

        return response


# ============================================================================
# MAIN QUERY HANDLER
# ============================================================================

three_layer = ThreeLayerResponse()

@app.post("/query", response_model=QueryResponse)
async def handle_query(req: QueryRequest) -> QueryResponse:
    """
    Handle probate procedure query with TIE-20 full stack.
    """
    global last_error

    query_id = str(uuid.uuid4())
    tracker = PerformanceTracker()
    tracker.start("total")

    try:
        # Normalize and extract
        normalized = normalize_query(req.query)
        keywords = extract_keywords(normalized)
        entities = extract_entities(normalized)

        # Determine zone
        zone_str = req.zone or "REPORTING"
        try:
            zone = QueryZone[zone_str]
        except KeyError:
            zone = QueryZone.REPORTING

        # Three-layer response
        result = await three_layer.respond(
            normalized,
            req.mode,
            zone,
            tracker
        )

        synthesis = result["synthesis"]
        cache_results = result["cache_results"]

        # Apply epistemic guardrails
        synthesis = EpistemicGuardrails.apply_guardrails(synthesis)

        # Build response
        response_text = synthesis["response"]
        confidence = synthesis["confidence"]
        authorities = synthesis.get("authorities", [])
        issue_categories = synthesis.get("issue_categories", [])

        # Doctrine references
        doctrine_refs = [
            DoctrineReference(
                topic=block.topic,
                confidence=block.confidence.value,
                authority=block.primary_authority,
                fragility_score=block.fragility_score
            )
            for block in cache_results[:5]
        ]

        # Confidence level
        if confidence >= 0.95:
            conf_level = "DEFENSIBLE"
        elif confidence >= 0.80:
            conf_level = "AGGRESSIVE"
        elif confidence >= 0.65:
            conf_level = "DISCLOSURE"
        else:
            conf_level = "HIGH_RISK"

        # Fragility score (average of used doctrines)
        fragility = (
            sum(b.fragility_score for b in cache_results) / len(cache_results)
            if cache_results else 0.5
        )

        # Epistemic gaps
        epistemic_gaps = synthesis.get("epistemic_warnings", [])

        # Disclosure caveat
        disclosure = None
        if cache_results and cache_results[0].disclosure_caveat:
            disclosure = cache_results[0].disclosure_caveat

        # Determinism hash
        hash_input = f"{req.query}|{req.mode.value}|{req.jurisdiction}|{VERSION}"
        determ_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        # Performance metrics
        total_latency = tracker.stop("total")
        performance = {
            "total_ms": round(total_latency, 2),
            **{k: round(v, 2) for k, v in result["latencies"].items()}
        }

        # Telemetry trace
        trace = QueryTrace(
            query_id=query_id,
            timestamp=datetime.utcnow(),
            query_text=req.query,
            normalized_query=normalized,
            keywords=keywords,
            entities=entities,
            zone=zone,
            issue_categories=issue_categories,
            total_latency_ms=total_latency,
            cache_latency_ms=result["latencies"]["cache"],
            vector_latency_ms=result["latencies"]["vector"] if result["latencies"]["vector"] > 0 else None,
            synthesis_latency_ms=result["latencies"]["synthesis"],
            cache_hits=len(cache_results),
            cache_blocks_used=[b.topic for b in cache_results],
            confidence_scores={"overall": confidence},
            vector_used=len(result["vector_results"]) > 0,
            vector_results_count=len(result["vector_results"]),
            response_mode=req.mode.value,
            response_length=len(response_text),
            authorities_cited=authorities,
            fragility_score=fragility,
            determinism_hash=determ_hash,
            doctrine_coverage=[b.topic for b in cache_results],
            epistemic_gaps=epistemic_gaps
        )
        telemetry.record_query(trace)

        # Drift detection
        if cache_results:
            drift_watcher.detect_drift(
                cache_results[0].topic,
                response_text
            )

        return QueryResponse(
            query_id=query_id,
            query=req.query,
            response=response_text,
            mode=req.mode,
            confidence_level=conf_level,
            confidence_score=round(confidence, 3),
            doctrines_used=doctrine_refs,
            authorities_cited=authorities,
            issue_categories=issue_categories,
            fragility_score=round(fragility, 3),
            epistemic_gaps=epistemic_gaps,
            disclosure_caveat=disclosure,
            performance=performance,
            determinism_hash=determ_hash,
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        last_error = str(e)
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# HEALTH & METRICS ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthStatus)
async def health_check() -> HealthStatus:
    """Engine health check endpoint."""
    uptime = (datetime.utcnow() - start_time).total_seconds()
    metrics = telemetry.get_metrics()

    return HealthStatus(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        uptime_seconds=round(uptime, 2),
        queries_processed=metrics["query_count"],
        cache_hit_rate=metrics["cache_hit_rate"],
        avg_latency_ms=metrics["avg_latency_ms"],
        doctrine_count=len(DOCTRINE_CACHE),
        last_error=last_error
    )


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Retrieve detailed telemetry metrics."""
    return telemetry.get_metrics()


@app.get("/coverage")
async def get_coverage() -> Dict[str, Any]:
    """Retrieve doctrine coverage map."""
    return telemetry.get_coverage_map()


@app.get("/doctrines")
async def list_doctrines() -> Dict[str, Any]:
    """List all doctrine blocks."""
    return {
        "count": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": block.topic,
                "category": block.issue_category.value,
                "confidence": block.confidence.value,
                "keywords": block.keywords,
                "authority_count": len(block.primary_authority)
            }
            for block in DOCTRINE_CACHE
        ]
    }


# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Engine startup initialization."""
    logger.info(f"Starting {ENGINE_NAME} v{VERSION}")
    logger.info(f"Port: {PORT}")
    logger.info(f"Doctrine blocks loaded: {len(DOCTRINE_CACHE)}")
    logger.info(f"Vector search enabled: {vector_search.enabled}")
    logger.info(f"Telemetry enabled: {telemetry.enabled}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
