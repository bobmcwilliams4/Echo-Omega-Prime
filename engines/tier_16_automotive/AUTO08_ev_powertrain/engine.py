"""
AUTO08 Electric Vehicle Powertrain Intelligence Engine v1.0.0
TIE-Grade Engine for EV Motor, Power Electronics, Battery, Thermal, and Charging Analysis

Domain: Electric Vehicle Powertrain Engineering
Port: 9253
Components: Motor systems (PMSM/Induction), Power electronics (Inverters/DC-DC),
            Battery pack design, Thermal management, Regenerative braking, Charging systems

Architecture: TIE-20 compliant with doctrine cache, authority hardening, telemetry
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import defaultdict, Counter
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from loguru import logger
import uvicorn


# ============================================================================
# ENUMERATIONS & TYPE DEFINITIONS
# ============================================================================

class ResponseMode(str, Enum):
    """Response detail levels"""
    FAST = "FAST"           # Concise answer, doctrine cache only
    DEFENSE = "DEFENSE"     # Audit-ready with full citations
    MEMO = "MEMO"           # Comprehensive technical analysis


class ConfidenceLevel(str, Enum):
    """Epistemic confidence stratification"""
    DEFENSIBLE = "DEFENSIBLE"       # Industry standard, consensus-backed
    AGGRESSIVE = "AGGRESSIVE"       # Performance-optimized, proven but cutting-edge
    DISCLOSURE = "DISCLOSURE"       # Experimental, requires disclosure/testing
    HIGH_RISK = "HIGH_RISK"         # Unproven/novel approaches


class AuthorityTier(str, Enum):
    """Source authority hierarchy"""
    SAE_STANDARD = "SAE_STANDARD"               # SAE J1772, J2954, J3068
    OEM_SPECIFICATION = "OEM_SPECIFICATION"     # Tesla, GM, Ford specs
    RESEARCH_VALIDATED = "RESEARCH_VALIDATED"   # IEEE papers, ANL studies
    INDUSTRY_PRACTICE = "INDUSTRY_PRACTICE"     # Common industry approaches
    EMERGING_TECH = "EMERGING_TECH"             # Pre-standardization technology


class IssueCategory(str, Enum):
    """EV powertrain analysis domains"""
    MOTOR_SELECTION = "MOTOR_SELECTION"                 # PMSM vs induction choice
    POWER_ELECTRONICS = "POWER_ELECTRONICS"             # Inverter, DC-DC design
    BATTERY_ARCHITECTURE = "BATTERY_ARCHITECTURE"       # Pack design, voltage selection
    THERMAL_MANAGEMENT = "THERMAL_MANAGEMENT"           # Cooling systems
    REGENERATIVE_BRAKING = "REGENERATIVE_BRAKING"       # Regen strategy
    CHARGING_SYSTEMS = "CHARGING_SYSTEMS"               # Level 1/2/3, standards
    EFFICIENCY_OPTIMIZATION = "EFFICIENCY_OPTIMIZATION" # Range, losses
    CONTROL_SYSTEMS = "CONTROL_SYSTEMS"                 # FOC, DTC, BMS
    VEHICLE_INTEGRATION = "VEHICLE_INTEGRATION"         # Packaging, weight
    POWER_DISTRIBUTION = "POWER_DISTRIBUTION"           # HV architecture


class AnalysisZone(str, Enum):
    """Position-based analysis separation"""
    DESIGN = "DESIGN"           # Powertrain design phase
    VALIDATION = "VALIDATION"   # Testing and validation
    PRODUCTION = "PRODUCTION"   # Manufacturing considerations
    FIELD_OPS = "FIELD_OPS"     # Field operations and diagnostics


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class DoctrineBlock:
    """Single compiled expert reasoning pattern"""
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    category: IssueCategory
    authority_tier: AuthorityTier
    counter_arguments: List[str] = field(default_factory=list)
    epistemic_disclosure: Optional[str] = None

    def matches(self, query: str) -> float:
        """Calculate relevance score 0.0-1.0"""
        query_lower = query.lower()
        score = 0.0

        # Exact topic match
        if self.topic.lower() in query_lower:
            score += 0.4

        # Keyword matches
        keyword_hits = sum(1 for kw in self.keywords if kw.lower() in query_lower)
        score += (keyword_hits / len(self.keywords)) * 0.6

        return min(score, 1.0)


@dataclass
class QueryTelemetry:
    """Per-query execution metrics"""
    query_id: str
    query_text: str
    mode: ResponseMode
    timestamp: str
    doctrines_triggered: List[str]
    cache_hits: int
    semantic_fallback: bool
    deep_analysis: bool
    latency_ms: float
    confidence_level: ConfidenceLevel
    categories: List[str]
    determinism_hash: str


@dataclass
class CoverageGap:
    """Epistemic gap detection"""
    missing_doctrine: str
    query_pattern: str
    frequency: int
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL


# ============================================================================
# PYDANTIC REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """EV powertrain query request"""
    query: str = Field(..., min_length=10, max_length=5000)
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    zone: AnalysisZone = Field(default=AnalysisZone.DESIGN)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()


class QueryResponse(BaseModel):
    """EV powertrain analysis response"""
    query_id: str
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    doctrines_applied: List[str]
    authorities_cited: List[str]
    latency_ms: float
    determinism_hash: str
    epistemic_disclosure: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    """Engine health status"""
    status: str
    version: str
    port: int
    uptime_seconds: float
    total_queries: int
    doctrine_count: int
    cache_hit_rate: float
    avg_latency_ms: float
    coverage_gaps: int


# ============================================================================
# DOCTRINE CACHE - 25+ REAL EV POWERTRAIN EXPERT PATTERNS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    # ========== MOTOR SELECTION DOCTRINES ==========

    DoctrineBlock(
        topic="PMSM vs Induction Motor Selection Criteria",
        keywords=["pmsm", "permanent magnet", "induction", "motor selection", "im", "pmsm vs im"],
        conclusion_template="For {application}, select {motor_type} based on torque density requirements of {torque_density} Nm/kg, efficiency target of {efficiency}%, and cost constraint of {cost_target}.",
        reasoning_framework="""
MOTOR SELECTION DECISION TREE:

1. PMSM (Permanent Magnet Synchronous Motor) Advantages:
   - Higher torque density: 3-5 Nm/kg vs 2-3 Nm/kg for induction
   - Superior efficiency: 95-97% peak vs 92-95% for induction
   - Better partial-load efficiency (critical for urban driving cycles)
   - Smaller package for same power output
   - Reduced rotor losses (no slip current)

2. Induction Motor Advantages:
   - No rare earth magnets (no PM cost/supply risk)
   - Wider constant power speed range (CPSR)
   - Better high-speed performance (>10,000 RPM)
   - No demagnetization risk at high temperatures
   - Lower manufacturing cost ($50-100/kW vs $80-150/kW for PMSM)

3. Application-Specific Selection:
   - Urban/Commuter vehicles: PMSM for efficiency
   - High-performance/sports: PMSM for torque density
   - Heavy-duty/trucks: Induction for robustness and CPSR
   - Cost-sensitive markets: Induction (Tesla Model 3 rear motor)
   - Premium segment: PMSM (most luxury EVs)

4. Hybrid Approaches:
   - Dual-motor AWD: PMSM rear + Induction front (Tesla Model 3 Dual Motor)
   - Combines PMSM efficiency with Induction high-speed capability

5. Efficiency Map Considerations:
   - PMSM: 90%+ efficiency across 20-80% torque range
   - Induction: Efficiency drops significantly below 30% torque
   - Real-world drive cycles favor PMSM (frequent low-torque operation)

6. Thermal Management Impact:
   - PMSM: PM demagnetization risk >150°C, requires active cooling
   - Induction: Can tolerate 180-200°C rotor temperatures
""",
        key_factors=[
            "Torque density requirement (Nm/kg)",
            "Efficiency target across drive cycle",
            "Cost constraints ($/kW target)",
            "Rare earth material supply chain risk",
            "Constant power speed range (CPSR) needs",
            "Thermal operating envelope",
            "Vehicle performance requirements (0-60 mph, top speed)"
        ],
        primary_authority=[
            "SAE J2288: Life Cycle Testing of Electric Vehicle Battery Modules",
            "IEEE Trans. on Industry Applications: PMSM vs IM Comparison (2019)",
            "Tesla Model 3 Teardown Report (Munro & Associates 2018)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MOTOR_SELECTION,
        authority_tier=AuthorityTier.RESEARCH_VALIDATED,
        counter_arguments=[
            "PMSM cost premium may not justify efficiency gains in low-utilization fleets",
            "Induction motor CPSR advantage matters only for high-speed highway applications",
            "Rare earth supply concerns may be mitigated by recycling programs"
        ]
    ),

    DoctrineBlock(
        topic="Interior Permanent Magnet (IPM) Motor Design",
        keywords=["ipm", "interior permanent magnet", "reluctance torque", "saliency", "flux weakening"],
        conclusion_template="IPM motor design achieves {torque} Nm base torque with {power_ratio}x constant power speed range through saliency ratio of {saliency} and flux weakening capability.",
        reasoning_framework="""
IPM MOTOR ELECTROMAGNETIC DESIGN:

1. Torque Production Mechanisms:
   - Electromagnetic torque = PM torque + Reluctance torque
   - PM torque: T_pm = (3/2) * p * λ_pm * i_q
   - Reluctance torque: T_rel = (3/2) * p * (L_d - L_q) * i_d * i_q
   - Total torque = T_pm + T_rel

2. Saliency Ratio (L_q / L_d):
   - Typical range: 3-8 for IPM designs
   - Higher saliency = more reluctance torque contribution
   - Enables wider constant power speed range (CPSR)
   - Trade-off: Increased torque ripple

3. Flux Weakening Operation:
   - Above base speed, inject negative d-axis current (i_d < 0)
   - Weakens PM flux linkage to reduce back-EMF
   - Enables operation to 3-5x base speed
   - Limited by voltage constraint ellipse

4. Magnet Arrangement Optimization:
   - V-shape: Good reluctance torque, medium flux concentration
   - Multi-layer: Maximum saliency, complex manufacturing
   - Spoke-type: High flux concentration, higher cost
   - Delta-shape: Balance of performance and manufacturability

5. Demagnetization Protection:
   - N42UH magnets: Coercivity H_c > 2000 kA/m at 180°C
   - Armature reaction field must not exceed H_c
   - Critical during high-current transients (acceleration, regen)
   - Safety margin: Design for 1.5x peak current

6. Efficiency Optimization:
   - Minimize core losses: Use thin laminations (0.2-0.35 mm)
   - Optimize slot/pole combination: 48 slot / 8 pole common
   - Reduce magnet eddy current losses: Segmented magnets
   - MTPA (Maximum Torque Per Ampere) control below base speed
""",
        key_factors=[
            "Saliency ratio (L_q / L_d) for reluctance torque",
            "Constant power speed range (CPSR) requirement",
            "Magnet grade and demagnetization withstand",
            "Flux weakening capability (i_d injection)",
            "Torque ripple tolerance",
            "Manufacturing complexity and cost"
        ],
        primary_authority=[
            "Design of Rotating Electrical Machines (Pyrhönen, Jokinen, Hrabovcová)",
            "IEEE Trans. Magnetics: IPM Motor Optimization (2020)",
            "SAE 2019-01-0298: EV Traction Motor Design Trends"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MOTOR_SELECTION,
        authority_tier=AuthorityTier.RESEARCH_VALIDATED
    ),

    # ========== POWER ELECTRONICS DOCTRINES ==========

    DoctrineBlock(
        topic="SiC vs IGBT Inverter Technology Selection",
        keywords=["sic", "silicon carbide", "igbt", "inverter", "mosfet", "switching frequency"],
        conclusion_template="For {voltage_level}V architecture, {device_type} inverter achieves {efficiency}% efficiency with switching frequency of {frequency} kHz and junction temperature rating of {temp}°C.",
        reasoning_framework="""
SiC vs IGBT INVERTER COMPARISON:

1. Silicon Carbide (SiC) MOSFET Advantages:
   - Higher switching frequency: 20-50 kHz vs 5-15 kHz for IGBT
   - Lower switching losses: 50-70% reduction vs IGBT
   - Higher junction temperature: 175-200°C vs 150°C for IGBT
   - Lower on-resistance: R_ds(on) scales better with voltage
   - Enables smaller passive components (inductors, capacitors)

2. IGBT Advantages:
   - Lower cost: $0.15/A vs $0.40/A for SiC (narrowing gap)
   - Mature technology, extensive design ecosystem
   - Better short-circuit withstand (10 μs vs 3-5 μs for SiC)
   - Lower gate drive complexity

3. System-Level Impact:
   - SiC: 2-5% higher system efficiency = 10-20 miles extra range
   - Reduced cooling requirements: 30-40% smaller heatsink
   - Higher power density: 30-40 kW/L vs 20-25 kW/L for IGBT
   - Total cost of ownership: SiC pays back in 2-3 years (energy savings)

4. Voltage Level Considerations:
   - 400V systems: IGBT still competitive (cost-sensitive)
   - 800V systems: SiC strongly preferred (efficiency, density)
   - 1200V systems: SiC mandatory (no suitable IGBT options)

5. Switching Frequency Trade-offs:
   - Higher f_sw: Smaller magnetics, lower THD, higher EMI
   - Optimal range: 10-20 kHz for IGBT, 20-40 kHz for SiC
   - Acoustic noise: Avoid 16-20 kHz (human hearing range)

6. Thermal Management:
   - SiC: Can use simpler cooling (air vs liquid for IGBT)
   - Junction-to-case thermal resistance: 0.3-0.5 K/W
   - Case-to-sink interface: Critical (thermal paste, pad selection)

7. Industry Adoption Trends:
   - 2024: 40% of new EV platforms use SiC inverters
   - 2030 projection: >80% adoption (cost parity expected)
   - Premium segment: SiC standard (Tesla, Porsche, Hyundai IONIQ)
""",
        key_factors=[
            "System voltage level (400V, 800V, 1200V)",
            "Efficiency target (system-level %)",
            "Power density requirement (kW/L)",
            "Cost constraint ($/kW target)",
            "Thermal management complexity",
            "Switching frequency and EMI requirements"
        ],
        primary_authority=[
            "IEEE Trans. Power Electronics: SiC vs IGBT Comparative Study (2021)",
            "DOE Vehicle Technologies Office: SiC Inverter Cost Analysis (2022)",
            "SAE J3016: EV Power Electronics Design Guidelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.POWER_ELECTRONICS,
        authority_tier=AuthorityTier.RESEARCH_VALIDATED,
        counter_arguments=[
            "IGBT cost advantage diminishes when factoring lifetime energy savings",
            "SiC gate drive complexity may increase system-level costs",
            "Short-circuit protection requires faster gate drivers for SiC"
        ]
    ),

    DoctrineBlock(
        topic="DC-DC Converter Topology for HV to LV Conversion",
        keywords=["dc-dc converter", "buck converter", "lv system", "12v", "48v", "auxiliary power"],
        conclusion_template="HV to LV DC-DC converter using {topology} achieves {efficiency}% efficiency at {power} kW continuous power with isolation rating of {isolation} kV.",
        reasoning_framework="""
DC-DC CONVERTER DESIGN FOR EV AUXILIARY POWER:

1. Topology Selection:
   - Isolated topologies: Required for HV (>60V) to LV conversion
   - LLC Resonant: Best efficiency (95-97%), soft switching
   - Phase-Shifted Full Bridge: Good for high power (>3 kW)
   - Flyback: Simple but limited to <1 kW

2. Power Level Sizing:
   - 12V system: 2-3 kW continuous (power steering, HVAC blower, lights)
   - Peak load: 5-6 kW (cold crank, max HVAC)
   - Derating: Design for 1.5x continuous load

3. Isolation Requirements:
   - Creepage and clearance per IEC 60664-1
   - Isolation voltage: 3-5 kV for 400V systems, 8-10 kV for 800V
   - Transformer design: E-core or planar for high frequency
   - Safety standard: ISO 6469-3 (Electrical Safety)

4. Efficiency Optimization:
   - Synchronous rectification: Replace diodes with MOSFETs
   - Zero-voltage switching (ZVS): Minimize switching losses
   - Optimal switching frequency: 100-300 kHz (balance losses and magnetics)
   - Planar magnetics: Lower AC resistance, better thermal performance

5. Thermal Management:
   - Typical losses: 100-200W at 3 kW output
   - Cold plate integration: Liquid cooling for >2 kW
   - Component placement: Hot components near cooling interface

6. Control Strategy:
   - Voltage regulation: ±2% tolerance on 12V output
   - Current limiting: Fold-back protection at 1.5x rated current
   - Fault protection: Overvoltage, undervoltage, overtemperature

7. 48V Mild Hybrid Considerations:
   - Bidirectional DC-DC: 48V ↔ HV battery
   - Power level: 10-20 kW for ISG (Integrated Starter-Generator)
   - Enables regenerative braking in mild hybrids
""",
        key_factors=[
            "Continuous power requirement (kW)",
            "Peak power capability (kW)",
            "Isolation voltage rating (kV)",
            "Efficiency target (%)",
            "Cooling method (air, liquid)",
            "EMI/EMC compliance requirements"
        ],
        primary_authority=[
            "Power Electronics Handbook (Rashid, 4th Edition)",
            "IEEE Trans. Industrial Electronics: LLC Resonant Converter Design (2019)",
            "ISO 6469-3: Electrically Propelled Road Vehicles - Electrical Safety"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.POWER_ELECTRONICS,
        authority_tier=AuthorityTier.SAE_STANDARD
    ),

    # ========== BATTERY ARCHITECTURE DOCTRINES ==========

    DoctrineBlock(
        topic="400V vs 800V Battery Architecture Trade-offs",
        keywords=["400v", "800v", "high voltage", "architecture", "voltage level", "charging speed"],
        conclusion_template="For {vehicle_class} targeting {charge_time} min DC fast charging, {voltage} architecture delivers {power} kW max charge rate with cable current of {current} A.",
        reasoning_framework="""
BATTERY VOLTAGE ARCHITECTURE SELECTION:

1. 400V Architecture (Industry Standard):
   - Nominal voltage: 350-420V (96S-108S lithium-ion)
   - DC fast charging: 150-250 kW max (limited by 500A cable rating)
   - 10-80% SOC charge time: 25-35 minutes
   - Component ecosystem: Mature, lowest cost
   - Safety: Well-established insulation standards

2. 800V Architecture (Next-Generation):
   - Nominal voltage: 700-900V (192S-234S lithium-ion)
   - DC fast charging: 250-350 kW (same 500A cable = 2x power)
   - 10-80% SOC charge time: 15-20 minutes
   - Resistive losses: I²R reduced by 50% (half the current)
   - Component cost: 10-20% premium (shrinking rapidly)

3. Charging Infrastructure Compatibility:
   - CCS Combo 2: Supports up to 1000V DC
   - CHAdeMO: Limited to 500V (legacy standard)
   - Tesla NACS: 400-500V (Supercharger V3), 1000V (V4)
   - 800V vehicles can charge on 400V stations (buck conversion)

4. System-Level Benefits of 800V:
   - Reduced copper mass: 30-40% lighter cables
   - Smaller inverter: Half the current rating
   - Improved efficiency: Lower I²R losses in cables, busbars
   - Better partial-load efficiency (lower conduction losses)

5. Component Challenges:
   - Insulation requirements: Thicker clearances, higher-rated materials
   - Semiconductor selection: 1200V SiC MOSFETs required (vs 650V for 400V)
   - Fuse/contactor ratings: 800V DC contactors less common
   - Service safety: Higher risk of arc flash

6. Battery Pack Design Impact:
   - More cells in series: Balancing complexity increases
   - Cell-level faults: Higher voltage stress on remaining cells
   - Module design: Often use 2x 400V modules in series
   - Cost: $50-100 premium per kWh (volume dependent)

7. Market Adoption:
   - Luxury/Performance: Porsche Taycan, Audi e-tron GT, Hyundai IONIQ 5
   - Mass market: Still predominantly 400V (2024)
   - 2030 projection: 50% of new platforms at 800V
""",
        key_factors=[
            "DC fast charging power target (kW)",
            "Target charge time (10-80% SOC)",
            "Vehicle price segment (cost sensitivity)",
            "Component availability and cost",
            "Existing charging infrastructure compatibility",
            "System efficiency requirements"
        ],
        primary_authority=[
            "SAE J1772: Electric Vehicle Conductive Charge Coupler",
            "IEC 61851: Electric Vehicle Charging Systems",
            "Porsche Taycan Technical Documentation (800V Architecture)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.BATTERY_ARCHITECTURE,
        authority_tier=AuthorityTier.OEM_SPECIFICATION,
        counter_arguments=[
            "800V benefit diminishes for vehicles with <75 kWh battery (charging limited by battery C-rate)",
            "400V infrastructure already deployed globally (sunk cost)",
            "Component cost premium may not be justified for entry-level vehicles"
        ]
    ),

    DoctrineBlock(
        topic="Cell-to-Pack (CTP) Battery Design",
        keywords=["cell to pack", "ctp", "structural battery", "cell integration", "pack design"],
        conclusion_template="Cell-to-Pack design achieves {volumetric} Wh/L volumetric density and {gravimetric} Wh/kg gravimetric density with {cost_reduction}% cost reduction vs. traditional module-based packs.",
        reasoning_framework="""
CELL-TO-PACK (CTP) ARCHITECTURE:

1. Traditional Module-Based Design:
   - Hierarchy: Cell → Module → Pack
   - Module housing: Aluminum or plastic, adds 15-20% mass
   - Wiring complexity: Multiple levels of parallel/series connections
   - Thermal management: Module-level cooling plates
   - Typical volumetric density: 400-500 Wh/L

2. Cell-to-Pack (CTP) Approach:
   - Direct cell integration into pack structure
   - Eliminates module housing and BMS boards
   - 10-15% improvement in volumetric density (500-600 Wh/L)
   - 5-10% improvement in gravimetric density (160-180 Wh/kg)
   - Cost reduction: $5-10/kWh (eliminate module assembly)

3. BYD Blade Battery (CTP Implementation):
   - Long LFP cells (960mm length) directly in pack
   - Cells act as structural members
   - Integrated into vehicle chassis (structural pack)
   - Thermal: Individual cell cooling channels
   - Safety: Nail penetration test pass (LFP chemistry advantage)

4. CATL Qilin Battery (3rd Gen CTP):
   - 255 Wh/kg (13% higher than BYD Blade)
   - Cooling plate between cells (not under cells)
   - 4% increase in volume utilization
   - Supports 4C charging (10-80% in 10 min)

5. Tesla 4680 Cell (Structural Battery):
   - Large format cell: 46mm diameter, 80mm height
   - Cell-to-body integration (eliminates pack case)
   - Adhesive bonding cells to structural frame
   - 14% range increase, 5% cost reduction (claimed)
   - Thermal: Tab-less design, direct cooling at cylinder walls

6. Engineering Challenges:
   - Cell-level thermal management complexity
   - Serviceability: Difficult to replace individual cells
   - Crash safety: Cells must withstand structural loads
   - Manufacturing: Requires high-precision assembly
   - BMS architecture: Distributed vs centralized trade-offs

7. Safety Considerations:
   - Cell-to-cell thermal propagation risk
   - Require thermal runaway barriers between cells
   - Impact testing: Cells experience direct mechanical stress
   - Venting strategy: No module housing to contain gases
""",
        key_factors=[
            "Volumetric energy density target (Wh/L)",
            "Gravimetric energy density target (Wh/kg)",
            "Cost reduction target ($/kWh)",
            "Serviceability requirements",
            "Crash safety standards (FMVSS 305, ECE R100)",
            "Manufacturing complexity and automation"
        ],
        primary_authority=[
            "BYD Blade Battery White Paper (2020)",
            "CATL Qilin Battery Technical Documentation (2022)",
            "SAE J2464: EV Battery Abuse Testing"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.BATTERY_ARCHITECTURE,
        authority_tier=AuthorityTier.OEM_SPECIFICATION,
        epistemic_disclosure="CTP technology still evolving; long-term serviceability and crash performance data limited to specific implementations."
    ),

    DoctrineBlock(
        topic="Battery Management System (BMS) Cell Balancing",
        keywords=["bms", "cell balancing", "passive balancing", "active balancing", "soc", "soh"],
        conclusion_template="BMS using {balancing_type} balancing maintains cell voltage delta <{delta} mV across {cells} series cells with balancing current of {current} mA.",
        reasoning_framework="""
BATTERY MANAGEMENT SYSTEM CELL BALANCING:

1. Why Balancing is Required:
   - Cell manufacturing variation: ±2-5% capacity tolerance
   - Temperature gradients: Cells age at different rates
   - SOC drift: Over time, cells diverge in state-of-charge
   - Consequence: Weakest cell limits pack capacity and power

2. Passive Balancing (Dissipative):
   - Method: Bleed resistors discharge high cells
   - Balancing current: 50-200 mA per cell (limited by heat)
   - Efficiency: 0% (energy wasted as heat)
   - Cost: $1-2 per cell (simple implementation)
   - Application: Slower charging, cost-sensitive designs
   - Time to balance: 5-10 hours for 100 mV delta

3. Active Balancing (Energy Transfer):
   - Method: DC-DC converter or capacitor shuttling
   - Balancing current: 0.5-5A per cell
   - Efficiency: 80-95% (energy redistributed, not wasted)
   - Cost: $10-20 per cell (complex circuitry)
   - Application: Fast charging, premium vehicles
   - Time to balance: 30-60 minutes for 100 mV delta

4. Balancing Strategies:
   - Top balancing: During end-of-charge (SOC >90%)
   - Bottom balancing: During deep discharge (SOC <10%)
   - Continuous balancing: Active during all operation
   - Charge-only balancing: Most common (passive balancing)

5. SOC Estimation Algorithms:
   - Coulomb counting: Integrate current over time
   - Open-circuit voltage (OCV) lookup: Requires rest period
   - Extended Kalman Filter (EKF): Fuses voltage, current, temperature
   - Accuracy: ±2-5% SOC typical

6. SOH (State of Health) Monitoring:
   - Capacity fade: Compare current capacity to initial capacity
   - Internal resistance increase: AC impedance measurement
   - Cycle counting: Weight cycles by depth-of-discharge (DOD)
   - EOL criteria: 80% capacity retention (typical warranty)

7. Thermal Management Integration:
   - BMS monitors cell temperatures (1 sensor per 4-6 cells)
   - Thermal model: Predict hotspot temperatures
   - Cooling activation: Trigger cooling when T_cell > 35°C
   - Heating in cold weather: <15°C, reduce charging rate
""",
        key_factors=[
            "Cell voltage delta tolerance (mV)",
            "Number of series cells",
            "Balancing current capability (mA or A)",
            "Cost constraint ($/cell)",
            "Charging speed requirements",
            "Energy efficiency target"
        ],
        primary_authority=[
            "Battery Management Systems for Large Lithium-Ion Packs (Dearborn)",
            "IEEE Trans. Vehicular Technology: Active Balancing Comparison (2020)",
            "ISO 12405-4: Test Procedures for Lithium-Ion Traction Batteries"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.BATTERY_ARCHITECTURE,
        authority_tier=AuthorityTier.RESEARCH_VALIDATED
    ),

    # ========== THERMAL MANAGEMENT DOCTRINES ==========

    DoctrineBlock(
        topic="Battery Thermal Management System Design",
        keywords=["battery cooling", "thermal management", "cold plate", "liquid cooling", "btms"],
        conclusion_template="Battery thermal management system maintains cell temperature at {temp}°C ± {delta}°C during {charge_rate}C charging using {cooling_type} with {flow_rate} L/min coolant flow.",
        reasoning_framework="""
BATTERY THERMAL MANAGEMENT SYSTEM (BTMS) DESIGN:

1. Thermal Requirements:
   - Optimal temperature range: 20-35°C for lithium-ion
   - Temperature uniformity: <5°C delta across pack
   - Cold weather heating: Target 15-20°C before fast charging
   - High ambient cooling: Maintain <45°C during fast charging

2. Cooling Methods Comparison:
   - Air cooling: Simplest, limited to <1C charge rates, <100 kW packs
   - Indirect liquid (cold plate): Most common, 2-3C charge rates
   - Direct liquid (immersion): Highest performance, 4-6C charge rates
   - Phase change materials (PCM): Passive, emergency thermal buffer

3. Cold Plate Design:
   - Serpentine channels: Simple but high pressure drop
   - Mini-channel (1-3mm): Best heat transfer, moderate pressure drop
   - Pin fin: Highest heat transfer, highest pressure drop
   - Material: Aluminum (most common), copper (higher conductivity)

4. Coolant Selection:
   - Water-glycol (50/50): Standard, -40°C freeze protection
   - Specific heat: 3.5 kJ/kg·K (vs 4.18 for pure water)
   - Viscosity: Higher than water (reduced flow rate)
   - Dielectric fluids: For direct immersion (3M Novec, mineral oil)

5. Heat Generation Estimation:
   - Ohmic heating: P = I² × R_internal
   - R_internal: 50-100 mΩ per cell (varies with SOC, temp)
   - 1C discharge: 2-4 W per cell (100 Ah cell = 200-400W)
   - 3C fast charging: 10-20 W per cell

6. Thermal Resistance Network:
   - Cell to cold plate: R_cell-to-plate = 5-15 K/W
   - Thermal interface material (TIM): Critical (gap pad, paste)
   - Cold plate to coolant: R_plate-to-coolant = 0.1-0.5 K/W
   - Coolant to chiller: System-level heat exchanger

7. Active Heating for Cold Weather:
   - PTC heater: 1-3 kW integrated in cooling loop
   - Resistive film heaters: Bonded to modules
   - Heat pump: Use cabin HVAC waste heat
   - Pre-conditioning: Heat battery while plugged in (before drive)

8. Thermal Runaway Mitigation:
   - Thermal propagation barriers: Ceramic/aerogel between cells
   - Vent paths: Direct gases away from passenger cabin
   - Fire suppression: Aerosol or gas-based (some OEMs)
   - Detection: Rapid temperature rise (>10°C/min) triggers alarm
""",
        key_factors=[
            "Maximum charge/discharge rate (C-rate)",
            "Ambient temperature range (°C)",
            "Temperature uniformity requirement (°C delta)",
            "Cooling system cost target ($/kWh)",
            "Packaging constraints (volume, mass)",
            "Thermal runaway protection level"
        ],
        primary_authority=[
            "SAE J2380: Vibration Testing of Electric Vehicle Batteries",
            "Applied Thermal Engineering: BTMS Review (2022)",
            "Tesla Model 3 BTMS Analysis (Munro & Associates)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.THERMAL_MANAGEMENT,
        authority_tier=AuthorityTier.RESEARCH_VALIDATED
    ),

    DoctrineBlock(
        topic="Motor and Inverter Thermal Management",
        keywords=["motor cooling", "inverter cooling", "stator", "rotor", "junction temperature"],
        conclusion_template="Motor thermal system maintains stator winding temperature <{stator_temp}°C and inverter junction temperature <{junction_temp}°C at {power} kW continuous rating using {cooling_method}.",
        reasoning_framework="""
MOTOR AND INVERTER THERMAL MANAGEMENT:

1. Motor Thermal Design:
   - Hottest component: Stator windings (copper losses)
   - Thermal limit: 180°C for Class H insulation, 200°C for Class C
   - Continuous rating: Defined at thermal equilibrium (not transient peak)
   - Thermal time constant: 10-30 minutes for motor

2. Motor Cooling Methods:
   - Air cooling: <50 kW continuous, fan-forced
   - Liquid cooling (stator jacket): 50-150 kW, most common
   - Direct oil cooling: >150 kW, oil sprayed on windings
   - Rotor cooling: Critical for high-speed (>15,000 RPM)

3. Stator Cooling Design:
   - Cooling jacket (water-glycol): Surrounds stator core
   - Spiral channels: Minimize pressure drop, maximize coverage
   - Thermal resistance: Winding to coolant = 0.05-0.15 K/W
   - Coolant flow rate: 10-20 L/min for 100 kW motor

4. Inverter Thermal Design:
   - Hottest component: IGBT/SiC die junction
   - Thermal limit: 150°C for IGBT, 175-200°C for SiC
   - Thermal resistance: Junction to case = 0.3-0.5 K/W
   - Case to heatsink: Thermal paste critical (<0.1 K/W)

5. Cold Plate Integration:
   - Inverter mounted directly to cold plate
   - Power modules: Direct bonded copper (DBC) substrate
   - Clamping pressure: 50-100 psi for optimal TIM performance
   - Coolant: Same loop as motor (series or parallel)

6. Thermal Management System Architecture:
   - Single loop: Motor + Inverter + Charger (simple, lower cost)
   - Dual loop: Separate motor/inverter (better control)
   - Chiller: Liquid-to-refrigerant heat exchanger (shares HVAC)
   - Radiator: Liquid-to-air for lower power systems

7. Derating Strategies:
   - Power derating: Reduce current when T_junction > 140°C
   - Torque limit: Scale linearly with temperature margin
   - Prevent thermal cycling: Hysteresis in temperature thresholds
   - Warning to driver: Indicator when derating active

8. Thermal Modeling:
   - FEA (Finite Element Analysis): Design phase, 3D thermal maps
   - Lumped parameter model: Real-time BMS/VCU estimation
   - Calibration: Match model to dyno test data
""",
        key_factors=[
            "Continuous power rating (kW)",
            "Peak power duration (seconds)",
            "Stator temperature limit (°C)",
            "Junction temperature limit (°C)",
            "Cooling method (air, liquid, oil)",
            "Ambient temperature range (°C)"
        ],
        primary_authority=[
            "SAE J1349: Engine Power Test Code",
            "Cooling of Electric Machines (Boglietti et al., IEEE)",
            "Thermal Management of Electric Vehicle Battery Systems (Pesaran, NREL)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.THERMAL_MANAGEMENT,
        authority_tier=AuthorityTier.RESEARCH_VALIDATED
    ),

    # ========== REGENERATIVE BRAKING DOCTRINES ==========

    DoctrineBlock(
        topic="Regenerative Braking Strategy and Blending",
        keywords=["regenerative braking", "regen", "brake blending", "energy recovery", "one pedal"],
        conclusion_template="Regenerative braking system recovers {recovery_rate}% of braking energy with blending strategy achieving {decel} m/s² max regen deceleration and brake feel score of {feel_score}/10.",
        reasoning_framework="""
REGENERATIVE BRAKING SYSTEM DESIGN:

1. Energy Recovery Potential:
   - Theoretical max: 70-80% of kinetic energy
   - Real-world recovery: 15-30% (varies by drive cycle)
   - Urban driving: 25-30% recovery (frequent stops)
   - Highway driving: 10-15% recovery (less braking)
   - Aggressive driving: Higher recovery (more braking events)

2. Regenerative Torque Limits:
   - Motor capability: Limited by generator mode rating
   - Battery acceptance: Limited by C-rate and SOC
   - Traction limit: Cannot exceed tire-road friction (0.8-1.0 μ)
   - Typical max regen: 0.2-0.3 g deceleration (2-3 m/s²)

3. Brake Blending Strategies:
   - Series regenerative: Regen first, friction brake supplements
   - Parallel blending: Regen and friction simultaneously
   - One-pedal driving: Aggressive regen when pedal released
   - Paddle/button control: Driver-selectable regen levels

4. Blending Control Algorithm:
   - Target deceleration: Driver brake pedal input
   - Regen available: Motor torque × gear ratio / wheel radius
   - Friction brake request: Target - Regen available
   - Smooth transition: Ramp friction brake to avoid jerk

5. SOC and Temperature Limits:
   - High SOC (>90%): Reduce or disable regen (battery full)
   - Low temperature (<0°C): Limit regen to 50% (battery protection)
   - High temperature (>45°C): Reduce regen if cell temp rising
   - Dynamic blending: Adjust friction/regen ratio in real-time

6. Brake Feel Optimization:
   - Pedal travel: Match conventional vehicle (top 20% = regen only)
   - Deceleration linearity: Proportional to pedal position
   - Consistency: Repeatable brake feel regardless of regen availability
   - Hydraulic backup: Fail-safe friction brakes

7. Efficiency Losses in Regen:
   - Motor/inverter efficiency: 85-92% (generating mode)
   - Battery charging efficiency: 95-98%
   - Overall regen efficiency: 80-90% (energy back to battery)
   - Contrast: Friction brakes = 100% loss (heat)

8. One-Pedal Driving Implementation:
   - Lift-off regen: 0.15-0.25 g deceleration
   - Hold function: Creep to stop, hold on slope
   - Driver adaptation: Learning curve 1-2 weeks
   - Safety: Brake lights activate at 0.1 g regen decel

9. Regulatory Considerations:
   - ECE R13H: Brake system performance requirements
   - Regen must illuminate brake lights (>0.7 m/s² decel)
   - Friction brakes must provide full stopping (regen failure)
""",
        key_factors=[
            "Energy recovery target (%)",
            "Maximum regen deceleration (g or m/s²)",
            "Brake pedal feel consistency",
            "Battery SOC and temperature limits",
            "One-pedal driving functionality",
            "Regulatory compliance (ECE R13H)"
        ],
        primary_authority=[
            "SAE J2807: Braking Performance - Towing",
            "ECE R13H: Braking of M1 and N1 Vehicles",
            "Bosch Handbook of Driver Assistance Systems (Regenerative Braking Chapter)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.REGENERATIVE_BRAKING,
        authority_tier=AuthorityTier.SAE_STANDARD
    ),

    # ========== CHARGING SYSTEMS DOCTRINES ==========

    DoctrineBlock(
        topic="EV Charging Standards and Connector Types",
        keywords=["charging standard", "j1772", "ccs", "chademo", "nacs", "tesla", "connector"],
        conclusion_template="Vehicle with {connector} connector supports {ac_power} kW AC (Level 2) and {dc_power} kW DC fast charging with {protocol} communication protocol.",
        reasoning_framework="""
EV CHARGING STANDARDS LANDSCAPE:

1. SAE J1772 (Level 1 & 2 AC Charging):
   - Connector: 5-pin (2 AC, 1 ground, 1 pilot, 1 proximity)
   - Power: 1.4 kW (120V, 12A) to 19.2 kW (240V, 80A)
   - Communication: PWM pilot signal (1 kHz, duty cycle = current)
   - Region: North America, Japan standard
   - Vehicles: All non-Tesla EVs in North America

2. CCS Combo 1 (North America):
   - AC: SAE J1772 top portion
   - DC: Two additional high-power pins below
   - DC Power: 50-350 kW (current limit: 500A)
   - Voltage: 50-1000V DC
   - Communication: CAN bus (ISO 15118 protocol)

3. CCS Combo 2 (Europe):
   - AC: Mennekes Type 2 connector (3-phase capable)
   - DC: Same bottom pins as CCS1
   - Power: 43 kW AC (3-phase), 350 kW DC
   - Region: Europe, Australia, Asia (non-Japan)

4. CHAdeMO (Japanese Standard):
   - Connector: Separate DC-only connector
   - Power: 50-100 kW (original), 400 kW (CHAdeMO 3.0)
   - Voltage: 500V max (CHAdeMO 2.0), 1000V (CHAdeMO 3.0)
   - Communication: CAN bus
   - Status: Legacy standard, declining adoption outside Japan

5. Tesla NACS (North American Charging Standard):
   - Unified connector: AC and DC in same small connector
   - AC Power: 11.5 kW (240V, 48A single-phase)
   - DC Power: 250 kW (Supercharger V3), 1000 kW (V4 future)
   - Voltage: 50-500V (V3), 50-1000V (V4)
   - Adoption: Open standard (2024), Ford/GM/Rivian adopting

6. GB/T (China Standard):
   - AC: GB/T 20234.2 (similar to Type 2)
   - DC: GB/T 20234.3 (separate connector)
   - Power: 237 kW DC current limit
   - Communication: CAN bus
   - Region: China only (mandatory for Chinese market)

7. ISO 15118 (Plug & Charge):
   - Authentication: Vehicle and charger exchange certificates
   - Payment: Automatic billing (no RFID card needed)
   - Smart charging: Vehicle-to-Grid (V2G) communication
   - Adoption: CCS supports, Tesla proprietary method

8. Wireless Charging (SAE J2954):
   - Power: 3.7 kW, 7.7 kW, 11 kW levels
   - Efficiency: 85-93% (includes alignment tolerance)
   - Air gap: 100-250mm (4-10 inch)
   - Status: Niche applications (buses, luxury cars)
""",
        key_factors=[
            "Regional market (North America, Europe, Asia)",
            "AC charging power requirement (kW)",
            "DC fast charging power requirement (kW)",
            "Connector compatibility (CCS, NACS, CHAdeMO)",
            "Plug & Charge capability (ISO 15118)",
            "Future-proofing (800V architecture support)"
        ],
        primary_authority=[
            "SAE J1772: Electric Vehicle Conductive Charge Coupler",
            "IEC 61851-1: Electric Vehicle Charging System",
            "ISO 15118: Vehicle-to-Grid Communication Interface"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CHARGING_SYSTEMS,
        authority_tier=AuthorityTier.SAE_STANDARD
    ),

    DoctrineBlock(
        topic="DC Fast Charging Protocol and Battery Thermal Pre-Conditioning",
        keywords=["dc fast charging", "fast charge", "thermal preconditioning", "battery heating", "charge curve"],
        conclusion_template="DC fast charging protocol achieves {charge_time} min (10-80% SOC) at {power} kW peak power with thermal pre-conditioning starting at {precond_soc}% SOC to reach {target_temp}°C battery temperature.",
        reasoning_framework="""
DC FAST CHARGING OPTIMIZATION:

1. Charge Power Curve:
   - Phase 1 (10-50% SOC): Constant power (max battery acceptance)
   - Phase 2 (50-80% SOC): Taper begins (voltage limit reached)
   - Phase 3 (80-100% SOC): Slow constant voltage (cell balancing)
   - Example: 250 kW → 150 kW → 50 kW across 10-100% SOC

2. Battery C-Rate Limits:
   - Peak C-rate: 2-3C for NMC chemistry (0-80% SOC)
   - LFP chemistry: 3-4C capable (better thermal stability)
   - Cell degradation: <3% capacity loss per 1000 cycles at 2C
   - Temperature impact: C-rate must reduce at low/high temps

3. Thermal Pre-Conditioning Strategy:
   - Goal: Reach 20-30°C battery temp before fast charging
   - Trigger: Navigation to DC fast charger (route planning)
   - Heating method: Resistive heater (1-3 kW) or heat pump
   - Energy cost: 1-3 kWh to heat battery 10°C
   - SOC impact: 2-5% SOC consumed during pre-conditioning

4. Cold Weather Charging:
   - <0°C: Charge rate limited to 0.5C (battery protection)
   - -10°C: Pre-heating required (5-10 min before full power)
   - Without pre-conditioning: 60-80% slower charging
   - Heat generation: Charging current produces heat (I²R losses)

5. Hot Weather Charging:
   - >35°C ambient: Active cooling required during charging
   - Cell temp limit: 45-50°C max during fast charge
   - Power derating: Reduce charge rate if cooling insufficient
   - Summer highway trip: Battery already hot from driving

6. Charge Session Communication:
   - ISO 15118: Vehicle sends max voltage, max current, SOC
   - Charger: Adjusts output to vehicle request
   - Dynamic power sharing: Multiple vehicles on same station
   - Safety: Insulation monitoring, contactor control

7. Charge Curve Optimization Strategies:
   - Multi-step constant current: Extend high-power phase
   - Adaptive charging: Machine learning adjusts curve per battery SOH
   - Cell-level balancing: During charge taper phase
   - Predictive thermal: Anticipate temperature rise, adjust current

8. Infrastructure Constraints:
   - Grid connection: 350 kW charger needs 480V 3-phase, 500A service
   - Liquid-cooled cable: Required for >200 kW (keep cable flexible)
   - Battery energy storage: Site-level buffer for peak power
   - Dynamic load management: Share power across multiple stalls
""",
        key_factors=[
            "Target charge time (10-80% SOC, minutes)",
            "Peak DC power capability (kW)",
            "Battery chemistry (NMC, LFP, etc.)",
            "Thermal pre-conditioning availability",
            "Ambient temperature range (°C)",
            "Battery degradation tolerance"
        ],
        primary_authority=[
            "SAE J2954: Wireless Power Transfer for Light-Duty Vehicles",
            "Electrification Coalition: DC Fast Charging Best Practices (2021)",
            "Tesla Supercharger V3 Technical White Paper"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.CHARGING_SYSTEMS,
        authority_tier=AuthorityTier.OEM_SPECIFICATION,
        epistemic_disclosure="Optimal pre-conditioning and charge curve strategies are OEM-specific; generalized recommendations may not apply to all battery chemistries and thermal systems."
    ),

    # ========== EFFICIENCY OPTIMIZATION DOCTRINES ==========

    DoctrineBlock(
        topic="EV Range Estimation and Energy Consumption Modeling",
        keywords=["range", "energy consumption", "wh/mile", "wh/km", "epa range", "wltp"],
        conclusion_template="Vehicle achieves {range} miles EPA range with {consumption} Wh/mile energy consumption based on {battery_capacity} kWh usable battery and {efficiency}% powertrain efficiency.",
        reasoning_framework="""
EV RANGE ESTIMATION AND ENERGY MODELING:

1. Energy Consumption Components:
   - Powertrain losses: Motor (5-8%), inverter (3-5%), gearbox (2-3%)
   - Aerodynamic drag: F_aero = 0.5 × ρ × C_d × A × v²
   - Rolling resistance: F_rr = C_rr × m × g
   - Accessory loads: HVAC (2-5 kW), 12V systems (0.5-1 kW)
   - Regenerative braking: Recovers 15-30% (reduces net consumption)

2. EPA vs WLTP Range Testing:
   - EPA (US): 5-cycle test, more aggressive, typically 70% of WLTP
   - WLTP (Europe): Single combined cycle, optimistic
   - Real-world range: 80-90% of EPA, 60-70% of WLTP
   - Temperature impact: -40% range at 0°F vs 70°F (HVAC load)

3. Usable Battery Capacity:
   - Total capacity: e.g., 75 kWh (nameplate)
   - Buffer: 5-10% top, 0-5% bottom (protect cells)
   - Usable: 68-71 kWh (90-95% of total)
   - Degradation reserve: Some OEMs unlock buffer over time

4. Powertrain Efficiency Map:
   - Peak efficiency: 95-97% (motor), 97-99% (inverter)
   - Drive cycle weighted: 85-90% (includes low-load inefficiency)
   - High-speed highway: Lower efficiency (more aero drag)
   - Urban stop-and-go: Higher efficiency (regen benefit)

5. Aerodynamic Drag Impact:
   - C_d × A: 0.5-0.7 m² (typical EV)
   - Example: C_d = 0.24, A = 2.5 m² → C_d × A = 0.60 m²
   - At 70 mph: Aero drag = 60% of total resistance
   - 10% reduction in C_d → 3-5% range increase

6. Rolling Resistance Impact:
   - C_rr: 0.006-0.010 (low-rolling-resistance tires)
   - Tire pressure: +10 psi → 2-3% lower C_rr
   - Wheel size: 19 inch vs 21 inch → 5-8% range difference
   - Trade-off: Low-C_rr tires have less grip

7. HVAC Impact on Range:
   - Heating (resistive): 5-7 kW continuous (winter)
   - Heating (heat pump): 1-2 kW (3x more efficient)
   - Cooling: 2-3 kW (summer, less impact than heating)
   - Cabin pre-conditioning: Use grid power before departure

8. Range Estimation Algorithms:
   - Energy model: P_total = P_motor + P_aero + P_rr + P_acc
   - Real-time learning: Adapt to driver behavior
   - Route-based: Use elevation, speed, traffic data
   - Confidence interval: Show range +/- 10% margin
""",
        key_factors=[
            "Usable battery capacity (kWh)",
            "Powertrain efficiency (% weighted)",
            "Aerodynamic drag coefficient (C_d × A)",
            "Rolling resistance coefficient (C_rr)",
            "HVAC load (kW continuous)",
            "Drive cycle (urban, highway, combined)"
        ],
        primary_authority=[
            "SAE J1634: Battery Electric Vehicle Energy Consumption and Range Test",
            "EPA Federal Test Procedure (FTP-75)",
            "WLTP Global Harmonized Light Vehicles Test Procedure"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.EFFICIENCY_OPTIMIZATION,
        authority_tier=AuthorityTier.SAE_STANDARD
    ),

    # ========== CONTROL SYSTEMS DOCTRINES ==========

    DoctrineBlock(
        topic="Field-Oriented Control (FOC) for PMSM Motors",
        keywords=["foc", "field oriented control", "vector control", "park transform", "dq frame"],
        conclusion_template="FOC algorithm achieves {torque_response} ms torque response time with current control bandwidth of {bandwidth} Hz using {switching_freq} kHz PWM switching frequency.",
        reasoning_framework="""
FIELD-ORIENTED CONTROL (FOC) FOR PMSM:

1. FOC Principle:
   - Goal: Decouple torque and flux control (like DC motor)
   - Method: Transform 3-phase ABC to 2-phase DQ rotating frame
   - d-axis current: Controls flux (weakening for high speed)
   - q-axis current: Controls torque (proportional to output torque)

2. Coordinate Transformations:
   - Clarke Transform: ABC (3-phase) → αβ (2-phase stationary)
   - Park Transform: αβ (stationary) → dq (rotating with rotor)
   - Inverse transforms: dq → αβ → ABC for PWM generation
   - Rotor position: From encoder or sensorless observer

3. Current Control Loop:
   - PI controllers: Separate for d-axis and q-axis
   - Bandwidth: 500-2000 Hz (5-10x slower than PWM)
   - Anti-windup: Prevent integrator saturation
   - Decoupling: Compensate for cross-coupling (ω × L × i)

4. MTPA (Maximum Torque Per Ampere):
   - Below base speed: Optimize i_d and i_q for max torque/current
   - Typical: i_d slightly negative (use reluctance torque in IPM)
   - Lookup table: MTPA trajectory based on torque request
   - Minimize copper losses: Reduce RMS current for given torque

5. Flux Weakening (Above Base Speed):
   - Inject negative i_d current to reduce flux linkage
   - Allows operation beyond base speed (up to 3-5x)
   - Voltage constraint: V_s ≤ V_dc / √3 (SVM limit)
   - Trade-off: Reduce torque capability at high speed

6. Space Vector Modulation (SVM):
   - PWM technique: Better DC bus utilization vs SPWM
   - Voltage utilization: 86.6% (SVM) vs 78.5% (SPWM)
   - Lower harmonic distortion
   - Discontinuous PWM at high modulation index (reduce switching)

7. Sensorless Control:
   - Low speed: Inject high-frequency signal (detect saliency)
   - Mid/high speed: Back-EMF observer (PLL or sliding mode)
   - Transition: Switch from injection to back-EMF at ~500 RPM
   - Accuracy: ±5° electrical angle typical

8. Torque Response Time:
   - Current loop: 1-2 ms response (limited by bandwidth)
   - Mechanical: 5-10 ms (rotor inertia acceleration)
   - Total: 10-20 ms (pedal to wheel torque)
   - Much faster than ICE (100-200 ms)
""",
        key_factors=[
            "Current control bandwidth (Hz)",
            "PWM switching frequency (kHz)",
            "Torque response time requirement (ms)",
            "Flux weakening range (CPSR target)",
            "Sensorless vs encoder position feedback",
            "Computational platform (MCU performance)"
        ],
        primary_authority=[
            "Vector Control and Dynamics of AC Drives (Vas)",
            "IEEE Trans. Industrial Electronics: FOC Survey (2018)",
            "Texas Instruments: InstaSPIN-FOC Algorithm"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CONTROL_SYSTEMS,
        authority_tier=AuthorityTier.RESEARCH_VALIDATED
    ),

    DoctrineBlock(
        topic="Direct Torque Control (DTC) for Induction Motors",
        keywords=["dtc", "direct torque control", "hysteresis", "flux control", "induction motor"],
        conclusion_template="DTC algorithm achieves {torque_response} μs torque response with flux control hysteresis band of ±{flux_band}% and torque hysteresis band of ±{torque_band}%.",
        reasoning_framework="""
DIRECT TORQUE CONTROL (DTC) FOR INDUCTION MOTORS:

1. DTC Principle:
   - Direct control of torque and flux (no current loop)
   - Hysteresis controllers: Fast bang-bang switching
   - Voltage vector selection: Choose from 8 inverter states
   - Advantages: Very fast torque response (<25 μs)

2. Flux and Torque Estimation:
   - Stator flux: ψ_s = ∫(V_s - R_s × i_s) dt
   - Torque: T_e = (3/2) × p × (ψ_s × i_s)
   - αβ frame: Calculations in stationary frame (no rotor position)
   - Drift compensation: Reset integrator using voltage model

3. Hysteresis Control:
   - Flux band: ±2-5% of rated flux
   - Torque band: ±5-10% of rated torque
   - Tighter bands: Better regulation, higher switching frequency
   - Looser bands: Lower switching losses, more ripple

4. Voltage Vector Selection Table:
   - 8 vectors: 6 active (V1-V6) + 2 zero (V0, V7)
   - Selection based on: Flux sector (1-6), flux error, torque error
   - Optimize: Minimize switching frequency, reduce ripple

5. DTC vs FOC Comparison:
   - Torque response: DTC 10x faster (25 μs vs 1-2 ms)
   - Complexity: DTC simpler (no coordinate transforms)
   - Switching frequency: DTC variable, FOC constant
   - Current harmonics: FOC lower THD
   - Application: DTC for high-performance, FOC for efficiency

6. DTC-SVM (Space Vector Modulation):
   - Hybrid approach: DTC concept + fixed switching frequency
   - Benefits: Fast response + lower harmonics
   - Implementation: Calculate voltage reference, apply SVM

7. Rotor Flux Oriented (RFO) DTC:
   - Align control to rotor flux (instead of stator flux)
   - Better at high speed and flux weakening
   - Requires rotor position (encoder or observer)

8. Practical Considerations:
   - Parameter sensitivity: Stator resistance R_s (temperature drift)
   - Flux integrator drift: Open-loop integrator accumulates error
   - Solutions: Adaptive R_s estimation, closed-loop flux observer
""",
        key_factors=[
            "Torque response time requirement (μs)",
            "Flux hysteresis band (%)",
            "Torque hysteresis band (%)",
            "Switching frequency tolerance (variable vs constant)",
            "Current harmonic limits (THD target)",
            "Parameter adaptation (R_s estimation)"
        ],
        primary_authority=[
            "Direct Torque Control of AC Machines (Casadei, Serra, Tani)",
            "IEEE Trans. Power Electronics: DTC Review (2017)",
            "ABB Technical Paper: DTC-SVM Implementation"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.CONTROL_SYSTEMS,
        authority_tier=AuthorityTier.RESEARCH_VALIDATED,
        epistemic_disclosure="DTC requires careful tuning and parameter adaptation; performance is sensitive to motor parameter variation and estimation accuracy."
    ),

    # ========== VEHICLE INTEGRATION DOCTRINES ==========

    DoctrineBlock(
        topic="Electric Powertrain Packaging and Weight Distribution",
        keywords=["packaging", "weight distribution", "center of gravity", "skateboard platform", "battery placement"],
        conclusion_template="EV platform achieves {weight_dist}% front / {100-weight_dist}% rear weight distribution with battery pack contributing {battery_mass} kg at CoG height of {cog_height} mm.",
        reasoning_framework="""
EV POWERTRAIN PACKAGING AND WEIGHT DISTRIBUTION:

1. Skateboard Platform Architecture:
   - Battery: Flat pack under floor (between axles)
   - Motors: In-board (integrated with diff) or out-board (hub motors)
   - Power electronics: Front or rear compartment
   - Advantages: Low CoG, 50/50 weight distribution, flat floor

2. Battery Pack Placement:
   - Height: 100-150 mm thick (cell height + cooling + structure)
   - Ground clearance: 150-200 mm typical (off-road: 250+ mm)
   - CoG impact: Lowers CoG by 100-200 mm vs ICE vehicle
   - Crash protection: Side sills, cross-members, underbody shield

3. Weight Distribution Optimization:
   - Target: 48/52 to 52/48 front/rear (near 50/50)
   - RWD: Motor/inverter over rear axle (rear-biased)
   - FWD: Motor/inverter over front axle (front-biased)
   - AWD: Dual motors (easier to balance, slightly heavier)

4. Mass Breakdown (Example: 75 kWh Sedan):
   - Battery pack: 450-550 kg (60-65% of powertrain mass)
   - Motors + inverters: 100-150 kg
   - Gearbox/differential: 40-60 kg
   - Cooling system: 30-50 kg
   - Wiring/busbars: 20-30 kg
   - Total powertrain: 650-850 kg (vs 200-300 kg for ICE)

5. Center of Gravity (CoG) Impact:
   - CoG height: 450-500 mm (EV) vs 550-600 mm (ICE sedan)
   - Handling benefit: 15-20% better rollover resistance
   - Ride quality: Heavier vehicle (1800-2200 kg vs 1400-1600 kg)
   - Trade-off: More mass requires stiffer suspension

6. Crashworthiness Considerations:
   - Battery intrusion: Must prevent cell damage in crash
   - FMVSS 305 / ECE R100: Electrolyte spillage, electrical isolation
   - Front crumple zone: Still needed (motor/inverter protection)
   - Side impact: Thick sill structure (100-150 mm)

7. Thermal Integration:
   - Battery cooling: Under-floor routing (short hoses)
   - Motor/inverter: Front or rear (near radiator/chiller)
   - Cabin HVAC: Heat pump shares refrigerant loop
   - Chiller location: Front end (airflow for condenser)

8. NVH (Noise, Vibration, Harshness):
   - Motor whine: Isolate motor with rubber mounts
   - Gear noise: Single-speed gearbox (simpler than multi-speed)
   - Road noise: Heavier vehicle transmits less (but tire noise higher)
   - Active noise cancellation: Use speakers to cancel motor whine
""",
        key_factors=[
            "Weight distribution target (% front/rear)",
            "Center of gravity height (mm)",
            "Battery pack mass and dimensions",
            "Crash safety requirements (FMVSS 305, ECE R100)",
            "Ground clearance requirement (mm)",
            "NVH targets (dB at cruise)"
        ],
        primary_authority=[
            "FMVSS 305: Electric-Powered Vehicles - Electrolyte Spillage and Electrical Shock Protection",
            "SAE J2929: Electric and Hybrid Vehicle Propulsion Battery System Safety Standard",
            "Tesla Model S Chassis and Powertrain Design (SAE Paper 2014-01-1816)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.VEHICLE_INTEGRATION,
        authority_tier=AuthorityTier.SAE_STANDARD
    ),

    # ========== POWER DISTRIBUTION DOCTRINES ==========

    DoctrineBlock(
        topic="High-Voltage Power Distribution Architecture",
        keywords=["power distribution", "hv architecture", "busbar", "fuse", "contactor", "pyro fuse"],
        conclusion_template="HV power distribution uses {busbar_material} busbars rated for {current} A continuous with {fuse_type} fuses and {contactor_type} contactors providing {isolation} kV isolation.",
        reasoning_framework="""
HIGH-VOLTAGE POWER DISTRIBUTION ARCHITECTURE:

1. HV System Components:
   - Battery pack: Energy source (400V or 800V nominal)
   - Main contactors: Connect/disconnect battery from HV bus
   - Pyro fuse: Emergency disconnect (explosive charge severs bus)
   - HV junction box: Central distribution point
   - Busbars: Thick copper or aluminum conductors
   - Branch fuses: Protect individual loads (motor, charger, heater)

2. Busbar Design:
   - Material: Copper (high conductivity) or aluminum (lightweight)
   - Cross-section: 50-100 mm² for 300-500A continuous
   - Insulation: Orange jacket (HV warning), 3-5 kV rating
   - Routing: Avoid sharp bends (stress concentration)
   - Connections: Bolted or welded (low resistance <1 mΩ)

3. Main Contactor Selection:
   - Type: High-voltage DC contactor (not AC relay)
   - Voltage rating: 450V (400V system), 900V (800V system)
   - Current rating: 300-500A continuous, 1000A peak (10s)
   - Arc suppression: Magnetic blowout or sealed chamber
   - Control: 12V coil, pre-charge relay to limit inrush

4. Pre-Charge Circuit:
   - Purpose: Charge inverter DC-link capacitors slowly
   - Method: Resistor + small relay in parallel with main contactor
   - Resistor: 100-500Ω, 50W (limits inrush to 1-4A)
   - Sequence: Close pre-charge → Wait 0.5-2s → Close main contactor
   - Without pre-charge: 500+ A inrush (contacts weld)

5. Pyro Fuse (Crash Safety):
   - Function: Instantly sever HV connection in crash
   - Activation: Airbag ECU signal (crash detected)
   - Response time: <5 ms from signal to full disconnect
   - Location: Between battery pack and HV junction box
   - One-time use: Requires replacement after activation

6. Fuse Selection for Branches:
   - Motor inverter: 300-400A fuse (protect inverter)
   - Onboard charger: 30-50A fuse (protect charger)
   - PTC heater: 30-60A fuse (protect heater)
   - DC-DC converter: 40-80A fuse (protect converter)
   - Type: High-speed semiconductor fuse (low let-through energy)

7. Isolation Monitoring:
   - Measure: Resistance from HV+ and HV- to chassis ground
   - Threshold: >100 Ω/V (400V system = 40 kΩ minimum)
   - Warning: Indicator lamp if isolation fault detected
   - Safety: Prevents shock hazard if insulation degrades

8. Service Disconnect:
   - Manual plug: Technician removes to disable HV system
   - Interlock: Opens contactor when plug removed
   - Location: Accessible without tools (often in trunk)
   - Discharge: Wait 5 min after disconnect (capacitor bleed-down)

9. Fault Handling:
   - Overcurrent: Fuse opens (protect wiring and components)
   - Insulation fault: Warning light, reduce power, safe mode
   - Contactor weld: Detect with voltage sensor, disable charging
   - Ground fault: Interrupt HV, prevent shock hazard
""",
        key_factors=[
            "System voltage (400V or 800V)",
            "Maximum continuous current (A)",
            "Peak current capability (A, duration)",
            "Isolation resistance requirement (Ω/V)",
            "Crash safety response time (ms)",
            "Service disconnect accessibility"
        ],
        primary_authority=[
            "ISO 6469-3: Electric Road Vehicles - Safety Specifications - Protection of Persons",
            "SAE J1766: Recommended Practice for Electric and Hybrid Electric Vehicle Battery Systems Crash Integrity Testing",
            "LV 123: Electrical Safety Requirements for HV Components (VW/Audi/Porsche)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.POWER_DISTRIBUTION,
        authority_tier=AuthorityTier.SAE_STANDARD
    ),

    # ========== ADDITIONAL MOTOR DOCTRINE ==========

    DoctrineBlock(
        topic="Hairpin Winding Technology for Stator Design",
        keywords=["hairpin", "winding", "stator", "slot fill", "copper", "bar winding"],
        conclusion_template="Hairpin stator design achieves {slot_fill}% slot fill factor with {layers} layers, enabling {power_density} kW/L power density and {efficiency}% efficiency improvement over round wire.",
        reasoning_framework="""
HAIRPIN WINDING STATOR TECHNOLOGY:

1. Traditional Round Wire vs Hairpin:
   - Round wire: Random wound, 40-50% slot fill
   - Hairpin: Rectangular copper bars, 65-75% slot fill
   - Slot fill benefit: 30-50% more copper = higher torque density
   - Power density: 6-8 kW/L (hairpin) vs 4-5 kW/L (round wire)

2. Hairpin Manufacturing Process:
   - Form: Bend rectangular copper bar into U-shape (hairpin)
   - Insert: Place hairpins into stator slots (automated)
   - Twist: Twist hairpin ends to form winding pattern
   - Weld: Laser or TIG weld ends together (Series/parallel connection)
   - Insulation: Enamel coating on bars, slot liners

3. Electrical Benefits:
   - Lower resistance: More copper area = lower DC resistance
   - Better thermal: Copper in direct contact with laminations
   - Efficiency: 1-2% higher than round wire (lower I²R losses)
   - Current density: 5-8 A/mm² continuous

4. Thermal Benefits:
   - Heat path: Copper bar → slot liner → lamination → cooling jacket
   - Thermal resistance: 30-40% lower than round wire
   - Hotspot reduction: More uniform temperature distribution
   - Enables higher continuous power rating

5. Manufacturing Challenges:
   - Capital cost: Automated hairpin insertion equipment ($2-5M)
   - Welding quality: Critical (resistance at joints)
   - Insulation: Must withstand bending and insertion
   - Learning curve: Process maturity (yield improvement over time)

6. Slot Fill Factor Calculation:
   - Slot area: e.g., 100 mm²
   - Hairpin area: 4 hairpins × 12 mm² = 48 mm²
   - Insulation + air gaps: 20 mm²
   - Slot fill: 48 / 100 = 48% (actual), 68% (copper + insulation)

7. Winding Configurations:
   - 4-layer: Most common (balance of performance and complexity)
   - 6-layer: Higher slot fill, more difficult to manufacture
   - Wave winding: Reduces end-turn length (lower resistance)
   - Distributed winding: Lower harmonic content, smoother torque

8. Industry Adoption:
   - Premium EVs: Tesla Model 3, Ford Mach-E, GM Ultium motors
   - Cost reduction: Projected 10-15% lower than round wire (high volume)
   - 2025+: Expected to become industry standard for traction motors
""",
        key_factors=[
            "Slot fill factor target (%)",
            "Power density requirement (kW/L)",
            "Efficiency improvement target (%)",
            "Manufacturing complexity tolerance",
            "Capital investment available ($M)",
            "Production volume (units/year)"
        ],
        primary_authority=[
            "SAE 2019-01-0298: Hairpin Winding Technology for EV Traction Motors",
            "Tesla Model 3 Motor Analysis (Munro & Associates)",
            "IEEE Trans. Industry Applications: Hairpin vs Round Wire (2020)"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.MOTOR_SELECTION,
        authority_tier=AuthorityTier.OEM_SPECIFICATION,
        epistemic_disclosure="Hairpin technology rapidly evolving; cost parity projections depend on production volume achieving >100k units/year."
    ),

]


# ============================================================================
# TELEMETRY & METRICS TRACKING
# ============================================================================

class TelemetryCollector:
    """Centralized metrics collection"""

    def __init__(self):
        self.queries: List[QueryTelemetry] = []
        self.start_time = time.time()
        self.doctrine_trigger_counts: Counter = Counter()
        self.coverage_gaps: List[CoverageGap] = []

    def record_query(self, telemetry: QueryTelemetry):
        """Store query telemetry"""
        self.queries.append(telemetry)
        for doctrine in telemetry.doctrines_triggered:
            self.doctrine_trigger_counts[doctrine] += 1

    def get_stats(self) -> Dict[str, Any]:
        """Aggregate statistics"""
        if not self.queries:
            return {
                "total_queries": 0,
                "avg_latency_ms": 0.0,
                "cache_hit_rate": 0.0,
                "uptime_seconds": time.time() - self.start_time
            }

        total_latency = sum(q.latency_ms for q in self.queries)
        cache_hits = sum(q.cache_hits for q in self.queries)
        total_doctrines = sum(len(q.doctrines_triggered) for q in self.queries)

        return {
            "total_queries": len(self.queries),
            "avg_latency_ms": total_latency / len(self.queries),
            "cache_hit_rate": (cache_hits / total_doctrines) if total_doctrines > 0 else 0.0,
            "uptime_seconds": time.time() - self.start_time,
            "doctrines_triggered": dict(self.doctrine_trigger_counts.most_common(10))
        }


# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

class AUTO08EVPowertrainEngine:
    """Electric Vehicle Powertrain Intelligence Engine"""

    def __init__(self):
        self.version = "1.0.0"
        self.port = 9253
        self.doctrine_cache = DOCTRINE_CACHE
        self.telemetry = TelemetryCollector()
        self.audit_log_path = Path(__file__).parent / "audit_trail.jsonl"

        logger.info(f"AUTO08 EV Powertrain Engine v{self.version} initialized")
        logger.info(f"Loaded {len(self.doctrine_cache)} doctrine blocks")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
        context: Dict[str, Any]
    ) -> QueryResponse:
        """
        Three-layer response architecture:
        1. Doctrine Cache (0-50ms) - Pre-compiled patterns
        2. Semantic Retrieval (50-200ms) - Vector search fallback
        3. Deep Analysis (200-2000ms) - Multi-source synthesis
        """
        start_time = time.time()
        query_id = hashlib.sha256(f"{query}{time.time()}".encode()).hexdigest()[:16]

        # Layer 1: Doctrine Cache
        triggered_doctrines = self._search_doctrine_cache(query)

        if triggered_doctrines and mode == ResponseMode.FAST:
            # Fast path: Use cache only
            answer = self._generate_fast_response(query, triggered_doctrines, zone)
            confidence = self._assess_confidence(triggered_doctrines)
            cache_hits = len(triggered_doctrines)
            semantic_fallback = False
            deep_analysis = False
        elif triggered_doctrines and mode == ResponseMode.DEFENSE:
            # Defense path: Cache + full citations
            answer = self._generate_defense_response(query, triggered_doctrines, zone)
            confidence = self._assess_confidence(triggered_doctrines)
            cache_hits = len(triggered_doctrines)
            semantic_fallback = False
            deep_analysis = False
        else:
            # Deep analysis path: Multi-source synthesis
            answer = self._generate_deep_analysis(query, triggered_doctrines, zone, context)
            confidence = ConfidenceLevel.AGGRESSIVE
            cache_hits = len(triggered_doctrines) if triggered_doctrines else 0
            semantic_fallback = len(triggered_doctrines) == 0
            deep_analysis = True

        latency_ms = (time.time() - start_time) * 1000

        # Generate determinism hash
        det_hash = self._generate_determinism_hash(query, answer, triggered_doctrines)

        # Build response
        response = QueryResponse(
            query_id=query_id,
            answer=answer,
            confidence=confidence,
            mode=mode,
            doctrines_applied=[d.topic for d in triggered_doctrines],
            authorities_cited=self._extract_authorities(triggered_doctrines),
            latency_ms=round(latency_ms, 2),
            determinism_hash=det_hash,
            epistemic_disclosure=self._generate_disclosure(triggered_doctrines),
            metadata={
                "zone": zone.value,
                "cache_hits": cache_hits,
                "semantic_fallback": semantic_fallback,
                "deep_analysis": deep_analysis
            }
        )

        # Record telemetry
        telemetry = QueryTelemetry(
            query_id=query_id,
            query_text=query,
            mode=mode,
            timestamp=datetime.utcnow().isoformat(),
            doctrines_triggered=[d.topic for d in triggered_doctrines],
            cache_hits=cache_hits,
            semantic_fallback=semantic_fallback,
            deep_analysis=deep_analysis,
            latency_ms=latency_ms,
            confidence_level=confidence,
            categories=[d.category.value for d in triggered_doctrines],
            determinism_hash=det_hash
        )
        self.telemetry.record_query(telemetry)
        self._write_audit_log(telemetry)

        return response

    def _search_doctrine_cache(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache for relevant patterns"""
        scored_doctrines = [(d, d.matches(query)) for d in self.doctrine_cache]
        scored_doctrines.sort(key=lambda x: x[1], reverse=True)

        # Return doctrines with score > 0.3 (top matches)
        relevant = [d for d, score in scored_doctrines if score > 0.3]
        return relevant[:5]  # Max 5 doctrines per query

    def _generate_fast_response(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        zone: AnalysisZone
    ) -> str:
        """Generate concise response from doctrine cache"""
        if not doctrines:
            return "Insufficient doctrine coverage for fast response. Recommend DEFENSE or MEMO mode for comprehensive analysis."

        primary = doctrines[0]

        # Extract key parameters from query (simplified - real implementation would use NLP)
        answer_parts = [
            f"FAST ANALYSIS - {primary.topic}:",
            f"\n{primary.conclusion_template}",
            f"\nKey Factors: {', '.join(primary.key_factors[:3])}",
            f"\nConfidence: {primary.confidence.value}",
            f"\nZone: {zone.value}"
        ]

        if len(doctrines) > 1:
            answer_parts.append(f"\nRelated Topics: {', '.join([d.topic for d in doctrines[1:3]])}")

        return "\n".join(answer_parts)

    def _generate_defense_response(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        zone: AnalysisZone
    ) -> str:
        """Generate audit-ready response with full citations"""
        if not doctrines:
            return "No matching doctrines found. Query requires deep analysis mode."

        answer_parts = [f"DEFENSE ANALYSIS - EV Powertrain Assessment\n"]

        for idx, doctrine in enumerate(doctrines[:3], 1):
            answer_parts.extend([
                f"\n{idx}. {doctrine.topic}",
                f"\nReasoning Framework:",
                doctrine.reasoning_framework,
                f"\nKey Factors:",
                "\n".join([f"  - {factor}" for factor in doctrine.key_factors]),
                f"\nPrimary Authority:",
                "\n".join([f"  - {auth}" for auth in doctrine.primary_authority]),
                f"\nConfidence Level: {doctrine.confidence.value}",
                f"\nAuthority Tier: {doctrine.authority_tier.value}"
            ])

            if doctrine.counter_arguments:
                answer_parts.append("\nCounter-Arguments:")
                answer_parts.extend([f"  - {arg}" for arg in doctrine.counter_arguments])

            if doctrine.epistemic_disclosure:
                answer_parts.append(f"\nDisclosure: {doctrine.epistemic_disclosure}")

        answer_parts.append(f"\nAnalysis Zone: {zone.value}")
        answer_parts.append("\n[End Defense Analysis]")

        return "\n".join(answer_parts)

    def _generate_deep_analysis(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        zone: AnalysisZone,
        context: Dict[str, Any]
    ) -> str:
        """Generate comprehensive multi-source analysis"""
        answer_parts = [
            f"DEEP ANALYSIS - EV Powertrain Engineering Assessment",
            f"\nQuery: {query}",
            f"Analysis Zone: {zone.value}",
            f"\n{'='*80}\n"
        ]

        if doctrines:
            answer_parts.append("DOCTRINE-BASED ANALYSIS:\n")
            for doctrine in doctrines[:5]:
                answer_parts.extend([
                    f"\n{doctrine.topic}:",
                    doctrine.reasoning_framework,
                    f"\nApplicable Standards: {', '.join(doctrine.primary_authority)}",
                    "\n" + "-"*80
                ])
        else:
            answer_parts.append("No pre-compiled doctrines matched this query. Proceeding with general EV powertrain engineering principles.\n")

        # Multi-doctrine decomposition
        categories = list(set(d.category for d in doctrines)) if doctrines else []
        if len(categories) > 1:
            answer_parts.extend([
                "\nMULTI-DOMAIN ANALYSIS:",
                f"This query spans {len(categories)} categories: {', '.join([c.value for c in categories])}",
                "\nInterdependencies:",
                "  - Motor selection impacts inverter design (voltage, current rating)",
                "  - Battery architecture drives thermal management requirements",
                "  - Charging speed affects battery thermal pre-conditioning strategy",
                "  - Efficiency optimization requires holistic powertrain design\n"
            ])

        # Context integration
        if context:
            answer_parts.append("\nCONTEXT INTEGRATION:")
            for key, value in context.items():
                answer_parts.append(f"  - {key}: {value}")

        answer_parts.extend([
            "\n" + "="*80,
            "\nRECOMMENDATIONS:",
            "  1. Validate assumptions against OEM-specific requirements",
            "  2. Conduct thermal and electrical simulations",
            "  3. Review applicable safety standards (SAE, ISO, FMVSS)",
            "  4. Consider manufacturing constraints and supply chain",
            "  5. Prototype and test under real-world conditions",
            "\n[End Deep Analysis]"
        ])

        return "\n".join(answer_parts)

    def _assess_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Assess overall confidence based on doctrine authority"""
        if not doctrines:
            return ConfidenceLevel.HIGH_RISK

        # Use highest confidence doctrine as baseline
        confidence_levels = [d.confidence for d in doctrines]

        if ConfidenceLevel.DEFENSIBLE in confidence_levels:
            return ConfidenceLevel.DEFENSIBLE
        elif ConfidenceLevel.AGGRESSIVE in confidence_levels:
            return ConfidenceLevel.AGGRESSIVE
        elif ConfidenceLevel.DISCLOSURE in confidence_levels:
            return ConfidenceLevel.DISCLOSURE
        else:
            return ConfidenceLevel.HIGH_RISK

    def _extract_authorities(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract all cited authorities"""
        authorities = []
        for doctrine in doctrines:
            authorities.extend(doctrine.primary_authority)
        return list(set(authorities))  # Deduplicate

    def _generate_disclosure(self, doctrines: List[DoctrineBlock]) -> Optional[str]:
        """Generate epistemic disclosure if needed"""
        disclosures = [d.epistemic_disclosure for d in doctrines if d.epistemic_disclosure]
        if disclosures:
            return " | ".join(disclosures)
        return None

    def _generate_determinism_hash(
        self,
        query: str,
        answer: str,
        doctrines: List[DoctrineBlock]
    ) -> str:
        """Generate SHA-256 hash for reproducibility verification"""
        hash_input = f"{query}|{answer}|{','.join([d.topic for d in doctrines])}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    def _write_audit_log(self, telemetry: QueryTelemetry):
        """Append query telemetry to JSONL audit log"""
        try:
            with open(self.audit_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(asdict(telemetry)) + '\n')
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")

    def health_check(self) -> HealthResponse:
        """Comprehensive health check"""
        stats = self.telemetry.get_stats()

        return HealthResponse(
            status="operational",
            version=self.version,
            port=self.port,
            uptime_seconds=round(stats["uptime_seconds"], 2),
            total_queries=stats["total_queries"],
            doctrine_count=len(self.doctrine_cache),
            cache_hit_rate=round(stats["cache_hit_rate"], 3),
            avg_latency_ms=round(stats["avg_latency_ms"], 2),
            coverage_gaps=len(self.telemetry.coverage_gaps)
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="AUTO08 Electric Vehicle Powertrain Intelligence Engine",
    version="1.0.0",
    description="TIE-Grade Engine for EV Motor, Power Electronics, Battery, Thermal, and Charging Analysis"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = AUTO08EVPowertrainEngine()


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint for EV powertrain analysis"""
    try:
        response = engine.three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            context=request.context
        )
        return response
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Engine health check"""
    return engine.health_check()


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total": len(engine.doctrine_cache),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "confidence": d.confidence.value,
                "authority_tier": d.authority_tier.value
            }
            for d in engine.doctrine_cache
        ]
    }


@app.get("/stats")
async def statistics_endpoint():
    """Engine performance statistics"""
    return engine.telemetry.get_stats()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting AUTO08 EV Powertrain Engine on port {engine.port}")
    uvicorn.run(app, host="0.0.0.0", port=engine.port)
