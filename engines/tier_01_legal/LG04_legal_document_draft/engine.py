"""
LG04 LEGAL DOCUMENT DRAFT ENGINE - Production Architecture
============================================================
TIE-20 compliant legal document drafting system for contract generation,
clause library management, template assembly, jurisdiction-specific
document variations, compliance checking, version tracking, and
collaborative editing support.

Architecture:
    Layer 1: Doctrine Cache (0-150ms) - Pre-compiled legal drafting doctrines
    Layer 2: Semantic Search (150-500ms) - TF-IDF clause and template search
    Layer 3: Document Assembly (500-1200ms) - Template-driven document generation
    Layer 4: Deep Analysis (on-demand) - Multi-doctrine synthesis

Response Modes:
    DET: Deterministic - exact template-driven drafting
    EF: Efficiency - balanced drafting with smart defaults
    SPEC: Specialist - detailed jurisdiction-specific drafting
    QUANTUM: Quantum - multi-scenario drafting with alternatives

Port: 8394
Engine ID: LG04
Tier: LEGAL (Auth 5.0)
Mode: EF (Efficiency)
Version: 1.0.0
Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import time
import traceback
import uuid
from collections import Counter, defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Literal, Optional, Set, Tuple

from fastapi import FastAPI, HTTPException, Depends, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

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
    record_document_generation,
    ErrorDomain,
    ResponseLayer,
    MutationType,
    MutationOrigin,
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
    get_document_type_patterns,
    get_jurisdiction_patterns,
    get_clause_category_keywords,
    DocumentDomain,
    ClauseCategory,
)

import sys

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DOCTRINE_CACHE,
    DoctrineResponse,
    LegalDocumentDoctrineEngine,
    get_engine as get_doctrine_engine,
    DoctrineDomain,
)

from search import (
    DoctrineSearchIndex,
    SearchResult,
    SearchResponse,
    ClauseTemplate,
    TemplateMatchResult,
    DocumentSimilarityResult,
    SearchMode,
    get_search_index,
    compute_query_hash,
    compute_content_hash,
)

# ============================================================================
# LOGGING SETUP
# ============================================================================

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG04_legal_document_draft/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "lg04_engine_{time}.log",
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
    """Available response modes for the engine."""
    DET = "DET"
    EF = "EF"
    SPEC = "SPEC"
    QUANTUM = "QUANTUM"


class ConfidenceBand(str, Enum):
    """Confidence stratification bands."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNCERTAIN = "UNCERTAIN"


class AnalysisZone(str, Enum):
    """Zoned analysis categories."""
    CONTRACT_FORMATION = "contract_formation"
    UCC_COMPLIANCE = "ucc_compliance"
    REAL_ESTATE = "real_estate"
    EMPLOYMENT = "employment"
    CORPORATE = "corporate"
    IP_RIGHTS = "ip_rights"
    FINANCE = "finance"
    ESTATE_PLANNING = "estate_planning"
    MA_TRANSACTION = "ma_transaction"
    REGULATORY = "regulatory"
    BOILERPLATE = "boilerplate"
    GENERAL = "general"


ENGINE_ID = "LG04"
ENGINE_NAME = "Legal Document Draft Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8394
ENGINE_AUTHORITY = 5.0
ENGINE_TIER = "LEGAL"
ENGINE_MODE = "EF"

AUTHORITY_GATE_LEVEL = 5.0

CONFIDENCE_THRESHOLDS = {
    ConfidenceBand.HIGH: 0.85,
    ConfidenceBand.MEDIUM: 0.65,
    ConfidenceBand.LOW: 0.40,
    ConfidenceBand.UNCERTAIN: 0.0,
}

BANNED_PHRASES = [
    "this document is guaranteed to be enforceable",
    "no court would challenge this",
    "this is a bulletproof contract",
    "you are fully protected",
    "this eliminates all legal risk",
    "no one can sue you with this",
    "this is absolutely binding",
    "there is zero chance of dispute",
]

DISCLAIMER_NOT_LEGAL_ADVICE = (
    "This document is generated for informational purposes. "
    "Consult a licensed attorney before execution."
)
DISCLAIMER_JURISDICTION = (
    "Legal requirements vary by jurisdiction. "
    "This document should be reviewed for local compliance."
)
DISCLAIMER_FACT_DEPENDENT = (
    "Document enforceability depends on specific facts and circumstances."
)


# ############################################################################
#
# SECTION 2: PYDANTIC REQUEST / RESPONSE MODELS
#
# ############################################################################


class DraftRequest(BaseModel):
    """Request to draft a legal document or query the engine."""
    query: str = Field(..., min_length=1, max_length=10000)
    document_type: str = ""
    jurisdiction: str = ""
    mode: ResponseMode = ResponseMode.EF
    authority_level: float = 5.0
    parties: List[str] = Field(default_factory=list)
    variables: Dict[str, str] = Field(default_factory=dict)
    clause_types: List[str] = Field(default_factory=list)
    include_deep_analysis: bool = False
    include_compliance_check: bool = True
    max_results: int = 5


class ClauseRequest(BaseModel):
    """Request for clause library operations."""
    clause_type: str = ""
    jurisdiction: str = ""
    document_type: str = ""
    query: str = ""
    top_k: int = 5


class ComplianceCheckRequest(BaseModel):
    """Request to check document compliance."""
    document_content: str = Field(..., min_length=1)
    document_type: str = ""
    jurisdiction: str = ""
    regulations: List[str] = Field(default_factory=list)


class VersionRequest(BaseModel):
    """Request for document version operations."""
    document_id: str
    content: str = ""
    author: str = ""
    comment: str = ""


class ThreeLayerResponse(BaseModel):
    """Three-layer response structure: summary, analysis, deep_dive."""
    summary: str
    analysis: str
    deep_dive: str = ""


class ComplianceResult(BaseModel):
    """Result of a compliance check."""
    compliant: bool = False
    score: float = 0.0
    issues: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    checked_regulations: List[str] = Field(default_factory=list)


class FactFragilityScore(BaseModel):
    """Fact fragility assessment for a document or clause."""
    overall_score: float = 0.0
    fragile_elements: List[Dict[str, Any]] = Field(default_factory=list)
    stable_elements: List[str] = Field(default_factory=list)
    risk_level: str = "MEDIUM"


class DriftStatus(BaseModel):
    """Doctrine drift watcher status."""
    doctrine_id: str
    topic: str
    last_checked: str = ""
    days_since_update: int = 0
    drift_detected: bool = False
    drift_signals: List[str] = Field(default_factory=list)
    confidence_adjustment: float = 0.0


class DocumentVersion(BaseModel):
    """A tracked version of a document."""
    version_id: str
    document_id: str
    version_number: int
    content_hash: str
    author: str = ""
    comment: str = ""
    timestamp: str = ""
    word_count: int = 0


class DraftResponse(BaseModel):
    """Full response from the drafting engine."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    trace_id: str = ""
    query: str = ""
    document_type: str = ""
    jurisdiction: str = ""
    mode: str = "EF"
    authority_level: float = 0.0
    response: ThreeLayerResponse
    doctrines_used: List[str] = Field(default_factory=list)
    clauses_generated: int = 0
    confidence: ConfidenceBand = ConfidenceBand.MEDIUM
    confidence_score: float = 0.0
    compliance: Optional[ComplianceResult] = None
    fact_fragility: Optional[FactFragilityScore] = None
    drift_warnings: List[DriftStatus] = Field(default_factory=list)
    normalization: Optional[Dict[str, Any]] = None
    determinism_hash: str = ""
    duration_ms: float = 0.0
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    disclaimers: List[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    port: int = ENGINE_PORT
    authority_level: float = ENGINE_AUTHORITY
    tier: str = ENGINE_TIER
    mode: str = ENGINE_MODE
    total_doctrines: int = 0
    total_clause_templates: int = 0
    search_index_docs: int = 0
    semantic_map_version: str = ""
    semantic_map_hash: str = ""
    telemetry_status: str = ""
    uptime_seconds: float = 0.0
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ############################################################################
#
# SECTION 3: AUTHORITY HARDENING
#
# ############################################################################


def verify_authority(level: float) -> bool:
    """Verify that the request has sufficient authority level."""
    return level >= AUTHORITY_GATE_LEVEL


def enforce_authority(level: float) -> None:
    """Raise an exception if authority is insufficient."""
    if not verify_authority(level):
        logger.warning("Authority gate REJECTED | provided={} required={}", level, AUTHORITY_GATE_LEVEL)
        raise HTTPException(
            status_code=403,
            detail=f"Insufficient authority level. Required: {AUTHORITY_GATE_LEVEL}, provided: {level}",
        )


# ############################################################################
#
# SECTION 4: CONFIDENCE STRATIFICATION
#
# ############################################################################


def stratify_confidence(score: float) -> ConfidenceBand:
    """Map a numeric confidence score to a confidence band."""
    if score >= CONFIDENCE_THRESHOLDS[ConfidenceBand.HIGH]:
        return ConfidenceBand.HIGH
    if score >= CONFIDENCE_THRESHOLDS[ConfidenceBand.MEDIUM]:
        return ConfidenceBand.MEDIUM
    if score >= CONFIDENCE_THRESHOLDS[ConfidenceBand.LOW]:
        return ConfidenceBand.LOW
    return ConfidenceBand.UNCERTAIN


def compute_confidence(
    doctrine_hits: int,
    search_score: float,
    normalization_confidence: float,
    jurisdiction_matched: bool,
    document_type_matched: bool,
) -> float:
    """Compute composite confidence score from multiple signals."""
    score = 0.0
    if doctrine_hits > 0:
        score += min(0.35, doctrine_hits * 0.07)
    score += min(0.25, search_score * 0.25)
    score += normalization_confidence * 0.20
    if jurisdiction_matched:
        score += 0.10
    if document_type_matched:
        score += 0.10
    return min(1.0, score)


# ############################################################################
#
# SECTION 5: EPISTEMIC GUARDRAILS
#
# ############################################################################


def apply_epistemic_guardrails(text: str) -> Tuple[str, List[str]]:
    """Scan text for banned phrases and apply epistemic safety checks."""
    violations: List[str] = []
    cleaned = text
    for phrase in BANNED_PHRASES:
        if phrase.lower() in cleaned.lower():
            violations.append(f"Removed banned phrase: '{phrase}'")
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            cleaned = pattern.sub("[REDACTED - overconfident claim]", cleaned)
    return cleaned, violations


def get_required_disclaimers(confidence: ConfidenceBand) -> List[str]:
    """Return disclaimers required based on confidence level."""
    disclaimers = [DISCLAIMER_NOT_LEGAL_ADVICE]
    if confidence in (ConfidenceBand.LOW, ConfidenceBand.UNCERTAIN, ConfidenceBand.MEDIUM):
        disclaimers.append(DISCLAIMER_JURISDICTION)
        disclaimers.append(DISCLAIMER_FACT_DEPENDENT)
    return disclaimers


# ############################################################################
#
# SECTION 6: DETERMINISM HASH
#
# ############################################################################


def compute_determinism_hash(
    query: str,
    document_type: str,
    jurisdiction: str,
    mode: str,
    response_content: str,
) -> str:
    """Compute SHA-256 determinism hash for the response."""
    payload = f"{query}|{document_type}|{jurisdiction}|{mode}|{response_content}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ############################################################################
#
# SECTION 7: AUDIT TRAIL
#
# ############################################################################


def write_audit_entry(entry: Dict[str, Any]) -> None:
    """Append an audit entry to the JSONL audit log."""
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    entry["engine_id"] = ENGINE_ID
    try:
        with open(AUDIT_LOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, default=str) + "\n")
    except OSError as exc:
        logger.error("Audit write failed: {}", str(exc))


# ############################################################################
#
# SECTION 8: FACT FRAGILITY SCORING
#
# ############################################################################


def assess_fact_fragility(
    content: str,
    document_type: str = "",
    jurisdiction: str = "",
) -> FactFragilityScore:
    """Assess the fragility of factual claims in document content."""
    fragile_elements: List[Dict[str, Any]] = []
    stable_elements: List[str] = []

    fragile_patterns = [
        (r"\b(currently|presently|at this time)\b", "temporal_dependency", 0.7),
        (r"\b(approximately|about|roughly|estimated)\b", "imprecise_quantity", 0.5),
        (r"\b(may|might|could|possibly)\b", "uncertainty_hedging", 0.4),
        (r"\b(to the best of .+ knowledge)\b", "knowledge_limitation", 0.6),
        (r"\b(as of the date hereof)\b", "date_dependency", 0.5),
        (r"\b(subject to change)\b", "explicit_mutability", 0.8),
        (r"\b(believed to be|understood to be)\b", "belief_qualifier", 0.6),
        (r"\b(in the opinion of)\b", "opinion_qualifier", 0.5),
    ]

    stable_patterns = [
        r"\b(shall|must|will)\b",
        r"\b(represents and warrants)\b",
        r"\b(unconditionally|irrevocably)\b",
        r"\b(covenants and agrees)\b",
        r"\b(is and shall be)\b",
    ]

    content_lower = content.lower()
    total_fragility = 0.0
    fragile_count = 0

    for pattern, label, weight in fragile_patterns:
        matches = re.findall(pattern, content_lower)
        if matches:
            fragile_count += len(matches)
            total_fragility += weight * len(matches)
            fragile_elements.append({
                "pattern": label,
                "occurrences": len(matches),
                "weight": weight,
                "risk_contribution": round(weight * len(matches), 3),
            })

    for pattern in stable_patterns:
        matches = re.findall(pattern, content_lower)
        if matches:
            stripped = pattern.strip(r'\\b()')
            stable_elements.append(f"{stripped} ({len(matches)} occurrences)")

    word_count = len(content.split())
    normalized_score = min(1.0, total_fragility / max(word_count / 100, 1))

    if normalized_score >= 0.7:
        risk = "HIGH"
    elif normalized_score >= 0.4:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return FactFragilityScore(
        overall_score=round(normalized_score, 4),
        fragile_elements=fragile_elements,
        stable_elements=stable_elements,
        risk_level=risk,
    )


# ############################################################################
#
# SECTION 9: DOCTRINE DRIFT WATCHER
#
# ############################################################################


class DoctrineDriftWatcher:
    """Monitors doctrine blocks for staleness and drift signals."""

    def __init__(self) -> None:
        self._staleness_threshold_days = ENGINE_CONFIG.get("drift_watcher", {}).get("staleness_threshold_days", 90)
        self._confidence_reduction = ENGINE_CONFIG.get("drift_watcher", {}).get("confidence_reduction_percent", 10) / 100.0
        self._drift_registry: Dict[str, DriftStatus] = {}
        self._initialize_registry()

    def _initialize_registry(self) -> None:
        now = datetime.now(timezone.utc)
        for doctrine_id, block in DOCTRINE_CACHE.items():
            last_updated = block.last_updated or "2026-02-10T00:00:00Z"
            try:
                updated_dt = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                updated_dt = now
            days_since = (now - updated_dt).days

            self._drift_registry[doctrine_id] = DriftStatus(
                doctrine_id=doctrine_id,
                topic=block.topic,
                last_checked=now.isoformat(),
                days_since_update=days_since,
                drift_detected=days_since > self._staleness_threshold_days,
                drift_signals=["staleness_warning"] if days_since > self._staleness_threshold_days else [],
                confidence_adjustment=-self._confidence_reduction if days_since > self._staleness_threshold_days else 0.0,
            )

    def check_doctrine(self, doctrine_id: str) -> Optional[DriftStatus]:
        return self._drift_registry.get(doctrine_id)

    def get_stale_doctrines(self) -> List[DriftStatus]:
        return [ds for ds in self._drift_registry.values() if ds.drift_detected]

    def get_all_status(self) -> List[DriftStatus]:
        return list(self._drift_registry.values())

    def apply_confidence_adjustment(self, doctrine_id: str, base_confidence: float) -> float:
        status = self._drift_registry.get(doctrine_id)
        if status and status.drift_detected:
            return max(0.0, base_confidence + status.confidence_adjustment)
        return base_confidence


# ############################################################################
#
# SECTION 10: DOCTRINE COVERAGE MAP
#
# ############################################################################


class DoctrineCoverageMap:
    """Maps document types to required doctrines and tracks coverage gaps."""

    COVERAGE_REQUIREMENTS: ClassVar[Dict[str, List[str]]] = {
        "sales_agreement": ["offer_and_acceptance", "consideration", "ucc_scope_and_applicability", "ucc_warranties", "ucc_risk_of_loss", "ucc_remedies"],
        "service_agreement": ["offer_and_acceptance", "consideration", "contract_interpretation", "breach_and_remedies"],
        "employment_agreement": ["at_will_employment", "non_compete_agreements", "confidentiality_nda", "ip_assignment_employment"],
        "lease_agreement": ["commercial_lease", "statute_of_frauds"],
        "merger_agreement": ["merger_agreement_structure", "due_diligence", "letter_of_intent"],
        "nda": ["confidentiality_nda"],
        "promissory_note": ["promissory_note"],
        "deed": ["deed_types", "deed_of_trust_mortgage"],
        "operating_agreement": ["llc_operating_agreement"],
        "shareholder_agreement": ["shareholder_agreement"],
        "trust": ["revocable_living_trust"],
        "will": ["last_will_testament"],
        "power_of_attorney": ["power_of_attorney"],
        "privacy_policy": ["privacy_policy_requirements"],
        "terms_of_service": ["terms_of_service"],
        "asset_purchase_agreement": ["asset_purchase_agreement", "due_diligence"],
        "software_license": ["software_license"],
    }

    def __init__(self) -> None:
        self._engine = get_doctrine_engine()

    def get_coverage(self, document_type: str) -> Dict[str, Any]:
        required = self.COVERAGE_REQUIREMENTS.get(document_type, [])
        if not required:
            return {"document_type": document_type, "coverage": 0.0, "covered": [], "gaps": [], "message": "No coverage requirements defined for this document type."}

        covered: List[str] = []
        gaps: List[str] = []
        for topic in required:
            result = self._engine.get_by_topic(topic)
            if result:
                covered.append(topic)
            else:
                gaps.append(topic)

        coverage_pct = len(covered) / len(required) if required else 0.0
        return {
            "document_type": document_type,
            "coverage": round(coverage_pct, 4),
            "total_required": len(required),
            "total_covered": len(covered),
            "covered": covered,
            "gaps": gaps,
        }

    def get_all_coverage(self) -> Dict[str, Any]:
        results = {}
        for doc_type in self.COVERAGE_REQUIREMENTS:
            results[doc_type] = self.get_coverage(doc_type)
        return results


# ############################################################################
#
# SECTION 11: METRICS COLLECTOR
#
# ############################################################################


class MetricsCollector:
    """Collects and aggregates engine performance metrics."""

    def __init__(self) -> None:
        self._request_count = 0
        self._error_count = 0
        self._latencies: List[float] = []
        self._documents_generated = 0
        self._clauses_generated = 0
        self._by_mode: Dict[str, int] = defaultdict(int)
        self._by_doc_type: Dict[str, int] = defaultdict(int)
        self._by_jurisdiction: Dict[str, int] = defaultdict(int)
        self._start_time = time.time()

    def record_request(self, mode: str, doc_type: str, jurisdiction: str, latency_ms: float, clauses: int, error: bool = False) -> None:
        self._request_count += 1
        self._latencies.append(latency_ms)
        self._by_mode[mode] += 1
        if doc_type:
            self._by_doc_type[doc_type] += 1
        if jurisdiction:
            self._by_jurisdiction[jurisdiction] += 1
        self._clauses_generated += clauses
        if error:
            self._error_count += 1
        else:
            self._documents_generated += 1

    def get_summary(self) -> Dict[str, Any]:
        avg_lat = sum(self._latencies) / len(self._latencies) if self._latencies else 0.0
        sorted_lats = sorted(self._latencies)
        p95 = sorted_lats[int(len(sorted_lats) * 0.95)] if len(sorted_lats) > 1 else avg_lat
        return {
            "total_requests": self._request_count,
            "total_documents": self._documents_generated,
            "total_clauses": self._clauses_generated,
            "total_errors": self._error_count,
            "error_rate": round(self._error_count / max(self._request_count, 1), 4),
            "avg_latency_ms": round(avg_lat, 2),
            "p95_latency_ms": round(p95, 2),
            "by_mode": dict(self._by_mode),
            "by_document_type": dict(self._by_doc_type),
            "by_jurisdiction": dict(self._by_jurisdiction),
            "uptime_seconds": round(time.time() - self._start_time, 2),
        }


# ############################################################################
#
# SECTION 12: CLAUSE LIBRARY AND TEMPLATE ENGINE
#
# ############################################################################


class ClauseLibrary:
    """Manages clause templates with categorization, versioning, and retrieval."""

    def __init__(self) -> None:
        self._search_index = get_search_index()
        self._templates: Dict[str, ClauseTemplate] = {}
        self._load_default_clauses()

    def _load_default_clauses(self) -> None:
        """Load default clause templates from doctrine cache."""
        default_clauses = self._generate_default_clauses()
        for clause in default_clauses:
            self._templates[clause.clause_id] = clause
            self._search_index.add_clause_template(clause)
        logger.info("ClauseLibrary loaded | templates={}", len(self._templates))

    def _generate_default_clauses(self) -> List[ClauseTemplate]:
        """Generate default clause templates from legal knowledge."""
        clauses: List[ClauseTemplate] = []

        clauses.append(ClauseTemplate(
            clause_id="CL-DEF-001", clause_type="definitions", title="Standard Definitions Section",
            content=(
                '"Agreement" means this [DOCUMENT_TYPE], including all exhibits, schedules, and amendments. '
                '"Affiliate" means any entity that directly or indirectly controls, is controlled by, or is under '
                'common control with a Party. "Business Day" means any day other than a Saturday, Sunday, or federal '
                'holiday. "Confidential Information" means [see Confidentiality clause]. "Effective Date" means the '
                'date first written above. "Party" or "Parties" refers to the signatories to this Agreement. '
                '"Person" means any individual, corporation, partnership, LLC, trust, or other entity.'
            ),
            document_types=["sales_agreement", "service_agreement", "license_agreement"],
            variables=["DOCUMENT_TYPE"], word_count=85, version=1,
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-RW-001", clause_type="representations_warranties", title="Mutual Representations and Warranties",
            content=(
                "Each Party represents and warrants to the other that: (a) it is duly organized, validly existing, and in "
                "good standing under the laws of its jurisdiction of organization; (b) it has full power and authority to enter "
                "into and perform this Agreement; (c) the execution, delivery, and performance of this Agreement has been duly "
                "authorized by all necessary corporate or other action; (d) this Agreement constitutes a legal, valid, and "
                "binding obligation enforceable in accordance with its terms; (e) the execution and performance of this Agreement "
                "does not conflict with any agreement, law, or regulation to which it is subject."
            ),
            document_types=["sales_agreement", "service_agreement", "license_agreement", "merger_agreement"],
            variables=[], word_count=110, version=1,
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-IND-001", clause_type="indemnification", title="Mutual Indemnification",
            content=(
                "Each Party (the 'Indemnifying Party') shall indemnify, defend, and hold harmless the other Party and its "
                "officers, directors, employees, and agents (the 'Indemnified Parties') from and against any and all losses, "
                "damages, liabilities, costs, and expenses (including reasonable attorneys' fees) arising out of or relating to: "
                "(a) any breach of the Indemnifying Party's representations, warranties, or covenants in this Agreement; "
                "(b) the negligence or willful misconduct of the Indemnifying Party; (c) any violation of applicable law by the "
                "Indemnifying Party. The Indemnifying Party's aggregate liability under this Section shall not exceed [CAP_AMOUNT]."
            ),
            document_types=["sales_agreement", "service_agreement", "license_agreement"],
            variables=["CAP_AMOUNT"], word_count=100, version=1,
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-LOL-001", clause_type="limitation_of_liability", title="Limitation of Liability",
            content=(
                "IN NO EVENT SHALL EITHER PARTY BE LIABLE TO THE OTHER PARTY FOR ANY INDIRECT, INCIDENTAL, SPECIAL, "
                "CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT NOT LIMITED TO LOSS OF PROFITS, LOSS OF DATA, BUSINESS "
                "INTERRUPTION, OR LOSS OF GOODWILL, REGARDLESS OF THE CAUSE OF ACTION OR THE THEORY OF LIABILITY, EVEN IF "
                "SUCH PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. EACH PARTY'S TOTAL AGGREGATE LIABILITY "
                "UNDER THIS AGREEMENT SHALL NOT EXCEED [LIABILITY_CAP]. THE FOREGOING LIMITATIONS SHALL NOT APPLY TO: "
                "(A) BREACHES OF CONFIDENTIALITY OBLIGATIONS; (B) INDEMNIFICATION OBLIGATIONS; OR (C) A PARTY'S GROSS "
                "NEGLIGENCE OR WILLFUL MISCONDUCT."
            ),
            document_types=["sales_agreement", "service_agreement", "license_agreement"],
            variables=["LIABILITY_CAP"], word_count=105, version=1,
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-CONF-001", clause_type="confidentiality", title="Confidentiality Obligations",
            content=(
                'The Receiving Party shall: (a) hold all Confidential Information in strict confidence; (b) not disclose '
                'Confidential Information to any third party without the Disclosing Party\'s prior written consent; (c) use '
                'Confidential Information solely for the purposes contemplated by this Agreement; (d) limit access to '
                'Confidential Information to those employees, contractors, and advisors who have a need to know and are bound '
                'by confidentiality obligations no less restrictive than those set forth herein. Confidential Information '
                'excludes information that: (i) is or becomes publicly available without breach of this Agreement; (ii) was '
                'known to the Receiving Party prior to disclosure; (iii) is independently developed without use of Confidential '
                'Information; or (iv) is rightfully obtained from a third party without restriction.'
            ),
            document_types=["nda", "sales_agreement", "service_agreement", "employment_agreement"],
            variables=[], word_count=130, version=1,
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-TERM-001", clause_type="termination", title="Termination Provisions",
            content=(
                "This Agreement may be terminated: (a) by mutual written consent of the Parties; (b) by either Party upon "
                "[NOTICE_PERIOD] days' prior written notice to the other Party; (c) by either Party immediately upon written "
                "notice if the other Party materially breaches this Agreement and fails to cure such breach within [CURE_PERIOD] "
                "days after receiving written notice thereof; (d) by either Party immediately upon written notice if the other "
                "Party becomes insolvent, files for bankruptcy, or has a receiver appointed for its assets. Upon termination, "
                "each Party shall promptly return or destroy all Confidential Information of the other Party. Sections [SURVIVING_SECTIONS] "
                "shall survive termination."
            ),
            document_types=["sales_agreement", "service_agreement", "license_agreement", "employment_agreement"],
            variables=["NOTICE_PERIOD", "CURE_PERIOD", "SURVIVING_SECTIONS"], word_count=115, version=1,
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-DR-001", clause_type="dispute_resolution", title="Dispute Resolution - Arbitration",
            content=(
                "Any dispute arising out of or relating to this Agreement shall be resolved as follows: (a) the Parties shall "
                "first attempt to resolve the dispute through good-faith negotiation between senior executives for a period of "
                "[NEGOTIATION_PERIOD] days; (b) if negotiation fails, the dispute shall be submitted to binding arbitration "
                "administered by [ARBITRATION_BODY] under its [RULES] then in effect; (c) the arbitration shall be conducted "
                "by [NUM_ARBITRATORS] arbitrator(s) in [ARBITRATION_VENUE]; (d) the arbitrator's decision shall be final and "
                "binding and may be entered as a judgment in any court of competent jurisdiction. Notwithstanding the foregoing, "
                "either Party may seek injunctive or other equitable relief from any court of competent jurisdiction."
            ),
            document_types=["sales_agreement", "service_agreement", "license_agreement"],
            variables=["NEGOTIATION_PERIOD", "ARBITRATION_BODY", "RULES", "NUM_ARBITRATORS", "ARBITRATION_VENUE"],
            word_count=120, version=1,
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-GL-001", clause_type="governing_law", title="Governing Law and Venue",
            content=(
                "This Agreement shall be governed by and construed in accordance with the laws of the State of [GOVERNING_STATE], "
                "without regard to its conflict of laws principles. Any legal action or proceeding arising under this Agreement "
                "shall be brought exclusively in the federal or state courts located in [VENUE_COUNTY], [GOVERNING_STATE], and "
                "each Party irrevocably consents to the personal jurisdiction and venue of such courts."
            ),
            document_types=["sales_agreement", "service_agreement", "license_agreement", "employment_agreement"],
            variables=["GOVERNING_STATE", "VENUE_COUNTY"], word_count=68, version=1,
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-FM-001", clause_type="force_majeure", title="Force Majeure",
            content=(
                "Neither Party shall be liable for any failure or delay in performing its obligations under this Agreement "
                "where such failure or delay results from any cause beyond the reasonable control of the affected Party, "
                "including but not limited to acts of God, flood, fire, earthquake, epidemic, pandemic, governmental orders, "
                "war, terrorism, riot, strike, lockout, or embargo ('Force Majeure Event'). The affected Party shall provide "
                "prompt written notice of the Force Majeure Event and use commercially reasonable efforts to mitigate its "
                "impact. If a Force Majeure Event continues for more than [FM_DURATION] consecutive days, the unaffected "
                "Party may terminate this Agreement upon [FM_NOTICE] days' written notice."
            ),
            document_types=["sales_agreement", "service_agreement", "license_agreement", "lease_agreement"],
            variables=["FM_DURATION", "FM_NOTICE"], word_count=110, version=1,
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-ASG-001", clause_type="assignment", title="Assignment Clause",
            content=(
                "Neither Party may assign or transfer this Agreement or any rights or obligations hereunder without the prior "
                "written consent of the other Party, which consent shall not be unreasonably withheld, conditioned, or delayed; "
                "provided, however, that either Party may assign this Agreement without consent to an Affiliate or in connection "
                "with a merger, acquisition, or sale of all or substantially all of its assets. Any purported assignment in "
                "violation of this Section shall be null and void. This Agreement shall be binding upon and inure to the benefit "
                "of the Parties and their respective permitted successors and assigns."
            ),
            document_types=["sales_agreement", "service_agreement", "license_agreement"],
            variables=[], word_count=100, version=1,
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-NOT-001", clause_type="notices", title="Notices",
            content=(
                "All notices required or permitted under this Agreement shall be in writing and shall be deemed given: (a) when "
                "delivered personally; (b) when sent by confirmed email to the address specified below; (c) one (1) Business Day "
                "after deposit with a nationally recognized overnight courier; or (d) three (3) Business Days after being sent "
                "by registered or certified mail, return receipt requested, postage prepaid, addressed to the Party at the "
                "address set forth on the signature page or at such other address as the Party may designate by notice."
            ),
            document_types=["sales_agreement", "service_agreement", "license_agreement", "lease_agreement"],
            variables=[], word_count=95, version=1,
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-SEV-001", clause_type="severability", title="Severability",
            content=(
                "If any provision of this Agreement is held by a court of competent jurisdiction to be invalid, illegal, or "
                "unenforceable, such provision shall be modified to the minimum extent necessary to make it valid, legal, and "
                "enforceable while preserving its original intent. If such modification is not possible, the provision shall be "
                "severed from this Agreement. The invalidity of any provision shall not affect the validity or enforceability "
                "of any other provision of this Agreement."
            ),
            document_types=["sales_agreement", "service_agreement", "license_agreement", "employment_agreement"],
            variables=[], word_count=78, version=1,
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-EA-001", clause_type="entire_agreement", title="Entire Agreement / Integration",
            content=(
                "This Agreement, including all exhibits and schedules attached hereto, constitutes the entire agreement between "
                "the Parties with respect to the subject matter hereof and supersedes all prior and contemporaneous agreements, "
                "understandings, negotiations, and discussions, whether oral or written, between the Parties relating to the "
                "subject matter hereof. No amendment to or modification of this Agreement shall be effective unless in writing "
                "and signed by both Parties."
            ),
            document_types=["sales_agreement", "service_agreement", "license_agreement", "employment_agreement"],
            variables=[], word_count=72, version=1,
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-CP-001", clause_type="counterparts", title="Counterparts and Electronic Execution",
            content=(
                "This Agreement may be executed in any number of counterparts, each of which shall be deemed an original, and "
                "all of which together shall constitute one and the same instrument. Signatures transmitted by electronic means "
                "(including PDF, DocuSign, or similar electronic signature platforms) shall be deemed original signatures for "
                "all purposes and shall have the same legal effect as original ink signatures."
            ),
            document_types=["sales_agreement", "service_agreement", "license_agreement", "employment_agreement"],
            variables=[], word_count=65, version=1,
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-NC-001", clause_type="non_compete", title="Non-Competition Covenant",
            content=(
                "During the term of employment and for a period of [NC_DURATION] following the termination of employment for "
                "any reason, Employee shall not, directly or indirectly, engage in, own, manage, operate, control, or participate "
                "in any business that competes with the Company's business within a [NC_GEOGRAPHIC] radius of any office of the "
                "Company at which Employee worked during the last [NC_LOOKBACK] months of employment. Employee acknowledges that "
                "this restriction is reasonable and necessary to protect the Company's legitimate business interests, including "
                "trade secrets, confidential information, and customer relationships."
            ),
            document_types=["employment_agreement", "non_compete"],
            variables=["NC_DURATION", "NC_GEOGRAPHIC", "NC_LOOKBACK"],
            word_count=98, version=1, jurisdiction="",
        ))

        clauses.append(ClauseTemplate(
            clause_id="CL-SUR-001", clause_type="survival", title="Survival Clause",
            content=(
                "The following provisions shall survive the expiration or termination of this Agreement: [SURVIVING_SECTIONS_LIST]. "
                "Any provision that by its nature or express terms should survive shall continue in full force and effect after "
                "termination or expiration of this Agreement."
            ),
            document_types=["sales_agreement", "service_agreement", "license_agreement"],
            variables=["SURVIVING_SECTIONS_LIST"], word_count=45, version=1,
        ))

        return clauses

    def get_clause(self, clause_id: str) -> Optional[ClauseTemplate]:
        return self._templates.get(clause_id)

    def search_clauses(self, query: str, clause_type: str = "", jurisdiction: str = "", top_k: int = 5) -> List[TemplateMatchResult]:
        return self._search_index.match_templates(query=query, clause_type=clause_type, jurisdiction=jurisdiction, top_k=top_k)

    def get_clauses_by_type(self, clause_type: str) -> List[ClauseTemplate]:
        return [t for t in self._templates.values() if t.clause_type == clause_type]

    def get_all_types(self) -> List[str]:
        return sorted(set(t.clause_type for t in self._templates.values()))

    def get_stats(self) -> Dict[str, Any]:
        type_counts: Dict[str, int] = defaultdict(int)
        for t in self._templates.values():
            type_counts[t.clause_type] += 1
        return {"total_templates": len(self._templates), "by_type": dict(type_counts)}


# ############################################################################
#
# SECTION 13: DOCUMENT VERSION TRACKER
#
# ############################################################################


class DocumentVersionTracker:
    """Tracks document versions with content hashing."""

    def __init__(self) -> None:
        self._versions: Dict[str, List[DocumentVersion]] = defaultdict(list)

    def create_version(self, document_id: str, content: str, author: str = "", comment: str = "") -> DocumentVersion:
        existing = self._versions.get(document_id, [])
        version_num = len(existing) + 1
        content_hash = compute_content_hash(content)
        version = DocumentVersion(
            version_id=str(uuid.uuid4()),
            document_id=document_id,
            version_number=version_num,
            content_hash=content_hash,
            author=author,
            comment=comment,
            timestamp=datetime.now(timezone.utc).isoformat(),
            word_count=len(content.split()),
        )
        self._versions[document_id].append(version)
        return version

    def get_versions(self, document_id: str) -> List[DocumentVersion]:
        return self._versions.get(document_id, [])

    def get_latest(self, document_id: str) -> Optional[DocumentVersion]:
        versions = self._versions.get(document_id, [])
        return versions[-1] if versions else None

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_documents": len(self._versions),
            "total_versions": sum(len(v) for v in self._versions.values()),
        }


# ############################################################################
#
# SECTION 14: COMPLIANCE CHECKER
#
# ############################################################################


class ComplianceChecker:
    """Checks document content against regulatory and legal requirements."""

    COMPLIANCE_RULES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "statute_of_frauds": {
            "applies_to": ["real_estate", "sales_agreement", "employment_agreement", "guaranty"],
            "checks": [
                {"name": "writing_requirement", "pattern": r"(agreement|contract|deed)", "required": True},
                {"name": "signature_block", "pattern": r"(signature|signed|executed)", "required": True},
                {"name": "party_identification", "pattern": r"(party|parties|buyer|seller|grantor|grantee)", "required": True},
            ],
        },
        "ucc_article_2": {
            "applies_to": ["sales_agreement", "supply_agreement"],
            "checks": [
                {"name": "goods_identification", "pattern": r"(goods|products|merchandise|inventory)", "required": True},
                {"name": "price_terms", "pattern": r"(price|purchase price|consideration|payment)", "required": True},
                {"name": "delivery_terms", "pattern": r"(delivery|ship|FOB|freight)", "required": True},
                {"name": "warranty_provisions", "pattern": r"(warrant|merchantab|fitness|AS IS)", "required": False},
            ],
        },
        "gdpr": {
            "applies_to": ["privacy_policy", "terms_of_service"],
            "checks": [
                {"name": "lawful_basis", "pattern": r"(lawful basis|legitimate interest|consent|contract)", "required": True},
                {"name": "data_subject_rights", "pattern": r"(right to access|right to erasure|portability|rectification)", "required": True},
                {"name": "data_retention", "pattern": r"(retention|retain|storage period|delete)", "required": True},
                {"name": "breach_notification", "pattern": r"(breach|notification|72 hours|supervisory authority)", "required": True},
            ],
        },
        "employment_law": {
            "applies_to": ["employment_agreement", "offer_letter"],
            "checks": [
                {"name": "at_will_statement", "pattern": r"(at.will|at will|no guarantee)", "required": True},
                {"name": "compensation", "pattern": r"(salary|wage|compensation|pay|remuneration)", "required": True},
                {"name": "position_description", "pattern": r"(position|title|role|duties|responsibilities)", "required": True},
            ],
        },
    }

    def check_compliance(self, content: str, document_type: str = "", jurisdiction: str = "", regulations: Optional[List[str]] = None) -> ComplianceResult:
        content_lower = content.lower()
        issues: List[str] = []
        recommendations: List[str] = []
        checked: List[str] = []
        total_checks = 0
        passed_checks = 0

        applicable_rules = regulations or list(self.COMPLIANCE_RULES.keys())

        for rule_name in applicable_rules:
            rule = self.COMPLIANCE_RULES.get(rule_name)
            if not rule:
                continue
            if document_type and document_type not in rule["applies_to"]:
                continue

            checked.append(rule_name)
            for check in rule["checks"]:
                total_checks += 1
                pattern = check["pattern"]
                found = bool(re.search(pattern, content_lower, re.IGNORECASE))
                if found:
                    passed_checks += 1
                elif check["required"]:
                    issues.append(f"[{rule_name}] Missing required element: {check['name']}")
                    recommendations.append(f"Add {check['name'].replace('_', ' ')} provisions to comply with {rule_name}")
                else:
                    recommendations.append(f"Consider adding {check['name'].replace('_', ' ')} for {rule_name} compliance")

        score = passed_checks / total_checks if total_checks > 0 else 1.0
        compliant = len(issues) == 0

        return ComplianceResult(
            compliant=compliant,
            score=round(score, 4),
            issues=issues,
            recommendations=recommendations,
            checked_regulations=checked,
        )


# ############################################################################
#
# SECTION 15: ZONED ANALYSIS
#
# ############################################################################


def determine_analysis_zone(
    document_type: str,
    domain: DocumentDomain,
    query: str,
) -> AnalysisZone:
    """Determine the analysis zone based on document type and domain."""
    zone_map: Dict[str, AnalysisZone] = {
        "contract": AnalysisZone.CONTRACT_FORMATION,
        "sales_agreement": AnalysisZone.UCC_COMPLIANCE,
        "supply_agreement": AnalysisZone.UCC_COMPLIANCE,
        "deed": AnalysisZone.REAL_ESTATE,
        "mortgage": AnalysisZone.REAL_ESTATE,
        "lease_agreement": AnalysisZone.REAL_ESTATE,
        "purchase_agreement": AnalysisZone.REAL_ESTATE,
        "employment_agreement": AnalysisZone.EMPLOYMENT,
        "offer_letter": AnalysisZone.EMPLOYMENT,
        "non_compete": AnalysisZone.EMPLOYMENT,
        "independent_contractor": AnalysisZone.EMPLOYMENT,
        "articles_of_incorporation": AnalysisZone.CORPORATE,
        "bylaws": AnalysisZone.CORPORATE,
        "operating_agreement": AnalysisZone.CORPORATE,
        "board_resolution": AnalysisZone.CORPORATE,
        "shareholder_agreement": AnalysisZone.CORPORATE,
        "patent_assignment": AnalysisZone.IP_RIGHTS,
        "software_license": AnalysisZone.IP_RIGHTS,
        "trademark_license": AnalysisZone.IP_RIGHTS,
        "promissory_note": AnalysisZone.FINANCE,
        "loan_agreement": AnalysisZone.FINANCE,
        "security_agreement": AnalysisZone.FINANCE,
        "guaranty": AnalysisZone.FINANCE,
        "revocable_trust": AnalysisZone.ESTATE_PLANNING,
        "last_will": AnalysisZone.ESTATE_PLANNING,
        "power_of_attorney": AnalysisZone.ESTATE_PLANNING,
        "merger_agreement": AnalysisZone.MA_TRANSACTION,
        "asset_purchase_agreement": AnalysisZone.MA_TRANSACTION,
        "privacy_policy": AnalysisZone.REGULATORY,
        "terms_of_service": AnalysisZone.REGULATORY,
    }

    if document_type in zone_map:
        return zone_map[document_type]

    domain_zone_map: Dict[DocumentDomain, AnalysisZone] = {
        DocumentDomain.CONTRACT: AnalysisZone.CONTRACT_FORMATION,
        DocumentDomain.REAL_ESTATE: AnalysisZone.REAL_ESTATE,
        DocumentDomain.EMPLOYMENT: AnalysisZone.EMPLOYMENT,
        DocumentDomain.CORPORATE: AnalysisZone.CORPORATE,
        DocumentDomain.INTELLECTUAL_PROPERTY: AnalysisZone.IP_RIGHTS,
        DocumentDomain.FINANCE: AnalysisZone.FINANCE,
        DocumentDomain.ESTATE_PLANNING: AnalysisZone.ESTATE_PLANNING,
        DocumentDomain.REGULATORY: AnalysisZone.REGULATORY,
    }

    return domain_zone_map.get(domain, AnalysisZone.GENERAL)


# ############################################################################
#
# SECTION 16: MULTI-DOCTRINE DECOMPOSITION
#
# ############################################################################


def decompose_multi_doctrine(
    query: str,
    document_type: str,
    normalization: NormalizationResult,
    doctrine_engine: LegalDocumentDoctrineEngine,
) -> List[DoctrineResponse]:
    """Decompose a complex query into multiple relevant doctrines."""
    results: List[DoctrineResponse] = []
    seen_ids: Set[str] = set()

    if document_type:
        coverage_map = DoctrineCoverageMap()
        coverage = coverage_map.get_coverage(document_type)
        for topic in coverage.get("covered", []):
            resp = doctrine_engine.get_by_topic(topic)
            if resp and resp.doctrine_id not in seen_ids:
                results.append(resp)
                seen_ids.add(resp.doctrine_id)

    for cat in normalization.detected_clause_categories:
        tag_results = doctrine_engine.get_by_tag(cat.replace("_", " "))
        for resp in tag_results:
            if resp.doctrine_id not in seen_ids:
                results.append(resp)
                seen_ids.add(resp.doctrine_id)

    if normalization.detected_domain != DocumentDomain.GENERAL:
        domain_map = {
            DocumentDomain.CONTRACT: "contract_formation",
            DocumentDomain.REAL_ESTATE: "real_estate",
            DocumentDomain.EMPLOYMENT: "employment",
            DocumentDomain.CORPORATE: "corporate",
            DocumentDomain.INTELLECTUAL_PROPERTY: "intellectual_property",
            DocumentDomain.FINANCE: "finance",
            DocumentDomain.ESTATE_PLANNING: "estate_planning",
            DocumentDomain.REGULATORY: "regulatory",
        }
        domain_key = domain_map.get(normalization.detected_domain, "")
        if domain_key:
            domain_results = doctrine_engine.get_by_domain(domain_key)
            for resp in domain_results:
                if resp.doctrine_id not in seen_ids:
                    results.append(resp)
                    seen_ids.add(resp.doctrine_id)

    if len(results) < 3:
        search_results = doctrine_engine.search_doctrines(query, top_k=5)
        for resp in search_results:
            if resp.doctrine_id not in seen_ids:
                results.append(resp)
                seen_ids.add(resp.doctrine_id)

    return results[:10]


# ############################################################################
#
# SECTION 17: THREE-LAYER RESPONSE BUILDER
#
# ############################################################################


def build_three_layer_response(
    query: str,
    document_type: str,
    jurisdiction: str,
    mode: ResponseMode,
    doctrines: List[DoctrineResponse],
    clauses: List[TemplateMatchResult],
    normalization: NormalizationResult,
    zone: AnalysisZone,
    include_deep: bool = False,
) -> ThreeLayerResponse:
    """Build a three-layer response (summary/analysis/deep_dive)."""

    # SUMMARY
    summary_parts: List[str] = []
    if document_type:
        summary_parts.append(f"Document Type: {document_type.replace('_', ' ').title()}")
    if jurisdiction:
        summary_parts.append(f"Jurisdiction: {jurisdiction}")
    summary_parts.append(f"Analysis Zone: {zone.value.replace('_', ' ').title()}")
    summary_parts.append(f"Response Mode: {mode.value}")
    if doctrines:
        summary_parts.append(f"Relevant Doctrines: {len(doctrines)}")
        doctrine_titles = [d.title for d in doctrines[:5]]
        summary_parts.append(f"Key Topics: {', '.join(doctrine_titles)}")
    if clauses:
        summary_parts.append(f"Matching Clause Templates: {len(clauses)}")

    summary = " | ".join(summary_parts)

    # ANALYSIS
    analysis_sections: List[str] = []

    if doctrines:
        analysis_sections.append("=== APPLICABLE LEGAL DOCTRINES ===")
        for i, doctrine in enumerate(doctrines[:7], 1):
            analysis_sections.append(f"\n[{i}] {doctrine.title} ({doctrine.doctrine_id})")
            analysis_sections.append(f"    Domain: {doctrine.domain}")
            analysis_sections.append(f"    Confidence: {doctrine.confidence} ({doctrine.confidence_score:.0%})")
            analysis_sections.append(f"    Summary: {doctrine.summary}")
            if doctrine.key_elements:
                analysis_sections.append(f"    Key Elements: {', '.join(doctrine.key_elements)}")

    if clauses:
        analysis_sections.append("\n=== RECOMMENDED CLAUSE TEMPLATES ===")
        for i, match in enumerate(clauses[:5], 1):
            t = match.template
            analysis_sections.append(f"\n[{i}] {t.title} ({t.clause_id})")
            analysis_sections.append(f"    Type: {t.clause_type}")
            analysis_sections.append(f"    Match Score: {match.match_score:.4f}")
            if t.variables:
                analysis_sections.append(f"    Variables: {', '.join(t.variables)}")
            analysis_sections.append(f"    Content Preview: {t.content[:200]}...")

    if normalization.detected_clause_categories:
        analysis_sections.append(f"\n=== DETECTED CLAUSE CATEGORIES ===")
        analysis_sections.append(f"Categories: {', '.join(normalization.detected_clause_categories)}")

    analysis = "\n".join(analysis_sections) if analysis_sections else "No relevant analysis generated for this query."

    # DEEP DIVE
    deep_dive = ""
    if include_deep and doctrines:
        deep_parts: List[str] = ["=== DEEP ANALYSIS ==="]
        for doctrine in doctrines[:5]:
            deep_parts.append(f"\n--- {doctrine.title} ---")
            deep_parts.append(doctrine.content)
        deep_dive = "\n".join(deep_parts)

    return ThreeLayerResponse(summary=summary, analysis=analysis, deep_dive=deep_dive)


# ############################################################################
#
# SECTION 18: DEEP ANALYSIS MODE
#
# ############################################################################


def perform_deep_analysis(
    query: str,
    document_type: str,
    jurisdiction: str,
    doctrines: List[DoctrineResponse],
    clauses: List[TemplateMatchResult],
) -> str:
    """Perform deep analysis combining multiple doctrine sources."""
    sections: List[str] = []

    sections.append("=" * 60)
    sections.append("DEEP ANALYSIS REPORT")
    sections.append(f"Query: {query}")
    sections.append(f"Document Type: {document_type or 'Not specified'}")
    sections.append(f"Jurisdiction: {jurisdiction or 'Not specified'}")
    sections.append("=" * 60)

    if doctrines:
        sections.append("\n## DOCTRINE SYNTHESIS")
        for doctrine in doctrines:
            sections.append(f"\n### {doctrine.title}")
            sections.append(f"ID: {doctrine.doctrine_id} | Domain: {doctrine.domain}")
            sections.append(f"Confidence: {doctrine.confidence} ({doctrine.confidence_score:.0%})")
            sections.append(f"\n{doctrine.content}")
            if doctrine.key_elements:
                sections.append(f"\nKey Elements: {', '.join(doctrine.key_elements)}")

    if clauses:
        sections.append("\n## CLAUSE TEMPLATE ANALYSIS")
        for match in clauses:
            t = match.template
            sections.append(f"\n### {t.title} (Score: {match.match_score:.4f})")
            sections.append(f"Type: {t.clause_type}")
            sections.append(f"\n{t.content}")

    sections.append("\n## DRAFTING RECOMMENDATIONS")
    if document_type:
        coverage_map = DoctrineCoverageMap()
        coverage = coverage_map.get_coverage(document_type)
        if coverage.get("gaps"):
            sections.append(f"\nCoverage Gaps: {', '.join(coverage['gaps'])}")
            sections.append("These topics should be addressed in the document but have no doctrine coverage.")
        sections.append(f"\nDoctrine Coverage: {coverage.get('coverage', 0):.0%}")

    sections.append(f"\n{'=' * 60}")
    sections.append("END OF DEEP ANALYSIS REPORT")

    return "\n".join(sections)


# ############################################################################
#
# SECTION 19: CORE QUERY PROCESSOR
#
# ############################################################################


def process_draft_query(
    request: DraftRequest,
    doctrine_engine: LegalDocumentDoctrineEngine,
    clause_library: ClauseLibrary,
    compliance_checker: ComplianceChecker,
    drift_watcher: DoctrineDriftWatcher,
    version_tracker: DocumentVersionTracker,
    metrics: MetricsCollector,
) -> DraftResponse:
    """Process a complete draft request through all engine components."""
    start_time = time.time()

    enforce_authority(request.authority_level)

    trace = trace_query(
        query_text=request.query,
        document_type=request.document_type,
        jurisdiction=request.jurisdiction,
        response_mode=request.mode.value,
        authority_level=request.authority_level,
    )

    try:
        # Step 1: Semantic normalization
        step_norm = trace.add_step("semantic_normalization")
        norm_result = normalize_query(request.query)
        doc_type = request.document_type or norm_result.detected_document_type
        jurisdiction = request.jurisdiction or norm_result.detected_jurisdiction
        step_norm.complete({"domain": norm_result.detected_domain.value, "doc_type": doc_type})

        # Step 2: Determine analysis zone
        step_zone = trace.add_step("zone_analysis")
        zone = determine_analysis_zone(doc_type, norm_result.detected_domain, request.query)
        step_zone.complete({"zone": zone.value})

        # Step 3: Multi-doctrine decomposition
        step_doctrine = trace.add_step("doctrine_decomposition", ResponseLayer.CACHE_HIT)
        doctrines = decompose_multi_doctrine(request.query, doc_type, norm_result, doctrine_engine)
        step_doctrine.complete({"doctrine_count": len(doctrines)})

        # Step 4: Clause search
        step_clauses = trace.add_step("clause_search", ResponseLayer.SEARCH_HIT)
        clause_results = clause_library.search_clauses(
            query=request.query,
            clause_type=request.clause_types[0] if request.clause_types else "",
            jurisdiction=jurisdiction,
            top_k=request.max_results,
        )
        step_clauses.complete({"clause_matches": len(clause_results)})

        # Step 5: Drift checking
        step_drift = trace.add_step("drift_check")
        drift_warnings: List[DriftStatus] = []
        for doctrine in doctrines:
            drift_status = drift_watcher.check_doctrine(doctrine.doctrine_id)
            if drift_status and drift_status.drift_detected:
                drift_warnings.append(drift_status)
                doctrine.confidence_score = drift_watcher.apply_confidence_adjustment(
                    doctrine.doctrine_id, doctrine.confidence_score
                )
        step_drift.complete({"drift_warnings": len(drift_warnings)})

        # Step 6: Build three-layer response
        step_response = trace.add_step("response_build", ResponseLayer.ASSEMBLY)
        three_layer = build_three_layer_response(
            query=request.query,
            document_type=doc_type,
            jurisdiction=jurisdiction,
            mode=request.mode,
            doctrines=doctrines,
            clauses=clause_results,
            normalization=norm_result,
            zone=zone,
            include_deep=request.include_deep_analysis,
        )

        if request.include_deep_analysis:
            three_layer.deep_dive = perform_deep_analysis(
                query=request.query,
                document_type=doc_type,
                jurisdiction=jurisdiction,
                doctrines=doctrines,
                clauses=clause_results,
            )
        step_response.complete()

        # Step 7: Compliance check
        compliance_result = None
        if request.include_compliance_check and three_layer.analysis:
            step_compliance = trace.add_step("compliance_check")
            compliance_result = compliance_checker.check_compliance(
                content=three_layer.analysis,
                document_type=doc_type,
                jurisdiction=jurisdiction,
            )
            step_compliance.complete({"compliant": compliance_result.compliant, "score": compliance_result.score})

        # Step 8: Fact fragility
        step_fragility = trace.add_step("fact_fragility")
        fragility = assess_fact_fragility(three_layer.analysis, doc_type, jurisdiction)
        step_fragility.complete({"fragility_score": fragility.overall_score})

        # Step 9: Confidence computation
        confidence_score = compute_confidence(
            doctrine_hits=len(doctrines),
            search_score=clause_results[0].match_score if clause_results else 0.0,
            normalization_confidence=norm_result.confidence,
            jurisdiction_matched=bool(jurisdiction),
            document_type_matched=bool(doc_type),
        )
        confidence_band = stratify_confidence(confidence_score)

        # Step 10: Epistemic guardrails
        cleaned_analysis, violations = apply_epistemic_guardrails(three_layer.analysis)
        three_layer.analysis = cleaned_analysis
        disclaimers = get_required_disclaimers(confidence_band)

        # Step 11: Determinism hash
        det_hash = compute_determinism_hash(
            query=request.query,
            document_type=doc_type,
            jurisdiction=jurisdiction,
            mode=request.mode.value,
            response_content=three_layer.analysis,
        )

        elapsed_ms = (time.time() - start_time) * 1000.0

        # Complete trace
        complete_trace(
            trace=trace,
            result_layer=ResponseLayer.ASSEMBLY,
            confidence=confidence_score,
            clause_count=len(clause_results),
            determinism_hash=det_hash,
            was_cache_hit=len(doctrines) > 0,
        )

        # Record metrics
        metrics.record_request(
            mode=request.mode.value,
            doc_type=doc_type,
            jurisdiction=jurisdiction,
            latency_ms=elapsed_ms,
            clauses=len(clause_results),
        )

        # Audit trail
        write_audit_entry({
            "event": "draft_query",
            "trace_id": trace.trace_id,
            "query_hash": compute_query_hash(request.query),
            "document_type": doc_type,
            "jurisdiction": jurisdiction,
            "mode": request.mode.value,
            "doctrines_used": len(doctrines),
            "clauses_matched": len(clause_results),
            "confidence": confidence_score,
            "duration_ms": elapsed_ms,
            "determinism_hash": det_hash,
        })

        return DraftResponse(
            trace_id=trace.trace_id,
            query=request.query,
            document_type=doc_type,
            jurisdiction=jurisdiction,
            mode=request.mode.value,
            authority_level=request.authority_level,
            response=three_layer,
            doctrines_used=[d.doctrine_id for d in doctrines],
            clauses_generated=len(clause_results),
            confidence=confidence_band,
            confidence_score=round(confidence_score, 4),
            compliance=compliance_result,
            fact_fragility=fragility,
            drift_warnings=drift_warnings,
            normalization=norm_result.model_dump(),
            determinism_hash=det_hash,
            duration_ms=round(elapsed_ms, 2),
            disclaimers=disclaimers,
        )

    except HTTPException:
        raise
    except Exception as exc:
        elapsed_ms = (time.time() - start_time) * 1000.0
        log_error(ErrorDomain.DOCUMENT_ASSEMBLY, str(exc), trace_id=trace.trace_id)
        metrics.record_request(
            mode=request.mode.value,
            doc_type=request.document_type,
            jurisdiction=request.jurisdiction,
            latency_ms=elapsed_ms,
            clauses=0,
            error=True,
        )
        write_audit_entry({
            "event": "draft_error",
            "trace_id": trace.trace_id,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        })
        raise HTTPException(status_code=500, detail=f"Engine error: {str(exc)}")


# ############################################################################
#
# SECTION 20: FASTAPI APPLICATION
#
# ############################################################################

# Singletons
_doctrine_engine: Optional[LegalDocumentDoctrineEngine] = None
_clause_library: Optional[ClauseLibrary] = None
_compliance_checker: Optional[ComplianceChecker] = None
_drift_watcher: Optional[DoctrineDriftWatcher] = None
_version_tracker: Optional[DocumentVersionTracker] = None
_metrics_collector: Optional[MetricsCollector] = None
_coverage_map: Optional[DoctrineCoverageMap] = None
_boot_time: float = 0.0


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown."""
    global _doctrine_engine, _clause_library, _compliance_checker
    global _drift_watcher, _version_tracker, _metrics_collector, _coverage_map, _boot_time

    _boot_time = time.time()
    logger.info("LG04 Legal Document Draft Engine starting | port={}", ENGINE_PORT)

    _doctrine_engine = get_doctrine_engine()
    _clause_library = ClauseLibrary()
    _compliance_checker = ComplianceChecker()
    _drift_watcher = DoctrineDriftWatcher()
    _version_tracker = DocumentVersionTracker()
    _metrics_collector = MetricsCollector()
    _coverage_map = DoctrineCoverageMap()

    search_idx = get_search_index()
    for doctrine_id, block in DOCTRINE_CACHE.items():
        search_idx.add_document(
            doc_id=doctrine_id,
            title=block.title,
            content=block.content,
            category="doctrine",
            jurisdiction="",
            document_type=",".join(block.applicable_document_types),
        )

    telemetry = get_telemetry()
    telemetry.record_audit_event("engine_start", metadata={"engine_id": ENGINE_ID, "version": ENGINE_VERSION, "port": ENGINE_PORT})

    logger.info(
        "LG04 engine ready | doctrines={} clause_templates={} search_docs={}",
        len(DOCTRINE_CACHE),
        len(_clause_library._templates),
        search_idx.get_stats()["total_documents"],
    )

    yield

    telemetry = get_telemetry()
    telemetry.record_audit_event("engine_stop", metadata={"uptime_seconds": time.time() - _boot_time})
    telemetry.stop()
    logger.info("LG04 engine shut down")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="TIE-20 compliant legal document drafting engine",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ENGINE_CONFIG.get("cors", {}).get("allow_origins", ["*"]),
    allow_credentials=True,
    allow_methods=ENGINE_CONFIG.get("cors", {}).get("allow_methods", ["*"]),
    allow_headers=ENGINE_CONFIG.get("cors", {}).get("allow_headers", ["*"]),
)


# --- ROUTES ---


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health endpoint returning engine status."""
    search_idx = get_search_index()
    telemetry = get_telemetry()
    return HealthResponse(
        status="healthy",
        total_doctrines=len(DOCTRINE_CACHE),
        total_clause_templates=len(_clause_library._templates) if _clause_library else 0,
        search_index_docs=search_idx.get_stats()["total_documents"],
        semantic_map_version=get_semantic_map_version(),
        semantic_map_hash=get_semantic_map_hash(),
        telemetry_status="running" if telemetry._running else "stopped",
        uptime_seconds=round(time.time() - _boot_time, 2) if _boot_time else 0.0,
    )


@app.post("/draft", response_model=DraftResponse)
async def draft_document(request: DraftRequest):
    """Main endpoint: draft a legal document or query the engine."""
    return process_draft_query(
        request=request,
        doctrine_engine=_doctrine_engine,
        clause_library=_clause_library,
        compliance_checker=_compliance_checker,
        drift_watcher=_drift_watcher,
        version_tracker=_version_tracker,
        metrics=_metrics_collector,
    )


@app.post("/clauses/search")
async def search_clauses(request: ClauseRequest):
    """Search the clause library."""
    enforce_authority(5.0)
    results = _clause_library.search_clauses(
        query=request.query,
        clause_type=request.clause_type,
        jurisdiction=request.jurisdiction,
        top_k=request.top_k,
    )
    return {"results": [{"template": r.template.model_dump(), "match_score": r.match_score} for r in results]}


@app.get("/clauses/types")
async def list_clause_types():
    """List all available clause types."""
    return {"clause_types": _clause_library.get_all_types(), "stats": _clause_library.get_stats()}


@app.get("/clauses/{clause_id}")
async def get_clause(clause_id: str):
    """Get a specific clause template."""
    clause = _clause_library.get_clause(clause_id)
    if not clause:
        raise HTTPException(status_code=404, detail=f"Clause {clause_id} not found")
    return clause.model_dump()


@app.post("/compliance/check", response_model=ComplianceResult)
async def check_compliance(request: ComplianceCheckRequest):
    """Check document compliance against regulations."""
    enforce_authority(5.0)
    return _compliance_checker.check_compliance(
        content=request.document_content,
        document_type=request.document_type,
        jurisdiction=request.jurisdiction,
        regulations=request.regulations or None,
    )


@app.get("/doctrines")
async def list_doctrines(domain: str = "", topic: str = "", tag: str = ""):
    """List doctrines with optional filtering."""
    engine = _doctrine_engine
    if topic:
        result = engine.get_by_topic(topic)
        return {"doctrines": [result.model_dump()] if result else []}
    if domain:
        results = engine.get_by_domain(domain)
        return {"doctrines": [r.model_dump() for r in results]}
    if tag:
        results = engine.get_by_tag(tag)
        return {"doctrines": [r.model_dump() for r in results]}
    return {"stats": engine.get_stats(), "topics": engine.get_all_topics(), "domains": engine.get_all_domains()}


@app.get("/doctrines/{doctrine_id}")
async def get_doctrine(doctrine_id: str):
    """Get a specific doctrine by ID."""
    result = _doctrine_engine.get_by_id(doctrine_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Doctrine {doctrine_id} not found")
    return result.model_dump()


@app.get("/coverage")
async def get_coverage(document_type: str = ""):
    """Get doctrine coverage map for document types."""
    if document_type:
        return _coverage_map.get_coverage(document_type)
    return _coverage_map.get_all_coverage()


@app.get("/drift")
async def get_drift_status(stale_only: bool = False):
    """Get doctrine drift watcher status."""
    if stale_only:
        return {"stale_doctrines": [ds.model_dump() for ds in _drift_watcher.get_stale_doctrines()]}
    return {"all_doctrines": [ds.model_dump() for ds in _drift_watcher.get_all_status()]}


@app.post("/versions/create")
async def create_version(request: VersionRequest):
    """Create a new document version."""
    enforce_authority(5.0)
    version = _version_tracker.create_version(
        document_id=request.document_id,
        content=request.content,
        author=request.author,
        comment=request.comment,
    )
    write_audit_entry({"event": "version_created", "document_id": request.document_id, "version": version.version_number})
    return version.model_dump()


@app.get("/versions/{document_id}")
async def get_versions(document_id: str):
    """Get all versions of a document."""
    versions = _version_tracker.get_versions(document_id)
    return {"document_id": document_id, "versions": [v.model_dump() for v in versions]}


@app.get("/metrics")
async def get_metrics():
    """Get engine performance metrics."""
    telemetry = get_telemetry()
    return {
        "engine_metrics": _metrics_collector.get_summary(),
        "telemetry_metrics": telemetry.get_metrics_snapshot().model_dump(),
        "search_stats": get_search_index().get_stats(),
        "version_stats": _version_tracker.get_stats(),
    }


@app.get("/semantic/map")
async def get_semantic_map_endpoint():
    """Get the semantic dictionary map."""
    sem_map = get_semantic_map()
    return {"version": get_semantic_map_version(), "total_terms": len(sem_map), "terms": {k: v.model_dump() for k, v in sem_map.items()}}


@app.get("/semantic/governance")
async def get_semantic_governance_endpoint():
    """Get semantic dictionary governance metadata."""
    return get_semantic_governance().model_dump()


@app.get("/semantic/verify")
async def verify_semantic_integrity():
    """Verify semantic dictionary integrity."""
    valid, message = verify_dictionary_integrity()
    return {"valid": valid, "message": message}


@app.post("/normalize")
async def normalize_endpoint(query: str = Query(..., min_length=1)):
    """Normalize a query through the semantic pipeline."""
    result = normalize_query(query)
    return result.model_dump()


@app.get("/audit/chain")
async def verify_audit_chain():
    """Verify the integrity of the audit trail hash chain."""
    telemetry = get_telemetry()
    valid, valid_count, invalid_count = telemetry.verify_audit_chain()
    return {"valid": valid, "valid_entries": valid_count, "invalid_entries": invalid_count}


@app.get("/audit/recent")
async def get_recent_audit(limit: int = Query(50, ge=1, le=500)):
    """Get recent audit entries from telemetry."""
    telemetry = get_telemetry()
    return {"traces": telemetry.get_recent_traces(limit=limit)}


@app.get("/search")
async def search_index(
    query: str = Query(..., min_length=1),
    top_k: int = Query(5, ge=1, le=50),
    category: str = "",
    jurisdiction: str = "",
    document_type: str = "",
    clause_type: str = "",
):
    """Search the full-text index."""
    search_idx = get_search_index()
    result = search_idx.search(
        query=query,
        top_k=top_k,
        category_filter=category,
        jurisdiction_filter=jurisdiction,
        document_type_filter=document_type,
        clause_type_filter=clause_type,
    )
    return result.model_dump()


@app.get("/config")
async def get_config():
    """Get engine configuration (non-sensitive)."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "authority_level": ENGINE_AUTHORITY,
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "response_modes": list(ResponseMode),
        "confidence_bands": {k.value: v for k, v in CONFIDENCE_THRESHOLDS.items()},
        "document_types": ENGINE_CONFIG.get("document_types", {}),
        "jurisdictions": list(ENGINE_CONFIG.get("jurisdictions", {}).get("states", {}).keys()),
    }


# ############################################################################
#
# SECTION 21: MAIN ENTRY POINT
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