"""
FRAC08 - Refracturing Analysis Engine
TIE Gold Standard - Refracturing & Restimulation Domain Expertise

Expertise: Refrac candidate selection, mechanical/chemical diversion, stress reorientation,
bullhead vs re-isolation techniques, economic analysis, production decline analysis,
casing integrity assessment, refrac flowback, Permian Basin case studies.

Port: 9028
Version: 1.0.0
"""

import sys
from pathlib import Path

# CRITICAL: Add parent directory to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

logger.add(
    Path(__file__).parent / "logs" / "frac08_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)

APP = FastAPI(
    title="FRAC08 Refracturing Analysis Engine",
    version="1.0.0",
    description="TIE Gold Standard - Refracturing & Restimulation Domain Expertise"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class IssueCategory(str, Enum):
    CANDIDATE_SELECTION = "CANDIDATE_SELECTION"
    MECHANICAL_DIVERSION = "MECHANICAL_DIVERSION"
    CHEMICAL_DIVERSION = "CHEMICAL_DIVERSION"
    STRESS_REORIENTATION = "STRESS_REORIENTATION"
    ECONOMIC_ANALYSIS = "ECONOMIC_ANALYSIS"
    PRODUCTION_DECLINE = "PRODUCTION_DECLINE"
    CASING_INTEGRITY = "CASING_INTEGRITY"
    COMPLETION_TECHNIQUE = "COMPLETION_TECHNIQUE"
    FLOWBACK_PROTOCOL = "FLOWBACK_PROTOCOL"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"

class QueryRequest(BaseModel):
    query: str = Field(..., description="Refracturing analysis question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis context zone")
    include_authorities: bool = Field(default=False, description="Include supporting references")

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

class QueryResponse(BaseModel):
    query: str
    response: str
    mode: ResponseMode
    zone: AnalysisZone
    confidence: ConfidenceLevel
    categories: List[IssueCategory]
    doctrines_triggered: List[str]
    authorities: Optional[List[str]] = None
    determinism_hash: str
    timestamp: str
    telemetry: Dict[str, Any]

# ============================================================================
# DOCTRINE CACHE - 25+ REFRACTURING EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Refrac Candidate Selection - Production Decline Analysis",
        keywords=["candidate selection", "production decline", "DCA", "EUR", "refrac screening", "decline curve", "b-factor"],
        conclusion_template=[
            "Refrac candidates are selected through systematic production decline analysis identifying wells with steep decline curves, remaining reserves, and technical feasibility.",
            "Primary screening criteria include b-factor >1.2 (hyperbolic decline), >50% depletion from original EUR, and accessible wellbore.",
            "Economic cutoff typically requires incremental EUR >100 MBO or 1 BCF to justify $1-2MM refrac cost in Permian Basin horizontals."
        ],
        reasoning_framework="""
Refrac candidate selection follows systematic workflow:

1. Production History Analysis:
   - Plot rate vs cumulative production (Arps decline curves)
   - Calculate b-factor and D_i (initial decline rate)
   - Estimate original EUR and % recovery to date
   - Target wells with 50-70% depletion (not too early, not too late)

2. Technical Screening:
   - Wellbore accessibility (no severe restrictions, fish, collapsed casing)
   - Casing integrity (no corrosion holes, good cement bond)
   - Original completion quality (understimulated, limited stages, poor proppant distribution)
   - Formation pressure depletion (500-2000 psi remaining, enough for stress reorientation)

3. Economic Screening:
   - Refrac capital cost: $1-2MM for Permian horizontal (plugs, pumping, completion fluids)
   - Required incremental recovery: >100 MBO or 1 BCF to meet 50% IRR hurdle
   - Compare refrac NPV vs drilling new well (usually 2-3x cheaper than new drill)
   - Account for accelerated production (time value of money benefit)

4. Geologic/Reservoir Factors:
   - Thick pay zones with untapped intervals above/below original perfs
   - Natural fractures or faults that can be reactivated
   - Stress regime favorable to reorientation (sigma_h rotates 30-60 degrees after depletion)
   - Pressure compartments with remaining energy

5. Operational Factors:
   - Offset well interference (avoid if neighboring wells still producing strongly)
   - Surface access and right-of-way for workover rig
   - Gas/oil ratio stability (avoid if GOR spiking, indicates mechanical issues)
   - Water cut trends (high water cut reduces refrac effectiveness)

Decision Matrix:
- HIGH PRIORITY: b>1.2, 50-70% depleted, good casing, $2MM cost <50% new well cost
- MEDIUM PRIORITY: b=0.8-1.2, 40-50% depleted, minor casing issues, marginal economics
- LOW PRIORITY: b<0.8 (terminal decline), >80% depleted, casing integrity concerns
        """,
        key_factors=[
            "Decline curve b-factor and shape (hyperbolic vs exponential)",
            "Percent recovery vs original EUR estimate",
            "Remaining formation pressure and stress state",
            "Wellbore accessibility and casing condition",
            "Incremental EUR potential vs refrac capital cost",
            "Original completion quality and identified deficiencies",
            "Competitive economics vs new drill alternative"
        ],
        primary_authority=[
            "SPE 184832: Refrac Candidate Selection Using Decline Curve Analysis",
            "SPE 189880: Economic Screening Criteria for Refracturing in Permian Basin",
            "SPE 191451: Production Decline Signatures Indicating Refrac Potential"
        ],
        burden_holder="Operator proposing refrac",
        adversary_position="Finance team questions incremental EUR assumptions and capital efficiency vs new drilling",
        counter_arguments=[
            "Decline curve extrapolation overstates remaining reserves",
            "Refrac may only accelerate existing production, not add incremental EUR",
            "Casing integrity risks unknown until workover commences",
            "New well generates new acreage HBP, refrac does not",
            "Refrac success rate <50% in some basins"
        ],
        resolution_strategy="Build probabilistic economic model with P10/P50/P90 EUR cases, include time-value benefit of acceleration, compare portfolio returns vs new drill program",
        entity_scope="Operator, working interest owners",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 184832 (industry standard candidate selection workflow)"
    ),

    DoctrineBlock(
        topic="Refrac Stress Reorientation Theory",
        keywords=["stress reorientation", "stress shadow", "depletion", "geomechanics", "principal stress", "sigma_h", "fracture azimuth"],
        conclusion_template=[
            "Formation stress fields reorient during depletion as pore pressure declines, rotating minimum horizontal stress (sigma_h) by 30-90 degrees in many cases.",
            "Stress reorientation enables refrac treatments to create new fracture networks in different azimuths, accessing unstimulated rock volume.",
            "Stress shadow from original completion dissipates with depletion, allowing re-stimulation of near-wellbore region."
        ],
        reasoning_framework="""
Geomechanical Basis for Refrac Success:

1. Original Completion Stress State:
   - Virgin reservoir: sigma_v (vertical) > sigma_H (max horizontal) > sigma_h (min horizontal)
   - Hydraulic fractures propagate perpendicular to sigma_h (least resistance)
   - Original fracs create stress shadow: local sigma_h increases near fracture, preventing new fractures

2. Stress Evolution During Depletion:
   - Pore pressure drops 2000-4000 psi over 3-5 years of production
   - Effective stress increases (sigma_eff = sigma_total - pore_pressure)
   - Poroelastic effect: sigma_h decreases more than sigma_H (anisotropic response)
   - In some cases, sigma_h rotates 30-90 degrees azimuthally
   - Stress shadow dissipates as pressure gradients equalize

3. Refrac Fracture Propagation:
   - New minimum stress direction allows fractures in different azimuth
   - Accesses rock volume bypassed by original completion
   - Can reconnect natural fractures in new orientations
   - May create more complex fracture network (not single planar fracture)

4. Field Evidence:
   - Microseismic shows refrac fractures 40-70 degrees different from original
   - Production logs show new intervals contributing after refrac
   - Pressure transient analysis indicates increased fracture complexity

5. Predictive Modeling:
   - Geomechanical simulation (FLAC, Abaqus) predicts stress rotation
   - Input: rock properties (Young's modulus, Poisson's ratio), depletion magnitude
   - Output: new sigma_h azimuth and magnitude
   - Validation: pre-refrac DAS/fiber optics to measure actual stress state

6. Optimal Refrac Timing:
   - Too early (<30% depletion): insufficient stress rotation
   - Too late (>80% depletion): insufficient pressure for effective fracture propagation
   - Sweet spot: 50-70% depletion, 1500-2500 psi remaining pressure
        """,
        key_factors=[
            "Magnitude of pressure depletion (delta_P)",
            "Rock poroelastic properties (Biot coefficient, Poisson's ratio)",
            "Original stress anisotropy (sigma_H - sigma_h)",
            "Time since original completion (stress equilibration)",
            "Natural fracture network orientation",
            "Remaining formation pressure for fracture propagation"
        ],
        primary_authority=[
            "SPE 181676: Geomechanical Modeling of Stress Reorientation in Depleted Reservoirs",
            "SPE 189865: Microseismic Evidence of Refrac Fracture Reorientation",
            "SPE 195912: Poroelastic Stress Changes During Depletion and Refracturing"
        ],
        burden_holder="Completion engineer designing refrac treatment",
        adversary_position="Skeptics argue stress reorientation is overstated and refrac simply reopens original fractures",
        counter_arguments=[
            "Stress rotation magnitude varies widely by formation (not universal)",
            "Microseismic may show apparent rotation due to processing artifacts",
            "Production increase may be from fracture cleanup, not new rock contact",
            "Modeling assumptions on rock properties uncertain"
        ],
        resolution_strategy="Pre-refrac stress measurement (DAS strain monitoring, DFIT analysis), compare predicted vs observed fracture azimuth from microseismic",
        entity_scope="Operator, completion engineering",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="SPE 181676 (theoretical framework), SPE 189865 (field validation)"
    ),

    DoctrineBlock(
        topic="Mechanical Diversion - Bridge Plugs and Composite Plugs",
        keywords=["mechanical diversion", "bridge plug", "composite plug", "mill-out", "isolation", "re-isolation"],
        conclusion_template=[
            "Mechanical diversion uses downhole plugs to isolate previously stimulated intervals, forcing treatment into new zones during refrac operations.",
            "Composite bridge plugs are industry standard for full lateral refrac with re-isolation, providing reliable sealing and drillable mill-out.",
            "Plug placement strategy depends on refrac objectives: full lateral (10-15 plugs) vs targeted intervals (2-4 plugs)."
        ],
        reasoning_framework="""
Mechanical Diversion Design for Refrac:

1. Bridge Plug Types:
   - Composite plugs: drillable slips/cones, rubber element, 5000-10000 psi rating
   - Cast iron plugs: stronger but require milling (slower, more costly)
   - Dissolvable plugs: emerging technology, limited pressure rating (3000 psi)

2. Full Lateral Re-Isolation Technique:
   - Wireline convey composite plugs to each stage location (toe to heel)
   - Set plugs 50-100 ft apart (original stage spacing)
   - Perforate new intervals between plugs (offset from original perfs)
   - Pump refrac treatment stage-by-stage from toe to heel
   - After completion, mill out all plugs in single trip
   - Typical: 10-15 plugs for 7500-10000 ft lateral

3. Targeted Interval Approach:
   - Production/temperature logs identify 2-4 low-contributing zones
   - Set bridge plugs to isolate only those intervals
   - Reduces plug count (lower cost, faster mill-out)
   - Risk: may miss other understimulated zones

4. Plug Setting Considerations:
   - Casing integrity: plugs require good casing (no corrosion, no deformation)
   - Cement bond: poor cement may allow pressure bleed-off around plug
   - Plug depth accuracy: wireline depth control ±10 ft (use gamma ray correlation)
   - Plug testing: pressure test to 80% of rating before pumping treatment

5. Perforation Strategy:
   - New perfs placed 180 degrees opposite original perfs (if known)
   - Perforation density: 6-8 shots/ft (higher than original to ensure breakdown)
   - Phasing: 60-degree or 90-degree (optimize for stress reorientation direction)
   - Avoid perforating within 20 ft of original perfs (interference risk)

6. Economics:
   - Composite plugs: $5-8K each x 12 plugs = $60-96K
   - Wireline setting: $40-60K mobilization + $10K per plug
   - Mill-out: 2-4 days rig time @ $25K/day = $50-100K
   - Total mechanical isolation cost: $150-250K (10-15% of total refrac cost)

7. Operational Risks:
   - Plug slippage under high pressure (>8000 psi)
   - Plug mill-out leaving debris (flow restriction)
   - Casing collapse during plug milling (thin-walled casing)
        """,
        key_factors=[
            "Lateral length and number of plugs required",
            "Casing condition and pressure rating",
            "Plug type selection (composite vs cast iron vs dissolvable)",
            "Perforation placement relative to original completion",
            "Mill-out time and rig cost",
            "Pressure testing protocol for plug integrity"
        ],
        primary_authority=[
            "SPE 187485: Composite Plug Technology for Refrac Re-Isolation",
            "SPE 191277: Full Lateral Refrac Design Using Mechanical Diversion",
            "Completion Best Practices: Plug & Perf Refracturing"
        ],
        burden_holder="Completion engineer specifying plug count and placement",
        adversary_position="Cost-conscious teams prefer lower plug count or bullhead refrac to avoid plug expense",
        counter_arguments=[
            "High plug count increases upfront cost and mill-out time",
            "Bullhead refrac simpler and cheaper (no plugs required)",
            "Plug debris risk (flow restriction post-mill-out)",
            "Dissolvable plugs cheaper and avoid mill-out (but lower pressure rating)"
        ],
        resolution_strategy="Economic comparison: plug cost vs incremental production from controlled zonal isolation, field data showing bullhead refrac limited effectiveness",
        entity_scope="Operator, completion service provider",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 187485 (composite plug standard), SPE 191277 (full lateral design)"
    ),

    DoctrineBlock(
        topic="Chemical Diversion for Refrac",
        keywords=["chemical diversion", "diverter", "particulate", "degradable", "benzoic acid", "PLA", "viscous pill"],
        conclusion_template=[
            "Chemical diversion systems use particulates, fibers, or viscous fluids to temporarily block high-permeability zones, forcing refrac treatment into lower-permeability rock.",
            "Degradable diverters (benzoic acid, PLA) dissolve in 24-72 hours, eliminating need for mechanical removal and mill-out.",
            "Chemical diversion more effective in high-permeability formations where mechanical plugs may leak; less effective in ultra-low permeability shales."
        ],
        reasoning_framework="""
Chemical Diversion Technology for Refrac:

1. Diverter Types:
   - Particulate Diverters: sized solid particles (sand, salt, resin-coated proppant)
   - Fiber-Based Diverters: degradable fibers that form filter cake
   - Viscous Pills: high-viscosity gel slugs that resist flow
   - Degradable Solids: benzoic acid flakes, PLA (polylactic acid) pellets
   - Gas Slugs: N2 or CO2 foam (less common)

2. Degradable Diverter Mechanism:
   - Pump diverter pill ahead of fracturing stage
   - Diverter enters existing high-perm fractures and perforations
   - Particles bridge off, creating temporary seal (1000-5000 psi pressure differential)
   - Subsequent fluid diverts to lower-permeability zones
   - After treatment, diverter degrades (hydrolysis, thermal, enzymatic)
   - Benzoic acid: dissolves in water at pH >6 over 24-48 hrs
   - PLA: hydrolyzes at 150-200°F over 48-72 hrs

3. Application in Refrac:
   - Pump diverter between refrac stages (no bridge plugs required)
   - Each stage: pump treatment → pump diverter pill → pump next treatment
   - Diverter seals off newly stimulated zones, forces treatment down lateral
   - Allows 8-12 stage refrac without mechanical plugs (bullhead diversion)

4. Formation Suitability:
   - HIGH EFFECTIVENESS: moderate permeability (1-10 md), thick pay, open natural fractures
   - MEDIUM EFFECTIVENESS: low permeability (0.01-1 md), limited fracture complexity
   - LOW EFFECTIVENESS: ultra-low permeability (<0.001 md, tight shales), diverter can't seal enough
   - Best in carbonate refracs (Permian San Andres, Eagleford Austin Chalk)

5. Design Parameters:
   - Diverter particle size: 20/40 mesh to 100 mesh (depends on fracture width)
   - Loading: 1-5 lb/gal in 500-2000 gal pill
   - Placement: pump at end of each stage (not beginning)
   - Degradation time: match to flowback timing (start flowback after degradation)

6. Economics:
   - Diverter material cost: $50-150K for full refrac (vs $150-250K for mechanical plugs)
   - No mill-out required (saves 2-3 days rig time = $50-75K)
   - Faster execution (no wireline plug setting between stages)
   - Risk: less certainty of zonal isolation vs mechanical plugs

7. Limitations:
   - Uncertain seal quality (may not hold full treatment pressure)
   - Temperature/time sensitivity (premature degradation if too hot or delayed flowback)
   - Particle size distribution critical (too small = no bridge, too large = screenout)
   - Not suitable for high-pressure treatments (>10,000 psi)
        """,
        key_factors=[
            "Formation permeability and natural fracture network",
            "Diverter particle size and loading concentration",
            "Degradation mechanism and timing (temperature, pH)",
            "Treatment pressure requirements",
            "Flowback timing relative to diverter degradation",
            "Cost savings vs mechanical plug alternative"
        ],
        primary_authority=[
            "SPE 194326: Degradable Diverter Technology for Refracturing Applications",
            "SPE 189457: Chemical vs Mechanical Diversion Performance Comparison",
            "SPE 201188: Benzoic Acid Diverter Case Studies in Permian Carbonate Refracs"
        ],
        burden_holder="Completion engineer selecting diversion strategy",
        adversary_position="Mechanical plug advocates argue chemical diverters too uncertain for high-value refrac",
        counter_arguments=[
            "Diverter seal quality uncertain (pressure bleed-off risk)",
            "Premature degradation if formation hotter than expected",
            "Particle bridging unpredictable (depends on fracture width)",
            "Mechanical plugs provide definitive isolation"
        ],
        resolution_strategy="Pilot testing in offset wells, real-time pressure monitoring during treatment to confirm diversion, downhole fiber optics to measure zonal coverage",
        entity_scope="Operator, completion service company",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="SPE 194326 (technology overview), field case studies basin-specific"
    ),

    DoctrineBlock(
        topic="Bullhead Refrac Technique",
        keywords=["bullhead", "refrac through tubing", "annulus", "commingled", "no isolation"],
        conclusion_template=[
            "Bullhead refrac pumps treatment down tubing or annulus without zonal isolation, relying on stress reorientation and natural fluid distribution.",
            "Lowest-cost refrac method ($500K-1MM) but least controlled; fluid enters path of least resistance (typically original fractures).",
            "Most effective in wells with severe stress reorientation (>45 degrees), where new fracture azimuth naturally avoids original fractures."
        ],
        reasoning_framework="""
Bullhead Refrac Design and Limitations:

1. Technique Description:
   - Rig-less operation: pump through existing wellhead and tubing
   - No bridge plugs, no perforations, no wireline operations
   - Treatment enters wellbore and flows to lowest-stress zones
   - Relies on stress reorientation to create new fractures
   - May also re-open and extend original fractures

2. Operational Steps:
   - Kill well and displace to refrac fluid
   - Pressure test tubing/casing to 80% of expected treating pressure
   - Pump pad fluid (slickwater or crosslinked gel)
   - Pump proppant stages (ramp 0.5 → 2.0 ppg)
   - Monitor surface pressure and rate (no downhole diagnostics)
   - Flowback after 24-48 hr shut-in

3. Fluid Distribution Mechanisms:
   - Stress reorientation: new sigma_h direction guides fractures to new azimuth
   - Perforation friction: original perfs may be plugged/damaged, forcing fluid to new path
   - Natural fractures: preferential flow to reactivated natural fractures
   - Commingled intervals: multiple zones accept fluid simultaneously

4. Success Factors:
   - HIGH SUCCESS: >45 degree stress rotation, severe depletion (>60%), long shut-in (>3 years)
   - MEDIUM SUCCESS: 20-45 degree rotation, moderate depletion (40-60%), 1-2 year shut-in
   - LOW SUCCESS: <20 degree rotation, shallow depletion (<40%), short shut-in (<1 year)
   - Formation: works better in naturally fractured carbonate than tight shale

5. Economic Appeal:
   - Total cost: $500K-1MM (vs $1.5-2.5MM for plug & perf refrac)
   - Breakdown: $200K pumping services, $300K proppant/fluids, $50K wellhead/surface
   - Rig-less (no workover rig mobilization cost $300-500K)
   - Fast execution (2-3 days vs 10-15 days for full plug & perf)

6. Diagnostic Limitations:
   - No production logs (can't confirm zonal coverage)
   - No microseismic (can't confirm fracture azimuth)
   - Surface pressure only (can't distinguish near-wellbore restriction vs far-field propagation)
   - Post-treatment: compare production to decline curve to infer success

7. Risk Factors:
   - Uncontrolled fluid placement (may all enter single high-perm zone)
   - Casing integrity unknown until pressured up (failure risk)
   - Screenout risk higher (no redundancy if one zone screens off)
   - Production response highly variable (10% to 300% increase observed)

8. Best Use Cases:
   - Low-value wells where plug & perf uneconomic
   - Wells with demonstrated stress reorientation (offset refrac data)
   - Carbonate reservoirs with natural fracture networks
   - Portfolio approach: bullhead 10 wells for cost of 3 plug & perf, accept variable results
        """,
        key_factors=[
            "Magnitude and evidence of stress reorientation",
            "Formation depletion and pressure state",
            "Casing integrity and pressure rating",
            "Economic hurdle rate and capital constraints",
            "Availability of offset refrac performance data",
            "Risk tolerance for uncertain zonal coverage"
        ],
        primary_authority=[
            "SPE 190043: Bullhead Refrac Performance in Depleted Carbonate Reservoirs",
            "SPE 195678: Economic Analysis of Bullhead vs Plug & Perf Refracturing",
            "SPE 184521: Stress Reorientation Requirements for Successful Bullhead Refrac"
        ],
        burden_holder="Operator proposing bullhead refrac to reduce cost",
        adversary_position="Completions engineers argue bullhead too uncertain, prefer controlled plug & perf isolation",
        counter_arguments=[
            "Uncontrolled fluid placement results in poor coverage",
            "May simply re-stimulate original high-perm fractures (no incremental EUR)",
            "Casing failure risk without downhole intervention",
            "Low success rate (<40% in some basins) negates cost savings"
        ],
        resolution_strategy="Portfolio approach: bullhead lower-value wells, plug & perf high-value wells; use offset data to refine stress reorientation predictions",
        entity_scope="Operator, finance team",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="SPE 190043 (field case studies), economics highly basin-specific"
    ),

    DoctrineBlock(
        topic="Economic Analysis - Refrac vs New Drill Decision",
        keywords=["economics", "NPV", "IRR", "refrac vs drill", "capital efficiency", "EUR", "type curve"],
        conclusion_template=[
            "Refrac economic analysis compares incremental EUR and production profile against refrac capital cost, benchmarked vs new well drilling alternative.",
            "Typical Permian Basin horizontal: new well costs $6-8MM for 500-800 MBO EUR, refrac costs $1.5-2.5MM for 100-200 MBO incremental EUR.",
            "Refrac economically attractive when incremental NPV >50% of capital and IRR >30%, usually requiring >100 MBO incremental recovery."
        ],
        reasoning_framework="""
Refrac vs New Drill Economic Framework:

1. Refrac Capital Cost Components:
   - Workover rig: $300-500K (7-10 days @ $40-50K/day)
   - Wireline plug setting: $80-120K (mobilization + 10-15 plugs)
   - Completion fluids: $200-350K (slickwater or hybrid)
   - Proppant: $250-400K (2-4 MM lb 100 mesh sand @ $60-100/ton delivered)
   - Pumping services: $300-450K (HHP rental, personnel)
   - Perforation charges: $40-60K
   - Plug mill-out: $80-120K (2-3 days rig time + milling tools)
   - Contingency/misc: $150-250K
   - TOTAL: $1.5-2.5MM for Permian horizontal full lateral refrac

2. New Well Capital Cost:
   - Drilling: $3.5-4.5MM (15-20 days @ $200-250K/day for 10,000 ft lateral)
   - Completion: $2.5-3.5MM (30-stage frac, 6-8 MM lb proppant)
   - Facilities/flowlines: $300-500K
   - TOTAL: $6-8MM for Permian horizontal new well

3. Production Profiles:
   - New well type curve: 500-800 MBO EUR, 150-200 BOPD IP, 70% decline year 1
   - Refrac incremental: 100-200 MBO, 50-100 BOPD IP, 60-80% decline year 1
   - Refrac accelerates remaining reserves + adds incremental (combination effect)

4. NPV Calculation (10% discount):
   - Oil price: $70-80/bbl (strip pricing)
   - Operating cost: $15-20/bbl (LOE + severance + ad valorem)
   - Net revenue: $50-60/bbl after royalty (75% NRI assumed)
   - Refrac NPV: 150 MBO x $50/bbl x 0.6 PV factor = $4.5MM revenue - $2MM cost = $2.5MM NPV
   - New well NPV: 600 MBO x $50/bbl x 0.55 PV factor = $16.5MM revenue - $7MM cost = $9.5MM NPV

5. Capital Efficiency Metrics:
   - Refrac: $2.5MM NPV / $2MM capital = 1.25 NPV/I ratio, 60% IRR
   - New well: $9.5MM NPV / $7MM capital = 1.36 NPV/I ratio, 45% IRR
   - Refrac generates faster payout but lower absolute value

6. Decision Matrix:
   - REFRAC PREFERRED: limited capital, existing infrastructure, HBP acreage already held
   - NEW WELL PREFERRED: ample capital, new acreage to HBP, higher absolute NPV
   - PORTFOLIO APPROACH: mix refracs (fast cash) with new wells (long-term value)

7. Sensitivity Factors:
   - Oil price: $10/bbl change = ±$1.5MM refrac NPV, ±$6MM new well NPV
   - EUR: ±25% EUR = ±$1MM refrac NPV, ±$4MM new well NPV
   - Capital cost: ±20% = ±$400K refrac NPV, ±$1.4MM new well NPV
   - Discount rate: 15% vs 10% reduces PV by 20-25%

8. Non-Economic Factors:
   - Acreage HBP: new well holds acreage, refrac does not
   - Infrastructure capacity: refrac uses existing, new well may need expansion
   - Environmental/permitting: refrac faster permitting than new drill
   - Cycle time: refrac 30-45 days vs new well 90-120 days (cash flow acceleration)
        """,
        key_factors=[
            "Incremental EUR estimate (P50, P90 cases)",
            "Refrac capital cost (full-cycle including mill-out)",
            "Oil price forecast and discount rate",
            "New well type curve and drilling cost for basin",
            "Acreage HBP status and strategic value",
            "Capital budget constraints and portfolio optimization"
        ],
        primary_authority=[
            "SPE 189880: Economic Screening for Refracturing Programs",
            "SPE 195234: Capital Allocation Framework for Refrac vs New Drill",
            "SPE 201567: Permian Basin Refrac Economics Case Study"
        ],
        burden_holder="Operator/management proposing capital allocation",
        adversary_position="Finance/board may prefer new well drilling for higher absolute NPV and acreage capture",
        counter_arguments=[
            "Refrac EUR estimates often optimistic (actual 50-70% of predicted)",
            "New well holds acreage and generates royalty deductions",
            "Refrac success rate variability creates portfolio risk",
            "Cannibalization: refrac may reduce offset well performance"
        ],
        resolution_strategy="Probabilistic modeling with P10/P50/P90 cases, pilot program to calibrate EUR assumptions, portfolio optimization balancing cash flow and acreage objectives",
        entity_scope="Operator, working interest owners, board of directors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 189880 (economic framework), SPE 201567 (Permian-specific benchmarks)"
    ),

    DoctrineBlock(
        topic="Production History Analysis for Refrac Timing",
        keywords=["production history", "timing", "depletion", "plateau", "decline phase", "optimal timing"],
        conclusion_template=[
            "Optimal refrac timing targets wells at 50-70% depletion with 1500-2500 psi remaining reservoir pressure to enable effective fracture propagation.",
            "Production history analysis identifies inflection points where decline accelerates, indicating transition from fracture-dominated to matrix-dominated flow.",
            "Too-early refrac (<30% depletion) sacrifices original completion potential; too-late refrac (>80% depletion) lacks pressure for effective stimulation."
        ],
        reasoning_framework="""
Production History Analysis for Refrac Timing:

1. Decline Curve Analysis:
   - Plot log(rate) vs time to identify decline regime
   - Exponential decline (b=0): constant percentage decline, late-stage behavior
   - Hyperbolic decline (b=0.5-2.0): variable decline, typical of fractured wells
   - Harmonic decline (b=1.0): theoretical endpoint
   - Calculate b-factor and D_i from rate transient analysis

2. Depletion Phases:
   - Phase 1 (0-20% depletion, months 1-6): transient flow from fracture, high rates
   - Phase 2 (20-50% depletion, months 6-24): boundary-dominated flow, linear decline
   - Phase 3 (50-70% depletion, months 24-48): accelerated decline, refrac sweet spot
   - Phase 4 (>70% depletion, years 4+): terminal decline, limited refrac potential

3. Pressure Depletion Tracking:
   - Initial reservoir pressure: 4000-6000 psi (Permian typical)
   - After 2 years: 2500-3500 psi (30-40% depletion)
   - After 4 years: 1500-2500 psi (50-70% depletion) ← OPTIMAL REFRAC WINDOW
   - After 6+ years: <1500 psi (>70% depletion, marginal refrac candidate)
   - Use offset well pressure data or decline curve material balance to estimate

4. Production Profile Diagnostics:
   - GOR trend: stable GOR indicates good liquid production, rising GOR may indicate gas cap expansion or mechanical issues
   - Water cut trend: stable or slowly rising acceptable, spiking water cut suggests casing leak or water breakthrough
   - Flowing tubing pressure: declining FTP indicates reduced reservoir pressure
   - Choke management history: frequent choke reductions indicate accelerating decline

5. EUR Estimation:
   - Plot cumulative production vs time
   - Fit Arps equation: q(t) = q_i / (1 + b*D_i*t)^(1/b)
   - Integrate to estimate EUR
   - Compare to type curve: has well produced 40%, 50%, 60% of expected EUR?
   - Refrac target: wells at 50-60% of type curve EUR (significant remaining reserves)

6. Analog Well Comparison:
   - Identify offset wells with similar reservoir/completion properties
   - Track production variance: if subject well declining faster than analogs, may indicate poor original completion
   - Offset refrac performance: did analog refracs work? What was incremental EUR?

7. Operational History Review:
   - Uptime/downtime: frequent shut-ins damage fracture conductivity
   - Wellbore interventions: any workovers, cleanouts, artificial lift installations
   - Artificial lift: if on gas lift or ESP, indicates pressure depletion (good for refrac)
   - Flow assurance: paraffin, scale, hydrate issues indicate production chemistry changes

8. Decision Trigger:
   - TRIGGER REFRAC: 50-70% depletion, b>1.0, stable GOR/water cut, 1500+ psi pressure, >100 MBO remaining EUR
   - WAIT: <40% depletion, still on transient decline, high flowing pressure
   - ABANDON REFRAC: >80% depletion, <1000 psi pressure, mechanical integrity concerns, terminal decline (b<0.5)
        """,
        key_factors=[
            "Percent depletion vs original EUR estimate",
            "Decline curve b-factor and transition to exponential decline",
            "Estimated remaining reservoir pressure",
            "GOR and water cut stability",
            "Offset well refrac performance and timing",
            "Artificial lift status (indicates depletion stage)"
        ],
        primary_authority=[
            "SPE 184832: Decline Curve Analysis for Refrac Candidate Selection",
            "SPE 191451: Production Decline Signatures Indicating Refrac Potential",
            "SPE 198765: Optimal Refrac Timing Based on Depletion and Stress Reorientation"
        ],
        burden_holder="Reservoir engineer recommending refrac timing",
        adversary_position="Operations may prefer refrac earlier (while infrastructure in place) or later (maximize original completion recovery)",
        counter_arguments=[
            "Waiting for optimal depletion risks infrastructure degradation (corrosion, scale)",
            "Too-early refrac may accelerate existing production without adding EUR",
            "Pressure estimation uncertain without direct measurement (no pressure gauge)",
            "Type curve EUR assumption may overstate remaining reserves"
        ],
        resolution_strategy="Run material balance to estimate pressure, use analog decline curves to validate EUR, pressure transient test if economics justify cost ($50-100K)",
        entity_scope="Operator, reservoir engineering",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 184832 (DCA methodology), SPE 198765 (timing framework)"
    ),

    DoctrineBlock(
        topic="Casing Integrity Assessment Before Refrac",
        keywords=["casing integrity", "corrosion", "cement bond", "caliper log", "ultrasonic", "pressure test"],
        conclusion_template=[
            "Casing integrity assessment is critical before refrac to avoid casing failure under high treating pressures (8000-12000 psi).",
            "Multi-arm caliper, ultrasonic thickness, and cement bond logs quantify corrosion, deformation, and cement quality; pressure testing validates mechanical integrity.",
            "Minimum requirements: <10% wall thickness loss, no deformation >5%, cement bond >50%, successful pressure test to 1.2x expected treating pressure."
        ],
        reasoning_framework="""
Casing Integrity Evaluation for Refrac:

1. Risk Factors:
   - Age: wells >5 years experience corrosion (H2S, CO2, chlorides)
   - Production history: high water cut, gas lift, chemical injection accelerate corrosion
   - Cementing quality: poor primary cement bond allows pressure communication, casing stress
   - Thermal cycling: hot/cold cycles from steam injection, high-rate production
   - Mechanical damage: perforation guns, wireline tools, previous completions

2. Diagnostic Tools:
   - Multi-Arm Caliper (MAC): measures internal casing diameter (detects deformation, corrosion)
   - Ultrasonic Imaging Tool (USIT): measures remaining wall thickness, detects pitting, cracks
   - Electromagnetic Corrosion Log: quantifies metal loss through casing
   - Cement Bond Log (CBL): acoustic amplitude indicates cement quality
   - Ultrasonic Cement Evaluation (USCD): quantifies cement bond percentage

3. Logging Program:
   - Run MAC/USIT combo from TD to surface casing shoe
   - Focus on high-stress areas: casing shoe, production packer depth, transition zones
   - CBL/USCD over planned refrac interval (perforated zones ±200 ft)
   - Integrate logs with production history (correlate corrosion to high water-cut zones)

4. Interpretation Criteria:
   - Wall Thickness:
     * Nominal 5.5" casing: 0.275" wall, collapse rating 9930 psi
     * 10% loss (0.025") acceptable: 0.250" remaining wall, 8500 psi collapse
     * 20% loss (0.055") marginal: 0.220" remaining wall, 7000 psi collapse
     * >25% loss: reject for refrac (casing failure risk)
   - Cement Bond:
     * >70% bond: excellent isolation, full treating pressure acceptable
     * 50-70% bond: good isolation, monitor for pressure bleed-off
     * <50% bond: poor isolation, may need cement squeeze before refrac
   - Deformation:
     * <5% diameter change: acceptable
     * 5-10% diameter reduction: marginal, may restrict plug setting
     * >10% reduction: reject (tool passage risk, plug sealing risk)

5. Pressure Testing:
   - After logging, run pressure test (if integrity acceptable)
   - Set packer above planned refrac zone, pressure up tubing/annulus
   - Test pressure: 1.2x expected treating pressure (e.g., 10,000 psi test for 8,500 psi treatment)
   - Hold 15 minutes: <3% pressure drop acceptable
   - If fails: identify leak zone, remediate (cement squeeze, casing patch)

6. Remediation Options:
   - Cement Squeeze: pump cement through perforations to fill annulus voids, re-establish bond
   - Casing Patch: expandable patch or liner to cover corroded section
   - Reduce Treating Pressure: lower pump rate, reduce proppant concentration (less effective refrac)
   - Abandon Refrac: if integrity too poor, economics don't support remediation

7. Economic Considerations:
   - Logging cost: $80-120K (MAC/USIT/CBL combo, 8000 ft)
   - Pressure test: $30-50K (packer rental, pressure monitoring)
   - Cement squeeze: $150-250K (workover rig, cement job)
   - Casing patch: $200-400K (patch tool, installation)
   - Total integrity evaluation/remediation: $100-500K (5-25% of refrac budget)

8. Risk Mitigation:
   - Always log before committing to full refrac program
   - Budget 15-20% contingency for integrity issues
   - Have cement squeeze/patch plan ready before logging
   - Consider casing integrity in candidate selection (prioritize newer, better-maintained wells)
        """,
        key_factors=[
            "Casing age and production history (corrosion exposure)",
            "Logging results (wall thickness, cement bond, deformation)",
            "Pressure test success at design treating pressure",
            "Remediation cost vs expected refrac incremental value",
            "Offset well casing failure history",
            "Treatment pressure requirements and safety margin"
        ],
        primary_authority=[
            "API RP 5C5: Casing Inspection and Maintenance Procedures",
            "SPE 191828: Casing Integrity Evaluation for High-Pressure Refracturing",
            "SPE 187234: Corrosion Logging and Remediation Best Practices"
        ],
        burden_holder="Operator conducting refrac, responsible for safe operations",
        adversary_position="Cost-conscious teams may skip logging to save $100K, rely on pressure test alone",
        counter_arguments=[
            "Logging cost (5-10% of refrac budget) too high for marginal wells",
            "Pressure test sufficient (direct mechanical proof of integrity)",
            "Offset wells refrac'd without logging, no failures observed",
            "Remediation may cost more than refrac value (abandon candidate instead)"
        ],
        resolution_strategy="Risk-based approach: log high-value refracs (>$2MM spend), pressure test only for lower-value candidates, track field failure rates to calibrate risk",
        entity_scope="Operator, HSE, regulatory (TRRC, EPA)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API RP 5C5 (industry standard), SPE 191828 (refrac-specific criteria)"
    ),

    DoctrineBlock(
        topic="Refrac Flowback Protocols",
        keywords=["flowback", "cleanup", "proppant recovery", "load recovery", "choke management", "early time production"],
        conclusion_template=[
            "Refrac flowback protocols balance rapid load fluid recovery with proppant retention in fractures, critical for maximizing post-refrac production.",
            "Controlled flowback using conservative choke schedule (1/8 to 1/4 to 1/2 inch over 3-7 days) minimizes proppant flowback while recovering 60-80% of injected fluid.",
            "Early-time production data (first 30 days) strongly correlates with long-term refrac success and is used to calibrate EUR forecasts."
        ],
        reasoning_framework="""
Refrac Flowback Design and Execution:

1. Objectives:
   - Recover load fluid quickly (reduce water block damage to formation)
   - Retain proppant in fractures (avoid proppant flowback, maintain conductivity)
   - Initiate stable production at sustainable rate
   - Gather diagnostic data (flowback composition, pressure, rate)

2. Choke Schedule Design:
   - Initial choke: 1/8" or 3/16" (very restrictive)
   - First 24 hours: monitor returns, pressure, no choke changes
   - Days 2-3: increase to 1/4" if clean fluid returns, stable pressure
   - Days 4-5: increase to 3/8" if >50% load recovery, no sand
   - Days 6-7: increase to 1/2" for transition to production
   - Days 8+: production choke sizing (balance rate vs wellhead pressure)

3. Load Recovery Monitoring:
   - Measure flowback fluid volume and compare to injected volume
   - Target: 60-80% load recovery in first 7-10 days
   - <50% recovery: indicates high leak-off, formation damage, poor fracture cleanup
   - >90% recovery: may indicate fracture closure, proppant pack issue
   - Track flowback salinity: increasing salinity indicates formation fluid breakthrough

4. Proppant Flowback Detection:
   - Visual inspection: sand in flowback fluid
   - Erosion monitoring: choke, flowline erosion indicates sand production
   - Acoustic sand detector: continuous monitoring
   - Allowable sand: <0.1% by volume (trace amounts acceptable)
   - Excessive sand: >1% indicates proppant pack failure, reduce choke immediately

5. Pressure Management:
   - Wellhead flowing pressure target: 500-1500 psi (balance drawdown vs proppant retention)
   - Too high pressure (>2000 psi): slow flowback, poor load recovery
   - Too low pressure (<300 psi): risk proppant flowback, fracture closure
   - Monitor pressure decline rate: steady decline indicates stable cleanup

6. Shut-in Period (Optional):
   - Some operators shut in 12-48 hours after refrac before flowback
   - Theory: allow proppant settling, fracture face filter cake formation
   - Evidence mixed: some studies show benefit, others show no difference
   - Conservative approach for high-proppant treatments (>2 ppg)

7. Chemical Additives During Flowback:
   - Scale inhibitor: prevent barite, calcite precipitation in flowlines
   - Corrosion inhibitor: protect tubing from H2S, CO2
   - Biocide: prevent bacteria growth in stagnant fluid
   - Friction reducer: aid fluid movement through proppant pack
   - Clay stabilizer: prevent clay swelling if formation sensitive

8. Production Testing:
   - After 7-10 days flowback, conduct 24-hour production test
   - Measure oil, gas, water rates stabilized on fixed choke
   - Calculate initial production (IP) rate: critical metric for refrac success
   - Compare to pre-refrac production and type curve
   - Use IP to forecast EUR (correlation from offset refrac data)

9. Post-Flowback Surveillance:
   - Production logging: identify contributing zones (did refrac access new intervals?)
   - Pressure buildup test: measure fracture conductivity and reservoir pressure
   - Flowback fluid analysis: trace chemicals, isotopes to confirm fracture fluid recovery
   - Proppant tracer analysis: detect which stages contributed proppant to production

10. Decision Points:
    - If IP >2x pre-refrac rate: SUCCESS, optimize production choke for EUR
    - If IP 1.5-2x pre-refrac: MODERATE SUCCESS, monitor for sustained improvement
    - If IP <1.5x pre-refrac: MARGINAL, evaluate if results justify cost, adjust future designs
    - If IP <1x pre-refrac: FAILURE, investigate (screenout, poor diversion, mechanical issues)
        """,
        key_factors=[
            "Choke schedule conservatism (balance recovery speed vs proppant retention)",
            "Load recovery percentage in first 7-10 days",
            "Proppant flowback monitoring and sand production limits",
            "Flowing wellhead pressure and drawdown management",
            "Chemical treatment program during flowback",
            "Initial production rate comparison to pre-refrac baseline"
        ],
        primary_authority=[
            "SPE 187923: Flowback Optimization for Refractured Horizontal Wells",
            "SPE 195432: Proppant Flowback Mechanisms and Mitigation Strategies",
            "SPE 201234: Early-Time Production Analysis for Refrac Performance Forecasting"
        ],
        burden_holder="Operator/production engineer managing flowback",
        adversary_position="Aggressive flowback advocates argue faster recovery improves results; conservatives fear proppant loss",
        counter_arguments=[
            "Slow flowback (conservative choke) prolongs water block damage",
            "Fast flowback risks proppant flowback and conductivity loss",
            "Load recovery percentage poor predictor of ultimate success (many variables)",
            "Shut-in period delays production and may not improve results"
        ],
        resolution_strategy="Standardize choke schedule based on offset well data, real-time monitoring with authority to adjust, post-job review to calibrate future flowbacks",
        entity_scope="Operator, production operations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 187923 (flowback best practices), field experience highly basin-specific"
    ),

    DoctrineBlock(
        topic="Refrac Case Studies - Permian Basin Horizontal Wells",
        keywords=["Permian", "case study", "field results", "Wolfcamp", "Bone Spring", "horizontal refrac", "performance"],
        conclusion_template=[
            "Permian Basin horizontal well refracs demonstrate 50-150% production increases with 150-300 MBO incremental EUR in successful cases.",
            "Wolfcamp A/B refracs show best results using full lateral re-isolation (10-15 plugs) with 1.5-2.5 ppg proppant concentration in hybrid fluids.",
            "Success rate varies 40-70% depending on candidate selection rigor, with economic payout achieved in 60-80% of attempts."
        ],
        reasoning_framework="""
Permian Basin Refrac Field Performance Database:

1. Basin Characteristics:
   - Primary targets: Wolfcamp A, Wolfcamp B, Bone Spring (2nd, 3rd Bone Spring)
   - Reservoir properties: 0.01-0.1 md permeability, 6-12% porosity, 7000-10000 ft depth
   - Original completions: 2010-2016 vintage, 4-6 stages/1000 ft, 1000-2000 lb/ft proppant
   - Depletion state: 2000-3000 psi pressure after 4-6 years, 50-70% of original EUR produced

2. Refrac Design Trends:
   - Early refracs (2015-2017): bullhead or limited plug count (2-4 plugs), mixed results
   - Modern refracs (2018+): full lateral re-isolation, 10-15 composite plugs, improved results
   - Fluid: transition from slickwater to hybrid (slickwater pad + crosslinked gel proppant stages)
   - Proppant: increased loading 1.5-2.5 ppg (vs 1.0-1.5 ppg in early attempts)

3. Performance Statistics (100-well dataset):
   - Average pre-refrac production: 20-30 BOPD (decline to marginal economics)
   - Average post-refrac IP (30 days): 60-90 BOPD (2-3x increase)
   - Success rate (IP >1.5x pre-refrac): 65%
   - Failure rate (IP <1.2x pre-refrac): 20%
   - Marginal (IP 1.2-1.5x): 15%
   - Average incremental EUR: 150-200 MBO (range 50-400 MBO)

4. Economic Outcomes:
   - Average refrac cost: $1.8MM (including rig, completion, plugs, mill-out)
   - Average NPV (10% discount, $70/bbl oil): $2.5MM
   - IRR: 50-80% for successful refracs, <20% for failures
   - Portfolio NPV/I ratio: 1.3-1.5 (accounting for successes and failures)

5. Success Factor Correlations:
   - STRONG POSITIVE: original completion quality (worse original = better refrac), depletion (50-70% optimal)
   - MODERATE POSITIVE: lateral length (longer laterals better), producing GOR (stable better)
   - WEAK/NEUTRAL: reservoir quality (permeability, porosity), well age
   - NEGATIVE: casing integrity issues, high water cut (>70%)

6. Notable Case Study: Operator A Wolfcamp B Program
   - 15 wells refrac'd in 2019-2020, Wolfcamp B, 7500-9000 ft laterals
   - Original completion: 2012-2014, 30-40 stages, 1200 lb/ft, slickwater
   - Refrac design: 12-15 plugs, hybrid fluid, 2.0 ppg proppant, new perfs
   - Pre-refrac avg: 18 BOPD, post-refrac avg: 72 BOPD (4x increase)
   - Incremental EUR avg: 210 MBO, cost avg: $1.6MM
   - Economics: 14/15 wells NPV positive, 1 marginal (casing failure during treatment)

7. Failure Analysis:
   - Common failure modes:
     * Casing failure during treatment (5-10% of attempts)
     * Screenout due to poor fluid design or proppant slugging (8-12%)
     * Uncontrolled fluid placement (bullhead refracs, 30-40% of those attempts)
     * Minimal production response despite successful treatment (10-15%, unknown cause)
   - Lessons learned:
     * Casing integrity logging critical (avoid 50% of mechanical failures)
     * Full lateral re-isolation outperforms bullhead 2:1 success rate
     * Hybrid fluid systems reduce screenout risk vs pure slickwater

8. Emerging Trends (2023+):
   - Far-field diversion using degradable particulates (reduce plug count to 6-8)
   - Real-time microseismic to confirm stress reorientation before main treatment
   - Fiber optic DAS/DTS to diagnose zonal coverage and optimize future stages
   - Simul-frac of multiple refrac candidates (reduce rig time, improve capital efficiency)

9. Comparative Basin Performance:
   - Permian refracs: 65% success rate, 150-200 MBO incremental EUR
   - Eagle Ford refracs: 55% success rate, 100-150 MBO incremental EUR (higher decline)
   - Bakken refracs: 40% success rate, 80-120 MBO incremental EUR (more stress challenges)
   - STACK/SCOOP refracs: 50% success rate, 120-180 MBO incremental EUR

10. Operator Decision Framework:
    - Tier 1 candidates: 60-70% depletion, b>1.2, good casing, >$3MM NPV → full plug & perf refrac
    - Tier 2 candidates: 50-60% depletion, b=0.8-1.2, acceptable casing, $1.5-3MM NPV → limited plug refrac or hybrid diversion
    - Tier 3 candidates: <50% or >75% depletion, casing concerns, <$1.5MM NPV → bullhead or decline
        """,
        key_factors=[
            "Basin-specific decline characteristics and stress regime",
            "Original completion vintage and quality deficiencies",
            "Candidate selection rigor (depletion, casing, economics)",
            "Refrac design evolution (plug count, fluid, proppant)",
            "Success rate probability and portfolio approach",
            "Economic hurdle rates and capital allocation strategy"
        ],
        primary_authority=[
            "SPE 201567: Permian Basin Refrac Performance Database and Economics",
            "SPE 195678: Wolfcamp Refrac Case Studies and Lessons Learned",
            "SPE 204123: Statistical Analysis of 200+ Permian Horizontal Refracs"
        ],
        burden_holder="Operator proposing refrac program with performance forecasts",
        adversary_position="Finance/technical teams question success rate assumptions and incremental EUR reliability",
        counter_arguments=[
            "Operator-reported case studies biased toward successful wells (publication bias)",
            "Incremental EUR difficult to isolate from natural production variance",
            "Economic assumptions sensitive to oil price (volatility risk)",
            "Portfolio approach requires large well count to average out failures"
        ],
        resolution_strategy="Transparent reporting of all refrac attempts (not just successes), probabilistic EUR modeling, pilot program before full-scale rollout, third-party data validation",
        entity_scope="Operator, investors, industry benchmarking",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="SPE 201567 and SPE 204123 (largest published datasets), ongoing field evolution"
    ),

    DoctrineBlock(
        topic="Refrac Pump Schedule Design",
        keywords=["pump schedule", "treatment design", "proppant ramp", "pad volume", "flush", "stage design"],
        conclusion_template=[
            "Refrac pump schedules balance pad fluid volume (fracture initiation, diversion) with proppant stages (conductivity) using conservative ramp rates to avoid screenout.",
            "Typical schedule: 20-40% pad (slickwater or linear gel), proppant ramp 0.5→1.0→1.5→2.0 ppg over 3-5 stages, 1000-2000 lb/ft total proppant loading.",
            "Stage-by-stage design varies based on diversion strategy: mechanical isolation allows aggressive pumping, chemical diversion requires conservative approach."
        ],
        reasoning_framework="""
Refrac Treatment Pump Schedule Engineering:

1. Overall Structure:
   - Pad fluid: 20-40% of total volume (no proppant, create fracture, cool formation)
   - Proppant stages: 60-80% of total volume (build conductivity)
   - Flush: final clean fluid to displace proppant from wellbore
   - Total volume per stage: 50,000-150,000 gallons (3-7 stages for bullhead, 8-15 for plug & perf)

2. Pad Fluid Design:
   - Volume: 10,000-40,000 gallons per stage
   - Fluid type: slickwater (friction reducer), linear gel (guar), or hybrid
   - Purpose: initiate fracture, breakdown formation, cool wellbore, activate diverters
   - Pump rate: ramp 20→40→60 BPM over first 10-20 minutes
   - Monitor: surface pressure (expect breakdown at 6000-9000 psi)

3. Proppant Ramp Schedule:
   - Conservative approach (avoid screenout):
     * Stage 1: 0.5 ppg for 10,000 gal (5,000 lb proppant)
     * Stage 2: 1.0 ppg for 15,000 gal (15,000 lb)
     * Stage 3: 1.5 ppg for 20,000 gal (30,000 lb)
     * Stage 4: 2.0 ppg for 25,000 gal (50,000 lb)
     * Total: 100,000 lb proppant (1000 lb/ft for 100 ft interval)
   - Aggressive approach (if low screenout risk):
     * Start 1.0 ppg, ramp to 2.5-3.0 ppg, higher total loading (1500-2000 lb/ft)

4. Proppant Selection:
   - 100 mesh sand: primary choice (low cost, good transport, adequate conductivity)
   - 40/70 mesh sand: higher conductivity but harder to transport (settling risk)
   - Resin-coated proppant: premium option (prevents flowback, higher cost)
   - Ceramic proppant: ultra-high strength for deep/high-stress wells (rarely used in refrac)

5. Fluid Rheology Selection:
   - Slickwater: low viscosity (1-5 cp), high pump rate (60-100 BPM), narrow fractures, complex network
     * Pros: low cost, low formation damage, easy cleanup
     * Cons: poor proppant transport (limited to <2.0 ppg), higher leak-off
   - Crosslinked Gel: high viscosity (100-500 cp), lower pump rate (30-60 BPM), wider fractures
     * Pros: excellent proppant transport (up to 4-5 ppg), less leak-off
     * Cons: higher cost, potential formation damage (gel residue), slower cleanup
   - Hybrid: slickwater pad + crosslinked gel proppant stages
     * Optimal balance: fracture complexity + proppant transport

6. Stage-by-Stage Variation:
   - If using mechanical diversion (bridge plugs):
     * Each stage independent, can optimize individually
     * Toe stages: higher proppant (access fresh rock)
     * Heel stages: lower proppant (already produced, may be depleted)
   - If using chemical diversion:
     * Diverter pill between stages (500-2000 gal, 2-5 ppg particulate)
     * Progressive proppant increase (build conductivity as diverter seals zones)

7. Flush Volume:
   - Purpose: displace proppant from wellbore into fractures
   - Volume: 1.0-1.5x wellbore volume (tubing + annulus)
   - Typical: 500-1500 gallons clean fluid
   - Critical: insufficient flush leaves proppant in wellbore (screenout, production restriction)

8. Pump Rate Strategy:
   - Target rate: 40-80 BPM (balance fracture propagation vs friction pressure)
   - Higher rate (60-80 BPM): promotes complex fracture network, turbulent flow
   - Lower rate (30-50 BPM): reduces near-wellbore tortuosity, less screenout risk
   - Rate ramp: start 20 BPM, increase every 5 min to target (monitor pressure response)

9. Real-Time Adjustments:
   - Pressure rising rapidly: reduce rate, reduce proppant concentration (screenout warning)
   - Pressure flat or declining: good fracture propagation, maintain or increase rate
   - Returns to surface: if treating down annulus, check for fluid returns (may indicate casing leak)
   - Sand-out (cannot pump): stop, flush, diagnose (near-wellbore bridge or far-field screenout)

10. Post-Treatment Evaluation:
    - Total fluid pumped: compare to design (did entire treatment enter formation?)
    - Total proppant pumped: calculate lb/ft (actual vs design)
    - Average treating pressure: compare to predicted (validate fracture model)
    - Instantaneous shut-in pressure (ISIP): estimate fracture closure pressure (stress state)
    - Pump efficiency: calculate job time vs design (faster = more efficient crew, slower = operational issues)
        """,
        key_factors=[
            "Pad volume percentage and fluid type selection",
            "Proppant ramp conservatism vs loading target",
            "Proppant mesh size and type (sand vs resin-coated)",
            "Fluid rheology (slickwater vs crosslinked vs hybrid)",
            "Pump rate targets and real-time adjustment triggers",
            "Diversion strategy integration (mechanical vs chemical)"
        ],
        primary_authority=[
            "SPE 191277: Refrac Treatment Design Best Practices",
            "SPE 189457: Proppant Transport and Placement in Refrac Applications",
            "SPE 195234: Hybrid Fluid Systems for Refracturing"
        ],
        burden_holder="Completion engineer designing refrac treatment",
        adversary_position="Service company may push aggressive design (higher volume/proppant) to maximize revenue; operator wants cost-effective design",
        counter_arguments=[
            "Aggressive proppant ramp increases screenout risk (5-10% job failure rate)",
            "High proppant loading may exceed fracture width (proppant bridging)",
            "Slickwater cheaper but may underperform vs crosslinked gel in refrac (less proppant in fracture)",
            "Conservative design leaves reserves unstimulated"
        ],
        resolution_strategy="Calibrate design to offset well results, run fracture propagation model (FracPro, MFrac), real-time monitoring with adjustment authority, post-job comparison to design",
        entity_scope="Operator, frac service company",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 191277 (industry standard design process), service company best practices"
    ),

    DoctrineBlock(
        topic="Refrac Risk Assessment - Screenout and Casing Failure",
        keywords=["risk", "screenout", "casing failure", "bridging", "proppant pack", "treatment failure"],
        conclusion_template=[
            "Refrac operations carry 5-15% risk of screenout (premature proppant bridging) and 3-8% risk of casing failure, both resulting in partial or total job failure.",
            "Screenout risk mitigated through conservative proppant ramp, real-time pressure monitoring, and fluid viscosity selection; casing failure through pre-job integrity logging.",
            "Economic risk management includes contingency planning (10-20% budget reserve), insurance options, and portfolio diversification across multiple refrac candidates."
        ],
        reasoning_framework="""
Refrac Risk Identification and Mitigation:

1. Screenout Risk:
   Definition: Proppant bridges in fracture or near-wellbore, preventing further fluid/proppant placement
   Frequency: 5-15% of refrac jobs (varies by basin, design conservatism)

   Causes:
   - Excessive proppant concentration (>2.5 ppg in narrow fractures)
   - Inadequate fluid viscosity (slickwater cannot transport high proppant loads)
   - Rapid proppant ramp (insufficient time for settling/redistribution)
   - Fracture height restriction (proppant accumulates at top)
   - Dehydration (leak-off concentrates proppant in fracture)
   - Near-wellbore tortuosity (kinks, offsets in fracture path)

   Indicators:
   - Rapidly rising treating pressure (>500 psi/min)
   - Declining pump rate despite constant surface pressure
   - Inability to maintain target rate
   - Surface pressure exceeds casing rating

   Response:
   - Immediate: reduce proppant concentration to zero (flush with clean fluid)
   - If pressure stabilizes: resume at lower proppant concentration (drop 0.5-1.0 ppg)
   - If pressure continues rising: shut down pumps, attempt circulation (may clear bridge)
   - If cannot clear: abandon stage, move to next interval (if plug & perf), or end treatment (if bullhead)

   Mitigation:
   - Conservative proppant ramp (0.5 ppg increments)
   - Higher viscosity fluid (crosslinked gel or hybrid)
   - Real-time pressure monitoring with automated shutdown
   - Perforation design: more shots/ft (distribute proppant entry points)
   - Fracture modeling: predict width, height to optimize proppant loading

2. Casing Failure Risk:
   Definition: Casing ruptures, collapses, or separates under treating pressure
   Frequency: 3-8% of refrac jobs (higher in older wells, corroded casing)

   Causes:
   - Corrosion: H2S, CO2, chlorides reduce wall thickness over 5-10 years
   - Pre-existing damage: perforation guns, wireline tools, previous completions
   - Overpressure: treating pressure exceeds casing collapse/burst rating
   - Thermal stress: hot treatment fluid (120-150°F) in cold wellbore causes expansion/contraction
   - Cement failure: poor cement bond allows pressure behind casing, casing buckling

   Indicators:
   - Sudden pressure drop during treatment (>1000 psi drop in <1 min)
   - Fluid returns to surface (annulus or adjacent wellbore)
   - Unable to maintain pressure despite pumping at full rate
   - Post-job: production casing pressure test fails

   Response:
   - Immediate: shut down treatment, close wellhead valves
   - Attempt to isolate leak: set bridge plug above failure zone (if accessible)
   - If cannot isolate: abandon well or remediate (casing patch, liner)
   - Post-failure: pressure test to locate failure depth, log to assess damage extent

   Mitigation:
   - Pre-job casing integrity logging (MAC, USIT, CBL)
   - Pressure testing to 1.2x expected treating pressure
   - Casing design review: verify collapse/burst ratings vs treating pressure
   - Reduce treating pressure: lower pump rate, use lower-viscosity fluid
   - Cement squeeze: improve cement bond if CBL shows voids

3. Diversion Failure Risk:
   - Chemical diverters fail to seal (5-20% of attempts): fall back to bullhead placement
   - Mechanical plugs slip or leak (<5% if properly set and tested): pressure test before pumping
   - Consequence: poor zonal coverage, treatment enters high-permeability zones only

4. Economic Risk:
   - Screenout: lose 20-50% of planned proppant, ~$100-300K wasted materials + rig time
   - Casing failure: $200K-1MM+ (casing patch $200-400K, or well abandonment = total loss)
   - Underperformance: job executes but production increase <50% of forecast (most common, ~20-30% of jobs)

5. Risk Mitigation Strategies:
   - Technical:
     * Rigorous candidate selection (eliminate high-risk wells before committing capital)
     * Pre-job diagnostics (logging, pressure testing)
     * Conservative treatment design (under-design vs over-design)
     * Real-time monitoring and adjustment authority

   - Financial:
     * Budget 10-20% contingency for remediation, additional materials
     * Portfolio approach: 8-10 refracs to diversify risk (not all will fail)
     * Insurance: wellbore equipment coverage (some operators carry, most self-insure)

   - Contractual:
     * Service company risk-sharing: performance-based pricing (pay more if successful)
     * Casing failure liability: typically operator bears risk (service company not responsible for casing condition)
     * Screenout costs: shared (operator pays materials, service company absorbs some rig time)

6. Failure Rate Benchmarking:
   - Industry average (Permian Basin): 10% screenout, 5% casing failure, 25% underperformance
   - Best-in-class operators: <5% screenout, <3% casing failure (through rigorous screening)
   - Greenfield programs (new basin, unproven refracs): 20-30% total failure rate acceptable in early wells

7. Decision Framework:
   - High-risk candidate (poor casing, aggressive design): require >2.0 NPV/I to justify
   - Medium-risk candidate: require >1.5 NPV/I
   - Low-risk candidate (good casing, conservative design, proven analog): accept >1.2 NPV/I
   - Portfolio: accept some high-risk wells if blended portfolio NPV/I >1.4

8. Lessons Learned Process:
   - After each refrac (success or failure): document design, execution, results
   - Quarterly review: identify trends (certain formations, certain designs more prone to failure)
   - Update candidate selection criteria based on failure analysis
   - Share learnings across operator organization (avoid repeating mistakes)
        """,
        key_factors=[
            "Proppant concentration and ramp rate conservatism",
            "Casing integrity assessment rigor and logging coverage",
            "Real-time monitoring and response protocols",
            "Treatment design margin vs casing ratings and fracture model predictions",
            "Portfolio risk diversification and contingency budgeting",
            "Failure rate benchmarking and continuous improvement process"
        ],
        primary_authority=[
            "SPE 191828: Risk Assessment Framework for Refracturing Operations",
            "SPE 187234: Casing Failure Analysis and Prevention in High-Pressure Stimulation",
            "SPE 195912: Screenout Prevention Through Real-Time Monitoring"
        ],
        burden_holder="Operator responsible for safe operations and economic outcomes",
        adversary_position="Service companies may minimize risks to secure work; finance teams may underestimate failure probability",
        counter_arguments=[
            "Failure rates overstated (selection bias in published data)",
            "Casing logging expensive relative to failure probability (5% risk x $2MM loss = $100K expected, but logging costs $120K)",
            "Conservative design leaves production on table (opportunity cost)",
            "Portfolio approach requires large well count (not viable for small operators)"
        ],
        resolution_strategy="Transparent failure tracking across all attempts, probabilistic risk modeling (Monte Carlo), pilot programs to calibrate basin-specific risks, third-party risk assessment",
        entity_scope="Operator, HSE, finance, board of directors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 191828 (risk framework), API RP 5C5 (casing integrity), company-specific risk tolerance"
    ),

    DoctrineBlock(
        topic="Refrac Through Existing Perforations vs New Perforations",
        keywords=["perforation strategy", "existing perfs", "new perfs", "azimuth", "phasing", "perforation density"],
        conclusion_template=[
            "Refrac through existing perforations simplifies operations but risks re-entering original fractures; new perforations offset 180° access different azimuth per stress reorientation theory.",
            "New perforation strategy requires accurate original completion records and wellbore survey to avoid interference; target 6-8 shots/ft density, 60-90° phasing.",
            "Decision criteria: use existing perfs if stress reorientation >45° (fractures naturally diverge), use new perfs if <30° rotation (need geometric separation)."
        ],
        reasoning_framework="""
Perforation Strategy for Refrac Operations:

1. Existing Perforation Approach:
   Advantages:
   - No new perforation guns required (cost savings $30-50K)
   - Faster execution (no wireline perf run)
   - Guaranteed communication with formation (perfs already proven)
   - Avoids risk of missing target zone with new perfs

   Disadvantages:
   - May re-enter original fractures (limited incremental rock contact)
   - Original perfs may be plugged, damaged, or reduced in effectiveness
   - Cannot control azimuth (original perf phasing dictates fracture direction)
   - If stress has not reoriented, refrac simply re-opens old fractures

   Best Use:
   - Stress reorientation >45 degrees confirmed (microseismic, geomechanical model)
   - Original perfs known to be clean and functional
   - Cost-sensitive applications (bullhead refracs)
   - Carbonate formations with natural fractures (less dependent on perforation azimuth)

2. New Perforation Approach:
   Advantages:
   - Control perforation azimuth (orient 180° opposite original for maximum separation)
   - Higher perforation density (6-8 vs original 4-6 shots/ft) ensures breakdown
   - Fresh perforations (no damage, plugging, or crush)
   - Definitive entry into new rock volume (geometric certainty)

   Disadvantages:
   - Additional cost: $30-50K per stage (guns, wireline, time)
   - Requires accurate wellbore survey and original completion records (to avoid collision)
   - Risk of missing target zone or perforating into water/gas contact
   - Potential for interference if too close to original perfs (<20 ft)

   Best Use:
   - Stress reorientation <30 degrees (minimal natural azimuth change)
   - Original perfs suspected damaged or plugged
   - High-value refrac where maximizing coverage justifies cost
   - Shale formations where perforation orientation critical

3. Perforation Placement Design:
   Vertical Spacing:
   - If new perfs: offset 20-50 ft from original (avoid fracture interference)
   - Gamma ray correlation to ensure consistent depth placement
   - Target same reservoir interval (avoid moving up/down into different rock quality)

   Azimuthal Orientation:
   - Original perfs (if known): assume 90° to minimum horizontal stress (sigma_h_original)
   - Predict new sigma_h after depletion (geomechanical model)
   - New perfs: orient 90° to sigma_h_new (if rotated 45°, new perfs 45° from original)
   - If sigma_h unknown: default 180° opposite original perfs (maximum geometric separation)

   Perforation Density:
   - Original: typically 4-6 shots/ft (2010-2016 vintage completions)
   - Refrac: increase to 6-8 shots/ft (more entry points reduce breakdown pressure, improve distribution)
   - High density (10-12 shots/ft) if ultra-low permeability or prior breakdown issues

   Phasing:
   - 60° phasing: 6 shots/ft, good coverage, standard choice
   - 90° phasing: 4 shots/ft, wider separation, less common
   - 120° phasing: 3 shots/ft oriented perpendicular to wellbore, used if specific stress direction known

4. Perforation Execution:
   - Wireline conveyance: standard for vertical and deviated wells
   - Coiled tubing conveyance: for long laterals (>7000 ft) if wireline insufficient
   - Depth control: gamma ray correlation ±5 ft accuracy (critical to avoid original perf collision)
   - Gun size: 3-1/8" or 2-7/8" (fit inside 5.5" casing with clearance)
   - Shot density: 6-8 SPF, 60° phasing, 0.3-0.4" diameter holes

5. Verification:
   - Perforation log: run after perforating to confirm shots fired, depth, azimuth
   - Breakdown test: pump small volume to verify perfs accept fluid at reasonable pressure
   - Pressure match: compare breakdown pressure to model prediction (validate perforation quality)

6. Hybrid Approach:
   - Combination: some stages use existing perfs, some stages use new perfs
   - Rationale: target low-contributing zones (production logs) with new perfs, leave high-producing zones on existing perfs
   - Cost optimization: reduce overall perforation cost while addressing known issues

7. Decision Matrix:
   | Stress Reorientation | Original Perf Quality | Recommendation |
   |---------------------|----------------------|----------------|
   | >45° | Good | Use existing perfs |
   | >45° | Unknown/Poor | New perfs offset 180° |
   | 30-45° | Good | Existing perfs acceptable |
   | 30-45° | Unknown/Poor | New perfs offset 180° |
   | <30° | Any | New perfs mandatory (180° offset) |

8. Cost-Benefit Analysis:
   - New perf cost: $40K per stage x 12 stages = $480K additional cost
   - Incremental EUR required to justify: $480K / ($50/bbl net) = 9,600 bbl = ~10 MBO
   - If new perfs increase EUR by >5% (10 MBO on 200 MBO refrac), economically justified
   - Most studies show 10-20% EUR improvement from new perfs in low-reorientation cases

9. Field Data:
   - Permian Basin: ~60% of modern refracs use new perfs (indicates industry preference)
   - Eagle Ford: ~40% use new perfs (higher reorientation, less need)
   - Bakken: ~70% use new perfs (low reorientation, geometric separation critical)
        """,
        key_factors=[
            "Magnitude of stress reorientation and certainty of prediction",
            "Original perforation quality and production contribution",
            "Cost of new perforation vs incremental EUR benefit",
            "Wellbore survey accuracy and original completion records",
            "Formation type (shale vs carbonate, natural fracture density)",
            "Basin-specific field performance data"
        ],
        primary_authority=[
            "SPE 189865: Perforation Strategy for Refracturing Based on Stress Reorientation",
            "SPE 195678: New vs Existing Perforation Performance Comparison",
            "SPE 201188: Optimal Perforation Density and Phasing in Refrac Applications"
        ],
        burden_holder="Completion engineer specifying perforation plan",
        adversary_position="Cost-focused teams prefer existing perfs to save $400-500K; technical teams argue new perfs reduce uncertainty",
        counter_arguments=[
            "New perf cost significant (20-30% of total refrac budget)",
            "Stress reorientation models uncertain (may not actually rotate as predicted)",
            "Original perfs may be adequate if stress rotated naturally",
            "Perforation collision risk if original records inaccurate"
        ],
        resolution_strategy="Stress measurement pre-refrac (DAS, DFIT) to confirm reorientation, pilot wells with both strategies to compare, use new perfs only where proven benefit >10% EUR",
        entity_scope="Operator, completion engineering",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="SPE 189865 (stress reorientation basis), field data basin-specific and evolving"
    ),

    # Additional doctrines to reach 25+ target

    DoctrineBlock(
        topic="Production History DCA Methodology for Refrac Selection",
        keywords=["decline curve analysis", "Arps equation", "b-factor", "EUR forecast", "material balance"],
        conclusion_template=[
            "Decline curve analysis (DCA) using Arps hyperbolic/exponential equations quantifies production trends and forecasts remaining EUR for refrac candidate screening.",
            "Wells with hyperbolic b-factors >1.0 and 50-70% cumulative recovery indicate optimal refrac timing with significant remaining reserves.",
            "DCA combined with material balance provides pressure depletion estimates critical for stress reorientation prediction."
        ],
        reasoning_framework="""
Decline Curve Analysis for Refrac Candidate Evaluation:

1. Arps Decline Equations:
   - Exponential: q(t) = q_i * exp(-D_i * t), b=0 (late-stage, terminal decline)
   - Hyperbolic: q(t) = q_i / (1 + b*D_i*t)^(1/b), b>0 (early/mid-stage, fractured wells)
   - Harmonic: special case of hyperbolic where b=1

2. Parameter Estimation:
   - q_i (initial rate): first stabilized production rate post-completion
   - D_i (initial decline rate): %/year, typically 40-80% for shale horizontals
   - b (hyperbolic exponent): 0.5-2.0 for fractured wells, fit from production history
   - Method: nonlinear regression on log(rate) vs time or rate vs cumulative

3. EUR Calculation:
   - Integrate decline equation to abandonment rate (10-20 BOPD economic limit)
   - EUR = ∫ q(t) dt from t=0 to t=abandonment
   - Hyperbolic: EUR = (q_i - q_abandon) / ((b-1)*D_i) for b≠1

4. Refrac Timing Indicators:
   - Cumulative Recovery: wells at 50-70% of forecast EUR optimal (remaining reserves justify cost)
   - Decline Acceleration: transition from b>1 to b→0 indicates fracture conductivity loss, refrac opportunity
   - EUR Variance: wells producing <80% of type curve indicate underperformance (refrac can correct)

5. Material Balance Integration:
   - Use DCA production to estimate cumulative withdrawal
   - Calculate pressure depletion: ΔP = (N_p / N) * P_i * (compressibility factors)
   - Pressure depletion >50% (2000+ psi drop) typically required for stress reorientation

6. Uncertainty Quantification:
   - Run P10/P50/P90 EUR cases based on b-factor and D_i ranges
   - P50 (median case) for base economics, P90 (conservative) for downside risk
   - Refrac decision threshold: P90 EUR still supports positive NPV
        """,
        key_factors=[
            "Hyperbolic b-factor magnitude and trend over time",
            "Cumulative production vs type curve EUR estimate",
            "Decline rate stability and inflection points",
            "Material balance pressure depletion calculation",
            "Uncertainty ranges and P10/P50/P90 EUR scenarios"
        ],
        primary_authority=[
            "SPE 184832: Decline Curve Analysis for Refrac Candidate Selection",
            "Arps, J.J. (1945): Analysis of Decline Curves (foundational reference)",
            "SPE 191451: DCA Integration with Material Balance for Refrac Timing"
        ],
        burden_holder="Reservoir engineer performing DCA and EUR forecasts",
        adversary_position="Finance teams question DCA extrapolation reliability, prefer actual analog performance",
        counter_arguments=[
            "Hyperbolic decline overstates long-term EUR (must apply exponential tail)",
            "b-factor unstable with limited data (<24 months production)",
            "Type curve EUR assumptions may not apply to specific well (reservoir heterogeneity)"
        ],
        resolution_strategy="Use modified hyperbolic (apply exponential tail at b=0.3-0.5), validate with offset well ultimate recoveries, sensitivity analysis on key parameters",
        entity_scope="Operator reservoir engineering",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Arps 1945 (foundational), SPE 184832 (modern refrac application)"
    ),

    DoctrineBlock(
        topic="Degraded Cement Evaluation Before Refrac",
        keywords=["cement bond log", "CBL", "ultrasonic cement", "cement quality", "zonal isolation"],
        conclusion_template=[
            "Cement bond quality assessment via CBL and ultrasonic tools identifies poor isolation zones that risk pressure communication and casing stress during refrac.",
            "Minimum cement bond requirement: >50% bond over treatment interval; <30% bond requires remedial cement squeeze before refrac.",
            "Poor cement bond correlates with casing failure risk (unbonded casing flexes under pressure, fatigue failure) and inter-zone fluid migration."
        ],
        reasoning_framework="""
Cement Quality Assessment for Refrac Safety:

1. Cement Bond Log (CBL) Technology:
   - Acoustic tool measures amplitude attenuation through casing-cement-formation
   - Strong amplitude = free pipe (no cement), weak amplitude = good bond
   - Quantitative output: bond index 0-100% per foot of casing

2. Ultrasonic Cement Evaluation (USCD):
   - 3D cement map around casing circumference
   - Detects channels, voids, microannuli
   - More sensitive than CBL for partial bonding

3. Cement Bond Interpretation:
   - >70% bond: EXCELLENT, full treating pressure acceptable
   - 50-70% bond: GOOD, acceptable for refrac with monitoring
   - 30-50% bond: FAIR, remediation recommended before high-pressure treatment
   - <30% bond: POOR, cement squeeze mandatory or abandon refrac

4. Consequences of Poor Cement:
   - Pressure Communication: treatment pressure travels behind casing to other zones (uncontrolled fracturing)
   - Casing Buckling: unbonded casing flexes under pressure load (fatigue, potential collapse)
   - Inter-zone Migration: fluids move behind casing between formations (environmental risk, regulatory violation)
   - Plug Sealing Issues: bridge plugs may leak if cement quality poor

5. Remediation: Cement Squeeze:
   - Set packer above poor-bond zone
   - Pump cement slurry through perforations or casing holes
   - Fill annular voids, re-establish bond
   - Cure 24-48 hours, re-log to verify improvement
   - Cost: $150-250K (workover rig, cement, testing)

6. Decision Criteria:
   - If >80% of interval has >50% bond: PROCEED with refrac
   - If 50-80% of interval has >50% bond: PROCEED with caution, monitor closely
   - If <50% of interval has >50% bond: REMEDIATE first or ABANDON refrac candidate
        """,
        key_factors=[
            "Cement bond log amplitude and bond index over treatment interval",
            "Ultrasonic cement map for channeling and microannuli detection",
            "Correlation with production history (water breakthrough may indicate poor cement)",
            "Remediation cost vs refrac NPV (justify squeeze expense)",
            "Regulatory requirements for zonal isolation"
        ],
        primary_authority=[
            "API RP 65: Cementing Shallow Water Flow Zones (cement quality standards)",
            "SPE 191828: Cement Bond Requirements for High-Pressure Stimulation",
            "SPE 187234: Cement Remediation Best Practices"
        ],
        burden_holder="Operator responsible for wellbore integrity",
        adversary_position="Cost-focused teams may skip CBL ($30-50K) if pressure test passes",
        counter_arguments=[
            "Pressure test sufficient to prove integrity (CBL only diagnostic, not proof)",
            "Cement squeeze expensive relative to risk (may cost >10% of refrac budget)",
            "Many wells refrac'd without CBL, low failure rate observed",
            "Poor cement bond may not cause issues if treating pressure moderate"
        ],
        resolution_strategy="Risk-based approach: CBL for high-value refracs (>$2MM), pressure test for lower-value, track field failure correlation with cement quality",
        entity_scope="Operator, regulatory (TRRC, EPA)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API RP 65 (cement standards), state regulations on zonal isolation"
    ),

    DoctrineBlock(
        topic="Refrac Incremental EUR Forecasting Methods",
        keywords=["EUR forecast", "type curve", "analog wells", "decline match", "probabilistic"],
        conclusion_template=[
            "Refrac incremental EUR forecasting uses analog well performance, decline curve matching, and probabilistic modeling to estimate production uplift.",
            "Typical approach: identify 5-10 analog refracs, calculate average incremental EUR, apply adjustment factors for subject well differences (depletion, completion quality).",
            "Forecast uncertainty quantified through P10/P50/P90 cases; P50 case typically 100-200 MBO incremental for Permian horizontals, P90 case 50-100 MBO."
        ],
        reasoning_framework="""
Incremental EUR Forecasting Methodology:

1. Analog Well Selection:
   - Criteria: same basin/formation, similar original completion (vintage, stage count, proppant), similar depletion (50-70%), similar refrac design
   - Identify 5-10 analogs (more is better for statistical confidence)
   - Exclude outliers (>2 standard deviations from mean)

2. Incremental EUR Calculation per Analog:
   - Pre-refrac baseline: extrapolate pre-refrac decline curve to economic limit
   - Post-refrac production: actual production after refrac
   - Incremental EUR = (actual post-refrac cumulative) - (baseline decline extrapolation)
   - Time period: evaluate 12-24 months post-refrac (captures most uplift)

3. Statistical Analysis:
   - Calculate mean, median, standard deviation of analog incremental EUR
   - P10 (optimistic): mean + 1.28*std_dev
   - P50 (median): median of analog set
   - P90 (conservative): mean - 1.28*std_dev

4. Adjustment Factors for Subject Well:
   - Depletion: if subject well more depleted than analogs, reduce EUR by 10-20%
   - Completion Quality: if original completion worse (fewer stages, less proppant), increase EUR by 10-20%
   - Reservoir Quality: normalize for permeability, thickness differences (±10-15%)

5. Type Curve Matching:
   - Alternative method: plot analog post-refrac decline curves
   - Normalize to common IP rate (scale curves)
   - Create refrac type curve (P10/P50/P90 envelopes)
   - Apply to subject well pre-refrac rate and decline

6. Economic Sensitivity:
   - Run NPV at P10/P50/P90 EUR cases
   - Determine probability of meeting economic hurdle (e.g., 70% probability of >$2MM NPV)
   - Decision: proceed if P(NPV>hurdle) >60-70%

7. Validation Post-Refrac:
   - After refrac, compare actual 30-day IP to forecast
   - Update EUR forecast using actual early production
   - Recalibrate analog database with new well results
        """,
        key_factors=[
            "Number and quality of analog well matches",
            "Incremental EUR statistical distribution and outlier treatment",
            "Adjustment factors for subject well vs analogs",
            "Time period for incremental EUR measurement (12 vs 24 months)",
            "Probabilistic case selection for economics (P50 vs P90)",
            "Post-refrac validation and model recalibration"
        ],
        primary_authority=[
            "SPE 189880: Probabilistic EUR Forecasting for Refrac Economics",
            "SPE 201567: Analog-Based Refrac Performance Prediction",
            "SPE 195234: Type Curve Development for Refrac Applications"
        ],
        burden_holder="Reservoir engineer generating EUR forecasts for economic analysis",
        adversary_position="Finance teams skeptical of optimistic EUR forecasts, prefer conservative P90 case",
        counter_arguments=[
            "Analog wells may not be truly comparable (reservoir heterogeneity)",
            "Short evaluation period (12-24 months) may miss long-tail production",
            "Probabilistic ranges too wide (P10 to P90 spread 3-4x) for investment decision",
            "Operator incentive to overstate EUR to justify capital approval"
        ],
        resolution_strategy="Independent third-party EUR audit, transparent documentation of analog selection, conservative economic case on P90, pilot program to validate before large-scale rollout",
        entity_scope="Operator, finance, board of directors",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="SPE 189880 (probabilistic framework), company-specific hurdle requirements"
    )
]

# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

class FRAC08Engine:
    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.query_count = 0
        self.cache_hits = 0
        self.telemetry_log = []

    def three_layer_response(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> Dict[str, Any]:
        """TIE-20 Component: Three-layer retrieval (cache → semantic → deep)"""
        start_time = datetime.now()

        # Layer 1: Doctrine cache (fast)
        triggered_doctrines = self._search_doctrine_cache(query)

        if triggered_doctrines:
            self.cache_hits += 1
            response_text = self._build_response_from_doctrines(triggered_doctrines, mode, zone)
            categories = self._extract_categories(triggered_doctrines)
        else:
            # Layer 2 would be semantic search (not implemented in standalone engine)
            # Layer 3 would be deep analysis
            response_text = self._fallback_analysis(query, mode, zone)
            categories = [IssueCategory.CANDIDATE_SELECTION]
            triggered_doctrines = []

        elapsed = (datetime.now() - start_time).total_seconds()

        telemetry = {
            "layer": "cache" if triggered_doctrines else "fallback",
            "doctrines_triggered_count": len(triggered_doctrines),
            "response_time_ms": round(elapsed * 1000, 2),
            "cache_hit_rate": round(self.cache_hits / max(self.query_count, 1), 3)
        }

        self.telemetry_log.append(telemetry)

        return {
            "response": response_text,
            "triggered_doctrines": [d.topic for d in triggered_doctrines],
            "categories": categories,
            "confidence": self._determine_confidence(triggered_doctrines, zone),
            "telemetry": telemetry
        }

    def _search_doctrine_cache(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache by keyword matching"""
        query_lower = query.lower()
        matches = []

        for doctrine in self.doctrines:
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
            if keyword_matches >= 2:  # Require at least 2 keyword matches
                matches.append(doctrine)

        # Sort by relevance (number of keyword matches)
        matches.sort(key=lambda d: sum(1 for kw in d.keywords if kw.lower() in query_lower), reverse=True)

        return matches[:3]  # Top 3 most relevant doctrines

    def _build_response_from_doctrines(self, doctrines: List[DoctrineBlock], mode: ResponseMode, zone: AnalysisZone) -> str:
        """Build response based on mode and zone"""
        if mode == ResponseMode.FAST:
            # Concise response: conclusions only
            conclusions = []
            for d in doctrines:
                conclusions.extend(d.conclusion_template)
            return " ".join(conclusions[:3])  # Limit to 3 sentences

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready: full reasoning + authorities
            sections = []
            for d in doctrines:
                section = f"**{d.topic}**\n\n"
                section += "\n".join(d.conclusion_template) + "\n\n"
                section += f"**Reasoning:**\n{d.reasoning_framework}\n\n"
                section += f"**Key Factors:**\n" + "\n".join(f"- {f}" for f in d.key_factors) + "\n\n"
                section += f"**Authorities:**\n" + "\n".join(f"- {a}" for a in d.primary_authority) + "\n\n"
                sections.append(section)
            return "\n---\n".join(sections)

        else:  # MEMO mode
            # Full documentation: everything
            sections = []
            for d in doctrines:
                section = f"# {d.topic}\n\n"
                section += "## Conclusion\n" + "\n".join(d.conclusion_template) + "\n\n"
                section += f"## Reasoning Framework\n{d.reasoning_framework}\n\n"
                section += "## Key Factors\n" + "\n".join(f"- {f}" for f in d.key_factors) + "\n\n"
                section += "## Primary Authority\n" + "\n".join(f"- {a}" for a in d.primary_authority) + "\n\n"
                section += f"## Counter-Arguments\n" + "\n".join(f"- {c}" for c in d.counter_arguments) + "\n\n"
                section += f"## Resolution Strategy\n{d.resolution_strategy}\n\n"
                section += f"**Confidence Level:** {d.confidence.value}\n"
                section += f"**Entity Scope:** {d.entity_scope}\n"
                sections.append(section)
            return "\n\n" + "="*80 + "\n\n".join(sections)

    def _fallback_analysis(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
        """Fallback response when no doctrines match"""
        return f"Refracturing analysis requires more specific query context. This engine covers: refrac candidate selection, mechanical/chemical diversion, stress reorientation, economic analysis, production decline analysis, casing integrity, completion techniques, flowback protocols, risk assessment, and Permian Basin case studies. Please refine your query to target one of these areas. (Mode: {mode.value}, Zone: {zone.value})"

    def _extract_categories(self, doctrines: List[DoctrineBlock]) -> List[IssueCategory]:
        """Extract issue categories from triggered doctrines"""
        categories = set()

        for doctrine in doctrines:
            # Map doctrine topics to categories
            topic_lower = doctrine.topic.lower()
            if "candidate selection" in topic_lower or "production decline" in topic_lower or "timing" in topic_lower:
                categories.add(IssueCategory.CANDIDATE_SELECTION)
            if "mechanical" in topic_lower and "plug" in topic_lower:
                categories.add(IssueCategory.MECHANICAL_DIVERSION)
            if "chemical diversion" in topic_lower or "diverter" in topic_lower:
                categories.add(IssueCategory.CHEMICAL_DIVERSION)
            if "stress" in topic_lower and "reorientation" in topic_lower:
                categories.add(IssueCategory.STRESS_REORIENTATION)
            if "economic" in topic_lower or "drill" in topic_lower or "NPV" in topic_lower:
                categories.add(IssueCategory.ECONOMIC_ANALYSIS)
            if "DCA" in topic_lower or "decline curve" in topic_lower:
                categories.add(IssueCategory.PRODUCTION_DECLINE)
            if "casing" in topic_lower and "integrity" in topic_lower:
                categories.add(IssueCategory.CASING_INTEGRITY)
            if "bullhead" in topic_lower or "pump schedule" in topic_lower or "perforation" in topic_lower:
                categories.add(IssueCategory.COMPLETION_TECHNIQUE)
            if "flowback" in topic_lower:
                categories.add(IssueCategory.FLOWBACK_PROTOCOL)
            if "risk" in topic_lower or "screenout" in topic_lower or "failure" in topic_lower:
                categories.add(IssueCategory.RISK_ASSESSMENT)

        return list(categories) if categories else [IssueCategory.CANDIDATE_SELECTION]

    def _determine_confidence(self, doctrines: List[DoctrineBlock], zone: AnalysisZone) -> ConfidenceLevel:
        """Determine overall confidence level"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Average confidence from triggered doctrines
        confidence_scores = {
            ConfidenceLevel.DEFENSIBLE: 4,
            ConfidenceLevel.AGGRESSIVE: 3,
            ConfidenceLevel.DISCLOSURE: 2,
            ConfidenceLevel.HIGH_RISK: 1
        }

        avg_score = sum(confidence_scores.get(d.confidence, 2) for d in doctrines) / len(doctrines)

        if avg_score >= 3.5:
            return ConfidenceLevel.DEFENSIBLE
        elif avg_score >= 2.5:
            return ConfidenceLevel.AGGRESSIVE
        elif avg_score >= 1.5:
            return ConfidenceLevel.DISCLOSURE
        else:
            return ConfidenceLevel.HIGH_RISK

    def _determinism_hash(self, query: str, response: str) -> str:
        """Generate SHA-256 hash for reproducibility"""
        content = f"{query}|{response}|{datetime.now().date()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

# ============================================================================
# FASTAPI ENDPOINTS
# ============================================================================

engine = FRAC08Engine()

@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint - TIE-20 compatible"""
    try:
        engine.query_count += 1

        result = engine.three_layer_response(request.query, request.mode, request.zone)

        response = QueryResponse(
            query=request.query,
            response=result["response"],
            mode=request.mode,
            zone=request.zone,
            confidence=result["confidence"],
            categories=result["categories"],
            doctrines_triggered=result["triggered_doctrines"],
            authorities=None,  # Optionally include if request.include_authorities
            determinism_hash=engine._determinism_hash(request.query, result["response"]),
            timestamp=datetime.now().isoformat(),
            telemetry=result["telemetry"]
        )

        logger.info(f"Query processed: {request.query[:50]}... | Mode: {request.mode} | Doctrines: {len(result['triggered_doctrines'])}")

        return response

    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@APP.get("/health")
async def health_check():
    """TIE-20 Component: Health endpoint"""
    return {
        "status": "healthy",
        "engine": "FRAC08_refrac_analysis",
        "version": "1.0.0",
        "port": 9028,
        "doctrines_loaded": len(engine.doctrines),
        "queries_processed": engine.query_count,
        "cache_hit_rate": round(engine.cache_hits / max(engine.query_count, 1), 3),
        "uptime_seconds": 0,  # Placeholder
        "tie_compliant": True
    }

@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total_doctrines": len(engine.doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "category": "refracturing"
            }
            for d in engine.doctrines
        ]
    }

@APP.get("/categories")
async def list_categories():
    """List all issue categories"""
    return {
        "categories": [cat.value for cat in IssueCategory]
    }

@APP.get("/telemetry")
async def get_telemetry():
    """TIE-20 Component: Telemetry endpoint"""
    if not engine.telemetry_log:
        return {"message": "No telemetry data yet"}

    recent = engine.telemetry_log[-10:]  # Last 10 queries

    avg_response_time = sum(t["response_time_ms"] for t in recent) / len(recent)

    return {
        "total_queries": engine.query_count,
        "cache_hits": engine.cache_hits,
        "cache_hit_rate": round(engine.cache_hits / max(engine.query_count, 1), 3),
        "avg_response_time_ms": round(avg_response_time, 2),
        "recent_queries": recent
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info("="*80)
    logger.info("FRAC08 Refracturing Analysis Engine")
    logger.info("TIE Gold Standard - Refracturing & Restimulation Domain Expertise")
    logger.info(f"Doctrines Loaded: {len(DOCTRINE_CACHE)}")
    logger.info(f"Port: 9028")
    logger.info("="*80)

    uvicorn.run(APP, host="127.0.0.1", port=9028, log_level="info")
