"""
PROD09 Corrosion Monitoring Intelligence Engine
Production corrosion mechanisms, monitoring, treatment, and integrity management
Port: 9224 | TIE-Grade | Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict, Counter

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

ENGINE_NAME = "PROD09_corrosion_monitoring"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 9224
AUDIT_LOG_PATH = Path(__file__).parent / "audit_trail.jsonl"

logger.add(
    Path(__file__).parent / "engine.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# ═══════════════════════════════════════════════════════════════════════════
# ENUMS & DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════

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
    CO2_CORROSION = "CO2_CORROSION"
    H2S_CORROSION = "H2S_CORROSION"
    MICROBIAL_CORROSION = "MICROBIAL_CORROSION"
    EROSION_CORROSION = "EROSION_CORROSION"
    GALVANIC_CORROSION = "GALVANIC_CORROSION"
    PITTING_CORROSION = "PITTING_CORROSION"
    MONITORING_TECHNIQUES = "MONITORING_TECHNIQUES"
    CHEMICAL_TREATMENT = "CHEMICAL_TREATMENT"
    MATERIAL_SELECTION = "MATERIAL_SELECTION"
    INTEGRITY_MANAGEMENT = "INTEGRITY_MANAGEMENT"
    CATHODIC_PROTECTION = "CATHODIC_PROTECTION"
    INSPECTION_METHODS = "INSPECTION_METHODS"

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
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    issue_category: IssueCategory
    triggered_count: int = 0

class QueryRequest(BaseModel):
    query: str = Field(..., description="Corrosion monitoring query")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.REPORTING, description="Analysis context zone")
    include_telemetry: bool = Field(default=False, description="Include performance metrics")

class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    zone: AnalysisZone
    triggered_doctrines: List[str]
    issue_categories: List[str]
    reasoning_chain: Optional[List[str]] = None
    authorities_cited: List[str]
    determinism_hash: str
    telemetry: Optional[Dict[str, Any]] = None
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrine_count: int
    total_queries: int
    avg_latency_ms: float
    cache_hit_rate: float
    uptime_seconds: float

# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ REAL CORROSION DOMAIN BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="CO2 Corrosion Mechanism and de Waard-Milliams Model",
        keywords=["co2", "sweet corrosion", "carbonic acid", "dewaard", "corrosion rate prediction"],
        conclusion_template="CO2 corrosion rates are predictable using the de Waard-Milliams model, incorporating temperature, partial pressure, and flow regime. Rates increase exponentially with temperature up to 60-80 degC, then decrease due to protective scale formation.",
        reasoning_framework="""
CO2 Corrosion Chemistry:
1. CO2 + H2O → H2CO3 (carbonic acid formation)
2. H2CO3 → H+ + HCO3- (acid dissociation, pH reduction)
3. Fe + H2CO3 → FeCO3 + H2 (iron dissolution)
4. FeCO3 precipitation forms protective scale at high temperature/pH

de Waard-Milliams Correlation (1975, updated 1991):
- Log(CR) = 5.8 - 1710/T + 0.67*log(pCO2)
- CR = corrosion rate (mm/year)
- T = temperature (Kelvin)
- pCO2 = partial pressure CO2 (bar)

Temperature Effects:
- Below 60 degC: Rate increases with temperature (kinetics dominate)
- Above 80 degC: FeCO3 scale provides protection (mass transfer limited)
- Peak corrosion typically 60-80 degC in flowing systems

Flow Regime Impact:
- Laminar flow: Uniform corrosion, scale protective
- Turbulent flow: Scale disruption, localized attack, mesa corrosion
- High velocity (>3 m/s): Erosion-corrosion, scale removal

Partial Pressure Considerations:
- pCO2 > 7 psi (0.5 bar): Severe corrosion risk
- pCO2 = 0.5-7 psi: Moderate risk, inhibitor required
- pCO2 < 0.5 psi: Minimal risk in water-wet systems

Water Chemistry Modifiers:
- pH increase: Reduces corrosion, promotes FeCO3 precipitation
- Chloride content: Increases corrosion, disrupts scale
- Calcium: Enhances FeCO3 scale formation
- Glycol contamination: Disrupts scale, increases corrosion
        """,
        key_factors=[
            "Temperature range and profile (exponential kinetics)",
            "CO2 partial pressure (log relationship to rate)",
            "Flow velocity and regime (turbulence effects)",
            "Water pH and alkalinity (scale formation potential)",
            "Chloride and calcium concentrations",
            "FeCO3 scale formation and stability",
            "Glycol or MEG contamination presence"
        ],
        primary_authority=[
            "de Waard & Milliams (1975) - Original CO2 corrosion model",
            "NACE SP0775-2018 - CO2 Corrosion in Oil and Gas Production",
            "API RP 14E - Design and Installation of Offshore Production Platform Piping Systems",
            "NORSOK M-506 - CO2 Corrosion Rate Calculation Model"
        ],
        burden_holder="Operator - prove corrosion rates within design limits",
        adversary_position="Regulatory/insurance may challenge model applicability to specific conditions",
        counter_arguments=[
            "Model assumes pure water, not valid for oil-wet systems",
            "Flow effects not fully captured in original correlation",
            "Glycol contamination invalidates predictions",
            "Localized corrosion not predicted by uniform corrosion models",
            "Scale protectiveness varies with operational upsets"
        ],
        resolution_strategy="Use conservative model inputs, validate with corrosion monitoring data, apply safety factors for turbulent flow",
        entity_scope="Oil and gas production systems with CO2-containing fluids",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for steady-state conditions, moderate for transient operations",
        controlling_precedent="NACE SP0775-2018 is industry standard for CO2 corrosion assessment",
        issue_category=IssueCategory.CO2_CORROSION
    ),

    DoctrineBlock(
        topic="H2S Corrosion and Sulfide Stress Cracking (SSC)",
        keywords=["h2s", "sour service", "ssc", "nace mr0175", "sulfide stress cracking"],
        conclusion_template="H2S corrosion presents dual threats: uniform corrosion and sulfide stress cracking. NACE MR0175/ISO 15156 governs material selection based on H2S partial pressure and hardness limits (HRC 22 for carbon steel).",
        reasoning_framework="""
H2S Corrosion Mechanisms:
1. H2S dissolution: H2S + H2O → H2S(aq)
2. Acid formation: H2S → H+ + HS- (pH reduction)
3. Iron sulfide formation: Fe + H2S → FeS + H2
4. Atomic hydrogen generation: H+ + e- → H (absorbed into steel)

Sulfide Stress Cracking (SSC):
- Hydrogen embrittlement mechanism in presence of H2S and tensile stress
- Catastrophic brittle failure without warning
- Threshold stress as low as 60-80% of yield strength
- Time-delayed cracking (hours to years after exposure)

NACE MR0175/ISO 15156 Requirements:
Part 2 (Carbon Steels):
- pH2S < 0.05 psia: No restrictions
- pH2S 0.05-3 psia: HRC ≤ 22 (248 HBW) maximum hardness
- pH2S > 3 psia: Requires CRA or specific qualified materials
- HAZ (heat affected zones) critical - PWHT required for welds

Part 3 (CRAs - Corrosion Resistant Alloys):
- 13Cr: Suitable to ~25 psia H2S with chloride limits
- Duplex SS (22Cr, 25Cr): To 100+ psia H2S, high strength
- Super duplex: Extreme conditions, chloride + H2S
- Nickel alloys (Inconel 625, 825): Highest resistance

Environmental Severity Assessment:
- Region 0: pH2S < 0.05 psia, no SSC risk
- Region 1: pH2S 0.05-1.5 psia, limited requirements
- Region 2: pH2S 1.5-22 psia, moderate severity
- Region 3: pH2S > 22 psia, severe environment

Critical Design Considerations:
- No field hardening (welding, cold working) above HRC 22
- PWHT for all welds in sour service (650 degC minimum)
- Hardness testing of HAZ mandatory (HRC or HV conversion)
- Pressure-containing bolting ≤ HRC 22 or qualified material
- Upset conditions (H2S slugs) require design basis review
        """,
        key_factors=[
            "H2S partial pressure (psia) - primary severity driver",
            "Material hardness (HRC 22 limit for CS)",
            "Temperature (affects H2S solubility and kinetics)",
            "pH and chloride content (synergistic effects)",
            "Tensile stress level (residual + applied)",
            "Weld heat affected zones (hardness spikes)",
            "Transient upset conditions (H2S slugs)"
        ],
        primary_authority=[
            "NACE MR0175/ISO 15156 (all parts) - Sour Service Material Requirements",
            "API RP 571 - Damage Mechanisms in Refining and Petrochemical",
            "NACE TM0177 - Laboratory SSC Testing",
            "NACE TM0284 - HIC (Hydrogen Induced Cracking) Testing"
        ],
        burden_holder="Operator - demonstrate material compliance with MR0175 for operating conditions",
        adversary_position="Regulators may require testing proof for non-standard materials or conditions",
        counter_arguments=[
            "Historical safe operation doesn't prove future compliance",
            "Upset conditions may exceed design basis H2S levels",
            "Welding/repair hardness may exceed HRC 22 without PWHT",
            "Chloride + H2S synergy increases SSC susceptibility",
            "Long-term exposure (years) may reveal latent cracking"
        ],
        resolution_strategy="Maintain hardness records, PWHT documentation, upset condition H2S modeling, periodic inspection",
        entity_scope="All pressure-containing equipment in sour (H2S) service",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for materials within MR0175 limits, disclosure required for excursions",
        controlling_precedent="NACE MR0175/ISO 15156 is universally accepted regulatory standard",
        issue_category=IssueCategory.H2S_CORROSION
    ),

    DoctrineBlock(
        topic="Microbiologically Influenced Corrosion (MIC)",
        keywords=["mic", "bacteria", "srb", "apb", "biofilm", "microbial corrosion"],
        conclusion_template="MIC results from bacterial colonization (SRB, APB, iron-oxidizing) creating aggressive microenvironments. Detection requires microbiological testing (BART, qPCR), treatment with biocides (quaternary amines, glutaraldehyde), and system cleanliness.",
        reasoning_framework="""
MIC Causative Organisms:
1. Sulfate-Reducing Bacteria (SRB):
   - Desulfovibrio, Desulfotomaculum species
   - Reduce SO4²⁻ → H2S (localized acidification)
   - Anaerobic, thrive in stagnant zones, under deposits
   - Classic "black slime" biofilm appearance

2. Acid-Producing Bacteria (APB):
   - Produce organic acids (acetic, lactic, formic)
   - Aerobic or facultative anaerobic
   - pH < 4 in biofilm microenvironment

3. Iron-Oxidizing/Reducing Bacteria:
   - Gallionella, Leptothrix (oxidizing)
   - Shewanella (reducing)
   - Form voluminous tubercles, create differential aeration cells

4. Slime-Forming Bacteria:
   - Pseudomonas, Flavobacterium
   - Create protective biofilm for SRB colonization
   - Enhance localized corrosion under deposits

MIC Mechanisms:
- Biofilm creates differential aeration cells (cathode vs anode zones)
- Metabolic products (H2S, organic acids) cause localized pH < 3
- Cathodic depolarization by bacterial electron transfer
- Protective film disruption by bacterial exopolymers

Detection Methods:
BART (Biological Activity Reaction Test):
- SRB-BART: Detects SRB via blackening (FeS formation)
- APB-BART: pH-based acid production detection
- Results in 1-5 days, semi-quantitative (10²-10⁶ cells/mL)

Molecular Methods (qPCR):
- DNA quantification of specific bacterial species
- Faster results (hours), higher sensitivity
- Identifies non-culturable organisms

Serial Dilution Culture:
- Specific media (Postgate's for SRB)
- Quantitative but slow (2-4 weeks)
- Gold standard for speciation

Field Indicators:
- Pitting under black deposits (tubercles)
- Localized attack in stagnant zones (dead legs)
- Rapid failure after system shutdown/startup
- Odor of H2S in low-H2S design systems

Treatment Strategies:
Chemical Biocides:
- Quaternary ammonium compounds (QUAT): Broad spectrum, filming biocide
- Glutaraldehyde: Fast-acting, non-oxidizing, effective on biofilms
- THPS (Tetrakis): SRB-specific, degrades to sulfate
- Chlorine/hypochlorite: Oxidizing, residual protection

Application Methods:
- Continuous injection: 10-50 ppm for control
- Slug/shock treatment: 200-1000 ppm for cleanout
- Batch treatment: Isolated system, extended contact time

Prevention:
- System velocity > 1 m/s (minimize stagnant zones)
- Pigging frequency to remove deposits and biofilm
- Oxygen scavenging (SRB require anaerobic conditions)
- Biocide residual monitoring
        """,
        key_factors=[
            "Bacterial population type and concentration (SRB, APB)",
            "System stagnation and flow velocity (biofilm formation)",
            "Deposit accumulation (creates anaerobic zones)",
            "Water quality (nutrients, oxygen, temperature)",
            "Biocide treatment frequency and effectiveness",
            "Pigging and cleaning frequency",
            "System startup/shutdown cycles (bacterial blooms)"
        ],
        primary_authority=[
            "NACE SP0775-2018 - Section on MIC in Oil & Gas",
            "API RP 38 - Biological Analysis of Subsurface Waters",
            "NACE TM0194 - Field Monitoring of Bacterial Growth",
            "NACE Publication 34109 - Microbiologically Influenced Corrosion Handbook"
        ],
        burden_holder="Operator - detect and control bacterial contamination via monitoring and treatment",
        adversary_position="Regulators may require proof of effective MIC control program",
        counter_arguments=[
            "MIC detection is unreliable (sampling issues, non-culturable bacteria)",
            "Biocide treatment is ineffective on established biofilms",
            "Pigging disrupts biofilm but redistributes bacteria",
            "Low bacterial counts don't exclude MIC (localized colonies)",
            "Oxygen ingress during shutdown creates MIC risk"
        ],
        resolution_strategy="Multi-method detection (BART + qPCR + culture), regular biocide slug treatments, pigging program, oxygen control",
        entity_scope="Water-handling production systems, injection systems, subsea equipment",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence in MIC attribution (difficult to prove causation), high confidence in treatment efficacy",
        controlling_precedent="NACE SP0775 and API RP 38 define industry best practices",
        issue_category=IssueCategory.MICROBIAL_CORROSION
    ),

    DoctrineBlock(
        topic="Corrosion Coupon Monitoring",
        keywords=["coupon", "weight loss", "corrosion rate", "mill scale", "coupon analysis"],
        conclusion_template="Corrosion coupons provide direct corrosion rate measurement via weight loss after exposure. Requires 30-90 day exposure, proper surface preparation, and correction for mill scale loss. Rates in mpy (mils per year) or mm/year.",
        reasoning_framework="""
Coupon Design and Installation:
- Geometry: Rectangular (1x2 inch, 2x3 inch) or cylindrical
- Material: Match pipe metallurgy (C1018, L80, 13Cr, etc.)
- Surface finish: Mill scale as-received or pre-corroded
- Mounting: Flush mount holders, avoid crevice corrosion
- Orientation: Parallel to flow, representative velocity
- Access: Installed in coupon holders with isolation valves

Exposure Period:
- Minimum 30 days for measurable weight loss (5+ mils)
- Typical 60-90 days for statistical confidence
- Longer exposure for low corrosion rate environments
- Avoid >180 days (excessive pitting, non-linear kinetics)

Coupon Retrieval and Analysis:
1. Document condition: Photos, pit depth, deposit appearance
2. Cleaning: Remove deposits (not corrosion product)
   - NACE TM0194 cleaning procedures
   - Avoid over-cleaning (removes metal)
3. Weight loss measurement: Precision balance (0.1 mg)
4. Corrosion rate calculation:

   CR (mpy) = (534 × W) / (D × A × T)

   W = weight loss (mg)
   D = density (g/cm³) - 7.85 for steel
   A = surface area (in²)
   T = exposure time (hours)

   CR (mm/year) = CR (mpy) × 0.0254

Mill Scale Correction:
- New coupons have mill scale (iron oxide from rolling)
- Initial weight loss (first 30 days) includes scale loss
- Correction: Use pre-corroded coupons or subtract initial rate
- Pre-corrosion: 7-14 day exposure before test period start

Pitting Analysis:
- Measure maximum pit depth with depth micrometer
- Pitting factor = Max pit depth / Average metal loss
- Pitting factor > 3 indicates localized corrosion
- Record pit morphology (hemispherical, undercut, etc.)

Data Interpretation:
- General corrosion: Uniform weight loss, pitting factor < 2
- Localized corrosion: Non-uniform loss, pitting factor > 3
- Erosion-corrosion: Directional grooving, flow-facing surface
- MIC: Pitting under deposits, black FeS product

Coupon Placement Strategy:
- Multiple locations: Upstream/downstream, top/bottom of pipe
- Critical points: After injection points, elbows, tees
- Reference locations: Low-risk areas for baseline comparison
- Minimum 3 coupons per location for statistical validity

Limitations:
- Point measurement, not representative of entire system
- Installation effects (crevice, flow disturbance)
- Time lag (30-90 days to detect rate change)
- Handling damage during retrieval/cleaning
- Mill scale artifacts on new coupons
        """,
        key_factors=[
            "Coupon material match to pipe metallurgy",
            "Exposure period duration (30-90 days typical)",
            "Proper cleaning procedure (avoid over-cleaning)",
            "Mill scale correction for new coupons",
            "Pit depth measurement and pitting factor",
            "Multiple coupon locations for spatial coverage",
            "Statistical validity (replicate coupons)"
        ],
        primary_authority=[
            "NACE TM0194 - Field Monitoring of Bacterial Growth in Oil and Gas Systems",
            "NACE SP0775-2018 - Corrosion Coupon Installation and Analysis",
            "ASTM G1 - Standard Practice for Preparing, Cleaning, and Evaluating Corrosion Test Specimens",
            "ASTM G46 - Standard Guide for Examination and Evaluation of Pitting Corrosion"
        ],
        burden_holder="Operator - install, retrieve, analyze coupons per standards; maintain exposure records",
        adversary_position="Regulators may question coupon representativeness or cleaning procedures",
        counter_arguments=[
            "Single coupon doesn't represent system-wide corrosion",
            "Installation crevice affects local corrosion rate",
            "Cleaning procedure removes metal, inflates rate",
            "Mill scale loss skews initial measurements",
            "Time lag prevents real-time corrosion control"
        ],
        resolution_strategy="Multiple locations, replicate coupons, standardized cleaning per ASTM G1, pre-corroded coupons to eliminate mill scale",
        entity_scope="All production systems requiring corrosion rate verification",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when per NACE/ASTM standards, moderate for non-standard procedures",
        controlling_precedent="ASTM G1 and NACE TM0194 define accepted coupon analysis methods",
        issue_category=IssueCategory.MONITORING_TECHNIQUES
    ),

    DoctrineBlock(
        topic="Electrical Resistance (ER) Probes",
        keywords=["er probe", "electrical resistance", "real-time monitoring", "metal loss", "corrosion trend"],
        conclusion_template="ER probes measure metal loss via resistance change in a sensing element, providing continuous corrosion rate data. Resolution ~0.1 mil, response time hours to days. Suitable for tracking trends and chemical treatment effectiveness.",
        reasoning_framework="""
ER Probe Operating Principle:
- Sensing element (wire, tube, strip-mesh) exposed to process
- Reference element sealed from process fluid
- Four-wire Kelvin connection eliminates lead resistance
- Resistance proportional to cross-sectional area:

  R = ρL/A

  ρ = resistivity (constant for given alloy)
  L = length (constant)
  A = cross-sectional area (decreases with corrosion)

- As corrosion thins element, A decreases, R increases
- ΔR converted to metal loss (mils) via calibration factor

Probe Designs:
1. Wire Loop (Flush Element):
   - 10-20 mil diameter wire in exposed loop
   - Fast response (hours), finite life (200-500 mils total loss)
   - Replace when 50-75% consumed

2. Tubular Element:
   - Thick-walled tube (40-100 mil wall)
   - Slower response (days), long life (years)
   - Suitable for low corrosion rate environments

3. Strip-Mesh Element:
   - Flat strip or mesh geometry
   - Moderate response and life
   - Good for erosion-corrosion (directional attack)

Measurement and Data Interpretation:
- Continuous resistance measurement (ohms)
- Conversion: ΔR → metal loss (mils) → corrosion rate (mpy)
- Instantaneous rate: Short-term slope (last 24-48 hours)
- Average rate: Long-term slope (weeks to months)

Corrosion Rate Calculation:
- Daily metal loss = (Reading_today - Reading_yesterday) mils
- Instantaneous rate (mpy) = Daily loss × 365
- Moving average (7-day, 30-day) smooths noise

Response Time and Sensitivity:
- Resolution: 0.1 mil typical (0.0025 mm)
- Detectable rate: 1-5 mpy minimum (depends on element life)
- Response time: Hours (thin wire) to days (thick tube)
- Noise: Temperature variations, electrical interference

Installation Considerations:
- Orientation: Parallel to flow for general corrosion
- Velocity: Match pipe flow velocity (representative environment)
- Temperature compensation: Required for accuracy (reference element)
- Avoid stagnant zones or flow disturbances
- Electrical grounding and isolation critical

Advantages:
- Real-time, continuous monitoring
- Trend detection (corrosion rate changes)
- Chemical treatment optimization (immediate feedback)
- No retrieval/analysis required
- Predictive maintenance (project remaining life)

Limitations:
- Point measurement (localized data)
- Finite life (element consumption)
- Low sensitivity for very low rates (<1 mpy)
- Pitting/localized attack not well represented
- Temperature sensitivity requires compensation
- Electrical noise and grounding issues
- Initial break-in period (oxide layer formation)

Optimal Use Cases:
- Chemical inhibitor effectiveness monitoring
- Upset detection (rapid rate increase)
- Seasonal or operational variation tracking
- Comparison of treatment programs (A/B testing)
- Compliance with corrosion rate limits (<5 mpy)
        """,
        key_factors=[
            "Probe element type and geometry (wire, tube, strip)",
            "Sensitivity and response time (hours to days)",
            "Temperature compensation accuracy",
            "Installation location and flow conditions",
            "Element remaining life (% consumed)",
            "Electrical grounding and noise mitigation",
            "Data smoothing (moving average vs. instantaneous rate)"
        ],
        primary_authority=[
            "NACE SP0775-2018 - ER Probe Application in Oil & Gas",
            "ASTM G96 - Online Monitoring of Corrosion in Plant Equipment",
            "API RP 45 - Recommended Practice for Analysis of Oilfield Waters",
            "NACE TM0497 - ER Probe Measurement Techniques"
        ],
        burden_holder="Operator - install, calibrate, maintain ER probes; interpret data trends",
        adversary_position="Regulators may question probe accuracy or representativeness of point measurement",
        counter_arguments=[
            "ER probe measures only local corrosion, not system-wide",
            "Temperature variations create false rate signals",
            "Electrical noise corrupts low-rate measurements",
            "Pitting attack not detected (averages over area)",
            "Element consumption limits long-term monitoring",
            "Initial break-in period delays accurate readings"
        ],
        resolution_strategy="Multiple probe locations, temperature-compensated models, moving average smoothing, coupon validation",
        entity_scope="Production systems requiring real-time corrosion monitoring and chemical treatment control",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for trend detection, moderate for absolute rate measurement",
        controlling_precedent="ASTM G96 and NACE SP0775 define ER probe best practices",
        issue_category=IssueCategory.MONITORING_TECHNIQUES
    ),

    DoctrineBlock(
        topic="Linear Polarization Resistance (LPR) Probes",
        keywords=["lpr", "linear polarization", "electrochemical", "instantaneous rate", "icorr"],
        conclusion_template="LPR probes measure instantaneous corrosion rate via electrochemical polarization (±10-30 mV from open circuit). Rapid response (minutes), high sensitivity (0.1 mpy), requires conductive electrolyte. Ideal for upset detection and treatment optimization.",
        reasoning_framework="""
LPR Electrochemical Principle:
- Three-electrode cell: Working (test), counter, reference
- Small voltage perturbation (±10-30 mV) applied to working electrode
- Resulting current measured (Faraday's law - proportional to corrosion)
- Polarization resistance Rp (ohms-cm²) calculated from Stern-Geary:

  Rp = ΔE / Δi

  ΔE = applied potential (mV)
  Δi = measured current density (µA/cm²)

Stern-Geary Equation:
  icorr = B / Rp

  icorr = corrosion current density (µA/cm²)
  B = Stern-Geary constant (mV) - typically 26 mV for steel in aerated water
  Rp = polarization resistance (ohm-cm²)

Conversion to Corrosion Rate:
  CR (mpy) = 0.13 × icorr × EW / ρ

  EW = equivalent weight (27.9 for steel)
  ρ = density (7.86 g/cm³ for steel)

Probe Design:
1. Two-electrode (simplified):
   - Working and counter combined (same material)
   - Pseudo-reference (third electrode, same material)
   - Lower accuracy but robust in field conditions

2. Three-electrode (standard):
   - Dedicated reference electrode (stable potential)
   - Working electrode (test material)
   - Counter electrode (completes circuit)
   - Higher accuracy, requires reference maintenance

Measurement Cycle:
- Potential scan: -10 mV to +10 mV (or -30 to +30 mV)
- Scan rate: 0.1-0.5 mV/s (quasi-steady state)
- Current response plotted vs. potential (I-V curve)
- Linear region slope = 1/Rp
- Calculation: icorr → corrosion rate (mpy)

Response Time and Sensitivity:
- Measurement time: 2-10 minutes per scan
- Update frequency: 15-60 minutes (avoid polarization effects)
- Sensitivity: 0.1 mpy detection limit
- Resolution: 0.01 mpy in clean systems

Advantages:
- Instantaneous corrosion rate (real-time)
- High sensitivity (detects low rates <1 mpy)
- Rapid upset detection (minutes to hours)
- Chemical treatment optimization (immediate feedback)
- No element consumption (non-destructive)
- Suitable for low corrosion rate environments

Limitations:
- Requires conductive electrolyte (water-continuous phase)
- Not applicable in oil-continuous or gas systems
- Electrode fouling/scaling affects accuracy
- Solution resistance (IR drop) correction needed
- Localized corrosion (pitting) underestimated
- Assumes uniform corrosion mechanism

Environmental Requirements:
- Water conductivity >100 µS/cm (minimum)
- Water-cut >30% for oil/water systems
- Temperature-stable environment (±5 degC)
- No gas slugging or foam (electrode exposure)

Calibration and Validation:
- B-constant verification (laboratory polarization curves)
- Coupon validation (LPR vs. weight loss comparison)
- Regular cleaning/maintenance (electrode surface)
- Reference electrode potential check (vs. SCE or Ag/AgCl)

Field Application Strategy:
- Install at injection points (chemical treatment evaluation)
- Multiple locations (spatial corrosion profile)
- Trend monitoring (detect upsets, treatment failures)
- Complement with coupons (validate absolute rates)
- Alarm thresholds (>5 mpy triggers investigation)
        """,
        key_factors=[
            "Water conductivity and water-cut (electrolyte requirement)",
            "B-constant accuracy (material and environment specific)",
            "Electrode surface condition (fouling, scaling)",
            "Solution resistance and IR drop correction",
            "Reference electrode stability",
            "Temperature stability during measurement",
            "Localized vs. uniform corrosion mode"
        ],
        primary_authority=[
            "ASTM G59 - Standard Test Method for Conducting Potentiodynamic Polarization Resistance Measurements",
            "NACE TM0497 - Measurement Techniques Related to Criteria for Cathodic Protection",
            "NACE SP0775-2018 - LPR Application in Corrosion Monitoring",
            "ASTM G102 - Calculation of Corrosion Rates from Electrochemical Measurements"
        ],
        burden_holder="Operator - install, calibrate, maintain LPR probes; validate with coupons",
        adversary_position="Regulators may question applicability in oil-continuous systems or low water-cut",
        counter_arguments=[
            "LPR invalid in oil-continuous phase (no conductivity)",
            "Electrode fouling invalidates measurements over time",
            "B-constant assumption inaccurate for mixed corrosion mechanisms",
            "Pitting corrosion severely underestimated by LPR",
            "Solution resistance causes large errors in low-conductivity fluids",
            "Gas slugging exposes electrodes, corrupts data"
        ],
        resolution_strategy="Water-cut monitoring, electrode cleaning schedule, coupon validation, B-constant verification for specific conditions",
        entity_scope="Water-continuous production systems, injection systems, wet gas pipelines with adequate water-cut",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="High confidence in water-continuous systems, low confidence in oil-continuous or low water-cut",
        controlling_precedent="ASTM G59 and G102 define standard LPR measurement and calculation procedures",
        issue_category=IssueCategory.MONITORING_TECHNIQUES
    ),

    DoctrineBlock(
        topic="Ultrasonic Thickness Measurement (UTM) and Inspection",
        keywords=["utm", "ultrasonic", "thickness", "remaining wall", "pigging inspection"],
        conclusion_template="Ultrasonic thickness measurement provides non-destructive remaining wall thickness assessment. Accuracy ±0.001 inch with proper calibration, detects general thinning and localized corrosion. Requires access, surface preparation, and qualified technicians per ASME V or API 510.",
        reasoning_framework="""
UT Measurement Principle:
- Piezoelectric transducer generates ultrasonic pulse (0.5-10 MHz)
- Sound wave travels through material at known velocity
- Reflection from back wall returns to transducer
- Time-of-flight measured, converted to thickness:

  Thickness = (Velocity × Time) / 2

  Velocity for steel ≈ 0.2330 inch/µs (5900 m/s)

Transducer Types:
1. Dual-element (separate send/receive):
   - Dead zone ~0.020 inch (thin materials)
   - Good for corroded/rough surfaces
   - Typical 5 MHz frequency

2. Single-element (pulse-echo):
   - Through-transmission mode
   - Requires smooth surface, couplant
   - Higher frequency (10 MHz) for precision

Couplant Requirements:
- Gel, oil, water (acoustic impedance matching)
- Eliminates air gap between transducer and surface
- Temperature-appropriate (high-temp gel for hot surfaces)

Calibration and Standards:
- Calibration block: Known thickness (per ASTM E797)
- Material-matched (same velocity as test piece)
- Multiple thickness steps (span range of interest)
- Verify zero point and linearity
- Daily calibration check

Measurement Accuracy:
- Resolution: 0.001 inch (0.025 mm) typical
- Accuracy: ±0.001-0.003 inch (depends on frequency, couplant)
- Repeatability: ±0.5% with good technique

Inspection Strategies:
Grid Pattern (CMLs - Corrosion Monitoring Locations):
- Defined grid (1-inch, 6-inch spacing per API 570)
- Permanent CML marking (paint, tags)
- Record coordinates, initial/current thickness
- Trend corrosion rates over time (years)

Scanning Technique:
- Continuous movement of transducer (detect local minima)
- Identify thin spots, pitting, erosion zones
- More comprehensive than single-point grid

Inline Inspection (ILI) Pigging:
- Magnetic flux leakage (MFL) or UT pig tools
- Full-length pipeline inspection (millions of points)
- Detects metal loss, pitting, cracking, dents
- Requires piggable pipeline (no restrictions)
- Data processing: ILI vendor analyzes, reports anomalies

Surface Preparation:
- Remove paint, scale, rust (affects coupling)
- Wire brush or grinder to bare metal
- Clean surface (oil, debris affects reading)
- Hot surfaces: Use high-temp couplant, delay gel

Temperature Considerations:
- Sound velocity changes with temperature
- Correction factors for elevated temperatures (>100 degF)
- Transducer limitations (max temp 150-300 degF depending on model)
- Delay line transducers for very hot surfaces

Data Interpretation:
- Remaining wall thickness vs. design minimum thickness
- Corrosion rate = (Initial - Current) / Time interval (years)
- Retirement thickness = Design min + safety margin
- Fitness-for-service assessment per API 579

Limitations:
- Access required (insulation removal, scaffolding)
- Surface preparation time-consuming
- Point or grid measurement (vs. full coverage)
- Trained operator required (certification per SNT-TC-1A)
- Couplant contamination of product in some cases
- Pitting depth measurement requires focused transducer
        """,
        key_factors=[
            "Transducer frequency and type (dual vs. single element)",
            "Calibration block material match and accuracy",
            "Surface preparation quality (coupling)",
            "Operator training and certification (SNT-TC-1A)",
            "CML location consistency (trending over time)",
            "Temperature correction for hot surfaces",
            "Grid density (inspection coverage)"
        ],
        primary_authority=[
            "ASME Section V - Nondestructive Examination (UT)",
            "API 570 - Piping Inspection Code (UT requirements)",
            "API 510 - Pressure Vessel Inspection Code",
            "ASTM E797 - Standard Practice for Measuring Thickness by Manual UT Pulse-Echo Contact Method",
            "API 579 - Fitness-for-Service (remaining life calculation)"
        ],
        burden_holder="Operator/owner - perform UT per code intervals, maintain CML records, qualified personnel",
        adversary_position="Regulators may require API 510/570 compliance, certified inspectors, documented CML history",
        counter_arguments=[
            "Grid inspection misses localized corrosion between CMLs",
            "Operator error (poor coupling, mis-calibration) invalidates data",
            "Infrequent inspection (5-10 year intervals) misses rapid corrosion",
            "CML location drift over time (imprecise repositioning)",
            "High-temperature surfaces require specialized equipment/training",
            "ILI pigging not feasible for unpiggable lines"
        ],
        resolution_strategy="Dense CML grids in high-risk areas, certified inspectors, annual trending, ILI pigging where feasible, scanning technique supplements grid",
        entity_scope="Pressure-containing piping and vessels subject to corrosion, per API 570/510 inspection intervals",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when per ASME V and API standards with certified personnel",
        controlling_precedent="ASME Section V and API 570/510 are regulatory-accepted UT standards",
        issue_category=IssueCategory.INSPECTION_METHODS
    ),

    DoctrineBlock(
        topic="Corrosion Inhibitor Selection - Film-Forming Amines",
        keywords=["inhibitor", "film-forming amine", "imidazoline", "quaternary amine", "filming inhibitor"],
        conclusion_template="Film-forming amine corrosion inhibitors (imidazolines, quaternary amines) adsorb onto steel surfaces creating hydrophobic barrier. Effective at 10-50 ppm for CO2 corrosion, requires oil-wetting for protection, dispersibility critical in water phase.",
        reasoning_framework="""
Inhibitor Chemistry and Mechanism:
1. Imidazoline-Based Inhibitors:
   - Structure: Five-membered heterocyclic ring (N-C-N)
   - Functional groups: Long-chain alkyl (C12-C18) - oil solubility
   - Adsorption: Nitrogen lone pairs bond to iron surface
   - Film formation: Hydrophobic alkyl chains orient outward
   - Barrier: Prevents water/acid contact with metal

2. Quaternary Ammonium Compounds (QUATs):
   - Structure: R4N+ (four alkyl groups, positive charge)
   - Cationic surfactant (attracted to negatively charged metal)
   - Dual function: Corrosion inhibitor + biocide
   - Filming action: Monolayer formation at metal interface

3. Amino Acids and Carboxylates:
   - Biodegradable "green" inhibitors
   - Adsorption via -COO- and -NH3+ groups
   - Lower effectiveness than imidazolines (higher dosage required)

Inhibitor Effectiveness Factors:
Concentration:
- Typical dose: 10-50 ppm active ingredient
- Higher dose for severe conditions (high CO2, temperature)
- Overdosing: Emulsion formation, water-wetting (counterproductive)

Temperature:
- Optimal performance: 60-150 degF (15-65 degC)
- High temperature (>200 degF): Thermal degradation of organics
- Low temperature (<40 degF): Poor dispersibility, wax-like deposits

Oil-Wetting Requirement:
- Inhibitor film must displace water from metal surface
- Oil-soluble formulation (dispersed in hydrocarbon phase)
- Requires minimum oil-to-water ratio (oil-continuous preferred)
- Water-wetting = corrosion (inhibitor ineffective if water contacts metal)

Dispersibility in Water:
- Paradox: Oil-soluble but must partition to water/metal interface
- Surfactant package improves water dispersion
- Inverted emulsion systems (oil-external microemulsion)
- Batch treatment: Pre-dilute in solvent before injection

Shear Stability:
- High-velocity systems (pumps, chokes) disrupt film
- Re-adsorption kinetics: Fast (imidazolines) vs. slow (fatty acids)
- Continuous injection maintains film under shear

Application Methods:
Continuous Injection:
- Metering pump at wellhead or separator inlet
- Dose based on water production rate (ppm in water phase)
- Residual monitoring (chemical tracer or analysis)

Batch Treatment:
- Slug dose (100-500 gallons) for well cleanout or startup
- Extended shut-in (6-24 hours) for adsorption
- Initial protection until continuous system operational

Squeeze Treatment (Downhole):
- High-volume injection into formation (1000-5000 gallons)
- Adsorption onto formation rock (sustained release)
- Protection period: Weeks to months (depends on production rate)
- Retreatment based on corrosion monitoring (coupons, ER)

Performance Testing:
Laboratory Screening:
- NACE TM0374 (Kettle test): Bubble CO2 through brine, measure weight loss
- Autoclave testing: Elevated temperature/pressure conditions
- Efficiency % = [(Blank rate - Inhibited rate) / Blank rate] × 100
- Target: >90% efficiency at proposed dose

Field Trials:
- Coupon racks or ER/LPR probes before/after treatment
- Establish baseline corrosion rate (no inhibitor)
- Inject inhibitor at increasing doses (10, 25, 50 ppm)
- Monitor rate reduction (target <5 mpy)

Inhibitor Residual Analysis:
- Colorimetric methods (complexation with indicator)
- Detects active ingredient concentration in produced water
- Confirms inhibitor reaching target (not adsorbing in tubulars)
- Adjust dose based on residual (too high = waste, too low = ineffective)

Environmental and Safety:
- Toxicity: LC50, LD50 for marine/aquatic organisms
- Biodegradability: OECD 301 testing (green inhibitors preferred)
- Offshore discharge limits: OSPAR, EPA regulations
- Handling: Flash point, corrosivity of concentrate
        """,
        key_factors=[
            "Inhibitor chemistry (imidazoline, QUAT, amino acid)",
            "Dosage concentration (10-50 ppm typical)",
            "Temperature range (affects stability and performance)",
            "Oil-wetting vs. water-wetting system conditions",
            "Dispersibility and surfactant package",
            "Application method (continuous, batch, squeeze)",
            "Performance testing (lab NACE TM0374, field trials)"
        ],
        primary_authority=[
            "NACE TM0374 - Laboratory Screening Tests to Determine the Ability of Scale Inhibitors to Prevent the Precipitation of Calcium Sulfate and Calcium Carbonate",
            "NACE SP0775-2018 - Corrosion Inhibitor Application",
            "EFC Publication 39 - Corrosion Inhibitors for Oil and Gas Production",
            "API RP 14E - Offshore Platform Piping Systems (inhibitor injection)"
        ],
        burden_holder="Operator - select, test, apply inhibitor at effective dose; monitor performance",
        adversary_position="Regulators may require toxicity data, discharge permits, proof of effectiveness",
        counter_arguments=[
            "Inhibitor ineffective in water-wet systems (film not formed)",
            "Overdosing causes emulsions, water quality issues",
            "High shear disrupts film, requires excessive dose",
            "Temperature extremes degrade inhibitor",
            "Environmental regulations prohibit certain chemistries",
            "Residual analysis doesn't prove surface protection (only bulk concentration)"
        ],
        resolution_strategy="Laboratory qualification per NACE TM0374, field trials with coupon validation, residual monitoring, oil-wetting confirmation",
        entity_scope="Oil and gas production systems with CO2 corrosion, liquid hydrocarbon phase for film formation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when properly tested and applied in oil-continuous systems, moderate in marginal oil-wetting",
        controlling_precedent="NACE TM0374 and SP0775 define inhibitor qualification and application standards",
        issue_category=IssueCategory.CHEMICAL_TREATMENT
    ),

    DoctrineBlock(
        topic="Corrosion-Resistant Alloy (CRA) Material Selection",
        keywords=["cra", "13cr", "duplex", "super duplex", "inconel", "material selection"],
        conclusion_template="CRA selection based on environmental severity (CO2, H2S, chloride, temperature). Carbon steel (inhibited) for mild service, 13Cr for moderate CO2/H2S, duplex/super duplex for severe chloride/H2S, nickel alloys (Inconel 625/825) for extreme conditions. NACE MR0175 Part 3 governs.",
        reasoning_framework="""
Material Selection Decision Tree:

1. Carbon Steel (API 5L, 5CT):
   - Sweet service: CO2 only, pH2S < 0.05 psia
   - Requires corrosion inhibitor program
   - Cost: Baseline ($)
   - Corrosion rate: 5-20+ mpy without inhibition
   - Limitations: Not suitable H2S > 0.05 psia (SSC risk)

2. 13% Chromium (13Cr) Martensitic Stainless:
   - Moderate sour service: pH2S < 25 psia, Cl < 50,000 ppm
   - Good CO2 resistance (passive film formation)
   - Cost: 2-3x carbon steel ($$)
   - Hardness control: HRC 22 max per NACE MR0175 Part 3
   - PWHT required for welds in sour service
   - Temperature limit: 450 degF (232 degC)
   - Applications: Tubing, flowlines, moderate sour wells

3. 22Cr Duplex Stainless Steel (2205):
   - Composition: 22Cr-5Ni-3Mo-0.15N (ferrite + austenite)
   - Severe service: pH2S to 100+ psia, Cl to 200,000 ppm
   - Excellent pitting resistance (PRE = Cr + 3.3Mo + 16N ≈ 35)
   - Cost: 4-5x carbon steel ($$$)
   - High strength (YS ≈ 80 ksi) - reduces wall thickness
   - Temperature range: -50 to 300 degF (-46 to 150 degC)
   - Limitations: 475 degC embrittlement (avoid 650-950 degF long-term)

4. 25Cr Super Duplex Stainless Steel (2507, Zeron 100):
   - Composition: 25Cr-7Ni-4Mo-0.25N
   - Extreme chloride + H2S: pH2S >100 psia, Cl >200,000 ppm
   - PRE ≈ 40-45 (superior pitting resistance)
   - Cost: 6-8x carbon steel ($$$$)
   - Applications: Subsea, HPHT wells, severe sour service
   - Weld qualification critical (maintain duplex structure in HAZ)

5. Nickel-Based Alloys (Inconel 625, 825, Hastelloy C-276):
   - Inconel 625: 61Ni-22Cr-9Mo - exceptional H2S resistance
   - Inconel 825: 42Ni-21Cr-3Mo - chloride SCC resistance
   - Cost: 10-15x carbon steel ($$$$$)
   - Applications: Extreme sour (pH2S >200 psia), high chloride + CO2 + H2S
   - Completions: Packers, hangers, safety valves in ultra-sour wells
   - Welding: GTAW (TIG) with controlled heat input, inert atmosphere

Environmental Severity Assessment:
NACE MR0175/ISO 15156 Part 3 Guidance:
- Table A.2: 13Cr limits (pH2S vs. temperature vs. chloride)
- Table A.27: Duplex limits (pH2S, temperature, chloride combinations)
- Environmental severity regions (0, 1, 2, 3 per Part 2)

Chloride Influence:
- Cl < 50,000 ppm: 13Cr acceptable in moderate sour
- Cl 50,000-150,000 ppm: 22Cr duplex required
- Cl > 150,000 ppm: 25Cr super duplex or nickel alloys
- Chloride + temperature synergy (SCC risk in austenitic SS)

CO2 Partial Pressure:
- pCO2 < 30 psi: Carbon steel with inhibitor or 13Cr
- pCO2 30-100 psi: 13Cr minimum
- pCO2 > 100 psi: Duplex or higher (passive film stability)

Temperature Considerations:
- <200 degF: All CRAs suitable (selection based on H2S/Cl)
- 200-350 degF: 13Cr, duplex, nickel alloys
- >350 degF: Duplex limited (embrittlement risk), nickel alloys preferred
- Thermal cycling: Duplex prone to sigma phase (reduce ductility)

Material Qualification:
- NACE TM0177 (SSC testing): H2S + stress + time (720 hours)
- NACE TM0316 (Four-point bend SSC test)
- ASTM G48 (Pitting resistance - FeCl3 test for PRE validation)
- Hardness testing: HV, HRC per NACE MR0175 limits
- Charpy impact testing: Verify toughness (duplex HAZ critical)

Cost-Benefit Analysis:
- Initial CAPEX: CRA 2-15x cost of carbon steel
- OPEX savings: Eliminate inhibitor program, reduce inspection
- Risk reduction: Eliminate SSC failures, extend asset life
- Breakeven: Typically 5-10 years for moderate sour, <5 years for severe

Field Considerations:
- Welding qualification: Duplex requires strict procedures (avoid embrittlement)
- Galling: Duplex prone to galling (special thread compounds required)
- Handling: Avoid steel contact (galvanic corrosion), use nylon slings
- Machining: Work hardening (duplex, nickel alloys require special tooling)
        """,
        key_factors=[
            "H2S partial pressure (primary driver for sour service)",
            "Chloride concentration (pitting and SCC risk)",
            "CO2 partial pressure (affects passive film stability)",
            "Temperature range (embrittlement, SCC considerations)",
            "Cost vs. risk tolerance (CAPEX vs. failure consequences)",
            "Welding and fabrication constraints",
            "NACE MR0175 Part 3 environmental limits"
        ],
        primary_authority=[
            "NACE MR0175/ISO 15156 Part 3 - CRA Material Requirements",
            "API 5CRA - Specification for CRA Tubing and Casing",
            "ASTM A276 - Stainless Steel Bars and Shapes",
            "NACE TM0177 - SSC Testing of Metals",
            "ASTM G48 - Pitting and Crevice Corrosion Resistance (PRE)"
        ],
        burden_holder="Operator - select CRA per MR0175 Part 3 for operating conditions, qualify materials/welding",
        adversary_position="Regulators may require material test reports, weld procedure qualification records, environmental justification",
        counter_arguments=[
            "CRA selection exceeds environmental severity (over-design)",
            "Cost not justified for remaining well life",
            "Welding procedures not qualified (HAZ embrittlement risk)",
            "Galling in threaded connections causes failures",
            "Upset conditions may exceed MR0175 Part 3 limits",
            "Long delivery times delay projects (exotic CRAs)"
        ],
        resolution_strategy="Conservative material selection per MR0175 Part 3 worst-case conditions, weld procedure qualification, cost-benefit analysis",
        entity_scope="Sour service wells, flowlines, and facilities with H2S or severe chloride environments",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when within MR0175 Part 3 environmental limits with qualified welding",
        controlling_precedent="NACE MR0175/ISO 15156 Part 3 is universally accepted CRA selection standard",
        issue_category=IssueCategory.MATERIAL_SELECTION
    ),

    DoctrineBlock(
        topic="Cathodic Protection (CP) for Pipelines and Structures",
        keywords=["cathodic protection", "impressed current", "sacrificial anode", "cp survey", "potential criteria"],
        conclusion_template="Cathodic protection polarizes steel to -0.85V CSE (Cu/CuSO4 reference) or 100 mV polarization shift, preventing corrosion electrochemically. Impressed current (rectifier) for long pipelines, sacrificial anodes (Mg, Zn, Al) for structures. Requires coating, regular surveys per NACE SP0169.",
        reasoning_framework="""
CP Electrochemical Principle:
- Corrosion = electrochemical reaction (anodic dissolution)
  Anode: Fe → Fe²⁺ + 2e⁻ (iron oxidation, metal loss)
  Cathode: O2 + 2H2O + 4e⁻ → 4OH⁻ (oxygen reduction)
- CP supplies electrons to steel (makes entire surface cathodic)
- Shifts potential negative (more reducing), stops anodic dissolution

NACE SP0169 Criteria for Protection:
1. -0.85 V CSE (Cu/CuSO4 reference electrode):
   - Absolute potential measurement (ON potential)
   - Instant-off potential preferred (eliminates IR drop)
   - Native potential typically -0.5 to -0.6 V CSE (bare steel in soil)

2. 100 mV Polarization Shift:
   - Native potential measured (no CP applied)
   - CP energized, measure polarized potential
   - Shift = Polarized - Native (must be ≥100 mV more negative)
   - Accounts for variable soil conditions

3. -0.95 V CSE for Bacteria or Elevated Temperature:
   - Higher protection level for SRB or >60 degC soil
   - Over-protection risk: Hydrogen embrittlement, coating disbondment

Impressed Current Cathodic Protection (ICCP):
Components:
- Rectifier: AC to DC conversion, adjustable output (0-50V, 0-100A typical)
- Anode bed: Inert anodes (graphite, MMO-coated Ti, high-silicon cast iron)
- Cable: Negative to pipeline, positive to anode bed
- Reference electrodes: Monitor potential at test stations

Design:
- Current requirement: 0.2-2 mA/ft² bare steel (depends on coating quality)
- Coated pipeline: 0.001-0.01 mA/ft² (coating shields, reduces current)
- Anode bed sizing: Deep vertical (100-300 ft) or horizontal distributed
- Anode consumption: Calculate life based on current density (years to decades)

Sacrificial Anode Cathodic Protection (SACP):
Anode Materials:
- Magnesium: -1.6 V CSE (highest driving voltage, fresh water/high resistivity soil)
- Zinc: -1.1 V CSE (seawater, moderate driving voltage)
- Aluminum: -1.05 V CSE (seawater, highest capacity Ah/lb)

Anode Selection:
- Driving voltage = Anode potential - Protected structure potential
- Mg: 0.75V driving voltage (aggressive protection)
- Zn/Al: 0.25V (less aggressive, suitable low-resistivity environments)

Bracelet Anodes (Pipelines):
- Installed at coating holidays or regular intervals (500-1000 ft)
- Bonded to pipe via thermite weld or mechanical clamp
- Weight: 10-50 lbs per anode (20-year design life typical)

Subsea Structure Anodes:
- Welded or bolted to jacket legs, risers, caissons
- Distributed coverage (anode spacing per current distribution modeling)
- Flush-mounted to avoid snagging (trawling areas)

CP Coating Interaction:
- Coating is primary corrosion control (CP is backup)
- Holiday (coating defect) = bare steel area requiring CP current
- Good coating: <1% bare area, minimal CP current
- Poor coating: High current demand, rapid anode consumption
- Coating breakdown over time increases CP current demand

CP Survey and Monitoring:
Annual Close-Interval Survey (CIS):
- Potential measurements every 2.5-10 ft along pipeline
- Identifies areas below -0.85V CSE (requires rectifier adjustment)
- Detects coating holidays (high current drain points)

Direct Current Voltage Gradient (DCVG):
- Locates coating holidays via voltage gradient over defect
- Walk pipeline with two reference electrodes (fixed spacing)
- Voltage spike indicates current flow (holiday location)

Alternating Current Voltage Gradient (ACVG):
- Detects coating defects via AC signal attenuation
- Transmitter induces AC on pipeline, receiver detects holidays
- Complements DCVG (different defect sensitivity)

Rectifier Inspection:
- Monthly: Check output voltage, current, AC input
- Annual: Verify ground bed resistance, anode consumption calculation
- Adjust output to maintain criteria (-0.85V CSE at all test stations)

Interference and Mitigation:
AC Interference:
- High-voltage transmission lines induce AC on pipeline
- Touch potential hazard (shock risk)
- Mitigation: Grounding, gradient control mats, zinc ribbon

DC Interference:
- Foreign CP system or DC-electrified rail causes stray current
- Anodic interference (accelerates corrosion)
- Mitigation: Bonding, forced drainage, insulating joints

Challenges:
- Shielding: Disbonded coating traps electrolyte, blocks CP current
- Attenuation: Current decays with distance from anode (long pipelines)
- Over-protection: Hydrogen embrittlement (high-strength steel), coating damage
- Current demand variability: Seasonal (soil moisture), coating degradation
        """,
        key_factors=[
            "Protection criteria (-0.85V CSE or 100 mV shift per NACE SP0169)",
            "Current requirement (depends on coating quality)",
            "Anode type and material (ICCP vs. SACP, Mg vs. Zn vs. Al)",
            "Soil resistivity (affects current distribution)",
            "Coating condition (primary defense, CP is backup)",
            "Survey frequency and compliance (annual CIS per regulations)",
            "Interference sources (AC power lines, foreign CP, rail)"
        ],
        primary_authority=[
            "NACE SP0169 - Control of External Corrosion on Underground or Submerged Metallic Piping Systems",
            "NACE SP0176 - Corrosion Control of Steel Fixed Offshore Platforms with CP",
            "API RP 651 - Cathodic Protection of Aboveground Petroleum Storage Tanks",
            "CFR 49 Part 192.463 - External corrosion control: Cathodic protection (pipeline regulations)"
        ],
        burden_holder="Operator - design, install, maintain CP per NACE SP0169; annual surveys; records retention",
        adversary_position="Regulators (PHMSA, state) require documented surveys, criteria compliance, rectifier maintenance logs",
        counter_arguments=[
            "Surveys show areas below -0.85V CSE (non-compliance)",
            "Rectifier failure periods leave pipeline unprotected",
            "Coating disbondment shields CP current (shielded corrosion)",
            "Over-protection causes hydrogen embrittlement or coating damage",
            "Stray current interference not mitigated (accelerated corrosion)",
            "Anode depletion on SACP systems (end of design life)"
        ],
        resolution_strategy="Regular CIS surveys, rectifier output adjustment, anode replacement on schedule, coating repair, interference mitigation bonds",
        entity_scope="Buried/submerged steel pipelines, tanks, offshore structures per regulatory requirements",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when surveys document criteria compliance per NACE SP0169",
        controlling_precedent="NACE SP0169 and CFR 49 Part 192 define regulatory CP requirements",
        issue_category=IssueCategory.CATHODIC_PROTECTION
    ),

    DoctrineBlock(
        topic="Pipeline Integrity Management (IIM) and Inline Inspection (ILI)",
        keywords=["integrity management", "ili", "smart pig", "mfl", "ultrasonic pig", "anomaly assessment"],
        conclusion_template="Pipeline integrity management per DOT regulations requires ILI pigging (MFL, UT) at intervals based on risk assessment. ILI detects metal loss, cracks, dents, with reporting per API 1163. Anomaly assessment per API 579 FFS determines repair/monitoring decisions.",
        reasoning_framework="""
Regulatory Framework:
49 CFR 192.921 (Gas Pipelines):
- Integrity Management Program (IMP) required for HCAs (High Consequence Areas)
- Baseline assessment within 10 years (complete by 2012-2022 depending on class)
- Reassessment intervals: 7 years (MFL), 10 years (direct assessment)

49 CFR 195.452 (Liquid Pipelines):
- IMP for HCAs (could affect high-population areas, sensitive environments)
- Baseline within 12.5 years (50% by 2007, 50% by 2012)
- Reassessment: 7 years maximum (earlier if integrity threat identified)

ILI Technologies:
1. Magnetic Flux Leakage (MFL):
   - Strong magnets magnetize pipe wall (axial or circumferential)
   - Metal loss (corrosion, pitting) causes flux leakage
   - Sensors detect leakage magnitude and location
   - Accuracy: ±10% wall thickness (80% confidence)
   - Detects: External/internal corrosion, pitting, general metal loss
   - Limitations: Requires magnetic steel (not CRA), minimum flow rate

2. Ultrasonic (UT) ILI:
   - Wheel-mounted UT transducers (hundreds to thousands)
   - Measures remaining wall thickness directly
   - Accuracy: ±0.5 mm (better than MFL for deep anomalies)
   - Detects: Corrosion, cracking (EMAT or phased array), laminations
   - Limitations: Requires liquid (couplant), slower than MFL, high cost

3. Caliper (Geometry):
   - Mechanical fingers or electromagnetic sensors measure ID
   - Detects: Dents, ovality, buckles, wrinkles
   - Used with MFL/UT to distinguish metal loss from deformation

4. Crack Detection:
   - EMAT (Electromagnetic Acoustic Transducer): SCC, fatigue cracks
   - Phased Array UT: High-resolution crack sizing
   - High-resolution MFL: Axial crack-like indications
   - Challenges: Low POD (probability of detection), high false-call rate

ILI Run Execution:
Piggability Assessment:
- Pipeline must accept pig (no restrictions <80% ID)
- Launcher/receiver facilities required
- Valves: Full-port or bypassed during run
- Bends: Minimum radius (3D to 5D depending on pig type)

Run Planning:
- Flow rate: 1-5 m/s (MFL), 0.3-3 m/s (UT) - tool-specific
- Batching: Gas pipelines may require liquid (UT couplant)
- Speed control: Regulate flow to maintain optimal pig velocity
- Tracking: Above-ground markers (AGMs) record pig passage

Data Processing and Reporting:
- Vendor processes raw data (weeks to months)
- Anomaly list: Location (GPS, centerline distance), severity, type
- Severity: % wall loss, depth (mm), length, width
- API 1163 reporting format: Immediate (>80% wall loss), 180-day, 1-year

Anomaly Assessment:
API 579 Fitness-for-Service (FFS):
- Level 1: Screening (conservative allowable depths)
- Level 2: Detailed (refined stress analysis, corrosion growth)
- Level 3: Advanced (FEA, fracture mechanics, remaining life)

RSTRENG (Remaining Strength):
- Empirical model for corroded pipe burst pressure
- Folias factor accounts for stress concentration
- Safe pressure = Burst pressure / Safety factor (1.5-3.0)

Metal Loss Growth Rate:
- Compare successive ILI runs (identify growing anomalies)
- Corrosion rate = (Depth_run2 - Depth_run1) / Time_interval
- Project remaining life: Time to critical depth at growth rate

Repair Decisions:
Immediate Repair (Mandatory):
- >80% wall loss (predicted failure pressure < MAOP)
- Leaks or weeps detected during inspection
- Critical crack indications

Scheduled Repair (180 days - 1 year):
- 50-80% wall loss (per regulatory tables)
- Dents with metal loss or stress concentrations
- Growing anomalies approaching critical depth

Monitor (Next ILI):
- <50% wall loss with low growth rate
- Stable anomalies (no growth over multiple runs)
- Non-critical geometry anomalies

Repair Methods:
- Full-encirclement steel sleeve (Type A or B per ASME B31.4/B31.8)
- Composite wrap (for low-pressure, non-critical)
- Cut-out and replace (severe corrosion, cracking)
- Grinding (external corrosion <50% depth, stress analysis required)

Validation Excavations:
- Dig up sample of ILI-reported anomalies (5-10% per API 1163)
- Direct measurement (UT, pit gauge) vs. ILI call
- Validate ILI accuracy (unity plot: Actual vs. Reported)
- Adjust confidence intervals for future assessments

Data Management:
- GIS integration: Anomaly locations, repair history
- Database: All ILI runs, anomaly growth tracking
- Risk assessment: Combine ILI data with consequence (HCA proximity)
- Predictive analytics: Machine learning for anomaly growth, failure prediction
        """,
        key_factors=[
            "Regulatory IMP requirements (49 CFR 192/195 for HCAs)",
            "ILI technology selection (MFL vs. UT vs. crack detection)",
            "ILI accuracy and confidence intervals (±10% WT for MFL)",
            "Anomaly assessment per API 579 (FFS remaining strength)",
            "Repair criteria (>80% immediate, 50-80% scheduled)",
            "Growth rate determination (successive ILI runs)",
            "Validation excavations (ILI accuracy verification)"
        ],
        primary_authority=[
            "49 CFR Part 192 Subpart O - Gas Pipeline Integrity Management",
            "49 CFR Part 195.452 - Liquid Pipeline Integrity Management",
            "API 1163 - In-Line Inspection Systems Qualification",
            "API 579 - Fitness-for-Service (FFS anomaly assessment)",
            "ASME B31.8S - Gas Pipeline Integrity Management",
            "NACE SP0502 - Pipeline External Corrosion Direct Assessment"
        ],
        burden_holder="Operator - conduct IMP per regulations, perform ILI at required intervals, repair per criteria, maintain records",
        adversary_position="PHMSA enforcement for IMP non-compliance, inadequate reassessment intervals, failure to repair per criteria",
        counter_arguments=[
            "ILI missed critical anomalies (tool tolerance, POD limitations)",
            "Anomaly growth rate underestimated (accelerated corrosion)",
            "Repairs not prioritized correctly (consequence analysis flawed)",
            "Validation digs show ILI inaccuracy (reporting vs. actual)",
            "Delayed repairs beyond regulatory timeframes",
            "Unpiggable segments not assessed (no ILI alternative applied)"
        ],
        resolution_strategy="Multi-run ILI for growth tracking, validation digs per API 1163, conservative FFS assessment, timely repairs, direct assessment for unpiggable",
        entity_scope="Regulated gas and liquid pipelines in HCAs per DOT integrity management requirements",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when ILI + validation + FFS + repairs per API/DOT standards",
        controlling_precedent="49 CFR 192/195 and API 1163/579 define regulatory and industry ILI/FFS standards",
        issue_category=IssueCategory.INTEGRITY_MANAGEMENT
    ),

    DoctrineBlock(
        topic="Erosion-Corrosion in High-Velocity Systems",
        keywords=["erosion corrosion", "velocity limit", "sand production", "flow-induced localized corrosion", "api 14e"],
        conclusion_template="Erosion-corrosion combines mechanical erosion with electrochemical corrosion at high velocities (>15 ft/s liquid, >60 ft/s gas). Sand production accelerates via abrasion. API 14E velocity limits prevent erosion. Mitigation: velocity reduction, erosion-resistant coatings, materials (tungsten carbide, ceramics).",
        reasoning_framework="""
Erosion-Corrosion Mechanism:
1. Protective Film Removal:
   - Flow-induced shear stress disrupts passive oxide or inhibitor film
   - Bare metal exposed to corrosive environment (instantaneous attack)
   - Film attempts to re-form, but continuous erosion prevents protection

2. Mechanical Abrasion:
   - Sand particles (quartz, feldspar) impact surface
   - Hardness: Sand (Mohs 7) >> Steel (Mohs 4-5)
   - Kinetic energy transfer: KE = 0.5 × m × v²
   - Higher velocity = exponential increase in erosion rate

3. Synergistic Effect:
   - Erosion + corrosion > sum of individual mechanisms
   - Erosion exposes fresh metal (high corrosion rate)
   - Corrosion weakens surface (easier erosion)

API 14E Velocity Limits:
Empirical C-Factor Equation:
  Ve = C / √ρ

  Ve = erosion velocity (ft/s)
  C = empirical constant (dimensionless)
  ρ = fluid density (lb/ft³)

C-Factor Guidelines:
- Continuous service: C = 100 (conservative)
- Intermittent service: C = 125 (moderate risk acceptance)
- Non-corrosive (sweet, inhibited): C = 150-200
- Corrosive (sour, no inhibitor): C = 75-100
- Solids-free assumed (sand increases erosion)

Example Calculations:
Liquid (water, ρ = 62.4 lb/ft³):
  Ve = 100 / √62.4 = 12.7 ft/s (continuous)

Gas (0.6 SG, 1000 psia, 100 degF, ρ ≈ 4 lb/ft³):
  Ve = 100 / √4 = 50 ft/s (continuous)

Two-Phase Flow:
- Use mixture density (weighted by volume fraction)
- ρmix = ρL × HL + ρG × (1 - HL)
- HL = liquid holdup (volume fraction liquid in pipe)

Sand Production Effects:
Sand Concentration Impact:
- 0.1% sand (by weight): 2-5x erosion rate increase
- 1% sand: 10-50x erosion rate increase
- Particle size: Larger particles (>100 microns) more erosive
- Particle shape: Angular (crushed) more erosive than rounded

Erosion Rate Models:
DNV RP O501 (Det Norske Veritas):
- Accounts for particle size, concentration, impact angle, material
- E = K × V^n × f(θ) × C × A
  E = erosion rate (mm/year)
  V = particle velocity (m/s)
  n = velocity exponent (2.6 for steel)
  f(θ) = impact angle function (max at 20-30 deg for ductile)
  C = particle concentration (kg/m³)
  A = particle shape factor

Critical Locations:
- Elbows: High-velocity impingement on outer radius (90 deg bends)
- Tees: Direct impingment on branch walls (flow splitting)
- Chokes: Velocity increase, turbulence, cavitation (liquid)
- Reducers: Velocity increase, flow separation zones

Erosion Patterns:
- Thinning: Directional (flow-facing surface, elbow outer radius)
- Grooving: Parallel to flow direction (sand cutting)
- Orange-peel: Liquid droplet impingement (wet gas systems)
- Horseshoe: Localized attack at stagnation points

Mitigation Strategies:
Design Solutions:
- Increase pipe diameter (reduce velocity below API 14E limit)
- Long-radius elbows (5D vs. 3D) - reduce impact angle, spread erosion
- Tee with erosion pad (weld overlay on impingement zone)
- Flow deflectors (dead tees, vortex finders in separators)

Material Solutions:
- Erosion-resistant overlays:
  * Tungsten carbide (extreme hardness, 10x erosion resistance)
  * Chromium carbide (arc spray or weld overlay)
  * Ceramics (Al2O3, ZrO2 tiles) for chokes, elbows
- Duplex stainless: Better erosion resistance than CS (strain hardening)

Operational Solutions:
- Sand control: Gravel packing, frac-pack, expandable sand screens
- Sand monitoring: Acoustic sensors, erosion probes, UT thickness trending
- Chemical sand consolidation (downhole resin injection)
- Reduced production rate (lower velocity, extend asset life)

Inspection and Monitoring:
- UT grid mapping: High-frequency inspections (annual in high-erosion areas)
- Radiography: Elbow profiles, detect thinning patterns
- Erosion probes: Flush-mounted elements, track metal loss rate
- Visual inspection (when accessible): Surface texture, grooving
        """,
        key_factors=[
            "Fluid velocity (API 14E C-factor limits)",
            "Sand production rate and particle size",
            "Fluid density (affects velocity limit calculation)",
            "Flow regime (turbulent vs. laminar, multiphase)",
            "Critical geometry (elbows, tees, chokes)",
            "Material erosion resistance (CS vs. overlays vs. CRA)",
            "Corrosion synergy (erosion + electrochemical attack)"
        ],
        primary_authority=[
            "API RP 14E - Recommended Practice for Design and Installation of Offshore Production Platform Piping Systems",
            "DNV RP O501 - Erosive Wear in Piping Systems",
            "NACE SP0110 - Wet Gas Internal Corrosion Direct Assessment",
            "ISO 13703 - Design and Installation of Piping Systems on Offshore Production Platforms"
        ],
        burden_holder="Operator - design to API 14E velocity limits, monitor erosion, implement mitigation in high-velocity zones",
        adversary_position="Regulators may require velocity calculations, erosion monitoring data, proof of API 14E compliance",
        counter_arguments=[
            "Actual velocities exceed API 14E limits (high production rates)",
            "Sand production uncontrolled (erosion accelerates beyond predictions)",
            "Erosion monitoring inadequate (missed critical thinning)",
            "Elbow/tee failures occurred despite API 14E compliance claims",
            "Two-phase flow density calculation incorrect (velocity underestimated)",
            "Material erosion resistance overestimated (overlay spalled off)"
        ],
        resolution_strategy="Conservative C-factors (75-100 for sour/sand), frequent UT inspections, erosion-resistant materials in critical areas, sand control",
        entity_scope="High-velocity production systems, sand-producing wells, multiphase flowlines and separators",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence in API 14E velocity limits (empirical, not mechanistic), high confidence with erosion monitoring",
        controlling_precedent="API RP 14E is industry-accepted erosion velocity guideline",
        issue_category=IssueCategory.EROSION_CORROSION
    ),

    DoctrineBlock(
        topic="Galvanic Corrosion in Mixed-Metallurgy Systems",
        keywords=["galvanic corrosion", "dissimilar metals", "galvanic series", "bimetallic couple", "insulating flange"],
        conclusion_template="Galvanic corrosion occurs when dissimilar metals are electrically connected in conductive electrolyte. Noble metal (cathode) protected, active metal (anode) corrodes. Severity depends on potential difference, area ratio (small anode/large cathode worst case), and electrolyte conductivity. Mitigation: insulating joints, coatings, similar metallurgy.",
        reasoning_framework="""
Galvanic Series in Seawater (Noble to Active):
Noble (Cathodic - Protected):
- Graphite, platinum
- Titanium, Hastelloy C
- 316 Stainless Steel (passive)
- Monel (Ni-Cu alloy)
- Nickel (passive)
- Inconel (passive)
- 13Cr Stainless (passive)
- Duplex stainless (passive)
- Copper, bronze, brass
- Carbon steel (passive in alkaline)

Active (Anodic - Corrodes):
- Carbon steel (active in acid/neutral)
- Cast iron
- Aluminum alloys
- Zinc
- Magnesium

Galvanic Couple Formation:
- Two dissimilar metals in electrical contact (direct or via conductive path)
- Electrolyte bridges the metals (seawater, brine, moist soil)
- Potential difference drives electron flow (active → noble)
- Anodic metal oxidizes (corrodes), cathodic metal protected

Driving Voltage:
- Potential difference (ΔE) = Ecathode - Eanode
- Example: 316 SS (+0.1V SCE) coupled to carbon steel (-0.6V SCE)
- ΔE = +0.1 - (-0.6) = 0.7V (significant driving force)

Area Ratio Effect (Critical):
Unfavorable Ratio (Small Anode / Large Cathode):
- Small carbon steel fitting + large stainless vessel
- High current density on small anode (rapid corrosion)
- Catastrophic failure of small component (bolt, flange)

Favorable Ratio (Large Anode / Small Cathode):
- Large carbon steel pipe + small stainless valve
- Low current density on large anode (minimal corrosion increase)
- Acceptable in many cases

Current Density Calculation:
  icorr (anode) = Itotal / Aanode

  Itotal = galvanic current (amperes) - from potential and resistance
  Aanode = anode surface area (cm²)

Electrolyte Conductivity:
- High conductivity (seawater, brine): Long-range galvanic effect
- Low conductivity (fresh water, dry soil): Short-range effect
- Distance: Galvanic effect decays with distance from junction
- Rule of thumb: Significant within 10-20 diameters in seawater

Common Galvanic Couples in Oil & Gas:
1. Carbon Steel + Stainless Fittings:
   - Stainless valve/flange on carbon steel pipe
   - Small CS bolt in stainless flange (bolt corrodes rapidly)

2. Carbon Steel + Copper Alloys:
   - Brass valve on steel pipe
   - Bronze pump on steel suction line
   - Admiralty brass condenser tubes + CS waterbox

3. Aluminum + Steel:
   - Aluminum anodes on steel structures (intentional - CP)
   - Aluminum equipment on steel support (unintentional - accelerates Al corrosion)

4. Carbon Steel + CRA Tubing:
   - 13Cr tubing in CS wellhead (CS corrodes at connection)
   - Duplex flowline connected to CS riser (insulating flange required)

5. Active vs. Passive Stainless:
   - Creviced stainless (active, -0.4V) vs. passive stainless (+0.1V)
   - Stainless in low-oxygen (active) coupled to aerated stainless (passive)

Mitigation Strategies:
Insulating Joints:
- Monolithic insulating flange (fiber gasket, coated bolts, sleeves)
- Full electrical isolation (mega-ohm resistance)
- API 6FB - Fire-tested insulating flanges for pipeline isolation

Coatings:
- Coat the cathode (reduce effective cathode area)
- Coating on anode less effective (defects become intense anodes)
- Dual-coat systems (both metals) for critical applications

Material Selection:
- Specify compatible metallurgy (minimize ΔE in galvanic series)
- Transition spools: CS → 13Cr → 22Cr (step-wise potential change)
- Avoid small active metal in large noble metal assembly

Design Practices:
- Avoid crevices at bimetallic junction (trap electrolyte)
- Drain water from low points (eliminate electrolyte)
- Seal joints with non-conductive sealants
- Cathodic protection can mitigate (polarize both metals to same potential)

Inspection and Monitoring:
- Potential surveys at bimetallic junctions (verify isolation)
- Visual inspection for preferential corrosion at junctions
- UT thickness monitoring of active metal component
- Leak testing (threaded connections, flanges)

Environmental Factors:
Temperature:
- Elevated temperature increases corrosion kinetics (galvanic current)
- Thermal cycling disrupts coatings, insulation

Oxygen:
- Oxygen depolarizes cathode (increases galvanic current)
- Deaeration reduces galvanic corrosion rate

pH:
- Acidic: Passive films break down (more active potential)
- Alkaline: Passive films stabilize (more noble potential)
        """,
        key_factors=[
            "Potential difference in galvanic series (ΔE driving voltage)",
            "Anode-to-cathode area ratio (small anode/large cathode critical)",
            "Electrolyte conductivity (seawater vs. fresh water range)",
            "Distance from junction (galvanic effect decay)",
            "Environmental factors (oxygen, temperature, pH)",
            "Insulating joint effectiveness (electrical isolation)",
            "Coating integrity on cathode or anode"
        ],
        primary_authority=[
            "ASTM G82 - Standard Guide for Development and Use of a Galvanic Series",
            "NACE SP0286 - Electrical Isolation of Cathodically Protected Pipelines",
            "API 6FB - Specification for Fire Test for Valves (includes insulating flanges)",
            "MIL-STD-889 - Dissimilar Metals (Military Standard on galvanic compatibility)"
        ],
        burden_holder="Operator - identify galvanic couples in design, install insulating joints, monitor corrosion at junctions",
        adversary_position="Failure analysis may attribute corrosion to galvanic coupling oversight in design",
        counter_arguments=[
            "Insulating flange failed (electrical short via coating breakdown)",
            "Area ratio unfavorable (small CS component corroded rapidly)",
            "Design did not account for bimetallic junction (no isolation)",
            "Coating on cathode degraded (restored full galvanic effect)",
            "CP ineffective at bimetallic junction (shielding, attenuation)",
            "Dissimilar metal use was unavoidable (material specification conflict)"
        ],
        resolution_strategy="Conservative material selection (avoid dissimilar metals), insulating flanges per API 6FB, coating noble metal, CP coverage verification",
        entity_scope="All systems with mixed metallurgy (CS/SS, CS/CRA, steel/copper alloys) in conductive environments",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when galvanic series ΔE and area ratio considered with proper mitigation",
        controlling_precedent="ASTM G82 galvanic series and NACE SP0286 isolation practices are industry-accepted standards",
        issue_category=IssueCategory.GALVANIC_CORROSION
    ),

    DoctrineBlock(
        topic="Pitting Corrosion and Pitting Resistance Equivalent (PRE)",
        keywords=["pitting", "pre", "pitting resistance", "chloride pitting", "astm g48"],
        conclusion_template="Pitting is localized corrosion forming cavities due to passive film breakdown, often chloride-induced. Pitting Resistance Equivalent (PRE = %Cr + 3.3×%Mo + 16×%N) predicts stainless steel resistance. PRE >40 (super duplex, 6Mo SS) for high-chloride, high-temp service. ASTM G48 ferric chloride test validates PRE.",
        reasoning_framework="""
Pitting Mechanism:
1. Passive Film Breakdown:
   - Stainless steel protected by chromium oxide passive film (Cr2O3)
   - Chloride ions (Cl⁻) penetrate film at defects (inclusions, scratches)
   - Localized depassivation creates anodic site (pit initiation)

2. Autocatalytic Propagation:
   - Metal dissolution in pit: M → M^n+ + ne⁻
   - Cation hydrolysis: M^n+ + H2O → M(OH)^(n-1)+ + H+ (acidification)
   - Chloride migration into pit (electroneutrality)
   - Low pH (3-4) in pit, high chloride (10x bulk) - aggressive environment
   - Pit grows deeper (autocatalytic, self-sustaining)

3. Differential Aeration Cell:
   - Pit interior: Oxygen-depleted, anodic (dissolution)
   - Surrounding surface: Oxygen-rich, cathodic (protected)
   - O2 + 2H2O + 4e⁻ → 4OH⁻ (cathode reaction on passive surface)

Pitting Resistance Equivalent (PRE):
Empirical Formula:
  PRE = %Cr + 3.3×%Mo + 16×%N

  %Cr, %Mo, %N = weight percent in alloy composition

Elemental Contributions:
- Chromium: Passive film formation (Cr2O3), stabilizes film
- Molybdenum: Enhances repassivation, prevents pit initiation
- Nitrogen: Strengthens passive film, increases critical pitting temperature

PRE Thresholds:
- PRE <30: 304/316 SS - low chloride, <40 degC, limited service
- PRE 30-35: 317L, 6Mo austenitic SS - moderate chloride, to 60 degC
- PRE 35-40: 22Cr duplex (2205) - high chloride (200K ppm), to 80 degC
- PRE >40: 25Cr super duplex (2507), 6Mo SS (254SMO) - extreme service
- PRE >50: Nickel alloys (Inconel, Hastelloy) - highest resistance

Critical Pitting Temperature (CPT):
- Temperature above which pitting initiates in ferric chloride solution
- ASTM G48 test: 6% FeCl3, 24-72 hours, vary temperature
- CPT correlated with PRE (higher PRE → higher CPT)
- Example: 2205 duplex CPT ≈ 35 degC, 2507 super duplex CPT ≈ 50 degC

Environmental Factors:
Chloride Concentration:
- Seawater (19,000 ppm Cl): Requires PRE >33 (duplex minimum)
- Brine (100,000-250,000 ppm Cl): Requires PRE >40 (super duplex or 6Mo)
- Saturation (>300,000 ppm): Nickel alloys (PRE >50)

Temperature:
- Pitting rate exponential with temperature (10 degC rule: 2x rate increase)
- CPT is threshold - pitting initiates rapidly above CPT
- Operational temperature <CPT - 20 degC safety margin

pH:
- Acidic (pH <4): Passive film unstable, general corrosion dominates
- Neutral (pH 5-9): Pitting is primary concern
- Alkaline (pH >10): Passive film stable, pitting suppressed

Oxygen:
- Oxygen required for cathode reaction (supports pitting current)
- Deaeration reduces pitting (but may not eliminate in high Cl⁻)

Stagnation:
- Stagnant zones (dead legs, under deposits) concentrate chloride
- Flow: Dilutes pit chemistry, can suppress pitting (if not erosive)

ASTM G48 Pitting Test:
Methods A, B, C, D, E, F:
- Method A: 6% FeCl3, 50 degC, 72 hours (ferric chloride test)
- Method E: 6% FeCl3, 22 degC, 24 hours (critical pitting temp determination)
- Weight loss measured, pitting depth, visual pitting severity

Acceptance Criteria:
- Weight loss <10 mg/cm² (mild pitting)
- No pitting visible at 20x magnification (stringent)
- Crevice-free specimen (distinguish pitting from crevice corrosion)

Material Selection Based on PRE:
Application Scenarios:
1. Sweet production water (CO2, low Cl):
   - 13Cr (PRE ≈ 13) with inhibitor, or
   - 22Cr duplex (PRE ≈ 35) inhibitor-free

2. Seawater injection (19K ppm Cl, 60 degC):
   - 22Cr duplex (PRE ≈ 35) minimum, or
   - 25Cr super duplex (PRE ≈ 42) for margin

3. High-salinity brine (200K ppm Cl, 90 degC):
   - 25Cr super duplex (PRE ≈ 42), or
   - 6Mo stainless (254SMO, PRE ≈ 43)

4. Extreme chloride + H2S (>150K ppm Cl, >100 psia H2S):
   - Inconel 625 (PRE ≈ 52), or
   - Hastelloy C-276 (PRE ≈ 70)

Inspection and Detection:
- Visual: Identify pits during turnaround, NDT access
- Pit depth gauge: Measure maximum pit depth
- Pitting factor: Max pit depth / Average wall loss (>3 = severe pitting)
- Metallography: Cross-section pits, measure geometry (aspect ratio)
- Electrochemical: Cyclic polarization (pitting potential Epit measurement)

Mitigation:
- Material upgrade: Increase PRE to exceed environmental severity
- Chloride reduction: Dilution, desalination, membrane treatment
- Temperature control: Keep below CPT - 20 degC margin
- Cathodic protection: Polarize below pitting potential (Epit)
- Inhibitors: Molybdate, nitrite stabilize passive film (limited effectiveness)
        """,
        key_factors=[
            "PRE value (%Cr + 3.3×%Mo + 16×%N) vs. environmental severity",
            "Chloride concentration (seawater to saturation brine)",
            "Temperature relative to critical pitting temperature (CPT)",
            "pH and oxygen content (affect passive film stability)",
            "Stagnation vs. flow conditions (chloride concentration)",
            "ASTM G48 test validation of pitting resistance",
            "Pitting factor (max depth / avg. loss) from inspection"
        ],
        primary_authority=[
            "ASTM G48 - Standard Test Methods for Pitting and Crevice Corrosion Resistance of Stainless Steels",
            "NACE MR0175/ISO 15156 Part 3 - CRA Limits (includes PRE considerations)",
            "ASTM A923 - Detecting Detrimental Intermetallic Phases in Duplex Stainless Steels",
            "ISO 17945 - Corrosion of Metals and Alloys - Determination of Critical Pitting Temperature"
        ],
        burden_holder="Operator - select material with adequate PRE for chloride/temperature conditions, validate with ASTM G48",
        adversary_position="Regulators or failure analysis may challenge material selection if pitting occurred (PRE inadequate)",
        counter_arguments=[
            "PRE calculation doesn't account for weld HAZ (local PRE reduction)",
            "ASTM G48 test conditions not representative of field (temperature, chloride)",
            "Pitting occurred despite adequate PRE (localized chloride concentration, deposits)",
            "Material certified PRE not verified (heat-specific chemistry variation)",
            "Operational upsets exceeded design CPT",
            "Crevice corrosion misidentified as pitting (different mechanism)"
        ],
        resolution_strategy="Conservative PRE margin (5-10 points above minimum), ASTM G48 testing of actual heat, weld procedure qualification, deposit control",
        entity_scope="Stainless steel and CRA equipment in chloride-containing environments (seawater, brine, sour production)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when PRE >10 points above environmental threshold with ASTM G48 validation",
        controlling_precedent="ASTM G48 and PRE calculation are universally accepted stainless steel pitting resistance metrics",
        issue_category=IssueCategory.PITTING_CORROSION
    ),
]

# ═══════════════════════════════════════════════════════════════════════════
# ENGINE CORE LOGIC
# ═══════════════════════════════════════════════════════════════════════════

class PROD09Engine:
    def __init__(self):
        self.start_time = time.time()
        self.total_queries = 0
        self.total_latency = 0.0
        self.cache_hits = 0
        self.cache_misses = 0

        self.doctrine_index = self._build_doctrine_index()
        self.issue_category_map = self._build_category_map()

        logger.info(f"{ENGINE_NAME} v{ENGINE_VERSION} initialized with {len(DOCTRINE_CACHE)} doctrines")

    def _build_doctrine_index(self) -> Dict[str, List[int]]:
        """Build keyword -> doctrine index for fast retrieval."""
        index = defaultdict(list)
        for i, doctrine in enumerate(DOCTRINE_CACHE):
            for keyword in doctrine.keywords:
                index[keyword.lower()].append(i)
            for word in doctrine.topic.lower().split():
                if len(word) > 3:
                    index[word].append(i)
        return dict(index)

    def _build_category_map(self) -> Dict[IssueCategory, List[int]]:
        """Build issue category -> doctrine index."""
        cat_map = defaultdict(list)
        for i, doctrine in enumerate(DOCTRINE_CACHE):
            cat_map[doctrine.issue_category].append(i)
        return dict(cat_map)

    def semantic_normalization(self, query: str) -> str:
        """Normalize corrosion domain terminology."""
        normalizations = {
            r'\bco2\b': 'CO2',
            r'\bh2s\b': 'H2S',
            r'\bssc\b': 'sulfide stress cracking',
            r'\bmic\b': 'microbiologically influenced corrosion',
            r'\bsrb\b': 'sulfate reducing bacteria',
            r'\ber probe\b': 'electrical resistance probe',
            r'\blpr\b': 'linear polarization resistance',
            r'\butm?\b': 'ultrasonic thickness',
            r'\bili\b': 'inline inspection',
            r'\bmfl\b': 'magnetic flux leakage',
            r'\bcra\b': 'corrosion resistant alloy',
            r'\bpre\b': 'pitting resistance equivalent',
            r'\bcp\b': 'cathodic protection',
            r'\biccp\b': 'impressed current cathodic protection',
            r'\bsacp\b': 'sacrificial anode cathodic protection',
            r'\bnace\b': 'NACE',
            r'\bapi\b': 'API',
            r'\bdewaard\b': 'de Waard',
            r'\b13cr\b': '13Cr',
            r'\b22cr\b': '22Cr duplex',
            r'\b25cr\b': '25Cr super duplex',
            r'\binconel\b': 'Inconel',
            r'\bffs\b': 'fitness-for-service',
            r'\bhaz\b': 'heat affected zone',
            r'\bpwht\b': 'post weld heat treatment',
        }

        import re
        normalized = query
        for pattern, replacement in normalizations.items():
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
        return normalized

    def three_layer_response(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> Tuple[str, List[DoctrineBlock], float]:
        """
        Layer 1: Doctrine cache (0-200ms)
        Layer 2: Semantic retrieval (200-2000ms)
        Layer 3: Deep analysis (2000-10000ms)
        """
        start = time.time()

        # Layer 1: Doctrine Cache Lookup
        normalized_query = self.semantic_normalization(query)
        query_tokens = set(normalized_query.lower().split())

        triggered_doctrines = []
        doctrine_scores = []

        for i, doctrine in enumerate(DOCTRINE_CACHE):
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in normalized_query.lower())
            topic_overlap = len(set(doctrine.topic.lower().split()) & query_tokens)
            score = keyword_matches * 3 + topic_overlap

            if score > 0:
                doctrine_scores.append((score, i))

        # Sort by relevance score
        doctrine_scores.sort(reverse=True, key=lambda x: x[0])

        # Take top 5 doctrines
        for score, idx in doctrine_scores[:5]:
            triggered_doctrines.append(DOCTRINE_CACHE[idx])
            DOCTRINE_CACHE[idx].triggered_count += 1

        latency = (time.time() - start) * 1000

        if triggered_doctrines:
            self.cache_hits += 1
            logger.info(f"Cache hit: {len(triggered_doctrines)} doctrines, {latency:.1f}ms")
        else:
            self.cache_misses += 1
            logger.warning(f"Cache miss: No doctrines matched query")

        return normalized_query, triggered_doctrines, latency

    def authority_hardening(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract and weight primary authorities."""
        authorities = []
        for doctrine in doctrines:
            authorities.extend(doctrine.primary_authority)

        # Count and rank
        auth_counts = Counter(authorities)
        return [auth for auth, count in auth_counts.most_common(10)]

    def confidence_stratification(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Determine overall confidence based on triggered doctrines."""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        confidence_scores = {
            ConfidenceLevel.DEFENSIBLE: 4,
            ConfidenceLevel.AGGRESSIVE: 3,
            ConfidenceLevel.DISCLOSURE: 2,
            ConfidenceLevel.HIGH_RISK: 1
        }

        avg_score = sum(confidence_scores[d.confidence] for d in doctrines) / len(doctrines)

        if avg_score >= 3.5:
            return ConfidenceLevel.DEFENSIBLE
        elif avg_score >= 2.5:
            return ConfidenceLevel.AGGRESSIVE
        elif avg_score >= 1.5:
            return ConfidenceLevel.DISCLOSURE
        else:
            return ConfidenceLevel.HIGH_RISK

    def multi_doctrine_decomposition(self, doctrines: List[DoctrineBlock]) -> Dict[IssueCategory, int]:
        """Categorize issues across multiple doctrines."""
        categories = defaultdict(int)
        for doctrine in doctrines:
            categories[doctrine.issue_category] += 1
        return dict(categories)

    def generate_response(self, query: str, mode: ResponseMode, zone: AnalysisZone,
                         normalized_query: str, doctrines: List[DoctrineBlock]) -> str:
        """Generate response based on mode and triggered doctrines."""

        if not doctrines:
            return (
                f"No specific corrosion monitoring doctrines matched the query '{query}'. "
                f"This engine covers: CO2/H2S corrosion mechanisms, MIC, monitoring techniques "
                f"(coupons, ER probes, LPR, UT, ILI pigging), chemical inhibitors, CRA material selection, "
                f"cathodic protection, integrity management, erosion-corrosion, galvanic corrosion, and pitting. "
                f"Please refine your query with relevant keywords."
            )

        if mode == ResponseMode.FAST:
            # Concise, executive summary
            primary = doctrines[0]
            return (
                f"{primary.conclusion_template}\n\n"
                f"Key Factors: {', '.join(primary.key_factors[:3])}.\n\n"
                f"Authority: {primary.primary_authority[0]}"
            )

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready, detailed
            response_parts = []
            response_parts.append(f"=== CORROSION ANALYSIS: {normalized_query.upper()} ===\n")

            for i, doctrine in enumerate(doctrines, 1):
                response_parts.append(f"\n{i}. {doctrine.topic}")
                response_parts.append(f"\nConclusion: {doctrine.conclusion_template}")
                response_parts.append(f"\nKey Factors:")
                for factor in doctrine.key_factors:
                    response_parts.append(f"  - {factor}")
                response_parts.append(f"\nPrimary Authority:")
                for auth in doctrine.primary_authority:
                    response_parts.append(f"  - {auth}")
                response_parts.append(f"\nConfidence: {doctrine.confidence.value}")
                response_parts.append(f"Issue Category: {doctrine.issue_category.value}")

            return "\n".join(response_parts)

        else:  # MEMO mode
            # Full documentation
            response_parts = []
            response_parts.append(f"TECHNICAL MEMORANDUM")
            response_parts.append(f"Subject: {normalized_query}")
            response_parts.append(f"Analysis Zone: {zone.value}")
            response_parts.append(f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
            response_parts.append(f"\n{'='*80}\n")

            for i, doctrine in enumerate(doctrines, 1):
                response_parts.append(f"\nSECTION {i}: {doctrine.topic.upper()}")
                response_parts.append(f"\n{doctrine.conclusion_template}")

                response_parts.append(f"\n\nTECHNICAL REASONING:")
                response_parts.append(doctrine.reasoning_framework)

                response_parts.append(f"\n\nKEY FACTORS:")
                for j, factor in enumerate(doctrine.key_factors, 1):
                    response_parts.append(f"  {j}. {factor}")

                response_parts.append(f"\n\nPRIMARY AUTHORITY:")
                for auth in doctrine.primary_authority:
                    response_parts.append(f"  - {auth}")

                response_parts.append(f"\n\nBURDEN OF PROOF: {doctrine.burden_holder}")
                response_parts.append(f"\nADVERSARY POSITION: {doctrine.adversary_position}")

                response_parts.append(f"\n\nCOUNTER-ARGUMENTS:")
                for arg in doctrine.counter_arguments:
                    response_parts.append(f"  - {arg}")

                response_parts.append(f"\n\nRESOLUTION STRATEGY: {doctrine.resolution_strategy}")
                response_parts.append(f"\nCONFIDENCE: {doctrine.confidence.value} - {doctrine.confidence_stratification}")
                response_parts.append(f"\n{'-'*80}")

            return "\n".join(response_parts)

    def determinism_hash(self, query: str, response: str, doctrines: List[DoctrineBlock]) -> str:
        """Generate SHA-256 hash for reproducibility verification."""
        doctrine_ids = "_".join(d.topic for d in doctrines)
        hash_input = f"{query}|{doctrine_ids}|{response[:200]}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    def telemetry_collect(self, latency_ms: float, doctrines_count: int,
                         query_length: int) -> Dict[str, Any]:
        """Collect performance and usage telemetry."""
        return {
            "latency_ms": round(latency_ms, 2),
            "doctrines_triggered": doctrines_count,
            "query_length": query_length,
            "cache_hit": doctrines_count > 0,
            "total_queries": self.total_queries,
            "avg_latency_ms": round(self.total_latency / max(self.total_queries, 1), 2),
            "cache_hit_rate": round(self.cache_hits / max(self.total_queries, 1), 3)
        }

    def audit_trail_log(self, query: str, response: str, mode: ResponseMode,
                       zone: AnalysisZone, doctrines: List[DoctrineBlock],
                       confidence: ConfidenceLevel, determinism_hash: str):
        """Append-only audit trail in JSONL format."""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "response_length": len(response),
            "mode": mode.value,
            "zone": zone.value,
            "doctrines_triggered": [d.topic for d in doctrines],
            "issue_categories": list(set(d.issue_category.value for d in doctrines)),
            "confidence": confidence.value,
            "determinism_hash": determinism_hash,
            "engine": ENGINE_NAME,
            "version": ENGINE_VERSION
        }

        with open(AUDIT_LOG_PATH, 'a') as f:
            f.write(json.dumps(audit_entry) + "\n")

    def query(self, request: QueryRequest) -> QueryResponse:
        """Main query processing with full TIE-20 pipeline."""
        start_time = time.time()
        self.total_queries += 1

        # Three-layer response
        normalized_query, doctrines, cache_latency = self.three_layer_response(
            request.query, request.mode, request.zone
        )

        # Multi-doctrine decomposition
        issue_categories = self.multi_doctrine_decomposition(doctrines)

        # Authority hardening
        authorities = self.authority_hardening(doctrines)

        # Confidence stratification
        confidence = self.confidence_stratification(doctrines)

        # Generate response
        answer = self.generate_response(
            request.query, request.mode, request.zone, normalized_query, doctrines
        )

        # Determinism hash
        det_hash = self.determinism_hash(request.query, answer, doctrines)

        # Total latency
        total_latency = (time.time() - start_time) * 1000
        self.total_latency += total_latency

        # Telemetry
        telemetry = None
        if request.include_telemetry:
            telemetry = self.telemetry_collect(total_latency, len(doctrines), len(request.query))

        # Audit trail
        self.audit_trail_log(
            request.query, answer, request.mode, request.zone, doctrines, confidence, det_hash
        )

        # Reasoning chain for DEFENSE/MEMO modes
        reasoning_chain = None
        if request.mode in [ResponseMode.DEFENSE, ResponseMode.MEMO]:
            reasoning_chain = [
                f"Normalized query: {normalized_query}",
                f"Triggered {len(doctrines)} doctrines via keyword matching",
                f"Issue categories: {list(issue_categories.keys())}",
                f"Authority sources: {len(authorities)} unique references",
                f"Confidence level: {confidence.value}"
            ]

        logger.info(
            f"Query processed: {len(doctrines)} doctrines, {total_latency:.1f}ms, "
            f"confidence={confidence.value}, mode={request.mode.value}"
        )

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            mode=request.mode,
            zone=request.zone,
            triggered_doctrines=[d.topic for d in doctrines],
            issue_categories=list(issue_categories.keys()),
            reasoning_chain=reasoning_chain,
            authorities_cited=authorities,
            determinism_hash=det_hash,
            telemetry=telemetry,
            timestamp=datetime.utcnow().isoformat()
        )

    def health(self) -> HealthResponse:
        """Comprehensive health check endpoint."""
        uptime = time.time() - self.start_time
        avg_latency = self.total_latency / max(self.total_queries, 1)
        cache_hit_rate = self.cache_hits / max(self.total_queries, 1)

        return HealthResponse(
            status="healthy",
            engine=ENGINE_NAME,
            version=ENGINE_VERSION,
            port=ENGINE_PORT,
            doctrine_count=len(DOCTRINE_CACHE),
            total_queries=self.total_queries,
            avg_latency_ms=round(avg_latency, 2),
            cache_hit_rate=round(cache_hit_rate, 3),
            uptime_seconds=round(uptime, 1)
        )

    def coverage_map(self) -> Dict[str, Any]:
        """Track triggered vs. missed doctrines (epistemic gap detection)."""
        triggered = [d for d in DOCTRINE_CACHE if d.triggered_count > 0]
        missed = [d for d in DOCTRINE_CACHE if d.triggered_count == 0]

        category_coverage = defaultdict(lambda: {"triggered": 0, "total": 0})
        for doctrine in DOCTRINE_CACHE:
            cat = doctrine.issue_category
            category_coverage[cat]["total"] += 1
            if doctrine.triggered_count > 0:
                category_coverage[cat]["triggered"] += 1

        return {
            "total_doctrines": len(DOCTRINE_CACHE),
            "triggered_doctrines": len(triggered),
            "missed_doctrines": len(missed),
            "coverage_rate": round(len(triggered) / len(DOCTRINE_CACHE), 3),
            "most_triggered": sorted(
                [(d.topic, d.triggered_count) for d in triggered],
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "category_coverage": {
                cat.value: {
                    "triggered": stats["triggered"],
                    "total": stats["total"],
                    "rate": round(stats["triggered"] / stats["total"], 3)
                }
                for cat, stats in category_coverage.items()
            }
        }

    def drift_watcher(self) -> Dict[str, Any]:
        """Detect doctrine drift (usage pattern changes over time)."""
        # Simplified drift detection - compare recent vs. historical trigger rates
        recent_threshold = max(1, self.total_queries // 10)

        drift_candidates = []
        for doctrine in DOCTRINE_CACHE:
            if doctrine.triggered_count > 0:
                trigger_rate = doctrine.triggered_count / max(self.total_queries, 1)
                if trigger_rate > 0.1:  # High-frequency doctrine
                    drift_candidates.append({
                        "topic": doctrine.topic,
                        "trigger_rate": round(trigger_rate, 3),
                        "absolute_count": doctrine.triggered_count,
                        "category": doctrine.issue_category.value
                    })

        return {
            "total_queries_analyzed": self.total_queries,
            "high_frequency_doctrines": sorted(
                drift_candidates,
                key=lambda x: x["trigger_rate"],
                reverse=True
            ),
            "drift_detection": "Monitoring trigger rate changes over time (placeholder for time-series analysis)"
        }

# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

APP = FastAPI(
    title="PROD09 Corrosion Monitoring Intelligence Engine",
    description="TIE-grade corrosion mechanisms, monitoring, treatment, and integrity management",
    version=ENGINE_VERSION
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = PROD09Engine()

@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with full TIE-20 analysis pipeline."""
    try:
        return engine.query(request)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check with performance metrics."""
    return engine.health()

@APP.get("/coverage")
async def coverage_endpoint():
    """Doctrine coverage map (triggered vs. missed)."""
    return engine.coverage_map()

@APP.get("/drift")
async def drift_endpoint():
    """Doctrine drift detection (usage pattern changes)."""
    return engine.drift_watcher()

@APP.get("/doctrines")
async def doctrines_endpoint():
    """List all available doctrines."""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "keywords": d.keywords,
                "triggered_count": d.triggered_count,
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }

@APP.get("/categories")
async def categories_endpoint():
    """List issue categories and doctrine counts."""
    category_counts = defaultdict(int)
    for doctrine in DOCTRINE_CACHE:
        category_counts[doctrine.issue_category.value] += 1

    return {
        "categories": dict(category_counts),
        "total_categories": len(category_counts)
    }

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(APP, host="0.0.0.0", port=ENGINE_PORT, log_level="info")
