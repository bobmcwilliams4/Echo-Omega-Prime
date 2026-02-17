"""
RAIL05 Passenger Rail Operations Intelligence Engine
TIE-Grade Autonomous Analysis System

Domain: Passenger rail operations, scheduling optimization, capacity planning,
        fare structures, station design, passenger flow modeling, service quality

Port: 9211
Version: 1.0.0
Architecture: TIE-20 Components (full autonomous intelligence)

This engine provides expert analysis of passenger rail operations including:
- Cyclic timetabling and schedule optimization (PESP models)
- Rolling stock assignment and capacity planning
- Crew scheduling and labor regulations
- Station design and passenger flow analysis
- Fare structures (zone-based, distance-based, integration)
- Service quality metrics (OTP, load factor, reliability)
- Platform screen doors and safety systems
- ADA/accessibility compliance
- Positive Train Control (PTC) for passenger operations
- FRA passenger safety regulations
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Literal
from dataclasses import dataclass, field, asdict
from enum import Enum

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger


# ============================================================================
# ENUMERATIONS AND DATA STRUCTURES
# ============================================================================

class ResponseMode(str, Enum):
    """Response mode selection"""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    """Confidence stratification levels"""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    """Analysis position zones"""
    PLANNING = "PLANNING"
    OPERATIONS = "OPERATIONS"
    AUDIT = "AUDIT"


class IssueCategory(str, Enum):
    """Passenger rail operation issue categories"""
    SCHEDULING = "SCHEDULING"
    CAPACITY = "CAPACITY"
    ROLLING_STOCK = "ROLLING_STOCK"
    CREW = "CREW"
    STATIONS = "STATIONS"
    FARES = "FARES"
    SERVICE_QUALITY = "SERVICE_QUALITY"
    SAFETY = "SAFETY"
    ACCESSIBILITY = "ACCESSIBILITY"
    INTEGRATION = "INTEGRATION"
    REGULATIONS = "REGULATIONS"
    OPERATIONS = "OPERATIONS"


class AuthorityLevel(str, Enum):
    """Authority hierarchy for passenger rail regulations"""
    FRA_REGULATION = "FRA_REGULATION"
    STATE_PUC = "STATE_PUC"
    ADA_STANDARD = "ADA_STANDARD"
    INDUSTRY_STANDARD = "INDUSTRY_STANDARD"
    BEST_PRACTICE = "BEST_PRACTICE"
    ENGINEERING_JUDGMENT = "ENGINEERING_JUDGMENT"


@dataclass
class DoctrineBlock:
    """
    Pre-compiled expert reasoning block for passenger rail operations.
    Each block represents 40-80 lines of deep domain expertise.
    """
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
    authority_level: AuthorityLevel
    fact_fragility_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = asdict(self)
        result['confidence'] = self.confidence.value
        result['issue_category'] = self.issue_category.value
        result['authority_level'] = self.authority_level.value
        return result


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """Passenger rail operations query request"""
    query: str = Field(..., min_length=10, description="Operation analysis question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis context zone")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class QueryResponse(BaseModel):
    """Passenger rail operations analysis response"""
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    answer: str
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    authority_chain: List[str]
    fact_fragility_score: float
    determinism_hash: str
    timestamp: str
    response_time_ms: float


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    avg_response_time_ms: float


# ============================================================================
# DOCTRINE CACHE - 25+ REAL PASSENGER RAIL OPERATIONS BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    DoctrineBlock(
        topic="Cyclic Timetabling and PESP Model",
        keywords=["cyclic timetable", "PESP", "periodic event scheduling", "clock-face schedule", "headway optimization", "transfer synchronization", "timetable periodicity"],
        conclusion_template="Cyclic timetabling using the Periodic Event Scheduling Problem (PESP) model provides mathematically optimal schedules with regular intervals, enabling passenger memorization of departure times and simplified transfer planning. Clock-face schedules (e.g., trains every 15, 20, or 30 minutes) enhance usability and operational efficiency.",
        reasoning_framework="""
CYCLIC TIMETABLING ANALYSIS:

1. PESP Mathematical Foundation:
   - Decision variables: Event times modulo period (T)
   - Constraints: Process time bounds [l_ij, u_ij] for each activity
   - Periodic tension: x_j - x_i - p_ij*T in [l_ij, u_ij]
   - Objective: Minimize passenger travel time and operational costs
   - NP-hard problem requiring heuristic or constraint programming solvers

2. Clock-Face Scheduling Benefits:
   - Passenger convenience: Easy memorization (e.g., trains at :15 and :45)
   - Transfer optimization: Synchronized arrivals at hubs
   - Operational simplicity: Repeating crew and rolling stock diagrams
   - Robustness: Regular patterns absorb minor delays better
   - Marketing advantage: "Every 15 minutes" is memorable slogan

3. Headway Optimization:
   - Peak period: Minimum safe headway constrained by signaling (typically 2-4 min)
   - Off-peak: Longer headways (15-30 min) balance service and cost
   - Express/local mixing: Overtaking requires careful scheduling
   - Platform capacity: Multiple services sharing platforms need coordination
   - Rolling stock availability: Turnaround times dictate minimum cycle

4. Transfer Synchronization:
   - Hub-and-spoke networks: Timed arrivals to minimize connection wait
   - Integrated timetabling: Coordinate multiple lines (Taktfahrplan)
   - Maximum connection time: Typically 5-10 min to avoid passenger frustration
   - Missed connection protection: Next service timing critical for reliability
   - Cross-platform transfers: Same-side arrival/departure ideal

5. Regularity vs. Flexibility:
   - Strict periodicity: Easier to solve, less adaptable to demand variation
   - Demand-driven adjustments: Peak hour service increases within cyclic framework
   - Special events: Temporary departures from regular schedule
   - Maintenance windows: Cyclic schedule simplifies possession planning
   - Disruption recovery: Return to cyclic pattern faster than ad-hoc schedules

6. Software Tools:
   - CADANS, DONS, TACT: PESP solvers for cyclic timetabling
   - Constraint programming (CP) and mixed-integer programming (MIP)
   - Heuristic methods: Simulated annealing, genetic algorithms
   - Validation: Simulation of passenger flows and delay propagation
   - Iterative refinement: Adjust bounds based on operational feedback

7. Implementation Challenges:
   - Infrastructure constraints: Single-track sections, junctions, platform limits
   - Heterogeneous fleet: Different acceleration, speed, dwell time characteristics
   - Uneven demand: Peaks may require capacity beyond cyclic headway minimum
   - Labor agreements: Crew shift patterns may conflict with optimal cycles
   - Political pressure: Local communities demand specific stop patterns
        """,
        key_factors=[
            "Period length (T) selection balances convenience and capacity",
            "Process time bounds derived from infrastructure and rolling stock",
            "Transfer time windows at hubs critical for network utility",
            "Conflict resolution at single-track or junction constraints",
            "Demand peaks may require overlay express services",
            "Crew and rolling stock diagrams must repeat within period",
            "Robustness to delays: cyclic schedules recover faster"
        ],
        primary_authority=[
            "Serafini and Ukovich (1989): Mathematical model for PESP",
            "Liebchen (2008): Periodic timetabling and optimization",
            "Odijk (1996): Cyclic railway timetabling using constraint programming"
        ],
        burden_holder="Transit agency planning department",
        adversary_position="Ad-hoc timetables allow more flexibility for demand variation",
        counter_arguments=[
            "Cyclic schedules may not optimally serve highly peaked demand",
            "Rigid periodicity reduces ability to respond to real-time disruptions",
            "PESP is NP-hard; finding optimal solutions is computationally expensive",
            "Transfer synchronization may force suboptimal headways on some lines",
            "Special events and maintenance require exceptions to cyclic pattern"
        ],
        resolution_strategy="Use PESP for base cyclic timetable, overlay peak-hour express services, maintain transfer synchronization at major hubs, validate with passenger flow simulation, allow controlled exceptions for planned events.",
        entity_scope="Commuter rail, regional rail, metro systems with regular service patterns",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="PESP is proven mathematical framework; implementation depends on data quality and constraint accuracy",
        controlling_precedent="European integrated timetabling (Switzerland, Netherlands) demonstrates effectiveness",
        issue_category=IssueCategory.SCHEDULING,
        authority_level=AuthorityLevel.INDUSTRY_STANDARD,
        fact_fragility_score=0.25
    ),

    DoctrineBlock(
        topic="Rolling Stock Assignment and Fleet Optimization",
        keywords=["rolling stock assignment", "fleet planning", "trainset utilization", "consist formation", "maintenance cycles", "fleet size", "unit coupling"],
        conclusion_template="Rolling stock assignment optimizes fleet utilization by matching trainset capacity to passenger demand, minimizing deadheading and maintenance downtime, while ensuring adequate spare ratio for reliability. Efficient assignment reduces capital costs and operational expenses.",
        reasoning_framework="""
ROLLING STOCK ASSIGNMENT ANALYSIS:

1. Fleet Sizing Methodology:
   - Service requirement: Number of trainsets in revenue service during peak
   - Maintenance reserve: Typically 15-25% for scheduled and unscheduled maintenance
   - Spare ratio: Additional units for failures, vandalism, accidents (5-10%)
   - Growth contingency: Future service expansion or ridership growth
   - Capital cost vs. operational flexibility tradeoff

2. Consist Formation:
   - Fixed consists: Permanently coupled trainsets (simpler operations, less flexibility)
   - Variable consists: Coupling/decoupling based on demand (more complex, higher utilization)
   - Peak augmentation: Add cars for peak periods, store off-peak
   - Locomotive-hauled vs. EMU/DMU: Different operational characteristics
   - Accessibility requirements: Low-floor, wheelchair spaces, bike capacity

3. Timetable-Driven Assignment:
   - Diagram construction: Sequence of trips assigned to each trainset
   - Turnaround time: Cleaning, inspection, driver changeover (typically 10-20 min)
   - Deadhead movements: Non-revenue travel to depots or balance fleet
   - Depot allocation: Overnight storage location based on start-of-day requirements
   - Maintenance windows: Schedule inspections during off-peak or overnight

4. Demand Matching:
   - Peak hour capacity: Sufficient seats/standing room to meet load standards
   - Off-peak efficiency: Avoid running empty or lightly loaded trains
   - Directional imbalance: Reverse-peak demand often much lower
   - Event-driven surges: Sports, concerts, holidays require flexible capacity
   - Real-time adjustments: Insert or cancel services based on actual loads

5. Maintenance Integration:
   - Planned inspections: Daily (A-check), weekly (B-check), monthly (C-check), annual (D-check)
   - Mileage-based triggers: Brake inspections, wheel truing, bogie overhaul
   - Reliability-centered maintenance: Predictive monitoring reduces unscheduled failures
   - Depot capacity: Inspection pits, washing plants, heavy maintenance shops
   - Parts inventory: Balance spare parts cost vs. downtime risk

6. Optimization Models:
   - Integer programming: Assign trainsets to diagram to minimize cost
   - Column generation: Handle large number of feasible diagrams
   - Heuristic methods: Greedy assignment, simulated annealing
   - Multi-objective: Balance capital cost, operating cost, service quality
   - Stochastic models: Account for delay and failure probability

7. Operational Constraints:
   - Trainset compatibility: Not all units can run on all routes (gauge, electrification, loading gauge)
   - Crew familiarity: Training requirements for different fleet types
   - Passenger experience: Consistent equipment reduces confusion
   - Energy efficiency: Newer units may be more efficient; prioritize for high-mileage diagrams
   - Political commitments: New trains often promised for specific routes
        """,
        key_factors=[
            "Fleet size = service requirement + maintenance reserve + spare ratio",
            "Consist length matched to peak demand to avoid overcrowding",
            "Turnaround time includes cleaning, inspection, crew change",
            "Maintenance cycles integrated into diagram planning",
            "Deadhead movements minimized to reduce non-revenue mileage",
            "Variable consists increase flexibility but require coupling infrastructure",
            "Spare ratio balances reliability and capital cost"
        ],
        primary_authority=[
            "Cordeau et al. (1998): Survey of optimization problems in train planning",
            "Peeters and Kroon (2008): Rolling stock circulation optimization",
            "APTA rolling stock utilization metrics and benchmarks"
        ],
        burden_holder="Transit agency fleet management department",
        adversary_position="Buy more trains to ensure ample capacity at all times",
        counter_arguments=[
            "Large spare ratio is financially unsustainable for capital-constrained agencies",
            "Variable consists add operational complexity and coupling/decoupling time",
            "Real-time load data often unavailable for dynamic assignment",
            "Political pressure to deploy new trains may override optimization",
            "Maintenance schedule disruptions force suboptimal substitutions"
        ],
        resolution_strategy="Use optimization models for base assignment, maintain 10-15% spare ratio, integrate maintenance windows into diagrams, validate with simulation, allow manual overrides for operational reality.",
        entity_scope="All passenger rail operators with multiple trainsets",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Optimization models are well-established; spare ratio depends on reliability data",
        controlling_precedent="European and Asian operators achieve 10-12% spare ratios with high reliability",
        issue_category=IssueCategory.ROLLING_STOCK,
        authority_level=AuthorityLevel.INDUSTRY_STANDARD,
        fact_fragility_score=0.20
    ),

    DoctrineBlock(
        topic="Crew Scheduling and Labor Compliance",
        keywords=["crew scheduling", "crew rostering", "labor agreements", "hours of service", "duty time", "rest periods", "crew depot", "train operator assignment"],
        conclusion_template="Crew scheduling must balance operational efficiency with complex labor agreements, hours-of-service regulations, and crew welfare. Optimized rosters minimize labor costs while ensuring compliance with FRA regulations (for freight/Amtrak) or local transit labor rules, and maintaining adequate rest periods for safety.",
        reasoning_framework="""
CREW SCHEDULING ANALYSIS:

1. Regulatory Framework:
   - FRA Hours of Service Act (49 USC 21103): 12-hour max duty, 10-hour rest (freight/intercity)
   - FTA labor protections: Section 13(c) requires protective arrangements for transit workers
   - State labor laws: Overtime, meal breaks, maximum consecutive days
   - ADA reasonable accommodation: Scheduling flexibility for disabled crew members
   - Collective bargaining agreements: Often more restrictive than regulations

2. Duty Definition:
   - Sign-on to sign-off: Includes pre-trip inspection, post-trip paperwork
   - Paid travel time: Deadhead movements, repositioning between depots
   - Meal breaks: Must be provided within duty period (typically 30 min unpaid)
   - Standby time: On-call crew may count as partial duty hours
   - Training and qualification: Recurrent training, route familiarity, new equipment

3. Roster Construction:
   - Duties: Sequence of trips, including sign-on, breaks, sign-off times
   - Runs: Multi-day pattern of duties assigned to a crew member
   - Lines of work: Fixed assignments for bidding seniority
   - Extra board: Unassigned pool to cover absences, surges, disruptions
   - Vacation and leave: Reduce available crew, require coverage planning

4. Optimization Objectives:
   - Minimize total crew cost: Regular hours, overtime, penalty pay
   - Minimize number of crew members: Efficient utilization reduces headcount
   - Maximize crew satisfaction: Predictable schedules, preferred shifts, weekends off
   - Ensure coverage: No uncovered duties, adequate extra board
   - Comply with all labor agreements: Seniority, work rules, bidding processes

5. Operational Constraints:
   - Depot assignment: Crew must start/end at their home depot
   - Route qualification: Crew must be trained on specific routes
   - Traction type: Different qualifications for electric, diesel, dual-mode
   - Equipment type: Some crew only qualified on certain trainsets
   - Maximum spread: Time between first and last trip (typically 10-12 hours)
   - Minimum turnaround: Rest between duties (typically 8-10 hours)

6. Disruption Handling:
   - Real-time reassignment: Delays cause crew to exceed hours of service
   - Relief points: Locations where crew can be changed mid-route
   - Taxi/deadhead: Transport crew to relief points or depots
   - Canceled services: Crew may be reassigned or sent home (guarantee pay issue)
   - Extra board callout: Minimum notice period (often 2 hours)

7. Software and Methods:
   - Column generation: Generate feasible duties, select optimal subset
   - Branch-and-price: Exact optimization for medium-sized problems
   - Heuristic methods: Large-scale rosters require meta-heuristics
   - Bidding systems: Crew select preferred lines by seniority
   - Fairness metrics: Ensure equitable distribution of undesirable shifts
        """,
        key_factors=[
            "Hours of service limits prevent fatigue-related safety incidents",
            "Labor agreements often more restrictive than federal regulations",
            "Depot location and route qualification constrain crew assignment",
            "Extra board size balances cost and coverage reliability",
            "Disruption recovery requires real-time crew reassignment capability",
            "Seniority bidding processes limit optimization flexibility",
            "Minimum rest periods are safety-critical and non-negotiable"
        ],
        primary_authority=[
            "49 USC 21103: Hours of Service Act",
            "FTA Section 13(c): Labor protections for transit workers",
            "Caprara et al. (1997): Algorithms for crew scheduling problems"
        ],
        burden_holder="Transit agency crew management and labor relations",
        adversary_position="Hire more crew to reduce stress and improve work-life balance",
        counter_arguments=[
            "Labor costs are largest operational expense; efficiency is financial necessity",
            "Overstaffing reduces individual crew member hours and income",
            "Complex optimization may produce rosters that feel unfair to crew",
            "Real-time disruptions often force manual intervention regardless of plan",
            "Labor agreements may prohibit certain optimization strategies"
        ],
        resolution_strategy="Use optimization to generate efficient base rosters, negotiate labor agreement terms that allow flexibility, maintain adequate extra board, invest in real-time crew management systems, ensure compliance with all regulations.",
        entity_scope="All passenger rail operators with employed crew (excludes automated metros)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulations are clear; optimization effectiveness depends on labor agreement terms",
        controlling_precedent="FRA and FTA enforcement actions for hours of service and labor violations",
        issue_category=IssueCategory.CREW,
        authority_level=AuthorityLevel.FRA_REGULATION,
        fact_fragility_score=0.15
    ),

    DoctrineBlock(
        topic="Station Dwell Time Analysis and Passenger Flow",
        keywords=["dwell time", "passenger boarding", "alighting", "platform width", "door width", "passenger flow rate", "crowding", "level boarding"],
        conclusion_template="Station dwell time is critical capacity determinant, governed by passenger boarding/alighting rates, door configuration, platform design, and crowding levels. Minimizing dwell time increases line capacity and schedule reliability; level boarding and wide doors are most effective interventions.",
        reasoning_framework="""
DWELL TIME AND PASSENGER FLOW ANALYSIS:

1. Dwell Time Components:
   - Door opening delay: 1-3 seconds
   - Passenger alighting: Flow rate depends on crowding, door width, steps
   - Passenger boarding: Flow rate depends on fare payment, crowding, door width
   - Door closing delay: 2-5 seconds (safety checks, obstacle detection)
   - Dwell time variability: CV (coefficient of variation) affects reliability

2. Passenger Flow Rates:
   - Level boarding (no steps): 1.5-2.0 passengers/second/door
   - One step: 1.0-1.5 passengers/second/door
   - Multiple steps: 0.5-1.0 passengers/second/door
   - Crowded conditions: Flow rate reduced by 30-50%
   - Mobility devices (wheelchairs, strollers): 15-30 seconds per device
   - Bicycles: 5-10 seconds per bike

3. Door Configuration Impact:
   - Door width: Wider doors (1.3-1.6m) allow parallel flow, higher rates
   - Number of doors: More doors distribute passenger load, reduce dwell
   - Door spacing: Affects passenger distribution along platform
   - Selective door opening: Skip doors at low-demand stations to save time
   - Platform screen doors: Increase safety but add opening/closing time

4. Platform Design:
   - Width: Minimum 3m for low-volume, 6m+ for high-volume stations
   - Circulation space: Queuing zones, vertical circulation (stairs, escalators, elevators)
   - Crowding: Level of Service (LOS) A-F based on square meters per person
   - Bottlenecks: Faregates, escalators, narrow passages limit throughput
   - Platform edge: Tactile strips, gap fillers, safety barriers

5. Fare Collection Impact:
   - Proof-of-payment: Fastest boarding (no validation at doors)
   - On-board validation: Adds 1-3 seconds per boarding passenger
   - Off-board validation: Faregates upstream of platform reduce dwell time
   - Contactless payment: Faster than magnetic stripe or cash
   - Fare integration: Cross-operator transfers require validation

6. Operational Strategies:
   - Skip-stop service: Express trains skip crowded stations, reduce dwell
   - Timed dwells: Hold trains for minimum time to even out headways
   - Passenger information: Display next train capacity to redistribute load
   - Platform assignment: Use multiple platforms for same line to spread demand
   - Staff assistance: Platform staff to assist boarding, discourage door holding

7. Capacity Calculation:
   - Minimum headway (H) = dwell time (D) + running time margin + safety buffer
   - Line capacity = 3600 / H trains per hour
   - Critical station: Longest dwell time determines system capacity
   - Dwell time reduction: 10-second reduction can increase capacity by 5-10%
   - Reliability impact: Dwell time variability causes bunching and delays
        """,
        key_factors=[
            "Level boarding eliminates steps, increases flow rate 50-100%",
            "Door width and number directly proportional to passenger throughput",
            "Crowding reduces flow rate; managing loads critical for dwell time",
            "Off-board fare payment minimizes boarding time per passenger",
            "Platform width must accommodate peak passenger volumes without LOS F",
            "Dwell time variability is enemy of schedule reliability",
            "Critical station with longest dwell limits entire line capacity"
        ],
        primary_authority=[
            "TCQSM (Transit Capacity and Quality of Service Manual), Chapter 3",
            "Weidmann (1993): Pedestrian flow characteristics",
            "Daamen and Hoogendoorn (2006): Passenger boarding and alighting times"
        ],
        burden_holder="Transit agency station design and operations departments",
        adversary_position="Accept longer dwell times rather than expensive station reconstruction",
        counter_arguments=[
            "Level boarding retrofits are extremely expensive for existing stations",
            "Platform widening may be physically impossible in constrained urban environments",
            "Passengers may not evenly distribute along platform despite information",
            "Door-holding passengers undermine even best-designed systems",
            "Special events cause unpredictable dwell time spikes"
        ],
        resolution_strategy="Prioritize level boarding for new construction and major renovations, use off-board fare payment, optimize door configuration, deploy real-time passenger information, analyze dwell time data to identify bottleneck stations, consider operational interventions (skip-stop, platform staff).",
        entity_scope="All high-frequency passenger rail systems (metro, light rail, commuter rail)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Pedestrian flow models are well-validated; dwell time prediction accuracy depends on data quality",
        controlling_precedent="World-class metros (Hong Kong, Singapore, Tokyo) achieve <30 second dwells with level boarding and wide doors",
        issue_category=IssueCategory.STATIONS,
        authority_level=AuthorityLevel.INDUSTRY_STANDARD,
        fact_fragility_score=0.20
    ),

    DoctrineBlock(
        topic="Fare Structure Design and Revenue Optimization",
        keywords=["fare structure", "zone-based fares", "distance-based fares", "flat fare", "fare integration", "elasticity", "revenue optimization", "equity"],
        conclusion_template="Fare structure design balances revenue maximization, ridership growth, equity, and operational simplicity. Zone-based and distance-based fares are economically efficient but complex; flat fares are simple but may be inequitable. Fare integration across operators increases network utility.",
        reasoning_framework="""
FARE STRUCTURE ANALYSIS:

1. Fare Structure Types:
   - Flat fare: Same price regardless of distance (simple, regressive for long trips)
   - Zone-based: Fare increases with number of zones crossed (simple, step function)
   - Distance-based: Continuous function of distance traveled (economically efficient, complex)
   - Hybrid: Flat within city core, distance-based for suburbs
   - Time-based passes: Unlimited travel for day/week/month (encourages frequent use)
   - Peak/off-peak pricing: Higher fares during congestion (demand management)

2. Economic Principles:
   - Price elasticity: Ridership response to fare changes (typically -0.2 to -0.5)
   - Revenue maximization: Price at elasticity = -1 (marginal revenue = 0)
   - Consumer surplus: Benefit to passengers from low fares
   - Cross-elasticity: Fare changes affect mode choice (auto, bus, rail)
   - Marginal cost pricing: Fares based on incremental cost of service (economic efficiency)

3. Equity Considerations:
   - Vertical equity: Low-income passengers pay disproportionate share of income
   - Horizontal equity: Similar passengers pay similar fares
   - Geographic equity: Suburban vs. urban fare burden
   - Discount programs: Senior, disabled, student, low-income reduced fares
   - Lifeline fares: Free or heavily discounted for essential trips

4. Fare Integration:
   - Cross-operator transfers: Single ticket for multi-operator journeys
   - Mode integration: Rail, bus, ferry on same fare media
   - Regional coordination: Unified fare structure across metropolitan area
   - Transfer time windows: Typically 60-120 minutes for free transfer
   - Account-based ticketing: Capping (best fare guarantee) across all trips

5. Revenue Management:
   - Yield management: Dynamic pricing based on demand (less common in transit)
   - Fare evasion: Revenue loss from non-payment (typically 2-10% of revenue)
   - Payment technology: Contactless, mobile, account-based systems
   - Revenue allocation: Distribute fare revenue among multiple operators
   - Fare box recovery ratio: Fare revenue / operating cost (30-80% range)

6. Operational Complexity:
   - Fare collection: On-board validators, faregates, proof-of-payment
   - Enforcement: Inspectors, fines, citation systems
   - Customer service: Explaining complex fare structures increases complaints
   - Technology requirements: Distance calculation, zone detection, capping algorithms
   - Change management: Fare increases are politically sensitive

7. Modeling and Optimization:
   - Demand forecasting: Predict ridership response to fare changes
   - Revenue optimization: Maximize revenue subject to ridership and equity constraints
   - Simulation: Agent-based models of passenger route choice and payment behavior
   - A/B testing: Pilot new fare structures in limited areas
   - Stakeholder engagement: Public input on fare policy changes
        """,
        key_factors=[
            "Price elasticity typically -0.2 to -0.5 for transit",
            "Flat fares are simplest but regressive for long trips",
            "Distance-based fares economically efficient but operationally complex",
            "Fare integration increases network utility and ridership",
            "Discount programs serve equity goals but reduce revenue",
            "Fare evasion losses must be balanced against enforcement cost",
            "Farebox recovery ratio varies widely by system and subsidy level"
        ],
        primary_authority=[
            "TCRP Report 95: Traveler Response to Transportation System Changes, Chapter 12 (Fares)",
            "Cervero (1990): Transit pricing and fare policy",
            "Parry and Small (2009): Optimal pricing of urban transport externalities"
        ],
        burden_holder="Transit agency revenue and planning departments, regional transit authorities",
        adversary_position="Keep fares low to maximize ridership and equity",
        counter_arguments=[
            "Low fares increase subsidy burden on taxpayers",
            "Fare revenue is critical for financial sustainability",
            "Complex fare structures may deter occasional riders",
            "Dynamic pricing may be perceived as unfair gouging",
            "Discount programs can be abused without strict verification"
        ],
        resolution_strategy="Use demand modeling to optimize fares for revenue and ridership, implement distance-based or zone fares with technology support, offer means-tested discount programs, pursue fare integration regionally, pilot fare changes before system-wide rollout, ensure clear communication of fare policy.",
        entity_scope="All fare-collecting passenger rail systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Economic models are well-established; elasticity estimates vary by context",
        controlling_precedent="London (Oyster/capping), Hong Kong (Octopus), Netherlands (OV-chipkaart) demonstrate successful fare integration",
        issue_category=IssueCategory.FARES,
        authority_level=AuthorityLevel.INDUSTRY_STANDARD,
        fact_fragility_score=0.25
    ),

    DoctrineBlock(
        topic="On-Time Performance (OTP) Metrics and Reliability",
        keywords=["on-time performance", "OTP", "reliability", "punctuality", "delay attribution", "headway regularity", "schedule adherence", "excess journey time"],
        conclusion_template="On-Time Performance (OTP) is primary service quality metric for passenger rail. Industry standard is percent of trains arriving within 5 minutes of schedule. High-frequency services use headway regularity as more relevant metric. Delay attribution distinguishes operator-caused vs. external delays.",
        reasoning_framework="""
ON-TIME PERFORMANCE ANALYSIS:

1. OTP Definition and Thresholds:
   - Industry standard: Train arrives within 5 minutes of scheduled time
   - European railways: Often use 3-minute threshold for regional, 5-15 min for long-distance
   - Commuter rail: Stricter threshold (1-3 min) due to connection sensitivity
   - Origin vs. destination: OTP typically measured at final destination
   - Intermediate stations: May track OTP at all stops to identify problem locations

2. High-Frequency Service Metrics:
   - Headway regularity: More relevant than schedule adherence for <10 min headways
   - Coefficient of variation (CV): Standard deviation / mean headway
   - Excess wait time: Actual wait time compared to expected wait (headway/2)
   - Bunching: Two trains arrive with <50% scheduled headway
   - Gapping: No train arrives for >150% scheduled headway

3. Delay Attribution:
   - Operator-caused: Rolling stock failures, crew issues, operational errors
   - Infrastructure-caused: Signal failures, track defects, power outages
   - External: Weather, trespassers, police activity, passenger incidents
   - Reactionary delay: Delay propagated from initial cause (secondary delays)
   - Primary vs. reactionary: Distinguish root cause from knock-on effects

4. Delay Propagation:
   - Schedule padding: Buffer time to absorb minor delays
   - Knock-on delays: Late train delays following train on same track
   - Crew delays: Crew exceeds hours of service due to delays
   - Platform conflicts: Delayed train blocks platform for following service
   - Recovery time: Additional running time to get back on schedule

5. Improvement Strategies:
   - Infrastructure: Eliminate bottlenecks, improve signaling, redundant systems
   - Rolling stock: Improve reliability, reduce failure rates (MDBF targets)
   - Operations: Better real-time control, faster incident response
   - Timetable design: Adequate running time margins, realistic dwell times
   - Maintenance: Predictive maintenance to prevent failures

6. Performance Targets:
   - Industry benchmarks: 90-95% OTP for well-run commuter systems
   - Contract incentives: Franchise agreements tie payment to OTP targets
   - Public transparency: Real-time OTP data published to hold operators accountable
   - Trend analysis: Monitor monthly/annual OTP trends to detect degradation
   - Comparative analysis: Benchmark against peer systems

7. Passenger Impact:
   - Perceived reliability: Consistency more important than average OTP
   - Connection misses: Delays cause missed transfers, disproportionate impact
   - Crowding: Late trains cause bunching, increased crowding on following train
   - Passenger information: Real-time updates reduce anxiety of delays
   - Compensation: Delay-repay schemes refund fares for poor OTP (UK, Germany)
        """,
        key_factors=[
            "5-minute threshold is industry standard for OTP",
            "High-frequency services should use headway regularity, not schedule adherence",
            "Delay attribution distinguishes controllable vs. uncontrollable causes",
            "Reactionary delays often exceed primary delays in total impact",
            "Adequate schedule padding reduces delay propagation",
            "Rolling stock reliability (MDBF) is critical for OTP",
            "Real-time information mitigates passenger perception of unreliability"
        ],
        primary_authority=[
            "EN 13103: European standard for railway reliability and punctuality",
            "TCRP Report 165: Transit Capacity and Quality of Service Manual, 3rd Edition",
            "Vuchic (2005): Urban Transit Operations, Planning, and Economics"
        ],
        burden_holder="Transit agency operations and performance monitoring",
        adversary_position="OTP is less important than safety and cost control",
        counter_arguments=[
            "Passengers prioritize reliability over minor schedule deviations",
            "Strict OTP targets may encourage unsafe rushing",
            "External delays are unavoidable and should not penalize operator",
            "Excessive schedule padding reduces service attractiveness",
            "Real-time information can substitute for punctuality if delays are communicated"
        ],
        resolution_strategy="Set realistic OTP targets (90-95%), use 5-minute threshold for scheduled services and headway regularity for high-frequency, attribute delays to identify improvement areas, invest in infrastructure and rolling stock reliability, publish real-time OTP data, consider delay-repay schemes.",
        entity_scope="All passenger rail operators with published schedules",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="OTP measurement is standardized; interpretation depends on service type and context",
        controlling_precedent="Japanese railways (Shinkansen) achieve 99%+ OTP; European TOCs 85-95% typical",
        issue_category=IssueCategory.SERVICE_QUALITY,
        authority_level=AuthorityLevel.INDUSTRY_STANDARD,
        fact_fragility_score=0.15
    ),

    DoctrineBlock(
        topic="Platform Screen Doors (PSD) Safety and Operations",
        keywords=["platform screen doors", "PSD", "platform edge doors", "automatic platform gates", "APG", "safety barriers", "HVAC benefits", "dwell time impact"],
        conclusion_template="Platform Screen Doors (PSD) or Automatic Platform Gates (APG) enhance safety by preventing passenger falls and suicides, enable HVAC energy savings in underground stations, but add cost, maintenance burden, and potential dwell time if door alignment is imperfect. Widely adopted for new metro systems.",
        reasoning_framework="""
PLATFORM SCREEN DOOR ANALYSIS:

1. Safety Benefits:
   - Fall prevention: Physical barrier prevents accidental falls onto tracks
   - Suicide prevention: Eliminates access to tracks for self-harm (reduces suicides by 70-90%)
   - Trespasser deterrence: Harder to access tracks for vandalism or shortcuts
   - Object prevention: Stops debris, luggage, strollers from falling onto tracks
   - Crowd management: Defines queuing zones, reduces platform edge crowding

2. Types of Platform Barriers:
   - Full-height PSD: Floor-to-ceiling barriers, enable HVAC conditioning
   - Half-height APG: Waist-height gates, lower cost, no HVAC benefit
   - Rope barriers: Minimal cost, symbolic deterrence only (not effective)
   - Sliding vs. folding: Sliding doors more common, folding for narrow platforms
   - Retrofits vs. new build: Retrofits more expensive, require platform strengthening

3. Operational Impact:
   - Door alignment: Train must stop precisely for PSD to align with train doors
   - Dwell time: Adds 1-3 seconds for PSD open/close cycle
   - Signaling integration: PSD interlock prevents train departure if doors not closed
   - Communication: CCTV and intercom for passengers trapped between doors
   - Emergency egress: Manual release for evacuation in emergencies

4. HVAC and Energy Benefits:
   - Underground stations: PSD enables air conditioning by containing platform environment
   - Energy savings: 20-40% reduction in HVAC energy by reducing tunnel airflow
   - Thermal comfort: Improved passenger experience in hot/cold climates
   - Air quality: Reduced tunnel dust and particulate matter on platforms
   - Noise reduction: PSD attenuates train noise in station

5. Cost and Maintenance:
   - Capital cost: $1-3 million per station for retrofits, $0.5-1M for new construction
   - Maintenance: Motors, sensors, safety interlocks require regular inspection
   - Reliability: Door failures can block platform access, require rapid response
   - Spare parts: Proprietary systems may have expensive or slow-to-obtain parts
   - Life cycle: 20-30 year design life, may require mid-life refurbishment

6. Operational Challenges:
   - Mixed fleet: If trainsets have different door spacing, PSD alignment is complex
   - Platform length: Short platforms may require selective door opening
   - Door width mismatch: Train doors narrower than PSD opening creates gap
   - Failure management: Door stuck open or closed requires manual intervention
   - Passenger behavior: Leaning on doors, forcing doors, vandalism

7. Regulatory and Standards:
   - No US federal requirement for PSD (unlike some Asian/European countries)
   - ADA compliance: Emergency communication must be accessible
   - Fire codes: PSD must not impede emergency egress from platform
   - Industry standards: IEEE 1474 (CBTC) and IEC 62267 (PSD) provide guidance
   - Insurance and liability: PSD reduces operator liability for falls/suicides
        """,
        key_factors=[
            "PSD reduces platform falls and suicides by 70-90%",
            "Full-height PSD enables HVAC conditioning, 20-40% energy savings",
            "Capital cost $1-3M per station for retrofits",
            "Requires precise train stopping and door alignment",
            "Maintenance and reliability critical for uninterrupted operations",
            "Mixed fleet door spacing complicates PSD implementation",
            "No US federal mandate but increasingly adopted for safety"
        ],
        primary_authority=[
            "IEC 62267: Railway applications - Platform screen doors",
            "IEEE 1474.1: CBTC system design and functional requirements",
            "APTA PSD best practices and case studies"
        ],
        burden_holder="Transit agency capital planning, engineering, and operations",
        adversary_position="PSD is too expensive for benefit; focus on passenger education",
        counter_arguments=[
            "Suicide and fall rates justify PSD investment on cost-benefit basis",
            "HVAC energy savings can offset capital cost over 10-15 years",
            "Liability and litigation risk from falls outweighs PSD cost",
            "Passenger perception of safety and modernity attracts ridership",
            "Retrofits are expensive but new construction cost is reasonable"
        ],
        resolution_strategy="Mandate PSD for all new underground metro systems, evaluate retrofit cost-benefit for existing high-risk stations (high suicide/fall rates), prioritize full-height PSD for HVAC benefits in hot/cold climates, ensure fleet standardization for door alignment, plan for maintenance and reliability.",
        entity_scope="Urban metro and light rail systems, especially underground stations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Safety benefits are proven; cost-benefit depends on fall/suicide rates and HVAC energy costs",
        controlling_precedent="Hong Kong, Singapore, Seoul, Paris, London have extensive PSD deployment with proven safety records",
        issue_category=IssueCategory.SAFETY,
        authority_level=AuthorityLevel.INDUSTRY_STANDARD,
        fact_fragility_score=0.20
    ),

    DoctrineBlock(
        topic="ADA Accessibility Compliance and Universal Design",
        keywords=["ADA compliance", "accessibility", "universal design", "wheelchair access", "level boarding", "tactile paving", "visual contrast", "audible announcements"],
        conclusion_template="ADA (Americans with Disabilities Act) mandates accessible design for all new and renovated passenger rail facilities. Key requirements include level boarding or portable lifts, tactile warning strips, visual/audible announcements, and accessible paths of travel. Universal design benefits all passengers, not just those with disabilities.",
        reasoning_framework="""
ADA ACCESSIBILITY ANALYSIS:

1. ADA Regulatory Framework:
   - ADA Title II: Public entities (transit agencies) must provide accessible service
   - 49 CFR Part 37: DOT ADA regulations for transportation
   - 49 CFR Part 38: ADA accessibility specifications for vehicles and facilities
   - DOJ 2010 ADA Standards: Architectural standards for facilities
   - Equivalent facilitation: Alternative designs that provide equal or better access

2. Vehicle Accessibility Requirements:
   - Level boarding: No vertical gap >0.5 inch, horizontal gap <3 inches (preferred)
   - Portable lifts: Required if level boarding not feasible (slow, 2-5 min per wheelchair)
   - Wheelchair spaces: Minimum 2 spaces per vehicle, more for longer consists
   - Priority seating: Clearly marked, fold-up to accommodate wheelchairs
   - Audible/visual announcements: Next stop, delays, safety messages
   - Handrails and stanchions: For standing passengers with mobility limitations

3. Station Accessibility:
   - Accessible path of travel: From street to platform without stairs
   - Elevators: Required at all stations unless waiver granted (historic, cost)
   - Escalators: Not sufficient for ADA compliance (must have elevator or ramp)
   - Tactile warning strips: Detectable warning surface at platform edge (24 inch wide)
   - Visual contrast: Platform edge marked with high-contrast color
   - Signage: Raised letters, Braille, high contrast, at accessible heights
   - Faregates: At least one wide gate (32 inch min) for wheelchairs

4. Communication Accessibility:
   - Audible announcements: Station name, next stop, doors opening side
   - Visual displays: Real-time arrival information, delay messages
   - TDD/TTY: Text telephone for customer service (legacy, now largely replaced by text/email)
   - Emergency communication: Accessible intercoms, visual alarms
   - Website/app: WCAG 2.0 AA compliance for digital information

5. Universal Design Principles:
   - Equitable use: Same means of use for all users
   - Flexibility: Accommodates wide range of preferences and abilities
   - Simple and intuitive: Easy to understand regardless of experience or language
   - Perceptible information: Communicates necessary information effectively (visual, audible, tactile)
   - Tolerance for error: Minimizes hazards and adverse consequences of accidents
   - Low physical effort: Can be used efficiently and comfortably
   - Size and space: Appropriate size and space for approach, reach, manipulation

6. Operational Practices:
   - Passenger assistance: Staff trained to assist passengers with disabilities
   - Service animals: Allowed on all vehicles and in all facilities
   - Wheelchair securement: Train operators or conductors assist with securement
   - Priority boarding: Allow wheelchair users to board first to reduce dwell time
   - Paratransit: ADA requires complementary paratransit for areas not accessible by rail

7. Compliance and Enforcement:
   - FTA compliance reviews: Periodic audits of ADA compliance
   - Complaint process: Passengers can file ADA complaints with FTA or DOJ
   - Corrective action: Agencies must remedy non-compliance within specified timeframe
   - Litigation risk: Failure to comply can result in lawsuits and consent decrees
   - Ongoing obligations: ADA compliance is continuous, not one-time
        """,
        key_factors=[
            "ADA Title II and 49 CFR Part 37/38 mandate accessible design",
            "Level boarding is preferred method for wheelchair access (0.5 inch max vertical gap)",
            "Elevators required at all new stations unless waiver granted",
            "Tactile warning strips and visual contrast at platform edge are required",
            "Audible and visual announcements must provide equivalent information",
            "Universal design benefits all passengers, not just those with disabilities",
            "Non-compliance risks FTA enforcement and litigation"
        ],
        primary_authority=[
            "ADA Title II (42 USC 12132): Public entities must provide accessible service",
            "49 CFR Part 37: DOT ADA regulations for transportation",
            "49 CFR Part 38: ADA accessibility specifications for vehicles and facilities"
        ],
        burden_holder="Transit agency planning, engineering, and operations departments",
        adversary_position="ADA compliance is too expensive; seek waivers for existing facilities",
        counter_arguments=[
            "ADA is federal law; non-compliance risks litigation and loss of federal funding",
            "Universal design improves experience for all passengers (parents with strollers, elderly, luggage)",
            "Aging population increases demand for accessible features",
            "Portable lifts are slow and unreliable; level boarding is better for all",
            "Retrofits are expensive but required for major renovations"
        ],
        resolution_strategy="Design all new facilities and vehicles for full ADA compliance from outset, prioritize level boarding for new construction and major renovations, seek FTA guidance on equivalent facilitation for challenging retrofits, train staff on accessibility and passenger assistance, monitor complaints and address promptly.",
        entity_scope="All US passenger rail systems receiving federal funding",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ADA requirements are clear federal law; application details may vary by context",
        controlling_precedent="FTA ADA compliance reviews and DOJ consent decrees define enforcement standards",
        issue_category=IssueCategory.ACCESSIBILITY,
        authority_level=AuthorityLevel.ADA_STANDARD,
        fact_fragility_score=0.10
    ),

    DoctrineBlock(
        topic="Positive Train Control (PTC) for Passenger Rail",
        keywords=["positive train control", "PTC", "ACSES", "ATC", "ATP", "ETCS", "overspeed protection", "signal compliance", "collision avoidance"],
        conclusion_template="Positive Train Control (PTC) is FRA-mandated safety system for passenger rail to prevent train-to-train collisions, overspeed derailments, and unauthorized incursions into work zones. ACSES (Advanced Civil Speed Enforcement System) is common US passenger rail PTC technology. Full interoperability with freight PTC (I-ETMS) remains challenging.",
        reasoning_framework="""
POSITIVE TRAIN CONTROL ANALYSIS:

1. PTC Regulatory Mandate:
   - Rail Safety Improvement Act of 2008: Mandated PTC on passenger rail by 2015 (extended to 2020)
   - 49 CFR Part 236 Subpart I: PTC system requirements
   - Coverage: All passenger rail lines and Class I freight lines with passenger service
   - Exemptions: Light rail, rapid transit (metros) not subject to FRA PTC mandate
   - Enforcement: FRA can shut down non-compliant railroads

2. PTC Functional Requirements:
   - Prevent train-to-train collisions: Enforce track authority limits
   - Prevent overspeed derailments: Enforce permanent and temporary speed restrictions
   - Prevent incursions into work zones: Enforce roadway worker protection limits
   - Prevent unauthorized movements through switches: Enforce switch positions
   - Interoperability: PTC systems must work across railroads (challenge for passenger/freight)

3. ACSES Technology (Amtrak/Commuter Rail):
   - Transponder-based: Balises (transponders) at track provide location and speed data
   - Continuous cab signals: Overlay on existing cab signal system
   - Overspeed enforcement: Automatic brake application if train exceeds speed limit
   - Civil speed enforcement: Enforces track geometry and temporary slow orders
   - Upgrade path: From legacy pulse-code cab signals to ACSES

4. I-ETMS Technology (Freight Railroads):
   - GPS-based: Trains determine position via GPS plus track database
   - Wayside interface units: Communicate signal and switch status to trains
   - Back office server: Centralized authority for track warrants and permissions
   - Locomotive onboard computer: Enforces speed and authority limits
   - Interoperability issues: Amtrak/commuter trains on freight tracks must support both ACSES and I-ETMS

5. PTC Implementation Challenges:
   - Cost: $10-15 billion nationwide, $2-5 million per route-mile for passenger rail
   - Spectrum: Radio frequency interference and capacity issues
   - Interoperability: Different PTC systems (ACSES, I-ETMS) require dual-equipped locomotives
   - Software complexity: Safety-critical software certification is time-consuming
   - Maintenance: New failure modes, requires skilled technicians
   - False positives: Overly conservative enforcement can cause unnecessary stops

6. Operational Impact:
   - Increased safety: Estimated to prevent 90% of signal-passed-at-danger (SPAD) incidents
   - Crew workload: Reduced cognitive load for speed enforcement, but new failure modes to manage
   - Capacity impact: Conservative PTC braking curves may reduce line capacity
   - Reliability: PTC failures can disable trains, require fallback to restricted speed operation
   - Training: Crew must be trained on PTC operation and failure management

7. International Comparison:
   - ETCS (European Train Control System): Levels 1, 2, 3 with increasing automation
   - CBTC (Communications-Based Train Control): Used for urban metros, not FRA-regulated
   - ATO (Automatic Train Operation): Grade of Automation (GoA) 1-4, up to fully driverless
   - US PTC: Less advanced than ETCS Level 2, but retrofitted to existing infrastructure
        """,
        key_factors=[
            "FRA mandates PTC on all passenger rail lines (except light rail/metro)",
            "PTC prevents train-to-train collisions, overspeed, and work zone incursions",
            "ACSES is common passenger rail PTC technology (transponder-based)",
            "Interoperability between ACSES and I-ETMS is challenging",
            "Implementation cost $10-15 billion nationwide, $2-5M per route-mile",
            "PTC improves safety but adds complexity and potential reliability issues",
            "International systems (ETCS) are more advanced but not deployed in US"
        ],
        primary_authority=[
            "Rail Safety Improvement Act of 2008 (PL 110-432): PTC mandate",
            "49 CFR Part 236 Subpart I: PTC system requirements",
            "FRA PTC implementation guidance and waivers"
        ],
        burden_holder="Passenger rail operators (Amtrak, commuter rail agencies), freight railroads hosting passenger",
        adversary_position="PTC is too expensive; existing safety systems are adequate",
        counter_arguments=[
            "PTC is federal law; non-compliance results in shutdown",
            "High-profile accidents (Chatsworth 2008) demonstrate need for PTC",
            "PTC prevents human error, which is leading cause of rail accidents",
            "Long-term safety benefits justify capital and operational costs",
            "Insurance and liability costs reduced with PTC deployment"
        ],
        resolution_strategy="Complete PTC implementation as mandated, pursue interoperability solutions for shared tracks, invest in crew training and maintenance expertise, monitor PTC reliability and address false positive enforcement, consider future upgrades to ETCS or CBTC standards for new lines.",
        entity_scope="All US passenger rail systems subject to FRA regulation (excludes light rail and rapid transit)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="PTC mandate and requirements are clear; implementation details and interoperability remain complex",
        controlling_precedent="FRA PTC Final Rule (2010) and subsequent amendments define compliance standards",
        issue_category=IssueCategory.SAFETY,
        authority_level=AuthorityLevel.FRA_REGULATION,
        fact_fragility_score=0.15
    ),

    DoctrineBlock(
        topic="Passenger Demand Forecasting and Ridership Modeling",
        keywords=["demand forecasting", "ridership modeling", "four-step model", "trip generation", "mode choice", "elasticity", "induced demand", "land use integration"],
        conclusion_template="Passenger demand forecasting uses four-step travel models (trip generation, distribution, mode choice, assignment) or activity-based models to predict ridership. Accuracy depends on quality of socioeconomic data, mode choice model calibration, and capturing induced demand effects. Land use integration critical for long-term forecasts.",
        reasoning_framework="""
PASSENGER DEMAND FORECASTING ANALYSIS:

1. Four-Step Travel Demand Model:
   - Trip generation: Predict number of trips by zone based on households, employment, demographics
   - Trip distribution: Predict origin-destination flows using gravity model
   - Mode choice: Predict share of trips by auto, transit, walk, bike using logit model
   - Trip assignment: Assign transit trips to specific routes and time periods
   - Iterative: Congestion feedback from assignment to mode choice

2. Activity-Based Models (ABM):
   - Person-day simulation: Model full daily activity pattern for each person
   - Tour-based: Primary tour (home-work-home), secondary tours, intermediate stops
   - Time use: Constrain total time available for travel and activities
   - Joint travel: Household members travel together for some activities
   - More realistic: Captures complex trip chaining and household interactions
   - Data intensive: Requires detailed household travel surveys

3. Mode Choice Modeling:
   - Multinomial logit (MNL): Probability of mode based on utility function
   - Utility = f(travel time, cost, comfort, reliability, access/egress)
   - Calibration: Estimate coefficients from revealed preference (actual behavior) or stated preference (surveys)
   - Value of time (VOT): Implicit willingness to pay to save travel time (typically $10-30/hour)
   - Cross-elasticity: How mode shares respond to changes in competing modes

4. Ridership Elasticities:
   - Fare elasticity: Typically -0.2 to -0.5 (10% fare increase reduces ridership 2-5%)
   - Service elasticity: Frequency, speed, coverage improvements increase ridership
   - Income elasticity: Higher income reduces transit share (auto ownership increases)
   - Gasoline price elasticity: Higher gas prices increase transit ridership
   - Cross-elasticity: Transit ridership responds to changes in auto travel time/cost

5. Induced Demand:
   - New transit service generates new trips that would not have occurred otherwise
   - Land use response: Transit-oriented development (TOD) increases residential and employment density near stations
   - Network effects: New line increases utility of entire network via transfers
   - Long-run elasticity: Larger than short-run as land use and auto ownership adjust
   - Forecasting challenge: Must predict land use changes, not just mode shift

6. Data Requirements:
   - Socioeconomic data: Population, households, employment by zone
   - Travel survey: Household travel behavior, mode choice, trip purpose
   - Transit service data: Routes, frequencies, fares, station locations
   - Network data: Travel times, transfer times, walking distances
   - Validation: Compare model predictions to actual ridership counts

7. Uncertainty and Sensitivity:
   - Parameter uncertainty: Mode choice coefficients, elasticities
   - Scenario uncertainty: Future population, employment, land use, fuel prices
   - Model uncertainty: Four-step vs. ABM, network representation
   - Sensitivity analysis: Test range of input assumptions
   - Forecast ranges: Report low/medium/high scenarios, not single point estimate
        """,
        key_factors=[
            "Four-step models are standard but activity-based models (ABM) more realistic",
            "Mode choice depends on travel time, cost, comfort, reliability, access/egress",
            "Fare elasticity typically -0.2 to -0.5 for transit",
            "Induced demand from land use changes critical for long-term forecasts",
            "Value of time (VOT) $10-30/hour typical for mode choice calibration",
            "Validation against actual ridership counts essential for credibility",
            "Forecast uncertainty requires sensitivity analysis and scenario ranges"
        ],
        primary_authority=[
            "TCRP Report 95: Traveler Response to Transportation System Changes",
            "FTA New Starts guidance: Travel demand forecasting for capital projects",
            "TRB Travel Forecasting Resource: Best practices and methods"
        ],
        burden_holder="Transit agency planning, consultants performing demand forecasting",
        adversary_position="Forecasts are always wrong; just build and see what happens",
        counter_arguments=[
            "Forecasts are necessary for capital investment decisions and federal funding",
            "Uncertainty can be quantified with sensitivity analysis and scenario planning",
            "Models improve with better data and calibration over time",
            "Post-opening ridership studies validate and improve future forecasts",
            "Induced demand is real and must be captured for accurate long-term forecasts"
        ],
        resolution_strategy="Use four-step or activity-based models depending on project complexity and data availability, calibrate mode choice to local travel behavior, incorporate land use scenarios for long-term forecasts, validate against observed ridership, report forecast ranges with sensitivity analysis, update forecasts as new data becomes available.",
        entity_scope="All passenger rail planning studies and capital project evaluations",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Forecasting methods are well-established but inherently uncertain; accuracy depends on data quality and scenario assumptions",
        controlling_precedent="FTA New Starts evaluation framework and forecasting guidance",
        issue_category=IssueCategory.CAPACITY,
        authority_level=AuthorityLevel.INDUSTRY_STANDARD,
        fact_fragility_score=0.35
    ),

    DoctrineBlock(
        topic="Load Factor and Crowding Management",
        keywords=["load factor", "crowding", "crush load", "standees", "seated capacity", "peak load point", "passenger comfort", "service frequency"],
        conclusion_template="Load factor (passengers / total capacity) measures vehicle utilization and crowding. Industry standards consider load factors >100% (standees) acceptable for peak periods, but passenger comfort degrades above 80-85% load. Crowding management strategies include increased frequency, larger trainsets, skip-stop service, and peak pricing.",
        reasoning_framework="""
LOAD FACTOR AND CROWDING ANALYSIS:

1. Load Factor Definition:
   - Load factor = Passengers onboard / Total capacity
   - Seated capacity: Number of seats (comfortable)
   - Crush capacity: Seats + standees at 4-6 passengers per square meter
   - Design capacity: Intermediate level (often 120-150% seated)
   - Peak load point: Location with highest ridership on route

2. Crowding Standards:
   - <60% load: Low utilization, potential for service reduction
   - 60-80% load: Comfortable, all passengers can sit during most of trip
   - 80-100% load: Some standees, beginning of discomfort
   - 100-120% load: Moderate crowding, acceptable for short peak periods
   - >120% load: Severe crowding, passenger dissatisfaction, safety concerns
   - >150% load: Crush conditions, may prevent boarding

3. Passenger Comfort Impact:
   - Personal space: <0.2 sq m/passenger is extremely uncomfortable
   - Standing duration: Acceptable for <15 min commute, not for long trips
   - Luggage and bikes: Reduce effective capacity
   - ADA wheelchair spaces: Require more space, reduce standee capacity
   - Air quality: Crowding increases CO2 levels, heat, odor

4. Crowding Measurement:
   - Automatic passenger counters (APC): Infrared or weight sensors count boardings/alightings
   - Manual counts: Surveyors count passengers at peak load point
   - Smart card data: Entry/exit taps infer ridership by segment
   - Video analytics: Computer vision counts passengers via CCTV
   - Real-time data: Display crowding levels to help passengers choose less-crowded trains

5. Crowding Management Strategies:
   - Increased frequency: Reduce headways to distribute passengers across more trains
   - Longer trainsets: Add cars to increase capacity per train (capital and operational cost)
   - Skip-stop service: Express trains relieve crowding on locals
   - Peak pricing: Higher fares during peak discourage discretionary travel
   - Demand management: Employer flex-time programs, staggered school hours
   - Information: Real-time crowding displays help passengers self-regulate

6. Service Quality Metrics:
   - Level of Service (LOS): A-F scale based on load factor and standee density
   - LOS A-B: <60% load, all passengers seated
   - LOS C: 60-85% load, some standees but comfortable
   - LOS D: 85-100% load, moderate crowding
   - LOS E: 100-120% load, heavy crowding
   - LOS F: >120% load, crush conditions, failure

7. Operational Constraints:
   - Platform length: Limits maximum trainset length
   - Signaling headway: Minimum safe separation between trains
   - Rolling stock availability: Fleet size limits frequency increases
   - Crew availability: More trains require more crew
   - Terminal capacity: Turnback and storage tracks limit frequency
        """,
        key_factors=[
            "Load factor >100% means standees; acceptable for peak periods",
            "Passenger comfort degrades above 80-85% load factor",
            "Peak load point determines capacity bottleneck",
            "Automatic passenger counters (APC) provide data for load factor analysis",
            "Increased frequency is most effective crowding relief strategy",
            "Real-time crowding information helps passengers choose less-crowded trains",
            "Level of Service (LOS) A-F scale standardizes crowding evaluation"
        ],
        primary_authority=[
            "TCQSM (Transit Capacity and Quality of Service Manual), Chapter 3",
            "APTA capacity and crowding standards",
            "Vuchic (2005): Urban Transit Operations, Planning, and Economics"
        ],
        burden_holder="Transit agency operations and service planning",
        adversary_position="Crowding is inevitable during peaks; passengers should adjust schedules",
        counter_arguments=[
            "Severe crowding drives passengers to alternative modes, reducing ridership",
            "Passenger safety and comfort are core service quality metrics",
            "Crowding data informs capital investment in additional capacity",
            "Real-time information empowers passengers to make informed choices",
            "Overcrowding can prevent wheelchair users from boarding (ADA issue)"
        ],
        resolution_strategy="Monitor load factors at peak load points using APC or manual counts, set LOS targets (e.g., LOS D or better), increase frequency or trainset length to relieve crowding, provide real-time crowding information, consider peak pricing or demand management for extreme peaks.",
        entity_scope="All high-frequency passenger rail systems with variable demand",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Load factor measurement is objective; acceptable crowding levels involve subjective passenger comfort judgments",
        controlling_precedent="World-class metros (Tokyo, Hong Kong) operate at 150-200% load during peaks but are considered extreme",
        issue_category=IssueCategory.SERVICE_QUALITY,
        authority_level=AuthorityLevel.INDUSTRY_STANDARD,
        fact_fragility_score=0.20
    ),

    DoctrineBlock(
        topic="FRA Passenger Equipment Safety Standards",
        keywords=["FRA passenger equipment", "49 CFR Part 238", "crashworthiness", "crash energy management", "buff strength", "emergency egress", "fire safety"],
        conclusion_template="FRA 49 CFR Part 238 establishes passenger equipment safety standards including crashworthiness, buff strength (800,000 lbf), fire safety, emergency egress, and brake performance. These standards are more stringent than international (e.g., European) standards, creating cost and procurement barriers for US passenger rail.",
        reasoning_framework="""
FRA PASSENGER EQUIPMENT SAFETY STANDARDS ANALYSIS:

1. Crashworthiness Requirements (49 CFR 238.203-233):
   - Buff strength: 800,000 lbf static compressive load on carbody structure
   - Collision posts: Vertical posts to maintain survival space in collisions
   - Corner posts: Reinforced to prevent roof collapse
   - Rollover strength: Roof must withstand 4x carbody weight
   - Crash energy management (CEM): Crushable zones absorb collision energy
   - Rationale: Protect passengers in train-to-train or grade crossing collisions

2. Structural vs. CEM Approaches:
   - Traditional (buff strength): Heavy steel carbody to resist compressive loads
   - CEM approach: Lighter carbody with crushable zones and strong survival space
   - FRA allows CEM with alternative compliance demonstration
   - European approach: Lighter cars, rely on train control to prevent collisions
   - Trade-off: Heavier cars increase infrastructure wear, energy consumption

3. Emergency Egress (49 CFR 238.113-115):
   - Emergency windows: Minimum number and size for egress
   - Door accessibility: Doors must be openable from inside in emergencies
   - Rescue access: External markings for emergency responders
   - Evacuation drills: Required for crew training
   - Tunnel and underwater crossings: Special egress provisions

4. Fire Safety (49 CFR 238.103-111):
   - Material flammability: Seats, walls, floors must meet flame spread and smoke emission tests
   - Fire detection: Smoke detectors in restrooms, electrical cabinets
   - Fire suppression: Extinguishers accessible to crew
   - Thermal barriers: Between passenger compartment and fuel tanks or engines
   - Emergency lighting: Battery-powered egress path lighting

5. Brake Performance (49 CFR 238.301-535):
   - Service brakes: Adequate to control speed on grades and maintain schedules
   - Emergency brakes: Fail-safe application on loss of pressure or control
   - Stopping distance: Specified for different speeds and train lengths
   - Brake system redundancy: Independent backup systems
   - Parking brakes: Prevent unintended movement when parked

6. Doors and Windows (49 CFR 238.119-125):
   - Entrance doors: Interlocked with propulsion to prevent opening while moving
   - Emergency signage: Clearly marked instructions for emergency door opening
   - Glazing: Laminated or tempered glass to prevent shattering
   - Window retention: Windows must not separate in collisions

7. International Harmonization Challenges:
   - European standards (TSI): Less stringent crashworthiness, lighter cars
   - US-Europe incompatibility: Difficult to procure European trainsets for US without costly modifications
   - FRA waivers: Case-by-case alternative compliance for foreign equipment
   - Cost impact: Compliance adds 10-30% to vehicle cost
   - Safety vs. cost: Debate over whether FRA standards are excessively conservative
        """,
        key_factors=[
            "FRA 49 CFR Part 238 mandates 800,000 lbf buff strength for crashworthiness",
            "Crash energy management (CEM) is alternative compliance approach",
            "Emergency egress, fire safety, and brake performance also regulated",
            "FRA standards more stringent than European (TSI), creating procurement barriers",
            "Compliance adds 10-30% to vehicle cost compared to international standards",
            "Waivers available for alternative compliance demonstration",
            "Safety vs. cost debate: Are FRA standards excessively conservative?"
        ],
        primary_authority=[
            "49 CFR Part 238: Passenger Equipment Safety Standards",
            "FRA alternative compliance guidance for CEM and foreign equipment",
            "NTSB accident reports and recommendations on passenger equipment safety"
        ],
        burden_holder="Passenger rail operators, rolling stock manufacturers",
        adversary_position="FRA standards are too stringent; adopt international standards to reduce costs",
        counter_arguments=[
            "US freight-passenger mixed traffic justifies higher crashworthiness standards",
            "NTSB accident investigations support need for robust passenger protection",
            "CEM approach allows lighter cars while maintaining safety",
            "Waivers provide flexibility for alternative compliance",
            "Cost of compliance is small compared to total capital investment"
        ],
        resolution_strategy="Comply with 49 CFR Part 238 for all new passenger equipment, pursue CEM approach for lighter-weight cars where feasible, seek FRA waivers for alternative compliance if procuring international equipment, engage in industry advocacy for standards harmonization where appropriate, prioritize passenger safety in design.",
        entity_scope="All US passenger rail operators subject to FRA jurisdiction (excludes light rail and rapid transit)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="FRA regulations are clear and enforced; CEM alternative compliance requires detailed engineering analysis",
        controlling_precedent="FRA 49 CFR Part 238 and enforcement actions define compliance standards",
        issue_category=IssueCategory.SAFETY,
        authority_level=AuthorityLevel.FRA_REGULATION,
        fact_fragility_score=0.10
    ),

    DoctrineBlock(
        topic="Station Parking and Park-and-Ride Facilities",
        keywords=["park-and-ride", "station parking", "parking demand", "parking pricing", "TOD", "access mode", "kiss-and-ride", "bike parking"],
        conclusion_template="Park-and-ride facilities extend passenger rail catchment area but require land, capital investment, and ongoing management. Parking demand forecasting must consider access mode shares, pricing, and competition with auto for entire trip. Transit-oriented development (TOD) can reduce long-term parking demand.",
        reasoning_framework="""
STATION PARKING AND PARK-AND-RIDE ANALYSIS:

1. Access Mode Shares:
   - Walk: Typically 10-30% at urban stations, <5% at suburban
   - Bicycle: 2-10% depending on infrastructure and climate
   - Kiss-and-ride (drop-off): 10-25% at suburban stations
   - Park-and-ride: 30-60% at suburban stations, <10% at urban
   - Feeder bus: 10-30% at well-connected stations
   - Catchment area: Walk 0.5-1 mile, bike 2-3 miles, auto 5-15 miles

2. Parking Demand Forecasting:
   - Mode choice model: Predict share of passengers arriving by auto
   - Occupancy rate: Passengers per vehicle (typically 1.1-1.3)
   - Turnover: All-day vs. mid-day departures (affects space requirements)
   - Growth projections: Future ridership and mode share changes
   - Induced demand: New parking may attract auto-oriented riders

3. Parking Supply and Configuration:
   - Surface parking: Low capital cost ($5-15K per space), land-intensive
   - Structured parking: High capital cost ($20-50K per space), land-efficient
   - Shared parking: Agreements with adjacent land uses for off-peak use
   - Reserved spaces: Premium parking for high-frequency users (monthly permits)
   - ADA spaces: 5% minimum, van-accessible, close to station entrance

4. Parking Pricing:
   - Free parking: Maximizes ridership but encourages auto access, costly to provide
   - Daily fees: $3-10 typical, market-based pricing in high-demand areas
   - Monthly permits: $50-150, guarantees space for frequent users
   - Dynamic pricing: Higher prices during peak demand to manage utilization
   - Revenue: Can offset parking facility cost but rarely covers full capital + O&M

5. Parking Management:
   - Enforcement: Prevent non-rail users from parking (shopping, airport overflow)
   - Time limits: Discourage all-day non-transit parking
   - Permit systems: Online reservation, waitlist management for high-demand stations
   - Overflow: Manage peak demand with remote lots and shuttle buses
   - Security: Lighting, CCTV, patrols to reduce crime and vandalism

6. Alternatives to Parking:
   - Kiss-and-ride: Drop-off/pick-up zones, reduce parking demand
   - Bike parking: Secure bike lockers, bike racks, bike-share integration
   - Feeder buses: Connect surrounding areas to station, reduce auto access
   - TOD: High-density residential and employment near station reduces parking demand
   - Shared mobility: TNCs (Uber/Lyft), car-share, scooters for first/last mile

7. TOD and Long-Term Parking Demand:
   - Transit-oriented development: Reduce auto dependency over time
   - Zoning changes: Allow higher density, mixed-use development near stations
   - Parking maximums: Limit parking supply to discourage auto use
   - Pedestrian improvements: Sidewalks, crosswalks, bike lanes increase walk/bike share
   - Land value capture: Use increased property values to fund transit improvements
        """,
        key_factors=[
            "Park-and-ride mode share 30-60% at suburban stations, <10% at urban",
            "Surface parking $5-15K per space, structured $20-50K per space",
            "Parking pricing can manage demand and generate revenue",
            "Feeder buses and TOD are alternatives that reduce parking demand",
            "Parking demand forecasting must consider mode choice and growth",
            "Kiss-and-ride and bike parking reduce need for auto parking spaces",
            "Long-term: TOD reduces auto access, allows parking lot redevelopment"
        ],
        primary_authority=[
            "TCRP Report 153: Guidelines for Providing Access to Public Transportation Stations",
            "ITE Parking Generation Manual: Trip generation and parking demand rates",
            "TOD best practices (Reconnecting America, CTOD)"
        ],
        burden_holder="Transit agency real estate and station operations",
        adversary_position="Provide ample free parking to maximize ridership",
        counter_arguments=[
            "Free parking is costly and encourages auto dependency",
            "Parking lots are low-value use of land near transit stations",
            "TOD generates higher ridership and revenue than parking lots",
            "Pricing parking generates revenue and manages demand efficiently",
            "Climate and equity goals favor reducing auto access over time"
        ],
        resolution_strategy="Forecast parking demand using mode choice models, provide adequate parking for initial service but plan for TOD redevelopment, implement parking pricing to manage demand and generate revenue, invest in bike parking and kiss-and-ride facilities, coordinate with local jurisdictions on TOD zoning and feeder bus service.",
        entity_scope="Suburban commuter rail and regional rail stations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Parking demand forecasting methods are established; mode share depends on local context and land use",
        controlling_precedent="TCRP Report 153 and ITE Parking Generation provide industry guidance",
        issue_category=IssueCategory.STATIONS,
        authority_level=AuthorityLevel.INDUSTRY_STANDARD,
        fact_fragility_score=0.25
    ),

    DoctrineBlock(
        topic="Passenger Information Systems (PIS) and Real-Time Data",
        keywords=["passenger information", "real-time arrivals", "GTFS-RT", "dynamic signage", "mobile apps", "service alerts", "wayfinding"],
        conclusion_template="Passenger Information Systems (PIS) provide real-time arrival predictions, service alerts, and wayfinding to improve passenger experience and reduce perceived wait time. GTFS and GTFS-RT are industry-standard data formats. Accurate real-time data requires vehicle tracking (GPS, wayside sensors) and prediction algorithms.",
        reasoning_framework="""
PASSENGER INFORMATION SYSTEMS ANALYSIS:

1. Information Types:
   - Real-time arrivals: Predicted arrival time at each station (minutes until arrival)
   - Service alerts: Delays, cancellations, track changes, disruptions
   - Wayfinding: Maps, station layouts, platform assignments, exit locations
   - Fare information: Prices, payment methods, fare zones
   - Accessibility: Elevator/escalator status, accessible routes
   - Connections: Transfer information to other lines or modes

2. Display Platforms:
   - Station displays: LED/LCD signs on platforms, concourses, entrance areas
   - On-board displays: Next stop, delay information, connections
   - Mobile apps: Real-time arrivals, trip planning, service alerts, ticketing
   - Website: Schedule, maps, fare information, trip planner
   - Third-party integration: Google Maps, Transit, Citymapper, etc.
   - Audio announcements: Automated and manual announcements for accessibility

3. GTFS and GTFS-RT Standards:
   - GTFS (General Transit Feed Specification): Static schedule, stops, routes, fares
   - GTFS-RT: Real-time updates (vehicle positions, trip updates, service alerts)
   - Open data: Public release enables third-party app development
   - Data quality: Accuracy and timeliness critical for user trust
   - Update frequency: Real-time feeds typically updated every 10-30 seconds

4. Vehicle Tracking Technology:
   - GPS: Accurate outdoor positioning, standard for surface rail and bus
   - Wayside transponders: Balises or RFID tags at known locations (backup to GPS)
   - Signaling system integration: Block occupancy and train location from signaling
   - Automatic Vehicle Location (AVL): Combined GPS, dead reckoning, map matching
   - Tunnel challenges: GPS unavailable, requires wayside sensors or inertial navigation

5. Arrival Prediction Algorithms:
   - Schedule-based: Use published schedule adjusted for known delays
   - Historical data: Average running times by time of day, day of week
   - Real-time tracking: Current vehicle position and speed
   - Machine learning: Predict delays based on patterns (weather, time, events)
   - Dwell time prediction: Estimate station stop duration based on crowding

6. Service Alert Management:
   - Incident detection: Automated alerts from vehicle/infrastructure monitoring
   - Alert authoring: Staff create and approve alert messages
   - Multi-channel distribution: Push to displays, apps, website, social media
   - Message prioritization: Critical alerts override routine information
   - Archive: Historical alerts for incident analysis and improvement

7. User Experience:
   - Perceived wait time: Real-time information reduces anxiety, perceived wait
   - Consistency: Same information across all channels builds trust
   - Accessibility: Audio, large print, high contrast for visual impairments
   - Multilingual: Major languages for diverse ridership
   - Simplicity: Clear, concise messages (avoid jargon)
        """,
        key_factors=[
            "Real-time arrival information reduces perceived wait time and anxiety",
            "GTFS and GTFS-RT are industry-standard open data formats",
            "Vehicle tracking via GPS or wayside sensors enables real-time predictions",
            "Multi-channel distribution (signs, apps, website, audio) ensures accessibility",
            "Data quality and update frequency critical for user trust",
            "Service alerts must be timely, accurate, and actionable",
            "Third-party app integration extends reach and functionality"
        ],
        primary_authority=[
            "GTFS and GTFS-RT specifications (Google/MobilityData)",
            "TCRP Report 165: Transit Capacity and Quality of Service Manual, Chapter 7",
            "FTA Open Data and Mobility Innovation guidelines"
        ],
        burden_holder="Transit agency IT, operations, and customer service departments",
        adversary_position="Static schedules are sufficient; real-time data is too expensive",
        counter_arguments=[
            "Passengers expect real-time information; lack of it is competitive disadvantage",
            "Open data enables third-party app development at no cost to agency",
            "Real-time data improves operational visibility and incident response",
            "Perceived wait time is key driver of customer satisfaction",
            "GPS and GTFS-RT technology costs have decreased significantly"
        ],
        resolution_strategy="Deploy vehicle tracking (GPS or wayside sensors), implement GTFS-RT feeds for real-time arrivals and alerts, publish open data to enable third-party apps, invest in station displays and mobile app, ensure data quality and update frequency, provide multi-channel and accessible information, monitor user feedback and improve continuously.",
        entity_scope="All passenger rail systems with variable schedules or service disruptions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="GTFS-RT is proven standard; arrival prediction accuracy depends on tracking technology and algorithms",
        controlling_precedent="Major transit agencies (NYC MTA, London TfL, BART) provide comprehensive real-time information",
        issue_category=IssueCategory.SERVICE_QUALITY,
        authority_level=AuthorityLevel.INDUSTRY_STANDARD,
        fact_fragility_score=0.15
    ),

    DoctrineBlock(
        topic="Cross-Border and Inter-City Passenger Rail Operations",
        keywords=["inter-city rail", "Amtrak", "cross-border", "customs", "immigration", "gauge compatibility", "electrification compatibility", "through-ticketing"],
        conclusion_template="Inter-city and cross-border passenger rail operations face unique challenges including gauge and electrification compatibility, customs/immigration procedures, through-ticketing, and multi-operator coordination. Amtrak operates US inter-city services, often on freight-owned tracks with priority disputes.",
        reasoning_framework="""
INTER-CITY AND CROSS-BORDER RAIL ANALYSIS:

1. Track Compatibility:
   - Gauge: Standard (4 ft 8.5 in) in US, Canada, Europe; incompatible gauges require bogie change or transloading
   - Electrification: 25 kV AC (modern standard), 12.5/15 kV AC (legacy Europe), 750/1500 V DC (legacy), diesel (non-electrified)
   - Loading gauge: Clearances vary; rolling stock must fit tightest section
   - Axle loads: Infrastructure capacity limits weight per axle
   - Dual-mode locomotives: Switch between electric and diesel for non-electrified sections

2. Signaling and Train Control:
   - Multiple systems: ACSES, I-ETMS, ETCS, legacy systems across different territories
   - Interoperability: Trains may need multiple signaling systems for cross-border
   - PTC compliance: FRA mandate in US, ETCS in Europe, different standards
   - Radio frequencies: Different frequencies and protocols for train-ground communication

3. Customs and Immigration:
   - Pre-clearance: Passengers clear customs/immigration before boarding (e.g., US-Canada)
   - On-board inspection: Officers inspect while train is moving (slows operations)
   - Station inspection: Dedicated customs area at border stations (adds transfer time)
   - Trusted traveler programs: NEXUS, Global Entry expedite frequent travelers
   - Visa requirements: International passengers must have valid visas

4. Through-Ticketing and Fare Integration:
   - Interline agreements: Multiple operators honor single ticket
   - Revenue allocation: Distribute fare revenue based on distance or negotiated formula
   - Reservation systems: Integrated booking across operators
   - Baggage handling: Check baggage through to final destination (rare in rail)
   - Connection protection: Missed connections due to delays handled by joint policy

5. Operational Coordination:
   - Schedule coordination: Aligned timetables for transfers
   - Rolling stock sharing: Cross-border services may require compatible equipment
   - Crew qualifications: Engineers qualified on both sides of border, multiple languages
   - Maintenance standards: Different inspection and maintenance regimes
   - Liability and insurance: Cross-border incidents require clear jurisdiction

6. Amtrak-Freight Railroad Relations:
   - Statutory preference: Amtrak has statutory priority on freight-owned tracks (45 USC 24308)
   - Enforcement challenges: Freight railroads often ignore priority, causing delays
   - Access fees: Amtrak pays incremental cost, not full cost recovery
   - Capacity constraints: Freight traffic growth reduces Amtrak reliability
   - Infrastructure investment: Amtrak funds improvements on freight tracks for better service

7. High-Speed Rail (HSR) Considerations:
   - Dedicated tracks: HSR typically requires separated, grade-separated tracks (>200 km/h)
   - International HSR: Eurostar (UK-France-Belgium), Thalys (France-Belgium-Netherlands-Germany)
   - Border procedures: Streamlined for HSR (e.g., Eurostar immigration in stations)
   - Competitive with air: <3 hour rail trip competitive with flying for city center to city center
   - US HSR challenges: No true HSR in US; Acela is limited by shared tracks and curves
        """,
        key_factors=[
            "Gauge and electrification compatibility critical for cross-border operations",
            "Customs/immigration procedures add time and complexity",
            "Through-ticketing requires interline agreements and revenue sharing",
            "Amtrak has statutory priority on freight tracks but enforcement is weak",
            "High-speed rail requires dedicated tracks for >200 km/h speeds",
            "Crew qualifications and signaling systems must be compatible across borders",
            "Pre-clearance or on-board inspection are options for international rail"
        ],
        primary_authority=[
            "45 USC 24308: Amtrak statutory preference on freight tracks",
            "International Railway Transport Committee (CIT): Cross-border rail regulations",
            "Amtrak-freight host railroad agreements"
        ],
        burden_holder="Inter-city rail operators (Amtrak, VIA Rail), freight railroads hosting passenger",
        adversary_position="Freight priority should override passenger; Amtrak should build own tracks",
        counter_arguments=[
            "Federal law grants Amtrak priority; freight railroads must comply",
            "Inter-city rail reduces highway and aviation congestion and emissions",
            "Dedicated passenger tracks are financially and physically infeasible in most corridors",
            "Improved Amtrak service benefits freight by reducing highway truck competition",
            "International rail provides seamless travel for border communities"
        ],
        resolution_strategy="Enforce Amtrak statutory priority through STB complaints and litigation, invest in capacity improvements on shared tracks, pursue dedicated HSR corridors where feasible, streamline customs/immigration procedures with pre-clearance or trusted traveler programs, negotiate through-ticketing and revenue allocation agreements with connecting operators.",
        entity_scope="Inter-city passenger rail (Amtrak, VIA Rail) and cross-border services",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Legal framework is clear but enforcement is weak; cross-border procedures are complex and politically sensitive",
        controlling_precedent="STB rulings on Amtrak preference disputes; Eurostar/Thalys demonstrate successful cross-border rail",
        issue_category=IssueCategory.INTEGRATION,
        authority_level=AuthorityLevel.FRA_REGULATION,
        fact_fragility_score=0.30
    ),

    DoctrineBlock(
        topic="Energy Consumption and Regenerative Braking",
        keywords=["energy consumption", "regenerative braking", "traction power", "substations", "catenary", "third rail", "energy efficiency", "electrification"],
        conclusion_template="Electric passenger rail is highly energy-efficient, especially with regenerative braking that recovers 15-30% of traction energy. Traction power supply via catenary (overhead) or third rail provides electricity to trains. Energy consumption depends on vehicle weight, speed, acceleration, grade, and schedule.",
        reasoning_framework="""
ENERGY CONSUMPTION AND REGENERATIVE BRAKING ANALYSIS:

1. Traction Power Supply:
   - Catenary (overhead): 25 kV AC (modern standard), 15 kV AC, 3 kV DC, 1.5 kV DC (legacy)
   - Third rail: 600-750 V DC (metro and light rail), lower voltage limits speed and current draw
   - Substations: Convert grid power (typically 3-phase AC) to traction voltage
   - Spacing: Catenary substations 10-50 km apart, third rail 1-5 km (higher losses)
   - Redundancy: Multiple substations prevent total power loss on single failure

2. Energy Consumption Factors:
   - Vehicle weight: Heavier trains require more energy (proportional to mass)
   - Acceleration: Rapid acceleration increases peak power demand
   - Top speed: Air resistance increases with square of speed
   - Grade: Climbing grades requires additional energy (potential energy gain)
   - Schedule: Frequent stops increase energy per passenger-km (acceleration losses)
   - Auxiliary loads: HVAC, lighting, doors (10-20% of total energy)

3. Regenerative Braking:
   - Principle: Traction motors operate as generators during braking, convert kinetic energy to electrical
   - Energy recovery: 15-30% of traction energy recovered (depends on braking profile and receptivity)
   - Receptivity: Requires another train on same electrical section to consume regenerated energy, or energy storage
   - Efficiency: Regenerated energy losses in conversion and transmission (80-90% efficient)
   - Friction braking: Blended with regenerative; pure friction at very low speeds or emergency

4. Energy Storage Systems:
   - Wayside storage: Supercapacitors or batteries at substations store regenerated energy
   - On-board storage: Batteries or flywheels on trains (less common, adds weight)
   - Grid feedback: Return regenerated energy to utility grid (requires approval, inverters)
   - Increased receptivity: Storage enables higher regeneration recovery even without adjacent trains

5. Energy Efficiency Improvements:
   - Lightweight materials: Aluminum, composites reduce vehicle weight
   - Aerodynamics: Streamlined nose, smooth undercarriage reduce air resistance
   - Eco-driving: Optimized driving profiles (coasting, moderate acceleration) save energy
   - LED lighting: Replace fluorescent/incandescent with LED (50-70% energy savings)
   - Efficient HVAC: Variable-speed compressors, heat pumps, improved insulation

6. Diesel vs. Electric Comparison:
   - Electric: 2-3 MJ/km per vehicle (well-to-wheel), highly efficient, zero local emissions
   - Diesel: 8-12 MJ/km per vehicle (well-to-wheel), less efficient, local emissions (NOx, PM)
   - Electrification capital cost: $2-5 million per track-mile for catenary infrastructure
   - Operating cost: Electricity typically cheaper than diesel per unit energy
   - Emissions: Electric grid decarbonization improves rail emissions over time

7. Demand Management:
   - Peak power demand: Limits number of trains accelerating simultaneously
   - Substation capacity: Sized for peak load, not average
   - Load management: Stagger train departures to reduce peak demand
   - Dynamic pricing: Time-of-use electricity rates incentivize off-peak charging (for battery trains)
        """,
        key_factors=[
            "Electric rail is 2-4x more energy-efficient than diesel (well-to-wheel)",
            "Regenerative braking recovers 15-30% of traction energy",
            "Energy consumption depends on weight, speed, acceleration, grade, schedule",
            "Catenary (overhead) supports higher speeds than third rail",
            "Wayside energy storage increases regenerative braking receptivity",
            "Eco-driving and lightweight materials improve efficiency",
            "Electrification capital cost $2-5M per track-mile but lower operating cost"
        ],
        primary_authority=[
            "TCRP Report 155: Track Design Handbook for Light Rail Transit",
            "IEEE 1653: Standard for Traction Power Systems for Rail Transit",
            "UIC Energy Efficiency Technologies for Railways"
        ],
        burden_holder="Transit agency engineering and operations departments",
        adversary_position="Diesel is cheaper upfront; avoid electrification capital cost",
        counter_arguments=[
            "Electric rail has lower operating cost and longer vehicle life than diesel",
            "Regenerative braking reduces energy cost by 15-30%",
            "Grid decarbonization makes electric rail increasingly low-carbon",
            "Local air quality benefits from zero-emission electric trains",
            "Electrification enables higher performance (acceleration, speed) than diesel"
        ],
        resolution_strategy="Electrify high-frequency and high-speed passenger rail lines for efficiency and performance, implement regenerative braking on all new rolling stock, consider wayside energy storage to increase regeneration receptivity, optimize driving profiles for energy efficiency, monitor energy consumption and set reduction targets.",
        entity_scope="All electric passenger rail systems; comparison for diesel commuter rail",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Energy efficiency metrics are well-established; regeneration recovery depends on system design and operation",
        controlling_precedent="European and Asian electric rail systems demonstrate efficiency and performance benefits",
        issue_category=IssueCategory.OPERATIONS,
        authority_level=AuthorityLevel.INDUSTRY_STANDARD,
        fact_fragility_score=0.15
    ),

    DoctrineBlock(
        topic="Station Design and Passenger Flow Optimization",
        keywords=["station design", "passenger flow", "vertical circulation", "faregates", "platform capacity", "queuing", "level of service", "universal design"],
        conclusion_template="Station design optimizes passenger flow from street to platform using adequate vertical circulation (stairs, escalators, elevators), fare collection, and platform capacity. Bottlenecks at faregates, escalators, or platform access degrade level of service and increase crowding. Universal design principles improve accessibility and overall user experience.",
        reasoning_framework="""
STATION DESIGN AND PASSENGER FLOW ANALYSIS:

1. Passenger Flow Path:
   - Street entry: Sidewalk, plaza, canopy (weather protection)
   - Concourse: Information, faregates, retail, waiting area
   - Vertical circulation: Stairs, escalators, elevators to platform level
   - Platform: Queuing zones, tactile strips, shelters, seating
   - Egress: Reverse path for exiting passengers (may be separate)

2. Vertical Circulation Capacity:
   - Stairs: 50-70 passengers/meter width/minute (descending higher than ascending)
   - Escalators: 100-120 passengers/meter width/minute (one-way)
   - Elevators: 10-20 passengers per cycle (slow for high volumes, critical for accessibility)
   - Bidirectional flow: Stairs must accommodate both directions, reduces effective capacity
   - Redundancy: Multiple escalators/stairs to handle peak flows and provide backup

3. Faregate and Access Control:
   - Faregate width: 0.6-0.9 m per lane, wider for wheelchairs
   - Throughput: 25-35 passengers/minute per gate (contactless payment faster)
   - Number of gates: Size to handle peak 15-minute passenger volume
   - Queuing space: Adequate area upstream of gates to prevent spillback to street
   - Fare evasion: Gate design balances throughput and security (height, sensors)

4. Platform Capacity:
   - Width: Minimum 3m for low-volume, 6m+ for high-volume stations
   - Queuing zones: Passengers wait in predictable locations (door alignment marks)
   - Circulation space: Movement along platform, avoiding queuing zones
   - Level of Service: A-F scale based on square meters per passenger
   - Crowding: LOS E-F (< 0.5 sq m/passenger) is unsafe and uncomfortable

5. Bottleneck Analysis:
   - Identify choke points: Faregates, escalators, narrow passages
   - Measure flow rates: Passengers per minute through each element
   - Capacity calculation: Minimum capacity element limits entire station
   - Queuing model: Simulate passenger arrivals and service times
   - Design interventions: Widen bottlenecks, add gates/escalators, improve wayfinding

6. Wayfinding and Signage:
   - Clarity: Clear, consistent signage to platforms, exits, connections
   - Visibility: High-contrast, illuminated, at decision points
   - Multilingual: Major languages for international stations
   - Maps: System map, station layout, "you are here" markers
   - Real-time information: Arrivals, delays, platform assignments

7. Universal Design and Accessibility:
   - Level access: No steps from street to train (elevators for grade separation)
   - Tactile guidance: Tactile paving for visually impaired navigation
   - Visual contrast: High-contrast colors at edges, hazards, decision points
   - Audible information: Announcements, beacons, accessible wayfinding apps
   - Seating and rest areas: For elderly and passengers with limited mobility
        """,
        key_factors=[
            "Faregates, escalators, and platform access are common bottlenecks",
            "Escalator capacity 100-120 pax/meter/min, stairs 50-70 pax/meter/min",
            "Platform width must accommodate peak queuing and circulation (6m+ for high-volume)",
            "Level of Service (LOS) A-F scale based on square meters per passenger",
            "Universal design improves accessibility and overall user experience",
            "Wayfinding reduces passenger confusion and improves flow efficiency",
            "Bottleneck capacity limits entire station throughput"
        ],
        primary_authority=[
            "TCQSM (Transit Capacity and Quality of Service Manual), Chapter 4",
            "NFPA 130: Standard for Fixed Guideway Transit and Passenger Rail Systems (fire/life safety)",
            "ADA Standards for Accessible Design (DOJ 2010 Standards)"
        ],
        burden_holder="Transit agency station design, architecture, and engineering",
        adversary_position="Minimal station design to reduce capital cost",
        counter_arguments=[
            "Poor station design degrades passenger experience and deters ridership",
            "Bottlenecks increase dwell time and reduce line capacity",
            "Crowding and congestion pose safety risks during emergencies",
            "Accessibility is legal requirement (ADA) and benefits all passengers",
            "Wayfinding and amenities improve customer satisfaction and loyalty"
        ],
        resolution_strategy="Design stations for peak 15-minute passenger flows with adequate faregate and vertical circulation capacity, ensure platform width accommodates queuing and circulation (LOS D or better), implement universal design for accessibility, provide clear wayfinding and real-time information, simulate passenger flows to identify and eliminate bottlenecks.",
        entity_scope="All passenger rail stations, especially high-volume urban stations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Pedestrian flow models are well-validated; capacity calculation requires accurate demand forecasts",
        controlling_precedent="World-class metro stations (Hong Kong, Singapore, Tokyo) demonstrate best practices in flow optimization",
        issue_category=IssueCategory.STATIONS,
        authority_level=AuthorityLevel.INDUSTRY_STANDARD,
        fact_fragility_score=0.20
    ),

    DoctrineBlock(
        topic="Service Reliability and Mean Distance Between Failures (MDBF)",
        keywords=["reliability", "MDBF", "mean distance between failures", "vehicle reliability", "maintenance", "failure modes", "predictive maintenance", "spare ratio"],
        conclusion_template="Service reliability depends critically on rolling stock Mean Distance Between Failures (MDBF), measured in miles or kilometers between service-affecting failures. Industry targets: 10,000-40,000 miles MDBF for light rail, 100,000+ miles for heavy rail. Predictive maintenance and adequate spare ratio improve reliability.",
        reasoning_framework="""
SERVICE RELIABILITY AND MDBF ANALYSIS:

1. MDBF Definition and Measurement:
   - MDBF: Total revenue service miles / number of service-affecting failures
   - Service-affecting failure: Delay >5 minutes or out-of-service vehicle
   - Non-service-affecting: Failures repaired without service impact
   - Reportable vs. non-reportable: FTA National Transit Database (NTD) definitions
   - Trend analysis: Monitor MDBF monthly/annually to detect degradation

2. MDBF Targets by Mode:
   - Light rail: 10,000-25,000 miles MDBF (lower due to complexity, street running)
   - Heavy rail/metro: 40,000-100,000+ miles MDBF (newer systems higher)
   - Commuter rail: 20,000-50,000 miles MDBF (locomotive-hauled lower than EMU)
   - High-speed rail: 150,000+ miles MDBF (critical for punctuality)
   - New vs. legacy: Newer fleets typically have higher MDBF as bugs are worked out

3. Common Failure Modes:
   - Doors: Sensors, motors, safety interlocks (most common failure)
   - Brakes: Air leaks, valve failures, wheel slide protection
   - HVAC: Compressor failures, refrigerant leaks, control systems
   - Traction: Motor bearings, inverter faults, pantograph/shoe issues
   - Auxiliary power: Battery failures, alternator/generator faults
   - Signaling/control: Onboard computers, communications, GPS

4. Maintenance Strategies:
   - Preventive maintenance: Time-based or mileage-based inspections and replacements
   - Predictive maintenance: Condition monitoring (vibration, temperature, oil analysis) triggers maintenance
   - Reliability-centered maintenance (RCM): Focus resources on critical failure modes
   - Failure analysis: Root cause investigation to prevent recurrence
   - Parts inventory: Balance spare parts cost vs. downtime risk

5. Spare Ratio and Fleet Availability:
   - Spare ratio: (Fleet size - service requirement) / fleet size (typically 10-20%)
   - Availability: Percentage of fleet available for service (target 90-95%)
   - Scheduled maintenance: Planned out-of-service time for inspections
   - Unscheduled failures: Unexpected breakdowns requiring spare vehicles
   - Cannibalization: Robbing parts from out-of-service vehicles (last resort)

6. Predictive Maintenance Technology:
   - Onboard sensors: Continuous monitoring of critical systems
   - Data analytics: Machine learning to predict failures before they occur
   - Remote diagnostics: Troubleshoot issues without removing vehicle from service
   - Condition-based triggers: Replace components when wear detected, not on fixed schedule
   - Cost-benefit: Predictive maintenance reduces unplanned failures but requires investment

7. Warranty and Supplier Accountability:
   - New vehicle warranty: Typically 5-10 years, includes MDBF guarantees
   - Performance penalties: Financial penalties if MDBF targets not met
   - Technical support: Manufacturer provides engineers to troubleshoot recurring issues
   - Design modifications: Retrofit fixes for systemic problems
   - Spare parts availability: Long-term parts support critical for fleet life (30-40 years)
        """,
        key_factors=[
            "MDBF targets: 10,000-25,000 miles light rail, 40,000-100,000+ miles heavy rail",
            "Door and brake failures are most common service-affecting failures",
            "Spare ratio 10-20% balances cost and reliability",
            "Predictive maintenance reduces unplanned failures and downtime",
            "New vehicle warranties include MDBF guarantees and performance penalties",
            "Fleet availability target: 90-95% of vehicles available for service",
            "Failure analysis and root cause correction prevent recurrence"
        ],
        primary_authority=[
            "FTA National Transit Database (NTD): MDBF reporting definitions",
            "APTA Rail Vehicle Reliability Standards",
            "IEEE 1624: Standard for Organizational Reliability Capability"
        ],
        burden_holder="Transit agency vehicle maintenance and fleet management",
        adversary_position="Accept lower MDBF to reduce maintenance cost",
        counter_arguments=[
            "Low MDBF degrades service reliability and passenger satisfaction",
            "Unreliable service drives passengers to alternative modes",
            "Spare vehicles are expensive; high MDBF reduces spare ratio needed",
            "Predictive maintenance reduces long-term cost despite upfront investment",
            "Warranty guarantees hold manufacturers accountable for design quality"
        ],
        resolution_strategy="Set MDBF targets in vehicle procurement specifications with performance penalties, invest in predictive maintenance technology, maintain adequate spare ratio (10-20%), conduct rigorous failure analysis and implement corrective actions, monitor MDBF trends and address degradation proactively, leverage warranty support for systemic issues.",
        entity_scope="All passenger rail systems with powered rolling stock",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="MDBF measurement is standardized; targets depend on vehicle technology and operational environment",
        controlling_precedent="FTA NTD reporting and APTA reliability benchmarks define industry standards",
        issue_category=IssueCategory.ROLLING_STOCK,
        authority_level=AuthorityLevel.INDUSTRY_STANDARD,
        fact_fragility_score=0.15
    ),

    DoctrineBlock(
        topic="Transit-Oriented Development (TOD) and Land Use Integration",
        keywords=["transit-oriented development", "TOD", "land use", "density", "mixed-use", "walkability", "value capture", "zoning", "joint development"],
        conclusion_template="Transit-Oriented Development (TOD) integrates high-density, mixed-use development near rail stations to maximize ridership, reduce auto dependency, and capture land value increases. Effective TOD requires supportive zoning, pedestrian-friendly design, and coordination between transit agencies and local governments. Value capture mechanisms fund transit investments.",
        reasoning_framework="""
TRANSIT-ORIENTED DEVELOPMENT ANALYSIS:

1. TOD Principles:
   - Density: Higher residential and employment density within 0.5 mile of stations (walkable catchment)
   - Mixed-use: Combine residential, office, retail, services to enable live-work-play without auto
   - Walkability: Sidewalks, crosswalks, bike lanes, human-scale streets
   - Parking management: Reduce or eliminate parking minimums, implement parking maximums
   - Design quality: Attractive public spaces, active street frontages, safe pedestrian environment

2. Land Use Density Targets:
   - Residential: 30-100+ dwelling units per acre near stations (vs. 5-10 suburban)
   - Employment: 50-200+ employees per acre (office, retail, services)
   - Floor Area Ratio (FAR): 2-10+ in TOD zones (ratio of building floor area to land area)
   - Gradual transition: Highest density at station, decreasing with distance
   - Minimum density zoning: Require minimum rather than maximum densities

3. Mixed-Use Development:
   - Vertical mix: Retail/office ground floor, residential upper floors
   - Horizontal mix: Diverse land uses within walking distance
   - 24-hour activity: Residential, office, entertainment create all-day vitality
   - Affordable housing: Include income-restricted units to serve transit-dependent populations
   - Community facilities: Schools, parks, libraries within TOD area

4. Zoning and Regulatory Tools:
   - Form-based codes: Regulate building form and street character, not just use
   - Overlay zones: Special TOD zoning on top of base zoning
   - Density bonuses: Allow higher density in exchange for public benefits (affordable housing, open space)
   - Parking maximums: Limit parking to discourage auto use
   - Streamlined permitting: Expedited approvals for TOD projects

5. Value Capture Mechanisms:
   - Special assessment districts: Property owners near stations pay for transit improvements
   - Tax increment financing (TIF): Capture future property tax increases to fund transit
   - Joint development: Transit agency leases or sells land for private development, shares revenue
   - Development impact fees: Charge developers for transit infrastructure costs
   - Land acquisition: Agency buys land before station announcement, sells after value increases

6. Pedestrian and Bicycle Infrastructure:
   - Complete streets: Sidewalks, bike lanes, crosswalks on all streets
   - Traffic calming: Slow auto speeds for pedestrian safety (bulb-outs, raised crossings)
   - Bike parking: Secure bike lockers, racks, bike-share stations at transit stops
   - Wayfinding: Maps, signage to guide pedestrians and cyclists
   - Greenways: Off-street paths connecting residential areas to stations

7. Implementation Challenges:
   - Community opposition: NIMBYism, concerns about density, traffic, affordability
   - Gentrification: TOD may displace low-income residents via rising rents
   - Coordination: Transit agency, city, county, developers must align goals
   - Timing: TOD takes 10-20 years to fully develop; interim uses needed
   - Funding: Value capture requires upfront investment before land value increases
        """,
        key_factors=[
            "TOD targets 30-100+ dwelling units/acre within 0.5 mile of stations",
            "Mixed-use development enables live-work-play without auto dependency",
            "Parking maximums and minimums elimination reduce auto use",
            "Value capture (TIF, joint development, assessments) funds transit investments",
            "Form-based codes and density bonuses incentivize TOD",
            "Community opposition and gentrification are major implementation challenges",
            "TOD takes 10-20 years to fully develop; requires long-term commitment"
        ],
        primary_authority=[
            "TCRP Report 128: Effects of TOD on Housing, Parking, and Travel",
            "Reconnecting America / CTOD: TOD best practices",
            "Urban Land Institute (ULI): TOD case studies and guides"
        ],
        burden_holder="Local governments (zoning authority), transit agencies (joint development), developers",
        adversary_position="TOD is social engineering; let market determine development patterns",
        counter_arguments=[
            "Auto-oriented sprawl is financially unsustainable and environmentally destructive",
            "TOD increases transit ridership and reduces operating subsidy per passenger",
            "Land value capture is fair way to fund transit from beneficiaries",
            "Walkable, mixed-use neighborhoods are in high market demand",
            "Climate and equity goals require reducing auto dependency"
        ],
        resolution_strategy="Adopt TOD-supportive zoning (density bonuses, parking maximums, form-based codes) near all new and existing stations, pursue joint development and value capture to fund transit, invest in pedestrian and bicycle infrastructure, engage communities early on TOD plans, include affordable housing requirements to mitigate gentrification, coordinate long-term land use and transit planning.",
        entity_scope="All passenger rail systems with stations in areas with development potential",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="TOD benefits are well-documented; implementation success depends on local political and market context",
        controlling_precedent="Successful TOD examples (Portland, Washington DC, Hong Kong, Tokyo) demonstrate ridership and fiscal benefits",
        issue_category=IssueCategory.INTEGRATION,
        authority_level=AuthorityLevel.BEST_PRACTICE,
        fact_fragility_score=0.25
    ),

]


# ============================================================================
# TELEMETRY AND METRICS
# ============================================================================

@dataclass
class QueryTelemetry:
    """Track query processing metrics"""
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    start_time: float
    end_time: float
    triggered_doctrines: List[str]
    confidence: ConfidenceLevel
    fact_fragility_score: float
    response_length: int

    def duration_ms(self) -> float:
        """Calculate query duration in milliseconds"""
        return (self.end_time - self.start_time) * 1000


class MetricsCollector:
    """Collect and aggregate system metrics"""

    def __init__(self):
        self.total_queries = 0
        self.total_response_time_ms = 0.0
        self.doctrine_hit_counts: Dict[str, int] = {}
        self.mode_counts: Dict[str, int] = {}
        self.zone_counts: Dict[str, int] = {}
        self.start_time = datetime.now(timezone.utc)

    def record_query(self, telemetry: QueryTelemetry):
        """Record metrics from a query"""
        self.total_queries += 1
        self.total_response_time_ms += telemetry.duration_ms()

        for doctrine in telemetry.triggered_doctrines:
            self.doctrine_hit_counts[doctrine] = self.doctrine_hit_counts.get(doctrine, 0) + 1

        mode_str = telemetry.mode.value
        self.mode_counts[mode_str] = self.mode_counts.get(mode_str, 0) + 1

        zone_str = telemetry.zone.value
        self.zone_counts[zone_str] = self.zone_counts.get(zone_str, 0) + 1

    def avg_response_time_ms(self) -> float:
        """Calculate average response time"""
        if self.total_queries == 0:
            return 0.0
        return self.total_response_time_ms / self.total_queries

    def uptime_seconds(self) -> float:
        """Calculate uptime in seconds"""
        return (datetime.now(timezone.utc) - self.start_time).total_seconds()


# ============================================================================
# CORE ENGINE
# ============================================================================

class RAIL05PassengerOperationsEngine:
    """
    RAIL05 Passenger Rail Operations Intelligence Engine
    TIE-Grade autonomous analysis system
    """

    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.metrics = MetricsCollector()
        self.version = "1.0.0"
        self.port = 9211

        logger.info(f"RAIL05 Engine initialized with {len(self.doctrines)} doctrine blocks")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
        context: Optional[Dict[str, Any]] = None
    ) -> QueryResponse:
        """
        Three-layer response system:
        Layer 1: Doctrine cache (0-200ms) - Pre-compiled expert blocks
        Layer 2: Semantic retrieval (200ms-2s) - Vector search if cache miss
        Layer 3: Deep analysis (2s+) - Multi-source synthesis
        """
        start_time = datetime.now(timezone.utc).timestamp()

        # Layer 1: Doctrine cache lookup
        triggered = self._search_doctrine_cache(query, context)

        if triggered:
            logger.info(f"Doctrine cache hit: {len(triggered)} blocks triggered")
            answer, confidence, fact_fragility = self._synthesize_from_doctrines(
                query, triggered, mode, zone
            )
        else:
            # Layer 2: Semantic retrieval (simulated - would use vector DB)
            logger.info("Doctrine cache miss, using semantic retrieval")
            answer, confidence, fact_fragility = self._semantic_retrieval(query, mode, zone)

        # Extract authority chain
        authority_chain = [d.primary_authority[0] for d in triggered[:3]] if triggered else []

        # Calculate determinism hash
        determinism_hash = self._calculate_hash(query, answer, triggered)

        end_time = datetime.now(timezone.utc).timestamp()
        response_time_ms = (end_time - start_time) * 1000

        # Record telemetry
        telemetry = QueryTelemetry(
            query=query,
            mode=mode,
            zone=zone,
            start_time=start_time,
            end_time=end_time,
            triggered_doctrines=[d.topic for d in triggered],
            confidence=confidence,
            fact_fragility_score=fact_fragility,
            response_length=len(answer)
        )
        self.metrics.record_query(telemetry)

        return QueryResponse(
            query=query,
            mode=mode,
            zone=zone,
            answer=answer,
            confidence=confidence,
            triggered_doctrines=[d.topic for d in triggered],
            authority_chain=authority_chain,
            fact_fragility_score=fact_fragility,
            determinism_hash=determinism_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
            response_time_ms=response_time_ms
        )

    def _search_doctrine_cache(
        self,
        query: str,
        context: Optional[Dict[str, Any]]
    ) -> List[DoctrineBlock]:
        """Search doctrine cache for relevant blocks"""
        query_lower = query.lower()
        triggered = []

        for doctrine in self.doctrines:
            # Check keyword matches
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
            topic_match = any(word in query_lower for word in doctrine.topic.lower().split())

            if keyword_matches >= 2 or topic_match:
                triggered.append(doctrine)

        # Sort by relevance (keyword matches)
        triggered.sort(
            key=lambda d: sum(1 for kw in d.keywords if kw.lower() in query_lower),
            reverse=True
        )

        return triggered[:5]  # Return top 5 most relevant

    def _synthesize_from_doctrines(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> tuple[str, ConfidenceLevel, float]:
        """Synthesize answer from triggered doctrine blocks"""

        if mode == ResponseMode.FAST:
            # Concise response from first doctrine
            primary = doctrines[0]
            answer = f"{primary.conclusion_template}\n\nKey factors: {', '.join(primary.key_factors[:3])}"
            confidence = primary.confidence
            fragility = primary.fact_fragility_score

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready response with authority
            parts = []
            for d in doctrines[:3]:
                parts.append(f"**{d.topic}**\n{d.conclusion_template}\n\nAuthority: {d.primary_authority[0]}")
            answer = "\n\n".join(parts)
            confidence = ConfidenceLevel.DEFENSIBLE
            fragility = sum(d.fact_fragility_score for d in doctrines[:3]) / 3

        else:  # MEMO
            # Full documentation with reasoning
            parts = [f"# Passenger Rail Operations Analysis: {query}\n"]
            for d in doctrines[:3]:
                parts.append(f"\n## {d.topic}\n")
                parts.append(f"{d.conclusion_template}\n")
                parts.append(f"\n### Analysis Framework\n{d.reasoning_framework[:500]}...\n")
                parts.append(f"\n### Key Factors\n" + "\n".join(f"- {kf}" for kf in d.key_factors[:5]))
                parts.append(f"\n### Primary Authority\n" + "\n".join(f"- {auth}" for auth in d.primary_authority))
            answer = "\n".join(parts)
            confidence = ConfidenceLevel.DEFENSIBLE
            fragility = sum(d.fact_fragility_score for d in doctrines[:3]) / 3

        # Apply epistemic guardrails
        if zone == AnalysisZone.AUDIT:
            answer += "\n\n**DISCLOSURE**: This analysis is based on industry standards and regulatory frameworks current as of knowledge cutoff. Specific operational contexts may require additional considerations."

        return answer, confidence, fragility

    def _semantic_retrieval(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> tuple[str, ConfidenceLevel, float]:
        """Fallback semantic retrieval (simulated)"""
        answer = f"Passenger rail operations analysis for: {query}\n\nThis query did not trigger specific doctrine blocks. General principles apply: optimize schedules for passenger convenience and operational efficiency, ensure adequate capacity and service quality, comply with safety regulations, integrate with land use and other modes for network utility."

        return answer, ConfidenceLevel.DISCLOSURE, 0.5

    def _calculate_hash(
        self,
        query: str,
        answer: str,
        doctrines: List[DoctrineBlock]
    ) -> str:
        """Calculate SHA-256 determinism hash"""
        content = f"{query}|{answer}|{','.join(d.topic for d in doctrines)}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def health_check(self) -> HealthResponse:
        """Comprehensive health check"""
        return HealthResponse(
            status="healthy",
            engine="RAIL05_passenger_operations",
            version=self.version,
            port=self.port,
            doctrines_loaded=len(self.doctrines),
            uptime_seconds=self.metrics.uptime_seconds(),
            total_queries=self.metrics.total_queries,
            avg_response_time_ms=self.metrics.avg_response_time_ms()
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="RAIL05 Passenger Rail Operations Intelligence Engine",
    description="TIE-Grade autonomous analysis for passenger rail operations",
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
engine = RAIL05PassengerOperationsEngine()


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "engine": "RAIL05_passenger_operations",
        "version": "1.0.0",
        "status": "operational",
        "description": "TIE-Grade Passenger Rail Operations Intelligence Engine"
    }


@app.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """
    Main query endpoint for passenger rail operations analysis
    """
    try:
        response = engine.three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            context=request.context
        )
        return response
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return engine.health_check()


@app.get("/doctrines", response_model=List[Dict[str, Any]])
async def list_doctrines():
    """List all available doctrine blocks"""
    return [d.to_dict() for d in engine.doctrines]


@app.get("/metrics", response_model=Dict[str, Any])
async def get_metrics():
    """Retrieve system metrics"""
    return {
        "total_queries": engine.metrics.total_queries,
        "avg_response_time_ms": engine.metrics.avg_response_time_ms(),
        "uptime_seconds": engine.metrics.uptime_seconds(),
        "doctrine_hit_counts": engine.metrics.doctrine_hit_counts,
        "mode_distribution": engine.metrics.mode_counts,
        "zone_distribution": engine.metrics.zone_counts
    }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting RAIL05 Passenger Rail Operations Engine on port 9211")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9211,
        log_level="info"
    )
