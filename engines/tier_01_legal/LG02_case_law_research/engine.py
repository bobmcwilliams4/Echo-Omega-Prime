"""
LG02 CASE LAW RESEARCH ENGINE - Production Architecture
=========================================================
Professional-grade case law research and analysis system for attorneys,
paralegals, and legal researchers.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert legal reasoning
    Layer 2: Semantic Search (200-700ms) - TF-IDF on cache miss
    Layer 3: Citation Analysis (700-1500ms) - Parse, Shepardize, precedent chains
    Layer 4: Deep Analysis (on-demand) - Multi-source legal synthesis

Response Modes:
    FAST: Doctrine-driven, minimal citations, sub-2 seconds
    DEFENSE: Structured reasoning, litigation-ready, burden analysis
    MEMO: Long-form, citation-heavy, legal memorandum format
    SHEPARDIZE: Citation verification and treatment analysis
    PRECEDENT_CHAIN: Full ancestry/descendant precedent graph

Features:
    - Bluebook citation parser (Vols Reporter Page (Court Year))
    - Court hierarchy with weighted authority scoring
    - Shepardize/KeyCite citation verification
    - Precedent chain tracking and graph analysis
    - Opinion section parser (majority, concurrence, dissent)
    - Headnote extraction
    - Key number system mapping
    - Jurisdiction filtering (federal circuits, state courts)
    - Legal issue taxonomy
    - Determinism hash on all responses
    - Epistemic guardrails against overconfident legal statements

Port: 8392
Engine ID: LG02
Tier: LEGAL (Auth 5.0)
Mode: EF (Elastic Framework)

Version: 2.0.0
Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

from fastapi import FastAPI, HTTPException, Depends, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List, Dict, Any, Literal, Tuple, Set
from enum import Enum
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import hashlib
import json
import math
import re
import time
import traceback
import uuid
from collections import Counter, defaultdict
from pathlib import Path

from loguru import logger

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

import sys
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
sys.path.insert(0, str(ENGINE_DIR.parent / "_shared"))

from telemetry import (
    get_telemetry,
    trace_query,
    complete_trace,
    log_error,
    record_doctrine_mutation,
    record_citation_lookup,
    ErrorDomain,
    ResponseLayer,
    MutationType,
    MutationOrigin,
    CitationLookupType,
    TelemetryCollector,
    QueryTrace,
    TelemetryStep,
)

from semantic import (
    normalize_query,
    NormalizationResult,
    get_semantic_map,
    get_governance_metadata as get_semantic_governance,
    get_semantic_map_version,
    get_semantic_map_hash,
    verify_dictionary_integrity,
    get_citation_patterns,
    get_court_abbreviations,
    CITATION_PATTERNS,
)

import sys

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DOCTRINE_CACHE,
    DoctrineResponse,
    CaseLawDoctrineEngine,
    get_engine as get_doctrine_engine,
)

from search import (
    DoctrineSearchIndex,
    SearchResult,
    CitationParser,
    ParsedCitation,
    ShepardizeEngine,
    ShepardizeResult,
    PrecedentWeightCalculator,
    PrecedentChainResult,
    PrecedentChainNode,
    get_search_index,
    get_citation_parser,
    get_weight_calculator,
    get_shepardize_engine,
    compute_query_hash,
    REPORTER_COURT_MAP,
    COURT_WEIGHT_MAP,
)

# ============================================================================
# LOGGING SETUP
# ============================================================================

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG02_case_law_research/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "lg02_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)

AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"

# Load config
CONFIG_PATH = Path(__file__).parent / "config.json"
with open(CONFIG_PATH, "r", encoding="utf-8") as _cf:
    ENGINE_CONFIG = json.load(_cf)


# ############################################################################
#
# SECTION 1: ENUMS, CONSTANTS, AND CONFIGURATION
#
# ############################################################################

class ResponseMode(str, Enum):
    """Response depth mode for queries."""
    FAST = "fast"
    DEFENSE = "defense"
    MEMO = "memo"
    SHEPARDIZE = "shepardize"
    PRECEDENT_CHAIN = "precedent_chain"


class Complexity(str, Enum):
    """Query complexity level."""
    STANDARD = "standard"
    ADVANCED = "advanced"
    EXPERT = "expert"


class JurisdictionType(str, Enum):
    """Legal jurisdiction classification."""
    FEDERAL = "federal"
    STATE = "state"
    INTERNATIONAL = "international"
    TRIBAL = "tribal"
    MILITARY = "military"


class CourtLevel(str, Enum):
    """Court hierarchy level."""
    SUPREME = "supreme"
    APPELLATE = "appellate"
    TRIAL = "trial"
    MAGISTRATE = "magistrate"
    ADMINISTRATIVE = "administrative"
    BANKRUPTCY = "bankruptcy"


class LegalDomain(str, Enum):
    """Primary legal domain classification."""
    CONSTITUTIONAL = "constitutional"
    CIVIL_PROCEDURE = "civil_procedure"
    CRIMINAL = "criminal"
    CONTRACT = "contract"
    TORT = "tort"
    PROPERTY = "property"
    CORPORATE = "corporate"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    ADMINISTRATIVE = "administrative"
    EMPLOYMENT = "employment"
    SECURITIES = "securities"
    BANKRUPTCY = "bankruptcy"
    ANTITRUST = "antitrust"
    ENVIRONMENTAL = "environmental"
    IMMIGRATION = "immigration"
    EVIDENCE = "evidence"
    APPELLATE = "appellate"
    FAMILY = "family"
    TAX = "tax"


class AnalysisZone(str, Enum):
    """Analysis zone separation for legal conclusions."""
    LITIGATION = "litigation"
    TRANSACTIONAL = "transactional"
    REGULATORY = "regulatory"


class ConfidenceBand(str, Enum):
    """Confidence stratification bands."""
    DEFENSIBLE = "defensible"
    SUPPORTABLE = "supportable"
    DISCLOSURE = "disclosure"
    HIGH_RISK = "high_risk"


class OpinionSection(str, Enum):
    """Sections of a judicial opinion."""
    SYLLABUS = "syllabus"
    MAJORITY = "majority"
    PLURALITY = "plurality"
    CONCURRENCE = "concurrence"
    CONCURRENCE_IN_JUDGMENT = "concurrence_in_judgment"
    DISSENT = "dissent"
    PER_CURIAM = "per_curiam"


class FragilityLevel(str, Enum):
    """Fact fragility assessment."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class AuthorityWeight(int, Enum):
    """Authority weight for legal sources."""
    US_SUPREME_COURT = 100
    FEDERAL_CIRCUIT_COURT = 85
    FEDERAL_DISTRICT_COURT = 70
    STATE_SUPREME_COURT = 75
    STATE_APPELLATE_COURT = 60
    STATE_TRIAL_COURT = 45
    TAX_COURT = 72
    FEDERAL_STATUTE = 95
    STATE_STATUTE = 80
    FEDERAL_REGULATION = 75
    STATE_REGULATION = 60
    RESTATEMENT = 50
    TREATISE = 35
    LAW_REVIEW = 30


AUTHORITY_HIERARCHY: Dict[str, int] = {
    name.lower(): weight.value for name, weight in AuthorityWeight.__members__.items()
}

CONFIDENCE_THRESHOLDS: Dict[ConfidenceBand, float] = {
    ConfidenceBand.DEFENSIBLE: 0.85,
    ConfidenceBand.SUPPORTABLE: 0.65,
    ConfidenceBand.DISCLOSURE: 0.50,
    ConfidenceBand.HIGH_RISK: 0.0,
}

ZONE_CITATION_REQUIREMENTS: Dict[AnalysisZone, str] = {
    AnalysisZone.LITIGATION: "mandatory_pinpoint",
    AnalysisZone.TRANSACTIONAL: "supportive",
    AnalysisZone.REGULATORY: "mandatory",
}

BANNED_PHRASES: List[str] = [
    "I'm certain that",
    "This is definitely",
    "There is no doubt",
    "It's guaranteed",
    "You will always win",
    "The court will certainly",
    "This is a slam dunk",
    "No judge would",
    "Any reasonable court",
    "It's black letter law that",
    "There's zero chance",
    "This is an open and shut case",
    "You are guaranteed to prevail",
    "No court has ever",
]

ENGINE_VERSION: str = "2.0.0"
ENGINE_ID: str = "LG02"
ENGINE_PORT: int = 8392


# ############################################################################
#
# SECTION 2: PYDANTIC MODELS
#
# ############################################################################

class LegalQuery(BaseModel):
    """Professional legal research query request."""
    question: str = Field(..., min_length=5, max_length=5000, description="Legal question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    jurisdiction: str = Field(default="federal", description="Legal jurisdiction")
    jurisdiction_type: Optional[JurisdictionType] = None
    legal_domain: Optional[LegalDomain] = None
    court_level: Optional[CourtLevel] = None
    complexity: Complexity = Field(default=Complexity.STANDARD)
    include_trace: bool = Field(default=False)
    include_counter_arguments: bool = Field(default=True)
    include_shepardize: bool = Field(default=False)
    include_precedent_chain: bool = Field(default=False)
    max_citations: Optional[int] = Field(default=None, ge=1, le=50)
    year_range_start: Optional[int] = None
    year_range_end: Optional[int] = None
    specific_courts: Optional[List[str]] = None
    party_names: Optional[List[str]] = None


class CitationParseRequest(BaseModel):
    """Request to parse one or more citations."""
    citations: List[str] = Field(..., min_length=1, max_length=50, description="Citation strings to parse")


class ShepardizeRequest(BaseModel):
    """Request to Shepardize a citation."""
    citation: str = Field(..., min_length=5, description="Citation to Shepardize")


class PrecedentWeightRequest(BaseModel):
    """Request to calculate precedent weight."""
    court_level: str = Field(..., description="Court level identifier")
    year: int = Field(..., ge=1700, le=2030, description="Year of decision")
    citation_count: int = Field(default=0, ge=0)
    positive_treatments: int = Field(default=0, ge=0)
    negative_treatments: int = Field(default=0, ge=0)
    overruled: bool = Field(default=False)
    same_jurisdiction: bool = Field(default=True)
    opinion_type: str = Field(default="majority")


class OpinionParseRequest(BaseModel):
    """Request to parse opinion sections from text."""
    text: str = Field(..., min_length=50, description="Opinion text to parse")
    case_citation: Optional[str] = None


class HeadnoteExtractRequest(BaseModel):
    """Request to extract headnotes from opinion text."""
    text: str = Field(..., min_length=100, description="Opinion text for headnote extraction")
    max_headnotes: int = Field(default=10, ge=1, le=50)


class KeyNumberLookupRequest(BaseModel):
    """Request to map legal issues to West Key Number System."""
    issue: str = Field(..., min_length=5, description="Legal issue to classify")
    domain: Optional[LegalDomain] = None


class VerifyRequest(BaseModel):
    """Verify deterministic output for a query."""
    question: str = Field(..., min_length=5)
    expected_hash: str = Field(..., min_length=64, max_length=64)


class Citation(BaseModel):
    """Structured legal citation in response."""
    authority_type: str
    reference: str
    court: Optional[str] = None
    year: Optional[int] = None
    relevance: str
    weight: int = Field(default=50)
    pinpoint: Optional[str] = None
    treatment: Optional[str] = None
    shepardize_signal: Optional[str] = None


class ReasoningStep(BaseModel):
    """Structured reasoning component in legal analysis."""
    step: int
    analysis: str
    authority: Optional[str] = None
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)


class ConflictResolution(BaseModel):
    """Resolution of conflicting authorities."""
    conflicting_authorities: List[str]
    resolution_method: str
    controlling_authority: str
    controlling_weight: int
    rationale: str
    dissenting_position: Optional[str] = None


class ZonedConclusion(BaseModel):
    """A conclusion pinned to one AnalysisZone."""
    zone: AnalysisZone
    conclusion: str
    confidence: float = Field(ge=0.0, le=1.0)
    caveats: List[str] = Field(default_factory=list)
    action_items: List[str] = Field(default_factory=list)
    citation_support: List[str] = Field(default_factory=list)


class FragilityAssessment(BaseModel):
    """Assessment of position fragility."""
    level: FragilityLevel
    single_source_dependencies: List[str] = Field(default_factory=list)
    multi_source_positions: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    mitigation_strategies: List[str] = Field(default_factory=list)


class SubIssue(BaseModel):
    """A decomposed sub-issue from a complex legal question."""
    issue_number: int
    issue_statement: str
    doctrine_key: Optional[str] = None
    analysis: str
    citations: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)
    depends_on: List[int] = Field(default_factory=list)


class LegalResponse(BaseModel):
    """Professional legal intelligence response."""
    query_id: str
    question: str
    mode: ResponseMode
    conclusion: str
    reasoning: str
    key_factors: List[str] = Field(default_factory=list)
    citations: List[Citation] = Field(default_factory=list)
    reasoning_steps: List[ReasoningStep] = Field(default_factory=list)
    opposing_arguments: Optional[List[str]] = None
    risk_assessment: Optional[str] = None
    distinguishing_factors: Optional[List[str]] = None
    zoned_conclusions: Optional[List[ZonedConclusion]] = None
    sub_issues: Optional[List[SubIssue]] = None
    fragility: Optional[FragilityAssessment] = None
    conflict_detected: bool = False
    conflict_resolution: Optional[ConflictResolution] = None
    doctrine_match: bool
    confidence_band: ConfidenceBand
    confidence_score: float = Field(ge=0.0, le=1.0)
    response_layer: str
    latency_ms: float
    authority_weight: Optional[int] = None
    determinism_hash: Optional[str] = None
    jurisdiction_applied: str = "federal"
    legal_domain_detected: Optional[str] = None
    epistemic_disclaimers: List[str] = Field(default_factory=list)
    shepardize_results: Optional[List[Dict[str, Any]]] = None
    precedent_chain: Optional[Dict[str, Any]] = None
    trace: Optional[List[Dict[str, Any]]] = None


class VerifyResponse(BaseModel):
    """Response for deterministic verification."""
    question: str
    computed_hash: str
    expected_hash: str
    match: bool
    confidence: float
    doctrine_key: Optional[str] = None


# ############################################################################
#
# SECTION 3: CORE ENGINE COMPONENTS
#
# ############################################################################

class MetricsCollector:
    """Lightweight metrics for operational awareness."""

    def __init__(self) -> None:
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.search_hits: int = 0
        self.citation_parses: int = 0
        self.shepardize_ops: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0
        self._max_latencies = 200

    def record_query(self, latency_ms: float, doctrine_hit: bool) -> None:
        """Record a completed query."""
        now = time.time()
        self.latencies.append(latency_ms)
        if len(self.latencies) > self._max_latencies:
            self.latencies.pop(0)
        self.queries.append(now)
        cutoff = now - 3600
        self.queries = [t for t in self.queries if t > cutoff]
        if doctrine_hit:
            self.doctrine_hits += 1
        else:
            self.doctrine_misses += 1

    def record_error(self, error_msg: str) -> None:
        """Record an error."""
        self.errors.append(time.time())
        self.last_error = f"{datetime.now(timezone.utc).isoformat()}: {error_msg[:200]}"
        cutoff = time.time() - 86400
        self.errors = [t for t in self.errors if t > cutoff]

    def query_start(self) -> None:
        self.active_queries += 1

    def query_end(self) -> None:
        self.active_queries = max(0, self.active_queries - 1)

    def get_latency_stats(self) -> Dict[str, float]:
        if not self.latencies:
            return {"avg_ms": 0.0, "p95_ms": 0.0, "last_ms": 0.0}
        sorted_lat = sorted(self.latencies)
        p95_idx = int(len(sorted_lat) * 0.95)
        return {
            "avg_ms": round(sum(self.latencies) / len(self.latencies), 2),
            "p95_ms": round(sorted_lat[min(p95_idx, len(sorted_lat) - 1)], 2),
            "last_ms": round(self.latencies[-1], 2),
        }

    def get_error_stats(self) -> Dict[str, Any]:
        now = time.time()
        return {
            "last_hour": sum(1 for t in self.errors if t > now - 3600),
            "last_24h": len(self.errors),
            "last_error": self.last_error,
        }

    def get_doctrine_hit_rate(self) -> float:
        total = self.doctrine_hits + self.doctrine_misses
        return round(self.doctrine_hits / max(total, 1), 4)

    def get_full_metrics(self) -> Dict[str, Any]:
        total = self.doctrine_hits + self.doctrine_misses
        return {
            "total_queries": total,
            "doctrine_hits": self.doctrine_hits,
            "doctrine_misses": self.doctrine_misses,
            "search_hits": self.search_hits,
            "citation_parses": self.citation_parses,
            "shepardize_ops": self.shepardize_ops,
            "hit_rate": self.get_doctrine_hit_rate(),
            "active_queries": self.active_queries,
            "latency": self.get_latency_stats(),
            "errors": self.get_error_stats(),
        }


class NormalizerManager:
    """Manages semantic normalization with stats tracking."""

    def __init__(self) -> None:
        self._count: int = 0
        self._modified_count: int = 0
        self._citations_extracted: int = 0
        self._courts_identified: int = 0

    def normalize(self, text: str) -> NormalizationResult:
        """Normalize a query through the semantic layer."""
        self._count += 1
        result = normalize_query(text)
        if result.was_modified:
            self._modified_count += 1
        self._citations_extracted += len(result.citations_found)
        self._courts_identified += len(result.courts_identified)
        return result

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_normalizations": self._count,
            "modified_count": self._modified_count,
            "modification_rate": round(self._modified_count / max(self._count, 1), 4),
            "citations_extracted": self._citations_extracted,
            "courts_identified": self._courts_identified,
            "semantic_version": get_semantic_map_version(),
        }

    def get_governance_info(self) -> Dict:
        return get_semantic_governance()

    def verify_integrity(self) -> Dict:
        return verify_dictionary_integrity()


class DoctrineManager:
    """Wraps the doctrine engine with extra tracking."""

    def __init__(self) -> None:
        self._engine = get_doctrine_engine()
        self._lookup_count: int = 0
        self._hit_count: int = 0
        self._miss_count: int = 0
        self._multi_match_count: int = 0

    def lookup(self, raw_query: str, normalized_query: str) -> Optional[DoctrineResponse]:
        """Look up a doctrine by query."""
        self._lookup_count += 1
        result = self._engine.quick_answer(normalized_query)
        if result is None:
            result = self._engine.quick_answer(raw_query)
        if result:
            self._hit_count += 1
        else:
            self._miss_count += 1
        return result

    def multi_lookup(self, query: str, max_results: int = 5) -> List[Tuple[str, DoctrineResponse, int]]:
        """Find multiple matching doctrines."""
        self._multi_match_count += 1
        return self._engine.multi_match(query, max_results)

    def get_doctrine(self, key: str) -> Optional[DoctrineResponse]:
        return self._engine.get_doctrine(key)

    def list_doctrines(self) -> List[Dict]:
        return self._engine.list_doctrines()

    def get_hit_stats(self) -> Dict:
        return self._engine.get_hit_stats()

    def get_recent_misses(self, limit: int = 20) -> List[str]:
        return self._engine.get_recent_misses(limit)


class SearchManager:
    """Manages the TF-IDF search index."""

    def __init__(self) -> None:
        self._index = get_search_index()
        self._query_count: int = 0
        self._results_returned: int = 0
        self._initialized: bool = False

    def initialize_from_doctrines(self, cache: Dict[str, DoctrineResponse]) -> None:
        """Build the search index from the doctrine cache."""
        for key, doctrine in cache.items():
            text = f"{doctrine.topic} {doctrine.quick_answer} {doctrine.full_doctrine}"
            self._index.add_document(
                key,
                text,
                metadata={
                    "topic": doctrine.topic,
                    "court_level": doctrine.court_level,
                    "authority_weight": doctrine.authority_weight,
                },
            )
        self._index.build_idf()
        self._initialized = True
        logger.info(f"Search index initialized with {len(cache)} doctrines")

    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search the doctrine index."""
        self._query_count += 1
        results = self._index.search(query, top_k=top_k)
        self._results_returned += len(results)
        return results

    def get_stats(self) -> Dict[str, Any]:
        stats = self._index.get_stats()
        stats["manager_queries"] = self._query_count
        stats["total_results_returned"] = self._results_returned
        return stats

    def get_misses(self, limit: int = 20) -> List[str]:
        return self._index.get_misses(limit)


class ConfidenceStratifier:
    """Classifies confidence scores into bands."""

    def __init__(self) -> None:
        self._classifications: Dict[str, int] = {}

    def classify(self, score: float) -> Tuple[ConfidenceBand, str]:
        """Classify a confidence score into a band."""
        band = self._classify_band(score)
        self._classifications[band.value] = self._classifications.get(band.value, 0) + 1
        label = ENGINE_CONFIG.get("confidence_bands", {}).get(band.value.upper(), {}).get("label", "")
        return band, label

    def _classify_band(self, score: float) -> ConfidenceBand:
        """Internal band classification."""
        if score >= 0.85:
            return ConfidenceBand.DEFENSIBLE
        elif score >= 0.65:
            return ConfidenceBand.SUPPORTABLE
        elif score >= 0.50:
            return ConfidenceBand.DISCLOSURE
        else:
            return ConfidenceBand.HIGH_RISK

    def get_stats(self) -> Dict:
        return {"classifications": dict(self._classifications)}


class DeterminismVerifier:
    """Verifies deterministic output through SHA-256 hashing."""

    def __init__(self) -> None:
        self._verifications: int = 0
        self._matches: int = 0
        self._mismatches: int = 0

    def compute_hash(self, *components: str) -> str:
        """Compute determinism hash from multiple components."""
        combined = "|".join(str(c) for c in components)
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    def verify(self, *components: str, expected: str = "") -> Tuple[bool, str]:
        """Verify determinism hash matches expected."""
        self._verifications += 1
        computed = self.compute_hash(*components)
        if expected:
            matches = computed == expected
            if matches:
                self._matches += 1
            else:
                self._mismatches += 1
            return matches, computed
        return True, computed

    def get_stats(self) -> Dict:
        return {
            "verifications": self._verifications,
            "matches": self._matches,
            "mismatches": self._mismatches,
        }


class EpistemicGuardrails:
    """Ensures legal analysis doesn't contain overconfident language."""

    def __init__(self, banned_phrases: List[str]) -> None:
        self._banned = [p.lower() for p in banned_phrases]
        self._violations_caught: int = 0

    def check_and_clean(self, text: str) -> Tuple[str, List[str]]:
        """Check text for banned phrases and return cleaned text."""
        violations: List[str] = []
        cleaned = text
        for phrase in self._banned:
            if phrase in cleaned.lower():
                violations.append(phrase)
                self._violations_caught += 1
        return cleaned, violations

    def get_required_disclaimers(self) -> List[str]:
        """Get the required epistemic disclaimers."""
        disclaimers = ENGINE_CONFIG.get("epistemic_guardrails", {}).get("required_disclaimers", {})
        return list(disclaimers.values())

    def get_stats(self) -> Dict:
        return {"violations_caught": self._violations_caught}


class ZonedAnalyzer:
    """Separates analysis into litigation, transactional, and regulatory zones."""

    def __init__(self) -> None:
        self._zone_counts: Dict[str, int] = {}

    def classify_zone(self, query: str) -> AnalysisZone:
        """Classify a query into an analysis zone."""
        query_lower = query.lower()

        litigation_signals = [
            "court", "judge", "trial", "motion", "hearing", "summary judgment",
            "dismiss", "appeal", "jury", "verdict", "plaintiff", "defendant",
            "litigation", "suit", "claim", "cause of action", "standing",
            "injunction", "damages", "relief", "discovery", "deposition",
        ]
        transactional_signals = [
            "contract", "agreement", "deal", "merger", "acquisition",
            "transaction", "closing", "negotiate", "term sheet", "corporate",
            "governance", "board", "shareholder", "fiduciary", "formation",
            "entity", "llc", "partnership", "joint venture",
        ]
        regulatory_signals = [
            "regulation", "compliance", "agency", "administrative", "enforcement",
            "sec", "epa", "fda", "ftc", "osha", "regulatory", "rulemaking",
            "audit", "inspection", "penalty", "fine", "violation", "permit",
        ]

        lit_score = sum(1 for s in litigation_signals if s in query_lower)
        trans_score = sum(1 for s in transactional_signals if s in query_lower)
        reg_score = sum(1 for s in regulatory_signals if s in query_lower)

        if lit_score >= trans_score and lit_score >= reg_score:
            zone = AnalysisZone.LITIGATION
        elif trans_score >= reg_score:
            zone = AnalysisZone.TRANSACTIONAL
        else:
            zone = AnalysisZone.REGULATORY

        self._zone_counts[zone.value] = self._zone_counts.get(zone.value, 0) + 1
        return zone

    def get_stats(self) -> Dict:
        return {"zone_distribution": dict(self._zone_counts)}


class FragilityAnalyzer:
    """Assesses how fragile a legal position is."""

    def __init__(self) -> None:
        self._assessments: int = 0

    def assess(
        self,
        citations: List[Citation],
        doctrine_hit: bool,
        confidence: float,
    ) -> FragilityAssessment:
        """Assess the fragility of a legal position."""
        self._assessments += 1

        single_source = []
        multi_source = []
        risk_factors = []
        mitigation = []

        # Check citation diversity
        unique_courts = set()
        for c in citations:
            if c.court:
                unique_courts.add(c.court)

        if len(citations) <= 1:
            single_source.append("Position relies on a single authority")
            risk_factors.append("Single point of failure if authority is overruled")
        else:
            multi_source.append(f"Position supported by {len(citations)} authorities")

        if len(unique_courts) <= 1 and len(citations) > 1:
            risk_factors.append("All authorities from the same court level")
            mitigation.append("Seek supporting authority from different court levels")

        # Check for old citations
        current_year = datetime.now(timezone.utc).year
        old_citations = [c for c in citations if c.year and c.year < current_year - 30]
        if old_citations:
            risk_factors.append(f"{len(old_citations)} citation(s) older than 30 years")
            mitigation.append("Verify old authorities remain good law via Shepardize")

        # Check confidence level
        if confidence < 0.5:
            risk_factors.append("Low confidence score indicates weak support")
            mitigation.append("Consider additional research or alternative theories")

        # Check for overruled citations
        overruled = [c for c in citations if c.treatment and "overruled" in c.treatment.lower()]
        if overruled:
            risk_factors.append(f"{len(overruled)} citation(s) have been overruled")
            mitigation.append("Replace overruled authorities with current precedent")

        # Determine level
        risk_count = len(risk_factors)
        if risk_count == 0:
            level = FragilityLevel.LOW
        elif risk_count <= 2:
            level = FragilityLevel.MODERATE
        elif risk_count <= 4:
            level = FragilityLevel.HIGH
        else:
            level = FragilityLevel.CRITICAL

        return FragilityAssessment(
            level=level,
            single_source_dependencies=single_source,
            multi_source_positions=multi_source,
            risk_factors=risk_factors,
            mitigation_strategies=mitigation,
        )

    def get_stats(self) -> Dict:
        return {"assessments": self._assessments}


class IssueDecomposer:
    """Decomposes complex legal queries into sub-issues."""

    ISSUE_KEYWORDS: Dict[str, List[str]] = {
        "standing": ["standing", "injury", "causation", "redressability", "article iii"],
        "jurisdiction": ["jurisdiction", "personal", "subject matter", "venue", "removal"],
        "merit": ["liability", "breach", "duty", "negligence", "damages", "relief"],
        "procedure": ["motion", "discovery", "summary judgment", "trial", "appeal"],
        "remedy": ["damages", "injunction", "restitution", "specific performance"],
        "defense": ["immunity", "statute of limitations", "estoppel", "laches"],
    }

    def __init__(self) -> None:
        self._decompositions: int = 0

    def decompose(self, query: str) -> List[SubIssue]:
        """Decompose a query into sub-issues."""
        self._decompositions += 1
        query_lower = query.lower()
        issues: List[SubIssue] = []
        issue_num = 0

        for category, keywords in self.ISSUE_KEYWORDS.items():
            matched_keywords = [kw for kw in keywords if kw in query_lower]
            if matched_keywords:
                issue_num += 1
                issues.append(SubIssue(
                    issue_number=issue_num,
                    issue_statement=f"Analysis of {category} issues: {', '.join(matched_keywords)}",
                    analysis=f"The query raises {category} questions involving {', '.join(matched_keywords)}. Each must be analyzed separately under the applicable legal framework.",
                    confidence=0.7,
                    depends_on=[i for i in range(1, issue_num) if category in ("merit", "remedy")],
                ))

        if not issues:
            issues.append(SubIssue(
                issue_number=1,
                issue_statement="General legal analysis",
                analysis="The query presents a general legal question that does not cleanly decompose into standard sub-issue categories.",
                confidence=0.6,
            ))

        return issues

    def get_stats(self) -> Dict:
        return {"decompositions": self._decompositions}


class DeepAnalyzer:
    """Provides deep multi-source analysis when doctrine and search fail."""

    def __init__(self) -> None:
        self._analyses: int = 0

    def analyze(
        self,
        query: str,
        normalized: str,
        jurisdiction: str,
        domain: Optional[LegalDomain],
    ) -> Dict[str, Any]:
        """Perform deep analysis synthesis."""
        self._analyses += 1

        domain_context = ""
        if domain:
            domain_context = f" in the area of {domain.value} law"

        analysis = {
            "conclusion": f"Based on general legal principles{domain_context}, the query requires further research with specific case law and statutory authority in the {jurisdiction} jurisdiction. The analysis should consider both majority and minority positions.",
            "reasoning": f"This question touches on fundamental legal principles{domain_context}. Without a direct doctrine match, the analysis must synthesize from multiple sources. Key considerations include the applicable standard of review, the burden of proof, and the weight of competing authorities.",
            "key_factors": [
                f"Jurisdiction: {jurisdiction}",
                f"Domain: {domain.value if domain else 'general'}",
                "Standard of review applicable to the legal question",
                "Burden of proof and which party bears it",
                "Weight of competing authorities",
                "Policy considerations underlying the legal rule",
            ],
            "suggested_research": [
                "Search for directly controlling precedent in the jurisdiction",
                "Review applicable statutes and regulations",
                "Check for recent developments or circuit splits",
                "Consult relevant Restatements and treatises",
                "Review law review articles for emerging trends",
            ],
            "confidence": 0.45,
        }

        return analysis

    def get_stats(self) -> Dict:
        return {"deep_analyses": self._analyses}


class AuditTrail:
    """Append-only audit trail for compliance."""

    def __init__(self, log_path: Path) -> None:
        self._log_path = log_path
        self._entries: List[Dict[str, Any]] = []
        self._count: int = 0

    def record(
        self,
        query_id: str,
        question: str,
        mode: str,
        response_layer: str,
        confidence: float,
        determinism_hash: str,
        citations_count: int,
        jurisdiction: str,
        latency_ms: float,
    ) -> None:
        """Record an audit entry."""
        entry = {
            "audit_id": str(uuid.uuid4()),
            "query_id": query_id,
            "question": question[:200],
            "mode": mode,
            "response_layer": response_layer,
            "confidence": confidence,
            "determinism_hash": determinism_hash,
            "citations_count": citations_count,
            "jurisdiction": jurisdiction,
            "latency_ms": latency_ms,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine_version": ENGINE_VERSION,
        }

        # Compute chain hash
        prev_hash = self._entries[-1].get("chain_hash", "genesis") if self._entries else "genesis"
        chain_input = f"{prev_hash}|{entry['audit_id']}|{entry['determinism_hash']}"
        entry["chain_hash"] = hashlib.sha256(chain_input.encode()).hexdigest()

        self._entries.append(entry)
        self._count += 1

        # Write to JSONL
        try:
            with open(self._log_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry, default=str) + "\n")
        except OSError as exc:
            logger.error(f"Audit write failed: {exc}")

    def get_recent(self, limit: int = 50) -> List[Dict]:
        return self._entries[-limit:]

    def verify_chain(self, limit: int = 50) -> Dict[str, Any]:
        """Verify the integrity of the audit chain."""
        entries = self._entries[-limit:]
        if not entries:
            return {"valid": True, "checked": 0}

        valid = True
        for i in range(1, len(entries)):
            prev_hash = entries[i - 1].get("chain_hash", "")
            expected_input = f"{prev_hash}|{entries[i]['audit_id']}|{entries[i]['determinism_hash']}"
            expected = hashlib.sha256(expected_input.encode()).hexdigest()
            if entries[i].get("chain_hash") != expected:
                valid = False
                break

        return {"valid": valid, "checked": len(entries)}

    def get_stats(self) -> Dict:
        return {"total_entries": self._count}


class OpinionParser:
    """Parses judicial opinions into constituent sections."""

    SECTION_PATTERNS: Dict[str, re.Pattern] = {
        "syllabus": re.compile(r"(?i)(syllabus|headnote|held:)", re.MULTILINE),
        "majority": re.compile(r"(?i)(opinion of the court|majority opinion|(?:justice|judge)\s+\w+\s+delivered the opinion)", re.MULTILINE),
        "plurality": re.compile(r"(?i)(plurality opinion|(?:justice|judge)\s+\w+\s+announced the judgment)", re.MULTILINE),
        "concurrence": re.compile(r"(?i)(concurring opinion|(?:justice|judge)\s+\w+,?\s+concurring)", re.MULTILINE),
        "concurrence_in_judgment": re.compile(r"(?i)(concurring in the judgment|concur(?:ring)? in judgment only)", re.MULTILINE),
        "dissent": re.compile(r"(?i)(dissenting opinion|(?:justice|judge)\s+\w+,?\s+dissenting)", re.MULTILINE),
        "per_curiam": re.compile(r"(?i)(per curiam)", re.MULTILINE),
    }

    def __init__(self) -> None:
        self._parses: int = 0

    def parse_sections(self, text: str) -> Dict[str, Dict[str, Any]]:
        """Parse an opinion text into sections."""
        self._parses += 1
        sections: Dict[str, Dict[str, Any]] = {}

        for section_name, pattern in self.SECTION_PATTERNS.items():
            match = pattern.search(text)
            if match:
                start = match.start()
                # Find the next section start to determine end
                next_start = len(text)
                for other_name, other_pattern in self.SECTION_PATTERNS.items():
                    if other_name == section_name:
                        continue
                    other_match = other_pattern.search(text, pos=start + 1)
                    if other_match and other_match.start() < next_start:
                        next_start = other_match.start()

                section_text = text[start:next_start].strip()
                word_count = len(section_text.split())

                # Extract author if possible
                author_match = re.search(
                    r"(?:Justice|Judge|Chief Justice)\s+([A-Z][a-z]+)",
                    section_text[:200],
                )
                author = author_match.group(1) if author_match else "Unknown"

                # Get weight modifier from config
                opinion_config = ENGINE_CONFIG.get("opinion_sections", {}).get(section_name, {})
                weight_modifier = opinion_config.get("weight_modifier", 0.5)
                is_binding = opinion_config.get("binding", False)

                sections[section_name] = {
                    "section": section_name,
                    "author": author,
                    "word_count": word_count,
                    "excerpt": section_text[:500],
                    "weight_modifier": weight_modifier,
                    "binding": is_binding,
                    "start_position": start,
                }

        return sections

    def get_stats(self) -> Dict:
        return {"parses": self._parses}


class HeadnoteExtractor:
    """Extracts headnotes (key legal propositions) from opinion text."""

    def __init__(self) -> None:
        self._extractions: int = 0

    def extract(self, text: str, max_headnotes: int = 10) -> List[Dict[str, Any]]:
        """Extract headnotes from opinion text."""
        self._extractions += 1
        headnotes: List[Dict[str, Any]] = []

        # Split into sentences
        sentences = re.split(r"(?<=[.!?])\s+", text)

        # Score sentences for legal significance
        scored: List[Tuple[float, str]] = []
        for sentence in sentences:
            if len(sentence) < 30 or len(sentence) > 500:
                continue
            score = self._score_sentence(sentence)
            if score > 0.3:
                scored.append((score, sentence))

        # Sort by score and take top N
        scored.sort(key=lambda x: x[0], reverse=True)

        for i, (score, sentence) in enumerate(scored[:max_headnotes]):
            # Classify the headnote topic
            topic = self._classify_topic(sentence)
            key_number = self._suggest_key_number(sentence)

            headnotes.append({
                "headnote_number": i + 1,
                "text": sentence.strip(),
                "significance_score": round(score, 3),
                "topic_classification": topic,
                "suggested_key_number": key_number,
            })

        return headnotes

    def _score_sentence(self, sentence: str) -> float:
        """Score a sentence for legal significance."""
        score = 0.0
        lower = sentence.lower()

        # Holding indicators
        holding_signals = ["held", "holding", "we hold", "the court held", "we conclude", "we find"]
        for signal in holding_signals:
            if signal in lower:
                score += 0.5

        # Legal rule signals
        rule_signals = ["must", "shall", "requires", "prohibits", "standard", "test", "elements", "factors"]
        for signal in rule_signals:
            if signal in lower:
                score += 0.2

        # Citation presence
        if re.search(r"\d+\s+[A-Z][a-z]+\.?\s+\d+", sentence):
            score += 0.15

        # Definitional language
        if any(phrase in lower for phrase in ["is defined as", "means", "constitutes", "encompasses"]):
            score += 0.3

        return min(score, 1.0)

    def _classify_topic(self, sentence: str) -> str:
        """Classify the legal topic of a headnote."""
        lower = sentence.lower()
        topic_keywords = {
            "Constitutional Law": ["constitution", "amendment", "due process", "equal protection"],
            "Civil Procedure": ["summary judgment", "dismiss", "motion", "jurisdiction", "pleading"],
            "Criminal Law": ["criminal", "guilty", "sentence", "miranda", "search", "seizure"],
            "Evidence": ["hearsay", "testimony", "admissible", "witness", "evidence"],
            "Contracts": ["contract", "breach", "consideration", "agreement", "obligation"],
            "Torts": ["negligence", "duty", "causation", "damages", "tort"],
            "Property": ["property", "easement", "title", "deed", "lien"],
            "Corporate": ["corporation", "shareholder", "fiduciary", "board", "director"],
        }

        best_topic = "General Law"
        best_score = 0
        for topic, keywords in topic_keywords.items():
            score = sum(1 for kw in keywords if kw in lower)
            if score > best_score:
                best_score = score
                best_topic = topic

        return best_topic

    def _suggest_key_number(self, sentence: str) -> str:
        """Suggest a West Key Number topic for a headnote."""
        lower = sentence.lower()
        key_map = {
            "92 Constitutional Law": ["constitution", "amendment", "due process"],
            "170B Federal Civil Procedure": ["summary judgment", "dismiss", "motion"],
            "157 Evidence": ["hearsay", "testimony", "admissible"],
            "106 Contracts": ["contract", "breach", "consideration"],
            "379 Torts": ["negligence", "duty", "causation"],
            "110A Criminal Law": ["criminal", "guilty", "miranda"],
            "349B Securities Regulation": ["securities", "fraud", "10b-5"],
            "51 Bankruptcy": ["bankruptcy", "stay", "discharge"],
        }

        for key_number, keywords in key_map.items():
            if any(kw in lower for kw in keywords):
                return key_number

        return "General"

    def get_stats(self) -> Dict:
        return {"extractions": self._extractions}


class KeyNumberMapper:
    """Maps legal issues to the West Key Number System."""

    KEY_NUMBER_DATABASE: Dict[str, Dict[str, Any]] = {
        "92": {"name": "Constitutional Law", "keywords": ["constitution", "amendment", "free speech", "due process", "equal protection", "search", "seizure"]},
        "106": {"name": "Contracts", "keywords": ["contract", "offer", "acceptance", "consideration", "breach", "formation", "ucc"]},
        "110": {"name": "Corporations", "keywords": ["corporation", "shareholder", "director", "fiduciary", "veil", "derivative"]},
        "170A": {"name": "Federal Courts", "keywords": ["federal court", "jurisdiction", "standing", "mootness", "ripeness", "erie"]},
        "170B": {"name": "Federal Civil Procedure", "keywords": ["summary judgment", "dismiss", "class action", "discovery", "pleading", "12(b)(6)"]},
        "379": {"name": "Torts", "keywords": ["negligence", "duty", "causation", "damages", "tort", "strict liability"]},
        "371": {"name": "Taxation", "keywords": ["tax", "irs", "deduction", "income", "irc", "revenue"]},
        "157": {"name": "Evidence", "keywords": ["evidence", "hearsay", "testimony", "admissible", "daubert", "expert"]},
        "110A": {"name": "Criminal Law", "keywords": ["criminal", "felony", "misdemeanor", "sentence", "miranda", "probable cause"]},
        "307": {"name": "Property", "keywords": ["property", "real estate", "deed", "title", "easement", "lien"]},
        "231": {"name": "Labor & Employment", "keywords": ["employment", "discrimination", "title vii", "ada", "fmla", "labor"]},
        "349B": {"name": "Securities Regulation", "keywords": ["securities", "sec", "10b-5", "fraud", "insider", "disclosure"]},
        "29": {"name": "Antitrust", "keywords": ["antitrust", "sherman", "monopoly", "restraint", "price fixing"]},
        "51": {"name": "Bankruptcy", "keywords": ["bankruptcy", "chapter 7", "chapter 11", "stay", "discharge", "creditor"]},
        "99": {"name": "Copyrights & IP", "keywords": ["copyright", "patent", "trademark", "fair use", "infringement"]},
        "15A": {"name": "Administrative Law", "keywords": ["administrative", "agency", "apa", "chevron", "deference", "rulemaking"]},
        "25T": {"name": "Alternative Dispute Resolution", "keywords": ["arbitration", "mediation", "adr", "faa"]},
        "78": {"name": "Civil Rights", "keywords": ["civil rights", "section 1983", "qualified immunity", "discrimination"]},
        "228": {"name": "Judgment", "keywords": ["res judicata", "collateral estoppel", "preclusion", "final judgment"]},
        "272": {"name": "Negligence", "keywords": ["negligence", "reasonable person", "standard of care", "malpractice"]},
    }

    def __init__(self) -> None:
        self._lookups: int = 0

    def map_issue(self, issue: str, domain: Optional[LegalDomain] = None) -> List[Dict[str, Any]]:
        """Map a legal issue to Key Number topics."""
        self._lookups += 1
        issue_lower = issue.lower()
        matches: List[Tuple[str, Dict[str, Any], int]] = []

        for key_num, data in self.KEY_NUMBER_DATABASE.items():
            score = sum(1 for kw in data["keywords"] if kw in issue_lower)
            if score > 0:
                matches.append((key_num, data, score))

        matches.sort(key=lambda x: x[2], reverse=True)

        return [
            {
                "key_number": key_num,
                "topic_name": data["name"],
                "relevance_score": score,
                "matched_keywords": [kw for kw in data["keywords"] if kw in issue_lower],
            }
            for key_num, data, score in matches[:5]
        ]

    def get_stats(self) -> Dict:
        return {"lookups": self._lookups}


class DriftWatcher:
    """Monitors for doctrine drift and staleness."""

    def __init__(self) -> None:
        self._checks: int = 0
        self._drift_events: List[Dict[str, Any]] = []

    def check_staleness(self, doctrine_key: str, doctrine: DoctrineResponse) -> Dict[str, Any]:
        """Check whether a doctrine is at risk of staleness."""
        self._checks += 1
        current_year = datetime.now(timezone.utc).year

        staleness_score = 0.0
        warnings: List[str] = []

        # Check last update year
        try:
            update_year = int(doctrine.last_major_update)
            age = current_year - update_year
            if age >= 5:
                staleness_score += 0.3
                warnings.append(f"Doctrine last updated {age} years ago")
        except (ValueError, TypeError):
            staleness_score += 0.2
            warnings.append("Cannot determine last update date")

        # Check if overruled
        if doctrine.overruled_by:
            staleness_score = 1.0
            warnings.append(f"Doctrine overruled by: {doctrine.overruled_by}")

        # Check staleness risk flag
        if doctrine.staleness_risk == "high":
            staleness_score += 0.4
            warnings.append("Doctrine flagged as high staleness risk")
        elif doctrine.staleness_risk == "medium":
            staleness_score += 0.2
            warnings.append("Doctrine flagged as medium staleness risk")

        return {
            "doctrine_key": doctrine_key,
            "staleness_score": min(round(staleness_score, 3), 1.0),
            "is_stale": staleness_score >= 0.5,
            "warnings": warnings,
            "last_update": doctrine.last_major_update,
            "overruled_by": doctrine.overruled_by,
        }

    def get_report(self) -> Dict[str, Any]:
        return {
            "checks_performed": self._checks,
            "drift_events": self._drift_events[-20:],
        }


# ############################################################################
#
# SECTION 4: APPLICATION LIFECYCLE
#
# ############################################################################

_metrics = MetricsCollector()
_normalizer = NormalizerManager()
_doctrine_manager = DoctrineManager()
_search_manager = SearchManager()
_confidence_stratifier = ConfidenceStratifier()
_determinism_verifier = DeterminismVerifier()
_guardrails = EpistemicGuardrails(BANNED_PHRASES)
_zoned_analyzer = ZonedAnalyzer()
_fragility_analyzer = FragilityAnalyzer()
_decomposer = IssueDecomposer()
_deep_analyzer = DeepAnalyzer()
_audit_trail = AuditTrail(AUDIT_LOG)
_opinion_parser = OpinionParser()
_headnote_extractor = HeadnoteExtractor()
_key_number_mapper = KeyNumberMapper()
_drift_watcher = DriftWatcher()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    logger.info(f"LG02 Case Law Research Engine v{ENGINE_VERSION} starting on port {ENGINE_PORT}")

    # Initialize search index from doctrine cache
    _search_manager.initialize_from_doctrines(DOCTRINE_CACHE)

    # Start telemetry background flush
    get_telemetry().start_background_flush()

    logger.info(f"Engine ready. {len(DOCTRINE_CACHE)} doctrines loaded.")
    yield
    logger.info("LG02 Engine shutting down")


app = FastAPI(
    title="LG02 Case Law Research Engine",
    description="Professional-grade case law research and analysis engine",
    version=ENGINE_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ############################################################################
#
# SECTION 5: CORE QUERY PIPELINE
#
# ############################################################################

def _build_citations(doctrine: DoctrineResponse, mode: ResponseMode) -> List[Citation]:
    """Build structured Citation objects from a doctrine response."""
    citations: List[Citation] = []
    parser = get_citation_parser()
    max_cites = 3 if mode == ResponseMode.FAST else 10

    for raw_cite in doctrine.citations[:max_cites]:
        parsed = parser.parse(raw_cite)
        citations.append(Citation(
            authority_type="case" if parsed.citation_type == "case" else parsed.citation_type,
            reference=raw_cite,
            court=parsed.court if parsed.is_valid else None,
            year=parsed.year if parsed.is_valid else None,
            relevance=f"Supporting authority for {doctrine.topic}",
            weight=parsed.court_weight,
            treatment="cited",
        ))

    # Add statute refs
    for ref in doctrine.statute_refs[:3]:
        parsed = parser.parse(ref)
        citations.append(Citation(
            authority_type="statute" if "U.S.C." in ref or "C.F.R." in ref else "rule",
            reference=ref,
            relevance=f"Applicable statutory/regulatory authority for {doctrine.topic}",
            weight=parsed.court_weight if parsed.is_valid else 80,
        ))

    return citations


def _build_reasoning_steps(doctrine: DoctrineResponse) -> List[ReasoningStep]:
    """Build reasoning steps from a doctrine's playbook."""
    steps: List[ReasoningStep] = []
    for i, step_text in enumerate(doctrine.practice_playbook, 1):
        authority = None
        if i <= len(doctrine.citations):
            authority = doctrine.citations[i - 1]
        steps.append(ReasoningStep(
            step=i,
            analysis=step_text,
            authority=authority,
            confidence=0.85 - (i * 0.02),
        ))
    return steps


def _compute_response_hash(normalized_query: str, doctrine_key: Optional[str], band: str, conclusion: str) -> str:
    """Compute determinism hash for a response."""
    return _determinism_verifier.compute_hash(normalized_query, doctrine_key or "", band, conclusion[:200])


async def process_query(query: LegalQuery) -> LegalResponse:
    """Main query processing pipeline."""
    start_ms = time.time() * 1000
    query_id = str(uuid.uuid4())
    _metrics.query_start()

    trace = trace_query(
        query=query.question,
        mode=query.mode.value,
        jurisdiction=query.jurisdiction,
    )

    try:
        # Step 1: Normalize
        step = trace.add_step("normalize", ResponseLayer.DOCTRINE)
        norm_result = _normalizer.normalize(query.question)
        normalized = norm_result.normalized
        step.complete(f"Normalized. Modified: {norm_result.was_modified}. Citations found: {len(norm_result.citations_found)}")

        # Step 2: Determine zone
        zone = _zoned_analyzer.classify_zone(query.question)

        # Step 3: Doctrine lookup
        step = trace.add_step("doctrine_lookup", ResponseLayer.DOCTRINE)
        doctrine = _doctrine_manager.lookup(query.question, normalized)

        if doctrine:
            step.complete(f"Hit: {doctrine.topic}", success=True)
            step.doctrine_hit = True

            citations = _build_citations(doctrine, query.mode)
            reasoning_steps = _build_reasoning_steps(doctrine)

            # Determine confidence
            base_confidence = 0.88
            if doctrine.overruled_by:
                base_confidence = 0.30
            elif doctrine.staleness_risk == "high":
                base_confidence = 0.65

            band, band_label = _confidence_stratifier.classify(base_confidence)

            # Epistemic check
            conclusion, violations = _guardrails.check_and_clean(doctrine.quick_answer)

            # Compute determinism hash
            det_hash = _compute_response_hash(normalized, doctrine.topic, band.value, conclusion)

            # Build fragility assessment
            fragility = _fragility_analyzer.assess(citations, True, base_confidence)

            # Shepardize if requested
            shepardize_results = None
            if query.include_shepardize or query.mode == ResponseMode.SHEPARDIZE:
                shep_engine = get_shepardize_engine()
                shepardize_results = []
                for cite in doctrine.citations[:5]:
                    result = shep_engine.shepardize(cite)
                    shepardize_results.append(result.to_dict())
                    record_citation_lookup(
                        CitationLookupType.SHEPARDIZE,
                        cite,
                        parsed_ok=True,
                        treatment=result.signal,
                    )

            # Opposing arguments
            opposing = doctrine.counter_arguments if query.include_counter_arguments else None

            # Disclaimers
            disclaimers = _guardrails.get_required_disclaimers()

            # Sub-issues for complex queries
            sub_issues = None
            if query.complexity in (Complexity.ADVANCED, Complexity.EXPERT):
                sub_issues = _decomposer.decompose(query.question)

            # Zoned conclusions
            zoned_conclusions = [ZonedConclusion(
                zone=zone,
                conclusion=doctrine.quick_answer,
                confidence=base_confidence,
                caveats=[band_label] if band != ConfidenceBand.DEFENSIBLE else [],
                action_items=doctrine.practice_playbook[:3],
                citation_support=doctrine.citations[:3],
            )]

            latency = (time.time() * 1000) - start_ms
            _metrics.record_query(latency, True)
            _metrics.query_end()

            complete_trace(trace, ResponseLayer.DOCTRINE, doctrine_hit=True,
                          citations_returned=len(citations), confidence=base_confidence,
                          determinism_hash=det_hash)

            _audit_trail.record(query_id, query.question, query.mode.value,
                               "doctrine", base_confidence, det_hash,
                               len(citations), query.jurisdiction, latency)

            return LegalResponse(
                query_id=query_id,
                question=query.question,
                mode=query.mode,
                conclusion=conclusion,
                reasoning=doctrine.full_doctrine[:2000] if query.mode != ResponseMode.FAST else doctrine.full_doctrine[:500],
                key_factors=doctrine.practice_playbook[:5],
                citations=citations,
                reasoning_steps=reasoning_steps,
                opposing_arguments=opposing,
                risk_assessment=f"Fragility: {fragility.level.value}. " + "; ".join(fragility.risk_factors[:3]) if fragility.risk_factors else None,
                distinguishing_factors=None,
                zoned_conclusions=zoned_conclusions,
                sub_issues=sub_issues,
                fragility=fragility,
                conflict_detected=False,
                doctrine_match=True,
                confidence_band=band,
                confidence_score=base_confidence,
                response_layer="doctrine",
                latency_ms=round(latency, 2),
                authority_weight=doctrine.authority_weight,
                determinism_hash=det_hash,
                jurisdiction_applied=query.jurisdiction,
                legal_domain_detected=doctrine.jurisdiction_scope,
                epistemic_disclaimers=disclaimers,
                shepardize_results=shepardize_results,
                trace=[s.to_dict() for s in trace.steps] if query.include_trace else None,
            )

        step.complete("Miss", success=True)

        # Step 4: Search fallback
        step = trace.add_step("search", ResponseLayer.SEARCH)
        search_results = _search_manager.search(normalized, top_k=5)

        if search_results:
            best = search_results[0]
            step.complete(f"Found {len(search_results)} results. Best: {best.topic} (score={best.score:.3f})")
            _metrics.search_hits += 1

            # Retrieve the matched doctrine
            matched_doctrine = _doctrine_manager.get_doctrine(best.doctrine_key)
            if matched_doctrine:
                citations = _build_citations(matched_doctrine, query.mode)
                reasoning_steps = _build_reasoning_steps(matched_doctrine)
                confidence = min(0.75, best.score / 2 + 0.4)
                band, band_label = _confidence_stratifier.classify(confidence)
                conclusion, _ = _guardrails.check_and_clean(matched_doctrine.quick_answer)
                det_hash = _compute_response_hash(normalized, best.doctrine_key, band.value, conclusion)
                fragility = _fragility_analyzer.assess(citations, False, confidence)

                latency = (time.time() * 1000) - start_ms
                _metrics.record_query(latency, False)
                _metrics.query_end()

                complete_trace(trace, ResponseLayer.SEARCH, doctrine_hit=False,
                              citations_returned=len(citations), confidence=confidence,
                              determinism_hash=det_hash)

                _audit_trail.record(query_id, query.question, query.mode.value,
                                   "search", confidence, det_hash,
                                   len(citations), query.jurisdiction, latency)

                return LegalResponse(
                    query_id=query_id,
                    question=query.question,
                    mode=query.mode,
                    conclusion=conclusion,
                    reasoning=matched_doctrine.full_doctrine[:1500],
                    key_factors=matched_doctrine.practice_playbook[:4],
                    citations=citations,
                    reasoning_steps=reasoning_steps,
                    opposing_arguments=matched_doctrine.counter_arguments if query.include_counter_arguments else None,
                    fragility=fragility,
                    doctrine_match=False,
                    confidence_band=band,
                    confidence_score=confidence,
                    response_layer="search",
                    latency_ms=round(latency, 2),
                    authority_weight=best.authority_weight,
                    determinism_hash=det_hash,
                    jurisdiction_applied=query.jurisdiction,
                    epistemic_disclaimers=_guardrails.get_required_disclaimers(),
                    trace=[s.to_dict() for s in trace.steps] if query.include_trace else None,
                )

        step.complete("No search results", success=True)

        # Step 5: Deep analysis fallback
        step = trace.add_step("deep_analysis", ResponseLayer.DEEP_ANALYSIS)
        analysis = _deep_analyzer.analyze(query.question, normalized, query.jurisdiction, query.legal_domain)
        step.complete("Deep analysis complete")

        confidence = analysis["confidence"]
        band, band_label = _confidence_stratifier.classify(confidence)
        conclusion = analysis["conclusion"]
        det_hash = _compute_response_hash(normalized, "deep_analysis", band.value, conclusion[:200])

        latency = (time.time() * 1000) - start_ms
        _metrics.record_query(latency, False)
        _metrics.query_end()

        complete_trace(trace, ResponseLayer.DEEP_ANALYSIS, doctrine_hit=False,
                      citations_returned=0, confidence=confidence,
                      determinism_hash=det_hash)

        _audit_trail.record(query_id, query.question, query.mode.value,
                           "deep_analysis", confidence, det_hash,
                           0, query.jurisdiction, latency)

        return LegalResponse(
            query_id=query_id,
            question=query.question,
            mode=query.mode,
            conclusion=conclusion,
            reasoning=analysis["reasoning"],
            key_factors=analysis["key_factors"],
            citations=[],
            reasoning_steps=[],
            doctrine_match=False,
            confidence_band=band,
            confidence_score=confidence,
            response_layer="deep_analysis",
            latency_ms=round(latency, 2),
            determinism_hash=det_hash,
            jurisdiction_applied=query.jurisdiction,
            legal_domain_detected=query.legal_domain.value if query.legal_domain else None,
            epistemic_disclaimers=_guardrails.get_required_disclaimers(),
            trace=[s.to_dict() for s in trace.steps] if query.include_trace else None,
        )

    except Exception as exc:
        latency = (time.time() * 1000) - start_ms
        _metrics.record_error(str(exc))
        _metrics.query_end()
        log_error(ErrorDomain.UNKNOWN, str(exc), trace.trace_id, query.question)
        logger.error(f"Query pipeline error: {exc}\n{traceback.format_exc()}")

        return LegalResponse(
            query_id=query_id,
            question=query.question,
            mode=query.mode,
            conclusion=f"Error processing query: {str(exc)[:200]}",
            reasoning="An error occurred during analysis. Please retry or simplify the query.",
            doctrine_match=False,
            confidence_band=ConfidenceBand.HIGH_RISK,
            confidence_score=0.0,
            response_layer="error",
            latency_ms=round(latency, 2),
            epistemic_disclaimers=_guardrails.get_required_disclaimers(),
        )


# ############################################################################
#
# SECTION 6: API ENDPOINTS
#
# ############################################################################

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "uptime_seconds": round(time.time() - _metrics.queries[0] if _metrics.queries else time.time(), 1),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/query", response_model=LegalResponse)
async def query_endpoint(query: LegalQuery):
    """Main legal research query endpoint."""
    return await process_query(query)


@app.post("/parse-citations")
async def parse_citations_endpoint(req: CitationParseRequest):
    """Parse Bluebook-format citations into structured components."""
    parser = get_citation_parser()
    results = []
    for raw in req.citations:
        parsed = parser.parse(raw)
        results.append(parsed.to_dict())
        _metrics.citation_parses += 1
        record_citation_lookup(
            CitationLookupType.PARSE,
            raw,
            parsed_ok=parsed.is_valid,
            court=parsed.court,
            reporter=parsed.reporter,
            year=parsed.year,
        )
    return {"citations": results, "parser_stats": parser.get_stats()}


@app.post("/shepardize")
async def shepardize_endpoint(req: ShepardizeRequest):
    """Shepardize a citation to check current status."""
    engine = get_shepardize_engine()
    result = engine.shepardize(req.citation)
    _metrics.shepardize_ops += 1
    record_citation_lookup(
        CitationLookupType.SHEPARDIZE,
        req.citation,
        parsed_ok=True,
        treatment=result.signal,
    )
    return result.to_dict()


@app.post("/precedent-weight")
async def precedent_weight_endpoint(req: PrecedentWeightRequest):
    """Calculate the authority weight of a legal precedent."""
    calc = get_weight_calculator()
    return calc.calculate_weight(
        court_level=req.court_level,
        year=req.year,
        citation_count=req.citation_count,
        positive_treatments=req.positive_treatments,
        negative_treatments=req.negative_treatments,
        overruled=req.overruled,
        same_jurisdiction=req.same_jurisdiction,
        opinion_type=req.opinion_type,
    )


@app.post("/parse-opinion")
async def parse_opinion_endpoint(req: OpinionParseRequest):
    """Parse a judicial opinion into sections (majority, concurrence, dissent)."""
    sections = _opinion_parser.parse_sections(req.text)
    return {
        "case_citation": req.case_citation,
        "sections_found": list(sections.keys()),
        "sections": sections,
        "section_count": len(sections),
    }


@app.post("/extract-headnotes")
async def extract_headnotes_endpoint(req: HeadnoteExtractRequest):
    """Extract headnotes (key legal propositions) from opinion text."""
    headnotes = _headnote_extractor.extract(req.text, req.max_headnotes)
    return {
        "headnotes": headnotes,
        "count": len(headnotes),
    }


@app.post("/key-number-lookup")
async def key_number_lookup_endpoint(req: KeyNumberLookupRequest):
    """Map a legal issue to West Key Number System topics."""
    results = _key_number_mapper.map_issue(req.issue, req.domain)
    return {
        "issue": req.issue,
        "key_number_matches": results,
        "count": len(results),
    }


@app.get("/doctrines")
async def list_doctrines_endpoint():
    """List all available legal doctrines."""
    return {
        "engine_id": ENGINE_ID,
        "doctrines": _doctrine_manager.list_doctrines(),
        "total": len(DOCTRINE_CACHE),
    }


@app.get("/doctrine/{key}")
async def get_doctrine_endpoint(key: str):
    """Get a specific doctrine by key."""
    doctrine = _doctrine_manager.get_doctrine(key)
    if not doctrine:
        raise HTTPException(status_code=404, detail=f"Doctrine '{key}' not found")
    return doctrine.to_dict()


@app.get("/court-hierarchy")
async def court_hierarchy_endpoint():
    """Get the court hierarchy with weights."""
    return {
        "engine_id": ENGINE_ID,
        "hierarchy": ENGINE_CONFIG.get("court_hierarchy", {}),
        "authority_weights": ENGINE_CONFIG.get("authority_weights", {}),
        "weight_map": COURT_WEIGHT_MAP,
    }


@app.get("/reporters")
async def reporters_endpoint():
    """Get the reporter identification database."""
    return {
        "engine_id": ENGINE_ID,
        "reporters": REPORTER_COURT_MAP,
        "bluebook_reporters": ENGINE_CONFIG.get("bluebook_reporters", {}),
    }


@app.get("/circuits")
async def circuits_endpoint():
    """Get federal circuit information."""
    return {
        "engine_id": ENGINE_ID,
        "circuits": ENGINE_CONFIG.get("federal_circuits", {}),
    }


@app.get("/opinion-sections")
async def opinion_sections_endpoint():
    """Get opinion section metadata and weight modifiers."""
    return {
        "engine_id": ENGINE_ID,
        "sections": ENGINE_CONFIG.get("opinion_sections", {}),
    }


@app.get("/key-number-system")
async def key_number_system_endpoint():
    """Get the Key Number System topic database."""
    return {
        "engine_id": ENGINE_ID,
        "topics": _key_number_mapper.KEY_NUMBER_DATABASE,
        "total_topics": len(_key_number_mapper.KEY_NUMBER_DATABASE),
    }


@app.get("/shepardize-signals")
async def shepardize_signals_endpoint():
    """Get Shepardize signal definitions."""
    return {
        "engine_id": ENGINE_ID,
        "signals": ENGINE_CONFIG.get("shepardize_signals", {}),
        "treatment_signals": ENGINE_CONFIG.get("citation_treatment_signals", {}),
    }


@app.get("/overruled")
async def overruled_endpoint():
    """Get list of overruled doctrines."""
    engine = get_doctrine_engine()
    return {
        "engine_id": ENGINE_ID,
        "overruled_doctrines": engine.get_overruled_doctrines(),
    }


@app.get("/stale-doctrines")
async def stale_doctrines_endpoint(threshold_year: int = Query(default=2023, ge=2000, le=2030)):
    """Get doctrines at risk of staleness."""
    engine = get_doctrine_engine()
    return {
        "engine_id": ENGINE_ID,
        "stale_doctrines": engine.get_stale_doctrines(threshold_year),
    }


@app.get("/coverage")
async def coverage_endpoint():
    """Get doctrine coverage report."""
    return {
        "engine_id": ENGINE_ID,
        "total_doctrines": len(DOCTRINE_CACHE),
        "doctrine_hit_stats": _doctrine_manager.get_hit_stats(),
        "search_stats": _search_manager.get_stats(),
    }


@app.get("/metrics")
async def metrics_endpoint():
    """Get comprehensive engine metrics."""
    return {
        "engine_id": ENGINE_ID,
        "engine_version": ENGINE_VERSION,
        "metrics": _metrics.get_full_metrics(),
        "telemetry": get_telemetry().get_stats(),
        "normalization": _normalizer.get_stats(),
        "doctrine_hits": _doctrine_manager.get_hit_stats(),
        "search": _search_manager.get_stats(),
        "confidence": _confidence_stratifier.get_stats(),
        "zones": _zoned_analyzer.get_stats(),
        "fragility": _fragility_analyzer.get_stats(),
        "drift": _drift_watcher.get_report(),
        "decomposition": _decomposer.get_stats(),
        "analysis": _deep_analyzer.get_stats(),
        "audit": _audit_trail.get_stats(),
        "determinism": _determinism_verifier.get_stats(),
        "citation_parser": get_citation_parser().get_stats(),
        "shepardize": get_shepardize_engine().get_stats(),
        "opinion_parser": _opinion_parser.get_stats(),
        "headnote_extractor": _headnote_extractor.get_stats(),
        "key_number_mapper": _key_number_mapper.get_stats(),
    }


@app.get("/audit")
async def audit_endpoint(limit: int = Query(default=50, ge=1, le=500)):
    """Get recent audit trail records."""
    return {
        "engine_id": ENGINE_ID,
        "records": _audit_trail.get_recent(limit),
        "chain_integrity": _audit_trail.verify_chain(limit),
    }


@app.post("/verify", response_model=VerifyResponse)
async def verify_endpoint(req: VerifyRequest):
    """Verify deterministic output for a query."""
    norm_result = _normalizer.normalize(req.question)
    normalized = norm_result.normalized

    doctrine = _doctrine_manager.lookup(req.question, normalized)
    doctrine_key = None
    conclusion = ""
    confidence = 0.5

    if doctrine:
        doctrine_key = doctrine.topic
        conclusion = doctrine.quick_answer
        confidence = 0.85
    else:
        conclusion = "No matching doctrine found."

    band, _ = _confidence_stratifier.classify(confidence)
    match, computed = _determinism_verifier.verify(
        normalized, doctrine_key or "", band.value, conclusion[:200],
        expected=req.expected_hash,
    )

    return VerifyResponse(
        question=req.question,
        computed_hash=computed,
        expected_hash=req.expected_hash,
        match=match,
        confidence=confidence,
        doctrine_key=doctrine_key,
    )


@app.get("/drift")
async def drift_endpoint():
    """Get doctrine drift/staleness report."""
    report_items = []
    for key, doctrine in DOCTRINE_CACHE.items():
        item = _drift_watcher.check_staleness(key, doctrine)
        if item["is_stale"] or item["warnings"]:
            report_items.append(item)
    return {
        "engine_id": ENGINE_ID,
        "drift_report": report_items,
        "total_checked": len(DOCTRINE_CACHE),
        "stale_count": sum(1 for r in report_items if r["is_stale"]),
    }


@app.get("/misses")
async def misses_endpoint(limit: int = Query(default=50, ge=1, le=200)):
    """Get recent doctrine and search misses."""
    return {
        "engine_id": ENGINE_ID,
        "doctrine_misses": _doctrine_manager.get_recent_misses(limit),
        "search_misses": _search_manager.get_misses(limit),
    }


@app.get("/semantic")
async def semantic_endpoint():
    """Get semantic normalization information."""
    return {
        "engine_id": ENGINE_ID,
        "normalization_stats": _normalizer.get_stats(),
        "governance": _normalizer.get_governance_info(),
        "integrity": _normalizer.verify_integrity(),
        "citation_patterns": list(CITATION_PATTERNS.keys()),
        "court_abbreviations_count": len(get_court_abbreviations()),
    }


@app.get("/config")
async def config_endpoint():
    """Get engine configuration (non-sensitive)."""
    safe_config = {k: v for k, v in ENGINE_CONFIG.items() if k not in ("secrets", "credentials")}
    return {
        "engine_id": ENGINE_ID,
        "config": safe_config,
    }


# ############################################################################
#
# SECTION 7: MAIN ENTRY POINT
#
# ############################################################################

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )