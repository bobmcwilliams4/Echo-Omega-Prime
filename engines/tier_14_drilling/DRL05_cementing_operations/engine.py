"""
DRL05 - Cementing Operations Intelligence Engine
ECHO OMEGA PRIME - Drilling Engineering Domain

Port: 9015
TIE Gold Standard: Real cementing expertise, NOT line count padding
Authority: API Spec 10A, ISO 10426, Well Cementing (Schlumberger)

Covers: Portland cement classes, slurry design, additives, primary cementing,
cement evaluation, remedial operations, HPHT, foam cement, gas migration
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
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# Configure loguru
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "logs" / "drl05_cementing_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)


# ============================================================================
# ENUMS & MODELS
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


class IssueCategory(str, Enum):
    SLURRY_DESIGN = "SLURRY_DESIGN"
    PRIMARY_CEMENTING = "PRIMARY_CEMENTING"
    REMEDIAL_CEMENTING = "REMEDIAL_CEMENTING"
    CEMENT_EVALUATION = "CEMENT_EVALUATION"
    ADDITIVES = "ADDITIVES"
    CONTAMINATION = "CONTAMINATION"
    GAS_MIGRATION = "GAS_MIGRATION"
    HPHT_OPERATIONS = "HPHT_OPERATIONS"
    LOST_CIRCULATION = "LOST_CIRCULATION"
    TESTING = "TESTING"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    EXECUTION = "EXECUTION"
    EVALUATION = "EVALUATION"


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=10, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    context: Dict[str, Any] = Field(default_factory=dict)
    max_depth: int = Field(default=3, ge=1, le=5)


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    doctrine_blocks_used: List[str]
    reasoning_chain: List[str]
    authorities: List[str]
    determinism_hash: str
    latency_ms: float
    coverage_gaps: List[str]
    response_mode: ResponseMode


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
    confidence_stratification: str
    controlling_precedent: str
    issue_category: IssueCategory
    zone: AnalysisZone


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrine_blocks: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float
    cache_hit_rate: float


# ============================================================================
# DOCTRINE CACHE - 25+ CEMENTING EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="API Cement Class Selection",
        keywords=["API", "class A", "class C", "class G", "class H", "cement type", "API Spec 10A"],
        conclusion_template=[
            "API Spec 10A defines Portland cement classes for oilwell applications.",
            "Class G and H are the most commonly used for oil and gas wells.",
            "Class selection depends on depth, temperature, and pressure conditions."
        ],
        reasoning_framework="""
API Spec 10A categorizes Portland cements into eight classes (A-H) based on sulfate resistance and application:
- **Class A**: General purpose, 0-6000 ft, available in Ordinary (O), Moderate (M), High (H) sulfate resistance
- **Class B**: Moderate sulfate resistance, 0-6000 ft, used where moderate to high sulfate resistance needed
- **Class C**: High early strength, 0-6000 ft, available in O, M, H sulfate resistance
- **Class D**: Moderate sulfate resistance, high temperature, 6000-10,000 ft, available in M, H
- **Class E**: High sulfate resistance, high temperature, 10,000-14,000 ft
- **Class F**: Extremely high sulfate resistance, high temperature, 10,000-16,000 ft
- **Class G**: Basic well cement, 0-8000 ft, can be used with accelerators/retarders, available in M, H
- **Class H**: Basic well cement, 0-8000 ft, slower hydration than G, available in M, H

**Class G and H are most versatile** - can be blended with additives for wide temperature/depth ranges.
Class G thickening time ~2.5-3.5 hr at 80°F (API), Class H ~3-4 hr at 80°F.

**Selection criteria**:
1. Depth/bottomhole temperature (BHT): deeper wells → Class G/H with retarders
2. Sulfate exposure: Class H (high sulfate resistance) preferred in sour zones
3. Strength development rate: Class C for surface/intermediate, Class G/H for production
4. Regulatory requirements: Some regions mandate Class H for specific zones
        """,
        key_factors=[
            "Well depth and bottomhole static temperature (BHST)",
            "Sulfate concentration in formation water",
            "Required thickening time for safe placement",
            "Compressive strength development schedule",
            "API Class H preferred for deeper, hotter wells"
        ],
        primary_authority=[
            "API Specification 10A - Cements and Materials for Well Cementing (2010)",
            "ISO 10426-1 - Petroleum and natural gas industries - Cements and materials for well cementing - Part 1: Specification (2009)",
            "API RP 10B-2 - Recommended Practice for Testing Well Cements (2013)"
        ],
        burden_holder="Operator",
        adversary_position="Using incorrect cement class risks poor bonding, insufficient strength, or premature setting",
        counter_arguments=[
            "Class A/C may be adequate for shallow wells with proper additives",
            "Blended cements can outperform straight API classes in specific applications",
            "Economic considerations favor Class A where suitable",
            "Some service companies recommend proprietary blends over API classes"
        ],
        resolution_strategy="Conduct API thickening time and compressive strength tests at anticipated BHST and BHCT, verify sulfate resistance rating matches formation water chemistry, document Class selection rationale in cementing program",
        entity_scope="Oil and gas operators, service companies, regulatory agencies",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API Spec 10A is authoritative industry standard; Class G/H selection defensible for 90%+ wells",
        controlling_precedent="API Spec 10A Section 3 - Classification and Requirements",
        issue_category=IssueCategory.SLURRY_DESIGN,
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Cement Slurry Density Design",
        keywords=["slurry density", "gel strength", "hydrostatic pressure", "lost circulation", "formation fracture"],
        conclusion_template=[
            "Slurry density must balance fracture pressure and mud weight windows.",
            "Typical range: 12.5-17.5 ppg for conventional wells, 9-12 ppg for lightweight systems.",
            "Excessive density causes lost circulation; insufficient density risks gas migration."
        ],
        reasoning_framework="""
Cement slurry density (ρ_cement) is the primary design parameter controlling:
1. **Hydrostatic pressure** during placement: P_h = 0.052 × ρ × TVD
2. **Annular fracture risk**: P_h + P_dynamic < P_fracture
3. **Gas migration prevention**: P_h > P_formation throughout gelation

**Design constraints**:
- **Lower bound**: Must exceed formation pore pressure (plus safety margin 0.5-1.0 ppg) to prevent influx during gelation when gel strength is low (<50 lbf/100ft²)
- **Upper bound**: Hydrostatic + ECD < formation fracture gradient (typically 0.8-0.95 × Frac Grad)
- **Typical densities**:
  * Surface/intermediate casing: 15.6-16.5 ppg (Class A/C + 35-38% silica flour)
  * Production casing: 15.8-17.5 ppg (Class H neat or with hematite)
  * Liners in depleted zones: 12.5-14.5 ppg (Class H + 20-40% perlite/cenospheres)
  * HPHT wells: 17-19 ppg (Class H + ilmenite/barite)

**Lightweight systems** (9-12 ppg) use extenders:
- **Perlite**: 9-13 ppg, high fluid loss, need strong fluid loss control
- **Cenospheres** (glass microspheres): 11-14 ppg, low permeability
- **Foamed cement**: 8-14 ppg, nitrogen/surfactant stabilized, complex rheology

**Weighting agents** for high density:
- **Hematite** (Fe2O3): up to 19 ppg, preferred over barite (no BaSO4 scaling)
- **Ilmenite** (FeTiO3): up to 19 ppg, acid-soluble
        """,
        key_factors=[
            "Formation fracture gradient at shoe and weaker zones",
            "Pore pressure profile with safety margin during gelation",
            "Mud weight to be displaced (density hierarchy)",
            "Risk of lost circulation vs gas migration",
            "Thickening time impact: lighter slurries set faster at same temperature"
        ],
        primary_authority=[
            "API RP 10B-2 - Recommended Practice for Testing Well Cements (2013) Section 6",
            "SPE 163043 - Cement Slurry Design for Gas Migration Prevention (2013)",
            "Well Cementing (Schlumberger 1991) Chapter 4 - Slurry Design"
        ],
        burden_holder="Operator and cementing service company (joint responsibility)",
        adversary_position="Density too high → lost circulation, poor mud displacement. Density too low → gas migration, annular pressure buildup.",
        counter_arguments=[
            "Heavier slurries provide better gas migration control",
            "Lost circulation can be mitigated with LCM or staged cementing",
            "Lightweight cement may have insufficient compressive strength",
            "Regulatory minimum density requirements in some jurisdictions"
        ],
        resolution_strategy="Plot slurry density against fracture gradient and pore pressure gradient. Verify ECD during displacement does not exceed 0.9 × Frac Grad. Confirm density hierarchy: ρ_lead_spacer < ρ_cement < ρ_tail_spacer (if used). Run gas migration risk assessment per SPE 163043.",
        entity_scope="Operators, service companies, well engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry consensus on density windows; specific values depend on formation properties",
        controlling_precedent="API RP 10B-2 density testing procedures; SPE gas migration models",
        issue_category=IssueCategory.SLURRY_DESIGN,
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Cement Additives - Retarders",
        keywords=["retarder", "thickening time", "BHCT", "lignosulfonate", "ANSA", "cellulose derivatives"],
        conclusion_template=[
            "Retarders extend thickening time for safe placement in high-temperature wells.",
            "Lignosulfonates are most common; concentration 0.1-2.0% BWOC.",
            "Thickening time must exceed pumping time by minimum 50% safety margin."
        ],
        reasoning_framework="""
**Retarders** slow cement hydration to extend thickening time (time to reach 70 Bc consistency per API RP 10B-2).

**Common retarder types**:
1. **Lignosulfonates** (e.g., D-65, HR-7, HR-12):
   - Most widely used, effective 100-230°F
   - Concentration: 0.1-1.0% BWOC (by weight of cement)
   - Mechanism: Adsorbs on cement particles, delays C3S/C2S hydration
   - Side effects: Increases fluid loss, reduces compressive strength ~10-15% at 24 hr

2. **Synthetic copolymers** (ANSA - aminomethylenephosphonate salts):
   - HPHT applications >230°F, up to 400°F
   - Concentration: 0.05-0.5% BWOC
   - Lower impact on strength vs lignosulfonates

3. **Cellulose derivatives** (hydroxyethylcellulose):
   - Dual retarder/fluid loss control
   - Concentration: 0.3-0.75% BWOC

4. **Organic acids** (citric acid, tartaric acid):
   - Low-temperature retardation (<120°F)
   - Concentration: 0.1-0.3% BWOC
   - Also reduce viscosity

**Design criteria**:
- **Thickening time** ≥ (Pumping time + 30 min mixing + displacement time) × 1.5 safety factor
- **API Schedule**: Test at BHCT (bottomhole circulating temperature), use API Schedule 7-9 depending on circulation time
- **Example**: 3 hr pumping + 1 hr displacement = 4 hr → require thickening time ≥ 6 hr at BHCT
- **Temperature impact**: Every 10°F increase reduces thickening time ~20-30% (Arrhenius relationship)

**Overdosing risk**: Excessive retarder (>2% lignosulfonate) can cause:
- "False set" - premature gelation then liquefaction
- Delayed strength development (>48 hr to reach 500 psi)
- Gas migration during prolonged liquid phase
        """,
        key_factors=[
            "Bottomhole circulating temperature (BHCT) from thermal modeling",
            "Total pumping time including displacement and safety margin",
            "API testing at proper temperature schedule and pressure",
            "Impact on compressive strength development",
            "Compatibility with other additives (fluid loss, dispersants)"
        ],
        primary_authority=[
            "API RP 10B-2 Section 7 - Thickening Time Testing",
            "API Spec 10A Section 7 - Requirements for Retarders",
            "SPE 148868 - High Temperature Retarders for HPHT Cementing (2011)"
        ],
        burden_holder="Service company (designs slurry), Operator (approves safety margin)",
        adversary_position="Insufficient retarder → premature setting, possible stuck pipe or poor mud displacement. Excessive retarder → prolonged transition time, gas migration.",
        counter_arguments=[
            "Higher retarder concentration provides additional safety margin",
            "Cooler-than-predicted BHCT could cause over-retardation",
            "Real-time thickening time monitoring can reduce safety margin",
            "Accelerated testing (higher temperature) provides conservative results"
        ],
        resolution_strategy="Conduct thickening time tests at BHCT ± 10°F. Verify thickening time ≥ 1.5 × total pumping time. Check 24-hr compressive strength ≥ 500 psi at BHCT. Document temperature profile used for test design.",
        entity_scope="Service companies, well engineers, laboratory technicians",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API testing protocols are industry standard; 1.5× safety margin is consensus practice",
        controlling_precedent="API RP 10B-2 thickening time procedures (Section 7)",
        issue_category=IssueCategory.ADDITIVES,
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Cement Additives - Fluid Loss Control",
        keywords=["fluid loss", "API fluid loss", "filtrate", "synthetic polymer", "CMHEC", "dehydration"],
        conclusion_template=[
            "Fluid loss additives prevent cement dehydration and premature bridging.",
            "API fluid loss target: <50 mL/30 min for most applications, <30 mL for critical zones.",
            "Synthetic polymers (CMHEC, PAC) preferred over bentonite for HPHT."
        ],
        reasoning_framework="""
**Fluid loss** is volume of water lost from cement slurry into permeable formations under differential pressure.
API test: 1000 psi differential, 30 minutes, through 325-mesh screen at BHCT.

**Why control fluid loss**:
1. **Prevent dehydration**: Excessive fluid loss → slurry thickens prematurely → poor mud displacement, bridging in annulus
2. **Maintain pumpability**: Water loss stiffens slurry, increases ECD, may cause lost circulation
3. **Formation damage**: High filtrate invasion can damage production zones
4. **Shale stability**: Water invasion destabilizes shale, causes wellbore enlargement

**Target values**:
- **General purpose**: <100 mL/30 min
- **Critical zones** (tight annulus, weak formations): <50 mL/30 min
- **Horizontal wells / slim holes**: <30 mL/30 min
- **HPHT wells**: <50 mL/30 min at BHCT >300°F

**Common fluid loss additives**:
1. **Cellulose derivatives**:
   - **CMHEC** (carboxymethyl hydroxyethyl cellulose): 0.3-0.75% BWOC, effective to 350°F
   - **PAC** (polyanionic cellulose): 0.5-1.5% BWOC, lower temperature limit ~200°F
   - Mechanism: Forms impermeable filter cake, increases viscosity

2. **Synthetic polymers**:
   - **AMPS copolymers** (2-acrylamido-2-methylpropanesulfonic acid): 0.2-0.6% BWOC, HPHT to 500°F
   - **Acrylamide/acrylate copolymers**: 0.3-0.8% BWOC
   - Advantage: Thermally stable, low concentration required

3. **Latex** (styrene-butadiene copolymer):
   - Concentration: 1-5% BWOC (by volume)
   - Forms elastic film, excellent fluid loss control (<20 mL/30 min)
   - Dual benefit: Improves flexibility, reduces shrinkage

4. **Bentonite** (gel):
   - Concentration: 2-5% BWOC
   - Low cost, but increases viscosity significantly
   - Not suitable for HPHT (degrades >250°F)

**Overdosing effects**:
- Excessive viscosity → increased ECD, friction pressure
- Reduced slurry yield (more water trapped in gel structure)
- Possible compatibility issues with dispersants
        """,
        key_factors=[
            "API fluid loss test results at BHCT and 1000 psi",
            "Annular geometry (tight annulus needs lower fluid loss)",
            "Formation permeability and differential pressure",
            "Temperature stability of fluid loss additive",
            "Impact on slurry rheology and pumpability"
        ],
        primary_authority=[
            "API RP 10B-2 Section 8 - Fluid Loss Testing",
            "API Spec 10A Section 8 - Fluid Loss Requirements",
            "SPE 135629 - Advanced Fluid Loss Additives for HPHT (2010)"
        ],
        burden_holder="Service company designs slurry; Operator specifies fluid loss target",
        adversary_position="Excessive fluid loss → dehydration, bridging, stuck pipe. Over-treatment → high ECD, lost circulation.",
        counter_arguments=[
            "Lower fluid loss always safer (minimizes dehydration risk)",
            "High fluid loss acceptable in high-permeability formations if no tight spots",
            "Latex provides superior control but adds cost",
            "Real-time monitoring can detect bridging early"
        ],
        resolution_strategy="Conduct API fluid loss tests at BHCT. Target <50 mL/30 min for standard applications, <30 mL for critical zones. Verify compatibility with retarders/dispersants (avoid flocculation). Confirm ECD with fluid loss additive does not exceed fracture gradient.",
        entity_scope="Service companies, well engineers, lab technicians",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API fluid loss testing is industry standard; target values are best practices",
        controlling_precedent="API RP 10B-2 fluid loss test procedures (Section 8)",
        issue_category=IssueCategory.ADDITIVES,
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Primary Cementing - Displacement Efficiency",
        keywords=["mud displacement", "centralization", "pipe movement", "displacement rate", "turbulent flow"],
        conclusion_template=[
            "Effective mud displacement requires turbulent flow, centralization >70%, and pipe movement.",
            "Critical displacement rate: achieve Reynolds number >3000 in annulus.",
            "Poor displacement causes microannuli and channeling."
        ],
        reasoning_framework="""
**Displacement efficiency** is the fraction of mud removed from the annulus and replaced with cement.
Target: >95% displacement for zonal isolation.

**Key factors affecting displacement**:

1. **Flow regime - Turbulent vs Laminar**:
   - **Reynolds number**: Re = (928 × ρ × v × D_h) / μ_p
     where ρ = density (ppg), v = velocity (ft/min), D_h = hydraulic diameter (in), μ_p = plastic viscosity (cP)
   - **Turbulent flow** (Re > 3000): Best displacement, breaks gelled mud films
   - **Laminar flow** (Re < 2100): Poor displacement, stable mud channels persist
   - **Transitional flow** (2100 < Re < 3000): Partial displacement

   **Practical displacement rates**:
   - Slim annulus (<1 in): 6-10 BPM → Re ~3000-5000
   - Standard annulus (1-3 in): 8-15 BPM → Re ~2500-4500
   - Large annulus (>3 in): 10-20 BPM → Re ~2000-3500 (hard to achieve turbulence)

2. **Centralization**:
   - **Standoff** = (D_hole - D_pipe) / (2 × (D_hole - D_pipe)) × 100%
   - **Target**: >70% standoff (API RP 10D-2)
   - **Critical sections**: 30° from bottom, top 500 ft, across production zones
   - Decentralized pipe → mud bypassing on wide side, cement channeling on narrow side
   - **Bow spring centralizers**: 1 per 40 ft (deviated), 1 per 60 ft (vertical)

3. **Pipe movement**:
   - **Rotation**: 10-40 RPM during displacement breaks gelled mud, improves contact
   - **Reciprocation**: ±10-20 ft every 5-10 minutes helps displacement
   - **Contraindication**: Avoid movement if stuck pipe risk, weak formations, H2S zones

4. **Density hierarchy**:
   - Maintain progression: ρ_mud < ρ_spacer_lead < ρ_cement < ρ_spacer_tail (if used)
   - Prevents cement from fingering through lighter mud

5. **Contact time and washes**:
   - **Chemical wash**: 5-10 BPL surfactant/solvent breaks oil-based mud film
   - **Spacer**: 50-200 BPL viscous pill (10-15 ppg, 50-100 sec Marsh viscosity)
   - **Contact time**: ≥10 min at critical zones (slower displacement rate)

**Failure mechanisms**:
- **Channeling**: Mud bypasses cement in eccentric annulus → microannuli
- **Gelled mud**: Static gel strength >100 lbf/100ft² not broken by cement → poor bonding
- **Contamination**: Cement/mud mixing creates weak transition zone
        """,
        key_factors=[
            "Reynolds number calculation for actual annular geometry",
            "Centralization program with standoff calculations",
            "Pipe movement plan (rotation/reciprocation schedule)",
            "Spacer and wash volumes, contact times",
            "Mud rheology and gel strength (static aging test)"
        ],
        primary_authority=[
            "API RP 10D-2 - Recommended Practice on Centralizer Placement (2010)",
            "API RP 65 Part 2 - Isolating Potential Flow Zones (2010)",
            "SPE 56536 - Mud Displacement by Cement Slurries (1999)"
        ],
        burden_holder="Operator and service company (joint responsibility for design and execution)",
        adversary_position="Poor displacement → microannuli, gas migration, failed cement bond logs",
        counter_arguments=[
            "High displacement rates risk lost circulation",
            "Turbulent flow not achievable in large/irregular boreholes",
            "Pipe movement may cause stuck pipe in deviated wells",
            "Centralizers add cost and rig time"
        ],
        resolution_strategy="Calculate Reynolds number for planned displacement rates. Design centralizer program for >70% standoff. Plan pipe movement (rotation if feasible). Specify spacer volume ≥200 ft annular column. Model displacement with cementing software (e.g., CemCADE, StimCADE).",
        entity_scope="Operators, service companies, drilling engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API RP 10D-2 centralization and RP 65 Part 2 displacement are industry standards",
        controlling_precedent="API RP 10D-2 centralization requirements; SPE displacement efficiency studies",
        issue_category=IssueCategory.PRIMARY_CEMENTING,
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Cement Bond Log (CBL) Interpretation",
        keywords=["CBL", "VDL", "E1 amplitude", "transit time", "bond index", "microannulus", "channeling"],
        conclusion_template=[
            "CBL measures acoustic attenuation to assess cement-to-casing bond quality.",
            "Good bond: E1 amplitude <10 mV, transit time >60 μs/ft (8-5/8 in casing).",
            "VDL distinguishes cement from fluid by formation arrivals."
        ],
        reasoning_framework="""
**Cement Bond Log (CBL)** is an acoustic wireline log measuring cement bond quality behind casing.

**Physics**:
1. **Acoustic pulse** (20-25 kHz) transmitted from tool centered in casing
2. **E1 wave** (casing arrival): Compressional wave traveling through casing steel
3. **E2 wave** (formation arrival): Refracted wave through cement and formation
4. **Attenuation**: Good cement bond damps E1 amplitude

**Measurements**:
1. **E1 Amplitude** (mV):
   - **Free pipe** (no cement or fluid): 15-30 mV (high amplitude, little damping)
   - **Poor bond** (microannulus, channeling): 10-20 mV
   - **Good bond**: <10 mV (well-bonded cement attenuates casing wave)
   - **Casing size dependent**: 5-1/2 in casing has lower free-pipe amplitude than 9-5/8 in

2. **Transit Time** (μs/ft or Δt):
   - **Free pipe**: ~57 μs/ft (steel compressional velocity ~17,500 ft/s)
   - **Cemented pipe**: >60 μs/ft (cement coupling slows casing wave)
   - **Bond Index (BI)**: BI = (Δt - Δt_free) / (Δt_bonded - Δt_free) × 100%
   - Good bond: BI > 80%

3. **Variable Density Log (VDL)** - waveform display:
   - Shows E1 (casing) and E2 (formation) arrivals over time
   - **Good cement**: Strong formation arrivals (E2), weak E1
   - **Poor cement/no cement**: Strong E1, weak/absent E2
   - **Channeling**: E2 arrives at some azimuths but not others (log rotation needed)

**Interpretation criteria** (8-5/8 in, 40 ppf casing example):
- **Good bond**: E1 < 8 mV, Δt > 65 μs/ft, formation arrivals on VDL
- **Fair bond**: E1 8-12 mV, Δt 60-65 μs/ft, weak formation arrivals
- **Poor bond**: E1 > 12 mV, Δt < 60 μs/ft, no formation arrivals
- **Free pipe**: E1 > 20 mV, Δt ~57 μs/ft, strong casing ringing on VDL

**Limitations**:
- Cannot detect thin microannuli (<1 mm) if cement is otherwise intact
- Assumes cement has standard acoustic properties (~8500-10,000 ft/s velocity)
- Lightweight or foamed cement may show poor bond (low acoustic impedance)
- Does not assess cement sheath integrity beyond casing OD
- Centralization affects measurement (tool must be centered)

**Modern alternatives**:
- **Ultrasonic Imaging** (USIT, Isolation Scanner): 360° azimuthal coverage, detects channeling
- **Radial Bond Tools**: Measure cement impedance at multiple azimuths
        """,
        key_factors=[
            "Casing size and weight (affects free-pipe amplitude baseline)",
            "Cement slurry acoustic properties (density, compressive strength)",
            "Formation acoustic properties (hard vs soft formations)",
            "Tool centralization during logging",
            "VDL interpretation for azimuthal coverage assessment"
        ],
        primary_authority=[
            "API RP 33 - Care and Use of Wireline Operations (historical reference)",
            "SPE 14418 - Cement Bond Logging - A State of the Art Review (1985)",
            "Schlumberger Log Interpretation Principles (Chapter 11 - Cement Evaluation)"
        ],
        burden_holder="Operator (interprets log), Service company (acquires log, provides interpretation guide)",
        adversary_position="CBL shows poor bond → may require remedial cementing (squeeze), potential gas migration pathway",
        counter_arguments=[
            "CBL is qualitative, cannot quantify microannulus size",
            "Lightweight cement gives poor CBL even if isolation is adequate",
            "Formation arrivals may be masked in soft formations (low acoustic impedance)",
            "Modern ultrasonic tools provide better data than CBL"
        ],
        resolution_strategy="Establish baseline criteria for good/fair/poor bond based on casing size and cement properties. Compare CBL amplitude to free-pipe log (run above TOC). Integrate VDL interpretation (formation arrival presence/absence). If critical zone shows poor bond, run ultrasonic log or consider remedial cementing.",
        entity_scope="Operators, service companies, petrophysicists, completion engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="CBL interpretation criteria are industry standard; thresholds vary by casing size and cement type",
        controlling_precedent="SPE 14418 CBL interpretation methods; service company interpretation charts",
        issue_category=IssueCategory.CEMENT_EVALUATION,
        zone=AnalysisZone.EVALUATION
    ),

    DoctrineBlock(
        topic="Remedial Cementing - Squeeze Operations",
        keywords=["squeeze", "hesitation squeeze", "low-pressure squeeze", "high-pressure squeeze", "perforate and squeeze", "bradenhead squeeze"],
        conclusion_template=[
            "Squeeze cementing repairs poor primary cement, isolates perforations, or abandons zones.",
            "Low-pressure squeeze (<0.5 psi/ft) preferred to avoid fracturing formation.",
            "Hesitation technique allows cement dehydration for better placement."
        ],
        reasoning_framework="""
**Squeeze cementing** is forcing cement slurry through perforations or channels to repair isolation failures.

**Types of squeeze operations**:

1. **Low-Pressure Squeeze**:
   - **Pressure limit**: <0.5 psi/ft fracture gradient (typically 200-800 psi surface pressure)
   - **Mechanism**: Cement dehydration against formation, filter cake buildup
   - **Application**: Water shutoff, repair microannuli, gas migration zones
   - **Technique**: "Hesitation" - pump cement, shut in 10-30 min (allows fluid loss), pump again
   - **Volumes**: Small (5-20 BPL cement), multiple stages if needed

2. **High-Pressure Squeeze** (Fracture Squeeze):
   - **Pressure**: Exceeds fracture gradient, intentionally fractures formation
   - **Mechanism**: Cement enters fractures, creates impermeable barrier
   - **Application**: Severe channeling, casing leaks, abandonment
   - **Risk**: Can communicate to other zones if fractures propagate vertically
   - **Volumes**: 50-200 BPL

3. **Bradenhead Squeeze**:
   - Pump cement down annulus (not tubing), force through casing perforations/leaks
   - **Used**: When tubing is stuck or unavailable
   - **Limitation**: Cannot apply high pressure (limited by casing burst rating)

4. **Perforate and Squeeze**:
   - Perforate above/below zone of interest, pump cement to isolate
   - **Application**: Isolate water zones, abandonments
   - **Sequence**: Perforate → pump spacer → pump cement → squeeze → WOC → perforate back (if needed)

**Squeeze procedure (Hesitation Low-Pressure)**:
1. **Isolate zone**: Set packer or bridge plug below, perforate above
2. **Pump pre-flush**: 25-50 BPL spacer or acid (to clean perforations, remove mud cake)
3. **Pump cement**: 5-20 BPL Class A/C + 2% CaCl2 accelerator, low fluid loss (<50 mL)
4. **Hesitate**: Shut in 15-30 min (cement dehydrates, builds filter cake)
5. **Squeeze**: Apply pressure <0.5 psi/ft (typically 200-500 psi), hold 15 min
6. **Release pressure**: Reverse circulate excess cement if possible
7. **WOC**: 12-24 hours (accelerated cement)
8. **Test**: Pressure test or run temperature log to verify placement

**Cement design for squeeze**:
- **Low fluid loss**: <30 mL/30 min API (critical for dehydration)
- **Accelerated**: 2-4% CaCl2 or 0.5-1% NaCl for fast strength (8-12 hr WOC)
- **High early strength**: Class A or C (not Class H, too slow)
- **Thickening time**: 2-4 hours (enough for hesitation cycles)
- **Dispersant**: May be needed to reduce viscosity for injection through tight perforations

**Evaluation**:
- **Pressure test**: Squeeze pressure (ISIP) indicates cement placement
- **Temperature log**: Cement hydration exotherm shows placement depth
- **CBL**: Re-run to verify improved bond (wait 24-48 hr for cement to harden)
        """,
        key_factors=[
            "Fracture gradient and maximum allowable squeeze pressure",
            "Perforation size and density (affects injectivity)",
            "Cement fluid loss (critical for low-pressure squeeze success)",
            "Hesitation time (longer → better dehydration)",
            "Accelerator concentration for rapid WOC"
        ],
        primary_authority=[
            "API RP 65 Part 2 - Isolating Potential Flow Zones During Well Construction (2010)",
            "SPE 6547 - Squeeze Cementing Operations (1977)",
            "Well Cementing (Schlumberger) Chapter 11 - Remedial Cementing"
        ],
        burden_holder="Operator designs squeeze; service company executes",
        adversary_position="Failed squeeze → persistent gas migration, water production, or zone communication",
        counter_arguments=[
            "High-pressure squeeze more reliable for severe channeling",
            "Fracturing formation is acceptable if no vertical fracture growth risk",
            "Multiple low-pressure squeezes may be needed (adds cost/time)",
            "Temperature logs may not detect thin cement placement"
        ],
        resolution_strategy="Diagnose isolation failure (CBL, temperature log, production log). Design low-pressure squeeze with high fluid loss control and accelerator. Plan hesitation cycles (pump → shut in → pump). Limit pressure <0.5 psi/ft. Evaluate with pressure test and temperature log.",
        entity_scope="Operators, service companies, completion engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API RP 65 Part 2 provides remedial cementing guidance; hesitation technique is best practice",
        controlling_precedent="API RP 65 Part 2 Section 7 - Remedial Cementing; SPE 6547 squeeze procedures",
        issue_category=IssueCategory.REMEDIAL_CEMENTING,
        zone=AnalysisZone.EXECUTION
    ),

    DoctrineBlock(
        topic="Gas Migration - Mechanisms and Prevention",
        keywords=["gas migration", "annular pressure", "transition time", "gel strength", "right-angle set", "expanding cement"],
        conclusion_template=[
            "Gas migration occurs during cement gelation when hydrostatic pressure drops below pore pressure.",
            "Critical period: transition time from liquid to gel (gel strength 50-500 lbf/100ft²).",
            "Prevention: minimize transition time with right-angle set cement, use gas-block additives."
        ],
        reasoning_framework="""
**Gas migration** is the flow of formation gas through cement during or after placement, causing annular pressure buildup (APB).

**Mechanism** (3 phases):

1. **Phase 1 - Liquid cement** (0-2 hr typical):
   - Slurry is liquid, hydrostatic pressure P_h = 0.052 × ρ_cement × TVD
   - If P_h > P_formation, no influx
   - Pressure maintained by liquid column

2. **Phase 2 - Gelation/transition** (2-6 hr typical):
   - Cement gels, forms structure, but not yet strong
   - **Gel strength development**: 0 → 50 → 500 lbf/100ft² over 1-4 hours
   - **Problem**: Gel cannot support full hydrostatic pressure → effective P_h drops
   - **Transition time**: Period when gel strength <500 lbf/100ft² (cannot seal gas percolation)
   - **Critical**: If P_formation > P_effective during transition → gas enters cement

3. **Phase 3 - Hardening** (6-24 hr typical):
   - Cement develops compressive strength >500 psi → impermeable
   - Gas migration stops if cement sets before excessive gas invasion

**Transition time criticality**:
- **Fast transition** (0.5-1.5 hr): "Right-angle set" - liquid → solid quickly, minimal gas invasion
- **Slow transition** (3-6 hr): Extended period of vulnerability → gas channels form

**Gas migration drivers**:
- **Shallow gas zones**: High permeability, P_formation close to P_hydrostatic → high influx rate
- **Underbalanced slurry**: ρ_cement insufficient margin above pore pressure
- **Cement shrinkage**: Volume reduction during setting (~2-7%) creates negative pressure
- **Excessive fluid loss**: Dehydration increases slurry density locally but reduces effective P_h

**Prevention methods**:

1. **Right-angle set additives**:
   - **Mechanism**: Precipitate calcium compounds rapidly, short transition time
   - **Sodium silicate**: 0.2-1.0% BWOC, works with Class A cement, 30-60 min transition
   - **Sodium chloride + Ca-aluminate**: Rapid gel strength development

2. **Latex cement**:
   - **Mechanism**: Flexible polymer film seals gas pathways, reduces permeability
   - **Concentration**: 1-5% by volume
   - **Benefit**: Also prevents shrinkage, improves ductility

3. **Expanding cement**:
   - **Mechanism**: CaO or MgO expansion counteracts shrinkage, maintains contact pressure
   - **Additives**: CaO 5-12% BWOC, CaSO4 (gypsum) 3-5%
   - **Expansion**: 0.1-0.5% volumetric (enough to offset shrinkage)

4. **Gas-block particulates**:
   - **Mechanism**: Gilsonite, graphite, or synthetic fibers bridge gas pathways
   - **Concentration**: Gilsonite 5-15% BWOC
   - **Permeability reduction**: 10-100× vs neat cement

5. **High density slurry**:
   - Increase safety margin: P_h - P_formation ≥ 200-300 psi throughout gelation
   - Trade-off: Fracture risk

6. **Thixotropic cement**:
   - Rapid gel strength development at static conditions
   - **Bentonite** 1-2% BWOC increases gel strength 2-3×

**Detection**:
- **Annular pressure buildup (APB)**: Surface pressure on annulus after WOC
- **Temperature log**: Gas flow creates cooling (Joule-Thomson effect) or channeling signature
- **Noise log**: Acoustic detection of gas flow behind casing
        """,
        key_factors=[
            "Transition time (target <2 hr)",
            "Pressure margin P_h - P_formation during gelation",
            "Gel strength development rate (API testing)",
            "Cement shrinkage characteristics",
            "Formation permeability and gas saturation"
        ],
        primary_authority=[
            "SPE 163043 - Cement Slurry Design for Gas Migration Prevention (2013)",
            "API RP 65 Part 2 - Section 6: Gas Migration Control (2010)",
            "SPE 56534 - Mechanism of Annular Pressure Buildup (1999)"
        ],
        burden_holder="Operator and service company (joint responsibility for slurry design)",
        adversary_position="Gas migration → annular pressure, casing collapse risk, environmental release, well integrity failure",
        counter_arguments=[
            "Right-angle set cements may have reduced long-term strength",
            "Expanding cements can cause casing stress if over-designed",
            "High-density cement prevents gas migration but risks fracturing",
            "Latex and additives increase cost significantly"
        ],
        resolution_strategy="Assess gas migration risk (shallow gas zones, high permeability). Design cement with transition time <2 hr (use sodium silicate or latex). Verify gel strength development with API testing. Consider expanding cement or gas-block additives for high-risk zones. Monitor annular pressure post-cement.",
        entity_scope="Operators, service companies, well integrity engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Gas migration mechanisms well-understood; right-angle set is proven mitigation (SPE 163043)",
        controlling_precedent="API RP 65 Part 2 Section 6; SPE gas migration prevention studies",
        issue_category=IssueCategory.GAS_MIGRATION,
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Foamed Cement - Design and Application",
        keywords=["foamed cement", "nitrogen", "surfactant", "foam quality", "foam stability", "lightweight cement"],
        conclusion_template=[
            "Foamed cement uses nitrogen gas to reduce density (8-14 ppg) while maintaining strength.",
            "Foam quality (gas volume fraction) typically 40-70%.",
            "Critical: foam stability during placement to prevent density segregation."
        ],
        reasoning_framework="""
**Foamed cement** is cement slurry with nitrogen (N2) gas dispersed as fine bubbles to reduce density while maintaining compressive strength.

**Design parameters**:

1. **Foam quality (Φ)**:
   - Φ = V_gas / (V_gas + V_slurry) × 100%
   - **Low foam**: 20-40% (density 13-15 ppg)
   - **Medium foam**: 40-60% (density 10-13 ppg)
   - **High foam**: 60-80% (density 8-10 ppg)
   - **Ultra-light**: >80% (density <8 ppg, rarely used)

2. **Density relationship**:
   - ρ_foam = ρ_base_slurry × (1 - Φ)
   - Example: 16 ppg base slurry, 50% foam quality → 8 ppg foamed cement

3. **Nitrogen requirement**:
   - N2 volume = (Φ / (1 - Φ)) × V_slurry at downhole P and T
   - Use real gas law (Z-factor) for HPHT conditions
   - Surface N2 volume >> downhole volume (compression)

4. **Surfactant**:
   - **Concentration**: 0.5-2.0% by volume of water (BVOW)
   - **Types**: Anionic (sodium lauryl sulfate), amphoteric (betaines), proprietary blends
   - **Function**: Stabilizes foam, prevents coalescence, maintains bubble size distribution
   - **Bubble size**: Target 50-200 microns (larger → unstable, smaller → viscous)

**Advantages**:
- **Reduced hydrostatic**: Prevents lost circulation in weak formations
- **Improved bonding**: Lower contact stress on casing, better for corrosion resistance
- **Bridging capability**: Bubbles can seal fractures/vugs (lost circulation control)

**Challenges**:

1. **Foam stability**:
   - **Segregation risk**: Gas rises, slurry settles → density stratification
   - **Mitigation**: Use high-viscosity base slurry (add bentonite, CMHEC), maintain turbulent flow during displacement
   - **Static stability test**: Measure density gradient after 30 min static (API RP 10B-4)

2. **Rheology**:
   - Foam is non-Newtonian, highly shear-thinning
   - **Yield stress**: 2-5× higher than base slurry (difficult to pump if over-foamed)
   - **Friction pressure**: Can be 2-3× higher than predicted (affects ECD)

3. **Strength development**:
   - Compressive strength ~ (1 - Φ)^2 × strength_base_slurry
   - Example: 3000 psi base slurry, 50% foam → ~750 psi (adequate for isolation)
   - **Minimum target**: 500 psi at 24 hr for structural integrity

4. **Nitrogen solubility**:
   - At high pressure, N2 dissolves in water phase → reduces foam quality downhole
   - **Effect**: Actual downhole density higher than designed (compression + solubility)
   - **Mitigation**: Use foam quality calculation software (e.g., CemCADE Foam Module)

5. **Contamination**:
   - Cement/mud mixing collapses foam → sudden density increase
   - **Prevention**: Use effective spacers, maintain density hierarchy

**Applications**:
- **Lost circulation zones**: 8-12 ppg foam, high foam quality (60-70%)
- **Depleted reservoirs**: 10-14 ppg, moderate foam (40-50%)
- **Weak formations** (low fracture gradient): 9-13 ppg
- **Shale gas wells** (long laterals): Reduce hydrostatic on toe

**Quality control**:
- **Real-time density measurement**: Continuous Coriolis meter on cement unit
- **Nitrogen flow rate monitoring**: Match planned injection rate
- **Surfactant batch testing**: Verify foam stability at BHCT and pressure
        """,
        key_factors=[
            "Foam quality (gas volume fraction) design and verification",
            "Surfactant selection and concentration for stability",
            "Base slurry rheology (must support foam stability)",
            "Nitrogen volume calculation at downhole P/T",
            "Static stability testing per API RP 10B-4"
        ],
        primary_authority=[
            "API RP 10B-4 - Preparation and Testing of Foamed Cement Slurries (2004)",
            "SPE 97261 - Foamed Cement for Weak Zone Cementing (2005)",
            "ISO 10426-5 - Foamed Cement Testing Procedures (2004)"
        ],
        burden_holder="Service company designs foam cement; Operator approves density and quality targets",
        adversary_position="Foam instability → density segregation, poor zonal isolation, lost circulation if segregated slurry is too heavy",
        counter_arguments=[
            "Foamed cement is complex, higher risk than conventional lightweight systems",
            "Perlite or cenospheres provide more stable lightweight cement",
            "Foam strength may be insufficient for structural loads",
            "Nitrogen equipment adds mobilization cost"
        ],
        resolution_strategy="Design foam quality for target density. Select surfactant and test stability at BHCT. Verify base slurry rheology supports foam (high PV/YP). Plan nitrogen injection rate based on slurry rate and foam quality. Monitor real-time density during pumping. Test compressive strength ≥500 psi at 24 hr.",
        entity_scope="Service companies, well engineers, specialized cementing crews",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Foamed cement is complex, requires specialized equipment and expertise; API RP 10B-4 provides testing standards",
        controlling_precedent="API RP 10B-4 foam cement testing; SPE field case studies",
        issue_category=IssueCategory.SLURRY_DESIGN,
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="HPHT Cementing - Challenges and Solutions",
        keywords=["HPHT", "high temperature", "high pressure", "retarders", "cement degradation", "strength retrogression"],
        conclusion_template=[
            "HPHT wells (>300°F, >10,000 psi) require specialized cement systems and additives.",
            "Strength retrogression occurs >230°F without silica stabilization.",
            "Use AMPS-based retarders and 35-40% silica flour for HPHT stability."
        ],
        reasoning_framework="""
**HPHT cementing** applies to wells with bottomhole conditions exceeding 300°F and/or 10,000 psi.

**HPHT challenges**:

1. **Strength retrogression**:
   - **Phenomenon**: Above ~230°F, Portland cement converts from C-S-H (calcium silicate hydrate) to α-C2SH (alpha-dicalcium silicate hydrate)
   - **Effect**: Compressive strength drops from 3000+ psi to <500 psi, permeability increases 100-1000×
   - **Mechanism**: Phase transformation increases porosity, weakens structure
   - **Solution**: Add silica flour 35-40% BWOC (by weight of cement)
   - **Silica function**: Reacts with Ca(OH)2 to form stable C-S-H, prevents retrogression

2. **Accelerated hydration**:
   - **Problem**: High temperature accelerates cement setting → short thickening time
   - **Risk**: Premature gelation before displacement complete → stuck pipe
   - **Solution**: High-temperature retarders
     * **AMPS copolymers** (aminomethylenephosphonate): 0.1-0.5% BWOC, effective to 500°F
     * **Phosphonates**: 0.05-0.3% BWOC, stable to 400°F
     * **Avoid lignosulfonates** at >300°F (degrade, lose effectiveness)

3. **Fluid loss at temperature**:
   - Standard fluid loss additives degrade >300°F
   - **Solutions**:
     * **AMPS copolymers**: Dual retarder/fluid loss control, 0.3-0.6% BWOC
     * **Synthetic polymers**: Thermally stable to 500°F
     * **Avoid cellulose derivatives** >250°F (thermal degradation)

4. **Free water and settling**:
   - High temperature increases free water separation (water rises, solids settle)
   - **API limit**: <5.2 mL free water per 250 mL slurry after 2 hr at BHST
   - **Solutions**:
     * **Decrease water/cement ratio**: Use dispersants to maintain pumpability
     * **Add anti-settling agents**: Bentonite 1-2% BWOC, synthetic polymers
     * **Downward slurry placement** (through drillpipe): Gravity aids particle suspension

5. **Thermal expansion/contraction**:
   - Casing expands during cementing (hot slurry), contracts during production (cooling)
   - **Risk**: Microannuli formation at casing-cement interface
   - **Solutions**:
     * **Flexible cement**: Latex 2-5%, reduces elastic modulus
     * **Expanding cement**: CaO 8-12% BWOC counteracts shrinkage
     * **High-strength cement**: >5000 psi compressive strength maintains integrity

6. **Formation damage**:
   - High filtrate invasion at HPHT damages production zones
   - **Target**: API fluid loss <30 mL/30 min at BHCT

**HPHT slurry design example** (15,000 ft, 350°F):
- **Base**: Class H cement
- **Silica flour**: 40% BWOC (prevent strength retrogression)
- **Retarder**: AMPS copolymer 0.3% BWOC (thickening time ~6 hr at 350°F)
- **Fluid loss**: AMPS copolymer (dual function) + latex 3% (target <30 mL)
- **Dispersant**: Polynaphthalene sulfonate 0.5% BWOC (reduce viscosity, allow lower W/C ratio)
- **Density**: 16.5 ppg (add hematite if needed)
- **Water/cement ratio**: 0.38-0.42 (lower than standard to reduce free water)

**Testing requirements**:
- **API Schedule 9**: Simulate BHCT ramp for thickening time test
- **Compressive strength**: Test at 24 hr, 7 days, 28 days at BHCT (target >3000 psi)
- **Permeability**: Measure at BHCT and pressure (target <0.1 mD)
- **Free water**: <5.2 mL per API Spec 10A at BHST
        """,
        key_factors=[
            "Bottomhole static temperature (BHST) and circulating temperature (BHCT)",
            "Silica flour concentration (35-40% BWOC mandatory >230°F)",
            "AMPS-based retarder selection and concentration",
            "Fluid loss control at HPHT (target <30 mL/30 min)",
            "Free water and settling test results"
        ],
        primary_authority=[
            "API RP 10B-2 Section 10 - HPHT Cement Testing (2013)",
            "API Spec 10A Annex B - High Temperature Cementing (2010)",
            "SPE 98896 - HPHT Cement System Design (2006)"
        ],
        burden_holder="Service company designs HPHT cement; Operator approves testing and performance criteria",
        adversary_position="HPHT cement failure → strength retrogression, sustained casing pressure, production zone damage",
        counter_arguments=[
            "Silica flour reduces early strength (24 hr), may delay operations",
            "AMPS retarders are expensive vs lignosulfonates",
            "Some wells have operated successfully without silica (if <230°F peak temperature)",
            "Free water acceptable if top of cement is well above production zone"
        ],
        resolution_strategy="Model BHST and BHCT using thermal simulators. If BHST >230°F, design cement with 35-40% silica flour. Select AMPS-based retarder for target thickening time. Test API fluid loss at BHCT (<30 mL). Verify free water <5.2 mL and compressive strength >3000 psi at 28 days.",
        entity_scope="Operators, service companies, HPHT specialists",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="HPHT cement design is well-established; silica flour requirement >230°F is industry consensus",
        controlling_precedent="API RP 10B-2 HPHT testing; SPE 98896 field proven designs",
        issue_category=IssueCategory.HPHT_OPERATIONS,
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Lost Circulation During Cementing",
        keywords=["lost circulation", "LCM", "thief zone", "fracture", "stage cementing", "low-density cement"],
        conclusion_template=[
            "Lost circulation during cementing risks incomplete zonal isolation and wellbore instability.",
            "Mitigation: stage cementing, low-density cement, or LCM-enhanced slurries.",
            "Severe losses may require liner/tieback strategy or cementing through coiled tubing."
        ],
        reasoning_framework="""
**Lost circulation** is loss of cement slurry to formation due to fractures, vugs, or high permeability.
**Risk**: Incomplete cement column → poor zonal isolation, shoe not cemented, potential kicks.

**Causes during cementing**:
1. **Fracture gradient exceeded**: ECD (slurry density + friction pressure) > formation fracture pressure
2. **Natural fractures**: Pre-existing fractures in carbonates, shales
3. **Vugs/caverns**: Karst, dissolved formations
4. **Unconsolidated zones**: Gravel, poorly consolidated sands

**Severity classification**:
- **Seepage losses**: <50 BPL, slows returns
- **Partial losses**: 50-500 BPL, significant volume but not total
- **Severe/total losses**: >500 BPL or complete loss of returns

**Prevention strategies**:

1. **Low-density cement**:
   - **Foamed cement**: 8-14 ppg (see separate doctrine on foamed cement)
   - **Extended cement**: Perlite (9-13 ppg), cenospheres (11-14 ppg), bentonite (12.5-14 ppg)
   - **Trade-off**: Lower density → lower compressive strength, may not meet structural requirements

2. **Staged cementing**:
   - **Technique**: Cement in multiple stages, isolate loss zones between stages
   - **Method**: Run DV tool on liner, or stage collar on casing string
   - **Example**: Stage 1 - cement from shoe to stage collar (above loss zone), Stage 2 - cement stage collar to surface (after WOC on Stage 1)
   - **Advantage**: Prevents slurry loss by reducing cement column height and hydrostatic pressure

3. **LCM-enhanced cement**:
   - Add lost circulation material to cement slurry to bridge fractures/vugs during placement
   - **Fiber**: Polypropylene, nylon fibers 1-5 ppf (pounds per foot³), bridges small fractures
   - **Particulates**: Gilsonite 5-15% BWOC, ground nut shells 5-10% BWOC
   - **Granular**: Sized calcium carbonate 10-40 ppf
   - **Mechanism**: Creates filter cake in fracture, reduces fluid loss
   - **Trade-off**: Increases slurry viscosity, may affect pumpability

4. **Wellbore strengthening**:
   - **Pre-treatment**: Pump LCM pill before cementing to seal fractures
   - **Graphite/calcium carbonate blend**: 20-40 ppf in weighted spacer
   - **Stress cage theory**: LCM props fractures open, allows higher ECD

5. **Reduce ECD**:
   - **Lower displacement rate**: Reduces friction pressure (may compromise turbulent flow and displacement efficiency)
   - **Use pipe movement carefully**: Surges can induce losses
   - **Optimize rheology**: Low-viscosity spacers reduce friction

**Operational responses during cementing**:

1. **Minor losses (seepage)**:
   - Continue pumping, monitor returns closely
   - May accept partial loss if top of cement (TOC) reaches target depth

2. **Partial losses**:
   - **Reduce pump rate** to lower ECD
   - **Switch to lower density slurry** if available (pre-mixed contingency batch)
   - **Pump LCM pill** through cement unit (if compatible)

3. **Severe/total losses**:
   - **Stop pumping** immediately to avoid losing entire cement volume
   - **Options**:
     * **Pump cement through coiled tubing** to shoe (places cement without pressuring annulus)
     * **Top job** - Wait for WOC on partial column, then pump additional cement down annulus
     * **Abandon attempt**, run liner with external casing packer (ECP) across loss zone, tie back to surface

**Top of Cement (TOC) determination after losses**:
- **Temperature log**: Cement hydration exotherm (hottest zone = TOC)
- **Radioactive tracer**: Add to cement, run gamma ray log
- **CBL/VDL**: Identify free pipe above TOC
- **Acoustic fill detection**: Tag top with wireline (mechanical or acoustic)

**Case example** - Severe loss in carbonate:
- Planned: 9-5/8 in casing, 16.0 ppg Class H neat, 1200 BPL
- Encountered: Total loss at 500 BPL pumped, TOC estimated at shoe (6000 ft MD)
- Response: Pumped 300 BPL foamed cement (11 ppg, 50% foam quality) through coiled tubing to shoe, followed by 200 BPL fiber-enhanced cement (13 ppg). TOC reached 3500 ft MD (above production zone). Ran liner tieback to surface for full isolation.
        """,
        key_factors=[
            "Formation fracture gradient profile (identify weak zones)",
            "Lost circulation history in offset wells",
            "ECD calculation including friction pressure",
            "Availability of contingency low-density cement",
            "TOC target depth vs zonal isolation requirements"
        ],
        primary_authority=[
            "API RP 10B-6 - Determining the Static Gel Strength of Cement Formulations (2010)",
            "SPE 101432 - Lost Circulation Material Selection (2006)",
            "IADC Drilling Manual - Lost Circulation Chapter"
        ],
        burden_holder="Operator (designs contingency), Service company (executes response)",
        adversary_position="Lost circulation during cementing → incomplete cement sheath, zonal isolation failure, potential well control issues",
        counter_arguments=[
            "Accepting partial loss may be better than risking stuck pipe with continued pumping",
            "Low-density cement may not meet compressive strength requirements",
            "Staged cementing adds rig time and cost",
            "LCM in cement may clog surface equipment or perforate tools later"
        ],
        resolution_strategy="Identify loss zones from offset well data and LOT/FIT. Design low-density cement system as contingency. Plan staged cementing if severe loss predicted. Pre-position coiled tubing if high-risk well. Monitor returns real-time during displacement. If losses occur, assess TOC, compare to zonal isolation requirements, execute tieback/liner strategy if needed.",
        entity_scope="Operators, service companies, drilling engineers, well engineers",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Lost circulation responses are field-specific; strategies proven in case studies but success varies",
        controlling_precedent="API RP 10B-6 gel strength measurement; SPE LCM field applications",
        issue_category=IssueCategory.LOST_CIRCULATION,
        zone=AnalysisZone.EXECUTION
    ),

    DoctrineBlock(
        topic="Two-Plug Cementing Method",
        keywords=["bottom plug", "top plug", "plug bumping", "displacement efficiency", "contamination", "cement head"],
        conclusion_template=[
            "Two-plug method uses bottom and top plugs to isolate cement from mud and prevent contamination.",
            "Bottom plug lands first, ruptures, allows cement flow; top plug lands at float collar, signals cement displacement complete.",
            "Plug bump pressure indicates successful landing; absence suggests plug bypass or equipment failure."
        ],
        reasoning_framework="""
**Two-plug cementing** is the standard method for primary cementing using mechanical plugs to separate fluids.

**Components**:

1. **Cementing head** (plug container):
   - Attaches to top of casing string
   - Holds bottom and top plugs before release
   - Typically has two chambers with mechanical releases

2. **Bottom plug** (leading plug):
   - **Construction**: Rubber cup/disk with rupturable diaphragm
   - **Function**: Separates mud ahead from cement behind, wipes casing ID
   - **Landing**: Lands on float collar, diaphragm ruptures at 200-500 psi differential
   - **Flow path**: After rupture, cement flows through plug and into annulus

3. **Top plug** (trailing plug):
   - **Construction**: Solid rubber plug (non-rupturable), free-floating or mechanical release
   - **Function**: Separates cement from displacement fluid (mud) behind, wipes residual cement from casing
   - **Landing**: Lands on bottom plug (seated in float collar), does NOT rupture
   - **Bump**: Pressure increases sharply when top plug lands (bump pressure)

4. **Float collar**:
   - **Location**: 1-2 joints above casing shoe
   - **Function**: Holds plugs, contains check valve to prevent backflow
   - **Design**: Landing shoulder for bottom plug, ball seat for check valve

**Cementing sequence**:

1. **Pre-pump**: Spacer/wash pumped down casing, ahead of bottom plug
2. **Bottom plug release**: Drop or mechanically release bottom plug from cement head
3. **Cement pumping**: Pump cement slurry behind bottom plug (plug descends with cement)
4. **Bottom plug landing**: Plug seats on float collar, pressure rises 200-500 psi, diaphragm ruptures
5. **Cement flow**: Cement flows through ruptured bottom plug into annulus
6. **Top plug release**: Release top plug when calculated cement volume pumped (or slightly before)
7. **Displacement**: Pump mud/water behind top plug to displace cement into annulus
8. **Top plug landing**: Plug lands on bottom plug (seated in float collar)
9. **Bump pressure**: Surface pressure rises sharply (500-2000 psi typical), indicates plug landed
10. **Hold pressure**: Maintain pressure briefly (2-5 min) to ensure float valve seats, prevent U-tubing

**Pressure signatures**:
- **Bottom plug rupture**: 200-500 psi spike, then pressure drops as cement flows
- **Top plug bump**: 500-2000 psi sustained pressure increase (higher than rupture)
- **No bump**: Indicates plug bypassed, shoe track not full, or float equipment failure

**Advantages**:
- **Prevents contamination**: Cement never contacts mud directly (isolated by plugs)
- **Wiping action**: Plugs clean casing ID, reduce cement-mud mixing
- **Positive indication**: Bump pressure confirms displacement complete
- **Float equipment testing**: Confirms float collar/shoe holds back pressure

**Failure modes**:

1. **Plug bypass**:
   - **Cause**: Plug undersized, damaged, or casing couplings create bypass path
   - **Indication**: No bump pressure, or lower than expected
   - **Result**: Cement/mud contamination, weak transition zone

2. **Premature plug landing**:
   - **Cause**: Obstruction in casing (scale, debris, dog-leg)
   - **Indication**: Bump pressure before calculated volume pumped
   - **Result**: Cement not fully displaced, top of cement (TOC) lower than planned

3. **Plug stuck in casing**:
   - **Cause**: Casing ID restrictions, high friction
   - **Action**: Increase pump pressure carefully, avoid exceeding casing burst rating

4. **Float equipment failure**:
   - **Cause**: Check valve stuck open, ball/flapper dislodged
   - **Indication**: Pressure bleeds off after bump, U-tubing occurs
   - **Result**: Cement column drops, TOC lower than planned, possible contamination

**Calculated volumes**:
- **Casing volume**: V_casing = π/4 × (ID_casing)² × L_casing
- **Displacement volume**: V_displace = V_casing - V_cement_pumped + V_shoe_track
- **Shoe track**: Volume from float collar to shoe (typically 2-5 BBL)
- **Plug volumes**: Each plug ~0.5-1.0 BBL, subtract from displacement

**Example calculation**:
- 9-5/8 in casing, 47 ppf, ID = 8.835 in, length = 10,000 ft
- V_casing = 0.1776 × 10,000 = 1,776 BBL
- Cement pumped = 1,200 BBL
- Shoe track (2 joints) = 3 BBL
- Displacement = 1,776 - 1,200 + 3 = 579 BBL (minus ~1 BBL for 2 plugs = 578 BBL)

**Modern alternatives**:
- **Single-plug cementing**: Uses only top plug, cement contacts mud ahead (acceptable for some applications)
- **Automatic plug release**: Mechanical timers or pressure-activated releases
- **Continuous circulation systems**: Eliminate plugs, use density switches and automated cementing unit
        """,
        key_factors=[
            "Accurate casing volume calculation (ID, length)",
            "Correct plug sizing for casing ID",
            "Float equipment integrity (pressure tested before cementing)",
            "Displacement volume calculation including shoe track",
            "Bump pressure monitoring (early/late/absent bump interpretation)"
        ],
        primary_authority=[
            "API Spec 10D - Bow-Spring Casing Centralizers (includes plug specifications)",
            "Well Cementing (Schlumberger) Chapter 7 - Primary Cementing Operations",
            "IADC Drilling Manual - Cementing Equipment and Procedures"
        ],
        burden_holder="Service company executes plug cementing; Operator monitors and approves",
        adversary_position="Plug failure → cement contamination, poor zonal isolation, TOC uncertainty",
        counter_arguments=[
            "Single-plug cementing adequate for shallow wells",
            "Continuous circulation systems eliminate plug-related failures",
            "Plug bypass rare with proper plug selection",
            "Bump pressure not definitive (can have false positives from restrictions)"
        ],
        resolution_strategy="Calculate casing and displacement volumes accurately. Select plugs rated for casing ID. Pressure test float equipment before cementing. Monitor pressure during displacement for bottom plug rupture and top plug bump. Investigate if bump pressure absent or occurs at wrong volume. Verify TOC with temperature log or CBL.",
        entity_scope="Service companies, operators, drilling engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Two-plug method is industry standard for primary cementing; procedure well-documented in API standards",
        controlling_precedent="API Spec 10D plug specifications; industry best practices (Schlumberger, Halliburton cementing manuals)",
        issue_category=IssueCategory.PRIMARY_CEMENTING,
        zone=AnalysisZone.EXECUTION
    ),

    # Additional doctrine blocks for comprehensive coverage

    DoctrineBlock(
        topic="Liner Cementing with DV Tool",
        keywords=["liner", "DV tool", "differential valve", "liner hanger", "liner top packer", "reverse circulation"],
        conclusion_template=[
            "Liner cementing requires differential valve (DV) tool for stage cementing and reverse circulation.",
            "DV tool opens ports above liner top for circulation after liner cementing.",
            "Critical: verify DV tool closes before displacing cement to prevent cement in casing above liner."
        ],
        reasoning_framework="""
**Liner cementing** is cementing a section of casing that does not extend to surface, hung from a liner hanger.

**DV tool (Differential Valve)**:
- Mechanical or hydraulic valve positioned just above liner top
- **Closed position**: During liner cementing, allows cement to flow down liner and up annulus
- **Open position**: After cementing, opens side ports for reverse circulation or stage cementing

**Liner cementing sequence**:

1. **Run liner**: Drill pipe with liner attached, DV tool above liner hanger
2. **Set liner hanger**: Mechanical or hydraulic activation, supports liner weight
3. **Circulate mud**: Condition hole, verify circulation through DV tool (ports open)
4. **Close DV tool**: Drop ball or apply pressure to close ports (cement path now through liner)
5. **Pump cement**: Down drill pipe, through liner, up annulus behind liner
6. **Displace cement**: Pump mud to displace cement into annulus (DV tool closed prevents cement entering casing above)
7. **Bump plug**: Plug lands on float collar in liner, confirms displacement
8. **Open DV tool**: Rotate drill pipe or apply reverse pressure to open side ports
9. **Reverse circulate**: Pump down annulus, returns through DV tool ports and up drill pipe (cleans excess cement from annulus)
10. **Pull out**: Release from liner hanger, pull drill pipe and DV tool

**DV tool types**:

1. **Mechanical ball-activated**:
   - Drop ball to close ports
   - Rotate pipe to shear pin, open ports
   - Simple, reliable, but requires pipe rotation

2. **Hydraulic pressure-differential**:
   - Apply pressure differential to close/open
   - No mechanical manipulation required
   - Example: Apply 1000 psi to close, release pressure to open

3. **Single-stage vs multi-stage**:
   - **Single-stage**: One set of ports, one cementing operation
   - **Multi-stage**: Multiple port sets, allows staged cementing (e.g., isolate loss zone mid-liner)

**Liner top cement placement**:
- **Goal**: Cement overlap ("tie-back") into casing above liner by 200-500 ft minimum
- **Challenge**: Accurate TOC prediction difficult (annular geometry changes at liner top)
- **Verification**: Temperature log, radioactive tracer, CBL

**Liner top packer (LTP)**:
- **Alternative to DV tool**: Inflatable packer set above liner top
- **Function**: Creates seal, allows cementing liner without contaminating casing above
- **Advantage**: Positive isolation, no reverse circulation needed
- **Disadvantage**: Adds cost, complexity, potential stuck pipe if packer fails to deflate

**Common issues**:

1. **DV tool failure to close**:
   - **Result**: Cement flows into casing above liner during displacement
   - **Prevention**: Test DV tool on surface before running

2. **DV tool failure to open**:
   - **Result**: Cannot reverse circulate, excess cement remains in annulus above liner top
   - **Mitigation**: May still achieve isolation if TOC adequate, but unable to clean annulus

3. **Liner hanger slippage**:
   - **Cause**: Insufficient setting force, cement slurry weight exceeds design
   - **Result**: Liner drops, TOC falls below target
   - **Prevention**: Verify liner hanger load rating exceeds cement column weight + safety factor

4. **Liner rotation with DV tool**:
   - **Contraindication**: Some DV tools prohibit rotation during cementing
   - **Trade-off**: Cannot rotate liner to improve displacement (unlike casing strings)

**Displacement calculations**:
- **Liner internal volume**: V_liner = 0.1776 × ID² × L_liner (ID in inches, L in feet, V in BBL)
- **Annular volume** (liner to openhole): V_annulus = 0.1776 × (D_hole² - OD_liner²) × L_liner
- **DV tool to liner top**: Typically 10-30 ft, minor volume (~1-3 BBL)
- **Displacement volume**: V_displace = V_liner - V_cement_pumped + V_liner_shoe_track
        """,
        key_factors=[
            "DV tool type and operating mechanism (ball drop, pressure, rotation)",
            "Liner hanger setting force and load rating",
            "Cement volume design for liner top overlap (tie-back)",
            "Reverse circulation plan after cementing",
            "TOC verification method (temperature log, tracer)"
        ],
        primary_authority=[
            "API Spec 11D1 - Packers and Bridge Plugs (covers liner hangers)",
            "SPE 25436 - Liner Cementing Practices (1993)",
            "Service company technical manuals (Halliburton, Baker Hughes liner systems)"
        ],
        burden_holder="Operator designs liner program; service company executes DV tool operation",
        adversary_position="DV tool failure → cement in casing above liner, or inability to clean annulus",
        counter_arguments=[
            "Liner top packer (LTP) more reliable than DV tool",
            "Excess cement above liner acceptable if not blocking production",
            "Can mill out cement above liner if DV tool fails to open",
            "Modern DV tools have high reliability (>95% success rate)"
        ],
        resolution_strategy="Select DV tool compatible with liner hanger system. Test DV tool function on surface. Calculate displacement volumes including DV tool volume. Monitor pressure for DV tool closure confirmation. Plan reverse circulation volume to clean annulus above liner top. Verify TOC with temperature log.",
        entity_scope="Operators, service companies, drilling engineers, completion engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Liner cementing with DV tools is standard practice; API Spec 11D1 covers equipment standards",
        controlling_precedent="API Spec 11D1 liner hanger specifications; SPE 25436 field procedures",
        issue_category=IssueCategory.PRIMARY_CEMENTING,
        zone=AnalysisZone.EXECUTION
    ),

    DoctrineBlock(
        topic="Cement Contamination - Mud/Cement Mixing",
        keywords=["contamination", "transition zone", "flocculation", "compatibility", "spacer", "wash"],
        conclusion_template=[
            "Cement contamination from mud mixing creates weak transition zones with low strength and high permeability.",
            "Incompatible fluids cause flocculation: oil-based mud + water-based cement.",
            "Prevention: effective spacers (50-200 BPL), chemical washes, density hierarchy, turbulent displacement."
        ],
        reasoning_framework="""
**Cement contamination** occurs when drilling mud mixes with cement slurry, creating a weak transition zone.

**Contamination mechanisms**:

1. **Direct mixing**:
   - Laminar flow in annulus → stable mud layer not displaced by cement
   - Mud channels bypass cement in eccentric annulus
   - Insufficient spacer/wash volume

2. **Incompatibility reactions**:
   - **Oil-based mud (OBM) + water-based cement**:
     * Oil film on casing/formation prevents cement bonding
     * Emulsification creates viscous, unpumpable sludge
     * **Severity**: Most severe contamination type

   - **Water-based mud (WBM) + cement**:
     * Clay particles from mud disperse in cement → increased viscosity
     * Bentonite swelling reduces cement permeability (can be beneficial)
     * **pH shock**: High pH cement (12-13) may flocculate low pH mud

   - **Synthetic-based mud (SBM) + cement**:
     * Similar to OBM, but less severe (synthetic oils more compatible)
     * Still requires effective spacer/wash

3. **Gelation and flocculation**:
   - **Flocculation**: Cement particles aggregate into weak clusters due to contamination
   - **Result**: "Dirty cement" with low compressive strength (<500 psi), high permeability (>1 mD)
   - **Appearance**: Dark brown/gray color (vs clean cement = light gray)

**Prevention strategies**:

1. **Spacer design**:
   - **Volume**: 50-200 BPL (10 min contact time at critical zones)
   - **Density**: Intermediate between mud and cement (ρ_mud < ρ_spacer < ρ_cement)
   - **Viscosity**: 40-100 sec Marsh funnel (scrubbing action)
   - **Composition**:
     * Water-based: Bentonite gel + weighing agent + dispersant
     * Surfactant-based: Detergent/solvent (for OBM) 2-5% + viscosifier
   - **Function**: Physically separates mud/cement, scrubs casing/formation

2. **Chemical wash** (for OBM/SBM):
   - **Surfactant wash**: 5-10 BPL high-concentration detergent (10-15%)
   - **Solvent wash**: Diesel, mineral oil, or mutual solvent 5-10 BPL
   - **Function**: Dissolves oil film, makes surface water-wet for cement bonding
   - **Sequence**: Wash → Water flush → Spacer → Cement
   - **Contact time**: Slow displacement (1-2 BPM) for 10-15 min at critical zones

3. **Turbulent flow displacement**:
   - Reynolds number Re > 3000 (see displacement efficiency doctrine)
   - Breaks mud gel structure, reduces stable mud channels
   - **Trade-off**: Higher ECD may risk fracturing weak formations

4. **Density hierarchy**:
   - Maintain ρ_mud < ρ_wash < ρ_spacer < ρ_cement
   - Prevents lighter fluid fingering through heavier fluid
   - **Example**: 12.5 ppg OBM → 13.0 ppg surfactant wash → 14.0 ppg spacer → 16.0 ppg cement

5. **Centralization**:
   - >70% standoff (API RP 10D-2) ensures uniform annular velocity
   - Reduces eccentric channeling where mud bypasses cement

**Testing mud/cement compatibility**:

1. **API compatibility test** (API RP 10B-2 Annex E):
   - Mix cement and mud in ratios: 100:0, 90:10, 75:25, 50:50, 0:100
   - Measure thickening time, compressive strength at 24 hr
   - **Acceptance**: <20% strength loss at 90:10 mix, <50% at 75:25
   - **Failure**: Flocculation, excessive thickening time increase, or <500 psi at any ratio

2. **Visual compatibility**:
   - Mix small samples, observe for color change, flocculation, or phase separation
   - **Poor compatibility**: Immediate darkening, clumps, or oil separation

**Remedial actions if contamination suspected**:
- **During cementing**: If returns show contaminated cement (dark color, low viscosity), continue pumping clean cement until returns clear
- **Post-cement**: CBL will show poor bond (high E1 amplitude). May require squeeze cementing to repair.

**Field indicators of contamination**:
- **Returns color**: Dark brown/gray instead of light gray
- **Thickening time**: Faster or slower than lab-tested values
- **Density**: Lower than pumped (water separation from flocculation)
- **Rheology**: Increased viscosity, gelling
        """,
        key_factors=[
            "Mud type (OBM, SBM, WBM) and compatibility with water-based cement",
            "Spacer/wash design (volume, density, viscosity, chemical composition)",
            "Displacement rate and flow regime (turbulent preferred)",
            "Density hierarchy maintenance",
            "API compatibility test results"
        ],
        primary_authority=[
            "API RP 10B-2 Annex E - Mud/Cement Compatibility Testing",
            "SPE 106876 - Spacer Design for Optimal Mud Displacement (2007)",
            "Well Cementing (Schlumberger) Chapter 5 - Mud Removal"
        ],
        burden_holder="Service company designs spacer/wash; Operator approves based on mud system",
        adversary_position="Cement contamination → weak transition zone, microannuli, poor CBL, gas migration pathway",
        counter_arguments=[
            "Small amounts of contamination acceptable if bulk cement is sound",
            "Bentonite from WBM contamination can reduce cement permeability (beneficial)",
            "Modern spacers nearly eliminate contamination risk",
            "Turbulent flow may not be achievable without risking lost circulation"
        ],
        resolution_strategy="Conduct API mud/cement compatibility testing before job. Design spacer with intermediate density and 50-200 BPL volume. Use chemical wash if OBM/SBM (surfactant or solvent). Plan turbulent displacement (Re >3000). Monitor returns for contamination (color, density). Run CBL to verify bond quality post-cement.",
        entity_scope="Operators, service companies, mud engineers, cementing engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API RP 10B-2 Annex E testing is industry standard; spacer design practices well-established",
        controlling_precedent="API RP 10B-2 Annex E compatibility testing; SPE 106876 spacer design",
        issue_category=IssueCategory.CONTAMINATION,
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Free Water and Cement Settling",
        keywords=["free water", "sedimentation", "settling", "water channel", "slurry stability", "anti-settling agents"],
        conclusion_template=[
            "Free water is water that separates from cement slurry and rises to top of column.",
            "API limit: <5.2 mL per 250 mL slurry after 2 hours at BHST.",
            "Prevention: reduce water/cement ratio, add bentonite or dispersants, ensure downward cement placement."
        ],
        reasoning_framework="""
**Free water** is gravitational water separation from cement slurry during static period before setting.

**Mechanism**:
1. Cement particles (density ~3.15 g/cm³) settle downward under gravity
2. Water (density 1.0 g/cm³) rises upward, accumulates at top
3. Creates **water channel** at top of cement column → permeable pathway, no zonal isolation

**API test** (API RP 10B-2 Section 9):
- Pour 250 mL slurry into graduated cylinder
- Incline at 45° (simulates deviated wellbore)
- Cure at BHST (bottomhole static temperature) for 2 hours
- Measure water volume at top
- **Limit**: <5.2 mL (2% by volume) is acceptable
- **Severe**: >10 mL indicates unstable slurry, unacceptable

**Factors increasing free water**:

1. **High water/cement ratio**:
   - Standard Class H: W/C = 0.38 (38% water by weight of cement)
   - Excess water (W/C >0.45): More free water, lower strength
   - **Solution**: Use dispersants to reduce W/C while maintaining pumpability

2. **Low slurry density**:
   - Lightweight cements (extended with perlite, bentonite) more prone to settling
   - Less cement mass to retain water in matrix

3. **High temperature**:
   - Accelerates hydration → faster water release
   - Reduces slurry viscosity → easier particle settling

4. **Inadequate mixing**:
   - Poor dispersion → agglomerated particles settle faster
   - Non-uniform density → localized settling

5. **Static conditions**:
   - Deviated/horizontal wells: Cement static for hours before setting
   - Vertical wells less susceptible (water channel at very top, may not affect critical zones)

**Sedimentation (settling)**:
- Related to free water but distinct: solid particles settle to bottom, water-rich layer at top
- **Consequence**: Density stratification, bottom = heavy (overstressed formation), top = light (weak, permeable)

**Prevention methods**:

1. **Reduce W/C ratio**:
   - Use **dispersants**: Polynaphthalene sulfonate (PNS) 0.3-0.8% BWOC, or polycarboxylate 0.1-0.5%
   - Allows lower water content while maintaining low viscosity
   - Target W/C ≤ 0.40 for Class H

2. **Anti-settling agents**:
   - **Bentonite**: 1-2% BWOC increases gel strength, suspends particles
   - **Synthetic polymers**: Xanthan gum, cellulose derivatives 0.1-0.5%
   - **Mechanism**: Increase yield point and gel strength, prevent settling

3. **Weighting agents**:
   - Replace some mix water with high-density additives (hematite, ilmenite)
   - Reduces W/C ratio, maintains target density

4. **Thixotropic additives**:
   - Develop high gel strength under static conditions
   - Prevents settling once cement is placed

5. **Downward slurry placement**:
   - Pump cement down drill pipe (inside casing or tubing), displaces upward
   - Gravity aids particle suspension (opposite of conventional annular placement)
   - Commonly used for liners, squeeze cementing

6. **Pipe movement during WOC**:
   - **Contraindication**: Avoid disturbing cement during initial set (may create channels)
   - Only applicable during pumping/displacement phase

**Horizontal/deviated well considerations**:
- **Worse settling**: 45-90° inclination maximizes free water accumulation
- **Water channel**: Forms on high side of casing → preferential gas migration path
- **Mitigation**: Essential to use anti-settling agents, reduce W/C ratio, consider foamed cement (no free water by definition)

**Testing protocol**:
- Run free water test at BHST and planned inclination (45° if deviated well)
- If >5.2 mL, adjust slurry:
  * Add bentonite 0.5-1.0% BWOC
  * Add dispersant 0.2-0.5% to allow W/C reduction
  * Retest until <5.2 mL
        """,
        key_factors=[
            "Water/cement ratio (target ≤0.40 for Class H)",
            "API free water test results at BHST and inclination",
            "Anti-settling agent type and concentration",
            "Well inclination (deviated wells higher risk)",
            "Slurry density and lightweight additives"
        ],
        primary_authority=[
            "API RP 10B-2 Section 9 - Free Water Test (2013)",
            "API Spec 10A Section 9 - Free Water Requirements",
            "SPE 11207 - Sedimentation in Cement Slurries (1982)"
        ],
        burden_holder="Service company designs slurry to meet free water specification; Operator sets acceptance criteria",
        adversary_position="Excessive free water → water channels, permeable pathways, failed zonal isolation, gas migration",
        counter_arguments=[
            "Small amount of free water acceptable if it accumulates above productive zones",
            "Free water at 2 hr does not predict final state after full curing",
            "Bentonite increases viscosity and may increase ECD",
            "Horizontal wells may tolerate higher free water if top side is not critical"
        ],
        resolution_strategy="Conduct API free water test at BHST and 45° inclination. If >5.2 mL, add bentonite 1-2% BWOC or reduce W/C with dispersant. Retest until <5.2 mL. For horizontal/deviated wells, target <3 mL. Document test results and slurry adjustments.",
        entity_scope="Service companies, lab technicians, well engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API free water test is industry standard; <5.2 mL acceptance criteria is API Spec 10A requirement",
        controlling_precedent="API Spec 10A Section 9; API RP 10B-2 free water test procedure",
        issue_category=IssueCategory.TESTING,
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Thickening Time and API Schedules",
        keywords=["thickening time", "consistency", "Bearden unit", "API schedule", "BHCT", "pressure schedule"],
        conclusion_template=[
            "Thickening time is time for cement to reach 70 Bc (Bearden units of consistency) at BHCT.",
            "Must exceed total pumping time plus displacement time by 1.5× safety factor minimum.",
            "API Schedules 4-9 simulate different well depth/temperature conditions."
        ],
        reasoning_framework="""
**Thickening time** is the duration cement slurry remains pumpable before reaching unacceptable consistency.

**API definition** (API RP 10B-2 Section 7):
- Time to reach **70 Bc** (Bearden consistency units) under simulated downhole conditions
- **70 Bc**: Arbitrary but reproducible threshold representing practical pumpability limit
- **100 Bc**: Equivalent to viscosity where slurry cannot be agitated (full gelation)

**Consistometer test**:
- **Equipment**: HPHT consistometer (high-pressure, high-temperature), rotating slurry paddle
- **Measurement**: Torque required to rotate paddle at constant speed (150 RPM)
- **Conversion**: Torque → Bearden consistency (Bc) via calibration
- **Conditions**: Ramp temperature and pressure per API Schedule to simulate wellbore

**API Schedules** (temperature/pressure ramps):

| Schedule | Application | Max Depth (ft) | BHCT (°F) | Pressure (psi) | Ramp Time (min) |
|----------|-------------|----------------|-----------|----------------|-----------------|
| 4 | Shallow, cold | 0-6,000 | 80-120 | 3,000 | 30 |
| 5 | Intermediate | 6,000-10,000 | 120-170 | 6,000 | 60 |
| 6 | Intermediate-deep | 8,000-12,000 | 140-200 | 8,000 | 75 |
| 7 | Deep | 10,000-14,000 | 170-230 | 10,000 | 90 |
| 8 | Deep-HPHT | 12,000-16,000 | 200-260 | 12,000 | 105 |
| 9 | HPHT | >14,000 | >230 | >14,000 | 120 |

**Schedule selection**:
- Based on true vertical depth (TVD) and bottomhole circulating temperature (BHCT)
- **Conservative approach**: Use schedule for next-higher depth if between categories
- **BHCT calculation**:
  * Circulating temperature lower than static due to mud cooling
  * BHCT ≈ BHST - (10-30°F) depending on circulation rate and time
  * Use thermal simulator (e.g., Halliburton's WellPlan) for accurate BHCT

**Thickening time design criteria**:

1. **Minimum thickening time**:
   - T_thick ≥ 1.5 × (T_mixing + T_pumping + T_displacement)
   - **T_mixing**: 15-30 min (batch mixing on surface)
   - **T_pumping**: Actual cement slurry pumping time (calculated or historical)
   - **T_displacement**: Mud displacement time (calculated from displacement volume and rate)
   - **Safety factor**: 1.5 is minimum, 2.0 preferred for critical wells

2. **Example calculation**:
   - Mixing: 20 min
   - Pumping: 120 min (2 hours cement slurry volume)
   - Displacement: 45 min
   - Total: 185 min
   - **Required thickening time**: 185 × 1.5 = **278 min (4.6 hr) minimum**

3. **Margin assessment**:
   - If thickening time = 6 hr, margin = 6 - 4.6 = 1.4 hr (84 min) → acceptable
   - If thickening time = 5 hr, margin = 0.4 hr (24 min) → tight, increase retarder

**Factors affecting thickening time**:

1. **Temperature** (dominant factor):
   - Every 10°F increase → ~20-30% reduction in thickening time (Arrhenius relationship)
   - **Critical**: Use BHCT, not surface temperature

2. **Pressure**:
   - Higher pressure slightly increases thickening time (~5-10% per 5,000 psi)
   - Less significant than temperature effect

3. **Cement type**:
   - Class C: ~2-3 hr at 80°F (fast-setting)
   - Class H: ~3-4 hr at 80°F (slower than Class C)
   - Class G: ~2.5-3.5 hr at 80°F

4. **Additives**:
   - **Retarders**: Increase thickening time (see retarder doctrine)
   - **Accelerators** (CaCl2, NaCl): Decrease thickening time
   - **Dispersants**: Minimal effect on thickening time

5. **Water/cement ratio**:
   - Higher W/C → slightly longer thickening time (dilution effect)

**Accelerated testing**:
- Test at BHCT + 10-20°F provides conservative result (shorter thickening time)
- Safer margin if actual well temperature is lower than predicted

**Real-time monitoring**:
- Some service companies use real-time consistometers on cementing unit
- Monitors actual slurry consistency during pumping
- Allows adjustment of pump rate if thickening faster/slower than predicted

**Failure consequences**:
- **Insufficient thickening time**: Cement gels before fully placed → stuck pipe, incomplete displacement, poor bonding
- **Excessive thickening time**: Unnecessary cost (retarder), may increase transition time and gas migration risk
        """,
        key_factors=[
            "Accurate BHCT from thermal modeling",
            "Total pumping time (mixing + pumping + displacement)",
            "API schedule selection based on depth and temperature",
            "Safety factor (1.5-2.0×) applied to total time",
            "Temperature sensitivity of cement/retarder system"
        ],
        primary_authority=[
            "API RP 10B-2 Section 7 - Thickening Time Testing (2013)",
            "API Spec 10A Table 1 - Thickening Time Requirements by Schedule",
            "SPE Monograph - Well Cementing (1990) Chapter 3"
        ],
        burden_holder="Service company conducts testing and designs slurry; Operator approves safety margin",
        adversary_position="Insufficient thickening time → premature setting, stuck pipe, poor zonal isolation",
        counter_arguments=[
            "2.0× safety factor may be excessive, adds cost",
            "Real-time monitoring reduces need for high safety margin",
            "Conservative temperature assumptions (BHCT + 10°F) build in margin",
            "Thickening time tests have inherent variability (±30 min typical)"
        ],
        resolution_strategy="Calculate total pumping time (mixing + pumping + displacement). Model BHCT using thermal simulator. Select appropriate API schedule. Test thickening time at BHCT. Verify thickening time ≥ 1.5 × total time (prefer 2.0×). If insufficient, increase retarder concentration and retest.",
        entity_scope="Service companies, lab technicians, well engineers, cementing engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API RP 10B-2 thickening time testing is industry standard; 1.5-2.0× safety factor is best practice",
        controlling_precedent="API RP 10B-2 Section 7; API Spec 10A thickening time specifications",
        issue_category=IssueCategory.TESTING,
        zone=AnalysisZone.PLANNING
    ),
]


# ============================================================================
# TELEMETRY & MONITORING
# ============================================================================

class TelemetryCollector:
    def __init__(self):
        self.queries_total = 0
        self.latencies_ms: List[float] = []
        self.doctrine_hit_counts: Dict[str, int] = {}
        self.error_counts: Dict[str, int] = {}
        self.start_time = time.time()

    def record_query(self, latency_ms: float, doctrines_used: List[str], error: Optional[str] = None):
        self.queries_total += 1
        self.latencies_ms.append(latency_ms)
        for doctrine in doctrines_used:
            self.doctrine_hit_counts[doctrine] = self.doctrine_hit_counts.get(doctrine, 0) + 1
        if error:
            self.error_counts[error] = self.error_counts.get(error, 0) + 1

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "total_queries": self.queries_total,
            "avg_latency_ms": np.mean(self.latencies_ms) if self.latencies_ms else 0.0,
            "p95_latency_ms": np.percentile(self.latencies_ms, 95) if self.latencies_ms else 0.0,
            "uptime_seconds": time.time() - self.start_time,
            "doctrine_hit_rate": len(self.doctrine_hit_counts) / len(DOCTRINE_CACHE) if DOCTRINE_CACHE else 0.0,
            "error_rate": sum(self.error_counts.values()) / max(self.queries_total, 1),
            "top_doctrines": sorted(self.doctrine_hit_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }


# ============================================================================
# CORE ENGINE
# ============================================================================

class DRL05CementingEngine:
    def __init__(self):
        self.telemetry = TelemetryCollector()
        self.doctrine_cache = DOCTRINE_CACHE
        logger.info(f"DRL05 Cementing Engine initialized with {len(self.doctrine_cache)} doctrine blocks")

    def semantic_normalize(self, query: str) -> str:
        """Normalize cementing-specific terminology"""
        replacements = {
            "API 10A": "API Spec 10A",
            "CBL": "cement bond log",
            "VDL": "variable density log",
            "BHCT": "bottomhole circulating temperature",
            "BHST": "bottomhole static temperature",
            "DV tool": "differential valve tool",
            "LCM": "lost circulation material",
            "OBM": "oil-based mud",
            "WBM": "water-based mud",
            "SBM": "synthetic-based mud",
            "BWOC": "by weight of cement",
            "ppg": "pounds per gallon",
            "Bc": "Bearden consistency",
            "TOC": "top of cement",
            "WOC": "wait on cement",
            "ECD": "equivalent circulating density",
        }
        normalized = query.lower()
        for abbrev, full in replacements.items():
            normalized = normalized.replace(abbrev.lower(), full.lower())
        return normalized

    def three_layer_response(self, query: str, mode: ResponseMode, max_depth: int) -> Tuple[str, List[str], List[str], ConfidenceLevel, List[str]]:
        """TIE-20 Component: Three-layer retrieval (cache → semantic → deep analysis)"""
        normalized_query = self.semantic_normalize(query)
        query_tokens = set(normalized_query.split())

        # Layer 1: Doctrine cache (fast path, 0-50ms)
        cache_hits = []
        for doctrine in self.doctrine_cache:
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in normalized_query)
            if keyword_matches >= 2 or any(kw.lower() in query_tokens for kw in doctrine.keywords[:3]):
                cache_hits.append(doctrine)

        if cache_hits:
            logger.info(f"Cache hit: {len(cache_hits)} doctrine blocks matched")
            return self._synthesize_response(cache_hits, query, mode, "cache")

        # Layer 2: Semantic search (fallback, 50-200ms)
        logger.info("Cache miss, performing semantic search")
        semantic_hits = self._semantic_search(normalized_query, top_k=5)
        if semantic_hits:
            return self._synthesize_response(semantic_hits, query, mode, "semantic")

        # Layer 3: Deep analysis (200-1000ms)
        logger.warning("Semantic search miss, performing deep analysis")
        all_relevant = self._deep_analysis(query, max_depth)
        return self._synthesize_response(all_relevant, query, mode, "deep")

    def _semantic_search(self, query: str, top_k: int = 5) -> List[DoctrineBlock]:
        """Semantic retrieval using keyword scoring"""
        query_tokens = set(query.lower().split())
        scores = []
        for doctrine in self.doctrine_cache:
            keyword_score = sum(2 if kw.lower() in query else 1 if any(kw.lower() in qt for qt in query_tokens) else 0
                              for kw in doctrine.keywords)
            framework_score = sum(1 for qt in query_tokens if qt in doctrine.reasoning_framework.lower())
            total_score = keyword_score * 2 + framework_score
            if total_score > 0:
                scores.append((total_score, doctrine))

        scores.sort(reverse=True, key=lambda x: x[0])
        return [d for _, d in scores[:top_k]]

    def _deep_analysis(self, query: str, max_depth: int) -> List[DoctrineBlock]:
        """Deep multi-doctrine analysis"""
        categories = self._categorize_query(query)
        relevant = [d for d in self.doctrine_cache if d.issue_category in categories]
        return relevant[:max_depth]

    def _categorize_query(self, query: str) -> List[IssueCategory]:
        """Categorize query into issue domains"""
        q_lower = query.lower()
        categories = []

        if any(term in q_lower for term in ["class", "API", "cement type", "portland"]):
            categories.append(IssueCategory.SLURRY_DESIGN)
        if any(term in q_lower for term in ["retarder", "accelerator", "fluid loss", "additive", "latex"]):
            categories.append(IssueCategory.ADDITIVES)
        if any(term in q_lower for term in ["displacement", "spacer", "wash", "primary cement", "two plug"]):
            categories.append(IssueCategory.PRIMARY_CEMENTING)
        if any(term in q_lower for term in ["squeeze", "remedial", "repair", "hesitation"]):
            categories.append(IssueCategory.REMEDIAL_CEMENTING)
        if any(term in q_lower for term in ["CBL", "bond log", "VDL", "ultrasonic", "evaluation"]):
            categories.append(IssueCategory.CEMENT_EVALUATION)
        if any(term in q_lower for term in ["gas migration", "annular pressure", "right angle", "transition time"]):
            categories.append(IssueCategory.GAS_MIGRATION)
        if any(term in q_lower for term in ["HPHT", "high temperature", "silica", "retrogression"]):
            categories.append(IssueCategory.HPHT_OPERATIONS)
        if any(term in q_lower for term in ["lost circulation", "thief", "foam cement", "lightweight"]):
            categories.append(IssueCategory.LOST_CIRCULATION)
        if any(term in q_lower for term in ["contamination", "mixing", "compatibility", "flocculation"]):
            categories.append(IssueCategory.CONTAMINATION)
        if any(term in q_lower for term in ["thickening time", "free water", "settling", "test"]):
            categories.append(IssueCategory.TESTING)

        return categories if categories else [IssueCategory.SLURRY_DESIGN]

    def _synthesize_response(self, doctrines: List[DoctrineBlock], query: str, mode: ResponseMode, source: str) -> Tuple[str, List[str], List[str], ConfidenceLevel, List[str]]:
        """Synthesize answer from doctrine blocks"""
        if not doctrines:
            return ("Insufficient cementing doctrine to answer query. Recommend consulting API Spec 10A, API RP 10B-2, or service company technical manual.",
                    [], [], ConfidenceLevel.DISCLOSURE, ["No relevant doctrine blocks found"])

        # Build response based on mode
        if mode == ResponseMode.FAST:
            answer = self._build_fast_response(doctrines, query)
        elif mode == ResponseMode.DEFENSE:
            answer = self._build_defense_response(doctrines, query)
        else:  # MEMO
            answer = self._build_memo_response(doctrines, query)

        # Aggregate metadata
        authorities = []
        reasoning_chain = []
        for d in doctrines:
            authorities.extend(d.primary_authority)
            reasoning_chain.append(f"{d.topic}: {d.conclusion_template[0]}")

        # Determine confidence
        confidence = self._assess_confidence(doctrines)

        # Identify coverage gaps
        gaps = self._identify_gaps(query, doctrines)

        doctrine_names = [d.topic for d in doctrines]

        return (answer, doctrine_names, reasoning_chain, confidence, gaps)

    def _build_fast_response(self, doctrines: List[DoctrineBlock], query: str) -> str:
        """FAST mode: Concise, actionable answer"""
        primary = doctrines[0]
        answer_parts = [
            f"**{primary.topic}**",
            "",
            primary.conclusion_template[0],
        ]

        if len(doctrines) > 1:
            answer_parts.append("")
            answer_parts.append("**Related considerations:**")
            for d in doctrines[1:3]:
                answer_parts.append(f"- {d.topic}: {d.conclusion_template[0]}")

        answer_parts.extend([
            "",
            f"**Primary authority:** {primary.primary_authority[0]}",
        ])

        return "\n".join(answer_parts)

    def _build_defense_response(self, doctrines: List[DoctrineBlock], query: str) -> str:
        """DEFENSE mode: Audit-ready, fully cited"""
        answer_parts = [
            "# Cementing Analysis",
            "",
            f"**Query:** {query}",
            "",
            "## Analysis",
            ""
        ]

        for i, d in enumerate(doctrines[:3], 1):
            answer_parts.extend([
                f"### {i}. {d.topic}",
                "",
                "**Conclusions:**"
            ])
            for conclusion in d.conclusion_template:
                answer_parts.append(f"- {conclusion}")

            answer_parts.extend([
                "",
                "**Key factors:**"
            ])
            for factor in d.key_factors[:5]:
                answer_parts.append(f"- {factor}")

            answer_parts.extend([
                "",
                "**Authorities:**"
            ])
            for auth in d.primary_authority:
                answer_parts.append(f"- {auth}")

            answer_parts.extend([
                "",
                f"**Confidence:** {d.confidence.value}",
                ""
            ])

        return "\n".join(answer_parts)

    def _build_memo_response(self, doctrines: List[DoctrineBlock], query: str) -> str:
        """MEMO mode: Full documentation with reasoning frameworks"""
        answer_parts = [
            "# CEMENTING OPERATIONS MEMORANDUM",
            "",
            f"**Subject:** {query}",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d')}",
            f"**Engine:** DRL05 Cementing Operations Intelligence Engine v1.0",
            "",
            "---",
            "",
            "## EXECUTIVE SUMMARY",
            ""
        ]

        for d in doctrines[:2]:
            for conclusion in d.conclusion_template:
                answer_parts.append(f"- {conclusion}")

        answer_parts.extend([
            "",
            "## DETAILED ANALYSIS",
            ""
        ])

        for i, d in enumerate(doctrines, 1):
            answer_parts.extend([
                f"### {i}. {d.topic}",
                "",
                "#### Reasoning Framework",
                "",
                d.reasoning_framework,
                "",
                "#### Key Factors",
                ""
            ])
            for factor in d.key_factors:
                answer_parts.append(f"- {factor}")

            answer_parts.extend([
                "",
                "#### Resolution Strategy",
                "",
                d.resolution_strategy,
                "",
                "#### Counter-Arguments",
                ""
            ])
            for arg in d.counter_arguments[:3]:
                answer_parts.append(f"- {arg}")

            answer_parts.extend([
                "",
                f"**Confidence Stratification:** {d.confidence_stratification}",
                "",
                "---",
                ""
            ])

        answer_parts.extend([
            "## AUTHORITIES",
            ""
        ])
        all_authorities = []
        for d in doctrines:
            all_authorities.extend(d.primary_authority)
        for auth in sorted(set(all_authorities)):
            answer_parts.append(f"- {auth}")

        return "\n".join(answer_parts)

    def _assess_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Assess overall confidence from doctrine blocks"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        confidence_scores = {
            ConfidenceLevel.DEFENSIBLE: 4,
            ConfidenceLevel.AGGRESSIVE: 3,
            ConfidenceLevel.DISCLOSURE: 2,
            ConfidenceLevel.HIGH_RISK: 1
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

    def _identify_gaps(self, query: str, doctrines: List[DoctrineBlock]) -> List[str]:
        """Identify coverage gaps"""
        gaps = []
        query_lower = query.lower()

        # Check for specific technical areas not covered
        if "temperature" in query_lower and not any("HPHT" in d.topic or "thickening time" in d.topic for d in doctrines):
            gaps.append("HPHT or thickening time considerations may be relevant")

        if "foam" in query_lower and not any("foam" in d.topic.lower() for d in doctrines):
            gaps.append("Foamed cement design principles not fully addressed")

        if "liner" in query_lower and not any("liner" in d.topic.lower() for d in doctrines):
            gaps.append("Liner-specific cementing considerations may apply")

        if len(doctrines) < 2:
            gaps.append("Limited doctrine coverage - consider additional domain expertise")

        return gaps


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="DRL05 - Cementing Operations Intelligence Engine",
    description="TIE Gold Standard engine for drilling cementing operations domain",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = DRL05CementingEngine()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint - TIE-20 three-layer response"""
    start_time = time.time()

    try:
        logger.info(f"Query received: {request.question[:100]}... (mode: {request.mode})")

        answer, doctrines_used, reasoning_chain, confidence, gaps = engine.three_layer_response(
            request.question,
            request.mode,
            request.max_depth
        )

        latency_ms = (time.time() - start_time) * 1000

        # Generate determinism hash
        hash_input = f"{request.question}|{request.mode}|{answer}"
        determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        # Record telemetry
        engine.telemetry.record_query(latency_ms, doctrines_used)

        logger.info(f"Query completed in {latency_ms:.1f}ms, {len(doctrines_used)} doctrines used, confidence: {confidence}")

        authorities = []
        for d in engine.doctrine_cache:
            if d.topic in doctrines_used:
                authorities.extend(d.primary_authority)

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            doctrine_blocks_used=doctrines_used,
            reasoning_chain=reasoning_chain,
            authorities=list(set(authorities)),
            determinism_hash=determinism_hash,
            latency_ms=latency_ms,
            coverage_gaps=gaps,
            response_mode=request.mode
        )

    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        engine.telemetry.record_query((time.time() - start_time) * 1000, [], error=str(e))
        raise HTTPException(status_code=500, detail=f"Query processing error: {str(e)}")


@APP.get("/health", response_model=HealthResponse)
async def health_check():
    """Health endpoint"""
    metrics = engine.telemetry.get_metrics()

    return HealthResponse(
        status="healthy",
        engine="DRL05_cementing_operations",
        version="1.0.0",
        port=9015,
        doctrine_blocks=len(engine.doctrine_cache),
        uptime_seconds=metrics["uptime_seconds"],
        total_queries=metrics["total_queries"],
        avg_latency_ms=metrics["avg_latency_ms"],
        cache_hit_rate=metrics["doctrine_hit_rate"]
    )


@APP.get("/doctrines")
async def list_doctrines():
    """List all doctrine blocks"""
    return {
        "total": len(engine.doctrine_cache),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "category": d.issue_category.value,
                "zone": d.zone.value,
                "confidence": d.confidence.value
            }
            for d in engine.doctrine_cache
        ]
    }


@APP.get("/metrics")
async def get_metrics():
    """Telemetry metrics endpoint"""
    return engine.telemetry.get_metrics()


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting DRL05 Cementing Operations Engine on port 9015")
    uvicorn.run(APP, host="0.0.0.0", port=9015)
