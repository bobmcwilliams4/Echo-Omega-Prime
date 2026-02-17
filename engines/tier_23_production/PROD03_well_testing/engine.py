"""
PROD03 - Well Testing & Pressure Transient Analysis Engine
TIE Gold Standard - Production Engineering Domain

Provides expert-level analysis of:
- Pressure buildup and drawdown testing
- Pressure derivative analysis (Bourdet derivative)
- Permeability and skin factor determination
- Wellbore storage and boundary effects
- Dual porosity/dual permeability models
- Rate transient analysis for unconventional wells
- Type curve matching and interpretation
- Interference and pulse testing
- Formation interval testing (MDT/RFT)
- Horizontal well test interpretation

Authority: Production engineering textbooks, SPE standards, industry best practices
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict, Counter

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from loguru import logger

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "PROD03"
ENGINE_NAME = "Well Testing & Pressure Transient Analysis Engine"
VERSION = "1.0.0"
PORT = 9033

# Configure logging
logger.add(
    f"logs/{ENGINE_ID}_{{time}}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}"
)

# ============================================================================
# ENUMS
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class IssueCategory(str, Enum):
    BUILDUP_ANALYSIS = "BUILDUP_ANALYSIS"
    DRAWDOWN_ANALYSIS = "DRAWDOWN_ANALYSIS"
    DERIVATIVE_INTERPRETATION = "DERIVATIVE_INTERPRETATION"
    SKIN_DETERMINATION = "SKIN_DETERMINATION"
    PERMEABILITY_ESTIMATION = "PERMEABILITY_ESTIMATION"
    WELLBORE_STORAGE = "WELLBORE_STORAGE"
    DUAL_POROSITY = "DUAL_POROSITY"
    BOUNDARY_DETECTION = "BOUNDARY_DETECTION"
    TYPE_CURVE_MATCHING = "TYPE_CURVE_MATCHING"
    HORIZONTAL_WELL_TESTING = "HORIZONTAL_WELL_TESTING"
    RATE_TRANSIENT_ANALYSIS = "RATE_TRANSIENT_ANALYSIS"
    INTERFERENCE_TESTING = "INTERFERENCE_TESTING"
    FORMATION_TESTING = "FORMATION_TESTING"
    MULTI_RATE_TESTING = "MULTI_RATE_TESTING"
    DST_INTERPRETATION = "DST_INTERPRETATION"

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=10, description="Well testing question or scenario")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.REPORTING, description="Analysis context zone")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")

    @field_validator('question')
    @classmethod
    def validate_question(cls, v: str) -> str:
        if len(v.strip()) < 10:
            raise ValueError("Question too short - provide detailed testing scenario")
        return v.strip()

class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    controlling_precedent: Optional[str] = None

class AnalysisResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    doctrine_blocks_triggered: List[str]
    reasoning_chain: List[str]
    key_factors: List[str]
    counter_arguments: List[str]
    epistemic_disclosure: Optional[str]
    determinism_hash: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    doctrine_count: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_response_time_ms: float

# ============================================================================
# DOCTRINE CACHE - REAL WELL TESTING EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    # Buildup Analysis
    DoctrineBlock(
        topic="horner_buildup_analysis",
        keywords=["horner", "buildup", "shut-in", "extrapolation", "p*", "average reservoir pressure"],
        conclusion_template=[
            "Horner analysis provides reliable permeability and skin estimates when middle-time region (MTR) is clearly identified.",
            "The Horner time function (tp+Δt)/Δt normalizes buildup data regardless of production history duration.",
            "Extrapolation of Horner straight line to infinite shut-in time yields p*, approximating average drainage area pressure for moderate production times."
        ],
        reasoning_framework="""
        HORNER METHOD FRAMEWORK:
        1. Plot Pws vs log[(tp+Δt)/Δt] where tp=production time, Δt=shut-in time
        2. Identify straight-line portion (MTR) - indicates infinite-acting radial flow
        3. Calculate permeability from slope m: k = 162.6 qBμ/(mh) [md]
        4. Determine skin from P1hr intercept: s = 1.151[(P1hr - Pwf)/m - log(k/φμctrw²) + 3.23]
        5. Extrapolate to p* at (tp+Δt)/Δt = 1 for average pressure estimate

        VALIDITY CONDITIONS:
        - Wellbore storage effects must have ended (derivative matches 0.5 slope before MTR)
        - Production time tp > 2-4 times shut-in time for accurate p*
        - No boundary effects during MTR (derivative plateau, no upward bend)
        - Single-phase flow or constant mobility ratio

        INTERPRETATION PITFALLS:
        - Choosing incorrect MTR leads to erroneous k and s
        - Wellbore storage masks early-time data - cannot use
        - Phase redistribution in gas wells distorts buildup shape
        - p* ≠ true average pressure if tp insufficient or boundaries present
        """,
        key_factors=[
            "Production time tp relative to shut-in time Δt",
            "Clear identification of middle-time region straight line",
            "Wellbore storage coefficient C and duration",
            "Skin factor magnitude (positive damage, negative stimulation)",
            "Boundary effects timing and nature (sealing fault, constant pressure)",
            "Fluid properties accuracy (B, μ, ct)",
            "Gauge resolution and pressure stabilization",
            "Phase behavior complications (gas liberation, water influx)"
        ],
        primary_authority=[
            "SPE Monograph: Well Test Analysis - Horne (1995)",
            "Matthews-Brons-Hazebroek method for bounded reservoirs",
            "Horner 1951 original paper - pressure buildup in wells",
            "SPE 12777 - Horner time function application limits"
        ],
        burden_holder="Engineer performing test interpretation",
        adversary_position="Reservoir extends indefinitely; skin is negligible; permeability is higher than indicated",
        counter_arguments=[
            "Horner plot slope too steep - wellbore storage not fully dissipated",
            "p* extrapolation unreliable - tp/Δt ratio insufficient",
            "Skin factor uncertainty ±1-2 due to P1hr reading errors",
            "Permeability overestimated if partial penetration not corrected",
            "Dual porosity system - Horner line may be composite of matrix and fracture flow"
        ],
        resolution_strategy="Use type curve matching to confirm flow regimes, validate Horner analysis with MDH or Muskat methods, check derivative for wellbore storage end and boundary start, apply corrections for partial penetration or gas slippage if applicable.",
        entity_scope="Oil and gas wells - buildup test interpretation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 12777 - Bourdet derivative confirms flow regime before applying Horner"
    ),

    DoctrineBlock(
        topic="bourdet_derivative_analysis",
        keywords=["derivative", "bourdet", "flow regime", "log-log", "diagnosis", "wellbore storage", "radial flow"],
        conclusion_template=[
            "The Bourdet pressure derivative is the single most powerful diagnostic tool in modern well test analysis.",
            "Derivative stabilizes at 0.5 during wellbore storage-dominated flow, then transitions to horizontal plateau during infinite-acting radial flow.",
            "Derivative shape uniquely identifies flow regimes: linear flow (1/2 slope), bilinear (1/4 slope), dual porosity (dip then rise), boundaries (upward turn)."
        ],
        reasoning_framework="""
        BOURDET DERIVATIVE MECHANICS:
        - Derivative = d(ΔP)/d(ln Δt) plotted on log-log with ΔP vs Δt
        - Amplifies subtle pressure changes invisible on semilog plots
        - Noise-resistant through L-algorithm smoothing

        FLOW REGIME SIGNATURES:
        1. Wellbore Storage: derivative = 0.5*pressure (unit slope log-log)
        2. Infinite-Acting Radial Flow: derivative flat, ΔP half-slope → permeability calculated
        3. Linear Flow (fractures/channels): derivative 1/2 slope
        4. Bilinear Flow (finite-conductivity fracture): derivative 1/4 slope
        5. Dual Porosity Transition: derivative dips (fracture flow) then rises to plateau (total system)
        6. Sealing Boundary: derivative doubles at boundary arrival, then unit slope
        7. Constant Pressure Boundary: derivative drops toward zero

        INTERPRETATION PROTOCOL:
        - Match derivative shape to theoretical responses FIRST
        - Extract parameters from derivative-stabilized periods (not pressure alone)
        - Validate regime transitions timing against reservoir geometry
        - Check consistency: radial flow derivative value = 0.5*m (semilog slope)
        """,
        key_factors=[
            "Derivative smoothing parameter L (typically 0.1-0.3)",
            "Wellbore storage end time (derivative departs from unit slope)",
            "Duration of derivative plateau (radial flow period)",
            "Derivative magnitude during radial flow (inversely proportional to kh)",
            "Timing and shape of derivative deviations (boundaries, dual porosity)",
            "Pressure and derivative overlay quality on type curves",
            "Noise level in measured pressure data",
            "Multi-rate history effects on derivative shape"
        ],
        primary_authority=[
            "Bourdet et al. 1983 SPE 12777 - derivative introduction",
            "Horne 1995 Well Test Analysis - derivative interpretation",
            "SPE Textbook Series: Advanced Well Test Analysis (Blasingame)",
            "Gringarten type curves (1979) - fracture flow regimes"
        ],
        burden_holder="Test analyst - prove flow regime identification is correct",
        adversary_position="Derivative features are noise artifacts; radial flow never truly achieved; boundaries are closer than interpreted",
        counter_arguments=[
            "Derivative smoothing obscures real reservoir heterogeneity",
            "Dual porosity dip could be gauge resolution artifact",
            "Horizontal derivative not truly flat - slight upward trend indicates boundary approaching",
            "Bilinear flow misidentified - actually wellbore storage + skin transition",
            "Type curve match non-unique - multiple models fit data equally well"
        ],
        resolution_strategy="Use multiple independent analysis methods (Horner, MDH, type curve, simulation history match). Validate regime timing against expected reservoir dimensions. Check derivative consistency with pressure behavior. Perform sensitivity analysis on smoothing parameter.",
        entity_scope="All well test types - buildup, drawdown, interference, injection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 12777 - derivative mandatory for modern analysis"
    ),

    DoctrineBlock(
        topic="skin_factor_determination",
        keywords=["skin", "damage", "stimulation", "near-wellbore", "permeability impairment", "acid", "fracture"],
        conclusion_template=[
            "Skin factor quantifies the additional pressure drop (or reduction) due to near-wellbore alterations compared to ideal radial flow.",
            "Positive skin indicates formation damage (drilling mud invasion, fines migration, scale deposition); negative skin indicates stimulation (acidizing, hydraulic fracturing).",
            "Total skin s decomposes into mechanical components: s = sd + sp + sθ + sc + ... where sd=damage, sp=partial penetration, sθ=deviation, sc=completion effects."
        ],
        reasoning_framework="""
        SKIN FACTOR CALCULATION:
        From Horner or MDH analysis:
        s = 1.151 * [(Pws,1hr - Pwf,Δt=0) / m - log(k / φμctrw²) + 3.23]

        From type curve match:
        s = (ΔP_actual - ΔP_ideal) / (radial flow regime pressure drop per log cycle)

        PHYSICAL INTERPRETATION:
        - s = 0: ideal well, no damage or stimulation
        - s > 0: damaged well, equivalent to reduced wellbore radius rw' = rw*exp(-s)
        - s < 0: stimulated well, effective wellbore radius increased
        - s = -5 to -7: typical for hydraulically fractured vertical wells (infinite-conductivity fracture)
        - s = 5-20: moderate to severe drilling damage
        - s > 50: severe plugging, near-wellbore permeability <0.1 md

        SKIN COMPONENT DECOMPOSITION:
        sd = damage skin (drilling, completion, production-induced)
        sp = partial penetration skin = (h/hp - 1)*ln(h/rw) for hp < h
        sθ = deviation skin for deviated/horizontal wells
        sc = completion skin (perforations, gravel pack)
        sf = pseudoskin from turbulence (gas wells, high-rate oil wells)

        DIAGNOSTIC CRITERIA:
        - If s varies with rate → turbulent pseudoskin sf = DQ present
        - If s varies with time → time-dependent damage (fines migration, asphaltene)
        - If s negative but no stimulation → horizontal well or high-angle deviation
        - If s > 20 → economic damage, acid stimulation candidate
        """,
        key_factors=[
            "Accuracy of P1hr or equivalent pressure reading",
            "Semilog slope m accuracy (affects skin ±30% if m off by 10%)",
            "Wellbore radius rw measurement (nominal vs caliper log)",
            "Fluid property values (μ, B, ct) at test conditions",
            "Phase behavior corrections (gas slippage, oil undersaturation)",
            "Rate history normalization for multi-rate tests",
            "Superposition effects if variable rate history",
            "Non-Darcy flow coefficient D for gas wells"
        ],
        primary_authority=[
            "van Everdingen-Hurst 1949 - skin factor definition",
            "Hawkins formula for damaged zone skin: s = (k/kd - 1)*ln(rd/rw)",
            "SPE 7490 - skin decomposition methods",
            "SPE Monograph - completion and workover skin effects"
        ],
        burden_holder="Reservoir engineer - justify skin magnitude and propose remediation",
        adversary_position="Skin is lower than calculated; damage is transient and will improve; stimulation is unnecessary based on current economics",
        counter_arguments=[
            "High skin could be partial penetration, not damage - perforating entire interval may suffice",
            "Calculated skin unreliable if wellbore storage not fully dissipated",
            "Rate-dependent skin component (turbulence) not separated from true damage",
            "Horizontal well pseudoradial skin misinterpreted as formation damage",
            "Negative skin from acidizing may be temporary - permeability damage recurs"
        ],
        resolution_strategy="Decompose total skin into geometric (sp, sθ) and true damage (sd) components. Compare to offset wells in same reservoir. Validate with production performance matching. If high damage, run diagnostic injection test or perform step-rate test to confirm damage zone radius and permeability.",
        entity_scope="Vertical, deviated, and horizontal wells - all reservoir types",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="dual_porosity_interpretation",
        keywords=["dual porosity", "naturally fractured", "matrix", "fracture", "warren-root", "transition", "storativity ratio", "interporosity"],
        conclusion_template=[
            "Dual porosity behavior is diagnostic of naturally fractured reservoirs where fractures provide permeability and matrix provides storage.",
            "Characteristic signature: early-time fracture radial flow, transition dip on derivative, late-time total system radial flow at higher level.",
            "Warren-Root parameters ω (storativity ratio) and λ (interporosity flow coefficient) quantify fracture-matrix system properties."
        ],
        reasoning_framework="""
        DUAL POROSITY MODEL (Warren-Root 1963):

        CONCEPTUAL MODEL:
        - Fracture network: high permeability kf, low storativity φfctf
        - Matrix blocks: low permeability km, high storativity φmctm
        - Fluid flows from matrix into fractures, then radially to wellbore through fractures

        DEFINING PARAMETERS:
        ω = (φct)f / [(φct)f + (φct)m] = fracture storativity fraction (0.001 - 0.1 typical)
        λ = α*rw²*km / kf = interporosity flow parameter (10⁻⁸ - 10⁻⁵ typical)
        α = shape factor depending on matrix block geometry (12/L² for slabs, 60/L² for cubes)

        PRESSURE TRANSIENT SIGNATURES:
        1. Early time: fracture system radial flow - derivative plateau at level (kh)f
        2. Transition: derivative dips to minimum (0.5*ω times early plateau)
        3. Late time: total system radial flow - derivative plateau at level (kh)total

        DERIVATIVE DIP CHARACTERISTICS:
        - Dip depth ∝ ω (storativity ratio)
        - Dip timing ∝ 1/λ (interporosity flow rate)
        - Deep dip (ω < 0.01): highly fractured, low matrix contribution
        - Shallow dip (ω > 0.1): moderately fractured, substantial matrix storage
        - Late transition (small λ): low matrix permeability, slow equilibration

        INTERPRETATION WORKFLOW:
        1. Match early-time derivative plateau → kf*h (fracture permeability-thickness)
        2. Match late-time derivative plateau → ktotal*h = (kf + km)*h
        3. Match dip depth → ω (fracture storativity fraction)
        4. Match dip timing → λ (interporosity flow coefficient)
        5. Calculate matrix permeability km and matrix block size L from ω and λ
        """,
        key_factors=[
            "Derivative dip depth (ω determination accuracy)",
            "Derivative dip timing (λ determination accuracy)",
            "Early and late radial flow plateau durations",
            "Fracture permeability kf vs total permeability ktotal ratio",
            "Matrix block size L from shape factor α assumptions",
            "Pseudosteady-state vs transient interporosity flow model selection",
            "Skin factor - applies to fracture system, not matrix",
            "Wellbore storage masking early fracture radial flow"
        ],
        primary_authority=[
            "Warren-Root 1963 SPE 426 - dual porosity model foundation",
            "Bourdet 1983 derivative application to dual porosity",
            "Cinco-Ley 1981 - transient interporosity flow model",
            "SPE Monograph: Naturally Fractured Reservoir Engineering (Aguilera)"
        ],
        burden_holder="Petrophysicist and reservoir engineer - prove dual porosity vs dual permeability vs single porosity",
        adversary_position="Reservoir is single porosity with heterogeneity; derivative dip is noise or boundary effect; fracture permeability is lower than interpreted",
        counter_arguments=[
            "Derivative dip could be partial penetration effect, not dual porosity",
            "Matrix permeability calculated from λ is model-dependent - actual block geometry unknown",
            "Dual permeability (matrix and fractures both permeable) fits data equally well",
            "Layered reservoir with crossflow mimics dual porosity signature",
            "Wellbore storage + skin transition can create false dip appearance"
        ],
        resolution_strategy="Validate dual porosity interpretation with: (1) core analysis for fracture density and matrix properties, (2) image logs for fracture characterization, (3) PLT for flow profile, (4) production history match requiring dual porosity model. Compare ω and λ to offset fractured wells in same field.",
        entity_scope="Naturally fractured carbonate and shale reservoirs",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Warren-Root model widely accepted but assumes idealized fracture-matrix geometry"
    ),

    DoctrineBlock(
        topic="boundary_effect_identification",
        keywords=["boundary", "sealing fault", "constant pressure", "channel", "wedge", "rectangular", "closed", "finite reservoir"],
        conclusion_template=[
            "Boundary effects manifest when pressure disturbance reaches reservoir limits, altering pressure derivative from infinite-acting radial flow.",
            "Sealing boundary: derivative doubles from radial plateau, then unit slope (pseudosteady state). Distance L = 0.01217*sqrt(kt/φμct) at boundary start time.",
            "Constant pressure boundary: derivative drops toward zero. Reservoir is infinite-acting from well perspective but pressure-supported."
        ],
        reasoning_framework="""
        BOUNDARY DETECTION FROM DERIVATIVE:

        SEALING FAULT (no-flow boundary):
        - Derivative departs upward from radial flow plateau
        - For single linear fault: derivative doubles (2x radial level), ΔP becomes linear in Δt (pseudosteady state)
        - Distance to fault: L = 0.01217 * sqrt(k*tdf / φμct) [ft] where tdf = time to derivative upward departure
        - For closed rectangular reservoir: derivative unit slope, pressure linear in Δt, slope ∝ 1/(drainage area)

        CONSTANT PRESSURE BOUNDARY (aquifer, gas cap, injection support):
        - Derivative drops from radial plateau toward zero
        - Indicates recharge from adjacent high-permeability zone or pressure maintenance
        - Distance to boundary: same formula as sealing fault using time of derivative downturn
        - Pressure stabilizes or declines slowly in late time

        CHANNEL RESERVOIR (two parallel sealing faults):
        - Early radial flow, then linear flow (1/2 slope on derivative)
        - Channel width W from linear flow slope
        - Late-time pseudosteady state (unit slope) after pressure hits channel ends

        WEDGE RESERVOIR (two faults at angle θ):
        - Derivative slope = θ/(2π) after radial flow
        - 90° wedge: derivative 1/4 slope
        - 180° fault: derivative doubles (standard sealing fault)

        DIAGNOSTIC CRITERIA:
        - tdf (boundary detection time) >> tws (wellbore storage end) for reliable interpretation
        - Multiple boundaries may interact - first arrival sets initial derivative departure
        - Interference from nearby wells mimics boundary effects
        - Late-time pressure falloff test more sensitive to boundaries than buildup
        """,
        key_factors=[
            "Time to boundary detection tdf from derivative departure",
            "Hydraulic diffusivity α = k/(φμct) accuracy",
            "Reservoir geometry (1D, 2D, 3D flow) determination",
            "Distance to boundary L calculation uncertainty (±30% typical)",
            "Distinction between true boundary vs interference from offset wells",
            "Shape of boundary (linear fault vs curved edge vs wedge)",
            "Boundary type (sealing vs constant pressure vs leaky)",
            "Multiple boundary interactions (e.g., channel reservoir)"
        ],
        primary_authority=[
            "Earlougher 1977 - boundary effects in well testing",
            "SPE Monograph: Advances in Well Test Analysis (finite reservoir shapes)",
            "Gray 1965 - linear reservoir testing",
            "Ramey-Cobb 1971 - wedge-shaped reservoirs"
        ],
        burden_holder="Geologist and reservoir engineer - validate boundary interpretation against seismic and geologic model",
        adversary_position="No boundary exists; derivative upturn is dual porosity transition or heterogeneity; reservoir is larger than indicated",
        counter_arguments=[
            "Boundary distance calculated assumes homogeneous k, φ, ct - heterogeneity could alter timing significantly",
            "Derivative upturn could be start of dual porosity late-time plateau, not boundary",
            "Interference from nearby producing wells creates pseudoboundary effect",
            "Constant pressure interpretation non-unique - could be high-permeability streak, not aquifer",
            "Channel width from linear flow assumes no crossflow - layered reservoir could give same signature"
        ],
        resolution_strategy="Correlate boundary distance and azimuth with seismic fault interpretation. Use image logs and core to confirm fault presence. Check offset well tests for consistent boundary location. Run interference test to distinguish boundary from well interference. Perform reservoir simulation with geologic model to validate boundary placement.",
        entity_scope="All reservoirs - oil, gas, water injection, pressure maintenance",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Boundary interpretation requires geologic corroboration for high confidence"
    ),

    DoctrineBlock(
        topic="horizontal_well_testing",
        keywords=["horizontal well", "pseudoradial", "linear flow", "early radial", "compound linear", "anisotropy", "vertical permeability"],
        conclusion_template=[
            "Horizontal wells exhibit multi-stage flow regimes: early radial (vertical plane), compound linear, late pseudoradial (ellipsoidal drainage).",
            "Derivative signatures: early 0.5 slope (radial perpendicular to wellbore), 1/2 slope (linear flow along wellbore), late plateau (pseudoradial total system).",
            "Permeability anisotropy kv/kh and horizontal length L determined from regime transition times and derivative slopes."
        ],
        reasoning_framework="""
        HORIZONTAL WELL FLOW REGIMES (Goode-Thambynayagam):

        REGIME 1 - Early Radial Flow (ERF):
        - Radial flow in vertical plane perpendicular to horizontal wellbore
        - Derivative = 0.5, pressure 1/2 slope on log-log
        - Duration short unless wellbore very long or kh >> kv
        - Yields kv (vertical permeability) from derivative level

        REGIME 2 - Compound Linear Flow (CLF):
        - Linear flow from formation into wellbore along length L
        - Derivative 1/2 slope, pressure 1/2 slope on log-log
        - Characteristic of horizontal wells in low-permeability reservoirs
        - Yields sqrt(khkv) and horizontal length L from slope

        REGIME 3 - Late Pseudoradial Flow (LPRF):
        - Ellipsoidal radial flow around entire horizontal wellbore
        - Derivative plateau (flat), pressure 1/2 slope semilog
        - Yields effective permeability keff = sqrt(khkv) from derivative level
        - Negative skin common due to increased drainage area (s = -3 to -6)

        REGIME 4 - Boundary Effects:
        - Top/bottom boundaries: derivative upturn if h/L ratio small
        - Lateral boundaries: derivative doubles or unit slope depending on geometry

        ANISOTROPY DETERMINATION:
        - kv from early radial flow derivative (if observed)
        - kh from late pseudoradial flow derivative and kv/kh ratio
        - Anisotropy ratio β = sqrt(kv/kh) from transition time ratios

        INTERPRETATION CHALLENGES:
        - Early radial flow often masked by wellbore storage
        - Compound linear flow may not develop if wellbore short or high anisotropy
        - Pseudoradial flow requires long test time (days to weeks in tight reservoirs)
        - Partial penetration effects if wellbore near top or bottom of interval
        - Heel-toe pressure variations in long horizontals complicate interpretation
        """,
        key_factors=[
            "Horizontal wellbore length L (measured depth in pay)",
            "Formation thickness h and wellbore position within interval",
            "Permeability anisotropy ratio kv/kh (typically 0.01 - 0.5)",
            "Effective wellbore radius (perforation density, openhole vs cased)",
            "Test duration required to reach pseudoradial flow",
            "Wellbore storage effects duration (wellbore volume large)",
            "Partial penetration corrections if wellbore eccentricity high",
            "Multiphase flow effects (gas coning, water slumping)"
        ],
        primary_authority=[
            "Goode-Thambynayagam 1987 SPE 16378 - horizontal well flow regimes",
            "Kuchuk 1991 - horizontal well test interpretation",
            "SPE Monograph: Horizontal Well Technology (Joshi)",
            "Cinco-Ley 1994 - transient pressure behavior of horizontal wells"
        ],
        burden_holder="Reservoir engineer - prove flow regime identification and anisotropy ratio",
        adversary_position="Horizontal well behaves as very-high-productivity vertical well with large negative skin; anisotropy is less than interpreted; permeability higher",
        counter_arguments=[
            "Compound linear flow slope could be fracture linear flow, not formation linear flow",
            "Pseudoradial flow never truly achieved - test stopped during transition",
            "Negative skin misattributed to geometry - actual stimulation (acid, fracture) present",
            "Anisotropy ratio unreliable if early radial flow not clearly observed",
            "Wellbore storage too long - early regimes completely masked"
        ],
        resolution_strategy="Use Goode-Thambynayagam type curves to match all regimes simultaneously. Validate anisotropy ratio with core analysis (kv/kh from minipermeameter or probe permeability). Check production performance against well test permeability. Use multiphase production log to confirm uniform inflow along lateral.",
        entity_scope="Horizontal and high-angle wells in conventional and unconventional reservoirs",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Horizontal well requires long test duration and high-resolution pressure gauges for reliable interpretation"
    ),

    DoctrineBlock(
        topic="rate_transient_analysis_unconventional",
        keywords=["rate transient analysis", "RTA", "blasingame", "agarwal-gardner", "flowing material balance", "NPI", "FMB", "type curve", "unconventional"],
        conclusion_template=[
            "Rate Transient Analysis (RTA) extracts reservoir properties from production rate and pressure data, particularly valuable for unconventional wells lacking shut-in tests.",
            "Blasingame type curves normalize rate and time using material balance pseudotime and pseudopressure, collapsing variable-rate/variable-pressure data onto single curve.",
            "Flowing Material Balance (FMB) provides model-independent original gas-in-place (OGIP) from linear plot of normalized pressure vs normalized cumulative production."
        ],
        reasoning_framework="""
        RATE TRANSIENT ANALYSIS FOUNDATIONS:

        BLASINGAME TYPE CURVES (1991):
        - Normalize rate: qD = q/(qiΔm) where Δm = m(pi) - m(pwf)
        - Normalize time: tDd = (β*ta)/Ac or material balance time tmb = Np/q
        - Plot qD vs tDd, match to type curves for b, d (decline exponents)
        - Works for oil (liquid flow) and gas (pseudopressure m(p) normalization)
        - Extracts permeability, skin, drainage area from type curve match

        AGARWAL-GARDNER (1999) - Flowing Material Balance:
        - Plot (m(pi) - m(pwf))/q vs Gp (gas) or (pi - pwf)/q vs Np (oil)
        - Straight line indicates boundary-dominated flow (BDF)
        - Slope = 1/OGIP for gas, 1/N for oil (volumetric reserves)
        - Y-intercept = skin and permeability effects
        - Model-independent - no assumption about reservoir shape or decline model

        NPI (Normalized Pressure Integral) Method:
        - Integrates pressure drop over time, normalizing for variable rate
        - Converts rate-time data into equivalent constant-rate drawdown
        - Applicable to both conventional and unconventional wells
        - Identifies flow regimes from NPI derivative

        UNCONVENTIONAL WELL RTA SPECIFICS:
        - Long transient period (years) due to ultra-low permeability
        - Linear flow dominant (1/2 slope) from hydraulic fractures
        - Extract fracture half-length xf and permeability k from linear flow slope
        - Stimulated reservoir volume (SRV) estimation from late-time BDF
        - Multi-well interference common - analyze as single drainage unit

        DIAGNOSTIC WORKFLOW:
        1. Plot log(rate) vs log(time) - identify decline regime (hyperbolic b, harmonic, exponential)
        2. Normalize with material balance time and pseudopressure
        3. Match Blasingame type curves - extract k, skin, Ac
        4. Plot FMB - validate BDF start, calculate OGIP
        5. Compare RTA permeability to core and well test values
        """,
        key_factors=[
            "Data quality - high-frequency rate and pressure measurements required",
            "Pseudopressure calculation accuracy for gas wells",
            "Material balance time vs real time selection",
            "Flow regime duration - need BDF for reserves estimate",
            "Multi-well interference effects on decline curve",
            "Hydraulic fracture contribution vs formation permeability",
            "Stimulated reservoir volume (SRV) uncertainty",
            "Depletion level - RTA most accurate in late transient to BDF transition"
        ],
        primary_authority=[
            "Blasingame et al. 1991 SPE 21688 - type curve analysis",
            "Agarwal-Gardner 1999 SPE 51902 - flowing material balance",
            "Wattenbarger et al. 1998 - unconventional gas RTA",
            "Clarkson 2013 SPE 162665 - shale RTA production analysis methods"
        ],
        burden_holder="Production engineer - demonstrate RTA results consistent with geology and well test",
        adversary_position="RTA overestimates reserves; permeability is lower than RTA indicates; drainage area is smaller due to poor fracture conductivity",
        counter_arguments=[
            "Blasingame match non-unique - multiple (k, Ac, skin) combinations fit data",
            "FMB straight line start ambiguous - BDF not clearly established",
            "Multi-well interference violates single-well RTA assumptions",
            "Pressure data unreliable - static bottomhole pressure estimated, not measured",
            "Hydraulic fracture degradation over time not accounted for in model",
            "Geomechanical effects (stress-dependent permeability) alter decline beyond reservoir depletion"
        ],
        resolution_strategy="Calibrate RTA with PLT data showing fracture contribution. Validate OGIP with volumetric calculation (Ac*h*φ*Sg/Bg). Cross-check with decline curve analysis (Arps) for consistency. Use reservoir simulation with explicit fracture model to history match production and RTA interpretation.",
        entity_scope="Unconventional oil and gas wells - shale, tight gas, coalbed methane",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="RTA requires boundary-dominated flow for reliable reserves - many unconventional wells never reach BDF"
    ),

    DoctrineBlock(
        topic="wellbore_storage_effects",
        keywords=["wellbore storage", "after-production", "C", "unit slope", "dimensionless", "fluid expansion", "compression"],
        conclusion_template=[
            "Wellbore storage masks reservoir response during early test time as fluid level changes or fluid expands/compresses in wellbore.",
            "Diagnostic signature: pressure and derivative both on unit slope (log-log) until storage effects dissipate.",
            "Dimensionless wellbore storage CsD = 0.8936C/(φcth rw²) determines duration: tws,end ≈ (60+3.5s)*C/(kh) [hours]."
        ],
        reasoning_framework="""
        WELLBORE STORAGE MECHANISMS:

        1. CHANGING FLUID LEVEL:
        - After shut-in, fluid continues to flow from formation into wellbore, raising fluid level
        - Wellbore acts as capacitor, storing produced fluid
        - Common in pumping wells, gas wells with liquid loading
        - Storage coefficient C = Vwb/144 (bbl/psi) for changing level

        2. WELLBORE FLUID COMPRESSION:
        - In wells shut in downhole (packer, SSSV), wellbore volume constant
        - Pressure rise compresses fluid in wellbore
        - Storage coefficient C = Vwb*cwb where cwb = fluid compressibility
        - Smaller C than changing level, but still significant in large-diameter wells

        3. PHASE REDISTRIBUTION:
        - Gas wells: liquid fallback, gas expansion
        - Oil wells: gas evolution, liquid swelling
        - Creates complex storage behavior, time-dependent C

        WELLBORE STORAGE EFFECT DURATION:
        tws,end = (60 + 3.5*s) * C / (k*h) [hours]
        - Proportional to wellbore volume and skin
        - Inversely proportional to permeability-thickness
        - High skin dramatically extends storage duration

        DIAGNOSTIC CRITERIA:
        - Log-log plot: ΔP and derivative both unit slope (45°)
        - Derivative value = 0.5 * pressure value during storage
        - CDe²s = dimensionless storage-skin group from type curve match
        - Storage ends when derivative departs from unit slope

        MITIGATION STRATEGIES:
        - Use downhole shut-in tools (reduce wellbore volume below packer)
        - Extend test duration until radial flow achieved
        - Use superposition for variable-rate history correction
        - Apply type curve deconvolution to extract reservoir response
        """,
        key_factors=[
            "Wellbore volume Vwb (larger diameter = larger C)",
            "Skin factor s (high skin extends storage duration)",
            "Permeability-thickness kh (low kh extends storage duration)",
            "Shut-in method (surface vs downhole valve)",
            "Fluid type and phase behavior (gas, oil, multiphase)",
            "Test duration relative to storage end time",
            "Gauge location (bottomhole vs surface measurement)",
            "Rate history before shut-in (affects storage contribution)"
        ],
        primary_authority=[
            "Agarwal et al. 1970 SPE 2735 - wellbore storage and skin",
            "Bourdet 1983 - derivative identification of storage end",
            "Ramey 1976 - wellbore storage during buildup tests",
            "SPE Monograph: Practical Solutions to wellbore storage"
        ],
        burden_holder="Test engineer - prove storage has ended before interpreting reservoir parameters",
        adversary_position="Wellbore storage ended earlier than interpreted; radial flow achieved sooner; permeability higher than calculated",
        counter_arguments=[
            "Derivative departure from unit slope is subtle - analyst may claim storage ended too early",
            "Phase redistribution creates pseudo-storage that extends beyond classical storage model",
            "Variable-rate history before shut-in violates constant-rate storage assumption",
            "Partial communication (layered reservoir, non-radial flow) mimics storage signature",
            "Storage coefficient C varies with pressure (phase behavior, tool operation)"
        ],
        resolution_strategy="Match pressure and derivative simultaneously on type curves to determine CDe²s. Validate storage coefficient C with wellbore volume calculation and fluid properties. Extend test duration until derivative clearly departs from unit slope and stabilizes at radial flow plateau. Use deconvolution algorithms if early-time data needed.",
        entity_scope="All well tests - critical for buildup, drawdown, injection, falloff",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Cannot interpret permeability or skin reliably until wellbore storage effects have dissipated"
    ),

    DoctrineBlock(
        topic="formation_interval_testing",
        keywords=["wireline formation test", "MDT", "RFT", "pretests", "mini-DST", "spherical flow", "pressure gradient", "mobility"],
        conclusion_template=[
            "Wireline formation testers (MDT, RFT) provide rapid pressure and mobility measurements at multiple depths without completing the well.",
            "Pretests create small spherical flow regime lasting seconds to minutes, yielding localized permeability estimates from pressure buildup.",
            "Pressure gradient from multi-depth measurements defines fluid contacts (OWC, GWC, GOC) and vertical communication."
        ],
        reasoning_framework="""
        FORMATION TESTER OPERATIONS:

        PRETEST SEQUENCE:
        1. Seal probe or dual-packer against formation
        2. Withdraw small fluid volume (5-20 cc) creating drawdown
        3. Shut in and monitor pressure buildup
        4. Repeat at multiple depths across interval

        SPHERICAL FLOW ANALYSIS:
        - Early time dominated by spherical flow into probe
        - Permeability from spherical flow equation: k = (Qμ / 4πrp*ΔP)
        - Pressure buildup rate ∝ k (high k = fast buildup)
        - Mobilityk/μ measured directly from buildup slope

        VERTICAL PRESSURE GRADIENT:
        - Plot pressure vs depth for all pretest points
        - Slope = fluid density gradient (0.433 psi/ft for fresh water, 0.35-0.45 oil)
        - Breaks in slope indicate fluid contacts or pressure compartments
        - Horizontal pressure intervals suggest vertical barriers (shale, cemented layers)

        MINI-DST (Extended Drawdown/Buildup):
        - Withdraw larger fluid volume (gallons to barrels) over minutes to hours
        - Achieves radial or ellipsoidal flow regime
        - Permeability anisotropy (kh vs kv) from flow regime transition
        - Formation damage assessment from skin factor

        DATA QUALITY FACTORS:
        - Supercharging: mudcake invasion raises measured pressure above true formation pressure
        - Tool movement: poor seal or wireline heave creates artifacts
        - Low permeability (<0.1 md): buildup too slow for reliable analysis
        - Heterogeneity: probe samples local <1 ft zone, may not represent bulk reservoir

        INTERPRETATION WORKFLOW:
        1. Correct for supercharging using pressure decline rate
        2. Identify spherical flow period on log-log plot
        3. Calculate mobility k/μ from buildup slope
        4. Estimate permeability using assumed or measured fluid viscosity
        5. Construct pressure-depth profile for fluid contacts
        6. Compare to well test permeability (WFT typically lower due to damage, scale)
        """,
        key_factors=[
            "Probe sealing quality (leak-off indicates poor seal)",
            "Formation permeability (< 0.1 md often too low for WFT)",
            "Mudcake thickness and invasion depth",
            "Supercharging magnitude and dissipation rate",
            "Pretest volume withdrawn (larger volume = deeper investigation)",
            "Pressure gauge resolution (0.1 psi or better required)",
            "Vertical spacing of test points (need 3+ per fluid type for gradient)",
            "Time allowed for buildup (often limited by rig time)"
        ],
        primary_authority=[
            "Schlumberger MDT Interpretation Principles Manual",
            "Halliburton RFT Analysis Guidelines",
            "SPE 77964 - formation tester applications and interpretation",
            "Kuchuk et al. - Wireline Formation Testing and Well Deliverability"
        ],
        burden_holder="Petrophysicist and log analyst - validate WFT permeability against core and well test",
        adversary_position="WFT permeability overestimates true reservoir permeability; fluid contacts are uncertain; pressure gradient indicates better vertical communication than actual",
        counter_arguments=[
            "WFT permeability is near-wellbore invaded zone, not virgin reservoir",
            "Supercharging correction unreliable - true formation pressure unknown",
            "Pressure break identified as fluid contact could be pressure compartment boundary",
            "Low-permeability zones may not build up pressure sufficiently for accurate reading",
            "Anisotropy effects - horizontal permeability from WFT may be much higher than vertical"
        ],
        resolution_strategy="Calibrate WFT permeability with core plugs from same depth. Use multiple pretest points to confirm pressure gradient consistency. Compare WFT fluid contacts with resistivity log contacts. Run extended mini-DST if WFT pretest permeability uncertain. Validate vertical communication with well test or tracer survey.",
        entity_scope="Exploration and appraisal wells - pre-completion formation evaluation",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="WFT provides valuable pressure and mobility data but permeability often lower than well test due to near-wellbore damage and small sample volume"
    ),

    DoctrineBlock(
        topic="interference_pulse_testing",
        keywords=["interference test", "pulse test", "multi-well", "connectivity", "anisotropy direction", "reservoir extent", "communication"],
        conclusion_template=[
            "Interference and pulse tests measure pressure response at observation wells during active or pulsed production/injection at source well, proving reservoir connectivity.",
            "Interference test: constant-rate production at active well, monitor pressure decline at observation wells. Time lag and magnitude indicate permeability, distance, and boundaries between wells.",
            "Pulse test: cyclic rate changes at active well create pressure pulses at observation wells. Phase lag and amplitude attenuation yield permeability and porosity independently."
        ],
        reasoning_framework="""
        INTERFERENCE TESTING PRINCIPLES:

        TEST DESIGN:
        - Active well: produce or inject at constant rate
        - Observation wells: shut in, monitor downhole pressure with high-resolution gauges
        - Test duration: hours to months depending on permeability and well spacing
        - Minimum 2 observation wells required; 3+ allows anisotropy determination

        PRESSURE RESPONSE ANALYSIS:
        - Time to first detectable response t1 at distance r: t1 ≈ 948*φμct*r² / k [hours]
        - Pressure drop magnitude ΔP ∝ k*t, inversely ∝ r² (infinite-acting period)
        - Log-log plot of ΔP vs time - match to line source solution or type curves
        - Extract k, φct from pressure buildup rate and arrival time

        ANISOTROPY DETERMINATION:
        - Observation wells at different azimuths respond at different times
        - Principal permeability directions kmax, kmin from elliptical pressure front
        - Anisotropy ratio kmax/kmin from ratio of arrival times at equal distances
        - Azimuth of kmax from orientation of fastest pressure response

        PULSE TESTING (Kamal-Brigham Method):
        - Active well: alternate high and low rates in square-wave pulses (e.g., 6 hr on, 6 hr off)
        - Observation well: pressure oscillates with same period but delayed phase and reduced amplitude
        - Phase lag τ and amplitude ratio A determine k and φct independently
        - Advantage over interference: shorter test time, less ambiguity in parameter estimation

        PULSE TEST ANALYSIS:
        - Phase lag τ = time delay between active well rate change and observation well pressure peak
        - From phase lag: k*t / (φμct*r²) = function(τ/pulse period)
        - From amplitude ratio: A = ΔPobs / ΔPactive = function(k*t, φμct*r²)
        - Solve simultaneously for k and φct

        DIAGNOSTIC APPLICATIONS:
        - Prove reservoir communication before waterflooding or EOR
        - Map permeability anisotropy for infill drilling optimization
        - Identify barriers between wells (faults, facies changes)
        - Measure sweep efficiency and injector-producer connectivity
        - Detect fracture network orientation in naturally fractured reservoirs
        """,
        key_factors=[
            "Well spacing r (closer wells = faster response, easier detection)",
            "Permeability magnitude (low k = long test duration, weeks to months)",
            "Porosity-compressibility product φct accuracy",
            "Observation well gauge resolution (0.01 psi required for long distances)",
            "Shut-in observation well storage effects (must end before response arrives)",
            "Rate stability at active well (constant rate critical for interference test)",
            "Pulse period selection for pulse test (6-24 hr typical)",
            "Background noise from barometric pressure, earth tides, other wells"
        ],
        primary_authority=[
            "Earlougher 1977 - interference test analysis chapter",
            "Kamal-Brigham 1975 SPE 5053 - pulse testing method",
            "Johnson et al. 1966 - pulse test interpretation",
            "SPE Monograph: Interference Testing (Cherry-Coats)"
        ],
        burden_holder="Reservoir engineer - prove test duration sufficient and response is real, not noise",
        adversary_position="No communication exists between wells; permeability is lower than interpreted; pressure response is from another source (aquifer, leakage)",
        counter_arguments=[
            "Pressure response too small - could be instrument noise or barometric variation",
            "Time lag too short - response is from local high-permeability channel, not bulk reservoir",
            "Anisotropy interpretation unreliable with only 2-3 observation wells",
            "Pulse test phase lag ambiguous - multiple k, φct pairs could fit data",
            "Interference from other active wells in field contaminates observation well response"
        ],
        resolution_strategy="Run test with redundant observation wells (4+ preferred). Use downhole shut-in tools to eliminate wellbore storage. Validate response arrival time against expected diffusivity. Compare interference permeability with well test and core values. Use tracer test to independently confirm communication. Perform reservoir simulation of interference test to validate interpretation.",
        entity_scope="Multi-well reservoirs - waterfloods, gas storage, enhanced recovery projects",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Interference tests prove connectivity but require high-quality pressure data and long test duration for low-permeability reservoirs"
    ),

    DoctrineBlock(
        topic="drill_stem_test_interpretation",
        keywords=["DST", "drill stem test", "initial flow", "final flow", "buildup", "cushion", "closed-chamber", "flow-shut-in sequence"],
        conclusion_template=[
            "Drill stem tests (DST) temporarily complete a well during drilling to measure formation pressure, flow rate, and fluid type without permanent completion.",
            "Standard DST sequence: initial flow period (IF), initial shut-in (ISI), final flow period (FF), final shut-in (FSI), each yielding distinct reservoir information.",
            "DST provides rapid assessment of reservoir productivity, permeability, skin, and fluid contacts, enabling drill-or-abandon decisions."
        ],
        reasoning_framework="""
        DST TOOL STRING COMPONENTS:
        - Packer: isolates tested interval from annulus
        - Flow valves: control when formation can flow into drillpipe
        - Pressure recorders: measure downhole pressure vs time
        - Reverse circulating valve: allows bullheading cushion fluid
        - Safety valve: prevents uncontrolled flow to surface

        DST SEQUENCE:
        1. RUN IN HOLE: Set packer, close annulus
        2. INITIAL FLOW (IF): Open valve, allow formation to flow into pipe (minutes to hours)
           - Measures initial productivity, formation pressure, fluid type
           - Drawdown pressure decline indicates permeability and skin
        3. INITIAL SHUT-IN (ISI): Close valve, monitor pressure buildup
           - Buildup analysis yields k, s, formation pressure pi
           - Typically shorter than final shut-in
        4. FINAL FLOW (FF): Reopen valve, longer flow period (hours)
           - Confirms sustained productivity, checks for boundaries
           - May reach stabilized flow rate if high permeability
        5. FINAL SHUT-IN (FSI): Close valve, final buildup
           - Most reliable buildup for analysis (longer duration)
           - Horner or MDH analysis for final k, s, p*
        6. PULL OUT OF HOLE: Retrieve tool, recover samples

        PRESSURE ANALYSIS:
        - Initial hydrostatic pressure = mud gradient * depth
        - First opening: sharp pressure drop if good communication
        - Buildup: analyze with Horner or MDH (same as production well test)
        - Flow period: transient IPR if stabilization not achieved
        - Cushion effects: hydrostatic head of cushion fluid affects pressure measurement

        FLOW ANALYSIS:
        - Surface flow rate measured during flow periods
        - Productivity index J = q / (pi - pwf) [stb/d/psi]
        - Compare to expected productivity from core permeability
        - Fluid recovery: oil, gas, water, mud filtrate analyzed

        DIAGNOSTIC SIGNATURES:
        - Good test: sharp pressure drop on opening, rapid buildup to formation pressure
        - Tight formation: slow pressure drop, minimal buildup, low recovery
        - Formation damage: high skin, slow buildup, low flow rate
        - Water influx: pressure support, increasing water cut during flow
        - Gas cut mud: indicates gas zone, need special precautions
        """,
        key_factors=[
            "Packer seal quality (leak-off invalidates test)",
            "Cushion fluid density and volume (affects hydrostatic correction)",
            "Flow period duration (need sufficient drawdown for analysis)",
            "Shut-in period duration (need radial flow period for k, s)",
            "Gauge clock accuracy and resolution",
            "Formation damage from mud filtrate invasion",
            "Phase behavior (gas, oil, water) and sampling",
            "Tool string configuration (closed chamber vs open to surface)"
        ],
        primary_authority=[
            "SPE Monograph: Drill Stem Testing (Lebourg)",
            "Schlumberger DST Interpretation Charts",
            "SPWLA DST Interpretation Guidelines",
            "API RP-56 Drill Stem Test Practices"
        ],
        burden_holder="Drilling and completions engineer - decide to test, complete, or abandon based on DST results",
        adversary_position="Formation is more productive than DST indicates; permeability is higher; skin is lower; test duration was insufficient",
        counter_arguments=[
            "DST flow rate unrepresentative - formation damaged by drilling fluid invasion",
            "Shut-in period too short - radial flow not achieved, k and s unreliable",
            "Packer leaked during test - measured pressure lower than true formation pressure",
            "Cushion fluid effects not properly accounted for in pressure analysis",
            "Gas shows in DST could be drilling fluid gas-cut, not formation gas"
        ],
        resolution_strategy="Compare DST permeability to core analysis and log-derived permeability. Run multiple DST flow-buildup cycles to confirm consistency. Analyze recovered fluid samples for formation fluid vs mud filtrate. Use wireline formation tester (MDT/RFT) for additional pressure measurements. Drill and complete if DST positive; run additional logs or sidetrack if DST marginal.",
        entity_scope="Exploration and appraisal wells - temporary well testing during drilling",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="DST is snapshot test during drilling, often affected by damage and short test duration - confirm with full well test after completion if economic"
    ),

    DoctrineBlock(
        topic="type_curve_matching_methodology",
        keywords=["type curve", "dimensionless", "wellbore storage", "CDe2s", "match point", "gringarten", "bourdet", "derivative matching"],
        conclusion_template=[
            "Type curve matching overlays field data on theoretical dimensionless pressure and derivative curves to identify flow regimes and extract reservoir parameters.",
            "Modern approach: match pressure AND derivative simultaneously on log-log plot to ensure unique interpretation of permeability, skin, and wellbore storage.",
            "Match point coordinates (tD, PD) relate to physical parameters: k = 141.2 qBμ/(h*PD/ΔP), t = tD*φμct*rw²/(0.000264*k)."
        ],
        reasoning_framework="""
        TYPE CURVE MATCHING WORKFLOW:

        STEP 1: PREPARE FIELD DATA
        - Calculate ΔP = Pi - Pwf (drawdown) or ΔP = Pws - Pwf (buildup)
        - Calculate Δt = time since rate change
        - Compute Bourdet derivative dΔP/d(ln Δt)
        - Plot ΔP and derivative vs Δt on log-log transparent overlay

        STEP 2: SELECT TYPE CURVE FAMILY
        - Wellbore storage + skin: Gringarten et al. 1979 (CDe²s curves)
        - Fractured well: Cinco-Ley, finite-conductivity fracture
        - Dual porosity: Warren-Root, De Swaan
        - Horizontal well: Goode-Thambynayagam
        - Bounded reservoir: Earlougher finite reservoir shapes

        STEP 3: MATCH DERIVATIVE FIRST
        - Overlay derivative on type curve derivative
        - Match derivative shape - critical for flow regime identification
        - Derivative is less affected by wellbore storage than pressure
        - Achieves unique match if all flow regimes present

        STEP 4: MATCH PRESSURE CURVE
        - With derivative fixed, slide pressure to match type curve pressure
        - Pressure and derivative must both match on SAME type curve (same CDe²s)
        - Verify match quality across all time periods

        STEP 5: READ MATCH POINT
        - Choose convenient match point (often tD = 1, PD = 1)
        - Read corresponding field values (Δt_match, ΔP_match)
        - Record CDe²s value from matched curve

        STEP 6: CALCULATE PARAMETERS
        Permeability: k = 141.2 * q*B*μ / (h * PD/ΔP)|match [md]
        Wellbore storage: C = 0.000295 * k*h * (tD/Δt)|match / (φμct) [bbl/psi]
        Skin: s = 0.5 * ln(CD*e²s / CD) where CD calculated from C

        DIMENSIONLESS GROUPS:
        - tD = 0.000264*k*t / (φμct*rw²) = dimensionless time
        - PD = kh*ΔP / (141.2*q*B*μ) = dimensionless pressure
        - CD = 0.8936*C / (φct*h*rw²) = dimensionless wellbore storage
        - CDe²s = combined wellbore storage-skin group

        VALIDATION CHECKS:
        - Does matched CDe²s value make sense for well configuration?
        - Is calculated C consistent with wellbore volume?
        - Does skin value agree with completion quality expectations?
        - Are pressure and derivative overlays consistent throughout test?
        """,
        key_factors=[
            "Data quality - noise in derivative reduces match uniqueness",
            "Flow regime diversity - more regimes = better constrained match",
            "Type curve family selection (must match reservoir physics)",
            "Match point selection (arbitrary but must be consistent)",
            "Dimensionless group calculations accuracy (B, μ, ct, φ)",
            "Wellbore radius rw (often uncertain - use caliper log)",
            "Rate normalization for variable-rate history",
            "Pressure gauge drift or calibration errors"
        ],
        primary_authority=[
            "Gringarten et al. 1979 SPE 8205 - wellbore storage and skin type curves",
            "Bourdet 1983 - use of derivative in type curve matching",
            "Earlougher 1977 - comprehensive type curve catalog",
            "SPE Reprint Series: Type Curve Analysis in Well Testing"
        ],
        burden_holder="Well test analyst - prove type curve match is unique and parameters reliable",
        adversary_position="Type curve match is non-unique; multiple parameter sets fit data equally; permeability and skin uncertain",
        counter_arguments=[
            "Pressure matches but derivative does not - inconsistent interpretation",
            "Multiple type curve families match data equally well (e.g., dual porosity vs heterogeneous single porosity)",
            "Wellbore storage coefficient C calculated from match does not agree with wellbore volume",
            "Skin factor from match unrealistic (e.g., s = -20 in unstimulated well)",
            "Match point selection arbitrary - different match point yields different k"
        ],
        resolution_strategy="Require simultaneous pressure and derivative match on same type curve. Validate C against wellbore geometry. Cross-check k and s with independent analysis (Horner, MDH). Use automated computer matching (e.g., Ecrin, Saphir) for objective parameter estimation. Run sensitivity analysis - vary match point and check parameter stability.",
        entity_scope="All well tests - buildup, drawdown, injection, interference",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Type curve matching is most reliable when derivative clearly defines flow regimes and both pressure and derivative overlay consistently"
    ),

    # Additional doctrine blocks for comprehensive coverage

    DoctrineBlock(
        topic="superposition_principles",
        keywords=["superposition", "variable rate", "rate normalization", "convolution", "deconvolution", "rate history"],
        conclusion_template=[
            "Superposition principle allows analysis of variable-rate well tests by summing individual constant-rate pressure responses.",
            "For variable-rate history, normalize pressure by current rate to collapse data onto equivalent constant-rate response.",
            "Deconvolution removes rate history effects from pressure data, extracting constant-rate response for type curve analysis."
        ],
        reasoning_framework="""
        SUPERPOSITION THEORY:
        - Linear systems: total pressure response = sum of individual rate change responses
        - ΔP(t) = Σ Δqi * Pd(t - ti) where Δqi = rate change at time ti
        - Allows variable-rate test interpretation using constant-rate solutions

        RATE NORMALIZATION:
        - Divide pressure by current rate: ΔP/q plots as if constant-rate test
        - Material balance time: tmb = Np/q (cumulative production / current rate)
        - Superposition time: tsa = Σ (Δqi/q) * Δti

        DECONVOLUTION ALGORITHMS:
        - Extract unit-rate pressure response pd(t) from variable-rate data
        - Removes rate history artifacts, reveals true reservoir response
        - Enables type curve matching even for complex rate histories
        - Algorithms: von Schroeter, Levitan-Crawford, Ilk
        """,
        key_factors=[
            "Rate measurement accuracy throughout test history",
            "Pressure gauge resolution and noise level",
            "Deconvolution algorithm stability (ill-posed problem)",
            "Regularization parameter selection",
            "Validation against constant-rate periods if available"
        ],
        primary_authority=[
            "Van Everdingen-Hurst 1949 - superposition in transient flow",
            "Von Schroeter et al. 2004 SPE 77688 - deconvolution algorithms",
            "Levitan-Crawford 2000 - automated well test deconvolution"
        ],
        burden_holder="Analyst - demonstrate deconvolved response is physical and reliable",
        adversary_position="Deconvolution introduces artifacts; rate normalization insufficient for complex history",
        counter_arguments=[
            "Deconvolution amplifies noise if regularization too weak",
            "Rate history incomplete or inaccurate - garbage in, garbage out",
            "Non-uniqueness in deconvolution solution"
        ],
        resolution_strategy="Validate deconvolution with forward convolution check. Compare to constant-rate period if available. Use multiple algorithms for cross-validation.",
        entity_scope="Wells with variable-rate production or injection history",
        confidence=ConfidenceLevel.AGGRESSIVE
    ),

    DoctrineBlock(
        topic="multi_rate_testing",
        keywords=["multi-rate test", "step-rate", "isochronal", "modified isochronal", "deliverability", "AOF", "non-darcy flow"],
        conclusion_template=[
            "Multi-rate tests measure well performance at several flow rates to determine deliverability curve and absolute open flow (AOF) potential.",
            "Step-rate test: sequential flow periods at increasing rates with short shut-ins between. Used for fracture pressure determination and deliverability.",
            "Isochronal test: equal-duration flow periods at different rates with long shut-in to constant pressure between. Eliminates transient effects in deliverability analysis."
        ],
        reasoning_framework="""
        MULTI-RATE TEST TYPES:

        STEP-RATE TEST:
        - Flow at rate q1 for time t, shut in briefly
        - Flow at rate q2 > q1 for time t, shut in
        - Continue for 3-5 rate steps
        - Plot Pwf vs q - curvature indicates deliverability relationship
        - Used for gas well deliverability and fracture gradient determination

        ISOCHRONAL TEST (gas wells):
        - Flow at q1 for time t, shut in to initial pressure
        - Flow at q2 for time t, shut in to initial pressure
        - Repeat for 3-4 rates, then extended flow at final rate
        - Plot (P² - Pwf²) vs q on log-log - slope n determines deliverability exponent
        - AOF calculated from deliverability equation: q = C*(P² - Pwf²)^n

        MODIFIED ISOCHRONAL TEST:
        - Same as isochronal but shorter shut-in (not to initial pressure)
        - Faster test, but requires transient correction
        - Use same-duration flow periods to minimize transient effects

        DELIVERABILITY ANALYSIS:
        - Darcy flow: (P² - Pwf²) ∝ q (linear, n = 1)
        - Non-Darcy flow: includes turbulence term, n < 1 (typically 0.5 - 0.9)
        - Deliverability equation: q = C*(Pr² - Pwf²)^n or q = a*ΔP + b*ΔP²
        - AOF: flow rate at Pwf = atmospheric pressure
        """,
        key_factors=[
            "Rate stabilization at each step (need steady-state pwf)",
            "Shut-in duration between steps (longer = more accurate)",
            "Number of rate steps (minimum 3, prefer 4-5)",
            "Rate range (should span expected operating range)",
            "Pressure measurement accuracy at high rates (turbulence effects)",
            "Non-Darcy flow coefficient D determination",
            "Liquid loading effects in gas wells"
        ],
        primary_authority=[
            "Rawlins-Schellhardt 1935 - gas well deliverability",
            "Jones 1961 - isochronal testing method",
            "SPE Gas Reservoir Engineering textbook"
        ],
        burden_holder="Production engineer - determine well's sustainable production rate and AOF",
        adversary_position="Well can produce at higher rate than multi-rate test indicates; AOF is higher; non-Darcy effects overstated",
        counter_arguments=[
            "Transient effects not fully stabilized - AOF overestimated",
            "Liquid loading during test reduced rates - not representative of dry gas production",
            "Turbulence coefficient D varies with rate - single value inadequate",
            "Fracture closure at high rates reduces deliverability"
        ],
        resolution_strategy="Ensure adequate stabilization time at each rate. Validate deliverability curve with production history matching. Check for non-Darcy effects consistency across all rates. Use PLT to verify uniform inflow.",
        entity_scope="Gas wells, high-rate oil wells, injection wells",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="permeability_estimation_methods",
        keywords=["permeability", "horner slope", "derivative plateau", "radius of investigation", "flow capacity", "kh product"],
        conclusion_template=[
            "Permeability k from Horner slope m: k = 162.6*qBμ/(m*h) [md]. Requires clear middle-time region straight line.",
            "Permeability from derivative plateau: k = 70.6*qBμ/(h*derivative_value) [md]. More robust to wellbore storage and boundaries.",
            "Flow capacity kh product more reliable than k alone - independent of net pay uncertainty."
        ],
        reasoning_framework="""
        PERMEABILITY CALCULATION METHODS:

        FROM HORNER PLOT (semilog analysis):
        - Plot Pws vs log[(tp+Δt)/Δt]
        - Slope m from straight line (MTR)
        - k = 162.6 * q*B*μ / (m * h) [md]
        - Advantage: traditional, widely used
        - Disadvantage: requires clear MTR, sensitive to wellbore storage

        FROM DERIVATIVE PLATEAU (log-log analysis):
        - Identify radial flow plateau on derivative plot
        - Read derivative value at plateau: der = ΔP'
        - k = 70.6 * q*B*μ / (h * der) [md]
        - Advantage: more robust, less affected by storage
        - Disadvantage: requires high-quality derivative, noise-free

        FROM TYPE CURVE MATCH:
        - Match pressure and derivative to type curves
        - k = 141.2 * q*B*μ / (h * PD/ΔP)|match [md]
        - Advantage: handles complex behavior (storage, skin, boundaries)
        - Disadvantage: non-unique if poor match

        FLOW CAPACITY kh:
        - Always report kh product [md-ft] in addition to k [md]
        - kh independent of net pay thickness uncertainty
        - More reliable for comparison between wells
        - Used directly in reservoir simulation

        RADIUS OF INVESTIGATION:
        - At any time t: ri = sqrt(0.000264*k*t / φμct) [ft]
        - Volume investigated: V = π*ri²*h*φ
        - Area investigated: A = π*ri²
        - Important for understanding test support volume
        """,
        key_factors=[
            "Net pay thickness h uncertainty (logs vs core vs petrophysics)",
            "Fluid properties B, μ at test conditions (PVT accuracy)",
            "Formation compressibility ct (often poorly known)",
            "Rate measurement accuracy q",
            "Porosity φ from logs or core",
            "Flow regime identification (must be infinite-acting radial)",
            "Permeability anisotropy kh vs kv",
            "Scale of permeability (test samples larger volume than core plug)"
        ],
        primary_authority=[
            "Matthews-Brons-Hazebroek 1954 - pressure buildup theory",
            "Horner 1951 - semilog analysis method",
            "Bourdet 1983 - derivative-based permeability"
        ],
        burden_holder="Reservoir engineer - justify permeability value and uncertainty range",
        adversary_position="Permeability is higher than calculated; net pay thicker; test sampled only low-k damaged zone",
        counter_arguments=[
            "Permeability from test is effective average over large volume - local core plugs may be higher or lower",
            "Anisotropy not accounted for - horizontal test yields kh, vertical test yields kv",
            "Partial penetration correction not applied - test k lower than true k",
            "Multiphase flow corrections (relative permeability) not applied - calculated k is effective, not absolute"
        ],
        resolution_strategy="Report kh product and estimated k separately with uncertainty. Cross-validate with core permeability (geometric mean of plugs). Check against production performance (flow rate vs drawdown). Use reservoir simulation to history match test and production.",
        entity_scope="All well tests - primary objective is permeability determination",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="pressure_derivative_diagnostic_features",
        keywords=["derivative signature", "flow regime", "log-log diagnostic", "plateau", "slope", "hump", "valley"],
        conclusion_template=[
            "Derivative diagnostic features uniquely identify flow regimes without ambiguity from semilog plots.",
            "Key signatures: unit slope (wellbore storage), flat plateau (radial flow), 1/2 slope (linear flow), 1/4 slope (bilinear flow), hump-valley (dual porosity).",
            "Derivative timing and magnitude provide flow regime duration and formation property estimates independent of pressure curve alone."
        ],
        reasoning_framework="""
        DERIVATIVE SIGNATURE CATALOG:

        WELLBORE STORAGE:
        - Derivative = 0.5 * pressure (unit slope on log-log)
        - Duration: tws,end = (60+3.5*s)*C/(kh)
        - Diagnostic: derivative and pressure both on 45° line

        INFINITE-ACTING RADIAL FLOW:
        - Derivative flat (horizontal plateau)
        - Derivative value = 0.5 * m (semilog slope)
        - k = 70.6*qBμ/(h*derivative_value)
        - Diagnostic: pressure half-slope, derivative flat

        LINEAR FLOW (fractures, channels):
        - Derivative 1/2 slope (log-log)
        - Pressure 1/2 slope (log-log)
        - xf = 0.01 * sqrt(k*t*derivative_slope) for fracture half-length
        - Diagnostic: both pressure and derivative parallel 1/2 slope

        BILINEAR FLOW (finite-conductivity fracture):
        - Derivative 1/4 slope (log-log)
        - Pressure 1/4 slope (log-log)
        - Indicates finite-conductivity hydraulic fracture
        - Diagnostic: both pressure and derivative parallel 1/4 slope

        DUAL POROSITY (naturally fractured):
        - Early radial flow plateau (fracture system)
        - Valley (dip to minimum)
        - Late radial flow plateau (total system, higher than early)
        - Valley depth ∝ ω (storativity ratio)
        - Valley timing ∝ 1/λ (interporosity flow)

        SEALING BOUNDARY:
        - Derivative doubles from radial plateau
        - Then unit slope (pseudosteady state)
        - Distance L = 0.01217*sqrt(kt/φμct) at boundary start
        - Diagnostic: derivative doubles, then parallel to storage line

        CONSTANT PRESSURE BOUNDARY:
        - Derivative drops from radial plateau toward zero
        - Indicates recharge or pressure support
        - Diagnostic: derivative downturn after radial flow
        """,
        key_factors=[
            "Derivative smoothing parameter L (0.1-0.3 typical)",
            "Data noise level - affects derivative quality",
            "Sampling frequency - need high-frequency data for good derivative",
            "Pressure gauge resolution - poor resolution = noisy derivative",
            "Test duration - need to reach diagnostic flow regime",
            "Rate stability - variable rate degrades derivative",
            "Multiple flow regime transitions - more regimes = better diagnosis"
        ],
        primary_authority=[
            "Bourdet et al. 1983 SPE 12777 - derivative diagnostic features",
            "Horne 1995 - comprehensive derivative interpretation",
            "Gringarten 1987 - type curve derivative matching"
        ],
        burden_holder="Analyst - identify flow regimes from derivative and extract parameters",
        adversary_position="Derivative features are noise or artifacts; flow regime not truly established; interpretation over-fit to noisy data",
        counter_arguments=[
            "Derivative smoothing obscures real reservoir features",
            "Plateau not truly flat - slight upward trend indicates boundary approaching",
            "Valley attributed to dual porosity could be transition from wellbore storage to radial flow",
            "1/2 slope misidentified - actually transition between regimes, not true linear flow"
        ],
        resolution_strategy="Use multiple smoothing parameters to confirm derivative features are real. Validate flow regime timing against reservoir dimensions and properties. Compare derivative-based parameters with pressure-based analysis (Horner, MDH). Use type curve matching to confirm flow regime sequence.",
        entity_scope="All well tests - derivative is universal diagnostic tool",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="test_design_and_duration",
        keywords=["test design", "duration", "gauge placement", "rate stabilization", "shut-in time", "radius of investigation", "flow regime"],
        conclusion_template=[
            "Well test design determines success: proper gauge placement, adequate flow/shut-in duration, rate stabilization, and data acquisition frequency are critical.",
            "Minimum shut-in time for buildup: until radial flow achieved. Rule of thumb: tmin = 10*C/(kh) or until derivative plateau observed.",
            "Test duration must achieve objectives: permeability requires radial flow (hours to days), boundaries require long tests (days to months)."
        ],
        reasoning_framework="""
        TEST DESIGN CHECKLIST:

        OBJECTIVES:
        1. Permeability k, skin s → need radial flow period
        2. Boundaries, reservoir size → need long test, boundary-dominated flow
        3. Dual porosity parameters → need both fracture and total system radial flow
        4. Anisotropy → need horizontal well test or interference test
        5. Deliverability → need multi-rate test or extended drawdown

        GAUGE SELECTION AND PLACEMENT:
        - Resolution: 0.01 psi or better (0.001 psi for low-permeability or long distances)
        - Accuracy: ±0.1% of reading or better
        - Sampling rate: 1 sample/second minimum (10/second preferred)
        - Placement: bottomhole (downhole shut-in preferable to surface)
        - Redundancy: 2 gauges for critical tests

        FLOW PERIOD DURATION:
        - Stabilization: rate constant ±2%, pressure declining steadily
        - For buildup analysis: tp > 2-4 times planned shut-in time
        - For drawdown analysis: until pseudosteady state (if bounded reservoir)
        - For multi-rate: each rate step long enough for stabilized pwf

        SHUT-IN DURATION:
        - Minimum: until wellbore storage ends and radial flow achieved
        - tmin = 10 * C / (k*h) [hours] or until derivative plateau seen
        - For boundaries: until derivative departure from radial plateau
        - For average pressure: tp/(Δt) < 1 to 10 (Horner extrapolation validity)
        - Practical: hours to days for high-k, days to weeks for low-k

        RATE MANAGEMENT:
        - Constant rate critical for interpretation
        - Minimize rate fluctuations: ±2% or better
        - Use downhole flow control if surface fluctuations unavoidable
        - Record rate continuously with high accuracy (±1%)

        DATA ACQUISITION:
        - Pressure: continuous, high-frequency (1-10 Hz)
        - Rate: continuous, ±1% accuracy
        - Temperature: useful for flow regime identification
        - Flowing pressure: both buildup and drawdown analysis
        - Fluid samples: representative formation fluid, not mud filtrate

        RADIUS OF INVESTIGATION:
        - Time to investigate to radius r: t = 948*φμct*r²/k [hours]
        - For r = 100 ft, typical: t = 1 hour (k=100md) to 100 hours (k=1md)
        - Area investigated A = π*ri² increases with time
        - Test duration sets volume of reservoir sampled
        """,
        key_factors=[
            "Estimated permeability range (affects test duration)",
            "Expected wellbore storage C (affects minimum shut-in time)",
            "Reservoir boundaries distance (affects test duration for boundary detection)",
            "Gauge selection and calibration",
            "Rate control capability (surface vs downhole)",
            "Cost vs benefit (rig time, lost production)",
            "Safety considerations (well control, H2S, high pressure)",
            "Data quality requirements (noise tolerance)"
        ],
        primary_authority=[
            "SPE Monograph: Well Test Design and Analysis (Earlougher)",
            "API RP-90 Recommended Practice for Well Testing",
            "Horne 1995 Chapter 2 - Test Design",
            "Lee-Rollins-Spivey: Pressure Transient Testing (SPE Textbook)"
        ],
        burden_holder="Test engineer - design test to meet objectives within time and cost constraints",
        adversary_position="Test duration was insufficient; radial flow not achieved; permeability and skin unreliable due to short test",
        counter_arguments=[
            "Wellbore storage did not end - radial flow never achieved despite multi-day test",
            "Gauge resolution insufficient - derivative too noisy for flow regime identification",
            "Rate variations during test invalidated constant-rate assumption",
            "Test stopped too early due to rig constraints - boundaries not reached",
            "Gauge drift or calibration error - measured pressure unreliable"
        ],
        resolution_strategy="Perform pre-test simulation to estimate required duration. Monitor derivative in real-time to confirm radial flow achieved. Extend test if objectives not met. Use high-quality gauges and rate measurement. Validate data quality before ending test. Post-test: deconvolution if rate varied, type curve matching if short test.",
        entity_scope="All well tests - design determines quality and interpretability",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Proper test design is more important than sophisticated analysis - garbage in, garbage out"
    )
]

# ============================================================================
# TELEMETRY
# ============================================================================

class Telemetry:
    def __init__(self):
        self.query_count = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.response_times: List[float] = []
        self.error_count = 0
        self.start_time = time.time()
        self.category_counts: Dict[str, int] = defaultdict(int)

    def record_query(self, duration_ms: float, cache_hit: bool, categories: List[str]):
        self.query_count += 1
        self.response_times.append(duration_ms)
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        for cat in categories:
            self.category_counts[cat] += 1

    def record_error(self):
        self.error_count += 1

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_queries": self.query_count,
            "cache_hit_rate": self.cache_hits / max(1, self.query_count),
            "avg_response_time_ms": sum(self.response_times) / max(1, len(self.response_times)),
            "error_count": self.error_count,
            "uptime_seconds": time.time() - self.start_time,
            "category_distribution": dict(self.category_counts)
        }

telemetry = Telemetry()

# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

def semantic_normalize(text: str) -> str:
    """Normalize domain-specific terminology for consistent matching"""
    text = text.lower()

    # Well testing term normalization
    replacements = {
        "pressure buildup": "buildup",
        "pressure build-up": "buildup",
        "horner plot": "horner",
        "horner analysis": "horner",
        "bourdet derivative": "derivative",
        "pressure derivative": "derivative",
        "formation damage": "skin damage",
        "near-wellbore damage": "skin damage",
        "hydraulic fracture": "fracture",
        "frac": "fracture",
        "naturally fractured": "dual porosity",
        "dual-porosity": "dual porosity",
        "warren-root": "dual porosity",
        "sealing fault": "boundary",
        "no-flow boundary": "boundary",
        "constant pressure boundary": "boundary",
        "type curve": "type curve matching",
        "rta": "rate transient analysis",
        "blasingame": "rate transient analysis",
        "flowing material balance": "rate transient analysis",
        "fmb": "rate transient analysis",
        "horizontal well": "horizontal well testing",
        "interference test": "interference",
        "pulse test": "pulse testing",
        "dst": "drill stem test",
        "mdt": "formation testing",
        "rft": "formation testing",
        "wireline formation test": "formation testing",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text

def calculate_determinism_hash(text: str) -> str:
    """Generate SHA-256 hash for response reproducibility"""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]

def match_doctrines(question: str) -> List[DoctrineBlock]:
    """Match question to relevant doctrine blocks using keyword and semantic matching"""
    question_norm = semantic_normalize(question)
    question_words = set(question_norm.split())

    scored_doctrines = []
    for doctrine in DOCTRINE_CACHE:
        # Keyword matching
        keyword_matches = sum(1 for kw in doctrine.keywords if kw in question_norm)

        # Topic matching
        topic_match = 2 if doctrine.topic.replace('_', ' ') in question_norm else 0

        # Word overlap
        doctrine_words = set(' '.join(doctrine.keywords).split())
        word_overlap = len(question_words & doctrine_words)

        score = keyword_matches * 3 + topic_match + word_overlap

        if score > 0:
            scored_doctrines.append((score, doctrine))

    # Sort by score descending and return top matches
    scored_doctrines.sort(reverse=True, key=lambda x: x[0])
    return [d for _, d in scored_doctrines[:5]]  # Return top 5 matches

def build_reasoning_chain(doctrines: List[DoctrineBlock], question: str) -> List[str]:
    """Construct step-by-step reasoning chain from triggered doctrines"""
    chain = [
        f"QUESTION ANALYSIS: {question[:200]}",
        f"DOCTRINE BLOCKS TRIGGERED: {len(doctrines)} relevant doctrines identified"
    ]

    for i, doctrine in enumerate(doctrines, 1):
        chain.append(f"DOCTRINE {i} ({doctrine.topic}): {doctrine.reasoning_framework[:300]}...")

    return chain

def synthesize_answer(doctrines: List[DoctrineBlock], question: str, mode: ResponseMode) -> str:
    """Generate final answer based on triggered doctrines and response mode"""
    if not doctrines:
        return "No specific doctrine blocks matched this well testing question. Please provide more details about the test type, flow regimes, or analysis objectives."

    primary = doctrines[0]

    if mode == ResponseMode.FAST:
        # Concise answer from primary doctrine
        answer = f"{primary.conclusion_template[0]} "
        if len(doctrines) > 1:
            answer += f"{doctrines[1].conclusion_template[0]}"
        return answer

    elif mode == ResponseMode.DEFENSE:
        # Detailed, audit-ready answer with full reasoning
        parts = [
            "WELL TESTING ANALYSIS:",
            "",
            "PRIMARY INTERPRETATION:",
            f"{primary.conclusion_template[0]}",
            f"{primary.conclusion_template[1] if len(primary.conclusion_template) > 1 else ''}",
            "",
            "TECHNICAL FRAMEWORK:",
            primary.reasoning_framework[:800],
            "",
            "KEY FACTORS:",
            "\n".join(f"- {factor}" for factor in primary.key_factors[:8]),
            "",
            "SUPPORTING AUTHORITY:",
            "\n".join(f"- {auth}" for auth in primary.primary_authority),
        ]

        if len(doctrines) > 1:
            parts.extend([
                "",
                "ADDITIONAL CONSIDERATIONS:",
                f"{doctrines[1].topic.upper()}: {doctrines[1].conclusion_template[0]}"
            ])

        return "\n".join(parts)

    else:  # MEMO mode
        # Comprehensive technical memorandum
        parts = [
            "TECHNICAL MEMORANDUM",
            "WELL TESTING & PRESSURE TRANSIENT ANALYSIS",
            "=" * 70,
            "",
            "EXECUTIVE SUMMARY:",
            primary.conclusion_template[0],
            "",
            "DETAILED ANALYSIS:",
            ""
        ]

        for i, doctrine in enumerate(doctrines[:3], 1):
            parts.extend([
                f"{i}. {doctrine.topic.upper().replace('_', ' ')}",
                "",
                "CONCLUSION:",
                "\n".join(f"  {line}" for line in doctrine.conclusion_template),
                "",
                "TECHNICAL FRAMEWORK:",
                doctrine.reasoning_framework,
                "",
                "CRITICAL FACTORS:",
                "\n".join(f"  - {factor}" for factor in doctrine.key_factors),
                "",
                "AUTHORITATIVE BASIS:",
                "\n".join(f"  - {auth}" for auth in doctrine.primary_authority),
                "",
                "ADVERSARIAL ANALYSIS:",
                f"  Opposing Position: {doctrine.adversary_position}",
                f"  Counter-Arguments:",
                "\n".join(f"    - {arg}" for arg in doctrine.counter_arguments[:5]),
                "",
                "RESOLUTION STRATEGY:",
                f"  {doctrine.resolution_strategy}",
                "",
                "-" * 70,
                ""
            ])

        return "\n".join(parts)

def apply_epistemic_guardrails(answer: str, doctrines: List[DoctrineBlock]) -> Tuple[str, Optional[str]]:
    """Apply epistemic safety checks and generate disclosure if needed"""
    # Check for high-risk interpretations
    high_risk_terms = [
        "guaranteed", "certain", "proven", "absolute", "definitive",
        "without doubt", "unquestionably", "indisputable"
    ]

    disclosure = None
    if any(term in answer.lower() for term in high_risk_terms):
        disclosure = "EPISTEMIC DISCLOSURE: Well test interpretation involves uncertainty in reservoir parameters, fluid properties, and model assumptions. Results should be validated with independent data sources (core analysis, production history, reservoir simulation)."

    # Check confidence levels of triggered doctrines
    risk_levels = [d.confidence for d in doctrines]
    if ConfidenceLevel.HIGH_RISK in risk_levels or ConfidenceLevel.AGGRESSIVE in risk_levels:
        if not disclosure:
            disclosure = "INTERPRETATION NOTICE: This analysis involves aggressive assumptions or non-unique solutions. Recommend cross-validation with offset well data, reservoir simulation, and geologic model."

    return answer, disclosure

# ============================================================================
# API ENDPOINTS
# ============================================================================

app = FastAPI(title=ENGINE_NAME, version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=Dict[str, str])
async def root():
    """Engine information endpoint"""
    return {
        "engine": ENGINE_ID,
        "name": ENGINE_NAME,
        "version": VERSION,
        "status": "operational",
        "domain": "Production Engineering - Well Testing & Pressure Transient Analysis"
    }

@app.get("/health", response_model=HealthResponse)
async def health():
    """Comprehensive health check with statistics"""
    stats = telemetry.get_stats()
    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        doctrine_count=len(DOCTRINE_CACHE),
        uptime_seconds=stats["uptime_seconds"],
        total_queries=stats["total_queries"],
        cache_hit_rate=stats["cache_hit_rate"],
        avg_response_time_ms=stats["avg_response_time_ms"]
    )

@app.post("/query", response_model=AnalysisResponse)
async def query_engine(request: QueryRequest):
    """
    Main query endpoint for well testing analysis

    Performs three-layer analysis:
    1. Doctrine cache matching (fast, <200ms)
    2. Semantic reasoning (detailed analysis)
    3. Epistemic validation and disclosure
    """
    start_time = time.time()

    try:
        logger.info(f"Query received: {request.question[:100]}... | Mode: {request.mode} | Zone: {request.zone}")

        # Layer 1: Doctrine cache matching
        matched_doctrines = match_doctrines(request.question)
        cache_hit = len(matched_doctrines) > 0

        if not cache_hit:
            logger.warning(f"No doctrine matches for question: {request.question[:100]}")
            telemetry.record_query((time.time() - start_time) * 1000, False, [])
            raise HTTPException(
                status_code=404,
                detail="No relevant doctrine blocks found. Please refine question to focus on specific well testing topics."
            )

        # Layer 2: Reasoning chain construction
        reasoning_chain = build_reasoning_chain(matched_doctrines, request.question)

        # Layer 3: Answer synthesis based on mode
        answer = synthesize_answer(matched_doctrines, request.question, request.mode)

        # Extract key factors and counter-arguments
        key_factors = []
        counter_arguments = []
        for doctrine in matched_doctrines[:2]:
            key_factors.extend(doctrine.key_factors[:5])
            counter_arguments.extend(doctrine.counter_arguments[:3])

        # Apply epistemic guardrails
        answer, disclosure = apply_epistemic_guardrails(answer, matched_doctrines)

        # Determine overall confidence
        confidence_levels = [d.confidence for d in matched_doctrines]
        if ConfidenceLevel.HIGH_RISK in confidence_levels:
            confidence = ConfidenceLevel.HIGH_RISK
        elif ConfidenceLevel.AGGRESSIVE in confidence_levels:
            confidence = ConfidenceLevel.AGGRESSIVE
        elif ConfidenceLevel.DISCLOSURE in confidence_levels:
            confidence = ConfidenceLevel.DISCLOSURE
        else:
            confidence = ConfidenceLevel.DEFENSIBLE

        # Generate determinism hash
        hash_input = answer + str(matched_doctrines[0].topic) + request.mode.value
        determinism_hash = calculate_determinism_hash(hash_input)

        # Record telemetry
        categories = [d.topic for d in matched_doctrines]
        duration_ms = (time.time() - start_time) * 1000
        telemetry.record_query(duration_ms, cache_hit, categories)

        logger.info(f"Query completed in {duration_ms:.2f}ms | Confidence: {confidence} | Doctrines: {len(matched_doctrines)}")

        return AnalysisResponse(
            answer=answer,
            confidence=confidence,
            doctrine_blocks_triggered=[d.topic for d in matched_doctrines],
            reasoning_chain=reasoning_chain,
            key_factors=key_factors,
            counter_arguments=counter_arguments,
            epistemic_disclosure=disclosure,
            determinism_hash=determinism_hash,
            timestamp=datetime.utcnow().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        telemetry.record_error()
        raise HTTPException(status_code=500, detail=f"Internal engine error: {str(e)}")

@app.get("/doctrines", response_model=List[Dict[str, Any]])
async def list_doctrines():
    """List all available doctrine blocks with metadata"""
    return [
        {
            "topic": d.topic,
            "keywords": d.keywords,
            "confidence": d.confidence,
            "entity_scope": d.entity_scope,
            "primary_authority": d.primary_authority[:2]  # First 2 authorities
        }
        for d in DOCTRINE_CACHE
    ]

@app.get("/stats", response_model=Dict[str, Any])
async def get_statistics():
    """Retrieve engine usage statistics"""
    return telemetry.get_stats()

# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting {ENGINE_NAME} v{VERSION}")
    logger.info(f"Doctrine blocks loaded: {len(DOCTRINE_CACHE)}")
    logger.info(f"Listening on port {PORT}")

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
