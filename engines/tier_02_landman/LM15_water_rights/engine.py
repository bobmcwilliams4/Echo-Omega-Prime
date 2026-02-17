"""
LM15 Water Rights Engine - Main Engine
========================================

Full FastAPI engine with all 20 TIE components implementing comprehensive
Texas water rights analysis: groundwater, surface water, produced water,
injection wells, aquifer management, conveyancing, and compliance.

Engine ID: LM15 | Port: 8413 | Mode: DET | Version: 2.0.0

Author: ECHO OMEGA PRIME Build System
Commander: Bobby Don McWilliams II
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from loguru import logger
from pydantic import BaseModel, Field, field_validator


# Ensure sibling modules are importable
import sys
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    AuthorityLevel,
    DoctrineCategory,
    DoctrineCacheBlock,
    JurisdictionScope,
    RiskLevel,
    build_doctrine_cache,
    get_coverage_map,
    search_doctrines,
    verify_doctrine_integrity,
    GROUNDWATER_RULES,
    SURFACE_WATER_RULES,
    PRODUCED_WATER_REGULATIONS,
    INJECTION_WELL_STANDARDS,
    AQUIFER_PROTECTION_RULES,
)
from search import (
    AquiferDataSearcher,
    ComplianceStatus,
    DisposalWellComplianceChecker,
    DoctrineSearchIndex,
    SearchQuery,
    SearchResponse,
    SearchResult,
    WaterPermitTracker,
    WaterRightsSearcher,
    WaterRightType,
)
from semantic import (
    AquiferAnalyzer,
    GroundwaterRightsAnalyzer,
    ProducedWaterComplianceEngine,
    SemanticTerm,
    SurfaceWaterPermitChecker,
    TermCategory,
    WaterRightsSemanticDictionary,
)
from telemetry import (
    AuditAction,
    MetricLevel,
    OperationType,
    WaterRightsTelemetry,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ENGINE_ID = "LM15"
ENGINE_NAME = "Water Rights Engine"
ENGINE_VERSION = "2.0.0"
ENGINE_PORT = 8415
ENGINE_MODE = "DET"
ENGINE_TIER = "LANDMAN"
ENGINE_AUTHORITY = 5.0
CONFIG_PATH = Path(__file__).parent / "config.json"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ResponseMode(str, Enum):
    FAST = "fast"
    ANALYSIS = "analysis"
    MEMO = "memo"
    WATER_PERMIT = "water_permit"
    DISPOSAL_COMPLIANCE = "disposal_compliance"


class WaterClassification(str, Enum):
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
    SALTWATER_DISPOSAL_WELL = "saltwater_disposal_well"
    ENHANCED_RECOVERY = "enhanced_recovery"
    EVAPORATION_PIT = "evaporation_pit"
    RECYCLING_REUSE = "recycling_reuse"
    TREATMENT_DISCHARGE = "treatment_discharge"
    LAND_APPLICATION = "land_application"
    TRUCK_HAUL = "truck_haul"
    PIPELINE_GATHERING = "pipeline_gathering"


class SeismicityLevel(str, Enum):
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class WaterRightQuery(BaseModel):
    """Input query for water rights analysis."""
    query_text: str = Field(..., min_length=1, description="Analysis query text")
    county: str = ""
    operator: str = ""
    aquifer: str = ""
    water_source: str = ""
    tds_mg_l: Optional[float] = None
    volume_bbls_day: Optional[float] = None
    volume_af_year: Optional[float] = None
    gpm: Optional[float] = None
    use_type: str = ""
    mode: ResponseMode = ResponseMode.ANALYSIS
    max_doctrines: int = 20
    include_citations: bool = True
    include_recommendations: bool = True
    session_id: str = ""


class WaterRightAnalysisResult(BaseModel):
    """Output from water rights analysis."""
    analysis_id: str
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    mode: str = ENGINE_MODE
    query_text: str
    classification: str = ""
    risk_level: str = "low"
    applicable_doctrines: list[dict[str, Any]] = Field(default_factory=list)
    regulatory_framework: dict[str, Any] = Field(default_factory=dict)
    compliance_notes: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    citations: list[str] = Field(default_factory=list)
    gcd_analysis: Optional[dict[str, Any]] = None
    permit_requirements: list[dict[str, Any]] = Field(default_factory=list)
    aquifer_data: Optional[dict[str, Any]] = None
    seismicity_assessment: Optional[dict[str, Any]] = None
    confidence: float = 1.0
    execution_time_ms: float = 0.0
    timestamp: str = ""
    determinism_hash: str = ""

    @field_validator("confidence")
    @classmethod
    def clamp_confidence(cls, v: float) -> float:
        return max(0.0, min(1.0, v))

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.analysis_id,
            "query": self.query_text,
            "classification": self.classification,
            "risk": self.risk_level,
            "doctrines": [d.get("doctrine_id", "") for d in self.applicable_doctrines],
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class DisposalWellQuery(BaseModel):
    """Query for disposal well compliance analysis."""
    well_id: str
    operator: str = ""
    county: str = ""
    permit_number: str = ""
    injection_zone: str = ""
    daily_volume_bbls: Optional[float] = None
    injection_pressure_psi: Optional[float] = None
    well_depth_ft: Optional[float] = None
    last_mit_date: str = ""
    permit_expiration: str = ""
    annual_report_filed: bool = True
    seismic_event_nearby: bool = False


class DisposalWellComplianceResult(BaseModel):
    """Output from disposal well compliance analysis."""
    analysis_id: str
    well_id: str
    engine_id: str = ENGINE_ID
    compliance_score: float = 100.0
    status: str = "compliant"
    violations: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    applicable_rules: list[dict[str, Any]] = Field(default_factory=list)
    seismicity_assessment: Optional[dict[str, Any]] = None
    recommendations: list[str] = Field(default_factory=list)
    mit_status: str = ""
    permit_status: str = ""
    execution_time_ms: float = 0.0
    timestamp: str = ""
    determinism_hash: str = ""

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.analysis_id,
            "well": self.well_id,
            "score": self.compliance_score,
            "violations": len(self.violations),
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class AquiferQuery(BaseModel):
    """Query for aquifer analysis."""
    aquifer_name: str
    county: str = ""
    saturated_thickness_ft: Optional[float] = None
    pumping_af_per_yr: Optional[float] = None
    area_acres: Optional[float] = None
    tds_mg_l: Optional[float] = None


class AquiferAnalysisResult(BaseModel):
    """Output from aquifer analysis."""
    analysis_id: str
    engine_id: str = ENGINE_ID
    aquifer_name: str
    aquifer_data: dict[str, Any] = Field(default_factory=dict)
    depletion_assessment: Optional[dict[str, Any]] = None
    water_quality_class: str = ""
    is_usdw: bool = True
    suitable_uses: list[str] = Field(default_factory=list)
    gcd_info: Optional[dict[str, Any]] = None
    recommendations: list[str] = Field(default_factory=list)
    timestamp: str = ""
    determinism_hash: str = ""

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.analysis_id,
            "aquifer": self.aquifer_name,
            "usdw": self.is_usdw,
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class ConveyanceQuery(BaseModel):
    """Query for water rights conveyancing analysis."""
    transaction_type: str
    county: str = ""
    water_source: str = ""
    aquifer: str = ""
    volume_af: Optional[float] = None
    buyer: str = ""
    seller: str = ""
    use_purpose: str = ""


class ConveyanceAnalysisResult(BaseModel):
    """Output from conveyance analysis."""
    analysis_id: str
    engine_id: str = ENGINE_ID
    transaction_type: str
    legal_requirements: list[str] = Field(default_factory=list)
    gcd_requirements: list[str] = Field(default_factory=list)
    tceq_requirements: list[str] = Field(default_factory=list)
    title_examination_notes: list[str] = Field(default_factory=list)
    applicable_doctrines: list[dict[str, Any]] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    risk_factors: list[str] = Field(default_factory=list)
    timestamp: str = ""
    determinism_hash: str = ""

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.analysis_id, "type": self.transaction_type,
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class AccommodationQuery(BaseModel):
    """Query for accommodation doctrine analysis."""
    surface_use: str
    mineral_operation: str
    county: str = ""
    water_source: str = ""
    volume_bbls_day: Optional[float] = None
    alternative_sources_available: bool = False


class HealthResponse(BaseModel):
    """Engine health check response."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    mode: str = ENGINE_MODE
    port: int = ENGINE_PORT
    tier: str = ENGINE_TIER
    authority: float = ENGINE_AUTHORITY
    status: str = "healthy"
    uptime_seconds: float = 0.0
    doctrine_count: int = 0
    semantic_term_count: int = 0
    total_operations: int = 0
    error_rate: float = 0.0
    avg_latency_ms: float = 0.0
    drift_events_24h: int = 0
    timestamp: str = ""
    determinism_hash: str = ""


class BatchWaterRightQuery(BaseModel):
    """Input for batch water rights analysis."""
    queries: list[WaterRightQuery] = Field(..., min_length=1, max_length=50,
                                            description="List of queries to analyze in batch")
    parallel: bool = Field(default=False, description="Whether to run queries in parallel")


class WaterBudgetEntry(BaseModel):
    """Single entry in a water budget calculation."""
    source_name: str
    source_type: str
    volume_bbls_day: float = 0.0
    volume_af_year: float = 0.0
    cost_per_bbl: float = 0.0
    reliability_score: float = 0.0
    permit_status: str = "unknown"
    notes: str = ""


class WaterBudgetResult(BaseModel):
    """Output from water budget calculation."""
    budget_id: str
    engine_id: str = ENGINE_ID
    operator: str = ""
    county: str = ""
    total_supply_bbls_day: float = 0.0
    total_demand_bbls_day: float = 0.0
    surplus_deficit_bbls_day: float = 0.0
    supply_sources: list[WaterBudgetEntry] = Field(default_factory=list)
    demand_items: list[dict[str, Any]] = Field(default_factory=list)
    freshwater_pct: float = 0.0
    recycled_pct: float = 0.0
    recommendations: list[str] = Field(default_factory=list)
    timestamp: str = ""
    determinism_hash: str = ""

    def compute_hash(self) -> str:
        """C06: Compute determinism hash for water budget."""
        content = json.dumps({
            "id": self.budget_id,
            "supply": self.total_supply_bbls_day,
            "demand": self.total_demand_bbls_day,
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


class SpillReportingQuery(BaseModel):
    """Query for spill reporting requirements."""
    volume_bbls: float = Field(..., ge=0, description="Volume of spill in barrels")
    substance: str = Field(..., description="Substance spilled (e.g., crude_oil, produced_water, drilling_fluids)")
    reached_water: bool = Field(default=False, description="Whether spill reached surface water or groundwater")
    county: str = ""
    lease_name: str = ""
    operator: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class PitComplianceQuery(BaseModel):
    """Query for pit/impoundment compliance check."""
    pit_type: str = Field(..., description="Type: reserve_pit, saltwater_pit, freshwater_pit, mud_pit")
    lined: bool = False
    contents: str = ""
    distance_to_water_ft: float = 1000.0
    volume_bbls: float = 0.0
    county: str = ""
    active: bool = True


class RegulatoryContact(BaseModel):
    """Regulatory agency contact information."""
    agency: str
    office: str = ""
    phone: str = ""
    email: str = ""
    website: str = ""
    jurisdiction: str = ""
    notes: str = ""


# ---------------------------------------------------------------------------
# Permian Basin GCD Reference Data
# ---------------------------------------------------------------------------

PERMIAN_GCD_REGISTRY: dict[str, dict[str, Any]] = {
    "MIDLAND": {
        "gcd_name": "Permian Basin Underground Water Conservation District",
        "established": 1965,
        "counties_served": ["MIDLAND", "MARTIN"],
        "permit_required": True,
        "exempt_domestic_gpm": 25000,
        "spacing_rules": "Minimum 300 ft from property line for wells >25,000 gpd",
        "production_limits": "Based on acreage allocation model",
        "reporting_frequency": "annual",
        "website": "https://www.pbuwcd.com",
        "phone": "(432) 682-4375",
        "notes": "Covers most active Permian Basin drilling area. Strong metering requirements.",
    },
    "MARTIN": {
        "gcd_name": "Permian Basin Underground Water Conservation District",
        "established": 1965,
        "counties_served": ["MIDLAND", "MARTIN"],
        "permit_required": True,
        "exempt_domestic_gpm": 25000,
        "spacing_rules": "Same as Midland County rules",
        "production_limits": "Acreage allocation model",
        "reporting_frequency": "annual",
        "website": "https://www.pbuwcd.com",
        "phone": "(432) 682-4375",
        "notes": "Significant oil and gas water demand. GCD monitoring water levels.",
    },
    "ECTOR": {
        "gcd_name": "No GCD established",
        "established": 0,
        "counties_served": ["ECTOR"],
        "permit_required": False,
        "exempt_domestic_gpm": 0,
        "spacing_rules": "No GCD spacing rules; Rule of Capture applies fully",
        "production_limits": "None (no GCD)",
        "reporting_frequency": "none",
        "website": "",
        "phone": "",
        "notes": "Rule of Capture applies. No permitting required. Consider TWDB well registration.",
    },
    "REEVES": {
        "gcd_name": "Middle Pecos Groundwater Conservation District",
        "established": 2005,
        "counties_served": ["REEVES", "PECOS"],
        "permit_required": True,
        "exempt_domestic_gpm": 25000,
        "spacing_rules": "Minimum 200 ft from property line for non-exempt wells",
        "production_limits": "Based on historical use and sustainable yield",
        "reporting_frequency": "annual",
        "website": "",
        "phone": "(432) 447-9651",
        "notes": "Active area for oil and gas water use. GCD working on DFC implementation.",
    },
    "PECOS": {
        "gcd_name": "Middle Pecos Groundwater Conservation District",
        "established": 2005,
        "counties_served": ["REEVES", "PECOS"],
        "permit_required": True,
        "exempt_domestic_gpm": 25000,
        "spacing_rules": "Same as Reeves County",
        "production_limits": "Sustainable yield allocation",
        "reporting_frequency": "annual",
        "website": "",
        "phone": "(432) 447-9651",
        "notes": "Pecos River Compact implications for surface/groundwater interaction.",
    },
    "WARD": {
        "gcd_name": "Ward County Water Improvement District",
        "established": 1928,
        "counties_served": ["WARD"],
        "permit_required": True,
        "exempt_domestic_gpm": 25000,
        "spacing_rules": "District-specific rules",
        "production_limits": "Annual allocation",
        "reporting_frequency": "annual",
        "website": "",
        "phone": "",
        "notes": "Historical irrigation district with evolving oil and gas water management.",
    },
}


def get_gcd_info(county: str) -> dict[str, Any]:
    """Look up GCD information for a Texas county."""
    info = PERMIAN_GCD_REGISTRY.get(county.upper())
    if info:
        return {
            "found": True,
            "county": county.upper(),
            **info,
        }
    return {
        "found": False,
        "county": county.upper(),
        "notes": f"No GCD data available for {county} County. Check TWDB GCD map for current status.",
        "twdb_gcd_map": "https://www.twdb.texas.gov/groundwater/conservation_districts/",
    }


# ---------------------------------------------------------------------------
# Core Engine Components
# ---------------------------------------------------------------------------

class WaterRightClassifier:
    """C01/C09: Classify water type and assess risk."""

    def classify(self, tds_mg_l: Optional[float], source: str, use: str) -> dict[str, Any]:
        classification = WaterClassification.UNKNOWN
        risk = RiskLevel.LOW
        if source.lower() in ("produced", "formation", "brine"):
            classification = WaterClassification.PRODUCED_WATER
            risk = RiskLevel.MODERATE
        elif source.lower() in ("flowback", "frac_flowback"):
            classification = WaterClassification.FLOWBACK_WATER
            risk = RiskLevel.MODERATE
        elif source.lower() in ("recycled", "treated_produced"):
            classification = WaterClassification.RECYCLED_WATER
            risk = RiskLevel.LOW
        elif source.lower() in ("river", "stream", "lake", "reservoir"):
            classification = WaterClassification.SURFACE_WATER
            risk = RiskLevel.MODERATE
        elif source.lower() in ("municipal", "city_water"):
            classification = WaterClassification.MUNICIPAL_WATER
            risk = RiskLevel.LOW
        elif tds_mg_l is not None:
            if tds_mg_l < 1000:
                classification = WaterClassification.FRESH_GROUNDWATER
                risk = RiskLevel.LOW
            elif tds_mg_l < 10000:
                classification = WaterClassification.BRACKISH_GROUNDWATER
                risk = RiskLevel.LOW
            else:
                classification = WaterClassification.SALINE_GROUNDWATER
                risk = RiskLevel.MODERATE
        permits_needed: list[str] = []
        if classification == WaterClassification.FRESH_GROUNDWATER:
            permits_needed.append("GCD production permit (if non-exempt)")
        elif classification == WaterClassification.SURFACE_WATER:
            permits_needed.append("TCEQ appropriation permit")
        elif classification == WaterClassification.PRODUCED_WATER:
            permits_needed.append("RRC H-1 disposal permit (if disposing)")
            permits_needed.append("RRC Rule 46 notification (if recycling)")
        elif classification == WaterClassification.BRACKISH_GROUNDWATER:
            permits_needed.append("GCD permit (may be required)")
            permits_needed.append("TCEQ concentrate disposal permit (if desalinating)")
        return {
            "classification": classification.value,
            "risk_level": risk.value,
            "tds_mg_l": tds_mg_l,
            "source": source,
            "use": use,
            "permits_needed": permits_needed,
            "is_usdw_source": tds_mg_l is not None and tds_mg_l < 10000,
        }


class GroundwaterAnalyzer:
    """C02/C10: Analyze groundwater rights and GCD compliance."""

    def __init__(self) -> None:
        self._gw_analyzer = GroundwaterRightsAnalyzer()
        self._gcd_rules = GROUNDWATER_RULES

    def analyze_gcd_compliance(self, county: str, gpm: float, use: str) -> dict[str, Any]:
        permit_check = self._gw_analyzer.determine_gcd_permit_needed(gpm, use, county)
        applicable_rules: list[dict[str, str]] = []
        for rule in self._gcd_rules:
            if rule.county.lower() == county.lower():
                applicable_rules.append({
                    "rule_id": rule.rule_id,
                    "district": rule.district_name,
                    "rule_number": rule.rule_number,
                    "title": rule.title,
                    "oilfield_provisions": rule.oilfield_provisions,
                })
        return {
            "county": county,
            "gpm": gpm,
            "use": use,
            "permit_analysis": permit_check,
            "applicable_gcd_rules": applicable_rules,
            "gcd_found": len(applicable_rules) > 0,
        }

    def evaluate_rule_of_capture(self, scenario: dict[str, Any]) -> dict[str, Any]:
        return self._gw_analyzer.evaluate_rule_of_capture(scenario)

    def assess_water_source(self, tds: float) -> dict[str, Any]:
        classification = self._gw_analyzer.classify_water_source(tds)
        is_usdw = self._gw_analyzer.is_usdw(tds)
        return {
            "tds_mg_l": tds,
            "classification": classification,
            "is_usdw": is_usdw,
            "drinking_water_quality": tds < 500,
        }


class SurfaceWaterAnalyzer:
    """C03: Analyze surface water rights and permit requirements."""

    def __init__(self) -> None:
        self._sw_checker = SurfaceWaterPermitChecker()

    def check_permit_requirements(self, use: str, volume_af_year: float, source: str) -> dict[str, Any]:
        return self._sw_checker.check_permit_needed(use, volume_af_year, source)

    def check_cancellation_risk(self, last_use_date: str) -> dict[str, Any]:
        current_date = datetime.now().strftime("%Y-%m-%d")
        return self._sw_checker.check_cancellation_risk(last_use_date, current_date)


class ProducedWaterManager:
    """C04: Manage produced water compliance and disposal analysis."""

    def __init__(self) -> None:
        self._pw_engine = ProducedWaterComplianceEngine()

    def evaluate_disposal(self, method: str, volume_bbls_day: float, county: str) -> dict[str, Any]:
        return self._pw_engine.evaluate_disposal_method(method, volume_bbls_day, county)

    def score_well_compliance(self, well_data: dict[str, Any]) -> dict[str, Any]:
        return self._pw_engine.score_compliance(well_data)


class DisposalWellComplianceAnalyzer:
    """C05: Full disposal well compliance analysis."""

    def __init__(self) -> None:
        self._checker = DisposalWellComplianceChecker()
        self._iw_standards = INJECTION_WELL_STANDARDS

    def analyze(self, query: DisposalWellQuery) -> DisposalWellComplianceResult:
        start = time.monotonic()
        analysis_id = f"DW-{uuid.uuid4().hex[:12]}"
        well_data = {
            "permit_expiration": query.permit_expiration,
            "last_mit_date": query.last_mit_date,
            "daily_volume_bbls": query.daily_volume_bbls or 0,
            "permitted_volume_bbls": 30000,
            "injection_pressure_psi": query.injection_pressure_psi or 0,
            "max_permitted_pressure_psi": (query.well_depth_ft or 10000) * 0.5,
            "annual_report_filed": query.annual_report_filed,
            "seismic_event_nearby": query.seismic_event_nearby,
        }
        self._checker.register_well(query.well_id, well_data)
        compliance = self._checker.check_compliance(query.well_id)
        applicable_rules: list[dict[str, Any]] = []
        for std in self._iw_standards:
            applicable_rules.append({
                "std_id": std.std_id,
                "title": std.title,
                "well_class": std.well_class,
                "citation": std.citation,
                "mit_interval_years": std.mit_interval_years,
            })
        seismicity = None
        if query.seismic_event_nearby or (query.county and query.county.lower() in ("reeves", "pecos", "ward", "culberson")):
            seismicity = {
                "in_review_area": True,
                "county": query.county,
                "protocol": "RRC Traffic Light Protocol applies",
                "recommendation": "Monitor TexNet for seismic events within 10-mile radius",
                "current_level": SeismicityLevel.YELLOW.value if query.seismic_event_nearby else SeismicityLevel.GREEN.value,
            }
        mit_status = "current"
        if query.last_mit_date:
            from datetime import datetime as dt
            try:
                last = dt.strptime(query.last_mit_date, "%Y-%m-%d")
                years = (dt.now() - last).days / 365.25
                if years > 5:
                    mit_status = "OVERDUE"
                elif years > 4:
                    mit_status = f"due_within_{int((5 - years) * 12)}_months"
                else:
                    mit_status = "current"
            except ValueError:
                mit_status = "unknown"
        permit_status = "active"
        if query.permit_expiration:
            from datetime import datetime as dt
            try:
                exp = dt.strptime(query.permit_expiration, "%Y-%m-%d")
                if exp < dt.now():
                    permit_status = "EXPIRED"
                elif (exp - dt.now()).days < 90:
                    permit_status = f"expiring_in_{(exp - dt.now()).days}_days"
            except ValueError:
                permit_status = "unknown"
        recommendations: list[str] = []
        if mit_status == "OVERDUE":
            recommendations.append("URGENT: Schedule mechanical integrity test immediately")
        if permit_status == "EXPIRED":
            recommendations.append("URGENT: Cease injection operations; renew permit before resuming")
        if seismicity and seismicity["current_level"] != "green":
            recommendations.append("Monitor seismic activity; prepare for potential volume curtailment")
        if compliance.get("compliance_score", 100) < 80:
            recommendations.append("Address identified violations before next RRC inspection")
        elapsed = (time.monotonic() - start) * 1000
        result = DisposalWellComplianceResult(
            analysis_id=analysis_id,
            well_id=query.well_id,
            compliance_score=compliance.get("compliance_score", 0),
            status=compliance.get("status", "unknown"),
            violations=compliance.get("violations", []),
            warnings=compliance.get("warnings", []),
            applicable_rules=applicable_rules,
            seismicity_assessment=seismicity,
            recommendations=recommendations,
            mit_status=mit_status,
            permit_status=permit_status,
            execution_time_ms=round(elapsed, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        result.compute_hash()
        return result


class AquiferAnalysisEngine:
    """C06: Aquifer analysis and depletion assessment."""

    def __init__(self) -> None:
        self._analyzer = AquiferAnalyzer()
        self._searcher = AquiferDataSearcher()

    def analyze(self, query: AquiferQuery) -> AquiferAnalysisResult:
        analysis_id = f"AQ-{uuid.uuid4().hex[:12]}"
        aq_data = self._searcher.get_aquifer(query.aquifer_name) or {}
        depletion = None
        if query.saturated_thickness_ft and query.pumping_af_per_yr and query.area_acres:
            recharge = aq_data.get("recharge_in_per_yr", 0.5)
            depletion = self._analyzer.assess_depletion_risk(
                query.aquifer_name, query.saturated_thickness_ft,
                recharge, query.pumping_af_per_yr, query.area_acres,
            )
        tds = query.tds_mg_l or (aq_data.get("tds_range", [500])[0] if aq_data.get("tds_range") else 500)
        aq_class = self._analyzer.classify_aquifer(tds, aq_data.get("type", "unknown"))
        recommendations: list[str] = []
        if depletion and depletion.get("depletion_risk") in ("high", "critical"):
            recommendations.append("Consider alternative water sources (brackish, recycled) to reduce freshwater depletion")
            recommendations.append("Monitor water levels annually and report to GCD")
        if aq_class.get("is_usdw"):
            recommendations.append("USDW protection requirements apply to all nearby injection wells")
        result = AquiferAnalysisResult(
            analysis_id=analysis_id,
            aquifer_name=query.aquifer_name,
            aquifer_data=aq_data,
            depletion_assessment=depletion,
            water_quality_class=aq_class.get("quality_class", ""),
            is_usdw=aq_class.get("is_usdw", True),
            suitable_uses=aq_class.get("suitable_uses", []),
            recommendations=recommendations,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        result.compute_hash()
        return result


class WaterConveyanceTracker:
    """C07: Track water rights conveyances and transfers."""

    def analyze_conveyance(self, query: ConveyanceQuery) -> ConveyanceAnalysisResult:
        analysis_id = f"CV-{uuid.uuid4().hex[:12]}"
        legal_reqs: list[str] = []
        gcd_reqs: list[str] = []
        tceq_reqs: list[str] = []
        title_notes: list[str] = []
        risk_factors: list[str] = []
        recommendations: list[str] = []
        tx_type = query.transaction_type.lower()
        if "groundwater" in tx_type or "severance" in tx_type or "water_deed" in tx_type:
            legal_reqs.extend([
                "Written deed instrument required for groundwater severance (TWC 36.002(d-1))",
                "Legal description of land from which rights are severed",
                "Specify aquifer, volume, and duration of rights conveyed",
                "Record in county deed records",
            ])
            gcd_reqs.extend([
                "Notify GCD of change in ownership for existing permits",
                "New owner must apply for production permit transfer or new permit",
                "Verify export restrictions if water will be used outside GCD boundary",
            ])
            title_notes.extend([
                "Search deed records for prior severances of water rights",
                "Check GCD records for existing permits and allocations",
                "Verify no liens or encumbrances on water rights",
                "Confirm surface access rights are included or separately addressed",
            ])
            risk_factors.extend([
                "Severed rights do not include surface access (Coyote Lake Ranch v. Lubbock)",
                "GCD may restrict production regardless of purchased volume",
                "DFC/MAG changes may reduce available allocation in future",
            ])
        elif "surface" in tx_type or "appropriation" in tx_type or "transfer" in tx_type:
            legal_reqs.extend([
                "TCEQ transfer application required (TWC 11.122)",
                "Public notice and comment period",
                "No-injury determination required",
            ])
            tceq_reqs.extend([
                "File transfer application with TCEQ Water Rights section",
                "Include proof of ownership of existing permit",
                "Demonstrate no injury to existing water rights holders",
                "Environmental flow conditions may be added on transfer",
            ])
            title_notes.extend([
                "Obtain copy of existing TCEQ water rights certificate",
                "Review permit conditions, priority date, and authorized use",
                "Check for pending cancellation proceedings (10-year non-use)",
            ])
        recommendations.extend([
            "Engage water rights attorney for transaction documentation",
            "Conduct thorough title examination of water rights",
            "Obtain representations and warranties regarding permit status and compliance",
        ])
        result = ConveyanceAnalysisResult(
            analysis_id=analysis_id,
            transaction_type=query.transaction_type,
            legal_requirements=legal_reqs,
            gcd_requirements=gcd_reqs,
            tceq_requirements=tceq_reqs,
            title_examination_notes=title_notes,
            applicable_doctrines=[],
            recommendations=recommendations,
            risk_factors=risk_factors,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        result.compute_hash()
        return result


class AccommodationDoctrineEvaluator:
    """C08: Evaluate accommodation doctrine issues for water use."""

    def evaluate(self, query: AccommodationQuery) -> dict[str, Any]:
        analysis_id = f"ACC-{uuid.uuid4().hex[:12]}"
        accommodation_applies = True
        reasoning: list[str] = []
        recommendations: list[str] = []
        risk = "moderate"
        reasoning.append("Getty Oil v. Jones (1971) established the accommodation doctrine requiring mineral lessee to accommodate existing surface uses")
        reasoning.append("Coyote Lake Ranch v. Lubbock (2016) extended to groundwater access by severed rights holder")
        if query.alternative_sources_available:
            reasoning.append("Alternative water sources available - lessee has duty to use them rather than impairing surface owner's water supply")
            risk = "high"
            recommendations.append("Use alternative water sources (recycled, brackish, off-site) to avoid accommodation doctrine liability")
        else:
            reasoning.append("No alternative water sources identified - mineral estate may prevail if extraction is reasonably necessary")
            risk = "moderate"
            recommendations.append("Document absence of reasonable alternative water sources")
        recommendations.extend([
            "Negotiate comprehensive surface use agreement addressing water allocation",
            "Meter all water use and maintain records",
            "Avoid interference with surface owner's existing water wells and infrastructure",
        ])
        return {
            "analysis_id": analysis_id,
            "accommodation_applies": accommodation_applies,
            "surface_use": query.surface_use,
            "mineral_operation": query.mineral_operation,
            "risk_level": risk,
            "legal_reasoning": reasoning,
            "recommendations": recommendations,
            "key_cases": [
                "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
                "Coyote Lake Ranch v. City of Lubbock, 498 S.W.3d 53 (Tex. 2016)",
            ],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class FreshwaterProtectionChecker:
    """C10: Check freshwater protection compliance."""

    def check_rule_8_compliance(self, well_data: dict[str, Any]) -> dict[str, Any]:
        issues: list[str] = []
        compliant = True
        surface_casing = well_data.get("surface_casing_depth_ft", 0)
        buqw_depth = well_data.get("buqw_depth_ft", 0)
        if buqw_depth > 0 and surface_casing < buqw_depth:
            compliant = False
            issues.append(f"Surface casing ({surface_casing} ft) does not extend below BUQW depth ({buqw_depth} ft)")
        if not well_data.get("cement_to_surface", False):
            compliant = False
            issues.append("Surface casing not cemented to surface")
        if not well_data.get("tceq_letter_obtained", False):
            issues.append("TCEQ freshwater protection letter not on file")
        if well_data.get("pit_liner_missing", False):
            compliant = False
            issues.append("Pit liner missing for fluid containment")
        return {
            "compliant": compliant,
            "issues": issues,
            "rule_8_citation": "16 TAC Sec. 3.8",
            "surface_casing_depth_ft": surface_casing,
            "buqw_depth_ft": buqw_depth,
            "recommendations": [
                "Ensure TCEQ letter is obtained before drilling",
                "Set surface casing below all freshwater zones",
                "Cement surface casing to surface with returns",
            ] if not compliant else ["Rule 8 compliance verified"],
        }

    def assess_usdw_risk(self, injection_zone_depth_ft: float, usdw_base_ft: float,
                         confining_zone_thickness_ft: float) -> dict[str, Any]:
        """Assess risk of injection operations to USDWs."""
        separation = injection_zone_depth_ft - usdw_base_ft
        risk = "low"
        concerns: list[str] = []
        recommendations: list[str] = []
        if separation < 250:
            risk = "critical"
            concerns.append(f"Injection zone only {separation:.0f} ft below USDW base (minimum 500 ft recommended)")
            recommendations.append("Conduct detailed geological review of confining zone integrity")
            recommendations.append("Install monitoring wells between injection zone and USDW")
        elif separation < 500:
            risk = "high"
            concerns.append(f"Injection zone {separation:.0f} ft below USDW base (less than 500 ft recommended separation)")
            recommendations.append("Enhanced monitoring of annular pressure recommended")
        elif separation < 1000:
            risk = "moderate"
        if confining_zone_thickness_ft < 50:
            risk = "critical" if risk != "critical" else risk
            concerns.append(f"Confining zone thickness ({confining_zone_thickness_ft:.0f} ft) is thin")
            recommendations.append("Evaluate confining zone permeability and continuity")
        return {
            "injection_zone_depth_ft": injection_zone_depth_ft,
            "usdw_base_ft": usdw_base_ft,
            "separation_ft": separation,
            "confining_zone_thickness_ft": confining_zone_thickness_ft,
            "risk_level": risk,
            "concerns": concerns,
            "recommendations": recommendations if recommendations else ["Adequate separation from USDW"],
        }

    def evaluate_spill_reporting(self, spill_volume_bbls: float, substance: str,
                                 reached_water: bool) -> dict[str, Any]:
        """Evaluate spill reporting requirements under Rule 8."""
        must_report = False
        report_timeframe = ""
        agencies: list[str] = []
        notes: list[str] = []
        if reached_water:
            must_report = True
            report_timeframe = "immediately"
            agencies.extend(["RRC", "TCEQ"])
            notes.append("Any spill reaching water requires immediate notification")
        if substance.lower() in ("crude_oil", "oil") and spill_volume_bbls > 5:
            must_report = True
            report_timeframe = "within 24 hours" if not reached_water else "immediately"
            if "RRC" not in agencies:
                agencies.append("RRC")
            notes.append(f"Crude oil spill of {spill_volume_bbls} bbls exceeds 5-bbl reporting threshold")
        elif substance.lower() in ("produced_water", "saltwater", "brine"):
            if spill_volume_bbls > 1 or reached_water:
                must_report = True
                report_timeframe = "within 24 hours" if not reached_water else "immediately"
                agencies.append("RRC")
                notes.append("Produced water release reporting triggered")
        if spill_volume_bbls > 25:
            notes.append("Large volume spill: consider NRC notification (1-800-424-8802)")
            if "TCEQ" not in agencies:
                agencies.append("TCEQ")
        return {
            "spill_volume_bbls": spill_volume_bbls,
            "substance": substance,
            "reached_water": reached_water,
            "must_report": must_report,
            "report_timeframe": report_timeframe,
            "agencies_to_notify": agencies,
            "notes": notes,
            "rule_8_citation": "16 TAC Sec. 3.8",
        }


class SeismicityRiskEvaluator:
    """Evaluate seismicity risk for disposal well operations."""

    def __init__(self) -> None:
        self._review_areas = {
            "reeves": {"risk": "high", "recent_events": True, "max_magnitude": 4.5},
            "pecos": {"risk": "high", "recent_events": True, "max_magnitude": 3.8},
            "ward": {"risk": "moderate", "recent_events": True, "max_magnitude": 3.2},
            "culberson": {"risk": "moderate", "recent_events": False, "max_magnitude": 2.5},
            "loving": {"risk": "moderate", "recent_events": True, "max_magnitude": 3.0},
            "midland": {"risk": "low", "recent_events": False, "max_magnitude": 1.5},
            "ector": {"risk": "low", "recent_events": False, "max_magnitude": 1.2},
            "martin": {"risk": "low", "recent_events": False, "max_magnitude": 1.0},
        }

    def evaluate(self, county: str, daily_volume_bbls: float,
                 injection_depth_ft: float, nearby_magnitude: Optional[float] = None) -> dict[str, Any]:
        """Evaluate seismicity risk for a disposal well location."""
        county_lower = county.lower()
        area_info = self._review_areas.get(county_lower, {"risk": "unknown", "recent_events": False, "max_magnitude": 0})
        traffic_light = SeismicityLevel.GREEN
        actions: list[str] = []
        risk_factors: list[str] = []
        if nearby_magnitude is not None:
            if nearby_magnitude >= 4.0:
                traffic_light = SeismicityLevel.RED
                actions.append("IMMEDIATE SHUT-IN of all disposal wells within review area")
                actions.append("Notify RRC within 24 hours")
                actions.append("Conduct seismic monitoring and submit report")
            elif nearby_magnitude >= 3.5:
                traffic_light = SeismicityLevel.ORANGE
                actions.append("SUSPEND operations pending RRC review")
                actions.append("Submit enhanced seismic monitoring data")
                actions.append("Prepare volume reduction plan")
            elif nearby_magnitude >= 2.0:
                traffic_light = SeismicityLevel.YELLOW
                actions.append("Reduce injection volume by 50%")
                actions.append("Increase monitoring frequency")
                actions.append("Report to RRC if magnitude exceeds 3.0")
        if daily_volume_bbls > 20000:
            risk_factors.append(f"High daily volume ({daily_volume_bbls:,.0f} bbls/day)")
        if injection_depth_ft < 5000:
            risk_factors.append(f"Shallow injection depth ({injection_depth_ft:,.0f} ft) - higher seismicity correlation")
        if area_info.get("risk") == "high":
            risk_factors.append(f"{county} County is in RRC seismic review area")
        if area_info.get("recent_events"):
            risk_factors.append(f"Recent seismic events recorded in {county} County")
        recommendations: list[str] = []
        if traffic_light == SeismicityLevel.GREEN:
            recommendations.append("Continue normal operations with standard monitoring")
        if area_info.get("risk") in ("high", "moderate"):
            recommendations.append("Install seismic monitoring station if not already present")
            recommendations.append("Maintain current TexNet data subscription")
        if daily_volume_bbls > 15000:
            recommendations.append("Consider distributing volume across multiple wells to reduce per-well risk")
        return {
            "county": county,
            "daily_volume_bbls": daily_volume_bbls,
            "injection_depth_ft": injection_depth_ft,
            "nearby_magnitude": nearby_magnitude,
            "traffic_light_level": traffic_light.value,
            "area_risk": area_info.get("risk", "unknown"),
            "in_review_area": area_info.get("risk") in ("high", "moderate"),
            "risk_factors": risk_factors,
            "required_actions": actions,
            "recommendations": recommendations,
            "protocol_citation": "RRC Disposal Well Seismicity Response Protocol (2014, updated 2023)",
        }

    def assess_permit_risk(self, county: str) -> dict[str, Any]:
        """Assess likelihood of enhanced permit scrutiny due to seismicity."""
        county_lower = county.lower()
        area_info = self._review_areas.get(county_lower, {"risk": "unknown"})
        enhanced_scrutiny = area_info.get("risk") in ("high", "moderate")
        timeline_impact = "none"
        additional_requirements: list[str] = []
        if area_info.get("risk") == "high":
            timeline_impact = "significant_delay"
            additional_requirements.extend([
                "Enhanced seismic monitoring plan required with application",
                "Pre-injection seismic baseline study may be required",
                "Lower maximum injection pressure may be imposed",
                "Volume restrictions likely",
                "Additional public notice and comment period",
            ])
        elif area_info.get("risk") == "moderate":
            timeline_impact = "moderate_delay"
            additional_requirements.extend([
                "Seismic monitoring plan recommended",
                "RRC may request additional geological data",
                "Volume monitoring conditions likely",
            ])
        return {
            "county": county,
            "enhanced_scrutiny": enhanced_scrutiny,
            "area_risk": area_info.get("risk", "unknown"),
            "timeline_impact": timeline_impact,
            "additional_requirements": additional_requirements,
        }


class InterstateCompactAnalyzer:
    """Analyze interstate water compact compliance and impacts."""

    def check_pecos_compact(self, water_use: str, volume_af: float, county: str) -> dict[str, Any]:
        """Check Pecos River Compact implications for water use."""
        pecos_counties = {"reeves", "pecos", "terrell", "crockett", "ward", "loving"}
        is_pecos_basin = county.lower() in pecos_counties
        compact_relevant = is_pecos_basin and water_use.lower() in ("surface_water", "river", "stream")
        notes: list[str] = []
        if compact_relevant:
            notes.append("Pecos River Compact (1949) governs interstate allocation")
            notes.append("New Mexico must deliver water to Texas per inflow-outflow formula")
            notes.append("River Master appointed by U.S. Supreme Court administers deliveries")
            notes.append(f"Water use of {volume_af} AF/yr from Pecos River subject to TCEQ surface water permit")
        if is_pecos_basin and water_use.lower() in ("groundwater", "well"):
            notes.append("Groundwater pumping from Pecos Valley Aquifer may affect river baseflow")
            notes.append("Compact does not directly regulate groundwater but hydrologic connection is recognized")
        return {
            "county": county,
            "water_use": water_use,
            "volume_af": volume_af,
            "is_pecos_basin": is_pecos_basin,
            "compact_relevant": compact_relevant,
            "compact": "Pecos River Compact (63 Stat. 159, 1949)" if compact_relevant else "N/A",
            "notes": notes,
            "key_case": "Texas v. New Mexico, 482 U.S. 124 (1987)" if compact_relevant else "",
        }

    def check_rio_grande_compact(self, county: str) -> dict[str, Any]:
        """Check Rio Grande Compact relevance for a county."""
        rio_grande_counties = {
            "el_paso", "hudspeth", "presidio", "brewster", "terrell",
            "val_verde", "kinney", "maverick", "webb", "zapata",
            "starr", "hidalgo", "cameron",
        }
        county_normalized = county.lower().replace(" ", "_")
        relevant = county_normalized in rio_grande_counties
        return {
            "county": county,
            "compact_relevant": relevant,
            "compact": "Rio Grande Compact (53 Stat. 785, 1939)" if relevant else "N/A",
            "notes": [
                "Rio Grande Compact governs CO-NM-TX water allocation",
                "Texas allocation administered through Elephant Butte index",
                "Bureau of Reclamation operates Rio Grande Project",
            ] if relevant else [],
        }


class WaterEconomicsCalculator:
    """Calculate water costs and economics for oil and gas operations."""

    def calculate_frack_water_cost(self, volume_bbls: float, source: str,
                                    transport_miles: float, county: str) -> dict[str, Any]:
        """Estimate cost of water for fracking operations."""
        base_cost_per_bbl = 0.0
        transport_cost_per_bbl = 0.0
        treatment_cost_per_bbl = 0.0
        source_lower = source.lower()
        if source_lower in ("freshwater", "groundwater", "fresh"):
            base_cost_per_bbl = 0.50
        elif source_lower in ("brackish", "brackish_groundwater"):
            base_cost_per_bbl = 0.30
            treatment_cost_per_bbl = 0.75
        elif source_lower in ("recycled", "recycled_produced"):
            base_cost_per_bbl = 0.15
            treatment_cost_per_bbl = 0.60
        elif source_lower in ("municipal", "city"):
            base_cost_per_bbl = 1.50
        elif source_lower in ("surface", "river"):
            base_cost_per_bbl = 0.40
        else:
            base_cost_per_bbl = 0.75
        if transport_miles <= 5:
            transport_cost_per_bbl = 0.10
        elif transport_miles <= 15:
            transport_cost_per_bbl = 0.30
        elif transport_miles <= 30:
            transport_cost_per_bbl = 0.60
        else:
            transport_cost_per_bbl = 0.15 * (transport_miles / 5)
        total_per_bbl = base_cost_per_bbl + transport_cost_per_bbl + treatment_cost_per_bbl
        total_cost = total_per_bbl * volume_bbls
        gallons = volume_bbls * 42
        cost_per_1000_gal = (total_per_bbl / 42) * 1000
        return {
            "volume_bbls": volume_bbls,
            "volume_gallons": gallons,
            "source": source,
            "transport_miles": transport_miles,
            "county": county,
            "cost_breakdown": {
                "source_cost_per_bbl": round(base_cost_per_bbl, 2),
                "transport_cost_per_bbl": round(transport_cost_per_bbl, 2),
                "treatment_cost_per_bbl": round(treatment_cost_per_bbl, 2),
                "total_cost_per_bbl": round(total_per_bbl, 2),
                "total_cost_per_1000_gal": round(cost_per_1000_gal, 2),
            },
            "total_cost_usd": round(total_cost, 2),
            "notes": [
                f"Estimated cost for {volume_bbls:,.0f} bbls of {source} water in {county} County",
                f"Transport distance: {transport_miles} miles",
                "Costs are estimates; actual costs vary by contract and market conditions",
            ],
        }

    def compare_water_sources(self, volume_bbls: float, transport_miles: float,
                               county: str) -> dict[str, Any]:
        """Compare costs across water source types."""
        sources = ["freshwater", "brackish", "recycled", "municipal"]
        comparisons: list[dict[str, Any]] = []
        for source in sources:
            calc = self.calculate_frack_water_cost(volume_bbls, source, transport_miles, county)
            comparisons.append({
                "source": source,
                "cost_per_bbl": calc["cost_breakdown"]["total_cost_per_bbl"],
                "total_cost_usd": calc["total_cost_usd"],
            })
        comparisons.sort(key=lambda x: x["cost_per_bbl"])
        return {
            "volume_bbls": volume_bbls,
            "transport_miles": transport_miles,
            "county": county,
            "comparisons": comparisons,
            "recommended_source": comparisons[0]["source"],
            "potential_savings_vs_freshwater": round(
                next(c["total_cost_usd"] for c in comparisons if c["source"] == "freshwater") - comparisons[0]["total_cost_usd"], 2
            ),
        }

    def calculate_disposal_cost(self, volume_bbls_day: float, method: str,
                                 transport_miles: float) -> dict[str, Any]:
        """Calculate produced water disposal costs."""
        disposal_fee_per_bbl = 0.0
        method_lower = method.lower()
        if method_lower in ("swd", "saltwater_disposal"):
            disposal_fee_per_bbl = 0.75
        elif method_lower in ("recycling", "recycle"):
            disposal_fee_per_bbl = 0.50
        elif method_lower in ("eor", "enhanced_recovery"):
            disposal_fee_per_bbl = 0.25
        elif method_lower in ("evaporation", "evap_pit"):
            disposal_fee_per_bbl = 0.40
        else:
            disposal_fee_per_bbl = 1.00
        transport_per_bbl = 0.0
        if transport_miles > 0:
            if method_lower in ("truck", "truck_haul"):
                transport_per_bbl = 0.10 * transport_miles
            else:
                transport_per_bbl = 0.02 * transport_miles
        total_per_bbl = disposal_fee_per_bbl + transport_per_bbl
        daily_cost = total_per_bbl * volume_bbls_day
        monthly_cost = daily_cost * 30
        annual_cost = daily_cost * 365
        return {
            "volume_bbls_day": volume_bbls_day,
            "method": method,
            "transport_miles": transport_miles,
            "disposal_fee_per_bbl": round(disposal_fee_per_bbl, 2),
            "transport_cost_per_bbl": round(transport_per_bbl, 2),
            "total_cost_per_bbl": round(total_per_bbl, 2),
            "daily_cost_usd": round(daily_cost, 2),
            "monthly_cost_usd": round(monthly_cost, 2),
            "annual_cost_usd": round(annual_cost, 2),
        }


class DroughtContingencyAnalyzer:
    """Analyze drought contingency planning and curtailment impacts."""

    def assess_drought_risk(self, county: str, water_source: str,
                            volume_af_per_yr: float) -> dict[str, Any]:
        """Assess drought risk for water supply operations."""
        arid_counties = {
            "reeves", "pecos", "ward", "winkler", "loving", "culberson",
            "ector", "midland", "martin", "andrews", "crane", "upton",
        }
        is_arid = county.lower() in arid_counties
        drought_history = {
            "last_major_drought": "2011",
            "drought_of_record": "1950-1957",
            "avg_annual_rainfall_in": 14.0 if is_arid else 22.0,
        }
        risk_level = "high" if is_arid else "moderate"
        if water_source.lower() in ("surface_water", "river", "stream"):
            risk_level = "critical" if is_arid else "high"
        curtailment_risk: list[str] = []
        if water_source.lower() in ("groundwater", "well"):
            curtailment_risk.append("GCD may impose emergency production restrictions during declared drought")
            curtailment_risk.append("Oil and gas use may be curtailed before domestic and livestock")
        elif water_source.lower() in ("surface_water", "river"):
            curtailment_risk.append("Junior appropriators curtailed first during shortage")
            curtailment_risk.append("Watermaster may issue priority call cutting off junior rights")
        recommendations: list[str] = [
            "Maintain multiple water source agreements (redundancy)",
            "Invest in produced water recycling capacity as drought backup",
            "Monitor TWDB drought conditions and GCD drought declarations",
            "Include force majeure and drought curtailment provisions in water supply contracts",
        ]
        if is_arid:
            recommendations.append("Consider on-site water storage (frac tanks, lined pits) for buffer supply")
        return {
            "county": county,
            "water_source": water_source,
            "volume_af_per_yr": volume_af_per_yr,
            "drought_risk": risk_level,
            "is_arid_region": is_arid,
            "drought_history": drought_history,
            "curtailment_risks": curtailment_risk,
            "recommendations": recommendations,
        }


class WaterSupplyPlanningEngine:
    """Plan water supply strategies for oil and gas operations."""

    def __init__(self) -> None:
        self._economics = WaterEconomicsCalculator()
        self._drought = DroughtContingencyAnalyzer()

    def create_supply_plan(self, county: str, wells_planned: int,
                           avg_water_per_well_bbls: float,
                           completion_schedule_months: int) -> dict[str, Any]:
        """Create a water supply plan for drilling operations."""
        total_water_bbls = wells_planned * avg_water_per_well_bbls
        total_water_af = total_water_bbls / 7758.0
        monthly_rate_bbls = total_water_bbls / max(completion_schedule_months, 1)
        daily_peak_bbls = monthly_rate_bbls / 20
        sources_recommended: list[dict[str, Any]] = []
        freshwater_pct = 0.5
        recycled_pct = 0.3
        brackish_pct = 0.2
        sources_recommended.append({
            "source": "freshwater_groundwater",
            "percentage": freshwater_pct * 100,
            "volume_bbls": round(total_water_bbls * freshwater_pct),
            "permits_required": ["GCD production permit"],
            "estimated_cost_per_bbl": 0.60,
        })
        sources_recommended.append({
            "source": "recycled_produced_water",
            "percentage": recycled_pct * 100,
            "volume_bbls": round(total_water_bbls * recycled_pct),
            "permits_required": ["RRC Rule 46 notification"],
            "estimated_cost_per_bbl": 0.75,
        })
        sources_recommended.append({
            "source": "brackish_groundwater",
            "percentage": brackish_pct * 100,
            "volume_bbls": round(total_water_bbls * brackish_pct),
            "permits_required": ["GCD permit (may be required)", "Concentrate disposal permit"],
            "estimated_cost_per_bbl": 1.05,
        })
        total_estimated_cost = sum(s["volume_bbls"] * s["estimated_cost_per_bbl"] for s in sources_recommended)
        drought_assessment = self._drought.assess_drought_risk(county, "groundwater", total_water_af)
        infrastructure: list[str] = [
            f"Freshwater storage: {int(daily_peak_bbls * 3):,} bbls (3-day buffer)",
            "Transfer pumps and temporary waterlines to well sites",
            "Metering equipment for GCD compliance",
            "Recycling facility or contract with recycling service provider",
        ]
        if total_water_bbls > 1000000:
            infrastructure.append("Dedicated water pipeline from source to central storage")
        return {
            "county": county,
            "wells_planned": wells_planned,
            "avg_water_per_well_bbls": avg_water_per_well_bbls,
            "total_water_bbls": total_water_bbls,
            "total_water_af": round(total_water_af, 1),
            "total_water_gallons": round(total_water_bbls * 42),
            "completion_schedule_months": completion_schedule_months,
            "monthly_rate_bbls": round(monthly_rate_bbls),
            "daily_peak_bbls": round(daily_peak_bbls),
            "sources": sources_recommended,
            "total_estimated_cost_usd": round(total_estimated_cost, 2),
            "cost_per_well_usd": round(total_estimated_cost / max(wells_planned, 1), 2),
            "infrastructure_requirements": infrastructure,
            "drought_assessment": drought_assessment,
            "regulatory_checklist": [
                "Obtain GCD production permit for freshwater wells",
                "File RRC Rule 46 notification for recycling operations",
                "Negotiate water supply agreements with backup provisions",
                "Register all water wells with GCD",
                "Install and calibrate metering equipment",
                "Submit water management plan to GCD (if required)",
            ],
        }


class ProducedWaterForecastEngine:
    """Forecast produced water volumes and plan disposal capacity."""

    def forecast_production(self, wells: list[dict[str, Any]]) -> dict[str, Any]:
        """Forecast produced water volumes from well production data."""
        total_daily_bbls = 0.0
        well_forecasts: list[dict[str, Any]] = []
        for well in wells:
            oil_bbls_day = well.get("oil_bbls_day", 0)
            wor = well.get("water_oil_ratio", 3.0)
            water_bbls_day = oil_bbls_day * wor
            well_age_months = well.get("age_months", 0)
            decline_factor = 1.0 + (well_age_months / 24.0) * 0.5
            projected_wor_12mo = wor * decline_factor
            projected_water_12mo = oil_bbls_day * projected_wor_12mo * 0.85
            total_daily_bbls += water_bbls_day
            well_forecasts.append({
                "well_id": well.get("well_id", "unknown"),
                "current_water_bbls_day": round(water_bbls_day, 1),
                "current_wor": wor,
                "projected_wor_12mo": round(projected_wor_12mo, 1),
                "projected_water_12mo_bbls_day": round(projected_water_12mo, 1),
            })
        total_monthly = total_daily_bbls * 30
        total_annual = total_daily_bbls * 365
        disposal_capacity_needed = total_daily_bbls * 1.2
        return {
            "well_count": len(wells),
            "total_current_water_bbls_day": round(total_daily_bbls, 1),
            "total_monthly_bbls": round(total_monthly),
            "total_annual_bbls": round(total_annual),
            "disposal_capacity_needed_bbls_day": round(disposal_capacity_needed),
            "well_forecasts": well_forecasts,
            "recommendations": [
                f"Secure disposal capacity for {disposal_capacity_needed:,.0f} bbls/day (includes 20% buffer)",
                "Consider recycling to reduce disposal volume by 20-40%",
                "Monitor WOR trends monthly for early warning of water breakthrough",
            ],
        }

    def evaluate_recycling_economics(self, daily_volume_bbls: float,
                                      disposal_cost_per_bbl: float,
                                      freshwater_cost_per_bbl: float) -> dict[str, Any]:
        """Evaluate economics of produced water recycling vs disposal + freshwater purchase."""
        recycling_capex_per_bbl_capacity = 15.0
        recycling_opex_per_bbl = 0.60
        recycling_recovery_rate = 0.80
        recycled_volume = daily_volume_bbls * recycling_recovery_rate
        concentrate_volume = daily_volume_bbls * (1 - recycling_recovery_rate)
        without_recycling_daily = (daily_volume_bbls * disposal_cost_per_bbl) + (recycled_volume * freshwater_cost_per_bbl)
        with_recycling_daily = (daily_volume_bbls * recycling_opex_per_bbl) + (concentrate_volume * disposal_cost_per_bbl)
        daily_savings = without_recycling_daily - with_recycling_daily
        annual_savings = daily_savings * 365
        capex = daily_volume_bbls * recycling_capex_per_bbl_capacity
        payback_years = capex / annual_savings if annual_savings > 0 else float("inf")
        economically_favorable = payback_years < 3.0
        return {
            "daily_volume_bbls": daily_volume_bbls,
            "disposal_cost_per_bbl": disposal_cost_per_bbl,
            "freshwater_cost_per_bbl": freshwater_cost_per_bbl,
            "without_recycling": {
                "daily_cost_usd": round(without_recycling_daily, 2),
                "annual_cost_usd": round(without_recycling_daily * 365, 2),
            },
            "with_recycling": {
                "daily_cost_usd": round(with_recycling_daily, 2),
                "annual_cost_usd": round(with_recycling_daily * 365, 2),
                "recycled_volume_bbls_day": round(recycled_volume, 1),
                "concentrate_volume_bbls_day": round(concentrate_volume, 1),
                "capex_usd": round(capex, 2),
            },
            "savings": {
                "daily_savings_usd": round(daily_savings, 2),
                "annual_savings_usd": round(annual_savings, 2),
                "payback_years": round(payback_years, 1) if payback_years != float("inf") else "never",
            },
            "economically_favorable": economically_favorable,
            "recommendation": "Recycling is economically favorable" if economically_favorable else "Recycling is not yet economic at current prices",
        }


# ---------------------------------------------------------------------------
# Main Engine Class
# ---------------------------------------------------------------------------

class WaterRightsEngine:
    """
    LM15 Water Rights Engine - All 20 TIE components.

    C01: Doctrine Cache
    C02: Semantic Dictionary
    C03: Search Index
    C04: Telemetry
    C05: Pydantic Models
    C06: Determinism Hash (SHA-256)
    C07: Health Endpoint
    C08: Config Loader
    C09: Risk Scoring
    C10: Compliance Checker
    C11: Audit Trail
    C12: Drift Watcher
    C13: Coverage Map
    C14: Integrity Verifier
    C15: Response Modes
    C16: Error Handler
    C17: Async Operations
    C18: Logging (loguru structured)
    C19: Export Formats
    C20: Version Tracker
    """

    def __init__(self) -> None:
        logger.info(f"Initializing {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
        # C08: Config Loader
        self.config = self._load_config()
        # C01: Doctrine Cache
        self.doctrine_cache = build_doctrine_cache()
        # C02: Semantic Dictionary
        self.semantic_dict = WaterRightsSemanticDictionary()
        # C03: Search Index
        self.search_index = DoctrineSearchIndex()
        self.search_index.index_doctrine_cache(self.doctrine_cache)
        self.searcher = WaterRightsSearcher()
        self.searcher.index_doctrines(self.doctrine_cache)
        # C04: Telemetry
        self.telemetry = WaterRightsTelemetry(ENGINE_ID, ENGINE_VERSION)
        # C12: Drift Watcher
        self.telemetry.set_doctrine_baseline(self.doctrine_cache)
        # Core analyzers
        self.classifier = WaterRightClassifier()
        self.gw_analyzer = GroundwaterAnalyzer()
        self.sw_analyzer = SurfaceWaterAnalyzer()
        self.pw_manager = ProducedWaterManager()
        self.disposal_analyzer = DisposalWellComplianceAnalyzer()
        self.aquifer_engine = AquiferAnalysisEngine()
        self.conveyance_tracker = WaterConveyanceTracker()
        self.accommodation_evaluator = AccommodationDoctrineEvaluator()
        self.freshwater_checker = FreshwaterProtectionChecker()
        # Additional analyzers
        self.seismicity_evaluator = SeismicityRiskEvaluator()
        self.compact_analyzer = InterstateCompactAnalyzer()
        self.economics_calculator = WaterEconomicsCalculator()
        self.drought_analyzer = DroughtContingencyAnalyzer()
        self.supply_planner = WaterSupplyPlanningEngine()
        self.forecast_engine = ProducedWaterForecastEngine()
        # Trackers
        self.permit_tracker = WaterPermitTracker()
        self.aquifer_searcher = AquiferDataSearcher()
        logger.info(
            f"{ENGINE_NAME} initialized: {len(self.doctrine_cache)} doctrines, "
            f"{self.semantic_dict.term_count} semantic terms, "
            f"{self.search_index.document_count} indexed documents"
        )

    def _load_config(self) -> dict[str, Any]:
        """C08: Load engine configuration from config.json."""
        if CONFIG_PATH.exists():
            config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            logger.info(f"Config loaded from {CONFIG_PATH}")
            return config
        logger.warning(f"Config not found at {CONFIG_PATH}, using defaults")
        return {"engine_id": ENGINE_ID, "engine_name": ENGINE_NAME, "version": ENGINE_VERSION, "port": ENGINE_PORT}

    async def analyze_water_right(self, query: WaterRightQuery) -> WaterRightAnalysisResult:
        """C15/C17: Main analysis endpoint with response modes and async."""
        start = time.monotonic()
        analysis_id = f"WR-{uuid.uuid4().hex[:12]}"
        logger.info(f"Analysis {analysis_id}: mode={query.mode.value}, query='{query.query_text[:80]}'")
        try:
            # C09: Classification and risk scoring
            classification = self.classifier.classify(query.tds_mg_l, query.water_source, query.use_type)
            # C01: Doctrine search
            max_docs = query.max_doctrines
            mode_config = self.config.get("response_modes", {}).get(query.mode.value, {})
            if mode_config:
                max_docs = mode_config.get("max_doctrines", max_docs)
            matched_doctrines = search_doctrines(self.doctrine_cache, query.query_text, max_results=max_docs)
            doctrine_dicts: list[dict[str, Any]] = []
            citations: list[str] = []
            for d in matched_doctrines:
                doc_dict: dict[str, Any] = {
                    "doctrine_id": d.doctrine_id,
                    "title": d.title,
                    "category": d.category.value,
                    "citation": d.citation,
                    "risk_if_violated": d.risk_if_violated.value,
                }
                if query.mode != ResponseMode.FAST:
                    doc_dict["summary"] = d.summary
                    doc_dict["key_provisions"] = d.key_provisions
                    doc_dict["permian_basin_notes"] = d.permian_basin_notes
                if query.mode == ResponseMode.MEMO:
                    doc_dict["detailed_analysis"] = d.detailed_analysis
                    doc_dict["exceptions"] = d.exceptions
                    doc_dict["related_doctrines"] = d.related_doctrines
                doctrine_dicts.append(doc_dict)
                if query.include_citations:
                    citations.append(d.citation)
            # Regulatory framework
            reg_framework: dict[str, Any] = {"agencies": []}
            if classification.get("classification") in ("fresh_groundwater", "brackish_groundwater"):
                reg_framework["agencies"].append({"name": "GCD", "role": "Groundwater production permitting"})
                reg_framework["primary_law"] = "TWC Chapter 36"
            if classification.get("classification") == "surface_water":
                reg_framework["agencies"].append({"name": "TCEQ", "role": "Surface water appropriation permitting"})
                reg_framework["primary_law"] = "TWC Chapter 11"
            if classification.get("classification") in ("produced_water", "flowback_water"):
                reg_framework["agencies"].append({"name": "RRC", "role": "Produced water disposal/recycling"})
                reg_framework["primary_law"] = "TNRC Chapter 91; 16 TAC Chapter 3"
            reg_framework["agencies"].append({"name": "EPA", "role": "UIC oversight, SDWA enforcement"})
            # C10: GCD compliance
            gcd_analysis = None
            if query.county and query.gpm:
                gcd_analysis = self.gw_analyzer.analyze_gcd_compliance(query.county, query.gpm, query.use_type)
            # Compliance notes
            compliance_notes: list[str] = []
            for permit in classification.get("permits_needed", []):
                compliance_notes.append(f"Permit required: {permit}")
            if classification.get("is_usdw_source"):
                compliance_notes.append("Water source is a USDW - protection requirements apply to nearby injection wells")
            # Recommendations
            recommendations: list[str] = []
            if query.include_recommendations:
                risk = classification.get("risk_level", "low")
                if risk in ("high", "critical"):
                    recommendations.append("Engage environmental counsel before proceeding")
                if gcd_analysis and gcd_analysis.get("permit_analysis", {}).get("permit_required"):
                    recommendations.append(f"Obtain GCD production permit before commencing pumping in {query.county} County")
                if classification.get("classification") == "produced_water":
                    recommendations.append("Evaluate recycling feasibility to reduce disposal costs and freshwater demand")
            # C09: Risk assessment
            overall_risk = classification.get("risk_level", "low")
            if matched_doctrines:
                critical_count = sum(1 for d in matched_doctrines if d.risk_if_violated == RiskLevel.CRITICAL)
                if critical_count >= 2:
                    overall_risk = "critical"
                elif critical_count >= 1:
                    overall_risk = "high"
            # Permit requirements
            permit_reqs: list[dict[str, Any]] = []
            for permit in classification.get("permits_needed", []):
                permit_reqs.append({"permit_type": permit, "agency": "See regulatory framework", "status": "required"})
            elapsed = (time.monotonic() - start) * 1000
            # C06: Determinism hash
            result = WaterRightAnalysisResult(
                analysis_id=analysis_id,
                query_text=query.query_text,
                classification=classification.get("classification", "unknown"),
                risk_level=overall_risk,
                applicable_doctrines=doctrine_dicts,
                regulatory_framework=reg_framework,
                compliance_notes=compliance_notes,
                recommendations=recommendations,
                citations=list(set(citations)),
                gcd_analysis=gcd_analysis,
                permit_requirements=permit_reqs,
                aquifer_data=self.aquifer_searcher.get_aquifer(query.aquifer) if query.aquifer else None,
                confidence=0.95 if matched_doctrines else 0.7,
                execution_time_ms=round(elapsed, 2),
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
            result.compute_hash()
            # C04: Record telemetry
            self.telemetry.record_operation(
                OperationType.WATER_RIGHT_ANALYSIS, elapsed, True,
                metadata={"mode": query.mode.value, "doctrines_matched": len(matched_doctrines)},
            )
            # C11: Audit trail
            self.telemetry.log_audit(
                AuditAction.ANALYSIS_COMPLETED, "engine", "water_right_analysis", analysis_id,
                {"query": query.query_text[:100], "mode": query.mode.value, "risk": overall_risk},
            )
            logger.info(f"Analysis {analysis_id} complete: {len(matched_doctrines)} doctrines, risk={overall_risk}, {elapsed:.1f}ms")
            return result
        except Exception as exc:
            elapsed = (time.monotonic() - start) * 1000
            self.telemetry.record_operation(
                OperationType.WATER_RIGHT_ANALYSIS, elapsed, False,
                error_message=str(exc),
            )
            logger.error(f"Analysis {analysis_id} failed: {exc}")
            raise

    async def analyze_disposal_well(self, query: DisposalWellQuery) -> DisposalWellComplianceResult:
        """Disposal well compliance analysis."""
        start = time.monotonic()
        result = self.disposal_analyzer.analyze(query)
        elapsed = (time.monotonic() - start) * 1000
        self.telemetry.record_operation(OperationType.INJECTION_WELL_CHECK, elapsed, True)
        return result

    async def analyze_aquifer(self, query: AquiferQuery) -> AquiferAnalysisResult:
        """Aquifer analysis and depletion assessment."""
        start = time.monotonic()
        result = self.aquifer_engine.analyze(query)
        elapsed = (time.monotonic() - start) * 1000
        self.telemetry.record_operation(OperationType.AQUIFER_SEARCH, elapsed, True)
        return result

    async def analyze_conveyance(self, query: ConveyanceQuery) -> ConveyanceAnalysisResult:
        """Water rights conveyance analysis."""
        start = time.monotonic()
        result = self.conveyance_tracker.analyze_conveyance(query)
        elapsed = (time.monotonic() - start) * 1000
        self.telemetry.record_operation(OperationType.CONVEYANCE_ANALYSIS, elapsed, True)
        return result

    async def evaluate_accommodation(self, query: AccommodationQuery) -> dict[str, Any]:
        """Accommodation doctrine evaluation."""
        start = time.monotonic()
        result = self.accommodation_evaluator.evaluate(query)
        elapsed = (time.monotonic() - start) * 1000
        self.telemetry.record_operation(OperationType.SURFACE_USE_ANALYSIS, elapsed, True)
        return result

    async def check_freshwater_protection(self, well_data: dict[str, Any]) -> dict[str, Any]:
        """Rule 8 freshwater protection check."""
        start = time.monotonic()
        result = self.freshwater_checker.check_rule_8_compliance(well_data)
        elapsed = (time.monotonic() - start) * 1000
        self.telemetry.record_operation(OperationType.FRESHWATER_IDENTIFICATION, elapsed, True)
        return result

    async def search(self, query: SearchQuery) -> SearchResponse:
        """C03: Full-text search across doctrines and records."""
        start = time.monotonic()
        response = self.searcher.search(query)
        elapsed = (time.monotonic() - start) * 1000
        self.telemetry.record_operation(OperationType.DOCTRINE_LOOKUP, elapsed, True)
        return response

    def lookup_term(self, term: str) -> Optional[SemanticTerm]:
        """C02: Semantic term lookup."""
        return self.semantic_dict.lookup(term)

    def search_terms(self, query: str, max_results: int = 10) -> list[SemanticTerm]:
        """C02: Semantic term search."""
        return self.semantic_dict.search(query, max_results)

    def extract_terms(self, text: str) -> list[SemanticTerm]:
        """C02: Extract recognized terms from text."""
        return self.semantic_dict.extract_terms_from_text(text)

    def get_health(self) -> HealthResponse:
        """C07: Health endpoint."""
        health = self.telemetry.get_health()
        return HealthResponse(
            status=health.status,
            uptime_seconds=health.uptime_seconds,
            doctrine_count=len(self.doctrine_cache),
            semantic_term_count=self.semantic_dict.term_count,
            total_operations=health.total_operations,
            error_rate=health.error_rate,
            avg_latency_ms=health.avg_latency_ms,
            drift_events_24h=health.drift_events_24h,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def get_coverage_map(self) -> dict[str, Any]:
        """C13: Doctrine coverage map."""
        return get_coverage_map(self.doctrine_cache)

    def verify_integrity(self) -> dict[str, Any]:
        """C14: Doctrine integrity verification."""
        return verify_doctrine_integrity(self.doctrine_cache)

    def check_drift(self) -> list[Any]:
        """C12: Check for doctrine drift."""
        return self.telemetry.check_doctrine_drift(self.doctrine_cache)

    def export_telemetry(self) -> dict[str, Any]:
        """C19: Export telemetry data."""
        return self.telemetry.export_telemetry()

    async def evaluate_seismicity(self, county: str, daily_volume_bbls: float,
                                    injection_depth_ft: float,
                                    nearby_magnitude: Optional[float] = None) -> dict[str, Any]:
        """Seismicity risk evaluation."""
        start = time.monotonic()
        result = self.seismicity_evaluator.evaluate(county, daily_volume_bbls, injection_depth_ft, nearby_magnitude)
        elapsed = (time.monotonic() - start) * 1000
        self.telemetry.record_operation(OperationType.SEISMICITY_REVIEW, elapsed, True)
        return result

    async def check_interstate_compact(self, county: str, water_use: str,
                                        volume_af: float) -> dict[str, Any]:
        """Interstate compact check."""
        start = time.monotonic()
        pecos = self.compact_analyzer.check_pecos_compact(water_use, volume_af, county)
        rio_grande = self.compact_analyzer.check_rio_grande_compact(county)
        elapsed = (time.monotonic() - start) * 1000
        self.telemetry.record_operation(OperationType.TRANSPORT_ANALYSIS, elapsed, True)
        return {
            "county": county,
            "pecos_river_compact": pecos,
            "rio_grande_compact": rio_grande,
        }

    async def calculate_water_cost(self, volume_bbls: float, source: str,
                                    transport_miles: float, county: str) -> dict[str, Any]:
        """Water cost calculation."""
        return self.economics_calculator.calculate_frack_water_cost(volume_bbls, source, transport_miles, county)

    async def compare_sources(self, volume_bbls: float, transport_miles: float,
                               county: str) -> dict[str, Any]:
        """Compare water source costs."""
        return self.economics_calculator.compare_water_sources(volume_bbls, transport_miles, county)

    async def assess_drought_risk(self, county: str, water_source: str,
                                   volume_af: float) -> dict[str, Any]:
        """Drought risk assessment."""
        return self.drought_analyzer.assess_drought_risk(county, water_source, volume_af)

    async def create_supply_plan(self, county: str, wells_planned: int,
                                  avg_water_per_well_bbls: float,
                                  schedule_months: int) -> dict[str, Any]:
        """Create water supply plan."""
        return self.supply_planner.create_supply_plan(county, wells_planned, avg_water_per_well_bbls, schedule_months)

    async def forecast_produced_water(self, wells: list[dict[str, Any]]) -> dict[str, Any]:
        """Forecast produced water volumes."""
        return self.forecast_engine.forecast_production(wells)

    async def evaluate_recycling_economics(self, daily_volume: float,
                                            disposal_cost: float,
                                            freshwater_cost: float) -> dict[str, Any]:
        """Evaluate recycling economics."""
        return self.forecast_engine.evaluate_recycling_economics(daily_volume, disposal_cost, freshwater_cost)

    async def check_usdw_risk(self, injection_depth_ft: float, usdw_base_ft: float,
                               confining_thickness_ft: float) -> dict[str, Any]:
        """USDW risk assessment."""
        return self.freshwater_checker.assess_usdw_risk(injection_depth_ft, usdw_base_ft, confining_thickness_ft)

    async def check_spill_reporting(self, volume_bbls: float, substance: str,
                                     reached_water: bool) -> dict[str, Any]:
        """Spill reporting requirements check."""
        return self.freshwater_checker.evaluate_spill_reporting(volume_bbls, substance, reached_water)

    def get_version_info(self) -> dict[str, Any]:
        """C20: Version tracking."""
        return {
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "mode": ENGINE_MODE,
            "port": ENGINE_PORT,
            "tier": ENGINE_TIER,
            "authority": ENGINE_AUTHORITY,
            "tie_components": 20,
            "doctrine_count": len(self.doctrine_cache),
            "semantic_terms": self.semantic_dict.term_count,
            "search_documents": self.search_index.document_count,
        }


# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------

def create_app() -> Any:
    """Create and configure the FastAPI application."""
    try:
        from fastapi import FastAPI, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
    except ImportError:
        logger.error("FastAPI not installed. Install with: pip install fastapi uvicorn")
        raise

    engine: Optional[WaterRightsEngine] = None

    @asynccontextmanager
    async def lifespan(app: Any) -> Any:
        nonlocal engine
        engine = WaterRightsEngine()
        logger.info(f"{ENGINE_NAME} v{ENGINE_VERSION} started on port {ENGINE_PORT}")
        yield
        if engine:
            engine.telemetry.shutdown()
        logger.info(f"{ENGINE_NAME} shutdown complete")

    app = FastAPI(
        title=ENGINE_NAME,
        version=ENGINE_VERSION,
        description=f"LM15 Water Rights Engine - Texas water law analysis (Port {ENGINE_PORT})",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def _get_engine() -> WaterRightsEngine:
        if engine is None:
            raise HTTPException(status_code=503, detail="Engine not initialized")
        return engine

    @app.get("/health")
    async def health() -> dict[str, Any]:
        eng = _get_engine()
        h = eng.get_health()
        return h.model_dump()

    @app.get("/version")
    async def version() -> dict[str, Any]:
        eng = _get_engine()
        return eng.get_version_info()

    @app.post("/api/v1/analyze")
    async def analyze_water_right(query: WaterRightQuery) -> dict[str, Any]:
        eng = _get_engine()
        result = await eng.analyze_water_right(query)
        return result.model_dump()

    @app.post("/api/v1/disposal/compliance")
    async def analyze_disposal_well(query: DisposalWellQuery) -> dict[str, Any]:
        eng = _get_engine()
        result = await eng.analyze_disposal_well(query)
        return result.model_dump()

    @app.post("/api/v1/aquifer/analyze")
    async def analyze_aquifer(query: AquiferQuery) -> dict[str, Any]:
        eng = _get_engine()
        result = await eng.analyze_aquifer(query)
        return result.model_dump()

    @app.post("/api/v1/conveyance/analyze")
    async def analyze_conveyance(query: ConveyanceQuery) -> dict[str, Any]:
        eng = _get_engine()
        result = await eng.analyze_conveyance(query)
        return result.model_dump()

    @app.post("/api/v1/accommodation/evaluate")
    async def evaluate_accommodation(query: AccommodationQuery) -> dict[str, Any]:
        eng = _get_engine()
        return await eng.evaluate_accommodation(query)

    @app.post("/api/v1/freshwater/check")
    async def check_freshwater(well_data: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return await eng.check_freshwater_protection(well_data)

    @app.post("/api/v1/search")
    async def search_doctrines_endpoint(query: SearchQuery) -> dict[str, Any]:
        eng = _get_engine()
        response = await eng.search(query)
        return {
            "query_hash": response.query_hash,
            "total_results": response.total_results,
            "returned": response.returned,
            "results": [
                {
                    "result_id": r.result_id,
                    "score": r.score,
                    "title": r.title,
                    "summary": r.summary,
                    "citation": r.citation,
                    "record_type": r.record_type,
                }
                for r in response.results
            ],
            "facets": response.facets,
            "execution_time_ms": response.execution_time_ms,
        }

    @app.get("/api/v1/term/{term}")
    async def lookup_term(term: str) -> dict[str, Any]:
        eng = _get_engine()
        result = eng.lookup_term(term)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Term '{term}' not found")
        return {
            "term": result.term,
            "category": result.category.value,
            "definition": result.definition,
            "abbreviation": result.abbreviation,
            "synonyms": result.synonyms,
            "related_terms": result.related_terms,
            "context_notes": result.context_notes,
            "regulatory_reference": result.regulatory_reference,
        }

    @app.get("/api/v1/terms/search")
    async def search_terms(q: str, max_results: int = 10) -> dict[str, Any]:
        eng = _get_engine()
        terms = eng.search_terms(q, max_results)
        return {
            "query": q,
            "count": len(terms),
            "terms": [
                {"term": t.term, "category": t.category.value, "definition": t.definition[:200]}
                for t in terms
            ],
        }

    @app.post("/api/v1/terms/extract")
    async def extract_terms(body: dict[str, str]) -> dict[str, Any]:
        eng = _get_engine()
        text = body.get("text", "")
        terms = eng.extract_terms(text)
        return {
            "text_length": len(text),
            "terms_found": len(terms),
            "terms": [
                {"term": t.term, "category": t.category.value, "definition": t.definition[:150]}
                for t in terms
            ],
        }

    @app.get("/api/v1/coverage")
    async def coverage_map() -> dict[str, Any]:
        eng = _get_engine()
        return eng.get_coverage_map()

    @app.get("/api/v1/integrity")
    async def integrity_check() -> dict[str, Any]:
        eng = _get_engine()
        return eng.verify_integrity()

    @app.get("/api/v1/drift")
    async def drift_check() -> dict[str, Any]:
        eng = _get_engine()
        events = eng.check_drift()
        return {
            "drift_events": len(events),
            "events": [
                {"drift_id": e.drift_id, "doctrine_id": e.doctrine_id, "severity": e.severity.value}
                for e in events
            ],
        }

    @app.get("/api/v1/telemetry")
    async def telemetry_export() -> dict[str, Any]:
        eng = _get_engine()
        return eng.export_telemetry()

    @app.get("/api/v1/aquifer/{name}")
    async def get_aquifer(name: str) -> dict[str, Any]:
        eng = _get_engine()
        data = eng.aquifer_searcher.get_aquifer(name)
        if not data:
            raise HTTPException(status_code=404, detail=f"Aquifer '{name}' not found")
        return data

    @app.get("/api/v1/aquifers/permian")
    async def get_permian_aquifers() -> dict[str, Any]:
        eng = _get_engine()
        aquifers = eng.aquifer_searcher.get_permian_aquifers()
        return {"count": len(aquifers), "aquifers": aquifers}

    @app.get("/api/v1/permits/expiring")
    async def get_expiring_permits(days: int = 90) -> dict[str, Any]:
        eng = _get_engine()
        permits = eng.permit_tracker.get_expiring_permits(days)
        return {"count": len(permits), "permits": permits}

    @app.get("/api/v1/depletion/summary")
    async def depletion_summary() -> dict[str, Any]:
        eng = _get_engine()
        return eng.aquifer_searcher.get_depletion_summary()

    @app.post("/api/v1/seismicity/evaluate")
    async def evaluate_seismicity(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return await eng.evaluate_seismicity(
            body.get("county", ""),
            body.get("daily_volume_bbls", 0),
            body.get("injection_depth_ft", 0),
            body.get("nearby_magnitude"),
        )

    @app.post("/api/v1/compact/check")
    async def check_compact(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return await eng.check_interstate_compact(
            body.get("county", ""),
            body.get("water_use", ""),
            body.get("volume_af", 0),
        )

    @app.post("/api/v1/economics/water-cost")
    async def water_cost(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return await eng.calculate_water_cost(
            body.get("volume_bbls", 0),
            body.get("source", "freshwater"),
            body.get("transport_miles", 0),
            body.get("county", ""),
        )

    @app.post("/api/v1/economics/compare-sources")
    async def compare_sources(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return await eng.compare_sources(
            body.get("volume_bbls", 0),
            body.get("transport_miles", 0),
            body.get("county", ""),
        )

    @app.post("/api/v1/economics/disposal-cost")
    async def disposal_cost(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return eng.economics_calculator.calculate_disposal_cost(
            body.get("volume_bbls_day", 0),
            body.get("method", "swd"),
            body.get("transport_miles", 0),
        )

    @app.post("/api/v1/drought/assess")
    async def assess_drought(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return await eng.assess_drought_risk(
            body.get("county", ""),
            body.get("water_source", "groundwater"),
            body.get("volume_af", 0),
        )

    @app.post("/api/v1/supply/plan")
    async def supply_plan(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return await eng.create_supply_plan(
            body.get("county", ""),
            body.get("wells_planned", 1),
            body.get("avg_water_per_well_bbls", 400000),
            body.get("schedule_months", 12),
        )

    @app.post("/api/v1/produced-water/forecast")
    async def forecast_pw(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return await eng.forecast_produced_water(body.get("wells", []))

    @app.post("/api/v1/produced-water/recycling-economics")
    async def recycling_economics(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return await eng.evaluate_recycling_economics(
            body.get("daily_volume_bbls", 0),
            body.get("disposal_cost_per_bbl", 0.75),
            body.get("freshwater_cost_per_bbl", 0.60),
        )

    @app.post("/api/v1/usdw/risk")
    async def usdw_risk(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return await eng.check_usdw_risk(
            body.get("injection_depth_ft", 0),
            body.get("usdw_base_ft", 0),
            body.get("confining_thickness_ft", 0),
        )

    @app.post("/api/v1/spill/reporting")
    async def spill_reporting(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return await eng.check_spill_reporting(
            body.get("volume_bbls", 0),
            body.get("substance", ""),
            body.get("reached_water", False),
        )

    @app.get("/api/v1/seismicity/permit-risk/{county}")
    async def seismicity_permit_risk(county: str) -> dict[str, Any]:
        eng = _get_engine()
        return eng.seismicity_evaluator.assess_permit_risk(county)

    @app.get("/api/v1/gcd/rules/{county}")
    async def gcd_rules(county: str) -> dict[str, Any]:
        eng = _get_engine()
        result = eng.gw_analyzer.analyze_gcd_compliance(county, 100, "industrial")
        return {
            "county": county,
            "gcd_found": result["gcd_found"],
            "rules": result["applicable_gcd_rules"],
        }

    @app.post("/api/v1/rule-of-capture/evaluate")
    async def evaluate_capture(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return eng.gw_analyzer.evaluate_rule_of_capture(body)

    @app.post("/api/v1/surface-water/permit-check")
    async def sw_permit_check(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return eng.sw_analyzer.check_permit_requirements(
            body.get("use", ""),
            body.get("volume_af_year", 0),
            body.get("source", ""),
        )

    @app.post("/api/v1/surface-water/cancellation-risk")
    async def sw_cancellation(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return eng.sw_analyzer.check_cancellation_risk(body.get("last_use_date", "2020-01-01"))

    @app.post("/api/v1/freshwater/rule8-check")
    async def rule8_check(body: dict[str, Any]) -> dict[str, Any]:
        eng = _get_engine()
        return await eng.check_freshwater_protection(body)

    # -------------------------------------------------------------------
    # Batch analysis endpoints
    # -------------------------------------------------------------------

    @app.post("/api/v1/batch/analyze")
    async def batch_analyze(body: dict[str, Any]) -> dict[str, Any]:
        """Batch analysis of multiple water right queries."""
        eng = _get_engine()
        queries = body.get("queries", [])
        if not queries:
            raise HTTPException(status_code=400, detail="No queries provided")
        if len(queries) > 50:
            raise HTTPException(status_code=400, detail="Maximum 50 queries per batch")
        results: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []
        start_all = time.monotonic()
        for idx, raw_q in enumerate(queries):
            try:
                q = WaterRightQuery(**raw_q)
                result = await eng.analyze_water_right(q)
                results.append({"index": idx, "status": "success", "result": result.model_dump()})
            except Exception as exc:
                errors.append({"index": idx, "status": "error", "error": str(exc)})
                logger.warning(f"Batch query {idx} failed: {exc}")
        elapsed_all = (time.monotonic() - start_all) * 1000
        return {
            "total_queries": len(queries),
            "successful": len(results),
            "failed": len(errors),
            "results": results,
            "errors": errors,
            "total_execution_time_ms": round(elapsed_all, 2),
        }

    @app.post("/api/v1/batch/disposal-check")
    async def batch_disposal_check(body: dict[str, Any]) -> dict[str, Any]:
        """Batch compliance check for multiple disposal wells."""
        eng = _get_engine()
        wells = body.get("wells", [])
        if not wells:
            raise HTTPException(status_code=400, detail="No wells provided")
        results: list[dict[str, Any]] = []
        for idx, well_data in enumerate(wells):
            try:
                q = DisposalWellQuery(**well_data)
                result = await eng.analyze_disposal_well(q)
                results.append({"index": idx, "well_id": well_data.get("well_id", f"WELL-{idx}"),
                                "status": "success", "result": result.model_dump()})
            except Exception as exc:
                results.append({"index": idx, "well_id": well_data.get("well_id", f"WELL-{idx}"),
                                "status": "error", "error": str(exc)})
        compliant_count = sum(1 for r in results if r.get("status") == "success" and
                              r.get("result", {}).get("is_compliant", False))
        return {
            "total_wells": len(wells),
            "compliant": compliant_count,
            "non_compliant": len(wells) - compliant_count,
            "results": results,
        }

    # -------------------------------------------------------------------
    # Report generation endpoints
    # -------------------------------------------------------------------

    @app.post("/api/v1/report/water-management")
    async def water_management_report(body: dict[str, Any]) -> dict[str, Any]:
        """Generate comprehensive water management report for an operator."""
        eng = _get_engine()
        operator = body.get("operator", "Unknown Operator")
        county = body.get("county", "")
        wells = body.get("wells", [])
        water_sources = body.get("water_sources", [])
        disposal_wells = body.get("disposal_wells", [])
        start_rpt = time.monotonic()
        report_id = f"WMR-{uuid.uuid4().hex[:10]}"
        source_analysis: list[dict[str, Any]] = []
        for src in water_sources:
            classification = eng.classifier.classify(
                src.get("tds_mg_l"), src.get("source_type", ""), src.get("use_type", "")
            )
            source_analysis.append({
                "source_name": src.get("name", "unnamed"),
                "source_type": src.get("source_type", "unknown"),
                "volume_bbls_day": src.get("volume_bbls_day", 0),
                "classification": classification,
            })
        disposal_analysis: list[dict[str, Any]] = []
        for dw in disposal_wells:
            try:
                dq = DisposalWellQuery(**dw)
                result = await eng.analyze_disposal_well(dq)
                disposal_analysis.append({
                    "well_id": dw.get("well_id", "unknown"),
                    "compliant": result.is_compliant,
                    "issues": result.issues,
                })
            except Exception as exc:
                disposal_analysis.append({
                    "well_id": dw.get("well_id", "unknown"),
                    "compliant": False,
                    "issues": [f"Analysis error: {exc}"],
                })
        pw_forecast = None
        if wells:
            pw_forecast = eng.forecast_engine.forecast_production(wells)
        gcd_info = None
        if county:
            gcd_info = eng.gw_analyzer.analyze_gcd_compliance(county, 100, "industrial")
        drought_info = None
        if county:
            drought_info = eng.drought_analyzer.assess_drought_risk(county, "groundwater", 100)
        total_freshwater_bbls_day = sum(
            s.get("volume_bbls_day", 0) for s in water_sources
            if s.get("source_type", "") in ("fresh_groundwater", "surface_water", "municipal_water")
        )
        total_recycled_bbls_day = sum(
            s.get("volume_bbls_day", 0) for s in water_sources
            if s.get("source_type", "") in ("recycled_water", "treated_water")
        )
        total_water = total_freshwater_bbls_day + total_recycled_bbls_day
        recycling_rate = (total_recycled_bbls_day / total_water * 100) if total_water > 0 else 0
        recommendations: list[str] = []
        if recycling_rate < 20:
            recommendations.append(
                f"Recycling rate is {recycling_rate:.1f}%. Consider increasing recycling "
                "to reduce freshwater demand and disposal costs. Industry target is 30-40%."
            )
        if any(not d.get("compliant") for d in disposal_analysis):
            recommendations.append(
                "One or more disposal wells have compliance issues. Address immediately "
                "to avoid RRC enforcement actions."
            )
        if drought_info and drought_info.get("risk_level") in ("high", "critical"):
            recommendations.append(
                f"Drought risk in {county} County is {drought_info.get('risk_level')}. "
                "Secure backup water supply agreements and increase on-site storage."
            )
        if gcd_info and gcd_info.get("gcd_found"):
            recommendations.append(
                f"Operate within {gcd_info.get('gcd_name', 'local')} GCD rules. "
                "Ensure all production permits are current and meters are calibrated."
            )
        elapsed_rpt = (time.monotonic() - start_rpt) * 1000
        return {
            "report_id": report_id,
            "report_type": "water_management",
            "operator": operator,
            "county": county,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "water_sources": source_analysis,
            "disposal_wells": disposal_analysis,
            "produced_water_forecast": pw_forecast,
            "gcd_compliance": gcd_info,
            "drought_assessment": drought_info,
            "summary_metrics": {
                "total_freshwater_bbls_day": round(total_freshwater_bbls_day, 1),
                "total_recycled_bbls_day": round(total_recycled_bbls_day, 1),
                "recycling_rate_pct": round(recycling_rate, 1),
                "disposal_wells_compliant": sum(1 for d in disposal_analysis if d.get("compliant")),
                "disposal_wells_total": len(disposal_analysis),
            },
            "recommendations": recommendations,
            "execution_time_ms": round(elapsed_rpt, 2),
        }

    @app.post("/api/v1/report/regulatory-summary")
    async def regulatory_summary_report(body: dict[str, Any]) -> dict[str, Any]:
        """Generate regulatory summary for a county or set of operations."""
        eng = _get_engine()
        county = body.get("county", "")
        operations = body.get("operations", [])
        report_id = f"RSR-{uuid.uuid4().hex[:10]}"
        applicable_regulations: list[dict[str, Any]] = []
        categories_seen: set[str] = set()
        for op in operations:
            op_type = op.get("type", "")
            if op_type in ("groundwater_pumping", "well_drilling") and "groundwater" not in categories_seen:
                categories_seen.add("groundwater")
                applicable_regulations.append({
                    "category": "Groundwater",
                    "primary_authority": "GCD (if established) + TWC Chapter 36",
                    "key_requirements": [
                        "Production permit from local GCD",
                        "Well registration with TWDB (if GCD not established)",
                        "Metering and reporting per GCD rules",
                        "Compliance with DFC (Desired Future Conditions)",
                    ],
                    "risk_level": "medium",
                })
            if op_type in ("surface_water_diversion",) and "surface_water" not in categories_seen:
                categories_seen.add("surface_water")
                applicable_regulations.append({
                    "category": "Surface Water",
                    "primary_authority": "TCEQ + TWC Chapter 11",
                    "key_requirements": [
                        "Appropriation permit from TCEQ (unless exempt)",
                        "Environmental flow standards compliance",
                        "Beneficial use requirement",
                        "Return flow obligations",
                    ],
                    "risk_level": "high",
                })
            if op_type in ("saltwater_disposal", "injection_well", "swd") and "disposal" not in categories_seen:
                categories_seen.add("disposal")
                applicable_regulations.append({
                    "category": "Saltwater Disposal",
                    "primary_authority": "RRC + 16 TAC Chapter 3 + UIC Class II",
                    "key_requirements": [
                        "W-14 injection permit from RRC",
                        "Mechanical integrity test (MIT) every 5 years",
                        "Monthly volume and pressure reporting (Form H-10)",
                        "Seismicity monitoring in Seismic Response Areas",
                        "USDW protection (casing and cement program)",
                    ],
                    "risk_level": "high",
                })
            if op_type in ("water_recycling", "produced_water_reuse") and "recycling" not in categories_seen:
                categories_seen.add("recycling")
                applicable_regulations.append({
                    "category": "Water Recycling",
                    "primary_authority": "RRC Rule 8 + Rule 46 + TCEQ (if surface discharge)",
                    "key_requirements": [
                        "RRC notification for recycling operations",
                        "Water quality testing before reuse",
                        "TCEQ permit if discharge to surface water",
                        "Record-keeping for recycled volumes",
                    ],
                    "risk_level": "medium",
                })
            if op_type in ("freshwater_use",) and "freshwater" not in categories_seen:
                categories_seen.add("freshwater")
                applicable_regulations.append({
                    "category": "Freshwater Protection",
                    "primary_authority": "RRC Statewide Rule 8 + SDWA",
                    "key_requirements": [
                        "Surface casing set through all usable-quality water strata",
                        "Cement returns to surface on surface casing",
                        "Freshwater sands isolation in well completions",
                        "RRC Form W-1 certification of casing program",
                    ],
                    "risk_level": "high",
                })
        seismicity_note = ""
        high_seismicity_counties = [
            "REEVES", "PECOS", "WARD", "CULBERSON", "LOVING", "MARTIN",
            "HOWARD", "STANTON", "MIDLAND",
        ]
        if county.upper() in high_seismicity_counties:
            seismicity_note = (
                f"{county} County is in an area of elevated seismic activity. "
                "RRC Seismic Response Area protocols may apply to injection wells. "
                "Enhanced monitoring and potential volume restrictions should be anticipated."
            )
        return {
            "report_id": report_id,
            "report_type": "regulatory_summary",
            "county": county,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "operations_analyzed": len(operations),
            "applicable_regulations": applicable_regulations,
            "seismicity_note": seismicity_note,
            "general_notes": [
                "All water-related permits should be obtained BEFORE commencing operations",
                "RRC and TCEQ conduct inspections; maintain compliance records on-site",
                "Penalties for non-compliance range from $1,000 to $25,000 per day per violation",
                "Environmental emergencies (spills reaching waters of the state) require immediate agency notification",
            ],
        }

    @app.post("/api/v1/report/lease-water-plan")
    async def lease_water_plan(body: dict[str, Any]) -> dict[str, Any]:
        """Generate water management plan for a specific lease."""
        eng = _get_engine()
        lease_name = body.get("lease_name", "Unknown Lease")
        county = body.get("county", "")
        section = body.get("section", "")
        block = body.get("block", "")
        survey = body.get("survey", "")
        planned_wells = body.get("planned_wells", 1)
        water_per_well_bbls = body.get("water_per_well_bbls", 400000)
        schedule_months = body.get("schedule_months", 12)
        report_id = f"LWP-{uuid.uuid4().hex[:10]}"
        total_water_needed = planned_wells * water_per_well_bbls
        supply_plan = eng.supply_planner.create_supply_plan(
            county, planned_wells, water_per_well_bbls, schedule_months
        )
        gcd_info = eng.gw_analyzer.analyze_gcd_compliance(county, 500, "oilfield") if county else None
        drought_risk = eng.drought_analyzer.assess_drought_risk(county, "groundwater", 0) if county else None
        seismicity = eng.seismicity_evaluator.evaluate(county, 5000, 8000, None) if county else None
        permit_checklist: list[dict[str, str]] = [
            {"permit": "GCD production permit", "agency": "Local GCD",
             "status": "required" if gcd_info and gcd_info.get("gcd_found") else "check_required",
             "notes": "Apply before drilling water supply wells"},
            {"permit": "RRC W-1 drilling permit", "agency": "RRC",
             "status": "required", "notes": "Includes surface casing program for freshwater protection"},
            {"permit": "TCEQ stormwater permit", "agency": "TCEQ",
             "status": "required", "notes": "TXR150000 general permit for construction activities"},
        ]
        if any(s.get("source_type") == "surface_water" for s in body.get("water_sources", [])):
            permit_checklist.append({
                "permit": "TCEQ surface water appropriation",
                "agency": "TCEQ",
                "status": "required",
                "notes": "12-18 month process; begin application immediately",
            })
        water_budget: dict[str, Any] = {
            "total_completion_water_bbls": total_water_needed,
            "total_completion_water_af": round(total_water_needed / 325851 * 100, 2),
            "monthly_peak_demand_bbls": round(total_water_needed / max(schedule_months / 2, 1)),
            "daily_peak_demand_bbls": round(total_water_needed / max(schedule_months / 2, 1) / 30),
            "recommended_storage_bbls": round(total_water_needed / planned_wells * 1.5),
            "recommended_storage_type": "lined pit or frac tanks",
        }
        return {
            "report_id": report_id,
            "report_type": "lease_water_plan",
            "lease_name": lease_name,
            "location": {
                "county": county,
                "section": section,
                "block": block,
                "survey": survey,
            },
            "development_plan": {
                "planned_wells": planned_wells,
                "water_per_well_bbls": water_per_well_bbls,
                "schedule_months": schedule_months,
            },
            "water_budget": water_budget,
            "supply_plan": supply_plan,
            "gcd_compliance": gcd_info,
            "drought_risk": drought_risk,
            "seismicity_assessment": seismicity,
            "permit_checklist": permit_checklist,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    # -------------------------------------------------------------------
    # Data export endpoints
    # -------------------------------------------------------------------

    @app.get("/api/v1/export/doctrines")
    async def export_doctrines(format: str = "json") -> dict[str, Any]:
        """C19: Export all doctrines in specified format."""
        eng = _get_engine()
        doctrines_list: list[dict[str, Any]] = []
        for d in eng.doctrine_cache:
            doc_dict: dict[str, Any] = {
                "doctrine_id": d.doctrine_id,
                "title": d.title,
                "category": d.category.value,
                "authority_level": d.authority_level.value,
                "jurisdiction": d.jurisdiction.value,
                "citation": d.citation,
                "summary": d.summary,
                "key_provisions": d.key_provisions,
                "risk_if_violated": d.risk_if_violated.value,
                "last_updated": d.last_updated,
                "permian_basin_notes": d.permian_basin_notes,
            }
            if format == "full":
                doc_dict["detailed_analysis"] = d.detailed_analysis
                doc_dict["exceptions"] = d.exceptions
                doc_dict["related_doctrines"] = d.related_doctrines
                doc_dict["compliance_checklist"] = d.compliance_checklist
            doctrines_list.append(doc_dict)
        hash_input = json.dumps(doctrines_list, sort_keys=True)
        export_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        return {
            "export_format": format,
            "total_doctrines": len(doctrines_list),
            "export_hash": export_hash,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "doctrines": doctrines_list,
        }

    @app.get("/api/v1/export/terms")
    async def export_terms(category: str = "") -> dict[str, Any]:
        """Export semantic terms, optionally filtered by category."""
        eng = _get_engine()
        if category:
            try:
                cat = TermCategory(category)
                terms = eng.semantic_dict.get_by_category(cat)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
        else:
            terms = eng.semantic_dict.get_all_terms()
        terms_list = [
            {
                "term": t.term,
                "category": t.category.value,
                "definition": t.definition,
                "abbreviation": t.abbreviation,
                "synonyms": t.synonyms,
                "related_terms": t.related_terms,
                "regulatory_reference": t.regulatory_reference,
            }
            for t in terms
        ]
        return {
            "filter_category": category or "all",
            "total_terms": len(terms_list),
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "terms": terms_list,
        }

    @app.get("/api/v1/export/telemetry")
    async def export_telemetry_data() -> dict[str, Any]:
        """Export telemetry data for external analysis."""
        eng = _get_engine()
        return eng.export_telemetry()

    @app.get("/api/v1/export/audit-trail")
    async def export_audit_trail(limit: int = 100) -> dict[str, Any]:
        """Export recent audit trail entries."""
        eng = _get_engine()
        entries = eng.telemetry.get_recent_audits(limit)
        return {
            "total_entries": len(entries),
            "limit": limit,
            "entries": entries,
        }

    # -------------------------------------------------------------------
    # Well-level analysis endpoints
    # -------------------------------------------------------------------

    @app.post("/api/v1/well/water-source-evaluation")
    async def well_water_source_eval(body: dict[str, Any]) -> dict[str, Any]:
        """Evaluate water source options for a specific well completion."""
        eng = _get_engine()
        county = body.get("county", "")
        well_name = body.get("well_name", "")
        target_volume_bbls = body.get("target_volume_bbls", 400000)
        timeline_days = body.get("timeline_days", 30)
        daily_demand = target_volume_bbls / max(timeline_days, 1)
        source_options: list[dict[str, Any]] = []
        freshwater_cost = eng.economics_calculator.calculate_frack_water_cost(
            target_volume_bbls, "freshwater", body.get("transport_miles", 5), county
        )
        source_options.append({
            "source": "Fresh Groundwater",
            "feasibility": "high" if daily_demand < 20000 else "medium",
            "permits_needed": ["GCD production permit", "RRC W-1 (for water well)"],
            "lead_time_days": 30,
            "cost_estimate": freshwater_cost,
            "environmental_impact": "moderate - aquifer depletion concern",
            "reliability": "high (drought dependent)",
        })
        recycled_cost = eng.economics_calculator.calculate_frack_water_cost(
            target_volume_bbls, "recycled", body.get("transport_miles", 10), county
        )
        source_options.append({
            "source": "Recycled Produced Water",
            "feasibility": "medium",
            "permits_needed": ["RRC Rule 46 notification"],
            "lead_time_days": 14,
            "cost_estimate": recycled_cost,
            "environmental_impact": "low - reduces disposal and freshwater demand",
            "reliability": "depends on nearby production volume",
        })
        brackish_cost = eng.economics_calculator.calculate_frack_water_cost(
            target_volume_bbls, "brackish", body.get("transport_miles", 8), county
        )
        source_options.append({
            "source": "Brackish Groundwater (Desalinated)",
            "feasibility": "medium",
            "permits_needed": ["GCD production permit", "TCEQ concentrate disposal"],
            "lead_time_days": 60,
            "cost_estimate": brackish_cost,
            "environmental_impact": "low - does not deplete freshwater aquifer",
            "reliability": "high",
        })
        cheapest = min(source_options, key=lambda x: x["cost_estimate"].get("total_cost_usd", float("inf")))
        return {
            "well_name": well_name,
            "county": county,
            "target_volume_bbls": target_volume_bbls,
            "timeline_days": timeline_days,
            "daily_demand_bbls": round(daily_demand),
            "source_options": source_options,
            "recommended_source": cheapest["source"],
            "recommendation_basis": "lowest total cost",
            "notes": [
                "Cost estimates are approximate and depend on local conditions",
                "Lead times assume no permitting delays",
                "Consider blending sources for risk diversification",
            ],
        }

    @app.post("/api/v1/well/disposal-capacity-check")
    async def disposal_capacity_check(body: dict[str, Any]) -> dict[str, Any]:
        """Check if disposal capacity is adequate for planned production."""
        eng = _get_engine()
        projected_water_bbls_day = body.get("projected_water_bbls_day", 0)
        disposal_wells = body.get("disposal_wells", [])
        total_permitted_capacity = 0.0
        well_details: list[dict[str, Any]] = []
        for dw in disposal_wells:
            permitted = dw.get("permitted_bbls_day", 0)
            current_injection = dw.get("current_injection_bbls_day", 0)
            available = max(0, permitted - current_injection)
            total_permitted_capacity += available
            well_details.append({
                "well_id": dw.get("well_id", "unknown"),
                "permitted_bbls_day": permitted,
                "current_injection_bbls_day": current_injection,
                "available_capacity_bbls_day": round(available),
                "utilization_pct": round(current_injection / permitted * 100, 1) if permitted > 0 else 0,
            })
        buffer_factor = 1.2
        needed_with_buffer = projected_water_bbls_day * buffer_factor
        adequate = total_permitted_capacity >= needed_with_buffer
        deficit = max(0, needed_with_buffer - total_permitted_capacity)
        return {
            "projected_water_bbls_day": projected_water_bbls_day,
            "required_capacity_bbls_day": round(needed_with_buffer),
            "available_capacity_bbls_day": round(total_permitted_capacity),
            "adequate": adequate,
            "deficit_bbls_day": round(deficit) if not adequate else 0,
            "disposal_wells": well_details,
            "recommendations": [
                f"Secure additional disposal capacity of {deficit:,.0f} bbls/day" if not adequate else "Capacity is adequate with 20% buffer",
                "Monitor injection pressures for early warning of capacity constraints",
                "Consider recycling to reduce disposal demand by 20-40%",
            ] if not adequate else [
                "Current capacity is adequate with 20% safety buffer",
                "Monitor well utilization rates; plan new permits when any well exceeds 80%",
            ],
        }

    @app.post("/api/v1/well/pit-compliance")
    async def pit_compliance(body: dict[str, Any]) -> dict[str, Any]:
        """Check pit/impoundment compliance with RRC rules."""
        eng = _get_engine()
        pit_type = body.get("pit_type", "reserve_pit")
        lined = body.get("lined", False)
        contents = body.get("contents", "drilling_fluids")
        distance_to_water_ft = body.get("distance_to_water_ft", 1000)
        volume_bbls = body.get("volume_bbls", 0)
        issues: list[str] = []
        is_compliant = True
        if pit_type == "reserve_pit" and not lined:
            if contents in ("oil_based_mud", "produced_water", "oily_waste"):
                issues.append("RRC Statewide Rule 8: Reserve pits containing oil-based mud or produced water must be lined")
                is_compliant = False
        if distance_to_water_ft < 150:
            issues.append("RRC Rule 8(d)(4)(G)(ii): Pit located within 150 feet of water well, spring, or watercourse")
            is_compliant = False
        if pit_type == "saltwater_pit":
            if not lined:
                issues.append("16 TAC 3.8: Saltwater pits must have synthetic liner with leak detection")
                is_compliant = False
            if volume_bbls > 500:
                issues.append("Large saltwater pit may require RRC permit and TCEQ stormwater coverage")
        closure_deadline = ""
        if pit_type == "reserve_pit":
            closure_deadline = "Within 1 year of well completion or 1 year after last use"
        elif pit_type == "saltwater_pit":
            closure_deadline = "Per RRC permit conditions; typically within 90 days of cease operations"
        return {
            "pit_type": pit_type,
            "lined": lined,
            "contents": contents,
            "distance_to_water_ft": distance_to_water_ft,
            "volume_bbls": volume_bbls,
            "is_compliant": is_compliant,
            "issues": issues,
            "closure_deadline": closure_deadline,
            "applicable_rules": [
                "RRC Statewide Rule 8 (16 TAC 3.8)",
                "TCEQ stormwater general permit TXR150000",
                "TWC Chapter 26 (water quality)",
            ],
        }

    # -------------------------------------------------------------------
    # Permit timeline endpoints
    # -------------------------------------------------------------------

    @app.get("/api/v1/permit/timeline/{permit_type}")
    async def get_permit_timeline(permit_type: str) -> dict[str, Any]:
        """Get standard regulatory timeline for a permit type."""
        from .semantic import RegulatoryTimelineTracker
        tracker = RegulatoryTimelineTracker()
        return tracker.get_timeline(permit_type)

    @app.post("/api/v1/permit/estimate-completion")
    async def estimate_permit_completion(body: dict[str, Any]) -> dict[str, Any]:
        """Estimate permit completion date from filing date."""
        from .semantic import RegulatoryTimelineTracker
        tracker = RegulatoryTimelineTracker()
        return tracker.estimate_completion(
            body.get("permit_type", ""),
            body.get("filing_date", ""),
        )

    @app.get("/api/v1/permit/types")
    async def list_permit_types() -> dict[str, Any]:
        """List available permit timeline types."""
        from .semantic import RegulatoryTimelineTracker
        tracker = RegulatoryTimelineTracker()
        return {"permit_types": tracker.list_permit_types()}

    # -------------------------------------------------------------------
    # County-level analysis
    # -------------------------------------------------------------------

    @app.get("/api/v1/county/{county}/water-profile")
    async def county_water_profile(county: str) -> dict[str, Any]:
        """Get comprehensive water profile for a Texas county."""
        eng = _get_engine()
        gcd_info = eng.gw_analyzer.analyze_gcd_compliance(county, 100, "industrial")
        drought_info = eng.drought_analyzer.assess_drought_risk(county, "groundwater", 100)
        seismicity_info = eng.seismicity_evaluator.evaluate(county, 5000, 8000, None)
        compact_info = {
            "pecos": eng.compact_analyzer.check_pecos_compact("oilfield", 100, county),
            "rio_grande": eng.compact_analyzer.check_rio_grande_compact(county),
        }
        permian_counties = [
            "MIDLAND", "ECTOR", "MARTIN", "HOWARD", "REEVES", "PECOS",
            "WARD", "CRANE", "UPTON", "WINKLER", "ANDREWS", "LOVING",
            "GLASSCOCK", "DAWSON", "GAINES", "YOAKUM", "TERRY", "LEA",
            "CULBERSON", "JEFF_DAVIS", "BREWSTER", "PRESIDIO",
        ]
        is_permian = county.upper() in permian_counties
        primary_aquifers: list[str] = []
        if is_permian:
            primary_aquifers = ["Ogallala (north)", "Pecos Valley", "Edwards-Trinity (Plateau)",
                                "Dockum", "Rustler", "Cenozoic Alluvium"]
        water_challenges: list[str] = []
        if is_permian:
            water_challenges = [
                "High demand from oil and gas completions (400,000+ bbls per well)",
                "Limited freshwater availability; groundwater levels declining",
                "Increasing seismic activity linked to saltwater disposal",
                "Distance from surface water sources",
                "Drought vulnerability (semi-arid climate, <15 inches annual rainfall)",
                "Growing competition between agricultural and industrial water users",
            ]
        return {
            "county": county,
            "is_permian_basin": is_permian,
            "primary_aquifers": primary_aquifers,
            "gcd_information": gcd_info,
            "drought_assessment": drought_info,
            "seismicity_assessment": seismicity_info,
            "interstate_compacts": compact_info,
            "water_challenges": water_challenges,
            "key_regulatory_contacts": {
                "rrc_district": "District 08 (Midland)" if is_permian else "See RRC district map",
                "tceq_region": "Region 7 (Midland)" if is_permian else "See TCEQ regional offices",
            },
        }

    @app.get("/api/v1/county/{county}/disposal-wells")
    async def county_disposal_wells(county: str) -> dict[str, Any]:
        """Get disposal well information for a county (from config data)."""
        eng = _get_engine()
        seis = eng.seismicity_evaluator.evaluate(county, 5000, 8000, None)
        high_seismicity_counties = ["REEVES", "PECOS", "WARD", "CULBERSON", "LOVING", "MARTIN"]
        is_sra = county.upper() in high_seismicity_counties
        return {
            "county": county,
            "seismic_response_area": is_sra,
            "seismicity_assessment": seis,
            "new_permit_considerations": [
                "MIT required before initial injection",
                "Annual mechanical integrity test thereafter" if is_sra else "MIT every 5 years",
                "Seismicity monitoring plan required" if is_sra else "Standard monitoring",
                "Volume restrictions possible in SRA" if is_sra else "Standard permitted volumes",
                "Monthly H-10 reporting to RRC",
            ],
            "regulatory_contacts": {
                "rrc_uic_section": "Railroad Commission of Texas, Oil and Gas Division, UIC Section",
                "phone": "(512) 463-6792",
                "website": "https://www.rrc.texas.gov/oil-and-gas/applications-and-permits/injection-storage-permits/",
            },
        }

    # -------------------------------------------------------------------
    # Compliance monitoring endpoints
    # -------------------------------------------------------------------

    @app.post("/api/v1/compliance/monitor")
    async def compliance_monitor(body: dict[str, Any]) -> dict[str, Any]:
        """Monitor ongoing compliance status for an operator's water operations."""
        eng = _get_engine()
        operator = body.get("operator", "")
        permits = body.get("permits", [])
        wells = body.get("wells", [])
        compliance_items: list[dict[str, Any]] = []
        for permit in permits:
            permit_id = permit.get("permit_id", "")
            permit_type = permit.get("type", "")
            expiration = permit.get("expiration_date", "")
            days_until_expiry = 9999
            if expiration:
                try:
                    exp_date = datetime.strptime(expiration, "%Y-%m-%d")
                    days_until_expiry = (exp_date - datetime.now()).days
                except ValueError:
                    days_until_expiry = -1
            status = "current"
            if days_until_expiry < 0:
                status = "expired"
            elif days_until_expiry < 90:
                status = "expiring_soon"
            elif days_until_expiry < 180:
                status = "renewal_recommended"
            compliance_items.append({
                "permit_id": permit_id,
                "permit_type": permit_type,
                "expiration_date": expiration,
                "days_until_expiry": days_until_expiry if days_until_expiry != 9999 else "no_expiration",
                "status": status,
                "action_needed": status in ("expired", "expiring_soon"),
            })
        well_compliance: list[dict[str, Any]] = []
        for well in wells:
            well_id = well.get("well_id", "")
            last_mit = well.get("last_mit_date", "")
            mit_interval_years = well.get("mit_interval_years", 5)
            mit_due = "unknown"
            mit_overdue = False
            if last_mit:
                try:
                    last_mit_date = datetime.strptime(last_mit, "%Y-%m-%d")
                    from datetime import timedelta
                    next_mit = last_mit_date + timedelta(days=mit_interval_years * 365)
                    mit_due = next_mit.strftime("%Y-%m-%d")
                    mit_overdue = next_mit < datetime.now()
                except ValueError:
                    mit_due = "invalid_date"
            well_compliance.append({
                "well_id": well_id,
                "last_mit_date": last_mit,
                "next_mit_due": mit_due,
                "mit_overdue": mit_overdue,
                "h10_current": well.get("h10_current", True),
            })
        expired_count = sum(1 for c in compliance_items if c["status"] == "expired")
        expiring_count = sum(1 for c in compliance_items if c["status"] == "expiring_soon")
        overdue_mit = sum(1 for w in well_compliance if w.get("mit_overdue"))
        overall_status = "compliant"
        if expired_count > 0 or overdue_mit > 0:
            overall_status = "non_compliant"
        elif expiring_count > 0:
            overall_status = "action_needed"
        return {
            "operator": operator,
            "overall_status": overall_status,
            "monitored_at": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "permits_current": sum(1 for c in compliance_items if c["status"] == "current"),
                "permits_expiring": expiring_count,
                "permits_expired": expired_count,
                "wells_mit_current": sum(1 for w in well_compliance if not w.get("mit_overdue")),
                "wells_mit_overdue": overdue_mit,
            },
            "permits": compliance_items,
            "well_compliance": well_compliance,
            "priority_actions": [
                f"Renew {expired_count} expired permits immediately" if expired_count > 0 else None,
                f"Schedule {overdue_mit} overdue MITs" if overdue_mit > 0 else None,
                f"Begin renewal process for {expiring_count} expiring permits" if expiring_count > 0 else None,
            ],
        }

    @app.post("/api/v1/compliance/h10-check")
    async def h10_check(body: dict[str, Any]) -> dict[str, Any]:
        """Check Form H-10 monthly reporting compliance."""
        eng = _get_engine()
        well_id = body.get("well_id", "")
        injection_volume_bbls = body.get("injection_volume_bbls", 0)
        injection_pressure_psi = body.get("injection_pressure_psi", 0)
        masp_psi = body.get("masp_psi", 0)
        reporting_month = body.get("reporting_month", "")
        issues: list[str] = []
        if masp_psi > 0 and injection_pressure_psi > masp_psi:
            issues.append(
                f"Injection pressure ({injection_pressure_psi} psi) exceeds MASP ({masp_psi} psi). "
                "This is a permit violation requiring immediate pressure reduction and RRC notification."
            )
        if injection_volume_bbls <= 0:
            issues.append("Zero or negative injection volume reported. Verify meter readings.")
        max_reasonable_volume = 100000 * 30
        if injection_volume_bbls > max_reasonable_volume:
            issues.append(
                f"Reported volume ({injection_volume_bbls:,.0f} bbls) exceeds expected maximum "
                f"({max_reasonable_volume:,.0f} bbls/month). Verify meter calibration."
            )
        return {
            "well_id": well_id,
            "reporting_month": reporting_month,
            "injection_volume_bbls": injection_volume_bbls,
            "injection_pressure_psi": injection_pressure_psi,
            "masp_psi": masp_psi,
            "pressure_compliant": injection_pressure_psi <= masp_psi if masp_psi > 0 else True,
            "issues": issues,
            "filing_deadline": "Last day of the month following the reporting month",
            "form_type": "Form H-10 (Monthly Injection/Disposal Well Report)",
            "filing_method": "RRC Online System (TCEQ MIS) or paper filing",
        }

    # Cloud-enriched /query endpoint
    import sys as _sys
    _shared_dir = str(Path(__file__).resolve().parent.parent / "_shared")
    if _shared_dir not in _sys.path:
        _sys.path.insert(0, _shared_dir)
    try:
        from cloud_retriever import retrieve_cloud_knowledge
        _cloud_ok = True
    except ImportError:
        _cloud_ok = False

    @app.post("/query")
    async def cloud_query(request: dict):
        import time as _time
        start = _time.monotonic()
        q = request.get("query", "") or request.get("prompt", "")
        cloud_data = {}
        cloud_citations = []
        if _cloud_ok and request.get("include_cloud", True):
            try:
                cloud = await retrieve_cloud_knowledge(q, category="water_rights")
                cloud_data = {"records": cloud.total_records, "merged_context": cloud.merged_text(3000), "sources_succeeded": cloud.sources_succeeded, "retrieval_time_ms": cloud.retrieval_time_ms}
                cloud_citations = cloud.citation_list()
            except Exception as e:
                logger.warning(f"Cloud retrieval failed: {e}")
        elapsed = (_time.monotonic() - start) * 1000
        return {"engine_id": ENGINE_ID, "engine_name": ENGINE_NAME, "query": q, "cloud_knowledge": cloud_data, "cloud_citations": cloud_citations, "processing_time_ms": round(elapsed, 2), "cloud_available": _cloud_ok}

    return app


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Start the LM15 Water Rights Engine."""
    try:
        import uvicorn
    except ImportError:
        logger.error("uvicorn not installed. Install with: pip install uvicorn")
        raise

    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")


if __name__ == "__main__":
    main()
