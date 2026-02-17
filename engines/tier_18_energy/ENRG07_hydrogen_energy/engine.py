"""
ENRG07 Hydrogen Energy Systems Intelligence Engine
TIE-Grade Implementation

Analyzes hydrogen energy systems: production (green/blue/gray), storage technologies,
fuel cells, infrastructure, and safety per NFPA 2, ASME B31.12, DOE standards.

Port: 9242
Version: 1.0.0
Author: ECHO OMEGA PRIME
"""

import sys
from pathlib import Path

# CRITICAL: Add parent directory to path BEFORE any local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import re
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict, Counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

ENGINE_NAME = "ENRG07_hydrogen_energy"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 9242
AUDIT_LOG_PATH = Path(__file__).parent / "audit_trail.jsonl"

# Configure loguru
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "engine.log",
    rotation="10 MB",
    retention="30 days",
    level="DEBUG"
)

# ═══════════════════════════════════════════════════════════════════════════
# ENUMS & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    """Response modes matching TIE standard."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    """Confidence stratification."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class AnalysisZone(str, Enum):
    """Position zones for fact separation."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class IssueCategory(str, Enum):
    """Hydrogen energy issue categories."""
    PRODUCTION = "PRODUCTION"
    STORAGE = "STORAGE"
    FUEL_CELLS = "FUEL_CELLS"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    SAFETY = "SAFETY"
    ECONOMICS = "ECONOMICS"
    POLICY = "POLICY"
    MATERIALS = "MATERIALS"
    APPLICATIONS = "APPLICATIONS"
    ENVIRONMENTAL = "ENVIRONMENTAL"

# Hydrogen color classification
HYDROGEN_COLORS = {
    "GREEN": "Electrolysis using renewable electricity (solar, wind, hydro)",
    "BLUE": "Steam methane reforming with carbon capture and storage (CCS)",
    "GRAY": "Steam methane reforming without CCS (conventional)",
    "TURQUOISE": "Methane pyrolysis producing solid carbon",
    "PINK": "Electrolysis using nuclear power",
    "YELLOW": "Electrolysis using grid electricity (mixed sources)",
    "BLACK": "Coal gasification without CCS",
    "BROWN": "Lignite gasification without CCS",
    "WHITE": "Naturally occurring geological hydrogen"
}

# Storage pressure standards
STORAGE_PRESSURES = {
    "TYPE_I_350": "350 bar steel tanks for fleet vehicles",
    "TYPE_III_350": "350 bar composite overwrapped aluminum",
    "TYPE_IV_350": "350 bar composite overwrapped polymer liner",
    "TYPE_IV_700": "700 bar composite for light-duty vehicles",
    "LH2": "Liquid hydrogen at -253 degrees C (20 K)",
    "METAL_HYDRIDE": "Solid-state storage in metal alloys",
    "LOHC": "Liquid organic hydrogen carriers (toluene/methylcyclohexane)"
}

# Fuel cell types
FUEL_CELL_TYPES = {
    "PEM": "Proton Exchange Membrane - automotive, portable",
    "SOFC": "Solid Oxide Fuel Cell - stationary power, high efficiency",
    "AFC": "Alkaline Fuel Cell - space applications",
    "PAFC": "Phosphoric Acid Fuel Cell - stationary CHP",
    "MCFC": "Molten Carbonate Fuel Cell - large stationary",
    "DMFC": "Direct Methanol Fuel Cell - portable electronics"
}

# Safety codes and standards
SAFETY_STANDARDS = [
    "NFPA 2: Hydrogen Technologies Code",
    "ASME B31.12: Hydrogen Piping and Pipelines",
    "ISO 19880-1: Gaseous hydrogen fueling stations",
    "SAE J2579: Fuel systems in fuel cell vehicles",
    "IEC 62282: Fuel cell technologies",
    "AIAA G-095: Guide to safety of hydrogen systems",
    "CGA G-5.3: Commodity specification for hydrogen"
]

BANNED_PHRASES = [
    "this is not legal advice",
    "consult an attorney",
    "I am not a lawyer",
    "seek professional advice",
    "cannot provide legal advice"
]

# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    """Hydrogen energy query request."""
    question: str = Field(..., min_length=10, max_length=2000)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.REPORTING
    context: Optional[Dict[str, Any]] = None

class DoctrineBlock(BaseModel):
    """Single doctrine reasoning block."""
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: Optional[str] = None
    adversary_position: Optional[str] = None
    counter_arguments: List[str] = Field(default_factory=list)
    resolution_strategy: Optional[str] = None
    entity_scope: Optional[str] = None
    confidence: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE
    confidence_stratification: str = ""
    controlling_precedent: List[str] = Field(default_factory=list)

class AnalysisResponse(BaseModel):
    """TIE-grade response model."""
    answer: str
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    reasoning_chain: List[str]
    authorities_cited: List[str]
    fragility_score: float = Field(ge=0.0, le=1.0)
    zone: AnalysisZone
    mode: ResponseMode
    determinism_hash: str
    latency_ms: float
    epistemic_caveats: List[str] = Field(default_factory=list)

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    queries_processed: int
    avg_latency_ms: float
    cache_hit_rate: float
    uptime_seconds: float

# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - REAL HYDROGEN ENERGY EXPERTISE
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [

    # ═══════════════════════════════════════════════════════════════════════
    # PRODUCTION METHODS
    # ═══════════════════════════════════════════════════════════════════════

    DoctrineBlock(
        topic="Green Hydrogen Production via PEM Electrolysis",
        keywords=["PEM", "electrolysis", "renewable", "green hydrogen", "proton exchange", "efficiency", "renewable energy"],
        conclusion_template="PEM electrolysis produces green hydrogen at {efficiency}% efficiency when powered by renewable electricity. Stack lifetime {lifetime} hours. Capital cost ${capex}/kW.",
        reasoning_framework="""
        PEM (Proton Exchange Membrane) electrolysis for green hydrogen production:

        1. TECHNOLOGY FUNDAMENTALS:
           - Polymer electrolyte membrane separates anode and cathode
           - Anode reaction: 2H2O -> O2 + 4H+ + 4e-
           - Cathode reaction: 4H+ + 4e- -> 2H2
           - Operating temperature: 50-80 degrees C
           - Operating pressure: 30-80 bar (some systems to 200 bar)
           - Current density: 1-3 A/cm2 (advanced systems to 5 A/cm2)

        2. EFFICIENCY CHARACTERISTICS:
           - Stack efficiency: 60-70% HHV (Higher Heating Value)
           - System efficiency: 50-65% HHV including BoP losses
           - Energy consumption: 50-60 kWh/kg H2 (4.5-5.5 kWh/Nm3)
           - Load range: 10-110% (excellent dynamic response)
           - Cold start time: < 5 minutes (vs hours for alkaline)

        3. STACK COMPONENTS:
           - Membrane: Nafion or similar perfluorosulfonic acid
           - Anode catalyst: Iridium oxide (IrO2) or mixed metal oxides
           - Cathode catalyst: Platinum (Pt) or Pt alloys
           - Bipolar plates: Titanium (expensive) or coated stainless steel
           - Catalyst loading: 2-4 mg/cm2 total PGM (platinum group metals)

        4. LIFETIME AND DEGRADATION:
           - Stack lifetime: 60,000-90,000 hours (commercial systems)
           - Degradation rate: 1-3 microV/h voltage decay
           - Failure modes: membrane thinning, catalyst dissolution, titanium corrosion
           - Maintenance: deionized water quality critical (< 0.1 microS/cm)

        5. COST STRUCTURE (2024):
           - Capital cost: $800-1,400/kW installed
           - Stack replacement: 30-40% of capex every 60,000 hours
           - PGM cost sensitivity: ~$150/kW for Ir and Pt at current prices
           - Learning curve: 18% cost reduction per doubling of capacity

        6. ADVANTAGES:
           - High current density (compact footprint)
           - Excellent dynamic response (ideal for variable renewables)
           - High pressure output (reduces compression costs)
           - High purity hydrogen (99.9%+)
           - No liquid electrolyte (simplified system)

        7. CHALLENGES:
           - PGM catalyst cost and supply constraints
           - Membrane durability under cycling conditions
           - Titanium bipolar plate cost
           - Limited operational track record at GW scale

        8. RENEWABLE INTEGRATION:
           - Rapid response to wind/solar variability (ms-second timescale)
           - Overload capability to 110% captures excess generation
           - Minimum load 10% allows night/low-wind operation
           - Grid services: frequency response, voltage support via inverter

        9. SCALE CONSIDERATIONS:
           - Largest single units: 20 MW (Nel, ITM, Siemens)
           - GW-scale projects: modular stacks in parallel
           - Balance of plant: water treatment, power electronics, gas processing
           - Footprint: ~10-15 m2/MW stack area

        10. TECHNO-ECONOMIC OPTIMIZATION:
            - LCOH (levelized cost of hydrogen): $3-6/kg green H2 (2024)
            - Dominated by electricity cost (60-80% of LCOH)
            - Capacity factor critical: 40% CF doubles LCOH vs 80% CF
            - Co-location with renewables vs grid connection tradeoff
        """,
        key_factors=[
            "Stack efficiency 60-70% HHV, system 50-65% HHV",
            "Energy consumption 50-60 kWh/kg H2",
            "PGM catalyst loading 2-4 mg/cm2 (Ir, Pt)",
            "Stack lifetime 60,000-90,000 hours",
            "Capital cost $800-1,400/kW installed",
            "Excellent dynamic response (10-110% load range)",
            "High pressure output (30-200 bar)",
            "LCOH $3-6/kg dominated by electricity cost"
        ],
        primary_authority=[
            "DOE Hydrogen and Fuel Cell Technologies Office Technical Targets",
            "IEA Global Hydrogen Review 2023",
            "IRENA Green Hydrogen Cost Reduction Report 2020",
            "Nel Hydrogen, ITM Power, Siemens Energy technical specifications"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on efficiency and cost ranges from commercial deployments. Medium confidence on long-term degradation at GW scale.",
        controlling_precedent=[
            "DOE target: $2/kg H2 by 2026 (requires <$500/kW capex + cheap renewables)"
        ]
    ),

    DoctrineBlock(
        topic="Blue Hydrogen via Steam Methane Reforming with CCS",
        keywords=["SMR", "blue hydrogen", "carbon capture", "natural gas", "CCS", "steam reforming", "methane"],
        conclusion_template="Blue hydrogen from SMR+CCS captures {capture_rate}% of CO2 emissions. Carbon intensity {ci} kg CO2/kg H2. Capture cost ${cost}/tonne CO2.",
        reasoning_framework="""
        Steam Methane Reforming (SMR) with Carbon Capture and Storage (CCS) for blue hydrogen:

        1. SMR PROCESS FUNDAMENTALS:
           - Primary reforming: CH4 + H2O -> CO + 3H2 (endothermic, 800-900 degrees C)
           - Secondary reforming: residual CH4 + air -> CO + H2 + N2
           - Water-gas shift: CO + H2O -> CO2 + H2 (exothermic, 200-400 degrees C)
           - Pressure swing adsorption (PSA) purifies H2 to 99.99%
           - Gray hydrogen efficiency: 70-80% HHV

        2. CARBON CAPTURE INTEGRATION:
           - CO2 sources: flue gas (low pressure, dilute) + PSA off-gas (high pressure, concentrated)
           - Pre-combustion capture: shift reactor -> CO2 separation before combustion
           - Post-combustion capture: amine scrubbing (MEA, MDEA) of flue gas
           - Oxy-fuel combustion: burn in pure O2 -> high purity CO2 stream
           - Typical capture rate: 90-95% from high-pressure streams

        3. CAPTURE RATE REALITY:
           - High-pressure CO2 (PSA off-gas): 95%+ capture economically feasible
           - Low-pressure flue gas: 60-85% capture (energy penalty significant)
           - Overall plant capture: 85-95% depending on configuration
           - Fugitive emissions: methane leakage in supply chain (1-3% of gas input)
           - Lifecycle emissions: 1-2 kg CO2/kg H2 vs 9-12 kg for gray H2

        4. CARBON STORAGE:
           - Saline aquifers: largest capacity, CO2 dissolves and mineralizes
           - Depleted oil/gas fields: structural trapping, monitoring infrastructure exists
           - Enhanced oil recovery (EOR): revenue from oil offsets costs
           - Storage capacity: Gt-scale in suitable geology
           - Permanence: 98%+ retention over 1000 years in suitable formations

        5. COST STRUCTURE:
           - Gray hydrogen production: $1.0-1.5/kg H2 (natural gas at $3-5/MMBtu)
           - CCS capital cost: $100-300/tonne CO2/year capture capacity
           - CCS operating cost: $30-70/tonne CO2 captured
           - Blue hydrogen premium: $0.50-1.50/kg over gray (depends on carbon price)
           - Total LCOH: $1.5-3.0/kg H2 (2024 costs)

        6. ENERGY PENALTY:
           - Amine scrubbing: 15-30% energy penalty on plant
           - Compression to pipeline pressure (100-150 bar): 0.1-0.2 MWh/tonne CO2
           - Overall efficiency: 60-70% HHV (vs 70-80% without CCS)
           - Parasitic load reduces hydrogen output 10-15%

        7. TECHNOLOGY MATURITY:
           - SMR: fully mature, 50+ years operational experience
           - Large-scale CCS: demonstrated at Quest (Canada), Sleipner (Norway)
           - Blue hydrogen plants: Air Products Port Arthur (Texas), NEOM (Saudi Arabia)
           - Largest blue H2 project: 3 GW planned capacity (multiple plants)

        8. POLICY AND CERTIFICATION:
           - EU taxonomy: blue hydrogen requires <3 kg CO2/kg H2 lifecycle
           - UK Low Carbon Hydrogen Standard: <2.4 kg CO2/kg H2
           - 45Q tax credit (US): $85/tonne CO2 for geological storage
           - CfD (Contract for Difference) schemes in UK for blue H2

        9. ADVANTAGES OVER GREEN:
           - Baseload production (not weather-dependent)
           - Lower capital cost ($1-2/kg vs $3-6/kg green)
           - Existing gas infrastructure leverages sunk costs
           - Near-term scalability (GW-scale plants feasible today)

        10. CHALLENGES:
            - Methane leakage in supply chain undermines carbon benefits
            - CCS permanence requires monitoring and long-term liability
            - Carbon price uncertainty affects economic viability
            - Public perception: "blue is greenwashing" vs "bridge technology"
            - Stranded asset risk: falling green H2 costs could obsolete blue
        """,
        key_factors=[
            "Overall CO2 capture rate 85-95% depending on configuration",
            "Lifecycle emissions 1-2 kg CO2/kg H2 (vs 9-12 gray, 0.1-0.5 green)",
            "CCS energy penalty reduces efficiency to 60-70% HHV",
            "LCOH $1.5-3.0/kg H2 (2024 costs)",
            "Methane leakage 1-3% of supply chain critical to lifecycle carbon",
            "Policy threshold: <2.4-3.0 kg CO2/kg H2 for low-carbon certification",
            "45Q tax credit $85/tonne CO2 (US)",
            "Baseload production advantage over intermittent renewables"
        ],
        primary_authority=[
            "IEA Blue Hydrogen Report 2021",
            "IPCC Special Report on CCS",
            "Air Products Port Arthur Blue Hydrogen Facility data",
            "UK Low Carbon Hydrogen Standard 2022"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on capture technology. Medium confidence on lifecycle emissions (methane leakage data uncertain).",
        controlling_precedent=[
            "EU Taxonomy: <3 kg CO2/kg H2 lifecycle emissions for low-carbon hydrogen"
        ]
    ),

    DoctrineBlock(
        topic="Alkaline Electrolysis Technology",
        keywords=["alkaline", "electrolysis", "KOH", "NaOH", "electrolyte", "mature technology", "low cost"],
        conclusion_template="Alkaline electrolysis achieves {efficiency}% efficiency at {current_density} A/cm2. Stack lifetime {lifetime} hours. Lower capital cost than PEM but slower response.",
        reasoning_framework="""
        Alkaline electrolysis for hydrogen production:

        1. TECHNOLOGY FUNDAMENTALS:
           - Liquid electrolyte: 25-30% KOH or NaOH solution
           - Anode reaction: 4OH- -> O2 + 2H2O + 4e-
           - Cathode reaction: 4H2O + 4e- -> 2H2 + 4OH-
           - Operating temperature: 60-80 degrees C (atmospheric) or 120-180 degrees C (pressurized)
           - Operating pressure: 1-30 bar (most commercial systems)
           - Current density: 0.2-0.4 A/cm2 (vs 1-3 for PEM)

        2. EFFICIENCY:
           - Stack efficiency: 60-70% HHV
           - System efficiency: 50-60% HHV
           - Energy consumption: 50-60 kWh/kg H2
           - Similar to PEM on energy basis despite lower current density

        3. STACK COMPONENTS:
           - Electrodes: Nickel-based (cheap, abundant)
           - Catalyst: Raney nickel, nickel-molybdenum alloys (no PGMs)
           - Separator: Asbestos (legacy), Zirfon (modern), ceramic
           - Bipolar plates: Nickel-plated steel
           - Zero PGM content (major cost advantage)

        4. LIFETIME:
           - Stack lifetime: 60,000-100,000 hours (mature systems)
           - Degradation: 1-2 microV/h (similar to PEM)
           - Electrolyte replacement: every 5-10 years
           - Corrosion: KOH attacks seals, gaskets over time

        5. COST:
           - Capital cost: $500-900/kW (30-50% less than PEM)
           - No PGM cost exposure
           - Higher BoP costs (electrolyte circulation, gas purification)
           - LCOH advantage at low capacity factors

        6. ADVANTAGES:
           - Mature technology (100+ years of development)
           - No precious metals (abundant materials)
           - Proven long-term durability
           - Lower capital cost
           - Simpler manufacturing

        7. DISADVANTAGES:
           - Low current density (large footprint)
           - Slow dynamic response (minutes to adjust, vs seconds for PEM)
           - Low partial load: 20-40% minimum (vs 10% PEM)
           - Liquid electrolyte handling complexity
           - Gas purity: 99.5% (vs 99.9%+ PEM) requires additional purification

        8. RENEWABLE INTEGRATION:
           - Poor match for variable renewables (slow response)
           - Suitable for baseload operation (e.g., dedicated wind farm)
           - Cannot provide grid services like PEM
           - Thermal inertia: hours to reach operating temperature from cold

        9. SCALE:
           - Largest units: 6 MW (Thyssenkrupp, John Cockerill)
           - GW-scale projects: many smaller units in parallel
           - Installed base: >1 GW cumulative (mostly industrial chlor-alkali heritage)

        10. COMPETITIVE POSITION:
            - Cost leader for baseload operation
            - Losing market share to PEM in renewable applications
            - Niche: industrial sites with steady power, space available
            - Technology path: advanced alkaline (AEM) bridges gap to PEM performance
        """,
        key_factors=[
            "Efficiency 50-60% HHV (system), competitive with PEM",
            "Current density 0.2-0.4 A/cm2 (10x lower than PEM)",
            "Zero PGM catalysts (nickel-based)",
            "Capital cost $500-900/kW (30-50% less than PEM)",
            "Slow dynamic response (minutes vs seconds)",
            "Minimum load 20-40% (poor renewable match)",
            "Stack lifetime 60,000-100,000 hours (proven durability)",
            "Liquid electrolyte adds complexity"
        ],
        primary_authority=[
            "Thyssenkrupp Uhde Chlorine Engineers technical data",
            "IEA Hydrogen Technology Perspectives 2023",
            "IRENA electrolyser cost database"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Very high confidence (mature technology with decades of data)."
    ),

    # ═══════════════════════════════════════════════════════════════════════
    # STORAGE TECHNOLOGIES
    # ═══════════════════════════════════════════════════════════════════════

    DoctrineBlock(
        topic="Type IV Compressed Hydrogen Storage at 700 bar",
        keywords=["Type IV", "700 bar", "composite", "overwrapped", "vehicle storage", "carbon fiber", "polymer liner"],
        conclusion_template="Type IV 700 bar tanks achieve {capacity} wt% hydrogen storage with {cycles} cycle life. Cost ${cost}/kWh stored. Gravimetric density {density} kg H2/kg system.",
        reasoning_framework="""
        Type IV composite overwrapped pressure vessel (COPV) technology for 700 bar hydrogen storage:

        1. TANK CONSTRUCTION:
           - Liner: High-density polyethylene (HDPE) or PA6 (polymer, not metal)
           - Overwrap: Carbon fiber reinforced polymer (CFRP)
           - Boss: Aluminum or stainless steel (load-bearing connection)
           - Fiber orientation: Hoop and helical windings for hoop and axial strength
           - Resin: Epoxy or similar thermosetting polymer

        2. PRESSURE RATING:
           - Nominal working pressure (NWP): 700 bar (70 MPa, 10,150 psi)
           - Burst pressure: 2.25x NWP = 1,575 bar (hydraulic test)
           - Service pressure: 87.5% NWP = 612.5 bar (accounts for temperature)
           - Pressure cycling: 15,000-20,000 cycles to NWP (design life)

        3. STORAGE CAPACITY:
           - Gravimetric density: 4.5-5.5 wt% H2 (kg H2 / kg system)
           - Volumetric density: 23-30 g/L (at 700 bar, 15 degrees C)
           - Typical tank: 5.6 kg H2 capacity, 125 L internal volume, ~120 kg total weight
           - Usable capacity: 90-95% (some H2 remains at minimum pressure)

        4. PERFORMANCE:
           - Fill time: 3-5 minutes (limited by thermodynamics, not tank)
           - Temperature rise during fill: 50-80 degrees C (adiabatic compression)
           - Cooling strategy: precooling H2 to -40 degrees C at station
           - Permeation: <1% per year through HDPE liner (acceptable for vehicles)

        5. SAFETY:
           - Thermally activated pressure relief device (TPRD): vents at 110 degrees C
           - Burst strength margin: 2.25x working pressure
           - Fire test: must vent safely without rupture (SAE J2579)
           - Gunfire test: penetration must not cause fragmentation
           - Drop test: no failure from 2m drop

        6. COST STRUCTURE:
           - Carbon fiber: 50-60% of tank cost (~$15/kg CFRP)
           - Manufacturing: filament winding, autoclaving, inspection
           - Cost per tank: $5,000-8,000 (2024, low volume)
           - Cost per kWh: $15-20/kWh (vs $100-150/kWh for batteries)
           - Learning curve: 20% cost reduction per doubling (high CF cost sensitivity)

        7. ADVANTAGES OVER TYPE III (metal liner):
           - 20-30% lighter (polymer liner vs aluminum)
           - No fatigue crack growth in liner (polymer self-heals microcracks)
           - Lower permeation with proper liner formulation
           - Corrosion-free liner

        8. REGULATORY COMPLIANCE:
           - UN ECE R134: Type approval for hydrogen vehicles (Europe)
           - SAE J2579: Fuel system safety (US)
           - ISO 19881: Gaseous hydrogen onboard storage systems
           - Periodic inspection: visual every 3 years, hydro test every 15 years (proposed)

        9. APPLICATIONS:
           - Light-duty fuel cell vehicles (passenger cars)
           - Forklifts and material handling
           - Drones (emerging)
           - Stationary storage (less common, Type I/III preferred)

        10. TECHNICAL CHALLENGES:
            - Carbon fiber cost and supply constraints
            - Permeation through liner (slow H2 loss)
            - End-of-life recycling (thermoset resin not recyclable)
            - Hydrogen embrittlement of boss threads (requires special alloys)
            - Conformability: cylindrical only (packaging constraints in vehicles)
        """,
        key_factors=[
            "Gravimetric density 4.5-5.5 wt% H2",
            "Volumetric density 23-30 g/L at 700 bar",
            "Pressure cycling: 15,000-20,000 cycles",
            "Cost $15-20/kWh stored (2024)",
            "Carbon fiber 50-60% of tank cost",
            "Permeation <1%/year acceptable for vehicles",
            "TPRD vents at 110 degrees C for fire safety",
            "Burst pressure 1,575 bar (2.25x NWP)"
        ],
        primary_authority=[
            "SAE J2579: Technical Information Report for Fuel Systems in Fuel Cell Vehicles",
            "ISO 19881: Gaseous hydrogen — Land vehicle fuel containers",
            "UN ECE R134: Hydrogen and fuel cell vehicles type approval",
            "DOE Hydrogen Storage Technical Targets"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence (widespread commercial deployment in FCEVs)."
    ),

    DoctrineBlock(
        topic="Liquid Hydrogen (LH2) Storage and Boil-Off",
        keywords=["liquid hydrogen", "LH2", "cryogenic", "boil-off", "20 Kelvin", "insulation", "evaporation"],
        conclusion_template="LH2 storage at {temp} K achieves {density} kg/m3 density but suffers {boil_off}% daily boil-off. Liquefaction energy {energy} kWh/kg H2.",
        reasoning_framework="""
        Liquid hydrogen (LH2) storage technology and boil-off management:

        1. THERMODYNAMIC PROPERTIES:
           - Boiling point: 20.28 K (-252.87 degrees C) at 1 atm
           - Critical point: 33.19 K, 13.13 bar (cannot liquefy above this)
           - Density: 70.8 kg/m3 (liquid) vs 0.09 kg/m3 (gas at STP)
           - Latent heat of vaporization: 445.6 kJ/kg (very low)
           - Specific heat: 9.7 kJ/(kg K) (liquid), 14.3 kJ/(kg K) (gas)

        2. LIQUEFACTION PROCESS:
           - Pre-cooling: ambient -> 80 K (liquid nitrogen heat exchanger)
           - Turbo-expander: 80 K -> 30 K (Joule-Thomson inefficient for H2)
           - Final cooling: ortho-para conversion catalyst (exothermic reaction)
           - Liquefaction energy: 10-15 kWh/kg H2 (33-50% of H2 energy content)
           - Efficiency: 30-40% (vs 90%+ for compression to 700 bar)

        3. ORTHO-PARA CONVERSION:
           - Hydrogen exists as ortho (parallel spins) and para (antiparallel spins)
           - At 300 K: 75% ortho, 25% para (equilibrium)
           - At 20 K: 0.2% ortho, 99.8% para (equilibrium)
           - Conversion heat release: 520 kJ/kg during cool-down
           - Catalyst needed: if unconverted, ortho->para occurs in tank (heats liquid, increases boil-off)

        4. STORAGE TANK DESIGN:
           - Inner vessel: Stainless steel or aluminum (cryogenic compatible)
           - Insulation: Multi-layer insulation (MLI, 30-100 layers) + vacuum jacket
           - Outer vessel: Carbon steel or aluminum
           - Vacuum pressure: <1 mPa (prevents convection/conduction)
           - Support structure: Low-conductivity supports (fiberglass, titanium)

        5. BOIL-OFF RATE:
           - Small tanks (50 L): 3-5% per day
           - Medium tanks (5,000 L): 0.5-1% per day
           - Large tanks (50,000 L): 0.05-0.2% per day
           - Spherical tanks best (minimize surface area to volume ratio)
           - Boil-off gas (BOG) must be vented or recaptured

        6. BOIL-OFF MANAGEMENT:
           - Active cooling: cryocoolers (electric) to re-liquefy BOG (energy intensive)
           - Passive venting: acceptable for short-term storage (days)
           - BOG recovery: compress and use as fuel (ships, industrial)
           - Pressure build-up: if venting blocked, tank pressure rises (safety risk)

        7. ADVANTAGES:
           - High volumetric density: 70.8 kg/m3 (2x better than 700 bar gas)
           - No high-pressure hazards (stored at 1-10 bar)
           - Suitable for large quantities (maritime, aerospace, bulk storage)
           - Faster refueling (liquid pumping vs gas compression)

        8. DISADVANTAGES:
           - Boil-off losses (1-5% per day depending on tank size)
           - High liquefaction energy (33-50% of H2 energy)
           - Complex cryogenic equipment (expensive, maintenance-intensive)
           - Ortho-para conversion essential (adds cost)
           - Cold embrittlement of structural materials

        9. APPLICATIONS:
           - Aerospace: Saturn V, Space Shuttle, SLS (proven technology)
           - Maritime: LH2 carriers for transcontinental transport
           - Bulk storage: large terminals (>100 tonnes)
           - Long-distance trucking: LH2 tanks in development (Daimler, Volvo)
           - NOT suitable for passenger vehicles (boil-off unacceptable if parked >1 week)

        10. COST:
            - Liquefaction cost: $2-4/kg H2 (energy + capex)
            - LH2 tank cost: $500-800/m3 (small), $200-400/m3 (large)
            - Insulation dominates cost for small tanks
            - Scale economies strong (large tanks much cheaper per unit volume)
        """,
        key_factors=[
            "Boiling point 20.28 K (-252.87 degrees C)",
            "Density 70.8 kg/m3 (2x better than 700 bar gas)",
            "Liquefaction energy 10-15 kWh/kg (33-50% of H2 energy)",
            "Boil-off 0.05-5% per day (scale-dependent)",
            "Ortho-para conversion essential to minimize boil-off",
            "Latent heat 445.6 kJ/kg (very low, easy to boil)",
            "Multi-layer insulation + vacuum required",
            "Best for large-scale, short-term storage"
        ],
        primary_authority=[
            "NASA Cryogenic Fluid Management Technology",
            "DOE Liquid Hydrogen Delivery Technical Assessment",
            "Air Liquide LH2 Industrial Handbook",
            "ISO 21013: Cryogenic vessels — Pressure-relief accessories"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence (decades of aerospace and industrial experience)."
    ),

    # ═══════════════════════════════════════════════════════════════════════
    # FUEL CELLS
    # ═══════════════════════════════════════════════════════════════════════

    DoctrineBlock(
        topic="PEM Fuel Cell Membrane Electrode Assembly (MEA)",
        keywords=["PEM", "fuel cell", "MEA", "membrane", "catalyst", "platinum", "Nafion", "electrode"],
        conclusion_template="PEM fuel cell MEA achieves {efficiency}% efficiency at {power_density} W/cm2. Pt loading {loading} mg/cm2. Lifetime {lifetime} hours.",
        reasoning_framework="""
        Proton Exchange Membrane (PEM) fuel cell MEA design and performance:

        1. MEA STRUCTURE:
           - Proton exchange membrane (PEM): 10-50 microns thick
           - Anode catalyst layer (ACL): Pt or Pt-Ru on carbon support
           - Cathode catalyst layer (CCL): Pt or Pt-Co on carbon support
           - Gas diffusion layers (GDL): Carbon paper or cloth with microporous layer
           - Total MEA thickness: 200-500 microns

        2. MEMBRANE MATERIALS:
           - Nafion (DuPont): perfluorosulfonic acid (PFSA) polymer, industry standard
           - Gore-Select: reinforced PFSA (higher mechanical strength)
           - Hydrocarbon membranes: lower cost, lower conductivity
           - Proton conductivity: 0.1 S/cm (hydrated Nafion at 80 degrees C)
           - Water management critical: membrane must stay hydrated

        3. CATALYST LAYERS:
           - Anode reaction: H2 -> 2H+ + 2e- (fast kinetics, low Pt loading)
           - Cathode reaction: O2 + 4H+ + 4e- -> 2H2O (slow kinetics, high Pt loading)
           - Total Pt loading: 0.3-0.6 mg/cm2 (automotive target <0.125 mg/cm2)
           - Cathode: 70-80% of total Pt (sluggish oxygen reduction reaction)
           - Ionomer in catalyst layer: Nafion dispersion for proton conduction

        4. PERFORMANCE:
           - Operating temperature: 60-80 degrees C (low-temp PEM)
           - Operating pressure: 1-3 bar (automotive), 1-10 bar (stationary)
           - Current density: 0.6-1.0 A/cm2 (typical), up to 2.0 A/cm2 (peak)
           - Voltage: 0.6-0.7 V per cell at rated current (1.23 V theoretical)
           - Stack efficiency: 50-60% (HHV) at rated power

        5. POWER DENSITY:
           - Gravimetric: 2.0-3.5 kW/kg (stack level, automotive)
           - Volumetric: 3.0-4.0 kW/L (stack level)
           - Area-specific: 0.6-1.0 W/cm2 active area
           - DOE 2025 target: 850 W/kg, 850 W/L (stack)

        6. LIFETIME AND DEGRADATION:
           - Automotive target: 5,000-8,000 hours (150,000+ miles)
           - Stationary target: 40,000-80,000 hours (5-10 years)
           - Voltage degradation: <10% over lifetime
           - Failure modes: Pt dissolution, carbon corrosion, membrane thinning, catalyst poisoning

        7. WATER MANAGEMENT:
           - Membrane requires hydration (40-100% relative humidity)
           - Cathode produces water (potential flooding)
           - Anode can dry out (especially at low current)
           - Humidification: external humidifier or self-humidification
           - GDL design critical: balance water removal vs membrane hydration

        8. COST STRUCTURE (2024):
           - Pt catalyst: $30-50/kW (at 0.3 mg/cm2, $30/g Pt)
           - Membrane: $20-30/kW
           - Bipolar plates: $10-20/kW (graphite or coated metal)
           - GDL: $5-10/kW
           - Total stack: $100-200/kW (automotive, volume production)
           - DOE target: $40/kW by 2030

        9. EFFICIENCY:
           - Peak efficiency: 60% HHV (low current density)
           - Rated efficiency: 50-55% HHV (0.6-0.7 A/cm2)
           - Low-load efficiency: 40-45% HHV (parasitic losses dominate)
           - System efficiency: 45-50% HHV (including air compressor, coolant pump)

        10. TECHNICAL CHALLENGES:
            - Pt cost and supply (need to reduce to <0.1 mg/cm2)
            - Cold start: freeze/thaw cycles damage membrane
            - Durability under dynamic load (automotive duty cycle harsh)
            - Contaminants: CO poisons Pt (must keep <10 ppm in H2)
            - Air filtration: NOx, SOx degrade performance
        """,
        key_factors=[
            "Efficiency 50-60% HHV at rated power",
            "Pt loading 0.3-0.6 mg/cm2 (target <0.125 mg/cm2)",
            "Current density 0.6-1.0 A/cm2 typical, 2.0 A/cm2 peak",
            "Power density 2.0-3.5 kW/kg (automotive stack)",
            "Operating temperature 60-80 degrees C",
            "Lifetime 5,000-8,000 hours (automotive), 40,000-80,000 hours (stationary)",
            "Stack cost $100-200/kW (volume production, 2024)",
            "Water management critical for performance"
        ],
        primary_authority=[
            "DOE Fuel Cell Technical Targets 2025",
            "Toyota Mirai, Hyundai Nexo technical specifications",
            "Ballard Power Systems MEA design data",
            "Journal of Power Sources (extensive PEM FC literature)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence (thousands of FCEVs deployed, extensive R&D data)."
    ),

    DoctrineBlock(
        topic="Solid Oxide Fuel Cell (SOFC) for Stationary Power",
        keywords=["SOFC", "solid oxide", "high temperature", "stationary", "CHP", "ceramic", "zirconia"],
        conclusion_template="SOFC achieves {efficiency}% electrical efficiency at {temp} degrees C. CHP efficiency {chp}%. Lifetime {lifetime} hours. Fuel flexibility key advantage.",
        reasoning_framework="""
        Solid Oxide Fuel Cell (SOFC) technology for stationary power generation:

        1. TECHNOLOGY FUNDAMENTALS:
           - Electrolyte: Yttria-stabilized zirconia (YSZ) ceramic, 10-20 microns thick
           - Anode: Nickel-YSZ cermet (ceramic-metal composite)
           - Cathode: Lanthanum strontium manganite (LSM) or similar perovskite
           - Operating temperature: 700-1000 degrees C (high-temp SOFC)
           - Intermediate temperature SOFC: 500-700 degrees C (faster start, lower materials stress)

        2. ELECTROCHEMISTRY:
           - Cathode: O2 + 4e- -> 2O2- (oxide ions produced)
           - Oxide ions migrate through YSZ electrolyte (O2- conductor at high temp)
           - Anode: H2 + O2- -> H2O + 2e- (or CH4 internal reforming)
           - Voltage: 0.7-0.8 V per cell at rated current

        3. EFFICIENCY:
           - Electrical efficiency: 50-60% HHV (natural gas fuel)
           - CHP (combined heat and power) efficiency: 80-90% total
           - High-grade heat available (600-800 degrees C exhaust)
           - Can reform natural gas internally (no external reformer needed)

        4. FUEL FLEXIBILITY:
           - Natural gas (primary fuel): internal reforming in anode
           - Biogas: tolerates H2S and other impurities (vs PEM)
           - Hydrogen: high efficiency, no reforming needed
           - Propane, diesel (with external reformer): marine, off-grid applications
           - Syngas from coal/biomass gasification: carbon-tolerant anode

        5. STACK DESIGN:
           - Planar design: flat cells with metallic interconnects (most common)
           - Tubular design: Siemens-Westinghouse legacy (better thermal cycling)
           - Cell size: 10x10 cm to 20x20 cm active area
           - Stack power: 1-500 kW (modular scaling)

        6. LIFETIME AND DEGRADATION:
           - Design life: 40,000-80,000 hours (5-10 years)
           - Voltage degradation: 0.2-0.5% per 1,000 hours
           - Failure modes: chromium poisoning (from interconnect), nickel coarsening, delamination
           - Thermal cycling damage: CTE mismatch causes cracks (limit start/stop cycles)

        7. ADVANTAGES:
           - Highest efficiency of all fuel cell types
           - Fuel flexibility (can use natural gas, biogas, H2)
           - No precious metal catalysts (cost advantage)
           - High-quality waste heat for CHP
           - Carbon monoxide tolerance (even beneficial as fuel)

        8. DISADVANTAGES:
           - High operating temperature (materials challenges, slow start)
           - Start-up time: 1-4 hours from cold (vs minutes for PEM)
           - Thermal cycling limitations (not suitable for frequent start/stop)
           - Sealing challenges at high temperature
           - Limited dynamic response (baseload operation preferred)

        9. APPLICATIONS:
           - Distributed CHP: hospitals, data centers, commercial buildings
           - Microgrids: 100 kW - 1 MW systems
           - Backup power: telecom, critical facilities (if minimal cycling)
           - Industrial heat: chemical plants, refineries (utilize high-temp exhaust)
           - Marine: APU (auxiliary power unit) for ships (Bloom Energy, Ceres Power)

        10. COST AND COMMERCIALIZATION:
            - System cost: $4,000-7,000/kW installed (2024)
            - Stack cost: $1,500-3,000/kW
            - High capex, low opex (long maintenance intervals)
            - Bloom Energy: largest commercial deployment (200+ MW installed)
            - Learning curve: 15% cost reduction per doubling of capacity
        """,
        key_factors=[
            "Electrical efficiency 50-60% HHV (best of all fuel cell types)",
            "CHP efficiency 80-90% total (including heat recovery)",
            "Operating temperature 700-1000 degrees C (high-temp) or 500-700 degrees C (IT-SOFC)",
            "Fuel flexibility: natural gas, biogas, H2, propane, diesel",
            "Lifetime 40,000-80,000 hours (baseload operation)",
            "No precious metals (nickel-based catalysts)",
            "Slow start-up (1-4 hours) limits dynamic applications",
            "System cost $4,000-7,000/kW installed (2024)"
        ],
        primary_authority=[
            "Bloom Energy commercial SOFC specifications",
            "DOE SOFC technical targets and status",
            "Ceres Power steel cell technology",
            "Mitsubishi Power fuel cell systems"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence (commercial deployments at MW scale)."
    ),

    # ═══════════════════════════════════════════════════════════════════════
    # INFRASTRUCTURE
    # ═══════════════════════════════════════════════════════════════════════

    DoctrineBlock(
        topic="Hydrogen Pipeline and Embrittlement per ASME B31.12",
        keywords=["pipeline", "embrittlement", "ASME B31.12", "steel", "cracking", "diffusion", "pressure"],
        conclusion_template="Hydrogen pipelines per ASME B31.12 require {steel_grade} steel to resist embrittlement. Design pressure {pressure} bar. Inspection interval {interval} years.",
        reasoning_framework="""
        Hydrogen pipeline design and hydrogen embrittlement mitigation per ASME B31.12:

        1. HYDROGEN EMBRITTLEMENT MECHANISMS:
           - Atomic hydrogen diffuses into steel lattice (small atom size)
           - Hydrogen accumulates at grain boundaries, inclusions, microvoids
           - Reduces fracture toughness, ductility, and fatigue resistance
           - Hydrogen-induced cracking (HIC): blistering, stepwise cracking
           - Stress corrosion cracking (SCC): synergy with tensile stress

        2. MATERIAL SUSCEPTIBILITY:
           - High-strength steels: more susceptible (yield strength >550 MPa risky)
           - Low-alloy steels: moderate susceptibility
           - Austenitic stainless steels (300 series): excellent resistance (FCC lattice)
           - Ferritic steels: susceptible (BCC lattice allows H diffusion)
           - Aluminum alloys: immune (no embrittlement mechanism)

        3. ASME B31.12 REQUIREMENTS:
           - Applicable to: hydrogen pipelines, piping in gaseous and liquefied service
           - Design pressure: based on hoop stress with hydrogen service factor
           - Material selection: Table 5-1 lists approved steels (mostly API 5L X42-X52)
           - Maximum hardness: 22 HRC (Rockwell C) to limit embrittlement
           - Welds: post-weld heat treatment (PWHT) for stress relief

        4. DESIGN CONSIDERATIONS:
           - Pressure: 20-100 bar typical for transmission pipelines
           - Wall thickness: increased vs natural gas (lower allowable stress)
           - Hydrogen service factor: 0.5-0.75 depending on steel grade
           - Fracture mechanics: assume worst-case flaw size, KIC threshold

        5. INSPECTION AND MONITORING:
           - Baseline inspection: UT (ultrasonic testing), radiography
           - In-service inspection: ILI (inline inspection) pigs for cracks
           - Interval: 5-10 years depending on risk assessment
           - Leak detection: H2 sensors, flow balance, pressure monitoring
           - Repair: grind out surface cracks, weld repair with qualified procedures

        6. EXISTING HYDROGEN PIPELINES:
           - US: 1,600 miles of H2 pipelines (Gulf Coast, Great Lakes)
           - Europe: 1,000+ miles (Germany, Netherlands, Belgium)
           - Operating since: 1960s-1970s (decades of safe operation)
           - Materials: mostly vintage steels, modern codes more conservative

        7. REPURPOSING NATURAL GAS PIPELINES:
           - Attractive for cost (existing ROW, infrastructure)
           - Challenges: unknown embrittlement state, vintage steels not B31.12 compliant
           - Assessment needed: material testing, crack detection, pressure deration
           - Blending strategy: 5-20% H2 in natural gas as interim step

        8. HYDROGEN BLENDING LIMITS:
           - 5% H2: generally safe in existing NG pipelines (minimal impact)
           - 10-20% H2: requires assessment (embrittlement, end-use equipment compatibility)
           - >20% H2: likely requires pipeline upgrades or replacement
           - End-use concerns: domestic appliances, gas turbines not H2-ready

        9. LEAK BEHAVIOR:
           - Hydrogen molecule: smallest (kinetic diameter 0.289 nm)
           - Higher leak rates through same defect vs CH4 (3.8x diffusivity)
           - Flame invisible in daylight (safety concern)
           - Wide flammability range: 4-75% in air (vs 5-15% for CH4)
           - Buoyancy: rises rapidly (reduces ground-level accumulation risk)

        10. COST:
            - New H2 pipeline: $1-2M per mile (20 inch, 100 bar)
            - Repurposing NG pipeline: $0.3-0.8M per mile (assessment + upgrades)
            - Inspection: $50-150K per mile (ILI, crack detection)
            - Compressor stations: every 100-200 miles (H2 requires more power than CH4)
        """,
        key_factors=[
            "ASME B31.12 governs hydrogen pipeline design in US",
            "Maximum hardness 22 HRC to limit embrittlement",
            "Hydrogen service factor 0.5-0.75 reduces allowable stress",
            "High-strength steels (>550 MPa yield) avoid due to embrittlement",
            "Austenitic stainless (300 series) excellent embrittlement resistance",
            "1,600 miles existing H2 pipelines in US (safe operation since 1960s)",
            "Hydrogen blending: 5% safe, 10-20% requires assessment, >20% major upgrades",
            "Inspection interval 5-10 years via inline inspection (ILI)"
        ],
        primary_authority=[
            "ASME B31.12: Hydrogen Piping and Pipelines",
            "DOE Hydrogen Pipeline Working Group Report",
            "European Hydrogen Backbone Study 2020",
            "API RP 941: Steels for Hydrogen Service at Elevated Temperatures and Pressures"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on codes and embrittlement mechanisms. Medium confidence on repurposing NG pipelines (case-by-case assessment needed)."
    ),

    DoctrineBlock(
        topic="Hydrogen Refueling Station Design per ISO 19880-1",
        keywords=["refueling", "fueling station", "700 bar", "precooling", "dispenser", "ISO 19880", "SAE J2601"],
        conclusion_template="H2 refueling station per ISO 19880-1 delivers {flow} kg/min at {pressure} bar with precooling to {temp} degrees C. Station capacity {capacity} kg/day.",
        reasoning_framework="""
        Hydrogen refueling station design per ISO 19880-1 and SAE J2601:

        1. STATION ARCHITECTURE:
           - Hydrogen supply: delivered tube trailer, pipeline, or on-site generation
           - Compression: multi-stage compressor to 450-900 bar (cascade storage)
           - Storage: high-pressure (900 bar), medium (450 bar), low (200 bar) banks
           - Precooling: chiller to -40 degrees C (required for 700 bar fills)
           - Dispenser: hose, nozzle, breakaway coupling, communications interface

        2. REFUELING PROTOCOL (SAE J2601):
           - Target pressure: 700 bar NWP (some stations 350 bar for buses/trucks)
           - Precooling: -40 degrees C (prevents tank temperature >85 degrees C)
           - Fill rate: 1.0-1.5 kg/min typical (5.6 kg fill in 3-5 minutes)
           - Pressure ramp: conservative initial ramp, then aggressive (avoid overshoot)
           - Communication: infrared (IR) link vehicle -> station (tank temp, SOC)
           - End-of-fill: 90-95% SOC (State of Charge) at 15 degrees C

        3. COMPRESSION:
           - Compressor types: reciprocating (piston), ionic liquid, hydraulic
           - Multi-stage: 3-5 stages to reach 900 bar
           - Intercooling: required between stages (manage heat of compression)
           - Power consumption: 2-3 kWh/kg H2 compressed from 200 bar to 900 bar
           - Maintenance: seals, valves every 2,000-5,000 hours (high wear item)

        4. CASCADE STORAGE:
           - Three pressure banks: low (200-300 bar), medium (450-500 bar), high (900 bar)
           - Filling strategy: draw from low bank first, then medium, then high (equalizes pressure)
           - Storage capacity: 150-500 kg on-site (serves 50-150 vehicles/day)
           - Pressure vessels: Type 1 steel or Type 3 composite (stationary)

        5. PRECOOLING SYSTEM:
           - Chiller: mechanical refrigeration to -40 degrees C
           - Heat exchanger: H2 flows through cold side before dispensing
           - Energy: 0.5-1.0 kWh/kg H2 cooled
           - Critical for 700 bar (adiabatic compression heats H2 50-80 degrees C during fill)
           - 350 bar fills: less critical (lower compression heating)

        6. DISPENSING:
           - Nozzle: SAE J2600 standardized receptacle (prevents mis-fueling)
           - Breakaway coupling: separates if vehicle drives away during fill
           - Mass flow meter: measures kg H2 dispensed
           - Safety: emergency stop, leak detection, ventilation, fire detection

        7. STATION CAPACITY:
           - Small station: 50-100 kg/day (10-20 cars)
           - Medium station: 200-500 kg/day (40-100 cars)
           - Large station: 1,000+ kg/day (200+ cars or bus depot)
           - Utilization: 30-50% typical (peak hours, geographic demand)

        8. COST STRUCTURE:
           - Small station (100 kg/day): $1.5-2.5M installed
           - Medium station (500 kg/day): $3-5M installed
           - Large station (1,000 kg/day): $5-8M installed
           - Compression: 30-40% of capex
           - Precooling: 10-15% of capex
           - Dispenser: 5-10% of capex

        9. SAFETY (NFPA 2):
           - Setback distances: from buildings, lot lines, ignition sources
           - Ventilation: natural or forced to prevent H2 accumulation
           - Hydrogen sensors: 25% LEL (lower explosive limit) alarm, 50% LEL shutdown
           - Fire suppression: typically not used (H2 fires self-extinguish if leak stops)
           - Emergency shutdown: manual and automatic (leak, fire, seismic)

        10. OPERATIONAL CHALLENGES:
            - Hydrogen supply cost: $5-15/kg at station gate (dominates total cost)
            - Low utilization: early stations 10-30% (chicken-and-egg with FCEVs)
            - Maintenance: compressor high wear, chiller reliability
            - Permitting: complex (fire marshal, building, environmental)
            - Business model: difficult to achieve ROI without high throughput
        """,
        key_factors=[
            "Refueling protocol: SAE J2601 (700 bar, -40 degrees C precool)",
            "Fill rate 1.0-1.5 kg/min (5.6 kg in 3-5 minutes)",
            "Compression power 2-3 kWh/kg H2 (200 bar to 900 bar)",
            "Precooling essential for 700 bar (prevents tank overheat)",
            "Cascade storage: 3 banks (200, 450, 900 bar) for efficient filling",
            "Station cost $1.5-8M depending on capacity (100-1,000 kg/day)",
            "Safety setbacks per NFPA 2 (buildings, ignition sources)",
            "Low utilization challenge (10-30% typical at early stations)"
        ],
        primary_authority=[
            "ISO 19880-1: Gaseous hydrogen — Fueling stations — Part 1: General requirements",
            "SAE J2601: Fueling protocols for light duty gaseous hydrogen surface vehicles",
            "NFPA 2: Hydrogen Technologies Code (Chapter 13: Fueling stations)",
            "California Fuel Cell Partnership station data"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence (100+ stations operating globally, well-documented standards)."
    ),

    # ═══════════════════════════════════════════════════════════════════════
    # SAFETY
    # ═══════════════════════════════════════════════════════════════════════

    DoctrineBlock(
        topic="Hydrogen Safety per NFPA 2",
        keywords=["NFPA 2", "safety", "flammability", "explosion", "ventilation", "detection", "setback"],
        conclusion_template="NFPA 2 requires {setback} ft setback from {source}. Ventilation {ach} ACH. H2 detectors at {alarm}% LEL alarm, {shutdown}% LEL shutdown.",
        reasoning_framework="""
        Hydrogen safety requirements per NFPA 2: Hydrogen Technologies Code:

        1. HYDROGEN HAZARD PROPERTIES:
           - Flammability limits: 4-75% by volume in air (very wide range)
           - Ignition energy: 0.02 mJ (10x lower than gasoline)
           - Autoignition temperature: 585 degrees C (high, but lower than methane 580 C)
           - Flame speed: 3.46 m/s (7x faster than gasoline)
           - Flame visibility: nearly invisible in daylight (UV/IR sensors needed)
           - Buoyancy: diffuses upward rapidly (reduces pooling risk vs gasoline)

        2. NFPA 2 SCOPE:
           - Applies to: generation, storage, piping, use of gaseous and liquefied H2
           - Covers: industrial, commercial, residential applications
           - Exclusions: bulk storage >15,000 lb (NFPA 55), marine vessels (other codes)
           - Compliance: adopted by AHJ (authority having jurisdiction) in building codes

        3. SETBACK DISTANCES (NFPA 2 Table 7.3.2.2):
           - From buildings: 25 ft (outdoor storage <3,000 SCF), 50 ft (>3,000 SCF)
           - From lot lines: 15 ft (small), 25 ft (medium), 50 ft (large)
           - From ignition sources: 20 ft (open flames, welding, hot surfaces)
           - From air intakes: 50 ft (prevent H2 ingress into HVAC)
           - Reduction allowed: if barriers, detectors, safety systems (engineered approach)

        4. VENTILATION REQUIREMENTS:
           - Outdoor: natural ventilation acceptable (H2 rises, disperses)
           - Indoor: mechanical ventilation required (6 ACH minimum, 12 ACH preferred)
           - Vent location: high point in room (H2 accumulates at ceiling)
           - Vent capacity: sufficient to keep H2 <25% LEL during normal operation
           - Emergency ventilation: activated on H2 detection (12+ ACH)

        5. HYDROGEN DETECTION:
           - Sensor technology: catalytic bead, electrochemical, thermal conductivity
           - Sensor location: ceiling level, near potential leak sources
           - Alarm setpoints: 25% LEL (1% H2 in air) warning, 50% LEL (2%) shutdown
           - Response time: <5 seconds T90 (time to 90% of final reading)
           - Calibration: quarterly with certified H2 gas (drift common failure mode)

        6. ELECTRICAL EQUIPMENT:
           - Classified location: Class I Division 2 (Zone 2) where H2 could be present
           - Electrical code: NEC Article 500 (hazardous locations)
           - Equipment: explosion-proof or purged/pressurized enclosures
           - Ignition sources: eliminate within 25 ft of H2 equipment

        7. PIPING AND CONNECTIONS:
           - Materials: stainless steel 300 series, copper (small sizes), approved polymers
           - Joints: welded preferred (no threaded fittings for permanent installations)
           - Pressure relief: PRD (pressure relief device) on every isolated section
           - Purging: N2 or He purge before introducing H2 (prevent air-H2 mixture)

        8. FIRE SUPPRESSION:
           - Hydrogen fires: typically allow to burn out (suppress leak, not fire)
           - Water spray: cooling adjacent structures, vessels (prevent BLEVE)
           - Foam/dry chemical: ineffective on H2 (molecule too small)
           - Automatic sprinklers: protect building, not H2 fire itself

        9. EMERGENCY PLANNING:
           - Emergency shutdown: manual (red button) and automatic (leak, fire, seismic)
           - ESD actions: close valves, stop compressors, vent to safe location
           - Training: personnel on H2 hazards, leak response, fire response
           - Coordination: fire department pre-planning (H2 fires unique)

        10. RISK ASSESSMENT:
            - QRA (quantitative risk assessment) for large installations
            - Scenarios: jet fire, BLEVE, deflagration, detonation (confined space)
            - Consequence modeling: ALOHA, PHAST, CFD (computational fluid dynamics)
            - Risk tolerance: individual risk <10^-6/year (public), <10^-4/year (workers)
        """,
        key_factors=[
            "Flammability range 4-75% (very wide, easier to ignite than gasoline)",
            "Ignition energy 0.02 mJ (10x lower than gasoline)",
            "Buoyancy: rises rapidly (reduces ground-level pooling)",
            "Setbacks 15-50 ft depending on quantity and exposure",
            "Ventilation 6-12 ACH (indoor), high-point exhaust",
            "H2 detectors: 25% LEL alarm (1% H2), 50% LEL shutdown (2% H2)",
            "Class I Div 2 electrical (explosion-proof or purged)",
            "Emergency shutdown: manual and automatic on leak/fire"
        ],
        primary_authority=[
            "NFPA 2: Hydrogen Technologies Code (2023 edition)",
            "NEC Article 500: Hazardous (Classified) Locations",
            "IFC Chapter 53: Compressed Gases (hydrogen provisions)",
            "DOE Hydrogen Safety Best Practices Manual"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Very high confidence (NFPA 2 is consensus code with decades of industry input)."
    ),

    # ═══════════════════════════════════════════════════════════════════════
    # ECONOMICS
    # ═══════════════════════════════════════════════════════════════════════

    DoctrineBlock(
        topic="Levelized Cost of Hydrogen (LCOH) Analysis",
        keywords=["LCOH", "cost", "economics", "capex", "opex", "electricity", "capacity factor", "NPV"],
        conclusion_template="Green hydrogen LCOH is ${lcoh}/kg at {cf}% capacity factor with electricity at ${elec}/kWh. Dominated by {component} cost.",
        reasoning_framework="""
        Levelized Cost of Hydrogen (LCOH) calculation and cost drivers:

        1. LCOH DEFINITION:
           - LCOH = total lifecycle cost / total hydrogen produced ($/kg H2)
           - Analogous to LCOE (levelized cost of electricity)
           - Inputs: capex, opex (fixed and variable), financing costs, production volume
           - Time horizon: 20-30 years typical (electrolyzer plant life)

        2. CAPITAL COSTS (CAPEX):
           - Electrolyzer: $800-1,400/kW (PEM), $500-900/kW (alkaline)
           - Balance of plant: 30-50% of electrolyzer cost (water treatment, power electronics, H2 processing)
           - Site preparation: $100-300/kW (civil, electrical, permitting)
           - Renewables co-location: $800-1,200/kW (solar), $1,200-1,800/kW (wind)
           - Total installed cost: $1,500-3,000/kW (electrolyzer + BoP + site)

        3. OPERATING COSTS (OPEX):
           - Electricity: 50-60 kWh/kg H2 (major variable cost)
           - Water: 9-10 L/kg H2 (minimal cost unless remote location)
           - Maintenance: 2-3% of capex per year
           - Stack replacement: every 60,000-90,000 hours (30-40% of initial capex)
           - Labor: $50-100K/year per technician (site size dependent)

        4. ELECTRICITY COST SENSITIVITY:
           - At $0.02/kWh: electricity = $1.00-1.20/kg H2 (60% of LCOH)
           - At $0.05/kWh: electricity = $2.50-3.00/kg H2 (75% of LCOH)
           - At $0.10/kWh: electricity = $5.00-6.00/kg H2 (85% of LCOH)
           - Conclusion: cheap electricity dominates LCOH for green H2

        5. CAPACITY FACTOR IMPACT:
           - Capacity factor (CF): actual production / nameplate capacity
           - Low CF (30%): capex amortized over less H2 -> doubles LCOH vs 80% CF
           - Renewable-coupled: 25-40% CF typical (solar/wind availability)
           - Grid-connected: 60-90% CF achievable (but electricity more expensive)
           - Optimization: balance cheap renewable hours vs full utilization

        6. GREEN HYDROGEN LCOH (2024):
           - Best case: $2.50-3.50/kg (cheap renewables, high CF, large scale)
           - Typical: $4.00-6.00/kg (moderate renewables, 40% CF)
           - Worst case: $8.00-12.00/kg (expensive electricity, low CF, small scale)
           - DOE target: $2/kg by 2026, $1/kg by 2031 (Hydrogen Shot)

        7. BLUE HYDROGEN LCOH (2024):
           - Natural gas: $1.00-1.50/kg H2 (at $3-5/MMBtu gas)
           - CCS cost: $0.50-1.50/kg H2 ($30-70/tonne CO2 captured)
           - Total LCOH: $1.50-3.00/kg H2
           - Carbon price sensitivity: +$0.10/kg per $10/tonne CO2 price

        8. GRAY HYDROGEN LCOH (2024):
           - SMR without CCS: $1.00-1.50/kg H2 (baseline, but high carbon)
           - Natural gas price dominates: $0.70-1.00/kg per $1/MMBtu gas
           - Carbon penalty: if $50/tonne CO2, adds $0.50/kg to LCOH

        9. COST REDUCTION PATHWAYS:
           - Electrolyzer learning curve: 18% cost reduction per doubling of capacity
           - Renewable cost decline: solar $0.01-0.02/kWh already achieved (some regions)
           - Scale economies: 1 GW plant 30% cheaper per kW than 10 MW
           - Technology: advanced electrolyzers (SOEC, AEM) promise 70% efficiency
           - Policy: subsidies (IRA 45V $3/kg), carbon prices, mandates (reduce effective LCOH)

        10. BREAKEVEN ANALYSIS:
            - Green vs gray: need <$0.03/kWh electricity to compete (without carbon price)
            - Green vs blue: green wins if electricity <$0.04/kWh or carbon >$100/tonne
            - Policy-adjusted: IRA 45V tax credit ($3/kg) makes green LCOH <$2/kg (US)
            - Geographic: Chile, Australia, Middle East have <$2/kg potential (solar/wind resources)
        """,
        key_factors=[
            "LCOH = capex + opex / total H2 produced over lifetime",
            "Electricity cost dominates green LCOH (60-85% of total)",
            "Green H2: $2.50-6.00/kg (2024), target $1-2/kg by 2030",
            "Blue H2: $1.50-3.00/kg (natural gas + CCS)",
            "Gray H2: $1.00-1.50/kg (no carbon penalty)",
            "Capacity factor critical: 30% CF doubles LCOH vs 80% CF",
            "Learning curve: 18% cost drop per capacity doubling",
            "IRA 45V tax credit: $3/kg for clean H2 (US)"
        ],
        primary_authority=[
            "IEA Global Hydrogen Review 2023",
            "IRENA Green Hydrogen Cost Reduction Report 2020",
            "DOE Hydrogen Shot ($1/kg by 2031 target)",
            "BloombergNEF Hydrogen Levelized Cost Update 2024"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on current costs. Medium confidence on future costs (technology and policy uncertainty)."
    ),

    # Add 15 more doctrine blocks to reach 25+ total...

    DoctrineBlock(
        topic="Hydrogen Color Classification and Carbon Intensity",
        keywords=["color", "green", "blue", "gray", "carbon intensity", "lifecycle emissions", "classification"],
        conclusion_template="Hydrogen color {color} has lifecycle emissions of {emissions} kg CO2/kg H2. Production method: {method}.",
        reasoning_framework="""
        Hydrogen color classification and associated carbon intensity:

        1. GREEN HYDROGEN (renewable electricity):
           - Production: electrolysis powered by solar, wind, hydro, or renewable grid
           - Carbon intensity: 0.1-0.5 kg CO2/kg H2 (minimal, from equipment manufacturing)
           - Purity: 99.9%+ (electrolysis produces pure H2)
           - Cost: $2.50-6.00/kg (2024), falling rapidly
           - Policy: preferred in EU taxonomy, IRA 45V (if <0.45 kg CO2eq/kg H2)

        2. BLUE HYDROGEN (fossil fuels with CCS):
           - Production: SMR or ATR (autothermal reforming) with carbon capture
           - Carbon intensity: 1-2 kg CO2/kg H2 (90-95% capture, residual emissions)
           - Cost: $1.50-3.00/kg
           - Advantage: baseload production, existing infrastructure
           - Controversy: methane leakage, CCS permanence

        3. GRAY HYDROGEN (fossil fuels, no CCS):
           - Production: SMR without carbon capture (conventional)
           - Carbon intensity: 9-12 kg CO2/kg H2 (unabated emissions)
           - Cost: $1.00-1.50/kg (cheapest, but high carbon)
           - Current dominance: 95% of global H2 production (2024)

        4. TURQUOISE HYDROGEN (methane pyrolysis):
           - Production: CH4 -> C(solid) + 2H2 (thermal decomposition, no CO2)
           - Carbon intensity: 0.5-2 kg CO2/kg H2 (depends on heat source, carbon fate)
           - Carbon product: solid graphite (potential value, or landfill burden)
           - Status: pilot/demonstration (BASF, Monolith Materials)

        5. PINK/PURPLE HYDROGEN (nuclear electricity):
           - Production: electrolysis powered by nuclear plants
           - Carbon intensity: 0.2-1.0 kg CO2/kg H2 (uranium mining, construction)
           - Advantage: baseload, no weather dependence
           - High-temp electrolysis: SOEC at 800 C using nuclear heat (higher efficiency)

        6. YELLOW HYDROGEN (grid electricity, mixed sources):
           - Production: electrolysis from grid (coal, gas, nuclear, renewables mix)
           - Carbon intensity: 5-15 kg CO2/kg H2 (depends on grid carbon intensity)
           - Intermediate step: grid decarbonizes over time -> yellow becomes greener

        7. BLACK/BROWN HYDROGEN (coal/lignite gasification):
           - Production: coal gasification without CCS
           - Carbon intensity: 15-25 kg CO2/kg H2 (highest of all colors)
           - Rare: mostly historical or niche (China)

        8. WHITE HYDROGEN (natural geological):
           - Production: naturally occurring in subsurface (serpentinization, radiolysis)
           - Carbon intensity: ~0 kg CO2/kg H2 (if directly extracted)
           - Status: exploration phase, Mali discovery 2024 (not yet commercial)

        9. POLICY THRESHOLDS:
           - EU Taxonomy: <3 kg CO2/kg H2 lifecycle for "low-carbon hydrogen"
           - UK Low Carbon Hydrogen Standard: <2.4 kg CO2/kg H2
           - IRA 45V (US): <0.45 kg for $3/kg credit, <1.5 kg for $1/kg credit
           - Certification: CertifHy (EU), ISCC (International Sustainability & Carbon Certification)

        10. LIFECYCLE ASSESSMENT (LCA) CONSIDERATIONS:
            - Scope: well-to-gate (production) or well-to-wheel (end use)
            - Methane leakage: 1-3% supply chain leakage adds 2-4 kg CO2eq/kg H2 (blue)
            - Renewable curtailment: using otherwise-wasted renewable energy -> near-zero emissions
            - Grid carbon intensity: dynamic (time-of-use) vs average annual
        """,
        key_factors=[
            "Green: <0.5 kg CO2/kg H2 (renewables)",
            "Blue: 1-2 kg CO2/kg H2 (fossil + 90%+ CCS)",
            "Gray: 9-12 kg CO2/kg H2 (fossil, no CCS)",
            "EU threshold: <3 kg CO2/kg for low-carbon",
            "IRA 45V: <0.45 kg for $3/kg credit",
            "Methane leakage critical for blue H2 lifecycle",
            "White H2: geological, exploration phase",
            "Color is production method, not end-use"
        ],
        primary_authority=[
            "IEA Global Hydrogen Review 2023 (color definitions)",
            "EU Delegated Acts on Renewable Hydrogen",
            "US IRA Section 45V (Clean Hydrogen Production Tax Credit)",
            "IPCC AR6 WG3 (hydrogen lifecycle emissions)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Solid-State Hydrogen Storage in Metal Hydrides",
        keywords=["metal hydride", "solid state", "storage", "reversible", "gravimetric", "volumetric", "LaNi5"],
        conclusion_template="Metal hydride {material} achieves {capacity} wt% H2 storage at {pressure} bar and {temp} degrees C. Reversible over {cycles} cycles.",
        reasoning_framework="""
        Metal hydride solid-state hydrogen storage technology:

        1. FUNDAMENTAL CHEMISTRY:
           - Reversible reaction: M + x/2 H2 <-> MHx (metal + hydrogen <-> metal hydride)
           - Exothermic absorption: heat released when H2 absorbed
           - Endothermic desorption: heat required to release H2
           - Pressure-composition isotherms: equilibrium pressure varies with temperature

        2. MATERIAL CLASSES:
           - AB5 type (LaNi5): 1.4 wt%, low pressure (1-10 bar), fast kinetics
           - AB2 type (TiFe, ZrMn2): 1.5-1.8 wt%, moderate pressure, low cost
           - AB type (MgH2): 7.6 wt% (theoretical), high temperature (300 C), slow kinetics
           - Complex hydrides (NaAlH4): 5.6 wt%, irreversible without catalyst, R&D phase
           - Borohydrides (LiBH4): 18 wt% (theoretical), >400 C desorption, impractical

        3. LANI5 (PROTOTYPICAL EXAMPLE):
           - Capacity: 1.37 wt% (LaNi5H6 stoichiometry)
           - Equilibrium pressure: 2 bar at 25 degrees C (ideal for low-pressure systems)
           - Kinetics: fast (seconds to minutes for full charge/discharge)
           - Cycle life: 10,000+ cycles with minimal degradation
           - Cost: $100-200/kg (lanthanum, nickel commodity price sensitive)

        4. ADVANTAGES:
           - Safety: stores H2 at low pressure (1-30 bar vs 700 bar compressed)
           - Compactness: volumetric density competitive with 350 bar (100+ kg H2/m3)
           - Purity: releases high-purity H2 (no contamination)
           - Heat management: exothermic absorption can be utilized (CHP)

        5. DISADVANTAGES:
           - Gravimetric capacity: 1-2 wt% typical (vs 5.5 wt% for Type IV tanks)
           - Weight: 50-100 kg of metal per kg H2 stored (heavy systems)
           - Cost: specialized alloys expensive (La, Ni, Ti, Zr)
           - Heat management: must remove heat during absorption, add heat for desorption
           - Kinetics: slow for high-capacity materials (MgH2 requires 250-350 C)

        6. THERMAL MANAGEMENT:
           - Absorption: -25 to -40 kJ/mol H2 heat released (cool hydride bed)
           - Desorption: heat input required (waste heat recovery, electric heater)
           - Heat exchanger: integral to hydride bed design (tubes, fins)
           - Insulation: for hot hydrides (Mg-based) to maintain operating temperature

        7. APPLICATIONS:
           - Forklift fuel cells: Plug Power, Ballard (low pressure, safety)
           - Stationary storage: grid-scale H2 buffer (MW-scale demonstrations)
           - Portable power: military, remote sensors (compact, safe)
           - Heat storage: thermochemical energy storage (absorb at night, release heat on demand)
           - NOT suitable: light-duty vehicles (weight penalty unacceptable)

        8. DOE TECHNICAL TARGETS (2025):
           - Gravimetric: 5.5 wt% (system level, including tank + BoP)
           - Volumetric: 40 g H2/L (system level)
           - Cost: $10/kWh (hydrogen storage system)
           - Cycle life: 1,500 cycles (vehicle lifetime)
           - Status: No metal hydride meets all targets simultaneously (trade-offs persist)

        9. RESEARCH DIRECTIONS:
           - Destabilized hydrides: MgH2 + additives (lower desorption temp)
           - Nanostructuring: smaller particles improve kinetics
           - Catalysts: Ni, Pd, Ti to enhance reaction rates
           - Complex hydrides: NaAlH4 with TiCl3 catalyst (reversible at 150 C)
           - Ammonia borane: 19 wt% H2, but irreversible (single-use)

        10. COMMERCIAL STATUS:
            - Niche applications only: forklifts (Plug Power), stationary (HyCube)
            - Not competitive with 700 bar for vehicles (weight, cost)
            - May resurface for aviation (volumetric density favored over gravimetric)
            - Low-pressure safety advantage for public acceptance (fueling stations)
        """,
        key_factors=[
            "LaNi5: 1.4 wt%, 2 bar equilibrium, fast kinetics, 10,000+ cycles",
            "MgH2: 7.6 wt%, requires 250-350 C, slow kinetics",
            "Volumetric density competitive (100+ kg H2/m3)",
            "Gravimetric density poor (1-2 wt% typical vs 5.5% target)",
            "Low-pressure storage (1-30 bar) safer than 700 bar",
            "Heat management critical (exothermic absorption, endothermic release)",
            "DOE targets: 5.5 wt%, 40 g/L, $10/kWh (not met by any material)",
            "Applications: forklifts, stationary, NOT vehicles"
        ],
        primary_authority=[
            "DOE Hydrogen Storage Technical Targets 2025",
            "Sandia National Labs Metal Hydride Database",
            "Journal of Alloys and Compounds (extensive hydride literature)",
            "IEA Hydrogen TCP Task 32: Hydrogen-Based Energy Storage"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Hydrogen Fuel Quality per ISO 14687 and SAE J2719",
        keywords=["fuel quality", "purity", "contaminants", "ISO 14687", "SAE J2719", "PEM", "impurities"],
        conclusion_template="Hydrogen fuel per ISO 14687 Grade D requires H2 purity >{purity}% with <{co} ppm CO, <{h2o} ppm H2O. Critical for PEM fuel cell lifetime.",
        reasoning_framework="""
        Hydrogen fuel quality specifications and contamination impacts:

        1. ISO 14687 GRADE D (PEM FUEL CELLS):
           - H2 purity: 99.97% minimum (Grade D for road vehicles)
           - Total hydrocarbons: <2 ppm (C1 equivalent, methane basis)
           - CO: <0.2 ppm (critical, poisons Pt catalyst)
           - CO2: <2 ppm (forms carbonate in MEA)
           - H2O: <5 ppm (excess water floods cathode)
           - Total sulfur: <0.004 ppm (permanent Pt poisoning)
           - Formaldehyde (HCHO): <0.01 ppm
           - Formic acid (HCOOH): <0.2 ppm
           - Ammonia (NH3): <0.1 ppm
           - Total halogenates: <0.05 ppm (Cl, Br, I)
           - Particulates: <1 mg/kg (filters required)

        2. SAE J2719 (US STANDARD, HARMONIZED WITH ISO):
           - Essentially identical to ISO 14687 Grade D
           - Adds O2 limit: <5 ppm (safety, not performance)
           - Adds N2 + Ar: <100 ppm (inert diluents)
           - He: no limit (inert, used as tracer in some systems)

        3. CO POISONING MECHANISM:
           - CO adsorbs strongly on Pt catalyst surface
           - Blocks H2 adsorption sites (reversible but severe)
           - Threshold: >10 ppm causes >50% power loss
           - ISO limit <0.2 ppm ensures <5% degradation
           - Air bleed: small air injection at anode can oxidize CO (emergency measure)

        4. SULFUR POISONING:
           - H2S, COS, SO2: all poison Pt irreversibly
           - Even 0.01 ppm over hours causes permanent degradation
           - Mechanism: Pt-S bond formation (stronger than Pt-H)
           - ISO limit <0.004 ppm total sulfur (stringent)
           - Source: SMR if desulfurization inadequate, pipeline contamination

        5. WATER VAPOR:
           - Excess water: cathode flooding (liquid water blocks gas diffusion)
           - Insufficient water: membrane drying (loss of conductivity)
           - ISO limit <5 ppm ensures no liquid water in tank/lines
           - MEA operates at 40-100% RH (humidification managed by fuel cell system)

        6. PARTICULATES:
           - Sources: compressor wear, pipeline rust, valve particles
           - Impact: clog GDL pores, scratch membrane, block flow channels
           - ISO limit <1 mg/kg (filtration to <5 microns required)
           - Filters: inline at fueling nozzle and vehicle inlet

        7. PRODUCTION PURITY:
           - Electrolysis: naturally high purity (99.9%+), minimal treatment
           - SMR with PSA: 99.95-99.99% achievable (PSA very effective)
           - SMR with membrane: 99.99%+ but higher cost
           - Contamination risk: downstream of production (storage, transport, dispensing)

        8. QUALITY ASSURANCE:
           - Sampling: at production, at fueling station (monthly testing)
           - Analysis: gas chromatography (GC), mass spectrometry (MS), electrochemical sensors
           - Certification: third-party labs (Air Liquide, Linde, Bureau Veritas)
           - Traceability: batch numbers, certificates of analysis

        9. IMPACT ON FUEL CELL:
           - CO <0.2 ppm: <5% power loss (acceptable)
           - CO 1 ppm: 20-30% power loss (unacceptable)
           - H2S 0.01 ppm: 10% voltage loss in 1,000 hours (permanent)
           - Particulates: gradual pressure drop, eventual cell failure

        10. COST OF PURIFICATION:
            - PSA (pressure swing adsorption): $0.10-0.30/kg H2 (SMR purification)
            - Additional drying: $0.05-0.15/kg (desiccant or membrane)
            - Filtration: <$0.05/kg (replaceable cartridges)
            - Total: $0.20-0.50/kg added to production cost for high purity
        """,
        key_factors=[
            "ISO 14687 Grade D: 99.97% H2 minimum for PEM FCEVs",
            "CO <0.2 ppm (poisons Pt catalyst at >10 ppm)",
            "Total sulfur <0.004 ppm (irreversible Pt poisoning)",
            "H2O <5 ppm (prevents cathode flooding)",
            "Particulates <1 mg/kg (requires filtration)",
            "Electrolysis naturally high purity (99.9%+)",
            "SMR requires PSA purification (adds $0.20-0.50/kg)",
            "Quality testing monthly at fueling stations"
        ],
        primary_authority=[
            "ISO 14687:2019 Hydrogen fuel quality — Product specification",
            "SAE J2719: Hydrogen Fuel Quality for Fuel Cell Vehicles",
            "CGA G-5.3: Commodity Specification for Hydrogen",
            "DOE Hydrogen Quality Guidelines for Fuel Cell Vehicles"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

]

# Expand to 25+ doctrines by adding more blocks for:
# - Hydrogen liquefaction thermodynamics
# - Fuel cell stack thermal management
# - Hydrogen in steel/iron metallurgy (direct reduced iron)
# - Hydrogen aviation (liquid vs compressed)
# - Power-to-X (hydrogen to ammonia, methanol, e-fuels)
# - Hydrogen codes (IFC, IMC, IRC)
# - Electrolyzer water quality requirements
# - Hydrogen compression technologies (mechanical, ionic, electrochemical)
# ... (10+ more doctrines to complete the cache)

# ═══════════════════════════════════════════════════════════════════════════
# TELEMETRY & METRICS
# ═══════════════════════════════════════════════════════════════════════════

class Telemetry:
    """Query telemetry and performance tracking."""

    def __init__(self):
        self.queries_total = 0
        self.queries_by_mode: Dict[str, int] = defaultdict(int)
        self.queries_by_zone: Dict[str, int] = defaultdict(int)
        self.latencies: List[float] = []
        self.cache_hits = 0
        self.cache_misses = 0
        self.triggered_doctrines: List[str] = []
        self.start_time = datetime.now()

    def record_query(
        self,
        mode: ResponseMode,
        zone: AnalysisZone,
        latency_ms: float,
        cache_hit: bool,
        doctrines: List[str]
    ):
        """Record query metrics."""
        self.queries_total += 1
        self.queries_by_mode[mode.value] += 1
        self.queries_by_zone[zone.value] += 1
        self.latencies.append(latency_ms)
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        self.triggered_doctrines.extend(doctrines)

    def get_stats(self) -> Dict[str, Any]:
        """Get telemetry statistics."""
        uptime = (datetime.now() - self.start_time).total_seconds()
        return {
            "queries_total": self.queries_total,
            "queries_by_mode": dict(self.queries_by_mode),
            "queries_by_zone": dict(self.queries_by_zone),
            "avg_latency_ms": sum(self.latencies) / len(self.latencies) if self.latencies else 0.0,
            "cache_hit_rate": self.cache_hits / max(1, self.queries_total),
            "uptime_seconds": uptime,
            "most_triggered_doctrines": Counter(self.triggered_doctrines).most_common(10)
        }

# Global telemetry instance
telemetry = Telemetry()

# ═══════════════════════════════════════════════════════════════════════════
# CORE ENGINE LOGIC
# ═══════════════════════════════════════════════════════════════════════════

class ENRG07HydrogenEngine:
    """Hydrogen Energy Systems Intelligence Engine."""

    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.telemetry = telemetry
        logger.info(f"ENRG07 Hydrogen Engine initialized with {len(self.doctrines)} doctrine blocks")

    def semantic_normalize(self, text: str) -> str:
        """Normalize hydrogen energy terminology."""
        text = text.lower()

        # Normalize hydrogen color variations
        text = re.sub(r'\brenewable\s+hydrogen\b', 'green hydrogen', text)
        text = re.sub(r'\bsmr\s+with\s+ccs\b', 'blue hydrogen', text)
        text = re.sub(r'\bsmr\s+without\s+ccs\b', 'gray hydrogen', text)

        # Normalize fuel cell types
        text = re.sub(r'\bproton\s+exchange\s+membrane\b', 'PEM', text)
        text = re.sub(r'\bsolid\s+oxide\b', 'SOFC', text)

        # Normalize storage
        text = re.sub(r'\b700\s*bar\b', '700 bar', text)
        text = re.sub(r'\b350\s*bar\b', '350 bar', text)
        text = re.sub(r'\bliquid\s+hydrogen\b', 'LH2', text)

        # Normalize units
        text = re.sub(r'\bkwh/kg\b', 'kWh/kg', text)
        text = re.sub(r'\bmpa\b', 'bar', text)  # 1 MPa = 10 bar

        return text

    def match_doctrines(self, question: str) -> List[DoctrineBlock]:
        """Match question to relevant doctrine blocks."""
        question_norm = self.semantic_normalize(question)
        question_words = set(question_norm.split())

        matches = []
        for doctrine in self.doctrines:
            # Check keyword overlap
            doctrine_keywords = set(kw.lower() for kw in doctrine.keywords)
            overlap = len(question_words & doctrine_keywords)

            # Check topic relevance
            topic_words = set(doctrine.topic.lower().split())
            topic_overlap = len(question_words & topic_words)

            score = overlap + (topic_overlap * 2)  # Weight topic higher

            if score > 0:
                matches.append((score, doctrine))

        # Sort by relevance score and return top matches
        matches.sort(reverse=True, key=lambda x: x[0])
        return [d for _, d in matches[:5]]  # Top 5 doctrines

    def three_layer_response(
        self,
        question: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Tuple[str, List[DoctrineBlock], float]:
        """
        Three-layer response architecture:
        1. Doctrine cache (0-200ms)
        2. Semantic retrieval (200-1000ms)
        3. Deep analysis (>1000ms, not implemented - would hit vector DB)
        """
        start = datetime.now()

        # Layer 1: Doctrine cache
        matched = self.match_doctrines(question)

        if matched:
            # Cache hit
            latency = (datetime.now() - start).total_seconds() * 1000
            return self.build_response(question, matched, mode, zone), matched, latency
        else:
            # Cache miss - would normally go to vector search
            # For now, return general response
            latency = (datetime.now() - start).total_seconds() * 1000
            general = "No specific doctrine matched. General hydrogen energy principles apply."
            return general, [], latency

    def build_response(
        self,
        question: str,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> str:
        """Build response based on mode and zone."""

        if mode == ResponseMode.FAST:
            # Concise response
            if doctrines:
                primary = doctrines[0]
                return f"{primary.conclusion_template}\n\nKey factors: {', '.join(primary.key_factors[:3])}"
            return "Insufficient doctrine match for FAST response."

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready response with citations
            parts = []
            for doctrine in doctrines:
                parts.append(f"## {doctrine.topic}\n")
                parts.append(f"{doctrine.conclusion_template}\n")
                parts.append(f"**Authorities:** {'; '.join(doctrine.primary_authority)}\n")
                parts.append(f"**Confidence:** {doctrine.confidence.value}\n")
            return "\n".join(parts)

        elif mode == ResponseMode.MEMO:
            # Full documentation
            parts = []
            for doctrine in doctrines:
                parts.append(f"# {doctrine.topic}\n")
                parts.append(f"## Conclusion\n{doctrine.conclusion_template}\n")
                parts.append(f"## Reasoning Framework\n{doctrine.reasoning_framework}\n")
                parts.append(f"## Key Factors\n" + "\n".join(f"- {f}" for f in doctrine.key_factors))
                parts.append(f"\n## Authorities\n" + "\n".join(f"- {a}" for a in doctrine.primary_authority))
                parts.append(f"\n**Confidence Level:** {doctrine.confidence.value}")
                if doctrine.confidence_stratification:
                    parts.append(f"\n**Confidence Rationale:** {doctrine.confidence_stratification}\n")
            return "\n\n".join(parts)

        return "Invalid response mode."

    def calculate_fragility_score(self, doctrines: List[DoctrineBlock]) -> float:
        """
        Calculate fact fragility score (0.0-1.0).
        Higher score = more fragile (uncertain, recharacterization risk).
        """
        if not doctrines:
            return 1.0  # Maximum fragility if no doctrine support

        # Average confidence levels
        confidence_map = {
            ConfidenceLevel.DEFENSIBLE: 0.1,
            ConfidenceLevel.AGGRESSIVE: 0.4,
            ConfidenceLevel.DISCLOSURE: 0.6,
            ConfidenceLevel.HIGH_RISK: 0.9
        }

        scores = [confidence_map.get(d.confidence, 0.5) for d in doctrines]
        return sum(scores) / len(scores)

    def apply_epistemic_guardrails(self, response: str) -> Tuple[str, List[str]]:
        """
        Apply epistemic guardrails - remove banned phrases, add caveats.
        Returns (cleaned_response, caveats_list).
        """
        caveats = []
        cleaned = response

        # Remove banned phrases
        for phrase in BANNED_PHRASES:
            if phrase in cleaned.lower():
                cleaned = re.sub(re.escape(phrase), "", cleaned, flags=re.IGNORECASE)
                caveats.append(f"Removed inappropriate disclaimer: '{phrase}'")

        # Add zone-appropriate caveats
        caveats.append("Analysis based on current hydrogen energy standards and engineering data.")
        caveats.append("Technology and costs evolving rapidly - verify current market data.")

        return cleaned.strip(), caveats

    def determinism_hash(self, question: str, doctrines: List[DoctrineBlock]) -> str:
        """Generate SHA-256 hash for reproducibility."""
        content = question + "".join(d.topic for d in doctrines)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    async def query(self, request: QueryRequest) -> AnalysisResponse:
        """Main query endpoint."""
        start = datetime.now()

        # Three-layer response
        answer, doctrines, cache_latency = self.three_layer_response(
            request.question,
            request.mode,
            request.zone
        )

        # Apply epistemic guardrails
        answer_clean, caveats = self.apply_epistemic_guardrails(answer)

        # Build reasoning chain
        reasoning_chain = [d.topic for d in doctrines]

        # Collect authorities
        authorities = []
        for d in doctrines:
            authorities.extend(d.primary_authority)
        authorities = list(set(authorities))  # Deduplicate

        # Calculate fragility
        fragility = self.calculate_fragility_score(doctrines)

        # Determine confidence
        if doctrines:
            confidence = doctrines[0].confidence
        else:
            confidence = ConfidenceLevel.HIGH_RISK

        # Determinism hash
        det_hash = self.determinism_hash(request.question, doctrines)

        # Total latency
        latency = (datetime.now() - start).total_seconds() * 1000

        # Record telemetry
        self.telemetry.record_query(
            request.mode,
            request.zone,
            latency,
            cache_hit=len(doctrines) > 0,
            doctrines=[d.topic for d in doctrines]
        )

        # Audit log
        self._audit_log(request, det_hash, latency)

        return AnalysisResponse(
            answer=answer_clean,
            confidence=confidence,
            triggered_doctrines=[d.topic for d in doctrines],
            reasoning_chain=reasoning_chain,
            authorities_cited=authorities,
            fragility_score=fragility,
            zone=request.zone,
            mode=request.mode,
            determinism_hash=det_hash,
            latency_ms=latency,
            epistemic_caveats=caveats
        )

    def _audit_log(self, request: QueryRequest, det_hash: str, latency: float):
        """Append-only audit trail."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": request.question,
            "mode": request.mode.value,
            "zone": request.zone.value,
            "determinism_hash": det_hash,
            "latency_ms": latency
        }

        with open(AUDIT_LOG_PATH, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="ENRG07 Hydrogen Energy Systems Engine",
    version=ENGINE_VERSION,
    description="TIE-grade hydrogen energy analysis: production, storage, fuel cells, infrastructure, safety"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Engine instance
engine = ENRG07HydrogenEngine()

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "engine": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "status": "operational",
        "port": str(ENGINE_PORT),
        "doctrines": str(len(DOCTRINE_CACHE))
    }

@app.post("/query", response_model=AnalysisResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint."""
    try:
        return await engine.query(request)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    stats = engine.telemetry.get_stats()
    return HealthResponse(
        status="healthy",
        engine=ENGINE_NAME,
        version=ENGINE_VERSION,
        port=ENGINE_PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        queries_processed=stats["queries_total"],
        avg_latency_ms=stats["avg_latency_ms"],
        cache_hit_rate=stats["cache_hit_rate"],
        uptime_seconds=stats["uptime_seconds"]
    )

@app.get("/doctrines", response_model=List[str])
async def list_doctrines():
    """List all doctrine topics."""
    return [d.topic for d in DOCTRINE_CACHE]

@app.get("/doctrine/{topic}", response_model=DoctrineBlock)
async def get_doctrine(topic: str):
    """Retrieve specific doctrine block."""
    for d in DOCTRINE_CACHE:
        if d.topic.lower() == topic.lower():
            return d
    raise HTTPException(status_code=404, detail=f"Doctrine '{topic}' not found")

@app.get("/stats", response_model=Dict[str, Any])
async def stats():
    """Telemetry statistics."""
    return engine.telemetry.get_stats()

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} hydrogen energy doctrine blocks")
    logger.info(f"Audit log: {AUDIT_LOG_PATH}")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info"
    )
