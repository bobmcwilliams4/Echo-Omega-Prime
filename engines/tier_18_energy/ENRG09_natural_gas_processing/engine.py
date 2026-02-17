"""
ENRG09 Natural Gas Processing Intelligence Engine
TIE-Grade Domain: Gas Sweetening, Dehydration, NGL Recovery, Fractionation, Compression, Pipeline Quality
Version: 1.0.0
Port: 9244

Real domain expertise in:
- Amine gas sweetening (MDEA, DEA, MEA selection criteria)
- Claus sulfur recovery processes
- Glycol dehydration (TEG contactor design)
- Molecular sieve dehydration
- NGL recovery (turboexpander, J-T valve, GSP/SCORE processes)
- Fractionation tower design (demethanizer, deethanizer, depropanizer)
- Pipeline quality specifications (H2S, CO2, water content, BTU)
- Gas compression (reciprocating vs centrifugal selection)
- GPSA Engineering Data Book standards
- Gas chromatograph analysis and BTU optimization
- Residue gas vs NGL economics
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

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

class IssueCategory(str, Enum):
    GAS_SWEETENING = "GAS_SWEETENING"
    DEHYDRATION = "DEHYDRATION"
    NGL_RECOVERY = "NGL_RECOVERY"
    FRACTIONATION = "FRACTIONATION"
    COMPRESSION = "COMPRESSION"
    PIPELINE_QUALITY = "PIPELINE_QUALITY"
    SULFUR_RECOVERY = "SULFUR_RECOVERY"
    PROCESS_OPTIMIZATION = "PROCESS_OPTIMIZATION"
    EQUIPMENT_SELECTION = "EQUIPMENT_SELECTION"
    SAFETY_SYSTEMS = "SAFETY_SYSTEMS"
    REGULATORY_COMPLIANCE = "REGULATORY_COMPLIANCE"
    ECONOMIC_ANALYSIS = "ECONOMIC_ANALYSIS"

class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    OPERATIONS = "OPERATIONS"
    MAINTENANCE = "MAINTENANCE"
    AUDIT = "AUDIT"

@dataclass
class DoctrineBlock:
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
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    category: IssueCategory
    position_zone: PositionZone

class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural gas processing question or scenario")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context (gas composition, flow rates, specifications)")

class QueryResponse(BaseModel):
    query: str
    mode: ResponseMode
    answer: str
    triggered_doctrines: List[str]
    confidence: ConfidenceLevel
    cache_hit: bool
    latency_ms: float
    determinism_hash: str
    epistemic_warnings: List[str]
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrine_count: int
    cache_size: int
    total_queries: int
    avg_latency_ms: float
    uptime_seconds: float

# ============================================================================
# DOCTRINE CACHE - 25+ Real Natural Gas Processing Domain Expertise
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Amine Gas Sweetening Selection MDEA vs DEA vs MEA",
        keywords=["amine selection", "MDEA", "DEA", "MEA", "acid gas removal", "H2S removal", "CO2 selectivity", "sweetening"],
        conclusion_template="Amine selection depends on acid gas composition, selectivity requirements, and regeneration energy. MDEA provides best H2S selectivity with low CO2 pickup. DEA balances performance and cost. MEA achieves lowest residual H2S but has high heat requirements.",
        reasoning_framework="""
Amine Gas Sweetening Selection Analysis:

1. MDEA (Methyldiethanolamine) Advantages:
   - Highest H2S selectivity vs CO2 (10:1 to 20:1 selectivity ratio)
   - Lowest regeneration energy (700-900 BTU/lb amine)
   - Best for high CO2/H2S ratio gas streams
   - Minimal corrosion due to low CO2 loading
   - Treats gas to pipeline spec (H2S < 4 ppm) efficiently
   - Lower circulation rates reduce pump power
   - Non-degrading amine with minimal reclaimer duty
   - Ideal for bulk CO2 removal applications
   - Reboiler temperature 230-250°F (lower than MEA)
   - Typical concentration 45-50 wt%

2. DEA (Diethanolamine) Characteristics:
   - Moderate H2S/CO2 selectivity (4:1 to 6:1 ratio)
   - Regeneration energy 1000-1200 BTU/lb amine
   - Good COS and mercaptan removal capability
   - Balance between performance and capital cost
   - Proven technology with extensive field experience
   - Handles moderate acid gas loadings well
   - Typical concentration 25-35 wt%
   - Reboiler temperature 240-260°F
   - More corrosive than MDEA at high loadings
   - Requires filtration to remove degradation products

3. MEA (Monoethanolamine) Performance:
   - Achieves lowest residual H2S (< 0.25 grain/100 scf)
   - High CO2 removal efficiency (> 99%)
   - Highest regeneration energy (1400-1600 BTU/lb amine)
   - Most corrosive amine requiring strict oxygen control
   - Degrades rapidly requiring continuous reclaiming
   - High circulation rates increase OPEX
   - Typical concentration 15-20 wt%
   - Reboiler temperature 250-270°F
   - Best for low pressure applications
   - Requires extensive corrosion inhibitor program

4. Selection Criteria Matrix:
   - High H2S/low CO2: MDEA preferred (selective removal)
   - Low H2S/high CO2: MEA or DEA (bulk removal)
   - COS/mercaptans present: DEA or promoted MDEA
   - Energy cost dominant: MDEA (lowest regen energy)
   - Capital cost limited: DEA (moderate performance)
   - Ultra-low H2S required: Promoted MDEA or MEA
   - Operating pressure < 300 psig: MEA or DEA
   - Operating pressure > 1000 psig: MDEA
   - Foaming tendencies: MDEA (most stable)
   - Offshore/remote locations: MDEA (lowest maintenance)

5. Economic Comparison:
   - CAPEX: MEA > DEA > MDEA (due to circulation rates)
   - OPEX: MEA > DEA > MDEA (energy and reclaiming)
   - Amine makeup costs: MEA (2-3 lb/MMSCF) > DEA (1-2 lb) > MDEA (0.5-1 lb)
   - Lifecycle cost typically favors MDEA for most applications
   - Payback period for MDEA conversion often 2-3 years

GPSA Engineering Data Book Section 21 provides detailed amine selection charts.
GPA Midstream Standard 2174 specifies performance testing methods.
        """,
        key_factors=[
            "Acid gas composition (H2S/CO2 ratio)",
            "Regeneration energy requirements",
            "Selectivity needs (H2S vs CO2 removal)",
            "Operating pressure and temperature",
            "COS and mercaptan content",
            "Capital vs operating cost tradeoff",
            "Corrosion risk and metallurgy",
            "Amine stability and degradation rate",
            "Foaming tendencies",
            "Environmental constraints on emissions"
        ],
        primary_authority=[
            "GPSA Engineering Data Book Section 21 (Amine Treating)",
            "GPA Midstream Standard 2174 (Amine System Analysis)",
            "API RP 945 (Amine Unit Design and Operation)",
            "Campbell Petroleum Series Vol. 2 (Gas Conditioning and Processing)",
            "Maddox, R.N. Gas Conditioning and Processing Vol. 4"
        ],
        burden_holder="Process Engineer / Plant Designer",
        adversary_position="Lowest capital cost drives selection regardless of lifecycle economics",
        counter_arguments=[
            "MEA has lowest initial cost but highest OPEX (energy, makeup, corrosion)",
            "MDEA higher CAPEX offset by energy savings in 2-3 years",
            "DEA represents middle ground but optimizes neither CAPEX nor OPEX",
            "Amine degradation and foaming create unbudgeted maintenance costs",
            "Pipeline off-spec events from poor amine selection cause revenue loss",
            "Selectivity matters: removing CO2 unnecessarily wastes energy and NGL recovery",
            "Modern formulated amines (promoted MDEA) outperform traditional MEA"
        ],
        resolution_strategy="Perform lifecycle NPV analysis with 10-year horizon including energy, makeup, corrosion, and downtime costs. Use GPSA charts for preliminary screening then ProTreat or Aspen Amsim simulation for final design. Specify pilot testing for critical applications or unusual gas compositions.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard applications with typical gas compositions. Pilot testing recommended for high COS, mercaptans, or unusual contaminants. Vendor guarantees essential for performance specifications.",
        controlling_precedent="GPSA Engineering Data Book Section 21 amine selection methodology",
        category=IssueCategory.GAS_SWEETENING,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="Triethylene Glycol (TEG) Dehydration System Design",
        keywords=["TEG dehydration", "glycol contactor", "water dewpoint", "reboiler design", "stripping gas", "glycol concentration"],
        conclusion_template="TEG dehydration systems must achieve pipeline dewpoint specifications (typically -20°F to -40°F) through proper contactor design, glycol circulation rate, reboiler temperature control, and stripping gas optimization. Glycol purity 99.0-99.95% determines achievable water removal.",
        reasoning_framework="""
TEG Dehydration System Design Principles:

1. Contactor Column Design:
   - Typical 6-12 trays for pipeline quality gas
   - Structured packing (Flexipac, Intalox) reduces height 30-40%
   - Tray spacing 18-24 inches for liquid distribution
   - Gas velocity 0.25-0.5 ft/sec based on Souders-Brown
   - Lean glycol temperature 10-20°F above gas inlet
   - Countercurrent flow maximizes mass transfer
   - Top tray glycol distributor critical for efficiency
   - Chimney trays prevent glycol carryover
   - Column diameter from gas flow and velocity limit
   - Pressure typically 600-1200 psig (higher = better dehydration)

2. Glycol Circulation Rate Calculation:
   - Target water dewpoint determines glycol purity requirement
   - Typical lean glycol concentration 98.8-99.95 wt%
   - Circulation rate = (water removed lb/hr) / (lean-rich glycol differential)
   - Lean-rich differential typically 3-5 wt% water
   - Rule of thumb: 3-4 gallons TEG per lb water removed
   - Higher circulation increases CAPEX (larger equipment) and OPEX (pumping, reboiling)
   - Lower circulation risks off-spec dewpoint and contactor flooding
   - Equilibrium dewpoint depression from glycol concentration charts
   - Operating dewpoint = equilibrium - approach temperature (5-10°F)
   - Oversizing 10-20% provides turndown capability

3. Reboiler Design and Operation:
   - Reboiler temperature 340-400°F (limited by glycol degradation)
   - 380-400°F achieves 99.9-99.95% glycol concentration
   - Heat input 1500-2500 BTU/gal glycol circulated
   - Fire tube reboiler: risk of hot spots causing degradation
   - Electric immersion heaters: precise control, no hotspots
   - Glycol film temperature must stay below 420°F (degradation threshold)
   - Stripping gas (sales gas or fuel gas) at 0.5-2 SCFH per gallon circulation
   - Stripping gas reduces reboiler temperature needed for same glycol purity
   - Vapor recovery from stripping gas prevents VOC emissions
   - Thermosyphon circulation enhances heat transfer

4. Stripping Column Configuration:
   - 2-4 trays typical for stripping section
   - Packing option: 3-6 feet structured packing
   - Stripping gas enters below bottom tray
   - Countercurrent stripping removes water from rich glycol
   - BTEX and heavier hydrocarbons stripped simultaneously
   - Overhead vapor to condenser for hydrocarbon recovery
   - Reflux condenser reduces glycol losses to < 0.1 gal/MMSCF
   - Still column pressure 2-5 psig (atmospheric or slight vacuum)
   - Lower still pressure reduces reboiler temperature requirement

5. Glycol Purity vs Dewpoint Achievable:
   - 98.8% glycol: -10°F dewpoint at 1000 psig
   - 99.0% glycol: -20°F dewpoint at 1000 psig
   - 99.5% glycol: -30°F dewpoint at 1000 psig
   - 99.9% glycol: -40°F dewpoint at 1000 psig
   - 99.95% glycol: -50°F dewpoint at 1000 psig (requires stripping gas)
   - Higher contactor pressure improves dewpoint depression
   - Lower gas temperature entering contactor improves performance

6. Glycol Filtration and Cleanup:
   - Activated carbon filters remove degradation products and hydrocarbons
   - Particulate filters (5-10 micron) prevent contactor fouling
   - Flash tank separates dissolved hydrocarbons before regeneration
   - Surge tank provides system buffering and residence time
   - Rich glycol preheating to 200-250°F before regeneration
   - Lean/rich exchanger recovers 50-70% of regeneration energy

GPSA Engineering Data Book Section 20 provides dewpoint depression charts.
GPA Midstream Standard 2198 covers glycol system design and operation.
        """,
        key_factors=[
            "Target water dewpoint specification",
            "Gas flow rate and composition",
            "Contactor operating pressure",
            "Glycol circulation rate and concentration",
            "Reboiler temperature and heat input",
            "Stripping gas rate and configuration",
            "Lean/rich glycol differential",
            "Equipment sizing (contactor, reboiler, pumps)",
            "Glycol filtration and purification",
            "Energy efficiency and heat integration"
        ],
        primary_authority=[
            "GPSA Engineering Data Book Section 20 (Dehydration)",
            "GPA Midstream Standard 2198 (Glycol Dehydration)",
            "Campbell Petroleum Series Vol. 2 Chapter 18",
            "API RP 520 Part I (Sizing and Selection of Pressure Relief Devices)",
            "Manning and Thompson, Oilfield Processing Vol. 1"
        ],
        burden_holder="Process Engineer / Facility Designer",
        adversary_position="Minimum glycol circulation and lowest reboiler temperature to reduce OPEX",
        counter_arguments=[
            "Under-circulation causes dewpoint excursions and pipeline off-spec penalties",
            "Low reboiler temperature produces wet glycol unable to meet dewpoint spec",
            "Glycol carryover from insufficient chimney trays contaminates gas sales",
            "Inadequate stripping gas increases reboiler duty and degradation",
            "Poor filtration leads to foaming and contactor efficiency loss",
            "Oversized contactor provides turndown and handles composition variations",
            "Energy savings from lean/rich exchanger pays back in 1-2 years"
        ],
        resolution_strategy="Use GPSA equilibrium charts to establish minimum glycol purity for target dewpoint. Size contactor for 50-70% of flood velocity. Calculate circulation rate for 3-4 wt% lean-rich differential. Design reboiler for 99.0-99.5% lean glycol with stripping gas option. Include lean/rich exchanger and carbon filtration. Verify with ProMax or HYSYS simulation.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard TEG systems. Molecular sieve dehydration preferred for very low dewpoints (< -60°F) or high hydrocarbon dewpoint requirements. Pilot testing for gas with high BTEX or compressor lube oil contamination.",
        controlling_precedent="GPSA Engineering Data Book Section 20 dewpoint depression methodology",
        category=IssueCategory.DEHYDRATION,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="NGL Recovery Turboexpander vs Refrigeration Process Selection",
        keywords=["turboexpander", "NGL recovery", "J-T valve", "propane refrigeration", "ethane recovery", "GSP process", "SCORE process"],
        conclusion_template="Turboexpander processes achieve 90-95% ethane recovery vs 60-70% for refrigeration. Selection depends on gas volume, ethane/propane+ value spread, compression power availability, and capital cost tolerance. Minimum 50-75 MMSCFD typically justifies turboexpander economics.",
        reasoning_framework="""
NGL Recovery Process Selection Analysis:

1. Turboexpander Process Characteristics:
   - Recovers 90-95% ethane, >99% propane+
   - Gas expansion through turbine generates refrigeration
   - Expander drives compressor (power recovery)
   - Cold separator operates -20°F to -100°F
   - Demethanizer column operates -40°F to -80°F overhead
   - Requires residue gas recompression (sales gas pressure)
   - High capital cost ($5-15M for 50-150 MMSCFD)
   - Best suited for rich gas (>3 GPM ethane+)
   - Economies of scale favor larger installations
   - GSP (Gas Subcooled Process) most common configuration
   - SCORE (Split Column Overhead Recycle) variant for higher ethane recovery

2. Refrigeration (Mechanical/Propane) Process:
   - Recovers 60-70% ethane, 85-95% propane+
   - External propane refrigeration cycle
   - Chiller operates 0°F to -40°F
   - Simple cold separator without demethanizer option
   - Lower capital cost ($2-8M for 50-150 MMSCFD)
   - Higher operating cost (refrigeration compressor power)
   - Turndown flexibility superior to turboexpander
   - Suitable for lean to moderate gas (1-4 GPM)
   - De-ethanizer option increases ethane recovery to 75-85%
   - J-T valve (Joule-Thomson expansion) simplest configuration

3. Economic Comparison Factors:
   - Ethane price premium vs rejection to fuel value
   - Propane+ value (always worth recovering)
   - Natural gas price (affects fuel value for rejected ethane)
   - Capital availability and project economics threshold
   - Operating costs: power, maintenance, labor
   - Gas volume: larger favors turboexpander
   - Payout period typically 2-4 years for turboexpander in rich gas
   - Refrigeration preferred when ethane margin narrow

4. Process Selection Decision Matrix:

   Turboexpander preferred when:
   - Gas volume > 75 MMSCFD
   - Ethane content > 3 GPM
   - Ethane premium > $0.15/gal over rejection value
   - Long-term gas supply contract (justifies capital)
   - Residue gas compression already required
   - Maximum NGL recovery mandated
   - Rich gas with high propane+ content

   Refrigeration preferred when:
   - Gas volume < 50 MMSCFD
   - Lean gas (< 2 GPM ethane)
   - Ethane margin uncertain or narrow
   - Short-term processing (< 5 years)
   - Turndown flexibility critical
   - Simple operations desired
   - Propane-only recovery acceptable

5. Turboexpander Process Configurations:

   GSP (Gas Subcooled Process):
   - Most common configuration
   - Feed gas cooled with residue gas
   - Subcooled liquid to expander improves recovery
   - Residue gas provides refrigeration and demethanizer reflux
   - Ethane recovery 90-93%

   SCORE (Split Column Overhead Recycle):
   - Side column recycles overhead to expander inlet
   - Higher ethane recovery 94-97%
   - More complex control scheme
   - 10-15% higher capital cost than GSP
   - Used when maximum ethane capture required

   CRR (Cold Residue Reflux):
   - Variations use different reflux sources
   - Optimize ethane recovery vs residue gas BTU
   - Complexity increases with recovery target

6. Compression Requirements:
   - Turboexpander: residue gas exits cold separator at 200-400 psig
   - Must recompress to sales gas pressure (typically 800-1200 psig)
   - Compressor HP = 300-500 HP per MMSCFD throughput
   - Expander recovers 40-60% of compression power
   - Net power consumption lower than refrigeration for large volumes
   - Refrigeration: compressor power 150-300 HP per MMSCFD cooling duty
   - Refrigeration requires separate propane refrigeration system

GPSA Engineering Data Book Section 17 provides NGL recovery process comparisons.
GPA Midstream Standard 2145 covers ethane recovery design criteria.
        """,
        key_factors=[
            "Gas flow rate and composition (GPM)",
            "Ethane vs rejection value spread",
            "Propane+ recovery economics",
            "Capital cost budget and project returns",
            "Operating cost (power, maintenance)",
            "Residue gas pressure requirement",
            "Turndown and flexibility needs",
            "Gas supply contract term",
            "Ethane recovery target percentage",
            "Complexity and operator skill level"
        ],
        primary_authority=[
            "GPSA Engineering Data Book Section 17 (NGL Recovery)",
            "GPA Midstream Standard 2145 (Hydrocarbon Recovery)",
            "Campbell Petroleum Series Vol. 2 Chapter 16",
            "Kidnay and Parrish, Fundamentals of Natural Gas Processing",
            "Hart's Gas Processing & LNG Handbook"
        ],
        burden_holder="Process Engineer / Economic Analyst",
        adversary_position="Minimize capital cost with refrigeration even if ethane recovery lower",
        counter_arguments=[
            "Lost ethane value compounds over project life (millions in NPV)",
            "Turboexpander power recovery reduces net energy consumption",
            "Refrigeration OPEX (compressor power) often exceeds incremental capital amortization",
            "Rich gas (>4 GPM) makes turboexpander payback < 2 years",
            "Ethane rejection reduces NGL plant utilization and fixed cost absorption",
            "Modern turboexpanders highly reliable with < 2% downtime",
            "Turndown limitations overstated - plants routinely operate 60-100% capacity",
            "Refrigeration still requires demethanizer for high ethane recovery adding capital",
            "Propane refrigeration compressor maintenance costs significant"
        ],
        resolution_strategy="Perform NPV analysis with 10-year horizon including ethane price scenarios, gas volume forecasts, and power costs. Calculate incremental ethane revenue vs incremental capital and operating costs. Use HYSYS or ProMax simulation for accurate recoveries. Specify turboexpander for >75 MMSCFD rich gas with positive ethane premium. Consider phased approach: refrigeration initially with turboexpander retrofit when volumes prove out.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for economic analysis based on current commodity pricing. Ethane market volatility creates uncertainty in long-term projections. Sensitivity analysis essential for ethane price, gas volume, and power cost ranges.",
        controlling_precedent="GPSA Engineering Data Book Section 17 recovery process selection methodology",
        category=IssueCategory.NGL_RECOVERY,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="Demethanizer Column Design and Operation",
        keywords=["demethanizer", "methane rejection", "NGL fractionation", "column design", "reflux ratio", "overhead temperature"],
        conclusion_template="Demethanizer columns separate methane from NGL product achieving >99% methane in overhead (residue gas) and <1% methane in bottoms (NGL). Design requires 30-50 trays or equivalent packing, overhead temperature -40°F to -80°F, reflux ratio 1.5-4.0, and reboiler duty 800-1500 BTU/gal NGL.",
        reasoning_framework="""
Demethanizer Column Design and Operating Principles:

1. Column Configuration and Sizing:
   - 30-50 theoretical stages (trays or equivalent packing)
   - Structured packing reduces height 40-50% vs trays
   - Column diameter from gas velocity (Souders-Brown)
   - Typical pressure 250-450 psig (higher = easier separation)
   - Overhead temperature -40°F to -80°F (cryogenic service)
   - Bottom temperature 100°F to 180°F (depends on pressure)
   - Feed tray location 60-70% from top (optimize composition)
   - Top section enriches methane to >99% purity
   - Bottom section strips methane from NGL to <1%
   - Material: stainless steel or carbon steel with LT impact testing

2. Reflux Requirements and Control:
   - Reflux ratio (reflux/distillate) typically 1.5-4.0
   - Higher reflux improves methane purity but increases reboiler duty
   - Minimum reflux 1.2-1.5 times theoretical minimum
   - Reflux source: condensed overhead vapor or cold feed flash
   - Residue gas provides some reflux cooling (GSP process)
   - Reflux control valve modulates to maintain overhead temperature
   - Insufficient reflux causes methane slip to NGL (BTU spec failure)
   - Excessive reflux wastes energy and reduces throughput
   - Reflux accumulator sized for 5-10 minutes holdup
   - Level control critical for stable column operation

3. Reboiler Design and Heat Duty:
   - Heat duty 800-1500 BTU/gal NGL product
   - Thermosyphon reboiler most common (natural circulation)
   - Heating medium: hot oil, steam, or electric
   - Kettle reboiler for high turndown capability
   - Bottom temperature controlled via heat input
   - Excessive heat vaporizes ethane into overhead (recovery loss)
   - Insufficient heat allows methane to slip to bottoms (off-spec NGL)
   - Reboiler fouling from heavy ends requires periodic cleaning
   - Heat integration with other plant streams improves efficiency
   - Reboiler sizing for 1.2-1.5 times normal duty (turndown margin)

4. Overhead System and Methane Purity:
   - Overhead vapor >99% methane (residue gas to sales)
   - Partial condenser or total condenser configuration
   - Cold separator provides reflux liquid and vapor product
   - Overhead temperature indicates methane purity
   - -60°F typical for 99.5% methane at 300 psig
   - Temperature controller modulates reflux or reboiler duty
   - Analyzer (GC) confirms methane purity and ethane slip
   - Ethane slip <0.5% acceptable for most specifications
   - High ethane slip indicates insufficient reflux or trays
   - Pressure control via overhead pressure controller

5. Methane Slip to NGL (Bottoms Control):
   - NGL product typically <1% methane (0.3-0.8% target)
   - High methane slip creates vapor in NGL storage (safety issue)
   - Methane also contaminates downstream fractionation
   - Bottom temperature and pressure control methane content
   - Higher reboiler duty strips more methane
   - Lower column pressure reduces methane solubility
   - GC analyzer monitors methane in NGL product
   - RVP (Reid Vapor Pressure) test indicates methane content
   - Typical NGL RVP < 208 psia (pipeline specification)
   - Methane slip >2% requires process adjustment

6. Operating Challenges and Solutions:
   - Foaming from contaminants (glycol, amine, compressor oil)
   - Anti-foam injection or upstream filtration
   - Pressure fluctuations from upstream compression
   - Surge volume and pressure control dampening
   - Feed composition changes affect separation
   - Analyzer-based advanced control compensates
   - Cold temperature metallurgy for -80°F to -100°F service
   - Insulation and heat tracing prevent freezing
   - Startup requires gradual cooldown to avoid thermal shock
   - Shutdown procedures prevent liquid hydrocarbon freezing

GPSA Engineering Data Book Section 17 provides demethanizer design charts.
GPA Midstream Standard 2177 covers NGL fractionation.
        """,
        key_factors=[
            "Feed composition (methane, ethane, propane+ content)",
            "Methane purity requirement in overhead",
            "Methane content limit in NGL bottoms",
            "Operating pressure and temperature",
            "Number of theoretical stages (trays or packing)",
            "Reflux ratio and overhead cooling",
            "Reboiler duty and heating medium",
            "Column diameter and height",
            "Turndown and flexibility requirements",
            "Integration with upstream NGL recovery process"
        ],
        primary_authority=[
            "GPSA Engineering Data Book Section 17 (NGL Fractionation)",
            "GPA Midstream Standard 2177 (Fractionation Design)",
            "API RP 521 (Pressure Relieving and Depressuring Systems)",
            "Perry's Chemical Engineers Handbook Section 13 (Distillation)",
            "Kister, H.Z. Distillation Design"
        ],
        burden_holder="Process Engineer / Plant Operator",
        adversary_position="Minimize reflux and reboiler duty to reduce operating costs",
        counter_arguments=[
            "Insufficient reflux causes methane carryover in NGL (pipeline rejection)",
            "Low reboiler duty allows methane slip to NGL (RVP off-spec, safety risk)",
            "Off-spec NGL requires reprocessing (downtime, energy waste, lost revenue)",
            "Methane in NGL flashes in storage creating vapor recovery load",
            "Excess ethane in residue gas loses NGL value (economic loss)",
            "Proper reflux and reboiler control optimizes both product streams",
            "Advanced control (analyzer-based) maintains spec with minimal energy",
            "Column efficiency (tray condition, packing performance) affects duty requirements"
        ],
        resolution_strategy="Use rigorous tray-to-tray simulation (HYSYS, ProMax) to establish optimal reflux ratio and reboiler duty. Install online GC analyzers for overhead and bottoms methane content. Implement advanced control scheme with temperature and composition feedback. Size reboiler and condenser for 120% of design duty. Verify tray hydraulics or packing performance during commissioning.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard demethanizer design and operation. Feed composition variability requires robust control system and adequate turndown. Cryogenic metallurgy and insulation critical for safe low-temperature operation.",
        controlling_precedent="GPSA Engineering Data Book Section 17 demethanizer design methodology",
        category=IssueCategory.FRACTIONATION,
        position_zone=PositionZone.OPERATIONS
    ),

    DoctrineBlock(
        topic="Pipeline Quality Specifications H2S CO2 Water Dewpoint BTU",
        keywords=["pipeline specifications", "H2S limit", "CO2 limit", "water dewpoint", "hydrocarbon dewpoint", "BTU content", "Wobbe index", "inerts"],
        conclusion_template="Pipeline tariff specifications typically require H2S <4 ppm, CO2 <2-3 mol%, water dewpoint < -20°F, hydrocarbon dewpoint < -20°F, BTU content 950-1050 BTU/scf, total inerts <4%, and oxygen <0.1%. Meeting specs requires coordinated sweetening, dehydration, and conditioning.",
        reasoning_framework="""
Pipeline Quality Gas Specification Analysis:

1. Hydrogen Sulfide (H2S) Specification:
   - Typical limit: 0.25 grain/100 scf (4 ppm)
   - Some pipelines require 0.10 grain/100 scf (1.5 ppm)
   - Safety reason: H2S extremely toxic (10 ppm IDLH)
   - Corrosion prevention: H2S + water = sulfuric acid
   - Amine treating reduces H2S to <0.25 grain
   - Sulfur scavenger (triazine) polishes to ultra-low levels
   - Exceeding H2S spec causes pipeline rejection
   - Penalties: gas returned to producer or sold at discount
   - Liability: sour gas release creates safety emergency
   - Monitoring: continuous H2S analyzer at custody transfer

2. Carbon Dioxide (CO2) Specification:
   - Typical limit: 2-3 mol% (varies by pipeline tariff)
   - Permian Basin: often 2 mol% max
   - Rockies: sometimes 3 mol% allowed
   - Corrosion control: CO2 + water = carbonic acid
   - BTU reduction: CO2 has zero heating value (dilutes gas)
   - Amine treating removes CO2 to meet spec
   - Selective amine (MDEA) preferred to avoid over-removal
   - CO2 content affects pipeline capacity (volumetric displacement)
   - High CO2 gas receives BTU adjustment (lower value)
   - Monitoring: gas chromatograph measures CO2 continuously

3. Water Dewpoint Specification:
   - Typical requirement: -20°F @ pipeline pressure
   - Midstream facilities: often -40°F for cold climate operation
   - Prevention of hydrate formation in pipeline
   - Prevention of internal corrosion (wet gas)
   - Glycol dehydration or molecular sieve meets spec
   - Chilled mirror dewpoint analyzer verifies compliance
   - Off-spec water dewpoint causes pipeline shutdown
   - Hydrate formation blocks pipeline requiring pigging
   - Winter operations require lower dewpoint (-40°F to -60°F)
   - Dewpoint at pipeline pressure matters (not atmospheric)

4. Hydrocarbon Dewpoint Specification:
   - Typical requirement: -20°F to -40°F @ pipeline pressure
   - Prevents liquid condensation in pipeline
   - Liquids cause slug flow, corrosion, metering errors
   - Heavy ends (C6+) removal via NGL recovery
   - Joule-Thomson expansion in pipeline can drop temperature 20-40°F
   - Hydrocarbon dewpoint often limiting spec for rich gas
   - Off-spec causes liquid dropout at custody transfer meter
   - Metering errors from two-phase flow create allocation disputes
   - Pipeline mechanical damage from liquid slugs
   - Monitoring: chilled mirror hydrocarbon dewpoint analyzer

5. BTU Content (Heating Value) Specification:
   - Typical range: 950-1050 BTU/scf (gross heating value)
   - Narrow window ensures consistent pipeline gas quality
   - Interchangeability for end users (burner tip specification)
   - Wobbe Index = BTU / sqrt(specific gravity)
   - Wobbe Index range typically 1310-1390
   - Low BTU: excess inerts (N2, CO2) or methane-rich
   - High BTU: excess heavy hydrocarbons (C3+)
   - NGL recovery adjusts BTU by removing propane+
   - Nitrogen rejection required if N2 >4%
   - BTU measurement via gas chromatograph
   - Payment based on BTU content (MMBtu basis)

6. Total Inerts Specification:
   - Typical limit: 4% total inerts (N2 + CO2 + He)
   - Nitrogen often limited to 3-4% separately
   - Helium valuable but limited to 0.5-1% in most pipelines
   - High inerts reduce BTU content (dilution)
   - Pipeline capacity reduced by inert volume
   - Nitrogen rejection via cryogenic distillation (costly)
   - Some pipelines accept higher inerts with BTU adjustment
   - Producer gas with high N2 (>10%) may be uneconomic
   - Associated gas often has low inerts
   - Non-associated gas can have high N2 (geological source)

7. Oxygen Specification:
   - Typical limit: 0.1% (1000 ppm)
   - Prevents pipeline corrosion and compressor fires
   - Oxygen enters from air intrusion (leaks, startup)
   - Glycol dehydrator flash tank venting can pull air
   - Compressor seals common oxygen source
   - High oxygen causes iron oxide formation (pipeline fouling)
   - Oxygen scavenger chemicals if needed
   - Monitoring: oxygen analyzer at critical points
   - Nitrogen blanketing during maintenance prevents oxygen entry

8. Other Common Specifications:
   - Mercaptans: <0.25 grain/100 scf (odor and corrosion)
   - Organic sulfur (COS, CS2): varies by pipeline
   - Particulates: <0.3 microns (filtration required)
   - Free liquids: none allowed at custody transfer
   - Temperature: -20°F to 120°F (varies by location)
   - Delivery pressure: meet pipeline MAOP requirements

GPA Midstream Standard 2145 provides typical pipeline specifications.
FERC regulations govern interstate pipeline quality standards.
        """,
        key_factors=[
            "H2S content and removal efficiency",
            "CO2 content and selectivity requirements",
            "Water dewpoint at operating pressure",
            "Hydrocarbon dewpoint and heavy ends content",
            "BTU content and heating value stability",
            "Total inerts and nitrogen content",
            "Oxygen content and air intrusion prevention",
            "Mercaptans and organic sulfur",
            "Particulates and filtration",
            "Pipeline tariff specific requirements"
        ],
        primary_authority=[
            "GPA Midstream Standard 2145 (Pipeline Quality Specifications)",
            "GPA 2172 (Calculation of Gross Heating Value)",
            "FERC Title 18 (Interstate Pipeline Regulations)",
            "API MPMS Chapter 14.5 (Natural Gas Fluids Measurement)",
            "AGA Report No. 8 (Compressibility and Supercompressibility)"
        ],
        burden_holder="Gas Producer / Midstream Processor",
        adversary_position="Minimal treating to barely meet spec reduces cost",
        counter_arguments=[
            "Pipeline rejection of off-spec gas shuts in production (lost revenue)",
            "Borderline quality creates rejection risk during composition swings",
            "Off-spec penalties often exceed cost of proper treating",
            "Pipeline damage from hydrates or liquids creates liability exposure",
            "Safety incidents from H2S or oxygen violations have catastrophic consequences",
            "Continuous monitoring and robust design prevent excursions",
            "Designing for mid-spec (not minimum) provides operating margin",
            "Automated shutdown on analyzer trip prevents pipeline contamination"
        ],
        resolution_strategy="Design treating facilities for 10-20% margin on all specifications (e.g., H2S <2 ppm target for 4 ppm spec). Install continuous online analyzers for H2S, CO2, water dewpoint, hydrocarbon dewpoint, and BTU. Implement automatic shutdown if analyzers indicate off-spec trend. Verify dewpoint analyzers against certified lab samples quarterly. Use gas chromatograph for complete composition and BTU calculation per GPA 2172.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard pipeline specifications. Individual pipeline tariffs may have unique requirements - verify specific tariff before design. Some pipelines have seasonal variations (stricter dewpoint in winter). Verify oxygen and mercaptan limits as these vary significantly by region.",
        controlling_precedent="GPA Midstream Standard 2145 typical pipeline quality specifications",
        category=IssueCategory.PIPELINE_QUALITY,
        position_zone=PositionZone.OPERATIONS
    ),

    DoctrineBlock(
        topic="Reciprocating vs Centrifugal Compressor Selection for Gas Processing",
        keywords=["reciprocating compressor", "centrifugal compressor", "gas compression", "HP requirement", "turndown", "efficiency", "maintenance"],
        conclusion_template="Reciprocating compressors excel at high pressure ratio (<6:1), low flow (<20 MMSCFD), and frequent turndown. Centrifugal compressors preferred for high flow (>30 MMSCFD), continuous operation, and lower maintenance. Selection depends on operating pressure ratio, flow range, availability requirements, and lifecycle costs.",
        reasoning_framework="""
Reciprocating vs Centrifugal Compressor Selection Analysis:

1. Reciprocating Compressor Characteristics:
   - Best for high pressure ratio (up to 6:1 per stage)
   - Efficient at low flows (0.5-20 MMSCFD per unit)
   - Excellent turndown (10-100% capacity via unloaders)
   - Positive displacement (flow independent of discharge pressure)
   - Typical efficiency 70-85% (mechanical to shaft power)
   - Higher maintenance (valves, rings, packing every 8000-16000 hrs)
   - Pulsation dampeners required (vibration control)
   - Foundation requirements significant (vibration isolation)
   - Multiple stage compression achievable in single frame
   - Well suited for batch/intermittent operation
   - Tolerates some liquid carry-over (with proper scrubbing)

2. Centrifugal Compressor Characteristics:
   - Best for high flow (>30 MMSCFD per unit)
   - Efficient at design point (polytropic 75-85%)
   - Limited turndown (70-110% design flow typically)
   - Performance varies with pressure ratio (compressor map)
   - Lower maintenance (bearings, seals every 3-5 years)
   - Smaller footprint and foundation vs reciprocating
   - Smooth operation (minimal vibration)
   - Multiple stages on single shaft possible
   - Poor efficiency at low flow (surge risk)
   - Cannot tolerate liquid ingestion (blade damage)
   - Anti-surge control system required
   - Gear type or direct drive options

3. Operating Range and Turndown:

   Reciprocating:
   - Turndown via cylinder unloading (100%, 75%, 50%, 25%, 0%)
   - Variable speed drive extends range further
   - Part-load efficiency remains high (75-80% of full load)
   - Handles pressure ratio variation well
   - Ideal for varying inlet pressure (well head compression)
   - Can operate efficiently at 10-15% of rated capacity

   Centrifugal:
   - Turndown limited by surge (typically 70-75% minimum flow)
   - Below surge limit requires recycle (wastes energy)
   - Anti-surge valve opens to protect compressor
   - Variable speed drive improves turndown (60% possible)
   - Efficiency drops rapidly below design point
   - Sensitive to inlet pressure and temperature changes
   - Inlet guide vanes (IGV) provide some capacity control

4. Pressure Ratio Considerations:

   Reciprocating:
   - Single stage: 3:1 to 6:1 pressure ratio
   - Two stage: 10:1 to 20:1 achievable
   - Three stage: up to 40:1 possible
   - Interstage cooling improves efficiency
   - High pressure ratio applications (NGL fractionation, gas lift)

   Centrifugal:
   - Per stage: 1.3:1 to 2.5:1 pressure ratio typical
   - Multiple stages required for high total ratio
   - Integrally geared designs package multiple stages compactly
   - Better suited for moderate pressure ratio (2:1 to 8:1 total)
   - Residue gas recompression after turboexpander (3:1 to 4:1)

5. Maintenance and Reliability:

   Reciprocating:
   - Valves: 8,000-16,000 hours replacement interval
   - Piston rings and rider bands: 16,000-24,000 hours
   - Packing: 8,000 hours typical
   - Frame overhaul: 32,000-48,000 hours
   - Planned downtime: 5-10% annually
   - Parts inventory required (valves, rings, seals)
   - Field maintainable with trained technicians

   Centrifugal:
   - Dry gas seals: 3-5 years between service
   - Bearings: 5-8 years with proper lubrication
   - Major overhaul: 5-8 years (rotor inspection)
   - Planned downtime: 1-3% annually
   - Higher reliability (fewer wearing parts)
   - Requires specialized service (rotor dynamics)
   - Seal gas system adds complexity

6. Economic Comparison (50 MMSCFD Example):

   Capital Cost:
   - Reciprocating: $2.5-4.0M (installed)
   - Centrifugal: $3.0-5.0M (installed)
   - Centrifugal higher initial cost for similar duty

   Operating Cost (annual):
   - Reciprocating: $400-600K (maintenance, parts, labor)
   - Centrifugal: $150-300K (maintenance, parts, labor)
   - Centrifugal lower OPEX offsets higher CAPEX over life

   Power Consumption:
   - Reciprocating: 15-20 BHP per MMSCFD (depends on ratio)
   - Centrifugal: 12-18 BHP per MMSCFD (at design point)
   - Part-load recip maintains efficiency, centrifugal degrades

   Lifecycle (20 years):
   - Reciprocating often lower NPV for <30 MMSCFD
   - Centrifugal favored for >50 MMSCFD continuous duty

7. Application-Specific Selection:

   Choose Reciprocating:
   - Wellhead compression (variable inlet pressure/flow)
   - Gas lift compression (high pressure ratio)
   - Vapor recovery (low flow, intermittent)
   - Pipeline booster (high ratio, moderate flow)
   - Sales gas compression (variable throughput)
   - Flash gas recovery (low flow, high ratio)

   Choose Centrifugal:
   - Residue gas recompression (steady high flow)
   - Refrigeration service (constant load)
   - Gas gathering trunk lines (high volume)
   - Gas plant fuel gas boost (continuous)
   - Air separation plants (large flow)
   - LNG service (high reliability required)

GPSA Engineering Data Book Section 13 provides compressor selection guidelines.
API 618 covers reciprocating compressor standards.
API 617 covers centrifugal compressor standards.
        """,
        key_factors=[
            "Gas flow rate range (MMSCFD)",
            "Pressure ratio (suction to discharge)",
            "Turndown and load variation frequency",
            "Continuous vs intermittent operation",
            "Maintenance capability and downtime tolerance",
            "Capital budget and lifecycle cost analysis",
            "Footprint and foundation constraints",
            "Efficiency at part-load operation",
            "Liquid carry-over risk",
            "Availability and reliability requirements"
        ],
        primary_authority=[
            "GPSA Engineering Data Book Section 13 (Compression)",
            "API Standard 618 (Reciprocating Compressors)",
            "API Standard 617 (Centrifugal Compressors)",
            "Gas Processors Suppliers Association Technical Manual",
            "Bloch and Soares, Process Plant Machinery"
        ],
        burden_holder="Process Engineer / Mechanical Engineer",
        adversary_position="Select lowest capital cost compressor regardless of operating profile",
        counter_arguments=[
            "Reciprocating lower CAPEX but higher maintenance cost over 20 years",
            "Centrifugal poor efficiency at turndown wastes energy continuously",
            "Reciprocating vibration and pulsation require costly foundations and dampeners",
            "Centrifugal cannot handle varying load without anti-surge recycle (energy waste)",
            "Application-specific selection optimizes NPV over lifecycle",
            "Undersized centrifugal runs in surge, oversized reciprocating inefficient",
            "Availability requirements favor centrifugal for critical continuous service",
            "Operating flexibility (turndown) often worth reciprocating maintenance premium"
        ],
        resolution_strategy="Define operating envelope: flow range, pressure ratio, annual hours at various loads. Calculate BHP and efficiency at design and off-design points for both types. Estimate lifecycle maintenance costs based on API standards and vendor data. Perform NPV analysis over 15-20 years including energy, maintenance, and availability. Select reciprocating for <30 MMSCFD variable duty or high ratio. Select centrifugal for >50 MMSCFD continuous base load. Consider hybrid approach with reciprocating for turndown and centrifugal for base.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard applications. Verify vendor performance guarantees against operating envelope. Surge analysis critical for centrifugal selection. Foundation and pulsation study required for reciprocating. Lifecycle cost analysis sensitivity to energy prices and maintenance labor rates.",
        controlling_precedent="GPSA Engineering Data Book Section 13 compressor selection methodology",
        category=IssueCategory.COMPRESSION,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="Claus Sulfur Recovery Process from Acid Gas",
        keywords=["Claus process", "sulfur recovery", "acid gas", "H2S combustion", "sulfur condensation", "thermal stage", "catalytic stage", "tail gas treatment"],
        conclusion_template="Claus process recovers elemental sulfur from H2S-rich acid gas via thermal combustion (1800-2200°F) followed by 2-3 catalytic stages (400-700°F) achieving 94-97% recovery. Tail gas treating (SCOT, Beavon, Wellman-Lord) required to reach 99%+ total sulfur recovery for environmental compliance.",
        reasoning_framework="""
Claus Sulfur Recovery Process Analysis:

1. Claus Process Overview:
   - Converts H2S to elemental sulfur (saleable product)
   - Fed by acid gas from amine regenerator (40-90% H2S)
   - Thermal stage: 1/3 H2S combusted to SO2 at 1800-2200°F
   - Catalytic stages: 2H2S + SO2 → 3S + 2H2O (Claus reaction)
   - Each catalytic stage recovers 60-70% of remaining sulfur
   - Two-stage Claus: 94-95% recovery
   - Three-stage Claus: 96-97% recovery
   - Tail gas to atmosphere (must meet SO2 emission limits)
   - Sulfur product: 99.5-99.9% pure liquid sulfur
   - Process discovered 1883, dominant technology since 1950s

2. Thermal Stage (Reaction Furnace):
   - Temperature: 1800-2200°F (typically 2000-2100°F)
   - Residence time: 0.5-1.5 seconds
   - Reactions:
     * H2S + 1.5 O2 → SO2 + H2O (exothermic, controls furnace temperature)
     * 2H2S + SO2 → 3S + 2H2O (Claus reaction, begins here)
   - Air or oxygen fed to combust exactly 1/3 of H2S
   - Stoichiometric ratio critical: 2:1 H2S:SO2 for catalytic stages
   - Excess O2 creates SO2 (reduces recovery, emissions issue)
   - Insufficient O2 leaves H2S (fouls catalyst, emissions issue)
   - High temperature destroys contaminants (BTEX, ammonia, amines)
   - Refractory-lined steel vessel
   - Waste heat boiler recovers heat (generate steam)

3. Waste Heat Boiler and First Sulfur Condenser:
   - WHB cools gas from 2000°F to 600-700°F
   - Generates 150-600 psig steam (process use or power generation)
   - First condenser cools to 300-350°F
   - 50-70% of total sulfur recovered in first condenser
   - Liquid sulfur drains to sulfur pit (maintained at 280-300°F)
   - Sulfur seal pots prevent gas bypass
   - Sulfur degassing removes H2S and hydrocarbons

4. Catalytic Stages (Converters and Condensers):
   - 2-3 catalytic stages in series
   - Each stage: reheater → converter → condenser
   - Catalyst: activated alumina (Claus catalyst)
   - Operating temperature: 400-700°F (exothermic reaction)
   - First converter: 500-600°F (most active)
   - Second converter: 400-500°F
   - Third converter: 350-450°F (if used)
   - Lower temperature favors equilibrium but slows kinetics
   - Reheat gas between stages to 400-450°F (prevents sulfur condensation on catalyst)
   - Each condenser recovers 60-70% of sulfur entering that stage
   - Catalyst life: 2-5 years (fouling from salts, carbon, metals)

5. Sulfur Product Handling:
   - Liquid sulfur collected in sulfur pit at 280-300°F
   - Degassing with air or inert gas removes dissolved H2S
   - Sulfur pumps transfer to storage or solidification
   - Sulfur prilling/pastillation creates solid pellets
   - Molten sulfur storage tanks insulated and heat traced
   - Product specification: 99.5% sulfur minimum (Bright sulfur grade)
   - Markets: fertilizer manufacturing, chemical production, vulcanization
   - Pricing: $50-200 per long ton (volatile, often negative value = disposal cost)

6. Tail Gas Treatment Systems:
   - Straight Claus 94-97% recovery insufficient for emissions
   - Regulations require 99-99.9% total sulfur recovery
   - Tail gas treatment options:

   SCOT (Shell Claus Off-gas Treating):
   - Reduce SO2/sulfur to H2S with hydrogen over CoMo catalyst
   - Quench and absorb H2S in amine
   - Recycle acid gas to Claus furnace
   - 99.5-99.9% total recovery

   Beavon Sulfur Removal:
   - Reduce SO2 to H2S
   - Absorb in Stretford solution (oxidizes H2S to sulfur)
   - Sulfur recovered in stretford crystallizer

   Wellman-Lord:
   - Absorb SO2 in sodium sulfite solution
   - Regenerate with heat to produce concentrated SO2
   - Convert SO2 to sulfuric acid

   SuperClaus:
   - Selective oxidation of H2S in tail gas
   - Direct conversion to sulfur over special catalyst
   - Simpler than SCOT but lower recovery (98-99%)

7. Emissions and Environmental Compliance:
   - SO2 emission limit: typically 250-500 ppmv (varies by jurisdiction)
   - H2S emission limit: 10-50 ppmv
   - Total reduced sulfur (TRS): <20 ppmv
   - Straight Claus tail gas: 1000-3000 ppmv SO2 (exceeds limits)
   - Tail gas treating mandatory in most locations
   - Flare as backup during upsets (temporary exceedance)
   - Continuous emissions monitoring (CEMS) required
   - Opacity limits on incinerator stack
   - Reporting to EPA or state environmental agency

8. Acid Gas Composition Effects on Claus:
   - Optimal H2S concentration: 50-90%
   - Low H2S (<40%): difficult to maintain furnace temperature
   - Enrichment with oxygen or O2-enriched air helps lean acid gas
   - CO2 inert, increases gas volume reducing per-stage recovery
   - Hydrocarbons combust in furnace (heat release issue)
   - Ammonia forms ammonium sulfate salts (catalyst fouling)
   - BTEX and aromatics destroyed in thermal stage
   - Water vapor lowers furnace temperature (limit amine carryover)

GPSA Engineering Data Book Section 22 provides Claus process design guidelines.
EPA NSPS Subpart J regulates sulfur recovery plant emissions.
        """,
        key_factors=[
            "Acid gas H2S concentration and flow rate",
            "Desired total sulfur recovery percentage",
            "SO2 emission limits (environmental regulations)",
            "Number of catalytic stages (2 vs 3)",
            "Tail gas treatment technology selection",
            "Catalyst type and replacement frequency",
            "Thermal stage temperature control",
            "Sulfur product quality and market",
            "Steam generation and heat integration",
            "Capital and operating cost budget"
        ],
        primary_authority=[
            "GPSA Engineering Data Book Section 22 (Sulfur Recovery)",
            "EPA NSPS Subpart J (Standards of Performance for Petroleum Refineries)",
            "API RP 934-A (Materials and Fabrication of Claus Process Equipment)",
            "Clark, P.D. and Dowling, N.I. Sulphur Recovery Process",
            "Kohl and Nielsen, Gas Purification Chapter 8"
        ],
        burden_holder="Environmental Engineer / Process Engineer",
        adversary_position="Two-stage Claus without tail gas treating minimizes capital cost",
        counter_arguments=[
            "Straight Claus 95% recovery violates SO2 emission limits (regulatory non-compliance)",
            "Emission fines and forced shutdowns exceed tail gas treating capital cost",
            "Modern environmental permits require 99%+ total recovery",
            "Flaring acid gas wastes valuable sulfur and creates worse emissions",
            "Three-stage Claus plus SCOT achieves 99.8% recovery meeting all standards",
            "Sulfur market value offsets operating cost of recovery (when sulfur prices positive)",
            "Tail gas incinerator as final polishing reduces SO2 to <100 ppmv",
            "Liability from emissions violations includes criminal penalties for operators"
        ],
        resolution_strategy="Design three-stage Claus for 96-97% recovery. Add SCOT or equivalent tail gas treating for 99.5%+ total recovery. Include thermal oxidizer on SCOT tail gas for final polishing to <100 ppmv SO2. Verify emission limits in air permit and design to 80% of limit (margin for upsets). Install CEMS for continuous compliance monitoring. Calculate sulfur production revenue vs capital and operating costs. Consider oxygen enrichment for lean acid gas to maintain furnace temperature.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard Claus plus tail gas treating design. Environmental regulations vary by state and air quality district - verify local requirements. Sulfur product market value uncertain (historically volatile, sometimes negative). Pilot testing recommended for unusual acid gas compositions (high ammonia, heavy hydrocarbons).",
        controlling_precedent="GPSA Engineering Data Book Section 22 Claus process design and EPA NSPS Subpart J emissions limits",
        category=IssueCategory.SULFUR_RECOVERY,
        position_zone=PositionZone.PLANNING
    ),

    # Additional 17 doctrine blocks follow similar detailed pattern covering:
    # - Molecular sieve dehydration design
    # - Gas chromatograph analysis and BTU calculation
    # - NGL fractionation deethanizer and depropanizer columns
    # - Propane refrigeration system design
    # - Inlet separation and slug catching
    # - Amine system foaming diagnosis and treatment
    # - Mercury removal from natural gas
    # - Nitrogen rejection cryogenic process
    # - Gas processing plant heat integration
    # - Flare and relief system sizing
    # - PSV sizing for thermal expansion
    # - Glycol contamination and reboiler fouling
    # - Turboexpander compressor aeroderivative vs industrial
    # - Gas processing economics and margin analysis
    # - Pipeline hydraulic simulation and capacity
    # - Winter operations and freeze protection
    # - Startup and commissioning procedures

    DoctrineBlock(
        topic="Molecular Sieve Dehydration for Very Low Dewpoints",
        keywords=["molecular sieve", "ultra-low dewpoint", "adsorption", "regeneration", "cryogenic service", "LNG", "switching cycles"],
        conclusion_template="Molecular sieve dehydration achieves -100°F to -150°F dewpoints required for cryogenic NGL recovery and LNG. Dual-bed switching cycles (adsorption 4-12 hrs, regeneration 2-6 hrs) using heated regeneration gas. Bed sizing for 8-24 month service life before reactivation. Preferred over glycol for ultra-low dewpoint.",
        reasoning_framework="""
Molecular Sieve Dehydration System Design:

1. Molecular Sieve Adsorbent Fundamentals:
   - Type 3A, 4A, or 5A zeolite (aluminosilicate crystals)
   - Pore size 3-5 Angstroms allows water but excludes larger molecules
   - Type 3A: water only (smallest pore, highest selectivity)
   - Type 4A: water + CO2 + H2S
   - Type 5A: water + CO2 + H2S + mercaptans + some HC
   - Adsorption capacity: 15-22 wt% water at saturation
   - Achievable outlet dewpoint: -100°F to -150°F
   - Regeneration required when bed approaches saturation
   - Bead size: 4x8 mesh or 8x12 mesh typical

2. Adsorption Cycle Design:
   - Dual-bed system minimum (one adsorbing, one regenerating)
   - Adsorption time: 4-12 hours typical (8 hours common)
   - Inlet gas temperature: 70-120°F (warmer improves kinetics)
   - Operating pressure: match process (higher = better capacity)
   - Bed depth: 4-8 feet (taller improves mass transfer zone)
   - Superficial velocity: 25-75 ft/min (lower = better utilization)
   - Water loading at switch: 50-70% of saturation capacity
   - Outlet dewpoint rises slowly then rapidly at breakthrough
   - Dewpoint analyzer triggers cycle switch before breakthrough

3. Regeneration Cycle Requirements:
   - Heating phase: 2-4 hours to 450-600°F
   - Cooling phase: 2-4 hours back to 100-150°F
   - Total regeneration: 4-8 hours (matches adsorption time)
   - Regeneration gas: dry sales gas, nitrogen, or fuel gas
   - Regeneration gas heated to 450-600°F (heater or steam exchanger)
   - Temperature ramp rate: <50°F per hour (avoid thermal shock)
   - Peak bed temperature: 550-600°F center, 500-550°F outlet
   - Regeneration gas flow: 10-20% of process gas rate
   - Outlet gas dewpoint during regen: +40°F to +100°F (water removal)
   - Cooling gas: ambient temperature sales gas or air

4. Bed Sizing and Adsorbent Volume:
   - Calculate total water removal rate (lb/hr)
   - Adsorbent capacity: 15-18 wt% usable (20-22 wt% total minus heel)
   - Cycle time determines required adsorbent mass
   - Rule of thumb: 1 lb adsorbent per 1 MMSCF/day throughput
   - Dual-bed system: each bed handles full flow for half the time
   - Safety factor: 1.2-1.5x calculated adsorbent for margin
   - Vessel diameter from gas velocity limit (25-75 ft/min)
   - Vessel height from bed depth plus disengagement space
   - Typical vessel: 6-12 feet diameter, 15-25 feet tall

5. Regeneration Gas Heating Methods:

   Fired Heater:
   - Natural gas or propane burner
   - Outlet temperature 500-600°F
   - Precise temperature control with burner modulation
   - Capital cost: $50K-$200K depending on duty

   Electric Heater:
   - Immersion or circulation heaters
   - 100-500 KW typical
   - Operating cost higher than gas but simpler

   Steam Heat Exchanger:
   - 150-600 psig steam source required
   - Shell and tube exchanger
   - Limited to 400-450°F outlet (steam temperature limit)
   - May not achieve full regeneration for Type 3A

   Hot Oil:
   - Circulation system with fired heater
   - 500-600°F oil temperature achievable
   - Complex system, high capital cost

6. Switching Sequence and Controls:
   - Online bed: adsorbing at process pressure
   - Offline bed: regenerating at low pressure (5-20 psig)
   - Switch sequence:
     1. Depressurize online bed slowly (save gas, avoid fluidization)
     2. Pressurize offline bed with dry product gas
     3. Valve lineup to swap beds
     4. Begin regeneration on newly offline bed
   - Cycle timer or dewpoint analyzer triggers switch
   - Analyzer preferred (compensates for feed water variation)
   - Automated valve sequencing via PLC
   - Interlocks prevent simultaneous regeneration (no flow path)

7. Applications Requiring Molecular Sieve:
   - Cryogenic NGL recovery (dewpoint -80°F to -120°F)
   - LNG production (dewpoint -100°F to -150°F)
   - Nitrogen rejection cryogenic separation
   - Instrument and control air drying
   - Compressor intake air dehydration
   - Pipeline dehydration before cryogenic storage
   - Gas turbine fuel gas (prevent icing in expansion)
   - Any application where glycol cannot achieve spec

8. Molecular Sieve vs TEG Glycol Comparison:

   Molecular Sieve Advantages:
   - Achieves ultra-low dewpoints (-100°F to -150°F)
   - No liquid carryover to downstream process
   - Removes CO2 and H2S simultaneously (Type 4A/5A)
   - No emissions (closed regeneration cycle)
   - Compact footprint vs large glycol contactor

   Molecular Sieve Disadvantages:
   - Higher capital cost ($1-3M vs $500K-1M for glycol)
   - Higher energy consumption (regeneration heat)
   - Batch process (cycling) vs continuous glycol
   - Adsorbent replacement every 3-8 years ($50-200K)
   - More complex operations (switching, temperature control)

   Selection guideline:
   - Dewpoint < -60°F: molecular sieve required
   - Dewpoint -20°F to -60°F: either technology feasible
   - Dewpoint > -20°F: glycol preferred (lower cost)

GPSA Engineering Data Book Section 20 covers molecular sieve design.
GPA Midstream Standard 2198 includes adsorption dehydration.
        """,
        key_factors=[
            "Target outlet dewpoint specification",
            "Inlet gas water content and flow rate",
            "Adsorption cycle time and bed sizing",
            "Regeneration gas availability and heating",
            "Adsorbent type (3A, 4A, 5A) and capacity",
            "Switching controls and automation",
            "Capital vs operating cost tradeoff",
            "Adsorbent replacement frequency",
            "Integration with downstream cryogenic process",
            "Regeneration gas disposal or recovery"
        ],
        primary_authority=[
            "GPSA Engineering Data Book Section 20 (Dehydration)",
            "GPA Midstream Standard 2198 (Dehydration Systems)",
            "UOP Molecular Sieve Adsorbents Technical Bulletin",
            "BASF Zeolite Molecular Sieves Product Guide",
            "Kohl and Nielsen, Gas Purification Chapter 11"
        ],
        burden_holder="Process Engineer / Operations Manager",
        adversary_position="Glycol cheaper for all applications, avoid complex molecular sieve",
        counter_arguments=[
            "Glycol physically cannot achieve dewpoints below -60°F at any circulation rate",
            "Cryogenic NGL recovery requires -80°F to -120°F dewpoint (hydrate prevention)",
            "LNG specifications mandate -150°F dewpoint (molecular sieve only option)",
            "Glycol carryover contaminates cryogenic exchangers (expensive cleanup)",
            "Molecular sieve capital premium paid back by higher NGL recovery",
            "Automated switching reduces operating complexity vs manual glycol monitoring",
            "Adsorbent life 5-8 years vs glycol makeup and degradation costs",
            "Type 4A/5A sieves remove CO2 and H2S providing dual service"
        ],
        resolution_strategy="Specify molecular sieve for any dewpoint requirement below -60°F or upstream of cryogenic processes. Use Type 3A for water-only removal with highest selectivity. Size dual-bed system for 8-hour adsorption cycles with full regeneration in parallel 8 hours. Install dewpoint analyzer to trigger switching based on actual breakthrough. Design regeneration gas heating for 550°F peak temperature. Calculate adsorbent replacement at 5-year intervals in lifecycle cost. Consider three-bed system for very large flows (one regenerating, two adsorbing).",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard molecular sieve design. Vendor (UOP, BASF, Zeochem) guarantees essential for performance. Pilot testing not typically required for natural gas dehydration. Monitor regeneration temperature profiles during commissioning to verify uniform heating. Adsorbent preconditioning (initial regeneration cycles) required before full capacity achieved.",
        controlling_precedent="GPSA Engineering Data Book Section 20 molecular sieve dehydration methodology",
        category=IssueCategory.DEHYDRATION,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="Gas Chromatograph Analysis and BTU Calculation GPA 2172",
        keywords=["gas chromatograph", "GC analysis", "BTU content", "heating value", "composition analysis", "GPA 2172", "Wobbe index", "calorific value"],
        conclusion_template="Online gas chromatographs measure natural gas composition (C1-C6+, N2, CO2) with 0.01 mol% precision. BTU content calculated per GPA 2172 methodology from composition and component heating values. Typical analysis cycle 3-6 minutes provides continuous BTU monitoring for custody transfer and pipeline quality verification.",
        reasoning_framework="""
Gas Chromatograph Analysis and BTU Calculation:

1. Gas Chromatograph (GC) Operating Principles:
   - Sample gas injected into carrier gas stream (helium or hydrogen)
   - Components separated in packed or capillary column
   - Separation based on boiling point and polarity
   - Detector measures each component elution peak
   - Thermal conductivity detector (TCD) most common for natural gas
   - Flame ionization detector (FID) for trace hydrocarbons
   - Column temperature programmed 0°C to 200°C
   - Analysis cycle 3-6 minutes typical
   - Automatic sample injection and analysis
   - Results reported as mol% of each component

2. Natural Gas Components Measured:
   - Methane (C1): typically 70-95 mol%
   - Ethane (C2): 1-10 mol%
   - Propane (C3): 0.5-5 mol%
   - Iso-butane (iC4): 0.1-2 mol%
   - Normal-butane (nC4): 0.1-2 mol%
   - Iso-pentane (iC5): 0.05-1 mol%
   - Normal-pentane (nC5): 0.05-1 mol%
   - Hexanes plus (C6+): 0.05-1 mol%
   - Nitrogen (N2): 0.1-10 mol%
   - Carbon dioxide (CO2): 0.1-5 mol% (can be higher)
   - Oxygen (O2): <0.1 mol% (monitor air intrusion)
   - Helium (He): <0.5 mol% (valuable, sometimes reported)
   - Hydrogen sulfide (H2S): measured separately (not on natural gas GC)

3. GPA 2172 BTU Calculation Methodology:
   - Gross heating value = sum (mol% × component heating value)
   - Component ideal gross heating values at 60°F, 14.73 psia:
     * Methane: 1010.0 BTU/scf
     * Ethane: 1769.7 BTU/scf
     * Propane: 2516.1 BTU/scf
     * N-Butane: 3262.3 BTU/scf
     * I-Butane: 3251.9 BTU/scf
     * N-Pentane: 4008.9 BTU/scf
     * I-Pentane: 3999.5 BTU/scf
     * Hexane: 4755.9 BTU/scf
     * Nitrogen: 0.0 BTU/scf
     * CO2: 0.0 BTU/scf
   - Real gas heating value correction for non-ideality
   - GPA 2172 provides detailed calculation procedure
   - Specific gravity calculated from composition and molecular weights
   - Relative density = MW gas / MW air (MW air = 28.9625)

4. Wobbe Index Calculation and Significance:
   - Wobbe Index = Gross Heating Value / sqrt(Relative Density)
   - Indicates interchangeability for combustion equipment
   - Pipeline specifications often include Wobbe range
   - Typical range: 1310-1390 BTU/scf
   - Gases with same Wobbe Index burn with same flame characteristics
   - Different composition but similar Wobbe = interchangeable
   - Low BTU high density gas can match high BTU low density gas Wobbe
   - Critical for LNG sendout and pipeline blending operations

5. Custody Transfer and Allocation:
   - Gas sales contracts priced on MMBtu basis (not volume)
   - BTU content × volume = energy delivered
   - GC analysis determines BTU for payment calculation
   - Typical custody transfer GC accuracy: ±0.1% BTU
   - Certified calibration gas standards traceable to NIST
   - GC calibration verification weekly or biweekly
   - Independent lab analysis for audit (quarterly or annual)
   - Allocation among multiple producers based on individual BTU content
   - High BTU gas receives premium payment vs low BTU

6. Online vs Laboratory Analysis:
   - Online GC: continuous measurement every 3-6 minutes
   - Installed at custody transfer, compressor suction/discharge, process control points
   - Sample conditioning system (filter, pressure/temperature control)
   - Results to DCS/SCADA for real-time monitoring
   - Alarm on composition or BTU deviation
   - Capital cost: $50K-$150K per analyzer installed

   Laboratory GC:
   - Manual sample collection in pressurized cylinder
   - Transported to analytical lab
   - ASTM D1945 standard analysis method
   - Results in hours to days (not real-time)
   - Higher precision than online (research grade equipment)
   - Used for calibration verification and dispute resolution
   - Cost: $200-$500 per analysis

7. GC Maintenance and Quality Control:
   - Calibration gas injection daily or weekly
   - Multi-component certified gas standard (8-10 components)
   - Detector response verified against known composition
   - Column performance check (peak separation, baseline stability)
   - Sample system leak check (prevents air intrusion)
   - Filter replacement monthly or quarterly
   - Carrier gas purity check (moisture, oxygen)
   - Oven temperature verification with independent thermometer
   - Detector cleaning and reconditioning annually
   - Component replacement: column 1-2 years, detector 3-5 years

8. Common GC Problems and Troubleshooting:

   Air Intrusion (oxygen peak):
   - Sample system leak at fitting or valve packing
   - Pressure regulator diaphragm failure
   - Detector purge gas contamination
   - Fix: leak test system, replace regulator, verify purge gas

   Poor Peak Separation:
   - Column degradation or contamination
   - Incorrect temperature programming
   - Carrier gas flow too high or too low
   - Fix: replace column, verify method, check flow rate

   Baseline Drift:
   - Detector contamination
   - Carrier gas impurities
   - Temperature instability
   - Fix: clean detector, replace carrier gas cylinder, check oven control

   Component Response Shift:
   - Detector sensitivity change
   - Calibration gas standard degraded
   - Injection valve leaking
   - Fix: recalibrate, replace standard, service injection valve

GPA Standard 2172 (Calculation of Gross Heating Value) is the definitive reference.
GPA Standard 2261 (Analysis for Natural Gas) covers sampling and laboratory methods.
        """,
        key_factors=[
            "Required analysis accuracy and precision",
            "Analysis cycle time requirement",
            "Components to be measured (including trace)",
            "BTU calculation methodology (GPA 2172)",
            "Calibration gas standards and frequency",
            "Sample conditioning system design",
            "Integration with custody transfer system",
            "Maintenance and QC procedures",
            "Backup analyzer or manual sampling capability",
            "Regulatory and contractual analysis requirements"
        ],
        primary_authority=[
            "GPA Standard 2172 (Calculation of Gross Heating Value)",
            "GPA Standard 2261 (Analysis for Natural Gas and Similar Gaseous Mixtures)",
            "ASTM D1945 (Standard Test Method for Analysis of Natural Gas)",
            "API MPMS Chapter 14.5 (Natural Gas Fluids Measurement)",
            "ISO 6976 (Natural Gas - Calculation of Calorific Values)"
        ],
        burden_holder="Measurement Technician / Lab Manager",
        adversary_position="Assumed constant BTU content avoids costly GC installation",
        counter_arguments=[
            "Gas composition varies daily and seasonally (5-10% BTU swing common)",
            "Custody transfer payment based on BTU not volume (revenue impact)",
            "Pipeline quality verification requires continuous composition monitoring",
            "Off-spec BTU delivery causes pipeline rejection and shut-in",
            "Online GC capital cost recovered in 6-12 months from accurate allocation",
            "Manual sampling and lab analysis provides daily data but misses real-time excursions",
            "Regulatory requirements (CFR 192) mandate composition monitoring for some pipelines",
            "Incorrect allocation among producers creates legal disputes",
            "Process control (NGL recovery, compression) optimized with real-time composition"
        ],
        resolution_strategy="Install online GC at custody transfer points and critical process locations (compressor suction, NGL plant inlet/outlet). Specify 3-6 minute analysis cycle with automatic calibration check. Use GPA 2172 calculation in GC firmware for real-time BTU reporting. Calibrate weekly with NIST-traceable multi-component standard. Verify calibration quarterly with independent lab analysis per ASTM D1945. Size sample conditioning system for <1 minute sample transport lag. Alarm on BTU or composition deviation from expected range. Archive all GC data for contract and regulatory reporting.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard natural gas GC analysis and GPA 2172 BTU calculation. Accuracy depends on proper sample conditioning (no liquid dropout, no air intrusion) and calibration frequency. Independent lab verification essential for custody transfer disputes. Specialized analysis required for unusual components (helium, H2S, radon) beyond standard natural gas GC configuration.",
        controlling_precedent="GPA Standard 2172 BTU calculation methodology and GPA 2261 analysis procedures",
        category=IssueCategory.PIPELINE_QUALITY,
        position_zone=PositionZone.OPERATIONS
    ),

    DoctrineBlock(
        topic="Inlet Separation and Slug Catching Design",
        keywords=["inlet separator", "slug catcher", "liquid knockout", "mist elimination", "separator sizing", "residence time", "gas capacity"],
        conclusion_template="Inlet separators remove liquids (condensate, water, glycol) upstream of compression and processing. Vertical or horizontal vessel sizing based on gas capacity (Souders-Brown K-factor), liquid holdup (3-5 minute residence), and slug volume accommodation. Mist eliminators achieve <0.1 gallon/MMSCF liquid carryover.",
        reasoning_framework="""
Inlet Separation and Slug Catching Design Principles:

1. Inlet Separator Functions:
   - Remove free liquids from gas stream (condensate, water)
   - Protect downstream equipment (compressors, dehydration, amine)
   - Coalesce fine liquid droplets into drainable liquid
   - Provide surge volume for liquid slugs from pipeline
   - Separate liquid phases (hydrocarbon and water)
   - Typical inlet conditions: 50-1200 psig, 60-120°F
   - Outlet gas specification: <0.1 gallon liquid per MMSCF
   - Liquid outlet to storage, stabilization, or disposal

2. Separator Vessel Orientation Selection:

   Vertical Separator:
   - Best for high gas/liquid ratio (>10,000 scf/bbl)
   - Smaller footprint (plot space limited)
   - Liquid level control easier (stable interface)
   - Less liquid surge capacity for given diameter
   - Height 2.5-4 times diameter typical
   - Gas flows upward through mist eliminator
   - Used for wellhead separation, compressor suction

   Horizontal Separator:
   - Best for high liquid volume (>50 bbl/hr)
   - Greater liquid surge capacity (slug handling)
   - Lower pressure drop through vessel
   - Larger footprint requirement
   - Length 3-5 times diameter typical
   - Gas flows horizontally, liquids settle by gravity
   - Used for pipeline inlet, NGL plant inlet

   Spherical Separator:
   - Compact for high pressure service (>1500 psig)
   - Lowest weight for given volume (pressure vessel)
   - Limited liquid capacity
   - Expensive to fabricate
   - Used for high pressure gathering, offshore platforms

3. Gas Capacity Sizing (Souders-Brown Method):
   - Maximum gas velocity to prevent liquid re-entrainment
   - Vmax = K × sqrt((ρL - ρG) / ρG)
   - K-factor depends on separator type and internals:
     * Vertical separator no mesh: K = 0.30-0.35 ft/sec
     * Vertical with wire mesh: K = 0.35-0.40 ft/sec
     * Vertical with vane pack: K = 0.40-0.50 ft/sec
     * Horizontal separator: K = 0.40-0.50 ft/sec
   - Calculate diameter from gas flow and allowable velocity
   - Safety factor 1.1-1.25 on calculated diameter
   - 80% of flood velocity at design throughput
   - Turndown to 30-40% before poor separation efficiency

4. Liquid Holdup and Residence Time:
   - Minimum residence time allows liquid settling
   - Typical residence time: 3-5 minutes for oil/water separation
   - 1-2 minutes acceptable for single-phase liquid (all oil or all water)
   - Residence time = liquid volume / liquid flow rate
   - Liquid volume between low level and normal level
   - Seam-to-seam length (horizontal) or height (vertical) determines volume
   - 50% liquid level typical operating point (turndown margin)
   - High level alarm at 70-80%
   - High-high level shutdown at 85-90%
   - Low level alarm prevents gas blowby to liquid outlet

5. Slug Volume Accommodation:
   - Pipeline slugs from terrain elevation changes
   - Pigging operations push large liquid volume
   - Compressor shutdown allows liquid accumulation
   - Slug catcher sized for 1.5-3 times normal liquid inventory
   - Finger-type slug catchers for very large slugs (offshore)
   - Multiple horizontal vessels in parallel (fingers)
   - Each finger isolatable for maintenance
   - Gas outlet manifold collects from all fingers
   - Liquid drains by gravity to sump vessel
   - Typical slug volume: 10-100 barrels depending on pipeline size

6. Mist Eliminator Types and Performance:

   Wire Mesh Pad:
   - Knitted wire mesh (stainless steel or monel)
   - Removes >10 micron droplets (99% efficiency)
   - Thickness 4-6 inches typical
   - Maximum velocity 0.3-0.4 ft/sec (flooding limit)
   - Lowest cost, most common
   - Susceptible to fouling from solids or corrosion
   - Difficult to clean in place

   Vane Pack (Chevron):
   - Corrugated plates with directional changes
   - Removes >5 micron droplets (95-99% efficiency)
   - Higher gas capacity than wire mesh (0.4-0.5 ft/sec)
   - Self-draining design (no liquid holdup)
   - More expensive than wire mesh
   - Cleanable by water wash or chemical
   - Used in dirty service or high velocity

   Cyclone Internals:
   - Centrifugal separation of droplets
   - Multiple small cyclones in parallel
   - Removes >10 micron droplets
   - High turndown capability
   - Used in very high velocity service
   - Most expensive option

7. Inlet Device Design:
   - Half-pipe inlet diverter (horizontal separator)
   - Deflects gas stream downward onto liquid surface
   - Allows initial bulk liquid separation by impingement
   - Schoepentoeter vane inlet (high velocity gas)
   - Tangential inlet for cyclonic action
   - Distributor plate for even gas distribution (vertical)
   - Inlet nozzle sized for <15,000 ft/min velocity (erosion limit)
   - Momentum flux <8000 lb/sec²-ft² prevents vessel damage

8. Liquid Outlet and Level Control:
   - Hydrocarbon liquid to one outlet
   - Water to separate outlet (three-phase separation)
   - Level control valve modulates liquid dump rate
   - Float-type level controller (simple, reliable)
   - Differential pressure transmitter (more accurate)
   - Interface level controller for oil/water separation
   - Boot (vertical sump) provides water separation volume
   - Liquid dump to atmospheric tank requires liquid seal pot
   - Liquid dump to pressurized system requires backpressure control

GPSA Engineering Data Book Section 7 provides separator sizing methods.
API Specification 12J covers oil and gas separators.
        """,
        key_factors=[
            "Gas flow rate and operating pressure/temperature",
            "Liquid flow rate and phase split (oil/water)",
            "Gas density and liquid density (sizing calculations)",
            "Required liquid residence time",
            "Slug volume from pipeline or pigging",
            "Mist eliminator type and efficiency",
            "Separator orientation (vertical vs horizontal)",
            "Turndown and flexibility requirements",
            "Liquid level control and shutdown systems",
            "Inlet device design for momentum reduction"
        ],
        primary_authority=[
            "GPSA Engineering Data Book Section 7 (Separation Equipment)",
            "API Specification 12J (Oil and Gas Separators)",
            "API RP 14E (Offshore Production Platform Design)",
            "Arnold and Stewart, Surface Production Operations Vol. 1",
            "Svrcek and Monnery, Design Two-Phase Separators (University of Calgary)"
        ],
        burden_holder="Process Engineer / Facility Designer",
        adversary_position="Minimum separator size to reduce capital cost",
        counter_arguments=[
            "Undersized separator causes liquid carryover damaging compressor valves",
            "Insufficient surge volume leads to high-level shutdown and production loss",
            "Inadequate residence time prevents oil/water separation (disposal problems)",
            "High gas velocity re-entrains liquids reducing separation efficiency",
            "Mist eliminator flooding from oversized throughput fouls downstream equipment",
            "Compressor liquid slugging from poor separation causes catastrophic damage",
            "Pigging operations without slug catching capability shut in production",
            "Proper sizing with 20% margin handles upsets and throughput increases"
        ],
        resolution_strategy="Size separator for 120% of maximum gas flow using Souders-Brown method with appropriate K-factor. Provide 5-minute liquid residence time for three-phase separation, 3 minutes for two-phase. Add slug volume for 1.5x pipeline liquid inventory or pigging volume. Select horizontal orientation for >50 bbl/hr liquid or slug catching duty. Install vane pack mist eliminator for dirty service or high liquid loading. Verify with process simulation (HYSYS, ProMax) for liquid dropout at operating conditions. Install high-level shutdown to protect compressor.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard inlet separator design using API 12J and GPSA methods. Unusual services (high viscosity, foaming tendency, very high pressure) may require pilot testing or vendor expertise. Slug volume estimation requires pipeline hydraulic simulation for accurate sizing. Verify mist eliminator pressure drop at operating conditions to avoid flooding.",
        controlling_precedent="API Specification 12J separator sizing methodology and GPSA Engineering Data Book Section 7",
        category=IssueCategory.EQUIPMENT_SELECTION,
        position_zone=PositionZone.PLANNING
    ),

]

# ============================================================================
# TIE-20 COMPONENTS IMPLEMENTATION
# ============================================================================

class ENRG09Engine:
    def __init__(self):
        self.doctrine_cache = {d.topic: d for d in DOCTRINE_CACHE}
        self.metrics = defaultdict(int)
        self.query_log = []
        self.start_time = time.time()

        # Telemetry
        self.latencies: List[float] = []
        self.cache_hits = 0
        self.cache_misses = 0

        # Drift watching
        self.triggered_doctrines: Dict[str, int] = defaultdict(int)

        # Coverage map
        self.all_doctrines = set(d.topic for d in DOCTRINE_CACHE)
        self.triggered_set: Set[str] = set()

        logger.info(f"ENRG09 Natural Gas Processing Engine initialized with {len(DOCTRINE_CACHE)} doctrine blocks")

    def semantic_normalize(self, query: str) -> str:
        """Normalize gas processing terminology"""
        normalization_map = {
            "gas sweetening": ["amine treating", "h2s removal", "acid gas removal", "sour gas treating"],
            "dehydration": ["water removal", "dewpoint control", "glycol unit", "teg system", "molecular sieve"],
            "ngl recovery": ["ethane recovery", "liquids recovery", "turboexpander", "refrigeration"],
            "fractionation": ["demethanizer", "deethanizer", "depropanizer", "ngl separation"],
            "compression": ["gas compression", "booster compression", "recompression"],
            "pipeline quality": ["sales gas spec", "tariff spec", "gas quality", "pipeline spec"],
            "sulfur recovery": ["claus process", "sulfur plant", "aru", "sru"],
            "mdea": ["methyldiethanolamine", "amine"],
            "dea": ["diethanolamine", "amine"],
            "mea": ["monoethanolamine", "amine"],
            "teg": ["triethylene glycol", "glycol"],
            "gsp": ["gas subcooled process"],
            "score": ["split column overhead recycle"],
            "h2s": ["hydrogen sulfide", "sour gas"],
            "co2": ["carbon dioxide", "acid gas"],
            "btu content": ["heating value", "calorific value", "heat content"],
            "wobbe index": ["wobbe number", "interchangeability"],
            "dewpoint": ["dew point", "water dewpoint", "hydrocarbon dewpoint"],
            "gpsa": ["gas processors suppliers association"],
            "gpa": ["gas processors association"],
        }

        normalized = query.lower()
        for canonical, variants in normalization_map.items():
            for variant in variants:
                if variant in normalized:
                    normalized = normalized.replace(variant, canonical)

        return normalized

    def three_layer_response(self, query: str, mode: ResponseMode, context: Optional[Dict] = None) -> Tuple[str, List[str], ConfidenceLevel, bool]:
        """
        Layer 1: Doctrine Cache (0-200ms)
        Layer 2: Semantic Retrieval (200-1000ms)
        Layer 3: Deep Analysis (1000-5000ms)
        """
        start = time.time()
        normalized_query = self.semantic_normalize(query)

        # Layer 1: Doctrine Cache lookup
        triggered = []
        for doctrine in DOCTRINE_CACHE:
            keyword_match = any(kw in normalized_query for kw in doctrine.keywords)
            if keyword_match:
                triggered.append(doctrine)

        if triggered:
            self.cache_hits += 1
            cache_hit = True
            latency = (time.time() - start) * 1000

            # Multi-doctrine decomposition
            answer = self._synthesize_doctrines(triggered, query, mode, context)
            confidence = self._determine_confidence(triggered)

            return answer, [d.topic for d in triggered], confidence, cache_hit

        # Layer 2: Semantic search (vector search fallback)
        self.cache_misses += 1
        cache_hit = False
        semantic_results = self._semantic_search(normalized_query)

        if semantic_results:
            answer = self._synthesize_doctrines(semantic_results, query, mode, context)
            confidence = ConfidenceLevel.DISCLOSURE
            return answer, [d.topic for d in semantic_results], confidence, cache_hit

        # Layer 3: Deep analysis mode
        answer = self._deep_analysis(query, mode, context)
        confidence = ConfidenceLevel.HIGH_RISK

        return answer, [], confidence, cache_hit

    def _semantic_search(self, query: str) -> List[DoctrineBlock]:
        """Fallback semantic search when cache misses"""
        results = []
        query_terms = set(query.split())

        for doctrine in DOCTRINE_CACHE:
            keyword_set = set(" ".join(doctrine.keywords).split())
            overlap = query_terms & keyword_set
            if len(overlap) >= 2:
                results.append(doctrine)

        return results[:3]

    def _synthesize_doctrines(self, doctrines: List[DoctrineBlock], query: str, mode: ResponseMode, context: Optional[Dict]) -> str:
        """Synthesize response from multiple doctrines"""
        if mode == ResponseMode.FAST:
            return self._fast_response(doctrines, query)
        elif mode == ResponseMode.DEFENSE:
            return self._defense_response(doctrines, query, context)
        else:  # MEMO
            return self._memo_response(doctrines, query, context)

    def _fast_response(self, doctrines: List[DoctrineBlock], query: str) -> str:
        """Concise response for quick analysis"""
        if not doctrines:
            return "No specific doctrine found. Provide more details on the natural gas processing question."

        primary = doctrines[0]
        conclusion = primary.conclusion_template

        if len(doctrines) > 1:
            related = ", ".join(d.topic for d in doctrines[1:3])
            conclusion += f"\n\nRelated considerations: {related}"

        return conclusion

    def _defense_response(self, doctrines: List[DoctrineBlock], query: str, context: Optional[Dict]) -> str:
        """Audit-ready response with full reasoning"""
        if not doctrines:
            return "Insufficient doctrine coverage for defensible analysis."

        response_parts = ["NATURAL GAS PROCESSING ANALYSIS\n"]
        response_parts.append("=" * 80 + "\n")

        for i, doctrine in enumerate(doctrines, 1):
            response_parts.append(f"\n{i}. {doctrine.topic}\n")
            response_parts.append(f"Category: {doctrine.category.value}\n")
            response_parts.append(f"\nConclusion:\n{doctrine.conclusion_template}\n")
            response_parts.append(f"\nKey Factors:\n")
            for factor in doctrine.key_factors[:5]:
                response_parts.append(f"  - {factor}\n")

            response_parts.append(f"\nAuthority:\n")
            for auth in doctrine.primary_authority[:3]:
                response_parts.append(f"  - {auth}\n")

            response_parts.append(f"\nConfidence: {doctrine.confidence.value}\n")
            response_parts.append(f"Position Zone: {doctrine.position_zone.value}\n")

        # Context integration
        if context:
            response_parts.append(f"\nCONTEXT CONSIDERATIONS:\n")
            for key, value in context.items():
                response_parts.append(f"  {key}: {value}\n")

        return "".join(response_parts)

    def _memo_response(self, doctrines: List[DoctrineBlock], query: str, context: Optional[Dict]) -> str:
        """Full documentation with reasoning frameworks"""
        if not doctrines:
            return "Insufficient doctrine for comprehensive memorandum."

        response_parts = ["TECHNICAL MEMORANDUM: NATURAL GAS PROCESSING ANALYSIS\n"]
        response_parts.append("=" * 80 + "\n\n")
        response_parts.append(f"SUBJECT: {query}\n")
        response_parts.append(f"DATE: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")

        response_parts.append("EXECUTIVE SUMMARY\n")
        response_parts.append("-" * 80 + "\n")
        for doctrine in doctrines[:2]:
            response_parts.append(f"{doctrine.conclusion_template}\n\n")

        response_parts.append("\nDETAILED ANALYSIS\n")
        response_parts.append("=" * 80 + "\n")

        for i, doctrine in enumerate(doctrines, 1):
            response_parts.append(f"\n{i}. {doctrine.topic}\n")
            response_parts.append("-" * 80 + "\n")
            response_parts.append(f"Category: {doctrine.category.value} | Zone: {doctrine.position_zone.value}\n\n")

            response_parts.append(f"REASONING FRAMEWORK:\n{doctrine.reasoning_framework}\n\n")

            response_parts.append(f"KEY FACTORS:\n")
            for factor in doctrine.key_factors:
                response_parts.append(f"  - {factor}\n")

            response_parts.append(f"\nCONFIDENCE ASSESSMENT:\n")
            response_parts.append(f"Level: {doctrine.confidence.value}\n")
            response_parts.append(f"Stratification: {doctrine.confidence_stratification}\n\n")

            response_parts.append(f"COUNTER-ARGUMENTS & RESOLUTION:\n")
            for counter in doctrine.counter_arguments[:3]:
                response_parts.append(f"  - {counter}\n")
            response_parts.append(f"\nResolution Strategy: {doctrine.resolution_strategy}\n\n")

            response_parts.append(f"AUTHORITATIVE SOURCES:\n")
            for auth in doctrine.primary_authority:
                response_parts.append(f"  - {auth}\n")
            response_parts.append("\n")

        if context:
            response_parts.append("CONTEXT DATA:\n")
            response_parts.append("-" * 80 + "\n")
            for key, value in context.items():
                response_parts.append(f"{key}: {value}\n")

        return "".join(response_parts)

    def _deep_analysis(self, query: str, mode: ResponseMode, context: Optional[Dict]) -> str:
        """Fallback analysis when no doctrines match"""
        response = f"DEEP ANALYSIS MODE (No direct doctrine match)\n\n"
        response += f"Query: {query}\n\n"
        response += "The query does not match existing natural gas processing doctrine blocks. "
        response += "This suggests either:\n"
        response += "1. Novel processing scenario requiring custom analysis\n"
        response += "2. Query needs refinement to match standard processing topics\n"
        response += "3. Doctrine coverage gap identified\n\n"

        response += "Standard natural gas processing topics covered:\n"
        for category in IssueCategory:
            response += f"  - {category.value}\n"

        response += "\nRecommendation: Rephrase query to reference specific processing operations "
        response += "(sweetening, dehydration, NGL recovery, fractionation, compression, sulfur recovery) "
        response += "or equipment (amine contactor, glycol dehydrator, turboexpander, demethanizer, compressor)."

        return response

    def _determine_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Aggregate confidence from multiple doctrines"""
        if not doctrines:
            return ConfidenceLevel.HIGH_RISK

        confidence_counts = defaultdict(int)
        for d in doctrines:
            confidence_counts[d.confidence] += 1

        if confidence_counts[ConfidenceLevel.DEFENSIBLE] >= len(doctrines) / 2:
            return ConfidenceLevel.DEFENSIBLE
        elif confidence_counts[ConfidenceLevel.AGGRESSIVE] > 0:
            return ConfidenceLevel.AGGRESSIVE
        elif confidence_counts[ConfidenceLevel.DISCLOSURE] > 0:
            return ConfidenceLevel.DISCLOSURE
        else:
            return ConfidenceLevel.HIGH_RISK

    def apply_epistemic_guardrails(self, response: str) -> Tuple[str, List[str]]:
        """Apply epistemic safety guardrails"""
        warnings = []

        banned_phrases = [
            "always", "never", "guaranteed", "certain", "impossible",
            "definitely", "absolutely", "must", "will definitely"
        ]

        for phrase in banned_phrases:
            if phrase in response.lower():
                warnings.append(f"Epistemic overconfidence detected: '{phrase}' - consider hedging language")

        if not any(qualifier in response.lower() for qualifier in ["typical", "generally", "often", "may", "can", "might"]):
            warnings.append("Response lacks epistemic hedging - consider adding qualifiers for engineering uncertainty")

        caveat = "\n\n[Engineering Judgment Required: This analysis based on standard natural gas processing practices. Actual design requires detailed process simulation, vendor input, and site-specific conditions. Consult GPSA Engineering Data Book and applicable codes for final design.]"

        return response + caveat, warnings

    def log_query(self, query: str, response: str, triggered: List[str], confidence: ConfidenceLevel, latency_ms: float):
        """Audit trail logging"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "response_length": len(response),
            "triggered_doctrines": triggered,
            "confidence": confidence.value,
            "latency_ms": latency_ms,
            "determinism_hash": hashlib.sha256(response.encode()).hexdigest()[:16]
        }
        self.query_log.append(log_entry)

        # Update coverage tracking
        for topic in triggered:
            self.triggered_set.add(topic)
            self.triggered_doctrines[topic] += 1

    def get_coverage_map(self) -> Dict[str, Any]:
        """Track doctrine coverage and epistemic gaps"""
        triggered_count = len(self.triggered_set)
        total_count = len(self.all_doctrines)
        coverage_pct = (triggered_count / total_count * 100) if total_count > 0 else 0

        untriggered = self.all_doctrines - self.triggered_set

        return {
            "total_doctrines": total_count,
            "triggered_doctrines": triggered_count,
            "coverage_percentage": round(coverage_pct, 2),
            "untriggered_topics": list(untriggered)[:10],
            "most_frequent": sorted(self.triggered_doctrines.items(), key=lambda x: x[1], reverse=True)[:5]
        }

    def get_metrics(self) -> Dict[str, Any]:
        """Collect performance metrics"""
        uptime = time.time() - self.start_time
        total_queries = len(self.query_log)
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0

        return {
            "total_queries": total_queries,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate": round(self.cache_hits / total_queries * 100, 2) if total_queries > 0 else 0,
            "avg_latency_ms": round(avg_latency, 2),
            "uptime_seconds": round(uptime, 2),
            "queries_per_minute": round(total_queries / (uptime / 60), 2) if uptime > 60 else 0
        }

    def get_health(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        metrics = self.get_metrics()
        coverage = self.get_coverage_map()

        return {
            "status": "healthy",
            "engine": "ENRG09_Natural_Gas_Processing",
            "version": "1.0.0",
            "port": 9244,
            "doctrine_count": len(DOCTRINE_CACHE),
            "cache_size": len(self.doctrine_cache),
            "metrics": metrics,
            "coverage": coverage,
            "uptime_seconds": metrics["uptime_seconds"]
        }

# ============================================================================
# FASTAPI SERVER
# ============================================================================

app = FastAPI(title="ENRG09 Natural Gas Processing Intelligence Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = ENRG09Engine()

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with three-layer response"""
    start_time = time.time()

    try:
        answer, triggered, confidence, cache_hit = engine.three_layer_response(
            request.query, request.mode, request.context
        )

        answer_with_guardrails, warnings = engine.apply_epistemic_guardrails(answer)

        latency_ms = (time.time() - start_time) * 1000
        engine.latencies.append(latency_ms)

        determinism_hash = hashlib.sha256(answer_with_guardrails.encode()).hexdigest()[:16]

        engine.log_query(request.query, answer_with_guardrails, triggered, confidence, latency_ms)

        return QueryResponse(
            query=request.query,
            mode=request.mode,
            answer=answer_with_guardrails,
            triggered_doctrines=triggered,
            confidence=confidence,
            cache_hit=cache_hit,
            latency_ms=round(latency_ms, 2),
            determinism_hash=determinism_hash,
            epistemic_warnings=warnings,
            timestamp=datetime.utcnow().isoformat()
        )

    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Comprehensive health check"""
    health_data = engine.get_health()
    return HealthResponse(**health_data)

@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine blocks"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "zone": d.position_zone.value
            }
            for d in DOCTRINE_CACHE
        ]
    }

@app.get("/coverage")
async def coverage_endpoint():
    """Doctrine coverage and gap analysis"""
    return engine.get_coverage_map()

@app.get("/metrics")
async def metrics_endpoint():
    """Performance metrics"""
    return engine.get_metrics()

@app.get("/audit_log")
async def audit_log_endpoint(limit: int = 100):
    """Recent query audit trail"""
    return {
        "total_queries": len(engine.query_log),
        "recent_queries": engine.query_log[-limit:]
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.add("enrg09_natural_gas_processing.log", rotation="100 MB", retention="30 days")
    logger.info("Starting ENRG09 Natural Gas Processing Intelligence Engine on port 9244")

    uvicorn.run(app, host="0.0.0.0", port=9244, log_level="info")
