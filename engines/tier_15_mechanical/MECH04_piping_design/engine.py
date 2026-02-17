"""
MECH04 - Piping Design & Analysis Engine
TIE Gold Standard Implementation

Domain: Mechanical Engineering - Piping Systems
Coverage: ASME B31.3/B31.4/B31.8, pipe sizing, stress analysis, material selection,
         flange ratings, hydraulics, two-phase flow, integrity management

Authority: ASME B31 codes, ASME B16 standards, API specifications
Version: 1.0.0
Port: 9044
"""

import asyncio
import hashlib
import json
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict
from dataclasses import dataclass, field

# CRITICAL: Add parent directory to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field
import uvicorn

# ============================================================================
# CONFIGURATION & LOGGING
# ============================================================================

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "logs" / "mech04_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)

APP = FastAPI(title="MECH04 Piping Design Engine", version="1.0.0")
APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# ENUMS & DATA MODELS
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
    PIPE_SIZING = "PIPE_SIZING"
    PRESSURE_RATING = "PRESSURE_RATING"
    MATERIAL_SELECTION = "MATERIAL_SELECTION"
    STRESS_ANALYSIS = "STRESS_ANALYSIS"
    SUPPORT_DESIGN = "SUPPORT_DESIGN"
    FLANGE_SELECTION = "FLANGE_SELECTION"
    HYDRAULICS = "HYDRAULICS"
    TWO_PHASE_FLOW = "TWO_PHASE_FLOW"
    CODE_COMPLIANCE = "CODE_COMPLIANCE"
    WELDING = "WELDING"
    CORROSION_PROTECTION = "CORROSION_PROTECTION"
    INTEGRITY_MANAGEMENT = "INTEGRITY_MANAGEMENT"

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    DESIGN = "DESIGN"
    REVIEW = "REVIEW"

@dataclass
class DoctrineBlock:
    """Encapsulates expert reasoning on a piping design topic"""
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: Optional[str] = None
    adversary_position: Optional[str] = None
    counter_arguments: List[str] = field(default_factory=list)
    entity_scope: str = "GENERAL"
    issue_categories: List[IssueCategory] = field(default_factory=list)

class QueryRequest(BaseModel):
    question: str = Field(..., description="Piping design question")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    context: Optional[Dict[str, Any]] = Field(default=None)

class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    authorities: List[str]
    reasoning_chain: List[str]
    triggered_doctrines: List[str]
    mode: ResponseMode
    determinism_hash: str
    telemetry: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float

# ============================================================================
# DOCTRINE CACHE - 25+ REAL PIPING DESIGN EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="ASME B31.3 Process Piping Code Applicability",
        keywords=["B31.3", "process piping", "refinery", "chemical plant", "scope", "applicability"],
        conclusion_template=[
            "ASME B31.3 Process Piping governs piping in petroleum refineries, chemical plants, and related processing facilities.",
            "The code covers piping within the property limits of facilities engaged in processing or handling of petroleum, chemicals, and related products.",
            "B31.3 does NOT apply to: power piping (B31.1), pipeline transportation (B31.4/B31.8), building services, or pressure vessels."
        ],
        reasoning_framework="""
ASME B31.3 Scope Analysis:
1. Facility Type: Is this a refinery, chemical plant, pharmaceutical plant, or related processing facility?
2. Property Limits: Does the piping lie within the property limits of the facility?
3. Exclusions: Does the piping fall under another B31 code (B31.1 power, B31.4/B31.8 pipeline, B31.9 building services)?
4. Fluid Service: Is the piping handling process fluids (not utility steam/water covered by B31.1)?

Key Determinations:
- B31.3 applies to process piping from equipment connection to first valve outside property line
- Interface with B31.4/B31.8 occurs at the first block valve outside the process unit property line
- Utility piping within a process plant (steam, cooling water, instrument air) typically follows B31.3, not B31.1
- Piping connecting to pressure vessels must meet B31.3 even if vessel is ASME Section VIII

Material Selection per B31.3:
- Table A-1 lists allowable materials and temperature limits
- Carbon steel: ASTM A106 Grade B (seamless pipe), A53 Grade B (seamless or welded)
- Low-temperature service (<-20°F): ASTM A333 Grades 1, 3, 6
- Stainless steel: ASTM A312 TP304, TP316, TP321 (austenitic)
- Duplex stainless: ASTM A790 S31803, S32205, S32750

Wall Thickness Calculation:
- Pressure design per Equation 3a: t = (P × D) / (2 × (S × E + P × Y))
- Where: t=thickness, P=internal pressure, D=OD, S=allowable stress, E=weld joint efficiency, Y=temperature coefficient
- Must add corrosion allowance and mill tolerance (typically 12.5%)
        """,
        key_factors=[
            "Facility type (refinery, chemical plant, pharma)",
            "Property line boundaries",
            "Fluid service (process vs utility)",
            "Code jurisdictional interfaces (B31.1, B31.4, B31.8)",
            "Material selection from Table A-1",
            "Pressure design calculation per Chapter II"
        ],
        primary_authority=[
            "ASME B31.3-2022 Process Piping Code",
            "ASME B31.3 Chapter I - Scope and Definitions",
            "ASME B31.3 Chapter II - Design",
            "ASME B31.3 Table A-1 - Allowable Stresses"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Code interpretation based on published ASME standards with clear jurisdictional boundaries.",
        controlling_precedent="ASME B31.3-2022 Paragraph 300 - Scope",
        issue_categories=[IssueCategory.CODE_COMPLIANCE, IssueCategory.MATERIAL_SELECTION]
    ),

    DoctrineBlock(
        topic="ASME B31.4 Pipeline Transportation Code",
        keywords=["B31.4", "pipeline", "liquid transportation", "crude oil", "refined products", "gathering"],
        conclusion_template=[
            "ASME B31.4 governs liquid petroleum pipelines for transportation systems beyond processing facility property limits.",
            "Covers crude oil, condensate, natural gasoline, natural gas liquids, LPG, liquid petroleum products, liquid anhydrous ammonia, liquid alcohol, and CO2.",
            "Design pressure per Barlow equation with location class factors (0.72, 0.60, 0.50, 0.40 for Classes 1-4)."
        ],
        reasoning_framework="""
B31.4 Applicability Determination:
1. Is the pipeline transporting liquid petroleum products between facilities?
2. Does the pipeline extend beyond property limits of a processing plant?
3. Is the pipeline a gathering system, transmission line, or distribution system?

Design Pressure Calculation (Barlow Equation):
P = (2 × S × t × F × E × T) / D

Where:
- P = internal design pressure (psig)
- S = specified minimum yield strength (SMYS) - typically 35,000 psi for Grade B, 42,000 for X42, 52,000 for X52
- t = nominal wall thickness (inches)
- F = design factor based on location class:
    * Class 1 (rural, low population): F = 0.72
    * Class 2 (fringe areas): F = 0.60
    * Class 3 (suburban): F = 0.50
    * Class 4 (urban, multistory buildings): F = 0.40
- E = longitudinal weld joint factor (1.00 for seamless, 1.00 for DSAW, 0.80 for ERW if not tested)
- T = temperature derating factor (1.00 for ≤250°F, reduce for higher temps per Table 402.3.1(b))
- D = nominal outside diameter (inches)

Location Class Determination:
- Count number of buildings intended for human occupancy within a 1-mile zone centered on each mile segment
- Class 1: 0-10 buildings
- Class 2: 11-46 buildings
- Class 3: 46+ buildings or class 2 with higher density areas
- Class 4: areas where multistory buildings prevail

Material Selection:
- API 5L Grade B (35 ksi SMYS): standard for most crude oil and products pipelines
- API 5L X42, X52, X60, X65, X70: higher grades for increased pressure or thinner walls
- Must have Charpy V-notch toughness testing for Grade B and higher in HCA (High Consequence Areas)
        """,
        key_factors=[
            "Location class (1-4) based on building density",
            "Design factor (0.72 to 0.40) based on location",
            "Material grade and SMYS",
            "Longitudinal weld joint factor",
            "High Consequence Area (HCA) designation",
            "Pipeline diameter and wall thickness"
        ],
        primary_authority=[
            "ASME B31.4-2022 Liquid Transportation Systems",
            "API 5L Specification for Line Pipe",
            "49 CFR Part 195 - Transportation of Hazardous Liquids by Pipeline",
            "ASME B31.4 Table 402.3.1(a) - Design Factor F"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Code-based design with regulatory overlap (DOT jurisdiction).",
        controlling_precedent="ASME B31.4 Chapter IV - Design",
        issue_categories=[IssueCategory.CODE_COMPLIANCE, IssueCategory.PRESSURE_RATING, IssueCategory.MATERIAL_SELECTION]
    ),

    DoctrineBlock(
        topic="ASME B31.8 Gas Transmission and Distribution",
        keywords=["B31.8", "gas pipeline", "natural gas", "transmission", "distribution", "class location"],
        conclusion_template=[
            "ASME B31.8 governs natural gas pipelines, including gathering, transmission, and distribution systems.",
            "Design pressure uses Barlow equation with location class factors identical to B31.4 (0.72, 0.60, 0.50, 0.40).",
            "Class locations determined by dwelling count within sliding 1-mile zone (same as B31.4 building methodology)."
        ],
        reasoning_framework="""
B31.8 Design Methodology:
1. Classify pipeline location (Class 1, 2, 3, or 4) based on dwelling density
2. Select design factor F based on class location
3. Calculate Maximum Allowable Operating Pressure (MAOP) using Barlow equation
4. Apply additional factors for temperature, weld joint type

Design Pressure Equation:
P = (2 × S × t × F × E × T) / D

Same form as B31.4, but:
- S = SMYS for gas pipeline steel (API 5L Grade B = 35,000 psi minimum)
- F = design factor: 0.72 (Class 1), 0.60 (Class 2), 0.50 (Class 3), 0.40 (Class 4)
- E = weld joint factor: 1.00 seamless/DSAW, 1.00 ERW if tested, 0.60 furnace butt weld
- T = temperature derating per Table 841.116A

Class Location (B31.8 methodology):
- Slide a 1-mile long zone along pipeline
- Count dwellings (buildings intended for human occupancy) in 220-yard corridor (110 yards each side)
- Class 1: 10 or fewer dwellings
- Class 2: More than 10 but less than 46 dwellings
- Class 3: 46 or more dwellings
- Class 4: Multistory buildings with 4+ stories above ground where traffic/occupancy are prevalent

Special Considerations:
- Gathering lines (low pressure, upstream of processing) may use higher F factors (0.80) if meeting specific criteria
- Distribution systems (lower pressure, residential delivery) follow Class 3 or 4 design factors
- Transmission lines (high pressure, long distance) typically Class 1 or 2
- Compressor station piping may exceed 0.72 design factor if meeting additional requirements
        """,
        key_factors=[
            "Dwelling count within 220-yard corridor",
            "Class location designation (1-4)",
            "Design factor based on location class",
            "Pipeline function (gathering, transmission, distribution)",
            "MAOP (Maximum Allowable Operating Pressure)",
            "Proximity to high consequence areas"
        ],
        primary_authority=[
            "ASME B31.8-2022 Gas Transmission and Distribution Piping Systems",
            "API 5L Specification for Line Pipe",
            "49 CFR Part 192 - Transportation of Natural and Other Gas by Pipeline",
            "ASME B31.8 Section 841.11 - Design Formula"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Code-prescribed methodology with regulatory oversight (PHMSA jurisdiction).",
        controlling_precedent="ASME B31.8 Chapter VIII - Design",
        issue_categories=[IssueCategory.CODE_COMPLIANCE, IssueCategory.PRESSURE_RATING]
    ),

    DoctrineBlock(
        topic="Pipe Sizing for Liquid Flow - Darcy-Weisbach Equation",
        keywords=["pipe sizing", "pressure drop", "Darcy-Weisbach", "friction factor", "velocity", "Reynolds number"],
        conclusion_template=[
            "Pipe sizing for liquid flow balances pressure drop, velocity limits, and economic pipe diameter.",
            "Darcy-Weisbach equation provides accurate friction loss: ΔP = f × (L/D) × (ρ × V²/2).",
            "Velocity limits: 3-10 ft/s typical for liquids; higher for clean fluids, lower for erosive/corrosive services."
        ],
        reasoning_framework="""
Pipe Sizing Methodology:
1. Determine flow rate (Q in gpm or bbl/hr)
2. Estimate pipe diameter based on velocity criteria
3. Calculate Reynolds number to determine flow regime
4. Determine friction factor (f) from Moody diagram or Colebrook equation
5. Calculate pressure drop using Darcy-Weisbach equation
6. Iterate if pressure drop exceeds allowable or velocity outside acceptable range

Darcy-Weisbach Pressure Drop:
ΔP = f × (L/D) × (ρ × V² / 2)

Where:
- ΔP = pressure drop (psi)
- f = Darcy friction factor (dimensionless)
- L = pipe length (ft)
- D = inside diameter (ft)
- ρ = fluid density (lb/ft³)
- V = fluid velocity (ft/s)

Velocity Calculation:
V = (Q × 0.4085) / (D²)  [for Q in gpm, D in inches]
V = (Q × 0.0119) / (D²)  [for Q in bbl/hr, D in inches]

Reynolds Number:
Re = (ρ × V × D) / μ = (D × V × ρ) / μ

Where:
- ρ = density (lb/ft³)
- V = velocity (ft/s)
- D = inside diameter (ft)
- μ = dynamic viscosity (lb/(ft·s))

For Re < 2300: Laminar flow, f = 64/Re
For Re > 4000: Turbulent flow, f from Moody diagram or Colebrook-White equation
For 2300 < Re < 4000: Transition region, use turbulent correlation

Colebrook-White Equation (turbulent flow):
1/√f = -2 × log₁₀[(ε/(3.7×D)) + (2.51/(Re×√f))]

Where ε = pipe roughness (ft) - typically 0.00015 ft for commercial steel

Velocity Guidelines:
- Water, clean hydrocarbons: 3-10 ft/s (5-7 ft/s optimal)
- Viscous fluids: 2-5 ft/s
- Steam (high pressure): 100-200 ft/s
- Erosive services (sand-laden fluids): 2-3 ft/s
- Suction lines (pumps): 2-4 ft/s to avoid cavitation
- Discharge lines: 5-10 ft/s
        """,
        key_factors=[
            "Flow rate (gpm, bbl/hr, or bbl/day)",
            "Fluid properties (density, viscosity)",
            "Reynolds number and flow regime",
            "Friction factor (laminar or turbulent)",
            "Allowable pressure drop",
            "Velocity limits based on service",
            "Pipe roughness (new vs corroded)",
            "Economic pipe diameter (capital vs operating cost)"
        ],
        primary_authority=[
            "Crane Technical Paper 410 - Flow of Fluids Through Valves, Fittings, and Pipe",
            "ASME B31.3 Appendix D - Flexibility and Stress Intensification Factors",
            "Perry's Chemical Engineers' Handbook - Fluid Mechanics Section",
            "Hydraulic Institute Standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Engineering analysis based on established fluid mechanics principles.",
        issue_categories=[IssueCategory.PIPE_SIZING, IssueCategory.HYDRAULICS]
    ),

    DoctrineBlock(
        topic="Hazen-Williams Equation for Water Flow",
        keywords=["Hazen-Williams", "water flow", "C factor", "roughness coefficient", "pressure drop"],
        conclusion_template=[
            "Hazen-Williams equation is widely used for water flow in pipe networks due to its simplicity.",
            "Applicable only to water at 60°F; not valid for other fluids, gases, or non-Newtonian fluids.",
            "C factor ranges: 150 (new smooth pipe) to 100 (old corroded pipe)."
        ],
        reasoning_framework="""
Hazen-Williams Equation:
V = 1.318 × C × R^0.63 × S^0.54

Or in pressure drop form:
ΔP = (4.52 × Q^1.85) / (C^1.85 × D^4.87) × L

Where:
- V = velocity (ft/s)
- C = Hazen-Williams roughness coefficient
- R = hydraulic radius (ft) = D/4 for circular pipes
- S = slope of energy line (ft/ft) = ΔH/L
- Q = flow rate (gpm)
- D = inside diameter (inches)
- L = pipe length (ft)
- ΔP = pressure drop (psi)

C Factor Selection:
- C = 150: New PVC, smooth plastic, glass
- C = 140: New smooth steel, copper
- C = 130: New cast iron, smooth coated steel
- C = 120: New uncoated steel or average condition pipe
- C = 100: Old corroded pipe, tuberculated iron
- C = 80-90: Very old, heavily corroded pipe

Limitations:
- ONLY applicable to water at approximately 60°F
- NOT valid for: oils, chemicals, gases, slurries, non-Newtonian fluids
- Empirical equation, not theoretically derived
- Less accurate than Darcy-Weisbach for Reynolds number extremes
- Cannot account for viscosity changes with temperature

When to Use:
- Municipal water distribution systems
- Fire protection piping (sprinkler systems typically use C=120)
- Potable water supply piping
- Cooling water systems (with appropriate C factor for fouling)

When NOT to Use:
- Process piping with hydrocarbons, chemicals, or non-water fluids
- Gas pipelines
- High-temperature or cryogenic services
- Viscous fluids (use Darcy-Weisbach instead)
        """,
        key_factors=[
            "Applicability limited to water at 60°F",
            "C factor selection based on pipe material and age",
            "Pipe inside diameter",
            "Flow rate in gpm",
            "Cannot be used for non-water fluids"
        ],
        primary_authority=[
            "AWWA Manual M11 - Steel Pipe Design and Installation",
            "NFPA 13 - Installation of Sprinkler Systems (uses C=120)",
            "Hydraulic Institute Engineering Data Book"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Empirical correlation with known limitations; conservative for design but not universally applicable.",
        issue_categories=[IssueCategory.PIPE_SIZING, IssueCategory.HYDRAULICS]
    ),

    DoctrineBlock(
        topic="Pipe Schedule and Wall Thickness Calculation",
        keywords=["pipe schedule", "wall thickness", "schedule 40", "schedule 80", "STD", "XS", "XXS", "Barlow"],
        conclusion_template=[
            "Pipe schedule is a wall thickness designation system; Schedule 40 is standard weight, Schedule 80 is extra strong.",
            "Wall thickness must satisfy internal pressure (Barlow equation), external loads, and code requirements.",
            "For sizes ≤NPS 12, schedule numbers approximate 1000×P/S; for larger sizes, schedules are arbitrary designations."
        ],
        reasoning_framework="""
Pipe Schedule System:
- Schedule Number ≈ 1000 × (P / S) where P = design pressure (psi), S = allowable stress (psi)
- Common schedules: 10, 20, 30, 40, 60, 80, 100, 120, 140, 160
- STD (Standard) = Schedule 40 for NPS ≤10, different for larger
- XS (Extra Strong) = Schedule 80 for most sizes
- XXS (Double Extra Strong) = heavier than Schedule 160

Wall Thickness Calculation per ASME B31.3:
t = (P × D) / (2 × S × E + 2 × P × Y) + C

Where:
- t = minimum required wall thickness (inches)
- P = internal design pressure (psig)
- D = outside diameter (inches)
- S = allowable stress at design temperature (psi) from Table A-1
- E = weld joint quality factor (1.0 for seamless, 1.0 for DSAW per Table A-1A, 0.85 for ERW if not 100% radiographed)
- Y = coefficient from Table 304.1.1 (0.4 for ferritic steel, 0.4 for austenitic steel at lower temps)
- C = corrosion allowance (typically 0.0625" to 0.125" for carbon steel process piping)

Then add mill tolerance:
- Mill tolerance per ASTM A530: +20%, -12.5%
- Therefore nominal wall thickness selected must be: t_nominal = t_min / 0.875

Barlow Equation (Simplified, for thin-wall cylinder):
P = (2 × S × t) / D

This assumes t/D < 0.1 (thin-wall assumption valid for most pipe)

For thick-wall cylinders (t/D > 0.1), use Lamé equation:
P = S × [(D_o² - D_i²) / D_o²]

Material Selection and Schedule:
- Carbon steel process piping: typically Schedule 40 for NPS ≤6, Schedule 30 or 40 for larger
- High-pressure service: Schedule 80, 160, or XXS
- Low-pressure (under 150 psi): Schedule 10 or 20 may suffice
- Cryogenic service: Schedule 40 minimum for thermal contraction margin

Standard Pipe Dimensions (examples):
- 2" Schedule 40: 2.375" OD, 0.154" wall, 2.067" ID
- 4" Schedule 40: 4.500" OD, 0.237" wall, 4.026" ID
- 6" Schedule 40: 6.625" OD, 0.280" wall, 6.065" ID
- 12" Schedule 40: 12.750" OD, 0.375" wall, 12.000" ID
        """,
        key_factors=[
            "Internal design pressure",
            "Allowable stress for material at design temperature",
            "Weld joint efficiency factor",
            "Corrosion allowance",
            "Mill tolerance (12.5% under-thickness permitted)",
            "External loads (weight, wind, seismic)",
            "Schedule availability for pipe size"
        ],
        primary_authority=[
            "ASME B31.3 Chapter II - Design, Para 304",
            "ASME B36.10M - Welded and Seamless Wrought Steel Pipe",
            "ASME B36.19M - Stainless Steel Pipe",
            "ASTM A530 - General Requirements for Specialized Carbon and Alloy Steel Pipe"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Code-mandated calculation method with established safety margins.",
        controlling_precedent="ASME B31.3 Paragraph 304.1.2 - Straight Pipe Under Internal Pressure",
        issue_categories=[IssueCategory.PRESSURE_RATING, IssueCategory.MATERIAL_SELECTION]
    ),

    DoctrineBlock(
        topic="Material Specifications - Carbon Steel Pipe",
        keywords=["A106", "A53", "API 5L", "carbon steel", "seamless", "ERW", "material selection"],
        conclusion_template=[
            "ASTM A106 Grade B is the standard seamless carbon steel pipe for high-temperature service.",
            "ASTM A53 Grade B is available in seamless or ERW; ERW requires additional scrutiny for cyclic service.",
            "API 5L is specified for pipeline service; Grade B (35 ksi SMYS) is standard, higher grades (X42-X80) for increased strength."
        ],
        reasoning_framework="""
Carbon Steel Pipe Material Selection:

ASTM A106 (Seamless Pipe for High-Temperature Service):
- Grades A, B, C (increasing strength: A=30ksi, B=35ksi, C=40ksi yield)
- A106 Grade B most common: 35,000 psi yield, 60,000 psi tensile
- Seamless manufacturing: no longitudinal weld seam
- Temperature range: -20°F to 750°F (Grade B)
- Applications: High-pressure steam, process piping, refinery service
- Chemistry: C ≤0.30%, Mn 0.29-1.06%, P ≤0.035%, S ≤0.035%, Si ≥0.10%

ASTM A53 (Pipe, Steel, Black and Hot-Dipped, Zinc-Coated, Welded and Seamless):
- Grade A or B (B is stronger: 35 ksi yield)
- Type F (furnace butt weld) - obsolete, not used
- Type E (electric resistance welded - ERW)
- Type S (seamless)
- A53 Grade B seamless is interchangeable with A106 Grade B for most applications
- ERW pipe (Type E) has longitudinal weld seam; ASME B31.3 allows E=1.0 if manufacturer tests per A53 requirements
- Applications: General structural, plumbing, low-pressure process

API 5L (Line Pipe - Petroleum and Natural Gas Industries):
- Grade A (30 ksi), Grade B (35 ksi), X42 (42 ksi), X52 (52 ksi), X60, X65, X70, X80
- PSL 1 (standard quality) vs PSL 2 (higher quality, tougher testing requirements)
- Manufacturing: Seamless, ERW, DSAW (double submerged arc welded),SAW (submerged arc welded)
- PSL 2 requires Charpy V-notch impact testing for toughness
- Applications: Oil and gas pipelines per ASME B31.4 and B31.8
- Grade B is most common for crude oil and products pipelines
- Higher grades (X52, X60, X65, X70) allow thinner walls for same pressure rating

Selection Criteria:
1. Temperature: A106 for >400°F, A53 or API 5L for lower temps
2. Pressure: Higher grades (X52-X70) if high pressure and cost-effective wall thickness reduction desired
3. Toughness: PSL 2 or A106 if low-temperature service or high consequence area
4. Code: B31.3 allows A106, A53, API 5L; B31.4/B31.8 specify API 5L
5. Welding: All are weldable; API 5L PSL 2 has controlled chemistry for better weldability

Corrosion Allowance:
- Add 0.0625" (1/16") to 0.125" (1/8") corrosion allowance for carbon steel in corrosive service
- Stainless steel typically no corrosion allowance unless specific corrodent present
        """,
        key_factors=[
            "Service temperature range",
            "Design pressure and required strength",
            "Seamless vs welded (ERW, DSAW)",
            "Applicable code (B31.3, B31.4, B31.8)",
            "Toughness requirements (impact testing)",
            "Corrosion environment",
            "Weldability and fabrication requirements"
        ],
        primary_authority=[
            "ASTM A106 - Seamless Carbon Steel Pipe for High-Temperature Service",
            "ASTM A53 - Pipe, Steel, Black and Hot-Dipped, Zinc-Coated, Welded and Seamless",
            "API 5L - Specification for Line Pipe",
            "ASME B31.3 Table A-1 - Allowable Stresses"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Material selection per published standards with clear applicability criteria.",
        issue_categories=[IssueCategory.MATERIAL_SELECTION, IssueCategory.CODE_COMPLIANCE]
    ),

    DoctrineBlock(
        topic="Low-Temperature Carbon Steel - ASTM A333",
        keywords=["A333", "low temperature", "cryogenic", "impact testing", "Grade 1", "Grade 3", "Grade 6"],
        conclusion_template=[
            "ASTM A333 seamless and welded pipe is specified for low-temperature service requiring notch-toughness.",
            "Grade 6 is most common, suitable to -50°F; Grade 3 to -150°F; Grade 1 is low-carbon for severe applications.",
            "All A333 grades require Charpy V-notch impact testing to verify toughness at design minimum temperature."
        ],
        reasoning_framework="""
ASTM A333 Low-Temperature Carbon Steel Pipe:

Grade Selection by Temperature:
- Grade 1: Low-carbon steel, suitable to -325°F (extreme cryogenic, LNG)
- Grade 3: Ni-alloyed (3.5% Ni), suitable to -150°F (ethylene, propylene refrigeration)
- Grade 6: Similar chemistry to A106 Grade B, suitable to -50°F (cold climates, refrigeration)
- Grade 7: Intermediate, suitable to -75°F
- Grade 8: Ni-alloyed, suitable to -320°F (LNG, liquid nitrogen)

Impact Testing Requirements:
- All A333 grades require Charpy V-notch impact testing per ASTM A333 specification
- Test temperature: at or below the design minimum temperature
- Minimum absorbed energy: typically 15 ft-lbf average (10 ft-lbf minimum for any single specimen)
- Three specimens tested; average and individual minimums must be met
- Lateral expansion measurement also recorded

Material Properties (Grade 6 example):
- Tensile: 60,000 psi minimum
- Yield: 35,000 psi minimum
- Chemistry: C ≤0.30%, Mn 0.29-1.06%, P ≤0.025%, S ≤0.025%, Si 0.10% min
- Manufacturing: Seamless or welded (ERW, SAW)

Design Considerations:
1. Temperature: Specify A333 if design minimum temperature <-20°F
2. Thermal shock: Material must tolerate rapid temperature changes without brittle fracture
3. Exemptions: ASME B31.3 permits A106/A53 Grade B to -20°F without impact testing
4. Thickness: Thinner materials (<0.5" wall) may not require impact testing per B31.3 exemption curves
5. Stress level: Low-stress service may permit higher minimum temperature per B31.3 Fig 323.2.2

Code Requirements (ASME B31.3):
- Para 323: Impact testing required when minimum design temperature below exemption curve
- Fig 323.2.2A: Exemption curves for carbon steel (based on thickness and stress)
- For temperatures <-20°F, A333 with impact testing is standard practice
- Alternatively, austenitic stainless steel (A312 TP304/316) inherently tough at low temps (no impact testing required)
        """,
        key_factors=[
            "Design minimum temperature",
            "Impact testing requirements (Charpy V-notch)",
            "Material grade selection (1, 3, 6, 7, 8)",
            "Pipe wall thickness (exemption curves)",
            "Code compliance (ASME B31.3 Para 323)",
            "Alternative materials (stainless steel)"
        ],
        primary_authority=[
            "ASTM A333 - Seamless and Welded Steel Pipe for Low-Temperature Service",
            "ASME B31.3 Para 323 - Impact Testing",
            "ASME B31.3 Fig 323.2.2A - Impact Test Exemption Curves",
            "ASME B31.3 Table A-1"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Code-mandated toughness requirements with material standards.",
        issue_categories=[IssueCategory.MATERIAL_SELECTION, IssueCategory.CODE_COMPLIANCE]
    ),

    DoctrineBlock(
        topic="Stainless Steel Pipe - ASTM A312 Austenitic Grades",
        keywords=["A312", "stainless steel", "TP304", "TP316", "TP321", "corrosion resistance", "austenitic"],
        conclusion_template=[
            "ASTM A312 covers seamless and welded austenitic stainless steel pipe for high-temperature and corrosive service.",
            "TP304 (18Cr-8Ni) is general-purpose grade; TP316 (18Cr-10Ni-2Mo) for chloride and marine environments; TP321 (18Cr-10Ni-Ti) for high-temperature stabilization.",
            "Austenitic stainless inherently tough at cryogenic temperatures; no impact testing required per ASME B31.3."
        ],
        reasoning_framework="""
ASTM A312 Austenitic Stainless Steel Grades:

TP304 (UNS S30400):
- Composition: 18% Cr, 8% Ni, ≤0.08% C, balance Fe
- Applications: General corrosion resistance, food/pharma, chemical processing
- Temperature: -425°F to 1500°F service range
- Corrosion: Excellent in oxidizing acids, organic acids; poor in chloride-containing environments (pitting)
- Weldability: Excellent; carbon migration can cause sensitization (intergranular corrosion) if held 800-1500°F
- Cost: Lower than 316, higher than carbon steel

TP316 (UNS S31600):
- Composition: 16-18% Cr, 10-14% Ni, 2-3% Mo, ≤0.08% C
- Applications: Marine, chloride environments, pulp/paper bleaching, pharmaceutical
- Molybdenum addition: Improves pitting and crevice corrosion resistance
- Seawater: TP316 vastly superior to TP304 (304 pits badly in seawater)
- Cost: 10-20% more expensive than TP304

TP321 (UNS S32100):
- Composition: 17-19% Cr, 9-12% Ni, Ti = 5×(C+N) min, ≤0.08% C
- Titanium stabilized: Prevents carbide precipitation during welding or elevated temperature service
- Applications: High-temperature service (900-1500°F), jet engine exhaust, refinery heaters
- Prevents sensitization: Ti combines with C to form TiC, preventing chromium carbide formation at grain boundaries
- Alternative: TP347 (Nb-stabilized) serves similar purpose

Low-Carbon Grades (L suffix):
- TP304L: ≤0.03% C (vs ≤0.08% for TP304)
- TP316L: ≤0.03% C
- Purpose: Reduce sensitization risk in welded components
- When to use: Heavy-section welding, no post-weld heat treatment available

Dual-Certified Grades:
- TP304/304L: meets both specs (common practice)
- TP316/316L: meets both specs
- Allows flexibility in fabrication

Design Allowable Stress:
- ASME B31.3 Table A-1: TP304/316 at 100°F = 20,000 psi allowable (vs 35,000 psi for A106 Grade B carbon steel)
- Lower allowable stress means thicker wall required for same pressure
- However, no corrosion allowance typically needed, offsetting some thickness penalty

Passivation:
- Stainless requires chromium oxide passive film for corrosion resistance
- Post-fabrication passivation (nitric acid or citric acid treatment) recommended
- Removes free iron contamination from machining, welding, grinding
        """,
        key_factors=[
            "Corrosion environment (chlorides, acids, seawater)",
            "Service temperature (cryogenic to high-temp)",
            "Sensitization risk (welding, heat treatment)",
            "Material cost vs lifecycle cost (corrosion resistance)",
            "Passivation and surface finish requirements",
            "Allowable stress (lower than carbon steel)"
        ],
        primary_authority=[
            "ASTM A312 - Seamless, Welded, and Heavily Cold Worked Austenitic Stainless Steel Pipes",
            "ASME B31.3 Table A-1",
            "NACE MR0175/ISO 15156 - Petroleum and Natural Gas Industries - Materials for Use in H₂S Environments"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Material selection based on corrosion science and code allowables.",
        issue_categories=[IssueCategory.MATERIAL_SELECTION, IssueCategory.CORROSION_PROTECTION]
    ),

    DoctrineBlock(
        topic="Duplex Stainless Steel - ASTM A790",
        keywords=["A790", "duplex", "S31803", "S32205", "S32750", "super duplex", "chloride resistance"],
        conclusion_template=[
            "ASTM A790 duplex stainless steel combines austenite and ferrite phases for superior strength and chloride stress corrosion cracking resistance.",
            "S31803/S32205 (2205) is standard duplex; S32750 (2507) is super duplex with higher alloy content and PREN.",
            "Duplex grades have 2× yield strength of austenitic 316, allowing thinner walls and cost savings despite higher material price."
        ],
        reasoning_framework="""
Duplex Stainless Steel Fundamentals:
- Microstructure: ~50% austenite, ~50% ferrite
- Strength: Yield ~65 ksi (vs ~30 ksi for TP316)
- Corrosion: Superior to 316 in chlorides, H₂S, CO₂
- Temperature limit: ~600°F (ferrite phase loses toughness above; sigma phase precipitation above 1200°F)

ASTM A790 Common Grades:

S31803 / S32205 (Duplex 2205):
- Composition: 22% Cr, 5% Ni, 3% Mo, 0.17% N
- PREN: ~35 (Pitting Resistance Equivalent Number = %Cr + 3.3×%Mo + 16×%N)
- Applications: Offshore oil & gas (seawater service), desalination, chemical processing
- Yield strength: 65 ksi minimum (double austenitic 316's 30 ksi)
- Cost: ~2× price of TP316, but thinner wall offsets material cost

S32750 (Super Duplex 2507):
- Composition: 25% Cr, 7% Ni, 4% Mo, 0.27% N
- PREN: ~42 (higher than 2205, excellent pitting resistance)
- Applications: Subsea oil & gas, high-chloride environments, CRA tubing
- Superior to 2205 in very aggressive chloride + H₂S environments

S32760 (Hyper Duplex):
- Composition: 25% Cr, 7% Ni, 3.5% Mo, 0.5-1.0% W, 0.2% N
- PREN: ~40+
- Applications: Most severe corrosion (high Cl⁻, CO₂, H₂S)

Design Advantages:
1. High strength allows Schedule 10 or 20 where 316 needs Schedule 40 (cost savings, weight reduction)
2. Chloride SCC resistance: duplex immune to chloride stress corrosion cracking <~200°F (austenitic 316 fails above 140°F in Cl⁻)
3. Erosion resistance: harder than austenitic grades
4. Thermal conductivity: 2× austenitic (better heat transfer, less thermal stress)

Design Limitations:
1. Temperature: Not for >600°F continuous service (ferrite embrittlement, sigma phase)
2. Toughness: Inferior to austenitic at cryogenic temps (use 316 for <-40°F)
3. Weldability: Requires nitrogen shielding gas, controlled heat input to maintain austenite/ferrite balance
4. Fabrication: Cold forming more difficult due to high strength

ASME B31.3 Allowables:
- S31803 at 100°F: 25,000 psi allowable (vs 20,000 for TP316)
- Higher allowable stress + high yield strength = significant wall thickness reduction
        """,
        key_factors=[
            "Chloride concentration and temperature",
            "H₂S and CO₂ partial pressures (sour service)",
            "Service temperature (<600°F for duplex)",
            "Strength advantage (65 ksi vs 30 ksi for 316)",
            "PREN value for pitting resistance",
            "Cost vs performance (material cost vs lifecycle)",
            "Fabrication and welding complexity"
        ],
        primary_authority=[
            "ASTM A790 - Seamless and Welded Ferritic/Austenitic Stainless Steel Pipe",
            "NACE MR0175/ISO 15156-3 - Corrosion-Resistant Alloys for Oilfield Equipment",
            "ASME B31.3 Table A-1",
            "DNV-RP-F112 - Duplex Stainless Steel - Design Against Hydrogen Induced Stress Cracking"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Engineering analysis of material properties with application-specific validation.",
        issue_categories=[IssueCategory.MATERIAL_SELECTION, IssueCategory.CORROSION_PROTECTION]
    ),

    DoctrineBlock(
        topic="Flange Ratings and Selection - ASME B16.5",
        keywords=["flange", "B16.5", "pressure class", "150#", "300#", "600#", "900#", "1500#", "2500#", "RFWN"],
        conclusion_template=[
            "ASME B16.5 defines flange pressure-temperature ratings for Classes 150, 300, 600, 900, 1500, 2500.",
            "Flange rating must satisfy system pressure AND temperature; allowable pressure decreases as temperature increases.",
            "Welding neck (WN) flanges are preferred for high-pressure, high-cycle, or severe service; slip-on (SO) for low-pressure."
        ],
        reasoning_framework="""
ASME B16.5 Flange Pressure Classes:

Flange Class System:
- Class 150: ~285 psi at 100°F (carbon steel), derated to ~140 psi at 600°F
- Class 300: ~740 psi at 100°F, ~450 psi at 600°F
- Class 600: ~1480 psi at 100°F, ~900 psi at 600°F
- Class 900: ~2220 psi at 100°F, ~1350 psi at 600°F
- Class 1500: ~3705 psi at 100°F, ~2220 psi at 600°F
- Class 2500: ~6170 psi at 100°F, ~3705 psi at 600°F

Pressure-Temperature Rating:
- Rating tables in ASME B16.5 Appendix give allowable pressure vs temperature for each material group
- Material Group 1.1: Carbon steel (A105 forgings, A516-70 plate)
- Material Group 2.1: Stainless steel austenitic (A182 F304/F316)
- Material Group 2.3: Duplex stainless (A182 F51, F53, F55)
- ALWAYS check P-T rating table for actual material at design temperature

Flange Types:

1. Welding Neck (WN, RFWN):
- Full-penetration butt weld to pipe
- Tapered hub provides gradual stress transition
- Best fatigue resistance
- Required for high-pressure, high-temperature, cyclic service
- ASME B31.3 mandates WN for severe cyclic conditions

2. Slip-On (SO):
- Pipe slips inside flange bore, fillet welded inside and outside
- Lower cost, easier alignment
- Lower fatigue strength (stress concentration at fillet welds)
- Acceptable for low-pressure, non-cyclic service
- NOT recommended for cyclic, high-vibration, or severe service

3. Socket Weld (SW):
- Pipe inserts into socket, fillet welded at face
- Small bore piping (NPS 2 and smaller typically)
- Good fatigue strength for small sizes
- Gap at bottom of socket provides stress relief and expansion space

4. Threaded:
- NPT threads, no welding
- Low-pressure, small-bore, non-critical service
- Risk of leakage; not for flammable/toxic fluids per many project specs

5. Lap Joint (LJ):
- Stub end welded to pipe, loose backing flange
- Used with expensive alloy pipe (stub end is alloy, flange is carbon steel)
- Allows flange rotation for bolt hole alignment
- Not for high-pressure service

6. Blind (BL):
- Solid disk, no bore
- Closes off end of pipe or vessel nozzle

Flange Facing:

Raised Face (RF):
- 1/16" or 1/4" raised ring around bore
- Most common facing for Class 150-600
- Gasket contacts raised face only

Ring-Type Joint (RTJ):
- Grooved face for metal ring gasket (oval or octagonal)
- Class 600 and higher, high-pressure, high-temperature
- Superior sealing, zero leakage tolerance services

Flat Face (FF):
- Entire flange face flat
- Cast iron flanges, low-pressure applications
- NOT interchangeable with RF (bolt stress issues)

Bolt Selection:
- ASTM A193 Grade B7 studs (alloy steel, heat treated)
- ASTM A194 Grade 2H heavy hex nuts
- For high-temperature (>800°F): B7 studs with Grade 7 or 7M nuts
- Stud length = flange thickness + gasket thickness + nut height + engagement + protrusion (typically 2-3 threads past nut)

Gasket Selection:
- Class 150-300: Spiral wound with graphite filler (ASME B16.20 Spec)
- Class 600+: Spiral wound or RTJ metal gasket
- Soft gaskets (compressed fiber, rubber) only for low-pressure, low-temperature
        """,
        key_factors=[
            "Design pressure AND temperature (P-T rating curve)",
            "Flange class (150, 300, 600, 900, 1500, 2500)",
            "Flange type (WN, SO, SW, threaded, lap joint, blind)",
            "Flange facing (RF, RTJ, FF)",
            "Material group (carbon steel, stainless, duplex)",
            "Cyclic service (fatigue requirements)",
            "Gasket and bolt selection"
        ],
        primary_authority=[
            "ASME B16.5 - Pipe Flanges and Flanged Fittings NPS 1/2 through NPS 24",
            "ASME B16.47 - Large Diameter Steel Flanges NPS 26 through NPS 60",
            "ASME B16.20 - Metallic Gaskets for Pipe Flanges",
            "ASME B31.3 Para 304.3.3 - Flange Joints"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Code-prescribed flange ratings with material-specific P-T curves.",
        controlling_precedent="ASME B16.5 Pressure-Temperature Ratings, Appendix Tables",
        issue_categories=[IssueCategory.FLANGE_SELECTION, IssueCategory.PRESSURE_RATING]
    ),

    DoctrineBlock(
        topic="Gasket Selection - Spiral Wound, Ring Joint, Compressed Fiber",
        keywords=["gasket", "spiral wound", "ring joint", "RTJ", "graphite", "PTFE", "compressed fiber", "B16.20"],
        conclusion_template=[
            "Spiral wound gaskets with graphite filler are standard for Class 150-600 flanges in process service.",
            "Ring-type joint (RTJ) metal gaskets required for Class 900+ or zero-leakage services.",
            "Gasket selection depends on pressure, temperature, flange class, and fluid compatibility."
        ],
        reasoning_framework="""
Gasket Types and Applications:

Spiral Wound Gaskets (ASME B16.20):
- Construction: V-shaped stainless steel winding with filler material (graphite, PTFE)
- Pressure: Up to 2500# flange class
- Temperature: Graphite filler to 850°F continuous (1200°F intermittent); PTFE to 500°F
- Advantages: Excellent resilience, accommodates flange distortion, reusable in some cases
- Inner ring: Solid metal ring prevents gasket blowout into pipe bore
- Outer ring: Centering ring positions gasket on flange
- Standard for most Class 150-600 hydrocarbon and chemical service

Ring-Type Joint (RTJ) Gaskets:
- Material: Soft iron, low-carbon steel, stainless steel, Monel, Inconel (depending on service)
- Styles: R (oval cross-section), RX (octagonal - higher pressure)
- Pressure: Class 600+ flanges, high-pressure service
- Temperature: Soft iron to 750°F, stainless to 1000°F+
- Sealing: Metal-to-metal contact in grooved flange face
- Applications: High-pressure gas, zero-tolerance leak services, subsea, wellhead
- One-time use: Deformed during installation, cannot be reused

Compressed Fiber (Non-Asbestos):
- Material: Aramid fibers with rubber binder (Garlock 3000, etc.)
- Pressure: Low to medium (Class 150-300)
- Temperature: Typically 500-750°F max depending on formulation
- Applications: Water, steam, dilute acids/bases, low-pressure hydrocarbons
- Cost: Lowest cost gasket option
- Limitations: Poor chemical resistance, compresses permanently, lower pressure capability

PTFE (Teflon) Gaskets:
- Material: Virgin PTFE or filled PTFE
- Temperature: -450°F to +500°F
- Chemical resistance: Excellent (nearly universal chemical compatibility)
- Pressure: Low to medium (limited by cold flow creep)
- Applications: Corrosive chemicals, pharmaceuticals, food/beverage
- Limitations: Cold flow under bolt stress, requires frequent retorquing

Graphite Sheet:
- Pure graphite sheet (no metal reinforcement)
- Temperature: -400°F to 850°F
- Chemical resistance: Excellent except strong oxidizers
- Pressure: Low to medium
- Applications: Heat exchangers, valve bonnets, manways
- Advantages: Conformable, thermal cycling resistant

Gasket Selection Criteria:

1. Pressure Class:
   - Class 150-300: Compressed fiber or spiral wound acceptable
   - Class 400-600: Spiral wound recommended
   - Class 900+: RTJ or high-performance spiral wound required

2. Temperature:
   - <500°F: Compressed fiber, PTFE, or spiral wound w/ graphite
   - 500-850°F: Spiral wound w/ graphite or RTJ
   - >850°F: RTJ only (metal gasket)

3. Fluid Service:
   - Hydrocarbons: Spiral wound w/ graphite (most common)
   - Corrosive chemicals: PTFE or spiral wound w/ PTFE filler
   - Oxygen service: Special oxygen-cleaned gaskets, no graphite (fire risk)
   - Sour gas (H₂S): Soft iron or stainless RTJ (no graphite degradation)

4. Flange Facing:
   - Raised Face (RF): Spiral wound or compressed fiber
   - Ring-Type Joint (RTJ): Metal ring gasket only

5. Leakage Tolerance:
   - Fugitive emissions (VOC): Spiral wound or RTJ
   - Toxic/flammable: RTJ for zero-leakage assurance
   - Water, low-hazard: Compressed fiber acceptable

Bolt Torque and Gasket Stress:
- Gasket manufacturer specifies minimum seating stress (psi)
- Bolt torque calculated to achieve gasket stress
- Under-torque: Leaks; over-torque: Gasket crushing or flange damage
- Spiral wound typically requires 10,000-20,000 psi seating stress
        """,
        key_factors=[
            "Flange class and pressure rating",
            "Service temperature",
            "Fluid chemical compatibility",
            "Leakage tolerance (emissions regulations)",
            "Flange facing type (RF vs RTJ)",
            "Bolt load and gasket seating stress"
        ],
        primary_authority=[
            "ASME B16.20 - Metallic Gaskets for Pipe Flanges",
            "ASME B16.21 - Nonmetallic Flat Gaskets for Pipe Flanges",
            "API 6A - Wellhead and Christmas Tree Equipment (RTJ gaskets)",
            "ASME PCC-1 - Guidelines for Pressure Boundary Bolted Flange Joint Assembly"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Gasket selection based on code requirements and manufacturer data.",
        issue_categories=[IssueCategory.FLANGE_SELECTION, IssueCategory.MATERIAL_SELECTION]
    ),

    DoctrineBlock(
        topic="Pipe Stress Analysis - Sustained, Thermal Expansion, Occasional Loads",
        keywords=["stress analysis", "Caesar II", "AutoPIPE", "sustained loads", "thermal expansion", "occasional loads", "flexibility"],
        conclusion_template=[
            "Pipe stress analysis verifies piping system can withstand sustained loads (weight, pressure), thermal expansion, and occasional loads (wind, seismic) per ASME B31.3.",
            "Sustained stress must not exceed allowable stress Sh; expansion stress limited to SA (1.25Sc + 0.25Sh); occasional stress limited to 1.33Sh.",
            "Flexibility analysis using Caesar II or AutoPIPE software required for systems with thermal expansion >1 inch movement or high-energy piping."
        ],
        reasoning_framework="""
Pipe Stress Analysis per ASME B31.3:

Load Categories:

1. Sustained Loads (SL):
- Weight of pipe, fluid, insulation, valves
- Internal pressure
- External pressure (vacuum)
- Static head of fluid column
- Allowable stress: SL ≤ Sh (hot allowable stress from Table A-1)

2. Thermal Expansion Loads (Thermal or Displacement):
- Thermal growth/contraction of piping
- Differential thermal expansion between connected equipment
- Building/structure settlement
- Allowable stress: SE ≤ SA = f(1.25Sc + 0.25Sh)
  Where: Sc = cold allowable, Sh = hot allowable, f = stress range reduction factor

3. Occasional Loads (OL):
- Wind
- Seismic (earthquake)
- Pressure surges (water hammer, relief valve discharge)
- Allowable stress: SL + OL ≤ k × Sh
  Where k = 1.15 for pressure + occasional, 1.20 for thermal + occasional, 1.33 for all combined

Stress Calculations:

Longitudinal Stress (sustained):
SL = PDo/(4t) + 0.75i × MA/Z + FAx/A

Where:
- P = internal pressure
- Do = outside diameter
- t = wall thickness
- i = stress intensification factor (SIF)
- MA = resultant bending moment
- Z = section modulus
- FAx = axial force
- A = pipe cross-sectional area

Expansion Stress Range:
SE = i × Mb/Z

Where:
- Mb = range of bending moment due to thermal expansion
- i = stress intensification factor for expansion (typically 1.0 straight pipe, higher for elbows/tees)

Stress Intensification Factors (SIF):
- Straight pipe: i = 1.0
- Butt-welded elbow: i = 0.9/h^(2/3) where h = tR/(r²) (flexibility characteristic)
- Tee connection: i = varies, typically 1.5-3.0 depending on geometry
- ASME B31.3 Appendix D provides SIF tables

Flexibility Analysis Triggers (when required):
1. Thermal expansion movement >1 inch
2. High-energy fluid (>200°F and >150 psig)
3. Cyclic service (thermal cycling)
4. Sensitive connected equipment (turbines, compressors, pumps)
5. No expansion loops or expansion joints

Flexibility Methods:
- L-bend (single 90° bend for flexibility)
- Z-bend (two 90° bends in perpendicular planes)
- Expansion loop (U-shaped detour)
- Expansion joint (bellows-type compensator)

Caesar II / AutoPIPE Software Analysis:
- Finite element pipe stress analysis
- Models pipe as beam elements with 6 DOF per node
- Calculates stresses, reactions, displacements
- Checks code compliance (B31.3, B31.1, B31.4, B31.8)
- Outputs: stress isometrics, support loads, nozzle loads on equipment

Support Spacing:
- Must prevent excessive sag (typically L/240 max deflection)
- Typical carbon steel pipe spacing:
  * 2" pipe: 7-10 ft
  * 4" pipe: 11-14 ft
  * 6" pipe: 14-17 ft
  * 12" pipe: 19-23 ft
- Closer spacing if vibration, high-temperature, or heavy valves/fittings

Nozzle Loads on Equipment:
- API 610 (pumps): Limits on Fx, Fy, Fz, Mx, My, Mz
- NEMA SM23 (steam turbines): Nozzle load limits
- Pressure vessel nozzles: WRC 107/297 local stress analysis
- Piping must not overstress equipment nozzles
        """,
        key_factors=[
            "Thermal expansion magnitude (ΔT × L × α)",
            "Sustained stress (weight + pressure)",
            "Expansion stress (thermal displacement)",
            "Occasional stress (wind + seismic)",
            "Support spacing and design",
            "Equipment nozzle load limits",
            "Code allowable stresses (Sh, Sc, SA)",
            "Stress intensification factors (elbows, tees)"
        ],
        primary_authority=[
            "ASME B31.3 Chapter II - Design, Para 319 - Flexibility and Stress Intensification Factors",
            "ASME B31.3 Appendix D - Flexibility and Stress Intensification Factors",
            "API 610 - Centrifugal Pumps for Petroleum, Petrochemical, and Natural Gas Industries",
            "WRC Bulletin 107/297 - Local Stresses in Cylindrical Shells Due to External Loadings on Nozzles"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Engineering analysis per code-mandated stress limits and calculation methods.",
        controlling_precedent="ASME B31.3 Para 319.4 - Allowable Stress Range",
        issue_categories=[IssueCategory.STRESS_ANALYSIS, IssueCategory.SUPPORT_DESIGN]
    ),

    DoctrineBlock(
        topic="Pipe Support Design - Types and Applications",
        keywords=["pipe support", "hanger", "shoe", "spring hanger", "constant support", "guide", "anchor", "restraint"],
        conclusion_template=[
            "Pipe supports must carry sustained loads (weight) while allowing thermal expansion movement or restraining against occasional loads.",
            "Variable spring hangers accommodate thermal displacement while maintaining near-constant support load; constant supports for critical cases.",
            "Guides and anchors control pipe movement; guides allow axial movement, anchors prevent all movement."
        ],
        reasoning_framework="""
Pipe Support Classification:

1. Rigid Supports (Weight-Bearing):
- Pipe shoe: Welded to pipe, rests on structure
- Clevis hanger: Rod and clevis assembly, hangs pipe from overhead structure
- Trapeze support: Horizontal beam supporting multiple pipes
- Pipe roll: Allows longitudinal movement while supporting weight
- Applications: Low-temperature lines, short spans, minimal thermal growth

2. Spring Supports (Variable Load):
- Variable spring hanger: Spring compresses/extends as pipe moves vertically
- Load variation: Typically 25% load change over travel range
- Applications: Long vertical runs with thermal expansion
- Design: Select spring to maintain load within 25% variation over expected travel

3. Constant Support Hangers:
- Mechanism: Spring with lever arm provides constant force regardless of position (within travel)
- Load variation: <6% over full travel (Type A per MSS SP-58)
- Applications: Sensitive equipment nozzles, turbine piping, where load variation must be minimized
- Cost: 3-5× more expensive than variable spring hangers

4. Guides:
- Limit transverse movement while allowing axial (longitudinal) pipe movement
- Pipe slides through guide in one direction only
- Applications: Control pipe thermal expansion direction, prevent lateral buckling
- Design: Wear plate or low-friction material (PTFE) at guide contact surface

5. Anchors:
- Prevent all pipe movement in all directions (6 DOF restrained)
- Transfers all thermal forces to structure
- Applications: Establish expansion loop boundaries, terminate expansion joints
- Design: Massive structural steel support, welded to pipe and structure

6. Restraints:
- Limit movement in specific directions while allowing movement in others
- Seismic restraints: Prevent excessive displacement during earthquake
- Sway braces: Diagonal members resisting lateral movement
- Applications: Seismic zones, prevent vibration-induced movement

Support Spacing Guidelines:

Horizontal Piping (ASME B31.3 recommendations):
- Support spacing = C × [E × I / W]^0.5
  Where: C = constant (depends on end conditions, typically 0.1-0.2)
         E = modulus of elasticity
         I = moment of inertia
         W = weight per unit length

Simplified Spacing Tables (carbon steel, 150°F):
- 2" pipe: 10 ft
- 3" pipe: 12 ft
- 4" pipe: 14 ft
- 6" pipe: 17 ft
- 8" pipe: 19 ft
- 10" pipe: 22 ft
- 12" pipe: 23 ft
- Reduce spacing by 50% if insulated or high-temperature (>450°F)

Vertical Piping:
- Support every floor or every 20-30 ft, whichever is less
- Riser clamps at each support point
- Bottom support must carry full weight of vertical run

Support Design Loads:

Vertical Load (Weight):
W = Wp + Wf + Wi + Wv

Where:
- Wp = pipe weight
- Wf = fluid weight
- Wi = insulation weight
- Wv = valve/fitting weight

Horizontal Load (Friction):
H = μ × W

Where:
- μ = coefficient of friction (0.3 typical for steel on steel, 0.1 for PTFE)
- W = vertical load

Thermal Load (Anchor/Guide):
F = E × A × α × ΔT

Where:
- E = modulus of elasticity
- A = pipe cross-sectional area
- α = coefficient of thermal expansion
- ΔT = temperature change

Support Selection Process:
1. Calculate pipe weight (pipe + fluid + insulation + fittings)
2. Determine thermal movement at support location (from stress analysis)
3. Select support type: rigid if <0.25" movement, spring if >0.25" movement
4. For springs, calculate hot load and cold load
5. Spring selection: Load range and travel must accommodate hot/cold difference
6. Verify support reactions don't overstress structure
        """,
        key_factors=[
            "Pipe weight (including fluid, insulation, fittings)",
            "Thermal expansion movement (vertical and horizontal)",
            "Support spacing (prevent sag)",
            "Spring hanger load variation (25% max for variable, 6% for constant)",
            "Guide vs anchor application",
            "Structural capacity for support reactions",
            "Friction forces at sliding supports"
        ],
        primary_authority=[
            "MSS SP-58 - Pipe Hangers and Supports - Materials, Design, Manufacture, Selection, Application, and Installation",
            "MSS SP-69 - Pipe Hangers and Supports - Selection and Application",
            "ASME B31.3 Para 321 - Supports",
            "Piping Handbook (Mohinder Nayyar)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Support design based on engineering calculations and industry standards.",
        issue_categories=[IssueCategory.SUPPORT_DESIGN, IssueCategory.STRESS_ANALYSIS]
    ),

    DoctrineBlock(
        topic="ASME B16.9 Fittings - Elbows, Tees, Reducers, Caps",
        keywords=["B16.9", "elbow", "tee", "reducer", "cap", "90 degree", "45 degree", "long radius", "short radius"],
        conclusion_template=[
            "ASME B16.9 specifies dimensions and tolerances for factory-made wrought steel butt-welding fittings (elbows, tees, reducers, caps).",
            "Long radius elbows (R = 1.5D) are standard; short radius (R = 1.0D) used where space limited but higher pressure drop.",
            "Wall thickness of fittings matches pipe schedule; pressure rating same as connected pipe."
        ],
        reasoning_framework="""
ASME B16.9 Butt-Welding Fittings:

Elbows:

90° Long Radius (LR):
- Radius of curvature R = 1.5 × Nominal Diameter
- Example: 6" LR 90° elbow has 9" centerline radius
- Standard for most applications (lower pressure drop, lower stress)
- Notation: "6\" 90° LR elbow" or "6\" 90° ELL"

90° Short Radius (SR):
- Radius of curvature R = 1.0 × Nominal Diameter
- Example: 6" SR 90° elbow has 6" centerline radius
- Use when space constrained (tighter bend)
- Higher pressure drop (~30% more than LR)
- Higher stress intensification factor (SIF)

45° Elbow:
- Always long radius (R = 1.5D)
- Used in pairs to achieve 90° turn with lower pressure drop than single 90° elbow
- Less stress than 90° elbow

3D Elbow (3R):
- Radius R = 3 × Nominal Diameter (custom, not B16.9 standard)
- Very low pressure drop
- Used in slurry service, low-shear applications

Tees:

Straight Tee:
- Three openings: run (straight through) and branch (perpendicular)
- Equal tee: All three openings same size
- Reducing tee: Branch opening smaller than run
- Pressure rating same as pipe
- High stress intensification at branch connection

Reducing Tee:
- Run size: 6" × 6" × 4" means 6" inlet, 6" outlet, 4" branch

Lateral (Wye):
- 45° branch connection (instead of 90°)
- Lower stress than straight tee
- Better flow characteristics

Reducers:

Concentric Reducer:
- Centerlines of both ends coincide
- Standard for vertical lines or gas/vapor lines (drainage not required)
- Notation: "6\" × 4\" conc reducer"

Eccentric Reducer:
- One side flat (top or bottom depending on orientation)
- Prevents gas pocket (top flat for liquid lines)
- Prevents liquid trap (bottom flat for gas lines)
- Standard for horizontal liquid lines

Swage (Swaged Reducer):
- One-piece forged reducer (no weld seam)
- Stronger than welded reducer
- Used for high-pressure service

Caps:

Butt-Weld Cap:
- Hemispherical or elliptical end closure
- Welded to pipe end
- Pressure rating per ASME B16.9

Wall Thickness:

Schedule Matching:
- Fitting wall thickness matches pipe schedule
- Example: Schedule 40 pipe uses Schedule 40 fittings
- Wall thickness increases at branch of tee (reinforcement)

Pressure Rating:
- Fittings have same pressure rating as pipe they connect
- No separate pressure class system (unlike flanges)
- Design pressure per ASME B31.3 pipe stress calculation applies

Material:

Common Materials:
- ASTM A234 WPB: Carbon steel (matches A106/A53 Grade B pipe)
- ASTM A234 WP11/WP22: Alloy steel (chrome-moly)
- ASTM A403 WP304/WP316: Stainless steel austenitic
- ASTM A815 WP-S31803/S32205: Duplex stainless

Pressure Drop in Fittings:

Equivalent Length Method:
- Each fitting = X feet of straight pipe for pressure drop calculation
- 90° LR elbow = 30 × diameter equivalent length
- 90° SR elbow = 16 × diameter (NOTE: higher actual ΔP due to sharper turn)
- 45° elbow = 15 × diameter
- Tee (flow through run) = 20 × diameter
- Tee (flow through branch) = 60 × diameter

K Factor Method:
- ΔP = K × (ρ × V²/2)
- K values from Crane TP-410 or equivalent
        """,
        key_factors=[
            "Elbow radius (long radius vs short radius)",
            "Tee type (straight, reducing, lateral)",
            "Reducer type (concentric vs eccentric)",
            "Wall thickness (schedule matching)",
            "Material specification (A234, A403, A815)",
            "Pressure drop (equivalent length or K factor)",
            "Stress intensification factors"
        ],
        primary_authority=[
            "ASME B16.9 - Factory-Made Wrought Buttwelding Fittings",
            "ASTM A234 - Piping Fittings of Wrought Carbon Steel and Alloy Steel",
            "ASTM A403 - Wrought Austenitic Stainless Steel Piping Fittings",
            "Crane TP-410 - Flow of Fluids Through Valves, Fittings, and Pipe"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Fitting selection per published standards with established pressure drop correlations.",
        issue_categories=[IssueCategory.MATERIAL_SELECTION, IssueCategory.HYDRAULICS]
    ),

    DoctrineBlock(
        topic="Pipe Welding - WPS, PQR, Welder Qualification",
        keywords=["welding", "WPS", "PQR", "welder qualification", "ASME Section IX", "GTAW", "SMAW", "root pass"],
        conclusion_template=[
            "ASME B31.3 requires all welding per qualified Welding Procedure Specifications (WPS) based on Procedure Qualification Records (PQR).",
            "Welders must be qualified per ASME Section IX; qualification valid 6 months unless welder performs welding in process.",
            "Critical piping (high-pressure, high-temperature, toxic, flammable) requires 100% radiographic examination or 100% ultrasonic testing."
        ],
        reasoning_framework="""
Welding Requirements per ASME B31.3:

Welding Procedure Specification (WPS):
- Written instructions for welders/welding operators
- Specifies: base metals, filler metal, process (GTAW/SMAW/FCAW/SAW), preheat, interpass temp, post-weld heat treatment (PWHT)
- Must be qualified by Procedure Qualification Record (PQR)
- Format per ASME Section IX QW-482

Procedure Qualification Record (PQR):
- Documents actual welding parameters and test results
- Includes: tensile test, bend tests, (impact tests if required)
- Once PQR created, multiple WPS can reference it (if within qualified ranges)
- PQR is permanent record; WPS can be revised

Welder Performance Qualification (WPQ):
- Each welder must demonstrate ability to produce sound welds per ASME Section IX
- Test: Weld test coupon, destructive test (bend test)
- Qualification valid: 6 months if welder has not performed welding in the qualified process; indefinite if welder welds at least quarterly in the process
- Requalification required if welder produces defective weld

Welding Processes:

GTAW (Gas Tungsten Arc Welding, TIG):
- Tungsten electrode, inert gas shield (argon or argon-helium)
- Used for root pass on stainless steel, duplex, high-alloy piping
- Excellent quality, slow, high skill requirement
- Preheat typically not required

SMAW (Shielded Metal Arc Welding, Stick):
- Consumable electrode with flux coating
- Most common for carbon steel piping fill/cap passes
- E7018 electrode typical for A106 Grade B pipe
- Preheat required if thickness >0.75" or carbon equivalent high

FCAW (Flux-Cored Arc Welding):
- Tubular electrode with flux core
- Higher deposition rate than SMAW
- Good for thick-wall pipe

SAW (Submerged Arc Welding):
- Automatic process, electrode feeds under blanket of granular flux
- High deposition rate
- Used for large-diameter pipeline construction (spiral or longitudinal seam)

Preheat and Interpass Temperature:

Carbon Steel (A106, A53, API 5L):
- Preheat 200-400°F if:
  * Wall thickness >0.75"
  * Carbon content >0.30%
  * Cold ambient temperature (<32°F)
- Purpose: Slow cooling rate, reduce hardness, prevent cracking

Stainless Steel (A312):
- Preheat generally NOT required (austenitic stainless not hardenable)
- Interpass temp <350°F to minimize carbide precipitation (sensitization)

Duplex Stainless (A790):
- Preheat NOT required
- Interpass temp 300°F max to maintain austenite-ferrite balance
- Nitrogen shielding gas required (maintain nitrogen content)

Post-Weld Heat Treatment (PWHT):

Carbon Steel:
- Required if thickness >1.25" (per B31.3 Para 331)
- PWHT temperature: 1100-1200°F hold time 1 hr/inch thickness minimum
- Purpose: Relieve residual stress, temper hard microstructure

Stainless Steel / Duplex:
- PWHT generally NOT required
- Exception: Solution anneal + quench if welding caused sensitization

Weld Examination:

Visual Examination (VT):
- 100% of all welds
- Per ASME Section V Article 9
- Acceptance: ASME B31.3 Para 341.3.2 (no cracks, complete fusion, uniform appearance)

Radiographic Examination (RT):
- Random (5-10%) or 100% depending on service
- ASME Section V Article 2
- Acceptance: ASME B31.3 Para 341.3.3

Ultrasonic Examination (UT):
- Alternative to RT for thick-wall pipe
- ASME Section V Article 4 or 5

Liquid Penetrant (PT) or Magnetic Particle (MT):
- Surface examination for austenitic stainless (PT) or ferritic steel (MT)
- Used when RT not feasible

When 100% Examination Required:
- Category D fluid service (ASME B31.3 Table 341.3.2) - most flammable/toxic services
- High-pressure (>1500 psi)
- Owner specification
        """,
        key_factors=[
            "WPS qualification and PQR documentation",
            "Welder qualification per ASME Section IX",
            "Welding process selection (GTAW, SMAW, FCAW, SAW)",
            "Preheat requirements (thickness, carbon content, temperature)",
            "Post-weld heat treatment (carbon steel >1.25\" wall)",
            "Weld examination (visual, RT, UT, PT, MT)",
            "Fluid service category (determines examination extent)"
        ],
        primary_authority=[
            "ASME B31.3 Chapter VI - Welding",
            "ASME Section IX - Welding and Brazing Qualifications",
            "ASME Section V - Nondestructive Examination",
            "AWS D1.1 - Structural Welding Code (supplemental)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Welding requirements per code-mandated qualification and testing procedures.",
        controlling_precedent="ASME B31.3 Para 328 - Welding",
        issue_categories=[IssueCategory.WELDING, IssueCategory.CODE_COMPLIANCE]
    ),

    DoctrineBlock(
        topic="Two-Phase Flow in Pipelines - Flow Regimes and Baker Chart",
        keywords=["two-phase flow", "Baker chart", "slug flow", "annular flow", "stratified flow", "flow regime"],
        conclusion_template=[
            "Two-phase flow (gas-liquid) exhibits different flow regimes: bubble, slug, stratified, wavy, annular, mist.",
            "Baker chart predicts flow regime based on gas and liquid velocities; regime affects pressure drop and erosion.",
            "Slug flow causes severe vibration and pressure pulsations; must be avoided in sensitive systems or mitigated with slug catchers."
        ],
        reasoning_framework="""
Two-Phase Flow Regimes:

Flow Patterns in Horizontal Pipes:

1. Stratified Flow (Smooth):
- Gas flows over liquid layer
- Low gas and liquid velocities
- Gravitational separation
- Lowest pressure drop regime

2. Wavy Stratified Flow:
- Gas velocity sufficient to create waves on liquid surface
- Intermediate velocities
- Still separated by gravity

3. Slug Flow (Intermittent):
- Liquid forms plugs (slugs) separated by gas pockets
- Most common in oil/gas pipelines
- Severe vibration, high pressure drop, erosion risk
- Slug catcher required to separate before entering equipment

4. Annular Flow:
- Liquid flows as film on pipe wall
- Gas flows at high velocity in center
- High gas velocity, moderate liquid rate
- Risk of liquid carryover

5. Dispersed (Mist) Flow:
- Liquid dispersed as droplets in gas
- Very high gas velocity
- Erosion risk if droplets contain solids

Baker Chart (Flow Regime Map):

Axes:
- X-axis: λ = (ρL/ρG) × (ρG/ρL)^0.5 × (VsL/VsG)
- Y-axis: ψ = (ρG/ρL)^0.5 × (VsG)

Where:
- ρL = liquid density
- ρG = gas density
- VsL = superficial liquid velocity = QL / A
- VsG = superficial gas velocity = QG / A
- QL, QG = volumetric flow rates
- A = pipe cross-sectional area

Flow Regime Prediction:
- Plot λ vs ψ on Baker chart
- Chart divided into regions: stratified, wavy, slug, annular, mist
- Determines expected flow pattern

Pressure Drop in Two-Phase Flow:

Lockhart-Martinelli Correlation:
- Defines two-phase multiplier Φ
- ΔP_TP = Φ² × ΔP_L
- Where ΔP_L = pressure drop if only liquid flowing at total mass rate

Beggs-Brill Correlation (Oil/Gas Pipelines):
- Accounts for pipe inclination (uphill, downhill, horizontal)
- Used in oil/gas production pipelines
- Predicts holdup (fraction of pipe volume occupied by liquid)

Erosional Velocity:

API RP 14E Criterion:
Ve = C / √ρm

Where:
- Ve = erosional velocity (ft/s)
- C = empirical constant (typically 100 for continuous service, 125 for intermittent)
- ρm = gas-liquid mixture density (lb/ft³)

If actual velocity > Ve, erosion risk high (especially with sand or solids)

Slug Flow Mitigation:

Slug Catchers:
- Separator vessel to capture liquid slugs before downstream equipment
- Volume sized to hold largest expected slug
- Gas outlet at top, liquid outlet at bottom

Choking (Flow Restriction):
- Orifice or choke valve to increase upstream pressure
- Stabilizes flow, reduces slug severity
- Trade-off: increased pressure drop

Pipeline Design for Two-Phase:

1. Avoid slug flow if possible (adjust diameter/pressure to move to annular or stratified)
2. If slug flow unavoidable, install slug catcher and pressure relief
3. Size pipe for erosional velocity limit
4. Use flexibility analysis for vibration from slug flow
5. Instrumentation: pressure transmitters to detect slugs
        """,
        key_factors=[
            "Gas and liquid flow rates (superficial velocities)",
            "Fluid densities (gas and liquid)",
            "Flow regime (stratified, slug, annular, mist)",
            "Baker chart prediction",
            "Erosional velocity (API RP 14E)",
            "Slug catcher sizing for slug flow",
            "Pressure drop correlation (Lockhart-Martinelli, Beggs-Brill)"
        ],
        primary_authority=[
            "API RP 14E - Recommended Practice for Design and Installation of Offshore Production Platform Piping Systems",
            "ASME MFC-19M - Safety Standard for Pressure Piping Systems",
            "Beggs, H.D. and Brill, J.P. - Two-Phase Flow in Pipes (SPE)",
            "Baker, O. - Simultaneous Flow of Oil and Gas (Oil & Gas Journal)"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Engineering correlations based on empirical data; requires validation for specific applications.",
        issue_categories=[IssueCategory.TWO_PHASE_FLOW, IssueCategory.HYDRAULICS]
    ),

    DoctrineBlock(
        topic="Pipeline Pigging - Cleaning and Inspection",
        keywords=["pigging", "pig", "inline inspection", "ILI", "smart pig", "cleaning pig", "scraper"],
        conclusion_template=[
            "Pipeline pigs are devices inserted into pipelines to clean, inspect, or perform maintenance without shutting down flow.",
            "Cleaning pigs remove wax, scale, debris; smart pigs (ILI tools) detect corrosion, cracks, geometry anomalies using MFL or UT sensors.",
            "Pig launchers and receivers required; pipeline must be piggable (no unbarred tees, full-bore valves, smooth bends)."
        ],
        reasoning_framework="""
Pipeline Pigging Operations:

Pig Types:

1. Cleaning Pigs (Utility Pigs):
- Foam pig: Low-density polyurethane foam, mild cleaning
- Brush pig: Wire brushes for scale and hard deposits
- Scraper pig: Metal blades for heavy wax or paraffin removal
- Batching pig: Separates product batches in multi-product pipelines
- Purpose: Remove debris, water, wax, scale

2. Gauging Pigs:
- Aluminum or plastic plate pigs
- Detect internal diameter restrictions (dents, buckles)
- Plate sized to fit through minimum acceptable ID
- If pig stuck, indicates geometry problem

3. Smart Pigs (Inline Inspection Tools - ILI):

Magnetic Flux Leakage (MFL):
- Powerful magnets magnetize pipe wall
- Sensors detect flux leakage at corrosion pits or cracks
- Detects: internal/external corrosion, metal loss
- Resolution: 10% wall thickness loss detectable
- Speed: 1-10 mph typical

Ultrasonic Testing (UT):
- UT transducers measure wall thickness directly
- More accurate than MFL (±0.5mm vs ±10% wall)
- Detects: corrosion, erosion, laminations, cracks
- Can measure through coating

Caliper Pig (Geometry):
- Mechanical or electronic arms measure internal diameter
- Detects: dents, ovality, buckles, wrinkles
- Resolution: ±1% diameter

Crack Detection:
- UT shear wave or EMAT (electromagnetic acoustic transducer)
- Detects: stress corrosion cracking (SCC), fatigue cracks, seam weld defects

Pigging Infrastructure:

Pig Launcher:
- Barrel section with access door (closure head)
- Isolation valves (mainline valve, bypass valve, kicker valve)
- Pressure equalization vent
- Pig signaler (detector) at launcher exit

Pig Receiver:
- Similar to launcher but downstream
- Receiver barrel sized to accommodate pig + debris
- Drain valve to remove liquids before opening

Piggable Pipeline Design Requirements:
1. Full-bore ball valves (no reduced port)
2. No unbarred tees (barred tees have deflector plate to guide pig)
3. Bend radius ≥5D (preferably 10D) for ILI tools
4. Reducers: gradual taper, no sudden diameter changes >5%
5. Minimum ID consistent (no restrictions <95% nominal ID)

Pigging Procedure:

1. Loading:
   - Open launcher door
   - Insert pig (check orientation - direction arrow)
   - Close and bolt door
   - Vent air from launcher
   - Open bypass valve to pressurize launcher

2. Launching:
   - Close mainline valve (diverts flow through launcher)
   - Open kicker valve (flow pushes pig into pipeline)
   - Pig passes launcher signaler (magnetic or acoustic detection)
   - Reopen mainline valve, close kicker valve (pig now in transit)

3. Tracking:
   - Monitor pig progress via above-ground signalers spaced along pipeline
   - Calculate pig speed: distance / time between signalers
   - Adjust flow rate if pig too fast (erosion risk) or too slow (stuck risk)

4. Receiving:
   - Pig arrives at receiver, triggers receiver signaler
   - Reduce pressure, isolate receiver barrel
   - Depressurize and drain receiver
   - Open receiver door, remove pig, inspect debris

Pigging Frequency:

Cleaning Pigs:
- Depends on wax deposition rate, water accumulation
- Oil lines: monthly to annually
- Gas lines: annually to every 5 years

Smart Pigs (ILI):
- Regulatory requirement: PHMSA 49 CFR 195.452 (liquids), 49 CFR 192.937 (gas)
- High Consequence Areas (HCA): every 5-10 years
- Non-HCA: every 10-20 years or as integrity management plan requires

Pig Stuck Events:
- Causes: Diameter restriction, debris accumulation, pig damage, paraffin blockage
- Response: Reverse flow to back pig out, cut pipeline to remove pig (last resort)
- Prevention: Run gauging pig first, ensure full-bore valves, regular cleaning
        """,
        key_factors=[
            "Pig type (cleaning, gauging, ILI smart pig)",
            "ILI technology (MFL, UT, caliper, crack detection)",
            "Launcher and receiver infrastructure",
            "Piggable design (full-bore valves, no restrictions, smooth bends)",
            "Pigging frequency (regulatory, operational)",
            "Pig tracking and speed control",
            "Stuck pig prevention and recovery"
        ],
        primary_authority=[
            "API 1160 - Managing System Integrity for Hazardous Liquid Pipelines",
            "ASME B31.4 Chapter IX - Inspection and Testing",
            "49 CFR Part 195.452 - Pipeline Integrity Management (Liquids)",
            "49 CFR Part 192.937 - Integrity Management Program (Gas)",
            "NACE SP0102 - Inline Inspection of Pipelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry practice with regulatory requirements for integrity management.",
        issue_categories=[IssueCategory.INTEGRITY_MANAGEMENT, IssueCategory.CODE_COMPLIANCE]
    ),

    DoctrineBlock(
        topic="Cathodic Protection for Buried Pipelines",
        keywords=["cathodic protection", "CP", "impressed current", "sacrificial anode", "corrosion control", "coating"],
        conclusion_template=[
            "Cathodic protection (CP) prevents external corrosion on buried or submerged steel pipelines by making the pipe cathode of an electrochemical cell.",
            "Two methods: sacrificial anode (galvanic) or impressed current (rectifier-based); impressed current for long pipelines.",
            "CP must achieve -850 mV (copper/copper sulfate reference) potential or 100 mV polarization shift per NACE SP0169."
        ],
        reasoning_framework="""
Cathodic Protection Principles:

Electrochemical Corrosion:
- Steel corrodes when it acts as anode (loses electrons, oxidizes: Fe → Fe²⁺ + 2e⁻)
- Cathode (protected) receives electrons (reduction: O₂ + 2H₂O + 4e⁻ → 4OH⁻)
- CP reverses natural corrosion by forcing entire pipeline to be cathode

Sacrificial Anode (Galvanic) CP:
- Anode material: Magnesium, zinc, or aluminum (more electronegative than steel)
- Anode corrodes, releasing electrons that flow to pipeline
- No external power required
- Applications: Short pipelines, distribution systems, overseas/remote (no power)
- Anode spacing: 100-500 ft depending on soil resistivity

Impressed Current CP (ICCP):
- Rectifier converts AC power to DC
- Positive terminal connected to anode bed (graphite, mixed metal oxide, high silicon cast iron)
- Negative terminal connected to pipeline
- Anode bed: multiple anodes in deep vertical boreholes or horizontal beds
- Applications: Long transmission pipelines, high current demand systems
- Current output: Adjustable via rectifier (0.1 to 100+ amps)

CP Criteria (NACE SP0169):

Negative Potential Criterion:
- Pipe-to-soil potential ≤ -850 mV vs copper/copper sulfate (CSE) reference electrode
- Most common criterion
- Measured with voltmeter: reference electrode on soil surface, wire connected to pipeline test point

100 mV Polarization Shift:
- Pipe potential shifts ≥100 mV negative when CP applied (instant-off vs depolarized)
- Proves CP current is polarizing pipeline
- Requires interrupted current survey (turn off CP briefly, measure decay)

-850 mV with IR Drop Considered:
- Measure potential during CP-on and CP-off (instant off)
- Difference is IR drop (voltage drop in soil resistance)
- Native potential + IR drop correction ≥ -850 mV

Pipeline Coating:

Purpose:
- Reduce CP current demand (coating insulates most of pipeline surface, CP protects holidays/defects)
- Uncoated pipeline requires 10-100× more CP current than coated

Common Coating Systems:
- Fusion Bonded Epoxy (FBE): Factory-applied, 12-16 mils, excellent adhesion
- 3-Layer Polyethylene (3LPE): FBE primer + adhesive + polyethylene, superior mechanical protection
- Coal Tar Enamel: Legacy system, still in use on older lines
- Tape Wrap: Field-applied, lower quality

Coating Resistance:
- High-quality coating: >100,000 ohm-ft²
- Degraded coating: <10,000 ohm-ft²

Stray Current Interference:

AC Interference:
- High-voltage AC power lines near pipeline induce AC voltage on pipeline
- Can cause AC corrosion or shock hazard
- Mitigation: grounding, zinc ribbon, polarization cells

DC Interference:
- Foreign CP systems, DC-electrified railways cause stray DC currents
- Pipe acts as unintended return path
- Current discharge points corrode
- Mitigation: Bonding, isolation, forced drainage

CP System Design:

Current Requirement Calculation:
I = (A × i) / E_c

Where:
- I = total CP current (amps)
- A = pipeline surface area (ft²)
- i = current density (mA/ft²) - typically 0.2-2.0 mA/ft² for coated pipe, 10-50 mA/ft² for bare steel
- E_c = coating efficiency (0.90 to 0.99 for good coating)

Anode Bed Design (ICCP):
- Anode resistance: R_a = ρ / (2πL) × ln(8L/d)
  Where: ρ = soil resistivity (ohm-cm), L = anode length (cm), d = anode diameter (cm)
- Multiple anodes in parallel: R_total = R_single / N (approximately, if widely spaced)

Soil Resistivity:
- Measured with Wenner 4-pin method
- Low resistivity (<1000 ohm-cm): good for galvanic anodes, low ICCP current
- High resistivity (>10,000 ohm-cm): galvanic anodes ineffective, ICCP requires deep anode bed

Monitoring:

Test Stations:
- Permanently installed access points (test lead wire connected to pipeline)
- Spaced 1/4 to 1 mile along pipeline
- Allow pipe-to-soil potential measurement without excavation

Close Interval Potential Survey (CIPS):
- Measure pipe potential every 2.5-5 ft along pipeline
- Identifies coating defects, current shielding, interference
- Annual requirement for high-consequence areas (HCA)

DCVG (Direct Current Voltage Gradient):
- Above-ground survey to locate coating defects
- Two electrodes on soil, measure voltage gradient
- Coating holiday creates voltage gradient peak
        """,
        key_factors=[
            "CP method (sacrificial anode vs impressed current)",
            "Potential criterion (-850 mV CSE or 100 mV shift)",
            "Pipeline coating (type, condition, resistance)",
            "Soil resistivity",
            "Current demand calculation",
            "Anode bed design and spacing",
            "Stray current interference (AC and DC)",
            "Monitoring (test stations, CIPS survey)"
        ],
        primary_authority=[
            "NACE SP0169 - Control of External Corrosion on Underground or Submerged Metallic Piping Systems",
            "ASME B31.4 Para 452 - External Corrosion Control",
            "ASME B31.8 Para 862 - External Corrosion Control",
            "49 CFR Part 192.463 - External Corrosion Control: Cathodic Protection",
            "49 CFR Part 195.571 - What criteria must I use to determine the adequacy of cathodic protection?"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Engineering practice based on electrochemical principles and regulatory standards.",
        controlling_precedent="NACE SP0169 Cathodic Protection Criteria",
        issue_categories=[IssueCategory.CORROSION_PROTECTION, IssueCategory.CODE_COMPLIANCE]
    ),

    DoctrineBlock(
        topic="Pipeline Integrity Management - ASME B31.8S and 49 CFR Part 192",
        keywords=["integrity management", "IMP", "B31.8S", "risk assessment", "HCA", "threat identification", "PHMSA"],
        conclusion_template=[
            "Pipeline Integrity Management Programs (IMP) required by PHMSA for gas transmission pipelines in High Consequence Areas (HCA).",
            "ASME B31.8S defines integrity management process: identify threats, assess risks, select mitigations, measure performance.",
            "Key threats: external corrosion, internal corrosion, SCC, third-party damage, manufacturing defects, equipment failure."
        ],
        reasoning_framework="""
Pipeline Integrity Management per ASME B31.8S and 49 CFR Part 192 Subpart O:

High Consequence Area (HCA) Definition:
- Areas where pipeline failure could have significant impact on people or environment
- Identified Impact Radius (PIR): distance gas could travel after pipeline rupture
- PIR = 0.69 × √(P × D²) where P = MAOP (psi), D = diameter (inches)
- HCA if PIR contains: 20+ buildings, drinking water source, or environmentally sensitive area

Integrity Management Process (8 Steps):

1. Identify High Consequence Areas:
- Use GIS mapping to overlay pipeline with population data, water sources, environmental areas
- Calculate PIR for each segment
- Classify segments: HCA or non-HCA

2. Baseline Assessment Plan:
- Select assessment method: ILI (smart pig), hydrostatic test, or Direct Assessment (DA)
- Prioritize HCA segments by risk
- Baseline assessment required within specified timeframe (50% by year 5, 100% by year 10 from rule effective date)

3. Identify Threats:
- 9 threat categories per ASME B31.8S:
  * Time-dependent: External corrosion, internal corrosion, stress corrosion cracking (SCC)
  * Stable: Manufacturing defects, welding/fabrication defects, equipment
  * Time-independent: Third-party damage (mechanical damage), incorrect operation, weather/outside force

4. Assess Risks:
- Qualitative or quantitative risk assessment
- Risk = Likelihood × Consequence
- Prioritize segments by risk score

5. Identify and Implement Integrity Assessment Methods:

Inline Inspection (ILI):
- MFL for corrosion
- UT for accurate wall thickness
- Caliper for geometry (dents, buckles)
- Crack detection for SCC, seam weld cracks

Hydrostatic Testing:
- Pressure test to 1.5× MAOP (or higher per code)
- Proves pipe can withstand pressure
- Does NOT detect corrosion, coating condition, or slow-growing cracks

Direct Assessment (DA):
- ECDA (External Corrosion Direct Assessment): coating survey, DCVG, CIS, excavations
- ICDA (Internal Corrosion Direct Assessment): flow modeling, excavations, UT measurements
- SCCDA (Stress Corrosion Cracking Direct Assessment): environment assessment, excavations
- Least expensive but requires extensive data collection and excavations

6. Remediation and Repair:
- Criteria: Repair if defect exceeds code allowable (ASME B31.8 Para 864.1, API 1104 Appendix A)
- Methods: Composite wrap, steel sleeve, cut-out and replace
- Timeline: Immediate (leak), 180 days (60%+ wall loss), 1 year (40-60% wall loss), or next reassessment interval

7. Re-assessment Intervals:
- ILI: 7 years typical, 5 years if previous ILI found anomalies
- Hydro test: No specific interval (generally not repeated unless specific threat)
- DA: 10 years maximum (ECDA), 7 years if ICDA found anomalies

8. Performance Monitoring:
- Track: leak history, excavation findings, ILI predicted vs actual, repair effectiveness
- Adjust program based on performance data

Threat-Specific Considerations:

External Corrosion:
- Primary mitigation: Coating + CP
- Assessment: ECDA or ILI (MFL or UT)
- Repair criteria: >80% wall loss = immediate, >40% = scheduled

Internal Corrosion:
- Mitigation: Corrosion inhibitor, gas dehydration (remove water)
- Assessment: ICDA or ILI (UT)
- Threat if: Free water present, CO₂ or H₂S in gas, oxygen ingress

Stress Corrosion Cracking (SCC):
- Causes: High-pH (carbonate-bicarbonate) or near-neutral pH (CO₂)
- Susceptible: Pre-1970 high-strength steel (X52+), specific coating types (tape, asphalt)
- Mitigation: Coating removal + replacement, stress reduction (pressure reduction)
- Assessment: ILI (UT or EMAT crack detection) or SCCDA

Third-Party Damage:
- Leading cause of pipeline failures
- Mitigation: Patrol (aerial or ground), One-Call system (811), public awareness
- Assessment: ILI (caliper, geometry) or excavation
- Immediate threat if dent + gouge or dent + crack

Manufacturing/Construction Defects:
- Seam weld defects (ERW, flash weld), hard spots, laminations
- Assessment: Hydrostatic test (original construction), ILI (crack detection)
- Repair if defect depth >12.5% wall thickness

Regulatory Compliance (PHMSA 49 CFR Part 192 Subpart O):
- All gas transmission operators must have written IMP
- Annual reports to PHMSA
- Performance metrics: leaks per mile, incidents, assessment completion %
- Enforcement: Civil penalties up to $200,000/day for violations
        """,
        key_factors=[
            "High Consequence Area (HCA) identification",
            "Threat identification (9 categories per B31.8S)",
            "Risk assessment (likelihood × consequence)",
            "Assessment method (ILI, hydro test, Direct Assessment)",
            "Reassessment intervals (5-10 years typical)",
            "Remediation criteria (wall loss thresholds)",
            "Performance monitoring and continuous improvement",
            "Regulatory compliance (PHMSA reporting)"
        ],
        primary_authority=[
            "ASME B31.8S - Managing System Integrity of Gas Pipelines",
            "49 CFR Part 192 Subpart O - Gas Transmission Pipeline Integrity Management",
            "API 1160 - Managing System Integrity for Hazardous Liquid Pipelines",
            "NACE SP0204 - Stress Corrosion Cracking Direct Assessment",
            "API 579 - Fitness-for-Service"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Integrity management per federal regulation and industry consensus standards.",
        controlling_precedent="49 CFR Part 192 Subpart O - Integrity Management Requirements",
        issue_categories=[IssueCategory.INTEGRITY_MANAGEMENT, IssueCategory.CODE_COMPLIANCE]
    ),

    DoctrineBlock(
        topic="Oilfield Flowline and Gathering System Design",
        keywords=["flowline", "gathering system", "production header", "separator", "oil well", "gas well", "multiphase"],
        conclusion_template=[
            "Oilfield flowlines transport produced fluids (oil, gas, water) from wellhead to central separator or tank battery.",
            "Gathering systems collect flowlines into larger trunk lines; low-pressure (50-300 psi typical) compared to transmission.",
            "Multiphase flow (oil-gas-water) requires slug flow mitigation, corrosion inhibition, and pigging capability."
        ],
        reasoning_framework="""
Oilfield Production Piping Systems:

Flowline:
- Individual line from wellhead to separation facility
- Length: 50 ft to several miles
- Pressure: Wellhead flowing pressure (100-2000 psi typical, can be higher)
- Size: 2" to 6" typical
- Material: Carbon steel (API 5L Grade B), stainless or duplex if sour (H₂S)
- Burial: Typically buried 3-4 ft below grade
- Code: ASME B31.4 (liquid) or B31.8 (gas), or API RP 1149 (offshore)

Gathering Line:
- Collects multiple flowlines into larger trunk line
- Feeds into central processing facility (CPF) or gas plant
- Pressure: Lower than flowline (50-500 psi), depends on compression/pumping
- Size: 6" to 24" typical
- Design factor: 0.60 to 0.72 (Class 1 or 2 location per B31.4/B31.8)

Production Header/Manifold:
- Piping system at wellsite or tank battery
- Combines production from multiple wells
- Includes: block valves, check valves, pressure gauges, sample points
- Material: Schedule 80 carbon steel typical (higher pressure allowance)

Multiphase Flow Considerations:

Oil-Gas-Water Flow:
- Gas-Oil Ratio (GOR): scf gas per bbl oil, ranges from 100 (dead oil) to 10,000+ (gas condensate)
- Water Cut: % water in total liquid, ranges from 0% (new well) to 95%+ (mature well)
- Flow regime: Typically slug or annular in flowlines (per Baker chart)

Slug Flow Mitigation:
- Slug catcher at inlet to separator (horizontal vessel sized to hold largest slug)
- Pig receiver can double as slug catcher
- Heater (if hydrates risk): indirect-fired or electric line heater

Erosional Velocity:
- API RP 14E: Ve = C/√ρm where C=100 for continuous service
- Sand production: Reduce C to 50-75 to avoid erosion
- Typical flowline velocity: 5-15 ft/s (below erosional limit)

Corrosion Control:

Sweet Corrosion (CO₂):
- Carbonic acid forms: CO₂ + H₂O → H₂CO₃
- Corrosion rate: 5-50 mpy (mils per year) if no inhibitor
- Mitigation: Batch or continuous corrosion inhibitor injection, coating (FBE/3LPE), CRA (corrosion-resistant alloy) piping

Sour Corrosion (H₂S):
- Hydrogen sulfide causes sulfide stress cracking (SSC) in carbon steel
- Threshold: >50 ppm H₂S in gas or 10 ppm in liquid (per NACE MR0175)
- Mitigation: HIC-resistant steel (API 5L PSL 2 with Charpy testing), stainless 316 (if low pressure), duplex 2205 (if high pressure/high Cl⁻)

Oxygen Corrosion:
- Oxygen ingress (tank vents, leaks) causes rapid pitting
- Mitigation: Oxygen scavenger chemical, blanketing gas (nitrogen)

Scale Deposition:
- Calcium carbonate, barium sulfate precipitate as pressure drops
- Mitigation: Scale inhibitor injection

Flowline Sizing:

Liquid Pipeline (Single-Phase Oil):
- Use Darcy-Weisbach or Hazen-Williams
- Typical velocity: 3-8 ft/s
- Pressure drop: 5-20 psi/mile (depends on viscosity, flow rate)

Gas Pipeline (Single-Phase Gas):
- Weymouth, Panhandle, or AGA equation
- Typical velocity: 10-50 ft/s
- Pressure drop: 1-10 psi/mile

Multiphase (Oil-Gas-Water):
- Use multiphase correlation: Beggs-Brill, Hagedorn-Brown, or simulation software (PIPESIM, OLGA)
- More complex due to flow regime transitions, holdup, slip velocity

Pipeline Pigging:

Reasons to Pig Flowlines:
- Remove paraffin (wax) buildup
- Remove water slugs
- Clean before ILI inspection
- Dry line before abandonment

Pig Launcher/Receiver:
- Small barrel-type launchers at wellheads (often 4" or 6" barrel)
- Receiver at separator or tank battery

Pigging Frequency:
- Paraffin removal: Weekly to monthly (depends on wax deposition rate, temperature)
- Water removal: After rainfall or condensation events

Hydrate Prevention:

Hydrate Formation:
- Gas hydrates (ice-like solids) form when gas + water at low temp + high pressure
- Plugs pipeline, prevents flow
- Typical hydrate temp: 40-60°F at 500-1000 psi

Prevention:
- Dehydration (remove water at wellhead with glycol dehydrator)
- Methanol or glycol injection (depresses hydrate formation temperature)
- Insulation + line heater (keep temperature above hydrate point)

Separation Equipment:

Production Separator:
- 2-phase (oil/gas) or 3-phase (oil/gas/water)
- Operates at lower pressure than flowline (pressure drop across choke or control valve)
- Typical pressure: 50-300 psi
- Size: 24" to 72" diameter × 10-20 ft long (horizontal)

Tank Battery:
- Atmospheric storage tanks (14.7 psia)
- Oil flows to stock tank after separator
- Vent gas to flare or vapor recovery unit (VRU)
        """,
        key_factors=[
            "Fluid composition (oil, gas, water, GOR, water cut)",
            "Flowline pressure and temperature",
            "Multiphase flow regime (slug, annular)",
            "Corrosion environment (CO₂, H₂S, O₂)",
            "Erosional velocity (sand production)",
            "Hydrate prevention (temperature, pressure, inhibitor)",
            "Pigging capability and frequency",
            "Pipeline burial depth and routing",
            "Separation equipment (2-phase vs 3-phase separator)"
        ],
        primary_authority=[
            "ASME B31.4 - Pipeline Transportation Systems for Liquid Hydrocarbons",
            "ASME B31.8 - Gas Transmission and Distribution Piping Systems (if gas dominant)",
            "API RP 14E - Design and Installation of Offshore Production Platform Piping Systems",
            "API RP 1149 - Pipeline Variable Uncertainties and Their Effects on Leak Detectability",
            "NACE MR0175/ISO 15156 - Materials for Use in H₂S-Containing Environments"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Oilfield piping design per industry practices and code requirements.",
        issue_categories=[IssueCategory.HYDRAULICS, IssueCategory.TWO_PHASE_FLOW, IssueCategory.CORROSION_PROTECTION]
    ),
]

# ============================================================================
# TELEMETRY & ANALYTICS
# ============================================================================

START_TIME = datetime.now()

TELEMETRY = {
    "queries_processed": 0,
    "doctrines_triggered": defaultdict(int),
    "response_times_ms": [],
    "modes_used": defaultdict(int),
    "errors": []
}

def record_telemetry(mode: ResponseMode, triggered: List[str], latency_ms: float):
    """Record query telemetry"""
    TELEMETRY["queries_processed"] += 1
    TELEMETRY["modes_used"][mode.value] += 1
    TELEMETRY["response_times_ms"].append(latency_ms)
    for doctrine in triggered:
        TELEMETRY["doctrines_triggered"][doctrine] += 1

# ============================================================================
# CORE ENGINE - TIE-20 IMPLEMENTATION
# ============================================================================

def three_layer_response(question: str, mode: ResponseMode) -> Tuple[str, List[str], ConfidenceLevel, List[str]]:
    """
    TIE Gold Standard: Three-layer response architecture
    Layer 1: Doctrine cache (0-50ms)
    Layer 2: Semantic retrieval (50-500ms) - not implemented here (would use Vectorize)
    Layer 3: Deep analysis with LLM - not implemented here (would use Workers AI)
    """
    triggered = []
    reasoning_chain = []

    # Normalize question
    normalized = semantic_normalization(question)

    # Layer 1: Doctrine cache lookup
    for doctrine in DOCTRINE_CACHE:
        if any(kw.lower() in normalized.lower() for kw in doctrine.keywords):
            triggered.append(doctrine.topic)

            if mode == ResponseMode.FAST:
                answer = " ".join(doctrine.conclusion_template)
                reasoning_chain.append(f"Cache hit: {doctrine.topic}")
                return answer, triggered, doctrine.confidence, reasoning_chain
            elif mode == ResponseMode.DEFENSE:
                answer = f"{doctrine.topic}\n\n" + " ".join(doctrine.conclusion_template) + f"\n\nAuthorities: {', '.join(doctrine.primary_authority)}\n\nReasoning:\n{doctrine.reasoning_framework[:500]}..."
                reasoning_chain.append(f"Defense mode: {doctrine.topic}")
                reasoning_chain.extend(doctrine.key_factors[:3])
                return answer, triggered, doctrine.confidence, reasoning_chain
            elif mode == ResponseMode.MEMO:
                answer = multi_doctrine_decomposition(question, [doctrine])
                reasoning_chain.append(f"Memo mode: {doctrine.topic}")
                reasoning_chain.append(doctrine.reasoning_framework[:200])
                return answer, triggered, doctrine.confidence, reasoning_chain

    # No cache hit - fallback response
    answer = f"Question analyzed: {question}. No specific doctrine matched. This question requires deep analysis. Available doctrines cover: {', '.join([d.topic for d in DOCTRINE_CACHE[:5]])}..."
    reasoning_chain.append("No doctrine cache hit - general response")
    return answer, triggered, ConfidenceLevel.DISCLOSURE, reasoning_chain

def semantic_normalization(text: str) -> str:
    """Normalize piping engineering terminology"""
    replacements = {
        "ASME B31.3": "B31.3 process piping",
        "ASME B31.4": "B31.4 pipeline",
        "ASME B31.8": "B31.8 gas pipeline",
        "ASTM A106": "A106 carbon steel seamless",
        "ASTM A312": "A312 stainless steel",
        "welding neck": "RFWN flange",
        "spiral wound": "spiral wound gasket",
        "cathodic protection": "CP corrosion control",
        "inline inspection": "ILI smart pig",
        "two-phase flow": "multiphase flow oil gas",
    }
    normalized = text
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    return normalized

def multi_doctrine_decomposition(question: str, doctrines: List[DoctrineBlock]) -> str:
    """Generate comprehensive memo-style response using multiple doctrines"""
    memo = f"ENGINEERING MEMO - PIPING DESIGN ANALYSIS\n"
    memo += f"Subject: {question}\n"
    memo += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n"
    memo += f"Engine: MECH04 Piping Design & Analysis v1.0.0\n\n"

    for doctrine in doctrines:
        memo += f"## {doctrine.topic}\n\n"
        memo += f"**Conclusion:**\n{' '.join(doctrine.conclusion_template)}\n\n"
        memo += f"**Key Factors:**\n"
        for factor in doctrine.key_factors:
            memo += f"- {factor}\n"
        memo += f"\n**Authorities:**\n"
        for auth in doctrine.primary_authority:
            memo += f"- {auth}\n"
        memo += f"\n**Confidence:** {doctrine.confidence.value}\n"
        memo += f"**Stratification:** {doctrine.confidence_stratification}\n\n"
        memo += "---\n\n"

    return memo

def authority_hardening(doctrines: List[DoctrineBlock]) -> List[str]:
    """Extract and deduplicate authorities from triggered doctrines"""
    authorities = []
    for doctrine in doctrines:
        authorities.extend(doctrine.primary_authority)
    return list(set(authorities))

def determinism_hash(question: str, answer: str) -> str:
    """SHA-256 hash for reproducibility verification"""
    content = f"{question}||{answer}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

# ============================================================================
# FASTAPI ENDPOINTS
# ============================================================================

@APP.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint - TIE Gold Standard implementation"""
    start = datetime.now()

    try:
        answer, triggered, confidence, reasoning = three_layer_response(
            request.question,
            request.mode
        )

        # Get authorities from triggered doctrines
        triggered_doctrines = [d for d in DOCTRINE_CACHE if d.topic in triggered]
        authorities = authority_hardening(triggered_doctrines)

        # Calculate telemetry
        latency_ms = (datetime.now() - start).total_seconds() * 1000
        record_telemetry(request.mode, triggered, latency_ms)

        # Generate determinism hash
        det_hash = determinism_hash(request.question, answer)

        telemetry = {
            "latency_ms": latency_ms,
            "doctrines_triggered": len(triggered),
            "mode": request.mode.value
        }

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            authorities=authorities,
            reasoning_chain=reasoning,
            triggered_doctrines=triggered,
            mode=request.mode,
            determinism_hash=det_hash,
            telemetry=telemetry
        )

    except Exception as e:
        logger.error(f"Query failed: {e}")
        TELEMETRY["errors"].append(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/health", response_model=HealthResponse)
async def health_check():
    """Health endpoint - comprehensive status"""
    uptime = (datetime.now() - START_TIME).total_seconds()

    return HealthResponse(
        status="operational",
        engine="MECH04_piping_design",
        version="1.0.0",
        port=9044,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=uptime
    )

@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total_doctrines": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "categories": [c.value for c in d.issue_categories],
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }

@APP.get("/telemetry")
async def get_telemetry():
    """Get engine telemetry and performance metrics"""
    avg_latency = sum(TELEMETRY["response_times_ms"]) / len(TELEMETRY["response_times_ms"]) if TELEMETRY["response_times_ms"] else 0

    return {
        "queries_processed": TELEMETRY["queries_processed"],
        "avg_latency_ms": avg_latency,
        "modes_used": dict(TELEMETRY["modes_used"]),
        "top_doctrines": dict(sorted(TELEMETRY["doctrines_triggered"].items(), key=lambda x: x[1], reverse=True)[:10]),
        "errors": TELEMETRY["errors"],
        "uptime_seconds": (datetime.now() - START_TIME).total_seconds()
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info(f"MECH04 Piping Design Engine v1.0.0 starting on port 9044")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    logger.info(f"TIE-20 components: three_layer_response, response_modes, doctrine_cache, authority_hardening, confidence_stratification, semantic_normalization, telemetry, determinism_hash")

    uvicorn.run(
        APP,
        host="0.0.0.0",
        port=9044,
        log_level="info"
    )
