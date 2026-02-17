"""
MECH01 - Industrial Pump Systems Intelligence Engine
TIE Gold Standard - Mechanical Engineering Domain

Expertise: Centrifugal pumps, positive displacement pumps, pump selection,
NPSH calculations, cavitation analysis, API standards, mechanical seals,
materials selection, reliability engineering.

Version: 1.0.0
Port: 9041
Authority Level: 9.2 (Field-proven pump engineering standards)
"""

import hashlib
import json
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict
import math

# Critical: Add engine directory to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# Configure structured logging
logger.add(
    Path(__file__).parent / "logs" / "mech01_{time:YYYY-MM-DD}.log",
    rotation="100 MB",
    retention="90 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
)


# ═══════════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════════


class ResponseMode(str, Enum):
    """Response depth modes"""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    """Stratified confidence levels"""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    """Position zones - never blur"""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class QueryRequest(BaseModel):
    """Pump engineering query request"""
    query: str = Field(..., min_length=3, max_length=2000)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    context: Optional[Dict[str, Any]] = None


class DoctrineBlock(BaseModel):
    """Single doctrine block - real pump engineering expertise"""
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: Optional[str] = None
    adversary_position: Optional[str] = None
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: List[str]
    confidence: ConfidenceLevel
    controlling_precedent: Optional[str] = None
    fact_fragility_score: float = Field(ge=0.0, le=10.0)


class QueryResponse(BaseModel):
    """Structured response"""
    answer: str
    confidence: ConfidenceLevel
    zone: AnalysisZone
    triggered_doctrines: List[str]
    reasoning_chain: List[str]
    epistemic_warnings: List[str]
    fact_fragility: float
    determinism_hash: str
    query_id: str
    timestamp: str


class HealthStatus(BaseModel):
    """Health check response"""
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float


# ═══════════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - REAL PUMP ENGINEERING EXPERTISE
# ═══════════════════════════════════════════════════════════════════════════════


DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Centrifugal Pump Specific Speed Selection",
        keywords=["specific speed", "ns", "impeller design", "pump selection", "efficiency"],
        conclusion_template=[
            "Specific speed (Ns) determines optimal impeller type and efficiency.",
            "Low Ns (500-1500) indicates radial flow, high efficiency at high head.",
            "High Ns (6000-15000) indicates axial flow, high efficiency at high flow.",
        ],
        reasoning_framework="""Specific speed is dimensionless number characterizing impeller geometry:

Ns = N × sqrt(Q) / H^0.75

Where:
- N = rotational speed (rpm)
- Q = flow rate (gpm at BEP)
- H = head per stage (ft)

Selection criteria:
- Ns 500-1000: Radial vane, high head, low flow (boiler feed)
- Ns 1500-3000: Francis vane, medium head/flow (most common)
- Ns 4000-6000: Mixed flow, low head, high flow
- Ns 7000-15000: Axial flow, very low head, very high flow

Efficiency vs Ns:
- Peak efficiency occurs at Ns = 2000-3000 for single stage
- Multi-stage pumps use lower Ns per stage for higher total head
- Increasing Ns beyond 4000 reduces efficiency but increases flow capacity

Field application: Oilfield water injection typically Ns = 1500-2500 (moderate head, moderate flow).""",
        key_factors=[
            "Rotational speed (higher N increases Ns)",
            "Flow requirement at BEP",
            "Total dynamic head per stage",
            "Efficiency target (peaks at Ns 2000-3000)",
            "NPSH available (low Ns needs more NPSHA)",
        ],
        primary_authority=[
            "Hydraulic Institute ANSI/HI 1.3 Centrifugal Pump Design",
            "API 610 11th Edition - Centrifugal Pumps for Petroleum",
            "Karassik Pump Handbook 4th Edition",
        ],
        counter_arguments=[
            "VFD allows speed adjustment to optimize Ns after installation",
            "Multi-stage design can achieve high head with moderate Ns per stage",
            "Suction specific speed (Nss) may be limiting factor, not Ns",
        ],
        resolution_strategy="Calculate Ns for duty point, select impeller type within efficiency range, verify NPSH margin >1.1× NPSHR.",
        entity_scope=["centrifugal pumps", "end suction", "between bearings", "multistage"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API 610 defines acceptable specific speed ranges by pump type",
        fact_fragility_score=2.1,
    ),

    DoctrineBlock(
        topic="NPSH Calculations and Cavitation Prevention",
        keywords=["NPSH", "NPSHA", "NPSHR", "cavitation", "suction", "vapor pressure"],
        conclusion_template=[
            "NPSHA must exceed NPSHR by minimum 1.1× margin (API 610).",
            "Cavitation occurs when NPSHA < NPSHR, causing erosion and performance loss.",
            "Suction specific speed (Nss) predicts cavitation resistance.",
        ],
        reasoning_framework="""NPSH Available calculation (absolute pressure basis):

NPSHA = Pa + Ps - Pf - Pvp

Where:
- Pa = atmospheric pressure (14.7 psia at sea level, less at altitude)
- Ps = static pressure at pump suction (gage pressure + Pa)
- Pf = friction losses in suction piping
- Pvp = vapor pressure of liquid at pumping temperature

For open tank with liquid level above pump:
NPSHA = (Patm / ρg) + Zs - hfs - (Pvp / ρg)

Where Zs = static elevation of liquid above pump centerline.

NPSH Required:
- Vendor provides NPSHR curve (function of flow rate)
- Typically NPSHR increases with Q^2
- 3% head drop criterion defines NPSHR
- Cavitation begins before 3% drop visible

API 610 margin requirements:
- NPSHA ≥ 1.1 × NPSHR for pumps <100 hp
- NPSHA ≥ NPSHR + 5 ft for pumps >100 hp (more stringent)

Suction Specific Speed (Nss):
Nss = N × sqrt(Q) / NPSHR^0.75

- Nss > 11,000 indicates cavitation-resistant design (double suction, inducer)
- Nss < 8,500 indicates conventional design
- High Nss allows operation with lower NPSHA

Field indicators of cavitation:
- Noise (popcorn sound)
- Vibration increase
- Head/flow performance degradation
- Impeller pitting/erosion (usually inlet vane tips)""",
        key_factors=[
            "Liquid vapor pressure at operating temperature",
            "Suction piping friction losses (minimize)",
            "Atmospheric pressure (altitude correction)",
            "Static head available (tank elevation)",
            "NPSHR curve shape (steep rise at high flow)",
        ],
        primary_authority=[
            "API 610 Section 6.1.6 NPSH Requirements",
            "ANSI/HI 9.6.1 NPSH for Rotodynamic Pumps",
            "ASME PTC 8.2 Centrifugal Pump Test Code",
        ],
        counter_arguments=[
            "Inducer can reduce NPSHR by 50% (adds cost, complexity)",
            "Booster pump can increase NPSHA (adds equipment, energy)",
            "Reducing pump speed lowers NPSHR per affinity laws",
        ],
        resolution_strategy="Calculate NPSHA worst-case (high temp, low level), compare to vendor NPSHR curve, verify 1.1× margin at all flow rates.",
        entity_scope=["all centrifugal pumps", "vertical turbine pumps", "canned motor pumps"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API 610 margin requirements are industry standard for process pumps",
        fact_fragility_score=1.8,
    ),

    DoctrineBlock(
        topic="Pump Affinity Laws",
        keywords=["affinity laws", "speed change", "impeller trim", "performance scaling"],
        conclusion_template=[
            "Flow varies directly with speed ratio (Q2/Q1 = N2/N1).",
            "Head varies with speed squared (H2/H1 = (N2/N1)²).",
            "Power varies with speed cubed (P2/P1 = (N2/N1)³).",
        ],
        reasoning_framework="""Affinity laws relate pump performance to speed and impeller diameter:

Speed Change (same impeller diameter):
Q2/Q1 = N2/N1
H2/H1 = (N2/N1)²
BHP2/BHP1 = (N2/N1)³

Impeller Trim (same speed):
Q2/Q1 = D2/D1
H2/H1 = (D2/D1)²
BHP2/BHP1 = (D2/D1)³

Where:
- Q = flow rate (gpm)
- H = head (ft)
- BHP = brake horsepower
- N = rotational speed (rpm)
- D = impeller diameter (in)

Limitations:
- Valid only for homologous operation (same efficiency point)
- Accuracy degrades for speed changes >±20%
- Accuracy degrades for trim >10% (gap effects)
- Reynolds number effects at very low speeds
- Does not account for change in system curve

VFD application:
- Reducing speed to 80% reduces flow to 80%, head to 64%, power to 51%
- Significant energy savings for variable flow applications
- Affinity laws predict new operating point, but system curve also matters

Impeller trim application:
- Trim 5% diameter reduces flow ~5%, head ~10%, power ~14%
- Used to match pump to actual system curve
- Cheaper than new impeller, but irreversible
- Excessive trim (>15%) reduces efficiency, increases NPSHR""",
        key_factors=[
            "Speed ratio (VFD allows continuous adjustment)",
            "Impeller diameter ratio (trim is irreversible)",
            "System curve shape (determines actual operating point)",
            "Efficiency degradation with excessive speed/trim change",
            "NPSHR increases with speed/diameter",
        ],
        primary_authority=[
            "ANSI/HI 1.1-1.2 Centrifugal Pump Terminology",
            "API 610 Annex I - Affinity Laws",
            "DOE Motor Challenge Fact Sheet - Pump VFD Savings",
        ],
        counter_arguments=[
            "System curve changes invalidate affinity predictions",
            "Mechanical limits (bearing life, critical speed) restrict speed range",
            "VFD harmonics and motor heating limit speed reduction",
        ],
        resolution_strategy="Apply affinity laws to predict performance, verify with system curve intersection, confirm mechanical limits not exceeded.",
        entity_scope=["centrifugal pumps", "mixed flow pumps", "axial flow pumps"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        fact_fragility_score=1.5,
    ),

    DoctrineBlock(
        topic="Pump Curve Analysis - Operating Point Determination",
        keywords=["pump curve", "system curve", "operating point", "BEP", "head-capacity"],
        conclusion_template=[
            "Operating point is intersection of pump curve and system curve.",
            "Best efficiency point (BEP) is optimal for reliability and life.",
            "Operating >120% BEP flow causes recirculation and cavitation.",
        ],
        reasoning_framework="""Pump curve components:
1. Head-Capacity (H-Q): Head delivered vs flow rate
2. Efficiency curve: Peak at BEP (Best Efficiency Point)
3. Power curve: BHP vs flow (typically rising or flat)
4. NPSHR curve: Required NPSH vs flow (typically rising)

System curve equation:
Hsys = Hstatic + K × Q²

Where:
- Hstatic = static lift + pressure head (constant)
- K = system resistance coefficient (Σ friction losses)
- Q = flow rate

Operating point determination:
- Plot pump H-Q curve and system curve on same axes
- Intersection = actual operating point (Q_op, H_op)
- If Q_op near BEP → good design (80-110% BEP optimal)
- If Q_op << BEP → minimum flow recirculation issues
- If Q_op >> BEP → cavitation, vibration, radial thrust

Preferred operating range (API 610):
- 70-120% of BEP flow for reliability
- Outside range: increased wear, reduced bearing life, seal failures
- Recirculation zone: <70% BEP (suction/discharge recirculation)

System curve changes:
- Fouling increases K → curve shifts up → flow reduces
- Valve throttling increases K → flow reduces, efficiency penalty
- VFD changes pump curve → new operating point at lower energy

Parallel operation:
- Two identical pumps: each delivers ~60-65% of single pump flow (not 50%, due to curve shape)
- Combined curve = 2Q at same H
- System curve flattens → operating point shifts right""",
        key_factors=[
            "Pump curve shape (steep vs flat)",
            "System static head vs friction head ratio",
            "BEP location and preferred operating range",
            "Parallel pump operation (system curve flattens)",
            "Control method (throttle valve vs VFD)",
        ],
        primary_authority=[
            "ANSI/HI 9.6.3 Rotodynamic Pump Guideline",
            "API 610 Clause 6.1.8 Preferred Operating Region",
            "Hydraulic Institute Pump FAQs",
        ],
        counter_arguments=[
            "Modern pumps have wider efficient range (60-110% BEP)",
            "Recirculation control devices allow operation below 70% BEP",
            "Variable system (batch processes) may require operation across full curve",
        ],
        resolution_strategy="Calculate system curve, overlay pump curve, verify operating point within 70-120% BEP, check NPSHA margin adequate.",
        entity_scope=["centrifugal pumps", "end suction", "split case", "vertical turbine"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API 610 defines acceptable operating range relative to BEP",
        fact_fragility_score=2.0,
    ),

    DoctrineBlock(
        topic="Positive Displacement Pump Selection - Reciprocating vs Rotary",
        keywords=["PD pump", "reciprocating", "plunger", "diaphragm", "gear", "screw", "lobe"],
        conclusion_template=[
            "Reciprocating pumps deliver constant flow independent of pressure (ideal for metering).",
            "Rotary PD pumps (gear, screw, lobe) tolerate higher viscosity and solids.",
            "Pulsation dampeners required for reciprocating pumps to reduce piping vibration.",
        ],
        reasoning_framework="""Positive Displacement Pump Types:

RECIPROCATING (API 674/675):
1. Plunger/Piston pumps:
   - Flow rate: 0.1-5000 gpm
   - Pressure: up to 100,000 psi (ultra-high pressure)
   - Efficiency: 85-95%
   - Applications: High pressure water injection, hydraulic fracturing, descaling
   - Advantages: Highest pressure capability, good efficiency
   - Disadvantages: Pulsating flow, high maintenance (valves, packing), sensitivity to solids

2. Diaphragm pumps (API 675):
   - Flow: 0.01-500 gpm
   - Pressure: up to 15,000 psi
   - Sealless design (no packing/seal leakage)
   - Applications: Chemical metering, hazardous fluids, slurries
   - Advantages: Zero leakage, handles abrasives, corrosion resistant
   - Disadvantages: Diaphragm rupture risk, lower efficiency (75-85%), flow limited

ROTARY (API 676):
3. External gear pumps:
   - Flow: 1-1500 gpm
   - Pressure: up to 3000 psi
   - Viscosity: up to 500,000 SSU
   - Applications: Lube oil, hydraulic oil, polymer transfer
   - Advantages: Simple, compact, handles high viscosity
   - Disadvantages: Fixed clearances (wear), limited to clean fluids

4. Internal gear (gerotor):
   - Lower pressure (<500 psi)
   - Self-priming
   - Applications: Fuel oil, lube oil transfer

5. Screw pumps (twin/triple screw):
   - Flow: 5-5000 gpm
   - Pressure: up to 3000 psi
   - Low pulsation (unlike reciprocating)
   - Applications: Crude oil, fuel oil, viscous fluids
   - Advantages: Smooth flow, high efficiency (80-85%), handles entrained gas
   - Disadvantages: Expensive, close tolerances (abrasive wear)

6. Lobe pumps (Roots type):
   - Flow: 5-4000 gpm
   - Pressure: up to 200 psi
   - Large clearances (handles solids)
   - Applications: Wastewater, food processing, slurries
   - Advantages: Gentle pumping (no pulsation damage), handles viscous + solids
   - Disadvantages: Lower efficiency (50-70%), limited pressure

Selection criteria:
- Pressure required → reciprocating if >1000 psi
- Viscosity → rotary if >1000 cP
- Solids content → lobe or diaphragm
- Pulsation sensitivity → screw or lobe
- Metering accuracy → plunger or diaphragm
- Seal leakage concern → diaphragm (sealless)""",
        key_factors=[
            "Maximum discharge pressure required",
            "Fluid viscosity and temperature",
            "Solids content and abrasiveness",
            "Flow pulsation tolerance (piping vibration)",
            "Seal leakage restrictions (hazardous fluids)",
            "Metering accuracy required",
        ],
        primary_authority=[
            "API 674 Reciprocating Pumps for Petroleum",
            "API 675 Controlled Volume Metering Pumps",
            "API 676 Rotary Positive Displacement Pumps",
        ],
        counter_arguments=[
            "Centrifugal pumps cheaper for low pressure, low viscosity",
            "VFD on centrifugal can provide flow control (alternative to metering pump)",
            "Progressive cavity pumps bridge gap (handles solids, moderate pressure)",
        ],
        resolution_strategy="Define pressure, viscosity, solids content, pulsation tolerance → select PD type → size per API standard → verify materials compatibility.",
        entity_scope=["reciprocating pumps", "rotary PD pumps", "diaphragm pumps"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API 674/675/676 define design requirements by pump type",
        fact_fragility_score=2.2,
    ),

    DoctrineBlock(
        topic="Pump Materials Selection - Metallurgy",
        keywords=["materials", "impeller", "casing", "316SS", "duplex", "CD4MCu", "corrosion"],
        conclusion_template=[
            "Carbon steel suitable for non-corrosive hydrocarbon service.",
            "316SS (UNS S31600) standard for seawater and mild acids.",
            "Duplex stainless (2205, 2507) for high chloride + high stress.",
        ],
        reasoning_framework="""Pump Component Materials by Service:

HYDROCARBON SERVICE (crude oil, diesel, gasoline):
- Casing: Carbon steel ASTM A216 WCB (cast) or A105 (forged)
- Impeller: Cast iron (low cost), bronze (better wear), 316SS (sour service)
- Shaft: 416SS (13% Cr martensitic), 17-4PH (precipitation hardened)
- Sleeves: 316SS, 17-4PH, chrome plated
- Cost: Lowest (carbon steel = baseline)

SEAWATER / BRINE:
- Casing: 316SS (UNS S31600), duplex 2205 (higher chloride tolerance)
- Impeller: CD4MCu (cast duplex ~25% Cr, 5% Ni, 2% Mo, 3% Cu)
  - Excellent seawater resistance, similar cost to 316SS
  - Higher strength than 316SS (yield 65 ksi vs 30 ksi)
- Shaft: Duplex 2205, super duplex 2507 (offshore, high stress)
- Bearing housing: 316SS minimum
- Fasteners: A4 (316SS) or super duplex
- Chloride pitting resistance: 316SS PREN ~24, 2205 PREN ~35, 2507 PREN ~42
  - PREN = %Cr + 3.3×%Mo + 16×%N (higher = better pitting resistance)

SOUR SERVICE (H2S):
- NACE MR0175/ISO 15156 compliance required
- 316SS acceptable if hardness <22 HRC
- Duplex requires stress relief, hardness limits
- Carbon steel with hardness <22 HRC, no hard welds
- Avoid: Bronze (stress corrosion cracking in H2S)

ACIDIC SERVICE (pH <4):
- Dilute acids: 316SS (sulfuric <20%, hydrochloric <3%)
- Concentrated acids: Alloy 20 (UNS N08020), Hastelloy C-276
- Nitric acid: 304/316SS (passivates stainless)
- Hydrofluoric acid: Monel 400 (Ni-Cu alloy)

ABRASIVE SLURRIES:
- Impeller: High chrome white iron (15-28% Cr), A532 Class III
- Casing: A532 Class II, rubber lined carbon steel (fines)
- Expeller seals, flush plans to prevent solids ingress
- Hard facing: Tungsten carbide, Stellite overlays

HARDNESS LIMITS (NACE):
- Maximum 22 HRC for sour service (prevents sulfide stress cracking)
- Maximum 36 HRC for sweet service (hydrogen embrittlement resistance)
- Heat treatment critical (avoid hard welds, HAZ)

COST MULTIPLIERS (vs carbon steel):
- 316SS: 3-4×
- Duplex 2205: 4-5×
- CD4MCu: 3.5-4×
- Alloy 20: 8-10×
- Hastelloy C-276: 15-20×""",
        key_factors=[
            "Chloride concentration (pitting corrosion)",
            "pH (acidic vs alkaline)",
            "H2S partial pressure (sour service)",
            "Solids content and hardness (abrasive wear)",
            "Temperature (creep, thermal cycling)",
            "Stress level (SCC, HE susceptibility)",
        ],
        primary_authority=[
            "API 610 Annex G Materials Selection",
            "NACE MR0175/ISO 15156 Sour Service",
            "ASTM A743/A744 Stainless Steel Castings",
        ],
        counter_arguments=[
            "Coating/lining cheaper than exotic alloys (epoxy, rubber, glass flake)",
            "Anodic protection for carbon steel in specific services",
            "Inhibitor injection reduces corrosion rates",
        ],
        resolution_strategy="Characterize fluid chemistry (chloride, pH, H2S, solids) → select materials per API 610 Annex G → verify NACE compliance if sour → confirm hardness limits.",
        entity_scope=["all pump types", "wetted components"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API 610 Annex G and NACE MR0175 define materials selection criteria",
        fact_fragility_score=2.3,
    ),

    DoctrineBlock(
        topic="Mechanical Seal Selection and Flush Plans",
        keywords=["mechanical seal", "single seal", "double seal", "seal flush", "API 682"],
        conclusion_template=[
            "Single seals adequate for non-hazardous, non-flashing fluids.",
            "Double seals required for toxic, flammable, or volatile fluids (API 682).",
            "Seal flush Plan 11 (recirculation from pump) most common for clean fluids.",
        ],
        reasoning_framework="""Mechanical Seal Types (API 682 4th Edition):

SINGLE SEALS:
- One sealing interface (rotating vs stationary face)
- Emissions: 100-500 ppm typical (depends on fluid, pressure)
- Cost: Baseline
- Applications: Non-hazardous, non-volatile, clean fluids
- Limitations: Cannot meet fugitive emission regulations for VOCs (<500 ppm EPA)

DOUBLE SEALS:
- Two seals in series with barrier fluid between
- Inner seal (process side), outer seal (atmospheric side)
- Barrier fluid pressure 15-25 psi above process pressure
- Emissions: <10 ppm (barrier fluid, not process fluid)
- Cost: 2-3× single seal
- Applications: Toxic, flammable, volatile, or environmentally restricted fluids
- API 682 Category 2 (emissions <500 ppm VOC)

CARTRIDGE SEALS:
- Pre-assembled seal, gland, sleeve unit
- No field measurement/setting required
- Reduced installation time, fewer errors
- Cost: 1.5-2× component seal
- Preferred for API 610 pumps (reliability, interchangeability)

SEAL FLUSH PLANS (API 682):
Plan 11 - Internal recirculation from pump discharge:
  - Clean, cool fluid available in pump
  - No external system required
  - Most common (60% of applications)
  - Limited cooling (fluid already at pump temp)

Plan 13 - Internal recirculation through cooler:
  - Same as Plan 11 + external heat exchanger
  - Used when pumped fluid >200°F
  - Cooling water or air cooler
  - Extends seal life (elastomers, face temperature)

Plan 23 - External flush from separate source:
  - Clean fluid injected into seal chamber
  - Used when pumped fluid is dirty, viscous, or solidifies
  - Requires compatible flush fluid (water, oil, solvent)
  - Pressure >15 psi above pump discharge

Plan 32 - External circulation through reservoir + cooler (double seal):
  - Barrier fluid circulates by thermosiphon or pumped
  - Reservoir monitors barrier fluid level (leak detection)
  - Cooler maintains barrier fluid <180°F
  - Most common double seal arrangement

Plan 53 - Pressurized barrier fluid (double seal):
  - Bladder accumulator maintains barrier pressure
  - Nitrogen blanket for pressure maintenance
  - Used for high pressure or zero-emission applications
  - Higher cost, complexity

Plan 54 - Externally pressurized barrier with pumped circulation:
  - Dedicated pump circulates barrier fluid
  - Highest reliability for critical services
  - API 682 Category 1 (<50 ppm emissions)
  - Cost: 5-8× single seal system

BARRIER FLUIDS:
- Light mineral oil (most common, compatible with hydrocarbons)
- Synthetic PAO oil (wider temp range, better oxidation resistance)
- Glycol/water (for water-miscible process fluids)
- Must be compatible with process fluid (if seal fails, they mix)

SEAL FACE MATERIALS:
- Carbon vs Silicon Carbide (SiC): most common pairing
  - SiC excellent wear, corrosion resistance
  - Carbon softer (wear preferentially, protect SiC)
- SiC vs SiC: high temp, abrasive service (no carbon to burn/erode)
- Tungsten Carbide vs SiC: extreme abrasion (slurries)

SEAL FAILURE MODES:
- Face wear (improper flush, dry running, abrasives)
- Elastomer failure (temperature, chemical attack, extrusion)
- Secondary seal leak (O-ring damage, compression set)
- Mechanical damage (vibration, misalignment, transients)""",
        key_factors=[
            "Fluid hazard classification (toxic, flammable, VOC)",
            "Emission regulations (EPA, OSHA, local)",
            "Pumped fluid properties (clean, abrasive, viscous, temp)",
            "Seal chamber pressure and temperature",
            "Reliability requirements (MTBF, maintenance interval)",
        ],
        primary_authority=[
            "API 682 4th Edition Seal Systems for Centrifugal Pumps",
            "API 610 11th Edition Mechanical Seal Requirements",
            "EPA Method 21 Fugitive Emissions Monitoring",
        ],
        counter_arguments=[
            "Packing (braided rope) cheaper than mechanical seals (higher emissions, maintenance)",
            "Magnetic drive pumps eliminate seals entirely (sealless, limited power)",
            "Canned motor pumps sealless alternative (expensive, limited repair)",
        ],
        resolution_strategy="Classify fluid hazard → select seal type (single, double, cartridge) → choose flush plan per API 682 → verify emission compliance.",
        entity_scope=["centrifugal pumps", "API 610 pumps", "ANSI pumps"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API 682 defines seal types and flush plans for process pumps",
        fact_fragility_score=2.4,
    ),

    DoctrineBlock(
        topic="Pump Bearing Selection - Radial vs Thrust Loads",
        keywords=["bearings", "radial load", "thrust load", "ball bearing", "roller bearing"],
        conclusion_template=[
            "Ball bearings handle combined radial and thrust loads (most centrifugal pumps).",
            "Cylindrical roller bearings for high radial loads (large pumps, horizontal split case).",
            "Angular contact ball bearings for high axial thrust (multistage pumps).",
        ],
        reasoning_framework="""Bearing Types for Pumps:

BALL BEARINGS (Deep Groove):
- Radial load capacity: Moderate
- Axial load capacity: Moderate (up to 50% of radial rating)
- Speed: High (DN <500,000)
- Applications: Small/medium end suction pumps, <100 hp
- Advantages: Simple, cheap, combined load capability
- Limitations: Lower radial capacity than rollers

CYLINDRICAL ROLLER BEARINGS:
- Radial load capacity: Very high (line contact vs point)
- Axial load capacity: None (rollers slide axially)
- Speed: Moderate (DN <400,000)
- Applications: Large horizontal split case pumps, between bearings design
- Requires separate thrust bearing (usually ball on opposite end)
- Advantages: Highest radial capacity, thermal expansion accommodation
- Disadvantages: Cannot restrain shaft axially (needs paired thrust bearing)

ANGULAR CONTACT BALL BEARINGS:
- Radial load capacity: Moderate
- Axial load capacity: High (one direction)
- Mounted in pairs (back-to-back or face-to-face):
  - Back-to-back (DB): Handles thrust both directions, wider span (better moment resistance)
  - Face-to-face (DF): Handles thrust both directions, narrower span
- Applications: Multistage pumps (high axial thrust), vertical pumps
- Duplex mounting provides axial preload (eliminates clearance, improves accuracy)

TAPERED ROLLER BEARINGS:
- Radial load capacity: Very high
- Axial load capacity: High (one direction, inherent to taper)
- Mounted in pairs (opposed) to handle thrust both ways
- Applications: Large vertical turbine pumps, slurry pumps
- Advantages: Combined high radial + thrust capability
- Disadvantages: More complex mounting (preload adjustment critical)

LOAD CALCULATIONS:
Radial load = √(Fx² + Fy²)
Where Fx, Fy = bearing reactions from shaft analysis

Axial load sources:
- Impeller unbalanced thrust (single suction impellers)
- Pressure acting on shaft area
- Mechanical seal closing force (spring, pressure)
- Weight of shaft + impeller (vertical pumps)

Unbalanced impeller thrust:
T = (π/4) × D2² × (P_discharge - P_suction)
Reduced by wear rings, balance holes, back vanes

Bearing life calculation (L10):
L10 = (C/P)^p × 10^6 / (60 × N)

Where:
- L10 = rating life (hours) for 90% survival
- C = dynamic load rating (from bearing catalog)
- P = equivalent radial load (includes radial + thrust components)
- p = 3 for ball bearings, 10/3 for roller bearings
- N = rotational speed (rpm)

API 610 requirement: L10 ≥ 25,000 hours (2.85 years continuous)

LUBRICATION:
- Oil bath: Simple, cheap (small pumps <10 hp)
- Oil ring: Moderate speed, <3600 rpm (medium pumps)
- Flinger disc: Higher speed, better cooling (larger pumps)
- Forced oil circulation: Large pumps >500 hp (cooler, filtration)
- Grease: Low speed, low temp (<180°F), sealed bearings (ANSI pumps)

Oil viscosity selection:
- ISO VG 32: High speed (3600 rpm), normal temp
- ISO VG 68: Medium speed (1800 rpm), elevated temp
- ISO VG 150: Low speed (<900 rpm), high load

BEARING FAILURES:
- Fatigue spalling: Normal end of life (L10 reached)
- Brinelling: Impact loads, improper installation (hammer marks)
- Overheating: Insufficient lubrication, over-tightening, misalignment
- Contamination: Dirt, water ingress (use lip seals, labyrinth seals)
- Corrosion: Moisture, acids (use stainless bearings, better seals)""",
        key_factors=[
            "Radial load magnitude (bearing reactions)",
            "Axial thrust magnitude and direction",
            "Rotational speed (DN limit)",
            "Operating temperature (limits lubricant, materials)",
            "Required L10 life (API 610 minimum 25,000 hrs)",
        ],
        primary_authority=[
            "API 610 Section 6.3 Bearings and Bearing Housings",
            "SKF General Catalogue (bearing selection)",
            "ANSI/ABMA Std 9 Load Ratings for Ball Bearings",
        ],
        counter_arguments=[
            "Magnetic bearings eliminate wear, no lubrication (expensive, limited load)",
            "Fluid film bearings for very large pumps (oil whip issues)",
            "Ceramic hybrid bearings for high temp, corrosion (cost 5×)",
        ],
        resolution_strategy="Calculate radial and thrust loads → select bearing type → verify L10 life >25,000 hrs → choose lubrication method → specify seals.",
        entity_scope=["centrifugal pumps", "vertical turbine pumps", "API 610 pumps"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API 610 requires minimum 25,000 hour L10 bearing life",
        fact_fragility_score=2.0,
    ),

    DoctrineBlock(
        topic="Pump Vibration Analysis and Diagnostics",
        keywords=["vibration", "unbalance", "misalignment", "cavitation", "frequency analysis"],
        conclusion_template=[
            "1× running speed vibration indicates unbalance (rotor mass asymmetry).",
            "2× running speed indicates misalignment (coupling or bearing).",
            "Cavitation produces broadband high-frequency noise (5-20 kHz).",
        ],
        reasoning_framework="""Vibration Frequency Signatures:

1× RUNNING SPEED (1× RPM):
- Cause: Rotor unbalance (mass eccentricity)
- Radial vibration dominant
- Phase stable (repeats each revolution)
- Fix: Balance rotor per ISO 1940 (G6.3 for pumps)

2× RUNNING SPEED (2× RPM):
- Cause: Misalignment (angular or parallel offset)
  - Angular misalignment → high axial vibration
  - Parallel misalignment → high radial vibration
- Also: Bent shaft, eccentric coupling
- Fix: Precision alignment (laser alignment, <2 mils TIR)

VANE PASS FREQUENCY (VPF = # vanes × RPM):
- Cause: Impeller-to-volute interaction (pressure pulsations)
- Example: 6-vane impeller at 3600 rpm → 360 Hz (21,600 CPM)
- Normal in all pumps, but should be <0.1 in/sec
- Excessive if: Insufficient clearance, off-design operation, bad volute cutwater
- Fix: Increase radial clearance, move operating point toward BEP

SUBSYNCHRONOUS (< 1× RPM):
- Cause: Oil whirl (0.4-0.48× RPM) or oil whip (1st critical speed)
- Occurs in fluid film bearings (journal bearings)
- Unstable, can lead to bearing failure
- Fix: Increase bearing preload, change oil viscosity, switch to anti-friction bearings

CAVITATION SIGNATURE:
- Broadband noise 5-20 kHz (bubble collapse frequency)
- Random, not synchronous with rotation
- Audible "popcorn" or "gravel" sound
- Fix: Increase NPSHA (raise suction pressure, lower temp, reduce losses)

BEARING DEFECT FREQUENCIES:
- Outer race fault: BPFO = (N_balls / 2) × RPM × (1 - d/D)
- Inner race fault: BPFI = (N_balls / 2) × RPM × (1 + d/D)
- Ball fault: BSF = (D / 2d) × RPM × (1 - (d/D)²)
- Cage frequency: FTF = RPM / 2 × (1 - d/D)
Where d = ball diameter, D = pitch diameter

VIBRATION SEVERITY (ISO 10816):
- Zone A (Good): <2.8 mm/sec RMS (0.11 in/sec)
- Zone B (Acceptable): 2.8-7.1 mm/sec (0.11-0.28 in/sec)
- Zone C (Unsatisfactory): 7.1-11.2 mm/sec (0.28-0.44 in/sec)
- Zone D (Unacceptable): >11.2 mm/sec (>0.44 in/sec)

API 610 LIMITS:
- Unfiltered: 0.30 in/sec peak (4.8 mm/sec RMS)
- Proximity probe: 2.0 mils pk-pk shaft displacement

MEASUREMENT LOCATIONS:
- Bearing housing (radial, axial directions)
- Shaft proximity probes (direct rotor vibration)
- Coupling guard (for torsional vibration)

ROOT CAUSE FLOWCHART:
1. Measure vibration at bearings (3 axes: radial, axial, tangential)
2. Perform FFT (Fast Fourier Transform) → identify dominant frequencies
3. Compare to known signatures:
   - 1× → balance
   - 2× → misalignment
   - VPF → hydraulic
   - Broadband → cavitation
   - BPFO/BPFI → bearing fault
4. Trending: Monitor over time (weekly, monthly)
   - Sudden increase → investigate immediately
   - Gradual increase → plan maintenance
5. Phase analysis: Measure phase angle at multiple points
   - In-phase → unbalance
   - 180° out → misalignment""",
        key_factors=[
            "Dominant frequency (1×, 2×, VPF, subsynchronous)",
            "Vibration severity (mm/sec RMS)",
            "Axial vs radial amplitude ratio",
            "Phase relationship (in-phase, 180°, random)",
            "Trend over time (stable, increasing, intermittent)",
        ],
        primary_authority=[
            "API 610 Section 6.7 Vibration and Noise",
            "ISO 10816 Mechanical Vibration Standards",
            "ISO 1940 Balance Quality for Rotors",
        ],
        counter_arguments=[
            "Low frequency vibration (<10 Hz) may be piping pulsation, not pump",
            "High vibration with good FFT may be loose foundation (structural resonance)",
            "Temperature, not vibration, may be first indicator of bearing failure",
        ],
        resolution_strategy="Measure vibration FFT → identify dominant frequency → compare to known signatures → perform corrective action → retest → trend.",
        entity_scope=["all rotating pumps", "centrifugal", "PD pumps with rotating elements"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API 610 and ISO 10816 define acceptable vibration limits",
        fact_fragility_score=2.5,
    ),

    DoctrineBlock(
        topic="API 610 Centrifugal Pump Standard Compliance",
        keywords=["API 610", "process pump", "reliability", "design requirements"],
        conclusion_template=[
            "API 610 defines minimum requirements for petroleum/chemical process pumps.",
            "Compliance ensures reliability: bearing life >25,000 hrs, mechanical seal API 682.",
            "OH2 (overhung, single stage, centerline mount) most common configuration.",
        ],
        reasoning_framework="""API 610 11th Edition Key Requirements:

PUMP TYPES (Configuration Codes):
- OH1: Overhung impeller, single stage, foot mounted
- OH2: Overhung impeller, single stage, centerline mounted (most common)
- OH3: Overhung impeller, two stage
- BB1: Between bearings, single stage, axially split (horizontal split case)
- BB2: Between bearings, single stage, radially split (barrel)
- BB3: Between bearings, multistage, axially split
- BB5: Between bearings, multistage, barrel (high pressure)
- VS1: Vertical suspended, single stage (sump pump)
- VS6: Vertical suspended, multistage (vertical turbine)

DESIGN REQUIREMENTS:
1. Bearing Life: L10 ≥ 25,000 hours minimum
2. Mechanical Seal: API 682 compliant (cartridge seal preferred)
3. Baseplate: Common for pump + driver, grouted (epoxy grout)
4. Coupling: Flexible, spacer type (allows seal removal without disturbing alignment)
5. Materials: Per Annex G (corrosion/erosion resistance)
6. Vibration: <0.30 in/sec unfiltered, <2.0 mils shaft displacement
7. NPSH Margin: NPSHA ≥ 1.1× NPSHR or NPSHA ≥ NPSHR + 5 ft (>100 hp)
8. Casing Design Pressure: 1.5× max operating pressure (minimum 25 psig)
9. Hydrotest: 1.5× design pressure (casing + cover)
10. Preferred Operating Region: 70-120% BEP flow

PERFORMANCE TEST (Section 6.10):
- Conducted per ASME PTC 8.2 or ISO 9906 Grade 1
- Minimum 5 test points across curve
- Tolerances: Q ±3%, H ±5%, efficiency per curve
- NPSHR test at 1.03× rated flow
- Vibration, sound, temperature limits

MATERIALS UPGRADES (vs ANSI pumps):
- Casing: Upgraded to corrosion-resistant alloy (316SS vs cast iron)
- Impeller: 316SS minimum (vs bronze)
- Shaft: 17-4PH or duplex (vs 416SS)
- Fasteners: A4-70 (316SS) vs B7 carbon steel
- Wear rings: Hardness differential >50 points (prevent galling)

SEAL CHAMBER (Section 6.1.9):
- API 682 dimensions (standardized)
- Seal flush connections (Plan 11, 13, 23, 32, etc.)
- Throttle bushing for high pressure drops (>300 psi)
- Vent and drain connections

NOZZLES:
- Suction nozzle: 1-2 sizes larger than discharge (reduce velocity, NPSHA)
- Flange rating: ASME B16.5 (150#, 300#, 600#, etc.)
- Top suction / top discharge for OH2 (maintenance access)

COUPLINGS:
- Spacer type (allows seal maintenance without disturbing alignment)
- Flexible element (elastomer, disc, gear)
- Guard required (OSHA)
- Service factor ≥1.5 (torque margin)

AUXILIARY SYSTEMS:
- Seal support system per API 682 (Plan 32, 53, 54)
- Bearing lubrication (oil mist for high speed, oil bath for low speed)
- Cooling water for seal/bearing if temp >180°F

INSPECTION AND TESTING:
- Rotor balance per ISO 1940 G6.3
- Hydrostatic test 1.5× design pressure
- Mechanical run test (2 hours minimum)
- Witness test if specified (purchaser present)

DOCUMENTATION (Section 9):
- Certified drawings (cross-section, outline, curve)
- Nameplate data
- Parts list with materials
- Maintenance manual
- Test reports""",
        key_factors=[
            "Pump type (OH2, BB1, etc.) per service requirements",
            "Design pressure (1.5× max operating)",
            "Materials per Annex G (fluid compatibility)",
            "Bearing life >25,000 hrs",
            "NPSH margin compliance",
            "Seal system per API 682",
        ],
        primary_authority=[
            "API 610 11th Edition Centrifugal Pumps for Petroleum",
            "API 682 4th Edition Shaft Sealing Systems",
            "ASME PTC 8.2 Centrifugal Pump Performance Test",
        ],
        counter_arguments=[
            "ANSI B73.1 pumps cheaper for non-critical services (commercial/industrial)",
            "ISO 5199/13709 international equivalent (metric units)",
            "Custom engineered pumps for unique requirements (not API standard)",
        ],
        resolution_strategy="Define service conditions → select pump type per API 610 → specify materials, seals, bearings → verify compliance with all requirements → witness test.",
        entity_scope=["process pumps", "petroleum refining", "chemical plants", "pipeline pumps"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API 610 is industry standard for process pump procurement",
        fact_fragility_score=1.7,
    ),

    DoctrineBlock(
        topic="Pump Alignment - Laser vs Reverse Indicator Methods",
        keywords=["alignment", "coupling", "laser alignment", "dial indicator", "soft foot"],
        conclusion_template=[
            "Laser alignment achieves <2 mils misalignment (vs 5-10 mils dial indicator).",
            "Soft foot must be corrected before alignment (shim under feet until <2 mils).",
            "Hot alignment accounts for thermal growth (pump/motor expand differently).",
        ],
        reasoning_framework="""Precision Alignment Process:

PRE-ALIGNMENT CHECKS:
1. Foundation: Level, grouted, no voids (ring test with hammer)
2. Baseplate: Flat, no twist (check corners with precision level)
3. Pipe strain: Disconnect coupling, check shaft movement (should be <2 mils)
   - If shaft moves >5 mils when uncoupling → piping forces excessive
   - Fix: Adjust pipe supports, add expansion loops, correct cold spring
4. Soft foot check:
   - Loosen one foot bolt at a time, measure shaft vertical movement with dial indicator
   - If movement >2 mils → soft foot exists (shim under foot)
   - Causes: Uneven baseplate, dirt under foot, warped machine foot
   - Fix: Add shims (stainless steel, no more than 3 per stack)

DIAL INDICATOR (REVERSE INDICATOR) METHOD:
Setup:
- Mount dial indicators on coupling (radial + axial readings)
- Zero at 12:00 position
- Rotate shafts together, record readings at 3:00, 6:00, 9:00

Radial (offset) measurement:
- Average 12:00 and 6:00 readings
- Offset = average × (coupling diameter / indicator radius)

Axial (angular) measurement:
- Difference between 12:00 and 6:00
- Angular misalignment = difference / coupling diameter

Tolerances (general machinery):
- Offset: <5 mils at coupling
- Angular: <1 mil per inch of coupling diameter

LASER ALIGNMENT METHOD:
Advantages:
- Accuracy: <0.5 mils (vs 2-5 mils dial indicator)
- Speed: 30 min vs 2+ hours dial indicator
- Live readout: Adjust and see results real-time
- Thermal compensation: Input machine temps, calculate hot alignment
- Documentation: Save alignments, trend over time

Procedure:
1. Mount laser transmitter on pump shaft
2. Mount detector on motor shaft (or vice versa)
3. Rotate shafts to measure offset and angularity
4. Software calculates shim corrections (vertical, horizontal)
5. Add/remove shims under motor feet
6. Recheck alignment
7. Target: <2 mils offset, <1 mil angularity

HOT vs COLD ALIGNMENT:
- Pumps expand upward when hot (casing heats, expands)
- Motors also expand (but less than pumps typically)
- Hot alignment offset = cold offset + thermal growth difference
- Example: 350°F pump may grow 10 mils upward from ambient
  - Set cold alignment 10 mils low → hot alignment perfect
- Laser software calculates hot alignment if temperatures entered

COMMON MISTAKES:
- Aligning with pipe strain (must disconnect coupling first)
- Ignoring soft foot (shims will compress unevenly, alignment lost)
- Not checking alignment after grouting (grout shrinkage moves machine)
- Aligning cold when pump operates hot (>200°F)

API 610 ALIGNMENT REQUIREMENTS:
- Alignment tolerances not explicitly specified
- Industry practice: <2 mils for critical pumps
- Verify alignment after:
  - Installation
  - Maintenance (bearing, seal replacement)
  - Coupling replacement
  - Every 12 months (or per vibration monitoring)

COUPLING TYPES (alignment sensitivity):
- Gear coupling: Most forgiving (angular misalignment OK)
- Elastomer coupling: Less forgiving (misalignment causes premature wear)
- Disc coupling: Least forgiving (tight alignment critical)
- Magnetic coupling: Very sensitive (gap must remain uniform)""",
        key_factors=[
            "Soft foot magnitude (must be <2 mils before alignment)",
            "Pipe strain (disconnect coupling to check)",
            "Operating temperature (hot vs cold alignment offset)",
            "Alignment method (laser vs dial indicator accuracy)",
            "Coupling type (tolerance to misalignment)",
        ],
        primary_authority=[
            "API 610 Section 7.2 Installation and Alignment",
            "RP 686 Machinery Installation and Installation Design (withdrawn but used)",
            "Shaft Alignment Handbook - Piotrowski",
        ],
        counter_arguments=[
            "Rough alignment (<10 mils) acceptable for non-critical ANSI pumps",
            "Self-aligning couplings compensate for misalignment (but reduce life)",
            "Flexure in piping may require intentional misalignment offset",
        ],
        resolution_strategy="Check soft foot → correct pipe strain → perform laser alignment → set hot/cold offset → verify <2 mils → document → trend over time.",
        entity_scope=["all coupled pumps", "motor-driven", "turbine-driven"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Industry best practice requires <2 mils misalignment for reliability",
        fact_fragility_score=2.2,
    ),

    DoctrineBlock(
        topic="Variable Speed Drives for Pump Energy Savings",
        keywords=["VFD", "VSD", "energy savings", "throttle valve", "affinity laws"],
        conclusion_template=[
            "VFD reduces energy consumption by cube of speed ratio (50% speed = 12.5% power).",
            "Throttle valve control wastes energy (converts to heat, pressure drop).",
            "Payback period typically <2 years for variable flow applications.",
        ],
        reasoning_framework="""VFD Energy Savings Analysis:

THROTTLE VALVE vs VFD COMPARISON:
Throttle valve control:
- Pump runs at constant speed (100% power at full speed)
- Valve closes to reduce flow → creates pressure drop
- Energy wasted as heat across valve
- Pump operates away from BEP → lower efficiency
- Power reduction minimal (maybe 10-20% at 50% flow)

VFD control:
- Pump speed reduced to match required flow
- Affinity laws: P2/P1 = (N2/N1)³
- 80% speed → 64% flow, 51% power (49% energy savings)
- 50% speed → 50% flow, 12.5% power (87.5% savings!)
- Pump remains near BEP (efficiency maintained)

EXAMPLE CALCULATION:
100 HP pump, 8000 hrs/year, $0.10/kWh electricity cost

Baseline (throttle valve):
- Full load power: 100 HP × 0.746 kW/HP = 74.6 kW
- Annual energy: 74.6 kW × 8000 hrs = 596,800 kWh
- Annual cost: 596,800 kWh × $0.10 = $59,680

With VFD (average 70% speed operation):
- Reduced power: 74.6 kW × (0.7)³ = 25.6 kW
- Annual energy: 25.6 kW × 8000 hrs = 204,800 kWh
- Annual cost: $20,480
- Savings: $39,200/year (66% reduction)

VFD cost: ~$15,000 for 100 HP unit
Payback: $15,000 / $39,200 = 0.38 years (4.6 months!)

APPLICATIONS BEST FOR VFD:
1. Variable flow demand:
   - Batch processes (changing flow rates)
   - Seasonal load variation (HVAC)
   - Multiple loads (parallel pumps, turn one off with VFD)
2. Flat system curve (high friction, low static):
   - Energy savings proportional to flow reduction
   - Steep system curve (high static) → less savings
3. Long operating hours:
   - 24/7 operation → maximum annual savings
   - Short runtime → longer payback

APPLICATIONS NOT SUITED FOR VFD:
1. Constant flow demand (no need to vary speed)
2. Steep system curve (mostly static head, little friction)
3. Low operating hours (<2000 hrs/year)
4. Positive displacement pumps (flow = speed × displacement, no pressure reduction)

VFD LIMITATIONS:
- Motor cooling reduced at low speed (<30 Hz / 50% speed)
  - May need external motor fan for continuous low speed
- Harmonics affect power quality (use filters, drive isolation transformer)
- Bearing currents (variable frequency → shaft voltage → bearing damage)
  - Fix: Insulated bearings, shaft grounding brush
- Resonance at certain speeds (critical speed of rotor)
  - Program VFD to skip resonant frequencies
- Minimum speed ~30% (below this, pump may surge or overheat)

PUMP CURVE CHANGES WITH VFD:
- Entire H-Q curve shifts per affinity laws
- 80% speed → 80% flow, 64% head
- System curve unchanged (TDH still same at any given flow)
- New operating point where pump curve (at new speed) intersects system curve

CONTROL STRATEGIES:
1. Manual speed adjustment (operator sets speed dial)
2. Flow setpoint (PID controller adjusts speed to maintain flow)
3. Pressure setpoint (maintain discharge pressure, common in water systems)
4. Level control (tank level setpoint, vary pump speed)

MOTOR CONSIDERATIONS:
- Standard NEMA motors rated for VFD use (inverter-duty insulation)
- Older motors may fail due to voltage spikes (dV/dt stress on windings)
- Motor nameplate: "Inverter Ready" or "VFD Rated"

PUMP CONSIDERATIONS:
- Thrust bearing sized for variable speed (thrust varies with speed²)
- Seal flush adequate at low speed (may need external flush if <50% speed)
- Minimum flow protection (software enforces minimum speed)""",
        key_factors=[
            "Flow variability (constant vs variable demand)",
            "Operating hours per year (longer = better payback)",
            "System curve shape (flat = high savings, steep = low savings)",
            "Electricity cost (higher = faster payback)",
            "Motor VFD compatibility (inverter-duty insulation)",
        ],
        primary_authority=[
            "DOE Motor Challenge Fact Sheet - Pumping Systems VFD",
            "ANSI/HI 1.4 Variable Speed Pumping",
            "Europump Variable Speed Driven Pumps - Best Practice Guide",
        ],
        counter_arguments=[
            "Two-speed motor cheaper than VFD (limited flexibility)",
            "Multiple smaller pumps instead of one large VFD pump (redundancy, staging)",
            "Throttle valve acceptable for short-duration flow changes",
        ],
        resolution_strategy="Analyze flow variation → calculate energy savings (affinity law) → estimate VFD cost → calculate payback → verify motor/pump compatible → implement.",
        entity_scope=["centrifugal pumps", "variable flow applications", "fan systems (similar physics)"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="DOE and Hydraulic Institute endorse VFDs for variable flow energy savings",
        fact_fragility_score=1.9,
    ),

    DoctrineBlock(
        topic="Multistage Pump Design and Application",
        keywords=["multistage", "high pressure", "boiler feed", "stages", "opposed impellers"],
        conclusion_template=[
            "Multistage pumps achieve high head (>500 ft) using multiple impellers in series.",
            "Opposed impeller arrangement (BB3) balances axial thrust.",
            "Stage count = total head / head per stage (limited by Ns per stage).",
        ],
        reasoning_framework="""Multistage Pump Design:

CONFIGURATION TYPES:
1. Inline (same direction impellers):
   - All impellers face same direction
   - Cumulative axial thrust (large thrust bearing required)
   - Simpler design, lower cost
   - Applications: Vertical turbine pumps, moderate stage count (<8)

2. Opposed (back-to-back impellers):
   - Half impellers face one direction, half opposite
   - Axial thrust balanced (minimal thrust bearing load)
   - API 610 BB3/BB5 configuration
   - Applications: High pressure (>1000 psi), many stages (>8)

3. Mixed (combination):
   - Some stages balanced, some inline
   - Partial thrust balance
   - Optimization for specific hydraulics

STAGE COUNT CALCULATION:
Number of stages = Total head required / Head per stage

Head per stage limited by:
- Specific speed (Ns) selection (1500-2500 for efficiency)
- Impeller diameter (mechanical stress limit)
- Materials (cast iron <300 ft/stage, steel <500 ft/stage)
- NPSH required (first stage critical)

Example:
Total head: 3000 ft
Head per stage: 400 ft
Stages required: 3000/400 = 7.5 → use 8 stages

FIRST STAGE CRITICAL:
- First stage sees lowest suction pressure (NPSHA critical)
- First stage impeller often larger diameter (lower Ns, lower NPSHR)
- Double-suction first stage (low NPSHR, balanced thrust)
- Inducer on first stage (for low NPSHA applications)

INTERSTAGE PRESSURE RISE:
- Each stage adds head (pressure)
- Interstage pressure = Suction + Σ(head of upstream stages)
- Casing pressure rating increases toward discharge
- Wear rings critical (high ΔP leakage path)

WEAR RING LEAKAGE:
- Recirculation from discharge side to suction side of each impeller
- Leakage flow = C × √ΔP
- Reduces efficiency (volumetric efficiency loss)
- Tight clearances critical (10-15 mils typical)
- Renewable rings (sacrifice rings, cheaper to replace than impeller)

AXIAL THRUST BALANCING:
Single direction impellers:
- Thrust = Σ(pressure × area on back shroud)
- Can exceed bearing capacity (>10,000 lbf common)

Opposed impellers (balanced):
- Half stages create thrust one direction
- Half stages create opposite thrust
- Net thrust <500 lbf (manageable by ball bearing)
- Residual thrust from:
  - Odd number of stages (one unbalanced)
  - Manufacturing tolerances
  - Wear (unequal clearances)

BALANCE DRUM/BALANCE DISC:
- Alternate to opposed impellers for thrust balance
- Balance drum: Shaft extension at discharge end, pressure acting on drum balances impeller thrust
- Balance disc: Floating disc behind last impeller, self-adjusting clearance
- Leakage flow returned to suction (energy loss)

APPLICATIONS BY TYPE:
BB3 (Axially Split, Multistage, Between Bearings):
- Boiler feed (3000+ psi)
- Pipeline pumps (1000-2000 psi)
- Waterflood injection (2000-5000 psi)
- Power: 100-20,000 HP

BB5 (Barrel, Multistage, Between Bearings):
- Very high pressure (>3000 psi)
- High temperature (>400°F)
- Hydrocarbon processing
- Barrel casing (single piece, radially split)
- Inner bundle removable (maintenance without disconnecting piping)

VS6 (Vertical Suspended, Multistage):
- Deep well pumps (oil production, water supply)
- Submersible (motor below pump, 4"-16" diameter)
- Lineshaft (motor at surface, long shaft to pump)
- Stages: 10-300 (oil wells may have 100+ stages)

EFFICIENCY CONSIDERATIONS:
- Each stage 75-85% efficient
- Overall efficiency = (stage efficiency)^n (where n = # stages)
- Example: 8 stages × 80% each = 0.80^8 = 16.8% overall (!!)
- Reality: Manufacturer optimizes, achieves 70-80% overall
- More stages → lower overall efficiency (leakage, friction losses)

MECHANICAL SEAL CHALLENGES:
- High pressure (3000+ psi) requires special seals
- Tandem seals (two seals in series, intermediate pressure breakdown)
- Cartridge seal with breakdown bushing
- API 682 Plan 53/54 (high pressure barrier fluid)""",
        key_factors=[
            "Total head required (determines stage count)",
            "Pressure per stage (limited by materials, stress)",
            "Axial thrust (opposed vs inline configuration)",
            "First stage NPSHA (critical for multistage)",
            "Efficiency target (more stages = lower efficiency)",
        ],
        primary_authority=[
            "API 610 BB3/BB5 Multistage Between Bearings Pumps",
            "ANSI/HI 2.1-2.2 Vertical Pumps Nomenclature",
            "Karassik Ch. 2.3 Multistage Centrifugal Pumps",
        ],
        counter_arguments=[
            "Multiple single-stage pumps in series (easier maintenance, higher efficiency)",
            "Positive displacement pump for very high pressure (>10,000 psi)",
            "Booster pump + single stage (two pumps, but simpler each)",
        ],
        resolution_strategy="Calculate total head → determine stages (400-500 ft/stage typical) → select configuration (opposed for >8 stages) → verify NPSHA for first stage → check efficiency.",
        entity_scope=["multistage centrifugal", "boiler feed", "pipeline", "vertical turbine"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API 610 defines multistage pump configurations BB3/BB5",
        fact_fragility_score=2.1,
    ),

    DoctrineBlock(
        topic="Slurry Pump Design and Abrasive Wear Considerations",
        keywords=["slurry", "abrasive", "hard iron", "rubber lined", "particle size"],
        conclusion_template=[
            "Hard iron (high chrome white iron) for coarse slurries (>200 mesh).",
            "Rubber lining for fine slurries (<200 mesh) - absorbs impact, prevents erosion.",
            "Recessed impeller design for large solids passage (trash pumps).",
        ],
        reasoning_framework="""Slurry Pump Metallurgy and Design:

ABRASIVE WEAR MECHANISMS:
1. Erosion: High velocity particles cut material (function of V³)
   - Increases rapidly with velocity (reduce impeller tip speed)
   - Particle angularity (sharp = worse)
   - Particle hardness (quartz, silica worse than clay)

2. Corrosion: Wet abrasives (acidic slurries accelerate wear)
   - Combined corrosion-erosion worse than either alone
   - Passivation layer removed by abrasion, exposing fresh metal

3. Impact: Large particles impact impeller/casing (fracture, spalling)
   - Depends on particle size, mass, velocity

MATERIALS SELECTION BY PARTICLE SIZE:
Coarse slurries (>1 mm, <200 mesh):
- High chrome white iron (15-28% Cr)
  - ASTM A532 Class III (15% Cr, 3% Mo) - standard
  - ASTM A532 Class III Type A (27% Cr) - extreme abrasion
  - Hardness: 58-62 HRC (very hard, wear resistant)
  - Carbide microstructure (M7C3, M23C6)
- Advantage: Excellent abrasion resistance, long life (2-5× mild steel)
- Disadvantage: Brittle (impact can crack), expensive

Fine slurries (<0.1 mm, >325 mesh):
- Rubber lining (natural or synthetic rubber)
  - Thickness: 1-2 inches
  - Hardness: 55-65 Shore A (softer than hard iron)
  - Absorbs particle impact (no rebound erosion)
  - Self-healing (small cuts close back up)
- Advantage: Excellent fine particle resistance, 5-10× steel life
- Disadvantage: Limited temperature (<180°F), chemicals attack rubber, initial cost high

Medium slurries (0.1-1 mm, 200-325 mesh):
- Options: Hard iron OR rubber (application dependent)
- Hard iron if: High temperature, chemically aggressive
- Rubber if: Cost-sensitive, moderate temp/chemistry

CORROSIVE SLURRIES:
- Duplex stainless steel (2205, 2507)
- Austenitic stainless 316SS (if low abrasion)
- Hard iron with corrosion resistant overlay (Stellite, tungsten carbide)

IMPELLER DESIGN TYPES:
1. Closed impeller (shrouds both sides):
   - Highest efficiency (80-85%)
   - Tight clearances (10-15 mils wear rings)
   - Clean to moderately dirty fluids
   - Abrasive wear on shrouds, rings

2. Semi-open impeller (front shroud only):
   - Moderate efficiency (70-75%)
   - Adjustable clearance (hand crank, wear adjustment)
   - Slurry service (less plugging than closed)
   - Common in hard iron slurry pumps

3. Open impeller (vanes only, no shrouds):
   - Lower efficiency (60-70%)
   - Large clearances (no plugging)
   - Very abrasive, large solids
   - Recessed impeller (large passage, non-clog)

4. Recessed impeller (rubber lined slurry):
   - Impeller recessed in casing (vortex action)
   - Solids don't contact impeller directly (less wear)
   - Efficiency 40-60% (lowest, but handles anything)
   - Trash pumps, sewage, construction dewatering

PARTICLE SIZE PASSAGE:
Rule of thumb: Impeller passage width ≥ 3× max particle size
- Example: 25 mm (1") max particle → 75 mm (3") passage minimum
- Prevents plugging, allows solids to pass through

VELOCITY LIMITS (ABRASIVE SERVICE):
- Wear rate ∝ V³ (velocity cubed relationship)
- Standard pumps: 100-150 ft/sec impeller tip speed
- Slurry pumps: 50-80 ft/sec (reduces wear dramatically)
- Reduce by: Lower speed (VFD), larger diameter impeller

WEAR LIFE PREDICTION:
Relative wear = (V/V_ref)³ × (C/C_ref)² × (particle_hardness_factor)

Where:
- V = fluid velocity
- C = solids concentration (% by weight)
- Hardness factor: Quartz = 1.0, Coal = 0.3, Clay = 0.1

OPERATING CONSIDERATIONS:
- Run near BEP (off-design increases recirculation wear)
- Avoid air ingestion (cavitation + abrasion = rapid failure)
- Maintain adequate NPSHA (cavitation erosion catastrophic with abrasives)
- Wear monitoring:
  - Performance degradation (head/flow drop)
  - Vibration increase (unbalanced from wear)
  - Scheduled teardown inspection (track hours, wear thickness)

EXPELLER SEALS (SLURRY):
- Packing (braided rope) common (cheap, tolerates abrasives)
- Mechanical seals with expeller (centrifugal action keeps solids out)
- Flush water to seal (clean water from external source)
- Seal chamber enlarged (reduce velocity, settling of solids away from seal)""",
        key_factors=[
            "Particle size distribution (fine, medium, coarse)",
            "Particle hardness (Mohs scale - quartz 7, steel 4-5)",
            "Solids concentration (% by weight)",
            "Fluid velocity (lower = exponentially less wear)",
            "Chemical environment (corrosion + abrasion synergy)",
        ],
        primary_authority=[
            "ANSI/HI 12.1-12.6 Slurry Pump Nomenclature",
            "Warman Slurry Pump Handbook (Weir)",
            "ASTM A532 White Iron Castings",
        ],
        counter_arguments=[
            "Hard facing overlays (tungsten carbide) better than hard iron (cost 3-5×)",
            "Ceramic linings for extreme abrasion (alumina, silicon carbide - brittle, thermal shock)",
            "Hydrotreatment to reduce particle size upstream (process change vs pump upgrade)",
        ],
        resolution_strategy="Characterize slurry (size, hardness, %, pH) → select materials (hard iron vs rubber) → design impeller (open, semi-open) → reduce velocity → predict life.",
        entity_scope=["slurry pumps", "mining", "dredging", "wastewater", "oil sands"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ANSI/HI 12 series defines slurry pump design standards",
        fact_fragility_score=2.6,
    ),
]


# ═══════════════════════════════════════════════════════════════════════════════
# TELEMETRY & METRICS
# ═══════════════════════════════════════════════════════════════════════════════


class Telemetry:
    """Query telemetry and performance tracking"""

    def __init__(self):
        self.query_count = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.start_time = datetime.utcnow()
        self.latencies: List[float] = []
        self.error_count = 0

    def record_query(self, latency_ms: float, cache_hit: bool, error: bool = False):
        """Record query metrics"""
        self.query_count += 1
        self.latencies.append(latency_ms)
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        if error:
            self.error_count += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get telemetry statistics"""
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        cache_hit_rate = self.cache_hits / self.query_count if self.query_count > 0 else 0

        return {
            "total_queries": self.query_count,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate": round(cache_hit_rate, 3),
            "avg_latency_ms": round(avg_latency, 2),
            "error_count": self.error_count,
            "uptime_seconds": round(uptime, 1),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SEMANTIC NORMALIZATION
# ═══════════════════════════════════════════════════════════════════════════════


SEMANTIC_MAPPINGS = {
    # Pump types
    "centrifugal": ["radial", "volute", "end suction", "split case"],
    "positive displacement": ["PD", "reciprocating", "rotary", "plunger", "diaphragm", "gear"],
    "screw pump": ["twin screw", "triple screw", "archimedes screw"],

    # NPSH concepts
    "NPSH": ["net positive suction head", "suction head", "available NPSH", "required NPSH"],
    "cavitation": ["vapor bubbles", "bubble collapse", "suction cavitation", "implosion"],

    # Materials
    "stainless steel": ["SS", "316SS", "304SS", "austenitic"],
    "duplex": ["2205", "2507", "super duplex", "lean duplex"],
    "hard iron": ["white iron", "high chrome", "A532", "abrasion resistant"],

    # Performance
    "BEP": ["best efficiency point", "peak efficiency", "design point"],
    "specific speed": ["Ns", "type number", "impeller classification"],
    "affinity laws": ["similarity laws", "fan laws", "scaling laws"],
}


def normalize_term(term: str) -> str:
    """Normalize pump engineering terminology"""
    term_lower = term.lower().strip()
    for canonical, variants in SEMANTIC_MAPPINGS.items():
        if term_lower == canonical or term_lower in [v.lower() for v in variants]:
            return canonical
    return term_lower


# ═══════════════════════════════════════════════════════════════════════════════
# QUERY ENGINE
# ═══════════════════════════════════════════════════════════════════════════════


class MECH01Engine:
    """Industrial Pump Systems Intelligence Engine - TIE Gold Standard"""

    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.telemetry = Telemetry()
        self.audit_log = Path(__file__).parent / "logs" / "audit_trail.jsonl"
        self.audit_log.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"MECH01 Engine initialized with {len(self.doctrines)} doctrine blocks")

    def three_layer_response(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> QueryResponse:
        """
        Three-layer response architecture:
        1. Doctrine cache (0-200ms)
        2. Semantic retrieval (200-800ms) - simplified for now
        3. Deep analysis (800ms+) - expanded reasoning for DEFENSE/MEMO modes
        """
        start_time = datetime.utcnow()
        query_id = hashlib.sha256(f"{query}{start_time.isoformat()}".encode()).hexdigest()[:16]

        # Normalize query terms
        normalized_query = " ".join([normalize_term(word) for word in query.split()])

        # Layer 1: Doctrine cache lookup
        triggered = self._doctrine_cache_lookup(normalized_query)
        cache_hit = len(triggered) > 0

        # Layer 2 would be vector search (not implemented in this standalone engine)

        # Layer 3: Deep synthesis
        answer, reasoning_chain, warnings, fragility = self._synthesize_response(
            query, triggered, mode, zone
        )

        # Confidence stratification
        confidence = self._stratify_confidence(triggered, fragility, zone)

        # Determinism hash
        det_hash = self._determinism_hash(query, triggered, mode)

        # Record telemetry
        latency = (datetime.utcnow() - start_time).total_seconds() * 1000
        self.telemetry.record_query(latency, cache_hit)

        # Audit trail
        self._write_audit(query_id, query, mode, zone, triggered, confidence)

        response = QueryResponse(
            answer=answer,
            confidence=confidence,
            zone=zone,
            triggered_doctrines=[d.topic for d in triggered],
            reasoning_chain=reasoning_chain,
            epistemic_warnings=warnings,
            fact_fragility=fragility,
            determinism_hash=det_hash,
            query_id=query_id,
            timestamp=datetime.utcnow().isoformat(),
        )

        logger.info(
            f"Query {query_id} processed in {latency:.1f}ms | "
            f"Doctrines: {len(triggered)} | Confidence: {confidence.value}"
        )

        return response

    def _doctrine_cache_lookup(self, query: str) -> List[DoctrineBlock]:
        """Fast doctrine cache lookup by keyword matching"""
        triggered = []
        query_lower = query.lower()
        query_words = set(query_lower.split())

        for doctrine in self.doctrines:
            # Check keyword overlap
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)

            # Check topic match
            topic_words = set(doctrine.topic.lower().split())
            topic_overlap = len(query_words & topic_words)

            # Trigger if strong match
            if keyword_matches >= 2 or topic_overlap >= 2:
                triggered.append(doctrine)

        return triggered

    def _synthesize_response(
        self, query: str, doctrines: List[DoctrineBlock], mode: ResponseMode, zone: AnalysisZone
    ) -> Tuple[str, List[str], List[str], float]:
        """Synthesize answer from triggered doctrines"""
        if not doctrines:
            return (
                "No matching pump engineering expertise found. Please refine query with specific pump type, operating conditions, or technical concern.",
                ["No doctrine blocks triggered"],
                ["Query outside current expertise domain"],
                8.0,
            )

        # Sort by relevance (topic match, then keyword match)
        doctrines_sorted = sorted(
            doctrines,
            key=lambda d: (
                sum(1 for kw in d.keywords if kw.lower() in query.lower()),
                len(set(query.lower().split()) & set(d.topic.lower().split()))
            ),
            reverse=True
        )

        reasoning_chain = []
        warnings = []
        answer_parts = []

        # Mode-dependent depth
        if mode == ResponseMode.FAST:
            # Concise answer from top doctrine
            top = doctrines_sorted[0]
            answer_parts.append(f"**{top.topic}:**")
            answer_parts.extend([f"• {c}" for c in top.conclusion_template])
            reasoning_chain.append(f"Primary doctrine: {top.topic}")

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready answer with authority citations
            for doctrine in doctrines_sorted[:3]:
                answer_parts.append(f"\n**{doctrine.topic}:**")
                answer_parts.extend([f"• {c}" for c in doctrine.conclusion_template])
                answer_parts.append(f"\n*Authorities:* {'; '.join(doctrine.primary_authority)}")

                if doctrine.controlling_precedent:
                    answer_parts.append(f"*Controlling Precedent:* {doctrine.controlling_precedent}")

                reasoning_chain.append(f"Applied {doctrine.topic} with {len(doctrine.key_factors)} factors")

        else:  # MEMO mode
            # Full documentation with reasoning framework
            for doctrine in doctrines_sorted[:2]:
                answer_parts.append(f"\n{'='*60}")
                answer_parts.append(f"**{doctrine.topic.upper()}**\n")
                answer_parts.append("**Conclusion:**")
                answer_parts.extend([f"{i+1}. {c}" for i, c in enumerate(doctrine.conclusion_template)])

                answer_parts.append("\n**Technical Analysis:**")
                answer_parts.append(doctrine.reasoning_framework)

                answer_parts.append("\n**Key Factors:**")
                answer_parts.extend([f"• {f}" for f in doctrine.key_factors])

                answer_parts.append("\n**Authoritative Sources:**")
                answer_parts.extend([f"• {auth}" for auth in doctrine.primary_authority])

                if doctrine.counter_arguments:
                    answer_parts.append("\n**Alternative Approaches:**")
                    answer_parts.extend([f"• {arg}" for arg in doctrine.counter_arguments])

                answer_parts.append(f"\n**Resolution Strategy:** {doctrine.resolution_strategy}")

                reasoning_chain.append(f"Full analysis: {doctrine.topic} ({doctrine.confidence.value})")

        # Epistemic warnings
        for doctrine in doctrines_sorted:
            if doctrine.fact_fragility_score > 5.0:
                warnings.append(
                    f"High fact fragility ({doctrine.fact_fragility_score:.1f}/10) in {doctrine.topic}: "
                    "Verify site-specific conditions and manufacturer data."
                )
            if doctrine.confidence == ConfidenceLevel.DISCLOSURE:
                warnings.append(
                    f"{doctrine.topic} requires disclosure of assumptions and limitations to stakeholders."
                )

        # Zone-specific warnings
        if zone == AnalysisZone.AUDIT:
            warnings.append(
                "AUDIT ZONE: All conclusions subject to independent verification. "
                "Manufacturer certified data and field test results required."
            )

        avg_fragility = sum(d.fact_fragility_score for d in doctrines_sorted) / len(doctrines_sorted)

        answer = "\n".join(answer_parts)
        return answer, reasoning_chain, warnings, avg_fragility

    def _stratify_confidence(
        self, doctrines: List[DoctrineBlock], fragility: float, zone: AnalysisZone
    ) -> ConfidenceLevel:
        """Stratify confidence level based on doctrine quality and zone"""
        if not doctrines:
            return ConfidenceLevel.HIGH_RISK

        # Start with doctrine confidence levels
        confidence_scores = {
            ConfidenceLevel.DEFENSIBLE: 4,
            ConfidenceLevel.AGGRESSIVE: 3,
            ConfidenceLevel.DISCLOSURE: 2,
            ConfidenceLevel.HIGH_RISK: 1,
        }

        avg_score = sum(confidence_scores[d.confidence] for d in doctrines) / len(doctrines)

        # Adjust for fragility
        if fragility > 6.0:
            avg_score -= 1
        elif fragility < 3.0:
            avg_score += 0.5

        # Zone constraints
        if zone == AnalysisZone.AUDIT:
            avg_score = min(avg_score, 3)  # Cap at AGGRESSIVE for audit

        # Map back to confidence level
        if avg_score >= 3.5:
            return ConfidenceLevel.DEFENSIBLE
        elif avg_score >= 2.5:
            return ConfidenceLevel.AGGRESSIVE
        elif avg_score >= 1.5:
            return ConfidenceLevel.DISCLOSURE
        else:
            return ConfidenceLevel.HIGH_RISK

    def _determinism_hash(self, query: str, doctrines: List[DoctrineBlock], mode: ResponseMode) -> str:
        """Generate deterministic hash for reproducibility"""
        content = f"{query}|{mode.value}|" + "|".join(sorted([d.topic for d in doctrines]))
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _write_audit(
        self,
        query_id: str,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
        doctrines: List[DoctrineBlock],
        confidence: ConfidenceLevel,
    ):
        """Write audit trail entry"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query_id": query_id,
            "query": query,
            "mode": mode.value,
            "zone": zone.value,
            "doctrines_triggered": [d.topic for d in doctrines],
            "confidence": confidence.value,
        }

        with open(self.audit_log, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def health_check(self) -> HealthStatus:
        """Comprehensive health check"""
        stats = self.telemetry.get_stats()
        return HealthStatus(
            status="healthy",
            engine="MECH01_Industrial_Pump_Systems",
            version="1.0.0",
            port=9041,
            doctrines_loaded=len(self.doctrines),
            uptime_seconds=stats["uptime_seconds"],
            total_queries=stats["total_queries"],
            cache_hit_rate=stats["cache_hit_rate"],
        )


# ═══════════════════════════════════════════════════════════════════════════════
# FASTAPI SERVER
# ═══════════════════════════════════════════════════════════════════════════════


app = FastAPI(
    title="MECH01 - Industrial Pump Systems Engine",
    description="TIE Gold Standard - Mechanical Engineering expertise for centrifugal pumps, positive displacement pumps, NPSH, materials, seals, API standards",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = MECH01Engine()


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Query the pump engineering intelligence engine.

    Supports three response modes:
    - FAST: Concise conclusions (0-200ms)
    - DEFENSE: Audit-ready with citations (200-800ms)
    - MEMO: Full documentation with reasoning (800ms+)

    Three analysis zones:
    - PLANNING: Exploratory analysis
    - REPORTING: Stakeholder communication
    - AUDIT: Third-party verification
    """
    try:
        response = engine.three_layer_response(request.query, request.mode, request.zone)
        return response
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthStatus)
async def health_endpoint():
    """Health check with telemetry stats"""
    return engine.health_check()


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total": len(engine.doctrines),
        "topics": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "fragility": d.fact_fragility_score,
            }
            for d in engine.doctrines
        ],
    }


@app.get("/")
async def root():
    """Engine info"""
    return {
        "engine": "MECH01_Industrial_Pump_Systems",
        "version": "1.0.0",
        "port": 9041,
        "doctrines": len(engine.doctrines),
        "endpoints": ["/query", "/health", "/doctrines"],
        "domains": [
            "Centrifugal pump selection (specific speed, NPSH)",
            "Positive displacement pumps (reciprocating, rotary)",
            "Pump curve analysis and operating point",
            "Materials selection (316SS, duplex, hard iron)",
            "Mechanical seals (API 682 flush plans)",
            "Bearing selection and lubrication",
            "Vibration analysis and diagnostics",
            "API 610 centrifugal pump standard",
            "VFD energy savings analysis",
            "Multistage pump design",
            "Slurry pump abrasive wear",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting MECH01 Industrial Pump Systems Engine on port 9041")
    uvicorn.run(app, host="127.0.0.1", port=9041, log_level="info")
