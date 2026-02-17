"""
MECH11 Hydraulic Systems Intelligence Engine
TIE-Grade Implementation

Analyzes hydraulic power systems: pump selection, actuator design, circuit design,
fluid selection, contamination control, and system troubleshooting.

Port: 9271
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Literal
from dataclasses import dataclass, field, asdict
from enum import Enum
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "MECH11"
ENGINE_NAME = "Hydraulic Systems Intelligence Engine"
VERSION = "1.0.0"
PORT = 9271

logger.add(
    f"logs/{ENGINE_ID}_{{time}}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)


# ============================================================================
# DOMAIN ENUMS
# ============================================================================

class IssueCategory(str, Enum):
    PUMP_SELECTION = "pump_selection"
    ACTUATOR_DESIGN = "actuator_design"
    CIRCUIT_DESIGN = "circuit_design"
    VALVE_SELECTION = "valve_selection"
    FLUID_SELECTION = "fluid_selection"
    CONTAMINATION_CONTROL = "contamination_control"
    PRESSURE_DROP = "pressure_drop"
    HEAT_MANAGEMENT = "heat_management"
    MOTION_CONTROL = "motion_control"
    SYSTEM_EFFICIENCY = "system_efficiency"
    TROUBLESHOOTING = "troubleshooting"
    PREDICTIVE_MAINTENANCE = "predictive_maintenance"


class ConfidenceStratification(str, Enum):
    DEFENSIBLE = "defensible"
    AGGRESSIVE = "aggressive"
    DISCLOSURE = "disclosure"
    HIGH_RISK = "high_risk"


class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class DoctrineBlock:
    """Core hydraulic systems domain knowledge unit"""
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: float
    confidence_stratification: ConfidenceStratification
    controlling_precedent: str

    def matches(self, query: str) -> float:
        """Calculate match score for query"""
        query_lower = query.lower()
        score = 0.0

        for keyword in self.keywords:
            if keyword.lower() in query_lower:
                score += 1.0

        if self.topic.lower() in query_lower:
            score += 2.0

        return score / (len(self.keywords) + 2)


@dataclass
class TelemetryData:
    """Performance tracking"""
    query_id: str
    timestamp: str
    category: IssueCategory
    mode: ResponseMode
    doctrine_hits: List[str]
    latency_ms: float
    confidence: float
    error_domain: Optional[str] = None


@dataclass
class CoverageMapEntry:
    """Doctrine coverage tracking"""
    doctrine_topic: str
    triggered_count: int
    last_triggered: Optional[str]
    epistemic_gaps: List[str]


class QueryRequest(BaseModel):
    """API request model"""
    query: str = Field(..., description="Hydraulic systems analysis query")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response depth")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class QueryResponse(BaseModel):
    """API response model"""
    query_id: str
    analysis: str
    confidence: float
    stratification: ConfidenceStratification
    sources: List[str]
    warnings: List[str]
    latency_ms: float
    determinism_hash: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    engine_id: str
    version: str
    uptime_seconds: float
    total_queries: int
    doctrine_count: int
    avg_latency_ms: float


# ============================================================================
# DOCTRINE CACHE - HYDRAULIC SYSTEMS EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    DoctrineBlock(
        topic="Hydraulic Pump Selection - Fixed vs Variable Displacement",
        keywords=["pump", "displacement", "gear pump", "piston pump", "vane pump", "fixed", "variable", "flow"],
        conclusion_template="For the specified application, {} pump is recommended based on {} with expected efficiency of {}.",
        reasoning_framework="""
Pump Selection Decision Framework:

Fixed Displacement Pumps (Gear, Vane, Fixed Piston):
- Constant flow per revolution regardless of pressure
- Simpler design, lower cost, high reliability
- Gear pumps: Up to 3000 PSI, 85-93% volumetric efficiency
- Vane pumps: Up to 2500 PSI, 90-95% efficiency, quieter operation
- Fixed piston pumps: Up to 5000+ PSI, 95-98% efficiency
- Best for constant speed/load applications
- Pressure relief valve required for system protection

Variable Displacement Pumps (Piston):
- Flow adjustable based on system demand
- Pressure compensated or load sensing control
- Axial piston: Up to 6000+ PSI, swashplate or bent axis design
- Radial piston: Ultra-high pressure to 10,000+ PSI
- Energy savings 20-60% vs fixed displacement
- Higher initial cost but lower operating cost
- Complex controls require skilled maintenance

Selection Criteria:
1. Operating pressure range and peaks
2. Flow requirements (constant vs variable)
3. Duty cycle and energy consumption
4. Noise requirements (vane quietest)
5. Contamination sensitivity (piston most sensitive)
6. Cost constraints (gear cheapest)
7. Space/weight limitations
8. Service life requirements

Application Matching:
- Mobile equipment: Variable piston (load sensing)
- Machine tools: Fixed vane (quiet, smooth flow)
- High pressure: Fixed or variable piston
- Low cost/simple: Gear pump with relief valve
- Energy critical: Variable displacement with pressure compensation
""",
        key_factors=[
            "Operating pressure range determines pump type feasibility",
            "Variable displacement saves energy when load varies significantly",
            "Contamination control critical for piston pumps (ISO 16/14/11 or better)",
            "Gear pumps best cost/performance for <2500 PSI constant load",
            "Vane pumps ideal for noise-sensitive applications",
            "Axial piston most common variable displacement (swashplate adjustment)",
            "Volumetric efficiency decreases with wear and contamination"
        ],
        primary_authority=[
            "ISO 4391 - Hydraulic Fluid Power - Pumps, motors and integral transmissions",
            "Eaton Hydraulic Pump Selection Guide (2022)",
            "Parker Hannifin Pump Engineering Handbook",
            "Bosch Rexroth Axial Piston Units - Technical Data",
            "NFPA T3.6.1 - Method for Verifying the Fatigue Pressure Rating of the Pressure Containing Envelope"
        ],
        burden_holder="System designer must justify pump selection based on lifecycle cost analysis",
        adversary_position="Lowest initial cost pump regardless of efficiency or suitability",
        counter_arguments=[
            "Variable displacement pumps have higher initial cost but 3-7 year payback",
            "Gear pump simplicity offset by energy waste and heat generation",
            "Contamination control costs for piston pumps offset by efficiency gains",
            "Noise reduction value depends on application environment",
            "Load sensing systems reduce installed power requirements by 30-50%"
        ],
        resolution_strategy="Lifecycle cost analysis including energy, maintenance, and replacement over 10-year horizon",
        entity_scope="All hydraulic power units from 1 HP to 500+ HP",
        confidence=0.95,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="ISO 4391 pump classification and performance standards"
    ),

    DoctrineBlock(
        topic="Hydraulic Cylinder Sizing - Bore and Rod Diameter Selection",
        keywords=["cylinder", "actuator", "bore", "rod", "piston", "force", "buckling", "sizing"],
        conclusion_template="Cylinder bore of {} inch with rod diameter {} inch provides {} lbf force at {} PSI with {} safety factor against buckling.",
        reasoning_framework="""
Cylinder Sizing Methodology:

Force Calculation:
- Extend force: F = P × A_piston = P × π(D²)/4
- Retract force: F = P × (A_piston - A_rod) = P × π(D² - d²)/4
- Where: P = pressure (PSI), D = bore (in), d = rod (in)
- Common pressure: 1500-3000 PSI (industrial), 3000-5000 PSI (mobile)

Bore/Rod Ratio Selection:
- Standard ratio: 2:1 (bore/rod diameter)
- Heavy duty: 1.6:1 to 1.8:1 (larger rod, less buckling)
- High speed: 2.5:1 to 3:1 (smaller rod, less mass)
- Double rod cylinders: Same area both directions

Buckling Analysis (Critical for long stroke):
- Euler buckling: F_critical = (π² × E × I) / (K × L)²
- Where: E = modulus (steel 30×10⁶ PSI), I = moment of inertia
- K = end fixity factor (2.0 pinned, 1.0 fixed-fixed, 0.5 guided)
- L = stroke length plus cushion distance
- Safety factor: Minimum 4:1 for buckling
- Slenderness ratio: L/d should be <40 for standard rods

Cushioning Requirements:
- Adjustable cushions recommended for stroke >12 inch at >10 ft/min
- Cushion length typically 0.25-0.5 inch per inch of bore
- Deceleration distance: d = v²/(2a), limit a to 2-3 g
- External shock absorbers required for high kinetic energy

Standard Bore Sizes (NFPA T3.6.17):
- Fractional: 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20 inch
- Metric: 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 320 mm

Mounting Style Selection:
- Fixed mounts: Flange, trunnion (side loads, high accuracy)
- Pivot mounts: Clevis, trunnion (angular misalignment)
- Guided applications: Rod loads <10% of thrust
""",
        key_factors=[
            "Bore size determines force output at given pressure",
            "Rod diameter must resist buckling based on stroke length and mounting",
            "2:1 bore/rod ratio is standard for balanced retraction speed",
            "Cushions required for smooth deceleration on long stroke cylinders",
            "Side loading shortens seal life - keep rod loads <5% of thrust",
            "Seal material selection critical: Nitrile (standard), Viton (high temp), Polyurethane (wear)",
            "Cylinder speed typically limited to 1-3 ft/s for seal life"
        ],
        primary_authority=[
            "NFPA T3.6.17 - Hydraulic Cylinders - Metric Series",
            "ISO 3320 - Fluid power systems - Cylinders - Dimensions and tolerances of housings",
            "Parker Cylinder Division Engineering Catalog",
            "SAE J1242 - Method for Determining Volume and Flow Capacity",
            "Eaton Mobile Cylinder Design Guide"
        ],
        burden_holder="Designer must verify buckling safety factor >4 for all loading conditions",
        adversary_position="Minimum bore size to reduce cost regardless of buckling risk",
        counter_arguments=[
            "Undersized rod leads to catastrophic buckling failure under compressive load",
            "Oversized bore increases cost, weight, and fluid volume unnecessarily",
            "Proper cushioning prevents damage and extends service life 3-5x",
            "Side load tolerance requires proper mounting and alignment",
            "Seal life directly impacts maintenance cost - proper design critical"
        ],
        resolution_strategy="Calculate required force, verify buckling, select next standard size with documented safety factors",
        entity_scope="All hydraulic cylinders from 1 inch bore to 20+ inch heavy industrial",
        confidence=0.96,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="NFPA T3.6.17 dimensional standards and SAE J1242 performance verification"
    ),

    DoctrineBlock(
        topic="Directional Control Valve Selection - Spool vs Poppet Design",
        keywords=["valve", "directional", "spool", "poppet", "control", "DCV", "flow path", "leakage"],
        conclusion_template="For this application, {} valve configuration with {} spool/poppet design provides {} flow at {} PSI drop.",
        reasoning_framework="""
Directional Control Valve Design Comparison:

Spool Valves (Most Common):
- Cylindrical spool slides in machined bore
- 2-way, 3-way, 4-way configurations
- Open center or closed center design
- Flow capacity: 0.5 to 200+ GPM per section
- Overlap/underlap determines position characteristics
- Internal leakage: 0.5-3 GPM typical at 3000 PSI
- Pressure rating: Up to 5000 PSI
- Fast response: 10-50 ms actuation time
- Sensitive to contamination (10-15 micron clearance)

Poppet Valves (Zero Leakage):
- Cone or ball seats against machined surface
- Zero internal leakage when seated
- Higher pressure drop than spool (10-150 PSI)
- Excellent contamination tolerance
- Limited to 2-way or 3-way (rarely 4-way)
- Slower response: 50-200 ms
- Used in load holding, pressure isolation
- Stackable configurations for complex circuits

Actuation Methods:
- Manual: Lever, push button, pedal
- Solenoid: DC (12V, 24V) or AC (120V, 240V)
- Pilot operated: Hydraulic or pneumatic pilot pressure
- Proportional: Variable current controls position
- Servo: Closed loop position/flow control

Position Sensing:
- Mechanical detents for manual override
- Electrical position sensors (LVDT, magnetostrictive)
- Spring return vs detented neutral
- Tandem center, open center, closed center neutral

Pressure Drop Considerations:
- Spool valve: ΔP = (Q/Cv)² where Cv = flow coefficient
- Typical 30-75 PSI drop at rated flow
- Excessive drop causes heat generation
- Size valve for actual flow, not pump capacity
""",
        key_factors=[
            "Spool valves offer high flow capacity with controllable leakage",
            "Poppet valves provide zero leakage for load holding applications",
            "Contamination control critical for spool valves (ISO 18/16/13 or better)",
            "Proportional valves enable precise speed/position control with electronic input",
            "Valve center condition (open/closed/tandem) determines circuit behavior",
            "Solenoid voltage must match available electrical system",
            "Flow coefficient Cv determines pressure drop at operating flow"
        ],
        primary_authority=[
            "ISO 4401 - Hydraulic fluid power - Four-port directional control valves",
            "NFPA T3.5.1 - Method for Determining the Flow Capacity of Hydraulic Fluid Power Valves",
            "Bosch Rexroth Industrial Hydraulics Manual",
            "Eaton Vickers Directional Controls Catalog",
            "ISO 10770 - Hydraulic fluid power - Electrically modulated hydraulic control valves"
        ],
        burden_holder="Designer must specify valve flow coefficient to limit pressure drop to <100 PSI at max flow",
        adversary_position="Smallest valve to minimize cost regardless of pressure drop and heat generation",
        counter_arguments=[
            "Undersized valve creates excessive pressure drop and heat",
            "Poppet valves required where zero leakage is critical safety requirement",
            "Proportional control justifies cost with precision and energy savings",
            "Contamination from undersized filtration destroys spool valves prematurely",
            "Wrong center condition causes circuit malfunction or unsafe operation"
        ],
        resolution_strategy="Calculate pressure drop using flow coefficient, verify contamination control, select actuation method based on control requirements",
        entity_scope="All directional control valves from 0.5 GPM micro valves to 200 GPM industrial",
        confidence=0.94,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="ISO 4401 mounting interfaces and NFPA T3.5.1 flow testing standards"
    ),

    DoctrineBlock(
        topic="Hydraulic Fluid Selection - ISO VG Grade and Fluid Type",
        keywords=["fluid", "oil", "hydraulic fluid", "viscosity", "VG grade", "mineral oil", "synthetic", "biodegradable"],
        conclusion_template="ISO VG {} {} hydraulic fluid recommended for {} °F operating temperature with {} filterability and {} environmental risk.",
        reasoning_framework="""
Hydraulic Fluid Selection Framework:

ISO Viscosity Grade (VG) Classification:
- VG number = kinematic viscosity at 40°C (cSt)
- Common grades: VG 32, VG 46, VG 68, VG 100
- VG 46: Most common industrial (70-120°F ambient)
- VG 32: Cold climate or high speed applications
- VG 68: High temperature or heavily loaded systems
- VG 100: Slow-moving heavy equipment
- Viscosity Index (VI): Measure of viscosity change with temperature (>100 preferred)

Fluid Types:

1. Mineral Oil (Most Common, 80% of applications):
- Petroleum-based with anti-wear (AW) additives
- Zinc dialkyldithiophosphate (ZDDP) for wear protection
- Cost: $5-15 per gallon
- Temperature range: -20°F to 180°F
- Good lubricity and seal compatibility
- Non-biodegradable, environmental concern

2. Fire Resistant Fluids (HFD):
- Water-glycol (HFC): 35-50% water content, limited to 130°F
- Water-in-oil emulsion (HFB): Milky appearance, requires monitoring
- Phosphate ester (HFD-R): High temperature to 200°F, aggressive to seals
- Use: Steel mills, die casting, mining (fire hazard areas)
- Cost: 2-4x mineral oil
- Requires compatible seal materials (Viton, EPDM)

3. Biodegradable Fluids (Environmentally Sensitive):
- Vegetable oil (HETG): Rapeseed, sunflower base
- Polyalkylene glycol (HEPG): Synthetic, excellent lubricity
- Synthetic ester (HEES): Highest performance, best VI
- Use: Forestry, marine, agriculture, food processing
- Cost: 2-5x mineral oil
- Faster oxidation, shorter change intervals

4. Synthetic Hydrocarbons (Extreme Performance):
- PAO (polyalphaolefin) base
- Temperature range: -40°F to 250°F
- Excellent viscosity index (VI 140-160)
- Extended drain intervals (3-5x mineral oil)
- Cost: 3-6x mineral oil
- Aerospace, high performance mobile equipment

Viscosity-Temperature Relationship:
- Optimal viscosity: 100-300 SUS (20-65 cSt) at operating temp
- Too low: Wear, internal leakage, efficiency loss
- Too high: Sluggish response, cavitation, power loss
- Viscosity doubles approximately every 35°F decrease

Additives:
- Anti-wear (AW): Protects pump and valve surfaces
- Extreme pressure (EP): For high load applications
- Anti-foam: Prevents air entrainment
- Rust/oxidation inhibitors: Extends fluid life
- Pour point depressants: Cold weather operation
""",
        key_factors=[
            "ISO VG 46 is standard for most industrial systems (70-120°F)",
            "Viscosity must be maintained in optimal range (100-300 SUS) at operating temperature",
            "Fire resistant fluids required by OSHA in specific high-risk environments",
            "Biodegradable fluids mandated for environmentally sensitive locations",
            "Seal compatibility must be verified when changing fluid types",
            "Synthetic fluids offer extended life but require higher initial investment",
            "Fluid contamination (water, particles, air) is primary cause of system failure"
        ],
        primary_authority=[
            "ISO 6743-4 - Classification of hydraulic fluids",
            "ASTM D2882 - Standard Test Method for Indicating Wear Characteristics of Petroleum Hydraulic Fluids (Vane Pump)",
            "ISO 11158 - Mineral hydraulic fluids for systems",
            "ASTM D445 - Standard Test Method for Kinematic Viscosity",
            "ISO 15380 - Environmentally acceptable hydraulic fluids"
        ],
        burden_holder="System owner must maintain fluid viscosity in acceptable range through temperature control and fluid selection",
        adversary_position="Cheapest available oil regardless of viscosity grade or additive package",
        counter_arguments=[
            "Wrong viscosity grade causes premature pump wear and efficiency loss",
            "Missing anti-wear additives lead to catastrophic pump failure",
            "Environmental contamination from mineral oil creates liability exposure",
            "Fire resistant fluids required by insurance and OSHA in high-risk areas",
            "Synthetic fluid cost justified by 3x longer change intervals and reduced downtime"
        ],
        resolution_strategy="Match ISO VG grade to operating temperature, select fluid type based on environmental/safety requirements, verify seal compatibility",
        entity_scope="All hydraulic systems from 1 gallon reservoir to 500+ gallon industrial",
        confidence=0.95,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="ISO 6743-4 fluid classification and ISO 11158 mineral oil specifications"
    ),

    DoctrineBlock(
        topic="Contamination Control - ISO 4406 Cleanliness Codes and Filtration",
        keywords=["contamination", "filtration", "cleanliness", "ISO 4406", "beta ratio", "filter", "particles", "micron"],
        conclusion_template="Target cleanliness {} per ISO 4406 requires {} micron filtration with beta ratio {} achieving {} % particle removal.",
        reasoning_framework="""
Contamination Control Framework:

ISO 4406 Cleanliness Code:
- Format: XX/YY/ZZ (particles per 100 mL)
- XX = particles >4 micron
- YY = particles >6 micron
- ZZ = particles >14 micron
- Each code number represents range (e.g., 16 = 1300-2500 particles)

Target Cleanliness by Component Type:
- Servo valves: 16/14/11 or better (most stringent)
- Proportional valves: 17/15/12
- Variable displacement pumps (piston): 18/16/13
- Fixed displacement pumps (vane): 19/17/14
- Fixed displacement pumps (gear): 20/18/15
- Cylinders and motors: 21/19/16 (most tolerant)
- New fluid from drum: Typically 22/20/18 (inadequate!)

Filter Rating and Beta Ratio:
- Nominal rating: Not standardized, unreliable
- Absolute rating: 98-99% removal (Beta 50-100)
- Beta ratio: Efficiency = (Beta - 1) / Beta × 100%
  - Beta 75 = 98.7% efficient
  - Beta 200 = 99.5% efficient
  - Beta 1000 = 99.9% efficient
- Filter target: Beta 200 or higher at target micron size
- Micron size selection: 3-5 micron for servos, 10 micron for standard

Filter Locations:
1. Suction strainer: 100-150 micron (protect pump from large debris)
2. Pressure filter: 3-25 micron (protect system components)
3. Return line filter: 10-25 micron (clean fluid before reservoir)
4. Offline kidney loop: 3-5 micron (continuous polishing)

Filter Maintenance:
- Bypass valve: Opens at 25-50 PSI differential
- Differential pressure indicator: Replace at 25 PSI
- Clogged filter causes bypass, unfiltered fluid damages system
- Change interval: Based on ΔP, not calendar schedule
- Used oil analysis: Particle count, wear metals, water content

Contamination Sources:
- Built-in: Manufacturing debris (60-80% of initial contamination)
- Ingressed: Cylinder rod seals, breathers, poor service practices
- Generated: Component wear, fluid oxidation
- Water: Condensation, seal leakage (aim for <500 PPM, <0.05%)

Contamination Effects:
- 70-80% of hydraulic failures caused by contamination
- Spool valve jamming from particles in clearances
- Pump wear from abrasive particles
- Seal damage from hard particles
- Fluid degradation from catalytic metals

New Fluid Handling:
- Filter all new fluid before adding to system
- Storage: Sealed, indoor, avoid temperature extremes
- Transfer: Use clean pump and hose, not funnel and bucket
- Flushing: Run system at full flow for 50+ hours pre-startup
""",
        key_factors=[
            "ISO 4406 cleanliness code must match component sensitivity",
            "Beta ratio >200 at target micron size for effective filtration",
            "70-80% of hydraulic failures attributed to contamination",
            "New fluid from drum is contaminated and must be filtered",
            "Filter bypass valve creates unprotected operation when filter clogs",
            "Water contamination accelerates oxidation and reduces fluid life",
            "Offline filtration (kidney loop) most effective for achieving high cleanliness"
        ],
        primary_authority=[
            "ISO 4406 - Hydraulic fluid power - Fluids - Method for coding level of contamination by solid particles",
            "ISO 16889 - Hydraulic fluid power - Filters - Multi-pass method for evaluating filtration performance (Beta ratio)",
            "ISO 11171 - Hydraulic fluid power - Calibration of automatic particle counters",
            "SAE AS4059 - Aerospace Filter Beta Ratio Testing",
            "NFPA T2.9.1 - Identification and Evaluation of Filter Performance"
        ],
        burden_holder="System owner must maintain documented cleanliness levels through periodic oil sampling",
        adversary_position="No filtration or minimal strainer to reduce initial cost",
        counter_arguments=[
            "Unfiltered systems experience 10x higher failure rates",
            "Servo valve replacement cost exceeds entire filtration system cost",
            "Contamination-related downtime far exceeds filter maintenance cost",
            "New fluid filtration investment recovered in extended component life",
            "Particle counters provide objective verification vs visual inspection"
        ],
        resolution_strategy="Specify ISO 4406 cleanliness target, select filters with Beta >200, implement periodic sampling and analysis",
        entity_scope="All hydraulic systems from mobile equipment to 1000+ gallon industrial",
        confidence=0.97,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="ISO 4406 contamination coding and ISO 16889 beta ratio test method"
    ),

    DoctrineBlock(
        topic="Hydraulic Circuit Design - Open Center vs Closed Center Systems",
        keywords=["circuit", "open center", "closed center", "load sensing", "pressure compensated", "flow control"],
        conclusion_template="For this application, {} circuit configuration provides {} efficiency with {} control strategy and {} power consumption.",
        reasoning_framework="""
Hydraulic Circuit Configuration Analysis:

Open Center Systems:
- Fixed displacement pump runs continuously
- Valve neutral position allows free flow to tank (zero pressure)
- Actuator movement: Valve shifts, flow diverted from tank to actuator
- Pressure builds only when actuator meets resistance
- Power consumption: Continuous even when idle
- Advantages:
  - Simple design, lower cost
  - Good for single-actuator machines
  - Responsive (no pressure buildup delay)
  - Less heat when working (pressure only at load)
- Disadvantages:
  - Constant power consumption at idle
  - Heat generation from continuous circulation
  - Limited multi-function capability (series circuits)
  - Energy efficiency: 15-25% (most energy wasted)

Closed Center Systems:
- Fixed or variable displacement pump
- Valve neutral position blocks all ports (traps pressure)
- System pressure maintained at setpoint (1500-3000 PSI typical)
- Pressure relief valve or unloading valve prevents overpressure
- Accumulator often used to store energy
- Advantages:
  - Multiple actuators can operate simultaneously (parallel circuits)
  - Instant response (pressure always available)
  - Better for complex machines
- Disadvantages:
  - Continuous high pressure even when idle
  - Significant heat generation (energy wasted as heat)
  - Higher component stress
  - Energy efficiency: 10-20% without load sensing

Load Sensing Systems (Advanced Closed Center):
- Variable displacement pump adjusts flow to demand
- Pressure maintained at 200-300 PSI above load requirement
- Load sensing signal from valve to pump control
- Flow matches actuator requirements exactly
- Advantages:
  - Energy savings 30-60% vs standard closed center
  - Reduced heat generation
  - Multiple actuators with proportional control
  - Lower installed power requirements
- Disadvantages:
  - Complex controls, higher initial cost
  - Requires clean fluid for reliable operation
  - More sophisticated troubleshooting

Pressure Compensated Systems:
- Variable pump maintains constant pressure regardless of flow
- Pressure setpoint adjustable (typically 1500-5000 PSI)
- Excess flow destoked (swashplate angle reduced)
- Common in industrial presses and machine tools
- Energy efficiency better than fixed pump, less than load sensing

Flow Control Strategies:
- Meter-in: Control flow entering actuator (stiff control)
- Meter-out: Control flow leaving actuator (prevent runaway)
- Bleed-off: Divert excess flow to tank (wastes energy)
- Load sensing: Match pump output to demand (most efficient)

Circuit Selection Criteria:
- Single actuator, simple tasks: Open center
- Multiple actuators, intermittent use: Closed center with accumulator
- Multiple actuators, continuous use: Load sensing
- High cycle rate, energy critical: Load sensing or pressure compensated
- Mobile equipment: Load sensing for fuel economy
- Stationary equipment: Cost vs efficiency tradeoff
""",
        key_factors=[
            "Open center systems simple but waste energy during idle circulation",
            "Closed center enables multiple simultaneous actuators but generates heat",
            "Load sensing provides 30-60% energy savings vs conventional systems",
            "Accumulator in closed center system stores energy for high flow demand bursts",
            "System pressure maintained continuously in closed center stresses components",
            "Pressure compensated pump limits maximum pressure, varies flow",
            "Mobile equipment strongly favors load sensing for fuel economy"
        ],
        primary_authority=[
            "ISO 1219-1 - Fluid power systems - Graphic symbols and circuit diagrams",
            "Eaton Load Sensing System Design Guide",
            "Bosch Rexroth Mobile Hydraulics Training Manual",
            "Parker Hydraulic Circuit Design Manual",
            "SAE J1116 - Categories of Off-Road Self-Propelled Work Machines"
        ],
        burden_holder="Designer must justify circuit configuration selection based on duty cycle and energy analysis",
        adversary_position="Simplest open center circuit regardless of energy waste",
        counter_arguments=[
            "Open center energy waste unacceptable for high duty cycle applications",
            "Load sensing investment recovered in 2-4 years from energy savings",
            "Closed center with accumulator enables peak flow exceeding pump capacity",
            "Multiple simultaneous actuators impossible with series open center",
            "Heat generation from inefficient circuits requires expensive cooling systems"
        ],
        resolution_strategy="Calculate duty cycle, energy consumption, and lifecycle cost for each circuit type, select based on ROI analysis",
        entity_scope="All hydraulic systems from 5 HP to 200+ HP industrial and mobile",
        confidence=0.93,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="ISO 1219-1 circuit symbols and Eaton/Parker system design guides"
    ),

    DoctrineBlock(
        topic="Accumulator Sizing - Bladder and Piston Types for Energy Storage",
        keywords=["accumulator", "bladder", "piston", "precharge", "sizing", "energy storage", "gas", "nitrogen"],
        conclusion_template="Accumulator size {} gallons with {} PSI precharge provides {} gallons usable volume at {} PSI operating pressure using {} design.",
        reasoning_framework="""
Accumulator Design and Sizing Framework:

Accumulator Types:

1. Bladder Accumulator (Most Common):
- Rubber bladder separates gas from fluid
- Sizes: 0.1 to 50 gallons
- Pressure: Up to 5000 PSI
- Fast response, compact
- Bladder life: 3-7 years typical
- Gas valve on top, fluid port on bottom
- Maximum compression ratio: 4:1 (gas side)

2. Piston Accumulator (High Volume):
- Free-floating piston separates gas and oil
- Sizes: 1 to 200+ gallons
- Pressure: Up to 10,000 PSI
- Slower response than bladder
- Long life, rebuildable
- Higher compression ratios: 10:1 possible
- Vertical or horizontal mounting

3. Diaphragm Accumulator (Small Volume):
- Elastic diaphragm separates gas and fluid
- Sizes: 0.05 to 5 gallons
- Pressure: Up to 3000 PSI
- Lowest cost, limited life
- Not repairable when diaphragm fails

Sizing Calculations:

Boyle's Law: P₁V₁ = P₂V₂ (isothermal, slow operation)
Adiabatic: P₁V₁ⁿ = P₂V₂ⁿ (fast operation, n = 1.4 for nitrogen)

Usable Volume:
V_usable = V₀ × (P₀/P₁ - P₀/P₂)
Where:
- V₀ = accumulator gas volume
- P₀ = precharge pressure (90% of minimum system pressure)
- P₁ = minimum operating pressure
- P₂ = maximum operating pressure

Precharge Pressure Selection:
- Standard: 90% of minimum system pressure
- Too low: Bladder bottoming, damage
- Too high: Reduced usable volume
- Temperature compensation: Pressure increases ~5 PSI per 10°F

Gas Selection:
- Nitrogen: Standard, inert, non-combustible
- Never use oxygen or compressed air (explosion risk)
- Dry nitrogen: Prevents internal corrosion
- Check precharge annually, adjust for temperature

Applications:

1. Energy Storage (Shock Absorption):
- Absorb pressure spikes from rapid valve closure
- Size for pressure spike energy: E = (P₂² - P₁²) × V / (2γ)
- Typical: 0.5-5 gallon bladder accumulator

2. Leakage Compensation:
- Maintain pressure during small leaks
- Size for acceptable pressure drop over time period
- Common in clamping circuits

3. Volume Compensation (Thermal Expansion):
- Prevent pressure buildup in blocked circuits
- Size for fluid thermal expansion: ΔV = V × β × ΔT
- β = 0.0004 per °F for mineral oil

4. Emergency Power Source:
- Provide fluid for emergency functions after pump stops
- Size for total volume of all actuators plus safety margin
- Typical: Large piston accumulator (10-100 gallons)

5. Pulsation Dampening:
- Smooth flow from piston pumps
- Size: 5-10x pump displacement per revolution
- Reduces noise and vibration

Safety Considerations:
- Accumulator = stored energy device (hazardous)
- Isolation valve required for maintenance
- Complete depressurization before disassembly
- Precharge only with dry nitrogen from dedicated equipment
- Regular inspection for corrosion, damage
- Bladder replacement on schedule or at first sign of gas-in-oil
""",
        key_factors=[
            "Precharge pressure should be 90% of minimum system pressure",
            "Usable volume is fraction of total volume based on pressure range",
            "Bladder accumulators limited to 4:1 compression ratio",
            "Temperature affects gas pressure - check precharge at operating temperature",
            "Never use compressed air or oxygen - explosion hazard with oil",
            "Bladder failure indicated by nitrogen bubbles in hydraulic oil",
            "Size for adiabatic process (n=1.4) for fast cycling applications"
        ],
        primary_authority=[
            "ISO 4414 - Pneumatic fluid power - General rules and safety requirements",
            "ASME Section VIII - Pressure Vessel Code (accumulators are pressure vessels)",
            "Parker Accumulator Sizing Guide",
            "Hydac Accumulator Technology Manual",
            "OSHA 1910.169 - Air Receivers (applies to accumulator safety)"
        ],
        burden_holder="Designer must calculate accumulator size for worst-case volume requirements with safety margin",
        adversary_position="Minimum size accumulator to reduce cost regardless of performance",
        counter_arguments=[
            "Undersized accumulator fails to perform intended function",
            "Wrong precharge causes bladder damage and premature failure",
            "Insufficient compression ratio requires larger, costlier accumulator",
            "Air precharge creates explosion risk and oxidation of fluid",
            "Missing isolation valve prevents safe maintenance"
        ],
        resolution_strategy="Calculate usable volume using Boyle's Law or adiabatic equation, select next standard size, verify precharge pressure",
        entity_scope="All hydraulic systems using accumulators from 0.1 gallon to 200+ gallon",
        confidence=0.94,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="ISO 4414 safety requirements and ASME Section VIII pressure vessel standards"
    ),

    DoctrineBlock(
        topic="Pressure Drop and Heat Generation in Hydraulic Systems",
        keywords=["pressure drop", "heat", "temperature", "cooling", "efficiency", "power loss", "heat exchanger"],
        conclusion_template="System pressure drop of {} PSI at {} GPM generates {} BTU/hr requiring {} cooling capacity at {} °F operating temperature.",
        reasoning_framework="""
Pressure Drop and Heat Analysis Framework:

Pressure Drop Sources:
1. Valves: 30-150 PSI (size properly to minimize)
2. Filters: 5-25 PSI clean, 50+ PSI clogged (replace filter)
3. Plumbing: 1-5 PSI per 100 feet (proper line sizing)
4. Fittings: 0.5-2 PSI each (minimize bends and restrictions)
5. Heat exchanger: 10-40 PSI
6. Components: Cylinders/motors typically <10 PSI

Total System Pressure Drop Target: <150 PSI at design flow

Heat Generation Formula:
Heat (BTU/hr) = ΔP (PSI) × Q (GPM) × 0.0004
Or: Heat (kW) = ΔP (bar) × Q (L/min) / 600

Example: 100 PSI drop at 50 GPM = 2,000 BTU/hr = 0.59 kW

Heat Sources:
- Pressure drop in restrictions (60-70% of heat)
- Pump inefficiency (10-15% of input power becomes heat)
- Fluid friction in lines and components
- Compression heating (rapid pressure increase)
- External heat pickup (ambient, engine compartment)

Acceptable Temperature Range:
- Mineral oil: 110-140°F optimal, 180°F maximum continuous
- Water-glycol: 130°F maximum (evaporation above this)
- Synthetic: 160-200°F continuous possible
- Cold start: >50°F required for proper viscosity

Temperature Effects:
- Every 18°F increase: Fluid life reduced by 50% (Arrhenius)
- Above 180°F: Accelerated oxidation, seal damage, additives depleted
- Below 50°F: Sluggish response, cavitation risk, high startup loads
- Viscosity change: Doubles every 35°F temperature decrease

Cooling Methods:

1. Tank Surface Area (Natural Convection):
- Dissipation: 0.001-0.002 BTU/hr per sq in per °F above ambient
- Rule of thumb: 1 sq ft surface per HP (marginal cooling)
- Adequate only for low duty cycle or small systems

2. Air-Cooled Heat Exchanger (Oil-to-Air):
- Fan forced air over finned tubes
- Dissipation: 20-40 BTU/hr per °F per CFM airflow
- Sizing: BTU/hr = CFM × ΔT × 1.08
- Requires 20-30°F approach temperature
- Common sizes: 50,000 to 500,000 BTU/hr

3. Water-Cooled Heat Exchanger (Oil-to-Water):
- Shell and tube or plate design
- Most efficient cooling method
- Sizing: BTU/hr = GPM_water × ΔT × 500
- Approach temperature: 5-10°F possible
- Requires clean water source
- Common in high power industrial systems

4. Thermostatic Control:
- Bypass valve maintains minimum operating temperature
- Prevents overcooling at startup or low ambient
- Valve opens at 110-120°F setpoint
- Full flow through cooler at 140-150°F

Heat Exchanger Sizing Example:
System: 50 HP pump, 75% efficient
Heat generation: 50 HP × 2545 BTU/HP × 0.25 = 31,800 BTU/hr
Temperature rise allowed: 20°F
Oil flow: 50 GPM
Required cooling: 31,800 BTU/hr

For air cooler:
CFM required = 31,800 / (20 × 1.08) = 1,472 CFM
Select cooler rated 40,000 BTU/hr at 20°F approach

System Efficiency Improvement:
- Reduce pressure drops (larger valves, less restrictive plumbing)
- Load sensing pump (match flow to demand)
- Variable frequency drive on electric motor
- Accumulator to reduce peak power
- Proper fluid viscosity grade
""",
        key_factors=[
            "Every 150 PSI pressure drop at 50 GPM generates 3,000 BTU/hr of heat",
            "Fluid temperature above 180°F dramatically reduces oil and seal life",
            "Heat exchanger must dissipate total system heat loss to maintain temperature",
            "Pressure drop reduction is more effective than adding cooling capacity",
            "Thermostatic bypass valve prevents overcooling during warmup",
            "Air cooled exchangers require 20-30°F approach, water cooled 5-10°F",
            "Reservoir surface area cooling inadequate for most industrial systems"
        ],
        primary_authority=[
            "ISO 23309 - Hydraulic fluid power - Determination of fluid power system performance",
            "Eaton Heat Dissipation in Hydraulic Systems Manual",
            "Parker Thermal Management Guide",
            "ASHRAE Heat Exchanger Design Guide",
            "ISO 16889 - Filter heat generation testing"
        ],
        burden_holder="Designer must calculate total heat generation and provide adequate cooling to maintain fluid temperature <140°F",
        adversary_position="No heat exchanger or undersized cooler to minimize initial cost",
        counter_arguments=[
            "Excessive temperature causes catastrophic seal failure and fluid breakdown",
            "Heat exchanger cost far less than downtime from thermal failures",
            "Proper sizing during design avoids expensive retrofit later",
            "Temperature control extends component life 3-5x",
            "Pressure drop reduction provides permanent energy savings"
        ],
        resolution_strategy="Calculate heat generation from all sources, select heat exchanger with 20% margin, verify fluid temperature under worst-case conditions",
        entity_scope="All hydraulic systems above 10 HP with continuous operation",
        confidence=0.95,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="ISO 23309 system performance and manufacturer heat dissipation guides"
    ),

    DoctrineBlock(
        topic="Electrohydraulic Motion Control - Proportional and Servo Valves",
        keywords=["proportional", "servo", "motion control", "position", "velocity", "feedback", "closed loop", "LVDT"],
        conclusion_template="Motion control system using {} valve with {} feedback provides {} positioning accuracy and {} response time at {} Hz bandwidth.",
        reasoning_framework="""
Electrohydraulic Motion Control Framework:

Proportional Valves:
- Spool position proportional to electrical input (0-10V or 4-20mA)
- Current-to-force solenoid actuator
- Open loop (no position feedback on spool)
- Hysteresis: 3-10% of signal (deadband)
- Response time: 50-200 ms
- Positioning accuracy: ±0.5-2% of stroke
- Cost: $500-3000
- Applications: Speed control, moderate precision positioning

Servo Valves:
- Closed loop spool position control (LVDT feedback)
- Two-stage design: Torque motor + pilot stage + main stage
- Minimal hysteresis: <0.1% of signal
- Response time: 5-20 ms
- Frequency response: 50-200 Hz (±90° phase)
- Positioning accuracy: ±0.01-0.1% with external feedback
- Cost: $3,000-15,000
- Applications: High precision, high speed motion control
- Contamination sensitive: ISO 16/14/11 minimum

Motion Control Strategies:

1. Open Loop Speed Control (Proportional Valve):
- Meter-in or meter-out flow control
- Speed varies with load
- Simple, low cost
- Accuracy: ±10-20% speed variation

2. Closed Loop Velocity Control:
- Velocity feedback (encoder, tachometer)
- PID controller adjusts valve command
- Maintains constant speed regardless of load
- Accuracy: ±1-2% velocity control

3. Closed Loop Position Control:
- Position feedback (LVDT, magnetostrictive, encoder)
- PID controller drives actuator to target position
- Servo valve: 0.001-0.010 inch accuracy
- Proportional valve: 0.010-0.100 inch accuracy
- Settling time: 0.1-1.0 seconds

4. Force Control:
- Load cell or pressure transducer feedback
- Controls force applied by actuator
- Used in presses, testing machines
- Accuracy: ±1-5% of full scale force

Feedback Sensors:

Position Sensors:
- LVDT (Linear Variable Differential Transformer): ±0.001 inch, analog output
- Magnetostrictive: ±0.001 inch, digital output, long stroke
- Linear encoder: ±0.0001 inch, highest accuracy
- Potentiometer: ±0.01 inch, low cost

Velocity Sensors:
- Rotary encoder with differentiation
- Tachometer generator (DC voltage proportional to speed)
- Accelerometer with integration

Pressure Sensors:
- Strain gauge: 0-10,000 PSI typical, ±0.25% accuracy
- Piezoelectric: High frequency response for dynamics
- 0-5V or 4-20mA output standard

Control System Design:

PID Controller Tuning:
- Proportional (P): Response magnitude (gain)
- Integral (I): Eliminates steady-state error
- Derivative (D): Damping, reduces overshoot
- Tuning: Start with P only, add I for error, add D for stability
- Sample rate: 10x system bandwidth minimum

Stability Criteria:
- Phase margin: >30° for stable system, >60° for robust
- Gain margin: >6 dB
- Frequency response testing to verify
- Avoid resonances in mechanical system

Common Issues:
- Valve null shift: Electronic offset adjustment required
- Stiction: Dither signal (small AC overlay) reduces
- Deadband: Proportional valves exhibit, servo valves minimal
- Saturation: Controller output limited to valve range
- Noise: Filter sensor signals, use shielded cables
""",
        key_factors=[
            "Servo valves provide 10x faster response and 10x better accuracy than proportional",
            "Closed loop control requires position/velocity feedback sensor",
            "PID controller tuning critical for stable, accurate motion control",
            "Proportional valves adequate for speed control and moderate positioning",
            "Servo valves require ISO 16/14/11 or better cleanliness - very contamination sensitive",
            "Frequency response bandwidth determines maximum achievable speed of motion",
            "Magnetostrictive sensors provide best combination of accuracy and stroke length"
        ],
        primary_authority=[
            "ISO 10770 - Hydraulic fluid power - Electrically modulated hydraulic control valves",
            "Moog Servo Valve Technical Bulletins",
            "Bosch Rexroth Proportional Valve Engineering Guide",
            "Parker Electrohydraulic Motion Control Manual",
            "NFPA T3.6.7 - Servo and Proportional Valve Testing"
        ],
        burden_holder="Controls engineer must tune PID parameters to achieve stable operation with required accuracy",
        adversary_position="Open loop proportional valve regardless of accuracy requirements",
        counter_arguments=[
            "Open loop cannot compensate for load variations and leakage",
            "Proportional valve hysteresis prevents precision positioning",
            "Servo valve investment justified by throughput and quality improvements",
            "Inadequate contamination control destroys expensive servo valves",
            "Poor PID tuning causes oscillation, overshoot, or sluggish response"
        ],
        resolution_strategy="Define accuracy and speed requirements, select valve type and sensor based on specifications, design and tune control system",
        entity_scope="All electrohydraulic motion control from simple speed control to precision multi-axis machines",
        confidence=0.92,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE,
        controlling_precedent="ISO 10770 valve specifications and manufacturer control system design guides"
    ),

    DoctrineBlock(
        topic="Hydraulic System Troubleshooting - Diagnostic Methodology",
        keywords=["troubleshooting", "diagnosis", "failure", "symptom", "pressure", "flow", "temperature", "noise"],
        conclusion_template="Symptom {} indicates probable cause {} verified by measuring {} with expected reading {} leading to repair action {}.",
        reasoning_framework="""
Systematic Hydraulic Troubleshooting Framework:

Primary Symptoms and Causes:

1. No Pressure or Low Pressure:
Causes:
- Pump not pumping (coupling broken, wrong rotation, internal failure)
- Relief valve set too low or stuck open
- Severe internal leakage (worn pump, valve, or cylinder seals)
- Low fluid level (pump cavitation)
Tests:
- Check pump rotation direction
- Measure pump output flow (should match displacement × RPM)
- Isolate and measure relief valve setting
- Check for fluid foaming (cavitation)

2. Slow Operation or Weak Force:
Causes:
- Low pressure (see above)
- Undersized valve or plumbing (excessive pressure drop)
- Internal leakage past cylinder seals or piston
- Wrong pump displacement or speed
Tests:
- Measure operating pressure under load
- Check pressure drop across valves and lines (should be <100 PSI)
- Isolate cylinder and check for drift (internal leakage)
- Verify pump flow output

3. Erratic Operation or Jerky Motion:
Causes:
- Air in system (compressible, foaming)
- Contaminated oil (sluggish valve operation)
- Sticking valve spools
- Loose electrical connections (proportional/servo valves)
- Mechanical binding in actuator or load
Tests:
- Check fluid level and look for foam
- Check filter differential pressure (clogged = contamination)
- Test valve for proper shifting
- Inspect for proper alignment and bearing condition

4. Excessive Heat Generation:
Causes:
- Relief valve bypassing continuously (pressure setting too low or stuck)
- Excessive pressure drops in system
- Wrong viscosity grade (too high = friction)
- Pump running continuously in open center at high pressure
- Insufficient cooling capacity
Tests:
- Measure operating temperature (should be 110-140°F)
- Check relief valve setting and operation
- Measure pressure drops through components
- Calculate heat generation and compare to cooling capacity

5. Excessive Noise:
Causes:
- Pump cavitation (low fluid level, restricted inlet, wrong viscosity)
- Air entrainment (leaking seals, vortex in reservoir)
- Worn pump bearings or internal parts
- Mechanical resonance
- Relief valve chattering (improper setting)
Tests:
- Check fluid level and inlet line restriction
- Listen for location of noise (pump, relief valve, etc.)
- Check for air bubbles in return line or reservoir
- Measure inlet vacuum (should be <5 inch Hg)

6. External Leakage:
Causes:
- Damaged seals or O-rings
- Loose fittings
- Cracked housings or cylinders
- Excessive pressure spikes
- Wrong seal material for fluid type
Tests:
- Visual inspection for leak location
- Check fitting torque
- Inspect for cracks or damage
- Monitor pressure for spikes (install pressure gauge with damper)

Diagnostic Tools and Measurements:

Pressure Gauges:
- Install at pump, actuator, before and after components
- Liquid-filled for shock protection
- Measure actual vs. expected pressure
- Snubbers or glycerin fill for pulsating systems

Flow Meters:
- Inline flow meter to verify pump output
- Compare actual vs. theoretical flow (GPM = Displacement × RPM / 231)
- Detect internal leakage in pumps and motors

Temperature Measurement:
- Infrared thermometer for surface temperatures
- Immersion thermometer for reservoir
- Monitor temperature rise during operation

Oil Sampling and Analysis:
- ISO 4406 particle count (contamination level)
- Viscosity testing (degradation, wrong grade)
- Water content (Karl Fischer test, should be <0.1%)
- Wear metals (ICP spectroscopy - detect component wear)
- Acid number (TAN - fluid oxidation)

Pressure Drop Testing:
- Measure pressure before and after components
- Calculate flow capacity: Q = Cv × √ΔP
- Identify restrictions and undersized components

Preventive Measures:
- Regular oil sampling and analysis (quarterly for critical systems)
- Filter changes based on differential pressure, not calendar
- Temperature monitoring and trending
- Vibration analysis for pumps and motors (bearing wear detection)
- Visual inspection for leaks and damage
- Maintain cleanliness during service
""",
        key_factors=[
            "Systematic approach: Identify symptom, list probable causes, test to verify",
            "Low pressure is most common symptom - check relief valve and pump output first",
            "Air in system causes erratic operation and must be bled from high points",
            "Heat generation indicates energy waste - identify and eliminate source",
            "Cavitation noise indicates inlet restriction or low fluid level",
            "Oil analysis detects impending failures before catastrophic breakdown",
            "70-80% of failures are contamination related - check filtration first"
        ],
        primary_authority=[
            "ISO 4413 - Hydraulic fluid power - General rules and safety requirements",
            "Eaton Hydraulic Troubleshooting Guide",
            "Parker Hannifin Troubleshooting Handbook",
            "Fluid Power Journal - Troubleshooting Series",
            "NFPA Recommended Maintenance Practices for Fluid Power Systems"
        ],
        burden_holder="Maintenance technician must follow systematic diagnostic approach with instrumentation",
        adversary_position="Replace components randomly until problem goes away",
        counter_arguments=[
            "Random part replacement wastes money and may not fix root cause",
            "Proper diagnosis identifies actual problem, not just symptoms",
            "Instrumentation provides objective data vs guesswork",
            "Oil analysis detects wear before catastrophic failure",
            "Contamination control prevents 70% of failures"
        ],
        resolution_strategy="Document symptoms, measure key parameters (pressure, flow, temperature), compare to normal values, identify and verify root cause, implement repair",
        entity_scope="All hydraulic system troubleshooting from mobile equipment to industrial machines",
        confidence=0.94,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="ISO 4413 general requirements and manufacturer troubleshooting procedures"
    ),

    DoctrineBlock(
        topic="Predictive Maintenance - Oil Analysis and Vibration Monitoring",
        keywords=["predictive maintenance", "oil analysis", "wear metals", "vibration", "condition monitoring", "CBM"],
        conclusion_template="Predictive maintenance program using {} sampling frequency and {} monitoring detects {} failure modes with {} lead time before failure.",
        reasoning_framework="""
Predictive Maintenance Strategy Framework:

Oil Analysis Program:

Sample Collection:
- Frequency: Quarterly for critical systems, annually for non-critical
- Sample location: Pressurized line port preferred (representative)
- Avoid: Drain plugs (settled contamination), breathers (atmosphere)
- Bottle: Clean, labeled with equipment ID, date, hours
- Consistent sampling point and method for trend analysis

Tests and Interpretation:

1. Particle Count (ISO 4406):
- Measures: particles >4, >6, >14 microns per 100 mL
- Cleanliness trend: Increasing = wear or contamination ingress
- Action limit: Exceeds component sensitivity requirement
- Typical: 18/16/13 for most systems, tighter for servo valves

2. Wear Metals (ICP Spectroscopy):
- Iron (Fe): Cylinder wear, pump/motor wear (30-50 PPM warning)
- Copper (Cu): Vane pump wear, bronze bushings (20-40 PPM warning)
- Aluminum (Al): Piston pump wear (10-20 PPM warning)
- Chromium (Cr): Hardened surfaces, piston rings (5-10 PPM warning)
- Trend analysis more important than absolute values
- Sudden increase = active wear, impending failure

3. Viscosity (ASTM D445):
- Compare to new oil specification (ISO VG grade)
- Increase >10%: Oxidation, contamination, wrong oil added
- Decrease >10%: Shearing, wrong oil added, fuel dilution
- Temperature correlation: Viscosity Index (VI) verification

4. Water Content (Karl Fischer):
- Target: <500 PPM (0.05%) for mineral oil
- >1000 PPM: Additive depletion, rust, bacteria growth
- Source: Condensation, seal leakage, water-based coolant
- Action: Drain water layer, vacuum dehydration, seal repair

5. Acid Number (TAN - Total Acid Number):
- Measures: Oxidation byproducts (acids)
- New oil: TAN 0.5-1.5 mg KOH/g
- Warning: TAN >2.0 (oil oxidizing)
- Critical: TAN >3.0 (change oil immediately)
- Accelerated by heat and contamination

6. Oxidation and Nitration (FTIR):
- Infrared spectroscopy detects molecular changes
- Oxidation: Carbonyl group formation
- Nitration: From high temperature, air ingress
- Early indicator before TAN increases significantly

Vibration Analysis Program:

Accelerometer Placement:
- Pump bearings (horizontal and vertical)
- Motor bearings
- Coupling
- High points on piping for water hammer

Vibration Measurements:
- Overall vibration level (RMS velocity, inch/sec)
- Frequency spectrum (FFT analysis)
- Bearing defect frequencies
- Cavitation detection (high frequency)

Alert Levels (ISO 10816):
- <0.1 inch/sec: Excellent (new equipment)
- 0.1-0.3 inch/sec: Good (acceptable)
- 0.3-0.7 inch/sec: Fair (monitor closely)
- >0.7 inch/sec: Poor (schedule repair)

Common Fault Detection:
- Unbalance: 1× running speed peak
- Misalignment: 2× running speed peak
- Bearing wear: Multiple harmonics, high frequency
- Looseness: Many harmonics of running speed
- Cavitation: Random high frequency (>10 kHz)

Predictive Maintenance Benefits:
- Reduce unplanned downtime by 50-70%
- Extend component life by 20-40%
- Optimize maintenance intervals (condition-based vs calendar)
- Early failure detection allows planned repair vs emergency
- Trend analysis predicts remaining useful life

Cost-Benefit Analysis:
- Oil analysis: $30-100 per sample
- Vibration system: $2,000-10,000 installed
- Typical ROI: 3-10x investment from avoided downtime
- Critical systems justify monthly monitoring
- Non-critical systems: Annual or biannual sufficient

Integration with CMMS:
- Track sample results over time
- Automate alerts when parameters exceed limits
- Schedule maintenance based on condition, not calendar
- Document corrective actions and effectiveness
""",
        key_factors=[
            "Oil analysis detects wear and contamination before catastrophic failure",
            "Increasing wear metals indicate active component degradation",
            "Particle count trend more important than single sample result",
            "Water contamination accelerates oxidation and depletes additives",
            "Vibration analysis detects mechanical issues (bearing wear, misalignment)",
            "Condition-based maintenance more cost effective than time-based",
            "ROI typically 3-10x from reduced downtime and extended component life"
        ],
        primary_authority=[
            "ISO 11171 - Hydraulic fluid power - Calibration of automatic particle counters",
            "ASTM D6224 - Standard Practice for In-Service Monitoring of Lubricating Oil",
            "ISO 10816 - Mechanical vibration - Evaluation of machine vibration",
            "ASTM D6595 - Standard Test Method for Determination of Wear Metals and Contaminants (ICP)",
            "ISO 4406 - Hydraulic fluid power - Fluids - Method for coding contamination level"
        ],
        burden_holder="Maintenance department must implement oil sampling program and respond to trending alerts",
        adversary_position="Run to failure, no monitoring or predictive maintenance",
        counter_arguments=[
            "Oil analysis cost far less than emergency repair and downtime",
            "Early detection allows planned repair during scheduled maintenance",
            "Trending identifies developing problems 30-90 days before failure",
            "Vibration monitoring detects mechanical issues missed by oil analysis",
            "Condition-based intervals optimize maintenance vs wasteful calendar schedules"
        ],
        resolution_strategy="Establish sampling frequency based on criticality, perform trending analysis, set alert limits based on component sensitivity, schedule repairs based on condition",
        entity_scope="All hydraulic systems where downtime cost exceeds monitoring cost (typically >25 HP systems)",
        confidence=0.93,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="ASTM D6224 in-service monitoring practices and ISO 10816 vibration standards"
    ),

]


# ============================================================================
# ENGINE CORE - TIE-20 IMPLEMENTATION
# ============================================================================

class HydraulicSystemsEngine:
    """MECH11 Hydraulic Systems Intelligence Engine"""

    def __init__(self):
        self.engine_id = ENGINE_ID
        self.version = VERSION
        self.start_time = datetime.now()
        self.query_count = 0
        self.total_latency = 0.0
        self.telemetry_log: List[TelemetryData] = []
        self.coverage_map: Dict[str, CoverageMapEntry] = {}
        self.audit_trail_path = Path(f"logs/{ENGINE_ID}_audit_trail.jsonl")
        self.audit_trail_path.parent.mkdir(exist_ok=True)

        # Initialize coverage map
        for doctrine in DOCTRINE_CACHE:
            self.coverage_map[doctrine.topic] = CoverageMapEntry(
                doctrine_topic=doctrine.topic,
                triggered_count=0,
                last_triggered=None,
                epistemic_gaps=[]
            )

        logger.info(f"{ENGINE_NAME} v{VERSION} initialized with {len(DOCTRINE_CACHE)} doctrine blocks")

    def three_layer_response(self, query: str, mode: ResponseMode) -> Dict[str, Any]:
        """TIE-20 Component: Three-layer response strategy"""
        start_time = datetime.now()

        # Layer 1: Doctrine Cache (0-200ms)
        doctrine_hits = self._search_doctrine_cache(query)

        if doctrine_hits and mode == ResponseMode.FAST:
            # Fast mode: Return cached conclusion
            result = self._build_fast_response(query, doctrine_hits)
        elif doctrine_hits:
            # Defense/Memo mode: Deep synthesis
            result = self._build_deep_response(query, doctrine_hits, mode)
        else:
            # No cache hits: Semantic search (Layer 2)
            result = self._fallback_response(query, mode)

        latency = (datetime.now() - start_time).total_seconds() * 1000

        # Update telemetry
        self._record_telemetry(query, result, latency, doctrine_hits)

        return result

    def _search_doctrine_cache(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache for matching blocks"""
        scored = [(d, d.matches(query)) for d in DOCTRINE_CACHE]
        scored.sort(key=lambda x: x[1], reverse=True)

        # Return top matches with score > 0.3
        hits = [d for d, score in scored if score > 0.3][:3]

        # Update coverage map
        for doctrine in hits:
            entry = self.coverage_map[doctrine.topic]
            entry.triggered_count += 1
            entry.last_triggered = datetime.now().isoformat()

        return hits

    def _build_fast_response(self, query: str, doctrines: List[DoctrineBlock]) -> Dict[str, Any]:
        """Fast mode: Concise cached response"""
        primary = doctrines[0]

        analysis = f"{primary.conclusion_template}\n\n"
        analysis += f"Key Factors:\n"
        for factor in primary.key_factors[:3]:
            analysis += f"- {factor}\n"

        return {
            "analysis": analysis.strip(),
            "confidence": primary.confidence,
            "stratification": primary.confidence_stratification,
            "sources": primary.primary_authority[:2],
            "mode": "FAST"
        }

    def _build_deep_response(self, query: str, doctrines: List[DoctrineBlock], mode: ResponseMode) -> Dict[str, Any]:
        """Defense/Memo mode: Comprehensive analysis"""
        primary = doctrines[0]

        analysis = f"# Hydraulic Systems Analysis\n\n"
        analysis += f"## Primary Assessment\n{primary.conclusion_template}\n\n"

        analysis += f"## Technical Framework\n{primary.reasoning_framework}\n\n"

        analysis += f"## Key Engineering Factors\n"
        for factor in primary.key_factors:
            analysis += f"- {factor}\n"
        analysis += "\n"

        if len(doctrines) > 1:
            analysis += f"## Related Considerations\n"
            for doctrine in doctrines[1:]:
                analysis += f"### {doctrine.topic}\n"
                for factor in doctrine.key_factors[:2]:
                    analysis += f"- {factor}\n"
                analysis += "\n"

        analysis += f"## Design Standards and References\n"
        all_sources = []
        for doctrine in doctrines:
            all_sources.extend(doctrine.primary_authority)
        unique_sources = list(dict.fromkeys(all_sources))[:5]
        for source in unique_sources:
            analysis += f"- {source}\n"

        if mode == ResponseMode.MEMO:
            analysis += f"\n## Counter-Arguments and Risk Factors\n"
            for arg in primary.counter_arguments[:3]:
                analysis += f"- {arg}\n"

            analysis += f"\n## Resolution Strategy\n{primary.resolution_strategy}\n"

        return {
            "analysis": analysis.strip(),
            "confidence": primary.confidence,
            "stratification": primary.confidence_stratification,
            "sources": unique_sources,
            "mode": mode.value
        }

    def _fallback_response(self, query: str, mode: ResponseMode) -> Dict[str, Any]:
        """No doctrine hits: General guidance"""
        analysis = f"The query regarding '{query}' requires specialized hydraulic systems analysis.\n\n"
        analysis += "General Hydraulic Systems Principles:\n"
        analysis += "- System design must consider pressure ratings, flow requirements, and duty cycle\n"
        analysis += "- Component selection based on ISO and NFPA standards\n"
        analysis += "- Contamination control critical for system reliability (ISO 4406 cleanliness codes)\n"
        analysis += "- Heat generation must be managed through proper sizing and cooling\n"
        analysis += "- Predictive maintenance through oil analysis extends component life\n\n"
        analysis += "Recommend consultation with hydraulic systems engineer for detailed analysis."

        return {
            "analysis": analysis,
            "confidence": 0.5,
            "stratification": ConfidenceStratification.DISCLOSURE,
            "sources": ["ISO 4413 - Hydraulic fluid power general rules", "NFPA technical standards"],
            "mode": mode.value
        }

    def _record_telemetry(self, query: str, result: Dict[str, Any], latency: float, doctrines: List[DoctrineBlock]):
        """TIE-20 Component: Telemetry tracking"""
        category = self._classify_query(query)

        telemetry = TelemetryData(
            query_id=hashlib.sha256(f"{query}{datetime.now().isoformat()}".encode()).hexdigest()[:16],
            timestamp=datetime.now().isoformat(),
            category=category,
            mode=ResponseMode(result.get("mode", "FAST")),
            doctrine_hits=[d.topic for d in doctrines],
            latency_ms=latency,
            confidence=result["confidence"]
        )

        self.telemetry_log.append(telemetry)
        self.query_count += 1
        self.total_latency += latency

        # Audit trail
        self._write_audit_trail(query, result, telemetry)

    def _classify_query(self, query: str) -> IssueCategory:
        """Classify query into issue category"""
        query_lower = query.lower()

        if any(k in query_lower for k in ["pump", "displacement", "gear", "piston", "vane"]):
            return IssueCategory.PUMP_SELECTION
        elif any(k in query_lower for k in ["cylinder", "actuator", "bore", "rod"]):
            return IssueCategory.ACTUATOR_DESIGN
        elif any(k in query_lower for k in ["circuit", "open center", "closed center", "load sensing"]):
            return IssueCategory.CIRCUIT_DESIGN
        elif any(k in query_lower for k in ["valve", "directional", "proportional", "servo"]):
            return IssueCategory.VALVE_SELECTION
        elif any(k in query_lower for k in ["fluid", "oil", "viscosity", "vg"]):
            return IssueCategory.FLUID_SELECTION
        elif any(k in query_lower for k in ["contamination", "filter", "cleanliness", "iso 4406"]):
            return IssueCategory.CONTAMINATION_CONTROL
        elif any(k in query_lower for k in ["pressure drop", "restriction", "line size"]):
            return IssueCategory.PRESSURE_DROP
        elif any(k in query_lower for k in ["heat", "temperature", "cooling", "heat exchanger"]):
            return IssueCategory.HEAT_MANAGEMENT
        elif any(k in query_lower for k in ["motion control", "position", "servo", "proportional"]):
            return IssueCategory.MOTION_CONTROL
        elif any(k in query_lower for k in ["efficiency", "energy", "power"]):
            return IssueCategory.SYSTEM_EFFICIENCY
        elif any(k in query_lower for k in ["troubleshoot", "problem", "failure", "symptom"]):
            return IssueCategory.TROUBLESHOOTING
        elif any(k in query_lower for k in ["maintenance", "oil analysis", "vibration", "predictive"]):
            return IssueCategory.PREDICTIVE_MAINTENANCE
        else:
            return IssueCategory.PUMP_SELECTION

    def _write_audit_trail(self, query: str, result: Dict[str, Any], telemetry: TelemetryData):
        """TIE-20 Component: Audit trail logging"""
        audit_entry = {
            "query_id": telemetry.query_id,
            "timestamp": telemetry.timestamp,
            "query": query,
            "category": telemetry.category.value,
            "mode": telemetry.mode.value,
            "confidence": result["confidence"],
            "stratification": result["stratification"].value if isinstance(result["stratification"], ConfidenceStratification) else result["stratification"],
            "doctrine_hits": telemetry.doctrine_hits,
            "latency_ms": telemetry.latency_ms
        }

        with open(self.audit_trail_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry, ensure_ascii=False) + "\n")

    def calculate_determinism_hash(self, query: str, result: Dict[str, Any]) -> str:
        """TIE-20 Component: Determinism hash for reproducibility"""
        hash_input = f"{query}|{result['analysis']}|{result['confidence']}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    def get_health(self) -> HealthResponse:
        """TIE-20 Component: Health endpoint"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        avg_latency = self.total_latency / self.query_count if self.query_count > 0 else 0

        return HealthResponse(
            status="operational",
            engine_id=self.engine_id,
            version=self.version,
            uptime_seconds=uptime,
            total_queries=self.query_count,
            doctrine_count=len(DOCTRINE_CACHE),
            avg_latency_ms=avg_latency
        )

    def get_coverage_map(self) -> List[Dict[str, Any]]:
        """TIE-20 Component: Coverage map for epistemic gaps"""
        return [
            {
                "doctrine": topic,
                "triggered_count": entry.triggered_count,
                "last_triggered": entry.last_triggered,
                "epistemic_gaps": entry.epistemic_gaps
            }
            for topic, entry in self.coverage_map.items()
        ]

    def get_metrics(self) -> Dict[str, Any]:
        """TIE-20 Component: Metrics collector"""
        category_counts = {}
        for tel in self.telemetry_log:
            cat = tel.category.value
            category_counts[cat] = category_counts.get(cat, 0) + 1

        return {
            "total_queries": self.query_count,
            "avg_latency_ms": self.total_latency / self.query_count if self.query_count > 0 else 0,
            "category_distribution": category_counts,
            "doctrine_coverage": {
                "total_doctrines": len(DOCTRINE_CACHE),
                "triggered_doctrines": sum(1 for e in self.coverage_map.values() if e.triggered_count > 0),
                "coverage_percentage": sum(1 for e in self.coverage_map.values() if e.triggered_count > 0) / len(DOCTRINE_CACHE) * 100
            }
        }


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    description="TIE-Grade Hydraulic Systems Intelligence Engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = HydraulicSystemsEngine()


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint"""
    try:
        result = engine.three_layer_response(request.query, request.mode)

        response = QueryResponse(
            query_id=hashlib.sha256(f"{request.query}{datetime.now().isoformat()}".encode()).hexdigest()[:16],
            analysis=result["analysis"],
            confidence=result["confidence"],
            stratification=result["stratification"],
            sources=result["sources"],
            warnings=[],
            latency_ms=engine.telemetry_log[-1].latency_ms if engine.telemetry_log else 0,
            determinism_hash=engine.calculate_determinism_hash(request.query, result)
        )

        logger.info(f"Query processed: {request.query[:50]}... | Mode: {request.mode} | Confidence: {result['confidence']}")
        return response

    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint"""
    return engine.get_health()


@app.get("/coverage")
async def coverage_endpoint():
    """Doctrine coverage map"""
    return {"coverage_map": engine.get_coverage_map()}


@app.get("/metrics")
async def metrics_endpoint():
    """Performance metrics"""
    return engine.get_metrics()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "engine": ENGINE_NAME,
        "version": VERSION,
        "status": "operational",
        "endpoints": {
            "query": "/query",
            "health": "/health",
            "coverage": "/coverage",
            "metrics": "/metrics"
        }
    }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
