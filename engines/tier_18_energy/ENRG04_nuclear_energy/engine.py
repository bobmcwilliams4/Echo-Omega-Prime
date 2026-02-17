"""
ENRG04 - Nuclear Energy Systems Intelligence Engine
TIE Gold Standard - Nuclear Engineering Expertise

Covers: Nuclear fission, PWR/BWR design, reactor control, fuel cycles,
radiation protection, waste management, NRC regulations, SMR, fusion basics

Port: 9084
Version: 1.0.0
"""

import sys
from pathlib import Path

# CRITICAL: Set sys.path BEFORE any local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "ENRG04"
ENGINE_NAME = "Nuclear Energy Systems Intelligence Engine"
VERSION = "1.0.0"
PORT = 9084

# Configure loguru
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    f"logs/{ENGINE_ID}_{{time}}.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
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

class ReactorType(str, Enum):
    PWR = "PWR"
    BWR = "BWR"
    CANDU = "CANDU"
    RBMK = "RBMK"
    SMR = "SMR"
    FUSION = "FUSION"

class WasteCategory(str, Enum):
    HLW = "HLW"  # High-Level Waste
    TRU = "TRU"  # Transuranic
    LLW = "LLW"  # Low-Level Waste
    GTCC = "GTCC"  # Greater Than Class C

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=10000)
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = None

class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    reactor_scope: Optional[List[ReactorType]] = None
    waste_category: Optional[List[WasteCategory]] = None

class QueryResponse(BaseModel):
    query: str
    answer: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    authority_citations: List[str]
    latency_ms: float
    determinism_hash: str
    warnings: List[str] = []

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    uptime_seconds: float
    total_queries: int
    doctrine_count: int
    avg_latency_ms: float

# ============================================================================
# DOCTRINE CACHE - NUCLEAR ENERGY EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    # ========== NUCLEAR FISSION FUNDAMENTALS ==========
    DoctrineBlock(
        topic="nuclear_fission_chain_reaction",
        keywords=["fission", "chain reaction", "neutron", "uranium-235", "criticality", "k-effective"],
        conclusion_template="Nuclear fission chain reactions require achieving and maintaining criticality (k-eff = 1.0). Subcritical systems (k-eff < 1.0) decay, supercritical systems (k-eff > 1.0) escalate exponentially without control.",
        reasoning_framework="""
Nuclear fission occurs when a heavy nucleus (U-235, Pu-239) absorbs a thermal neutron and splits into two lighter fission fragments plus 2-3 prompt neutrons and energy (~200 MeV/fission).

For a self-sustaining chain reaction:
- Each fission must produce ≥1 neutron that causes another fission
- k-effective = (neutrons in generation n+1) / (neutrons in generation n)
- k-eff = 1.0 → critical (steady power)
- k-eff < 1.0 → subcritical (power decays)
- k-eff > 1.0 → supercritical (power rises)

Fast neutrons (~2 MeV) must be moderated to thermal energies (~0.025 eV) to maximize fission probability in U-235. Moderators (light water, heavy water, graphite) slow neutrons via elastic scattering without absorbing them.

Delayed neutrons (0.65% of total, half-life 0.2-56s) enable reactor control. Without them, reactor period would be milliseconds and control impossible.

Reactivity is defined as ρ = (k-eff - 1) / k-eff. Positive reactivity insertion → power increase. Negative reactivity → power decrease.
""",
        key_factors=[
            "k-effective determination (six-factor formula: η·ε·p·f·Pf·Pt)",
            "Neutron moderation and thermalization",
            "Delayed neutron fraction β (~0.0065 for U-235)",
            "Prompt neutron lifetime (~10^-4 seconds in thermal reactors)",
            "Neutron cross-sections (absorption, fission, scattering)",
            "Reactor period and doubling time"
        ],
        primary_authority=[
            "Lamarsh & Baratta, Introduction to Nuclear Engineering (3rd ed.)",
            "DOE Fundamentals Handbook: Nuclear Physics and Reactor Theory",
            "Glasstone & Sesonske, Nuclear Reactor Engineering (4th ed.)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR, ReactorType.BWR, ReactorType.CANDU]
    ),

    DoctrineBlock(
        topic="neutron_moderation_thermalization",
        keywords=["moderation", "thermalization", "moderator", "light water", "heavy water", "graphite", "slowing down"],
        conclusion_template="Neutron moderation is essential in thermal reactors to slow fast fission neutrons (~2 MeV) to thermal energies (~0.025 eV) where U-235 fission cross-section is maximum. Moderator selection balances slowing power against parasitic absorption.",
        reasoning_framework="""
Fast neutrons born from fission must lose energy to increase fission probability:
- U-235 thermal fission cross-section: ~580 barns
- U-235 fast fission cross-section: ~1.5 barns
- Factor of ~387 increase at thermal energies

Energy loss per collision:
- Hydrogen (light water): avg 50% energy loss, ξ = 1.0
- Deuterium (heavy water): avg 36% energy loss, ξ = 0.725
- Carbon (graphite): avg 14% energy loss, ξ = 0.158

Number of collisions to thermalize from 2 MeV to 0.025 eV:
- Light water: ~18 collisions
- Heavy water: ~25 collisions
- Graphite: ~115 collisions

Moderator selection criteria:
1. High slowing power (ξΣs) → rapid thermalization
2. Low absorption cross-section → minimize parasitic losses
3. Moderation ratio (ξΣs / Σa) → efficiency metric
4. Physical/chemical stability under radiation
5. Cost and availability

Light water (H2O): Best slowing power but absorbs neutrons → requires enriched fuel
Heavy water (D2O): Low absorption → natural uranium fuel viable
Graphite: Low absorption, high temp capability → gas-cooled reactors
""",
        key_factors=[
            "Logarithmic energy decrement (ξ)",
            "Slowing-down power (ξΣs)",
            "Moderation ratio (ξΣs / Σa)",
            "Average number of collisions to thermalize",
            "Resonance escape probability",
            "Moderator temperature effects on reactivity"
        ],
        primary_authority=[
            "Duderstadt & Hamilton, Nuclear Reactor Analysis",
            "Stacey, Nuclear Reactor Physics (3rd ed.)",
            "NRC NUREG/CR-5640: Neutron Slowing Down and Thermalization"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR, ReactorType.BWR, ReactorType.CANDU]
    ),

    # ========== PWR DESIGN ==========
    DoctrineBlock(
        topic="pwr_primary_secondary_loop",
        keywords=["PWR", "pressurized water reactor", "primary loop", "secondary loop", "steam generator", "pressurizer"],
        conclusion_template="PWRs use a dual-loop system: primary loop (pressurized 15.5 MPa, 315°C) contains reactor coolant that never boils; secondary loop produces steam for turbine. This separation prevents radioactive contamination of turbine.",
        reasoning_framework="""
PWR Primary Loop (Reactor Coolant System):
- Pressure: 15.5 MPa (2250 psi) maintained by pressurizer
- Temperature: 290°C inlet → 315°C outlet (ΔT = 25°C typical)
- Coolant: Demineralized light water with boric acid (0-2000 ppm)
- Flow: 4 loops in large PWRs (Westinghouse 4-loop), 2-3 in smaller
- Components: Reactor vessel, reactor coolant pumps, steam generators, pressurizer
- Subcooled liquid throughout → no boiling in core

Pressurizer Function:
- Maintains primary system pressure via steam bubble
- Electric heaters → increase pressure
- Spray system → decrease pressure
- Surge line connects to hot leg → accommodates thermal expansion
- Safety/relief valves → overpressure protection

Steam Generator (SG):
- U-tube bundle heat exchanger
- Primary (hot) side: tube side, radioactive
- Secondary (cold) side: shell side, feedwater → steam
- Typical SG: 5000-16000 U-tubes, 15-20m tall
- Secondary steam: 6-7 MPa, ~280°C, ~15% moisture

Secondary Loop:
- Receives heat from SG, produces steam
- Steam drives turbine → generator → electricity
- Condenser: steam → water via cooling water (ocean, river, cooling tower)
- Feedwater pumps return condensate to SG
- Non-radioactive → allows turbine maintenance without rad exposure

Advantage: Radioactivity contained in primary loop. Disadvantage: Lower thermal efficiency (~33%) due to extra heat exchange step.
""",
        key_factors=[
            "Primary loop pressure maintenance",
            "Pressurizer heater and spray control",
            "Steam generator U-tube integrity (SG tube rupture risk)",
            "Secondary side chemistry (AVT, phosphate)",
            "Primary side boron concentration for reactivity control",
            "Reactor coolant pump seal integrity"
        ],
        primary_authority=[
            "Todreas & Kazimi, Nuclear Systems Vol. I",
            "Westinghouse Technology Manual: PWR Systems",
            "NRC Standard Review Plan NUREG-0800 Chapter 5: Reactor Coolant System"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR]
    ),

    DoctrineBlock(
        topic="pwr_reactivity_control_boron_rods",
        keywords=["reactivity control", "control rods", "boron", "chemical shim", "rod cluster control assembly", "RCCA"],
        conclusion_template="PWR reactivity control combines chemical shim (soluble boron in coolant) for long-term compensation of fuel burnup and control rods (Ag-In-Cd or B4C) for load-following and shutdown. Boron provides large negative reactivity without spatial flux distortion.",
        reasoning_framework="""
Chemical Shim (Soluble Boron):
- Boric acid (H3BO3) dissolved in primary coolant
- Concentration range: 0-2000 ppm boron
- B-10 isotope: 3835 barn thermal absorption cross-section
- Advantages: Uniform negative reactivity, no flux peaking, large worth
- Disadvantages: Slow response (hours via dilution/boration), positive moderator temp coefficient at high conc
- Used for: Compensating fuel burnup over cycle, xenon override, cold shutdown margin

Control Rod Clusters (RCCA - Rod Cluster Control Assembly):
- Composition: Ag-In-Cd (80-15-5) or B4C in stainless steel tubes
- Configuration: 20-24 rods per cluster, inserted from top
- Control banks: Multiple clusters moved together (A, B, C, D banks)
- Insertion depth: 0% (fully withdrawn) to 100% (fully inserted)
- Worth: ~10-20% Δk/k for all rods
- Advantages: Fast response (seconds), precise control
- Disadvantages: Local flux peaking, limited worth per bank

Reactivity Control Strategy:
1. Beginning of Cycle (BOC): High boron (1500-2000 ppm), rods mostly withdrawn
2. During Cycle: Gradually reduce boron as fuel depletes, maintain rods in optimal position
3. Load Following: Move control rods, maintain boron constant
4. Xenon Override: Rods or boron to counter Xe-135 buildup after power reduction
5. End of Cycle (EOC): Low boron (0-50 ppm), rods deeper insertion
6. Shutdown: Trip rods (full insertion) + borate to cold shutdown boron conc

Rod Insertion Limits:
- Avoid excessive insertion during power operation → local power peaking
- Insertion limits defined in Technical Specifications per power level
- Flux maps verify peaking factors within limits
""",
        key_factors=[
            "Boron reactivity worth curve (ppm to pcm conversion)",
            "Control rod worth and differential worth",
            "Shutdown margin (k-eff ≤ 0.95 with limiting rod stuck out)",
            "Moderator temperature coefficient (MTC) dependency on boron",
            "Rod ejection accident analysis",
            "Boron dilution accident prevention"
        ],
        primary_authority=[
            "NRC Regulatory Guide 1.68: Initial Test Programs for PWRs",
            "ANSI/ANS-19.6.1: Reload Startup Physics Tests",
            "Westinghouse WCAP-9272-P: Reload Safety Evaluation Methodology"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR]
    ),

    # ========== BWR DESIGN ==========
    DoctrineBlock(
        topic="bwr_direct_cycle_design",
        keywords=["BWR", "boiling water reactor", "direct cycle", "steam separator", "steam dryer", "jet pump"],
        conclusion_template="BWRs use a direct cycle where coolant boils in the reactor core and steam flows directly to the turbine. This eliminates steam generators but makes turbine radioactive. Void fraction in core provides strong negative reactivity feedback.",
        reasoning_framework="""
BWR Direct Cycle Characteristics:
- Single loop: reactor → turbine → condenser → feedwater → reactor
- Pressure: 7.0 MPa (1000 psi) in reactor vessel
- Temperature: 278°C saturation, ~13% steam quality at core exit
- Coolant boils in upper 2/3 of core → two-phase flow
- Steam separators and dryers remove moisture before turbine
- Turbine and condenser become radioactive (N-16, short half-life)

Core Power Distribution:
- Axial: Bottom-peaked due to void formation at top
- Radial: Controlled by control rod pattern and flow distribution
- Void coefficient: Highly negative (-10 to -50 pcm/%void)
- Power-to-flow ratio determines void fraction

Steam Separation System:
1. Steam separators (centrifugal): Remove bulk water from steam
2. Steam dryers (chevron type): Remove moisture to <0.1% quality
3. Separated water returns to downcomer (recirculation)

Recirculation System:
- Jet pumps: Use high-pressure steam to drive recirculation flow
- Core flow control: Variable recirculation flow → power control
- Increase flow → less voiding → higher power
- Decrease flow → more voiding → lower power
- Natural circulation capable at ~30% power without pumps

Advantages:
- Higher thermal efficiency (~34%) due to single cycle
- Simpler system, no steam generators
- Strong negative void feedback → inherent stability

Disadvantages:
- Turbine radioactive → more complex maintenance
- Potential for recirculation pump failures
- Flow instabilities (density wave oscillations) at low flow
""",
        key_factors=[
            "Void fraction distribution (axial and radial)",
            "Void reactivity coefficient",
            "Critical power ratio (CPR) for boiling crisis prevention",
            "Recirculation flow rate and core power relationship",
            "Steam quality at core exit",
            "Moisture carryover limits (turbine blade erosion)"
        ],
        primary_authority=[
            "GE BWR/4 Technology Manual",
            "NRC NUREG-0800 Chapter 4.4: Thermal-Hydraulic Design",
            "ANSI/ANS-19.1: BWR Reload Fuel Safety Evaluation"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.BWR]
    ),

    DoctrineBlock(
        topic="bwr_control_rods_cruciform",
        keywords=["BWR control rods", "cruciform", "bottom entry", "control rod drive", "CRD", "fine motion control"],
        conclusion_template="BWR control rods insert from bottom using cruciform geometry (cross-shaped) containing B4C poison. Bottom entry allows refueling without removing rods and provides scram via gravity assist. Control Rod Drive (CRD) hydraulic system enables fine motion control.",
        reasoning_framework="""
BWR Control Rod Design:
- Geometry: Cruciform (4 blades in cross pattern)
- Material: B4C powder in stainless steel tubes
- Position: Insert between 4 fuel assemblies
- Entry: Bottom of core (vs top in PWR)
- Pattern: Checkerboard arrangement for uniform flux

Control Rod Drive (CRD) Mechanism:
- Hydraulic system using reactor water
- Fine Motion Control Rod Drive (FMCRD): 3-inch incremental steps
- Locking piston: Holds rod position
- Drive water: High-pressure injection to move rod
- Exhaust water: Vent to lower pressure
- Notch positions: Typically 48 notches from fully inserted to withdrawn

Rod Movement Sequences:
1. Insert (Negative Reactivity): Drive water pressure → piston up → rod in
2. Withdraw (Positive Reactivity): Exhaust water → piston down → rod out
3. Scram: All CRD accumulators fire → rods insert via hydraulic and gravity in <3 seconds

Control Rod Patterns:
- Deep rods: Near center, high worth
- Shallow rods: Near periphery, lower worth
- Sequence: Carefully planned to avoid local power peaking
- Power shaping: Control rod pattern defines radial flux distribution

BWR Reactivity Control Strategy:
- No soluble boron (unlike PWR)
- Control rods only mechanism for reactivity control
- Power maneuvering: Rod patterns and recirculation flow
- Shutdown margin: Subset of rods sufficient for k-eff < 0.95
- Standby Liquid Control System (SLCS): Backup boron injection for shutdown

Advantages:
- Refueling: Top head removal accesses fuel without removing rods
- Scram: Gravity-assisted insertion (more reliable)
- Maintenance: CRD accessible from below during operation

Disadvantages:
- Complex CRD hydraulic system (leak potential)
- Bottom entry → penetrations in vessel bottom (integrity concern)
- Seals must prevent coolant leakage
""",
        key_factors=[
            "Control rod worth and pattern optimization",
            "CRD insertion time (scram analysis)",
            "Hydraulic control unit (HCU) operability",
            "Rod sequence exchange limits",
            "Standby Liquid Control System flow rate",
            "Control rod density (rods per fuel assembly)"
        ],
        primary_authority=[
            "GE Service Information Letter 409: Control Rod Drive System",
            "NRC Regulatory Guide 1.77: BWR Control Rod System Assumptions",
            "NUREG-1434: BWR Technical Specifications"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.BWR]
    ),

    # ========== REACTOR FUEL ==========
    DoctrineBlock(
        topic="nuclear_fuel_uo2_zircaloy",
        keywords=["UO2", "uranium dioxide", "fuel pellet", "zircaloy", "cladding", "fuel rod", "enrichment"],
        conclusion_template="Commercial reactor fuel consists of UO2 ceramic pellets (3-5% U-235 enrichment) stacked in zircaloy cladding tubes. Fuel design must accommodate fission gas release, pellet swelling, cladding creep, and prevent cladding breach under all operating conditions.",
        reasoning_framework="""
Fuel Pellet Design:
- Material: Uranium dioxide (UO2) ceramic
- Enrichment: 3-5% U-235 (PWR/BWR), 0.7% (CANDU natural), 19.75% max (SMR)
- Dimensions: ~8-10 mm diameter, ~10-15 mm height
- Density: 95-96% theoretical density (10.96 g/cm³)
- Dish/chamfer: End dishes for thermal expansion accommodation
- Grain size: 8-12 μm for fission gas retention

Cladding Material:
- Zircaloy-2 (BWR): Zr + 1.5% Sn + 0.1% Fe + 0.05% Ni
- Zircaloy-4 (PWR): Zr + 1.5% Sn + 0.2% Fe + 0.1% Cr (no Ni)
- Optimized ZIRLOTM, M5™: Advanced alloys with better corrosion resistance
- Wall thickness: 0.5-0.7 mm
- Purpose: Contain fission products, provide structural support, low neutron absorption

Fuel Rod Assembly:
- Rod length: 3.6-4.5 m (PWR/BWR)
- Pellet stack height: Slightly less than rod length → plenum for gas
- Fill gas: Helium at ~2-3 MPa (improves heat transfer)
- Plenum volume: Upper ~10-15 cm for fission gas accumulation
- Spring: Holds pellet stack, accommodates irradiation growth
- End plugs: Welded caps, hermetic seal

Fuel Assembly Configuration:
- PWR: 17×17 array (264 rods), 24 guide tubes, 1 instrumentation tube
- BWR: 8×8, 9×9, 10×10 arrays, partial length rods, water rods
- Grid spacers: Every 40-50 cm to prevent rod vibration
- Nozzles: Top and bottom, handling and coolant distribution

Fuel Performance Limits:
1. Clad stress: Hoop stress from internal gas pressure < yield strength
2. Clad corrosion: Oxide layer < 100 μm (hydrogen pickup concern)
3. Clad hydriding: Hydrogen content < 600 ppm (embrittlement)
4. Pellet-clad interaction (PCI): Avoid stress corrosion cracking during power ramps
5. Departure from Nucleate Boiling (DNB): Maintain nucleate boiling (no film boiling)
6. Burnup limit: 62 GWd/MTU (current regulatory limit)

In-Pile Behavior:
- Fission gas release: Xe, Kr gases accumulate in plenum and grain boundaries
- Pellet swelling: ~1% volume increase per 10 GWd/MTU
- Densification: Initial ~1% shrinkage in first few days
- Clad creep-down: External pressure compresses clad onto pellet
- Pellet-clad gap: Closes over time → improves heat transfer
""",
        key_factors=[
            "Enrichment level and isotopic composition (U-235, U-238, Pu-239 buildup)",
            "Burnup (GWd/MTU or MWd/kgU)",
            "Fission gas release fraction",
            "Linear heat generation rate (LHGR, kW/m)",
            "Fuel centerline temperature (< 2800°C UO2 melting point)",
            "Cladding corrosion and oxide thickness"
        ],
        primary_authority=[
            "NRC NUREG/CR-7024: Fuel Performance Code FRAPCON-4.0",
            "IAEA TECDOC-1233: Fuel Modelling in Accident Conditions",
            "Olander, Fundamental Aspects of Nuclear Reactor Fuel Elements"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR, ReactorType.BWR]
    ),

    DoctrineBlock(
        topic="fuel_burnup_depletion",
        keywords=["burnup", "fuel depletion", "fissile inventory", "plutonium buildup", "discharge burnup", "cycle length"],
        conclusion_template="Fuel burnup measures energy extracted per unit mass of fuel (GWd/MTU). As U-235 depletes, Pu-239 breeds from U-238 and becomes major fissile contributor. Modern fuel reaches 45-62 GWd/MTU discharge burnup over 4-6 year residence.",
        reasoning_framework="""
Burnup Definition:
- Units: GWd/MTU (gigawatt-days per metric ton uranium) or MWd/kgU
- Typical discharge: 45-62 GWd/MTU (PWR/BWR), 7-10 GWd/MTU (CANDU)
- Peak pin: ~10-15% higher than assembly average

Fissile Isotope Evolution:
Initial (BOL - Beginning of Life):
- U-235: 3-5% (enriched fuel)
- U-238: 95-97%
- Pu-239: 0%

After 1 Cycle (~18 GWd/MTU):
- U-235: ~2.5% (depleted ~30%)
- Pu-239: ~0.5% (bred from U-238)
- Pu-241: ~0.1%
- Other actinides: ~0.2%

End of Life (EOL - 50 GWd/MTU):
- U-235: ~0.8% (depleted ~75%)
- Pu-239: ~0.5-0.6%
- Total Pu: ~1.0%
- Fission products: ~5%
- Energy from Pu fission: ~40-50% of total

Plutonium Breeding:
- U-238 + n → U-239 → Np-239 → Pu-239 (β-decay, 23 min + 2.3 days)
- Pu-239 fission cross-section: ~750 barns (thermal) vs U-235 ~580 barns
- Pu-239 absorbs neutron → Pu-240 → Pu-241 (fissile) → Pu-242
- Buildup rate: ~1 kg Pu per MTU per 10 GWd/MTU

Reactivity Depletion:
- BOL: Maximum k-eff (excess reactivity compensated by boron/rods)
- Midlife: Equilibrium reactivity (Pu buildup partially offsets U-235 depletion)
- EOL: Minimum k-eff (insufficient fissile, reload required)
- Cycle length: 12-24 months between refuelings

Refueling Strategy:
- Batch fraction: 1/3 or 1/4 core reloaded per cycle
- Shuffle: Move partially burned assemblies to higher flux regions
- Fresh fuel: Place in low flux periphery initially
- Residence time: 3-6 years total (multiple cycles)

Burnup Limits:
- Regulatory: 62 GWd/MTU current limit (under review for increase)
- Technical: Cladding integrity, fission gas release, clad oxide thickness
- Economic: Diminishing returns beyond ~50-55 GWd/MTU
""",
        key_factors=[
            "Assembly-average vs peak-pin burnup",
            "Fissile inventory (U-235 + Pu-239 + Pu-241)",
            "Conversion ratio (Pu bred per U-235 consumed)",
            "Burnable absorbers (Gd2O3, IFBA) for reactivity control",
            "Cycle length economics (capacity factor vs fuel cost)",
            "High-burnup fuel structural integrity"
        ],
        primary_authority=[
            "NRC NUREG/CR-6534: Extended Burnup Fuel Behavior",
            "EPRI TR-1025871: High Burnup Fuel Experience",
            "IAEA Nuclear Energy Series NF-T-3.8: Spent Fuel Performance"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR, ReactorType.BWR]
    ),

    # ========== REACTOR KINETICS ==========
    DoctrineBlock(
        topic="delayed_neutrons_reactor_period",
        keywords=["delayed neutrons", "prompt neutrons", "precursor", "reactor period", "prompt critical", "dollar", "beta"],
        conclusion_template="Delayed neutrons (0.65% of total, 0.2-56s half-lives) make reactor control possible by extending effective neutron generation time from ~10^-4 to ~0.1 seconds. One dollar reactivity ($1.00 = β) brings reactor to prompt critical; exceeding one dollar causes exponential power rise uncontrollable by rods.",
        reasoning_framework="""
Neutron Populations:
- Prompt neutrons: 99.35%, released instantly (<10^-14 s) from fission
- Delayed neutrons: 0.65%, released from fission product decay (0.2-56 s)
- Delayed neutron fraction β: 0.0065 for U-235, 0.0021 for Pu-239

Six Delayed Neutron Groups (U-235):
| Group | Fraction | Half-life (s) | Precursor |
|-------|----------|---------------|-----------|
| 1     | 0.000215 | 55.72         | Br-87     |
| 2     | 0.001424 | 22.72         | I-137     |
| 3     | 0.001274 | 6.22          | various   |
| 4     | 0.002568 | 2.30          | various   |
| 5     | 0.000748 | 0.61          | various   |
| 6     | 0.000273 | 0.23          | various   |

Reactor Kinetics Equation:
- Without delayed neutrons: T = ℓ / ρ (period ~ 10^-4 / reactivity)
- With delayed neutrons: T ≈ ℓ / (ρ - β) when ρ < β
- Effective generation time Λ ≈ ℓ / (1 - β) ≈ 10^-1 seconds

Reactivity Units:
- Absolute reactivity ρ = (k - 1) / k
- Dollars: reactivity / β (normalized to delayed neutron fraction)
- Cents: 1 cent = β/100 = 6.5 pcm (for β = 0.0065)
- $1.00 = prompt critical threshold

Reactor States:
1. Subcritical (ρ < 0): Power decreases exponentially
2. Critical (ρ = 0): Steady power
3. Supercritical (0 < ρ < β): Delayed critical, controllable rise
4. Prompt supercritical (ρ > β): Exponential rise, control rods too slow

Power Response:
- Small reactivity insertion (ρ << β): Period T = Λ / ρ ≈ 80 s / ρ(dollars)
- 10¢ insertion → 80s period → e-folding time 80s (power doubles ~55s)
- 50¢ insertion → 16s period → power doubles ~11s
- $1.05 insertion → prompt critical → millisecond doubling (catastrophic)

Control Strategy:
- Normal operation: Reactivity changes < 50¢ (slow, controllable)
- Control rod banks: Worth limited to ~$0.50-1.00 per bank
- Total rod worth: $10-20 for full bank insertion
- Scram: Insert all rods simultaneously (-$10 to -$20 reactivity)
- Maximum reactivity insertion rate: Limited by Technical Specifications (e.g., ≤5¢/s)

Importance:
- Delayed neutrons extend control time from milliseconds to seconds
- Enable precise power maneuvering
- Prevent prompt critical excursions during normal operation
- Rod ejection/drop accidents analyzed for prompt critical potential
""",
        key_factors=[
            "Effective delayed neutron fraction (β-eff) for mixed core",
            "Prompt neutron lifetime (ℓ)",
            "Reactivity insertion rate (ρ/s or $/s)",
            "Reactor period (T) measurement and limits",
            "Prompt critical threshold (ρ = β)",
            "Scram reactivity worth"
        ],
        primary_authority=[
            "Keepin, Physics of Nuclear Kinetics",
            "Hetrick, Dynamics of Nuclear Reactors",
            "NRC NUREG-1338: Control Rod Drop Accident Analysis"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR, ReactorType.BWR, ReactorType.CANDU]
    ),

    DoctrineBlock(
        topic="xenon_poisoning_iodine_dynamics",
        keywords=["xenon-135", "iodine-135", "xenon poisoning", "iodine pit", "xenon oscillation", "samarium-149"],
        conclusion_template="Xe-135 is the most significant fission product poison (2.7 million barn cross-section). After reactor shutdown, Xe-135 peaks at 8-12 hours due to I-135 decay, creating 'iodine pit' that can prevent restart. Spatial xenon oscillations in large cores require axial power distribution monitoring.",
        reasoning_framework="""
Xenon-135 Production and Removal:
- Production: Fission yield (0.3%) + I-135 decay (6.7% fission yield, 6.6h half-life)
- Removal: Neutron absorption (σ = 2.7×10^6 barns) + decay (9.2h half-life)
- Equilibrium: Production = Removal at steady power

Equilibrium Xenon Worth:
- PWR at full power: ~2500-3000 pcm negative reactivity
- Largest single reactivity effect in reactor
- Proportional to power level (higher flux → more burnout)

Xenon Transients:
1. Startup from Cold:
   - Zero Xe at start
   - Xe builds to equilibrium over 40-50 hours
   - Reactivity decreases ~2500 pcm during buildup
   - Must withdraw control rods or reduce boron to compensate

2. Shutdown (Iodine Pit):
   - Flux → 0, Xe absorption stops but I-135 decay continues
   - Xe peaks at 8-12 hours post-shutdown (~6000 pcm negative)
   - Peak Xe worth may exceed available positive reactivity → can't restart
   - Xe decays over 2-3 days, reactivity recovers
   - Critical for load-following plants (avoid shutdown during Xe peak)

3. Power Reduction:
   - Reduced flux → less Xe burnout
   - I-135 decay continues → Xe rises above equilibrium
   - Negative reactivity insertion → power decreases further
   - Must add positive reactivity (withdraw rods, reduce boron)

4. Power Increase:
   - Increased flux → more Xe burnout
   - Xe temporarily decreases below new equilibrium
   - Positive reactivity → power rises further
   - Must add negative reactivity to prevent overshoot

Xenon Oscillations (Spatial):
- Large cores (PWR/BWR): Axial and radial Xe oscillations possible
- Mechanism: Local power increase → Xe burnout → more power → flux tilt
- Opposite region: Power decrease → Xe buildup → less power
- Oscillation period: ~24-30 hours
- Damping: Requires control rod insertion or power reduction
- Detection: Out-of-core neutron detectors, in-core flux maps
- Prevention: Axial offset monitoring, load-following limits

Samarium-149 (Comparison):
- Stable isotope (no decay removal)
- Cross-section: 40,800 barns (high but < Xe)
- Builds up slowly from Pm-149 (53h half-life)
- Equilibrium: ~700 pcm negative reactivity
- No transient effects (stable → always in equilibrium)
""",
        key_factors=[
            "Equilibrium xenon worth vs power level",
            "Xenon-free to xenon-equilibrium reactivity swing",
            "Iodine pit timing and magnitude",
            "Minimum downtime to avoid xenon dead time",
            "Xenon oscillation damping techniques",
            "Samarium equilibrium worth"
        ],
        primary_authority=[
            "Glasstone & Sesonske, Ch. 7: Fission Product Poisons",
            "NRC NUREG-1350: Information Digest (Xenon Transients)",
            "Randall & St. John, Xenon Spatial Oscillations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR, ReactorType.BWR]
    ),

    # ========== REACTOR SAFETY ==========
    DoctrineBlock(
        topic="defense_in_depth_safety_philosophy",
        keywords=["defense in depth", "safety layers", "redundancy", "diversity", "fail-safe", "safety culture"],
        conclusion_template="Defense-in-depth is the fundamental nuclear safety philosophy requiring multiple independent layers of protection: prevent accidents, detect abnormalities, control transients, contain releases, mitigate consequences. No single failure can defeat all barriers.",
        reasoning_framework="""
Five Levels of Defense in Depth:

Level 1: Prevention (Conservative Design and Operation)
- Margin to operating limits (e.g., power < licensed thermal rating)
- Quality assurance in design, construction, operation
- Defense against common-mode failures
- Redundancy and diversity in safety systems
- Example: Fuel design with margin to melt, pressure vessel 2.5× safety factor

Level 2: Detection and Control (Abnormal Operation)
- Monitoring systems detect parameter deviations
- Automatic control systems restore normal operation
- Reactor protection system (RPS) trips on limiting conditions
- Example: High neutron flux → control rod insertion, pressurizer pressure → spray actuation

Level 3: Accident Mitigation (Design Basis Accidents)
- Engineered Safety Features (ESF) prevent core damage
- Emergency Core Cooling System (ECCS) for LOCAs
- Auxiliary feedwater for steam generator tube rupture (PWR)
- Containment isolation on high radiation/pressure
- Example: Large-break LOCA → ECCS actuates, containment isolates

Level 4: Severe Accident Management (Beyond Design Basis)
- Containment integrity prevents large releases even with core melt
- Passive autocatalytic recombiners (PARs) prevent hydrogen explosion
- Cavity flooding to cool corium (molten core)
- Severe Accident Management Guidelines (SAMGs)
- Example: Fukushima → containment venting prevented catastrophic breach

Level 5: Emergency Response (Off-Site Mitigation)
- Emergency Planning Zones (EPZ): 10 mile plume, 50 mile ingestion
- Evacuation, sheltering, potassium iodide distribution
- Environmental monitoring and dose assessment
- Public communication and coordination with local authorities
- Example: TMI-2 → precautionary evacuation within 5 miles

Safety Principles:
1. Redundancy: Multiple trains of safety systems (2×100%, 3×50%, 4×25%)
2. Diversity: Different technologies for same function (e.g., motor + diesel + turbine-driven pumps)
3. Physical Separation: Trains separated to prevent common damage (fire, flood, missile)
4. Fail-Safe: Components fail to safe state (e.g., control rods drop on loss of power)
5. Single Failure Criterion: Assume one failure, system must still perform
6. Independence: Safety systems independent from control systems

Probabilistic Risk Assessment (PRA):
- Quantifies defense-in-depth effectiveness
- Core Damage Frequency (CDF): Modern PWR/BWR ~10^-5 to 10^-6 per year
- Large Early Release Frequency (LERF): ~10^-7 per year
- Identifies vulnerabilities for improvement
""",
        key_factors=[
            "Safety system redundancy and diversity",
            "Single failure criterion compliance",
            "Common-cause failure prevention",
            "Physical separation of safety trains",
            "Safety-grade vs non-safety-grade classification",
            "Regulatory oversight and inspection"
        ],
        primary_authority=[
            "IAEA Safety Standards NS-R-1: Safety of Nuclear Power Plants - Design",
            "NRC Regulatory Guide 1.174: Probabilistic Risk Assessment",
            "INSAG-10: Defence in Depth in Nuclear Safety (IAEA)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR, ReactorType.BWR, ReactorType.SMR]
    ),

    DoctrineBlock(
        topic="eccs_emergency_core_cooling",
        keywords=["ECCS", "emergency core cooling system", "LOCA", "loss of coolant accident", "high pressure injection", "low pressure injection", "accumulators"],
        conclusion_template="ECCS prevents core damage during LOCAs by providing makeup water at all break sizes. PWR ECCS includes high-pressure injection (small breaks), accumulators (intermediate), and low-pressure injection (large breaks). ECCS must meet 10 CFR 50.46 criteria: peak clad temp <1204°C, <17% clad oxidation, <1% H2 generation, coolable geometry, long-term cooling.",
        reasoning_framework="""
PWR ECCS Architecture (Typical 4-Loop Westinghouse):

1. High Pressure Injection (HPI) / Safety Injection (SI):
   - Centrifugal pumps: 2-3 trains, ~1500 gpm each at 1200 psi
   - Actuation: Reactor trip + low pressurizer pressure (1800 psi)
   - Purpose: Small breaks (0.5-2 inch), maintain core cooling before depressurization
   - Water source: Refueling Water Storage Tank (RWST), borated water

2. Accumulators (Passive):
   - Pressure tanks: 4 units (one per loop), 7000-8000 gal each
   - Gas pressure: Nitrogen, 600-700 psi
   - Actuation: Automatic when RCS pressure < accumulator pressure (~600 psi)
   - Purpose: Intermediate breaks (2-6 inch), rapid inventory addition during blowdown
   - Boron concentration: 2000-2400 ppm

3. Low Pressure Injection (LPI) / Residual Heat Removal (RHR):
   - High-capacity pumps: 2 trains, ~4000 gpm each at 150 psi
   - Actuation: Low pressurizer pressure (~200 psi)
   - Purpose: Large breaks (>6 inch), long-term core cooling
   - Also used for shutdown cooling and containment spray

4. Containment Spray:
   - Pumps: 2 trains, spray headers in containment dome
   - Purpose: Reduce containment pressure/temperature, scrub fission products
   - Water source: RWST initially, then recirculation from sump

LOCA Phases:

Phase 1: Blowdown (0-30 seconds):
- Break opens, RCS depressurizes rapidly
- Core initially cooled by stored energy in coolant
- Accumulators inject when pressure drops below 600 psi
- HPI pumps start but flow limited by back-pressure

Phase 2: Refill (30-60 seconds):
- RCS pressure equalizes with containment
- Downcomer and lower plenum refill with ECCS water
- Core still uncovered, heating up

Phase 3: Reflood (1-5 minutes):
- ECCS water rises through core
- Steam generation cools fuel (film boiling → nucleate boiling transition)
- Peak clad temperature (PCT) reached during this phase
- Must satisfy 10 CFR 50.46 limits

Phase 4: Long-Term Cooling (hours to days):
- Core fully quenched
- RHR pumps provide continuous cooling
- Recirculation mode: Pump water from containment sump through RHR heat exchangers
- Decay heat removal over months

10 CFR 50.46 Acceptance Criteria:
1. Peak clad temperature (PCT) ≤ 1204°C (2200°F)
2. Maximum clad oxidation ≤ 17% of total clad thickness
3. Maximum hydrogen generation ≤ 1% of total clad
4. Coolable geometry maintained (no core melt, rod fragmentation)
5. Long-term cooling capability demonstrated

BWR ECCS (Comparison):
- High Pressure Core Spray (HPCS): Similar to PWR HPI
- Low Pressure Core Spray (LPCS): Top-down spray cooling
- Low Pressure Coolant Injection (LPCI): Similar to PWR LPI
- Automatic Depressurization System (ADS): Opens relief valves to allow LPI injection
- No accumulators (boiling reactor → different transient)
""",
        key_factors=[
            "ECCS pump head-flow characteristics",
            "Break size vs applicable ECCS train",
            "RWST inventory and switchover to recirculation",
            "Sump screen clogging (debris, insulation)",
            "Peak clad temperature calculation (RELAP, TRACE codes)",
            "Emergency Operating Procedures (EOPs) for ECCS actuation"
        ],
        primary_authority=[
            "10 CFR 50.46: Acceptance Criteria for ECCS",
            "NRC Regulatory Guide 1.157: LOCA Evaluation Models",
            "WCAP-16996-P: Realistic LOCA Methodology (Westinghouse)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR]
    ),

    DoctrineBlock(
        topic="containment_structure_function",
        keywords=["containment", "containment building", "design pressure", "leak rate", "pressure suppression", "filtered vents"],
        conclusion_template="Containment is the final barrier preventing fission product release to environment. PWR large-dry containment designed for ~50 psi internal pressure; BWR Mark I/II use pressure suppression pools. Post-Fukushima, filtered vents and severe accident improvements enhance containment integrity.",
        reasoning_framework="""
PWR Containment (Large Dry):
- Type: Steel-lined reinforced concrete cylinder with hemispherical dome
- Dimensions: ~40m diameter, ~60m tall, 1-1.5m thick concrete, 6-12mm steel liner
- Design pressure: 45-60 psig (3-4 bar)
- Free volume: ~2.5-3.0 million ft³
- Function: Withstand steam/hydrogen pressure from LOCA, prevent release

Design Basis:
- Large-break LOCA with concurrent loss of offsite power
- Maximum pressure occurs 20-60 seconds post-LOCA (steam blowdown)
- Containment spray reduces pressure via steam condensation
- Passive heat removal through concrete walls (no active systems required for 72 hours)

Penetrations:
- Equipment hatch: Large opening for reactor vessel installation
- Personnel airlock: Double-door interlocked entry
- Piping: All lines isolated on containment isolation signal (CIS)
- Electrical: Sealed penetrations for cables
- Each penetration tested for leak-tightness (10 CFR 50 Appendix J)

Leak Rate Testing:
- Type A: Integrated leak rate test (ILRT) every 10-15 years, pressurize to design pressure
- Type B: Local leak rate tests (LLRT) on penetrations every 2 years
- Type C: Valves and airlocks every 2 years
- Acceptance: <0.1-0.2% containment volume per day at design pressure

BWR Mark I Containment (Pressure Suppression):
- Dry well: Steel pressure vessel surrounding reactor (pear-shaped)
- Wet well (torus): Donut-shaped pool below dry well
- Vent pipes: 8-10 large pipes connect dry well to suppression pool
- Design: LOCA steam routed to pool, condenses, limits pressure
- Pressure: ~40 psig design, ~20 psig typical peak

BWR Mark II/III:
- Mark II: Pressure suppression with over/under weir design
- Mark III: Large dry containment similar to PWR

Severe Accident Features (Post-Fukushima):
1. Hydrogen Control:
   - Passive Autocatalytic Recombiners (PARs): Catalytically combine H2+O2 → H2O
   - Igniter systems: Controlled burn before explosive concentration
   - Inerting (BWR Mark I): Nitrogen atmosphere during operation (no oxygen → no H2 combustion)

2. Cavity Flooding:
   - Flood reactor cavity to cool molten corium (core-concrete interaction mitigation)
   - External Reactor Vessel Cooling (ERVC): Cool vessel exterior to prevent failure

3. Filtered Containment Venting:
   - Release pressure to prevent catastrophic failure
   - Filters remove ~99.9% of particulates, ~99% of iodine
   - Hardened vent paths withstand severe accident conditions

4. Instrumentation:
   - Wide-range pressure, temperature, radiation monitors
   - Hydrogen concentration monitoring
   - Water level in sump/cavity

Containment Failure Modes:
- Overpressure: Exceeds design pressure (>60 psi PWR, >40 psi BWR)
- Basemat melt-through: Molten corium erodes concrete foundation
- Hydrogen detonation: Concentration >8-10% in air
- Steam explosion: Molten fuel contacts water (rapid pressurization)
- Bypass: Steam generator tube rupture (PWR) → release to atmosphere via secondary
""",
        key_factors=[
            "Containment design pressure and margin",
            "Leak rate test results and trend",
            "Hydrogen concentration limits",
            "Containment spray actuation setpoint",
            "Severe accident management guidelines (SAMGs)",
            "Venting strategy (filtered vs unfiltered)"
        ],
        primary_authority=[
            "10 CFR 50 Appendix J: Containment Leak Rate Testing",
            "NRC NUREG-1935: State-of-the-Art Reactor Consequence Analyses",
            "IAEA TECDOC-1791: Mitigation of Hydrogen Hazards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR, ReactorType.BWR]
    ),

    # ========== RADIATION PROTECTION ==========
    DoctrineBlock(
        topic="alara_dose_limits",
        keywords=["ALARA", "as low as reasonably achievable", "dose limits", "occupational exposure", "public dose", "10 CFR 20"],
        conclusion_template="ALARA (As Low As Reasonably Achievable) is the legal and ethical requirement to minimize radiation exposure below regulatory limits. 10 CFR 20 limits: 5 rem/year occupational, 0.1 rem/year public. Time, distance, shielding are primary ALARA tools.",
        reasoning_framework="""
Regulatory Dose Limits (10 CFR 20):

Occupational (Adult Workers):
- Total Effective Dose Equivalent (TEDE): 5 rem/year (50 mSv/year)
- Lens of eye: 15 rem/year
- Shallow dose (skin): 50 rem/year
- Extremities: 50 rem/year
- Declared pregnant worker: 0.5 rem to embryo/fetus over gestation
- Minors: 10% of adult limits

Public:
- TEDE: 0.1 rem/year (100 mrem/year, 1 mSv/year)
- Effluent limits: 10 CFR 50 Appendix I (ALARA for releases)
- Unrestricted area boundary dose

ALARA Program Elements:
1. Management commitment and policy
2. Dose tracking and trending (individual and collective)
3. Pre-job ALARA planning for high-dose tasks
4. Engineering controls (remote handling, shielding, ventilation)
5. Administrative controls (access limitations, time limits)
6. ALARA review committee
7. Training and awareness

Time-Distance-Shielding:

Time:
- Dose = Dose Rate × Time
- Minimize duration in radiation areas
- Use mock-ups for training (reduce time in actual field)
- Dose rate surveys to identify hot spots

Distance:
- Dose Rate ∝ 1/r² (point source, no scattering)
- Double distance → 1/4 dose rate
- Remote tools extend effective distance (10-ft pole reduces dose 100×)

Shielding:
- Gamma: High-Z materials (lead, tungsten, concrete)
- Neutron: Hydrogenous materials (water, polyethylene, concrete)
- Beta: Low-Z materials (plastic, aluminum) avoid bremsstrahlung
- Alpha: Paper, skin (not penetrating, inhalation/ingestion hazard)
- Half-Value Layer (HVL): Thickness reducing dose rate by 50%
  - Co-60 (1.25 MeV): 1.2 cm lead, 6 cm concrete
  - Cs-137 (0.662 MeV): 0.65 cm lead, 4.8 cm concrete

Radiation Work Permits (RWP):
- Required for entry to High Radiation Areas (>100 mrem/hr)
- Specifies: Dose rate, estimated dose, time limit, protective equipment
- Pre-job briefing, dose tracking, post-job survey

Contamination Control:
- Surface contamination limits (removable): 1000 dpm/100cm² β/γ, 20 dpm/100cm² α
- Contamination Area: >10,000 dpm/100cm² removable
- Personal Protective Equipment (PPE): Anti-contamination clothing, respirators
- Portal monitors detect contamination on exit

Internal Dose:
- Derived Air Concentration (DAC): Air concentration for 50 mSv/year internal dose
- Annual Limit on Intake (ALI): Activity intake for 50 mSv committed dose
- Bioassay: Whole-body counting, urinalysis to detect internal contamination
- Respiratory protection: Fit testing, assigned protection factor (APF)

Typical Plant Doses:
- Average occupational: 50-200 mrem/year (well below 5 rem limit)
- Refueling outage workers: 500-1500 mrem per outage
- High-dose tasks: Steam generator replacement, reactor vessel inspection
- Public dose from plant effluents: <1 mrem/year (100× below limit)
""",
        key_factors=[
            "Individual and collective dose tracking",
            "Hot particle detection and removal",
            "Source term reduction (coolant chemistry, system decon)",
            "Job planning and dose estimation",
            "Protective equipment selection",
            "Regulatory reporting (10 CFR 20.2206 annual reports)"
        ],
        primary_authority=[
            "10 CFR 20: Standards for Protection Against Radiation",
            "NRC Regulatory Guide 8.8: ALARA Program Information",
            "ICRP Publication 103: Recommendations of the ICRP (2007)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR, ReactorType.BWR, ReactorType.CANDU]
    ),

    # ========== SPENT FUEL MANAGEMENT ==========
    DoctrineBlock(
        topic="spent_fuel_pool_storage",
        keywords=["spent fuel pool", "SFP", "wet storage", "decay heat", "boiling", "fuel rack", "criticality"],
        conclusion_template="Spent fuel pools store discharged fuel underwater for 5-10 years to remove decay heat and provide radiation shielding. SFP cooling and makeup are critical safety functions; loss of cooling can lead to boiling, uncovery, zircaloy fire (Fukushima lesson). High-density racks use borated steel or flux traps for criticality control.",
        reasoning_framework="""
Spent Fuel Pool Design:

Physical:
- Location: Typically adjacent to reactor building (PWR), above reactor (BWR)
- Depth: 40-45 feet, fuel ~25 feet deep under water
- Water volume: 250,000-500,000 gallons
- Water: Demineralized, borated (2000 ppm boron)
- Liner: Stainless steel, leak detection underneath
- Capacity: 1.5-3× full core offloads (20-30 years of spent fuel)

Decay Heat Removal:
- Fresh discharge: ~10 MW thermal (1% of reactor power)
- After 1 day: ~4 MW
- After 1 week: ~2 MW
- After 1 year: ~0.5 MW
- After 10 years: ~0.1 MW
- SFP cooling pumps: 2-3 trains, 1000-3000 gpm, heat exchangers
- Ultimate heat sink: Component cooling water → service water → ocean/river/cooling tower

Criticality Prevention:
- k-eff must be <0.95 with optimum moderation and unborated water (worst case)
- Methods:
  1. Low-density racks: Large spacing (21-inch pitch), ~200 assemblies
  2. High-density racks: Borated steel (B4C) neutron absorber panels, 9-inch pitch
  3. Flux trap design: Water gaps between absorber panels
  4. Burnup credit: Higher burnup fuel has lower reactivity (not yet fully approved)
- Analysis: KENO Monte Carlo, CASMO/SIMULATE, worst-case fresh fuel assumption

Water Level and Shielding:
- Minimum 10 feet of water above fuel for shielding
- Dose rate at pool edge: <2 mrem/hr with 20 feet of water
- Makeup systems: Multiple sources (demineralized, service water, fire protection)
- Evaporation: ~50-100 gpm under normal conditions

Spent Fuel Pool Accident (Fukushima Insight):
- Loss of cooling → water heats to boiling (~100°C)
- Boil-off rate: ~50-100 gpm with fresh fuel
- If uncovered: Zircaloy oxidation begins at 900°C (exothermic, accelerates)
  Zr + 2H2O → ZrO2 + 2H2 + heat
- Hydrogen generation and potential fire/explosion
- Massive fission product release if cladding fails (SFP not in containment)

Post-Fukushima Improvements:
- Instrumentation: Reliable water level indication
- Makeup: Diverse and flexible connections (fire hoses, temporary pumps)
- FLEX equipment: Portable pumps, generators, hoses staged on-site
- Spray capability: Spray from above if pool level lost
- Emergency procedures: Severe accident management for SFP

Fuel Handling:
- Refueling: Underwater using fuel handling crane and tools
- Inspection: Visual, ultrasonic (UT), eddy current (ET) for defects
- Reracking: Moving fuel between racks to balance heat load
- Cask loading: Transfer fuel to dry storage cask after ~5-10 years cooling
""",
        key_factors=[
            "SFP cooling system redundancy",
            "Makeup water sources and flow rates",
            "Boil-off time to uncovery",
            "Fuel rack criticality safety margin",
            "Dose rates during fuel handling",
            "Seismic qualification of racks and building"
        ],
        primary_authority=[
            "NRC NUREG-1738: SFP Accident Risk Assessment",
            "10 CFR 50.68: Criticality Accident Requirements",
            "NRC Information Notice 2012-13: Fukushima SFP Insights"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR, ReactorType.BWR]
    ),

    DoctrineBlock(
        topic="dry_cask_storage_isfsi",
        keywords=["dry cask", "dry storage", "ISFSI", "independent spent fuel storage installation", "MPC", "canister", "passive cooling"],
        conclusion_template="Dry cask storage uses sealed steel canisters filled with inert gas, placed in concrete or steel overpacks, cooled by passive air circulation. Licensed for 40-60 years (renewable), dry casks are seismically robust and eliminate boiling/criticality concerns of wet storage. No central repository exists; 70+ ISFSIs in US store ~90,000 MTU.",
        reasoning_framework="""
Dry Cask Storage System Components:

Multi-Purpose Canister (MPC):
- Stainless steel cylinder, welded lid
- Dimensions: ~5m tall, ~2m diameter, ~100 tons loaded
- Capacity: 24-37 PWR assemblies or 56-89 BWR assemblies
- Fill gas: Helium (inert, good thermal conductivity)
- Pressure: ~5 bar helium backfill
- Sealing: Multi-layer weld, leak-tested to ANSI N14.5

Overpack Options:
1. Vertical concrete cask:
   - Reinforced concrete body, ~25 cm thick
   - Steel liner inside, weather barrier outside
   - Air inlet vents at bottom, outlet at top (passive convection)
   - Weight: ~150 tons loaded

2. Horizontal storage module (HSM):
   - Concrete bunker, MPC inserted horizontally
   - Common at BWR sites
   - Natural air circulation through vents

Transfer Cask:
- Temporary shielded cask for moving MPC from SFP to ISFSI
- Not used for long-term storage

Heat Removal:
- Passive air cooling: Natural convection driven by decay heat
- Air flow: Inlet (ambient) → annulus → outlet (heated ~30°C rise)
- Heat load: 10-40 kW per cask (depends on fuel age, loading)
- No active systems → no pumps, no electricity, no operator action

Fuel Eligibility:
- Minimum cooling time: 3-10 years in SFP (depends on burnup)
- Maximum burnup: 45-62 GWd/MTU (depending on cask design)
- Maximum decay heat per assembly: 0.5-1.5 kW
- Damaged fuel: Special canisters with failed clad fuel

Criticality Safety:
- Dry environment → no moderation → subcritical even with fresh fuel
- Basket design: Borated aluminum or steel neutron absorbers
- k-eff < 0.95 under all conditions (flooding, optimal moderation)

Licensing:
- 10 CFR 72: Licensing Requirements for ISFSI
- Certificate of Compliance (CoC): NRC approves cask design (40-60 years)
- Site-specific or general license
- Renewal: 10 CFR 72 allows renewal in 20-40 year increments
- Aging management: Inspections, monitoring for degradation

Current Status (US):
- ~70 ISFSIs at reactor sites + 1 away-from-reactor (Morris, IL)
- ~90,000 MTU spent fuel (~3000 casks)
- No permanent repository (Yucca Mountain project canceled)
- Continued storage GEIS: Assumes on-site storage for 60-160 years

Cask Vendors:
- NAC International: NAC-UMS, NAC-MPC
- Holtec: HI-STORM, HI-STAR
- Transnuclear (AREVA): NUHOMS
- EnergySolutions: FuelSolutions

Challenges:
- Retrievability: Must be able to remove fuel for eventual disposal
- Corrosion: Stress corrosion cracking of stainless steel (salt environments)
- Crud: Fuel surface deposits can increase heat load
- Public acceptance: Community concerns about long-term storage
""",
        key_factors=[
            "Maximum cladding temperature (400°C limit)",
            "Helium leak rate and pressure monitoring",
            "Concrete degradation (aging management)",
            "Thermal performance during off-normal conditions",
            "Seismic analysis and tip-over prevention",
            "Radiation dose rates at site boundary (<25 mrem/year)"
        ],
        primary_authority=[
            "10 CFR 72: Licensing Requirements for ISFSI and Dry Cask Storage",
            "NRC NUREG-2215: Dry Cask Storage Standard Review Plan",
            "EPRI TR-1025206: Dry Cask Storage Characterization"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR, ReactorType.BWR]
    ),

    # ========== WASTE MANAGEMENT ==========
    DoctrineBlock(
        topic="nuclear_waste_classification_hlw_llw",
        keywords=["high-level waste", "HLW", "low-level waste", "LLW", "transuranic", "TRU", "GTCC", "waste classification"],
        conclusion_template="Nuclear waste is classified by origin and radioactivity: HLW (spent fuel, reprocessing waste), TRU (>100 nCi/g alpha, Z>92), LLW Classes A/B/C (reactor operations), GTCC (low-level but exceeds Class C limits). Disposal requirements vary from shallow land burial (LLW) to deep geologic repository (HLW/TRU).",
        reasoning_framework="""
Waste Classification (10 CFR 61):

High-Level Waste (HLW):
- Definition: Spent nuclear fuel OR liquid/solid reprocessing waste
- Activity: Highest levels of fission products and actinides
- Heat: Significant decay heat (>2 kW/canister)
- Volume: ~70,000 MTU spent fuel + ~90 million gallons reprocessing waste (legacy)
- Disposal: Deep geologic repository (Yucca Mountain planned, now canceled)
- Timeframe: Isolation required for 10,000-1,000,000 years

Transuranic Waste (TRU):
- Definition: Alpha-emitting isotopes with Z>92, half-life >20 years, >100 nCi/g
- Sources: Plutonium contaminated materials (gloves, tools, rags), reprocessing residues
- Volume: ~100,000 m³ (US defense programs)
- Disposal: Waste Isolation Pilot Plant (WIPP), New Mexico, salt formation 655m deep
- Timeframe: Isolation for 10,000 years

Low-Level Waste (LLW) - 10 CFR 61.55:
- Class A (lowest):
  - Limits: C-14 <0.8 Ci/m³, Ni-63 <3.5 Ci/m³, Cs-137 <1 Ci/m³
  - Examples: Contaminated paper, plastic, tools (short half-life)
  - Disposal: Shallow land burial, no engineered barriers required after 100 years

- Class B (intermediate):
  - Limits: C-14 <8 Ci/m³, Ni-63 <70 Ci/m³, Cs-137 <44 Ci/m³
  - Examples: Resins, filters, evaporator bottoms
  - Disposal: Shallow burial with stability requirements (no subsidence)

- Class C (highest LLW):
  - Limits: C-14 <80 Ci/m³, Ni-63 <700 Ci/m³, TRU <100 nCi/g
  - Examples: Activated metals (reactor internals), concentrated resins
  - Disposal: Shallow burial with intruder barriers (concrete, clay caps)

Greater Than Class C (GTCC):
- Exceeds Class C limits but not HLW/TRU
- Examples: Reactor pressure vessel internals, sealed sources
- Volume: ~10,000 m³ projected
- Disposal: DOE responsibility, likely deep borehole or repository

Waste Volumes and Sources:

Reactor Operations (per GWe-year):
- LLW: 50-150 m³/year
  - Dry active waste (DAW): Protective clothing, paper, plastic (~40%)
  - Wet waste: Resins, filters, sludges (~30%)
  - Irradiated components: Tools, parts (~20%)
  - Other: Contaminated oil, trash (~10%)
- Spent fuel: 20-30 MTU/year

Volume Reduction Techniques:
- Compaction: 4:1 to 10:1 reduction for DAW
- Incineration: 100:1 reduction (now rare due to air emissions)
- Supercompaction: 5:1 additional reduction after initial compaction
- Evaporation: Concentrate liquid waste, reduce volume 10-50×
- Decontamination: Clean and free-release items (no disposal needed)

Disposal Sites (US):
- LLW: Barnwell SC (SE compact), Richland WA (NW/Rocky Mountain), Clive UT (EnergySolutions)
- Closed: Beatty NV, Maxey Flats KY, Sheffield IL, West Valley NY
- HLW: None (Yucca Mountain license denied)
- TRU: WIPP (Carlsbad, NM)

Typical Isotopes by Category:

HLW/Spent Fuel:
- Fission products: Cs-137, Sr-90, I-129, Tc-99 (half-lives 30y to millions)
- Actinides: Pu-239, Am-241, Cm-244 (thousands of years)

LLW Class A:
- H-3, C-14, Co-60, Fe-55 (mostly <30 year half-lives)

LLW Class C/GTCC:
- Ni-63, Nb-94, Ni-59 (activation products, 100-20,000 year half-lives)

TRU:
- Pu-238, Pu-239, Am-241 (24,000+ year half-lives)
""",
        key_factors=[
            "Waste characterization (gamma spectroscopy, scaling factors)",
            "10 CFR 61 concentration limits compliance",
            "Waste form stability (compressive strength, leachability)",
            "Package integrity (Type A/B shipping containers)",
            "Disposal site waste acceptance criteria (WAC)",
            "Cost per cubic foot disposal ($100-3000/ft³ depending on class)"
        ],
        primary_authority=[
            "10 CFR 61: Licensing Requirements for Land Disposal of Radioactive Waste",
            "NRC Branch Technical Position on Waste Form (1991)",
            "DOE Order 435.1: Radioactive Waste Management"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR, ReactorType.BWR]
    ),

    # ========== NRC REGULATIONS ==========
    DoctrineBlock(
        topic="nrc_10cfr50_licensing",
        keywords=["10 CFR 50", "operating license", "construction permit", "FSAR", "technical specifications", "NRC inspection"],
        conclusion_template="10 CFR 50 governs domestic licensing of nuclear power reactors. Licensing requires construction permit (based on PSAR), then operating license (based on FSAR). Technical Specifications define operational limits and surveillance requirements. NRC conducts resident inspection and enforcement using Reactor Oversight Process (ROP).",
        reasoning_framework="""
Licensing Process (10 CFR 50):

Phase 1: Early Site Permit (Optional, 10 CFR 52):
- Site suitability evaluation (seismic, meteorology, hydrology, demographics)
- Valid for 20 years, banked for future use
- Resolves site issues before reactor design selected

Phase 2: Construction Permit (CP):
- Application: Preliminary Safety Analysis Report (PSAR)
- PSAR Contents:
  - Site characteristics
  - Reactor design (conceptual)
  - Safety systems
  - Accident analyses (preliminary)
- Review: NRC staff (18-24 months), ACRS review, public hearing
- Approval: CP issued, construction authorized

Phase 3: Operating License (OL):
- Application: Final Safety Analysis Report (FSAR)
- FSAR Contents (18 chapters):
  - Ch 1-2: Introduction, site characteristics
  - Ch 3-5: Design of structures, reactor, coolant systems
  - Ch 6: Engineered safety features
  - Ch 7-8: Instrumentation, electric power
  - Ch 9-13: Auxiliary systems, steam, radioactive waste, conduct of operations
  - Ch 14-15: Testing, accident analyses
  - Ch 16-18: Technical Specs, quality assurance, human factors
- Inspections, Tests, Analyses, and Acceptance Criteria (ITAAC) verified
- Fuel load authorization → criticality testing → power ascension testing
- Full-power license issued after successful testing

Technical Specifications (10 CFR 50.36):
- Limiting Conditions for Operation (LCO): Equipment required for safe operation
- Limiting Safety System Settings (LSSS): Trip setpoints
- Surveillance Requirements (SR): Test frequency and acceptance criteria
- Design Features: Physical characteristics (fuel enrichment, containment)
- Administrative Controls: Organization, procedures, reporting

Example LCO:
- "Two steam generators shall be OPERABLE in MODES 1, 2, and 3"
- Action: If one SG inoperable, restore within 72 hours or be in Mode 3 within 6 hours

Reactor Oversight Process (ROP):
- Cornerstone Approach: Initiating Events, Mitigating Systems, Barrier Integrity, Emergency Preparedness
- Performance Indicators (PIs): Objective metrics (scrams, safety system unavailability)
- Inspection Findings: Violations categorized by significance (Green/White/Yellow/Red)
- Action Matrix: Increased oversight for degraded performance
- Resident Inspectors: 2-3 NRC inspectors on-site full-time

License Renewal (10 CFR 54):
- Original license: 40 years
- Renewal: Additional 20 years (one renewal granted → 60 year total)
- Second renewal: Additional 20 years (80 years total) - several under review
- Aging Management Programs (AMPs): Address time-limited aging analyses (TLAA)
- Examples: Reactor vessel embrittlement, fatigue, corrosion

Enforcement (10 CFR 2 Appendix C):
- Severity Levels:
  - Level I (Red): Serious safety significance
  - Level II (Yellow): Moderate safety significance
  - Level III (White): Low safety significance
  - Level IV (Green): Minimal safety significance
- Civil penalties: $0 to $150,000+ per violation per day
- Orders: Modify, suspend, or revoke license
- Confirmatory Action Letters (CAL): Formal commitments

Reportability (10 CFR 50.72/50.73):
- Immediate (1-hour): Unplanned reactor trip, loss of safety function
- 24-hour: Degraded safety system
- 30-day: Procedure violations, design deficiencies
- Event Notification System (ENS): 24/7 NRC Operations Center
- Licensee Event Report (LER): Detailed written report within 60 days
""",
        key_factors=[
            "FSAR update requirements (10 CFR 50.71e)",
            "License amendment process (10 CFR 50.90)",
            "10 CFR 50.59 evaluations (changes without prior NRC approval)",
            "Technical Specification compliance and reporting",
            "NRC inspection program scope and frequency",
            "Operational event rate (scrams per 7000 critical hours)"
        ],
        primary_authority=[
            "10 CFR 50: Domestic Licensing of Production and Utilization Facilities",
            "NRC NUREG-0800: Standard Review Plan",
            "NRC Inspection Manual Chapter 2515: Reactor Oversight Process"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        reactor_scope=[ReactorType.PWR, ReactorType.BWR]
    ),

    # ========== ADVANCED REACTORS ==========
    DoctrineBlock(
        topic="small_modular_reactors_smr",
        keywords=["SMR", "small modular reactor", "NuScale", "BWRX-300", "mPower", "passive safety", "factory fabrication"],
        conclusion_template="Small Modular Reactors (SMRs) are advanced reactors <300 MWe designed for factory fabrication, reduced capital cost, enhanced passive safety, and flexible siting. NuScale (77 MWe iPWR) received first US Design Certification (2020). SMR advantages: modularity, reduced construction risk, passive safety; challenges: economics of scale, supply chain, regulatory novelty.",
        reasoning_framework="""
SMR Definition and Characteristics:

Size:
- Small: <300 MWe electrical output (vs 1000+ MWe for traditional)
- Modular: Factory-fabricated modules, rail/truck transportable
- Scalability: Deploy 1-12 modules as needed

Leading SMR Designs (US):

1. NuScale Power Module (iPWR):
   - Capacity: 77 MWe (250 MWth) per module
   - Design: Integral PWR (steam generators inside vessel)
   - Containment: Steel vessel submerged in pool
   - Passive safety: Natural circulation, no reactor coolant pumps
   - Certification: NRC Design Certification approved 2020
   - Deployment: UAMPS project, Idaho (6 modules, 462 MWe)

2. GE-Hitachi BWRX-300 (SMR BWR):
   - Capacity: 300 MWe
   - Design: Simplified BWR with passive safety
   - Passive ECCS: Isolation Condenser, Gravity-Driven Cooling
   - No recirculation pumps (natural circulation)
   - Licensing: Canada (CNSC pre-licensing), US (in progress)

3. Holtec SMR-160 (iPWR):
   - Capacity: 160 MWe
   - Design: Integral PWR with underground siting
   - Passive cooling: Air-cooled condenser
   - Fuel: Standard 17×17 PWR assemblies

4. Westinghouse eVinci (Micro-reactor):
   - Capacity: 5 MWe (15 MWth)
   - Design: Heat pipe cooled, solid core
   - Fuel: TRISO in metal matrix
   - Lifetime: 8+ years without refueling

Passive Safety Features:

Natural Circulation:
- No reactor coolant pumps → eliminates pump failure and seal LOCA
- Buoyancy-driven flow sufficient for decay heat removal
- Slower transients → more time for operator response

Passive ECCS:
- Gravity-driven injection (no pumps)
- Boiling/condensation heat transfer
- Example (NuScale): Reactor vessel submerged in pool, heat conducts through steel to pool → pool boils → steam vented

Inherent Safety:
- Smaller core → lower power density → slower heatup
- Higher surface-to-volume ratio → better heat removal
- Negative reactivity coefficients (self-regulating)

Economic and Deployment Advantages:

Factory Fabrication:
- Modules built in factory → higher quality, shorter schedule
- Rail/truck transport to site
- Reduced on-site construction (crane hours, labor)

Financial:
- Lower upfront capital per module (~$500M vs $10B for large plant)
- Incremental deployment → cash flow starts earlier
- Reduced construction risk (proven module design)

Flexibility:
- Right-size for small grids, remote areas, industrial applications
- Load following (turn modules on/off)
- Non-electric applications: Desalination, district heating, hydrogen production

Challenges:

Economics:
- Loss of economy of scale → higher $/kW than large reactors
- Target: $4000-6000/kW vs $6000-9000/kW for large reactors
- Requires factory production volume (>10/year) to achieve cost targets

Regulatory:
- First-of-a-kind licensing (NuScale took 5 years)
- Addressing prescriptive regulations written for large reactors
- Need for risk-informed, performance-based rules

Supply Chain:
- Establishing factory production lines
- Specialized components (small steam generators, compact vessels)
- Quality assurance for factory production

Spent Fuel:
- More modules → more spent fuel handling
- Integral designs may require specialized casks

Market:
- Competition with natural gas, renewables + storage
- Customer acceptance of nuclear (public perception)
- Need for standardized design (avoid customization)

Current Status (2026):
- NuScale: Design certified, UAMPS project delayed to ~2029
- BWRX-300: Canada site preparation (Ontario Power Generation)
- TerraPower Natrium (345 MWe sodium fast reactor): Kemmerer, WY construction planned
- X-energy Xe-100 (80 MWe TRISO gas reactor): DOE Advanced Reactor Demonstration
""",
        key_factors=[
            "Passive safety system reliability demonstration",
            "Factory quality assurance program",
            "Module transportation and site assembly logistics",
            "Economic competitiveness vs combined-cycle gas",
            "Grid integration (voltage regulation, frequency response)",
            "Security plan for smaller, distributed plants"
        ],
        primary_authority=[
            "NRC Design Certification: NuScale (DC-52-04)",
            "DOE Advanced Reactor Demonstration Program",
            "NEI 18-04: Risk-Informed Performance-Based Guidance for SMRs"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        reactor_scope=[ReactorType.SMR]
    ),

    DoctrineBlock(
        topic="fusion_energy_tokamak_basics",
        keywords=["fusion", "tokamak", "ITER", "deuterium-tritium", "plasma", "magnetic confinement", "Q factor"],
        conclusion_template="Fusion energy releases energy by fusing light nuclei (D+T → He + n + 17.6 MeV). Tokamak uses magnetic fields to confine 100-million°C plasma long enough for net energy gain. ITER aims for Q=10 (10× energy out vs in). Major challenges: plasma stability, tritium breeding, first-wall materials, and scaling to commercial power (DEMO). Fusion promises unlimited fuel, no long-lived waste, inherent safety, but remains decades from commercial deployment.",
        reasoning_framework="""
Fusion Reactions:

Primary Reaction (D-T):
- Deuterium + Tritium → Helium-4 + Neutron + 17.6 MeV
- D + T → ⁴He (3.5 MeV) + n (14.1 MeV)
- Advantages: Lowest temperature requirement (~100 million K), highest cross-section
- Disadvantages: Tritium is radioactive (12.3y half-life), must be bred, neutrons activate structure

Alternative Reactions:
- D + D → T + p (4.0 MeV) or ³He + n (3.3 MeV)
- D + ³He → ⁴He + p (18.3 MeV) - aneutronic (no neutrons), but requires 1 billion K
- p + ¹¹B → 3 ⁴He (8.7 MeV) - aneutronic, very high temperature

Lawson Criterion (Ignition Conditions):
- Must satisfy: n·τ·T > 3×10²¹ m⁻³·s·keV
  - n: Plasma density (~10²⁰ particles/m³)
  - τ: Energy confinement time (~5 seconds)
  - T: Temperature (~10-20 keV = 100-200 million K)
- If met, fusion power > input power (self-sustaining)

Tokamak Design:

Magnetic Confinement:
- Toroidal field coils: Create primary magnetic field (5-10 Tesla)
- Poloidal field coils: Induce current in plasma (creates secondary field)
- Resulting field: Helical field lines confine plasma in toroidal chamber
- Plasma shape: Doughnut-shaped, major radius ~6m, minor radius ~2m (ITER)

Heating Methods:
- Ohmic heating: Induced current resistively heats plasma (~10-30 MW, up to ~20 million K)
- Neutral Beam Injection (NBI): High-energy deuterium atoms (~1 MeV, 33 MW)
- Radio-Frequency (RF) heating: Ion cyclotron (ICRH) or electron cyclotron (ECRH) (~20 MW)
- Alpha particle heating: Fusion-born alphas deposit energy in plasma (self-heating at ignition)

Plasma Stability Challenges:
- MHD instabilities: Edge-localized modes (ELMs), disruptions
- Turbulence: Anomalous transport reduces confinement
- Impurities: High-Z materials (tungsten) radiate energy, cool plasma
- Control: Feedback systems, pellet injection, error field correction coils

ITER (International Thermonuclear Experimental Reactor):

Parameters:
- Location: Cadarache, France
- Partners: EU, US, Russia, China, Japan, Korea, India
- Major radius: 6.2 m, minor radius: 2.0 m
- Plasma volume: 840 m³
- Magnetic field: 5.3 T toroidal
- Plasma current: 15 MA
- Fusion power: 500 MW (Q = 10, 50 MW input → 500 MW fusion output)
- Pulse length: 400-600 seconds (not continuous)
- Construction: 2010-2035 (first plasma ~2035), full D-T operations ~2035-2040

Key Technologies:
- Superconducting magnets: Nb₃Sn, 4.5 K, 68,000 amp
- Blanket modules: Breed tritium, shield magnets from neutrons
- Divertor: Tungsten, exhaust heat and helium ash (10-20 MW/m² heat flux)
- Vacuum vessel: Double-wall steel, 8000 m³

Tritium Breeding:
- Tritium scarce (no natural supply beyond trace atmospheric)
- Blanket modules contain lithium:
  - ⁶Li + n → T + ⁴He + 4.8 MeV
  - ⁷Li + n → T + ⁴He + n - 2.5 MeV (requires fast neutron)
- Breeding ratio must be >1.0 to sustain fuel supply
- Tritium handling: Closed loop, minimize inventory (<1 kg on-site)

Materials Challenges:

First Wall:
- 14.1 MeV neutrons cause displacement damage (atomic displacements)
- Fluence: ~3-5 MW·y/m² over lifetime → 30-50 dpa (displacements per atom)
- Embrittlement, swelling, activation
- Candidate materials: Tungsten (high melting point), reduced-activation ferritic steel (RAFM)

Neutron Activation:
- 14 MeV neutrons activate all structural materials
- Tungsten, steel → radioactive isotopes (half-lives days to years)
- Advantage: No long-lived transuranics (no fission → no Pu, Am, Cm)
- Waste: Low-level to intermediate-level, 100 year decay to safe levels

Safety:
- Inherently safe: Plasma quenches if confinement lost (no chain reaction)
- Tritium inventory: <1 kg on-site (vs tons of fissile in fission reactor)
- No meltdown risk: No stored energy in fuel
- No prompt criticality: Fusion requires precise conditions, self-limiting

Path to Commercial Fusion:

ITER → DEMO → Commercial:
- ITER (2035-2045): Demonstrate Q=10, breeding, long pulses
- DEMO (2040-2050): First electricity-generating fusion plant, Q>25, continuous operation
- Commercial (2050+): Economic competitiveness, <$0.10/kWh, fleet deployment

Alternative Approaches:
- Stellarator (Wendelstein 7-X): Non-axisymmetric magnetic field, no induced current
- Inertial Confinement (NIF): Laser compression, achieved ignition 2022 but far from net electricity
- Compact designs: ARC (MIT), SPARC (Commonwealth Fusion), private ventures with high-field magnets

Advantages:
- Fuel: Deuterium from seawater (virtually unlimited), lithium for tritium breeding
- No CO₂ emissions
- No long-lived radioactive waste (100-year vs 10,000-year for fission)
- Inherent safety (self-quenching)

Challenges:
- Technical: Plasma control, materials, tritium breeding ratio >1
- Economic: ITER cost ~$25 billion, DEMO likely $15+ billion
- Timeline: Commercial power not before 2050-2060
- Competition: Fission, renewables, and storage improving rapidly
""",
        key_factors=[
            "Plasma beta (pressure/magnetic pressure ratio)",
            "Energy confinement time scaling (H-mode vs L-mode)",
            "First-wall heat flux management",
            "Tritium breeding ratio in blanket",
            "Disruption mitigation systems",
            "Divertor lifetime (erosion, thermal fatigue)"
        ],
        primary_authority=[
            "ITER Technical Basis (ITER EDA Documentation Series No. 24)",
            "Freidberg, Plasma Physics and Fusion Energy",
            "National Academies: Final Report of the Committee on a Strategic Plan for U.S. Burning Plasma Research (2019)"
        ],
        confidence=ConfidenceLevel.DISCLOSURE,
        reactor_scope=[ReactorType.FUSION]
    ),
]

# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class Telemetry:
    def __init__(self):
        self.query_count = 0
        self.total_latency_ms = 0.0
        self.doctrine_hits: Dict[str, int] = {}
        self.start_time = time.time()

    def record_query(self, latency_ms: float, doctrines: List[str]):
        self.query_count += 1
        self.total_latency_ms += latency_ms
        for doctrine in doctrines:
            self.doctrine_hits[doctrine] = self.doctrine_hits.get(doctrine, 0) + 1

    def get_avg_latency(self) -> float:
        return self.total_latency_ms / self.query_count if self.query_count > 0 else 0.0

    def get_uptime(self) -> float:
        return time.time() - self.start_time

telemetry = Telemetry()

# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

def normalize_query(query: str) -> str:
    """Normalize query for consistent matching."""
    return query.lower().strip()

def search_doctrines(query: str, top_k: int = 5) -> List[DoctrineBlock]:
    """Search doctrine cache for relevant blocks."""
    query_norm = normalize_query(query)
    query_tokens = set(query_norm.split())

    scored = []
    for doctrine in DOCTRINE_CACHE:
        keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_norm)
        token_overlap = len(query_tokens & set(kw.lower() for kw in doctrine.keywords))
        topic_match = 1 if any(word in doctrine.topic for word in query_tokens) else 0

        score = keyword_matches * 3 + token_overlap * 2 + topic_match * 5
        if score > 0:
            scored.append((score, doctrine))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [d for _, d in scored[:top_k]]

def build_response(query: str, mode: ResponseMode, doctrines: List[DoctrineBlock]) -> str:
    """Build response based on mode and triggered doctrines."""
    if not doctrines:
        return "No relevant nuclear energy expertise found for this query. Please refine your question to focus on reactor design, fuel cycles, radiation protection, waste management, NRC regulations, SMR technology, or fusion energy."

    if mode == ResponseMode.FAST:
        # Concise response
        primary = doctrines[0]
        response = f"{primary.conclusion_template}\n\n"
        response += f"Key factors: {', '.join(primary.key_factors[:3])}"
        return response

    elif mode == ResponseMode.DEFENSE:
        # Audit-ready with citations
        response = "NUCLEAR ENERGY ANALYSIS\n" + "="*60 + "\n\n"
        for i, doctrine in enumerate(doctrines[:3], 1):
            response += f"{i}. {doctrine.topic.upper()}\n"
            response += f"   {doctrine.conclusion_template}\n\n"
            response += f"   Key Technical Factors:\n"
            for factor in doctrine.key_factors[:4]:
                response += f"   • {factor}\n"
            response += f"\n   Primary Authority:\n"
            for auth in doctrine.primary_authority:
                response += f"   • {auth}\n"
            response += f"\n   Confidence: {doctrine.confidence.value}\n\n"
        return response

    else:  # MEMO
        # Comprehensive documentation
        response = "NUCLEAR ENERGY INTELLIGENCE ENGINE - TECHNICAL MEMORANDUM\n"
        response += "="*70 + "\n\n"
        response += f"SUBJECT: {query}\n"
        response += f"DATE: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n"
        response += f"ENGINE: {ENGINE_ID} v{VERSION}\n\n"

        response += "EXECUTIVE SUMMARY\n" + "-"*70 + "\n"
        response += f"{doctrines[0].conclusion_template}\n\n"

        response += "DETAILED ANALYSIS\n" + "-"*70 + "\n"
        for i, doctrine in enumerate(doctrines[:3], 1):
            response += f"\n{i}. {doctrine.topic.upper()}\n\n"
            response += f"Conclusion: {doctrine.conclusion_template}\n\n"
            response += f"Technical Reasoning:\n{doctrine.reasoning_framework}\n\n"
            response += f"Critical Factors:\n"
            for factor in doctrine.key_factors:
                response += f"  • {factor}\n"
            response += f"\nRegulatory/Technical Authority:\n"
            for auth in doctrine.primary_authority:
                response += f"  • {auth}\n"
            response += f"\nConfidence Assessment: {doctrine.confidence.value}\n"
            if doctrine.reactor_scope:
                response += f"Applicable Reactor Types: {', '.join(r.value for r in doctrine.reactor_scope)}\n"
            response += "\n" + "-"*70 + "\n"

        return response

def calculate_determinism_hash(query: str, answer: str, doctrines: List[str]) -> str:
    """Calculate SHA-256 hash for reproducibility verification."""
    content = f"{query}|{answer}|{','.join(sorted(doctrines))}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

def three_layer_response(query: str, mode: ResponseMode) -> QueryResponse:
    """TIE-20 Component: Three-layer response with doctrine cache."""
    start_time = time.time()

    # Layer 1: Doctrine Cache (0-50ms)
    doctrines = search_doctrines(query, top_k=5)

    # Layer 2: Semantic Retrieval (would integrate vector DB here)
    # For now, doctrine cache is sufficient

    # Layer 3: Deep Analysis (synthesize multiple doctrines)
    answer = build_response(query, mode, doctrines)

    # Determine overall confidence
    if doctrines:
        confidence = doctrines[0].confidence
    else:
        confidence = ConfidenceLevel.DISCLOSURE

    # Collect citations
    citations = []
    for d in doctrines[:3]:
        citations.extend(d.primary_authority)

    # Determinism hash
    doctrine_topics = [d.topic for d in doctrines]
    det_hash = calculate_determinism_hash(query, answer, doctrine_topics)

    latency_ms = (time.time() - start_time) * 1000
    telemetry.record_query(latency_ms, doctrine_topics)

    return QueryResponse(
        query=query,
        answer=answer,
        mode=mode,
        confidence=confidence,
        triggered_doctrines=doctrine_topics,
        authority_citations=list(set(citations)),
        latency_ms=round(latency_ms, 2),
        determinism_hash=det_hash
    )

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    description="Nuclear Energy Systems Intelligence Engine - TIE Gold Standard"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "engine": ENGINE_ID,
        "name": ENGINE_NAME,
        "version": VERSION,
        "status": "operational"
    }

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        uptime_seconds=round(telemetry.get_uptime(), 2),
        total_queries=telemetry.query_count,
        doctrine_count=len(DOCTRINE_CACHE),
        avg_latency_ms=round(telemetry.get_avg_latency(), 2)
    )

@app.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint."""
    try:
        logger.info(f"Query received: {request.query[:100]}... | Mode: {request.mode}")
        response = three_layer_response(request.query, request.mode)
        logger.info(f"Query completed: {len(response.triggered_doctrines)} doctrines, {response.latency_ms}ms")
        return response
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/doctrines", response_model=List[str])
async def list_doctrines():
    """List all doctrine topics."""
    return [d.topic for d in DOCTRINE_CACHE]

@app.get("/stats", response_model=Dict[str, Any])
async def get_stats():
    """Retrieve engine statistics."""
    return {
        "total_queries": telemetry.query_count,
        "avg_latency_ms": round(telemetry.get_avg_latency(), 2),
        "uptime_seconds": round(telemetry.get_uptime(), 2),
        "doctrine_count": len(DOCTRINE_CACHE),
        "top_doctrines": sorted(
            telemetry.doctrine_hits.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Doctrine cache loaded: {len(DOCTRINE_CACHE)} blocks")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
