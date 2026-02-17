"""
FRAC07 - Flowback & Well Cleanup Intelligence Engine
Domain: Completions - Flowback Operations
Port: 9027
Version: 1.0.0

TIE Gold Standard Engine - Flowback operations expertise covering equipment,
choke management, data acquisition, load recovery, proppant flowback prevention,
water disposal, emissions control, and production optimization.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Any
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# Configure structured logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "logs" / "frac07_flowback_{time:YYYY-MM-DD}.log",
    rotation="500 MB",
    retention="90 days",
    level="DEBUG"
)


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
    EQUIPMENT = "EQUIPMENT"
    CHOKE_MANAGEMENT = "CHOKE_MANAGEMENT"
    DATA_ACQUISITION = "DATA_ACQUISITION"
    LOAD_RECOVERY = "LOAD_RECOVERY"
    PROPPANT_MANAGEMENT = "PROPPANT_MANAGEMENT"
    WATER_MANAGEMENT = "WATER_MANAGEMENT"
    EMISSIONS = "EMISSIONS"
    PRODUCTION_OPT = "PRODUCTION_OPT"
    FORMATION_DAMAGE = "FORMATION_DAMAGE"
    SAFETY = "SAFETY"


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Flowback operations question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    sources: List[str]
    triggered_doctrines: List[str]
    determinism_hash: str
    timestamp: str
    query_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float


class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    category: IssueCategory
    adversarial_considerations: Optional[str] = None
    interaction_dependencies: List[str] = Field(default_factory=list)


# TIE Gold Standard: 25+ Real Flowback Doctrine Blocks
DOCTRINE_BLOCKS = [
    DoctrineBlock(
        topic="Flowback Equipment Configuration",
        keywords=["separator", "sand trap", "choke manifold", "flowback tanks", "equipment", "piping"],
        conclusion_template="Standard flowback equipment train consists of adjustable choke → sand trap → 3-phase separator → flowback tanks, sized for expected rates and pressures with safety factor of 1.5x.",
        reasoning_framework="""
        Equipment sizing methodology:
        1. Predict peak flowback rate from offset wells (typically 2-5 MMcf/d gas, 500-2000 bbl/d liquid)
        2. Size choke manifold for max SIWHP (often 5000-10000 psi wellhead, controlled down to separator pressure)
        3. Sand trap rated for velocities <5 ft/sec to allow sand dropout (critical for proppant capture)
        4. Three-phase separator sized for gas/oil/water separation at controlled pressure (50-200 psi typical)
        5. Flowback tank battery (500-1000 bbl capacity) for temporary storage before disposal/recycling
        6. Flare/VRU for gas handling (EPA methane regulations require 95% capture efficiency)
        7. Redundant equipment (backup separator, dual chokes) for continuous operation

        Critical design factors:
        - Erosional velocity limits in piping (API RP 14E: Ve = C/√ρm, C=100-150 for solids-free)
        - Pressure drop calculations across choke (subcritical vs critical flow regimes)
        - Sand handling capacity (expect 0.1-5 lbm proppant per 1000 gal flowback in well-designed fracs)
        - Temperature considerations (choke can freeze with rapid gas expansion, need insulation/heating)
        - H2S/CO2 corrosion if sour gas (material selection, inhibitor injection)
        """,
        key_factors=[
            "Expected peak flowback rate from offset data",
            "Wellhead pressure and drawdown strategy",
            "Proppant concentration in early flowback",
            "Gas composition (lean vs rich, sour vs sweet)",
            "Separator pressure optimization (higher = more liquid recovery, lower = more gas production)",
            "Tank capacity for 24-72 hr storage (weekends, disposal logistics)",
            "Emissions compliance (flare vs VRU, 95% methane capture)",
            "Safety systems (PSV, SDV, flame arrestors)"
        ],
        primary_authority=[
            "API RP 14E (Erosional Velocity)",
            "EPA NSPS OOOOa (Methane Emissions)",
            "ASME B31.3 (Process Piping)",
            "Operator field standards",
            "Offset well flowback data"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.EQUIPMENT,
        adversarial_considerations="Undersized equipment causes shutdowns and lost production. Oversized equipment wastes capital. Balance based on offset well performance and conservative safety factors."
    ),

    DoctrineBlock(
        topic="Choke Management Strategy - Aggressive vs Conservative",
        keywords=["choke", "drawdown", "aggressive", "conservative", "IP rate", "formation damage"],
        conclusion_template="Choke management strategy depends on formation permeability, completion quality, and operator risk tolerance. Aggressive drawdown (large choke) maximizes early IP but risks proppant flowback and formation damage. Conservative approach (small choke, gradual increases) prioritizes EUR over IP.",
        reasoning_framework="""
        Two competing philosophies:

        AGGRESSIVE CHOKE MANAGEMENT:
        - Start with larger choke size (24/64" to 48/64")
        - Rapid drawdown to achieve high initial production (IP) rates
        - Goal: Clean up frac fluid quickly, establish high IP for reserves booking
        - Risk: Proppant flowback, formation fines migration, fracture collapse, embedment
        - Best for: High-perm formations (>1 md), well-consolidated rock, high-quality proppants
        - Industry trend in tight oil (Permian, Eagle Ford): "choke it back and let it flow"

        CONSERVATIVE CHOKE MANAGEMENT:
        - Start with small choke (12/64" to 24/64")
        - Gradual increases (stepping up 4/64" every 6-24 hrs)
        - Monitor for proppant flowback (sand in separator, erosion indicators)
        - Goal: Minimize formation damage, preserve fracture conductivity, maximize EUR
        - Risk: Slower cleanup, prolonged flowback period, lower IP (but potentially better EUR)
        - Best for: Low-perm formations (<0.1 md), unconsolidated sands, resin-coated proppants

        Decision factors:
        1. Formation rock strength (UCS, Young's modulus from logs)
        2. Proppant type and strength (20/40 vs 100 mesh, ceramic vs sand, RCP vs uncoated)
        3. Completion quality (perforation density, cluster spacing, proppant placement uniformity)
        4. Frac fluid type (slickwater = faster cleanup vs crosslinked gel = slower)
        5. Reservoir pressure (overpressured = more energy, faster cleanup)
        6. Economic drivers (IP-focused vs EUR-focused development)
        7. Offset well performance (if neighbors had proppant issues, be conservative)

        Real-world hybrid approach:
        - Start conservative (small choke) for first 12-24 hrs to allow near-wellbore cleanup
        - Monitor proppant in flowback (visual inspection, sand detector, erosion coupons)
        - If clean (no sand), step up choke aggressively to maximize rate
        - If sand detected, hold choke size or reduce until flowback cleans up
        - Target drawdown <50% of reservoir pressure initially, can increase after cleanup
        """,
        key_factors=[
            "Formation permeability and rock strength",
            "Proppant type, size, and crush strength",
            "Completion design quality (cluster efficiency)",
            "Economic objective (IP vs EUR optimization)",
            "Offset well flowback performance and proppant production",
            "Frac fluid type and expected cleanup time",
            "Real-time proppant monitoring capability",
            "Formation damage risk (clay swelling, fines migration)"
        ],
        primary_authority=[
            "SPE papers on choke management strategies",
            "Operator-specific flowback procedures",
            "Offset well production data",
            "Proppant vendor recommendations",
            "Field best practices and lessons learned"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.CHOKE_MANAGEMENT,
        adversarial_considerations="Aggressive choke strategy inflates IP for reserves booking but may damage fractures and reduce EUR. Conservative strategy protects long-term value but risks opportunity cost if formation can handle higher rates. No universal answer - depends on asset development strategy and rock quality.",
        interaction_dependencies=["Proppant Flowback Prevention", "Formation Damage Prevention"]
    ),

    DoctrineBlock(
        topic="Flowback Data Acquisition and Monitoring",
        keywords=["data", "monitoring", "sensors", "SCADA", "pressure", "temperature", "rate", "analytics"],
        conclusion_template="Comprehensive flowback data acquisition includes continuous monitoring of rates (gas, oil, water), pressures (SIWHP, separator, line), temperatures, and proppant production. Modern systems integrate real-time SCADA with automated analytics for choke optimization.",
        reasoning_framework="""
        Critical flowback measurements (1-minute intervals minimum):

        PRESSURE MEASUREMENTS:
        1. Shut-in wellhead pressure (SIWHP) - indicates reservoir pressure depletion
        2. Flowing wellhead pressure (FWHP) - input to IPR calculations
        3. Separator pressure - optimized for liquid/gas separation efficiency
        4. Line pressures across choke (upstream/downstream ΔP)
        5. Tank vapor space pressure (safety, emissions monitoring)

        RATE MEASUREMENTS:
        1. Gas rate (typically turbine meter or Coriolis, ±2% accuracy)
        2. Oil rate (Coriolis or positive displacement meter)
        3. Water rate (by difference or dedicated meter)
        4. Total liquid rate (separator dump cycles or level instruments)
        5. Cumulative volumes (integration for load recovery calculations)

        TEMPERATURE MEASUREMENTS:
        1. Wellhead temperature (correlate with drawdown, hydrate risk)
        2. Separator temperature (optimize separation, detect upsets)
        3. Choke temperature (detect freezing risk from gas expansion)

        COMPOSITION/QUALITY:
        1. Gas composition (GC analysis, BTU content, C1-C5+)
        2. Water salinity/TDS (inline conductivity or lab samples)
        3. Proppant concentration (visual, sand detector, erosion monitoring)
        4. Oil API gravity (densitometer or samples)
        5. H2S/CO2 content (safety, corrosion management)

        DERIVED ANALYTICS:
        1. Load recovery percentage = (cumulative liquid out / frac volume) × 100%
        2. Gas-liquid ratio (GLR) trend - indicates transition from cleanup to production
        3. Water cut trend - oil vs water production ratio
        4. Drawdown = SIWHP - FWHP (manage to prevent formation damage)
        5. Productivity index = rate / drawdown (real-time well performance)
        6. EUR forecasting (Arps decline curve analysis starting after cleanup)

        Modern SCADA integration:
        - Cloud-based platforms (Corva, Well Data Labs, Validere)
        - Automated choke recommendations based on real-time data
        - Machine learning models for optimal flowback trajectory
        - Remote monitoring (reduce field visits, improve safety)
        - Integration with completion data for fracture diagnostics
        """,
        key_factors=[
            "Sensor accuracy and calibration (±2-5% for custody transfer)",
            "Data sampling frequency (1-min typical, can go to 1-sec for transient analysis)",
            "SCADA system reliability and cybersecurity",
            "Real-time analytics vs post-processing",
            "Integration with completion and geology data",
            "Automated alerts for out-of-range conditions",
            "Data storage and retention (comply with regulatory requirements)",
            "Remote access for optimization decisions"
        ],
        primary_authority=[
            "API MPMS Ch 5 (Metering)",
            "Manufacturer specs (Emerson, Weatherford, etc.)",
            "Operator SCADA standards",
            "SPE papers on flowback optimization",
            "State oil and gas commission reporting requirements"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.DATA_ACQUISITION,
        adversarial_considerations="High-quality data enables real-time optimization but requires capital investment in instrumentation. Manual gauging is cheaper but introduces delays and human error. Balance depends on well economics and development scale."
    ),

    DoctrineBlock(
        topic="Load Recovery Calculations and Optimization",
        keywords=["load recovery", "frac fluid", "cleanup", "efficiency", "reservoir contact"],
        conclusion_template="Load recovery (percentage of frac fluid returned to surface) typically ranges from 20-70% depending on formation permeability, fluid type, and cleanup strategy. Higher recovery indicates better fracture cleanup but doesn't always correlate with better EUR - some fluid imbibition improves reservoir contact.",
        reasoning_framework="""
        Load recovery calculation:
        Load Recovery % = (Cumulative Flowback Volume / Total Frac Volume Pumped) × 100%

        Where:
        - Cumulative Flowback Volume = oil + water produced during flowback period
        - Total Frac Volume = slickwater + crosslinked gel + proppant slurry volume
        - Flowback period = typically defined as first 30-90 days or until stable production

        Typical ranges by formation type:
        - Tight oil (Permian, Bakken): 30-60% recovery, higher perm = higher recovery
        - Shale gas (Marcellus, Haynesville): 20-40% recovery, ultra-low perm retains more fluid
        - Tight gas (Cotton Valley): 40-70% recovery, intermediate perm
        - Conventional reservoirs: 70-90% recovery (rare to frac these anymore)

        Factors affecting load recovery:

        FORMATION PROPERTIES:
        1. Permeability - higher perm = faster cleanup, higher recovery
        2. Porosity - higher porosity = more fluid storage capacity, lower recovery
        3. Clay content - swelling clays trap fluid, reduce recovery
        4. Natural fractures - can enhance cleanup if well-connected
        5. Reservoir pressure - higher pressure drives fluid back faster

        FLUID PROPERTIES:
        1. Slickwater - lower viscosity, easier cleanup, higher recovery (50-70%)
        2. Crosslinked gel - higher viscosity, slower cleanup, lower recovery (20-40%)
        3. Hybrid fluids - intermediate recovery (40-60%)
        4. Surfactants - improve wettability, enhance cleanup (add 10-20% recovery)
        5. Breakers - degrade gel, improve cleanup if properly designed

        OPERATIONAL FACTORS:
        1. Choke management - aggressive = faster cleanup, higher recovery
        2. Soak time - longer soak may reduce recovery but improve reservoir contact
        3. Gas lift / N2 assist - artificially enhances recovery
        4. Surfactant-assisted flowback - chemical injection post-frac

        OPTIMIZATION CONSIDERATIONS:
        - Maximum load recovery is NOT always optimal for EUR
        - Some fluid imbibition can improve matrix permeability (water blocking vs enhancement)
        - Ultra-low recovery (<20%) may indicate fracture closure or severe formation damage
        - Ultra-high recovery (>80%) may indicate poor fracture-reservoir contact
        - Target "Goldilocks" zone: 40-60% recovery with strong oil/gas production

        Advanced analytics:
        - Plot load recovery vs cumulative gas production (look for correlation)
        - Compare load recovery across wells in same formation (identify outliers)
        - Chemical tracer analysis (determine which frac stages are producing)
        - Decline curve analysis (does faster cleanup correlate with better EUR?)
        """,
        key_factors=[
            "Formation permeability and porosity",
            "Frac fluid type and volume pumped",
            "Choke management and flowback rate",
            "Soak time before flowback initiation",
            "Use of cleanup additives (surfactants, solvents)",
            "Reservoir pressure and drive mechanism",
            "Fracture geometry and conductivity",
            "Correlation between recovery and long-term EUR"
        ],
        primary_authority=[
            "SPE papers on load recovery optimization",
            "Operator frac database (offset wells)",
            "Service company fluid performance data",
            "Academic research on fluid-rock interaction",
            "Field case studies by basin"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.LOAD_RECOVERY,
        adversarial_considerations="Industry debates optimal load recovery target. Some argue maximum recovery prevents formation damage; others argue retained fluid improves reservoir contact. No universal answer - depends on formation mineralogy and wettability.",
        interaction_dependencies=["Frac Fluid Recovery Efficiency", "Formation Damage Prevention"]
    ),

    DoctrineBlock(
        topic="Proppant Flowback Prevention and Management",
        keywords=["proppant", "sand", "flowback", "production", "fracture", "conductivity", "erosion"],
        conclusion_template="Proppant flowback (sand production) indicates fracture instability or poor proppant pack consolidation. Prevention strategies include conservative choke management, resin-coated proppants, proper completion design, and downhole sand control. Acceptable proppant production is <1 lbm per 1000 bbl produced long-term.",
        reasoning_framework="""
        Proppant flowback mechanisms:

        1. FRACTURE CLOSURE AND PROPPANT CRUSH:
        - Insufficient fracture width or closure stress exceeds proppant crush strength
        - Proppant embeds into formation or crushes to fines
        - Fine proppant particles mobilize and flow back with produced fluids
        - More common with weak proppants (100 mesh sand) or high-stress formations

        2. PROPPANT PACK INSTABILITY:
        - Unconsolidated proppant pack (no resin coating or natural cementation)
        - High fluid velocities through pack mobilize grains (Reynolds number >10)
        - Cyclic stress from pressure fluctuations breaks grain contacts
        - Common in early flowback before pack stabilizes

        3. FORMATION SAND PRODUCTION:
        - Weak, unconsolidated formation (Gulf Coast, California)
        - Formation fines and sand mix with proppant in fracture
        - Cannot distinguish formation sand from proppant in flowback
        - Indicates formation damage risk

        4. POOR PROPPANT PLACEMENT:
        - Proppant settling in heel stages (horizontal wells)
        - Uneven proppant distribution across clusters (some overpacked, some underpacked)
        - Proppant in unstressed fractures (far-field tips) flows back first

        Prevention strategies:

        PROPPANT SELECTION:
        - Use higher-strength proppant (ceramic vs sand) in high-stress formations
        - Resin-coated proppant (RCP) for unconsolidated formations - resin bonds grains
        - Larger mesh sizes (20/40 vs 100 mesh) are more stable but lower conductivity
        - Proppant crush testing at reservoir stress conditions

        COMPLETION DESIGN:
        - Optimize perforation size (prevent proppant bridging in perfs, allow flowback)
        - Limit perforation density (reduce velocity through each perf)
        - Proper cluster spacing (ensure all clusters take proppant evenly)
        - Diverter use (force proppant into all perfs, not just easiest path)

        CHOKE MANAGEMENT:
        - Conservative drawdown (<50% reservoir pressure) during early flowback
        - Gradual choke increases (monitor for sand after each step change)
        - Hold choke size if sand appears, allow pack to stabilize
        - Some operators use cyclic choke (open-shut cycles to settle proppant)

        DOWNHOLE SAND CONTROL:
        - Wire-wrapped screens (WWS) or expandable sand screens (ESS)
        - Gravel pack in casing/liner annulus (rare in unconventional)
        - Chemical consolidation (resin injection to cement proppant pack)
        - Only used in severe cases due to cost and conductivity loss

        MONITORING AND RESPONSE:
        - Visual inspection of flowback (sand in separator dump)
        - Acoustic sand detectors (quantify sand rate in real-time)
        - Erosion coupons (measure equipment wear from sand)
        - If >5 lbm/1000 bbl sustained: reduce choke, investigate root cause

        Consequences of proppant flowback:
        - Loss of fracture conductivity (reduced EUR)
        - Equipment erosion (chokes, valves, separators require frequent replacement)
        - Disposal costs (sand-contaminated water harder to recycle)
        - Safety hazards (erosion can cause leaks, fires)
        - Wellbore fill (sand accumulates in horizontal lateral, requires cleanout)
        """,
        key_factors=[
            "Proppant type, size, and crush strength",
            "Formation stress and rock strength",
            "Fracture geometry and closure stress",
            "Perforation design (size, density, phasing)",
            "Choke management and drawdown rate",
            "Resin-coated vs uncoated proppant economics",
            "Real-time sand monitoring capability",
            "Equipment erosion tolerance and replacement costs"
        ],
        primary_authority=[
            "API RP 19C (Proppant Testing)",
            "SPE papers on proppant flowback",
            "Proppant vendor technical data (CARBO, Hi-Crush)",
            "Operator field experience and case studies",
            "Sand control vendor recommendations (Schlumberger, Halliburton)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PROPPANT_MANAGEMENT,
        adversarial_considerations="RCP proppant costs 2-3x more than uncoated sand. Economic justification requires proving EUR improvement exceeds cost delta. In low-stress formations, may be essential. In high-quality rock, may be unnecessary. Field trial data is critical.",
        interaction_dependencies=["Choke Management Strategy", "Equipment Erosion"]
    ),

    DoctrineBlock(
        topic="Flowback Water Quality and Chemistry",
        keywords=["TDS", "salinity", "scaling", "bacteria", "water quality", "ions", "chemistry"],
        conclusion_template="Flowback water chemistry evolves from frac fluid (low TDS, controlled chemistry) to formation brine (high TDS, scaling ions, bacteria). Typical progression: 5,000 mg/L TDS at Day 1 → 50,000-200,000+ mg/L by Day 30 as formation water mixes in. Water quality dictates disposal vs recycling options.",
        reasoning_framework="""
        Flowback water chemistry evolution:

        STAGE 1 - EARLY FLOWBACK (Days 0-3):
        - Dominated by frac fluid (slickwater with friction reducer, biocide, scale inhibitor)
        - Low TDS: 1,000-10,000 mg/L (similar to fresh water or makeup water)
        - Low scaling potential (no significant Ca, Ba, Sr)
        - Minimal bacteria (biocide still effective)
        - Clear to slightly cloudy appearance
        - pH near neutral (6-8) from frac fluid additives

        STAGE 2 - TRANSITION (Days 3-14):
        - Mixing zone: frac fluid + formation brine
        - Rising TDS: 10,000-100,000 mg/L (rapid increase)
        - Increasing hardness (Ca, Mg) and scaling ions (Ba, Sr)
        - Bacteria begin to grow as biocide degrades
        - Water darkens (dissolved organics, suspended solids)
        - pH may shift (can go alkaline or acidic depending on formation)

        STAGE 3 - LATE FLOWBACK / PRODUCED WATER (Days 14+):
        - Dominated by formation brine (minimal frac fluid remaining)
        - High TDS: 50,000-300,000 mg/L (formation-dependent)
        - High scaling potential (BaSO4, SrSO4, CaSO4, CaCO3)
        - Active bacterial populations (SRB, APB, GHB)
        - Dark brown/black color (oil, organics, iron sulfide)
        - May be sour (H2S) or contain dissolved CO2

        Critical ions and concerns:

        TOTAL DISSOLVED SOLIDS (TDS):
        - Permian: 100,000-250,000 mg/L (hypersaline, near saturation)
        - Eagle Ford: 50,000-150,000 mg/L
        - Marcellus: 80,000-300,000 mg/L (some highest TDS in US)
        - Bakken: 150,000-350,000 mg/L
        - Haynesville: 80,000-200,000 mg/L

        SCALING IONS:
        1. Calcium (Ca²⁺): 5,000-50,000 mg/L - forms CaCO3, CaSO4 scales
        2. Magnesium (Mg²⁺): 500-5,000 mg/L - forms MgCO3, Mg(OH)2
        3. Barium (Ba²⁺): 100-5,000 mg/L - forms BaSO4 (worst scale, insoluble)
        4. Strontium (Sr²⁺): 500-5,000 mg/L - forms SrSO4 scale
        5. Sulfate (SO4²⁻): 10-500 mg/L - pairs with Ca, Ba, Sr
        6. Bicarbonate (HCO3⁻): 100-2,000 mg/L - forms carbonate scales at high pH

        BACTERIAL POPULATIONS:
        1. Sulfate-reducing bacteria (SRB) - produce H2S, cause souring, MIC
        2. Acid-producing bacteria (APB) - produce organic acids, corrosion
        3. General heterotrophic bacteria (GHB) - slime formers, biofouling
        4. Concentrations: 10²-10⁶ CFU/mL in untreated flowback

        OTHER PARAMETERS:
        - Oil and grease: 50-5,000 mg/L (emulsions, free oil)
        - Total suspended solids (TSS): 100-10,000 mg/L (proppant, formation fines, scale)
        - NORM (naturally occurring radioactive material): Ra-226, Ra-228 in some formations
        - Heavy metals: Fe, Mn, Pb, As (formation-dependent)

        Water quality testing protocol:
        - Sample every 24 hrs during first week, then weekly
        - Field tests: TDS (conductivity), pH, temperature, visual appearance
        - Lab analysis: full ion panel (cations and anions), bacteria, oil/grease, TSS
        - Special tests: NORM, heavy metals if required by regulations

        Implications for disposal/recycling:
        - Low TDS (<10,000 mg/L): can recycle with minimal treatment
        - Medium TDS (10,000-50,000 mg/L): blending or treatment required for recycling
        - High TDS (>50,000 mg/L): disposal in Class II injection well or specialized treatment
        - Scaling potential: add inhibitors or avoid mixing incompatible waters
        - Bacterial control: continuous biocide treatment if recycling
        """,
        key_factors=[
            "Formation brine TDS and composition",
            "Frac fluid chemistry and additives",
            "Load recovery rate (faster = more frac fluid, slower = more brine)",
            "Time evolution of water chemistry",
            "Scaling potential (Ba, Sr, Ca with sulfate)",
            "Bacterial growth and souring risk",
            "Disposal regulations (UIC Class II permit limits)",
            "Recycling economics vs disposal costs"
        ],
        primary_authority=[
            "EPA UIC regulations (Class II wells)",
            "State water disposal regulations",
            "USGS produced water database",
            "SPE papers on produced water management",
            "Water testing lab protocols (API RP 45)",
            "Operator water management plans"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.WATER_MANAGEMENT,
        adversarial_considerations="Water chemistry is formation-specific. Generic assumptions lead to scaling failures, corrosion, or bacterial souring. Invest in early water sampling and analysis to develop basin-specific water management strategy."
    ),

    DoctrineBlock(
        topic="Flare Operations and EPA Methane Regulations",
        keywords=["flare", "emissions", "methane", "EPA", "VRU", "capture", "compliance", "OOOOa"],
        conclusion_template="EPA NSPS OOOOa (2016) and OOOOb/OOOOc (2024) require 95% methane capture efficiency during flowback. Operators must use green completions (VRU/pipeline) or high-efficiency flares. Venting is prohibited except for emergencies. State regulations may be more stringent.",
        reasoning_framework="""
        Regulatory framework for flowback gas handling:

        EPA NSPS OOOOa (New Source Performance Standards, 2016):
        - Applies to wells drilled/fractured after June 3, 2016
        - Requires reduced emissions completions (REC), aka "green completions"
        - 95% methane capture efficiency during flowback
        - Gas must be routed to sales pipeline, used on-site, or flared (NOT vented)
        - Monthly reporting of gas volumes captured, flared, vented

        EPA OOOOb (2024, proposed):
        - Expands coverage to all existing wells (not just new sources)
        - Tightens methane capture requirements
        - Potential for flaring fees/penalties
        - Increased monitoring and reporting

        STATE REGULATIONS (can be more stringent):
        - Colorado: requires 95% capture, limits flaring duration to 60 days
        - Pennsylvania: flaring restricted near populated areas
        - North Dakota: flaring capture targets, penalties for excess flaring
        - New Mexico: aggressive methane rules, 98% capture by 2026
        - Texas: RRC flaring permits required, trend toward restrictions

        Gas handling options during flowback:

        1. VAPOR RECOVERY UNIT (VRU):
        - Compresses flowback gas to pipeline pressure (500-1200 psi)
        - Routes gas to sales pipeline or on-site use (artificial lift, power generation)
        - Typical efficiency: 97-99% methane capture
        - Equipment: VRU skid with compressor, scrubber, controls
        - Economics: positive if gas price > operating cost (~$0.50-2.00/Mcf)
        - Challenges: requires pipeline access, may need gas treating (dehydration, H2S removal)

        2. HIGH-EFFICIENCY ENCLOSED FLARE:
        - Combusts flowback gas in enclosed flare (not open pit flare)
        - Destruction efficiency >98% for proper design and operation
        - Converts methane (CH4) to CO2 and H2O (reduces GWP from 25x to 1x)
        - Requires pilot flame, proper air-fuel mixing, minimum BTU content
        - Lower operating cost than VRU but no revenue from gas
        - Used when pipeline unavailable or gas volumes too low for VRU economics

        3. ON-SITE USE:
        - Power generation (turbines, gensets)
        - Artificial lift (gas lift, pneumatic pumps)
        - Drilling rig fuel (if rig still on location)
        - Limited capacity (typically <1 MMcf/d)

        4. VENTING (prohibited except emergencies):
        - Only allowed for safety (emergency shutdowns, pressure relief)
        - Must be reported and justified
        - Penalties for non-compliance

        Operational considerations:

        FLOWBACK GAS CHARACTERISTICS:
        - High initial rate: 2-10 MMcf/d during first few days
        - Declining rate: drops to <1 MMcf/d by end of flowback
        - Variable composition: rich gas (high BTU) early, lean gas late
        - May contain H2S, CO2, NGLs (requires treating)

        VRU SIZING:
        - Must handle peak flowback rate (size for 5-10 MMcf/d typical)
        - Turndown ratio (ability to handle low rates at end of flowback)
        - Portability (trailer-mounted units move well to well)

        FLARE DESIGN:
        - Smokeless operation (complete combustion)
        - Wind shields (prevent blowout in high winds)
        - Pilot monitoring (continuous flame detection)
        - Minimum net heating value (typically 200-300 BTU/scf for efficient combustion)
        - If gas too lean, may need supplemental fuel

        COMPLIANCE MONITORING:
        - Continuous flow measurement (turbine or ultrasonic meters)
        - Calculate volumes captured, flared, vented
        - Monthly reporting to EPA (via CEDRI database)
        - Records retention (5 years)
        - Third-party audits in some states

        Economics:
        - VRU rental: $5,000-15,000/month
        - Flare rental: $2,000-5,000/month
        - Pipeline connection: $10,000-100,000 (distance-dependent)
        - Methane penalties (if implemented): $900-1,500 per ton CH4 (proposed)
        - Gas revenue: $2-6/Mcf (market-dependent) × flowback volume (50-500 MMcf)

        Industry trend:
        - Shift from flaring to VRU/pipeline (regulatory and ESG pressure)
        - Shared infrastructure (multiple wells to one VRU or pipeline)
        - Pre-planning (pipeline tie-in before flowback, not after)
        - Real-time emissions monitoring (LDAR, satellite, aerial)
        """,
        key_factors=[
            "EPA and state methane regulations (95%+ capture)",
            "Pipeline access and capacity",
            "VRU vs flare economics (gas price, equipment cost)",
            "Flowback gas rate and composition (BTU, H2S, CO2)",
            "VRU sizing for peak rate and turndown",
            "Flare design for complete combustion",
            "Compliance monitoring and reporting systems",
            "ESG commitments and stakeholder pressure"
        ],
        primary_authority=[
            "EPA 40 CFR Part 60 Subpart OOOOa",
            "EPA OOOOb/OOOOc proposed rules (2024)",
            "State oil and gas commission regulations",
            "EPA CEDRI reporting system",
            "API standards for VRU and flare design",
            "Operator environmental compliance plans"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.EMISSIONS,
        adversarial_considerations="Flaring is cheaper upfront but faces increasing regulatory and ESG scrutiny. VRU has higher capital cost but generates revenue and improves emissions profile. Operators in low-gas-price environments may push back on VRU requirements. State-by-state variation creates compliance complexity.",
        interaction_dependencies=["Flowback to Sales Timeline", "Gas Handling During Flowback"]
    ),

    DoctrineBlock(
        topic="Water Disposal and Recycling Planning",
        keywords=["disposal", "recycling", "SWD", "Class II", "reuse", "treatment", "trucking", "pipeline"],
        conclusion_template="Flowback water disposal options: (1) Class II saltwater disposal (SWD) well injection, (2) recycling/reuse for future fracs, (3) treatment to discharge standards (rare). Selection depends on water chemistry, local infrastructure, regulations, and economics. Permian and Eagle Ford have extensive SWD infrastructure; Marcellus relies more on recycling.",
        reasoning_framework="""
        Disposal/recycling decision framework:

        OPTION 1: CLASS II SALTWATER DISPOSAL WELL INJECTION

        Regulatory: EPA Underground Injection Control (UIC) Program
        - Class II wells for oil and gas produced water disposal
        - Permit required (demonstrate injection zone isolation, no USDW contamination)
        - Injection pressure limits (must not exceed fracture pressure of injection zone)
        - Monthly reporting (volumes, pressures, water quality)

        Technical requirements:
        - Injection zone: permeable formation below USDW (underground source of drinking water)
        - Typical depths: 5,000-12,000 ft
        - Water quality: must be compatible with injection zone (avoid plugging)
        - Pre-treatment: solids removal (filtration), sometimes bacteria kill

        Economics:
        - Disposal fee: $0.25-3.00 per barrel (location-dependent)
        - Trucking: $1-5 per barrel (distance-dependent)
        - Pipeline: $0.10-0.50 per barrel (if infrastructure exists)
        - Permian: ~$0.75/bbl avg disposal cost (lots of SWD capacity)
        - Marcellus: $2-4/bbl (limited SWD, must truck to Ohio)

        Challenges:
        - Seismicity (induced earthquakes from injection, esp. in Oklahoma, Texas)
        - Regulatory pressure to reduce injection volumes
        - SWD capacity constraints in some basins
        - Trucking logistics (600-1000 truck trips per well in high-water-cut plays)

        OPTION 2: RECYCLING / REUSE FOR FUTURE FRACS

        Technical approach:
        - Blend high-TDS flowback with fresh/brackish water to reduce salinity
        - Remove solids (filtration, settling tanks)
        - Kill bacteria (biocide, oxidizers, UV)
        - Add scale inhibitor (prevent BaSO4, SrSO4 precipitation)
        - Reuse as base fluid for next frac job

        Water quality targets for recycling:
        - TDS: <50,000 mg/L preferred (can go higher with additives)
        - TSS: <50 mg/L (prevent pump damage, perf plugging)
        - Oil & grease: <50 mg/L (emulsion issues)
        - Bacteria: <100 CFU/mL (prevent souring, biofouling)
        - Iron: <50 mg/L (can precipitate, cause scaling)

        Treatment technologies:
        - Settling/clarification (gravity separation of solids)
        - Filtration (multimedia, cartridge, membrane)
        - Chemical oxidation (chlorine dioxide, peroxide for bacteria/organics)
        - Evaporation/crystallization (remove dissolved salts, expensive)
        - Reverse osmosis (RO) (produces fresh water, but very expensive, high waste)

        Economics:
        - Basic treatment (settling + filtration + biocide): $0.25-0.75/bbl
        - Advanced treatment (RO, evaporation): $3-10/bbl
        - Breakeven: recycling economic if treatment cost < disposal cost
        - Permian: recycling growing (disposal getting expensive, ESG pressure)
        - Marcellus: recycling common (limited disposal, high trucking cost)

        Infrastructure:
        - Centralized treatment facilities (serve multiple operators)
        - Portable treatment units (on-site, move well to well)
        - Impoundments (temporary storage, blending)
        - Pipeline networks (move water between pads)

        Challenges:
        - Variable water chemistry (requires flexible treatment)
        - Scaling risk (mixing incompatible waters)
        - Bacterial souring (need continuous biocide)
        - Regulatory approval (some states require permits for recycling)

        OPTION 3: TREATMENT TO DISCHARGE STANDARDS (rare)

        - Remove TDS to <500 mg/L (drinking water standard) or <1,000 mg/L (surface discharge)
        - Requires advanced treatment (RO, evaporation, distillation)
        - Very expensive: $5-20/bbl
        - Only economic if no disposal or recycling options exist
        - Rare in US oil and gas (limited to some California operations)

        Basin-specific strategies:

        PERMIAN BASIN:
        - High water cut (5-20 bbl water per bbl oil in many wells)
        - Extensive SWD network (lowest disposal costs in US)
        - Growing recycling (Diamondback, Pioneer leading)
        - Waterflood wastewater also requires disposal

        MARCELLUS SHALE:
        - Lower water volumes (gas wells)
        - Limited in-state disposal (environmental opposition)
        - Truck to Ohio SWD wells ($2-4/bbl)
        - High recycling rates (50-90% in some areas)

        EAGLE FORD:
        - Moderate water cut
        - Good SWD infrastructure (South Texas)
        - Mix of disposal and recycling

        BAKKEN:
        - Lower water cut initially (increases with well age)
        - SWD infrastructure adequate
        - Cold climate challenges (winterization, freezing)

        Future trends:
        - Increased recycling (regulatory, ESG, cost)
        - Centralized water management (multi-operator facilities)
        - Beneficial reuse (agriculture, industrial, rare but growing)
        - Real-time water quality monitoring (optimize blending)
        - Produced water as resource, not waste (mindset shift)
        """,
        key_factors=[
            "Water chemistry (TDS, scaling ions, bacteria)",
            "Flowback volume per well",
            "Local SWD capacity and pricing",
            "Recycling infrastructure availability",
            "Treatment technology costs",
            "Regulatory approval for disposal/recycling",
            "Trucking vs pipeline logistics",
            "Future frac demand (market for recycled water)",
            "ESG and community relations"
        ],
        primary_authority=[
            "EPA UIC Class II regulations (40 CFR 144-148)",
            "State water disposal permits and regulations",
            "SPE papers on produced water management",
            "DOE research on water treatment technologies",
            "Operator water management best practices",
            "Basin-specific water studies (USGS, universities)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.WATER_MANAGEMENT,
        adversarial_considerations="Disposal vs recycling is hotly debated. Environmentalists push for recycling and zero discharge. Operators prefer disposal (simpler, cheaper in many basins). Seismicity concerns are forcing industry toward recycling in some areas (Oklahoma, Texas). Economics and regulations both driving the shift.",
        interaction_dependencies=["Flowback Water Quality", "Load Recovery Optimization"]
    ),

    DoctrineBlock(
        topic="Initial Production (IP) Rate Determination",
        keywords=["IP", "initial production", "24-hour", "rate", "decline", "EUR", "reserves"],
        conclusion_template="Initial Production (IP) rate is typically measured as average rate over first 24 hours or 30 days on production. Industry standard is 24-hour IP (IP24) reported in BOE/d. IP is marketing metric for well performance but poor predictor of EUR - decline curve analysis required for reserves estimation.",
        reasoning_framework="""
        IP rate definitions and measurement:

        IP24 (24-hour IP):
        - Average production rate over first 24 hours of continuous production
        - Measured after flowback cleanup (when on sales, no longer flowing to tanks)
        - Reported in barrels of oil equivalent per day (BOE/d)
        - Conversion: Gas (Mcf) to BOE using 6:1 ratio (6 Mcf = 1 BOE)
        - Most common industry standard for press releases and well performance comparisons

        IP30 (30-day IP):
        - Average production rate over first 30 days on production
        - More conservative metric (includes early decline)
        - Better predictor of well performance than IP24
        - Less common in marketing but more useful for engineering

        Peak rate:
        - Highest single-day production rate achieved
        - Often during early flowback (not representative of sustained production)
        - Can be misleading (transient, not economically recoverable at that rate)

        Measurement protocol:

        TIMING:
        - IP24 starts when well is placed on sales (pipeline or tank battery)
        - Excludes flowback period (flowback to sales timeline varies: 3-30 days)
        - Must be continuous 24-hour period (shutdowns invalidate measurement)

        RATE ALLOCATION:
        - Oil rate: measured via LACT unit or tank gauging
        - Gas rate: measured via orifice or turbine meter
        - Water rate: measured or estimated (often by difference)
        - Total liquids = oil + water
        - BOE = oil (bbl) + [gas (Mcf) / 6]

        CHOKE SETTING:
        - IP should be measured at optimized choke (not maximum choke)
        - Aggressive choke inflates IP but may damage formation
        - Industry practice: measure at choke size expected for long-term operation

        Basin-specific IP ranges (IP24 in BOE/d):

        PERMIAN DELAWARE:
        - Tier 1 wells: 1,500-3,000 BOE/d
        - Tier 2 wells: 750-1,500 BOE/d
        - Tier 3 wells: 300-750 BOE/d
        - Economic threshold: ~500 BOE/d for typical well costs

        PERMIAN MIDLAND:
        - Tier 1: 1,000-2,500 BOE/d
        - Tier 2: 500-1,000 BOE/d
        - Lower IPs than Delaware but better EUR in some intervals

        EAGLE FORD:
        - Oil window: 500-1,500 BOE/d (western Eagle Ford)
        - Condensate window: 1,000-3,000 BOE/d (central)
        - Dry gas window: 5-15 MMcf/d (eastern, convert to BOE/d)

        BAKKEN:
        - Middle Bakken: 500-1,500 BOE/d
        - Three Forks: 400-1,200 BOE/d
        - Decline steeper than Permian (need higher IP for economics)

        MARCELLUS/UTICA (gas):
        - Tier 1: 15-30 MMcf/d (2,500-5,000 BOE/d equivalent)
        - Tier 2: 8-15 MMcf/d (1,300-2,500 BOE/d)
        - Very low decline rates (good EUR relative to IP)

        Relationship between IP and EUR:

        CORRELATION:
        - Positive correlation: higher IP generally means higher EUR
        - But not linear: doubling IP does not double EUR
        - Decline rate matters more than IP for EUR
        - Example: 1,000 BOE/d IP with 50% b-factor may have same EUR as 2,000 BOE/d IP with 70% b-factor

        DECLINE CURVE ANALYSIS (Arps hyperbolic):
        q(t) = qi / (1 + b × Di × t)^(1/b)
        Where:
        - qi = initial rate (IP)
        - Di = initial decline rate (% per year)
        - b = hyperbolic exponent (0 = exponential, 1 = harmonic)
        - EUR = cumulative production over well life (often 30 years)

        Typical decline parameters by basin:
        - Permian: b = 0.6-1.2, Di = 50-80% per year
        - Eagle Ford: b = 0.8-1.5, Di = 60-90% per year
        - Bakken: b = 1.0-1.8, Di = 70-95% per year
        - Marcellus: b = 0.3-0.8, Di = 30-60% per year (shallower decline)

        IP optimization vs EUR optimization:
        - IP-focused: aggressive choke, maximize early rate (good for marketing, bad for EUR)
        - EUR-focused: conservative choke, protect fractures (better long-term economics)
        - Public companies face pressure to report high IPs (stock price impact)
        - Private equity firms focus on EUR and NPV (less IP obsession)

        Reporting and benchmarking:
        - Operators report IP24 in quarterly earnings (avg across wells drilled)
        - Analyst community tracks IP trends (basin maturation, parent-child effects)
        - Declining IPs may indicate formation depletion or completion issues
        - IP creep (increasing IPs) indicates better completion designs

        Limitations of IP as metric:
        - Does not account for well cost (high IP, high cost may have poor economics)
        - Does not predict EUR (need 6-12 months production history for reliable forecast)
        - Can be gamed (aggressive choke, short measurement period)
        - Marketing-focused, not engineering-focused
        """,
        key_factors=[
            "Measurement timing (when flowback ends, production stabilizes)",
            "Choke setting during measurement (optimized vs maximum)",
            "Oil vs gas vs BOE reporting conventions",
            "Basin-specific IP ranges and expectations",
            "Correlation (or lack thereof) between IP and EUR",
            "Decline curve parameters (b-factor, Di)",
            "Operator motivations (IP marketing vs EUR optimization)",
            "Well cost per BOE/d of IP (economic efficiency metric)"
        ],
        primary_authority=[
            "SPE reserves definitions and guidelines",
            "Operator reporting standards (quarterly filings)",
            "Arps decline curve equations (SPE papers)",
            "Basin-specific type curves (consulting firms, operators)",
            "SEC reserves reporting rules (if public company)",
            "Industry benchmarking databases (Enverus, Wood Mackenzie)"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.PRODUCTION_OPT,
        adversarial_considerations="IP is the most abused metric in unconventional oil and gas. Operators cherry-pick best wells, measure at maximum choke, and report IP before decline sets in. Smart investors focus on EUR, F&D costs, and recycle ratios - not IP. IP sells stocks; EUR makes money.",
        interaction_dependencies=["Choke Management Strategy", "EUR Forecasting"]
    ),

    DoctrineBlock(
        topic="Surfactant-Assisted Flowback",
        keywords=["surfactant", "wettability", "imbibition", "cleanup", "recovery", "chemistry"],
        conclusion_template="Surfactant-assisted flowback uses chemical surfactants injected post-frac to alter wettability, reduce interfacial tension, and improve frac fluid recovery. Field results show 10-30% increase in load recovery and 15-25% improvement in early gas/oil production in some basins. Cost is $5,000-20,000 per well.",
        reasoning_framework="""
        Surfactant flowback chemistry and mechanisms:

        WETTABILITY ALTERATION:
        - Shale formations are often mixed-wet or oil-wet (water-wet is rare)
        - Oil-wet rock preferentially imbibes oil, traps water in pores
        - Water-wet rock imbibes water, makes oil recovery easier
        - Surfactants adsorb to rock surface, change wettability from oil-wet to water-wet
        - Result: frac fluid flows back instead of being trapped by capillary forces

        INTERFACIAL TENSION (IFT) REDUCTION:
        - Water-oil IFT in shale: 20-50 dynes/cm (untreated)
        - Surfactants reduce IFT to 0.1-5 dynes/cm
        - Lower IFT reduces capillary pressure (Pc = 2γcosθ / r)
        - Frees trapped frac fluid from small pores and microfractures

        EMULSION PREVENTION:
        - Surfactants prevent formation of tight emulsions (oil-water mixing)
        - Stable emulsions increase viscosity, reduce flowback rates
        - Demulsification improves oil-water separation in surface equipment

        MICROEMULSION FORMATION:
        - Some surfactants create microemulsions (oil droplets in water)
        - Mobilizes residual oil trapped in matrix
        - Can increase oil recovery during flowback

        Surfactant types and selection:

        ANIONIC SURFACTANTS:
        - Negatively charged head group (sulfates, sulfonates, carboxylates)
        - Best for water-wetting sandstone, less effective in shale
        - Example: sodium dodecyl sulfate (SDS)

        CATIONIC SURFACTANTS:
        - Positively charged head group (quaternary ammonium)
        - Adsorb strongly to negatively charged shale surfaces
        - Good for wettability alteration in shale
        - Example: cetyltrimethylammonium bromide (CTAB)

        NONIONIC SURFACTANTS:
        - No charge (ethoxylates, alkyl polyglucosides)
        - Best IFT reduction, less wettability alteration
        - Less sensitive to salinity (good for high-TDS brines)
        - Example: alcohol ethoxylates, sorbitan esters

        AMPHOTERIC SURFACTANTS:
        - Dual charge (zwitterionic)
        - pH-dependent behavior
        - Good thermal stability
        - Example: betaines, sultaines

        FLUOROSURFACTANTS:
        - Extremely low IFT (can reach <0.01 dynes/cm)
        - Expensive, environmental concerns (PFAS)
        - Rarely used in oil and gas anymore

        Application methods:

        OPTION 1: PRE-FLUSH (before flowback):
        - Inject surfactant slug (10-50 bbl) down tubing after frac
        - Shut in well for soak period (6-24 hours)
        - Surfactant contacts formation, alters wettability
        - Begin flowback
        - Timing challenge: don't want to wait too long (deferred production)

        OPTION 2: MIXED WITH FRAC FLUID:
        - Add surfactant to frac fluid (0.1-0.5 gpt concentration)
        - Surfactant distributed throughout fracture network during pumping
        - No separate injection step, no soak time delay
        - Lower concentration may be less effective

        OPTION 3: CONTINUOUS INJECTION DURING FLOWBACK:
        - Inject surfactant continuously at low rate (0.5-2 bpm)
        - Surfactant swept through formation by flowback
        - Good for extended flowback periods
        - Requires injection equipment on-site

        Field performance results:

        PERMIAN BASIN (multiple operators):
        - Load recovery increase: 15-25% (from 40% to 55%)
        - Oil production uplift: 10-20% in first 90 days
        - Gas production uplift: 5-15%
        - Cost: $10,000-15,000 per well
        - Payback: <3 months in most cases

        EAGLE FORD (condensate window):
        - Load recovery increase: 20-30%
        - Condensate uplift: 15-25%
        - Faster cleanup (flowback to sales in 5 days vs 10 days)
        - Cost: $8,000-12,000 per well

        BAKKEN:
        - Load recovery increase: 10-20% (formation very tight, harder to see benefit)
        - Oil uplift: 5-15%
        - Mixed results (some operators see benefit, others don't)
        - Cost: $12,000-18,000 per well

        MARCELLUS/UTICA (gas):
        - Load recovery increase: 10-20%
        - Gas production uplift: 10-20% in early flowback
        - Reduced water handling costs (faster cleanup)
        - Cost: $5,000-10,000 per well

        Challenges and limitations:

        SURFACTANT ADSORPTION:
        - Surfactant adsorbs to rock (especially clay minerals)
        - High adsorption reduces concentration in flowback fluid
        - May require higher injection volumes than predicted

        SALINITY SENSITIVITY:
        - Anionic surfactants lose effectiveness at high TDS (>50,000 mg/L)
        - Must select surfactant compatible with formation brine chemistry
        - Nonionic surfactants more tolerant of high salinity

        TEMPERATURE STABILITY:
        - Surfactants can degrade at high temperature (>200°F)
        - Shale formations typically 150-300°F
        - Must select thermally stable surfactants

        COST-BENEFIT ANALYSIS:
        - Surfactant cost: $5,000-20,000 per well
        - Incremental production: 1,000-5,000 BOE in first year
        - NPV at $70/bbl oil: $70,000-350,000
        - ROI: 3-20x (highly economic in most cases)
        - But: results are formation-dependent, not universal

        Vendor landscape:
        - Baker Hughes (CLEANUP additives)
        - Halliburton (FlowPro surfactants)
        - Schlumberger (SurfClear)
        - Specialty chemical companies (Huntsman, BASF, Stepan)
        - Formulations are proprietary, limited technical disclosure
        """,
        key_factors=[
            "Formation wettability (oil-wet vs water-wet)",
            "Surfactant type selection (anionic, cationic, nonionic)",
            "Application method (pre-flush, mixed, continuous injection)",
            "Surfactant concentration and volume",
            "Soak time (if pre-flush method)",
            "Formation brine salinity and compatibility",
            "Temperature stability of surfactant",
            "Cost-benefit economics (incremental production vs surfactant cost)",
            "Offset well performance data with/without surfactant"
        ],
        primary_authority=[
            "SPE papers on surfactant-assisted flowback",
            "Service company technical literature (Baker Hughes, Halliburton, SLB)",
            "University research (UT Austin, Colorado School of Mines)",
            "Operator field trials and case studies",
            "Surfactant vendor data sheets"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.LOAD_RECOVERY,
        adversarial_considerations="Surfactant vendors oversell performance - field results are highly variable. Some operators see 20%+ uplift, others see zero. Formation-specific testing required. Don't assume results from Permian apply to Bakken. Beware of cherry-picked case studies in vendor presentations.",
        interaction_dependencies=["Load Recovery Optimization", "Frac Fluid Recovery Efficiency"]
    ),

    DoctrineBlock(
        topic="Nitrogen-Assisted Flowback",
        keywords=["nitrogen", "N2", "gas lift", "unloading", "liquid loading", "foam"],
        conclusion_template="Nitrogen-assisted flowback injects nitrogen gas downhole to unload liquid, reduce hydrostatic pressure, and improve flowback rates in low-pressure or liquid-loaded wells. Common in Marcellus gas wells and CBM. Cost is $20,000-50,000 per well for equipment and N2 supply.",
        reasoning_framework="""
        Nitrogen-assisted flowback mechanics:

        LIQUID LOADING PROBLEM:
        - Low-pressure wells cannot lift liquids to surface
        - Liquid accumulates in wellbore (loading up)
        - Wellbore pressure increases, chokes off inflow from formation
        - Well dies or produces at very low rate
        - Common in: gas wells, depleted oil wells, coalbed methane (CBM)

        NITROGEN INJECTION SOLUTION:
        - Inject nitrogen gas down tubing or annulus
        - N2 aerates liquid column (creates foam or mist)
        - Reduces hydrostatic pressure on formation
        - Gas expansion provides lift energy
        - Liquids flow to surface, well unloads

        DENSITY REDUCTION:
        - Pure water column: 0.433 psi/ft hydrostatic gradient
        - 50% N2 aerated: ~0.15-0.25 psi/ft gradient
        - 10,000 ft well: hydrostatic pressure reduced from 4,330 psi to 1,500-2,500 psi
        - Drawdown increased, inflow from formation increases

        Operational configurations:

        CONTINUOUS INJECTION:
        - N2 injected continuously during flowback
        - Rate: 1-5 MMscf/d (100-500 Mscf/hr)
        - Injected down annulus (casing-tubing) or macaroni string
        - Produces up tubing
        - Used for extended flowback (weeks to months)

        INTERMITTENT INJECTION (CHAMBER LIFT):
        - Inject N2 in cycles (on for 15 min, off for 45 min)
        - Liquid accumulates during off cycle, lifted during on cycle
        - Lower N2 consumption than continuous
        - Used for low-rate wells

        SOAP/FOAM INJECTION:
        - Add foaming surfactant with N2
        - Creates stable foam (better liquid lifting)
        - Reduces N2 rate requirement (more efficient)
        - Surfactant cost: $500-2,000 per well

        Equipment and logistics:

        N2 SUPPLY:
        - Cryogenic liquid N2 tanker trucks (typically 7,500-9,000 gallons LN2 per truck)
        - 1 gallon LN2 = 93 scf gaseous N2
        - Consumption: 1-5 MMscf/d = 10-50 gallons LN2/hr = 2-10 trucks per week
        - Cost: $0.50-2.00 per Mcf (region-dependent)

        INJECTION EQUIPMENT:
        - Cryogenic pump (converts liquid N2 to high-pressure gas)
        - Vaporizer (heat exchanger)
        - Pressure control system (regulate injection rate)
        - Safety systems (pressure relief, N2 detection)
        - Rental cost: $5,000-15,000 per month

        WELLHEAD CONFIGURATION:
        - Install lubricator or snubbing unit to inject down annulus
        - Or run macaroni string (1-2" coiled tubing) down production tubing
        - Packer optional (isolate annulus from tubing)

        Application in different well types:

        MARCELLUS/UTICA GAS WELLS:
        - Problem: high water production during flowback (5,000-20,000 bbl)
        - Low reservoir pressure in some areas (<2,000 psi)
        - N2 lift accelerates water removal, gets to gas production faster
        - Duration: 1-4 weeks typically
        - Cost: $20,000-40,000 per well
        - Payback: faster time to sales, higher early gas rates

        COALBED METHANE (CBM):
        - Very low reservoir pressure (<500 psi)
        - High water production (dewatering required)
        - N2 lift essential in many CBM fields (Powder River, San Juan Basin)
        - Continuous lift for months to years (not just flowback)
        - Economics marginal (low gas prices, high operating cost)

        PERMIAN BASIN OIL WELLS (rare):
        - Most Permian wells have sufficient pressure (don't need N2)
        - Occasional use in old, depleted wells or re-fracs
        - Duration: days to weeks

        BAKKEN OIL WELLS:
        - Rarely needed (high reservoir pressure)
        - Occasional use if well was shut in for extended period (liquid loading)

        Optimization and monitoring:

        N2 INJECTION RATE OPTIMIZATION:
        - Too low: insufficient lift, well still loaded
        - Too high: waste N2, no incremental benefit, potential for gas interference
        - Typical range: 0.5-3 MMscf/d for vertical wells, 1-5 MMscf/d for horizontal
        - Optimize using gradient surveys (pressure/temperature logging while flowing)

        INJECTION PRESSURE:
        - Must exceed wellhead pressure + friction losses
        - Typical: 500-3,000 psi injection pressure
        - Safety limit: do not exceed casing pressure rating

        MONITORING:
        - Wellhead pressure (should decrease as well unloads)
        - Production rate (oil, gas, water - should increase)
        - N2 consumption rate (optimize for cost)
        - Liquid level surveys (echometer, acoustic) - measure fluid column height

        Economics:

        COST COMPONENTS:
        - N2 supply: $10,000-30,000 (1-4 weeks × 2-5 MMscf/d × $1-2/Mcf)
        - Equipment rental: $5,000-15,000 per month
        - Trucking/logistics: $2,000-5,000
        - Labor/supervision: $3,000-8,000
        - Total: $20,000-50,000 per well

        BENEFIT:
        - Faster flowback (1-2 weeks vs 3-6 weeks without N2)
        - Higher early production rates (2-5x increase during unloading)
        - Reduced downtime (well doesn't die from liquid loading)
        - Incremental gas production: 50-200 MMcf (Marcellus typical)
        - NPV at $3/Mcf gas: $150,000-600,000
        - ROI: 3-10x (highly economic in gas wells)

        Alternatives to N2:
        - Plunger lift (mechanical, no gas injection, lower cost but less effective)
        - Velocity string (smaller tubing to increase velocity, no external energy)
        - Electric submersible pump (ESP) (for oil wells, not gas wells)
        - Natural gas lift (use produced gas, cheaper than N2 but not always available)

        Safety considerations:
        - N2 is asphyxiant (displaces oxygen, confined space hazard)
        - N2 detection systems required (portable monitors)
        - Proper ventilation during operations
        - Cryogenic hazards (LN2 at -320°F, frostbite risk)
        - High-pressure gas hazards (equipment failure can cause injuries)
        """,
        key_factors=[
            "Reservoir pressure (low pressure = more likely to need N2)",
            "Water production rate during flowback",
            "Well depth and configuration (vertical vs horizontal)",
            "N2 supply availability and cost",
            "Equipment rental costs",
            "Injection rate optimization (balance cost vs effectiveness)",
            "Duration of N2 lift requirement",
            "Safety protocols for N2 handling",
            "Economic analysis (incremental production vs N2 cost)"
        ],
        primary_authority=[
            "SPE papers on gas lift and unloading",
            "N2 service providers (Air Liquide, Linde, Airgas)",
            "Operator field procedures",
            "CBM and shale gas case studies",
            "API RP 11V7 (Gas Lift Design)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PRODUCTION_OPT,
        adversarial_considerations="N2 lift is standard practice in Marcellus gas wells but overkill in high-pressure oil wells. Service companies push N2 on every well (they make money on it). Engineering analysis required - don't N2 lift a well that doesn't need it. Plunger lift is cheaper and often sufficient.",
        interaction_dependencies=["Flowback to Sales Timeline", "Liquid Loading Management"]
    ),

    DoctrineBlock(
        topic="Formation Damage Prevention During Flowback",
        keywords=["formation damage", "permeability", "skin", "clay swelling", "fines migration", "scale"],
        conclusion_template="Formation damage during flowback reduces near-wellbore permeability, increases skin factor, and permanently impairs well productivity. Primary damage mechanisms: clay swelling, fines migration, scale precipitation, proppant embedment. Prevention requires compatible frac fluids, controlled drawdown, and inhibitor chemicals.",
        reasoning_framework="""
        Formation damage mechanisms during flowback:

        1. CLAY SWELLING:
        - Shale formations contain swelling clays (smectite, mixed-layer illite-smectite)
        - Freshwater or low-salinity frac fluid contacts clay minerals
        - Clays hydrate and expand (can swell 10-100x original volume)
        - Swelling reduces pore throat size, blocks flow paths
        - Permeability reduction: 50-90% in severe cases
        - Irreversible (clay does not shrink back when dried)

        CLAY TYPES AND SWELLING POTENTIAL:
        - Smectite (montmorillonite): highest swelling (expands ~15x)
        - Mixed-layer illite-smectite: moderate swelling
        - Illite: low swelling
        - Kaolinite: minimal swelling but can migrate as fines
        - Chlorite: minimal swelling, acid-sensitive

        PREVENTION:
        - Use KCl (potassium chloride) in frac fluid (2-3% concentration)
        - KCl stabilizes clays (potassium ion prevents hydration)
        - Avoid pure freshwater contact with formation
        - Use clay stabilizer chemicals (quaternary amines, cationic polymers)
        - Pre-flush with KCl brine before flowback

        2. FINES MIGRATION:
        - Formation contains mobile fines (clay particles, rock fragments, proppant fines)
        - High fluid velocity during flowback mobilizes fines
        - Fines plug pore throats downstream (lodging mechanism)
        - Permeability reduction: 30-70%
        - Can be partially reversible (backflow or acid treatment)

        CRITICAL VELOCITY:
        - Below critical velocity: fines remain attached to pore walls
        - Above critical velocity: fines detach and migrate
        - Vcrit depends on: pore throat size, fines size, fluid salinity, wettability
        - Typically: Vcrit = 0.1-1 ft/day for shale (very low)

        PREVENTION:
        - Controlled drawdown (gradual choke increases)
        - High-salinity frac fluid (electrostatic stabilization of fines)
        - Resin-coated proppant (reduces proppant fines)
        - Pre-pack screens (filter fines, but reduces conductivity)

        3. SCALE PRECIPITATION:
        - Mixing of frac fluid and formation brine
        - Incompatible waters cause mineral precipitation
        - BaSO4, SrSO4, CaSO4, CaCO3 scales
        - Blocks fractures and near-wellbore permeability
        - Permeability reduction: 20-60%

        SCALING CHEMISTRY:
        - Frac fluid: low TDS, may contain sulfate (from makeup water)
        - Formation brine: high TDS, high Ca/Ba/Sr
        - When mixed: exceed solubility product, scale precipitates
        - BaSO4 worst: extremely insoluble, cannot be acid-dissolved

        PREVENTION:
        - Scale inhibitor in frac fluid (0.5-2 gpt phosphonate or polymer)
        - Avoid sulfate in makeup water (use RO or softened water)
        - Control pH (lower pH reduces carbonate scale)
        - Squeeze scale inhibitor into formation (lasts 3-12 months)

        4. PROPPANT EMBEDMENT:
        - High closure stress crushes proppant into formation face
        - Creates "proppant rind" at fracture-formation interface
        - Reduces effective fracture width, increases flow resistance
        - Permeability reduction: 10-40% (localized near fracture face)
        - Worse in soft formations (low Young's modulus, high Poisson's ratio)

        PREVENTION:
        - Use high-strength proppant (ceramic vs sand)
        - Optimize proppant loading (not too high, causes embedment)
        - Conservative drawdown (reduce closure stress)
        - Proppant size selection (larger proppant embeds less)

        5. EMULSION BLOCKING:
        - Oil-water emulsions form during flowback (especially in oil wells)
        - Emulsions are viscous (10-1000 cp vs 1 cp for water)
        - Block flow in pores and fractures
        - Permeability reduction: 30-80% (temporary, can break with time/chemicals)

        PREVENTION:
        - Demulsifier in frac fluid or flowback (0.1-0.5 gpt)
        - Control flowback rate (high shear can create emulsions)
        - Use nonemulsifying surfactants
        - Heat (surface tanks, promotes emulsion breaking)

        Skin factor and productivity impact:

        SKIN FACTOR DEFINITION:
        - Dimensionless measure of near-wellbore damage
        - s = 0: no damage (ideal)
        - s > 0: positive skin, damage (permeability reduced)
        - s < 0: negative skin, stimulation (permeability enhanced, rare)

        PRODUCTIVITY INDEX (PI):
        PI = q / (Pr - Pwf)
        Where:
        - q = production rate
        - Pr = reservoir pressure
        - Pwf = wellbore flowing pressure
        - PI reduction = measure of formation damage

        RELATIONSHIP:
        - Skin of +5 can reduce PI by 50% (half the production rate)
        - Skin of +10 can reduce PI by 75%
        - Skin of +20 can reduce PI by 90% (well nearly killed)

        Damage detection and quantification:

        PRESSURE TRANSIENT ANALYSIS (PTA):
        - Buildup test or diagnostic fracture injection test (DFIT)
        - Analyze pressure vs time data
        - Extract skin factor from log-log plot
        - Requires pressure gauge and flow rate data

        PRODUCTION DECLINE ANALYSIS:
        - Compare actual production to type curve (undamaged well)
        - Lower production = positive skin
        - Requires offset well data for baseline

        FLOWBACK WATER VOLUME:
        - Low load recovery (<20%) may indicate severe damage
        - Fluid trapped by damage, cannot flow back

        Damage remediation (if prevention fails):

        ACID TREATMENT:
        - HCl acid for carbonate scales, clay dissolution
        - HF acid for silicate dissolution (very aggressive, use carefully)
        - Inject acid, soak, flowback
        - Cost: $50,000-200,000
        - Can improve skin by 5-20 points

        SOLVENT TREATMENT:
        - Mutual solvents for emulsion breaking
        - Aromatic solvents for asphaltene/paraffin removal
        - Cost: $20,000-100,000

        REFRACK:
        - If damage is severe and irreversible, refrack the well
        - New fracture bypasses damaged zone
        - Cost: $1-3 million
        - Last resort option
        """,
        key_factors=[
            "Formation mineralogy (clay type and content)",
            "Frac fluid compatibility (salinity, pH, additives)",
            "Drawdown rate during flowback (slow = less damage)",
            "Water chemistry (scaling potential)",
            "Proppant type and strength (embedment resistance)",
            "Use of clay stabilizers and scale inhibitors",
            "Monitoring for damage indicators (low PI, low recovery)",
            "Remediation options (acid, solvent, refrack)"
        ],
        primary_authority=[
            "SPE papers on formation damage",
            "Schlumberger oilfield chemistry handbook",
            "API RP 42 (Formation Damage)",
            "University research (Stanford, UT Austin)",
            "Service company technical manuals",
            "Operator damage case studies"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.FORMATION_DAMAGE,
        adversarial_considerations="Formation damage is often blamed for poor well performance when real issue is bad completion design or reservoir quality. Service companies push expensive acid treatments that may not help. Root cause analysis required - don't throw money at acid jobs without confirming damage exists and is treatable.",
        interaction_dependencies=["Choke Management Strategy", "Frac Fluid Chemistry"]
    )
]

# Telemetry and monitoring
class Telemetry:
    def __init__(self):
        self.query_count = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.doctrine_triggers: Dict[str, int] = defaultdict(int)
        self.start_time = datetime.now()
        self.error_log: List[Dict[str, Any]] = []

    def log_query(self, query: str, mode: ResponseMode, triggered_doctrines: List[str], cache_hit: bool):
        self.query_count += 1
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        for doctrine in triggered_doctrines:
            self.doctrine_triggers[doctrine] += 1

        logger.info(
            f"Query processed | Mode: {mode} | Doctrines: {len(triggered_doctrines)} | Cache: {'HIT' if cache_hit else 'MISS'}"
        )

    def log_error(self, error: str, context: Dict[str, Any]):
        self.error_log.append({
            "timestamp": datetime.now().isoformat(),
            "error": error,
            "context": context
        })
        logger.error(f"Error logged: {error} | Context: {context}")

    def get_stats(self) -> Dict[str, Any]:
        uptime = (datetime.now() - self.start_time).total_seconds()
        cache_rate = self.cache_hits / self.query_count if self.query_count > 0 else 0.0

        return {
            "uptime_seconds": uptime,
            "total_queries": self.query_count,
            "cache_hit_rate": cache_rate,
            "doctrine_trigger_counts": dict(self.doctrine_triggers),
            "error_count": len(self.error_log)
        }


# Initialize FastAPI app
APP = FastAPI(
    title="FRAC07 - Flowback & Well Cleanup Intelligence Engine",
    description="TIE Gold Standard engine for flowback operations expertise",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Global telemetry
TELEMETRY = Telemetry()

# Doctrine cache (keyword-based fast lookup)
DOCTRINE_CACHE: Dict[str, List[DoctrineBlock]] = {}

def build_doctrine_cache():
    """Build keyword-based doctrine lookup cache."""
    for block in DOCTRINE_BLOCKS:
        for keyword in block.keywords:
            keyword_lower = keyword.lower()
            if keyword_lower not in DOCTRINE_CACHE:
                DOCTRINE_CACHE[keyword_lower] = []
            DOCTRINE_CACHE[keyword_lower].append(block)
    logger.info(f"Doctrine cache built: {len(DOCTRINE_CACHE)} keywords indexing {len(DOCTRINE_BLOCKS)} blocks")


def find_relevant_doctrines(query: str, top_n: int = 5) -> List[DoctrineBlock]:
    """Find relevant doctrine blocks using keyword matching."""
    query_lower = query.lower()
    scores: Dict[str, float] = defaultdict(float)

    # Score each doctrine block by keyword matches
    for keyword, blocks in DOCTRINE_CACHE.items():
        if keyword in query_lower:
            for block in blocks:
                scores[block.topic] += 1.0

    # Rank blocks by score
    ranked = sorted(
        [(topic, score) for topic, score in scores.items()],
        key=lambda x: x[1],
        reverse=True
    )

    # Return top N blocks
    result = []
    seen_topics = set()
    for topic, _ in ranked[:top_n]:
        if topic not in seen_topics:
            block = next(b for b in DOCTRINE_BLOCKS if b.topic == topic)
            result.append(block)
            seen_topics.add(topic)

    return result


def generate_response(query: str, doctrines: List[DoctrineBlock], mode: ResponseMode) -> str:
    """Generate response based on mode and triggered doctrines."""
    if not doctrines:
        return "No relevant flowback operations doctrine found. Please provide more specific information about equipment, choke management, data acquisition, load recovery, proppant management, water disposal, emissions, or production optimization."

    if mode == ResponseMode.FAST:
        # Concise response using conclusion templates
        parts = []
        for doctrine in doctrines[:3]:
            parts.append(f"{doctrine.topic}: {doctrine.conclusion_template}")
        return "\n\n".join(parts)

    elif mode == ResponseMode.DEFENSE:
        # Detailed response with reasoning and authority
        parts = []
        for doctrine in doctrines[:3]:
            section = f"## {doctrine.topic}\n\n"
            section += f"{doctrine.conclusion_template}\n\n"
            section += f"**Reasoning:**\n{doctrine.reasoning_framework[:500]}...\n\n"
            section += f"**Key Factors:** {', '.join(doctrine.key_factors[:5])}\n\n"
            section += f"**Authority:** {', '.join(doctrine.primary_authority)}\n"
            parts.append(section)
        return "\n\n".join(parts)

    else:  # MEMO
        # Comprehensive response with full reasoning
        parts = []
        for doctrine in doctrines:
            section = f"## {doctrine.topic}\n\n"
            section += f"**Conclusion:** {doctrine.conclusion_template}\n\n"
            section += f"**Full Reasoning Framework:**\n{doctrine.reasoning_framework}\n\n"
            section += f"**Key Factors:**\n"
            for factor in doctrine.key_factors:
                section += f"- {factor}\n"
            section += f"\n**Primary Authority:**\n"
            for auth in doctrine.primary_authority:
                section += f"- {auth}\n"
            if doctrine.adversarial_considerations:
                section += f"\n**Adversarial Considerations:** {doctrine.adversarial_considerations}\n"
            parts.append(section)
        return "\n\n".join(parts)


def compute_determinism_hash(query: str, doctrines: List[DoctrineBlock], mode: ResponseMode) -> str:
    """Compute SHA-256 hash for determinism verification."""
    content = f"{query}|{mode}|" + "|".join([d.topic for d in doctrines])
    return hashlib.sha256(content.encode()).hexdigest()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint - three-layer response with doctrine cache."""
    try:
        # Find relevant doctrines
        doctrines = find_relevant_doctrines(request.query, top_n=5)
        triggered_topics = [d.topic for d in doctrines]

        # Generate response
        answer = generate_response(request.query, doctrines, request.mode)

        # Determine confidence (use highest confidence from triggered doctrines)
        confidence = ConfidenceLevel.DEFENSIBLE
        if doctrines:
            confidence_order = [ConfidenceLevel.DEFENSIBLE, ConfidenceLevel.AGGRESSIVE, ConfidenceLevel.DISCLOSURE, ConfidenceLevel.HIGH_RISK]
            for doctrine in doctrines:
                if confidence_order.index(doctrine.confidence) > confidence_order.index(confidence):
                    confidence = doctrine.confidence

        # Compute determinism hash
        det_hash = compute_determinism_hash(request.query, doctrines, request.mode)

        # Log telemetry
        TELEMETRY.log_query(request.query, request.mode, triggered_topics, cache_hit=len(doctrines) > 0)

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            mode=request.mode,
            sources=[d.primary_authority[0] if d.primary_authority else "Field expertise" for d in doctrines[:3]],
            triggered_doctrines=triggered_topics,
            determinism_hash=det_hash,
            timestamp=datetime.now().isoformat(),
            query_id=hashlib.sha256(f"{request.query}{datetime.now().isoformat()}".encode()).hexdigest()[:16],
            metadata={
                "doctrines_evaluated": len(doctrines),
                "categories": list(set([d.category.value for d in doctrines]))
            }
        )

    except Exception as e:
        logger.exception("Query processing error")
        TELEMETRY.log_error(str(e), {"query": request.query, "mode": request.mode})
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint with comprehensive stats."""
    stats = TELEMETRY.get_stats()

    return HealthResponse(
        status="operational",
        version="1.0.0",
        port=9027,
        doctrines_loaded=len(DOCTRINE_BLOCKS),
        uptime_seconds=stats["uptime_seconds"],
        total_queries=stats["total_queries"],
        cache_hit_rate=stats["cache_hit_rate"]
    )


@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics."""
    return {
        "total_doctrines": len(DOCTRINE_BLOCKS),
        "doctrines": [
            {
                "topic": block.topic,
                "category": block.category.value,
                "keywords": block.keywords,
                "confidence": block.confidence.value
            }
            for block in DOCTRINE_BLOCKS
        ]
    }


@APP.on_event("startup")
async def startup_event():
    """Initialize engine on startup."""
    logger.info("FRAC07 Flowback Operations Engine starting...")
    build_doctrine_cache()
    logger.info(f"Engine ready with {len(DOCTRINE_BLOCKS)} doctrine blocks on port 9027")


@APP.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    stats = TELEMETRY.get_stats()
    logger.info(f"FRAC07 Engine shutting down | Queries processed: {stats['total_queries']}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(APP, host="0.0.0.0", port=9027, log_level="info")
