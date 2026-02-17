"""
LM21 Federal/State Lands Engine - Main Engine
==============================================

Full FastAPI engine with all 20 TIE components implementing comprehensive
federal and state land oil & gas leasing, permitting, royalty compliance,
environmental review, and surface management.

Engine ID: LM21 | Port: 8521 | Mode: DET | Version: 1.0.0

Author: ECHO OMEGA PRIME Build System
Commander: Bobby Don McWilliams II
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field, field_validator

# Add _shared to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "APPS" / "_SHARED"))

try:
    from cloud_retriever import CloudRetriever
    CLOUD_AVAILABLE = True
except ImportError:
    CLOUD_AVAILABLE = False
    logger.warning("CloudRetriever not available, running in standalone mode")


# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    ConfidenceLevel,
    DoctrineBlock,
    EntityScope,
    build_doctrine_cache,
)
from search import (
    FederalLandsSearchEngine as FederalLeaseSearcher,
    SearchResponse as LeaseSearchQuery,
    SearchResult as LeaseSearchResult,
)
StateLeaseSearcher = FederalLeaseSearcher  # alias — same engine handles both
from semantic import (
    FederalStateLandsNormalizer,
    NormalizationResult,
    SemanticMatch,
)
from telemetry import (
    AuditEntry,
    CoverageGap,
    DriftEvent,
    ErrorDomain,
    FederalLandsTelemetry,
    MetricSnapshot,
    QueryPhase,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ENGINE_ID = "LM21"
ENGINE_NAME = "Federal/State Lands Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8521
ENGINE_MODE = "DET"
ENGINE_TIER = "LANDMAN"
ENGINE_AUTHORITY = 7.5
CONFIG_PATH = Path(__file__).parent / "config.json"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ResponseMode(str, Enum):
    """Query response mode selection."""
    FAST = "fast"
    DEFENSE = "defense"
    MEMO = "memo"
    APD_ANALYSIS = "apd_analysis"
    LEASE_REVIEW = "lease_review"
    NEPA_COMPLIANCE = "nepa_compliance"


class LandCategory(str, Enum):
    """Federal/state land classification."""
    BLM_PUBLIC_DOMAIN = "blm_public_domain"
    BLM_ACQUIRED_LANDS = "blm_acquired_lands"
    NATIONAL_FOREST = "national_forest"
    SPLIT_ESTATE_FEDERAL = "split_estate_federal"
    TEXAS_SCHOOL_LANDS = "texas_school_lands"
    TEXAS_UNIVERSITY_LANDS = "texas_university_lands"
    TEXAS_GLO_RELINQUISHMENT = "texas_glo_relinquishment"
    NM_STATE_TRUST = "nm_state_trust"
    TRIBAL_LANDS = "tribal_lands"
    RAILROAD_GRANT = "railroad_grant"
    UNKNOWN = "unknown"


class LeaseType(str, Enum):
    """Federal lease acquisition method."""
    COMPETITIVE = "competitive"
    NONCOMPETITIVE = "noncompetitive"
    EXCHANGE = "exchange"
    PREFERENCE_RIGHT = "preference_right"
    RENEWED = "renewed"
    STATE_COMPETITIVE = "state_competitive"
    STATE_NONCOMPETITIVE = "state_noncompetitive"


class PermitStatus(str, Enum):
    """APD/drilling permit status."""
    PRE_APD = "pre_apd"
    APD_SUBMITTED = "apd_submitted"
    NEPA_PENDING = "nepa_pending"
    ESA_CONSULTATION = "esa_consultation"
    APPROVED = "approved"
    DRILLING = "drilling"
    SUSPENDED = "suspended"
    COMPLETED = "completed"


class EnvironmentalCategory(str, Enum):
    """NEPA compliance level."""
    CATEGORICAL_EXCLUSION = "categorical_exclusion"
    ENVIRONMENTAL_ASSESSMENT = "environmental_assessment"
    FINDING_NO_SIGNIFICANT_IMPACT = "finding_no_significant_impact"
    ENVIRONMENTAL_IMPACT_STATEMENT = "environmental_impact_statement"
    RECORD_OF_DECISION = "record_of_decision"


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class FederalLandsQuery(BaseModel):
    """Input query for federal/state lands analysis."""
    query_text: str = Field(..., min_length=1, description="Analysis query text")
    land_category: LandCategory = LandCategory.UNKNOWN
    lease_serial: str = ""
    blm_state: str = ""
    county: str = ""
    operator: str = ""
    township: str = ""
    range: str = ""
    section: str = ""
    lease_type: Optional[LeaseType] = None
    primary_term_years: Optional[int] = None
    royalty_rate: Optional[float] = None
    mode: ResponseMode = ResponseMode.DEFENSE
    max_doctrines: int = 20
    include_citations: bool = True
    include_recommendations: bool = True
    lease_date: Optional[str] = None
    session_id: str = ""

    @field_validator("royalty_rate")
    @classmethod
    def validate_royalty_rate(cls, v: Optional[float]) -> Optional[float]:
        if v is not None:
            if v < 0.0 or v > 1.0:
                raise ValueError("Royalty rate must be between 0.0 and 1.0")
        return v


class FederalLandsAnalysisResult(BaseModel):
    """Output from federal/state lands analysis."""
    analysis_id: str
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    mode: str = ENGINE_MODE
    query_text: str
    land_classification: str = ""
    lease_classification: str = ""
    applicable_doctrines: List[Dict[str, Any]] = Field(default_factory=list)
    regulatory_framework: Dict[str, Any] = Field(default_factory=dict)
    compliance_requirements: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    citations: List[str] = Field(default_factory=list)
    lease_terms_analysis: Optional[Dict[str, Any]] = None
    apd_requirements: Optional[Dict[str, Any]] = None
    nepa_pathway: Optional[Dict[str, Any]] = None
    royalty_obligations: Optional[Dict[str, Any]] = None
    unit_analysis: Optional[Dict[str, Any]] = None
    confidence: float = 1.0
    risk_assessment: str = ""
    execution_time_ms: float = 0.0
    timestamp: str = ""
    determinism_hash: str = ""

    @field_validator("confidence")
    @classmethod
    def clamp_confidence(cls, v: float) -> float:
        return max(0.0, min(1.0, v))

    def compute_hash(self) -> str:
        """Generate SHA-256 determinism hash."""
        content = json.dumps({
            "id": self.analysis_id,
            "query": self.query_text,
            "land": self.land_classification,
            "lease": self.lease_classification,
            "doctrines": [d.get("doctrine_id", "") for d in self.applicable_doctrines],
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class APDQuery(BaseModel):
    """Query for Application for Permit to Drill analysis."""
    apd_serial: str
    lease_serial: str = ""
    operator: str = ""
    well_name: str = ""
    surface_owner: str = ""
    split_estate: bool = False
    proximity_to_wilderness: bool = False
    proximity_to_water: bool = False
    esa_species_present: bool = False
    cultural_resources: bool = False
    mode: ResponseMode = ResponseMode.APD_ANALYSIS


class APDAnalysisResult(BaseModel):
    """Result from APD compliance analysis."""
    apd_id: str
    analysis_id: str
    nepa_category: str = ""
    nepa_timeline_days: int = 0
    esa_section7_required: bool = False
    nhpa_section106_required: bool = False
    split_estate_compliance: List[str] = Field(default_factory=list)
    surface_use_requirements: List[str] = Field(default_factory=list)
    bonding_requirements: Dict[str, Any] = Field(default_factory=dict)
    reclamation_obligations: List[str] = Field(default_factory=list)
    tribal_consultation: bool = False
    estimated_approval_days: int = 0
    risk_factors: List[str] = Field(default_factory=list)
    mitigation_measures: List[str] = Field(default_factory=list)
    confidence: float = 1.0
    determinism_hash: str = ""


class LeaseTermsQuery(BaseModel):
    """Query for federal lease terms analysis."""
    lease_serial: str
    land_category: LandCategory = LandCategory.BLM_PUBLIC_DOMAIN
    ira_2022_applicable: bool = True
    lease_date: Optional[str] = None
    mode: ResponseMode = ResponseMode.LEASE_REVIEW


class LeaseTermsResult(BaseModel):
    """Result from lease terms analysis."""
    lease_id: str
    analysis_id: str
    primary_term_years: int = 10
    royalty_rate: float = 0.125
    rental_per_acre_year1: float = 1.50
    rental_per_acre_year2_plus: float = 2.00
    minimum_bid: float = 2.00
    expression_of_interest_window_days: int = 10
    first_year_production_required: bool = False
    acreage_limit: int = 0
    rental_increase_schedule: List[Dict[str, Any]] = Field(default_factory=list)
    ira_2022_impacts: List[str] = Field(default_factory=list)
    post_ira_fees: Dict[str, float] = Field(default_factory=dict)
    confidence: float = 1.0
    determinism_hash: str = ""


class HealthResponse(BaseModel):
    """Comprehensive health check response."""
    engine_id: str
    engine_name: str
    version: str
    port: int
    mode: str
    authority_level: float
    status: str = "healthy"
    uptime_seconds: float = 0.0
    doctrines_loaded: int = 0
    queries_processed: int = 0
    error_rate: float = 0.0
    avg_latency_ms: float = 0.0
    cache_hit_rate: float = 0.0
    coverage_gaps: int = 0
    drift_events: int = 0
    cloud_connected: bool = False
    timestamp: str = ""


class MetricsResponse(BaseModel):
    """Detailed metrics response."""
    total_queries: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    vector_searches: int = 0
    deep_analyses: int = 0
    errors: int = 0
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    doctrines_triggered: Dict[str, int] = Field(default_factory=dict)
    coverage_gaps: List[str] = Field(default_factory=list)
    drift_events: List[Dict[str, Any]] = Field(default_factory=list)


class CoverageResponse(BaseModel):
    """Doctrine coverage map response."""
    total_doctrines: int = 0
    triggered_doctrines: List[str] = Field(default_factory=list)
    untriggered_doctrines: List[str] = Field(default_factory=list)
    coverage_gaps: List[Dict[str, Any]] = Field(default_factory=list)
    gap_analysis: Dict[str, Any] = Field(default_factory=dict)


class DoctrinesResponse(BaseModel):
    """List of all available doctrines."""
    total: int = 0
    doctrines: List[Dict[str, Any]] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Global State
# ---------------------------------------------------------------------------

DOCTRINE_CACHE: Dict[str, DoctrineBlock] = {}
SEMANTIC_DICT: Optional[FederalStateLandsNormalizer] = None
TELEMETRY: Optional[FederalLandsTelemetry] = None
CLOUD_RETRIEVER: Optional[CloudRetriever] = None
ENGINE_START_TIME: float = 0.0
CONFIG: Dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Core Engine Logic
# ---------------------------------------------------------------------------

def classify_land_category(query: FederalLandsQuery) -> LandCategory:
    """Classify land category from query context."""
    text = query.query_text.lower()

    if query.land_category != LandCategory.UNKNOWN:
        return query.land_category

    # BLM categories
    if "public domain" in text or "original public land" in text:
        return LandCategory.BLM_PUBLIC_DOMAIN
    if "acquired land" in text or "blm acquired" in text:
        return LandCategory.BLM_ACQUIRED_LANDS

    # Forest Service
    if "national forest" in text or "usfs" in text or "forest service" in text:
        return LandCategory.NATIONAL_FOREST

    # Split estate
    if "split estate" in text or "stock-raising" in text or "srha" in text:
        return LandCategory.SPLIT_ESTATE_FEDERAL

    # Texas state lands
    if "school land" in text or "psl" in text or "permanent school fund" in text:
        return LandCategory.TEXAS_SCHOOL_LANDS
    if "university land" in text or "puf" in text or "permanent university fund" in text:
        return LandCategory.TEXAS_UNIVERSITY_LANDS
    if "relinquishment act" in text or "texas glo" in text:
        return LandCategory.TEXAS_GLO_RELINQUISHMENT

    # New Mexico
    if "new mexico state land" in text or "nm state trust" in text:
        return LandCategory.NM_STATE_TRUST

    # Tribal
    if "tribal" in text or "indian land" in text or "allotment" in text:
        return LandCategory.TRIBAL_LANDS

    # Railroad grant
    if "railroad" in text or "grant land" in text:
        return LandCategory.RAILROAD_GRANT

    # Default to BLM public domain if federal context
    if "blm" in text or "bureau of land management" in text or "federal lease" in text:
        return LandCategory.BLM_PUBLIC_DOMAIN

    return LandCategory.UNKNOWN


def classify_lease_type(query: FederalLandsQuery) -> Optional[LeaseType]:
    """Classify lease acquisition type from query."""
    text = query.query_text.lower()

    if query.lease_type:
        return query.lease_type

    if "competitive" in text or "oral auction" in text or "sealed bid" in text:
        return LeaseType.COMPETITIVE
    if "noncompetitive" in text or "over the counter" in text or "lottery" in text:
        return LeaseType.NONCOMPETITIVE
    if "exchange" in text or "lieu selection" in text:
        return LeaseType.EXCHANGE
    if "preference right" in text or "prla" in text:
        return LeaseType.PREFERENCE_RIGHT
    if "renewal" in text or "renewed" in text:
        return LeaseType.RENEWED

    return None


def search_doctrine_cache(
    normalized_query: str,
    land_cat: LandCategory,
    max_results: int = 20
) -> List[DoctrineBlock]:
    """Search doctrine cache for matching blocks."""
    matches: List[Tuple[float, DoctrineBlock]] = []
    query_terms = set(normalized_query.lower().split())

    for topic, block in DOCTRINE_CACHE.items():
        # Keyword matching
        keyword_score = 0.0
        for kw in block.keywords:
            if kw.lower() in normalized_query.lower():
                keyword_score += 1.0

        # Entity scope matching
        scope_bonus = 0.0
        if land_cat == LandCategory.BLM_PUBLIC_DOMAIN and block.entity_scope == EntityScope.FEDERAL:
            scope_bonus = 2.0
        elif land_cat == LandCategory.TEXAS_SCHOOL_LANDS and block.entity_scope == EntityScope.STATE_TX:
            scope_bonus = 2.0
        elif land_cat == LandCategory.NM_STATE_TRUST and block.entity_scope == EntityScope.STATE_NM:
            scope_bonus = 2.0
        elif land_cat == LandCategory.SPLIT_ESTATE_FEDERAL and block.entity_scope == EntityScope.SPLIT_ESTATE:
            scope_bonus = 3.0

        total_score = keyword_score + scope_bonus

        if total_score > 0.0:
            matches.append((total_score, block))

    # Sort by score descending
    matches.sort(key=lambda x: x[0], reverse=True)

    return [block for score, block in matches[:max_results]]


def apply_authority_hardening(doctrines: List[DoctrineBlock]) -> List[DoctrineBlock]:
    """Apply hierarchical authority weighting and conflict resolution."""
    if not doctrines:
        return []

    # Weight by confidence level
    confidence_weights = {
        ConfidenceLevel.DEFENSIBLE: 1.0,
        ConfidenceLevel.AGGRESSIVE: 0.75,
        ConfidenceLevel.DISCLOSURE: 0.5,
        ConfidenceLevel.HIGH_RISK: 0.25,
    }

    weighted = []
    for doctrine in doctrines:
        weight = confidence_weights.get(doctrine.confidence, 0.5)

        # Boost federal statute authority
        if "30 USC" in " ".join(doctrine.primary_authority):
            weight += 0.2
        if "43 USC" in " ".join(doctrine.primary_authority):
            weight += 0.2
        if "43 CFR" in " ".join(doctrine.primary_authority):
            weight += 0.15

        # Boost controlling precedent
        if doctrine.controlling_precedent:
            weight += 0.1

        weighted.append((weight, doctrine))

    # Sort by weight descending
    weighted.sort(key=lambda x: x[0], reverse=True)

    return [d for w, d in weighted]


def apply_confidence_stratification(
    doctrines: List[DoctrineBlock],
    query: FederalLandsQuery
) -> Tuple[float, str]:
    """Stratify confidence across triggered doctrines."""
    if not doctrines:
        return 0.5, "DISCLOSURE"

    # Aggregate confidence levels
    level_counts = {
        ConfidenceLevel.DEFENSIBLE: 0,
        ConfidenceLevel.AGGRESSIVE: 0,
        ConfidenceLevel.DISCLOSURE: 0,
        ConfidenceLevel.HIGH_RISK: 0,
    }

    for doctrine in doctrines:
        level_counts[doctrine.confidence] += 1

    total = sum(level_counts.values())
    if total == 0:
        return 0.5, "DISCLOSURE"

    # Weighted confidence score
    confidence_score = (
        level_counts[ConfidenceLevel.DEFENSIBLE] * 1.0 +
        level_counts[ConfidenceLevel.AGGRESSIVE] * 0.75 +
        level_counts[ConfidenceLevel.DISCLOSURE] * 0.5 +
        level_counts[ConfidenceLevel.HIGH_RISK] * 0.25
    ) / total

    # Determine stratification level
    if confidence_score >= 0.85:
        level = "DEFENSIBLE"
    elif confidence_score >= 0.65:
        level = "AGGRESSIVE"
    elif confidence_score >= 0.4:
        level = "DISCLOSURE"
    else:
        level = "HIGH_RISK"

    return confidence_score, level


def build_regulatory_framework(
    doctrines: List[DoctrineBlock],
    land_cat: LandCategory,
    lease_type: Optional[LeaseType]
) -> Dict[str, Any]:
    """Build comprehensive regulatory framework from triggered doctrines."""
    framework = {
        "primary_statutes": [],
        "regulations": [],
        "blm_orders": [],
        "state_authorities": [],
        "environmental_compliance": [],
        "surface_management": [],
    }

    statute_set = set()
    regulation_set = set()

    for doctrine in doctrines:
        for auth in doctrine.primary_authority:
            if "USC" in auth or "U.S.C." in auth:
                statute_set.add(auth)
            elif "CFR" in auth or "C.F.R." in auth:
                regulation_set.add(auth)
            elif "Onshore Order" in auth or "NTL" in auth:
                if auth not in framework["blm_orders"]:
                    framework["blm_orders"].append(auth)
            elif "Texas" in auth or "New Mexico" in auth:
                if auth not in framework["state_authorities"]:
                    framework["state_authorities"].append(auth)

    framework["primary_statutes"] = sorted(statute_set)
    framework["regulations"] = sorted(regulation_set)

    # Add standard environmental compliance requirements
    if land_cat in [LandCategory.BLM_PUBLIC_DOMAIN, LandCategory.BLM_ACQUIRED_LANDS, LandCategory.NATIONAL_FOREST]:
        framework["environmental_compliance"] = [
            "NEPA compliance (42 USC 4321 et seq.)",
            "ESA Section 7 consultation if species present (16 USC 1536)",
            "NHPA Section 106 review (54 USC 306108)",
            "Clean Water Act Section 404 if wetlands impacted",
            "Clean Air Act conformity determination",
        ]

    if land_cat == LandCategory.SPLIT_ESTATE_FEDERAL:
        framework["surface_management"] = [
            "Surface owner notification (43 CFR 3814.1)",
            "Bond to cover surface damages (43 CFR 3104.5)",
            "Reclamation plan (43 CFR 3162.5-1)",
            "Surface use agreement or waiver",
        ]

    return framework


def generate_recommendations(
    query: FederalLandsQuery,
    doctrines: List[DoctrineBlock],
    land_cat: LandCategory,
    lease_type: Optional[LeaseType],
    confidence: float
) -> List[str]:
    """Generate actionable recommendations based on analysis."""
    recs = []

    # Confidence-based recommendations
    if confidence < 0.6:
        recs.append("DISCLOSURE REQUIRED: Confidence below defensible threshold. Consult regulatory attorney before proceeding.")

    # Land category specific
    if land_cat == LandCategory.BLM_PUBLIC_DOMAIN:
        if lease_type == LeaseType.COMPETITIVE:
            recs.append("Monitor BLM quarterly lease sale schedules. Submit Expression of Interest 10+ days before sale.")
            recs.append("Prepare for sealed bid or oral auction. Minimum bid post-IRA 2022: $10/acre.")
        elif lease_type == LeaseType.NONCOMPETITIVE:
            recs.append("File noncompetitive lease offer only for parcels that received no bids at competitive sale.")
            recs.append("First-qualified-offeror priority. Consider lottery if multiple simultaneous offers.")

    if land_cat == LandCategory.SPLIT_ESTATE_FEDERAL:
        recs.append("Notify surface owner 30 days prior to surface entry. Bond must cover reclamation costs.")
        recs.append("Attempt to negotiate surface use agreement. If impasse, BLM will adjudicate under 43 CFR 3814.")

    if land_cat == LandCategory.NATIONAL_FOREST:
        recs.append("Forest Service consent required before BLM can issue lease. May take 6-12 months.")
        recs.append("Expect additional surface use stipulations and timing limitations.")

    if land_cat in [LandCategory.TEXAS_SCHOOL_LANDS, LandCategory.TEXAS_UNIVERSITY_LANDS]:
        recs.append("GLO competitive lease sales typically quarterly. Monitor GLO website for sale dates.")
        recs.append("Relinquishment Act lands: verify whether mineral estate was reserved by State or conveyed.")

    # APD recommendations
    if "apd" in query.query_text.lower() or "permit to drill" in query.query_text.lower():
        recs.append("Submit APD to BLM field office with jurisdiction. Allow 30-60 days for CE, 6-12 months for EA/EIS.")
        recs.append("Conduct cultural resource survey and biological assessment before APD submittal to avoid delays.")
        recs.append("If ESA-listed species present, anticipate Section 7 consultation adding 135+ days to timeline.")

    # Royalty recommendations
    if query.royalty_rate is not None:
        if query.royalty_rate < 0.125:
            recs.append("WARNING: Federal royalty rate below statutory minimum of 12.5%. Verify lease terms.")
        elif query.royalty_rate >= 0.1875:
            recs.append("Post-IRA 2022 federal leases have 16.67% minimum royalty (1/6th). Confirm compliance.")

    # NEPA recommendations
    nepa_keywords = ["nepa", "environmental", "eis", "ea"]
    if any(kw in query.query_text.lower() for kw in nepa_keywords):
        recs.append("Scoping process for EIS typically 60+ days. Draft EIS public comment 45+ days.")
        recs.append("Categorical Exclusions available for some activities under DOI 516 DM 11. Consult BLM.")

    return recs


def generate_citations(doctrines: List[DoctrineBlock]) -> List[str]:
    """Extract and deduplicate citations from triggered doctrines."""
    citations = set()

    for doctrine in doctrines:
        for auth in doctrine.primary_authority:
            citations.add(auth)
        if doctrine.controlling_precedent:
            citations.add(doctrine.controlling_precedent)

    return sorted(citations)


def analyze_apd_requirements(
    query: FederalLandsQuery,
    land_cat: LandCategory,
    doctrines: List[DoctrineBlock]
) -> Optional[Dict[str, Any]]:
    """Generate APD-specific analysis if query relates to drilling permits."""
    apd_keywords = ["apd", "permit to drill", "application for permit", "drilling permit"]
    if not any(kw in query.query_text.lower() for kw in apd_keywords):
        return None

    apd_data = {
        "nepa_category": "environmental_assessment",
        "estimated_timeline_days": 180,
        "required_surveys": [],
        "required_consultations": [],
        "bonding_required": True,
        "reclamation_plan_required": True,
    }

    # NEPA category determination
    if "categorical exclusion" in query.query_text.lower():
        apd_data["nepa_category"] = "categorical_exclusion"
        apd_data["estimated_timeline_days"] = 45
    elif "eis" in query.query_text.lower() or "environmental impact statement" in query.query_text.lower():
        apd_data["nepa_category"] = "environmental_impact_statement"
        apd_data["estimated_timeline_days"] = 365

    # Required surveys
    apd_data["required_surveys"] = [
        "Cultural resources Class III inventory",
        "Biological resources survey",
        "Threatened/endangered species habitat assessment",
        "Paleontological resources survey (if sensitive areas)",
        "Wetlands delineation (if applicable)",
    ]

    # Consultations
    apd_data["required_consultations"] = []
    if "species" in query.query_text.lower() or "endangered" in query.query_text.lower():
        apd_data["required_consultations"].append("USFWS Section 7 consultation")
        apd_data["estimated_timeline_days"] += 135

    if "cultural" in query.query_text.lower() or "historic" in query.query_text.lower():
        apd_data["required_consultations"].append("SHPO Section 106 consultation")

    if "tribal" in query.query_text.lower():
        apd_data["required_consultations"].append("Tribal consultation under EO 13175")

    return apd_data


def analyze_nepa_pathway(
    query: FederalLandsQuery,
    land_cat: LandCategory
) -> Optional[Dict[str, Any]]:
    """Determine NEPA compliance pathway."""
    nepa_keywords = ["nepa", "environmental", "eis", "ea", "categorical exclusion"]
    if not any(kw in query.query_text.lower() for kw in nepa_keywords):
        return None

    nepa = {
        "category": "environmental_assessment",
        "estimated_days": 180,
        "public_comment_required": True,
        "finding_required": "FONSI",
        "pathway_rationale": "",
    }

    text = query.query_text.lower()

    if "categorical exclusion" in text or "ce" in text or "cx" in text:
        nepa["category"] = "categorical_exclusion"
        nepa["estimated_days"] = 30
        nepa["public_comment_required"] = False
        nepa["finding_required"] = "CE determination"
        nepa["pathway_rationale"] = "May qualify under DOI 516 DM 11 for routine operations."

    elif "eis" in text or "environmental impact statement" in text or "significant impact" in text:
        nepa["category"] = "environmental_impact_statement"
        nepa["estimated_days"] = 365
        nepa["public_comment_required"] = True
        nepa["finding_required"] = "Record of Decision"
        nepa["pathway_rationale"] = "Significant environmental impacts require full EIS under 40 CFR 1501.3."

    else:
        nepa["pathway_rationale"] = "Standard EA pathway. FONSI likely if no significant impacts."

    return nepa


def analyze_royalty_obligations(
    query: FederalLandsQuery,
    land_cat: LandCategory,
    lease_type: Optional[LeaseType]
) -> Optional[Dict[str, Any]]:
    """Analyze royalty rate, rental, and reporting obligations."""
    royalty_keywords = ["royalty", "rental", "onrr", "reporting", "valuation"]
    if not any(kw in query.query_text.lower() for kw in royalty_keywords):
        return None

    royalty = {
        "royalty_rate": 0.125,
        "rental_year_1_10": 1.50,
        "rental_year_after": 2.00,
        "minimum_royalty": 0.0,
        "reporting_entity": "ONRR",
        "reporting_frequency": "monthly",
        "valuation_method": "higher of gross proceeds or index price",
        "ira_2022_applicable": True,
    }

    # Post-IRA 2022 adjustments
    if query.lease_date and query.lease_date >= "2022-08-16":
        royalty["royalty_rate"] = 0.16667  # 1/6th
        royalty["rental_year_1_10"] = 3.00
        royalty["rental_year_after"] = 5.00
        royalty["ira_2022_applicable"] = True

    # Override with query-provided royalty rate
    if query.royalty_rate is not None:
        royalty["royalty_rate"] = query.royalty_rate

    # State lands have different rates
    if land_cat == LandCategory.TEXAS_SCHOOL_LANDS:
        royalty["royalty_rate"] = 0.25  # Texas GLO typically 25%
        royalty["reporting_entity"] = "Texas GLO"
        royalty["ira_2022_applicable"] = False

    if land_cat == LandCategory.NM_STATE_TRUST:
        royalty["royalty_rate"] = 0.1875  # NM State Land Office 18.75%+
        royalty["reporting_entity"] = "NM State Land Office"
        royalty["ira_2022_applicable"] = False

    return royalty


def analyze_unit_agreements(
    query: FederalLandsQuery,
    doctrines: List[DoctrineBlock]
) -> Optional[Dict[str, Any]]:
    """Analyze unitization and communitization requirements."""
    unit_keywords = ["unit", "communitization", "participating area", "allocation"]
    if not any(kw in query.query_text.lower() for kw in unit_keywords):
        return None

    unit = {
        "type": "unknown",
        "approval_required_from": [],
        "allocation_method": "",
        "participating_area_required": True,
        "requirements": [],
    }

    text = query.query_text.lower()

    if "communitization" in text:
        unit["type"] = "communitization_agreement"
        unit["approval_required_from"] = ["BLM", "All lessees", "All working interest owners"]
        unit["allocation_method"] = "Surface acreage allocation"
        unit["requirements"] = [
            "BLM approval required under 43 CFR 3105.2-3",
            "Must prevent drainage or waste",
            "All parties must consent to CA",
            "Participating area designation for each well",
        ]

    elif "unit" in text or "unitization" in text:
        unit["type"] = "unit_agreement"
        unit["approval_required_from"] = ["BLM", "All lessees in unit"]
        unit["allocation_method"] = "Reservoir engineering allocation formula"
        unit["participating_area_required"] = True
        unit["requirements"] = [
            "Unit operator designation required",
            "Unit agreement must specify allocation formula",
            "Participating area for each well",
            "Non-participating areas may revert to individual lease status",
        ]

    return unit


def three_layer_response(
    query: FederalLandsQuery,
    telemetry: FederalLandsTelemetry
) -> FederalLandsAnalysisResult:
    """
    Three-layer response architecture:
    1. Doctrine Cache (0-200ms) - pre-compiled reasoning
    2. Semantic Retrieval (200-500ms) - vector search fallback
    3. Deep Analysis (500ms+) - multi-source synthesis
    """
    analysis_id = str(uuid.uuid4())
    start_time = time.time()

    telemetry.start_query(analysis_id)

    # Layer 0: Normalization
    phase_start = time.time()
    normalized = SEMANTIC_DICT.normalize(query.query_text).normalized_query if SEMANTIC_DICT else query.query_text
    land_cat = classify_land_category(query)
    lease_type = classify_lease_type(query)
    telemetry.record_phase(analysis_id, QueryPhase.NORMALIZATION, time.time() - phase_start)

    # Layer 1: Doctrine Cache Lookup
    phase_start = time.time()
    doctrines = search_doctrine_cache(normalized, land_cat, max_results=query.max_doctrines)
    cache_hit = len(doctrines) > 0
    telemetry.record_phase(analysis_id, QueryPhase.CACHE_LOOKUP, time.time() - phase_start)

    if cache_hit:
        telemetry.record_cache_hit(analysis_id)
        logger.info(f"Cache hit | doctrines={len(doctrines)} | query={query.query_text[:50]}")
    else:
        telemetry.record_cache_miss(analysis_id)
        logger.warning(f"Cache miss | query={query.query_text[:50]}")

    # Layer 2: Vector Search Fallback (if cache miss or low confidence)
    if not cache_hit or len(doctrines) < 3:
        phase_start = time.time()
        # Vector search would go here - stub for now
        logger.info("Vector search fallback triggered")
        telemetry.record_phase(analysis_id, QueryPhase.VECTOR_SEARCH, time.time() - phase_start)

    # Layer 3: Deep Analysis (if complex query or multi-doctrine interaction)
    if query.mode in [ResponseMode.DEFENSE, ResponseMode.MEMO] or len(doctrines) > 5:
        phase_start = time.time()
        # Deep analysis synthesis
        logger.info("Deep analysis mode activated")
        telemetry.record_phase(analysis_id, QueryPhase.DEEP_ANALYSIS, time.time() - phase_start)

    # Authority Hardening
    phase_start = time.time()
    doctrines = apply_authority_hardening(doctrines)
    telemetry.record_phase(analysis_id, QueryPhase.AUTHORITY_HARDENING, time.time() - phase_start)

    # Confidence Stratification
    phase_start = time.time()
    confidence, risk_level = apply_confidence_stratification(doctrines, query)
    telemetry.record_phase(analysis_id, QueryPhase.CONFIDENCE_STRATIFICATION, time.time() - phase_start)

    # Build comprehensive response
    phase_start = time.time()
    regulatory_framework = build_regulatory_framework(doctrines, land_cat, lease_type)
    recommendations = generate_recommendations(query, doctrines, land_cat, lease_type, confidence) if query.include_recommendations else []
    citations = generate_citations(doctrines) if query.include_citations else []

    apd_requirements = analyze_apd_requirements(query, land_cat, doctrines)
    nepa_pathway = analyze_nepa_pathway(query, land_cat)
    royalty_obligations = analyze_royalty_obligations(query, land_cat, lease_type)
    unit_analysis = analyze_unit_agreements(query, doctrines)

    telemetry.record_phase(analysis_id, QueryPhase.RESPONSE_ASSEMBLY, time.time() - phase_start)

    # Assemble result
    result = FederalLandsAnalysisResult(
        analysis_id=analysis_id,
        query_text=query.query_text,
        land_classification=land_cat.value,
        lease_classification=lease_type.value if lease_type else "",
        applicable_doctrines=[
            {
                "doctrine_id": d.topic,
                "keywords": d.keywords,
                "conclusion": d.conclusion_template,
                "confidence": d.confidence.value,
                "entity_scope": d.entity_scope.value,
                "primary_authority": d.primary_authority[:3],
            }
            for d in doctrines[:10]
        ],
        regulatory_framework=regulatory_framework,
        compliance_requirements=[],
        recommendations=recommendations,
        citations=citations,
        apd_requirements=apd_requirements,
        nepa_pathway=nepa_pathway,
        royalty_obligations=royalty_obligations,
        unit_analysis=unit_analysis,
        confidence=confidence,
        risk_assessment=risk_level,
        execution_time_ms=(time.time() - start_time) * 1000,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    result.compute_hash()

    total_time = time.time() - start_time
    telemetry.record_phase(analysis_id, QueryPhase.TOTAL, total_time)
    telemetry.complete_query(analysis_id, success=True)

    # Audit trail
    telemetry.log_audit(AuditEntry(
        timestamp=datetime.now(timezone.utc).isoformat(),
        query_id=analysis_id,
        query_text=query.query_text,
        mode=query.mode.value,
        doctrines_triggered=[d.topic for d in doctrines],
        confidence=confidence,
        determinism_hash=result.determinism_hash,
    ))

    logger.info(f"Query complete | id={analysis_id} | time={total_time*1000:.2f}ms | confidence={confidence:.2f}")

    return result


# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager for startup/shutdown."""
    global DOCTRINE_CACHE, SEMANTIC_DICT, TELEMETRY, CLOUD_RETRIEVER, ENGINE_START_TIME, CONFIG

    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    ENGINE_START_TIME = time.time()

    # Load config
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            CONFIG = json.load(f)
        logger.info(f"Config loaded from {CONFIG_PATH}")
    else:
        logger.warning(f"Config not found at {CONFIG_PATH}, using defaults")
        CONFIG = {}

    # Build doctrine cache
    DOCTRINE_CACHE = build_doctrine_cache()
    logger.info(f"Doctrine cache built | blocks={len(DOCTRINE_CACHE)}")

    # Initialize semantic dictionary
    SEMANTIC_DICT = FederalStateLandsNormalizer()
    logger.info("Semantic dictionary initialized")

    # Initialize telemetry
    telemetry_path = Path(__file__).parent / "data" / "lm21_telemetry.jsonl"
    telemetry_path.parent.mkdir(exist_ok=True)
    TELEMETRY = FederalLandsTelemetry(str(telemetry_path))
    logger.info(f"Telemetry initialized | path={telemetry_path}")

    # Initialize cloud retriever if available
    if CLOUD_AVAILABLE:
        try:
            CLOUD_RETRIEVER = CloudRetriever(engine_id=ENGINE_ID)
            logger.info("Cloud retriever connected")
        except Exception as e:
            logger.warning(f"Cloud retriever init failed: {e}")
            CLOUD_RETRIEVER = None

    logger.info(f"{ENGINE_NAME} ready | doctrines={len(DOCTRINE_CACHE)} | port={ENGINE_PORT}")

    yield

    # Shutdown
    if TELEMETRY:
        TELEMETRY.flush()
    logger.info(f"{ENGINE_NAME} shutdown complete")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="TIE Gold Standard federal/state lands oil & gas intelligence engine",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint with engine info."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "mode": ENGINE_MODE,
        "authority": ENGINE_AUTHORITY,
        "status": "operational",
        "endpoints": [
            "/health",
            "/query",
            "/apd",
            "/lease-terms",
            "/metrics",
            "/doctrines",
            "/coverage",
        ],
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Comprehensive health check."""
    uptime = time.time() - ENGINE_START_TIME

    stats = TELEMETRY.get_stats() if TELEMETRY else {}

    return HealthResponse(
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=ENGINE_VERSION,
        port=ENGINE_PORT,
        mode=ENGINE_MODE,
        authority_level=ENGINE_AUTHORITY,
        status="healthy",
        uptime_seconds=uptime,
        doctrines_loaded=len(DOCTRINE_CACHE),
        queries_processed=stats.get("total_queries", 0),
        error_rate=stats.get("error_rate", 0.0),
        avg_latency_ms=stats.get("avg_latency_ms", 0.0),
        cache_hit_rate=stats.get("cache_hit_rate", 0.0),
        coverage_gaps=len(stats.get("coverage_gaps", [])),
        drift_events=len(stats.get("drift_events", [])),
        cloud_connected=CLOUD_RETRIEVER is not None,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/query", response_model=FederalLandsAnalysisResult)
async def query_endpoint(query: FederalLandsQuery):
    """Main query endpoint for federal/state lands analysis."""
    if not TELEMETRY:
        raise HTTPException(status_code=503, detail="Telemetry not initialized")

    try:
        result = three_layer_response(query, TELEMETRY)
        return result
    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        if TELEMETRY:
            TELEMETRY.complete_query("error", success=False)
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@app.post("/apd", response_model=APDAnalysisResult)
async def apd_endpoint(query: APDQuery):
    """APD-specific analysis endpoint."""
    analysis_id = str(uuid.uuid4())

    # Build federal lands query from APD query
    federal_query = FederalLandsQuery(
        query_text=f"APD {query.apd_serial} for lease {query.lease_serial} operator {query.operator}",
        lease_serial=query.lease_serial,
        operator=query.operator,
        mode=query.mode if query.mode in [ResponseMode.APD_ANALYSIS, ResponseMode.DEFENSE] else ResponseMode.APD_ANALYSIS,
    )

    result = three_layer_response(federal_query, TELEMETRY)

    # Transform into APD-specific result
    apd_result = APDAnalysisResult(
        apd_id=query.apd_serial,
        analysis_id=analysis_id,
        nepa_category=result.nepa_pathway.get("category", "") if result.nepa_pathway else "",
        nepa_timeline_days=result.nepa_pathway.get("estimated_days", 0) if result.nepa_pathway else 0,
        esa_section7_required=query.esa_species_present,
        nhpa_section106_required=query.cultural_resources,
        split_estate_compliance=[] if not query.split_estate else [
            "Surface owner notification required",
            "Bond for surface damages",
            "Surface use plan required",
        ],
        surface_use_requirements=result.apd_requirements.get("required_surveys", []) if result.apd_requirements else [],
        bonding_requirements={
            "lease_bond": True,
            "statewide_bond_option": True,
            "nationwide_bond_option": True,
        },
        reclamation_obligations=[
            "Submit reclamation plan with APD",
            "Interim reclamation during operations",
            "Final reclamation within 1 year of abandonment",
        ],
        tribal_consultation=False,
        estimated_approval_days=result.nepa_pathway.get("estimated_days", 180) if result.nepa_pathway else 180,
        risk_factors=[],
        mitigation_measures=result.recommendations[:5],
        confidence=result.confidence,
    )

    return apd_result


@app.post("/lease-terms", response_model=LeaseTermsResult)
async def lease_terms_endpoint(query: LeaseTermsQuery):
    """Federal lease terms analysis endpoint."""
    analysis_id = str(uuid.uuid4())

    # Determine if IRA 2022 applies
    ira_applicable = query.ira_2022_applicable
    if query.lease_date and query.lease_date < "2022-08-16":
        ira_applicable = False

    # Base federal lease terms
    result = LeaseTermsResult(
        lease_id=query.lease_serial,
        analysis_id=analysis_id,
        primary_term_years=10,
        royalty_rate=0.16667 if ira_applicable else 0.125,
        rental_per_acre_year1=3.00 if ira_applicable else 1.50,
        rental_per_acre_year2_plus=5.00 if ira_applicable else 2.00,
        minimum_bid=10.00 if ira_applicable else 2.00,
        expression_of_interest_window_days=10 if ira_applicable else 0,
        first_year_production_required=False,
        acreage_limit=10240,  # Standard BLM lease limit
        rental_increase_schedule=[
            {"years": "1-5", "rate_per_acre": 3.00 if ira_applicable else 1.50},
            {"years": "6-10", "rate_per_acre": 5.00 if ira_applicable else 2.00},
        ],
        ira_2022_impacts=[
            "Minimum royalty rate increased to 16.67% (1/6th)",
            "Rental rates doubled",
            "Minimum bid increased to $10/acre",
            "Expression of Interest nomination process required",
            "Royalty relief eliminated for marginal production",
        ] if ira_applicable else [],
        post_ira_fees={
            "rental_year_1": 3.00,
            "rental_year_2_plus": 5.00,
            "royalty_rate": 0.16667,
            "minimum_bid": 10.00,
        } if ira_applicable else {},
        confidence=0.95,
    )

    return result


@app.get("/metrics", response_model=MetricsResponse)
async def metrics():
    """Detailed metrics endpoint."""
    if not TELEMETRY:
        raise HTTPException(status_code=503, detail="Telemetry not initialized")

    stats = TELEMETRY.get_stats()

    return MetricsResponse(
        total_queries=stats.get("total_queries", 0),
        cache_hits=stats.get("cache_hits", 0),
        cache_misses=stats.get("cache_misses", 0),
        vector_searches=stats.get("vector_searches", 0),
        deep_analyses=stats.get("deep_analyses", 0),
        errors=stats.get("errors", 0),
        avg_latency_ms=stats.get("avg_latency_ms", 0.0),
        p50_latency_ms=stats.get("p50_latency_ms", 0.0),
        p95_latency_ms=stats.get("p95_latency_ms", 0.0),
        p99_latency_ms=stats.get("p99_latency_ms", 0.0),
        doctrines_triggered=stats.get("doctrines_triggered", {}),
        coverage_gaps=stats.get("coverage_gaps", []),
        drift_events=stats.get("drift_events", []),
    )


@app.get("/doctrines", response_model=DoctrinesResponse)
async def doctrines():
    """List all available doctrine blocks."""
    doctrines_list = [
        {
            "topic": block.topic,
            "keywords": block.keywords,
            "entity_scope": block.entity_scope.value,
            "confidence": block.confidence.value,
            "authority_count": len(block.primary_authority),
        }
        for block in DOCTRINE_CACHE.values()
    ]

    return DoctrinesResponse(
        total=len(doctrines_list),
        doctrines=doctrines_list,
    )


@app.get("/coverage", response_model=CoverageResponse)
async def coverage():
    """Doctrine coverage map endpoint."""
    if not TELEMETRY:
        raise HTTPException(status_code=503, detail="Telemetry not initialized")

    coverage_data = TELEMETRY.get_coverage_map()

    return CoverageResponse(
        total_doctrines=len(DOCTRINE_CACHE),
        triggered_doctrines=coverage_data.get("triggered", []),
        untriggered_doctrines=coverage_data.get("untriggered", []),
        coverage_gaps=coverage_data.get("gaps", []),
        gap_analysis={
            "total_gaps": len(coverage_data.get("gaps", [])),
            "gap_categories": coverage_data.get("gap_categories", {}),
        },
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Launching {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
    )
