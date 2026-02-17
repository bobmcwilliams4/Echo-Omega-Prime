"""
FRAC01 - Hydraulic Fracturing Design Engine
TIE Gold Standard Implementation

Provides expert-level hydraulic fracturing design analysis including:
- Frac design fundamentals (net pressure, closure stress, ISIP)
- Fracture geometry models (PKN, KGD, radial, pseudo-3D)
- Treatment scheduling and pump rate optimization
- Formation stress profiling and mini-frac/DFIT analysis
- Fracture height containment and conductivity calculations
- Multi-stage completion design (plug-and-perf vs sliding sleeve)
- Permian Basin-specific frac designs
- Frac hit mitigation and stress shadowing analysis
- Real-time frac monitoring and pressure interpretation

Port: 9021
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Literal
from enum import Enum
from dataclasses import dataclass, field, asdict
from collections import defaultdict

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

ENGINE_ID = "FRAC01"
ENGINE_NAME = "Hydraulic Fracturing Design Engine"
VERSION = "1.0.0"
PORT = 9021

logger.add(
    f"logs/{ENGINE_ID}_{{time}}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
)


# ═══════════════════════════════════════════════════════════════════════════
# ENUMS AND DATA CLASSES
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


class IssueCategory(str, Enum):
    FRAC_DESIGN = "FRAC_DESIGN"
    GEOMETRY_MODEL = "GEOMETRY_MODEL"
    TREATMENT_SCHEDULE = "TREATMENT_SCHEDULE"
    STRESS_PROFILING = "STRESS_PROFILING"
    CONDUCTIVITY = "CONDUCTIVITY"
    COMPLETION_TYPE = "COMPLETION_TYPE"
    BASIN_SPECIFIC = "BASIN_SPECIFIC"
    FRAC_HIT = "FRAC_HIT"
    MONITORING = "MONITORING"
    CONTAINMENT = "CONTAINMENT"
    DIVERSION = "DIVERSION"
    PRESSURE_ANALYSIS = "PRESSURE_ANALYSIS"


@dataclass
class DoctrineBlock:
    """Represents a single doctrine block with expert reasoning."""
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
    controlling_precedent: List[str]
    category: IssueCategory
    issue_strata: List[str] = field(default_factory=list)


@dataclass
class QueryContext:
    """Context for query processing."""
    query: str
    mode: ResponseMode
    issue_categories: List[IssueCategory]
    triggered_doctrines: List[str]
    confidence_level: ConfidenceLevel
    timestamp: str
    session_id: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    query: str = Field(..., description="Hydraulic fracturing design question")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response mode")
    session_id: Optional[str] = Field(None, description="Session identifier")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class QueryResponse(BaseModel):
    response: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    issue_categories: List[str]
    reasoning_chain: Optional[List[str]] = None
    determinism_hash: str
    latency_ms: float
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float


# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Frac Design Fundamentals - Net Pressure and Closure Stress",
        keywords=["net pressure", "closure stress", "ISIP", "instantaneous shut-in pressure", "pnet", "formation closure"],
        conclusion_template=[
            "Net pressure (Pnet) is the treating pressure minus closure stress, representing the pressure expanding the fracture.",
            "Closure stress is the minimum principal stress (typically horizontal in most basins), determined from ISIP after shut-in.",
            "Accurate closure stress determination is critical for fracture geometry modeling and treatment design."
        ],
        reasoning_framework="""
Net pressure analysis requires:
1. Real-time treating pressure monitoring at perforations (correct for hydrostatic and friction)
2. ISIP identification from pressure decline after shut-in (first inflection point or G-function derivative)
3. Net pressure calculation: Pnet = Ptreating - Pclosure
4. Higher net pressure indicates wider fractures, lower net pressure indicates longer fractures
5. Excessive net pressure risks height growth, low net pressure risks screenout
6. Mini-frac tests provide closure stress before main treatment
7. Pressure-dependent leakoff (PDL) affects net pressure interpretation
8. Stress shadowing from adjacent stages alters local closure stress
9. Poroelastic effects can create apparent stress increases near fractures
10. Temperature effects on fluid rheology alter friction, affecting apparent net pressure
        """,
        key_factors=[
            "ISIP determination methodology (G-function, square-root time, log-log diagnostic)",
            "Fracture height containment vs stress barriers",
            "Poroelastic stress alterations from depletion",
            "Friction pressure corrections (tubing, perforations, near-wellbore tortuosity)",
            "Fluid leakoff rate affecting pressure decline shape",
            "Real-time adjustments to pump rate based on net pressure trends"
        ],
        primary_authority=[
            "SPE 179164 - Net Pressure Analysis in Unconventional Reservoirs",
            "Nolte KG (1979) - Determination of Fracture Parameters from Fracturing Pressure Decline",
            "SPE 107877 - Fracture Closure Stress: Reexamination of Field Data"
        ],
        burden_holder="Operator must demonstrate accurate closure stress determination to justify fracture geometry predictions",
        adversary_position="Conservative models assume higher closure stress, leading to narrower fracture width estimates and lower conductivity",
        counter_arguments=[
            "ISIP may not equal true closure if near-wellbore restrictions exist",
            "Pressure-dependent leakoff can mask true closure signature",
            "Multiple fractures opening simultaneously alter pressure decline",
            "Wellbore storage effects can obscure early-time closure signals",
            "Poroelastic stress changes from fluid injection shift local closure stress"
        ],
        resolution_strategy="Use multiple analysis methods (G-function, square-root time, Nolte's method) for closure stress confirmation; calibrate with diagnostic fracture injection tests (DFITs) before main treatment",
        entity_scope="Applies to all hydraulic fracturing operations; critical for unconventional shale completions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when mini-frac or DFIT data available; moderate confidence from main treatment ISIP alone",
        controlling_precedent=[
            "Industry standard: ISIP = closure stress in absence of near-wellbore restrictions",
            "SPE best practices recommend pre-treatment DFITs for closure stress calibration"
        ],
        category=IssueCategory.FRAC_DESIGN,
        issue_strata=["pressure analysis", "fracture mechanics", "geomechanics"]
    ),

    DoctrineBlock(
        topic="PKN vs KGD Fracture Geometry Models",
        keywords=["PKN", "KGD", "fracture geometry", "radial fracture", "pseudo-3D", "fracture width", "fracture length"],
        conclusion_template=[
            "PKN (Perkins-Kern-Nordgren) assumes fracture height is constant and small relative to length; suitable for confined fractures.",
            "KGD (Khristianovic-Geertsma-de Klerk) assumes plane strain, constant height, and width varies along length; better for long fractures.",
            "Pseudo-3D models account for height growth and variable stress barriers, more realistic for unconventional completions."
        ],
        reasoning_framework="""
Model selection depends on:
1. PKN: Height << Length, stress barriers confine fracture vertically
   - Width proportional to (net pressure)^0.25, length to (volume)^0.6
   - Suitable for thin pay zones with strong barriers
2. KGD: Plane strain, fracture height ~ fracture length
   - Width proportional to (net pressure)^0.5, length to (volume)^0.8
   - Suitable for tall fractures or vertical wells
3. Pseudo-3D: Allows height growth, variable stress profiles
   - Numerically solves for width/length/height simultaneously
   - Accounts for stress contrasts in multilayer formations
4. Radial fracture: Circular geometry for very short treatments
5. Modern unconventional completions typically use pseudo-3D or planar 3D simulators
6. Model choice affects proppant transport, conductivity, and production forecasts
7. Calibration with microseismic or tiltmeter data validates model selection
8. Complex fracture models (discrete fracture networks) for natural fracture systems
        """,
        key_factors=[
            "Fracture height relative to length",
            "Stress barrier strength (vertical stress contrast)",
            "Fluid leakoff coefficient",
            "Proppant transport requirements",
            "Formation layering and heterogeneity",
            "Computational resources for real-time optimization"
        ],
        primary_authority=[
            "Perkins TK, Kern LR (1961) - Widths of Hydraulic Fractures",
            "Nordgren RP (1972) - Propagation of a Vertical Hydraulic Fracture",
            "SPE 166506 - Comparison of Fracture Geometry Models"
        ],
        burden_holder="Engineer must justify model selection based on reservoir geometry and stress profile",
        adversary_position="Simplified models (PKN/KGD) may overestimate fracture length, underestimate width",
        counter_arguments=[
            "PKN/KGD do not account for height growth",
            "Pseudo-3D requires detailed stress log data often unavailable",
            "Model calibration requires expensive diagnostics (microseismic, DAS)",
            "Natural fractures invalidate continuum models",
            "Proppant bridging and tip screenout not captured in simple models"
        ],
        resolution_strategy="Use pseudo-3D for design, validate with field diagnostics; PKN/KGD acceptable for screening calculations",
        entity_scope="All hydraulic fracturing operations; model sophistication scales with well cost and data availability",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with calibrated pseudo-3D; moderate with uncalibrated PKN/KGD",
        controlling_precedent=[
            "Industry trend: Pseudo-3D models standard for unconventional completions",
            "Operators with extensive datasets use fully 3D planar simulators"
        ],
        category=IssueCategory.GEOMETRY_MODEL,
        issue_strata=["fracture mechanics", "reservoir engineering", "numerical modeling"]
    ),

    DoctrineBlock(
        topic="Treatment Scheduling - Pad, Slurry Stages, Flush",
        keywords=["pad volume", "slurry stages", "proppant schedule", "flush volume", "proppant ramp", "stage design"],
        conclusion_template=[
            "Pad fluid creates fracture width and length before proppant introduction, preventing early screenout.",
            "Slurry stages incrementally increase proppant concentration to maximum designed value, balancing placement and conductivity.",
            "Flush ensures proppant clears wellbore and perforations, preventing plugging and enabling intervention access."
        ],
        reasoning_framework="""
Treatment schedule design:
1. Pad stage: 10-30% of total fluid volume (higher for low-perm formations)
   - Creates fracture geometry, reduces net pressure before proppant
   - Excessive pad wastes fluid, insufficient pad causes premature screenout
2. Proppant ramp: Gradual concentration increase (0.5 → 2.0+ ppg)
   - Step increases (0.25-0.5 ppg increments) allow monitoring for screenout
   - Aggressive ramps risk bridging, conservative ramps waste pumping time
3. Maximum proppant concentration: 2.0-3.0 ppg (slickwater), up to 8 ppg (crosslinked gel)
   - Limited by proppant transport capacity and friction pressure
   - Higher concentration increases conductivity but risks screenout
4. Flush stage: Displace proppant from wellbore
   - Volume = wellbore volume + perforation volume + safety margin
   - Insufficient flush leaves proppant in wellbore, preventing wireline/CT access
5. Stage sequencing for multi-stage completions
6. Real-time adjustments based on treating pressure response
        """,
        key_factors=[
            "Formation permeability (lower perm = larger pad)",
            "Fracture complexity (natural fractures increase leakoff, require more pad)",
            "Proppant transport fluid efficiency",
            "Maximum allowable treating pressure",
            "Operational constraints (pump rate, proppant blender capacity)",
            "Post-frac intervention plans (wireline, CT)"
        ],
        primary_authority=[
            "SPE 102227 - Optimizing Fracture Treatment Design",
            "Economides MJ, Nolte KG (2000) - Reservoir Stimulation, 3rd Ed",
            "SPE 119900 - Slickwater Fracturing in the Barnett Shale"
        ],
        burden_holder="Operator must demonstrate treatment schedule achieves proppant placement without screenout",
        adversary_position="Conservative schedules with large pad and slow ramp waste time and fluid",
        counter_arguments=[
            "Excessive pad increases cost without improving conductivity",
            "Aggressive proppant ramps increase screenout risk",
            "Flush volume estimates may be inaccurate with complex wellbore geometry",
            "Real-time adjustments require experienced on-site engineer",
            "Proppant settling in horizontal wellbores complicates flush design"
        ],
        resolution_strategy="Design conservative initial schedule, use real-time monitoring to optimize subsequent stages",
        entity_scope="All proppant fracturing operations; slickwater vs gel affects proppant transport",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with analog well data; moderate confidence for first well in area",
        controlling_precedent=[
            "Unconventional completions: 15-25% pad, 0.5→2.0 ppg ramp standard",
            "Real-time optimization standard practice for large treatments"
        ],
        category=IssueCategory.TREATMENT_SCHEDULE,
        issue_strata=["completion design", "operational execution", "proppant transport"]
    ),

    DoctrineBlock(
        topic="Pump Rate Optimization for Fracture Geometry",
        keywords=["pump rate", "injection rate", "fracture width", "friction pressure", "limited entry", "rate step-up"],
        conclusion_template=[
            "Higher pump rates increase fracture width (more conductivity) but risk height growth and friction limits.",
            "Optimal pump rate balances fracture geometry objectives with surface pressure constraints and formation response.",
            "Rate step-up/step-down tests diagnose near-wellbore restrictions and calibrate friction models."
        ],
        reasoning_framework="""
Pump rate selection:
1. Higher rate benefits:
   - Increased fracture width (width ∝ rate^0.25 to 0.5 depending on model)
   - Better proppant transport in slickwater
   - Reduced treatment time (lower cost)
2. Higher rate risks:
   - Excessive height growth if insufficient stress barriers
   - Surface pressure limits (pump capacity, tubular ratings)
   - Near-wellbore friction and tortuosity pressure drop
   - Wellbore storage effects masking fracture response
3. Rate optimization:
   - Start with formation injectivity test (step-rate test)
   - Typical unconventional rates: 60-100 bpm (Permian), 80-120 bpm (Eagle Ford)
   - Limited entry design distributes flow across perforations
4. Rate step-up/step-down diagnostics:
   - Pressure response to rate changes reveals friction vs fracture extension
   - Near-wellbore tortuosity identified by nonlinear pressure-rate relationship
5. Real-time rate adjustments based on net pressure trends
        """,
        key_factors=[
            "Formation breakdown pressure and fracture gradient",
            "Stress barriers and height containment",
            "Surface equipment capacity (HHP available)",
            "Tubular pressure ratings (casing, tubing, wellhead)",
            "Perforation design (limited entry requires higher rate)",
            "Fluid rheology and friction reducer efficiency"
        ],
        primary_authority=[
            "SPE 115769 - Rate Effects on Fracture Geometry",
            "Nolte KG (1988) - Principles for Fracture Design Based on Pressure Analysis",
            "SPE 152596 - Limited Entry Design for Improved Distribution"
        ],
        burden_holder="Engineer must demonstrate rate selection achieves design fracture geometry within operational limits",
        adversary_position="Aggressive high-rate designs risk uncontrolled height growth and equipment failure",
        counter_arguments=[
            "Higher rates increase friction, reducing net pressure available for fracture width",
            "Rate-dependent leakoff can dominate fracture growth at very high rates",
            "Equipment limitations may prevent optimal rate",
            "Near-wellbore complexity can cause pressure spikes independent of rate",
            "Excessive rate in naturally fractured formations causes uncontrolled fracture complexity"
        ],
        resolution_strategy="Use step-rate testing to establish safe operating envelope; start conservative, increase if pressure response favorable",
        entity_scope="All fracturing operations; particularly critical for limited entry and multi-cluster designs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with step-rate test data; moderate confidence from offset well analogs",
        controlling_precedent=[
            "Industry standard: Rate selected to achieve target width while maintaining surface pressure <10,000 psi",
            "Limited entry designs require sufficient rate to achieve uniform distribution"
        ],
        category=IssueCategory.FRAC_DESIGN,
        issue_strata=["hydraulic design", "operational limits", "equipment capacity"]
    ),

    DoctrineBlock(
        topic="Formation Stress Profiling - Mini-Frac and DFIT Analysis",
        keywords=["mini-frac", "DFIT", "diagnostic fracture injection test", "closure stress", "leakoff coefficient", "G-function"],
        conclusion_template=[
            "Mini-frac tests inject small fluid volumes to determine closure stress, leakoff, and fracture geometry before main treatment.",
            "DFIT (Diagnostic Fracture Injection Test) provides detailed formation characterization including stress, permeability, and compliance.",
            "Accurate pre-treatment testing reduces main treatment risk and enables design optimization."
        ],
        reasoning_framework="""
Mini-frac/DFIT workflow:
1. Inject small volume (5-20 bbl) at low rate
2. Shut in and monitor pressure decline
3. Analysis methods:
   - G-function (dimensionless time) identifies closure
   - Square-root time plot for early-time leakoff
   - Log-log diagnostic for flow regimes
   - After-closure analysis (ACA) for permeability
4. Closure stress determination:
   - First deviation from linear G-function trend
   - Inflection point in pressure vs time
   - End of linear flow in log-log diagnostic
5. Leakoff coefficient from decline slope
6. Fracture compliance from pressure-dependent closure
7. Use results to calibrate main treatment design
8. Multiple DFITs in multi-zone completions characterize each interval
        """,
        key_factors=[
            "Injection volume sufficient to overcome wellbore storage",
            "Shut-in duration long enough to observe closure (typically 2-4x injection time)",
            "Pressure gauge resolution and accuracy",
            "Near-wellbore storage effects",
            "Formation heterogeneity affecting closure signature",
            "Poroelastic effects in low-permeability formations"
        ],
        primary_authority=[
            "SPE 107877 - Modern Fracture Pressure Analysis",
            "Barree RD, Mukherjee H (1996) - Determination of Pressure-Dependent Leakoff",
            "SPE 179725 - DFIT Analysis in Unconventional Reservoirs"
        ],
        burden_holder="Operator should conduct DFIT to characterize formation before large expenditure on main treatment",
        adversary_position="Mini-frac costs and time may not be justified if analog data exists",
        counter_arguments=[
            "Wellbore storage can obscure true closure signal",
            "Multiple fractures may open, complicating analysis",
            "Pressure gauges may lack resolution for subtle closure signature",
            "Formation heterogeneity makes single-point test non-representative",
            "Time and cost of testing vs incremental design improvement"
        ],
        resolution_strategy="Conduct DFIT on first well in new area, use results to optimize subsequent wells; skip if robust analog data exists",
        entity_scope="Recommended for all new field developments; critical for deep, high-pressure reservoirs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with well-executed DFIT; low confidence without pre-treatment testing",
        controlling_precedent=[
            "Best practice: DFIT before first frac in new field",
            "Regulatory agencies may require stress testing in sensitive areas (seismicity, aquifer protection)"
        ],
        category=IssueCategory.STRESS_PROFILING,
        issue_strata=["geomechanics", "formation characterization", "design optimization"]
    ),

    DoctrineBlock(
        topic="Fracture Height Containment and Stress Barriers",
        keywords=["height growth", "stress barriers", "containment", "vertical migration", "caprock", "shale barriers"],
        conclusion_template=[
            "Fracture height containment requires sufficient stress contrast in bounding layers to prevent vertical migration.",
            "Stress barriers >500 psi typically provide strong containment; <200 psi allows height growth.",
            "Uncontrolled height growth risks aquifer contamination, gas migration, and reduced proppant concentration in pay zone."
        ],
        reasoning_framework="""
Height containment analysis:
1. Stress barrier strength = (σv_barrier - σv_pay)
   - Strong barrier: >500 psi contrast
   - Moderate: 200-500 psi
   - Weak: <200 psi (height growth likely)
2. Factors promoting height growth:
   - High net pressure (excessive rate or viscous fluid)
   - Weak stress barriers (similar rock properties)
   - Natural fractures bridging barriers
   - Thin pay zones relative to fracture length
3. Containment strategies:
   - Limit net pressure (reduce rate, use low-viscosity fluid)
   - Stage placement away from barrier-poor zones
   - Diverting agents to force lateral growth
4. Consequences of height growth:
   - Reduced proppant concentration in pay zone
   - Potential aquifer communication
   - Gas/water migration from non-pay zones
5. Detection methods:
   - Microseismic mapping shows vertical extent
   - Temperature logs identify fractured intervals
   - Pressure buildup in monitoring wells
        """,
        key_factors=[
            "Vertical stress profile from logs or correlation",
            "Young's modulus contrast (stiff barriers resist fracture)",
            "Natural fracture orientation and density",
            "Net pressure during treatment",
            "Regulatory constraints (aquifer protection zones)",
            "Reservoir architecture (pay zone thickness, barrier continuity)"
        ],
        primary_authority=[
            "SPE 98107 - Height Containment in Layered Formations",
            "Warpinski NR (1985) - Measurement of Width and Pressure in a Propagating Hydraulic Fracture",
            "SPE 119890 - Microseismic Evidence of Height Containment"
        ],
        burden_holder="Operator must demonstrate fracture height stays within permitted zones (environmental regulations)",
        adversary_position="Conservative designs with low net pressure sacrifice conductivity to ensure containment",
        counter_arguments=[
            "Stress barriers may be locally absent (faulting, erosion)",
            "Natural fractures can bypass stress barriers",
            "Microseismic detects shear, not just fracture extent",
            "Net pressure control difficult in real-time",
            "Height growth may be acceptable if non-pay zones are non-producing but hydrocarbon-bearing"
        ],
        resolution_strategy="Design for containment in sensitive areas (aquifers); tolerate moderate height growth in thick hydrocarbon columns; validate with microseismic",
        entity_scope="All hydraulic fracturing; critical near aquifers, in shallow formations, and in regulatory-sensitive areas",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with strong stress barriers (>500 psi); disclosure required for weak barriers",
        controlling_precedent=[
            "EPA guidelines: Demonstrate no aquifer communication via fracture height modeling",
            "State regulations (TX RRC, NM OCD) require barrier assessment for permits"
        ],
        category=IssueCategory.CONTAINMENT,
        issue_strata=["geomechanics", "environmental protection", "regulatory compliance"]
    ),

    DoctrineBlock(
        topic="Fracture Conductivity Calculations and Proppant Pack Permeability",
        keywords=["conductivity", "proppant pack", "permeability", "width", "kw", "dimensionless conductivity", "proppant crush"],
        conclusion_template=[
            "Fracture conductivity (kf·wf) is the product of proppant pack permeability and propped fracture width.",
            "Dimensionless conductivity (FCD) > 1.0 indicates fracture dominates flow; < 0.1 suggests fracture ineffective.",
            "Proppant selection, concentration, and placement control achieved conductivity."
        ],
        reasoning_framework="""
Conductivity fundamentals:
1. Conductivity definition: C = kf × wf (md-ft)
   - kf = proppant pack permeability (md)
   - wf = propped fracture width (ft)
2. Dimensionless conductivity: FCD = (kf·wf) / (k·Lf)
   - k = reservoir permeability
   - Lf = fracture half-length
   - FCD > 10: infinite conductivity (fracture offers no flow resistance)
   - FCD = 1-10: finite conductivity (moderate fracture resistance)
   - FCD < 1: fracture adds significant flow resistance
3. Proppant pack permeability:
   - Depends on proppant size, roundness, sorting
   - 20/40 mesh: 50,000-150,000 md (unconfined)
   - 100 mesh: 5,000-15,000 md
   - Stress-dependent: permeability reduces with closure stress
   - Proppant crush at high stress reduces permeability
4. Propped width:
   - Width = (proppant volume) / (fracture area × proppant porosity)
   - Typical: 0.01-0.05 ft (slickwater), 0.05-0.2 ft (gel)
5. Maximizing conductivity:
   - Higher proppant concentration (more volume)
   - Larger mesh size (higher permeability)
   - High-strength proppant (ceramic, resin-coated)
   - Wider fractures (higher rate, viscous fluid)
        """,
        key_factors=[
            "Proppant type (sand, ceramic, resin-coated)",
            "Proppant size distribution (mesh)",
            "Closure stress (determines crush and embedment)",
            "Proppant concentration and placement efficiency",
            "Formation embedment (soft formations reduce effective width)",
            "Non-Darcy flow effects at high velocity"
        ],
        primary_authority=[
            "SPE 84306 - Realistic Assessment of Proppant Pack Conductivity",
            "API RP 19D - Measuring Proppant Pack Conductivity",
            "SPE 171649 - Conductivity Loss Mechanisms in Fractures"
        ],
        burden_holder="Engineer must justify proppant selection achieves required conductivity at in-situ stress",
        adversary_position="Lab-measured conductivity overstates field performance due to non-Darcy effects, gel damage, fines",
        counter_arguments=[
            "API conductivity tests use clean conditions, field has gel residue and formation fines",
            "Proppant crushing and embedment reduce width over time",
            "Multiphase flow (oil, gas, water) reduces effective permeability",
            "Non-Darcy flow at high velocity reduces apparent conductivity",
            "Incomplete proppant placement (settling, flowback) leaves lower-than-designed concentration"
        ],
        resolution_strategy="Design for FCD > 1.0 using field-representative conductivity (API data derated by 50-70%); validate with production data",
        entity_scope="All proppant fracturing; conductivity critical for production in low-permeability unconventionals",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Moderate confidence due to lab-to-field translation uncertainty; production history provides validation",
        controlling_precedent=[
            "Industry trend: Design for FCD = 1-5 in unconventionals (balance conductivity and cost)",
            "High-conductivity designs (FCD > 10) used in high-perm conventional reservoirs"
        ],
        category=IssueCategory.CONDUCTIVITY,
        issue_strata=["reservoir engineering", "proppant selection", "production optimization"]
    ),

    DoctrineBlock(
        topic="Tip Screenout (TSO) Design for Maximum Proppant Placement",
        keywords=["tip screenout", "TSO", "proppant pack", "screenout", "bridging", "near-wellbore", "fracture tip"],
        conclusion_template=[
            "Tip screenout (TSO) intentionally bridges proppant at fracture tip to build wide, highly conductive pack near wellbore.",
            "TSO requires aggressive proppant ramping and precise pressure monitoring to avoid premature near-wellbore screenout.",
            "Successful TSO maximizes conductivity in critical near-wellbore region, improving productivity."
        ],
        reasoning_framework="""
TSO design principles:
1. Concept: Build proppant bridge at fracture tip, then pack behind it
   - Creates maximum width near wellbore (highest flow velocity region)
   - Sacrifices fracture length for conductivity
2. Execution:
   - Rapid proppant concentration ramp (e.g., 0→4 ppg in 10 minutes)
   - Monitor pressure for rapid rise indicating tip bridge
   - Continue pumping to pack proppant behind bridge
   - Controlled screenout (pressure rise 500-1500 psi)
3. Pressure signatures:
   - Gradual rise: Proppant reaching tip, not yet bridged
   - Rapid rise: Tip bridge formed, packing behind
   - Runaway rise: Near-wellbore bridge (abort, flush)
4. Advantages:
   - Maximum conductivity near wellbore
   - High proppant concentration in critical flow region
5. Risks:
   - Premature near-wellbore screenout (lost well)
   - Inability to place planned proppant volume
   - Difficulty diagnosing bridge location
6. Best applications:
   - Low-permeability reservoirs (FCD dominated by near-wellbore region)
   - Wells with severe near-wellbore damage
        """,
        key_factors=[
            "Proppant transport efficiency (must reach tip before bridging)",
            "Real-time pressure monitoring and interpretation",
            "Pump rate capability to continue after screenout",
            "Fracture geometry (longer fractures easier to screen at tip)",
            "Fluid rheology (slickwater difficult for controlled TSO)",
            "Experience of on-site frac engineer"
        ],
        primary_authority=[
            "SPE 39959 - Tip Screenout Fracturing: A Technique for Soft, Unstable Formations",
            "SPE 25892 - Design and Execution of Tip Screenout Treatments",
            "SPE 163990 - TSO in Unconventional Reservoirs"
        ],
        burden_holder="Operator must justify TSO approach provides better productivity than conventional design",
        adversary_position="TSO risks are high; conventional design safer and more predictable",
        counter_arguments=[
            "Premature near-wellbore screenout can lose well (costly sidetrack)",
            "Difficult to diagnose tip vs near-wellbore bridge in real-time",
            "Slickwater (common in unconventionals) poor proppant transport for TSO",
            "May not place full designed proppant volume",
            "Post-screenout cleanup difficult, may damage proppant pack"
        ],
        resolution_strategy="Use TSO selectively in wells with demonstrated near-wellbore damage or very low permeability; conventional design for most unconventionals",
        entity_scope="Applicable to conventional and unconventional; more common in conventional high-perm reservoirs",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="High risk technique; requires experienced engineer and real-time decision-making",
        controlling_precedent=[
            "Conventional TSO common in Gulf Coast soft formations",
            "Unconventional TSO rare; most operators prefer predictable placement"
        ],
        category=IssueCategory.FRAC_DESIGN,
        issue_strata=["advanced techniques", "proppant placement", "risk management"]
    ),

    DoctrineBlock(
        topic="Multi-Stage Completion Design - Plug-and-Perf vs Sliding Sleeve",
        keywords=["plug-and-perf", "sliding sleeve", "ball drop", "multi-stage", "completion efficiency", "coiled tubing"],
        conclusion_template=[
            "Plug-and-perf uses temporary bridge plugs and perforating guns to isolate and stimulate stages sequentially.",
            "Sliding sleeve systems use pre-installed sleeves opened by ball drops or shifting tools, eliminating wireline/CT.",
            "Plug-and-perf dominates unconventional completions due to flexibility; sliding sleeves offer speed advantages."
        ],
        reasoning_framework="""
Completion system comparison:
1. Plug-and-perf:
   - Set bridge plug above previous stage
   - Run perforating guns, shoot new stage
   - Pump frac treatment
   - Repeat for each stage (toe to heel)
   - Advantages: Unlimited stages, precise placement, optimize per stage
   - Disadvantages: Wireline time (1-2 hrs/stage), equipment risk, plug milling required
2. Sliding sleeve (ball-actuated):
   - Pre-installed sleeves in completion string
   - Drop sized balls to open sleeves sequentially
   - All sleeves isolated with packers
   - Advantages: Fast (no wireline), continuous pumping possible
   - Disadvantages: Limited stages (ball size progression), no flexibility, isolation risk
3. Sliding sleeve (coil tubing/wireline actuated):
   - Mechanically shift sleeves with CT or wireline tools
   - Advantages: More stages than ball-drop, can selectively treat
   - Disadvantages: CT/wireline time, shifting tool reliability
4. Industry trends:
   - Plug-and-perf: 80%+ of US unconventional completions
   - Sliding sleeve: Niche applications (very long laterals, offshore, re-fracs)
   - Hybrid: Limited entry plug-and-perf with cemented liners
        """,
        key_factors=[
            "Number of stages (sliding sleeve limited by ball sizes)",
            "Stage spacing flexibility",
            "Completion cost (wireline vs rig time)",
            "Operational risk (stuck tools, failed isolation)",
            "Re-fracturing potential (plug-and-perf easier)",
            "Wellbore trajectory and accessibility"
        ],
        primary_authority=[
            "SPE 152530 - Completion Technology Comparison in Shale Plays",
            "SPE 174782 - Plug-and-Perf Evolution in Unconventional Completions",
            "SPE 168638 - Sliding Sleeve Applications and Limitations"
        ],
        burden_holder="Operator must select completion system based on well design, stage count, and economic optimization",
        adversary_position="Sliding sleeve advocates cite wireline time and risk; plug-and-perf advocates cite flexibility",
        counter_arguments=[
            "Plug-and-perf wireline time adds 1-3 days to completion",
            "Sliding sleeve ball-drop limits stage count to ~15-20",
            "Plug-and-perf plug milling after completion adds cost",
            "Sliding sleeve isolation failures difficult to diagnose and repair",
            "Plug-and-perf allows real-time stage design optimization"
        ],
        resolution_strategy="Use plug-and-perf for flexibility and stage count; consider sliding sleeve for speed-critical applications with <15 stages",
        entity_scope="All multi-stage horizontal completions; selection varies by basin and operator preference",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in plug-and-perf reliability; moderate confidence in sliding sleeve isolation",
        controlling_precedent=[
            "Industry standard: Plug-and-perf for unconventional multi-stage (Permian, Eagle Ford, Bakken)",
            "Sliding sleeve use declining except in offshore and specific re-frac applications"
        ],
        category=IssueCategory.COMPLETION_TYPE,
        issue_strata=["completion design", "operational efficiency", "cost optimization"]
    ),

    DoctrineBlock(
        topic="Permian Basin Frac Designs - Wolfcamp, Bone Spring, Spraberry",
        keywords=["Permian Basin", "Wolfcamp", "Bone Spring", "Spraberry", "Delaware Basin", "Midland Basin", "slickwater", "hybrid frac"],
        conclusion_template=[
            "Permian Basin completions vary by formation: Wolfcamp uses high-intensity slickwater, Bone Spring uses hybrid fluids, Spraberry uses moderate-intensity designs.",
            "Delaware Basin (west) has deeper, higher-pressure reservoirs than Midland Basin (east).",
            "Proppant loading, stage spacing, and cluster count increase over time as operators optimize EUR."
        ],
        reasoning_framework="""
Permian completion characteristics:
1. Wolfcamp (Delaware and Midland):
   - Depth: 7,000-12,000 ft TVD
   - Slickwater dominant (100 mesh sand)
   - High cluster count: 6-10 clusters/stage
   - Tight stage spacing: 150-250 ft
   - Proppant: 1,500-3,000 lbs/ft
   - Total fluid: 50,000-100,000 bbl/well
2. Bone Spring (Delaware):
   - Depth: 8,000-11,000 ft
   - Hybrid fluid (slickwater + crosslinked gel)
   - Moderate cluster count: 4-6/stage
   - Stage spacing: 200-300 ft
   - Proppant: 1,200-2,000 lbs/ft
   - Higher conductivity focus than Wolfcamp
3. Spraberry (Midland):
   - Depth: 7,000-9,000 ft
   - Slickwater or hybrid
   - Cluster count: 4-6/stage
   - Stage spacing: 250-400 ft
   - Proppant: 1,000-1,800 lbs/ft
4. Basin differences:
   - Delaware: Deeper, higher pressure, thicker Wolfcamp stacks
   - Midland: Shallower, lower pressure, more developed infrastructure
5. Trends:
   - Increasing proppant intensity (2015: 500 lbs/ft → 2020: 2000+ lbs/ft)
   - Tighter stage spacing (2015: 400 ft → 2020: 200 ft)
   - More clusters per stage (2015: 3-4 → 2020: 6-10)
        """,
        key_factors=[
            "Formation depth and pressure",
            "Natural fracture intensity (Wolfcamp > Bone Spring > Spraberry)",
            "Proppant cost and logistics (West Texas infrastructure)",
            "Well spacing and parent-child interactions",
            "Operator strategy (EUR maximization vs NPV)",
            "Water availability and disposal capacity"
        ],
        primary_authority=[
            "SPE 187242 - Wolfcamp Completion Optimization in the Delaware Basin",
            "SPE 191775 - Parent-Child Well Interactions in the Permian",
            "URTeC 2901309 - Evolution of Permian Completions"
        ],
        burden_holder="Operator must adapt generic design to specific basin, formation, and well conditions",
        adversary_position="One-size-fits-all designs ignore formation-specific differences and waste capital",
        counter_arguments=[
            "High-intensity designs may not be economic at lower oil prices",
            "Parent-child well interactions reduce child well productivity regardless of completion intensity",
            "Natural fractures in Wolfcamp may short-circuit high cluster count designs",
            "Water sourcing and disposal costs vary by area",
            "Optimal design evolves as operators gain experience"
        ],
        resolution_strategy="Start with basin/formation analog, adjust based on local offset performance and economics",
        entity_scope="All Permian Basin unconventional completions; design varies by operator, basin, and formation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in established trends; moderate confidence in optimal design for new areas",
        controlling_precedent=[
            "Industry trend: High-intensity slickwater for Wolfcamp Delaware",
            "Operators publish case studies showing incremental EUR with design changes"
        ],
        category=IssueCategory.BASIN_SPECIFIC,
        issue_strata=["regional practices", "formation characteristics", "economic optimization"]
    ),

    DoctrineBlock(
        topic="Delaware Basin vs Midland Basin Frac Design Differences",
        keywords=["Delaware Basin", "Midland Basin", "Permian", "depth", "pressure", "completions", "infrastructure"],
        conclusion_template=[
            "Delaware Basin (west Permian) has deeper, higher-pressure reservoirs with thicker prospective intervals.",
            "Midland Basin (east Permian) has shallower, lower-pressure reservoirs with more developed infrastructure.",
            "Completion designs reflect basin differences: Delaware uses higher-intensity treatments, Midland uses more moderate designs."
        ],
        reasoning_framework="""
Basin comparison:
1. Delaware Basin:
   - Depth: 8,000-14,000 ft TVD (Wolfcamp, Bone Spring, Avalon)
   - Reservoir pressure: 0.6-0.8 psi/ft (overpressured in places)
   - Thick stacked pay: 1,000+ ft of Wolfcamp alone
   - Natural fractures: Moderate to high intensity
   - Completion intensity: 2,000-3,000 lbs/ft proppant
   - Stage spacing: 150-250 ft
   - Challenges: Deeper drilling, higher completion costs, less infrastructure
2. Midland Basin:
   - Depth: 7,000-10,000 ft TVD (Spraberry, Wolfcamp, Lower Clearfork)
   - Reservoir pressure: 0.45-0.6 psi/ft (normal to slightly overpressured)
   - Thinner individual zones, multiple stacked targets
   - Natural fractures: Low to moderate intensity
   - Completion intensity: 1,200-2,000 lbs/ft proppant
   - Stage spacing: 200-350 ft
   - Advantages: Shallower, lower cost, extensive infrastructure
3. Economic considerations:
   - Delaware: Higher upfront cost, larger EURs, longer payback
   - Midland: Lower cost, faster payback, more mature field development
4. Frac hit risk:
   - Both basins: Child well productivity impacted by parent depletion
   - Delaware: Thicker pay may reduce interference
        """,
        key_factors=[
            "Formation depth and pressure",
            "Prospective interval thickness",
            "Natural fracture density and orientation",
            "Infrastructure (pipelines, disposal, frac sand)",
            "Well spacing and development density",
            "Operator cost structure and risk tolerance"
        ],
        primary_authority=[
            "SPE 194345 - Delaware vs Midland Completion Comparison",
            "EIA Permian Basin Analysis (Annual)",
            "URTeC 123 - Regional Completion Trends"
        ],
        burden_holder="Operator must optimize design for basin-specific geology and economics",
        adversary_position="Basin generalizations oversimplify; intra-basin variability can exceed inter-basin differences",
        counter_arguments=[
            "Delaware and Midland both have significant internal variability",
            "Operator execution and well placement matter more than basin",
            "Proppant intensity trends converging between basins",
            "Infrastructure gap closing as Delaware develops",
            "Parent-child interactions similar in both basins"
        ],
        resolution_strategy="Use basin trends as starting point, refine with local offset data and operator-specific learnings",
        entity_scope="All Permian Basin operators; design selection critical for capital allocation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in general basin differences; moderate confidence in optimal design for specific location",
        controlling_precedent=[
            "Delaware Basin: Trend toward high-intensity completions (>2,500 lbs/ft)",
            "Midland Basin: Moderate intensity (1,500-2,000 lbs/ft) with tighter spacing"
        ],
        category=IssueCategory.BASIN_SPECIFIC,
        issue_strata=["regional geology", "economic drivers", "infrastructure"]
    ),

    DoctrineBlock(
        topic="Frac Hit Mitigation and Parent-Child Well Interactions",
        keywords=["frac hit", "parent-child", "well interference", "depletion", "pressure sink", "fracture-driven interactions", "FDI"],
        conclusion_template=[
            "Frac hits occur when child well fractures communicate with depleted parent wells, causing treatment diversion and child well underperformance.",
            "Mitigation strategies include parent well shut-in, re-pressurization, optimized spacing, and modified completion designs.",
            "Industry lacks consensus solution; frac hits remain major challenge in unconventional field development."
        ],
        reasoning_framework="""
Frac hit mechanisms:
1. Pressure depletion around parent creates preferential flow path
2. Child well fractures propagate toward low-pressure parent
3. Treatment fluid and proppant diverted away from target reservoir
4. Parent well may produce child's frac fluid (years of cleanup)
5. Child well EUR reduced 20-50% vs standalone well
Mitigation strategies:
1. Parent well management:
   - Shut in parent before child frac (months in advance)
   - Re-pressurize parent by injecting gas/water
   - Flowback parent during child frac to reduce pressure contrast
2. Well spacing optimization:
   - Increase spacing (600 ft → 800-1000 ft)
   - Stagger landing zones vertically
   - Optimize development sequence (simultaneous vs sequential)
3. Completion design:
   - Reduce child well stage count near parent
   - Lower pump rate to reduce fracture extent
   - Diverting agents to force away from parent
4. Monitoring:
   - Fiber optic (DAS/DTS) on parent to detect child frac arrivals
   - Pressure monitoring in parent during child frac
   - Microseismic to map fracture growth
Challenges:
- No universal solution; effectiveness varies by geology
- Parent re-pressurization difficult in low-perm unconventionals
- Spacing increases reduce well count per section (lower NPV)
        """,
        key_factors=[
            "Parent well depletion magnitude and extent",
            "Well spacing and relative positions",
            "Natural fracture connectivity",
            "Completion intensity (larger child fracs = more interference)",
            "Time lag between parent and child completions",
            "Formation permeability (lower perm = slower re-pressurization)"
        ],
        primary_authority=[
            "SPE 184876 - Parent-Child Well Relationships in Unconventionals",
            "URTeC 2019-263 - Frac Hit Mitigation Field Trial Results",
            "SPE 195912 - Economics of Well Spacing and Frac Hit Mitigation"
        ],
        burden_holder="Operator must balance child well performance vs development density to maximize asset value",
        adversary_position="Aggressive spacing (close wells) maximizes well count but destroys child well productivity",
        counter_arguments=[
            "Parent re-pressurization often ineffective in tight formations",
            "Increased spacing reduces wells per section, lowering total recovery",
            "Mitigation strategies add cost and complexity",
            "Frac hit severity varies unpredictably even with consistent operations",
            "Long-term effects uncertain (does parent recover after child cleanup?)"
        ],
        resolution_strategy="Pilot test mitigation strategies; adopt proven methods; adjust spacing based on economic optimization including child well degradation",
        entity_scope="All unconventional operators in infill development phase; critical for maximizing field-wide recovery",
        confidence=ConfidenceLevel.DISCLOSURE,
        confidence_stratification="High uncertainty; field results inconsistent; no industry-wide consensus on best practices",
        controlling_precedent=[
            "Industry acknowledges frac hits reduce child well EUR",
            "Operators testing various mitigation strategies; results mixed",
            "Regulatory interest in spacing rules to prevent waste (e.g., Texas RRC)"
        ],
        category=IssueCategory.FRAC_HIT,
        issue_strata=["field development", "well interactions", "economic optimization"]
    ),

    DoctrineBlock(
        topic="Stress Shadowing Effects on Multi-Stage Completions",
        keywords=["stress shadow", "stress interference", "fracture spacing", "simultaneous fracturing", "zipper frac", "stress reorientation"],
        conclusion_template=[
            "Stress shadowing occurs when fractures from one stage alter the local stress field, affecting subsequent fracture propagation.",
            "Effects include fracture curving, reduced width, and non-uniform growth, leading to incomplete reservoir contact.",
            "Mitigation strategies include simultaneous fracturing (zipper fracs), optimized cluster spacing, and diverting agents."
        ],
        reasoning_framework="""
Stress shadow mechanics:
1. Fracture opening creates local stress increase perpendicular to fracture
2. Stress increase affects next fracture:
   - Reduces width (higher closure stress)
   - Causes curving away from previous fracture
   - May prevent fracture initiation from inner clusters
3. Magnitude depends on:
   - Fracture spacing (closer = stronger effect)
   - Net pressure (higher = stronger)
   - Formation stiffness (stiffer = stress propagates farther)
   - Time lag (stress relaxes over time via poroelasticity)
4. Consequences:
   - Non-uniform fracture growth (outer clusters dominate)
   - Reduced stimulated reservoir volume (SRV)
   - Lower effective cluster count than designed
5. Mitigation:
   - Zipper fracturing: Alternate stages between two wells (stress cancels)
   - Simultaneous fracturing: Frac multiple stages at once
   - Wider cluster spacing: Reduce stress overlap
   - Limited entry: Force more uniform flow distribution
   - Diverting agents: Temporarily plug dominant perforations
6. Detection:
   - Fiber optic DAS: Shows which clusters take fluid
   - Production logs: Identify non-contributing clusters
   - Microseismic: Maps actual fracture geometry
        """,
        key_factors=[
            "Cluster spacing within stage (typically 20-50 ft)",
            "Stage spacing (150-400 ft)",
            "Completion sequence (toe-to-heel vs simultaneous)",
            "Formation geomechanical properties",
            "Net pressure during treatment",
            "Natural fracture density (can mitigate stress shadow)"
        ],
        primary_authority=[
            "SPE 174345 - Stress Shadow Effects in Multi-Cluster Fracturing",
            "SPE 181650 - Geomechanical Modeling of Fracture Interference",
            "URTeC 2154 - Zipper Fracturing Field Results"
        ],
        burden_holder="Engineer must design completion to minimize stress shadow effects and maximize cluster efficiency",
        adversary_position="Close cluster spacing wastes perforations; conservative spacing reduces stress shadow but limits SRV",
        counter_arguments=[
            "Stress shadow models require accurate geomechanical data often unavailable",
            "Simultaneous/zipper fracs add operational complexity and cost",
            "Natural fractures may dominate over stress shadow effects",
            "Fiber optic measurements show high variability even with mitigation",
            "Long-term production impact of non-uniform fractures unclear"
        ],
        resolution_strategy="Use fiber optic diagnostics to measure cluster efficiency; adopt simultaneous/zipper fracs if stress shadow severe; optimize cluster spacing based on measurements",
        entity_scope="All multi-cluster completions; severity increases with tighter spacing and higher cluster counts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence stress shadow exists; moderate confidence in mitigation effectiveness",
        controlling_precedent=[
            "Industry trend: Zipper fracs adopted by many operators to mitigate stress shadow",
            "Fiber optic use increasing to diagnose cluster efficiency"
        ],
        category=IssueCategory.FRAC_DESIGN,
        issue_strata=["geomechanics", "completion optimization", "cluster design"]
    ),

    DoctrineBlock(
        topic="Limited Entry Perforating for Uniform Flow Distribution",
        keywords=["limited entry", "perforation design", "cluster efficiency", "flow distribution", "friction pressure", "perforation diameter"],
        conclusion_template=[
            "Limited entry design uses small perforation diameter to create friction pressure, forcing uniform flow distribution across clusters.",
            "Perforation friction should be 200-500 psi to achieve uniform distribution without excessive surface pressure.",
            "Proper limited entry design improves cluster efficiency from 30-50% to 70-90%."
        ],
        reasoning_framework="""
Limited entry principles:
1. Concept: Perforation friction dominates over formation differences
   - Without limited entry: Low-stress clusters take all fluid, high-stress clusters shut in
   - With limited entry: Perforation friction forces flow to all clusters
2. Design criteria:
   - Perforation friction ΔPperf = 200-500 psi per cluster
   - ΔPperf >> stress variation between clusters (typically 50-200 psi)
   - Calculate required perforation diameter and count
3. Calculation:
   - ΔP = (ρ × Q²) / (Cd² × n² × d⁴)
   - ρ = fluid density, Q = rate, Cd = discharge coefficient
   - n = number of perforations, d = diameter
   - Typical: 4-6 perforations at 0.3-0.4 inch diameter
4. Trade-offs:
   - Too much friction: Excessive surface pressure, limits rate
   - Too little friction: Clusters don't take uniformly
5. Execution:
   - Requires precise perforating (wireline or TCP)
   - Quality control on shot count and phasing
   - May need step-rate test to confirm friction
6. Validation:
   - Fiber optic DAS shows flow into each cluster
   - Production logs post-frac show contributing intervals
        """,
        key_factors=[
            "Stress variation between clusters",
            "Pump rate and fluid rheology",
            "Surface pressure limitations",
            "Perforation gun capability (shot density, phasing)",
            "Formation breakdown pressure variation",
            "Operational risk of plugged perforations"
        ],
        primary_authority=[
            "SPE 179124 - Limited Entry Design for Improved Cluster Efficiency",
            "SPE 184829 - Perforation Design Optimization in Unconventionals",
            "SPE 191472 - Limited Entry Field Results and Validation"
        ],
        burden_holder="Completion engineer must design perforation scheme to achieve uniform distribution",
        adversary_position="Aggressive limited entry risks excessive surface pressure and perforation erosion",
        counter_arguments=[
            "Perforation erosion during treatment changes friction over time",
            "Formation heterogeneity may overwhelm perforation friction effect",
            "Requires accurate stress profile rarely available",
            "Small perforations increase plugging risk from scale, debris",
            "Limited entry ineffective if natural fractures dominate"
        ],
        resolution_strategy="Design for 300-400 psi perforation friction; validate with fiber optic on first stage; adjust subsequent stages if needed",
        entity_scope="All multi-cluster plug-and-perf completions; critical for achieving design cluster count",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence limited entry improves distribution; moderate confidence in exact friction required",
        controlling_precedent=[
            "Industry standard: Limited entry for multi-cluster completions",
            "Fiber optic diagnostics show 2-3x improvement in cluster efficiency with limited entry"
        ],
        category=IssueCategory.DIVERSION,
        issue_strata=["completion design", "perforation engineering", "flow distribution"]
    ),

    DoctrineBlock(
        topic="Chemical Diversion Agents for Improved Fracture Complexity",
        keywords=["diverting agents", "chemical diversion", "particulate diverter", "degradable fibers", "fracture complexity", "temporary plugging"],
        conclusion_template=[
            "Diverting agents temporarily plug dominant flow paths, forcing treatment into un-stimulated regions and increasing fracture complexity.",
            "Types include particulates (sized salt, degradable polymers), fibers, and benzoic acid flakes; selection depends on temperature and degradation timing.",
            "Effective diversion increases stimulated reservoir volume (SRV) and cluster efficiency without operational complexity of mechanical isolation."
        ],
        reasoning_framework="""
Diversion technology:
1. Mechanism:
   - Diverter particles bridge at fracture entry or inside fracture
   - Temporarily plug high-permeability flow paths
   - Force subsequent fluid into un-stimulated perforations/fractures
   - Diverter degrades or flows back, restoring conductivity
2. Types:
   - Particulate: Sized salt (dissolves), benzoic acid flakes (dissolves), degradable polymer beads
   - Fiber: Degradable fibers that bridge with proppant
   - Hybrid: Fiber + particulate for stronger bridge
3. Design considerations:
   - Particle size: Must match fracture width and perforation diameter
   - Concentration: 10-50 lbs/1000 gal (higher for stronger diversion)
   - Degradation time: Hours to weeks depending on temperature
   - Placement: Between proppant stages or in dedicated diversion stages
4. Benefits:
   - Improves cluster efficiency (more clusters contributing)
   - Increases fracture complexity (stimulates more rock volume)
   - Lower cost than mechanical diverters (ball sealers, bridge plugs)
5. Limitations:
   - Effectiveness depends on fracture width (too wide = no bridging)
   - May not degrade fully, reducing fracture conductivity
   - Difficult to confirm diversion in real-time
   - Can plug surface equipment or perforations prematurely
        """,
        key_factors=[
            "Formation temperature (controls degradation rate)",
            "Fracture width and perforation size",
            "Cluster efficiency without diversion (baseline)",
            "Fluid compatibility and mixing",
            "Post-treatment cleanup requirements",
            "Cost vs benefit (incremental production vs chemical cost)"
        ],
        primary_authority=[
            "SPE 184834 - Chemical Diversion in Multi-Stage Completions",
            "SPE 189851 - Degradable Fiber Diverter Performance",
            "SPE 191782 - Field Trials of Particulate Diverters"
        ],
        burden_holder="Operator must justify diverter selection and demonstrate net benefit over cost",
        adversary_position="Diverters add cost and risk (incomplete degradation, plugging) without guaranteed benefit",
        counter_arguments=[
            "Diverter effectiveness hard to measure (no direct evidence of improved distribution)",
            "May not degrade completely, leaving residue in fracture",
            "Can plug surface lines, valves, perforations during pumping",
            "Natural fractures may provide complexity without chemical diversion",
            "Production uplift difficult to isolate from other completion variables"
        ],
        resolution_strategy="Use diverters selectively in zones with demonstrated low cluster efficiency; track production vs cost; avoid in naturally fractured reservoirs",
        entity_scope="Unconventional multi-stage completions; use increasing but not yet universal",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence in diversion mechanism; low confidence in quantifying production benefit",
        controlling_precedent=[
            "Service companies offer multiple diverter products; adoption growing",
            "Some operators report 10-20% production uplift; others see no benefit"
        ],
        category=IssueCategory.DIVERSION,
        issue_strata=["stimulation chemistry", "fracture complexity", "economic optimization"]
    ),

    DoctrineBlock(
        topic="Real-Time Frac Monitoring - Treating Pressure Interpretation",
        keywords=["real-time monitoring", "treating pressure", "pressure analysis", "screenout detection", "net pressure", "fracture growth"],
        conclusion_framework=[
            "Real-time treating pressure interpretation guides operational decisions during fracturing to optimize treatment and avoid failures.",
            "Pressure signatures indicate fracture growth, height migration, near-wellbore restrictions, and screenout onset.",
            "Experienced frac engineers use pressure trends to adjust rate, proppant schedule, and treatment strategy in real-time."
        ],
        reasoning_framework="""
Pressure interpretation during treatment:
1. Normal fracture growth:
   - Gradual pressure decline after breakdown
   - Stable or slowly increasing net pressure
   - Indicates fracture extending, leakoff balanced by growth
2. Height growth:
   - Sudden pressure drop (fracture breaking into lower-stress layer)
   - Or sustained pressure rise (difficulty extending into high-stress barrier)
3. Near-wellbore restriction:
   - High initial pressure, slow decline
   - Large difference between surface and downhole pressure
   - Indicates tortuosity, perforation plugging, or multiple fracture interaction
4. Screenout indicators:
   - Rapid pressure rise (500+ psi in minutes)
   - Loss of rate (pump pressure exceeds limit)
   - If at fracture tip: Controlled TSO (continue if planned)
   - If near wellbore: Abort, flush, risk of lost well
5. Rate step changes:
   - Pressure response to rate change reveals fracture vs friction
   - Linear response: Friction-dominated
   - Nonlinear: Fracture geometry change
6. Real-time decisions:
   - Reduce rate if pressure approaching limits
   - Slow proppant ramp if screenout risk
   - Increase rate if net pressure dropping (more width needed)
   - Abort and flush if uncontrolled near-wellbore screenout
7. Data integration:
   - Surface pressure (corrected for hydrostatic, friction)
   - Downhole pressure gauges (if available)
   - Slurry rate and density
   - Proppant concentration
        """,
        key_factors=[
            "Baseline pressure expectations from design model",
            "Real-time vs historical pressure trends",
            "Rate and proppant schedule changes",
            "Equipment limitations (max pressure, HHP)",
            "Stage-to-stage pressure variations",
            "Experience of on-site engineer"
        ],
        primary_authority=[
            "Nolte KG (1991) - Fracturing-Pressure Analysis for Nonideal Behavior",
            "SPE 107877 - Fracture Pressure Decline Analysis",
            "SPE 152596 - Real-Time Completion Optimization"
        ],
        burden_holder="Frac engineer must interpret pressure in real-time and make operational decisions",
        adversary_position="Automated systems cannot replace experienced engineer judgment for complex pressure interpretation",
        counter_arguments=[
            "Pressure interpretation ambiguous without additional diagnostics",
            "Real-time decisions under time pressure increase risk of error",
            "Surface pressure corrections uncertain (friction, hydrostatic)",
            "Multiple effects can cause similar pressure signatures",
            "Automated advisory systems improving but not yet autonomous"
        ],
        resolution_strategy="Train engineers on pressure interpretation; use real-time advisors as decision support; validate interpretations post-job with DFIT or production data",
        entity_scope="All hydraulic fracturing operations; critical for large, expensive treatments",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in experienced engineer interpretation; moderate confidence in automated systems",
        controlling_precedent=[
            "Industry standard: Experienced frac engineer on-site for critical wells",
            "Real-time advisors (automated pressure interpretation) increasingly used"
        ],
        category=IssueCategory.MONITORING,
        issue_strata=["operational execution", "decision-making", "pressure analysis"]
    ),

    DoctrineBlock(
        topic="Frac Gradient Calculations for Treatment Design",
        keywords=["frac gradient", "fracture pressure", "breakdown pressure", "psi/ft", "minimum stress", "leak-off test"],
        conclusion_template=[
            "Frac gradient (psi/ft) is the pressure required to propagate a fracture, typically equal to minimum horizontal stress plus breakdown increment.",
            "Calculated from leak-off tests (LOT), formation integrity tests (FIT), or offset well data.",
            "Accurate frac gradient critical for equipment sizing, hydraulic horsepower requirements, and safe operation."
        ],
        reasoning_framework="""
Frac gradient determination:
1. Definition: Frac gradient = Fracture pressure / True vertical depth
   - Typical range: 0.5-1.0 psi/ft (varies by basin, depth, tectonic regime)
   - Normal faulting (extensional): 0.5-0.65 psi/ft
   - Strike-slip: 0.65-0.85 psi/ft
   - Reverse faulting (compressional): 0.85-1.2 psi/ft
2. Measurement methods:
   - Leak-off test (LOT): Pump slowly into formation, record pressure at leakoff
   - Formation integrity test (FIT): Pump to predetermined pressure, hold
   - DFIT: Full pressure cycle, analyze closure stress
   - Offset well data: Use nearby wells' breakdown pressure
3. Breakdown vs propagation:
   - Breakdown pressure: Initial pressure to create fracture (higher)
   - Propagation pressure: Pressure to extend fracture (lower, ~= closure stress + net pressure)
   - Frac gradient typically refers to propagation pressure
4. Applications:
   - Surface pressure prediction: Psurface = (gradient × TVD) - hydrostatic + friction
   - HHP sizing: HHP = (Psurface × rate) / (40.8 × efficiency)
   - Tubular design: Casing/tubing must handle frac pressure + safety factor
5. Uncertainty:
   - LOT/FIT may measure breakdown, not propagation
   - Heterogeneity causes variation along wellbore
   - Pore pressure changes (depletion) alter gradient over time
        """,
        key_factors=[
            "Tectonic regime (controls stress state)",
            "Depth (gradient often increases with depth)",
            "Formation lithology (shale vs sandstone)",
            "Pore pressure (overpressure increases gradient)",
            "Depletion (reduces pore pressure, may reduce gradient)",
            "Natural fractures (may lower gradient if pre-existing fractures)"
        ],
        primary_authority=[
            "SPE 10313 - Fracture Gradient Prediction",
            "Hubbert MK, Willis DG (1957) - Mechanics of Hydraulic Fracturing",
            "Zoback MD (2010) - Reservoir Geomechanics"
        ],
        burden_holder="Engineer must determine accurate frac gradient for safe and effective treatment design",
        adversary_position="Conservative gradient estimates lead to over-designed equipment and higher costs",
        counter_arguments=[
            "LOT/FIT may not represent treatment conditions (rate, fluid type)",
            "Offset well data may not account for local variations",
            "Gradient can change stage-to-stage in heterogeneous formations",
            "Depletion over time alters gradient, requiring updates",
            "Uncertainty requires safety factors, adding cost"
        ],
        resolution_strategy="Use best available data (DFIT > LOT > offset); apply conservative safety factor for equipment design; update with actual treating pressures",
        entity_scope="All hydraulic fracturing operations; critical for new field developments and deep/high-pressure reservoirs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with DFIT; moderate with LOT; low with regional correlation alone",
        controlling_precedent=[
            "Industry standard: Use DFIT or offset well data for frac gradient in design",
            "Regulatory: LOT required after casing in many jurisdictions for well control"
        ],
        category=IssueCategory.PRESSURE_ANALYSIS,
        issue_strata=["geomechanics", "well design", "operational planning"]
    ),

    DoctrineBlock(
        topic="Proppant Selection - Sand vs Ceramic vs Resin-Coated",
        keywords=["proppant type", "sand", "ceramic", "resin-coated", "proppant strength", "conductivity", "cost"],
        conclusion_template=[
            "Proppant selection balances conductivity, crush resistance, and cost based on closure stress and formation characteristics.",
            "Sand (20/40, 30/50, 100 mesh) dominates unconventional completions due to low cost; ceramic and resin-coated used in high-stress or high-productivity wells.",
            "Proppant crush at closure stress reduces permeability; high-strength proppant maintains conductivity at stress but costs 2-10x more."
        ],
        reasoning_framework="""
Proppant type comparison:
1. Sand (frac sand, white sand, Northern White, West Texas brown):
   - Strength: 4,000-6,000 psi closure stress
   - Permeability: 50,000-150,000 md (20/40 mesh, unconfined)
   - Cost: $50-150/ton (varies by logistics)
   - Applications: Most unconventional completions (Permian, Eagle Ford, Bakken)
   - Limitations: Crushes at high stress, embedment in soft formations
2. Ceramic (sintered bauxite, lightweight ceramic):
   - Strength: 8,000-20,000 psi (depending on grade)
   - Permeability: 80,000-200,000 md
   - Cost: $300-800/ton
   - Applications: Deep wells, high-stress reservoirs, critical high-rate wells
   - Benefits: Maintains conductivity at stress, less embedment
3. Resin-coated sand (curable, precured):
   - Strength: 6,000-10,000 psi (coating adds strength)
   - Permeability: Slightly less than uncoated due to resin
   - Cost: $150-300/ton
   - Applications: Proppant flowback prevention, high-velocity gas wells
   - Benefits: Consolidates pack, prevents flowback, may reduce crushing
4. Selection criteria:
   - Closure stress: <6,000 psi = sand adequate; >8,000 psi = ceramic
   - EUR expectations: High-value wells justify ceramic cost
   - Flowback risk: Resin-coated if flowback observed in offsets
   - Logistics: Sand availability and transport cost vary regionally
5. Mesh size:
   - 20/40 (largest): High conductivity, poor transport in slickwater
   - 30/50: Compromise
   - 40/70, 100 mesh: Lower conductivity, excellent transport, used in slickwater
        """,
        key_factors=[
            "Closure stress (primary driver)",
            "Formation softness (embedment risk)",
            "Well EUR and economic value",
            "Proppant logistics and cost",
            "Fluid system (slickwater vs gel affects transport)",
            "Flowback risk and mitigation"
        ],
        primary_authority=[
            "API RP 19D - Proppant Testing Standards",
            "SPE 84306 - Proppant Selection for Unconventional Reservoirs",
            "SPE 171649 - Long-Term Conductivity of Proppant Types"
        ],
        burden_holder="Engineer must justify proppant type based on stress, economics, and conductivity requirements",
        adversary_position="Sand is adequate for most unconventionals; ceramic over-specified and wastes money",
        counter_arguments=[
            "Ceramic cost rarely justified by incremental production in unconventionals",
            "Sand crushes but still provides sufficient conductivity at <6,000 psi stress",
            "Resin-coated benefits difficult to quantify",
            "Proppant embedment in soft formations negates strength advantage",
            "100 mesh sand conductivity may be insufficient for long-term production"
        ],
        resolution_strategy="Use sand for most unconventional completions (<6,000 psi stress); ceramic for deep/high-stress wells with high EUR; resin-coated selectively for flowback issues",
        entity_scope="All proppant fracturing; selection drives material cost (often 30-50% of completion budget)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in selection criteria; moderate confidence in long-term conductivity predictions",
        controlling_precedent=[
            "Industry standard: 100 mesh sand for Permian/Eagle Ford slickwater",
            "Ceramic use declining in unconventionals due to cost vs benefit"
        ],
        category=IssueCategory.FRAC_DESIGN,
        issue_strata=["proppant engineering", "material selection", "economic optimization"]
    ),

    DoctrineBlock(
        topic="Cluster Spacing Optimization for Stimulated Reservoir Volume",
        keywords=["cluster spacing", "perforation spacing", "SRV", "stimulated reservoir volume", "fracture spacing", "recovery efficiency"],
        conclusion_template=[
            "Cluster spacing (distance between perforation clusters within a stage) controls fracture density and stimulated reservoir volume (SRV).",
            "Tighter spacing increases fracture count but risks stress shadowing reducing individual fracture growth.",
            "Optimal spacing balances SRV maximization with operational constraints and cluster efficiency."
        ],
        reasoning_framework="""
Cluster spacing principles:
1. Typical spacing: 20-50 ft in unconventional completions
   - Tighter spacing: More fractures, higher SRV, but stress shadow effects
   - Wider spacing: Less stress shadow, but lower fracture density
2. Stress shadow considerations:
   - Stress increase from one fracture affects neighbors
   - Effect magnitude inversely related to spacing (closer = stronger)
   - Can cause non-uniform fracture growth (outer clusters dominate)
3. Formation drainage:
   - Ultra-low permeability (<0.001 md): Fracture spacing drives recovery
   - Tighter spacing improves sweep, reduces interwell spacing requirements
4. Operational limits:
   - Perforation gun length and shot count
   - Stage length and total cluster count
   - Sliding sleeve systems limited by ball size progression
5. Trends over time:
   - 2010s: 50-100 ft spacing (3-4 clusters/stage)
   - 2020s: 20-40 ft spacing (6-10 clusters/stage)
   - Driven by improved cluster efficiency (limited entry, diverters)
6. Optimization approach:
   - Model stress shadow vs SRV trade-off
   - Test spacing variations in pilot wells
   - Measure cluster efficiency with fiber optics
   - Economic optimization: Spacing vs well count vs EUR
        """,
        key_factors=[
            "Formation permeability (lower perm = tighter spacing needed)",
            "Natural fracture density (high density may relax spacing needs)",
            "Stress shadow magnitude (formation stiffness, net pressure)",
            "Cluster efficiency (limited entry, diversion effectiveness)",
            "Stage length and total cluster count",
            "Economics (perforation cost, completion time)"
        ],
        primary_authority=[
            "SPE 181670 - Cluster Spacing Optimization in Unconventionals",
            "URTeC 2901522 - Impact of Cluster Spacing on EUR",
            "SPE 189840 - Stress Shadow Effects on Cluster Design"
        ],
        burden_holder="Completion engineer must optimize cluster spacing to maximize SRV and EUR within operational constraints",
        adversary_position="Aggressive tight spacing wastes perforations due to stress shadow; conservative spacing limits SRV",
        counter_arguments=[
            "Stress shadow models require uncertain geomechanical inputs",
            "Fiber optic data shows high variability in cluster efficiency regardless of spacing",
            "Tighter spacing increases perforation cost and wireline time",
            "Natural fractures may provide connectivity making tight spacing unnecessary",
            "Optimal spacing varies by formation, making one-size-fits-all approach flawed"
        ],
        resolution_strategy="Use basin-specific analog data as baseline; test spacing variations with fiber optic diagnostics; optimize based on measured cluster efficiency and production response",
        entity_scope="All multi-cluster unconventional completions; spacing is key design parameter",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Moderate confidence; optimal spacing varies by formation and requires field testing",
        controlling_precedent=[
            "Industry trend: Tighter spacing over time (50 ft → 25 ft average)",
            "Operators use fiber optic to validate cluster efficiency and adjust spacing"
        ],
        category=IssueCategory.FRAC_DESIGN,
        issue_strata=["completion design", "reservoir contact", "economic optimization"]
    ),

    DoctrineBlock(
        topic="Fracture Fluid Selection - Slickwater vs Crosslinked Gel vs Hybrid",
        keywords=["slickwater", "crosslinked gel", "hybrid fluid", "fluid selection", "friction reducer", "proppant transport", "gel damage"],
        conclusion_template=[
            "Slickwater (water + friction reducer) dominates unconventional completions due to low cost, minimal formation damage, and ability to create complex fractures.",
            "Crosslinked gel (guar + borate/zirconate) provides superior proppant transport and width but risks formation damage and costs more.",
            "Hybrid fluids combine slickwater pad with gel proppant stages, balancing complexity and conductivity."
        ],
        reasoning_framework="""
Fluid system comparison:
1. Slickwater:
   - Composition: 99%+ water, polyacrylamide friction reducer (0.5-2 gpt), biocide, scale inhibitor
   - Viscosity: ~1-5 cp
   - Benefits: Low cost ($0.50-1.00/bbl), minimal damage, creates complex fractures in naturally fractured rock
   - Limitations: Poor proppant transport (settling), requires high rate, narrow fractures
   - Applications: Most shale completions (Permian, Eagle Ford, Marcellus, Bakken)
2. Crosslinked gel:
   - Composition: Guar or HPG (20-40 lbs/1000 gal), crosslinker (borate, zirconate), breaker
   - Viscosity: 100-1000 cp
   - Benefits: Excellent proppant transport, wider fractures, controlled fracture geometry
   - Limitations: High cost ($3-8/bbl), formation damage from gel residue, complex mixing
   - Applications: Conventional reservoirs, tight gas sands, some deeper shales (Haynesville)
3. Hybrid:
   - Sequence: Slickwater pad → gel slurry stages → slickwater flush
   - Benefits: Complexity from slickwater, conductivity from gel-placed proppant
   - Balances cost and performance
4. Selection factors:
   - Formation permeability: <0.001 md = slickwater (damage avoidance critical)
   - Natural fractures: Present = slickwater (leverage complexity)
   - Proppant concentration: >3 ppg often requires gel
   - Economics: Slickwater 30-50% cheaper than gel
   - Water availability: Gel uses less volume
        """,
        key_factors=[
            "Formation permeability and damage sensitivity",
            "Natural fracture density",
            "Desired proppant concentration",
            "Water availability and disposal capacity",
            "Fluid cost and logistics",
            "Target fracture geometry (complex vs simple)"
        ],
        primary_authority=[
            "SPE 119900 - Slickwater Fracturing in Shale Reservoirs",
            "SPE 102227 - Fracturing Fluid Selection Criteria",
            "SPE 185043 - Hybrid Fluid Design Optimization"
        ],
        burden_holder="Engineer must select fluid system matching formation characteristics and economic constraints",
        adversary_position="Slickwater advocates cite low cost and damage avoidance; gel advocates cite conductivity and proppant placement",
        counter_arguments=[
            "Slickwater proppant settling leaves lower effective concentration",
            "Gel damage can offset conductivity benefit",
            "Hybrid complexity adds operational risk (fluid changes during treatment)",
            "Natural fractures in some shales may not benefit from slickwater complexity",
            "Friction reducer technology improving, narrowing gap with gel transport"
        ],
        resolution_strategy="Use slickwater for low-perm, naturally fractured shales; gel for high-perm conventional or deep tight gas; hybrid selectively for intermediate cases",
        entity_scope="All hydraulic fracturing; fluid choice drives cost, performance, and operational complexity",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in selection criteria; field results validate slickwater for most unconventionals",
        controlling_precedent=[
            "Industry standard: Slickwater for Permian, Eagle Ford, Bakken, Marcellus shales",
            "Gel use declining in unconventionals but persists in some basins (Haynesville, Tuscaloosa)"
        ],
        category=IssueCategory.FRAC_DESIGN,
        issue_strata=["fluid systems", "formation damage", "economic optimization"]
    ),

    DoctrineBlock(
        topic="Post-Frac Flowback and Cleanup Strategy",
        keywords=["flowback", "cleanup", "load recovery", "choke management", "proppant flowback", "unloading"],
        conclusion_template=[
            "Post-frac flowback removes frac fluid from formation while minimizing proppant flowback and formation damage.",
            "Controlled flowback with gradual choke-up establishes proppant pack stability and prevents sand production.",
            "Aggressive flowback risks proppant production; conservative flowback delays production and may leave damaging fluid in formation."
        ],
        reasoning_framework="""
Flowback best practices:
1. Initial flowback (0-24 hours):
   - Small choke (8-12/64"), low rate
   - Recover wellbore fluid (cleaner, less proppant)
   - Monitor for proppant production (sand in flowback samples)
2. Choke management:
   - Gradual choke-up schedule (increase size every 6-24 hrs)
   - Typical progression: 8 → 12 → 16 → 24 → 32/64"
   - Halt choke-up if proppant production observed
   - Target: Stabilize proppant pack before full production rate
3. Load recovery:
   - Typical: 20-40% of injected fluid recovered in first 30 days
   - Higher recovery in higher-perm formations
   - Residual fluid may reduce effective permeability (damage)
4. Proppant flowback indicators:
   - Sand in flowback samples
   - Erosion of surface equipment (chokes, lines)
   - Production decline after initial spike
5. Mitigation strategies:
   - Resin-coated proppant (consolidates pack)
   - Screen-out completions (pack held by near-wellbore restriction)
   - Gradual choke-up
   - Downhole sand screens (rare in unconventionals)
6. Economic considerations:
   - Aggressive flowback: Earlier production, more revenue
   - Conservative: Proppant pack stability, long-term productivity
   - Balance depends on well value and proppant flowback risk
        """,
        key_factors=[
            "Proppant type and strength",
            "Formation consolidation (soft vs hard rock)",
            "Fracture conductivity (higher conductivity = higher velocity = more flowback risk)",
            "Completion type (open hole vs cased hole affects sand production)",
            "Fluid recovery rate and formation damage",
            "Well economic value (high-value wells justify conservative approach)"
        ],
        primary_authority=[
            "SPE 114194 - Flowback Management in Unconventional Reservoirs",
            "SPE 173333 - Proppant Flowback Mechanisms and Mitigation",
            "SPE 187225 - Choke Management Optimization"
        ],
        burden_holder="Operator must balance rapid production startup vs long-term well integrity",
        adversary_position="Aggressive flowback advocates prioritize cash flow; conservative advocates prioritize well life",
        counter_arguments=[
            "Proppant flowback difficult to predict; varies well-to-well",
            "Residual frac fluid may not cause significant damage in ultra-low-perm shales",
            "Resin-coated proppant cost may not justify flowback benefit",
            "Choke management labor-intensive, requires on-site personnel",
            "Optimal strategy varies by formation and well design"
        ],
        resolution_strategy="Use basin-specific analog data for choke schedule; monitor proppant production; adjust in real-time; consider resin-coated proppant if flowback observed in offsets",
        entity_scope="All hydraulic fracturing operations; critical for well productivity and longevity",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Moderate confidence; flowback behavior varies significantly by formation and completion",
        controlling_precedent=[
            "Industry best practice: Gradual choke-up over 1-2 weeks",
            "Operators develop field-specific flowback schedules based on experience"
        ],
        category=IssueCategory.FRAC_DESIGN,
        issue_strata=["post-frac operations", "well integrity", "production optimization"]
    ),
]


# ═══════════════════════════════════════════════════════════════════════════
# TELEMETRY AND METRICS
# ═══════════════════════════════════════════════════════════════════════════

class Telemetry:
    """Tracks engine performance metrics."""

    def __init__(self):
        self.total_queries = 0
        self.total_latency_ms = 0.0
        self.doctrine_hits = defaultdict(int)
        self.category_counts = defaultdict(int)
        self.mode_counts = defaultdict(int)
        self.start_time = time.time()

    def record_query(self, latency_ms: float, doctrines: List[str],
                    categories: List[IssueCategory], mode: ResponseMode):
        """Record query metrics."""
        self.total_queries += 1
        self.total_latency_ms += latency_ms
        for d in doctrines:
            self.doctrine_hits[d] += 1
        for c in categories:
            self.category_counts[c.value] += 1
        self.mode_counts[mode.value] += 1

    @property
    def avg_latency_ms(self) -> float:
        """Calculate average latency."""
        return self.total_latency_ms / self.total_queries if self.total_queries > 0 else 0.0

    @property
    def uptime_seconds(self) -> float:
        """Calculate uptime."""
        return time.time() - self.start_time


telemetry = Telemetry()


# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE MATCHING ENGINE
# ═══════════════════════════════════════════════════════════════════════════

def match_doctrines(query: str) -> List[DoctrineBlock]:
    """Match query to relevant doctrine blocks."""
    query_lower = query.lower()
    matched = []

    for doctrine in DOCTRINE_CACHE:
        # Check keywords
        if any(kw.lower() in query_lower for kw in doctrine.keywords):
            matched.append(doctrine)
            continue
        # Check topic
        if any(word in query_lower for word in doctrine.topic.lower().split()):
            matched.append(doctrine)

    return matched[:5]  # Return top 5 matches


# ═══════════════════════════════════════════════════════════════════════════
# RESPONSE GENERATION
# ═══════════════════════════════════════════════════════════════════════════

def generate_response(query: str, mode: ResponseMode, doctrines: List[DoctrineBlock]) -> str:
    """Generate response based on mode and matched doctrines."""

    if not doctrines:
        return (
            f"Query received: {query}\n\n"
            "No specific hydraulic fracturing doctrines matched this query. "
            "Please rephrase or provide more details about the frac design, "
            "completion type, basin, or technical aspect you're interested in."
        )

    if mode == ResponseMode.FAST:
        # Concise response
        primary = doctrines[0]
        response_parts = [
            f"**{primary.topic}**\n",
            "\n".join(f"• {c}" for c in primary.conclusion_template),
            f"\n\n**Key Factors**: {', '.join(primary.key_factors[:3])}"
        ]
        return "\n".join(response_parts)

    elif mode == ResponseMode.DEFENSE:
        # Audit-ready detailed response
        response_parts = []
        for doctrine in doctrines[:3]:
            response_parts.append(f"## {doctrine.topic}\n")
            response_parts.append("**Conclusion**:")
            response_parts.extend(f"• {c}" for c in doctrine.conclusion_template)
            response_parts.append("\n**Reasoning Framework**:")
            response_parts.append(doctrine.reasoning_framework.strip())
            response_parts.append("\n**Primary Authority**:")
            response_parts.extend(f"• {a}" for a in doctrine.primary_authority)
            response_parts.append("\n**Counter-Arguments**:")
            response_parts.extend(f"• {ca}" for ca in doctrine.counter_arguments[:3])
            response_parts.append(f"\n**Resolution Strategy**: {doctrine.resolution_strategy}\n")
        return "\n".join(response_parts)

    else:  # MEMO
        # Full technical memo
        response_parts = [
            f"# Hydraulic Fracturing Analysis: {query}\n",
            f"**Date**: {datetime.utcnow().strftime('%Y-%m-%d')}",
            f"**Engine**: {ENGINE_NAME} v{VERSION}\n",
            "---\n"
        ]

        for i, doctrine in enumerate(doctrines[:3], 1):
            response_parts.append(f"## {i}. {doctrine.topic}\n")
            response_parts.append("### Conclusion")
            response_parts.extend(f"{c}" for c in doctrine.conclusion_template)
            response_parts.append("\n### Technical Analysis")
            response_parts.append(doctrine.reasoning_framework.strip())
            response_parts.append("\n### Key Factors")
            response_parts.extend(f"• {kf}" for kf in doctrine.key_factors)
            response_parts.append("\n### Authoritative References")
            response_parts.extend(f"• {ref}" for ref in doctrine.primary_authority)
            response_parts.append(f"\n### Confidence Level: {doctrine.confidence.value}")
            response_parts.append(f"{doctrine.confidence_stratification}")
            response_parts.append("\n### Counter-Arguments and Rebuttals")
            for ca in doctrine.counter_arguments:
                response_parts.append(f"• **Counter**: {ca}")
            response_parts.append(f"\n**Resolution Strategy**: {doctrine.resolution_strategy}\n")
            response_parts.append("---\n")

        return "\n".join(response_parts)


# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title=ENGINE_NAME,
    description="TIE Gold Standard Hydraulic Fracturing Design Intelligence Engine",
    version=VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint."""
    return {
        "engine": ENGINE_NAME,
        "engine_id": ENGINE_ID,
        "version": VERSION,
        "status": "operational",
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "endpoints": ["/query", "/health", "/doctrines"]
    }


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Process hydraulic fracturing design query."""
    start_time = time.time()

    try:
        # Match doctrines
        matched_doctrines = match_doctrines(request.query)

        # Generate response
        response_text = generate_response(
            request.query,
            request.mode,
            matched_doctrines
        )

        # Extract metadata
        triggered = [d.topic for d in matched_doctrines]
        categories = list(set(d.category for d in matched_doctrines))
        confidence = matched_doctrines[0].confidence if matched_doctrines else ConfidenceLevel.DISCLOSURE

        # Calculate determinism hash
        hash_input = f"{request.query}|{request.mode.value}|{triggered}"
        det_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        # Record telemetry
        latency_ms = (time.time() - start_time) * 1000
        telemetry.record_query(latency_ms, triggered, categories, request.mode)

        logger.info(f"Query processed: {request.query[:50]}... | Mode: {request.mode.value} | Latency: {latency_ms:.1f}ms")

        return QueryResponse(
            response=response_text,
            mode=request.mode,
            confidence=confidence,
            triggered_doctrines=triggered,
            issue_categories=[c.value for c in categories],
            determinism_hash=det_hash,
            latency_ms=latency_ms,
            timestamp=datetime.utcnow().isoformat()
        )

    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=telemetry.uptime_seconds,
        total_queries=telemetry.total_queries,
        avg_latency_ms=telemetry.avg_latency_ms
    )


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrines."""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords[:5],
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
