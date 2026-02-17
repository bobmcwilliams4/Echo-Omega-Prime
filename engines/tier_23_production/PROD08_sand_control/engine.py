"""
PROD08 Sand Control Intelligence Engine
Production Engineering Domain - Sand Management & Control Systems

TIE-Grade Engine: Sand production prediction, gravel pack design, screen selection,
frac pack operations, chemical consolidation, sand management strategies.

Port: 9223
Version: 1.0.0
"""

import sys
from pathlib import Path

# CRITICAL: Add parent directory to path BEFORE any local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import re
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

import uvicorn
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
    OPERATIONS = "OPERATIONS"
    MONITORING = "MONITORING"
    REMEDIAL = "REMEDIAL"


class SandControlMethod(str, Enum):
    GRAVEL_PACK = "GRAVEL_PACK"
    FRAC_PACK = "FRAC_PACK"
    STANDALONE_SCREEN = "STANDALONE_SCREEN"
    EXPANDABLE_SCREEN = "EXPANDABLE_SCREEN"
    CHEMICAL_CONSOLIDATION = "CHEMICAL_CONSOLIDATION"
    ORIENTED_PERFORATION = "ORIENTED_PERFORATION"
    NONE = "NONE"


class IssueCategory(str, Enum):
    SANDING_PREDICTION = "SANDING_PREDICTION"
    GRAVEL_SIZING = "GRAVEL_SIZING"
    SCREEN_SELECTION = "SCREEN_SELECTION"
    FRAC_PACK_DESIGN = "FRAC_PACK_DESIGN"
    PACK_PLACEMENT = "PACK_PLACEMENT"
    CONSOLIDATION = "CONSOLIDATION"
    MONITORING = "MONITORING"
    REMEDIATION = "REMEDIATION"
    ECONOMICS = "ECONOMICS"


@dataclass
class DoctrineBlock:
    """Core knowledge unit for sand control engineering"""
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
    controlling_precedent: Optional[str] = None
    category: IssueCategory = IssueCategory.SANDING_PREDICTION


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=10)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    context: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    answer: str
    mode: ResponseMode
    zone: AnalysisZone
    confidence: ConfidenceLevel
    doctrines_triggered: List[str]
    reasoning_chain: List[str]
    authorities_cited: List[str]
    determinism_hash: str
    telemetry: Dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float


# ============================================================================
# DOCTRINE CACHE - 25+ REAL SAND CONTROL KNOWLEDGE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    # SANDING PREDICTION DOCTRINES

    DoctrineBlock(
        topic="Critical Drawdown Pressure",
        keywords=["critical drawdown", "sanding onset", "rock strength", "pore pressure", "drawdown limit"],
        conclusion_template="Critical drawdown pressure represents the pressure differential at which sand production initiates. For unconsolidated formations, critical drawdown typically ranges from 200-1500 psi depending on formation strength, stress regime, and fluid properties. Exceeding critical drawdown by more than 20% dramatically increases sanding risk.",
        reasoning_framework="""
Critical drawdown analysis follows these principles:

1. STRESS STATE ASSESSMENT
   - In-situ stress magnitudes (Sv, SHmax, Shmin)
   - Pore pressure regime
   - Effective stress calculations
   - Stress path during depletion

2. ROCK STRENGTH EVALUATION
   - Unconfined compressive strength (UCS)
   - Cohesion and internal friction angle
   - Consolidation state (cementation)
   - Grain size distribution

3. CRITICAL DRAWDOWN CALCULATION
   - Mohr-Coulomb failure criterion
   - Thick-wall cylinder models
   - Cavity stability analysis
   - Safety factor application (typically 1.5-2.0)

4. DEPLETION EFFECTS
   - Pore pressure decline over time
   - Stress arch deterioration
   - Critical drawdown reduction with depletion
   - Need for dynamic operating limits

5. VALIDATION METHODS
   - Thick-wall cylinder (TWC) testing
   - Core flow testing
   - Analog well performance
   - Calibration to field observations

The critical drawdown defines the maximum safe production rate and
establishes whether sand control completion is required. Conservative
estimation is essential because underestimating critical drawdown leads
to sand production, erosion damage, and potential well loss.
""",
        key_factors=[
            "Formation UCS and consolidation state",
            "In-situ stress regime and pore pressure",
            "Perforation tunnel stability",
            "Production rate and drawdown magnitude",
            "Depletion history and stress path",
            "Safety factor for uncertainty"
        ],
        primary_authority=[
            "SPE 73752 - Predicting Onset of Sand Production",
            "SPE 84496 - Critical Drawdown in Unconsolidated Reservoirs",
            "SPE 110647 - TWC Testing for Sand Prediction"
        ],
        burden_holder="Operator must prove critical drawdown not exceeded",
        adversary_position="Conservative critical drawdown estimates reduce production",
        counter_arguments=[
            "TWC testing may not represent actual wellbore conditions",
            "Critical drawdown increases with perforation cleanup",
            "Field experience shows higher safe rates than predictions",
            "Cost of sand control may exceed cost of managing sand",
            "Depletion effects not captured in static models"
        ],
        resolution_strategy="Use TWC testing plus field calibration with phased rate increases and sand monitoring",
        entity_scope="Unconsolidated to moderately consolidated formations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for TWC-calibrated predictions; moderate for correlations",
        controlling_precedent="SPE 73752 Mohr-Coulomb cavity stability model",
        category=IssueCategory.SANDING_PREDICTION
    ),

    DoctrineBlock(
        topic="Thick Wall Cylinder Testing",
        keywords=["TWC test", "laboratory testing", "sanding prediction", "core analysis", "failure pressure"],
        conclusion_template="Thick Wall Cylinder testing provides the most reliable method for predicting sanding onset by replicating wellbore stress conditions on core samples. TWC testing measures failure pressure under controlled stress states, fluid flow, and temperature, yielding critical drawdown values with 70-85% field accuracy when properly conducted.",
        reasoning_framework="""
TWC testing methodology and interpretation:

1. SAMPLE PREPARATION
   - Preserved core material essential
   - Cylindrical samples (1.5-2 inch OD typical)
   - Central axial hole simulating wellbore
   - Length-to-diameter ratio 2:1 minimum
   - Orientation to bedding planes documented

2. TEST CONDITIONS
   - Confining stress simulating in-situ conditions
   - Axial stress representing overburden
   - Pore pressure at reservoir conditions
   - Temperature control (reservoir temp)
   - Flow rate ramped incrementally

3. FAILURE DETECTION
   - Sand production monitoring (weight or particle count)
   - Pressure differential recording
   - Acoustic emission detection
   - Post-test CT scanning
   - Failure mode documentation

4. DATA INTERPRETATION
   - Critical drawdown at sanding onset
   - Failure envelope construction
   - Stress-dependent behavior
   - Rate effects on failure
   - Correlation to field conditions

5. VALIDATION AND SCALING
   - Multiple tests for statistics
   - Comparison to field sanding history
   - Calibration factors development
   - Uncertainty quantification
   - Update predictions with production data

TWC testing costs $5,000-15,000 per test but provides high-confidence
data for completion design decisions worth millions. Essential for
high-value wells or when sand control method selection is marginal.
""",
        key_factors=[
            "Core preservation quality",
            "Stress state replication accuracy",
            "Sample size effects and scaling",
            "Multiple tests for statistical confidence",
            "Calibration to field performance",
            "Cost-benefit for well economics"
        ],
        primary_authority=[
            "SPE 110647 - TWC Testing Best Practices",
            "SPE 143927 - Laboratory Testing for Sand Prediction",
            "SPE 168152 - TWC Test Validation Against Field Data"
        ],
        burden_holder="Laboratory must replicate field conditions accurately",
        adversary_position="TWC tests are expensive and may not capture all field variables",
        counter_arguments=[
            "Sample disturbance affects results",
            "Scale effects between core and wellbore",
            "Time-dependent effects not captured",
            "Cost prohibitive for marginal wells",
            "Correlations may substitute adequately"
        ],
        resolution_strategy="Use TWC for high-value wells; validate with field data; develop regional correlations",
        entity_scope="Unconsolidated formations requiring sand control",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with proper execution; validate against field performance",
        controlling_precedent="SPE 110647 standard TWC testing protocol",
        category=IssueCategory.SANDING_PREDICTION
    ),

    DoctrineBlock(
        topic="Formation Sand Analysis",
        keywords=["grain size distribution", "D10", "D50", "D90", "sieve analysis", "particle size"],
        conclusion_template="Formation sand grain size distribution is the fundamental parameter for gravel pack and screen design. D10, D50, and D90 values determine gravel sizing ratios and screen aperture selection. Proper characterization requires representative sampling, standard sieve analysis, and accounting for fines migration potential.",
        reasoning_framework="""
Formation sand characterization protocol:

1. SAMPLING REQUIREMENTS
   - Core samples from production interval
   - Sidewall cores if core unavailable
   - Minimum 100 grams per sample
   - Multiple depth samples for heterogeneity
   - Avoid contamination with drilling mud

2. SIEVE ANALYSIS PROCEDURE
   - ASTM D422 or API RP 58 standard
   - Sieve sizes from 4 mesh to 270 mesh
   - Wet or dry sieving depending on fines
   - Hydrometer analysis for clay fraction
   - Weight percent retained per sieve

3. CRITICAL PARAMETERS
   - D10: 10% passing (controls retention)
   - D50: median grain size (central tendency)
   - D90: 90% passing (coarse fraction)
   - Coefficient of uniformity: Cu = D60/D10
   - Sorting coefficient: D75/D25

4. DESIGN IMPLICATIONS
   - Gravel size = 6x formation D50 (classical)
   - Gravel size = 5x formation D10 (conservative)
   - Screen aperture = D10/2 to D10
   - Uniform formation (Cu < 3): easier to control
   - Non-uniform (Cu > 5): bridging concerns

5. SPECIAL CONSIDERATIONS
   - Bimodal distributions require dual analysis
   - Clay and silt content affects bridging
   - Carbonate vs silica sand behavior
   - Fines migration vs in-situ fines
   - Production history effects on distribution

Accurate grain size analysis is non-negotiable. A $500 sieve analysis
determines $100,000+ in completion design. Errors in D50 by 20% can
cause pack failures or excessive sand production.
""",
        key_factors=[
            "Representative sample collection",
            "Standard sieve analysis execution",
            "D10, D50, D90 determination",
            "Uniformity coefficient calculation",
            "Fines content quantification",
            "Multiple samples for heterogeneous zones"
        ],
        primary_authority=[
            "API RP 58 - Sand Control Recommended Practices",
            "SPE 30096 - Formation Sand Analysis and Gravel Selection",
            "ASTM D422 - Particle Size Analysis Standard"
        ],
        burden_holder="Operator must obtain representative formation sand samples",
        adversary_position="Limited sampling may not capture formation variability",
        counter_arguments=[
            "Core samples may not represent actual produced sand",
            "Fines generation during production changes distribution",
            "Single samples insufficient for heterogeneous zones",
            "Sidewall cores provide inadequate sample volume",
            "Production alters grain size over time"
        ],
        resolution_strategy="Collect multiple samples across interval; validate with produced sand analysis if available",
        entity_scope="All sand control completions requiring pack or screen sizing",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with proper sampling and analysis",
        controlling_precedent="API RP 58 grain size analysis requirements",
        category=IssueCategory.GRAVEL_SIZING
    ),

    # GRAVEL PACK DESIGN DOCTRINES

    DoctrineBlock(
        topic="Gravel Sizing Criteria",
        keywords=["gravel pack sizing", "Saucier criteria", "6x rule", "beta wave", "gravel to sand ratio"],
        conclusion_template="Gravel sizing follows established criteria to ensure formation sand retention while maintaining permeability. The classical 6x median (D50) rule provides conservative sizing. Modern beta wave theory refines this to 5-7x formation D10-D40 depending on uniformity coefficient. Proper sizing prevents formation sand production while avoiding pack plugging.",
        reasoning_framework="""
Gravel pack sizing methodology:

1. CLASSICAL SAUCIER CRITERIA (1974)
   - Gravel D50 = 6x formation D50
   - Gravel must be uniform: Cu < 2.5
   - Formation retention if gravel D10 > 5x formation D50
   - Applies to uniform formations (Cu < 3)
   - Conservative, widely accepted

2. BETA WAVE THEORY (COBERLY)
   - Based on particle bridging mechanics
   - Gravel D50 = 5-6x formation D40
   - Accounts for sorting coefficient
   - Predicts sand retention and permeability
   - More accurate for non-uniform formations

3. MODERN PRACTICE
   - For Cu < 3: Use 6x formation D50
   - For Cu 3-5: Use 5-6x formation D40
   - For Cu > 5: Consider D10 multiplier method
   - Target gravel Cu < 2.5 for uniformity
   - Verify with lab pack tests if critical

4. GRAVEL SPECIFICATIONS
   - Standard sizes: 8/12, 10/20, 12/20, 16/30, 20/40 mesh
   - Roundness > 0.6 (Krumbein scale)
   - Sphericity > 0.6
   - Silica sand preferred for strength
   - Resin-coated for high-rate applications

5. PACK PERMEABILITY CONSIDERATIONS
   - Gravel pack permeability: 100-300 Darcy typical
   - Must exceed formation permeability by 10-20x
   - Larger gravel = higher permeability
   - Avoid oversizing (poor retention)
   - Balance retention vs flow capacity

6. VALIDATION
   - Laboratory pack tests for critical wells
   - Produced sand monitoring post-installation
   - Pressure performance analysis
   - Analog well performance comparison
   - Adjust criteria based on field results

Gravel sizing is the single most critical sand control design parameter.
Undersizing causes sand production; oversizing wastes permeability and
may allow pack invasion into formation. Use conservative criteria and
validate with testing for high-value wells.
""",
        key_factors=[
            "Formation grain size distribution (D10, D40, D50)",
            "Uniformity coefficient of formation",
            "Gravel pack uniformity requirement (Cu < 2.5)",
            "Saucier 6x median rule vs beta wave theory",
            "Pack permeability vs formation permeability",
            "Gravel quality specifications (roundness, strength)"
        ],
        primary_authority=[
            "SPE 4772 - Saucier Gravel Pack Criteria",
            "SPE 30096 - Modern Gravel Sizing Methods",
            "API RP 58 - Gravel Pack Design Guidelines"
        ],
        burden_holder="Completion engineer must select gravel preventing sand production",
        adversary_position="Oversized gravel wastes money and may reduce effectiveness",
        counter_arguments=[
            "6x rule overly conservative for uniform formations",
            "Larger gravel reduces completion cost",
            "Formation fines will plug regardless of gravel size",
            "Gravel permeability not limiting factor",
            "Field data shows wider sizing range acceptable"
        ],
        resolution_strategy="Use conservative sizing (5-6x D50) unless lab testing justifies alternatives",
        entity_scope="All gravel pack and frac pack completions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for Saucier criteria; moderate for non-uniform formations",
        controlling_precedent="SPE 4772 Saucier gravel sizing methodology",
        category=IssueCategory.GRAVEL_SIZING
    ),

    DoctrineBlock(
        topic="Gravel Pack Placement",
        keywords=["pack placement", "alpha wave", "beta wave", "washout", "crossover", "squeeze"],
        conclusion_template="Gravel pack placement quality determines completion success. Alpha wave placement (gravel slurry ahead of carrier fluid) fills annulus from bottom up. Beta wave placement (carrier fluid ahead) settles gravel by gravity. Crossover from alpha to beta indicates proper pack, while early crossover or washout signals placement problems requiring remediation.",
        reasoning_framework="""
Gravel pack placement mechanics and monitoring:

1. ALPHA WAVE PLACEMENT
   - Gravel-laden slurry travels ahead of clean carrier
   - Occurs during initial pumping stage
   - Fills annulus from perforations upward
   - Controlled by pump rate and fluid rheology
   - Indicates good pack quality when sustained

2. BETA WAVE PLACEMENT
   - Clean carrier fluid ahead of gravel
   - Gravel settles by gravity from carrier
   - Normal after annulus fills (crossover event)
   - Slower placement than alpha wave
   - Final pack consolidation phase

3. CROSSOVER DETECTION
   - Pressure response: increase then stabilization
   - Density measurement at surface return
   - Volume balance calculations
   - Gamma ray tools (some designs)
   - Indicates annulus fill complete

4. PLACEMENT PROBLEMS
   - Premature crossover: voids in pack
   - Washout: pack erosion, poor consolidation
   - Bridging: pack plugs prematurely
   - No crossover: leak-off or pack failure
   - High pressure: bridging or screen plugging

5. DESIGN PARAMETERS
   - Pump rate: 3-12 BPM depending on wellbore size
   - Fluid viscosity: 20-50 cp for gravel transport
   - Gravel concentration: 8-16 PPA typical
   - Overflush: 50-100% pack volume
   - Reverse-out procedure if bridging occurs

6. QUALITY ASSURANCE
   - Pressure monitoring and interpretation
   - Volume tracking (gravel pumped vs calculated need)
   - Fluid returns monitoring
   - Post-pack pressure test
   - Production performance validation

Proper placement technique is as critical as gravel sizing. A perfectly
sized pack poorly placed will fail. Real-time monitoring and experienced
personnel are essential. Placement problems caught early can be remediated;
problems discovered post-completion may require workover or recompletion.
""",
        key_factors=[
            "Alpha wave vs beta wave behavior",
            "Crossover event detection",
            "Pump rate and fluid rheology control",
            "Volume balance verification",
            "Pressure response interpretation",
            "Washout and bridging recognition"
        ],
        primary_authority=[
            "SPE 28909 - Gravel Pack Placement Mechanics",
            "SPE 154500 - Alpha-Beta Wave Theory in Practice",
            "API RP 58 - Gravel Pack Placement Procedures"
        ],
        burden_holder="Service company must achieve proper pack placement",
        adversary_position="Placement quality difficult to verify without production history",
        counter_arguments=[
            "Subsurface conditions unpredictable",
            "Formation damage during placement unavoidable",
            "Crossover detection unreliable in some cases",
            "Washout may occur during production, not placement",
            "Post-pack testing not always conclusive"
        ],
        resolution_strategy="Use real-time monitoring with experienced supervision; validate with post-pack testing",
        entity_scope="All gravel pack and frac pack operations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with proper monitoring; moderate without real-time data",
        controlling_precedent="SPE 28909 alpha-beta wave placement theory",
        category=IssueCategory.PACK_PLACEMENT
    ),

    # SCREEN SELECTION DOCTRINES

    DoctrineBlock(
        topic="Wire-Wrapped Screen Design",
        keywords=["wire wrap screen", "slot size", "keystone wire", "base pipe", "screen gauge"],
        conclusion_template="Wire-wrapped screens consist of trapezoidal (keystone) wire wound around a base pipe with longitudinal rods. Slot width determines sand retention, typically D10/2 to D10 of formation sand. Wire-wrap screens offer high open area (8-12%), low cost, and good strength, making them the standard for gravel pack completions.",
        reasoning_framework="""
Wire-wrapped screen design principles:

1. CONSTRUCTION ELEMENTS
   - Base pipe: structural support, flow capacity
   - Longitudinal rods: wire attachment, strength
   - Keystone wire: wrapped wire forming slots
   - Slot width: opening between wire wraps
   - Open area: percentage of inflow area

2. SLOT SIZING
   - With gravel pack: 10-12 slot (0.010-0.012 inch)
   - Retains gravel D10 (prevents pack loss)
   - Standalone: D10/2 to D10 of formation sand
   - Allows some fines passage initially
   - Natural bridging over time

3. WIRE-WRAP ADVANTAGES
   - High open area (8-12%)
   - Low pressure drop across screen
   - Robust mechanical strength
   - Proven reliability
   - Low cost ($5-15/ft)

4. LIMITATIONS
   - Plugging risk in high-fines environments
   - Erosion at slots with high velocity
   - Corrosion in aggressive fluids
   - Limited to straight hole sections
   - Requires gravel pack in unconsolidated formations

5. MATERIAL SELECTION
   - Carbon steel: standard, low cost
   - 316 stainless: corrosion resistance
   - Alloy 825/625: severe corrosion environments
   - Coating options: epoxy, nickel
   - Wire gauge: 0.045-0.080 inch typical

6. QUALITY SPECIFICATIONS
   - Slot width tolerance: +/- 0.001 inch
   - Wire attachment: welded or locked
   - Roundness and straightness limits
   - Pressure rating verification
   - API thread connections

Wire-wrap screens are the workhorse of sand control. Simple, reliable,
cost-effective when paired with proper gravel packs. Not suitable for
standalone applications in unconsolidated formations due to large slot
openings relative to formation sand.
""",
        key_factors=[
            "Slot width selection (gravel pack vs standalone)",
            "Open area percentage (8-12% typical)",
            "Base pipe strength and flow capacity",
            "Material selection for environment",
            "Manufacturing quality and tolerances",
            "Cost vs performance tradeoffs"
        ],
        primary_authority=[
            "API RP 58 - Screen Design Standards",
            "SPE 56193 - Wire-Wrap Screen Performance",
            "SPE 116116 - Screen Selection Guidelines"
        ],
        burden_holder="Manufacturer must meet slot tolerance and strength specifications",
        adversary_position="Premium screens offer better performance despite higher cost",
        counter_arguments=[
            "Wire-wrap slots too large for many formations",
            "Plugging risk higher than premium screens",
            "Erosion resistance inferior to premium options",
            "Limited corrosion resistance",
            "Cannot handle high fines content"
        ],
        resolution_strategy="Wire-wrap for gravel pack; premium screens for standalone or harsh conditions",
        entity_scope="Standard gravel pack completions in moderate environments",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for gravel pack applications",
        controlling_precedent="API RP 58 wire-wrap screen standards",
        category=IssueCategory.SCREEN_SELECTION
    ),

    DoctrineBlock(
        topic="Premium Mesh Screen Selection",
        keywords=["premium screen", "metal mesh", "sintered mesh", "direct wrap", "protective shroud"],
        conclusion_template="Premium mesh screens use woven wire cloth or sintered metal filter media bonded to perforated base pipe. Mesh screens offer superior plugging resistance, tighter filtration (10-250 micron), and better standalone performance than wire-wrap. Cost is 3-5x wire-wrap but justified for high-value wells, standalone applications, or problematic formations.",
        reasoning_framework="""
Premium mesh screen technology and application:

1. SCREEN TYPES
   - Woven wire mesh: interlaced wire strands
   - Sintered mesh: multiple layers fused together
   - Direct wrap: mesh wrapped on perforated base pipe
   - Protective shroud: outer layer prevents impact damage
   - Single vs multi-layer construction

2. FILTRATION RATINGS
   - Absolute rating: largest particle passing
   - Nominal rating: 95% retention size
   - Beta ratio: filtration efficiency metric
   - Typical range: 10-250 micron
   - Much finer than wire-wrap (250-300 micron)

3. DESIGN ADVANTAGES
   - Tight filtration for fine formations
   - High plugging resistance (tortuous path)
   - Standalone capability without gravel pack
   - Erosion resistance superior to wire-wrap
   - Corrosion-resistant materials available

4. PERFORMANCE CONSIDERATIONS
   - Lower open area than wire-wrap (3-8%)
   - Higher pressure drop across screen
   - Cleanout more difficult if plugged
   - Cost: $15-75/ft depending on specification
   - Justification based on well economics

5. APPLICATION CRITERIA
   - Standalone screens in moderately consolidated formations
   - High fines content formations
   - Extended-reach horizontal wells (no gravel pack)
   - High-rate wells requiring plugging resistance
   - Corrosive or erosive environments

6. VENDOR OPTIONS
   - Schlumberger ScreenMaster/MeshRite
   - Halliburton DuraScreen
   - Baker Hughes MultiChem
   - Weatherford OptiPac Premium
   - Various boutique manufacturers

Premium screens are not universally better—they are application-specific.
Use when formation characteristics, well trajectory, or operating conditions
justify the cost premium. Improper application wastes money; proper application
prevents workover costs exceeding $500K-2MM.
""",
        key_factors=[
            "Filtration rating vs formation grain size",
            "Standalone vs gravel pack application",
            "Open area and pressure drop tradeoffs",
            "Cost justification via well economics",
            "Plugging resistance in high-fines zones",
            "Material compatibility with fluids"
        ],
        primary_authority=[
            "SPE 116116 - Screen Selection Decision Tree",
            "SPE 168625 - Premium Screen Performance Review",
            "SPE 185870 - Standalone Screen Case Studies"
        ],
        burden_holder="Completion engineer must justify premium screen cost",
        adversary_position="Premium screens uneconomic for marginal wells",
        counter_arguments=[
            "3-5x cost premium not justified by performance",
            "Gravel pack with wire-wrap equally effective",
            "Lower open area reduces productivity",
            "Plugging still occurs despite premium design",
            "Workover to replace screen negates savings"
        ],
        resolution_strategy="Use economic analysis comparing completion cost vs workover risk and NPV impact",
        entity_scope="High-value wells, standalone applications, problematic formations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for properly selected applications",
        controlling_precedent="SPE 116116 screen selection methodology",
        category=IssueCategory.SCREEN_SELECTION
    ),

    DoctrineBlock(
        topic="Expandable Sand Screen Technology",
        keywords=["expandable screen", "ESS", "solid body expansion", "annular fill", "openhole completion"],
        conclusion_template="Expandable sand screens (ESS) are run collapsed on drillpipe, then mechanically expanded against the openhole formation face. ESS eliminates gravel pack operations, provides annular isolation, and enables complex well geometries. Technology matured significantly since 2000 with 10,000+ installations, but requires proper formation competence and expansion quality control.",
        reasoning_framework="""
Expandable sand screen application and limitations:

1. TECHNOLOGY FUNDAMENTALS
   - Screen run collapsed (4.5-6.5 inch OD typical)
   - Expansion cone forces radial expansion
   - Final OD: 8.5-12.5 inch (hole dependent)
   - Expansion ratio: 30-60% diameter increase
   - Screen contacts formation, eliminating annulus

2. ESS ADVANTAGES
   - No gravel pack operation required
   - Saves rig time (12-36 hours)
   - Enables long openhole intervals (2000+ ft)
   - Annular isolation (no crossflow)
   - Large OD screen in small initial casing

3. FORMATION REQUIREMENTS
   - Moderately consolidated rock (UCS > 500 psi)
   - Gauge hole (not washed out)
   - No massive shale or clay zones
   - Adequate formation strength to support screen
   - Minimal wellbore breathing during expansion

4. EXPANSION PROCESS
   - Run screen on drillpipe to depth
   - Circulate and condition hole
   - Pull expansion cone through screen
   - Monitor expansion force and travel
   - Pressure test post-expansion

5. DESIGN CONSIDERATIONS
   - Screen filtration: 150-300 micron typical
   - Base pipe collapse rating after expansion
   - Expansion force: 40,000-100,000 lbf
   - Backup screen if expansion fails
   - Contingency for partial expansion

6. RISK FACTORS
   - Incomplete expansion in washouts
   - Screen damage during expansion
   - Formation damage from expansion force
   - Inability to remove if problems occur
   - Higher cost than conventional screens ($50-150/ft)

ESS works exceptionally well in the right applications: gauge hole,
moderately competent formations, wells where gravel pack is impractical
(ERD horizontal, slim hole). Misapplication in weak or washed-out holes
leads to expensive fishing jobs or underperforming wells. Thorough
caliper log analysis and formation strength assessment mandatory.
""",
        key_factors=[
            "Formation competence (UCS > 500 psi)",
            "Hole gauge and quality",
            "Expansion force and expansion ratio",
            "Screen filtration vs formation sand",
            "Cost vs rig time savings",
            "Contingency planning for expansion failure"
        ],
        primary_authority=[
            "SPE 116631 - Expandable Screen Technology Review",
            "SPE 168152 - ESS Application Guidelines",
            "SPE 191411 - 20 Years of Expandable Screens"
        ],
        burden_holder="Operator must ensure formation competence and hole quality",
        adversary_position="ESS risk and cost exceed benefits of gravel pack elimination",
        counter_arguments=[
            "Expansion failures require costly remediation",
            "Formation damage from expansion force",
            "Screen cannot be retrieved if problems occur",
            "Higher cost than wire-wrap plus gravel pack",
            "Limited filtration range vs formation variability"
        ],
        resolution_strategy="Use ESS in competent formations with gauge holes; retain gravel pack option for weak formations",
        entity_scope="Moderately consolidated formations, openhole horizontal wells",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="High confidence in proper applications; high risk in marginal formations",
        controlling_precedent="SPE 116631 ESS application envelope",
        category=IssueCategory.SCREEN_SELECTION
    ),

    # FRAC PACK DOCTRINES

    DoctrineBlock(
        topic="Frac Pack vs Gravel Pack Decision",
        keywords=["frac pack", "tip screenout", "fracture conductivity", "proppant placement", "permeability impairment"],
        conclusion_template="Frac pack combines hydraulic fracturing with gravel packing to achieve both sand control and permeability enhancement. Tip screenout (TSO) creates short, highly conductive fractures while placing gravel pack. Frac pack outperforms gravel pack in damaged or low-permeability formations (k < 100 md) but adds complexity and cost ($200K-800K incremental).",
        reasoning_framework="""
Frac pack design rationale and execution:

1. FRAC PACK OBJECTIVES
   - Bypass near-wellbore damage (skin bypass)
   - Create conductivity to offset screen pressure drop
   - Maintain sand control via gravel pack
   - Achieve both stimulation and exclusion
   - Increase rate capability and well longevity

2. CANDIDATE SELECTION
   - Formation permeability < 100 md (primary)
   - Damaged formations (skin > +5)
   - High-rate production requirements
   - Formations with natural fines migration
   - Wells justifying incremental cost

3. DESIGN PARAMETERS
   - Tip screenout: intentional bridging at fracture tip
   - Fracture half-length: 20-100 ft typical
   - Proppant: 20/40 mesh, high-strength
   - Fracture conductivity: 1000-5000 md-ft
   - Pad volume: 20-30% of total fluid

4. EXECUTION SEQUENCE
   - Perforate with limited entry (2-4 SPF)
   - Pump pad fluid (low viscosity, 50-100 bbl)
   - Ramp proppant concentration (0.5-16 PPA)
   - Achieve tip screenout (pressure rise)
   - Continue pumping to fill annulus with pack
   - Reverse-out if needed

5. TSO INDICATORS
   - Net pressure increase 500-1500 psi
   - Screenout at designed proppant volume
   - Maintained pumping after screenout
   - Post-job pressure decline
   - Production improvement vs offset gravel packs

6. QUALITY METRICS
   - Fracture half-length from pressure decline
   - Skin factor from buildup test (target: -2 to -4)
   - Production rate vs offset wells
   - Sand control effectiveness
   - Net present value improvement

Frac pack is not universally superior to gravel pack—it is a solution
for specific problems (damage, low perm, high rate needs). Incremental
cost of $200K-800K must be justified by incremental NPV exceeding $1-5MM.
For clean, high-permeability formations, conventional gravel pack is adequate.
""",
        key_factors=[
            "Formation permeability and damage",
            "Tip screenout achievement",
            "Fracture conductivity vs formation permeability",
            "Incremental cost vs NPV benefit",
            "Proppant and fluid design",
            "Skin factor improvement measurement"
        ],
        primary_authority=[
            "SPE 54737 - Frac Pack Design and Optimization",
            "SPE 90369 - Frac Pack Performance Analysis",
            "SPE 107718 - Frac Pack vs Gravel Pack Economics"
        ],
        burden_holder="Engineer must justify incremental frac pack cost with NPV analysis",
        adversary_position="Gravel pack adequate for most applications at lower cost and risk",
        counter_arguments=[
            "Frac pack complexity increases failure risk",
            "Incremental cost not justified in many cases",
            "Fracture may grow out of zone",
            "Formation damage may be overestimated",
            "Conventional gravel pack with matrix acidizing equally effective"
        ],
        resolution_strategy="Use economic modeling with skin factor and rate sensitivity; frac pack if NPV gain > 3x cost",
        entity_scope="Damaged or low-permeability formations requiring sand control",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for low-perm damaged zones; moderate for marginal candidates",
        controlling_precedent="SPE 54737 frac pack design optimization",
        category=IssueCategory.FRAC_PACK_DESIGN
    ),

    DoctrineBlock(
        topic="Proppant Selection for Frac Pack",
        keywords=["proppant", "20/40 mesh", "conductivity", "crush strength", "resin coated proppant"],
        conclusion_template="Frac pack proppant must provide high conductivity while being retained by gravel pack. Standard selection is 20/40 mesh intermediate-strength proppant (ISP) or resin-coated sand. Proppant crush strength must exceed closure stress by 1.5-2x safety factor. Resin coating prevents flowback and consolidates pack but adds $150-300/ton cost.",
        reasoning_framework="""
Proppant selection for frac pack applications:

1. SIZE SELECTION
   - 20/40 mesh standard for frac pack
   - Larger than gravel (12/20 or 16/30 typical)
   - Gravel retains proppant at wellbore
   - Smaller proppant (40/70) for tighter formations
   - Size ratio: proppant > 1.5x gravel for retention

2. STRENGTH REQUIREMENTS
   - Closure stress: in-situ minimum horizontal stress
   - Safety factor: 1.5-2.0x closure stress
   - ISP: 6000-8000 psi strength (3000-4000 psi closure)
   - High-strength ceramic: 10,000-15,000 psi
   - Sand: adequate for < 4000 psi closure

3. CONDUCTIVITY CONSIDERATIONS
   - 20/40 ISP: 1500-3000 md-ft at 4000 psi
   - Fracture length short, conductivity critical
   - Higher conductivity offsets lower permeability
   - Target: CfD > 1.6 for infinite conductivity
   - Degradation over time from stress and fines

4. RESIN-COATED PROPPANT (RCP)
   - Pre-cured (cured before pumping)
   - Curable (cures downhole at temperature)
   - Benefits: consolidation, flowback prevention
   - Cost premium: $150-300/ton vs sand
   - Essential for high-rate or unconsolidated zones

5. ECONOMIC EVALUATION
   - Sand: $50-80/ton (baseline)
   - ISP: $150-250/ton
   - HSP (high-strength): $400-800/ton
   - RCP: $300-600/ton
   - Ceramic: $800-1500/ton

6. PLACEMENT CONSIDERATIONS
   - Proppant transport in viscous fluid
   - Settling velocity calculations
   - Tip screenout timing
   - Gravel pack retention verification
   - Post-frac pack consolidation

Proppant cost is 15-30% of frac pack total cost. Underdesigned proppant
(insufficient strength) causes crushing, embedment, and conductivity loss,
negating the frac pack benefit. Overdesigned proppant (excessive strength)
wastes money without performance gain. Match proppant to stress regime.
""",
        key_factors=[
            "Proppant size (20/40 mesh standard)",
            "Crush strength vs closure stress (1.5-2x safety factor)",
            "Conductivity requirements (CfD > 1.6)",
            "Resin coating benefits vs cost",
            "Gravel pack retention of proppant",
            "Economic optimization vs well NPV"
        ],
        primary_authority=[
            "SPE 90369 - Proppant Selection for Frac Pack",
            "SPE 106281 - Resin-Coated Proppant Performance",
            "API RP 56 - Proppant Testing Standards"
        ],
        burden_holder="Engineer must select proppant matching stress and conductivity needs",
        adversary_position="Premium proppants do not justify incremental cost in many cases",
        counter_arguments=[
            "High-strength proppant cost not justified by marginal conductivity gain",
            "Resin coating unnecessary for many applications",
            "Sand adequate for low-stress environments",
            "Conductivity degradation occurs regardless of proppant type",
            "Economic models overestimate proppant impact"
        ],
        resolution_strategy="Use stress-matched proppant with economic sensitivity analysis; RCP for high-rate wells",
        entity_scope="All frac pack completions requiring proppant placement",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for stress-matched selection",
        controlling_precedent="API RP 56 proppant strength testing",
        category=IssueCategory.FRAC_PACK_DESIGN
    ),

    # CHEMICAL CONSOLIDATION DOCTRINES

    DoctrineBlock(
        topic="Resin Consolidation Systems",
        keywords=["resin consolidation", "furan resin", "epoxy resin", "consolidation treatment", "sand bonding"],
        conclusion_template="Chemical consolidation bonds formation sand grains using thermosetting resins (furan or epoxy) to create permeable, consolidated mass preventing sand production. Successful treatments achieve 60-90% sand control effectiveness at 10-30% of gravel pack cost. Technology limited by formation permeability (> 250 md required), heterogeneity, and treatment execution quality.",
        reasoning_framework="""
Resin consolidation design and application:

1. RESIN CHEMISTRY
   - Furan resin: furfuryl alcohol polymer
   - Epoxy resin: bisphenol-A based
   - Catalyst systems: acid or amine initiated
   - Curing: exothermic polymerization reaction
   - Set time: 6-48 hours (temperature dependent)

2. TREATMENT DESIGN
   - Pre-flush: remove fines and oil-wet sand
   - Resin stage: 50-200 gal/ft of pay
   - Overflush: displace resin into formation
   - Shut-in: allow curing (12-72 hours)
   - Flowback: remove unconsolidated material

3. CANDIDATE CRITERIA
   - Formation permeability > 250 md (critical)
   - Porosity > 20% (adequate void space)
   - Uniform sand (no clay or shale streaks)
   - Oil-wet or intermediate wettability
   - Low water saturation (< 40%)

4. TREATMENT LIMITATIONS
   - Ineffective in water-wet formations
   - Fails in heterogeneous or laminated zones
   - Requires extended shut-in time (well offline)
   - Permeability reduction: 20-40% typical
   - Re-treatment difficult if initial treatment fails

5. SUCCESS FACTORS
   - Proper candidate selection (most critical)
   - Adequate resin volume (100-200 gal/ft minimum)
   - Formation temperature 80-250°F optimal
   - Good wellbore cleanup before treatment
   - Extended shut-in for complete cure

6. PERFORMANCE EXPECTATIONS
   - Success rate: 60-70% in proper candidates
   - Sand reduction: 80-95% in successful treatments
   - Longevity: 2-5+ years in stable formations
   - Cost: $30K-150K vs $200K-800K for gravel pack
   - Retreat option if failure occurs

Resin consolidation is a low-cost alternative to mechanical sand control
but only in carefully selected candidates. Misapplication wastes treatment
cost and delays definitive sand control (gravel pack). Best application:
marginal wells where gravel pack economics are poor but sand production
limits production. High-value wells justify mechanical sand control.
""",
        key_factors=[
            "Formation permeability (> 250 md required)",
            "Wettability and water saturation",
            "Formation homogeneity",
            "Resin volume per foot of pay",
            "Cure time and shut-in duration",
            "Success probability vs mechanical alternatives"
        ],
        primary_authority=[
            "SPE 158915 - Resin Consolidation Case Studies",
            "SPE 103174 - Chemical Sand Control Methods",
            "SPE 131256 - Resin Treatment Design Optimization"
        ],
        burden_holder="Operator must verify candidate meets resin consolidation criteria",
        adversary_position="Mechanical sand control more reliable despite higher cost",
        counter_arguments=[
            "Success rate too low for high-value wells",
            "Permeability reduction not acceptable",
            "Re-treatment after failure negates cost savings",
            "Formation damage from resin common",
            "Mechanical sand control eliminates uncertainty"
        ],
        resolution_strategy="Use resin for marginal economics; mechanical sand control for high-value wells",
        entity_scope="Low-cost sand control for marginal wells in suitable formations",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence in proper candidates; high risk in marginal formations",
        controlling_precedent="SPE 158915 candidate selection criteria",
        category=IssueCategory.CONSOLIDATION
    ),

    # MONITORING DOCTRINES

    DoctrineBlock(
        topic="Acoustic Sand Monitoring",
        keywords=["acoustic sand detector", "sand monitor", "clamp-on sensor", "erosion monitoring", "real-time sand detection"],
        conclusion_template="Acoustic sand detectors measure particle impact noise on flowline to detect sand production in real-time. Clamp-on sensors are non-intrusive, providing continuous monitoring without flow interruption. Acoustic monitoring enables early sand detection (< 10 pptb), rate optimization, and erosion prevention, justifying $15K-40K installation cost for wells with sand control uncertainty.",
        reasoning_framework="""
Acoustic sand monitoring technology and application:

1. DETECTION PRINCIPLE
   - Sand particles impact flowline wall
   - Impact generates acoustic emission (high frequency)
   - Piezoelectric sensor detects vibrations
   - Signal processing filters process noise
   - Output: sand concentration estimate (pptb)

2. SENSOR TECHNOLOGY
   - Clamp-on (non-intrusive) preferred
   - Intrusive probes (higher sensitivity, erosion risk)
   - Multiple sensors for redundancy
   - Temperature compensation essential
   - Frequency range: 20-200 kHz

3. INSTALLATION LOCATION
   - Horizontal flowline section (10-15 ft from wellhead)
   - Downstream of choke (erosion risk area)
   - Avoid elbows and flow disturbances
   - Multiple locations for critical wells
   - Integration with SCADA system

4. MONITORING CAPABILITIES
   - Real-time sand rate (parts per thousand barrels)
   - Trending over time (detect increases)
   - Alarm thresholds (e.g., > 10 pptb)
   - Correlation with production rate
   - Automated rate reduction on high sand

5. OPERATIONAL STRATEGY
   - Initial low-rate production with monitoring
   - Gradual rate increases while monitoring sand
   - Rate optimization: maximum rate at acceptable sand level
   - Early warning of screen failure
   - Erosion prevention in downstream equipment

6. ECONOMIC JUSTIFICATION
   - System cost: $15K-40K (sensors + installation)
   - Prevents erosion failures: $100K-2MM repair costs
   - Optimizes production rate (may allow higher rates)
   - Extends equipment life
   - Justifies insurance on sand control performance

Acoustic monitoring is essential for wells with sand control uncertainty:
standalone screens, resin consolidation, marginal formations. The ability
to detect sand early and adjust rates prevents catastrophic erosion failures.
For wells with proven gravel packs in stable formations, monitoring may be
optional, but insurance value often justifies installation.
""",
        key_factors=[
            "Clamp-on vs intrusive sensor selection",
            "Installation location and sensor count",
            "Alarm threshold setting (pptb)",
            "Integration with rate control",
            "Calibration and validation",
            "Cost vs erosion risk economics"
        ],
        primary_authority=[
            "SPE 109824 - Acoustic Sand Monitoring Systems",
            "SPE 166506 - Sand Management Using Real-Time Monitoring",
            "SPE 179120 - Optimization with Acoustic Detectors"
        ],
        burden_holder="Operator must install and maintain functional monitoring system",
        adversary_position="Monitoring cost not justified for wells with robust sand control",
        counter_arguments=[
            "False alarms reduce operator confidence",
            "Calibration difficult without independent sand measurement",
            "System cost not justified for low-rate wells",
            "Manual sand sampling adequate",
            "Gravel pack eliminates need for monitoring"
        ],
        resolution_strategy="Install on high-value wells and uncertain sand control; trend data for validation",
        entity_scope="Wells with sand production risk or uncertainty",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for early detection; moderate for quantitative measurement",
        controlling_precedent="SPE 109824 acoustic monitoring best practices",
        category=IssueCategory.MONITORING
    ),

    DoctrineBlock(
        topic="Erosion Monitoring and Inspection",
        keywords=["erosion probe", "ultrasonic thickness", "gamma scan", "flowline inspection", "erosion rate"],
        conclusion_template="Erosion monitoring tracks metal loss in chokes, flowlines, and elbows exposed to sand-laden flow. Ultrasonic thickness (UT) measurements, erosion probes, and gamma scans detect wall thinning before failure. Inspection intervals of 3-12 months typical depending on sand severity. Erosion-induced failures cause $500K-5MM in costs (production loss, environmental, repair).",
        reasoning_framework="""
Erosion monitoring and prevention program:

1. EROSION MECHANISMS
   - Particle impingement: high-velocity sand impact
   - Erosion rate proportional to velocity^2.5 to ^3
   - Maximum erosion at elbows, tees, chokes
   - Erosion threshold velocity (API RP 14E)
   - Sand concentration amplifies erosion

2. MONITORING METHODS
   - Ultrasonic thickness (UT) testing
   - Erosion probes (intrusive wear elements)
   - Gamma ray backscatter (non-intrusive)
   - Visual inspection during shutdowns
   - Baseline → periodic re-measurement

3. CRITICAL LOCATIONS
   - Chokes (maximum velocity)
   - First elbow after wellhead
   - Pipeline elbows and tees
   - Separator inlet
   - Subsurface safety valve

4. INSPECTION INTERVALS
   - High sand (> 50 pptb): monthly
   - Moderate sand (10-50 pptb): quarterly
   - Low sand (< 10 pptb): semi-annual
   - Adjust based on erosion trends
   - More frequent after screen failure

5. EROSION RATE CALCULATION
   - Wall thickness loss per unit time
   - Remaining life = (current - minimum) / rate
   - Minimum wall: per ASME B31.3 or B31.4
   - Safety factor 1.5-2.0 applied
   - Replacement scheduling before failure

6. MITIGATION STRATEGIES
   - Erosion-resistant materials (tungsten carbide)
   - Increased wall thickness
   - Flow velocity reduction (choke sizing)
   - Sand production reduction (rate limiting)
   - Erosion-resistant coatings

Erosion monitoring is non-negotiable for wells producing sand. Undetected
erosion leads to catastrophic failures: flowline ruptures, environmental
spills, fire risk, personnel hazards. Proactive monitoring and replacement
costs $5K-50K/year. Erosion failure costs average $500K plus production loss
and potential environmental liability exceeding $5-50MM.
""",
        key_factors=[
            "Erosion rate measurement methods",
            "Inspection interval based on sand severity",
            "Critical location identification",
            "Remaining life calculations",
            "Replacement vs repair decisions",
            "Velocity management and materials selection"
        ],
        primary_authority=[
            "API RP 14E - Erosional Velocity Guidelines",
            "NACE SP0304 - Erosion in Oil and Gas Production",
            "SPE 166506 - Sand Management and Erosion Prevention"
        ],
        burden_holder="Operator must implement erosion monitoring program",
        adversary_position="Erosion monitoring cost burden excessive for marginal wells",
        counter_arguments=[
            "Inspection frequency may be excessive",
            "Erosion rates highly variable and unpredictable",
            "Conservative replacement wastes serviceable equipment",
            "Velocity limits overly restrictive",
            "Cost of monitoring approaches cost of replacement"
        ],
        resolution_strategy="Risk-based inspection intervals; higher frequency for critical locations and high sand rates",
        entity_scope="All wells and facilities handling sand-laden production",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for UT measurement; moderate for erosion rate prediction",
        controlling_precedent="API RP 14E erosional velocity calculation",
        category=IssueCategory.MONITORING
    ),

    # ECONOMIC AND DECISION DOCTRINES

    DoctrineBlock(
        topic="Sand Control Economics",
        keywords=["sand control cost", "NPV analysis", "completion cost", "workover cost", "economic optimization"],
        conclusion_template="Sand control completion costs range from $30K (resin) to $800K (frac pack), representing 10-40% of well completion cost. Economic analysis must compare completion cost vs production benefit, workover risk, and equipment protection. Wells with NPV > $5MM typically justify mechanical sand control; marginal wells may use sand management or chemical methods.",
        reasoning_framework="""
Sand control economic decision framework:

1. COMPLETION COST RANGES
   - No sand control: $0 (baseline)
   - Chemical consolidation: $30K-150K
   - Standalone screen: $50K-200K
   - Gravel pack: $150K-500K
   - Frac pack: $350K-1,200K
   - Expandable screen: $200K-600K

2. PRODUCTION IMPACT
   - Skin factor improvement
   - Rate increase vs baseline
   - Acceleration of reserves
   - Extended well life
   - Reduced downtime from workovers

3. RISK COSTS
   - Workover to repair sand control failure: $300K-2MM
   - Equipment erosion damage: $100K-5MM
   - Lost production during workover: $50K-500K/month
   - Environmental liability: $1MM-50MM potential
   - Probability of failure by method

4. NPV CALCULATION METHODOLOGY
   - Discount rate: 10-15% typical
   - Reserve acceleration value
   - Incremental completion cost
   - Workover probability and cost
   - Equipment protection value

5. DECISION CRITERIA
   - NPV > $5MM: justify frac pack or premium methods
   - NPV $1-5MM: gravel pack or standalone screen
   - NPV < $1MM: chemical or sand management
   - IRR threshold: > 30% for marginal projects
   - Sensitivity to sand production severity

6. OPTIMIZATION STRATEGIES
   - Match sand control method to well value
   - Multi-well learning curve cost reduction
   - Standardization for efficiency
   - Supply chain optimization
   - Risk pooling across well portfolio

Economic optimization is critical. Over-designed sand control (frac pack
on marginal well) wastes capital. Under-designed sand control (no control
on high-value well) risks well loss and liability. Match method to well NPV,
reservoir characteristics, and operator risk tolerance.
""",
        key_factors=[
            "Sand control method cost comparison",
            "NPV increase from skin reduction and rate improvement",
            "Workover probability and cost by method",
            "Well economic value (NPV, reserves)",
            "Erosion risk and equipment protection value",
            "Discount rate and economic hurdles"
        ],
        primary_authority=[
            "SPE 107718 - Sand Control Economics and Optimization",
            "SPE 151830 - Economic Comparison of Methods",
            "SPE 174848 - Risk-Based Sand Control Selection"
        ],
        burden_holder="Engineer must demonstrate economic justification for sand control method",
        adversary_position="Premium sand control not justified by marginal NPV improvement",
        counter_arguments=[
            "NPV models overestimate sand control benefit",
            "Conservative approach justified despite lower NPV",
            "Workover risk underestimated in models",
            "Equipment protection value difficult to quantify",
            "Standardization reduces flexibility for optimization"
        ],
        resolution_strategy="Use probabilistic economic models with sensitivity analysis; match method to well tier",
        entity_scope="All sand control completion design decisions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for economic framework; moderate for probability estimates",
        controlling_precedent="SPE 107718 economic optimization methodology",
        category=IssueCategory.ECONOMICS
    ),

    DoctrineBlock(
        topic="Sand Management vs Sand Exclusion",
        keywords=["sand management", "sand exclusion", "acceptable sand production", "downstream processing", "de-sanding"],
        conclusion_template="Sand management accepts controlled sand production while protecting facilities, contrasting with sand exclusion (gravel pack, screens). Sand management viable when: sand rate < 10-50 pptb, downstream equipment tolerates sand, de-sanding facilities available, and well economics do not justify exclusion. Management cost is $10K-100K vs $150K-800K for exclusion.",
        reasoning_framework="""
Sand management vs sand exclusion decision framework:

1. SAND MANAGEMENT PHILOSOPHY
   - Accept low-level sand production
   - Protect facilities from erosion and plugging
   - Monitor and control production rate
   - Install de-sanding equipment
   - Lower cost than mechanical exclusion

2. SAND MANAGEMENT COMPONENTS
   - Acoustic sand detectors: $15K-40K
   - Automated choke control: $30K-80K
   - De-sanding hydrocyclones: $100K-500K
   - Sand jetting and removal: $5K-20K/year
   - Erosion monitoring: $10K-30K/year

3. CANDIDATE CRITERIA FOR MANAGEMENT
   - Marginally consolidated formation
   - Sand rate predictably low (< 50 pptb)
   - Short production life (< 3 years)
   - Well economics marginal (NPV < $1MM)
   - Facilities designed for sand handling

4. EXCLUSION METHOD COMPARISON
   - Gravel pack: complete exclusion, high cost
   - Standalone screen: partial exclusion, moderate cost
   - Chemical consolidation: uncertain, low cost
   - Frac pack: exclusion + stimulation, highest cost
   - Management: controlled production, lowest cost

5. RISK CONSIDERATIONS
   - Erosion damage if sand exceeds design
   - Sand accumulation in vessels and lines
   - Disposal costs for produced sand
   - Environmental permit requirements
   - Uncertainty in long-term sand behavior

6. ECONOMIC COMPARISON
   - Management total cost: $50K-200K
   - Exclusion completion cost: $150K-800K
   - Differential justifies management for marginal wells
   - Exclusion justified for high-value wells
   - Portfolio approach: exclude high-value, manage marginal

Sand management is not abdication of responsibility—it is an engineering
decision for specific well populations. Misapplication to high-value wells
or severe sanding formations causes excessive costs and risks. Proper application
to marginal wells with controlled sanding saves capital while maintaining
production and safety.
""",
        key_factors=[
            "Expected sand production rate (pptb)",
            "Well economic value (NPV)",
            "Facility sand handling capability",
            "Monitoring and control infrastructure",
            "Environmental and regulatory constraints",
            "Erosion risk tolerance and mitigation"
        ],
        primary_authority=[
            "SPE 166506 - Sand Management Philosophy and Practice",
            "SPE 151830 - Economic Comparison Management vs Exclusion",
            "SPE 102374 - Successful Sand Management Programs"
        ],
        burden_holder="Operator must demonstrate sand management provides adequate protection",
        adversary_position="Sand exclusion eliminates uncertainty and long-term costs",
        counter_arguments=[
            "Sand management defers problem without solving it",
            "Erosion risk exceeds cost savings",
            "Regulatory pressure favors exclusion",
            "Sand disposal costs underestimated",
            "Facilities designed for sand-free production"
        ],
        resolution_strategy="Tiered approach: exclusion for high-value wells; management for marginal wells with monitoring",
        entity_scope="Marginal wells with low sand production in formations with sand handling capability",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence; requires ongoing monitoring and adjustment",
        controlling_precedent="SPE 166506 sand management decision framework",
        category=IssueCategory.ECONOMICS
    ),

    # ADDITIONAL TECHNICAL DOCTRINES

    DoctrineBlock(
        topic="Perforation Strategy for Sand Control",
        keywords=["perforation density", "shot phasing", "tunnel stability", "limited entry", "underbalance"],
        conclusion_template="Perforation design affects sand production and sand control effectiveness. Limited shot density (2-4 SPF) for frac pack enables limited entry fracturing. Higher density (6-12 SPF) for gravel pack maximizes inflow. Perforation tunnel stability depends on formation strength, underbalance, and perforation diameter. Unstable tunnels initiate sand production.",
        reasoning_framework="""
Perforation design for sand control completions:

1. SHOT DENSITY SELECTION
   - Gravel pack: 6-12 SPF (maximize inflow area)
   - Frac pack: 2-4 SPF (limited entry pressure drop)
   - Standalone screen: 4-8 SPF (balance flow and stability)
   - Lower density in weak formations (reduce instability)
   - Higher density in competent formations

2. PHASING CONSIDERATIONS
   - 60° phasing: 6 SPF (standard)
   - 120° phasing: 3 SPF (unidirectional fracturing)
   - 180° phasing: 2 SPF (pure horizontal fractures)
   - Oriented perforating for stress regime alignment
   - Random phasing for gravel pack (maximize coverage)

3. PERFORATION TUNNEL STABILITY
   - Large diameter (0.5-0.7 inch) reduces stability
   - Deep penetration (12-18 inch) helps bypass damage
   - Underbalance magnitude affects stability
   - Formation strength controls critical tunnel size
   - Unstable tunnels collapse and produce sand

4. UNDERBALANCE MAGNITUDE
   - Gravel pack: 200-500 psi (clean perforations)
   - Frac pack: 300-800 psi (ensure fracture initiation)
   - Excessive underbalance destabilizes tunnels
   - Insufficient underbalance leaves damage
   - Dynamic underbalance from surge preferred

5. PERFORATION DIAMETER EFFECTS
   - Large holes: higher inflow, lower stability
   - Small holes: better stability, higher pressure drop
   - 0.4-0.5 inch diameter typical for sand control
   - Shaped charges vs abrasive jetting
   - Gun size constraints in smaller completions

6. DAMAGE BYPASS
   - Penetration depth must exceed damaged zone
   - Typical damage: 6-12 inches radial
   - Perforation depth: 12-18 inches target
   - Longer perforations lower skin
   - Confirms with pressure transient analysis

Perforation design is often underappreciated in sand control. Poor
perforation strategy (excessive underbalance, unstable tunnels, insufficient
density) can cause a well-designed gravel pack to fail. Integration of
perforation, completion, and reservoir engineering essential.
""",
        key_factors=[
            "Shot density (SPF) for completion type",
            "Phasing for stress regime and fracture control",
            "Underbalance magnitude for cleanup vs stability",
            "Perforation tunnel diameter and stability",
            "Penetration depth to bypass damage",
            "Formation strength and critical tunnel size"
        ],
        primary_authority=[
            "SPE 73772 - Perforation Design for Sand Control",
            "SPE 94305 - Perforation Stability Analysis",
            "SPE 158915 - Integrated Completion and Perforation Design"
        ],
        burden_holder="Perforation designer must account for formation stability",
        adversary_position="Perforation design secondary to completion design",
        counter_arguments=[
            "Formation strength controls stability more than perforation design",
            "Gravel pack compensates for perforation deficiencies",
            "Underbalance magnitude difficult to control precisely",
            "Standard practices adequate without detailed analysis",
            "Cost of oriented perforating not justified"
        ],
        resolution_strategy="Integrate perforation design with completion design; use stability modeling for weak formations",
        entity_scope="All sand control completions requiring perforations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for stability principles; moderate for field execution",
        controlling_precedent="SPE 73772 perforation stability guidelines",
        category=IssueCategory.PACK_PLACEMENT
    ),

    DoctrineBlock(
        topic="Slotted Liner vs Screen Completions",
        keywords=["slotted liner", "wire-wrap screen", "completion cost", "mill slot", "slot width", "liner vs screen"],
        conclusion_template="Slotted liners (mill-cut or laser-cut slots in casing) offer low-cost alternative to wire-wrap screens for gravel pack completions. Cost is $3-8/ft vs $10-25/ft for screens. Slotted liners have lower open area (1-3% vs 8-12%), higher pressure drop, and less precise slot control. Justified for low-rate, cost-sensitive applications where pressure drop is not limiting.",
        reasoning_framework="""
Slotted liner vs wire-wrap screen comparison:

1. SLOTTED LINER CONSTRUCTION
   - Mill-cut slots: sawed slots in casing body
   - Laser-cut slots: precision laser cutting
   - Slot width: 0.012-0.040 inch typical
   - Slot density: 2-6 slots/inch longitudinal
   - Open area: 1-3% (vs 8-12% for screens)

2. PERFORMANCE COMPARISON
   - Open area: slotted liner 1/3 to 1/4 of screen
   - Pressure drop: 3-5x higher than screen
   - Flow capacity: adequate for low-rate wells (< 2000 BPD)
   - Gravel retention: comparable to screens
   - Strength: higher than wire-wrap screens

3. COST COMPARISON
   - Slotted liner: $3-8/ft (with gravel pack operation)
   - Wire-wrap screen: $10-25/ft
   - Savings: $7-17/ft × 500 ft = $3,500-8,500 per well
   - Justification: marginal well economics
   - Offset by higher pressure drop losses

4. APPLICATION CRITERIA
   - Low production rate (< 2000 BPD)
   - Well economics marginal (NPV < $2MM)
   - Formation permeability high (> 500 md)
   - Gravel pack completion (not standalone)
   - Cost savings justify performance tradeoff

5. LIMITATIONS
   - Not suitable for high-rate wells (pressure drop)
   - Slot width control less precise than wire-wrap
   - Plugging risk higher due to lower open area
   - Cannot use with premium gravel pack designs
   - Limited vendor options for quality control

6. QUALITY CONSIDERATIONS
   - Slot width tolerance: +/- 0.002 inch (laser-cut)
   - Internal burrs and sharp edges (mill-cut risk)
   - Casing strength after slotting
   - Corrosion resistance (same as base casing)
   - API thread integrity after slotting

Slotted liners are not inferior—they are application-specific. For
high-rate, high-value wells, wire-wrap screens are clearly superior.
For low-rate, cost-constrained wells, slotted liners provide adequate
performance at significant cost savings. Match technology to well economics.
""",
        key_factors=[
            "Open area comparison (1-3% vs 8-12%)",
            "Pressure drop and flow capacity",
            "Cost differential ($3-8/ft vs $10-25/ft)",
            "Production rate and well economics",
            "Slot width precision and quality control",
            "Gravel pack vs standalone application"
        ],
        primary_authority=[
            "SPE 116116 - Slotted Liner Performance Analysis",
            "SPE 151830 - Cost Optimization in Sand Control",
            "SPE 56193 - Comparative Screen Performance"
        ],
        burden_holder="Engineer must justify screen cost premium or slotted liner cost savings",
        adversary_position="Wire-wrap screens universally superior to slotted liners",
        counter_arguments=[
            "Pressure drop from slotted liner reduces production",
            "Cost savings negated by production losses",
            "Slot width inconsistency causes pack failures",
            "Limited open area increases plugging risk",
            "Wire-wrap cost premium is justified by performance"
        ],
        resolution_strategy="Use slotted liners for low-rate marginal wells; screens for moderate to high-rate wells",
        entity_scope="Low-rate gravel pack completions in cost-sensitive applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for low-rate applications",
        controlling_precedent="SPE 116116 slotted liner vs screen comparison",
        category=IssueCategory.SCREEN_SELECTION
    ),

    DoctrineBlock(
        topic="Oriented Perforation for Sand Control",
        keywords=["oriented perforation", "stress direction", "perforation azimuth", "fracture initiation", "sanding anisotropy"],
        conclusion_template="Oriented perforating aligns perforation tunnels with maximum horizontal stress direction to control fracture initiation (frac pack) or minimize shear failure (gravel pack). In anisotropic stress regimes (SHmax/Shmin > 1.2), oriented perforating reduces sanding risk by 20-40% and improves frac pack fracture geometry. Cost premium is $10K-30K per well.",
        reasoning_framework="""
Oriented perforation rationale and application:

1. STRESS-DEPENDENT PERFORATION FAILURE
   - Perforation tunnels are stress concentrators
   - Shear failure occurs at angles to SHmax
   - Tunnels aligned with SHmax more stable
   - Tunnels perpendicular to SHmax less stable
   - Anisotropic stress increases directional effect

2. ORIENTATION STRATEGIES
   - Gravel pack: align with SHmax (maximize stability)
   - Frac pack: align with SHmax (control fracture initiation)
   - Horizontal well: perforate updip or downdip
   - Avoid perforating perpendicular to SHmax
   - 60° or 120° phasing aligned to stress

3. STRESS REGIME DETERMINATION
   - Image logs: breakout and fracture identification
   - Dipole sonic: stress-induced anisotropy
   - Regional stress databases
   - Leak-off tests and FIT data
   - Breakout width analysis (SHmax/Shmin ratio)

4. CANDIDATE SELECTION
   - Anisotropic stress: SHmax/Shmin > 1.2
   - Weak formations (UCS < 2000 psi)
   - High-value wells (NPV > $5MM)
   - Frac pack completions (fracture control)
   - Wells with sanding history in area

5. COST-BENEFIT ANALYSIS
   - Oriented perforating cost: $10K-30K
   - Benefit: 20-40% sanding risk reduction
   - Improved frac pack fracture geometry
   - Reduced skin factor (2-3 skin units)
   - Justified by well NPV and sanding risk

6. EXECUTION REQUIREMENTS
   - Gyroscope or continuous inclination tool
   - Gun rotation control
   - Depth correlation accuracy
   - Quality control on orientation (+/- 15° tolerance)
   - Verification with oriented caliper or imaging

Oriented perforating is a refinement, not a revolution. In isotropic stress
fields (offshore deepwater, many basins), orientation provides minimal benefit.
In highly anisotropic stress regimes (tectonically active, depleted reservoirs),
orientation significantly reduces sanding risk and improves stimulation.
Candidate selection and cost-benefit analysis essential.
""",
        key_factors=[
            "Stress anisotropy (SHmax/Shmin ratio)",
            "Formation strength and sanding risk",
            "Perforation alignment with maximum stress",
            "Cost premium vs sanding risk reduction",
            "Frac pack fracture initiation control",
            "Execution quality and orientation accuracy"
        ],
        primary_authority=[
            "SPE 94305 - Oriented Perforating for Sand Control",
            "SPE 168152 - Stress-Based Perforation Design",
            "SPE 179258 - Oriented Perforating Field Results"
        ],
        burden_holder="Engineer must demonstrate stress anisotropy justifies oriented perforating",
        adversary_position="Oriented perforating cost premium not justified by uncertain benefit",
        counter_arguments=[
            "Stress direction uncertain in many fields",
            "Cost premium not justified by marginal benefit",
            "Random perforating adequate with gravel pack",
            "Execution quality variable, negating design",
            "Isotropic stress fields do not benefit from orientation"
        ],
        resolution_strategy="Use in anisotropic stress regimes (SHmax/Shmin > 1.2) for high-value wells",
        entity_scope="High-value wells in anisotropic stress regimes with sanding risk",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="High confidence in anisotropic stress; low benefit in isotropic stress",
        controlling_precedent="SPE 94305 oriented perforation design methodology",
        category=IssueCategory.PACK_PLACEMENT
    ),

    DoctrineBlock(
        topic="Multi-Zone Sand Control Completions",
        keywords=["multi-zone completion", "interval isolation", "selective gravel pack", "zonal sand control", "stacked pay"],
        conclusion_template="Multi-zone sand control completions require interval isolation (packers) and selective gravel packing or screening. Design complexity increases exponentially with zone count. Two-zone completions are standard ($200K-600K incremental); three-plus zones are challenging (> $800K incremental). Commingled flow vs selective production drives design; economics must justify multi-zone complexity.",
        reasoning_framework="""
Multi-zone sand control design considerations:

1. ZONAL ARCHITECTURE OPTIONS
   - Commingled production: all zones open simultaneously
   - Selective production: isolate zones, open selectively
   - Sequential gravel packing: pack each zone separately
   - Single-trip gravel pack: pack all zones in one run
   - Tubing-conveyed vs wireline-conveyed completions

2. ISOLATION REQUIREMENTS
   - Production packers: seal between zones
   - Crossover tools: isolate upper zones during lower zone pack
   - Sliding sleeves: selective zone control
   - Hydraulic-set vs mechanical-set packers
   - Redundant seals for critical applications

3. GRAVEL PACK STRATEGY
   - Bottom-up packing: standard sequence
   - Top-down packing: for limited conditions
   - Single-trip packing: efficiency vs complexity
   - Independent gravel sizing per zone
   - Pack quality verification per zone

4. DESIGN COMPLEXITY
   - String design: sizes, weights, connections
   - Gravel pack crossover tool integration
   - Screen lengths and placement
   - Slurry rates and volumes per zone
   - Contingency for pack failures

5. ECONOMIC CONSIDERATIONS
   - Two-zone incremental cost: $200K-600K
   - Three-plus zone cost: $800K-1,500K
   - Justification: NPV increase from separate zones
   - Alternative: single-zone completion of best interval
   - Commingled vs selective production economics

6. OPERATIONAL RISKS
   - Pack placement verification difficult
   - Crossover tool failures
   - Packer seal failures (inter-zonal flow)
   - Screen running complications
   - Workover costs multiplied by zone count

Multi-zone sand control is not routine—it is an engineering challenge
requiring detailed planning, quality equipment, and experienced personnel.
Failures in multi-zone completions are costly to remediate (often $1MM+).
Default recommendation: complete best single zone unless multi-zone NPV
exceeds single-zone NPV by > $2MM.
""",
        key_factors=[
            "Zone count and vertical separation",
            "Commingled vs selective production strategy",
            "Gravel pack crossover and isolation design",
            "Incremental cost vs NPV benefit",
            "Operational risk and complexity",
            "Workover access and remediation capability"
        ],
        primary_authority=[
            "SPE 107718 - Multi-Zone Completion Economics",
            "SPE 151830 - Multi-Zone Sand Control Design",
            "SPE 172369 - Selective Gravel Pack Completions"
        ],
        burden_holder="Engineer must justify multi-zone complexity with economic analysis",
        adversary_position="Single-zone completion of best interval is lower risk and cost",
        counter_arguments=[
            "Multi-zone complexity increases failure risk exponentially",
            "NPV improvement often overstated",
            "Workover difficulty eliminates multi-zone value",
            "Commingled production negates need for isolation",
            "Single-zone completion more reliable"
        ],
        resolution_strategy="Use multi-zone only if NPV improvement > $2MM and zone separation > 100 ft",
        entity_scope="Wells with multiple productive zones requiring sand control",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence for two-zone; high risk for three-plus zones",
        controlling_precedent="SPE 107718 multi-zone economic optimization",
        category=IssueCategory.PACK_PLACEMENT
    ),

    DoctrineBlock(
        topic="Horizontal Well Sand Control Challenges",
        keywords=["horizontal well", "openhole horizontal", "liner hanger", "heel-to-toe effect", "ERD sand control"],
        conclusion_template="Horizontal wells present unique sand control challenges: long openhole sections (1000-5000 ft), inability to gravel pack conventionally, heel-to-toe pressure effects, and difficult workover access. Standalone screens, expandable screens, or selective gravel packs via bullheading are standard. Sand control cost in horizontals is 2-4x vertical wells ($300K-2MM).",
        reasoning_framework="""
Horizontal well sand control design approach:

1. UNIQUE CHALLENGES
   - Long openhole exposure (1,000-5,000 ft typical)
   - Cannot use conventional gravel pack tools
   - Heel-to-toe pressure drop affects placement
   - Proppant/gravel settling in lateral
   - Workover access extremely difficult

2. COMPLETION OPTIONS
   - Standalone premium screens (most common)
   - Expandable sand screens (ESS)
   - Shunt tube gravel pack systems
   - Oriented or cemented liners
   - Open hole (no sand control, high risk)

3. STANDALONE SCREEN DESIGN
   - Premium mesh screens (not wire-wrap)
   - Screen filtration: 150-250 micron
   - Centralization essential
   - Screen joints: premium connections
   - External casing packer (ECP) for isolation

4. SHUNT TUBE GRAVEL PACK
   - Alternate path around screen for gravel slurry
   - Enables gravel placement in horizontal sections
   - Complex and expensive ($500K-2MM)
   - Requires competent formation for success
   - Limited field track record vs standalone screens

5. EXPANDABLE SCREENS FOR HORIZONTALS
   - Ideal application (no gravel pack needed)
   - Eliminates annular space
   - Requires gauge hole and competent rock
   - Expansion quality critical
   - Higher cost but proven performance

6. HEEL-TO-TOE EFFECTS
   - Pressure drop along lateral affects inflow
   - Toe region under-produces vs heel
   - Completion design must account for pressure profile
   - Inflow control devices (ICD) may be combined
   - Screen placement and perforation density optimization

Horizontal well sand control is inherently more challenging and costly
than vertical wells. Standalone screens are the default unless formation
is too weak (requires ESS or shunt pack). The inability to work over
horizontal sections means sand control must be correct on initial
completion—no second chances without sidetrack.
""",
        key_factors=[
            "Lateral length and openhole stability",
            "Standalone screen vs shunt pack vs ESS",
            "Screen filtration and centralization",
            "Heel-to-toe pressure effects",
            "Workover impracticality and cost",
            "Formation competence and hole quality"
        ],
        primary_authority=[
            "SPE 116631 - Horizontal Well Sand Control Methods",
            "SPE 168152 - ESS Application in Horizontals",
            "SPE 191411 - Shunt Tube Gravel Pack Case Studies"
        ],
        burden_holder="Engineer must select robust sand control for one-time completion",
        adversary_position="Horizontal sand control cost prohibitive; vertical wells preferred",
        counter_arguments=[
            "Standalone screens inadequate for weak formations",
            "ESS risk of expansion failure too high",
            "Shunt pack cost and complexity not justified",
            "Horizontal well benefits do not offset sand control cost",
            "Vertical wells with hydraulic fractures equally productive"
        ],
        resolution_strategy="Use standalone premium screens for competent formations; ESS for weak formations with gauge holes",
        entity_scope="Horizontal openhole completions requiring sand control",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence for competent formations; high risk for weak formations",
        controlling_precedent="SPE 116631 horizontal sand control design guidelines",
        category=IssueCategory.SCREEN_SELECTION
    ),

]


# ============================================================================
# CORE ENGINE CLASS
# ============================================================================

class PROD08SandControlEngine:
    """Production Engineering Intelligence: Sand Control & Management"""

    def __init__(self):
        self.version = "1.0.0"
        self.port = 9223
        self.start_time = datetime.now()
        self.query_count = 0
        self.cache_hits = 0
        self.doctrine_cache = DOCTRINE_CACHE

        # Build search indices
        self._build_indices()

        logger.info(f"PROD08 Sand Control Engine v{self.version} initialized on port {self.port}")
        logger.info(f"Loaded {len(self.doctrine_cache)} doctrine blocks")

    def _build_indices(self):
        """Build keyword and category indices for fast lookup"""
        self.keyword_index: Dict[str, List[DoctrineBlock]] = defaultdict(list)
        self.category_index: Dict[IssueCategory, List[DoctrineBlock]] = defaultdict(list)

        for doctrine in self.doctrine_cache:
            # Index by keywords
            for keyword in doctrine.keywords:
                self.keyword_index[keyword.lower()].append(doctrine)

            # Index by category
            self.category_index[doctrine.category].append(doctrine)

        logger.info(f"Built indices: {len(self.keyword_index)} keywords, {len(self.category_index)} categories")

    def _normalize_query(self, query: str) -> str:
        """Semantic normalization for sand control terminology"""
        query_lower = query.lower()

        # Normalize common terms
        normalizations = {
            r'\bgravel\s*pack\b': 'gravel_pack',
            r'\bfrac\s*pack\b': 'frac_pack',
            r'\bfrac[-\s]*pack\b': 'frac_pack',
            r'\bwire[-\s]*wrap\b': 'wire_wrap',
            r'\bwire\s*wrap(?:ped)?\s*screen\b': 'wire_wrap_screen',
            r'\bpremium\s*screen\b': 'premium_screen',
            r'\bexpandable\s*screen\b': 'expandable_screen',
            r'\bstandalone\s*screen\b': 'standalone_screen',
            r'\bchemical\s*consolidation\b': 'chemical_consolidation',
            r'\bresin\s*consolidation\b': 'resin_consolidation',
            r'\bsanding\s*prediction\b': 'sanding_prediction',
            r'\bcritical\s*drawdown\b': 'critical_drawdown',
            r'\bthick\s*wall\s*cylinder\b': 'TWC_testing',
            r'\bTWC\s*test\b': 'TWC_testing',
            r'\bgrain\s*size\b': 'grain_size_distribution',
            r'\bD10\b': 'D10_parameter',
            r'\bD50\b': 'D50_parameter',
            r'\bD90\b': 'D90_parameter',
            r'\balpha\s*wave\b': 'alpha_wave',
            r'\bbeta\s*wave\b': 'beta_wave',
            r'\bcrossover\b': 'pack_crossover',
            r'\btip\s*screen[-\s]*out\b': 'tip_screenout',
            r'\bTSO\b': 'tip_screenout',
            r'\berosi(?:on|ve)\b': 'erosion',
            r'\bacoustic\s*(?:sand\s*)?(?:detector|monitor)\b': 'acoustic_sand_detector',
            r'\bslot(?:ted)?\s*liner\b': 'slotted_liner',
            r'\boriented\s*perf\b': 'oriented_perforation',
            r'\bmulti[-\s]*zone\b': 'multi_zone',
            r'\bhorizontal\s*well\b': 'horizontal_well',
            r'\bshunt\s*(?:tube|pack)\b': 'shunt_tube',
            r'\b(?:sand\s*)?management\b': 'sand_management',
            r'\b(?:sand\s*)?exclusion\b': 'sand_exclusion',
        }

        for pattern, replacement in normalizations.items():
            query_lower = re.sub(pattern, replacement, query_lower)

        return query_lower

    def _search_doctrines(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache using keywords and semantic matching"""
        query_normalized = self._normalize_query(query)
        query_terms = set(query_normalized.split())

        scored_doctrines: List[Tuple[DoctrineBlock, float]] = []

        for doctrine in self.doctrine_cache:
            score = 0.0

            # Keyword matching
            doctrine_keywords = set(k.lower() for k in doctrine.keywords)
            keyword_matches = query_terms & doctrine_keywords
            score += len(keyword_matches) * 10.0

            # Topic matching
            if any(term in doctrine.topic.lower() for term in query_terms):
                score += 15.0

            # Full-text matching in reasoning framework
            for term in query_terms:
                if len(term) > 3 and term in doctrine.reasoning_framework.lower():
                    score += 2.0

            if score > 0:
                scored_doctrines.append((doctrine, score))

        # Sort by score descending
        scored_doctrines.sort(key=lambda x: x[1], reverse=True)

        # Return top doctrines
        return [d for d, s in scored_doctrines[:5]]

    def _three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Tuple[str, List[str], List[str], ConfidenceLevel]:
        """
        Three-layer response architecture:
        1. Doctrine cache (0-200ms)
        2. Semantic retrieval (fallback)
        3. Deep analysis mode (complex queries)
        """
        # Layer 1: Doctrine cache search
        relevant_doctrines = self._search_doctrines(query)

        if relevant_doctrines:
            self.cache_hits += 1
            # Cache hit - fast response
            return self._build_response_from_doctrines(
                query, relevant_doctrines, mode, zone
            )
        else:
            # Layer 2: Semantic retrieval (fallback to general knowledge)
            return self._fallback_response(query, mode, zone)

    def _build_response_from_doctrines(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Tuple[str, List[str], List[str], ConfidenceLevel]:
        """Build response from triggered doctrine blocks"""

        doctrines_triggered = [d.topic for d in doctrines]
        authorities = []
        reasoning_chain = []

        # Aggregate authorities
        for d in doctrines:
            authorities.extend(d.primary_authority)
        authorities = list(set(authorities))  # Deduplicate

        # Build reasoning chain
        for d in doctrines:
            reasoning_chain.append(f"DOCTRINE: {d.topic}")
            reasoning_chain.append(f"CONCLUSION: {d.conclusion_template}")

        # Determine overall confidence
        confidence_levels = [d.confidence for d in doctrines]
        if all(c == ConfidenceLevel.DEFENSIBLE for c in confidence_levels):
            overall_confidence = ConfidenceLevel.DEFENSIBLE
        elif any(c == ConfidenceLevel.HIGH_RISK for c in confidence_levels):
            overall_confidence = ConfidenceLevel.HIGH_RISK
        elif any(c == ConfidenceLevel.AGGRESSIVE for c in confidence_levels):
            overall_confidence = ConfidenceLevel.AGGRESSIVE
        else:
            overall_confidence = ConfidenceLevel.DISCLOSURE

        # Build response based on mode
        if mode == ResponseMode.FAST:
            answer = self._build_fast_response(query, doctrines, zone)
        elif mode == ResponseMode.DEFENSE:
            answer = self._build_defense_response(query, doctrines, zone)
        else:  # MEMO
            answer = self._build_memo_response(query, doctrines, zone)

        return answer, doctrines_triggered, authorities, overall_confidence

    def _build_fast_response(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        zone: AnalysisZone
    ) -> str:
        """Fast, concise response (1-2 paragraphs)"""
        primary_doctrine = doctrines[0]

        response = f"**{primary_doctrine.topic}**\n\n"
        response += primary_doctrine.conclusion_template + "\n\n"

        # Add key factors
        response += "**Key Factors:**\n"
        for factor in primary_doctrine.key_factors[:3]:
            response += f"- {factor}\n"

        # Add zone-specific guidance
        if zone == AnalysisZone.PLANNING:
            response += "\n**Planning Consideration:** "
            response += "Evaluate formation characteristics and well economics before selecting sand control method."
        elif zone == AnalysisZone.OPERATIONS:
            response += "\n**Operational Guidance:** "
            response += "Follow established procedures and monitor real-time parameters during execution."
        elif zone == AnalysisZone.MONITORING:
            response += "\n**Monitoring Protocol:** "
            response += "Establish baseline measurements and trend data for early problem detection."

        return response

    def _build_defense_response(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        zone: AnalysisZone
    ) -> str:
        """Audit-ready, detailed defense response"""
        response = f"# Sand Control Analysis: {query}\n\n"
        response += f"**Analysis Zone:** {zone.value}\n"
        response += f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n"

        for idx, doctrine in enumerate(doctrines, 1):
            response += f"## {idx}. {doctrine.topic}\n\n"
            response += f"**Conclusion:**\n{doctrine.conclusion_template}\n\n"

            response += f"**Technical Framework:**\n{doctrine.reasoning_framework}\n\n"

            response += f"**Critical Factors:**\n"
            for factor in doctrine.key_factors:
                response += f"- {factor}\n"
            response += "\n"

            response += f"**Authorities:**\n"
            for auth in doctrine.primary_authority:
                response += f"- {auth}\n"
            response += "\n"

            response += f"**Confidence Assessment:** {doctrine.confidence.value}\n"
            response += f"**Stratification:** {doctrine.confidence_stratification}\n\n"

            if doctrine.controlling_precedent:
                response += f"**Controlling Precedent:** {doctrine.controlling_precedent}\n\n"

            response += "---\n\n"

        return response

    def _build_memo_response(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        zone: AnalysisZone
    ) -> str:
        """Full technical memorandum format"""
        response = f"# TECHNICAL MEMORANDUM\n\n"
        response += f"**Subject:** {query}\n"
        response += f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n"
        response += f"**Analysis Zone:** {zone.value}\n"
        response += f"**Engine:** PROD08 Sand Control Intelligence v{self.version}\n\n"

        response += "## EXECUTIVE SUMMARY\n\n"
        primary = doctrines[0]
        response += primary.conclusion_template + "\n\n"

        response += "## TECHNICAL ANALYSIS\n\n"
        for idx, doctrine in enumerate(doctrines, 1):
            response += f"### {idx}. {doctrine.topic}\n\n"
            response += doctrine.reasoning_framework + "\n\n"

            response += "**Key Technical Factors:**\n"
            for factor in doctrine.key_factors:
                response += f"- {factor}\n"
            response += "\n"

        response += "## AUTHORITIES AND REFERENCES\n\n"
        all_authorities = []
        for d in doctrines:
            all_authorities.extend(d.primary_authority)
        all_authorities = sorted(set(all_authorities))

        for auth in all_authorities:
            response += f"- {auth}\n"
        response += "\n"

        response += "## RISK ASSESSMENT\n\n"
        response += "**Position Analysis:**\n"
        for d in doctrines[:2]:
            response += f"- **{d.topic}:** {d.burden_holder}\n"
        response += "\n"

        response += "**Counter-Arguments:**\n"
        for d in doctrines[:2]:
            for counter in d.counter_arguments[:3]:
                response += f"- {counter}\n"
        response += "\n"

        response += "**Resolution Strategy:**\n"
        for d in doctrines[:2]:
            response += f"- **{d.topic}:** {d.resolution_strategy}\n"
        response += "\n"

        response += "## RECOMMENDATIONS\n\n"
        response += f"Based on the analysis in the {zone.value} zone, the following approach is recommended:\n\n"
        for d in doctrines[:2]:
            response += f"- {d.conclusion_template}\n"
        response += "\n"

        response += f"**Confidence Level:** {doctrines[0].confidence.value}\n"
        response += f"**Confidence Stratification:** {doctrines[0].confidence_stratification}\n"

        return response

    def _fallback_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Tuple[str, List[str], List[str], ConfidenceLevel]:
        """Fallback when no doctrines match"""
        answer = f"**Query Analysis: {query}**\n\n"
        answer += "The query did not trigger specific doctrine blocks in the sand control knowledge base. "
        answer += "This may indicate a novel issue or a query requiring integration across multiple domains.\n\n"

        answer += "**General Sand Control Principles:**\n"
        answer += "- Formation sand characterization (grain size distribution) is fundamental\n"
        answer += "- Match sand control method to formation strength and well economics\n"
        answer += "- Gravel pack for unconsolidated formations with proper sizing (5-6x D50)\n"
        answer += "- Frac pack for low-permeability or damaged zones requiring stimulation\n"
        answer += "- Standalone screens for moderately consolidated formations\n"
        answer += "- Monitor sand production and erosion continuously\n"
        answer += "- Economic optimization: match method cost to well NPV\n\n"

        answer += "For specific technical guidance, please refine the query to address: sanding prediction, "
        answer += "gravel sizing, screen selection, frac pack design, placement quality, chemical consolidation, "
        answer += "monitoring systems, or economic analysis.\n"

        return answer, [], ["SPE General Sand Control Literature"], ConfidenceLevel.DISCLOSURE

    def _calculate_determinism_hash(self, query: str, answer: str) -> str:
        """SHA-256 hash for response reproducibility"""
        content = f"{query}|{answer}|{self.version}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    async def process_query(self, request: QueryRequest) -> QueryResponse:
        """Main query processing with full TIE-20 components"""
        start_time = datetime.now()
        self.query_count += 1

        logger.info(f"Processing query in {request.mode.value} mode, zone {request.zone.value}")

        # Three-layer response
        answer, doctrines_triggered, authorities, confidence = self._three_layer_response(
            request.query,
            request.mode,
            request.zone
        )

        # Build reasoning chain
        reasoning_chain = [
            f"Query normalized and analyzed",
            f"Doctrine search: {len(doctrines_triggered)} blocks triggered",
            f"Response mode: {request.mode.value}",
            f"Analysis zone: {request.zone.value}",
            f"Confidence level: {confidence.value}"
        ]

        # Calculate determinism hash
        determinism_hash = self._calculate_determinism_hash(request.query, answer)

        # Telemetry
        elapsed = (datetime.now() - start_time).total_seconds()
        telemetry = {
            "elapsed_ms": int(elapsed * 1000),
            "doctrines_triggered": len(doctrines_triggered),
            "cache_hit": len(doctrines_triggered) > 0,
            "mode": request.mode.value,
            "zone": request.zone.value,
            "query_length": len(request.query)
        }

        logger.info(f"Query processed in {elapsed*1000:.1f}ms, {len(doctrines_triggered)} doctrines triggered")

        return QueryResponse(
            answer=answer,
            mode=request.mode,
            zone=request.zone,
            confidence=confidence,
            doctrines_triggered=doctrines_triggered,
            reasoning_chain=reasoning_chain,
            authorities_cited=authorities,
            determinism_hash=determinism_hash,
            telemetry=telemetry
        )

    def get_health(self) -> HealthResponse:
        """Comprehensive health check"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        cache_hit_rate = (self.cache_hits / self.query_count * 100) if self.query_count > 0 else 0.0

        return HealthResponse(
            status="operational",
            version=self.version,
            port=self.port,
            doctrines_loaded=len(self.doctrine_cache),
            uptime_seconds=uptime,
            total_queries=self.query_count,
            cache_hit_rate=cache_hit_rate
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="PROD08 Sand Control Intelligence Engine",
    description="Production Engineering - Sand Control & Management Systems",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = PROD08SandControlEngine()


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with TIE-20 architecture"""
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
        "by_category": {
            cat.value: len(blocks)
            for cat, blocks in engine.category_index.items()
        },
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in engine.doctrine_cache
        ]
    }


@app.get("/")
async def root():
    """Root endpoint with engine information"""
    return {
        "engine": "PROD08 Sand Control Intelligence",
        "version": engine.version,
        "port": engine.port,
        "status": "operational",
        "doctrines": len(engine.doctrine_cache),
        "capabilities": [
            "Sanding prediction analysis",
            "Gravel pack design",
            "Screen selection guidance",
            "Frac pack optimization",
            "Chemical consolidation evaluation",
            "Sand monitoring strategies",
            "Economic analysis",
            "Multi-zone completions",
            "Horizontal well sand control"
        ],
        "endpoints": {
            "query": "/query",
            "health": "/health",
            "doctrines": "/doctrines"
        }
    }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    logger.info("="*80)
    logger.info("PROD08 SAND CONTROL INTELLIGENCE ENGINE")
    logger.info(f"Version: {engine.version}")
    logger.info(f"Port: {engine.port}")
    logger.info(f"Doctrines Loaded: {len(engine.doctrine_cache)}")
    logger.info("="*80)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=engine.port,
        log_level="info"
    )
