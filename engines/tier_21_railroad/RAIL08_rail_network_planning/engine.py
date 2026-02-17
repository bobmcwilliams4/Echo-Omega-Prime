"""
RAIL08 Rail Network Planning Intelligence Engine
TIE-Grade Domain Expert System

Analyzes railroad network planning: capacity analysis, corridor studies,
intermodal terminal design, train dispatching optimization, and infrastructure
investment planning.

Port: 9214
Version: 1.0.0
Authority: FRA, AAR, AREMA, UIC, Class I railroads
"""

import sys
from pathlib import Path

# CRITICAL: Add parent to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field


# ============================================================================
# ENUMS AND CONSTANTS
# ============================================================================

class ResponseMode(str, Enum):
    """Response verbosity modes."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    """Epistemic confidence stratification."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class IssueCategory(str, Enum):
    """Rail network planning issue categories."""
    CAPACITY_ANALYSIS = "CAPACITY_ANALYSIS"
    CORRIDOR_PLANNING = "CORRIDOR_PLANNING"
    INTERMODAL_TERMINAL = "INTERMODAL_TERMINAL"
    DISPATCHING = "DISPATCHING"
    INFRASTRUCTURE_INVESTMENT = "INFRASTRUCTURE_INVESTMENT"
    YARD_DESIGN = "YARD_DESIGN"
    GRADE_CROSSING = "GRADE_CROSSING"
    CLEARANCE_REQUIREMENTS = "CLEARANCE_REQUIREMENTS"
    NETWORK_SIMULATION = "NETWORK_SIMULATION"
    SHORT_LINE_ECONOMICS = "SHORT_LINE_ECONOMICS"
    BENEFIT_COST_ANALYSIS = "BENEFIT_COST_ANALYSIS"
    TRAIN_PERFORMANCE = "TRAIN_PERFORMANCE"


class AnalysisZone(str, Enum):
    """Position zones to prevent disclosure mixing."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


BANNED_PHRASES = [
    "I am not a lawyer",
    "this is not legal advice",
    "consult a professional",
    "I cannot provide",
    "beyond my scope"
]


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """Network planning query request."""
    query: str = Field(..., min_length=10, description="Planning question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis zone")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class DoctrineBlock(BaseModel):
    """Pre-compiled domain expertise block."""
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: Optional[str] = None
    adversary_position: Optional[str] = None
    counter_arguments: List[str] = Field(default_factory=list)
    resolution_strategy: Optional[str] = None
    entity_scope: Optional[str] = None
    confidence: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE
    controlling_precedent: Optional[str] = None


class TelemetryData(BaseModel):
    """Query execution telemetry."""
    query_hash: str
    mode: ResponseMode
    zone: AnalysisZone
    cache_hit: bool
    semantic_search_ms: Optional[float]
    deep_analysis_ms: Optional[float]
    total_ms: float
    doctrines_triggered: List[str]
    confidence: ConfidenceLevel
    determinism_hash: str


class HealthResponse(BaseModel):
    """Engine health status."""
    engine: str
    version: str
    status: str
    port: int
    uptime_seconds: float
    queries_processed: int
    cache_size: int
    avg_response_ms: float
    error_rate: float


class QueryResponse(BaseModel):
    """Network planning analysis response."""
    answer: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    doctrines_applied: List[str]
    key_factors: List[str]
    authority_citations: List[str]
    telemetry: TelemetryData
    determinism_hash: str
    timestamp: str


# ============================================================================
# DOCTRINE CACHE - REAL DOMAIN EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    # Capacity Analysis
    DoctrineBlock(
        topic="UIC 406 Line Capacity Methodology",
        keywords=["capacity", "UIC 406", "line utilization", "compression factor", "timetable"],
        conclusion_template="Line capacity per UIC 406: theoretical capacity C = 1440/T (trains/day), practical capacity = 0.7*C for mixed traffic, 0.8*C for freight-only. {corridor} shows {utilization}% utilization with {compression} compression factor.",
        reasoning_framework="""UIC 406 Capacity Analysis Framework:

1. THEORETICAL CAPACITY CALCULATION
   - Minimum headway time T (minutes) between trains
   - C_theoretical = 1440 minutes/day / T
   - Example: T=10 min → C=144 trains/day
   - T depends on signal spacing, train speed, braking distance

2. PRACTICAL CAPACITY REDUCTION
   - Mixed passenger/freight: 60-70% of theoretical
   - Freight-only: 75-80% of theoretical
   - High-speed passenger: 70-75% of theoretical
   - Compression factor accounts for scheduling conflicts

3. CAPACITY CONSUMPTION FACTORS
   - Train speed heterogeneity (fast vs slow trains)
   - Station dwell times and schedule recovery time
   - Single-track sections (meet/pass requirements)
   - Track maintenance windows (reduces available time)
   - Peak directional flows vs bidirectional balance

4. BOTTLENECK IDENTIFICATION
   - Signal spacing inadequacies (increases T)
   - Grade crossings causing speed restrictions
   - Single-track chokepoints in double-track corridor
   - Terminal/yard throat congestion
   - Insufficient siding length for meets

5. CAPACITY EXPANSION STRATEGIES
   - Reduce headway T via advanced signaling (CBTC, ETCS)
   - Add second main track (doubles practical capacity)
   - Lengthen sidings for longer trains/more meets
   - Separate passenger/freight on parallel tracks
   - Optimize train scheduling (reduce compression)

6. SIMULATION VALIDATION
   - RailSys or OpenTrack timetable simulation
   - Monte Carlo analysis of delay propagation
   - Sensitivity to heterogeneity and dwell times
   - Verification against actual operations data

UIC 406 is the international standard. U.S. Class I railroads use proprietary
variants but fundamental principles remain: headway time T, theoretical vs
practical capacity, compression factor, and bottleneck analysis.""",
        key_factors=[
            "Minimum headway time T",
            "Compression factor for mixed traffic",
            "Bottleneck locations",
            "Signal spacing adequacy",
            "Heterogeneity penalty (fast vs slow)"
        ],
        primary_authority=[
            "UIC Code 406 - Capacity (2013)",
            "AREMA Manual Chapter 6 - Railway Engineering",
            "TRB TCRP Report 13 - Rail Transit Capacity"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All rail corridors worldwide"
    ),

    DoctrineBlock(
        topic="Train Performance Calculation (TPC Curves)",
        keywords=["TPC", "train performance", "ruling grade", "horsepower per ton", "resistance"],
        conclusion_template="Train performance on {grade}% grade: HPT requirement {hpt}, maximum tonnage {tonnage} tons, velocity {speed} mph. Davis equation resistance: R = 1.3 + 29/W + 0.045*V + 0.0005*AV^2.",
        reasoning_framework="""Train Performance Calculation Framework:

1. DAVIS EQUATION FOR TRAIN RESISTANCE
   - R = 1.3 + 29/W + 0.045*V + 0.0005*AV^2 (lb/ton)
   - W = weight per axle (tons)
   - V = velocity (mph)
   - A = cross-sectional area (sq ft) / tons
   - Covers journal friction, flange contact, air resistance

2. RULING GRADE DETERMINATION
   - Steepest sustained grade in corridor (typically 1-2%)
   - Limits maximum train tonnage for given HP
   - Compensated grade accounts for curvature: G_comp = G + 0.04*D
   - D = degree of curvature; 0.04% per degree rule

3. HORSEPOWER PER TON (HPT) CALCULATION
   - HPT = (G + R) * V / 375
   - G = grade (%), R = resistance (lb/ton), V = speed (mph)
   - Example: 1% grade, 5 lb/ton resistance, 25 mph → HPT = 0.4
   - Modern AC traction locos: 4000-4500 HP, ~140 tons = 30 HPT

4. MAXIMUM TONNAGE CALCULATION
   - T_max = (Total HP * Adhesion Factor) / (G + R) / V * 375
   - Adhesion factor ~0.25-0.35 depending on rail conditions
   - Dynamic braking capacity also limits downhill tonnage

5. VELOCITY-GRADE TRADEOFF
   - Higher grade → lower speed to maintain drawbar pull
   - Momentum operation: accelerate before grade, coast up
   - Distributed power units (DPU) improve train handling

6. SIMULATION AND VALIDATION
   - Train Performance Calculator (TPC) software
   - Train Energy Model (TEM) for fuel consumption
   - Field validation with dynamometer car tests
   - GPS-based actual vs predicted performance

Critical for: corridor feasibility (can we run desired tonnage?), locomotive
assignment (how many units needed?), schedule planning (realistic transit times),
fuel budgeting, and infrastructure investment (reduce ruling grade?).""",
        key_factors=[
            "Davis equation resistance",
            "Ruling grade and compensated grade",
            "Horsepower per ton (HPT)",
            "Adhesion limits",
            "Distributed power configuration"
        ],
        primary_authority=[
            "AAR Manual of Standards and Recommended Practices",
            "AREMA Manual Chapter 5 - Track Design",
            "Hay, W.W. - Railroad Engineering (1982)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All freight and passenger rail systems"
    ),

    DoctrineBlock(
        topic="Intermodal Terminal Capacity and Design",
        keywords=["intermodal", "terminal", "crane productivity", "dwell time", "double-stack"],
        conclusion_template="Intermodal terminal capacity: {cranes} cranes at {lifts} lifts/hour = {capacity} containers/day. Requires {tracks} working tracks, {storage} TEU ground storage, truck turn time < {turn} minutes.",
        reasoning_framework="""Intermodal Terminal Design Framework:

1. CRANE PRODUCTIVITY ANALYSIS
   - Rubber-tired gantry (RTG): 25-30 lifts/hour
   - Rail-mounted gantry (RMG): 30-35 lifts/hour
   - Top-pick reach stacker: 8-12 lifts/hour (lower cost)
   - Capacity = Cranes * Lifts/Hour * Operating Hours
   - Example: 4 RTGs * 28 lifts/hr * 16 hrs = 1,792 lifts/day

2. WORKING TRACK REQUIREMENTS
   - One working track per crane (minimum)
   - Track length = train length + locomotive escape
   - Typical: 8,000-10,000 ft for double-stack trains
   - Double-ended operations require two access points

3. CONTAINER STORAGE LAYOUT
   - Ground slots: 1 TEU = 8 ft x 20 ft footprint
   - Stack height: 3-4 high for reach stackers, 5-6 for RTGs
   - Dwell time: 2-5 days average (import/export balance)
   - Peak storage = (Daily Volume * Dwell Days) / Turnover

4. TRUCK GATE OPERATIONS
   - Turn time: 20-40 minutes target (arrival to departure)
   - Gate lanes: 1 lane per 50-75 trucks/hour
   - Chassis pool: 1.2-1.5 chassis per container on terminal
   - RFID/OCR automation reduces gate transaction time

5. RAIL ACCESS AND SWITCHING
   - Lead track capacity for inbound/outbound cuts
   - Switching time: 2-4 hours per train
   - Class I interchange: daily or multiple times per day
   - On-terminal switching loco(s) required

6. FACILITY EXPANSION PLANNING
   - Horizontal expansion: add tracks and storage area
   - Vertical expansion: taller stacks (requires RMG/ASC)
   - Technology: automated stacking cranes (ASC) → 40+ lifts/hr
   - Near-dock rail reduces drayage costs (LA/LB model)

Design drivers: container volume forecast, train frequency, import/export mix,
chassis availability, and truck gate transaction time. Sub-40 minute truck
turns critical for competitive positioning vs pure truck transload.""",
        key_factors=[
            "Crane type and productivity",
            "Working track length and quantity",
            "Container dwell time",
            "Truck turn time",
            "Chassis pool sizing"
        ],
        primary_authority=[
            "ASCE Port and Harbor Engineering",
            "Intermodal Association of North America (IANA) Standards",
            "TRB NCFRP Report 4 - Intermodal Connectors"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All intermodal rail terminals"
    ),

    DoctrineBlock(
        topic="Centralized Traffic Control (CTC) Dispatching Optimization",
        keywords=["CTC", "dispatching", "train order", "meet planning", "velocity optimization"],
        conclusion_template="CTC dispatching on {corridor}: optimize meets to minimize total delay. Priority trains: {priority}, velocity equalization reduces conflicts by {reduction}%, simulation shows {meets} optimal meet locations.",
        reasoning_framework="""CTC Dispatching Optimization Framework:

1. SINGLE-TRACK MEET/PASS PLANNING
   - Two trains approaching: one must take siding
   - Decision factors: train priority, velocity, siding location
   - Minimize total delay-minutes (sum of both trains)
   - Rule: faster train should meet slower train at siding

2. DOUBLE-TRACK DIRECTIONAL OPERATIONS
   - Typically: Track 1 westbound, Track 2 eastbound
   - Reduces conflicts but limits flexibility
   - Crossovers allow reverse running (maintenance, unbalanced flow)
   - Fleeting: group trains in same direction to minimize crossovers

3. TRAIN PRIORITY HIERARCHY
   - Passenger > Intermodal > Manifest > Unit train > Local
   - Class I railroads use computer-aided dispatching (CAD)
   - Network optimization considers downstream impacts
   - Delay costs: passenger $500+/min, freight $50-150/min

4. VELOCITY HOMOGENIZATION
   - Mixed speeds (70 mph passenger, 40 mph freight) consume capacity
   - Slowing fast trains reduces conflicts but increases transit time
   - Speeding slow trains (lighter loads, more HP) reduces heterogeneity
   - Optimal: minimize speed variance while meeting customer commitments

5. SIGNAL SYSTEM INTERACTION
   - Automatic Block Signal (ABS): fixed blocks, ~2-mile spacing
   - CTC: dispatcher controls signals remotely
   - Positive Train Control (PTC): enforces speed restrictions, prevents collisions
   - Moving block (future): reduces headway, increases capacity

6. SIMULATION-BASED DISPATCH PLANNING
   - RailSim/OpenTrack: test dispatch strategies offline
   - Monte Carlo analysis: delay propagation under uncertainty
   - Real-time dispatching: adjust plan based on actual train positions
   - Machine learning: predict optimal meets from historical data

Dispatching is an art and science. Experienced dispatchers develop intuition
for optimal meets, but simulation and optimization algorithms (linear programming,
genetic algorithms) can find better solutions, especially on complex networks
with many trains and sidings.""",
        key_factors=[
            "Train priority hierarchy",
            "Meet/pass location optimization",
            "Velocity homogenization",
            "Signal system capabilities",
            "Real-time vs planned dispatching"
        ],
        primary_authority=[
            "AAR Operating Rules",
            "FRA Track Safety Standards (49 CFR 213)",
            "AREMA Communications & Signals Manual"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All CTC-controlled rail corridors"
    ),

    DoctrineBlock(
        topic="Benefit-Cost Analysis for Rail Infrastructure Investment",
        keywords=["BCA", "benefit-cost", "NPV", "TIGER grants", "FRA guidance"],
        conclusion_template="Rail infrastructure BCA: {project} has NPV ${npv}M, BCR {bcr}, IRR {irr}%. Benefits: {benefits}, costs: {costs}. Meets FRA/FTA threshold of BCR > 1.0.",
        reasoning_framework="""Rail Infrastructure Benefit-Cost Analysis Framework:

1. COST COMPONENTS
   - Capital costs: design, ROW acquisition, construction, equipment
   - Operating costs: maintenance, labor, energy, insurance
   - Residual value: asset value at end of analysis period (typically 30 years)
   - Cost escalation: 3-5% annual inflation for construction costs

2. BENEFIT CATEGORIES
   - Travel time savings: freight velocity improvement, passenger trip time
   - Operating cost savings: fuel, crew, equipment utilization
   - Safety improvements: accident reduction (FRA accident cost database)
   - Environmental: emissions reduction, noise reduction
   - Economic development: job creation, induced investment (use cautiously)

3. DISCOUNT RATE SELECTION
   - OMB Circular A-94: 7% real discount rate for public investments
   - FRA/FTA: 3% and 7% sensitivity analysis required
   - Lower rate → higher NPV (future benefits valued more)
   - Private investors: 10-15% hurdle rate

4. BENEFIT-COST RATIO (BCR) CALCULATION
   - BCR = PV(Benefits) / PV(Costs)
   - BCR > 1.0 → economically justified
   - BCR > 2.0 → highly competitive for federal grants
   - TIGER/INFRA/CRISI grants prioritize high BCR projects

5. SENSITIVITY AND RISK ANALYSIS
   - Traffic growth uncertainty: low/base/high scenarios
   - Cost overrun risk: construction contingency 15-30%
   - Benefit realization risk: ridership/tonnage may not materialize
   - Monte Carlo simulation for probabilistic BCR distribution

6. INDUCED DEMAND AND WIDER ECONOMIC IMPACTS
   - Improved rail capacity may induce new freight/passenger demand
   - Regional economic impacts (jobs, GDP) hard to quantify rigorously
   - FRA skeptical of overly optimistic multiplier effects
   - Conservative approach: count only direct user benefits

Typical BCR thresholds: grade separation (1.5-3.0), double-tracking (1.2-2.5),
intermodal terminal (1.0-2.0), positive train control (0.5-1.0 - mandated by law
regardless). Travel time and safety benefits are most defensible; economic
development benefits are speculative and heavily discounted by FRA reviewers.""",
        key_factors=[
            "Capital and operating costs",
            "Travel time and safety benefits",
            "Discount rate (3% vs 7%)",
            "Traffic growth scenarios",
            "Benefit-cost ratio (BCR)"
        ],
        primary_authority=[
            "FRA Benefit-Cost Analysis Guidance (2021)",
            "OMB Circular A-94",
            "FTA Capital Investment Grant (CIG) Program Guidance"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All federally-funded rail infrastructure projects"
    ),

    DoctrineBlock(
        topic="Double-Stack Clearance Requirements",
        keywords=["double-stack", "clearance", "Plate H", "vertical clearance", "tunnel modification"],
        conclusion_template="Double-stack clearance requires {clearance} ft vertical clearance (Plate H). Existing corridor has {current} ft. Modifications: {tunnels} tunnel raises, {bridges} bridge raises, cost ${cost}M.",
        reasoning_framework="""Double-Stack Clearance Analysis Framework:

1. CLEARANCE PLATE STANDARDS
   - Plate C: standard boxcar (15 ft 1 in. above rail)
   - Plate H: double-stack (20 ft 2 in. above rail)
   - Plate K: high-cube double-stack (20 ft 9 in.)
   - Vertical: top of rail to overhead obstruction
   - Horizontal: centerline of track to lateral obstruction

2. CRITICAL OBSTRUCTION TYPES
   - Tunnels: most expensive to modify (raise floor, lower track)
   - Overhead bridges: raise bridge or lower track (easier than tunnel)
   - Signal bridges: relocate to side-mounted signals
   - Catenary: electrified railroads (incompatible with double-stack)
   - Rock cuts: blast/excavate additional vertical clearance

3. TUNNEL MODIFICATION STRATEGIES
   - Lower track bed (notching): 6-12 inch reduction via ballast removal
   - Tunnel floor lowering: excavate below ties (expensive, slow)
   - Tunnel ceiling raise: jack and reinforce tunnel roof (very expensive)
   - New bore: parallel tunnel (most expensive, last resort)
   - Typical cost: $5-50M per tunnel depending on length and method

4. BRIDGE MODIFICATION STRATEGIES
   - Raise bridge deck: expensive if approaches must be regraded
   - Lower track under bridge: create vertical sag (drainage issues)
   - Replace bridge with higher clearance structure
   - Typical cost: $1-10M per bridge

5. ECONOMIC JUSTIFICATION
   - Double-stack reduces cost per container by 30-40% vs single-stack
   - Required for competitive intermodal service (BNSF, UP standard)
   - Corridor must have sufficient traffic density to justify investment
   - Break-even: typically 500,000+ containers/year

6. ROUTE SELECTION AND ALTERNATIVES
   - Identify lowest-cost route with fewest obstructions
   - May route around mountains vs through tunnels
   - Ex: BNSF Southern Transcon (double-stack) vs northern route (restricted)
   - Short line railroads often cannot justify double-stack investment

U.S. Class I railroads prioritized double-stack clearance in 1980s-2000s. Most
mainline routes now accommodate Plate H. Remaining restrictions are eastern
railroads with old tunnels (CSX, NS) - multi-billion dollar issue. Short lines
serving intermodal terminals must coordinate with Class I clearance standards.""",
        key_factors=[
            "Plate H clearance (20 ft 2 in.)",
            "Tunnel modification costs",
            "Bridge raise vs track lowering",
            "Traffic density justification",
            "Route alternative analysis"
        ],
        primary_authority=[
            "AAR Plate Diagrams (Manual of Standards)",
            "AREMA Manual Chapter 28 - Clearances",
            "FRA Track Safety Standards (49 CFR 213)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All rail corridors seeking double-stack capability"
    ),

    DoctrineBlock(
        topic="Rail Yard Classification and Design",
        keywords=["classification yard", "hump yard", "flat switching", "retarder", "bowl tracks"],
        conclusion_template="Classification yard design: {type} yard with {tracks} classification tracks, {capacity} cars/day throughput. Hump yards require {gradient}% grade, {retarders} retarders, automation level {automation}.",
        reasoning_framework="""Rail Yard Classification Design Framework:

1. YARD TYPES AND SELECTION
   - Flat yard: locomotive-switched, low throughput (<500 cars/day)
   - Hump yard: gravity-switched, high throughput (1500-3000 cars/day)
   - Automated hump: radar-controlled retarders, minimal crew
   - Receiving/departure/classification track separation

2. HUMP YARD DESIGN PARAMETERS
   - Hump height: 18-24 ft above bowl tracks
   - Bowl track gradient: 0.2-0.4% for car rollout
   - Retarders: 2-3 positions (primary, secondary, trim)
   - Classification tracks: 40-80 tracks typical for major yards
   - Track length: 4,000-8,000 ft for unit train blocks

3. THROUGHPUT CAPACITY CALCULATION
   - Humping rate: 1-2 cars/minute (manual), 2-3 cars/min (automated)
   - Daily capacity = Rate * Operating Hours
   - Example: 2 cars/min * 18 hrs/day * 60 min/hr = 2,160 cars/day
   - Receiving/departure track capacity must match humping rate

4. RETARDER TECHNOLOGY
   - Master retarder: slows all cars after hump crest
   - Group retarder: groups cars by destination track
   - Trim retarder: final speed control before coupling
   - Radar-based weight/velocity sensing for automation
   - Hydraulic vs pneumatic retarders (hydraulic more precise)

5. SWITCHING LEAD AND LADDER DESIGN
   - Switching lead: 3,000+ ft for cut assembly
   - Ladder: series of turnouts to classification tracks
   - Turnout spacing: 30-50 ft centers
   - Crossovers: allow flexible routing and escape tracks

6. OPERATIONAL CONSIDERATIONS
   - Car inspection and repair facilities adjacent to bowl
   - Inbound train inspection before humping (bad order cars)
   - Outbound train assembly and air brake test
   - Intermodal/unit trains often bypass classification yard

Major U.S. hump yards: Bailey Yard (North Platte, UP - world's largest), Clearing
Yard (Chicago, BNSF), Conway Yard (Pittsburgh, NS). Many Class I railroads have
closed smaller hump yards due to Precision Scheduled Railroading (PSR) emphasis
on run-through trains and reduced classification. Hump yards are capital-intensive
but essential for manifest freight networks.""",
        key_factors=[
            "Hump vs flat yard selection",
            "Classification track quantity and length",
            "Retarder automation level",
            "Throughput capacity (cars/day)",
            "Receiving/departure track balance"
        ],
        primary_authority=[
            "AREMA Manual Chapter 5 - Yard and Terminal Design",
            "AAR Interchange Rules (Field Manual)",
            "Fröidh, O. - Rail Yard Simulation and Optimization"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All rail classification yards"
    ),

    DoctrineBlock(
        topic="Grade Crossing Elimination and Priority Ranking",
        keywords=["grade crossing", "separation", "FRA priority", "accident prediction", "quiet zone"],
        conclusion_template="Grade crossing {crossing_id}: {accidents} accidents, USDOT# {usdot}, priority index {priority}. Recommend {solution} (cost ${cost}M). Quiet zone requires {requirements}.",
        reasoning_framework="""Grade Crossing Elimination Framework:

1. FRA ACCIDENT PREDICTION MODEL
   - Accident frequency = K * (Train Count * Vehicle Count) ^ 0.5
   - K factor depends on crossing characteristics: gates, lights, passive
   - Higher train/vehicle counts → exponentially higher risk
   - National average: 1 accident per 200,000 exposure units

2. USDOT CROSSING INVENTORY
   - Every public crossing has unique USDOT number
   - Data: train count, vehicle count, protection type, surface type
   - Updates via FRA crossing inventory database (publicly accessible)
   - Accident history: past 10 years of incidents and fatalities

3. PRIORITY RANKING METHODOLOGY
   - Hazard Index = (Train * Vehicle) * Protection Factor
   - Cost-benefit: accident cost avoided vs separation cost
   - Community impact: school bus routes, emergency vehicle access
   - Federal funding: CRISI grants prioritize high-hazard crossings

4. SEPARATION ALTERNATIVES
   - Grade separation: overpass or underpass ($5-20M)
   - Crossing closure: reroute traffic (cheapest if viable)
   - Upgraded protection: add gates/lights ($250K-$500K)
   - Quiet zone: requires supplemental safety measures (see below)

5. QUIET ZONE REQUIREMENTS (FRA Rule)
   - No routine train horn (24 CFR 222)
   - Requires: four-quadrant gates OR median barriers OR road closure
   - Risk assessment: demonstrate no significant risk increase
   - Community desire: noise reduction near residential areas
   - Cost: $500K-$2M per crossing for supplemental safety measures

6. DESIGN STANDARDS FOR GRADE SEPARATION
   - Vertical clearance: 23 ft minimum over roadway
   - Horizontal clearance: 16 ft from centerline of track
   - Railroad overpass: road goes under (cheaper, railroad prefers)
   - Railroad underpass: road goes over (more expensive, drainage issues)
   - ADA compliance: ramps, elevators for pedestrian access

High-priority crossings: >20 trains/day, >5,000 vehicles/day, history of accidents,
school bus routes, no gates/lights. FRA CRISI grants fund ~$100-200M/year for
crossing elimination. State DOTs also fund via rail safety programs. Typical
cost-benefit threshold: $10M separation justified if prevents 1-2 fatal accidents
over 20 years (statistical value of life ~$10M per FRA guidance).""",
        key_factors=[
            "FRA accident prediction formula",
            "USDOT crossing inventory data",
            "Hazard index and priority ranking",
            "Grade separation vs closure vs upgrade",
            "Quiet zone supplemental safety requirements"
        ],
        primary_authority=[
            "FRA Grade Crossing Safety Regulations (49 CFR 222)",
            "MUTCD Part 8 - Railroad Crossings",
            "FHWA Highway-Rail Crossing Handbook"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All highway-rail grade crossings in U.S."
    ),

    DoctrineBlock(
        topic="Network Simulation with RailSys and OpenTrack",
        keywords=["RailSys", "OpenTrack", "simulation", "timetable", "delay propagation"],
        conclusion_template="Network simulation using {software}: {trains} trains, {hours} simulation hours. Results: {utilization}% capacity utilization, {delays} delay-minutes, bottleneck at {location}.",
        reasoning_framework="""Rail Network Simulation Framework:

1. SIMULATION SOFTWARE SELECTION
   - RailSys: European standard, UIC 406 capacity, timetable conflict detection
   - OpenTrack: Swiss Federal Railways, open-source, detailed train dynamics
   - UCSD RailPlan: North American focus, Class I railroad adoptions
   - Proprietary: BNSF, UP, NS have internal simulation tools

2. INPUT DATA REQUIREMENTS
   - Infrastructure: track layout, signal locations, speed limits, grades
   - Rolling stock: train length, weight, HP, resistance coefficients
   - Timetable: scheduled train paths, arrival/departure times
   - Stochastic elements: dwell time variability, initial delays

3. TIMETABLE CONFLICT DETECTION
   - Identify conflicting train paths (two trains, one track segment)
   - Buffer time: minimum separation between trains (usually 3-5 min)
   - Optimize timetable to minimize conflicts and total delay
   - Graphical timetable (Marey chart): visualize train paths over time/space

4. DELAY PROPAGATION ANALYSIS
   - Primary delay: initial delay (e.g., late departure, slow order)
   - Secondary delay: propagated to following trains (blocking, waiting)
   - Knock-on effect: delays cascade through network
   - Recovery time: schedule padding to absorb delays

5. CAPACITY UTILIZATION METRICS
   - Line utilization: % of time track is occupied
   - UIC 406 compression: ratio of timetabled to theoretical capacity
   - Critical sections: bottlenecks where utilization > 80%
   - Sensitivity: impact of additional train on total delay

6. MONTE CARLO STOCHASTIC SIMULATION
   - Run 100-1,000 iterations with random initial delays
   - Output: distribution of total delay (mean, 95th percentile)
   - Robustness: how sensitive is schedule to minor disruptions?
   - Risk assessment: probability of severe delays (> 30 min)

Simulation is essential for: new service feasibility (can we add 10 more trains?),
infrastructure investment justification (double-tracking reduces delay by X%),
timetable optimization (best meet locations), and PTC implementation analysis.
Class I railroads use simulation to test operating plan changes before field
deployment. Passenger rail agencies use it for schedule development and public
hearings (NEC Future, California High-Speed Rail).""",
        key_factors=[
            "Software selection (RailSys, OpenTrack, proprietary)",
            "Input data quality (infrastructure, rolling stock, timetable)",
            "Conflict detection and resolution",
            "Delay propagation and recovery",
            "Stochastic Monte Carlo analysis"
        ],
        primary_authority=[
            "OpenTrack User Manual (IFV ETH Zurich)",
            "RailSys Documentation (RMCon)",
            "TRB TCRP Report 13 - Rail Transit Capacity"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All rail network planning studies"
    ),

    DoctrineBlock(
        topic="Short Line Railroad Economics and Viability",
        keywords=["short line", "Class III", "operating ratio", "car interchange", "subsidy"],
        conclusion_template="Short line {railroad}: {miles} miles, {carloads} annual carloads, operating ratio {or}%. Revenue ${revenue}M, expenses ${expenses}M. Interchange with {class1}. {viable} without subsidy.",
        reasoning_framework="""Short Line Railroad Economics Framework:

1. SHORT LINE CLASSIFICATION
   - Class III: < $38.8M annual revenue (2022 threshold, inflation-adjusted)
   - Class II (Regional): $38.8M - $500M revenue
   - Class I: > $500M revenue (7 railroads: BNSF, UP, NS, CSX, CP, CN, KCS)
   - ~600 short lines operate ~50,000 miles (1/3 of U.S. rail network)

2. REVENUE SOURCES
   - Freight: per-car or per-ton rates to shippers
   - Interchange revenue: Class I pays short line for car delivery
   - Switching fees: industrial plant switching services
   - Lease/storage: car storage, industrial siding leases
   - Government grants: FRA CRISI, state rail improvement programs

3. COST STRUCTURE
   - Track maintenance: ties, rail, ballast, drainage (~$20-50K/mile/year)
   - Locomotive maintenance: fuel, repairs, crew wages
   - Insurance: liability, property, workers compensation
   - Administrative: office, accounting, regulatory compliance
   - Fixed costs high relative to traffic (diseconomies of density)

4. OPERATING RATIO (OR) ANALYSIS
   - OR = Operating Expenses / Operating Revenue
   - Class I target: 60-65% (BNSF, UP)
   - Short line typical: 80-95% (thin margins)
   - OR > 100%: losing money, requires subsidy or abandonment

5. TRAFFIC DENSITY AND VIABILITY
   - Break-even: typically 1,000-5,000 carloads/year
   - High-density short lines (10,000+ cars/year): very profitable
   - Low-density (< 500 cars/year): subsidy-dependent
   - Captive shippers: single customer (grain elevator, coal mine)

6. GRANT PROGRAMS AND PUBLIC SUPPORT
   - FRA CRISI: capital grants for track rehab, bridges
   - State rail loan/grant programs: 45 states have programs
   - TIGER/INFRA: larger projects, intermodal connectors
   - Economic development: communities support short lines to retain industry

Short lines serve branch lines abandoned by Class I railroads (1980s-2000s).
Staggers Rail Act (1980) enabled short line growth via deregulation and easier
abandonment. Many short lines are owned by holding companies (Genesee & Wyoming,
Watco, RailAmerica). Viability depends on: sufficient traffic density, reasonable
track condition (deferred maintenance backlog), and access to Class I interchange.
Without grants, many rural short lines would abandon, forcing grain/lumber/etc
to truck (higher cost, more emissions).""",
        key_factors=[
            "Annual carloads and revenue",
            "Operating ratio (target < 95%)",
            "Track condition and deferred maintenance",
            "Class I interchange revenue",
            "Grant funding availability"
        ],
        primary_authority=[
            "AAR Class III Railroad Statistics",
            "FRA CRISI Grant Program Guidance",
            "American Short Line and Regional Railroad Association (ASLRRA)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All Class III short line railroads"
    ),

    DoctrineBlock(
        topic="Class I Railroad Operations Planning and PSR",
        keywords=["Class I", "PSR", "precision scheduled railroading", "train plan", "dwell time"],
        conclusion_template="Class I railroad {railroad}: PSR implementation reduced operating ratio from {old_or}% to {new_or}%. Train count reduced by {reduction}%, average train length {length} cars, terminal dwell {dwell} hours.",
        reasoning_framework="""Class I Railroad Operations Planning Framework:

1. PRECISION SCHEDULED RAILROADING (PSR) PRINCIPLES
   - Originated: Hunter Harrison at CN, CP, CSX (2000s-2010s)
   - Core: run trains on fixed schedule (like passenger rail), not on-demand
   - Longer trains: 10,000+ ft, 150+ cars (requires DPU, longer sidings)
   - Fewer trains: consolidate traffic, reduce switching
   - Lower operating ratio: reduce crew, locomotives, fuel

2. TRAIN PLAN DEVELOPMENT
   - Origin-destination (O-D) pairs: major terminals
   - Service frequency: daily, 2x/week, as-needed
   - Train schedule: fixed departure/arrival times
   - Car blocking: group cars by destination to minimize switching
   - Run-through trains: bypass intermediate classification yards

3. TERMINAL DWELL TIME REDUCTION
   - Dwell: time from train arrival to car departure
   - Industry average: 24-30 hours (pre-PSR)
   - PSR target: < 24 hours, best-in-class < 18 hours
   - Techniques: pre-blocking, advance consist planning, crew availability

4. LOCOMOTIVE AND CREW PRODUCTIVITY
   - Locomotive turns: cycles per month (higher = better utilization)
   - Crew starts: fewer crew starts per train-mile (longer runs, fewer handoffs)
   - DPU (Distributed Power Units): unmanned mid-train/rear locos
   - Fuel efficiency: track condition, train handling, DPU optimization

5. CUSTOMER SERVICE IMPACTS
   - Reduced flexibility: fixed schedules may not match shipper needs
   - Longer transit times: consolidation delays for small shipments
   - Improved reliability: on-time performance increases (if PSR done well)
   - Shipper complaints: peak season capacity constraints

6. OPERATIONAL METRICS (CLASS I REPORTING)
   - Operating ratio (OR): expenses/revenue (target 60-65%)
   - Revenue ton-miles (RTM): freight volume metric
   - Train velocity: average mph including stops (target 25-30 mph)
   - Terminal dwell: hours in yard (target < 24 hrs)
   - Cars online: total fleet count (lower = better asset utilization)

PSR transformed Class I railroads 2015-2020. BNSF, UP, NS, CSX all implemented
variants. Results: OR improved 5-10 points, train counts down 20-30%, operating
margins up. Controversies: service disruptions during transition, shipper complaints,
regulatory scrutiny (STB hearings), and labor opposition (crew job losses).
Long-term: PSR is now industry standard; debate is about execution, not concept.""",
        key_factors=[
            "Fixed train schedules (PSR model)",
            "Train length and DPU configuration",
            "Terminal dwell time reduction",
            "Operating ratio (OR) improvement",
            "Customer service trade-offs"
        ],
        primary_authority=[
            "Surface Transportation Board (STB) Class I Reports",
            "AAR Railroad Performance Measures (RPM)",
            "Hunter Harrison - Precision Scheduled Railroading (2016)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All Class I railroads (BNSF, UP, NS, CSX, CP, CN, KCS)"
    ),

    DoctrineBlock(
        topic="Positive Train Control (PTC) Implementation and Impact",
        keywords=["PTC", "ETMS", "I-ETMS", "interoperability", "safety overlay"],
        conclusion_template="PTC implementation: {railroad} uses {system} (I-ETMS, ACSES, etc). Cost ${cost}B, prevents {prevented} accident types. Interoperability with {railroads}, covers {miles} route-miles.",
        reasoning_framework="""Positive Train Control (PTC) Implementation Framework:

1. PTC MANDATE (RAIL SAFETY IMPROVEMENT ACT 2008)
   - Required on: passenger rail, Class I mainlines with toxic-by-inhalation (TIH)
   - Deadline: 12/31/2020 (extended from 2015)
   - Prevents: train-to-train collisions, overspeed derailments, unauthorized entry into work zones, movement through misaligned switches
   - Does NOT prevent: grade crossing accidents, trespasser strikes, track defects

2. PTC SYSTEM TYPES
   - I-ETMS (Interoperable ETMS): freight railroad standard (BNSF, UP, NS, CSX)
   - ACSES (Advanced Civil Speed Enforcement System): Amtrak NEC
   - E-ATC: commuter rail (SEPTA, Metro-North)
   - Overlay system: uses existing track circuits + GPS + onboard computer

3. TECHNICAL COMPONENTS
   - Onboard computer: enforces speed limits, stop signals
   - GPS: position determination (backup: track circuits, wheel tachometer)
   - Radio: 220 MHz nationwide (AAR mandate), transmits movement authorities
   - Wayside devices: signal interface units, switch position monitors
   - Back office: dispatch system integration, movement authority generation

4. INTEROPERABILITY REQUIREMENTS
   - Freight railroads must interoperate (BNSF locos run on UP, NS, CSX)
   - Standard: I-ETMS, coordinated by AAR
   - Onboard database: track profiles, speed limits, signal locations
   - Border territories: PTC handoff between railroads
   - Locomotive provisioning: install/test on 20,000+ locomotives

5. IMPLEMENTATION COSTS
   - Industry total: ~$15 billion (freight + passenger + commuter)
   - BNSF: $2.5B, UP: $2.9B, NS: $1.3B, CSX: $2.4B
   - Per-locomotive: $50-150K (hardware + installation + testing)
   - Annual O&M: $300-500M industry-wide (software, spectrum, maintenance)

6. SAFETY IMPACT AND BENEFIT-COST
   - Accidents prevented: ~10-15 per year (FRA estimate)
   - Lives saved: 5-10 per year
   - Benefit-cost ratio: 0.5-1.0 (benefits < costs in pure economic terms)
   - Congress mandated regardless of BCR (political/safety imperative)
   - Unintended benefits: improved dispatching data, velocity optimization

PTC is the largest rail safety investment in U.S. history. Implementation was
technically complex (interoperability, radio spectrum, software bugs) and
financially burdensome (especially for commuter rail and short lines). FRA
provided deadline extensions and alternative compliance options. As of 2021,
~99% of required route-miles have PTC in operation. Future: PTC data can enable
traffic optimization, predictive maintenance, and autonomous train operation.""",
        key_factors=[
            "Mandate: passenger rail + TIH mainlines",
            "System types (I-ETMS, ACSES, E-ATC)",
            "Interoperability requirements",
            "Implementation cost (~$15B industry-wide)",
            "Safety benefit (10-15 accidents/year prevented)"
        ],
        primary_authority=[
            "FRA PTC Regulations (49 CFR 236 Subpart I)",
            "Rail Safety Improvement Act of 2008",
            "AAR PTC Implementation Standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All U.S. railroads with PTC mandate"
    ),

    DoctrineBlock(
        topic="Rail Corridor Environmental Impact Assessment",
        keywords=["NEPA", "EIS", "environmental impact", "Section 106", "wetlands"],
        conclusion_template="Rail corridor EIS: {project} requires {level} NEPA review. Impacts: {impacts}. Mitigation: {mitigation}. Section 106 historic sites: {historic}. ROD expected {date}.",
        reasoning_framework="""Rail Corridor Environmental Impact Framework:

1. NEPA PROCESS LEVELS
   - Categorical Exclusion (CE): minor projects, no EIS required
   - Environmental Assessment (EA): moderate impacts, FONSI possible
   - Environmental Impact Statement (EIS): major impacts, full public process
   - FRA/FTA are lead federal agencies for rail projects

2. IMPACT CATEGORIES ANALYZED
   - Air quality: diesel emissions, particulates (PM2.5), NOx
   - Noise and vibration: FTA/FRA noise assessment methodology
   - Wetlands and water: Section 404 permits (USACE), stormwater (EPA)
   - Wildlife and habitat: Endangered Species Act (ESA) consultation
   - Historic/cultural: Section 106 (NHPA), tribal consultation
   - Visual/aesthetics: viewshed analysis, community character

3. SECTION 106 HISTORIC PRESERVATION
   - National Historic Preservation Act (NHPA) Section 106
   - Identify historic properties: buildings, bridges, archaeological sites
   - Assess adverse effects: physical damage, visual intrusion
   - Mitigation: avoidance, minimization, documentation (HABS/HAER)
   - State Historic Preservation Officer (SHPO) consultation

4. WETLANDS AND SECTION 404 PERMITS
   - Fill or dredge in wetlands requires USACE permit
   - Sequencing: avoid, minimize, compensate (mitigation bank)
   - Mitigation ratio: 1:1 to 3:1 (acres created per acre filled)
   - Typical rail corridor: 1-5 acres of wetland fill per mile

5. NOISE AND VIBRATION MITIGATION
   - FRA/FTA noise criteria: moderate impact > 3 dB increase, severe > 8 dB
   - Mitigation: noise walls, track damping, operational restrictions
   - Vibration: affects sensitive equipment (hospitals, labs)
   - Ground-borne noise: rumble in buildings near tracks

6. PUBLIC INVOLVEMENT AND ALTERNATIVES
   - Scoping: identify issues, alternatives, stakeholders
   - Alternatives: no-build, build alternatives (routes, technologies)
   - Public hearings: minimum 2 (draft EIS, final EIS)
   - Record of Decision (ROD): FRA/FTA selects preferred alternative

Typical EIS timeline: 2-4 years for major rail projects (California HSR, Gateway
Tunnel). Costs: $5-20M for EIS preparation. Lawsuits common (environmental groups,
NIMBYs, historic preservationists). Key to success: early agency coordination,
robust alternatives analysis, meaningful mitigation commitments, and transparent
public process. Section 106 is often the sleeper issue - historic bridge demolition
can derail a project if not addressed early.""",
        key_factors=[
            "NEPA level (CE, EA, EIS)",
            "Section 106 historic preservation",
            "Wetlands and Section 404 permits",
            "Noise and vibration impacts",
            "Public involvement and ROD timeline"
        ],
        primary_authority=[
            "FRA Environmental Procedures (23 CFR 771)",
            "FTA Noise and Vibration Manual (2018)",
            "NEPA Regulations (40 CFR 1500-1508)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All federally-funded rail infrastructure projects"
    ),

    DoctrineBlock(
        topic="Rail Infrastructure Financing Mechanisms",
        keywords=["RRIF", "TIFIA", "PABs", "tax increment financing", "public-private partnership"],
        conclusion_template="Financing structure: {project} uses {mechanism} (RRIF, TIFIA, PABs). Loan ${loan}M at {rate}% interest, {term} years. Equity ${equity}M, federal grant ${grant}M. Total ${total}M.",
        reasoning_framework="""Rail Infrastructure Financing Framework:

1. RAILROAD REHABILITATION & IMPROVEMENT FINANCING (RRIF)
   - FRA loan program: up to $35B lending authority
   - Eligible: Class I, II, III railroads, intermodal facilities
   - Terms: up to 35 years, interest = Treasury rate
   - Credit risk premium: 3-5% of loan amount (upfront fee)
   - Use: track rehab, bridge replacement, equipment, PTC

2. TRANSPORTATION INFRASTRUCTURE FINANCE & INNOVATION ACT (TIFIA)
   - USDOT loan program: roads, transit, rail
   - Up to 49% of project cost
   - Terms: 35 years, interest = Treasury rate + 1%
   - Investment-grade rating required (BBB- or better)
   - Use: major projects (> $50M cost)

3. PRIVATE ACTIVITY BONDS (PABs)
   - Tax-exempt bonds for private rail projects
   - $15B authorization (SAFETEA-LU 2005)
   - Interest savings: 1-2% vs taxable bonds
   - Must meet public benefit test (freight mobility, emissions reduction)
   - Amtrak, commuter rail, freight intermodal eligible

4. TAX INCREMENT FINANCING (TIF)
   - Local government captures property tax increase from development
   - Rail station/terminal drives surrounding real estate value
   - TIF revenue bonds repay infrastructure costs
   - Common for commuter rail stations, streetcar projects
   - Controversy: subsidy to private developers, diverts tax revenue

5. PUBLIC-PRIVATE PARTNERSHIPS (P3)
   - Private partner: design, build, finance, operate, maintain
   - Revenue sources: user fees (tolls, fares), availability payments
   - Risk transfer: construction, ridership, O&M to private sector
   - Examples: Brightline (Florida), Texas Central HSR
   - Challenges: revenue risk (ridership forecasts optimistic), public skepticism

6. FEDERAL GRANT PROGRAMS
   - CRISI (Consolidated Rail Infrastructure and Safety Improvements): $1B/year
   - INFRA: multimodal, competitive, large projects (> $100M)
   - FTA Capital Investment Grants (CIG): new starts, core capacity
   - RAISE (formerly TIGER): discretionary grants, 20% max
   - State DOT programs: many states have rail capital programs

Typical capital stack: 40% federal grant, 30% RRIF/TIFIA loan, 20% private
equity, 10% state/local. Interest rate subsidy (RRIF/TIFIA at Treasury rate)
is the most valuable federal contribution - saves ~3% vs commercial rate. Credit
risk premium and loan processing timeline (12-24 months) are downsides. Short
lines use RRIF extensively; Class I railroads prefer internal capital or commercial
bonds (faster, no FRA approval required).""",
        key_factors=[
            "RRIF loans (up to 35 years, Treasury rate)",
            "TIFIA loans (up to 49% of cost)",
            "Private Activity Bonds (PABs, tax-exempt)",
            "Tax Increment Financing (TIF, local)",
            "Federal grants (CRISI, INFRA, RAISE)"
        ],
        primary_authority=[
            "FRA RRIF Program Guidance",
            "USDOT TIFIA Program Guide",
            "IRC Section 142(a)(13) - Private Activity Bonds"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All rail infrastructure financing in U.S."
    ),

    DoctrineBlock(
        topic="Rail Freight Demand Forecasting Methodology",
        keywords=["demand forecast", "freight model", "elasticity", "commodity flow", "transearch"],
        conclusion_template="Freight demand forecast: {commodity} growth {growth}% annually, price elasticity {elasticity}. Baseline {baseline} carloads, forecast {forecast} carloads in {year}. Model: {model}.",
        reasoning_framework="""Rail Freight Demand Forecasting Framework:

1. COMMODITY FLOW DATA SOURCES
   - Transearch: IHS Markit proprietary database (county-to-county flows)
   - Freight Analysis Framework (FAF): FHWA/BTS public data (state-to-state)
   - Waybill Sample: STB 1% sample of rail freight (confidential, aggregated)
   - Carload data: AAR weekly carload reports (aggregate, by commodity type)

2. DEMAND DRIVERS AND ELASTICITIES
   - GDP growth: freight ton-miles correlate 0.7-0.9 with GDP
   - Commodity-specific: coal (declining), intermodal (growing 3-5%/year)
   - Price elasticity: freight demand -0.5 to -1.5 (rail vs truck competition)
   - Fuel prices: higher diesel → modal shift to rail (fuel-efficient)
   - Industrial production: steel, chemicals, autos drive manifest freight

3. MODAL CHOICE MODELING
   - Logit model: rail vs truck mode share
   - Variables: cost, time, reliability, shipment size
   - Rail advantage: long-haul (>500 miles), heavy bulk (coal, grain, crude)
   - Truck advantage: short-haul, time-sensitive, small shipments
   - Intermodal: combines rail line-haul + truck drayage

4. SCENARIO ANALYSIS
   - Base case: current trends continue
   - High growth: economic boom, infrastructure investment
   - Low growth: recession, carbon pricing, truck automation
   - Policy scenarios: carbon tax, congestion pricing, truck size/weight limits

5. DISAGGREGATION TO CORRIDOR LEVEL
   - National forecast → state → county → rail corridor
   - Network assignment: which routes will traffic use?
   - Capacity constraints: if corridor full, traffic diverts or mode-shifts
   - Growth factors: apply % growth to baseline O-D matrix

6. VALIDATION AND CALIBRATION
   - Backcast: test model on historical data (2010-2020)
   - Error metrics: RMSE, MAPE (mean absolute percentage error)
   - Expert judgment: sanity-check forecasts with railroad ops staff
   - Update frequency: re-forecast every 3-5 years with new data

Typical forecast horizon: 20-30 years for infrastructure planning. Uncertainty
increases with time: +/- 10% at 5 years, +/- 30% at 20 years. Scenario analysis
essential to bound uncertainty. Coal traffic decline (50% drop 2010-2020) was
NOT foreseen by most forecasts - lesson: be humble about long-term predictions.
Intermodal growth has been consistent bright spot (4-5%/year for 30+ years).""",
        key_factors=[
            "Data sources (Transearch, FAF, Waybill)",
            "Demand elasticities (GDP, price, fuel)",
            "Modal choice modeling (rail vs truck)",
            "Scenario analysis (base, high, low)",
            "Validation and calibration"
        ],
        primary_authority=[
            "FHWA Freight Analysis Framework (FAF)",
            "STB Waybill Sample Methodology",
            "TRB Freight Demand Modeling Conference Proceedings"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="All rail freight demand forecasting studies"
    ),

    DoctrineBlock(
        topic="Passenger Rail Service Planning and Operating Cost Estimation",
        keywords=["passenger rail", "operating cost", "farebox recovery", "subsidy", "ridership"],
        conclusion_template="Passenger rail {service}: {trains} trains/day, {ridership} annual riders. Operating cost ${opcost}M, revenue ${revenue}M, farebox recovery {recovery}%, subsidy ${subsidy}M.",
        reasoning_framework="""Passenger Rail Service Planning Framework:

1. SERVICE FREQUENCY AND SCHEDULE
   - Frequency: hourly, 2-hour, peak-only, daily (long-distance)
   - Higher frequency → higher ridership (induced demand)
   - Minimum viable: 4 round-trips/day for commuter rail
   - Timetable: optimize for commuter peaks, off-peak travel, connections

2. OPERATING COST COMPONENTS
   - Crew: engineers, conductors, on-board service (long-distance)
   - Fuel/electricity: diesel, electric catenary, hybrid
   - Maintenance: rolling stock (cars, locomotives), track, stations
   - Insurance, dispatch, administration
   - Typical: $50-150 per train-mile (commuter rail), $200-500 (Amtrak LD)

3. FAREBOX RECOVERY RATIO
   - Ratio: fare revenue / operating cost
   - Commuter rail: 30-60% typical (NYC Metro-North: 60%, others 30-40%)
   - Amtrak Northeast Corridor: 90-100% (profitable)
   - Amtrak long-distance: 30-50% (heavy subsidy)
   - U.S. policy: no federal operating subsidy for Amtrak LD routes (political debate)

4. RIDERSHIP FORECASTING
   - Elasticity: service frequency, fare, travel time, parking cost
   - Induced demand: new service creates new trips (20-40% of forecast)
   - Market share: rail vs auto mode split (depends on congestion, parking cost)
   - Validation: peer system comparisons, stated preference surveys

5. SUBSIDY SOURCES
   - Federal: FTA CIG capital grants (no operating subsidy for most)
   - State: operating subsidy (CA, NY, IL, WA, etc.)
   - Local: sales tax, property tax, general fund
   - Farebox: ticket revenue (30-60% of operating cost)
   - Advertising, parking, real estate development (minor)

6. CAPITAL COST ESTIMATION
   - Rolling stock: $5-10M per rail car, $5-8M per locomotive
   - Stations: $10-50M for full-service station, $1-5M for simple platform
   - Track: $3-10M per mile (single track, depends on terrain, ROW)
   - Electrification: $5-15M per mile (catenary, substations)
   - Signals/PTC: $2-5M per mile

Passenger rail is subsidy-dependent in North America (unlike Europe/Asia where
ridership density is higher). Political support essential: dedicated funding
source (sales tax in LA, SF), state commitment (Amtrak state-supported routes),
or federal grants (NEC, California HSR). Operating cost control critical: crew
labor agreements, preventive maintenance (avoid reactive repairs), and energy
efficiency. High farebox recovery (> 50%) makes service politically sustainable.""",
        key_factors=[
            "Service frequency (trains/day)",
            "Operating cost ($/train-mile)",
            "Farebox recovery ratio (revenue/cost)",
            "Ridership forecast and elasticity",
            "Subsidy sources (federal, state, local)"
        ],
        primary_authority=[
            "FTA Annual Database (National Transit Database)",
            "Amtrak Financial Reports",
            "TRB Transit Cooperative Research Program (TCRP)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All U.S. passenger rail services"
    ),

    DoctrineBlock(
        topic="Rail Bridge Load Rating and Replacement Priority",
        keywords=["bridge", "load rating", "Cooper E-80", "replacement priority", "AREMA"],
        conclusion_template="Bridge {bridge_id}: built {year}, load rating {rating}, condition {condition}. Replacement cost ${cost}M, priority rank {priority}. Meets/fails {standard} loading.",
        reasoning_framework="""Rail Bridge Load Rating and Replacement Framework:

1. COOPER E-LOADING SYSTEM
   - Cooper E-80: standard freight locomotive axle loading (80,000 lb/axle)
   - Modern heavy freight: 315,000 lb railcars → E-90 or higher needed
   - Historic bridges: E-40 to E-60 (lighter, pre-1960s)
   - Load rating: maximum safe load bridge can carry

2. BRIDGE INSPECTION AND RATING
   - FRA Bridge Safety Standards (49 CFR 237): inspection every year
   - Rating method: AREMA Manual Chapter 15 (Load Rating)
   - Factors: span length, material (steel, timber, concrete), condition
   - Defects: corrosion, fatigue cracks, timber rot, concrete spalling

3. BRIDGE CONDITION CLASSIFICATION
   - Good: no defects, full load rating
   - Fair: minor defects, load restrictions possible
   - Poor: significant defects, speed/weight restrictions required
   - Critical: unsafe, immediate repair or closure

4. REPLACEMENT PRIORITY RANKING
   - Safety: structural condition, deficiency rating
   - Traffic: trains/day, tonnage, passenger vs freight
   - Network criticality: mainline vs branch, alternate route availability
   - Cost-benefit: replacement cost vs repair cost, remaining life

5. REPLACEMENT COST ESTIMATION
   - Span length: $1-5M per 100 ft of span (steel/concrete)
   - Foundation: $500K-2M per pier (depends on soil, water depth)
   - Temporary shoofly: $500K-3M for detour track during construction
   - Total: $5-50M for typical railroad bridge replacement

6. BRIDGE MANAGEMENT SYSTEMS
   - Database: all bridges, inspection reports, load ratings
   - Predictive modeling: deterioration rates, remaining life
   - Budget optimization: which bridges to replace first given limited funds?
   - FRA reporting: annual bridge inventory submission

U.S. railroads own ~100,000 bridges (Class I + short lines). Many are 100+ years
old (built 1880-1920s). FRA mandates inspection but does NOT fund replacement
(unlike highways, where federal-aid bridge program exists). Class I railroads
spend $1-2B/year on bridge maintenance and replacement. Short lines often have
severely deficient bridges but lack capital for replacement - this is where
state/federal grants (CRISI, etc.) are critical. Timber bridges are the most
problematic: short life (20-30 years), fire risk, and increasing load requirements.""",
        key_factors=[
            "Cooper E-loading (E-80 standard for modern freight)",
            "Bridge condition (good, fair, poor, critical)",
            "Load rating and restrictions",
            "Replacement priority (safety, traffic, criticality)",
            "Replacement cost ($5-50M typical)"
        ],
        primary_authority=[
            "FRA Bridge Safety Standards (49 CFR 237)",
            "AREMA Manual Chapter 15 - Steel Structures",
            "AAR Bridge Management Practices"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All railroad bridges in U.S."
    ),

    DoctrineBlock(
        topic="Rail Electrification Feasibility and Economics",
        keywords=["electrification", "catenary", "AC vs DC", "regenerative braking", "ROI"],
        conclusion_template="Electrification of {corridor}: {miles} miles, {system} system (25kV AC / 1500V DC). Capital cost ${capex}M, energy savings ${savings}M/year, payback {payback} years.",
        reasoning_framework="""Rail Electrification Feasibility Framework:

1. ELECTRIFICATION SYSTEM TYPES
   - 25kV AC overhead catenary: modern standard (high speed, commuter)
   - 1500V DC overhead: legacy systems (Northeast Corridor south of NYC)
   - 750V DC third rail: subway, light rail (short distances, urban)
   - 15kV AC: European standard (Germany, Switzerland)

2. CAPITAL COST COMPONENTS
   - Catenary installation: $5-15M per mile (poles, wire, tensioning)
   - Substations: $5-20M each, spaced 10-30 miles apart
   - Traction power upgrades: utility interconnection, transformers
   - Signal system compatibility: electrical interference mitigation
   - Total: $10-30M per mile for mainline electrification

3. OPERATING COST SAVINGS
   - Energy efficiency: electric 2-3x more efficient than diesel
   - Fuel cost: electricity ~$0.10/kWh vs diesel ~$3/gallon equivalent
   - Maintenance: electric locos have fewer moving parts, longer life
   - Regenerative braking: downhill/braking energy returned to grid (10-20% savings)
   - Example: $1M/year savings per 100 miles of electrified corridor

4. ENVIRONMENTAL BENEFITS
   - Zero direct emissions (diesel particulates, NOx eliminated)
   - Grid emissions depend on power source (coal, gas, renewables)
   - Noise reduction: electric locos quieter than diesel
   - Carbon accounting: lifecycle analysis includes grid mix

5. PAYBACK PERIOD AND ROI
   - Capital cost / annual savings = payback period
   - Typical: 15-30 years for freight, 10-20 years for high-traffic passenger
   - Traffic density critical: need high train volume to justify investment
   - Example: NEC (Amtrak) electrified due to high passenger frequency

6. TECHNICAL CHALLENGES
   - Clearance: catenary requires 23+ ft vertical clearance (conflicts with double-stack freight)
   - Compatibility: diesel locos cannot run under catenary (or dual-mode needed)
   - Resilience: ice storms, wind can down catenary (outage risk)
   - Utility coordination: substantial electrical load (10-50 MW per substation)

Electrification in U.S.: only ~1,000 miles electrified (NEC, some commuter rail).
Europe/Asia: extensive electrification (50-90% of mainlines). Reason for U.S.
lag: low traffic density on most freight corridors, double-stack clearance conflicts,
and low diesel fuel prices (historically). California High-Speed Rail will be
fully electrified (25kV AC). Amtrak proposed NEC South electrification (Washington-Richmond)
but shelved due to cost. Electrification makes sense for: high-frequency passenger
corridors, urban commuter rail, and environmental policy mandates.""",
        key_factors=[
            "System type (25kV AC, 1500V DC, etc.)",
            "Capital cost ($10-30M per mile)",
            "Energy savings (2-3x vs diesel)",
            "Payback period (10-30 years)",
            "Clearance and compatibility issues"
        ],
        primary_authority=[
            "AREMA Manual Chapter 33 - Electric Traction",
            "FRA Electrification Guidance",
            "IEC 60850 - Railway Applications - Supply Voltages"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="All rail electrification feasibility studies"
    ),

    DoctrineBlock(
        topic="Rail Network Resilience and Disaster Recovery",
        keywords=["resilience", "disaster recovery", "redundancy", "flooding", "earthquake"],
        conclusion_template="Network resilience: {corridor} vulnerable to {hazard}. Redundancy: {redundant} alternate routes. Recovery time {recovery} days, mitigation cost ${mitigation}M.",
        reasoning_framework="""Rail Network Resilience and Disaster Recovery Framework:

1. HAZARD TYPES AND EXPOSURE
   - Flooding: washouts, bridge scour, submerged track (hurricanes, rivers)
   - Earthquakes: track misalignment, bridge collapse (West Coast)
   - Landslides: debris on track, track undermining (mountains)
   - Extreme weather: heat kink (rail buckling), snow/ice, wind (derailments)
   - Wildfire: bridge/trestle fire, signal/communication damage

2. NETWORK REDUNDANCY ANALYSIS
   - Single point of failure: critical bridges, tunnels, chokepoints
   - Alternate routes: parallel lines, detour via other railroads
   - Interline agreements: trackage rights, haulage agreements for detours
   - Example: CSX Howard Street Tunnel fire (2001) → 6-week closure, massive detours

3. DISASTER RECOVERY PLANNING
   - Emergency response: assess damage, clear debris, temporary shoring
   - Repair prioritization: mainline first, branch lines deferred
   - Temporary track: shoofly around washout, Bailey bridge (military-style)
   - Supply chain: stockpile rail, ties, ballast at strategic locations
   - Contractor pre-positioning: on-call MOT (Maintenance of Way) contractors

4. RECOVERY TIME ESTIMATION
   - Minor: 1-3 days (washout repair, debris clearing)
   - Moderate: 1-4 weeks (bridge temporary repair, track realignment)
   - Major: 1-6 months (bridge replacement, tunnel repair)
   - Catastrophic: > 6 months (major bridge collapse, long tunnel failure)

5. MITIGATION STRATEGIES
   - Flood protection: raise track grade, improve drainage, scour countermeasures
   - Seismic retrofit: bridge column jacketing, base isolators, ductile design
   - Rockfall protection: catchment ditches, barriers, scaling (remove loose rock)
   - Climate adaptation: heat-resistant rail (CWR stress management), fire breaks

6. COST-BENEFIT OF RESILIENCE INVESTMENT
   - Mitigation cost: $1-10M per vulnerable location
   - Avoided cost: service disruption (lost revenue, detour costs, customer penalties)
   - Risk assessment: probability × consequence (expected annual loss)
   - Prioritize: high-traffic corridors, no alternate routes, high-hazard zones

Major disasters: Hurricane Katrina (2005) - CSX, NS lines flooded, months to repair;
Tohoku earthquake (2011, Japan) - extensive rail damage, rapid rebuild; California
wildfires (annual) - bridge fires, signal damage. Lesson: redundancy is expensive
but essential. Single-track branch lines with no detour are extremely vulnerable.
Class I railroads have detailed disaster recovery plans and pre-negotiated mutual
aid agreements. Short lines often lack resources for rapid recovery.""",
        key_factors=[
            "Hazard exposure (flooding, earthquake, etc.)",
            "Network redundancy (alternate routes)",
            "Recovery time (days to months)",
            "Mitigation cost ($1-10M per site)",
            "Risk assessment and prioritization"
        ],
        primary_authority=[
            "AAR Emergency Response Guidelines",
            "AREMA Manual Chapter 8 - Concrete Structures (Seismic)",
            "FEMA National Infrastructure Protection Plan"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All rail networks subject to natural disasters"
    ),

    DoctrineBlock(
        topic="Rail Corridor Land Use and Transit-Oriented Development (TOD)",
        keywords=["TOD", "land use", "zoning", "joint development", "value capture"],
        conclusion_template="TOD analysis: {station} has {acres} acres developable land, zoning {zoning}, density {density} units/acre. Value capture potential ${value}M via {mechanism}.",
        reasoning_framework="""Transit-Oriented Development (TOD) Framework:

1. TOD PRINCIPLES AND BENEFITS
   - High-density mixed-use development within 0.5 mile of station
   - Walkable, bike-friendly, reduced parking requirements
   - Benefits: ridership increase (20-40%), real estate value uplift, reduced VMT
   - Typology: urban infill (redevelopment), greenfield (new community)

2. LAND USE AND ZONING COORDINATION
   - Zoning overlay: higher density, reduced setbacks, mixed-use allowed
   - Parking reduction: 0.5-1.0 spaces per unit (vs 2.0 standard)
   - Form-based codes: regulate building form, not just use
   - Local government approval: rezone, variances, design review

3. JOINT DEVELOPMENT OPPORTUNITIES
   - Railroad-owned land: station parking lots, air rights, adjacent parcels
   - Public-private partnership: developer builds on railroad land
   - Revenue to railroad: land lease, sale, parking revenue share
   - Example: Metro-North (NYC) - multiple joint developments at stations

4. VALUE CAPTURE MECHANISMS
   - Tax Increment Financing (TIF): capture property tax increase
   - Special Assessment District (SAD): landowners pay for infrastructure
   - Development Impact Fees: developer pays for station improvements
   - Land value tax: tax land appreciation from transit access
   - Typical capture: 10-30% of land value uplift

5. RIDERSHIP IMPACT
   - TOD elasticity: 1% density increase → 0.5-1.5% ridership increase
   - Mode shift: auto to transit (induced by reduced parking, walkability)
   - Reverse commute: jobs at TOD stations, not just residential
   - Network effect: multiple TOD stations amplify ridership

6. CHALLENGES AND BARRIERS
   - NIMBY opposition: neighbors oppose density, traffic, character change
   - Parking politics: merchants demand parking, TOD reduces it
   - Affordability: market-rate TOD displaces low-income residents
   - Railroad reluctance: liability concerns, operational conflicts

Successful TOD examples: Washington DC (Metro), Portland (MAX), Denver (RTD),
San Francisco (BART). Keys to success: supportive zoning, city-transit agency
coordination, quality urban design, and market demand. Commuter rail TOD is
harder than urban rail (lower frequency, longer trips, auto-oriented suburbs).
Parking is the biggest battle: TOD requires LESS parking, but local officials
fear spillover parking in neighborhoods. Compromise: shared parking structures,
time-of-day restrictions, residential parking permits.""",
        key_factors=[
            "TOD zoning (density, mixed-use, parking reduction)",
            "Joint development (railroad land, P3)",
            "Value capture (TIF, SAD, fees)",
            "Ridership impact (density elasticity)",
            "NIMBY opposition and political support"
        ],
        primary_authority=[
            "FTA TOD Planning Guidance",
            "TRB TCRP Report 102 - TOD in the U.S.",
            "Center for Transit-Oriented Development (CTOD)"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="All passenger rail station planning"
    ),

    DoctrineBlock(
        topic="Rail Safety Performance Metrics and FRA Reporting",
        keywords=["FRA safety", "accident rate", "reportable incidents", "FRA Form 54", "injury frequency"],
        conclusion_template="Safety metrics: {railroad} has {accidents} reportable accidents, {injuries} injuries, accident rate {rate} per million train-miles. FRA inspection findings: {findings}.",
        reasoning_framework="""Rail Safety Performance Metrics Framework:

1. FRA REPORTABLE INCIDENTS (49 CFR 225)
   - Train accidents: derailment, collision, $10,500+ damage threshold (2022)
   - Highway-rail crossing incidents: grade crossing collisions
   - Employee injuries: days away from work, restricted duty, medical treatment
   - Reporting: FRA Form 6180.54 (accidents), 6180.55 (crossing), 6180.98 (injuries)

2. ACCIDENT RATE CALCULATION
   - Rate = (Accidents / Train-Miles) * 1,000,000
   - Industry average: ~2-3 train accidents per million train-miles
   - Class I best-in-class: <2.0, worst: >4.0
   - Trend: declining over decades (improved track, equipment, PTC)

3. INJURY FREQUENCY RATE
   - Rate = (Injuries / Employee-Hours) * 200,000
   - 200,000 = 100 employees working 40 hrs/week for 50 weeks
   - Industry average: ~2-3 injuries per 200,000 employee-hours
   - Leading indicators: near-miss reporting, safety audits

4. FRA INSPECTION PROGRAM
   - Track inspectors: inspect track, bridges, signals (spot checks)
   - Operating Practices: observe train operations, crew compliance
   - Hazmat: inspect hazmat tank cars, placarding, training
   - Motive Power & Equipment: inspect locomotives, freight cars
   - Findings: defects, violations, civil penalties ($1,000-$100,000 per violation)

5. SAFETY MANAGEMENT SYSTEMS (SMS)
   - Proactive: risk assessment, hazard identification, mitigation
   - Required: passenger railroads (FRA SMS rule, 49 CFR 270)
   - Voluntary: freight railroads (but encouraged)
   - Components: safety policy, risk management, assurance, promotion

6. PUBLIC REPORTING AND TRANSPARENCY
   - FRA accident database: publicly accessible, searchable
   - Annual safety statistics: FRA Office of Safety Analysis
   - Media attention: high-profile accidents (derailments, hazmat releases)
   - STB oversight: service quality, but FRA is primary safety regulator

Rail safety has improved dramatically: 1970s = 10,000+ accidents/year, 2020s = 1,000+
accidents/year. PTC mandate (2008) targeted passenger rail and TIH corridors.
Human factors (crew error) remain leading cause (~40% of accidents). Track defects
(~30%), equipment failure (~20%), signal/other (~10%). FRA's risk-based inspection
program focuses resources on high-risk railroads and corridors. Short lines have
higher accident rates (less capital for maintenance) but lower absolute accident
counts (lower traffic). Safety culture is critical: railroads with strong safety
leadership have measurably better outcomes.""",
        key_factors=[
            "FRA reportable incidents (Form 54, 55, 98)",
            "Accident rate (per million train-miles)",
            "Injury frequency rate (per 200,000 employee-hours)",
            "FRA inspection findings and violations",
            "Safety Management Systems (SMS)"
        ],
        primary_authority=[
            "FRA Safety Statistics (Office of Safety Analysis)",
            "49 CFR 225 - Accident Reporting",
            "49 CFR 270 - System Safety Program (SMS)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All U.S. railroads under FRA jurisdiction"
    ),

    DoctrineBlock(
        topic="High-Speed Rail Corridor Planning and Engineering Standards",
        keywords=["high-speed rail", "HSR", "FRA Tier 3", "geometry", "grade separation"],
        conclusion_template="HSR corridor {corridor}: design speed {speed} mph (FRA Tier {tier}), alignment {alignment}, grade max {grade}%, curve radius min {radius} ft. Cost ${cost}B.",
        reasoning_framework="""High-Speed Rail Corridor Planning Framework:

1. FRA SPEED TIER CLASSIFICATIONS
   - Tier I: < 80 mph (conventional passenger rail)
   - Tier II: 80-125 mph (higher-speed rail, Amtrak NEC)
   - Tier III: > 125 mph (true high-speed rail, requires FRA waiver or EIS)
   - FRA vs FTA: FRA regulates railroad safety, FTA funds transit

2. GEOMETRIC DESIGN STANDARDS
   - Curve radius: R (ft) = 0.067 * V^2 / (E + U)
     * V = speed (mph), E = superelevation (inches), U = unbalance (inches)
   - Example: 220 mph requires R > 25,000 ft (4.7 miles) for 6 in. super + 3 in. unbalance
   - Grade: max 3.5% for freight compatibility, 1.5% for pure HSR
   - Vertical curves: min 30,000 ft radius for smooth ride quality

3. GRADE SEPARATION REQUIREMENTS
   - 100% grade separation: no at-grade crossings (FRA Tier III requirement)
   - Fencing: prevent trespassing, wildlife intrusion
   - Overpasses: roads/trails cross over HSR (preferred)
   - Underpasses: HSR dives under existing roads (expensive, drainage issues)
   - Wildlife crossings: dedicated passages every 1-3 miles in rural areas

4. RIGHT-OF-WAY AND ALIGNMENT SELECTION
   - ROW width: 100-150 ft for double-track HSR + emergency access
   - Alignment: minimize curves, grades, property impacts
   - Station spacing: 30-60 miles for regional HSR, 100+ miles for express
   - Urban sections: tunnel (very expensive, $200-500M per mile)

5. SIGNALING AND TRAIN CONTROL
   - ETCS Level 2: European standard, moving block, 3-4 min headways
   - ACSES: Amtrak NEC system, speed enforcement
   - CBTC: Communications-Based Train Control, used on transit
   - Positive Train Control (PTC): U.S. mandate, prevents collisions/overspeeds

6. COST ESTIMATION AND FUNDING
   - Per-mile cost: $50-150M (mostly rural, at-grade), $200-500M (urban, tunnel/elevated)
   - Rolling stock: $5-15M per car (8-10 car trainsets)
   - Total project: California HSR = $105B (520 miles), Texas Central = $20B (240 miles)
   - Funding: federal grants (limited), state bonds, private investment (rare in U.S.)

U.S. HSR status: no operating true HSR (>150 mph revenue service). Amtrak Acela
reaches 150 mph on limited NEC sections. California HSR under construction (delayed,
over budget). Brightline (Florida) is 125 mph max (higher-speed, not true HSR).
Texas Central (Dallas-Houston) proposed 205 mph, private funding, regulatory
battles. Barrier: huge capital cost, land acquisition, political opposition,
and low ridership projections vs air/auto. Success factors: high population
density corridor, supportive state government, realistic cost/schedule, and
public-private partnership. Europe/Asia context not transferable: U.S. has lower
density, car culture, and limited rail experience.""",
        key_factors=[
            "FRA Tier III (> 125 mph) requirements",
            "Geometric design (curve radius, grade)",
            "100% grade separation",
            "Cost ($50-500M per mile)",
            "Funding and political support"
        ],
        primary_authority=[
            "FRA Track Safety Standards (49 CFR 213)",
            "FRA High-Speed Rail Strategic Plan",
            "AREMA Manual Chapter 5 - High-Speed Track Design"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="All U.S. high-speed rail corridor planning"
    ),

    DoctrineBlock(
        topic="Rail Infrastructure Asset Management and Life-Cycle Costing",
        keywords=["asset management", "life-cycle cost", "SOGR", "TAM", "FTA"],
        conclusion_template="Asset management: {asset} has {age} years remaining useful life, replacement cost ${cost}M. SOGR backlog ${backlog}M. TAM targets: {targets}.",
        reasoning_framework="""Rail Infrastructure Asset Management Framework:

1. STATE OF GOOD REPAIR (SOGR)
   - Definition: all assets functioning as designed, minimal service disruptions
   - SOGR backlog: deferred maintenance, assets past useful life
   - FTA reporting: transit agencies must report SOGR annually
   - Amtrak NEC backlog: ~$40B (2022 estimate)

2. TRANSIT ASSET MANAGEMENT (TAM) PLANS (FTA)
   - Required: all FTA grant recipients (49 CFR 625)
   - Components: asset inventory, condition assessment, investment prioritization
   - Performance targets: % assets in good/fair condition vs poor
   - Tier I agencies (> $100M): individual TAM plan
   - Tier II agencies (< $100M): participate in group TAM plan

3. USEFUL LIFE BY ASSET CLASS
   - Rail: 30-50 years (depends on tonnage, maintenance)
   - Ties: 30-40 years (concrete), 20-30 years (wood)
   - Ballast: 20-30 years (cleaning/renewal needed)
   - Bridges: 50-100 years (steel/concrete, with maintenance)
   - Signals: 20-40 years (electronics obsolescence)
   - Rolling stock: 25-40 years (rail cars), 15-25 years (buses)

4. LIFE-CYCLE COST ANALYSIS
   - Total cost: capital + operating + maintenance + disposal - residual value
   - Discount rate: 3-7% (OMB guidance)
   - Scenario comparison: new build vs rehab vs replace
   - Example: new bridge $20M, rehab existing $5M, but rehab only adds 10 years life

5. PREVENTIVE MAINTENANCE STRATEGIES
   - Reactive: fix when broken (highest life-cycle cost)
   - Preventive: scheduled inspections, planned replacements (lower cost)
   - Predictive: monitor condition, replace based on actual degradation (lowest cost)
   - Example: rail grinding every 5-10 years prevents defects, extends rail life 20%

6. INVESTMENT PRIORITIZATION
   - Risk matrix: likelihood × consequence of failure
   - Service criticality: mainline > branch, passenger > freight
   - Cost-effectiveness: cost per additional service year
   - Regulatory compliance: FRA track standards, ADA, seismic retrofit

Asset management is data-driven: GIS inventory, condition ratings, failure rates,
cost models. Transit agencies use TERM (Transit Economic Requirements Model) to
forecast SOGR needs. Class I railroads use proprietary systems (e.g., BNSF's
ARES - Asset Reliability Engineering System). Short lines often lack sophisticated
asset management - rely on FRA inspection to identify defects. Deferred maintenance
is a major issue: Amtrak NEC, NYC subway, many commuter rail systems have multi-billion
dollar SOGR backlogs. Political challenge: maintenance is not glamorous, hard to
fund vs new projects.""",
        key_factors=[
            "State of Good Repair (SOGR) backlog",
            "Transit Asset Management (TAM) plan",
            "Useful life by asset class",
            "Life-cycle cost analysis",
            "Preventive vs reactive maintenance"
        ],
        primary_authority=[
            "FTA TAM Final Rule (49 CFR 625)",
            "FTA TERM (Transit Economic Requirements Model)",
            "AREMA Manual Chapter 4 - Rail Maintenance"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All rail infrastructure asset management programs"
    ),

    # Add 3 more blocks to reach 25+ target
    DoctrineBlock(
        topic="Rail Cybersecurity and SCADA System Protection",
        keywords=["cybersecurity", "SCADA", "PTC", "OT security", "rail hacking"],
        conclusion_template="Cybersecurity assessment: {system} has {vulnerabilities} vulnerabilities (CVSS score {cvss}). Mitigation: {mitigation}. Compliance with {standard}.",
        reasoning_framework="""Rail Cybersecurity Framework:

1. OPERATIONAL TECHNOLOGY (OT) ATTACK SURFACE
   - SCADA: Supervisory Control and Data Acquisition (signal, switch, power)
   - PTC: Positive Train Control (train-to-wayside communication)
   - CTC: Centralized Traffic Control (dispatcher to field devices)
   - Ticketing/fare: automated fare collection, online sales
   - Back office: CAD/CAM, asset management, crew scheduling

2. THREAT VECTORS
   - Remote access: VPN, remote desktop (weak passwords, no MFA)
   - Vendor maintenance: third-party access to SCADA networks
   - Insider threat: disgruntled employees, sabotage
   - Supply chain: compromised equipment firmware (e.g., Chinese manufactured components)
   - Wireless: PTC radio (220 MHz), WiFi on trains, cellular modems

3. NIST CYBERSECURITY FRAMEWORK
   - Identify: asset inventory, risk assessment
   - Protect: access control, encryption, network segmentation
   - Detect: intrusion detection, logging, anomaly detection
   - Respond: incident response plan, forensics, recovery
   - Recover: backup/restore, business continuity, lessons learned

4. RAIL-SPECIFIC REGULATIONS
   - TSA Security Directives: freight/passenger rail cybersecurity (2021-2022)
   - FRA: no specific cyber rule yet, but safety consequences trigger oversight
   - DHS CISA: Critical Infrastructure protection, voluntary assessments
   - PTC systems: must have cybersecurity controls (AAR standards)

5. NETWORK SEGMENTATION AND AIR-GAPS
   - OT network: isolated from IT network (no direct internet connection)
   - Firewall: ICS-aware firewall between OT and IT
   - DMZ: screened subnet for data exchange
   - Physical air-gap: no network connection (manual USB transfer)
   - Remote access: jump box, MFA, VPN with strict access control

6. INCIDENT RESPONSE AND RECOVERY
   - Detection time: average 200+ days for OT breaches (very slow)
   - Containment: isolate affected systems, switch to manual operations
   - Forensics: preserve logs, identify attack vector, patch vulnerabilities
   - Recovery: restore from clean backups, validate integrity
   - Lessons learned: update procedures, train staff, improve defenses

Real incidents: 2008 Poland tram hack (teenager derailed trams using IR remote),
2015 Ukraine power grid attack (BlackEnergy malware), ransomware on SF Muni (2016,
fare system encrypted). Rail is attractive target: high public impact, aging
infrastructure, limited IT security expertise in rail workforce. TSA directives
(post-Colonial Pipeline ransomware) require: incident reporting, cybersecurity
coordinator, and vulnerability assessments. Compliance is a challenge: many rail
systems run Windows XP or older (unsupported), lack budgets for upgrades.""",
        key_factors=[
            "OT attack surface (SCADA, PTC, CTC)",
            "Threat vectors (remote access, vendor, insider)",
            "NIST Cybersecurity Framework",
            "TSA Security Directives (rail specific)",
            "Network segmentation and air-gaps"
        ],
        primary_authority=[
            "TSA SD 1580/82-2021 Series (Rail Cybersecurity)",
            "NIST Cybersecurity Framework v1.1",
            "IEC 62443 - Industrial Automation and Control Systems Security"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="All rail systems with digital control/communication"
    ),

    DoctrineBlock(
        topic="Rail Labor Agreements and Crew Scheduling Optimization",
        keywords=["labor agreement", "crew scheduling", "hours of service", "FRA", "union"],
        conclusion_template="Crew scheduling: {railroad} operates under {agreement} agreement. HOS limit {hours} hours, rest {rest} hours. Optimization saves ${savings}M/year via {method}.",
        reasoning_framework="""Rail Labor and Crew Scheduling Framework:

1. HOURS OF SERVICE (HOS) REGULATIONS (FRA 49 CFR 228)
   - Train crews: 12-hour on-duty limit (extended to 14 with dispatcher approval)
   - Minimum rest: 10 consecutive hours off-duty
   - Signal workers: 12-hour limit, 10 hours rest
   - Dispatchers: 9-hour limit (after 12-hour shifts for 6+ consecutive days)
   - Fatigue risk: violations result in civil penalties, criminal for flagrant

2. LABOR AGREEMENTS (COLLECTIVE BARGAINING)
   - UTU/SMART: United Transportation Union (conductors, brakemen)
   - BLE&T: Brotherhood of Locomotive Engineers and Trainmen
   - National agreements: wages, benefits, work rules (industry-wide)
   - Local agreements: road/yard assignments, seniority rosters
   - Disputes: National Mediation Board (NMB), Presidential Emergency Board (PEB)

3. CREW ASSIGNMENT AND SENIORITY
   - Pool service: assigned to train as needed (road crews)
   - Extra board: on-call for vacancies, vacations, sick leave
   - Assigned jobs: regular schedule (yard jobs, locals)
   - Seniority: determines choice of assignment (high seniority = better jobs)
   - Bumping: senior employee can displace junior on preferred assignment

4. CREW SCHEDULING OPTIMIZATION
   - Problem: minimize crew costs while meeting train plan and HOS limits
   - Constraints: HOS, rest, seniority, home terminal, union work rules
   - Objective function: minimize deadhead miles, overtime, extra board usage
   - Methods: integer programming, column generation, heuristics
   - Software: in-house (BNSF, UP), vendor (Optym, Quintiq)

5. TWO-PERSON CREW REQUIREMENT
   - Current: engineer + conductor (federal regulation for most trains)
   - Proposed: one-person crews (railroad cost savings, union opposition)
   - FRA: proposed rule requiring 2-person crews (safety justification)
   - Exception: yard jobs, short-line railroads (case-by-case waiver)
   - Politics: high-profile derailments increase pressure for 2-person mandate

6. LABOR COST DRIVERS
   - Wages: $80-120K/year for road crews (including overtime)
   - Benefits: health, pension (multi-employer plan), railroad retirement
   - Overtime: time-and-a-half after 8 hours (or per agreement)
   - Deadhead: pay crew to travel to/from remote terminals (non-revenue)
   - Guarantee: minimum pay even if train doesn't run (bad weather, service cuts)

Labor is 20-30% of Class I railroad operating costs. Crew availability is a major
operational constraint: if no crew available, train can't run (service delays).
PSR emphasis on longer trains and fewer crew starts reduces labor costs. Union
opposition to one-person crews is strong (safety, job loss). FRA has not finalized
two-person crew rule due to political pressure from both sides. Short lines often
have more flexible work rules (non-union or local agreements). Crew scheduling
is NP-hard problem; even small optimizations (1-2% cost reduction) = $10-50M/year
for Class I railroads.""",
        key_factors=[
            "Hours of Service (12-hour limit, 10-hour rest)",
            "Union agreements (UTU/SMART, BLE&T)",
            "Crew scheduling optimization (minimize deadhead, overtime)",
            "Two-person crew requirement (regulatory debate)",
            "Labor cost (20-30% of operating expenses)"
        ],
        primary_authority=[
            "FRA Hours of Service Regulations (49 CFR 228)",
            "National Railway Labor Act (RLA)",
            "BLET/SMART National Agreements"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All U.S. railroads with unionized crews"
    ),
]


# ============================================================================
# CORE ENGINE CLASS
# ============================================================================

class RAIL08Engine:
    """RAIL08 Rail Network Planning Intelligence Engine."""

    def __init__(self):
        """Initialize engine."""
        self.engine_name = "RAIL08_rail_network_planning"
        self.version = "1.0.0"
        self.port = 9214
        self.start_time = time.time()

        # Metrics
        self.queries_processed = 0
        self.total_response_time = 0.0
        self.errors = 0
        self.cache_hits = 0

        # Configure logger
        logger.remove()
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
            level="INFO"
        )
        logger.add(
            f"O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/{self.engine_name}/audit_{datetime.now():%Y%m%d}.jsonl",
            format="{message}",
            level="INFO",
            rotation="100 MB"
        )

        logger.info(f"{self.engine_name} v{self.version} initializing on port {self.port}")

    # ========================================================================
    # TIE-20 COMPONENT: THREE LAYER RESPONSE
    # ========================================================================

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
        context: Optional[Dict[str, Any]]
    ) -> Tuple[str, List[str], TelemetryData]:
        """
        Three-layer response strategy:
        1. Doctrine cache (0-200ms) - pre-compiled expertise
        2. Semantic retrieval (200-2000ms) - vector search fallback
        3. Deep analysis (2000ms+) - full reasoning synthesis
        """
        start = time.time()
        query_hash = hashlib.sha256(query.encode()).hexdigest()[:16]

        # Layer 1: Doctrine Cache
        triggered_doctrines = self._search_doctrine_cache(query)
        if triggered_doctrines:
            self.cache_hits += 1
            answer = self._synthesize_from_doctrines(triggered_doctrines, query, mode, zone)
            confidence = self._determine_confidence(triggered_doctrines, context)
            doctrines_applied = [d.topic for d in triggered_doctrines]

            telemetry = TelemetryData(
                query_hash=query_hash,
                mode=mode,
                zone=zone,
                cache_hit=True,
                semantic_search_ms=None,
                deep_analysis_ms=None,
                total_ms=(time.time() - start) * 1000,
                doctrines_triggered=doctrines_applied,
                confidence=confidence,
                determinism_hash=self._compute_determinism_hash(query, answer)
            )

            return answer, doctrines_applied, telemetry

        # Layer 2: Semantic Search (fallback if no cache hit)
        semantic_start = time.time()
        semantic_results = self._semantic_search(query)
        semantic_ms = (time.time() - semantic_start) * 1000

        if semantic_results:
            answer = self._synthesize_from_semantic(semantic_results, query, mode, zone)
            confidence = ConfidenceLevel.AGGRESSIVE
            doctrines_applied = [r["topic"] for r in semantic_results]

            telemetry = TelemetryData(
                query_hash=query_hash,
                mode=mode,
                zone=zone,
                cache_hit=False,
                semantic_search_ms=semantic_ms,
                deep_analysis_ms=None,
                total_ms=(time.time() - start) * 1000,
                doctrines_triggered=doctrines_applied,
                confidence=confidence,
                determinism_hash=self._compute_determinism_hash(query, answer)
            )

            return answer, doctrines_applied, telemetry

        # Layer 3: Deep Analysis (no cache, no semantic match)
        deep_start = time.time()
        answer = self._deep_analysis(query, mode, zone, context)
        deep_ms = (time.time() - deep_start) * 1000
        confidence = ConfidenceLevel.DISCLOSURE

        telemetry = TelemetryData(
            query_hash=query_hash,
            mode=mode,
            zone=zone,
            cache_hit=False,
            semantic_search_ms=semantic_ms,
            deep_analysis_ms=deep_ms,
            total_ms=(time.time() - start) * 1000,
            doctrines_triggered=[],
            confidence=confidence,
            determinism_hash=self._compute_determinism_hash(query, answer)
        )

        return answer, [], telemetry

    # ========================================================================
    # DOCTRINE CACHE SEARCH
    # ========================================================================

    def _search_doctrine_cache(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache for matching blocks."""
        query_lower = query.lower()
        matches = []

        for doctrine in DOCTRINE_CACHE:
            # Check if any keyword appears in query
            if any(kw.lower() in query_lower for kw in doctrine.keywords):
                matches.append(doctrine)

        # Sort by relevance (number of keyword matches)
        matches.sort(
            key=lambda d: sum(1 for kw in d.keywords if kw.lower() in query_lower),
            reverse=True
        )

        return matches[:5]  # Top 5 matches

    # ========================================================================
    # SEMANTIC SEARCH (PLACEHOLDER - WOULD USE VECTOR DB IN PRODUCTION)
    # ========================================================================

    def _semantic_search(self, query: str) -> List[Dict[str, Any]]:
        """Semantic search fallback (placeholder for vector DB)."""
        # In production: query vector database, return top-k similar blocks
        # For now: empty (all handled by doctrine cache)
        return []

    # ========================================================================
    # SYNTHESIS METHODS
    # ========================================================================

    def _synthesize_from_doctrines(
        self,
        doctrines: List[DoctrineBlock],
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> str:
        """Synthesize answer from triggered doctrine blocks."""
        if mode == ResponseMode.FAST:
            # Concise answer
            primary = doctrines[0]
            return f"{primary.conclusion_template}\n\nKey factors: {', '.join(primary.key_factors[:3])}."

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready, cite authorities
            parts = []
            for doctrine in doctrines[:3]:
                parts.append(f"## {doctrine.topic}\n")
                parts.append(f"{doctrine.conclusion_template}\n")
                parts.append(f"**Authority:** {'; '.join(doctrine.primary_authority)}\n")
            return "\n".join(parts)

        else:  # MEMO
            # Full documentation
            parts = [f"# Rail Network Planning Analysis\n\n"]
            parts.append(f"**Query:** {query}\n\n")
            for doctrine in doctrines:
                parts.append(f"## {doctrine.topic}\n\n")
                parts.append(f"{doctrine.reasoning_framework}\n\n")
                parts.append(f"**Key Factors:**\n")
                for factor in doctrine.key_factors:
                    parts.append(f"- {factor}\n")
                parts.append(f"\n**Primary Authority:**\n")
                for auth in doctrine.primary_authority:
                    parts.append(f"- {auth}\n")
                parts.append("\n")
            return "".join(parts)

    def _synthesize_from_semantic(
        self,
        results: List[Dict[str, Any]],
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> str:
        """Synthesize from semantic search results."""
        return f"Semantic search results for: {query}\n(Would synthesize from vector DB results in production)"

    def _deep_analysis(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Deep analysis when no doctrine cache hit."""
        return (
            f"Deep analysis mode activated for query: {query}\n\n"
            f"No direct doctrine match found. This query requires expert review.\n"
            f"Recommend consulting FRA regulations, AREMA Manual, or industry experts."
        )

    # ========================================================================
    # CONFIDENCE DETERMINATION
    # ========================================================================

    def _determine_confidence(
        self,
        doctrines: List[DoctrineBlock],
        context: Optional[Dict[str, Any]]
    ) -> ConfidenceLevel:
        """Determine confidence level based on triggered doctrines."""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Use most conservative confidence from triggered doctrines
        confidence_order = [
            ConfidenceLevel.HIGH_RISK,
            ConfidenceLevel.DISCLOSURE,
            ConfidenceLevel.AGGRESSIVE,
            ConfidenceLevel.DEFENSIBLE
        ]

        for level in confidence_order:
            if any(d.confidence == level for d in doctrines):
                return level

        return ConfidenceLevel.DEFENSIBLE

    # ========================================================================
    # DETERMINISM HASH
    # ========================================================================

    def _compute_determinism_hash(self, query: str, answer: str) -> str:
        """Compute SHA-256 hash for reproducibility."""
        combined = f"{query}||{answer}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    # ========================================================================
    # HEALTH ENDPOINT
    # ========================================================================

    def get_health(self) -> HealthResponse:
        """Return engine health status."""
        uptime = time.time() - self.start_time
        avg_response = (
            self.total_response_time / self.queries_processed
            if self.queries_processed > 0
            else 0.0
        )
        error_rate = (
            self.errors / self.queries_processed
            if self.queries_processed > 0
            else 0.0
        )

        return HealthResponse(
            engine=self.engine_name,
            version=self.version,
            status="healthy",
            port=self.port,
            uptime_seconds=uptime,
            queries_processed=self.queries_processed,
            cache_size=len(DOCTRINE_CACHE),
            avg_response_ms=avg_response,
            error_rate=error_rate
        )

    # ========================================================================
    # QUERY HANDLER
    # ========================================================================

    def process_query(self, request: QueryRequest) -> QueryResponse:
        """Process network planning query."""
        start = time.time()

        try:
            # Three-layer response
            answer, doctrines_applied, telemetry = self.three_layer_response(
                request.query,
                request.mode,
                request.zone,
                request.context
            )

            # Extract key factors and authorities
            triggered = [d for d in DOCTRINE_CACHE if d.topic in doctrines_applied]
            key_factors = []
            authorities = []
            for doctrine in triggered:
                key_factors.extend(doctrine.key_factors[:3])
                authorities.extend(doctrine.primary_authority)

            # Apply epistemic guardrails
            answer = self._apply_epistemic_guardrails(answer)

            # Log to audit trail
            self._log_audit_trail(request, answer, telemetry)

            # Update metrics
            elapsed = time.time() - start
            self.queries_processed += 1
            self.total_response_time += elapsed

            return QueryResponse(
                answer=answer,
                mode=request.mode,
                confidence=telemetry.confidence,
                doctrines_applied=doctrines_applied,
                key_factors=list(set(key_factors))[:10],
                authority_citations=list(set(authorities))[:10],
                telemetry=telemetry,
                determinism_hash=telemetry.determinism_hash,
                timestamp=datetime.now().isoformat()
            )

        except Exception as e:
            self.errors += 1
            logger.error(f"Query processing error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # ========================================================================
    # EPISTEMIC GUARDRAILS
    # ========================================================================

    def _apply_epistemic_guardrails(self, answer: str) -> str:
        """Apply epistemic guardrails to prevent banned phrases."""
        for phrase in BANNED_PHRASES:
            if phrase.lower() in answer.lower():
                logger.warning(f"Banned phrase detected: {phrase}")
                answer = answer.replace(phrase, "[EXPERTISE APPLIED]")
        return answer

    # ========================================================================
    # AUDIT TRAIL
    # ========================================================================

    def _log_audit_trail(
        self,
        request: QueryRequest,
        answer: str,
        telemetry: TelemetryData
    ) -> None:
        """Log query to JSONL audit trail."""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "query_hash": telemetry.query_hash,
            "query": request.query,
            "mode": request.mode.value,
            "zone": request.zone.value,
            "answer_preview": answer[:200],
            "doctrines_triggered": telemetry.doctrines_triggered,
            "confidence": telemetry.confidence.value,
            "cache_hit": telemetry.cache_hit,
            "total_ms": telemetry.total_ms,
            "determinism_hash": telemetry.determinism_hash
        }
        logger.info(json.dumps(audit_entry))


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="RAIL08 Rail Network Planning Engine",
    version="1.0.0",
    description="TIE-grade rail network planning intelligence"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Global engine instance
ENGINE = RAIL08Engine()


@APP.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return ENGINE.get_health()


@APP.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Process network planning query."""
    return ENGINE.process_query(request)


@APP.get("/")
async def root():
    """Root endpoint."""
    return {
        "engine": "RAIL08_rail_network_planning",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": ["/health", "/query"]
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting RAIL08 Rail Network Planning Engine on port {ENGINE.port}")
    uvicorn.run(
        APP,
        host="127.0.0.1",
        port=ENGINE.port,
        log_level="info"
    )
