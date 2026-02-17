"""
ENRG12 Energy Storage Systems Intelligence Engine
TIE-Grade Implementation v1.0.0

Domain Coverage:
- Pumped Hydro Storage (PHS) design and operation
- Compressed Air Energy Storage (CAES) systems
- Flywheel Energy Storage Systems (FESS)
- Supercapacitor and ultracapacitor technologies
- Thermal Energy Storage (TES) systems
- Grid-scale storage economics and optimization
- Battery energy storage systems (BESS) integration
- Hybrid storage systems
- Storage arbitrage and ancillary services
- Round-trip efficiency optimization

Port: 9332
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict, Counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field
import uvicorn


# ═══════════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════════

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
    PUMPED_HYDRO = "PUMPED_HYDRO"
    CAES = "CAES"
    FLYWHEEL = "FLYWHEEL"
    SUPERCAPACITOR = "SUPERCAPACITOR"
    THERMAL_STORAGE = "THERMAL_STORAGE"
    BESS_INTEGRATION = "BESS_INTEGRATION"
    HYBRID_SYSTEMS = "HYBRID_SYSTEMS"
    GRID_ECONOMICS = "GRID_ECONOMICS"
    ARBITRAGE = "ARBITRAGE"
    ANCILLARY_SERVICES = "ANCILLARY_SERVICES"
    EFFICIENCY = "EFFICIENCY"
    SAFETY = "SAFETY"


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Energy storage analysis query")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis context zone")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    entity_scope: str
    adversarial_considerations: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    sources: List[str]
    reasoning_chain: List[str]
    triggered_doctrines: List[str]
    epistemic_flags: List[str]
    determinism_hash: str
    latency_ms: float
    mode: ResponseMode
    zone: AnalysisZone


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int


# ═══════════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ Energy Storage Expert Blocks
# ═══════════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Pumped Hydro Storage Fundamentals",
        keywords=["pumped hydro", "PHS", "reversible turbine", "upper reservoir", "lower reservoir", "head", "penstock"],
        conclusion_template=[
            "Pumped hydro storage (PHS) is the most mature and widely deployed grid-scale storage technology, representing over 95% of global energy storage capacity.",
            "PHS operates by pumping water from a lower reservoir to an upper reservoir during low-demand periods, then releasing it through turbines during peak demand.",
            "Round-trip efficiency typically ranges from 70-85%, with plant capacity ranging from 100 MW to 3,000+ MW."
        ],
        reasoning_framework="""
Pumped hydro storage design considerations:
1. Site selection requires significant elevation differential (minimum 100-300 meters head)
2. Upper and lower reservoir sizing based on energy capacity requirements (E = m*g*h)
3. Reversible pump-turbine selection or separate pump/turbine configurations
4. Penstock design for hydraulic efficiency and water hammer mitigation
5. Environmental impact assessment (aquatic ecosystems, land use, visual impact)
6. Seismic analysis and dam safety requirements
7. Transmission interconnection and grid integration studies
8. Economic analysis including capital cost ($1,000-$4,000/kW), O&M costs, and revenue streams
9. Permitting timeline (5-10 years typical) and stakeholder engagement
10. Operational flexibility: startup time 1-3 minutes, ramp rate up to 50% capacity/minute

Technical performance metrics:
- Energy capacity: Function of reservoir volume and head (E = rho*g*V*h/3600, MWh)
- Power capacity: Turbine-generator rating
- Discharge duration: Typically 4-12 hours at rated power
- Cycling capability: 50,000+ cycles over 50-100 year lifespan
- Black start capability: Yes (most PHS plants)
- Response time: Sub-1-minute for spinning reserve, 1-3 minutes from standstill
        """,
        key_factors=[
            "Topography and geology (head availability, reservoir siting)",
            "Water availability and environmental constraints",
            "Proximity to transmission infrastructure and load centers",
            "Round-trip efficiency (energy losses in pumping, turbine, and hydraulic systems)",
            "Operational flexibility and response time requirements",
            "Capital cost and project financing structure",
            "Regulatory and permitting requirements (FERC, state, environmental)",
            "Long-term O&M costs and equipment life"
        ],
        primary_authority=[
            "FERC Order 841 (energy storage participation in wholesale markets)",
            "IEEE 1881-2018 (pumped storage hydropower plant design)",
            "USACE Engineering Manual EM 1110-2-3001 (hydropower engineering)",
            "IEC 62930 (pumped storage power plants performance testing)",
            "ASCE Hydro Review technical publications"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Utilities, ISOs/RTOs, project developers, EPC contractors, regulatory agencies",
        adversarial_considerations="Environmental groups may challenge ecological impacts; local communities may oppose land use changes; cost overruns and schedule delays are common risks."
    ),

    DoctrineBlock(
        topic="Compressed Air Energy Storage (CAES) Technology",
        keywords=["CAES", "compressed air", "cavern storage", "diabatic", "adiabatic", "isothermal", "natural gas", "recuperator"],
        conclusion_template=[
            "CAES systems store energy by compressing air into underground caverns or above-ground vessels, then releasing it through turbines to generate electricity.",
            "Diabatic CAES (existing commercial plants) requires natural gas for reheating, while advanced adiabatic and isothermal CAES aim for fuel-free operation.",
            "Only two commercial-scale diabatic CAES plants exist worldwide (Huntorf, Germany 290 MW; McIntosh, Alabama 110 MW), both using salt caverns."
        ],
        reasoning_framework="""
CAES system architecture and design:
1. Compression train: Multi-stage intercooled compressors (efficiency 70-85%)
2. Storage volume: Underground cavern (salt dome, hard rock, aquifer) or above-ground vessels
3. Expansion train: Multi-stage turbines with reheating
4. Thermal management: Heat recovery, storage, or rejection strategy
5. Grid interconnection: Synchronous or inverter-based generation

CAES technology variants:
A. Diabatic CAES (D-CAES):
   - Compression heat rejected to atmosphere via intercoolers
   - Stored air at ambient temperature (40-80 bar in cavern)
   - Natural gas combustion during expansion to reheat air
   - Round-trip efficiency: 42-55% (including fuel energy)
   - Heat rate: 4,000-5,500 Btu/kWh (vs. 7,000-10,000 for simple cycle CT)

B. Adiabatic CAES (A-CAES):
   - Compression heat stored in thermal energy storage (TES) system
   - Stored heat used to reheat air during expansion (no fuel needed)
   - Round-trip efficiency: 65-75% (electricity-to-electricity)
   - Technical challenges: High-temperature TES (>600 deg C), heat exchanger design
   - No commercial deployments yet (multiple pilot projects)

C. Isothermal CAES (I-CAES):
   - Near-constant temperature compression/expansion via liquid piston or spray cooling
   - Lower pressure operation (10-30 bar), smaller temperature excursions
   - Round-trip efficiency: 70-80% (theoretical)
   - Above-ground storage possible (lower pressure reduces volume requirements)
   - Early-stage development (SustainX, LightSail Energy pilots discontinued)

Cavern storage considerations:
- Salt cavern: Best sealing, 100+ bar possible, solution mining required
- Hard rock: Lower pressure (60-80 bar), water seal or steel lining needed
- Aquifer: Porous rock formation, requires caprock seal, pressure limited
- Volume sizing: 1,000-10,000 cubic meters per MW-hour storage
        """,
        key_factors=[
            "Availability of suitable underground storage geology",
            "CAES variant selection (diabatic, adiabatic, isothermal) based on efficiency and fuel requirements",
            "Compression and expansion equipment efficiency and cost",
            "Thermal energy storage performance for A-CAES",
            "Natural gas infrastructure availability for D-CAES",
            "Storage pressure and volume requirements (function of energy capacity)",
            "Cavern integrity, sealing, and cycling durability",
            "Economic competitiveness vs. battery storage and peaker plants"
        ],
        primary_authority=[
            "DOE/EPRI CAES technical reports and feasibility studies",
            "ASME Boiler and Pressure Vessel Code (Section VIII for above-ground storage)",
            "API RP 1171 (functional integrity of natural gas storage in depleted hydrocarbon reservoirs and aquifer reservoirs)",
            "State public utility commission market participation rules",
            "EPA Clean Air Act permits (if combustion-based)"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="Utilities, grid operators, project developers, equipment manufacturers, geologists",
        adversarial_considerations="Unproven commercial viability of A-CAES and I-CAES; high capital cost; geological risk; competition from declining battery costs."
    ),

    DoctrineBlock(
        topic="Flywheel Energy Storage Systems",
        keywords=["flywheel", "FESS", "rotational inertia", "magnetic bearing", "vacuum chamber", "frequency regulation", "power quality"],
        conclusion_template=[
            "Flywheel energy storage systems store kinetic energy in a rotating mass, offering extremely fast response, high power density, and long cycle life.",
            "FESS excel at short-duration, high-cycle applications like frequency regulation, power quality, and uninterruptible power supply (UPS).",
            "Round-trip efficiency is 85-95%, with cycle life exceeding 100,000 full depth-of-discharge cycles and 20+ year operational life."
        ],
        reasoning_framework="""
Flywheel technology fundamentals:
1. Kinetic energy storage: E = 0.5 * I * omega^2, where I = moment of inertia, omega = angular velocity
2. Rotor design: Composite materials (carbon fiber) for high energy density, steel for lower cost
3. Magnetic bearings: Eliminate friction, enable vacuum operation
4. Vacuum containment: Reduces air resistance losses at high RPM (10,000-50,000 RPM)
5. Motor-generator: Bidirectional power conversion (charge/discharge)
6. Power electronics: Fast-switching inverters for grid interface

Performance characteristics:
- Energy capacity: Typically 3-100 kWh per flywheel unit
- Power capacity: 100 kW to 20 MW per unit (scalable via parallel units)
- Discharge duration: Seconds to 15 minutes (limited energy capacity)
- Response time: <4 milliseconds (sub-cycle response)
- Round-trip efficiency: 85-95% (minimal standby losses: 1-2%/hour)
- Cycle life: 100,000+ full cycles, 175,000+ at 80% DOD
- Operational life: 20+ years with minimal maintenance
- Ambient temperature range: -40 to +50 deg C (no performance degradation)

Grid application strengths:
- Frequency regulation (PJM RegD market leader before rule changes)
- Synthetic inertia and grid stabilization
- Power quality and voltage support
- UPS and microgrid applications
- Fast-ramping renewable firming (seconds to minutes)
- Transit systems (regenerative braking capture)

Technical limitations:
- High self-discharge rate limits long-duration storage
- Energy density lower than batteries (10-30 Wh/kg vs. 100-250 for Li-ion)
- Capital cost: $1,500-$6,000/kW (higher than batteries on energy basis)
- Safety: Catastrophic failure containment required (rotor burst)
        """,
        key_factors=[
            "Application match to flywheel strengths (high power, short duration, fast response)",
            "Cycle life requirements and frequency of charge-discharge events",
            "Ambient temperature and environmental conditions",
            "Maintenance requirements and operational simplicity",
            "Footprint and siting constraints (modular scalability)",
            "Safety systems for rotor containment",
            "Economic comparison to batteries for specific use case",
            "Grid interconnection requirements and market rules"
        ],
        primary_authority=[
            "IEEE 1547 (distributed energy resources interconnection)",
            "FERC Order 755 (frequency regulation compensation, later revised)",
            "UL 1741 (inverters, converters, controllers for use in independent power systems)",
            "Beacon Power, Amber Kinetics technical specifications and field data",
            "ISO/RTO frequency regulation market rules"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Grid operators, frequency regulation market participants, data centers, transit agencies, power quality customers",
        adversarial_considerations="Market rule changes (e.g., PJM RegD speed neutrality) have reduced flywheel competitiveness; battery cost declines threaten economic viability."
    ),

    DoctrineBlock(
        topic="Supercapacitor and Ultracapacitor Technology",
        keywords=["supercapacitor", "ultracapacitor", "EDLC", "pseudocapacitor", "power density", "fast charge", "pulse power"],
        conclusion_template=[
            "Supercapacitors (also called ultracapacitors or EDLCs) store energy electrostatically at the electrode-electrolyte interface, enabling extremely fast charge/discharge and very long cycle life.",
            "Supercapacitors bridge the gap between conventional capacitors (high power, low energy) and batteries (high energy, lower power), offering power density 10-100x higher than batteries.",
            "Typical applications include pulse power, regenerative braking, power buffering, and backup power for sub-minute durations."
        ],
        reasoning_framework="""
Supercapacitor electrochemical principles:
1. Electric Double-Layer Capacitors (EDLC): Energy stored at carbon electrode-electrolyte interface
2. Pseudocapacitors: Energy stored via fast surface redox reactions (higher energy density)
3. Hybrid capacitors: Combine EDLC and battery-like electrodes (lithium-ion capacitors)
4. Capacitance: C = epsilon*A/d, where A = electrode surface area, d = charge separation distance
5. Energy: E = 0.5*C*V^2; Power: P = V^2/(4*ESR), where ESR = equivalent series resistance

Performance metrics:
- Energy density: 1-10 Wh/kg (EDLC), 10-30 Wh/kg (hybrid capacitors)
- Power density: 5,000-10,000 W/kg (100x higher than Li-ion batteries)
- Round-trip efficiency: 90-98%
- Cycle life: 500,000 to 1,000,000+ cycles
- Operational life: 10-15 years
- Charge time: Seconds to minutes
- Operating temperature: -40 to +65 deg C (vs. -20 to +60 for Li-ion)
- Calendar life: Voltage and temperature dependent, ~10 years at rated conditions

Grid and energy storage applications:
A. Grid frequency regulation and stabilization:
   - Sub-second response to frequency deviations
   - Bridge storage between flywheels and batteries
   - Synthetic inertia for low-inertia grids (high renewables penetration)

B. Renewable energy smoothing:
   - Mitigate solar PV variability due to cloud transients (seconds to minutes)
   - Wind gust response and power quality improvement
   - Combined with batteries for multi-timescale smoothing

C. Transportation and industrial:
   - Regenerative braking in EVs, trams, cranes
   - Voltage stabilization in DC microgrids
   - Backup power for data centers, telecom (seconds to minutes)
   - Pulse power for rail acceleration, elevators

D. Hybrid storage systems:
   - Supercapacitor + battery: Supercap handles high-frequency cycling, extends battery life
   - Power-to-energy ratio optimization: Supercaps for power, batteries for energy

Economic considerations:
- Capital cost: $5,000-$20,000/kWh (energy basis), $100-$500/kW (power basis)
- Low O&M cost (no degradation from cycling)
- Cost-effective for high-cycle, short-duration applications
- Not competitive with batteries for energy storage (>15 minutes duration)
        """,
        key_factors=[
            "Application power-to-energy ratio (high P/E favors supercapacitors)",
            "Cycle life requirements and duty cycle characteristics",
            "Response time and ramp rate requirements",
            "Operating temperature range and environmental conditions",
            "Energy capacity needs (seconds to minutes discharge duration)",
            "Round-trip efficiency and standby losses",
            "Economic comparison to batteries and flywheels",
            "System integration architecture (standalone vs. hybrid)"
        ],
        primary_authority=[
            "IEC 62391-1 (fixed electric double layer capacitors for use in electronic equipment)",
            "IEEE 1679 (guide for the characterization and evaluation of lithium-based batteries in stationary applications - hybrid systems)",
            "Maxwell Technologies, Skeleton Technologies, Nippon Chemi-Con technical datasheets",
            "DOE Energy Storage Database (supercapacitor project data)",
            "SAE J2464 (electric and hybrid electric vehicle rechargeable energy storage system safety)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Grid operators, renewable developers, microgrid operators, EV manufacturers, industrial facilities, UPS vendors",
        adversarial_considerations="High cost per kWh limits addressable market; battery performance improvements encroach on supercapacitor territory; niche applications only."
    ),

    DoctrineBlock(
        topic="Thermal Energy Storage Systems",
        keywords=["thermal storage", "TES", "sensible heat", "latent heat", "phase change material", "PCM", "molten salt", "ice storage", "chilled water"],
        conclusion_template=[
            "Thermal energy storage (TES) systems store energy as heat or cold, enabling load shifting, renewable integration, and grid flexibility.",
            "TES technologies include sensible heat storage (water, molten salt), latent heat storage (phase change materials), and thermochemical storage.",
            "Applications range from HVAC load shifting (ice storage, chilled water) to concentrating solar power (CSP) plants and industrial process heat storage."
        ],
        reasoning_framework="""
Thermal energy storage classification:
1. Sensible heat storage: Energy stored as temperature change in a material (Q = m*Cp*delta_T)
2. Latent heat storage: Energy stored during phase change at constant temperature (Q = m*L_fusion or L_vaporization)
3. Thermochemical storage: Energy stored in reversible chemical reactions (highest energy density, least mature)

Technology variants and applications:

A. HVAC and Building Thermal Storage:
   - Ice storage: Freeze water during off-peak hours, melt during peak cooling demand
     * Energy density: ~80 kWh/m3 (latent heat of ice fusion: 334 kJ/kg)
     * Typical capacity: 1,000-10,000 ton-hours cooling
     * Round-trip efficiency: 80-90% (including chiller COP degradation)
     * Use case: Commercial building peak demand reduction, utility load shifting

   - Chilled water storage: Store cold water (39-45 deg F) in insulated tanks
     * Energy density: ~10-15 kWh/m3 (sensible heat, lower than ice)
     * Lower capital cost than ice, simpler integration
     * Stratified tanks maintain temperature differential

   - Hot water storage: District heating, solar thermal, CHP systems
     * Temperature range: 140-200 deg F (residential) to 200-350 deg F (industrial)
     * Pressurized tanks for higher temperature operation
     * Daily or seasonal storage (large underground tanks in Europe)

B. Concentrating Solar Power (CSP) Thermal Storage:
   - Molten salt storage (60% NaNO3, 40% KNO3): Industry standard for CSP plants
     * Operating temperature: 550-1,050 deg F (290-565 deg C)
     * Energy density: 50-80 kWh/m3 (sensible heat storage)
     * Storage duration: 4-15 hours at rated turbine output
     * Round-trip efficiency: 93-99% (thermal-to-thermal, excluding parasitic loads)
     * Freeze protection required (salt melts at 430 deg F/220 deg C)

   - Two-tank vs. thermocline storage:
     * Two-tank: Separate hot and cold salt tanks, higher efficiency, higher cost
     * Thermocline: Single tank with temperature gradient, lower cost, some mixing losses

   - CSP + storage economics: Enables dispatchable solar generation, capacity credit, post-sunset generation

C. Industrial Process Heat Storage:
   - High-temperature storage for cement, steel, chemical plants
   - Waste heat recovery and reuse (reduce fuel consumption)
   - Phase change materials (PCMs) for isothermal storage:
     * Salt hydrates, paraffins, metals (Al, Mg, Zn) for various temperature ranges
     * Higher energy density than sensible storage
     * Challenge: Thermal conductivity, cycling stability, cost

D. Grid-Scale Thermal-Electric Storage:
   - Carnot battery: Heat pump charges thermal storage, heat engine discharges to electricity
   - Pumped heat energy storage (PHES): Similar concept, various working fluids
   - Round-trip efficiency: 50-70% (limited by Carnot efficiency)
   - Early-stage development (Malta Inc., Siemens Gamesa Electric Thermal Energy Storage)

Economic and performance factors:
- Capital cost: $10-$50/kWh_thermal (sensible heat), $20-$100/kWh_thermal (PCM), $50-$150/kWh_electric (thermal-electric)
- Very low self-discharge (insulated tanks: <1%/day; underground seasonal storage: <10%/season)
- Long life: 20-30 years for tanks and heat exchangers
- No cycle degradation (unlike batteries)
        """,
        key_factors=[
            "Application temperature range and heating/cooling requirements",
            "Storage duration (hours, days, seasonal)",
            "Energy density requirements and available space",
            "Integration with existing systems (HVAC, CSP, industrial process)",
            "Round-trip efficiency including conversion losses",
            "Capital cost and economic payback from load shifting or energy arbitrage",
            "Freeze protection and thermal management for molten salt systems",
            "Environmental and safety considerations (non-toxic, non-flammable preferred)"
        ],
        primary_authority=[
            "ASHRAE Handbook - HVAC Applications (thermal storage chapter)",
            "DOE SunShot CSP Program thermal storage research and commercial plant data",
            "IEA Energy Storage Technology Roadmap (thermal storage section)",
            "NREL CSP thermal storage publications and techno-economic analysis",
            "Local utility rate structures and demand charge tariffs (economic drivers)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Building owners, utilities, CSP plant developers, industrial facilities, district heating/cooling operators",
        adversarial_considerations="Limited awareness and market penetration outside CSP; low energy density (sensible heat) requires large volumes; thermal-electric storage unproven at scale."
    ),

    DoctrineBlock(
        topic="Grid-Scale Storage Economics and Optimization",
        keywords=["energy arbitrage", "capacity market", "ancillary services", "LCOS", "NPV", "IRR", "degradation", "cycling", "merchant storage"],
        conclusion_template=[
            "Grid-scale energy storage economics depend on stacked revenue streams including energy arbitrage, capacity payments, and ancillary services.",
            "Levelized cost of storage (LCOS) is the key metric for comparing storage technologies, incorporating capital cost, efficiency, lifetime, and degradation.",
            "Optimal storage dispatch requires sophisticated optimization algorithms that balance revenue maximization, degradation management, and operational constraints."
        ],
        reasoning_framework="""
Revenue streams for grid-scale storage:

1. Energy Arbitrage (Time-Shifting):
   - Buy low-cost energy during off-peak hours, sell during peak hours
   - Revenue = (Price_peak - Price_offpeak) * Energy_discharged * eta_roundtrip - Degradation_cost
   - Market volatility and price spreads critical to economics
   - Duck curve in high-solar grids creates favorable arbitrage opportunities
   - Day-ahead and real-time market participation

2. Capacity Market Participation:
   - Receive payments for being available during system peak hours
   - ISO/RTO capacity markets (e.g., PJM, NYISO, ISO-NE)
   - Must demonstrate availability and performance (capacity testing)
   - Duration requirements: Typically 4-6 hours discharge at rated power
   - Payment: $50-$200/kW-year (varies by region and market conditions)

3. Ancillary Services:
   - Frequency regulation (automatic generation control, AGC)
     * Payment for capacity ($$/MW) + performance ($$/MW for actual regulation)
     * Fast-responding storage (batteries, flywheels) earn performance multipliers
     * FERC Order 755 (pay-for-performance, later revised) boosted storage economics
   - Spinning and non-spinning reserves
   - Voltage support and reactive power
   - Black start capability (rare, but high value if available)

4. Transmission and Distribution Deferral:
   - Avoid or delay costly transmission/distribution upgrades
   - Value = NPV of deferred infrastructure investment
   - Non-wires alternative (NWA) programs in some jurisdictions
   - Requires detailed engineering study and regulatory approval

5. Renewable Firming and Shaping:
   - Store excess renewable generation, dispatch when needed
   - Capture curtailed energy (negative pricing events)
   - Shape renewable output to match load or contract obligations
   - Investment Tax Credit (ITC) eligibility if charged 100% from renewables

Cost components and LCOS calculation:

Levelized Cost of Storage (LCOS) = (Capex_total + PV(Opex + Replacement)) / (PV(Energy_discharged) * eta)

Where:
- Capex_total = EPC cost + soft costs (development, permitting, interconnection, financing)
- Opex = Fixed O&M + Variable O&M + Insurance + Property tax
- Replacement = Battery replacement or major overhaul (mid-life)
- Energy_discharged = Annual discharged energy over project life, accounting for degradation
- eta = Round-trip efficiency
- PV = Present value using project discount rate

Key cost drivers:
- Battery/storage system capital cost: $200-$600/kWh (declining rapidly for Li-ion)
- Power conversion system (PCS/inverter): $100-$200/kW
- Balance of system (BOS): Containers, HVAC, site work, electrical: $50-$150/kWh
- Soft costs: Development, permitting, interconnection: $50-$200/kWh
- Fixed O&M: $10-$25/kW-year
- Augmentation/replacement: $100-$300/kWh (battery modules, 10-15 years into project)
- Insurance: 0.3-0.5% of capital cost per year
- Degradation impact: Reduced capacity and energy throughput over life

Degradation modeling:
- Calendar aging: Capacity fade over time (temperature and SOC dependent)
- Cycle aging: Capacity fade per equivalent full cycle (DOD dependent)
- Combined degradation model: Capacity(t) = f(calendar_age, cycle_count, temperature, SOC, DOD)
- Replacement trigger: Typically 70-80% of nameplate capacity (end of life)
- Augmentation strategy: Add new modules to maintain capacity vs. full replacement

Optimization strategies:

A. Perfect foresight (offline optimization):
   - Maximize NPV given known future prices (historical analysis or scenario)
   - Linear or mixed-integer programming
   - Understand theoretical revenue potential and inform bidding strategy

B. Predictive optimization (day-ahead, hour-ahead):
   - Forecast prices and market conditions
   - Optimize dispatch schedule considering degradation, SOC constraints, market rules
   - Update in real-time based on actual conditions
   - Machine learning for price forecasting

C. Real-time heuristic dispatch:
   - Rule-based control (e.g., charge when price < $X, discharge when price > $Y)
   - Simple, robust, but suboptimal
   - Useful as fallback or for simple arbitrage-only applications

D. Multi-objective optimization:
   - Balance revenue, degradation, operational risk
   - Pareto frontier of revenue vs. degradation
   - Decision-maker preference weighting

Market and regulatory considerations:
- ISO/RTO tariff rules on storage participation
- FERC Order 841 (storage participation in wholesale markets)
- State-level storage mandates and incentives (CA, NY, MA, NJ)
- Interconnection queue position and network upgrade costs
- Tax incentives: ITC, PTC (if coupled with renewables), depreciation (MACRS)
        """,
        key_factors=[
            "Market price volatility and arbitrage opportunities",
            "Availability of capacity and ancillary service markets",
            "Storage technology round-trip efficiency and degradation characteristics",
            "Capital cost and financing terms (interest rate, debt/equity ratio, tax equity)",
            "Operational strategy and dispatch optimization sophistication",
            "Regulatory framework and market design (FERC orders, state policies)",
            "Transmission interconnection cost and timeline",
            "Revenue uncertainty and merchant risk vs. contracted revenue (PPA, tolling agreement)"
        ],
        primary_authority=[
            "FERC Order 841 (electric storage resource participation in markets operated by RTOs and ISOs)",
            "FERC Order 755 (frequency regulation compensation in organized wholesale power markets, later revised)",
            "ISO/RTO tariffs and market participation rules (PJM, CAISO, ERCOT, NYISO, ISO-NE, MISO, SPP)",
            "NREL and Lazard LCOS studies and benchmarking reports",
            "State public utility commission storage policies and mandates",
            "IRS tax code (ITC eligibility for storage paired with renewables)",
            "Academic literature on storage optimization (operations research journals)"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="Storage developers, utilities, IPPs, investors, grid operators, regulators, energy traders",
        adversarial_considerations="Market rule changes can destroy project economics overnight (e.g., PJM RegD); degradation uncertainty creates revenue risk; declining battery costs create value erosion for existing assets."
    ),

    DoctrineBlock(
        topic="Battery Energy Storage System (BESS) Integration",
        keywords=["BESS", "lithium-ion", "inverter", "BMS", "DC-coupled", "AC-coupled", "solar plus storage", "islanding", "black start"],
        conclusion_template=[
            "Battery energy storage systems (BESS) have become the dominant grid-scale storage technology due to rapidly declining lithium-ion battery costs and modular scalability.",
            "BESS integration requires careful design of the battery management system (BMS), power conversion system (PCS), thermal management, and grid interconnection.",
            "Co-location with renewable generation (solar + storage, wind + storage) enables optimized energy capture, firming, and ITC eligibility."
        ],
        reasoning_framework="""
BESS system architecture:

1. Battery subsystem:
   - Battery chemistry: Li-ion (NMC, LFP, NCA), flow battery, lead-acid, Na-ion (emerging)
   - Cell → Module → Rack → Container hierarchy
   - Energy capacity: kWh to MWh scale per container
   - Power capacity: Defined by PCS rating (C-rate: power/energy ratio)
   - Voltage range: 600-1500 VDC typical (utility-scale)

2. Battery Management System (BMS):
   - Cell voltage and temperature monitoring
   - State of charge (SOC) and state of health (SOH) estimation
   - Balancing control (passive or active cell balancing)
   - Safety limits: Overcurrent, overvoltage, undervoltage, overtemperature protection
   - Communication with PCS and plant controller (Modbus, CAN)

3. Power Conversion System (PCS):
   - Bidirectional DC-AC inverter
   - Grid-forming or grid-following capability
   - Reactive power control (voltage support)
   - Ride-through capability (LVRT, HVRT per grid code)
   - Efficiency: 95-98% (one-way), 90-96% round-trip AC-AC

4. Thermal management:
   - Liquid cooling (glycol, refrigerant) for high C-rate or hot climates
   - Air cooling (HVAC) for moderate climates and lower C-rate
   - Target battery temperature: 15-35 deg C (optimal performance and life)
   - Derating required if ambient temperature outside design range

5. Monitoring and control system:
   - Supervisory control and data acquisition (SCADA)
   - Energy management system (EMS): Dispatch optimization, SOC management
   - Communication with grid operator (DNP3, IEC 61850)
   - Cybersecurity (NERC CIP compliance for bulk electric system)

6. Fire suppression and safety:
   - Smoke and gas detection (thermal runaway early warning)
   - Clean agent fire suppression (Novec 1230, FM-200) or water mist
   - Thermal runaway propagation prevention (inter-module barriers)
   - UL 9540A fire safety testing standard

DC-coupled vs. AC-coupled solar + storage:

DC-coupled (shared inverter):
- Solar PV DC output → DC bus → Battery DC → Inverter → AC grid
- Single inverter (lower cost, higher efficiency for solar-to-battery charging)
- Limited operational flexibility (battery can only charge from solar + grid import via inverter)
- ITC eligibility straightforward (battery charged exclusively from solar)

AC-coupled (separate inverters):
- Solar PV → Inverter 1 → AC grid; Battery → Inverter 2 → AC grid
- Greater operational flexibility (battery can charge from solar or grid independently)
- Higher cost (two inverters), slightly lower efficiency (two DC-AC conversions for solar-to-battery)
- ITC eligibility requires metering to prove 100% solar charging in first 5 years (or proportional ITC)

Grid interconnection and operation:

- Interconnection agreement: Define interconnection point, capacity, technical requirements
- Interconnection study: System impact study, facilities study (grid upgrade costs)
- Facility rating: Gross capacity (inverter AC rating) vs. net capacity (accounting for losses)
- Operating modes:
  * Grid-following: Synchronize to grid frequency, export/import real and reactive power
  * Grid-forming: Create voltage and frequency reference (islanded microgrids, black start)
  * Voltage and frequency ride-through (grid code compliance)
  * Anti-islanding protection (detect grid loss, cease energizing)

Black start capability:
- Ability to energize de-energized grid section without external power
- BESS well-suited (can start immediately, unlike thermal plants)
- Cranking path design: Sequence of breaker closures to energize grid stepwise
- Coordination with thermal generation (BESS starts grid, thermal plants synchronize)

Islanding and microgrid operation:
- Seamless transition from grid-connected to islanded mode
- Maintain voltage and frequency within limits during island (grid-forming control)
- Load shedding if generation insufficient (under-frequency load shedding)
- Re-synchronization and reconnection to main grid

Degradation management in BESS:
- Cycle depth: Deeper discharge (higher DOD) → faster degradation
- Operating temperature: High temperature accelerates calendar and cycle aging
- Charge/discharge rate (C-rate): Higher C-rate increases degradation
- SOC window restriction: Operate between 10-90% SOC (vs. 0-100%) to extend life
- Warranty structure: Throughput (MWh) or time-based, with capacity retention guarantee (e.g., 70% at 10 years)
        """,
        key_factors=[
            "Battery chemistry selection based on energy vs. power needs, cost, safety, and life",
            "Power-to-energy ratio (C-rate) design: 0.25C (4-hour) to 4C (15-minute) systems",
            "DC-coupled vs. AC-coupled architecture for solar + storage",
            "BMS design and SOC/SOH estimation accuracy",
            "Thermal management system sizing for climate and duty cycle",
            "Fire safety and thermal runaway mitigation (UL 9540A testing)",
            "Grid code compliance (voltage/frequency ride-through, reactive power capability)",
            "Degradation modeling and warranty structure",
            "Interconnection cost and timeline",
            "ITC eligibility and tax equity financing structure (if paired with solar)"
        ],
        primary_authority=[
            "IEEE 1547-2018 (standard for interconnecting distributed energy resources with electric power systems)",
            "UL 9540 (energy storage systems and equipment) and UL 9540A (test method for evaluating thermal runaway fire propagation)",
            "NERC PRC-024-3 (generator frequency and voltage protective relay settings)",
            "NERC CIP standards (cybersecurity for bulk electric system)",
            "IRS ITC guidance for energy storage paired with solar (Notice 2018-59)",
            "Inverter manufacturers (SMA, Sungrow, PowerElectronics, TMEIC) technical specifications",
            "Battery OEM datasheets and warranty terms (Tesla, LG, CATL, BYD, Samsung SDI)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="BESS developers, utilities, solar + storage developers, EPC contractors, grid operators, AHJs (fire marshal, building department)",
        adversarial_considerations="Fire safety concerns drive increased regulation and costs; interconnection delays and upgrade costs can kill projects; ITC recapture risk if charging from grid."
    ),

    DoctrineBlock(
        topic="Hybrid Storage Systems and Multi-Technology Optimization",
        keywords=["hybrid storage", "battery plus flywheel", "supercapacitor battery", "power energy decoupling", "stacked services", "complementary"],
        conclusion_template=[
            "Hybrid storage systems combine two or more storage technologies to optimize performance across multiple timescales and applications.",
            "Common hybrids include battery + supercapacitor (power/energy decoupling), battery + flywheel (extended cycle life), and PHS + battery (long + short duration).",
            "Hybrid systems can deliver stacked revenue streams more cost-effectively than single-technology solutions by matching technology strengths to service requirements."
        ],
        reasoning_framework="""
Rationale for hybrid storage:

1. Power-energy decoupling:
   - High-power technology (supercapacitor, flywheel) handles fast transients and high-rate cycling
   - High-energy technology (battery) handles sustained discharge and bulk energy storage
   - Extends battery life by offloading high-rate, high-cycle duty to complementary technology

2. Multi-timescale service provision:
   - Sub-second to seconds: Supercapacitor, flywheel (frequency regulation, power quality)
   - Minutes to hours: Battery (energy arbitrage, firming, capacity)
   - Hours to days: PHS, CAES (long-duration storage, seasonal shifting)

3. Cost optimization:
   - Match expensive high-performance technology ($/kWh) to short-duration needs (small kWh required)
   - Match cheaper technology ($/kW) to long-duration needs (large kWh required)
   - Overall system LCOS lower than single technology for multi-service application

Common hybrid architectures:

A. Battery + Supercapacitor:
   - Supercap handles high-frequency cycling (seconds), battery handles energy (minutes-hours)
   - Configuration 1: Parallel DC bus (both connected to same inverter via DC-DC converters)
   - Configuration 2: Supercap on DC bus, battery on AC bus (AC-coupled)
   - Control strategy: Supercap responds to fast signals, battery to slow signals (frequency separation)
   - Application: Renewable smoothing (supercap for seconds, battery for minutes), EV fast charging (supercap peak shaving)
   - Performance benefit: 2-5x battery cycle life extension, improved round-trip efficiency
   - Economic challenge: Supercap capital cost ($/kWh) limits economic optimality to narrow applications

B. Battery + Flywheel:
   - Flywheel handles high-cycle regulation (AGC), battery handles energy arbitrage
   - Installed together at same site, coordinated dispatch via plant controller
   - Application: PJM RegD market (before rule change), CAISO regulation market
   - Performance benefit: Flywheel earns high performance payments, battery provides energy capacity
   - Economic challenge: Flywheel capex, market rule changes reduce value proposition

C. Pumped Hydro + Battery:
   - PHS provides long-duration (8-12 hour) storage, battery provides fast response (seconds-minutes)
   - PHS handles daily arbitrage, battery handles frequency regulation and reserves
   - Application: High-renewable grids needing both fast response and long duration
   - Example: Australia (Snowy 2.0 PHS + multiple large BESS projects in NEM)
   - Performance benefit: Complementary timescales, stacked services maximize value
   - Geographic constraint: PHS requires specific topography, limits deployment

D. Thermal Storage + Battery:
   - Thermal storage (ice, hot water) handles HVAC load shifting (hours to day)
   - Battery handles power quality, backup, or electric arbitrage
   - Application: Commercial buildings, microgrids, district heating/cooling
   - Performance benefit: Lower combined cost than battery-only for multi-service needs
   - Control coordination: Building energy management system (BEMS) optimizes both

E. Flow Battery + Lithium-Ion Battery:
   - Flow battery provides 6-10 hour duration (cheap $/kWh, independent power/energy sizing)
   - Li-ion provides 1-2 hour duration (high efficiency, fast response, lower capex for short duration)
   - Application: Multi-duration resource adequacy (CAISO proposed long-duration RFO)
   - Performance benefit: Optimize $/kW and $/kWh separately for different discharge durations
   - Development status: Emerging (flow battery cost and performance improving)

Control and optimization of hybrid systems:

1. Hierarchical control architecture:
   - Plant-level controller: Receives grid signals, market dispatch, optimizes revenue
   - Technology-level controller: Manages each storage technology (BMS, flywheel controller, etc.)
   - Inter-technology coordination: Allocate signals to appropriate technology based on frequency content

2. Frequency separation filter:
   - High-pass filter → fast technology (supercap, flywheel)
   - Low-pass filter → slow technology (battery, PHS)
   - Tuning: Filter cutoff frequency balances performance and technology utilization

3. SOC management:
   - Prevent technology from reaching SOC limits (maintain operational flexibility)
   - Rebalancing strategy: Use slow technology to recharge fast technology during low-value periods
   - Example: Battery recharges supercapacitor to 50% SOC during night, both ready for day

4. Degradation-aware dispatch:
   - Minimize battery cycling by offloading high-cycle duty to flywheel/supercap
   - Track cumulative battery cycles and enforce throughput warranty limits
   - Real-time cost of degradation ($$/cycle) influences dispatch optimization

Economic analysis of hybrid systems:

- Hybrid NPV = Revenue_stacked - Capex_hybrid - Opex_hybrid - PV(Replacement_hybrid)
- Compare to single-technology NPV for same services
- Hybrid economically justified if: NPV_hybrid > NPV_single_tech_A AND NPV_hybrid > NPV_single_tech_B
- Sensitivity analysis: Revenue uncertainty, technology cost evolution, market rule changes

Challenges and barriers:
- Control complexity: Coordinating multiple technologies requires sophisticated algorithms
- Interconnection: Utility and ISO/RTO may not have tariff framework for hybrid resources (improving)
- Financing: Lenders less familiar with hybrid systems, perceived technology risk
- O&M: Multiple technologies → multiple maintenance contracts, spare parts inventory
- Market rules: Some markets prohibit co-located resources from bidding as single resource (evolving)
        """,
        key_factors=[
            "Application requirements across multiple timescales (seconds to hours)",
            "Technology cost trends and relative $/kW vs. $/kWh economics",
            "Control system sophistication and technology coordination algorithms",
            "Market rules on hybrid resource participation and revenue stacking",
            "Degradation characteristics and complementary cycling behavior",
            "Site constraints (footprint, interconnection capacity)",
            "O&M complexity and multi-vendor support",
            "Financing and lender acceptance of hybrid technology risk"
        ],
        primary_authority=[
            "FERC Notice of Proposed Rulemaking (NOPR) on hybrid resources (Docket No. RM24-9-000)",
            "CAISO Hybrid Resources Initiative stakeholder process and tariff revisions",
            "DOE Energy Storage Grand Challenge (research on hybrid and long-duration storage)",
            "IEEE publications on hybrid energy storage control strategies",
            "Academic literature (IEEE Transactions on Power Systems, Energy journals)",
            "Hybrid project case studies (Hornsdale Power Reserve + wind farm, etc.)"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="Storage developers, utilities, grid operators, researchers, equipment manufacturers, regulators",
        adversarial_considerations="Unproven economic advantage in most markets; control complexity creates risk; market rule uncertainty; difficult financing due to novelty."
    ),

    DoctrineBlock(
        topic="Long-Duration Energy Storage (LDES) Technologies",
        keywords=["long duration", "LDES", "flow battery", "hydrogen", "iron-air", "gravity storage", "seasonal storage", "multi-day"],
        conclusion_template=[
            "Long-duration energy storage (LDES), typically defined as 8+ hours to days or weeks, is critical for deep decarbonization and grid reliability in high-renewable scenarios.",
            "Emerging LDES technologies include flow batteries, hydrogen storage, iron-air batteries, compressed CO2 storage, and gravity-based systems.",
            "LDES economics depend on capturing infrequent but high-value events (multi-day heat waves, wind lulls, seasonal mismatches), requiring different financial models than Li-ion."
        ],
        reasoning_framework="""
LDES technology landscape and characteristics:

1. Flow Batteries (Vanadium Redox, Zinc-Bromine, Iron-Chromium):
   - Power and energy capacity independently scalable (tank size vs. stack size)
   - Electrolyte stored in external tanks, pumped through electrochemical stack
   - Vanadium redox flow battery (VRFB): Most mature, 10,000+ cycles, 65-75% efficiency
   - Zinc-bromine: Lower cost electrolyte, complexity in managing dendrite formation
   - Duration: 4-12 hours typical, scalable to 24+ hours economically
   - Capital cost: $300-$600/kWh (target <$200/kWh for competitiveness)
   - Advantages: Long life, no capacity fade, non-flammable, recyclable electrolyte
   - Challenges: Lower energy density than Li-ion, higher balance of plant cost, parasitic losses (pumps)

2. Hydrogen Energy Storage (Electrolysis + Storage + Fuel Cell or Turbine):
   - Electrolyzer: Convert excess renewable electricity to H2 (PEM, alkaline, solid oxide)
   - Storage: Compressed H2 tanks, underground cavern, or chemical carrier (ammonia, LOHC)
   - Reconversion: Fuel cell (40-60% efficiency) or combustion turbine (30-40% efficiency)
   - Round-trip efficiency: 30-50% (electricity-to-H2-to-electricity)
   - Duration: Days to months (limited by storage capacity, not technology)
   - Capital cost: $500-$1,500/kW (electrolyzer + fuel cell), $5-$20/kWh (storage, highly variable)
   - Advantages: Seasonal storage capability, leverages existing natural gas infrastructure (blending), decarbonizes hard-to-electrify sectors
   - Challenges: Low round-trip efficiency, high cost, hydrogen embrittlement, safety (flammability), lack of infrastructure
   - Use case: Long-duration backup (>24 hours), renewable curtailment capture, sector coupling

3. Iron-Air Batteries (Form Energy, etc.):
   - Electrochemistry: Reversible rusting of iron (Fe + O2 ↔ Fe2O3)
   - Discharge: Iron oxidizes (rusts), releases energy
   - Charge: Apply current to reduce rust back to iron
   - Duration: 100+ hours discharge at rated power (multi-day storage)
   - Capital cost target: <$20/kWh (leverages cheap iron and air)
   - Round-trip efficiency: ~50% (lower than Li-ion, but acceptable for infrequent use)
   - Advantages: Extremely low-cost materials, non-flammable, recyclable, long duration
   - Challenges: Low efficiency, large footprint, slow response, unproven at scale (first projects under construction 2023-2024)
   - Use case: Multi-day reliability backstop (replace peaker plants for rare events)

4. Compressed CO2 Energy Storage:
   - Compress CO2 to liquid or supercritical state, store in tanks or underground
   - Expand through turbine to generate electricity (similar to CAES, but uses CO2 as working fluid)
   - Advantages: Higher energy density than compressed air, no combustion required
   - Challenges: Early-stage development, efficiency and cost unproven
   - Developer: Energy Dome (Italy), pilot projects operational

5. Gravity-Based Storage (Energy Vault, Gravitricity):
   - Store energy by lifting mass against gravity, release by lowering mass
   - Energy Vault: Crane lifts composite blocks, stacks them (potential energy storage)
   - Gravitricity: Hoist weight in abandoned mine shaft
   - Round-trip efficiency: 75-85%
   - Advantages: Long life, no degradation, simple concept
   - Challenges: High capex, low energy density, unproven economics, requires specific geography (mine shafts) or large footprint
   - Status: Demonstration projects, limited commercial deployment

6. Liquid Air Energy Storage (LDES) - Highview Power:
   - Liquefy air using excess electricity (cryogenic process, -196 deg C)
   - Store liquid air in insulated tanks
   - Regasify air and expand through turbine to generate electricity
   - Round-trip efficiency: 50-60%
   - Duration: 8-24+ hours
   - Advantages: Uses mature cryogenic technology, non-hazardous working fluid
   - Challenges: Complexity, efficiency, cost, footprint
   - Status: Pilot plants operational (UK), first utility-scale project under construction

Economic drivers and market fit for LDES:

- Capacity credit: Value of ensuring adequacy during multi-day low-renewable periods
  * Example: California ELCC studies show 8-hour storage has higher capacity credit than 4-hour
  * Iron-air 100-hour storage could achieve ~95% capacity credit (vs. ~60% for 4-hour Li-ion)

- Energy arbitrage: Infrequent but extreme price spikes during heat waves, polar vortex
  * Example: Texas Feb 2021 freeze (ERCOT prices $9,000/MWh for days)
  * Low cycling frequency acceptable for LDES (50-100 cycles/year vs. 250+ for Li-ion arbitrage)

- Renewable curtailment capture: Store GWh-scale excess generation during low-demand seasons
  * Example: California spring solar curtailment (negative prices, GWh curtailed)
  * Hydrogen or multi-day LDES can capture and time-shift to summer peak

- LCOS for LDES: Must account for low utilization (capacity factor 5-20% vs. 30-60% for Li-ion)
  * Fixed costs (capex, fixed O&M) dominate economics
  * Low $/kWh critical, $/kW and efficiency less critical than for Li-ion
  * Target: <$50/kWh for flow batteries, <$20/kWh for iron-air, $5-$20/kWh for hydrogen storage

Policy and market design for LDES:

- Duration-differentiated procurement (California, New York)
  * AB 2514 (CA): 1,325 MW energy storage mandate, subset for long-duration
  * NYSERDA long-duration storage RFP (pilot projects)

- Capacity market reforms to value duration
  * PJM, NYISO considering extended performance requirements (6-10 hours)

- Federal support: DOE Long Duration Storage Shot (90% cost reduction target, $0.05/kWh)
  * Funding for demonstration projects, R&D, manufacturing scale-up
        """,
        key_factors=[
            "Application duration requirements (hours, days, seasonal)",
            "Utilization frequency and capacity factor (daily cycling vs. rare events)",
            "Round-trip efficiency vs. energy capacity cost trade-off",
            "Technology maturity and commercial track record",
            "Footprint and siting constraints (energy density)",
            "Integration with renewable generation profile (solar, wind, seasonal)",
            "Market design and policy support for long-duration value",
            "Capital cost trajectory and cost reduction potential"
        ],
        primary_authority=[
            "DOE Long Duration Storage Shot (LDES initiative and targets)",
            "NREL LDES technical and economic analysis reports",
            "California Energy Commission IEPR proceedings on long-duration storage",
            "NYSERDA long-duration energy storage roadmap and solicitations",
            "MIT Energy Initiative Future of Energy Storage study (LDES chapter)",
            "IEA Energy Storage Technology Roadmap (long-duration section)",
            "Form Energy, Highview Power, Energy Dome technical whitepapers and project announcements"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="Utilities, grid planners, renewable developers, LDES technology vendors, policymakers, research institutions, investors",
        adversarial_considerations="Technology immaturity and unproven economics; low round-trip efficiency concerns; uncertain market value and revenue streams; long payback periods challenge financing."
    ),

    DoctrineBlock(
        topic="Storage Siting and Environmental Considerations",
        keywords=["siting", "environmental impact", "permitting", "land use", "visual impact", "noise", "NEPA", "CEQA", "wetlands", "endangered species"],
        conclusion_template=[
            "Energy storage siting requires careful consideration of land use, environmental impacts, community acceptance, and permitting timelines.",
            "Key environmental issues include land disturbance, visual impact, noise (from HVAC and transformers), stormwater management, and fire risk.",
            "Permitting timelines vary widely (6 months to 3+ years) depending on technology, scale, location, and environmental review requirements (NEPA, CEQA, state/local)."
        ],
        reasoning_framework="""
Siting considerations by storage type:

1. Utility-Scale Battery Storage:
   - Footprint: 1-3 acres per 10-20 MWh (container-based systems)
   - Setbacks: Typically 50-300 feet from property lines (fire safety, noise)
   - Visual impact: Low-profile containers (8-10 feet tall), screening with landscaping or fencing
   - Noise: HVAC systems, transformers (40-60 dBA at property line), may require noise walls
   - Fire safety: Clearance zones, access roads for fire department, water supply (hydrants)
   - Stormwater: Impervious surface (containers, pads) triggers stormwater management plan
   - Environmental review: Typically categorical exclusion or mitigated negative declaration (unless sensitive habitat)

2. Pumped Hydro Storage:
   - Footprint: Large (100s to 1000s of acres for reservoirs, dams, powerhouse)
   - Environmental impacts: Habitat alteration, aquatic ecosystems, wetlands, visual, recreation
   - Permitting: Major federal (FERC license, Army Corps 404 permit, NEPA EIS) and state processes
   - Timeline: 5-10 years (stakeholder engagement, studies, environmental review, appeals)
   - Mitigation: Fish passage, habitat restoration, recreation enhancements, downstream flow requirements
   - Public opposition: Often significant (land use, recreation, environmental groups)

3. CAES (Underground Cavern):
   - Footprint: Small surface footprint (compressor/turbine building, substation), large underground volume
   - Geology: Requires suitable salt dome, hard rock, or aquifer (geological survey and testing required)
   - Environmental: Groundwater impact assessment, subsidence risk, brine disposal (salt cavern solution mining)
   - Permitting: State oil and gas commission or equivalent (underground storage), EPA UIC permit (injection wells)
   - Community concerns: Groundwater contamination risk, seismic activity, industrialization of rural areas

4. Thermal Storage (Molten Salt, Ice, Chilled Water):
   - Footprint: Moderate (tanks, chillers, heat exchangers)
   - Environmental: Minimal if at existing industrial or power plant site
   - Chemical handling: Molten salt (nitrates) requires spill containment, safety protocols
   - Permitting: Local building permits, potentially state air quality permit (if combustion equipment)
   - Integration: Often co-located with CSP plant or district energy system (reduces incremental permitting)

Environmental review process:

Federal (if federal funding, federal land, or federal permit):
- National Environmental Policy Act (NEPA)
  * Categorical Exclusion (CatEx): Minimal environmental impact, no EA or EIS required
  * Environmental Assessment (EA): Moderate potential impact, 6-18 months, results in FONSI or EIS
  * Environmental Impact Statement (EIS): Significant impact likely, 2-5 years, detailed alternatives analysis
  * Lead agency: DOE (if DOE funding), Army Corps (404 permit), FERC (hydropower)

State (California example):
- California Environmental Quality Act (CEQA)
  * Categorical Exemption: Ministerial projects, existing facilities, minor changes
  * Negative Declaration (ND) or Mitigated Negative Declaration (MND): No significant impact or mitigated impacts, 6-12 months
  * Environmental Impact Report (EIR): Significant impact, 1-3 years, public scoping, alternatives, mitigation monitoring
  * Lead agency: Local jurisdiction (county, city) or state agency (CEC for thermal plants >50 MW)

Key environmental issues assessed:

1. Land Use and Planning:
   - Consistency with general plan, zoning, and comprehensive plan
   - Agricultural land conversion (prime farmland, Williamson Act in CA)
   - Scenic resources and visual impact (viewshed analysis, simulations)
   - Compatibility with surrounding uses (residential, commercial, industrial)

2. Biological Resources:
   - Endangered and threatened species (federal ESA, state equivalents)
   - Critical habitat designation and consultation (USFWS, NOAA Fisheries)
   - Migratory birds (Migratory Bird Treaty Act)
   - Wetlands and waters of the U.S. (Clean Water Act Section 404 permit)
   - Habitat connectivity and wildlife corridors

3. Cultural and Tribal Resources:
   - Historical resources (buildings, structures, sites >50 years old)
   - Archaeological resources (survey, testing, mitigation)
   - Tribal consultation (AB 52 in CA, NHPA Section 106 federal)
   - Sacred sites and traditional cultural properties

4. Hazards and Safety:
   - Fire risk (battery thermal runaway, wildfire ignition potential)
   - Seismic hazards (fault rupture, ground shaking, liquefaction)
   - Flooding (100-year floodplain, dam inundation)
   - Hazardous materials (batteries, electrolyte, oils) storage and spill prevention

5. Noise:
   - Baseline noise survey
   - Operational noise modeling (HVAC, transformers, inverters)
   - Construction noise (temporary)
   - Compliance with local noise ordinance (often 50-60 dBA daytime, 40-50 dBA nighttime at property line)

6. Air Quality:
   - Construction emissions (fugitive dust, equipment exhaust)
   - Operational emissions (minimal for batteries, significant for CAES with combustion)
   - Greenhouse gas emissions (CEQA in CA, state climate action plans)

7. Traffic and Transportation:
   - Construction traffic (heavy trucks, worker commute)
   - Operational traffic (minimal for most storage)
   - Road damage and improvement requirements

Stakeholder engagement and community acceptance:

- Early outreach: Inform neighbors, community groups, local officials before formal application
- Public meetings: Present project, answer questions, address concerns
- Community benefits: Local jobs, tax revenue, grid reliability improvements
- Opposition management: Fire safety concerns (battery storage), visual impact, property values
- Local hire and workforce development commitments can build support
        """,
        key_factors=[
            "Site selection considering environmental constraints (wetlands, habitat, cultural resources)",
            "Zoning and land use consistency with local plans",
            "Environmental review pathway (CatEx, EA/ND, EIS/EIR) and timeline",
            "Fire safety and setback requirements for battery storage",
            "Community engagement and addressing local concerns (noise, visual, safety)",
            "Mitigation measures and monitoring commitments",
            "Permitting agency coordination (local, state, federal)",
            "Project schedule risk from permitting delays and litigation"
        ],
        primary_authority=[
            "NEPA (42 U.S.C. 4321 et seq.) and CEQ regulations",
            "CEQA (California Public Resources Code Section 21000 et seq.) and CEQA Guidelines",
            "Clean Water Act Section 404 (wetlands and waters of the U.S.)",
            "Endangered Species Act (16 U.S.C. 1531 et seq.)",
            "National Historic Preservation Act Section 106",
            "Local zoning ordinances and general plans",
            "NFPA 855 (standard for installation of stationary energy storage systems, fire safety)",
            "UL 9540A (fire safety test method for ESS)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Project developers, utilities, environmental consultants, permitting agencies, community stakeholders, tribal governments",
        adversarial_considerations="Environmental groups may challenge habitat impacts; community opposition to battery fire risk; permitting delays can exceed 2 years; litigation risk from CEQA/NEPA challenges."
    ),

    DoctrineBlock(
        topic="Round-Trip Efficiency Analysis and Optimization",
        keywords=["round-trip efficiency", "RTE", "losses", "parasitic load", "inverter efficiency", "self-discharge", "HVAC", "auxiliary"],
        conclusion_template=[
            "Round-trip efficiency (RTE) is the ratio of energy discharged to energy charged, accounting for all conversion, storage, and parasitic losses.",
            "Battery storage RTE is typically 85-95% (AC-to-AC), while mechanical storage (PHS, CAES, flywheel) ranges from 70-85%, and emerging LDES technologies 30-75%.",
            "Optimizing RTE requires minimizing conversion losses (inverter, transformer), storage losses (self-discharge, thermal), and parasitic loads (HVAC, BMS, controls)."
        ],
        reasoning_framework="""
Round-trip efficiency breakdown by storage type:

1. Lithium-Ion Battery Storage:
   - Inverter (PCS) efficiency: 96-98% one-way, 92-96% round-trip (AC-DC-AC)
   - Battery charge-discharge efficiency: 95-98% (coulombic efficiency)
   - Auxiliary loads (BMS, HVAC, controls): 1-3% of throughput
   - Self-discharge: 1-3% per month (minimal for daily cycling)
   - Total AC-to-AC RTE: 85-95% (typical 88-92% for deployed systems)
   - Temperature impact: Lower efficiency at temperature extremes (derating)

2. Pumped Hydro Storage:
   - Pump efficiency: 88-92%
   - Turbine efficiency: 90-94%
   - Hydraulic losses (penstock friction, inlet/outlet): 2-5%
   - Evaporation and seepage: <1% (negligible for short-term cycles)
   - Auxiliary loads (controls, gates, transformer): <1%
   - Total RTE: 70-85% (typical 75-80%)
   - Variable-speed pump-turbine technology improves efficiency vs. fixed-speed

3. Compressed Air Energy Storage:
   - Compression efficiency: 70-85% (intercooled multi-stage)
   - Expansion efficiency: 80-90% (with reheat)
   - Thermal losses: 10-30% (compression heat rejected in diabatic CAES)
   - Cavern leakage: <1% per month
   - Auxiliary loads: 2-4%
   - Diabatic CAES RTE: 42-55% (electricity-to-electricity, not including fuel energy input)
   - Adiabatic CAES RTE (theoretical): 65-75% (heat recovery and reuse)

4. Flywheel Energy Storage:
   - Motor-generator efficiency: 95-98% round-trip
   - Bearing losses: Minimal (magnetic bearings in vacuum)
   - Windage losses: <1% (vacuum enclosure)
   - Self-discharge: 1-2% per hour (significant for long-duration storage)
   - Power electronics efficiency: 96-98%
   - Total RTE: 85-95% (for discharge within minutes to hours)
   - Standby losses dominate for idle storage (limits long-duration applications)

5. Supercapacitor:
   - ESR losses: 2-5% per charge-discharge cycle
   - Power electronics efficiency: 96-98%
   - Self-discharge: 10-40% per month (high leakage current)
   - Total RTE: 90-98% (for fast cycling applications)

6. Thermal Energy Storage:
   - Ice storage: 80-90% RTE (accounting for chiller COP degradation during ice-making)
   - Molten salt (CSP): 93-99% RTE (thermal-to-thermal, minimal heat losses from well-insulated tanks)
   - Carnot battery (thermal-electric): 50-70% RTE (limited by Carnot efficiency of heat engine)

7. Emerging LDES:
   - Hydrogen (electrolysis + fuel cell): 30-50% RTE
   - Iron-air battery: ~50% RTE
   - Liquid air energy storage: 50-60% RTE
   - Flow batteries: 65-80% RTE

Efficiency optimization strategies:

1. Inverter and transformer sizing:
   - Operate inverter near peak efficiency point (typically 40-80% of rated capacity)
   - Oversizing inverter reduces efficiency at light loads
   - High-efficiency transformers (99%+) for grid interconnection

2. Battery thermal management:
   - Maintain optimal temperature range (15-35 deg C for Li-ion)
   - Liquid cooling more efficient than air cooling in hot climates
   - Pre-cooling before high-rate discharge reduces resistance losses
   - Minimize HVAC parasitic loads (insulation, economizer modes)

3. Power electronics optimization:
   - Silicon carbide (SiC) or gallium nitride (GaN) devices (higher efficiency than silicon IGBTs)
   - Synchronous rectification (reduce diode losses)
   - Soft-switching techniques (reduce switching losses)

4. SOC management:
   - Avoid extreme SOC ranges (0-10%, 90-100%) where resistance is higher
   - Operate in mid-SOC range (20-80%) for best efficiency (if energy capacity allows)

5. Auxiliary load reduction:
   - Energy-efficient HVAC (variable-speed fans, economizers, nighttime cooling)
   - Low-power BMS and control systems
   - Transformer no-load losses (use high-efficiency units)
   - Standby mode for idle storage (power down non-essential systems)

6. C-rate optimization:
   - Lower charge-discharge rate (C-rate) reduces resistive losses (I^2*R)
   - Trade-off: Lower C-rate requires larger energy capacity (higher capex) for same power rating
   - Economic optimization: Balance $/kW vs. $/kWh considering market revenue and efficiency

7. Self-discharge minimization:
   - Battery chemistry selection (LFP lower self-discharge than NMC)
   - Cool storage temperature reduces self-discharge rate
   - Periodic top-up charging for long-term idle storage

Impact of efficiency on economics:

- Revenue impact: RTE directly multiplies arbitrage revenue (e.g., 90% RTE → earn 90% of price spread)
- Degradation: Higher losses → more energy cycled through battery → faster degradation
- Market competitiveness: 5% RTE difference can swing project NPV by 10-20%
- Operational strategy: Low RTE technologies (hydrogen, iron-air) only economic for infrequent use (high value events)

Example calculation:
- Battery BESS: 100 MWh energy capacity, 90% RTE, $40/MWh off-peak, $100/MWh peak
- Daily arbitrage revenue: 100 MWh * 0.9 * ($100 - $40) = $5,400/day
- Annual (300 cycles): $1,620,000/year
- If RTE degrades to 85% over time: $1,530,000/year (-5.6% revenue)
        """,
        key_factors=[
            "Technology-specific efficiency characteristics and loss mechanisms",
            "Operating conditions (temperature, C-rate, SOC range) impact on efficiency",
            "Auxiliary load minimization strategies",
            "Power electronics and inverter efficiency optimization",
            "Trade-off between capital cost (larger system) and efficiency (smaller losses)",
            "Market application and cycling frequency (RTE more critical for high-cycle apps)",
            "Degradation impact on long-term efficiency",
            "Measurement and verification of RTE (site acceptance testing)"
        ],
        primary_authority=[
            "IEC 61427-2 (secondary batteries for renewable energy storage - performance tests)",
            "IEC 62933-2-1 (electrical energy storage systems - unit parameters and testing methods - general)",
            "IEEE 1679 (guide for characterization and evaluation of lithium-based batteries in stationary applications)",
            "Inverter manufacturers (SMA, Sungrow, etc.) efficiency curves and datasheets",
            "Battery cell datasheets (coulombic efficiency, internal resistance) from OEMs",
            "EPRI energy storage performance testing protocols"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Storage developers, EPC contractors, utilities, equipment manufacturers, testing labs, O&M providers",
        adversarial_considerations="Efficiency degradation over life reduces revenue; manufacturers may overstate RTE in marketing materials; field performance often lower than lab-tested values."
    ),

    DoctrineBlock(
        topic="Storage Safety Standards and Fire Protection",
        keywords=["battery fire", "thermal runaway", "UL 9540", "UL 9540A", "NFPA 855", "fire suppression", "FM-200", "Novec", "water mist"],
        conclusion_template=[
            "Battery energy storage systems pose fire and safety risks, particularly lithium-ion batteries which can undergo thermal runaway leading to fire and toxic gas release.",
            "UL 9540, UL 9540A, and NFPA 855 establish safety standards for ESS installation, testing, and fire protection requirements.",
            "Fire protection strategies include early detection (smoke, gas, temperature), suppression (clean agent, water mist), and propagation prevention (module spacing, barriers)."
        ],
        reasoning_framework="""
Battery fire hazards and thermal runaway:

1. Thermal runaway mechanism (lithium-ion):
   - Initiating event: Internal short circuit, overcharge, external heat, mechanical abuse
   - Exothermic reactions: SEI layer breakdown, electrolyte decomposition, cathode oxygen release
   - Temperature rise: Cell temperature exceeds 150-200 deg C, self-heating accelerates
   - Venting: Pressure buildup → safety vent opens → flammable gas release (CO, CO2, H2, hydrocarbons)
   - Ignition: Vented gas ignites (if ignition source or sufficient temperature), flames exit vent
   - Propagation: Heat from burning cell → adjacent cells → cascading thermal runaway

2. Hazards from battery fires:
   - Intense heat: Cell temperatures 500-1000 deg C, flames 1000+ deg C
   - Toxic gases: HF (from electrolyte salt LiPF6), CO, CO2, VOCs (health hazard, firefighter risk)
   - Re-ignition: Cells can re-ignite hours or days after initial fire (off-gassing continues)
   - Water reactivity: Lithium metal fires react with water (rare in Li-ion, more concern for Li-metal batteries)
   - Electrical hazard: Energized DC and AC systems present shock and arc flash risk

Safety standards and testing:

1. UL 9540 (Energy Storage Systems and Equipment):
   - Product-level safety certification: Battery, inverter, BMS, ESS unit (container)
   - Testing: Electrical safety, mechanical integrity, environmental (temperature, humidity, altitude)
   - Thermal abuse testing: Overcharge, over-discharge, short circuit, heat exposure
   - Does NOT include fire propagation testing at unit or installation level (that's UL 9540A)

2. UL 9540A (Test Method for Evaluating Thermal Runaway Fire Propagation in Battery Energy Storage Systems):
   - Four-tier cascading failure test:
     * Tier 1: Cell-level thermal runaway (induced by heater)
     * Tier 2: Module-level propagation (does cell-to-cell propagation occur?)
     * Tier 3: Unit-level propagation (does module-to-module propagation occur in a rack/container?)
     * Tier 4: Installation-level propagation (does unit-to-unit propagation occur, e.g., container-to-container?)
   - Measurements: Gas species (CO, CO2, HF, etc.), temperatures, fire spread, time to events
   - Results inform fire protection design: Suppression type, detection, ventilation, spacing

3. NFPA 855 (Standard for Installation of Stationary Energy Storage Systems):
   - Adopted 2020, updated 2023 (major revisions for Li-ion safety)
   - Installation requirements:
     * Spacing between ESS units (10 feet separation or 1-hour fire barrier)
     * Room size limits (600 kWh per room for indoor Li-ion, unless sprinklered and meets deflagration venting)
     * Ventilation (mechanical ventilation, gas detection interlock)
     * Fire detection (smoke, heat, gas detection required)
     * Fire suppression (automatic suppression required for Li-ion >50 kWh indoors)
     * Emergency response plan and training for AHJs
   - Outdoor installations: Fewer restrictions, but still require spacing, access, and suppression
   - Deflagration venting: Pressure relief for rapid gas release (prevent container explosion)

4. IFC (International Fire Code) Appendix Z - Energy Storage Systems:
   - Adopted by many jurisdictions alongside NFPA 855
   - Prescriptive requirements similar to NFPA 855

Fire protection strategies:

A. Fire Detection:
   - Multi-sensor approach: Smoke (optical, ionization), heat (rate-of-rise, fixed temperature), gas (CO, VOCs)
   - Early warning: Detect thermal runaway before flame (off-gassing precedes fire by minutes)
   - Gas detection: Continuous monitoring, alarm at low thresholds (ppm levels for H2, CO)
   - Thermal imaging: Infrared cameras for hot spot detection (pre-thermal runaway)

B. Fire Suppression Systems:
   - Clean agent systems (Novec 1230, FM-200, Sapphire):
     * Gaseous suppressants, electrically non-conductive, no residue
     * Effectiveness: Extinguish flame, but may not cool cells enough to prevent re-ignition
     * Design concentration: 4-6% by volume, discharge in <10 seconds
     * Limited effectiveness on deep-seated battery fires (agent doesn't penetrate battery core)

   - Water mist systems:
     * Fine water droplets (cooling + oxygen displacement)
     * Effectiveness: Better cooling than clean agents, can prevent propagation
     * Concerns: Electrical safety (de-energize first), water damage to electronics
     * Design: High-pressure (1500+ psi) or low-pressure systems, nozzle coverage

   - Aerosol suppression (emerging):
     * Solid particulate aerosol (potassium compound), extinguishes flame and cools
     * Compact, no pressurized cylinders
     * Unproven for large-scale BESS

   - Water deluge (last resort, outdoor or firefighter response):
     * Large volumes of water to cool battery (prevent propagation)
     * Not practical for automatic system (water damage)
     * Firefighter tactic: Defensive cooling, prevent spread to adjacent structures

C. Propagation Prevention:
   - Module spacing and barriers: Physical separation and thermal barriers between modules
   - Rack-level fire barriers: Steel or fire-rated panels between racks within container
   - Container separation: 10+ feet between containers (NFPA 855), or fire-rated wall
   - Vent design: Direct off-gas away from adjacent units and ignition sources
   - Load-bearing collapse prevention: Ensure structure remains intact during fire (firefighter safety)

D. Emergency Response Planning:
   - Pre-fire planning with local fire department: Site walkthrough, hazard briefing, access
   - Emergency response guide: Electrical isolation procedure, suppression system manual operation
   - Thermal runaway monitoring: Real-time alerts to fire department (integration with fire alarm panel)
   - Re-entry protocols: Wait period after fire (24-48 hours), gas monitoring before entry

Lessons from BESS fire incidents:

- Arizona APS McMicken fire (2019): 2 MW/2 MWh BESS, explosion during firefighter response (4 injured)
  * Root cause: Module-level thermal runaway, vented gas accumulated, deflagration upon door opening
  * Changes: Improved gas detection, deflagration venting, enhanced fire suppression, firefighter training

- South Korea ESS fires (2017-2019): 29 fires in 3 years
  * Root causes: Poor installation quality, electrical faults, inadequate BMS protection
  * Changes: Mandatory UL 9540A testing, improved installation standards, enhanced monitoring

- Tesla Megapack fire (Moss Landing, CA, 2021): 300 MW/1,200 MWh facility
  * Fire contained to single Megapack unit (propagation prevented by design)
  * Cause under investigation (likely cell-level defect or electrical fault)
        """,
        key_factors=[
            "Compliance with UL 9540, UL 9540A, and NFPA 855 standards",
            "Fire detection system design (multi-sensor, early warning)",
            "Fire suppression system selection and sizing (clean agent, water mist, or hybrid)",
            "Thermal runaway propagation prevention (spacing, barriers, venting)",
            "Emergency response planning and AHJ coordination",
            "Battery chemistry safety profile (LFP safer than NMC, NCA)",
            "BMS protection functions and fault detection algorithms",
            "Installation quality and commissioning (prevent electrical faults)",
            "Insurance requirements and risk assessment"
        ],
        primary_authority=[
            "UL 9540 (standard for energy storage systems and equipment)",
            "UL 9540A (test method for evaluating thermal runaway fire propagation in battery energy storage systems)",
            "NFPA 855 (standard for installation of stationary energy storage systems)",
            "International Fire Code (IFC) Appendix Z - Energy Storage Systems",
            "NFPA 70 (National Electrical Code, Article 706 - Energy Storage Systems)",
            "OSHA regulations on hazardous materials and electrical safety",
            "Local fire marshal and AHJ requirements"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="BESS developers, EPC contractors, AHJs (fire marshal, building department), fire protection engineers, battery manufacturers, insurance underwriters",
        adversarial_considerations="Fire incidents drive increased regulation and costs; AHJs may impose requirements beyond NFPA 855; community opposition to battery projects due to fire risk; insurance may be expensive or unavailable for non-compliant systems."
    ),

    # Additional doctrines to reach 25+ blocks
    DoctrineBlock(
        topic="Storage Interconnection and Grid Integration",
        keywords=["interconnection", "PPA", "ISO", "RTO", "grid code", "reactive power", "LVRT", "HVRT", "IEEE 1547", "black start"],
        conclusion_template=[
            "Energy storage interconnection to the grid requires compliance with IEEE 1547, regional grid codes, and ISO/RTO market participation rules.",
            "Interconnection studies (system impact, facilities study) determine required network upgrades and costs, which can range from minimal to tens of millions of dollars.",
            "Storage must provide grid support functions including voltage regulation (reactive power), frequency response, and ride-through during grid disturbances."
        ],
        reasoning_framework="""
Interconnection process:
1. Submit interconnection application to utility or ISO/RTO
2. Feasibility study: Preliminary assessment of grid impact and upgrade needs
3. System impact study: Detailed power flow, short circuit, stability analysis
4. Facilities study: Engineer specific network upgrades, cost estimate
5. Interconnection agreement: Finalize terms, cost allocation, construction schedule
6. Network upgrades: Build transmission/distribution upgrades (if required)
7. Commissioning and testing: Verify performance and grid code compliance
8. Commercial operation: Begin market participation or PPA delivery

Timeline: 1-3 years typical (can be longer if major upgrades or queue position issues)

Grid code compliance requirements:
- Voltage and frequency ride-through (LVRT, HVRT, UFRT, OFRT)
- Reactive power capability (power factor 0.95 leading to 0.95 lagging typical)
- Active power control (ramp rate limits, frequency-droop response)
- Communication and monitoring (SCADA, telemetry to grid operator)
- Protection systems (anti-islanding, overvoltage, undervoltage, frequency)
        """,
        key_factors=[
            "Interconnection queue position and study timeline",
            "Network upgrade costs and cost allocation (developer vs. utility)",
            "Point of interconnection selection (transmission vs. distribution)",
            "Grid code compliance requirements (IEEE 1547, NERC, ISO/RTO)",
            "Reactive power and voltage support capability",
            "Ride-through and frequency response performance"
        ],
        primary_authority=[
            "IEEE 1547-2018 (interconnection of distributed energy resources)",
            "FERC Order 2003 and 2023 (interconnection procedures)",
            "ISO/RTO tariffs and business practice manuals",
            "NERC reliability standards (PRC, VAR, BAL, etc.)",
            "Utility electric tariffs and interconnection handbooks"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Storage developers, utilities, transmission owners, ISO/RTOs, interconnection study consultants",
        adversarial_considerations="Interconnection queue delays and cost uncertainty; network upgrade costs can exceed project capex; rule changes can strand assets."
    ),

    DoctrineBlock(
        topic="Storage Market Participation and Revenue Stacking",
        keywords=["capacity market", "frequency regulation", "energy arbitrage", "ancillary services", "reserve", "demand response", "REC", "stacking"],
        conclusion_template=[
            "Revenue stacking—participating in multiple grid service markets simultaneously—is critical to energy storage project economics.",
            "Key markets include energy arbitrage, capacity, frequency regulation, spinning/non-spinning reserves, and voltage support.",
            "Market rules on dual participation, telemetry, and performance requirements vary by ISO/RTO and can limit stacking opportunities."
        ],
        reasoning_framework="""
Revenue stream categories:
1. Energy arbitrage: Buy low, sell high (day-ahead and real-time markets)
2. Capacity market: Payments for availability during peak hours or system stress
3. Ancillary services:
   - Frequency regulation (AGC): Fast response to frequency deviations
   - Spinning reserves: Synchronized generation ready in <10 minutes
   - Non-spinning reserves: Generation ready in <10-30 minutes
   - Voltage support: Reactive power for voltage regulation
4. Demand response: Load reduction payments during peak events
5. Transmission/distribution deferral: Value of avoiding infrastructure upgrades
6. Renewable firming: PPA premium for dispatchable renewable energy

Stacking constraints and opportunities:
- Simultaneous participation: Some ISOs allow regulation + energy market (CAISO), others restrict (PJM)
- SOC management: Must maintain sufficient SOC to deliver on all committed services
- Telemetry and control: ISO may require direct dispatch control (limits self-scheduling)
- Performance penalties: Underperformance results in reduced payments or penalties
        """,
        key_factors=[
            "ISO/RTO market design and revenue stacking rules",
            "Storage operational flexibility (SOC, response time, duration)",
            "Market price volatility and revenue predictability",
            "Telemetry and dispatch control requirements",
            "Performance incentives and penalties",
            "Optimization algorithm sophistication for multi-market bidding"
        ],
        primary_authority=[
            "FERC Order 841 (storage participation in RTO/ISO markets)",
            "ISO/RTO tariffs (CAISO, PJM, ERCOT, NYISO, ISO-NE, MISO)",
            "FERC Order 755 (frequency regulation compensation)",
            "State PUC market participation rules",
            "DOE and national lab storage market analysis reports"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="Storage developers, energy traders, utilities, market operators, optimizers",
        adversarial_considerations="Market rule changes eliminate revenue streams (e.g., PJM RegD speed neutrality); price suppression from storage oversupply; performance risk and penalties."
    ),

    DoctrineBlock(
        topic="Storage Degradation Modeling and Warranty Structures",
        keywords=["degradation", "capacity fade", "cycle life", "calendar aging", "warranty", "throughput", "EOL", "augmentation"],
        conclusion_template=[
            "Battery storage degrades over time due to calendar aging (time-based) and cycle aging (usage-based), reducing capacity and increasing resistance.",
            "Degradation modeling is essential for accurate revenue forecasting, warranty compliance, and replacement planning.",
            "Warranty structures typically guarantee minimum capacity retention (e.g., 70% at 10 years) and/or energy throughput (e.g., 50,000 MWh over warranty period)."
        ],
        reasoning_framework="""
Degradation mechanisms (Li-ion):
1. Calendar aging: Capacity loss over time (even if unused)
   - Drivers: Storage temperature, SOC level (higher SOC = faster aging)
   - Rate: 2-3% per year typical (varies by chemistry, temp, SOC)
2. Cycle aging: Capacity loss per charge-discharge cycle
   - Drivers: Depth of discharge (DOD), C-rate, temperature
   - Rate: 0.01-0.05% per equivalent full cycle (varies widely)
3. Resistance increase: Internal resistance rises, reducing efficiency and power capability
4. End of life: Typically defined as 70-80% of original capacity

Degradation modeling approaches:
- Empirical models: Curve-fit to manufacturer data or field measurements
- Semi-empirical models: Physics-informed equations (Arrhenius, power-law)
- Electrochemical models: Detailed physics (SEI growth, lithium plating) - computationally intensive

Warranty structures:
- Capacity retention: 70% at 10 years, 60% at 15 years (typical)
- Throughput: 50,000 MWh (varies by product and application)
- Dual trigger: Whichever comes first (time or throughput)
- Exclusions: Abuse, non-recommended operating conditions void warranty
        """,
        key_factors=[
            "Degradation model accuracy and validation against field data",
            "Operating strategy impact on degradation (SOC window, C-rate, temperature)",
            "Warranty terms and replacement trigger conditions",
            "Augmentation vs. full replacement cost and timing",
            "Economic impact of degradation on revenue and LCOS",
            "Battery chemistry degradation characteristics (LFP vs. NMC)"
        ],
        primary_authority=[
            "Battery manufacturer datasheets and warranty documents",
            "IEEE 1679 (battery characterization and testing)",
            "Academic literature on Li-ion degradation (Journal of Power Sources, Electrochimica Acta)",
            "NREL Battery Lifetime Models and tools",
            "Field data from operating projects (publicly reported or via aggregators)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Storage developers, asset owners, O&M providers, battery manufacturers, investors, lenders",
        adversarial_considerations="Manufacturer degradation claims often optimistic; field performance worse than lab; warranty claims difficult to enforce; replacement costs create NPV risk."
    ),

    DoctrineBlock(
        topic="Seasonal and Multi-Day Storage Applications",
        keywords=["seasonal storage", "multi-day", "winter peak", "polar vortex", "heatwave", "renewable variability", "100% renewable", "reliability"],
        conclusion_template=[
            "Seasonal and multi-day storage is required to address extended periods of low renewable generation (e.g., winter cold snaps, multi-day wind lulls) in high-renewable grids.",
            "Technologies suited for seasonal storage include pumped hydro (if reservoir size allows), hydrogen, and emerging long-duration technologies (iron-air, flow batteries).",
            "Economics depend on capturing infrequent but high-value reliability events, requiring different financial models than daily-cycling storage."
        ],
        reasoning_framework="""
Seasonal storage drivers:
- Renewable energy seasonal mismatch: Excess solar in spring/summer, deficit in winter
- Multi-day weather events: Polar vortex (low solar + wind), heat dome (high demand + low wind)
- 100% renewable grids: Need weeks of storage to ensure reliability during worst-case conditions

Storage duration requirements by scenario:
- Daily smoothing: 4-8 hours (Li-ion battery adequate)
- Multi-day reliability: 24-100 hours (emerging LDES needed)
- Seasonal shifting: Weeks to months (hydrogen, very large PHS only viable options today)

Economic challenges:
- Low capacity factor: Seasonal storage used 10-50 times per year (vs. 300+ for daily arbitrage)
- High $/kWh requirement: Must be <$20/kWh to be cost-effective (vs. $200-400 for Li-ion)
- Revenue uncertainty: Reliability value hard to quantify, depends on rare events
        """,
        key_factors=[
            "Grid renewable penetration level and seasonal generation profile",
            "Historical weather patterns and worst-case duration analysis",
            "Storage duration requirements (hours, days, weeks)",
            "Technology cost on $/kWh basis for long duration",
            "Revenue mechanisms (capacity market, reliability contracts, socialized cost)",
            "Alternative solutions (inter-regional transmission, demand response, firm low-carbon generation)"
        ],
        primary_authority=[
            "NREL Cambium scenarios for future grid conditions",
            "CAISO, NYISO, ISO-NE long-term resource adequacy studies",
            "MIT Energy Initiative Future of Energy Storage report (seasonal storage chapter)",
            "Princeton Net-Zero America study (seasonal storage requirements)",
            "State energy plans (CA, NY, MA) with high renewable targets"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="Grid planners, policymakers, LDES developers, utilities, renewable developers, researchers",
        adversarial_considerations="Uncertain economics and technology maturity; alternative solutions may be cheaper (transmission, nuclear); political risk if costs too high."
    ),

    DoctrineBlock(
        topic="Distributed vs. Centralized Storage Deployment",
        keywords=["distributed storage", "centralized", "behind-the-meter", "BTM", "front-of-meter", "FTM", "community storage", "aggregation", "VPP"],
        conclusion_template=[
            "Storage can be deployed at centralized utility-scale sites (front-of-meter) or distributed behind customer meters (BTM) or on distribution feeders.",
            "Centralized storage benefits from economies of scale, simpler market participation, and utility ownership models, but lacks distribution benefits.",
            "Distributed storage provides local benefits (voltage support, distribution deferral, resilience) but faces higher $/kW costs and aggregation complexity."
        ],
        reasoning_framework="""
Centralized (front-of-meter) storage:
- Location: Transmission-connected or distribution substation
- Scale: 10-300 MW typical, up to 3 GW (Moss Landing)
- Ownership: Utility, IPP, merchant developer
- Revenue: Wholesale market participation (energy, capacity, ancillary services)
- Benefits: Economies of scale, ISO/RTO market access, bulk energy shifting
- Challenges: Transmission upgrade costs, siting (land acquisition, permitting), no distribution benefits

Distributed (behind-the-meter) storage:
- Location: Customer premises (residential, C&I)
- Scale: 5-20 kWh (residential), 100-1000 kWh (C&I)
- Ownership: Customer, third-party (via lease or PPA)
- Revenue: Demand charge reduction, time-of-use arbitrage, backup power, VPP aggregation
- Benefits: Customer bill savings, resilience, no transmission costs, rapid deployment
- Challenges: High $/kW cost (small scale), complex aggregation, telemetry/control, customer acquisition cost

Community storage (distribution-connected, front-of-meter):
- Location: Distribution feeder (neighborhood scale)
- Scale: 500 kW - 5 MW
- Ownership: Utility or third-party
- Revenue: Distribution services (voltage support, peak shaving, deferral) + market participation
- Benefits: Distribution benefits, lower cost than BTM, serves multiple customers
- Challenges: Utility regulatory approval, cost recovery mechanism

Virtual Power Plant (VPP) aggregation:
- Aggregate 100s-1000s of BTM storage systems into single market resource
- Dispatch coordinated by VPP operator (e.g., Tesla, Sunrun, Stem)
- Participate in wholesale markets (capacity, demand response, ancillary services)
- Challenges: Communication, control reliability, customer opt-out, ISO/RTO market rules
        """,
        key_factors=[
            "Scale economies vs. distribution benefits trade-off",
            "Ownership model and financing (utility rate-base, third-party, customer)",
            "Market access and revenue opportunities (wholesale vs. retail)",
            "Aggregation technology and VPP platform maturity",
            "Regulatory framework (utility ownership rules, cost recovery)",
            "Customer value proposition (bill savings, resilience, environmental)"
        ],
        primary_authority=[
            "FERC Order 2222 (DER aggregation in wholesale markets)",
            "State PUC proceedings on utility storage ownership and rate-basing",
            "California Self-Generation Incentive Program (SGIP) for BTM storage",
            "VPP case studies (Tesla VPP in South Australia, Green Mountain Power in Vermont)",
            "IEEE 1547 (distributed resource interconnection)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Utilities, storage developers, VPP operators, regulators, customers (residential and C&I)",
        adversarial_considerations="Utility resistance to third-party ownership; regulatory uncertainty on cost recovery; VPP coordination challenges; cybersecurity risks."
    ),

    DoctrineBlock(
        topic="Storage and Renewable Integration Strategies",
        keywords=["solar plus storage", "wind plus storage", "firming", "curtailment", "capacity credit", "ITC", "hybrid", "co-location"],
        conclusion_template=[
            "Co-locating energy storage with renewable generation (solar + storage, wind + storage) improves renewable capacity credit, captures curtailed energy, and enables firm power contracts.",
            "DC-coupled solar + storage shares a single inverter (lower cost), while AC-coupled systems have separate inverters (more flexibility).",
            "Federal Investment Tax Credit (ITC) applies to storage if charged 100% from co-located renewable generation (or proportional ITC if partially grid-charged)."
        ],
        reasoning_framework="""
Benefits of renewable + storage co-location:
1. Increased capacity credit: Storage dispatches renewable energy during system peak (higher resource adequacy value)
2. Curtailment capture: Store excess renewable generation during low-demand or negative-price periods
3. Firming and shaping: Deliver consistent power profile (e.g., 6-hour block) regardless of solar/wind variability
4. Transmission utilization: Share interconnection capacity, avoid separate upgrade costs
5. ITC eligibility: Storage qualifies for federal ITC (30% through 2032) if charged from renewables

DC-coupled vs. AC-coupled solar + storage:
- DC-coupled: Solar → Battery → Inverter → Grid (single inverter, higher efficiency, lower cost, less flexibility)
- AC-coupled: Solar → Inverter1 → Grid; Battery → Inverter2 → Grid (independent operation, more flexibility, higher cost)

Operational strategies:
- Energy shifting: Charge from solar midday, discharge during evening peak
- Capacity delivery: Ensure availability during system peak hours (for capacity market)
- Frequency regulation: Fast response using battery (solar cannot provide)
- Curtailment avoidance: Charge when grid congestion would curtail solar

ITC considerations:
- Standalone storage: No ITC (unless charged 100% from renewables)
- Co-located storage: Full ITC if charged 100% from co-located solar in first 5 years
- Proportional ITC: Charge X% from solar → receive X% of ITC (requires metering to prove)
- Recapture risk: If grid-charging exceeds allowed amount, must repay portion of ITC
        """,
        key_factors=[
            "Renewable generation profile and storage duration sizing",
            "DC-coupled vs. AC-coupled architecture trade-offs",
            "ITC eligibility and grid-charging limitations",
            "Capacity credit methodology (ELCC, UCAP) in regional market",
            "Curtailment risk and negative pricing frequency",
            "Interconnection capacity sharing and upgrade costs",
            "PPA structure (firm vs. as-available energy delivery)"
        ],
        primary_authority=[
            "IRS Notice 2018-59 (ITC for energy storage paired with solar)",
            "FERC Order 845 (interconnection process reforms, including storage)",
            "State RPS and clean energy procurement rules",
            "ISO/RTO capacity accreditation methodologies (ELCC, UCAP)",
            "Solar + storage PPA and offtake agreement templates"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Renewable developers, storage developers, utilities, tax equity investors, offtakers, grid operators",
        adversarial_considerations="ITC recapture risk if grid-charging exceeds limits; capacity credit may be lower than expected; market price cannibalization as solar + storage penetration increases."
    )
]


# ═══════════════════════════════════════════════════════════════════════════════
# ENGINE CORE
# ═══════════════════════════════════════════════════════════════════════════════

class ENRG12Engine:
    def __init__(self):
        self.doctrine_cache = DOCTRINE_CACHE
        self.query_count = 0
        self.start_time = datetime.now()
        self.metrics = {
            "total_queries": 0,
            "cache_hits": 0,
            "deep_analysis_count": 0,
            "avg_latency_ms": 0.0
        }
        logger.info(f"ENRG12 Energy Storage Systems Engine initialized with {len(self.doctrine_cache)} doctrines")

    def normalize_query(self, query: str) -> str:
        """Normalize energy storage terminology for semantic matching."""
        query_lower = query.lower()

        # Technology aliases
        replacements = {
            "phs": "pumped hydro storage",
            "bess": "battery energy storage system",
            "ess": "energy storage system",
            "caes": "compressed air energy storage",
            "fess": "flywheel energy storage",
            "tes": "thermal energy storage",
            "ldes": "long duration energy storage",
            "vrfb": "vanadium redox flow battery",
            "deg c": "degrees celsius",
            "deg f": "degrees fahrenheit",
            "rte": "round-trip efficiency",
            "soc": "state of charge",
            "doe": "depth of discharge",
            "c-rate": "charge rate",
            "kw": "kilowatt",
            "mw": "megawatt",
            "kwh": "kilowatt-hour",
            "mwh": "megawatt-hour"
        }

        for old, new in replacements.items():
            query_lower = query_lower.replace(old, new)

        return query_lower

    def search_doctrines(self, query: str, top_k: int = 3) -> List[DoctrineBlock]:
        """Search doctrine cache for relevant blocks."""
        query_normalized = self.normalize_query(query)
        query_terms = set(query_normalized.split())

        scored_doctrines = []
        for doctrine in self.doctrine_cache:
            # Calculate relevance score
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_normalized)
            topic_match = 3 if any(term in doctrine.topic.lower() for term in query_terms) else 0

            score = keyword_matches * 2 + topic_match

            if score > 0:
                scored_doctrines.append((score, doctrine))

        # Sort by score and return top K
        scored_doctrines.sort(key=lambda x: x[0], reverse=True)
        return [d[1] for d in scored_doctrines[:top_k]]

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> QueryResponse:
        """
        TIE-20 Component: Three-layer response architecture.
        Layer 1: Doctrine cache (0-200ms)
        Layer 2: Semantic retrieval (fallback)
        Layer 3: Deep analysis (if needed)
        """
        start_time = datetime.now()

        # Layer 1: Doctrine cache search
        relevant_doctrines = self.search_doctrines(query, top_k=3)

        if relevant_doctrines:
            self.metrics["cache_hits"] += 1
            response = self._build_response_from_doctrines(
                query, relevant_doctrines, mode, zone
            )
        else:
            # Layer 2/3: Deep analysis fallback
            self.metrics["deep_analysis_count"] += 1
            response = self._deep_analysis(query, mode, zone)

        # Calculate latency
        latency_ms = (datetime.now() - start_time).total_seconds() * 1000
        response.latency_ms = latency_ms

        # Update metrics
        self.metrics["total_queries"] += 1
        self.metrics["avg_latency_ms"] = (
            (self.metrics["avg_latency_ms"] * (self.metrics["total_queries"] - 1) + latency_ms)
            / self.metrics["total_queries"]
        )

        return response

    def _build_response_from_doctrines(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> QueryResponse:
        """Build response from doctrine cache hits."""

        # Synthesize answer from doctrine conclusions
        if mode == ResponseMode.FAST:
            answer_parts = [doctrines[0].conclusion_template[0]]
        elif mode == ResponseMode.DEFENSE:
            answer_parts = []
            for d in doctrines[:2]:
                answer_parts.extend(d.conclusion_template)
        else:  # MEMO
            answer_parts = []
            for d in doctrines:
                answer_parts.append(f"\n### {d.topic}\n")
                answer_parts.extend(d.conclusion_template)
                answer_parts.append(f"\n{d.reasoning_framework[:500]}...")

        answer = "\n\n".join(answer_parts)

        # Extract sources
        sources = []
        for d in doctrines:
            sources.extend(d.primary_authority)
        sources = list(set(sources))[:5]  # Unique, top 5

        # Build reasoning chain
        reasoning_chain = [
            f"Query matched doctrine: {d.topic}" for d in doctrines
        ]

        # Triggered doctrines
        triggered = [d.topic for d in doctrines]

        # Epistemic flags
        epistemic_flags = []
        for d in doctrines:
            if d.confidence == ConfidenceLevel.AGGRESSIVE:
                epistemic_flags.append(f"AGGRESSIVE position on {d.topic}")
            elif d.confidence == ConfidenceLevel.HIGH_RISK:
                epistemic_flags.append(f"HIGH RISK designation for {d.topic}")
            if d.adversarial_considerations:
                epistemic_flags.append(f"Adversarial concerns: {d.adversarial_considerations[:100]}...")

        # Determinism hash
        determinism_hash = hashlib.sha256(
            f"{query}|{mode}|{zone}|{[d.topic for d in doctrines]}".encode()
        ).hexdigest()[:16]

        return QueryResponse(
            answer=answer,
            confidence=doctrines[0].confidence,
            sources=sources,
            reasoning_chain=reasoning_chain,
            triggered_doctrines=triggered,
            epistemic_flags=epistemic_flags,
            determinism_hash=determinism_hash,
            latency_ms=0.0,  # Set by caller
            mode=mode,
            zone=zone
        )

    def _deep_analysis(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> QueryResponse:
        """Fallback deep analysis when no doctrine cache hits."""

        answer = (
            f"Deep analysis mode for query: '{query}'\n\n"
            f"No direct doctrine cache match found. This query requires synthesis across "
            f"energy storage systems expertise. Key considerations:\n\n"
            f"1. Technology selection based on application requirements (duration, power, response time)\n"
            f"2. Economic analysis including LCOS, revenue stacking, and market participation\n"
            f"3. Regulatory compliance (interconnection, safety, environmental)\n"
            f"4. Performance optimization (round-trip efficiency, degradation management)\n"
            f"5. Grid integration and operational strategies\n\n"
            f"For detailed guidance, please consult the relevant doctrine blocks or refine the query."
        )

        return QueryResponse(
            answer=answer,
            confidence=ConfidenceLevel.DISCLOSURE,
            sources=["General energy storage engineering principles"],
            reasoning_chain=["No doctrine cache match", "Deep analysis synthesis required"],
            triggered_doctrines=[],
            epistemic_flags=["DISCLOSURE: Deep analysis mode, limited doctrine support"],
            determinism_hash=hashlib.sha256(f"{query}|deep".encode()).hexdigest()[:16],
            latency_ms=0.0,
            mode=mode,
            zone=zone
        )

    def health_check(self) -> HealthResponse:
        """TIE-20 Component: Health endpoint."""
        uptime = (datetime.now() - self.start_time).total_seconds()

        return HealthResponse(
            status="healthy",
            engine="ENRG12_energy_storage",
            version="1.0.0",
            port=9332,
            doctrines_loaded=len(self.doctrine_cache),
            uptime_seconds=uptime,
            total_queries=self.metrics["total_queries"]
        )


# ═══════════════════════════════════════════════════════════════════════════════
# FASTAPI SERVER
# ═══════════════════════════════════════════════════════════════════════════════

APP = FastAPI(
    title="ENRG12 Energy Storage Systems Intelligence Engine",
    description="TIE-grade engine for energy storage analysis and optimization",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = ENRG12Engine()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with three-layer response architecture."""
    try:
        response = engine.three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone
        )
        return response
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint."""
    return engine.health_check()


@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics."""
    return {
        "total": len(engine.doctrine_cache),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in engine.doctrine_cache
        ]
    }


@APP.get("/metrics")
async def metrics_endpoint():
    """Performance metrics endpoint."""
    return {
        "engine": "ENRG12_energy_storage",
        "metrics": engine.metrics,
        "uptime_seconds": (datetime.now() - engine.start_time).total_seconds()
    }


if __name__ == "__main__":
    logger.info("Starting ENRG12 Energy Storage Systems Intelligence Engine on port 9332")
    uvicorn.run(APP, host="0.0.0.0", port=9332)
