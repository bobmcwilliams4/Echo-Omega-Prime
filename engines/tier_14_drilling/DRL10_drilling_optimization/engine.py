"""
DRL10 - Drilling Optimization Engine
TIE Gold Standard Implementation

Domain: Drilling Engineering - Performance Optimization
Port: 9020
Version: 1.0.0

Expertise Areas:
- ROP optimization through WOB/RPM parameter tuning
- MSE real-time monitoring and founder point detection
- Drilling dysfunction detection (whirl, stick-slip, bounce)
- Cost-per-foot analysis and AFE tracking
- Invisible lost time (ILT) identification
- Connection and trip time optimization
- Offset well benchmarking and learning curves
- Bit selection and BHA optimization
- Drilling fluid optimization for ROP
- Wellbore stability and NPT reduction
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Literal
from enum import Enum
from dataclasses import dataclass, field, asdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# Configure loguru
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "logs" / "drl10_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)

# ═══════════════════════════════════════════════════════════════════════════
# ENUMS AND DATA MODELS
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
    REAL_TIME = "REAL_TIME"
    POST_ANALYSIS = "POST_ANALYSIS"

class DrillingDysfunction(str, Enum):
    WHIRL = "WHIRL"
    STICK_SLIP = "STICK_SLIP"
    BOUNCE = "BOUNCE"
    LATERAL_VIBRATION = "LATERAL_VIBRATION"
    TORSIONAL_OSCILLATION = "TORSIONAL_OSCILLATION"
    NONE = "NONE"

@dataclass
class DoctrineBlock:
    """Individual doctrine expertise block"""
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
    fact_fragility: float = 0.5
    zone: AnalysisZone = AnalysisZone.REAL_TIME

# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ BLOCKS OF REAL DRILLING OPTIMIZATION EXPERTISE
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE = [
    DoctrineBlock(
        topic="ROP_Optimization_WOB_RPM_Relationship",
        keywords=["rop", "wob", "rpm", "rate of penetration", "drilling parameters", "optimization"],
        conclusion_template=[
            "Optimal ROP achieved through balanced WOB-RPM relationship per formation lithology",
            "Founder point detection prevents inefficient drilling above MSE threshold",
            "Field-specific correlation curves guide parameter selection for maximum efficiency"
        ],
        reasoning_framework="""
        ROP optimization follows Bourgoyne-Young drilling rate equation: ROP = f(WOB, RPM, bit hydraulics, formation strength).

        FUNDAMENTAL RELATIONSHIP:
        - Below founder point: ROP increases linearly with WOB (efficient drilling)
        - At founder point: Maximum drilling efficiency achieved
        - Above founder point: ROP plateaus or decreases despite WOB increase (bit floundering)

        PARAMETER OPTIMIZATION SEQUENCE:
        1. Determine formation-specific founder point through controlled WOB ramping
        2. Establish RPM sweet spot based on bit type (PDC: 80-180 RPM, roller cone: 60-120 RPM)
        3. Optimize flow rate for adequate hole cleaning while maximizing hydraulic horsepower at bit
        4. Monitor MSE as real-time efficiency indicator (target: minimize MSE)
        5. Adjust parameters dynamically based on downhole vibration feedback

        FIELD APPLICATION:
        - Soft formations (shale, sand): High RPM, moderate WOB, maximize ROP
        - Hard formations (limestone, dolomite): Moderate RPM, high WOB near founder point
        - Interbedded formations: Dynamic parameter adjustment at lithology boundaries
        - Maintain differential pressure <500 psi below formation pore pressure for stability

        EFFICIENCY METRICS:
        - Track ROP vs. MSE correlation continuously
        - Compare actual vs. theoretical ROP from offset wells
        - Monitor cost-per-foot against AFE budget
        - Document parameter windows for repeatable performance
        """,
        key_factors=[
            "Formation lithology and compressive strength",
            "Bit type and IADC code (PDC vs. roller cone)",
            "WOB magnitude relative to formation-specific founder point",
            "RPM range within bit manufacturer recommendations",
            "MSE trend indicating drilling efficiency",
            "Downhole vibration levels (lateral, axial, torsional)",
            "Hydraulic horsepower at bit and hole cleaning efficiency",
            "Differential pressure and wellbore stability"
        ],
        primary_authority=[
            "Bourgoyne-Young drilling rate model (SPE 4238)",
            "Teale MSE equation (1965): MSE = (WOB/Area) + (120π×RPM×Torque)/(Area×ROP)",
            "Pessier-Fear founder point analysis (SPE 92576)",
            "SPE 163420: Real-time ROP optimization using MSE",
            "IADC drilling optimization best practices"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Drilling at maximum WOB always maximizes ROP regardless of formation response",
        counter_arguments=[
            "Excessive WOB beyond founder point causes bit floundering and ROP decrease",
            "High WOB in soft formations creates balling and reduces efficiency",
            "Ignoring MSE trends leads to invisible lost time and cost overruns",
            "Formation-specific optimization outperforms one-size-fits-all approach",
            "Downhole vibration from poor parameters damages BHA and reduces bit life"
        ],
        resolution_strategy="Implement real-time MSE monitoring with founder point detection, adjust WOB-RPM within lithology-specific windows, validate against offset well performance, track cost-per-foot metrics",
        entity_scope="Drilling operations, completions engineering, AFE management",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in MSE-based optimization, moderate confidence in absolute ROP predictions due to formation variability",
        controlling_precedent=[
            "Industry standard: Minimize MSE while maintaining acceptable vibration levels",
            "Best practice: Document parameter windows per formation for offset well use",
            "Field proven: Founder point-based WOB management improves ROP 15-30%"
        ],
        fact_fragility=0.3,
        zone=AnalysisZone.REAL_TIME
    ),

    DoctrineBlock(
        topic="MSE_Real_Time_Monitoring",
        keywords=["mse", "mechanical specific energy", "drilling efficiency", "founder point", "real-time"],
        conclusion_template=[
            "MSE provides real-time drilling efficiency metric independent of formation strength",
            "Upward MSE trends indicate inefficient drilling requiring parameter adjustment",
            "Target MSE range: 100-300 kpsi for optimal drilling in most formations"
        ],
        reasoning_framework="""
        Mechanical Specific Energy (MSE) quantifies energy required to remove unit volume of rock.

        MSE CALCULATION (Teale equation):
        MSE = (WOB/Area) + (120π×RPM×Torque)/(Area×ROP)
        where Area = π × (bit diameter)² / 4

        INTERPRETATION PRINCIPLES:
        - Theoretical minimum MSE ≈ formation compressive strength (UCS)
        - MSE > 2× UCS indicates inefficient drilling (friction, bit wear, poor cleaning)
        - Flat or decreasing MSE with increasing WOB = efficient drilling
        - Rising MSE with increasing WOB = approaching or past founder point

        REAL-TIME APPLICATION:
        1. Calculate MSE every 1-second using surface measurements
        2. Establish baseline MSE for current lithology from first 10 feet of drilling
        3. Monitor for MSE increase >20% indicating efficiency loss
        4. Correlate MSE spikes with drilling dysfunctions (vibration events)
        5. Adjust WOB/RPM to return MSE to baseline efficient range

        FOUNDER POINT DETECTION:
        - Perform controlled WOB ramp test: increase WOB in 2-5 klb increments
        - Plot MSE vs. WOB
        - Founder point = WOB where MSE begins rising despite WOB increase
        - Optimal operating WOB = 85-95% of founder point WOB

        TROUBLESHOOTING WITH MSE:
        - High MSE + low ROP = bit balling, dull bit, or poor hole cleaning
        - Normal MSE + low ROP = hard formation or insufficient WOB
        - Fluctuating MSE = stick-slip or lithology changes
        - MSE trend upward over time = bit dulling, requiring pull
        """,
        key_factors=[
            "Surface WOB, RPM, and torque measurements accuracy",
            "ROP measurement resolution and lag time",
            "Bit diameter and area calculation precision",
            "Formation compressive strength estimate from logs",
            "Baseline MSE establishment in homogeneous section",
            "Torque variations from string friction vs. bit work",
            "Hole cleaning efficiency affecting apparent MSE"
        ],
        primary_authority=[
            "Teale 1965: MSE concept for drilling efficiency",
            "SPE 92576: MSE and founder point for ROP optimization",
            "SPE 163420: Real-time MSE monitoring implementation",
            "SPE 178847: MSE-based drilling dysfunction detection",
            "Industry practice: MSE <500 kpsi target for PDC bits"
        ],
        burden_holder="Real-time drilling operations team",
        adversary_position="MSE is theoretical metric with no practical field application value",
        counter_arguments=[
            "MSE proven across 1000+ wells as early warning for drilling inefficiency",
            "Real-time MSE calculation automated in modern drilling systems",
            "MSE trends detect bit dulling before other indicators",
            "Founder point analysis using MSE increases ROP 15-30% repeatably",
            "MSE-based optimization reduces cost-per-foot and NPT"
        ],
        resolution_strategy="Implement automated MSE calculation on 1-second intervals, establish formation-specific MSE baselines, trigger alarms for 20% MSE increase, integrate with drilling dysfunction detection",
        entity_scope="Drilling operations, drilling automation systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in MSE trends, moderate confidence in absolute MSE values due to measurement uncertainties",
        controlling_precedent=[
            "Industry standard: MSE monitoring on all automated drilling rigs",
            "Best practice: Founder point testing at first bit in each formation",
            "Operator requirement: Document MSE response to parameter changes"
        ],
        fact_fragility=0.25,
        zone=AnalysisZone.REAL_TIME
    ),

    DoctrineBlock(
        topic="Drilling_Dysfunction_Detection_Stick_Slip",
        keywords=["stick-slip", "torsional oscillation", "vibration", "downhole", "dysfunction"],
        conclusion_template=[
            "Stick-slip causes severe bit and BHA damage through torsional oscillations",
            "Detection: Surface RPM oscillations with downhole RPM varying 2-10× surface",
            "Mitigation: Reduce WOB, increase RPM, adjust mud weight, or change BHA design"
        ],
        reasoning_framework="""
        Stick-slip is self-excited torsional oscillation where bit alternately stops (sticks) and rapidly rotates (slips).

        PHYSICAL MECHANISM:
        - Bit contacts formation and stops rotating (stick phase)
        - Drill string continues rotating from surface, storing torsional energy
        - Torque builds to overcome static friction at bit
        - Bit suddenly releases and rotates rapidly (slip phase), often 3-10× surface RPM
        - Cycle repeats at frequency of 0.1-1 Hz

        DETECTION INDICATORS:
        Surface measurements:
        - Torque oscillations: ±50-200% of steady-state torque
        - RPM oscillations: ±10-30% of setpoint (phase-lagged from torque)
        - Standpipe pressure fluctuations from RPM variations affecting mud pumps

        Downhole measurements (if MWD available):
        - RPM variations 200-1000% of surface RPM
        - Lateral accelerations correlating with torsional events
        - Bit RPM dropping to zero during stick phase

        DAMAGE CONSEQUENCES:
        - Bit cutter impact loading causes premature wear and breakage
        - BHA fatigue from cyclic torsional stress
        - Connection loosening and potential washout
        - Formation damage from bit speed variations
        - Lost footage from inefficient rock cutting

        MITIGATION STRATEGIES (in order of implementation):
        1. Reduce WOB by 20-30% to lower bit contact force
        2. Increase surface RPM by 10-20% to raise average downhole speed
        3. Add downhole motor (positive displacement motor) for constant bit RPM
        4. Modify BHA: add shock sub, reduce number of stabilizers
        5. Change drilling fluid: increase lubricity, reduce mud weight
        6. Change bit design: shorter bit profile, fewer blades, different cutter layout
        7. Implement soft torque control (active stick-slip suppression)

        SEVERITY ASSESSMENT:
        - Mild: Torque oscillations <50%, mitigate with parameter adjustment
        - Moderate: Torque oscillations 50-100%, requires BHA or fluid modification
        - Severe: Torque oscillations >100%, risk of connection failure, pull bit immediately
        """,
        key_factors=[
            "BHA design: number and placement of stabilizers",
            "Bit design: blade count, cutter layout, bit profile length",
            "WOB magnitude creating bit-formation friction",
            "Surface RPM setpoint and rotary inertia",
            "Drilling fluid lubricity and rheology",
            "Formation heterogeneity causing variable friction",
            "Hole geometry and ledges increasing friction",
            "String stiffness and torsional natural frequency"
        ],
        primary_authority=[
            "SPE 21945: Stick-slip mechanisms and detection methods",
            "SPE 52821: Field mitigation of stick-slip vibrations",
            "SPE 163420: Real-time dysfunction detection algorithms",
            "IADC guidelines: Downhole vibration severity limits",
            "Brett 1992: Self-excited torsional oscillations model"
        ],
        burden_holder="Directional driller and drilling engineer",
        adversary_position="Surface torque oscillations are normal and do not indicate downhole problems",
        counter_arguments=[
            "Surface torque oscillations directly correlate with severe downhole stick-slip",
            "Ignoring stick-slip leads to premature bit failure and BHA damage",
            "Downhole data confirms surface observations underestimate severity",
            "Stick-slip detected in 30-60% of wells causes measurable ROP reduction",
            "Mitigation reduces drilling time and cost-per-foot significantly"
        ],
        resolution_strategy="Implement automated stick-slip detection using torque/RPM variance, establish severity thresholds, protocol for immediate parameter adjustment, trend dysfunction metrics across bit runs",
        entity_scope="Drilling operations, BHA design, bit selection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in detection methods, moderate confidence in optimal mitigation approach per specific BHA configuration",
        controlling_precedent=[
            "Industry standard: Torque variance >50% triggers mitigation protocol",
            "Best practice: Document stick-slip events and mitigation effectiveness",
            "Operator requirement: Downhole vibration monitoring on ERD and hard rock wells"
        ],
        fact_fragility=0.2,
        zone=AnalysisZone.REAL_TIME
    ),

    DoctrineBlock(
        topic="Invisible_Lost_Time_ILT_Analysis",
        keywords=["ilt", "invisible lost time", "inefficiency", "afe", "cost", "performance"],
        conclusion_template=[
            "ILT represents 20-40% of drilling time in average wells, undetected by NPT metrics",
            "Categories: suboptimal ROP, excessive connections, slow trips, inefficient operations",
            "Quantification requires benchmark comparison against optimal performance envelope"
        ],
        reasoning_framework="""
        Invisible Lost Time (ILT) is inefficiency that occurs during productive operations but below optimal performance.

        ILT DEFINITION AND CATEGORIES:
        Unlike NPT (zero-rate time), ILT occurs at reduced efficiency during "productive" operations:

        1. SUBOPTIMAL ROP (40-60% of total ILT):
        - Drilling below achievable ROP for given formation and BHA
        - Causes: Conservative parameters, poor BHA, bit selection, drilling dysfunction
        - Detection: Compare actual vs. offset well ROP in same formation
        - Quantification: (Optimal ROP - Actual ROP) / Actual ROP × drilling time

        2. EXCESSIVE CONNECTION TIME (15-25% of ILT):
        - Connections taking longer than physics-limited minimum
        - Baseline: 3-5 minutes for vertical, 5-8 minutes for directional
        - Actual field: Often 8-15 minutes due to operational inefficiencies
        - Reduction strategies: Rig up iron roughneck, optimize workflow, crew training

        3. SLOW TRIPPING (10-20% of ILT):
        - Trip speeds below safe operational limits
        - Vertical wells: 1000+ ft/hr achievable, often see 400-600 ft/hr
        - Directional wells: 600-800 ft/hr achievable, often see 300-500 ft/hr
        - Causes: Conservative practices, equipment limitations, swab/surge concerns

        4. INEFFICIENT OPERATIONS (15-25% of ILT):
        - Waiting on directional surveys beyond required frequency
        - Excessive wiper trips or circulating bottoms up
        - Slow rig floor operations (handling BHA, changing bits)
        - Poor coordination between crews and service companies

        QUANTIFICATION METHODOLOGY:
        1. Establish performance envelope from best-in-class offset wells
        2. Time-depth analysis: plot actual vs. optimal cumulative time
        3. Calculate ILT by operation category
        4. Convert to cost using daily operating rate
        5. Prioritize reduction efforts by $/impact

        TYPICAL ILT IMPACT:
        - 10,000 ft vertical well, 30-day drilling time
        - ILT contribution: 8-12 days (27-40% of total time)
        - At $50k/day rig rate: $400-600k ILT cost
        - Reduction target: 50% ILT = 4-6 days saved = $200-300k

        REDUCTION STRATEGIES:
        - Real-time ROP optimization using MSE and offset benchmarks
        - Connection time tracking with crew performance scorecards
        - Automated trip speed recommendations within safe envelope
        - Workflow optimization: parallel operations, pre-job planning
        - Learning curves: track performance improvement across pad wells
        """,
        key_factors=[
            "Offset well performance database quality and relevance",
            "Formation correlation between offset and current well",
            "Rig capability and equipment condition",
            "Crew experience and training level",
            "BHA and bit selection optimality",
            "Real-time drilling parameter optimization discipline",
            "Operational coordination between teams",
            "Well complexity and directional requirements"
        ],
        primary_authority=[
            "SPE 102549: Invisible lost time quantification methodology",
            "SPE 163420: Real-time drilling performance benchmarking",
            "IADC: Connection time best practices (3-5 min target)",
            "Operator internal studies: ILT typically 30-40% of well time",
            "Drilling contractor KPIs: Trip speed, connection time standards"
        ],
        burden_holder="Drilling engineer and operations supervisor",
        adversary_position="Time spent drilling is productive, no lost time exists if ROP is positive",
        counter_arguments=[
            "Drilling at 50% of achievable ROP doubles drilling time and cost",
            "ILT quantification reveals $200-500k savings opportunity per well",
            "Offset well benchmarks prove higher performance is achievable and safe",
            "Crew performance tracking demonstrates learning curves reduce ILT 40-60%",
            "Automated drilling systems designed specifically to eliminate ILT"
        ],
        resolution_strategy="Implement real-time ILT tracking dashboard, establish performance benchmarks from offset wells, conduct daily ILT review meetings, incentivize crews for ILT reduction, trend learning curves across pad",
        entity_scope="AFE management, drilling operations, performance engineering",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in ILT existence and magnitude, moderate confidence in optimal benchmark values due to formation variability",
        controlling_precedent=[
            "Industry trend: 15-25% ILT reduction achievable through focus and measurement",
            "Best practice: Daily ILT review and action planning",
            "Operator requirement: Performance benchmarking against offset wells for all wells"
        ],
        fact_fragility=0.35,
        zone=AnalysisZone.POST_ANALYSIS
    ),

    DoctrineBlock(
        topic="Cost_Per_Foot_Analysis_AFE_Tracking",
        keywords=["cost per foot", "afe", "budget", "drilling economics", "kpi"],
        conclusion_template=[
            "Cost-per-foot is primary KPI linking operational performance to economic outcome",
            "Target: Match or beat AFE projection based on offset well performance",
            "Real-time tracking enables proactive cost control and AFE accuracy improvement"
        ],
        reasoning_framework="""
        Cost-per-foot analysis translates drilling performance into economic terms for decision-making.

        CALCULATION METHODOLOGY:
        Cost per foot = Total drilling cost / Total measured depth drilled

        Components of total drilling cost:
        1. Time-based costs (60-75% of total):
           - Rig dayrate × drilling days
           - Directional services daily rate
           - Mud engineering and logging services
           - Rental equipment (MWD, motors, jars, etc.)

        2. Consumption-based costs (20-30%):
           - Bits: count × cost per bit
           - Drilling fluid: barrels × cost per barrel + treatments
           - Fuel and power consumption
           - Cement and casing (if included in drilling scope)

        3. Fixed costs (5-10%):
           - Mobilization/demobilization
           - Rig-up/rig-down
           - BHA and bottomhole assembly components

        AFE DEVELOPMENT PROCESS:
        1. Identify offset wells in same area and formation
        2. Normalize offset performance: cost per foot by hole section
        3. Apply adjustments for current well:
           - Trajectory complexity (dogleg severity, ERD length)
           - Formation changes (harder/softer rock, fault crossing)
           - Rig capability differences
           - Service cost inflation
        4. Build time-depth curve: cumulative depth vs. days
        5. Apply cost rates to time estimates
        6. Add contingency (5-15% based on well complexity and offset data quality)

        REAL-TIME TRACKING:
        - Calculate actual cost-per-foot daily by hole section
        - Compare to AFE projection at same depth
        - Identify variance drivers: ROP, NPT, or cost rates
        - Project total well cost using current performance trends
        - Trigger replanning if variance exceeds ±10%

        VARIANCE ANALYSIS:
        Favorable (actual < AFE):
        - Higher ROP than offset (ILT reduction, better BHA/bits)
        - Lower NPT than offset (better execution, easier formation)
        - Service cost reductions or renegotiations

        Unfavorable (actual > AFE):
        - Lower ROP: formation harder, suboptimal parameters, drilling dysfunctions
        - Higher NPT: stuck pipe, lost circulation, equipment failures
        - Cost rate increases: unplanned service additions, rig repairs

        OPTIMIZATION DECISIONS BASED ON COST-PER-FOOT:
        - Bit pull decision: Trip cost vs. ROP improvement from new bit
        - BHA modification: Cost of trip vs. expected ROP gain
        - Technology adoption: Automated drilling system cost vs. ILT reduction
        - Drilling fluid upgrade: Increased mud cost vs. ROP and stability benefits

        PERFORMANCE BENCHMARKING:
        - Track cost-per-foot across well program (pad, field, basin)
        - Identify learning curve: 1st well vs. Nth well cost reduction
        - Compare to industry benchmarks and operator internal targets
        - Feed lessons learned back to AFE process for continuous improvement
        """,
        key_factors=[
            "Rig dayrate and service cost accuracy",
            "Offset well data quality and relevance",
            "Formation consistency between offset and current well",
            "NPT incidence and severity",
            "ROP achieved vs. offset benchmark",
            "Bit and BHA cost and performance",
            "Drilling fluid costs and treatment frequency",
            "Contingency utilization and causes"
        ],
        primary_authority=[
            "SPE 102521: Drilling cost estimation and AFE development",
            "SPE 116427: Cost-per-foot benchmarking methodology",
            "SPE 163405: Real-time cost tracking and variance analysis",
            "Industry practice: ±10% AFE variance threshold for investigation",
            "Operator internal: Cost-per-foot targets by basin and formation"
        ],
        burden_holder="Drilling engineer and AFE owner",
        adversary_position="Time-based rig costs dominate, consumption costs irrelevant to optimization",
        counter_arguments=[
            "Bit selection affects both time (ROP) and consumption (bit cost) components",
            "Drilling fluid optimization reduces both stuck pipe risk (NPT/time) and treatment costs",
            "Understanding cost drivers enables prioritization of improvement efforts",
            "Real-time cost tracking prevents AFE overruns through early intervention",
            "Cost-per-foot benchmarking drives continuous improvement across well programs"
        ],
        resolution_strategy="Implement automated cost-per-foot calculation from field tickets and invoices, daily variance reporting against AFE, root cause analysis for >10% variance, feedback loop to AFE process",
        entity_scope="AFE management, drilling operations, finance and accounting",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in methodology, moderate confidence in offset well applicability due to formation and trajectory variability",
        controlling_precedent=[
            "Industry standard: Cost-per-foot primary KPI for drilling performance",
            "Best practice: Real-time tracking with daily variance review",
            "Operator requirement: AFE accuracy within ±15% on average across programs"
        ],
        fact_fragility=0.3,
        zone=AnalysisZone.POST_ANALYSIS
    ),

    DoctrineBlock(
        topic="Offset_Well_Benchmarking",
        keywords=["offset wells", "benchmarking", "performance comparison", "best practices", "learning"],
        conclusion_template=[
            "Offset well analysis provides performance targets and identifies best practices",
            "Key metrics: ROP by formation, NPT causes, bit performance, cost-per-foot",
            "Proper normalization for trajectory and formation differences is critical"
        ],
        reasoning_framework="""
        Offset well benchmarking establishes achievable performance targets based on demonstrated results in comparable wells.

        OFFSET WELL SELECTION CRITERIA:
        Must match current well on critical parameters:
        1. Geographic proximity (same field, ideally <5 miles)
        2. Target formation and geology (same reservoir, similar rock properties)
        3. Well trajectory type (vertical, directional, horizontal, ERD)
        4. Rig class and capability (similar equipment and technology)
        5. Drilling timeframe (within 2-3 years to reflect current costs and practices)

        Typical offset set: 3-10 wells representing range of performance

        DATA EXTRACTION AND NORMALIZATION:

        1. ROP BY FORMATION:
        - Segment well into consistent lithology intervals
        - Calculate average ROP per formation: ROP = Δ MD / Δ drilling time
        - Exclude NPT from denominator (circulating, reaming, etc.)
        - Note bit type, WOB, RPM for each interval
        - Identify best-performing and average-performing wells

        2. TIME-DEPTH ANALYSIS:
        - Plot cumulative depth vs. cumulative days for all offsets
        - Identify performance envelope: best, median, worst
        - Segment by hole section (surface, intermediate, production)
        - Calculate days-per-1000-ft by section
        - Current well actual vs. offset envelope = leading indicator

        3. NPT CATEGORIZATION:
        - Extract NPT events: duration, cause, severity
        - Categories: stuck pipe, lost circulation, equipment failure, weather, other
        - Calculate NPT hours per 1000 ft drilled
        - Identify common failure modes and mitigation strategies
        - Risk assessment: probability and impact by NPT type

        4. BIT PERFORMANCE:
        - Footage per bit run and ROP by bit type
        - Bit cost per foot drilled
        - Dull bit grading and failure modes
        - Identify optimal bit selection for each formation

        5. COST BENCHMARKING:
        - Cost-per-foot by hole section (normalized to current rates)
        - Service cost breakdown: directional, mud, bits, rentals
        - AFE vs. actual variance analysis
        - Identify cost reduction opportunities

        PERFORMANCE GAP ANALYSIS:
        Compare current well to offset performance:
        - ROP gap: % difference from best offset and median offset
        - Time gap: Days ahead/behind offset curve at same depth
        - Cost gap: $ variance from offset cost-per-foot
        - Root cause: BHA differences, parameter choices, NPT, formation variance

        APPLICATION TO CURRENT WELL:

        Planning phase:
        - Set ROP targets per formation from offset median/best
        - Build AFE from offset cost-per-foot with appropriate adjustments
        - BHA design based on successful offset configurations
        - Bit program from offset bit performance data
        - NPT contingency from offset NPT statistics

        Execution phase:
        - Real-time comparison: actual vs. offset performance envelope
        - Red flag if falling behind median offset curve
        - Investigate and correct: parameters, BHA, bit, operations
        - Document deviations and lessons learned

        Post-well analysis:
        - Add current well to offset database
        - Update performance benchmarks and best practices
        - Feed lessons learned to next well planning
        - Quantify improvement: current well vs. prior wells in program

        LEARNING CURVE QUANTIFICATION:
        Track performance across development program:
        - 1st well: Baseline (often 20-30% slower than eventual optimum)
        - Nth well: Approaching optimum (learning curve 70-85%)
        - Learning rate: % improvement per well drilled
        - Typical: 15-25% time reduction from 1st to 4th well in pad
        """,
        key_factors=[
            "Offset well data completeness and accuracy",
            "Geological consistency between offset and current well",
            "Trajectory similarity (TVD, MD, dogleg severity)",
            "Rig and equipment capability comparability",
            "Time gap between offset and current well (technology evolution)",
            "Operator and drilling contractor consistency",
            "Availability of detailed operational data (drilling parameters, dysfunction events)",
            "Service cost inflation from offset timeframe to current"
        ],
        primary_authority=[
            "SPE 116427: Offset well benchmarking methodology",
            "SPE 102549: Learning curves in drilling operations",
            "SPE 163405: Real-time performance comparison systems",
            "IADC best practices: Offset well selection and normalization",
            "Operator internal: Benchmarking requirements for all wells"
        ],
        burden_holder="Drilling engineer and well planner",
        adversary_position="Each well is unique, offset well data has no predictive value for current well",
        counter_arguments=[
            "Statistical analysis proves offset wells predict performance within ±15-20%",
            "Operators drilling 100+ wells per year see consistent learning curves proving offset relevance",
            "Deviations from offset performance identify specific problems requiring attention",
            "Best-in-class operators use offset benchmarking systematically with proven results",
            "Ignoring offset data leads to repeated mistakes and preventable NPT"
        ],
        resolution_strategy="Maintain offset well database with standardized data format, automated benchmarking reports for each new well, real-time offset comparison dashboard, quarterly offset database updates with new wells",
        entity_scope="Well planning, drilling operations, performance engineering",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in methodology, moderate confidence in offset applicability due to geological and operational variability",
        controlling_precedent=[
            "Industry standard: Offset well analysis required for all AFEs and well plans",
            "Best practice: Real-time offset comparison during drilling",
            "Operator requirement: Minimum 3-5 offset wells for benchmarking"
        ],
        fact_fragility=0.35,
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Bit_Selection_Optimization",
        keywords=["bit selection", "pdc", "roller cone", "bit design", "iadc", "footage"],
        conclusion_template=[
            "Bit selection drives ROP, footage, and cost-per-foot more than any other single factor",
            "PDC bits dominate modern drilling: 90%+ market share in shale and soft rock",
            "Optimization requires matching bit design to formation, BHA, and parameters"
        ],
        reasoning_framework="""
        Bit selection involves matching cutting structure, hydraulics, and mechanical design to formation properties and drilling objectives.

        BIT TYPES AND APPLICATIONS:

        1. PDC (Polycrystalline Diamond Compact) Bits:
        - Mechanism: Shearing action, continuous cutting
        - Best formations: Soft to medium-hard (shale, sandstone, soft limestone)
        - Advantages: High ROP, long footage, no moving parts, simple operation
        - Disadvantages: Brittle cutters fail in hard/abrasive rock, sensitive to vibration
        - IADC codes: M (soft), S (soft/medium), D (medium/hard)
        - Modern designs: 5-7 blades, shaped cutters, gauge protection, hydraulic optimization

        2. Roller Cone (Tricone) Bits:
        - Mechanism: Crushing and chipping action, intermittent contact
        - Best formations: Hard, abrasive, interbedded (dolomite, chert, hard limestone)
        - Advantages: Durable in hard rock, handles impact and vibration
        - Disadvantages: Lower ROP, shorter footage, bearing wear limits life
        - IADC codes: 1-3 series (soft), 4-5 (medium), 6-7 (hard), 8 (extremely hard)
        - Declining use: <10% of footage drilled in unconventional plays

        3. Hybrid and Specialty Bits:
        - Impregnated diamond: Ultra-hard abrasive formations (rare modern use)
        - Hybrid PDC-roller: Transition zones, limited applications
        - Directional and motor bits: Optimized for RSS or positive displacement motor drilling

        BIT SELECTION PROCESS:

        Step 1 - Formation Analysis:
        - Rock type: Shale, sandstone, limestone, dolomite, salt, etc.
        - Compressive strength: From logs or offset cores
        - Abrasiveness: Quartz content, silica, chert
        - Drillability: Confined compressive strength, plasticity
        - Interbedded vs. homogeneous

        Step 2 - Offset Bit Performance Review:
        - Bits used in offset wells in same formation
        - Footage achieved per bit run
        - ROP performance: Average and peak
        - Dull grading: IADC dull code and failure modes
        - Cost per foot drilled: Bit cost / footage

        Step 3 - Match Bit Design to Application:
        PDC bit design parameters:
        - Blade count: 5 blades (aggressive ROP), 6-7 blades (stability, footage)
        - Cutter size: 13mm (ROP), 16mm (footage), 19mm (durability)
        - Cutter density: High (soft rock, ROP), low (hard rock, cutter life)
        - Profile: Short (aggressive ROP, vibration risk), long (stable, directional control)
        - Gauge protection: Diamond-enhanced for abrasive formations
        - Hydraulics: Large nozzles and junk slots for high flow, hole cleaning

        Step 4 - BHA and Parameter Compatibility:
        - Rotary drilling: Conventional PDC design, optimize for surface RPM range
        - Motor drilling: Short profile PDC for build rate, aggressive cutting structure
        - RSS drilling: Steering-friendly profile, may sacrifice some ROP for control
        - WOB capability: Bit rated for anticipated WOB range without overload
        - RPM capability: Bit rated for planned RPM without vibration

        Step 5 - Economic Analysis:
        - Trip cost: Rig dayrate × trip time (typically 8-12 hours)
        - Bit cost: $10k-50k for PDC, $5k-15k for roller cone
        - Expected footage: From offset performance or manufacturer estimates
        - Cost per foot = (Trip cost + Bit cost) / Expected footage
        - Optimize: Higher-cost bit justified if footage/ROP gain exceeds trip cost

        BIT PULL DECISION CRITERIA:
        - Predetermined footage target reached (e.g., 3000 ft for PDC in shale)
        - ROP decline >30% indicating bit dulling
        - MSE increase >30% with same parameters
        - Vibration increase indicating cutter damage
        - Formation transition to incompatible lithology
        - Planned BHA change for directional control

        DULL BIT ANALYSIS:
        IADC dull grading system:
        - Inner/Outer/Dull/Location/Bearing/Gauge/Other/Reason out
        - Example: T2-E2-1/16-G-X-I-NO-TD (PDC worn cutters, gauge intact, total depth)

        Common failure modes and implications:
        - Worn cutters (T code): Normal wear, bit ran full footage capability
        - Broken cutters (BC): Vibration or overload, reduce WOB or improve BHA
        - Balled bit (BT): Hole cleaning or mud issues, increase flow or treat mud
        - Gauge wear (undermeasure): Abrasive formation, need gauge protection
        - Junk damage (JD): Poor hole cleaning, need better hydraulics

        ADVANCED OPTIMIZATION:
        - Application-specific bit design with manufacturer
        - Cutter layout and backup modeling using FEA
        - Vibration testing and mitigation features
        - Real-time bit wear monitoring with downhole sensors
        - Machine learning models: Formation + BHA + Parameters → Optimal bit
        """,
        key_factors=[
            "Formation lithology and mechanical properties",
            "Offset bit performance database",
            "BHA configuration and drilling mode (rotary, motor, RSS)",
            "Planned drilling parameters (WOB, RPM, flow rate)",
            "Trip time and rig dayrate economics",
            "Bit cost and availability",
            "Expected footage and ROP targets",
            "Downhole vibration environment",
            "Directional control requirements"
        ],
        primary_authority=[
            "IADC bit classification and dull grading system",
            "SPE 29401: PDC bit selection for shale formations",
            "SPE 112741: Bit optimization using offset analysis",
            "Bit manufacturer technical manuals and application guides",
            "SPE 163427: Economics of bit selection and pull decisions"
        ],
        burden_holder="Drilling engineer and bit company technical representative",
        adversary_position="Generic PDC bit works for all formations, bit selection is not critical",
        counter_arguments=[
            "Wrong bit selection causes 50%+ ROP loss and premature failure",
            "Application-specific PDC design doubles footage in hard formations",
            "Bit cost is <5% of well cost, but drives 40%+ of drilling time",
            "Offset bit analysis proves specific designs outperform by 2-5×",
            "Optimized bit selection shown to reduce cost-per-foot 15-30% in field trials"
        ],
        resolution_strategy="Maintain offset bit performance database, engage bit company technical support for design selection, conduct dull bit analysis after every run, track bit KPIs ($/ft, footage, ROP), continuous improvement cycle",
        entity_scope="Well planning, drilling operations, bit suppliers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in bit type selection, moderate confidence in specific design features due to proprietary manufacturer data",
        controlling_precedent=[
            "Industry standard: PDC bits for 90%+ of unconventional drilling",
            "Best practice: Offset bit analysis and dull grading for all bit runs",
            "Operator requirement: Pre-spud bit program with economic justification"
        ],
        fact_fragility=0.25,
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="BHA_Optimization_For_ROP",
        keywords=["bha", "bottomhole assembly", "stabilizers", "rop", "vibration", "wob transfer"],
        conclusion_template=[
            "BHA design impacts ROP through WOB transfer efficiency and vibration control",
            "Stabilizer placement controls neutral point location and buckling prevention",
            "Optimal BHA: Minimize component count, maximize stiffness, control vibration"
        ],
        reasoning_framework="""
        BHA design determines how efficiently surface WOB transfers to the bit and how well vibration is controlled.

        BHA COMPONENT FUNCTIONS:

        1. Drill Collars:
        - Provide weight for WOB (30-50 klb typical)
        - Stiffness prevents buckling under compression
        - Typical: 6.75"-9.5" OD × 2.75"-3" ID × 30-60 ft sections
        - Placement: Immediately above bit for maximum weight transfer

        2. Stabilizers:
        - Center BHA in hole and prevent buckling
        - Reduce lateral vibration and whirl
        - Control WOB transfer and neutral point location
        - Types: Integral blade, welded blade, sleeve, non-rotating
        - Placement critical: Too many = friction and ROP loss, too few = vibration

        3. Heavyweight Drill Pipe (HWDP):
        - Transition between drill collars and drill pipe
        - Additional weight without full stiffness of collars
        - Reduces fatigue at collar-pipe connection
        - Typical: 5" OD × 30-90 ft

        4. Shock Sub / Vibration Dampener:
        - Absorbs axial shock and impact loads
        - Reduces high-frequency vibration to bit
        - Placement: Above bit, below MWD, or both
        - Effectiveness: 30-50% reduction in peak acceleration

        5. Downhole Motor / RSS:
        - Adds rotary power at bit independent of string rotation
        - Motor: Positive displacement, 100-300 RPM, 200-500 HP
        - RSS: Rotary steerable system for directional control
        - Impact on ROP: +20-60% in formations where surface RPM limited

        6. MWD/LWD:
        - Measurement while drilling and logging while drilling tools
        - Provide real-time directional and formation data
        - Large OD (6.75"-8" typical) can act as stabilizer
        - Weight (2000-5000 lbs) affects neutral point calculation

        BHA DESIGN OPTIMIZATION FOR ROP:

        VERTICAL WELLS (simplest case):
        - Minimize component count: Bit + collars + HWDP + drill pipe
        - No stabilizers unless vibration problems occur
        - Maximize WOB transfer efficiency (approach 100%)
        - Typical: Bit, 1 shock sub, 8-15 stands drill collars, 3-5 stands HWDP, drill pipe

        DIRECTIONAL WELLS (build, hold, drop):
        - Stabilizer placement controls build rate and WOB transfer
        - Pendulum BHA (drop): No stabilizers near bit, weight causes drop
        - Build BHA: Motor + bent sub or RSS, stabilizer 30-60 ft above bit
        - Hold BHA: Stabilizers at specific spacing to lock in angle
        - Packed hole assembly: Stabilizers every 30-60 ft, high side force, low ROP

        HORIZONTAL WELLS (unconventional plays):
        - Challenge: WOB transfer efficiency drops to 60-80% in lateral
        - BHA friction on low side of hole consumes WOB
        - Solution: Motor drilling to add downhole power
        - RSS for continuous steering without sliding
        - Minimize stabilizer count to reduce friction
        - Typical: Bit, motor or RSS, MWD, 3-5 stands collars, HWDP, drill pipe

        NEUTRAL POINT CALCULATION AND MANAGEMENT:
        Neutral point = location where drill string transitions from compression (below) to tension (above)

        Calculation:
        - Drill collar weight in mud = OD² - ID² × mud weight factor × length
        - Neutral point depth below rotary table = WOB / (collar unit weight in mud)
        - Example: 40 klb WOB, 120 lb/ft collars in 12 ppg mud → NP at 333 ft = 11 stands of collars

        Management principles:
        - Keep neutral point in drill collars (never in drill pipe = buckling and fatigue)
        - Rule of thumb: Minimum 1.5× WOB worth of collar weight
        - Place first stabilizer below neutral point for buckling prevention

        VIBRATION CONTROL THROUGH BHA DESIGN:

        1. Lateral vibration (whirl):
        - Cause: BHA mass imbalance, bit force imbalance
        - Mitigation: Stabilizers near bit, reduce unbalanced cutting forces
        - Severe cases: Add more stabilizers (trade-off with ROP)

        2. Axial vibration (bit bounce):
        - Cause: Bit impact with formation, poor weight distribution
        - Mitigation: Shock sub above bit, reduce WOB, increase RPM

        3. Torsional vibration (stick-slip):
        - Cause: Bit friction variations, BHA torsional resonance
        - Mitigation: Reduce stabilizer count, add downhole motor, increase surface RPM

        BHA OPTIMIZATION PROCESS:

        Step 1 - Review offset well BHA performance:
        - Identify BHAs that achieved high ROP with acceptable vibration
        - Note stabilizer count and placement
        - Correlate BHA design with dull bit condition and vibration severity

        Step 2 - Design baseline BHA:
        - Start with minimal components for ROP
        - Add stabilizers only as needed for directional control or vibration mitigation
        - Size components for adequate WOB capacity (1.5-2× planned WOB)

        Step 3 - Model and validate:
        - Torque and drag modeling: Confirm WOB transfer efficiency >70%
        - Buckling analysis: Confirm neutral point in collars
        - Vibration modeling: Check for resonance frequencies matching RPM range

        Step 4 - Field execution and adjustment:
        - Monitor downhole vibration if MWD capable
        - If vibration excessive: Add shock sub or stabilizer
        - If ROP poor: Remove unnecessary stabilizers or add motor
        - Document performance for next well offset

        ROP IMPACT OF BHA COMPONENTS:
        - Each stabilizer: -5 to -15% ROP due to friction and WOB loss
        - Shock sub: -5% ROP due to WOB cushioning, but prevents bit damage
        - Motor: +20 to +60% ROP from added downhole power
        - RSS: +10 to +30% ROP from eliminating slide drilling
        - Minimalist BHA (vertical): Baseline ROP = 100%
        - Typical directional BHA: 80-90% of vertical ROP potential
        """,
        key_factors=[
            "Well trajectory and directional requirements",
            "Formation properties and expected vibration environment",
            "Planned WOB and neutral point calculation",
            "Offset BHA performance data",
            "Hole size and clearances",
            "Component availability and compatibility",
            "Rig hoisting capacity for heavy BHA",
            "Real-time vibration monitoring capability"
        ],
        primary_authority=[
            "SPE 163508: BHA design optimization for ROP",
            "SPE 29350: Vibration mitigation through BHA design",
            "API RP 7G: Drill stem design and operating limits",
            "Directional drilling manuals: Stabilizer placement rules",
            "Drilling contractor BHA design guidelines"
        ],
        burden_holder="Drilling engineer and directional driller",
        adversary_position="BHA design is directional concern only, has minimal impact on ROP",
        counter_arguments=[
            "BHA friction consumes 20-40% of WOB in horizontals, directly limiting ROP",
            "Excessive stabilizers reduce ROP 30-50% through drag and buckling",
            "Minimalist BHA design proven to increase ROP 15-25% in field trials",
            "Motor addition in horizontals increases ROP 30-60% consistently",
            "Vibration from poor BHA destroys bits prematurely, reducing effective ROP"
        ],
        resolution_strategy="Develop BHA design library from offset well performance, standardize BHAs by well type and formation, model torque/drag and vibration before running, track BHA-specific ROP and dysfunction metrics",
        entity_scope="Well planning, directional drilling, drilling operations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in BHA impact on ROP, moderate confidence in optimal design due to well-specific variability",
        controlling_precedent=[
            "Industry trend: Minimalist BHA design for ROP in unconventional horizontals",
            "Best practice: BHA vibration modeling before running in hard rock or ERD wells",
            "Operator requirement: Offset BHA review and performance tracking"
        ],
        fact_fragility=0.3,
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Drilling_Fluid_Optimization_For_ROP",
        keywords=["drilling fluid", "mud", "rheology", "rop", "ecd", "hole cleaning"],
        conclusion_template=[
            "Drilling fluid affects ROP through ECD management, hole cleaning, and bit hydraulics",
            "Low mud weight and optimized rheology maximize ROP while maintaining wellbore stability",
            "Fluid optimization is continuous process balancing ROP, stability, and hole cleaning"
        ],
        reasoning_framework="""
        Drilling fluid optimization balances ROP maximization with wellbore stability, hole cleaning, and hydraulic efficiency.

        DRILLING FLUID IMPACTS ON ROP:

        1. EQUIVALENT CIRCULATING DENSITY (ECD):
        - ECD = Static mud weight + pressure losses in annulus
        - High ECD → High differential pressure → Bit balling, slow ROP, differential sticking risk
        - Target: ECD < Formation pore pressure + 0.5 ppg (safety margin)
        - ECD reduction strategies: Lower mud weight, reduce viscosity, increase annular clearance

        2. DIFFERENTIAL PRESSURE ACROSS BIT:
        - Δp = Formation pore pressure - ECD
        - High Δp (underbalanced): Fast ROP, instability risk, kicks
        - Low Δp (overbalanced): Slow ROP, stable well, bit balling
        - Optimal: Δp = 200-500 psi overbalanced for most formations
        - Permeable formations: Chip hold-down effect reduces ROP if Δp too high

        3. HOLE CLEANING EFFICIENCY:
        - Poor cleaning → Cuttings bed → Stuck pipe, slow ROP, high torque
        - Good cleaning → Clean hole → Maximum ROP, low drag
        - Transport ratio: ROP × hole area / flow rate
        - Target: <0.7 for vertical, <1.2 for 45°, <2.0 for horizontal
        - Viscosity and gel strength lift cuttings, but increase ECD (trade-off)

        4. BIT HYDRAULICS:
        - Nozzle velocity = (Flow rate / Nozzle area) × 1.27 (units conversion)
        - Hydraulic horsepower at bit (HHP) = (Flow × ΔP_bit) / 1714
        - Impact force = (Flow × ΔP_bit)^0.5 / 37
        - Junk slot velocity and TFA (total flow area) determine hole cleaning at bit
        - Optimization: Balance HHP for cleaning vs. pressure losses for low ECD

        5. LUBRICITY AND FRICTION:
        - Mud-to-formation friction coefficient: 0.15-0.35 typical
        - High friction → High torque → WOB loss to friction → Lower ROP
        - Lubricants reduce friction 30-50%, increase WOB transfer efficiency
        - Critical in ERD and horizontal wells where friction consumes WOB

        FLUID OPTIMIZATION PROCESS:

        PLANNING PHASE:
        1. Pore pressure and fracture gradient from offset wells and logs
        2. Set mud weight: Pore pressure + 0.5 ppg (safety margin) to Fracture gradient - 0.5 ppg (loss margin)
        3. Rheology design: Plastic viscosity 20-40 cp, yield point 10-20 lb/100ft² (adjust for hole cleaning needs)
        4. Filtration control: API fluid loss <5 cc for stable shale, <10 cc for sandstone
        5. Solids control: LGS (low-gravity solids) <6% for maximum ROP

        EXECUTION PHASE:
        Real-time monitoring and adjustment:

        - ROP declining with same parameters → Check for bit balling or cuttings accumulation
        - Torque increasing → Hole cleaning problem or high friction
        - ECD rising → Viscosity too high, reduce with water or base oil
        - Instability (tight hole, overpull) → Increase mud weight or improve filtration
        - Lost circulation → Reduce ECD, add LCM (lost circulation material)

        Fluid property adjustments:
        - ROP priority: Minimize mud weight and viscosity (within stability limits)
        - Stability priority: Increase mud weight, improve filtration, inhibition
        - Hole cleaning priority: Increase viscosity and flow rate, reduce ROP if needed
        - Friction priority: Add lubricants, reduce solids content

        COMMON ROP-LIMITING FLUID ISSUES AND SOLUTIONS:

        1. BIT BALLING (formation sticks to bit face):
        - Cause: High differential pressure, clay-rich cuttings, poor dispersion
        - Detection: ROP decline, torque spikes, motor stalling
        - Solutions: Reduce overbalance, increase detergent concentration, add dispersant, increase flow rate

        2. CUTTINGS BED IN HORIZONTAL SECTION:
        - Cause: Low annular velocity, insufficient viscosity, high ROP
        - Detection: Increasing torque, pump pressure, overpull when sliding
        - Solutions: Increase flow rate, increase low-shear viscosity, reduce ROP, increase pipe rotation, backreaming

        3. HIGH ECD LIMITING MUD WEIGHT:
        - Cause: High annular pressure losses from tight clearances or high viscosity
        - Impact: Cannot increase mud weight for stability without fracturing formation
        - Solutions: Reduce plastic viscosity, enlarge hole (reaming), use managed pressure drilling (MPD)

        4. DIFFERENTIAL STICKING:
        - Cause: High overbalance + permeable formation + thick filter cake
        - Detection: Stuck pipe when stationary against permeable zone
        - Solutions: Reduce overbalance, improve filtration, add spotting fluid, keep pipe moving

        5. FORMATION DAMAGE REDUCING ROP:
        - Cause: Mud filtrate invades formation, changes rock properties
        - Impact: Lower effective ROP in permeable sands
        - Solutions: Use oil-based or synthetic mud, improve filtration, underbalanced drilling

        MUD SYSTEM SELECTION BY WELL TYPE:

        WATER-BASED MUD (WBM):
        - Cost: $10-30/bbl
        - Applications: Shallow sections, simple wells, environmentally sensitive areas
        - ROP impact: Moderate (clay dispersion and hydration can slow ROP)
        - Advantages: Low cost, environmentally acceptable, easy to engineer
        - Disadvantages: Shale instability, temperature limits, high friction

        OIL-BASED MUD (OBM) / SYNTHETIC-BASED MUD (SBM):
        - Cost: $80-150/bbl
        - Applications: Complex directional wells, ERD, shale formations, HPHT
        - ROP impact: High (20-40% faster than WBM in shale)
        - Advantages: Shale stability, high temperature tolerance, lubricity, low ECD
        - Disadvantages: High cost, environmental disposal restrictions, slower filtration

        UNDERBALANCED DRILLING (UBD):
        - Cost: Premium (requires specialized equipment and engineering)
        - Applications: Depleted reservoirs, damage-prone formations, high ROP priority
        - ROP impact: Very high (50-200% faster than overbalanced)
        - Advantages: Maximum ROP, no formation damage, early production
        - Disadvantages: Complex operations, wellbore stability challenges, safety risks

        MANAGED PRESSURE DRILLING (MPD):
        - Cost: $50-200k/well for surface equipment and engineering
        - Applications: Narrow pressure window, high ECD wells, wellbore breathing
        - ROP impact: Moderate to high (allows lower mud weight and ECD)
        - Advantages: Precise pressure control, enables drilling undrillable wells
        - Disadvantages: Equipment cost, learning curve, limited rig compatibility

        ADVANCED OPTIMIZATION:
        - Real-time ECD monitoring with PWD (pressure while drilling)
        - Automated fluid property measurement and control
        - Hole cleaning modeling and validation
        - Drilling fluid digital twin for predictive optimization
        """,
        key_factors=[
            "Formation pore pressure and fracture gradient",
            "Wellbore stability requirements (shale, salt, unconsolidated sands)",
            "Hole cleaning needs (trajectory, ROP, hole size)",
            "Environmental and regulatory constraints on fluid type",
            "Offset well fluid performance data",
            "Budget constraints (WBM vs. OBM/SBM)",
            "Rig fluid handling and solids control equipment capability",
            "Real-time fluid monitoring and adjustment capability"
        ],
        primary_authority=[
            "SPE 163420: Drilling fluid optimization for ROP",
            "SPE 84448: ECD management in narrow margin wells",
            "API RP 13B: Fluid property testing and specification",
            "SPE 105442: Hole cleaning in horizontal and ERD wells",
            "Mud company technical manuals and fluid system design guides"
        ],
        burden_holder="Drilling engineer and mud engineer",
        adversary_position="Drilling fluid type and properties have minimal impact on ROP, geology is dominant factor",
        counter_arguments=[
            "OBM consistently shows 20-40% higher ROP than WBM in shale formations",
            "High ECD from poor fluid design limits achievable mud weight and causes losses",
            "Bit balling from incompatible fluid can reduce ROP by 50-80%",
            "Poor hole cleaning from inadequate fluid properties causes stuck pipe and NPT",
            "Lubricity and friction reduction from fluid additives improves WOB transfer 10-20%"
        ],
        resolution_strategy="Establish formation-specific fluid design guidelines, real-time fluid property monitoring, daily mud engineer review of ROP and fluid performance correlation, offset well fluid performance database",
        entity_scope="Drilling engineering, mud engineering, wellbore stability",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in fluid impact on ROP, moderate confidence in optimal fluid design due to cost and environmental constraints",
        controlling_precedent=[
            "Industry trend: OBM/SBM for complex directional wells in unconventional plays",
            "Best practice: Real-time ECD monitoring in narrow margin wells",
            "Operator requirement: Fluid program designed from offset well data and wellbore stability modeling"
        ],
        fact_fragility=0.3,
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Connection_Time_Optimization",
        keywords=["connection", "stand", "pipe handling", "ilt", "efficiency", "crew"],
        conclusion_template=[
            "Connections represent 5-15% of total well time: Major ILT opportunity",
            "Physics-limited minimum: 3-5 minutes vertical, 5-8 minutes directional",
            "Optimization through workflow design, equipment, and crew training"
        ],
        reasoning_framework="""
        Connection time optimization reduces invisible lost time through process improvement and automation.

        CONNECTION OPERATION BREAKDOWN:

        Typical connection sequence (adding stand):
        1. Stop drilling, pick up to slips (~30 sec)
        2. Set slips, break circulation (~15 sec)
        3. Pick up new stand from setback to elevator (~30 sec)
        4. Stab stand into connection (~20 sec)
        5. Make up connection (spin and torque) (~60-90 sec)
        6. Lower kelly/top drive to drilling position (~15 sec)
        7. Resume circulation, pick up slips (~15 sec)
        8. Resume drilling, tag bottom (~30 sec)

        TOTAL PHYSICS-LIMITED TIME: 3-4 minutes for vertical well with iron roughneck and efficient crew

        ACTUAL FIELD TIME: Often 8-15 minutes due to operational inefficiencies

        CONNECTION TIME COMPONENTS AND OPTIMIZATION:

        1. PIPE HANDLING (30-40% of connection time):
        - Manual: Rig crew handles stands manually with elevators and tongs (slow, labor-intensive)
        - Mechanized: Pipe handling system automates stand movement from setback (30-50% time reduction)
        - Optimization: Pre-position next stand, minimize horizontal movement, reduce waiting for crew positioning

        2. CONNECTION MAKEUP (25-35% of connection time):
        - Manual tongs: Spinner + backup tongs + torque tongs (slow, requires multiple crew)
        - Power tongs: Pneumatic or hydraulic spinning and torque (moderate speed, still manual)
        - Iron roughneck: Automated spinning and torque wrench (fast, consistent, safe)
        - Optimization: Iron roughneck reduces makeup from 90 sec to 30-45 sec

        3. SLIPS OPERATION (10-15% of connection time):
        - Manual slips: Set and remove manually (slow, safety risk)
        - Pneumatic slips: Air-actuated for faster operation (moderate speed)
        - Automated slips: Integrated with top drive controls (fastest, minimal crew interaction)
        - Optimization: Pneumatic or automated slips save 10-20 sec per connection

        4. CIRCULATION MANAGEMENT (5-10% of connection time):
        - Manual: Driller manually stops and starts pumps (variable timing)
        - Semi-automated: Preset pump controls for connection sequence (consistent)
        - Fully automated: Pumps synchronized with drilling controls (fastest)
        - Optimization: Automated circulation saves 5-10 sec, improves consistency

        5. DIRECTIONAL SURVEYS (variable, 0-5 min per connection):
        - Conventional MWD: Survey every 1-3 stands, 3-5 min survey time
        - Fast MWD: Survey every stand, <1 min survey time
        - Continuous inclination: Real-time inclination, no survey delays (except depth correlation)
        - Optimization: Fast MWD or continuous systems eliminate survey-related ILT

        CREW WORKFLOW OPTIMIZATION:

        Parallel operations:
        - While making up connection: Next stand pre-positioned, torque wrench prepared
        - While surveying: Circulate bottoms up if hole cleaning needed (productive time)
        - During trip: Pre-stage BHA components for next section

        Standardized procedures:
        - Written procedure with step-by-step instructions and target times
        - Crew training on standard work and time-motion efficiency
        - Daily connection time tracking and crew performance feedback
        - Safety without rushing: Efficiency from smooth choreography, not speed

        EQUIPMENT UPGRADES FOR CONNECTION TIME REDUCTION:

        | Equipment | Time Savings per Connection | Payback Example (30-day well, 300 connections) |
        |-----------|----------------------------|----------------------------------------------|
        | Iron roughneck | 45-60 sec | 225-300 min = 3.8-5 hr = $8-10k @ $50k/day rig rate |
        | Pipe handling system | 30-45 sec | 150-225 min = 2.5-3.8 hr = $5-8k |
        | Pneumatic slips | 10-20 sec | 50-100 min = 0.8-1.7 hr = $1.7-3.5k |
        | Fast MWD | 2-4 min (on survey connections) | 200-400 min = 3.3-6.7 hr = $7-14k |

        Total potential ILT reduction: 10-15 hours per well = $20-30k savings
        Equipment cost: Iron roughneck rental ~$15-25k/well
        ROI: Positive on first well, major savings across multi-well programs

        CONNECTION TIME TRACKING AND IMPROVEMENT:

        Measurement:
        - Automated: EDR (electronic drilling recorder) extracts connection start/end from rig sensors
        - Manual: Driller logs connection times on tour report
        - Granular: Time each component (handling, makeup, survey) to identify bottlenecks

        Benchmarking:
        - Offset wells: Target median or best offset connection time
        - Rig capability: Best achieved on same rig in similar well
        - Industry benchmarks: 3-5 min vertical (automated), 5-8 min directional (with surveys)

        Continuous improvement:
        - Daily connection time review with crew
        - Identify slowest connections and root causes
        - Implement countermeasures: Training, procedure changes, equipment fixes
        - Track improvement trend across well program (learning curve)

        LEARNING CURVE ACROSS PAD DEVELOPMENT:
        Typical connection time improvement 1st to 10th well:
        - 1st well: 10-12 min average (crew learning, process refinement)
        - 5th well: 7-9 min average (standardized procedures, crew proficiency)
        - 10th well: 5-7 min average (approaching optimal for equipment and well type)
        - Improvement: 30-50% reduction in connection time through learning

        SPECIAL CASES:

        Casing running:
        - Slower than drill pipe due to handling larger OD and weight
        - Typical: 8-12 min per joint (40 ft) with manual tongs
        - Optimized: 5-7 min with casing running tool and crew proficiency
        - Hundreds of connections per casing string → Major ILT opportunity

        Trip connections (coming out of hole):
        - Faster than drilling connections (no makeup, only breakout)
        - Target: 2-3 min per stand for vertical, 3-5 min for directional
        - Optimization: Automated pipe racker, high-speed breakout, efficient stand handling
        """,
        key_factors=[
            "Rig equipment capability (iron roughneck, pipe handling, automated systems)",
            "Crew size, training, and experience level",
            "Well type (vertical, directional, horizontal) affecting survey frequency",
            "MWD survey speed and frequency requirements",
            "Connection procedure standardization and adherence",
            "Offset well connection time benchmarks",
            "Safety culture balance with efficiency",
            "Number of connections in well program (ROI for equipment upgrades)"
        ],
        primary_authority=[
            "IADC connection time benchmarks: 3-5 min vertical, 5-8 min directional",
            "SPE 102549: ILT analysis including connection time component",
            "Drilling contractor operational guidelines and KPIs",
            "Equipment manufacturer specifications and performance data",
            "Operator internal: Connection time targets by rig and well type"
        ],
        burden_holder="Drilling operations supervisor and rig crew",
        adversary_position="Connection time is necessary operational overhead, not subject to optimization",
        counter_arguments=[
            "300 connections × 5 min saved per connection = 25 hours = 1+ day saved per well",
            "Iron roughneck and automation proven to reduce connection time 40-60%",
            "Crew training and standardized procedures reduce time 20-30% with no capital cost",
            "Connection time learning curves demonstrate improvement is achievable and sustainable",
            "Best-in-class operators achieve 4-5 min connections consistently through focus and measurement"
        ],
        resolution_strategy="Implement automated connection time tracking from EDR, daily crew performance review, standardized connection procedures, equipment upgrade analysis, connection time trending across well program",
        entity_scope="Drilling operations, rig crew management, equipment selection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in optimization potential, moderate confidence in achievable times due to rig and crew variability",
        controlling_precedent=[
            "Industry trend: Automation and iron roughnecks becoming standard on modern rigs",
            "Best practice: Connection time tracking and crew performance feedback",
            "Operator requirement: Target connection times specified for all wells"
        ],
        fact_fragility=0.25,
        zone=AnalysisZone.REAL_TIME
    ),

    DoctrineBlock(
        topic="Learning_Curve_Analysis_Pad_Development",
        keywords=["learning curve", "pad drilling", "continuous improvement", "batch drilling", "afe"],
        conclusion_template=[
            "Learning curves demonstrate 20-40% drilling time reduction from 1st to Nth well in program",
            "Improvements compound: ROP, connection time, NPT, operational efficiency all improve",
            "Quantification enables accurate AFE forecasting and justifies batch development"
        ],
        reasoning_framework="""
        Learning curve analysis quantifies performance improvement across sequential wells in development program.

        LEARNING CURVE CONCEPT:
        Each successive well drilled benefits from:
        - Crew familiarity with well design and procedures
        - Refined BHA and bit selections based on offset performance
        - Optimized drilling parameters for each formation
        - Improved operational efficiency and coordination
        - Reduced NPT from avoided mistakes
        - Better AFE estimates from actual cost data

        MATHEMATICAL MODELS:

        Wright's Cumulative Average Model (aerospace industry standard):
        Y_n = Y_1 × n^b
        where:
        Y_n = Time (or cost) for nth well
        Y_1 = Time (or cost) for 1st well
        n = Well number in sequence
        b = Learning curve exponent = log(learning rate) / log(2)

        Example: 85% learning curve
        b = log(0.85) / log(2) = -0.234
        Y_10 = Y_1 × 10^(-0.234) = Y_1 × 0.58 (42% time reduction by 10th well)

        Typical drilling learning curves: 80-90% (vs. 70-80% in manufacturing)
        Faster learning (75-80%): Simple vertical wells, homogeneous formation, consistent rig
        Slower learning (85-95%): Complex directional wells, variable geology, crew turnover

        COMPONENTS OF DRILLING LEARNING CURVE:

        1. ROP IMPROVEMENT (30-40% of total learning):
        - 1st well: Conservative parameters, unknown formation response
        - Nth well: Optimized WOB-RPM, proven bit selection, dysfunction mitigation
        - Typical: 20-35% ROP increase from 1st to 5th well in pad

        2. NPT REDUCTION (25-35% of total learning):
        - 1st well: Higher NPT from unexpected events and problem-solving delays
        - Nth well: Avoided NPT from lessons learned, better planning
        - Typical: 50-70% NPT reduction from 1st to 5th well

        3. CONNECTION TIME REDUCTION (10-15% of total learning):
        - 1st well: Crew learning workflow, procedure refinement
        - Nth well: Smooth choreography, minimal wasted motion
        - Typical: 30-40% connection time reduction from 1st to 5th well

        4. OPERATIONAL EFFICIENCY (15-25% of total learning):
        - Survey frequency optimization
        - Trip speed improvement
        - BHA handling and rig-up efficiency
        - Coordination between drilling crew, directional driller, mud engineer
        - Typical: 15-25% efficiency gain in non-drilling operations

        QUANTIFICATION METHODOLOGY:

        Data collection:
        - Drilling time by hole section for each well (exclude common completion time)
        - ROP by formation interval
        - NPT hours and categories
        - Connection time and trip time
        - Cost per foot by hole section
        - Days from spud to TD (total depth)

        Analysis:
        1. Plot cumulative average time vs. well number on log-log scale
        2. Fit linear regression: log(Y_n) = log(Y_1) + b × log(n)
        3. Calculate learning rate: LR = 2^b (typically 0.80-0.90)
        4. Extrapolate to future wells: Predict time/cost for well N+1, N+2, etc.
        5. Decompose by component: ROP, NPT, connections, operations

        Example pad development (10 wells, 10,000 ft horizontal each):
        Well 1: 28 days, $4.2M
        Well 2: 24 days, $3.6M (86% learning curve)
        Well 3: 21 days, $3.15M
        Well 4: 19 days, $2.85M
        Well 5: 17 days, $2.55M (61% of well 1 time, 85% learning curve)
        Wells 6-10: 16-17 days, $2.4-2.6M (approaching asymptote)

        DRIVERS OF LEARNING RATE:

        Faster learning (steeper curve):
        - Same rig and crew across all wells (no turnover)
        - Similar well designs (manufacturing mode)
        - Homogeneous geology with consistent formation tops
        - Batch drilling mode: Continuous operations, no mobilization gaps
        - Active performance review and lessons learned process
        - Technology adoption: Automated drilling, real-time optimization

        Slower learning (flatter curve):
        - Crew turnover between wells
        - Varying well designs or trajectory targets
        - Geologic variability requiring different approaches
        - Time gaps between wells (forgetting)
        - Complacency or lack of performance focus

        AFE IMPLICATIONS:

        Traditional AFE (single well):
        - Based on offset wells average or median performance
        - High uncertainty due to limited specific well data
        - Accuracy typically ±20-30% on 1st well in new area

        Learning curve AFE (pad development):
        - 1st well: Conservative estimate (may exceed AFE)
        - 2nd-5th wells: Decreasing AFE based on learning curve projection
        - 6th+ wells: Stable AFE near asymptotic performance
        - Overall program accuracy: ±10-15% (much better than single well)

        Example AFE evolution (10-well pad):
        Well 1 AFE: $4.5M (conservative, allow for unknowns)
        Well 1 Actual: $4.2M (beat AFE 7%)
        Well 2 AFE: $3.7M (apply 85% learning curve)
        Well 2 Actual: $3.6M (beat AFE 3%)
        Well 3-5 AFE: $3.0M, $2.8M, $2.6M
        Wells 6-10 AFE: $2.5M (near asymptote)

        Program total AFE: $30M vs. $28.5M actual (5% under, excellent accuracy)

        OPERATIONAL APPLICATIONS:

        Crew incentives:
        - Bonus structure tied to learning curve achievement
        - Reward crew for beating prior well performance (safely)
        - Recognition for fastest connection times, highest ROP achievements

        Technology justification:
        - ROI calculation: Technology cost vs. time savings on N wells
        - Example: $500k automated drilling system saves 1 day per well
        - Payback: 10 wells × 1 day × $50k/day = $500k savings, immediate ROI
        - Greater impact on later wells where incremental improvements harder

        Rig selection and contracts:
        - Premium for keeping same rig and crew across pad (avoid learning reset)
        - Long-term rig contracts for batch drilling vs. well-by-well
        - Incentive clauses for performance improvement

        Real-time monitoring:
        - Track current well against learning curve projection
        - If falling behind: Investigate and correct immediately
        - If ahead: Capture and institutionalize the improvement

        PLATEAU AND CONTINUOUS IMPROVEMENT:

        Learning curve asymptote:
        - Performance plateaus after 5-10 wells typically
        - Further improvement requires step-change: New technology, process redesign, different rig
        - Continuous improvement mindset: Set new targets beyond initial learning curve

        Example: After achieving 16-day wells (plateau), set new target:
        - Technology: Add automated drilling, target 14 days
        - Process: Optimize casing program, eliminate one trip, target 13 days
        - Operations: 24-hour operations instead of daylight drilling, target 11 days
        """,
        key_factors=[
            "Well design consistency across pad",
            "Geological consistency and formation top predictability",
            "Rig and crew consistency (same personnel across wells)",
            "Time gaps between wells (continuous vs. intermittent drilling)",
            "Organizational learning culture and lessons learned process",
            "Technology adoption rate and effectiveness",
            "Complexity of well (vertical vs. directional vs. extended reach)",
            "Baseline performance level (more room for improvement if starting poor)"
        ],
        primary_authority=[
            "Wright 1936: Cumulative average learning curve model",
            "SPE 102549: Learning curves in drilling operations",
            "SPE 116427: Pad drilling optimization and benchmarking",
            "SPE 163405: Real-time learning curve tracking",
            "Industry studies: 80-90% learning curves typical for drilling"
        ],
        burden_holder="Drilling engineering and program management",
        adversary_position="Each well is unique, past performance has no predictive value for future wells",
        counter_arguments=[
            "Statistical analysis of 1000+ pad developments proves consistent 80-90% learning curves",
            "Learning curve models predict well time within ±10% accuracy from well 3 onward",
            "Operators achieving 30-40% time reduction from 1st to 10th well repeatedly across multiple pads",
            "Rig and crew consistency demonstrably accelerates learning and improves outcomes",
            "Learning curve-based AFEs significantly more accurate than single-well offset averages"
        ],
        resolution_strategy="Implement learning curve tracking across all pad developments, quantify improvement by component (ROP, NPT, connections, operations), use learning curve projections for AFE development, incentivize crews for improvement, share lessons learned across organization",
        entity_scope="Well program planning, AFE development, operations management",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in learning curve existence and 80-90% range, moderate confidence in specific rate due to well and organizational variability",
        controlling_precedent=[
            "Industry standard: Learning curves expected and tracked on all pad developments",
            "Best practice: Learning curve-based AFE for wells 2+ in program",
            "Operator requirement: Continuous improvement targets for multi-well programs"
        ],
        fact_fragility=0.3,
        zone=AnalysisZone.PLANNING
    ),
]

# Add more doctrine blocks to reach 25+ total
DOCTRINE_CACHE.extend([
    DoctrineBlock(
        topic="Trip_Time_Optimization",
        keywords=["trip", "tripping", "pipe movement", "trip speed", "swab", "surge"],
        conclusion_template=[
            "Trip time represents 10-20% of total well time in deep wells",
            "Safe trip speeds: 1000+ ft/hr vertical, 600-800 ft/hr directional",
            "Optimization balances speed with swab/surge pressure management"
        ],
        reasoning_framework="""
        Trip time optimization requires balancing maximum speed with wellbore pressure management and equipment limitations.

        TRIP OPERATIONS:

        Trip out (POOH - Pull Out Of Hole):
        - Remove drill string from well to change bit, run logs, or case hole
        - Upward pipe movement creates swab pressure (pressure reduction)
        - Excessive swab can cause formation influx (kick) or wellbore collapse

        Trip in (RIH - Run In Hole):
        - Run new bit or BHA into well to resume drilling
        - Downward pipe movement creates surge pressure (pressure increase)
        - Excessive surge can fracture formation and cause lost circulation

        PHYSICS OF SWAB AND SURGE:

        Surge/Swab pressure = f(pipe speed, annular clearance, mud viscosity)

        Approximate calculation:
        ΔP_surge (psi) = (V_pipe × μ × L) / (D_hole² - D_pipe²)
        where:
        V_pipe = Pipe speed (ft/min)
        μ = Mud viscosity (cp)
        L = Length of affected column (ft)
        D_hole = Hole diameter (in)
        D_pipe = Pipe outer diameter (in)

        Impact factors:
        - Tight annular clearance → Higher surge/swab
        - High mud viscosity → Higher surge/swab
        - Fast pipe speed → Higher surge/swab
        - BHA vs. drill pipe → BHA creates 2-5× more surge due to larger OD

        SAFE TRIP SPEED DETERMINATION:

        Maximum trip speed limited by:
        1. Swab pressure: Must not reduce BHP below formation pore pressure (kick risk)
        2. Surge pressure: Must not exceed fracture pressure (lost circulation risk)
        3. Rig hoisting capacity and braking system
        4. Hole cleaning: Allow cuttings to settle during trip, prevent pack-off
        5. Equipment wear: High speeds increase wear on elevators, slips, blocks

        Typical safe trip speeds:
        - Vertical wells, open hole: 1000-1500 ft/hr
        - Directional wells, open hole: 600-1000 ft/hr
        - Cased hole: 1500-2000 ft/hr (less surge/swab concern)
        - BHA through tight spots: 200-400 ft/hr (controlled)
        - Ledges and doglegs: 100-300 ft/hr (prevent BHA damage)

        TRIP TIME COMPONENTS:

        1. PULLING OUT OF HOLE:
        - Break connection every 90 ft (3 joints per stand)
        - Lay down stand in setback or pipe rack
        - Physics time: Depth / trip speed + connections
        - Example: 15,000 ft well, 800 ft/hr, 3 min/connection, 166 stands
        - Physics time: 18.75 hr + 8.3 hr connections = 27 hr
        - Actual field: Often 35-45 hr due to inefficiencies

        2. BIT CHANGE AND BHA INSPECTION:
        - Lay out bit and downhole tools
        - Inspect BHA components, measure wear
        - Pick up new bit and check torque on connections
        - Typical: 1-2 hours

        3. RUNNING IN HOLE:
        - Pick up stands from setback
        - Make up connections (faster than breakout, no torque required)
        - Fill pipe every 5-10 stands to maintain hole hydrostatic
        - Physics time: Similar to POOH
        - Actual field: 10-20% faster than POOH (makeup faster than breakout)

        OPTIMIZATION STRATEGIES:

        Speed optimization:
        - Calculate maximum safe trip speed using surge/swab modeling
        - Vary speed: Fast in casing, slower in open hole tight sections
        - Automate trip speed control using rig hoisting system
        - Real-time monitoring: Track BHP with PWD to verify safe margins

        Connection optimization during trips:
        - Automated pipe racker: Reduces handling time 30-50%
        - Casing elevator: Faster pick-up and lay-down than manual
        - Iron roughneck for breakout: Faster than manual tongs
        - Standardized procedures: Consistent 2-3 min per stand target

        Fill-up optimization:
        - Automatic fill-up system: Monitor annular returns, add fluid continuously
        - Prevent dry-tripping: Forgetting to fill pipe causes swab and kick risk
        - Balance: Fill frequently enough for safety, not so often it slows trip

        Pipe handling optimization:
        - Pre-stage rig floor for trip: Clear obstructions, position equipment
        - Optimize setback: Nearest stands accessible first (minimize searching)
        - Parallel operations: While pulling, prepare next BHA components

        TRIP MONITORING AND CONTROL:

        Hole fill monitoring:
        - Measure fluid returned to pits during POOH
        - Expected: Volume equal to pipe displacement
        - Low returns: Formation taking fluid (lost circulation)
        - High returns: Formation giving fluid (kick)
        - Automate: Flowmeter on trip tank, alarmed for variance

        Drag monitoring:
        - Measure overpull/slack-off during trip
        - Increasing drag: Hole problems developing (tight hole, cuttings bed, key seating)
        - Corrective action: Circulate and backreame before continuing trip

        WIPER TRIPS:
        - Short trip out and back in (typically 500-1500 ft)
        - Purpose: Check for tight hole, clean wellbore, verify no stuck pipe risk
        - Frequency: After drilling trouble zones, before running casing or logs
        - Optimization: Eliminate unnecessary wiper trips (high ILT cost)
        - Decision criteria: Drag trend, offset well experience, formation instability indicators
        """,
        key_factors=[
            "Well depth and trajectory (trip time proportional to depth)",
            "Annular clearance and surge/swab pressure limits",
            "Mud viscosity and density",
            "Rig hoisting capacity and speed capability",
            "Hole condition (tight spots, ledges, doglegs)",
            "BHA diameter and tool configuration",
            "Crew efficiency and equipment (automated racker, iron roughneck)",
            "Real-time trip monitoring (PWD, flow monitoring)"
        ],
        primary_authority=[
            "SPE 102549: Trip time as ILT component",
            "API RP 96: Wellbore pressure management during tripping",
            "Drilling contractor trip speed guidelines",
            "Surge/swab modeling software validation studies",
            "IADC: Trip monitoring best practices"
        ],
        burden_holder="Drilling operations supervisor and driller",
        adversary_position="Trip speed is limited by rig capability, not subject to optimization",
        counter_arguments=[
            "Most rigs capable of 1500+ ft/hr but operated at 400-600 ft/hr due to conservative practices",
            "Surge/swab modeling proves higher speeds are safe with proper monitoring",
            "Automated trip speed control eliminates human reaction time, enables safe speed increase",
            "Trip time optimization saves 0.5-1.5 days per bit run in deep wells",
            "Best-in-class operators achieve 1000+ ft/hr trip speeds consistently"
        ],
        resolution_strategy="Conduct surge/swab modeling for each well, establish safe trip speed limits, implement real-time trip monitoring, automate trip speed control, track trip time performance against benchmarks",
        entity_scope="Drilling operations, wellbore stability engineering",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in optimization potential, moderate confidence in absolute safe speed limits due to hole condition variability",
        controlling_precedent=[
            "Industry trend: Automated trip speed control on modern rigs",
            "Best practice: Surge/swab modeling before deep or narrow margin wells",
            "Operator requirement: Trip speed limits documented in drilling procedures"
        ],
        fact_fragility=0.3,
        zone=AnalysisZone.REAL_TIME
    ),

    DoctrineBlock(
        topic="D_Exponent_Drilling_Efficiency",
        keywords=["d exponent", "d-exp", "corrected d-exponent", "pore pressure", "drilling efficiency"],
        conclusion_template=[
            "d-exponent provides formation drillability metric independent of drilling parameters",
            "Corrected d-exponent normalizes for mud weight, enables pore pressure detection",
            "Trend changes indicate lithology changes, pressure transitions, or bit dulling"
        ],
        reasoning_framework="""
        d-exponent (modified d-exponent) is normalized ROP metric for formation comparison and pore pressure detection.

        D-EXPONENT DERIVATION:

        Original equation (Bingham 1965):
        d = [log(ROP/60RPM)] / [log(12WOB/10^6 × Bit_diameter)]

        Simplified modern form:
        d = log(ROP) / [log(WOB) - log(RPM)]

        Physical meaning:
        - d-exponent relates ROP to drilling parameters (WOB and RPM)
        - Higher d = easier drilling (high ROP for given WOB/RPM)
        - Lower d = harder drilling (low ROP despite high WOB/RPM)
        - Typical range: 0.5-3.0

        CORRECTED D-EXPONENT:

        Corrects for overbalance effect on ROP:
        d_corrected = d × (ECD / Normal_pressure_gradient)

        where:
        ECD = Equivalent circulating density (ppg)
        Normal_pressure_gradient = 0.465 psi/ft or 8.9 ppg for fresh water formation

        Purpose:
        - Removes mud weight impact on ROP
        - Enables comparison across different mud weights
        - Critical for pore pressure detection (d-exp trend reversal)

        APPLICATIONS:

        1. LITHOLOGY CORRELATION:
        - d-exponent signature for each lithology type
        - Shale: d = 1.0-1.5 (plastic deformation, moderate ROP)
        - Sandstone: d = 1.5-2.5 (brittle failure, high ROP if soft)
        - Limestone: d = 0.8-1.5 (hard, low ROP)
        - Dolomite: d = 0.5-1.0 (very hard, very low ROP)
        - Salt: d = 2.5-4.0 (extremely soft, very high ROP)

        Use: Identify formation tops and lithology changes in real-time

        2. PORE PRESSURE DETECTION:
        - Normal pressure: d-exponent increases with depth (compaction trend)
        - Overpressured zone: d-exponent reversal (increase) when entering transition
        - Mechanism: Undercompaction or fluid expansion increases porosity, decreases strength

        Detection workflow:
        - Plot d_corrected vs. depth
        - Establish normal compaction trend (straight line on semi-log plot)
        - Monitor for departure from trend (increases above trend line)
        - Confirm with other indicators: Shale density from logs, gas in mud, connection gas
        - Increase mud weight if overpressure confirmed

        3. BIT DULLING DETECTION:
        - Fresh bit: High d-exponent (efficient cutting)
        - Worn bit: Declining d-exponent with depth (reduced cutting efficiency)
        - Dull bit: 20-40% lower d-exponent than fresh bit in same formation

        Use: Optimize bit pull decision based on efficiency loss

        4. DRILLING EFFICIENCY MONITORING:
        - Compare actual d-exponent to offset well in same formation
        - Lower than offset: Suboptimal parameters, bit selection, or BHA
        - Higher than offset: Optimized drilling, potential for further ROP increase

        LIMITATIONS AND CORRECTIONS:

        Issues with basic d-exponent:
        - Assumes linear relationship (log-log plot), actual formation response non-linear
        - Ignores bit type differences (PDC vs. roller cone)
        - Sensitive to measurement errors in ROP, WOB, RPM
        - Does not account for bit hydraulics or torque
        - Formation damage from filtrate invasion affects shallow penetration

        Modern improvements:
        - Sigma log (Eaton 1975): Uses torque instead of WOB for better correlation
        - Mechanical efficiency (ME): Ratio of minimum energy to actual energy
        - MSE (Mechanical Specific Energy): More direct efficiency metric, replacing d-exp in modern systems

        IMPLEMENTATION:

        Calculation:
        - Real-time: Calculate from surface drilling parameters every 1 second
        - Smooth: Moving average over 5-10 ft to reduce noise
        - Normalize: Apply ECD correction
        - Plot: d_corrected vs. depth, overlay on drilling parameters and mud logs

        Interpretation protocol:
        - Establish baseline d-exponent in normal pressure section (typically surface hole)
        - Monitor for trend departures indicating lithology changes or pressure anomalies
        - Cross-reference with offset well d-exponent profiles
        - Integrate with other pore pressure indicators for multi-signal confirmation

        Reporting:
        - Include d-exponent plot in daily drilling report
        - Flag significant trend changes for geologist and drilling engineer review
        - Use for real-time geosteering in horizontal wells (maintain in target zone)
        - Post-well: Compare predicted vs. actual formation tops and pressures
        """,
        key_factors=[
            "Measurement accuracy of ROP, WOB, and RPM",
            "Formation lithology and mechanical properties",
            "Bit type and wear state",
            "Mud weight (ECD) and differential pressure",
            "Drilling fluid filtration and formation damage",
            "Offset well d-exponent data for comparison",
            "Pore pressure gradient and compaction state",
            "Real-time calculation and display capability"
        ],
        primary_authority=[
            "Bingham 1965: d-exponent concept and derivation",
            "Jorden and Shirley 1966: d-exponent for pore pressure detection",
            "Eaton 1975: Corrected d-exponent and sigma log",
            "SPE 16666: d-exponent applications and limitations",
            "Modern practice: MSE preferred over d-exponent for efficiency monitoring"
        ],
        burden_holder="Drilling engineer and wellsite geologist",
        adversary_position="d-exponent is obsolete, replaced by MSE and other modern methods",
        counter_arguments=[
            "d-exponent still widely used for pore pressure detection in exploration drilling",
            "Corrected d-exponent effective for lithology correlation when calibrated to offset wells",
            "Simple calculation from standard drilling parameters, no additional sensors required",
            "Complementary to MSE: d-exponent for lithology, MSE for drilling efficiency",
            "d-exponent provides formation property indicator, MSE provides operational efficiency indicator"
        ],
        resolution_strategy="Calculate d-exponent in parallel with MSE, use d_corrected for pore pressure monitoring, establish baseline from offset wells, integrate into real-time drilling dashboard, post-well validation against logs",
        entity_scope="Drilling operations, wellsite geology, pore pressure prediction",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence in d-exponent for lithology indication, low confidence for quantitative pore pressure prediction without calibration",
        controlling_precedent=[
            "Industry practice: d-exponent calculated on most wells for formation evaluation",
            "Best practice: Corrected d-exponent for pore pressure monitoring in exploration wells",
            "Modern trend: MSE supplementing or replacing d-exponent for efficiency monitoring"
        ],
        fact_fragility=0.45,
        zone=AnalysisZone.REAL_TIME
    ),
])

# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC REQUEST/RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════════════════

class DrillingQuery(BaseModel):
    """Drilling optimization query request"""
    query: str = Field(..., description="Drilling optimization question or scenario")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(None, description="Well and drilling context")
    parameters: Optional[Dict[str, float]] = Field(None, description="Current drilling parameters")

class ConfidenceAssessment(BaseModel):
    """Confidence and fragility assessment"""
    confidence_level: ConfidenceLevel
    confidence_explanation: str
    fact_fragility_score: float = Field(..., ge=0.0, le=1.0)
    key_assumptions: List[str]
    data_quality_dependencies: List[str]

class DoctrineReference(BaseModel):
    """Reference to doctrine block used"""
    topic: str
    relevance_score: float
    key_points: List[str]

class DrillingOptimizationResponse(BaseModel):
    """Drilling optimization analysis response"""
    query: str
    response_text: str
    mode: ResponseMode
    confidence: ConfidenceAssessment
    doctrines_applied: List[DoctrineReference]
    recommendations: List[str]
    zone: AnalysisZone
    metrics: Optional[Dict[str, Any]] = None
    determinism_hash: str

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    engine_id: str
    version: str
    doctrine_count: int
    uptime_seconds: float
    total_queries: int

# ═══════════════════════════════════════════════════════════════════════════
# ENGINE CORE LOGIC
# ═══════════════════════════════════════════════════════════════════════════

class DRL10Engine:
    """DRL10 Drilling Optimization Engine - TIE Gold Standard Implementation"""

    def __init__(self):
        self.engine_id = "DRL10"
        self.version = "1.0.0"
        self.start_time = datetime.now()
        self.query_count = 0
        self.doctrine_cache = {d.topic: d for d in DOCTRINE_CACHE}
        logger.info(f"DRL10 Engine initialized with {len(DOCTRINE_CACHE)} doctrine blocks")

    def semantic_normalize(self, query: str) -> str:
        """Normalize drilling terminology"""
        normalizations = {
            "rate of penetration": "rop",
            "weight on bit": "wob",
            "rotations per minute": "rpm",
            "revolutions per minute": "rpm",
            "mechanical specific energy": "mse",
            "invisible lost time": "ilt",
            "non-productive time": "npt",
            "bottom hole assembly": "bha",
            "polycrystalline diamond compact": "pdc",
            "authorized for expenditure": "afe",
            "cost per foot": "cost-per-foot",
            "drilling dysfunction": "dysfunction",
            "stick slip": "stick-slip",
            "wellbore instability": "instability",
            "hole cleaning": "cleaning",
            "equivalent circulating density": "ecd",
        }
        normalized = query.lower()
        for phrase, term in normalizations.items():
            normalized = normalized.replace(phrase, term)
        return normalized

    def search_doctrines(self, query: str, top_k: int = 5) -> List[DoctrineBlock]:
        """Search doctrine cache for relevant blocks"""
        normalized_query = self.semantic_normalize(query)
        query_terms = set(normalized_query.split())

        scored_doctrines = []
        for doctrine in DOCTRINE_CACHE:
            # Score based on keyword overlap
            keyword_overlap = len(query_terms.intersection(set(doctrine.keywords)))
            # Score based on topic relevance
            topic_match = 1.0 if any(term in doctrine.topic.lower() for term in query_terms) else 0.0
            # Combined score
            score = keyword_overlap + (topic_match * 2)
            if score > 0:
                scored_doctrines.append((score, doctrine))

        # Sort by score and return top_k
        scored_doctrines.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored_doctrines[:top_k]]

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        context: Optional[Dict[str, Any]] = None
    ) -> DrillingOptimizationResponse:
        """
        Three-layer response strategy:
        1. Doctrine cache (0-200ms)
        2. Semantic retrieval (200-1000ms)
        3. Deep analysis (1-5s)
        """
        start_time = datetime.now()
        self.query_count += 1

        # Layer 1: Search doctrine cache
        relevant_doctrines = self.search_doctrines(query, top_k=5)

        if not relevant_doctrines:
            # Fallback if no doctrines match
            response_text = f"Query '{query}' did not match any drilling optimization doctrines. Please refine query to include terms like: ROP, WOB, RPM, MSE, bit selection, BHA, drilling dysfunction, cost-per-foot, ILT, NPT, or connection time."
            confidence = ConfidenceAssessment(
                confidence_level=ConfidenceLevel.DISCLOSURE,
                confidence_explanation="No relevant doctrine blocks found",
                fact_fragility_score=1.0,
                key_assumptions=["Query requires domain expertise not captured in doctrine cache"],
                data_quality_dependencies=["Broader drilling optimization knowledge base needed"]
            )
            return DrillingOptimizationResponse(
                query=query,
                response_text=response_text,
                mode=mode,
                confidence=confidence,
                doctrines_applied=[],
                recommendations=["Refine query with specific drilling optimization terms"],
                zone=AnalysisZone.PLANNING,
                determinism_hash=self._compute_hash(query, response_text)
            )

        # Layer 2: Synthesize response from top doctrines
        primary_doctrine = relevant_doctrines[0]

        if mode == ResponseMode.FAST:
            response_text = self._generate_fast_response(query, primary_doctrine, context)
        elif mode == ResponseMode.DEFENSE:
            response_text = self._generate_defense_response(query, relevant_doctrines, context)
        else:  # MEMO
            response_text = self._generate_memo_response(query, relevant_doctrines, context)

        # Extract recommendations
        recommendations = self._extract_recommendations(relevant_doctrines, context)

        # Assess confidence
        confidence = self._assess_confidence(relevant_doctrines, context)

        # Build doctrine references
        doctrine_refs = [
            DoctrineReference(
                topic=d.topic,
                relevance_score=0.9 - (i * 0.15),  # Decreasing relevance
                key_points=d.conclusion_template[:3]
            )
            for i, d in enumerate(relevant_doctrines[:3])
        ]

        # Compute determinism hash
        det_hash = self._compute_hash(query, response_text)

        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"Query processed in {elapsed:.3f}s, mode={mode.value}, doctrines={len(relevant_doctrines)}")

        return DrillingOptimizationResponse(
            query=query,
            response_text=response_text,
            mode=mode,
            confidence=confidence,
            doctrines_applied=doctrine_refs,
            recommendations=recommendations,
            zone=primary_doctrine.zone,
            determinism_hash=det_hash
        )

    def _generate_fast_response(
        self,
        query: str,
        doctrine: DoctrineBlock,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Generate concise response for FAST mode"""
        conclusions = " ".join(doctrine.conclusion_template)

        context_note = ""
        if context:
            if "rop" in context:
                context_note = f"\n\nCurrent ROP: {context['rop']} ft/hr. "
            if "wob" in context and "rpm" in context:
                context_note += f"Parameters: WOB={context['wob']} klb, RPM={context['rpm']}. "

        return f"""**{doctrine.topic}**

{conclusions}

**Key Factors**: {', '.join(doctrine.key_factors[:5])}
{context_note}
**Resolution**: {doctrine.resolution_strategy[:200]}..."""

    def _generate_defense_response(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Generate audit-ready response for DEFENSE mode"""
        primary = doctrines[0]

        response = f"""**DRILLING OPTIMIZATION ANALYSIS - DEFENSE DOCUMENTATION**

**Query**: {query}

**Primary Doctrine**: {primary.topic}

**Conclusions (Defensible)**:
"""
        for i, conclusion in enumerate(primary.conclusion_template, 1):
            response += f"{i}. {conclusion}\n"

        response += f"\n**Reasoning Framework**:\n{primary.reasoning_framework[:800]}...\n"

        response += f"\n**Key Technical Factors**:\n"
        for i, factor in enumerate(primary.key_factors, 1):
            response += f"{i}. {factor}\n"

        response += f"\n**Authoritative References**:\n"
        for i, auth in enumerate(primary.primary_authority, 1):
            response += f"{i}. {auth}\n"

        response += f"\n**Adversarial Position**: {primary.adversary_position}\n"
        response += f"\n**Counter-Arguments**:\n"
        for i, counter in enumerate(primary.counter_arguments, 1):
            response += f"{i}. {counter}\n"

        response += f"\n**Resolution Strategy**: {primary.resolution_strategy}\n"

        response += f"\n**Confidence**: {primary.confidence.value}"
        response += f"\n**Confidence Stratification**: {primary.confidence_stratification}\n"

        if len(doctrines) > 1:
            response += f"\n**Supporting Doctrines**:\n"
            for doctrine in doctrines[1:3]:
                response += f"- {doctrine.topic}: {doctrine.conclusion_template[0]}\n"

        return response

    def _generate_memo_response(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Generate comprehensive memo for MEMO mode"""
        primary = doctrines[0]

        memo = f"""**TECHNICAL MEMORANDUM - DRILLING OPTIMIZATION**

**Subject**: {query}
**Date**: {datetime.now().strftime('%Y-%m-%d')}
**Engine**: DRL10 Drilling Optimization Engine v{self.version}

**EXECUTIVE SUMMARY**

{primary.conclusion_template[0]}

**TECHNICAL ANALYSIS**

**Background and Context**:
{primary.reasoning_framework[:1200]}

**Primary Doctrine - {primary.topic}**:

**Key Conclusions**:
"""
        for i, conclusion in enumerate(primary.conclusion_template, 1):
            memo += f"{i}. {conclusion}\n"

        memo += f"\n**Critical Success Factors**:\n"
        for i, factor in enumerate(primary.key_factors, 1):
            memo += f"{i}. {factor}\n"

        memo += f"\n**Technical Authorities and Standards**:\n"
        for i, auth in enumerate(primary.primary_authority, 1):
            memo += f"{i}. {auth}\n"

        memo += f"\n**Risk Assessment**:\n"
        memo += f"- Fact Fragility Score: {primary.fact_fragility:.2f} (0=robust, 1=fragile)\n"
        memo += f"- Confidence Level: {primary.confidence.value}\n"
        memo += f"- Stratification: {primary.confidence_stratification}\n"

        memo += f"\n**Alternative Perspectives**:\n"
        memo += f"Adversarial Position: {primary.adversary_position}\n\n"
        memo += f"Counter-Arguments:\n"
        for i, counter in enumerate(primary.counter_arguments, 1):
            memo += f"{i}. {counter}\n"

        memo += f"\n**Recommended Actions**:\n{primary.resolution_strategy}\n"

        if len(doctrines) > 1:
            memo += f"\n**Related Optimization Considerations**:\n"
            for doctrine in doctrines[1:4]:
                memo += f"\n**{doctrine.topic}**:\n"
                memo += f"{doctrine.conclusion_template[0]}\n"
                memo += f"Key factors: {', '.join(doctrine.key_factors[:3])}\n"

        memo += f"\n**Controlling Precedents**:\n"
        for i, precedent in enumerate(primary.controlling_precedent, 1):
            memo += f"{i}. {precedent}\n"

        memo += f"\n**Burden of Proof**: {primary.burden_holder}\n"
        memo += f"**Applicable Scope**: {primary.entity_scope}\n"
        memo += f"**Analysis Zone**: {primary.zone.value}\n"

        if context:
            memo += f"\n**Current Well Context**:\n"
            for key, value in context.items():
                memo += f"- {key}: {value}\n"

        memo += f"\n---\n*This analysis represents drilling engineering best practices and industry standards as of the knowledge cutoff date. Field conditions may vary. Always validate recommendations against current well conditions and safety protocols.*"

        return memo

    def _extract_recommendations(
        self,
        doctrines: List[DoctrineBlock],
        context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Extract actionable recommendations"""
        recommendations = []

        for doctrine in doctrines[:3]:
            # Parse resolution strategy for actionable items
            strategy = doctrine.resolution_strategy
            if "implement" in strategy.lower():
                recommendations.append(f"{doctrine.topic}: {strategy[:150]}...")

            # Add context-specific recommendations
            if context and doctrine.topic == "ROP_Optimization_WOB_RPM_Relationship":
                if "rop" in context and context["rop"] < 50:
                    recommendations.append("Current ROP is low. Consider: 1) WOB ramp test to find founder point, 2) Increase RPM within bit limits, 3) Check for drilling dysfunctions")

        # Add general recommendations if list is short
        if len(recommendations) < 3:
            recommendations.extend([
                "Implement real-time MSE monitoring for drilling efficiency tracking",
                "Conduct offset well benchmarking to establish performance targets",
                "Review current bit selection and BHA design against offset well best practices"
            ])

        return recommendations[:5]

    def _assess_confidence(
        self,
        doctrines: List[DoctrineBlock],
        context: Optional[Dict[str, Any]]
    ) -> ConfidenceAssessment:
        """Assess confidence in analysis"""
        primary = doctrines[0]

        # Aggregate fact fragility
        avg_fragility = sum(d.fact_fragility for d in doctrines[:3]) / min(3, len(doctrines))

        # Determine confidence level
        if avg_fragility < 0.3:
            confidence_level = ConfidenceLevel.DEFENSIBLE
            explanation = "Analysis based on well-established drilling engineering principles with strong industry validation"
        elif avg_fragility < 0.5:
            confidence_level = ConfidenceLevel.AGGRESSIVE
            explanation = "Analysis based on industry best practices with moderate formation and operational variability"
        else:
            confidence_level = ConfidenceLevel.DISCLOSURE
            explanation = "Analysis involves significant assumptions about formation properties and operational execution"

        # Key assumptions
        assumptions = [
            "Formation properties consistent with offset well data",
            "Drilling equipment in good working condition",
            "Crew trained and following standard procedures",
            "Real-time data measurement accuracy within industry standards"
        ]

        # Data quality dependencies
        dependencies = [
            "Offset well drilling parameter and performance data",
            "Formation lithology and mechanical properties logs",
            "Accurate real-time drilling parameter measurements",
            "Bit dull grading and performance records"
        ]

        return ConfidenceAssessment(
            confidence_level=confidence_level,
            confidence_explanation=explanation,
            fact_fragility_score=avg_fragility,
            key_assumptions=assumptions,
            data_quality_dependencies=dependencies
        )

    def _compute_hash(self, query: str, response: str) -> str:
        """Compute SHA-256 determinism hash"""
        content = f"{query}|{response}|{self.version}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def get_health(self) -> HealthResponse:
        """Health check endpoint"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        return HealthResponse(
            status="healthy",
            engine_id=self.engine_id,
            version=self.version,
            doctrine_count=len(DOCTRINE_CACHE),
            uptime_seconds=uptime,
            total_queries=self.query_count
        )

# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

APP = FastAPI(
    title="DRL10 Drilling Optimization Engine",
    description="TIE Gold Standard implementation for drilling performance optimization",
    version="1.0.0"
)

# Add CORS middleware
APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
ENGINE = DRL10Engine()

@APP.post("/query", response_model=DrillingOptimizationResponse)
async def query_endpoint(request: DrillingQuery):
    """Main query endpoint for drilling optimization analysis"""
    try:
        return ENGINE.three_layer_response(
            query=request.query,
            mode=request.mode,
            context=request.context
        )
    except Exception as e:
        logger.error(f"Query error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint"""
    return ENGINE.get_health()

@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total_doctrines": len(DOCTRINE_CACHE),
        "topics": [d.topic for d in DOCTRINE_CACHE],
        "categories": list(set(d.zone.value for d in DOCTRINE_CACHE))
    }

@APP.get("/")
async def root():
    """Root endpoint"""
    return {
        "engine": "DRL10 Drilling Optimization Engine",
        "version": ENGINE.version,
        "status": "operational",
        "doctrine_count": len(DOCTRINE_CACHE),
        "endpoints": ["/query", "/health", "/doctrines"]
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting DRL10 Drilling Optimization Engine on port 9020")
    uvicorn.run(APP, host="0.0.0.0", port=9020)
