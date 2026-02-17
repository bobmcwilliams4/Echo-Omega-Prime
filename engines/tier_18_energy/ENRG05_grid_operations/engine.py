"""
ENRG05 - Electrical Grid Operations & Power Systems Intelligence Engine
TIE Gold Standard - Power Grid Operations Expertise

Authority Level: EXPERT
Domain: Electrical Power Systems, Grid Operations, Transmission & Distribution
Version: 1.0.0
Port: 9085
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import time
from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ============================================================================
# ENUMERATIONS & DATA MODELS
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


class AuthorityLevel(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    TERTIARY = "TERTIARY"
    REFERENCE = "REFERENCE"


class IssueCategory(str, Enum):
    POWER_FUNDAMENTALS = "POWER_FUNDAMENTALS"
    TRANSMISSION = "TRANSMISSION"
    DISTRIBUTION = "DISTRIBUTION"
    TRANSFORMERS = "TRANSFORMERS"
    PROTECTION = "PROTECTION"
    SCADA_CONTROL = "SCADA_CONTROL"
    POWER_FLOW = "POWER_FLOW"
    FAULT_ANALYSIS = "FAULT_ANALYSIS"
    POWER_QUALITY = "POWER_QUALITY"
    VOLTAGE_REGULATION = "VOLTAGE_REGULATION"
    REACTIVE_COMPENSATION = "REACTIVE_COMPENSATION"
    ENERGY_STORAGE = "ENERGY_STORAGE"
    GRID_INTERCONNECTION = "GRID_INTERCONNECTION"
    RELIABILITY_STANDARDS = "RELIABILITY_STANDARDS"
    RENEWABLE_INTEGRATION = "RENEWABLE_INTEGRATION"


@dataclass
class DoctrineBlock:
    """Single doctrine block with complete reasoning framework"""
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: Optional[str] = None
    burden_holder: Optional[str] = None
    adversary_position: Optional[str] = None
    counter_arguments: List[str] = field(default_factory=list)
    resolution_strategy: Optional[str] = None
    entity_scope: Optional[str] = None
    issue_category: IssueCategory = IssueCategory.POWER_FUNDAMENTALS
    authority_level: AuthorityLevel = AuthorityLevel.PRIMARY


class QueryRequest(BaseModel):
    query: str = Field(..., description="Power grid question or analysis request")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    doctrine_blocks_triggered: List[str]
    reasoning_chain: List[str]
    authorities_cited: List[str]
    timestamp: str
    determinism_hash: str
    telemetry: Dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrine_count: int
    uptime_seconds: float
    total_queries: int
    avg_response_time_ms: float


# ============================================================================
# DOCTRINE CACHE - POWER GRID EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="AC Power Fundamentals - Three-Phase Systems",
        keywords=["three-phase", "AC power", "balanced load", "delta", "wye", "star connection", "line voltage", "phase voltage"],
        conclusion_template=[
            "Three-phase AC systems provide superior power delivery efficiency compared to single-phase.",
            "The relationship between line and phase quantities depends on connection type (wye vs delta).",
            "Balanced three-phase systems eliminate neutral current and optimize conductor utilization."
        ],
        reasoning_framework="""
Three-phase AC power is the backbone of modern electrical grids. In a wye (star) connection,
line voltage = √3 × phase voltage, while line current = phase current. In a delta connection,
line voltage = phase voltage, while line current = √3 × phase current. The √3 factor arises from
the 120° phase displacement between conductors.

Balanced three-phase loads draw equal current in all three phases with proper phase relationships,
resulting in zero neutral current. This allows smaller neutral conductors and eliminates neutral
harmonic issues. The instantaneous power in a balanced three-phase system is constant, eliminating
torque pulsations in motors and providing smooth power delivery.

Power calculations: P = √3 × VL × IL × cos(θ) for three-phase systems, where VL is line voltage,
IL is line current, and θ is the power factor angle. Reactive power Q = √3 × VL × IL × sin(θ).
Apparent power S = √3 × VL × IL. The power triangle relates P, Q, and S.
        """,
        key_factors=[
            "Phase displacement: 120° between conductors in three-phase systems",
            "Connection topology: Wye provides neutral point, delta provides phase-to-phase robustness",
            "Voltage/current relationships: √3 conversion factors depend on connection type",
            "Balanced operation: Equal loading across phases eliminates neutral current",
            "Power factor: Ratio of real to apparent power, critical for system efficiency",
            "Harmonic considerations: Balanced systems cancel triplen harmonics in line currents"
        ],
        primary_authority=[
            "IEEE Std 141 (Red Book) - Electric Power Distribution for Industrial Plants",
            "IEEE Std 399 (Brown Book) - Power Systems Analysis",
            "Grainger & Stevenson - Power System Analysis (textbook reference)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Fundamental electrical engineering principles with universal application",
        issue_category=IssueCategory.POWER_FUNDAMENTALS,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Power Factor and Reactive Power Management",
        keywords=["power factor", "reactive power", "VAR", "KVAR", "leading", "lagging", "capacitive", "inductive"],
        conclusion_template=[
            "Power factor below 0.95 indicates inefficient power utilization and increased system losses.",
            "Inductive loads (motors, transformers) require reactive power compensation for optimal operation.",
            "Utilities typically impose penalties for poor power factor, incentivizing correction."
        ],
        reasoning_framework="""
Power factor (PF) is the ratio of real power (kW) to apparent power (kVA): PF = P/S = cos(θ).
Industrial facilities typically have lagging power factor (0.7-0.9) due to inductive motor loads.
Low power factor increases current draw for the same real power, causing higher I²R losses in
conductors and transformers, reduced equipment capacity, and voltage drop issues.

Reactive power (Q) in KVAR represents the oscillating energy exchange between source and load.
Inductive loads (motors, transformers) consume reactive power (lagging PF), while capacitive
loads supply reactive power (leading PF). The relationship: S² = P² + Q², forming the power triangle.

Power factor correction involves adding capacitors to offset inductive VAR demand. For a load
drawing P kW at PF1, to improve to PF2: KVAR needed = P × (tan(θ1) - tan(θ2)). Over-correction
(leading PF) can cause voltage rise and resonance issues. Modern solutions include switched
capacitor banks, SVCs (Static VAR Compensators), and STATCOMs (Static Synchronous Compensators).
        """,
        key_factors=[
            "Economic impact: Utility demand charges and power factor penalties",
            "System efficiency: Higher PF reduces transmission losses and increases capacity",
            "Voltage stability: Reactive power affects voltage regulation throughout the grid",
            "Equipment sizing: Lower PF requires larger conductors and transformers",
            "Harmonics interaction: Capacitors can create resonance with system inductance",
            "Dynamic vs. static compensation: Switching speed and control requirements"
        ],
        primary_authority=[
            "IEEE Std 18 - Standard for Shunt Power Capacitors",
            "IEEE Std 1036 - Application Guide for Shunt Power Capacitors",
            "ANSI C84.1 - Voltage Ratings for Electric Power Systems"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established power system operational practice with clear engineering basis",
        issue_category=IssueCategory.REACTIVE_COMPENSATION,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Transmission System Voltage Levels - HV/EHV/UHV",
        keywords=["transmission voltage", "high voltage", "extra high voltage", "ultra high voltage", "230 kV", "500 kV", "765 kV"],
        conclusion_template=[
            "Higher transmission voltages enable lower losses and greater power capacity over long distances.",
            "Voltage level selection balances capital cost, right-of-way requirements, and transmission efficiency.",
            "North American transmission systems primarily use 115kV, 230kV, 345kV, 500kV, and 765kV."
        ],
        reasoning_framework="""
Transmission voltage selection is driven by power transfer requirements and distance. Power loss
in transmission lines: P_loss = I² × R. For constant power P = √3 × V × I × cos(θ), current
decreases linearly with voltage, making losses proportional to 1/V². Doubling voltage reduces
losses by 75% for the same power transfer.

Standard North American transmission voltages:
- High Voltage (HV): 115 kV, 138 kV, 161 kV (short-distance bulk transmission)
- Extra High Voltage (EHV): 230 kV, 345 kV, 500 kV (long-distance bulk transmission)
- Ultra High Voltage (UHV): 765 kV, 1000 kV+ (extremely long distances, limited deployment)

The trade-offs: Higher voltages require larger insulation clearances, more expensive equipment
(transformers, breakers, insulators), wider rights-of-way, and more complex protection schemes.
However, they enable power transfer across hundreds of miles with acceptable losses (typically
<3% per 100 miles at 500kV).

Corona discharge becomes significant above 230kV, causing radio interference and power loss.
Bundle conductors (multiple conductors per phase) reduce electric field gradient and mitigate
corona. EHV and UHV lines always use bundled conductors (2-8 per phase).
        """,
        key_factors=[
            "Economic breakpoint: Voltage selection based on power-distance product",
            "Loss minimization: I²R losses decrease with V² increase",
            "Equipment costs: Transformers, breakers, insulators scale exponentially with voltage",
            "Right-of-way width: Electrical clearances increase with voltage",
            "Stability limits: Higher voltages support greater angular stability margins",
            "Corona and EMF: Environmental and health considerations at EHV/UHV"
        ],
        primary_authority=[
            "NERC Transmission Planning Standards (TPL-001 through TPL-007)",
            "IEEE Std 1366 - Distribution Reliability Indices",
            "ANSI C84.1 - Voltage Ratings (transmission voltage classifications)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard transmission engineering practice based on fundamental physics and economic optimization",
        issue_category=IssueCategory.TRANSMISSION,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="HVDC Transmission Systems",
        keywords=["HVDC", "high voltage direct current", "VSC", "LCC", "converter station", "DC transmission"],
        conclusion_template=[
            "HVDC offers advantages for very long distance transmission, submarine cables, and asynchronous grid interconnection.",
            "Modern VSC-HVDC provides independent active and reactive power control with black-start capability.",
            "Economic breakeven distance for overhead HVDC vs HVAC is approximately 400-600 km."
        ],
        reasoning_framework="""
High Voltage Direct Current (HVDC) transmission eliminates skin effect, reactive power losses,
and capacitive charging current that limit AC transmission distance. HVDC systems use converter
stations at each end to transform AC to DC and back. Two main technologies:

1. Line-Commutated Converter (LCC): Thyristor-based, requires strong AC grid for commutation,
   consumes reactive power (~50% of transmitted power), lower cost per MW, proven for ±500kV to
   ±800kV bipolar systems. Examples: Pacific DC Intertie (±500kV, 3,100 MW).

2. Voltage Source Converter (VSC): IGBT-based, independent P and Q control, can feed weak/isolated
   grids, black-start capability, lower losses, compact footprint. Typical ratings: ±320kV to
   ±525kV, up to 2,000+ MW per bipole.

HVDC advantages: (1) Lower losses for distances >600 km, (2) Cable transmission >50 km (AC charging
current becomes prohibitive), (3) Asynchronous interconnection (linking 50Hz and 60Hz grids, or
grids with different stability characteristics), (4) No reactive compensation needed along route,
(5) Controllable power flow independent of AC system impedance.

HVDC disadvantages: High capital cost of converter stations ($300-500M each), complexity, need for
AC filters to handle harmonics, and single-point failure risk at converters.
        """,
        key_factors=[
            "Economic breakeven: HVDC competitive beyond 400-600 km overhead, 50+ km undersea",
            "Technology selection: LCC for bulk power, VSC for grid services and weak AC systems",
            "Reactive power: LCC consumes reactive power; VSC can supply or consume as needed",
            "Reliability: Bipolar systems allow single-pole operation at 50% capacity",
            "Harmonics: Both LCC and VSC generate harmonics requiring filtering",
            "Multi-terminal HVDC: VSC enables multi-terminal DC grids; LCC typically point-to-point"
        ],
        primary_authority=[
            "IEEE Std 1204 - Guide for Planning DC Links Terminating at AC Locations Having Low Short-Circuit Capacities",
            "CIGRE Technical Brochures on HVDC Transmission",
            "IEC 60633 - Terminology for HVDC Transmission"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Established HVDC technology with extensive operational history but evolving VSC capabilities",
        issue_category=IssueCategory.TRANSMISSION,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Distribution System Configurations - Radial, Loop, Network",
        keywords=["radial distribution", "loop feed", "network distribution", "primary distribution", "secondary distribution"],
        conclusion_template=[
            "Radial systems offer simplicity and low cost but lack redundancy for critical loads.",
            "Loop and network configurations provide improved reliability through alternate feed paths.",
            "Urban areas typically use network distribution; rural areas use radial feeders."
        ],
        reasoning_framework="""
Distribution system topology determines reliability, cost, and operational complexity:

1. Radial Distribution: Single path from substation to load. Advantages: Simple protection
   coordination, low cost, easy fault location. Disadvantages: Any fault upstream interrupts
   all downstream customers, typical SAIDI (System Average Interruption Duration Index) of
   100-300 minutes/year. Standard for rural and low-density suburban areas. Typical voltage:
   12.47kV or 13.8kV primary, 120/240V secondary.

2. Loop (Primary Loop): Feeder forms a loop with normally-open sectionalizing switches. During
   outages, switches reconfigure to restore service from alternate path. Reduces SAIDI to
   60-150 minutes/year. Common in suburban areas with moderate load density. Requires automated
   switching (reclosers, SCADA) for effective operation.

3. Network Distribution: Multiple primary feeders supply network transformers connected to a
   common secondary bus (typically 208Y/120V or 480Y/277V). Network protectors (reverse-power
   sensing breakers) on each transformer isolate faults while maintaining service. Provides
   highest reliability (SAIDI <30 minutes/year) but highest cost. Standard for dense urban
   areas (Manhattan, downtown cores).

Protection coordination complexity increases from radial (simple time-current coordination) to
network (directional relays, network protector logic, fault current contribution from multiple
sources).
        """,
        key_factors=[
            "Load density economics: Network justified above ~25 MVA/sq-mi; radial below ~5 MVA/sq-mi",
            "Reliability requirements: Critical loads demand redundancy via loop or network",
            "Fault current: Network systems have higher fault currents due to multiple sources",
            "Protection complexity: Network requires sophisticated directional and differential schemes",
            "Voltage regulation: Network inherently better due to multiple feed points",
            "Automation impact: Smart switches and SCADA make loop systems nearly as reliable as networks"
        ],
        primary_authority=[
            "IEEE Std 1366 - Distribution Reliability Indices",
            "IEEE Std 1547 - Interconnection and Interoperability of DER",
            "Rural Utilities Service (RUS) Bulletin 1724E-300 - Design Guide for Rural Distribution"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established distribution engineering practice with clear economic and reliability trade-offs",
        issue_category=IssueCategory.DISTRIBUTION,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Power Transformers - Design and Operation",
        keywords=["power transformer", "step-up", "step-down", "turns ratio", "impedance", "tap changer", "cooling"],
        conclusion_template=[
            "Transformer capacity is limited by thermal design; overload capability depends on cooling method and ambient conditions.",
            "Tap changers provide voltage regulation: DETC (de-energized) for seasonal adjustment, LTC (load tap changer) for dynamic control.",
            "Transformer impedance is critical for fault current limitation and parallel operation."
        ],
        reasoning_framework="""
Power transformers convert AC voltage levels via electromagnetic induction. Turns ratio determines
voltage transformation: V2/V1 = N2/N1. Current transforms inversely: I2/I1 = N1/N2 (neglecting
losses). Three-phase transformers use delta-wye, wye-wye, or delta-delta connections, each with
specific phase shift and grounding characteristics.

Transformer impedance (typically 5-15% on transformer MVA base) serves dual purposes: (1) Limits
fault current magnitude, and (2) Divides load between parallel transformers. Lower impedance
increases fault current but reduces voltage drop under load. Utilities typically specify
7.5-10% impedance for distribution transformers, 10-15% for transmission transformers.

Tap changers adjust turns ratio to regulate voltage: De-Energized Tap Changer (DETC) requires
outage, used for seasonal adjustment (±2.5% to ±5% in 16-32 steps). Load Tap Changer (LTC)
operates under load, provides dynamic voltage control (±10% in 32 steps typical), essential for
maintaining ANSI C84.1 voltage limits (±5% from nominal).

Cooling methods determine capacity: OA (Oil-immersed, Air-cooled, baseline), OA/FA (forced air,
+15% capacity), OA/FA/FA (+25%), OA/FA/FOA (forced oil, +33%). Transformers can tolerate
temporary overloads based on thermal time constant (hours) and pre-load history.
        """,
        key_factors=[
            "Impedance selection: Balance fault current limitation vs. voltage regulation",
            "Cooling system: Determines continuous rating and overload capability",
            "Tap changer type: LTC required for dynamic voltage control; DETC for static adjustment",
            "Insulation class: Temperature rise limits (55°C, 65°C, 80°C) determine capacity",
            "Load cycling: Transformers lose life exponentially with temperature above rated",
            "Parallel operation: Equal impedances required for proper load sharing"
        ],
        primary_authority=[
            "IEEE Std C57.12.00 - General Requirements for Liquid-Immersed Distribution, Power, and Regulating Transformers",
            "IEEE Std C57.91 - Loading Guide for Mineral-Oil-Immersed Transformers",
            "ANSI C84.1 - Voltage Ratings for Electric Power Systems"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Fundamental transformer engineering principles with comprehensive standards support",
        issue_category=IssueCategory.TRANSFORMERS,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Circuit Breaker Technologies - SF6, Vacuum, Oil",
        keywords=["circuit breaker", "SF6", "vacuum breaker", "oil breaker", "interrupting capacity", "arc extinction"],
        conclusion_template=[
            "SF6 breakers dominate transmission (>72.5kV) due to superior arc quenching and compact design.",
            "Vacuum breakers are standard for medium voltage (5-38kV) distribution applications.",
            "Interrupting capacity must exceed maximum available fault current with safety margin."
        ],
        reasoning_framework="""
Circuit breakers interrupt fault current by extinguishing the arc that forms when contacts open.
Three primary technologies for power system breakers:

1. SF6 (Sulfur Hexafluoride) Breakers: Gas blast extinguishes arc. Advantages: Excellent
   dielectric strength (2.5x air at same pressure), compact size, very high interrupting capacity
   (>63 kA symmetric), fast operation (2-3 cycles), minimal maintenance. Used for 72.5kV to 800kV.
   Disadvantage: SF6 is potent greenhouse gas (23,500x CO2); newer designs use sealed enclosures
   and recycling to minimize emissions.

2. Vacuum Breakers: Arc in high vacuum (<10⁻⁴ torr) extinguishes at current zero due to lack of
   ionizable medium. Standard for 5kV to 38kV distribution. Advantages: Long service life (20+ years,
   10,000+ operations), minimal maintenance, environmentally friendly. Limitations: Limited voltage
   range (<72.5kV economical), potential for chopping overvoltages on capacitive loads.

3. Oil Breakers: Arc decomposes oil, creating hydrogen bubble with high dielectric strength.
   Legacy technology being replaced by SF6 and vacuum. Advantages: Low cost, robust. Disadvantages:
   Fire hazard, maintenance-intensive, bulky, environmental concerns.

Interrupting capacity (Amperes RMS Asymmetrical) must exceed maximum fault current. Standards
require 1.3x safety factor. Fault current increases when generators are added or system impedance
reduces; breakers may require replacement even if voltage rating is adequate.
        """,
        key_factors=[
            "Voltage level: SF6 for transmission, vacuum for distribution",
            "Interrupting duty: Must exceed maximum prospective fault current",
            "Operating speed: Transmission faults require clearing in 3-8 cycles",
            "Maintenance: Vacuum requires minimal maintenance; SF6 requires gas monitoring",
            "Environmental: SF6 emissions a concern; vacuum and alternative gases (CO2 mixtures) emerging",
            "TRV (Transient Recovery Voltage): Breaker must withstand voltage recovery after arc extinction"
        ],
        primary_authority=[
            "IEEE Std C37.04 - Rating Structure for AC High-Voltage Circuit Breakers",
            "IEEE Std C37.06 - AC High-Voltage Circuit Breakers Rated on Symmetrical Current Basis",
            "IEC 62271-100 - High-voltage switchgear and controlgear"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Mature circuit breaker technology with extensive operational history and clear application guidelines",
        issue_category=IssueCategory.PROTECTION,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Protective Relaying - Overcurrent, Distance, Differential",
        keywords=["protective relay", "overcurrent", "distance relay", "differential", "51", "21", "87", "coordination"],
        conclusion_template=[
            "Overcurrent relays (51/51N) provide simple, cost-effective protection for radial distribution systems.",
            "Distance relays (21) protect transmission lines by measuring impedance to fault location.",
            "Differential relays (87) offer high-speed protection for transformers, generators, and buses."
        ],
        reasoning_framework="""
Protective relaying detects faults and initiates circuit breaker operation to isolate the faulted
section. Relay selection depends on system configuration, fault types, and speed requirements.

1. Overcurrent Relays (ANSI 51 - phase, 51N/51G - ground): Operate when current exceeds setpoint
   for specified time. Time-current curves (inverse, very inverse, extremely inverse) coordinate
   with upstream/downstream devices. Standard for radial distribution. Advantages: Simple,
   inexpensive, proven. Limitations: Cannot distinguish fault location; must coordinate with
   multiple devices; settings sensitive to system configuration changes.

2. Distance Relays (ANSI 21): Measure impedance (Z = V/I) to determine fault distance. Three zones:
   Zone 1 (instantaneous, 80-90% of line), Zone 2 (time-delayed, 120% to cover entire line plus
   margin), Zone 3 (backup, 200%+ for remote backup). Used on transmission lines >50 miles.
   Advantages: Not affected by source impedance changes, provides fault location information.
   Limitations: Complex settings, potential for misoperation on stable power swings (requires
   power swing blocking).

3. Differential Relays (ANSI 87): Compare current entering and leaving protected zone. For
   transformers (87T), buses (87B), or generators (87G). Operate when differential current
   (I_in - I_out) exceeds threshold. High-speed operation (1-2 cycles). Advantages: Absolute
   selectivity, high-speed, not affected by external faults. Limitations: Requires CTs at all
   terminals, expensive, complex CT ratio compensation for transformers.

Modern microprocessor relays combine multiple functions (51/51N/21/87/27/59/81) with communication
capability for synchrophasor, fault records, and wide-area protection schemes.
        """,
        key_factors=[
            "Selectivity: Fault isolation must be limited to smallest affected zone",
            "Speed: Transmission faults require clearing in 3-8 cycles for stability",
            "Coordination: Time-current curves must coordinate across cascaded devices",
            "Reliability: Redundant protection required for critical equipment",
            "CT accuracy: Protection CTs must remain accurate during fault (ANSI C class)",
            "Communication: Modern schemes use fiber, microwave, or power line carrier for pilot protection"
        ],
        primary_authority=[
            "IEEE Std C37.2 - Electrical Power System Device Function Numbers",
            "IEEE Std C37.113 - Guide for Protective Relay Applications to Transmission Lines",
            "IEEE Std C37.91 - Guide for Protecting Power Transformers"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established protective relaying principles with comprehensive application guides",
        issue_category=IssueCategory.PROTECTION,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="SCADA and Energy Management Systems",
        keywords=["SCADA", "EMS", "RTU", "supervisory control", "state estimation", "AGC", "economic dispatch"],
        conclusion_template=[
            "SCADA provides real-time monitoring and control of transmission and distribution systems.",
            "Energy Management Systems (EMS) add advanced functions: state estimation, optimal power flow, contingency analysis.",
            "Cybersecurity is critical; NERC CIP standards mandate protection of control systems."
        ],
        reasoning_framework="""
SCADA (Supervisory Control and Data Acquisition) systems form the operational backbone of electric
grids. Architecture: Remote Terminal Units (RTUs) at substations collect data (voltages, currents,
breaker status, transformer taps) and execute control commands. Communication to central control
via fiber, microwave, or cellular (DNP3, IEC 61850, or Modbus protocols). Update rate: 2-10 seconds
for transmission SCADA, 15-60 seconds for distribution.

Energy Management System (EMS) applications run on top of SCADA data:

1. State Estimation: Calculates best estimate of system state (voltages, flows) from redundant
   measurements using weighted least squares. Detects bad data and topology errors. Foundation
   for all other EMS functions.

2. Contingency Analysis: Simulates N-1 and N-2 contingencies (loss of one or two elements) to
   verify system can survive credible outages without violating thermal or voltage limits.
   Required by NERC TPL standards.

3. Optimal Power Flow (OPF): Determines generator dispatch to minimize cost while satisfying
   load and network constraints. Considers generator costs, transmission losses, and voltage/
   thermal limits. Runs every 5-15 minutes.

4. Automatic Generation Control (AGC): Adjusts generator output in real-time to maintain frequency
   and scheduled interchange. Target: ±0.036 Hz from 60.000 Hz (NERC BAL-001-2).

Cybersecurity: NERC CIP (Critical Infrastructure Protection) standards CIP-002 through CIP-014
mandate security controls including network segmentation, access controls, incident response,
and personnel training. SCADA networks must be isolated from corporate IT networks.
        """,
        key_factors=[
            "Data quality: State estimation requires redundant measurements for reliability",
            "Update rate: SCADA must provide timely data for operator decision-making",
            "Communication reliability: Redundant paths required for critical RTUs",
            "Cybersecurity: Defense-in-depth with network segmentation, firewalls, intrusion detection",
            "Human factors: Operator interface design critical for situational awareness",
            "Integration: EMS must coordinate with DMS (Distribution Management System) and market systems"
        ],
        primary_authority=[
            "IEEE Std 1379 - Data Acquisition and Control (SCADA) Systems",
            "NERC CIP-002 through CIP-014 - Critical Infrastructure Protection Standards",
            "IEC 61850 - Communication Networks and Systems for Power Utility Automation"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established SCADA/EMS technology with evolving cybersecurity requirements",
        issue_category=IssueCategory.SCADA_CONTROL,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Load Flow Analysis - Power System Planning",
        keywords=["load flow", "power flow", "AC power flow", "Newton-Raphson", "bus voltages", "line flows"],
        conclusion_template=[
            "Load flow analysis determines steady-state voltages, currents, and power flows throughout the network.",
            "Newton-Raphson is the standard iterative method for solving the nonlinear power flow equations.",
            "Results identify voltage violations, overloaded equipment, and system losses under various conditions."
        ],
        reasoning_framework="""
Load flow (power flow) analysis solves the nonlinear algebraic equations governing AC power systems
in steady state. For each bus i: P_i = Σ |V_i||V_k|Y_ik cos(θ_i - θ_k - α_ik) and
Q_i = Σ |V_i||V_k|Y_ik sin(θ_i - θ_k - α_ik), summing over all connected buses k.

Bus classifications:
- PQ Bus (Load): P and Q specified, solve for V and θ (most buses)
- PV Bus (Generator): P and V specified, solve for Q and θ (generator buses)
- Slack/Swing Bus: V and θ specified (θ=0 reference), solves for P and Q (balances system)

Newton-Raphson method solves iteratively using Jacobian matrix [∂P/∂θ, ∂P/∂V; ∂Q/∂θ, ∂Q/∂V].
Convergence in 3-7 iterations typical for well-conditioned systems. Gauss-Seidel and Fast
Decoupled methods are alternatives (slower convergence but simpler).

Load flow reveals: (1) Bus voltage magnitudes (must stay within ±5% per ANSI C84.1), (2) Line
and transformer loadings (must stay below thermal ratings), (3) Generator reactive power
requirements (must stay within capability curves), (4) System losses (I²R losses in all elements).

Planning engineers run hundreds of load flow scenarios: peak load, light load, contingencies
(N-1, N-2), generator dispatch patterns, renewable generation profiles. Modern software
(PowerWorld, PSS/E, PSLF) automates batch runs and visualization.
        """,
        key_factors=[
            "Convergence: Ill-conditioned systems may fail to converge (voltage collapse, islanding)",
            "Accuracy: Load and generation data accuracy critical for meaningful results",
            "Contingency analysis: N-1 (single element outage) is minimum standard; N-2 for critical systems",
            "Voltage limits: ANSI C84.1 Range A (±5%) must be maintained",
            "Thermal limits: Summer vs winter ratings differ due to ambient temperature",
            "Losses: Total system losses typically 3-7%; transmission 1-3%, distribution 2-4%"
        ],
        primary_authority=[
            "IEEE Std 399 (Brown Book) - Power System Analysis",
            "NERC TPL-001-5 - Transmission System Planning Performance Requirements",
            "ANSI C84.1 - Voltage Ratings for Electric Power Systems"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Fundamental power system analysis technique with extensive validation and practical application",
        issue_category=IssueCategory.POWER_FLOW,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Fault Analysis - Symmetrical and Asymmetrical Faults",
        keywords=["short circuit", "fault current", "symmetrical fault", "line-to-ground", "line-to-line", "three-phase fault"],
        conclusion_template=[
            "Three-phase symmetrical faults produce highest fault current but are least common (~5% of faults).",
            "Single line-to-ground faults are most common (~70-80%) but produce lower fault current in most systems.",
            "Fault current magnitude determines breaker interrupting requirements and relay settings."
        ],
        reasoning_framework="""
Power system faults are categorized as symmetrical (three-phase) or asymmetrical (single line-to-ground,
line-to-line, double line-to-ground). Analysis uses symmetrical components: positive sequence
(normal balanced operation), negative sequence (phase imbalance), zero sequence (ground current return).

Symmetrical Three-Phase Fault: All three phases short together. Highest fault current (only
positive sequence network active): I_fault = V / (Z_source + Z_line). Simplest analysis but
rare (~5% of faults). Used for breaker sizing since it represents maximum duty.

Asymmetrical Faults:
1. Single Line-to-Ground (SLG): 70-80% of faults. Current magnitude depends heavily on grounding.
   For solidly grounded systems: I_f = 3 × V / (Z1 + Z2 + Z0). If Z0 >> Z1+Z2 (low zero-sequence
   path), SLG current may be lower than three-phase fault.

2. Line-to-Line (L-L): 15-20% of faults. I_f = V / (Z1 + Z2). No zero sequence (no ground path).
   Magnitude ~87% of three-phase fault.

3. Double Line-to-Ground (LLG): 5-10% of faults. Most complex analysis; may exceed three-phase
   fault in certain system configurations (low Z0).

DC component decays with time constant L/R (typically 30-100ms). Peak asymmetrical current
(first cycle) = √2 × 1.6 × symmetrical RMS for X/R ratio of 15-20 (typical). Breakers and
relays must handle asymmetrical duty.
        """,
        key_factors=[
            "Fault statistics: SLG 70-80%, LL 15-20%, three-phase ~5%",
            "Grounding impact: Solidly grounded systems have higher SLG current than resistance-grounded",
            "X/R ratio: Higher X/R increases DC offset and asymmetrical peak current",
            "Breaker rating: Must interrupt symmetrical current but withstand asymmetrical momentary",
            "System changes: Adding generators or reducing impedance increases fault current",
            "Arc flash hazard: Fault current determines incident energy (NFPA 70E, IEEE 1584)"
        ],
        primary_authority=[
            "IEEE Std 141 (Red Book) - Electric Power Distribution for Industrial Plants",
            "IEEE Std 399 (Brown Book) - Power System Analysis",
            "IEEE Std 551 - Calculating Short-Circuit Currents in Industrial and Commercial Power Systems"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established fault analysis methodology based on symmetrical components theory",
        issue_category=IssueCategory.FAULT_ANALYSIS,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Power Quality - Harmonics, Sag, Swell, Flicker",
        keywords=["harmonics", "THD", "voltage sag", "voltage swell", "flicker", "power quality", "transients"],
        conclusion_template=[
            "Harmonics from nonlinear loads cause equipment heating, nuisance tripping, and communication interference.",
            "Voltage sags (0.1 to 0.9 pu for 0.5 cycles to 1 minute) are the most common power quality problem.",
            "IEEE 519 limits harmonic distortion: THD < 5% for voltage, varying current limits based on system strength."
        ],
        reasoning_framework="""
Power quality disturbances cause equipment malfunction, reduced efficiency, and premature failure.
Key categories:

1. Harmonics: Frequencies that are integer multiples of fundamental (60Hz). Sources: Variable
   frequency drives (VFDs), switch-mode power supplies, LED lighting, arc furnaces. Effects:
   Transformer heating (eddy current losses scale with frequency²), neutral overloading (triplen
   harmonics add in neutral), motor heating, capacitor failure (XC decreases with frequency,
   increasing current). IEEE 519 limits: Voltage THD <5% at PCC (point of common coupling),
   current THD limits based on ISC/IL ratio (stronger systems have tighter limits).

2. Voltage Sag (Dip): Reduction to 0.1-0.9 pu for 0.5 cycles to 1 minute. Causes: Faults on
   utility system, motor starting, transformer energizing. Effects: Nuisance tripping of
   adjustable speed drives, computer resets, lighting flicker, contactor dropout. Most common
   power quality complaint. Mitigation: Voltage regulators, UPS, DVR (Dynamic Voltage Restorer).

3. Voltage Swell: Increase to 1.1-1.8 pu for 0.5 cycles to 1 minute. Causes: Single line-to-ground
   faults (unfaulted phases rise), sudden load rejection, incorrect tap settings. Effects:
   Equipment damage if sustained, insulation stress.

4. Flicker: Rapid voltage fluctuations (<5%) at 1-30 Hz causing visible light intensity changes.
   Sources: Arc furnaces, welders, large motor starting. Human eye most sensitive at 8-10 Hz.
   IEC 61000-4-15 defines Pst (short-term severity) <1.0 acceptable.

5. Transients: Microsecond to millisecond overvoltages (up to 3-5 pu). Sources: Lightning,
   switching, capacitor energizing. Mitigation: Surge arresters, transient voltage surge
   suppressors (TVSS).
        """,
        key_factors=[
            "Harmonic sources: VFDs, SMPS, LED drivers proliferating with energy efficiency push",
            "IEEE 519 compliance: Responsibility split between utility (voltage) and customer (current)",
            "Sag immunity: Critical loads need ride-through capability (UPS, DVR, energy storage)",
            "Resonance: Capacitors and system inductance create parallel resonance at harmonic frequencies",
            "Measurement: Power quality analyzers capture events per IEEE 1159 classifications",
            "Economic impact: Poor power quality costs U.S. industry $100B+ annually"
        ],
        primary_authority=[
            "IEEE Std 519 - Harmonic Control in Electric Power Systems",
            "IEEE Std 1159 - Monitoring Electric Power Quality",
            "IEEE Std 1346 - Electronic Equipment Response to Power Quality Disturbances"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Mature power quality standards with extensive measurement data and established mitigation techniques",
        issue_category=IssueCategory.POWER_QUALITY,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Voltage Regulation - Tap Changers, Regulators, Capacitors",
        keywords=["voltage regulation", "LTC", "voltage regulator", "capacitor bank", "ANSI C84.1", "voltage drop"],
        conclusion_template=[
            "ANSI C84.1 requires voltage within ±5% of nominal (Range A) for proper equipment operation.",
            "Load tap changers (LTCs) on substation transformers provide primary voltage control.",
            "Distribution voltage regulators and switched capacitors provide secondary control closer to loads."
        ],
        reasoning_framework="""
Voltage regulation maintains voltage within acceptable limits despite varying load and generation.
ANSI C84.1 defines Range A: ±5% from nominal (114-126V for 120V base) for normal operation.
Range B (±10%) allowed for emergency conditions.

Transmission voltage regulation: Generator automatic voltage regulators (AVRs) maintain terminal
voltage setpoint by adjusting excitation. Transmission system voltage controlled by generator
reactive power output, switched shunt capacitors/reactors, and SVCs/STATCOMs. Target: ±5% at
bulk delivery points.

Distribution voltage regulation hierarchy:
1. Substation LTC: Load tap changer on distribution transformer adjusts secondary voltage (typically
   ±10% in 32 steps of 0.625% each). Set to maintain feeder voltage at substation within narrow
   band (122-124V on 120V base). Operates 1-5 times per day following load variations.

2. Line Voltage Regulators: Single-phase or three-phase step-voltage regulators installed mid-feeder
   (±10% range, 32 steps). Used on long rural feeders where voltage drop exceeds LTC range. Each
   regulator has line drop compensation (LDC) to simulate voltage at a point downstream.

3. Switched Capacitor Banks: Installed throughout distribution system to provide reactive power
   support, reducing I²X voltage drop. Fixed or switched (time-clock, voltage-controlled, or
   VAR-controlled). Typical sizes: 300-1200 KVAR per bank.

Voltage drop calculation: V_drop = I × (R cos θ + X sin θ) for single-phase, or √3 × I × (R cos θ + X sin θ)
for three-phase. On distribution feeders (X/R ≈ 1-2), both resistive and reactive components matter.

Advanced schemes: Conservation Voltage Reduction (CVR) intentionally lowers voltage to reduce energy
consumption (1% voltage reduction ≈ 0.7-0.8% energy reduction). Requires coordinated control of
LTCs, regulators, and capacitors via SCADA.
        """,
        key_factors=[
            "ANSI C84.1 Range A: ±5% mandatory for normal operation",
            "Coordination: LTC, regulators, and capacitors must coordinate to avoid hunting",
            "Line drop compensation: Regulators compensate for impedance to load center",
            "Capacitor switching: Transients must be limited (back-to-back switching, pre-insertion resistors)",
            "Smart inverters: IEEE 1547-2018 allows DER to provide voltage support",
            "AMI integration: Smart meters enable real-time visibility of customer voltage"
        ],
        primary_authority=[
            "ANSI C84.1 - Voltage Ratings for Electric Power Systems",
            "IEEE Std C57.15 - Requirements, Terminology, and Test Code for Step-Voltage Regulators",
            "IEEE Std 1547 - Interconnection and Interoperability of DER"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established voltage regulation practice with clear standards and proven control strategies",
        issue_category=IssueCategory.VOLTAGE_REGULATION,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="NERC Reliability Standards - Compliance Requirements",
        keywords=["NERC", "reliability standards", "CIP", "TPL", "BAL", "compliance", "transmission planning"],
        conclusion_template=[
            "NERC reliability standards are mandatory and enforceable with penalties up to $1M per day per violation.",
            "TPL standards require N-1 and N-2 contingency analysis to ensure system can survive credible outages.",
            "CIP standards mandate cybersecurity controls for critical cyber assets."
        ],
        reasoning_framework="""
North American Electric Reliability Corporation (NERC) develops and enforces mandatory reliability
standards for the bulk electric system (BES). Key standard families:

1. Transmission Planning (TPL-001 through TPL-007): Require planning assessment demonstrating system
   can withstand contingencies without violating thermal, voltage, or stability limits. N-1 (single
   element outage) is baseline; N-2 (simultaneous loss of two elements) required for critical paths.
   Annual planning assessment plus real-time operational assessments. Must consider 1-year, 5-year,
   and 10-year horizons.

2. Balancing Authority (BAL): Control frequency and interchange. BAL-001-2 (Real Power Balancing
   Control Performance) requires ACE (Area Control Error) to meet CPS1 (Control Performance Standard 1,
   12-month average ≥ 100%) and CPS2 (10-minute average ACE within L10 for ≥90% of periods).
   BAL-003-1 requires frequency response sufficient to arrest decline within first few seconds
   of large generation loss.

3. Critical Infrastructure Protection (CIP-002 through CIP-014): Cybersecurity requirements.
   CIP-002 identifies critical cyber assets. CIP-003 through CIP-009 mandate security management,
   personnel training, electronic security perimeter, physical security, system security management,
   incident response, and recovery plans. CIP-013 addresses supply chain risk. Violations carry
   severe penalties ($1M/day maximum).

4. Facility Ratings (FAC-008, FAC-009): Require documented methodology for facility ratings (thermal,
   voltage, stability). Actual loading must remain below ratings.

5. Vegetation Management (FAC-003): Requires transmission line clearances to prevent flashovers
   from tree contact (major cause of cascading outages).

Regional entities (WECC, SERC, MRO, etc.) may have additional regional standards. Compliance
audits conducted every 3-6 years; self-certifications and spot checks in between.
        """,
        key_factors=[
            "Mandatory compliance: FERC-approved standards enforceable by law",
            "Severe penalties: Violations can result in $1M per day per violation",
            "N-1 / N-2 contingency: System must survive single and dual element outages",
            "CIP cybersecurity: Defense-in-depth required for critical assets",
            "Documentation: Extensive evidence required to demonstrate compliance",
            "Regional variations: Some regions have stricter standards than NERC baseline"
        ],
        primary_authority=[
            "NERC Reliability Standards (TPL, BAL, CIP, FAC families)",
            "FERC Order 888, 2000 - Transmission access and reliability",
            "Regional Reliability Standards (WECC, SERC, MRO, etc.)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Legally enforceable standards with clear requirements and established audit processes",
        issue_category=IssueCategory.RELIABILITY_STANDARDS,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Grid Interconnection - IEEE 1547 for Distributed Energy Resources",
        keywords=["IEEE 1547", "DER", "interconnection", "distributed generation", "anti-islanding", "grid support"],
        conclusion_template=[
            "IEEE 1547-2018 establishes technical requirements for interconnecting distributed energy resources to the grid.",
            "Anti-islanding protection is mandatory to prevent energizing isolated grid sections during utility outages.",
            "Modern DER inverters provide grid support functions: voltage/frequency ride-through, active/reactive power control."
        ],
        reasoning_framework="""
IEEE 1547 "Standard for Interconnection and Interoperability of Distributed Energy Resources with
Associated Electric Power Systems Interfaces" governs interconnection of solar PV, wind, energy
storage, and other DER. 2018 revision represents major update from 2003 version.

Key 1547-2018 requirements:

1. Voltage/Frequency Ride-Through: DER must remain online during grid disturbances (replaces
   previous "trip immediately" philosophy). Continuous operation range: 88-110% voltage, 59.3-60.5 Hz.
   Mandatory operation zones for temporary excursions (e.g., 70-88% voltage for 2-10 seconds).
   Helps maintain grid stability during disturbances.

2. Active Power Control: Inverters must support frequency-watt (reduce output during over-frequency),
   volt-watt (reduce output during overvoltage), and ramp rate limiting. Enables DER to provide
   frequency response similar to synchronous generators.

3. Reactive Power Control: Volt-VAR mode for voltage regulation, fixed power factor, or fixed
   VAR output. Inverters can provide/absorb reactive power within capability curve (typically
   0.85 lagging to 0.85 leading at full real power, increasing to ±100% VAR at zero real power).

4. Anti-Islanding: Inverter must detect loss of utility grid and cease energizing within 2 seconds.
   Methods: Under/over voltage/frequency, rate-of-change of frequency, impedance measurement,
   transfer trip. Prevents safety hazard to utility workers and equipment damage.

5. Interoperability: IEEE 2030.5 communication protocol for advanced functions (dynamic operating
   envelopes, pricing response, grid services).

Interconnection process: Application → initial review → detailed study (if needed) → agreement →
commissioning test. Timelines vary by utility and system size (weeks for residential, months/years
for utility-scale).
        """,
        key_factors=[
            "Paradigm shift: From 'disconnect on disturbance' to 'ride through and support'",
            "Grid services: Modern inverters can provide voltage/frequency regulation",
            "Safety: Anti-islanding remains critical despite ride-through requirements",
            "Hosting capacity: Distribution circuits have limits on DER before voltage issues arise",
            "Interoperability: IEEE 2030.5 enables utility dispatch of DER for grid services",
            "Screening: Fast-track interconnection available for systems passing simplified screens"
        ],
        primary_authority=[
            "IEEE Std 1547-2018 - Interconnection and Interoperability of DER",
            "IEEE Std 1547.1 - Conformance Test Procedures for Equipment Interconnecting DER",
            "UL 1741 - Inverters, Converters, Controllers for Use in Independent Power Systems"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Recently updated standard (2018) with extensive industry consensus and emerging operational experience",
        issue_category=IssueCategory.GRID_INTERCONNECTION,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Energy Storage - Battery, Pumped Hydro, Flywheel",
        keywords=["energy storage", "battery storage", "pumped hydro", "flywheel", "BESS", "grid-scale storage"],
        conclusion_template=[
            "Pumped hydro storage provides 95%+ of global grid-scale storage (170+ GW) but requires specific geography.",
            "Lithium-ion battery storage is growing rapidly (50+ GW globally) with 1-4 hour duration typical.",
            "Energy storage provides multiple grid services: peak shaving, frequency regulation, renewable integration, black start."
        ],
        reasoning_framework="""
Energy storage technologies vary widely in duration, power rating, efficiency, and cost:

1. Pumped Hydro Storage (PHS): Water pumped uphill during low-demand periods, released through
   turbines during peak demand. Characteristics: 100 MW to 3,000 MW capacity, 4-24 hour duration,
   70-85% round-trip efficiency, >50 year lifespan, low cost per MWh stored ($50-100/kWh).
   Limitations: Geography-dependent (needs elevation difference, water supply), long permitting/
   construction (10+ years), environmental concerns. Dominates global storage: ~170 GW installed,
   95% of grid storage capacity.

2. Lithium-Ion Battery Energy Storage Systems (BESS): Grid-scale installations using Li-ion
   batteries (same chemistry as EVs). Characteristics: 10 MW to 400+ MW, 1-4 hour duration typical,
   85-95% round-trip efficiency, 10-15 year lifespan, declining costs ($200-400/kWh installed).
   Advantages: Fast response (<100ms), modular, can be sited anywhere, no emissions. Applications:
   Frequency regulation, peak shaving, renewable firming, transmission deferral. Rapid growth:
   50+ GW installed globally as of 2024.

3. Flywheel Energy Storage: Rotating mass stores kinetic energy (E = ½Iω²). Characteristics:
   1-20 MW, seconds to minutes duration, >90% efficiency, 20+ year lifespan, very high cycle life
   (millions of cycles). Applications: Frequency regulation, UPS, power quality. Limited deployment
   due to high $/kWh for longer duration.

4. Other Technologies: Compressed Air Energy Storage (CAES, 2 facilities globally), liquid air,
   thermal storage, hydrogen. Various stages of commercial deployment.

Grid services provided by storage: (1) Frequency regulation (ACE/AGC response), (2) Spinning reserve
(replace lost generation), (3) Peak shaving (reduce demand charges), (4) Renewable integration
(time-shift solar/wind), (5) Transmission/distribution deferral (delay infrastructure upgrades),
(6) Black start (restore grid after blackout), (7) Voltage support (reactive power injection).
        """,
        key_factors=[
            "Economics: Declining battery costs making 4-hour systems competitive with peakers",
            "Duration: Batteries excel at 1-4 hours; pumped hydro for 6-24 hours",
            "Cycle life: Battery degradation limits lifetime cycles; pumped hydro has unlimited cycles",
            "Response speed: Batteries can respond in milliseconds; pumped hydro in seconds to minutes",
            "ITC/PTC: Federal tax credits (30% ITC for standalone storage) improving economics",
            "Fire safety: Li-ion thermal runaway risk requires UL 9540A testing and NFPA 855 compliance"
        ],
        primary_authority=[
            "IEEE Std 2030.2 - Guide for Design, Operation, and Maintenance of Battery Energy Storage Systems",
            "NFPA 855 - Installation of Stationary Energy Storage Systems",
            "UL 9540 - Energy Storage Systems and Equipment"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Rapidly evolving technology with established practices for pumped hydro but emerging standards for batteries",
        issue_category=IssueCategory.ENERGY_STORAGE,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Renewable Integration Challenges - Variability and Inverter Dynamics",
        keywords=["renewable integration", "solar variability", "wind variability", "inverter-based resources", "grid-following", "grid-forming"],
        conclusion_template=[
            "High renewable penetration creates challenges: reduced system inertia, voltage regulation complexity, frequency control issues.",
            "Grid-following inverters require strong grid for synchronization; grid-forming inverters can operate in weak grids or islanded mode.",
            "NERC warns that >75% instantaneous renewable penetration may threaten stability without mitigation measures."
        ],
        reasoning_framework="""
Renewable energy (solar PV, wind) differs fundamentally from synchronous generators, creating
integration challenges as penetration increases:

1. Variability and Uncertainty: Solar output varies with clouds (seconds to minutes), diurnal
   cycle (zero at night), and seasonal patterns. Wind varies with weather fronts (hours), diurnal
   patterns, and seasonal trends. Forecasting essential for grid operations: day-ahead forecasts
   for unit commitment, hour-ahead for dispatch, 5-minute-ahead for regulation. Forecast errors
   require flexible reserves (fast-start gas turbines, storage, demand response).

2. Reduced System Inertia: Synchronous generators provide rotational inertia (stored energy in
   spinning mass) that resists frequency changes: df/dt = (P_gen - P_load) / (2H), where H is
   system inertia constant. Inverter-based renewables provide zero physical inertia (unless
   synthetic inertia is programmed). Low inertia causes faster frequency deviations during
   disturbances, potentially triggering under-frequency load shedding before governors can respond.
   Mitigation: Require inverters to emulate inertia (synthetic inertia via fast active power
   injection), maintain minimum synchronous generation online, deploy fast frequency response
   from batteries.

3. Inverter Dynamics vs. Synchronous Machine Dynamics: Traditional grid-following inverters use
   Phase-Locked Loop (PLL) to synchronize with grid voltage; require strong voltage source (short
   circuit ratio >3). High inverter penetration creates weak grid (low SCR), leading to voltage
   instability and inverter trips during faults. Grid-forming inverters create voltage reference
   internally, can operate in weak grids or islanded mode. Transition to grid-forming is critical
   for >60% renewable penetration.

4. Voltage Regulation: Large utility-scale solar plants (100-500 MW) can cause significant voltage
   swings. IEEE 1547-2018 requires volt-VAR control, but coordination with utility voltage
   regulation equipment (LTCs, capacitors) is complex. Cloud transients can cause voltage
   fluctuations exceeding ANSI C84.1 Range A.

5. Protection Coordination: Inverters have limited fault current contribution (1.1-1.2x rated
   current typical), unlike synchronous machines (5-10x). Traditional overcurrent relays may
   not detect faults in high-DER circuits. Requires adaptive protection or microprocessor relays
   with directional/communication elements.
        """,
        key_factors=[
            "Inertia decline: System inertia decreasing as coal/nuclear retire and renewables grow",
            "Minimum synchronous generation: May need to curtail renewables to maintain stability",
            "Grid-forming capability: Essential for grids targeting >60% instantaneous renewables",
            "Forecasting: Accuracy critical for economic dispatch and reliability",
            "Transmission congestion: Renewable-rich areas often lack transmission to load centers",
            "Duck curve: California's load-net-renewables curve showing steep evening ramp"
        ],
        primary_authority=[
            "NERC Special Report - Integrating Inverter-Based Resources into Low Short Circuit Strength Systems",
            "IEEE Task Force Report - Impact of Inverter-Based Generation on Bulk Power System Dynamics",
            "CAISO Special Report - Managing Oversupply and the Duck Curve"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Emerging challenges with evolving mitigation strategies; field experience accumulating rapidly",
        issue_category=IssueCategory.RENEWABLE_INTEGRATION,
        authority_level=AuthorityLevel.SECONDARY
    ),

    DoctrineBlock(
        topic="Microgrid Operation - Islanded and Grid-Connected Modes",
        keywords=["microgrid", "islanding", "grid-connected", "black start", "seamless transition", "microgrid controller"],
        conclusion_template=[
            "Microgrids can operate grid-connected or islanded, providing resilience during utility outages.",
            "Seamless transition between modes requires sophisticated control and energy storage for frequency/voltage stabilization.",
            "Military bases, hospitals, and campuses increasingly deploy microgrids for critical load resilience."
        ],
        reasoning_framework="""
A microgrid is a localized group of distributed energy resources (DER), loads, and storage that
can operate connected to the main grid or islanded. Key characteristics and operational modes:

Grid-Connected Mode: Microgrid operates as part of utility grid. DER may reduce net import, provide
reactive power support, or export excess generation. Grid provides frequency and voltage reference.
Microgrid controller optimizes economics (peak shaving, demand response, energy arbitrage with storage).

Islanded Mode: Microgrid disconnects from utility at Point of Common Coupling (PCC) and operates
independently. Requires local generation to balance load, energy storage to buffer transients,
and sophisticated control to maintain frequency (60.00 Hz ±0.05 Hz target) and voltage (±5% per
ANSI C84.1). One or more inverters must operate in grid-forming mode to establish voltage reference.

Transition (Grid-Connected ↔ Islanded): Two approaches:
1. Seamless Transition: Microgrid controller detects utility disturbance, pre-synchronizes island
   sources, opens PCC breaker without interruption. Requires energy storage to buffer mismatch
   between generation and load during first 1-2 seconds. Most sophisticated approach.

2. Non-Seamless (Black Start): Utility loss causes brief outage, microgrid controller performs
   black start sequence (energize critical loads step-by-step to avoid inrush overload). Simpler
   but involves 5-60 second interruption.

Microgrid Controller: Coordinates DER dispatch, storage charging/discharging, load shedding (if
generation insufficient), and PCC breaker control. Typically hierarchical: (1) Primary control
(droop or virtual synchronous machine for load sharing), (2) Secondary control (restore frequency/
voltage to nominal), (3) Tertiary control (economic optimization).

Applications: Military bases (energy security), hospitals (critical load resilience), campuses
(cost savings + sustainability), remote communities (cost-effective vs. long utility feeders),
industrial facilities (power quality, reliability).

Standards: IEEE 2030.7 (microgrid controller specification), IEEE 1547.4 (guide for design,
operation, and integration), UL 1741 SA (inverter certification including microgrid functions).
        """,
        key_factors=[
            "Resilience value: Difficult to quantify but critical for hospitals, data centers, military",
            "Energy storage essential: Buffers generation-load mismatch during transitions and islands",
            "Control complexity: Seamless transition requires fast (<1 second) sophisticated control",
            "Black start capability: Microgrid must start from zero grid voltage using local resources",
            "Load prioritization: Shed non-critical loads if generation insufficient in island mode",
            "Economics: Microgrids expensive ($2,000-5,000/kW) unless resilience value is high"
        ],
        primary_authority=[
            "IEEE Std 2030.7 - Standard for Specification of Microgrid Controllers",
            "IEEE Std 1547.4 - Guide for Design, Operation, and Integration of DER Island Systems",
            "DOE Microgrid Exchange Group - Best Practices and Case Studies"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Emerging technology with rapidly evolving standards and increasing field deployments",
        issue_category=IssueCategory.GRID_INTERCONNECTION,
        authority_level=AuthorityLevel.SECONDARY
    ),

    DoctrineBlock(
        topic="Power Market Operations - LMP and Ancillary Services",
        keywords=["LMP", "locational marginal price", "ancillary services", "day-ahead market", "real-time market", "ISO", "RTO"],
        conclusion_template=[
            "Locational Marginal Prices (LMP) reflect energy cost, congestion, and losses at each node in the transmission network.",
            "Ancillary services (regulation, spinning reserve, non-spinning reserve) maintain reliability and are procured through market mechanisms.",
            "ISOs/RTOs operate centralized markets balancing economic efficiency and reliability constraints."
        ],
        reasoning_framework="""
Restructured electricity markets separate energy production from delivery. Independent System
Operators (ISOs) or Regional Transmission Organizations (RTOs) operate wholesale markets. Major
markets: CAISO (California), ERCOT (Texas), PJM (Mid-Atlantic), NYISO (New York), ISO-NE (New England),
MISO (Midwest), SPP (Plains states).

Market Structure:
1. Day-Ahead Market: Generators submit offers (price-quantity pairs) for next day's hourly energy.
   ISO runs Security-Constrained Unit Commitment (SCUC) to determine which generators commit and
   Security-Constrained Economic Dispatch (SCED) to determine output levels, minimizing total cost
   while respecting transmission limits and N-1 contingencies. Clears ~95% of next day's energy.

2. Real-Time Market: 5-minute dispatch to balance actual load vs. day-ahead schedules. Runs SCED
   every 5 minutes using updated forecasts and actual conditions. Handles real-time deviations,
   forced outages, and renewable forecast errors.

Locational Marginal Price (LMP): The cost to serve one additional MW at a specific bus. LMP =
Energy Component + Congestion Component + Loss Component. All generators at a bus receive the
LMP (even if their cost is lower); all loads pay the LMP. Congestion component can be large
(tens to hundreds of $/MWh) when transmission is constrained. Virtual transactions (financial
products) arbitrage day-ahead vs. real-time LMP differences.

Ancillary Services Markets:
1. Regulation (AGC): Fast-response (1-5 seconds) to track ACE signal. Paid for capacity ($/MW)
   and performance (mileage). Batteries excel due to fast response and unlimited cycles.

2. Spinning Reserve: Online generation that can ramp within 10 minutes. Provides contingency
   reserve for sudden generator/transmission loss. Typical requirement: largest single contingency
   plus margin.

3. Non-Spinning Reserve: Offline generation that can start and load within 10-30 minutes. Lower
   value than spinning reserve.

4. Voltage Support: Reactive power to maintain voltage. Often cost-of-service regulated rather
   than market-based.

Financial Transmission Rights (FTRs): Hedge congestion cost between two locations. If FTR holder
has rights from A to B and congestion causes price difference, holder receives payment equal to
price differential times FTR MW quantity.
        """,
        key_factors=[
            "Marginal pricing: All generators at location receive LMP, even if their cost is lower",
            "Congestion rent: ISO collects congestion payments; used to fund FTR payouts and operations",
            "Make-whole payments: If day-ahead commitment loses money in real-time, ISO pays difference",
            "Market power: Large generators can strategically withhold to raise LMP (subject to mitigation)",
            "Renewable integration: Zero marginal cost renewables depress LMP during high production",
            "Capacity markets: Separate market for long-term resource adequacy (PJM, ISO-NE, NYISO)"
        ],
        primary_authority=[
            "FERC Order 888 - Open Access Transmission",
            "FERC Order 2000 - Regional Transmission Organizations",
            "ISO/RTO Market Manuals and Operating Procedures (e.g., CAISO BPM, PJM Manual 11)"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Complex market structures with regional variations; evolving to accommodate renewables and storage",
        issue_category=IssueCategory.SCADA_CONTROL,
        authority_level=AuthorityLevel.SECONDARY
    ),

    DoctrineBlock(
        topic="Static VAR Compensator (SVC) and STATCOM",
        keywords=["SVC", "STATCOM", "reactive compensation", "FACTS", "voltage support", "thyristor", "VSC"],
        conclusion_template=[
            "SVCs use thyristor-controlled reactors and switched capacitors to provide fast reactive power compensation.",
            "STATCOMs use VSC technology to provide superior reactive power control with smaller footprint than SVCs.",
            "Both are FACTS devices enabling increased transmission capacity and improved voltage stability."
        ],
        reasoning_framework="""
Flexible AC Transmission Systems (FACTS) devices provide dynamic reactive power control for voltage
regulation and power flow optimization. Two primary shunt compensation devices:

Static VAR Compensator (SVC): Combines Thyristor-Switched Capacitors (TSCs) and Thyristor-Controlled
Reactors (TCRs) to provide continuously variable reactive power. TCR uses phase-angle control to
vary effective reactance from zero to full inductive. TSCs provide discrete capacitive steps.
Combined: -100 to +100 MVAR typical range in 0.1 MVAR increments. Response time: 1-2 cycles.
Advantages: Mature technology (since 1970s), proven reliability, lower cost than STATCOM.
Disadvantages: Generates harmonics (5th, 7th, 11th) requiring filters, large footprint, reactive
output decreases with voltage squared (Q ∝ V²), cannot control voltage during deep sags.

Static Synchronous Compensator (STATCOM): Voltage Source Converter (VSC) using IGBTs or GTOs to
synthesize AC voltage in phase with grid. Acts as synchronous condenser with no rotating parts.
Reactive power: Q = V × (V_grid - V_statcom) / X_coupling. Continuously adjustable from full
capacitive to full inductive. Response time: <1 cycle (faster than SVC). Advantages: Output
independent of voltage (can provide full reactive current down to 0.2 pu voltage, critical during
faults), superior harmonics (PWM produces high-frequency harmonics easily filtered), compact
footprint (50% of SVC), can provide active power with energy storage. Disadvantages: Higher cost
($30-50/kVAR vs. $15-25/kVAR for SVC), higher losses (1-3% vs. 0.5-1% for SVC).

Applications: (1) Voltage support at load centers or weak points in transmission system, (2) Power
oscillation damping (modulate reactive power to damp low-frequency oscillations), (3) Transmission
capacity increase (maintain voltage during heavy transfers), (4) Wind farm integration (provide
voltage support during faults to meet LVRT requirements), (5) Arc furnace flicker mitigation.

Typical installations: 50-300 MVAR at transmission substations (115-500 kV). Large STATCOMs can
exceed ±500 MVAR. SVC market mature and stable; STATCOM market growing due to superior performance
for renewable integration and grid support.
        """,
        key_factors=[
            "Voltage dependence: SVC output degrades with low voltage; STATCOM maintains full output",
            "Response speed: Both fast (<2 cycles), STATCOM slightly faster",
            "Harmonics: SVC generates characteristic harmonics; STATCOM cleaner",
            "Economics: SVC lower cost for bulk compensation; STATCOM for performance-critical applications",
            "Active power: STATCOM with battery can provide frequency response and peak shaving",
            "Reliability: SVC proven over 50+ years; STATCOM newer but track record improving"
        ],
        primary_authority=[
            "IEEE Std 1031 - Application Guide for SVC",
            "CIGRE Technical Brochure 144 - Static Synchronous Compensator (STATCOM)",
            "IEEE FACTS Working Group Publications"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established SVC technology; STATCOM increasingly proven with growing installations",
        issue_category=IssueCategory.REACTIVE_COMPENSATION,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Smart Grid Technologies - AMI, DA, DMS, DERMS",
        keywords=["smart grid", "AMI", "advanced metering", "distribution automation", "DMS", "DERMS", "grid modernization"],
        conclusion_template=[
            "Advanced Metering Infrastructure (AMI) provides 15-minute interval data enabling time-of-use rates and outage detection.",
            "Distribution Automation (DA) with automated switches and FLISR reduces outage duration by 30-50%.",
            "DERMS (Distributed Energy Resource Management Systems) coordinate DER to provide grid services and avoid overloads."
        ],
        reasoning_framework="""
Smart grid technologies enhance grid observability, controllability, and efficiency through digital
communication and automation:

1. Advanced Metering Infrastructure (AMI): Two-way communication smart meters replace monthly
   manual reads. Capabilities: 15-minute interval data, remote connect/disconnect, outage detection
   ("last gasp" signal), voltage monitoring, demand response signals. Benefits: Time-of-use and
   dynamic pricing, faster outage detection/restoration, reduced theft, detailed load profiles for
   planning. Deployment: 100M+ meters in U.S. (70% penetration). Communication: Mesh radio (900 MHz),
   cellular (LTE/5G), or PLC (power line carrier).

2. Distribution Automation (DA): Automated switches, reclosers, and voltage regulators with SCADA
   communication enable remote control and automatic reconfiguration. Key application: Fault Location,
   Isolation, and Service Restoration (FLISR). When fault occurs, automated sequence: (1) Recloser
   locks out after multiple unsuccessful reclose attempts, (2) Downstream switches open to isolate
   faulted section, (3) Upstream switches close to restore unfaulted sections from alternate feeder.
   Result: Reduces outage duration from hours to minutes for customers beyond fault, improves SAIDI
   by 30-50%. Requires detailed feeder modeling and communication infrastructure.

3. Distribution Management System (DMS): Software platform integrating SCADA, AMI, DA, and GIS data.
   Applications: Topology processing, state estimation, volt-VAR optimization (VVO), outage management,
   switching order generation. VVO coordinates LTCs, regulators, and capacitors to minimize losses
   while maintaining voltage within ANSI limits; 2-4% energy savings typical.

4. Distributed Energy Resource Management System (DERMS): Coordinates aggregated DER (rooftop solar,
   battery storage, EVs, flexible loads) to provide grid services. Functions: DER visibility and
   forecasting, dispatch for peak shaving or frequency response, voltage regulation, hosting capacity
   analysis. DERMS sits above DMS and below ISO/RTO market systems. Critical for managing high DER
   penetration (>30% on circuit).

5. Advanced Distribution Management System (ADMS): Integrated platform combining DMS, OMS (Outage
   Management System), and DERMS in single vendor solution. Growing adoption to reduce integration
   complexity.

Cybersecurity: Smart grid communication creates attack surface. NIST Cybersecurity Framework and
IEC 62351 provide guidance. Key controls: Encrypted communication (TLS/DTLS), authentication
(PKI certificates), network segmentation, intrusion detection.
        """,
        key_factors=[
            "AMI value: Unlocks time-of-use rates, improves outage response, enables demand response",
            "DA/FLISR economics: SAIDI reduction justifies investment in automation",
            "VVO: 2-4% energy savings from optimized voltage levels and reduced losses",
            "DERMS criticality: Essential for grids with >30% DER penetration",
            "Communication infrastructure: Fiber optic buildout expensive ($50K-200K per mile)",
            "Vendor integration: Multi-vendor interoperability challenging; standards (IEC 61850, IEEE 2030.5) help"
        ],
        primary_authority=[
            "IEC 61850 - Communication Networks and Systems for Power Utility Automation",
            "IEEE 2030.5 - Smart Energy Profile Application Protocol",
            "NIST Framework and Roadmap for Smart Grid Interoperability Standards"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Rapidly evolving smart grid technologies with proven benefits but integration complexity and cybersecurity concerns",
        issue_category=IssueCategory.SCADA_CONTROL,
        authority_level=AuthorityLevel.SECONDARY
    ),

    DoctrineBlock(
        topic="Demand Response and Load Management",
        keywords=["demand response", "load management", "peak shaving", "load curtailment", "interruptible load", "direct load control"],
        conclusion_template=[
            "Demand response shifts or reduces load during peak periods, deferring generation and transmission investment.",
            "Direct load control (cycling air conditioners, water heaters) provides fast, reliable response for emergencies.",
            "Price-responsive demand (time-of-use, critical peak pricing) engages customers in grid optimization."
        ],
        reasoning_framework="""
Demand response (DR) modifies customer electricity consumption in response to grid conditions or
price signals. Complements supply-side resources (generators, storage) with demand-side flexibility.

DR Program Types:

1. Direct Load Control (DLC): Utility remotely controls customer equipment (air conditioners, water
   heaters, pool pumps) during peak periods. Communication: Radio (paging network), cellular, WiFi
   (smart thermostats). Typical cycling: 15 minutes off, 30 minutes on during peak hours. Savings:
   0.5-1.5 kW per air conditioner, 0.5-1.0 kW per water heater. Customer incentive: $25-100/year bill
   credit. Reliability: High (utility controls directly), used for emergency capacity.

2. Interruptible/Curtailable Tariffs: Industrial customers receive discount in exchange for agreeing
   to reduce load when called (4-8 hours advance notice, 2-4 hours duration, limited to 10-20 events/year).
   Typical participants: Cement plants, data centers, wastewater treatment. Curtailment: 1-50 MW per
   facility. Penalties for non-compliance: $10-100/kWh. Provides emergency reserves cheaper than
   peaker plants.

3. Critical Peak Pricing (CPP): Customers face high prices ($1-2/kWh vs. $0.10-0.20/kWh off-peak)
   during declared critical peak events (typically 3-6 PM on hot summer days, 10-15 events/year).
   Opt-in or default with opt-out. Response: 15-30% load reduction during events. Requires AMI for
   interval billing.

4. Time-of-Use (TOU) Rates: Different prices by time period (on-peak, off-peak, super-off-peak).
   Predictable schedule (e.g., on-peak 4-9 PM weekdays). Encourages EV charging overnight, shifting
   pool pumps to midday (solar soak up). Peak/off-peak ratio: 2:1 to 5:1. Lower response than CPP
   (~5-10% load shift) but more predictable.

5. ISO/RTO Market-Based Programs: Aggregators bid demand response into wholesale markets (day-ahead,
   real-time, ancillary services). DR resources paid LMP when dispatched. Typical participants: Large
   commercial/industrial facilities, aggregated residential. Minimum bid size: 0.1-1.0 MW. Controversy:
   Whether DR should receive full LMP or LMP minus retail rate (FERC Order 745).

Benefits: (1) Defers generation investment (peakers cost $1,000-1,500/kW), (2) Defers transmission/
distribution upgrades, (3) Lowers wholesale prices during peak (elastic demand reduces LMP),
(4) Provides emergency reserves (cheaper and faster to deploy than building new plants),
(5) Integrates renewables (shift load to match wind/solar availability).

Challenges: (1) Customer engagement (requires education, enabling technology), (2) Measurement and
verification of savings (customer baseline estimation complex), (3) Persistence (does response
decay over time?), (4) Equity concerns (TOU/CPP may burden customers who can't shift load).
        """,
        key_factors=[
            "Peak shaving value: Deferring peakers saves $1,000+/kW in generation capacity",
            "Technology enablers: Smart thermostats (Nest, Ecobee) enable residential participation",
            "Industrial flexibility: Process industries can shift 20-50% of load with economic incentive",
            "Measurement & verification: Accurate baseline critical for crediting savings",
            "Grid edge integration: Batteries, EVs, smart appliances increase flexibility",
            "Market evolution: ISO/RTOs increasingly allowing DR in energy and ancillary service markets"
        ],
        primary_authority=[
            "FERC Order 745 - Demand Response Compensation in Organized Markets",
            "IEEE Std 2030.2.1 - Monitoring Electric Transportation and Grid Integration",
            "DOE Demand Response and Advanced Metering - Best Practices Guide"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Proven DR programs with decades of experience but evolving market rules and technology enablement",
        issue_category=IssueCategory.SCADA_CONTROL,
        authority_level=AuthorityLevel.SECONDARY
    ),

    DoctrineBlock(
        topic="Arc Flash Hazard Analysis - NFPA 70E and IEEE 1584",
        keywords=["arc flash", "incident energy", "PPE", "NFPA 70E", "IEEE 1584", "arc flash boundary", "arc-rated clothing"],
        conclusion_template=[
            "Arc flash hazards can exceed 100 cal/cm² in high-fault-current switchgear, causing fatal injuries.",
            "IEEE 1584 provides calculation methodology for incident energy and arc flash boundaries.",
            "NFPA 70E requires arc flash labeling and appropriate PPE for electrical work on energized equipment."
        ],
        reasoning_framework="""
Electrical arc flash is an explosive release of energy caused by fault current flowing through air.
Temperature can reach 35,000°F (4x surface of sun), causing severe burns, blast pressure, molten
metal spray, and hearing damage. Arc flash is a leading cause of electrical workplace injuries.

Incident Energy: Thermal energy (in cal/cm²) at working distance (typically 18 inches). Calculated
per IEEE 1584-2018: Considers system voltage, available fault current, arc gap, equipment type
(open air, enclosed box, switchgear), and fault clearing time. Example: 480V switchgear with
40 kA available fault current and 0.1 second clearing time may produce 15-40 cal/cm² at 18 inches.
By comparison: 1.2 cal/cm² causes curable burn, >40 cal/cm² is likely fatal.

Arc Flash Boundary: Distance at which incident energy equals 1.2 cal/cm² (onset of second-degree
burn). Calculated per IEEE 1584 or NFPA 70E tables. Only qualified persons with appropriate PPE
may cross boundary during energized work. Typical boundaries: 2-10 feet for low-voltage equipment,
up to 20+ feet for high-current medium-voltage gear.

Personal Protective Equipment (PPE): Arc-rated (AR) clothing rated in cal/cm² (ATPV or EBT rating).
NFPA 70E defines categories:
- PPE Category 1: 4 cal/cm² (AR shirt + pants or coverall, safety glasses, hard hat, leather gloves)
- PPE Category 2: 8 cal/cm² (+ FR balaclava, ear protection)
- PPE Category 3: 25 cal/cm² (+ double-layer switching hood, voltage-rated gloves)
- PPE Category 4: 40 cal/cm² (+ arc flash suit, total enclosure)

Hazard Mitigation:
1. Reduce fault current: Current-limiting fuses, higher impedance
2. Reduce clearing time: Faster relays, zone-selective interlocking (0.1 sec vs. 0.3 sec saves 3x energy)
3. Increase working distance: Remote racking, infrared windows for inspection
4. De-energize: NFPA 70E preferred approach is work de-energized with LOTO (Lockout/Tagout)
5. Arc-resistant switchgear: Redirects arc energy away from worker (IEEE C37.20.7)

Labels: NFPA 70E requires arc flash warning labels on equipment showing: (1) Nominal voltage,
(2) Arc flash boundary, (3) Incident energy or PPE category, (4) Working distance, (5) Date of
latest study. Labels must be updated when system changes (new generators, transformers, or utility
upgrades increase fault current).

Study frequency: Perform arc flash analysis every 5 years or when system changes >10% of fault
current. Software tools: ETAP, SKM PowerTools, EasyPower.
        """,
        key_factors=[
            "Fatal hazard: Arc flash causes 5-10 fatalities and 2,000+ injuries annually in U.S.",
            "Clearing time dominance: Reducing fault clearing from 0.3s to 0.1s cuts incident energy ~66%",
            "Voltage dependence: Higher voltage creates longer arc; medium voltage more hazardous than low",
            "Fault current: Higher available fault current increases incident energy",
            "Equipment design: Enclosed equipment confines arc; arc-resistant gear redirects energy",
            "Economic impact: Retrofitting arc-resistant switchgear costs $100K-500K per lineup"
        ],
        primary_authority=[
            "NFPA 70E - Standard for Electrical Safety in the Workplace",
            "IEEE Std 1584-2018 - Guide for Performing Arc Flash Hazard Calculations",
            "IEEE C37.20.7 - Guide for Testing Metal-Enclosed Switchgear for Arc Flash"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established arc flash safety standards with clear calculation methodology and PPE requirements",
        issue_category=IssueCategory.PROTECTION,
        authority_level=AuthorityLevel.PRIMARY
    ),
]


# ============================================================================
# TELEMETRY SYSTEM
# ============================================================================

class TelemetryCollector:
    """Comprehensive query telemetry tracking"""

    def __init__(self):
        self.query_count = 0
        self.total_response_time = 0.0
        self.doctrine_hit_counts: Dict[str, int] = defaultdict(int)
        self.issue_category_counts: Dict[str, int] = defaultdict(int)
        self.mode_counts: Dict[str, int] = defaultdict(int)
        self.start_time = time.time()

    def record_query(
        self,
        response_time_ms: float,
        doctrines_triggered: List[str],
        issue_categories: List[str],
        mode: ResponseMode
    ):
        """Record telemetry for a single query"""
        self.query_count += 1
        self.total_response_time += response_time_ms

        for doctrine in doctrines_triggered:
            self.doctrine_hit_counts[doctrine] += 1

        for category in issue_categories:
            self.issue_category_counts[category] += 1

        self.mode_counts[mode.value] += 1

    def get_stats(self) -> Dict[str, Any]:
        """Return current telemetry statistics"""
        uptime = time.time() - self.start_time
        avg_response = self.total_response_time / self.query_count if self.query_count > 0 else 0.0

        return {
            "total_queries": self.query_count,
            "avg_response_time_ms": round(avg_response, 2),
            "uptime_seconds": round(uptime, 2),
            "queries_per_hour": round(self.query_count / (uptime / 3600), 2) if uptime > 0 else 0,
            "top_doctrines": dict(sorted(self.doctrine_hit_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            "issue_category_distribution": dict(self.issue_category_counts),
            "mode_distribution": dict(self.mode_counts)
        }


# ============================================================================
# POWER GRID INTELLIGENCE ENGINE
# ============================================================================

class ENRG05Engine:
    """Electrical Grid Operations & Power Systems Intelligence Engine"""

    def __init__(self):
        self.version = "1.0.0"
        self.doctrine_cache = DOCTRINE_CACHE
        self.telemetry = TelemetryCollector()
        logger.info(f"ENRG05 Engine v{self.version} initialized with {len(self.doctrine_cache)} doctrine blocks")

    def _search_doctrines(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache for relevant blocks using keyword matching"""
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        scored_doctrines = []
        for doctrine in self.doctrine_cache:
            # Calculate relevance score based on keyword matches
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
            topic_match = 1 if any(term in doctrine.topic.lower() for term in query_terms) else 0

            score = keyword_matches * 2 + topic_match

            if score > 0:
                scored_doctrines.append((score, doctrine))

        # Sort by score descending and return top matches
        scored_doctrines.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored_doctrines[:5]]  # Top 5 matches

    def _build_reasoning_chain(self, doctrines: List[DoctrineBlock], mode: ResponseMode) -> List[str]:
        """Build reasoning chain from triggered doctrines"""
        chain = []

        for doctrine in doctrines:
            if mode == ResponseMode.FAST:
                chain.append(f"{doctrine.topic}: {doctrine.conclusion_template[0]}")
            elif mode == ResponseMode.DEFENSE:
                chain.append(
                    f"{doctrine.topic}:\n"
                    f"Conclusion: {' '.join(doctrine.conclusion_template)}\n"
                    f"Authority: {doctrine.primary_authority[0]}\n"
                    f"Confidence: {doctrine.confidence.value}"
                )
            else:  # MEMO
                chain.append(
                    f"{doctrine.topic}:\n"
                    f"Analysis: {doctrine.reasoning_framework}\n"
                    f"Key Factors: {', '.join(doctrine.key_factors[:3])}\n"
                    f"Authorities: {', '.join(doctrine.primary_authority)}\n"
                    f"Confidence: {doctrine.confidence_stratification}"
                )

        return chain

    def _synthesize_answer(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode
    ) -> str:
        """Synthesize final answer from doctrine blocks"""
        if not doctrines:
            return (
                "No specific doctrine blocks matched this power grid query. "
                "This may indicate a question outside standard grid operations, "
                "or requiring specialized analysis beyond cached doctrine."
            )

        if mode == ResponseMode.FAST:
            # Concise summary
            points = [d.conclusion_template[0] for d in doctrines[:3]]
            return "Power Grid Analysis:\n\n" + "\n\n".join(f"• {p}" for p in points)

        elif mode == ResponseMode.DEFENSE:
            # Structured audit-ready response
            sections = []
            for i, doctrine in enumerate(doctrines[:3], 1):
                sections.append(
                    f"{i}. {doctrine.topic}\n"
                    f"   Finding: {doctrine.conclusion_template[0]}\n"
                    f"   Authority: {doctrine.primary_authority[0]}\n"
                    f"   Confidence: {doctrine.confidence.value}"
                )
            return "POWER GRID TECHNICAL ANALYSIS\n\n" + "\n\n".join(sections)

        else:  # MEMO
            # Comprehensive memorandum
            sections = [f"Subject: {query}\n"]

            for doctrine in doctrines[:3]:
                sections.append(
                    f"\n{doctrine.topic}\n"
                    f"{'=' * len(doctrine.topic)}\n\n"
                    f"Conclusion: {' '.join(doctrine.conclusion_template)}\n\n"
                    f"Technical Analysis:\n{doctrine.reasoning_framework}\n\n"
                    f"Key Factors:\n" + "\n".join(f"  • {kf}" for kf in doctrine.key_factors) + "\n\n"
                    f"Authority References:\n" + "\n".join(f"  • {auth}" for auth in doctrine.primary_authority) + "\n\n"
                    f"Confidence Assessment: {doctrine.confidence_stratification}"
                )

            return "\n".join(sections)

    def _determine_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Determine overall confidence level from triggered doctrines"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Use most conservative (highest risk) confidence level
        confidence_priority = {
            ConfidenceLevel.HIGH_RISK: 4,
            ConfidenceLevel.DISCLOSURE: 3,
            ConfidenceLevel.AGGRESSIVE: 2,
            ConfidenceLevel.DEFENSIBLE: 1
        }

        max_priority = max(confidence_priority[d.confidence] for d in doctrines)

        for level, priority in confidence_priority.items():
            if priority == max_priority:
                return level

        return ConfidenceLevel.DISCLOSURE

    def _compute_determinism_hash(self, query: str, answer: str, doctrines: List[DoctrineBlock]) -> str:
        """Compute SHA-256 hash for response determinism verification"""
        doctrine_ids = ",".join(d.topic for d in doctrines)
        hash_input = f"{query}|{answer}|{doctrine_ids}|{self.version}"
        return hashlib.sha256(hash_input.encode()).hexdigest()

    def query(self, request: QueryRequest) -> QueryResponse:
        """Process power grid intelligence query"""
        start_time = time.time()

        # Search doctrine cache
        relevant_doctrines = self._search_doctrines(request.query)

        # Build reasoning chain
        reasoning_chain = self._build_reasoning_chain(relevant_doctrines, request.mode)

        # Synthesize answer
        answer = self._synthesize_answer(request.query, relevant_doctrines, request.mode)

        # Determine confidence
        confidence = self._determine_confidence(relevant_doctrines)

        # Collect authorities
        authorities = []
        for doctrine in relevant_doctrines:
            authorities.extend(doctrine.primary_authority)
        authorities = list(dict.fromkeys(authorities))  # Remove duplicates, preserve order

        # Compute determinism hash
        determinism_hash = self._compute_determinism_hash(request.query, answer, relevant_doctrines)

        # Record telemetry
        response_time_ms = (time.time() - start_time) * 1000
        self.telemetry.record_query(
            response_time_ms=response_time_ms,
            doctrines_triggered=[d.topic for d in relevant_doctrines],
            issue_categories=[d.issue_category.value for d in relevant_doctrines],
            mode=request.mode
        )

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            doctrine_blocks_triggered=[d.topic for d in relevant_doctrines],
            reasoning_chain=reasoning_chain,
            authorities_cited=authorities,
            timestamp=datetime.utcnow().isoformat() + "Z",
            determinism_hash=determinism_hash,
            telemetry={
                "response_time_ms": round(response_time_ms, 2),
                "doctrines_evaluated": len(self.doctrine_cache),
                "doctrines_triggered": len(relevant_doctrines),
                "mode": request.mode.value
            }
        )

    def get_health(self) -> HealthResponse:
        """Return engine health status"""
        stats = self.telemetry.get_stats()

        return HealthResponse(
            status="healthy",
            engine="ENRG05 - Electrical Grid Operations & Power Systems",
            version=self.version,
            port=9085,
            doctrine_count=len(self.doctrine_cache),
            uptime_seconds=stats["uptime_seconds"],
            total_queries=stats["total_queries"],
            avg_response_time_ms=stats["avg_response_time_ms"]
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="ENRG05 - Electrical Grid Operations & Power Systems Engine",
    description="TIE Gold Standard power grid intelligence with 25+ doctrine blocks covering transmission, distribution, protection, SCADA, power quality, reliability standards, and renewable integration",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = ENRG05Engine()

@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Process power grid intelligence query"""
    try:
        return engine.query(request)
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Engine health check"""
    return engine.get_health()


@APP.get("/doctrines")
async def doctrines_endpoint():
    """List all doctrine blocks with metadata"""
    return {
        "total_doctrines": len(engine.doctrine_cache),
        "doctrines": [
            {
                "topic": d.topic,
                "issue_category": d.issue_category.value,
                "confidence": d.confidence.value,
                "authority_level": d.authority_level.value,
                "keywords": d.keywords[:5],
                "primary_authority": d.primary_authority[0] if d.primary_authority else None
            }
            for d in engine.doctrine_cache
        ]
    }


@APP.get("/stats")
async def stats_endpoint():
    """Return detailed telemetry statistics"""
    return engine.telemetry.get_stats()


if __name__ == "__main__":
    logger.info("Starting ENRG05 - Electrical Grid Operations & Power Systems Engine on port 9085")
    uvicorn.run(APP, host="0.0.0.0", port=9085)
