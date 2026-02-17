"""
LM13 Water Rights Analyzer Engine
====================================

Core analysis engine for water rights as they relate to oil and gas
operations, surface use, and environmental compliance in Texas.

Capabilities:
- Water right identification and classification
- Groundwater conservation district rule analysis
- Produced water disposal permit tracking
- Injection well compliance monitoring
- Surface use agreement water provisions analysis
- Freshwater source identification and protection zone mapping
- Water transport and sale agreement analysis
- Environmental compliance risk scoring
- Seismicity risk assessment for disposal wells
- Produced water recycling economics analysis

All outputs are Pydantic-validated with SHA-256 determinism hashes.
Uses loguru for structured logging and type hints on every function.

Author: ECHO OMEGA PRIME Build System
Engine: LM13 v1.0.0
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import date, datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from loguru import logger
from pydantic import BaseModel, Field, field_validator

# Cloud retriever for Cognition Cloud integration
sys.path.insert(0, str(Path(__file__).parent.parent / "_shared"))
try:
    from cloud_retriever import CognitionCloudRetriever
    CLOUD_RETRIEVER_AVAILABLE = True
except ImportError:
    logger.warning("CognitionCloudRetriever not available - deep analysis mode limited")
    CLOUD_RETRIEVER_AVAILABLE = False


# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    AquiferProtectionRule,
    DoctrineCategory,
    GroundwaterRule,
    InjectionWellStandard,
    ProducedWaterRegulation,
    RiskLevel,
    SurfaceWaterRule,
    TexasWaterDoctrine,
    WaterDoctrineCache,
)
from search import (
    AquiferIndex,
    AquiferName,
    ComplianceStatus,
    GeoCoordinate,
    OperatorIndex,
    PermitIndex,
    WaterPermitRecord,
    WaterRightType,
    WaterRightsSearchEngine,
    WaterSearchQuery,
    WaterSearchResponse,
    WellType,
)
from semantic import (
    SemanticTerm,
    WaterRightsSemanticDictionary,
)
from telemetry import (
    AuditAction,
    OperationType,
    WaterRightsTelemetry,
)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ENGINE_ID = "LM13"
ENGINE_NAME = "Water Rights Analyzer"
ENGINE_VERSION = "2.0.0"  # TIE-20 compliant
ENGINE_PORT = 8413
CONFIG_PATH = Path(__file__).parent / "config.json"


# ---------------------------------------------------------------------------
# TIE-20 Component Enums
# ---------------------------------------------------------------------------

class ResponseMode(str, Enum):
    """TIE-20 Component 2: Response modes for different use cases."""
    FAST = "fast"  # Concise answer, doctrine cache only
    DEFENSE = "defense"  # Audit-ready with full citations
    MEMO = "memo"  # Full documentation mode with reasoning chain
    PLANNING = "planning"  # Forward-looking analysis
    REPORTING = "reporting"  # Historical/factual reporting
    AUDIT = "audit"  # Forensic review mode


class ConfidenceStratification(str, Enum):
    """TIE-20 Component 5: Confidence stratification levels."""
    DEFENSIBLE = "defensible"  # High-confidence, well-established law
    AGGRESSIVE = "aggressive"  # Arguable position, some risk
    DISCLOSURE = "disclosure"  # Must disclose uncertainty
    HIGH_RISK = "high_risk"  # Significant legal exposure


class AnalysisZone(str, Enum):
    """TIE-20 Component 13: Analysis zones - never blur these."""
    PLANNING = "planning"  # What we MIGHT do
    REPORTING = "reporting"  # What we DID do
    AUDIT = "audit"  # What we SHOULD HAVE done


class AuthorityLevel(str, Enum):
    """TIE-20 Component 4: Authority hierarchy for conflict resolution."""
    STATUTE = "statute"  # Texas Water Code, Oil & Gas statutes
    REGULATION = "regulation"  # TCEQ/RRC rules, 16 TAC, 30 TAC
    CASE_LAW = "case_law"  # Texas Supreme Court, appeals courts
    ADMINISTRATIVE = "administrative"  # TCEQ/RRC orders, GCD rules
    GUIDANCE = "guidance"  # TCEQ guidance documents
    BEST_PRACTICE = "best_practice"  # Industry standard practice


# Authority weights for conflict resolution
AUTHORITY_WEIGHTS = {
    AuthorityLevel.STATUTE: 1.0,
    AuthorityLevel.REGULATION: 0.9,
    AuthorityLevel.CASE_LAW: 0.85,
    AuthorityLevel.ADMINISTRATIVE: 0.7,
    AuthorityLevel.GUIDANCE: 0.5,
    AuthorityLevel.BEST_PRACTICE: 0.3,
}


class IssueCategory(str, Enum):
    """TIE-20 Component 19: Multi-doctrine decomposition categories."""
    GROUNDWATER_RIGHTS = "groundwater_rights"
    SURFACE_WATER_RIGHTS = "surface_water_rights"
    PRODUCED_WATER_DISPOSAL = "produced_water_disposal"
    INJECTION_WELL_COMPLIANCE = "injection_well_compliance"
    GCD_JURISDICTION = "gcd_jurisdiction"
    AQUIFER_PROTECTION = "aquifer_protection"
    WATER_QUALITY = "water_quality"
    SEISMICITY_RISK = "seismicity_risk"
    ENVIRONMENTAL_COMPLIANCE = "environmental_compliance"
    WATER_TRANSFER = "water_transfer"
    DROUGHT_MANAGEMENT = "drought_management"
    INTERSTATE_COMPACT = "interstate_compact"


class IssueStratum(str, Enum):
    """TIE-20 Component 19: Issue complexity strata."""
    THRESHOLD = "threshold"  # Initial classification
    SUBSTANTIVE = "substantive"  # Core legal/regulatory question
    PROCEDURAL = "procedural"  # Process and timing
    REMEDIAL = "remedial"  # How to fix violations


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# TIE-20 Component Classes
# ---------------------------------------------------------------------------

class FactFragilityScore(BaseModel):
    """TIE-20 Component 14: Fact fragility scoring."""
    fact_statement: str
    verifiability: float = Field(ge=0.0, le=1.0, description="How easily can this be proven?")
    recharacterization_risk: float = Field(ge=0.0, le=1.0, description="Could opposing counsel reframe this?")
    testimony_dependence: float = Field(ge=0.0, le=1.0, description="Does this rely on witness testimony?")
    documentary_support: float = Field(ge=0.0, le=1.0, description="Do we have documents proving this?")
    overall_fragility: float = Field(ge=0.0, le=1.0, description="Composite fragility score")
    risk_notes: str = ""

    def compute_overall(self) -> float:
        """Compute overall fragility as weighted average."""
        self.overall_fragility = (
            (1.0 - self.verifiability) * 0.3 +
            self.recharacterization_risk * 0.3 +
            self.testimony_dependence * 0.2 +
            (1.0 - self.documentary_support) * 0.2
        )
        return self.overall_fragility


class ZonedAnalysisResult(BaseModel):
    """TIE-20 Component 13: Zoned analysis - separating planning/reporting/audit."""
    zone: AnalysisZone
    issue_description: str
    applicable_doctrines: List[str] = Field(default_factory=list)
    authority_citations: List[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    risk_level: RiskLevel
    recommendations: List[str] = Field(default_factory=list)
    epistemic_caveat: str = ""


class DoctrineInteraction(BaseModel):
    """TIE-20 Component 19: Multi-doctrine decomposition - doctrine interaction edges."""
    from_category: IssueCategory
    to_category: IssueCategory
    interaction_type: str  # "conflicts", "reinforces", "conditions", "triggers"
    resolution_priority: int = 1
    notes: str = ""


class DecomposedIssue(BaseModel):
    """TIE-20 Component 19: Multi-doctrine decomposition result."""
    category: IssueCategory
    stratum: IssueStratum
    description: str
    applicable_doctrines: List[str] = Field(default_factory=list)
    authority_level: AuthorityLevel
    authority_weight: float
    confidence_stratification: ConfidenceStratification
    interactions: List[DoctrineInteraction] = Field(default_factory=list)
    resolution_order: int = 0


class CoverageGap(BaseModel):
    """TIE-20 Component 10: Coverage map - epistemic gap detection."""
    query_aspect: str
    triggered_doctrines: List[str] = Field(default_factory=list)
    missed_doctrines: List[str] = Field(default_factory=list)
    gap_severity: str  # "minor", "moderate", "critical"
    recommended_research: str = ""


class DriftObservation(BaseModel):
    """TIE-20 Component 9: Drift watcher - doctrine drift detection."""
    doctrine_id: str
    observation_date: str
    drift_type: str  # "statutory_change", "case_law_update", "regulatory_amendment", "administrative_order"
    drift_severity: str  # "minor", "moderate", "major"
    description: str
    source_citation: str
    action_required: str = ""


class ThreeLayerResponse(BaseModel):
    """TIE-20 Component 1: Three-layer response structure."""
    query: str
    response_mode: ResponseMode

    # Layer 1: Doctrine Cache (0-200ms)
    cache_hit: bool = False
    cache_doctrines: List[str] = Field(default_factory=list)
    cache_response: str = ""
    cache_latency_ms: float = 0.0

    # Layer 2: Semantic Retrieval (200-1000ms)
    semantic_triggered: bool = False
    semantic_matches: List[Dict[str, Any]] = Field(default_factory=list)
    semantic_response: str = ""
    semantic_latency_ms: float = 0.0

    # Layer 3: Deep Analysis (1000-5000ms)
    deep_analysis_triggered: bool = False
    deep_sources: List[str] = Field(default_factory=list)
    deep_response: str = ""
    deep_latency_ms: float = 0.0

    # Final synthesis
    final_answer: str
    total_latency_ms: float
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_stratification: ConfidenceStratification
    authority_level: AuthorityLevel
    citations: List[str] = Field(default_factory=list)

    # TIE-20 integrated components
    zoned_analysis: Optional[List[ZonedAnalysisResult]] = None
    fact_fragility: Optional[List[FactFragilityScore]] = None
    decomposed_issues: Optional[List[DecomposedIssue]] = None
    coverage_gaps: Optional[List[CoverageGap]] = None
    drift_alerts: Optional[List[DriftObservation]] = None

    determinism_hash: str = ""

    def compute_hash(self) -> str:
        """Generate SHA-256 determinism hash."""
        content = f"{self.query}|{self.final_answer}|{self.total_latency_ms:.2f}"
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class WaterClassification(str, Enum):
    """Primary water classification."""
    FRESH_GROUNDWATER = "fresh_groundwater"
    BRACKISH_GROUNDWATER = "brackish_groundwater"
    SALINE_GROUNDWATER = "saline_groundwater"
    SURFACE_WATER = "surface_water"
    PRODUCED_WATER = "produced_water"
    FLOWBACK_WATER = "flowback_water"
    RECYCLED_WATER = "recycled_water"
    TREATED_WATER = "treated_water"
    MUNICIPAL_WATER = "municipal_water"
    UNKNOWN = "unknown"


class DisposalMethod(str, Enum):
    """Produced water disposal method."""
    SALTWATER_DISPOSAL_WELL = "saltwater_disposal_well"
    ENHANCED_RECOVERY = "enhanced_recovery"
    EVAPORATION_PIT = "evaporation_pit"
    RECYCLING_REUSE = "recycling_reuse"
    TREATMENT_DISCHARGE = "treatment_discharge"
    LAND_APPLICATION = "land_application"
    TRUCK_HAUL = "truck_haul"
    PIPELINE_GATHERING = "pipeline_gathering"


class ComplianceCategory(str, Enum):
    """Compliance scoring categories."""
    PERMIT_COMPLIANCE = "permit_compliance"
    MECHANICAL_INTEGRITY = "mechanical_integrity"
    REPORTING_COMPLIANCE = "reporting_compliance"
    ENVIRONMENTAL_IMPACT = "environmental_impact"
    SEISMICITY_RISK = "seismicity_risk"
    WATER_SOURCING = "water_sourcing"


class SeismicityRiskLevel(str, Enum):
    """Traffic light protocol level."""
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"


class FreshwaterProtectionZone(str, Enum):
    """Freshwater protection zone classification."""
    USDW_PRIMARY = "usdw_primary"
    USDW_SECONDARY = "usdw_secondary"
    RECHARGE_ZONE = "recharge_zone"
    CONTRIBUTING_ZONE = "contributing_zone"
    TRANSITION_ZONE = "transition_zone"
    NOT_IN_ZONE = "not_in_zone"


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class WaterRightIdentification(BaseModel):
    """Result of water right identification and classification."""
    record_id: str
    classification: WaterClassification
    right_type: WaterRightType
    permit_number: str = ""
    operator_name: str = ""
    county: str = ""
    aquifer: str = ""
    tds_mg_l: Optional[float] = None
    volume_bbls_per_day: Optional[float] = None
    volume_af_per_year: Optional[float] = None
    gcd_name: str = ""
    gcd_permit_required: bool = False
    surface_water_permit_required: bool = False
    injection_permit_required: bool = False
    applicable_doctrines: list[str] = Field(default_factory=list)
    regulatory_notes: list[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.LOW
    confidence: float = 1.0
    analysis_timestamp: str = ""
    determinism_hash: str = ""

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        return max(0.0, min(1.0, v))

    def compute_hash(self) -> str:
        content = json.dumps({
            "record_id": self.record_id,
            "classification": self.classification.value,
            "right_type": self.right_type.value,
            "permit": self.permit_number,
            "operator": self.operator_name,
            "county": self.county,
            "aquifer": self.aquifer,
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class GCDRuleAnalysis(BaseModel):
    """Result of groundwater conservation district rule analysis."""
    gcd_name: str
    county: str
    aquifer: str
    permit_required: bool
    permit_type: str = ""
    spacing_rule_ft: float = 0.0
    production_limit_af_per_year: float = 0.0
    allocation_factor_af_per_acre: float = 0.0
    export_restrictions: bool = False
    export_fee_per_1000_gal: float = 0.0
    metering_required: bool = True
    reporting_frequency: str = "annual"
    exempt_threshold_gpm: float = 25.0
    oilfield_provisions: str = ""
    applicable_rules: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.LOW
    analysis_timestamp: str = ""
    determinism_hash: str = ""

    def compute_hash(self) -> str:
        content = json.dumps({
            "gcd": self.gcd_name,
            "county": self.county,
            "permit_required": self.permit_required,
            "production_limit": self.production_limit_af_per_year,
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class ProducedWaterDisposalAnalysis(BaseModel):
    """Result of produced water disposal analysis."""
    well_id: str
    operator_name: str
    county: str
    disposal_method: DisposalMethod
    permit_number: str = ""
    permit_status: str = "active"
    injection_zone: str = ""
    injection_zone_depth_ft: float = 0.0
    max_injection_pressure_psi: float = 0.0
    authorized_volume_bbls_per_day: float = 0.0
    actual_volume_bbls_per_day: float = 0.0
    volume_utilization_pct: float = 0.0
    tds_mg_l: float = 0.0
    in_seismicity_review_area: bool = False
    seismicity_risk: SeismicityRiskLevel = SeismicityRiskLevel.GREEN
    last_mit_date: Optional[str] = None
    last_mit_result: str = ""
    mit_next_due: Optional[str] = None
    mit_overdue: bool = False
    compliance_issues: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.LOW
    analysis_timestamp: str = ""
    determinism_hash: str = ""

    def compute_hash(self) -> str:
        content = json.dumps({
            "well_id": self.well_id,
            "operator": self.operator_name,
            "disposal_method": self.disposal_method.value,
            "permit": self.permit_number,
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class InjectionWellComplianceReport(BaseModel):
    """Injection well compliance monitoring report."""
    well_id: str
    api_number: str = ""
    operator_name: str = ""
    county: str = ""
    well_class: str = "Class II-D"
    permit_number: str = ""
    permit_status: str = "active"
    injection_zone: str = ""
    injection_zone_depth_ft: float = 0.0
    usdw_protection_depth_ft: float = 0.0
    surface_casing_depth_ft: float = 0.0
    max_injection_pressure_psi: float = 0.0
    current_injection_pressure_psi: float = 0.0
    pressure_compliance: bool = True
    authorized_volume_bbls_per_day: float = 0.0
    actual_volume_bbls_per_day: float = 0.0
    volume_compliance: bool = True
    mechanical_integrity: MechanicalIntegrityStatus = Field(default=None)
    annular_pressure_normal: bool = True
    area_of_review_clear: bool = True
    financial_assurance_current: bool = True
    annual_report_filed: bool = True
    in_seismicity_review_area: bool = False
    seismicity_events_nearby: int = 0
    seismicity_risk: SeismicityRiskLevel = SeismicityRiskLevel.GREEN
    compliance_score: float = 100.0
    compliance_category_scores: dict[str, float] = Field(default_factory=dict)
    violations: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.LOW
    analysis_timestamp: str = ""
    determinism_hash: str = ""

    class Config:
        arbitrary_types_allowed = True

    def compute_hash(self) -> str:
        content = json.dumps({
            "well_id": self.well_id,
            "operator": self.operator_name,
            "permit": self.permit_number,
            "compliance_score": self.compliance_score,
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class MechanicalIntegrityStatus(BaseModel):
    """Mechanical integrity test status."""
    last_test_date: Optional[str] = None
    last_test_result: str = "unknown"
    test_pressure_psi: float = 0.0
    pressure_decline_pct: float = 0.0
    pass_threshold_pct: float = 5.0
    passed: bool = False
    next_test_due: Optional[str] = None
    overdue: bool = False
    tests_in_last_5_years: int = 0
    notes: str = ""


class SurfaceUseWaterAnalysis(BaseModel):
    """Surface use agreement water provisions analysis."""
    agreement_id: str
    surface_owner: str = ""
    mineral_lessee: str = ""
    county: str = ""
    tract_acres: float = 0.0
    water_source_provisions: list[str] = Field(default_factory=list)
    water_well_restrictions: list[str] = Field(default_factory=list)
    produced_water_handling: list[str] = Field(default_factory=list)
    surface_damage_provisions: list[str] = Field(default_factory=list)
    domestic_well_protection: bool = False
    domestic_well_distance_ft: Optional[float] = None
    pit_restrictions: list[str] = Field(default_factory=list)
    accommodation_doctrine_applies: bool = True
    freshwater_source_identified: bool = False
    freshwater_source_type: str = ""
    risk_factors: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.LOW
    analysis_timestamp: str = ""
    determinism_hash: str = ""

    def compute_hash(self) -> str:
        content = json.dumps({
            "agreement_id": self.agreement_id,
            "surface_owner": self.surface_owner,
            "county": self.county,
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class FreshwaterSourceReport(BaseModel):
    """Freshwater source identification report."""
    location: dict[str, float] = Field(default_factory=dict)
    county: str = ""
    aquifer_name: str = ""
    aquifer_type: str = ""
    tds_mg_l: float = 0.0
    classification: WaterClassification = WaterClassification.FRESH_GROUNDWATER
    protection_zone: FreshwaterProtectionZone = FreshwaterProtectionZone.NOT_IN_ZONE
    gcd_name: str = ""
    gcd_permit_required: bool = False
    surface_casing_depth_ft: float = 0.0
    nearby_water_wells: int = 0
    depletion_status: str = ""
    recharge_rate_in_per_year: float = 0.0
    water_quality_concerns: list[str] = Field(default_factory=list)
    alternative_sources: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.LOW
    analysis_timestamp: str = ""
    determinism_hash: str = ""

    def compute_hash(self) -> str:
        content = json.dumps({
            "county": self.county,
            "aquifer": self.aquifer_name,
            "tds": self.tds_mg_l,
            "protection_zone": self.protection_zone.value,
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class WaterTransportAnalysis(BaseModel):
    """Water transport and sale agreement analysis."""
    agreement_id: str
    agreement_type: str = ""
    buyer: str = ""
    seller: str = ""
    water_source_type: WaterClassification = WaterClassification.UNKNOWN
    source_location: str = ""
    delivery_location: str = ""
    transport_method: str = ""
    volume_bbls_per_day: float = 0.0
    volume_af_per_year: float = 0.0
    price_per_bbl: float = 0.0
    term_years: float = 0.0
    take_or_pay: bool = False
    minimum_volume_bbls_per_day: float = 0.0
    quality_specs: dict[str, Any] = Field(default_factory=dict)
    gcd_export_permit_required: bool = False
    pipeline_permit_required: bool = False
    crossing_gcd_boundaries: bool = False
    gcd_districts_involved: list[str] = Field(default_factory=list)
    regulatory_risks: list[str] = Field(default_factory=list)
    contract_risks: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.LOW
    analysis_timestamp: str = ""
    determinism_hash: str = ""

    def compute_hash(self) -> str:
        content = json.dumps({
            "agreement_id": self.agreement_id,
            "buyer": self.buyer,
            "seller": self.seller,
            "volume": self.volume_bbls_per_day,
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class ComplianceRiskReport(BaseModel):
    """Environmental compliance risk scoring report."""
    entity_id: str
    entity_type: str = ""
    entity_name: str = ""
    county: str = ""
    overall_score: float = 100.0
    risk_level: RiskLevel = RiskLevel.LOW
    category_scores: dict[str, float] = Field(default_factory=dict)
    permit_status: str = "active"
    active_violations: int = 0
    historical_violations: int = 0
    mit_status: str = "current"
    seismicity_risk: SeismicityRiskLevel = SeismicityRiskLevel.GREEN
    environmental_flags: list[str] = Field(default_factory=list)
    regulatory_exposure: list[str] = Field(default_factory=list)
    mitigation_steps: list[str] = Field(default_factory=list)
    estimated_penalty_exposure_usd: float = 0.0
    analysis_timestamp: str = ""
    determinism_hash: str = ""

    @field_validator("overall_score")
    @classmethod
    def validate_score(cls, v: float) -> float:
        return max(0.0, min(100.0, v))

    def compute_hash(self) -> str:
        content = json.dumps({
            "entity_id": self.entity_id,
            "entity_name": self.entity_name,
            "overall_score": self.overall_score,
            "risk_level": self.risk_level.value,
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class EngineHealthResponse(BaseModel):
    """Engine health check response."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    status: str = "healthy"
    uptime_seconds: float = 0.0
    total_operations: int = 0
    total_errors: int = 0
    error_rate: float = 0.0
    avg_response_time_ms: float = 0.0
    records_indexed: int = 0
    doctrines_loaded: int = 0
    terms_loaded: int = 0
    timestamp: str = ""


# ---------------------------------------------------------------------------
# Component Classes
# ---------------------------------------------------------------------------

class WaterRightClassifier:
    """Classifies water rights based on source, quality, and regulatory context."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config
        self._freshwater_tds_limit = config.get("permit_thresholds", {}).get(
            "freshwater_protection", {}
        ).get("usdw_tds_threshold_mg_l", 10000)
        self._brackish_range = config.get("permit_thresholds", {}).get(
            "brackish_water", {}
        ).get("tds_range_mg_l", [1000, 10000])
        logger.info("WaterRightClassifier initialized (USDW TDS limit: {} mg/L)", self._freshwater_tds_limit)

    def classify_by_tds(self, tds_mg_l: float) -> WaterClassification:
        """Classify water by total dissolved solids concentration."""
        if tds_mg_l < 500:
            return WaterClassification.FRESH_GROUNDWATER
        elif tds_mg_l < self._brackish_range[0]:
            return WaterClassification.FRESH_GROUNDWATER
        elif tds_mg_l < self._brackish_range[1]:
            return WaterClassification.BRACKISH_GROUNDWATER
        elif tds_mg_l < self._freshwater_tds_limit:
            return WaterClassification.SALINE_GROUNDWATER
        else:
            return WaterClassification.PRODUCED_WATER

    def classify_source(
        self,
        source_type: str,
        tds_mg_l: Optional[float] = None,
        aquifer_name: str = "",
        is_produced: bool = False,
        is_recycled: bool = False,
        is_flowback: bool = False,
    ) -> WaterClassification:
        """Classify water source using multiple attributes."""
        if is_produced:
            return WaterClassification.PRODUCED_WATER
        if is_flowback:
            return WaterClassification.FLOWBACK_WATER
        if is_recycled:
            return WaterClassification.RECYCLED_WATER

        source_lower = source_type.lower()
        if "surface" in source_lower or "river" in source_lower or "lake" in source_lower:
            return WaterClassification.SURFACE_WATER
        if "municipal" in source_lower or "city" in source_lower:
            return WaterClassification.MUNICIPAL_WATER
        if "treated" in source_lower:
            return WaterClassification.TREATED_WATER

        if tds_mg_l is not None:
            return self.classify_by_tds(tds_mg_l)

        # Classify by aquifer if TDS not available
        aquifer_lower = aquifer_name.lower()
        if any(name in aquifer_lower for name in ["ogallala", "edwards", "gulf coast"]):
            return WaterClassification.FRESH_GROUNDWATER
        if any(name in aquifer_lower for name in ["dockum", "santa rosa"]):
            return WaterClassification.BRACKISH_GROUNDWATER
        if any(name in aquifer_lower for name in ["rustler", "ellenburger"]):
            return WaterClassification.SALINE_GROUNDWATER

        return WaterClassification.UNKNOWN

    def determine_right_type(
        self,
        classification: WaterClassification,
        purpose: str = "industrial",
    ) -> WaterRightType:
        """Determine the applicable water right type based on classification and purpose."""
        if classification == WaterClassification.SURFACE_WATER:
            return WaterRightType.SURFACE_WATER_APPROPRIATION
        if classification in (
            WaterClassification.FRESH_GROUNDWATER,
            WaterClassification.BRACKISH_GROUNDWATER,
        ):
            return WaterRightType.GCD_PRODUCTION_PERMIT
        if classification == WaterClassification.PRODUCED_WATER:
            return WaterRightType.INJECTION_WELL_H1
        if classification == WaterClassification.RECYCLED_WATER:
            return WaterRightType.RECYCLING_FACILITY
        return WaterRightType.GCD_PRODUCTION_PERMIT

    def identify_permits_needed(
        self,
        classification: WaterClassification,
        county: str,
        volume_bbls_per_day: float,
        is_export: bool = False,
    ) -> list[str]:
        """Identify all permits needed based on water classification and use."""
        permits: list[str] = []

        if classification == WaterClassification.SURFACE_WATER:
            if volume_bbls_per_day > 0:
                permits.append("TCEQ Surface Water Appropriation Permit (TWC Ch. 11)")

        if classification in (
            WaterClassification.FRESH_GROUNDWATER,
            WaterClassification.BRACKISH_GROUNDWATER,
        ):
            gpm_equivalent = volume_bbls_per_day * 42 / 1440  # bbls/day to GPM
            if gpm_equivalent > 25:
                permits.append(f"GCD Production Permit ({county} County)")
            if is_export:
                permits.append(f"GCD Export Permit ({county} County)")

        if classification == WaterClassification.PRODUCED_WATER:
            permits.append("RRC H-1 Disposal Well Permit (16 TAC 3.9)")
            permits.append("RRC Financial Assurance / Plugging Bond")

        if classification == WaterClassification.TREATED_WATER:
            permits.append("TCEQ TPDES Discharge Permit (if surface discharge)")

        return permits


class GroundwaterDistrictAnalyzer:
    """Analyzes GCD rules for a specific county/location."""

    def __init__(self, config: dict[str, Any], doctrine_cache: WaterDoctrineCache) -> None:
        self._config = config
        self._doctrine_cache = doctrine_cache
        self._district_data = config.get("texas_water_districts", {}).get("permian_basin_gcds", [])
        self._district_by_county: dict[str, dict[str, Any]] = {}
        for district in self._district_data:
            self._district_by_county[district["county"].lower()] = district
        logger.info("GroundwaterDistrictAnalyzer initialized ({} districts)", len(self._district_data))

    def analyze_county(self, county: str, purpose: str = "industrial", volume_af_per_year: float = 0.0) -> GCDRuleAnalysis:
        """Analyze GCD rules for a specific county."""
        timestamp = datetime.now(timezone.utc).isoformat()
        county_lower = county.strip().lower()
        district = self._district_by_county.get(county_lower)

        if not district:
            analysis = GCDRuleAnalysis(
                gcd_name=f"Unknown GCD ({county} County)",
                county=county,
                aquifer="Unknown",
                permit_required=True,
                oilfield_provisions="GCD not in database. Recommend contacting TWDB for GCD information.",
                recommendations=[
                    f"Research GCD coverage for {county} County via TWDB GCD map",
                    "Contact county clerk for local water well registration requirements",
                    "Assume permit required until confirmed otherwise",
                ],
                risk_level=RiskLevel.MODERATE,
                analysis_timestamp=timestamp,
            )
            analysis.compute_hash()
            return analysis

        permit_required = True
        if purpose.lower() in ("domestic", "livestock"):
            exempt_gpm = district.get("exempt_domestic_gpm", 25)
            gpm_equivalent = volume_af_per_year * 325851 / 525960  # AF/yr to avg GPM
            if gpm_equivalent < exempt_gpm:
                permit_required = False

        recommendations: list[str] = []
        if purpose.lower() in ("industrial", "oilfield"):
            recommendations.append("Apply for commercial/industrial production permit before drilling water well")
            recommendations.append("Install totalizing flow meter on all permitted wells")
            recommendations.append("Submit annual production reports by deadline")
        if volume_af_per_year > 100:
            recommendations.append("Consider brackish water alternatives to reduce fresh groundwater demand")
            recommendations.append("Evaluate produced water recycling to offset fresh water consumption")

        risk_level = RiskLevel.LOW
        if volume_af_per_year > 500:
            risk_level = RiskLevel.MODERATE
            recommendations.append("Large volume request may face additional GCD scrutiny or public hearing")
        if volume_af_per_year > 1000:
            risk_level = RiskLevel.HIGH
            recommendations.append("Volume exceeds typical allocation - prepare detailed aquifer impact analysis")

        applicable_rules: list[str] = []
        gcd_rules = self._doctrine_cache.get_gcd_rules_by_county(county)
        for rule in gcd_rules:
            applicable_rules.append(f"{rule.rule_number}: {rule.title}")

        analysis = GCDRuleAnalysis(
            gcd_name=district["name"],
            county=county,
            aquifer=district.get("aquifer_primary", "Unknown"),
            permit_required=permit_required,
            permit_type="commercial_production" if purpose.lower() in ("industrial", "oilfield") else "standard_production",
            spacing_rule_ft=district.get("spacing_rule_ft", 300),
            production_limit_af_per_year=district.get("production_limit_acre_ft_per_year", 1.5) * max(volume_af_per_year / 1.5, 1),
            allocation_factor_af_per_acre=district.get("production_limit_acre_ft_per_year", 1.5),
            export_restrictions=True,
            metering_required=True,
            reporting_frequency="annual",
            exempt_threshold_gpm=district.get("exempt_domestic_gpm", 25),
            oilfield_provisions="Commercial/industrial permits required for oilfield water supply wells. Additional conditions may apply for high-volume production.",
            applicable_rules=applicable_rules,
            recommendations=recommendations,
            risk_level=risk_level,
            analysis_timestamp=timestamp,
        )
        analysis.compute_hash()
        return analysis

    def get_district_info(self, county: str) -> Optional[dict[str, Any]]:
        """Get raw district configuration data for a county."""
        return self._district_by_county.get(county.strip().lower())

    def list_districts(self) -> list[str]:
        """List all known GCD district names."""
        return [d["name"] for d in self._district_data]


class ProducedWaterTracker:
    """Tracks produced water disposal permits and operations."""

    def __init__(self, config: dict[str, Any], doctrine_cache: WaterDoctrineCache) -> None:
        self._config = config
        self._doctrine_cache = doctrine_cache
        self._pw_thresholds = config.get("permit_thresholds", {}).get("produced_water_management", {})
        self._injection_thresholds = config.get("permit_thresholds", {}).get("rrc_injection_wells", {})
        self._tracked_wells: dict[str, ProducedWaterDisposalAnalysis] = {}
        logger.info("ProducedWaterTracker initialized")

    def analyze_disposal_well(
        self,
        well_id: str,
        operator_name: str,
        county: str,
        injection_zone: str,
        injection_zone_depth_ft: float,
        authorized_volume_bbls_per_day: float,
        actual_volume_bbls_per_day: float,
        tds_mg_l: float = 250000.0,
        in_seismicity_area: bool = False,
        last_mit_date: Optional[str] = None,
        last_mit_result: str = "passed",
        permit_number: str = "",
    ) -> ProducedWaterDisposalAnalysis:
        """Analyze a disposal well for compliance and risk."""
        timestamp = datetime.now(timezone.utc).isoformat()

        # Calculate utilization
        utilization = (actual_volume_bbls_per_day / authorized_volume_bbls_per_day * 100) if authorized_volume_bbls_per_day > 0 else 0.0

        # Calculate max injection pressure
        max_pressure = injection_zone_depth_ft * 0.5  # Default 0.5 PSI/ft

        # MIT overdue check
        mit_overdue = False
        mit_next_due = None
        if last_mit_date:
            try:
                last_test = datetime.fromisoformat(last_mit_date).date()
                five_years_later = last_test.replace(year=last_test.year + 5)
                mit_next_due = five_years_later.isoformat()
                if five_years_later < date.today():
                    mit_overdue = True
            except (ValueError, TypeError):
                mit_overdue = True

        # Seismicity risk assessment
        seismicity_risk = SeismicityRiskLevel.GREEN
        if in_seismicity_area:
            if actual_volume_bbls_per_day > 20000:
                seismicity_risk = SeismicityRiskLevel.YELLOW
            if actual_volume_bbls_per_day > 30000:
                seismicity_risk = SeismicityRiskLevel.ORANGE

        # Compliance issues
        compliance_issues: list[str] = []
        if utilization > 100:
            compliance_issues.append(f"Volume exceeds authorized limit ({utilization:.0f}%)")
        if mit_overdue:
            compliance_issues.append("Mechanical integrity test overdue")
        if last_mit_result == "failed":
            compliance_issues.append("Last MIT failed - well should be shut in")

        # Recommendations
        recommendations: list[str] = []
        if utilization > 80:
            recommendations.append("Approaching volume limit - consider adding disposal capacity")
        if seismicity_risk != SeismicityRiskLevel.GREEN:
            recommendations.append("In seismicity review area - monitor TexNet data and prepare for potential curtailment")
            recommendations.append("Invest in produced water recycling to reduce disposal dependence")
        if mit_overdue:
            recommendations.append("Schedule MIT immediately to avoid permit violation")
        if not permit_number:
            recommendations.append("Verify H-1 permit number and status with RRC")

        # Risk level
        risk_level = RiskLevel.LOW
        if compliance_issues:
            risk_level = RiskLevel.MODERATE
        if mit_overdue or last_mit_result == "failed":
            risk_level = RiskLevel.HIGH
        if seismicity_risk in (SeismicityRiskLevel.ORANGE, SeismicityRiskLevel.RED):
            risk_level = RiskLevel.CRITICAL

        analysis = ProducedWaterDisposalAnalysis(
            well_id=well_id,
            operator_name=operator_name,
            county=county,
            disposal_method=DisposalMethod.SALTWATER_DISPOSAL_WELL,
            permit_number=permit_number,
            injection_zone=injection_zone,
            injection_zone_depth_ft=injection_zone_depth_ft,
            max_injection_pressure_psi=max_pressure,
            authorized_volume_bbls_per_day=authorized_volume_bbls_per_day,
            actual_volume_bbls_per_day=actual_volume_bbls_per_day,
            volume_utilization_pct=utilization,
            tds_mg_l=tds_mg_l,
            in_seismicity_review_area=in_seismicity_area,
            seismicity_risk=seismicity_risk,
            last_mit_date=last_mit_date,
            last_mit_result=last_mit_result,
            mit_next_due=mit_next_due,
            mit_overdue=mit_overdue,
            compliance_issues=compliance_issues,
            recommendations=recommendations,
            risk_level=risk_level,
            analysis_timestamp=timestamp,
        )
        analysis.compute_hash()
        self._tracked_wells[well_id] = analysis
        return analysis

    def get_tracked_well(self, well_id: str) -> Optional[ProducedWaterDisposalAnalysis]:
        return self._tracked_wells.get(well_id)

    def get_all_tracked(self) -> list[ProducedWaterDisposalAnalysis]:
        return list(self._tracked_wells.values())

    def get_high_risk_wells(self) -> list[ProducedWaterDisposalAnalysis]:
        return [
            w for w in self._tracked_wells.values()
            if w.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)
        ]


class InjectionWellMonitor:
    """Monitors injection well compliance status."""

    def __init__(self, config: dict[str, Any], doctrine_cache: WaterDoctrineCache) -> None:
        self._config = config
        self._doctrine_cache = doctrine_cache
        self._seismicity_config = config.get("seismicity_monitoring", {})
        self._scoring_config = config.get("compliance_scoring", {})
        logger.info("InjectionWellMonitor initialized")

    def generate_compliance_report(
        self,
        well_id: str,
        api_number: str,
        operator_name: str,
        county: str,
        permit_number: str,
        injection_zone: str,
        injection_zone_depth_ft: float,
        surface_casing_depth_ft: float,
        max_injection_pressure_psi: float,
        current_injection_pressure_psi: float,
        authorized_volume_bbls_per_day: float,
        actual_volume_bbls_per_day: float,
        last_mit_date: Optional[str] = None,
        last_mit_result: str = "passed",
        annular_pressure_psi: float = 0.0,
        annual_report_filed: bool = True,
        bond_current: bool = True,
        in_seismicity_area: bool = False,
        nearby_seismic_events: int = 0,
        violations: Optional[list[str]] = None,
    ) -> InjectionWellComplianceReport:
        """Generate a comprehensive injection well compliance report."""
        timestamp = datetime.now(timezone.utc).isoformat()

        # Pressure compliance
        pressure_compliance = current_injection_pressure_psi <= max_injection_pressure_psi

        # Volume compliance
        volume_compliance = actual_volume_bbls_per_day <= authorized_volume_bbls_per_day

        # MIT status
        mit_status = MechanicalIntegrityStatus(
            last_test_date=last_mit_date,
            last_test_result=last_mit_result,
            passed=last_mit_result == "passed",
        )
        if last_mit_date:
            try:
                last_test = datetime.fromisoformat(last_mit_date).date()
                five_years_later = last_test.replace(year=last_test.year + 5)
                mit_status.next_test_due = five_years_later.isoformat()
                mit_status.overdue = five_years_later < date.today()
            except (ValueError, TypeError):
                mit_status.overdue = True
        else:
            mit_status.overdue = True

        # Annular pressure check
        annular_normal = annular_pressure_psi < 200  # 200 PSI threshold

        # Seismicity risk
        seismicity_risk = SeismicityRiskLevel.GREEN
        if in_seismicity_area:
            if nearby_seismic_events > 0:
                seismicity_risk = SeismicityRiskLevel.YELLOW
            if nearby_seismic_events > 3:
                seismicity_risk = SeismicityRiskLevel.ORANGE
            if nearby_seismic_events > 5:
                seismicity_risk = SeismicityRiskLevel.RED

        # Calculate category scores
        category_scores: dict[str, float] = {}

        # Permit compliance score
        permit_score = 100.0
        if not pressure_compliance:
            permit_score -= 30.0
        if not volume_compliance:
            permit_score -= 30.0
        category_scores[ComplianceCategory.PERMIT_COMPLIANCE.value] = max(0, permit_score)

        # Mechanical integrity score
        mit_score = 100.0
        if mit_status.overdue:
            mit_score -= 50.0
        if not mit_status.passed:
            mit_score -= 50.0
        if not annular_normal:
            mit_score -= 25.0
        category_scores[ComplianceCategory.MECHANICAL_INTEGRITY.value] = max(0, mit_score)

        # Reporting score
        report_score = 100.0
        if not annual_report_filed:
            report_score -= 40.0
        if not bond_current:
            report_score -= 30.0
        category_scores[ComplianceCategory.REPORTING_COMPLIANCE.value] = max(0, report_score)

        # Environmental score
        env_score = 100.0
        if violations:
            env_score -= min(len(violations) * 15, 60)
        category_scores[ComplianceCategory.ENVIRONMENTAL_IMPACT.value] = max(0, env_score)

        # Seismicity score
        seis_score = 100.0
        seis_map = {
            SeismicityRiskLevel.GREEN: 0,
            SeismicityRiskLevel.YELLOW: 25,
            SeismicityRiskLevel.ORANGE: 50,
            SeismicityRiskLevel.RED: 75,
        }
        seis_score -= seis_map.get(seismicity_risk, 0)
        category_scores[ComplianceCategory.SEISMICITY_RISK.value] = max(0, seis_score)

        # Water sourcing score
        category_scores[ComplianceCategory.WATER_SOURCING.value] = 100.0

        # Calculate weighted overall score
        weights = {cat["category"]: cat["weight"] for cat in self._scoring_config.get("risk_categories", [])}
        overall_score = 0.0
        total_weight = 0.0
        for cat_name, cat_score in category_scores.items():
            weight = weights.get(cat_name, 1.0 / len(category_scores))
            overall_score += cat_score * weight
            total_weight += weight
        if total_weight > 0:
            overall_score /= total_weight
        overall_score = overall_score  # Already weighted

        # Determine risk level from overall score
        risk_level = RiskLevel.LOW
        if overall_score < 80:
            risk_level = RiskLevel.MODERATE
        if overall_score < 60:
            risk_level = RiskLevel.HIGH
        if overall_score < 40:
            risk_level = RiskLevel.CRITICAL

        # Build recommendations
        recommendations: list[str] = []
        if not pressure_compliance:
            recommendations.append("Reduce injection pressure to authorized maximum immediately")
        if not volume_compliance:
            recommendations.append("Reduce injection volume to authorized maximum")
        if mit_status.overdue:
            recommendations.append("Schedule mechanical integrity test immediately")
        if not mit_status.passed:
            recommendations.append("Well should be shut in until MIT passes - repair casing/packer")
        if not annular_normal:
            recommendations.append("Investigate elevated annular pressure - possible tubing/packer leak")
        if not annual_report_filed:
            recommendations.append("File annual H-10 report immediately")
        if not bond_current:
            recommendations.append("Renew financial assurance / plugging bond")
        if seismicity_risk != SeismicityRiskLevel.GREEN:
            recommendations.append("Monitor TexNet seismicity data daily")
            if seismicity_risk in (SeismicityRiskLevel.ORANGE, SeismicityRiskLevel.RED):
                recommendations.append("Contact RRC regarding potential volume curtailment order")

        report = InjectionWellComplianceReport(
            well_id=well_id,
            api_number=api_number,
            operator_name=operator_name,
            county=county,
            permit_number=permit_number,
            injection_zone=injection_zone,
            injection_zone_depth_ft=injection_zone_depth_ft,
            usdw_protection_depth_ft=surface_casing_depth_ft,
            surface_casing_depth_ft=surface_casing_depth_ft,
            max_injection_pressure_psi=max_injection_pressure_psi,
            current_injection_pressure_psi=current_injection_pressure_psi,
            pressure_compliance=pressure_compliance,
            authorized_volume_bbls_per_day=authorized_volume_bbls_per_day,
            actual_volume_bbls_per_day=actual_volume_bbls_per_day,
            volume_compliance=volume_compliance,
            mechanical_integrity=mit_status,
            annular_pressure_normal=annular_normal,
            financial_assurance_current=bond_current,
            annual_report_filed=annual_report_filed,
            in_seismicity_review_area=in_seismicity_area,
            seismicity_events_nearby=nearby_seismic_events,
            seismicity_risk=seismicity_risk,
            compliance_score=overall_score,
            compliance_category_scores=category_scores,
            violations=violations or [],
            recommendations=recommendations,
            risk_level=risk_level,
            analysis_timestamp=timestamp,
        )
        report.compute_hash()
        return report


class SurfaceUseWaterAnalyzer:
    """Analyzes surface use agreements for water-related provisions."""

    def __init__(self, doctrine_cache: WaterDoctrineCache) -> None:
        self._doctrine_cache = doctrine_cache
        logger.info("SurfaceUseWaterAnalyzer initialized")

    def analyze_agreement(
        self,
        agreement_id: str,
        surface_owner: str,
        mineral_lessee: str,
        county: str,
        tract_acres: float,
        has_domestic_well: bool = False,
        domestic_well_distance_ft: Optional[float] = None,
        water_source_provisions: Optional[list[str]] = None,
        produced_water_handling: Optional[list[str]] = None,
        pit_allowed: bool = True,
    ) -> SurfaceUseWaterAnalysis:
        """Analyze a surface use agreement for water-related provisions and risks."""
        timestamp = datetime.now(timezone.utc).isoformat()

        risk_factors: list[str] = []
        recommendations: list[str] = []
        water_well_restrictions: list[str] = []
        pit_restrictions: list[str] = []

        # Accommodation doctrine analysis
        if has_domestic_well:
            risk_factors.append("Surface owner has domestic water well - accommodation doctrine applies")
            if domestic_well_distance_ft and domestic_well_distance_ft < 500:
                risk_factors.append(f"Domestic well within {domestic_well_distance_ft:.0f} ft of proposed operations")
                recommendations.append("Site produced water facilities >500 ft from domestic well")
                recommendations.append("Conduct baseline water quality test on domestic well before operations begin")
            water_well_restrictions.append("Operations must not impair domestic well per Merriman v. XTO (2013)")
            water_well_restrictions.append("Alternative facility locations required if domestic well would be affected")

        if tract_acres < 40:
            risk_factors.append("Small tract (<40 acres) limits facility siting options")
            recommendations.append("Conduct detailed surface survey to map all constraints before facility design")

        if not pit_allowed:
            pit_restrictions.append("Surface use agreement prohibits open pits")
            recommendations.append("Use closed-loop tank systems for all fluids")
        else:
            pit_restrictions.append("Pits must be lined with synthetic liner (min 12 mil)")
            pit_restrictions.append("Freshwater pits: max 500 bbls without additional permitting")

        # Produced water provisions
        produced_handling = produced_water_handling or []
        if not produced_handling:
            produced_handling = [
                "Produced water must be stored in closed tanks or lined pits",
                "Spills must be cleaned up immediately and reported per RRC Rule 20",
                "All tank batteries must have secondary containment (berm/dike)",
            ]
            recommendations.append("Agreement silent on produced water - add explicit handling provisions")

        surface_damage_provisions = [
            "Operator responsible for surface restoration after operations cease",
            "Soil contamination from produced water spills must be remediated to background levels",
            "Annual surface damage payments apply per agreement terms",
        ]

        risk_level = RiskLevel.LOW
        if has_domestic_well and (not domestic_well_distance_ft or domestic_well_distance_ft < 500):
            risk_level = RiskLevel.HIGH
        elif risk_factors:
            risk_level = RiskLevel.MODERATE

        analysis = SurfaceUseWaterAnalysis(
            agreement_id=agreement_id,
            surface_owner=surface_owner,
            mineral_lessee=mineral_lessee,
            county=county,
            tract_acres=tract_acres,
            water_source_provisions=water_source_provisions or [],
            water_well_restrictions=water_well_restrictions,
            produced_water_handling=produced_handling,
            surface_damage_provisions=surface_damage_provisions,
            domestic_well_protection=has_domestic_well,
            domestic_well_distance_ft=domestic_well_distance_ft,
            pit_restrictions=pit_restrictions,
            accommodation_doctrine_applies=has_domestic_well,
            risk_factors=risk_factors,
            recommendations=recommendations,
            risk_level=risk_level,
            analysis_timestamp=timestamp,
        )
        analysis.compute_hash()
        return analysis


class FreshwaterSourceIdentifier:
    """Identifies freshwater sources and protection zones."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config
        self._aquifer_data = config.get("aquifer_zones", {}).get("major_aquifers", [])
        self._aquifer_by_name: dict[str, dict[str, Any]] = {}
        for aq in self._aquifer_data:
            self._aquifer_by_name[aq["name"].lower()] = aq
        logger.info("FreshwaterSourceIdentifier initialized ({} aquifers)", len(self._aquifer_data))

    def identify_source(
        self,
        county: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        aquifer_name: str = "",
        tds_mg_l: Optional[float] = None,
        depth_ft: Optional[float] = None,
    ) -> FreshwaterSourceReport:
        """Identify freshwater sources at a given location."""
        timestamp = datetime.now(timezone.utc).isoformat()

        # Find aquifer info
        aquifer_info = self._aquifer_by_name.get(aquifer_name.lower(), {})
        if not aquifer_info and not aquifer_name:
            # Default to Ogallala for Permian Basin counties
            permian_counties = ["midland", "ector", "martin", "andrews", "gaines", "winkler"]
            if county.lower() in permian_counties:
                aquifer_name = "Ogallala"
                aquifer_info = self._aquifer_by_name.get("ogallala", {})
            else:
                aquifer_name = "Unknown"

        # Classify water
        if tds_mg_l is not None:
            if tds_mg_l < 1000:
                classification = WaterClassification.FRESH_GROUNDWATER
            elif tds_mg_l < 10000:
                classification = WaterClassification.BRACKISH_GROUNDWATER
            else:
                classification = WaterClassification.SALINE_GROUNDWATER
        else:
            tds_range = aquifer_info.get("tds_range_mg_l", [500, 1500])
            avg_tds = sum(tds_range) / 2
            if avg_tds < 1000:
                classification = WaterClassification.FRESH_GROUNDWATER
            elif avg_tds < 10000:
                classification = WaterClassification.BRACKISH_GROUNDWATER
            else:
                classification = WaterClassification.SALINE_GROUNDWATER
            tds_mg_l = avg_tds

        # Determine protection zone
        protection_zone = FreshwaterProtectionZone.NOT_IN_ZONE
        if tds_mg_l < 10000:
            protection_zone = FreshwaterProtectionZone.USDW_PRIMARY
        elif tds_mg_l < 3000:
            protection_zone = FreshwaterProtectionZone.USDW_PRIMARY

        # Depletion status
        depletion = aquifer_info.get("depletion_concern", "UNKNOWN")
        recharge = aquifer_info.get("recharge_rate_inches_per_year", 0.0)

        # Water quality concerns
        concerns: list[str] = []
        if tds_mg_l and tds_mg_l > 500:
            concerns.append(f"TDS ({tds_mg_l:.0f} mg/L) exceeds EPA secondary drinking water standard (500 mg/L)")
        if depletion in ("HIGH", "CRITICAL"):
            concerns.append(f"Aquifer depletion rated {depletion} - long-term supply risk")
        if recharge < 0.5:
            concerns.append(f"Very low recharge rate ({recharge} in/yr) - aquifer is essentially non-renewable")

        # Alternative sources
        alternatives: list[str] = []
        if classification == WaterClassification.FRESH_GROUNDWATER:
            alternatives.append("Brackish groundwater (Dockum, Rustler) with basic treatment")
            alternatives.append("Recycled produced water for oilfield use")
            alternatives.append("Municipal effluent (treated wastewater)")
        if classification == WaterClassification.BRACKISH_GROUNDWATER:
            alternatives.append("Use directly for frac operations (may need chemistry adjustment)")
            alternatives.append("Blend with recycled produced water")

        # Recommendations
        recommendations: list[str] = []
        if protection_zone == FreshwaterProtectionZone.USDW_PRIMARY:
            recommendations.append("Ensure surface casing set below deepest freshwater per GPD letter")
            recommendations.append("Maintain secondary containment on all facilities within USDW zone")
        if depletion in ("HIGH", "CRITICAL"):
            recommendations.append("Minimize fresh groundwater consumption - use alternatives where feasible")
        recommendations.append("Obtain GCD permit before drilling water supply well")
        recommendations.append("Conduct baseline water quality analysis at permit and every 5 years")

        report = FreshwaterSourceReport(
            location={"latitude": latitude or 0.0, "longitude": longitude or 0.0},
            county=county,
            aquifer_name=aquifer_name,
            aquifer_type=aquifer_info.get("type", "unknown"),
            tds_mg_l=tds_mg_l,
            classification=classification,
            protection_zone=protection_zone,
            gcd_name="",
            gcd_permit_required=True,
            surface_casing_depth_ft=depth_ft or 0.0,
            depletion_status=depletion,
            recharge_rate_in_per_year=recharge,
            water_quality_concerns=concerns,
            alternative_sources=alternatives,
            recommendations=recommendations,
            risk_level=RiskLevel.MODERATE if depletion in ("HIGH", "CRITICAL") else RiskLevel.LOW,
            analysis_timestamp=timestamp,
        )
        report.compute_hash()
        return report


class WaterTransportAnalyzer:
    """Analyzes water transport and sale agreements."""

    def __init__(self, config: dict[str, Any], doctrine_cache: WaterDoctrineCache) -> None:
        self._config = config
        self._doctrine_cache = doctrine_cache
        self._transport_config = config.get("permit_thresholds", {}).get("water_transport", {})
        logger.info("WaterTransportAnalyzer initialized")

    def analyze_agreement(
        self,
        agreement_id: str,
        agreement_type: str,
        buyer: str,
        seller: str,
        water_source_type: WaterClassification,
        source_county: str,
        delivery_county: str,
        transport_method: str,
        volume_bbls_per_day: float,
        price_per_bbl: float,
        term_years: float,
        take_or_pay: bool = False,
        minimum_volume_bbls_per_day: float = 0.0,
        quality_specs: Optional[dict[str, Any]] = None,
    ) -> WaterTransportAnalysis:
        """Analyze a water transport/sale agreement for regulatory and contract risks."""
        timestamp = datetime.now(timezone.utc).isoformat()

        # Check if crossing GCD boundaries
        crossing_gcd = source_county.lower() != delivery_county.lower()
        gcd_districts: list[str] = []
        if crossing_gcd:
            gcd_districts.append(f"{source_county} County GCD (source)")
            gcd_districts.append(f"{delivery_county} County GCD (delivery)")

        # Export permit required?
        export_permit = crossing_gcd and water_source_type in (
            WaterClassification.FRESH_GROUNDWATER,
            WaterClassification.BRACKISH_GROUNDWATER,
        )

        # Pipeline permit
        pipeline_permit = transport_method.lower() in ("pipeline", "gathering_system")

        # Volume conversion
        af_per_year = volume_bbls_per_day * 365.25 / 7758.0  # bbls to AF

        # Regulatory risks
        regulatory_risks: list[str] = []
        if export_permit:
            regulatory_risks.append(f"GCD export permit required for cross-county transport ({source_county} to {delivery_county})")
            regulatory_risks.append("Export fees and conditions may apply")
        if pipeline_permit:
            regulatory_risks.append("RRC pipeline permit required for produced water pipeline")
            regulatory_risks.append("Surface owner right-of-way agreements needed along pipeline route")
        if water_source_type == WaterClassification.PRODUCED_WATER:
            regulatory_risks.append("Produced water transport requires DOT hazmat manifesting if H2S present")
            regulatory_risks.append("Truck transport limited to 130 bbls per truck (DOT)")
        if volume_bbls_per_day > 10000:
            regulatory_risks.append("Large volume transport may trigger additional environmental review")

        # Contract risks
        contract_risks: list[str] = []
        if take_or_pay and minimum_volume_bbls_per_day > 0:
            annual_obligation = minimum_volume_bbls_per_day * 365.25 * price_per_bbl
            contract_risks.append(
                f"Take-or-pay obligation: ${annual_obligation:,.0f}/year minimum"
            )
        if term_years > 3:
            contract_risks.append(f"Long-term commitment ({term_years:.0f} years) - verify water availability for full term")
        if not quality_specs:
            contract_risks.append("No water quality specifications defined - add TDS, TSS, bacteria, pH requirements")
        if water_source_type == WaterClassification.RECYCLED_WATER and not quality_specs:
            contract_risks.append("CRITICAL: Recycled water without quality specs creates completion risk")

        # Recommendations
        recommendations: list[str] = []
        if export_permit:
            recommendations.append("Obtain GCD export permit before initiating transport")
            recommendations.append("Budget for export surcharge ($0.25-$1.00 per 1,000 gallons typical)")
        if pipeline_permit:
            recommendations.append("File pipeline permit application with RRC")
            recommendations.append("Conduct hydrostatic pressure test before commissioning pipeline")
            recommendations.append("Implement corrosion protection and leak detection systems")
        if take_or_pay:
            recommendations.append("Verify water demand forecast supports minimum volume commitment")
        if not quality_specs:
            recommendations.append("Add quality specifications: TDS, TSS, pH, bacteria, hardness, scaling ions")
        recommendations.append("Include force majeure clause covering drought, regulatory curtailment, and equipment failure")
        recommendations.append("Define metering standards and dispute resolution process")

        # Risk level
        risk_level = RiskLevel.LOW
        if regulatory_risks:
            risk_level = RiskLevel.MODERATE
        if contract_risks and take_or_pay:
            risk_level = RiskLevel.MODERATE
        if any("CRITICAL" in r for r in contract_risks):
            risk_level = RiskLevel.HIGH

        analysis = WaterTransportAnalysis(
            agreement_id=agreement_id,
            agreement_type=agreement_type,
            buyer=buyer,
            seller=seller,
            water_source_type=water_source_type,
            source_location=source_county,
            delivery_location=delivery_county,
            transport_method=transport_method,
            volume_bbls_per_day=volume_bbls_per_day,
            volume_af_per_year=af_per_year,
            price_per_bbl=price_per_bbl,
            term_years=term_years,
            take_or_pay=take_or_pay,
            minimum_volume_bbls_per_day=minimum_volume_bbls_per_day,
            quality_specs=quality_specs or {},
            gcd_export_permit_required=export_permit,
            pipeline_permit_required=pipeline_permit,
            crossing_gcd_boundaries=crossing_gcd,
            gcd_districts_involved=gcd_districts,
            regulatory_risks=regulatory_risks,
            contract_risks=contract_risks,
            recommendations=recommendations,
            risk_level=risk_level,
            analysis_timestamp=timestamp,
        )
        analysis.compute_hash()
        return analysis


class ComplianceRiskScorer:
    """Scores environmental compliance risk for operators, wells, and facilities."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config
        self._scoring_config = config.get("compliance_scoring", {})
        self._risk_categories = self._scoring_config.get("risk_categories", [])
        self._risk_thresholds = self._scoring_config.get("risk_thresholds", {})
        self._auto_flags = self._scoring_config.get("auto_flag_conditions", [])
        logger.info("ComplianceRiskScorer initialized ({} categories)", len(self._risk_categories))

    def score_operator(
        self,
        operator_id: str,
        operator_name: str,
        county: str,
        active_permits: int = 0,
        expired_permits: int = 0,
        active_violations: int = 0,
        historical_violations: int = 0,
        wells_with_mit_current: int = 0,
        wells_with_mit_overdue: int = 0,
        wells_with_mit_failed: int = 0,
        annual_reports_filed: int = 0,
        annual_reports_due: int = 0,
        in_seismicity_area: bool = False,
        seismic_events_nearby: int = 0,
        spills_last_year: int = 0,
        remediation_pending: int = 0,
    ) -> ComplianceRiskReport:
        """Score an operator's overall compliance risk."""
        timestamp = datetime.now(timezone.utc).isoformat()

        category_scores: dict[str, float] = {}

        # Permit compliance
        permit_score = 100.0
        if expired_permits > 0:
            permit_score -= min(expired_permits * 15, 60)
        total_permits = active_permits + expired_permits
        if total_permits > 0 and expired_permits / total_permits > 0.1:
            permit_score -= 20
        category_scores[ComplianceCategory.PERMIT_COMPLIANCE.value] = max(0, permit_score)

        # Mechanical integrity
        mit_score = 100.0
        total_wells = wells_with_mit_current + wells_with_mit_overdue + wells_with_mit_failed
        if total_wells > 0:
            overdue_pct = (wells_with_mit_overdue + wells_with_mit_failed) / total_wells
            mit_score -= overdue_pct * 80
        if wells_with_mit_failed > 0:
            mit_score -= min(wells_with_mit_failed * 20, 50)
        category_scores[ComplianceCategory.MECHANICAL_INTEGRITY.value] = max(0, mit_score)

        # Reporting
        report_score = 100.0
        if annual_reports_due > 0:
            filing_rate = annual_reports_filed / annual_reports_due
            report_score = filing_rate * 100
        category_scores[ComplianceCategory.REPORTING_COMPLIANCE.value] = max(0, report_score)

        # Environmental
        env_score = 100.0
        if active_violations > 0:
            env_score -= min(active_violations * 15, 60)
        if spills_last_year > 0:
            env_score -= min(spills_last_year * 10, 40)
        if remediation_pending > 0:
            env_score -= min(remediation_pending * 10, 30)
        category_scores[ComplianceCategory.ENVIRONMENTAL_IMPACT.value] = max(0, env_score)

        # Seismicity
        seis_score = 100.0
        if in_seismicity_area:
            seis_score -= 10
            if seismic_events_nearby > 0:
                seis_score -= min(seismic_events_nearby * 10, 50)
        category_scores[ComplianceCategory.SEISMICITY_RISK.value] = max(0, seis_score)

        # Water sourcing
        category_scores[ComplianceCategory.WATER_SOURCING.value] = 100.0

        # Weighted overall
        weights = {cat["category"]: cat["weight"] for cat in self._risk_categories}
        overall = 0.0
        for cat_name, cat_score in category_scores.items():
            weight = weights.get(cat_name, 1.0 / max(len(category_scores), 1))
            overall += cat_score * weight

        # Determine risk level
        risk_level = RiskLevel.LOW
        thresholds = self._risk_thresholds
        if overall < thresholds.get("moderate", [60, 79])[0]:
            risk_level = RiskLevel.HIGH
        elif overall < thresholds.get("low", [80, 100])[0]:
            risk_level = RiskLevel.MODERATE
        if overall < thresholds.get("critical", [0, 39])[1]:
            risk_level = RiskLevel.CRITICAL

        # Auto-flags
        env_flags: list[str] = []
        if expired_permits > 0:
            env_flags.append(f"{expired_permits} expired permit(s)")
        if wells_with_mit_overdue > 0:
            env_flags.append(f"{wells_with_mit_overdue} well(s) with overdue MIT")
        if wells_with_mit_failed > 0:
            env_flags.append(f"{wells_with_mit_failed} well(s) with failed MIT")
        if spills_last_year > 0:
            env_flags.append(f"{spills_last_year} spill(s) in last year")
        if remediation_pending > 0:
            env_flags.append(f"{remediation_pending} pending remediation(s)")

        # Regulatory exposure
        regulatory_exposure: list[str] = []
        if active_violations > 0:
            regulatory_exposure.append(f"Active RRC/TCEQ violations: {active_violations}")
        if wells_with_mit_failed > 0:
            regulatory_exposure.append("Wells with failed MIT subject to shut-in order")
        if expired_permits > 0:
            regulatory_exposure.append("Operating under expired permits subject to enforcement")

        # Penalty estimate
        penalty_estimate = (
            active_violations * 10000 +
            wells_with_mit_failed * 25000 +
            expired_permits * 5000 +
            spills_last_year * 15000
        )

        # Mitigation steps
        mitigation: list[str] = []
        if wells_with_mit_overdue > 0:
            mitigation.append(f"Schedule MIT for {wells_with_mit_overdue} overdue well(s) immediately")
        if expired_permits > 0:
            mitigation.append(f"Renew {expired_permits} expired permit(s)")
        if annual_reports_filed < annual_reports_due:
            mitigation.append(f"File {annual_reports_due - annual_reports_filed} overdue annual report(s)")
        if spills_last_year > 0:
            mitigation.append("Review and update spill prevention plans")
        if remediation_pending > 0:
            mitigation.append("Accelerate pending remediation activities")
        if in_seismicity_area:
            mitigation.append("Implement daily TexNet monitoring and seismicity response plan")

        report = ComplianceRiskReport(
            entity_id=operator_id,
            entity_type="operator",
            entity_name=operator_name,
            county=county,
            overall_score=overall,
            risk_level=risk_level,
            category_scores=category_scores,
            permit_status="active" if expired_permits == 0 else "some_expired",
            active_violations=active_violations,
            historical_violations=historical_violations,
            mit_status="current" if wells_with_mit_overdue == 0 and wells_with_mit_failed == 0 else "overdue",
            seismicity_risk=SeismicityRiskLevel.YELLOW if in_seismicity_area and seismic_events_nearby > 0 else SeismicityRiskLevel.GREEN,
            environmental_flags=env_flags,
            regulatory_exposure=regulatory_exposure,
            mitigation_steps=mitigation,
            estimated_penalty_exposure_usd=penalty_estimate,
            analysis_timestamp=timestamp,
        )
        report.compute_hash()
        return report


# ---------------------------------------------------------------------------
# Main Engine
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# TIE-20 Component Implementation Classes
# ---------------------------------------------------------------------------

class WaterRightsCoverageMap:
    """TIE-20 Component 10: Coverage map - track triggered vs missed doctrines."""

    def __init__(self, doctrine_cache: WaterDoctrineCache) -> None:
        self._cache = doctrine_cache
        self._query_log: List[Dict[str, Any]] = []

    def analyze_coverage(
        self,
        query: str,
        triggered_doctrine_ids: List[str],
    ) -> List[CoverageGap]:
        """Identify coverage gaps - doctrines that should have been considered."""
        gaps: List[CoverageGap] = []

        # Extract key water rights concepts
        query_lower = query.lower()
        all_doctrines = self._cache.get_all_doctrines()

        # Check for groundwater gaps
        if any(term in query_lower for term in ["groundwater", "aquifer", "well", "gcd"]):
            groundwater_doctrines = [
                d.doctrine_id for d in all_doctrines
                if d.category in (DoctrineCategory.GROUNDWATER_CAPTURE, DoctrineCategory.GROUNDWATER_CONSERVATION_DISTRICT)
            ]
            missed = [d for d in groundwater_doctrines if d not in triggered_doctrine_ids]
            if missed:
                gaps.append(CoverageGap(
                    query_aspect="groundwater_rights",
                    triggered_doctrines=triggered_doctrine_ids,
                    missed_doctrines=missed[:5],
                    gap_severity="moderate" if len(missed) > 3 else "minor",
                    recommended_research="Review Rule of Capture doctrine and applicable GCD regulations",
                ))

        # Check for surface water gaps
        if any(term in query_lower for term in ["surface water", "river", "stream", "tceq permit"]):
            surface_doctrines = [
                d.doctrine_id for d in all_doctrines
                if d.category == DoctrineCategory.SURFACE_WATER_APPROPRIATION
            ]
            missed = [d for d in surface_doctrines if d not in triggered_doctrine_ids]
            if missed:
                gaps.append(CoverageGap(
                    query_aspect="surface_water_rights",
                    triggered_doctrines=triggered_doctrine_ids,
                    missed_doctrines=missed[:5],
                    gap_severity="critical" if "permit" in query_lower else "moderate",
                    recommended_research="Review TWC Chapter 11 surface water appropriation requirements",
                ))

        # Check for produced water gaps
        if any(term in query_lower for term in ["produced water", "disposal", "injection", "saltwater"]):
            disposal_doctrines = [
                d.doctrine_id for d in all_doctrines
                if d.category == DoctrineCategory.PRODUCED_WATER_DISPOSAL
            ]
            missed = [d for d in disposal_doctrines if d not in triggered_doctrine_ids]
            if missed:
                gaps.append(CoverageGap(
                    query_aspect="produced_water_disposal",
                    triggered_doctrines=triggered_doctrine_ids,
                    missed_doctrines=missed[:5],
                    gap_severity="critical",
                    recommended_research="Review RRC 16 TAC §3.9 injection well requirements",
                ))

        # Check for aquifer protection gaps
        if any(term in query_lower for term in ["edwards", "trinity", "ogallala", "carrizo", "aquifer protection"]):
            aquifer_doctrines = [
                d.doctrine_id for d in all_doctrines
                if d.category == DoctrineCategory.AQUIFER_PROTECTION_ZONE
            ]
            missed = [d for d in aquifer_doctrines if d not in triggered_doctrine_ids]
            if missed:
                gaps.append(CoverageGap(
                    query_aspect="aquifer_protection",
                    triggered_doctrines=triggered_doctrine_ids,
                    missed_doctrines=missed[:5],
                    gap_severity="critical",
                    recommended_research="Review Edwards Aquifer Authority regulations and contributing/recharge zone restrictions",
                ))

        self._query_log.append({
            "query": query,
            "triggered": triggered_doctrine_ids,
            "gaps": len(gaps),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        return gaps


class WaterRightsDriftWatcher:
    """TIE-20 Component 9: Drift watcher - detect doctrine drift over time."""

    def __init__(self) -> None:
        self._observations: List[DriftObservation] = []
        self._baseline_date = "2024-01-01"
        self._load_known_drifts()

    def _load_known_drifts(self) -> None:
        """Load known recent changes in Texas water law."""
        # SB 2 (2023) - groundwater conservation districts
        self._observations.append(DriftObservation(
            doctrine_id="GCD_SB2_2023",
            observation_date="2023-09-01",
            drift_type="statutory_change",
            drift_severity="major",
            description="SB 2 (88th Legislature) amended TWC §36.1071 - GCD desired future conditions now require 30-year planning horizon",
            source_citation="Tex. Water Code §36.1071 (effective Sept 1, 2023)",
            action_required="Update GCD permit analysis to reference 30-year DFC timeline",
        ))

        # HB 3246 (2023) - brackish groundwater production zones
        self._observations.append(DriftObservation(
            doctrine_id="BGPZ_HB3246_2023",
            observation_date="2023-09-01",
            drift_type="statutory_change",
            drift_severity="moderate",
            description="HB 3246 (88th Legislature) created new brackish groundwater production zones - expedited permitting for designated zones",
            source_citation="Tex. Water Code §36.454 (effective Sept 1, 2023)",
            action_required="Check if project area falls within designated BGPZ for permit streamlining",
        ))

        # TCEQ rule changes - OSSF and wastewater
        self._observations.append(DriftObservation(
            doctrine_id="TCEQ_OSSF_2024",
            observation_date="2024-01-15",
            drift_type="regulatory_amendment",
            drift_severity="minor",
            description="30 TAC Chapter 285 amendments - revised OSSF setback requirements from water wells",
            source_citation="30 TAC §285.91(10) (effective Jan 15, 2024)",
            action_required="Verify septic system setbacks from water wells meet new 150-foot standard",
        ))

        # Edwards Aquifer Authority - permit amendments
        self._observations.append(DriftObservation(
            doctrine_id="EAA_PERMIT_2023",
            observation_date="2023-06-01",
            drift_type="administrative_order",
            drift_severity="major",
            description="EAA reduced initial regular permits (IRP) due to aquifer levels - new applications suspended",
            source_citation="EAA Board Resolution 2023-06-15",
            action_required="CRITICAL: No new Edwards Aquifer permits available - must use existing permitted sources or alternative aquifers",
        ))

        # Railroad Commission - injection well seismicity
        self._observations.append(DriftObservation(
            doctrine_id="RRC_SEISMIC_2023",
            observation_date="2023-11-01",
            drift_type="administrative_order",
            drift_severity="major",
            description="RRC issued disposal well restrictions in Midland Basin due to seismicity - 16 TAC §3.9 emergency rules",
            source_citation="RRC Oil and Gas Docket No. 08-XXXX (Nov 2023)",
            action_required="All Midland Basin disposal wells require seismic monitoring and pressure/volume limits",
        ))

    def check_for_drift(self, doctrine_id: str) -> List[DriftObservation]:
        """Check if a specific doctrine has known drift."""
        return [obs for obs in self._observations if obs.doctrine_id == doctrine_id]

    def get_recent_drifts(self, days: int = 365) -> List[DriftObservation]:
        """Get drift observations from recent time period."""
        cutoff = datetime.now(timezone.utc).timestamp() - (days * 86400)
        recent = []
        for obs in self._observations:
            try:
                obs_ts = datetime.fromisoformat(obs.observation_date).timestamp()
                if obs_ts >= cutoff:
                    recent.append(obs)
            except Exception:
                continue
        return recent

    def get_all_observations(self) -> List[DriftObservation]:
        """Get all drift observations."""
        return self._observations


class MultiDoctrineDecomposer:
    """TIE-20 Component 19: Multi-doctrine decomposition - break complex issues into categories/strata."""

    def __init__(self, doctrine_cache: WaterDoctrineCache) -> None:
        self._cache = doctrine_cache
        self._interaction_graph = self._build_interaction_graph()

    def _build_interaction_graph(self) -> List[DoctrineInteraction]:
        """Build doctrine interaction graph for water rights domain."""
        interactions = [
            # Groundwater + GCD interactions
            DoctrineInteraction(
                from_category=IssueCategory.GROUNDWATER_RIGHTS,
                to_category=IssueCategory.GCD_JURISDICTION,
                interaction_type="conditions",
                resolution_priority=1,
                notes="Rule of Capture subject to GCD regulation where GCD exists",
            ),
            DoctrineInteraction(
                from_category=IssueCategory.GCD_JURISDICTION,
                to_category=IssueCategory.GROUNDWATER_RIGHTS,
                interaction_type="reinforces",
                resolution_priority=2,
                notes="GCD permits codify groundwater rights within district boundaries",
            ),

            # Aquifer protection + groundwater
            DoctrineInteraction(
                from_category=IssueCategory.AQUIFER_PROTECTION,
                to_category=IssueCategory.GROUNDWATER_RIGHTS,
                interaction_type="conflicts",
                resolution_priority=1,
                notes="Edwards Aquifer protection zones restrict groundwater development",
            ),
            DoctrineInteraction(
                from_category=IssueCategory.GROUNDWATER_RIGHTS,
                to_category=IssueCategory.AQUIFER_PROTECTION,
                interaction_type="triggers",
                resolution_priority=3,
                notes="Groundwater extraction in protected zones triggers enhanced review",
            ),

            # Produced water + injection well
            DoctrineInteraction(
                from_category=IssueCategory.PRODUCED_WATER_DISPOSAL,
                to_category=IssueCategory.INJECTION_WELL_COMPLIANCE,
                interaction_type="reinforces",
                resolution_priority=1,
                notes="Produced water disposal requires RRC injection well permit",
            ),
            DoctrineInteraction(
                from_category=IssueCategory.INJECTION_WELL_COMPLIANCE,
                to_category=IssueCategory.SEISMICITY_RISK,
                interaction_type="triggers",
                resolution_priority=2,
                notes="Injection wells in seismically active areas trigger monitoring requirements",
            ),

            # Water quality + all categories
            DoctrineInteraction(
                from_category=IssueCategory.WATER_QUALITY,
                to_category=IssueCategory.GROUNDWATER_RIGHTS,
                interaction_type="conditions",
                resolution_priority=2,
                notes="Water quality standards condition beneficial use classification",
            ),
            DoctrineInteraction(
                from_category=IssueCategory.WATER_QUALITY,
                to_category=IssueCategory.SURFACE_WATER_RIGHTS,
                interaction_type="conditions",
                resolution_priority=2,
                notes="Surface water permits conditioned on water quality protection",
            ),
            DoctrineInteraction(
                from_category=IssueCategory.WATER_QUALITY,
                to_category=IssueCategory.PRODUCED_WATER_DISPOSAL,
                interaction_type="reinforces",
                resolution_priority=1,
                notes="Disposal water quality determines injection zone classification",
            ),

            # Interstate compact interactions
            DoctrineInteraction(
                from_category=IssueCategory.INTERSTATE_COMPACT,
                to_category=IssueCategory.SURFACE_WATER_RIGHTS,
                interaction_type="conflicts",
                resolution_priority=1,
                notes="Rio Grande Compact limits surface water appropriations in El Paso",
            ),

            # Drought + all water sources
            DoctrineInteraction(
                from_category=IssueCategory.DROUGHT_MANAGEMENT,
                to_category=IssueCategory.GROUNDWATER_RIGHTS,
                interaction_type="triggers",
                resolution_priority=3,
                notes="Drought triggers GCD pumping restrictions",
            ),
            DoctrineInteraction(
                from_category=IssueCategory.DROUGHT_MANAGEMENT,
                to_category=IssueCategory.SURFACE_WATER_RIGHTS,
                interaction_type="triggers",
                resolution_priority=2,
                notes="Drought triggers TCEQ water allocation curtailment",
            ),
        ]
        return interactions

    def decompose(self, query: str, response_text: str) -> List[DecomposedIssue]:
        """Decompose complex query into issue categories and strata."""
        issues: List[DecomposedIssue] = []
        query_lower = query.lower()

        # Groundwater rights
        if any(term in query_lower for term in ["groundwater", "aquifer", "well", "rule of capture"]):
            applicable = self._cache.get_by_category(DoctrineCategory.GROUNDWATER_CAPTURE)
            issues.append(DecomposedIssue(
                category=IssueCategory.GROUNDWATER_RIGHTS,
                stratum=IssueStratum.SUBSTANTIVE,
                description="Groundwater ownership and production rights under Rule of Capture",
                applicable_doctrines=[d.doctrine_id for d in applicable[:5]],
                authority_level=AuthorityLevel.CASE_LAW,
                authority_weight=AUTHORITY_WEIGHTS[AuthorityLevel.CASE_LAW],
                confidence_stratification=ConfidenceStratification.DEFENSIBLE,
                resolution_order=1,
            ))

        # GCD jurisdiction
        if any(term in query_lower for term in ["gcd", "conservation district", "permit"]):
            applicable = self._cache.get_by_category(DoctrineCategory.GROUNDWATER_CONSERVATION_DISTRICT)
            issues.append(DecomposedIssue(
                category=IssueCategory.GCD_JURISDICTION,
                stratum=IssueStratum.PROCEDURAL,
                description="GCD permitting jurisdiction and requirements",
                applicable_doctrines=[d.doctrine_id for d in applicable[:5]],
                authority_level=AuthorityLevel.REGULATION,
                authority_weight=AUTHORITY_WEIGHTS[AuthorityLevel.REGULATION],
                confidence_stratification=ConfidenceStratification.DEFENSIBLE,
                resolution_order=2,
            ))

        # Surface water rights
        if any(term in query_lower for term in ["surface water", "river", "stream", "tceq"]):
            applicable = self._cache.get_by_category(DoctrineCategory.SURFACE_WATER_APPROPRIATION)
            issues.append(DecomposedIssue(
                category=IssueCategory.SURFACE_WATER_RIGHTS,
                stratum=IssueStratum.SUBSTANTIVE,
                description="Surface water appropriation and TCEQ permit requirements",
                applicable_doctrines=[d.doctrine_id for d in applicable[:5]],
                authority_level=AuthorityLevel.STATUTE,
                authority_weight=AUTHORITY_WEIGHTS[AuthorityLevel.STATUTE],
                confidence_stratification=ConfidenceStratification.DEFENSIBLE,
                resolution_order=1,
            ))

        # Produced water disposal
        if any(term in query_lower for term in ["produced water", "disposal", "saltwater"]):
            applicable = self._cache.get_by_category(DoctrineCategory.PRODUCED_WATER_DISPOSAL)
            issues.append(DecomposedIssue(
                category=IssueCategory.PRODUCED_WATER_DISPOSAL,
                stratum=IssueStratum.SUBSTANTIVE,
                description="Produced water disposal regulations and permit requirements",
                applicable_doctrines=[d.doctrine_id for d in applicable[:5]],
                authority_level=AuthorityLevel.REGULATION,
                authority_weight=AUTHORITY_WEIGHTS[AuthorityLevel.REGULATION],
                confidence_stratification=ConfidenceStratification.DEFENSIBLE,
                resolution_order=1,
            ))

        # Injection well compliance
        if any(term in query_lower for term in ["injection well", "class ii", "uic", "rrc"]):
            issues.append(DecomposedIssue(
                category=IssueCategory.INJECTION_WELL_COMPLIANCE,
                stratum=IssueStratum.PROCEDURAL,
                description="RRC injection well permitting and compliance monitoring",
                applicable_doctrines=["RRC_16TAC3.9", "RRC_16TAC3.14", "RRC_16TAC3.46"],
                authority_level=AuthorityLevel.REGULATION,
                authority_weight=AUTHORITY_WEIGHTS[AuthorityLevel.REGULATION],
                confidence_stratification=ConfidenceStratification.DEFENSIBLE,
                resolution_order=2,
            ))

        # Add interactions
        for issue in issues:
            issue.interactions = [
                intr for intr in self._interaction_graph
                if intr.from_category == issue.category
            ]

        # Sort by resolution order
        issues.sort(key=lambda x: x.resolution_order)

        return issues


class FactFragilityScorer:
    """TIE-20 Component 14: Fact fragility scoring - identify vulnerable factual assertions."""

    def score_facts(self, text: str) -> List[FactFragilityScore]:
        """Score factual assertions for fragility."""
        scores: List[FactFragilityScore] = []

        # Extract factual statements (simplified - real implementation would use NLP)
        statements = [s.strip() for s in text.split('.') if len(s.strip()) > 20]

        for stmt in statements[:10]:  # Limit to first 10 statements
            stmt_lower = stmt.lower()

            # Verifiability heuristics
            verifiability = 0.8  # Default medium-high
            if any(term in stmt_lower for term in ["recorded", "filed", "permit number", "date"]):
                verifiability = 0.95  # High - public records
            elif any(term in stmt_lower for term in ["likely", "probably", "appears", "seems"]):
                verifiability = 0.4  # Low - hedged language
            elif any(term in stmt_lower for term in ["verbally", "understanding", "believed"]):
                verifiability = 0.3  # Very low - no documentation

            # Recharacterization risk
            rechar_risk = 0.3  # Default low
            if any(term in stmt_lower for term in ["intent", "purpose", "reason", "in order to"]):
                rechar_risk = 0.7  # High - subjective intent
            elif any(term in stmt_lower for term in ["abandoned", "waived", "forfeited"]):
                rechar_risk = 0.8  # Very high - legal conclusions

            # Testimony dependence
            testimony_dep = 0.2  # Default low
            if any(term in stmt_lower for term in ["operator stated", "landowner claimed", "witness"]):
                testimony_dep = 0.9  # High - direct testimony
            elif any(term in stmt_lower for term in ["understanding", "discussed"]):
                testimony_dep = 0.6  # Medium - indirect

            # Documentary support
            doc_support = 0.7  # Default medium
            if any(term in stmt_lower for term in ["per recorded instrument", "per permit", "per filed"]):
                doc_support = 0.95  # High - explicit doc reference
            elif any(term in stmt_lower for term in ["no record", "unrecorded", "verbal"]):
                doc_support = 0.1  # Very low - no docs

            score = FactFragilityScore(
                fact_statement=stmt,
                verifiability=verifiability,
                recharacterization_risk=rechar_risk,
                testimony_dependence=testimony_dep,
                documentary_support=doc_support,
                overall_fragility=0.0,
            )
            score.compute_overall()

            # Only include medium+ fragility facts
            if score.overall_fragility >= 0.4:
                if score.overall_fragility >= 0.7:
                    score.risk_notes = "CRITICAL: High fragility - strengthen with documentary evidence"
                elif score.overall_fragility >= 0.5:
                    score.risk_notes = "MODERATE: Consider additional supporting documentation"
                else:
                    score.risk_notes = "Minor fragility - monitor if challenged"

                scores.append(score)

        return scores


class WaterRightsAnalyzerEngine:
    """Main LM13 Water Rights Analyzer Engine.

    Orchestrates all analysis components: classification, GCD analysis,
    produced water tracking, injection well monitoring, surface use analysis,
    freshwater identification, water transport analysis, and compliance scoring.
    """

    def __init__(self, config_path: Optional[Path] = None) -> None:
        self._config_path = config_path or CONFIG_PATH
        self._config = self._load_config()
        self._doctrine_cache = WaterDoctrineCache()
        self._doctrine_cache.load_all()
        self._semantic_dict = WaterRightsSemanticDictionary()
        self._search_engine = WaterRightsSearchEngine()
        self._telemetry = WaterRightsTelemetry()

        # TIE-20 Components
        self._coverage_map = WaterRightsCoverageMap(self._doctrine_cache)
        self._drift_watcher = WaterRightsDriftWatcher()
        self._decomposer = MultiDoctrineDecomposer(self._doctrine_cache)
        self._fragility_scorer = FactFragilityScorer()

        # Cloud retriever (TIE-20 Component 20: deep analysis mode)
        self._cloud_retriever: Optional[CognitionCloudRetriever] = None
        if CLOUD_RETRIEVER_AVAILABLE:
            try:
                self._cloud_retriever = CognitionCloudRetriever()
                logger.info("CognitionCloudRetriever initialized for deep analysis mode")
            except Exception as exc:
                logger.warning("Failed to initialize CognitionCloudRetriever: {}", exc)

        # Initialize components
        self.classifier = WaterRightClassifier(self._config)
        self.gcd_analyzer = GroundwaterDistrictAnalyzer(self._config, self._doctrine_cache)
        self.produced_water_tracker = ProducedWaterTracker(self._config, self._doctrine_cache)
        self.injection_well_monitor = InjectionWellMonitor(self._config, self._doctrine_cache)
        self.surface_use_analyzer = SurfaceUseWaterAnalyzer(self._doctrine_cache)
        self.freshwater_identifier = FreshwaterSourceIdentifier(self._config)
        self.transport_analyzer = WaterTransportAnalyzer(self._config, self._doctrine_cache)
        self.risk_scorer = ComplianceRiskScorer(self._config)

        self._start_time = time.monotonic()
        logger.info(
            "WaterRightsAnalyzerEngine v{} initialized (port {}, {} doctrines, {} terms)",
            ENGINE_VERSION, ENGINE_PORT,
            len(self._doctrine_cache._doctrines),
            len(self._semantic_dict._all_terms) if self._semantic_dict._loaded else "lazy",
        )

    def _load_config(self) -> dict[str, Any]:
        """Load engine configuration from JSON file."""
        if self._config_path.exists():
            config = json.loads(self._config_path.read_text())
            logger.info("Config loaded from {}", self._config_path)
            return config
        logger.warning("Config file not found at {}, using defaults", self._config_path)
        return {}

    # -- Analysis Methods --

    def identify_water_right(
        self,
        source_type: str = "",
        tds_mg_l: Optional[float] = None,
        aquifer_name: str = "",
        county: str = "",
        volume_bbls_per_day: float = 0.0,
        is_produced: bool = False,
        is_recycled: bool = False,
        is_flowback: bool = False,
        operator_name: str = "",
    ) -> WaterRightIdentification:
        """Identify and classify a water right, determining applicable permits and regulations."""
        start = time.monotonic()
        try:
            classification = self.classifier.classify_source(
                source_type=source_type,
                tds_mg_l=tds_mg_l,
                aquifer_name=aquifer_name,
                is_produced=is_produced,
                is_recycled=is_recycled,
                is_flowback=is_flowback,
            )
            right_type = self.classifier.determine_right_type(classification)
            permits_needed = self.classifier.identify_permits_needed(
                classification=classification,
                county=county,
                volume_bbls_per_day=volume_bbls_per_day,
            )

            # Find applicable doctrines
            applicable_doctrines: list[str] = []
            if classification in (WaterClassification.FRESH_GROUNDWATER, WaterClassification.BRACKISH_GROUNDWATER):
                doctrines = self._doctrine_cache.get_by_category(DoctrineCategory.GROUNDWATER_CAPTURE)
                applicable_doctrines.extend([d.doctrine_id for d in doctrines])
                gcd_doctrines = self._doctrine_cache.get_by_category(DoctrineCategory.GROUNDWATER_CONSERVATION_DISTRICT)
                applicable_doctrines.extend([d.doctrine_id for d in gcd_doctrines])
            elif classification == WaterClassification.SURFACE_WATER:
                doctrines = self._doctrine_cache.get_by_category(DoctrineCategory.SURFACE_WATER_APPROPRIATION)
                applicable_doctrines.extend([d.doctrine_id for d in doctrines])
            elif classification == WaterClassification.PRODUCED_WATER:
                doctrines = self._doctrine_cache.get_by_category(DoctrineCategory.PRODUCED_WATER_DISPOSAL)
                applicable_doctrines.extend([d.doctrine_id for d in doctrines])

            # Volume conversion
            af_per_year = volume_bbls_per_day * 365.25 / 7758.0 if volume_bbls_per_day > 0 else None

            # GCD check
            gcd_required = classification in (
                WaterClassification.FRESH_GROUNDWATER,
                WaterClassification.BRACKISH_GROUNDWATER,
            )

            result = WaterRightIdentification(
                record_id=f"WRI-{hashlib.sha256(f'{source_type}{county}{operator_name}'.encode()).hexdigest()[:12]}",
                classification=classification,
                right_type=right_type,
                operator_name=operator_name,
                county=county,
                aquifer=aquifer_name,
                tds_mg_l=tds_mg_l,
                volume_bbls_per_day=volume_bbls_per_day,
                volume_af_per_year=af_per_year,
                gcd_permit_required=gcd_required,
                surface_water_permit_required=classification == WaterClassification.SURFACE_WATER,
                injection_permit_required=classification == WaterClassification.PRODUCED_WATER,
                applicable_doctrines=applicable_doctrines,
                regulatory_notes=permits_needed,
                risk_level=RiskLevel.LOW,
                confidence=0.95 if tds_mg_l is not None else 0.7,
                analysis_timestamp=datetime.now(timezone.utc).isoformat(),
            )
            result.compute_hash()

            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.WATER_RIGHT_ANALYSIS, duration, True,
                metadata={"classification": classification.value, "county": county},
            )
            return result

        except Exception as exc:
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.WATER_RIGHT_ANALYSIS, duration, False,
                error_message=str(exc),
            )
            raise

    def analyze_gcd_rules(self, county: str, purpose: str = "industrial", volume_af_per_year: float = 0.0) -> GCDRuleAnalysis:
        """Analyze GCD rules for a given county and purpose."""
        start = time.monotonic()
        try:
            result = self.gcd_analyzer.analyze_county(county, purpose, volume_af_per_year)
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.GCD_RULE_LOOKUP, duration, True,
                metadata={"county": county, "purpose": purpose},
            )
            return result
        except Exception as exc:
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.GCD_RULE_LOOKUP, duration, False,
                error_message=str(exc),
            )
            raise

    def analyze_disposal_well(self, **kwargs: Any) -> ProducedWaterDisposalAnalysis:
        """Analyze a produced water disposal well."""
        start = time.monotonic()
        try:
            result = self.produced_water_tracker.analyze_disposal_well(**kwargs)
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.PRODUCED_WATER_TRACKING, duration, True,
                metadata={"well_id": kwargs.get("well_id", "")},
            )
            self._telemetry.compliance.record_score(
                kwargs.get("well_id", ""),
                100.0 if result.risk_level == RiskLevel.LOW else (
                    75.0 if result.risk_level == RiskLevel.MODERATE else (
                        50.0 if result.risk_level == RiskLevel.HIGH else 25.0
                    )
                ),
            )
            return result
        except Exception as exc:
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.PRODUCED_WATER_TRACKING, duration, False,
                error_message=str(exc),
            )
            raise

    def generate_injection_well_report(self, **kwargs: Any) -> InjectionWellComplianceReport:
        """Generate an injection well compliance report."""
        start = time.monotonic()
        try:
            result = self.injection_well_monitor.generate_compliance_report(**kwargs)
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.INJECTION_WELL_CHECK, duration, True,
                metadata={
                    "well_id": kwargs.get("well_id", ""),
                    "compliance_score": result.compliance_score,
                },
            )
            self._telemetry.compliance.record_score(
                kwargs.get("well_id", ""), result.compliance_score,
            )
            return result
        except Exception as exc:
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.INJECTION_WELL_CHECK, duration, False,
                error_message=str(exc),
            )
            raise

    def analyze_surface_use(self, **kwargs: Any) -> SurfaceUseWaterAnalysis:
        """Analyze surface use agreement water provisions."""
        start = time.monotonic()
        try:
            result = self.surface_use_analyzer.analyze_agreement(**kwargs)
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.SURFACE_USE_ANALYSIS, duration, True,
                metadata={"agreement_id": kwargs.get("agreement_id", "")},
            )
            return result
        except Exception as exc:
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.SURFACE_USE_ANALYSIS, duration, False,
                error_message=str(exc),
            )
            raise

    def identify_freshwater_source(self, **kwargs: Any) -> FreshwaterSourceReport:
        """Identify freshwater sources at a location."""
        start = time.monotonic()
        try:
            result = self.freshwater_identifier.identify_source(**kwargs)
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.FRESHWATER_IDENTIFICATION, duration, True,
                metadata={"county": kwargs.get("county", "")},
            )
            return result
        except Exception as exc:
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.FRESHWATER_IDENTIFICATION, duration, False,
                error_message=str(exc),
            )
            raise

    def analyze_water_transport(self, **kwargs: Any) -> WaterTransportAnalysis:
        """Analyze a water transport/sale agreement."""
        start = time.monotonic()
        try:
            result = self.transport_analyzer.analyze_agreement(**kwargs)
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.TRANSPORT_ANALYSIS, duration, True,
                metadata={"agreement_id": kwargs.get("agreement_id", "")},
            )
            return result
        except Exception as exc:
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.TRANSPORT_ANALYSIS, duration, False,
                error_message=str(exc),
            )
            raise

    def score_operator_compliance(self, **kwargs: Any) -> ComplianceRiskReport:
        """Score an operator's environmental compliance risk."""
        start = time.monotonic()
        try:
            result = self.risk_scorer.score_operator(**kwargs)
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.COMPLIANCE_SCORING, duration, True,
                metadata={
                    "operator": kwargs.get("operator_name", ""),
                    "score": result.overall_score,
                },
            )
            self._telemetry.compliance.record_score(
                kwargs.get("operator_id", ""), result.overall_score,
            )
            return result
        except Exception as exc:
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.COMPLIANCE_SCORING, duration, False,
                error_message=str(exc),
            )
            raise

    # -- Search Methods --

    def search_permits(self, query: WaterSearchQuery) -> WaterSearchResponse:
        """Search the permit index."""
        start = time.monotonic()
        try:
            result = self._search_engine.search(query)
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.PERMIT_SEARCH, duration, True,
                output_size=result.total_results,
            )
            return result
        except Exception as exc:
            duration = (time.monotonic() - start) * 1000
            self._telemetry.record_operation(
                OperationType.PERMIT_SEARCH, duration, False,
                error_message=str(exc),
            )
            raise

    def index_permit(self, record: WaterPermitRecord) -> None:
        """Add a permit record to the search index."""
        self._search_engine.index_record(record)
        self._telemetry.audit.log(
            action=AuditAction.RECORD_CREATED,
            actor="engine",
            resource_type="permit",
            resource_id=record.record_id,
            details=f"Indexed permit {record.permit_number} ({record.operator_name})",
        )

    # -- Doctrine Methods --

    def lookup_doctrine(self, doctrine_id: str) -> Optional[TexasWaterDoctrine]:
        """Look up a specific water rights doctrine."""
        start = time.monotonic()
        result = self._doctrine_cache.get_doctrine(doctrine_id)
        duration = (time.monotonic() - start) * 1000
        self._telemetry.record_operation(
            OperationType.DOCTRINE_LOOKUP, duration, result is not None,
            metadata={"doctrine_id": doctrine_id},
        )
        return result

    def search_doctrines(self, query: str) -> list[TexasWaterDoctrine]:
        """Search doctrines by keyword."""
        start = time.monotonic()
        results = self._doctrine_cache.search_doctrines(query)
        duration = (time.monotonic() - start) * 1000
        self._telemetry.record_operation(
            OperationType.DOCTRINE_LOOKUP, duration, True,
            output_size=len(results),
        )
        return results

    # -- Semantic Methods --

    def lookup_term(self, term: str) -> Optional[SemanticTerm]:
        """Look up a water rights term in the semantic dictionary."""
        return self._semantic_dict.lookup(term)

    def search_terms(self, query: str) -> list[SemanticTerm]:
        """Search the semantic dictionary."""
        start = time.monotonic()
        results = self._semantic_dict.search(query)
        duration = (time.monotonic() - start) * 1000
        self._telemetry.record_operation(
            OperationType.SEMANTIC_SEARCH, duration, True,
            output_size=len(results),
        )
        return results

    def extract_terms(self, text: str) -> list[SemanticTerm]:
        """Extract recognized water rights terms from text."""
        start = time.monotonic()
        results = self._semantic_dict.extract_terms_from_text(text)
        duration = (time.monotonic() - start) * 1000
        self._telemetry.record_operation(
            OperationType.TERM_EXTRACTION, duration, True,
            input_size=len(text), output_size=len(results),
        )
        return results

    # -- TIE-20 Component 1: Three-Layer Response --

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode = ResponseMode.FAST,
        enable_deep_analysis: bool = False,
        enable_zoned_analysis: bool = False,
        enable_fact_fragility: bool = False,
        enable_decomposition: bool = False,
    ) -> ThreeLayerResponse:
        """
        TIE-20 Component 1: Three-layer response system.

        Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert blocks
        Layer 2: Semantic Retrieval (200-1000ms) - Vector/keyword search
        Layer 3: Deep Analysis (1000-5000ms) - Cognition Cloud synthesis
        """
        total_start = time.monotonic()
        response = ThreeLayerResponse(
            query=query,
            response_mode=mode,
            final_answer="",
            total_latency_ms=0.0,
            confidence=0.0,
            confidence_stratification=ConfidenceStratification.DEFENSIBLE,
            authority_level=AuthorityLevel.GUIDANCE,
        )

        triggered_doctrine_ids: List[str] = []

        # LAYER 1: Doctrine Cache (fastest)
        layer1_start = time.monotonic()
        cache_results = self._doctrine_cache.search_doctrines(query)
        if cache_results:
            response.cache_hit = True
            response.cache_doctrines = [d.doctrine_id for d in cache_results[:5]]
            triggered_doctrine_ids.extend(response.cache_doctrines)

            # Build cache response from doctrine blocks
            cache_text_parts = []
            for doc in cache_results[:3]:  # Top 3 doctrines
                cache_text_parts.append(f"**{doc.topic}** (Authority: {doc.primary_authority})")
                cache_text_parts.append(doc.conclusion_template)

            response.cache_response = "\n\n".join(cache_text_parts)
            response.cache_latency_ms = (time.monotonic() - layer1_start) * 1000

            # Determine authority level and stratification from top doctrine
            top_doctrine = cache_results[0]
            response.authority_level = self._map_authority_level(top_doctrine.primary_authority)
            response.confidence_stratification = top_doctrine.confidence_stratification
            response.confidence = 0.85
            response.citations = [top_doctrine.primary_authority]

            # FAST mode: return cache response immediately
            if mode == ResponseMode.FAST:
                response.final_answer = response.cache_response
                response.total_latency_ms = response.cache_latency_ms
                response.compute_hash()
                return response

        # LAYER 2: Semantic Retrieval (medium speed)
        layer2_start = time.monotonic()
        semantic_matches = self._search_engine.search_permits(
            WaterSearchQuery(
                search_type="semantic",
                query_text=query,
                max_results=10,
            )
        )
        if semantic_matches:
            response.semantic_triggered = True
            response.semantic_matches = [
                {
                    "permit_id": match.permit_id,
                    "permit_type": match.permit_type.value if hasattr(match, 'permit_type') else "unknown",
                    "score": getattr(match, 'relevance_score', 0.0),
                }
                for match in semantic_matches[:5]
            ]

            # Build semantic response
            semantic_parts = []
            if response.cache_response:
                semantic_parts.append(response.cache_response)
                semantic_parts.append("\n**Additional Context from Permit Records:**")

            for match in semantic_matches[:3]:
                semantic_parts.append(
                    f"- {match.permit_type.value if hasattr(match, 'permit_type') else 'Permit'}: "
                    f"{match.permit_id} ({getattr(match, 'operator_name', 'Unknown operator')})"
                )

            response.semantic_response = "\n".join(semantic_parts)
            response.semantic_latency_ms = (time.monotonic() - layer2_start) * 1000

            # Update confidence with semantic evidence
            if response.confidence < 0.9:
                response.confidence = min(0.9, response.confidence + 0.1)

        # Synthesize DEFENSE/MEMO response
        if mode in (ResponseMode.DEFENSE, ResponseMode.MEMO):
            final_parts = []

            if mode == ResponseMode.MEMO:
                final_parts.append(f"# Water Rights Analysis Memorandum")
                final_parts.append(f"**Query:** {query}\n")

            if response.cache_response:
                final_parts.append("## Legal Framework\n")
                final_parts.append(response.cache_response)

            if response.semantic_response:
                final_parts.append("\n## Permit Records Analysis\n")
                final_parts.append(response.semantic_response)

            if mode == ResponseMode.DEFENSE:
                final_parts.append("\n## Audit Trail\n")
                final_parts.append(f"- Doctrines consulted: {len(triggered_doctrine_ids)}")
                final_parts.append(f"- Authority level: {response.authority_level.value}")
                final_parts.append(f"- Confidence stratification: {response.confidence_stratification.value}")
                final_parts.append(f"- Citations: {', '.join(response.citations)}")

            response.final_answer = "\n".join(final_parts)

        # LAYER 3: Deep Analysis (slowest, most comprehensive)
        if enable_deep_analysis and self._cloud_retriever:
            layer3_start = time.monotonic()
            try:
                # Query Cognition Cloud for multi-source synthesis
                cloud_results = self._cloud_retriever.query(
                    query=query,
                    context=f"Water rights analysis. Doctrines: {', '.join(triggered_doctrine_ids[:5])}",
                    max_results=5,
                )
                if cloud_results:
                    response.deep_analysis_triggered = True
                    response.deep_sources = [r.get('source', 'unknown') for r in cloud_results]

                    # Synthesize deep response
                    deep_parts = [response.final_answer or response.semantic_response or response.cache_response]
                    deep_parts.append("\n## Deep Analysis (Cognition Cloud)\n")
                    for result in cloud_results[:3]:
                        deep_parts.append(f"- {result.get('content', '')[:200]}...")

                    response.deep_response = "\n".join(deep_parts)
                    response.deep_latency_ms = (time.monotonic() - layer3_start) * 1000
                    response.final_answer = response.deep_response
                    response.confidence = min(0.95, response.confidence + 0.05)
            except Exception as exc:
                logger.warning("Deep analysis failed: {}", exc)

        # TIE-20 Component 13: Zoned Analysis
        if enable_zoned_analysis:
            response.zoned_analysis = self._generate_zoned_analysis(query, response.final_answer or response.cache_response)

        # TIE-20 Component 14: Fact Fragility Scoring
        if enable_fact_fragility:
            response.fact_fragility = self._fragility_scorer.score_facts(response.final_answer or response.cache_response)

        # TIE-20 Component 19: Multi-Doctrine Decomposition
        if enable_decomposition:
            response.decomposed_issues = self._decomposer.decompose(query, response.final_answer or response.cache_response)

        # TIE-20 Component 10: Coverage Map (always run)
        response.coverage_gaps = self._coverage_map.analyze_coverage(query, triggered_doctrine_ids)

        # TIE-20 Component 9: Drift Watcher (always check)
        response.drift_alerts = []
        for doc_id in triggered_doctrine_ids:
            drifts = self._drift_watcher.check_for_drift(doc_id)
            response.drift_alerts.extend(drifts)

        # Finalize
        if not response.final_answer:
            response.final_answer = response.semantic_response or response.cache_response or "No applicable doctrines found."

        response.total_latency_ms = (time.monotonic() - total_start) * 1000
        response.compute_hash()

        # Audit trail logging (TIE-20 Component 15)
        self._telemetry.audit.log(
            action=AuditAction.QUERY,
            user_id="system",
            resource_type="three_layer_response",
            resource_id=response.determinism_hash[:12],
            details={
                "query": query,
                "mode": mode.value,
                "layers_used": sum([response.cache_hit, response.semantic_triggered, response.deep_analysis_triggered]),
                "confidence": response.confidence,
                "latency_ms": response.total_latency_ms,
            },
        )

        return response

    def _map_authority_level(self, citation: str) -> AuthorityLevel:
        """Map citation to authority hierarchy level."""
        citation_lower = citation.lower()
        if "tex. water code" in citation_lower or "twc" in citation_lower:
            return AuthorityLevel.STATUTE
        elif "16 tac" in citation_lower or "30 tac" in citation_lower:
            return AuthorityLevel.REGULATION
        elif "s.w." in citation_lower or "tex. sup. ct." in citation_lower:
            return AuthorityLevel.CASE_LAW
        elif "tceq" in citation_lower or "rrc" in citation_lower or "eaa" in citation_lower:
            return AuthorityLevel.ADMINISTRATIVE
        elif "guidance" in citation_lower or "guidance" in citation_lower:
            return AuthorityLevel.GUIDANCE
        else:
            return AuthorityLevel.BEST_PRACTICE

    def _generate_zoned_analysis(self, query: str, response_text: str) -> List[ZonedAnalysisResult]:
        """Generate zoned analysis - separate planning/reporting/audit perspectives."""
        zones: List[ZonedAnalysisResult] = []
        query_lower = query.lower()

        # PLANNING ZONE: What might we do?
        if any(term in query_lower for term in ["can we", "should we", "planning", "future", "proposed"]):
            zones.append(ZonedAnalysisResult(
                zone=AnalysisZone.PLANNING,
                issue_description="Forward-looking analysis of water rights acquisition strategy",
                applicable_doctrines=["GWD_PLANNING", "TCEQ_PERMIT_FORECAST"],
                authority_citations=["TWC §36.113 (GCD permitting)", "TWC §11.121 (TCEQ permits)"],
                confidence=0.7,
                risk_level=RiskLevel.MEDIUM,
                recommendations=[
                    "Conduct preliminary GCD consultation before finalizing drilling plans",
                    "Verify water availability through hydrological study",
                    "Budget 6-12 months for permit acquisition timeline",
                ],
                epistemic_caveat="Planning analysis based on current regulations - subject to regulatory change",
            ))

        # REPORTING ZONE: What did we do?
        if any(term in query_lower for term in ["completed", "drilled", "obtained", "historical", "past"]):
            zones.append(ZonedAnalysisResult(
                zone=AnalysisZone.REPORTING,
                issue_description="Historical analysis of completed water rights actions",
                applicable_doctrines=["PERMIT_COMPLIANCE", "REPORTING_REQUIREMENTS"],
                authority_citations=["16 TAC §3.14 (injection well reporting)", "TWC §36.203 (GCD reporting)"],
                confidence=0.9,
                risk_level=RiskLevel.LOW,
                recommendations=[
                    "Verify all required reports filed with TCEQ/RRC/GCD",
                    "Confirm production volumes within permitted limits",
                    "Maintain records for 5-year audit period",
                ],
                epistemic_caveat="",
            ))

        # AUDIT ZONE: What should we have done?
        if any(term in query_lower for term in ["compliance", "audit", "violation", "should have", "required"]):
            zones.append(ZonedAnalysisResult(
                zone=AnalysisZone.AUDIT,
                issue_description="Retrospective compliance audit of water rights actions",
                applicable_doctrines=["PERMIT_CONDITIONS", "ENFORCEMENT_STANDARDS"],
                authority_citations=["16 TAC §3.14", "30 TAC §305.125", "TWC §11.081"],
                confidence=0.85,
                risk_level=RiskLevel.HIGH,
                recommendations=[
                    "Conduct gap analysis against permit conditions",
                    "Implement corrective action plan for any deficiencies",
                    "Engage counsel if potential violation identified",
                ],
                epistemic_caveat="Audit findings based on available records - may not reflect undocumented conditions",
            ))

        return zones

    # -- Health and Telemetry --

    def health_check(self) -> EngineHealthResponse:
        """Return engine health status."""
        health = self._telemetry.get_health(
            records_indexed=len(self._search_engine._all_records),
            doctrines_loaded=len(self._doctrine_cache._doctrines),
            terms_loaded=len(self._semantic_dict._all_terms) if self._semantic_dict._loaded else 0,
        )
        return EngineHealthResponse(
            status=health.status,
            uptime_seconds=health.uptime_seconds,
            total_operations=health.total_operations,
            total_errors=health.total_errors,
            error_rate=health.error_rate,
            avg_response_time_ms=health.avg_response_time_ms,
            records_indexed=health.records_indexed,
            doctrines_loaded=health.doctrines_loaded,
            terms_loaded=health.terms_loaded,
            timestamp=health.timestamp,
        )

    def get_telemetry(self) -> dict[str, Any]:
        """Get complete telemetry data (TIE-20 Component 8: enhanced)."""
        return {
            "health": self.health_check().model_dump(),
            "metrics": self._telemetry.get_metrics().to_dict(),
            "performance": self._telemetry.performance.get_summary(),
            "compliance": self._telemetry.compliance.get_summary(),
            "doctrine_stats": self._doctrine_cache.get_statistics(),
            "semantic_stats": self._semantic_dict.get_statistics(),
            "search_stats": self._search_engine.get_statistics(),
            # TIE-20 additions
            "coverage_stats": {
                "total_queries": len(self._coverage_map._query_log),
                "recent_gaps": len([
                    q for q in self._coverage_map._query_log[-100:]
                    if q.get('gaps', 0) > 0
                ]),
            },
            "drift_stats": {
                "total_observations": len(self._drift_watcher.get_all_observations()),
                "major_drifts": len([
                    d for d in self._drift_watcher.get_all_observations()
                    if d.drift_severity == "major"
                ]),
                "recent_drifts_365d": len(self._drift_watcher.get_recent_drifts(365)),
            },
        }

    def get_doctrine_cache(self) -> WaterDoctrineCache:
        """Access the doctrine cache directly."""
        return self._doctrine_cache

    def get_semantic_dictionary(self) -> WaterRightsSemanticDictionary:
        """Access the semantic dictionary directly."""
        return self._semantic_dict

    def get_search_engine(self) -> WaterRightsSearchEngine:
        """Access the search engine directly."""
        return self._search_engine

    def get_config(self) -> dict[str, Any]:
        """Return the engine configuration."""
        return self._config

    # -- TIE-20 Component 4: Authority Hardening --

    def resolve_authority_conflicts(
        self,
        conflicting_doctrines: List[TexasWaterDoctrine],
    ) -> TexasWaterDoctrine:
        """
        TIE-20 Component 4: Authority hardening - resolve conflicts using hierarchical weights.

        Authority hierarchy (highest to lowest):
        1. Statute (Texas Water Code, Oil & Gas Code)
        2. Regulation (TCEQ/RRC rules - 16 TAC, 30 TAC)
        3. Case Law (Texas Supreme Court, Courts of Appeals)
        4. Administrative (TCEQ orders, GCD rules, EAA regulations)
        5. Guidance (TCEQ guidance documents)
        6. Best Practice (Industry standards)
        """
        if not conflicting_doctrines:
            raise ValueError("Must provide at least one doctrine to resolve")

        if len(conflicting_doctrines) == 1:
            return conflicting_doctrines[0]

        # Score each doctrine by authority level
        scored_doctrines = []
        for doctrine in conflicting_doctrines:
            auth_level = self._map_authority_level(doctrine.primary_authority)
            weight = AUTHORITY_WEIGHTS[auth_level]

            # Adjust weight by confidence stratification
            strat_multiplier = {
                ConfidenceStratification.DEFENSIBLE: 1.0,
                ConfidenceStratification.AGGRESSIVE: 0.8,
                ConfidenceStratification.DISCLOSURE: 0.6,
                ConfidenceStratification.HIGH_RISK: 0.4,
            }.get(doctrine.confidence_stratification, 0.5)

            final_score = weight * strat_multiplier * doctrine.confidence

            scored_doctrines.append((final_score, doctrine))

        # Sort by score descending
        scored_doctrines.sort(key=lambda x: x[0], reverse=True)

        winning_doctrine = scored_doctrines[0][1]

        logger.info(
            "Authority conflict resolved: {} doctrines evaluated, selected {} (score: {:.3f})",
            len(conflicting_doctrines),
            winning_doctrine.doctrine_id,
            scored_doctrines[0][0],
        )

        return winning_doctrine

    def explain_authority_hierarchy(self) -> Dict[str, Any]:
        """
        TIE-20 Component 4: Explain the authority hierarchy system.

        Returns detailed explanation of how conflicting doctrines are resolved.
        """
        return {
            "hierarchy": [
                {
                    "level": level.value,
                    "weight": AUTHORITY_WEIGHTS[level],
                    "examples": self._get_authority_examples(level),
                    "description": self._get_authority_description(level),
                }
                for level in [
                    AuthorityLevel.STATUTE,
                    AuthorityLevel.REGULATION,
                    AuthorityLevel.CASE_LAW,
                    AuthorityLevel.ADMINISTRATIVE,
                    AuthorityLevel.GUIDANCE,
                    AuthorityLevel.BEST_PRACTICE,
                ]
            ],
            "resolution_algorithm": "weighted_score = authority_weight × stratification_multiplier × confidence",
            "stratification_multipliers": {
                "DEFENSIBLE": 1.0,
                "AGGRESSIVE": 0.8,
                "DISCLOSURE": 0.6,
                "HIGH_RISK": 0.4,
            },
        }

    def _get_authority_examples(self, level: AuthorityLevel) -> List[str]:
        """Get example authorities for each level."""
        examples = {
            AuthorityLevel.STATUTE: [
                "Texas Water Code Chapter 36 (GCDs)",
                "Texas Water Code Chapter 11 (Surface Water)",
                "Texas Water Code Chapter 27 (Injection Wells)",
            ],
            AuthorityLevel.REGULATION: [
                "16 TAC §3.9 (RRC Injection Well Rules)",
                "30 TAC Chapter 297 (Water Rights)",
                "30 TAC Chapter 331 (Underground Injection Control)",
            ],
            AuthorityLevel.CASE_LAW: [
                "Sipriano v. Great Spring Waters of America (Texas Supreme Court - Rule of Capture)",
                "Edwards Aquifer Authority v. Day (Texas Supreme Court - GCD authority)",
                "In re Adjudication of the Water Rights of the Upper Guadalupe Segment",
            ],
            AuthorityLevel.ADMINISTRATIVE: [
                "TCEQ Water Rights Permit 12-3456",
                "RRC Disposal Well Permit SWD-789",
                "Edwards Aquifer Authority Initial Regular Permit",
            ],
            AuthorityLevel.GUIDANCE: [
                "TCEQ RG-366: Guidelines for Surface Water Quality Monitoring",
                "RRC Oil and Gas Division Guidance on Mechanical Integrity Testing",
            ],
            AuthorityLevel.BEST_PRACTICE: [
                "API RP 51R: Disposal Wells Recommended Practices",
                "TIPRO Water Management Best Practices",
            ],
        }
        return examples.get(level, [])

    def _get_authority_description(self, level: AuthorityLevel) -> str:
        """Get description of each authority level."""
        descriptions = {
            AuthorityLevel.STATUTE: "Enacted by Texas Legislature - highest binding authority",
            AuthorityLevel.REGULATION: "Promulgated by TCEQ/RRC with statutory authority - binding force of law",
            AuthorityLevel.CASE_LAW: "Texas court decisions interpreting statutes - binding precedent",
            AuthorityLevel.ADMINISTRATIVE: "Agency orders and GCD rules - binding within jurisdiction",
            AuthorityLevel.GUIDANCE: "Agency guidance documents - persuasive but not binding",
            AuthorityLevel.BEST_PRACTICE: "Industry standards - no legal force but relevant for negligence analysis",
        }
        return descriptions.get(level, "Unknown authority level")


# ============================================================================
# FASTAPI SERVER + CLOUD RETRIEVAL
# ============================================================================

import sys as _sys
import asyncio as _asyncio
from pathlib import Path as _Path
from contextlib import asynccontextmanager

_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "_shared"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel as _BaseModel, Field as _Field

try:
    from cloud_retriever import retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
except ImportError:
    _CLOUD_AVAILABLE = False
    logger.warning("cloud_retriever not available — running without cloud knowledge")


class _QueryRequest(_BaseModel):
    query: str = ""
    prompt: str = ""
    mode: str = "analysis"
    include_cloud: bool = True


class _QueryResponse(_BaseModel):
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    query: str = ""
    analysis: Dict[str, Any] = _Field(default_factory=dict)
    cloud_knowledge: Dict[str, Any] = _Field(default_factory=dict)
    cloud_citations: List[Dict[str, str]] = _Field(default_factory=list)
    processing_time_ms: float = 0.0


_engine = WaterRightsAnalyzerEngine()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"LM13 {ENGINE_NAME} v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    yield
    if _CLOUD_AVAILABLE:
        from cloud_retriever import get_cloud_retriever
        await get_cloud_retriever().close()


app = FastAPI(
    title=f"ECHO {ENGINE_ID} {ENGINE_NAME}", version=ENGINE_VERSION,
    description="Water Rights Analyzer with Cloud Knowledge Retrieval", lifespan=lifespan,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
async def health():
    return {
        "engine_id": ENGINE_ID, "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION, "status": "healthy", "port": ENGINE_PORT,
        "cloud_available": _CLOUD_AVAILABLE,
    }


@app.post("/query")
async def query_endpoint(request: _QueryRequest):
    import time, hashlib
    start = time.monotonic()
    q = request.query or request.prompt

    cloud_data: Dict[str, Any] = {}
    cloud_citations: List[Dict[str, str]] = []
    if _CLOUD_AVAILABLE and request.include_cloud:
        try:
            cloud = await retrieve_cloud_knowledge(q, category="water_rights")
            cloud_data = {
                "records": cloud.total_records,
                "merged_context": cloud.merged_text(3000),
                "sources_succeeded": cloud.sources_succeeded,
                "retrieval_time_ms": cloud.retrieval_time_ms,
            }
            cloud_citations = cloud.citation_list()
        except Exception as e:
            logger.warning(f"Cloud retrieval failed: {e}")

    analysis: Dict[str, Any] = {}
    try:
        health_info = _engine.get_health()
        analysis = {
            "mode": request.mode,
            "engine_status": health_info,
            "query_processed": q,
            "doctrine_coverage": _engine.get_config().get("doctrine_count", 0),
        }
    except Exception as e:
        logger.error(f"Local analysis failed: {e}")
        analysis = {"error": str(e)}

    elapsed = (time.monotonic() - start) * 1000
    return _QueryResponse(
        query=q, analysis=analysis, cloud_knowledge=cloud_data,
        cloud_citations=cloud_citations, processing_time_ms=round(elapsed, 2),
    )


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting LM13 {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    uvicorn.run("engine:app", host="0.0.0.0", port=ENGINE_PORT, reload=False, log_level="info")
