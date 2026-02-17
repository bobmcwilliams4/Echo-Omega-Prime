"""
PROD06 Water Cut Analysis Engine v1.0.0
TIE-Grade Intelligence Engine for Water Production Analysis

Analyzes water cut trends, BSW measurements, waterflood performance,
water breakthrough prediction, and production decline due to water encroachment.

Port: 9221
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import re
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

ENGINE_ID = "PROD06"
ENGINE_NAME = "Water Cut Analysis Engine"
VERSION = "1.0.0"
PORT = 9221
AUDIT_LOG_PATH = Path(__file__).parent / "audit_trail.jsonl"

# Epistemic guardrails
BANNED_PHRASES = [
    "guarantee", "certain", "definitely", "always works", "never fails",
    "100% accurate", "perfectly predicts", "eliminates all risk"
]

DISCLOSURE_CAVEAT = (
    "Water cut analysis involves subsurface uncertainty, measurement variability, "
    "and complex reservoir behavior. Predictions should be validated with field data, "
    "production tests, and reservoir simulation. Regulatory requirements for water "
    "disposal, injection, and reporting vary by jurisdiction."
)

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

class ZoneType(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class IssueCategory(str, Enum):
    WATER_CUT_CALCULATION = "WATER_CUT_CALCULATION"
    BSW_MEASUREMENT = "BSW_MEASUREMENT"
    WATERFLOOD_PERFORMANCE = "WATERFLOOD_PERFORMANCE"
    BREAKTHROUGH_PREDICTION = "BREAKTHROUGH_PREDICTION"
    DECLINE_ANALYSIS = "DECLINE_ANALYSIS"
    PRODUCED_WATER_HANDLING = "PRODUCED_WATER_HANDLING"
    INJECTION_WATER_QUALITY = "INJECTION_WATER_QUALITY"
    DIAGNOSTIC_PLOTS = "DIAGNOSTIC_PLOTS"
    WATER_OIL_RATIO = "WATER_OIL_RATIO"
    REGULATORY_COMPLIANCE = "REGULATORY_COMPLIANCE"
    RESERVOIR_SIMULATION = "RESERVOIR_SIMULATION"
    SEPARATION_EFFICIENCY = "SEPARATION_EFFICIENCY"

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: List[str]
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

class QueryRequest(BaseModel):
    question: str = Field(..., description="Water cut analysis question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    zone: ZoneType = Field(default=ZoneType.PLANNING, description="Analysis zone")

class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    sources: List[str]
    reasoning_chain: List[str]
    triggered_doctrines: List[str]
    missed_doctrines: List[str]
    determinism_hash: str
    mode: ResponseMode
    zone: ZoneType
    timestamp: str
    disclosure: str

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrine_count: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float
    cache_hit_rate: float

# ============================================================================
# DOCTRINE CACHE - 25+ REAL WATER CUT ANALYSIS BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Water Cut Definition and Calculation",
        keywords=["water cut", "water fraction", "liquid production", "percentage", "bwpd", "bopd", "calculation"],
        conclusion_template=[
            "Water cut is the ratio of water production to total liquid production, expressed as a percentage.",
            "Calculated as: Water Cut (%) = (Water Rate / (Water Rate + Oil Rate)) × 100",
            "Critical metric for evaluating well performance, waterflood efficiency, and economic viability."
        ],
        reasoning_framework=[
            "Water cut quantifies the proportion of produced water in total liquid stream",
            "Expressed as percentage, fraction, or water-oil ratio (WOR)",
            "Industry standard: WC% = (BWPD / (BWPD + BOPD)) × 100",
            "Alternative: WC% = (BWPD / BLPD) × 100 where BLPD = total liquid",
            "Water-oil ratio: WOR = BWPD / BOPD (inverse relationship to oil cut)",
            "Economic limit often reached at 95-98% water cut depending on oil price and lifting costs",
            "Rising water cut indicates reservoir depletion, water encroachment, or waterflood breakthrough",
            "Can be measured at wellhead, separator, or sales point (reporting basis matters)",
            "Free water vs emulsified water distinction affects measurement accuracy",
            "Temperature and pressure conditions affect phase separation and measurement",
            "Produced water includes formation water, injected water, and condensed steam",
            "Water cut progression follows characteristic S-curve in waterflood projects",
            "Early water production may indicate coning, channeling, or completion issues",
            "Sudden water cut increases suggest casing leak, fracture communication, or completion failure",
            "Declining water cut is unusual and may indicate measurement error or changing flow regime",
            "Water cut trends analyzed alongside GOR, pressure, and rate changes",
            "Field-wide water cut aggregates individual well performance",
            "Used in reserves estimation, decline curve analysis, and economic forecasting",
            "Critical input for facility design (separation, treatment, disposal capacity)",
            "Regulatory reporting requirements vary by jurisdiction and disposal method"
        ],
        key_factors=[
            "Measurement point (wellhead, separator, tank)",
            "Free water vs emulsified water separation",
            "Temperature and pressure conditions during measurement",
            "Flow regime (stable vs slug flow affects sampling)",
            "Meter accuracy and calibration status",
            "Sampling frequency and methodology",
            "Emulsion stability and treating chemical effects"
        ],
        primary_authority=[
            "SPE 28615 - Water Cut Measurement and Prediction",
            "API RP 45 - Recommended Practice for Analysis of Oilfield Waters",
            "Craft and Hawkins - Applied Petroleum Reservoir Engineering (2014)",
            "Thakur and Satter - Integrated Waterflood Asset Management (1998)"
        ],
        burden_holder="Operator",
        adversary_position="Disputes measurement accuracy, claims wellhead vs separator discrepancy",
        counter_arguments=[
            "Wellhead measurement may not reflect true reservoir water cut",
            "Emulsions cause under-reporting of water content",
            "Slug flow causes measurement variability",
            "Downhole water cut meters provide more accurate real-time data",
            "Temperature changes between wellhead and separator affect phase behavior"
        ],
        resolution_strategy="Use separator-based measurement with proper retention time, validate with lab BSW tests, trend over time to smooth transient effects",
        entity_scope="All oil-producing wells and fields",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Calculation methodology is industry-standard; measurement accuracy depends on equipment and conditions",
        controlling_precedent="API RP 45 sampling and analysis procedures"
    ),

    DoctrineBlock(
        topic="BSW Measurement Techniques - Centrifuge Method",
        keywords=["BSW", "basic sediment water", "centrifuge", "ASTM D4007", "field test", "lab analysis"],
        conclusion_template=[
            "Centrifuge method is the primary field test for measuring BSW content in crude oil samples.",
            "ASTM D4007 specifies centrifuge speed, temperature, and duration for accurate results.",
            "Reports combined volume percent of water and sediment in oil sample."
        ],
        reasoning_framework=[
            "BSW = Basic Sediment and Water content in crude oil",
            "Measured as volume percentage of non-oil material",
            "Centrifuge method per ASTM D4007 uses centrifugal force to separate phases",
            "Sample mixed with solvent (typically toluene or xylene) in graduated tube",
            "Centrifuged at 800-1500 rpm for 10 minutes (varies by API gravity)",
            "Water and sediment settle to bottom; read volume from graduations",
            "Result reported as vol% BSW (e.g., 2.5% BSW means 97.5% oil)",
            "Field test provides quick results for allocation and custody transfer",
            "More accurate than visual observation or settling tests",
            "Temperature affects emulsion stability and separation efficiency",
            "Solvent selection impacts separation (aromatic solvents better for heavy crude)",
            "Tight emulsions may require heating or demulsifier addition",
            "Sediment includes sand, silt, corrosion products, and paraffins",
            "Cannot distinguish between water and sediment (both reported together)",
            "Karl Fischer titration provides water-only measurement (no sediment)",
            "Lab BSW more accurate than field test due to controlled conditions",
            "Sampling technique critical - must be representative of flowing stream",
            "Thief samples from tanks may not represent wellstream composition",
            "Composite samples over time better than grab samples for variable production",
            "Results used for royalty calculations, custody transfer, and sales contracts"
        ],
        key_factors=[
            "Centrifuge speed and duration (standardized by crude API gravity)",
            "Solvent type and volume (toluene for light crude, xylene for heavy)",
            "Sample temperature during test",
            "Emulsion tightness and stability",
            "Presence of treating chemicals or demulsifiers",
            "Sample representativeness (grab vs composite)",
            "Operator technique and experience"
        ],
        primary_authority=[
            "ASTM D4007 - Standard Test Method for Water and Sediment in Crude Oil by Centrifuge Method",
            "ASTM D95 - Standard Test Method for Water in Petroleum Products by Distillation",
            "ASTM D473 - Standard Test Method for Sediment in Crude Oils by Extraction",
            "API MPMS Chapter 10.3 - Sediment and Water Determination"
        ],
        burden_holder="Operator (must prove oil quality meets contract specifications)",
        adversary_position="Claims BSW measurement underreports water content due to emulsion stability",
        counter_arguments=[
            "Centrifuge may not break tight emulsions completely",
            "Field conditions less controlled than lab standards",
            "Operator bias toward lower BSW readings (higher oil credit)",
            "Karl Fischer method more accurate for water-only measurement",
            "Automated online BSW meters provide continuous monitoring"
        ],
        resolution_strategy="Use ASTM-compliant procedures, calibrate centrifuge regularly, validate field tests with periodic lab analysis, use Karl Fischer for disputed measurements",
        entity_scope="Crude oil purchase contracts, royalty calculations, custody transfer",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Method is industry-standard but accuracy depends on execution and sample quality",
        controlling_precedent="ASTM D4007 is contractual standard for BSW measurement"
    ),

    DoctrineBlock(
        topic="Karl Fischer Titration for Water Content",
        keywords=["Karl Fischer", "water content", "coulometric", "volumetric", "ASTM D4928", "precision"],
        conclusion_template=[
            "Karl Fischer titration measures water content in crude oil with high precision.",
            "ASTM D4928 specifies coulometric method for low water concentrations (<1%).",
            "More accurate than centrifuge BSW for custody transfer and dispute resolution."
        ],
        reasoning_framework=[
            "Karl Fischer (KF) titration is chemical analytical method for water determination",
            "Based on redox reaction between iodine and water in presence of sulfur dioxide",
            "Coulometric KF for low water content (0.001% to 5%)",
            "Volumetric KF for higher water content (0.01% to 100%)",
            "ASTM D4928 covers coulometric method for petroleum products",
            "Sample injected into anhydrous methanol with KF reagent",
            "Water reacts stoichiometrically with iodine; endpoint detected electrochemically",
            "Result reported as mass% or volume% water (no sediment measurement)",
            "Precision ±0.02% for water content >0.1%",
            "Lab-only method; requires trained technician and specialized equipment",
            "Not affected by emulsion stability or sediment content",
            "Can measure water in light ends, condensates, and refined products",
            "Industry standard for custody transfer dispute resolution",
            "More expensive and time-consuming than centrifuge BSW",
            "Sample handling critical - moisture contamination from atmosphere",
            "Oven drying or distillation alternative for very low water content",
            "Used for validation of online water cut meters",
            "Critical for high-value crude and tight specifications",
            "Regulatory acceptance for royalty and tax calculations",
            "Provides single-component water measurement (unlike BSW which includes sediment)"
        ],
        key_factors=[
            "Method selection (coulometric vs volumetric based on water range)",
            "Sample homogeneity and representativeness",
            "Moisture contamination during sampling and handling",
            "Instrument calibration and reagent quality",
            "Operator training and technique",
            "Interference from mercaptans, H2S, or other reactive compounds"
        ],
        primary_authority=[
            "ASTM D4928 - Standard Test Method for Water in Crude Oils by Coulometric Karl Fischer Titration",
            "ASTM E203 - Standard Test Method for Water Using Volumetric Karl Fischer Titration",
            "API MPMS Chapter 10.9 - Standard Test Method for Water in Crude Oil by Coulometric KF",
            "ISO 12937 - Petroleum products - Determination of water by KF"
        ],
        burden_holder="Party disputing centrifuge BSW results bears cost of KF analysis",
        adversary_position="Accepts KF as definitive for water content but may dispute sampling method",
        counter_arguments=[
            "Sample may not be representative of bulk production",
            "Time delay between sampling and analysis (water may settle)",
            "KF only measures water, not sediment (different from BSW)",
            "High cost limits routine use",
            "Requires specialized lab and trained personnel"
        ],
        resolution_strategy="Use for custody transfer disputes, validate centrifuge BSW calibration, composite sampling over production period, chain of custody documentation",
        entity_scope="High-value crude, custody transfer points, contract disputes",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Gold standard for water measurement; accuracy limited only by sampling quality",
        controlling_precedent="ASTM D4928 is industry-accepted referee method"
    ),

    DoctrineBlock(
        topic="Waterflood Performance - Buckley-Leverett Theory",
        keywords=["Buckley-Leverett", "fractional flow", "water saturation", "breakthrough", "displacement efficiency"],
        conclusion_template=[
            "Buckley-Leverett theory predicts water saturation profile and breakthrough timing in waterfloods.",
            "Fractional flow curve relates water cut to water saturation at reservoir conditions.",
            "Breakthrough occurs when water front reaches producer based on saturation distribution."
        ],
        reasoning_framework=[
            "Buckley-Leverett is fundamental 1D immiscible displacement theory",
            "Describes water saturation movement in porous media during waterflood",
            "Fractional flow fw = qw / qt as function of water saturation Sw",
            "fw depends on relative permeability curves krw(Sw) and kro(Sw)",
            "Also depends on viscosity ratio (oil/water) and capillary pressure",
            "Shock front forms at saturation where dfw/dSw is maximum",
            "Shock front advances at velocity proportional to dfw/dSw",
            "Breakthrough occurs when shock front reaches production well",
            "Post-breakthrough, water cut follows fractional flow curve",
            "Assumptions: 1D linear flow, incompressible fluids, no gravity/capillary forces",
            "Welge tangent construction determines average saturation behind front",
            "Water saturation profile shows sharp front (piston-like displacement)",
            "Mobility ratio M = (krw/μw) / (kro/μo) affects sweep efficiency",
            "Unfavorable mobility (M > 1) causes viscous fingering and early breakthrough",
            "Reservoir heterogeneity (permeability layers) violates 1D assumption",
            "Vertical sweep affected by gravity override (water denser than oil)",
            "Areal sweep affected by well pattern and permeability distribution",
            "Used to estimate waterflood recovery factor and oil production profile",
            "Basis for more complex reservoir simulation but useful analytical tool",
            "Predicts S-curve of water cut vs cumulative oil production"
        ],
        key_factors=[
            "Relative permeability curves (krw and kro vs Sw)",
            "Oil-water viscosity ratio",
            "Initial water saturation (Swi) and residual oil saturation (Sor)",
            "Capillary pressure effects (negligible in high-rate floods)",
            "Reservoir heterogeneity and layering",
            "Gravity segregation (dip angle and density contrast)",
            "Well spacing and injection/production rate balance"
        ],
        primary_authority=[
            "Buckley, S.E. and Leverett, M.C. - Mechanism of Fluid Displacement in Sands (1942)",
            "Welge, H.J. - A Simplified Method for Computing Oil Recovery by Gas or Water Drive (1952)",
            "Craig, F.F. - The Reservoir Engineering Aspects of Waterflooding (SPE Monograph 1971)",
            "Lake, L.W. - Enhanced Oil Recovery (1989)"
        ],
        burden_holder="Operator (must design waterflood to maximize recovery)",
        adversary_position="Claims Buckley-Leverett over-predicts recovery due to heterogeneity and fingering",
        counter_arguments=[
            "Real reservoirs are 3D and heterogeneous (not 1D homogeneous)",
            "Gravity and capillary forces are significant in many cases",
            "Relative permeability curves vary spatially and with rate",
            "Viscous fingering in unfavorable mobility ratio cases",
            "Fractures and high-perm streaks cause early breakthrough",
            "Requires accurate rel perm data (often uncertain)"
        ],
        resolution_strategy="Use for initial screening and analytical predictions; validate with reservoir simulation and field data; update relative permeability from production history matching",
        entity_scope="Waterflood projects in sandstone and carbonate reservoirs",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Provides theoretical framework but real reservoirs deviate significantly; use for trends not absolutes",
        controlling_precedent="Buckley-Leverett theory is foundational but must be adapted to field conditions"
    ),

    DoctrineBlock(
        topic="Water Breakthrough Prediction - Channel and Frontal Advance",
        keywords=["breakthrough", "water advance", "channeling", "heterogeneity", "Koval factor", "Dykstra-Parsons"],
        conclusion_template=[
            "Water breakthrough time depends on reservoir heterogeneity, mobility ratio, and well spacing.",
            "Channels through high-permeability zones cause earlier breakthrough than piston-like advance.",
            "Dykstra-Parsons coefficient and Koval factor quantify heterogeneity impact on breakthrough."
        ],
        reasoning_framework=[
            "Breakthrough = time when injected water first reaches production well",
            "Ideal piston displacement: BT = (Pore Volume / Injection Rate) × (1 - Swi)",
            "Reality: heterogeneity causes channeling and early breakthrough",
            "Dykstra-Parsons coefficient VDP quantifies permeability variation (0 to 1)",
            "VDP = 0: homogeneous; VDP > 0.7: highly heterogeneous",
            "High-permeability streaks or fractures carry water preferentially",
            "Koval factor K relates effective to actual mobility ratio",
            "K > 1 indicates adverse mobility and channeling",
            "Stiles method for layered reservoirs with no crossflow",
            "Water breaks through first in highest permeability layer",
            "Crossflow between layers improves sweep but delays breakthrough prediction",
            "Geological modeling (geostatistics) captures spatial permeability distribution",
            "Tracer tests validate flow paths and connectivity",
            "Pressure transient analysis identifies high-perm channels",
            "Production logging (PLT) shows water entry intervals",
            "Temperature logs detect cooler injected water zones",
            "Hall plot analysis identifies changing injectivity (channels opening)",
            "Early breakthrough indicates preferential flow path or casing/completion leak",
            "Conformance control (gels, foams) blocks high-perm channels",
            "Pattern balancing adjusts injection to equalize arrival times",
            "Post-breakthrough water production accelerates (S-curve)"
        ],
        key_factors=[
            "Reservoir heterogeneity (VDP coefficient, fracture presence)",
            "Mobility ratio (oil/water viscosity and rel perm)",
            "Well spacing and pattern geometry (5-spot, line drive, etc)",
            "Vertical permeability and crossflow between layers",
            "Completion intervals (perforated zones in injector/producer)",
            "Injection rate and pressure (induces fractures at high pressure)",
            "Geological continuity (channels, barriers, faults)"
        ],
        primary_authority=[
            "Dykstra, H. and Parsons, R.L. - The Prediction of Oil Recovery by Waterflood (1950)",
            "Stiles, W.E. - Use of Permeability Distribution in Waterflood Calculations (1949)",
            "Koval, E.J. - A Method for Predicting the Performance of Unstable Miscible Displacement (1963)",
            "Craig, F.F. - Reservoir Engineering Aspects of Waterflooding (SPE Monograph)"
        ],
        burden_holder="Operator (must predict and manage breakthrough timing)",
        adversary_position="Claims breakthrough earlier than predicted due to undisclosed fractures or channels",
        counter_arguments=[
            "Geological model may miss small-scale heterogeneity",
            "Induced fractures during injection not accounted for",
            "Completion problems (behind-casing flow) cause unexpected breakthrough",
            "Faults or unconformities create unexpected connectivity",
            "Injection above fracture pressure opens new flow paths"
        ],
        resolution_strategy="Use conservative (early) breakthrough estimates; monitor injection pressure for fracturing; run tracer tests to validate flow paths; adjust pattern with production data",
        entity_scope="All waterflood projects, especially heterogeneous reservoirs",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Prediction accuracy low in heterogeneous reservoirs; use as planning estimate with wide uncertainty range",
        controlling_precedent="Dykstra-Parsons and Stiles methods are industry-standard analytical tools"
    ),

    DoctrineBlock(
        topic="Chan Diagnostic Plots for Water Production Analysis",
        keywords=["Chan plot", "WOR", "diagnostic plot", "water cut trend", "log-log plot", "problem identification"],
        conclusion_template=[
            "Chan diagnostic plots use log-log plot of WOR vs cumulative oil to identify water production mechanisms.",
            "Slope patterns distinguish coning, channeling, breakthrough, and normal displacement.",
            "Enables early detection of completion problems or reservoir management issues."
        ],
        reasoning_framework=[
            "Chan plots graph log(WOR) vs log(Cumulative Oil) on log-log axes",
            "WOR = water-oil ratio = Qw / Qo (inverse of oil cut)",
            "Different slopes indicate different water production mechanisms:",
            "Slope = 0 (flat): constant WOR, equilibrium or steady-state coning",
            "Slope = 1: normal waterflood displacement (Buckley-Leverett behavior)",
            "Slope > 1: accelerating water production, possible channeling or coning",
            "Slope < 1: improving watercut, unusual (may indicate rate reduction or conformance)",
            "Developed by K.S. Chan (1995) for mature waterflood analysis",
            "Complements water cut vs time plots with cumulative production basis",
            "Log-log format expands early-time data and compresses late-time",
            "Useful for identifying onset of water coning in vertical wells",
            "Critical rate exceeded if WOR increases sharply (coning)",
            "Plateau region suggests stabilized cone below perforations",
            "Step change in slope indicates new water source (layer breakthrough, channel)",
            "Can be used for individual wells or field aggregates",
            "Diagnostic tool; does not predict future performance without model",
            "Requires accurate oil and water rate measurements over time",
            "Baseline established during initial production before water",
            "Changes in operational conditions (rate, pressure) affect interpretation",
            "Combined with Hall plots and pressure data for comprehensive diagnosis"
        ],
        key_factors=[
            "Data quality (accurate oil and water rates)",
            "Operational changes (rate variations, shut-ins, workovers)",
            "Measurement frequency (daily vs monthly affects resolution)",
            "Cumulative oil accuracy (accounts for all production history)",
            "Presence of multiple water sources (injection, aquifer, coning)",
            "Wellbore conditions (casing leaks, completion failures)"
        ],
        primary_authority=[
            "Chan, K.S. - Water Control Diagnostic Plots (SPE 30775, 1995)",
            "Seright, R.S. et al - Water Shutoff and Conformance Improvement (SPE REEE 2003)",
            "Bailey et al - Water Control (SPE Textbook Series Vol 5)",
            "Economides and Nolte - Reservoir Stimulation (Wiley 2000)"
        ],
        burden_holder="Operator (must diagnose water production and implement remediation)",
        adversary_position="Claims plot interpretation ambiguous without pressure and geological data",
        counter_arguments=[
            "Multiple mechanisms can produce similar slopes",
            "Requires long production history for clear trends",
            "Rate changes confound interpretation",
            "Does not identify specific channel or cone location",
            "Needs supporting data (logs, pressure, tracer) for definitive diagnosis"
        ],
        resolution_strategy="Use in combination with production logging, pressure data, and reservoir simulation; validate interpretations with workover results or tracer tests",
        entity_scope="Mature waterflood wells with water production issues",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Diagnostic tool with established interpretation guidelines; pattern recognition requires experience",
        controlling_precedent="Chan (1995) methodology widely adopted for water production diagnosis"
    ),

    DoctrineBlock(
        topic="Water Coning in Vertical Wells",
        keywords=["coning", "critical rate", "cone stability", "vertical well", "water encroachment", "perforation strategy"],
        conclusion_template=[
            "Water coning occurs when production rate exceeds critical rate, drawing water upward into wellbore.",
            "Critical rate depends on permeability anisotropy, oil-water density difference, and oil column thickness.",
            "Remediation includes rate reduction, perforating higher, or mechanical isolation."
        ],
        reasoning_framework=[
            "Water coning = upward movement of water-oil contact toward wellbore",
            "Driven by pressure drawdown overcoming gravity segregation",
            "Occurs in wells with bottom water drive or waterflood underrun",
            "Critical rate qc = threshold below which cone remains stable",
            "Classic equation: qc ∝ (kh × kv)^0.5 × Δρ × h^2 / (μo × Bo)",
            "Where kh=horizontal perm, kv=vertical perm, Δρ=density difference, h=oil column",
            "Anisotropy ratio kv/kh reduces critical rate (layering inhibits cone)",
            "Higher oil column h increases critical rate (gravity stabilizes cone)",
            "Lower oil viscosity increases critical rate (easier to lift oil)",
            "Perforating higher in oil column reduces coning tendency",
            "Perforation interval length affects effective distance to water contact",
            "Horizontal wells increase critical rate by 2-5x vs vertical wells",
            "Cone shape controlled by permeability anisotropy and rate",
            "Transient coning during rate changes may be reversible",
            "Steady-state cone develops at constant production rate",
            "Production logging (spinner, water holdup) identifies water entry interval",
            "Temperature logs show cooler water influx",
            "Workover to plug back lower perforations or install bridge plug",
            "Dual completion allows selective production from upper intervals",
            "Economic tradeoff: lower rate (defers water) vs higher rate (faster payout)"
        ],
        key_factors=[
            "Vertical to horizontal permeability ratio (kv/kh)",
            "Oil column thickness above water contact",
            "Oil-water density difference (Δρ)",
            "Oil viscosity and formation volume factor",
            "Production rate relative to critical rate",
            "Perforation interval location and length",
            "Wellbore deviation (horizontal component reduces coning)"
        ],
        primary_authority=[
            "Meyer, H.I. and Garder, A.O. - Mechanics of Two Immiscible Fluids in Porous Media (JPT 1954)",
            "Chappelear, J.E. and Hirasaki, G.J. - A Model of Oil-Water Coning (SPE 4980, 1976)",
            "Hoyland, L.A. et al - Critical Rate for Water Coning (SPE 15855, 1989)",
            "Aziz, K. et al - Petroleum Reservoir Simulation (Applied Science 1979)"
        ],
        burden_holder="Operator (must manage rate to prevent coning or remediate if occurs)",
        adversary_position="Claims coning inevitable due to thin oil column; disputes critical rate calculation",
        counter_arguments=[
            "Critical rate equations assume homogeneous reservoir (rarely true)",
            "Fractures or high-perm streaks invalidate analytical models",
            "Rate restrictions reduce revenue and project economics",
            "Horizontal well conversion expensive and uncertain",
            "Workover costs may exceed incremental oil value"
        ],
        resolution_strategy="Calculate critical rate using conservative parameters; monitor water cut trend; implement rate restrictions or workover based on economic analysis",
        entity_scope="Vertical wells in reservoirs with bottom water or waterflood underrun",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Critical rate equations provide screening tool; actual behavior depends on reservoir heterogeneity",
        controlling_precedent="Meyer-Garder and Chappelear-Hirasaki analytical solutions are industry-standard"
    ),

    DoctrineBlock(
        topic="Produced Water Handling and Treatment",
        keywords=["produced water", "treatment", "oil-water separation", "skim tank", "API separator", "hydrocyclone"],
        conclusion_template=[
            "Produced water requires treatment to remove oil, suspended solids, and dissolved components before disposal or reuse.",
            "API gravity separators, skim tanks, and hydrocyclones remove bulk free oil.",
            "Advanced treatment (media filters, membranes, chemical) needed for discharge or injection."
        ],
        reasoning_framework=[
            "Produced water = all water brought to surface with oil and gas",
            "Includes formation water, injection water, and condensed water vapor",
            "Volume increases over field life as water cut rises",
            "Disposal options: reinjection (EOR/disposal), discharge (offshore), evaporation (onshore)",
            "Treatment level depends on disposal method and regulations",
            "API gravity separator uses gravity settling to remove free oil",
            "Sizing based on Stokes Law: settling velocity ∝ droplet diameter squared",
            "Requires retention time (typically 20-30 minutes for oil droplets > 150 microns)",
            "Skim tanks provide additional settling time and remove emulsion layer",
            "Hydrocyclones use centrifugal force for compact separation (high g-force)",
            "Effective for 10-50 micron oil droplets; small footprint vs gravity separator",
            "Induced gas flotation (IGF) uses micro-bubbles to float oil droplets",
            "Chemical treatment (demulsifiers, coagulants, flocculants) enhances separation",
            "Media filters (walnut shell, anthracite) remove residual oil and solids",
            "Membrane filtration (ultrafiltration, reverse osmosis) for high-purity reuse",
            "Biological treatment removes dissolved organics (slow, large footprint)",
            "Oil content limits: <29 mg/L for offshore discharge (Gulf of Mexico), <10 mg/L (North Sea)",
            "Injection water: <10 mg/L oil, <2 mg/L solids to prevent formation damage",
            "Suspended solids cause plugging of injection wells and reservoir pores",
            "Corrosion control: oxygen scavengers, biocides, scale inhibitors",
            "Regulatory compliance: discharge permits, monitoring, reporting (NPDES, EPA UIC)"
        ],
        key_factors=[
            "Water volume (BWPD) and oil content (mg/L)",
            "Droplet size distribution (affects separation method)",
            "Emulsion stability (tight emulsions need chemical treatment)",
            "Suspended solids content and particle size",
            "Disposal method (injection, discharge, evaporation)",
            "Regulatory discharge limits (offshore vs onshore, jurisdiction)",
            "Space constraints (offshore platform vs onshore facility)"
        ],
        primary_authority=[
            "API Publication 421 - Monographs on Refinery Environmental Control - Management of Water Discharges",
            "EPA 40 CFR Part 435 - Oil and Gas Extraction Point Source Category",
            "SPE 115361 - Produced Water Treatment Technologies (2008)",
            "Arnold, K. and Stewart, M. - Surface Production Operations Vol 1 (Gulf Publishing 1999)"
        ],
        burden_holder="Operator (must treat to meet discharge or injection standards)",
        adversary_position="Regulator claims inadequate treatment; environmental groups oppose any discharge",
        counter_arguments=[
            "Treatment costs may be prohibitive (especially for low oil prices)",
            "Technology limitations for tight emulsions or high solids",
            "Space constraints on offshore platforms limit treatment options",
            "Beneficial reuse (irrigation, livestock) has lower standards but limited demand",
            "Evaporation ponds acceptable in arid climates but not in wet regions"
        ],
        resolution_strategy="Design treatment to meet regulatory standards with margin; use proven technologies with operational history; monitor effluent continuously; maintain treatment chemicals and equipment",
        entity_scope="All oil production operations with water handling",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Separation technology mature and well-understood; regulatory compliance mandatory",
        controlling_precedent="EPA NPDES permits and state injection well permits specify enforceable limits"
    ),

    DoctrineBlock(
        topic="Injection Water Quality Requirements",
        keywords=["injection water", "water quality", "suspended solids", "oil content", "bacteria", "formation damage"],
        conclusion_template=[
            "Injection water must meet stringent quality standards to prevent formation damage and injectivity decline.",
            "Typical limits: <5-10 mg/L oil, <2-5 mg/L suspended solids, <100 CFU/mL bacteria.",
            "Filtration, deoiling, and biocide treatment required for most produced water reinjection."
        ],
        reasoning_framework=[
            "Injection water quality critical to maintain reservoir injectivity",
            "Formation damage from: suspended solids plugging pores, oil droplets blocking flow paths, bacterial growth",
            "Suspended solids (TSS): sand, silt, corrosion products, scale, biomass",
            "Particle size distribution matters: particles > pore throat diameter cause bridging",
            "Typical sandstone pore throats: 1-100 microns; carbonates: 0.1-10 microns (tighter)",
            "Filtration targets: <2 mg/L TSS for sandstone, <1 mg/L for tight formations",
            "Oil content limit: <10 mg/L (prevents emulsion blocking and wettability change)",
            "Dissolved oxygen promotes corrosion and aerobic bacterial growth",
            "Oxygen scavengers (sulfite, bisulfite) reduce DO to <50 ppb",
            "Sulfate-reducing bacteria (SRB) produce H2S, causing souring and corrosion",
            "Biocides (glutaraldehyde, THPS, quaternary amines) control bacteria",
            "Target: <100 colony forming units (CFU) per mL",
            "Scale inhibitors prevent CaCO3, CaSO4, BaSO4 precipitation",
            "Compatibility testing: mix injection water with formation water to check scaling",
            "Corrosion inhibitors protect injection wellbore and tubing",
            "Water clarity (turbidity) indicates particle load: <5 NTU acceptable",
            "Injectivity decline monitored via Hall plot (cumulative pressure × time vs cumulative injection)",
            "Hall plot slope increase indicates formation damage or skin growth",
            "Acid stimulation or fracturing restores injectivity if damage occurs",
            "Filtration technologies: cartridge filters (5-50 micron), multimedia (sand/anthracite), membranes",
            "Regulatory compliance: UIC Class II well permits specify injection water quality"
        ],
        key_factors=[
            "Particle size distribution and concentration (TSS)",
            "Oil content (free and emulsified)",
            "Bacterial count (total and SRB)",
            "Dissolved oxygen level",
            "Scale-forming ions (Ca, Ba, Sr, sulfate)",
            "Formation pore throat size and permeability",
            "Injection rate and pressure (affects filtration efficiency)"
        ],
        primary_authority=[
            "SPE 73737 - Water Quality Requirements for Injection Wells (2002)",
            "NACE SP0499 - Microbiological Influenced Corrosion in Oilfield Water Handling",
            "API RP 38 - Biological Analysis of Subsurface Injection Waters",
            "Veil, J.A. - Produced Water Management Options (2011)"
        ],
        burden_holder="Operator (must treat injection water to protect reservoir)",
        adversary_position="Formation damage claim due to inadequate water quality control",
        counter_arguments=[
            "Treatment costs reduce waterflood economics",
            "Produced water naturally contains some solids and oil",
            "High injection rates tolerate higher particle loading",
            "Formation may have natural permeability variability (not all damage from water)",
            "Acid stimulation can remediate damage periodically"
        ],
        resolution_strategy="Establish quality targets based on formation characteristics; implement filtration and chemical treatment; monitor injectivity with Hall plots; stimulate as needed",
        entity_scope="All waterflood and disposal injection wells",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Quality requirements well-established by industry experience; enforcement varies by regulator",
        controlling_precedent="EPA UIC Class II permits and state regulations specify water quality monitoring"
    ),

    DoctrineBlock(
        topic="Water-Oil Ratio (WOR) Decline Analysis",
        keywords=["WOR", "water-oil ratio", "decline curve", "economic limit", "Ershaghi-Omoregie", "X-plot"],
        conclusion_template=[
            "WOR vs cumulative oil production follows predictable trends for normal waterflood displacement.",
            "Ershaghi-Omoregie X-plot linearizes WOR data for forecasting and reserves estimation.",
            "Economic limit reached when lifting costs exceed oil revenue at prevailing WOR."
        ],
        reasoning_framework=[
            "WOR = water-oil ratio = Qw / Qo (barrels water per barrel oil)",
            "Inverse of oil cut: Oil Cut = Qo / (Qo + Qw) = 1 / (1 + WOR)",
            "WOR increases over time as waterflood matures and water cut rises",
            "Typically follows exponential or hyperbolic trend: WOR = a × Np^b",
            "Where Np = cumulative oil production, a and b are empirical constants",
            "Ershaghi-Omoregie (1978) X-plot: log(WOR) vs log(Np) or log(WOR) vs Np",
            "Linear trend on semi-log plot allows extrapolation to economic limit",
            "Economic limit WOR depends on oil price, lifting cost, and water disposal cost",
            "Example: $60/bbl oil, $15/bbl lifting + water disposal → limit at WOR = 3-4",
            "Higher oil prices justify producing at higher WOR (more water handling)",
            "WOR forecast used for reserves booking (SEC PDP, PDNP categories)",
            "Declining oil rate with increasing WOR: qo = qt / (1 + WOR)",
            "Total liquid rate qt may be constant (pump limited) while qo declines",
            "Artificial lift (rod pump, ESP, gas lift) capacity limits total liquid",
            "Upgrade artificial lift to handle higher water rates extends field life",
            "Water disposal capacity (injection, evaporation, discharge) may constrain WOR",
            "Sudden WOR jumps indicate new water source (not normal decline trend)",
            "Conformance treatments reduce WOR by blocking high-water zones",
            "Infill drilling can improve recovery in bypassed oil zones with lower WOR",
            "Combination of Arps oil decline and WOR trend yields full forecast"
        ],
        key_factors=[
            "Historical WOR vs cumulative oil trend",
            "Oil price and operating cost structure",
            "Artificial lift capacity and water handling limits",
            "Water disposal cost and regulatory constraints",
            "Remaining oil saturation and reservoir heterogeneity",
            "Conformance treatment options and costs"
        ],
        primary_authority=[
            "Ershaghi, I. and Omoregie, O. - A Method for Extrapolation of Cut vs Recovery Curves (JPT 1978)",
            "Lo, K.K. et al - Decline Curve Analysis Using Type Curves (JPT 1990)",
            "SPE 77290 - Waterflood Performance Prediction Using WOR Data",
            "Fetkovich, M.J. - Decline Curve Analysis Using Type Curves (JPT 1980)"
        ],
        burden_holder="Operator (must forecast WOR for reserves and economics)",
        adversary_position="Disputes economic limit WOR; claims premature abandonment",
        counter_arguments=[
            "Operating costs may decline with field maturity (paid off capital)",
            "Oil price increases extend economic limit WOR",
            "Technology improvements (ESP vs rod pump) reduce lifting cost",
            "Conformance treatments can reverse WOR trend",
            "Tax or royalty relief may improve economics at high WOR"
        ],
        resolution_strategy="Update WOR forecast with actual data; run sensitivity on oil price and costs; evaluate conformance options; benchmark against analog fields",
        entity_scope="Mature waterflood fields approaching economic limit",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="WOR trends well-established in waterflood literature; economic limit depends on variable oil prices",
        controlling_precedent="Ershaghi-Omoregie method widely used for WOR forecasting"
    ),

    DoctrineBlock(
        topic="Relative Permeability and Fractional Flow",
        keywords=["relative permeability", "krw", "kro", "fractional flow", "Corey correlation", "SCAL"],
        conclusion_template=[
            "Relative permeability curves define water and oil flow capacity as function of saturation.",
            "Fractional flow fw relates water cut to saturation using krw, kro, and fluid viscosities.",
            "Special core analysis (SCAL) measures rel perm for reservoir-specific values."
        ],
        reasoning_framework=[
            "Relative permeability kr = ratio of effective perm at saturation to absolute perm",
            "krw(Sw) = water rel perm as function of water saturation",
            "kro(Sw) = oil rel perm as function of water saturation",
            "At Swi (initial water saturation): krw = 0, kro = max (often <1 due to residual oil)",
            "At Sor (residual oil saturation): krw = max, kro = 0",
            "Corey correlation: krw = krw_max × ((Sw - Swi) / (1 - Swi - Sor))^nw",
            "Similarly: kro = kro_max × ((1 - Sw - Sor) / (1 - Swi - Sor))^no",
            "Exponents nw and no are empirical (typically 2-4 for sandstone)",
            "Fractional flow: fw = 1 / (1 + (kro/krw) × (μw/μo))",
            "Water cut at surface: WC = fw / Bw / (fw/Bw + (1-fw)/Bo) ≈ fw for low-shrinkage oil",
            "Endpoint saturations Swi and Sor from core measurements or well logs",
            "Crossover saturation Sw* where krw = kro indicates equal mobility",
            "Wettability affects rel perm curves: water-wet vs oil-wet vs mixed-wet",
            "SCAL tests: steady-state (long duration, accurate) or unsteady-state (faster, requires analysis)",
            "Three-phase rel perm (oil-water-gas) more complex; Stone's methods used",
            "Hysteresis in drainage vs imbibition curves (different paths for Sw increasing vs decreasing)",
            "Reservoir simulation uses rel perm tables or correlations as input",
            "Upscaling from core to grid-block scale involves averaging and pseudo functions",
            "Uncertainty in rel perm major contributor to waterflood prediction uncertainty",
            "History matching adjusts rel perm to match observed water cut and pressure"
        ],
        key_factors=[
            "Endpoint saturations (Swi, Sor)",
            "Curvature exponents (nw, no) or measured data points",
            "Wettability (water-wet, oil-wet, mixed)",
            "Fluid viscosity ratio (μo / μw)",
            "Rock lithology (sandstone, carbonate, shale)",
            "Temperature and pressure (affect viscosity and wettability)"
        ],
        primary_authority=[
            "Corey, A.T. - The Interrelation Between Gas and Oil Relative Permeabilities (1954)",
            "Brooks, R.H. and Corey, A.T. - Properties of Porous Media Affecting Fluid Flow (1966)",
            "Honarpour, M. et al - Relative Permeability of Petroleum Reservoirs (CRC Press 1986)",
            "API RP 40 - Recommended Practice for Core Analysis (1998)"
        ],
        burden_holder="Operator (must determine rel perm for reservoir simulation)",
        adversary_position="Disputes rel perm values; claims lab measurements not representative of reservoir",
        counter_arguments=[
            "Core samples may not represent reservoir heterogeneity",
            "Preservation and handling alter wettability",
            "Lab conditions (temperature, pressure, fluids) differ from reservoir",
            "Scale effects: core plugs vs reservoir scale",
            "Hysteresis not captured in single drainage or imbibition curve"
        ],
        resolution_strategy="Use SCAL measurements as starting point; adjust in reservoir simulation history matching; validate with analog reservoirs; use uncertainty ranges in forecasts",
        entity_scope="All multi-phase flow reservoirs (waterflood, gas injection, depletion)",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Rel perm critical input but high uncertainty; use ranges not single values",
        controlling_precedent="SCAL measurements per API RP 40 are industry-standard but subject to interpretation"
    ),

    DoctrineBlock(
        topic="Water Cut Measurement - Online Meters vs Manual Sampling",
        keywords=["online meter", "water cut meter", "clamp-on", "microwave", "capacitance", "manual sampling"],
        conclusion_template=[
            "Online water cut meters provide real-time monitoring but require calibration and validation.",
            "Technologies include microwave, capacitance, infrared, and gamma-ray absorption.",
            "Manual sampling (centrifuge BSW, Karl Fischer) validates meter accuracy and resolves disputes."
        ],
        reasoning_framework=[
            "Online meters measure water cut continuously in flowing stream",
            "Advantages: real-time data, no sampling lag, automated monitoring",
            "Disadvantages: drift, fouling, calibration needs, emulsion sensitivity",
            "Microwave meters measure dielectric constant (water ~80, oil ~2)",
            "Capacitance meters similar principle (lower frequency than microwave)",
            "Infrared absorption exploits water O-H bond absorption",
            "Gamma-ray densitometers measure fluid density (water denser than oil)",
            "Coriolis meters measure mass flow and density; calculate water cut from density",
            "Clamp-on ultrasonic meters non-intrusive but less accurate",
            "Accuracy: ±1-2% water cut for clean systems; worse for emulsions or gas",
            "Calibration against manual samples required (weekly or monthly)",
            "Flow regime affects accuracy: slug flow, high gas, emulsions cause errors",
            "Installation location matters: after separator better than wellhead",
            "Temperature and pressure compensation necessary for density-based methods",
            "Salinity affects dielectric constant (fresh water vs brine)",
            "Oil type (API gravity, aromatics content) affects microwave response",
            "Fouling of sensor (paraffin, scale, solids) drifts calibration",
            "Meter verification with portable densitometer or grab samples",
            "Allocation metering (custody transfer) requires higher accuracy (±0.5%) and certification",
            "Regulatory acceptance varies; some jurisdictions require manual sampling backup"
        ],
        key_factors=[
            "Meter technology (microwave, capacitance, gamma, Coriolis)",
            "Flow conditions (velocity, regime, gas fraction)",
            "Fluid properties (salinity, API gravity, emulsion tendency)",
            "Calibration frequency and procedure",
            "Installation location (wellhead, separator outlet, pipeline)",
            "Temperature and pressure conditions",
            "Fouling and maintenance status"
        ],
        primary_authority=[
            "ISO 9377 - Water quality - Determination of hydrocarbon oil index",
            "API MPMS Chapter 10 - Sediment and Water Determination",
            "SPE 166138 - Water Cut Measurement Technology Review (2013)",
            "NFOGM (Norwegian) - Handbook of Water Fraction Measurement (2005)"
        ],
        burden_holder="Operator (must provide accurate water cut for allocation and royalty)",
        adversary_position="Disputes online meter accuracy; demands manual sampling for royalty calculation",
        counter_arguments=[
            "Online meters drift without frequent calibration",
            "Emulsions cause under-reading of water cut",
            "Gas slugs cause transient errors",
            "Manual sampling provides legal defensibility",
            "Meter maintenance records incomplete or unavailable"
        ],
        resolution_strategy="Use online meters for trending and control; validate monthly with manual sampling (centrifuge and periodic Karl Fischer); maintain calibration logs; use manual samples for royalty/allocation calculations",
        entity_scope="All production operations with water cut measurement needs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Online meters useful for operations but manual sampling remains standard for allocation",
        controlling_precedent="API MPMS Chapter 10 and contract terms specify measurement method for royalty"
    ),

    DoctrineBlock(
        topic="Water Disposal Regulations - UIC Class II Wells",
        keywords=["water disposal", "UIC", "injection well", "Class II", "EPA", "SDWA", "permit"],
        conclusion_template=[
            "Underground injection of produced water regulated under EPA Safe Drinking Water Act UIC program.",
            "Class II wells for oil and gas related injection require permit with operational limits.",
            "Mechanical integrity testing and water quality monitoring mandatory."
        ],
        reasoning_framework=[
            "Underground Injection Control (UIC) program under Safe Drinking Water Act (SDWA)",
            "Class II wells: oil and gas related injection (disposal and EOR)",
            "Subclasses: II-D (disposal), II-R (enhanced recovery), II-H (hydrocarbon storage)",
            "Permits issued by EPA or state (primacy) with delegated authority",
            "Texas, Oklahoma, Louisiana, North Dakota, Wyoming have primacy (state-issued permits)",
            "Permit application requires geological/hydrogeological data, well construction, operating plan",
            "Non-endangerment standard: injection must not endanger underground sources of drinking water (USDW)",
            "USDW = aquifer with <10,000 mg/L TDS used or suitable for drinking water",
            "Injection zone must be below all USDWs or isolated by confining layers",
            "Area of review (AOR): zone around well where injection pressure may affect USDWs",
            "Mechanical integrity test (MIT) required every 5 years (or more frequently)",
            "MIT includes: pressure test (tubing/packer), radioactive tracer survey (no communication outside injection zone)",
            "Maximum injection pressure limits: 90% of fracture pressure or 0.8 psi/ft, whichever less",
            "Injection rate and volume limits specified in permit",
            "Water quality monitoring: quarterly or annual sampling and analysis",
            "Annulus pressure monitoring to detect tubing leaks",
            "Plugging and abandonment plan required (bond posted)",
            "Violations: injection without permit, exceed pressure/volume limits, failed MIT, endangerment",
            "Enforcement: cease injection, corrective action, penalties, well closure",
            "Induced seismicity concerns: Oklahoma, Texas reduce disposal volumes in seismic zones"
        ],
        key_factors=[
            "Injection zone depth and isolation from USDWs",
            "Injection pressure and rate (below fracture pressure)",
            "Well mechanical integrity (tubing, casing, cement, packer)",
            "Water quality and compatibility with formation",
            "Area of review (nearby wells and USDWs)",
            "Seismic risk assessment (in areas with induced seismicity)",
            "State vs EPA regulatory authority (primacy status)"
        ],
        primary_authority=[
            "40 CFR Part 144-148 - Underground Injection Control Program",
            "EPA UIC Class II Well Guidance Documents",
            "Texas RRC Rule 3.9 and 3.46 - Injection Well Permits and Operations",
            "Oklahoma OCC Rules on Disposal Wells and Seismicity"
        ],
        burden_holder="Operator (must obtain permit and comply with operational requirements)",
        adversary_position="Regulator or public claims injection endangers groundwater or causes earthquakes",
        counter_arguments=[
            "Injection zone thousands of feet below drinking water aquifers",
            "Multiple confining layers prevent upward migration",
            "Mechanical integrity testing validates well integrity",
            "Injection pressure well below fracture pressure",
            "Seismic correlation uncertain (natural vs induced)"
        ],
        resolution_strategy="Maintain permit compliance; conduct MIT on schedule; monitor injection pressure and annulus; respond to seismic events with rate reductions if required; engage with regulators proactively",
        entity_scope="All produced water disposal wells in oil and gas operations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory framework well-established; compliance mandatory; seismic risk emerging issue",
        controlling_precedent="SDWA and state UIC regulations are enforceable with civil and criminal penalties"
    ),

    DoctrineBlock(
        topic="Declining Oil Rate with Constant Liquid Rate - Artificial Lift Constraints",
        keywords=["liquid rate", "oil decline", "artificial lift", "ESP", "rod pump", "total fluid", "pump capacity"],
        conclusion_template=[
            "Many wells produce at constant total liquid rate (BLPD) limited by artificial lift capacity.",
            "As water cut increases, oil rate declines while water rate increases to maintain constant liquid.",
            "Economic limit reached when oil revenue insufficient to cover lifting and water handling costs."
        ],
        reasoning_framework=[
            "Total liquid rate qt = qo + qw (oil plus water)",
            "Artificial lift systems (ESP, rod pump, gas lift) have maximum liquid capacity",
            "ESP: electric submersible pump, capacity 500-50,000 BLPD depending on stages",
            "Rod pump: sucker rod pump, capacity 10-5,000 BLPD depending on size and stroke",
            "Gas lift: capacity depends on gas availability and well depth",
            "Pump sized for expected peak liquid rate (considers future water cut)",
            "Operating at maximum pump capacity (qt = constant) as water cut rises:",
            "qo = qt / (1 + WOR) decreases as WOR increases",
            "qw = qt × WOR / (1 + WOR) increases as WOR increases",
            "Revenue = qo × oil_price - qt × lifting_cost - qw × water_disposal_cost",
            "Economic limit when revenue < opex or qo < minimum viable rate",
            "Example: ESP at 5,000 BLPD, WOR increases from 1 to 10:",
            "Initially: qo=2,500 bopd, qw=2,500 bwpd (50% water cut)",
            "Later: qo=455 bopd, qw=4,545 bwpd (91% water cut)",
            "Pump upgrade (larger ESP, different stages) increases liquid capacity but costly",
            "Downgrade pump for declining fields to reduce power cost and maintenance",
            "Rod pump: reduce stroke length or speed to match reservoir deliverability",
            "Gas lift: optimize injection rate and valve spacing for changing conditions",
            "Monitoring: dynamometer cards (rod pump), ESP motor parameters (amps, temp), casing pressure (gas lift)",
            "Pump efficiency declines with increasing water cut (wear, gas interference)",
            "Water handling facilities (separator, tanks, disposal) must match peak liquid rate"
        ],
        key_factors=[
            "Artificial lift type and capacity (ESP stages, pump size, gas availability)",
            "Current and projected water cut trend",
            "Reservoir deliverability (IPR curve)",
            "Oil price and operating costs (lifting, disposal, electricity)",
            "Pump efficiency and power consumption",
            "Facility constraints (separator, tank, disposal capacity)",
            "Well depth and fluid properties (affect lift requirements)"
        ],
        primary_authority=[
            "Brown, K.E. - The Technology of Artificial Lift Methods (PennWell 1980)",
            "API RP 11L - Recommended Practice for Design Calculations for Sucker Rod Pumping Systems",
            "API RP 11S - Recommended Practice for Electric Submersible Pump Testing",
            "Golan, M. and Whitson, C.H. - Well Performance (Tapir 1995)"
        ],
        burden_holder="Operator (must optimize artificial lift for changing conditions)",
        adversary_position="Claims operator under-investing in lift capacity to restrict production",
        counter_arguments=[
            "Pump upgrade costs may not be economic at current oil prices",
            "Reservoir deliverability may not support higher rates",
            "Water handling capacity limits total liquid rate",
            "Equipment availability and lead times delay upgrades",
            "Well may be near economic limit regardless of lift capacity"
        ],
        resolution_strategy="Conduct nodal analysis to determine optimal lift configuration; forecast economics with pump upgrade vs current operation; consider workover to reduce water cut vs lift upgrade",
        entity_scope="All wells with artificial lift and rising water cut",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Artificial lift optimization is standard practice; economics drive decision",
        controlling_precedent="API recommended practices for lift system design and operation"
    ),

    DoctrineBlock(
        topic="Waterflood Pattern Balancing - Injection-Production Ratio",
        keywords=["pattern balancing", "voidage replacement", "injection rate", "production rate", "pressure maintenance"],
        conclusion_template=[
            "Waterflood patterns require injection-production balance to maintain reservoir pressure.",
            "Voidage replacement ratio (VRR) = injection rate / production rate (reservoir volumes).",
            "VRR > 1 increases pressure; VRR < 1 depletes reservoir and reduces sweep efficiency."
        ],
        reasoning_framework=[
            "Waterflood injects water to replace produced oil and maintain pressure",
            "Voidage replacement ratio VRR = (Injection RB/D) / (Production RB/D)",
            "RB = reservoir barrels (corrected for formation volume factors)",
            "qinj_RB = qinj_STB / Bw (water shrinks slightly at reservoir conditions)",
            "qprod_RB = (qo × Bo + qw × Bw + qg × Bg) / 5.615 (converts SCF gas to RB)",
            "VRR = 1.0 ideal for pressure maintenance (replace produced volume exactly)",
            "VRR > 1.0 pressure increase, may improve sweep but risks fracturing",
            "VRR < 1.0 pressure decline, reduces injectivity and sweep efficiency",
            "Pattern imbalance: some injectors overdosed, others underdosed",
            "Hall plot for each injector monitors injectivity (cumulative pressure × time vs cumulative injection)",
            "Increasing Hall slope indicates formation damage or reduced injectivity",
            "Decreasing Hall slope indicates fracture or improved injectivity (unusual)",
            "Balance patterns by adjusting individual injector rates via surface choke or pump speed",
            "Objective: equalize injection front arrival time at all producers in pattern",
            "Producers with early breakthrough need reduced injection in feeding injectors",
            "Producers with no water need increased injection (likely bypassed)",
            "Surveillance: monitor water cut, pressure, GOR at each producer",
            "Tracer tests validate flow paths and injector-producer connectivity",
            "Conformance treatments (gels, polymers) in injectors redirect water to unswept zones",
            "Field-wide VRR calculated from total injection and production",
            "Individual pattern VRR may differ from field average (allocate injection strategically)"
        ],
        key_factors=[
            "Reservoir pressure vs initial pressure (degree of depletion)",
            "Individual well water cuts (indicates breakthrough locations)",
            "Injector Hall plots (injectivity trends)",
            "Formation volume factors (Bo, Bw, Bg)",
            "Reservoir heterogeneity (permeability distribution)",
            "Well pattern geometry (5-spot, line drive, etc)",
            "Injection rate limits (surface pressure, downhole pressure, permits)"
        ],
        primary_authority=[
            "Craig, F.F. - Reservoir Engineering Aspects of Waterflooding (SPE Monograph)",
            "Thakur, G.C. and Satter, A. - Integrated Waterflood Asset Management (PennWell 1998)",
            "SPE 124831 - Waterflood Surveillance and Management (2009)",
            "Hall, H.N. - How to Analyze Waterflood Injection Well Performance (1963)"
        ],
        burden_holder="Operator (must balance patterns for optimal recovery)",
        adversary_position="Claims operator over-injecting in some patterns to inflate reserves or meet contractual commitments",
        counter_arguments=[
            "Over-injection risks fracturing and channeling (reduces recovery)",
            "Under-injection leaves oil bypassed (reduces recovery)",
            "Balancing requires data and analysis not always available",
            "Injection rate limits (permit, facility, wellbore) constrain optimization",
            "Pressure increase above fracture pressure is operationally prohibited"
        ],
        resolution_strategy="Calculate field and pattern VRR monthly; adjust injector rates to balance arrivals; use surveillance data (WC, pressure, tracers) to guide allocation; maintain VRR near 1.0 field-wide",
        entity_scope="All waterflood projects with multiple injectors and producers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="VRR concept fundamental to waterflood management; implementation depends on data quality",
        controlling_precedent="Hall plot analysis and VRR calculation are industry-standard surveillance tools"
    ),

    DoctrineBlock(
        topic="Emulsion Stability and Demulsification",
        keywords=["emulsion", "demulsifier", "tight emulsion", "rag layer", "settling time", "chemical treatment"],
        conclusion_template=[
            "Emulsions are mixtures of oil and water stabilized by surfactants, asphaltenes, and solids.",
            "Tight emulsions resist gravity separation and require chemical demulsifiers.",
            "Demulsifier selection based on bottle tests and field trials; dosage optimized for cost and performance."
        ],
        reasoning_framework=[
            "Emulsion = dispersion of one liquid in another (oil-in-water or water-in-oil)",
            "Most crude oil emulsions are water-in-oil (water droplets in continuous oil phase)",
            "Stabilized by natural surfactants: asphaltenes, resins, naphthenic acids, solids",
            "Tight emulsion resists breaking; appears as rag layer in separator or tank",
            "Rag layer = semi-solid layer between oil and water phases",
            "Interfacial film around water droplets prevents coalescence",
            "Demulsifiers are surfactants that displace natural stabilizers and allow coalescence",
            "Chemistry: polyethylene glycol, polyoxypropylene, alkylphenol resins",
            "Demulsifier selection via bottle test: mix crude with demulsifier, observe settling",
            "Metrics: settling time, water drop volume, clarity of separated phases",
            "Field dosage: 5-50 ppm typical (parts per million of liquid volume)",
            "Injection point: upstream of separator or heater-treater for residence time",
            "Heat enhances demulsification: reduces viscosity, increases droplet collision",
            "Heater-treater: combines heating (120-150F) and retention (30-60 min) for separation",
            "Electrostatic treater uses high voltage to coalesce water droplets (dehydrators)",
            "Overdosing demulsifier can stabilize emulsion (reverse emulsion)",
            "Emulsion viscosity higher than pure oil (inhibits flow and separation)",
            "Tight emulsions contain <1% water but resist measurement (BSW uncertainty)",
            "Changing crude source or mixing changes emulsion stability (requires new demulsifier)",
            "Environmental/safety: demulsifiers generally low toxicity but disposal restrictions"
        ],
        key_factors=[
            "Crude oil properties (API gravity, asphaltene content, acidity)",
            "Water salinity and pH",
            "Temperature (separator, heater-treater)",
            "Retention time in separator or tank",
            "Demulsifier chemistry and dosage",
            "Mixing energy (gentle mixing aids demulsification; vigorous mixing stabilizes)",
            "Presence of solids (sand, clay stabilize emulsions)"
        ],
        primary_authority=[
            "SPE 38849 - Petroleum Emulsions: Basic Principles (1997)",
            "Sjoblom, J. et al - Emulsions and Emulsion Stability (CRC Press 2006)",
            "API Publication 4638 - Selected Analytical Methods for Environmental Remediation",
            "Grace, R. - Commercial Emulsion Breaking (in Sjoblom book)"
        ],
        burden_holder="Operator (must break emulsions to meet sales specifications and custody transfer)",
        adversary_position="Disputes BSW measurement claiming tight emulsion under-reports water",
        counter_arguments=[
            "Standard centrifuge BSW may not break tight emulsions",
            "Demulsifier costs reduce netback",
            "Bottle test results may not scale to field conditions",
            "Emulsion variability with changing production requires frequent optimization",
            "Some emulsions unbreakable economically (high dosage, high temp, long time)"
        ],
        resolution_strategy="Conduct regular bottle tests with multiple demulsifiers; optimize dosage and injection point; use heat if economic; validate with Karl Fischer for custody transfer",
        entity_scope="All crude oil production with water content and emulsion issues",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Demulsification technology mature but field-specific optimization required",
        controlling_precedent="Sales contracts specify maximum BSW (e.g. 0.5%); operator must meet spec"
    ),

    DoctrineBlock(
        topic="Water Influx from Aquifer - Material Balance",
        keywords=["aquifer", "water influx", "material balance", "encroachment", "van Everdingen-Hurst", "Carter-Tracy"],
        conclusion_template=[
            "Natural water influx from aquifers affects reservoir pressure and water production.",
            "Material balance equation includes cumulative water influx We term.",
            "Aquifer models (van Everdingen-Hurst, Carter-Tracy, Fetkovich) estimate We from production data."
        ],
        reasoning_framework=[
            "Water influx = water entering reservoir from surrounding aquifer",
            "Driven by pressure drop in reservoir (expansion of aquifer water and rock)",
            "Material balance: N = (Np × Bo + Wp × Bw + Gp × Bg - We) / (Bo - Boi + Bg × (Rsi - Rs) + Boi × (cf + cw × Swi) × ΔP)",
            "Where We = cumulative water influx (reservoir barrels)",
            "Aquifer strength: strong (pressure support), weak (limited influx), none (depletion drive)",
            "Edge-water drive: aquifer surrounds reservoir laterally",
            "Bottom-water drive: aquifer underlies reservoir (gravity segregation)",
            "Infinite-acting aquifer: large volume, pressure at outer boundary unchanged",
            "Finite aquifer: limited volume, pressure declines throughout aquifer",
            "van Everdingen-Hurst (1949): analytical solution for radial aquifer with diffusivity equation",
            "Carter-Tracy (1960): simplification of VEH for computational efficiency",
            "Fetkovich (1971): pseudo-steady-state model using productivity index for aquifer",
            "Aquifer parameters: permeability k, porosity φ, thickness h, radius re, encroachment angle θ",
            "Water influx lags pressure drop (diffusivity delay)",
            "History matching: adjust aquifer parameters to match observed pressure and water production",
            "Early water production may be from aquifer influx, not waterflood breakthrough",
            "Strong aquifer maintains pressure near initial (small pressure drop)",
            "Weak aquifer shows pressure decline but some water influx",
            "Water influx reduces ultimate oil recovery if oil bypassed by water",
            "Aquifer volume estimated from geology (seismic, well logs, outcrops)"
        ],
        key_factors=[
            "Aquifer size (radius, thickness, porosity)",
            "Aquifer permeability and compressibility",
            "Encroachment geometry (edge-water vs bottom-water)",
            "Reservoir-aquifer contact area",
            "Pressure decline magnitude and rate",
            "Water production history (distinguish aquifer vs injection water)",
            "Water salinity (aquifer vs injection water may differ)"
        ],
        primary_authority=[
            "van Everdingen, A.F. and Hurst, W. - Application of Laplace Transformation to Flow Problems (1949)",
            "Carter, R.D. and Tracy, G.W. - An Improved Method for Calculating Water Influx (1960)",
            "Fetkovich, M.J. - A Simplified Approach to Water Influx Calculations (JPT 1971)",
            "Dake, L.P. - Fundamentals of Reservoir Engineering (Elsevier 1978)"
        ],
        burden_holder="Operator (must account for aquifer influx in reserves and forecasts)",
        adversary_position="Claims water influx over-estimated to inflate reserves or justify low recovery",
        counter_arguments=[
            "Aquifer size and properties uncertain (limited data beyond reservoir)",
            "Water production may be from waterflood injection not aquifer",
            "Material balance non-unique solution (multiple aquifer models fit data)",
            "Pressure data sparse or unreliable (affects influx calculation)",
            "Salinity analysis can distinguish aquifer water from injection water"
        ],
        resolution_strategy="Match multiple data types (pressure, water production, salinity); use conservative aquifer properties; validate with seismic and regional geology; update model with new data",
        entity_scope="Reservoirs with active aquifer support (common in sandstone, carbonate)",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Aquifer influx models require assumptions and history matching; high uncertainty in aquifer properties",
        controlling_precedent="van Everdingen-Hurst and Carter-Tracy models are industry-standard but parameter selection is interpretive"
    ),

    DoctrineBlock(
        topic="Water Saturation from Well Logs - Archie Equation",
        keywords=["water saturation", "Archie equation", "resistivity log", "porosity", "cementation", "saturation exponent"],
        conclusion_template=[
            "Archie equation calculates water saturation Sw from resistivity log and porosity.",
            "Sw = (a × Rw / (φ^m × Rt))^(1/n) where Rw=water resistivity, Rt=formation resistivity.",
            "Accurate Sw requires calibration of cementation exponent m and saturation exponent n."
        ],
        reasoning_framework=[
            "Water saturation Sw = fraction of pore space occupied by water",
            "Oil saturation So = 1 - Sw (assumes no gas or Sg=0)",
            "Archie (1942) empirical relationship for clean sandstone",
            "Formation resistivity Rt measured by induction or laterolog (deep reading)",
            "Water resistivity Rw from water sample or SP log (spontaneous potential)",
            "Porosity φ from density, neutron, or sonic log",
            "Cementation exponent m relates porosity to formation factor F = a / φ^m",
            "Typical: a=1.0, m=2.0 for sandstone; m=1.8-2.2 range",
            "Saturation exponent n typically 2.0 (Archie's original); range 1.8-2.5",
            "Higher n means more oil-wet or complex pore structure",
            "Archie assumes: clean rock (no clay), water-wet, isotropic pores",
            "Shaly sands violate clean rock assumption (clay conductivity)",
            "Shale corrections: Simandoux, Indonesia, Waxman-Smits models",
            "Carbonate rocks: variable pore types (vuggy, fracture, intergranular) affect m and n",
            "Core calibration: measure Rt, Sw, φ on core plugs; regress for m and n",
            "Capillary pressure Pc relates to Sw (height above free water level)",
            "Transition zone: Sw decreases with height above water contact (Pc increases)",
            "Irreducible water saturation Swirr at top of oil column (Pc maximum)",
            "Log-derived Sw used for reserves calculation: N = 7758 × A × h × φ × (1 - Sw) / Bo",
            "Uncertainty in Sw propagates to reserves uncertainty (±5% Sw → ±10% OOIP)"
        ],
        key_factors=[
            "Formation resistivity Rt accuracy (tool calibration, borehole conditions)",
            "Water resistivity Rw (temperature, salinity)",
            "Porosity φ accuracy (lithology, fluid effects)",
            "Cementation exponent m (rock type, pore geometry)",
            "Saturation exponent n (wettability, pore complexity)",
            "Shale volume and clay conductivity (if shaly)",
            "Invasion effects (mud filtrate alters Sw near wellbore)"
        ],
        primary_authority=[
            "Archie, G.E. - The Electrical Resistivity Log as an Aid in Determining Reservoir Characteristics (1942)",
            "Schlumberger Log Interpretation Principles/Applications (1989)",
            "Tiab, D. and Donaldson, E.C. - Petrophysics (Gulf Publishing 2004)",
            "Asquith, G. and Krygowski, D. - Basic Well Log Analysis (AAPG 2004)"
        ],
        burden_holder="Operator (must determine Sw for reserves and well planning)",
        adversary_position="Disputes Sw values; claims logs over-estimate water (under-estimate oil)",
        counter_arguments=[
            "Archie equation calibration uncertain without core data",
            "Shaly sands require corrections (Archie invalid)",
            "Invasion by mud filtrate reduces Sw near wellbore (logs read flushed zone)",
            "Fractures and vugs cause heterogeneous Sw not captured by logs",
            "Fresh water zones (low salinity) have high resistivity (Sw under-estimated)"
        ],
        resolution_strategy="Calibrate Archie parameters with core data; use shale corrections in shaly intervals; use deep resistivity tools to minimize invasion effects; compare with capillary pressure Sw from core",
        entity_scope="All well log interpretation for reservoir characterization",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Archie equation well-validated in clean sandstones; requires calibration and corrections in complex lithologies",
        controlling_precedent="Archie equation is industry-standard for Sw from logs; SEC accepts for reserves if properly calibrated"
    ),

    DoctrineBlock(
        topic="Produced Water Salinity and Water Type Identification",
        keywords=["salinity", "TDS", "water chemistry", "chloride", "sulfate", "formation water", "injection water"],
        conclusion_template=[
            "Water salinity and ion composition identify water source: formation, injection, or aquifer.",
            "Total dissolved solids (TDS) and major ion ratios fingerprint water types.",
            "Geochemical analysis distinguishes breakthrough water from coning or channeling."
        ],
        reasoning_framework=[
            "Produced water chemistry varies with source: formation, injected, or aquifer",
            "Total dissolved solids (TDS) = sum of all dissolved ions (mg/L or ppm)",
            "Formation water: typically high TDS (10,000-300,000 mg/L) from long residence time",
            "Injection water: lower TDS if from surface source or treated produced water",
            "Aquifer water: variable TDS depending on aquifer type and connectivity",
            "Major ions: Na+, Ca2+, Mg2+, Cl-, SO4^2-, HCO3-",
            "Chloride dominant anion in most oilfield brines",
            "Sulfate high in seawater injection or aquifers with gypsum/anhydrite",
            "Calcium and magnesium from dissolution of carbonate minerals",
            "Sodium-chloride type water = typical formation brine",
            "Sodium-bicarbonate type = meteoric water or CO2-charged aquifer",
            "Ion ratios as fingerprints: Cl/Br (bromide conservative tracer), Na/Cl, Ca/Mg, SO4/Cl",
            "Mixing calculations: (Cmix - C1) / (C2 - C1) = fraction of water type 2",
            "Where Cmix = measured concentration, C1 and C2 = endmember concentrations",
            "Isotope analysis (δ18O, δD) distinguishes meteoric vs evaporated water",
            "Strontium isotopes (87Sr/86Sr) identify formation age and source",
            "Sudden change in salinity indicates new water source (breakthrough, aquifer influx, leak)",
            "Decreased TDS suggests injection water breakthrough (if injecting lower salinity)",
            "Increased sulfate suggests seawater injection breakthrough (if injecting seawater)",
            "Regulatory: EPA requires discharge monitoring for TDS, Cl, metals, hydrocarbons",
            "Scaling potential: high Ca, Ba, Sr with sulfate → BaSO4, SrSO4, CaSO4 scale"
        ],
        key_factors=[
            "TDS concentration and major ion composition",
            "Formation water baseline chemistry (pre-injection)",
            "Injection water chemistry (if waterflood active)",
            "Aquifer water chemistry (if aquifer influx possible)",
            "Sampling point (wellhead, separator, test separator)",
            "Sample handling (preservation, filtration, acidification)",
            "Analytical accuracy (certified lab, QA/QC)"
        ],
        primary_authority=[
            "API RP 45 - Recommended Practice for Analysis of Oilfield Waters",
            "ASTM D3352 - Standard Test Method for Strontium Ion in Brackish Water",
            "SPE 21113 - Use of Chemical and Isotopic Tracers for Reservoir Characterization",
            "Collins, A.G. - Geochemistry of Oilfield Waters (Elsevier 1975)"
        ],
        burden_holder="Operator (must identify water source for production optimization)",
        adversary_position="Claims water chemistry insufficient to prove water source; demands isotope analysis",
        counter_arguments=[
            "Ion ratios may overlap between water types (non-unique fingerprint)",
            "Mixing of multiple sources complicates interpretation",
            "Sampling contamination (mud, treating chemicals) alters chemistry",
            "Analytical variability introduces uncertainty",
            "Isotope and trace element analysis expensive (not routine)"
        ],
        resolution_strategy="Establish baseline formation water chemistry pre-waterflood; sample injection water regularly; use ion ratios and TDS trends to identify mixing; use isotopes for definitive source identification in critical cases",
        entity_scope="Waterflood projects and wells with multiple potential water sources",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Major ion chemistry provides reliable screening tool; isotopes provide definitive identification",
        controlling_precedent="API RP 45 standard methods for water analysis widely accepted"
    ),

    DoctrineBlock(
        topic="Waterflood Conformance - Gel and Polymer Treatments",
        keywords=["conformance", "gel treatment", "polymer", "sweep efficiency", "channeling", "crosslinker"],
        conclusion_template=[
            "Conformance treatments reduce water channeling through high-permeability zones.",
            "Polymer gels and foams block water flow, redirecting injection to unswept regions.",
            "Treatment design requires reservoir characterization and flow simulation to target zones."
        ],
        reasoning_framework=[
            "Conformance = distribution of injected water across reservoir thickness and area",
            "Poor conformance: water channels through high-perm zones, bypassing oil in low-perm",
            "Causes: permeability heterogeneity, fractures, thief zones, viscous fingering",
            "Polymer flooding increases water viscosity (improves mobility ratio)",
            "Partially hydrolyzed polyacrylamide (HPAM) typical polymer (MW 1-30 million Daltons)",
            "Polymer concentration 500-2,000 ppm; viscosity 10-100 cp at shear rate",
            "Injectivity reduced (higher pressure) but sweep improved (more oil contacted)",
            "Gel treatments for near-well conformance (injector or producer)",
            "Polymer + crosslinker → gel forms in situ over hours to days",
            "Crosslinkers: chromium acetate, aluminum citrate, phenol-formaldehyde, organic (PEI)",
            "Gelant injected into high-perm zone; gels and blocks flow; water diverts to low-perm",
            "Placement critical: use logs, tracers, flow profiling to identify thief zones",
            "Bullhead injection (down tubing) or selective (straddle packer, coiled tubing)",
            "Gel strength tailored to permeability contrast and pressure gradient",
            "Weak gel for moderate permeability contrast; strong gel for fractures",
            "Temperature affects gelation time (faster at higher temp; design for reservoir T)",
            "Salinity and pH affect crosslinking (optimize for formation water chemistry)",
            "Foam treatments: gas + surfactant → foam reduces gas mobility in high-perm zones",
            "Microbial treatments: bacteria produce biopolymer in situ (experimental)",
            "Risk: over-treatment blocks all flow (requires remediation by acid or breaker)",
            "Monitoring: pressure response, tracer breakthrough, production logging post-treatment"
        ],
        key_factors=[
            "Permeability contrast and distribution (logs, core, RFT)",
            "Thief zone identification (tracers, production logs, temperature surveys)",
            "Gel chemistry selection (polymer type, crosslinker, concentration)",
            "Reservoir temperature and salinity (affects gelation)",
            "Placement method (bullhead vs selective)",
            "Treatment volume (pore volumes in thief zone)",
            "Post-treatment monitoring (pressure, production, water cut)"
        ],
        primary_authority=[
            "SPE 89468 - Conformance Improvement Using Gels (2004)",
            "Seright, R.S. - Polymer Flooding (in Lake, L.W., Enhanced Oil Recovery, 1989)",
            "SPE 77411 - Gel Treatments in Production Wells (2002)",
            "Sorbie, K.S. - Polymer-Improved Oil Recovery (CRC Press 1991)"
        ],
        burden_holder="Operator (must improve conformance to maximize recovery)",
        adversary_position="Claims gel treatment damaged productive zones and reduced oil production",
        counter_arguments=[
            "Over-treatment can block oil-productive zones (reduced oil rate)",
            "Gel placement uncertain (may not reach intended zone)",
            "Effectiveness temporary (gel degrades over time)",
            "High cost and operational risk (workover, lost production)",
            "Polymer adsorption reduces injectivity permanently"
        ],
        resolution_strategy="Use production logs and tracers to identify thief zones; design gel chemistry for reservoir conditions; inject conservatively with pressure monitoring; evaluate with post-treatment logs and production data",
        entity_scope="Waterflood projects with channeling and poor conformance",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Gel treatments can improve conformance but success variable; requires careful design and placement",
        controlling_precedent="No regulatory standard; design based on SPE literature and service company experience"
    ),

    DoctrineBlock(
        topic="Economic Limit - Oil Price Sensitivity and Operating Cost",
        keywords=["economic limit", "operating cost", "netback", "oil price", "abandonment", "PV10"],
        conclusion_template=[
            "Economic limit reached when well revenue falls below operating cost (negative netback).",
            "Operating cost includes lifting, water handling, overhead, and workover amortization.",
            "Oil price volatility shifts economic limit; low prices force earlier abandonment."
        ],
        reasoning_framework=[
            "Economic limit = production rate where revenue equals operating cost (breakeven)",
            "Revenue = qo × (oil_price - differential) where differential = quality/transport deduction",
            "Operating cost (opex) = lifting + water_disposal + electricity + overhead + maintenance",
            "Lifting cost per barrel ($/BOE or $/bbl liquid) increases with water cut",
            "Example: $8/bbl liquid lifting cost at 90% water cut → $80/bbl oil (qo/qt = 0.1)",
            "Water disposal cost: $0.50-$5/bbl depending on method (injection, evaporation, discharge)",
            "Electricity for ESP/rod pump major cost component (scales with liquid rate and depth)",
            "Gas lift: cost = gas volume × gas value (opportunity cost)",
            "Workover cost amortized over expected incremental production",
            "Overhead allocation (field staff, facilities, G&A) per well or per BOE",
            "Netback = revenue - opex - capex (per bbl basis)",
            "Negative netback sustained → shut-in or abandon well",
            "Regulatory: may require plugging and abandonment (P&A) when production ceases",
            "P&A cost $50K-$500K depending on depth and complexity (removes future liability)",
            "PV10 = present value of future revenue - opex at 10% discount (SEC reserves metric)",
            "PDP reserves include only economic production (netback > 0)",
            "Oil price forecast affects reserves and economic limit (SEC uses historical average)",
            "Sensitivity analysis: economic limit water cut vs oil price",
            "Example: at $50/bbl, limit at 95% WC; at $80/bbl, limit at 98% WC",
            "Tax relief or royalty reduction may extend economic life (lower effective opex)",
            "Recompletion to new zone or workover may restore economics vs abandonment"
        ],
        key_factors=[
            "Oil price (WTI, Brent, local) and price differential",
            "Operating cost structure (lifting, disposal, power, overhead)",
            "Water cut and total liquid rate (affect $/BOE)",
            "Artificial lift type and efficiency (power cost)",
            "Water disposal method and cost",
            "Regulatory requirements (monitoring, reporting, P&A bonding)",
            "Tax and royalty rates (affect netback)"
        ],
        primary_authority=[
            "SEC Regulation S-X Rule 4-10 - Financial Accounting and Reporting for Oil and Gas",
            "SPE PRMS - Petroleum Resources Management System (2018)",
            "API Bulletin D11 - Economic Considerations for Oil and Gas Well Abandonment",
            "DOE - Marginal Well Report and Economic Analysis"
        ],
        burden_holder="Operator (must justify continued operation or abandon when uneconomic)",
        adversary_position="Royalty owner or regulator claims premature abandonment; operator should invest in workover",
        counter_arguments=[
            "Workover cost may not be recovered at current oil price",
            "Remaining reserves too small to justify continued operation",
            "Facility maintenance costs exceed well revenue (field economics)",
            "Environmental liability accumulates with extended operation",
            "P&A now cheaper than delayed P&A (regulatory escalation)"
        ],
        resolution_strategy="Calculate economic limit water cut for range of oil prices; forecast when limit reached; evaluate workover economics vs P&A; communicate plan to stakeholders; comply with regulatory P&A requirements",
        entity_scope="All producing wells approaching economic limit",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Economic calculation straightforward; oil price forecast uncertain; operator discretion within regulatory limits",
        controlling_precedent="SEC rules and state conservation regulations govern reserves booking and abandonment timing"
    ),

    DoctrineBlock(
        topic="Water Production Forecasting - Koval and X-plot Methods",
        keywords=["water production forecast", "Koval factor", "X-plot", "WOR prediction", "reserves"],
        conclusion_template=[
            "Water production forecasting uses Koval method or X-plot to extrapolate WOR trends.",
            "Koval factor adjusts for reservoir heterogeneity and adverse mobility.",
            "X-plot linearizes WOR vs cumulative oil for straight-line extrapolation to economic limit."
        ],
        reasoning_framework=[
            "Accurate water production forecast required for reserves, facility sizing, economics",
            "Historical WOR or water cut vs cumulative oil provides baseline trend",
            "Koval (1963) method for heterogeneous reservoirs with viscous fingering",
            "Effective fractional flow curve adjusted by Koval factor K",
            "K = sqrt(V_dp × M_eff) where V_dp = Dykstra-Parsons coefficient, M_eff = effective mobility ratio",
            "Higher K (>1) means more heterogeneity and earlier breakthrough",
            "Forecast water cut from effective fractional flow curve using Koval-adjusted saturation",
            "Requires relative permeability data and permeability distribution (V_dp from logs/core)",
            "X-plot (Ershaghi-Omoregie 1978): plot log(WOR) vs log(Np) or log(WOR) vs Np",
            "Linear trend on semi-log or log-log plot extrapolates to economic limit WOR",
            "Economic limit WOR = (Lifting cost + Water disposal cost) / (Oil price - Operating cost)",
            "Cumulative oil at economic limit Np_limit = intercept from X-plot extrapolation",
            "Remaining reserves = Np_limit - Np_current",
            "Chan plot (log-log WOR vs Np) identifies mechanism changes (slope breaks)",
            "Normal waterflood: slope ~1 on Chan plot (Buckley-Leverett behavior)",
            "Coning or channeling: slope >1 (accelerating water)",
            "Forecast assumes mechanism continues; operational changes invalidate trend",
            "Combine with Arps oil decline for full production forecast",
            "Uncertainty: oil price, operating cost, operational changes (conformance, rate)",
            "Use P10/P50/P90 scenarios for reserves (range of economic limit WOR)"
        ],
        key_factors=[
            "Historical WOR or water cut data quality and duration",
            "Reservoir heterogeneity (V_dp from logs)",
            "Relative permeability and mobility ratio",
            "Operational changes (rate, pressure, conformance treatments)",
            "Oil price and cost forecast (affects economic limit WOR)",
            "Facility constraints (separator, disposal capacity)",
            "Regulatory requirements (SEC, state conservation)"
        ],
        primary_authority=[
            "Koval, E.J. - A Method for Predicting the Performance of Unstable Miscible Displacement (SPE 450, 1963)",
            "Ershaghi, I. and Omoregie, O. - A Method for Extrapolation of Cut vs Recovery Curves (JPT 1978)",
            "Lo, K.K. et al - Decline Curve Analysis Using Type Curves for Two-Phase Flow (JPT 1990)",
            "SPE PRMS - Petroleum Resources Management System (reserves definitions)"
        ],
        burden_holder="Operator (must forecast water production for reserves and facility planning)",
        adversary_position="Disputes forecast as overly optimistic (claims higher water cut, less reserves)",
        counter_arguments=[
            "Historical trend may not continue (conformance, coning, rate changes)",
            "Heterogeneity not adequately characterized (V_dp uncertain)",
            "Economic limit WOR assumption optimistic (oil price decline, cost increase)",
            "X-plot extrapolation beyond data range unreliable",
            "Facility constraints may force earlier abandonment than economic limit"
        ],
        resolution_strategy="Use multiple methods (Koval, X-plot, Chan plot); compare with analog fields; update forecast with actual data; sensitivity on economic limit WOR; document assumptions for reserves auditor",
        entity_scope="All waterflood reservoirs requiring reserves estimation and production forecasting",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Forecasting methods empirical with significant uncertainty; use ranges not single values",
        controlling_precedent="SEC and SPE PRMS require reasonable certainty for reserves; forecasting methodology documented in reserves report"
    )
]

# ============================================================================
# METRICS & TELEMETRY
# ============================================================================

class EngineMetrics:
    def __init__(self):
        self.total_queries = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_latency_ms = 0.0
        self.error_count = 0
        self.start_time = datetime.now(timezone.utc)
        self.triggered_doctrines: Dict[str, int] = {}
        self.missed_doctrines: Dict[str, int] = {}

    def record_query(self, latency_ms: float, triggered: List[str], missed: List[str], hit_cache: bool):
        self.total_queries += 1
        self.total_latency_ms += latency_ms
        if hit_cache:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        for topic in triggered:
            self.triggered_doctrines[topic] = self.triggered_doctrines.get(topic, 0) + 1
        for topic in missed:
            self.missed_doctrines[topic] = self.missed_doctrines.get(topic, 0) + 1

    def record_error(self):
        self.error_count += 1

    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / self.total_queries if self.total_queries > 0 else 0.0

    @property
    def cache_hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0

    @property
    def uptime_seconds(self) -> float:
        return (datetime.now(timezone.utc) - self.start_time).total_seconds()

# ============================================================================
# SEMANTIC NORMALIZATION
# ============================================================================

WATER_CUT_SYNONYMS = {
    "water cut": ["water fraction", "water percentage", "WC", "water content", "water production ratio"],
    "water-oil ratio": ["WOR", "water oil ratio", "water to oil ratio", "produced water ratio"],
    "BSW": ["basic sediment and water", "basic sediment water", "bottom sediment water", "BS&W"],
    "breakthrough": ["water breakthrough", "BT", "first water", "water arrival"],
    "emulsion": ["tight emulsion", "emulsified oil", "oil-water emulsion", "rag layer"],
    "separator": ["oil-water separator", "FWKO", "free water knockout", "API separator"],
    "injection": ["water injection", "waterflood", "water flood", "secondary recovery"],
    "disposal": ["water disposal", "saltwater disposal", "SWD", "disposal well"],
    "coning": ["water coning", "water cresting", "bottom water coning", "cone formation"],
    "aquifer": ["water drive", "aquifer influx", "edge water", "bottom water"]
}

def normalize_term(text: str) -> str:
    """Normalize water cut domain terminology."""
    text_lower = text.lower()
    for canonical, synonyms in WATER_CUT_SYNONYMS.items():
        for syn in synonyms:
            if syn in text_lower:
                text_lower = text_lower.replace(syn, canonical)
    return text_lower

# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

class PROD06Engine:
    def __init__(self):
        self.metrics = EngineMetrics()
        self.doctrine_cache = DOCTRINE_CACHE
        logger.info(f"{ENGINE_NAME} v{VERSION} initialized with {len(self.doctrine_cache)} doctrine blocks")

    def apply_epistemic_guardrails(self, text: str) -> str:
        """Remove banned phrases and add disclosure caveat."""
        result = text
        for phrase in BANNED_PHRASES:
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            result = pattern.sub("[EPISTEMIC GUARDRAIL REMOVED]", result)
        return result

    def semantic_search_doctrines(self, query: str, top_k: int = 5) -> List[DoctrineBlock]:
        """Semantic search through doctrine cache based on keyword matching."""
        query_normalized = normalize_term(query)
        query_terms = set(query_normalized.lower().split())

        scores = []
        for doctrine in self.doctrine_cache:
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_normalized)
            topic_match = 2 if any(term in doctrine.topic.lower() for term in query_terms) else 0
            score = keyword_matches + topic_match
            scores.append((score, doctrine))

        scores.sort(reverse=True, key=lambda x: x[0])
        return [doc for score, doc in scores[:top_k] if score > 0]

    def multi_doctrine_decomposition(self, query: str) -> Dict[str, Any]:
        """Decompose query into issue categories and identify doctrine interactions."""
        categories = []
        query_lower = query.lower()

        # Category detection
        if any(term in query_lower for term in ["water cut", "WC%", "water fraction"]):
            categories.append(IssueCategory.WATER_CUT_CALCULATION)
        if any(term in query_lower for term in ["BSW", "basic sediment", "centrifuge", "karl fischer"]):
            categories.append(IssueCategory.BSW_MEASUREMENT)
        if any(term in query_lower for term in ["waterflood", "injection", "breakthrough", "pattern"]):
            categories.append(IssueCategory.WATERFLOOD_PERFORMANCE)
        if any(term in query_lower for term in ["coning", "aquifer", "encroachment"]):
            categories.append(IssueCategory.BREAKTHROUGH_PREDICTION)
        if any(term in query_lower for term in ["WOR", "decline", "forecast", "economic limit"]):
            categories.append(IssueCategory.DECLINE_ANALYSIS)
        if any(term in query_lower for term in ["disposal", "treatment", "separator"]):
            categories.append(IssueCategory.PRODUCED_WATER_HANDLING)
        if any(term in query_lower for term in ["injection quality", "suspended solids", "bacteria"]):
            categories.append(IssueCategory.INJECTION_WATER_QUALITY)
        if any(term in query_lower for term in ["chan plot", "diagnostic", "x-plot"]):
            categories.append(IssueCategory.DIAGNOSTIC_PLOTS)
        if any(term in query_lower for term in ["emulsion", "demulsifier", "tight emulsion"]):
            categories.append(IssueCategory.SEPARATION_EFFICIENCY)
        if any(term in query_lower for term in ["permit", "UIC", "discharge", "regulation"]):
            categories.append(IssueCategory.REGULATORY_COMPLIANCE)

        if not categories:
            categories.append(IssueCategory.WATER_CUT_CALCULATION)  # Default

        return {
            "categories": categories,
            "interaction_dag": self._build_interaction_dag(categories),
            "complexity": "high" if len(categories) > 2 else "medium" if len(categories) == 2 else "low"
        }

    def _build_interaction_dag(self, categories: List[IssueCategory]) -> List[Tuple[str, str]]:
        """Build directed acyclic graph of doctrine interactions."""
        interactions = []
        if IssueCategory.BSW_MEASUREMENT in categories and IssueCategory.WATER_CUT_CALCULATION in categories:
            interactions.append(("BSW_MEASUREMENT", "WATER_CUT_CALCULATION"))
        if IssueCategory.WATERFLOOD_PERFORMANCE in categories and IssueCategory.BREAKTHROUGH_PREDICTION in categories:
            interactions.append(("WATERFLOOD_PERFORMANCE", "BREAKTHROUGH_PREDICTION"))
        if IssueCategory.BREAKTHROUGH_PREDICTION in categories and IssueCategory.DECLINE_ANALYSIS in categories:
            interactions.append(("BREAKTHROUGH_PREDICTION", "DECLINE_ANALYSIS"))
        if IssueCategory.PRODUCED_WATER_HANDLING in categories and IssueCategory.REGULATORY_COMPLIANCE in categories:
            interactions.append(("PRODUCED_WATER_HANDLING", "REGULATORY_COMPLIANCE"))
        return interactions

    def fact_fragility_scoring(self, answer: str, sources: List[str]) -> Dict[str, Any]:
        """Score fact fragility based on verifiability and source quality."""
        # Check source authority
        peer_reviewed = sum(1 for s in sources if any(term in s for term in ["SPE", "ASTM", "API", "JPT"]))
        regulatory = sum(1 for s in sources if any(term in s for term in ["EPA", "CFR", "Rule", "Regulation"]))

        # Verifiability score
        verifiable_statements = len(re.findall(r'\d+', answer))  # Numeric claims
        hedge_words = len(re.findall(r'\b(may|might|could|possibly|typically|generally)\b', answer, re.IGNORECASE))

        fragility_score = max(0, 10 - peer_reviewed * 2 - regulatory * 2 + hedge_words - verifiable_statements * 0.5)

        return {
            "fragility_score": min(10, fragility_score),
            "verifiability": "high" if verifiable_statements > 5 else "medium" if verifiable_statements > 2 else "low",
            "source_quality": "high" if (peer_reviewed + regulatory) > 3 else "medium" if (peer_reviewed + regulatory) > 1 else "low",
            "recharacterization_risk": "high" if hedge_words > 5 else "medium" if hedge_words > 2 else "low"
        }

    def three_layer_response(self, query: str, mode: ResponseMode, zone: ZoneType) -> Tuple[str, List[str], List[str], ConfidenceLevel]:
        """
        Three-layer response architecture:
        1. Doctrine Cache (0-200ms)
        2. Semantic Retrieval (200-2000ms)
        3. Deep Analysis (2000ms+)
        """
        start_time = datetime.now(timezone.utc)

        # Layer 1: Doctrine Cache
        triggered_doctrines = []
        answer_components = []
        sources = []

        cache_matches = self.semantic_search_doctrines(query, top_k=3)
        if cache_matches:
            triggered_doctrines = [d.topic for d in cache_matches]
            for doctrine in cache_matches:
                answer_components.append(f"**{doctrine.topic}**\n" + "\n".join(doctrine.conclusion_template))
                sources.extend(doctrine.primary_authority)

            cache_latency = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            if cache_latency < 200 and mode == ResponseMode.FAST:
                # Fast path: return cache results only
                answer = "\n\n".join(answer_components)
                answer = self.apply_epistemic_guardrails(answer)
                return answer, sources, triggered_doctrines, ConfidenceLevel.DEFENSIBLE

        # Layer 2: Semantic Retrieval (if cache insufficient or DEFENSE/MEMO mode)
        decomposition = self.multi_doctrine_decomposition(query)
        categories = decomposition["categories"]

        # Add reasoning from matched doctrines
        if mode in [ResponseMode.DEFENSE, ResponseMode.MEMO]:
            for doctrine in cache_matches[:2]:
                reasoning = "\n".join(doctrine.reasoning_framework[:10])  # First 10 lines
                answer_components.append(f"\n**Reasoning ({doctrine.topic}):**\n{reasoning}")

        # Layer 3: Deep Analysis (MEMO mode only)
        if mode == ResponseMode.MEMO:
            deep_analysis = self._deep_analysis(query, cache_matches, decomposition)
            answer_components.append(f"\n**Deep Analysis:**\n{deep_analysis}")

        answer = "\n\n".join(answer_components)
        answer = self.apply_epistemic_guardrails(answer)

        # Add disclosure caveat for DEFENSE/MEMO
        if mode in [ResponseMode.DEFENSE, ResponseMode.MEMO]:
            answer += f"\n\n**Disclosure:** {DISCLOSURE_CAVEAT}"

        # Determine confidence
        confidence = self._determine_confidence(cache_matches, zone, mode)

        # Identify missed doctrines
        all_topics = {d.topic for d in self.doctrine_cache}
        missed = list(all_topics - set(triggered_doctrines))

        return answer, sources, triggered_doctrines, confidence

    def _deep_analysis(self, query: str, matched_doctrines: List[DoctrineBlock], decomposition: Dict) -> str:
        """Generate deep analysis with multi-doctrine synthesis."""
        analysis_parts = []

        # Issue complexity
        categories = decomposition["categories"]
        analysis_parts.append(f"Issue involves {len(categories)} categories: {', '.join([c.value for c in categories])}")

        # Doctrine interactions
        if decomposition["interaction_dag"]:
            interactions = ", ".join([f"{a} → {b}" for a, b in decomposition["interaction_dag"]])
            analysis_parts.append(f"Doctrine interactions: {interactions}")

        # Adversarial considerations
        if matched_doctrines:
            adversary_positions = [d.adversary_position for d in matched_doctrines[:2]]
            analysis_parts.append(f"Adversarial positions to consider: {'; '.join(adversary_positions)}")

        # Key uncertainties
        key_factors = []
        for doctrine in matched_doctrines[:2]:
            key_factors.extend(doctrine.key_factors[:3])
        if key_factors:
            analysis_parts.append(f"Key factors affecting outcome: {', '.join(key_factors[:5])}")

        return "\n\n".join(analysis_parts)

    def _determine_confidence(self, matched_doctrines: List[DoctrineBlock], zone: ZoneType, mode: ResponseMode) -> ConfidenceLevel:
        """Determine confidence level based on doctrine support and context."""
        if not matched_doctrines:
            return ConfidenceLevel.HIGH_RISK

        # Aggregate doctrine confidence
        confidence_levels = [d.confidence for d in matched_doctrines]
        if all(c == ConfidenceLevel.DEFENSIBLE for c in confidence_levels):
            base_confidence = ConfidenceLevel.DEFENSIBLE
        elif any(c == ConfidenceLevel.HIGH_RISK for c in confidence_levels):
            base_confidence = ConfidenceLevel.HIGH_RISK
        elif any(c == ConfidenceLevel.AGGRESSIVE for c in confidence_levels):
            base_confidence = ConfidenceLevel.AGGRESSIVE
        else:
            base_confidence = ConfidenceLevel.DISCLOSURE

        # Zone adjustments
        if zone == ZoneType.AUDIT:
            if base_confidence == ConfidenceLevel.AGGRESSIVE:
                return ConfidenceLevel.DISCLOSURE
        elif zone == ZoneType.PLANNING:
            pass  # No adjustment

        return base_confidence

    def generate_determinism_hash(self, query: str, answer: str, mode: ResponseMode, zone: ZoneType) -> str:
        """Generate SHA-256 hash for response reproducibility."""
        content = f"{query}|{answer}|{mode.value}|{zone.value}|{VERSION}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]

    def audit_log(self, query: str, response: QueryResponse):
        """Append query and response to JSONL audit trail."""
        try:
            log_entry = {
                "timestamp": response.timestamp,
                "query": query,
                "mode": response.mode.value,
                "zone": response.zone.value,
                "confidence": response.confidence.value,
                "triggered_doctrines": response.triggered_doctrines,
                "determinism_hash": response.determinism_hash,
                "answer_length": len(response.answer),
                "source_count": len(response.sources)
            }
            with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            logger.error(f"Audit log write failed: {e}")

    async def query(self, request: QueryRequest) -> QueryResponse:
        """Main query endpoint."""
        start_time = datetime.now(timezone.utc)

        try:
            answer, sources, triggered, confidence = self.three_layer_response(
                request.question, request.mode, request.zone
            )

            # Missed doctrines
            all_topics = {d.topic for d in self.doctrine_cache}
            missed = list(all_topics - set(triggered))

            # Build response
            response = QueryResponse(
                answer=answer,
                confidence=confidence,
                sources=list(set(sources)),  # Deduplicate
                reasoning_chain=[f"Triggered doctrines: {', '.join(triggered)}"],
                triggered_doctrines=triggered,
                missed_doctrines=missed[:5],  # Top 5 missed
                determinism_hash=self.generate_determinism_hash(request.question, answer, request.mode, request.zone),
                mode=request.mode,
                zone=request.zone,
                timestamp=datetime.now(timezone.utc).isoformat(),
                disclosure=DISCLOSURE_CAVEAT if request.mode in [ResponseMode.DEFENSE, ResponseMode.MEMO] else ""
            )

            # Metrics
            latency_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            hit_cache = len(triggered) > 0
            self.metrics.record_query(latency_ms, triggered, missed, hit_cache)

            # Audit log
            self.audit_log(request.question, response)

            logger.info(f"Query processed: {len(answer)} chars, {len(triggered)} doctrines, {latency_ms:.1f}ms")
            return response

        except Exception as e:
            self.metrics.record_error()
            logger.error(f"Query failed: {e}")
            raise HTTPException(status_code=500, detail=f"Query processing error: {str(e)}")

    def health(self) -> HealthResponse:
        """Health check endpoint."""
        return HealthResponse(
            status="healthy",
            engine_id=ENGINE_ID,
            version=VERSION,
            port=PORT,
            doctrine_count=len(self.doctrine_cache),
            uptime_seconds=self.metrics.uptime_seconds,
            total_queries=self.metrics.total_queries,
            avg_latency_ms=self.metrics.avg_latency_ms,
            cache_hit_rate=self.metrics.cache_hit_rate
        )

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    description="TIE-Grade Water Cut Analysis Engine for petroleum production operations"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = PROD06Engine()

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Process water cut analysis query."""
    return await engine.query(request)

@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Engine health check."""
    return engine.health()

@app.get("/doctrines")
async def doctrines_endpoint():
    """List all doctrine topics."""
    return {
        "total": len(DOCTRINE_CACHE),
        "topics": [d.topic for d in DOCTRINE_CACHE],
        "categories": list(set(d.topic.split(" - ")[0] if " - " in d.topic else d.topic for d in DOCTRINE_CACHE))
    }

@app.get("/metrics")
async def metrics_endpoint():
    """Detailed metrics."""
    return {
        "total_queries": engine.metrics.total_queries,
        "cache_hit_rate": engine.metrics.cache_hit_rate,
        "avg_latency_ms": engine.metrics.avg_latency_ms,
        "error_count": engine.metrics.error_count,
        "uptime_seconds": engine.metrics.uptime_seconds,
        "top_triggered_doctrines": sorted(
            engine.metrics.triggered_doctrines.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10],
        "top_missed_doctrines": sorted(
            engine.metrics.missed_doctrines.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
    }

@app.on_event("startup")
async def startup_event():
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    logger.info(f"Audit trail: {AUDIT_LOG_PATH}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"{ENGINE_NAME} shutting down. Total queries: {engine.metrics.total_queries}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
