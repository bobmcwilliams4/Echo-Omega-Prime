"""
OFE14 Chemical Injection Systems Intelligence Engine v1.0.0
============================================================

Domain: Oilfield chemical injection systems, pump selection, dosing optimization,
        corrosion/scale/paraffin programs, chemical compatibility, inventory management

Port: 9284
Architecture: TIE-20 compliant (three-layer response, doctrine cache, telemetry)

Author: ECHO OMEGA PRIME
Date: 2026-02-14
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field


# ============================================================================
# ENUMERATIONS
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
    PUMP_SELECTION = "PUMP_SELECTION"
    INJECTION_POINT_DESIGN = "INJECTION_POINT_DESIGN"
    CORROSION_INHIBITOR = "CORROSION_INHIBITOR"
    SCALE_INHIBITOR = "SCALE_INHIBITOR"
    PARAFFIN_MANAGEMENT = "PARAFFIN_MANAGEMENT"
    DEMULSIFIER = "DEMULSIFIER"
    H2S_SCAVENGER = "H2S_SCAVENGER"
    BIOCIDE = "BIOCIDE"
    DOSING_OPTIMIZATION = "DOSING_OPTIMIZATION"
    CHEMICAL_COMPATIBILITY = "CHEMICAL_COMPATIBILITY"
    INVENTORY_MANAGEMENT = "INVENTORY_MANAGEMENT"
    SAFETY_COMPLIANCE = "SAFETY_COMPLIANCE"
    COST_ANALYSIS = "COST_ANALYSIS"


class AuthorityLevel(str, Enum):
    API_STANDARD = "API_STANDARD"
    MANUFACTURER_SPEC = "MANUFACTURER_SPEC"
    INDUSTRY_PRACTICE = "INDUSTRY_PRACTICE"
    FIELD_DATA = "FIELD_DATA"
    VENDOR_RECOMMENDATION = "VENDOR_RECOMMENDATION"
    REGULATORY = "REGULATORY"
    LABORATORY_TEST = "LABORATORY_TEST"


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=10, description="Chemical injection question")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING)
    context: Optional[Dict[str, Any]] = Field(default=None, description="Well/system context")


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    response_time_ms: float
    determinism_hash: str
    metadata: Dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    avg_response_ms: float


# ============================================================================
# DOCTRINE BLOCK STRUCTURE
# ============================================================================

class DoctrineBlock:
    """Structured chemical injection expertise block"""

    def __init__(
        self,
        topic: str,
        keywords: List[str],
        conclusion_template: List[str],
        reasoning_framework: str,
        key_factors: List[str],
        primary_authority: List[str],
        confidence: ConfidenceLevel,
        category: IssueCategory,
        authority_level: AuthorityLevel
    ):
        self.topic = topic
        self.keywords = [k.lower() for k in keywords]
        self.conclusion_template = conclusion_template
        self.reasoning_framework = reasoning_framework
        self.key_factors = key_factors
        self.primary_authority = primary_authority
        self.confidence = confidence
        self.category = category
        self.authority_level = authority_level
        self.hit_count = 0
        self.last_triggered = None


# ============================================================================
# DOCTRINE CACHE - 25+ REAL CHEMICAL INJECTION EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    DoctrineBlock(
        topic="API 675 Chemical Metering Pump Selection",
        keywords=["metering pump", "api 675", "chemical pump", "pump selection", "diaphragm", "plunger"],
        conclusion_template=[
            "Select API 675 chemical metering pump based on fluid properties, flow rate requirements, and pressure conditions.",
            "Diaphragm pumps preferred for corrosive/abrasive fluids with precise flow control requirements.",
            "Plunger pumps provide higher pressures and flow rates but require seal maintenance and fluid compatibility."
        ],
        reasoning_framework="""
API 675 defines two primary metering pump types:

DIAPHRAGM PUMPS:
- Hydraulically actuated diaphragm isolates chemical from drive mechanism
- Ideal for corrosive, toxic, or abrasive fluids (acids, caustics, scale inhibitors)
- Flow range: 0.1 to 100 GPH typical
- Pressure: up to 7500 psi (520 bar)
- Accuracy: +/- 1% at steady state
- Advantages: No seals contacting chemical, precise dosing, low maintenance
- Limitations: Lower flow capacity, higher cost per GPH

PLUNGER PUMPS:
- Direct displacement via reciprocating plunger with packed seals
- Suited for non-abrasive fluids requiring higher flows (demulsifiers, defoamers)
- Flow range: 1 to 500+ GPH
- Pressure: up to 10,000 psi (690 bar)
- Seal life dependent on fluid lubricity and solids content
- Advantages: Higher flow capacity, lower cost per GPH
- Limitations: Seal wear with abrasive/dry fluids, periodic packing replacement

SELECTION CRITERIA:
1. Fluid compatibility: Check elastomer/wetted material compatibility (Viton, PTFE, Hastelloy, 316SS)
2. Flow requirement: Match pump capacity curve to required dosing rate with 20% margin
3. Discharge pressure: Must exceed wellhead/pipeline pressure plus friction losses plus 100 psi safety margin
4. Turndown ratio: API 675 pumps typically 10:1 manual, 100:1 with VFD
5. Suction conditions: Flooded suction preferred, NPSH requirements if lift required
6. Temperature rating: Verify pump temp limits vs chemical storage/ambient conditions
7. Control method: Stroke adjustment (manual/pneumatic), VFD, flow meter feedback loop
8. Redundancy: Install duplex or triplex pump systems for critical applications
9. Pulsation dampener: Required for smooth injection, protects check valves
10. Calibration: Verify actual flow vs stroke setting with graduated cylinder test

COMMON ERRORS:
- Undersizing pump discharge pressure (fails to inject under wellhead pressure)
- Selecting plunger pump for slurry or crystallizing fluids (rapid seal failure)
- No pulsation dampener (check valve chatter, flow surges)
- Single pump on critical wells (no backup during maintenance)
- Improper suction design (cavitation, inconsistent flow)
""",
        key_factors=[
            "Fluid chemical compatibility with wetted materials (seals, valves, diaphragm)",
            "Flow rate range with adequate turndown ratio (10:1 minimum)",
            "Discharge pressure exceeds system pressure plus friction plus 100 psi margin",
            "Temperature limits of pump components vs operating conditions",
            "Maintenance accessibility and spare parts availability",
            "Control method (stroke, speed, flow feedback) for dosing precision",
            "Pulsation dampener and pressure relief valve protection"
        ],
        primary_authority=[
            "API 675 'Positive Displacement Pumps - Reciprocating' (3rd Edition 2024)",
            "Manufacturer pump curves and materials compatibility charts (Milton Roy, Grundfos, ProMinent)",
            "NACE MR0175/ISO 15156 for sour service materials selection"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PUMP_SELECTION,
        authority_level=AuthorityLevel.API_STANDARD
    ),

    DoctrineBlock(
        topic="Injection Quill Design and Placement",
        keywords=["injection quill", "quill placement", "atomization", "mixing", "injection point"],
        conclusion_template=[
            "Position injection quill at pipeline centerline with nozzle facing upstream into flow for optimal atomization and mixing.",
            "Retractable quills enable maintenance without system shutdown, critical for high-pressure or hazardous service.",
            "Quill length should reach 1/3 pipe diameter from wall with spray angle 30-45 degrees for turbulent dispersion."
        ],
        reasoning_framework="""
INJECTION QUILL DESIGN PRINCIPLES:

QUILL TYPES:
1. Fixed quills: Welded/threaded into pipeline, low cost, permanent installation
2. Retractable quills: Hot-tap installation, can withdraw for cleaning/replacement without shutdown
3. Atomizing quills: Multiple orifice nozzle for fine chemical dispersion

PLACEMENT RULES:
- Position at pipeline centerline (50% of pipe diameter from wall)
- Nozzle orientation: UPSTREAM into flow (not downstream) for immediate mixing
- Minimum 5 pipe diameters downstream of elbow/tee/valve for uniform flow profile
- Minimum 2 pipe diameters upstream of next fitting to complete mixing
- Avoid low points (chemical pooling) and high points (vapor lock)

QUILL LENGTH CALCULATION:
- For pipe diameter D, quill insertion depth = D/3 from pipe wall
- Example: 4-inch pipe → quill extends 1.33 inches from wall into flow
- Too shallow: chemical rides pipe wall, poor mixing
- Too deep: obstructs flow, creates turbulence/erosion

NOZZLE DESIGN:
- Orifice size: Balance between atomization (small = good) and plugging risk (large = reliable)
- Typical range: 0.040 to 0.125 inch diameter
- Spray angle: 30-45 degrees for turbulent dispersion
- Multi-orifice nozzles: 4-8 holes at 45-90 degree spacing for radial distribution
- Back pressure check valve prevents backflow when pump stops

FLOW VELOCITY REQUIREMENTS:
- Minimum pipeline velocity: 3 ft/sec for chemical dispersion
- Optimal: 5-10 ft/sec for turbulent mixing (Reynolds >4000)
- Laminar flow (Re <2300): Chemical stratification risk, consider static mixer

MATERIALS:
- Quill body: 316SS minimum, Hastelloy C-276 for extreme corrosion
- Nozzle: Hardened 17-4PH SS or tungsten carbide for erosion resistance
- Packing: Graphite or PTFE for retractable seal

INSTALLATION BEST PRACTICES:
- Install isolation valve + check valve upstream of quill
- Pressure gauge at injection point to monitor backpressure
- Sample port 10 pipe diameters downstream to verify chemical residual
- For subsea/downhole: capillary tube injection to annulus or tubing
- Retractable quill procedure: pressurize annular seal chamber, withdraw under pressure

COMMON FAILURES:
- Nozzle plugging from chemical crystallization (heat trace or solvent flush)
- Quill erosion from high velocity or abrasive fluids (upgrade to carbide nozzle)
- Poor mixing from downstream injection (chemical exits before dispersing)
- Packing leaks on retractable quills (rebuild seal assembly annually)
""",
        key_factors=[
            "Quill insertion depth 1/3 pipe diameter from wall at centerline",
            "Nozzle oriented upstream into flow for immediate atomization",
            "Placement >5D downstream of fittings for uniform flow profile",
            "Orifice size balances atomization vs plugging resistance",
            "Retractable design for high-value or hazardous chemical service",
            "Back pressure check valve prevents siphoning",
            "Pipeline velocity >3 ft/sec minimum for turbulent mixing"
        ],
        primary_authority=[
            "NACE SP0108 'Control of Internal Corrosion in Steel Pipelines and Piping Systems'",
            "API RP 14E 'Design and Installation of Offshore Production Platform Piping Systems'",
            "Quill manufacturer installation guides (Kuehne Chemical, Swagelok)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.INJECTION_POINT_DESIGN,
        authority_level=AuthorityLevel.API_STANDARD
    ),

    DoctrineBlock(
        topic="Corrosion Inhibitor Film-Forming Amine Programs",
        keywords=["corrosion inhibitor", "filming amine", "imidazoline", "quaternary amine", "residual testing"],
        conclusion_template=[
            "Film-forming amines (imidazolines, quaternary amines) adsorb to steel surfaces creating hydrophobic barrier against CO2 and H2S corrosion.",
            "Target residual concentration 10-50 ppm in produced water measured by colorimetric or fluorescent tracer testing.",
            "Effectiveness depends on water-wetting (>40% water cut), temperature (<250F optimal), and crude oil surfactant interference."
        ],
        reasoning_framework="""
CORROSION INHIBITOR CHEMISTRY:

PRIMARY TYPES:
1. Imidazoline-based: Most common, adsorbs to steel via nitrogen functional groups
   - Forms monomolecular film at steel-water interface
   - Effective at 100-250F, degrades above 300F
   - Oil-soluble, requires partitioning to water phase

2. Quaternary ammonium compounds: Cationic surfactants, strong adsorption
   - Effective at lower temperatures (<150F)
   - Good for water-continuous systems
   - Can cause emulsion issues at high concentrations

3. Phosphate esters: For high-temperature applications (>250F)
   - Forms protective iron phosphate layer
   - Requires alkaline pH control

4. Organic sulfur compounds: For H2S corrosion (sour service)
   - Thiols, mercaptans, sulfides
   - Caution: Can increase H2S corrosivity if overdosed

MECHANISM OF PROTECTION:
- Amine molecules adsorb to steel surface via electrostatic attraction
- Hydrocarbon tails orient outward creating water-repellent film
- Film thickness: 10-100 angstroms (molecular monolayer)
- Prevents H2O, CO2, H2S contact with steel (blocks cathodic reaction)
- Film persistence: 24-72 hours, requires continuous replenishment

DOSING STRATEGY:
1. Initial slug: 50-200 ppm to establish film (first 24-48 hours)
2. Maintenance dose: 10-50 ppm continuous injection
3. Batch treatment: Periodic slugs if continuous injection not feasible
4. Adjust based on corrosion rate monitoring (weight loss coupons, ER probes, iron counts)

RESIDUAL TESTING METHODS:
- Colorimetric: Dye-based chemistry reacts with inhibitor (field test kit)
- Fluorescence: Fluorescent tracer co-injected, measured by fluorometer (0.1 ppm detection)
- Potentiometric titration: Lab method, quantifies active ingredient
- Target residual: 10-50 ppm in produced water sample

PERFORMANCE MONITORING:
- Weight loss coupons: 30-90 day exposure, target <2 mils/year (mpy)
- Electrical resistance (ER) probes: Real-time corrosion rate trending
- Linear polarization resistance (LPR): Instantaneous corrosion current
- Iron counts: Dissolved Fe in produced water, target <5 ppm (indicates active corrosion)
- Pigging debris analysis: Internal corrosion product accumulation

FACTORS AFFECTING PERFORMANCE:
- Water cut: Requires >40% for water-continuous phase (inhibitor partitioning)
- Temperature: Optimal 100-250F, desorption at higher temps
- Flow regime: Turbulent flow improves distribution, erosion can remove film
- Crude oil composition: Surfactants/asphaltenes compete for adsorption sites
- Chlorides: High salinity (>50,000 ppm) increases corrosion driving force
- CO2 partial pressure: >30 psi CO2 requires higher inhibitor dose
- H2S: Sour service requires specialty inhibitors + materials upgrade

COMMON ISSUES:
- Underdosing: Localized corrosion breakthroughs, pitting
- Overdosing: Emulsion formation, increased chemical cost, disposal issues
- Incompatibility: Precipitation when mixed with other chemicals (test before blending)
- Temperature excursions: Inhibitor desorption during hot oil treatments
- Solids carryover: Sand/scale block adsorption sites, reduce effectiveness
""",
        key_factors=[
            "Film-forming mechanism requires water-continuous phase (>40% water cut)",
            "Target residual 10-50 ppm measured in produced water samples",
            "Optimal temperature range 100-250F before thermal degradation",
            "Initial slug dose 50-200 ppm to establish film, then 10-50 ppm maintenance",
            "Performance monitored via corrosion coupons (<2 mpy), ER probes, iron counts (<5 ppm)",
            "Crude oil surfactants and high salinity reduce film stability",
            "Incompatibility testing required before mixing with other chemicals"
        ],
        primary_authority=[
            "NACE SP0169 'Control of External Corrosion on Underground or Submerged Metallic Piping Systems'",
            "NACE TM0194 'Field Monitoring of Bacterial Growth in Oil and Gas Systems'",
            "Inhibitor vendor performance data (Baker Hughes, Halliburton, Clariant)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CORROSION_INHIBITOR,
        authority_level=AuthorityLevel.INDUSTRY_PRACTICE
    ),

    DoctrineBlock(
        topic="Scale Inhibitor Squeeze Treatment Design",
        keywords=["scale inhibitor", "squeeze treatment", "adsorption", "precipitation", "barium sulfate", "calcium carbonate"],
        conclusion_template=[
            "Scale inhibitor squeeze treatments inject high concentration inhibitor (5,000-20,000 ppm) that adsorbs onto formation rock, then desorbs slowly protecting production tubing for 3-18 months.",
            "Treatment life depends on adsorption/desorption isotherm, formation temperature, brine chemistry, and production rate.",
            "Design requires core flow tests, compatibility testing, and return curve modeling to optimize inhibitor type and volume."
        ],
        reasoning_framework="""
SCALE INHIBITOR SQUEEZE TREATMENT FUNDAMENTALS:

SCALE TYPES IN OILFIELD:
1. Calcium carbonate (CaCO3): Forms when CO2 flashes, pH rises, decreases pressure
2. Barium/strontium sulfate (BaSO4, SrSO4): Incompatible water mixing, insoluble, difficult to remove
3. Calcium sulfate (CaSO4): Temperature/pressure dependent solubility
4. Iron sulfide (FeS): H2S + Fe corrosion products, forms black sludge
5. Halite (NaCl): Evaporation of brine in near-wellbore

INHIBITOR CHEMISTRY:
- Phosphonates (DTPMP, HEDP): Low cost, effective for CaCO3, limited thermal stability (<200F)
- Polymeric inhibitors (polyacrylates, phosphino-polycarboxylic acid): High temp (>250F), BaSO4/SrSO4
- Sulfonated polymers: Sour service, H2S resistance
- Green inhibitors: Biodegradable polyaspartates (environmental regulations)

SQUEEZE TREATMENT MECHANISM:
1. PREFLUSH: Inject 10-50 bbl compatible brine to displace formation water from near-wellbore
   - Prevents precipitation of inhibitor with formation brine
   - May include mutual solvent (ethylene glycol monobutyl ether) to improve injectivity

2. MAIN TREATMENT: Inject 10-100 bbl inhibitor solution (5,000-20,000 ppm active)
   - Inhibitor adsorbs onto formation rock (sandstone, carbonate)
   - Adsorption isotherm: Langmuir or Freundlich model
   - Higher concentration → more adsorption → longer life

3. OVERFLUSH: Inject 20-100 bbl brine to push inhibitor deep into formation
   - Prevents inhibitor flowback during initial production
   - Volume based on wellbore geometry and desired penetration depth

4. SHUT-IN: 12-48 hours soak time for adsorption equilibrium
   - Allows inhibitor molecules to bond with rock surface
   - Temperature-dependent: Longer soak at lower temps

5. FLOWBACK: Produce well, monitor inhibitor returns
   - Initial high concentration (10,000+ ppm) decreases over time
   - Target plateau: 5-20 ppm for scale inhibition
   - Treatment life: Time until residual drops below minimum effective concentration (MEC)

DESIGN PARAMETERS:
- Inhibitor type: Match to scale type, temperature, brine chemistry
- Concentration: Core flow tests determine adsorption capacity vs concentration
- Volume: Balance treatment life vs fluid cost and injection time
- Injection rate: Must not fracture formation (<0.8 psi/ft gradient)
- Shut-in time: Minimum for adsorption equilibrium (typically 24 hours)

CORE FLOW TESTING (Lab Evaluation):
1. Obtain formation core samples (1-inch diameter, 3-6 inch length)
2. Saturate with formation brine, heat to reservoir temperature
3. Inject inhibitor solution at reservoir conditions
4. Displace with brine, measure inhibitor returns over time
5. Generate return curve: Inhibitor concentration vs pore volumes produced
6. Determine treatment life based on MEC threshold (5-20 ppm)

RETURN CURVE INTERPRETATION:
- Sharp peak then rapid decline: Poor adsorption (wrong inhibitor for rock type)
- High peak, slow decline: Good adsorption, long treatment life
- Plateau behavior: Ideal, sustained protection at MEC level
- Secondary peak: Precipitation/re-dissolution (compatibility issue)

TREATMENT LIFE FACTORS:
- Formation adsorption capacity: Sandstone >carbonate (higher surface area)
- Temperature: Higher temp reduces adsorption (endothermic desorption)
- Production rate: Higher rate depletes inhibitor faster (shorter life)
- Water cut: Higher water cut requires higher MEC (more scale risk)
- Inhibitor concentration: Higher dose → longer life (diminishing returns above 20,000 ppm)

MONITORING AND OPTIMIZATION:
- Sample produced water weekly initially, monthly after stabilization
- Plot inhibitor residual vs cumulative production (barrels or days)
- Re-squeeze when residual <MEC or scale detected (pressure drop, solids)
- Adjust next treatment based on actual vs predicted life
- Consider continuous low-dose injection if squeeze life <3 months

COMMON FAILURES:
- Incompatibility: Inhibitor precipitates with formation brine (white-out test required)
- Under-treatment: Insufficient volume or concentration, short life (<1 month)
- Formation damage: Inhibitor/overflush fluid reduces permeability
- Early flowback: Insufficient shut-in time, inhibitor returns too quickly
- Wrong inhibitor type: Phosphonate used for BaSO4 (ineffective, use polymer)
""",
        key_factors=[
            "Inhibitor type selected based on scale mineralogy, temperature, and brine compatibility",
            "Squeeze volume and concentration designed from core flow test return curves",
            "Treatment sequence: preflush, main treatment (5,000-20,000 ppm), overflush, shut-in 12-48 hours",
            "Target residual 5-20 ppm in produced water for scale protection",
            "Treatment life depends on adsorption capacity, production rate, and temperature",
            "Compatibility testing prevents inhibitor precipitation with formation brine",
            "Re-squeeze when residual drops below MEC or scale detected"
        ],
        primary_authority=[
            "SPE 164111 'Scale Inhibitor Squeeze Treatment Design and Case Histories'",
            "NACE Publication 31215 'Oilfield Scale Inhibition: Chemical and Testing Procedures'",
            "Vendor squeeze design software (ScaleChem, MultiScale, ProSqueeze)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SCALE_INHIBITOR,
        authority_level=AuthorityLevel.INDUSTRY_PRACTICE
    ),

    DoctrineBlock(
        topic="Paraffin Management - Crystal Modifiers vs Solvents",
        keywords=["paraffin", "wax", "pour point depressant", "crystal modifier", "solvent", "aromatic naphtha"],
        conclusion_template=[
            "Paraffin crystal modifiers (pour point depressants) prevent wax crystallization by disrupting lattice formation, effective for prevention but not remediation.",
            "Aromatic solvents (xylene, toluene, diesel) dissolve existing paraffin deposits for remediation but provide no long-term prevention.",
            "Combination approach: Solvent treatment to clear existing deposits, then continuous crystal modifier injection to prevent recurrence."
        ],
        reasoning_framework="""
PARAFFIN PROBLEM OVERVIEW:
- Crude oil contains dissolved paraffin waxes (C18-C60 n-alkanes)
- As temperature drops below cloud point, wax crystallizes and deposits
- Deposits restrict flow in tubing, flowlines, separators, tanks
- Common in shallow wells, cold climates, subsea pipelines

PARAFFIN CRYSTAL MODIFIERS (POUR POINT DEPRESSANTS):
Chemistry:
- Copolymers of ethylene-vinyl acetate (EVA)
- Polyacrylates, polymethacrylates
- Alkyl phenol-formaldehyde resins

Mechanism:
- Adsorb onto growing wax crystals during nucleation
- Disrupt crystal lattice formation, prevent large crystal aggregation
- Result: Smaller, dispersed crystals that remain suspended in oil
- Lowers pour point 10-40F (oil stays fluid at lower temperature)

Application:
- MUST inject continuously BEFORE wax crystallizes (above cloud point)
- Typical dose: 50-500 ppm in crude oil
- Inject at wellhead or upstream of temperature drop
- Ineffective for removing existing deposits (prevention only)
- Performance tested via cold finger test or pour point measurement

AROMATIC SOLVENTS (REMEDIATION):
Common solvents:
- Xylene (dimethylbenzene): Strong wax solvent, 280F flash point
- Toluene (methylbenzene): Fast dissolving, 40F flash point (flammable)
- Diesel/kerosene: Safer, slower dissolving, lower cost
- Condensate: Field-available, variable solvency
- Citrus-based (d-limonene): Low toxicity, biodegradable

Mechanism:
- Dissolve paraffin crystals by solvating hydrocarbon chains
- Require contact time (soak) and temperature (heat improves solvency)
- Effectiveness depends on solvent aromaticity and paraffin composition

Application methods:
1. Batch treatment: Bull-head solvent down tubing, soak 4-24 hours, flow back
   - Volume: 5-50 barrels based on deposit thickness and tubing capacity
   - Heat if possible (hot oil, electric line heater) to improve dissolution

2. Circulation: Pump solvent down tubing, return via annulus with deposit debris
   - Requires packer with circulation port or open annulus

3. Solvent squeeze: Inject solvent into formation, soak, produce back
   - For near-wellbore paraffin plugging

Limitations:
- Temporary fix (deposits return without prevention program)
- Flammability and toxicity concerns (confined spaces, H2S)
- Disposal costs for solvent-contaminated fluids
- Can damage downhole elastomers (packers, pump seals)

HOT OIL TREATMENTS:
- Circulate heated oil (150-200F) to melt paraffin deposits
- Requires hot oil truck/unit, tubing circulation capability
- Combines thermal melting + light aromatic solvency
- Effective for heavy deposits that resist chemical solvents
- Risk of thermal shock to casing/tubing (gradual heating required)

MECHANICAL REMOVAL:
1. Pigging: Scraper pigs remove deposits from pipelines
   - Requires pig launcher/receiver, schedule based on deposit rate
   - Chemical batch ahead of pig improves removal efficiency

2. Hot water/steam: Melt and flush deposits (offshore platforms)

3. Wireline scraping tools: Downhole cutters/scrapers for tubing
   - Temporary solution, does not prevent recurrence

INTEGRATED PARAFFIN MANAGEMENT PROGRAM:
1. Initial remediation: Solvent or hot oil treatment to clear existing deposits
2. Prevention: Continuous crystal modifier injection (50-500 ppm)
3. Monitoring: Flowing tubing pressure (FTP) trending, periodic caliper surveys
4. Maintenance: Re-treat when FTP indicates 20% restriction
5. Optimization: Adjust inhibitor dose based on deposit rate, test new chemistries

COLD FLOW TESTING:
- Lab test to evaluate crystal modifier performance
- Chill crude oil sample with/without inhibitor
- Measure pour point, viscosity, crystal size distribution
- Correlate to field conditions (tubing wall temp, flow regime)

COMMON FAILURES:
- Crystal modifier added after deposits form (ineffective)
- Insufficient dosage for heavy paraffin crude (increase to 1000+ ppm)
- Solvent treatment without follow-up prevention (deposits return in weeks)
- Incompatibility: Crystal modifier destabilizes emulsion (bottle test required)
- Wrong solvent: Kerosene used for heavy paraffin (requires aromatic solvent)
""",
        key_factors=[
            "Crystal modifiers prevent wax nucleation, must inject continuously above cloud point",
            "Aromatic solvents dissolve existing deposits but provide no prevention",
            "Typical doses: 50-500 ppm crystal modifier, 5-50 bbl solvent for batch treatment",
            "Hot oil treatment (150-200F) effective for heavy deposits resistant to solvents",
            "Integrated program: solvent remediation + continuous crystal modifier injection",
            "Performance monitoring via flowing tubing pressure and periodic caliper surveys",
            "Compatibility testing required to avoid emulsion issues"
        ],
        primary_authority=[
            "SPE 114363 'Paraffin Deposition and Control in Oil Wells'",
            "NACE Publication 34109 'Review of Paraffin Deposition Research'",
            "Chemical vendor technical bulletins (Baker Hughes, Clariant, Innospec)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PARAFFIN_MANAGEMENT,
        authority_level=AuthorityLevel.INDUSTRY_PRACTICE
    ),

    DoctrineBlock(
        topic="Demulsifier Optimization via Bottle Testing",
        keywords=["demulsifier", "emulsion", "bottle test", "water drop", "oil-water separation"],
        conclusion_template=[
            "Demulsifier selection and dosage optimized through bottle testing: Mix produced emulsion with varying demulsifier concentrations, observe water drop rate and clarity at operating temperature.",
            "Optimal demulsifier provides fastest water drop (minutes vs hours), cleanest oil/water interface, and lowest rag layer volume.",
            "Field dose typically 10-100 ppm based on bottle test results scaled to separator residence time and shear conditions."
        ],
        reasoning_framework="""
EMULSION FORMATION IN OILFIELD:
- Water droplets dispersed in continuous oil phase (W/O emulsion) stabilized by:
  1. Natural surfactants (asphaltenes, resins, naphthenic acids)
  2. Fine solids (clays, corrosion products, scale)
  3. High shear (chokes, pumps, turbulent flow)
- Stable emulsions persist for hours/days without treatment
- Impact: Off-spec crude oil (>1% BS&W), corrosion, equipment fouling

DEMULSIFIER CHEMISTRY:
- Surfactant blends designed to displace natural emulsifiers
- Common components:
  1. Alkylphenol-formaldehyde resins: Primary demulsifier, broad crude compatibility
  2. Polyoxyalkylene polymers (EO/PO block copolymers): Water clarifiers
  3. Amine oxides: Neutralize asphaltene stabilization
  4. Organic solvents: Carrier, improve dispersion (xylene, heavy aromatic naphtha)

- Hydrophilic-Lipophilic Balance (HLB): 4-8 for W/O emulsions
- Tailored formulations for crude properties (TAN, asphaltene content, API gravity)

BOTTLE TEST PROCEDURE:
1. Sample collection:
   - Obtain wellhead or separator emulsion sample (1 quart minimum)
   - Sample at operating temperature if possible
   - Record sample source, temp, pressure, BS&W, API gravity

2. Test setup:
   - Fill 100 mL graduated cylinders with emulsion (duplicate or triplicate)
   - Heat water bath to separator operating temperature (100-150F typical)
   - Add demulsifier at varying concentrations: 0 (blank), 10, 25, 50, 100, 200 ppm
   - Cap and invert 10 times to mix (simulate mechanical agitation)

3. Observation:
   - Place cylinders in water bath
   - Record time to first water drop appearance
   - Measure water volume separated at intervals: 5, 10, 30, 60, 120 minutes
   - Note oil clarity, water clarity, rag layer (emulsion at interface)
   - Photograph at 60 and 120 minutes for documentation

4. Evaluation criteria:
   - Water drop rate: Fastest separation indicates optimal dose
   - Oil quality: Clear, bright oil (low haze, <0.5% BS&W)
   - Water quality: Clear, low oil content (<100 ppm oil in water)
   - Rag layer: Minimum volume at interface (target <2% of total)
   - Over-treatment indicator: Tight emulsion or reverse emulsion (O/W)

INTERPRETING RESULTS:
- Optimal dose: Lowest concentration achieving >90% water drop in 30-60 minutes
- Field dose = Bottle test dose × Safety factor (1.5-3x) for shear, mixing, residence time
- Multiple demulsifiers tested: Select product with best oil/water clarity at lowest dose
- Crude variability: Repeat tests monthly or when crude source changes

FIELD APPLICATION:
- Injection point: Upstream of separator, sufficient mixing but avoid high shear
- Common locations: Wellhead, header, heater treater inlet
- Injection method: Continuous (metering pump) or batch (slug doses)
- Mixing: Low-shear static mixer or natural turbulence (avoid centrifugal pump recycle)
- Residence time: Separator designed for 15-30 minutes retention minimum
- Temperature: Higher temp improves demulsification (heat to 120-150F if crude viscosity allows)

TROUBLESHOOTING POOR PERFORMANCE:
Issue: Field performance worse than bottle test
Causes/Solutions:
- Insufficient mixing: Add static mixer at injection point
- Short-circuiting: Baffles or weir in separator, increase level
- Over-treatment: Reduce dose, may cause re-emulsification
- Crude property change: Re-run bottle test with current crude sample
- Shear: High-pressure drop chokes downstream of injection (relocate upstream)
- Solids interference: Clays/fines stabilize emulsion (add flocculant, centrifuge)
- Temperature: Separator cooler than bottle test (increase heat input)

ADVANCED TESTING:
- Dynamic bottle test: Continuous mixing during test (better simulates separator shear)
- Coalescence time: Measure droplet growth under microscope
- Interfacial tension: Demulsifier reduces IFT, aids coalescence
- Crude compatibility: Mix demulsifier with crude, check for precipitation/sludge

COMMON ERRORS:
- Using old or weathered emulsion sample (results not representative)
- Testing at ambient temp when separator operates at 140F (under-predicts performance)
- Over-treating in field based on bottle test (causes tight emulsion)
- Single product tested (competitor products may outperform at lower cost)
- No follow-up testing when crude changes (seasonal variation, new wells)
""",
        key_factors=[
            "Bottle test procedure: 100 mL emulsion + demulsifier, heat to separator temp, observe water drop rate",
            "Optimal dose provides >90% water drop in 30-60 minutes with clear oil/water, minimal rag layer",
            "Field dose = bottle test dose × 1.5-3x safety factor for mixing and shear effects",
            "Injection upstream of separator with adequate mixing, avoid high-shear pumps/chokes",
            "Re-test monthly or when crude properties change (new wells, seasonal variation)",
            "Troubleshoot poor field performance: verify temp, residence time, mixing, dose rate",
            "Over-treatment causes tight emulsion or reverse emulsion (reduce dose)"
        ],
        primary_authority=[
            "SPE 93274 'Demulsifier Selection and Optimization for Crude Oil Dehydration'",
            "ASTM D4007 'Standard Test Method for Water and Sediment in Crude Oil by the Centrifuge Method'",
            "Demulsifier vendor protocols (Nalco Champion, Baker Hughes, Clariant)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.DEMULSIFIER,
        authority_level=AuthorityLevel.LABORATORY_TEST
    ),

    DoctrineBlock(
        topic="H2S Scavenger Systems - Triazine vs Solid-Based",
        keywords=["h2s scavenger", "hydrogen sulfide", "triazine", "caustic", "iron sponge", "sweetening"],
        conclusion_template=[
            "Triazine-based H2S scavengers react irreversibly with H2S forming non-toxic dithiazine, suitable for liquid phase treatment in pipelines and separators.",
            "Solid scavengers (iron sponge, zinc oxide) adsorb H2S from gas phase, regenerable or disposable, used for wellhead gas sweetening.",
            "Select based on phase (liquid vs gas), H2S concentration, temperature, and disposal requirements."
        ],
        reasoning_framework="""
H2S HAZARD AND REGULATORY LIMITS:
- Hydrogen sulfide: Colorless, toxic gas, 'rotten egg' odor at <1 ppm
- Toxicity: 100 ppm = immediately dangerous, 500 ppm = fatal in minutes
- Corrosivity: Sour corrosion (sulfide stress cracking), requires NACE MR0175 materials
- Regulatory: OSHA PEL 10 ppm (8-hr TWA), 15 ppm ceiling
- Pipeline specs: <4 ppm H2S for sales gas, <10 ppm for crude oil

TRIAZINE-BASED SCAVENGERS (LIQUID PHASE):
Chemistry:
- 1,3,5-tris(2-hydroxyethyl)hexahydro-s-triazine (MEA-triazine)
- Reacts with H2S: 3 H2S + Triazine → Dithiazine + H2O
- Reaction irreversible, non-regenerable
- Stoichiometry: 1 lb triazine neutralizes ~0.75 lb H2S

Application:
- Inject into produced water, crude oil, or wet gas streams
- Dose: 2-5x stoichiometric requirement (H2S varies, safety margin)
- Example: 100 ppm H2S in water → 300-500 ppm triazine dose
- Injection point: Upstream of vessels where H2S liberation occurs (separators, tanks)
- Reaction time: 5-15 minutes for 95% removal
- Temperature limit: Effective up to 250F, degrades above 300F

Advantages:
- Fast reaction kinetics, handles slugs of H2S
- Liquid injection, easy to meter and control
- Low toxicity reaction products (dithiazine)
- Suitable for offshore (no solid waste)

Disadvantages:
- Chemical cost increases with H2S loading
- Reaction products increase TDS in water (disposal concern)
- Not regenerable (continuous consumption)
- Can form stable emulsions if overdosed

Monitoring:
- H2S test strips or electronic monitors downstream
- Target: <10 ppm H2S in treated fluid
- Over-treatment: Excess triazine odor (amine-like smell)

SOLID-BASED SCAVENGERS (GAS PHASE):
1. Iron Sponge (Iron Oxide):
   - Ferric oxide (Fe2O3) impregnated on wood chips or ceramic media
   - Reaction: Fe2O3 + 3 H2S → Fe2S3 + 3 H2O
   - Capacity: 10-20 lb H2S per 100 lb media
   - Regeneration: Air oxidation converts sulfide back to oxide (exothermic, fire risk)
   - Disposal: Spent media pyrophoric when dry (water-wet for disposal)
   - Temperature limit: <110F (higher temp accelerates degradation)
   - Cost: Low, suitable for low H2S (<100 ppm) wellhead applications

2. Zinc Oxide (ZnO):
   - Reaction: ZnO + H2S → ZnS + H2O
   - Capacity: 25-35 lb H2S per 100 lb media
   - Non-regenerable, higher capacity than iron sponge
   - Effective up to 750F (amine plant tail gas treating)
   - Disposal: Landfill acceptable (non-hazardous waste)

3. Caustic Scrubbing (NaOH):
   - Reaction: 2 NaOH + H2S → Na2S + 2 H2O
   - Liquid-gas contact tower (packed bed or spray)
   - Handles high H2S concentrations (>1000 ppm)
   - Regeneration: Not practical for small scale
   - Disposal: Sulfide-contaminated caustic (treatment required)
   - Cost: Higher CAPEX (tower, pumps), lower OPEX for high H2S

DESIGN CONSIDERATIONS:
Vessel sizing (iron sponge):
- Flow rate: GHSV (gas hourly space velocity) = 200-400 hr⁻¹
- Example: 1 MMSCFD gas → Vessel volume = 1,000,000/(24×300) = 139 ft³
- Bed depth: 3-6 ft minimum for contact time
- Pressure drop: <1 psi across bed (avoid channeling)

Breakthrough monitoring:
- Install H2S monitor downstream of vessel
- Replace media when H2S breakthrough occurs (typically >1 ppm)
- Media life: 3-12 months depending on H2S loading

Regeneration (iron sponge):
- Shut off gas flow, introduce air at 1-2% O2 in gas
- Exothermic reaction raises bed temperature (monitor for hot spots >150F)
- Over-oxidation risk: Media combustion (requires water spray cooling)
- Regeneration cycles: 5-10 before replacement

SELECTION CRITERIA:
| Factor | Triazine | Iron Sponge | ZnO | Caustic |
|--------|----------|-------------|-----|---------|
| Phase | Liquid/wet gas | Dry gas | Dry gas | Gas |
| H2S ppm | Any | <500 | <1000 | >1000 |
| CAPEX | Low | Low | Medium | High |
| OPEX | High | Low | Medium | Medium |
| Regenerable | No | Yes (limited) | No | No |
| Temperature | <250F | <110F | <750F | <200F |
| Disposal | Water treatment | Hazmat | Landfill | Treatment |

COMBINED SYSTEMS:
- Three-stage: Iron sponge (bulk removal) → Triazine (polishing) → Monitoring
- Seasonal: Solid scavenger in winter (low gas rates), triazine in summer (high rates)
- Offshore: Triazine only (no solid waste handling)

COMMON ERRORS:
- Iron sponge for wet gas (media clumping, channeling, poor contact)
- Triazine under-dosing during H2S surges (breakthrough to downstream equipment)
- No regeneration of iron sponge (premature replacement, high cost)
- Dry spent iron sponge disposal (pyrophoric ignition hazard)
- Caustic for low H2S (over-designed, high cost vs iron sponge)
""",
        key_factors=[
            "Triazine scavengers for liquid phase, 2-5x stoichiometric dose, fast reaction (5-15 min)",
            "Iron sponge for dry gas <500 ppm H2S, regenerable via air oxidation, pyrophoric when dry",
            "Zinc oxide for higher H2S (<1000 ppm) or high temp (<750F), non-regenerable, landfill disposal",
            "Caustic scrubbing for high H2S (>1000 ppm) gas streams, higher CAPEX, sulfide-contaminated waste",
            "Monitor H2S downstream, target <10 ppm in treated fluid/gas",
            "Iron sponge regeneration: 1-2% O2, monitor bed temp (<150F to avoid combustion)",
            "Select based on phase, H2S concentration, temperature, and disposal options"
        ],
        primary_authority=[
            "NACE MR0175/ISO 15156 'Petroleum and Natural Gas Industries - Materials for Use in H2S Environments'",
            "GPA 2172 'Sulfur Recovery Guidelines'",
            "Scavenger vendor technical data (Merichem, SulfaTreat, M-I SWACO)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.H2S_SCAVENGER,
        authority_level=AuthorityLevel.INDUSTRY_PRACTICE
    ),

    DoctrineBlock(
        topic="Biocide Programs for Microbiological Control",
        keywords=["biocide", "bacteria", "srb", "apb", "glutaraldehyde", "thps", "oxidizing", "microbiological corrosion"],
        conclusion_template=[
            "Biocides control sulfate-reducing bacteria (SRB), acid-producing bacteria (APB), and slime-forming bacteria that cause microbiologically influenced corrosion (MIC) and reservoir souring.",
            "Non-oxidizing biocides (glutaraldehyde, THPS, quaternary amines) for continuous dosing, oxidizing biocides (chlorine, bromine) for shock treatments.",
            "Monitor effectiveness via bacteria counts (BART tests, culture vials), sulfide production, and sessile bacteria on coupons."
        ],
        reasoning_framework="""
MICROBIOLOGICAL THREATS IN OILFIELD:

1. SULFATE-REDUCING BACTERIA (SRB):
   - Anaerobic bacteria reduce sulfate (SO4²⁻) to sulfide (S²⁻/H2S)
   - Reaction: SO4²⁻ + Organic carbon → H2S + CO2
   - Problems: MIC (pitting corrosion), H2S souring, biofouling
   - Detection: Black iron sulfide precipitates, H2S smell, BART test positive in 1-4 days
   - Common genera: Desulfovibrio, Desulfotomaculum

2. ACID-PRODUCING BACTERIA (APB):
   - Aerobic/facultative bacteria produce organic acids (acetic, formic, lactic)
   - Lower pH at steel surface → accelerated general corrosion
   - Detection: pH drop in produced water, APB BART test positive

3. SLIME-FORMING BACTERIA:
   - Produce extracellular polymeric substances (EPS) biofilm
   - Biofilm shields SRB from biocides, creates oxygen concentration cells (pitting)
   - Fouling of heat exchangers, filters, injection wells (plugging)

4. IRON-OXIDIZING/REDUCING BACTERIA:
   - Participate in redox corrosion reactions
   - Iron bacteria tubercles create differential aeration cells

BIOCIDE TYPES:

NON-OXIDIZING BIOCIDES (Continuous Dosing):

1. Glutaraldehyde:
   - Aldehyde chemistry, cross-links bacterial proteins
   - Dose: 50-200 ppm continuous, 500-1000 ppm batch
   - pH dependent: More effective at pH 7-8.5 (degrades at pH >9)
   - Temperature limit: Effective up to 200F
   - Broad spectrum: SRB, APB, slime formers
   - Low toxicity to higher organisms, biodegradable
   - Caution: Can polymerize at high pH or temp (fouling)

2. THPS (Tetrakis Hydroxymethyl Phosphonium Sulfate):
   - Organophosphorus compound, disrupts cell membranes
   - Dose: 25-100 ppm continuous, 250-500 ppm batch
   - Advantages: Effective at high temp (>250F), high salinity, H2S environments
   - Breaks down to phosphate (can serve as nutrient at low dose)
   - Used in waterfloods, downhole squeeze treatments

3. Quaternary Ammonium Compounds (Quats):
   - Cationic surfactants, disrupt cell membrane
   - Dose: 25-100 ppm continuous
   - Advantages: Low cost, broad spectrum, compatible with corrosion inhibitors
   - Disadvantages: Foaming, surfactant properties can cause emulsions
   - Adsorbs to formation rock (can plug injection wells)

4. Isothiazolones (MIT, BIT):
   - Effective at low dose (5-25 ppm)
   - Temperature limit: <140F (degrades rapidly above)
   - Often blended with glutaraldehyde for synergy

OXIDIZING BIOCIDES (Shock Treatments):

1. Chlorine/Hypochlorite (NaOCl, Ca(OCl)2):
   - Oxidizes bacterial cell components
   - Dose: 50-200 ppm free chlorine, batch treatment
   - Advantages: Low cost, rapid kill
   - Disadvantages: Corrosive to steel (requires corrosion inhibitor), reacts with H2S/ammonia (loses effectiveness)
   - Effective for surface facilities, not downhole (high chloride demand)

2. Chlorine Dioxide (ClO2):
   - More stable than chlorine, effective over wider pH range
   - Less corrosive than chlorine
   - Generated on-site (unstable in storage)
   - Used in water injection systems

3. Peracetic Acid:
   - Strong oxidizer, breaks down to acetic acid + oxygen
   - Effective at low temp and high organic loading
   - Expensive, limited oilfield use

DOSING STRATEGY:

Continuous Low-Dose (Prevention):
- Maintains planktonic bacteria at <10³ CFU/mL
- Dose: 25-100 ppm non-oxidizing biocide
- Injection point: Water source, injection pump suction, header
- Used in: Waterfloods, production facilities, pipelines

Batch Treatment (Remediation):
- Kills established biofilm and sessile bacteria
- Dose: 500-2000 ppm non-oxidizing or 100-500 ppm oxidizing
- Soak time: 6-24 hours for biofilm penetration
- Used in: Waterflood wells (squeeze), fouled equipment, startup commissioning

Alternating Biocides:
- Rotate between biocide types monthly or quarterly
- Prevents bacterial resistance development
- Example: Glutaraldehyde 2 months → THPS 2 months → Quat 2 months

MONITORING EFFECTIVENESS:

BART (Biological Activity Reaction Test):
- Field test vials with selective media
- SRB BART: Incubate water sample, black color = SRB positive (1-7 days)
- APB BART: Yellow color change = APB positive
- Semi-quantitative: Faster reaction = higher bacteria count
- Frequency: Weekly during startup, monthly during normal operation

Heterotrophic Plate Count (HPC):
- Lab culture method, quantifies total viable bacteria (CFU/mL)
- Target: <10³ CFU/mL for waterflood, <10⁴ CFU/mL for production
- Requires 2-7 days incubation

Sessile Bacteria Monitoring:
- Retrieve corrosion coupons after 30-90 day exposure
- Culture biofilm from coupon surface
- Indicates effectiveness of biocide reaching pipe wall (vs planktonic only)

Sulfide Production:
- Measure H2S in produced water or injection water returns
- Increasing H2S indicates SRB activity (biocide insufficient)

ATP (Adenosine Triphosphate) Testing:
- Measures cellular energy molecule (all living cells)
- Rapid test (minutes), correlates to total biomass
- Expressed as RLU (relative light units)

WATER INJECTION WELL BIOCIDE SQUEEZE:
1. Displace wellbore with freshwater (reduce salinity for biocide effectiveness)
2. Inject 50-100 bbl biocide solution (1000-2000 ppm active)
3. Overflush with 50-100 bbl freshwater
4. Shut in 12-24 hours (soak time for biofilm kill)
5. Resume injection, monitor bacteria returns for 30+ days
6. Re-squeeze when bacteria counts exceed threshold

COMPATIBILITY ISSUES:
- Oxidizing biocides + H2S: Consume biocide, form sulfur precipitate (ineffective)
- Glutaraldehyde + high pH: Polymerization, fouling
- Quats + anionic surfactants: Precipitation (incompatible with some demulsifiers)
- Chlorine + corrosion inhibitor: Can deactivate inhibitor (test before blending)

COMMON FAILURES:
- Continuous dosing too low (bacteria adapt, develop resistance)
- Batch treatment with insufficient soak time (biofilm survives)
- No monitoring (assuming biocide is working without verification)
- Single biocide used for years (bacterial resistance, rotate types)
- Oxidizing biocide in H2S-containing water (instant consumption, no kill)
- Biocide injected after bacteria established (biofilm shields cells, increase dose or mechanical cleaning first)
""",
        key_factors=[
            "Non-oxidizing biocides (glutaraldehyde 50-200 ppm, THPS 25-100 ppm) for continuous dosing",
            "Oxidizing biocides (chlorine 50-200 ppm) for batch shock treatments in H2S-free systems",
            "Monitor effectiveness via BART tests (SRB/APB), bacteria counts (<10³ CFU/mL), H2S production",
            "Rotate biocide types (glutaraldehyde, THPS, quats) to prevent bacterial resistance",
            "Batch treatments: 500-2000 ppm, 6-24 hour soak time to penetrate biofilm",
            "Water injection well squeeze: 1000-2000 ppm biocide, 12-24 hr shut-in, monitor returns 30+ days",
            "Compatibility: Oxidizing biocides ineffective in H2S-containing water, quats incompatible with anionic surfactants"
        ],
        primary_authority=[
            "NACE TM0194 'Field Monitoring of Bacterial Growth in Oil and Gas Systems'",
            "NACE SP0175 'Design, Installation, Operation, and Maintenance of Microbiologically Influenced Corrosion Control Systems'",
            "API RP 38 'Biological Analysis of Subsurface Injection Waters'"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.BIOCIDE,
        authority_level=AuthorityLevel.INDUSTRY_PRACTICE
    ),

    DoctrineBlock(
        topic="Chemical Dosing Rate Optimization via MEC Testing",
        keywords=["minimum effective concentration", "mec", "dosing optimization", "cost per boe", "performance testing"],
        conclusion_template=[
            "Minimum Effective Concentration (MEC) testing determines lowest chemical dose achieving performance target, optimizing cost without sacrificing protection.",
            "Methodology: Reduce dose incrementally (e.g., 100 → 75 → 50 ppm), monitor performance metric (corrosion rate, residual, water drop), identify threshold where performance degrades.",
            "Re-optimize quarterly or when production conditions change (water cut, temperature, production rate)."
        ],
        reasoning_framework="""
MINIMUM EFFECTIVE CONCENTRATION (MEC) CONCEPT:
- MEC: Lowest chemical concentration achieving desired performance outcome
- Below MEC: Performance degrades (corrosion breakthrough, scale formation, emulsion)
- Above MEC: Marginal benefit, unnecessary cost
- Goal: Operate just above MEC with 10-20% safety margin

PERFORMANCE METRICS BY CHEMICAL TYPE:

1. Corrosion Inhibitor MEC:
   - Metric: Corrosion rate <2 mils per year (mpy)
   - Measurement: Weight loss coupons (30-90 day), ER probes (real-time), iron counts (<5 ppm)
   - Typical MEC: 10-30 ppm residual in produced water
   - Optimization: Start at 50 ppm, reduce to 40 → 30 → 20 ppm, monitor corrosion rate
   - If rate exceeds 2 mpy at 20 ppm → MEC is 25-30 ppm

2. Scale Inhibitor MEC:
   - Metric: No scale deposition, pressure drop stable
   - Measurement: Residual in produced water, visual inspection, pressure monitoring
   - Typical MEC: 5-20 ppm residual
   - Optimization: Reduce squeeze treatment concentration or frequency until scale detected

3. Demulsifier MEC:
   - Metric: Oil BS&W <1%, water oil content <100 ppm
   - Measurement: Centrifuge BS&W, oil-in-water analyzer
   - Typical MEC: 10-50 ppm in crude oil
   - Optimization: Reduce dose until emulsion persists or off-spec product

4. Paraffin Inhibitor MEC:
   - Metric: Flowing tubing pressure (FTP) stable, no restriction
   - Measurement: FTP trending, caliper survey
   - Typical MEC: 50-200 ppm in crude oil
   - Optimization: Reduce dose until FTP increases (indicates deposit buildup)

5. Biocide MEC:
   - Metric: Bacteria count <10³ CFU/mL, no H2S increase
   - Measurement: BART tests, HPC culture, H2S monitoring
   - Typical MEC: 25-100 ppm continuous dose
   - Optimization: Reduce dose until bacteria count spikes or H2S increases

MEC TESTING PROCEDURE:

Step 1: Establish Baseline
- Operate at current dose for 2-4 weeks
- Document performance: Corrosion rate, residual, product quality, bacteria count
- Ensure system stable before testing (no upsets, shutdowns, production changes)

Step 2: Incremental Dose Reduction
- Reduce chemical dose by 20-25% (e.g., 100 → 75 ppm)
- Maintain new dose for 2-4 weeks (allow system equilibration)
- Monitor performance metrics closely (weekly sampling minimum)

Step 3: Continue Reduction
- If performance remains acceptable, reduce dose another 20-25% (75 → 55 ppm)
- Repeat monitoring period
- Continue stepwise reduction until performance degrades

Step 4: Identify MEC Threshold
- When performance metric exceeds target (e.g., corrosion >2 mpy, scale detected):
  - MEC = Previous dose level (last dose with acceptable performance)
  - Example: Performance OK at 55 ppm, degrades at 40 ppm → MEC = 55 ppm

Step 5: Set Operating Dose
- Operating dose = MEC × Safety factor (1.1-1.2)
- Example: MEC 55 ppm → Operating dose 60-65 ppm (10-20% margin)
- Safety factor accounts for: Production upsets, crude variability, measurement error

COST-BENEFIT ANALYSIS:

Calculate cost per barrel of oil equivalent (BOE):
- Chemical cost = (Dose ppm × Flow rate bbl/day × 42 gal/bbl × 8.34 lb/gal / 1,000,000) × Chemical $/lb
- Example: 50 ppm corrosion inhibitor, 500 BOPD, $5/lb chemical
  - Daily lb = (50 × 500 × 42 × 8.34 / 1,000,000) = 8.76 lb/day
  - Daily cost = 8.76 × $5 = $43.80/day
  - Cost per BOE = $43.80 / 500 = $0.088/BOE

Optimization savings:
- Reduce dose from 100 ppm to 60 ppm (MEC 55 ppm + 10% margin)
- Savings = (100-60)/100 = 40% reduction
- Annual savings = $43.80 × 365 × 0.4 = $6,394 per well

Multiply by well count:
- 100 wells × $6,394 = $639,400 annual savings

RE-OPTIMIZATION TRIGGERS:
- Production changes: Water cut increase/decrease, new wells added, rate changes
- Seasonal: Temperature variation affects chemical effectiveness
- Crude source change: Different reservoir, commingled production
- Scheduled: Quarterly or bi-annual re-testing as best practice
- Failure: If performance degrades, increase dose back to previous level

ADVANCED OPTIMIZATION: MULTIVARIATE TESTING:
- Test multiple chemicals simultaneously (corrosion inhibitor + scale inhibitor)
- Design of Experiments (DOE): Matrix of dose combinations
- Identify optimal blend ratio and total dose
- Example: 50 ppm corrosion inhibitor + 20 ppm scale inhibitor may outperform 75 ppm + 30 ppm

AUTOMATED DOSING CONTROL:
- Install online monitoring: Corrosion ER probe, residual analyzer, flow meter
- Feed monitoring data to PLC/DCS controlling chemical pump
- Auto-adjust dose to maintain target residual or corrosion rate
- Advanced: Machine learning models predict optimal dose based on production conditions

COMMON ERRORS:
- Testing during production upset period (results not representative)
- Insufficient monitoring frequency (miss early signs of degradation)
- No safety margin (operate exactly at MEC, no buffer for variability)
- One-time test (never re-optimize despite changing conditions)
- Ignoring crude/water variability (MEC changes but dose remains static)
- Cost-cutting below MEC (short-term savings, long-term equipment damage)
""",
        key_factors=[
            "MEC testing: Reduce dose incrementally (20-25% steps), monitor performance 2-4 weeks per level",
            "Performance metrics: Corrosion rate <2 mpy, scale residual 5-20 ppm, BS&W <1%, bacteria <10³ CFU/mL",
            "Operating dose = MEC × 1.1-1.2 safety factor for production variability",
            "Cost per BOE calculation: (Dose × Flow × 42 × 8.34 / 1,000,000) × Chemical $/lb / BOE/day",
            "Re-optimize quarterly or when water cut, temperature, or crude source changes",
            "Multivariate testing optimizes chemical blend ratios and total dose",
            "Avoid operating below MEC (equipment damage exceeds chemical cost savings)"
        ],
        primary_authority=[
            "SPE 184554 'Chemical Treatment Optimization Using Minimum Effective Concentration'",
            "NACE Corrosion Journal articles on inhibitor performance testing",
            "Chemical vendor optimization protocols (Nalco Champion, Baker Hughes)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.DOSING_OPTIMIZATION,
        authority_level=AuthorityLevel.INDUSTRY_PRACTICE
    ),

    DoctrineBlock(
        topic="Chemical Compatibility Testing Protocol",
        keywords=["compatibility", "precipitation", "white-out test", "chemical mixing", "incompatibility"],
        conclusion_template=[
            "Chemical compatibility testing prevents precipitation, phase separation, or performance degradation when mixing oilfield treatment chemicals or blending with produced fluids.",
            "Standard tests: Visual white-out (precipitation), viscosity change, phase separation, performance verification (corrosion coupon, bottle test).",
            "Test before field deployment: New chemical, chemical blend changes, produced fluid chemistry changes, or temperature/pressure changes."
        ],
        reasoning_framework="""
CHEMICAL INCOMPATIBILITY RISKS:
- Precipitation: Insoluble solids form, plug injection lines, coat equipment
- Phase separation: Chemicals partition into separate phases, uneven distribution
- Deactivation: Chemicals react, neutralize active ingredients
- Synergistic problems: Stable emulsions, foam, increased viscosity
- Corrosion acceleration: Some chemical combinations increase corrosivity

COMMON INCOMPATIBILITIES:

1. Corrosion Inhibitor + Scale Inhibitor:
   - Cationic corrosion inhibitor (amine-based) + Anionic scale inhibitor (phosphonate, polymer)
   - Risk: Electrostatic attraction → precipitation
   - Test: Mix at field concentrations, observe for haze/precipitate

2. Demulsifier + Corrosion Inhibitor:
   - Both are surfactants, can interfere with interfacial activity
   - Risk: Tight emulsion, reduced demulsification
   - Test: Bottle test with both chemicals vs demulsifier alone

3. Biocide + Reducing Agents:
   - Oxidizing biocide (chlorine) + H2S, sulfite, or organic reducing agents
   - Risk: Biocide consumed, no bacterial kill
   - Test: Chlorine residual measurement after mixing

4. Scale Inhibitor + Formation Brine:
   - High-calcium/magnesium brine + phosphonate scale inhibitor
   - Risk: Calcium phosphonate precipitation
   - Test: White-out test (mix inhibitor solution with formation brine)

5. Chemicals + High-Salinity Water:
   - Some chemicals salt out (become insoluble) at high TDS
   - Risk: Precipitation in injection water or downhole
   - Test: Mix with actual injection/formation water

6. Temperature Effects:
   - Chemical solubility decreases at low temp (winter storage, subsea)
   - Thermal degradation at high temp (>250F downhole)
   - Test: Chill to minimum expected temp, heat to maximum expected temp

COMPATIBILITY TEST PROCEDURES:

WHITE-OUT TEST (Precipitation):
1. Mix produced water or synthetic brine (match field salinity, hardness, pH)
2. Add chemical 1 at field concentration (e.g., 100 ppm scale inhibitor)
3. Add chemical 2 at field concentration (e.g., 50 ppm corrosion inhibitor)
4. Shake/agitate to mix thoroughly
5. Observe immediately and after 1, 4, 24 hours
6. Record: Clear = compatible, Haze = marginal, Precipitate = incompatible
7. Repeat at field temperature (heat to 100-150F if applicable)

PHASE SEPARATION TEST:
1. Mix chemicals in graduated cylinder
2. Let stand 24-48 hours at field temperature
3. Observe: Single homogeneous phase = compatible, Layers = incompatible
4. Common with oil-soluble vs water-soluble chemical mixtures

VISCOSITY TEST:
1. Measure viscosity of chemical 1 alone
2. Measure viscosity of chemical 2 alone
3. Measure viscosity of blended solution
4. Acceptable: Blend viscosity ≤ 1.5× higher individual component
5. Concern: Dramatic viscosity increase (gel formation, polymer cross-linking)

PERFORMANCE VERIFICATION TESTS:

Corrosion Inhibitor Compatibility:
- Weight loss coupons with: Inhibitor A alone, Inhibitor B alone, A+B blend
- Expose for 7-30 days in synthetic brine or produced water
- Compare corrosion rates: Blend should be ≤ either individual inhibitor
- If blend rate >individual, chemicals interfering (incompatible)

Demulsifier Compatibility:
- Bottle test with: Demulsifier A alone, A+corrosion inhibitor, A+scale inhibitor
- Compare water drop rate and oil/water clarity
- If blend degrades performance, chemicals incompatible

Scale Inhibitor Compatibility:
- Dynamic scale loop test: Flow brine at scaling conditions with/without inhibitor blend
- Measure: Scale deposition rate, pressure drop, effluent hardness
- Blend should prevent scale as effectively as inhibitor alone

Biocide Compatibility:
- BART or HPC test with: Biocide alone, Biocide + other chemicals
- Bacteria kill rate should be equivalent (blend does not deactivate biocide)

FIELD INJECTION COMPATIBILITY:
- Test chemical package (all chemicals blended) with injection water
- Inject small volume (5-10 bbl) through temporary test line
- Monitor for: Pressure increase (plugging), precipitation in sample, phase separation
- If test fails, inject chemicals at separate points or reformulate blend

STORAGE STABILITY:
- Store chemical blend at field conditions (temp, container material)
- Sample weekly for 4 weeks
- Test: Viscosity, phase separation, active ingredient concentration (titration)
- Reject if properties change >10% over storage period

DOCUMENTATION:
Record for each compatibility test:
- Chemical names, concentrations, batch numbers
- Water composition (TDS, hardness, pH, temperature)
- Test method and duration
- Visual observations (photos)
- Quantitative results (corrosion rate, viscosity, bacteria count)
- Pass/Fail decision and rationale
- Date, technician name, lab location

REGULATORY/SAFETY COMPATIBILITY:
- SDS (Safety Data Sheet) review: Check for incompatible materials listed
- GHS classification: Oxidizers + flammables, acids + bases = UNSAFE
- Example: Never store oxidizing biocide (chlorine) near flammable solvents
- Storage segregation required by fire code and OSHA

COMMON ERRORS:
- Testing at dilute concentration (incompatibility may only occur at field strength)
- Testing at ambient temp (problems appear at field temp 100-150F)
- Short observation time (precipitation can take hours to develop)
- Not testing with actual produced fluids (synthetic brine may not reveal issues)
- Assuming vendor 'compatible' claims (always verify with field-specific test)
- Mixing concentrated chemicals (never mix concentrates, dilute first)
""",
        key_factors=[
            "White-out test: Mix chemicals at field concentrations in produced water, observe for haze/precipitate",
            "Test conditions match field: Salinity, temperature, pH, chemical ratios",
            "Performance verification: Corrosion coupons, bottle tests, bacteria kill rates with blended chemicals",
            "Observation period: 1, 4, 24 hours minimum, 7-30 days for corrosion/biocide tests",
            "Common incompatibilities: Cationic + anionic chemicals, oxidizers + reducers, high hardness + phosphonates",
            "Storage stability: Test chemical blend at field temp for 4 weeks, viscosity/concentration change <10%",
            "Re-test when: New chemical, produced fluid changes, temperature changes, or blend ratio changes"
        ],
        primary_authority=[
            "NACE TM0374 'Laboratory Screening Tests to Determine the Ability of Scale Inhibitors to Prevent the Precipitation of Calcium Sulfate and Calcium Carbonate'",
            "ASTM D4740 'Standard Test Method for Cleanliness and Compatibility of Residual Fuels by Spot Test'",
            "Chemical vendor compatibility matrices and test protocols"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CHEMICAL_COMPATIBILITY,
        authority_level=AuthorityLevel.LABORATORY_TEST
    ),

    DoctrineBlock(
        topic="Chemical Inventory and Tote Farm Management",
        keywords=["chemical storage", "tote", "bulk tank", "inventory", "spill containment", "material handling"],
        conclusion_template=[
            "Chemical tote farm design requires spill containment (110% of largest vessel), secondary containment, proper ventilation, and segregation of incompatible chemicals.",
            "Inventory management tracks usage rates, reorder points, and shelf life to prevent stockouts and chemical degradation.",
            "Material handling procedures include PPE requirements, spill response, and compatibility with transfer equipment (pumps, hoses, fittings)."
        ],
        reasoning_framework="""
CHEMICAL STORAGE VESSEL TYPES:

1. Totes (IBC - Intermediate Bulk Container):
   - Standard: 275 gallon (1000 liter) UN-rated composite (HDPE inner, steel cage)
   - Advantages: Stackable, forklift-movable, returnable/refillable, standard fittings
   - Disadvantages: Limited to 1.9 specific gravity (some chemicals require steel drums)
   - Fittings: 2-inch ball valve bottom outlet, 6-inch top fill cap, vent
   - Lifespan: 5-10 years with proper handling

2. Bulk Tanks:
   - Sizes: 500-10,000 gallon vertical or horizontal
   - Materials: Polyethylene, fiberglass, steel (coated for corrosive chemicals)
   - Advantages: Lower cost per gallon, fewer deliveries, less handling
   - Disadvantages: Permanent installation, larger footprint, require pump systems
   - Level monitoring: Sight glass, float switch, ultrasonic level transmitter

3. Day Tanks:
   - Small tanks (50-100 gallon) near injection point for chemical pump suction
   - Fed from bulk tank or tote via transfer pump
   - Advantages: Maintains flooded suction for metering pump, reduces pump cavitation
   - Float switch auto-refills from bulk storage

TOTE FARM DESIGN REQUIREMENTS:

Spill Containment:
- Regulatory: EPA 40 CFR 112 (SPCC - Spill Prevention, Control, and Countermeasures)
- Requirement: Containment capacity ≥ 110% of largest vessel within containment
- Example: Four 275-gal totes → Containment = 275 × 1.10 = 302.5 gallon minimum
- Construction: Concrete pad with bermed walls, or prefab polyethylene spill pallets
- Drainage: Sump with manual valve (normally closed) for rainwater removal after inspection

Secondary Containment:
- Double-walled totes or tanks for high-hazard chemicals (toxics, RCRA)
- Leak detection between primary and secondary wall (vacuum monitor, sensor)

Ventilation:
- Outdoor storage preferred (natural ventilation)
- Indoor storage: Mechanical ventilation, explosion-proof if flammable chemicals
- Vent totes to atmosphere (pressure equalization during filling/dispensing)

Segregation:
- Acids separated from bases (3-foot minimum, or separate containment area)
- Oxidizers separated from flammables (per NFPA 400)
- Incompatible chemicals: Refer to SDS Section 10 (Stability and Reactivity)
- Color-code totes or labels for visual identification

Environmental Protection:
- Impermeable surface (concrete, asphalt, or liner) prevents soil contamination
- Cover or roof (optional): Protects chemicals from sunlight (UV degradation), rain dilution
- Freeze protection: Heat trace or insulated enclosure for winter storage in cold climates
- Heating: Maintain chemicals above pour point (some scale inhibitors solidify <50F)

Fire Protection:
- Fire extinguisher (Type ABC) accessible within 50 feet
- Flammable chemical storage: Bonding/grounding straps during transfer (static ignition)
- Fire-rated separation from buildings, ignition sources (per NFPA 30)

Security:
- Fencing or enclosure (prevent vandalism, unauthorized access)
- Locks on chemical feed buildings
- Signage: Chemical name, hazard labels (NFPA diamond, GHS pictograms)

INVENTORY MANAGEMENT SYSTEM:

Tracking Methods:
1. Manual logs: Paper log sheet per chemical, record deliveries and usage
2. Spreadsheet: Excel with columns: Chemical, Date, Delivered (gal), Used (gal), Balance (gal)
3. Automated: Tank level monitors → SCADA/DCS, real-time inventory and usage trends
4. Barcode/RFID: Scan totes on delivery/disposal, track individual vessel history

Key Metrics:
- Usage rate: Gallons per day or per barrel oil produced
- Reorder point: Inventory level triggering next order
- Lead time: Days from order to delivery (account for supplier shipping time)
- Safety stock: Buffer inventory for usage variability or delivery delays
- Reorder point = (Usage rate × Lead time) + Safety stock

Example Calculation:
- Corrosion inhibitor: 5 gal/day usage, 7-day lead time, 3-day safety stock
- Reorder point = (5 × 7) + (5 × 3) = 35 + 15 = 50 gallons
- When inventory drops to 50 gallons → place order

Par Levels:
- Minimum: Reorder point (triggers order)
- Maximum: Storage capacity or economic order quantity (EOQ)
- Target: Midpoint between min and max (minimize stockouts and overstocking)

Shelf Life Management:
- Most oilfield chemicals: 6-24 month shelf life (check SDS Section 10)
- FIFO (First In, First Out): Use oldest inventory first
- Mark totes with received date, rotate stock
- Expired chemicals: Contact vendor for disposal or return (do not use past shelf life)

Economic Order Quantity (EOQ):
- Balances ordering cost vs holding cost
- EOQ = sqrt((2 × Annual usage × Order cost) / Holding cost per unit)
- Larger orders → lower per-gallon price, but higher inventory holding cost
- Consider: Bulk discounts, storage capacity, capital tied up in inventory

MATERIAL HANDLING PROCEDURES:

Personal Protective Equipment (PPE):
- Minimum: Safety glasses, chemical-resistant gloves (nitrile, neoprene), steel-toe boots
- For corrosives/toxics: Face shield, chemical apron, respiratory protection (if inadequate ventilation)
- Refer to SDS Section 8 (Exposure Controls/Personal Protection)

Transfer Equipment:
- Pumps: Chemical-compatible (polypropylene, PVDF, 316SS for corrosives)
- Air-operated diaphragm (AOD) pumps: Common for tote transfer (no electric motor, explosion-proof)
- Hoses: Chemical-resistant (Viton, EPDM, PTFE liner), pressure-rated, inspect for cracks/leaks
- Fittings: Camlock or threaded, compatible with tote outlet (2-inch NPT or camlock typical)
- Bonding/grounding: Connect tote and receiving vessel to prevent static discharge (flammables)

Tote Handling:
- Forklift with IBC attachment or pallet forks
- Inspect tote before moving: Cracks, leaks, secure valve
- Do not stack >2 high unless manufacturer-rated (risk of bottom tote collapse)
- Secure totes during transport (straps, prevent shifting/tipping)

Spill Response:
- Spill kit on-site: Absorbent pads, boom, neutralizer (for acids/bases), disposal bags, PPE
- Small spill (<5 gal): Contain with absorbent, clean up, dispose per regulations
- Large spill (>RQ): Report to OSBP National Response Center (if hazardous material, >RQ threshold)
- Spill reporting quantities: 40 CFR 302 (e.g., sulfuric acid >1000 lb)

REGULATORY COMPLIANCE:

SPCC Plan (Spill Prevention, Control, and Countermeasures):
- Required if: Oil storage >1,320 gallons aboveground (aggregate), or >42,000 gallons buried
- Plan elements: Site diagram, spill containment, drainage, loading/unloading procedures
- PE certification (if >10,000 gal capacity or history of spills)
- Review every 5 years or upon facility change

Tier II Reporting (EPCRA):
- Required if: Hazardous chemical storage >10,000 lb (or EHS >500 lb/TPQ)
- Report to: SERC (State Emergency Response Commission), LEPC (Local), fire department
- Annual submission (by March 1) with chemical names, quantities, locations

DOT Placarding:
- Totes in transport: UN1760, 1993, etc. placards based on chemical class
- Bill of lading required, driver training, shipping papers

Waste Disposal:
- Empty totes: Triple-rinsed = non-hazardous (40 CFR 261.7)
- Unusable chemicals: Manifest as hazardous waste (if RCRA-listed or characteristic)
- Vendor take-back programs: Many suppliers accept returnable totes (deposit refund)

COMMON ERRORS:
- Undersized containment (does not meet 110% rule, fails inspection)
- No segregation (acids stored next to bases, creates hazard)
- Poor inventory tracking (run out of critical chemical, production downtime)
- Using expired chemicals (reduced effectiveness, may have degraded)
- No spill kit (unable to respond to leak/spill, regulatory violation)
- Overfilling totes (overflow during thermal expansion)
- No labels (unable to identify chemical after label falls off, safety hazard)
""",
        key_factors=[
            "Spill containment ≥110% of largest vessel capacity, impermeable surface, manual drainage valve",
            "Segregate incompatible chemicals: acids vs bases, oxidizers vs flammables (3-ft minimum)",
            "Inventory tracking: Usage rate, reorder point = (Usage × Lead time) + Safety stock",
            "Shelf life management: FIFO rotation, date totes on receipt, dispose of expired chemicals",
            "PPE requirements per SDS Section 8: Chemical gloves, safety glasses, face shield for corrosives",
            "Transfer equipment: Chemical-compatible pumps (AOD), hoses (Viton, EPDM), bonding/grounding for flammables",
            "Regulatory: SPCC plan if >1,320 gal oil storage, Tier II if >10,000 lb hazardous chemicals"
        ],
        primary_authority=[
            "EPA 40 CFR 112 'Oil Pollution Prevention' (SPCC requirements)",
            "NFPA 30 'Flammable and Combustible Liquids Code'",
            "OSHA 29 CFR 1910.106 'Flammable Liquids Storage'"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.INVENTORY_MANAGEMENT,
        authority_level=AuthorityLevel.REGULATORY
    ),

    DoctrineBlock(
        topic="Safety Data Sheet (SDS) and GHS Compliance",
        keywords=["sds", "safety data sheet", "ghs", "hazcom", "chemical labeling", "hazard communication"],
        conclusion_template=[
            "SDS (Safety Data Sheet) provides 16 sections of chemical hazard information, required for all hazardous chemicals under OSHA HazCom 29 CFR 1910.1200.",
            "GHS (Globally Harmonized System) standardizes hazard classification and labeling with pictograms, signal words, and hazard statements.",
            "Employers must maintain current SDS library, train employees on hazard interpretation, and ensure GHS-compliant labels on all containers."
        ],
        reasoning_framework="""
OSHA HAZARD COMMUNICATION STANDARD (HazCom 2012):
- Regulation: 29 CFR 1910.1200
- Purpose: Ensure chemical hazards communicated to workers
- Three key elements:
  1. Chemical inventory and hazard determination
  2. Labels and warning signs (GHS-compliant)
  3. Safety Data Sheets (SDS) accessible to employees
- Training: Required at hire and when new hazard introduced

SDS 16-SECTION FORMAT (GHS Revision):

Section 1: Identification
- Product name, synonyms, recommended use
- Supplier details: Name, address, phone, emergency contact (24-hr)
- Emergency phone: CHEMTREC 1-800-424-9300 (common for oilfield chemicals)

Section 2: Hazard Identification
- GHS classification: Specific hazard classes and categories
  Example: "Acute Toxicity, Oral, Category 4" or "Skin Corrosion, Category 1A"
- Signal word: "Danger" (severe) or "Warning" (less severe)
- Hazard statements: Standardized phrases (H-codes)
  Example: "H314 - Causes severe skin burns and eye damage"
- Precautionary statements: Prevention, response, storage, disposal (P-codes)
  Example: "P280 - Wear protective gloves/eye protection"
- Pictograms: GHS symbols (flame, corrosion, exclamation mark, etc.)

Section 3: Composition/Information on Ingredients
- Chemical name and CAS number for hazardous components >1% (>0.1% if carcinogen)
- Trade secret ingredients: May be withheld (manufacturer claims confidentiality)
- Impurities/additives contributing to hazard classification

Section 4: First Aid Measures
- By exposure route: Inhalation, ingestion, skin contact, eye contact
- Most important symptoms/effects (acute and delayed)
- Immediate medical attention required: Yes/No and special treatment needed
- Example (Glutaraldehyde): "If swallowed, rinse mouth. Do NOT induce vomiting. Get medical attention."

Section 5: Fire-Fighting Measures
- Suitable extinguishing media: Water, foam, CO2, dry chemical
- Unsuitable media: (e.g., water stream on flammable liquids)
- Specific hazards: Combustion products (CO, SO2, HCl, etc.)
- Special protective equipment: SCBA, chemical-resistant firefighter turnout gear

Section 6: Accidental Release Measures
- Personal precautions: Evacuate area, ventilate, PPE required
- Environmental precautions: Prevent entry to waterways, notify authorities if release >RQ
- Containment: Dike, absorb with inert material (sand, vermiculite)
- Cleanup: Sweep/vacuum, neutralize if applicable, dispose per Section 13

Section 7: Handling and Storage
- Handling: Avoid contact with incompatibles, use PPE, ensure ventilation
- Storage: Temperature limits, keep containers closed, segregation requirements
- Incompatibilities: Specific chemicals to separate (acids/bases, oxidizers/organics)
- Example: "Store away from oxidizing agents. Keep container tightly closed."

Section 8: Exposure Controls/Personal Protection
- Exposure limits:
  - OSHA PEL (Permissible Exposure Limit): Legal limit, 8-hr TWA
  - ACGIH TLV (Threshold Limit Value): Recommended limit, industry standard
  - Example (H2S): OSHA PEL = 10 ppm TWA, ACGIH TLV = 1 ppm TWA (more protective)
- Engineering controls: Ventilation (general exhaust, local exhaust), enclosed systems
- PPE:
  - Respiratory: Not required (adequate ventilation) vs N95, half-face, full-face SCBA
  - Eye: Safety glasses, goggles, face shield
  - Skin: Nitrile gloves, neoprene gloves, chemical apron
  - Feet: Steel-toe boots, chemical-resistant boots
- Glove compatibility: Check manufacturer data (nitrile vs neoprene vs Viton)

Section 9: Physical and Chemical Properties
- Appearance: Liquid/solid, color, odor
- pH: Important for corrosivity classification
- Flash point: Temperature at which vapors ignite (flammability classification)
  - <73F = Category 1 (extremely flammable), 73-100F = Category 2, etc.
- Specific gravity: >1 = sinks in water, <1 = floats
- Vapor pressure: Higher = more volatile (evaporates faster)
- Solubility: Water-soluble vs oil-soluble
- Example (Xylene): Flash point 81F, Specific gravity 0.87, Water solubility 0.015%

Section 10: Stability and Reactivity
- Chemical stability: Stable or unstable under normal conditions
- Incompatible materials: Chemicals that react dangerously
  - Example (Hypochlorite): "Incompatible with acids, ammonia, reducing agents"
- Hazardous decomposition products: CO, NOx, HCl, etc. (fire/thermal decomposition)
- Conditions to avoid: Heat, sparks, static, shock, incompatibles

Section 11: Toxicological Information
- Acute toxicity: LD50 (oral/dermal lethal dose), LC50 (inhalation lethal concentration)
  - Category 1 (high toxicity): LD50 <50 mg/kg, LC50 <100 ppm
  - Category 4 (low toxicity): LD50 300-2000 mg/kg
- Routes of exposure: Inhalation, ingestion, skin absorption, eye contact
- Chronic effects: Carcinogenicity, reproductive toxicity, organ damage
- Example (Glutaraldehyde): "May cause allergic skin reaction. Suspected of causing cancer."

Section 12: Ecological Information
- Aquatic toxicity: LC50 for fish, daphnia (96-hr, 48-hr)
- Persistence: Biodegradability, half-life in environment
- Bioaccumulation: BCF (bioconcentration factor) in organisms
- Not required in US (OSHA does not mandate), but included for global compliance

Section 13: Disposal Considerations
- Waste codes: RCRA hazardous waste codes (D001 ignitable, D002 corrosive, etc.)
- Disposal methods: Incineration, landfill (non-hazardous), recycling
- Regulatory: 40 CFR 261 (hazardous waste identification)
- Example: "Dispose of in accordance with federal, state, local regulations. May be RCRA hazardous waste."

Section 14: Transport Information
- UN number: UN1760, UN1993, etc. (hazardous materials identification)
- Proper shipping name: "Corrosive liquid, n.o.s." or specific chemical name
- Hazard class: 3 (flammable), 8 (corrosive), 6.1 (toxic), etc.
- Packing group: I (high danger), II (medium), III (low)
- DOT placard: Diamond-shaped sign on vehicle/container
- Marine pollutant: Yes/No (additional marking required for ocean transport)

Section 15: Regulatory Information
- TSCA status: Listed on Toxic Substances Control Act inventory (can be manufactured/imported)
- SARA 313 (EPCRA): Reportable if >10,000 lb on-site (Tier II reporting)
- CERCLA/SARA RQ: Reportable quantity for spills (notify National Response Center)
  - Example (Sulfuric acid): RQ = 1000 lb
- California Prop 65: Warning required if chemical causes cancer/reproductive harm
- State-specific: Right-to-Know laws (NJ, PA, MA, etc.)

Section 16: Other Information
- Revision date, version number, changes from previous version
- Disclaimer: SDS accuracy, limitations, intended use
- Legend: Abbreviations used (TWA, STEL, PEL, TLV, ACGIH, NIOSH, etc.)

GHS LABELING REQUIREMENTS:

Required Elements on Container Label:
1. Product identifier: Chemical name matching SDS
2. Signal word: DANGER or WARNING
3. Hazard statements: H-codes text ("Causes severe skin burns")
4. Precautionary statements: P-codes text ("Wear protective gloves")
5. Pictograms: GHS symbols (see below)
6. Supplier information: Name, address, phone

GHS Pictograms (9 symbols):
- Flame: Flammable liquids/gases/solids, self-reactive
- Flame over circle: Oxidizers
- Gas cylinder: Compressed gases
- Corrosion: Skin/eye corrosion, metal corrosion
- Exploding bomb: Explosives, self-reactive, organic peroxides
- Skull and crossbones: Acute toxicity (fatal/toxic)
- Exclamation mark: Irritant, sensitizer, acute toxicity (harmful)
- Health hazard: Carcinogen, respiratory sensitizer, reproductive toxicity, organ damage
- Environment: Aquatic toxicity (not required in US)

EMPLOYER RESPONSIBILITIES:

SDS Accessibility:
- Maintain SDS for every hazardous chemical on-site
- Accessible to employees during work shift (paper binder, electronic database)
- Update within 3 months of receiving new information from manufacturer
- SDS age: No expiration, but update when chemical reformulated or new hazard data

Chemical Inventory:
- List all hazardous chemicals used/stored at facility
- Cross-reference with SDS library (ensure SDS available for each chemical)
- Update inventory when new chemicals introduced or old chemicals discontinued

Employee Training:
- Initial training: At hire, before working with hazardous chemicals
- Additional training: When new chemical/hazard introduced
- Training content:
  - How to read SDS (16 sections, where to find specific information)
  - GHS label elements (pictograms, signal words, hazard statements)
  - Physical/health hazards of chemicals in work area
  - Protective measures: PPE, engineering controls, safe handling
  - Location of SDS and chemical inventory
- Documentation: Roster, date, topics covered, trainer signature

Secondary Container Labeling:
- If chemical transferred from original container to secondary (bucket, spray bottle)
- Label must include: Product identifier, hazard warnings
- Full GHS label not required for secondary containers (simplified acceptable)

Hazard Determination:
- Manufacturer/distributor classifies chemicals, prepares SDS and labels
- Employer: Use SDS info, may not need to classify (unless mixing chemicals)

COMMON ERRORS:
- Outdated SDS (5-10 years old, does not reflect current GHS format)
- SDS not accessible (locked in supervisor office, employees can't access on-shift)
- No secondary container labels (transferred chemicals not identified)
- No training documentation (OSHA inspection finds no proof of training)
- Missing SDS for "non-hazardous" products (some cleaning products are hazardous)
- No chemical inventory (unclear which chemicals on-site, missing SDS)
""",
        key_factors=[
            "SDS 16 sections: Identification, Hazards, Composition, First Aid, Fire, Spills, Handling, Exposure/PPE, Properties, Stability, Toxicology, Ecology, Disposal, Transport, Regulatory, Other",
            "GHS label elements: Product name, Signal word (Danger/Warning), Pictograms, Hazard statements, Precautionary statements, Supplier info",
            "Employer must maintain SDS library accessible to employees during shift, update within 3 months",
            "Employee training required at hire and when new chemical introduced: SDS interpretation, GHS labels, hazards, PPE",
            "Key SDS sections for oilfield: Section 8 (Exposure limits, PPE), Section 7 (Storage, incompatibilities), Section 6 (Spill response)",
            "Exposure limits: OSHA PEL (legal), ACGIH TLV (recommended, often more protective)",
            "Secondary containers require labels with product name and hazard warnings"
        ],
        primary_authority=[
            "OSHA 29 CFR 1910.1200 'Hazard Communication Standard (HazCom)'",
            "GHS Revision 7 (United Nations Globally Harmonized System of Classification and Labelling of Chemicals)",
            "OSHA Brief 'Hazard Communication Standard: Safety Data Sheets'"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SAFETY_COMPLIANCE,
        authority_level=AuthorityLevel.REGULATORY
    ),

]


# ============================================================================
# ENGINE STATE
# ============================================================================

class EngineState:
    """Global engine state tracking"""

    def __init__(self):
        self.start_time = time.time()
        self.total_queries = 0
        self.total_response_time = 0.0
        self.doctrine_coverage = {doc.topic: 0 for doc in DOCTRINE_CACHE}

    def record_query(self, response_time: float, triggered_doctrines: List[str]):
        self.total_queries += 1
        self.total_response_time += response_time
        for doctrine in triggered_doctrines:
            if doctrine in self.doctrine_coverage:
                self.doctrine_coverage[doctrine] += 1

    def get_uptime(self) -> float:
        return time.time() - self.start_time

    def get_avg_response_time(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return self.total_response_time / self.total_queries


ENGINE_STATE = EngineState()


# ============================================================================
# CORE INTELLIGENCE FUNCTIONS
# ============================================================================

def normalize_query(query: str) -> str:
    """Normalize query text for matching"""
    return query.lower().strip()


def match_doctrines(query: str) -> List[DoctrineBlock]:
    """Match query against doctrine cache keywords"""
    normalized = normalize_query(query)
    tokens = set(normalized.split())

    matches = []
    for doctrine in DOCTRINE_CACHE:
        # Calculate keyword overlap
        keyword_matches = sum(1 for kw in doctrine.keywords if kw in normalized)
        if keyword_matches > 0:
            matches.append((doctrine, keyword_matches))

    # Sort by keyword match count descending
    matches.sort(key=lambda x: x[1], reverse=True)

    # Return top matching doctrines
    return [doc for doc, _ in matches[:5]]


def build_response(
    query: str,
    triggered_doctrines: List[DoctrineBlock],
    mode: ResponseMode,
    zone: AnalysisZone
) -> Tuple[str, ConfidenceLevel]:
    """Build response from triggered doctrines based on mode"""

    if not triggered_doctrines:
        return (
            "No specific chemical injection system doctrine matched this query. "
            "Please provide more details about the chemical type (corrosion inhibitor, scale inhibitor, paraffin, etc.), "
            "application conditions, or specific technical question.",
            ConfidenceLevel.DISCLOSURE
        )

    primary_doctrine = triggered_doctrines[0]

    # Update doctrine hit tracking
    primary_doctrine.hit_count += 1
    primary_doctrine.last_triggered = datetime.utcnow().isoformat()

    if mode == ResponseMode.FAST:
        # Concise answer from conclusion template
        answer = " ".join(primary_doctrine.conclusion_template)
        confidence = primary_doctrine.confidence

    elif mode == ResponseMode.DEFENSE:
        # Full reasoning with authorities
        answer_parts = [
            "ANALYSIS:",
            primary_doctrine.reasoning_framework,
            "",
            "KEY FACTORS:",
            *[f"- {factor}" for factor in primary_doctrine.key_factors],
            "",
            "PRIMARY AUTHORITY:",
            *[f"- {auth}" for auth in primary_doctrine.primary_authority],
            "",
            "CONCLUSION:",
            " ".join(primary_doctrine.conclusion_template)
        ]
        answer = "\n".join(answer_parts)
        confidence = primary_doctrine.confidence

    else:  # MEMO mode
        # Comprehensive memo format
        answer_parts = [
            f"CHEMICAL INJECTION SYSTEMS TECHNICAL MEMORANDUM",
            f"Topic: {primary_doctrine.topic}",
            f"Category: {primary_doctrine.category.value}",
            f"Authority Level: {primary_doctrine.authority_level.value}",
            "",
            "EXECUTIVE SUMMARY:",
            " ".join(primary_doctrine.conclusion_template),
            "",
            "DETAILED ANALYSIS:",
            primary_doctrine.reasoning_framework,
            "",
            "CRITICAL FACTORS:",
            *[f"{i+1}. {factor}" for i, factor in enumerate(primary_doctrine.key_factors)],
            "",
            "SUPPORTING AUTHORITY:",
            *[f"[{i+1}] {auth}" for i, auth in enumerate(primary_doctrine.primary_authority)],
            "",
            "CONFIDENCE ASSESSMENT:",
            f"This analysis is classified as {primary_doctrine.confidence.value} based on "
            f"{primary_doctrine.authority_level.value} level authority sources.",
            "",
        ]

        # Add related doctrines if multiple triggered
        if len(triggered_doctrines) > 1:
            answer_parts.extend([
                "RELATED CONSIDERATIONS:",
                *[f"- {doc.topic}: {doc.conclusion_template[0]}"
                  for doc in triggered_doctrines[1:3]]
            ])

        answer = "\n".join(answer_parts)
        confidence = primary_doctrine.confidence

    return answer, confidence


def generate_determinism_hash(query: str, answer: str) -> str:
    """Generate SHA-256 hash for response determinism verification"""
    content = f"{query}|{answer}".encode('utf-8')
    return hashlib.sha256(content).hexdigest()


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="OFE14 Chemical Injection Systems Intelligence Engine",
    version="1.0.0",
    description="TIE-grade engine for oilfield chemical injection system analysis"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure loguru
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "logs" / "ofe14_{time:YYYY-MM-DD}.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)


@app.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest) -> QueryResponse:
    """
    Main query endpoint - Three-layer response architecture
    """
    start_time = time.time()
    query_id = str(uuid.uuid4())

    logger.info(f"Query {query_id}: {request.question[:100]}... | Mode: {request.mode} | Zone: {request.zone}")

    try:
        # Layer 1: Doctrine cache (fast path)
        triggered_doctrines = match_doctrines(request.question)

        # Layer 2: Build response from doctrines
        answer, confidence = build_response(
            request.question,
            triggered_doctrines,
            request.mode,
            request.zone
        )

        # Layer 3: Deep analysis would integrate vector search + external data
        # (Simplified for this implementation - full TIE has vector DB integration)

        response_time_ms = (time.time() - start_time) * 1000

        # Generate determinism hash
        det_hash = generate_determinism_hash(request.question, answer)

        # Track metrics
        doctrine_topics = [d.topic for d in triggered_doctrines]
        ENGINE_STATE.record_query(response_time_ms, doctrine_topics)

        # Build metadata
        metadata = {
            "query_id": query_id,
            "mode": request.mode.value,
            "zone": request.zone.value,
            "doctrines_evaluated": len(DOCTRINE_CACHE),
            "doctrines_triggered": len(triggered_doctrines),
            "primary_doctrine": triggered_doctrines[0].topic if triggered_doctrines else None,
            "category": triggered_doctrines[0].category.value if triggered_doctrines else None,
        }

        logger.info(
            f"Query {query_id} completed in {response_time_ms:.2f}ms | "
            f"Triggered: {len(triggered_doctrines)} doctrines | "
            f"Confidence: {confidence.value}"
        )

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            triggered_doctrines=doctrine_topics,
            response_time_ms=response_time_ms,
            determinism_hash=det_hash,
            metadata=metadata
        )

    except Exception as e:
        logger.error(f"Query {query_id} failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint with engine metrics
    """
    return HealthResponse(
        status="operational",
        engine="OFE14_chemical_injection",
        version="1.0.0",
        port=9284,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=ENGINE_STATE.get_uptime(),
        total_queries=ENGINE_STATE.total_queries,
        avg_response_ms=ENGINE_STATE.get_avg_response_time()
    )


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total_doctrines": len(DOCTRINE_CACHE),
        "categories": list(set(d.category.value for d in DOCTRINE_CACHE)),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords,
                "authority_level": d.authority_level.value,
                "hit_count": d.hit_count
            }
            for d in DOCTRINE_CACHE
        ]
    }


@app.get("/metrics")
async def get_metrics():
    """Detailed engine performance metrics"""
    return {
        "uptime_seconds": ENGINE_STATE.get_uptime(),
        "total_queries": ENGINE_STATE.total_queries,
        "avg_response_time_ms": ENGINE_STATE.get_avg_response_time(),
        "doctrine_coverage": ENGINE_STATE.doctrine_coverage,
        "most_triggered_doctrines": sorted(
            ENGINE_STATE.doctrine_coverage.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
    }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("OFE14 Chemical Injection Systems Intelligence Engine v1.0.0")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} chemical injection expertise doctrine blocks")
    logger.info(f"Categories: {len(set(d.category for d in DOCTRINE_CACHE))}")
    logger.info("TIE-20 Architecture: ACTIVE")
    logger.info("Port: 9284")
    logger.info("=" * 80)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9284,
        log_level="info"
    )
