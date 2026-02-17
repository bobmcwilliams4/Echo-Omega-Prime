"""
PROD04 - Reservoir Management Intelligence Engine
TIE Gold Standard - Production Engineering Domain
Port: 9034
Version: 1.0.0

Real reservoir management expertise: material balance, drive mechanisms, EOR,
waterflood design, simulation, PVT properties, field development.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field, asdict
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# Configure logger
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "logs" / "prod04_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
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


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class IssueCategory(str, Enum):
    MATERIAL_BALANCE = "MATERIAL_BALANCE"
    DRIVE_MECHANISM = "DRIVE_MECHANISM"
    RECOVERY_FACTOR = "RECOVERY_FACTOR"
    WATERFLOOD = "WATERFLOOD"
    EOR = "EOR"
    SIMULATION = "SIMULATION"
    OOIP_OGIP = "OOIP_OGIP"
    PVT = "PVT"
    RELATIVE_PERM = "RELATIVE_PERM"
    HETEROGENEITY = "HETEROGENEITY"
    FIELD_DEVELOPMENT = "FIELD_DEVELOPMENT"


@dataclass
class DoctrineBlock:
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
    confidence_stratification: Dict[str, str]
    controlling_precedent: str
    issue_category: IssueCategory
    epistemic_guardrails: List[str] = field(default_factory=list)


@dataclass
class QueryMetrics:
    query_id: str
    timestamp: str
    mode: ResponseMode
    latency_ms: float
    cache_hit: bool
    doctrine_triggered: List[str]
    confidence: ConfidenceLevel
    zone: AnalysisZone
    issue_categories: List[str]
    determinism_hash: str


# ============================================================================
# PYDANTIC I/O MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., description="Reservoir management question")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(AnalysisZone.PLANNING, description="Analysis context")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    doctrines_applied: List[str]
    issue_categories: List[str]
    cache_hit: bool
    latency_ms: float
    determinism_hash: str
    epistemic_caveats: List[str]
    recommendations: List[str]
    query_id: str


class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrines_loaded: int
    cache_size: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float


# ============================================================================
# DOCTRINE CACHE - 25+ REAL RESERVOIR MANAGEMENT BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Material Balance Equation - Havlena-Odeh Method",
        keywords=["material balance", "havlena odeh", "drive index", "F vs Eo", "reservoir volumes"],
        conclusion_template=[
            "Apply Havlena-Odeh straight-line method to determine drive mechanism and original hydrocarbon in place.",
            "Plot F (underground withdrawal) vs appropriate E term based on suspected drive mechanism.",
            "Straight-line fit confirms drive type; slope yields OOIP/OGIP; intercept indicates additional drive energy."
        ],
        reasoning_framework="""
The material balance equation relates cumulative production to reservoir pressure decline:
N = (F - We) / (Eo + m*Eg + Ef,w)

Havlena-Odeh linearization:
1. Solution gas drive: F/Eo vs Ef,w/Eo → slope = m (gas cap size)
2. Gas cap drive: F/Eg vs Eo/Eg → intercept = N*m
3. Water drive: F vs (Eo + m*Eg + Ef,w) → slope = N, intercept = We

Drive indices:
- SDI (solution gas) = (Eo*N) / F
- DDI (gas cap) = (m*Eg*N) / F
- WDI (water drive) = We / F
- Sum to 1.0 at any time

Key assumptions:
- PVT data accurate (Bo, Bg, Rs correlations validated)
- Pressure history reliable (weighted average)
- Production data complete (oil, gas, water)
- Water influx model appropriate (if applicable)

Permian Basin considerations:
- Weak water drives typical (WDI < 0.1)
- Solution gas drive dominant early life
- Gas cap expansion in structural highs
- Pressure maintenance via water/gas injection
        """,
        key_factors=[
            "Accurate PVT properties (Bo, Bg, Rs, cf)",
            "Representative reservoir pressure (volumetric weighted)",
            "Complete production history (oil, gas, water)",
            "Appropriate water influx model selection",
            "Gas cap size estimation (m = ratio of initial gas cap to oil zone)",
            "Formation and water compressibility (cf, cw)",
            "Detection of pressure support mechanisms",
            "Data quality and consistency checks"
        ],
        primary_authority=[
            "Havlena & Odeh (1963) - 'The Material Balance as an Equation of a Straight Line'",
            "Dake, L.P. (1978) - Fundamentals of Reservoir Engineering",
            "Walsh & Lake (2003) - Primary Hydrocarbon Recovery",
            "Tarek Ahmed (2018) - Reservoir Engineering Handbook"
        ],
        burden_holder="Reservoir engineer performing material balance analysis",
        adversary_position="Material balance unreliable due to: poor PVT data, heterogeneous pressure distribution, unaccounted water influx, non-equilibrium gas-oil contact",
        counter_arguments=[
            "Material balance validated by independent volumetric OOIP/OGIP calculation",
            "PVT correlations calibrated to lab-measured samples",
            "Pressure surveys conducted in multiple wells across field",
            "History match of multiple drive scenarios tested",
            "Aquifer model validated by water production history"
        ],
        resolution_strategy="Integrate material balance with volumetric methods, simulation, and decline curve analysis for triangulated reserves estimate",
        entity_scope="Applies to all reservoir types; accuracy depends on data quality and aquifer model selection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Material balance with high-quality PVT, pressure, production data and validated aquifer model",
            "AGGRESSIVE": "Material balance with limited data or unvalidated water influx assumptions",
            "DISCLOSURE": "Acknowledge data gaps, aquifer uncertainty, and non-equilibrium conditions",
            "HIGH_RISK": "Applying material balance to complex compartmentalized or highly heterogeneous reservoirs without supporting evidence"
        },
        controlling_precedent="Havlena-Odeh straight-line method is SPE standard for drive mechanism identification",
        issue_category=IssueCategory.MATERIAL_BALANCE,
        epistemic_guardrails=[
            "Material balance is volumetric average - cannot detect compartmentalization",
            "Requires sufficient pressure decline to differentiate drive mechanisms",
            "Water influx model selection significantly impacts OOIP estimate"
        ]
    ),

    DoctrineBlock(
        topic="Drive Mechanism Identification",
        keywords=["solution gas drive", "gas cap drive", "water drive", "combination drive", "pressure decline", "GOR", "WOR"],
        conclusion_template=[
            "Identify primary drive mechanism from pressure-production behavior and drive indices.",
            "Solution gas: rapid pressure decline, increasing GOR, no water production.",
            "Water drive: slow pressure decline, stable GOR, increasing WOR."
        ],
        reasoning_framework="""
Drive mechanism classification:
1. Solution gas drive (depletion):
   - Rapid pressure decline (0.5-1.0 psi per bbl produced)
   - GOR rises steadily as gas breaks out
   - Recovery factor: 5-30% (typical 15-20%)
   - No natural pressure support

2. Gas cap drive:
   - Moderate pressure decline
   - GOR increases in structurally high wells
   - Recovery factor: 20-40%
   - Requires gravity segregation

3. Water drive (aquifer influx):
   - Slow pressure decline (maintained above bubble point)
   - Stable or declining GOR
   - WOR increases over time
   - Recovery factor: 35-75%
   - Strong: p/z remains constant (gas reservoirs)

4. Combination drive:
   - Features of multiple mechanisms
   - Drive indices evolve over time
   - Common in Permian: solution gas + weak water drive

Diagnostic indicators:
- Pressure decline rate vs production
- GOR trend (constant, increasing, decreasing)
- WOR trend (edge water, bottom water, no water)
- Drive index calculation from material balance
- Reservoir position vs OWC/GOC

Permian Basin typical:
- Weak to negligible water drives
- Solution gas dominant mechanism
- Gas cap in structural reservoirs
- Pressure maintenance via injection essential
        """,
        key_factors=[
            "Pressure decline rate (psi/bbl produced)",
            "GOR behavior (constant, rising, falling)",
            "WOR behavior (timing, rate, source)",
            "Structural position vs fluid contacts",
            "Material balance drive indices",
            "Aquifer strength and connectivity",
            "Recovery factor expectations by mechanism",
            "Economic optimization of drive"
        ],
        primary_authority=[
            "Muskat, M. (1949) - Physical Principles of Oil Production",
            "Clark, N.J. (1969) - Elements of Petroleum Reservoirs",
            "SPE Monograph Vol. 3 - Enhanced Oil Recovery",
            "McCain, W.D. (1990) - Properties of Petroleum Fluids"
        ],
        burden_holder="Reservoir engineer characterizing production mechanism",
        adversary_position="Drive mechanism misidentified; reservoir behavior attributed to wrong source of energy",
        counter_arguments=[
            "Multiple diagnostic criteria agree on drive mechanism",
            "Material balance drive indices consistent with observed behavior",
            "Analogous field performance validates interpretation",
            "Aquifer testing confirms water drive strength",
            "Simulation history match reproduces observed trends"
        ],
        resolution_strategy="Integrate pressure, production, and fluid analysis with material balance and analog fields for robust drive mechanism identification",
        entity_scope="Universal reservoir engineering principle; mechanism dictates field development strategy",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Drive mechanism identified from multiple diagnostic criteria with supporting field data",
            "AGGRESSIVE": "Drive mechanism assumed without sufficient pressure or production history",
            "DISCLOSURE": "Early field life may exhibit transitional behavior; mechanism may evolve",
            "HIGH_RISK": "Designing development plan based on incorrect drive assumption (e.g., assuming strong water drive when none exists)"
        },
        controlling_precedent="Drive mechanism determines recovery factor and optimal development strategy",
        issue_category=IssueCategory.DRIVE_MECHANISM,
        epistemic_guardrails=[
            "Drive mechanism may change over field life (e.g., transition from solution gas to waterflood)",
            "Compartmentalized reservoirs may exhibit different drives in different fault blocks"
        ]
    ),

    DoctrineBlock(
        topic="Recovery Factor Estimation by Drive Type",
        keywords=["recovery factor", "RF", "ultimate recovery", "EUR", "solution gas", "water drive", "gas cap"],
        conclusion_template=[
            "Estimate ultimate recovery factor based on identified drive mechanism and reservoir quality.",
            "Solution gas: 5-30% (typical 15-20%); Water drive: 35-75%; Gas cap: 20-40%.",
            "Adjust for reservoir quality, heterogeneity, and operational constraints."
        ],
        reasoning_framework="""
Recovery factor ranges by drive mechanism:

Solution gas drive (depletion):
- Range: 5-30% OOIP
- Typical: 15-20% OOIP
- Low end: high viscosity, low permeability, poor rock quality
- High end: light oil, high permeability, homogeneous
- Rapid pressure decline limits recovery
- Gas evolution creates two-phase flow inefficiency

Gas cap drive:
- Range: 20-40% OOIP
- Typical: 25-35% OOIP
- Requires gravity segregation (low rate, high vertical permeability)
- Gas cap expansion displaces oil downward
- Better than solution gas, worse than water drive
- Optimal with controlled gas cap blowdown

Water drive (strong aquifer):
- Range: 35-75% OOIP
- Typical: 50-60% OOIP
- Maintains pressure above bubble point
- Efficient displacement mechanism
- Early water breakthrough reduces recovery
- Edge water better than bottom water

Combination drive:
- Weighted average based on drive indices
- RF = SDI*RF_sg + DDI*RF_gc + WDI*RF_wd
- Example: 0.7*20% + 0.2*30% + 0.1*50% = 25%

Modifying factors:
- Oil viscosity (higher μ → lower RF)
- Permeability heterogeneity (higher Vk → lower RF)
- Wettability (oil-wet reduces RF)
- Dip angle (steeper improves gravity segregation)
- Reservoir thickness (thicker better for gas cap)

Permian Basin typical:
- Solution gas drive: 15-25% (weak aquifers)
- Pressure maintenance via waterflood: 30-50%
- CO2 EOR incremental: 10-20% additional
        """,
        key_factors=[
            "Primary drive mechanism (solution gas, gas cap, water)",
            "Oil properties (viscosity, API gravity)",
            "Rock properties (permeability, heterogeneity)",
            "Wettability characteristics",
            "Structural dip and geometry",
            "Reservoir continuity and compartmentalization",
            "Operational constraints (rate limits, water handling)",
            "Economic cutoff (abandonment conditions)"
        ],
        primary_authority=[
            "Arps, J.J. (1967) - 'A Statistical Study of Recovery Efficiency'",
            "Guthrie & Greenberger (1965) - 'The Use of Multiple Correlation Analyses for Estimating Recovery Factors'",
            "SPE PRMS (2018) - Petroleum Resources Management System",
            "Permian Basin statistics (various SPE papers)"
        ],
        burden_holder="Reservoir engineer estimating reserves and ultimate recovery",
        adversary_position="Recovery factor overstated; actual performance will fall short of estimate",
        counter_arguments=[
            "RF based on analog field performance with similar drive and reservoir quality",
            "Conservative assumptions applied for heterogeneity and operational limits",
            "Material balance and simulation support RF estimate",
            "Economic limit defined based on actual operating costs",
            "Probabilistic range (P10/P50/P90) captures uncertainty"
        ],
        resolution_strategy="Use analog field database, material balance, and simulation to triangulate recovery factor with probabilistic uncertainty range",
        entity_scope="Applies to all oil reservoirs; accuracy improves with field performance history",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "RF based on producing analog fields, material balance, and reservoir simulation",
            "AGGRESSIVE": "RF at high end of range without supporting analog data",
            "DISCLOSURE": "RF is probabilistic; actual performance depends on operational execution",
            "HIGH_RISK": "Basing investment decision on unsubstantiated high RF estimate"
        },
        controlling_precedent="Recovery factor is fundamental to reserves estimation and field economics",
        issue_category=IssueCategory.RECOVERY_FACTOR,
        epistemic_guardrails=[
            "RF evolves with field development (e.g., waterflood increases RF)",
            "Ultimate RF not known until field abandonment"
        ]
    ),

    DoctrineBlock(
        topic="Waterflood Design - Pattern Selection",
        keywords=["waterflood", "injection pattern", "five spot", "seven spot", "line drive", "pattern efficiency"],
        conclusion_template=[
            "Select waterflood pattern based on reservoir geometry, well spacing, and fluid mobility.",
            "Five-spot most common; seven-spot for better sweep; line drive for directional permeability.",
            "Pattern efficiency depends on mobility ratio and areal heterogeneity."
        ],
        reasoning_framework="""
Waterflood pattern types:

1. Five-spot (1 injector : 4 producers):
   - Most common pattern
   - Isotropic reservoir
   - Areal sweep efficiency: 72% at breakthrough (M=1)
   - Well spacing: 40-80 acres typical
   - Inverted five-spot: 4 injectors : 1 producer (better sweep)

2. Seven-spot (1 injector : 6 producers):
   - Higher sweep efficiency: 78% at BT (M=1)
   - More complex well arrangement
   - Requires regular hexagonal geometry
   - Used for thick, homogeneous reservoirs

3. Line drive (row of injectors : row of producers):
   - Directional permeability (kx >> ky)
   - Elongated reservoir geometry
   - Edge water drive simulation
   - Easier pressure maintenance
   - Areal sweep: 60-65% at BT (M=1)

4. Direct line drive (alternating injector-producer):
   - Tight spacing (10-20 acres)
   - Low permeability reservoirs
   - High injection pressure
   - Better vertical sweep

5. Peripheral/crestal injection:
   - Injectors at flank or crest
   - Utilize gravity segregation
   - Maintain reservoir pressure
   - Slower response time

Pattern efficiency factors:
- Mobility ratio M = (krw/μw) / (kro/μo)
- M < 1: favorable (water less mobile)
- M > 1: unfavorable (viscous fingering)
- Areal sweep EA = f(M, well spacing, heterogeneity)
- Vertical sweep EV = f(Vk, gravity, rate)
- Volumetric sweep EV = EA * EV * ED (displacement efficiency)

Permian Basin waterflood design:
- 40-acre five-spot typical (1/4 mile spacing)
- Infill to 20-acre in high quality rock
- Line drive for fractured carbonates with directional trends
- CO2 WAG using existing waterflood patterns
        """,
        key_factors=[
            "Reservoir geometry (isotropic vs directional permeability)",
            "Well spacing and density",
            "Mobility ratio (oil vs water)",
            "Permeability heterogeneity (Vk, layering)",
            "Formation dip and structural features",
            "Existing well locations (greenfield vs brownfield)",
            "Injection water availability and quality",
            "Economic optimization (wells vs recovery)"
        ],
        primary_authority=[
            "Craig, F.F. (1971) - The Reservoir Engineering Aspects of Waterflooding",
            "Willhite, G.P. (1986) - Waterflooding (SPE Textbook Series Vol. 3)",
            "Dyes, Caudle & Erickson (1954) - 'Oil Production After Breakthrough'",
            "Lake, L.W. (1989) - Enhanced Oil Recovery"
        ],
        burden_holder="Reservoir engineer designing waterflood project",
        adversary_position="Pattern selection suboptimal; poor sweep efficiency leads to low recovery and high water cut",
        counter_arguments=[
            "Pattern selected based on reservoir simulation of multiple scenarios",
            "Mobility ratio and heterogeneity quantified from core and log data",
            "Directional permeability confirmed by pressure transient tests",
            "Economic optimization of pattern spacing vs wells required",
            "Analogous field waterflood performance validates design"
        ],
        resolution_strategy="Use reservoir simulation to test multiple pattern configurations and select optimal based on NPV and recovery",
        entity_scope="Applies to all waterflood projects; pattern selection critical to project economics",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Pattern selected via simulation with calibrated reservoir model and validated assumptions",
            "AGGRESSIVE": "Pattern selection based solely on rule-of-thumb without simulation",
            "DISCLOSURE": "Actual sweep efficiency depends on reservoir heterogeneity not fully characterized",
            "HIGH_RISK": "Using unfavorable pattern (e.g., five-spot in highly directional reservoir)"
        },
        controlling_precedent="Waterflood pattern determines sweep efficiency and ultimate recovery",
        issue_category=IssueCategory.WATERFLOOD,
        epistemic_guardrails=[
            "Pattern performance varies by layer due to vertical heterogeneity",
            "Actual well locations constrained by surface access and existing infrastructure"
        ]
    ),

    DoctrineBlock(
        topic="Waterflood Optimization - Injection Rate and Fractional Flow",
        keywords=["injection rate", "fractional flow", "buckley leverett", "water cut", "voidage replacement"],
        conclusion_template=[
            "Optimize injection rate for voidage replacement and pressure maintenance without exceeding fracture pressure.",
            "Use Buckley-Leverett fractional flow theory to predict water breakthrough and ultimate recovery.",
            "Balance injection rate vs water handling capacity and operating costs."
        ],
        reasoning_framework="""
Injection rate determination:

Voidage replacement ratio (VRR):
VRR = (Water injected BPD) / (Oil + Water + Gas produced, reservoir BPD)
- VRR = 1.0: maintain reservoir pressure
- VRR > 1.0: pressure increase (fracture risk)
- VRR < 1.0: pressure decline

Fracture pressure constraint:
- Pmax_inj < Pfrac = σmin + α*Pp
- σmin = minimum horizontal stress (from LOT, minifrac)
- Typical Permian: 0.7-0.8 psi/ft gradient
- Maintain injection pressure 200-500 psi below fracture

Injectivity:
II = q_inj / (Pinj - Pavg)
- II declines over time (plugging, scaling, fines migration)
- Water quality critical (filtration, compatibility)
- Stimulation required if II drops significantly

Buckley-Leverett fractional flow:
fw = 1 / (1 + (kro/krw)*(μw/μo))
- Saturation profile advances as shock front
- Water breakthrough time: tBT = PV / (fw'*A*φ*h*Sw)
- Ultimate recovery from fractional flow curve
- Assumes 1D displacement, no capillary/gravity

Welge graphical method:
- Tangent to fw curve gives average Sw behind front
- Water-oil ratio WOR = fw / (1 - fw)
- Cumulative oil recovery vs water injected

Vertical sweep efficiency:
- High rate: poor vertical sweep (viscous dominated)
- Low rate: better sweep (gravity segregation)
- Optimal rate: balance recovery vs project life

Permian waterflood operations:
- Target VRR 1.0-1.2
- Injection rate: 500-2000 BPD per well
- Injection pressure: 1500-3000 psi (depth dependent)
- Water treatment essential (bacterial control, oxygen removal)
        """,
        key_factors=[
            "Voidage replacement ratio (pressure maintenance)",
            "Fracture pressure and injection pressure limit",
            "Injectivity and water quality",
            "Relative permeability curves (krw, kro)",
            "Oil/water viscosity ratio",
            "Reservoir heterogeneity (vertical sweep)",
            "Injection rate vs recovery tradeoff",
            "Water handling capacity and cost"
        ],
        primary_authority=[
            "Buckley, S.E. & Leverett, M.C. (1942) - 'Mechanism of Fluid Displacement in Sands'",
            "Welge, H.J. (1952) - 'A Simplified Method for Computing Oil Recovery'",
            "Craig, F.F. (1971) - Waterflooding",
            "Willhite, G.P. (1986) - Waterflooding SPE Textbook"
        ],
        burden_holder="Reservoir/production engineer optimizing waterflood operations",
        adversary_position="Injection rate too high (fracturing reservoir) or too low (insufficient pressure support)",
        counter_arguments=[
            "Injection pressure monitored continuously; fracture pressure not exceeded",
            "VRR tracking confirms adequate voidage replacement",
            "Fractional flow analysis predicts water breakthrough timing",
            "Rate optimization via simulation balances recovery and project economics",
            "Analogous field performance validates injection strategy"
        ],
        resolution_strategy="Monitor injection pressure, VRR, and individual well injectivity; adjust rates to maintain pressure without fracturing",
        entity_scope="Applies to all waterflood operations; critical to project success",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Injection strategy based on fracture pressure testing, simulation, and field monitoring",
            "AGGRESSIVE": "Injecting near fracture pressure without adequate monitoring",
            "DISCLOSURE": "Formation damage may reduce injectivity over time; water treatment essential",
            "HIGH_RISK": "Fracturing reservoir through over-injection; short-circuiting and poor sweep"
        },
        controlling_precedent="Injection rate optimization balances pressure maintenance, sweep efficiency, and operational constraints",
        issue_category=IssueCategory.WATERFLOOD,
        epistemic_guardrails=[
            "Buckley-Leverett assumes 1D displacement; actual 3D reservoir has complex flow",
            "Injectivity declines over time; periodic stimulation required"
        ]
    ),

    DoctrineBlock(
        topic="CO2 EOR - Miscible vs Immiscible Displacement",
        keywords=["CO2 EOR", "miscible displacement", "MMP", "minimum miscibility pressure", "immiscible", "CO2 flooding"],
        conclusion_template=[
            "Determine if reservoir pressure exceeds minimum miscibility pressure (MMP) for miscible CO2 flood.",
            "Miscible displacement (P > MMP): 10-20% incremental recovery; Immiscible (P < MMP): 5-10%.",
            "MMP depends on oil composition and temperature; measured by slim tube or correlations."
        ],
        reasoning_framework="""
CO2 EOR mechanisms:

Miscible displacement (P > MMP):
- Multi-contact miscibility develops
- No interfacial tension between CO2 and oil
- Displacement efficiency approaches 100% in swept volume
- Incremental recovery: 10-20% OOIP (tertiary)
- Requires reservoir pressure > MMP + 200 psi margin

Immiscible displacement (P < MMP):
- Interfacial tension exists
- Oil swelling and viscosity reduction
- Incremental recovery: 5-10% OOIP
- Lower CO2 utilization efficiency
- Still economically viable in some cases

Minimum Miscibility Pressure (MMP):

Experimental determination:
1. Slim tube test (ASTM standard)
   - 40-ft coiled tube, reservoir temperature
   - CO2 injection at varying pressure
   - MMP = pressure where recovery >90% or breaks trend

2. Rising bubble apparatus
   - Visual observation of miscibility
   - Faster than slim tube

Correlations (when no lab data):
- Yellig & Metcalfe (1980): MMP = f(T, MW_C5+, volatiles)
- Cronquist (1978): MMP ≈ 1100 + 21*T(°F) - approximate
- Alston et al. (1985): MMP = f(composition, temperature)

Typical MMP ranges:
- Light oil (35-45 API): 1200-1800 psi
- Medium oil (25-35 API): 1500-2500 psi
- Heavy oil (15-25 API): 2000-3500 psi
- Temperature increases MMP (20-30 psi/°F)

CO2 utilization:
- Miscible: 5-15 Mcf CO2 per incremental bbl oil
- Immiscible: 15-30 Mcf CO2 per incremental bbl oil
- Recycle CO2 to reduce net purchase

Permian Basin CO2 EOR:
- Most projects miscible (reservoir depths 5000-9000 ft)
- MMP typically 1300-2200 psi for Permian light oils
- Pressure maintenance via WAG essential
- Natural CO2 from McElmo Dome, Bravo Dome pipelines
        """,
        key_factors=[
            "Reservoir pressure vs MMP (miscibility condition)",
            "Oil composition (API gravity, C5+ molecular weight)",
            "Reservoir temperature",
            "CO2 availability and cost",
            "Pressure maintenance strategy",
            "Reservoir heterogeneity (CO2 channeling risk)",
            "Corrosion and H2S management",
            "CO2 recycle infrastructure"
        ],
        primary_authority=[
            "Yellig, W.F. & Metcalfe, R.S. (1980) - 'Determination of CO2 MMP'",
            "Holm, L.W. & Josendal, V.A. (1974) - 'Mechanisms of Oil Displacement by CO2'",
            "Stalkup, F.I. (1983) - 'Miscible Displacement' SPE Monograph",
            "Klins, M.A. (1984) - 'Carbon Dioxide Flooding'"
        ],
        burden_holder="Reservoir engineer designing CO2 EOR project",
        adversary_position="Reservoir pressure insufficient for miscibility; incremental recovery overstated",
        counter_arguments=[
            "MMP measured via slim tube test at reservoir temperature",
            "Reservoir pressure maintained above MMP via WAG and pressure monitoring",
            "Oil composition analysis confirms MMP estimate",
            "Analogous CO2 flood performance validates recovery estimate",
            "Simulation with tuned EOS predicts miscible displacement"
        ],
        resolution_strategy="Measure MMP via slim tube, maintain reservoir pressure above MMP through injection strategy, validate with simulation",
        entity_scope="Applies to all CO2 EOR projects; miscibility determines project economics",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "MMP measured experimentally, reservoir pressure maintained above MMP, simulation validates recovery",
            "AGGRESSIVE": "Assuming miscibility without MMP measurement or adequate pressure maintenance",
            "DISCLOSURE": "Reservoir heterogeneity may cause early CO2 breakthrough and reduced sweep",
            "HIGH_RISK": "Designing project assuming miscible recovery when pressure < MMP"
        },
        controlling_precedent="Miscibility is binary condition; MMP must be exceeded for miscible displacement",
        issue_category=IssueCategory.EOR,
        epistemic_guardrails=[
            "MMP increases with temperature and decreasing oil gravity",
            "Pressure decline during production may fall below MMP over time"
        ]
    ),

    DoctrineBlock(
        topic="WAG (Water Alternating Gas) Process Design",
        keywords=["WAG", "water alternating gas", "WAG ratio", "cycle frequency", "mobility control", "CO2 utilization"],
        conclusion_template=[
            "Design WAG process to improve sweep efficiency and reduce gas channeling in CO2 or hydrocarbon gas floods.",
            "Typical WAG ratio: 1:1 to 2:1 water:gas on HCPV basis; cycle frequency: 1-6 months.",
            "WAG improves recovery by 5-10% over continuous gas injection in heterogeneous reservoirs."
        ],
        reasoning_framework="""
WAG process objectives:
1. Mobility control (reduce gas channeling)
2. Improve sweep efficiency (vertical and areal)
3. Reduce gas utilization (Mcf/bbl oil)
4. Maintain miscibility pressure

WAG ratio (water:gas on HCPV basis):
- 1:1 most common
- 2:1 for highly heterogeneous reservoirs
- 1:2 for low permeability (maintain injectivity)
- Higher water ratio → better sweep, lower gas utilization
- Lower water ratio → faster oil response, higher gas cost

Cycle frequency:
- Slug size: 0.05-0.5 HCPV per cycle
- Cycle length: 1-6 months typical
- Shorter cycles: better mobility control
- Longer cycles: operational simplicity
- Tradeoff: mixing vs operational efficiency

WAG vs continuous gas injection:
- WAG improves recovery by 5-10% OOIP
- Reduces gas requirement by 20-40%
- Slows oil production rate (more cycles)
- Increases operational complexity
- Better for heterogeneous reservoirs

Hysteresis effects:
- Relative permeability hysteresis in WAG cycles
- Gas trapping during water injection
- Oil trapping during gas re-injection
- Requires hysteresis model in simulation

Three-phase flow:
- Complex relative permeability (kro, krw, krg)
- Stone's method or three-phase correlations
- Significant uncertainty in three-phase kr

Operational considerations:
- Single wellbore (inject both water and gas)
- Separate injection wells (water vs gas)
- Corrosion control (CO2 + water)
- Scale inhibition
- Well integrity (pressure cycling)

Permian CO2 WAG:
- 1:1 to 1.5:1 WAG ratio typical
- 3-6 month cycles
- Total injection: 30-50% HCPV CO2 + water
- Incremental recovery: 12-18% OOIP (tertiary)
        """,
        key_factors=[
            "WAG ratio (water:gas on HCPV basis)",
            "Cycle frequency and slug size",
            "Reservoir heterogeneity (Vk, Lorenz coefficient)",
            "Relative permeability hysteresis",
            "Three-phase flow behavior",
            "Gas channeling and gravity override risk",
            "Operational complexity and costs",
            "Corrosion and scale management"
        ],
        primary_authority=[
            "Christensen, J.R. et al. (2001) - 'Review of WAG Field Experience'",
            "Stalkup, F.I. (1983) - 'Miscible Displacement' SPE Monograph",
            "Lake, L.W. (1989) - Enhanced Oil Recovery",
            "Kulkarni, M.M. (2003) - 'Multiphase Mechanisms and Fluid Dynamics in Gas Injection EOR'"
        ],
        burden_holder="Reservoir engineer designing WAG injection strategy",
        adversary_position="WAG process suboptimal; gas channeling still occurs, recovery not improved vs continuous injection",
        counter_arguments=[
            "WAG ratio and cycle frequency optimized via reservoir simulation",
            "Analogous WAG field performance demonstrates incremental recovery",
            "Hysteresis and three-phase flow incorporated in simulation model",
            "Pilot test validates WAG design before full-field implementation",
            "Monitoring (tracers, 4D seismic) confirms improved sweep"
        ],
        resolution_strategy="Optimize WAG design through simulation with validated hysteresis model; conduct pilot test before full-field rollout",
        entity_scope="Applies to all gas injection EOR (CO2, hydrocarbon gas, N2); especially valuable in heterogeneous reservoirs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "WAG design based on simulation with hysteresis, validated by pilot test and analog field data",
            "AGGRESSIVE": "Assuming WAG benefit without simulation or pilot test",
            "DISCLOSURE": "Three-phase flow uncertainty; actual hysteresis may differ from model",
            "HIGH_RISK": "Implementing WAG without operational capability to handle water and gas co-injection"
        },
        controlling_precedent="WAG is proven technology for mobility control in gas floods",
        issue_category=IssueCategory.EOR,
        epistemic_guardrails=[
            "Relative permeability hysteresis poorly understood; lab measurements required",
            "Operational complexity increases costs; tradeoff vs incremental recovery"
        ]
    ),

    DoctrineBlock(
        topic="Reservoir Simulation - Black Oil vs Compositional Models",
        keywords=["reservoir simulation", "black oil model", "compositional model", "equation of state", "EOS", "fluid characterization"],
        conclusion_template=[
            "Select black oil model for simple depletion/waterflood; compositional model for gas injection EOR.",
            "Black oil: faster runtime, assumes constant PVT properties; Compositional: tracks component mass transfer.",
            "Compositional required for CO2 EOR, gas cycling, volatile oil, gas condensate."
        ],
        reasoning_framework="""
Black oil model:

Assumptions:
- Three pseudo-components: oil, gas, water
- PVT properties (Bo, Bg, Rs, μ) function of pressure only
- No mass transfer between oil and gas phases
- Valid for depletion, waterflood, immiscible gas injection

Governing equations:
- Oil conservation: ∂(φSoBo)/∂t + ∇(ρo*vo) = qo
- Gas conservation: ∂(φ(SgBg + Rs*SoBo))/∂t + ∇ = qg
- Water conservation: ∂(φSwBw)/∂t + ∇(ρw*vw) = qw
- Pressure equation (IMPES or fully implicit)

Advantages:
- Fast computation (minutes to hours)
- Mature, robust algorithms
- Standard industry tool
- Adequate for most conventional reservoirs

Limitations:
- Cannot model miscibility development
- Inaccurate for volatile oil (near-critical)
- Inaccurate for gas cycling, gas injection EOR
- Assumes equilibrium (no compositional gradients)

Compositional model:

Assumptions:
- Nc components (C1, C2, ..., C7+)
- Phase behavior via Equation of State (EOS)
- Mass transfer between phases (flash calculation)
- Tracks composition in oil and gas phases

Governing equations:
- Component i conservation: ∂(φΣ(Sj*ρj*xij))/∂t + ∇(Σ) = qi
- Flash calculation: minimize Gibbs free energy
- EOS: Peng-Robinson, Soave-Redlich-Kwong (SRK)

Required data:
- Component analysis (gas chromatography)
- PVT lab data (DL, CVD, swelling tests)
- EOS tuning (match lab data)
- Binary interaction parameters (BIP)

Applications:
- CO2 miscible flooding (MMP development)
- Hydrocarbon gas injection (vaporization)
- Gas condensate reservoirs (retrograde condensation)
- Volatile oil (Bo > 2.0 rb/stb)

Disadvantages:
- Slow computation (10-100x slower than black oil)
- Requires extensive PVT characterization
- Complex EOS tuning process
- More parameters = more uncertainty

Permian Basin simulation practice:
- Black oil for waterflood, solution gas drive
- Compositional for CO2 EOR (miscibility modeling)
- Dual porosity/permeability for fractured carbonates
- Fine grid near wells, coarse in aquifer
        """,
        key_factors=[
            "Recovery process (depletion/waterflood vs gas injection)",
            "Oil volatility (Bo, GOR, near-critical)",
            "Miscibility requirements (CO2 EOR)",
            "Available PVT data (component analysis)",
            "Computational resources (runtime constraints)",
            "Model complexity vs accuracy tradeoff",
            "Uncertainty quantification needs",
            "Regulatory/partner requirements"
        ],
        primary_authority=[
            "Aziz, K. & Settari, A. (1979) - Petroleum Reservoir Simulation",
            "Fanchi, J.R. (2006) - Principles of Applied Reservoir Simulation",
            "CMG, Eclipse, INTERSECT User Manuals",
            "Coats, K.H. (1980) - 'An Equation of State Compositional Model'"
        ],
        burden_holder="Reservoir engineer selecting appropriate simulation tool",
        adversary_position="Model type inappropriate for process being simulated; results unreliable",
        counter_arguments=[
            "Model selection based on physics of recovery process",
            "Black oil validated for non-miscible processes via field history match",
            "Compositional model tuned to lab PVT data for gas injection",
            "Sensitivity analysis quantifies uncertainty in model predictions",
            "Analogous reservoir simulation validates modeling approach"
        ],
        resolution_strategy="Use simplest model adequate for physics of problem; validate with field data; quantify uncertainty",
        entity_scope="Applies to all reservoir simulation; model selection fundamental to reliability",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Model type matches physics of process; tuned to lab and field data; uncertainty quantified",
            "AGGRESSIVE": "Using black oil model for CO2 miscible flood or compositional for simple waterflood",
            "DISCLOSURE": "All models are simplifications; grid resolution and relative permeability are significant uncertainties",
            "HIGH_RISK": "Basing investment decision on simulation with inappropriate model type"
        },
        controlling_precedent="Simulation model must capture essential physics of recovery process",
        issue_category=IssueCategory.SIMULATION,
        epistemic_guardrails=[
            "All simulation is approximation; validate against field performance",
            "Compositional models have higher uncertainty due to more parameters"
        ]
    ),

    DoctrineBlock(
        topic="History Matching Methodology",
        keywords=["history match", "calibration", "assisted history matching", "uncertainty quantification", "STOIIP"],
        conclusion_template=[
            "Calibrate simulation model to field production and pressure history before making predictions.",
            "Match pressure first, then rates, then saturations (if available).",
            "Use assisted history matching for systematic parameter adjustment and uncertainty quantification."
        ],
        reasoning_framework="""
History matching workflow:

1. Initialization:
   - STOIIP from volumetric (structure, φ, Sw)
   - Verify material balance OOIP agrees
   - Initialize pressures (depth-corrected)
   - Initialize saturations (Sw from logs, Sg from GOC)

2. Match sequence (hierarchical):
   a) Pressure history:
      - Weighted average reservoir pressure
      - Individual well pressures (BHP, THP)
      - Aquifer influx (if water drive)
      - Adjust: STOIIP, aquifer size/strength, transmissibility

   b) Production rates:
      - Oil, gas, water rates (historical controls)
      - GOR and WOR trends
      - Adjust: kh, skin, relative permeability, well PI

   c) Saturation distribution (if available):
      - Cased-hole logs, RST, pulsed neutron
      - Water saturation behind casing
      - Adjust: vertical permeability, capillary pressure

3. Parameter adjustment:
   - Modify uncertain parameters within reasonable ranges
   - Preserve geologic realism (honor structure, facies)
   - Avoid compensating errors (e.g., changing kv to match rate)

4. Quantify uncertainty:
   - Multiple realizations (P10, P50, P90)
   - Probabilistic forecast
   - Tornado chart of sensitive parameters

Assisted history matching:
- Automatic parameter optimization
- Gradient-based (Gauss-Newton, Levenberg-Marquardt)
- Ensemble-based (EnKF, ES-MDA)
- Reduces manual effort
- Quantifies parameter uncertainty

Match quality metrics:
- Pressure RMSE < 50 psi acceptable
- Rate match within ±10% typical
- GOR/WOR trends directionally correct
- No single mismatch > 20%

Common adjustments:
- STOIIP (±10% typical uncertainty)
- Permeability (kh, kv, kh/kv ratio)
- Aquifer parameters (size, influx constant)
- Relative permeability curves (endpoints, exponents)
- Well productivity (skin, completion efficiency)

Permian Basin history match challenges:
- Sparse pressure data (often only early DST)
- Commingled production (multiple zones)
- Waterflood pressure support (multiple patterns)
- Fractured carbonates (dual porosity/permeability)
        """,
        key_factors=[
            "Data quality (pressure, production, saturation)",
            "Parameter uncertainty ranges",
            "Number of realizations (uncertainty quantification)",
            "Geologic constraints (facies, structure)",
            "Match quality acceptance criteria",
            "Computational budget (runtime)",
            "Expertise in parameter adjustment",
            "Software capabilities (assisted matching)"
        ],
        primary_authority=[
            "Oliver, D.S. & Chen, Y. (2011) - 'Recent Progress on Reservoir History Matching'",
            "Tavassoli, Z. et al. (2004) - 'Errors in History Matching'",
            "Schulze-Riegert, R. et al. (2002) - 'Modern Techniques for History Matching'",
            "CMG CMOST, Schlumberger Mepo User Manuals"
        ],
        burden_holder="Reservoir engineer performing history match and forecasting",
        adversary_position="History match non-unique; model cannot predict future performance reliably",
        counter_arguments=[
            "Multiple parameters constrained by independent data (core, logs, tests)",
            "Match quality meets industry-standard criteria",
            "Sensitivity analysis identifies critical parameters",
            "Multiple realizations bracket uncertainty in forecast",
            "Geologic model honors structural and facies interpretations"
        ],
        resolution_strategy="Systematic hierarchical matching, constrain parameters to reasonable ranges, quantify uncertainty via multiple realizations",
        entity_scope="Essential for all simulation-based forecasts; match quality determines prediction reliability",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Systematic match process, parameters within reasonable ranges, uncertainty quantified",
            "AGGRESSIVE": "Over-tuning model to match sparse data; unrealistic parameter values",
            "DISCLOSURE": "History match non-unique; forecast uncertainty larger than match quality suggests",
            "HIGH_RISK": "Making investment decision based on unvalidated simulation"
        },
        controlling_precedent="History matching is calibration; prediction reliability depends on match quality and data richness",
        issue_category=IssueCategory.SIMULATION,
        epistemic_guardrails=[
            "Perfect match may indicate over-fitting; geologic realism must be preserved",
            "Forecast uncertainty always larger than historical uncertainty"
        ]
    ),

    DoctrineBlock(
        topic="OOIP/OGIP Estimation - Volumetric Method",
        keywords=["OOIP", "OGIP", "volumetric", "stock tank oil initially in place", "original gas in place", "reserves"],
        conclusion_template=[
            "Calculate OOIP/OGIP volumetrically from structure, porosity, and saturation data.",
            "OOIP = 7758 * A * h * φ * (1 - Sw) / Bo; OGIP = 43560 * A * h * φ * (1 - Sw) / Bg.",
            "Uncertainty ±20-50% depending on data quality; validate with material balance."
        ],
        reasoning_framework="""
Volumetric OOIP calculation:

OOIP (stb) = 7758 * A * h * φ * (1 - Sw) / Boi

Where:
- 7758 = conversion factor (acre-ft to bbl)
- A = area (acres)
- h = net pay thickness (ft)
- φ = average porosity (fraction)
- Sw = average water saturation (fraction)
- Boi = initial formation volume factor (rb/stb)

Volumetric OGIP calculation:

OGIP (scf) = 43560 * A * h * φ * (1 - Sw - Soi) / Bgi

Where:
- 43560 = conversion factor (acre-ft to ft³)
- Soi = oil saturation (if oil present)
- Bgi = initial gas formation volume factor (rcf/scf)

Alternative OGIP formula:
OGIP = A * h * φ * (1 - Sw) / (Bg * 5.615) (MMscf)

Parameter estimation:

Area (A):
- Map closure from seismic structure maps
- Down-to fluid contact (OWC, GOC)
- Planimeter or GIS calculation
- Uncertainty: ±10-30% (structure quality dependent)

Net pay thickness (h):
- Cutoffs: φ > 0.06, Sw < 0.5, Vsh < 0.4 (typical)
- Log-derived or core-calibrated
- Net-to-gross ratio
- Uncertainty: ±15-25%

Porosity (φ):
- Log-derived (density-neutron, sonic)
- Core-calibrated
- Arithmetic, geometric, or harmonic average
- Uncertainty: ±10-20%

Water saturation (Sw):
- Archie equation from resistivity logs
- Core-calibrated (Dean-Stark)
- Saturation-height model (J-function)
- Uncertainty: ±10-30% (highest uncertainty)

Formation volume factor (Bo, Bg):
- Lab-measured PVT or correlations
- Standing, Vasquez-Beggs for Bo
- Real gas law for Bg
- Uncertainty: ±5-10%

Total volumetric uncertainty:
- Low quality: ±40-50% (P10-P90 range)
- Medium quality: ±25-35%
- High quality: ±15-25%

Probabilistic OOIP:
- Monte Carlo simulation
- Probability distributions for A, h, φ, Sw
- P10/P50/P90 OOIP estimates

Validation:
- Compare volumetric vs material balance OOIP
- Agreement within 20% builds confidence
- Large discrepancy requires reconciliation
        """,
        key_factors=[
            "Structure map quality (seismic, well control)",
            "Fluid contact depth (OWC, GOC, FWL)",
            "Porosity measurement and averaging method",
            "Water saturation (Archie parameters, core calibration)",
            "Net pay cutoff criteria",
            "Formation volume factor (lab vs correlation)",
            "Reservoir heterogeneity (layering, facies)",
            "Probabilistic vs deterministic approach"
        ],
        primary_authority=[
            "SPE PRMS (2018) - Petroleum Resources Management System",
            "Crain, E.R. (2000) - Crain's Petrophysical Handbook",
            "Dake, L.P. (1978) - Fundamentals of Reservoir Engineering",
            "SPEE Guidelines on Reserves Definitions and Estimation"
        ],
        burden_holder="Reservoir engineer estimating in-place volumes for reserves booking",
        adversary_position="OOIP/OGIP overstated due to optimistic parameter assumptions",
        counter_arguments=[
            "Parameters derived from rigorous log and core analysis",
            "Probabilistic approach captures uncertainty range",
            "Volumetric OOIP validated by material balance estimate",
            "Conservative cutoffs applied for net pay identification",
            "Independent review by qualified reserves evaluator"
        ],
        resolution_strategy="Use probabilistic volumetric estimate, validate with material balance, apply conservative assumptions for reserves booking",
        entity_scope="Fundamental to all reserves estimation; accuracy depends on data quality",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Probabilistic volumetric estimate with rigorous petrophysics, validated by material balance",
            "AGGRESSIVE": "Deterministic estimate with optimistic assumptions and no validation",
            "DISCLOSURE": "OOIP/OGIP is uncertain; actual reserves depend on recovery factor",
            "HIGH_RISK": "Booking reserves based on unvalidated volumetric calculation"
        },
        controlling_precedent="Volumetric OOIP/OGIP is primary method for undeveloped reservoirs",
        issue_category=IssueCategory.OOIP_OGIP,
        epistemic_guardrails=[
            "Volumetric estimate is static; does not account for reservoir dynamics",
            "Water saturation has highest uncertainty; core calibration essential"
        ]
    ),

    DoctrineBlock(
        topic="PVT Properties - Bo Correlations (Standing, Vasquez-Beggs)",
        keywords=["Bo", "formation volume factor", "PVT", "Standing correlation", "Vasquez Beggs", "oil FVF"],
        conclusion_template=[
            "Estimate oil formation volume factor (Bo) from Standing or Vasquez-Beggs correlation when lab data unavailable.",
            "Bo increases with GOR, API, and temperature; decreases with pressure.",
            "Correlations accurate to ±5-10% for conventional oils; lab measurement preferred for critical applications."
        ],
        reasoning_framework="""
Oil formation volume factor (Bo):

Definition:
Bo = Volume of oil + dissolved gas at reservoir conditions / Volume of oil at stock tank conditions
Units: rb/stb (reservoir barrels per stock tank barrel)
Typical range: 1.05 - 2.5 rb/stb

Standing correlation (1947):

Bob = 0.9759 + 0.000120 * [Rs*(γg/γo)^0.5 + 1.25*T]^1.2

Where:
- Bob = Bo at bubble point (rb/stb)
- Rs = solution GOR (scf/stb)
- γg = gas specific gravity (air=1)
- γo = oil specific gravity = 141.5/(API+131.5)
- T = temperature (°F)

For P > Pb (undersaturated):
Bo = Bob * exp[co*(Pb - P)]
- co = oil compressibility (typical 5-20 × 10^-6 psi^-1)

Vasquez-Beggs correlation (1980):

Bob = 1 + C1*Rs + C2*(T-60)*(API/γgs) + C3*Rs*(T-60)*(API/γgs)

API ≤ 30:
C1 = 4.677e-4, C2 = 1.751e-5, C3 = -1.811e-8

API > 30:
C1 = 4.670e-4, C2 = 1.100e-5, C3 = 1.337e-9

γgs = γg * (1 + 5.912e-5*API*Tsep*log(Psep/114.7))
- Tsep, Psep = separator temperature (°F) and pressure (psia)

McCain correlation (1988):
- More complex, accounts for separator conditions
- Better for volatile oils

Correlation selection:
- Standing: simple, widely used, conservative
- Vasquez-Beggs: improved accuracy, accounts for separator conditions
- McCain: best for volatile oils
- Lab PVT: always preferred for critical decisions

Lab measurements:
- Differential liberation (DL) test
- Constant composition expansion (CCE)
- Separator test (flash to stock tank)
- Accuracy: ±1-2% (much better than correlations)

Permian Basin Bo characteristics:
- Light oils (35-45 API): Bo = 1.3-1.6 rb/stb
- Volatile oils (>50 API): Bo > 2.0 rb/stb
- Solution GOR typical: 500-1500 scf/stb
- Temperature: 120-200°F (depth dependent)
        """,
        key_factors=[
            "Solution GOR (Rs) - most sensitive parameter",
            "Oil API gravity",
            "Gas specific gravity",
            "Reservoir temperature",
            "Separator conditions (for Vasquez-Beggs)",
            "Oil compressibility (for undersaturated oil)",
            "Lab data availability",
            "Application criticality (reserves vs operational)"
        ],
        primary_authority=[
            "Standing, M.B. (1947) - 'A Pressure-Volume-Temperature Correlation for Mixtures of California Oils and Gases'",
            "Vasquez, M. & Beggs, H.D. (1980) - 'Correlations for Fluid Physical Property Prediction'",
            "McCain, W.D. (1990) - Properties of Petroleum Fluids",
            "Whitson, C.H. & Brule, M.R. (2000) - Phase Behavior SPE Monograph"
        ],
        burden_holder="Reservoir engineer estimating PVT properties for volumetrics or simulation",
        adversary_position="Bo correlation inaccurate; volumetric OOIP or simulation results unreliable",
        counter_arguments=[
            "Correlation selected appropriate to oil type and data availability",
            "Correlation predictions within ±5-10% of lab-measured values for analogous oils",
            "Sensitivity analysis shows OOIP insensitive to ±10% Bo variation",
            "Lab PVT obtained for final reserves booking and simulation",
            "Multiple correlations tested; conservative value selected"
        ],
        resolution_strategy="Use established correlation appropriate to oil characteristics; validate with lab data when available; quantify uncertainty",
        entity_scope="Applies to all black oil reservoir engineering; Bo essential for volumetrics and simulation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Bo from established correlation, validated by lab data or analogous reservoir",
            "AGGRESSIVE": "Using correlation outside calibrated range (heavy oil, near-critical)",
            "DISCLOSURE": "Correlations have ±5-10% uncertainty; lab measurement preferred for critical applications",
            "HIGH_RISK": "Using uncalibrated correlation for volatile oil or near-critical fluid"
        },
        controlling_precedent="Standing and Vasquez-Beggs correlations are industry-standard for Bo estimation",
        issue_category=IssueCategory.PVT,
        epistemic_guardrails=[
            "Correlations developed for specific crude oil types; extrapolation risky",
            "Separator conditions affect measured Bo; must match field operations"
        ]
    ),

    DoctrineBlock(
        topic="Gas Viscosity - Lee-Gonzalez Correlation",
        keywords=["gas viscosity", "μg", "Lee Gonzalez", "natural gas properties", "Z factor"],
        conclusion_template=[
            "Calculate gas viscosity from Lee-Gonzalez-Eakin correlation as function of pressure, temperature, and composition.",
            "μg increases with pressure and molecular weight; decreases with temperature.",
            "Typical range 0.01-0.03 cp for natural gas at reservoir conditions."
        ],
        reasoning_framework="""
Gas viscosity (μg):

Lee-Gonzalez-Eakin correlation (1966):

μg = K * exp(X * ρg^Y)

Where:
K = (9.4 + 0.02*M) * T^1.5 / (209 + 19*M + T)
X = 3.5 + 986/T + 0.01*M
Y = 2.4 - 0.2*X

- μg = gas viscosity (cp)
- T = temperature (°R = °F + 460)
- M = molecular weight (lb/lbmol)
- ρg = gas density (lb/ft³)

Gas density calculation:
ρg = (P*M) / (Z*R*T)
- P = pressure (psia)
- Z = compressibility factor (from correlations or EOS)
- R = gas constant = 10.732 psia-ft³/(lbmol-°R)

Molecular weight from gas gravity:
M = 28.97 * γg
- γg = gas specific gravity (air = 1)

Compressibility factor (Z):
- Standing-Katz chart (graphical)
- Dranchuk-Abou-Kassem correlation (1975)
- Beggs-Brill correlation (1973)
- Peng-Robinson or SRK EOS (compositional)

Viscosity behavior:
- Increases with pressure (density effect)
- Decreases with temperature (kinetic energy)
- Increases with molecular weight (heavier components)
- Typical range: 0.01-0.03 cp at reservoir conditions

Alternative correlations:
- Carr-Kobayashi-Burrows (1954)
- Lohrenz-Bray-Clark (LBC) for high pressure
- Dean-Stiel for sour gas (H2S, CO2)

Lab measurement:
- Rolling ball viscometer
- Electromagnetic viscometer
- Accuracy ±2-5%

Application in reservoir engineering:
- Gas flow rate calculation (Darcy's law)
- Material balance (gas expansion)
- IPR curves (gas well deliverability)
- Simulation input (compositional or black oil)

Permian gas typical properties:
- γg = 0.65-0.75 (lean gas)
- T = 120-200°F
- P = 1000-5000 psia
- μg = 0.018-0.025 cp
        """,
        key_factors=[
            "Gas specific gravity (or composition)",
            "Reservoir pressure",
            "Reservoir temperature",
            "Compressibility factor (Z)",
            "Presence of non-hydrocarbon components (CO2, N2, H2S)",
            "Correlation selection (standard vs sour gas)",
            "Lab data availability",
            "Application sensitivity to viscosity"
        ],
        primary_authority=[
            "Lee, A.L., Gonzalez, M.H., & Eakin, B.E. (1966) - 'The Viscosity of Natural Gases'",
            "McCain, W.D. (1990) - Properties of Petroleum Fluids",
            "Whitson & Brule (2000) - Phase Behavior SPE Monograph",
            "Standing, M.B. & Katz, D.L. (1942) - 'Density of Natural Gases'"
        ],
        burden_holder="Reservoir/production engineer estimating gas properties for well performance",
        adversary_position="Gas viscosity estimate inaccurate; well deliverability or reserves calculations unreliable",
        counter_arguments=[
            "Lee-Gonzalez correlation validated for wide range of natural gases",
            "Composition-based calculation for critical applications",
            "Lab-measured viscosity for sour gas or high-pressure reservoirs",
            "Sensitivity analysis shows results insensitive to ±10% viscosity variation",
            "Z-factor from established correlation or EOS"
        ],
        resolution_strategy="Use Lee-Gonzalez for standard natural gas; composition-based methods for sour gas or critical applications",
        entity_scope="Applies to all gas reservoirs and gas-phase calculations; essential for flow calculations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Lee-Gonzalez correlation for lean gas, composition-based for sour gas, lab data when available",
            "AGGRESSIVE": "Using correlation for high-pressure (>10,000 psi) or highly sour gas without validation",
            "DISCLOSURE": "Correlations accurate ±5-10%; composition and non-HC components affect accuracy",
            "HIGH_RISK": "Ignoring viscosity in gas well deliverability or reserves estimation"
        },
        controlling_precedent="Lee-Gonzalez is industry-standard correlation for natural gas viscosity",
        issue_category=IssueCategory.PVT,
        epistemic_guardrails=[
            "Viscosity increases non-linearly with pressure due to density increase",
            "Sour gas (H2S, CO2) requires composition-specific correlations"
        ]
    ),

    DoctrineBlock(
        topic="Relative Permeability and Capillary Pressure",
        keywords=["relative permeability", "kr", "kro", "krw", "krg", "capillary pressure", "Pc", "Corey exponent"],
        conclusion_template=[
            "Characterize two-phase and three-phase relative permeability from core measurements or empirical correlations.",
            "Relative permeability controls fluid mobility and displacement efficiency.",
            "Capillary pressure affects fluid distribution, particularly in low-permeability or thin reservoirs."
        ],
        reasoning_framework="""
Relative permeability concepts:

Definition:
kr = effective permeability to phase / absolute permeability
- kro = oil relative permeability
- krw = water relative permeability
- krg = gas relative permeability

Two-phase kr (oil-water):
- Drainage: water displacing oil (initial saturation)
- Imbibition: oil displacing water (recovery process)
- Hysteresis: drainage and imbibition curves differ

Corey correlation (empirical):
kro = kro_max * ((So - Sor) / (1 - Swc - Sor))^No
krw = krw_max * ((Sw - Swc) / (1 - Swc - Sor))^Nw

- Swc = connate water saturation
- Sor = residual oil saturation
- No, Nw = Corey exponents (typically 2-4)
- kro_max, krw_max = endpoint relative permeabilities

Critical parameters:
- Swc: immobile water (typical 0.15-0.35)
- Sor: trapped oil after waterflood (typical 0.15-0.35)
- Crossover point: Sw where kro = krw
- kro at Swc: endpoint (typical 0.6-1.0)
- krw at Sor: endpoint (typical 0.1-0.5)

Three-phase kr (oil-water-gas):
- Stone's Model I: kro function of krw and krg
- Stone's Model II: improved, widely used
- Empirical three-phase correlations
- Significant uncertainty vs two-phase

Capillary pressure (Pc):

Definition:
Pc = Pnw - Pw (pressure difference across interface)
- Pnw = non-wetting phase pressure
- Pw = wetting phase pressure

Leverett J-function (scaling):
J(Sw) = (Pc / σ) * sqrt(k / φ)
- σ = interfacial tension
- Normalizes Pc for different k and φ

Capillary pressure effects:
- Fluid distribution vs height above FWL
- Transition zone thickness
- Affects material balance (pressure averaging)
- Critical in low-k reservoirs (tight gas, shale)

Laboratory measurement:
- Steady-state method (long duration, accurate)
- Unsteady-state (short duration, Penn State method)
- Centrifuge method (capillary pressure)
- SCAL (special core analysis)

Wettability effects:
- Water-wet: water preferentially wets rock
- Oil-wet: oil preferentially wets rock
- Mixed-wet: spatially variable
- Affects kr curves and Sor significantly

Permian Basin kr characteristics:
- Water-wet to mixed-wet sandstones
- Oil-wet carbonates common
- Sor waterflood: 0.25-0.35 (sandstone), 0.20-0.30 (carbonate)
- CO2 EOR reduces Sor to 0.05-0.15
        """,
        key_factors=[
            "Core measurement data availability",
            "Wettability (water-wet vs oil-wet)",
            "Saturation endpoints (Swc, Sor, Sgr)",
            "Corey exponents or measured kr curves",
            "Two-phase vs three-phase flow",
            "Hysteresis effects (drainage vs imbibition)",
            "Capillary pressure (Pc) for low-k reservoirs",
            "Uncertainty quantification (multiple kr sets)"
        ],
        primary_authority=[
            "Corey, A.T. (1954) - 'The Interrelation Between Gas and Oil Relative Permeabilities'",
            "Stone, H.L. (1970) - 'Probability Model for Estimating Three-Phase Relative Permeability'",
            "Honarpour, M. et al. (1986) - 'Relative Permeability of Petroleum Reservoirs'",
            "Anderson, W.G. (1987) - 'Wettability Literature Survey' (6-part series)"
        ],
        burden_holder="Reservoir engineer characterizing fluid flow for simulation or analytical models",
        adversary_position="Relative permeability curves inappropriate; simulation predictions unreliable",
        counter_arguments=[
            "Kr curves measured on representative core samples",
            "Wettability characterized via contact angle and Amott tests",
            "Multiple kr sets tested in simulation (uncertainty quantification)",
            "History match validates kr assumptions",
            "Analogous reservoir kr data supports curves used"
        ],
        resolution_strategy="Measure kr on core samples when available; use correlations with uncertainty range; validate via history match",
        entity_scope="Essential for all multiphase flow calculations; highest uncertainty in reservoir simulation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Kr from core measurements, wettability characterized, uncertainty quantified",
            "AGGRESSIVE": "Using generic kr curves without core data or wettability consideration",
            "DISCLOSURE": "Kr is highly uncertain; 3-phase kr especially poorly constrained",
            "HIGH_RISK": "Basing waterflood or EOR design on uncalibrated kr assumptions"
        },
        controlling_precedent="Relative permeability controls displacement efficiency; most uncertain parameter in simulation",
        issue_category=IssueCategory.RELATIVE_PERM,
        epistemic_guardrails=[
            "Three-phase kr has large uncertainty; lab measurements difficult",
            "Wettability can change during production (e.g., asphaltene deposition)"
        ]
    ),

    DoctrineBlock(
        topic="Reservoir Heterogeneity - Dykstra-Parsons Coefficient",
        keywords=["heterogeneity", "Dykstra Parsons", "Vk", "permeability variation", "Lorenz coefficient", "layering"],
        conclusion_template=[
            "Quantify vertical permeability heterogeneity via Dykstra-Parsons coefficient (Vk) or Lorenz coefficient.",
            "Higher heterogeneity reduces waterflood and gas flood sweep efficiency.",
            "Vk > 0.7 indicates highly heterogeneous reservoir; Vk < 0.5 relatively homogeneous."
        ],
        reasoning_framework="""
Dykstra-Parsons permeability variation (Vk):

Definition:
Vk = (k50 - k84.1) / k50

Where:
- k50 = median permeability (50th percentile)
- k84.1 = permeability at 84.1 percentile (1 std dev)
- Derived from log-normal permeability distribution

Calculation procedure:
1. Arrange permeability data in descending order
2. Assign percentile to each value
3. Plot on log-probability paper
4. Read k50 and k84.1 from plot
5. Calculate Vk

Interpretation:
- Vk = 0: perfectly homogeneous (all k identical)
- Vk < 0.5: relatively homogeneous
- Vk = 0.5-0.7: moderate heterogeneity
- Vk > 0.7: highly heterogeneous
- Vk approaching 1.0: extreme heterogeneity

Impact on sweep efficiency:
- Higher Vk → lower areal and vertical sweep
- Water/gas channels through high-k layers
- Low-k layers bypassed
- Reduces waterflood recovery by 10-30% (Vk > 0.7)

Lorenz coefficient:

Alternative heterogeneity measure:
Lc = 2 * ∫[F(φ) - φ] dφ from 0 to 1

Where F(φ) = cumulative flow capacity vs storage capacity
- Lc = 0: perfect homogeneity
- Lc = 1: extreme heterogeneity
- Lorenz curve plots F vs φ

Relationship to recovery:
- Vk affects vertical sweep efficiency
- Lorenz coefficient affects flow capacity distribution
- Both correlate with reduced recovery

Strategies to mitigate heterogeneity:
1. Pattern infill (reduce well spacing)
2. Horizontal wells (contact more layers)
3. Profile modification (polymers, gels)
4. Selective completion (isolate high-k layers)
5. Reduced injection rate (improve vertical sweep)

Permian Basin heterogeneity:
- Fluvial sandstones: Vk = 0.6-0.8 (moderate-high)
- Eolian sandstones: Vk = 0.4-0.6 (low-moderate)
- Carbonates: Vk = 0.7-0.9 (high, fractures + vugs)
- Requires detailed reservoir characterization
        """,
        key_factors=[
            "Permeability data quantity and quality",
            "Log-normal distribution validity",
            "Vertical vs areal heterogeneity",
            "Impact on sweep efficiency",
            "Mitigation strategy selection",
            "Reservoir type (sandstone, carbonate, shale)",
            "Data source (core, logs, well tests)",
            "Scale of measurement (core vs reservoir)"
        ],
        primary_authority=[
            "Dykstra, H. & Parsons, R.L. (1950) - 'The Prediction of Oil Recovery by Waterflooding'",
            "Warren, J.E. & Cosgrove, J.J. (1964) - 'Prediction of Waterflood Behavior in a Stratified System'",
            "Lake, L.W. (1989) - Enhanced Oil Recovery",
            "Schmalz, J.P. & Rahme, H.D. (1950) - 'The Variation of Waterflood Performance With Variation in Permeability Profile'"
        ],
        burden_holder="Reservoir engineer characterizing heterogeneity for waterflood/EOR design",
        adversary_position="Heterogeneity underestimated; actual sweep efficiency much lower than predicted",
        counter_arguments=[
            "Vk calculated from extensive core and log permeability data",
            "Geostatistical model captures permeability distribution",
            "Waterflood simulation includes layered heterogeneity",
            "Analogous field performance validates Vk estimate",
            "Mitigation strategies incorporated in development plan"
        ],
        resolution_strategy="Quantify heterogeneity from core/log data, incorporate in simulation, design mitigation strategies",
        entity_scope="Applies to all reservoirs; critical for waterflood and gas injection projects",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Vk from extensive data, incorporated in layered simulation model, mitigation planned",
            "AGGRESSIVE": "Ignoring heterogeneity or assuming homogeneous reservoir without data",
            "DISCLOSURE": "Core-scale heterogeneity may not represent reservoir-scale; upscaling uncertainty",
            "HIGH_RISK": "Designing waterflood assuming homogeneous reservoir when Vk > 0.7"
        },
        controlling_precedent="Dykstra-Parsons coefficient is standard measure of vertical heterogeneity",
        issue_category=IssueCategory.HETEROGENEITY,
        epistemic_guardrails=[
            "Core permeability may not represent reservoir permeability (scale effect)",
            "Fractures and vugs create non-log-normal distributions (carbonates)"
        ]
    ),

    DoctrineBlock(
        topic="Field Development Planning - Infill Drilling Economics",
        keywords=["field development", "infill drilling", "well spacing", "drainage area", "EUR", "NPV"],
        conclusion_template=[
            "Optimize well spacing via economic analysis balancing incremental recovery vs drilling costs.",
            "Tighter spacing increases total recovery but reduces per-well EUR.",
            "Optimal spacing: maximize NPV considering commodity prices, costs, and discount rate."
        ],
        reasoning_framework="""
Field development optimization:

Well spacing economics:

Typical progression:
1. Primary development: 160-acre spacing (1 well per section)
2. Secondary development: 40-80 acre (infill to 4-8 wells)
3. Tertiary development: 10-20 acre (dense spacing for EOR)

Recovery vs spacing:
- Wider spacing: higher per-well EUR, lower field recovery
- Tighter spacing: lower per-well EUR, higher field recovery
- Diminishing returns as spacing decreases

Example (waterflood):
- 160-acre: 150 Mbbl/well, 40% field recovery
- 40-acre: 80 Mbbl/well, 55% field recovery (4x wells)
- 10-acre: 30 Mbbl/well, 65% field recovery (16x wells)

Economic analysis:

NPV = Σ [(Revenue - OpEx - CapEx) / (1+r)^t]

Where:
- Revenue = oil/gas production × prices
- OpEx = operating costs (LOE, water handling, chemicals)
- CapEx = drilling, completion, facilities
- r = discount rate (typically 10%)
- t = time (years)

Breakeven analysis:
- Min well EUR for economic viability
- Depends on: oil price, well cost, LOE, discount rate
- Example: $60/bbl oil, $2.5MM well, $15/bbl LOE → ~40 Mbbl EUR required

Infill drilling workflow:
1. Identify bypassed oil (simulation, saturation logs)
2. Estimate incremental EUR per infill well
3. Calculate NPV vs drilling cost
4. Prioritize high-NPV locations
5. Execute phased development (pilot first)

Permian Basin infill economics:
- Primary 640-1280 acre spacing (1-2 wells per section)
- Waterflood infill to 40 acre typical
- CO2 EOR infill to 10-20 acre (horizontal wells)
- Breakeven EUR ~30-50 Mbbl ($60 oil, $2-3MM well)
- Sweet spots: high initial oil saturation, good reservoir quality

Risk factors:
- Oil price volatility (commodity risk)
- Well performance uncertainty (geology)
- Operating cost inflation
- Regulatory changes (flaring, water disposal)
- Technical risk (completion quality)

Mitigation strategies:
- Pilot test before full-field infill
- Probabilistic EUR forecast (P10/P50/P90)
- Sensitivity to oil price and costs
- Portfolio optimization (high-grade best locations)
- Phase development over time
        """,
        key_factors=[
            "Well spacing (drainage area per well)",
            "Incremental EUR per infill well",
            "Drilling and completion costs",
            "Oil and gas prices (forecast)",
            "Operating costs (LOE, water handling)",
            "Discount rate and project timeline",
            "Reservoir heterogeneity (bypassed oil)",
            "Waterflood or EOR incremental recovery"
        ],
        primary_authority=[
            "SPE Economics & Evaluation (various papers)",
            "Arps, J.J. (1945) - 'Analysis of Decline Curves'",
            "Campbell, J.M. (1992) - Oil Property Evaluation",
            "Thompson, R.S. & Wright, J.D. (1985) - Oil Property Evaluation"
        ],
        burden_holder="Reservoir engineer / asset team planning field development",
        adversary_position="Infill drilling uneconomic; NPV negative or insufficient return on capital",
        counter_arguments=[
            "Infill locations selected based on simulation-predicted bypassed oil",
            "Economic analysis incorporates realistic price deck and cost estimates",
            "Pilot wells validate infill well performance assumptions",
            "Portfolio optimization maximizes NPV across all opportunities",
            "Sensitivity analysis quantifies downside risk"
        ],
        resolution_strategy="Use reservoir simulation to identify bypassed oil, economic analysis to rank opportunities, pilot test to validate",
        entity_scope="Applies to all field development decisions; fundamental to capital allocation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Infill program based on simulation, economic analysis, and pilot validation",
            "AGGRESSIVE": "Drilling infill wells without bypassed pay analysis or economic justification",
            "DISCLOSURE": "Economics sensitive to oil price; EUR forecasts probabilistic",
            "HIGH_RISK": "Proceeding with uneconomic infill program (NPV < 0 at realistic prices)"
        },
        controlling_precedent="Field development requires economic optimization, not just technical feasibility",
        issue_category=IssueCategory.FIELD_DEVELOPMENT,
        epistemic_guardrails=[
            "Oil price forecasts highly uncertain; use range of scenarios",
            "Actual well performance varies; probabilistic EUR essential"
        ]
    ),

    DoctrineBlock(
        topic="Permian Basin Reservoir Characteristics",
        keywords=["Permian Basin", "Spraberry", "Wolfcamp", "Delaware Basin", "Midland Basin", "tight oil"],
        conclusion_template=[
            "Permian Basin: multiple stacked plays, Paleozoic carbonate and sandstone, conventional to unconventional.",
            "Delaware and Midland sub-basins; major plays include Wolfcamp, Bone Spring, Spraberry, San Andres.",
            "Reservoir engineering varies by formation: conventional (secondary recovery) vs unconventional (primary horizontal wells)."
        ],
        reasoning_framework="""
Permian Basin overview:

Geographic extent:
- West Texas and SE New Mexico
- 86,000 square miles
- >500 producing fields
- Discovered 1920s, still actively developed

Sub-basins:
1. Delaware Basin (west)
   - Deeper (8,000-12,000 ft)
   - Higher pressure, temperature
   - Wolfcamp, Bone Spring plays

2. Midland Basin (east)
   - Shallower (5,000-9,000 ft)
   - Spraberry, Wolfcamp plays
   - Central Basin Platform between sub-basins

Major plays and characteristics:

San Andres Formation (conventional):
- Permian Age carbonate (dolomite)
- Depth: 4,000-6,000 ft
- Porosity: 8-15%, Permeability: 1-100 md
- Solution gas drive → waterflood
- Recovery: 15-25% primary, 30-50% waterflood
- CO2 EOR incremental: 10-15%

Spraberry Formation (tight oil):
- Leonardian Age sandstone/siltstone
- Depth: 6,500-8,500 ft
- Porosity: 8-12%, Permeability: 0.01-0.5 md
- Horizontal wells + hydraulic fracturing
- Recovery: 5-10% primary (no water drive)
- Large OOIP, low recovery per well

Wolfcamp Formation (unconventional):
- Pennsylvanian-Permian Age shale/carbonate
- Depth: 7,000-11,000 ft (varies by sub-basin)
- Porosity: 6-10%, Permeability: 0.001-0.01 md
- Multiple benches (Wolfcamp A, B, C, D)
- Horizontal wells, multistage fracturing
- High GOR (1,000-3,000 scf/stb), volatile oil

Bone Spring Formation (Delaware):
- Leonardian Age sandstone
- Depth: 8,000-10,000 ft
- Porosity: 8-14%, Permeability: 0.01-1 md
- Horizontal development, similar to Spraberry
- Lower GOR than Wolfcamp

Reservoir engineering considerations:

Conventional plays (San Andres, Grayburg):
- Pressure depletion → waterflood → CO2 EOR
- Pattern floods (five-spot, line drive)
- Infill drilling to 10-40 acre spacing
- Material balance and simulation standard tools

Unconventional plays (Wolfcamp, Spraberry, Bone Spring):
- Primary horizontal well development
- 10,000+ ft laterals, 50-100 frac stages
- Well spacing: 4-8 wells per 640-acre unit
- Parent-child well interference
- Decline curve analysis (Arps, Duong, Stretched Exponential)
- Limited role for waterflood (permeability too low)

Production statistics:
- Permian Basin: ~5 million BOPD (2024)
- ~40% of US oil production
- 1,000+ rigs actively drilling
- Hundreds of billions of barrels OOIP
        """,
        key_factors=[
            "Sub-basin (Delaware vs Midland)",
            "Formation (conventional vs unconventional)",
            "Depth and pressure regime",
            "Reservoir quality (porosity, permeability)",
            "Drive mechanism (solution gas, weak water drive)",
            "Development strategy (vertical vs horizontal)",
            "Recovery method (primary, waterflood, CO2 EOR)",
            "Well economics (EUR, costs, oil price)"
        ],
        primary_authority=[
            "Dutton, S.P. et al. (2005) - 'Permian Basin Oil and Gas Fields' AAPG Memoir",
            "Galley, J.E. (1958) - 'Oil and Geology in the Permian Basin'",
            "SPE Permian Basin Oil and Gas Recovery Conference (annual proceedings)",
            "Texas RRC and New Mexico OCD production data"
        ],
        burden_holder="Reservoir engineer developing Permian Basin assets",
        adversary_position="Reservoir characterization inadequate; development plan inappropriate for formation type",
        counter_arguments=[
            "Formation-specific reservoir characterization via core, logs, production data",
            "Development strategy matches formation characteristics (horizontal for tight, waterflood for conventional)",
            "Analogous field performance validates approach",
            "Probabilistic reserves account for uncertainty",
            "Operational experience in basin guides execution"
        ],
        resolution_strategy="Tailor reservoir engineering approach to formation type and reservoir quality; leverage basin analogs",
        entity_scope="Applies to all Permian Basin reservoirs; largest US oil-producing basin",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Formation-specific engineering approach, validated by analogs and field performance",
            "AGGRESSIVE": "Applying unconventional techniques to conventional reservoirs or vice versa",
            "DISCLOSURE": "Permian spans wide range of reservoir types; generalizations risky",
            "HIGH_RISK": "Ignoring formation-specific characteristics in development planning"
        },
        controlling_precedent="Permian Basin reservoir engineering must be tailored to specific formation and play type",
        issue_category=IssueCategory.FIELD_DEVELOPMENT,
        epistemic_guardrails=[
            "Permian reservoirs vary widely; formation-specific analysis essential",
            "Unconventional plays still evolving; best practices changing rapidly"
        ]
    )
]


# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class TelemetryCollector:
    def __init__(self):
        self.queries: List[QueryMetrics] = []
        self.start_time = time.time()
        self.doctrine_usage: Dict[str, int] = defaultdict(int)

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        for doctrine in metrics.doctrine_triggered:
            self.doctrine_usage[doctrine] += 1

    def get_stats(self) -> Dict[str, Any]:
        if not self.queries:
            return {
                "total_queries": 0,
                "avg_latency_ms": 0.0,
                "cache_hit_rate": 0.0
            }

        return {
            "total_queries": len(self.queries),
            "avg_latency_ms": sum(q.latency_ms for q in self.queries) / len(self.queries),
            "cache_hit_rate": sum(1 for q in self.queries if q.cache_hit) / len(self.queries),
            "mode_distribution": {
                mode: sum(1 for q in self.queries if q.mode == mode)
                for mode in ResponseMode
            },
            "top_doctrines": sorted(
                self.doctrine_usage.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }


# ============================================================================
# CORE ENGINE
# ============================================================================

class PROD04Engine:
    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.telemetry = TelemetryCollector()
        self.doctrine_index = self._build_doctrine_index()
        logger.info(f"PROD04 initialized with {len(self.doctrines)} doctrine blocks")

    def _build_doctrine_index(self) -> Dict[str, List[int]]:
        """Build keyword index for fast doctrine lookup"""
        index = defaultdict(list)
        for i, doctrine in enumerate(self.doctrines):
            for keyword in doctrine.keywords:
                index[keyword.lower()].append(i)
        return index

    def _search_doctrines(self, query: str) -> List[int]:
        """Search doctrines by keyword matching"""
        query_lower = query.lower()
        matched_indices: Set[int] = set()

        # Keyword matching
        for keyword, indices in self.doctrine_index.items():
            if keyword in query_lower:
                matched_indices.update(indices)

        # Category matching
        for i, doctrine in enumerate(self.doctrines):
            if doctrine.issue_category.value.lower().replace("_", " ") in query_lower:
                matched_indices.add(i)

        return list(matched_indices)

    def _generate_determinism_hash(self, query: str, triggered: List[int]) -> str:
        """Generate SHA-256 hash for reproducibility"""
        content = query + "|" + "|".join(str(i) for i in sorted(triggered))
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Dict[str, Any]:
        """TIE Gold Standard three-layer response"""
        start_time = time.time()

        # Layer 1: Doctrine cache (0-200ms)
        triggered_indices = self._search_doctrines(query)
        cache_hit = len(triggered_indices) > 0

        triggered_doctrines = [self.doctrines[i] for i in triggered_indices]

        # Layer 2: Semantic retrieval (fallback, not implemented here - would query vector DB)
        # Layer 3: Deep analysis (would invoke LLM, not implemented)

        # Build response based on mode
        if mode == ResponseMode.FAST:
            answer = self._fast_response(query, triggered_doctrines, zone)
        elif mode == ResponseMode.DEFENSE:
            answer = self._defense_response(query, triggered_doctrines, zone)
        else:  # MEMO
            answer = self._memo_response(query, triggered_doctrines, zone)

        # Determine confidence
        confidence = self._determine_confidence(triggered_doctrines)

        # Extract recommendations
        recommendations = self._extract_recommendations(triggered_doctrines)

        # Epistemic caveats
        caveats = self._extract_caveats(triggered_doctrines)

        latency_ms = (time.time() - start_time) * 1000

        # Record metrics
        metrics = QueryMetrics(
            query_id=hashlib.sha256(f"{time.time()}{query}".encode()).hexdigest()[:12],
            timestamp=datetime.now().isoformat(),
            mode=mode,
            latency_ms=latency_ms,
            cache_hit=cache_hit,
            doctrine_triggered=[d.topic for d in triggered_doctrines],
            confidence=confidence,
            zone=zone,
            issue_categories=[d.issue_category.value for d in triggered_doctrines],
            determinism_hash=self._generate_determinism_hash(query, triggered_indices)
        )
        self.telemetry.record_query(metrics)

        return {
            "answer": answer,
            "confidence": confidence,
            "doctrines_applied": [d.topic for d in triggered_doctrines],
            "issue_categories": list(set(d.issue_category.value for d in triggered_doctrines)),
            "cache_hit": cache_hit,
            "latency_ms": latency_ms,
            "determinism_hash": metrics.determinism_hash,
            "epistemic_caveats": caveats,
            "recommendations": recommendations,
            "query_id": metrics.query_id
        }

    def _fast_response(self, query: str, doctrines: List[DoctrineBlock], zone: AnalysisZone) -> str:
        """Concise response mode"""
        if not doctrines:
            return "No matching doctrines found in PROD04 reservoir management knowledge base. Query may be outside domain scope (material balance, drive mechanisms, waterflood, EOR, simulation, PVT, field development)."

        # Use first doctrine's conclusion template
        primary = doctrines[0]
        conclusion = " ".join(primary.conclusion_template)

        return f"**{primary.topic}**\n\n{conclusion}\n\n**Confidence:** {primary.confidence.value}"

    def _defense_response(self, query: str, doctrines: List[DoctrineBlock], zone: AnalysisZone) -> str:
        """Audit-ready response mode"""
        if not doctrines:
            return "No applicable doctrines found. Query requires domain expertise outside PROD04 scope."

        sections = []

        for doctrine in doctrines[:3]:  # Top 3 doctrines
            section = f"### {doctrine.topic}\n\n"
            section += f"**Conclusion:** {' '.join(doctrine.conclusion_template)}\n\n"
            section += f"**Reasoning Framework:**\n{doctrine.reasoning_framework}\n\n"
            section += f"**Key Factors:** {', '.join(doctrine.key_factors)}\n\n"
            section += f"**Authority:** {'; '.join(doctrine.primary_authority)}\n\n"
            section += f"**Confidence Stratification:**\n"
            for level, desc in doctrine.confidence_stratification.items():
                section += f"- **{level}:** {desc}\n"
            section += "\n"
            sections.append(section)

        return "\n".join(sections)

    def _memo_response(self, query: str, doctrines: List[DoctrineBlock], zone: AnalysisZone) -> str:
        """Full documentation mode"""
        if not doctrines:
            return "# Reservoir Management Analysis\n\nNo applicable doctrines identified for this query."

        memo = "# Reservoir Management Analysis - PROD04 Engine\n\n"
        memo += f"**Query:** {query}\n\n"
        memo += f"**Analysis Zone:** {zone.value}\n\n"
        memo += f"**Doctrines Applied:** {len(doctrines)}\n\n"
        memo += "---\n\n"

        for i, doctrine in enumerate(doctrines, 1):
            memo += f"## {i}. {doctrine.topic}\n\n"
            memo += f"**Issue Category:** {doctrine.issue_category.value}\n\n"
            memo += f"**Keywords:** {', '.join(doctrine.keywords)}\n\n"
            memo += f"### Conclusion\n{' '.join(doctrine.conclusion_template)}\n\n"
            memo += f"### Reasoning Framework\n{doctrine.reasoning_framework}\n\n"
            memo += f"### Key Factors\n"
            for factor in doctrine.key_factors:
                memo += f"- {factor}\n"
            memo += "\n"
            memo += f"### Primary Authority\n"
            for auth in doctrine.primary_authority:
                memo += f"- {auth}\n"
            memo += "\n"
            memo += f"### Confidence Stratification\n"
            for level, desc in doctrine.confidence_stratification.items():
                memo += f"**{level}:** {desc}\n\n"
            memo += f"### Counter-Arguments\n"
            for arg in doctrine.counter_arguments:
                memo += f"- {arg}\n"
            memo += "\n"
            memo += f"### Resolution Strategy\n{doctrine.resolution_strategy}\n\n"
            memo += "---\n\n"

        return memo

    def _determine_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Determine overall confidence from triggered doctrines"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Use highest confidence level (most conservative)
        confidence_order = [
            ConfidenceLevel.DEFENSIBLE,
            ConfidenceLevel.AGGRESSIVE,
            ConfidenceLevel.DISCLOSURE,
            ConfidenceLevel.HIGH_RISK
        ]

        for conf in confidence_order:
            if any(d.confidence == conf for d in doctrines):
                return conf

        return ConfidenceLevel.DEFENSIBLE

    def _extract_recommendations(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract actionable recommendations"""
        recs = []
        for doctrine in doctrines:
            recs.append(f"{doctrine.topic}: {doctrine.resolution_strategy}")
        return recs[:5]  # Top 5

    def _extract_caveats(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract epistemic guardrails"""
        caveats = []
        for doctrine in doctrines:
            caveats.extend(doctrine.epistemic_guardrails)
        return list(set(caveats))[:10]  # Unique, top 10


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="PROD04 - Reservoir Management Intelligence Engine",
    description="TIE Gold Standard - Production Engineering Domain",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Global engine instance
ENGINE = PROD04Engine()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint - three-layer response"""
    try:
        result = ENGINE.three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone
        )
        return QueryResponse(**result)
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Comprehensive health check"""
    stats = ENGINE.telemetry.get_stats()
    return HealthResponse(
        status="operational",
        version="1.0.0",
        port=9034,
        doctrines_loaded=len(ENGINE.doctrines),
        cache_size=len(ENGINE.doctrine_index),
        uptime_seconds=time.time() - ENGINE.telemetry.start_time,
        total_queries=stats["total_queries"],
        avg_latency_ms=stats["avg_latency_ms"]
    )


@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrines"""
    return {
        "total": len(ENGINE.doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in ENGINE.doctrines
        ]
    }


@APP.get("/stats")
async def statistics_endpoint():
    """Telemetry statistics"""
    return ENGINE.telemetry.get_stats()


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting PROD04 Reservoir Management Engine on port 9034")
    uvicorn.run(APP, host="0.0.0.0", port=9034, log_level="info")
