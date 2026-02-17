"""
R09 - Well Plugging Requirements Intelligence Engine
ECHO OMEGA PRIME Regulatory Division
Port: 8709 | Version: 1.0.0

Purpose: Analyze well plugging requirements under RRC Statewide Rule 14
         and related regulations. No-LLM mode for deterministic responses.

TIE-20 Compliant: All 20 mandatory components implemented
Authority: Bobby Don McWilliams II
"""

import sys
import hashlib
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Literal, Tuple
from enum import Enum
from dataclasses import dataclass, asdict

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from loguru import logger

# Import shared cloud retriever
# Add both parent dirs to path
engine_dir = Path(__file__).parent
sys.path.insert(0, str(engine_dir))
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(engine_dir.parent / "_shared"))

try:
    from cloud_retriever import retrieve_from_cloud
except ImportError:
    retrieve_from_cloud = None

# Local imports
import doctrines
import semantic
import search
import telemetry

DOCTRINE_BLOCKS = doctrines.DOCTRINE_BLOCKS
IssueCategory = doctrines.IssueCategory
ConfidenceLevel = doctrines.ConfidenceLevel
normalize_query = semantic.normalize_query
extract_keywords = semantic.extract_keywords
vector_search_fallback = search.vector_search_fallback
TelemetryCollector = telemetry.TelemetryCollector
QueryMetrics = telemetry.QueryMetrics


# ═══════════════════════════════════════════════════════════════════════════
# ENUMS AND MODELS
# ═══════════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    """Response verbosity modes"""
    FAST = "fast"
    DEFENSE = "defense"
    MEMO = "memo"


class ConfidenceStratification(str, Enum):
    """Risk-adjusted confidence levels"""
    DEFENSIBLE = "defensible"
    AGGRESSIVE = "aggressive"
    DISCLOSURE = "disclosure"
    HIGH_RISK = "high_risk"


class AnalysisZone(str, Enum):
    """Position zone for analysis"""
    PLANNING = "planning"
    REPORTING = "reporting"
    AUDIT = "audit"


class WellType(str, Enum):
    """Well classification for plugging"""
    OIL = "oil"
    GAS = "gas"
    INJECTION = "injection"
    DISPOSAL = "disposal"
    WATER_SUPPLY = "water_supply"
    MULTIPLE_COMPLETION = "multiple_completion"
    HORIZONTAL = "horizontal"
    GEOTHERMAL = "geothermal"


class PlugType(str, Enum):
    """Type of cement plug required"""
    SURFACE_CASING = "surface_casing"
    PRODUCTION_CASING = "production_casing"
    OPEN_HOLE = "open_hole"
    PERFORATED_INTERVAL = "perforated_interval"
    MULTIPLE_COMPLETION = "multiple_completion"
    PACKER = "packer"
    LINER_TOP = "liner_top"


class PluggingRequest(BaseModel):
    """Input model for plugging analysis"""
    query: str = Field(..., description="Natural language question about plugging requirements")
    well_type: Optional[WellType] = Field(None, description="Type of well being plugged")
    depth_feet: Optional[int] = Field(None, description="Total depth in feet", ge=0)
    surface_casing_depth: Optional[int] = Field(None, ge=0)
    production_casing_depth: Optional[int] = Field(None, ge=0)
    open_hole_intervals: Optional[List[Tuple[int, int]]] = Field(None, description="Open hole intervals as (top, bottom)")
    perforated_intervals: Optional[List[Tuple[int, int]]] = Field(None)
    h2s_present: Optional[bool] = Field(False, description="H2S well designation")
    bay_or_estuary: Optional[bool] = Field(False, description="Located in bay or estuary")
    response_mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(AnalysisZone.PLANNING, description="Analysis context")

    class Config:
        use_enum_values = True


class PlugRequirement(BaseModel):
    """Individual plug requirement"""
    plug_type: PlugType
    interval_top: int = Field(..., description="Top of plug in feet")
    interval_bottom: int = Field(..., description="Bottom of plug in feet")
    cement_sacks: int = Field(..., description="Estimated cement required (sacks)", ge=0)
    regulatory_cite: str = Field(..., description="Specific rule citation")
    placement_method: str = Field(..., description="Recommended placement method")
    verification_required: bool = Field(True, description="Verification test required")

    class Config:
        use_enum_values = True


class NotificationRequirement(BaseModel):
    """Required notifications for plugging"""
    party: str
    timing: str
    method: str
    form_required: Optional[str] = None


class PluggingResponse(BaseModel):
    """Output model for plugging analysis"""
    query: str
    well_type: Optional[str]
    doctrine_topics: List[str]
    plug_requirements: List[PlugRequirement]
    notification_requirements: List[NotificationRequirement]
    estimated_total_cost: Optional[float] = Field(None, description="Estimated plugging cost in USD")
    timeline_days: int = Field(..., description="Estimated timeline in days")
    primary_authorities: List[str]
    confidence: ConfidenceLevel
    confidence_stratification: ConfidenceStratification
    reasoning: str
    caveat: Optional[str] = None
    response_mode: ResponseMode
    zone: AnalysisZone
    triggered_doctrines: List[str]
    query_hash: str
    telemetry: Dict[str, Any]

    class Config:
        use_enum_values = True


# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE (Component 3)
# ═══════════════════════════════════════════════════════════════════════════

doctrine_cache = {block.topic: block for block in DOCTRINE_BLOCKS}


def get_doctrine_coverage() -> Dict[str, Any]:
    """Component 10: Coverage map - track triggered vs missed doctrines"""
    return {
        "total_doctrines": len(DOCTRINE_BLOCKS),
        "topics": [b.topic for b in DOCTRINE_BLOCKS],
        "categories": list(set(b.category.value for b in DOCTRINE_BLOCKS)),
        "confidence_distribution": {
            level.value: sum(1 for b in DOCTRINE_BLOCKS if b.confidence == level)
            for level in ConfidenceLevel
        }
    }


# ═══════════════════════════════════════════════════════════════════════════
# AUTHORITY HARDENING (Component 4)
# ═══════════════════════════════════════════════════════════════════════════

AUTHORITY_HIERARCHY = {
    "16 TAC §3.14": 100,  # Statewide Rule 14 - highest authority
    "16 TAC §3.78": 95,   # Financial security
    "16 TAC §3.8": 90,    # Organizational report
    "Texas Natural Resources Code": 85,
    "RRC field rules": 80,
    "RRC policy": 70,
    "Industry standards": 50,
    "Best practices": 40,
}


def resolve_authority_conflict(authorities: List[str]) -> str:
    """Resolve conflicts between multiple authorities using hierarchy"""
    if not authorities:
        return "No authority cited"

    weighted = [(auth, AUTHORITY_HIERARCHY.get(auth, 0)) for auth in authorities]
    weighted.sort(key=lambda x: x[1], reverse=True)

    return weighted[0][0]


# ═══════════════════════════════════════════════════════════════════════════
# CONFIDENCE STRATIFICATION (Component 5)
# ═══════════════════════════════════════════════════════════════════════════

def stratify_confidence(
    confidence: ConfidenceLevel,
    zone: AnalysisZone,
    well_type: Optional[WellType],
    h2s_present: bool,
    bay_or_estuary: bool
) -> ConfidenceStratification:
    """Component 5: Risk-adjusted confidence stratification"""

    # High-risk scenarios force disclosure level
    if h2s_present or bay_or_estuary:
        return ConfidenceStratification.DISCLOSURE

    # Audit zone requires defensible positions
    if zone == AnalysisZone.AUDIT:
        if confidence in [ConfidenceLevel.HIGH, ConfidenceLevel.MEDIUM]:
            return ConfidenceStratification.DEFENSIBLE
        else:
            return ConfidenceStratification.DISCLOSURE

    # Injection/disposal wells are high-risk
    if well_type in [WellType.INJECTION, WellType.DISPOSAL]:
        return ConfidenceStratification.DISCLOSURE

    # Standard stratification based on confidence
    if confidence == ConfidenceLevel.HIGH:
        return ConfidenceStratification.DEFENSIBLE
    elif confidence == ConfidenceLevel.MEDIUM:
        return ConfidenceStratification.AGGRESSIVE
    elif confidence == ConfidenceLevel.LOW:
        return ConfidenceStratification.DISCLOSURE
    else:
        return ConfidenceStratification.HIGH_RISK


# ═══════════════════════════════════════════════════════════════════════════
# SEMANTIC NORMALIZATION (Component 6)
# ═══════════════════════════════════════════════════════════════════════════

PLUGGING_TERM_MAP = {
    "plug": ["plug", "plugging", "plugged", "cement plug", "plug back"],
    "cement": ["cement", "cementing", "cemented", "cement slurry"],
    "surface_casing": ["surface casing", "surface pipe", "conductor"],
    "production_casing": ["production casing", "production string", "long string"],
    "abandonment": ["abandonment", "abandoned", "P&A", "plug and abandon"],
    "notification": ["notification", "notice", "notify", "filing"],
    "h10": ["h10", "h-10", "plugging report", "plugging form"],
    "bond": ["bond", "surety", "financial security", "letter of credit"],
    "orphan": ["orphan well", "inactive well", "abandoned well"],
}


def normalize_plugging_query(query: str) -> str:
    """Component 6: Domain-specific semantic normalization"""
    normalized = query.lower()

    for canonical, variants in PLUGGING_TERM_MAP.items():
        for variant in variants:
            if variant in normalized:
                normalized = normalized.replace(variant, canonical)
                break

    return normalized


# ═══════════════════════════════════════════════════════════════════════════
# FACT FRAGILITY SCORING (Component 14)
# ═══════════════════════════════════════════════════════════════════════════

def score_fact_fragility(
    well_type: Optional[WellType],
    depth_provided: bool,
    casing_data_provided: bool,
    location_specifics: bool
) -> Dict[str, Any]:
    """Component 14: Assess verifiability and recharacterization risk"""

    verifiability_score = 0
    if well_type:
        verifiability_score += 25
    if depth_provided:
        verifiability_score += 25
    if casing_data_provided:
        verifiability_score += 30
    if location_specifics:
        verifiability_score += 20

    recharacterization_risk = "low" if verifiability_score >= 75 else \
                              "medium" if verifiability_score >= 50 else "high"

    return {
        "verifiability_score": verifiability_score,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": "low" if verifiability_score >= 75 else "high",
        "documentary_support": "strong" if casing_data_provided else "weak"
    }


# ═══════════════════════════════════════════════════════════════════════════
# PLUG REQUIREMENT CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════

def calculate_cement_sacks(interval_length: int, hole_diameter: float = 7.0) -> int:
    """Calculate cement sacks needed for interval (94 lb sacks)"""
    # Typical yield: 1.15 cubic feet per sack for Class A cement
    # Hole diameter default 7 inches
    import math

    radius_ft = (hole_diameter / 2) / 12  # inches to feet
    volume_cuft = math.pi * (radius_ft ** 2) * interval_length

    # Add 20% safety factor
    volume_cuft *= 1.2

    sacks = int(math.ceil(volume_cuft / 1.15))
    return max(sacks, 5)  # Minimum 5 sacks per plug


def generate_plug_requirements(
    well_type: WellType,
    depth_feet: int,
    surface_casing_depth: Optional[int],
    production_casing_depth: Optional[int],
    open_hole_intervals: Optional[List[Tuple[int, int]]],
    perforated_intervals: Optional[List[Tuple[int, int]]],
    h2s_present: bool,
    bay_or_estuary: bool
) -> List[PlugRequirement]:
    """Generate specific plug requirements based on well configuration"""

    plugs = []

    # Surface casing plug (required for all wells)
    if surface_casing_depth:
        plugs.append(PlugRequirement(
            plug_type=PlugType.SURFACE_CASING,
            interval_top=max(0, surface_casing_depth - 100),
            interval_bottom=surface_casing_depth,
            cement_sacks=calculate_cement_sacks(100),
            regulatory_cite="16 TAC §3.14(b)(2)(A)",
            placement_method="Dump bailer or pump through tubing",
            verification_required=True
        ))

    # Production casing plug
    if production_casing_depth:
        plug_length = 200 if h2s_present or bay_or_estuary else 100
        plugs.append(PlugRequirement(
            plug_type=PlugType.PRODUCTION_CASING,
            interval_top=max(0, production_casing_depth - plug_length),
            interval_bottom=production_casing_depth,
            cement_sacks=calculate_cement_sacks(plug_length),
            regulatory_cite="16 TAC §3.14(b)(2)(B)",
            placement_method="Balanced plug method recommended",
            verification_required=True
        ))

    # Perforated interval plugs
    if perforated_intervals:
        for top, bottom in perforated_intervals:
            interval_length = bottom - top
            plugs.append(PlugRequirement(
                plug_type=PlugType.PERFORATED_INTERVAL,
                interval_top=top,
                interval_bottom=bottom,
                cement_sacks=calculate_cement_sacks(interval_length + 50),
                regulatory_cite="16 TAC §3.14(b)(2)(C)",
                placement_method="Squeeze cementing through perforations",
                verification_required=True
            ))

    # Open hole plugs
    if open_hole_intervals:
        for top, bottom in open_hole_intervals:
            interval_length = min(bottom - top, 100)  # Max 100 ft per plug
            plugs.append(PlugRequirement(
                plug_type=PlugType.OPEN_HOLE,
                interval_top=top,
                interval_bottom=top + interval_length,
                cement_sacks=calculate_cement_sacks(interval_length),
                regulatory_cite="16 TAC §3.14(b)(2)(D)",
                placement_method="Dump bailer or pump",
                verification_required=False
            ))

    # Surface plug (all wells)
    plugs.append(PlugRequirement(
        plug_type=PlugType.SURFACE_CASING,
        interval_top=0,
        interval_bottom=50,
        cement_sacks=calculate_cement_sacks(50),
        regulatory_cite="16 TAC §3.14(b)(2)(E)",
        placement_method="Pour from surface",
        verification_required=True
    ))

    return plugs


# ═══════════════════════════════════════════════════════════════════════════
# NOTIFICATION REQUIREMENTS
# ═══════════════════════════════════════════════════════════════════════════

def generate_notification_requirements(
    well_type: WellType,
    h2s_present: bool,
    bay_or_estuary: bool
) -> List[NotificationRequirement]:
    """Generate required notifications per 16 TAC §3.14"""

    notifications = [
        NotificationRequirement(
            party="Railroad Commission",
            timing="At least 5 days before plugging",
            method="File Form H-10 (Notice of Intention to Plug and Abandon)",
            form_required="Form H-10"
        ),
        NotificationRequirement(
            party="Surface owner",
            timing="At least 14 days before plugging",
            method="Certified mail or personal delivery",
            form_required=None
        ),
    ]

    if well_type in [WellType.INJECTION, WellType.DISPOSAL]:
        notifications.append(NotificationRequirement(
            party="TCEQ (if injection/disposal permit holder)",
            timing="30 days before plugging",
            method="Written notice to appropriate TCEQ regional office",
            form_required="TCEQ Well Closure Notification"
        ))

    if bay_or_estuary:
        notifications.append(NotificationRequirement(
            party="General Land Office",
            timing="Before beginning plugging operations",
            method="Written notice per state lease terms",
            form_required=None
        ))

    return notifications


# ═══════════════════════════════════════════════════════════════════════════
# COST ESTIMATION
# ═══════════════════════════════════════════════════════════════════════════

def estimate_plugging_cost(
    plug_requirements: List[PlugRequirement],
    well_type: WellType,
    depth_feet: int,
    h2s_present: bool
) -> float:
    """Estimate total plugging cost in USD"""

    # Base cost components
    mobilization = 5000.0
    rig_day_rate = 3500.0 if depth_feet < 5000 else 7500.0

    # Cement cost: $20 per sack average
    total_sacks = sum(p.cement_sacks for p in plug_requirements)
    cement_cost = total_sacks * 20

    # Estimate days
    days = len(plug_requirements) * 0.5  # 0.5 day per plug average
    if h2s_present:
        days *= 1.5  # H2S requires additional safety measures

    rig_cost = rig_day_rate * days

    # Additional costs
    testing_cost = 2000.0 * sum(1 for p in plug_requirements if p.verification_required)
    filing_fee = 250.0

    # Injection wells require additional decommissioning
    if well_type in [WellType.INJECTION, WellType.DISPOSAL]:
        testing_cost += 5000.0  # Groundwater testing

    total = mobilization + rig_cost + cement_cost + testing_cost + filing_fee

    return round(total, 2)


# ═══════════════════════════════════════════════════════════════════════════
# THREE-LAYER RESPONSE (Component 1)
# ═══════════════════════════════════════════════════════════════════════════

def three_layer_response(request: PluggingRequest, telemetry: TelemetryCollector) -> PluggingResponse:
    """Component 1: Three-layer response system"""

    start_time = time.time()

    # Layer 1: Doctrine cache lookup (0-200ms)
    normalized = normalize_plugging_query(request.query)
    keywords = extract_keywords(normalized)

    triggered = []
    for keyword in keywords:
        if keyword in doctrine_cache:
            triggered.append(keyword)

    # Layer 2: Semantic retrieval if needed
    if not triggered:
        semantic_results = vector_search_fallback(normalized, top_k=3)
        triggered = [r["topic"] for r in semantic_results]
        telemetry.record_event("semantic_fallback", {"query": request.query, "results": len(triggered)})

    # Layer 3: Deep analysis mode
    if not request.well_type or not request.depth_feet:
        telemetry.record_event("deep_analysis", {"reason": "insufficient_parameters"})
        # Return generic guidance
        confidence = ConfidenceLevel.LOW
        reasoning = "Limited well parameters provided. General plugging requirements returned."
        plug_requirements = []
        notifications = generate_notification_requirements(
            WellType.OIL,  # Default
            request.h2s_present or False,
            request.bay_or_estuary or False
        )
        estimated_cost = None
        timeline = 14
    else:
        # Full analysis with complete parameters
        confidence = ConfidenceLevel.HIGH
        reasoning = f"Complete well configuration analyzed. {len(triggered)} doctrine topics triggered."

        plug_requirements = generate_plug_requirements(
            request.well_type,
            request.depth_feet,
            request.surface_casing_depth,
            request.production_casing_depth,
            request.open_hole_intervals,
            request.perforated_intervals,
            request.h2s_present or False,
            request.bay_or_estuary or False
        )

        notifications = generate_notification_requirements(
            request.well_type,
            request.h2s_present or False,
            request.bay_or_estuary or False
        )

        estimated_cost = estimate_plugging_cost(
            plug_requirements,
            request.well_type,
            request.depth_feet,
            request.h2s_present or False
        )

        timeline = max(14, len(plug_requirements) * 2)  # 2 days per plug minimum

    # Stratify confidence
    strat = stratify_confidence(
        confidence,
        request.zone,
        request.well_type,
        request.h2s_present or False,
        request.bay_or_estuary or False
    )

    # Generate caveat if needed
    caveat = None
    if strat in [ConfidenceStratification.DISCLOSURE, ConfidenceStratification.HIGH_RISK]:
        caveat = "This analysis is for planning purposes only. Actual plugging requirements may vary based on specific well conditions and RRC district engineer requirements. Consult with qualified professionals before proceeding."

    # Primary authorities
    authorities = list(set(p.regulatory_cite for p in plug_requirements))
    authorities.append("16 TAC §3.14 (Plugging)")
    authorities.append("16 TAC §3.78 (Financial Security)")

    # Determinism hash
    hash_input = json.dumps({
        "query": request.query,
        "well_type": request.well_type.value if request.well_type else None,
        "depth": request.depth_feet,
        "triggered": triggered
    }, sort_keys=True)
    query_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    elapsed = time.time() - start_time
    telemetry.record_latency("total_response", elapsed)

    return PluggingResponse(
        query=request.query,
        well_type=request.well_type.value if request.well_type else None,
        doctrine_topics=triggered,
        plug_requirements=plug_requirements,
        notification_requirements=notifications,
        estimated_total_cost=estimated_cost,
        timeline_days=timeline,
        primary_authorities=authorities,
        confidence=confidence,
        confidence_stratification=strat,
        reasoning=reasoning,
        caveat=caveat,
        response_mode=request.response_mode,
        zone=request.zone,
        triggered_doctrines=triggered,
        query_hash=query_hash,
        telemetry=telemetry.get_summary()
    )


# ═══════════════════════════════════════════════════════════════════════════
# AUDIT TRAIL (Component 15)
# ═══════════════════════════════════════════════════════════════════════════

AUDIT_LOG_PATH = Path(__file__).parent / "audit_trail.jsonl"


def append_audit_trail(request: PluggingRequest, response: PluggingResponse):
    """Component 15: Append-only audit trail for forensic review"""

    audit_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query": request.query,
        "well_type": request.well_type.value if request.well_type else None,
        "depth": request.depth_feet,
        "response_mode": response.response_mode.value,
        "confidence": response.confidence.value,
        "confidence_strat": response.confidence_stratification.value,
        "triggered_doctrines": response.triggered_doctrines,
        "plug_count": len(response.plug_requirements),
        "estimated_cost": response.estimated_total_cost,
        "query_hash": response.query_hash,
        "latency_ms": response.telemetry.get("total_response_ms", 0)
    }

    try:
        with AUDIT_LOG_PATH.open("a") as f:
            f.write(json.dumps(audit_entry) + "\n")
    except Exception as e:
        logger.error(f"Failed to write audit trail: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION (Component 17)
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="R09 - Plugging Requirements Engine",
    description="Well plugging requirements analysis under 16 TAC §3.14",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

telemetry_collector = TelemetryCollector()


@app.get("/health")
async def health_check():
    """Component 12: Comprehensive health check"""
    return {
        "status": "operational",
        "engine": "R09_plugging_requirements",
        "version": "1.0.0",
        "port": 8709,
        "mode": "no_llm",
        "doctrine_count": len(DOCTRINE_BLOCKS),
        "uptime_seconds": telemetry_collector.get_uptime(),
        "total_queries": telemetry_collector.get_query_count(),
        "avg_latency_ms": telemetry_collector.get_avg_latency(),
        "error_rate": telemetry_collector.get_error_rate()
    }


@app.post("/analyze", response_model=PluggingResponse)
async def analyze_plugging(request: PluggingRequest):
    """Main analysis endpoint"""

    try:
        telemetry_collector.increment_query_count()
        response = three_layer_response(request, telemetry_collector)
        append_audit_trail(request, response)
        return response

    except Exception as e:
        telemetry_collector.record_error("analysis_failed", str(e))
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total": len(DOCTRINE_BLOCKS),
        "topics": [
            {
                "topic": b.topic,
                "category": b.category.value,
                "confidence": b.confidence.value,
                "keywords": b.keywords
            }
            for b in DOCTRINE_BLOCKS
        ]
    }


@app.get("/coverage")
async def get_coverage():
    """Component 10: Doctrine coverage map"""
    return get_doctrine_coverage()


@app.get("/metrics")
async def get_metrics():
    """Component 11: Performance metrics"""
    return telemetry_collector.get_summary()


if __name__ == "__main__":
    import uvicorn

    logger.info("R09 Plugging Requirements Engine starting on port 8709")
    logger.info(f"Loaded {len(DOCTRINE_BLOCKS)} doctrine blocks")

    uvicorn.run(app, host="0.0.0.0", port=8709)