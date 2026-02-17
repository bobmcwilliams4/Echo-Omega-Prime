"""
OFE05 - Artificial Lift Systems Engine
TIE Gold Standard - Oilfield Equipment Intelligence

Domain: Artificial lift method selection, design, troubleshooting, and optimization
Port: 9005
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass, field, asdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger


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


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class IssueCategory(str, Enum):
    LIFT_SELECTION = "LIFT_SELECTION"
    PUMP_DESIGN = "PUMP_DESIGN"
    ESP_ANALYSIS = "ESP_ANALYSIS"
    GAS_LIFT_DESIGN = "GAS_LIFT_DESIGN"
    DYNAMOMETER = "DYNAMOMETER"
    FAILURE_ANALYSIS = "FAILURE_ANALYSIS"
    OPTIMIZATION = "OPTIMIZATION"
    ROD_STRING = "ROD_STRING"
    EQUIPMENT_SPEC = "EQUIPMENT_SPEC"
    PERFORMANCE = "PERFORMANCE"
    TROUBLESHOOTING = "TROUBLESHOOTING"
    COMPLIANCE = "COMPLIANCE"


@dataclass
class DoctrineBlock:
    """Represents a compiled expert reasoning block for artificial lift systems."""
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    issue_category: IssueCategory
    disclosure_caveat: Optional[str] = None


class QueryRequest(BaseModel):
    query: str = Field(..., description="Artificial lift systems question or scenario")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis context zone")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional well/reservoir context")


class QueryResponse(BaseModel):
    query: str
    answer: str
    mode: ResponseMode
    zone: AnalysisZone
    confidence: ConfidenceLevel
    doctrines_triggered: List[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrine_count: int
    uptime_seconds: float
    queries_processed: int
    avg_latency_ms: float


# ============================================================================
# DOCTRINE CACHE - 25+ EXPERT BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Beam Pump Selection and Sizing",
        keywords=["rod pump", "beam pump", "sucker rod", "API 11E", "pumping unit", "displacement", "stroke length"],
        conclusion_template=[
            "Beam pump selection requires matching pumping unit geometry to well requirements.",
            "Key factors: production rate target, pump depth, fluid gravity, pumping speed.",
            "API 11E geometry calculations determine torque and load requirements."
        ],
        reasoning_framework="""
Beam pump (sucker rod pump) selection methodology:
1. Determine required pump displacement (BPD) based on reservoir IPR and tubing intake pressure
2. Calculate fluid load: (pump depth × fluid gradient) + dynamic fluid level effects
3. Select pumping unit size (geometry class from API 11E: C-320D-256-120 format)
   - First number = peak torque rating (thousand in-lbs)
   - Second = structure rating (hundred lbs)
   - Third = stroke length (inches)
4. Verify polished rod load does not exceed 90% of unit rating
5. Calculate pump displacement: PD = 0.1166 × D² × S × N × Ev
   - D = plunger diameter (inches)
   - S = stroke length (inches)
   - N = pumping speed (SPM)
   - Ev = volumetric efficiency (typically 0.70-0.85 for rod pumps)
6. Rod string design per API 11L to prevent buckling and fatigue
7. Counterbalance torque calculation to minimize peak loads
8. Prime mover sizing: brake horsepower = (fluid load × stroke × SPM) / (33000 × efficiency)

Critical design constraints:
- Maximum pumping speed: 20-24 SPM for deep wells, 30+ SPM for shallow
- Minimum stroke length for good efficiency: 64 inches+
- Rod stress safety factor: 0.5-0.6 on minimum load, avoid compressive buckling
- Tubing anchor required below pump to prevent tubing movement
- Gas anchor or separator needed if gas production >10% GLR
        """,
        key_factors=[
            "Pump depth and setting depth below perforations",
            "Fluid production rate (BPD) and reservoir pressure",
            "Fluid specific gravity (oil, water, gas content)",
            "Pumping unit geometry and load rating (API 11E)",
            "Rod string design and grade (API 11L)",
            "Volumetric efficiency and fillage",
            "Dynamometer analysis for optimization"
        ],
        primary_authority=[
            "API 11E: Specification for Pumping Units",
            "API 11L: Recommended Practice for Design Calculations for Sucker Rod Pumping Systems",
            "API RP 11BR: Care and Handling of Sucker Rods"
        ],
        burden_holder="Engineer",
        adversary_position="Undersized pump leads to poor fillage; oversized creates excessive loads",
        counter_arguments=[
            "Larger pump ensures capacity margin",
            "Smaller pump reduces operating costs",
            "Faster pumping speed increases wear",
            "Longer stroke improves efficiency but increases torque"
        ],
        resolution_strategy="Match pump size to IPR curve and optimize for minimum cost per barrel over equipment life",
        entity_scope="Oil and gas production wells requiring artificial lift",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in API design methods; medium in actual field performance prediction",
        controlling_precedent="API 11E and 11L are industry standard for rod pump design",
        issue_category=IssueCategory.PUMP_DESIGN
    ),

    DoctrineBlock(
        topic="Dynamometer Card Analysis",
        keywords=["dynamometer", "dynagraph", "surface card", "downhole card", "pump fillage", "wave equation"],
        conclusion_template=[
            "Dynamometer cards reveal pump performance and mechanical issues.",
            "Surface card is actual; downhole card is calculated via wave equation.",
            "Card shape diagnoses gas lock, fluid pound, tubing movement, valve leaks."
        ],
        reasoning_framework="""
Dynamometer analysis process:
1. Surface card acquisition: Load vs. position at polished rod (real-time or memory card)
2. Downhole card calculation using wave equation analysis:
   - Input: surface card + rod string data + pumping speed
   - Wave equation models elastic rod behavior and damping
   - Output: predicted load and position at pump plunger
3. Card shape interpretation:
   - Full fillage: Parallelogram shape with flat top/bottom
   - Gas interference: Tapered top, reduced area
   - Fluid pound: Sharp peaks at top and bottom (pump hitting stops)
   - Traveling valve leak: Loop at top right
   - Standing valve leak: Loop at bottom left
   - Tubing movement: Shifted baseline or tilted card
   - Anchored rod: Excessive stretch, high peak loads
4. Calculate pump fillage (volumetric efficiency):
   - Ev = (actual card area) / (theoretical full card area)
   - Typical values: 0.70-0.85 good, <0.60 poor fillage
5. Identify optimization opportunities:
   - Adjust pumping speed to reduce fluid pound
   - Increase stroke length to improve efficiency
   - Repair leaking valves if indicated
   - Install gas separator if gas interference present
6. Load analysis:
   - Peak polished rod load (max upstroke)
   - Minimum polished rod load (should be positive to avoid compression)
   - Counterbalance adjustment to balance loads
        """,
        key_factors=[
            "Surface card shape and area",
            "Downhole calculated card accuracy",
            "Pump fillage percentage",
            "Gas lock or interference indications",
            "Fluid pound frequency",
            "Valve leak signatures",
            "Rod stress and fatigue limits"
        ],
        primary_authority=[
            "API RP 11G: Recommended Practice for Installation and Luffing Procedure for Sucker Rod Pumps",
            "Dynamometer card interpretation guides (Lufkin, Weatherford)",
            "Wave equation analysis software validation"
        ],
        burden_holder="Production Engineer",
        adversary_position="Misinterpretation of card shape leads to wrong corrective action",
        counter_arguments=[
            "Card looks normal but production is low",
            "Multiple issues create overlapping signatures",
            "Wave equation assumptions may not match actual rod behavior",
            "Gas slugging creates intermittent abnormal cards"
        ],
        resolution_strategy="Combine card analysis with well test data and equipment inspection to confirm diagnosis",
        entity_scope="Rod pumping wells with dynamometer monitoring",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in card shape diagnosis; medium in wave equation accuracy for deep wells",
        controlling_precedent="Dynamometer analysis is standard practice per API RP 11G",
        issue_category=IssueCategory.DYNAMOMETER
    ),

    DoctrineBlock(
        topic="ESP Selection and Sizing",
        keywords=["ESP", "electric submersible pump", "centrifugal pump", "pump curve", "stages", "head", "BHP"],
        conclusion_template=[
            "ESP selection matches pump performance curve to well IPR and required lift.",
            "Critical factors: total dynamic head (TDH), production rate, motor horsepower.",
            "Stage count adjusts head capacity; pump size determines rate capacity."
        ],
        reasoning_framework="""
ESP (Electrical Submersible Pump) sizing methodology:
1. Determine well requirements:
   - Production rate target (BPD or B/D)
   - Pump setting depth (feet TVD)
   - Pumping fluid level (PFL) below surface
   - Reservoir IPR curve (pressure vs. rate relationship)
   - Fluid properties: SG, viscosity, temperature, %water, %gas
2. Calculate Total Dynamic Head (TDH):
   TDH = (Discharge pressure / 0.433 / SG) + Pump setting depth - Pumping fluid level + Friction losses
   - Discharge pressure typically 50-200 psi for surface facilities
   - SG = specific gravity of produced fluid (weighted average of oil/water)
   - Friction losses calculated from tubing size and flow rate (Hazen-Williams or Moody)
3. Select pump series (size) based on production rate:
   - Series 338: 50-500 BPD (2.88" OD housing, 4.5" casing)
   - Series 400: 200-1500 BPD (3.62" OD, 5.5" casing)
   - Series 538: 500-5000 BPD (4.56" OD, 7" casing)
   - Series 675: 2000-15000 BPD (5.75" OD, 8.625" casing)
4. Determine stage count from manufacturer pump curve:
   - Each stage adds ~10-25 ft of head (varies by series and rate)
   - Total stages = TDH / (head per stage at desired rate)
   - Typical range: 50-400 stages
5. Motor horsepower calculation:
   BHP = (Rate × TDH × SG) / (3960 × pump efficiency)
   - Pump efficiency from curve (typically 55-75% at best efficiency point)
   - Add 20-30% safety margin for motor selection
6. Cable sizing: voltage drop <30V per 1000 ft, ampacity for motor load + safety margin
7. Gas handling: free gas at pump intake should be <10-15% by volume
   - Use gas separator if higher GLR
   - Shroud or rotary gas separator for high-gas wells
8. VFD (Variable Frequency Drive) sizing if speed control desired:
   - Allows pump curve shifting by adjusting frequency (30-70 Hz typical range)
   - Enables optimization as reservoir declines
        """,
        key_factors=[
            "Total dynamic head (TDH) requirements",
            "Production rate and pump curve match",
            "Motor horsepower and voltage",
            "Cable size and voltage drop",
            "Gas handling at pump intake",
            "Pump efficiency at operating point",
            "ESP run life and reliability history"
        ],
        primary_authority=[
            "ESP manufacturer design software (Centrilift, REDA, Summit, Baker Hughes)",
            "API RP 11S7: Recommended Practice for Application, Installation, and Operation of Electric Submersible Pump Systems",
            "Petroleum Production Systems textbook (Guo, Lyons, Ghalambor)"
        ],
        burden_holder="Completion/Production Engineer",
        adversary_position="Undersized ESP cannot lift required rate; oversized ESP runs inefficiently and wastes power",
        counter_arguments=[
            "Larger ESP provides reserve capacity",
            "Smaller ESP reduces capital cost",
            "High stage count increases mechanical complexity",
            "VFD adds cost but enables flexibility"
        ],
        resolution_strategy="Select ESP at or near best efficiency point (BEP) on pump curve for target rate and TDH",
        entity_scope="Wells requiring high-volume artificial lift, especially horizontal or high-water-cut wells",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in design calculations; medium in predicting actual run life",
        controlling_precedent="API RP 11S7 and manufacturer design standards",
        issue_category=IssueCategory.ESP_ANALYSIS
    ),

    DoctrineBlock(
        topic="ESP Failure Analysis",
        keywords=["ESP failure", "motor burn", "bearing wear", "cable fault", "run life", "teardown"],
        conclusion_template=[
            "ESP failures result from mechanical, electrical, or operational causes.",
            "Common modes: motor overheating, bearing wear, cable insulation breakdown, scaling/corrosion.",
            "Teardown analysis identifies root cause and guides design changes."
        ],
        reasoning_framework="""
ESP failure analysis process:
1. Operational data review before failure:
   - Motor temperature trend (from downhole sensor if equipped)
   - Motor current and voltage (from VFD or surface panel)
   - Production rate and fluid level trend
   - Vibration or unusual noise reports
2. Teardown inspection by manufacturer or third party:
   - Motor: winding insulation breakdown, bearing condition, shaft wear
   - Pump: stage wear (diffusers, impellers), shaft/sleeve wear, scale/corrosion deposits
   - Seal section (protector): oil condition, seal integrity, pressure equalization
   - Cable: insulation breakdown location, armor damage, connector integrity
3. Common failure modes and root causes:

   MOTOR FAILURES:
   - Overheating: Low flow past motor (rate too low), high fluid temperature, inadequate shroud
   - Winding failure: Voltage imbalance, voltage spikes, contaminated motor oil
   - Bearing wear: Thrust imbalance, solids production, insufficient lubrication

   PUMP FAILURES:
   - Abrasive wear: Sand production, need for abrasion-resistant metallurgy or coating
   - Corrosion: H2S, CO2, produced water chemistry, need for corrosion inhibitor or upgraded materials
   - Gas lock: Free gas at intake >15%, need for gas separator
   - Scale buildup: CaCO3, BaSO4 deposition, need for scale inhibitor

   CABLE FAILURES:
   - Insulation breakdown: Mechanical damage during run, chemical attack, voltage stress
   - Armor corrosion: Produced fluid attack, need for protected cable design
   - Connector failure: Improper makeup, moisture intrusion

   OPERATIONAL FAILURES:
   - Off-design operation: Running far from BEP, cycling on/off frequently
   - Voltage issues: Undervoltage, overvoltage, phase imbalance >2%
   - Solid production: Need for sand control or desander ahead of pump

4. Corrective actions based on diagnosis:
   - Metallurgy upgrade: Ni-resist for abrasion, duplex stainless for H2S
   - Gas handling: Add separator, increase shroud flow, reduce rate
   - Operational: Adjust rate to BEP, improve voltage quality, add filters
   - Chemical: Scale/corrosion inhibitor program
   - Design: Change pump series, reduce stages, upgrade motor HP
        """,
        key_factors=[
            "Run life compared to field average",
            "Failure mode (motor, pump, cable, seal)",
            "Operational conditions at failure",
            "Teardown findings and root cause",
            "Wellbore environment (temp, pressure, fluids, solids)",
            "Voltage and power quality",
            "Previous failure history and patterns"
        ],
        primary_authority=[
            "ESP manufacturer teardown reports and guidelines",
            "API RP 11S7 failure analysis section",
            "Industry failure databases (operators, service companies)"
        ],
        burden_holder="Production/Completion Engineer and Service Company",
        adversary_position="Multiple contributing factors make single root cause unclear",
        counter_arguments=[
            "Failure was random, not systematic",
            "Well conditions are inherently harsh and unavoidable",
            "Cost of upgrade outweighs run life improvement",
            "Teardown may not reveal early-stage degradation causes"
        ],
        resolution_strategy="Systematic teardown analysis plus operational data review to identify correctable root causes",
        entity_scope="All ESP installations with reliability concerns",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in physical failure mode; medium in linking to specific operational cause",
        controlling_precedent="Teardown analysis per manufacturer protocols",
        issue_category=IssueCategory.FAILURE_ANALYSIS
    ),

    DoctrineBlock(
        topic="Gas Lift Valve Spacing and Design",
        keywords=["gas lift", "valve spacing", "injection pressure", "gradient curve", "unloading", "operating valve"],
        conclusion_template=[
            "Gas lift valve spacing determines unloading sequence and operating depth.",
            "Design balances injection gas pressure, well gradient, and valve performance.",
            "Proper spacing ensures sequential valve opening and stable operation."
        ],
        reasoning_framework="""
Gas lift valve spacing design methodology:
1. Well data requirements:
   - Tubing size and setting depth
   - Reservoir IPR curve (pressure vs. gas-free production rate)
   - Available injection gas pressure and rate
   - Fluid gradient (oil/water mixture specific gravity)
   - Static and flowing bottomhole pressures
2. Operating point selection:
   - Injection depth: deepest point gas can be injected effectively
   - Operating gas injection rate (Mscf/D)
   - Target liquid production rate (BPD)
3. Gradient curves (pressure vs. depth):
   - Static fluid gradient (before gas injection)
   - Flowing gradient at various GLRs (gas-liquid ratios)
   - Gas injection pressure curve (available pressure minus surface friction)
4. Unloading valve spacing calculation:
   - Start at surface casing pressure point
   - Space valves to sequentially open as fluid level falls
   - Each valve operates until next deeper valve opens
   - Typical spacing: 500-1000 ft intervals for deep wells, closer for shallow
   - Pressure differential at each valve:
     ΔP = (Injection pressure) - (Tubing pressure at valve depth)
   - Each valve must have sufficient ΔP to open (typically 50-100 psi)
5. Operating valve selection:
   - Located at or slightly above target injection depth
   - Sized to pass required gas rate at available ΔP
   - Valve performance curves: gas rate vs. ΔP for given port size
   - Typical orifice sizes: 1/4", 3/8", 1/2", 3/4", 1"
6. Valve types:
   - Unloading valves (PPO = Pressure-Operated, nitrogen-charged dome)
   - Operating valve (orifice check valve or throttling valve)
   - Fluid-operated valves for deep/high-pressure wells
7. Design verification:
   - Gradient analysis: confirm valves space correctly on pressure-depth plot
   - Unloading simulation: ensure each valve opens in sequence
   - Operating stability: verify operating valve does not cycle/flutter
        """,
        key_factors=[
            "Injection gas pressure available at surface",
            "Well depth and tubing size",
            "Target production rate and injection GLR",
            "Fluid gradient (oil/water SG)",
            "Valve spacing intervals",
            "Unloading vs. operating valve design",
            "Valve performance curves (Cv, orifice size)"
        ],
        primary_authority=[
            "API RP 11V6: Design of Continuous Flow Gas Lift Installations Using Injection-Pressure-Operated Valves",
            "Gas lift design software (Prosper, WellFlo, Autographs)",
            "Valve manufacturer catalogs (Camco, Weatherford)"
        ],
        burden_holder="Production/Reservoir Engineer",
        adversary_position="Improper spacing causes valves to interfere or fail to unload sequentially",
        counter_arguments=[
            "Closer spacing provides more control but increases cost",
            "Deeper injection improves efficiency but requires higher pressure",
            "Larger orifice passes more gas but may cycle unstable",
            "Smaller orifice provides stable operation but limits capacity"
        ],
        resolution_strategy="Use gradient analysis software to optimize spacing for available pressure and target rate",
        entity_scope="Wells with sufficient injection gas pressure and moderate to high productivity",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in spacing calculations; medium in actual valve performance prediction",
        controlling_precedent="API RP 11V6 valve spacing methodology",
        issue_category=IssueCategory.GAS_LIFT_DESIGN
    ),

    DoctrineBlock(
        topic="Progressive Cavity Pump (PCP) Applications",
        keywords=["PCP", "progressive cavity", "Moineau pump", "screw pump", "elastomer", "viscous oil", "heavy oil"],
        conclusion_template=[
            "PCP (progressive cavity pump) is ideal for high-viscosity, solids-laden fluids.",
            "Rotor-stator interference fit creates progressive cavities that move fluid.",
            "Elastomer selection critical for fluid compatibility and temperature."
        ],
        reasoning_framework="""
PCP (Progressive Cavity Pump) design and application:
1. Operating principle:
   - Single helical rotor rotates inside double helical stator (elastomer)
   - Interference fit creates sealed cavities that progress from suction to discharge
   - Positive displacement action: flow rate proportional to rotor RPM
   - Self-priming and can handle high gas content (up to 80% free gas)
2. Applications where PCP excels:
   - High-viscosity fluids: heavy oil (>100 cp), cold production, bitumen
   - Solids production: sand, fines up to 10% by volume
   - High water cut: up to 100% water
   - Corrosive fluids: H2S, CO2 with proper elastomer selection
   - Low to moderate rates: 50-3000 BPD typical
   - Deviated and horizontal wells: handles gas and solids better than ESP
3. Design parameters:
   - Pump geometry: rotor diameter, eccentricity, pitch length, stages
   - Displacement per revolution: function of geometry (typically 0.1-2.0 gallons/rev)
   - Operating speed: 100-500 RPM typical (higher speed reduces size but increases wear)
   - Lift capacity: head per stage × number of stages
     Typical head per stage: 50-100 psi (varies with elastomer fit)
   - Production rate: Q (BPD) = Displacement (gal/rev) × RPM × Volumetric efficiency × 34.3
     Volumetric efficiency: 0.75-0.95 depending on wear and gas content
4. Elastomer selection (critical for run life):
   - Nitrile (Buna-N): General purpose, oil/water, <180°F, low cost
   - HNBR (Hydrogenated Nitrile): Higher temp to 250°F, better abrasion resistance
   - Viton (Fluoroelastomer): Aromatics, solvents, high temp to 300°F, expensive
   - Aflas: Extreme temp/chemicals, 350°F+, very expensive
   - Fit selection: Standard, medium, or tight fit (tighter fit = higher head but faster wear)
5. Drive systems:
   - Surface drive: electric motor or engine, sheave/belt or gearbox to polished rod
   - Hydraulic drive: surface hydraulic power unit, downhole hydraulic motor
   - Direct drive: downhole electric motor (less common)
6. Typical failure modes:
   - Stator elastomer wear: abrasion from solids, chemical attack, heat degradation
   - Rotor wear: hard coatings help with solids
   - Tubing wear: rotor/tubing contact in deviated wells
   - Rod string failures: torque and tension reversals
   - Drive system failures: belt slippage, gearbox wear
7. Advantages over other lift methods:
   - Handles high viscosity (beam pump struggles >50 cp)
   - Tolerates solids (ESP fails quickly with sand)
   - Efficient at low rates (gas lift requires minimum rate)
   - Simple surface equipment (vs. ESP cable/VFD complexity)
8. Disadvantages:
   - Limited temperature (<250°F for most elastomers)
   - Limited lift (<3000 ft typical, up to 6000 ft with multiple stages)
   - Elastomer wear requires periodic replacement (1-3 year run life typical)
   - Not economical for high-rate wells (>3000 BPD)
        """,
        key_factors=[
            "Fluid viscosity and temperature",
            "Solids content and particle size",
            "Production rate and lift requirement",
            "Elastomer compatibility with produced fluids",
            "Operating speed and wear rate trade-off",
            "Run life and replacement cost economics",
            "Wellbore deviation and torque capacity"
        ],
        primary_authority=[
            "PCP manufacturer design guides (Schlumberger, Weatherford, NOV)",
            "API RP 11S1: Progressing Cavity Pump Systems",
            "SPE papers on PCP performance and elastomer selection"
        ],
        burden_holder="Production Engineer",
        adversary_position="PCP is only solution for some heavy oil wells, but run life and maintenance costs are concerns",
        counter_arguments=[
            "ESP can handle viscosity with special stages",
            "Beam pump cheaper for low-rate shallow wells",
            "Hydraulic jet pump avoids elastomer wear issue",
            "Elastomer degradation is unpredictable"
        ],
        resolution_strategy="Use PCP where fluid properties (viscosity, solids, gas) exceed capability of ESP or rod pump",
        entity_scope="Heavy oil, high-solids, or high-gas wells with moderate lift and rate",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in application suitability; medium in elastomer run life prediction",
        controlling_precedent="PCP is standard artificial lift for heavy oil and solids production per API RP 11S1",
        issue_category=IssueCategory.PUMP_DESIGN
    ),

    DoctrineBlock(
        topic="Plunger Lift Systems",
        keywords=["plunger lift", "gas assist", "free piston", "cycle time", "arrival sensor", "slug flow"],
        conclusion_template=[
            "Plunger lift uses reservoir gas energy to lift liquid slugs.",
            "Free-traveling plunger creates interface between gas and liquid.",
            "Cycle optimization balances buildUp time, afterflow, and arrival speed."
        ],
        reasoning_framework="""
Plunger lift design and operation:
1. Operating principle:
   - Well shut in to build casing pressure and liquid accumulation
   - Plunger dropped or falls to bottom, seals tubing/casing annulus
   - Well opened, gas pressure lifts plunger and liquid slug to surface
   - Plunger caught at surface, liquid unloaded, cycle repeats
   - Mechanical interface between gas and liquid prevents gas bypass
2. Candidate well requirements:
   - Sufficient reservoir gas energy: GLR >400 scf/bbl minimum, >800 ideal
   - Adequate shut-in pressure build: need 50-100 psi per 1000 ft of lift
   - Liquid production rate: 10-300 BPD typical (too high for plunger efficiency)
   - Tubing size: 2-3/8" to 3-1/2" most common (larger tubing harder to seal)
   - Reasonably vertical well: <30° deviation (plunger may not fall in deviated wells)
3. Plunger types:
   - Conventional (brush) plunger: spring-loaded sealing elements, standard design
   - Pad plunger: polymer pads for sealing, handles light solids
   - Turbulent flow plunger: slots/ports reduce fall speed, gentler arrival
   - Two-piece plunger: articulated for deviated wells
4. Cycle optimization:
   - Shut-in time (build time): allow casing pressure and liquid level to rise
     Too short: insufficient pressure to lift plunger
     Too long: excessive gas compression, reduced cycles/day
   - Afterflow time: keep well open after plunger arrival to unload gas
     Too short: gas trapped, reduces pressure drawdown
     Too long: liquid fallback, wasted cycle
   - Cycle frequency: 4-24 cycles per day typical
     Optimization: maximize daily production = (liquid per cycle) × (cycles per day)
5. Surface equipment:
   - Motor valve or plunger controller: automated cycle control
   - Arrival sensor: optical or magnetic, detects plunger at surface
   - Lubricator: captures plunger, allows liquid to flow to sales line
   - Catcher: mechanical device to hold plunger at surface
6. Downhole equipment:
   - Bumper spring: cushions plunger arrival at bottom
   - Bottom-hole assembly: seating nipple, stop, debris barrier
   - Tubing anchor/catcher: prevent tubing movement
7. Optimization strategies:
   - Time-based control: fixed shut-in and afterflow times
   - Pressure-based control: open at target casing pressure
   - Differential pressure control: monitor tubing-casing ΔP
   - Adaptive control: adjust cycle based on plunger velocity and load
8. Troubleshooting common issues:
   - Plunger not arriving: insufficient gas pressure, plunger stuck, liquid fallback
   - Slow plunger rise: low pressure, gas bypass around plunger, tubing debris
   - Short cycles: inadequate shut-in time, liquid influx rate too high
   - Liquid carry-over: afterflow too short, separator issues
        """,
        key_factors=[
            "Gas-liquid ratio (GLR) and reservoir pressure",
            "Liquid production rate and accumulation",
            "Shut-in pressure build rate",
            "Plunger type and sealing effectiveness",
            "Cycle time optimization (shut-in, afterflow)",
            "Arrival velocity and bottom impact",
            "Wellbore deviation and plunger fall"
        ],
        primary_authority=[
            "API RP 11V1: Recommended Practice on the Application of Subsurface Pumps",
            "Plunger lift controller manufacturer guides",
            "SPE papers on plunger lift optimization (Ferguson, Lea)"
        ],
        burden_holder="Production Engineer and Operations",
        adversary_position="Plunger lift is low-cost but only works for specific well conditions",
        counter_arguments=[
            "Insufficient GLR for plunger to lift reliably",
            "Rate too high for intermittent lift method",
            "Deviated wellbore prevents plunger fall",
            "Solids production plugs plunger or tubing"
        ],
        resolution_strategy="Use plunger lift as low-cost solution for gas wells with liquid loading, optimize cycles with controller",
        entity_scope="Gas wells with liquid loading, stripper oil wells with high GLR",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in candidate screening; medium in cycle optimization and reliability",
        controlling_precedent="Plunger lift standard practice per API RP 11V1",
        issue_category=IssueCategory.LIFT_SELECTION
    ),

    DoctrineBlock(
        topic="Hydraulic Jet Pump Systems",
        keywords=["jet pump", "hydraulic pump", "power fluid", "venturi", "nozzle throat", "cavitation"],
        conclusion_template=[
            "Hydraulic jet pump uses high-pressure power fluid to entrain and lift produced fluids.",
            "No moving parts downhole: nozzle, throat, and diffuser create momentum transfer.",
            "Ideal for sandy, corrosive, or high-temperature wells."
        ],
        reasoning_framework="""
Hydraulic jet pump design and application:
1. Operating principle:
   - Surface power fluid pump generates high-pressure clean fluid (1500-5000 psi)
   - Power fluid pumped down tubing or casing to jet pump assembly
   - High-velocity jet through nozzle creates low pressure (venturi effect)
   - Produced fluid entrained in throat section via momentum transfer
   - Mixed fluid returned to surface through annulus or separate return string
   - Power fluid separated and recirculated; produced fluid to sales/disposal
2. Jet pump assembly components:
   - Nozzle: converts power fluid pressure to kinetic energy (velocity)
   - Throat (mixing tube): produced fluid entrained and mixed with power fluid
   - Diffuser: converts velocity back to pressure for lift
   - No valves, no moving parts downhole
3. Design parameters and calculations:
   - Nozzle-throat area ratio (N/T ratio): key design parameter
     Typical range: 0.10 to 0.40
     Lower ratio: higher produced fluid ratio, lower efficiency
     Higher ratio: lower produced fluid ratio, higher efficiency
   - Cavitation number: ensure adequate pressure to avoid cavitation damage
     Must maintain positive pressure at throat entrance
   - M ratio (produced fluid rate / power fluid rate):
     Function of N/T ratio, power fluid pressure, lift depth, fluid properties
     Typical M ratio: 0.3 to 1.5 (M=1 means equal volumes power and produced fluid)
   - Efficiency: mechanical efficiency typically 20-40% (lower than rod pump or ESP)
     Offset by ability to handle difficult fluids and no downhole moving parts
4. Power fluid options:
   - Produced crude oil: if clean enough, reduces separation cost
   - Produced water: if non-corrosive and clean
   - Fresh water: if produced fluids not suitable for recirculation
   - Selection based on compatibility, cleanliness, availability
5. Surface equipment:
   - Triplex or quintuplex power fluid pump: high-pressure positive displacement
   - Power fluid treating: filtration, chemical treatment, deaeration
   - Separator: three-phase separation of power fluid, oil, water, gas
   - Power fluid tank and recirculation system
6. Applications where jet pump excels:
   - High sand production: no valves or close clearances to plug
   - Corrosive fluids: H2S, CO2, chlorides (use corrosion-resistant materials)
   - High temperature: no elastomers, no motor cooling issues (350°F+)
   - Scaling fluids: can run with mild scale buildup, easy to pull and clean
   - Intermittent production: can shut in and restart easily
   - Limited wellhead space: surface pump can be located away from well
7. Disadvantages:
   - Low mechanical efficiency: high operating cost (power)
   - Requires clean power fluid: filtration and treating costs
   - Pressure losses in long surface lines: limits application distance
   - Cavitation damage if improperly designed
   - Surface equipment complexity: pump, separator, treating
8. Optimization:
   - N/T ratio selection: balance production rate vs. efficiency
   - Power fluid pressure: optimize for maximum production at minimum cost
   - Free pump insert service: can change N/T ratio by pulling insert, no workover
        """,
        key_factors=[
            "Sand/solids production severity",
            "Corrosion and scaling potential",
            "Bottomhole temperature",
            "Production rate and lift requirement",
            "Power fluid availability and quality",
            "Nozzle-throat ratio optimization",
            "Operating cost vs. capital cost trade-off"
        ],
        primary_authority=[
            "API RP 11U1: Hydraulic Pumping for Oil Wells – Jet Pumping",
            "Jet pump manufacturer design software",
            "SPE papers on jet pump performance"
        ],
        burden_holder="Production Engineer",
        adversary_position="Jet pump has low efficiency but may be only viable solution for extreme conditions",
        counter_arguments=[
            "High operating cost due to low efficiency",
            "Complex surface facilities vs. simple rod pump",
            "Cavitation risk if poorly designed",
            "Power fluid treating costs can be high"
        ],
        resolution_strategy="Use jet pump where solids, temperature, or corrosion preclude other methods; optimize N/T ratio",
        entity_scope="Wells with sand, high temp, or corrosive conditions beyond capability of rod pump/ESP/PCP",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in application suitability; medium in performance and efficiency prediction",
        controlling_precedent="Hydraulic jet pump per API RP 11U1",
        issue_category=IssueCategory.PUMP_DESIGN
    ),

    DoctrineBlock(
        topic="Rod String Design and API 11L",
        keywords=["sucker rod", "rod string", "API 11L", "tapered string", "rod grade", "fatigue", "buckling"],
        conclusion_template=[
            "Rod string design per API 11L prevents buckling, fatigue, and excessive stress.",
            "Tapered strings optimize weight and strength: heavier rods at top, lighter at bottom.",
            "Safety factors: 0.5-0.6 on minimum load, <0.85 on maximum stress."
        ],
        reasoning_framework="""
Sucker rod string design methodology per API 11L:
1. Design inputs:
   - Pumping unit: peak polished rod load (PRL), stroke length
   - Pump: setting depth, plunger diameter, pump displacement
   - Fluid: specific gravity, production rate
   - Operating conditions: pumping speed (SPM), environment (H2S, CO2)
2. Rod grades and materials:
   - API Grade D: 90,000 psi tensile strength (most common, lower cost)
   - API Grade K: 115,000 psi (higher strength, used in deeper wells)
   - API Grade C: 60,000 psi (legacy, rarely used)
   - Fiberglass rods: lower weight, corrosion resistant, used in corrosive or deep wells
   - Rod sizes: 1/2", 5/8", 3/4", 7/8", 1" diameter (3/4" and 7/8" most common)
3. String design options:
   - All one size (uniform string): simple but not optimized
   - Two or three size taper: heavier rods at top to carry load, lighter at bottom
     Example: 1000 ft of 7/8" + 2000 ft of 3/4" + 2000 ft of 5/8"
   - Continuous taper: gradual size reduction (less common)
4. Load calculations:
   - Static rod weight: sum of rod weight from each section
   - Fluid load on plunger: (0.433 psi/ft × fluid SG × pump depth) × plunger area
   - Dynamic loads: acceleration effects from pumping speed and stroke
     Peak polished rod load (max upstroke): static + fluid + acceleration + friction
     Minimum polished rod load (max downstroke): static - acceleration - friction
5. Stress analysis:
   - Tensile stress: Load / rod cross-sectional area
   - Safety factor on minimum load: must be >0.5 to avoid compression buckling
     Buckling occurs if minimum load goes negative (rod in compression)
   - Safety factor on maximum stress: <0.85 of rod grade tensile strength
     Lower stress extends fatigue life
6. Fatigue analysis:
   - Stress reversals cause fatigue cracks at rod couplings
   - Modified Goodman diagram: relates mean stress and alternating stress to fatigue life
   - Target service factor >1.0 for acceptable fatigue life
   - Corrosive environments (H2S, CO2) reduce fatigue life, require higher safety factors
7. Rod string optimization:
   - Minimize weight to reduce loads and power requirements
   - Use tapered string to put stronger rods where stress is highest
   - Consider fiberglass rods for top section (lowest stress, corrosion environment)
   - Avoid compression buckling by ensuring minimum load stays positive
8. Couplings and connections:
   - API 8 round threads (most common), API 5 square threads (legacy)
   - Slim-hole (SH) couplings for small casing clearance
   - Stress concentration at coupling: failure initiates here
   - Proper torque critical: undertorqued causes backing out, overtorqued causes damage
        """,
        key_factors=[
            "Pump setting depth and fluid load",
            "Polished rod load limits (peak and minimum)",
            "Rod grade and size selection",
            "Tapered string configuration",
            "Stress safety factors (max <0.85, min >0.5)",
            "Fatigue life and service factor",
            "Corrosive environment derating"
        ],
        primary_authority=[
            "API RP 11L: Design Calculations for Sucker Rod Pumping Systems",
            "API Spec 11B: Specification for Sucker Rods",
            "Rod string design software (API RP 11L compliant)"
        ],
        burden_holder="Production/Completions Engineer",
        adversary_position="Underdesigned rod string fails in service; overdesigned wastes cost and power",
        counter_arguments=[
            "All one size is simpler inventory but less optimized",
            "Higher grade rods cost more but allow deeper wells",
            "Fiberglass rods solve corrosion but have lower tensile strength",
            "Conservative design reduces failures but increases cost"
        ],
        resolution_strategy="Use API 11L design software to optimize tapered string for minimum cost meeting safety factors",
        entity_scope="All beam pump installations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in API 11L design methods; medium in actual fatigue life prediction",
        controlling_precedent="API RP 11L is industry standard for rod string design",
        issue_category=IssueCategory.ROD_STRING
    ),

    DoctrineBlock(
        topic="VFD (Variable Frequency Drive) for ESP",
        keywords=["VFD", "variable frequency drive", "ESP speed control", "soft start", "frequency", "motor protection"],
        conclusion_template=[
            "VFD enables ESP speed control by varying motor frequency (30-70 Hz).",
            "Benefits: soft start, rate optimization, motor protection, power factor correction.",
            "Allows ESP to adapt to reservoir decline without pulling and replacing pump."
        ],
        reasoning_framework="""
VFD (Variable Frequency Drive) application for ESP:
1. Operating principle:
   - VFD converts fixed-frequency AC power (60 Hz) to variable-frequency output (30-70 Hz typical)
   - ESP motor speed proportional to frequency: 3600 RPM at 60 Hz, 1800 RPM at 30 Hz (for 2-pole motor)
   - Pump performance curves scale with speed:
     Q₂/Q₁ = N₂/N₁ (flow scales linearly with speed)
     H₂/H₁ = (N₂/N₁)² (head scales with speed squared)
     BHP₂/BHP₁ = (N₂/N₁)³ (power scales with speed cubed)
2. Key benefits:
   - Soft start: ramp up frequency gradually to reduce inrush current and mechanical shock
     Extends motor and pump life vs. across-the-line starting
   - Production optimization: adjust speed to match reservoir as it declines
     Can reduce frequency as pressure drops rather than pulling pump
   - Energy savings: reduce speed = cubic reduction in power (if rate can be reduced)
   - Motor protection: VFD monitors current, voltage, temperature, shuts down on fault
   - Power factor correction: VFD improves power factor, reduces utility demand charges
3. VFD selection and sizing:
   - Voltage rating: match ESP system voltage (480V, 1000V, 4160V common)
   - Current rating: 1.15-1.25× motor nameplate FLA (full load amps)
   - Enclosure: NEMA 1 indoor, NEMA 3R/4/4X outdoor or hazardous location
   - Control interface: local keypad, SCADA integration, automation
4. Operating range:
   - Minimum frequency: typically 30-40 Hz (below this, motor cooling inadequate)
   - Maximum frequency: typically 60-70 Hz (above 60 Hz may exceed pump mechanical limits)
   - Optimal range: 45-60 Hz for most applications
5. Installation considerations:
   - Power cable: VFD output has harmonic content, may need VFD-rated cable
   - Cable length limits: VFD-cable-motor interaction can cause voltage reflections
     Use dV/dt filters or cable reactors if cable >5000 ft
   - Step-up transformer: if VFD output voltage < ESP system voltage
     Example: 480V VFD + transformer to 1000V for ESP motor
   - Harmonic filters: reduce harmonics back to utility grid (may be required by utility)
6. Operational best practices:
   - Gradual speed changes: ramp 1-2 Hz per minute to avoid water hammer or gas lock
   - Avoid frequent starts: each start adds thermal and mechanical stress
   - Monitor motor temperature and vibration: early warning of issues
   - Maintain speed within design range: don't operate near minimum or maximum continuously
7. Common issues and solutions:
   - Nuisance trips: overvoltage, undervoltage, overcurrent due to transients
     Solution: Adjust trip setpoints, add filters, check power quality
   - Motor overheating at low speed: insufficient cooling from low flow past motor
     Solution: Don't operate below 40 Hz, use shrouded motor, increase annular flow
   - Cable failures: voltage spikes due to VFD switching
     Solution: Use VFD-rated cable, add dV/dt filters, check grounding
   - Harmonic issues: interference with other equipment, utility complaints
     Solution: Add harmonic filters on VFD input (line reactors, active filters)
        """,
        key_factors=[
            "ESP motor voltage and HP rating",
            "VFD current and voltage capacity",
            "Operating frequency range (30-70 Hz)",
            "Soft start and ramp rate settings",
            "Motor protection features (I, V, T)",
            "Power cable length and VFD compatibility",
            "Harmonics and power quality"
        ],
        primary_authority=[
            "VFD manufacturer application guides (ABB, Schneider, Siemens, Rockwell)",
            "API RP 11S7 VFD section",
            "IEEE standards on VFD harmonics and cable effects"
        ],
        burden_holder="Electrical/Production Engineer",
        adversary_position="VFD adds cost and complexity but provides operational flexibility",
        counter_arguments=[
            "Direct online starter is cheaper for fixed-speed operation",
            "VFD harmonics can cause interference issues",
            "VFD failures add downtime risk",
            "Speed variation limited by pump design range"
        ],
        resolution_strategy="Use VFD where production rate or reservoir conditions vary, benefits justify cost",
        entity_scope="ESP installations with variable rate requirements or declining reservoirs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in VFD performance; medium in long-term reliability and harmonic effects",
        controlling_precedent="VFD application per manufacturer and API RP 11S7 guidelines",
        issue_category=IssueCategory.ESP_ANALYSIS
    ),

    DoctrineBlock(
        topic="Lift Method Selection Decision Tree",
        keywords=["lift selection", "beam pump vs ESP", "gas lift vs PCP", "well conditions", "economics", "IPR"],
        conclusion_template=[
            "Artificial lift selection depends on rate, depth, fluid properties, and reservoir characteristics.",
            "Decision tree: screen by production rate, then depth, then fluid challenges.",
            "Economic analysis compares capital and operating costs over well life."
        ],
        reasoning_framework="""
Artificial lift method selection process:
1. Candidate well evaluation inputs:
   - Production rate potential: low (<100 BPD), medium (100-1000 BPD), high (>1000 BPD)
   - Lift requirement: pump setting depth, bottomhole pressure, fluid level
   - Reservoir IPR: productivity index, decline rate, drive mechanism
   - Fluid properties: viscosity, SG, water cut, GOR, sand/solids, corrosiveness
   - Wellbore: deviation, casing size, tubing size, completion type
   - Infrastructure: power availability, gas availability, access/space constraints
2. Initial screening by production rate:
   - Low rate (<100 BPD):
     Plunger lift (if high GLR), rod pump (if shallow), PCP (if viscous/sand)
   - Medium rate (100-1000 BPD):
     Rod pump, ESP (series 338-400), PCP, gas lift
   - High rate (>1000 BPD):
     ESP (series 400+), gas lift
3. Secondary screening by depth and lift:
   - Shallow (<3000 ft): rod pump preferred (simple, economical)
   - Medium (3000-8000 ft): rod pump, ESP, gas lift (depends on rate and fluids)
   - Deep (>8000 ft): ESP or gas lift (rod pump limited by rod strength and power)
4. Tertiary screening by fluid challenges:
   - High viscosity (>100 cp): PCP > rod pump >> ESP (ESP requires special stages)
   - High GOR (>1000 scf/bbl): gas lift or plunger > ESP with separator > rod pump
   - Sand/solids: PCP or jet pump > rod pump with sand pump > ESP (ESP fails quickly)
   - Corrosive (H2S, CO2): PCP, jet pump, or rod pump with special metallurgy > ESP
   - Scaling: jet pump > PCP > rod pump with inhibitor > ESP
   - High temperature (>250°F): jet pump > ESP > PCP (elastomer limit) > rod pump
5. Wellbore considerations:
   - Deviated/horizontal (>45°): ESP or PCP > rod pump (side loads on rods)
   - Small casing (4.5"): rod pump series 338 or ESP series 338 (limited options)
   - Large casing (7"+): All methods applicable, ESP higher capacity available
6. Infrastructure/operational factors:
   - No electric power: gas lift or hydraulic pump (engine-driven)
   - No gas available: rod pump, ESP, PCP, hydraulic pump
   - Offshore/remote: ESP or gas lift (lower maintenance frequency than rod pump)
   - Multiple wells: gas lift (central compressor) or shared hydraulic power unit
7. Economic comparison framework:
   - Capital costs: equipment, installation, surface facilities
   - Operating costs: power/fuel, maintenance, workover frequency
   - Run life: expected time between failures and replacement cost
   - Production optimization: method that maximizes NPV over well life
   - Example comparison (medium-rate well, 5000 ft, 500 BPD):
     Rod pump: $50K capital, $200/day opex, 5-year life → NPV = X
     ESP: $80K capital, $150/day opex, 3-year life → NPV = Y
     Select method with highest NPV or lowest cost per incremental barrel
8. Hybrid or sequential lift strategies:
   - Start with rod pump, convert to plunger as rate declines and GLR rises
   - Use ESP initially, switch to gas lift as reservoir pressure declines
   - PCP for early high-viscosity production, rod pump after cold production
        """,
        key_factors=[
            "Production rate and reservoir IPR",
            "Lift depth and fluid gradient",
            "Fluid viscosity, GOR, sand content",
            "Wellbore deviation and completion",
            "Power and gas infrastructure availability",
            "Capital cost vs. operating cost trade-off",
            "Expected run life and maintenance frequency"
        ],
        primary_authority=[
            "SPE Textbook: Petroleum Production Systems (Guo, Lyons, Ghalambor) Chapter on Lift Selection",
            "API RP 11V1: Application of Subsurface Pumps",
            "Lift system vendor selection guides"
        ],
        burden_holder="Production/Reservoir Engineer",
        adversary_position="No single lift method is optimal for all conditions; selection is case-specific",
        counter_arguments=[
            "Rod pump is simplest and most common",
            "ESP handles highest rates and deepest depths",
            "PCP is only choice for heavy oil with solids",
            "Gas lift uses free reservoir energy and has low maintenance"
        ],
        resolution_strategy="Apply decision tree screening, then economic analysis of viable options for specific well",
        entity_scope="All wells requiring artificial lift",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in screening criteria; medium in economic forecasting accuracy",
        controlling_precedent="Industry standard lift selection methodology per SPE textbooks and API guidelines",
        issue_category=IssueCategory.LIFT_SELECTION
    ),

    DoctrineBlock(
        topic="Gas Anchor and Separator Design",
        keywords=["gas anchor", "gas separator", "poor boy", "packer-type", "centrifugal", "free gas handling"],
        conclusion_template=[
            "Gas anchors and separators reduce free gas entering the pump.",
            "Poor boy: simple dip tube, relies on gas buoyancy.",
            "Centrifugal separator: spins fluid, gas separates by density, most effective."
        ],
        reasoning_framework="""
Gas anchor and separator design for rod pumps:
1. Purpose and benefits:
   - Separate free gas from liquid before pump intake
   - Improve pump fillage and volumetric efficiency
   - Reduce gas locking and pound-off
   - Increase pump capacity and run life
   - Required when gas-liquid ratio (GLR) at pump >10-15%
2. Poor boy gas anchor (simplest design):
   - Dip tube extends below pump intake
   - Operates on principle: gas is lighter than oil, rises to top
   - Liquid enters bottom of dip tube, gas vents to annulus
   - Length: 20-40 ft typical
   - Advantages: cheap, no moving parts, easy to install
   - Disadvantages: only ~30-50% gas separation efficiency, requires low entry velocity
   - Best for: low rate wells (<100 BPD), moderate GLR (<500 scf/bbl)
3. Packer-type gas anchor:
   - Packer isolates perforations from tubing-casing annulus
   - Gas and liquid enter chamber below packer
   - Gas rises to top of chamber, vents through ports to annulus above packer
   - Liquid enters pump intake at bottom of chamber
   - Advantages: 50-70% separation efficiency, controls gas entry point
   - Disadvantages: requires packer setting, limited chamber volume
   - Best for: wells with discrete gas entry zone that can be isolated
4. Centrifugal (rotary) gas separator:
   - Rotating vanes or auger impart centrifugal force to fluid
   - Heavier liquid moves outward to chamber wall, flows to pump intake
   - Lighter gas concentrates at center, vents through gas ports to annulus
   - Separation efficiency: 70-95% (best performance)
   - Advantages: high efficiency, handles high rates and high GLR
   - Disadvantages: moving parts (bearings), more expensive, requires minimum flow rate
   - Best for: high-rate wells (>200 BPD), high GLR (>1000 scf/bbl)
5. Design parameters:
   - Inlet area: sufficient to keep entry velocity low (<5 ft/sec to allow gas rise)
   - Chamber length: 20-60 ft typical, longer improves separation
   - Gas vent ports: sized to pass separated gas without creating back pressure
   - Rotation speed (centrifugal): 300-600 RPM typical, driven by production string rotation
6. Installation considerations:
   - Set below perforations to capture all gas
   - Set above pump by 1-2 tubing joints (20-40 ft) to allow separated gas to vent
   - Tubing anchor required below separator to prevent tubing movement
   - Adequate annular space for gas venting (tight annulus reduces performance)
7. Performance evaluation:
   - Measure pump fillage and volumetric efficiency with/without separator
   - Monitor gas production from annulus (should increase with separator)
   - Dynamometer card: look for reduction in gas interference signature
   - Economic evaluation: separator cost vs. production increase
8. Limitations:
   - Cannot eliminate solution gas (dissolved gas that comes out of solution at pump)
   - Foam or emulsion can reduce separation efficiency
   - Very high GLR (>2000 scf/bbl) may exceed separator capacity
   - Requires pressure differential between tubing and casing for gas venting
        """,
        key_factors=[
            "Gas-liquid ratio (GLR) at pump intake",
            "Production rate and separator sizing",
            "Separator type (poor boy, packer, centrifugal)",
            "Installation depth and perforation coverage",
            "Separation efficiency target",
            "Tubing-casing annulus clearance",
            "Cost vs. production improvement"
        ],
        primary_authority=[
            "API RP 11AR1: Care and Handling of Subsurface Pumps",
            "Gas separator manufacturer design guides",
            "SPE papers on gas anchor performance"
        ],
        burden_holder="Production Engineer and Completion Designer",
        adversary_position="Gas separator adds cost and complexity but improves pump performance",
        counter_arguments=[
            "Poor boy is cheap but low efficiency",
            "Centrifugal separator is best but expensive and has moving parts",
            "Separator may not be needed if GLR is low",
            "Gas lock can be managed by operating adjustments (speed, stroke)"
        ],
        resolution_strategy="Use separator where GLR >200 scf/bbl and pump fillage is poor; select type based on GLR and rate",
        entity_scope="Rod pump wells with gas production causing poor fillage",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in separator design principles; medium in actual field efficiency",
        controlling_precedent="Gas separator application per API RP 11AR1",
        issue_category=IssueCategory.EQUIPMENT_SPEC
    ),

    DoctrineBlock(
        topic="Tubing Anchor and Catcher Design",
        keywords=["tubing anchor", "tubing movement", "catcher", "compression anchor", "tension anchor"],
        conclusion_template=[
            "Tubing anchors prevent movement during pumping cycles.",
            "Compression anchor: slips set by upward force (most common).",
            "Tension anchor: slips set by downward force (less common)."
        ],
        reasoning_framework="""
Tubing anchor design and application:
1. Purpose of tubing anchors:
   - Prevent tubing movement (stretch and compression) during pumping cycles
   - Movement causes:
     * Rod pump: upstroke lifts fluid load, stretches tubing; downstroke compresses
     * ESP: pressure pulsations, thermal expansion
   - Effects of tubing movement:
     * Reduces effective pump stroke length and capacity
     * Causes tubing wear at couplings against casing
     * Accelerates rod and tubing fatigue
     * Creates erratic pump performance
2. Types of tubing anchors:
   a) Compression (cup-type) anchor:
      - Slips set by upward force on anchor body
      - Pumping upstroke creates compression, forces slips outward against casing
      - Most common type for rod pumps
      - Advantages: simple, reliable, low cost
      - Disadvantages: requires pump-down or wireline setting in some designs
   b) Tension (mandrel-type) anchor:
      - Slips set by downward force (tubing weight or jar impact)
      - Less common, used where compression anchor unsuitable
   c) Hydraulic-set anchor:
      - Slips set by hydraulic pressure applied through tubing
      - Used for ESP or where precise setting depth required
      - Can be released and reset without pulling tubing
   d) Mechanical-set anchor:
      - Slips set by rotation or jarring
      - Used in deviated wells where weight/compression setting may not work
3. Design considerations:
   - Casing size compatibility: anchor OD must fit casing ID with clearance
   - Slip material: hardened steel or carbide inserts for grip
   - Load rating: must exceed maximum tubing load (tension + pump load)
   - Setting depth: typically 1-2 joints below pump intake
     Deep enough to be in tension (below neutral point) but not so deep as to be in perforations
4. Installation procedure:
   - Run tubing anchor on tubing string at planned depth
   - Lower pump assembly to compress anchor and set slips
   - Apply tubing weight or jar to verify anchor is set
   - Tag bottom or measure to confirm depth
5. Tubing catcher (safety backup):
   - Installed above tubing anchor
   - Catches tubing if anchor fails or pump parts
   - Prevents tubing and rods from falling into hole
   - Critical safety device, required in most jurisdictions
6. Performance verification:
   - Observe surface tubing movement: should be zero if anchor holding
   - Dynamometer card: check for baseline shift indicating movement
   - Fluid level: measure tubing-casing annulus to verify anchor in tension zone
7. Troubleshooting anchor failures:
   - Anchor not holding: slips worn, casing size too large, insufficient compression force
   - Anchor stuck: slips over-set, casing deformation, corrosion/scale buildup
   - Tubing wear despite anchor: casing/tubing eccentricity, wellbore dogleg
        """,
        key_factors=[
            "Casing size and condition",
            "Tubing load (weight + pump load)",
            "Anchor type and load rating",
            "Setting depth and method",
            "Slip material and grip strength",
            "Presence of tubing catcher",
            "Wellbore deviation and dogleg severity"
        ],
        primary_authority=[
            "API RP 11AR1: Care and Handling of Subsurface Pumps",
            "Tubing anchor manufacturer specifications",
            "State regulatory requirements (Railroad Commission of Texas, etc.)"
        ],
        burden_holder="Completion Engineer and Rig Supervisor",
        adversary_position="Tubing anchor is required for rod pumps; failure to install causes poor performance",
        counter_arguments=[
            "Anchor adds cost and trip time",
            "Anchor can get stuck and complicate workovers",
            "Not needed for shallow low-rate wells",
            "Casing damage risk from slips"
        ],
        resolution_strategy="Install compression anchor on all rod pump wells, verify setting and performance",
        entity_scope="All rod pump wells and many ESP wells",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in anchor design and necessity; medium in long-term reliability",
        controlling_precedent="Tubing anchor standard practice per API RP 11AR1 and state regulations",
        issue_category=IssueCategory.EQUIPMENT_SPEC
    ),

    DoctrineBlock(
        topic="Pumping Unit Geometry and API 11E Classes",
        keywords=["API 11E", "pumping unit", "geometry", "conventional", "Mark II", "air balance", "torque rating"],
        conclusion_template=[
            "API 11E defines pumping unit geometry classes and rating system.",
            "Designation example: C-320D-256-120 = Conventional, 320K in-lbs torque, 25.6K lbs structure, 120 inch stroke.",
            "Geometry affects torque, load distribution, and counterbalance requirements."
        ],
        reasoning_framework="""
Pumping unit geometry and API 11E classification:
1. API 11E specification purpose:
   - Standardize pumping unit geometry, nomenclature, and ratings
   - Allow comparison of units from different manufacturers
   - Define load and torque rating methods
   - Provide design formulas for unit selection
2. Unit designation format (API 11E):
   Geometry-PeakTorque-StructureRating-StrokeLength
   Example: C-320D-256-120
   - C = Conventional geometry (other codes: M = Mark II, A = Air Balance, B = Beam Balance)
   - 320D = Peak torque rating: 320,000 in-lbs (320K), Class D
   - 256 = Structure rating: 25,600 lbs (25.6K)
   - 120 = Maximum stroke length: 120 inches
3. Geometry types:
   a) Conventional (C):
      - Walking beam pivots at center
      - Horsehead at front, counterweights at rear
      - Most common geometry (>80% of installations)
      - Torque factor ~constant over stroke cycle
   b) Mark II (M):
      - Beam pivot point moved back, reduces counterweight requirement
      - Lower peak torque than Conventional for same load
      - 20-25% better torque efficiency
      - Used for deep wells or high loads
   c) Air Balance (A):
      - Air cylinder provides counterbalance force instead of weights
      - Adjustable counterbalance without changing weights
      - Used where frequent load changes expected
   d) Beam Balance (B):
      - Counterweights on beam itself
      - Compact design for low-clearance locations
4. Load and torque calculations:
   - Polished rod load (PRL): max load at polished rod clamp
     PRL = fluid load + rod weight + dynamic forces
   - Structure rating: maximum allowable PRL (lbs)
   - Peak torque: maximum rotational torque on gearbox (in-lbs)
     Torque = PRL × torque arm distance (function of geometry and crank angle)
   - Unit selection: both structure rating and torque rating must exceed calculated values
5. Counterbalance effect:
   - Purpose: offset beam and rod weight to reduce peak motor load
   - Proper counterbalance: motor load approximately equal on upstroke and downstroke
   - Counterbalance weight calculation:
     CBE (counterbalance effect) = weight of beam + (weight of rods / 2) + fluid load factor
     Fluid load factor varies by geometry (0.5 for conventional, 0.4 for Mark II)
   - Adjust by adding/removing counterweights on crank
6. Stroke length considerations:
   - Longer stroke: higher volumetric efficiency, fewer cycles per barrel
   - Shorter stroke: lower peak loads, can run faster SPM
   - Stroke length adjustable in many units by changing crank arm position (pin settings)
   - Typical range: 30" to 300" (most common: 64", 86", 100", 120", 168")
7. Prime mover sizing:
   - Brake horsepower (BHP) = (fluid load × stroke × SPM) / (33,000 × efficiency)
   - Efficiency: ~0.75-0.85 for electric motor, ~0.70 for gas engine
   - Motor or engine must provide peak BHP plus starting torque
   - Typical prime movers: 15-100 HP electric, 20-150 HP natural gas engine
8. Unit selection example:
   - Given: 5000 ft depth, 500 BPD, 2.25" pump, 0.8 SG fluid
   - Calculate PRL: ~18,000 lbs peak
   - Select unit: C-228D-213-120 (22.8K in-lbs torque, 21.3K lbs structure, 120" stroke)
   - Verify: structure rating 21,300 > 18,000 ✓, torque adequate ✓
        """,
        key_factors=[
            "Unit geometry (Conventional, Mark II, Air Balance)",
            "Peak torque rating (in-lbs)",
            "Structure rating (max polished rod load, lbs)",
            "Stroke length (inches)",
            "Counterbalance effect and adjustment",
            "Prime mover horsepower",
            "Load and torque calculation methodology"
        ],
        primary_authority=[
            "API Spec 11E: Specification for Pumping Units",
            "Pumping unit manufacturer selection guides (Lufkin, Weatherford)",
            "API RP 11L: Design Calculations for Sucker Rod Pumping Systems (uses 11E units)"
        ],
        burden_holder="Production Engineer",
        adversary_position="API 11E standardization allows comparison but actual units vary in quality and features",
        counter_arguments=[
            "Conventional geometry is simplest and most reliable",
            "Mark II reduces loads but adds mechanical complexity",
            "Air balance is flexible but requires compressor and maintenance",
            "Larger unit provides reserve capacity but costs more and uses more power"
        ],
        resolution_strategy="Use API 11E calculations to select minimum unit meeting load and torque requirements",
        entity_scope="All beam pump installations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in API 11E rating system and selection methodology",
        controlling_precedent="API Spec 11E is universally accepted pumping unit standard",
        issue_category=IssueCategory.EQUIPMENT_SPEC
    ),

    DoctrineBlock(
        topic="Polished Rod Clamp and Stuffing Box",
        keywords=["polished rod", "stuffing box", "packing", "carrier bar", "leak", "seal"],
        conclusion_template=[
            "Polished rod clamp connects pumping unit to rod string.",
            "Stuffing box seals annulus around polished rod to prevent wellhead leaks.",
            "Proper packing selection and maintenance critical for safety and environmental compliance."
        ],
        reasoning_framework="""
Polished rod clamp and stuffing box design:
1. Polished rod clamp:
   - Connects horsehead carrier bar to top of polished rod
   - Clamp body bolts around polished rod, secured with cap screws
   - Must allow free vertical movement during pumping stroke
   - Safety: inspect regularly for cracks, wear, proper torque on fasteners
   - Failure mode: clamp slip or breakage causes loss of rod string control (serious hazard)
2. Polished rod specifications:
   - Material: alloy steel, hardened and chrome-plated surface
   - Diameter: 3/4", 7/8", 1", 1-1/8", 1-1/4" (most common 1" and 1-1/8")
   - Length: 20-30 ft typical (extends from clamp to stuffing box to top rod)
   - Surface finish: smooth, hard chrome plating for wear resistance and seal life
   - API grades similar to sucker rods (Grade D, K)
3. Stuffing box (wellhead seal):
   - Purpose: seal annular space between polished rod and wellhead
   - Prevents produced fluids (oil, gas, water) from escaping at surface
   - Critical for safety (prevent gas release) and environmental compliance (prevent spills)
4. Stuffing box components:
   - Body: bolts to wellhead flange or clamshell assembly
   - Packing: compressible seal material that grips polished rod
   - Gland: compression follower plate that tightens packing against rod
   - Tightening bolts: compress gland to adjust packing pressure
5. Packing materials:
   - Asbestos-free synthetic rubber (most common today)
   - Braided packing: graphite, PTFE, aramid fiber
   - V-ring or chevron packing: rubber rings stacked in V shape
   - Selection based on:
     * Fluid type: oil, water, gas, H2S, CO2
     * Temperature: ambient to 300°F
     * Pressure: wellhead pressure
     * Rod speed and stroke
6. Stuffing box maintenance:
   - Tighten packing periodically as it wears and compresses
   - Replace packing when leaking cannot be stopped by tightening
   - Typical packing life: 6-24 months depending on conditions
   - Leaking stuffing box: safety and environmental violation, must repair immediately
7. Common stuffing box problems:
   - Leak around rod: packing worn, dried out, or insufficiently tightened
     Solution: tighten gland, replace packing if needed
   - Excessive friction: over-tightened, causing high loads and power consumption
     Solution: back off gland slightly, check for polished rod surface damage
   - Polished rod wear: grooves worn into rod surface by packing
     Solution: rotate rod 1/4 turn to present fresh surface, or replace rod
   - Corrosion: H2S or CO2 attack on metal parts
     Solution: upgrade to corrosion-resistant materials
8. Polished rod surface maintenance:
   - Inspect for scoring, pitting, corrosion
   - Light scoring can be polished with emery cloth
   - Deep grooves require rod replacement (groove causes packing to leak)
   - Chrome plating can be re-applied in some cases
        """,
        key_factors=[
            "Polished rod diameter and material",
            "Polished rod surface condition",
            "Stuffing box body and pressure rating",
            "Packing material and fluid compatibility",
            "Gland compression and adjustment",
            "Leak detection and repair",
            "Safety and environmental compliance"
        ],
        primary_authority=[
            "API RP 11AR2: Care and Handling of Polished Rods",
            "Stuffing box manufacturer installation guides",
            "OSHA and EPA regulations on wellhead emissions"
        ],
        burden_holder="Production Operations and Well Tender",
        adversary_position="Stuffing box is simple device but critical for safety; neglect causes violations",
        counter_arguments=[
            "Over-tightening wastes power and wears rod",
            "Under-tightening leaks fluids and gas",
            "Packing replacement is routine maintenance but requires well shutdown",
            "Polished rod damage is expensive to repair"
        ],
        resolution_strategy="Maintain proper stuffing box adjustment, replace packing on schedule, inspect polished rod regularly",
        entity_scope="All beam pump wellheads",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in stuffing box function and maintenance requirements",
        controlling_precedent="Stuffing box maintenance per API RP 11AR2 and safety regulations",
        issue_category=IssueCategory.EQUIPMENT_SPEC
    ),

    DoctrineBlock(
        topic="Production Optimization via Lift Method",
        keywords=["optimization", "cost per barrel", "NPV", "run life", "efficiency", "production rate"],
        conclusion_template=[
            "Lift method optimization balances production rate, efficiency, and cost.",
            "Objective: minimize cost per barrel or maximize NPV over well life.",
            "Consider capital cost, operating cost, run life, and production response."
        ],
        reasoning_framework="""
Production optimization via artificial lift method selection and operation:
1. Optimization objective functions:
   a) Minimize cost per barrel produced:
      Cost/bbl = (Capital cost + Operating cost) / (Production rate × Time)
      Favor low-cost methods for marginal wells
   b) Maximize net present value (NPV):
      NPV = Σ[(Revenue - Opex) × (1 + discount rate)^-t] - Capex
      Favor high-rate production even if cost per barrel is higher
   c) Maximize production rate subject to cost constraint:
      Useful when oil price is high and every barrel has high margin
2. Cost components by lift method:

   ROD PUMP:
   - Capital: Pumping unit ($30-80K), rods ($10-30K), pump ($2-8K), install ($10-20K)
     Total: $50-140K depending on size and depth
   - Operating: Power ($50-200/day), maintenance ($20-50/day), workovers (~every 3-5 years, $50-100K)
   - Run life: 3-7 years typical for pump, 10-20 years for surface unit

   ESP:
   - Capital: Downhole assembly ($40-150K), cable ($20-80K), VFD ($20-60K), install ($20-40K)
     Total: $100-330K depending on size and depth
   - Operating: Power ($100-400/day), maintenance ($10-30/day), workovers (~every 2-4 years, $80-200K)
   - Run life: 2-5 years typical (shorter in harsh conditions)

   GAS LIFT:
   - Capital: Valves and mandrels ($10-30K), tubing ($20-60K), surface compression ($50-300K per well, shared)
     Total: $80-400K depending on compression needs
   - Operating: Compression fuel/power ($50-300/day), maintenance ($10-30/day), valve service (~every 5+ years)
   - Run life: Valves 5-15 years, compressor 15-25 years

   PCP:
   - Capital: Downhole pump ($15-50K), drive head ($10-30K), rods ($10-30K), install ($10-20K)
     Total: $45-130K
   - Operating: Power ($40-150/day), maintenance ($20-40/day), workovers (~every 1-3 years, $40-80K)
   - Run life: 1-4 years for elastomer, 10-20 years for drive head

   PLUNGER LIFT:
   - Capital: Plunger ($2-5K), controller ($5-15K), lubricator/catcher ($5-10K)
     Total: $12-30K (very low cost)
   - Operating: Minimal power, low maintenance (<$10/day), plunger replacement (~$2-5K every 2-5 years)
   - Run life: Plunger 2-5+ years, controller 10+ years

3. Production rate impact:
   - Higher rate → more revenue per day → can justify higher cost method
   - Lower rate → must minimize cost, favor simple low-cost methods
   - Rate decline over time → method that adapts (VFD for ESP, speed control for rod pump) has advantage
4. Efficiency considerations:
   - Mechanical efficiency: ESP 60-75%, Rod pump 50-70%, Gas lift 20-50%, PCP 50-70%, Jet pump 20-40%
   - Energy cost ($/bbl) = (Hydraulic HP × Operating hours) / (Efficiency × Production volume) × Energy price
   - High energy price → favor high-efficiency methods
   - Low energy price → efficiency less critical than reliability
5. Operational flexibility:
   - Methods with adjustability (VFD for ESP, speed/stroke for rod pump, gas rate for gas lift) allow optimization as conditions change
   - Fixed-speed methods require workover to change capacity (less flexible)
6. Optimization workflow:
   - Step 1: Screen viable methods based on well conditions (rate, depth, fluids)
   - Step 2: Design each method for target production rate
   - Step 3: Estimate capital and operating costs over expected well life
   - Step 4: Forecast production profile (decline curve)
   - Step 5: Calculate NPV for each method using discount rate (typically 10-15%)
   - Step 6: Select method with highest NPV or lowest cost per barrel
   - Step 7: Sensitivity analysis on key assumptions (oil price, run life, decline rate)
7. Operational optimization (after installation):
   - Rod pump: adjust speed and stroke to maximize production without fluid pound or gas lock
   - ESP: adjust VFD speed to operate at best efficiency point (BEP) on pump curve
   - Gas lift: optimize injection rate and valve depth for maximum production at minimum gas usage
   - PCP: adjust speed to balance rate and wear (higher speed = more rate but faster elastomer wear)
   - Plunger: optimize cycle time (shut-in and afterflow) for maximum cycles per day
8. Real-time optimization technologies:
   - SCADA monitoring: track production, power, downhole sensors
   - Automated controllers: adjust lift parameters based on well response
   - Machine learning models: predict optimal settings based on historical data
   - Economic optimization algorithms: adjust for changing oil price and costs
        """,
        key_factors=[
            "Capital cost by method",
            "Operating cost (power, maintenance, workovers)",
            "Expected run life and replacement frequency",
            "Production rate and decline curve",
            "Energy efficiency and power cost",
            "NPV calculation and discount rate",
            "Operational flexibility and adaptability"
        ],
        primary_authority=[
            "SPE Economics and Evaluation papers on lift method optimization",
            "Operator internal economic models and field data",
            "Service company cost databases"
        ],
        burden_holder="Production/Reservoir Engineer and Asset Team",
        adversary_position="Lowest cost per barrel may not maximize NPV; must consider time value of money",
        counter_arguments=[
            "Cheapest method upfront may have higher long-term cost",
            "Highest efficiency may not justify high capital cost",
            "Simplest method may sacrifice production",
            "Most flexible method may have lower reliability"
        ],
        resolution_strategy="Use NPV analysis with realistic cost and production forecasts to select optimal lift method",
        entity_scope="All wells requiring artificial lift economic evaluation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in cost estimation and NPV methodology; medium in production forecasting",
        controlling_precedent="Engineering economics principles applied to artificial lift selection",
        issue_category=IssueCategory.OPTIMIZATION
    ),

    DoctrineBlock(
        topic="ESP Motor Cooling and Shrouding",
        keywords=["ESP motor", "motor cooling", "shroud", "thermal protection", "motor temperature", "flow past motor"],
        conclusion_template=[
            "ESP motors require liquid flow past motor for cooling.",
            "Shroud forces production through annular space around motor.",
            "Insufficient cooling causes motor overheating and failure."
        ],
        reasoning_framework="""
ESP motor cooling requirements and shrouding:
1. Motor cooling fundamentals:
   - ESP motors are oil-filled, submersed in wellbore fluids
   - Motor windings generate heat (I²R losses, core losses)
   - Heat must be removed by wellbore fluid flow past motor housing
   - Required cooling flow rate typically 1-5 ft/sec annular velocity
   - If flow too low → motor overheats → insulation failure → motor burn
2. Motor heat generation:
   - Function of motor load (HP), efficiency, and voltage
   - Higher load = more heat
   - Voltage imbalance increases losses and heat
   - Typical motor efficiency: 85-92% (8-15% of power becomes heat)
3. Cooling flow paths:
   - Open annulus: fluid flows up casing-tubing annulus, passes motor
   - Shrouded motor: shroud tube forces ALL production up past motor
   - Natural vs. forced flow: high-rate wells provide natural flow; low-rate wells may need shroud
4. Shroud design:
   - Sheet metal or tubing section around motor OD
   - Extends above motor to force flow through motor-shroud annulus
   - Annular area between motor OD and shroud ID controls velocity
   - Design target: minimum 1 ft/sec velocity at minimum production rate
5. Shroud sizing calculation:
   - Annular area = π/4 × (Shroud ID² - Motor OD²)
   - Velocity (ft/sec) = Production rate (BPD) / (Annular area (in²) × 0.0119)
   - Example: 500 BPD, 5.5" shroud ID, 4.56" motor OD
     Area = π/4 × (5.5² - 4.56²) = 7.42 in²
     Velocity = 500 / (7.42 × 0.0119) = 5.7 ft/sec ✓ (adequate)
6. Motor temperature monitoring:
   - Downhole temperature sensors: embedded in motor windings or on housing
   - Typical operating limit: 200-250°F depending on motor insulation class
   - Trend monitoring: temperature rise over time indicates cooling issue
   - Trip setpoint: typically 15-25°F below max rated temperature
7. Shroud installation and considerations:
   - Attached to motor/pump assembly before running in hole
   - Length: extends from below motor intake to above motor top
   - Clearance: must fit inside casing with adequate clearance
   - Perforation coverage: shroud bottom must be below perforations to capture flow
8. Cooling problems and solutions:

   Problem: Low production rate insufficient for cooling
   Solution: Install or extend shroud to increase velocity

   Problem: Gas production bypasses motor (flows up annulus, not through shroud)
   Solution: Install packer above motor to force flow through shroud

   Problem: High fluid temperature from reservoir (>180°F)
   Solution: Use high-temperature motor insulation (Class H or higher, rated 200-250°F)

   Problem: VFD operation at low speed reduces flow
   Solution: Don't operate below 40 Hz; ensure minimum flow maintained

   Problem: Shut-in well overheats (no flow, motor still energized)
   Solution: Interlock motor starter with pump-off control; shut down if no flow
9. Motor thermal protection strategies:
   - Downhole temperature sensor with surface alarm
   - Time-delayed overload relay on motor starter
   - VFD overcurrent and overtemperature protection
   - Pump-off control to shut down on low production/no flow
        """,
        key_factors=[
            "Motor horsepower and heat generation",
            "Production rate and annular velocity",
            "Shroud sizing and installation",
            "Downhole temperature monitoring",
            "Reservoir fluid temperature",
            "Gas content and flow path",
            "VFD speed and minimum flow requirement"
        ],
        primary_authority=[
            "ESP motor manufacturer specifications and guidelines",
            "API RP 11S7 motor cooling section",
            "ESP design software shroud sizing modules"
        ],
        burden_holder="ESP Design Engineer and Operations",
        adversary_position="Inadequate motor cooling is leading cause of ESP failures",
        counter_arguments=[
            "Shroud adds cost and reduces annular clearance",
            "High-rate wells don't need shroud",
            "Temperature sensors add cost and connection points",
            "Oversized motor reduces loading and heat but wastes power"
        ],
        resolution_strategy="Design shroud to ensure minimum 1 ft/sec velocity at lowest expected production rate",
        entity_scope="All ESP installations, especially critical for low-rate or high-temperature wells",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in motor cooling requirements and shroud design",
        controlling_precedent="Motor cooling per ESP manufacturer specifications and API RP 11S7",
        issue_category=IssueCategory.ESP_ANALYSIS
    ),

    DoctrineBlock(
        topic="Beam Pump Prime Mover Selection",
        keywords=["prime mover", "electric motor", "gas engine", "brake horsepower", "starting torque", "NEMA"],
        conclusion_template=[
            "Prime mover provides power to turn pumping unit.",
            "Electric motor: most common, 15-100 HP, 3-phase preferred.",
            "Gas engine: used where electric power unavailable or to utilize lease gas."
        ],
        reasoning_framework="""
Prime mover selection and sizing for beam pumps:
1. Prime mover options:
   a) Electric motor (most common):
      - 3-phase AC induction motor (230V, 460V, or 575V)
      - Single-phase for small units (<15 HP, residential power)
      - Typical sizes: 15, 20, 25, 30, 40, 50, 60, 75, 100 HP
      - NEMA Design D: high starting torque (225% of rated), required for beam pumps
      - Enclosure: TEFC (totally enclosed fan cooled) or explosion-proof for hazardous areas
   b) Natural gas engine:
      - 20-150 HP typical
      - Fueled by lease gas (free fuel source)
      - Advantages: no electric infrastructure required, can use otherwise-flared gas
      - Disadvantages: higher maintenance, air emissions, noise, less efficient
   c) Diesel engine (rare):
      - Used only where no electric or gas available
      - High fuel cost, maintenance, emissions
2. Brake horsepower (BHP) calculation:
   BHP = (Fluid load × Stroke × SPM) / (33,000 × Efficiency)
   Where:
   - Fluid load (lbs): pump depth × fluid gradient + dynamic effects
   - Stroke (inches): from pumping unit rating
   - SPM: strokes per minute (pumping speed)
   - Efficiency: 0.75-0.85 for electric motor, 0.70 for gas engine
   - 33,000: constant (ft-lbs/min per HP)
   Example: 10,000 lbs fluid load, 100" stroke, 12 SPM, 0.80 efficiency
   BHP = (10,000 × 100 × 12) / (33,000 × 0.80) = 45 HP
   Select next standard size up: 50 HP motor
3. Electric motor starting requirements:
   - Beam pump has high starting torque (must overcome static friction and acceleration)
   - NEMA Design D motor required: 225% starting torque at 5% slip
   - Standard Design B motor (150% torque) insufficient for beam pumps
   - Soft start or VFD can reduce starting current but Design D still preferred
4. Motor nameplate ratings:
   - Voltage: must match available power (208V, 230V, 460V, 575V common)
   - Full Load Amps (FLA): for wire and breaker sizing
   - Service Factor (SF): 1.15 typical (can run 15% overload continuously)
   - Insulation Class: B (266°F), F (311°F), H (356°F) for high-temperature service
   - Frame size: NEMA standard (254T, 286T, etc.)
5. Gas engine sizing and configuration:
   - HP rating at operating altitude and temperature
   - De-rate for altitude: ~3% per 1000 ft above sea level
   - Low-speed engine (900-1200 RPM) preferred for long life and reliability
   - Governor control: droop or isochronous speed regulation
   - Ignition: magneto (no electric power needed) or battery
6. Prime mover installation considerations:
   - Mounting: foundation pad, alignment to pumping unit sheave
   - Guarding: belt guard required for safety (OSHA)
   - Electrical: disconnect, overload protection, grounding
   - Gas engine: fuel line, exhaust, cooling (air or radiator), emissions controls
7. Belt drive design:
   - V-belt or poly-V belt connects motor/engine sheave to gearbox input sheave
   - Speed ratio: motor RPM / gearbox input RPM
   - Typical motor speed: 1800 RPM (4-pole) or 1200 RPM (6-pole)
   - Gearbox input speed: 300-600 RPM typical
   - Belt tension critical: too loose = slippage, too tight = bearing wear
8. Operational considerations:
   - Electric motor: power factor (0.85-0.95), inrush current, voltage quality
   - Gas engine: fuel quality (BTU content, H2S level), emissions compliance
   - Both: load factor (% of rated HP), duty cycle (intermittent vs. continuous)
   - Maintenance: electric motor low (bearing grease every 6-12 months)
                 gas engine high (oil, filters, valves, ignition every 500-2000 hours)
        """,
        key_factors=[
            "Brake horsepower requirement",
            "Prime mover type (electric vs. gas)",
            "Motor Design D for beam pump starting",
            "Voltage and phase availability",
            "Service factor and duty cycle",
            "Gas engine fuel source and emissions",
            "Belt drive speed ratio and tension"
        ],
        primary_authority=[
            "NEMA MG1: Motors and Generators Standard",
            "API RP 11L prime mover sizing",
            "Pumping unit manufacturer installation manuals"
        ],
        burden_holder="Electrical Engineer and Operations",
        adversary_position="Undersized motor trips on overload; oversized motor wastes capital and power (low power factor)",
        counter_arguments=[
            "Larger motor provides reserve capacity",
            "Smaller motor saves cost but may not start under load",
            "Gas engine uses free fuel but has high maintenance cost",
            "Electric motor is efficient but requires power infrastructure"
        ],
        resolution_strategy="Calculate BHP per API RP 11L, select next standard motor size up, verify Design D rating",
        entity_scope="All beam pump installations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in BHP calculation and motor selection methodology",
        controlling_precedent="Motor sizing per API RP 11L and NEMA MG1 standards",
        issue_category=IssueCategory.EQUIPMENT_SPEC
    )
]


# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class TelemetryCollector:
    """Tracks query performance and doctrine usage."""

    def __init__(self):
        self.queries_processed = 0
        self.total_latency_ms = 0.0
        self.doctrine_hit_count: Dict[str, int] = {}
        self.error_count = 0
        self.start_time = datetime.now()

    def record_query(self, latency_ms: float, doctrines_triggered: List[str], error: bool = False):
        self.queries_processed += 1
        self.total_latency_ms += latency_ms
        if error:
            self.error_count += 1
        for doctrine in doctrines_triggered:
            self.doctrine_hit_count[doctrine] = self.doctrine_hit_count.get(doctrine, 0) + 1

    def get_metrics(self) -> Dict[str, Any]:
        uptime = (datetime.now() - self.start_time).total_seconds()
        return {
            "queries_processed": self.queries_processed,
            "avg_latency_ms": self.total_latency_ms / max(1, self.queries_processed),
            "error_count": self.error_count,
            "uptime_seconds": uptime,
            "top_doctrines": sorted(self.doctrine_hit_count.items(), key=lambda x: x[1], reverse=True)[:10]
        }


telemetry = TelemetryCollector()


# ============================================================================
# CORE INTELLIGENCE ENGINE
# ============================================================================

class ArtificialLiftEngine:
    """Artificial Lift Systems Intelligence Engine - TIE Gold Standard"""

    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.version = "1.0.0"
        logger.info(f"OFE05 Artificial Lift Engine v{self.version} initialized with {len(self.doctrines)} doctrine blocks")

    def three_layer_response(self, query: str, mode: ResponseMode, zone: AnalysisZone, context: Optional[Dict] = None) -> QueryResponse:
        """
        TIE-20 Component: Three-layer response system
        Layer 1: Doctrine cache (fast, 0-50ms)
        Layer 2: Semantic retrieval (medium, 50-200ms)
        Layer 3: Deep analysis (slow, 200ms+)
        """
        start_time = datetime.now()

        # Normalize query
        normalized_query = self._semantic_normalization(query)

        # Layer 1: Doctrine cache lookup
        triggered_doctrines = self._doctrine_cache_lookup(normalized_query)

        if not triggered_doctrines:
            # Layer 2 would go here (semantic vector search) - using keyword fallback for now
            triggered_doctrines = self._fallback_keyword_match(normalized_query)

        # Build response based on mode
        answer = self._build_response(triggered_doctrines, mode, zone, context)

        # Confidence stratification
        confidence = self._assess_confidence(triggered_doctrines, query)

        # Generate determinism hash
        response_data = f"{query}|{answer}|{mode.value}|{zone.value}"
        determinism_hash = hashlib.sha256(response_data.encode()).hexdigest()[:16]

        # Calculate latency
        latency_ms = (datetime.now() - start_time).total_seconds() * 1000

        # Record telemetry
        telemetry.record_query(latency_ms, [d.topic for d in triggered_doctrines])

        # Audit trail (would write to JSONL in production)
        logger.info(f"Query processed: {query[:100]} | Mode: {mode.value} | Doctrines: {len(triggered_doctrines)} | Latency: {latency_ms:.1f}ms")

        return QueryResponse(
            query=query,
            answer=answer,
            mode=mode,
            zone=zone,
            confidence=confidence,
            doctrines_triggered=[d.topic for d in triggered_doctrines],
            determinism_hash=determinism_hash,
            latency_ms=round(latency_ms, 2),
            timestamp=datetime.now().isoformat()
        )

    def _semantic_normalization(self, query: str) -> str:
        """TIE-20 Component: Normalize domain-specific terms"""
        normalizations = {
            "sucker rod pump": "rod pump",
            "beam pump": "rod pump",
            "electrical submersible pump": "ESP",
            "electric submersible pump": "ESP",
            "progressive cavity": "PCP",
            "screw pump": "PCP",
            "moineau": "PCP",
            "artificial lift": "lift",
            "dynagraph": "dynamometer",
            "downhole card": "dynamometer card",
            "surface card": "dynamometer card"
        }

        normalized = query.lower()
        for term, replacement in normalizations.items():
            normalized = normalized.replace(term, replacement)

        return normalized

    def _doctrine_cache_lookup(self, normalized_query: str) -> List[DoctrineBlock]:
        """TIE-20 Component: Fast doctrine cache retrieval"""
        triggered = []
        query_words = set(normalized_query.lower().split())

        for doctrine in self.doctrines:
            # Check keyword overlap
            keyword_hits = sum(1 for kw in doctrine.keywords if kw.lower() in normalized_query)
            if keyword_hits >= 2:  # Threshold: at least 2 keyword matches
                triggered.append(doctrine)
            elif keyword_hits == 1:
                # Check topic match for single keyword hit
                if any(word in doctrine.topic.lower() for word in query_words):
                    triggered.append(doctrine)

        # Sort by relevance (keyword hit count)
        triggered.sort(key=lambda d: sum(1 for kw in d.keywords if kw.lower() in normalized_query), reverse=True)

        return triggered[:5]  # Top 5 most relevant

    def _fallback_keyword_match(self, normalized_query: str) -> List[DoctrineBlock]:
        """Layer 2 fallback: broader keyword matching"""
        matches = []
        for doctrine in self.doctrines:
            if any(kw.lower() in normalized_query for kw in doctrine.keywords):
                matches.append(doctrine)

        return matches[:3]  # Return top 3

    def _build_response(self, doctrines: List[DoctrineBlock], mode: ResponseMode, zone: AnalysisZone, context: Optional[Dict]) -> str:
        """TIE-20 Component: Response modes (FAST/DEFENSE/MEMO)"""

        if not doctrines:
            return "No specific artificial lift doctrine applies to this query. Please provide more details about the equipment type, well conditions, or specific technical issue."

        if mode == ResponseMode.FAST:
            # Concise response: conclusions only
            parts = []
            for d in doctrines[:2]:  # Top 2 doctrines
                parts.append(f"**{d.topic}:**\n" + "\n".join(f"- {c}" for c in d.conclusion_template))
            return "\n\n".join(parts)

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready response: conclusions + authority + confidence
            parts = []
            for d in doctrines[:3]:
                section = f"## {d.topic}\n\n"
                section += "### Conclusion:\n" + "\n".join(f"- {c}" for c in d.conclusion_template) + "\n\n"
                section += "### Authority:\n" + "\n".join(f"- {a}" for a in d.primary_authority) + "\n\n"
                section += f"### Confidence: {d.confidence.value}\n"
                section += f"**Stratification:** {d.confidence_stratification}\n\n"
                if d.disclosure_caveat:
                    section += f"**Disclosure:** {d.disclosure_caveat}\n\n"
                parts.append(section)
            return "\n".join(parts)

        else:  # MEMO
            # Full documentation: reasoning + factors + authority + adversarial analysis
            parts = []
            for d in doctrines[:3]:
                section = f"# {d.topic}\n\n"
                section += "## Executive Summary\n" + "\n".join(f"- {c}" for c in d.conclusion_template) + "\n\n"
                section += f"## Detailed Analysis\n\n{d.reasoning_framework}\n\n"
                section += "## Key Factors\n" + "\n".join(f"- {f}" for f in d.key_factors) + "\n\n"
                section += "## Authoritative Sources\n" + "\n".join(f"- {a}" for a in d.primary_authority) + "\n\n"
                section += f"## Adversarial Position\n{d.adversary_position}\n\n"
                section += "## Counter-Arguments\n" + "\n".join(f"- {c}" for c in d.counter_arguments) + "\n\n"
                section += f"## Resolution Strategy\n{d.resolution_strategy}\n\n"
                section += f"## Confidence Assessment\n**Level:** {d.confidence.value}\n\n{d.confidence_stratification}\n\n"
                if d.disclosure_caveat:
                    section += f"**Disclosure Caveat:** {d.disclosure_caveat}\n\n"
                parts.append(section)

            return "\n---\n\n".join(parts)

    def _assess_confidence(self, doctrines: List[DoctrineBlock], query: str) -> ConfidenceLevel:
        """TIE-20 Component: Confidence stratification"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Use most conservative confidence from triggered doctrines
        confidence_order = [ConfidenceLevel.DEFENSIBLE, ConfidenceLevel.AGGRESSIVE, ConfidenceLevel.DISCLOSURE, ConfidenceLevel.HIGH_RISK]
        doctrine_confidences = [d.confidence for d in doctrines]

        for level in reversed(confidence_order):  # Start from most conservative
            if level in doctrine_confidences:
                return level

        return ConfidenceLevel.DEFENSIBLE


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="OFE05 - Artificial Lift Systems Engine",
    description="TIE Gold Standard Intelligence Engine for Artificial Lift Method Selection, Design, and Troubleshooting",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = ArtificialLiftEngine()


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Main query endpoint for artificial lift intelligence.

    Supports three response modes:
    - FAST: Quick conclusions only
    - DEFENSE: Audit-ready with citations
    - MEMO: Full technical documentation
    """
    try:
        return engine.three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            context=request.context
        )
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        telemetry.record_query(0, [], error=True)
        raise HTTPException(status_code=500, detail=f"Engine error: {str(e)}")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """TIE-20 Component: Comprehensive health endpoint"""
    metrics = telemetry.get_metrics()
    return HealthResponse(
        status="operational",
        version=engine.version,
        port=9005,
        doctrine_count=len(engine.doctrines),
        uptime_seconds=metrics["uptime_seconds"],
        queries_processed=metrics["queries_processed"],
        avg_latency_ms=metrics["avg_latency_ms"]
    )


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics and categories"""
    return {
        "total_doctrines": len(engine.doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in engine.doctrines
        ]
    }


@app.get("/metrics")
async def get_metrics():
    """TIE-20 Component: Telemetry and performance metrics"""
    return telemetry.get_metrics()


@app.get("/")
async def root():
    """Engine information and usage"""
    return {
        "engine": "OFE05 - Artificial Lift Systems Engine",
        "version": engine.version,
        "status": "operational",
        "domain": "Oilfield Equipment - Artificial Lift Methods",
        "doctrines": len(engine.doctrines),
        "capabilities": [
            "Rod pump (beam pump) design and troubleshooting",
            "ESP selection, sizing, and failure analysis",
            "Gas lift valve spacing and optimization",
            "PCP applications and elastomer selection",
            "Plunger lift systems and cycle optimization",
            "Hydraulic jet pump design",
            "Dynamometer card analysis",
            "Lift method selection decision tree",
            "Production optimization economics",
            "Equipment specifications (API 11E, 11L, 11S7)"
        ],
        "endpoints": {
            "query": "POST /query - Main intelligence endpoint",
            "health": "GET /health - System health check",
            "doctrines": "GET /doctrines - List all doctrine blocks",
            "metrics": "GET /metrics - Performance telemetry"
        }
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting OFE05 Artificial Lift Systems Engine on port 9005")
    uvicorn.run(app, host="0.0.0.0", port=9005)
