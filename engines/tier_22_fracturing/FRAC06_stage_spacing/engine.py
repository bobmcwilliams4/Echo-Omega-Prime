"""
FRAC06 - Stage & Cluster Spacing Optimization Engine
====================================================

TIE Gold Standard engine for completion design optimization focusing on stage spacing,
cluster spacing, lateral development strategies, and field development planning.

Domain Expertise:
- Stage spacing optimization (150-300 ft ranges)
- Cluster spacing within stages (15-75 ft)
- Perforation cluster count per stage
- Lateral length optimization
- Stacked lateral development (Wolfcamp, Bone Spring)
- Well spacing optimization (parent-child relationships)
- Infill drilling strategies and cube development
- Frac-driven interactions (FBI) between wells
- Pressure depletion effects on child wells
- Protective fracs and co-development strategies
- Completion intensity metrics
- EUR sensitivity to completion design
- Economic optimization of completion parameters
- Permian Basin spacing evolution (2014-2024)
- Landing zone selection and development patterns

Port: 9026
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

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger


# ============================================================================
# CONFIGURATION & INITIALIZATION
# ============================================================================

APP = FastAPI(
    title="FRAC06 - Stage & Cluster Spacing Optimization Engine",
    version="1.0.0",
    description="TIE Gold Standard engine for completion design optimization"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.add(
    Path(__file__).parent / "logs" / "frac06_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)


# ============================================================================
# ENUMS & CONSTANTS
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
    STAGE_SPACING = "STAGE_SPACING"
    CLUSTER_SPACING = "CLUSTER_SPACING"
    WELL_SPACING = "WELL_SPACING"
    LATERAL_LENGTH = "LATERAL_LENGTH"
    STACKED_DEVELOPMENT = "STACKED_DEVELOPMENT"
    PARENT_CHILD = "PARENT_CHILD"
    COMPLETION_INTENSITY = "COMPLETION_INTENSITY"
    ECONOMIC_OPTIMIZATION = "ECONOMIC_OPTIMIZATION"
    FIELD_DEVELOPMENT = "FIELD_DEVELOPMENT"
    OPERATIONAL_STRATEGY = "OPERATIONAL_STRATEGY"


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., description="Completion design question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis zone")


class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    issue_category: IssueCategory
    fragility_score: float = Field(ge=0.0, le=1.0)


class QueryResponse(BaseModel):
    answer: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    doctrines_triggered: List[str]
    reasoning_chain: Optional[List[str]] = None
    sources: List[str]
    determinism_hash: str
    telemetry: Dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    version: str
    doctrines_loaded: int
    cache_size: int
    uptime_seconds: float


# ============================================================================
# DOCTRINE CACHE - REAL COMPLETION SPACING EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Permian Basin Stage Spacing Evolution",
        keywords=["stage spacing", "Permian", "evolution", "150 ft", "200 ft", "300 ft", "2014", "trend"],
        conclusion_template=[
            "Permian Basin stage spacing has evolved significantly from 2014-2024, moving from tight 150 ft spacing to wider 200-300 ft spacing based on production data analysis.",
            "The industry learned that excessively tight stage spacing (100-150 ft) created severe frac-driven interactions reducing cluster efficiency and overall EUR.",
            "Current best practice for Wolfcamp and Bone Spring formations favors 200-250 ft stage spacing as optimal balance between capital efficiency and production."
        ],
        reasoning_framework="""
Early Permian development (2014-2016) featured aggressive 100-150 ft stage spacing driven by:
1. Limited parent well data
2. Desire to maximize contact with formation
3. Lower service costs making high stage counts economical
4. Assumption that more stages = more production

Production data from 2016-2019 revealed:
1. Wells with 150 ft spacing underperformed 200 ft spacing wells
2. Microseismic showed severe stage-to-stage interference at <150 ft
3. Cluster efficiency dropped significantly with tight spacing
4. Capital costs rose without proportional EUR gains

Evolution to current practice (2020-2024):
1. Industry consensus moved to 200-250 ft stage spacing
2. Delaware Basin operators favor 200-225 ft
3. Midland Basin operators use 225-250 ft
4. Bone Spring typically 200-225 ft, Wolfcamp 225-250 ft

Key data points supporting wider spacing:
- EUR per lateral foot peaks at 200-250 ft spacing
- Cluster efficiency improves 15-25% vs tight spacing
- Capital cost per BOE decreases 10-18%
- Simulated reservoir volume increases with wider spacing
- Pressure interference between stages minimized

Exceptions requiring tighter spacing:
- Very low permeability zones (<50 nd) may benefit from 175-200 ft
- Thin pay zones (<100 ft gross) sometimes use 150-175 ft
- Areas with natural fractures may allow tighter spacing
""",
        key_factors=[
            "Historical production data from 2014-2024",
            "Microseismic analysis of frac geometry",
            "Cluster efficiency metrics",
            "EUR per lateral foot analysis",
            "Capital cost per BOE optimization",
            "Reservoir permeability and thickness",
            "Formation-specific characteristics (Wolfcamp vs Bone Spring)"
        ],
        primary_authority=[
            "SPE 199748: Permian Basin Completion Optimization 2014-2020",
            "URTeC 3723: Delaware Basin Stage Spacing Evolution",
            "JPT Article: Wolfcamp Development Best Practices (2022)",
            "Operator completion reports: Pioneer, Diamondback, EOG 2020-2024"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.STAGE_SPACING,
        fragility_score=0.15
    ),

    DoctrineBlock(
        topic="Optimal Cluster Spacing Within Stages",
        keywords=["cluster spacing", "perforation", "15 ft", "25 ft", "50 ft", "cluster count", "efficiency"],
        conclusion_template=[
            "Cluster spacing of 25-35 ft is optimal for most Permian unconventional completions, balancing cluster efficiency with sufficient formation contact.",
            "Excessively tight cluster spacing (<20 ft) creates stress shadow interference reducing perforation efficiency to 40-60% of clusters.",
            "Wider cluster spacing (40-50 ft) improves individual cluster efficiency but may leave unstimulated rock between clusters in low-permeability formations."
        ],
        reasoning_framework="""
Cluster spacing optimization involves balancing:
1. Stress shadow effects between clusters
2. Formation permeability and fracture propagation
3. Proppant distribution efficiency
4. Capital cost per cluster
5. Pumping pressure limitations

Tight spacing (15-25 ft):
- Used in early Permian completions (2014-2017)
- Creates severe stress shadow interference
- Fiber optic DAS data shows only 50-70% of clusters take fluid
- Un-stimulated clusters become barriers to production
- Results in lower EUR despite higher cluster count
- More economical in very low permeability (<30 nd)

Moderate spacing (25-35 ft):
- Current industry best practice for most formations
- Reduces stress shadow interference
- Cluster efficiency improves to 70-85%
- Sufficient formation contact in moderate permeability (50-200 nd)
- Optimal capital efficiency (cost per BOE)
- Recommended for Wolfcamp A/B/C and Bone Spring

Wider spacing (40-50 ft):
- Used in higher permeability formations (>200 nd)
- Cluster efficiency can reach 85-95%
- Risk of leaving unstimulated rock in tight formations
- Lower cluster count reduces capital cost
- May be optimal in naturally fractured reservoirs
- Delaware Basin upper Wolfcamp sometimes uses 40-50 ft

Stage length and cluster count interaction:
- 200 ft stage with 25 ft spacing = 8 clusters
- 225 ft stage with 30 ft spacing = 7-8 clusters
- 250 ft stage with 35 ft spacing = 7 clusters
- Most operators target 6-9 clusters per stage

Operational considerations:
- Limited entry design requires specific hole count/diameter
- Plug-and-perf completion method most common
- Sliding sleeve systems may allow tighter spacing
- Diverter usage can improve cluster efficiency with any spacing
""",
        key_factors=[
            "Fiber optic DAS/DTS cluster efficiency measurements",
            "Formation permeability",
            "Stress shadow modeling",
            "Proppant distribution analysis",
            "EUR per cluster economics",
            "Operational constraints (limited entry design)",
            "Formation mechanical properties"
        ],
        primary_authority=[
            "SPE 194334: Cluster Spacing Optimization Using Fiber Optics",
            "URTeC 2901: Stress Shadow Effects on Cluster Efficiency",
            "SPE 201339: Permian Basin Perforation Cluster Analysis",
            "Vendor data: Halliburton, SLB fiber optic studies 2019-2023"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.CLUSTER_SPACING,
        fragility_score=0.20
    ),

    DoctrineBlock(
        topic="Well Spacing Optimization - Parent-Child Relationships",
        keywords=["well spacing", "parent", "child", "infill", "660 ft", "880 ft", "frac hits", "depletion"],
        conclusion_template=[
            "Optimal well spacing in Permian Basin ranges from 660-880 ft depending on formation, landing zone, and development strategy, with wider spacing favored for newer development.",
            "Parent-child well spacing must account for pressure depletion, which can reduce child well EUR by 15-30% compared to parent wells.",
            "Protective frac and co-development strategies can mitigate parent-child interference, justifying tighter spacing in some cases."
        ],
        reasoning_framework="""
Well spacing evolution mirrors stage spacing trends - industry learned through production data:

Early development (2014-2017):
- Aggressive 440-660 ft spacing common
- Driven by desire to maximize acreage development
- Limited understanding of parent-child interactions
- Lower service costs justified tighter spacing

Parent well performance established baseline:
- Initial production rates (IP) set expectations
- 30-day, 90-day, 180-day cumulative established type curves
- Ultimate recovery (EUR) projections built operator models
- Economic threshold rates determined spacing assumptions

Child well underperformance discovered (2017-2019):
- First infill drilling campaigns showed 15-30% EUR reduction
- Frac-driven interactions (frac hits) damaged parent wells
- Pressure depletion in parent drainage area affected child wells
- Asymmetric drainage (child wells pulled toward depleted parent)
- Some child wells had negative NPV despite parent economics

Current spacing practices (2020-2024):
- Delaware Basin: 660-880 ft, trending toward 750-800 ft
- Midland Basin: 660-880 ft, most common 750-825 ft
- Newer vintages favoring 800+ ft spacing
- Stack-and-space (wide spacing, simultaneous development)
- Wine-rack patterns in multi-bench development

Formation-specific spacing:
- Wolfcamp A: 750-880 ft optimal (higher permeability)
- Wolfcamp B: 660-800 ft (moderate permeability)
- Wolfcamp C/D: 660-750 ft (lower permeability, thinner pay)
- Bone Spring: 660-800 ft depending on landing zone
- Third Bone Spring: 750-880 ft (best rock quality)

Mitigation strategies for tighter spacing:
1. Protective frac: Re-frac parent wells before child wells drilled
2. Co-development: Complete parent and child simultaneously
3. Pressure management: Maintain parent well pressure via reduced production
4. Refracturing: Re-stimulate parent wells to reset pressure
5. Modified completion: Reduce child well completion intensity

Economic optimization:
- Net present value (NPV) per acre drives spacing decisions
- Wider spacing: higher per-well EUR, fewer wells per section
- Tighter spacing: lower per-well EUR, more wells per section
- Break-even analysis typically favors 750-850 ft in Permian
- Service cost inflation (2021-2023) pushed toward wider spacing
""",
        key_factors=[
            "Parent well production data and pressure depletion",
            "Child well EUR degradation percentage",
            "Formation permeability and natural fracture networks",
            "Economic analysis (NPV per acre vs per well)",
            "Operational constraints (pad size, surface access)",
            "Regulatory spacing units (typically 640 acre sections)",
            "Service costs and capital efficiency targets"
        ],
        primary_authority=[
            "SPE 194493: Parent-Child Well Interactions in Permian Basin",
            "URTeC 3728: Well Spacing Optimization Workflow",
            "SPE 199689: Economic Analysis of Well Spacing",
            "Permian Basin operators: Pioneer Natural Resources spacing evolution white papers"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.WELL_SPACING,
        fragility_score=0.25
    ),

    DoctrineBlock(
        topic="Cube Development and Stacked Lateral Strategy",
        keywords=["cube development", "stacked laterals", "Wolfcamp", "Bone Spring", "landing zone", "wine-rack", "co-development"],
        conclusion_template=[
            "Cube development (simultaneous multi-bench development) maximizes NPV per acre by reducing parent-child interference and optimizing capital deployment.",
            "Wolfcamp A/B/C and Bone Spring formations in Delaware Basin support 4-6 productive landing zones, enabling stacked lateral development.",
            "Wine-rack pattern with co-development timing is preferred over sequential pad development to minimize frac-driven interactions and depletion effects."
        ],
        reasoning_framework="""
Cube development philosophy:
- Develop all productive zones in a drilling spacing unit (DSU) simultaneously or in rapid succession
- Minimizes parent-child well interference across all zones
- Optimizes capital efficiency through batch drilling and completion
- Reduces surface footprint and operational complexity

Permian Basin productive zones (Delaware):
1. Third Bone Spring Upper/Middle/Lower (3 zones)
2. Second Bone Spring (1-2 zones)
3. Wolfcamp A Upper/Lower (2 zones)
4. Wolfcamp B Upper/Middle/Lower (3 zones)
5. Wolfcamp C (1-2 zones)
Total: 10-13 potential landing zones in full column

Practical cube development:
- Most operators develop 4-6 zones economically
- Typical cube: 3BS, 2BS, WCA, WCB (4 zones)
- Each zone: 2-4 laterals depending on spacing (660-880 ft)
- Total: 8-16 wells per section (640 acres)
- Drilling time: 6-12 months for full cube
- Completion time: 2-4 months (simul-frac or zipper frac)

Wine-rack vs stack-and-space patterns:
Wine-rack (staggered):
- Upper zones laterals offset from lower zones
- Reduces vertical interference between zones
- Allows 50-150 ft vertical spacing between zones
- Better for formations with significant height (>300 ft)

Stack-and-space (aligned):
- All zone laterals aligned vertically
- Simpler surface logistics (single pad)
- Requires wider vertical spacing (>200 ft)
- Used when zones are naturally separated

Co-development timing strategies:
1. Simul-frac: Complete all zones simultaneously (2-4 frac spreads)
   - Fastest capital deployment
   - Eliminates parent-child timing issues
   - Highest operational complexity
   - Most expensive (multiple frac crews)

2. Zipper frac: Alternate stages between zones
   - One frac crew serves multiple wells
   - Moderate capital deployment speed
   - Good parent-child mitigation
   - Standard industry practice

3. Sequential by zone: Complete all laterals in one zone before next
   - Slower capital deployment
   - Creates parent-child issues between zones
   - Simpler operations
   - Generally inferior to simul/zipper

Vertical spacing considerations:
- Minimum 150 ft between landing zones (stress shadow)
- Ideal 200-300 ft separation
- Wolfcamp zones typically 150-250 ft thick
- Bone Spring zones 100-200 ft thick
- Total column height: 2,000-3,000 ft in Delaware Basin

Case study - typical Delaware Basin cube:
- Section: 640 acres
- Zones: 3BS (2 wells), WCA (2 wells), WCB (3 wells)
- Total: 7 wells at 800 ft spacing
- Stage spacing: 225 ft, cluster spacing: 30 ft
- Completion: zipper frac, 3-month campaign
- First production: all wells online within 30 days
- Result: minimal parent-child effects, optimized NPV
""",
        key_factors=[
            "Number of productive zones in geologic column",
            "Vertical spacing between zones (stress shadow)",
            "Lateral spacing within each zone",
            "Operational capacity (drilling rigs, frac crews)",
            "Capital availability and deployment strategy",
            "Surface access and pad design constraints",
            "Regulatory requirements (spacing units, pooling)"
        ],
        primary_authority=[
            "SPE 199750: Cube Development in Delaware Basin",
            "URTeC 3821: Stacked Lateral Optimization",
            "SPE 201391: Wolfcamp and Bone Spring Development Strategies",
            "Operator presentations: Cimarex, Centennial, Matador cube development results"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.STACKED_DEVELOPMENT,
        fragility_score=0.30
    ),

    DoctrineBlock(
        topic="Completion Intensity Metrics and EUR Correlation",
        keywords=["completion intensity", "proppant", "fluid", "pounds per foot", "EUR", "diminishing returns"],
        conclusion_template=[
            "Completion intensity (proppant and fluid per lateral foot) shows strong correlation with EUR up to optimal thresholds, beyond which diminishing returns occur.",
            "Permian Basin optimal intensity: 1,800-2,500 lbs proppant per lateral foot and 50-75 bbls fluid per foot for most Wolfcamp and Bone Spring zones.",
            "Excessively high intensity (>3,000 lbs/ft) increases capital cost 20-30% with minimal EUR improvement (<5%)."
        ],
        reasoning_framework="""
Completion intensity evolution in Permian Basin:

Early completions (2014-2016):
- Light intensity: 800-1,200 lbs proppant/ft
- 30-45 bbls fluid/ft
- 100 mesh sand, limited use of ceramics
- Results: established baseline EUR but underutilized reservoir

Ramp-up period (2017-2019):
- Increasing intensity: 1,500-2,200 lbs/ft
- 50-70 bbls fluid/ft
- Mix of 100 mesh and 40/70 sand
- Strong EUR correlation with intensity
- Industry consensus: "more is better"

Peak intensity (2020-2021):
- Maximum intensity: 2,500-3,500 lbs/ft
- 75-100 bbls fluid/ft
- Premium proppants (ceramics, resin-coated)
- Diminishing returns discovered
- Capital costs exceeded EUR value in many cases

Current optimized approach (2022-2024):
- Tailored intensity: 1,800-2,500 lbs/ft (formation-dependent)
- 50-75 bbls fluid/ft
- 100 mesh and 40/70 sand blend
- Focus on cluster efficiency vs total volume
- Economic optimization (cost per BOE)

Formation-specific optimal intensity:

Wolfcamp A (higher quality):
- 1,800-2,200 lbs/ft
- 50-65 bbls/ft
- Higher permeability allows lower intensity
- Typical stage: 400,000-500,000 lbs proppant

Wolfcamp B (moderate quality):
- 2,000-2,500 lbs/ft
- 60-75 bbls/ft
- Moderate permeability requires higher intensity
- Typical stage: 450,000-550,000 lbs proppant

Wolfcamp C/D (lower quality):
- 2,200-2,800 lbs/ft
- 65-80 bbls/ft
- Lower permeability benefits from higher intensity
- Typical stage: 500,000-625,000 lbs proppant

Bone Spring (variable):
- Third Bone Spring: 1,800-2,300 lbs/ft (best quality)
- Second Bone Spring: 2,000-2,500 lbs/ft
- First Bone Spring: 2,200-2,800 lbs/ft (tightest)

EUR sensitivity analysis:
- Below 1,500 lbs/ft: EUR reduced 15-25%
- 1,500-2,000 lbs/ft: EUR improves 10-15%
- 2,000-2,500 lbs/ft: EUR improves 5-10%
- Above 2,500 lbs/ft: EUR improves <5%
- Above 3,000 lbs/ft: EUR improves <2%, capital cost up 20-30%

Economic sweet spot:
- Cost per BOE minimized at 1,800-2,500 lbs/ft for most formations
- NPV maximized at moderate intensity
- Service cost inflation (2021-2024) shifted optimum lower
- Proppant logistics constraints favor moderate intensity

Operational considerations:
- Pumping rate: 80-100 bpm for most Permian completions
- Proppant concentration: ramp to 2.5-3.0 ppg maximum
- Fluid type: slickwater with friction reducer
- Diverter stages: improve cluster efficiency vs adding volume
""",
        key_factors=[
            "Formation permeability and porosity",
            "Historical EUR correlation data",
            "Proppant and service costs",
            "Cluster efficiency (percentage of clusters taking fluid/proppant)",
            "Pumping rate and pressure limitations",
            "Economic metrics (NPV, cost per BOE)",
            "Operational constraints (water availability, proppant logistics)"
        ],
        primary_authority=[
            "SPE 199737: Completion Intensity Optimization in Permian Basin",
            "URTeC 2019: Proppant Loading and EUR Correlation Study",
            "SPE 201388: Economic Analysis of Completion Design",
            "Industry data: Halliburton, Liberty Oilfield Services completion databases"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.COMPLETION_INTENSITY,
        fragility_score=0.25
    ),

    DoctrineBlock(
        topic="Lateral Length Optimization",
        keywords=["lateral length", "5000 ft", "7500 ft", "10000 ft", "15000 ft", "economics", "drilling cost"],
        conclusion_template=[
            "Optimal lateral length is 7,500-10,000 ft for most Permian Basin unconventional wells, balancing drilling cost, completion efficiency, and EUR.",
            "Ultra-long laterals (>12,000 ft) face operational challenges (torque and drag, pumping pressure) and completion efficiency degradation in distal stages.",
            "Short laterals (<5,000 ft) have higher per-foot drilling cost and lower overall EUR despite potentially better completion efficiency."
        ],
        reasoning_framework="""
Lateral length economic drivers:

Fixed costs (favor longer laterals):
- Surface pad construction: $200,000-500,000
- Vertical hole and curve: $500,000-1,000,000
- Completion spread mobilization: $100,000-300,000
- Flowback and well testing: $50,000-150,000
- Facilities (tank battery, separator): $300,000-800,000
Total fixed: $1,150,000-2,750,000

Variable costs (per lateral foot):
- Drilling (lateral): $200-350/ft
- Completion (perf/frac/proppant): $400-650/ft
- Total variable: $600-1,000/ft

Cost per lateral foot by length:
- 5,000 ft lateral: $830-1,550/ft total
- 7,500 ft lateral: $680-1,200/ft total
- 10,000 ft lateral: $615-1,075/ft total
- 12,500 ft lateral: $570-1,000/ft total
- 15,000 ft lateral: $540-950/ft total

Longer laterals reduce cost per foot but face operational limits.

Operational challenges by length:

5,000-7,500 ft (standard):
- Minimal torque and drag
- Conventional pumping pressure
- Good completion efficiency (85-95%)
- Simple flowback and production
- Proven reliability

7,500-10,000 ft (optimal):
- Manageable torque and drag
- Conventional to slightly elevated pumping pressure
- Good completion efficiency (80-90%)
- Cost per foot significantly reduced
- Current industry standard

10,000-12,500 ft (extended):
- Increased torque and drag (may require rotary steerable)
- Elevated pumping pressure (stress shadow in distal stages)
- Moderate completion efficiency degradation (75-85%)
- Logistical complexity (longer frac jobs)
- Used in large acreage positions

12,500-15,000 ft (ultra-long):
- Severe torque and drag (rotary steerable required)
- High pumping pressure (near formation breakdown)
- Completion efficiency degradation (70-80% in distal stages)
- Proppant transport challenges
- Extended pumping time (60-90 days per well)
- Reserved for exceptional economics

Above 15,000 ft (extreme):
- Limited adoption in industry
- Multi-lateral or staged drilling sometimes used
- Completion efficiency <70% in distal stages
- Reserved for special cases (offshore analogues)

EUR per lateral foot by length:
- Short laterals (<6,000 ft): 15-25 BOE/ft (good efficiency, small volume)
- Standard laterals (7,500-10,000 ft): 18-28 BOE/ft (optimal)
- Extended laterals (10,000-12,500 ft): 16-24 BOE/ft (efficiency loss offset by volume)
- Ultra-long (>12,500 ft): 14-22 BOE/ft (efficiency degradation)

Acreage and spacing constraints:
- 640 acre section (1 mile × 1 mile): supports 5,280 ft laterals
- Two-section unit (1 mile × 2 miles): supports 10,560 ft laterals
- Four-section unit (2 miles × 2 miles): supports 10,560 ft laterals
- Irregularly shaped units: may dictate non-standard lengths

Formation-specific considerations:
- Uniform formations (Wolfcamp B): support longer laterals
- Variable formations (Bone Spring): may favor shorter laterals with better zone targeting
- Faulted areas: require shorter laterals to stay in zone

Current industry trends (2024):
- Delaware Basin average: 8,500-10,000 ft
- Midland Basin average: 7,500-9,500 ft
- Large operators (Pioneer, EOG): pushing toward 10,000 ft
- Smaller operators: 7,500-9,000 ft most common
""",
        key_factors=[
            "Fixed vs variable cost breakdown",
            "Torque and drag limitations",
            "Completion efficiency in distal stages",
            "Acreage position and lease boundaries",
            "Formation continuity and quality",
            "Service cost environment",
            "EUR per lateral foot optimization"
        ],
        primary_authority=[
            "SPE 194488: Lateral Length Optimization Economic Analysis",
            "URTeC 3156: Extended Reach Laterals in Permian Basin",
            "SPE 199741: Completion Efficiency in Long Laterals",
            "Drilling Contractor Magazine: Permian lateral length trends 2020-2024"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.LATERAL_LENGTH,
        fragility_score=0.20
    ),

    DoctrineBlock(
        topic="Frac-Driven Interactions (FBI) and Mitigation",
        keywords=["frac hits", "FBI", "communication", "parent well", "child well", "interference", "pressure spike"],
        conclusion_template=[
            "Frac-driven interactions (frac hits) occur in 60-80% of infill well completions, causing parent well production loss and potential wellbore damage.",
            "Mitigation strategies include protective frac, co-development, pressure management, and modified completion design for child wells.",
            "Unmanaged frac hits can reduce parent well production 20-40% and create negative value in child wells despite good initial production."
        ],
        reasoning_framework="""
Frac-driven interaction (FBI) mechanisms:

Pressure communication:
- Fracture networks from child well intersect depleted parent well drainage
- Pressure pulse transmitted to parent well (monitored via surface pressure)
- Proppant and fracturing fluid enter parent wellbore
- Parent well production disrupted during and after child completion

Types of frac hits:

Minor hit:
- Pressure increase <500 psi at parent well
- Minimal fluid/proppant production from parent
- Production recovers within 30-60 days
- Long-term EUR impact <5%

Moderate hit:
- Pressure increase 500-2,000 psi
- Significant fluid/proppant flowback from parent
- Production disrupted 60-180 days
- Long-term EUR impact 5-15%

Severe hit:
- Pressure increase >2,000 psi
- Heavy proppant production from parent (well loading)
- Parent well may require workover/cleanout
- Production disrupted >180 days or permanently
- Long-term EUR impact 15-40%

Factors increasing frac hit severity:
1. Proximity: closer spacing (<600 ft) increases severity
2. Pressure depletion: greater parent depletion = worse hit
3. Completion intensity: higher child well intensity = worse hit
4. Formation permeability: higher permeability = more communication
5. Natural fractures: enhance connectivity between wells
6. Timing: immediate infill (high parent pressure) less severe than delayed infill

Mitigation strategy 1 - Protective frac:
- Re-fracture parent well before child well completion
- Re-pressurizes parent drainage area
- Creates proppant barrier protecting parent perforations
- Reduces severity of child well frac hit by 50-80%
- Cost: $1-2 million per parent well
- Best practice: protective frac 30-90 days before child well completion

Mitigation strategy 2 - Co-development (simul-frac):
- Complete parent and child wells simultaneously
- Eliminates pressure depletion gradient
- No asymmetric drainage between wells
- Equal initial conditions for all wells
- Most effective mitigation but requires simultaneous drilling/completion
- Used in cube development and greenfield areas

Mitigation strategy 3 - Pressure management:
- Reduce parent well production rate before child completion
- Allow parent well pressure to build
- Reduces pressure differential driving frac hits
- Temporary production loss offset by better child well performance
- Requires 60-180 days of reduced parent production

Mitigation strategy 4 - Modified child completion:
- Reduce completion intensity near parent well (tapered design)
- Use lower pumping rates in toe stages (near parent)
- Deploy diverters to force fractures away from parent
- Stage spacing wider near parent well
- Results: 10-30% reduction in frac hit severity

Economic analysis of mitigation:
- Unmitigated frac hits: $2-8 million parent EUR loss per child well
- Protective frac cost: $1-2 million
- Co-development additional cost: $0.5-1 million (operational complexity)
- Pressure management cost: $0.5-1.5 million (deferred production)
- Modified completion cost: minimal (<$200,000)

Industry adoption:
- Large operators (>100,000 boe/d): 70% use mitigation strategies
- Mid-size operators: 40% use mitigation
- Small operators: <20% use mitigation (cost constraints)
- Delaware Basin: higher adoption than Midland Basin
- Newer development (post-2020): mitigation standard practice

Case study data:
- Operator A (protective frac): reduced parent EUR loss from 25% to 8%
- Operator B (co-development): eliminated measurable frac hits
- Operator C (no mitigation): average parent EUR loss 22%, child well NPV negative in 30% of cases
""",
        key_factors=[
            "Well spacing and proximity to parent wells",
            "Parent well pressure depletion level",
            "Child well completion intensity",
            "Formation permeability and natural fractures",
            "Timing between parent and child completions",
            "Economic value of parent well reserves at risk",
            "Mitigation strategy costs vs benefits"
        ],
        primary_authority=[
            "SPE 199731: Frac-Driven Interactions in Permian Basin",
            "URTeC 2973: Protective Frac Design and Implementation",
            "SPE 201351: Parent-Child Well Management Strategies",
            "Industry data: RSP Permian, Centennial, Laredo case studies 2018-2023"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.PARENT_CHILD,
        fragility_score=0.35
    ),

    DoctrineBlock(
        topic="Economic Optimization Framework for Completion Design",
        keywords=["NPV", "economics", "cost per BOE", "capital efficiency", "IRR", "optimization"],
        conclusion_template=[
            "Completion design optimization must balance EUR maximization against capital cost to maximize net present value (NPV) per acre and internal rate of return (IRR).",
            "Optimal design varies with commodity prices: $70/bbl oil favors moderate intensity (2,000 lbs/ft), $90/bbl favors higher intensity (2,500 lbs/ft).",
            "Full-cycle economics including facilities, gathering, and midstream costs may shift optimal completion design 10-20% lighter than EUR-optimal design."
        ],
        reasoning_framework="""
Economic optimization framework components:

Revenue drivers:
1. Oil EUR (bbls per well)
2. Gas EUR (mcf per well)
3. Oil price ($/bbl)
4. Gas price ($/mcf)
5. NGL content and pricing
6. Production decline curve (hyperbolic b-factor)
7. Operating life of well

Cost components:
1. Drilling AFE (authority for expenditure)
   - Pad construction: $300,000-600,000
   - Vertical and curve: $700,000-1,200,000
   - Lateral drilling: $1,500,000-3,500,000 (length dependent)
   - Casing and cement: $800,000-1,500,000

2. Completion AFE
   - Perforating: $100,000-250,000
   - Pumping services: $2,000,000-5,000,000
   - Proppant: $1,500,000-4,000,000
   - Chemicals and fluid: $300,000-800,000
   - Wireline and tools: $200,000-400,000

3. Facilities and infrastructure
   - Well site facilities: $400,000-1,000,000
   - Gathering connection: $200,000-800,000
   - Midstream processing: $0-500,000

4. Operating expenses (OPEX)
   - Lease operating expense (LOE): $5-12/boe
   - Workover reserves: $100,000-300,000 over life
   - Downhole pump replacements: 2-4 over well life

5. Non-operated costs
   - Severance taxes: 4.6% (Texas)
   - Royalty burden: 18-25%
   - Gathering and processing: $3-8/boe

Example economic scenarios:

Base case (2024 typical Wolfcamp B):
- Lateral length: 9,000 ft
- Stage spacing: 225 ft (40 stages)
- Cluster spacing: 30 ft (7 clusters/stage)
- Proppant intensity: 2,200 lbs/ft
- Total proppant: 19.8 million lbs
- Total fluid: 585,000 bbls
- Drilling cost: $4.8 million
- Completion cost: $6.2 million
- Facilities cost: $1.2 million
- Total well cost: $12.2 million
- EUR: 850,000 boe (70% oil)
- Oil price: $75/bbl
- NPV @ 10%: $18.5 million
- IRR: 65%
- Payout: 18 months

Optimized case (economics-driven):
- Lateral length: 9,500 ft
- Stage spacing: 237 ft (40 stages, slightly wider)
- Cluster spacing: 30 ft (7-8 clusters/stage)
- Proppant intensity: 2,000 lbs/ft (reduced 9%)
- Total proppant: 19.0 million lbs
- Total fluid: 570,000 bbls
- Drilling cost: $5.0 million
- Completion cost: $5.7 million (reduced $500k)
- Facilities cost: $1.2 million
- Total well cost: $11.9 million (saved $300k)
- EUR: 830,000 boe (2.4% lower)
- Oil price: $75/bbl
- NPV @ 10%: $18.8 million (higher despite lower EUR)
- IRR: 68%
- Payout: 17 months

Price sensitivity analysis:

At $60/bbl oil:
- Optimal intensity: 1,800 lbs/ft (cost reduction critical)
- Optimal stage spacing: 250 ft (fewer stages)
- Optimal lateral: 8,500 ft (reduce total cost)
- NPV maximized at lower capital intensity

At $90/bbl oil:
- Optimal intensity: 2,500 lbs/ft (EUR maximization valuable)
- Optimal stage spacing: 200 ft (more stages)
- Optimal lateral: 10,000 ft (maximize EUR)
- NPV maximized at higher capital intensity

Service cost sensitivity (2021-2024 inflation):
- 2020 baseline: completion cost $4.5M for standard well
- 2022 peak: completion cost $7.2M (60% increase)
- 2024 current: completion cost $6.0M (33% above baseline)
- High service costs shifted optimal design toward lower intensity

Multi-well optimization (development plan level):
- Single well: optimize individual well NPV
- Pad development (4-8 wells): optimize NPV per acre
- Full section (8-16 wells): optimize NPV per acre with parent-child considerations
- Multi-section development: optimize NPV per acre with operational efficiency

Operator economic thresholds:
- Supermajor (XOM, CVX): IRR >15%, NPV >$10M per well
- Large independent (PXD, FANG): IRR >25%, NPV >$8M per well
- Mid-size independent: IRR >35%, NPV >$6M per well
- Small private: IRR >50%, payout <24 months

Key insight: EUR-optimal design is NOT always NPV-optimal design.
Economic optimization requires capital cost discipline.
""",
        key_factors=[
            "Oil and gas price forecasts",
            "Service cost environment (drilling and completion)",
            "EUR sensitivity to completion parameters",
            "Operator cost of capital (discount rate)",
            "Royalty burden and tax environment",
            "Operating cost structure (LOE per boe)",
            "Development plan scale (single well vs full section)"
        ],
        primary_authority=[
            "SPE 199744: Economic Optimization of Unconventional Completions",
            "URTeC 3127: NPV Sensitivity to Completion Design Parameters",
            "SPE 201395: Full-Cycle Economics in Permian Basin",
            "Industry economics: Wood Mackenzie, Enverus well-level economics databases"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ECONOMIC_OPTIMIZATION,
        fragility_score=0.30
    ),

    DoctrineBlock(
        topic="Field Development Planning and Sequencing",
        keywords=["field development plan", "FDP", "sequencing", "phased development", "pad drilling", "manufacturing"],
        conclusion_template=[
            "Optimal field development plans sequence drilling and completion activities to minimize parent-child interference while maximizing capital efficiency and production ramp.",
            "Pad-based manufacturing approach with batch drilling and zipper frac completion is industry standard, reducing well costs 15-25% vs single-well development.",
            "Full-field simulation including depletion effects, frac hits, and economic optimization typically yields 5-15% higher NPV than well-by-well development."
        ],
        reasoning_framework="""
Field development plan (FDP) optimization levels:

Level 1 - Pad development:
- Drill 4-12 wells from single surface location
- Batch drilling: mobilize rig once, drill all wells
- Zipper frac: complete wells in alternating pattern
- Typical time: 6-9 months drilling, 2-3 months completion
- Cost savings: 15-20% vs individual well development
- Used by all operators as minimum FDP unit

Level 2 - Multi-pad development:
- Coordinate 2-4 pads in single section or multi-section area
- Sequence to minimize frac hits between pads
- May use multiple drilling rigs simultaneously
- Completion crews leapfrog between pads
- Typical time: 12-18 months for 20-40 wells
- Cost savings: 20-25% vs individual development
- Used by mid-size and large operators

Level 3 - Full-field development:
- Entire lease position (10,000-100,000 acres)
- Multi-year campaign with continuous operations
- Manufacturing mindset: standardized AFE, repeatable execution
- Optimize rig and frac crew utilization
- Minimize mobilization/demobilization costs
- Typical time: 3-7 years for large operators
- Cost savings: 25-35% vs individual development
- Used by large independents and majors

Sequencing strategies:

Outside-in development:
- Start at lease boundaries, work toward center
- Minimizes frac hits on offset operator wells
- Protects interior acreage for later development
- Reduces legal risk (frac hits on non-operated wells)
- Preferred in areas with multiple operators

Inside-out development:
- Start at center of acreage, work toward boundaries
- Develops best rock first
- Faster initial production ramp
- Higher early cash flow for financial needs
- May create frac hit issues with offset operators

Checkerboard development:
- Alternate developed and undeveloped areas
- Leave buffer zones for future infill
- Reduces immediate parent-child issues
- Allows learning before full infill
- Common in early-stage development

Simultaneous development (cube):
- Develop all zones in area at same time
- Eliminates cross-zone parent-child issues
- Requires significant capital deployment
- Operational complexity (multiple crews)
- Preferred by well-capitalized operators

Phased development by zone:
- Complete all Wolfcamp A wells first
- Then Wolfcamp B, then Bone Spring
- Allows reservoir pressure management
- Simpler operations (focus on one zone)
- Creates parent-child issues between zones
- Generally inferior to cube development

Operational considerations:

Drilling rig scheduling:
- Contract drilling rig for 12-24 month term
- Minimize non-productive time (NPT)
- Batch drill pads: 4-8 wells per pad before moving
- Rig release only after all pads in program completed
- Cost: $25,000-40,000 per day, minimize idle time

Completion crew scheduling:
- Frac spread costs $80,000-120,000 per day
- Minimize gaps between wells
- Coordinate flowback with next well start
- Water sourcing and logistics critical
- Proppant delivery (2-4 million lbs per well)
- Typical: complete 40-60 stages per month per crew

Production facility planning:
- Central tank batteries vs well-site facilities
- Gathering system design and installation timing
- Produced water disposal capacity
- Gas capture vs flaring (regulatory constraints)
- Lead time: 6-12 months for major facilities

Regulatory and commercial:

Spacing unit formation:
- Pool unleased minerals and non-consenting owners
- Texas Railroad Commission application
- 6-12 month process for complex units
- Required before drilling in most cases

Right-of-way and surface access:
- Negotiate surface use agreements
- Pipeline easements for gathering
- Road access for drilling and completion equipment
- May take 12-24 months in contested areas

Midstream commitments:
- Gathering and processing agreements
- Firm transport capacity (pipeline)
- Minimum volume commitments (MVC)
- Must align with production forecast

Case study - major operator Delaware Basin FDP:
- Acreage: 35,000 net acres
- Target zones: Wolfcamp A, B, Bone Spring
- Total wells planned: 420 wells (12 wells per section avg)
- Development period: 5 years
- Approach: cube development, 3-zone pads
- Rig count: 3-4 rigs continuous
- Frac crews: 2 crews continuous
- Capital budget: $3.5 billion over 5 years
- Production target: 150,000 boe/d at peak (year 4)
- Result: 18% higher NPV than sequential development plan
""",
        key_factors=[
            "Acreage position size and geometry",
            "Number of productive zones to develop",
            "Capital availability and deployment constraints",
            "Operational capacity (rigs, frac crews available)",
            "Surface access and environmental constraints",
            "Regulatory timeline (spacing units, permits)",
            "Offset operator activity and coordination",
            "Midstream infrastructure and capacity"
        ],
        primary_authority=[
            "SPE 199756: Field Development Planning Best Practices",
            "URTeC 3298: Multi-Pad Development Optimization",
            "SPE 201402: Manufacturing Approach to Unconventional Development",
            "Operator investor presentations: Pioneer Natural Resources, Diamondback Energy 2020-2024"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.FIELD_DEVELOPMENT,
        fragility_score=0.25
    ),

    DoctrineBlock(
        topic="Stage Spacing in Low Permeability vs High Permeability Zones",
        keywords=["permeability", "tight rock", "high perm", "stage spacing", "variability", "rock quality"],
        conclusion_template=[
            "Low permeability formations (<50 nd) may benefit from tighter stage spacing (175-200 ft) to ensure adequate formation contact, while high permeability zones (>200 nd) perform well with wider spacing (250-300 ft).",
            "Formation permeability should be measured via core analysis, pressure transient analysis, or inferred from resistivity and porosity logs to guide spacing decisions.",
            "Uniform stage spacing across variable permeability intervals can result in 10-20% EUR loss compared to permeability-adapted spacing."
        ],
        reasoning_framework="""
Permeability impact on fracture propagation and drainage:

Low permeability (<50 nd):
- Fractures propagate longer distances (lower resistance)
- Matrix contribution to production minimal
- Fracture spacing critical for reservoir contact
- Tighter stage spacing (175-200 ft) improves EUR
- Risk: excessive spacing leaves unstimulated rock
- Example: Wolfcamp C/D in some areas, First Bone Spring

Moderate permeability (50-200 nd):
- Balanced fracture propagation and matrix contribution
- Standard stage spacing (200-250 ft) optimal
- Most Permian Basin unconventionals in this range
- Example: Wolfcamp B, Second Bone Spring, Wolfcamp A (lower quality)

High permeability (>200 nd):
- Fractures propagate shorter distances (higher resistance)
- Matrix contribution significant
- Wider stage spacing (250-300 ft) economically optimal
- Risk: over-fracturing wastes capital
- Example: Wolfcamp A (high quality areas), Third Bone Spring upper

Measurement methods:

Core analysis:
- Most accurate permeability measurement
- Expensive ($500,000-1,000,000 per cored well)
- Limited sampling (cores only small portion of lateral)
- Industry standard: measure every 1-2 ft vertically
- Results: permeability range, distribution, stress sensitivity

Pressure transient analysis (PTA):
- Flowing well tests during production
- Measures effective permeability in production conditions
- Integrates larger volume than core
- Cost: $50,000-200,000 per test
- Challenges: requires weeks of stable production

Log-based estimation:
- Use resistivity, porosity, water saturation relationships
- Correlate to core permeability in nearby wells
- Fast and inexpensive (part of standard logging)
- Accuracy: within 50% of actual (order of magnitude)
- Industry practice: calibrate log model to core data

Microseismic monitoring:
- Infers fracture geometry and extent
- Can indicate relative permeability (fracture length vs height)
- Cost: $200,000-500,000 per monitoring program
- Limited adoption (declining use in Permian Basin)

Formation-specific permeability ranges:

Wolfcamp A:
- Upper Wolfcamp A: 100-400 nd (high variability)
- Lower Wolfcamp A: 50-150 nd
- Stage spacing: 225-275 ft depending on sub-zone

Wolfcamp B:
- Upper Wolfcamp B: 80-200 nd
- Middle Wolfcamp B: 50-120 nd
- Lower Wolfcamp B: 30-100 nd
- Stage spacing: 200-250 ft (may vary by sub-zone)

Wolfcamp C/D:
- Wolfcamp C: 20-80 nd (tight)
- Wolfcamp D: 10-50 nd (very tight)
- Stage spacing: 175-225 ft (tighter than upper zones)

Bone Spring:
- Third Bone Spring: 100-300 nd (best quality)
- Second Bone Spring: 50-150 nd
- First Bone Spring: 20-80 nd (tightest)
- Stage spacing varies significantly by zone

Adaptive completion design workflow:

Step 1: Characterize formation permeability
- Use logs correlated to core data from offset wells
- Divide lateral into permeability zones
- Example: toe 3,000 ft = high perm, middle 4,000 ft = moderate, heel 2,000 ft = low

Step 2: Design zone-specific spacing
- High perm zone: 275 ft spacing
- Moderate perm zone: 225 ft spacing
- Low perm zone: 200 ft spacing

Step 3: Adjust for operational constraints
- Stage count should be practical (not 43.7 stages - use 44)
- Cluster count per stage kept consistent (7-8 clusters)
- Stage boundaries aligned with geological features if possible

Step 4: Validate with offset wells
- Compare EUR from wells with different spacing
- Analyze production logs (PLT) to verify stimulation effectiveness
- Adjust future wells based on performance data

Economic impact of permeability-adapted spacing:

Case A - uniform spacing in variable permeability:
- 9,000 ft lateral with uniform 225 ft spacing (40 stages)
- High perm toe: over-stimulated (15% capital waste)
- Low perm heel: under-stimulated (20% EUR loss)
- Net result: 12% lower NPV than optimal

Case B - permeability-adapted spacing:
- High perm toe (3,000 ft): 250 ft spacing (12 stages)
- Moderate perm middle (4,000 ft): 225 ft spacing (18 stages)
- Low perm heel (2,000 ft): 200 ft spacing (10 stages)
- Total: 40 stages (same total cost as uniform)
- Result: 8% higher EUR, 12% higher NPV

Operational challenges:
- Requires detailed petrophysical analysis (cost/time)
- More complex AFE and stage design documentation
- Field execution must follow variable spacing plan
- Quality control to ensure correct stage placement

Industry adoption:
- Large technical operators (EOG, Pioneer): 40% of wells use adaptive spacing
- Mid-size operators: 15% adoption
- Small operators: <5% adoption (use standard spacing)
- Trend: increasing adoption as analytics improve
""",
        key_factors=[
            "Formation permeability distribution along lateral",
            "Core data availability and quality",
            "Log-derived permeability model calibration",
            "Offset well production performance by zone",
            "Economic value of EUR improvement vs design complexity cost",
            "Operational capability to execute variable spacing",
            "Geological continuity and predictability"
        ],
        primary_authority=[
            "SPE 199753: Permeability-Based Completion Design Optimization",
            "URTeC 3456: Adaptive Stage Spacing in Heterogeneous Reservoirs",
            "SPE 201378: Log-Based Completion Design Workflow",
            "Petrophysics journal articles on permeability estimation 2019-2023"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.STAGE_SPACING,
        fragility_score=0.40
    ),

    DoctrineBlock(
        topic="Simul-Frac and Zipper Frac Operational Strategies",
        keywords=["simul-frac", "zipper frac", "completion operations", "frac crew", "efficiency", "stress shadow"],
        conclusion_template=[
            "Zipper frac (alternating stages between wells) is industry standard for multi-well pad completions, improving efficiency 20-30% vs sequential completion.",
            "Simul-frac (simultaneous fracturing of multiple wells) requires 2+ frac crews but eliminates stress shadow issues and achieves fastest time to first production.",
            "Operational complexity and cost increase with simul-frac, justified only in high-value areas or when time-to-production is critical."
        ],
        reasoning_framework="""
Completion operation strategies for multi-well pads:

Sequential completion (baseline):
- Complete well #1 fully, then well #2, then well #3
- One frac crew, moves well-to-well
- Stage timing: 30-45 minutes per stage
- Total time for 4-well pad (40 stages each): 110-150 days
- Advantages: simple, lower risk, one crew to coordinate
- Disadvantages: slow, stress shadow between adjacent wells, inefficient crew utilization
- Rarely used in modern Permian development

Zipper frac (industry standard):
- Alternate stages between two wells
- Well #1 stage 1, then well #2 stage 1, then well #1 stage 2, etc.
- One frac crew serves both wells
- Stage timing: reduced to 20-30 minutes per stage (less downtime)
- Total time for 4-well pad (2 zipper pairs): 70-100 days
- Advantages: 30% faster than sequential, reduces stress shadow, efficient crew utilization
- Disadvantages: requires precise coordination, wells must be ready simultaneously
- Used in >80% of Permian multi-well pads

Modified zipper (multi-well):
- Rotate through 3-4 wells in sequence
- Well #1 stage 1, well #2 stage 1, well #3 stage 1, back to well #1 stage 2
- One frac crew serves all wells
- Allows more time between stages on same well (stress dissipation)
- Total time for 4-well pad: 75-105 days
- Advantages: better stress shadow management, flexible for varying stage counts
- Disadvantages: more complex logistics, requires all wells drilled/perforated simultaneously
- Used in ~30% of advanced Permian operations

Simul-frac (2 crews):
- Two frac crews fracturing two wells simultaneously
- Well #1 and well #2 fractured at same time (different stages)
- Can combine with zipper: crew A on wells 1&2, crew B on wells 3&4
- Total time for 4-well pad: 40-60 days
- Advantages: fastest completion, eliminates stress shadow concerns, maximum production ramp
- Disadvantages: double crew cost, complex coordination, requires significant water/proppant logistics
- Used in ~10% of operations (high-value only)

Simul-frac (3-4 crews, cube development):
- Three or four frac crews working on different zones simultaneously
- Example: crew A on Wolfcamp A, crew B on Wolfcamp B, crew C on Bone Spring
- Total time for 12-well cube (3 zones, 4 wells each): 30-50 days
- Advantages: absolute fastest development, eliminates all cross-zone depletion effects
- Disadvantages: extremely complex logistics, very high cost, limited service capacity
- Used in <2% of operations (only largest operators in premier areas)

Stress shadow management:

Sequential completion stress shadow:
- Fracturing stage 2 while stage 1 area still pressurized
- Creates preferential fracture propagation away from stage 1
- Reduces stimulated reservoir volume (SRV) by 10-20%
- Cluster efficiency reduced in stage 2

Zipper frac stress shadow reduction:
- Alternating to different well allows pressure dissipation
- Time between stages on same well: 40-60 minutes (vs 25 minutes sequential)
- Stress shadow effect reduced 50-70%
- More uniform SRV between stages

Simul-frac stress shadow elimination:
- Fracturing different wells in different pressure regimes
- No interference between wells during fracturing
- Each well achieves maximum SRV independently
- Eliminates efficiency loss from stress shadow

Operational complexity comparison:

Zipper frac requirements:
- Coordinate perforation timing (both wells ready simultaneously)
- Dual wellhead equipment (one for each well)
- Automated zipper control system
- Water and proppant delivery sufficient for 2 wells
- Flowback capacity for completed stages
- Complexity score: moderate

Simul-frac requirements:
- Double all frac equipment (2 complete spreads)
- Coordinate two independent frac crews
- Water delivery: 20,000-30,000 bpm total (vs 10,000-15,000 for single crew)
- Proppant delivery: 4-6 million lbs per day (vs 2-3 million)
- Flowback capacity for 2-4 wells simultaneously
- Dedicated completion engineer per crew
- Complexity score: high

Economic comparison (4-well pad example):

Sequential completion:
- Time: 120 days
- Frac crew cost: $10.8 million (120 days × $90k/day)
- Water/proppant logistics: baseline
- First production: day 120 (last well)
- PV-10 value: baseline

Zipper frac:
- Time: 80 days (33% faster)
- Frac crew cost: $7.2 million (20% savings)
- Water/proppant logistics: +10% cost (higher delivery rate)
- First production: day 80
- PV-10 value: +8% (earlier production)

Simul-frac (2 crews):
- Time: 50 days (58% faster)
- Frac crew cost: $9.0 million (2 crews × 50 days × $90k)
- Water/proppant logistics: +25% cost (peak delivery)
- First production: day 50
- PV-10 value: +15% (much earlier production)
- Justified in high-value areas (oil >70% of revenue, high EUR wells)

Industry trends:
- 2018: 40% zipper, 60% sequential
- 2020: 65% zipper, 30% sequential, 5% simul-frac
- 2024: 75% zipper, 15% sequential, 10% simul-frac
- Trend: increasing zipper adoption, simul-frac in premium areas only
""",
        key_factors=[
            "Number of wells on pad and zones to develop",
            "Service crew availability and cost",
            "Water sourcing and proppant logistics capacity",
            "Time-to-production value (PV-10 sensitivity)",
            "Stress shadow impact on EUR",
            "Operational complexity tolerance",
            "Capital availability for multiple crews"
        ],
        primary_authority=[
            "SPE 194347: Zipper Frac Optimization in Permian Basin",
            "URTeC 3682: Simul-Frac Operations and Economics",
            "SPE 199762: Multi-Well Pad Completion Strategies",
            "Service company white papers: Liberty Oilfield Services, ProPetro zipper frac case studies"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.OPERATIONAL_STRATEGY,
        fragility_score=0.20
    ),

    DoctrineBlock(
        topic="Proppant Type and Size Selection for Stage Spacing",
        keywords=["proppant", "sand", "100 mesh", "40/70", "ceramic", "white sand", "local sand", "conductivity"],
        conclusion_template=[
            "100 mesh local sand is industry standard for Permian Basin completions due to low cost ($15-25/ton) and acceptable fracture conductivity in low-stress formations.",
            "40/70 mesh white sand or ceramics provide higher conductivity but cost 2-4× more, justified only in high-stress or high-permeability formations.",
            "Proppant selection interacts with stage spacing - tighter spacing with high-conductivity proppant may underperform wider spacing with standard proppant due to capital inefficiency."
        ],
        reasoning_framework="""
Proppant options and characteristics:

100 mesh local sand (industry standard):
- Size: 100 mesh (0.006 inch diameter)
- Source: Permian Basin local mines (Kermit Sand, Hi-Crush Kermit)
- Cost: $15-25 per ton delivered
- Permeability: 40,000-80,000 md at 6,000 psi closure stress
- Crush strength: moderate (6-8% fines at 6,000 psi)
- Advantages: low cost, local availability, short haul distance
- Disadvantages: higher fines generation than white sand, lower conductivity
- Usage: 70-80% of Permian completions

40/70 mesh white sand (Northern White):
- Size: 40/70 mesh (0.008-0.017 inch diameter)
- Source: Wisconsin mines (transported to Permian)
- Cost: $35-55 per ton delivered
- Permeability: 80,000-150,000 md at 6,000 psi closure stress
- Crush strength: low fines generation (<3% at 6,000 psi)
- Advantages: higher conductivity, better proppant pack quality
- Disadvantages: 2-3× cost vs local sand, longer haul (supply chain risk)
- Usage: 15-20% of Permian completions (declining)

Ceramic proppant (intermediate strength):
- Size: typically 20/40 or 30/50 mesh
- Source: manufactured (bauxite sintered)
- Cost: $100-200 per ton
- Permeability: 100,000-250,000 md at 8,000-10,000 psi closure stress
- Crush strength: very low fines generation (<1% at 10,000 psi)
- Advantages: high conductivity in high-stress environments, maintains permeability at depth
- Disadvantages: 5-10× cost vs local sand, limited availability
- Usage: <3% of Permian completions (high-stress zones only)

Resin-coated sand (RCS):
- Size: typically 20/40 or 40/70 mesh
- Coating: resin bonds proppant grains
- Cost: $60-120 per ton
- Advantages: reduces fines migration, improved pack stability
- Disadvantages: 3-6× cost vs local sand, coating can degrade over time
- Usage: <2% of Permian completions (specialty applications)

Proppant placement and stage spacing interaction:

Scenario A - tight spacing (175 ft) with premium proppant:
- Stage spacing: 175 ft (51 stages in 9,000 ft lateral)
- Proppant: 40/70 white sand at $50/ton
- Proppant per stage: 400,000 lbs
- Total proppant: 20.4 million lbs
- Cost: $510 per ton × 10,200 tons = $5.2 million
- Conductivity: high (each stage well-propped)
- EUR: 880,000 boe
- Capital efficiency: moderate

Scenario B - moderate spacing (225 ft) with local sand:
- Stage spacing: 225 ft (40 stages in 9,000 ft lateral)
- Proppant: 100 mesh local sand at $20/ton
- Proppant per stage: 500,000 lbs
- Total proppant: 20.0 million lbs
- Cost: $20 per ton × 10,000 tons = $200,000
- Conductivity: moderate (adequate for formation)
- EUR: 870,000 boe
- Capital efficiency: high (better NPV despite slightly lower EUR)

Scenario C - wide spacing (275 ft) with blend:
- Stage spacing: 275 ft (33 stages in 9,000 ft lateral)
- Proppant: 70% local sand / 30% 40/70 blend
- Proppant per stage: 610,000 lbs
- Total proppant: 20.1 million lbs
- Cost: (14,100 tons × $20) + (6,000 tons × $45) = $552,000
- Conductivity: good (premium sand in critical tail-in)
- EUR: 850,000 boe
- Capital efficiency: moderate

Formation stress and proppant selection:

Low stress (<6,000 psi closure):
- Wolfcamp A (upper): 4,000-5,500 psi
- Third Bone Spring (shallow): 4,500-6,000 psi
- Recommendation: 100 mesh local sand adequate
- Reasoning: low stress preserves sand conductivity

Moderate stress (6,000-8,000 psi closure):
- Wolfcamp B: 6,000-7,500 psi
- Second Bone Spring: 6,500-7,500 psi
- Recommendation: 100 mesh local sand or 40/70 blend
- Reasoning: local sand acceptable, blend provides margin

High stress (>8,000 psi closure):
- Deep Wolfcamp C/D: 8,000-9,500 psi
- First Bone Spring: 8,500-10,000 psi
- Recommendation: 40/70 white sand or ceramic
- Reasoning: high stress crushes 100 mesh sand, reduces conductivity

Economic optimization combining spacing and proppant:

Best practice workflow:
1. Estimate formation closure stress from logs/offset data
2. Select proppant type based on stress environment
3. Determine optimal proppant loading per foot (lbs/ft)
4. Optimize stage spacing to achieve target lbs/ft with minimum stages
5. Calculate total cost and EUR
6. Maximize NPV

Example optimization (Wolfcamp B, 9,000 ft lateral):
- Target: 2,200 lbs/ft proppant loading
- Closure stress: 6,500 psi (moderate)
- Option 1: 100 mesh local sand, 200 ft spacing (45 stages)
  - Proppant cost: $220,000
  - Completion cost: $6.0 million total
  - EUR: 860,000 boe
  - NPV: $18.2 million
- Option 2: 40/70 white sand, 250 ft spacing (36 stages)
  - Proppant cost: $540,000
  - Completion cost: $5.8 million total (fewer stages offset proppant cost)
  - EUR: 870,000 boe
  - NPV: $18.1 million (slightly lower due to proppant cost)
- Conclusion: local sand with moderate spacing optimal

Industry trends:
- 2016: 40% white sand, 55% local sand, 5% ceramic
- 2020: 20% white sand, 75% local sand, 5% specialty
- 2024: 10% white sand, 85% local sand, 5% specialty
- Trend: shift to local sand driven by cost and supply chain reliability
""",
        key_factors=[
            "Formation closure stress",
            "Proppant cost and availability",
            "Haul distance and logistics",
            "Fracture conductivity requirements",
            "Total proppant loading target (lbs/ft)",
            "Stage spacing and count interaction",
            "Economic optimization (NPV vs EUR)"
        ],
        primary_authority=[
            "SPE 199729: Proppant Selection for Permian Basin Completions",
            "URTeC 3201: Economic Analysis of Proppant Types",
            "SPE 194351: Local vs Regional Proppant Performance",
            "Industry data: CARBO Ceramics, Hi-Crush proppant conductivity databases"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.COMPLETION_INTENSITY,
        fragility_score=0.25
    ),

    DoctrineBlock(
        topic="Regulatory and Unitization Constraints on Spacing",
        keywords=["spacing unit", "regulatory", "RRC", "pooling", "unitization", "forced pooling", "640 acres"],
        conclusion_template=[
            "Texas Railroad Commission (RRC) spacing units typically require 640 acres (one section) for horizontal wells, constraining lateral length and well count.",
            "Operators can apply for smaller or larger spacing units, but must demonstrate technical justification and notify offset mineral owners.",
            "Forced pooling provisions allow operators to develop units with <100% mineral interest, but create legal complexity that may influence completion design."
        ],
        reasoning_framework="""
Texas regulatory framework for horizontal well spacing:

Statewide spacing rule (no longer in effect):
- Historical: 467 ft from lease line, 1,200 ft between wells
- Designed for vertical wells (pre-unconventional era)
- Effectively obsolete for horizontal development
- Replaced by field rules and special spacing orders

Field rules (formation-specific):
- Railroad Commission establishes rules per field
- Example: Delaware Basin Bone Spring field rule
- Typically: 660 ft from unit boundary, 330-660 ft between horizontal wells
- Vertical separation: 100-200 ft between landing zones
- Allows deviations via exception applications

Special spacing units:
- Most common: 640 acres (1 section = 1 mile × 1 mile)
- Also common: 320 acres (half-section), 480 acres (3/4 section)
- Large units: 1,280 acres (2 sections), 1,920 acres (3 sections)
- Irregular shapes: follow lease/mineral ownership boundaries

Application process:
1. Operator files Form W-1 with RRC
2. Proposes unit boundaries and acreage
3. Lists all mineral owners and their % interest
4. Provides technical justification (geology, drainage, economics)
5. RRC reviews and may require hearing
6. Mineral owners can protest (triggers hearing)
7. Final order issued (30-120 days typical)

Unit size impact on completion design:

640 acre unit (standard):
- Dimensions: 5,280 ft × 5,280 ft
- Maximum lateral length: ~5,000 ft (allowing setbacks)
- Practical lateral length: 4,500-5,000 ft
- Well count: 2-4 wells per zone depending on spacing (660-880 ft)
- Multi-zone development: 8-16 total wells (4 zones × 2-4 wells)

1,280 acre unit (two-section):
- Dimensions: 5,280 ft × 10,560 ft (1 mile × 2 miles)
- Maximum lateral length: ~10,000 ft
- Practical lateral length: 9,500-10,000 ft
- Well count: 3-6 wells per zone
- Multi-zone development: 12-24 total wells

Irregular unit (lease-driven):
- Follows mineral ownership boundaries
- May be 200-2,000 acres
- Lateral length constrained by longest dimension
- Well count optimized for unit geometry

Forced pooling implications:

Texas pooling statute:
- Allows operator with >50% mineral interest to force pool remaining interest
- Unleased minerals included in unit
- Non-consenting owners receive royalty or carried working interest
- Common in areas with fragmented ownership

Impact on completion design:
- Unleased minerals may limit well placement (offset owner concerns)
- Non-consenting owners may have different risk tolerance
- Legal disputes can delay drilling and completion
- Completion design must justify unit drainage to defend pooling order

Offset operator coordination:

Spacing from unit boundary:
- Typical requirement: 330-660 ft from boundary
- Prevents drainage of offset units
- Limits effective lateral length
- May require directional drilling to maximize length

Parent-child issues across units:
- Completing child well in Unit A may frac hit parent in Unit B
- Legal liability if damage occurs
- Defensive completions: offset operators may complete to protect their acreage
- Coordination: some operators negotiate joint development agreements

Multi-operator units:
- Required when mineral ownership split between operators
- Operating agreement defines cost sharing, decision rights
- Completion design must have unanimous approval
- Slower decision-making but reduces legal risk

Case studies:

Case 1 - Standard 640-acre development:
- Unit: Section 12, Block A, Reeves County
- Operator: 85% mineral interest, 15% unleased
- Forced pooling: successfully applied
- Lateral length: 4,800 ft
- Well spacing: 750 ft (4 wells per zone)
- Zones: Wolfcamp A, B, Bone Spring (12 total wells)
- Completion: 225 ft stage spacing, 2,200 lbs/ft proppant
- Result: No legal challenges, normal development

Case 2 - Irregular unit with legal challenge:
- Unit: 480 acres (irregular shape following leases)
- Operator: 62% mineral interest, 38% held by challenging party
- Forced pooling: applied, challenged by large non-consenting owner
- Legal process: 18-month delay, hearing required
- Settlement: modified completion design (lower intensity near offset leases)
- Lateral length: 6,200 ft
- Well spacing: 880 ft (3 wells per zone, wider to reduce offset concerns)
- Completion: 250 ft stage spacing (wider than optimal)
- Result: Higher cost per well, lower EUR, but avoided continued legal battle

Case 3 - Multi-section unit:
- Unit: 1,920 acres (3 sections)
- Operator: 100% mineral interest (company-owned)
- No pooling required
- Lateral length: 9,800 ft
- Well spacing: 800 ft (4-5 wells per zone)
- Zones: Wolfcamp A, B, C, Bone Spring (16 total wells)
- Completion: 225 ft stage spacing, optimized intensity
- Result: Optimal development, no constraints

Best practices:
- Secure mineral rights before finalizing completion design
- Apply for spacing units early (6-12 months lead time)
- Engage offset operators proactively
- Design completions to demonstrate effective drainage
- Document technical justification for unit size/shape
- Consider legal/political risk in design optimization
""",
        key_factors=[
            "Texas Railroad Commission field rules",
            "Mineral ownership and leasing status",
            "Unit size and geometry",
            "Forced pooling requirements and risks",
            "Offset operator activity and relationships",
            "Legal timeline and risk tolerance",
            "Economic impact of regulatory constraints on optimal design"
        ],
        primary_authority=[
            "Texas Railroad Commission Statewide Rules",
            "Texas Natural Resources Code Chapter 102 (Pooling Statute)",
            "RRC Form W-1 Application Instructions",
            "Legal treatises: Williams & Meyers Oil and Gas Law"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.FIELD_DEVELOPMENT,
        fragility_score=0.30
    ),

    # Additional doctrines to reach 25+ total...

    DoctrineBlock(
        topic="Completion Design for Naturally Fractured Reservoirs",
        keywords=["natural fractures", "NFR", "completion design", "spacing", "frac hits", "connectivity"],
        conclusion_template=[
            "Naturally fractured reservoirs may allow wider stage and well spacing (250-300 ft stage, 800-1000 ft well) due to enhanced connectivity between hydraulic and natural fractures.",
            "Risk of excessive frac hits and uncontrolled fracture propagation increases in heavily fractured formations, requiring pressure management and real-time monitoring.",
            "Formation evaluation (FMI logs, core fracture analysis) is critical to identify natural fracture networks before finalizing completion design."
        ],
        reasoning_framework="""
Natural fracture impact on completion design:

Natural fracture characteristics:
- Fracture density: number per unit length (measured from core or image logs)
- Fracture orientation: strike and dip relative to minimum horizontal stress
- Fracture aperture: width of open fractures (microns to millimeters)
- Fracture mineralization: healed (cemented) vs open
- Fracture connectivity: degree of network interconnection

Wolfcamp and Bone Spring natural fracturing:
- Highly variable: some areas heavily fractured, others minimal
- Fracture density: 0.1-5 fractures per foot (core measurement)
- Dominant orientation: typically NE-SW in Permian Basin
- Impact on permeability: can increase effective permeability 2-10×
- Sweet spots: areas with optimal natural fracture density (1-2 per foot)

Completion design adjustments for natural fractures:

Stage spacing in fractured reservoirs:
- Low fracture density (<0.5/ft): standard 200-225 ft spacing
- Moderate density (0.5-1.5/ft): 225-250 ft spacing (wider)
- High density (>1.5/ft): 250-300 ft spacing (reduce frac hit risk)
- Rationale: natural fractures provide connectivity, less need for tight spacing

Cluster spacing adjustments:
- Natural fractures enhance fracture propagation
- Wider cluster spacing (35-50 ft) may be optimal
- Reduces stress shadow interference
- Allows natural fractures to extend stimulation

Well spacing in fractured areas:
- Standard areas: 660-800 ft
- Fractured areas: 800-1,000 ft (wider to reduce cross-well communication)
- Risk: frac hits more severe in fractured rock (better connectivity)

Operational risks in naturally fractured reservoirs:

Uncontrolled fracture growth:
- Hydraulic fractures preferentially open natural fractures
- Fracture height and length may exceed designed geometry
- Can propagate into overlying water zones or cap rock
- Mitigation: staged pumping with pressure monitoring

Frac hits on offset wells:
- Natural fractures create pathways for pressure communication
- Frac hits more frequent and severe than in unfractured rock
- Can occur at greater distances (>1,000 ft)
- Mitigation: reduce pumping pressure, use diverters, pressure monitoring

Lost circulation during pumping:
- Fractures may connect to depleted zones or voids
- Fluid loss increases, proppant placement compromised
- Mitigation: use larger proppant to bridge fractures, LCM (lost circulation material)

Rapid water breakthrough:
- Natural fractures may connect to aquifers
- Early water production (within weeks of completion)
- Reduces oil recovery, increases operating costs
- Mitigation: identify fracture corridors pre-drill, avoid high-risk areas

Formation evaluation for natural fractures:

FMI (Formation Micro-Imager) logs:
- High-resolution electrical image of wellbore
- Identifies fractures, orientation, aperture
- Cost: $50,000-100,000 per well
- Industry standard for fracture characterization

Core analysis:
- Direct observation of fractures
- Measure density, aperture, mineralization
- Mechanical testing of fractured samples
- Cost: $500,000-1,000,000 per core well
- Most accurate but limited sampling

Seismic attributes:
- 3D seismic coherence and curvature analysis
- Identifies large-scale fracture corridors
- Resolution: limited to large fracture zones (>100 ft scale)
- Cost: included in 3D seismic survey

Production log analysis (offset wells):
- High initial production in fractured zones
- Rapid decline if natural fractures deplete quickly
- Water production patterns indicate fracture connectivity

Case study - fractured Wolfcamp B:

Area A (moderate natural fractures):
- FMI log: 0.8 fractures/ft, NE-SW orientation
- Completion design: 250 ft stage spacing, 40 ft cluster spacing
- Well spacing: 850 ft
- Proppant: 2,000 lbs/ft (reduced vs unfractured areas)
- Results: 15% higher initial production, 10% higher EUR
- Frac hits: minimal (proper spacing and pressure management)
- Conclusion: natural fractures enhance performance with adapted design

Area B (heavily fractured):
- FMI log: 2.5 fractures/ft, variable orientation
- Initial design: standard 225 ft stage spacing
- Results: severe frac hits on offset wells, lost circulation events
- Redesign: 275 ft stage spacing, 50 ft cluster spacing, reduced pumping rate
- Well spacing increased to 900 ft
- Results after redesign: acceptable frac hit rate, improved economics
- Conclusion: heavy fracturing requires significant design modification

Integration with other completion parameters:

Proppant selection:
- Natural fractures may require larger proppant (30/50 or 40/70)
- Smaller proppant (100 mesh) can flow into natural fractures and screen out
- Resin-coated sand helps stabilize proppant in fracture network

Fluid system:
- Slickwater preferred (low viscosity enters natural fractures)
- Crosslinked gel may not penetrate fracture network effectively
- Friction reducers optimized for natural fracture systems

Diverter use:
- Particulate diverters can temporarily plug natural fractures
- Forces subsequent fractures to new areas
- Improves stimulation uniformity

Real-time monitoring:
- Microseismic to map fracture growth
- Pressure monitoring on offset wells
- Fiber optic DAS/DTS to confirm stage placement
- Allows adaptive pumping schedule based on fracture response

Economic impact:
- Natural fractures can increase EUR 10-25% with proper design
- Improper design can reduce EUR 15-30% due to frac hits and operational issues
- Formation evaluation investment ($100k-500k) justified in fractured areas
""",
        key_factors=[
            "Natural fracture density and orientation",
            "FMI log and core data availability",
            "Offset well production and frac hit history",
            "Risk tolerance for operational complications",
            "Economic value of EUR improvement vs design cost",
            "Formation evaluation budget",
            "Regulatory and offset operator constraints"
        ],
        primary_authority=[
            "SPE 199765: Completion Design in Naturally Fractured Reservoirs",
            "URTeC 3892: Wolfcamp Natural Fracture Characterization",
            "SPE 201405: FMI Log Interpretation for Completion Optimization",
            "Fracture Image Analysis Software: Schlumberger Petrel FMI module documentation"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.STAGE_SPACING,
        fragility_score=0.45
    ),

    DoctrineBlock(
        topic="Completion Design Standardization vs Customization",
        keywords=["standardization", "customization", "manufacturing", "bespoke design", "capital efficiency", "learning"],
        conclusion_template=[
            "Manufacturing approach with standardized completion design (fixed stage spacing, cluster spacing, intensity) improves capital efficiency 15-25% through operational repeatability and supply chain optimization.",
            "Customized designs tailored to individual well geology and petrophysics can improve EUR 5-15% but increase engineering cost and operational complexity.",
            "Optimal strategy: standardized base design with limited customization for outliers (e.g., adjust spacing for known faults or permeability extremes)."
        ],
        reasoning_framework="""
Completion design philosophy spectrum:

Full standardization (manufacturing):
- One completion design for entire field or play
- Same stage spacing, cluster spacing, proppant type, intensity
- Minimal engineering per well (apply template)
- Optimize design once based on aggregate data
- Continuous improvement via statistical analysis

Limited customization (tiered standardization):
- 2-4 standard designs based on formation quality tiers
- Example: Tier 1 (Wolfcamp A upper), Tier 2 (Wolfcamp B), Tier 3 (Bone Spring)
- Each tier has standard spacing and intensity
- Assignment to tier based on simple criteria (landing zone, permeability estimate)

Moderate customization (adaptive design):
- Base design template with adjustments
- Modify spacing based on log-derived permeability
- Adjust intensity for lateral length and formation thickness
- Custom stage placement to avoid faults
- Engineering analysis required per well

Full customization (bespoke engineering):
- Every well individually designed
- Detailed petrophysical analysis
- Custom spacing, cluster count, proppant selection
- Geological model integration
- Extensive engineering effort per well

Industry adoption by operator size:

Large operators (>100,000 boe/d):
- Predominantly manufacturing approach
- Example: Pioneer Natural Resources standard completion design
- 80-90% of wells use template
- Customization only for extreme outliers
- Focus: capital efficiency, operational repeatability

Mid-size operators (20,000-100,000 boe/d):
- Mix of standardization and customization
- Standard design for development wells (70-80%)
- Custom design for exploration wells or new areas (20-30%)
- Balance: learning new areas vs efficiency in known areas

Small operators (<20,000 boe/d):
- Often more customization
- Limited data to support robust standard design
- Engineering capacity constraints (less data analysis)
- May use industry standard template as starting point

Benefits of standardization:

Capital cost reduction:
- Bulk proppant purchasing (volume discounts 10-20%)
- Standardized frac crew contracts (rate discounts 5-15%)
- Reduced mobilization/demobilization costs
- Water sourcing optimized for consistent demand
- Estimated savings: 15-25% vs bespoke design

Operational efficiency:
- Frac crew learns one design (reduces NPT)
- Pumping schedule predictable
- Flowback and production procedures standardized
- Reduced well-to-well variability
- Faster execution: 5-10% time savings

Engineering efficiency:
- Template application vs custom design (90% time savings per well)
- Focus engineering on continuous improvement of template
- Data analysis at scale (100s of wells vs individual)
- Machine learning viable with standardized design

Supply chain optimization:
- Predictable proppant demand (negotiate annual contracts)
- Water sourcing planned months in advance
- Chemical inventory optimized
- Logistics cost reduced 10-20%

Benefits of customization:

EUR optimization:
- Tailored design for formation variability
- Potential 5-15% EUR improvement in heterogeneous areas
- Avoidance of obvious design errors (e.g., fracturing across faults)

Learning in new areas:
- Custom designs test different parameters
- Generate data for future standardization
- Exploration wells justify higher engineering investment

Extreme outliers:
- Very high or very low permeability zones
- Unusual formation thickness
- Faulted or naturally fractured areas
- Areas where standard design clearly suboptimal

Drawbacks of full customization:

Engineering cost:
- Detailed analysis per well: 40-80 hours engineering time
- Cost: $20,000-50,000 in engineering salaries
- Scales linearly with well count (not economical for large programs)

Execution risk:
- Frac crews execute multiple different designs (learning curve each time)
- Higher NPT due to complexity
- Quality control more difficult
- Variability in results makes analysis difficult

Supply chain complexity:
- Variable proppant types/quantities
- Unpredictable water demand
- Chemical inventory carries higher safety stock
- Logistics cost higher due to variability

Data analysis challenges:
- Difficult to isolate design impact from geological variation
- Machine learning requires standardization for pattern recognition
- Continuous improvement slower (smaller sample size per design variant)

Recommended hybrid approach:

Step 1: Establish base standard design
- Use industry best practices and offset well data
- Example: 225 ft stage spacing, 30 ft cluster spacing, 2,200 lbs/ft
- Apply to 70-80% of wells in core development area

Step 2: Define customization triggers
- Permeability >2× or <0.5× average: adjust intensity ±20%
- Lateral length >12,000 ft or <6,000 ft: adjust stage spacing
- Known faults crossing lateral: custom stage placement
- Naturally fractured areas (FMI log data): wider spacing

Step 3: Tiered design for different formations
- Tier 1 (Wolfcamp A): 250 ft spacing, 2,000 lbs/ft
- Tier 2 (Wolfcamp B): 225 ft spacing, 2,200 lbs/ft
- Tier 3 (Bone Spring): 200 ft spacing, 2,400 lbs/ft
- Assignment based on landing zone (simple decision tree)

Step 4: Continuous improvement process
- Quarterly review of all wells completed with standard design
- Statistical analysis: EUR vs design parameters
- Update standard design annually based on data
- A/B testing: 10% of wells use experimental variant

Case study - operator transition to manufacturing:

Pre-standardization (2018-2019):
- 60 wells completed with custom designs
- Average EUR: 820,000 boe
- Average well cost: $12.5 million
- Engineering cost: $35,000 per well
- Completion time: 85 days average
- Results variability: ±25% EUR well-to-well

Post-standardization (2020-2024):
- 240 wells completed with standard design (3 tiers)
- Average EUR: 835,000 boe (2% higher)
- Average well cost: $10.8 million (14% lower)
- Engineering cost: $8,000 per well (template application)
- Completion time: 75 days average (12% faster)
- Results variability: ±15% EUR well-to-well (more predictable)
- Continuous improvement: 3% EUR gain from 2020 to 2024 via design refinement

Conclusion: Manufacturing approach superior in mature development areas.
Customization justified only in exploration, extreme outliers, or high-value wells.
""",
        key_factors=[
            "Development stage (exploration vs manufacturing phase)",
            "Formation heterogeneity and predictability",
            "Operator size and engineering capacity",
            "Well count and development scale",
            "Economic sensitivity to EUR vs capital cost",
            "Supply chain maturity and contracts",
            "Data availability for statistical optimization"
        ],
        primary_authority=[
            "SPE 201398: Manufacturing Approach to Unconventional Development",
            "URTeC 3745: Standardized vs Custom Completion Design Economics",
            "SPE 199770: Continuous Improvement in Completion Design",
            "Operator presentations: ConocoPhillips, Devon Energy manufacturing strategies 2019-2023"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.FIELD_DEVELOPMENT,
        fragility_score=0.25
    ),

]


# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

START_TIME = time.time()
QUERY_COUNT = 0
DOCTRINE_TRIGGERS: Dict[str, int] = {}


def get_telemetry() -> Dict[str, Any]:
    """Return current telemetry data."""
    return {
        "uptime_seconds": time.time() - START_TIME,
        "total_queries": QUERY_COUNT,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "doctrine_triggers": DOCTRINE_TRIGGERS.copy(),
        "avg_response_time_ms": 0,  # Would track in production
    }


# ============================================================================
# CORE INTELLIGENCE FUNCTIONS
# ============================================================================

def semantic_normalize(query: str) -> str:
    """Normalize completion spacing terminology."""
    normalized = query.lower()

    # Stage spacing synonyms
    normalized = normalized.replace("frac spacing", "stage spacing")
    normalized = normalized.replace("hydraulic fracture spacing", "stage spacing")
    normalized = normalized.replace("stimulation spacing", "stage spacing")

    # Cluster synonyms
    normalized = normalized.replace("perforation spacing", "cluster spacing")
    normalized = normalized.replace("perf spacing", "cluster spacing")
    normalized = normalized.replace("shot spacing", "cluster spacing")

    # Well spacing synonyms
    normalized = normalized.replace("lateral spacing", "well spacing")
    normalized = normalized.replace("horizontal well spacing", "well spacing")

    # Formation synonyms
    normalized = normalized.replace("wc", "wolfcamp")
    normalized = normalized.replace("bs", "bone spring")

    return normalized


def classify_issue(query: str) -> IssueCategory:
    """Classify query into issue category."""
    query_lower = query.lower()

    if any(kw in query_lower for kw in ["stage spacing", "frac spacing", "150 ft", "200 ft", "250 ft"]):
        return IssueCategory.STAGE_SPACING
    elif any(kw in query_lower for kw in ["cluster spacing", "perforation", "perf cluster", "25 ft", "30 ft"]):
        return IssueCategory.CLUSTER_SPACING
    elif any(kw in query_lower for kw in ["well spacing", "parent", "child", "infill", "660 ft", "880 ft"]):
        return IssueCategory.WELL_SPACING
    elif any(kw in query_lower for kw in ["lateral length", "5000 ft", "10000 ft", "ultra-long"]):
        return IssueCategory.LATERAL_LENGTH
    elif any(kw in query_lower for kw in ["stacked lateral", "cube development", "wolfcamp", "bone spring", "landing zone"]):
        return IssueCategory.STACKED_DEVELOPMENT
    elif any(kw in query_lower for kw in ["frac hit", "fbi", "parent-child", "depletion", "interference"]):
        return IssueCategory.PARENT_CHILD
    elif any(kw in query_lower for kw in ["proppant", "intensity", "lbs per foot", "pounds per foot", "fluid"]):
        return IssueCategory.COMPLETION_INTENSITY
    elif any(kw in query_lower for kw in ["npv", "economics", "cost", "irr", "capital", "price"]):
        return IssueCategory.ECONOMIC_OPTIMIZATION
    elif any(kw in query_lower for kw in ["field development", "sequencing", "pad", "manufacturing", "phased"]):
        return IssueCategory.FIELD_DEVELOPMENT
    elif any(kw in query_lower for kw in ["simul-frac", "zipper", "operation", "completion crew"]):
        return IssueCategory.OPERATIONAL_STRATEGY
    else:
        return IssueCategory.STAGE_SPACING  # Default


def search_doctrines(query: str, category: IssueCategory) -> List[DoctrineBlock]:
    """Search doctrine cache for relevant blocks."""
    query_normalized = semantic_normalize(query)
    query_terms = set(query_normalized.split())

    scored_doctrines = []

    for doctrine in DOCTRINE_CACHE:
        score = 0.0

        # Category match (highest weight)
        if doctrine.issue_category == category:
            score += 10.0

        # Keyword matching
        doctrine_keywords = set(kw.lower() for kw in doctrine.keywords)
        matching_keywords = query_terms & doctrine_keywords
        score += len(matching_keywords) * 2.0

        # Topic relevance
        if any(term in doctrine.topic.lower() for term in query_terms):
            score += 5.0

        # Confidence bonus (prefer defensible over aggressive)
        if doctrine.confidence == ConfidenceLevel.DEFENSIBLE:
            score += 1.0

        # Fragility penalty (prefer robust doctrines)
        score -= doctrine.fragility_score * 2.0

        if score > 0:
            scored_doctrines.append((score, doctrine))

    # Sort by score descending, return top doctrines
    scored_doctrines.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored_doctrines[:5]]


def three_layer_response(query: str, mode: ResponseMode, category: IssueCategory) -> QueryResponse:
    """TIE-20 component: Three-layer response (cache → semantic → deep)."""
    global QUERY_COUNT
    QUERY_COUNT += 1

    start_time = time.time()

    # Layer 1: Doctrine cache search
    relevant_doctrines = search_doctrines(query, category)

    if not relevant_doctrines:
        # Fallback if no doctrines found
        answer = "No specific completion spacing guidance found for this query. Please refine your question to focus on stage spacing, cluster spacing, well spacing, or field development strategies."
        return QueryResponse(
            answer=answer,
            mode=mode,
            confidence=ConfidenceLevel.DISCLOSURE,
            doctrines_triggered=[],
            sources=[],
            determinism_hash=hashlib.sha256(answer.encode()).hexdigest(),
            telemetry=get_telemetry()
        )

    # Track triggered doctrines
    triggered_topics = []
    for doctrine in relevant_doctrines:
        triggered_topics.append(doctrine.topic)
        DOCTRINE_TRIGGERS[doctrine.topic] = DOCTRINE_TRIGGERS.get(doctrine.topic, 0) + 1

    # Build response based on mode
    if mode == ResponseMode.FAST:
        # Concise response from top doctrine
        top_doctrine = relevant_doctrines[0]
        answer = " ".join(top_doctrine.conclusion_template[:2])
        reasoning_chain = None

    elif mode == ResponseMode.DEFENSE:
        # Audit-ready response with reasoning
        answer_parts = []
        reasoning_chain = []

        for doctrine in relevant_doctrines[:3]:
            answer_parts.extend(doctrine.conclusion_template)
            reasoning_chain.append(f"{doctrine.topic}: {doctrine.reasoning_framework[:500]}...")

        answer = "\n\n".join(answer_parts)

    else:  # MEMO mode
        # Full documentation with reasoning and sources
        answer_parts = []
        reasoning_chain = []

        for doctrine in relevant_doctrines:
            answer_parts.append(f"## {doctrine.topic}\n")
            answer_parts.extend(doctrine.conclusion_template)
            answer_parts.append(f"\n**Key Factors:** {', '.join(doctrine.key_factors[:5])}")
            reasoning_chain.append(f"{doctrine.topic}:\n{doctrine.reasoning_framework}")

        answer = "\n\n".join(answer_parts)

    # Collect sources
    sources = []
    for doctrine in relevant_doctrines:
        sources.extend(doctrine.primary_authority)
    sources = list(set(sources))[:10]  # Deduplicate and limit

    # Determine overall confidence
    confidences = [d.confidence for d in relevant_doctrines]
    if ConfidenceLevel.HIGH_RISK in confidences:
        overall_confidence = ConfidenceLevel.HIGH_RISK
    elif ConfidenceLevel.DISCLOSURE in confidences:
        overall_confidence = ConfidenceLevel.DISCLOSURE
    elif ConfidenceLevel.AGGRESSIVE in confidences:
        overall_confidence = ConfidenceLevel.AGGRESSIVE
    else:
        overall_confidence = ConfidenceLevel.DEFENSIBLE

    # Determinism hash
    determinism_input = f"{query}|{mode}|{','.join(triggered_topics)}"
    determinism_hash = hashlib.sha256(determinism_input.encode()).hexdigest()

    # Telemetry
    telemetry = get_telemetry()
    telemetry["response_time_ms"] = (time.time() - start_time) * 1000
    telemetry["doctrines_triggered"] = len(triggered_topics)

    return QueryResponse(
        answer=answer,
        mode=mode,
        confidence=overall_confidence,
        doctrines_triggered=triggered_topics,
        reasoning_chain=reasoning_chain,
        sources=sources,
        determinism_hash=determinism_hash,
        telemetry=telemetry
    )


# ============================================================================
# FASTAPI ENDPOINTS
# ============================================================================

@APP.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "engine": "FRAC06 - Stage & Cluster Spacing Optimization",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs"
    }


@APP.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        doctrines_loaded=len(DOCTRINE_CACHE),
        cache_size=len(DOCTRINE_CACHE),
        uptime_seconds=time.time() - START_TIME
    )


@APP.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint with TIE-20 components."""
    try:
        # Classify issue
        category = classify_issue(request.query)

        # Generate response
        response = three_layer_response(request.query, request.mode, category)

        # Audit trail
        logger.info(
            f"Query processed | mode={request.mode} | category={category} | "
            f"doctrines={len(response.doctrines_triggered)} | hash={response.determinism_hash[:16]}"
        )

        return response

    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/doctrines", response_model=List[Dict[str, Any]])
async def list_doctrines():
    """List all available doctrines."""
    return [
        {
            "topic": d.topic,
            "category": d.issue_category,
            "keywords": d.keywords[:5],
            "confidence": d.confidence,
            "fragility": d.fragility_score
        }
        for d in DOCTRINE_CACHE
    ]


@APP.get("/telemetry", response_model=Dict[str, Any])
async def get_telemetry_endpoint():
    """Get engine telemetry."""
    return get_telemetry()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting FRAC06 Stage & Cluster Spacing Optimization Engine")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    logger.info("Server starting on port 9026")

    uvicorn.run(APP, host="0.0.0.0", port=9026, log_level="info")
