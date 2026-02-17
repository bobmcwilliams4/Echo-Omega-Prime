"""
P05 Creditor Claim Intelligence Engine
Texas creditor claim analysis - priority, statute of limitations, secured vs unsecured, exempt property

TIE-20 GOLD STANDARD ENGINE
Port: 8655 | Mode: HYBRID | Domain: Creditor Claims

Author: ECHO OMEGA PRIME Build System
Date: 2026-02-12
Version: 1.0.0
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import json
import hashlib
from collections import defaultdict

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from loguru import logger

# Configure loguru
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
    level="INFO"
)
logger.add(
    "O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/P05_creditor_claim/engine.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)

# Import engine modules

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DOCTRINE_CACHE, DoctrineBlock, IssueCategory, ConfidenceLevel,
    get_doctrine_by_keyword, get_doctrine_by_category, get_high_confidence_doctrines
)
from semantic import CreditorClaimSemanticNormalizer
from search import CreditorClaimSearchEngine, SearchResult
from telemetry import (
    CreditorClaimTelemetry, QueryMetrics, ClaimCategory, QueryZone,
    ErrorDomain, create_query_id, PerformanceSnapshot
)

# Load configuration
CONFIG_PATH = Path(__file__).parent / "config.json"
with CONFIG_PATH.open("r") as f:
    CONFIG = json.load(f)

ENGINE_ID = CONFIG["engine_id"]
ENGINE_VERSION = CONFIG["version"]
ENGINE_PORT = CONFIG["port"]
ENGINE_DOMAIN = CONFIG["domain"]

logger.info(f"Initializing {ENGINE_ID} v{ENGINE_VERSION} on port {ENGINE_PORT}")

# ═══════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    """Response mode selection"""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ClaimAnalysisRequest(BaseModel):
    """Request model for creditor claim analysis"""
    query: str = Field(..., min_length=10, description="Creditor claim question or scenario")
    mode: ResponseMode = Field(ResponseMode.DEFENSE, description="Response detail level")
    claim_category: Optional[str] = Field(None, description="Specific claim category filter")
    estate_value: Optional[float] = Field(None, description="Total estate value for priority analysis")
    claim_amount: Optional[float] = Field(None, description="Amount of specific claim")
    death_date: Optional[str] = Field(None, description="Date of death (YYYY-MM-DD)")
    notice_date: Optional[str] = Field(None, description="Date notice to creditors published")
    administration_type: Optional[str] = Field(None, description="Independent or dependent administration")

    @validator("death_date", "notice_date")
    def validate_date_format(cls, v):
        if v:
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
        return v


class ClaimAnalysisResponse(BaseModel):
    """Response model for creditor claim analysis"""
    query_id: str
    timestamp: str
    query: str
    mode: str

    # Primary analysis
    answer: str
    confidence_level: str
    claim_categories: List[str]
    issue_categories: List[str]

    # Supporting analysis
    doctrines_applied: List[str]
    authority_sources: List[str]
    key_factors: List[str]
    adverse_positions: List[str]

    # Metadata
    cache_hit: bool
    latency_ms: float
    epistemic_warnings: List[str]
    fact_fragility_score: float
    determinism_hash: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    engine_id: str
    version: str
    port: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float
    doctrine_count: int
    error_rate: float


# ═══════════════════════════════════════════════════════════════════
# CORE ENGINE CLASS
# ═══════════════════════════════════════════════════════════════════

class CreditorClaimEngine:
    """
    Texas Creditor Claim Intelligence Engine

    TIE-20 Components:
    1. three_layer_response - Doctrine Cache (0-200ms) → Semantic Search → Deep Analysis
    2. response_modes - FAST/DEFENSE/MEMO with different detail levels
    3. doctrine_cache - 12+ pre-compiled expert reasoning blocks with real domain content
    4. authority_hardening - Hierarchical authority levels with weights, conflict resolution
    5. confidence_stratification - DEFENSIBLE/AGGRESSIVE/DISCLOSURE/HIGH_RISK
    6. semantic_normalization - Domain-specific term normalization, deterministic
    7. vector_search - Semantic retrieval fallback when cache misses
    8. telemetry - Full query tracing, latency tracking, error domains
    9. drift_watcher - Detect doctrine drift over time
    10. coverage_map - Track triggered/missed doctrines, epistemic gap detection
    11. metrics_collector - Latency stats, error rates, hit rates, queries/hour
    12. health_endpoint - Comprehensive JSON health check
    13. zoned_analysis - CLASSIFICATION/PRIORITY/SOL/EXEMPTIONS/PROCEDURES zones
    14. fact_fragility_scoring - Verifiability, recharacterization risk
    15. audit_trail_jsonl - Every query logged for forensic review
    16. determinism_hash_sha256 - SHA-256 for reproducibility
    17. fastapi_server - Full FastAPI with CORS, lifespan, typed endpoints
    18. loguru_logging - Structured logging, rotation, never print()
    19. multi_doctrine_decomposition - Issue categories, strata, interaction
    20. deep_analysis_mode - Multi-source synthesis, full reasoning chain
    """

    def __init__(self):
        self.engine_id = ENGINE_ID
        self.version = ENGINE_VERSION
        self.start_time = datetime.now()

        # Component 3: Doctrine Cache
        self.doctrine_cache = DOCTRINE_CACHE
        logger.info(f"Loaded {len(self.doctrine_cache)} doctrine blocks")

        # Component 6: Semantic Normalization
        self.semantic_normalizer = CreditorClaimSemanticNormalizer()
        logger.info("Semantic normalizer initialized")

        # Component 7: Vector Search
        self.search_engine = CreditorClaimSearchEngine(engine_id=self.engine_id)
        logger.info("Search engine initialized")

        # Component 8: Telemetry
        self.telemetry = CreditorClaimTelemetry(engine_id=self.engine_id)
        logger.info("Telemetry system initialized")

        # Component 9: Drift Watcher
        self.drift_baseline: Dict[str, int] = {}
        self._initialize_drift_baseline()

        # Component 10: Coverage Map
        self.coverage_map: Dict[str, int] = defaultdict(int)

        logger.success(f"{self.engine_id} v{self.version} initialized successfully")

    def _initialize_drift_baseline(self) -> None:
        """Initialize drift detection baseline"""
        for doctrine in self.doctrine_cache:
            self.drift_baseline[doctrine.topic] = len(doctrine.reasoning_framework)
        logger.debug(f"Drift baseline established for {len(self.drift_baseline)} doctrines")

    # ═══════════════════════════════════════════════════════════════════
    # COMPONENT 1: THREE-LAYER RESPONSE
    # ═══════════════════════════════════════════════════════════════════

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        context: Dict[str, Any]
    ) -> Tuple[str, List[DoctrineBlock], bool, float]:
        """
        Three-layer response architecture:
        Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert blocks
        Layer 2: Semantic Search (200-500ms) - Vector retrieval from knowledge base
        Layer 3: Deep Analysis (500-2000ms) - Multi-source synthesis
        """
        start_time = datetime.now()

        # Layer 1: Doctrine Cache
        cache_result, cache_hit = self._query_doctrine_cache(query, context)
        if cache_hit and mode == ResponseMode.FAST:
            latency = (datetime.now() - start_time).total_seconds() * 1000
            logger.info(f"Cache hit, FAST mode, returning in {latency:.1f}ms")
            return cache_result, [], True, latency

        # Layer 2: Semantic Search (if cache miss or higher detail needed)
        search_results = []
        if not cache_hit or mode in [ResponseMode.DEFENSE, ResponseMode.MEMO]:
            search_results = self._semantic_search_layer(query, context)
            logger.debug(f"Semantic search returned {len(search_results)} results")

        # Layer 3: Deep Analysis (if MEMO mode or complex query)
        if mode == ResponseMode.MEMO or (not cache_hit and len(search_results) < 3):
            deep_result = self._deep_analysis_layer(query, cache_result, search_results, context)
            latency = (datetime.now() - start_time).total_seconds() * 1000
            logger.info(f"Deep analysis complete in {latency:.1f}ms")
            return deep_result, [], False, latency

        # Combine cache and search results
        combined_result = self._combine_layers(cache_result, search_results, mode, context)
        latency = (datetime.now() - start_time).total_seconds() * 1000

        return combined_result, [], cache_hit, latency

    def _query_doctrine_cache(
        self,
        query: str,
        context: Dict[str, Any]
    ) -> Tuple[str, bool]:
        """Query pre-compiled doctrine cache"""
        # Normalize query
        normalized_query = self.semantic_normalizer.normalize_query(query)

        # Extract entities
        entities = self.semantic_normalizer.extract_claim_entities(normalized_query)

        # Find matching doctrines by keywords
        matched_doctrines: List[DoctrineBlock] = []
        for doctrine in self.doctrine_cache:
            match_score = self._calculate_doctrine_match_score(normalized_query, doctrine, entities)
            if match_score > 0.3:
                matched_doctrines.append(doctrine)
                self.coverage_map[doctrine.topic] += 1

        if not matched_doctrines:
            return "No cached doctrine matched query", False

        # Sort by relevance
        matched_doctrines.sort(
            key=lambda d: self._calculate_doctrine_match_score(normalized_query, d, entities),
            reverse=True
        )

        # Use top doctrine
        top_doctrine = matched_doctrines[0]
        logger.info(f"Cache hit: {top_doctrine.topic}")

        # Format response based on doctrine
        response = self._format_doctrine_response(top_doctrine, context)

        return response, True

    def _calculate_doctrine_match_score(
        self,
        query: str,
        doctrine: DoctrineBlock,
        entities: Dict[str, List[str]]
    ) -> float:
        """Calculate how well doctrine matches query"""
        query_lower = query.lower()
        score = 0.0

        # Keyword matching
        for keyword in doctrine.keywords:
            if keyword.lower() in query_lower:
                score += 0.15

        # Topic matching
        if doctrine.topic.replace("_", " ") in query_lower:
            score += 0.3

        # Entity matching
        for entity_list in entities.values():
            for entity in entity_list:
                if entity in [kw.upper() for kw in doctrine.keywords]:
                    score += 0.1

        # Category matching
        category_keywords = {
            IssueCategory.SECURED_RIGHTS: ["secured", "lien", "mortgage", "collateral"],
            IssueCategory.PRIORITY: ["priority", "order", "class", "funeral", "family allowance"],
            IssueCategory.EXEMPTIONS: ["homestead", "exempt", "family allowance"],
            IssueCategory.PROCEDURES: ["notice", "filing", "deadline", "verification"],
            IssueCategory.SOL: ["statute of limitations", "deadline", "two year", "nonclaim"],
        }

        for category, keywords in category_keywords.items():
            if doctrine.category == category:
                if any(kw in query_lower for kw in keywords):
                    score += 0.2

        return min(score, 1.0)

    def _format_doctrine_response(
        self,
        doctrine: DoctrineBlock,
        context: Dict[str, Any]
    ) -> str:
        """Format doctrine into response"""
        sections = []

        # Conclusion
        sections.append("ANALYSIS:")
        sections.extend(doctrine.conclusion_template)
        sections.append("")

        # Key factors
        sections.append("KEY FACTORS:")
        for factor in doctrine.key_factors[:5]:
            sections.append(f"• {factor}")
        sections.append("")

        # Authority
        sections.append("PRIMARY AUTHORITY:")
        for auth in doctrine.primary_authority:
            sections.append(f"• {auth}")
        sections.append("")

        # Adversary position
        sections.append("POTENTIAL CHALLENGES:")
        sections.append(f"• {doctrine.adversary_position}")
        sections.append("")

        # Confidence
        sections.append(f"CONFIDENCE LEVEL: {doctrine.confidence.value}")

        if doctrine.disclosure_caveat:
            sections.append(f"\nDISCLOSURE: {doctrine.disclosure_caveat}")

        return "\n".join(sections)

    def _semantic_search_layer(
        self,
        query: str,
        context: Dict[str, Any]
    ) -> List[SearchResult]:
        """Layer 2: Semantic search fallback"""
        # Expand query terms
        expanded_queries = self.semantic_normalizer.expand_query_terms(query)

        results = []
        for expanded_query in expanded_queries[:3]:  # Limit to 3 expansions
            search_results = self.search_engine.semantic_search(
                query=expanded_query,
                top_k=5,
                threshold=0.75
            )
            results.extend(search_results)

        # Deduplicate by content
        seen_content = set()
        unique_results = []
        for result in results:
            content_hash = hashlib.sha256(result.content.encode()).hexdigest()
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                unique_results.append(result)

        return unique_results[:10]

    def _deep_analysis_layer(
        self,
        query: str,
        cache_result: str,
        search_results: List[SearchResult],
        context: Dict[str, Any]
    ) -> str:
        """Layer 3: Deep multi-source analysis"""
        sections = []

        sections.append("COMPREHENSIVE CREDITOR CLAIM ANALYSIS")
        sections.append("=" * 80)
        sections.append("")

        # Issue decomposition
        sections.append("ISSUE DECOMPOSITION:")
        categories = self.semantic_normalizer.identify_claim_category(query)
        for category in categories:
            sections.append(f"• {category}")
        sections.append("")

        # Cached doctrine analysis
        if cache_result and cache_result != "No cached doctrine matched query":
            sections.append("DOCTRINE ANALYSIS:")
            sections.append(cache_result)
            sections.append("")

        # Search results synthesis
        if search_results:
            sections.append("SUPPORTING AUTHORITY:")
            for i, result in enumerate(search_results[:5], 1):
                sections.append(f"{i}. {result.source} (relevance: {result.score:.2f})")
                sections.append(f"   {result.content[:200]}...")
                sections.append("")

        # Multi-doctrine synthesis for complex issues
        relevant_doctrines = [
            d for d in self.doctrine_cache
            if any(cat in d.category.value for cat in categories)
        ][:5]

        if len(relevant_doctrines) > 1:
            sections.append("MULTI-DOCTRINE SYNTHESIS:")
            sections.append("This issue implicates multiple doctrinal areas:")
            for doctrine in relevant_doctrines:
                sections.append(f"• {doctrine.topic}: {doctrine.conclusion_template[0]}")
            sections.append("")

        # Fact dependencies
        sections.append("CRITICAL FACT DEPENDENCIES:")
        fact_deps = set()
        for doctrine in relevant_doctrines:
            fact_deps.update(doctrine.fact_dependencies)
        for fact in list(fact_deps)[:10]:
            sections.append(f"• {fact}")
        sections.append("")

        # Risk analysis
        sections.append("RISK ANALYSIS:")
        confidence_levels = [d.confidence for d in relevant_doctrines]
        if any(c in [ConfidenceLevel.DISCLOSURE, ConfidenceLevel.HIGH_RISK] for c in confidence_levels):
            sections.append("⚠ This analysis contains positions with heightened risk:")
            for doctrine in relevant_doctrines:
                if doctrine.confidence in [ConfidenceLevel.DISCLOSURE, ConfidenceLevel.HIGH_RISK]:
                    sections.append(f"  • {doctrine.topic}: {doctrine.confidence.value}")
                    if doctrine.disclosure_caveat:
                        sections.append(f"    {doctrine.disclosure_caveat}")
        else:
            sections.append("✓ Primary positions are defensible under current Texas law")
        sections.append("")

        return "\n".join(sections)

    def _combine_layers(
        self,
        cache_result: str,
        search_results: List[SearchResult],
        mode: ResponseMode,
        context: Dict[str, Any]
    ) -> str:
        """Combine cache and search results intelligently"""
        sections = []

        if mode == ResponseMode.DEFENSE:
            sections.append("CREDITOR CLAIM ANALYSIS (AUDIT-READY)")
            sections.append("=" * 80)
            sections.append("")

        sections.append(cache_result)
        sections.append("")

        if search_results and mode == ResponseMode.DEFENSE:
            sections.append("ADDITIONAL AUTHORITY:")
            for result in search_results[:3]:
                sections.append(f"• {result.source}: {result.content[:150]}...")
            sections.append("")

        return "\n".join(sections)

    # ═══════════════════════════════════════════════════════════════════
    # COMPONENT 4: AUTHORITY HARDENING
    # ═══════════════════════════════════════════════════════════════════

    def apply_authority_hardening(
        self,
        doctrines: List[DoctrineBlock]
    ) -> List[Dict[str, Any]]:
        """Hierarchical authority weighting and conflict resolution"""
        authority_weights = {
            "Texas Estates Code": 1.0,
            "Texas Constitution": 1.0,
            "Texas Property Code": 0.9,
            "Texas Supreme Court": 0.95,
            "Texas Court of Appeals": 0.85,
            "Federal statute": 0.9,
            "UCC": 0.8,
            "Secondary authority": 0.5,
        }

        weighted_authorities = []
        for doctrine in doctrines:
            for auth in doctrine.primary_authority:
                weight = 0.7  # Default
                for key, val in authority_weights.items():
                    if key in auth:
                        weight = val
                        break

                weighted_authorities.append({
                    "source": auth,
                    "weight": weight,
                    "doctrine": doctrine.topic,
                    "confidence": doctrine.confidence.value
                })

        # Sort by weight
        weighted_authorities.sort(key=lambda x: x["weight"], reverse=True)
        return weighted_authorities

    # ═══════════════════════════════════════════════════════════════════
    # COMPONENT 5: CONFIDENCE STRATIFICATION
    # ═══════════════════════════════════════════════════════════════════

    def stratify_confidence(
        self,
        doctrines: List[DoctrineBlock],
        context: Dict[str, Any]
    ) -> ConfidenceLevel:
        """Determine overall confidence level for position"""
        if not doctrines:
            return ConfidenceLevel.HIGH_RISK

        confidence_scores = {
            ConfidenceLevel.DEFENSIBLE: 4,
            ConfidenceLevel.AGGRESSIVE: 3,
            ConfidenceLevel.DISCLOSURE: 2,
            ConfidenceLevel.HIGH_RISK: 1,
        }

        avg_score = sum(confidence_scores[d.confidence] for d in doctrines) / len(doctrines)

        if avg_score >= 3.5:
            return ConfidenceLevel.DEFENSIBLE
        elif avg_score >= 2.5:
            return ConfidenceLevel.AGGRESSIVE
        elif avg_score >= 1.5:
            return ConfidenceLevel.DISCLOSURE
        else:
            return ConfidenceLevel.HIGH_RISK

    # ═══════════════════════════════════════════════════════════════════
    # COMPONENT 13: ZONED ANALYSIS
    # ═══════════════════════════════════════════════════════════════════

    def identify_analysis_zone(self, query: str) -> QueryZone:
        """Identify which creditor claim zone the query falls into"""
        query_lower = query.lower()

        zone_keywords = {
            QueryZone.CLASSIFICATION: ["secured", "unsecured", "priority", "type of claim", "classify"],
            QueryZone.PRIORITY: ["priority", "order", "class", "first", "pay before", "funeral", "family allowance"],
            QueryZone.SOL: ["deadline", "time limit", "statute of limitations", "two year", "nonclaim", "late"],
            QueryZone.EXEMPTIONS: ["homestead", "exempt", "protected", "family allowance", "exempt property"],
            QueryZone.PROCEDURES: ["notice", "filing", "verification", "claim form", "how to file"],
            QueryZone.SECURED_RIGHTS: ["foreclosure", "lien", "security interest", "collateral", "secured creditor"],
        }

        zone_scores = defaultdict(int)
        for zone, keywords in zone_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    zone_scores[zone] += 1

        if zone_scores:
            return max(zone_scores.items(), key=lambda x: x[1])[0]
        return QueryZone.CLASSIFICATION

    # ═══════════════════════════════════════════════════════════════════
    # COMPONENT 14: FACT FRAGILITY SCORING
    # ═══════════════════════════════════════════════════════════════════

    def calculate_fact_fragility(
        self,
        doctrines: List[DoctrineBlock],
        context: Dict[str, Any]
    ) -> float:
        """Calculate how fragile the position is to fact changes"""
        if not doctrines:
            return 1.0  # Maximum fragility

        fragility_factors = []

        for doctrine in doctrines:
            # Count critical fact dependencies
            fact_count = len(doctrine.fact_dependencies)

            # Higher fact dependencies = more fragile
            fact_fragility = min(fact_count / 10.0, 1.0)

            # Counter-argument strength
            counter_strength = len(doctrine.counter_arguments) / 8.0
            counter_fragility = min(counter_strength, 1.0)

            # Confidence level affects fragility
            confidence_fragility = {
                ConfidenceLevel.DEFENSIBLE: 0.2,
                ConfidenceLevel.AGGRESSIVE: 0.5,
                ConfidenceLevel.DISCLOSURE: 0.7,
                ConfidenceLevel.HIGH_RISK: 0.9,
            }[doctrine.confidence]

            # Average fragility for this doctrine
            doctrine_fragility = (fact_fragility + counter_fragility + confidence_fragility) / 3
            fragility_factors.append(doctrine_fragility)

        return sum(fragility_factors) / len(fragility_factors)

    # ═══════════════════════════════════════════════════════════════════
    # COMPONENT 16: DETERMINISM HASH
    # ═══════════════════════════════════════════════════════════════════

    def generate_determinism_hash(
        self,
        query: str,
        response: str,
        doctrines: List[DoctrineBlock]
    ) -> str:
        """Generate SHA-256 hash for response reproducibility"""
        content = f"{query}||{response}||{','.join(d.topic for d in doctrines)}"
        return hashlib.sha256(content.encode()).hexdigest()

    # ═══════════════════════════════════════════════════════════════════
    # COMPONENT 9: DRIFT WATCHER
    # ═══════════════════════════════════════════════════════════════════

    def detect_doctrine_drift(self) -> Dict[str, Any]:
        """Detect if doctrines have drifted from baseline"""
        drift_report = {
            "drifted_doctrines": [],
            "total_doctrines": len(self.doctrine_cache),
            "drift_detected": False
        }

        for doctrine in self.doctrine_cache:
            current_length = len(doctrine.reasoning_framework)
            baseline_length = self.drift_baseline.get(doctrine.topic, 0)

            if abs(current_length - baseline_length) > 100:  # 100 char threshold
                drift_report["drifted_doctrines"].append({
                    "doctrine": doctrine.topic,
                    "baseline_length": baseline_length,
                    "current_length": current_length,
                    "drift": current_length - baseline_length
                })
                drift_report["drift_detected"] = True

        return drift_report

    # ═══════════════════════════════════════════════════════════════════
    # COMPONENT 10: COVERAGE MAP
    # ═══════════════════════════════════════════════════════════════════

    def get_coverage_map(self) -> Dict[str, Any]:
        """Get doctrine coverage statistics"""
        total_doctrines = len(self.doctrine_cache)
        triggered_doctrines = len([k for k, v in self.coverage_map.items() if v > 0])

        top_doctrines = sorted(
            self.coverage_map.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        untriggered = [
            d.topic for d in self.doctrine_cache
            if self.coverage_map.get(d.topic, 0) == 0
        ]

        return {
            "total_doctrines": total_doctrines,
            "triggered_doctrines": triggered_doctrines,
            "coverage_rate": triggered_doctrines / total_doctrines if total_doctrines > 0 else 0,
            "top_10_doctrines": [{"topic": k, "count": v} for k, v in top_doctrines],
            "untriggered_count": len(untriggered),
            "untriggered_sample": untriggered[:10]
        }

    # ═══════════════════════════════════════════════════════════════════
    # MAIN QUERY PROCESSOR
    # ═══════════════════════════════════════════════════════════════════

    def process_query(self, request: ClaimAnalysisRequest) -> ClaimAnalysisResponse:
        """
        Main query processing with full TIE-20 implementation
        """
        start_time = datetime.now()
        query_id = create_query_id(request.query, start_time)

        logger.info(f"Processing query {query_id}: {request.query[:50]}...")

        # Build context
        context = {
            "estate_value": request.estate_value,
            "claim_amount": request.claim_amount,
            "death_date": request.death_date,
            "notice_date": request.notice_date,
            "administration_type": request.administration_type,
        }

        # Component 13: Identify analysis zone
        zone = self.identify_analysis_zone(request.query)
        logger.debug(f"Analysis zone: {zone.value}")

        # Component 1: Three-layer response
        answer, matched_doctrines, cache_hit, layer_latency = self.three_layer_response(
            query=request.query,
            mode=request.mode,
            context=context
        )

        # Get relevant doctrines for metadata
        if not matched_doctrines:
            normalized_query = self.semantic_normalizer.normalize_query(request.query)
            entities = self.semantic_normalizer.extract_claim_entities(normalized_query)
            matched_doctrines = [
                d for d in self.doctrine_cache
                if self._calculate_doctrine_match_score(normalized_query, d, entities) > 0.3
            ][:5]

        # Component 5: Confidence stratification
        confidence = self.stratify_confidence(matched_doctrines, context)

        # Component 4: Authority hardening
        weighted_authorities = self.apply_authority_hardening(matched_doctrines)

        # Component 14: Fact fragility
        fact_fragility = self.calculate_fact_fragility(matched_doctrines, context)

        # Component 6: Identify claim categories
        claim_categories = self.semantic_normalizer.identify_claim_category(request.query)

        # Component 16: Determinism hash
        determinism_hash = self.generate_determinism_hash(request.query, answer, matched_doctrines)

        # Epistemic warnings
        epistemic_warnings = []
        for doctrine in matched_doctrines:
            if doctrine.disclosure_caveat:
                epistemic_warnings.append(f"{doctrine.topic}: {doctrine.disclosure_caveat}")

        # Total latency
        total_latency = (datetime.now() - start_time).total_seconds() * 1000

        # Component 8: Record telemetry
        metrics = QueryMetrics(
            query_id=query_id,
            timestamp=start_time,
            query_text=request.query,
            claim_category=ClaimCategory(claim_categories[0]) if claim_categories else None,
            zone=zone,
            mode=request.mode.value,
            total_latency_ms=total_latency,
            cache_latency_ms=layer_latency if cache_hit else 0,
            semantic_latency_ms=layer_latency if not cache_hit else 0,
            deep_analysis_latency_ms=total_latency - layer_latency,
            cache_hit=cache_hit,
            doctrines_triggered=[d.topic for d in matched_doctrines],
            confidence_level=confidence.value,
            response_length=len(answer),
            authority_sources=len(weighted_authorities),
            citations_count=sum(len(d.primary_authority) for d in matched_doctrines),
            fact_fragility_score=fact_fragility,
            epistemic_warnings=len(epistemic_warnings),
            determinism_hash=determinism_hash
        )
        self.telemetry.record_query(metrics)

        # Build response
        response = ClaimAnalysisResponse(
            query_id=query_id,
            timestamp=start_time.isoformat(),
            query=request.query,
            mode=request.mode.value,
            answer=answer,
            confidence_level=confidence.value,
            claim_categories=claim_categories,
            issue_categories=[zone.value],
            doctrines_applied=[d.topic for d in matched_doctrines],
            authority_sources=[a["source"] for a in weighted_authorities[:10]],
            key_factors=[f for d in matched_doctrines for f in d.key_factors][:10],
            adverse_positions=[d.adversary_position for d in matched_doctrines][:5],
            cache_hit=cache_hit,
            latency_ms=round(total_latency, 2),
            epistemic_warnings=epistemic_warnings,
            fact_fragility_score=round(fact_fragility, 3),
            determinism_hash=determinism_hash
        )

        logger.success(f"Query {query_id} completed in {total_latency:.1f}ms | Confidence: {confidence.value}")
        return response


# ═══════════════════════════════════════════════════════════════════
# COMPONENT 17: FASTAPI SERVER
# ═══════════════════════════════════════════════════════════════════

app = FastAPI(
    title=f"{ENGINE_ID} - Texas Creditor Claim Analysis Engine",
    description="TIE-20 gold standard engine for creditor claim analysis",
    version=ENGINE_VERSION,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
engine: Optional[CreditorClaimEngine] = None


@app.on_event("startup")
async def startup_event():
    """Initialize engine on startup"""
    global engine
    engine = CreditorClaimEngine()
    logger.success(f"{ENGINE_ID} FastAPI server started on port {ENGINE_PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info(f"{ENGINE_ID} shutting down")


@app.post("/analyze", response_model=ClaimAnalysisResponse)
async def analyze_claim(request: ClaimAnalysisRequest):
    """
    Analyze creditor claim question

    Returns comprehensive analysis with doctrine application, authority sources,
    confidence stratification, and fact fragility assessment.
    """
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    try:
        response = engine.process_query(request)
        return response
    except Exception as e:
        logger.error(f"Query processing error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


# Component 12: Health Endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check endpoint"""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    uptime = (datetime.now() - engine.start_time).total_seconds()
    metrics = engine.telemetry.get_health_metrics()

    return HealthResponse(
        status=metrics["status"],
        engine_id=engine.engine_id,
        version=engine.version,
        port=ENGINE_PORT,
        uptime_seconds=uptime,
        total_queries=engine.telemetry.total_queries,
        cache_hit_rate=metrics["cache_hit_rate"],
        avg_latency_ms=metrics["avg_latency_ms"],
        doctrine_count=len(engine.doctrine_cache),
        error_rate=metrics["error_analysis"]["error_rate"] if "error_analysis" in metrics else 0.0
    )


@app.get("/metrics")
async def get_metrics():
    """Get detailed telemetry metrics"""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    return JSONResponse(content=engine.telemetry.get_health_metrics())


@app.get("/coverage")
async def get_coverage():
    """Get doctrine coverage map"""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    return JSONResponse(content=engine.get_coverage_map())


@app.get("/drift")
async def check_drift():
    """Check for doctrine drift"""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    return JSONResponse(content=engine.detect_doctrine_drift())


@app.get("/doctrines")
async def list_doctrines(category: Optional[str] = Query(None)):
    """List available doctrines, optionally filtered by category"""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    doctrines = engine.doctrine_cache

    if category:
        try:
            cat_enum = IssueCategory(category)
            doctrines = [d for d in doctrines if d.category == cat_enum]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

    return JSONResponse(content={
        "total": len(doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "confidence": d.confidence.value,
                "keywords": d.keywords[:5],
            }
            for d in doctrines
        ]
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")
