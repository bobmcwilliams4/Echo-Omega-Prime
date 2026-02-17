"""
PROD10 Pipeline Flow Assurance Intelligence Engine
TIE-Grade Production Intelligence System

Analyzes pipeline flow assurance challenges including hydrate formation,
wax deposition, asphaltene precipitation, scale formation, slugging, and
multiphase flow in production pipelines.

Port: 9225
Version: 1.0.0
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
    HYDRATE_FORMATION = "HYDRATE_FORMATION"
    WAX_DEPOSITION = "WAX_DEPOSITION"
    ASPHALTENE_PRECIPITATION = "ASPHALTENE_PRECIPITATION"
    SCALE_FORMATION = "SCALE_FORMATION"
    TERRAIN_SLUGGING = "TERRAIN_SLUGGING"
    HYDRODYNAMIC_SLUGGING = "HYDRODYNAMIC_SLUGGING"
    MULTIPHASE_FLOW = "MULTIPHASE_FLOW"
    PIGGING_OPERATIONS = "PIGGING_OPERATIONS"
    THERMAL_MANAGEMENT = "THERMAL_MANAGEMENT"
    CORROSION_EROSION = "CORROSION_EROSION"
    PRESSURE_DROP = "PRESSURE_DROP"
    FLOW_REGIME = "FLOW_REGIME"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


@dataclass
class DoctrineBlock:
    """Core doctrine block with pipeline flow assurance expertise"""
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
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    hit_count: int = 0
    last_triggered: Optional[str] = None


class QueryRequest(BaseModel):
    query: str = Field(..., description="Pipeline flow assurance query")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis zone")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class QueryResponse(BaseModel):
    answer: str
    mode: ResponseMode
    zone: AnalysisZone
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    processing_time_ms: float
    determinism_hash: str
    coverage_gaps: List[str]
    metadata: Dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrine_count: int
    total_queries: int
    avg_response_time_ms: float
    uptime_seconds: float
    cache_hit_rate: float


# ============================================================================
# PIPELINE FLOW ASSURANCE INTELLIGENCE ENGINE
# ============================================================================

class PipelineFlowAssuranceEngine:
    """TIE-Grade Pipeline Flow Assurance Intelligence Engine"""

    def __init__(self):
        self.version = "1.0.0"
        self.port = 9225
        self.start_time = time.time()

        # Telemetry
        self.metrics = {
            "total_queries": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_processing_time_ms": 0.0,
            "doctrine_triggers": defaultdict(int),
            "mode_usage": defaultdict(int),
            "zone_usage": defaultdict(int),
        }

        # Doctrine cache
        self.doctrine_cache: Dict[str, DoctrineBlock] = {}
        self._initialize_doctrine_cache()

        # Audit trail
        self.audit_log_path = Path(__file__).parent / "audit_trail.jsonl"

        # Coverage tracking
        self.coverage_map: Dict[str, int] = defaultdict(int)

        logger.info(f"PROD10 Pipeline Flow Assurance Engine v{self.version} initialized on port {self.port}")
        logger.info(f"Loaded {len(self.doctrine_cache)} doctrine blocks")

    def _initialize_doctrine_cache(self):
        """Initialize doctrine cache with pipeline flow assurance expertise"""

        # Hydrate Formation and Prediction
        self.doctrine_cache["HYDRATE_FORMATION_THERMODYNAMICS"] = DoctrineBlock(
            topic="Hydrate Formation Thermodynamic Prediction",
            keywords=["hydrate", "formation", "CSMHyd", "thermodynamic", "prediction", "equilibrium", "phase envelope"],
            conclusion_template="Hydrate formation risk assessment requires thermodynamic modeling using CSMHyd or equivalent. Pressure-temperature envelope defines safe operating zone. Gas composition drives hydrate stability region. Subcooling defines driving force for nucleation.",
            reasoning_framework="""
1. Gas Composition Analysis:
   - Measure gas composition (C1-C4, CO2, H2S, N2)
   - Identify hydrate formers (primarily C1-C3, CO2, H2S)
   - Calculate hydrate equilibrium curve using CSMHyd model
   - Determine structure I vs structure II hydrate formation

2. Thermodynamic Modeling:
   - Apply van der Waals-Platteeuw model for chemical potential
   - Use Peng-Robinson EOS for fluid phase equilibrium
   - Calculate hydrate dissociation temperature at operating pressure
   - Establish pressure-temperature (P-T) safety margin

3. Subcooling Assessment:
   - Subcooling = T_hydrate - T_operating
   - >5F subcooling = high risk zone
   - >10F subcooling = critical risk, immediate action required
   - Subcooling drives nucleation kinetics and growth rate

4. Water Activity Consideration:
   - Free water presence mandatory for hydrate formation
   - Water cut >3% significantly increases hydrate risk
   - Salinity reduces hydrate formation temperature by ~1.8F per 1% NaCl
   - Water-in-oil emulsions can form hydrates at interfaces

5. Kinetic Inhibition Window:
   - Low subcooling (<3F) may allow kinetic inhibitor use
   - High subcooling requires thermodynamic inhibitors (MEG, MeOH)
   - Nucleation induction time decreases exponentially with subcooling
   - Turbulence and nucleation sites reduce induction time

6. Operational Boundary Definition:
   - Plot P-T operating envelope against hydrate curve
   - Maintain minimum 5F safety margin above hydrate temperature
   - Monitor wellhead and pipeline temperature continuously
   - Depressurization crosses hydrate curve = high plug risk
            """,
            key_factors=[
                "Gas composition (C1-C4, CO2, H2S content)",
                "Operating pressure and temperature profile",
                "Subcooling degree (T_hydrate - T_operating)",
                "Water cut and salinity",
                "Nucleation sites (rust, scale, sand)",
                "Flow regime and turbulence intensity",
                "Residence time in hydrate formation zone"
            ],
            primary_authority=[
                "Sloan & Koh, Clathrate Hydrates of Natural Gases, 3rd Ed (2008)",
                "SPE 28506: Field Experience with Hydrate Inhibition",
                "API RP 14E: Recommended Practice for Design and Installation of Offshore Production Platform Piping Systems"
            ],
            burden_holder="Operator must prove safe operating conditions outside hydrate stability zone",
            adversary_position="Hydrate formation is unpredictable without real-time monitoring",
            counter_arguments=[
                "CSMHyd model validated against 5000+ experimental data points",
                "Commercial software (PVTSim, OLGA) use same thermodynamic foundation",
                "Field experience confirms P-T envelope predictions within 2-3F",
                "Hydrate plugs occur when operating inside predicted envelope",
                "Kinetic studies show subcooling is primary nucleation driver"
            ],
            resolution_strategy="Use validated thermodynamic models + real-time P-T monitoring + safety margin",
            entity_scope="All wet gas/condensate pipelines operating near hydrate formation conditions",
            confidence=ConfidenceLevel.DEFENSIBLE,
            confidence_stratification="Thermodynamic models are industry standard, validated by decades of field data",
            controlling_precedent="CSMHyd and van der Waals-Platteeuw model universally accepted in oil/gas industry"
        )

        self.doctrine_cache["HYDRATE_INHIBITION_MEG"] = DoctrineBlock(
            topic="Monoethylene Glycol (MEG) Hydrate Inhibition",
            keywords=["MEG", "monoethylene glycol", "thermodynamic inhibitor", "hydrate prevention", "concentration"],
            conclusion_template="MEG is the preferred thermodynamic hydrate inhibitor for high water cut systems. Required concentration follows Hammerschmidt equation. Regeneration and recirculation reduces chemical cost. Overdosing wastes chemical; underdosing risks plug formation.",
            reasoning_framework="""
1. MEG Concentration Calculation (Hammerschmidt Equation):
   - ΔT = (K * W) / (100 * MW - MW * W)
   - ΔT = depression (deg F), W = wt% inhibitor, MW = molecular weight, K = constant
   - For MEG: MW = 62, K = 2335
   - Typical concentrations: 30-80 wt% in aqueous phase

2. Injection Rate Determination:
   - Mass MEG = (Water rate) * (MEG wt%) / (100 - MEG wt%)
   - Account for MEG losses: salt precipitation, degradation, carryover
   - Typical loss rate: 0.1-0.5% of injected MEG per cycle
   - Overdosing margin: 5-10% above calculated minimum

3. Injection Point Selection:
   - Inject upstream of first hydrate formation point
   - Ensure complete mixing within 10 pipe diameters
   - Wellhead injection for offshore subsea tiebacks
   - Monitor MEG concentration in produced water downstream

4. MEG Regeneration Economics:
   - Regeneration unit recovers 99%+ of MEG from produced water
   - Distillation removes salts, achieves 80% lean MEG
   - Break-even water cut typically 15-20%
   - Regeneration justifies MEG vs methanol for high water production

5. Rich MEG Handling:
   - Rich MEG = produced water + MEG (30-50 wt%)
   - Flash separation removes hydrocarbon vapors
   - Salt precipitation in reboiler requires periodic cleaning
   - Corrosion control: pH adjustment, corrosion inhibitor addition

6. MEG Compatibility:
   - Compatible with most elastomers (avoid EPDM)
   - Density 1.11 g/cm3 at 60F, viscosity increases at low temperature
   - Monitor for MEG degradation products (acids)
   - MEG-water mixtures can freeze at high concentration (>60 wt%)
            """,
            key_factors=[
                "Subcooling degree (determines required MEG concentration)",
                "Water production rate (determines MEG injection rate)",
                "MEG regeneration capability (economics)",
                "Injection point and mixing effectiveness",
                "MEG losses and makeup requirements",
                "Produced water salinity (impacts regeneration)",
                "System materials compatibility"
            ],
            primary_authority=[
                "SPE 30696: Hydrate Inhibition with MEG in Offshore Production",
                "Hammerschmidt Equation (1934) - Industry Standard",
                "ISO 16530: Petroleum and Natural Gas Industries - Well Integrity"
            ],
            burden_holder="Operator must ensure adequate MEG concentration throughout system",
            adversary_position="MEG cost is prohibitive compared to methanol or LDHI",
            counter_arguments=[
                "MEG regeneration reduces cost to 10-20% of methanol (non-recoverable)",
                "MEG lower vapor pressure = minimal losses to gas phase",
                "Environmental profile superior to methanol (lower toxicity)",
                "Proven track record in North Sea, Gulf of Mexico high water cut fields",
                "LDHI limited to low subcooling (<10F); MEG handles any subcooling"
            ],
            resolution_strategy="Use MEG for high water cut (>20%) with regeneration; methanol for low water cut or no regeneration",
            entity_scope="Wet gas and condensate pipelines with significant water production",
            confidence=ConfidenceLevel.DEFENSIBLE,
            confidence_stratification="MEG inhibition is mature technology with decades of field validation",
            controlling_precedent="Hammerschmidt equation and MEG regeneration proven in >500 offshore installations"
        )

        self.doctrine_cache["HYDRATE_LDHI"] = DoctrineBlock(
            topic="Low Dosage Hydrate Inhibitor (LDHI) Application",
            keywords=["LDHI", "kinetic inhibitor", "KHI", "anti-agglomerant", "AA", "low dosage"],
            conclusion_template="LDHI effective for low subcooling (<10F) and short residence time (<24 hrs). Kinetic inhibitors (KHI) delay nucleation; anti-agglomerants (AA) prevent plug formation. Cost-effective alternative to thermodynamic inhibitors at 0.1-2 wt% dosage.",
            reasoning_framework="""
1. LDHI Mechanism Classification:
   - Kinetic Hydrate Inhibitors (KHI): Delay nucleation and crystal growth
     * Polymer-based (PVP, PVCap, copolymers)
     * Adsorb on hydrate crystal surface, inhibit growth
     * Typical dosage: 0.3-1.5 wt% on water phase
   - Anti-Agglomerants (AA): Allow formation but prevent blockage
     * Surfactant molecules with hydrophobic/hydrophilic groups
     * Keep hydrate particles dispersed in oil phase
     * Typical dosage: 0.5-2.0 wt% on water phase

2. Applicability Window:
   - Subcooling limit: <10F for KHI, <12F for AA
   - Residence time: <24 hours (kinetic delay window)
   - Water cut: <50% preferred; AA tolerates higher water cut
   - Gas composition: High CO2/H2S reduces KHI effectiveness
   - Flow rate: Must maintain turbulent flow for AA dispersion

3. KHI Performance Factors:
   - Polymer molecular weight and hydrophobicity
   - Synergists enhance performance (methanol, salts)
   - Temperature ramp-up after shutdown critical (reheat slowly)
   - Shut-in time >24 hrs may exceed kinetic window
   - Cloud point must be below minimum operating temperature

4. AA Performance Factors:
   - Oil continuous phase required (water cut <50% optimal)
   - Dispersed water droplet size <100 microns
   - Shear rate must maintain emulsion stability
   - Hydrate particle loading <30 vol% to avoid rheology issues
   - Separator performance may degrade with AA (stable emulsions)

5. Economic Justification:
   - LDHI cost per barrel typically 10-50% of MEG cost
   - No regeneration infrastructure required
   - Smaller injection pumps and storage
   - Environmental benefit: lower chemical volume
   - Risk: Plug formation if exceed applicability window

6. Field Trial Protocol:
   - Lab cold flow testing mandatory (rocking cell, autoclave)
   - Pilot test in section of pipeline before full deployment
   - Monitor pressure drop, temperature profile, hydrate indicators
   - Establish shut-in procedures (warm restart critical)
   - Have MEG backup system for upset conditions
            """,
            key_factors=[
                "Subcooling degree (<10F for KHI, <12F for AA)",
                "Residence time in hydrate zone (<24 hrs)",
                "Water cut (AA tolerates higher than KHI)",
                "Gas composition (CO2, H2S impact KHI)",
                "Shut-in procedures and restart protocol",
                "Lab testing validation (rocking cell)",
                "Backup inhibition strategy"
            ],
            primary_authority=[
                "SPE 65022: Kinetic Hydrate Inhibitor Field Trial in Gulf of Mexico",
                "SPE 74679: Anti-Agglomerant Hydrate Inhibitors for Deepwater Production",
                "OTC 19892: Low Dosage Hydrate Inhibitors: Progress and Challenges"
            ],
            burden_holder="Operator must prove LDHI effective within applicability window via lab/field testing",
            adversary_position="LDHI risk of failure higher than thermodynamic inhibitors; plug consequences severe",
            counter_arguments=[
                "LDHI deployed successfully in >200 offshore fields worldwide",
                "Risk mitigated by conservative applicability limits and backup systems",
                "Cold flow testing predicts field performance within 2-3F margin",
                "Cost savings justify risk when applied within proven window",
                "Monitoring (P-T, flow rate) provides early warning of inhibition failure"
            ],
            resolution_strategy="Deploy LDHI within proven applicability window + cold flow testing + real-time monitoring + MEG backup",
            entity_scope="Subsea tiebacks and wet gas pipelines with low subcooling and short residence time",
            confidence=ConfidenceLevel.AGGRESSIVE,
            confidence_stratification="LDHI requires rigorous qualification but offers significant cost savings within applicability limits",
            controlling_precedent="Industry acceptance growing; 200+ field deployments with success when properly qualified"
        )

        # Wax Deposition
        self.doctrine_cache["WAX_APPEARANCE_TEMPERATURE"] = DoctrineBlock(
            topic="Wax Appearance Temperature (WAT) and Cloud Point",
            keywords=["WAT", "wax appearance temperature", "cloud point", "paraffin", "crystallization"],
            conclusion_template="WAT defines temperature at which wax crystals first appear. Cloud point measured by ASTM D2500 or DSC. Pipeline temperature below WAT initiates wax deposition. Crude oil composition and pressure determine WAT.",
            reasoning_framework="""
1. WAT Definition and Measurement:
   - WAT = temperature at which first wax crystals appear
   - Cloud Point (ASTM D2500): Visual observation of haze in cooled sample
   - Differential Scanning Calorimetry (DSC): Detects exothermic crystallization
   - Cross-Polarized Microscopy (CPM): Direct crystal observation
   - Typical WAT range: 40-110F for waxy crudes

2. Composition Factors:
   - n-alkanes C18-C60 are primary wax components
   - Higher carbon number = higher melting point
   - API gravity inversely correlates with wax content
   - Asphaltenes and resins can modify wax crystallization
   - Gas content (dissolved light ends) depresses WAT

3. Pressure Effect on WAT:
   - Increasing pressure typically increases WAT by 0.1-0.5F per 100 psi
   - Light ends dissolve more wax at high pressure
   - Depressurization can trigger wax precipitation
   - Single-phase vs two-phase flow impacts WAT measurement

4. Temperature Profile Consequence:
   - Pipeline temperature < WAT = wax deposition zone
   - Radial temperature gradient drives wax deposition to cold pipe wall
   - Subsea pipelines: seawater temperature 35-40F = severe wax risk
   - Burial depth affects heat transfer and temperature profile

5. Wax Deposition Mechanism:
   - Molecular diffusion: wax molecules diffuse to cold wall
   - Shear dispersion: turbulence brings wax-rich fluid to wall
   - Brownian diffusion: wax crystals deposit on wall
   - Thermophoresis: temperature gradient drives particle migration
   - Deposition rate peaks 5-15F below WAT

6. Operational Implications:
   - Maintain pipeline temperature >WAT + 5F safety margin
   - Insulation, burial, or active heating required for subsea lines
   - Shut-in cool-down can deposit inches of wax in hours
   - Restart after shutdown requires wax remediation plan
   - Pigging removes deposited wax but doesn't prevent deposition
            """,
            key_factors=[
                "Crude oil wax content and carbon number distribution",
                "WAT measurement method and accuracy",
                "Pipeline temperature profile vs WAT",
                "Pressure effect on wax solubility",
                "Insulation and thermal management",
                "Shut-in and restart procedures",
                "Wax deposition rate kinetics"
            ],
            primary_authority=[
                "ASTM D2500: Cloud Point of Petroleum Products",
                "SPE 15654: Prediction of Wax Deposition in Production Systems",
                "Energy Fuels 2008: Wax Deposition Mechanisms and Models"
            ],
            burden_holder="Operator must measure WAT and design thermal management to maintain T > WAT",
            adversary_position="WAT measurements vary by method; field conditions differ from lab",
            counter_arguments=[
                "Multiple WAT methods (DSC, CPM, ASTM D2500) show agreement within 3-5F",
                "PVT sampling and lab analysis standard industry practice",
                "Field experience confirms wax deposition below measured WAT",
                "Thermal modeling (OLGA, PIPESIM) predicts temperature profile accurately",
                "Wax deposition observed in >90% of pipelines operating below WAT"
            ],
            resolution_strategy="Measure WAT by multiple methods + thermal modeling + maintain T > WAT + pigging schedule",
            entity_scope="All waxy crude pipelines, especially subsea and buried lines",
            confidence=ConfidenceLevel.DEFENSIBLE,
            confidence_stratification="WAT is measurable fluid property; deposition below WAT is well-documented phenomenon",
            controlling_precedent="Industry consensus: maintain pipeline temperature above WAT to prevent wax deposition"
        )

        self.doctrine_cache["WAX_DEPOSITION_MODELING"] = DoctrineBlock(
            topic="Wax Deposition Modeling and Prediction",
            keywords=["wax deposition", "Singh model", "deposition rate", "thickness", "modeling"],
            conclusion_template="Wax deposition rate modeled by molecular diffusion (Singh model) and shear dispersion. Deposition thickness grows until equilibrium between deposition and shear removal. OLGA and PIPESIM commercial tools incorporate wax models.",
            reasoning_framework="""
1. Singh Molecular Diffusion Model:
   - Deposition flux J = -D * dC/dr (Fick's Law)
   - D = diffusion coefficient (function of temperature, viscosity)
   - dC/dr = radial concentration gradient
   - Driving force: solubility difference between bulk and wall temperature
   - Model validated in lab flow loops and field data

2. Heat and Mass Transfer Analogy:
   - Heat transfer coefficient h relates to mass transfer coefficient k_m
   - Chilton-Colburn analogy: k_m = h / (ρ * C_p * Le^(2/3))
   - Le = Lewis number (ratio of thermal to mass diffusivity)
   - Higher Reynolds number increases both h and k_m

3. Deposition Rate Factors:
   - Temperature difference (T_bulk - T_wall): primary driver
   - Flow velocity: high velocity increases deposition initially
   - Wax concentration: higher wax content = higher deposition
   - Pipe wall roughness: rough surface increases deposition
   - Shear stress: high shear removes soft deposits

4. Equilibrium Deposit Thickness:
   - Deposition rate = removal rate at equilibrium
   - Removal mechanisms: shear stripping, aging/hardening, sloughing
   - Typical equilibrium thickness: 0.1-1.0 inch in production pipelines
   - Time to equilibrium: days to weeks depending on conditions
   - Aging hardens deposit (increasing paraffin crystallinity)

5. OLGA Wax Model Implementation:
   - Solves coupled heat/mass transfer in multiphase flow
   - Predicts wax thickness vs distance and time
   - Accounts for changing flow properties (viscosity, density)
   - Validation against field pigging data shows ±20% accuracy
   - Requires accurate PVT data (wax curve, viscosity vs T)

6. Field Data Calibration:
   - Pigging frequency and pig weight calibrate model
   - Pressure drop increase indicates wax buildup
   - Smart pig inspection (caliper, UT) measures deposit thickness
   - Adjust deposition rate constant to match field observations
   - Re-calibrate after production rate or crude quality changes
            """,
            key_factors=[
                "Temperature gradient (bulk to wall)",
                "Flow velocity and Reynolds number",
                "Wax solubility vs temperature curve",
                "Crude oil viscosity and density",
                "Pipe wall roughness and surface condition",
                "Shear stress magnitude",
                "Aging and hardening of deposits"
            ],
            primary_authority=[
                "SPE 15654: Singh et al. Wax Deposition Model (1999)",
                "SPE 107334: OLGA Wax Model Validation Against Field Data",
                "J Pet Sci Eng 2011: Wax Deposition Mechanisms Review"
            ],
            burden_holder="Operator must model wax deposition to design pigging frequency and thermal management",
            adversary_position="Models are empirical and site-specific; field variability high",
            counter_arguments=[
                "Singh model physical basis (Fick's Law) is sound",
                "Commercial software (OLGA) used industry-wide for wax prediction",
                "Field calibration improves model accuracy to ±20%",
                "Pigging data provides direct validation of model predictions",
                "Conservative assumptions (worst-case T profile) provide safety margin"
            ],
            resolution_strategy="Use validated wax model + field calibration + pigging program + pressure monitoring",
            entity_scope="Waxy crude pipelines requiring wax management strategy",
            confidence=ConfidenceLevel.DEFENSIBLE,
            confidence_stratification="Wax modeling mature technology; field-calibrated models reliable for pigging planning",
            controlling_precedent="Industry standard practice: model wax deposition using OLGA or equivalent + field calibration"
        )

        self.doctrine_cache["WAX_CHEMICAL_INHIBITION"] = DoctrineBlock(
            topic="Chemical Wax Inhibitors and Pour Point Depressants",
            keywords=["wax inhibitor", "pour point depressant", "PPD", "crystal modifier", "chemical treatment"],
            conclusion_template="Chemical wax inhibitors modify crystal structure to reduce deposition and improve flow properties. Pour point depressants (PPD) lower gelation temperature. Effectiveness varies with crude composition. Typical dosage 100-5000 ppm.",
            reasoning_framework="""
1. Wax Inhibitor Mechanisms:
   - Crystal Modifiers: Co-crystallize with wax, disrupt lattice structure
   - Pour Point Depressants (PPD): Modify crystal size/shape, reduce gel strength
   - Dispersants: Keep wax crystals suspended in oil phase
   - Paraffin Inhibitors (PI): Prevent wax adhesion to pipe wall
   - Combination products target multiple mechanisms

2. Chemical Classes:
   - Ethylene-Vinyl Acetate (EVA) copolymers: 10-40% vinyl acetate
   - Polyalkyl methacrylates: side chain matches crude wax distribution
   - Polyalphaolefins: specialty polymers for specific crudes
   - Alkyl phenol-formaldehyde resins: adhesion inhibitors
   - Dosage: 100-5000 ppm depending on chemistry and crude

3. Performance Testing:
   - Cold Finger Test (ASTM D3230): Deposition mass at target temperature
   - Pour Point (ASTM D97): Lowest temperature of fluidity
   - Gel Strength: Viscosity or yield stress at low temperature
   - Rheology Modifier Test: Viscosity vs shear rate
   - Field trial: Pigging frequency, pressure drop, deposit thickness

4. Application Strategy:
   - Inject at wellhead or platform before temperature drops
   - Ensure mixing: turbulent flow for 10+ pipe diameters
   - Maintain concentration throughout system (monitor at outlet)
   - Some chemicals require >110F injection temperature for dissolution
   - Continuous injection preferred over batch treatment

5. Crude Oil Compatibility:
   - Effectiveness varies with wax carbon number distribution
   - Screen multiple products (6-12 candidates typical)
   - Lighter crudes (>35 API) often respond better
   - Asphaltenic crudes may show poor response
   - Crude blending can change optimal chemistry/dosage

6. Economics vs Alternatives:
   - Chemical cost: $0.50-$5.00 per barrel treated
   - Compare to pigging cost, insulation cost, heating cost
   - Reduced pigging frequency is primary economic driver
   - May eliminate need for heated pipeline (CAPEX savings)
   - Synergy: chemical + pigging better than either alone
            """,
            key_factors=[
                "Chemical type and compatibility with crude wax",
                "Dosage rate (ppm) and injection point",
                "Pour point reduction achieved (lab testing)",
                "Field trial validation (pigging frequency change)",
                "Cost per barrel vs alternative wax mitigation",
                "Injection temperature and mixing",
                "Long-term effectiveness (emulsion, separator impact)"
            ],
            primary_authority=[
                "SPE 56678: Chemical Wax Inhibitors for Subsea Pipelines",
                "ASTM D3230: Apparent Viscosity of Hot Melt Adhesives",
                "OTC 8778: Pour Point Depressant Field Trial Results"
            ],
            burden_holder="Operator must test and validate chemical effectiveness for specific crude oil",
            adversary_position="Chemical inhibitors are expensive and effectiveness unpredictable",
            counter_arguments=[
                "Lab screening identifies effective chemicals before field trial",
                "Cost often justified by elimination of hot oil circulation",
                "Field trials in >500 pipelines demonstrate 30-70% pigging reduction",
                "Some subsea developments uneconomic without chemical wax control",
                "Risk mitigation: use conservative dosage based on cold finger test"
            ],
            resolution_strategy="Screen chemicals via lab testing + field trial + cost-benefit vs pigging/heating",
            entity_scope="Waxy crude pipelines where chemical treatment is cost-effective vs mechanical/thermal methods",
            confidence=ConfidenceLevel.AGGRESSIVE,
            confidence_stratification="Chemical effectiveness crude-specific; requires testing but proven in many applications",
            controlling_precedent="Industry practice: lab screening + field trial before full deployment"
        )

        # Asphaltene Precipitation
        self.doctrine_cache["ASPHALTENE_ONSET_PRESSURE"] = DoctrineBlock(
            topic="Asphaltene Onset Pressure and Precipitation Envelope",
            keywords=["asphaltene", "onset pressure", "AOP", "de Boer plot", "precipitation envelope"],
            conclusion_template="Asphaltene onset pressure (AOP) defines pressure below which asphaltenes precipitate. Measured by PVT analysis (de Boer plot, NIR, filtration). Depressurization through AOP risks deposition. Gas injection and crude blending alter AOP.",
            reasoning_framework="""
1. Asphaltene Definition and Solubility:
   - Asphaltenes = heaviest crude oil fraction, insoluble in n-alkanes (C5-C7)
   - Solubility parameter theory: asphaltenes stable when crude solubility matches
   - Pressure drop dissolves light ends, destabilizes asphaltenes
   - Onset pressure = point where asphaltene solubility parameter exceeded

2. Measurement Methods:
   - de Boer Plot: NIR absorbance vs pressure during depressurization
     * Detects asphaltene flocculation by light scattering change
     * Identifies upper and lower onset pressures
   - Acoustic Resonance: Density change from asphaltene precipitation
   - Filtration: Membrane filtration to capture precipitated asphaltenes
   - Typical AOP range: 1000-5000 psi for asphaltic crudes

3. Pressure-Temperature Precipitation Envelope:
   - Upper Onset Pressure (UOP): high pressure boundary
   - Lower Onset Pressure (LOP): low pressure boundary
   - Bubble point inside envelope = complex phase behavior
   - Some crudes show re-dissolution at very low pressure
   - Temperature effect: higher T generally decreases AOP

4. Field Implications:
   - Production through AOP = risk of wellbore/tubing deposition
   - Separator pressure below AOP = risk of vessel fouling
   - Pipeline depressurization can trigger asphaltene deposition
   - Commingling asphaltic with paraffinic crude can destabilize
   - Water production exacerbates (asphaltenes concentrate at interface)

5. Gas Injection Effect:
   - CO2 injection: dissolves in oil, precipitates asphaltenes
   - Methane injection: less severe than CO2 but still destabilizes
   - Miscible vs immiscible flood: miscible more likely to precipitate
   - Monitor AOP change in EOR projects with gas injection

6. Mitigation Strategies:
   - Maintain pressure above AOP throughout production system
   - Chemical dispersants (aromatic solvents, amphiphilic polymers)
   - Blending with lighter crudes to increase solubility parameter
   - Hot oil treatment to re-dissolve deposited asphaltenes
   - Mechanical removal (pigging, coiled tubing jetting)
            """,
            key_factors=[
                "Asphaltene content of crude (wt%)",
                "Onset pressure magnitude (UOP and LOP)",
                "Operating pressure profile vs AOP envelope",
                "Gas injection composition (CO2 vs methane)",
                "Crude blending and commingling",
                "Temperature profile effect",
                "Water cut and emulsion tendency"
            ],
            primary_authority=[
                "SPE 64991: Asphaltene Precipitation Envelope from PVT Analysis",
                "Energy Fuels 2014: de Boer Method for Asphaltene Onset Detection",
                "SPE 171005: Asphaltene Deposition Mechanisms in Production Systems"
            ],
            burden_holder="Operator must measure AOP and design pressure profile to avoid precipitation",
            adversary_position="AOP measurement expensive and results vary between methods",
            counter_arguments=[
                "PVT labs routinely measure AOP as part of fluid characterization",
                "de Boer method repeatable within ±100 psi",
                "Multiple methods (NIR, acoustic, filtration) provide validation",
                "Field observation confirms deposition when operating below AOP",
                "Cost of AOP measurement tiny compared to remediation cost"
            ],
            resolution_strategy="Measure AOP via PVT analysis + maintain pressure above AOP + chemical dispersants if needed",
            entity_scope="Heavy/asphaltic crude production systems, especially with gas injection EOR",
            confidence=ConfidenceLevel.DEFENSIBLE,
            confidence_stratification="AOP measurement is standard PVT practice; asphaltene precipitation below AOP well-documented",
            controlling_precedent="Industry consensus: operate above AOP or use chemical treatment to prevent deposition"
        )

        # Scale Formation
        self.doctrine_cache["SCALE_PREDICTION_MODELING"] = DoctrineBlock(
            topic="Scale Prediction and Saturation Index Modeling",
            keywords=["scale", "saturation index", "ScaleChem", "OLI", "calcium carbonate", "barium sulfate"],
            conclusion_template="Scale precipitation occurs when saturation index (SI) >0. ScaleChem, OLI, and PHREEQC predict SI from water chemistry. Common scales: CaCO3, BaSO4, SrSO4, CaSO4. Pressure, temperature, pH drive scale tendency.",
            reasoning_framework="""
1. Saturation Index Definition:
   - SI = log10(IAP / Ksp)
   - IAP = ion activity product in solution
   - Ksp = solubility product constant
   - SI > 0 = supersaturated, scale precipitation likely
   - SI < 0 = undersaturated, scale will not precipitate

2. Common Oilfield Scales:
   - Calcium Carbonate (CaCO3): Most common, T/pH sensitive
     * Ksp increases with T → scale on cooling or depressurization
     * CO2 degassing raises pH → drives CaCO3 precipitation
   - Barium Sulfate (BaSO4): Very low solubility, severe plugging
     * Mixing seawater (SO4) with formation water (Ba) = instant scale
     * Retrograde solubility: less soluble at high T
   - Strontium Sulfate (SrSO4): Similar to BaSO4, North Sea issue
   - Calcium Sulfate (CaSO4): Gypsum, anhydrite, hemihydrate forms

3. Water Analysis Requirements:
   - Cations: Ca, Mg, Ba, Sr, Fe, Na, K
   - Anions: HCO3, CO3, SO4, Cl, OH
   - pH, temperature, pressure, TDS
   - CO2 partial pressure (degassing drives pH change)
   - Sample collection: anaerobic, preserve pH, analyze within 24 hrs

4. Modeling Software:
   - ScaleChem (Schlumberger): oilfield-specific scale prediction
   - OLI Systems: rigorous thermodynamic model (Pitzer equations)
   - PHREEQC (USGS): geochemical modeling, free software
   - SCALE2000: industry standard for quick screening
   - Accuracy: ±0.3 SI units for well-characterized systems

5. Pressure and Temperature Effects:
   - Depressurization: CO2 degassing raises pH, precipitates CaCO3
   - Cooling: CaCO3 solubility increases (retrograde for sulfates)
   - Flash calculation: vapor-liquid equilibrium impacts ionic strength
   - Downhole to surface: P and T drop = multiple scale risks

6. Mixing and Commingling:
   - Seawater injection + formation water = sulfate scale
   - Different reservoir zones with incompatible waters = scale
   - Injection water breakthrough: monitor water chemistry change
   - Mixing ratio determines maximum SI (typically 10-40% seawater)
   - 3D reservoir simulation to predict breakthrough timing
            """,
            key_factors=[
                "Produced water chemistry (cations, anions, pH)",
                "Injection water chemistry (seawater, aquifer)",
                "Pressure and temperature profile",
                "CO2 partial pressure and degassing",
                "Water mixing ratios (formation + injection)",
                "Saturation index magnitude for each scale type",
                "Kinetics (CaCO3 fast, BaSO4 moderate, SrSO4 slow)"
            ],
            primary_authority=[
                "SPE 21021: Barium Sulfate Scale Control in North Sea",
                "NACE Corrosion 2008: Scale Prediction Software Comparison",
                "OGP Report 567: Produced Water Treatment and Disposal"
            ],
            burden_holder="Operator must analyze water chemistry and predict scale tendency before commingling",
            adversary_position="Scale models are theoretical; field conditions show unexpected scaling",
            counter_arguments=[
                "ScaleChem and OLI models validated against >1000 field samples",
                "Scale formation correlates with SI > 0 in 95%+ of cases",
                "Unexpected scaling usually due to incomplete water analysis",
                "Kinetic inhibitors effective when SI < +2.0 (model guides dosage)",
                "Scale prediction standard in waterfloods to design injection strategy"
            ],
            resolution_strategy="Comprehensive water analysis + scale modeling + inhibitor treatment when SI > 0",
            entity_scope="All produced water systems, especially waterfloods and seawater injection",
            confidence=ConfidenceLevel.DEFENSIBLE,
            confidence_stratification="Scale thermodynamics well-understood; models reliable when water analysis complete",
            controlling_precedent="Industry practice: predict scale with software (ScaleChem/OLI) before designing treatment"
        )

        self.doctrine_cache["SCALE_INHIBITOR_SQUEEZE"] = DoctrineBlock(
            topic="Scale Inhibitor Squeeze Treatment Design",
            keywords=["scale inhibitor", "squeeze", "phosphonate", "polymer", "retention", "return curve"],
            conclusion_template="Squeeze treatment injects scale inhibitor into formation, adsorbs on rock, slowly desorbs to protect production. Phosphonates and polymers common. Design requires lab testing (adsorption isotherm, return curve). Squeeze life: weeks to years.",
            reasoning_framework="""
1. Squeeze Mechanism:
   - Injection: Pump inhibitor slug (5-50 bbl) into near-wellbore formation
   - Shut-in: Allow adsorption onto rock surface (4-24 hrs)
   - Production: Inhibitor desorbs, maintains protective concentration
   - Target: 5-20 ppm inhibitor in produced water (above MIC)
   - Squeeze life = time until inhibitor falls below MIC

2. Scale Inhibitor Chemistry:
   - Phosphonates (DTPMP, HEDP, ATMP): Most common, broad spectrum
     * Chelate metal ions (Ca, Ba, Sr)
     * Threshold effect: sub-stoichiometric dosage effective
     * Stable to 200-250F
   - Polymers (polyacrylates, phosphino-polymers): High T applications
     * Thermal stability to 300F+
     * Crystal distortion mechanism
     * Higher cost than phosphonates
   - Dosage: 1000-5000 ppm in squeeze slug, 5-20 ppm in produced water

3. Lab Core Flood Testing:
   - Adsorption Isotherm: Inhibitor retention vs concentration
   - Dynamic Return Curve: Inhibitor concentration vs pore volumes produced
   - Compatibility: Inhibitor + formation water + injection water
   - Precipitation Test: High concentration (10,000 ppm) stability
   - Temperature Stability: Thermal degradation at reservoir T

4. Squeeze Design Parameters:
   - Inhibitor volume: 5-50 bbl (depends on well productivity, squeeze life)
   - Preflush: 10-100 bbl seawater or brine to displace oil
   - Overflush: 10-50 bbl to push inhibitor into formation
   - Shut-in time: 4-24 hrs (longer = better adsorption)
   - Maximum injection rate: avoid fracturing formation

5. Squeeze Life Prediction:
   - Adsorption/Desorption Model: Uses lab isotherm + flow rate
   - Typical squeeze life: 3-12 months (sandstone), 1-3 months (carbonate)
   - Carbonates have lower retention (less adsorption sites)
   - High water cut wells need more frequent squeezes
   - Return curve monitoring validates model, adjusts future squeezes

6. Continuous Injection Alternative:
   - Subsea wells: continuous injection via umbilical
   - Platform wells: continuous dosing at wellhead or separator
   - Dosage: 5-30 ppm in produced water
   - Economics: continuous vs squeeze depends on well count and accessibility
   - Offshore platform: continuous often preferred (no rig for squeeze)
            """,
            key_factors=[
                "Inhibitor chemistry (phosphonate vs polymer)",
                "Lab core flood adsorption isotherm",
                "Squeeze volume and concentration",
                "Formation type (sandstone vs carbonate)",
                "Reservoir temperature (thermal stability)",
                "Produced water rate (desorption rate)",
                "Target squeeze life (3-12 months typical)"
            ],
            primary_authority=[
                "SPE 27389: Scale Inhibitor Squeeze Design and Field Results",
                "SPE 164116: Phosphonate Scale Inhibitors for HP/HT Wells",
                "NACE 09563: Scale Inhibitor Selection and Testing Protocol"
            ],
            burden_holder="Operator must conduct lab testing and design squeeze to achieve target life",
            adversary_position="Squeeze life unpredictable; field results deviate from lab",
            counter_arguments=[
                "Return curve modeling from lab data predicts field life within ±30%",
                ">10,000 squeeze treatments performed annually in oil/gas industry",
                "Field monitoring validates squeeze performance and refines design",
                "Conservative design (higher volume, concentration) provides safety margin",
                "Continuous injection option if squeeze life inadequate"
            ],
            resolution_strategy="Lab core flood + squeeze design modeling + field monitoring + adjust future treatments",
            entity_scope="All wells with scale risk (especially waterfloods and seawater injection)",
            confidence=ConfidenceLevel.DEFENSIBLE,
            confidence_stratification="Squeeze treatment is mature technology; lab-to-field correlation well-established",
            controlling_precedent="Industry standard: squeeze treatment for downhole scale prevention, validated by decades of use"
        )

        # Terrain Slugging
        self.doctrine_cache["TERRAIN_SLUGGING_MECHANISM"] = DoctrineBlock(
            topic="Terrain-Induced Slugging in Hilly Pipelines",
            keywords=["terrain slugging", "pipeline profile", "riser", "slug length", "separator upset"],
            conclusion_template="Terrain slugging occurs in hilly multiphase pipelines when liquid accumulates in low points and is periodically pushed out by gas. Slug length can be hundreds of barrels. Causes separator upsets and platform vibration. Mitigation: choking, gas lift, slug catchers.",
            reasoning_framework="""
1. Terrain Slugging Mechanism:
   - Pipeline profile has multiple low points (valleys)
   - Liquid accumulates in valleys, blocks gas flow
   - Gas pressure builds upstream until overcomes liquid blockage
   - Large liquid slug (10-500 bbl) pushes rapidly through pipeline
   - Cycle repeats every few minutes to hours
   - Severe in subsea tiebacks with 1000+ ft elevation changes

2. Slug Characteristics:
   - Slug length: 100-5000 ft (depends on valley length and holdup)
   - Slug frequency: 2-60 minutes (depends on gas/liquid rates)
   - Slug velocity: 15-50 ft/s (much higher than average flow velocity)
   - Liquid surge: 2-10X normal liquid rate for 30-120 seconds
   - Gas blowdown after slug: high gas rate, low liquid rate

3. Conditions Favoring Terrain Slugging:
   - Low gas velocity: <10 ft/s in horizontal sections
   - High liquid holdup in valleys (>50% pipe volume)
   - Long valleys: >500 ft between high points
   - Riser at pipeline outlet (creates backpressure)
   - Shutdown/restart (liquid accumulation during shut-in)

4. Impact on Facilities:
   - Separator liquid surge exceeds design capacity (overflow or shutdown)
   - Gas blowdown can blow liquid carryover to gas compression
   - Platform deck vibration from slug impact at riser base
   - Flare system overload during gas blowdown phase
   - Pressure transients risk equipment overpressure

5. Prediction Methods:
   - OLGA dynamic simulation: predicts slug frequency, length, velocity
   - Simplified criteria: Froude number, Taitel stability criterion
   - Field data: pressure/flow measurements show slug signature
   - Smart pig inspection: identifies liquid holdup locations
   - Subsea pressure/temperature sensors confirm slugging

6. Mitigation Strategies:
   - Topside choking: increase backpressure, stabilize flow (reduces throughput)
   - Gas lift at low points: inject gas to reduce liquid holdup
   - Slug catcher: large vessel (500-5000 bbl) absorbs liquid surges
   - Self-lifting riser (alternative configuration reduces slugging)
   - Active control: automated choke adjustment based on flow measurements
            """,
            key_factors=[
                "Pipeline elevation profile (valley depth and length)",
                "Gas and liquid flow rates (superficial velocities)",
                "Riser height and backpressure",
                "Separator liquid handling capacity",
                "Slug frequency and severity (OLGA prediction)",
                "Liquid holdup in low points",
                "Restart procedure after shutdown"
            ],
            primary_authority=[
                "SPE 56461: Terrain Slugging in Subsea Pipelines",
                "J Pet Sci Eng 2012: Terrain Slugging Characteristics and Mitigation",
                "Multiphase Sci Tech 2005: OLGA Terrain Slugging Validation"
            ],
            burden_holder="Operator must predict slugging severity and design mitigation (slug catcher, gas lift, choke)",
            adversary_position="OLGA simulation uncertain; field slugging worse than predicted",
            counter_arguments=[
                "OLGA model validated in >200 subsea pipelines worldwide",
                "Slug frequency and length predicted within ±30% of field data",
                "Conservative design (oversized slug catcher) provides safety margin",
                "Subsea instrumentation confirms slugging behavior matches simulation",
                "Alternative: install slug suppression before production startup"
            ],
            resolution_strategy="OLGA simulation + slug catcher design + instrumentation + operational procedures",
            entity_scope="Subsea tiebacks and hilly terrain multiphase pipelines",
            confidence=ConfidenceLevel.DEFENSIBLE,
            confidence_stratification="Terrain slugging well-understood phenomenon; OLGA predictions validated by field data",
            controlling_precedent="Industry practice: OLGA simulation mandatory for subsea pipeline design with hilly profile"
        )

        # Multiphase Flow
        self.doctrine_cache["MULTIPHASE_FLOW_CORRELATIONS"] = DoctrineBlock(
            topic="Multiphase Flow Correlations and Pressure Drop Prediction",
            keywords=["multiphase flow", "pressure drop", "Beggs-Brill", "holdup", "flow pattern"],
            conclusion_template="Multiphase pressure drop predicted by empirical correlations (Beggs-Brill, Duns-Ros) or mechanistic models (OLGA). Flow pattern (stratified, slug, annular) determines pressure gradient. Liquid holdup increases pressure drop vs single-phase gas.",
            reasoning_framework="""
1. Flow Pattern Regimes:
   - Stratified: Low velocities, liquid flows along bottom, gas on top
   - Slug: Intermittent liquid slugs separated by gas pockets (common)
   - Annular: High gas velocity, liquid film on wall, gas core in center
   - Bubble: Low gas fraction, bubbles dispersed in continuous liquid
   - Flow pattern map: uses superficial gas/liquid velocities

2. Beggs-Brill Correlation (1973):
   - Empirical correlation for multiphase pressure drop
   - Horizontal and inclined flow patterns
   - Calculates liquid holdup H_L based on Fr number and flow pattern
   - Pressure gradient: dP/dL = (ρ_L * H_L + ρ_G * (1-H_L)) * g * sin(θ) + friction
   - Widely used in industry, implemented in PIPESIM, PROSPER

3. Mechanistic Models:
   - OLGA: Solves transient two-fluid conservation equations
   - Predicts flow pattern transitions, pressure, holdup vs distance/time
   - Accounts for terrain profile, pipe diameter changes, heat transfer
   - More accurate than correlations but requires detailed input data
   - Industry standard for subsea multiphase pipeline design

4. Liquid Holdup Effect:
   - Holdup H_L = fraction of pipe volume occupied by liquid
   - H_L > liquid input fraction = liquid accumulation (slip)
   - High holdup increases hydrostatic head and pressure drop
   - Uphill sections: H_L increases (gravity slows liquid)
   - Downhill sections: H_L decreases (liquid accelerates)

5. Pressure Drop Components:
   - Frictional: Wall shear stress from flow velocity
   - Gravitational: ρ * g * Δz (elevation change)
   - Acceleration: Change in kinetic energy (usually small)
   - Total dP/dL = dP/dL_friction + dP/dL_gravity + dP/dL_acceleration
   - Inclined flow: sin(θ) term dominates for low Fr number

6. Field Application:
   - Measure wellhead P, T, and flowline outlet P, T
   - Calculate pressure drop and compare to correlation/model
   - Tune friction factor and holdup to match field data
   - Recalibrate after production rate or GOR changes
   - Erosional velocity: V_e = C / sqrt(ρ_mix), C = 100-150 for continuous service
            """,
            key_factors=[
                "Gas and liquid superficial velocities",
                "Pipeline diameter and roughness",
                "Elevation profile (uphill/downhill)",
                "Fluid properties (density, viscosity, surface tension)",
                "Flow pattern regime",
                "Liquid holdup fraction",
                "Temperature profile (impacts fluid properties)"
            ],
            primary_authority=[
                "Beggs & Brill, J Pet Tech 1973: Multiphase Flow in Pipes",
                "OLGA User Manual: Mechanistic Multiphase Flow Model",
                "API RP 14E: Pipeline Design for Multiphase Flow"
            ],
            burden_holder="Operator must predict multiphase pressure drop for pipeline design and operations",
            adversary_position="Correlations are empirical; accuracy poor for field conditions outside database",
            counter_arguments=[
                "Beggs-Brill validated against 1000+ lab/field data points",
                "OLGA mechanistic model based on conservation laws, not purely empirical",
                "Field tuning improves correlation accuracy to ±10% pressure drop",
                "Subsea pipelines routinely designed using multiphase models (OLGA)",
                "Alternative: conservative design (larger diameter) if prediction uncertainty high"
            ],
            resolution_strategy="Use validated correlation/model + field calibration + erosional velocity check",
            entity_scope="All multiphase production pipelines (oil/gas/water)",
            confidence=ConfidenceLevel.DEFENSIBLE,
            confidence_stratification="Multiphase flow prediction is mature technology; models validated by extensive field use",
            controlling_precedent="Industry consensus: Beggs-Brill or OLGA for multiphase pressure drop, field-tuned for accuracy"
        )

        # Pigging Operations
        self.doctrine_cache["INTELLIGENT_PIGGING"] = DoctrineBlock(
            topic="Intelligent Pigging for Pipeline Inspection",
            keywords=["intelligent pig", "ILI", "MFL", "UT", "caliper", "corrosion", "crack detection"],
            conclusion_framework="""Smart pigs (ILI tools) inspect pipeline integrity without shutdown. MFL detects metal loss (corrosion). UT measures wall thickness. Caliper detects dents and ovality. Crack detection uses EMAT or CMFL. Data analysis identifies defects requiring repair.""",
            reasoning_framework="""
1. Intelligent Pig Tool Types:
   - Magnetic Flux Leakage (MFL): Detects metal loss (corrosion, erosion)
     * Magnetizes pipe wall, sensors measure flux leakage at defects
     * Accuracy: ±10% wall thickness, 80% POD for >20% wall loss
   - Ultrasonic (UT): Measures remaining wall thickness directly
     * Accuracy: ±0.5 mm (0.020 inch), better than MFL for small defects
   - Caliper: Measures internal diameter changes (dents, ovality)
     * Mechanical arms or EM sensors detect geometry changes
   - Crack Detection: EMAT (electromagnetic acoustic) or CMFL
     * Detects stress corrosion cracking, fatigue cracks

2. Pipeline Preparation:
   - Cleaning pig run first to remove deposits (wax, scale, debris)
   - Verify pig launchers/receivers operational, traps sized for ILI tool
   - Remove inline restrictions (valves <80% ID = pig trap risk)
   - Fill low spots with liquid (gas-filled ILI tools travel erratically)
   - Minimum flow velocity: 2-3 ft/s for consistent pig speed

3. Data Collection and Analysis:
   - ILI tool records data at 1-10 mm axial resolution
   - GPS and odometer track tool position vs distance
   - Data downloaded at receiver, analyzed by vendor software
   - Feature classification: metal loss, dents, cracks, geometry
   - Severity grading: B31G, DNV, or API 579 fitness-for-service

4. Defect Assessment:
   - RSTRENG (B31G): Calculates remaining strength for corrosion defects
   - Depth >80% wall = immediate repair/replacement
   - Depth 20-80% = monitor, re-inspect in 1-5 years
   - Crack features = hydrostatic retest or repair (high risk)
   - Dents >6% OD = assess for fatigue risk

5. Frequency Determination:
   - Corrosion rate: Initial ILI + follow-up ILI at 3-5 years
   - High corrosion rate (>5 mpy) = annual ILI
   - Low corrosion rate (<1 mpy) = 5-10 year ILI interval
   - Regulatory requirements: DOT, PHMSA mandates for onshore
   - Offshore: API RP 1160 recommended practices

6. Limitations and Alternatives:
   - Unpiggable pipelines: tight bends, small diameter, no launcher/receiver
   - Alternative: Direct Assessment (DA) using ECDA, ICDA methods
   - Alternative: Hydrostatic testing to 1.25-1.5X MAOP
   - Cost: $50-200K per ILI run depending on diameter and length
   - Risk: Pig stuck in line (requires excavation/cutting)
            """,
            key_factors=[
                "ILI tool type (MFL, UT, caliper, crack) and capabilities",
                "Pipeline piggability (bends, diameter, launcher/receiver)",
                "Defect types expected (corrosion, cracks, dents)",
                "ILI frequency based on corrosion rate",
                "Fitness-for-service assessment (B31G, DNV)",
                "Regulatory requirements (DOT, PHMSA, API)",
                "Cost vs risk of undetected defects"
            ],
            primary_authority=[
                "API 1163: Inline Inspection Systems Qualification",
                "ASME B31.8S: Managing System Integrity of Gas Pipelines",
                "NACE SP0102: Inline Inspection of Pipelines"
            ],
            burden_holder="Operator must conduct ILI at intervals sufficient to detect defects before failure",
            adversary_position="ILI tools have POD <100%; defects missed leading to failures",
            counter_arguments=[
                "MFL/UT POD >95% for defects >30% wall thickness",
                "Repeat ILI runs improve detection via comparison",
                "Unity sizing (MFL + UT) improves accuracy vs single tool",
                "Field validation: excavation of called features confirms sizing accuracy",
                "Regulatory acceptance: ILI standard for HCA pipeline integrity"
            ],
            resolution_strategy="ILI per API 1163 + fitness-for-service + excavation validation + re-inspection interval based on corrosion rate",
            entity_scope="All pipelines in high consequence areas (HCA) and aging pipelines",
            confidence=ConfidenceLevel.DEFENSIBLE,
            confidence_stratification="ILI technology mature and validated; industry standard for pipeline integrity management",
            controlling_precedent="DOT/PHMSA regulations mandate ILI for gas transmission pipelines in HCAs"
        )

        self.doctrine_cache["PIGGING_FREQUENCY_WAX"] = DoctrineBlock(
            topic="Pigging Frequency Optimization for Wax Removal",
            keywords=["pigging", "pig", "wax removal", "scraper", "frequency", "pressure drop"],
            conclusion_template="Pigging frequency determined by wax deposition rate and acceptable pressure drop increase. Monitor pressure drop trend to optimize schedule. Typical frequency: weekly to quarterly. Pig weight validates wax model predictions.",
            reasoning_framework="""
1. Pressure Drop Monitoring:
   - Baseline pressure drop after pigging = clean pipe condition
   - ΔP increases over time as wax deposits reduce effective diameter
   - Trigger pigging when ΔP increases 10-20% above baseline
   - Smart pressure sensors at inlet/outlet track ΔP continuously
   - Trend analysis predicts when trigger threshold will be reached

2. Wax Buildup Rate:
   - Deposition rate (inch/day) from wax model (OLGA) or field data
   - Temperature profile determines deposition zone length
   - Higher deposition rate = more frequent pigging required
   - Seasonal variation: winter deposition higher (colder seawater)
   - Production rate change alters wax deposition (velocity effect)

3. Pig Type Selection:
   - Scraper pig: Wire brush or carbide blades for hard wax
   - Foam pig: Light cleaning, used between scraper runs
   - Gauge plate pig: Detects restrictions, run before scraper
   - Multi-diameter pig: Effective in variable ID pipelines
   - Bi-directional pig: Can be launched from either end

4. Pigging Procedure:
   - Preflush: Increase flow rate to 1.5X normal (turbulence helps)
   - Launch pig: Ensure pig launcher equalized before opening
   - Track pig: Acoustic/magnetic sensors confirm pig passage
   - Receive pig: Confirm arrival time (travel time = L / velocity)
   - Measure wax: Weigh pig before/after or measure receiver volume

5. Frequency Optimization:
   - Initial frequency: Conservative (weekly) until trend established
   - Adjust based on ΔP trend and pig weight data
   - Target: Pig before wax hardens (easier removal, lower risk)
   - Aged wax (>30 days) hardens, may require chemical/heat treatment
   - Economic optimization: pigging cost vs production loss from ΔP

6. Risk of Deferred Pigging:
   - Hard wax difficult to remove, pig may stick
   - Severe restriction: pig moves slowly or stops
   - Plugged pipeline: requires coiled tubing, hot oil, or chemical treatment
   - Stuck pig: excavation/cutting may be required (subsea = very expensive)
   - Rule: Pig before wax thickness >10% pipe radius (e.g., 1 inch in 10 inch ID)
            """,
            key_factors=[
                "Wax deposition rate (inch/day or inch/month)",
                "Acceptable pressure drop increase threshold",
                "Pipeline diameter and length",
                "Wax hardness and age",
                "Pig type and cleaning effectiveness",
                "Seasonal temperature variation",
                "Cost of pigging vs production loss"
            ],
            primary_authority=[
                "SPE 77573: Pigging Practice for Wax Control in Subsea Pipelines",
                "Pipeline Pigging and Integrity Technology, 4th Ed (2012)",
                "API RP 5L3: Recommended Practice for Conducting Drop-Weight Tear Tests"
            ],
            burden_holder="Operator must establish pigging frequency to prevent wax plugs and maintain capacity",
            adversary_position="Pigging frequency arbitrary; field conditions unpredictable",
            counter_arguments=[
                "Pressure drop monitoring provides objective trigger for pigging",
                "Pig weight data validates wax deposition rate assumptions",
                "Field experience establishes reliable frequency for each pipeline",
                "Conservative approach (frequent pigging) low cost vs plug remediation",
                "SCADA system automates ΔP trending and pigging alerts"
            ],
            resolution_strategy="Monitor ΔP + establish frequency based on wax model/field data + adjust based on pig weight",
            entity_scope="All waxy crude pipelines requiring regular wax removal",
            confidence=ConfidenceLevel.DEFENSIBLE,
            confidence_stratification="Pigging is standard practice; frequency optimization based on field data is reliable",
            controlling_precedent="Industry consensus: regular pigging prevents wax plugs; optimize frequency via monitoring"
        )

        # Additional Doctrines (25+ total)
        self.doctrine_cache["HYDRATE_EMERGENCY_DEPRESSURIZATION"] = DoctrineBlock(
            topic="Emergency Depressurization and Hydrate Dissociation Risk",
            keywords=["emergency depressurization", "EDP", "blowdown", "hydrate", "Joule-Thomson cooling"],
            conclusion_template="Emergency depressurization through hydrate stability zone creates severe plug risk. Joule-Thomson cooling lowers temperature further into hydrate zone. Controlled depressurization (<100 psi/hr) or heating required. EDP system design must account for hydrate formation.",
            reasoning_framework="""
1. Joule-Thomson Cooling Effect:
   - Gas expansion through valve/orifice causes temperature drop
   - JT coefficient μ_JT = (dT/dP)_H, typically 3-7F per 100 psi for natural gas
   - Rapid depressurization (500-1000 psi/hr) = 15-70F cooling
   - Cooling crosses hydrate curve even if initial T > T_hydrate
   - Hydrate formation during blowdown can plug vent/relief system

2. Hydrate Formation Kinetics During Depressurization:
   - Subcooling increases during blowdown (moving deeper into hydrate zone)
   - Nucleation time inversely proportional to subcooling
   - Turbulence from high velocity accelerates nucleation
   - Water dropout from gas phase increases hydrate risk
   - Plug can form in minutes under high subcooling

3. Controlled Depressurization Strategy:
   - Maximum rate: 50-100 psi/hr to limit JT cooling
   - Monitor temperature continuously during blowdown
   - Inject methanol or MEG during depressurization
   - Active heating (hot oil circulation, electric tracing) if available
   - Stop depressurization if T approaches T_hydrate - 5F

4. EDP System Design Considerations:
   - Size relief valve for required depressurization rate
   - Insulation on blowdown lines to reduce heat loss
   - Methanol injection point upstream of choke
   - Temperature monitoring at multiple points
   - Alternate flowpath if primary route plugs with hydrate

5. Field Experience and Incidents:
   - Multiple subsea blowdown failures due to hydrate plugs
   - Hydrate formation in relief valve prevented full depressurization
   - Blocked vent line caused overpressure of downstream equipment
   - Lesson: Controlled depressurization preferred over rapid EDP
   - Regulators increasingly require hydrate analysis for EDP systems

6. Mitigation Options:
   - Pre-charge system with methanol before shutdown
   - Install electric or hot water heat tracing on blowdown lines
   - Two-stage depressurization: high-pressure to mid-pressure (with heating), then mid to atmospheric
   - Nitrogen purge to displace hydrocarbon gas before depressurization
   - Subsea intervention capability (ROV hot water jetting) for plug remediation
            """,
            key_factors=[
                "Depressurization rate (psi/hr)",
                "Joule-Thomson cooling magnitude",
                "Hydrate formation temperature at depressurizing P",
                "Subcooling created during blowdown",
                "Chemical injection capability during EDP",
                "Insulation and heating of blowdown system",
                "Alternate flowpaths if plug occurs"
            ],
            primary_authority=[
                "SPE 96418: Hydrate Formation During Subsea Blowdown",
                "API RP 521: Pressure-Relieving and Depressuring Systems",
                "HSE Offshore Information Sheet 3/2006: Hydrate Blockages"
            ],
            burden_holder="Operator must design EDP system to prevent hydrate plug formation during blowdown",
            adversary_position="EDP must be rapid for safety; can't wait for slow controlled depressurization",
            counter_arguments=[
                "Hydrate plug in relief system creates greater safety risk than slower depressurization",
                "Methanol injection during EDP proven effective in many installations",
                "Two-stage depressurization balances safety and hydrate risk",
                "Field incidents show rapid EDP through hydrate zone causes plugs",
                "API RP 521 recommends hydrate analysis for depressurizing systems"
            ],
            resolution_strategy="Design EDP for controlled rate + methanol injection + monitoring + alternate flowpaths",
            entity_scope="All subsea and cold climate facilities with hydrate-forming fluids",
            confidence=ConfidenceLevel.DEFENSIBLE,
            confidence_stratification="JT cooling and hydrate formation during depressurization are well-documented phenomena",
            controlling_precedent="Industry moving toward controlled depressurization with chemical injection to prevent hydrate plugs"
        )

        self.doctrine_cache["CORROSION_CO2_SWEET"] = DoctrineBlock(
            topic="Sweet Corrosion from CO2 in Production Systems",
            keywords=["CO2 corrosion", "sweet corrosion", "carbonic acid", "corrosion rate", "de Waard model"],
            conclusion_template="CO2 dissolves in water to form carbonic acid, causing sweet corrosion. Corrosion rate depends on CO2 partial pressure, temperature, pH, flow velocity. de Waard model predicts rate. Mitigation: corrosion inhibitor, pH stabilization, corrosion-resistant alloys.",
            reasoning_framework="""
1. Sweet Corrosion Mechanism:
   - CO2 dissolves in water: CO2 + H2O ⇌ H2CO3 (carbonic acid)
   - Carbonic acid dissociates: H2CO3 ⇌ H+ + HCO3- ⇌ 2H+ + CO3(2-)
   - Hydrogen ions attack steel: Fe + 2H+ → Fe(2+) + H2
   - Iron carbonate scale: Fe(2+) + CO3(2-) → FeCO3 (protective if conditions right)
   - Non-protective scale: high velocity, low pH, temperature swings

2. de Waard Corrosion Rate Model:
   - log(CR) = A - B / T + C * log(P_CO2) + D * pH
   - CR = corrosion rate (mm/year)
   - T = temperature (Kelvin)
   - P_CO2 = CO2 partial pressure (bar)
   - pH of produced water
   - Model validated for 5% CO2 to 100% CO2, 40-300F

3. Key Variables Affecting Corrosion Rate:
   - CO2 Partial Pressure: P_CO2 = y_CO2 * P_total
     * >30 psi CO2: High corrosion risk (>10 mpy)
     * 7-30 psi: Moderate risk (1-10 mpy)
     * <7 psi: Low risk (<1 mpy)
   - Temperature: Peak corrosion at 140-180F (FeCO3 scale non-protective)
   - pH: Lower pH = higher corrosion (pH 4-5 typical for CO2 systems)
   - Flow Velocity: >10 ft/s erodes protective scale

4. FeCO3 Scale Formation:
   - Protective scale forms at T >140F, low velocity, high Fe(2+) supersaturation
   - Scale reduces corrosion rate by 10-100X when intact
   - Scale breakdown: mechanical damage, temperature cycling, chemical upset
   - Scaling tendency: Calculate FeCO3 saturation index
   - Non-scaling conditions require continuous corrosion inhibitor

5. Corrosion Inhibitor Treatment:
   - Filming inhibitors: Adsorb on steel, block corrosive species
   - Typical chemistry: Imidazolines, quaternary ammonium, phosphate esters
   - Dosage: 10-100 ppm continuous injection
   - Injection point: Upstream of corrosion zone (wellhead, separator inlet)
   - Effectiveness: >95% corrosion reduction when properly applied

6. Material Selection:
   - Carbon steel: Acceptable if CR <5 mpy with inhibitor treatment
   - 13Cr stainless: Good resistance to CO2, used for P_CO2 >30 psi
   - Duplex/super duplex: High strength + corrosion resistance
   - CRA clad pipe: Carbon steel + CRA inner layer (cost optimization)
   - Fiber reinforced pipe (FRP): Non-metallic, immune to CO2 corrosion
            """,
            key_factors=[
                "CO2 partial pressure (psi)",
                "Temperature (peak corrosion 140-180F)",
                "pH of produced water",
                "Flow velocity (>10 ft/s erodes scale)",
                "FeCO3 scale formation tendency",
                "Corrosion inhibitor effectiveness",
                "Material selection (carbon steel vs CRA)"
            ],
            primary_authority=[
                "NACE 1D182: de Waard CO2 Corrosion Model (1995)",
                "ISO 15156: Materials for H2S-Containing Environments (includes CO2)",
                "NACE SP0206: Internal Corrosion Direct Assessment"
            ],
            burden_holder="Operator must predict CO2 corrosion rate and design mitigation (inhibitor, materials, monitoring)",
            adversary_position="de Waard model is empirical; field corrosion rates vary widely",
            counter_arguments=[
                "de Waard model validated against 1000+ field/lab data points",
                "NORSOK M-506 uses de Waard as basis for material selection",
                "Corrosion monitoring (coupons, ER probes) validates model predictions",
                "Conservative design (CRA materials) where model uncertainty high",
                "Inhibitor treatment proven effective when properly applied"
            ],
            resolution_strategy="Predict CR with de Waard model + corrosion inhibitor program + monitoring (coupons, probes) + material upgrade if needed",
            entity_scope="All production systems with CO2 content >0.5 mol%",
            confidence=ConfidenceLevel.DEFENSIBLE,
            confidence_stratification="CO2 corrosion mechanisms well-understood; models and mitigation proven by extensive field experience",
            controlling_precedent="Industry standard: de Waard model + NORSOK M-506 for CO2 corrosion assessment and material selection"
        )

        self.doctrine_cache["EROSIONAL_VELOCITY_API14E"] = DoctrineBlock(
            topic="Erosional Velocity and API RP 14E Criterion",
            keywords=["erosional velocity", "API RP 14E", "C factor", "sand production", "velocity limit"],
            conclusion_template="Erosional velocity V_e = C / sqrt(rho_mix) limits pipeline velocity to prevent erosion. API RP 14E: C=100 for continuous service, C=125-150 for intermittent. Sand production lowers allowable C factor. Exceed V_e = risk of erosion failure.",
            reasoning_framework="""
1. API RP 14E Erosional Velocity Equation:
   - V_e = C / sqrt(ρ_mix)
   - V_e = erosional velocity (ft/s)
   - C = empirical constant (typically 100-150)
   - ρ_mix = mixture density (lb/ft3)
   - Lower density (gas) = higher V_e; higher density (liquid) = lower V_e

2. C Factor Selection:
   - C = 100: Continuous service (24/7 production)
   - C = 125: Intermittent service (well testing, occasional high rate)
   - C = 150: Short-term service (well cleanup, temporary operation)
   - Sand-free production: C up to 150 acceptable
   - Sand production: Reduce C to 75-100 depending on sand rate

3. Sand Production Impact:
   - Sand particles (quartz, feldspar) are highly erosive
   - Erosion rate proportional to sand rate^2.5 (highly nonlinear)
   - 0.1% sand by volume can reduce pipe life from decades to months
   - Elbows, tees, chokes erode 5-10X faster than straight pipe
   - Erosion pattern: Horseshoe-shaped grooves opposite flow direction

4. Velocity Calculation for Multiphase Flow:
   - Mixture velocity V_mix = (Q_gas + Q_liquid) / A_pipe
   - Mixture density ρ_mix = (ρ_gas * HG + ρ_liquid * HL)
   - HG, HL = gas/liquid holdup fractions
   - Check V_mix < V_e for safe operation
   - High GOR wells: gas dominates, velocity typically exceeds V_e

5. Erosion Monitoring and Inspection:
   - Ultrasonic thickness (UT) monitoring at elbows and restrictions
   - Baseline thickness after installation
   - Periodic UT surveys (annual to 5-year depending on risk)
   - Erosion rate (mpy) = (t_initial - t_current) / time_years
   - Replace when remaining thickness < MAWP + corrosion allowance

6. Design Mitigation:
   - Increase pipe diameter to reduce velocity (V ∝ 1/D^2)
   - Use erosion-resistant materials (tungsten carbide, ceramic linings)
   - Install erosion probes (replaceable wear elements) at high-risk points
   - Design flowlines for C=100 even if initial rate allows C=150
   - Long radius elbows (5D bend radius) reduce erosion vs short radius (1.5D)
            """,
            key_factors=[
                "Mixture velocity (ft/s)",
                "Mixture density (lb/ft3)",
                "C factor based on service (continuous vs intermittent)",
                "Sand production rate (lb/1000 bbl)",
                "Pipe geometry (elbows, tees, restrictions)",
                "Material erosion resistance",
                "Inspection frequency and remaining thickness"
            ],
            primary_authority=[
                "API RP 14E: Design and Installation of Offshore Production Platform Piping Systems",
                "NACE SP0110: Wet Gas Internal Corrosion Direct Assessment",
                "DNV-RP-O501: Erosive Wear in Piping Systems"
            ],
            burden_holder="Operator must design for velocity < V_e and monitor erosion in high-risk areas",
            adversary_position="API 14E is conservative; many pipelines operate above V_e without erosion",
            counter_arguments=[
                "API 14E based on >50 years industry experience and failure data",
                "Exceeding V_e documented cause of erosion failures (loss of containment)",
                "Sand production dramatically accelerates erosion (C factor must be reduced)",
                "UT monitoring confirms erosion in areas where V > V_e",
                "Conservative design (C=100) provides safety margin for uncertainties"
            ],
            resolution_strategy="Design for V < V_e (C=100 for continuous) + UT monitoring + reduce C if sand production",
            entity_scope="All production flowlines and pipelines, especially high-velocity gas and sand-producing wells",
            confidence=ConfidenceLevel.DEFENSIBLE,
            confidence_stratification="API RP 14E is industry consensus standard; erosional velocity criterion validated by field data",
            controlling_precedent="API RP 14E mandatory reference for offshore facility design; regulators enforce erosional velocity limits"
        )

        logger.info(f"Initialized {len(self.doctrine_cache)} doctrine blocks for pipeline flow assurance")

    # ============================================================================
    # SEMANTIC NORMALIZATION
    # ============================================================================

    def _normalize_query(self, query: str) -> str:
        """Normalize query terms for consistent doctrine matching"""
        normalizations = {
            # Hydrate terms
            "gas hydrate": "hydrate",
            "hydrates": "hydrate",
            "clathrate": "hydrate",
            "hydrate plug": "hydrate formation",
            "hydrate blockage": "hydrate formation",

            # Inhibitor terms
            "glycol": "MEG",
            "monoethylene glycol": "MEG",
            "ethylene glycol": "MEG",
            "methanol": "MeOH",
            "kinetic inhibitor": "LDHI KHI",
            "anti-agglomerant": "LDHI AA",

            # Wax terms
            "paraffin": "wax",
            "wax deposition": "wax",
            "wax plug": "wax deposition",
            "pour point": "WAT",
            "cloud point": "WAT",

            # Asphaltene terms
            "asphaltene deposition": "asphaltene precipitation",
            "asphaltene plugging": "asphaltene precipitation",

            # Scale terms
            "calcium carbonate": "CaCO3 scale",
            "barium sulfate": "BaSO4 scale",
            "scale deposition": "scale formation",
            "scaling": "scale formation",

            # Flow terms
            "slugging": "terrain slugging",
            "liquid surge": "terrain slugging",
            "two-phase flow": "multiphase flow",
            "three-phase flow": "multiphase flow",

            # Pigging terms
            "scraping": "pigging",
            "pipeline pig": "pigging",
            "smart pig": "intelligent pigging",
            "ILI": "intelligent pigging",

            # Corrosion terms
            "CO2 corrosion": "sweet corrosion",
            "carbonic acid": "sweet corrosion",
            "erosion-corrosion": "erosional velocity",
        }

        normalized = query.lower()
        for term, replacement in normalizations.items():
            normalized = normalized.replace(term.lower(), replacement)

        return normalized

    # ============================================================================
    # THREE-LAYER RESPONSE SYSTEM
    # ============================================================================

    def _check_doctrine_cache(self, query: str) -> Optional[DoctrineBlock]:
        """Layer 1: Fast cache lookup (0-50ms)"""
        normalized = self._normalize_query(query)
        query_terms = set(normalized.lower().split())

        best_match = None
        best_score = 0

        for doctrine_key, doctrine in self.doctrine_cache.items():
            # Match on keywords
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in normalized)

            # Match on topic terms
            topic_terms = set(doctrine.topic.lower().split())
            topic_matches = len(query_terms.intersection(topic_terms))

            score = keyword_matches * 3 + topic_matches

            if score > best_score:
                best_score = score
                best_match = doctrine

        # Require minimum score threshold
        if best_score >= 3:
            best_match.hit_count += 1
            best_match.last_triggered = datetime.utcnow().isoformat()
            self.metrics["cache_hits"] += 1
            self.coverage_map[best_match.topic] += 1
            return best_match

        self.metrics["cache_misses"] += 1
        return None

    def _semantic_search(self, query: str, top_k: int = 3) -> List[DoctrineBlock]:
        """Layer 2: Semantic search across doctrine blocks (50-200ms)"""
        # Simplified semantic search using keyword matching
        # In production, would use vector embeddings

        normalized = self._normalize_query(query)
        query_terms = set(normalized.lower().split())

        scored_doctrines = []
        for doctrine in self.doctrine_cache.values():
            keyword_score = sum(2 for kw in doctrine.keywords if kw.lower() in normalized)
            topic_score = len(query_terms.intersection(set(doctrine.topic.lower().split())))
            framework_terms = set(doctrine.reasoning_framework.lower().split())
            framework_score = len(query_terms.intersection(framework_terms)) / 10

            total_score = keyword_score + topic_score + framework_score

            if total_score > 0:
                scored_doctrines.append((total_score, doctrine))

        scored_doctrines.sort(reverse=True, key=lambda x: x[0])

        results = [doctrine for score, doctrine in scored_doctrines[:top_k]]

        for doctrine in results:
            doctrine.hit_count += 1
            doctrine.last_triggered = datetime.utcnow().isoformat()
            self.coverage_map[doctrine.topic] += 1

        return results

    def _deep_analysis(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
        """Layer 3: Deep analysis with multi-doctrine synthesis (200ms+)"""
        # Get top doctrines
        relevant_doctrines = self._semantic_search(query, top_k=5)

        if not relevant_doctrines:
            return self._handle_coverage_gap(query, mode, zone)

        # Build response based on mode
        if mode == ResponseMode.FAST:
            # Concise answer from top doctrine
            top = relevant_doctrines[0]
            return f"{top.conclusion_template}\n\nKey factors: {', '.join(top.key_factors[:3])}."

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready response with authorities
            response_parts = []
            for doctrine in relevant_doctrines[:3]:
                response_parts.append(f"**{doctrine.topic}**")
                response_parts.append(doctrine.conclusion_template)
                response_parts.append(f"\nAuthorities: {'; '.join(doctrine.primary_authority)}")
                response_parts.append(f"Confidence: {doctrine.confidence.value}\n")
            return "\n".join(response_parts)

        else:  # MEMO mode
            # Comprehensive memorandum
            response_parts = []
            response_parts.append("TECHNICAL MEMORANDUM: PIPELINE FLOW ASSURANCE ANALYSIS\n")

            for i, doctrine in enumerate(relevant_doctrines[:3], 1):
                response_parts.append(f"\n{i}. {doctrine.topic.upper()}")
                response_parts.append(f"\nConclusion: {doctrine.conclusion_template}")
                response_parts.append(f"\nAnalysis Framework:\n{doctrine.reasoning_framework[:500]}...")
                response_parts.append(f"\nKey Factors:")
                for factor in doctrine.key_factors:
                    response_parts.append(f"  - {factor}")
                response_parts.append(f"\nPrimary Authority:")
                for auth in doctrine.primary_authority:
                    response_parts.append(f"  - {auth}")
                response_parts.append(f"\nConfidence Level: {doctrine.confidence.value}")
                response_parts.append(f"Stratification: {doctrine.confidence_stratification}\n")

            return "\n".join(response_parts)

    def _handle_coverage_gap(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
        """Handle queries with no matching doctrines"""
        gap_response = (
            "EPISTEMIC LIMITATION: This query addresses pipeline flow assurance topics "
            "outside the current doctrine coverage. "
        )

        if zone == AnalysisZone.AUDIT:
            gap_response += (
                "For audit purposes, recommend engaging specialist flow assurance consultant "
                "with expertise in this specific area. Avoid unsupported technical assertions."
            )
        else:
            gap_response += (
                "Recommend consulting industry references (SPE, ASME, API, NACE) or specialist "
                "flow assurance engineering firms for authoritative guidance on this topic."
            )

        return gap_response

    # ============================================================================
    # QUERY PROCESSING
    # ============================================================================

    async def process_query(self, request: QueryRequest) -> QueryResponse:
        """Main query processing with three-layer response"""
        start_time = time.time()

        self.metrics["total_queries"] += 1
        self.metrics["mode_usage"][request.mode.value] += 1
        self.metrics["zone_usage"][request.zone.value] += 1

        # Layer 1: Cache check
        cached_doctrine = self._check_doctrine_cache(request.query)

        if cached_doctrine and request.mode == ResponseMode.FAST:
            # Fast path: return cached conclusion
            answer = cached_doctrine.conclusion_template
            triggered = [cached_doctrine.topic]
            confidence = cached_doctrine.confidence
        else:
            # Layer 2 or 3: Semantic search or deep analysis
            if request.mode == ResponseMode.FAST and not cached_doctrine:
                relevant = self._semantic_search(request.query, top_k=1)
                if relevant:
                    answer = relevant[0].conclusion_template
                    triggered = [relevant[0].topic]
                    confidence = relevant[0].confidence
                else:
                    answer = self._handle_coverage_gap(request.query, request.mode, request.zone)
                    triggered = []
                    confidence = ConfidenceLevel.DISCLOSURE
            else:
                # Deep analysis
                answer = self._deep_analysis(request.query, request.mode, request.zone)
                relevant = self._semantic_search(request.query, top_k=5)
                triggered = [d.topic for d in relevant]
                confidence = relevant[0].confidence if relevant else ConfidenceLevel.DISCLOSURE

        # Calculate determinism hash
        hash_input = f"{request.query}|{request.mode.value}|{answer}"
        determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        # Identify coverage gaps
        coverage_gaps = self._identify_coverage_gaps(request.query)

        processing_time = (time.time() - start_time) * 1000
        self.metrics["total_processing_time_ms"] += processing_time

        # Audit trail
        self._write_audit_log(request, answer, triggered, processing_time, determinism_hash)

        return QueryResponse(
            answer=answer,
            mode=request.mode,
            zone=request.zone,
            confidence=confidence,
            triggered_doctrines=triggered,
            processing_time_ms=round(processing_time, 2),
            determinism_hash=determinism_hash,
            coverage_gaps=coverage_gaps,
            metadata={
                "doctrine_cache_size": len(self.doctrine_cache),
                "cache_hit": cached_doctrine is not None,
                "query_length": len(request.query),
            }
        )

    def _identify_coverage_gaps(self, query: str) -> List[str]:
        """Identify topics mentioned in query but not covered by doctrines"""
        gaps = []

        # Check for key flow assurance topics
        topic_coverage = {
            "hydrate": any("hydrate" in d.topic.lower() for d in self.doctrine_cache.values()),
            "wax": any("wax" in d.topic.lower() for d in self.doctrine_cache.values()),
            "asphaltene": any("asphaltene" in d.topic.lower() for d in self.doctrine_cache.values()),
            "scale": any("scale" in d.topic.lower() for d in self.doctrine_cache.values()),
            "slug": any("slug" in d.topic.lower() for d in self.doctrine_cache.values()),
            "multiphase": any("multiphase" in d.topic.lower() for d in self.doctrine_cache.values()),
            "corrosion": any("corrosion" in d.topic.lower() for d in self.doctrine_cache.values()),
            "erosion": any("erosion" in d.topic.lower() for d in self.doctrine_cache.values()),
        }

        query_lower = query.lower()
        for topic, has_coverage in topic_coverage.items():
            if topic in query_lower and not has_coverage:
                gaps.append(f"Limited doctrine coverage for {topic}")

        return gaps

    def _write_audit_log(self, request: QueryRequest, answer: str, triggered: List[str],
                         processing_time: float, determinism_hash: str):
        """Write query to audit trail"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": request.query,
            "mode": request.mode.value,
            "zone": request.zone.value,
            "triggered_doctrines": triggered,
            "answer_length": len(answer),
            "processing_time_ms": processing_time,
            "determinism_hash": determinism_hash,
        }

        with open(self.audit_log_path, "a") as f:
            f.write(json.dumps(audit_entry) + "\n")

    # ============================================================================
    # HEALTH & METRICS
    # ============================================================================

    def get_health(self) -> HealthResponse:
        """Health check endpoint"""
        uptime = time.time() - self.start_time
        avg_response_time = (
            self.metrics["total_processing_time_ms"] / self.metrics["total_queries"]
            if self.metrics["total_queries"] > 0
            else 0.0
        )

        cache_hit_rate = (
            self.metrics["cache_hits"] / (self.metrics["cache_hits"] + self.metrics["cache_misses"])
            if (self.metrics["cache_hits"] + self.metrics["cache_misses"]) > 0
            else 0.0
        )

        return HealthResponse(
            status="healthy",
            version=self.version,
            port=self.port,
            doctrine_count=len(self.doctrine_cache),
            total_queries=self.metrics["total_queries"],
            avg_response_time_ms=round(avg_response_time, 2),
            uptime_seconds=round(uptime, 2),
            cache_hit_rate=round(cache_hit_rate, 3),
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="PROD10 Pipeline Flow Assurance Intelligence Engine",
    description="TIE-Grade production intelligence for pipeline flow assurance challenges",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = PipelineFlowAssuranceEngine()


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Process pipeline flow assurance query"""
    try:
        return await engine.process_query(request)
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint"""
    return engine.get_health()


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine blocks"""
    return {
        "total": len(engine.doctrine_cache),
        "doctrines": [
            {
                "key": key,
                "topic": doctrine.topic,
                "keywords": doctrine.keywords,
                "hit_count": doctrine.hit_count,
                "last_triggered": doctrine.last_triggered,
                "confidence": doctrine.confidence.value,
            }
            for key, doctrine in engine.doctrine_cache.items()
        ]
    }


@app.get("/metrics")
async def metrics_endpoint():
    """Detailed metrics"""
    return {
        "total_queries": engine.metrics["total_queries"],
        "cache_hits": engine.metrics["cache_hits"],
        "cache_misses": engine.metrics["cache_misses"],
        "mode_usage": dict(engine.metrics["mode_usage"]),
        "zone_usage": dict(engine.metrics["zone_usage"]),
        "doctrine_triggers": dict(engine.metrics["doctrine_triggers"]),
        "coverage_map": dict(engine.coverage_map),
        "avg_processing_time_ms": (
            engine.metrics["total_processing_time_ms"] / engine.metrics["total_queries"]
            if engine.metrics["total_queries"] > 0
            else 0.0
        ),
    }


if __name__ == "__main__":
    logger.info(f"Starting PROD10 Pipeline Flow Assurance Engine on port {engine.port}")
    uvicorn.run(app, host="0.0.0.0", port=engine.port)
