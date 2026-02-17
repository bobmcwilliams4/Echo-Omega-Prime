"""
MECH09 - Pressure Vessel Design Engine
TIE Gold Standard - Mechanical Engineering Domain
Port: 9049 | Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ============================================================================
# ENUMS & CONSTANTS
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
    SHELL_DESIGN = "SHELL_DESIGN"
    HEAD_DESIGN = "HEAD_DESIGN"
    NOZZLE_REINFORCEMENT = "NOZZLE_REINFORCEMENT"
    SUPPORT_DESIGN = "SUPPORT_DESIGN"
    MATERIAL_SELECTION = "MATERIAL_SELECTION"
    TESTING_NDE = "TESTING_NDE"
    FABRICATION = "FABRICATION"
    IN_SERVICE = "IN_SERVICE"
    FITNESS_FOR_SERVICE = "FITNESS_FOR_SERVICE"
    OILFIELD_PRODUCTION = "OILFIELD_PRODUCTION"
    CODE_COMPLIANCE = "CODE_COMPLIANCE"
    REGISTRATION = "REGISTRATION"


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., description="Pressure vessel design question")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    context: Optional[Dict[str, Any]] = Field(default=None)
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING)


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    authorities: List[str]
    mode: ResponseMode
    zone: AnalysisZone
    determinism_hash: str
    latency_ms: float
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float


# ============================================================================
# DOCTRINE BLOCKS
# ============================================================================

@dataclass
class DoctrineBlock:
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
    category: IssueCategory


# ============================================================================
# DOCTRINE CACHE - 25+ REAL PRESSURE VESSEL EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="ASME Section VIII Division 1 Shell Thickness Calculation",
        keywords=["shell thickness", "cylinder", "ASME VIII-1", "internal pressure", "minimum thickness"],
        conclusion_template=[
            "Shell thickness for cylindrical vessels under internal pressure is calculated per ASME VIII-1 UG-27.",
            "Required thickness t = PR/(SE-0.6P) where P=design pressure, R=inside radius, S=allowable stress, E=weld joint efficiency.",
            "Minimum thickness after corrosion allowance must be verified."
        ],
        reasoning_framework="""
ASME Section VIII Division 1 UG-27 provides the fundamental formula for cylindrical shell thickness:
t = PR/(SE - 0.6P) for internal pressure

Where:
- P = design pressure (psig), typically MAWP or higher
- R = inside radius of shell (inches)
- S = allowable stress value from ASME Section II Part D (psi)
- E = weld joint efficiency (0.70 for spot RT, 0.85 for partial RT, 1.0 for full RT per UW-12)

The 0.6P term accounts for the effect of pressure on the stress calculation. For thin-wall vessels (P < 0.385SE),
this simplifies to t ≈ PR/SE.

Corrosion allowance (CA) must be added to calculated thickness: t_required = t_calc + CA
Common CA: 1/8" (3mm) for non-corrosive service, 1/4" (6mm) for corrosive service.

Material selection affects S value. SA-516 Gr 70 has S=20,000 psi at ambient, decreasing with temperature.
SA-240 304 stainless has S=20,000 psi at ambient for thin sections.

Minimum fabricated thickness is typically t + CA, but never less than code minimums (typically 1/16" for small vessels).
        """,
        key_factors=[
            "Design pressure (MAWP + margin, typically 10% over operating)",
            "Inside radius vs outside radius (formula uses IR)",
            "Material allowable stress from Section II Part D Table 1A",
            "Joint efficiency based on RT extent (UW-11, UW-12)",
            "Corrosion allowance based on service conditions",
            "Temperature effects on allowable stress",
            "Code-specified minimum thickness for vessel size",
            "Nominal vs minimum thickness for mill tolerances"
        ],
        primary_authority=[
            "ASME BPVC Section VIII Division 1, UG-27 (cylindrical shells)",
            "ASME Section II Part D Table 1A (allowable stress)",
            "ASME Section VIII Division 1 UW-12 (joint efficiency)",
            "ASME Section VIII Division 1 UG-16(b) (minimum thickness)"
        ],
        burden_holder="Design engineer must demonstrate calculated thickness meets code requirements",
        adversary_position="Thickness calculation may not account for local loads, fabrication tolerances, or secondary stresses",
        counter_arguments=[
            "Formula assumes uniform internal pressure only",
            "Does not include bending from supports or external loads",
            "Assumes perfect cylindrical geometry",
            "Does not account for localized corrosion or pitting",
            "Joint efficiency may be optimistic if weld quality varies"
        ],
        resolution_strategy="Add thickness margin for uncertainty (10-15%), use conservative joint efficiency, verify fabrication tolerances, consider Division 2 design-by-analysis for complex loadings",
        entity_scope="All cylindrical pressure vessels under internal pressure per ASME VIII-1",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard cylindrical shells, moderate for vessels with combined loads",
        controlling_precedent="ASME BPVC VIII-1 UG-27 is universally accepted for shell thickness calculations",
        category=IssueCategory.SHELL_DESIGN
    ),

    DoctrineBlock(
        topic="Ellipsoidal Head Design per ASME VIII-1",
        keywords=["ellipsoidal head", "2:1 head", "torispherical", "dished head", "head thickness"],
        conclusion_template=[
            "Ellipsoidal heads (2:1 ratio) are designed per ASME VIII-1 UG-32(d) using t = PD/(2SE-0.2P).",
            "2:1 ellipsoidal heads have D = major axis (vessel OD), depth = D/4, providing efficient stress distribution.",
            "Thickness is typically less than equivalent cylinder due to favorable geometry."
        ],
        reasoning_framework="""
ASME VIII-1 UG-32(d) provides formula for ellipsoidal heads with D/2h ratio of 2:1:
t = PD/(2SE - 0.2P)

Where:
- D = major axis diameter (vessel inside diameter for 2:1 ellipsoidal head)
- P = design pressure
- S = allowable stress
- E = weld joint efficiency (typically 1.0 for seamless heads)

The 2:1 ellipsoidal head is the most common dished head in pressure vessel design:
- Major axis = vessel ID
- Minor axis (depth) = ID/4
- Provides excellent stress distribution (approx 2x more efficient than flat head)
- Membrane stress is roughly twice the hoop stress in the cylinder

For heads with D/2h other than 2:1, use UG-32(e) with stress intensification factor.

Seamless heads (spun, pressed) typically have E=1.0. Welded segmented heads use applicable E per joint category.

Knuckle radius and crown radius must meet UG-32 requirements:
- For 2:1 heads: crown radius ≈ D, knuckle radius ≈ 0.17D
- Actual radii from manufacturer must be verified

Thickness at center is uniform; junction with cylinder (knuckle) has higher stress but code formula accounts for this.
        """,
        key_factors=[
            "Head type: 2:1 ellipsoidal most common, hemispherical most efficient",
            "Inside diameter vs outside diameter (formula uses ID for 2:1 heads)",
            "Seamless vs welded head construction (affects E)",
            "Crown radius and knuckle radius verification",
            "Corrosion allowance addition",
            "Nozzle penetrations in head (require reinforcement per UG-37)",
            "Transition to cylinder (junction design per UW-13)"
        ],
        primary_authority=[
            "ASME VIII-1 UG-32(d) for 2:1 ellipsoidal heads",
            "ASME VIII-1 UG-32(e) for other ellipsoidal ratios",
            "ASME VIII-1 Appendix 1-4 for detailed head design",
            "ASME VIII-1 UG-81 for head tolerances"
        ],
        burden_holder="Designer must verify head geometry matches code assumptions and manufacturer cert",
        adversary_position="Actual head geometry may deviate from theoretical 2:1 ratio, affecting stress distribution",
        counter_arguments=[
            "Manufacturing tolerances can alter D/2h ratio",
            "Knuckle radius variation affects stress concentration",
            "Weld joint at cylinder-head junction may be weak point",
            "Local loads from supports or attachments not addressed",
            "Head nozzles create stress concentrations"
        ],
        resolution_strategy="Verify manufacturer's certified dimensions, add thickness margin for tolerances, reinforce nozzles per UG-37, use Division 2 FEA for critical vessels",
        entity_scope="All ellipsoidal dished heads per ASME VIII-1",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard 2:1 heads, moderate for non-standard ratios",
        controlling_precedent="ASME VIII-1 UG-32 is the universal standard for dished head design",
        category=IssueCategory.HEAD_DESIGN
    ),

    DoctrineBlock(
        topic="Hemispherical Head Design - Most Efficient Geometry",
        keywords=["hemispherical head", "hemisphere", "half sphere", "dome"],
        conclusion_template=[
            "Hemispherical heads are the most efficient pressure-containing geometry, requiring t = PL/(2SE-0.2P).",
            "L = head radius (typically = vessel ID), resulting in thickness approximately half that of cylinder.",
            "Used for high-pressure vessels where material savings justify higher fabrication cost."
        ],
        reasoning_framework="""
ASME VIII-1 UG-32(a) formula for hemispherical heads:
t = PL/(2SE - 0.2P) where L = inside radius of hemisphere

The hemisphere is the ideal pressure-containing shape:
- Uniform membrane stress in all directions
- Stress = PR/(2t), exactly half the hoop stress in a cylinder
- No bending moments in perfect sphere under uniform pressure

For a hemispherical head with L = vessel ID/2:
- Required thickness is approximately 50% of equivalent cylinder thickness
- Material savings can be substantial for large or high-pressure vessels
- Fabrication cost is higher (forming, welding)

Typically used when:
- Pressure > 3000 psi (material savings outweigh fabrication cost)
- Large diameter vessels (material cost dominates)
- Weight-critical applications (aerospace, mobile vessels)

Challenges:
- More expensive to fabricate than ellipsoidal heads
- Requires specialized forming equipment
- May require segmented construction (welded gores) for large diameters
- Junction with cylinder requires careful design (stress concentration)

Segmented hemispheres use multiple "gores" (segments) welded together. Joint efficiency applies to gore welds.
        """,
        key_factors=[
            "Inside radius L (typically vessel ID/2)",
            "Design pressure and allowable stress",
            "Seamless vs segmented construction",
            "Gore weld joint efficiency for segmented heads",
            "Economic tradeoff: material savings vs fabrication cost",
            "Junction design with cylindrical shell",
            "Tolerance on spherical radius (affects stress uniformity)"
        ],
        primary_authority=[
            "ASME VIII-1 UG-32(a) for hemispherical heads",
            "ASME VIII-1 UG-79 for spherical shell tolerances",
            "ASME VIII-1 UW-13 for head-to-shell welds"
        ],
        burden_holder="Designer must justify economic and technical basis for hemispherical head selection",
        adversary_position="Fabrication cost and complexity may outweigh material savings, especially for moderate pressures",
        counter_arguments=[
            "Ellipsoidal heads are nearly as efficient at lower fabrication cost",
            "Segmented construction introduces weld joint efficiency penalties",
            "Tolerance stackup can create out-of-roundness",
            "Junction with cylinder may require thickening",
            "Inspection of internal gore welds is difficult"
        ],
        resolution_strategy="Perform economic analysis comparing material vs fabrication cost, use seamless forming when possible, specify tight tolerances on radius, use transition cone if needed",
        entity_scope="High-pressure vessels, large-diameter vessels, weight-critical applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for design calculations, moderate for economic justification",
        controlling_precedent="ASME VIII-1 UG-32(a) governs hemispherical head design",
        category=IssueCategory.HEAD_DESIGN
    ),

    DoctrineBlock(
        topic="Torispherical Head Design (ASME F&D Head)",
        keywords=["torispherical", "flanged and dished", "F&D head", "ASME head", "knuckle radius"],
        conclusion_template=[
            "Torispherical (F&D) heads are designed per ASME VIII-1 UG-32(c) with specific crown and knuckle radius ratios.",
            "Standard ASME F&D head: crown radius = vessel OD, knuckle radius = 6% of OD.",
            "Less efficient than ellipsoidal but easier to fabricate from flat plate."
        ],
        reasoning_framework="""
ASME VIII-1 UG-32(c) formula for torispherical heads:
t = (0.885 * P * L)/(SE - 0.1P) where L = crown radius

Torispherical head geometry:
- Crown (spherical dish) with radius L
- Knuckle (toroidal section) with radius r connecting crown to straight flange
- Straight flange section for welding to shell

Standard ASME F&D head ratios:
- Crown radius L = vessel OD (outside diameter)
- Knuckle radius r = 6% of OD (0.06 * OD)
- These ratios give factor M = 1.77 in stress calculation

The 0.885 factor comes from stress intensification in the knuckle region:
- Crown stress is relatively low (similar to hemisphere)
- Knuckle experiences high bending stress (2-3x crown stress)
- Code formula ensures knuckle stress stays within limits

Torispherical vs Ellipsoidal:
- Torispherical requires ~40% more thickness than 2:1 ellipsoidal
- Easier to fabricate (simple dishing operation)
- Lower cost for small to medium vessels
- Higher knuckle stress concentrates fatigue damage

Variations:
- ASME F&D (L=OD, r=0.06*OD) is standard
- Korbbogen head (European, different ratios)
- Custom ratios require UG-32(e) calculations
        """,
        key_factors=[
            "Crown radius L (typically vessel OD for standard F&D)",
            "Knuckle radius r (typically 6% OD for standard F&D)",
            "Ratio L/r affects stress intensification factor M",
            "Fabrication method (cold forming, hot forming)",
            "Knuckle stress concentration under fatigue loading",
            "Minimum knuckle radius per UG-32(c): r ≥ 0.06L",
            "Thickness greater than ellipsoidal for same pressure"
        ],
        primary_authority=[
            "ASME VIII-1 UG-32(c) for torispherical heads",
            "ASME VIII-1 UG-32(e) for non-standard ratios",
            "ASME VIII-1 UG-81 for head forming tolerances"
        ],
        burden_holder="Designer must verify actual crown and knuckle radii match code assumptions",
        adversary_position="Knuckle stress concentration makes torispherical heads prone to fatigue in cyclic service",
        counter_arguments=[
            "Ellipsoidal heads are more efficient for same pressure",
            "Knuckle region is fatigue-critical (not addressed in Division 1)",
            "Actual radii may vary from theoretical due to springback",
            "Higher thickness increases cost and weight",
            "Not suitable for high-cycle fatigue applications"
        ],
        resolution_strategy="Use ellipsoidal heads for fatigue service, verify manufacturer radii certification, add fatigue analysis per Division 2 if needed, consider knuckle thickness increase",
        entity_scope="Low to moderate pressure vessels where fabrication cost is priority",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Code formula is conservative but doesn't address fatigue explicitly",
        controlling_precedent="ASME VIII-1 UG-32(c) for standard torispherical, UG-32(e) for custom",
        category=IssueCategory.HEAD_DESIGN
    ),

    DoctrineBlock(
        topic="Nozzle Reinforcement - Area Replacement Method",
        keywords=["nozzle reinforcement", "area replacement", "UG-37", "compensation", "opening"],
        conclusion_template=[
            "Nozzle openings require reinforcement per ASME VIII-1 UG-37 area replacement method.",
            "Area removed by opening must be replaced within defined limits by excess thickness in shell, nozzle, and reinforcing pad.",
            "Reinforcement zone dimensions and area calculations are precisely specified by code."
        ],
        reasoning_framework="""
ASME VIII-1 UG-37 area replacement method ensures nozzle opening doesn't weaken vessel:

Required Area (A):
A = d * tr * F where:
- d = nozzle diameter (ID of opening)
- tr = required thickness of shell (before CA)
- F = stress correction factor (typically 1.0 for same material)

Available Reinforcement Areas:
A1 = Excess thickness in shell (within reinforcement zone)
A2 = Excess thickness in nozzle wall projecting outward
A3 = Excess thickness in nozzle wall projecting inward
A41 = Area of reinforcing pad (if used)

Reinforcement limits (dimensions of reinforcement zone):
- Parallel to vessel: d (diameter on each side of centerline)
- Perpendicular to vessel: 2.5t or 2.5tn, whichever is smaller

Adequacy check: A1 + A2 + A3 + A41 ≥ A

Design strategies:
1. Increase shell thickness locally (integrally reinforced)
2. Increase nozzle wall thickness
3. Add reinforcing pad (common for pipe nozzles)
4. Use forged nozzle neck with taper

Strength welds:
- Nozzle-to-shell weld must be full penetration
- Pad-to-shell weld must develop pad strength
- Minimum fillet size per UW-16

Special cases:
- Radial nozzles (90° to shell): standard calculation
- Hillside nozzles (angled): require projection correction
- Nozzles in formed heads: may use different limits
- Multiple adjacent nozzles: interaction must be checked
        """,
        key_factors=[
            "Nozzle diameter and shell required thickness",
            "Material stress correction factor F",
            "Reinforcement zone dimensions (limits of credit)",
            "Excess thickness available in shell and nozzle",
            "Reinforcing pad dimensions and thickness",
            "Weld strength and penetration requirements",
            "Hillside nozzle angle correction",
            "Multiple nozzle interaction (spacing < 2*avg diameter)"
        ],
        primary_authority=[
            "ASME VIII-1 UG-37 for area replacement method",
            "ASME VIII-1 UG-40 for reinforcement limits",
            "ASME VIII-1 UW-15, UW-16 for nozzle welds",
            "ASME VIII-1 Appendix 1-7 for hillside nozzles"
        ],
        burden_holder="Designer must demonstrate adequate reinforcement area within code limits",
        adversary_position="Area replacement method is simplified and doesn't capture actual stress distribution around opening",
        counter_arguments=[
            "Method assumes uniform stress field (not true near nozzle)",
            "Doesn't account for bending stress at nozzle junction",
            "Pad edge creates stress concentration (not analyzed)",
            "Weld heat-affected zone may have reduced strength",
            "Method doesn't address fatigue or local loads on nozzle"
        ],
        resolution_strategy="Use Division 2 FEA for critical nozzles, add safety margin (10-20% extra area), use integral reinforcement when possible, perform fatigue analysis if cyclic",
        entity_scope="All nozzles and openings in ASME VIII-1 vessels",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for static pressure, moderate for fatigue or dynamic loads",
        controlling_precedent="ASME VIII-1 UG-37 is universally applied for nozzle reinforcement",
        category=IssueCategory.NOZZLE_REINFORCEMENT
    ),

    DoctrineBlock(
        topic="ASME Section VIII Division 2 - Design by Analysis",
        keywords=["Division 2", "design by analysis", "FEA", "stress categories", "elastic-plastic"],
        conclusion_template=[
            "ASME VIII-2 permits design by analysis using detailed stress categorization and higher allowable stresses.",
            "Allows FEA-based design with elastic or elastic-plastic analysis methods.",
            "Results in thinner, lighter vessels with rigorous analysis requirements."
        ],
        reasoning_framework="""
ASME Section VIII Division 2 provides alternative rules allowing detailed stress analysis:

Key differences from Division 1:
- Higher allowable stresses (S = 2/3 yield vs Division 1 at various factors)
- Requires detailed stress analysis (FEA typically)
- Stress categorization: primary, secondary, peak
- Fatigue analysis required for cyclic service
- More rigorous material testing and quality requirements

Design by Analysis methods (Part 5):
1. Elastic analysis with stress categorization
2. Limit load analysis (plastic collapse)
3. Elastic-plastic analysis (ratcheting, shakedown)

Stress categories:
- Primary membrane (Pm): uniform through thickness, limit = S
- Primary bending (Pb): linear through thickness, Pm+Pb limit = 1.5S
- Secondary (Q): self-limiting (thermal, discontinuity), Pm+Pb+Q limit = 3S
- Peak (F): local (notch, weld), affects fatigue only

Protection against failure modes:
- Plastic collapse: limit load ≥ design pressure
- Local failure: Pm ≤ S, Pm+Pb ≤ 1.5S
- Collapse from buckling: eigenvalue analysis
- Cyclic loading: fatigue curves with usage factor
- Ratcheting: elastic-plastic shakedown analysis

Material requirements (Division 2 more stringent):
- Normalized or quenched-and-tempered required for many steels
- Charpy impact testing required
- Material test reports with full chemistry and properties

Fabrication requirements:
- Full radiography typically required
- PWHT requirements more extensive
- Stricter tolerances on geometry

Typical weight savings: 20-40% vs Division 1 for same vessel
        """,
        key_factors=[
            "Design approach: elastic, limit load, or elastic-plastic",
            "Stress categorization and allowable limits",
            "FEA mesh quality and convergence",
            "Material properties for analysis (E, ν, yield, ultimate)",
            "Load cases: pressure, thermal, external, seismic",
            "Fatigue analysis for cyclic service",
            "Protection against buckling, ratcheting",
            "Material testing and quality requirements (Part 3)"
        ],
        primary_authority=[
            "ASME VIII-2 Part 5 (Design by Analysis)",
            "ASME VIII-2 Part 3 (Materials)",
            "ASME VIII-2 Section 5.2 (Protection Against Plastic Collapse)",
            "ASME VIII-2 Section 5.5 (Fatigue Assessment)"
        ],
        burden_holder="Designer must demonstrate competence in FEA and Division 2 methodology",
        adversary_position="Division 2 complexity and cost may not be justified for simple vessels",
        counter_arguments=[
            "Requires expensive FEA software and trained analysts",
            "More complex material and fabrication requirements increase cost",
            "Inspector familiarity with Division 2 may be limited",
            "Errors in FEA modeling can be non-conservative",
            "Jurisdictional acceptance may vary (some states prefer Division 1)"
        ],
        resolution_strategy="Use Division 2 for high-pressure or weight-critical vessels where savings justify cost, third-party FEA review for critical vessels, ensure fabricator and inspector Division 2 experience",
        entity_scope="High-pressure vessels, large vessels, weight-critical applications, cyclic service",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="High confidence if proper FEA and analysis, moderate risk from modeling errors",
        controlling_precedent="ASME VIII-2 is accepted alternative to Division 1, requires Design Report",
        category=IssueCategory.CODE_COMPLIANCE
    ),

    DoctrineBlock(
        topic="Maximum Allowable Working Pressure (MAWP) Calculation",
        keywords=["MAWP", "maximum allowable working pressure", "UG-98", "nameplate pressure"],
        conclusion_template=[
            "MAWP is the maximum gauge pressure permissible at the top of the vessel in operating position at designated temperature.",
            "Calculated per ASME VIII-1 UG-98 based on weakest component (shell, head, nozzle, flange).",
            "MAWP appears on nameplate and defines legal operating limit."
        ],
        reasoning_framework="""
ASME VIII-1 UG-98 defines MAWP calculation methodology:

MAWP is determined by:
1. Calculate pressure rating of each component (shell, heads, nozzles, flanges) at design temperature
2. MAWP = minimum pressure rating among all components
3. Adjust for static head if significant

Component pressure ratings:
- Cylindrical shell: P = (SE*t)/(R + 0.6t) [from UG-27 rearranged]
- 2:1 Ellipsoidal head: P = (2SE*t)/(D + 0.2t)
- Hemispherical head: P = (2SE*t)/(L + 0.2t)
- Nozzle necks, flanges: per applicable code sections

Temperature effects:
- S (allowable stress) decreases with temperature per Section II-D
- MAWP must be specified at design temperature
- If multiple operating temperatures, may specify multiple MAWP values

Corrosion allowance:
- Use minimum thickness (as-fabricated minus CA) for MAWP calculation
- MAWP decreases over vessel life as corrosion occurs
- Periodic re-rating required per API 510 for in-service vessels

Static head correction:
- For tall vessels, pressure at bottom exceeds MAWP
- Maximum pressure = MAWP + static head (ρgh)
- Design must account for maximum pressure at bottom

Overpressure protection:
- Relief device set pressure ≤ MAWP (typically MAWP or 1.1*MAWP if fire case)
- Accumulated pressure during relief ≤ 1.1*MAWP (1.21*MAWP for fire)
- Multiple relief devices may be required

Nameplate requirements (UG-116):
- MAWP in psig (or kPag)
- Design temperature in °F (or °C)
- Manufacturer name and U-stamp
- National Board registration number (if registered)
        """,
        key_factors=[
            "Minimum thickness of each component after CA",
            "Allowable stress at design temperature",
            "Weakest component governs MAWP",
            "Joint efficiency of governing component",
            "Static head for tall vessels",
            "Relief device set pressure coordination",
            "Temperature variation effects on MAWP",
            "Re-rating requirements for in-service vessels"
        ],
        primary_authority=[
            "ASME VIII-1 UG-98 (MAWP definition and calculation)",
            "ASME VIII-1 UG-99 (pressure relief devices)",
            "ASME VIII-1 UG-116 (nameplate requirements)",
            "API 510 (in-service inspection and re-rating)"
        ],
        burden_holder="Manufacturer must certify MAWP based on as-built dimensions and Code calculations",
        adversary_position="Actual operating pressure may exceed MAWP due to process upsets or relief device failure",
        counter_arguments=[
            "MAWP doesn't account for transient pressure spikes",
            "Temperature variation can reduce actual safe pressure",
            "Corrosion reduces MAWP over time (not monitored continuously)",
            "Nozzle loads can create local stress exceeding pressure rating",
            "Relief device capacity may be inadequate for all scenarios"
        ],
        resolution_strategy="Design pressure higher than operating (10-25% margin), ensure relief device adequacy, implement pressure monitoring/alarms, periodic thickness testing per API 510",
        entity_scope="All ASME pressure vessels requiring nameplate certification",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for new vessels, moderate for aged vessels with corrosion",
        controlling_precedent="ASME VIII-1 UG-98 defines legally binding MAWP for stamped vessels",
        category=IssueCategory.CODE_COMPLIANCE
    ),

    DoctrineBlock(
        topic="Hydrostatic Testing Requirements per ASME VIII-1",
        keywords=["hydrostatic test", "pressure test", "UG-99", "test pressure", "water test"],
        conclusion_template=[
            "All ASME VIII-1 vessels require hydrostatic test at 1.3*MAWP minimum per UG-99.",
            "Test must be held for sufficient time to permit visual examination of all surfaces and joints.",
            "Pneumatic test permitted only when hydrostatic is impractical, at 1.1*MAWP with additional precautions."
        ],
        reasoning_framework="""
ASME VIII-1 UG-99 hydrostatic test requirements:

Test pressure:
- Standard: 1.3 * MAWP * (Sa/Sd)
  where Sa = allowable stress at test temperature (ambient)
        Sd = allowable stress at design temperature
- For vessels with design temperature < ambient, ratio Sa/Sd > 1, so test pressure increases
- Minimum test pressure: 1.3 * MAWP

Test procedure:
1. Fill vessel with water or other suitable liquid
2. Pressurize to test pressure gradually
3. Hold pressure for minimum time (typically 30 min for small vessels, longer for large)
4. Visually examine all welds, joints, surfaces for leakage or deformation
5. Reduce pressure and drain

Test fluid:
- Water is standard (readily available, safe, incompressible)
- Temperature ≥ ambient dew point (prevent brittle fracture)
- For stainless: chloride content < 50 ppm (prevent stress corrosion cracking)
- For vessels in low-temperature service: test temperature ≥ MDMT + 50°F

Acceptance criteria:
- No visible leakage
- No visible permanent deformation
- No cracking or tearing
- Pressure gauge must remain stable

Pneumatic test (UG-100):
- Only when hydrostatic is impractical (weight, contamination concerns)
- Test pressure: 1.1 * MAWP * (Sa/Sd)
- Additional safety precautions required (blast shields, personnel exclusion)
- Typically requires Owner and Inspector approval

Post-weld heat treatment (PWHT):
- If required by UCS-56, must be done BEFORE hydrostatic test
- Test after PWHT verifies vessel integrity after thermal cycle

Test documentation:
- Manufacturer's Data Report (Form U-1) includes test pressure and temperature
- Inspector witness and sign-off required
- Photographs may be required for certain jurisdictions
        """,
        key_factors=[
            "Test pressure calculation with temperature correction",
            "Hold time based on vessel size",
            "Visual examination during test",
            "Test fluid selection (water quality, temperature)",
            "PWHT completion before test",
            "MDMT compliance (test temperature)",
            "Pneumatic test special precautions if required",
            "Documentation and inspector witness"
        ],
        primary_authority=[
            "ASME VIII-1 UG-99 (hydrostatic test)",
            "ASME VIII-1 UG-100 (pneumatic test)",
            "ASME VIII-1 UG-84 (pressure relief during test)",
            "ASME VIII-1 UCS-66, UCS-67 (impact test exemptions based on test temperature)"
        ],
        burden_holder="Manufacturer must perform test per code and provide documentation",
        adversary_position="Hydrostatic test may not reveal all defects, especially fatigue-prone areas or leak paths",
        counter_arguments=[
            "Test pressure is static (doesn't simulate cyclic or dynamic loads)",
            "Small leak paths may seal under test pressure then leak in service",
            "Water contamination risk for stainless or sensitive materials",
            "Test doesn't verify corrosion resistance or long-term integrity",
            "Pneumatic test is less conservative (stored energy risk)"
        ],
        resolution_strategy="Supplement with NDE (RT, UT, MT, PT) for critical welds, ensure proper PWHT, use filtered/treated water for stainless, hold pressure longer for large vessels",
        entity_scope="All new ASME VIII-1 pressure vessels before initial service",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence that test verifies pressure integrity, moderate for long-term service",
        controlling_precedent="ASME VIII-1 UG-99 hydrostatic test is mandatory for Code compliance and U-stamp",
        category=IssueCategory.TESTING_NDE
    ),

    DoctrineBlock(
        topic="Saddle Support Design Using Zick Analysis",
        keywords=["saddle support", "Zick analysis", "vessel support", "stiffening ring", "wear plate"],
        conclusion_template=[
            "Horizontal cylindrical vessels on saddle supports are designed using Zick method (or modern FEA).",
            "Zick method addresses shell stresses: circumferential bending at horn, longitudinal bending at saddle.",
            "Stiffening rings or wear plates may be required to prevent local shell buckling."
        ],
        reasoning_framework="""
Saddle supports for horizontal vessels create localized stresses analyzed by Zick method:

Key stress locations:
1. Circumferential bending at saddle horn (12 o'clock and 6 o'clock positions)
2. Longitudinal bending at saddle centerline
3. Tangential shear at saddle edges
4. Compressive stress under saddle (potential buckling)

Zick analysis approach:
- Treat vessel as beam on two supports
- Calculate reactions from deadweight + contents + attachments
- Compute shell bending stresses using shell theory
- Check combined pressure + support stresses against allowables

Critical dimensions:
- Saddle spacing (L): typically 0.2-0.4 of vessel length for minimum stress
- Contact angle (θ): typically 120-150° for optimal load distribution
- Saddle width: affects bearing stress on shell
- Distance from tangent line (a): affects moment arm

Wear plates:
- Steel plates welded to shell at saddle contact area
- Distribute load over larger area (reduce bearing stress)
- Stiffen shell against local buckling
- Typical thickness: 1/4" to 1/2" depending on load

Stiffening rings:
- Required if circumferential bending stress exceeds allowable
- Full-circumference rings at saddle locations
- Designed as ring in compression with external radial load
- May be inside or outside shell

Longitudinal stress check:
- Vessel acts as beam in bending between saddles
- Maximum moment at midspan (uniform load) or at saddles (concentrated load)
- Combined pressure + bending stress must be within limits

Modern practice:
- FEA increasingly used instead of Zick (more accurate for complex geometry)
- Zick method is conservative for standard configurations
- Non-standard geometries (oval shells, insulated) require FEA
        """,
        key_factors=[
            "Saddle spacing and location optimization",
            "Contact angle (120° minimum typical)",
            "Vessel weight (empty + operating + test)",
            "Wind and seismic loads if applicable",
            "Shell thickness and stiffness",
            "Wear plate or stiffening ring requirements",
            "Weld design for attachments to shell",
            "Longitudinal bending stress combined with pressure"
        ],
        primary_authority=[
            "Zick, L.P. 'Stresses in Large Horizontal Cylindrical Pressure Vessels on Two Saddle Supports' (original paper)",
            "ASME VIII-1 Appendix G (historical, now non-mandatory)",
            "Bednar, H.H. 'Pressure Vessel Design Handbook' (detailed Zick procedures)",
            "PD 5500 Annex G (British Standard, similar approach)"
        ],
        burden_holder="Designer must verify saddle design prevents excessive shell stress and local buckling",
        adversary_position="Zick method makes simplifying assumptions that may not match actual behavior",
        counter_arguments=[
            "Assumes uniform shell thickness (local thin areas not addressed)",
            "Doesn't account for initial out-of-roundness",
            "Elastic analysis only (no plasticity or buckling)",
            "Wind/seismic loads may dominate in some cases",
            "Attachment welds are stress concentrations (fatigue risk)"
        ],
        resolution_strategy="Use FEA for critical or non-standard vessels, add stiffening rings conservatively, verify weld design, consider dynamic loads, inspect shell roundness",
        entity_scope="Horizontal cylindrical pressure vessels on saddle supports",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence - method is widely used but has known limitations",
        controlling_precedent="Zick method is industry standard, though not in current ASME VIII-1 mandatory rules",
        category=IssueCategory.SUPPORT_DESIGN
    ),

    DoctrineBlock(
        topic="Material Selection - Carbon Steel SA-516 Grade 70",
        keywords=["SA-516", "carbon steel", "pressure vessel plate", "Grade 70", "material properties"],
        conclusion_template=[
            "SA-516 Grade 70 is the most common carbon steel for pressure vessel shells and heads.",
            "Minimum tensile strength 70 ksi, yield 38 ksi, good weldability and toughness.",
            "Suitable for moderate temperatures (-20°F to 650°F) and general process service."
        ],
        reasoning_framework="""
ASME SA-516 (ASTM A516) Carbon Steel Plate for Pressure Vessels:

Chemical composition (Grade 70):
- Carbon: 0.27% max (weldable without preheat for thin sections)
- Manganese: 0.79-1.30% (provides strength and toughness)
- Phosphorus: 0.035% max, Sulfur: 0.035% max (low for good weldability)
- Silicon: 0.13-0.45%

Mechanical properties (Grade 70):
- Tensile strength: 70-90 ksi
- Yield strength: 38 ksi minimum
- Elongation: 21% minimum in 2" (17% in 8")
- Reduction of area: not specified

Allowable stress (ASME Section II Part D):
- At ambient: 17,500 psi (tensile basis) or 20,000 psi (yield basis), use 17,500 psi
- Decreases with temperature: 15,700 psi @ 300°F, 14,000 psi @ 500°F
- Not permitted above 700°F per code

Temperature limits:
- MDMT (minimum design metal temperature): depends on thickness and impact testing
- Without impact testing: typically limited to 20°F or higher (per UCS-66)
- With Charpy impact testing: can go to -20°F or lower
- Maximum: 650°F for long-term service (creep becomes concern above)

Heat treatment:
- Supplied normalized or as-rolled (no PWHT required for fabrication)
- PWHT after welding per UCS-56: required if thickness > 1.25" (varies by P-No.)

Weldability:
- Excellent with common processes (SMAW, GMAW, SAW, FCAW)
- Preheat typically not required for thin sections (< 1")
- Thicker sections may require preheat (200-300°F) to prevent cracking

Corrosion resistance:
- Moderate atmospheric corrosion (rusts in humid environment)
- 1/8" to 1/4" corrosion allowance typical for process service
- Not suitable for sour service (H2S) without special treatment
- Can be clad or lined for corrosive service

Typical applications:
- Oil and gas production vessels
- Refinery process vessels (non-sour, moderate temperature)
- Water tanks and storage vessels
- General industrial pressure vessels
        """,
        key_factors=[
            "Grade selection (70 most common, 60 and 65 also available)",
            "Allowable stress temperature dependence",
            "Impact testing requirements for low temperature (UCS-66)",
            "PWHT requirements based on thickness (UCS-56)",
            "Preheat requirements for welding thick sections",
            "Corrosion allowance for service environment",
            "Alternative materials for severe service (sour, high temp)",
            "Mill test report (MTR) certification requirements"
        ],
        primary_authority=[
            "ASME SA-516 / ASTM A516 material specification",
            "ASME Section II Part D Table 1A (allowable stress)",
            "ASME VIII-1 UCS-56 (PWHT requirements)",
            "ASME VIII-1 UCS-66 (impact test exemptions)"
        ],
        burden_holder="Designer must select material suitable for temperature, pressure, and corrosive environment",
        adversary_position="SA-516 may not be suitable for all services, especially low temperature or corrosive",
        counter_arguments=[
            "Limited low-temperature toughness (requires impact testing below 20°F)",
            "Poor corrosion resistance (needs coating or CA)",
            "Not suitable for sour service (H2S cracking)",
            "Strength decreases significantly above 500°F",
            "Other materials (stainless, alloy steels) may have longer life"
        ],
        resolution_strategy="Specify impact testing for low-temperature service, use stainless or alloy for corrosive/sour service, add adequate CA, consider cladding for corrosion, use creep-resistant steel above 650°F",
        entity_scope="General-purpose pressure vessels in moderate service conditions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard applications, moderate for borderline temperature/corrosion cases",
        controlling_precedent="SA-516 Gr 70 is the industry default for carbon steel pressure vessels",
        category=IssueCategory.MATERIAL_SELECTION
    ),

    DoctrineBlock(
        topic="Stainless Steel SA-240 Type 304/316 for Pressure Vessels",
        keywords=["SA-240", "stainless steel", "304", "316", "corrosion resistant"],
        conclusion_template=[
            "SA-240 austenitic stainless steel (304, 316) provides excellent corrosion resistance.",
            "Type 316 has molybdenum for superior pitting/crevice corrosion resistance.",
            "Higher cost than carbon steel, but lower corrosion allowance and longer life."
        ],
        reasoning_framework="""
ASME SA-240 Stainless Steel Plate for Pressure Vessels:

Common grades:
- Type 304 (S30400): 18% Cr, 8% Ni - general corrosion resistance
- Type 304L (S30403): low carbon (0.03% max) - improved weld corrosion resistance
- Type 316 (S31600): 18% Cr, 10% Ni, 2% Mo - superior to 304 in chloride environments
- Type 316L (S31603): low carbon 316 - best weld corrosion resistance

Mechanical properties (Type 304):
- Tensile strength: 75 ksi minimum
- Yield strength: 30 ksi minimum
- Elongation: 40% minimum (very ductile)

Allowable stress (Type 304, 304L):
- At ambient: 20,000 psi (for t ≤ 5")
- Remains high at elevated temperature: 15,700 psi @ 600°F
- Can be used to 1500°F (creep becomes limiting above 1000°F)

Type 316 advantages over 304:
- Molybdenum improves resistance to pitting and crevice corrosion
- Better performance in chloride-containing environments (seawater, brines)
- Slightly higher strength and creep resistance
- About 20% higher material cost

Corrosion resistance:
- Excellent in atmospheric exposure (minimal corrosion allowance needed)
- Resistant to many chemicals, organic acids, food products
- Susceptible to chloride stress corrosion cracking above ~150°F (316 more resistant than 304)
- Susceptible to pitting in stagnant chloride solutions (316 superior to 304)

Fabrication considerations:
- Excellent weldability (no preheat or PWHT required)
- Work-hardens rapidly (difficult to cold form, machine)
- Low carbon grades (304L, 316L) prevent carbide precipitation in weld HAZ
- Electropolishing improves corrosion resistance for sanitary applications

Surface finish:
- 2B finish (mill finish) standard for vessels
- Electropolished or passivated for pharmaceutical, food, sanitary service
- Pickled and passivated to restore corrosion resistance after welding

Applications:
- Food and pharmaceutical processing vessels
- Chemical processing (acids, organic chemicals)
- Cryogenic service (excellent low-temperature toughness)
- High-purity or clean service (semiconductor, biotech)
        """,
        key_factors=[
            "Grade selection: 304 vs 316 based on corrosive environment",
            "Low carbon grades (L) for welded construction",
            "Allowable stress for thin vs thick sections",
            "Chloride SCC risk above 150°F (material, temperature, stress)",
            "Corrosion allowance (minimal or zero for most applications)",
            "Surface finish requirements for service",
            "Passivation after fabrication",
            "Cost premium vs carbon steel (2-3x material cost)"
        ],
        primary_authority=[
            "ASME SA-240 material specification",
            "ASME Section II Part D Table 1A (allowable stress)",
            "ASME VIII-1 UHA (high-alloy steels)",
            "NACE MR0175/ISO 15156 (sour service, if applicable)"
        ],
        burden_holder="Designer must justify stainless steel selection based on corrosion environment and economics",
        adversary_position="Stainless steel cost premium may not be justified if carbon steel with coating performs adequately",
        counter_arguments=[
            "2-3x cost of carbon steel (material + fabrication)",
            "Chloride SCC risk in certain environments",
            "Galling during assembly/disassembly (need anti-seize)",
            "Thermal expansion higher than carbon steel (expansion joint design)",
            "Magnetic permeability may be concern for some applications"
        ],
        resolution_strategy="Use carbon steel with lining if economics favor, select 316 over 304 for chloride exposure, stress-relieve if SCC risk, specify passivation, evaluate total lifecycle cost",
        entity_scope="Corrosive service vessels, food/pharma, cryogenic, high-purity applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for corrosion resistance, moderate for SCC risk assessment",
        controlling_precedent="SA-240 304/316 are industry standards for corrosion-resistant pressure vessels",
        category=IssueCategory.MATERIAL_SELECTION
    ),

    DoctrineBlock(
        topic="Post-Weld Heat Treatment (PWHT) Requirements",
        keywords=["PWHT", "post-weld heat treatment", "stress relief", "UCS-56", "thermal treatment"],
        conclusion_template=[
            "PWHT is required per ASME VIII-1 UCS-56 for carbon steel vessels based on thickness and material.",
            "Purpose: reduce residual stress, improve toughness, temper weld microstructure.",
            "Typical cycle: heat to 1100-1200°F, hold 1 hr per inch of thickness, slow cool."
        ],
        reasoning_framework="""
ASME VIII-1 UCS-56 Post-Weld Heat Treatment Requirements:

Mandatory PWHT for carbon steel (P-No. 1 materials like SA-516):
- Nominal thickness > 1.25" (any weld)
- Nominal thickness ≤ 1.25": PWHT not required (but may be beneficial)

PWHT exemptions (even if t > 1.25"):
- Vessels not subject to Code PWHT if constructed entirely of P-No. 1 Gr 1 or 2 and:
  - All welds made with low-hydrogen process (E7018 or better)
  - Preheat per UCS-79 is used
  - May still require Owner specification or jurisdictional requirement

PWHT procedure (UCS-56):
- Holding temperature: 1100°F minimum (typically 1150°F for SA-516)
- Heating rate: not to exceed 400°F/hr divided by maximum metal thickness in inches (slower for thick sections)
- Holding time: 1 hour per inch of thickness (minimum 30 min, maximum not specified)
- Cooling rate: ≤ 500°F/hr down to 600°F (then air cool)

Furnace PWHT:
- Preferred method: entire vessel in furnace with controlled atmosphere
- Temperature uniformity within ±25°F in heating zone
- Multiple thermocouples to monitor temperature distribution

Local PWHT:
- Permitted for repairs or when full furnace treatment impractical
- Heated band width: 3 * thickness on each side of weld (minimum 3" each side)
- Thermal gradients controlled to prevent distortion
- May not be as effective as furnace PWHT

Benefits of PWHT:
- Reduces residual stresses from welding (by 80-90%)
- Tempers hard martensite in weld HAZ (improves toughness, ductility)
- Reduces susceptibility to brittle fracture
- Improves resistance to stress corrosion cracking
- Dimensional stability (relieves stresses that could cause distortion)

Timing of PWHT:
- Must be done BEFORE hydrostatic test
- Should be done after all welding complete (avoid re-heat cycles)
- If multiple PWHT cycles required, subsequent cycles may not be as effective

Non-ferrous and stainless steels:
- Austenitic stainless (304, 316): PWHT not required (may be detrimental - sensitization)
- High-alloy materials: per UHA - generally no PWHT unless specified
        """,
        key_factors=[
            "Material P-Number and thickness trigger requirements",
            "Holding temperature and time based on thickness",
            "Heating and cooling rate limits to prevent distortion",
            "Furnace vs local PWHT (furnace preferred)",
            "Temperature monitoring and documentation",
            "Exemptions for low-hydrogen electrodes with preheat",
            "Timing (before hydrostatic test)",
            "Effects on material properties (may reduce hardness slightly)"
        ],
        primary_authority=[
            "ASME VIII-1 UCS-56 (PWHT requirements for carbon steel)",
            "ASME VIII-1 UW-40 (PWHT procedures)",
            "ASME VIII-1 UCS-85 (impact testing after PWHT)",
            "AWS D1.1 (supplemental welding requirements)"
        ],
        burden_holder="Manufacturer must perform and document PWHT per Code requirements",
        adversary_position="PWHT adds cost and schedule, and some argue modern welding practices reduce need",
        counter_arguments=[
            "Modern low-hydrogen electrodes may make PWHT less critical",
            "PWHT furnace cost and availability may be prohibitive",
            "Local PWHT is less effective than furnace treatment",
            "Distortion risk during thermal cycle",
            "May reduce hardness below desired level for wear resistance"
        ],
        resolution_strategy="Follow Code requirements strictly (liability issue), use furnace PWHT when possible, document temperature charts, perform hardness testing after PWHT if critical",
        entity_scope="Carbon steel pressure vessels with thickness > 1.25 inches per Code",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence that PWHT improves vessel integrity when properly done",
        controlling_precedent="ASME VIII-1 UCS-56 is mandatory for Code compliance",
        category=IssueCategory.FABRICATION
    ),

    DoctrineBlock(
        topic="Non-Destructive Examination (NDE) Requirements",
        keywords=["NDE", "radiography", "RT", "ultrasonic", "UT", "liquid penetrant", "magnetic particle"],
        conclusion_template=[
            "ASME VIII-1 requires NDE of welded joints based on joint category and required joint efficiency.",
            "Full radiography (RT) provides E=1.0, spot RT provides E=0.85, no RT limits to E=0.70.",
            "Other NDE methods (UT, MT, PT) supplement or substitute for RT in certain applications."
        ],
        reasoning_framework="""
ASME VIII-1 NDE requirements (UW-11, UW-51, UW-52):

Radiographic Examination (RT):
- Full RT: 100% of joint length examined, E = 1.0
- Spot RT: periodic examination per UW-52, E = 0.85
- No RT: visual examination only, E = 0.70 (max vessel thickness limits apply)

Joint categories (UW-3):
- Category A: longitudinal joints in shell/heads, full pressure stress
- Category B: circumferential joints in shell/heads
- Category C: ligaments between openings, nozzle-to-shell joints
- Category D: welded connections not subject to primary stress

RT extent by category and service:
- Lethal service: full RT required (all categories)
- Unfired steam boilers >50 psig: full RT required
- Category A joints: RT per Table UW-12 (depends on service, thickness)
- Category B,C,D: spot RT or visual (except lethal service)

Ultrasonic Examination (UT):
- Alternative to RT for thick sections (> 2")
- ASME Section V Article 5 governs UT procedures
- May be more sensitive than RT for certain defects (laminations, lack of fusion)
- Requires skilled technician and calibration blocks

Magnetic Particle Testing (MT):
- Surface and near-surface discontinuities in ferromagnetic materials
- Required for some nozzle attachment welds
- ASME Section V Article 7 procedures

Liquid Penetrant Testing (PT):
- Surface discontinuities in non-magnetic materials (stainless steel, aluminum)
- Required for some nozzle attachment welds on austenitic stainless
- ASME Section V Article 6 procedures

Visual Examination (VT):
- Required for ALL welds (supplement to other NDE)
- Weld profile, size, reinforcement, undercut, porosity assessment
- QC Inspector qualified per SNT-TC-1A or equivalent

NDE acceptance criteria:
- RT: per ASME Section VIII-1 Appendix 4 (rounded indications, elongated indications, slag)
- UT: per ASME Section V and vessel specification
- MT/PT: no relevant indications (cracks, lack of fusion) permitted

Documentation:
- RT films retained by Manufacturer for life of vessel (or min 5 years)
- UT, MT, PT reports retained per QC program
- NDE must be performed by certified technicians (ASNT Level II minimum)
        """,
        key_factors=[
            "Joint category determines RT requirements",
            "Service (lethal vs non-lethal) affects extent",
            "Joint efficiency desired (E = 0.7, 0.85, 1.0) drives RT extent",
            "Full vs spot RT cost and schedule impact",
            "UT suitability for thick sections or inaccessible joints",
            "MT/PT for surface crack detection on critical welds",
            "NDE timing (after welding, before PWHT for some methods)",
            "Technician certification and procedure qualification"
        ],
        primary_authority=[
            "ASME VIII-1 UW-11 (RT requirements by joint category)",
            "ASME VIII-1 UW-51, UW-52 (extent of RT, spot RT)",
            "ASME Section V (NDE methods and acceptance)",
            "ASME VIII-1 Appendix 4 (RT acceptance standards)",
            "SNT-TC-1A (NDE technician qualification)"
        ],
        burden_holder="Manufacturer must perform NDE per Code and provide documentation to Inspector",
        adversary_position="NDE is expensive and may delay project, some argue excessive for low-risk vessels",
        counter_arguments=[
            "RT doesn't detect all defect types (laminations, lack of fusion parallel to beam)",
            "UT is operator-dependent (skill variation)",
            "Spot RT may miss defects between examination locations",
            "Surface NDE (MT/PT) doesn't detect subsurface defects",
            "Cost of full RT can be 10-20% of vessel fabrication cost"
        ],
        resolution_strategy="Specify full RT for critical vessels (E=1.0 reduces thickness), use UT for thick sections, combine methods (RT + UT) for high-consequence vessels, invest in skilled NDE technicians",
        entity_scope="All ASME Code welded pressure vessels based on joint category and service",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence that proper NDE detects fabrication defects",
        controlling_precedent="ASME VIII-1 UW-11, UW-51 mandatory for Code compliance",
        category=IssueCategory.TESTING_NDE
    ),

    DoctrineBlock(
        topic="API 510 In-Service Inspection and Remaining Life Assessment",
        keywords=["API 510", "in-service inspection", "remaining life", "fitness for service", "thickness testing"],
        conclusion_template=[
            "API 510 governs inspection, repair, and alteration of pressure vessels in service.",
            "Remaining life calculated based on actual thickness, corrosion rate, and retirement thickness.",
            "Inspection intervals based on remaining life and consequence of failure."
        ],
        reasoning_framework="""
API 510 Pressure Vessel Inspection Code:

Purpose:
- Maintain safety and integrity of in-service pressure vessels
- Determine inspection intervals and methods
- Calculate remaining life and fitness for service
- Guide repair and alteration activities

Remaining life calculation:
Remaining Life (years) = (Actual Thickness - Retirement Thickness) / Corrosion Rate

Where:
- Actual Thickness = current measured thickness (UT or RT)
- Retirement Thickness = minimum thickness for MAWP + CA
- Corrosion Rate = thickness loss per year (from inspection history)

Example:
- Original thickness: 0.500"
- Current thickness: 0.425" (measured after 10 years)
- Retirement thickness: 0.375" (calculated per UG-27 + CA)
- Corrosion rate: (0.500 - 0.425) / 10 = 0.0075 in/yr
- Remaining life: (0.425 - 0.375) / 0.0075 = 6.7 years

Inspection intervals:
- Based on remaining life and risk category
- Typical: 50% of remaining life, or 10 years, whichever is less
- High-risk vessels: more frequent (25% of remaining life)
- Low-risk vessels: may extend to 15 years

Inspection methods:
- External visual (every interval)
- Internal visual (if accessible)
- Ultrasonic thickness testing (UT) at critical locations
- Radiography (RT) if internal UT not possible
- Pressure testing if required by jurisdiction or after repair

Critical Thickness Locations (CTLs):
- Areas with highest corrosion rate or stress
- Nozzles, attachments, weld joints
- Bottom of vertical vessels (water accumulation)
- Areas of turbulence or impingement

Re-rating vessels:
- If thickness < design minimum, calculate new MAWP
- May de-rate vessel to lower pressure
- Must update nameplate if MAWP changed
- Requires recalculation per original Code of construction

Repair vs replacement:
- Repair if remaining life > 5 years (rule of thumb)
- Replace if extensive corrosion or multiple defects
- Economic analysis: repair cost vs new vessel cost

Documentation:
- Inspection reports with thickness data and charts
- Remaining life calculations
- Repairs performed
- Alterations and re-rating calculations
- Owner/User inspection program per API 510
        """,
        key_factors=[
            "Thickness testing locations and frequency",
            "Corrosion rate determination (short-term vs long-term)",
            "Retirement thickness calculation (Code formula + CA)",
            "Remaining life and next inspection interval",
            "Risk-based inspection (RBI) to optimize intervals",
            "Re-rating calculations if thickness below design",
            "Repair procedures per ASME VIII-1 or NBR (National Board)",
            "Jurisdictional requirements (some states have specific rules)"
        ],
        primary_authority=[
            "API 510 Pressure Vessel Inspection Code",
            "ASME VIII-1 (original Code of construction for calculations)",
            "API 579-1/ASME FFS-1 (Fitness for Service assessment)",
            "National Board Inspection Code (NBIC) for repairs"
        ],
        burden_holder="Owner/User must maintain inspection program and ensure vessel fitness for service",
        adversary_position="Remaining life calculations are estimates and actual corrosion may accelerate unexpectedly",
        counter_arguments=[
            "Corrosion rate may not be constant (can accelerate)",
            "Localized corrosion (pitting) may not be detected by UT",
            "Process changes can alter corrosion environment",
            "External corrosion under insulation (CUI) may go undetected",
            "Thickness readings have measurement uncertainty (±0.005 to 0.010)"
        ],
        resolution_strategy="Conservative corrosion rate assumptions, frequent inspection of high-risk areas, use RBI methods, CUI inspection programs, online monitoring if available",
        entity_scope="All in-service ASME pressure vessels requiring periodic inspection",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence - remaining life is an estimate based on historical data",
        controlling_precedent="API 510 is widely adopted and required by many jurisdictions",
        category=IssueCategory.IN_SERVICE
    ),

    DoctrineBlock(
        topic="Fitness-for-Service Assessment per API 579-1/ASME FFS-1",
        keywords=["fitness for service", "FFS", "API 579", "ASME FFS-1", "flaw assessment", "local thin area"],
        conclusion_template=[
            "API 579-1/ASME FFS-1 provides methodology to assess fitness of degraded vessels.",
            "Covers local thin areas, cracks, dents, corrosion, laminations, and other damage mechanisms.",
            "Three assessment levels: Level 1 (conservative), Level 2 (detailed), Level 3 (FEA/testing)."
        ],
        reasoning_framework="""
API 579-1/ASME FFS-1 Fitness-for-Service Standard:

Purpose:
- Determine if degraded vessel can safely continue operation
- Provide remaining life estimates for damaged equipment
- Guide repair-vs-continue-operation decisions
- Cover damage types not addressed by original design codes

Damage mechanisms covered:
- Part 4: Local Thin Areas (LTA) - corrosion, erosion
- Part 5: Local Metal Loss (LML) - general corrosion over large area
- Part 6: Pitting Corrosion
- Part 7: Blisters and Laminations
- Part 8: Weld Misalignment and Shell Distortions
- Part 9: Crack-like Flaws
- Part 10: Creep Damage
- Part 11: Fire Damage
- Part 12: Dents, Gouges, Dent-Gouge Combinations

Three-tiered assessment approach:
Level 1: Conservative, rules-based, minimal data required
Level 2: Detailed analysis using measured dimensions
Level 3: Advanced methods (FEA, fracture mechanics, testing)

Example: Local Thin Area (LTA) Assessment:
Level 1:
- Remaining thickness factor (Rt) = tmin / trd
- If Rt ≥ 0.9 → acceptable
- If Rt < 0.9 → go to Level 2

Level 2:
- Calculate MAWP based on actual tmin, length, and width of LTA
- Use chart-based methods or equations from Part 4
- If MAWP_LTA ≥ operating pressure → acceptable

Level 3:
- FEA of vessel with LTA to determine stress distribution
- Plastic collapse analysis or limit load calculation
- More accurate but requires expertise and software

Crack assessment (Part 9):
- Crack length, depth, orientation measured
- Fracture mechanics (stress intensity factor K)
- Compare K to material toughness (KIc or Kmat)
- Determine remaining life based on crack growth rate

Remaining life for LTA:
- Similar to API 510 approach
- Account for shape and size of LTA (stress concentration)
- May be less than uniform thickness remaining life

Acceptance criteria:
- MAWP of degraded area ≥ operating pressure (with safety factor)
- Stress in degraded area ≤ allowable (may use higher allowables than design)
- Brittle fracture resistance adequate (toughness requirements)

Documentation:
- FFS assessment report required
- Calculations, measurements, assumptions
- Recommendations (operate, repair, monitor, replace)
- Re-inspection interval
        """,
        key_factors=[
            "Type and extent of damage (LTA, crack, dent, etc.)",
            "Measured dimensions (thickness, length, width, depth)",
            "Operating pressure and temperature",
            "Material properties (strength, toughness)",
            "Assessment level (1, 2, or 3) based on complexity",
            "Remaining life calculation for continuing damage",
            "Monitoring plan and re-inspection interval",
            "Economic comparison: FFS vs repair vs replace"
        ],
        primary_authority=[
            "API 579-1/ASME FFS-1 (Fitness-for-Service standard)",
            "ASME VIII-1 or VIII-2 (original design code for reference)",
            "API 510 (in-service inspection procedures)",
            "ASME Section XI (for nuclear, similar approach)"
        ],
        burden_holder="Owner/User must perform or contract FFS assessment and document results",
        adversary_position="FFS assessments may be optimistic, allowing continued operation of questionable equipment",
        counter_arguments=[
            "Level 1 may be overly conservative, leading to unnecessary repairs",
            "Level 3 requires expensive FEA and expert analysts",
            "Assumptions about corrosion rate or crack growth may be wrong",
            "Measurement uncertainty in damage dimensions affects results",
            "Pressure testing to validate FFS may not be practical"
        ],
        resolution_strategy="Use conservative assumptions, validate with pressure test if possible, frequent re-inspection if accepting degraded condition, independent review of Level 3 assessments",
        entity_scope="In-service pressure vessels with damage or degradation beyond design basis",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence - FFS allows continued operation but requires careful analysis",
        controlling_precedent="API 579-1/ASME FFS-1 is recognized standard for fitness-for-service",
        category=IssueCategory.FITNESS_FOR_SERVICE
    ),

    DoctrineBlock(
        topic="Oilfield Production Vessels per API 12F and 12J",
        keywords=["API 12F", "API 12J", "production separator", "oil and gas separator", "oilfield vessel"],
        conclusion_template=[
            "API 12F and 12J govern design and fabrication of shop-welded oilfield production vessels.",
            "API 12F for vessels ≤ 15 psig, API 12J for > 15 psig (overlaps with ASME VIII-1).",
            "Less stringent than ASME but widely used for non-jurisdictional oilfield applications."
        ],
        reasoning_framework="""
API 12F and 12J Standards for Oilfield Production Vessels:

API 12F (Stock Tanks and Production Vessels ≤ 15 psig):
- Covers atmospheric and low-pressure storage tanks and vessels
- Design pressure: 0.5 psig to 15 psig
- Common applications: oil storage tanks, gun barrels, wash tanks, heater-treaters
- Shell thickness based on hydrostatic head (not pressure stress)
- Minimum thickness: typically 3/16" for small tanks, 1/4" for large
- No RT or NDE required (visual inspection only)
- No U-stamp required (non-ASME Code vessel)

API 12J (Oil and Gas Separators > 15 psig):
- Covers higher-pressure production separators
- Design pressure: > 15 psig (typically 50-1500 psig for oilfield)
- Common applications: vertical and horizontal separators, scrubbers, treaters
- Design may follow ASME VIII-1 formulas OR API 12J simplified rules
- Shell thickness: may use API 12J tables or ASME calculation
- Full RT not required (spot RT optional)
- No U-stamp typically (unless Owner specifies ASME Code construction)

Comparison to ASME VIII-1:
- API 12J is less rigorous (lower QC, less NDE, no stamp)
- API 12J may allow thinner shells for same pressure (less conservative factors)
- ASME VIII-1 required if:
  - Jurisdictional (state requires Code vessels)
  - Lethal service
  - Owner specifies Code construction
  - Pressure > 3000 psi (API 12J not applicable)

Typical API 12J separator design:
- Horizontal or vertical cylindrical vessel
- 2:1 ellipsoidal or hemispherical heads
- Nozzles for inlet, gas outlet, oil outlet, water outlet
- Internal baffles, mist eliminators, weirs
- Saddle or leg supports
- Relief valve per API 520/521

Advantages of API 12J:
- Lower cost (no Code fees, less NDE, simpler QC)
- Faster fabrication (no AI inspection, no stamp)
- Adequate for oilfield production (proven track record)

Disadvantages of API 12J:
- Not acceptable in ASME jurisdictions (most U.S. states)
- No third-party design review (higher risk)
- Lower resale value (buyers may prefer Code vessels)
- Less rigorous NDE (potential hidden defects)

API 12K:
- Specifies production tanks for oil production
- Atmospheric pressure, bolted construction
        """,
        key_factors=[
            "Pressure level (15 psig is dividing line between 12F and 12J)",
            "Jurisdictional requirements (ASME Code may be mandatory)",
            "Service (oil, gas, water, or multiphase)",
            "Design approach (ASME formulas vs API 12J tables)",
            "NDE extent (visual only vs spot RT)",
            "Certification and stamping requirements",
            "Internal components (baffles, weirs, mist pads)",
            "Relief valve sizing per API 520/521"
        ],
        primary_authority=[
            "API Spec 12F (Stock Tanks and Production Vessels)",
            "API Spec 12J (Oil and Gas Separators)",
            "API RP 520 (Sizing of Pressure Relief Devices)",
            "API Std 521 (Guide for Pressure Relief and Depressuring)"
        ],
        burden_holder="Manufacturer must comply with API 12F/12J requirements and Owner specifications",
        adversary_position="API 12F/12J vessels lack third-party oversight and may not meet Code safety margins",
        counter_arguments=[
            "Less rigorous QC and NDE than ASME Code",
            "No Authorized Inspector oversight",
            "May not be legal in jurisdictions requiring Code vessels",
            "Resale value lower than Code-stamped vessels",
            "Insurance may require ASME Code vessels"
        ],
        resolution_strategy="Use ASME VIII-1 for jurisdictional installations, API 12J for remote non-jurisdictional sites, verify local regulations, consider life-cycle cost including resale",
        entity_scope="Oilfield production separators, treaters, storage tanks in non-jurisdictional areas",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence - API 12F/12J widely used but less conservative than ASME",
        controlling_precedent="API 12F/12J are industry standards for oilfield production equipment",
        category=IssueCategory.OILFIELD_PRODUCTION
    ),

    DoctrineBlock(
        topic="Wind and Seismic Loads per ASCE 7",
        keywords=["wind load", "seismic load", "ASCE 7", "earthquake", "lateral load"],
        conclusion_template=[
            "Pressure vessels exposed to wind and seismic loads must be designed per ASCE 7.",
            "Wind pressure depends on wind speed, exposure category, and vessel geometry.",
            "Seismic loads depend on seismic zone, soil type, and importance factor."
        ],
        reasoning_framework="""
ASCE 7 Minimum Design Loads for Buildings and Other Structures:

Wind loads (ASCE 7 Chapter 29):
Design wind pressure: p = qz * G * Cp
Where:
- qz = velocity pressure at height z = 0.00256 * Kz * Kzt * Kd * V^2
- V = basic wind speed (mph) from ASCE 7 maps (3-sec gust, 50-year return)
- Kz = velocity pressure exposure coefficient (depends on height and terrain)
- Kzt = topographic factor (typically 1.0)
- Kd = directionality factor (typically 0.95)
- G = gust effect factor (typically 0.85 for rigid structures)
- Cp = pressure coefficient (depends on shape: cylinder ≈ 0.7-0.9)

For cylindrical vessel:
- Windward pressure: positive (+) pushing on cylinder
- Leeward pressure: negative (-) suction on back side
- Net force = pressure × projected area

Typical wind design:
- 90 mph wind → qz ≈ 20 psf → p ≈ 15 psf on cylinder
- For D=10 ft, H=50 ft vessel → Force ≈ 7,500 lb
- Creates overturning moment at base → anchor bolt design

Seismic loads (ASCE 7 Chapter 15):
Seismic base shear: V = Cs * W
Where:
- Cs = seismic response coefficient = SDS / (R/I)
- SDS = design spectral acceleration (from ASCE 7 maps, function of location and soil)
- R = response modification factor (≈ 3 for vessels on braced frames)
- I = importance factor (1.0 for normal, 1.5 for hazardous contents)
- W = operating weight of vessel + contents

Typical seismic design:
- SDS = 0.5g (moderate seismic zone)
- R = 3, I = 1.5 → Cs = 0.25
- Vessel weight 50,000 lb → V = 12,500 lb lateral force
- Applied at center of gravity → overturning moment

Support design for wind/seismic:
- Anchor bolts: tension due to overturning + shear
- Base plate: bending from bolt forces
- Skirt or legs: compression + bending
- Foundation: overturning stability (factor of safety ≥ 1.5)

Combination with pressure loads:
- Pressure creates hoop and longitudinal stress in shell
- Wind/seismic creates bending stress
- Combined stress must be within allowables (ASME or AISC)

Tall vessels (H/D > 5):
- More sensitive to wind/seismic (higher moments)
- May require bracing or guy wires
- Sloshing of liquid contents can amplify seismic response

Special considerations:
- Insulated vessels: wind area increases due to insulation jacket
- Piping loads: connected piping can impose additional lateral loads
- Operating vs empty condition: worst case governs
        """,
        key_factors=[
            "Basic wind speed for site location (ASCE 7 maps)",
            "Exposure category (open terrain vs urban)",
            "Seismic design category and spectral accelerations",
            "Importance factor based on contents (hazardous = 1.5)",
            "Operating weight and center of gravity",
            "Vessel height-to-diameter ratio (slenderness)",
            "Support type (skirt, legs, saddles) and anchor bolt design",
            "Foundation design for overturning and sliding"
        ],
        primary_authority=[
            "ASCE 7 Minimum Design Loads (wind and seismic)",
            "AISC 360 (steel design for supports)",
            "ACI 318 (concrete foundation design)",
            "ASME VIII-1 (pressure vessel shell design)"
        ],
        burden_holder="Designer must include wind/seismic loads in vessel and support design",
        adversary_position="Wind/seismic loads may be underestimated or neglected in non-structural engineer designs",
        counter_arguments=[
            "ASCE 7 maps are probabilistic (actual wind/seismic may exceed design)",
            "Vessel interaction with structure (stiffness, damping) is complex",
            "Sloshing effects in partially-filled vessels not addressed by simple analysis",
            "Piping loads can be significant but often not included in design",
            "Climate change may increase wind speeds beyond historical data"
        ],
        resolution_strategy="Use site-specific wind/seismic studies for critical vessels, conservatively estimate operating weight, include piping loads, FEA for complex support systems, engage structural engineer",
        entity_scope="Outdoor pressure vessels, tall vessels (H/D > 5), vessels in high wind or seismic zones",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard designs, moderate for complex geometry or extreme loads",
        controlling_precedent="ASCE 7 is the U.S. standard for wind and seismic loads on structures",
        category=IssueCategory.SUPPORT_DESIGN
    ),

    DoctrineBlock(
        topic="National Board Registration and R-Stamp",
        keywords=["National Board", "NB registration", "R-stamp", "repair", "alteration", "rerating"],
        conclusion_template=[
            "National Board registration provides permanent vessel record and enables tracking through vessel life.",
            "R-stamp is required for repairs and alterations to Code vessels (National Board Inspection Code).",
            "Registration is optional but recommended for resale value and repair tracking."
        ],
        reasoning_framework="""
National Board of Boiler and Pressure Vessel Inspectors:

National Board Registration:
- Voluntary program for ASME Code vessels
- Vessel assigned unique NB number (e.g., NB-12345)
- Number stamped on nameplate along with U-stamp
- Vessel data entered into National Board database
- Permanent record of original design and construction

Benefits of NB registration:
- Proof of Code compliance for jurisdictional inspections
- Facilitates repairs (repair org can look up original design)
- Increases resale value (buyers prefer registered vessels)
- Required by some jurisdictions or insurance companies
- Enables tracking of repairs and alterations

Registration process:
1. Manufacturer completes Form NB-1 (vessel data report)
2. Submit to National Board with registration fee
3. National Board issues NB number
4. Manufacturer stamps NB number on nameplate

R-Stamp (Repair Authorization):
- National Board Inspection Code (NBIC) Part 2 governs repairs
- Organizations must obtain NB "R" Certificate of Authorization
- R-stamp denotes repair performed per NBIC
- Required for pressure-retaining repairs on Code vessels in many jurisdictions

Repair vs alteration:
- Repair: restore vessel to original design condition (crack repair, corroded area replacement)
- Alteration: change vessel design (add nozzle, increase MAWP, change MDMT)

R-stamp repair procedure:
1. Owner requests repair from R-stamp holder
2. R-stamp holder prepares repair documentation (drawing, procedure, WPS)
3. Authorized Inspector reviews and approves repair plan
4. Repair performed per approved procedure
5. NDE and pressure test per NBIC
6. Inspector witnesses and signs Form R-1 (repair report)
7. R-stamp applied to vessel near repair

Re-rating and VR-stamp:
- If vessel MAWP changed, requires VR-stamp (Verify and Re-rate)
- VR-stamp holder recalculates MAWP based on current Code
- New nameplate affixed with updated MAWP
- Form VR-1 submitted to National Board

Common repairs requiring R-stamp:
- Nozzle additions or replacements
- Shell or head patch plates
- Weld crack repairs
- Thickness restoration (weld buildup)
- Internal lining or cladding

Jurisdictional variations:
- Some states require R-stamp for any pressure-retaining repair
- Some allow Owner/User to perform minor repairs without R-stamp
- Some do not recognize NBIC (rely on ASME VIII-1 only)
        """,
        key_factors=[
            "NB registration status (registered vs non-registered)",
            "NB number stamped on nameplate (if registered)",
            "Repair organization R-stamp certificate",
            "Authorized Inspector involvement in repair",
            "Repair documentation (R-1 form, drawings, procedures)",
            "NDE and testing after repair per NBIC",
            "Re-rating if MAWP changed (VR-stamp)",
            "Jurisdictional requirements for repairs"
        ],
        primary_authority=[
            "National Board Inspection Code (NBIC) Part 2 (Repairs)",
            "National Board Inspection Code (NBIC) Part 3 (Alterations)",
            "ASME VIII-1 (original design code for reference)",
            "State/Provincial jurisdictional rules"
        ],
        burden_holder="Repair organization must hold R-stamp and follow NBIC procedures",
        adversary_position="NB registration and R-stamp requirements add cost and may delay repairs",
        counter_arguments=[
            "Non-registered vessels can be repaired without R-stamp in some jurisdictions",
            "R-stamp process adds cost (inspector fees, documentation)",
            "Some owners bypass NBIC and repair without stamps (illegal in many states)",
            "VR-stamp re-rating may reveal vessel no longer meets current Code",
            "NB database does not include all repair history (only R-stamped repairs)"
        ],
        resolution_strategy="Register new vessels with NB for long-term value, use R-stamp holders for all repairs, maintain repair records even if not R-stamped, verify jurisdictional requirements",
        entity_scope="ASME Code pressure vessels requiring repair, alteration, or re-rating",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - NB registration and R-stamp are well-established systems",
        controlling_precedent="National Board Inspection Code (NBIC) is adopted by most U.S. jurisdictions",
        category=IssueCategory.REGISTRATION
    ),

    DoctrineBlock(
        topic="Corrosion Allowance Selection and Design Life",
        keywords=["corrosion allowance", "CA", "design life", "service life", "corrosion rate"],
        conclusion_template=[
            "Corrosion allowance is additional thickness to account for metal loss during vessel service life.",
            "Common values: 1/8\" (non-corrosive), 1/4\" (moderate corrosion), 1/2\" (severe corrosion).",
            "Design life typically 15-25 years for process vessels, longer for storage tanks."
        ],
        reasoning_framework="""
Corrosion Allowance (CA) Design Philosophy:

Definition:
- CA = extra thickness added to calculated minimum thickness
- Accounts for general corrosion, erosion, and other metal loss mechanisms
- Not intended to address localized corrosion (pitting, crevice)

Design life calculation:
Design Life (years) = Corrosion Allowance / Corrosion Rate

Example:
- CA = 0.125" (1/8")
- Corrosion rate = 0.005 in/yr (5 mils per year)
- Design life = 0.125 / 0.005 = 25 years

Common CA values by service:
- Non-corrosive (clean water, air): 1/16" (0.0625")
- Mildly corrosive (produced water, sweet crude): 1/8" (0.125")
- Moderately corrosive (sour gas, brine): 1/4" (0.250")
- Severely corrosive (acids, high H2S): 1/2" (0.500") or use corrosion-resistant alloy

Corrosion rate estimation methods:
1. Industry experience / historical data (most common)
2. Laboratory testing (corrosion coupons in simulated service)
3. Calculation (NACE equations for CO2, H2S corrosion)
4. Conservative assumption (0.010 in/yr if unknown)

Factors affecting corrosion rate:
- Fluid chemistry (pH, chlorides, CO2, H2S, O2)
- Temperature (corrosion typically increases with temperature)
- Flow velocity (erosion-corrosion above 10 ft/s)
- Presence of solids (sand, scale → erosion)
- Microbiological activity (MIC - microbiologically influenced corrosion)

Internal vs external CA:
- Internal CA: based on process fluid corrosivity
- External CA: atmospheric corrosion (typically 0" if coated/painted)
- For jacketed vessels: external CA may be needed for jacket side

CA on different components:
- Shell and heads: full CA
- Nozzle necks: typically 1/2 of shell CA (less exposure)
- Internal components (baffles): may not need CA if replaceable

Minimum thickness after CA:
- Original thickness = calculated + CA
- Retirement thickness = calculated (or slightly higher for safety)
- MAWP calculated using retirement thickness

Zero CA option:
- Use corrosion-resistant material (stainless steel, alloy)
- Use internal lining (rubber, glass, polymer)
- Cathodic protection for external surfaces
- Coatings (paint, epoxy) with maintenance program

CA and inspection:
- Thickness testing during in-service inspection tracks actual corrosion
- If actual < assumed rate → extend life
- If actual > assumed rate → increase inspection frequency or re-rate

Economic optimization:
- Larger CA → higher initial cost, lower lifecycle cost (longer life)
- Smaller CA → lower initial cost, more frequent replacement
- Break-even analysis based on vessel cost, installation cost, downtime cost
        """,
        key_factors=[
            "Corrosion rate estimation method and accuracy",
            "Desired design life (15-25 years typical)",
            "Process fluid corrosivity (sweet vs sour, pH, chlorides)",
            "Temperature and flow velocity effects",
            "Alternative corrosion mitigation (coating, CRA, inhibitors)",
            "Internal vs external CA requirements",
            "In-service monitoring and re-rating plans",
            "Economic analysis of CA vs material upgrade"
        ],
        primary_authority=[
            "ASME VIII-1 UG-25 (corrosion allowance in design)",
            "NACE SP0106 (Control of Internal Corrosion in Steel Pipelines)",
            "API RP 571 (Damage Mechanisms in Refining)",
            "API RP 581 (Risk-Based Inspection)"
        ],
        burden_holder="Designer must specify appropriate CA based on service and desired life",
        adversary_position="Corrosion rate estimates are uncertain and actual corrosion may exceed design assumptions",
        counter_arguments=[
            "Corrosion rate can vary widely (localized corrosion not addressed)",
            "Process conditions may change (increase corrosivity)",
            "CA adds weight and cost (may be excessive for non-corrosive service)",
            "Coatings or inhibitors may provide better economics than thick CA",
            "Monitoring and maintenance may be more cost-effective than large CA"
        ],
        resolution_strategy="Use conservative CA for uncertain environments, validate with corrosion testing, implement monitoring program, consider material upgrade for severe service, perform economic analysis",
        entity_scope="All pressure vessels in corrosive service",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence - CA selection based on estimates and historical data",
        controlling_precedent="Industry practice varies, but 1/8\" CA is common baseline",
        category=IssueCategory.MATERIAL_SELECTION
    ),

    DoctrineBlock(
        topic="Minimum Design Metal Temperature (MDMT) and Impact Testing",
        keywords=["MDMT", "minimum design metal temperature", "impact testing", "brittle fracture", "Charpy"],
        conclusion_template=[
            "MDMT is the lowest temperature at which vessel can safely operate without risk of brittle fracture.",
            "Impact testing (Charpy V-notch) required below exemption curves in ASME VIII-1 UCS-66.",
            "Lower MDMT or thicker material typically requires impact testing for carbon steel."
        ],
        reasoning_framework="""
ASME VIII-1 UCS-66 MDMT and Impact Testing Requirements:

Purpose:
- Prevent brittle fracture at low temperatures
- Carbon steel ductility decreases at low temperature (ductile-to-brittle transition)
- Impact testing verifies adequate toughness at design temperature

MDMT definition:
- Minimum Design Metal Temperature
- Lowest temperature for metal in operating or test condition
- Specified on vessel nameplate
- Must consider:
  - Minimum process temperature
  - Atmospheric temperature for outdoor vessels
  - Autorefrigeration during depressuring
  - Hydrostatic test temperature

Impact test exemption curves (UCS-66):
- Curve A: Material not normalized, no PWHT (most restrictive)
- Curve B: Material normalized or PWHT applied
- Curve C: Material normalized AND PWHT applied (least restrictive)
- Curve D: Killed fine-grain steel (3:1 thickness ratio)

For a given thickness, curves define minimum temperature without impact testing.

Example (SA-516 Gr 70):
- Thickness = 1.0"
- Curve B (normalized or PWHT)
- Exemption temperature ≈ 0°F
- If MDMT < 0°F → impact testing required
- If MDMT ≥ 0°F → no impact testing needed

Impact test procedure (UCS-67):
- Charpy V-notch specimen (10mm x 10mm x 55mm)
- Three specimens tested at MDMT
- Minimum absorbed energy: 15 ft-lb average, 10 ft-lb individual (for 5/16" thick)
- Lateral expansion: 0.015" minimum average (additional toughness criterion)

Test temperature margin:
- Test at MDMT - 50°F if MDMT < room temperature (provides safety margin)
- Or test at MDMT if MDMT ≥ room temperature

Impact testing alternatives:
- Use material with inherent low-temperature toughness (ASTM A333, A350)
- Use austenitic stainless steel (no MDMT limit, ductile at cryogenic temperatures)
- Increase thickness to move into exemption zone
- Increase MDMT (change process or insulate)

PWHT effects on MDMT:
- PWHT improves toughness (tempering of weld HAZ)
- Allows use of Curve B or C (warmer exemption temperature)
- For thick vessels (> 1.25"), PWHT may be required anyway (UCS-56)

Hydrostatic test temperature:
- Test fluid temperature must be ≥ MDMT + 50°F (for carbon steel)
- Or test fluid temperature ≥ 60°F
- Purpose: avoid brittle fracture during test

Coincident ratio method (UCS-66(b)):
- For vessels operating above MDMT most of the time
- Allows reduction in impact test requirements
- Based on stress ratio and temperature ratio
        """,
        key_factors=[
            "Minimum operating temperature and atmospheric conditions",
            "Material specification and condition (normalized, PWHT)",
            "Vessel thickness (thicker = colder exemption temperature)",
            "Applicable exemption curve (A, B, C, or D)",
            "Impact test results (energy, lateral expansion)",
            "Hydrostatic test temperature coordination with MDMT",
            "Alternative materials for low-temperature service",
            "Coincident ratio if operating temperature varies"
        ],
        primary_authority=[
            "ASME VIII-1 UCS-66 (impact test exemption curves)",
            "ASME VIII-1 UCS-67 (Charpy impact test procedures)",
            "ASME VIII-1 UG-84 (test temperature requirements)",
            "ASME Section II Part A (material specifications with toughness)"
        ],
        burden_holder="Designer must specify MDMT and determine if impact testing is required",
        adversary_position="Impact test exemption curves are empirical and may not guarantee toughness in all cases",
        counter_arguments=[
            "Exemption curves are based on historical data (may be optimistic)",
            "Actual ductile-to-brittle transition varies by heat of material",
            "Weld heat-affected zone may have lower toughness than base metal",
            "Impact test specimens may not represent actual vessel behavior",
            "Some jurisdictions require impact testing regardless of exemption"
        ],
        resolution_strategy="Specify impact testing for critical low-temperature service, use normalized material or PWHT to improve exemption, add safety margin on MDMT, use inherently tough materials (stainless, fine-grain)",
        entity_scope="Carbon steel pressure vessels with MDMT below exemption curves",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - impact testing is proven method to verify toughness",
        controlling_precedent="ASME VIII-1 UCS-66 is mandatory for carbon steel low-temperature service",
        category=IssueCategory.MATERIAL_SELECTION
    ),

    DoctrineBlock(
        topic="Fabrication Tolerances per ASME VIII-1 UG-80 and UG-81",
        keywords=["fabrication tolerances", "out-of-roundness", "UG-80", "UG-81", "dimensional tolerances"],
        conclusion_template=[
            "ASME VIII-1 UG-80 and UG-81 specify permissible variations in vessel dimensions.",
            "Out-of-roundness of cylindrical shells limited to prevent stress concentration and buckling.",
            "Tolerances ensure vessel geometry matches design assumptions used in Code calculations."
        ],
        reasoning_framework="""
ASME VIII-1 Fabrication Tolerances:

UG-80 Cylindrical Shell Tolerances:
Out-of-roundness limit:
- Difference between maximum and minimum inside diameter measured at any cross-section
- Must not exceed 1% of nominal diameter
- For D = 100", max variation = 1.0"

Measurement:
- Use inside diameter caliper or template at multiple cross-sections
- Check near supports, heads, and nozzles (areas of constraint)

Causes of out-of-roundness:
- Shell rolling (springback, over-bending)
- Welding distortion (shrinkage)
- Support loads during fabrication
- Thermal distortion during PWHT

Effects of out-of-roundness:
- Increases local bending stress (higher stress at "flat" areas)
- Reduces buckling resistance under external pressure
- May affect nozzle fit-up and alignment
- Can cause vibration in service

Correction methods:
- Cold rolling or pressing to restore roundness
- Heat straightening (localized heating and quenching)
- Internal jacks or mandrels during welding
- Post-weld machining (for precision vessels)

UG-81 Formed Head Tolerances:
Out-of-roundness for dished heads:
- Similar 1% limit on diameter
- Additional limits on knuckle radius and crown radius

Depth tolerance for ellipsoidal heads:
- 2:1 ellipsoidal head: depth = D/4 ± 1.25%
- For 100" diameter: depth = 25" ± 0.31"

Crown radius tolerance:
- For 2:1 ellipsoidal: crown radius ≈ D ± specified tolerance
- Manufacturer must certify actual radii (affects stress calculation)

UG-79 Tolerance on Thickness:
Mill tolerance:
- Plate thickness typically +0.01", -0.00" (no undermeasure allowed)
- After forming: thinning at knuckle areas must be checked
- Minimum thickness after forming must meet design requirement

Weld reinforcement:
- External: not to exceed lesser of 1/4" or 1/4*t
- Internal: to be minimized (full penetration ground flush preferred)
- Excessive reinforcement is stress concentrator

Alignment tolerances (UW-33):
- Offset at longitudinal joints: ≤ 1/4*t (max 1/8")
- Offset at circumferential joints: ≤ 1/2*t (max 3/8")
- Excessive offset creates stress concentration

Nozzle projection:
- Nozzle necks must project adequately for full-penetration weld
- Typical: nozzle projects 1/8" to 1/4" proud of shell ID
- Allows complete weld penetration and grinding

Length and diameter:
- Overall length tolerance: ± 1/2" typical (varies by specification)
- Diameter tolerance: ± 1/8" on OD (affects fit-up with supports)

Inspection of tolerances:
- Manufacturer Quality Control measures dimensions
- Authorized Inspector verifies compliance with Code tolerances
- Non-compliant dimensions may require repair or rejection
        """,
        key_factors=[
            "Out-of-roundness measurement and limit (1% of diameter)",
            "Head depth and radius tolerances (critical for stress)",
            "Plate thickness undermeasure (not permitted)",
            "Weld reinforcement limits (1/4\" or 1/4*t)",
            "Joint offset limits (1/4*t longitudinal, 1/2*t circumferential)",
            "Measurement methods and frequency",
            "Corrective actions if tolerances exceeded",
            "Inspector verification and documentation"
        ],
        primary_authority=[
            "ASME VIII-1 UG-79 (thickness tolerances)",
            "ASME VIII-1 UG-80 (cylindrical shell tolerances)",
            "ASME VIII-1 UG-81 (formed head tolerances)",
            "ASME VIII-1 UW-33 (weld joint alignment)"
        ],
        burden_holder="Manufacturer must fabricate within Code tolerances and provide documentation",
        adversary_position="Tolerances may be difficult to achieve with standard fabrication methods",
        counter_arguments=[
            "1% out-of-roundness is fairly loose (some vessels need tighter for precision)",
            "Measurement is subjective (depends on measurement method and location)",
            "Correction of out-of-tolerance vessel is expensive",
            "Tight tolerances increase fabrication cost significantly",
            "Some tolerances (weld reinforcement) are cosmetic more than structural"
        ],
        resolution_strategy="Specify tighter tolerances if required by service, invest in precision forming equipment, measure frequently during fabrication, use jigs and fixtures to control geometry, machine heads if necessary",
        entity_scope="All ASME Code pressure vessels during fabrication",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - tolerances are well-established and verifiable",
        controlling_precedent="ASME VIII-1 UG-80, UG-81 tolerances are mandatory for Code compliance",
        category=IssueCategory.FABRICATION
    ),

    # Additional doctrine blocks would go here to reach 25+ total
    # Topics to add: flat head design, quick-opening closures, external pressure design,
    # buckling analysis, creep design, etc.
]


# ============================================================================
# ENGINE CORE
# ============================================================================

class MECH09Engine:
    def __init__(self):
        self.start_time = time.time()
        self.query_count = 0
        self.total_latency = 0.0
        self.doctrine_hit_count = defaultdict(int)
        self.triggered_categories = defaultdict(int)

        logger.info("MECH09 Pressure Vessel Design Engine initialized")
        logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Tuple[str, List[str], List[str], ConfidenceLevel]:
        """
        Three-layer retrieval: doctrine cache → semantic search → deep analysis
        """
        triggered = []
        authorities = []

        # Layer 1: Doctrine cache (0-50ms)
        cache_result = self._search_doctrine_cache(query)
        if cache_result:
            triggered.extend([d.topic for d in cache_result])
            for doctrine in cache_result:
                authorities.extend(doctrine.primary_authority)
                self.doctrine_hit_count[doctrine.topic] += 1
                self.triggered_categories[doctrine.category.value] += 1

            answer = self._synthesize_from_doctrines(cache_result, query, mode, zone)
            confidence = self._determine_confidence(cache_result)

            logger.info(f"Cache hit: {len(cache_result)} doctrines triggered")
            return answer, triggered, authorities, confidence

        # Layer 2: Semantic search (would use vector DB in production)
        logger.info("Cache miss, semantic search not implemented (would query vector DB)")

        # Layer 3: Deep analysis
        answer = self._deep_analysis(query, mode, zone)
        confidence = ConfidenceLevel.DISCLOSURE

        return answer, triggered, authorities, confidence

    def _search_doctrine_cache(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache by keywords"""
        query_lower = query.lower()
        matches = []

        for doctrine in DOCTRINE_CACHE:
            for keyword in doctrine.keywords:
                if keyword.lower() in query_lower:
                    matches.append(doctrine)
                    break

        return matches

    def _synthesize_from_doctrines(
        self,
        doctrines: List[DoctrineBlock],
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> str:
        """Synthesize answer from triggered doctrine blocks"""

        if mode == ResponseMode.FAST:
            # Concise response
            conclusions = []
            for d in doctrines[:3]:  # Top 3 doctrines
                conclusions.extend(d.conclusion_template)
            return " ".join(conclusions)

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready response with full authority citations
            response_parts = []

            for d in doctrines:
                response_parts.append(f"**{d.topic}**")
                response_parts.append("\n".join(d.conclusion_template))
                response_parts.append(f"\nAuthorities: {', '.join(d.primary_authority)}")
                response_parts.append(f"Confidence: {d.confidence.value}")
                response_parts.append("")

            return "\n".join(response_parts)

        else:  # MEMO mode
            # Full documentation with reasoning
            memo_parts = []

            memo_parts.append(f"PRESSURE VESSEL DESIGN MEMORANDUM")
            memo_parts.append(f"Query: {query}")
            memo_parts.append(f"Analysis Zone: {zone.value}")
            memo_parts.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            memo_parts.append("")

            for i, d in enumerate(doctrines, 1):
                memo_parts.append(f"{i}. {d.topic}")
                memo_parts.append("")
                memo_parts.append("Conclusion:")
                memo_parts.append("\n".join(d.conclusion_template))
                memo_parts.append("")
                memo_parts.append("Reasoning Framework:")
                memo_parts.append(d.reasoning_framework.strip())
                memo_parts.append("")
                memo_parts.append("Key Factors:")
                for factor in d.key_factors:
                    memo_parts.append(f"  - {factor}")
                memo_parts.append("")
                memo_parts.append("Primary Authority:")
                for auth in d.primary_authority:
                    memo_parts.append(f"  - {auth}")
                memo_parts.append("")
                memo_parts.append(f"Burden: {d.burden_holder}")
                memo_parts.append(f"Adversarial Position: {d.adversary_position}")
                memo_parts.append("")
                memo_parts.append("Counter-Arguments:")
                for arg in d.counter_arguments:
                    memo_parts.append(f"  - {arg}")
                memo_parts.append("")
                memo_parts.append(f"Resolution Strategy: {d.resolution_strategy}")
                memo_parts.append(f"Confidence: {d.confidence.value} - {d.confidence_stratification}")
                memo_parts.append("")
                memo_parts.append("---")
                memo_parts.append("")

            return "\n".join(memo_parts)

    def _determine_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Determine overall confidence from triggered doctrines"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Use most conservative confidence level
        confidence_hierarchy = [
            ConfidenceLevel.HIGH_RISK,
            ConfidenceLevel.DISCLOSURE,
            ConfidenceLevel.AGGRESSIVE,
            ConfidenceLevel.DEFENSIBLE
        ]

        for level in confidence_hierarchy:
            if any(d.confidence == level for d in doctrines):
                return level

        return ConfidenceLevel.DEFENSIBLE

    def _deep_analysis(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
        """Fallback deep analysis when no doctrine cache hits"""
        return (
            f"Deep analysis required for: {query}\n\n"
            "This query did not trigger cached doctrine blocks. "
            "In production, this would invoke semantic vector search or LLM-based analysis. "
            "Recommended: consult ASME BPVC Section VIII Division 1 or Division 2 for detailed guidance."
        )

    def determinism_hash(self, query: str, answer: str) -> str:
        """SHA-256 hash for reproducibility verification"""
        content = f"{query}|||{answer}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def query(self, req: QueryRequest) -> QueryResponse:
        """Main query endpoint"""
        start = time.time()
        self.query_count += 1

        answer, triggered, authorities, confidence = self.three_layer_response(
            req.query, req.mode, req.zone
        )

        latency_ms = (time.time() - start) * 1000
        self.total_latency += latency_ms

        det_hash = self.determinism_hash(req.query, answer)

        # Audit trail
        logger.info(
            f"Query processed | Mode: {req.mode.value} | Zone: {req.zone.value} | "
            f"Triggered: {len(triggered)} | Latency: {latency_ms:.2f}ms | Hash: {det_hash}"
        )

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            triggered_doctrines=triggered,
            authorities=list(set(authorities)),  # Deduplicate
            mode=req.mode,
            zone=req.zone,
            determinism_hash=det_hash,
            latency_ms=round(latency_ms, 2),
            timestamp=datetime.now().isoformat()
        )

    def health(self) -> HealthResponse:
        """Health check endpoint"""
        uptime = time.time() - self.start_time
        avg_latency = self.total_latency / self.query_count if self.query_count > 0 else 0.0

        return HealthResponse(
            status="operational",
            version="1.0.0",
            port=9049,
            doctrines_loaded=len(DOCTRINE_CACHE),
            uptime_seconds=round(uptime, 2),
            total_queries=self.query_count,
            avg_latency_ms=round(avg_latency, 2)
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="MECH09 - Pressure Vessel Design Engine",
    description="TIE Gold Standard - Mechanical Engineering Domain",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = MECH09Engine()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    """Main query endpoint - three-layer response"""
    try:
        return engine.query(req)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint"""
    return engine.health()


@APP.get("/doctrines")
async def list_doctrines():
    """List all doctrine topics and categories"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }


@APP.get("/categories")
async def list_categories():
    """List issue categories and doctrine counts"""
    category_counts = defaultdict(int)
    for d in DOCTRINE_CACHE:
        category_counts[d.category.value] += 1

    return {
        "categories": dict(category_counts),
        "total_categories": len(category_counts)
    }


@APP.get("/")
async def root():
    """Root endpoint"""
    return {
        "engine": "MECH09 - Pressure Vessel Design Engine",
        "version": "1.0.0",
        "port": 9049,
        "domain": "Mechanical Engineering - Pressure Vessels",
        "doctrines": len(DOCTRINE_CACHE),
        "endpoints": ["/query", "/health", "/doctrines", "/categories"]
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting MECH09 Pressure Vessel Design Engine on port 9049")
    uvicorn.run(APP, host="127.0.0.1", port=9049, log_level="info")
