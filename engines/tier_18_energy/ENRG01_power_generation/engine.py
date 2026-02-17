import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

"""
ENRG01 - Power Generation & Energy Systems Intelligence Engine
Comprehensive knowledge engine covering thermal, nuclear, renewable, and distributed power generation

Port: 9081
Version: 1.0.0
TIE-20 Compliant Architecture
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from loguru import logger
import hashlib
import json
from datetime import datetime
from dataclasses import dataclass, asdict

# ============================================================================
# CONFIGURATION & LOGGING
# ============================================================================

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "logs" / "enrg01_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)

APP = FastAPI(
    title="ENRG01 Power Generation Intelligence Engine",
    description="Comprehensive power generation and energy systems knowledge engine",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DOMAIN MODELS
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
    THERMAL_POWER = "THERMAL_POWER"
    NUCLEAR_POWER = "NUCLEAR_POWER"
    RENEWABLE_ENERGY = "RENEWABLE_ENERGY"
    HYDROELECTRIC = "HYDROELECTRIC"
    GRID_INTEGRATION = "GRID_INTEGRATION"
    EMISSIONS_CONTROL = "EMISSIONS_CONTROL"
    RELIABILITY_STANDARDS = "RELIABILITY_STANDARDS"
    ECONOMIC_ANALYSIS = "ECONOMIC_ANALYSIS"
    DISTRIBUTED_GENERATION = "DISTRIBUTED_GENERATION"
    ENERGY_STORAGE = "ENERGY_STORAGE"
    COGENERATION = "COGENERATION"
    COMMISSIONING_OPERATIONS = "COMMISSIONING_OPERATIONS"

@dataclass
class DoctrineBlock:
    """Represents a reusable expert reasoning block"""
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: Optional[str]
    adversary_position: Optional[str]
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    controlling_precedent: Optional[str]

class QueryRequest(BaseModel):
    query: str = Field(..., description="Power generation question or scenario")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")

class QueryResponse(BaseModel):
    query: str
    mode: ResponseMode
    answer: str
    confidence: ConfidenceLevel
    doctrines_applied: List[str]
    key_factors: List[str]
    authorities: List[str]
    determinism_hash: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float

# ============================================================================
# DOCTRINE CACHE - POWER GENERATION EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    # ========== THERMAL POWER GENERATION ==========

    DoctrineBlock(
        topic="coal_fired_power_plant_operation",
        keywords=["coal", "pulverized coal", "boiler", "steam turbine", "thermal efficiency", "heat rate"],
        conclusion_template=[
            "Coal-fired power plants convert chemical energy in coal to electrical energy through combustion, steam generation, and turbine rotation",
            "Typical thermal efficiency ranges from 33-45% depending on technology (subcritical, supercritical, ultra-supercritical)",
            "Heat rate (Btu/kWh) is the inverse measure of efficiency - lower heat rate indicates higher efficiency"
        ],
        reasoning_framework="""
        Coal Plant Operation Analysis:
        1. Fuel Preparation: Coal crushing, pulverization to fine powder (~70 microns)
        2. Combustion: Pulverized coal burned in boiler at 1400-1700°C
        3. Steam Generation: Water heated in boiler tubes to produce high-pressure superheated steam (2400-3500 psi, 540-600°C)
        4. Steam Turbine: High-pressure steam expands through turbine stages (HP, IP, LP), rotating generator
        5. Condenser: Exhaust steam condensed back to water using cooling system
        6. Feedwater System: Condensate pumped back to boiler through feedwater heaters
        7. Efficiency Factors: Steam conditions (higher P/T = higher efficiency), number of reheat stages, feedwater heating stages
        8. Rankine Cycle: Thermodynamic cycle governing coal plant operation
        9. Subcritical (<3208 psi): 33-37% efficiency
        10. Supercritical (>3208 psi): 38-42% efficiency
        11. Ultra-supercritical (>4400 psi, >593°C): 43-45%+ efficiency
        12. Heat Rate Calculation: Heat rate (Btu/kWh) = 3412 / efficiency
        13. Emissions: CO2 ~2.2 lb/kWh, SO2, NOx, particulates, mercury (require controls)
        14. Load Following: Coal plants can operate 40-100% load, ramp rate 1-3% per minute
        15. Capacity Factor: Typically 60-85% for coal baseload plants
        """,
        key_factors=[
            "Steam pressure and temperature (subcritical vs supercritical)",
            "Number of reheat and feedwater heating stages",
            "Condenser vacuum (affects LP turbine efficiency)",
            "Coal quality (heating value, moisture, ash content)",
            "Boiler design (pulverized coal, cyclone, fluidized bed)",
            "Emissions control equipment parasitic load",
            "Cooling system efficiency"
        ],
        primary_authority=[
            "ASME Boiler and Pressure Vessel Code",
            "NFPA 85 Boiler and Combustion Systems Hazards Code",
            "EPA Clean Air Act regulations (NSPS, MACT)",
            "Steam: Its Generation and Use (Babcock & Wilcox)",
            "Power Plant Engineering (Black & Veatch)"
        ],
        burden_holder="Plant operator to demonstrate compliance with emissions limits and efficiency standards",
        adversary_position="Environmental groups may challenge emissions, water use, coal ash disposal",
        counter_arguments=[
            "Coal provides reliable baseload power unlike intermittent renewables",
            "Modern emissions controls reduce pollutants by 90%+",
            "Carbon capture and storage (CCS) can reduce CO2 emissions",
            "Existing coal fleet provides grid stability and inertia",
            "Coal is lowest-cost fuel in many regions"
        ],
        resolution_strategy="Balance reliability and economic benefits against environmental impacts; transition to higher-efficiency supercritical technology; retrofit with emissions controls; consider co-firing with biomass",
        entity_scope="Electric utilities, independent power producers, industrial cogeneration",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="EPA Clean Power Plan (vacated), Mercury and Air Toxics Standards (MATS), Regional Haze Rule"
    ),

    DoctrineBlock(
        topic="combined_cycle_gas_turbine_ccgt",
        keywords=["CCGT", "combined cycle", "natural gas", "gas turbine", "HRSG", "heat recovery"],
        conclusion_template=[
            "Combined cycle gas turbine (CCGT) plants achieve 55-62% thermal efficiency by combining Brayton and Rankine cycles",
            "Gas turbine (Brayton cycle) generates ~2/3 of output, steam turbine (Rankine cycle) generates ~1/3 from waste heat recovery",
            "CCGT offers fast startup (30-60 min to full load), excellent load following, and lowest CO2 emissions among fossil fuels"
        ],
        reasoning_framework="""
        CCGT Plant Analysis:
        1. Gas Turbine (Brayton Cycle): Air compressed, fuel combusted, hot gases expand through turbine
        2. Exhaust Temperature: Gas turbine exhaust ~600-650°C contains significant thermal energy
        3. HRSG (Heat Recovery Steam Generator): Unfired or supplementary-fired boiler captures exhaust heat
        4. Steam Generation: HRSG produces steam at 2-3 pressure levels (LP, IP, HP)
        5. Steam Turbine: Steam expands through turbine stages, drives second generator
        6. Combined Efficiency: Gas turbine 35-40% + steam turbine 15-22% = 55-62% total
        7. 1x1 Configuration: 1 gas turbine + 1 HRSG + 1 steam turbine
        8. 2x1 Configuration: 2 gas turbines + 2 HRSGs + 1 steam turbine (higher efficiency)
        9. Fast Start: Simple cycle mode in 10 min, full combined cycle in 30-60 min
        10. Load Following: Excellent turndown (20-100%), fast ramp rates (10-20 MW/min)
        11. Emissions: CO2 ~0.8 lb/kWh (60% less than coal), low NOx with DLN combustors, no SO2/particulates
        12. Fuel Flexibility: Primarily natural gas, can burn diesel/distillate backup fuel
        13. Capacity Factor: 50-90% depending on market role (baseload vs peaking)
        14. Water Use: Lower than coal (no boiler feedwater, only steam cycle makeup and cooling)
        15. Economics: Low capital cost, high fuel cost, excellent for mid-merit and peaking duty
        """,
        key_factors=[
            "Gas turbine technology (GE 7/9HA, Siemens H-class, Mitsubishi M501J)",
            "Number of pressure levels in HRSG (1, 2, or 3)",
            "Supplementary firing in HRSG (increases output but reduces efficiency)",
            "Ambient temperature (higher temp reduces gas turbine output and efficiency)",
            "Natural gas price and availability",
            "Grid role (baseload, intermediate, peaking)",
            "Steam turbine configuration (single-shaft vs multi-shaft)"
        ],
        primary_authority=[
            "ASME Performance Test Code PTC 46 (Combined Cycle)",
            "ISO 2314 Gas Turbines - Acceptance Tests",
            "EPA 40 CFR Part 60 Subpart KKKK (NSPS for Combustion Turbines)",
            "NERC Reliability Standards (generator performance)",
            "Gas Turbine Engineering Handbook (Boyce)"
        ],
        burden_holder="Plant developer to demonstrate compliance with air permits and interconnection requirements",
        adversary_position="Local opposition to gas infrastructure, environmental groups concerned with methane leakage",
        counter_arguments=[
            "CCGT is cleanest fossil fuel option (half the CO2 of coal)",
            "Provides flexible generation to support renewable integration",
            "Fast startup complements solar/wind intermittency",
            "Lower water consumption than coal or nuclear",
            "Can be converted to hydrogen fuel in future"
        ],
        resolution_strategy="Site plants near gas pipelines and load centers; optimize for flexible operation; invest in advanced controls for fast ramping; consider hydrogen co-firing capability",
        entity_scope="Electric utilities, IPPs, merchant power generators",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="EPA NSPS Subpart KKKK, state air quality permits, FERC interconnection agreements"
    ),

    DoctrineBlock(
        topic="simple_cycle_gas_turbine_peaking",
        keywords=["peaker", "simple cycle", "combustion turbine", "LMS100", "aeroderivative", "peak demand"],
        conclusion_template=[
            "Simple cycle gas turbines (peakers) provide rapid-start generation for peak demand periods with 30-40% efficiency",
            "Fast startup time (5-10 minutes to full load) and low capital cost offset lower efficiency compared to CCGT",
            "Two main types: heavy-duty industrial turbines and aeroderivative turbines adapted from aircraft engines"
        ],
        reasoning_framework="""
        Peaking Gas Turbine Analysis:
        1. Brayton Cycle Only: Compression → combustion → expansion (no steam cycle)
        2. Thermal Efficiency: 30-40% (lower than CCGT but acceptable for infrequent operation)
        3. Startup Time: 5-10 minutes from cold shutdown to full load
        4. Load Following: Excellent (10-100% load), fast ramp rates (50+ MW/min for aeroderivatives)
        5. Heavy-Duty Turbines: GE Frame 7/9, Siemens SGT-800, rugged industrial design
        6. Aeroderivative Turbines: GE LMS100/LM6000, Siemens SGT-A35, derived from jet engines
        7. Aeroderivative Advantages: Faster start, higher efficiency (~40% vs 35%), lighter weight
        8. Aeroderivative Disadvantages: Higher cost, more maintenance, shorter inspection intervals
        9. Capacity Factor: Typically <20% (operate only during peak demand periods)
        10. Economics: Low CapEx ($600-900/kW), high heat rate (9,000-11,000 Btu/kWh)
        11. Revenue Model: Capacity payments + energy arbitrage during high-price hours
        12. Emissions: CO2 ~1.2-1.5 lb/kWh, NOx controlled with water/steam injection or SCR
        13. Black Start Capability: Some units equipped for grid restoration after blackout
        14. Fuel: Natural gas primary, distillate/diesel backup (dual-fuel capability common)
        15. Applications: Peak shaving, voltage support, frequency regulation, operating reserves
        """,
        key_factors=[
            "Annual capacity factor and operating hours",
            "Electricity market price volatility (spark spread)",
            "Grid reliability requirements (reserve margins)",
            "Ambient temperature impact on output (derating in summer peaks)",
            "Fuel availability and dual-fuel capability",
            "Emissions limits (NOx, CO) and control technology",
            "Black start vs non-black start capability"
        ],
        primary_authority=[
            "NERC Reliability Standards (BAL, PRC, VAR)",
            "FERC Order 755 (Frequency Regulation Compensation)",
            "EPA 40 CFR Part 60 Subpart KKKK",
            "ISO/RTO market rules (capacity, energy, ancillary services)",
            "ASME PTC 22 (Gas Turbine Performance Testing)"
        ],
        burden_holder="Generator owner to demonstrate availability during peak periods and compliance with emissions permits",
        adversary_position="Critics argue peakers undermine renewables, local communities concerned with air quality impacts",
        counter_arguments=[
            "Peakers essential for grid reliability during extreme weather events",
            "Battery storage cannot yet provide sustained multi-hour peaking capacity",
            "Rapid response supports renewable integration (backs up solar/wind outages)",
            "Low capital cost enables quick deployment to meet load growth",
            "Modern DLN combustors reduce NOx to <9 ppm"
        ],
        resolution_strategy="Optimize dispatch economics; consider battery storage hybrid for first 2-4 hours; site away from disadvantaged communities; invest in advanced emissions controls",
        entity_scope="Merchant generators, utilities, competitive retailers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="FERC capacity market rules, state renewable portfolio standards, EPA Good Neighbor Rule"
    ),

    # ========== NUCLEAR POWER ==========

    DoctrineBlock(
        topic="pressurized_water_reactor_pwr",
        keywords=["PWR", "nuclear", "reactor", "uranium", "fuel assembly", "control rods", "steam generator"],
        conclusion_template=[
            "Pressurized Water Reactors (PWR) are the most common nuclear reactor design (>60% of global fleet) using two separate water loops",
            "Primary loop circulates pressurized water (~2250 psi, 325°C) through reactor core without boiling, transferring heat to secondary loop via steam generators",
            "PWR design features include: negative temperature coefficient (inherent safety), boric acid chemical shim, and containment building protection"
        ],
        reasoning_framework="""
        PWR Design and Operation Analysis:
        1. Fuel: Uranium dioxide (UO2) pellets, 3-5% enriched U-235, clad in zircaloy tubes
        2. Fuel Assembly: 264-289 fuel rods arranged in 17x17 grid, control rod guide tubes, instrumentation
        3. Reactor Core: 150-200 fuel assemblies, typically 1/3 replaced every 18-24 months (refueling outage)
        4. Primary Loop (Reactor Coolant System): Pressurized water (2200-2400 psi) prevents boiling despite high temp
        5. Reactor Vessel: 8-12 inch thick steel pressure vessel, houses core and control rod mechanisms
        6. Pressurizer: Maintains constant pressure in primary loop via electric heaters and spray system
        7. Control Rods: Silver-indium-cadmium or boron carbide absorbers, inserted from top
        8. Chemical Shim: Boric acid dissolved in coolant provides reactivity control (supplements control rods)
        9. Negative Temperature Coefficient: Rising temp reduces reactivity (self-regulating, inherent safety)
        10. Steam Generators (2-4 units): Heat exchangers transfer heat from primary to secondary loop
        11. Secondary Loop: Lower pressure (~1000 psi) water boils in steam generators, drives turbine
        12. Turbine-Generator: Conventional steam turbine (HP, LP stages), generates 1000-1650 MWe
        13. Condenser: Steam condensed using cooling water (river, ocean, cooling towers)
        14. Thermal Efficiency: 32-36% (lower than fossil due to lower steam temperature)
        15. Capacity Factor: >90% for modern units (among highest of any generation technology)
        16. Fuel Burnup: 50,000-60,000 MWd/MTU (megawatt-days per metric ton uranium)
        17. Safety Systems: Emergency core cooling (ECCS), containment building, passive safety features (AP1000)
        18. NRC Oversight: Resident inspectors, baseline inspections, safety culture assessments
        """,
        key_factors=[
            "Fuel enrichment level (3-5% U-235) and burnup target",
            "Refueling outage length (30-40 days typical) and schedule (18 or 24-month cycle)",
            "Primary coolant chemistry (boric acid concentration, lithium, pH control)",
            "Steam generator tube integrity (corrosion, plugging, replacement)",
            "Capacity factor optimization (online maintenance, outage planning)",
            "NRC inspection findings and performance indicators",
            "Spent fuel storage (in-pool vs dry cask)"
        ],
        primary_authority=[
            "10 CFR Part 50 (Domestic Licensing of Production and Utilization Facilities)",
            "10 CFR Part 100 (Reactor Site Criteria)",
            "NRC Regulatory Guides (1.1-1.233)",
            "ASME Boiler & Pressure Vessel Code Section III (Nuclear)",
            "ANSI/ANS Standards (nuclear criticality, fuel design, safety analysis)",
            "NUREG-0800 Standard Review Plan"
        ],
        burden_holder="Nuclear licensee to demonstrate safety case to NRC, comply with Technical Specifications",
        adversary_position="Nuclear critics cite accident risks (Fukushima, Chernobyl), waste disposal concerns, high costs",
        counter_arguments=[
            "PWR has excellent safety record in US (no radiation deaths at commercial reactors)",
            "Carbon-free baseload generation critical for decarbonization",
            "Modern Gen III/III+ designs (AP1000, EPR) have passive safety systems",
            "Spent fuel safely stored on-site in dry casks (no geological repository needed immediately)",
            "Lowest lifecycle CO2 emissions of any dispatchable generation (~12 g CO2/kWh)"
        ],
        resolution_strategy="Maintain strong safety culture and operational excellence; pursue license renewals (60-80 years); invest in digital instrumentation upgrades; optimize refueling outages; advocate for spent fuel solutions",
        entity_scope="Nuclear operating companies (Exelon, Duke, Southern, Entergy, etc.)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Atomic Energy Act, NRC Part 50/52 regulations, Price-Anderson Act (liability)"
    ),

    DoctrineBlock(
        topic="boiling_water_reactor_bwr",
        keywords=["BWR", "boiling water", "direct cycle", "GE", "recirculation", "jet pump"],
        conclusion_template=[
            "Boiling Water Reactors (BWR) use a direct cycle design where water boils in the reactor core and steam directly drives the turbine",
            "BWR design simplifies steam generation (no steam generators) but requires turbine components to handle radioactive steam",
            "Modern BWRs (BWR/6, ABWR, ESBWR) feature internal recirculation pumps and enhanced safety systems"
        ],
        reasoning_framework="""
        BWR Design Analysis:
        1. Direct Cycle: Water boils in reactor core (~1050 psi, 285°C), steam goes directly to turbine
        2. Single Loop: No separate primary/secondary loops (simpler than PWR but turbine becomes radioactive)
        3. Fuel: Similar to PWR - UO2 pellets, 3-4% enriched, zircaloy cladding
        4. Core Design: Fuel bundles with integral channels, control rods inserted from bottom
        5. Control Rods: Cruciform shape, boron carbide absorber, hydraulic drive from below
        6. Reactivity Control: Control rods only (no chemical shim like PWR)
        7. Void Coefficient: Negative - increased boiling reduces reactivity (safety feature)
        8. Recirculation System: Jet pumps (BWR/4-6) or internal pumps (ABWR) drive coolant flow
        9. Power Control: Adjust recirculation flow to change void fraction and reactivity
        10. Steam Separation: Moisture separators and dryers remove water from steam before turbine
        11. Turbine: HP and LP stages, must handle slightly radioactive steam (N-16 activation)
        12. Turbine Isolation: Fast-acting valves close on accident signals to contain radioactivity
        13. Thermal Efficiency: 33-34% (similar to PWR)
        14. Capacity Factor: 85-92% for modern BWRs
        15. Safety Systems: Isolation condensers, containment cooling, automatic depressurization, ECCS
        16. Containment: Mark I (light bulb), Mark II (over-under), Mark III (dry well/wet well)
        17. ESBWR (GE Hitachi): Passive safety, natural circulation, no recirculation pumps
        """,
        key_factors=[
            "Recirculation pump performance and flow control",
            "Steam dryer integrity (vibration, cracking issues in some plants)",
            "Control rod pattern and sequencing",
            "Water chemistry (maintain low oxygen, conductivity to prevent IGSCC)",
            "Fuel bundle design (GE14, SVEA-96, Atrium) and thermal margins",
            "Containment type and pressure suppression performance",
            "Turbine maintenance (radioactive contamination requires special handling)"
        ],
        primary_authority=[
            "10 CFR Part 50 (NRC Licensing)",
            "NUREG-0800 Standard Review Plan",
            "NRC Generic Letters and Bulletins (GE BWR-specific issues)",
            "BWROG (BWR Owners Group) topical reports",
            "ASME Section III (nuclear components)"
        ],
        burden_holder="BWR licensee to manage radioactive steam systems and demonstrate ECCS adequacy",
        adversary_position="Critics point to Fukushima accident (BWR design), hydrogen generation, Mark I containment concerns",
        counter_arguments=[
            "US BWRs have different site conditions than Fukushima (no major tsunami risk)",
            "Post-Fukushima upgrades (FLEX equipment, hardened vents) improve accident resilience",
            "Direct cycle design simplifies steam generation and eliminates steam generator failures",
            "Proven track record (>300 reactor-years of operation in US)",
            "Advanced BWRs (ABWR, ESBWR) incorporate passive safety features"
        ],
        resolution_strategy="Implement Fukushima lessons learned; maintain robust emergency preparedness; pursue license renewals; consider SMR replacements for older units",
        entity_scope="BWR operators (Exelon, Entergy, Energy Harbor, etc.)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="NRC post-Fukushima orders, 10 CFR 50.54(f) information requests"
    ),

    # ========== RENEWABLE ENERGY ==========

    DoctrineBlock(
        topic="solar_photovoltaic_pv_systems",
        keywords=["solar PV", "photovoltaic", "inverter", "module", "panel", "crystalline silicon", "thin film"],
        conclusion_template=[
            "Solar PV systems convert sunlight directly to electricity using semiconductor materials (primarily silicon) with no moving parts",
            "System performance depends on: module efficiency (15-22%), irradiance (sunlight intensity), temperature (higher temp reduces efficiency), and inverter efficiency (96-98%)",
            "Levelized cost of electricity (LCOE) for utility-scale solar has declined 90% since 2010, now competitive with fossil fuels in many regions"
        ],
        reasoning_framework="""
        Solar PV System Analysis:
        1. PV Effect: Photons strike semiconductor, create electron-hole pairs, generate DC voltage
        2. Module Types:
           - Monocrystalline Silicon: 20-22% efficiency, black appearance, premium cost
           - Polycrystalline Silicon: 15-17% efficiency, blue appearance, lower cost
           - Thin Film (CdTe, CIGS, a-Si): 10-12% efficiency, flexible, lower cost
           - Bifacial: Capture light on both sides, 10-20% additional yield from ground reflection
        3. Module Degradation: Typically 0.5-0.8% per year, 25-30 year warranties guarantee >80% output
        4. Temperature Coefficient: -0.3 to -0.5% per °C above 25°C (performance drops in heat)
        5. Irradiance: Peak performance at 1000 W/m² (STC), output scales linearly with irradiance
        6. Array Configuration: Series strings for voltage, parallel strings for current
        7. Inverters: Convert DC to AC, maximum power point tracking (MPPT), grid synchronization
        8. String Inverters: One inverter per array (10-100 kW), simple but vulnerable to shading
        9. Microinverters: One per module, optimize each panel individually, higher cost
        10. Central Inverters: Utility-scale (1-5 MW), lowest $/W, require DC combiners
        11. Tracking Systems: Fixed-tilt (simplest), single-axis (15-25% more energy), dual-axis (5% more than single)
        12. Capacity Factor: 15-30% depending on location (Arizona >30%, cloudy regions <20%)
        13. AC vs DC Ratings: AC output lower than DC due to inverter losses, temperature derating
        14. Grid Integration: IEEE 1547 compliance, anti-islanding, voltage/frequency ride-through
        15. Energy Storage Pairing: Batteries enable time-shifting, capacity firming, frequency regulation
        16. O&M: Panel cleaning, inverter replacement (~10-15 years), vegetation management
        17. LCOE Drivers: CapEx ($800-1200/kW utility-scale), capacity factor, O&M, discount rate
        """,
        key_factors=[
            "Solar resource (DNI, GHI, POA irradiance) and site-specific production modeling",
            "Module technology, efficiency, degradation rate, and warranty terms",
            "Inverter topology (string, central, micro) and efficiency",
            "Tracking system (fixed, single-axis, dual-axis) economics",
            "Land availability and terrain (slopes, shading, soil conditions)",
            "Interconnection costs and transmission availability",
            "Tax incentives (ITC, PTC, accelerated depreciation)"
        ],
        primary_authority=[
            "IEEE 1547 Standard for Interconnecting Distributed Resources",
            "UL 1703 (PV Modules), UL 1741 (Inverters)",
            "NEC Article 690 (Solar PV Systems)",
            "FERC Order 2222 (Distributed Energy Resource Aggregation)",
            "IRS Publication 5695 (Investment Tax Credit)"
        ],
        burden_holder="Developer to demonstrate grid code compliance and obtain interconnection approval",
        adversary_position="Critics cite intermittency, land use, manufacturing emissions, recycling challenges",
        counter_arguments=[
            "Battery storage mitigates intermittency (4-8 hour storage common)",
            "Agrivoltaics and dual-use (grazing, pollinator habitat) address land use concerns",
            "Silicon PV energy payback time ~2 years (generates clean energy for 25+ years)",
            "Module recycling technologies emerging (recover silicon, silver, glass)",
            "Solar creates more jobs per MW than fossil fuels"
        ],
        resolution_strategy="Pair with storage for dispatchability; optimize tracker economics; negotiate favorable PPAs; leverage tax credits; engage community early",
        entity_scope="Utility-scale developers, C&I customers, residential installers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="FERC Order 2023 (interconnection reform), state RPS mandates, IRA tax credits"
    ),

    DoctrineBlock(
        topic="wind_turbine_power_generation",
        keywords=["wind turbine", "wind farm", "rotor", "blade", "nacelle", "gearbox", "wake effect"],
        conclusion_template=[
            "Wind turbines convert kinetic energy of wind to electrical energy using aerodynamic lift on rotor blades (modern turbines: 2-15 MW)",
            "Power output follows cube law: power ∝ wind speed³ (doubling wind speed = 8x power), making siting and wind resource critical",
            "Capacity factor for land-based wind: 35-45%, offshore wind: 45-55% due to higher, steadier winds"
        ],
        reasoning_framework="""
        Wind Turbine Analysis:
        1. Betz Limit: Maximum theoretical efficiency 59.3% (actual turbines achieve 35-45%)
        2. Components:
           - Rotor: 2 or 3 blades, 50-120m diameter (onshore), up to 240m (offshore)
           - Nacelle: Houses gearbox, generator, controls, yaw drive
           - Tower: 80-120m hub height (onshore), 100-150m (offshore) for stronger winds
           - Foundation: Spread-foot (onshore), monopile/jacket/floating (offshore)
        3. Power Curve: Cut-in (3-4 m/s), rated power (11-15 m/s), cut-out (25-30 m/s for safety)
        4. Gearbox: Converts low-speed rotor rotation (10-20 RPM) to high-speed generator (1200-1800 RPM)
        5. Direct-Drive: No gearbox, multi-pole permanent magnet generator (higher reliability, heavier)
        6. Pitch Control: Actively adjust blade angle to optimize power capture and limit overspeed
        7. Yaw Control: Rotate nacelle to face wind direction (upwind turbine design)
        8. Power Electronics: Converter allows variable-speed operation and grid connection
        9. Wake Effect: Downstream turbines produce 10-30% less power due to upstream turbine wakes
        10. Array Layout: Optimize spacing (5-10 rotor diameters) to minimize wake losses
        11. Offshore Advantages: Higher wind speeds, less turbulence, larger turbine scales (15+ MW)
        12. Offshore Challenges: Higher CapEx ($3000-5000/kW), O&M access, transmission costs
        13. Capacity Factor: Onshore 35-45%, offshore 45-55%, depends on wind class and turbine
        14. Wind Classes: IEC Class I (high wind, 50 m/s extreme), II (medium), III (low wind)
        15. O&M: Gearbox replacement (10-15 years), blade inspections, lightning protection, yaw bearing
        16. Curtailment: Reduce output for grid constraints, environmental (bird/bat), or pricing
        17. LCOE Drivers: CapEx, capacity factor, O&M, financing costs, transmission
        """,
        key_factors=[
            "Wind resource quality (mean wind speed, Weibull distribution, wind shear exponent)",
            "Turbine technology (geared vs direct-drive, rated power, rotor diameter)",
            "Hub height optimization (taller = more energy but higher cost)",
            "Wake modeling and array optimization",
            "Offshore vs onshore economics and risk",
            "Transmission availability and interconnection queue position",
            "Wildlife impacts (avian/bat mortality) and mitigation measures"
        ],
        primary_authority=[
            "IEC 61400 series (Wind Turbine Design Standards)",
            "IEEE 1547 (Grid Interconnection)",
            "AWEA/NREL best practices for wind resource assessment",
            "BOEM (offshore leasing and permitting)",
            "FAA obstruction marking and lighting requirements"
        ],
        burden_holder="Developer to prove grid stability, environmental compliance, and project viability",
        adversary_position="Local opposition (visual, noise, flicker), wildlife advocates, property value concerns",
        counter_arguments=[
            "Wind generates zero-emission electricity at competitive costs",
            "Modern turbines operate quietly (40-45 dB at 300m, below ambient noise)",
            "Setbacks and siting guidelines minimize community impacts",
            "Economic benefits (tax revenue, lease payments, jobs) to rural communities",
            "Offshore wind avoids onshore land use conflicts entirely"
        ],
        resolution_strategy="Conduct thorough wind resource and environmental studies; engage community early; optimize turbine selection for site; secure PPA or market hedge",
        entity_scope="Wind developers (Orsted, NextEra, Avangrid), utilities, community wind",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="FERC transmission policy, state RPS, BOEM offshore leases, ESA consultation"
    ),

    # ========== HYDROELECTRIC POWER ==========

    DoctrineBlock(
        topic="hydroelectric_dam_operation",
        keywords=["hydroelectric", "dam", "reservoir", "turbine", "penstock", "tailrace", "Francis turbine"],
        conclusion_template=[
            "Hydroelectric plants convert potential energy of elevated water to electrical energy via turbines (most efficient generation technology at 85-90%)",
            "Dam types: run-of-river (minimal storage), conventional storage, pumped-storage (energy storage via reversible operation)",
            "Turbine selection depends on head and flow: Pelton (high head/low flow), Francis (medium head/flow), Kaplan (low head/high flow)"
        ],
        reasoning_framework="""
        Hydroelectric System Analysis:
        1. Power Equation: P = ρ × g × Q × H × η (density × gravity × flow × head × efficiency)
        2. Head Types:
           - Gross Head: Vertical distance from reservoir to tailwater
           - Net Head: Gross head minus friction/turbulence losses (~5-10%)
           - High Head: >100m (Pelton turbines)
           - Medium Head: 30-100m (Francis turbines)
           - Low Head: <30m (Kaplan or Bulb turbines)
        3. Dam Classification:
           - Run-of-River: No significant storage, follow natural flow, minimal environmental impact
           - Storage: Large reservoir, seasonal/annual regulation, firm capacity
           - Pumped-Storage: Two reservoirs, pump water uphill during low demand, generate during peaks
        4. Pelton Turbine: Impulse turbine, water jets strike buckets on wheel, high head (100-2000m)
        5. Francis Turbine: Reaction turbine, water fills runner and exits axially, medium head (30-500m)
        6. Kaplan Turbine: Axial-flow reaction turbine, adjustable blades, low head (5-80m), high flow
        7. Generator Synchronization: Turbine speed controlled to match grid frequency (60 Hz = 3600/n RPM)
        8. Penstock: Pressure pipe delivering water from reservoir to turbine (design for surge pressure)
        9. Spillway: Safety structure to release excess water, prevent dam overtopping
        10. Reservoir Management: Balance flood control, irrigation, recreation, power generation, environmental flows
        11. Capacity Factor: 40-60% depending on hydrology and competing water uses
        12. Peaking Capability: Rapid start/stop (minutes), excellent for load following and frequency regulation
        13. Black Start: Many hydro plants can start without external power (essential for grid restoration)
        14. Environmental Issues: Fish passage (ladders, bypass), sediment transport, downstream flow regimes
        15. FERC Licensing: 30-50 year licenses, relicensing requires environmental studies, stakeholder engagement
        16. Pumped-Storage Economics: Energy arbitrage (buy low/sell high), ancillary services revenue
        """,
        key_factors=[
            "Hydrological regime (seasonal flow variability, drought risk)",
            "Reservoir storage capacity and regulation capability",
            "Turbine technology selection for head and flow conditions",
            "Environmental constraints (fish, recreation, minimum flows)",
            "Competing water uses (irrigation, municipal, flood control)",
            "Transmission availability and distance to load centers",
            "FERC license terms and relicensing schedule"
        ],
        primary_authority=[
            "Federal Power Act (16 USC §791a et seq.)",
            "FERC Part 4 (Licensing of Hydropower Projects)",
            "Clean Water Act Section 401 (State Water Quality Certification)",
            "Endangered Species Act (ESA consultation)",
            "USACE dam safety regulations",
            "USBR design standards for dams"
        ],
        burden_holder="Hydro licensee to balance power generation with environmental, safety, and public interest requirements",
        adversary_position="Environmental groups advocate for dam removal, free-flowing rivers, fish habitat restoration",
        counter_arguments=[
            "Hydro provides zero-carbon dispatchable generation (complements renewables)",
            "Pumped-storage essential for grid-scale energy storage (90%+ of global storage capacity)",
            "Modern fish passage and flow management techniques mitigate impacts",
            "Existing dams are infrastructure assets with 50-100+ year lifespans",
            "Retrofit opportunities (add turbines to non-powered dams, upgrade efficiency)"
        ],
        resolution_strategy="Balance generation with environmental flows; invest in fish passage technology; engage stakeholders in relicensing; pursue efficiency upgrades; explore pumped-storage expansion",
        entity_scope="Federal agencies (USACE, USBR), public utilities, private hydro owners",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="FERC licensing orders, ESA biological opinions, state 401 certifications"
    ),

    # ========== EMISSIONS CONTROL ==========

    DoctrineBlock(
        topic="selective_catalytic_reduction_scr_nox_control",
        keywords=["SCR", "NOx", "ammonia", "urea", "catalyst", "nitrogen oxides", "SNCR"],
        conclusion_template=[
            "Selective Catalytic Reduction (SCR) reduces NOx emissions by 90%+ using ammonia/urea injection over catalyst bed at 600-750°F",
            "SCR is the primary NOx control for coal plants, CCGT, and cement kilns to meet EPA NSPS and MACT standards",
            "Catalyst consists of vanadium, titanium, tungsten oxides; requires replacement every 3-5 years; ammonia slip must be controlled"
        ],
        reasoning_framework="""
        SCR System Analysis:
        1. Chemical Reaction: 4 NH3 + 4 NO + O2 → 4 N2 + 6 H2O (ammonia reacts with NOx to form nitrogen and water)
        2. Catalyst: Honeycomb or plate structure, vanadium pentoxide/titanium dioxide, active at 600-750°F
        3. Ammonia Source: Anhydrous ammonia (NH3) or aqueous urea solution (CO(NH2)2 → NH3)
        4. Injection Grid: Spray ammonia into flue gas upstream of catalyst, mixing critical for uniform distribution
        5. NOx Reduction: 85-95% depending on catalyst age, temperature, NH3/NOx ratio
        6. Ammonia Slip: Excess NH3 passing through (must be <5 ppm to prevent downstream corrosion and odor)
        7. Temperature Window: SCR inactive <500°F, catalyst sintering >800°F (placement in flue gas path critical)
        8. Coal vs Gas: Coal plants typically high-dust SCR (before particulate removal), gas turbines use tail-end SCR
        9. Catalyst Deactivation: Poisoning by arsenic/phosphorus (coal), sulfur compounds, erosion from fly ash
        10. Catalyst Management: Periodic testing, cleaning (soot blowing, washing), replacement layers
        11. SNCR Alternative: Non-catalytic reduction at 1600-2000°F, lower cost but only 30-50% reduction
        12. Economic Trade-offs: SCR CapEx $50-150/kW, ammonia costs, catalyst replacement, auxiliary power (fan, pump)
        13. Co-Benefits: Some SCR systems also reduce mercury oxidation (for easier removal in wet FGD)
        14. Regulatory Drivers: EPA NSPS (0.15 lb/MMBtu for coal), MACT standards, ozone transport SIPs
        15. Monitoring: CEMS for NOx, ammonia, O2; catalyst activity testing; pressure drop (plugging indicator)
        """,
        key_factors=[
            "Flue gas temperature profile and SCR placement",
            "Catalyst type (vanadium vs zeolite) and geometry",
            "Ammonia injection control (NH3/NOx ratio optimization)",
            "Fuel quality impacts (ash, sulfur, arsenic in coal)",
            "Catalyst life and replacement schedule",
            "Ammonia slip limits and downstream impacts (air heater fouling)",
            "Integration with other controls (ESP, FGD, CO catalyst)"
        ],
        primary_authority=[
            "EPA 40 CFR Part 60 (NSPS for Steam Generators)",
            "EPA 40 CFR Part 63 (MACT for Boilers)",
            "NESCAUM SCR Technology Manual",
            "EPRI SCR Design and Optimization Guidelines",
            "State Implementation Plans (SIP) for ozone non-attainment"
        ],
        burden_holder="Plant owner to demonstrate continuous compliance with NOx limits via CEMS",
        adversary_position="Environmental groups may push for lower limits, SCR on all coal units, ammonia safety concerns",
        counter_arguments=[
            "SCR achieves 90%+ NOx reduction, meeting stringent air quality standards",
            "Modern controls eliminate visible plumes and regional haze impacts",
            "Ammonia handling is routine in chemical and agricultural industries",
            "Cost-effective compared to plant retirement (extends useful life)",
            "Combined SCR+SNCR can achieve <0.05 lb/MMBtu NOx"
        ],
        resolution_strategy="Optimize catalyst selection and NH3 injection; implement predictive maintenance; consider hybrid SCR+SNCR; evaluate low-NOx burners as pre-control",
        entity_scope="Coal-fired power plants, natural gas combined cycle, industrial boilers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="EPA Cross-State Air Pollution Rule (CSAPR), Regional Haze Rule, NAAQS for ozone"
    ),

    DoctrineBlock(
        topic="flue_gas_desulfurization_so2_scrubber",
        keywords=["FGD", "scrubber", "SO2", "sulfur dioxide", "limestone", "gypsum", "wet scrubber"],
        conclusion_template=[
            "Flue Gas Desulfurization (FGD) removes 95-98% of SO2 emissions from coal plant exhaust using wet limestone scrubbers",
            "Wet FGD sprays limestone slurry into flue gas; SO2 reacts to form calcium sulfite/sulfate (gypsum byproduct)",
            "Gypsum can be sold for wallboard manufacturing; alternative dry FGD uses lime injection but produces non-saleable waste"
        ],
        reasoning_framework="""
        FGD System Analysis:
        1. Wet Limestone FGD (Most Common):
           - Reaction: CaCO3 + SO2 + 1/2 O2 + 2 H2O → CaSO4·2H2O + CO2 (limestone + SO2 → gypsum)
           - Absorber Tower: Countercurrent gas/liquid contact, spray nozzles atomize slurry
           - SO2 Removal: 95-98% depending on liquid/gas ratio, slurry pH, residence time
           - Byproduct: Gypsum (calcium sulfate dihydrate), 90-95% purity, sold to wallboard industry
        2. Process Steps:
           - Limestone grinding (200-325 mesh)
           - Slurry preparation (10-20% solids)
           - Absorber tower (gas rises, slurry falls)
           - Forced oxidation (air injection converts sulfite to sulfate)
           - Gypsum dewatering (vacuum filters or centrifuges to 10% moisture)
        3. Dry FGD (Spray Dryer):
           - Inject lime (CaO) or slaked lime (Ca(OH)2) slurry into hot flue gas
           - Water evaporates, dry solids collected in baghouse
           - SO2 Removal: 80-95% (lower than wet FGD)
           - No byproduct sales (calcium sulfite/sulfate/fly ash mix sent to landfill)
        4. Seawater FGD: Use alkalinity in seawater instead of limestone (coastal plants only)
        5. Economic Drivers: Wet FGD CapEx $200-400/kW, limestone cost, power consumption (6-8% of plant output)
        6. Water Use: Makeup water for evaporation and blowdown (5-10 gpm/MW)
        7. Wastewater: FGD wastewater contains mercury, selenium, chlorides (requires treatment before discharge)
        8. Mist Eliminators: Prevent water droplet carryover (causes stack plume, corrosion)
        9. Materials: Alloys (Hastelloy, rubber lining) for corrosion resistance in acidic environment
        10. Operational Issues: Scaling, plugging, corrosion, gypsum quality degradation
        11. Regulatory Drivers: EPA NSPS (0.2-1.0 lb SO2/MMBtu depending on coal sulfur), acid rain program
        12. SO2 Allowance Market: Cap-and-trade program (mostly defunct due to low prices and plant retirements)
        """,
        key_factors=[
            "Coal sulfur content (0.5-4% S) and SO2 production rate",
            "FGD technology selection (wet limestone vs dry lime)",
            "Gypsum market availability and pricing",
            "Water availability and wastewater discharge limits",
            "FGD reliability and forced outage rate",
            "Limestone quality and grinding fineness",
            "Auxiliary power consumption (pumps, fans, agitators)"
        ],
        primary_authority=[
            "EPA 40 CFR Part 60 (NSPS for SO2)",
            "Clean Air Act Acid Rain Program (Title IV)",
            "EPA Effluent Limitation Guidelines (Steam Electric)",
            "EPRI FGD Design and Troubleshooting Manuals"
        ],
        burden_holder="Plant owner to maintain FGD operation and meet SO2 limits continuously",
        adversary_position="Critics cite water use, wastewater toxicity, gypsum disposal if no market, cost impacts on electricity rates",
        counter_arguments=[
            "Wet FGD achieves 95-98% SO2 removal, essentially eliminating acid rain from coal plants",
            "Gypsum byproduct is commercial product (wallboard), not waste",
            "Modern wastewater treatment (ZLD, evaporation ponds) eliminates discharge",
            "Dry FGD option available where water is scarce",
            "FGD enables continued operation of coal plants with high-sulfur coal"
        ],
        resolution_strategy="Optimize limestone utilization and gypsum quality; secure gypsum sales contracts; implement wastewater treatment; consider co-benefits (mercury oxidation)",
        entity_scope="Coal-fired power plants burning medium to high sulfur coal",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="EPA Acid Rain Program regulations, state SO2 emissions limits"
    ),

    # ========== GRID INTEGRATION ==========

    DoctrineBlock(
        topic="ieee_1547_grid_interconnection_standard",
        keywords=["IEEE 1547", "interconnection", "distributed generation", "anti-islanding", "voltage ride-through"],
        conclusion_template=[
            "IEEE 1547 Standard for Interconnecting Distributed Energy Resources (DER) establishes technical requirements for grid-tied generation",
            "Key requirements: anti-islanding protection (detect utility outage, disconnect within 2 sec), voltage/frequency ride-through, power quality limits",
            "2018 revision (IEEE 1547-2018) mandates advanced grid support functions: volt-var, freq-watt, dynamic reactive power"
        ],
        reasoning_framework="""
        IEEE 1547 Standard Analysis:
        1. Scope: Covers DER up to 10 MVA per unit at distribution voltage (≤35 kV)
        2. Anti-Islanding: DER must detect loss of utility grid and cease energizing within 2 seconds
        3. Islanding Detection Methods:
           - Passive: Monitor voltage, frequency, rate-of-change
           - Active: Inject perturbations, measure response
           - Transfer trip: Direct communication from utility
        4. Voltage Ride-Through (VRT): DER must remain online during voltage sags/swells per NERC PRC-024
        5. Frequency Ride-Through (FRT): Remain online for 59.5-60.5 Hz normal, trip only for extreme excursions
        6. Power Quality:
           - Voltage flicker: ΔV ≤ 5% (rapid voltage changes cause lamp flicker)
           - Harmonics: Total Harmonic Distortion (THD) < 5%
           - DC injection: < 0.5% of rated output
        7. Volt-Var Function: DER adjusts reactive power output based on local voltage (supports voltage regulation)
        8. Freq-Watt Function: DER reduces active power during overfrequency events (supports frequency stability)
        9. Reactive Power Control: DER can provide dynamic Var support (0.9 leading to 0.9 lagging PF)
        10. Ramp Rate Control: Utility can limit DER power ramping to manage grid stability
        11. Interoperability: IEC 61850, IEEE 2030.5 (Smart Energy Profile), SunSpec Modbus for DER communications
        12. Certification: UL 1741 SA tests inverters for IEEE 1547-2018 compliance
        13. FERC Order 2222: Enables DER aggregations to participate in wholesale markets (builds on 1547)
        14. California Rule 21: State-specific interconnection tariff implementing 1547 + additional requirements
        15. Hosting Capacity: Maximum DER penetration before grid upgrades needed (IEEE 1547 enables higher hosting capacity)
        """,
        key_factors=[
            "DER technology (solar PV, wind, battery, diesel) and inverter capabilities",
            "Utility grid code and interconnection tariff",
            "Hosting capacity analysis (voltage, thermal, protection limits)",
            "Advanced inverter settings (volt-var, freq-watt curves)",
            "Communication requirements (SCADA, DERMS integration)",
            "Protection coordination (overcurrent, ground fault, reclosing)",
            "Interconnection study (distribution load flow, short circuit, stability)"
        ],
        primary_authority=[
            "IEEE 1547-2018 Standard for Interconnecting DER",
            "UL 1741 SA (Inverter Certification)",
            "FERC Order 2222 (DER Aggregation)",
            "NERC PRC-024 (Generator Frequency and Voltage Ride-Through)",
            "State interconnection tariffs (CA Rule 21, NY SIR, etc.)"
        ],
        burden_holder="DER owner to prove compliance with 1547 and pass utility acceptance tests",
        adversary_position="Utilities may impose overly restrictive screens, delay studies, or require costly upgrades",
        counter_arguments=[
            "IEEE 1547-2018 advanced functions provide grid benefits (voltage/frequency support)",
            "Standardized requirements streamline interconnection (reduce delays, costs)",
            "DER aggregations can provide grid services (FERC 2222)",
            "Hosting capacity analysis identifies where DER can connect with minimal upgrades",
            "Fast-track processes for small systems (<25 kW) reduce barriers"
        ],
        resolution_strategy="Use certified equipment (UL 1741 SA); engage utility early; leverage fast-track processes; aggregate DER for market participation; advocate for hosting capacity transparency",
        entity_scope="Solar, wind, battery developers, C&I customers, utilities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="IEEE 1547-2018 standard, FERC Order 2222, state PUC interconnection rules"
    ),

    DoctrineBlock(
        topic="nerc_reliability_standards_compliance",
        keywords=["NERC", "reliability", "CIP", "BAL", "MOD", "compliance", "bulk electric system"],
        conclusion_template=[
            "NERC (North American Electric Reliability Corporation) enforces mandatory reliability standards for the Bulk Electric System (BES)",
            "Key standard categories: BAL (balancing), VAR (voltage/reactive), CIP (cybersecurity), MOD (modeling), PRC (protection)",
            "Non-compliance penalties up to $1M/day/violation; NERC audits, self-reports, and spot checks enforce compliance"
        ],
        reasoning_framework="""
        NERC Reliability Standards Analysis:
        1. NERC Authority: FERC-approved Electric Reliability Organization (ERO) per Energy Policy Act 2005
        2. BES Definition: Facilities at ≥100 kV, generation ≥20 MVA (some ≥75 MVA), critical lower-voltage facilities
        3. Regional Entities: WECC, ERCOT, SERC, ReliabilityFirst, MRO, NPCC, SPP, RFC (enforce standards regionally)
        4. BAL Standards (Balancing and Frequency):
           - BAL-001: Real Power Balancing Control Performance (ACE limits)
           - BAL-002: Disturbance Control Standard (recover from contingencies within 15 min)
           - BAL-003: Frequency Response and Frequency Bias Setting
        5. VAR Standards (Voltage and Reactive Power):
           - VAR-001: Voltage and Reactive Control (maintain scheduled voltage at POI)
           - VAR-002: Generator Operation for Maintaining Network Voltage Schedules
        6. CIP Standards (Cybersecurity):
           - CIP-002: BES Cyber System Categorization (Low, Medium, High impact)
           - CIP-003 to CIP-011: Security policies, access controls, incident response, recovery plans
           - CIP-013: Supply Chain Risk Management (vendor security)
        7. MOD Standards (Modeling, Data, and Analysis):
           - MOD-032: Data for Power System Modeling and Analysis
           - Generator owners must provide validated models for planning studies
        8. PRC Standards (Protection and Control):
           - PRC-024: Generator Frequency and Voltage Ride-Through (low/high voltage, frequency)
           - PRC-025: Generator Relay Settings (ensure proper coordination)
        9. Compliance Enforcement:
           - Self-Certification: Annual compliance attestation
           - Audits: On-site reviews every 3-6 years
           - Spot Checks: Targeted reviews based on risk
           - Self-Reports: Violations must be disclosed within 24 hours (for some standards)
           - Penalties: Base penalty matrix + aggravating/mitigating factors, up to $1M/day
        10. Violation Severity Levels (VSL): Lower, Moderate, High, Severe (affects penalty)
        11. Mitigation Plans: Entity must remediate and prevent recurrence
        12. Compliance Culture: NERC assesses whether entity has robust compliance program
        """,
        key_factors=[
            "BES facility classification (generation, transmission, critical facilities)",
            "NERC standard applicability (which standards apply to specific entity types)",
            "CIP cyber asset categorization (impacts security control requirements)",
            "Evidence retention (3 years for most standards)",
            "Internal compliance program (policies, training, audits, documentation)",
            "Regional entity interpretation (some flexibility in standard application)",
            "Violation disclosure timing (self-report within 24 hours for some standards)"
        ],
        primary_authority=[
            "NERC Reliability Standards (100+ standards across 14 categories)",
            "FERC Order 672 (NERC ERO authority)",
            "NERC Rules of Procedure (Appendix 4B: Compliance Enforcement)",
            "NERC Compliance Monitoring and Enforcement Program (CMEP)",
            "Regional Entity Compliance Monitoring Plans"
        ],
        burden_holder="Registered Entity (GO, GOP, TO, TOP, BA, etc.) to prove continuous compliance with applicable standards",
        adversary_position="Industry argues some standards are overly prescriptive, burdensome for small entities, stifle innovation",
        counter_arguments=[
            "Standards prevent blackouts (2003 Northeast Blackout spurred NERC mandatory standards)",
            "Results-based standards (vs prescriptive) provide flexibility",
            "Regional variances allow adaptation to local conditions",
            "NERC provides compliance guidance, templates, and lessons learned",
            "Industry participates in standard development (stakeholder-driven process)"
        ],
        resolution_strategy="Invest in robust compliance program; track evidence; conduct internal audits; engage with NERC during standard development; leverage industry best practices",
        entity_scope="Generator owners/operators, transmission owners/operators, balancing authorities, reliability coordinators",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="FERC-approved NERC Reliability Standards, NERC Rules of Procedure, regional variance approvals"
    ),

    # ========== ECONOMIC ANALYSIS ==========

    DoctrineBlock(
        topic="levelized_cost_of_energy_lcoe",
        keywords=["LCOE", "levelized cost", "CapEx", "OpEx", "capacity factor", "discount rate", "NPV"],
        conclusion_template=[
            "Levelized Cost of Energy (LCOE) measures lifetime cost per MWh, accounting for capital, O&M, fuel, and financing costs",
            "LCOE = (CapEx × CRF + Annual OpEx) / (Capacity × 8760 × Capacity Factor), where CRF = capital recovery factor",
            "As of 2024, utility-scale LCOE: Solar $30-60/MWh, Wind $30-70/MWh, CCGT $45-75/MWh, Coal $60-120/MWh, Nuclear $90-150/MWh"
        ],
        reasoning_framework="""
        LCOE Calculation and Analysis:
        1. Formula: LCOE = Σ(Ct / (1+r)^t) / Σ(Et / (1+r)^t)
           - Ct = Costs in year t (CapEx, OpEx, fuel, decommissioning)
           - Et = Electricity generated in year t
           - r = Discount rate (WACC)
           - t = Year (0 to project lifetime)
        2. Capital Recovery Factor (CRF): CRF = r(1+r)^n / ((1+r)^n - 1)
           - Annualizes upfront CapEx over project life
           - Higher discount rate or shorter life = higher CRF
        3. CapEx Components:
           - EPC (engineering, procurement, construction)
           - Interconnection and transmission upgrades
           - Owner's costs (development, financing, insurance)
           - Contingency (typically 5-10%)
        4. OpEx Components:
           - Fixed O&M ($/kW-year): labor, parts, scheduled maintenance
           - Variable O&M ($/MWh): consumables, cycling costs
           - Fuel costs (for fossil plants)
           - Property taxes, insurance, land lease
        5. Capacity Factor Impact: Doubling capacity factor cuts LCOE nearly in half (fixed costs amortized over more MWh)
        6. Discount Rate (WACC): Weighted average cost of debt and equity
           - Higher risk projects (merchant, unproven tech) = higher WACC
           - Contracted projects (PPA) or regulated assets = lower WACC
           - Typical range: 3-8% (regulated utility) to 8-12% (merchant developer)
        7. Technology Comparisons:
           - Renewables: High CapEx, zero fuel cost, low OpEx, variable capacity factor
           - Fossil: Moderate CapEx, high fuel cost, moderate OpEx, high capacity factor
           - Nuclear: Very high CapEx, low fuel cost, moderate OpEx, very high capacity factor
        8. LCOE Limitations:
           - Ignores grid integration costs (transmission, storage, curtailment)
           - Does not capture value of dispatchability or ancillary services
           - Time-of-day energy value not reflected (solar peak ≠ evening peak)
        9. Value-Adjusted LCOE (VALCOE): LCOE adjusted for capacity credit, energy timing, ancillary services
        10. Sensitivity Analysis: Key drivers are CapEx, capacity factor, fuel prices, discount rate
        11. Learning Curves: Solar PV LCOE declined 90% since 2010 due to module cost reductions
        12. IRA Tax Credits: ITC/PTC reduce effective CapEx, lowering LCOE for renewables by 30-50%
        """,
        key_factors=[
            "CapEx ($/kW installed) and EPC cost escalation",
            "Capacity factor (annual production / theoretical max)",
            "Discount rate (WACC) and financing structure",
            "OpEx (fixed $/kW-year and variable $/MWh)",
            "Fuel costs and price volatility (for fossil plants)",
            "Project lifetime (20-30 years typical, 40-60 for nuclear)",
            "Tax incentives (ITC, PTC, accelerated depreciation)"
        ],
        primary_authority=[
            "NREL Annual Technology Baseline (ATB) - LCOE projections",
            "Lazard Levelized Cost of Energy Analysis (annual report)",
            "EIA Electricity Market Module documentation",
            "IEA World Energy Outlook - generation cost analysis",
            "EPRI Technical Assessment Guide - cost methodologies"
        ],
        burden_holder="Project developer to justify economic viability to investors, lenders, and offtakers",
        adversary_position="Critics argue LCOE oversimplifies (ignores integration costs, reliability value, capacity credit)",
        counter_arguments=[
            "LCOE provides apples-to-apples comparison for screening studies",
            "Sensitivity analysis reveals key economic drivers and risks",
            "Value-adjusted LCOE (VALCOE) addresses dispatchability and timing",
            "Portfolio optimization models (not LCOE alone) guide investment decisions",
            "LCOE trends (solar/wind declining, coal/nuclear rising) inform policy"
        ],
        resolution_strategy="Use LCOE for initial screening; supplement with capacity value, integration costs, and market price forecasts; conduct probabilistic analysis for high-risk inputs (fuel, CapEx)",
        entity_scope="Developers, utilities, regulators, investors, policy makers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="No controlling legal precedent; economic analysis standard practice per NREL, Lazard, IEA methodologies"
    ),

    DoctrineBlock(
        topic="power_purchase_agreement_ppa_structure",
        keywords=["PPA", "offtake", "contract", "fixed price", "tolling", "merchant", "capacity payment"],
        conclusion_template=[
            "Power Purchase Agreement (PPA) is a long-term contract (10-25 years) where buyer purchases electricity from generator at defined price and terms",
            "PPA types: Fixed-price ($/MWh), Capacity+Energy ($/kW-month + $/MWh), Tolling (buyer provides fuel), Merchant (no contract)",
            "PPA bankability critical for project financing - 15-20 year contracts with creditworthy offtakers reduce financing costs"
        ],
        reasoning_framework="""
        PPA Structure Analysis:
        1. Fixed-Price (Bundled) PPA:
           - Seller provides energy at fixed $/MWh for contract term
           - Seller takes fuel price risk, generation risk, market price risk
           - Buyer gets price certainty, hedge against market volatility
           - Common for renewables (zero fuel cost = predictable economics)
        2. Capacity + Energy (Unbundled) PPA:
           - Capacity Payment: $/kW-month for availability (covers CapEx + fixed OpEx)
           - Energy Payment: $/MWh for actual generation (covers fuel + variable OpEx)
           - Seller guaranteed revenue if available, buyer pays only for energy used
           - Common for gas peakers, baseload coal/nuclear
        3. Tolling Agreement:
           - Buyer provides fuel, seller converts to electricity (pays tolling fee)
           - Seller takes generation risk (forced outages, efficiency degradation)
           - Buyer takes fuel price risk and market price risk
           - Common for merchant gas plants serving load-serving entities
        4. Proxy Revenue (Virtual PPA):
           - Financial contract (no physical delivery)
           - Seller gets fixed price, buyer gets market price, contract settles difference
           - Enables corporate PPAs (buyer anywhere in grid, seller elsewhere)
        5. Contract Terms:
           - Term: 10-25 years (longer = better financing, higher risk of obsolescence)
           - Commercial Operation Date (COD): Milestone triggering contract obligations
           - Guaranteed Capacity: MW available during peak periods (with force majeure exceptions)
           - Liquidated Damages: Penalties for delayed COD, underperformance, early termination
           - Dispatch Rights: Who controls when/how much plant generates
        6. Price Escalation: Fixed, CPI-indexed, fuel-indexed, declining (solar/wind)
        7. Creditworthiness: Investment-grade offtaker (utility, tech company) vs speculative (merchant, startup)
        8. Collateral: Letters of credit, parent guarantees, reserves (secure performance obligations)
        9. Transmission: Who pays for delivery (generator vs buyer)
        10. Renewable Energy Certificates (RECs): Bundled or unbundled, who retains RECs
        11. Tax Equity Impact: ITC/PTC affect PPA pricing (developer passes through some savings to buyer)
        12. Merchant Risk: No PPA = full exposure to spot market prices (high risk, high potential reward)
        """,
        key_factors=[
            "Contract structure (fixed, capacity+energy, tolling, virtual)",
            "Contract term and price escalation (CPI, fixed, declining)",
            "Offtaker creditworthiness (investment grade vs sub-investment)",
            "Capacity factor risk allocation (P50, P90, P99 production estimates)",
            "Dispatch rights and curtailment provisions",
            "Force majeure and change-in-law protections",
            "RECs and environmental attributes ownership"
        ],
        primary_authority=[
            "FERC Section 205 (Filed Rate Doctrine for public utility PPAs)",
            "State PUC oversight of utility procurement (IRP, RFP, prudence review)",
            "PURPA Qualifying Facility (QF) contracts (mandatory purchase)",
            "ISDA Master Agreement (for financial virtual PPAs)",
            "Commercial contract law (UCC, state-specific)"
        ],
        burden_holder="Seller to deliver contracted capacity/energy; buyer to pay agreed price; both to negotiate bankable terms",
        adversary_position="Consumer advocates may challenge utility PPA costs as imprudent; generators may seek termination if uneconomic",
        counter_arguments=[
            "PPAs enable project financing (debt/equity require contracted revenue)",
            "Long-term contracts hedge buyer against price volatility",
            "Competitive procurement (RFPs) ensures least-cost supply",
            "Corporate PPAs drive renewable development beyond RPS mandates",
            "PPA terms evolve to balance risk (e.g., declining solar prices, RECs unbundled)"
        ],
        resolution_strategy="Structure PPA to align risks with party best able to manage; ensure bankability for financing; negotiate exit options for both parties; index pricing to market where possible",
        entity_scope="IPPs, utilities, corporate buyers, load-serving entities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="FERC filed rate doctrine, state PUC prudence reviews, PURPA mandatory purchase obligations"
    ),

    # ========== DISTRIBUTED GENERATION ==========

    DoctrineBlock(
        topic="combined_heat_and_power_chp_cogeneration",
        keywords=["CHP", "cogeneration", "thermal efficiency", "steam turbine", "heat recovery", "district heating"],
        conclusion_template=[
            "Combined Heat and Power (CHP) generates electricity and captures waste heat for useful thermal energy (space heating, process steam, cooling)",
            "CHP achieves 70-90% total efficiency (vs 30-50% for separate heat and power) by utilizing exhaust heat that would otherwise be wasted",
            "CHP technologies: gas turbines with HRSG, reciprocating engines with heat recovery, steam turbines with extraction/backpressure"
        ],
        reasoning_framework="""
        CHP System Analysis:
        1. Efficiency Comparison:
           - Separate Power (45%) + Separate Boiler (80%) = 65% avg system efficiency (100 units fuel → 45 power + 20 heat wasted)
           - CHP (80-90%): 100 units fuel → 30-40 power + 50-60 useful heat + 10-20 losses
           - Energy Savings: 20-30% fuel reduction for same power + heat output
        2. Gas Turbine CHP:
           - Gas turbine generates electricity, exhaust (900-1100°F) produces steam in HRSG
           - Steam used for process heat, space heating, absorption chilling, or steam turbine (combined cycle)
           - Sizes: 1-40 MW, electrical efficiency 25-40%, total CHP efficiency 70-80%
        3. Reciprocating Engine CHP:
           - Natural gas or diesel engine drives generator, jacket water and exhaust heat recovered
           - Jacket water (200°F) for low-temp heat, exhaust (700-1000°F) for steam or hot water
           - Sizes: 100 kW - 10 MW, electrical efficiency 35-45%, total CHP efficiency 75-85%
        4. Steam Turbine CHP:
           - Boiler generates high-pressure steam, steam passes through turbine (generates power), exhaust steam used for process
           - Extraction Turbine: Steam extracted at intermediate pressure for heating
           - Backpressure Turbine: Exhaust steam at elevated pressure (50-150 psi) for process use
           - Sizes: 500 kW - 250 MW, electrical efficiency 15-35%, total CHP efficiency 80-90%
        5. Thermal Load Matching: CHP economics depend on coincident electric and thermal loads (hospitals, universities, industrial plants)
        6. Power-to-Heat Ratio: Gas turbine (2:1), recip engine (1:1 to 1:2), steam turbine (1:3 to 1:10)
        7. Economics:
           - Spark Spread: (Power price - Fuel cost/efficiency) determines electricity value
           - Avoided Boiler Fuel: Thermal energy value = fuel cost of displaced boiler
           - CapEx: $1500-3500/kW installed (higher for small units, lower for large)
           - Payback: 3-7 years for good thermal load match
        8. Regulatory Drivers:
           - PURPA: Qualifying Facility (QF) status for <80 MW CHP (mandatory utility purchase)
           - EPA Combined Heat and Power Partnership (CHP incentives, technical assistance)
           - State incentives: CA Self-Generation Incentive Program, NY CHP tax credits
        9. Interconnection: IEEE 1547 compliance, backup/maintenance agreements with utility
        10. Emissions: EPA 40 CFR Part 60 Subpart KKKK (NSPS for stationary combustion turbines/engines)
        """,
        key_factors=[
            "Thermal load profile (magnitude, duration, temperature requirements)",
            "Electric load profile and coincidence with thermal load",
            "Fuel availability and pricing (natural gas most common)",
            "Power-to-heat ratio match with CHP technology",
            "Utility standby rates and interconnection charges",
            "Environmental permits (air quality, noise, emissions)",
            "Maintenance requirements and planned outage coordination"
        ],
        primary_authority=[
            "PURPA Section 210 (Qualifying Facility rules)",
            "EPA 40 CFR Part 60 Subpart KKKK (CHP emissions standards)",
            "FERC 18 CFR Part 292 (QF interconnection and rates)",
            "DOE CHP Technical Assistance Partnerships",
            "ASHRAE 90.1 (building energy standards allowing CHP credit)"
        ],
        burden_holder="CHP operator to maintain high availability to maximize fuel savings and revenue",
        adversary_position="Utilities may oppose CHP (reduces electricity sales), impose high standby charges, delay interconnection",
        counter_arguments=[
            "CHP provides onsite reliability (critical for hospitals, data centers)",
            "Reduces grid congestion and T&D losses (generation at point of use)",
            "Lowers GHG emissions per USEPA (20-30% reduction vs separate heat/power)",
            "PURPA QF status guarantees grid access and avoided-cost payments",
            "Resilience during grid outages (islanding capability if permitted)"
        ],
        resolution_strategy="Conduct detailed thermal/electric load analysis; select technology matching P/H ratio; negotiate favorable standby rates; pursue QF status; size for baseload thermal demand",
        entity_scope="Industrial facilities, hospitals, universities, district energy systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="PURPA Section 210, FERC QF regulations, state PUC interconnection tariffs"
    ),

    DoctrineBlock(
        topic="microgrid_design_and_operation",
        keywords=["microgrid", "islanding", "black start", "PCC", "master controller", "diesel genset", "battery storage"],
        conclusion_template=[
            "Microgrids are localized energy systems capable of operating grid-connected or islanded (isolated from utility grid)",
            "Key components: generation (solar, diesel, CHP), storage (batteries), loads, controls (microgrid controller), and point of common coupling (PCC) switch",
            "Applications: military bases, campuses, critical facilities (hospitals, data centers), remote communities, resilience/reliability enhancement"
        ],
        reasoning_framework="""
        Microgrid System Analysis:
        1. Definition: Self-contained electrical distribution system with local generation, storage, loads, and controls
        2. Operating Modes:
           - Grid-Connected: Utility provides baseload, microgrid DER supplements, imports/exports power
           - Islanded: Disconnected from utility (planned or unplanned), local generation serves all loads
           - Black Start: Start up from complete shutdown (no external power available)
        3. Components:
           - DER: Solar PV, wind, CHP, diesel/natural gas generators (provides power)
           - Energy Storage: Batteries (Li-ion, flow), flywheels (short-duration, frequency stabilization)
           - Loads: Critical loads (must serve), non-critical loads (can shed during island mode)
           - Point of Common Coupling (PCC): Switch isolating microgrid from utility grid
           - Microgrid Controller: Master controller coordinates DER dispatch, load shedding, seamless transition
        4. Microgrid Controller Functions:
           - Economic Dispatch: Optimize DER scheduling to minimize cost (grid-connected mode)
           - Seamless Transition: Detect utility outage, island within <1 second, no load interruption
           - Frequency/Voltage Regulation: Maintain 60 Hz ± 0.1 Hz, voltage ± 5% during island
           - Load Shedding: Drop non-critical loads if generation < demand (islanded mode)
           - Black Start Sequencing: Start diesel gensets, synchronize DER, energize loads in priority order
           - Resynchronization: Match microgrid voltage/frequency/phase to utility before reconnecting
        5. Battery Storage Sizing:
           - Energy Capacity (kWh): Island duration × critical load (e.g., 4 hours × 500 kW = 2000 kWh)
           - Power Capacity (kW): Maximum load step + ramp rate support (e.g., 500 kW + 200 kW = 700 kW)
           - C-rate: Power/Energy (e.g., 700 kW / 2000 kWh = 0.35C, ~3 hour discharge)
        6. Generator Sizing:
           - Must carry critical load + losses during island mode
           - Diesel gensets: 500-5000 kW, slow start (1-5 min), baseload in island mode
           - Gas turbines: 5-40 MW, fast start (5-10 min), for larger microgrids
        7. Protection Coordination:
           - Microgrid must have internal protection (overcurrent, ground fault, arc flash)
           - Islanding must not energize de-energized utility lines (anti-islanding per IEEE 1547)
           - Reclosers, relays must coordinate in both grid-connected and islanded modes
        8. Communications: IEC 61850, Modbus, DNP3 for DER control, SCADA for operator visibility
        9. Economics:
           - CapEx: $2000-5000/kW (high cost due to controls, storage, redundancy)
           - Revenue: Avoided utility demand charges, energy arbitrage, resiliency value (avoided outage costs)
           - Grants: DOD, DOE, state programs for microgrid resilience
        10. Regulatory: IEEE 1547, UL 1741, state interconnection rules apply to grid-connected operation
        """,
        key_factors=[
            "Critical load identification and prioritization",
            "Island duration requirement (hours to days)",
            "DER mix (solar, CHP, diesel) and capacity sizing",
            "Battery storage energy and power capacity",
            "Seamless transition vs brief interruption tolerance",
            "Black start capability (diesel gensets typically provide)",
            "Cost-benefit analysis (resilience value vs CapEx)"
        ],
        primary_authority=[
            "IEEE 2030.7 Standard for Microgrid Controllers",
            "IEEE 1547 (Interconnection of DER)",
            "UL 1741 (Inverters, Converters, Controllers for DER)",
            "NFPA 70 Article 705 (Interconnected Electric Power Production Sources)",
            "DOE Microgrid Program (technical assistance, funding)"
        ],
        burden_holder="Microgrid owner to design, test, and operate system safely in all modes",
        adversary_position="Utilities may resist microgrids (reduces sales), impose interconnection barriers, prohibit islanding",
        counter_arguments=[
            "Microgrids enhance grid resilience (critical facilities maintain power during outages)",
            "Reduce utility peak demand (demand charges, infrastructure deferral)",
            "Enable renewable integration (storage smooths solar/wind variability)",
            "Resilience value (avoided outage costs for hospitals, military, data centers) justifies premium cost",
            "IEEE standards and UL certifications ensure safety"
        ],
        resolution_strategy="Conduct detailed resilience value analysis; engage utility early on interconnection; pilot test seamless transitions; secure grant funding (DOD, DOE); prioritize critical loads",
        entity_scope="Military bases, hospitals, universities, industrial facilities, remote communities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="IEEE 2030.7, state PUC tariffs on islanding and interconnection"
    )
]

# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class TelemetryCollector:
    """Tracks query performance and doctrine usage"""
    def __init__(self):
        self.queries_processed = 0
        self.total_latency_ms = 0.0
        self.doctrine_hit_count: Dict[str, int] = {}
        self.error_count = 0

    def record_query(self, latency_ms: float, doctrines_used: List[str], error: bool = False):
        self.queries_processed += 1
        self.total_latency_ms += latency_ms
        if error:
            self.error_count += 1
        for doctrine in doctrines_used:
            self.doctrine_hit_count[doctrine] = self.doctrine_hit_count.get(doctrine, 0) + 1

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "queries_processed": self.queries_processed,
            "avg_latency_ms": self.total_latency_ms / max(1, self.queries_processed),
            "error_rate": self.error_count / max(1, self.queries_processed),
            "top_doctrines": sorted(self.doctrine_hit_count.items(), key=lambda x: x[1], reverse=True)[:10]
        }

TELEMETRY = TelemetryCollector()

# ============================================================================
# CORE REASONING ENGINE
# ============================================================================

class PowerGenerationEngine:
    """Main reasoning engine for power generation intelligence"""

    def __init__(self):
        self.doctrines = {d.topic: d for d in DOCTRINE_CACHE}
        logger.info(f"Loaded {len(self.doctrines)} doctrine blocks")

    def three_layer_response(self, query: str, mode: ResponseMode) -> QueryResponse:
        """TIE-20 Component: Three-layer reasoning (cache → semantic → deep)"""
        start_time = datetime.now()

        # Layer 1: Doctrine cache lookup
        matched_doctrines = self._match_doctrines(query)

        if not matched_doctrines:
            # Fallback: generic power generation guidance
            matched_doctrines = [self.doctrines["coal_fired_power_plant_operation"]]

        # Layer 2: Semantic analysis
        key_factors = self._extract_key_factors(query, matched_doctrines)

        # Layer 3: Deep synthesis
        answer = self._synthesize_answer(query, matched_doctrines, key_factors, mode)

        # Compute determinism hash
        hash_input = f"{query}|{mode.value}|{[d.topic for d in matched_doctrines]}"
        determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        # Collect authorities
        authorities = []
        for doctrine in matched_doctrines:
            authorities.extend(doctrine.primary_authority)

        elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
        TELEMETRY.record_query(elapsed_ms, [d.topic for d in matched_doctrines])

        return QueryResponse(
            query=query,
            mode=mode,
            answer=answer,
            confidence=matched_doctrines[0].confidence if matched_doctrines else ConfidenceLevel.DISCLOSURE,
            doctrines_applied=[d.topic for d in matched_doctrines],
            key_factors=key_factors,
            authorities=list(set(authorities))[:5],
            determinism_hash=determinism_hash,
            timestamp=datetime.now().isoformat()
        )

    def _match_doctrines(self, query: str) -> List[DoctrineBlock]:
        """Match query to relevant doctrine blocks"""
        query_lower = query.lower()
        matches = []

        for doctrine in DOCTRINE_CACHE:
            score = 0
            for keyword in doctrine.keywords:
                if keyword.lower() in query_lower:
                    score += 1
            if doctrine.topic.replace("_", " ") in query_lower:
                score += 3
            if score > 0:
                matches.append((score, doctrine))

        matches.sort(reverse=True, key=lambda x: x[0])
        return [d for _, d in matches[:3]]

    def _extract_key_factors(self, query: str, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract key factors from matched doctrines"""
        factors = []
        for doctrine in doctrines:
            factors.extend(doctrine.key_factors[:3])
        return factors[:5]

    def _synthesize_answer(self, query: str, doctrines: List[DoctrineBlock],
                          key_factors: List[str], mode: ResponseMode) -> str:
        """Synthesize answer based on mode"""
        if mode == ResponseMode.FAST:
            return self._fast_response(doctrines)
        elif mode == ResponseMode.DEFENSE:
            return self._defense_response(query, doctrines, key_factors)
        else:  # MEMO
            return self._memo_response(query, doctrines, key_factors)

    def _fast_response(self, doctrines: List[DoctrineBlock]) -> str:
        """Concise response (FAST mode)"""
        if not doctrines:
            return "Insufficient information to provide specific guidance."

        primary = doctrines[0]
        conclusions = " ".join(primary.conclusion_template)
        return f"{conclusions}\n\nKey considerations: {', '.join(primary.key_factors[:3])}."

    def _defense_response(self, query: str, doctrines: List[DoctrineBlock],
                         key_factors: List[str]) -> str:
        """Audit-ready response (DEFENSE mode)"""
        sections = []
        sections.append("POWER GENERATION ANALYSIS\n")

        for i, doctrine in enumerate(doctrines, 1):
            sections.append(f"{i}. {doctrine.topic.replace('_', ' ').upper()}")
            sections.append("\nConclusion:")
            sections.append(" ".join(doctrine.conclusion_template))
            sections.append("\n\nKey Factors:")
            for factor in doctrine.key_factors[:5]:
                sections.append(f"  • {factor}")
            sections.append("\n\nApplicable Standards/Authority:")
            for auth in doctrine.primary_authority[:3]:
                sections.append(f"  • {auth}")
            sections.append("\n")

        sections.append(f"CONFIDENCE LEVEL: {doctrines[0].confidence.value}")

        return "\n".join(sections)

    def _memo_response(self, query: str, doctrines: List[DoctrineBlock],
                      key_factors: List[str]) -> str:
        """Full documentation (MEMO mode)"""
        sections = []
        sections.append("MEMORANDUM - POWER GENERATION INTELLIGENCE ENGINE\n")
        sections.append(f"SUBJECT: {query}\n")
        sections.append("EXECUTIVE SUMMARY")
        sections.append("=" * 60)

        if doctrines:
            sections.append(" ".join(doctrines[0].conclusion_template))

        sections.append("\n\nDETAILED ANALYSIS")
        sections.append("=" * 60)

        for doctrine in doctrines:
            sections.append(f"\n{doctrine.topic.replace('_', ' ').title()}")
            sections.append("-" * 60)
            sections.append("\nReasoning Framework:")
            sections.append(doctrine.reasoning_framework)

            if doctrine.adversary_position:
                sections.append("\n\nPotential Challenges:")
                sections.append(f"  {doctrine.adversary_position}")

            if doctrine.counter_arguments:
                sections.append("\nCounter-Arguments:")
                for arg in doctrine.counter_arguments:
                    sections.append(f"  • {arg}")

            sections.append(f"\n\nRecommended Strategy: {doctrine.resolution_strategy}")

        sections.append("\n\nAPPLICABLE AUTHORITY")
        sections.append("=" * 60)
        authorities = []
        for doctrine in doctrines:
            authorities.extend(doctrine.primary_authority)
        for auth in list(set(authorities)):
            sections.append(f"  • {auth}")

        sections.append(f"\n\nCONFIDENCE ASSESSMENT: {doctrines[0].confidence.value if doctrines else 'UNKNOWN'}")

        return "\n".join(sections)

# ============================================================================
# GLOBAL ENGINE INSTANCE
# ============================================================================

ENGINE = PowerGenerationEngine()
START_TIME = datetime.now()

# ============================================================================
# API ENDPOINTS
# ============================================================================

@APP.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    uptime = (datetime.now() - START_TIME).total_seconds()
    return HealthResponse(
        status="operational",
        engine="ENRG01_power_generation",
        version="1.0.0",
        port=9081,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=uptime
    )

@APP.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process power generation query"""
    try:
        logger.info(f"Processing query: {request.query[:100]}... (mode: {request.mode})")
        response = ENGINE.three_layer_response(request.query, request.mode)
        logger.info(f"Query processed successfully. Doctrines applied: {len(response.doctrines_applied)}")
        return response
    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        TELEMETRY.record_query(0, [], error=True)
        raise HTTPException(status_code=500, detail=f"Engine error: {str(e)}")

@APP.get("/metrics")
async def get_metrics():
    """Retrieve engine telemetry metrics"""
    return TELEMETRY.get_metrics()

@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total": len(DOCTRINE_CACHE),
        "topics": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "category": d.topic.split("_")[0].upper()
            }
            for d in DOCTRINE_CACHE
        ]
    }

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info("=" * 80)
    logger.info("ENRG01 Power Generation Intelligence Engine")
    logger.info("Version: 1.0.0 | Port: 9081")
    logger.info(f"Doctrines loaded: {len(DOCTRINE_CACHE)}")
    logger.info("=" * 80)

    uvicorn.run(APP, host="0.0.0.0", port=9081, log_level="info")
