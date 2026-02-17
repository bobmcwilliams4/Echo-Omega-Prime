"""
LG01 CONTRACT ANALYSIS ENGINE - Production Architecture
Professional-grade contract analysis system for legal teams, procurement,
and compliance officers.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled contract law reasoning
    Layer 2: Semantic Retrieval (200-700ms) - Fast search on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-source synthesis

Response Modes:
    FAST: Clause identification, sub-2 seconds
    REVIEW: Detailed analysis with risk scoring, 2-10 seconds
    MEMO: Full legal memorandum with citations, 10-30 seconds

Engine: LG01 Contract Analysis Engine
Tier: 1 (LEGAL)
Mode: DET (Deterministic)
Priority: 90 (Critical Infrastructure)
Port: 8401

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal, Tuple
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import hashlib
import json
import re
import time
import uuid
from pathlib import Path
from loguru import logger

# Engine components
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
    ErrorDomain,
    ResponseLayer,
    MutationType,
    MutationOrigin,
    ClauseExtractionRecord,
    RiskAssessmentRecord,
    ComplianceCheckRecord,
    ClauseCategory as TelemetryClauseCategory,
    RiskLevel as TelemetryRiskLevel,
)
from semantic import (
    normalize_semantics,
    normalize_clause_type,
    NormalizationResult,
    get_map_metadata,
    compute_text_hash,
    lock_governance,
    verify_integrity,
)
import sys

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DOCTRINE_CACHE,
    DOCTRINE_INTERACTIONS,
    DoctrineBlock,
    DoctrineCoverageMap,
    AuthorityLevel,
    ConfidenceLevel,
    RiskSeverity,
    ClauseCategory,
    ControllingPrecedent,
    DoctrineInteraction,
    get_all_doctrine_keys,
    get_doctrine,
    get_doctrines_by_category,
    get_doctrine_count,
    get_interaction_edges_for,
    get_all_categories,
)
from search import (
    get_search_index,
    InvertedIndex,
    SearchDocument,
    SearchQuery,
    SearchScope,
    SortOrder,
    SearchResult,
    compare_clauses,
    detect_boilerplate,
    compute_customization_score,
    ComparisonResult,
    ClauseDiff,
    trigram_similarity,
    extract_snippet,
)

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "LG01"
ENGINE_NAME = "Contract Analysis Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8401
ENGINE_TIER = 1
ENGINE_MODE = "DET"

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG01/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "lg01_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)

AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"

# Epistemic guardrails
BANNED_PHRASES: List[str] = [
    "this contract is definitely",
    "there is no risk",
    "this clause is completely safe",
    "you have nothing to worry about",
    "this is guaranteed to",
    "no court would ever",
    "this is always enforceable",
    "this clause is bulletproof",
    "this is 100% compliant",
    "you are fully protected",
    "there are no issues",
    "this is standard and fine",
]


# ============================================================================
# METRICS COLLECTOR
# ============================================================================

class MetricsCollector:
    """Lightweight operational metrics."""

    def __init__(self) -> None:
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0
        self._max_latencies: int = 100

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
        last_hour = sum(1 for t in self.errors if t > now - 3600)
        last_24h = len(self.errors)
        return {"last_hour": last_hour, "last_24h": last_24h, "last_error": self.last_error}

    def get_doctrine_hit_rate(self) -> float:
        total = self.doctrine_hits + self.doctrine_misses
        if total == 0:
            return 1.0
        return round(self.doctrine_hits / total, 3)

    def queries_last_hour(self) -> int:
        cutoff = time.time() - 3600
        return sum(1 for t in self.queries if t > cutoff)


_metrics = MetricsCollector()


def get_metrics() -> MetricsCollector:
    return _metrics


# ============================================================================
# ENUMS
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "fast"
    REVIEW = "review"
    MEMO = "memo"


class ContractType(str, Enum):
    SERVICE_AGREEMENT = "service_agreement"
    MASTER_SERVICE_AGREEMENT = "master_service_agreement"
    SOFTWARE_LICENSE = "software_license"
    SAAS_AGREEMENT = "saas_agreement"
    NDA = "nda"
    EMPLOYMENT_AGREEMENT = "employment_agreement"
    INDEPENDENT_CONTRACTOR = "independent_contractor"
    LEASE_AGREEMENT = "lease_agreement"
    PURCHASE_AGREEMENT = "purchase_agreement"
    SUPPLY_AGREEMENT = "supply_agreement"
    JOINT_VENTURE = "joint_venture"
    PARTNERSHIP_AGREEMENT = "partnership_agreement"
    MERGER_AGREEMENT = "merger_agreement"
    ASSET_PURCHASE = "asset_purchase"
    STOCK_PURCHASE = "stock_purchase"
    FRANCHISE_AGREEMENT = "franchise_agreement"
    CONSULTING_AGREEMENT = "consulting_agreement"
    LOAN_AGREEMENT = "loan_agreement"
    SETTLEMENT_AGREEMENT = "settlement_agreement"
    LICENSING_AGREEMENT = "licensing_agreement"
    CONSTRUCTION_CONTRACT = "construction_contract"
    REAL_ESTATE_PURCHASE = "real_estate_purchase"
    OIL_GAS_LEASE = "oil_gas_lease"
    OPERATING_AGREEMENT = "operating_agreement"
    OTHER = "other"


class AnalysisType(str, Enum):
    CLAUSE_EXTRACTION = "clause_extraction"
    RISK_ASSESSMENT = "risk_assessment"
    COMPLIANCE_CHECK = "compliance_check"
    CONTRACT_COMPARISON = "contract_comparison"
    OBLIGATION_TRACKING = "obligation_tracking"
    GENERAL_QUERY = "general_query"


class RiskLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NOT_APPLICABLE = "not_applicable"
    REQUIRES_REVIEW = "requires_review"


# ============================================================================
# REQUEST MODELS
# ============================================================================

class ContractQuery(BaseModel):
    """Contract analysis query request."""
    question: str = Field(..., min_length=5, description="Contract-related question or clause text")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response depth")
    contract_type: Optional[ContractType] = Field(default=None, description="Type of contract")
    analysis_type: AnalysisType = Field(default=AnalysisType.GENERAL_QUERY, description="Analysis type")
    jurisdiction: str = Field(default="US", description="Governing jurisdiction")
    contract_id: Optional[str] = Field(default=None, description="Contract identifier for tracking")
    include_trace: bool = Field(default=False, description="Include reasoning trace")
    include_negotiation_guidance: bool = Field(default=True, description="Include negotiation tips")


class ClauseExtractionRequest(BaseModel):
    """Request to extract and analyze clauses from contract text."""
    contract_text: str = Field(..., min_length=50, description="Full or partial contract text")
    contract_type: Optional[ContractType] = Field(default=None, description="Contract type hint")
    contract_id: Optional[str] = Field(default=None, description="Contract identifier")
    focus_clauses: Optional[List[str]] = Field(default=None, description="Specific clause types to focus on")
    include_risk: bool = Field(default=True, description="Include risk assessment per clause")
    include_boilerplate_detection: bool = Field(default=True, description="Detect boilerplate clauses")


class RiskAssessmentRequest(BaseModel):
    """Request for contract risk assessment."""
    contract_text: str = Field(..., min_length=50, description="Contract text or clause text")
    contract_type: Optional[ContractType] = Field(default=None, description="Contract type")
    contract_id: Optional[str] = Field(default=None, description="Contract identifier")
    jurisdiction: str = Field(default="US", description="Jurisdiction")
    risk_tolerance: str = Field(default="moderate", description="Risk tolerance: conservative, moderate, aggressive")


class ComplianceCheckRequest(BaseModel):
    """Request for compliance checking against a framework."""
    contract_text: str = Field(..., min_length=50, description="Contract text")
    frameworks: List[str] = Field(default=["general"], description="Compliance frameworks to check against")
    contract_type: Optional[ContractType] = Field(default=None, description="Contract type")
    contract_id: Optional[str] = Field(default=None, description="Contract identifier")
    jurisdiction: str = Field(default="US", description="Jurisdiction")


class ContractComparisonRequest(BaseModel):
    """Request to compare two contracts."""
    contract_a_text: str = Field(..., min_length=50, description="First contract text")
    contract_b_text: str = Field(..., min_length=50, description="Second contract text")
    contract_a_id: str = Field(default="contract_a", description="First contract identifier")
    contract_b_id: str = Field(default="contract_b", description="Second contract identifier")
    focus_clauses: Optional[List[str]] = Field(default=None, description="Specific clause types to compare")


class ObligationTrackingRequest(BaseModel):
    """Request to extract obligations and deadlines from contract."""
    contract_text: str = Field(..., min_length=50, description="Contract text")
    contract_type: Optional[ContractType] = Field(default=None, description="Contract type")
    contract_id: Optional[str] = Field(default=None, description="Contract identifier")
    effective_date: Optional[str] = Field(default=None, description="Contract effective date (ISO format)")


class SearchRequest(BaseModel):
    """Search request for the clause/doctrine index."""
    query: str = Field(..., min_length=2, description="Search query")
    scope: str = Field(default="all", description="Search scope: clauses, doctrines, contracts, all")
    clause_type: Optional[str] = Field(default=None, description="Filter by clause type")
    risk_level: Optional[str] = Field(default=None, description="Filter by risk level")
    max_results: int = Field(default=20, ge=1, le=100, description="Maximum results")


class AnalyzeRequest(BaseModel):
    """Request model for contract analysis and redline endpoints."""
    text: str = Field(..., min_length=10, description="Contract text to analyze")
    contract_type: str = Field(default="general", description="Type of contract being analyzed")
    jurisdiction: Optional[str] = Field(default=None, description="Governing jurisdiction")


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class Citation(BaseModel):
    """Structured legal citation."""
    authority: str
    reference: str
    relevance: str


class ReasoningStep(BaseModel):
    """Single reasoning step."""
    step: int
    analysis: str
    authority: Optional[str] = None


class RiskFinding(BaseModel):
    """Individual risk finding."""
    risk_id: str
    clause_type: str
    risk_level: RiskLevel
    risk_score: float
    description: str
    factors: List[str]
    mitigation: List[str]
    recommendation: str
    confidence: float


class ClauseAnalysis(BaseModel):
    """Analysis of a single extracted clause."""
    clause_id: str
    clause_type: str
    clause_category: str
    clause_text: str
    summary: str
    is_boilerplate: bool
    customization_score: float
    risk_level: RiskLevel
    risk_score: float
    risk_factors: List[str]
    key_provisions: List[str]
    missing_provisions: List[str]
    negotiation_points: List[str]
    doctrine_applicable: Optional[str] = None
    confidence: float = 0.0


class ObligationItem(BaseModel):
    """A single contractual obligation."""
    obligation_id: str
    party: str
    obligation_type: str
    description: str
    deadline: Optional[str] = None
    recurring: bool = False
    recurrence_pattern: Optional[str] = None
    clause_reference: str
    priority: str
    status: str = "active"


class ComplianceFinding(BaseModel):
    """Single compliance finding."""
    finding_id: str
    framework: str
    requirement: str
    status: ComplianceStatus
    description: str
    clause_reference: Optional[str] = None
    remediation: Optional[str] = None
    confidence: float


class ContractResponse(BaseModel):
    """Primary contract analysis response."""
    query_id: str
    question: str
    mode: ResponseMode

    conclusion: str
    reasoning: str

    key_factors: List[str]
    citations: List[Citation]

    risk_findings: Optional[List[RiskFinding]] = None
    negotiation_guidance: Optional[str] = None
    common_pitfalls: Optional[List[str]] = None
    best_practices: Optional[List[str]] = None

    doctrine_match: bool
    confidence_tier: Literal["high", "moderate", "requires_review"]
    response_layer: Literal["doctrine", "semantic", "deep_analysis"]
    latency_ms: float

    coverage_report: Optional[Dict[str, Any]] = None
    determinism_hash: Optional[str] = None

    reasoning_trace: Optional[List[ReasoningStep]] = None
    limitations: List[str] = Field(default_factory=list)

    timestamp: str
    version: str = ENGINE_VERSION
    engine_id: str = ENGINE_ID

    disclosure_caveat: str = Field(
        default="This analysis is for informational purposes. Consult qualified legal counsel for binding legal opinions."
    )


class ClauseExtractionResponse(BaseModel):
    """Response from clause extraction analysis."""
    extraction_id: str
    contract_id: Optional[str]
    total_clauses: int
    clauses: List[ClauseAnalysis]
    overall_risk_score: float
    overall_risk_level: RiskLevel
    risk_summary: Dict[str, int]
    boilerplate_count: int
    custom_count: int
    missing_standard_clauses: List[str]
    recommendations: List[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str
    version: str = ENGINE_VERSION


class RiskAssessmentResponse(BaseModel):
    """Response from risk assessment."""
    assessment_id: str
    contract_id: Optional[str]
    overall_risk_level: RiskLevel
    overall_risk_score: float
    risk_findings: List[RiskFinding]
    risk_distribution: Dict[str, int]
    critical_issues: List[str]
    recommendations: List[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str
    version: str = ENGINE_VERSION


class ComplianceCheckResponse(BaseModel):
    """Response from compliance check."""
    check_id: str
    contract_id: Optional[str]
    overall_status: ComplianceStatus
    frameworks_checked: List[str]
    findings: List[ComplianceFinding]
    compliance_score: float
    remediation_summary: List[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str
    version: str = ENGINE_VERSION


class ObligationTrackingResponse(BaseModel):
    """Response from obligation tracking."""
    tracking_id: str
    contract_id: Optional[str]
    total_obligations: int
    obligations: List[ObligationItem]
    upcoming_deadlines: List[Dict[str, str]]
    party_summary: Dict[str, int]
    determinism_hash: str
    latency_ms: float
    timestamp: str
    version: str = ENGINE_VERSION


class HealthResponse(BaseModel):
    """System health check response."""
    status: Literal["healthy", "degraded", "unhealthy"]
    engine: str
    engine_id: str
    version: str
    tier: int
    mode: str
    uptime_seconds: float
    api_latency: Dict[str, float]
    doctrine_cache: Dict[str, Any]
    semantic_map: Dict[str, Any]
    search_index: Dict[str, Any]
    active_queries: int
    queries_last_hour: int
    error_rate: Dict[str, Any]
    timestamp: str


# ============================================================================
# DOCTRINE MATCHING ENGINE
# ============================================================================

class DoctrineMatchResult:
    """Result of matching a query against the doctrine cache."""

    def __init__(
        self,
        doctrine: Optional[DoctrineBlock],
        topic_key: Optional[str],
        match_score: int,
        authority_weight: int,
        all_candidates: List[Dict[str, Any]],
        determinism_hash: str,
    ):
        self.doctrine = doctrine
        self.topic_key = topic_key
        self.match_score = match_score
        self.authority_weight = authority_weight
        self.all_candidates = all_candidates
        self.determinism_hash = determinism_hash

    @property
    def is_match(self) -> bool:
        return self.doctrine is not None


def match_doctrine(
    query_text: str,
    contract_type: Optional[str] = None,
    min_score: int = 2,
) -> DoctrineMatchResult:
    """Match a normalized query against the doctrine cache.

    Algorithm:
        1. Tokenize normalized query
        2. Score each doctrine by keyword overlap
        3. Apply contract-type boost if applicable
        4. Select highest-scoring doctrine above threshold
        5. Compute determinism hash for reproducibility

    Args:
        query_text: Normalized query text.
        contract_type: Optional contract type for boosting.
        min_score: Minimum score to consider a match.

    Returns:
        DoctrineMatchResult with best match and audit trail.
    """
    lower_query = query_text.lower()
    candidates: List[Dict[str, Any]] = []

    for key, doctrine in DOCTRINE_CACHE.items():
        score = 0
        matched_keywords: List[str] = []

        for keyword in doctrine.keywords:
            if keyword.lower() in lower_query:
                score += 1
                matched_keywords.append(keyword)
                if len(keyword.split()) > 2:
                    score += 1

        if contract_type and doctrine.matches_contract_type(contract_type):
            score += 1

        if score > 0:
            candidates.append({
                "key": key,
                "topic": doctrine.topic,
                "score": score,
                "authority_weight": doctrine.get_authority_weight(),
                "matched_keywords": matched_keywords,
                "confidence": doctrine.confidence,
            })

    candidates.sort(key=lambda c: (-c["score"], -c["authority_weight"]))

    hash_input = f"{query_text}|{contract_type or 'none'}|{json.dumps([c['key'] for c in candidates[:5]])}"
    determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    if candidates and candidates[0]["score"] >= min_score:
        best = candidates[0]
        doctrine = DOCTRINE_CACHE[best["key"]]
        return DoctrineMatchResult(
            doctrine=doctrine,
            topic_key=best["key"],
            match_score=best["score"],
            authority_weight=best["authority_weight"],
            all_candidates=candidates[:10],
            determinism_hash=determinism_hash,
        )

    return DoctrineMatchResult(
        doctrine=None,
        topic_key=None,
        match_score=0,
        authority_weight=0,
        all_candidates=candidates[:10],
        determinism_hash=determinism_hash,
    )


# ============================================================================
# CLAUSE EXTRACTION ENGINE
# ============================================================================

_CLAUSE_PATTERNS: Dict[str, List[re.Pattern]] = {
    "indemnification": [
        re.compile(r"(?:indemnif(?:y|ication)|hold\s+harmless|defend\s+and\s+indemnif)", re.IGNORECASE),
    ],
    "limitation_of_liability": [
        re.compile(r"(?:limitation\s+of\s+liability|liability\s+(?:cap|ceiling|limit)|aggregate\s+liability|maximum\s+liability)", re.IGNORECASE),
    ],
    "confidentiality": [
        re.compile(r"(?:confidential\s+information|confidentiality|non[\s-]?disclosure|proprietary\s+information)", re.IGNORECASE),
    ],
    "termination": [
        re.compile(r"(?:terminat(?:ion|e)|expir(?:ation|e)|right\s+to\s+terminate)", re.IGNORECASE),
    ],
    "force_majeure": [
        re.compile(r"(?:force\s+majeure|act\s+of\s+god|beyond\s+(?:reasonable\s+)?control|unforeseeable)", re.IGNORECASE),
    ],
    "intellectual_property": [
        re.compile(r"(?:intellectual\s+property|ip\s+(?:ownership|rights|assignment)|work[\s-]?(?:for|made\s+for)\s+hire)", re.IGNORECASE),
    ],
    "governing_law": [
        re.compile(r"(?:governing\s+law|choice\s+of\s+law|governed\s+by|applicable\s+law)", re.IGNORECASE),
    ],
    "dispute_resolution": [
        re.compile(r"(?:dispute\s+resolution|arbitrat(?:ion|e)|mediat(?:ion|e)|forum\s+selection|jurisdiction)", re.IGNORECASE),
    ],
    "representations_warranties": [
        re.compile(r"(?:represent(?:ation)?s?\s+and\s+warrant(?:y|ies)|represents?\s+and\s+warrants?)", re.IGNORECASE),
    ],
    "assignment": [
        re.compile(r"(?:assignment|(?:anti[\s-]?)?assign(?:ment|able)|change\s+of\s+control|successors?\s+and\s+assigns?)", re.IGNORECASE),
    ],
    "payment_terms": [
        re.compile(r"(?:payment\s+terms?|net\s+\d{2}|invoice|payment\s+(?:schedule|obligation)|late\s+payment)", re.IGNORECASE),
    ],
    "insurance": [
        re.compile(r"(?:insurance\s+(?:require|obligation|coverage)|certificate\s+of\s+insurance|additional\s+insured)", re.IGNORECASE),
    ],
    "data_protection": [
        re.compile(r"(?:data\s+protect(?:ion|ed)|gdpr|ccpa|personal\s+data|data\s+process(?:ing|or)|privacy)", re.IGNORECASE),
    ],
    "non_compete": [
        re.compile(r"(?:non[\s-]?compet(?:e|ition)|restrictive\s+covenant|non[\s-]?solicitation|exclusivity)", re.IGNORECASE),
    ],
    "scope_of_work": [
        re.compile(r"(?:scope\s+of\s+(?:work|services)|statement\s+of\s+work|deliverables?|acceptance\s+(?:criteria|testing))", re.IGNORECASE),
    ],
    "service_level": [
        re.compile(r"(?:service\s+level|sla|uptime|availability|performance\s+(?:standard|metric))", re.IGNORECASE),
    ],
    "auto_renewal": [
        re.compile(r"(?:auto(?:matic)?[\s-]?renewal|evergreen|renewal\s+term|non[\s-]?renewal\s+notice)", re.IGNORECASE),
    ],
    "entire_agreement": [
        re.compile(r"(?:entire\s+agreement|integration\s+clause|supersedes?\s+all\s+prior|merger\s+clause)", re.IGNORECASE),
    ],
    "severability": [
        re.compile(r"(?:severab(?:ility|le)|if\s+any\s+provision.*(?:invalid|unenforceable))", re.IGNORECASE),
    ],
    "waiver": [
        re.compile(r"(?:waiver|failure\s+to\s+enforce.*(?:not|shall\s+not).*waiver|no\s+waiver)", re.IGNORECASE),
    ],
    "notices": [
        re.compile(r"(?:notice(?:s)?\s+(?:shall|must|will)\s+be\s+(?:in\s+writing|given|sent|delivered))", re.IGNORECASE),
    ],
    "counterparts": [
        re.compile(r"(?:counterparts?|executed\s+in\s+(?:one\s+or\s+more\s+)?counterparts?)", re.IGNORECASE),
    ],
    "amendment": [
        re.compile(r"(?:amend(?:ment|ed)|modif(?:ication|ied)|no\s+oral\s+(?:amendment|modification))", re.IGNORECASE),
    ],
}


def extract_clauses_from_text(
    text: str,
    contract_type: Optional[str] = None,
    focus_clauses: Optional[List[str]] = None,
    include_risk: bool = True,
    include_boilerplate: bool = True,
) -> List[ClauseAnalysis]:
    """Extract and analyze clauses from contract text.

    Splits text into paragraphs, matches each against clause patterns,
    and produces structured analysis for each identified clause.

    Args:
        text: Full or partial contract text.
        contract_type: Type of contract for context.
        focus_clauses: Optional list of clause types to focus on.
        include_risk: Whether to include risk assessment.
        include_boilerplate: Whether to detect boilerplate.

    Returns:
        List of ClauseAnalysis objects.
    """
    paragraphs = _split_into_paragraphs(text)
    clauses: List[ClauseAnalysis] = []
    seen_types: set = set()

    target_patterns = _CLAUSE_PATTERNS
    if focus_clauses:
        normalized_focus = {normalize_clause_type(c) for c in focus_clauses}
        target_patterns = {
            k: v for k, v in _CLAUSE_PATTERNS.items()
            if k in normalized_focus or normalize_clause_type(k) in normalized_focus
        }

    for para_idx, paragraph in enumerate(paragraphs):
        if len(paragraph.strip()) < 30:
            continue

        for clause_type, patterns in target_patterns.items():
            for pattern in patterns:
                if pattern.search(paragraph):
                    if clause_type in seen_types and len(paragraph) < 200:
                        continue

                    clause_analysis = _analyze_clause(
                        clause_text=paragraph,
                        clause_type=clause_type,
                        contract_type=contract_type,
                        include_risk=include_risk,
                        include_boilerplate=include_boilerplate,
                        paragraph_index=para_idx,
                    )
                    clauses.append(clause_analysis)
                    seen_types.add(clause_type)
                    break

    return clauses


def _split_into_paragraphs(text: str) -> List[str]:
    """Split contract text into meaningful paragraphs.

    Handles section numbering, lettered subsections, and clause delimiters.
    """
    section_pattern = re.compile(
        r"(?:^|\n)(?:"
        r"\d+\.\s+"
        r"|[A-Z]+\.\s+"
        r"|Section\s+\d+"
        r"|Article\s+[IVX\d]+"
        r"|ARTICLE\s+[IVX\d]+"
        r"|(?:\([a-z]\)|\([ivx]+\))\s+"
        r")",
        re.MULTILINE,
    )

    split_points = [m.start() for m in section_pattern.finditer(text)]

    if not split_points:
        return [p.strip() for p in text.split("\n\n") if p.strip()]

    paragraphs: List[str] = []
    for i, start in enumerate(split_points):
        end = split_points[i + 1] if i + 1 < len(split_points) else len(text)
        para = text[start:end].strip()
        if para:
            paragraphs.append(para)

    if not paragraphs:
        return [p.strip() for p in text.split("\n\n") if p.strip()]

    return paragraphs


def _analyze_clause(
    clause_text: str,
    clause_type: str,
    contract_type: Optional[str],
    include_risk: bool,
    include_boilerplate: bool,
    paragraph_index: int,
) -> ClauseAnalysis:
    """Analyze a single extracted clause."""
    clause_id = f"clause_{paragraph_index}_{clause_type}_{uuid.uuid4().hex[:8]}"

    category = _get_clause_category(clause_type)

    is_bp = False
    custom_score = 1.0
    if include_boilerplate:
        is_bp, bp_conf, bp_match = detect_boilerplate(clause_text, clause_type)
        custom_score = compute_customization_score(clause_text, clause_type)

    risk_level = RiskLevel.MEDIUM
    risk_score = 0.5
    risk_factors: List[str] = []
    if include_risk:
        risk_level, risk_score, risk_factors = _assess_clause_risk(clause_text, clause_type, contract_type)

    key_provisions = _extract_key_provisions(clause_text, clause_type)
    missing_provisions = _identify_missing_provisions(clause_text, clause_type)
    negotiation_points = _generate_negotiation_points(clause_text, clause_type, risk_factors)

    doctrine_key = _find_applicable_doctrine(clause_type)

    summary = _generate_clause_summary(clause_text, clause_type, risk_level, is_bp)

    return ClauseAnalysis(
        clause_id=clause_id,
        clause_type=clause_type,
        clause_category=category,
        clause_text=clause_text[:2000],
        summary=summary,
        is_boilerplate=is_bp,
        customization_score=custom_score,
        risk_level=risk_level,
        risk_score=risk_score,
        risk_factors=risk_factors,
        key_provisions=key_provisions,
        missing_provisions=missing_provisions,
        negotiation_points=negotiation_points,
        doctrine_applicable=doctrine_key,
        confidence=round(0.7 + (0.2 if doctrine_key else 0.0), 3),
    )


def _get_clause_category(clause_type: str) -> str:
    """Map clause type to category."""
    category_map: Dict[str, str] = {
        "indemnification": "financial",
        "limitation_of_liability": "financial",
        "confidentiality": "ip_data",
        "termination": "termination",
        "force_majeure": "legal",
        "intellectual_property": "ip_data",
        "governing_law": "legal",
        "dispute_resolution": "legal",
        "representations_warranties": "legal",
        "assignment": "change_control",
        "payment_terms": "financial",
        "insurance": "financial",
        "data_protection": "ip_data",
        "non_compete": "operational",
        "scope_of_work": "operational",
        "service_level": "operational",
        "auto_renewal": "termination",
        "entire_agreement": "boilerplate",
        "severability": "boilerplate",
        "waiver": "boilerplate",
        "notices": "boilerplate",
        "counterparts": "boilerplate",
        "amendment": "boilerplate",
    }
    return category_map.get(clause_type, "other")


def _assess_clause_risk(
    clause_text: str,
    clause_type: str,
    contract_type: Optional[str],
) -> Tuple[RiskLevel, float, List[str]]:
    """Assess risk level for a clause."""
    lower = clause_text.lower()
    risk_flags: List[str] = []
    base_score = 0.3

    high_risk_indicators = {
        "unlimited liability": 0.25,
        "sole remedy": 0.15,
        "waive all": 0.2,
        "irrevocable": 0.1,
        "perpetual": 0.1,
        "exclusive remedy": 0.15,
        "without limitation": 0.15,
        "as is": 0.15,
        "no warranty": 0.15,
        "consequential damages": 0.1,
        "punitive damages": 0.1,
        "willful misconduct": -0.1,
        "fraud": -0.05,
        "gross negligence": -0.05,
    }

    for indicator, adjustment in high_risk_indicators.items():
        if indicator in lower:
            base_score += adjustment
            if adjustment > 0:
                risk_flags.append(f"Contains '{indicator}' language")

    clause_risk_baseline: Dict[str, float] = {
        "indemnification": 0.15,
        "limitation_of_liability": 0.2,
        "force_majeure": 0.1,
        "non_compete": 0.15,
        "assignment": 0.1,
        "termination": 0.1,
        "data_protection": 0.15,
        "governing_law": 0.05,
        "intellectual_property": 0.15,
    }
    base_score += clause_risk_baseline.get(clause_type, 0.0)

    if "mutual" in lower or "each party" in lower:
        base_score -= 0.1
    if "reasonable" in lower:
        base_score -= 0.05
    if "shall not exceed" in lower:
        base_score -= 0.05

    if clause_type == "indemnification":
        if "defend" not in lower:
            risk_flags.append("No defense obligation in indemnification clause")
            base_score += 0.05
        if "cap" not in lower and "limit" not in lower and "maximum" not in lower:
            risk_flags.append("Indemnification may be uncapped")
            base_score += 0.1

    if clause_type == "limitation_of_liability":
        if "consequential" not in lower:
            risk_flags.append("Consequential damages exclusion not apparent")
        if "willful" not in lower and "fraud" not in lower:
            risk_flags.append("No carve-out for willful misconduct/fraud detected")
            base_score += 0.1

    if clause_type == "termination":
        if "cure" not in lower and "grace" not in lower:
            risk_flags.append("No cure period detected")
            base_score += 0.05
        if "notice" not in lower:
            risk_flags.append("No notice requirement detected")
            base_score += 0.05

    if clause_type == "force_majeure":
        if "pandemic" not in lower and "epidemic" not in lower:
            risk_flags.append("No pandemic/epidemic enumeration (post-COVID gap)")
            base_score += 0.05
        if "mitigation" not in lower and "mitigat" not in lower:
            risk_flags.append("No mitigation obligation")
            base_score += 0.05

    if clause_type == "data_protection":
        if "breach" not in lower and "notification" not in lower:
            risk_flags.append("No data breach notification provision")
            base_score += 0.1
        if "sub-processor" not in lower and "subprocessor" not in lower:
            risk_flags.append("No sub-processor management provision")
            base_score += 0.05

    if clause_type == "intellectual_property":
        if "background" not in lower and "pre-existing" not in lower:
            risk_flags.append("Background IP not addressed")
            base_score += 0.05
        if "license" not in lower:
            risk_flags.append("No license-back provision for background IP")
            base_score += 0.05

    score = max(0.0, min(1.0, base_score))

    if score >= 0.8:
        level = RiskLevel.CRITICAL
    elif score >= 0.6:
        level = RiskLevel.HIGH
    elif score >= 0.4:
        level = RiskLevel.MEDIUM
    elif score >= 0.2:
        level = RiskLevel.LOW
    else:
        level = RiskLevel.NEGLIGIBLE

    return level, round(score, 3), risk_flags


def _extract_key_provisions(clause_text: str, clause_type: str) -> List[str]:
    """Extract key provisions from clause text."""
    lower = clause_text.lower()
    provisions: List[str] = []

    general_patterns = {
        "mutual obligation": r"\b(?:each\s+party|both\s+parties|mutual(?:ly)?)\b",
        "written notice required": r"\bwritten\s+notice\b",
        "time limitation specified": r"\b\d+\s+(?:day|month|year|business\s+day)s?\b",
        "dollar amount specified": r"\$[\d,]+(?:\.\d{2})?",
        "percentage specified": r"\b\d+(?:\.\d+)?%\b",
        "termination right": r"\bright\s+to\s+terminat",
        "consent required": r"\b(?:prior\s+)?(?:written\s+)?consent\b",
        "survival provision": r"\bsurviv(?:es?|al|ing)\b",
        "governing law specified": r"\bgoverned\s+by\s+(?:the\s+)?law",
    }

    for label, pattern in general_patterns.items():
        if re.search(pattern, lower):
            provisions.append(label)

    type_provisions: Dict[str, Dict[str, str]] = {
        "indemnification": {
            "defense obligation": r"\bdefend\b",
            "third-party claims covered": r"\bthird[\s-]?party\b",
            "attorneys fees included": r"\b(?:attorney|counsel)\s*(?:'s|s')?\s*fees?\b",
        },
        "limitation_of_liability": {
            "aggregate cap": r"\baggregate\b",
            "per-occurrence limit": r"\bper[\s-]?(?:occurrence|incident|claim)\b",
            "carve-outs present": r"\b(?:exclud(?:es?|ing)|carve[\s-]?out|(?:shall|does)\s+not\s+apply)\b",
        },
        "termination": {
            "cure period": r"\bcure\s+period\b",
            "wind-down obligations": r"\bwind[\s-]?down|transition\b",
            "survival clause": r"\bsurviv\b",
        },
        "confidentiality": {
            "marking requirement": r"\bmark(?:ed|ing)\b",
            "exceptions listed": r"\bexcept(?:ion|ed|s)\b",
            "return/destroy obligation": r"\b(?:return|destroy|destruct)\b",
        },
    }

    if clause_type in type_provisions:
        for label, pattern in type_provisions[clause_type].items():
            if re.search(pattern, lower):
                provisions.append(label)

    return provisions[:10]


def _identify_missing_provisions(clause_text: str, clause_type: str) -> List[str]:
    """Identify standard provisions missing from a clause."""
    lower = clause_text.lower()
    missing: List[str] = []

    expected: Dict[str, List[Tuple[str, str]]] = {
        "indemnification": [
            ("defense obligation", r"\bdefend\b"),
            ("notice requirement", r"\bnotice\b"),
            ("duty to mitigate", r"\bmitigat"),
            ("cap reference", r"\b(?:cap|limit|maximum|aggregate)\b"),
        ],
        "limitation_of_liability": [
            ("fraud/willful misconduct carve-out", r"\b(?:fraud|willful)\b"),
            ("IP infringement carve-out", r"\b(?:infring|intellectual\s+property)\b"),
            ("data breach carve-out", r"\bdata\s+(?:breach|protection)\b"),
        ],
        "termination": [
            ("cure period", r"\bcure\b"),
            ("notice requirement", r"\bnotice\b"),
            ("wind-down provisions", r"\b(?:wind[\s-]?down|transition)\b"),
            ("survival clause", r"\bsurviv"),
        ],
        "confidentiality": [
            ("standard exceptions", r"\bexcept(?:ion|s|ed)\b"),
            ("return/destroy obligation", r"\b(?:return|destroy|destruct)\b"),
            ("injunctive relief", r"\binjunctiv"),
            ("duration specified", r"\b\d+\s+(?:year|month)s?\b"),
        ],
        "force_majeure": [
            ("pandemic/epidemic", r"\b(?:pandemic|epidemic)\b"),
            ("cyber events", r"\b(?:cyber|ransomware|data\s+breach)\b"),
            ("mitigation obligation", r"\bmitigat"),
            ("termination trigger", r"\bterminat"),
            ("notice requirement", r"\bnotice\b"),
        ],
        "data_protection": [
            ("breach notification timing", r"\b(?:72\s+hour|breach\s+notif)\b"),
            ("sub-processor management", r"\bsub[\s-]?processor\b"),
            ("cross-border transfers", r"\b(?:cross[\s-]?border|transfer|scc)\b"),
            ("data subject rights", r"\bdata\s+subject\b"),
        ],
        "intellectual_property": [
            ("background IP carve-out", r"\bbackground\b"),
            ("license-back provision", r"\blicense[\s-]?back\b"),
            ("moral rights waiver", r"\bmoral\s+rights?\b"),
            ("assignment language", r"\b(?:hereby\s+)?assign"),
        ],
        "governing_law": [
            ("conflicts of law waiver", r"\bconflict\s+of\s+law"),
            ("CISG opt-out", r"\bcisg\b"),
            ("jury trial waiver", r"\bjury\b"),
        ],
    }

    if clause_type in expected:
        for label, pattern in expected[clause_type]:
            if not re.search(pattern, lower):
                missing.append(label)

    return missing


def _generate_negotiation_points(
    clause_text: str,
    clause_type: str,
    risk_factors: List[str],
) -> List[str]:
    """Generate negotiation points based on clause analysis."""
    points: List[str] = []

    for factor in risk_factors:
        if "uncapped" in factor.lower():
            points.append("Negotiate a reasonable cap on this obligation")
        if "no cure" in factor.lower():
            points.append("Request a 30-day cure period before termination")
        if "no notice" in factor.lower():
            points.append("Add written notice requirement with reasonable timeline")
        if "no carve-out" in factor.lower():
            points.append("Add carve-outs for fraud, willful misconduct, and IP infringement")
        if "pandemic" in factor.lower():
            points.append("Update force majeure to include pandemic/epidemic events")
        if "no defense" in factor.lower():
            points.append("Add defense obligation (not just indemnification)")
        if "no breach notification" in factor.lower():
            points.append("Add 72-hour breach notification requirement")
        if "background ip" in factor.lower():
            points.append("Identify and carve out pre-existing background IP")

    doctrine_key = _find_applicable_doctrine(clause_type)
    if doctrine_key and doctrine_key in DOCTRINE_CACHE:
        doctrine = DOCTRINE_CACHE[doctrine_key]
        for practice in doctrine.best_practices[:3]:
            if practice not in points:
                points.append(practice)

    return points[:8]


def _find_applicable_doctrine(clause_type: str) -> Optional[str]:
    """Find the most applicable doctrine for a clause type."""
    type_doctrine_map: Dict[str, str] = {
        "indemnification": "indemnification_general",
        "limitation_of_liability": "limitation_of_liability",
        "confidentiality": "confidentiality_nda",
        "termination": "termination_for_cause",
        "force_majeure": "force_majeure",
        "intellectual_property": "ip_ownership",
        "governing_law": "governing_law",
        "dispute_resolution": "governing_law",
        "representations_warranties": "representations_warranties",
        "assignment": "assignment_change_of_control",
        "payment_terms": "payment_terms",
        "insurance": "insurance_requirements",
        "data_protection": "data_protection",
        "non_compete": "restrictive_covenants",
        "scope_of_work": "scope_of_work",
        "service_level": "service_level_agreement",
        "auto_renewal": "auto_renewal",
    }
    return type_doctrine_map.get(clause_type)


def _generate_clause_summary(
    clause_text: str,
    clause_type: str,
    risk_level: RiskLevel,
    is_boilerplate: bool,
) -> str:
    """Generate a concise summary of the clause."""
    readable_type = clause_type.replace("_", " ").title()

    if is_boilerplate:
        return f"Standard boilerplate {readable_type} clause. Language appears to follow market conventions."

    risk_desc = {
        RiskLevel.CRITICAL: "contains critical risk factors requiring immediate attention",
        RiskLevel.HIGH: "presents elevated risk warranting careful review",
        RiskLevel.MEDIUM: "contains moderate risk factors for consideration",
        RiskLevel.LOW: "presents low risk with standard protections",
        RiskLevel.NEGLIGIBLE: "presents minimal risk exposure",
    }

    return f"{readable_type} clause that {risk_desc.get(risk_level, 'requires review')}."


# ============================================================================
# RISK ASSESSMENT ENGINE
# ============================================================================

def assess_contract_risk(
    clauses: List[ClauseAnalysis],
    contract_type: Optional[str] = None,
    risk_tolerance: str = "moderate",
) -> Tuple[RiskLevel, float, List[RiskFinding], List[str]]:
    """Assess overall contract risk from extracted clauses.

    Args:
        clauses: List of extracted clause analyses.
        contract_type: Optional contract type for context.
        risk_tolerance: Risk tolerance level.

    Returns:
        Tuple of (overall_level, overall_score, findings, critical_issues).
    """
    if not clauses:
        return RiskLevel.LOW, 0.2, [], ["No clauses analyzed — unable to assess risk"]

    findings: List[RiskFinding] = []
    critical_issues: List[str] = []
    total_score = 0.0
    weights: Dict[str, float] = {
        "financial": 0.25,
        "operational": 0.20,
        "legal": 0.20,
        "termination": 0.15,
        "ip_data": 0.10,
        "change_control": 0.10,
    }

    category_scores: Dict[str, List[float]] = {}
    for clause in clauses:
        cat = clause.clause_category
        if cat not in category_scores:
            category_scores[cat] = []
        category_scores[cat].append(clause.risk_score)

        if clause.risk_level in (RiskLevel.CRITICAL, RiskLevel.HIGH):
            finding = RiskFinding(
                risk_id=f"risk_{uuid.uuid4().hex[:8]}",
                clause_type=clause.clause_type,
                risk_level=clause.risk_level,
                risk_score=clause.risk_score,
                description=clause.summary,
                factors=clause.risk_factors,
                mitigation=clause.negotiation_points[:3],
                recommendation=clause.negotiation_points[0] if clause.negotiation_points else "Review with legal counsel",
                confidence=clause.confidence,
            )
            findings.append(finding)

            if clause.risk_level == RiskLevel.CRITICAL:
                critical_issues.append(
                    f"CRITICAL: {clause.clause_type.replace('_', ' ').title()} — {', '.join(clause.risk_factors[:2])}"
                )

    for cat, scores in category_scores.items():
        weight = weights.get(cat, 0.05)
        avg_score = sum(scores) / len(scores)
        total_score += avg_score * weight

    standard_clause_types = {
        "indemnification", "limitation_of_liability", "confidentiality",
        "termination", "governing_law", "representations_warranties",
    }
    found_types = {c.clause_type for c in clauses}
    missing = standard_clause_types - found_types
    if missing:
        for m in missing:
            critical_issues.append(f"Missing standard clause: {m.replace('_', ' ').title()}")
        total_score += 0.05 * len(missing)

    total_score = min(1.0, total_score)

    tolerance_adjustment = {"conservative": 0.05, "moderate": 0.0, "aggressive": -0.05}
    total_score += tolerance_adjustment.get(risk_tolerance, 0.0)
    total_score = max(0.0, min(1.0, total_score))

    if total_score >= 0.8:
        overall = RiskLevel.CRITICAL
    elif total_score >= 0.6:
        overall = RiskLevel.HIGH
    elif total_score >= 0.4:
        overall = RiskLevel.MEDIUM
    elif total_score >= 0.2:
        overall = RiskLevel.LOW
    else:
        overall = RiskLevel.NEGLIGIBLE

    return overall, round(total_score, 3), findings, critical_issues


# ============================================================================
# COMPLIANCE ENGINE
# ============================================================================

_COMPLIANCE_FRAMEWORKS: Dict[str, List[Dict[str, str]]] = {
    "general": [
        {"requirement": "Governing law specified", "check": r"\bgoverning\s+law|choice\s+of\s+law|governed\s+by\b"},
        {"requirement": "Dispute resolution mechanism", "check": r"\bdispute\s+resolution|arbitration|mediation\b"},
        {"requirement": "Limitation of liability present", "check": r"\blimitation\s+of\s+liability|liability\s+cap\b"},
        {"requirement": "Confidentiality provisions", "check": r"\bconfidential|non[\s-]?disclosure\b"},
        {"requirement": "Termination provisions", "check": r"\bterminat(?:ion|e)\b"},
        {"requirement": "Indemnification present", "check": r"\bindemnif(?:y|ication)\b"},
        {"requirement": "Assignment provisions", "check": r"\bassignment|assign(?:able)?\b"},
        {"requirement": "Notice provisions", "check": r"\bnotice(?:s)?\s+(?:shall|must|will)\b"},
        {"requirement": "Entire agreement clause", "check": r"\bentire\s+agreement|integration\s+clause\b"},
        {"requirement": "Severability clause", "check": r"\bseverab(?:ility|le)\b"},
    ],
    "gdpr": [
        {"requirement": "Data Processing Agreement (DPA)", "check": r"\bdata\s+processing\s+agreement|dpa\b"},
        {"requirement": "Controller/Processor classification", "check": r"\bcontroller|processor\b"},
        {"requirement": "Sub-processor management", "check": r"\bsub[\s-]?processor\b"},
        {"requirement": "Data breach notification (72 hours)", "check": r"\bbreach\s+notif|72\s+hour\b"},
        {"requirement": "Cross-border transfer mechanism", "check": r"\bcross[\s-]?border|standard\s+contractual|scc\b"},
        {"requirement": "Data subject rights", "check": r"\bdata\s+subject\s+rights?\b"},
        {"requirement": "Data Protection Impact Assessment", "check": r"\b(?:dpia|impact\s+assessment)\b"},
        {"requirement": "Records of processing", "check": r"\brecords?\s+of\s+processing\b"},
        {"requirement": "Security measures specified", "check": r"\bsecurity\s+measures?|technical.*organizational\b"},
        {"requirement": "Data retention/deletion", "check": r"\bretention|delet(?:ion|e)\b"},
    ],
    "ccpa": [
        {"requirement": "Personal information definition", "check": r"\bpersonal\s+information|pii\b"},
        {"requirement": "Sale of data addressed", "check": r"\bsale\s+of\s+(?:personal\s+)?(?:data|information)\b"},
        {"requirement": "Consumer rights provisions", "check": r"\bconsumer\s+rights?|right\s+to\s+(?:know|delete|opt)\b"},
        {"requirement": "Data sharing restrictions", "check": r"\bshar(?:e|ing)\s+(?:personal\s+)?(?:data|information)\b"},
        {"requirement": "Service provider obligations", "check": r"\bservice\s+provider\b"},
        {"requirement": "Opt-out mechanism", "check": r"\bopt[\s-]?out\b"},
    ],
    "sox": [
        {"requirement": "Internal controls provisions", "check": r"\binternal\s+controls?\b"},
        {"requirement": "Audit rights specified", "check": r"\baudit\s+rights?|right\s+to\s+audit\b"},
        {"requirement": "Financial reporting accuracy", "check": r"\bfinancial\s+report(?:ing)?\b"},
        {"requirement": "Record retention requirements", "check": r"\brecord\s+retention\b"},
        {"requirement": "Whistleblower protection", "check": r"\bwhistleblower\b"},
    ],
    "hipaa": [
        {"requirement": "Business Associate Agreement", "check": r"\bbusiness\s+associate\s+agreement|baa\b"},
        {"requirement": "PHI handling provisions", "check": r"\bprotected\s+health\s+information|phi\b"},
        {"requirement": "Minimum necessary standard", "check": r"\bminimum\s+necessary\b"},
        {"requirement": "Breach notification", "check": r"\bbreach\s+notif\b"},
        {"requirement": "Security safeguards", "check": r"\bsecurity\s+safeguards?|administrative.*physical.*technical\b"},
    ],
}


def check_compliance(
    contract_text: str,
    frameworks: List[str],
    contract_type: Optional[str] = None,
    jurisdiction: str = "US",
) -> Tuple[ComplianceStatus, float, List[ComplianceFinding]]:
    """Check contract compliance against specified frameworks.

    Args:
        contract_text: Full contract text.
        frameworks: List of framework identifiers to check.
        contract_type: Optional contract type.
        jurisdiction: Jurisdiction context.

    Returns:
        Tuple of (overall_status, score, findings).
    """
    findings: List[ComplianceFinding] = []
    total_checks = 0
    passed_checks = 0
    lower_text = contract_text.lower()

    for framework in frameworks:
        checks = _COMPLIANCE_FRAMEWORKS.get(framework, _COMPLIANCE_FRAMEWORKS["general"])

        for check in checks:
            total_checks += 1
            finding_id = f"comp_{uuid.uuid4().hex[:8]}"
            requirement = check["requirement"]
            pattern = check["check"]

            match = re.search(pattern, lower_text, re.IGNORECASE)
            if match:
                status = ComplianceStatus.COMPLIANT
                passed_checks += 1
                description = f"Contract contains provisions addressing: {requirement}"
                remediation = None
                confidence = 0.85
            else:
                status = ComplianceStatus.NON_COMPLIANT
                description = f"Contract does not appear to address: {requirement}"
                remediation = f"Add provisions addressing {requirement.lower()}"
                confidence = 0.75

            findings.append(ComplianceFinding(
                finding_id=finding_id,
                framework=framework,
                requirement=requirement,
                status=status,
                description=description,
                remediation=remediation,
                confidence=confidence,
            ))

    score = passed_checks / max(1, total_checks)

    if score >= 0.9:
        overall = ComplianceStatus.COMPLIANT
    elif score >= 0.7:
        overall = ComplianceStatus.PARTIALLY_COMPLIANT
    elif score >= 0.5:
        overall = ComplianceStatus.REQUIRES_REVIEW
    else:
        overall = ComplianceStatus.NON_COMPLIANT

    return overall, round(score, 3), findings


# ============================================================================
# OBLIGATION EXTRACTION ENGINE
# ============================================================================

_OBLIGATION_PATTERNS: List[Dict[str, Any]] = [
    {"type": "delivery", "pattern": re.compile(r"(?:shall|will|must)\s+deliver", re.IGNORECASE), "party_hint": "provider"},
    {"type": "payment", "pattern": re.compile(r"(?:shall|will|must)\s+pay", re.IGNORECASE), "party_hint": "buyer"},
    {"type": "notice", "pattern": re.compile(r"(?:shall|will|must)\s+(?:provide|give|send)\s+(?:written\s+)?notice", re.IGNORECASE), "party_hint": "either"},
    {"type": "compliance", "pattern": re.compile(r"(?:shall|will|must)\s+comply", re.IGNORECASE), "party_hint": "both"},
    {"type": "insurance", "pattern": re.compile(r"(?:shall|will|must)\s+maintain\s+(?:.*\s+)?insurance", re.IGNORECASE), "party_hint": "provider"},
    {"type": "confidentiality", "pattern": re.compile(r"(?:shall|will|must)\s+(?:keep|maintain)\s+(?:.*\s+)?confidential", re.IGNORECASE), "party_hint": "both"},
    {"type": "reporting", "pattern": re.compile(r"(?:shall|will|must)\s+(?:provide|submit|deliver)\s+(?:.*\s+)?report", re.IGNORECASE), "party_hint": "provider"},
    {"type": "consent", "pattern": re.compile(r"(?:shall|will|must)\s+(?:obtain|secure)\s+(?:.*\s+)?consent", re.IGNORECASE), "party_hint": "either"},
    {"type": "indemnification", "pattern": re.compile(r"(?:shall|will|must)\s+(?:indemnify|defend|hold\s+harmless)", re.IGNORECASE), "party_hint": "either"},
    {"type": "return", "pattern": re.compile(r"(?:shall|will|must)\s+(?:return|destroy|delete)", re.IGNORECASE), "party_hint": "either"},
    {"type": "performance", "pattern": re.compile(r"(?:shall|will|must)\s+(?:perform|execute|complete|provide)", re.IGNORECASE), "party_hint": "provider"},
    {"type": "restriction", "pattern": re.compile(r"(?:shall|will|must)\s+not\b", re.IGNORECASE), "party_hint": "either"},
]

_DEADLINE_PATTERNS: List[re.Pattern] = [
    re.compile(r"within\s+(\d+)\s+(day|business\s+day|month|year|week|hour)s?", re.IGNORECASE),
    re.compile(r"no\s+later\s+than\s+(\d+)\s+(day|business\s+day|month|year|week)s?", re.IGNORECASE),
    re.compile(r"(\d+)\s+(day|business\s+day|month|year|week)s?\s+(?:after|from|following)", re.IGNORECASE),
    re.compile(r"(?:by|before|on\s+or\s+before)\s+(\w+\s+\d{1,2},?\s+\d{4})", re.IGNORECASE),
    re.compile(r"(?:annual(?:ly)?|quarterly|monthly|weekly|daily)", re.IGNORECASE),
]


def extract_obligations(
    contract_text: str,
    contract_type: Optional[str] = None,
    effective_date: Optional[str] = None,
) -> List[ObligationItem]:
    """Extract obligations and deadlines from contract text.

    Args:
        contract_text: Contract text to analyze.
        contract_type: Optional contract type context.
        effective_date: Contract effective date for deadline calculation.

    Returns:
        List of ObligationItem objects.
    """
    paragraphs = contract_text.split("\n")
    obligations: List[ObligationItem] = []
    seen_sigs: set = set()

    for para_idx, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        if len(paragraph) < 20:
            continue

        for obl_pattern in _OBLIGATION_PATTERNS:
            match = obl_pattern["pattern"].search(paragraph)
            if match:
                sig = hashlib.sha256(paragraph[:100].encode()).hexdigest()[:12]
                if sig in seen_sigs:
                    continue
                seen_sigs.add(sig)

                deadline = _extract_deadline(paragraph)
                is_recurring = bool(re.search(r"(?:annual|quarterly|monthly|weekly|daily|periodic|ongoing)", paragraph, re.IGNORECASE))
                recurrence = None
                if is_recurring:
                    recurrence_match = re.search(r"(annual(?:ly)?|quarterly|monthly|weekly|daily)", paragraph, re.IGNORECASE)
                    if recurrence_match:
                        recurrence = recurrence_match.group(1).lower()

                obligation = ObligationItem(
                    obligation_id=f"obl_{para_idx}_{uuid.uuid4().hex[:6]}",
                    party=obl_pattern["party_hint"],
                    obligation_type=obl_pattern["type"],
                    description=paragraph[:500],
                    deadline=deadline,
                    recurring=is_recurring,
                    recurrence_pattern=recurrence,
                    clause_reference=f"paragraph_{para_idx + 1}",
                    priority="high" if obl_pattern["type"] in ("payment", "indemnification", "compliance") else "medium",
                )
                obligations.append(obligation)
                break

    return obligations


def _extract_deadline(text: str) -> Optional[str]:
    """Extract deadline information from text."""
    for pattern in _DEADLINE_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(0)
    return None


# ============================================================================
# EPISTEMIC GUARDRAILS
# ============================================================================

def apply_epistemic_guardrails(conclusion: str, confidence: float) -> Tuple[str, List[str]]:
    """Apply epistemic guardrails to prevent overconfident assertions.

    Args:
        conclusion: Analysis conclusion text.
        confidence: Confidence score.

    Returns:
        Tuple of (cleaned_conclusion, limitations_list).
    """
    cleaned = conclusion
    for phrase in BANNED_PHRASES:
        if phrase.lower() in cleaned.lower():
            cleaned = re.sub(re.escape(phrase), "[ASSERTION REMOVED]", cleaned, flags=re.IGNORECASE)

    limitations: List[str] = []

    limitations.append(
        "This analysis is for informational purposes only and does not constitute legal advice."
    )

    if confidence < 0.6:
        limitations.append(
            "Confidence level is below the high-confidence threshold. "
            "Review by qualified legal counsel is strongly recommended."
        )

    limitations.append(
        "Contract enforceability may vary by jurisdiction. Analysis assumes "
        "the specified governing law unless otherwise noted."
    )

    limitations.append(
        "Legal standards evolve. This analysis reflects current law as understood "
        f"at the time of analysis ({datetime.now(timezone.utc).strftime('%Y-%m-%d')})."
    )

    return cleaned, limitations


# ============================================================================
# RESPONSE BUILDER
# ============================================================================

def build_doctrine_response(
    query: ContractQuery,
    match: DoctrineMatchResult,
    norm_result: NormalizationResult,
    latency_ms: float,
    coverage: DoctrineCoverageMap,
) -> ContractResponse:
    """Build a full response from a doctrine match.

    Args:
        query: Original query.
        match: Doctrine match result.
        norm_result: Semantic normalization result.
        latency_ms: Response latency.
        coverage: Doctrine coverage map.

    Returns:
        Complete ContractResponse.
    """
    doctrine = match.doctrine
    if doctrine is None:
        return _build_no_match_response(query, match, norm_result, latency_ms, coverage)

    conclusion, limitations = apply_epistemic_guardrails(
        doctrine.conclusion_template,
        0.85 if match.match_score >= 4 else 0.7,
    )

    citations = [
        Citation(
            authority=auth.get("authority", "Unknown"),
            reference=auth.get("reference", ""),
            relevance=f"Primary authority for {doctrine.topic}",
        )
        for auth in doctrine.primary_authority
    ]

    risk_findings = None
    if query.mode in (ResponseMode.REVIEW, ResponseMode.MEMO):
        risk_findings = [
            RiskFinding(
                risk_id=f"risk_{uuid.uuid4().hex[:8]}",
                clause_type=match.topic_key or "unknown",
                risk_level=RiskLevel(doctrine.risk_severity.value),
                risk_score=0.6 if doctrine.risk_severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL) else 0.4,
                description=factor,
                factors=[factor],
                mitigation=doctrine.mitigation_strategies[:2],
                recommendation=doctrine.mitigation_strategies[0] if doctrine.mitigation_strategies else "Review with counsel",
                confidence=0.8,
            )
            for factor in doctrine.risk_factors[:5]
        ]

    negotiation = doctrine.negotiation_guidance if query.include_negotiation_guidance else None

    trace = None
    if query.include_trace:
        trace = [
            ReasoningStep(step=1, analysis=f"Query normalized: {norm_result.normalized[:200]}"),
            ReasoningStep(step=2, analysis=f"Doctrine match: {doctrine.topic} (score: {match.match_score})"),
            ReasoningStep(step=3, analysis=f"Authority weight: {match.authority_weight}"),
            ReasoningStep(step=4, analysis=doctrine.reasoning_framework[:500]),
        ]

    confidence_tier: Literal["high", "moderate", "requires_review"]
    if match.match_score >= 4:
        confidence_tier = "high"
    elif match.match_score >= 3:
        confidence_tier = "moderate"
    else:
        confidence_tier = "requires_review"

    return ContractResponse(
        query_id=str(uuid.uuid4()),
        question=query.question[:500],
        mode=query.mode,
        conclusion=conclusion,
        reasoning=doctrine.reasoning_framework,
        key_factors=doctrine.key_factors,
        citations=citations,
        risk_findings=risk_findings,
        negotiation_guidance=negotiation,
        common_pitfalls=doctrine.common_pitfalls if query.mode != ResponseMode.FAST else None,
        best_practices=doctrine.best_practices if query.mode != ResponseMode.FAST else None,
        doctrine_match=True,
        confidence_tier=confidence_tier,
        response_layer="doctrine",
        latency_ms=latency_ms,
        coverage_report=coverage.get_coverage_report(),
        determinism_hash=match.determinism_hash,
        reasoning_trace=trace,
        limitations=limitations,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def _build_no_match_response(
    query: ContractQuery,
    match: DoctrineMatchResult,
    norm_result: NormalizationResult,
    latency_ms: float,
    coverage: DoctrineCoverageMap,
) -> ContractResponse:
    """Build response when no doctrine matched."""
    conclusion = (
        "No specific contract law doctrine matched the query with sufficient confidence. "
        "The analysis will use general contract principles. For specialized legal questions, "
        "consult with qualified legal counsel who can review the specific contract terms "
        "and applicable jurisdiction."
    )

    _, limitations = apply_epistemic_guardrails(conclusion, 0.4)
    limitations.insert(0, "No specific doctrine matched. Analysis is general in nature.")

    return ContractResponse(
        query_id=str(uuid.uuid4()),
        question=query.question[:500],
        mode=query.mode,
        conclusion=conclusion,
        reasoning="General contract law principles apply. The query did not match any pre-compiled doctrine with sufficient specificity.",
        key_factors=["Query specificity", "Jurisdiction applicability", "Contract type context"],
        citations=[],
        doctrine_match=False,
        confidence_tier="requires_review",
        response_layer="semantic",
        latency_ms=latency_ms,
        coverage_report=coverage.get_coverage_report(),
        determinism_hash=match.determinism_hash,
        limitations=limitations,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

_start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("LG01 Contract Analysis Engine starting on port {}", ENGINE_PORT)
    lock_governance()
    _seed_search_index()
    logger.info("LG01 engine ready. Doctrines: {}, Semantic map integrity verified.", get_doctrine_count())
    yield
    logger.info("LG01 Contract Analysis Engine shutting down")


app = FastAPI(
    title="LG01 Contract Analysis Engine",
    description="Production-grade contract analysis engine providing deterministic clause extraction, risk assessment, obligation tracking, and compliance checking.",
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


def _seed_search_index() -> None:
    """Seed the search index with doctrine data."""
    index = get_search_index()
    for key, doctrine in DOCTRINE_CACHE.items():
        doc = SearchDocument(
            doc_id=f"doctrine_{key}",
            doc_type="doctrine",
            title=doctrine.topic,
            content=f"{doctrine.conclusion_template}\n{doctrine.reasoning_framework}",
            clause_type=key,
            risk_level=doctrine.risk_severity.value,
            tags=doctrine.keywords[:5],
            metadata={
                "category": doctrine.category.value,
                "confidence": doctrine.confidence_level.value,
                "authority_weight": doctrine.get_authority_weight(),
            },
        )
        index.add_document(doc)
    logger.info("Search index seeded with {} doctrine documents", len(DOCTRINE_CACHE))


# ============================================================================
# HEALTH ENDPOINT
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Comprehensive health check for operational monitoring."""
    metrics = get_metrics()
    sem_valid, sem_hash, sem_count = verify_integrity()
    index = get_search_index()
    index_stats = index.get_stats()
    telemetry = get_telemetry()

    error_stats = metrics.get_error_stats()
    error_rate_last_hour = error_stats["last_hour"]
    queries_hour = metrics.queries_last_hour()

    status: Literal["healthy", "degraded", "unhealthy"]
    if error_rate_last_hour > 10 or not sem_valid:
        status = "unhealthy"
    elif error_rate_last_hour > 3 or queries_hour > 1000:
        status = "degraded"
    else:
        status = "healthy"

    return HealthResponse(
        status=status,
        engine=ENGINE_NAME,
        engine_id=ENGINE_ID,
        version=ENGINE_VERSION,
        tier=ENGINE_TIER,
        mode=ENGINE_MODE,
        uptime_seconds=round(time.time() - _start_time, 2),
        api_latency=metrics.get_latency_stats(),
        doctrine_cache={
            "status": "loaded",
            "doctrines": get_doctrine_count(),
            "categories": len(get_all_categories()),
            "hit_rate": metrics.get_doctrine_hit_rate(),
            "interactions": len(DOCTRINE_INTERACTIONS),
        },
        semantic_map={
            "status": "valid" if sem_valid else "INTEGRITY_FAILURE",
            "entries": sem_count,
            "hash": sem_hash[:16],
            "integrity_valid": sem_valid,
        },
        search_index={
            "status": "loaded",
            "documents": index_stats.total_documents,
            "terms": index_stats.total_terms,
        },
        active_queries=metrics.active_queries,
        queries_last_hour=queries_hour,
        error_rate=error_stats,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ============================================================================
# CONTRACT QUERY ENDPOINT
# ============================================================================

@app.post("/analyze", response_model=ContractResponse)
async def analyze_contract(query: ContractQuery) -> ContractResponse:
    """Primary contract analysis endpoint.

    Matches query against doctrine cache, applies semantic normalization,
    and returns structured analysis with risk assessment and citations.
    """
    start = time.time()
    metrics = get_metrics()
    metrics.query_start()

    trace_id = trace_query(
        query_text=query.question,
        query_type=query.analysis_type.value,
        mode=query.mode.value,
        contract_type=query.contract_type.value if query.contract_type else None,
        contract_id=query.contract_id,
    )

    try:
        norm_result = normalize_semantics(query.question)
        norm_ms = (time.time() - start) * 1000

        match_start = time.time()
        match = match_doctrine(
            norm_result.normalized,
            contract_type=query.contract_type.value if query.contract_type else None,
        )
        match_ms = (time.time() - match_start) * 1000

        coverage = DoctrineCoverageMap()
        for key in DOCTRINE_CACHE:
            if match.topic_key and key == match.topic_key:
                coverage.mark_triggered(key)
            elif match.all_candidates and any(c["key"] == key for c in match.all_candidates):
                coverage.mark_not_triggered(key)

        latency_ms = (time.time() - start) * 1000

        response = build_doctrine_response(query, match, norm_result, latency_ms, coverage)

        metrics.record_query(latency_ms, match.is_match)
        metrics.query_end()

        complete_trace(
            trace_id=trace_id,
            query_text=query.question,
            query_type=query.analysis_type.value,
            mode=query.mode.value,
            contract_type=query.contract_type.value if query.contract_type else None,
            doctrine_matched=match.is_match,
            doctrine_id=match.topic_key,
            doctrine_topic=match.doctrine.topic if match.doctrine else None,
            confidence_score=0.85 if match.is_match else 0.4,
            response_layer=ResponseLayer.DOCTRINE if match.is_match else ResponseLayer.SEMANTIC,
            latency_ms=latency_ms,
            doctrine_lookup_ms=match_ms,
            semantic_lookup_ms=norm_ms,
            citations_count=len(response.citations),
            response_length=len(response.conclusion),
            contract_id=query.contract_id,
            determinism_hash=match.determinism_hash,
        )

        return response

    except Exception as exc:
        metrics.record_error(str(exc))
        metrics.query_end()
        log_error(ErrorDomain.DOCTRINE_ENGINE, str(exc), exc=exc, trace_id=trace_id)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(exc)}")


# ============================================================================
# CLAUSE EXTRACTION ENDPOINT
# ============================================================================

@app.post("/extract-clauses", response_model=ClauseExtractionResponse)
async def extract_clauses(request: ClauseExtractionRequest) -> ClauseExtractionResponse:
    """Extract and analyze clauses from contract text."""
    start = time.time()

    try:
        clauses = extract_clauses_from_text(
            text=request.contract_text,
            contract_type=request.contract_type.value if request.contract_type else None,
            focus_clauses=request.focus_clauses,
            include_risk=request.include_risk,
            include_boilerplate=request.include_boilerplate_detection,
        )

        risk_dist: Dict[str, int] = {}
        boilerplate_count = 0
        custom_count = 0
        total_risk = 0.0

        for clause in clauses:
            level = clause.risk_level.value
            risk_dist[level] = risk_dist.get(level, 0) + 1
            total_risk += clause.risk_score
            if clause.is_boilerplate:
                boilerplate_count += 1
            else:
                custom_count += 1

        overall_score = total_risk / max(1, len(clauses))
        if overall_score >= 0.7:
            overall_level = RiskLevel.HIGH
        elif overall_score >= 0.5:
            overall_level = RiskLevel.MEDIUM
        elif overall_score >= 0.3:
            overall_level = RiskLevel.LOW
        else:
            overall_level = RiskLevel.NEGLIGIBLE

        found_types = {c.clause_type for c in clauses}
        standard_types = {"indemnification", "limitation_of_liability", "confidentiality", "termination", "governing_law"}
        missing = sorted(standard_types - found_types)

        recommendations: List[str] = []
        if missing:
            recommendations.append(f"Missing standard clauses: {', '.join(t.replace('_', ' ').title() for t in missing)}")
        if risk_dist.get("critical", 0) > 0:
            recommendations.append("Critical risk clauses detected — prioritize legal review")
        if boilerplate_count > len(clauses) * 0.7:
            recommendations.append("High proportion of boilerplate — review for adequacy to specific transaction")

        hash_input = f"{len(clauses)}|{json.dumps(risk_dist)}|{overall_score}"
        determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()

        latency_ms = (time.time() - start) * 1000
        telemetry = get_telemetry()
        telemetry.record_clause_extraction(len(clauses))

        return ClauseExtractionResponse(
            extraction_id=str(uuid.uuid4()),
            contract_id=request.contract_id,
            total_clauses=len(clauses),
            clauses=clauses,
            overall_risk_score=round(overall_score, 3),
            overall_risk_level=overall_level,
            risk_summary=risk_dist,
            boilerplate_count=boilerplate_count,
            custom_count=custom_count,
            missing_standard_clauses=missing,
            recommendations=recommendations,
            determinism_hash=determinism_hash,
            latency_ms=round(latency_ms, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    except Exception as exc:
        log_error(ErrorDomain.CLAUSE_EXTRACTION, str(exc), exc=exc)
        raise HTTPException(status_code=500, detail=f"Clause extraction failed: {str(exc)}")


# ============================================================================
# RISK ASSESSMENT ENDPOINT
# ============================================================================

@app.post("/assess-risk", response_model=RiskAssessmentResponse)
async def assess_risk(request: RiskAssessmentRequest) -> RiskAssessmentResponse:
    """Comprehensive risk assessment of contract text."""
    start = time.time()

    try:
        clauses = extract_clauses_from_text(
            text=request.contract_text,
            contract_type=request.contract_type.value if request.contract_type else None,
            include_risk=True,
            include_boilerplate=True,
        )

        overall_level, overall_score, findings, critical_issues = assess_contract_risk(
            clauses=clauses,
            contract_type=request.contract_type.value if request.contract_type else None,
            risk_tolerance=request.risk_tolerance,
        )

        risk_dist: Dict[str, int] = {}
        for f in findings:
            level = f.risk_level.value
            risk_dist[level] = risk_dist.get(level, 0) + 1

        recommendations: List[str] = []
        for issue in critical_issues:
            recommendations.append(f"Address: {issue}")
        for finding in findings[:5]:
            recommendations.append(finding.recommendation)

        hash_input = f"{overall_score}|{len(findings)}|{json.dumps(sorted(critical_issues))}"
        determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()

        latency_ms = (time.time() - start) * 1000
        telemetry = get_telemetry()
        telemetry.record_risk_assessment(len(findings))

        return RiskAssessmentResponse(
            assessment_id=str(uuid.uuid4()),
            contract_id=request.contract_id,
            overall_risk_level=overall_level,
            overall_risk_score=overall_score,
            risk_findings=findings,
            risk_distribution=risk_dist,
            critical_issues=critical_issues,
            recommendations=recommendations,
            determinism_hash=determinism_hash,
            latency_ms=round(latency_ms, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    except Exception as exc:
        log_error(ErrorDomain.RISK_ASSESSMENT, str(exc), exc=exc)
        raise HTTPException(status_code=500, detail=f"Risk assessment failed: {str(exc)}")


# ============================================================================
# COMPLIANCE CHECK ENDPOINT
# ============================================================================

@app.post("/check-compliance", response_model=ComplianceCheckResponse)
async def compliance_check(request: ComplianceCheckRequest) -> ComplianceCheckResponse:
    """Check contract compliance against regulatory frameworks."""
    start = time.time()

    try:
        overall_status, score, findings = check_compliance(
            contract_text=request.contract_text,
            frameworks=request.frameworks,
            contract_type=request.contract_type.value if request.contract_type else None,
            jurisdiction=request.jurisdiction,
        )

        non_compliant = [f for f in findings if f.status == ComplianceStatus.NON_COMPLIANT]
        remediation_summary = [f.remediation for f in non_compliant if f.remediation]

        hash_input = f"{score}|{len(findings)}|{json.dumps(request.frameworks)}"
        determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()

        latency_ms = (time.time() - start) * 1000
        telemetry = get_telemetry()
        telemetry.record_compliance_check(len(findings))

        return ComplianceCheckResponse(
            check_id=str(uuid.uuid4()),
            contract_id=request.contract_id,
            overall_status=overall_status,
            frameworks_checked=request.frameworks,
            findings=findings,
            compliance_score=score,
            remediation_summary=remediation_summary,
            determinism_hash=determinism_hash,
            latency_ms=round(latency_ms, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    except Exception as exc:
        log_error(ErrorDomain.COMPLIANCE_CHECK, str(exc), exc=exc)
        raise HTTPException(status_code=500, detail=f"Compliance check failed: {str(exc)}")


# ============================================================================
# CONTRACT COMPARISON ENDPOINT
# ============================================================================

@app.post("/compare")
async def compare_contracts(request: ContractComparisonRequest) -> Dict[str, Any]:
    """Compare two contracts and identify differences."""
    start = time.time()

    try:
        clauses_a = extract_clauses_from_text(request.contract_a_text, include_risk=False, include_boilerplate=False)
        clauses_b = extract_clauses_from_text(request.contract_b_text, include_risk=False, include_boilerplate=False)

        dict_a = {c.clause_type: c.clause_text for c in clauses_a}
        dict_b = {c.clause_type: c.clause_text for c in clauses_b}

        result = compare_clauses(dict_a, dict_b, request.contract_a_id, request.contract_b_id)

        latency_ms = (time.time() - start) * 1000
        response = result.to_dict()
        response["latency_ms"] = round(latency_ms, 2)
        return response

    except Exception as exc:
        log_error(ErrorDomain.CLAUSE_EXTRACTION, str(exc), exc=exc)
        raise HTTPException(status_code=500, detail=f"Contract comparison failed: {str(exc)}")


# ============================================================================
# OBLIGATION TRACKING ENDPOINT
# ============================================================================

@app.post("/track-obligations", response_model=ObligationTrackingResponse)
async def track_obligations(request: ObligationTrackingRequest) -> ObligationTrackingResponse:
    """Extract and track obligations from contract text."""
    start = time.time()

    try:
        obligations = extract_obligations(
            contract_text=request.contract_text,
            contract_type=request.contract_type.value if request.contract_type else None,
            effective_date=request.effective_date,
        )

        upcoming = [
            {"obligation_id": o.obligation_id, "type": o.obligation_type, "deadline": o.deadline or "not specified"}
            for o in obligations
            if o.deadline
        ][:10]

        party_summary: Dict[str, int] = {}
        for o in obligations:
            party_summary[o.party] = party_summary.get(o.party, 0) + 1

        hash_input = f"{len(obligations)}|{json.dumps(sorted(party_summary.keys()))}"
        determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()

        latency_ms = (time.time() - start) * 1000

        return ObligationTrackingResponse(
            tracking_id=str(uuid.uuid4()),
            contract_id=request.contract_id,
            total_obligations=len(obligations),
            obligations=obligations,
            upcoming_deadlines=upcoming,
            party_summary=party_summary,
            determinism_hash=determinism_hash,
            latency_ms=round(latency_ms, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    except Exception as exc:
        log_error(ErrorDomain.CONTRACT_PARSING, str(exc), exc=exc)
        raise HTTPException(status_code=500, detail=f"Obligation tracking failed: {str(exc)}")


# ============================================================================
# SEARCH ENDPOINT
# ============================================================================

@app.post("/search")
async def search_clauses(request: SearchRequest) -> Dict[str, Any]:
    """Search the clause and doctrine index."""
    start = time.time()

    try:
        scope_map = {
            "clauses": SearchScope.CLAUSES,
            "doctrines": SearchScope.DOCTRINES,
            "contracts": SearchScope.CONTRACTS,
            "all": SearchScope.ALL,
        }

        query = SearchQuery(
            query_text=request.query,
            scope=scope_map.get(request.scope, SearchScope.ALL),
            clause_type_filter=request.clause_type,
            risk_level_filter=request.risk_level,
            max_results=request.max_results,
        )

        index = get_search_index()
        results = index.search(query)
        latency_ms = (time.time() - start) * 1000

        return {
            "query": request.query,
            "total_results": len(results),
            "results": [r.to_dict() for r in results],
            "latency_ms": round(latency_ms, 2),
        }

    except Exception as exc:
        log_error(ErrorDomain.SEARCH, str(exc), exc=exc)
        raise HTTPException(status_code=500, detail=f"Search failed: {str(exc)}")


# ============================================================================
# DOCTRINE ENDPOINTS
# ============================================================================

@app.get("/doctrines")
async def list_doctrines() -> Dict[str, Any]:
    """List all available doctrines."""
    return {
        "total": get_doctrine_count(),
        "categories": get_all_categories(),
        "doctrines": {
            key: {
                "topic": d.topic,
                "category": d.category.value,
                "risk_severity": d.risk_severity.value,
                "confidence": d.confidence_level.value,
                "keywords_count": len(d.keywords),
                "authority_weight": d.get_authority_weight(),
                "precedent": d.get_precedent_anchor(),
            }
            for key, d in DOCTRINE_CACHE.items()
        },
    }


@app.get("/doctrines/{key}")
async def get_doctrine_detail(key: str) -> Dict[str, Any]:
    """Get detailed doctrine by key."""
    doctrine = get_doctrine(key)
    if not doctrine:
        raise HTTPException(status_code=404, detail=f"Doctrine '{key}' not found")

    interactions = get_interaction_edges_for(key)

    return {
        "key": key,
        "topic": doctrine.topic,
        "category": doctrine.category.value,
        "keywords": doctrine.keywords,
        "conclusion_template": doctrine.conclusion_template,
        "reasoning_framework": doctrine.reasoning_framework,
        "key_factors": doctrine.key_factors,
        "primary_authority": doctrine.primary_authority,
        "risk_severity": doctrine.risk_severity.value,
        "risk_factors": doctrine.risk_factors,
        "mitigation_strategies": doctrine.mitigation_strategies,
        "negotiation_guidance": doctrine.negotiation_guidance,
        "common_pitfalls": doctrine.common_pitfalls,
        "best_practices": doctrine.best_practices,
        "confidence_level": doctrine.confidence_level.value,
        "controlling_precedent": {
            "case_name": doctrine.controlling_precedent.case_name,
            "citation": doctrine.controlling_precedent.citation,
            "court": doctrine.controlling_precedent.court,
            "holding": doctrine.controlling_precedent.holding,
        } if doctrine.controlling_precedent else None,
        "jurisdictional_notes": doctrine.jurisdictional_notes,
        "related_doctrines": doctrine.related_doctrines,
        "interactions": [
            {
                "source": i.source_topic,
                "target": i.target_topic,
                "type": i.interaction_type,
                "description": i.description,
            }
            for i in interactions
        ],
        "authority_weight": doctrine.get_authority_weight(),
    }


# ============================================================================
# TELEMETRY ENDPOINTS
# ============================================================================

@app.get("/telemetry")
async def get_telemetry_stats() -> Dict[str, Any]:
    """Get telemetry statistics."""
    telemetry = get_telemetry()
    perf = telemetry.get_performance_snapshot()
    return perf.to_dict()


@app.get("/telemetry/errors")
async def get_recent_errors() -> Dict[str, Any]:
    """Get recent errors."""
    telemetry = get_telemetry()
    errors = telemetry.get_recent_errors(20)
    return {"total": len(errors), "errors": errors}


# ============================================================================
# VERSION AND INFO
# ============================================================================

@app.get("/")
async def root() -> Dict[str, Any]:
    """Engine information endpoint."""
    return {
        "engine": ENGINE_NAME,
        "engine_id": ENGINE_ID,
        "version": ENGINE_VERSION,
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "port": ENGINE_PORT,
        "priority": 90,
        "status": "operational",
        "doctrines": get_doctrine_count(),
        "endpoints": [
            "/health",
            "/analyze",
            "/extract-clauses",
            "/assess-risk",
            "/check-compliance",
            "/compare",
            "/track-obligations",
            "/search",
            "/doctrines",
            "/doctrines/{key}",
            "/telemetry",
            "/telemetry/errors",
        ],
        "architecture": {
            "layer_1": "Doctrine Cache (0-200ms)",
            "layer_2": "Semantic Retrieval (200-700ms)",
            "layer_3": "Deep Analysis (on-demand)",
        },
        "author": "ECHO OMEGA PRIME",
        "authority": "11.0 SOVEREIGN",
    }


# ============================================================================
# CONTRACT HEALTH SCORE ENGINE
# ============================================================================

class ContractHealthDimension(BaseModel):
    """Single dimension of contract health scoring."""
    dimension: str
    score: float
    max_score: float
    weight: float
    findings: List[str]
    recommendations: List[str]


class ContractHealthScore(BaseModel):
    """Comprehensive contract health score."""
    health_id: str
    contract_id: Optional[str]
    overall_score: float
    overall_grade: str
    dimensions: List[ContractHealthDimension]
    critical_gaps: List[str]
    strengths: List[str]
    improvement_priorities: List[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str
    version: str = ENGINE_VERSION


class ContractHealthRequest(BaseModel):
    """Request for contract health scoring."""
    contract_text: str = Field(..., min_length=100, description="Full contract text")
    contract_type: Optional[ContractType] = Field(default=None, description="Contract type")
    contract_id: Optional[str] = Field(default=None, description="Contract identifier")
    jurisdiction: str = Field(default="US", description="Jurisdiction")


def compute_contract_health(
    clauses: List[ClauseAnalysis],
    contract_type: Optional[str] = None,
    jurisdiction: str = "US",
) -> Tuple[float, str, List[ContractHealthDimension], List[str], List[str], List[str]]:
    """Compute comprehensive contract health score across multiple dimensions.

    Dimensions:
        1. Completeness: Are all standard clauses present?
        2. Risk Balance: Are risk allocation provisions adequate?
        3. Enforceability: Are clauses well-drafted for enforcement?
        4. Compliance Readiness: Does the contract meet regulatory requirements?
        5. Negotiation Quality: Does the contract reflect balanced negotiation?
        6. Operational Clarity: Are obligations and timelines clear?
        7. Termination Protection: Are exit provisions adequate?
        8. IP Protection: Are IP rights properly addressed?

    Args:
        clauses: Extracted clause analyses.
        contract_type: Type of contract.
        jurisdiction: Applicable jurisdiction.

    Returns:
        Tuple of (overall_score, grade, dimensions, gaps, strengths, priorities).
    """
    dimensions: List[ContractHealthDimension] = []
    critical_gaps: List[str] = []
    strengths: List[str] = []
    priorities: List[str] = []

    found_types = {c.clause_type for c in clauses}

    # 1. COMPLETENESS DIMENSION
    standard_required = {
        "indemnification", "limitation_of_liability", "confidentiality",
        "termination", "governing_law", "representations_warranties",
        "assignment", "payment_terms", "notices", "entire_agreement",
    }
    type_specific: Dict[str, set] = {
        "saas_agreement": {"service_level", "data_protection", "auto_renewal"},
        "employment_agreement": {"non_compete", "intellectual_property"},
        "construction_contract": {"scope_of_work", "insurance"},
        "oil_gas_lease": {"scope_of_work"},
        "merger_agreement": {"representations_warranties"},
    }
    required = standard_required.copy()
    if contract_type and contract_type in type_specific:
        required |= type_specific[contract_type]

    present = found_types & required
    completeness_score = len(present) / max(1, len(required))
    missing = required - found_types
    completeness_findings: List[str] = []
    completeness_recs: List[str] = []
    if missing:
        for m in sorted(missing):
            completeness_findings.append(f"Missing: {m.replace('_', ' ').title()}")
            completeness_recs.append(f"Add {m.replace('_', ' ').title()} clause")
            critical_gaps.append(f"Missing standard clause: {m.replace('_', ' ').title()}")
    if completeness_score >= 0.9:
        strengths.append("High clause completeness — all standard provisions present")

    dimensions.append(ContractHealthDimension(
        dimension="Completeness",
        score=round(completeness_score * 100, 1),
        max_score=100.0,
        weight=0.20,
        findings=completeness_findings,
        recommendations=completeness_recs,
    ))

    # 2. RISK BALANCE DIMENSION
    risk_clauses = [c for c in clauses if c.clause_category == "financial"]
    high_risk_count = sum(1 for c in clauses if c.risk_level in (RiskLevel.CRITICAL, RiskLevel.HIGH))
    low_risk_count = sum(1 for c in clauses if c.risk_level in (RiskLevel.LOW, RiskLevel.NEGLIGIBLE))
    total_clauses = max(1, len(clauses))
    risk_ratio = 1.0 - (high_risk_count / total_clauses)
    risk_findings: List[str] = []
    risk_recs: List[str] = []
    if high_risk_count > 0:
        risk_findings.append(f"{high_risk_count} high/critical risk clauses detected")
        risk_recs.append("Review and negotiate high-risk provisions")
        priorities.append(f"Address {high_risk_count} high-risk clauses")
    has_lol = "limitation_of_liability" in found_types
    has_indem = "indemnification" in found_types
    has_cons = any("consequential" in (c.clause_text or "").lower() for c in clauses)
    if has_lol and has_indem:
        strengths.append("Core risk allocation framework present (LOL + Indemnification)")
        risk_ratio = min(1.0, risk_ratio + 0.1)
    if not has_lol:
        risk_findings.append("No limitation of liability clause")
        risk_recs.append("Add limitation of liability provision")
        critical_gaps.append("No liability cap — unlimited exposure")

    dimensions.append(ContractHealthDimension(
        dimension="Risk Balance",
        score=round(risk_ratio * 100, 1),
        max_score=100.0,
        weight=0.20,
        findings=risk_findings,
        recommendations=risk_recs,
    ))

    # 3. ENFORCEABILITY DIMENSION
    boilerplate_clauses = [c for c in clauses if c.is_boilerplate]
    custom_clauses = [c for c in clauses if not c.is_boilerplate]
    enforce_score = 0.6
    enforce_findings: List[str] = []
    enforce_recs: List[str] = []

    has_governing = "governing_law" in found_types
    has_dispute = "dispute_resolution" in found_types
    has_entire = "entire_agreement" in found_types
    has_sev = "severability" in found_types

    if has_governing:
        enforce_score += 0.1
    else:
        enforce_findings.append("No governing law clause")
        enforce_recs.append("Add governing law provision")
    if has_dispute:
        enforce_score += 0.1
    else:
        enforce_findings.append("No dispute resolution mechanism")
        enforce_recs.append("Add dispute resolution clause")
    if has_entire:
        enforce_score += 0.05
    if has_sev:
        enforce_score += 0.05

    for c in clauses:
        if c.missing_provisions:
            enforce_score -= 0.02 * len(c.missing_provisions)

    enforce_score = max(0.0, min(1.0, enforce_score))

    if enforce_score >= 0.8:
        strengths.append("Strong enforceability framework with governing law and dispute resolution")

    dimensions.append(ContractHealthDimension(
        dimension="Enforceability",
        score=round(enforce_score * 100, 1),
        max_score=100.0,
        weight=0.15,
        findings=enforce_findings,
        recommendations=enforce_recs,
    ))

    # 4. COMPLIANCE READINESS DIMENSION
    compliance_score = 0.5
    compliance_findings: List[str] = []
    compliance_recs: List[str] = []

    has_dp = "data_protection" in found_types
    has_compliance = any("compliance" in (c.clause_text or "").lower() for c in clauses)
    has_insurance = "insurance" in found_types

    if has_dp:
        compliance_score += 0.2
        strengths.append("Data protection provisions present")
    else:
        compliance_findings.append("No data protection provisions")
        compliance_recs.append("Add GDPR/CCPA-compliant data protection provisions")

    if has_compliance:
        compliance_score += 0.15
    if has_insurance:
        compliance_score += 0.1

    compliance_score = max(0.0, min(1.0, compliance_score))

    dimensions.append(ContractHealthDimension(
        dimension="Compliance Readiness",
        score=round(compliance_score * 100, 1),
        max_score=100.0,
        weight=0.15,
        findings=compliance_findings,
        recommendations=compliance_recs,
    ))

    # 5. NEGOTIATION QUALITY DIMENSION
    mutual_count = sum(1 for c in clauses if any("mutual" in p.lower() for p in c.key_provisions))
    balanced_score = 0.5 + (0.05 * mutual_count)
    custom_ratio = len(custom_clauses) / max(1, len(clauses))
    balanced_score += custom_ratio * 0.2
    negotiation_findings: List[str] = []
    negotiation_recs: List[str] = []

    if custom_ratio > 0.5:
        strengths.append("Well-negotiated contract with customized provisions")
    else:
        negotiation_findings.append("High proportion of boilerplate — may indicate form contract")
        negotiation_recs.append("Review boilerplate provisions for adequacy to this transaction")

    balanced_score = max(0.0, min(1.0, balanced_score))

    dimensions.append(ContractHealthDimension(
        dimension="Negotiation Quality",
        score=round(balanced_score * 100, 1),
        max_score=100.0,
        weight=0.10,
        findings=negotiation_findings,
        recommendations=negotiation_recs,
    ))

    # 6. OPERATIONAL CLARITY DIMENSION
    clarity_score = 0.5
    clarity_findings: List[str] = []
    clarity_recs: List[str] = []
    has_scope = "scope_of_work" in found_types
    has_payment = "payment_terms" in found_types
    has_sla = "service_level" in found_types
    has_notices = "notices" in found_types

    if has_scope:
        clarity_score += 0.15
    else:
        clarity_findings.append("No scope of work provisions")
        clarity_recs.append("Add detailed scope of work with acceptance criteria")
    if has_payment:
        clarity_score += 0.1
    if has_sla:
        clarity_score += 0.1
    if has_notices:
        clarity_score += 0.05

    time_clauses = sum(1 for c in clauses if any("time" in p.lower() for p in c.key_provisions))
    clarity_score += min(0.1, time_clauses * 0.02)
    clarity_score = max(0.0, min(1.0, clarity_score))

    dimensions.append(ContractHealthDimension(
        dimension="Operational Clarity",
        score=round(clarity_score * 100, 1),
        max_score=100.0,
        weight=0.10,
        findings=clarity_findings,
        recommendations=clarity_recs,
    ))

    # 7. TERMINATION PROTECTION DIMENSION
    term_score = 0.3
    term_findings: List[str] = []
    term_recs: List[str] = []
    has_term = "termination" in found_types
    has_renewal = "auto_renewal" in found_types

    if has_term:
        term_score += 0.3
        term_clause = next((c for c in clauses if c.clause_type == "termination"), None)
        if term_clause:
            if "cure period" in [p.lower() for p in term_clause.key_provisions]:
                term_score += 0.1
            if "survival provision" in [p.lower() for p in term_clause.key_provisions]:
                term_score += 0.1
            if term_clause.missing_provisions:
                for mp in term_clause.missing_provisions:
                    term_findings.append(f"Termination clause missing: {mp}")
    else:
        term_findings.append("No termination provisions")
        term_recs.append("Add termination for cause and convenience provisions")
        critical_gaps.append("No termination clause — no exit mechanism")

    term_score = max(0.0, min(1.0, term_score))

    dimensions.append(ContractHealthDimension(
        dimension="Termination Protection",
        score=round(term_score * 100, 1),
        max_score=100.0,
        weight=0.05,
        findings=term_findings,
        recommendations=term_recs,
    ))

    # 8. IP PROTECTION DIMENSION
    ip_score = 0.3
    ip_findings: List[str] = []
    ip_recs: List[str] = []
    has_ip = "intellectual_property" in found_types
    has_conf = "confidentiality" in found_types

    if has_ip:
        ip_score += 0.3
        strengths.append("IP ownership provisions present")
    else:
        ip_findings.append("No IP ownership provisions")
        ip_recs.append("Add IP ownership and assignment provisions")
    if has_conf:
        ip_score += 0.2
    else:
        ip_findings.append("No confidentiality provisions")
        ip_recs.append("Add confidentiality/NDA provisions")

    ip_score = max(0.0, min(1.0, ip_score))

    dimensions.append(ContractHealthDimension(
        dimension="IP Protection",
        score=round(ip_score * 100, 1),
        max_score=100.0,
        weight=0.05,
        findings=ip_findings,
        recommendations=ip_recs,
    ))

    # OVERALL SCORE
    overall = sum(d.score * d.weight for d in dimensions) / 100.0 * 100
    overall = round(max(0.0, min(100.0, overall)), 1)

    if overall >= 85:
        grade = "A"
    elif overall >= 75:
        grade = "B"
    elif overall >= 65:
        grade = "C"
    elif overall >= 50:
        grade = "D"
    else:
        grade = "F"

    return overall, grade, dimensions, critical_gaps, strengths, priorities


@app.post("/health-score", response_model=ContractHealthScore)
async def contract_health_score(request: ContractHealthRequest) -> ContractHealthScore:
    """Compute comprehensive contract health score."""
    start = time.time()

    try:
        clauses = extract_clauses_from_text(
            text=request.contract_text,
            contract_type=request.contract_type.value if request.contract_type else None,
            include_risk=True,
            include_boilerplate=True,
        )

        overall, grade, dimensions, gaps, strengths, priorities = compute_contract_health(
            clauses=clauses,
            contract_type=request.contract_type.value if request.contract_type else None,
            jurisdiction=request.jurisdiction,
        )

        hash_input = f"{overall}|{grade}|{len(dimensions)}|{len(gaps)}"
        determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()

        latency_ms = (time.time() - start) * 1000

        return ContractHealthScore(
            health_id=str(uuid.uuid4()),
            contract_id=request.contract_id,
            overall_score=overall,
            overall_grade=grade,
            dimensions=dimensions,
            critical_gaps=gaps,
            strengths=strengths,
            improvement_priorities=priorities,
            determinism_hash=determinism_hash,
            latency_ms=round(latency_ms, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    except Exception as exc:
        log_error(ErrorDomain.DOCTRINE_ENGINE, str(exc), exc=exc)
        raise HTTPException(status_code=500, detail=f"Health score computation failed: {str(exc)}")


# ============================================================================
# BATCH ANALYSIS ENDPOINT
# ============================================================================

class BatchClauseRequest(BaseModel):
    """Request for batch clause analysis across multiple contracts."""
    contracts: List[Dict[str, str]] = Field(
        ..., description="List of {contract_id, text} objects",
        min_length=1,
        max_length=20,
    )
    focus_clauses: Optional[List[str]] = Field(default=None, description="Clause types to focus on")


@app.post("/batch-analyze")
async def batch_analyze(request: BatchClauseRequest) -> Dict[str, Any]:
    """Batch analysis of multiple contracts."""
    start = time.time()

    results: List[Dict[str, Any]] = []
    total_clauses = 0
    total_risks = 0

    for contract in request.contracts:
        contract_id = contract.get("contract_id", str(uuid.uuid4())[:8])
        text = contract.get("text", "")

        if len(text) < 50:
            results.append({
                "contract_id": contract_id,
                "status": "skipped",
                "reason": "Text too short (minimum 50 characters)",
            })
            continue

        try:
            clauses = extract_clauses_from_text(
                text=text,
                focus_clauses=request.focus_clauses,
                include_risk=True,
                include_boilerplate=True,
            )

            risk_count = sum(1 for c in clauses if c.risk_level in (RiskLevel.CRITICAL, RiskLevel.HIGH))
            total_clauses += len(clauses)
            total_risks += risk_count

            results.append({
                "contract_id": contract_id,
                "status": "analyzed",
                "total_clauses": len(clauses),
                "high_risk_clauses": risk_count,
                "clause_types": sorted({c.clause_type for c in clauses}),
                "overall_risk": "high" if risk_count > 2 else "medium" if risk_count > 0 else "low",
            })

        except Exception as exc:
            results.append({
                "contract_id": contract_id,
                "status": "error",
                "error": str(exc)[:200],
            })

    latency_ms = (time.time() - start) * 1000

    return {
        "batch_id": str(uuid.uuid4()),
        "total_contracts": len(request.contracts),
        "analyzed": sum(1 for r in results if r["status"] == "analyzed"),
        "skipped": sum(1 for r in results if r["status"] == "skipped"),
        "errors": sum(1 for r in results if r["status"] == "error"),
        "total_clauses_extracted": total_clauses,
        "total_high_risk_clauses": total_risks,
        "results": results,
        "latency_ms": round(latency_ms, 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# CLAUSE TEMPLATE LIBRARY
# ============================================================================

_CLAUSE_TEMPLATES: Dict[str, Dict[str, str]] = {
    "indemnification_mutual": {
        "name": "Mutual Indemnification (Balanced)",
        "template": """Each party (the "Indemnifying Party") shall defend, indemnify, and hold harmless
the other party and its officers, directors, employees, agents, successors, and assigns
(collectively, the "Indemnified Party") from and against any and all third-party claims,
damages, losses, liabilities, costs, and expenses (including reasonable attorneys' fees)
arising out of or resulting from: (a) the Indemnifying Party's breach of any representation,
warranty, or obligation under this Agreement; (b) the Indemnifying Party's negligence or
willful misconduct; or (c) the Indemnifying Party's violation of applicable law.

The Indemnified Party shall: (i) provide prompt written notice of any claim for which
indemnification is sought; (ii) grant the Indemnifying Party sole control over the defense
and settlement of such claim (provided that settlement does not impose obligations on the
Indemnified Party without its consent); and (iii) provide reasonable cooperation at the
Indemnifying Party's expense.

The indemnification obligations under this Section are subject to the limitation of liability
set forth in Section [X] and shall survive termination or expiration of this Agreement for
a period of [3] years.""",
        "risk_level": "low",
        "clause_type": "indemnification",
    },
    "limitation_of_liability_standard": {
        "name": "Limitation of Liability (Standard Commercial)",
        "template": """LIMITATION OF LIABILITY. EXCEPT FOR (A) A PARTY'S INDEMNIFICATION
OBLIGATIONS UNDER SECTION [X], (B) A PARTY'S BREACH OF ITS CONFIDENTIALITY OBLIGATIONS
UNDER SECTION [X], (C) INFRINGEMENT OR MISAPPROPRIATION OF THE OTHER PARTY'S INTELLECTUAL
PROPERTY RIGHTS, AND (D) A PARTY'S FRAUD OR WILLFUL MISCONDUCT:

(i) IN NO EVENT SHALL EITHER PARTY BE LIABLE TO THE OTHER PARTY FOR ANY INDIRECT,
INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT NOT LIMITED TO
LOSS OF PROFITS, LOSS OF REVENUE, LOSS OF DATA, OR LOSS OF BUSINESS OPPORTUNITY, HOWEVER
CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY; AND

(ii) EACH PARTY'S TOTAL AGGREGATE LIABILITY ARISING OUT OF OR RELATED TO THIS AGREEMENT
SHALL NOT EXCEED THE GREATER OF (A) THE TOTAL AMOUNTS PAID OR PAYABLE BY [CUSTOMER]
UNDER THIS AGREEMENT DURING THE TWELVE (12) MONTH PERIOD PRECEDING THE EVENT GIVING
RISE TO THE CLAIM, OR (B) [$X].

THE FOREGOING LIMITATIONS SHALL APPLY EVEN IF A PARTY HAS BEEN ADVISED OF THE POSSIBILITY
OF SUCH DAMAGES AND REGARDLESS OF WHETHER ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.""",
        "risk_level": "medium",
        "clause_type": "limitation_of_liability",
    },
    "force_majeure_modern": {
        "name": "Force Majeure (Post-COVID Modern)",
        "template": """Neither party shall be liable for any failure or delay in performing its
obligations under this Agreement (other than payment obligations) where such failure or
delay results from a Force Majeure Event. A "Force Majeure Event" means any event beyond
the reasonable control of the affected party, including but not limited to: (a) natural
disasters, including earthquakes, floods, hurricanes, and severe weather events;
(b) epidemics, pandemics, or public health emergencies, including quarantine or isolation
orders; (c) acts of war, armed conflict, terrorism, or civil unrest; (d) government
actions, embargoes, sanctions, or trade restrictions; (e) cyber attacks, ransomware, or
widespread technology failures; (f) labor disputes, strikes, or lockouts (other than those
involving the affected party's own employees); (g) supply chain disruptions affecting
essential materials or services; and (h) failure of essential utility services.

The affected party shall: (i) provide prompt written notice to the other party describing
the Force Majeure Event and its expected duration; (ii) use commercially reasonable efforts
to mitigate the impact of the Force Majeure Event and resume performance; (iii) provide
regular updates on the status of the Force Majeure Event; and (iv) resume full performance
promptly when the Force Majeure Event subsides.

If a Force Majeure Event continues for more than [90/180] consecutive days, either party
may terminate this Agreement upon [30] days' written notice, without liability for such
termination other than payment for services performed prior to the termination date.""",
        "risk_level": "low",
        "clause_type": "force_majeure",
    },
    "confidentiality_standard": {
        "name": "Confidentiality (Standard Mutual)",
        "template": """Each party (the "Receiving Party") acknowledges that, in connection with this
Agreement, it may receive Confidential Information of the other party (the "Disclosing Party").
"Confidential Information" means all non-public information, whether disclosed orally, in
writing, or by any other means, that is designated as confidential or that a reasonable
person would understand to be confidential given the nature of the information and
circumstances of disclosure, including: business plans, financial data, customer lists,
pricing information, technical data, trade secrets, and proprietary software.

Confidential Information does not include information that: (a) is or becomes publicly
available without breach of this Agreement; (b) was known to the Receiving Party prior to
disclosure, as documented by the Receiving Party's records; (c) is independently developed
by the Receiving Party without use of the Disclosing Party's Confidential Information; or
(d) is lawfully received from a third party without restriction on disclosure.

The Receiving Party shall: (i) use Confidential Information solely for the purposes of this
Agreement; (ii) protect Confidential Information with at least the same degree of care used
to protect its own confidential information, but no less than reasonable care; (iii) limit
access to Confidential Information to employees, agents, and advisors who have a need to
know and are bound by confidentiality obligations at least as protective as this Section;
and (iv) not disclose Confidential Information to any third party without the Disclosing
Party's prior written consent.

The Receiving Party may disclose Confidential Information if required by law or court order,
provided that the Receiving Party: (a) gives the Disclosing Party prompt written notice
(to the extent legally permitted); and (b) cooperates with the Disclosing Party's efforts
to obtain a protective order.

Upon termination or expiration of this Agreement, the Receiving Party shall promptly return
or destroy all Confidential Information and certify such return or destruction in writing.

The obligations under this Section shall survive for [5] years after termination or
expiration of this Agreement; provided that obligations with respect to trade secrets shall
survive for as long as such information remains a trade secret under applicable law.""",
        "risk_level": "low",
        "clause_type": "confidentiality",
    },
    "governing_law_us": {
        "name": "Governing Law (US - Standard)",
        "template": """This Agreement shall be governed by and construed in accordance with the laws
of the State of [STATE], without regard to its conflict of laws principles. The United
Nations Convention on Contracts for the International Sale of Goods (CISG) shall not apply
to this Agreement.

Any dispute arising out of or related to this Agreement that cannot be resolved through
good-faith negotiation within [30] days shall be submitted to binding arbitration
administered by [AAA/JAMS] in accordance with its Commercial Arbitration Rules. The
arbitration shall be conducted in [CITY, STATE] before [one/three] arbitrator(s). The
arbitrator(s) shall have no authority to award punitive damages. The decision of the
arbitrator(s) shall be final and binding, and judgment on the award may be entered in any
court of competent jurisdiction.

Notwithstanding the foregoing, either party may seek injunctive or other equitable relief
in any court of competent jurisdiction to protect its intellectual property rights or
Confidential Information without being required to post bond or prove actual damages.

EACH PARTY HEREBY IRREVOCABLY WAIVES ANY RIGHT TO A JURY TRIAL IN CONNECTION WITH ANY
LEGAL PROCEEDING ARISING OUT OF OR RELATED TO THIS AGREEMENT.

The prevailing party in any dispute arising under this Agreement shall be entitled to
recover its reasonable attorneys' fees and costs from the non-prevailing party.""",
        "risk_level": "low",
        "clause_type": "governing_law",
    },
}


@app.get("/templates")
async def list_clause_templates() -> Dict[str, Any]:
    """List all available clause templates."""
    return {
        "total": len(_CLAUSE_TEMPLATES),
        "templates": {
            key: {
                "name": tmpl["name"],
                "clause_type": tmpl["clause_type"],
                "risk_level": tmpl["risk_level"],
                "length": len(tmpl["template"]),
            }
            for key, tmpl in _CLAUSE_TEMPLATES.items()
        },
    }


@app.get("/templates/{key}")
async def get_clause_template(key: str) -> Dict[str, Any]:
    """Get a specific clause template."""
    if key not in _CLAUSE_TEMPLATES:
        raise HTTPException(status_code=404, detail=f"Template '{key}' not found")
    tmpl = _CLAUSE_TEMPLATES[key]
    return {
        "key": key,
        "name": tmpl["name"],
        "clause_type": tmpl["clause_type"],
        "risk_level": tmpl["risk_level"],
        "template": tmpl["template"],
    }


# ============================================================================
# SEMANTIC MAP INFO ENDPOINT
# ============================================================================

@app.get("/semantic-map")
async def semantic_map_info() -> Dict[str, Any]:
    """Get semantic map metadata and statistics."""
    return get_map_metadata()


# ============================================================================
# CONTRACT REDLINING ENGINE
# ============================================================================

class RedlineChange(BaseModel):
    """A single redline change recommendation."""
    clause_type: str
    original_text: str
    suggested_text: str
    reason: str
    risk_reduction: str
    priority: str  # "critical", "high", "medium", "low"
    category: str  # "protective", "clarifying", "strengthening", "balanced"


class RedlineReport(BaseModel):
    """Full redline analysis report."""
    contract_id: str
    total_changes: int
    critical_changes: int
    high_changes: int
    medium_changes: int
    low_changes: int
    changes: List[RedlineChange]
    overall_improvement_score: float
    analysis_timestamp: str
    determinism_hash: str


# Redline pattern library - maps risk indicators to suggested improvements
_REDLINE_PATTERNS: Dict[str, Dict[str, Any]] = {
    "unlimited_liability": {
        "triggers": [
            "unlimited liability",
            "all damages",
            "any and all losses",
            "without limitation",
            "no cap on",
            "unlimited damages",
        ],
        "clause_type": "limitation_of_liability",
        "suggested_approach": "Cap liability at contract value or 12 months of fees",
        "risk_reduction": "Reduces exposure from unlimited to bounded financial risk",
        "priority": "critical",
        "category": "protective",
        "replacement_template": (
            "The aggregate liability of either party under this Agreement shall not exceed "
            "the total fees paid or payable during the twelve (12) month period immediately "
            "preceding the event giving rise to the claim, except for breaches of "
            "confidentiality obligations, indemnification obligations, and willful misconduct."
        ),
    },
    "unilateral_termination": {
        "triggers": [
            "may terminate at any time",
            "sole discretion to terminate",
            "terminate without cause immediately",
            "terminate without notice",
            "terminate for any reason",
        ],
        "clause_type": "termination",
        "suggested_approach": "Add mutual termination rights with reasonable notice period",
        "risk_reduction": "Prevents surprise termination without preparation time",
        "priority": "critical",
        "category": "balanced",
        "replacement_template": (
            "Either party may terminate this Agreement without cause upon sixty (60) days' "
            "prior written notice to the other party. Upon termination without cause, the "
            "terminating party shall pay for all services rendered and expenses incurred "
            "through the effective date of termination."
        ),
    },
    "broad_indemnification": {
        "triggers": [
            "indemnify and hold harmless from any and all",
            "defend indemnify hold harmless from all claims",
            "full indemnification",
            "indemnify against all losses damages costs",
            "unlimited indemnification",
        ],
        "clause_type": "indemnification",
        "suggested_approach": "Limit indemnification to specific, enumerated scenarios",
        "risk_reduction": "Narrows indemnification scope to manageable, insurable risks",
        "priority": "high",
        "category": "protective",
        "replacement_template": (
            "Each party (the 'Indemnifying Party') shall indemnify, defend, and hold harmless "
            "the other party from and against third-party claims, damages, and reasonable "
            "attorneys' fees arising from: (a) the Indemnifying Party's material breach of "
            "this Agreement; (b) the Indemnifying Party's gross negligence or willful "
            "misconduct; or (c) the Indemnifying Party's violation of applicable law. "
            "The Indemnifying Party's liability under this Section shall be subject to the "
            "limitation of liability provisions set forth herein."
        ),
    },
    "no_ip_ownership": {
        "triggers": [
            "all work product belongs to",
            "all intellectual property shall be owned by",
            "exclusive ownership of all",
            "all rights title and interest",
            "work made for hire",
        ],
        "clause_type": "intellectual_property",
        "suggested_approach": "Distinguish pre-existing IP from new work product",
        "risk_reduction": "Protects pre-existing IP while granting appropriate rights to new work",
        "priority": "high",
        "category": "balanced",
        "replacement_template": (
            "Work Product: All deliverables created specifically for Client under this Agreement "
            "('Work Product') shall be owned by Client upon full payment. Pre-Existing IP: "
            "Each party retains ownership of its pre-existing intellectual property. To the "
            "extent any Pre-Existing IP of Provider is incorporated into Work Product, Provider "
            "grants Client a perpetual, non-exclusive, royalty-free license to use such "
            "Pre-Existing IP solely as part of the Work Product."
        ),
    },
    "no_force_majeure": {
        "triggers": [
            "no excuse for non-performance",
            "regardless of circumstances",
            "no exceptions to performance",
            "without regard to external events",
        ],
        "clause_type": "force_majeure",
        "suggested_approach": "Add comprehensive force majeure clause",
        "risk_reduction": "Provides protection against unforeseeable events beyond party control",
        "priority": "high",
        "category": "protective",
        "replacement_template": (
            "Neither party shall be liable for any delay or failure to perform its obligations "
            "under this Agreement to the extent such delay or failure results from circumstances "
            "beyond the reasonable control of the affected party, including but not limited to: "
            "acts of God, natural disasters, epidemic or pandemic, war, terrorism, government "
            "actions, labor disputes, power failures, internet or telecommunications failures, "
            "or cyberattacks. The affected party shall provide prompt written notice and use "
            "commercially reasonable efforts to mitigate the impact. If the force majeure "
            "event continues for more than ninety (90) days, either party may terminate the "
            "affected obligations upon thirty (30) days' written notice."
        ),
    },
    "waiver_of_jury_trial": {
        "triggers": [
            "waive right to jury trial",
            "waives jury trial",
            "no jury trial",
            "bench trial only",
        ],
        "clause_type": "dispute_resolution",
        "suggested_approach": "Replace with arbitration clause or keep jury trial right",
        "risk_reduction": "Preserves dispute resolution flexibility",
        "priority": "medium",
        "category": "balanced",
        "replacement_template": (
            "Any dispute arising out of or relating to this Agreement shall first be submitted "
            "to mediation in accordance with the rules of JAMS. If mediation is unsuccessful "
            "within sixty (60) days, either party may initiate binding arbitration under the "
            "rules of the American Arbitration Association. The arbitration shall be conducted "
            "by a single arbitrator in the city where the non-filing party is headquartered. "
            "The arbitrator's decision shall be final and binding."
        ),
    },
    "automatic_renewal_trap": {
        "triggers": [
            "automatically renew",
            "auto-renew",
            "shall renew unless",
            "deemed renewed",
            "continuous renewal",
        ],
        "clause_type": "renewal",
        "suggested_approach": "Add clear opt-out window and renewal notice requirement",
        "risk_reduction": "Prevents involuntary contract extension",
        "priority": "medium",
        "category": "clarifying",
        "replacement_template": (
            "This Agreement shall automatically renew for successive one (1) year terms unless "
            "either party provides written notice of non-renewal at least ninety (90) days "
            "prior to the expiration of the then-current term. The renewing party shall provide "
            "a renewal notice no later than one hundred twenty (120) days before expiration, "
            "including any proposed changes to pricing or terms. Pricing adjustments upon "
            "renewal shall not exceed the greater of five percent (5%) or the Consumer Price "
            "Index increase for the preceding twelve (12) month period."
        ),
    },
    "missing_data_protection": {
        "triggers": [
            "no obligation to protect data",
            "data provided as-is",
            "no data security",
            "no confidentiality for data",
        ],
        "clause_type": "data_protection",
        "suggested_approach": "Add minimum data protection standards",
        "risk_reduction": "Ensures minimum security for shared data",
        "priority": "critical",
        "category": "strengthening",
        "replacement_template": (
            "Each party shall implement and maintain commercially reasonable administrative, "
            "technical, and physical safeguards to protect the other party's Confidential "
            "Information and any personal data processed under this Agreement. Such safeguards "
            "shall include, at minimum: (a) encryption of data in transit and at rest; "
            "(b) access controls limiting data access to authorized personnel; (c) regular "
            "security assessments; (d) incident response procedures with notification within "
            "72 hours of discovery of a security breach. Each party shall comply with all "
            "applicable data protection laws, including GDPR and CCPA where applicable."
        ),
    },
    "vague_scope": {
        "triggers": [
            "and other services as needed",
            "including but not limited to any",
            "and all related activities",
            "such other tasks as may be required",
            "any additional work as requested",
        ],
        "clause_type": "scope_of_work",
        "suggested_approach": "Define specific scope with change order process",
        "risk_reduction": "Prevents scope creep and undefined obligations",
        "priority": "high",
        "category": "clarifying",
        "replacement_template": (
            "The scope of services is limited to those expressly described in Exhibit A "
            "('Statement of Work'). Any services not specifically included in the Statement "
            "of Work shall be considered out-of-scope. Additional services may be added only "
            "through a written Change Order signed by authorized representatives of both "
            "parties. Each Change Order shall specify: (a) description of additional services; "
            "(b) timeline for delivery; (c) additional fees, if any; and (d) impact on "
            "existing deliverables and timelines."
        ),
    },
    "no_warranty_period": {
        "triggers": [
            "no warranty",
            "as-is",
            "without warranty of any kind",
            "all warranties disclaimed",
            "no guarantees",
        ],
        "clause_type": "warranty",
        "suggested_approach": "Add reasonable warranty period with specific remedies",
        "risk_reduction": "Ensures minimum quality standards and recourse for defects",
        "priority": "medium",
        "category": "strengthening",
        "replacement_template": (
            "Provider warrants that: (a) services shall be performed in a professional and "
            "workmanlike manner consistent with generally accepted industry standards; "
            "(b) deliverables shall materially conform to the specifications set forth in the "
            "Statement of Work for a period of ninety (90) days following acceptance "
            "('Warranty Period'); and (c) Provider has the right and authority to enter into "
            "this Agreement. Client's sole remedy for breach of warranty shall be, at "
            "Provider's option: (i) re-performance of the defective services at no additional "
            "cost; or (ii) a pro-rata refund of fees paid for the defective services."
        ),
    },
    "unilateral_amendment": {
        "triggers": [
            "may modify this agreement at any time",
            "reserves the right to amend",
            "may change terms at its sole discretion",
            "terms subject to change without notice",
        ],
        "clause_type": "amendment",
        "suggested_approach": "Require mutual written consent for amendments",
        "risk_reduction": "Prevents unilateral changes to agreed terms",
        "priority": "critical",
        "category": "protective",
        "replacement_template": (
            "This Agreement may not be amended, modified, or supplemented except by a written "
            "instrument signed by authorized representatives of both parties. No waiver of any "
            "provision of this Agreement shall be effective unless in writing and signed by the "
            "waiving party. A waiver of any provision on one occasion shall not constitute a "
            "waiver of such provision on any other occasion."
        ),
    },
    "non_compete_overbroad": {
        "triggers": [
            "shall not compete anywhere",
            "worldwide non-compete",
            "in perpetuity shall not",
            "permanent restriction",
            "global non-competition",
        ],
        "clause_type": "non_compete",
        "suggested_approach": "Narrow scope, geography, and duration to enforceable limits",
        "risk_reduction": "Makes restriction enforceable while still providing reasonable protection",
        "priority": "high",
        "category": "balanced",
        "replacement_template": (
            "During the term of this Agreement and for a period of twelve (12) months "
            "following termination ('Restricted Period'), the Receiving Party shall not "
            "directly solicit the Disclosing Party's customers who were served during the "
            "last twelve (12) months of the Agreement term, within the geographic areas where "
            "the Disclosing Party actively conducts business. This restriction shall not "
            "prohibit the Receiving Party from: (a) providing services to customers who "
            "independently seek such services; (b) general advertising not targeted at the "
            "Disclosing Party's customers; or (c) performing work in different service areas."
        ),
    },
}


def _generate_redlines(text: str, contract_type: str = "general") -> List[RedlineChange]:
    """Analyze contract text and generate redline recommendations."""
    text_lower = text.lower()
    changes: List[RedlineChange] = []

    for pattern_key, pattern_config in _REDLINE_PATTERNS.items():
        for trigger in pattern_config["triggers"]:
            if trigger.lower() in text_lower:
                # Find the surrounding context (sentence/paragraph containing the trigger)
                trigger_idx = text_lower.find(trigger.lower())
                # Extract a window of context around the trigger
                context_start = max(0, text.rfind(".", 0, trigger_idx) + 1)
                context_end = text.find(".", trigger_idx + len(trigger))
                if context_end == -1:
                    context_end = min(len(text), trigger_idx + 500)
                else:
                    context_end += 1

                original_context = text[context_start:context_end].strip()

                change = RedlineChange(
                    clause_type=pattern_config["clause_type"],
                    original_text=original_context[:500],
                    suggested_text=pattern_config["replacement_template"],
                    reason=pattern_config["suggested_approach"],
                    risk_reduction=pattern_config["risk_reduction"],
                    priority=pattern_config["priority"],
                    category=pattern_config["category"],
                )
                changes.append(change)
                break  # Only one match per pattern group

    # Sort by priority
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    changes.sort(key=lambda c: priority_order.get(c.priority, 99))

    return changes


def _calculate_improvement_score(changes: List[RedlineChange]) -> float:
    """Calculate overall improvement score from redline changes."""
    if not changes:
        return 0.0

    priority_weights = {"critical": 25.0, "high": 15.0, "medium": 8.0, "low": 3.0}
    total_weight = sum(priority_weights.get(c.priority, 1.0) for c in changes)
    max_possible = len(changes) * 25.0  # If all were critical

    # Improvement score represents risk reduction potential
    raw_score = (total_weight / max_possible) * 100.0 if max_possible > 0 else 0.0
    return round(min(raw_score, 100.0), 2)


@app.post("/redline")
async def redline_contract(request: AnalyzeRequest) -> RedlineReport:
    """Generate redline recommendations for a contract.

    Analyzes contract text and produces specific clause-level
    change recommendations with replacement language templates.
    """
    trace_id = trace_query("redline", request.contract_type)
    try:
        normalized = normalize_semantics(request.text)
        changes = _generate_redlines(request.text, request.contract_type)
        improvement_score = _calculate_improvement_score(changes)

        # Count by priority
        priority_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for change in changes:
            priority_counts[change.priority] = priority_counts.get(change.priority, 0) + 1

        # Determinism hash
        hash_input = f"{normalized.normalized_text}|redline|{len(changes)}"
        det_hash = hashlib.sha256(hash_input.encode()).hexdigest()

        report = RedlineReport(
            contract_id=f"RL-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            total_changes=len(changes),
            critical_changes=priority_counts["critical"],
            high_changes=priority_counts["high"],
            medium_changes=priority_counts["medium"],
            low_changes=priority_counts["low"],
            changes=changes,
            overall_improvement_score=improvement_score,
            analysis_timestamp=datetime.utcnow().isoformat() + "Z",
            determinism_hash=det_hash,
        )

        complete_trace(trace_id, True)
        _metrics.record_query(datetime.utcnow().timestamp(), "redline")
        return report

    except Exception as e:
        complete_trace(trace_id, False)
        log_error("redline", str(e), traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PENALTY / DAMAGES CALCULATOR
# ============================================================================

class DamagesInput(BaseModel):
    """Input for damages calculation."""
    contract_value: float
    breach_type: str  # "material", "minor", "anticipatory", "fundamental"
    liability_cap: Optional[float] = None
    consequential_excluded: bool = True
    indemnification_applies: bool = False
    liquidated_damages_rate: Optional[float] = None  # percentage per day/week
    liquidated_damages_period: Optional[str] = "day"  # "day", "week", "month"
    days_in_breach: int = 0
    actual_damages: Optional[float] = None
    mitigation_efforts: bool = True
    jurisdiction: str = "US_GENERAL"


class DamagesEstimate(BaseModel):
    """Estimated damages calculation result."""
    direct_damages: float
    consequential_damages: float
    liquidated_damages: float
    punitive_potential: float
    total_estimated_exposure: float
    liability_cap_applied: bool
    capped_exposure: float
    mitigation_credit: float
    net_exposure: float
    risk_level: str
    calculation_notes: List[str]
    disclaimer: str
    determinism_hash: str


# Breach type multipliers for damage estimation
_BREACH_MULTIPLIERS: Dict[str, Dict[str, float]] = {
    "material": {
        "direct_factor": 0.40,
        "consequential_factor": 0.25,
        "punitive_factor": 0.0,
        "mitigation_credit": 0.15,
    },
    "minor": {
        "direct_factor": 0.10,
        "consequential_factor": 0.05,
        "punitive_factor": 0.0,
        "mitigation_credit": 0.20,
    },
    "anticipatory": {
        "direct_factor": 0.30,
        "consequential_factor": 0.15,
        "punitive_factor": 0.0,
        "mitigation_credit": 0.25,
    },
    "fundamental": {
        "direct_factor": 0.60,
        "consequential_factor": 0.35,
        "punitive_factor": 0.10,
        "mitigation_credit": 0.10,
    },
}


def _calculate_damages(inp: DamagesInput) -> DamagesEstimate:
    """Calculate estimated damages exposure from breach parameters."""
    notes: List[str] = []
    multipliers = _BREACH_MULTIPLIERS.get(inp.breach_type, _BREACH_MULTIPLIERS["material"])

    # Direct damages
    if inp.actual_damages is not None and inp.actual_damages > 0:
        direct = inp.actual_damages
        notes.append(f"Direct damages based on stated actual damages: ${direct:,.2f}")
    else:
        direct = inp.contract_value * multipliers["direct_factor"]
        notes.append(
            f"Direct damages estimated at {multipliers['direct_factor']*100:.0f}% "
            f"of contract value: ${direct:,.2f}"
        )

    # Consequential damages
    if inp.consequential_excluded:
        consequential = 0.0
        notes.append("Consequential damages excluded per contract terms")
    else:
        consequential = inp.contract_value * multipliers["consequential_factor"]
        notes.append(
            f"Consequential damages estimated at {multipliers['consequential_factor']*100:.0f}% "
            f"of contract value: ${consequential:,.2f}"
        )

    # Liquidated damages
    liquidated = 0.0
    if inp.liquidated_damages_rate is not None and inp.days_in_breach > 0:
        period_multiplier = {"day": 1, "week": 7, "month": 30}.get(
            inp.liquidated_damages_period or "day", 1
        )
        periods = inp.days_in_breach / period_multiplier
        liquidated = inp.contract_value * (inp.liquidated_damages_rate / 100.0) * periods
        notes.append(
            f"Liquidated damages: {inp.liquidated_damages_rate}% per {inp.liquidated_damages_period} "
            f"x {periods:.1f} periods = ${liquidated:,.2f}"
        )
        # Check for penalty vs. liquidated damages doctrine
        if liquidated > inp.contract_value * 0.5:
            notes.append(
                "WARNING: Liquidated damages exceed 50% of contract value — "
                "may be challenged as an unenforceable penalty under common law"
            )

    # Punitive damages potential
    punitive = inp.contract_value * multipliers["punitive_factor"]
    if punitive > 0:
        notes.append(
            f"Punitive damages potential: ${punitive:,.2f} (rare in contract cases, "
            "requires showing of fraud, malice, or willful misconduct)"
        )

    # Total before caps
    total_exposure = direct + consequential + liquidated + punitive

    # Liability cap
    cap_applied = False
    capped_exposure = total_exposure
    if inp.liability_cap is not None and inp.liability_cap > 0:
        if total_exposure > inp.liability_cap:
            capped_exposure = inp.liability_cap
            cap_applied = True
            notes.append(
                f"Liability cap applied: exposure reduced from ${total_exposure:,.2f} "
                f"to ${inp.liability_cap:,.2f}"
            )
        else:
            notes.append(f"Liability cap of ${inp.liability_cap:,.2f} not exceeded")

    # Mitigation credit
    mitigation_credit = 0.0
    if inp.mitigation_efforts:
        mitigation_credit = capped_exposure * multipliers["mitigation_credit"]
        notes.append(
            f"Mitigation efforts credit: ${mitigation_credit:,.2f} "
            f"({multipliers['mitigation_credit']*100:.0f}% reduction)"
        )

    net_exposure = max(0, capped_exposure - mitigation_credit)

    # Risk level classification
    ratio = net_exposure / inp.contract_value if inp.contract_value > 0 else 0
    if ratio > 0.5:
        risk_level = "CRITICAL"
    elif ratio > 0.3:
        risk_level = "HIGH"
    elif ratio > 0.15:
        risk_level = "MEDIUM"
    elif ratio > 0.05:
        risk_level = "LOW"
    else:
        risk_level = "MINIMAL"

    notes.append(f"Net exposure ratio: {ratio*100:.1f}% of contract value → {risk_level}")

    # Determinism hash
    hash_input = (
        f"{inp.contract_value}|{inp.breach_type}|{inp.days_in_breach}|"
        f"{direct}|{consequential}|{liquidated}|{net_exposure}"
    )
    det_hash = hashlib.sha256(hash_input.encode()).hexdigest()

    return DamagesEstimate(
        direct_damages=round(direct, 2),
        consequential_damages=round(consequential, 2),
        liquidated_damages=round(liquidated, 2),
        punitive_potential=round(punitive, 2),
        total_estimated_exposure=round(total_exposure, 2),
        liability_cap_applied=cap_applied,
        capped_exposure=round(capped_exposure, 2),
        mitigation_credit=round(mitigation_credit, 2),
        net_exposure=round(net_exposure, 2),
        risk_level=risk_level,
        calculation_notes=notes,
        disclaimer=(
            "LEGAL DISCLAIMER: This is an automated estimation tool for educational and "
            "planning purposes only. It does not constitute legal advice. Actual damages "
            "depend on jurisdiction, specific contract terms, court interpretation, and "
            "factual circumstances. Consult qualified legal counsel for specific situations."
        ),
        determinism_hash=det_hash,
    )


@app.post("/calculate-damages")
async def calculate_damages(inp: DamagesInput) -> DamagesEstimate:
    """Calculate estimated damages exposure from contract breach.

    Provides structured damages analysis including direct, consequential,
    liquidated, and punitive damages with liability cap application.
    """
    trace_id = trace_query("calculate_damages", inp.breach_type)
    try:
        result = _calculate_damages(inp)
        complete_trace(trace_id, True)
        _metrics.record_query(datetime.utcnow().timestamp(), "calculate_damages")
        return result
    except Exception as e:
        complete_trace(trace_id, False)
        log_error("calculate_damages", str(e), traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# JURISDICTION ANALYZER
# ============================================================================

class JurisdictionProfile(BaseModel):
    """Profile of a jurisdiction's contract law characteristics."""
    jurisdiction: str
    legal_system: str  # "common_law", "civil_law", "mixed"
    key_statutes: List[str]
    contract_formation_rules: List[str]
    notable_doctrines: List[str]
    limitation_period_years: int
    punitive_damages_available: bool
    specific_performance_availability: str  # "readily", "limited", "rare"
    forum_selection_enforceability: str  # "strong", "moderate", "weak"
    arbitration_friendly: bool
    non_compete_enforceability: str  # "strong", "moderate", "weak", "banned"
    choice_of_law_rules: str
    notable_considerations: List[str]


# Jurisdiction database
_JURISDICTIONS: Dict[str, JurisdictionProfile] = {
    "US_DELAWARE": JurisdictionProfile(
        jurisdiction="Delaware, USA",
        legal_system="common_law",
        key_statutes=[
            "Delaware Uniform Commercial Code (Title 6)",
            "Delaware General Corporation Law (Title 8)",
            "Delaware LLC Act (Title 6, Chapter 18)",
            "Delaware Arbitration Act",
        ],
        contract_formation_rules=[
            "Offer, acceptance, and consideration required",
            "Statute of Frauds applies to contracts over $500 in goods",
            "Electronic signatures valid under UETA adoption",
            "Parol evidence rule strictly applied",
        ],
        notable_doctrines=[
            "Freedom of contract strongly favored",
            "Implied covenant of good faith and fair dealing",
            "Economic waste doctrine limits specific performance",
            "Sophisticated party doctrine — fewer protective rules for commercial entities",
            "Efficient breach theory recognized",
        ],
        limitation_period_years=6,
        punitive_damages_available=True,
        specific_performance_availability="limited",
        forum_selection_enforceability="strong",
        arbitration_friendly=True,
        non_compete_enforceability="moderate",
        choice_of_law_rules=(
            "Strong presumption favoring parties' contractual choice of law. "
            "Delaware courts will honor choice-of-law provisions unless they "
            "violate a fundamental policy of a state with a materially greater interest."
        ),
        notable_considerations=[
            "Preferred jurisdiction for corporate and commercial disputes",
            "Court of Chancery provides specialized equity court",
            "Experienced judiciary with extensive commercial law precedent",
            "No jury trials in Chancery Court (equity only)",
            "Advanced and expedited proceedings available",
        ],
    ),
    "US_NEW_YORK": JurisdictionProfile(
        jurisdiction="New York, USA",
        legal_system="common_law",
        key_statutes=[
            "New York UCC (Article 2 — Sale of Goods)",
            "General Obligations Law",
            "CPLR (Civil Practice Law and Rules)",
            "BCL (Business Corporation Law)",
        ],
        contract_formation_rules=[
            "Offer, acceptance, and consideration required",
            "Statute of Frauds for goods over $500 and services over 1 year",
            "GOL Section 5-701 additional writing requirements",
            "Choice of law provisions respected under GOL Section 5-1401 (>$250K)",
        ],
        notable_doctrines=[
            "Four corners rule — contract interpreted within its four corners",
            "Sophisticated party presumption in commercial deals",
            "Material adverse change/effect doctrine",
            "Implied covenant of good faith and fair dealing (limited scope)",
            "No-oral-modification clauses enforced under GOL 15-301",
        ],
        limitation_period_years=6,
        punitive_damages_available=True,
        specific_performance_availability="limited",
        forum_selection_enforceability="strong",
        arbitration_friendly=True,
        non_compete_enforceability="moderate",
        choice_of_law_rules=(
            "GOL Section 5-1401: parties to contracts over $250,000 may select "
            "NY law regardless of connection. NY courts apply 'center of gravity' "
            "or 'grouping of contacts' test for conflicts."
        ),
        notable_considerations=[
            "Commercial Division handles complex commercial disputes",
            "Well-developed body of commercial law precedent",
            "International arbitration center (AAA, JAMS, ICC)",
            "High litigation costs — factor into dispute resolution planning",
            "GOL 5-1402 allows consent to NY jurisdiction for contracts >$1M",
        ],
    ),
    "US_CALIFORNIA": JurisdictionProfile(
        jurisdiction="California, USA",
        legal_system="common_law",
        key_statutes=[
            "California Civil Code",
            "California Commercial Code (UCC)",
            "California Business and Professions Code Section 16600",
            "CCPA/CPRA (Data Privacy)",
        ],
        contract_formation_rules=[
            "Offer, acceptance, and consideration required",
            "Civil Code 1624 — Statute of Frauds",
            "Unconscionability doctrine aggressively applied",
            "Public policy limitations on freedom of contract",
        ],
        notable_doctrines=[
            "Strong unconscionability doctrine — procedural and substantive",
            "Implied covenant of good faith and fair dealing (expansive)",
            "Anti-indemnity statutes in construction (Civil Code 2782)",
            "Penalties vs. liquidated damages strictly scrutinized",
            "Consumer protection overlay on B2B contracts with power imbalance",
        ],
        limitation_period_years=4,
        punitive_damages_available=True,
        specific_performance_availability="limited",
        forum_selection_enforceability="moderate",
        arbitration_friendly=True,
        non_compete_enforceability="banned",
        choice_of_law_rules=(
            "California applies governmental interest analysis. Courts may refuse "
            "to honor choice-of-law provisions if CA has a materially greater interest "
            "and the chosen law would violate a fundamental CA policy."
        ),
        notable_considerations=[
            "NON-COMPETE BAN: B&P Code 16600 voids non-competes (narrow exceptions only)",
            "CCPA/CPRA applies to personal data — contract must address",
            "Prop 65 environmental disclosures may be required",
            "Strong employee protection statutes affect service contracts",
            "Punitive damages available for fraud/oppression (Civil Code 3294)",
            "Anti-SLAPP statute may apply to certain contract disputes",
        ],
    ),
    "US_TEXAS": JurisdictionProfile(
        jurisdiction="Texas, USA",
        legal_system="common_law",
        key_statutes=[
            "Texas Business and Commerce Code",
            "Texas UCC (Title 1, Chapters 1-11)",
            "Texas Civil Practice and Remedies Code",
            "Texas Insurance Code (for insurance contracts)",
        ],
        contract_formation_rules=[
            "Offer, acceptance, and consideration required",
            "Statute of Frauds — Business & Commerce Code Chapter 26",
            "Electronic signatures valid under UETA",
            "Oral modifications may be valid despite no-oral-modification clauses",
        ],
        notable_doctrines=[
            "Plain meaning rule strictly applied",
            "No implied covenant of good faith in arm's-length commercial contracts",
            "Anti-indemnity statute (Chapter 127 — oilfield, Chapter 130 — construction)",
            "Economic loss rule limits tort claims in contract disputes",
            "Texas Citizens Participation Act (anti-SLAPP)",
        ],
        limitation_period_years=4,
        punitive_damages_available=True,
        specific_performance_availability="limited",
        forum_selection_enforceability="strong",
        arbitration_friendly=True,
        non_compete_enforceability="moderate",
        choice_of_law_rules=(
            "Texas applies Restatement (Second) of Conflict of Laws 'most significant "
            "relationship' test. Generally respects contractual choice of law unless "
            "it violates fundamental Texas policy."
        ),
        notable_considerations=[
            "OILFIELD: Chapter 127 voids indemnity for sole negligence of indemnitee",
            "CONSTRUCTION: Chapter 130 anti-indemnity provisions",
            "No state income tax — may affect compensation/payment structures",
            "Strong arbitration enforcement",
            "Exemplary (punitive) damages capped at greater of $200K or 2x economic + non-economic",
            "Attorney's fees recoverable if contract so provides (CPRC Chapter 38)",
        ],
    ),
    "UK_ENGLAND_WALES": JurisdictionProfile(
        jurisdiction="England and Wales, UK",
        legal_system="common_law",
        key_statutes=[
            "Sale of Goods Act 1979",
            "Unfair Contract Terms Act 1977 (UCTA)",
            "Contracts (Rights of Third Parties) Act 1999",
            "Late Payment of Commercial Debts Act 1998",
            "UK GDPR / Data Protection Act 2018",
        ],
        contract_formation_rules=[
            "Offer, acceptance, and consideration required",
            "No general Statute of Frauds (repealed, except land)",
            "Battle of the forms — last shot doctrine (Butler v. Ex-Cell-O)",
            "Electronic signatures valid",
        ],
        notable_doctrines=[
            "UCTA reasonableness test for exemption clauses",
            "Penalty clause doctrine (Cavendish v. Makdessi — proportionality test)",
            "Entire agreement clauses strictly construed",
            "Implied terms by statute and common law",
            "No punitive/exemplary damages in contract (Addis v. Gramophone)",
            "Mitigation of loss duty",
        ],
        limitation_period_years=6,
        punitive_damages_available=False,
        specific_performance_availability="rare",
        forum_selection_enforceability="strong",
        arbitration_friendly=True,
        non_compete_enforceability="moderate",
        choice_of_law_rules=(
            "Rome I Regulation (retained in UK law). Parties' choice of law generally "
            "respected. In absence of choice, law of habitual residence of characteristic "
            "performer applies."
        ),
        notable_considerations=[
            "London is global center for commercial arbitration (LCIA, ICC)",
            "No punitive damages in contract — only compensatory",
            "UCTA may invalidate unreasonable exclusion/limitation clauses",
            "UK GDPR applies to personal data processing",
            "Late payment interest statutory right (8% + Bank of England base rate)",
            "Penalty clause reform post-Cavendish: legitimate interest test",
        ],
    ),
}


@app.get("/jurisdictions")
async def list_jurisdictions() -> Dict[str, Any]:
    """List all available jurisdiction profiles."""
    return {
        "jurisdictions": {
            key: {
                "name": profile.jurisdiction,
                "legal_system": profile.legal_system,
                "limitation_years": profile.limitation_period_years,
                "non_compete": profile.non_compete_enforceability,
                "arbitration_friendly": profile.arbitration_friendly,
            }
            for key, profile in _JURISDICTIONS.items()
        },
        "count": len(_JURISDICTIONS),
    }


@app.get("/jurisdictions/{key}")
async def get_jurisdiction(key: str) -> JurisdictionProfile:
    """Get detailed profile for a specific jurisdiction."""
    key_upper = key.upper()
    if key_upper not in _JURISDICTIONS:
        raise HTTPException(
            status_code=404,
            detail=f"Jurisdiction '{key}' not found. Available: {list(_JURISDICTIONS.keys())}",
        )
    return _JURISDICTIONS[key_upper]


class JurisdictionCompareRequest(BaseModel):
    """Request to compare jurisdictions."""
    jurisdictions: List[str]
    contract_type: str = "general"
    focus_areas: List[str] = []  # e.g., ["non_compete", "liability", "arbitration"]


@app.post("/jurisdictions/compare")
async def compare_jurisdictions(request: JurisdictionCompareRequest) -> Dict[str, Any]:
    """Compare multiple jurisdictions for contract planning.

    Produces side-by-side comparison of key legal characteristics
    relevant to contract negotiation and dispute resolution.
    """
    trace_id = trace_query("jurisdiction_compare", ",".join(request.jurisdictions))
    try:
        profiles: Dict[str, JurisdictionProfile] = {}
        for j_key in request.jurisdictions:
            key_upper = j_key.upper()
            if key_upper in _JURISDICTIONS:
                profiles[key_upper] = _JURISDICTIONS[key_upper]

        if not profiles:
            raise HTTPException(
                status_code=400,
                detail=f"No valid jurisdictions found. Available: {list(_JURISDICTIONS.keys())}",
            )

        # Build comparison matrix
        comparison = {
            "jurisdictions_compared": list(profiles.keys()),
            "comparison_matrix": {},
            "recommendations": [],
        }

        # Standard comparison dimensions
        dimensions = [
            ("legal_system", lambda p: p.legal_system),
            ("limitation_period", lambda p: f"{p.limitation_period_years} years"),
            ("punitive_damages", lambda p: "Available" if p.punitive_damages_available else "Not available"),
            ("specific_performance", lambda p: p.specific_performance_availability),
            ("forum_selection", lambda p: p.forum_selection_enforceability),
            ("arbitration", lambda p: "Friendly" if p.arbitration_friendly else "Unfriendly"),
            ("non_compete", lambda p: p.non_compete_enforceability),
        ]

        for dim_name, dim_func in dimensions:
            comparison["comparison_matrix"][dim_name] = {
                key: dim_func(profile) for key, profile in profiles.items()
            }

        # Generate recommendations based on comparison
        if len(profiles) >= 2:
            # Find most business-friendly jurisdiction
            scoring: Dict[str, int] = {k: 0 for k in profiles}
            for key, profile in profiles.items():
                if profile.arbitration_friendly:
                    scoring[key] += 2
                if profile.forum_selection_enforceability == "strong":
                    scoring[key] += 2
                if profile.non_compete_enforceability in ("moderate", "strong"):
                    scoring[key] += 1
                if profile.limitation_period_years >= 6:
                    scoring[key] += 1
                if not profile.punitive_damages_available:
                    scoring[key] += 1  # Less exposure for defendants

            best = max(scoring, key=scoring.get)  # type: ignore[arg-type]
            comparison["recommendations"].append(
                f"Most business-friendly for defendants: {best} (score: {scoring[best]})"
            )

            # Non-compete warning
            for key, profile in profiles.items():
                if profile.non_compete_enforceability == "banned":
                    comparison["recommendations"].append(
                        f"WARNING: Non-competes banned in {key} — do not include in contracts governed by this law"
                    )

        comparison["analysis_timestamp"] = datetime.utcnow().isoformat() + "Z"

        complete_trace(trace_id, True)
        _metrics.record_query(datetime.utcnow().timestamp(), "jurisdiction_compare")
        return comparison

    except HTTPException:
        raise
    except Exception as e:
        complete_trace(trace_id, False)
        log_error("jurisdiction_compare", str(e), traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# NEGOTIATION ADVISOR
# ============================================================================

class NegotiationPosition(BaseModel):
    """A single negotiation position with strategy."""
    clause_type: str
    current_position: str
    recommended_position: str
    leverage_points: List[str]
    concession_strategy: str
    walk_away_threshold: str
    priority: str  # "must_have", "strong_preference", "nice_to_have", "tradeable"


class NegotiationPlan(BaseModel):
    """Full negotiation plan for a contract."""
    contract_type: str
    party_role: str  # "buyer", "seller", "licensor", "licensee", "employer", "contractor"
    total_positions: int
    must_haves: int
    strong_preferences: int
    nice_to_haves: int
    tradeables: int
    positions: List[NegotiationPosition]
    overall_strategy: str
    opening_move: str
    fallback_strategy: str
    batna_notes: str  # Best Alternative to Negotiated Agreement
    analysis_timestamp: str


# Negotiation strategy library by party role
_NEGOTIATION_STRATEGIES: Dict[str, Dict[str, List[NegotiationPosition]]] = {
    "buyer": {
        "general": [
            NegotiationPosition(
                clause_type="limitation_of_liability",
                current_position="Seller liability unlimited",
                recommended_position="Cap at 2-3x annual contract value with carve-outs",
                leverage_points=[
                    "Market competition — alternative suppliers available",
                    "Volume commitment as bargaining chip",
                    "Insurance coverage can backstop the cap",
                ],
                concession_strategy="Start at 3x, concede to 2x if needed, but protect carve-outs for IP infringement and data breach",
                walk_away_threshold="Cap below 1x annual value with no carve-outs is unacceptable",
                priority="strong_preference",
            ),
            NegotiationPosition(
                clause_type="termination",
                current_position="Seller can terminate at will with 30 days notice",
                recommended_position="Mutual termination for convenience with 90 days notice; termination for cause with 30 days cure",
                leverage_points=[
                    "Transition costs are significant — short notice is disruptive",
                    "Industry standard is 90 days for enterprise contracts",
                    "Offer longer initial term in exchange for termination protection",
                ],
                concession_strategy="Negotiate from 120 days down to 90 days; accept 60 days only with transition assistance clause",
                walk_away_threshold="Less than 60 days notice without transition assistance",
                priority="must_have",
            ),
            NegotiationPosition(
                clause_type="warranty",
                current_position="As-is, no warranties",
                recommended_position="12-month warranty on deliverables with re-performance remedy",
                leverage_points=[
                    "Warranty demonstrates seller confidence in their product",
                    "Industry standard warranties exist — no warranty is below market",
                    "Warranty cost is minimal for quality products",
                ],
                concession_strategy="Start at 24 months, concede to 12 months. Accept 6 months only for custom/experimental work",
                walk_away_threshold="No warranty at all for standard products/services",
                priority="must_have",
            ),
            NegotiationPosition(
                clause_type="data_protection",
                current_position="No data protection terms",
                recommended_position="DPA with breach notification, security standards, and audit rights",
                leverage_points=[
                    "Regulatory requirement — GDPR/CCPA mandate data protection terms",
                    "Reputational risk to both parties from data breach",
                    "Standard DPA templates available — low effort to include",
                ],
                concession_strategy="Non-negotiable for any contract involving personal data or confidential business data",
                walk_away_threshold="No data protection terms when data sharing is involved",
                priority="must_have",
            ),
            NegotiationPosition(
                clause_type="indemnification",
                current_position="No indemnification",
                recommended_position="Mutual indemnification for IP infringement and third-party claims from negligence",
                leverage_points=[
                    "IP indemnification is market standard",
                    "Mutual structure is balanced — protects both parties",
                    "Insurance typically covers these obligations",
                ],
                concession_strategy="Start with broad mutual indemnification, narrow to IP + negligence if needed",
                walk_away_threshold="No IP indemnification from seller",
                priority="strong_preference",
            ),
            NegotiationPosition(
                clause_type="pricing",
                current_position="Annual price increases at seller discretion",
                recommended_position="Price lock for initial term with CPI-based cap on renewal increases",
                leverage_points=[
                    "Multi-year commitment reduces seller's acquisition cost",
                    "Budget predictability is essential for planning",
                    "Competitive alternatives with better pricing terms",
                ],
                concession_strategy="Accept CPI + 2% cap as compromise; reject uncapped discretionary increases",
                walk_away_threshold="Uncapped price increases or increases exceeding 10% per year",
                priority="strong_preference",
            ),
        ],
    },
    "seller": {
        "general": [
            NegotiationPosition(
                clause_type="limitation_of_liability",
                current_position="Unlimited exposure",
                recommended_position="Cap at 12 months of fees with exclusion of consequential damages",
                leverage_points=[
                    "Liability exposure must be insurable and proportional",
                    "Unlimited liability creates pricing pressure",
                    "Industry standard is 12 months for SaaS/services",
                ],
                concession_strategy="Start at 6 months, move to 12 months. Resist 24+ months unless premium pricing",
                walk_away_threshold="Unlimited liability or consequential damages without exclusion",
                priority="must_have",
            ),
            NegotiationPosition(
                clause_type="payment_terms",
                current_position="Net 60 or longer",
                recommended_position="Net 30 with late payment interest",
                leverage_points=[
                    "Cash flow impact of extended payment terms",
                    "Late payment interest is standard commercial practice",
                    "Offer early payment discount as incentive",
                ],
                concession_strategy="Accept Net 45 as compromise; offer 2% discount for Net 15",
                walk_away_threshold="Net 90+ without advance payment or milestone structure",
                priority="strong_preference",
            ),
            NegotiationPosition(
                clause_type="scope_of_work",
                current_position="Broadly defined scope",
                recommended_position="Narrow, specific scope with formal change order process",
                leverage_points=[
                    "Clear scope protects both parties from disputes",
                    "Change orders allow flexibility while maintaining control",
                    "Scope creep is the top cause of project failure",
                ],
                concession_strategy="Define core scope tightly; allow minor adjustments (< 10% effort) without change order",
                walk_away_threshold="Open-ended scope without change order mechanism",
                priority="must_have",
            ),
            NegotiationPosition(
                clause_type="intellectual_property",
                current_position="All IP transfers to buyer",
                recommended_position="Work product transfers; pre-existing IP retained with perpetual license",
                leverage_points=[
                    "Pre-existing IP represents years of investment",
                    "License grant achieves buyer's operational needs",
                    "Full IP transfer would require significant premium",
                ],
                concession_strategy="Grant broad license to pre-existing IP in deliverables; retain ownership for reuse",
                walk_away_threshold="Transfer of all pre-existing IP without substantial premium",
                priority="must_have",
            ),
        ],
    },
}


def _generate_negotiation_plan(
    contract_type: str,
    party_role: str,
    contract_text: str = "",
) -> NegotiationPlan:
    """Generate a negotiation plan based on party role and contract type."""
    # Get base positions for role
    role_positions = _NEGOTIATION_STRATEGIES.get(party_role, {}).get("general", [])

    if not role_positions:
        # Generate generic positions
        role_positions = _NEGOTIATION_STRATEGIES.get("buyer", {}).get("general", [])

    # Count by priority
    counts = {"must_have": 0, "strong_preference": 0, "nice_to_have": 0, "tradeable": 0}
    for pos in role_positions:
        counts[pos.priority] = counts.get(pos.priority, 0) + 1

    # Generate overall strategy
    if party_role in ("buyer", "licensee"):
        overall_strategy = (
            "Leverage competitive alternatives and volume commitment to secure favorable terms. "
            "Prioritize protection clauses (liability cap, warranty, data protection) as must-haves. "
            "Use pricing flexibility and term length as tradeable concessions."
        )
        opening_move = (
            "Lead with willingness to commit to a longer term or higher volume in exchange for "
            "stronger protective terms. Present your ideal position on all must-have clauses early."
        )
        fallback_strategy = (
            "If key protections cannot be achieved, consider: (1) phased approach with shorter "
            "initial term; (2) escrow arrangement for liability; (3) third-party insurance rider."
        )
        batna_notes = (
            "Maintain active alternatives throughout negotiation. Ensure at least two qualified "
            "vendors have been evaluated. BATNA strength directly correlates with negotiation leverage."
        )
    else:
        overall_strategy = (
            "Protect margins and intellectual property while demonstrating value. Lead with "
            "product/service differentiation to justify premium terms. Use scope clarity as "
            "the foundation for all other negotiations."
        )
        opening_move = (
            "Present comprehensive proposal with clear scope, pricing, and standard terms. "
            "Anchor on your standard contract rather than responding to buyer's template."
        )
        fallback_strategy = (
            "If buyer demands exceed acceptable risk: (1) offer tiered pricing for different "
            "risk levels; (2) propose insurance-backed indemnification; (3) suggest pilot phase."
        )
        batna_notes = (
            "Understand your sales pipeline and this deal's importance. Stronger pipeline = "
            "more willingness to walk away from unfavorable terms."
        )

    return NegotiationPlan(
        contract_type=contract_type,
        party_role=party_role,
        total_positions=len(role_positions),
        must_haves=counts["must_have"],
        strong_preferences=counts["strong_preference"],
        nice_to_haves=counts["nice_to_have"],
        tradeables=counts["tradeable"],
        positions=role_positions,
        overall_strategy=overall_strategy,
        opening_move=opening_move,
        fallback_strategy=fallback_strategy,
        batna_notes=batna_notes,
        analysis_timestamp=datetime.utcnow().isoformat() + "Z",
    )


class NegotiationRequest(BaseModel):
    """Request for negotiation plan generation."""
    contract_type: str = "general"
    party_role: str = "buyer"  # "buyer", "seller", "licensor", "licensee"
    contract_text: str = ""
    focus_areas: List[str] = []


@app.post("/negotiation-plan")
async def negotiation_plan(request: NegotiationRequest) -> NegotiationPlan:
    """Generate a negotiation plan for a contract.

    Produces structured negotiation positions with leverage points,
    concession strategies, and walk-away thresholds per clause type.
    """
    trace_id = trace_query("negotiation_plan", request.party_role)
    try:
        plan = _generate_negotiation_plan(
            contract_type=request.contract_type,
            party_role=request.party_role,
            contract_text=request.contract_text,
        )
        complete_trace(trace_id, True)
        _metrics.record_query(datetime.utcnow().timestamp(), "negotiation_plan")
        return plan
    except Exception as e:
        complete_trace(trace_id, False)
        log_error("negotiation_plan", str(e), traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# LAUNCH
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
        workers=1,
    )