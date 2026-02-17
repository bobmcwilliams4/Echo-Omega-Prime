"""
MECH13 - Tribology and Lubrication Intelligence Engine
TIE-Grade Domain Expert System

Analyzes friction mechanisms, wear analysis, lubrication regimes, oil analysis programs,
surface engineering, and bearing lubrication design.

Port: 9273
Version: 1.0.0
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import re

# CRITICAL: Add parent directory to sys.path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_NAME = "MECH13_tribology"
ENGINE_VERSION = "1.0.0"
PORT = 9273
LOG_FILE = Path(__file__).parent / f"{ENGINE_NAME}_audit.jsonl"

# Configure loguru
logger.add(
    LOG_FILE,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="100 MB"
)

# ============================================================================
# ENUMS AND DATA STRUCTURES
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
    FRICTION_ANALYSIS = "FRICTION_ANALYSIS"
    WEAR_MECHANISMS = "WEAR_MECHANISMS"
    LUBRICATION_REGIME = "LUBRICATION_REGIME"
    OIL_ANALYSIS = "OIL_ANALYSIS"
    BEARING_DESIGN = "BEARING_DESIGN"
    SURFACE_ENGINEERING = "SURFACE_ENGINEERING"
    GREASE_SELECTION = "GREASE_SELECTION"
    CONDITION_MONITORING = "CONDITION_MONITORING"
    LUBRICANT_CHEMISTRY = "LUBRICANT_CHEMISTRY"
    EHL_CONTACTS = "EHL_CONTACTS"
    SEAL_COMPATIBILITY = "SEAL_COMPATIBILITY"
    CONTAMINATION_CONTROL = "CONTAMINATION_CONTROL"

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

@dataclass
class TelemetryRecord:
    query_id: str
    timestamp: datetime
    mode: ResponseMode
    latency_ms: float
    cache_hit: bool
    doctrines_triggered: List[str]
    confidence: ConfidenceLevel
    error_domain: Optional[str] = None

@dataclass
class CoverageStats:
    triggered_doctrines: Set[str] = field(default_factory=set)
    missed_doctrines: Set[str] = field(default_factory=set)
    epistemic_gaps: List[str] = field(default_factory=list)

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., description="Tribology analysis query")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis context zone")
    include_telemetry: bool = Field(default=False, description="Include performance metrics")

class QueryResponse(BaseModel):
    response: str
    confidence: ConfidenceLevel
    doctrines_applied: List[str]
    reasoning_chain: List[str]
    telemetry: Optional[Dict[str, Any]] = None
    determinism_hash: str
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrine_count: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float

# ============================================================================
# DOCTRINE CACHE - 25+ REAL TRIBOLOGY EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Stribeck Curve Analysis - Lubrication Regime Identification",
        keywords=["stribeck", "lubrication regime", "boundary", "mixed", "hydrodynamic", "friction coefficient", "sommerfeld number"],
        conclusion_template=[
            "The Stribeck curve defines three distinct lubrication regimes based on Sommerfeld number (ηN/P).",
            "Boundary lubrication occurs at low speeds or high loads where asperity contact dominates.",
            "Hydrodynamic lubrication at high speeds creates full fluid film separation with lowest friction."
        ],
        reasoning_framework=[
            "The Stribeck curve plots friction coefficient (μ) versus Sommerfeld number (ηN/P) where:",
            "  η = dynamic viscosity (Pa·s)",
            "  N = rotational speed (rev/s)",
            "  P = bearing pressure (Pa)",
            "",
            "Three regimes:",
            "1. BOUNDARY LUBRICATION (Sommerfeld < 10^-7):",
            "   - Metal-to-metal asperity contact dominates",
            "   - Friction coefficient μ = 0.08-0.15",
            "   - High wear rates, depends on surface chemistry and additives",
            "   - Friction independent of viscosity, governed by surface films",
            "   - EP and AW additives critical for load-carrying capacity",
            "",
            "2. MIXED LUBRICATION (Sommerfeld 10^-7 to 10^-5):",
            "   - Partial fluid film with intermittent asperity contact",
            "   - Friction coefficient μ = 0.02-0.08 (decreasing with speed)",
            "   - Transition zone where both fluid film and surface chemistry matter",
            "   - Most common operating regime for many machinery components",
            "   - Requires balanced additive package for film strength and wear protection",
            "",
            "3. HYDRODYNAMIC LUBRICATION (Sommerfeld > 10^-5):",
            "   - Full fluid film separation, no asperity contact",
            "   - Friction coefficient μ = 0.001-0.005",
            "   - Friction proportional to viscosity and shear rate",
            "   - Near-zero wear, governed by viscous dissipation",
            "   - Viscosity selection based on load, speed, temperature",
            "",
            "Design implications:",
            "- Increase speed or viscosity to move right on curve (toward hydrodynamic)",
            "- Reduce load to improve film thickness",
            "- Surface finish critical in boundary/mixed regimes",
            "- For boundary regime: prioritize EP/AW additives over base oil viscosity",
            "- For hydrodynamic regime: optimize viscosity for minimum power loss",
            "",
            "Film thickness ratio (λ = h_min / σ_composite):",
            "  λ < 1: Boundary lubrication",
            "  λ = 1-3: Mixed lubrication",
            "  λ > 3: Hydrodynamic lubrication",
            "where h_min = minimum film thickness, σ = RMS surface roughness"
        ],
        key_factors=[
            "Sommerfeld number (ηN/P) determines regime",
            "Friction coefficient varies 100x across regimes (0.001 to 0.15)",
            "Boundary regime: surface chemistry dominates, viscosity secondary",
            "Hydrodynamic regime: viscosity dominates, surface chemistry irrelevant",
            "Lambda ratio (λ) predicts asperity contact probability",
            "Operating regime dictates lubricant selection strategy",
            "Mixed regime most common in real machinery due to variable loads/speeds"
        ],
        primary_authority=[
            "Stribeck, R. (1902) Die wesentlichen Eigenschaften der Gleit- und Rollenlager",
            "Hamrock, B.J., Schmid, S.R., Jacobson, B.O. (2004) Fundamentals of Fluid Film Lubrication, 2nd Ed",
            "ASME/STLE Tribology Standards: Film Thickness Calculations"
        ],
        burden_holder="Engineer selecting lubricant and operating conditions",
        adversary_position="Vendor claims work in all regimes without regime-specific justification",
        counter_arguments=[
            "Single-viscosity lubricant cannot optimize all three regimes simultaneously",
            "Boundary additives increase hydrodynamic friction via viscosity modifiers",
            "Low-speed startup always enters boundary regime regardless of running conditions",
            "Temperature rise shifts operating point left on Stribeck curve (lower ηN/P)",
            "Contamination or wear debris changes effective surface roughness and regime"
        ],
        resolution_strategy="Calculate Sommerfeld number for actual operating conditions (nominal and extreme), determine dominant regime, select lubricant formulation optimized for that regime while ensuring adequate protection in transient regimes",
        entity_scope="Rotating machinery, journal bearings, gears, cams, rolling element bearings under EHL",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - fundamental tribology law, experimentally validated across all machinery types",
        controlling_precedent="Stribeck curve is foundational - all bearing design codes (ISO, AGMA, SKF) reference lubrication regime classification"
    ),

    DoctrineBlock(
        topic="Archard Wear Equation - Adhesive Wear Prediction",
        keywords=["archard", "wear volume", "adhesive wear", "wear coefficient", "sliding distance", "hardness", "normal load"],
        conclusion_template=[
            "Archard's equation predicts wear volume as V = K × (W × L) / H.",
            "Wear coefficient K is dimensionless and material-pair specific (typically 10^-3 to 10^-8).",
            "Hardness H in denominator shows wear inversely proportional to surface hardness."
        ],
        reasoning_framework=[
            "Archard wear equation: V = K × (W × L) / H",
            "where:",
            "  V = wear volume (mm³)",
            "  K = dimensionless wear coefficient (material-pair dependent)",
            "  W = normal load (N)",
            "  L = sliding distance (m)",
            "  H = hardness of softer material (Pa or N/mm²)",
            "",
            "Wear coefficient K ranges:",
            "- Severe adhesive wear (metal-metal, dry): K = 10^-2 to 10^-3",
            "- Mild adhesive wear (boundary lubrication): K = 10^-5 to 10^-7",
            "- Mixed lubrication with good additives: K = 10^-7 to 10^-8",
            "- Hydrodynamic lubrication (no contact): K ≈ 0",
            "",
            "Physical interpretation:",
            "- K represents probability that asperity contact produces wear particle",
            "- In boundary regime, K reduced by EP/AW additive films (typically 10-100x reduction)",
            "- Surface hardness H in denominator: doubling hardness halves wear",
            "- Linear dependence on load W and distance L (first-order approximation)",
            "",
            "Limitations of Archard model:",
            "- Assumes steady-state wear (not break-in or catastrophic failure)",
            "- Does not account for abrasive, erosive, or corrosive wear",
            "- K varies with contact pressure, sliding velocity, temperature",
            "- Real wear often non-linear due to work hardening or thermal effects",
            "- Does not predict wear particle size distribution",
            "",
            "Design applications:",
            "1. Material selection: maximize H (nitriding, carburizing, hard coatings)",
            "2. Load reduction: W appears linearly, so halving load halves wear",
            "3. Lubrication regime: moving to mixed/hydrodynamic reduces K by orders of magnitude",
            "4. Sliding distance: reduce L via design (rolling instead of sliding)",
            "5. Wear life prediction: V_critical / (K×W/H) = allowable sliding distance",
            "",
            "K determination methods:",
            "- Pin-on-disk testing per ASTM G99",
            "- Block-on-ring per ASTM G77",
            "- Four-ball wear test per ASTM D4172",
            "- Field calibration from actual component wear measurements"
        ],
        key_factors=[
            "K varies 5-6 orders of magnitude depending on lubrication regime",
            "Hardness increase directly reduces wear (linear relationship)",
            "Load and sliding distance scale wear linearly in first-order model",
            "Boundary lubrication reduces K by factor of 10-100 vs dry sliding",
            "Surface treatments (nitriding, PVD) increase H and reduce K simultaneously",
            "Temperature rise can soften material and increase K",
            "Wear coefficient K must be experimentally determined for each material pair and lubricant"
        ],
        primary_authority=[
            "Archard, J.F. (1953) Contact and Rubbing of Flat Surfaces, Journal of Applied Physics 24(8)",
            "ASTM G99 - Standard Test Method for Wear Testing with Pin-on-Disk Apparatus",
            "Hutchings, I.M. (1992) Tribology: Friction and Wear of Engineering Materials"
        ],
        burden_holder="Design engineer predicting component wear life",
        adversary_position="Manufacturer claims negligible wear without specifying K or testing conditions",
        counter_arguments=[
            "Archard equation assumes constant K, but K varies with pressure and velocity",
            "Break-in wear phase has higher K than steady-state operation",
            "Abrasive contamination introduces separate wear mechanism not captured by K",
            "Thermal effects and oxidation change surface properties over time",
            "Wear particles can act as third-body abrasives, increasing effective K"
        ],
        resolution_strategy="Measure or estimate K for specific material pair and lubricant via standardized testing (ASTM G99, D4172), apply safety factor for K variability, calculate wear volume over expected service life, compare to allowable wear depth for component tolerance limits",
        entity_scope="Sliding contacts, journal bearings, piston rings, gears in boundary/mixed lubrication, seals",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for adhesive wear in steady-state boundary lubrication; model breaks down for abrasive, erosive, fretting, or catastrophic wear",
        controlling_precedent="Archard equation is standard in tribology literature; used in bearing design software and maintenance interval calculations"
    ),

    DoctrineBlock(
        topic="Reynolds Equation for Hydrodynamic Bearings - Film Pressure Distribution",
        keywords=["reynolds equation", "hydrodynamic", "pressure distribution", "film thickness", "journal bearing", "slider bearing", "viscosity"],
        conclusion_template=[
            "Reynolds equation governs pressure distribution in thin fluid films: ∂/∂x(h³∂p/∂x) + ∂/∂z(h³∂p/∂z) = 6μU∂h/∂x.",
            "Film thickness h appears cubed, making bearing clearance critical (load capacity ∝ 1/C²).",
            "Solution yields load capacity, friction, and minimum film thickness for journal bearings."
        ],
        reasoning_framework=[
            "Reynolds equation (2D incompressible, isothermal):",
            "  ∂/∂x(h³ ∂p/∂x) + ∂/∂z(h³ ∂p/∂z) = 6μU ∂h/∂x + 12μ ∂h/∂t",
            "where:",
            "  p = pressure in film (Pa)",
            "  h = film thickness (m)",
            "  μ = dynamic viscosity (Pa·s)",
            "  U = surface velocity (m/s)",
            "  x, z = coordinates (circumferential, axial)",
            "  t = time (for squeeze films)",
            "",
            "Physical meaning:",
            "- Left side: pressure-driven flow (Poiseuille flow) in x and z directions",
            "- Right side: shear-driven flow (Couette flow) due to moving surface",
            "- Wedge geometry (∂h/∂x ≠ 0) generates pressure rise",
            "- Pressure gradient balances applied load on bearing",
            "",
            "Journal bearing simplifications:",
            "- Cylindrical coordinates: x → θR (circumferential), z → axial",
            "- Film thickness: h(θ) = C(1 + ε cos(θ)) where C = radial clearance, ε = eccentricity ratio",
            "- Infinitely long bearing (∂p/∂z = 0): 1D solution",
            "- Short bearing (∂p/∂θ << ∂p/∂z): axial flow dominates",
            "",
            "Load capacity scaling:",
            "- Sommerfeld number S = (μN/P)(R/C)² where N = speed, P = bearing pressure",
            "- Load capacity W ∝ μNU R²L / C²",
            "- Doubling clearance C reduces load capacity by factor of 4",
            "- Load capacity linear in viscosity μ and speed N",
            "",
            "Minimum film thickness h_min:",
            "- For journal bearing: h_min = C(1 - ε)",
            "- Eccentricity ratio ε increases with load (ε → 1 for high load)",
            "- Design criterion: h_min > 3σ (3x composite surface roughness) for hydrodynamic regime",
            "- Typical journal bearings: h_min = 5-50 microns depending on size and load",
            "",
            "Friction coefficient:",
            "- μ_friction = (πR/C) × √(S) for infinitely long bearing",
            "- Friction increases with viscosity (opposite of boundary lubrication)",
            "- Minimum friction at moderate Sommerfeld number (~0.1-1.0)",
            "",
            "Design trade-offs:",
            "- Tight clearance (small C): high load capacity, but higher friction and tighter tolerances",
            "- Loose clearance (large C): lower friction, easier manufacturing, but lower load capacity",
            "- Viscosity increase: higher load capacity but higher power loss",
            "- Speed increase: better film thickness, but thermal issues and power loss",
            "",
            "Numerical solution methods:",
            "- Finite difference on pressure grid",
            "- Finite element for complex geometries",
            "- Mobility method for fast iteration",
            "- Commercial codes: ORBIT, THERMO-HD, ROMAC"
        ],
        key_factors=[
            "Film thickness h cubed in equation makes clearance critically important",
            "Load capacity inversely proportional to clearance squared (W ∝ 1/C²)",
            "Pressure generation requires wedge geometry (∂h/∂x ≠ 0)",
            "Minimum film thickness h_min must exceed 3x surface roughness for full hydrodynamic regime",
            "Friction increases with viscosity in hydrodynamic regime (opposite of boundary)",
            "Sommerfeld number S governs bearing performance maps",
            "Thermal effects (viscosity decrease with temperature) require coupled thermo-hydrodynamic solution"
        ],
        primary_authority=[
            "Reynolds, O. (1886) On the Theory of Lubrication, Philosophical Transactions of Royal Society",
            "Hamrock, B.J. Fundamentals of Fluid Film Lubrication (2004) - Chapter 4: Reynolds Equation",
            "ISO 7902 - Hydrodynamic Plain Journal Bearings under Steady-State Conditions"
        ],
        burden_holder="Bearing designer ensuring adequate film thickness and load capacity",
        adversary_position="Supplier claims bearing works without providing clearance, viscosity, or film thickness calculations",
        counter_arguments=[
            "Reynolds equation assumes isothermal conditions; thermal effects reduce viscosity 50%+ in high-speed bearings",
            "Misalignment introduces edge loading not captured by 2D model",
            "Surface roughness effects (micro-EHL) alter pressure distribution near asperities",
            "Turbulent flow at high Reynolds numbers invalidates laminar flow assumption",
            "Elastic deformation of bearing surfaces (especially in thin-wall bushings) changes film shape"
        ],
        resolution_strategy="Solve Reynolds equation numerically for actual geometry, loads, speeds; verify h_min > 3σ; if thermal effects significant, use coupled thermo-hydrodynamic solver; validate with ORBIT or equivalent software; apply safety factor on minimum film thickness",
        entity_scope="Journal bearings, slider bearings, thrust bearings, tilting pad bearings, gas bearings (compressible form)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for steady-state, laminar, isothermal conditions; lower confidence for high-speed thermal effects or turbulent flow",
        controlling_precedent="Reynolds equation is foundational - all bearing design standards (ISO 7902, API 610, API 684) reference Reynolds-based calculations"
    ),

    DoctrineBlock(
        topic="Elastohydrodynamic Lubrication (EHL) - Rolling Contact Film Thickness",
        keywords=["EHL", "elastohydrodynamic", "rolling contact", "hertzian", "film thickness", "pressure spike", "ball bearing", "gear teeth"],
        conclusion_template=[
            "EHL combines elastic deformation and hydrodynamic pressure in rolling contacts.",
            "Central film thickness h_c ∝ (μU)^0.67 W^-0.067 - weakly dependent on load.",
            "Minimum film thickness h_min ≈ 0.6 h_c due to pressure spike at exit constriction."
        ],
        reasoning_framework=[
            "Elastohydrodynamic Lubrication (EHL) occurs in rolling contacts where:",
            "- Contact pressures exceed 1 GPa (Hertzian stress)",
            "- Elastic deformation of surfaces creates convergent-divergent wedge",
            "- Lubricant viscosity increases 1000x due to pressure-viscosity effect",
            "- Film thickness 0.1-1.0 microns (submicron in many cases)",
            "",
            "Central film thickness (Hamrock-Dowson equation):",
            "  h_c = 2.69 × R' × (μ₀U)^0.67 × α^0.53 × W^-0.067 × (1-0.61e^-0.73k)",
            "where:",
            "  h_c = central film thickness (m)",
            "  R' = reduced radius of curvature (m)",
            "  μ₀ = ambient viscosity (Pa·s)",
            "  U = entrainment velocity = (u₁+u₂)/2 (m/s)",
            "  α = pressure-viscosity coefficient (Pa^-1), typically 10-25 GPa^-1",
            "  W = load per unit length (N/m)",
            "  k = ellipticity parameter (ratio of contact ellipse axes)",
            "",
            "Key insights from h_c scaling:",
            "- Speed exponent 0.67: doubling speed increases h_c by factor of 1.6",
            "- Load exponent -0.067: doubling load decreases h_c by only 4.5%",
            "- Viscosity exponent 0.67: film thickness sensitive to viscosity",
            "- Pressure-viscosity coefficient α strongly affects film (exponent 0.53)",
            "",
            "Minimum film thickness:",
            "  h_min ≈ 0.6 × h_c (empirical from numerical solutions)",
            "- Occurs at exit constriction due to pressure spike",
            "- Pressure spike can reach 2-3x Hertzian maximum pressure",
            "- Critical location for surface distress and pitting initiation",
            "",
            "Pressure-viscosity relationship (Barus equation):",
            "  μ(p) = μ₀ × exp(α × p)",
            "- At p = 1 GPa and α = 20 GPa^-1: μ = μ₀ × exp(20) ≈ μ₀ × 5×10^8",
            "- Lubricant becomes nearly solid in high-pressure zone",
            "- Shear stress limited by lubricant shear strength (~10 MPa)",
            "",
            "Lambda ratio for EHL contacts:",
            "  λ = h_min / σ_composite",
            "- λ > 3: Full EHL, negligible asperity contact",
            "- λ = 1-3: Partial EHL, some micro-contact",
            "- λ < 1: Boundary lubrication despite rolling motion",
            "",
            "Design implications:",
            "1. Viscosity selection: higher μ₀ increases h_c, but limit viscosity to avoid churning losses",
            "2. Speed increase: most effective way to increase film thickness (exponent 0.67)",
            "3. Load reduction: weak effect on h_c (exponent only -0.067)",
            "4. Synthetic esters/PAO: higher α (pressure-viscosity coefficient) than mineral oils",
            "5. Surface finish: λ > 3 requires h_min > 0.3-0.9 microns for typical bearing surfaces",
            "",
            "Failure modes in EHL:",
            "- Surface fatigue pitting at h_min location (pressure spike zone)",
            "- Micropitting if λ < 2 (mixed lubrication)",
            "- Scuffing if thermal effects reduce viscosity below critical",
            "- Rolling contact fatigue life ∝ h_min^3 (ISO 281 bearing life)"
        ],
        key_factors=[
            "Film thickness weakly dependent on load (exponent -0.067) due to elastic deformation compensation",
            "Speed has strong effect (exponent 0.67) - most effective design lever",
            "Pressure-viscosity coefficient α critical for synthetics vs mineral oils",
            "Minimum film thickness h_min ≈ 0.6 h_c at exit constriction",
            "Lambda ratio λ = h_min/σ must exceed 3 for full EHL protection",
            "Pressure spike at exit can reach 2-3x Hertzian max pressure",
            "Rolling contact fatigue life strongly dependent on h_min (power law exponent 3-10)"
        ],
        primary_authority=[
            "Hamrock, B.J., Dowson, D. (1977) Isothermal EHL of Point Contacts, ASME Journal of Lubrication Technology",
            "Johnson, K.L. (1985) Contact Mechanics, Cambridge University Press - Chapter 4: EHL",
            "ISO 281 - Rolling Bearings: Dynamic Load Ratings and Rating Life (EHL film thickness in life adjustment)"
        ],
        burden_holder="Rolling element bearing designer or gear engineer ensuring adequate film thickness",
        adversary_position="Supplier claims grease or low-viscosity oil adequate without EHL film thickness calculation",
        counter_arguments=[
            "Thermal effects reduce viscosity at contact inlet, lowering h_c by 30-50% vs isothermal prediction",
            "Surface roughness orientation (transverse vs longitudinal) affects effective λ",
            "Non-Newtonian shear thinning at high shear rates reduces film thickness",
            "Starvation (insufficient lubricant supply) reduces h_c below fully-flooded prediction",
            "Slide-to-roll ratio > 0.1 introduces frictional heating and thinning"
        ],
        resolution_strategy="Calculate h_c using Hamrock-Dowson equation for actual speeds, loads, lubricant properties (μ₀, α); estimate h_min = 0.6 h_c; compute λ = h_min/σ; require λ > 3 for full protection, λ > 2 minimum for acceptable life; if λ < 2, increase speed, viscosity, or improve surface finish",
        entity_scope="Ball bearings, roller bearings, gear teeth, cam-follower contacts, CVT (continuously variable transmission) contacts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for steady-state isothermal point contacts; moderate confidence for line contacts or thermal effects; lower confidence for starved or contaminated conditions",
        controlling_precedent="Hamrock-Dowson equations widely accepted in bearing industry; ISO 281 bearing life calculations reference EHL film thickness; AGMA gear rating standards use EHL-based scuffing criteria"
    ),

    DoctrineBlock(
        topic="Oil Analysis Interpretation - Wear Metals and Contamination Limits",
        keywords=["oil analysis", "spectrometry", "wear metals", "particle count", "ISO 4406", "viscosity", "TAN", "TBN", "ferrography"],
        conclusion_template=[
            "Oil analysis detects abnormal wear via elemental spectroscopy (Fe, Cu, Cr, Al, Pb, Sn).",
            "ISO 4406 cleanliness code (e.g., 18/16/13) specifies particle counts at 4, 6, 14 microns.",
            "Trend analysis more valuable than single-point data; 2x increase in wear metals triggers investigation."
        ],
        reasoning_framework=[
            "Oil analysis program monitors lubricant condition and equipment health:",
            "",
            "1. WEAR METAL ANALYSIS (ICP or RDE spectroscopy):",
            "   - Iron (Fe): general wear from ferrous components (gears, bearings, cylinders)",
            "   - Copper (Cu): bronze bearings, bushings, thrust washers, gear coatings",
            "   - Chromium (Cr): piston rings, hardened steel bearings (>1% Cr steel)",
            "   - Aluminum (Al): aluminum bearings, pistons, debris from wear",
            "   - Lead (Pb): babbitt bearings, bronze alloys, solder contamination",
            "   - Tin (Sn): babbitt bearings, bronze, overlay plating on bearings",
            "   - Molybdenum (Mo): piston rings with moly coating, oil additive (MoDTC)",
            "   - Nickel (Ni): bearing cages, steel alloys, high-temp alloys",
            "",
            "   Typical baseline levels (ppm):",
            "   - Fe: 10-30 (gearboxes), 5-15 (hydraulics), 20-50 (engines)",
            "   - Cu: 5-15 (gearboxes with bronze gears), 10-30 (compressors)",
            "   - Cr: <5 (normal), >10 suggests bearing distress",
            "   - Al: <10 (normal), >20 suggests piston/bearing wear",
            "   - Pb: <10 (babbitt bearings), >30 suggests overlay loss",
            "",
            "   Abnormal wear thresholds:",
            "   - 2x baseline: investigate, increase sampling frequency",
            "   - 3x baseline: urgent - schedule inspection/maintenance",
            "   - 10x baseline: critical - component failure imminent",
            "",
            "2. PARTICLE COUNT (ISO 4406 cleanliness code):",
            "   - Measures particles >4μm, >6μm, >14μm per 100mL",
            "   - Reported as ISO code: X/Y/Z (e.g., 18/16/13)",
            "   - Code 18 = 1300-2500 particles, Code 16 = 320-640, Code 13 = 40-80",
            "",
            "   Target cleanliness levels:",
            "   - Servo valves, high-performance hydraulics: 14/12/9 or better",
            "   - General hydraulics: 18/16/13",
            "   - Gearboxes: 19/17/14",
            "   - Circulating systems: 20/18/15",
            "",
            "   New oil from supplier often 20/18/15 - requires filtration before use",
            "",
            "3. VISCOSITY (ASTM D445 kinematic viscosity):",
            "   - Measures viscosity at 40°C and 100°C",
            "   - ±10% deviation from baseline triggers fluid replacement",
            "   - Increase suggests oxidation, contamination, or wrong fluid",
            "   - Decrease suggests fuel dilution, thermal breakdown, or shear degradation",
            "",
            "4. ACID NUMBER AND BASE NUMBER:",
            "   - TAN (Total Acid Number, ASTM D664): measures acidic oxidation products",
            "   - TBN (Total Base Number, ASTM D2896): measures alkaline reserve in engine oils",
            "   - TAN increase >2.0 mg KOH/g vs new oil indicates oxidation",
            "   - TBN decrease to <50% of original indicates depleted additive reserve",
            "",
            "5. WATER CONTENT (Karl Fischer method, ASTM D6304):",
            "   - <100 ppm: acceptable for most systems",
            "   - 100-500 ppm: caution, monitor for increase",
            "   - >500 ppm: unacceptable, water damages additives and accelerates oxidation",
            "   - Water promotes rust, bacterial growth, additive depletion, foam",
            "",
            "6. FERROGRAPHY (analytical ferrography, ASTM D7690):",
            "   - Separates magnetic particles by size for microscopic examination",
            "   - Identifies wear mode: cutting, sliding, fatigue, severe sliding",
            "   - Large particles (>15 microns) suggest abnormal wear",
            "   - Laminar particles indicate sliding wear",
            "   - Chunky particles suggest fatigue or corrosive wear",
            "   - Dark oxide particles (FeO) indicate high-temperature sliding",
            "",
            "TREND ANALYSIS STRATEGY:",
            "- Baseline: 3-5 samples on new/rebuilt equipment to establish normal",
            "- Routine sampling: monthly (critical), quarterly (normal), annually (low-duty)",
            "- Plot wear metals vs operating hours: slope indicates wear rate",
            "- Sudden step increase (not gradual slope): indicates event (seal failure, contamination ingestion)",
            "- Combine multiple tests: Fe+Cr elevated + viscosity increase + particle count increase = bearing distress + oxidation",
            "",
            "CORRECTIVE ACTIONS:",
            "- High wear metals: inspect component, check alignment, verify lubrication regime",
            "- High particle count: increase filtration, check seals, add kidney-loop filter",
            "- High TAN or low TBN: change fluid, investigate operating temperature",
            "- High water: check seals, add desiccant breather, investigate condensation sources"
        ],
        key_factors=[
            "Wear metal concentrations (ppm) indicate component distress before failure",
            "ISO 4406 cleanliness code governs hydraulic system reliability",
            "Trend analysis (slope over time) more valuable than single-point absolute values",
            "2x baseline wear metals triggers investigation; 10x baseline indicates imminent failure",
            "Particle count in new oil often unacceptable - filtration before use essential",
            "Water content >500 ppm damages additives and accelerates oxidation",
            "TAN increase or TBN depletion indicates oil end-of-life",
            "Ferrography identifies wear mode (sliding, fatigue, cutting) from particle morphology"
        ],
        primary_authority=[
            "ASTM D7720 - Standard Practice for Statistically Evaluating Measurand Alarm Limits for Oil Analysis",
            "ISO 4406 - Hydraulic Fluid Power: Fluids - Method for Coding Level of Contamination by Solid Particles",
            "SAE AS4059 - Aerospace Fluid Power: Cleanliness Requirements for Aircraft Hydraulic Systems"
        ],
        burden_holder="Maintenance engineer interpreting oil analysis data and deciding on corrective actions",
        adversary_position="Laboratory provides data without context or thresholds; operator ignores gradual wear trends",
        counter_arguments=[
            "Single-point sample can have measurement variability ±20%, trend needed for confidence",
            "Wear metal baselines vary by equipment type, manufacturer, and operating conditions",
            "Particle count can spike temporarily after maintenance without indicating failure",
            "Viscosity increase from oxidation can be masked by fuel dilution (false normal reading)",
            "Spectroscopy detects only dissolved metals <5 microns; large wear particles require ferrography"
        ],
        resolution_strategy="Establish equipment-specific baselines via 3-5 initial samples; set alarm thresholds at 2x and 3x baseline for wear metals; monitor trends (plot ppm vs hours); combine multiple tests (metals + particles + viscosity + TAN/TBN) for diagnosis; investigate when any parameter exceeds 2x baseline or trend slope increases",
        entity_scope="Gearboxes, hydraulic systems, compressors, engines, turbines, pumps - any lubricated machinery",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for wear metal and particle count trends; moderate confidence for single-point diagnosis; lower confidence without baseline data or trend history",
        controlling_precedent="ASTM D7720 provides statistical methods for alarm limits; ISO 4406 is universal standard for hydraulic cleanliness; industry-wide acceptance of trend analysis over absolute limits"
    ),

    DoctrineBlock(
        topic="Lubricant Base Oil Groups (API) - Performance Characteristics",
        keywords=["base oil", "group I", "group II", "group III", "group IV", "PAO", "synthetic", "viscosity index", "saturates", "sulfur"],
        conclusion_template=[
            "API classifies base oils into Groups I-V based on refining method, saturates, sulfur, and VI.",
            "Group III and PAO (Group IV) are synthetic with VI >120, superior thermal/oxidative stability.",
            "Group I mineral oils have VI 80-120, lower cost but shorter drain intervals."
        ],
        reasoning_framework=[
            "API Base Oil Classification (five groups):",
            "",
            "GROUP I (Solvent-refined mineral oil):",
            "  - Saturates: <90%",
            "  - Sulfur: >0.03%",
            "  - Viscosity Index (VI): 80-120",
            "  - Production: solvent refining, mild hydrotreatment",
            "  - Characteristics:",
            "    * High sulfur and aromatics (polar compounds)",
            "    * Good solvency for additives",
            "    * Lower oxidative stability (shorter drain intervals)",
            "    * VI improvers often required for multigrade oils",
            "    * Lowest cost per gallon",
            "  - Applications: industrial oils, grease base stocks, low-tier automotive oils",
            "  - Typical drain interval: 3000-5000 miles (automotive), 500-1000 hours (industrial)",
            "",
            "GROUP II (Hydrocracked mineral oil):",
            "  - Saturates: >90%",
            "  - Sulfur: <0.03%",
            "  - Viscosity Index (VI): 80-120",
            "  - Production: severe hydrocracking, hydrotreatment",
            "  - Characteristics:",
            "    * Low sulfur, low aromatics (saturated hydrocarbons)",
            "    * Clear, water-white appearance",
            "    * Improved oxidative stability vs Group I",
            "    * Better low-temperature properties",
            "    * Moderate cost",
            "  - Applications: modern automotive oils (most 5W-30, 10W-30), hydraulic fluids",
            "  - Typical drain interval: 5000-7500 miles (automotive), 1000-2000 hours (industrial)",
            "",
            "GROUP III (Hydrocracked/hydroisomerized synthetic):",
            "  - Saturates: >90%",
            "  - Sulfur: <0.03%",
            "  - Viscosity Index (VI): >120",
            "  - Production: severe hydrocracking with isomerization",
            "  - Characteristics:",
            "    * High VI (often 130-150) with minimal VI improvers",
            "    * Excellent oxidative stability (extended drains)",
            "    * Low volatility (low oil consumption)",
            "    * Improved cold-start performance",
            "    * Marketed as 'synthetic' in many regions (legal definition varies)",
            "  - Applications: synthetic automotive oils, premium hydraulics, compressors",
            "  - Typical drain interval: 10,000-15,000 miles (automotive), 3000-5000 hours (industrial)",
            "",
            "GROUP IV (Polyalphaolefins - PAO):",
            "  - Synthetic hydrocarbon (not petroleum-derived)",
            "  - Viscosity Index (VI): 120-160",
            "  - Production: oligomerization of alpha-olefins (ethylene, propylene, butene)",
            "  - Characteristics:",
            "    * Uniform molecular structure (narrow MW distribution)",
            "    * Highest VI of hydrocarbon base oils (typically 130-160)",
            "    * Excellent low-temperature fluidity (pour point -40°C to -60°C)",
            "    * Superior oxidative and thermal stability",
            "    * Low volatility (NOACK <10%)",
            "    * Poor solvency for additives (requires Group I/II blend or esters)",
            "  - Applications: premium synthetics, extreme-temperature lubricants, aviation",
            "  - Typical drain interval: 15,000-25,000 miles (automotive), 5000-8000 hours (industrial)",
            "",
            "GROUP V (All others - synthetic esters, PAGs, silicones):",
            "  - Synthetic esters: diesters, polyolesters, phosphate esters",
            "  - Polyalkylene glycols (PAG): water-soluble or water-insoluble",
            "  - Silicones: polydimethylsiloxane (extreme temperature)",
            "  - Characteristics:",
            "    * Esters: polar, excellent solvency, biodegradable, hygroscopic",
            "    * PAG: non-petroleum, incompatible with mineral oils, high VI",
            "    * Silicones: extreme temperature range (-50°C to +250°C), low traction",
            "  - Applications:",
            "    * Esters: jet engine oils, 2-stroke oils, compressor oils, biodegradable hydraulics",
            "    * PAG: gear oils (especially worm gears), compressor oils, coolants",
            "    * Silicones: vacuum pumps, dampers, extreme temperature applications",
            "",
            "VISCOSITY INDEX (VI) IMPACT:",
            "- VI = measure of viscosity change with temperature (ASTM D2270)",
            "- High VI (>120): minimal viscosity loss at high temperature",
            "- Group I VI 90: 10W-40 requires 15% VI improver (shear unstable)",
            "- Group III VI 140: 5W-30 requires minimal VI improver (shear stable)",
            "- PAO VI 150: enables wide-range multiviscosity (0W-40, 5W-50)",
            "",
            "OXIDATIVE STABILITY:",
            "- Group I: 500-1000 hours before significant oxidation (RPVOT)",
            "- Group II: 1000-2000 hours",
            "- Group III/IV: 2000-5000 hours",
            "- Oxidation leads to viscosity increase, sludge, varnish, TAN increase",
            "",
            "SELECTION CRITERIA:",
            "- Cost-sensitive, moderate duty: Group II",
            "- Extended drain, high temperature: Group III or PAO blend",
            "- Extreme cold starts: PAO or Group III (low pour point)",
            "- Biodegradability: esters (Group V)",
            "- Seal/paint compatibility: avoid PAO alone, blend with esters or Group I/II"
        ],
        key_factors=[
            "Group III and PAO have VI >120, enabling wide-range multigrade oils with minimal VI improvers",
            "Group II is workhorse for modern automotive/industrial oils (low sulfur, moderate cost)",
            "PAO has best low-temperature performance (pour point -40°C to -60°C) but poor additive solvency",
            "Esters (Group V) provide polarity and solvency for additives in PAO blends",
            "Oxidative stability increases from Group I to IV, extending drain intervals 5-10x",
            "Group I/II are petroleum-derived; Group III is hydrocracked to synthetic-like properties; PAO/esters are true synthetics",
            "Base oil choice affects additive treat rate, drain interval, low-temp performance, and cost"
        ],
        primary_authority=[
            "API 1509 - Engine Oil Licensing and Certification System (base oil classification)",
            "ASTM D2270 - Standard Practice for Calculating Viscosity Index from Kinematic Viscosity",
            "Mortier, R.M., Fox, M.F., Orszulik, S.T. (2010) Chemistry and Technology of Lubricants, 3rd Ed"
        ],
        burden_holder="Lubricant formulator or procurement engineer selecting base oil for application requirements",
        adversary_position="Supplier markets Group III as 'full synthetic' at premium price vs PAO; or claims all base oils equivalent",
        counter_arguments=[
            "Group III labeled 'synthetic' but is hydrocracked mineral oil (legal definition varies by region)",
            "PAO superior to Group III in low-temp flow, but Group III often sufficient and lower cost",
            "Group I adequate for many industrial applications with lower cost and shorter drain intervals",
            "Ester content in 'synthetic blend' can be <5% with majority Group I/II",
            "VI improver shear degradation negates high VI of base oil in some multigrade oils"
        ],
        resolution_strategy="Define application requirements: drain interval, temperature range, load, seal compatibility; select base oil group that meets performance at lowest total cost (including drain interval economics); verify with supplier base oil group breakdown if labeled 'synthetic' or 'blend'; for critical applications use Group III or PAO; for cost-sensitive use Group II",
        entity_scope="All lubricated equipment: engines, gearboxes, hydraulics, compressors, turbines",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - API base oil groups are industry-standard classification with clear chemical and performance distinctions",
        controlling_precedent="API 1509 defines base oil groups universally accepted by lubricant industry; ASTM standards for VI and oxidation testing provide objective performance metrics"
    ),

    DoctrineBlock(
        topic="EP and AW Additives - Extreme Pressure and Anti-Wear Mechanisms",
        keywords=["EP", "AW", "ZDDP", "extreme pressure", "anti-wear", "sulfur", "phosphorus", "chlorine", "boundary lubrication", "additive"],
        conclusion_template=[
            "Anti-Wear (AW) additives form protective films at moderate temperatures (90-150°C) to prevent adhesive wear.",
            "Extreme Pressure (EP) additives activate at high temperatures (>150°C) to prevent scuffing and seizure.",
            "ZDDP (zinc dialkyldithiophosphate) is the most common AW additive, providing sacrificial tribofilm."
        ],
        reasoning_framework=[
            "EP and AW additives protect surfaces in boundary and mixed lubrication regimes:",
            "",
            "ANTI-WEAR (AW) ADDITIVES:",
            "- Function: form low-shear-strength protective films at moderate contact temperatures",
            "- Activation: 90-150°C (typical asperity contact flash temperature)",
            "- Mechanism: chemical reaction with metal surface to form sacrificial layer",
            "",
            "ZDDP (Zinc Dialkyldithiophosphate) - primary AW additive:",
            "  - Chemical structure: Zn[(RO)₂PS₂]₂ where R = alkyl chain",
            "  - Thermal decomposition at 90-130°C releases phosphorus and sulfur",
            "  - Forms zinc phosphate glassy film on steel surfaces (100-200 nm thick)",
            "  - Film shears preferentially, protecting base metal from wear",
            "  - Typical treat rate: 0.1-0.2 wt% P (0.8-1.5 wt% ZDDP)",
            "  - Benefits:",
            "    * Reduces wear by factor of 5-10 in boundary lubrication",
            "    * Provides corrosion protection (Zn, P compounds inhibit rust)",
            "    * Antioxidant (sacrificial - consumes peroxides)",
            "  - Limitations:",
            "    * Catalyst poison (automotive emissions - reduced in modern oils)",
            "    * Ash-forming (contributes to engine deposits)",
            "    * Incompatible with some seal materials (nitrile swelling)",
            "",
            "Other AW additives:",
            "  - TCP (tricresyl phosphate): ashless AW for aviation/hydraulic fluids",
            "  - Phosphate esters: provide AW with low ash, good hydrolytic stability",
            "  - Molybdenum dithiocarbamate (MoDTC): AW + friction modifier",
            "",
            "EXTREME PRESSURE (EP) ADDITIVES:",
            "- Function: prevent scuffing, scoring, and seizure under extreme loads",
            "- Activation: >150°C flash temperature (high-load asperity contact)",
            "- Mechanism: react with metal surface to form low-shear inorganic films",
            "",
            "Sulfur-based EP additives:",
            "  - Active sulfur (polysulfides): react with iron to form FeS films",
            "  - Activation temperature: 150-200°C",
            "  - FeS film shear strength ~100 MPa (vs steel-steel >500 MPa)",
            "  - Typical treat rate: 0.5-3 wt% S in gear oils, cutting fluids",
            "  - Limitations:",
            "    * Corrosive to yellow metals (copper, bronze) - avoid in worm gears",
            "    * Can cause staining at high temperatures (>100°C storage)",
            "    * Odor (H₂S evolution at high temperatures)",
            "",
            "Phosphorus-based EP additives:",
            "  - Triphenyl phosphate, TCP: forms iron phosphate films",
            "  - Activation temperature: 130-180°C",
            "  - Typical treat rate: 0.1-0.5 wt% P (combined AW/EP function)",
            "",
            "Chlorinated paraffins (older EP technology):",
            "  - Forms FeCl₂ films at very high temperatures (>200°C)",
            "  - Activation requires high temperature and load",
            "  - Environmental concerns (PBT - persistent, bioaccumulative, toxic)",
            "  - Being phased out in many applications",
            "",
            "ADDITIVE SYNERGY AND ANTAGONISM:",
            "- ZDDP + sulfur EP: synergistic, common in gear oils",
            "- ZDDP + detergents: antagonistic, detergents can deactivate ZDDP film",
            "- Active sulfur + yellow metals: highly corrosive, incompatible",
            "- MoDTC + ZDDP: synergistic for friction reduction + wear protection",
            "",
            "FILM FORMATION MECHANISM:",
            "1. Additive adsorbs to metal surface via polar groups",
            "2. Flash temperature at asperity contact exceeds activation temperature",
            "3. Additive decomposes, releasing reactive S, P, or Cl",
            "4. Reactive species react with iron oxide layer to form tribofilm",
            "5. Tribofilm (FeS, FePO₄, FeS₂) shears at lower stress than base metal",
            "6. Continuous film formation and removal during operation",
            "",
            "TESTING METHODS:",
            "- Four-ball EP test (ASTM D2783): measure weld load, load wear index",
            "  * Weld load >250 kg indicates good EP performance",
            "- Four-ball wear test (ASTM D4172): measure scar diameter under standard load",
            "  * Scar <0.4 mm indicates good AW performance",
            "- FZG gear test (DIN 51354): measure gear scuffing load stage",
            "  * Failure load stage >12 indicates excellent EP protection",
            "- Timken OK load (ASTM D2782): maximum load before scoring",
            "",
            "SELECTION CRITERIA:",
            "- Moderate loads, steel-steel contacts: ZDDP alone (0.1% P) sufficient",
            "- High loads, potential scuffing: ZDDP + sulfur EP (0.1% P + 1-2% S)",
            "- Yellow metal compatibility: avoid active sulfur, use phosphorus-based",
            "- Ashless requirement (2-stroke, aviation): TCP or phosphate esters",
            "- Environmental/toxicity: avoid chlorinated paraffins, minimize ZDDP"
        ],
        key_factors=[
            "AW additives (ZDDP) activate at 90-150°C, form protective phosphate films, reduce wear 5-10x",
            "EP additives (sulfur, phosphorus) activate at >150°C, prevent scuffing and seizure under extreme loads",
            "ZDDP is workhorse AW additive but catalyst poison and ash-former (reduced in modern automotive oils)",
            "Sulfur EP highly effective but corrosive to copper/bronze - incompatible with worm gears",
            "Additive films (FeS, FePO₄) shear at 100-200 MPa vs steel-steel 500+ MPa",
            "Four-ball and FZG tests provide standardized EP/AW performance metrics",
            "ZDDP concentration in automotive oils reduced from 1200 ppm P (1990s) to 600-800 ppm P (2020s) for emissions"
        ],
        primary_authority=[
            "Spikes, H. (2004) The History and Mechanisms of ZDDP, Tribology Letters 17(3)",
            "ASTM D2783 - Extreme Pressure Properties of Lubricating Fluids (Four-Ball Method)",
            "Mortier, R.M. (2010) Chemistry and Technology of Lubricants - Chapter 7: EP and AW Additives"
        ],
        burden_holder="Lubricant formulator balancing AW/EP performance with emissions, seal compatibility, and cost",
        adversary_position="Marketing claims 'superior EP protection' without test data; or claims ZDDP-free oil equivalent to ZDDP oil",
        counter_arguments=[
            "ZDDP reduction for emissions compliance reduces wear protection in older engines designed for higher P levels",
            "Alternative AW additives (boron, molybdenum) not as effective as ZDDP for steel-steel contacts",
            "Sulfur EP can cause copper corrosion in bronze synchronizers (manual transmissions)",
            "Extreme pressure claims require FZG or four-ball test data - not all 'EP oils' perform equally",
            "Additive treat rate alone doesn't indicate performance - synergy and base oil quality matter"
        ],
        resolution_strategy="Specify AW/EP requirements based on contact load, material compatibility, and application (automotive, industrial, gear, hydraulic); request four-ball wear test (ASTM D4172) for AW verification and FZG load stage or four-ball EP test (ASTM D2783) for EP verification; avoid sulfur EP if yellow metals present; balance ZDDP level with emission requirements if automotive",
        entity_scope="Gears, bearings, hydraulic pumps, engines, sliding contacts in boundary/mixed lubrication",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - EP/AW additive chemistry and mechanisms well-established with decades of industrial use and standardized testing",
        controlling_precedent="ASTM D2783, D4172, and DIN 51354 are industry-standard tests; API/ILSAC specifications define minimum AW/EP performance for automotive oils"
    ),

    DoctrineBlock(
        topic="Grease Selection - NLGI Grade, Thickener Type, and Dropping Point",
        keywords=["grease", "NLGI", "thickener", "lithium", "polyurea", "calcium sulfonate", "dropping point", "consistency", "worked penetration"],
        conclusion_template=[
            "NLGI grade (000 to 6) defines grease consistency via worked penetration (ASTM D217).",
            "NLGI 2 is most common (penetration 265-295), suitable for general-purpose bearings.",
            "Thickener type (lithium, calcium sulfonate, polyurea) determines temperature range and water resistance."
        ],
        reasoning_framework=[
            "Grease composition: Base oil (70-95%) + Thickener (3-30%) + Additives (0-10%)",
            "",
            "NLGI CONSISTENCY GRADES (ASTM D217 worked penetration):",
            "- Penetration = depth (0.1 mm) that cone penetrates grease under standard load",
            "- Worked penetration: after 60 strokes in grease worker (simulates shear)",
            "",
            "  Grade | Penetration (0.1mm) | Consistency | Applications",
            "  ------|---------------------|-------------|-------------",
            "  000   | 445-475             | Fluid       | Gear enclosed systems",
            "  00    | 400-430             | Semi-fluid  | Centralized lube systems",
            "  0     | 355-385             | Soft        | Cold climate, low-speed bearings",
            "  1     | 310-340             | Soft        | Cold starts, food processing",
            "  2     | 265-295             | Standard    | General-purpose bearings (most common)",
            "  3     | 220-250             | Firm        | High-vibration, vertical shafts",
            "  4     | 175-205             | Very firm   | High-temp, slow-speed, vertical",
            "  5     | 130-160             | Hard        | Specialty applications",
            "  6     | 85-115              | Very hard   | Specialty (rare)",
            "",
            "- NLGI 2 accounts for ~75% of grease market (versatile, pumpable, stays in place)",
            "- Softer grades (0, 1): better low-temp flow, easier pumping, risk of leakage",
            "- Harder grades (3, 4): resist leakage, high-vibration, but poor low-temp and pumping",
            "",
            "THICKENER TYPES:",
            "",
            "1. LITHIUM SOAP (most common, ~70% of grease market):",
            "   - Chemistry: lithium stearate or 12-hydroxystearate",
            "   - Dropping point: 175-190°C (simple soap), 200-260°C (complex lithium)",
            "   - Max operating temp: 120-130°C (simple), 150-180°C (complex)",
            "   - Water resistance: good",
            "   - Mechanical stability: excellent (resists shear)",
            "   - Cost: moderate",
            "   - Applications: general-purpose automotive, industrial bearings, chassis lube",
            "   - Limitation: not for very high temp or heavy water exposure",
            "",
            "2. CALCIUM SULFONATE COMPLEX:",
            "   - Chemistry: calcium sulfonate + calcium carbonate nanoparticles",
            "   - Dropping point: >260°C (often >300°C)",
            "   - Max operating temp: 180-200°C",
            "   - Water resistance: excellent (best of all thickeners)",
            "   - Mechanical stability: very good",
            "   - EP properties: inherent due to calcium carbonate particles (no separate EP additive needed)",
            "   - Cost: higher than lithium",
            "   - Applications: marine, steel mills, paper mills, high-water environments, high-temp bearings",
            "   - Benefit: combines high temp, water resistance, and EP in one thickener system",
            "",
            "3. POLYUREA:",
            "   - Chemistry: urea linkage between diisocyanate and amine",
            "   - Dropping point: >250°C (no true dropping point - gradual degradation)",
            "   - Max operating temp: 150-180°C (some formulations to 200°C)",
            "   - Water resistance: good to excellent",
            "   - Mechanical stability: excellent (very shear-stable)",
            "   - Oxidative stability: superior (long relubrication intervals)",
            "   - Cost: higher than lithium",
            "   - Applications: electric motors, high-speed bearings, sealed-for-life bearings, automotive wheel bearings",
            "   - Benefit: long life (oxidative stability), wide temp range, low oil bleed",
            "",
            "4. ALUMINUM COMPLEX:",
            "   - Dropping point: >250°C",
            "   - Max operating temp: 150-175°C",
            "   - Water resistance: fair (less than lithium)",
            "   - Mechanical stability: good",
            "   - Applications: high-temp industrial bearings, food-grade formulations (some approved)",
            "",
            "5. BENTONITE (CLAY) THICKENER:",
            "   - Non-soap inorganic thickener",
            "   - No true dropping point (non-melting)",
            "   - Max operating temp: 200-250°C (limited by base oil)",
            "   - Water resistance: poor (absorbs water, loses consistency)",
            "   - Mechanical stability: poor (irreversible shear thinning)",
            "   - Applications: extreme high-temp (ovens, kilns), radiation environments",
            "   - Limitation: not pumpable, requires pre-packing, sensitive to water",
            "",
            "DROPPING POINT (ASTM D566 or D2265):",
            "- Temperature at which grease becomes fluid and drips",
            "- Indicates maximum usable temperature (with safety margin)",
            "- Rule of thumb: max operating temp = dropping point - 50°C to 80°C",
            "- Lithium simple soap: 175-190°C dropping point → max use 120-130°C",
            "- Polyurea: >250°C dropping point → max use 170-180°C",
            "",
            "BASE OIL VISCOSITY IN GREASE:",
            "- Grease base oil typically ISO VG 100-220 (mineral oil, PAO, or ester)",
            "- Low-temp grease: ISO VG 32-68 with low pour point",
            "- High-speed bearings: lower viscosity base oil (ISO VG 68-100) to reduce churning",
            "- Heavy-load, slow-speed: higher viscosity (ISO VG 220-460)",
            "",
            "GREASE LIFE AND RELUBRICATION INTERVALS:",
            "- L10 life: operating hours until 10% of bearings require relubrication",
            "- SKF relubrication formula: t_f = (14 × 10^6 / (n × d_m^1.4)) × k_factors",
            "  where n = speed (rpm), d_m = mean bearing diameter (mm)",
            "- Polyurea grease: 2-3x life vs lithium due to oxidative stability",
            "- High temperature: life reduced exponentially (halves every 15°C above 70°C)",
            "",
            "COMPATIBILITY:",
            "- Mixing incompatible greases can cause softening or hardening",
            "- Lithium + calcium: generally compatible",
            "- Lithium + polyurea: limited compatibility (test before field use)",
            "- Aluminum + most others: poor compatibility",
            "- Recommendation: purge old grease when switching thickener type",
            "",
            "SELECTION CRITERIA:",
            "1. Temperature: select thickener with dropping point >50°C above max operating temp",
            "2. Water exposure: calcium sulfonate (excellent), polyurea (good), lithium (fair)",
            "3. Speed: NLGI 2 for general, NLGI 1 or 0 for high speed to reduce churning",
            "4. Load: EP additives or calcium sulfonate thickener for heavy loads",
            "5. Relubrication interval: polyurea or calcium sulfonate for long life",
            "6. Cost: lithium for general-purpose, upgrade to polyurea/calcium sulfonate for severe service"
        ],
        key_factors=[
            "NLGI 2 is most common grade (75% of market), suitable for general bearings",
            "NLGI grade defines consistency via worked penetration: softer = better pumpability, harder = resists leakage",
            "Lithium thickener most common (70% of market), max temp ~130°C (simple) or 180°C (complex)",
            "Calcium sulfonate: highest water resistance, inherent EP, max temp 200°C, higher cost",
            "Polyurea: best oxidative stability (long life), max temp 180°C, sealed-for-life bearings",
            "Dropping point indicates max temperature with 50-80°C safety margin",
            "Thickener compatibility critical when switching grease types - purge or test before mixing"
        ],
        primary_authority=[
            "NLGI Lubricating Grease Guide, 5th Edition (2014)",
            "ASTM D217 - Cone Penetration of Lubricating Grease",
            "SKF Grease Selection Guide (SKF publication PUB GS/P1 10000/1 EN)"
        ],
        burden_holder="Bearing engineer or maintenance planner selecting grease for application requirements",
        adversary_position="Supplier recommends single 'multi-purpose' grease for all applications without temperature, water, or speed justification",
        counter_arguments=[
            "Multi-purpose NLGI 2 lithium grease not optimal for high-temp, high-water, or sealed-for-life applications",
            "Polyurea grease 2-3x higher cost but often justified by extended relubrication intervals (total cost lower)",
            "Softer grease (NLGI 0, 1) can leak from seals in vertical or high-vibration applications",
            "Harder grease (NLGI 3, 4) difficult to pump, causing starvation in centralized systems",
            "Mixing incompatible thickeners causes consistency loss and bearing failure"
        ],
        resolution_strategy="Define operating conditions: temperature (max and min), speed (rpm), load, water exposure, relubrication interval; select NLGI grade (typically 2, use 1 for high speed or cold, 3 for vertical/vibration); select thickener: lithium for general <130°C, calcium sulfonate for water/high-temp, polyurea for long life/sealed; verify dropping point >50°C above max temp; confirm compatibility if switching from existing grease",
        entity_scope="Rolling element bearings, sleeve bearings, chassis grease points, gears (open or semi-enclosed), slides and ways",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - NLGI grading system and thickener chemistry well-established with decades of field experience and standardized testing",
        controlling_precedent="NLGI grade standards universally accepted; bearing manufacturers (SKF, Timken, NSK) publish grease selection guides based on NLGI classification and thickener type"
    ),

    DoctrineBlock(
        topic="Surface Engineering - Nitriding, PVD Coatings, and DLC for Wear Resistance",
        keywords=["surface treatment", "nitriding", "PVD", "DLC", "coating", "hardness", "wear resistance", "friction", "case depth"],
        conclusion_template=[
            "Nitriding diffuses nitrogen into steel surface, creating 700-1200 HV case to 0.1-0.8mm depth.",
            "PVD coatings (TiN, TiAlN, CrN) deposit 1-5 micron ceramic films with hardness 2000-3000 HV.",
            "DLC (diamond-like carbon) provides ultra-low friction (μ = 0.05-0.15) and extreme hardness (2000-8000 HV)."
        ],
        reasoning_framework=[
            "Surface engineering modifies surface properties without affecting bulk material:",
            "",
            "1. NITRIDING (Thermal Diffusion Process):",
            "",
            "   Gas Nitriding (most common):",
            "   - Process: heat steel to 500-550°C in ammonia (NH₃) atmosphere 20-80 hours",
            "   - Nitrogen diffuses into surface, forming iron nitrides (Fe₂N, Fe₃N, Fe₄N)",
            "   - Case depth: 0.1-0.8 mm (0.004-0.030 inch) depending on time and steel",
            "   - Surface hardness: 700-1200 HV (Vickers) on nitriding steels (Cr, Mo, Al alloyed)",
            "   - Core hardness unchanged (typically 300-400 HV)",
            "   - Advantages:",
            "     * Low processing temperature (minimal distortion, no quench)",
            "     * Excellent wear resistance (hard case)",
            "     * Improved fatigue strength (compressive residual stress in case)",
            "     * Corrosion resistance improved (passive nitride layer)",
            "   - Limitations:",
            "     * Thin case (not suitable for heavy abrasive wear)",
            "     * Requires nitriding steels (plain carbon steels limited hardness ~400 HV)",
            "     * Long process time (20-80 hours)",
            "   - Applications: gears, crankshafts, camshafts, valve components, injection mold tooling",
            "",
            "   Plasma (Ion) Nitriding:",
            "   - Process: ionized nitrogen plasma bombards surface at 350-500°C",
            "   - Faster than gas nitriding (4-20 hours), better control of case depth and compound layer",
            "   - Case depth: 0.05-0.5 mm, hardness: 700-1200 HV",
            "   - Benefit: lower temperature option, selective nitriding via masking",
            "",
            "   Salt Bath Nitriding (Liquid Nitriding, QPQ):",
            "   - Process: immerse in molten cyanate salt (350-580°C), then oxidize in second salt bath",
            "   - Case depth: 0.01-0.03 mm (thin, primarily for corrosion + moderate wear)",
            "   - Surface hardness: 600-900 HV",
            "   - Benefit: fast (1-4 hours), excellent corrosion resistance (black oxide layer)",
            "   - Limitation: thin case, environmental concerns (cyanide salts)",
            "",
            "2. PHYSICAL VAPOR DEPOSITION (PVD) COATINGS:",
            "",
            "   Process overview:",
            "   - Deposit thin ceramic films (1-5 microns) via vacuum evaporation or sputtering",
            "   - Substrate temperature 150-500°C (low vs CVD, minimal distortion)",
            "   - Ion bombardment during deposition improves adhesion and densifies coating",
            "",
            "   TiN (Titanium Nitride) - gold color:",
            "   - Hardness: 2000-2500 HV",
            "   - Friction coefficient: 0.4-0.6 (vs uncoated steel 0.6-0.8)",
            "   - Max service temp: 600°C (oxidation above this)",
            "   - Applications: cutting tools, dies, decorative (gold color), bearings",
            "   - Limitation: not suitable for high-temp or oxidizing environments",
            "",
            "   TiAlN (Titanium Aluminum Nitride) - violet/purple color:",
            "   - Hardness: 2500-3000 HV",
            "   - Friction coefficient: 0.4-0.5",
            "   - Max service temp: 800-900°C (Al₂O₃ protective layer forms)",
            "   - Applications: high-speed machining tools, hot forging dies, severe wear",
            "   - Benefit: superior high-temp oxidation resistance vs TiN",
            "",
            "   CrN (Chromium Nitride) - silver/gray color:",
            "   - Hardness: 1700-2200 HV",
            "   - Friction coefficient: 0.4-0.5",
            "   - Max service temp: 700°C",
            "   - Corrosion resistance: excellent (better than TiN)",
            "   - Applications: plastic injection molds (anti-stick), forming tools, marine environments",
            "   - Benefit: best corrosion resistance of common PVD coatings",
            "",
            "   AlTiN, AlCrN, TiB₂ (advanced PVD coatings):",
            "   - Hardness: 3000-3500 HV",
            "   - Max service temp: 900-1100°C",
            "   - Applications: extreme machining (titanium, Inconel), dry cutting",
            "",
            "3. DIAMOND-LIKE CARBON (DLC):",
            "",
            "   Types:",
            "   - Hydrogenated a-C:H (softer, lower friction): 1000-2000 HV, μ = 0.05-0.10",
            "   - Non-hydrogenated ta-C (tetrahedral amorphous carbon, harder): 5000-8000 HV, μ = 0.10-0.15",
            "   - Metal-doped DLC (W-DLC, Cr-DLC): improved adhesion, moderate hardness 1500-3000 HV",
            "",
            "   Deposition: PVD or PECVD (plasma-enhanced CVD), 1-3 micron thickness",
            "   Substrate temp: 50-200°C (very low, suitable for temperature-sensitive parts)",
            "",
            "   Properties:",
            "   - Hardness: 1000-8000 HV depending on sp3/sp2 carbon bond ratio",
            "   - Friction coefficient: 0.05-0.15 (ultra-low, comparable to PTFE in dry conditions)",
            "   - Wear resistance: excellent (can exceed hardened steel 100x in sliding)",
            "   - Chemical inertness: excellent (resists acids, bases, solvents)",
            "   - Electrical insulation: high resistivity (except graphitic DLC)",
            "",
            "   Limitations:",
            "   - Adhesion challenges on steel (requires interlayer: Cr, Ti, W)",
            "   - Thermal stability limited to 300-400°C (graphitization above this)",
            "   - Residual compressive stress can cause spalling on thick coatings (>3 microns)",
            "   - Not effective in high-temperature or oxidizing environments",
            "",
            "   Applications:",
            "   - Automotive: piston rings, tappets, fuel injectors (friction reduction)",
            "   - Medical: orthopedic implants, surgical instruments (biocompatibility + wear)",
            "   - Precision tooling: punches, forming dies, razor blades",
            "   - Aerospace: landing gear components, bearings",
            "",
            "SURFACE TREATMENT COMPARISON:",
            "",
            "  Treatment    | Hardness (HV) | Thickness | Friction μ | Max Temp | Cost",
            "  -------------|---------------|-----------|------------|----------|------",
            "  Nitriding    | 700-1200      | 0.1-0.8mm | 0.15-0.20  | 500°C    | Low-Med",
            "  TiN PVD      | 2000-2500     | 1-5μm     | 0.4-0.6    | 600°C    | Medium",
            "  TiAlN PVD    | 2500-3000     | 1-5μm     | 0.4-0.5    | 900°C    | Med-High",
            "  CrN PVD      | 1700-2200     | 1-5μm     | 0.4-0.5    | 700°C    | Medium",
            "  DLC (a-C:H)  | 1000-2000     | 1-3μm     | 0.05-0.10  | 300°C    | High",
            "  DLC (ta-C)   | 5000-8000     | 1-3μm     | 0.10-0.15  | 300°C    | Very High",
            "",
            "SELECTION STRATEGY:",
            "- Deep case for heavy wear: nitriding (0.1-0.8 mm case)",
            "- Extreme hardness for abrasive wear: TiAlN or ta-C DLC (2500-8000 HV)",
            "- Ultra-low friction: DLC (μ = 0.05-0.15, can eliminate lubricant in some cases)",
            "- High-temperature wear: TiAlN (up to 900°C) or nitriding (500°C)",
            "- Corrosion + wear: CrN PVD or QPQ nitriding",
            "- Cost-sensitive, moderate wear: gas nitriding",
            "",
            "ADHESION AND FAILURE MODES:",
            "- PVD/DLC coatings fail via spalling if adhesion inadequate (requires interlayer)",
            "- Nitriding fails via case crushing if overloaded (exceeds 700-1200 HV yield)",
            "- Edge chipping common on thin hard coatings (fillet radii required)",
            "- Thermal cycling can delaminate coatings if CTE mismatch (substrate vs coating)"
        ],
        key_factors=[
            "Nitriding creates 0.1-0.8 mm case at 700-1200 HV, low distortion, cost-effective",
            "PVD coatings (TiN, TiAlN, CrN) deposit 1-5 micron ceramic films at 2000-3000 HV",
            "DLC provides ultra-low friction (μ = 0.05-0.15) and hardness up to 8000 HV (ta-C)",
            "TiAlN superior to TiN for high-temperature applications (900°C vs 600°C)",
            "DLC limited to 300-400°C max temperature (graphitization above this)",
            "Surface treatment selection depends on: wear type, temperature, friction requirements, case depth, cost",
            "PVD/DLC adhesion critical - requires proper substrate preparation and interlayers"
        ],
        primary_authority=[
            "ASM Handbook Volume 5: Surface Engineering (2013)",
            "Holmberg, K., Matthews, A. (2009) Coatings Tribology, 2nd Ed - Chapter 6: PVD Coatings",
            "Robertson, J. (2002) Diamond-like Amorphous Carbon, Materials Science and Engineering R37"
        ],
        burden_holder="Design engineer selecting surface treatment to meet wear, friction, and temperature requirements",
        adversary_position="Coating vendor claims universal superiority of one coating type without application-specific analysis",
        counter_arguments=[
            "No single coating optimal for all conditions: DLC fails at high temp, TiAlN has higher friction than DLC, nitriding too thin for heavy abrasive wear",
            "Coating adhesion failure more common than coating wear in improperly prepared substrates",
            "DLC friction advantage lost in boundary lubrication with EP additives (both achieve μ ~ 0.05-0.10)",
            "Nitriding distortion claim overstated - still requires post-process grinding for precision parts",
            "PVD coating cost justified only if life extension exceeds 3-5x vs uncoated (economic breakeven)"
        ],
        resolution_strategy="Define application requirements: wear type (sliding, rolling, abrasive), temperature, friction target, required case depth, substrate hardness; select treatment: nitriding for deep case + moderate cost, TiAlN for high-temp + hardness, DLC for ultra-low friction + moderate temp; verify substrate preparation (hardness, roughness, cleanliness) for PVD/DLC adhesion; test in application before production",
        entity_scope="Gears, bearings, cutting tools, forming dies, piston rings, valve components, shafts, slides",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - surface treatment technologies mature with extensive industrial use and published performance data",
        controlling_precedent="ASM handbooks and coating manufacturer data sheets provide standardized treatment properties; bearing OEMs (SKF, Schaeffler) specify surface treatments in technical requirements"
    ),

    # Additional doctrine blocks continue with same depth and rigor...
    # (25+ blocks total covering all major tribology domains)

    DoctrineBlock(
        topic="Bearing Lubrication Design - Minimum Film Thickness Calculation",
        keywords=["bearing", "film thickness", "clearance", "viscosity", "sommerfeld", "eccentricity", "load capacity"],
        conclusion_template=[
            "Minimum film thickness h_min = C(1 - ε) where C = radial clearance and ε = eccentricity ratio.",
            "Design criterion: h_min > 3σ_composite ensures full hydrodynamic regime (λ > 3).",
            "Sommerfeld number S = (μN/P)(R/C)² governs bearing performance and eccentricity."
        ],
        reasoning_framework=[
            "Journal bearing film thickness design follows Reynolds equation solutions:",
            "",
            "KEY PARAMETERS:",
            "- C = radial clearance (m): difference between bearing and journal radii",
            "- ε = eccentricity ratio: e/C where e = eccentricity (journal center offset)",
            "- h_min = minimum film thickness (m): occurs at maximum load point",
            "- σ = RMS surface roughness (m): composite σ = √(σ_bearing² + σ_journal²)",
            "- λ = lambda ratio: h_min/σ (film thickness parameter)",
            "",
            "MINIMUM FILM THICKNESS:",
            "  h_min = C(1 - ε)",
            "",
            "Eccentricity ratio ε varies with load:",
            "- Light load (S > 1): ε ≈ 0.2-0.4, h_min ≈ 0.6-0.8 C",
            "- Moderate load (S ≈ 0.1-1.0): ε ≈ 0.5-0.7, h_min ≈ 0.3-0.5 C",
            "- Heavy load (S < 0.1): ε ≈ 0.8-0.95, h_min ≈ 0.05-0.2 C",
            "- Critical load (ε → 1): h_min → 0, metal contact imminent",
            "",
            "LAMBDA RATIO (λ):",
            "  λ = h_min / σ_composite",
            "",
            "Lubrication regime classification:",
            "- λ < 1: Boundary lubrication (asperity contact, high wear)",
            "- λ = 1-3: Mixed lubrication (partial contact, moderate wear)",
            "- λ > 3: Hydrodynamic lubrication (full film, negligible wear)",
            "",
            "Design target: λ > 3 for long bearing life",
            "  → h_min > 3 × σ_composite",
            "",
            "SOMMERFELD NUMBER:",
            "  S = (μN/P) × (R/C)²",
            "where:",
            "  μ = dynamic viscosity (Pa·s)",
            "  N = rotational speed (rev/s)",
            "  P = bearing pressure = W/(D×L) (Pa)",
            "  W = load (N)",
            "  D = journal diameter (m)",
            "  L = bearing length (m)",
            "  R = journal radius (m)",
            "  C = radial clearance (m)",
            "",
            "Sommerfeld number governs bearing performance:",
            "- High S (>1): thick film, low friction, but high power loss",
            "- Low S (<0.01): thin film, risk of metal contact",
            "- Optimal S ≈ 0.1-1.0: balance film thickness and friction",
            "",
            "CLEARANCE SELECTION:",
            "- Tight clearance (C/R = 0.0005-0.001): high load capacity, tight tolerance required",
            "- Normal clearance (C/R = 0.001-0.002): general-purpose, good balance",
            "- Loose clearance (C/R = 0.002-0.004): easy assembly, lower load capacity",
            "",
            "Typical clearance ratios C/R:",
            "- Precision spindles: 0.0005-0.0008",
            "- Automotive engine bearings: 0.0008-0.0015",
            "- Industrial machinery: 0.001-0.002",
            "- Large turbine bearings: 0.0015-0.003",
            "",
            "DESIGN PROCEDURE:",
            "1. Define load W, speed N, bearing dimensions (D, L)",
            "2. Select clearance C (typically C/R = 0.001-0.002)",
            "3. Select lubricant viscosity μ at operating temperature",
            "4. Calculate bearing pressure P = W/(D×L)",
            "5. Calculate Sommerfeld number S = (μN/P)(R/C)²",
            "6. Determine eccentricity ratio ε from S (charts or iterative solution)",
            "7. Calculate h_min = C(1 - ε)",
            "8. Measure or estimate surface roughness σ_composite",
            "9. Calculate lambda ratio λ = h_min/σ",
            "10. Verify λ > 3 (if not, increase C, μ, or N, or decrease P)",
            "",
            "SURFACE FINISH TARGETS:",
            "- High-performance bearings: Ra = 0.1-0.4 microns (σ ≈ 0.15-0.5 microns)",
            "- General industrial: Ra = 0.4-1.6 microns (σ ≈ 0.5-2.0 microns)",
            "- Composite roughness: σ_composite = √(σ_bearing² + σ_journal²)",
            "",
            "Example calculation:",
            "  Given: D = 100 mm, L = 50 mm, W = 10 kN, N = 1500 rpm = 25 rev/s",
            "         C = 0.1 mm (C/R = 0.002), μ = 0.03 Pa·s (ISO VG 68 at 60°C)",
            "         σ_bearing = σ_journal = 0.8 microns",
            "",
            "  P = W/(D×L) = 10000/(0.1×0.05) = 2 MPa",
            "  S = (0.03×25/2×10^6) × (0.05/0.0001)² = 0.234",
            "  From charts: ε ≈ 0.65 at S = 0.234",
            "  h_min = 0.1 × (1-0.65) = 0.035 mm = 35 microns",
            "  σ_composite = √(0.8² + 0.8²) = 1.13 microns",
            "  λ = 35/1.13 = 31 → Full hydrodynamic (λ >> 3), excellent",
            "",
            "THERMAL EFFECTS:",
            "- Viscosity decreases with temperature: μ_new ≈ μ_ref × exp[-α(T-T_ref)]",
            "- Thermal expansion reduces clearance C (potentially by 10-30%)",
            "- Shear heating in oil film: ΔT ≈ μ×U²/(2k) where k = thermal conductivity",
            "- Iterative thermo-hydrodynamic solution required for high-speed bearings",
            "",
            "FAILURE MODES:",
            "- λ < 1: Boundary lubrication, rapid wear, scuffing, seizure",
            "- Excessive clearance: oil leakage, whirl instability, vibration",
            "- Insufficient viscosity: film breakdown, metal contact",
            "- Misalignment: edge loading, local film thickness <3σ even if average λ > 3"
        ],
        key_factors=[
            "Minimum film thickness h_min = C(1 - ε) depends on clearance and eccentricity ratio",
            "Lambda ratio λ = h_min/σ must exceed 3 for full hydrodynamic lubrication",
            "Sommerfeld number S governs bearing performance: S = (μN/P)(R/C)²",
            "Clearance ratio C/R typically 0.001-0.002 for general industrial bearings",
            "Tight clearance increases load capacity (W ∝ 1/C²) but requires tighter tolerances",
            "Surface finish critical: σ < h_min/3 required for λ > 3",
            "Thermal effects reduce viscosity 50%+ in high-speed bearings, requiring coupled analysis"
        ],
        primary_authority=[
            "ISO 7902-1 - Hydrodynamic Plain Journal Bearings under Steady-State Conditions - Calculation Procedure",
            "Raimondi, A.A., Boyd, J. (1958) Solution for Infinitely Long Journal Bearing, ASLE Transactions",
            "Hamrock, B.J. (2004) Fundamentals of Fluid Film Lubrication - Chapter 9: Journal Bearing Design"
        ],
        burden_holder="Bearing designer ensuring adequate film thickness and load capacity while avoiding excessive friction",
        adversary_position="Supplier provides bearing without clearance specification or film thickness calculation",
        counter_arguments=[
            "ISO 7902 assumes isothermal conditions; thermal effects reduce viscosity 50%+ in high-speed bearings, reducing λ",
            "Misalignment introduces edge loading with local λ < 1 even if calculated average λ > 3",
            "Startup and shutdown pass through boundary regime (λ < 1) regardless of running design",
            "Contamination or wear debris increases effective surface roughness σ, reducing λ over time",
            "Vibration and dynamic loads can momentarily reduce h_min below calculated steady-state value"
        ],
        resolution_strategy="Calculate Sommerfeld number S for actual load, speed, viscosity, clearance; determine ε from S; calculate h_min = C(1-ε); measure or specify surface finish σ; verify λ = h_min/σ > 3; if λ < 3, increase clearance C, viscosity μ, speed N, or improve surface finish; apply safety factor (λ > 4-5 recommended for critical applications); verify with bearing analysis software (ORBIT, THERMO-HD) for thermal effects",
        entity_scope="Journal bearings, sleeve bearings, crankshaft bearings, turbine bearings, motor bearings, hydrostatic bearings",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for steady-state isothermal conditions per ISO 7902; moderate confidence for high-speed or heavily loaded bearings requiring thermo-hydrodynamic analysis",
        controlling_precedent="ISO 7902 is international standard for journal bearing calculation; API 610 (pumps) and API 684 (rotordynamics) reference ISO 7902 methodology"
    ),

    DoctrineBlock(
        topic="Viscosity Index Improvers - Shear Stability and Temporary vs Permanent Loss",
        keywords=["viscosity index", "VII", "polymer", "shear stability", "temporary viscosity loss", "permanent viscosity loss", "PSSI", "multigrade"],
        conclusion_template=[
            "Viscosity Index Improvers (VII) are high-MW polymers that expand at high temp to maintain viscosity.",
            "Shear degradation causes permanent viscosity loss (PSSI = Permanent Shear Stability Index).",
            "Temporary viscosity loss is recoverable shear thinning; permanent loss is chain scission."
        ],
        reasoning_framework=[
            "Viscosity Index Improvers (VII) enable wide-range multigrade oils (e.g., 5W-30, 10W-40):",
            "",
            "FUNCTION AND MECHANISM:",
            "- VII are high-molecular-weight polymers (MW 50,000 to 500,000)",
            "- At low temp: polymer coils contract, minimal viscosity contribution",
            "- At high temp: polymer coils expand, thicken oil to maintain target viscosity",
            "- Result: high Viscosity Index (VI >150 for VII-treated oils vs 90-110 for base oil alone)",
            "",
            "COMMON VII CHEMISTRIES:",
            "1. Olefin Copolymers (OCP):",
            "   - Ethylene-propylene copolymers",
            "   - MW: 50,000-200,000",
            "   - Shear stability: moderate to good",
            "   - Cost: low to moderate",
            "   - Applications: automotive engine oils, industrial lubricants",
            "",
            "2. Polymethacrylates (PMA):",
            "   - Methacrylate esters with varying alkyl chain lengths",
            "   - MW: 30,000-100,000",
            "   - Shear stability: good to excellent (lower MW than OCP)",
            "   - Multifunctional: can include dispersant side chains (DI-PMA)",
            "   - Applications: premium automotive oils, ATF, hydraulic fluids",
            "",
            "3. Styrene-Diene Copolymers:",
            "   - Styrene-isoprene or styrene-butadiene",
            "   - MW: 100,000-300,000",
            "   - Shear stability: poor to moderate (high MW, prone to scission)",
            "   - Cost: low",
            "   - Applications: legacy industrial oils (being replaced by OCP/PMA)",
            "",
            "4. Hydrogenated Styrene-Diene (HSD):",
            "   - Hydrogenated to improve oxidative stability",
            "   - Shear stability: moderate",
            "   - Applications: gear oils, some automotive applications",
            "",
            "SHEAR DEGRADATION MECHANISMS:",
            "",
            "1. TEMPORARY VISCOSITY LOSS (reversible):",
            "   - Mechanism: high shear rate aligns polymer chains, reducing hydrodynamic volume",
            "   - Recovery: when shear rate decreases, chains re-coil and viscosity recovers",
            "   - Measurement: compare viscosity at low shear (40°C, 100°C) vs high shear (10^6 s⁻¹)",
            "   - HTHS (High Temperature High Shear) viscosity: ASTM D4683, 150°C, 10^6 s⁻¹",
            "   - Example: 5W-30 may have KV100 = 10 cSt but HTHS = 2.9 cP (temporary thinning)",
            "   - Impact: reduced film thickness in high-shear contacts (bearings, cams) during operation",
            "",
            "2. PERMANENT VISCOSITY LOSS (irreversible):",
            "   - Mechanism: mechanical scission of polymer backbone at high shear stress",
            "   - Occurs in: gears, pumps, bearings (shear stress >1 MPa)",
            "   - Result: polymer MW decreases, viscosity contribution permanently reduced",
            "   - Measurement: PSSI (Permanent Shear Stability Index) or SSI (Shear Stability Index)",
            "",
            "PERMANENT SHEAR STABILITY INDEX (PSSI):",
            "  PSSI = [(KV_fresh - KV_sheared) / (KV_fresh - KV_base)] × 100%",
            "where:",
            "  KV_fresh = kinematic viscosity of fresh VII-treated oil (cSt at 100°C)",
            "  KV_sheared = KV after shearing (ASTM D6278 sonic shear, or ASTM D5621 Kurt Orbahn)",
            "  KV_base = KV of base oil without VII (cSt at 100°C)",
            "",
            "PSSI interpretation:",
            "- PSSI < 10%: Excellent shear stability (e.g., PMA, low-MW OCP)",
            "- PSSI 10-30%: Good shear stability (typical OCP)",
            "- PSSI 30-60%: Moderate shear stability (high-MW OCP, HSD)",
            "- PSSI > 60%: Poor shear stability (styrene-diene, very high MW polymers)",
            "",
            "TEST METHODS FOR SHEAR STABILITY:",
            "- ASTM D6278 (Sonic Shear): ultrasonic probe shears oil, simulates mechanical shear",
            "- ASTM D5621 (Kurt Orbahn): diesel injector pump shears oil, field-representative",
            "- ASTM D7109 (Tapered Roller Bearing Rig): 20 hours at high load/speed",
            "- CEC L-45-A-99 (European): diesel injector pump, correlates with field performance",
            "",
            "IMPACT ON LUBRICANT PERFORMANCE:",
            "- Fresh oil: 10W-40 meets viscosity targets at -25°C (10W) and 100°C (40 grade)",
            "- After shear: viscosity at 100°C drops to ~9.5 cSt (now performs like 10W-30)",
            "- Consequence: reduced film thickness at high temp, increased wear in boundary regime",
            "- SAE J300 limits: minimum HTHS viscosity to ensure protection after shear",
            "",
            "MULTIGRADE OIL DESIGN CONSIDERATIONS:",
            "- Wide-range multigrade (e.g., 5W-50, 0W-40): requires high VII treat rate (10-15%)",
            "  → Higher shear degradation risk due to high-MW polymers",
            "- Narrow-range multigrade (e.g., 5W-30, 10W-30): lower VII treat rate (3-8%)",
            "  → Better shear stability, preferred for modern engines",
            "- Monograde oils (SAE 30, 40): no VII required, best shear stability but poor cold-start",
            "",
            "VII SELECTION CRITERIA:",
            "1. Shear stability required: select low-MW PMA or OCP (PSSI < 20%)",
            "2. Cost-sensitive: OCP (lower cost than PMA)",
            "3. Multifunctional (dispersancy + VII): DI-PMA (dispersant polymethacrylate)",
            "4. Narrow-viscosity-range multigrade: minimize VII treat rate for better shear stability",
            "5. High-VI base oil (Group III, PAO): reduces VII requirement, improves shear stability",
            "",
            "FIELD IMPLICATIONS:",
            "- Hydraulic systems: shear degradation reduces viscosity below minimum required for pump protection",
            "  → Monitor viscosity after 500-1000 hours, top-up or change if drops >10%",
            "- Engine oils: HTHS viscosity critical for cam/bearing protection",
            "  → SAE J300 specifies minimum HTHS (e.g., 2.6 cP for xW-20, 2.9 cP for xW-30)",
            "- Gear oils: high shear in gear mesh can permanently reduce viscosity 20-30%",
            "  → Use shear-stable VII (PMA) or higher base oil viscosity with less VII",
            "",
            "TEMPORARY VS PERMANENT LOSS COMPARISON:",
            "- Temporary loss: high-shear thinning during operation, recovers at rest",
            "  → Measured via HTHS viscosity (ASTM D4683, D5481)",
            "  → Impact: reduced film thickness in loaded contacts during operation",
            "- Permanent loss: irreversible MW reduction due to chain scission",
            "  → Measured via PSSI (ASTM D6278, D5621)",
            "  → Impact: viscosity grade shift over service life (e.g., 10W-40 → 10W-30)",
            "",
            "MITIGATION STRATEGIES:",
            "1. Use high-VI base oils (Group III, PAO) to reduce VII requirement",
            "2. Select shear-stable VII (PMA, low-MW OCP) for critical applications",
            "3. Avoid excessive viscosity range (5W-50 more prone to shear than 5W-30)",
            "4. Monitor viscosity in service (oil analysis) and replace when drops >10%",
            "5. For severe-shear applications (hydraulics, gears): use monograde or narrow-range multigrade"
        ],
        key_factors=[
            "VII polymers expand at high temp to maintain viscosity, enabling multigrade oils (e.g., 5W-30)",
            "Temporary viscosity loss is reversible shear thinning; permanent loss is chain scission (irreversible)",
            "PSSI (Permanent Shear Stability Index) <10% excellent, 10-30% good, >60% poor",
            "Wide-range multigrades (5W-50, 0W-40) require high VII treat rate, higher shear risk",
            "PMA (polymethacrylates) have best shear stability; styrene-diene worst (being phased out)",
            "High-VI base oils (Group III, PAO) reduce VII requirement, improving shear stability",
            "HTHS viscosity (150°C, 10^6 s⁻¹) measures temporary loss; ASTM D6278/D5621 measures permanent loss"
        ],
        primary_authority=[
            "SAE J300 - Engine Oil Viscosity Classification (includes HTHS minimum requirements)",
            "ASTM D6278 - Shear Stability of Polymer-Containing Fluids Using Sonic Shear",
            "Mortier, R.M. (2010) Chemistry and Technology of Lubricants - Chapter 6: Viscosity Modifiers"
        ],
        burden_holder="Lubricant formulator balancing multigrade range, shear stability, and cost",
        adversary_position="Marketing claims wide-range multigrade (0W-50) superior without disclosing shear degradation risk",
        counter_arguments=[
            "Wide-range multigrade requires 10-15% VII treat rate, high risk of shear degradation (PSSI >30%)",
            "Temporary HTHS thinning reduces film thickness 20-40% in loaded contacts during operation",
            "Shear degradation converts 10W-40 into 10W-30 over service life, reducing protection",
            "Group I base oil multigrade (high VII content) shears more than Group III narrow-range (low VII)",
            "Monograde or narrow-range multigrade provides better shear stability for severe-duty applications"
        ],
        resolution_strategy="Define application shear severity (hydraulic pumps, gears, engines); specify PSSI requirement (<20% for severe shear, <30% for moderate); select VII chemistry (PMA for best shear stability, OCP for cost balance); use high-VI base oil to minimize VII treat rate; avoid excessive viscosity range (prefer 5W-30 over 5W-50 if possible); test with ASTM D6278 or D5621; monitor viscosity in service and replace when drops >10%",
        entity_scope="Automotive engine oils, hydraulic fluids, gear oils, industrial circulating oils, ATF (automatic transmission fluids)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - VII chemistry and shear degradation mechanisms well-studied with decades of field data and standardized testing (ASTM D6278, D5621, SAE J300)",
        controlling_precedent="SAE J300 mandates minimum HTHS viscosity and shear stability for engine oil classifications; API/ILSAC specifications include shear stability limits; ISO VG classification system references viscosity at 40°C and 100°C (indirectly affected by VII shear)"
    ),

]

# ============================================================================
# TRIBOLOGY INTELLIGENCE ENGINE
# ============================================================================

class MECH13TribologyEngine:
    def __init__(self):
        self.doctrine_cache = DOCTRINE_CACHE
        self.telemetry_records: List[TelemetryRecord] = []
        self.coverage_stats = CoverageStats()
        self.total_queries = 0
        self.start_time = datetime.now()

        logger.info(f"{ENGINE_NAME} v{ENGINE_VERSION} initialized with {len(self.doctrine_cache)} doctrine blocks")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Dict[str, Any]:
        """
        Three-layer architecture:
        1. Doctrine Cache (0-200ms): Pre-compiled expert blocks
        2. Semantic Retrieval (200-2000ms): Vector search fallback
        3. Deep Analysis (2-10s): Multi-source synthesis
        """
        start_time = datetime.now()
        query_id = hashlib.sha256(f"{query}{start_time}".encode()).hexdigest()[:16]

        # Layer 1: Doctrine Cache
        triggered_doctrines = self._search_doctrine_cache(query)
        cache_hit = len(triggered_doctrines) > 0

        if cache_hit:
            response = self._generate_from_doctrines(triggered_doctrines, query, mode, zone)
            latency_ms = (datetime.now() - start_time).total_seconds() * 1000

            self._record_telemetry(query_id, mode, latency_ms, cache_hit, triggered_doctrines)

            return {
                "response": response["text"],
                "confidence": response["confidence"],
                "doctrines_applied": [d.topic for d in triggered_doctrines],
                "reasoning_chain": response["reasoning_chain"],
                "layer": "DOCTRINE_CACHE",
                "latency_ms": latency_ms
            }

        # Layer 2: Semantic Retrieval (simplified - would use vector DB in production)
        semantic_results = self._semantic_search(query)
        if semantic_results:
            response = self._generate_from_semantic(semantic_results, query, mode, zone)
            latency_ms = (datetime.now() - start_time).total_seconds() * 1000
            self._record_telemetry(query_id, mode, latency_ms, False, [])
            return response

        # Layer 3: Deep Analysis (fallback)
        response = self._deep_analysis(query, mode, zone)
        latency_ms = (datetime.now() - start_time).total_seconds() * 1000
        self._record_telemetry(query_id, mode, latency_ms, False, [])
        return response

    def _search_doctrine_cache(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache by keyword matching"""
        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))

        matches = []
        for doctrine in self.doctrine_cache:
            # Check keyword overlap
            doctrine_keywords = set(k.lower() for k in doctrine.keywords)
            overlap = query_words & doctrine_keywords

            # Also check topic and reasoning framework for matches
            topic_match = any(word in doctrine.topic.lower() for word in query_words)
            framework_text = " ".join(doctrine.reasoning_framework).lower()
            framework_match = any(word in framework_text for word in query_words if len(word) > 4)

            if len(overlap) >= 2 or topic_match or framework_match:
                matches.append(doctrine)
                self.coverage_stats.triggered_doctrines.add(doctrine.topic)

        # Track missed doctrines
        if not matches:
            for doctrine in self.doctrine_cache:
                self.coverage_stats.missed_doctrines.add(doctrine.topic)

        return matches[:5]  # Top 5 most relevant

    def _generate_from_doctrines(
        self,
        doctrines: List[DoctrineBlock],
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Dict[str, Any]:
        """Generate response from triggered doctrine blocks"""
        reasoning_chain = []

        # Build response based on mode
        if mode == ResponseMode.FAST:
            # Concise summary
            text_parts = []
            for doctrine in doctrines:
                text_parts.extend(doctrine.conclusion_template)
                reasoning_chain.append(f"Applied doctrine: {doctrine.topic}")

            response_text = " ".join(text_parts[:3])  # First 3 conclusions
            confidence = doctrines[0].confidence

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready with citations
            text_parts = ["TRIBOLOGY ANALYSIS:\n"]
            for doctrine in doctrines:
                text_parts.append(f"\n{doctrine.topic}:")
                text_parts.extend(doctrine.conclusion_template)
                text_parts.append("\nKey Factors:")
                text_parts.extend([f"  - {factor}" for factor in doctrine.key_factors[:5]])
                text_parts.append("\nAuthority:")
                text_parts.extend([f"  - {auth}" for auth in doctrine.primary_authority])
                reasoning_chain.append(f"Doctrine: {doctrine.topic} | Authority: {doctrine.controlling_precedent}")

            response_text = "\n".join(text_parts)
            confidence = self._aggregate_confidence([d.confidence for d in doctrines])

        else:  # MEMO mode
            # Full documentation
            text_parts = [f"MEMORANDUM: Tribology Analysis - {query}\n"]
            text_parts.append(f"Analysis Zone: {zone.value}\n")

            for i, doctrine in enumerate(doctrines, 1):
                text_parts.append(f"\n{'='*60}")
                text_parts.append(f"DOCTRINE {i}: {doctrine.topic}")
                text_parts.append(f"{'='*60}\n")

                text_parts.append("CONCLUSION:")
                text_parts.extend([f"  {c}" for c in doctrine.conclusion_template])

                text_parts.append("\nREASONING FRAMEWORK:")
                text_parts.extend([f"  {line}" for line in doctrine.reasoning_framework[:30]])

                text_parts.append("\nKEY FACTORS:")
                text_parts.extend([f"  - {factor}" for factor in doctrine.key_factors])

                text_parts.append("\nPRIMARY AUTHORITY:")
                text_parts.extend([f"  - {auth}" for auth in doctrine.primary_authority])

                text_parts.append(f"\nCONFIDENCE: {doctrine.confidence.value}")
                text_parts.append(f"STRATIFICATION: {doctrine.confidence_stratification}")

                reasoning_chain.append(
                    f"Doctrine: {doctrine.topic} | "
                    f"Confidence: {doctrine.confidence.value} | "
                    f"Precedent: {doctrine.controlling_precedent}"
                )

            text_parts.append(f"\n{'='*60}")
            text_parts.append("OVERALL ASSESSMENT:")
            text_parts.append(f"  Triggered Doctrines: {len(doctrines)}")
            text_parts.append(f"  Aggregate Confidence: {self._aggregate_confidence([d.confidence for d in doctrines]).value}")

            response_text = "\n".join(text_parts)
            confidence = self._aggregate_confidence([d.confidence for d in doctrines])

        return {
            "text": response_text,
            "confidence": confidence,
            "reasoning_chain": reasoning_chain
        }

    def _semantic_search(self, query: str) -> Optional[List[str]]:
        """Semantic search fallback (simplified - would use vector DB)"""
        # In production, this would query a vector database
        # For now, return None to fall through to deep analysis
        return None

    def _generate_from_semantic(
        self,
        results: List[str],
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Dict[str, Any]:
        """Generate response from semantic search results"""
        return {
            "response": "Semantic search results (placeholder)",
            "confidence": ConfidenceLevel.DISCLOSURE,
            "doctrines_applied": [],
            "reasoning_chain": ["Semantic retrieval layer"],
            "layer": "SEMANTIC_RETRIEVAL"
        }

    def _deep_analysis(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Dict[str, Any]:
        """Deep analysis fallback when cache misses"""
        epistemic_gap = f"No specific doctrine found for: {query}"
        self.coverage_stats.epistemic_gaps.append(epistemic_gap)

        response_text = (
            f"DEEP ANALYSIS MODE:\n\n"
            f"Query: {query}\n"
            f"Zone: {zone.value}\n\n"
            f"No pre-compiled doctrine blocks matched this query. "
            f"This represents an epistemic gap in the current knowledge base. "
            f"Recommendation: Consult tribology references (ASM Handbook Vol 18, "
            f"Hutchings & Shipway 'Tribology', Hamrock 'Fundamentals of Fluid Film Lubrication') "
            f"or domain experts for this specific analysis.\n\n"
            f"General tribology principles to consider:\n"
            f"  - Lubrication regime (boundary/mixed/hydrodynamic)\n"
            f"  - Stribeck curve analysis\n"
            f"  - Wear mechanisms (adhesive, abrasive, erosive, corrosive, fatigue)\n"
            f"  - Surface engineering options (nitriding, PVD, DLC)\n"
            f"  - Lubricant selection (base oil group, additives, viscosity)\n"
            f"  - Film thickness calculations (Reynolds equation for hydrodynamic, Hamrock-Dowson for EHL)\n"
            f"  - Oil analysis trending (wear metals, particle count, viscosity, TAN/TBN)"
        )

        return {
            "response": response_text,
            "confidence": ConfidenceLevel.DISCLOSURE,
            "doctrines_applied": [],
            "reasoning_chain": ["Deep analysis - epistemic gap identified"],
            "layer": "DEEP_ANALYSIS"
        }

    def _aggregate_confidence(self, confidences: List[ConfidenceLevel]) -> ConfidenceLevel:
        """Aggregate confidence from multiple doctrines"""
        if not confidences:
            return ConfidenceLevel.DISCLOSURE

        # Use most conservative confidence level
        confidence_order = [
            ConfidenceLevel.HIGH_RISK,
            ConfidenceLevel.DISCLOSURE,
            ConfidenceLevel.AGGRESSIVE,
            ConfidenceLevel.DEFENSIBLE
        ]

        for level in confidence_order:
            if level in confidences:
                return level

        return ConfidenceLevel.DEFENSIBLE

    def _record_telemetry(
        self,
        query_id: str,
        mode: ResponseMode,
        latency_ms: float,
        cache_hit: bool,
        doctrines: List[DoctrineBlock]
    ):
        """Record query telemetry"""
        record = TelemetryRecord(
            query_id=query_id,
            timestamp=datetime.now(),
            mode=mode,
            latency_ms=latency_ms,
            cache_hit=cache_hit,
            doctrines_triggered=[d.topic for d in doctrines],
            confidence=doctrines[0].confidence if doctrines else ConfidenceLevel.DISCLOSURE
        )
        self.telemetry_records.append(record)
        self.total_queries += 1

        # Write to audit trail
        self._write_audit_trail(record)

    def _write_audit_trail(self, record: TelemetryRecord):
        """Append to JSONL audit trail"""
        audit_entry = {
            "query_id": record.query_id,
            "timestamp": record.timestamp.isoformat(),
            "mode": record.mode.value,
            "latency_ms": record.latency_ms,
            "cache_hit": record.cache_hit,
            "doctrines_triggered": record.doctrines_triggered,
            "confidence": record.confidence.value
        }

        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(audit_entry) + "\n")

    def get_health(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        uptime_seconds = (datetime.now() - self.start_time).total_seconds()

        cache_hit_rate = 0.0
        avg_latency_ms = 0.0
        if self.telemetry_records:
            cache_hits = sum(1 for r in self.telemetry_records if r.cache_hit)
            cache_hit_rate = cache_hits / len(self.telemetry_records)
            avg_latency_ms = sum(r.latency_ms for r in self.telemetry_records) / len(self.telemetry_records)

        return {
            "status": "healthy",
            "engine": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "port": PORT,
            "doctrine_count": len(self.doctrine_cache),
            "uptime_seconds": uptime_seconds,
            "total_queries": self.total_queries,
            "cache_hit_rate": cache_hit_rate,
            "avg_latency_ms": avg_latency_ms,
            "triggered_doctrines": len(self.coverage_stats.triggered_doctrines),
            "missed_doctrines": len(self.coverage_stats.missed_doctrines),
            "epistemic_gaps": len(self.coverage_stats.epistemic_gaps)
        }

    def calculate_determinism_hash(self, query: str, response: str) -> str:
        """SHA-256 hash for response reproducibility"""
        content = f"{query}|{response}|{ENGINE_VERSION}"
        return hashlib.sha256(content.encode()).hexdigest()

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=f"{ENGINE_NAME} - Tribology and Lubrication Intelligence",
    version=ENGINE_VERSION,
    description="TIE-grade expert system for friction, wear, lubrication, and surface engineering analysis"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
engine = MECH13TribologyEngine()

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with three-layer response"""
    try:
        result = engine.three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone
        )

        determinism_hash = engine.calculate_determinism_hash(
            request.query,
            result["response"]
        )

        telemetry = None
        if request.include_telemetry:
            telemetry = {
                "layer": result.get("layer", "UNKNOWN"),
                "latency_ms": result.get("latency_ms", 0.0),
                "cache_hit": len(result["doctrines_applied"]) > 0
            }

        return QueryResponse(
            response=result["response"],
            confidence=result["confidence"],
            doctrines_applied=result["doctrines_applied"],
            reasoning_chain=result["reasoning_chain"],
            telemetry=telemetry,
            determinism_hash=determinism_hash,
            timestamp=datetime.now()
        )

    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Comprehensive health check"""
    health = engine.get_health()
    return HealthResponse(**health)

@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total_doctrines": len(engine.doctrine_cache),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "category": d.topic.split(" - ")[0] if " - " in d.topic else "General"
            }
            for d in engine.doctrine_cache
        ]
    }

@app.get("/coverage")
async def coverage_stats():
    """Doctrine coverage statistics"""
    return {
        "triggered_doctrines": list(engine.coverage_stats.triggered_doctrines),
        "missed_doctrines": list(engine.coverage_stats.missed_doctrines),
        "epistemic_gaps": engine.coverage_stats.epistemic_gaps,
        "coverage_rate": len(engine.coverage_stats.triggered_doctrines) / len(engine.doctrine_cache)
    }

@app.get("/telemetry")
async def telemetry_summary():
    """Performance telemetry summary"""
    if not engine.telemetry_records:
        return {"message": "No queries processed yet"}

    records = engine.telemetry_records

    mode_breakdown = {}
    for mode in ResponseMode:
        mode_records = [r for r in records if r.mode == mode]
        if mode_records:
            mode_breakdown[mode.value] = {
                "count": len(mode_records),
                "avg_latency_ms": sum(r.latency_ms for r in mode_records) / len(mode_records),
                "cache_hit_rate": sum(1 for r in mode_records if r.cache_hit) / len(mode_records)
            }

    return {
        "total_queries": len(records),
        "overall_cache_hit_rate": sum(1 for r in records if r.cache_hit) / len(records),
        "overall_avg_latency_ms": sum(r.latency_ms for r in records) / len(records),
        "mode_breakdown": mode_breakdown
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {PORT}")
    logger.info(f"Doctrine blocks loaded: {len(DOCTRINE_CACHE)}")
    logger.info(f"Audit trail: {LOG_FILE}")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
