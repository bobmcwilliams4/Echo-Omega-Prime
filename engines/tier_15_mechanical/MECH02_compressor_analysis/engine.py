"""
MECH02 - Compressor Analysis Engine
Tax Intelligence Engine (TIE) Gold Standard Architecture
Domain: Mechanical Engineering - Gas Compression Systems

Port: 9042
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, Counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from loguru import logger
import uvicorn


# ============================================================================
# ENUMS AND DATA MODELS
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


class CompressorType(str, Enum):
    RECIPROCATING = "RECIPROCATING"
    CENTRIFUGAL = "CENTRIFUGAL"
    SCREW = "SCREW"
    AXIAL = "AXIAL"


class IssueCategory(str, Enum):
    DESIGN = "DESIGN"
    PERFORMANCE = "PERFORMANCE"
    MAINTENANCE = "MAINTENANCE"
    CONTROL = "CONTROL"
    STANDARDS = "STANDARDS"
    EFFICIENCY = "EFFICIENCY"
    VIBRATION = "VIBRATION"
    THERMODYNAMICS = "THERMODYNAMICS"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


@dataclass
class DoctrineBlock:
    """Core knowledge block with real compressor engineering expertise"""
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
    controlling_precedent: str
    issue_category: IssueCategory
    compressor_types: List[CompressorType]


@dataclass
class TelemetryRecord:
    """Track query performance and decisions"""
    query_id: str
    timestamp: float
    mode: ResponseMode
    cache_hit: bool
    doctrines_triggered: List[str]
    latency_ms: float
    confidence: ConfidenceLevel
    zone: AnalysisZone


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = None
    compressor_type: Optional[CompressorType] = None
    zone: AnalysisZone = AnalysisZone.PLANNING


class QueryResponse(BaseModel):
    query_id: str
    response: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    doctrines_applied: List[str]
    latency_ms: float
    determinism_hash: str
    epistemic_warnings: List[str]
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float


# ============================================================================
# DOCTRINE CACHE - REAL COMPRESSOR ENGINEERING EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="reciprocating_compressor_clearance_volume",
        keywords=["clearance", "volumetric efficiency", "reciprocating", "pocket", "clearance volume"],
        conclusion_template=[
            "Clearance volume is the space remaining in the cylinder when the piston is at top dead center (TDC).",
            "Volumetric efficiency decreases as clearance volume increases due to re-expansion of trapped gas.",
            "Typical clearance ranges from 3-10% of piston displacement; excessive clearance indicates valve/ring wear."
        ],
        reasoning_framework="""
1. Clearance volume (Vc) is essential space for valve operation but reduces efficiency
2. Re-expansion of compressed gas in clearance reduces net volume intake
3. Volumetric efficiency η_v = 1 + C - C*(r^(1/n)) where C=clearance ratio, r=pressure ratio, n=polytropic exponent
4. Variable clearance pockets allow capacity control without speed changes
5. Excessive clearance from worn components drastically reduces capacity
6. Clearance volume measurement during overhaul validates mechanical condition
7. API 618 specifies minimum volumetric efficiency requirements based on clearance
        """,
        key_factors=[
            "Clearance ratio (Vc/Vd) typically 3-10%",
            "Pressure ratio impact on re-expansion",
            "Fixed vs variable clearance pockets",
            "Valve unloading vs clearance control",
            "Mechanical wear increasing clearance",
            "API 618 efficiency requirements"
        ],
        primary_authority=["API 618 Fifth Edition", "GPSA Engineering Data Book Section 13", "Compressor Handbook (Hanlon)"],
        burden_holder="Maintenance",
        adversary_position="Clearance volume is negligible and doesn't affect performance",
        counter_arguments=[
            "10% clearance can reduce volumetric efficiency by 15-20% at high pressure ratios",
            "Field measurements show 1% clearance increase = 2-3% capacity loss",
            "API 618 mandates clearance verification during commissioning",
            "Variable clearance pockets are standard capacity control method",
            "Worn valves increase effective clearance beyond design"
        ],
        resolution_strategy="Calculate volumetric efficiency with actual clearance measurements; compare to API 618 minimum",
        entity_scope="Reciprocating compressors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: API 618 calculation methods are industry standard",
        controlling_precedent="API 618 Fifth Edition Section 4.3",
        issue_category=IssueCategory.DESIGN,
        compressor_types=[CompressorType.RECIPROCATING]
    ),

    DoctrineBlock(
        topic="centrifugal_surge_control",
        keywords=["surge", "centrifugal", "anti-surge", "stonewall", "operating envelope"],
        conclusion_template=[
            "Surge is unstable flow reversal occurring at low flow/high head conditions in centrifugal compressors.",
            "Anti-surge control prevents operation left of surge line by recycling or venting gas.",
            "Surge control line (SCL) must be positioned 10-15% right of actual surge line for safe margin."
        ],
        reasoning_framework="""
1. Surge occurs when flow decreases below minimum stable flow at given head
2. Flow reversal causes mechanical damage from rapid pressure/temperature fluctuations
3. Anti-surge valve (ASV) opens to increase flow through compressor
4. Surge control line positioned with safety margin accounts for instrumentation accuracy
5. Multiple surge events can destroy thrust bearings and seals
6. API 617 requires surge detection and control systems on all centrifugal compressors
7. Compressor map defines surge line, operating line, and choke line
8. Hot gas bypass vs cold recycle affects efficiency and process stability
        """,
        key_factors=[
            "Surge line definition from performance test",
            "Anti-surge valve sizing and response time",
            "Surge control line margin (typically 10-15%)",
            "Flow measurement accuracy and lag",
            "Multiple surge cycles = bearing damage",
            "API 617 surge control requirements",
            "Hot vs cold recycle tradeoffs"
        ],
        primary_authority=["API 617 Eighth Edition", "API 670 Machinery Protection Systems", "ASME PTC-10 Compressor Performance"],
        burden_holder="Controls",
        adversary_position="Occasional surge events are harmless and don't require sophisticated control",
        counter_arguments=[
            "Single severe surge can destroy thrust bearing in seconds",
            "API 617 mandates surge control for mechanical protection",
            "Field failures from surge cost $500K-$2M in downtime and repairs",
            "Insurance may deny claims if surge control not per API 617",
            "Modern DCS-based surge control prevents >99% of surge events"
        ],
        resolution_strategy="Implement API 617-compliant surge control with adequate margin; verify ASV response time <1 second",
        entity_scope="Centrifugal compressors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: API 617 surge control requirements are mandatory for machinery protection",
        controlling_precedent="API 617 Eighth Edition Chapter 4",
        issue_category=IssueCategory.CONTROL,
        compressor_types=[CompressorType.CENTRIFUGAL]
    ),

    DoctrineBlock(
        topic="polytropic_vs_isentropic_efficiency",
        keywords=["polytropic", "isentropic", "efficiency", "head", "multistage"],
        conclusion_template=[
            "Polytropic efficiency is the true measure of compressor aerodynamic performance independent of pressure ratio.",
            "Isentropic efficiency varies with pressure ratio making cross-comparison misleading for different applications.",
            "API 617 specifies polytropic efficiency for centrifugal compressor performance guarantees."
        ],
        reasoning_framework="""
1. Isentropic efficiency = (isentropic work)/(actual work) depends on pressure ratio
2. Polytropic efficiency represents infinitesimal stage efficiency, independent of pressure ratio
3. For multistage compressors, polytropic efficiency is constant but isentropic efficiency decreases with stages
4. η_polytropic > η_isentropic for pressure ratios >1.5
5. API 617 performance curves use polytropic head and efficiency
6. Polytropic exponent n = (k-1)/k * 1/η_p where k=specific heat ratio, η_p=polytropic efficiency
7. Field performance testing uses polytropic efficiency to detect degradation
8. Compressor selection and comparison must use same efficiency basis
        """,
        key_factors=[
            "Polytropic efficiency independent of pressure ratio",
            "Isentropic efficiency decreases with more stages",
            "API 617 uses polytropic basis",
            "Performance degradation detection",
            "Typical polytropic efficiency 72-86% for centrifugal",
            "Compressor map efficiency contours"
        ],
        primary_authority=["API 617 Eighth Edition", "ASME PTC-10", "GPSA Engineering Data Book Section 13"],
        burden_holder="Engineering",
        adversary_position="Isentropic efficiency is simpler and adequate for compressor evaluation",
        counter_arguments=[
            "API 617 explicitly requires polytropic efficiency for guarantees",
            "Isentropic efficiency comparison invalid for different pressure ratios",
            "Polytropic method aligns with ASME PTC-10 test procedures",
            "Field engineers misdiagnose degradation using isentropic method",
            "OEM performance curves universally use polytropic basis"
        ],
        resolution_strategy="Use polytropic efficiency per API 617; convert isentropic to polytropic for comparisons",
        entity_scope="Centrifugal and axial compressors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: API 617 and ASME PTC-10 specify polytropic method as industry standard",
        controlling_precedent="API 617 Eighth Edition Annex C",
        issue_category=IssueCategory.EFFICIENCY,
        compressor_types=[CompressorType.CENTRIFUGAL, CompressorType.AXIAL]
    ),

    DoctrineBlock(
        topic="rod_load_analysis_reciprocating",
        keywords=["rod load", "reversal", "combined load", "tension", "compression"],
        conclusion_template=[
            "Rod load analysis ensures the compressor rod operates within allowable tension and compression limits.",
            "Combined rod load includes gas forces, inertia forces, and friction must not exceed API 618 limits.",
            "Rod load reversal (crossing zero load) causes packing wear and reduced packing life."
        ],
        reasoning_framework="""
1. Gas load = (P_discharge - P_suction) * piston area varies through stroke
2. Inertia load = mass * acceleration reverses direction twice per revolution
3. Combined load = gas load + inertia load + friction
4. Tension load limited by rod material allowable stress
5. Compression load limited by rod buckling criteria (Euler column formula)
6. API 618 requires rod load diagrams for each cylinder
7. Rod load reversal (tension to compression) causes packing wear
8. High speed increases inertia loads; may require heavier rod
9. Unbalanced multistage compressors have higher rod loads
        """,
        key_factors=[
            "Maximum tension load vs allowable stress",
            "Maximum compression load vs buckling limit",
            "Rod load reversal frequency and magnitude",
            "Inertia force proportional to RPM²",
            "Packing life inversely proportional to load reversals",
            "API 618 rod load calculation requirements",
            "Rod material (typically 4140/4340 steel)"
        ],
        primary_authority=["API 618 Fifth Edition Section 4.8", "GPSA Engineering Data Book", "Compressor rod design standards"],
        burden_holder="Design Engineering",
        adversary_position="Rod loads are conservative; actual failures are rare",
        counter_arguments=[
            "Field rod failures occur when API 618 limits exceeded",
            "Rod load reversal is #1 cause of premature packing failure",
            "Insurance underwriters require API 618 compliance documentation",
            "High inertia loads at high speed cause fatigue failures",
            "Packing replacement costs $50K-$200K per event on large frames"
        ],
        resolution_strategy="Generate rod load diagram per API 618; verify no reversal or reduce speed/pressure to eliminate",
        entity_scope="Reciprocating compressors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: API 618 rod load analysis is mandatory mechanical design requirement",
        controlling_precedent="API 618 Fifth Edition Section 4.8",
        issue_category=IssueCategory.DESIGN,
        compressor_types=[CompressorType.RECIPROCATING]
    ),

    DoctrineBlock(
        topic="intercooling_benefits_multistage",
        keywords=["intercooler", "multistage", "isothermal", "power reduction", "efficiency"],
        conclusion_template=[
            "Intercooling between compression stages approaches isothermal compression reducing total power consumption.",
            "Intercooler effectiveness typically 85-95% achieved with finned tube or plate-fin heat exchangers.",
            "Power savings from intercooling = 8-15% for two-stage compression compared to single-stage."
        ],
        reasoning_framework="""
1. Compression work = ∫PdV; isothermal work is minimum theoretical work
2. Adiabatic compression heats gas increasing work for subsequent stages
3. Intercooling removes heat approaching isothermal path
4. Optimal staging: P2/P1 = P3/P2 = ... = (Pf/P1)^(1/n) for n stages
5. Intercooler effectiveness = (T2_actual - T3_actual)/(T2_actual - T_cooling) typically 85-95%
6. Pressure drop in intercooler (typically 2-5 psi) reduces benefit
7. Power savings = work saved - fan/pump power for cooling medium
8. Intercooling also reduces discharge temperature protecting downstream equipment
9. Water-cooled vs air-cooled intercooler selection depends on site conditions
        """,
        key_factors=[
            "Intercooler effectiveness 85-95%",
            "Pressure drop 2-5 psi typical",
            "Power savings 8-15% for two-stage",
            "Approach to isothermal compression",
            "Optimal interstage pressure ratio",
            "Cooling water availability and cost",
            "Discharge temperature reduction benefit"
        ],
        primary_authority=["GPSA Engineering Data Book Section 13", "API 618 intercooler requirements", "Heat exchanger design standards"],
        burden_holder="Process Engineering",
        adversary_position="Intercooler cost exceeds power savings value over equipment life",
        counter_arguments=[
            "NPV calculation shows 2-3 year payback on intercooler investment",
            "Reduced discharge temperature extends valve life by 50%+",
            "Lower temperature reduces moisture condensation in gas",
            "Field data confirms 10-12% power reduction with intercooling",
            "API 618 recommends intercooling for PR > 3.5 per stage"
        ],
        resolution_strategy="Economic analysis comparing intercooler CAPEX vs power savings NPV; typically justified for PR > 4 total",
        entity_scope="Multistage compressors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: Thermodynamic benefits are proven; economics depend on site-specific power costs",
        controlling_precedent="GPSA Engineering Data Book Figure 13-16",
        issue_category=IssueCategory.EFFICIENCY,
        compressor_types=[CompressorType.RECIPROCATING, CompressorType.CENTRIFUGAL]
    ),

    DoctrineBlock(
        topic="gas_properties_compression_performance",
        keywords=["molecular weight", "k-value", "Z-factor", "specific heat ratio", "compressibility"],
        conclusion_template=[
            "Gas molecular weight (MW) affects density and thus power required for compression at given volumetric flow.",
            "Specific heat ratio k=Cp/Cv affects polytropic exponent and compression temperature rise.",
            "Compressibility factor Z accounts for non-ideal gas behavior; using Z=1 for high pressure causes significant error."
        ],
        reasoning_framework="""
1. Power ∝ MW for constant volumetric flow and pressure ratio
2. Polytropic exponent n = (k-1)/k * 1/η_p determines temperature rise
3. Heavy gases (high MW, low k) compress with less temperature rise
4. Light gases (low MW, high k like H2) have high temperature rise per stage
5. Z-factor < 1 for most hydrocarbons at high pressure (non-ideal behavior)
6. Ideal gas assumption (Z=1) overpredicts power for high pressure applications
7. Gas property variations with composition require case-by-case analysis
8. Accurate equation of state (Peng-Robinson, SRK) required for Z-factor
9. Moisture in gas affects k-value and can cause liquid carryover
        """,
        key_factors=[
            "Molecular weight impact on power (∝ MW)",
            "k-value affects temperature rise (monatomic ~1.67, diatomic ~1.4, polyatomic ~1.1-1.3)",
            "Z-factor correction for non-ideal gas",
            "Gas composition variation over field life",
            "Equation of state selection (Peng-Robinson, SRK, BWRS)",
            "CO2 content increases MW and reduces k",
            "H2S content affects k-value and corrosivity"
        ],
        primary_authority=["GPSA Engineering Data Book Section 23", "API 617/618 gas property requirements", "Thermodynamic property databases"],
        burden_holder="Process Engineering",
        adversary_position="Gas can be treated as ideal (Z=1) for simplicity in design calculations",
        counter_arguments=[
            "High pressure gas (>500 psig) has Z=0.7-0.9; Z=1 assumption causes 15-30% error",
            "API 617 requires real gas properties for performance predictions",
            "OEM selection programs use rigorous thermodynamics, not ideal gas",
            "Field performance deviates from predictions when ideal gas assumed",
            "Modern process simulators (ProMax, HYSYS) solve real gas properties instantly"
        ],
        resolution_strategy="Use equation of state (Peng-Robinson or SRK) for Z-factor; update gas composition in models quarterly",
        entity_scope="All compressor types",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: Real gas thermodynamics required by API standards and proven in field performance",
        controlling_precedent="API 617 Annex C, API 618 Section 1.3",
        issue_category=IssueCategory.THERMODYNAMICS,
        compressor_types=[CompressorType.RECIPROCATING, CompressorType.CENTRIFUGAL, CompressorType.SCREW]
    ),

    DoctrineBlock(
        topic="compressor_valve_design_maintenance",
        keywords=["valve", "plate valve", "channel valve", "poppet", "valve life", "valve loss"],
        conclusion_template=[
            "Compressor valves are the highest maintenance item in reciprocating compressors with typical life 8,000-16,000 hours.",
            "Plate valves offer longer life and lower maintenance than channel valves but higher pressure drop.",
            "Valve loss (pressure drop) directly increases power consumption; 1 psi loss ≈ 0.3% power increase."
        ],
        reasoning_framework="""
1. Valves open/close every revolution subjected to pressure differential and impact
2. Plate valves use flexible steel plates; channel valves use guided strips
3. Poppet valves (ring valves) used for high pressure/high MW gas applications
4. Valve loss = pressure drop during flow through valve = wasted compression energy
5. Typical valve loss 1-4% of compression pressure rise
6. Valve life inversely proportional to speed (RPM) and pressure differential
7. Premature valve failure from liquid slugs, solids, or high temperature
8. API 618 requires valves accessible without removing cylinders
9. Condition monitoring via valve temperature, noise, cylinder performance
10. Replacing valves before failure prevents secondary damage to pistons/cylinders
        """,
        key_factors=[
            "Valve life typically 8,000-16,000 hours",
            "Plate vs channel vs poppet valve selection",
            "Valve loss 1-4% of pressure rise",
            "1 psi valve loss ≈ 0.3% power increase",
            "Liquid slugs destroy valves instantly",
            "Valve accessibility per API 618",
            "Predictive replacement vs run-to-failure"
        ],
        primary_authority=["API 618 Fifth Edition valve requirements", "OEM valve maintenance manuals", "Field valve life data"],
        burden_holder="Maintenance",
        adversary_position="Run valves to failure since replacement is quick and cheap",
        counter_arguments=[
            "Catastrophic valve failure causes piston/cylinder damage ($50K-$200K repair)",
            "Unplanned downtime costs 10x planned maintenance shutdown",
            "Valve debris from failure damages downstream equipment",
            "API 618 recommends condition-based valve replacement",
            "Modern thermography detects failing valves 1-2 weeks before catastrophic failure"
        ],
        resolution_strategy="Implement condition-based valve monitoring (temperature, performance); replace at 70-80% of expected life",
        entity_scope="Reciprocating compressors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: Field data supports predictive valve replacement reducing total cost of ownership",
        controlling_precedent="API 618 Fifth Edition Section 4.7",
        issue_category=IssueCategory.MAINTENANCE,
        compressor_types=[CompressorType.RECIPROCATING]
    ),

    DoctrineBlock(
        topic="packing_rider_ring_wear_mechanisms",
        keywords=["packing", "rider ring", "rod wear", "packing case", "lubrication"],
        conclusion_template=[
            "Packing prevents pressurized gas from escaping along the compressor rod requiring tight sealing and lubrication.",
            "Rider rings support the rod preventing metal-to-metal contact in the packing case.",
            "Packing life 4,000-12,000 hours depends on rod load reversal, gas cleanliness, and lubrication quality."
        ],
        reasoning_framework="""
1. Packing rings seal against rod; rider rings support rod in packing case
2. Tangential cut packing allows installation without rod removal
3. Rod load reversal causes packing wear as rod direction changes
4. Contaminated gas (solids, liquids) drastically reduces packing life
5. Insufficient lubrication causes excessive wear and heat
6. Packing case vent monitors packing leakage and wear
7. Rod surface finish (8-16 RMS) critical for packing sealing and life
8. Packing pressure breakdown through multiple rings in series
9. Packing case pressure typically 5-15% of discharge pressure
10. Excessive packing case pressure indicates worn packing rings
        """,
        key_factors=[
            "Packing life 4,000-12,000 hours typical",
            "Rod load reversal accelerates wear",
            "Gas cleanliness (particles >10 micron damage packing)",
            "Lubrication rate 2-8 drops/minute typical",
            "Rod surface finish 8-16 RMS",
            "Packing case pressure monitoring",
            "Tangential cut vs butt cut packing"
        ],
        primary_authority=["API 618 packing requirements", "OEM packing maintenance procedures", "Packing vendor technical bulletins"],
        burden_holder="Maintenance",
        adversary_position="Packing is cheap consumable; replace only when obvious leakage occurs",
        counter_arguments=[
            "Packing failure releases hydrocarbon gas (safety/environmental risk)",
            "Excessive packing wear scores rod requiring expensive rod replacement",
            "Packing case pressure >20% of discharge indicates imminent failure",
            "Planned packing replacement costs $5K; emergency replacement costs $50K+ in downtime",
            "API 618 requires packing case pressure monitoring for leak detection"
        ],
        resolution_strategy="Monitor packing case pressure; replace packing when pressure >15% discharge or every 8,000 hours",
        entity_scope="Reciprocating compressors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: Packing monitoring and preventive replacement is industry best practice",
        controlling_precedent="API 618 Fifth Edition Section 4.9",
        issue_category=IssueCategory.MAINTENANCE,
        compressor_types=[CompressorType.RECIPROCATING]
    ),

    DoctrineBlock(
        topic="api_618_recip_standards_compliance",
        keywords=["API 618", "reciprocating", "design standard", "pulsation", "mechanical design"],
        conclusion_template=[
            "API 618 Fifth Edition is the petroleum industry standard for reciprocating compressor procurement and design.",
            "API 618 mandates pulsation analysis, mechanical design criteria, and performance testing requirements.",
            "Non-API 618 compressors acceptable for non-critical service but insurance/financing may require API compliance."
        ],
        reasoning_framework="""
1. API 618 covers design, materials, fabrication, inspection, testing of reciprocating compressors
2. Pulsation analysis required to prevent piping vibration and failures
3. Mechanical design criteria: rod load, bearing load, foundation, torsional analysis
4. Performance test requirements: capacity, power, efficiency verification
5. Separable vs integral compressors have different API 618 requirements
6. Labyrinth piston vs pressure packing design requirements
7. Five inspection levels from normal to most stringent
8. API 618 compliance adds 15-25% to compressor cost but reduces lifecycle cost
9. Insurance underwriters require API 618 for compressors >500 HP
10. Non-API compressors suitable for intermittent or non-critical applications
        """,
        key_factors=[
            "Pulsation analysis mandatory (API 618 Chapter 3)",
            "Mechanical design criteria (loads, stress, deflection)",
            "Performance testing requirements (Chapter 5)",
            "Separable vs integral machine requirements",
            "Five inspection levels",
            "15-25% cost premium for API 618",
            "Insurance/financing requirements"
        ],
        primary_authority=["API 618 Fifth Edition", "API 688 pulsation control", "Insurance underwriting requirements"],
        burden_holder="Procurement/Engineering",
        adversary_position="Non-API compressor adequate for our application; API compliance is expensive over-engineering",
        counter_arguments=[
            "API 618 requirements derived from field failure analysis over decades",
            "Pulsation-induced piping failures cost $500K-$5M in damage and downtime",
            "Insurance may deny claims if non-API compressor fails in critical service",
            "Lenders require API 618 compliance for project financing",
            "API 618 compressors have 2-3x longer MTBF than non-API equivalents"
        ],
        resolution_strategy="Specify API 618 for critical service (>500 HP, continuous operation, hazardous gas); cost-benefit analysis required",
        entity_scope="Reciprocating compressors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: API 618 is industry consensus standard for critical reciprocating compressor applications",
        controlling_precedent="API 618 Fifth Edition",
        issue_category=IssueCategory.STANDARDS,
        compressor_types=[CompressorType.RECIPROCATING]
    ),

    DoctrineBlock(
        topic="api_617_centrifugal_standards_compliance",
        keywords=["API 617", "centrifugal", "design standard", "performance test", "mechanical running test"],
        conclusion_template=[
            "API 617 Eighth Edition is the petroleum industry standard for centrifugal compressor procurement and design.",
            "API 617 requires mechanical running test, performance test, and comprehensive inspection/testing regime.",
            "Special purpose compressors (API 617) vs general purpose (API 672) selected based on criticality and cost."
        ],
        reasoning_framework="""
1. API 617 covers axial and centrifugal compressors for petroleum, chemical, and gas industry
2. Mechanical running test verifies vibration, bearing temperature, seal performance
3. Performance test verifies head, efficiency, surge point per ASME PTC-10
4. String test for multi-body trains simulates installed configuration
5. Rotor dynamics analysis required to avoid critical speeds in operating range
6. Dry gas seals vs oil film seals specified based on gas composition and emissions
7. API 617 compliance adds 30-50% to compressor cost vs general purpose design
8. Three inspection levels: standard, intermediate, comprehensive
9. Surge control system requirements per API 617 Chapter 4
10. Lube oil system designed per API 614
        """,
        key_factors=[
            "Mechanical running test (vibration, temperature, seals)",
            "Performance test per ASME PTC-10",
            "Rotor dynamics analysis avoiding criticals",
            "Dry gas seal vs oil film seal selection",
            "30-50% cost premium for API 617",
            "Three inspection levels",
            "Surge control per API 617 Chapter 4"
        ],
        primary_authority=["API 617 Eighth Edition", "ASME PTC-10", "API 614 lube oil systems"],
        burden_holder="Procurement/Engineering",
        adversary_position="General purpose compressor (API 672) adequate and much cheaper than special purpose API 617",
        counter_arguments=[
            "API 617 critical speed analysis prevents catastrophic vibration failures",
            "Comprehensive factory testing detects issues before field installation",
            "API 617 compressors achieve 99%+ availability in critical service",
            "General purpose compressor failure in critical service costs $2M-$10M downtime",
            "Project financing requires API 617 for compressors >5,000 HP"
        ],
        resolution_strategy="Specify API 617 for critical service (continuous operation, no backup, >2,000 HP); API 672 acceptable for non-critical",
        entity_scope="Centrifugal and axial compressors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: API 617 is industry consensus standard for critical centrifugal compressor applications",
        controlling_precedent="API 617 Eighth Edition",
        issue_category=IssueCategory.STANDARDS,
        compressor_types=[CompressorType.CENTRIFUGAL, CompressorType.AXIAL]
    ),

    DoctrineBlock(
        topic="capacity_control_methods_comparison",
        keywords=["capacity control", "speed control", "suction throttle", "clearance pocket", "slide valve", "IGV"],
        conclusion_template=[
            "Speed control via VFD is most efficient capacity control method reducing power proportionally with flow.",
            "Suction throttling wastes power but is simple/cheap for applications not requiring continuous turndown.",
            "Clearance pocket unloaders for reciprocating and IGV/diffuser control for centrifugal achieve good efficiency."
        ],
        reasoning_framework="""
1. Speed control (VFD): Power ∝ Speed³, flow ∝ Speed, excellent turndown with efficiency
2. Suction throttling: Reduces suction pressure artificially, power reduction minimal, wastes energy
3. Clearance pocket (recip): Reduces volumetric efficiency, moderate power reduction
4. Bypass/recycle: Maintains full load on compressor, zero power savings, used for surge control
5. Inlet guide vanes (IGV, centrifugal): Pre-swirl reduces head and power, good efficiency
6. Diffuser vanes (centrifugal): Adjust diffuser angle changing head/flow, excellent efficiency
7. Slide valve (screw): Adjusts internal compression ratio, moderate efficiency
8. Step control (cylinder unloading, recip): 25/50/75/100% steps, good efficiency in steps
9. Selection criteria: turndown range, efficiency, CAPEX, control precision, reliability
        """,
        key_factors=[
            "Speed control (VFD): best efficiency, high CAPEX",
            "Suction throttle: worst efficiency, low CAPEX",
            "Clearance pocket: moderate efficiency, moderate CAPEX",
            "IGV/diffuser: good efficiency, high CAPEX",
            "Bypass: zero efficiency benefit, used only for surge control",
            "Step control: good average efficiency",
            "Turndown range requirements vs method capability"
        ],
        primary_authority=["GPSA Engineering Data Book Section 13", "API 618/617 capacity control guidance", "VFD vendor application guides"],
        burden_holder="Controls/Process Engineering",
        adversary_position="Suction throttling is adequate and avoids VFD cost and complexity",
        counter_arguments=[
            "VFD pays back in 2-4 years from power savings on variable flow applications",
            "Suction throttling wastes 20-40% of power at reduced capacity",
            "Modern VFDs have 98%+ efficiency and high reliability",
            "Environmental permits increasingly require efficiency improvements (VFD)",
            "Field data shows VFD reduces compressor station power 15-35% annually"
        ],
        resolution_strategy="Economic analysis: VFD if annual load factor <85%; clearance/IGV if 85-95%; fixed speed if >95%",
        entity_scope="All compressor types",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: VFD economic benefits proven across thousands of installations; thermodynamic efficiency proven",
        controlling_precedent="GPSA Engineering Data Book Section 13.22",
        issue_category=IssueCategory.CONTROL,
        compressor_types=[CompressorType.RECIPROCATING, CompressorType.CENTRIFUGAL, CompressorType.SCREW]
    ),

    DoctrineBlock(
        topic="vibration_monitoring_api_670",
        keywords=["vibration", "API 670", "proximity probe", "accelerometer", "bearing monitoring"],
        conclusion_template=[
            "API 670 specifies machinery protection system requirements including vibration monitoring for critical compressors.",
            "Proximity probes measure shaft displacement; accelerometers measure casing vibration; both required on critical machines.",
            "Vibration alarm/trip setpoints per API 617/618 prevent catastrophic failures from excessive vibration."
        ],
        reasoning_framework="""
1. Vibration monitoring detects unbalance, misalignment, bearing wear, rub, surge
2. Proximity probes (eddy current) measure shaft displacement relative to bearing
3. Accelerometers measure casing/bearing housing high frequency vibration
4. API 670 requires dual redundant sensors on critical machines
5. Alarm setpoint typically 50% of trip; trip prevents catastrophic failure
6. Continuous monitoring via DCS/PLC with trending and alarm annunciation
7. API 617/618 specify vibration limits based on rotor weight and speed
8. Sudden vibration increase indicates imminent failure; immediate shutdown required
9. Vibration spectrum analysis identifies failure mode (unbalance vs misalignment vs bearing defect)
10. Wireless vibration sensors now available but API 670 requires hardwired for critical machines
        """,
        key_factors=[
            "Proximity probes for shaft displacement (mils pk-pk)",
            "Accelerometers for casing vibration (g or in/sec)",
            "Dual redundant sensors on critical machines",
            "Alarm at 50% of trip setpoint typical",
            "API 617/618 vibration limits (function of speed/weight)",
            "Continuous monitoring and trending",
            "Spectrum analysis for diagnostics"
        ],
        primary_authority=["API 670 Fifth Edition", "API 617 vibration limits", "API 618 vibration limits", "ISO 10816 machinery vibration"],
        burden_holder="Instrumentation/Controls",
        adversary_position="Periodic handheld vibration measurements adequate; continuous monitoring is expensive overkill",
        counter_arguments=[
            "API 670 mandates continuous monitoring on critical compressors >1,000 HP",
            "Catastrophic failure from undetected vibration costs $1M-$10M",
            "Handheld measurements miss transient vibration events (surge, rub)",
            "Insurance requires API 670 compliance on critical rotating equipment",
            "Modern DCS integration makes continuous monitoring cost-effective"
        ],
        resolution_strategy="Implement API 670-compliant continuous vibration monitoring on all critical compressors per API 617/618",
        entity_scope="Critical compressors (API 617/618)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: API 670 is industry consensus standard for machinery protection systems",
        controlling_precedent="API 670 Fifth Edition",
        issue_category=IssueCategory.VIBRATION,
        compressor_types=[CompressorType.RECIPROCATING, CompressorType.CENTRIFUGAL]
    ),

    DoctrineBlock(
        topic="screw_compressor_applications_limitations",
        keywords=["screw compressor", "oil flooded", "oil free", "slide valve", "vi ratio"],
        conclusion_template=[
            "Oil-flooded screw compressors achieve 5-10:1 pressure ratios in single stage with good efficiency and low maintenance.",
            "Oil-free screw compressors required for process gas but have lower efficiency and higher maintenance than oil-flooded.",
            "Internal volume ratio (Vi) must match external pressure ratio for efficient operation; mismatch wastes power."
        ],
        reasoning_framework="""
1. Screw compressor uses intermeshing helical rotors to trap and compress gas
2. Oil-flooded: oil seals, cools, lubricates; contaminates gas requiring separation
3. Oil-free: no oil contact with gas, lower efficiency, timing gears synchronize rotors
4. Built-in volume ratio (Vi) = V_inlet / V_discharge designed for specific pressure ratio
5. Vi mismatch: over-compression (Vi too high) or under-compression (Vi too low) wastes power
6. Slide valve adjusts capacity and Vi ratio within limits
7. Typical applications: VRU, refrigeration, air service, low-pressure gas gathering
8. Not suitable for high pressure ratio (>10:1 single stage) or high MW gas
9. Simple design, few wearing parts, lower maintenance than reciprocating
10. API 619 covers screw compressor design for petroleum service
        """,
        key_factors=[
            "Oil-flooded: 5-10:1 PR single stage, oil contamination issue",
            "Oil-free: lower efficiency, process gas compatible",
            "Vi ratio must match application PR",
            "Slide valve capacity/Vi control",
            "Typical applications: VRU, refrigeration, air",
            "Not for high PR or high MW gas",
            "API 619 screw compressor standard"
        ],
        primary_authority=["API 619 Fifth Edition", "Screw compressor OEM technical manuals", "GPSA Engineering Data Book"],
        burden_holder="Engineering",
        adversary_position="Screw compressor universally applicable replacing reciprocating compressors in all services",
        counter_arguments=[
            "Screw compressor inefficient for PR >8:1 requiring multistage with intercooling",
            "High MW gas (>40) requires excessive power in screw vs reciprocating",
            "Oil-free screw has 10-15% lower efficiency than oil-flooded",
            "Vi mismatch in variable pressure service reduces efficiency 5-15%",
            "Reciprocating compressor preferred for high PR, high MW, or variable pressure applications"
        ],
        resolution_strategy="Select screw for VRU, refrigeration, air service PR <8:1; reciprocating for high PR/MW applications",
        entity_scope="Screw compressors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: Screw compressor advantages/limitations well documented in API 619 and field experience",
        controlling_precedent="API 619 Fifth Edition",
        issue_category=IssueCategory.DESIGN,
        compressor_types=[CompressorType.SCREW]
    ),

    DoctrineBlock(
        topic="compression_ratio_calculation_multistage",
        keywords=["compression ratio", "pressure ratio", "stage ratio", "optimal staging", "multistage"],
        conclusion_template=[
            "Overall compression ratio is final discharge pressure divided by initial suction pressure (r = Pd/Ps).",
            "Optimal staging for minimum work: equal pressure ratios per stage (P2/P1 = P3/P2 = ... = r^(1/n)).",
            "Practical staging considers intercooler pressure drop and discharge temperature limits per stage."
        ],
        reasoning_framework="""
1. Compression ratio r = P_discharge / P_suction (absolute pressures)
2. For n stages with intercooling, optimal staging: each stage has ratio r^(1/n)
3. Equal work per stage minimizes total work when intercooling to same inlet temperature
4. Intercooler pressure drop reduces benefit of staging (typically 2-5 psi loss)
5. Discharge temperature limit (typically 275-350°F) may force more stages
6. Reciprocating: limited to ~4:1 per stage for volumetric efficiency
7. Centrifugal: limited to ~2.5:1 per stage (impeller) for good efficiency
8. Very high ratio (>20:1) may require 3-4 stages with intercooling
9. Stage ratio affects valve life (recip), impeller tip speed (centrifugal)
        """,
        key_factors=[
            "Overall ratio r = Pd/Ps",
            "Optimal staging: equal ratios r^(1/n) per stage",
            "Intercooler pressure drop penalty",
            "Discharge temperature limit per stage",
            "Reciprocating: ~4:1 per stage max",
            "Centrifugal: ~2.5:1 per impeller max",
            "High ratio applications require multistaging"
        ],
        primary_authority=["GPSA Engineering Data Book Section 13", "Thermodynamics textbooks (Moran & Shapiro)", "API 618/617 staging guidance"],
        burden_holder="Process Engineering",
        adversary_position="Single stage compression adequate for any pressure ratio with sufficient driver power",
        counter_arguments=[
            "High ratio single stage causes excessive discharge temperature (>500°F) damaging valves/seals",
            "Volumetric efficiency <50% at 8:1 ratio in reciprocating compressor",
            "Multistage with intercooling reduces power 8-15% vs single stage at same ratio",
            "API 618 recommends intercooling for PR >3.5 to protect components",
            "Field experience: single stage >5:1 has poor reliability and high maintenance"
        ],
        resolution_strategy="Calculate optimal staging r^(1/n); adjust for intercooler ΔP and Td limit; typically 2 stages for r=4-12, 3+ for r>12",
        entity_scope="All compressor types",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: Thermodynamic optimization and equipment limitations well established",
        controlling_precedent="GPSA Engineering Data Book Figure 13-16",
        issue_category=IssueCategory.DESIGN,
        compressor_types=[CompressorType.RECIPROCATING, CompressorType.CENTRIFUGAL]
    ),

    DoctrineBlock(
        topic="field_gas_compression_for_gas_lift",
        keywords=["gas lift", "field compression", "casing head gas", "injection pressure", "VRU"],
        conclusion_template=[
            "Field gas compression for gas lift typically compresses casing head gas (50-150 psig) to injection pressure (800-1500 psig).",
            "Screw or reciprocating compressors selected based on capacity, pressure ratio, and gas quality.",
            "VRU (vapor recovery unit) captures and compresses tank vapors preventing venting and recovering valuable gas."
        ],
        reasoning_framework="""
1. Gas lift uses compressed gas injected into wellbore to reduce flowing bottomhole pressure
2. Injection pressure must overcome tubing head pressure plus hydrostatic column
3. Typical field compression: 2-stage reciprocating with intercooler for 8-15:1 ratio
4. Casing head gas may contain H2S, CO2, liquids requiring scrubbers and dehydration
5. VRU compresses tank vapors (atmospheric to sales line pressure 100-1000 psig)
6. Engine-driven compressors common in field (no electric power) using field gas as fuel
7. Portability vs permanent installation depends on well life and production rate
8. Gas quality affects compressor metallurgy (H2S requires special materials)
9. Remote monitoring and auto-shutdown for unmanned operation
10. Flare reduction regulations driving VRU adoption replacing venting
        """,
        key_factors=[
            "Casing head gas 50-150 psig to injection 800-1500 psig",
            "2-stage reciprocating typical for 8-15:1 PR",
            "H2S/CO2 content requires scrubbing and special metallurgy",
            "Engine-driven common (no electric power in field)",
            "VRU for tank vapor recovery (flare reduction)",
            "Remote monitoring for unmanned sites",
            "Portability vs permanent installation"
        ],
        primary_authority=["API 618 field compressor guidance", "Gas lift design manuals", "EPA flare reduction regulations"],
        burden_holder="Production/Facilities Engineering",
        adversary_position="Vent tank vapors to atmosphere rather than install expensive VRU",
        counter_arguments=[
            "EPA regulations increasingly prohibit routine flaring/venting",
            "VRU economics: $200K CAPEX recovers 50-200 Mcf/day = 1-3 year payback",
            "Vented gas represents lost revenue and methane emissions",
            "ESG requirements and carbon credits favor VRU installation",
            "Insurance/financing may require VRU for environmental compliance"
        ],
        resolution_strategy="Install VRU for production >25 BOPD or regulatory requirement; gas lift compression ROI analysis based on incremental oil production",
        entity_scope="Field compression (reciprocating, screw)",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="AGGRESSIVE: VRU economics variable by gas value; gas lift compression proven technology",
        controlling_precedent="EPA regulations and economic analysis",
        issue_category=IssueCategory.DESIGN,
        compressor_types=[CompressorType.RECIPROCATING, CompressorType.SCREW]
    ),

    DoctrineBlock(
        topic="gas_dehydration_before_compression",
        keywords=["dehydration", "glycol", "water content", "hydrates", "corrosion"],
        conclusion_template=[
            "Gas dehydration before compression prevents hydrate formation, corrosion, and liquid carryover damage to compressor.",
            "Triethylene glycol (TEG) dehydration achieves <7 lb H2O/MMscf meeting pipeline specs and preventing hydrates.",
            "Hydrate formation temperature increases with pressure; compression without dehydration risks hydrate blockage."
        ],
        reasoning_framework="""
1. Water vapor in gas condenses when cooled (intercoolers, aftercoolers)
2. Hydrates form at low temperature + high pressure blocking lines and damaging equipment
3. Water causes internal corrosion in carbon steel piping and compressor components
4. Liquid water carryover destroys compressor valves (recip) or causes surge (centrifugal)
5. TEG dehydration absorbs water reducing content to <7 lb/MMscf (pipeline spec <7-10 lb/MMscf)
6. Molecular sieve dehydration achieves <1 lb/MMscf for cryogenic applications
7. Compression increases gas temperature but intercooling/aftercooling re-approaches water dewpoint
8. API 618/617 require inlet scrubbers to prevent liquid carryover
9. Hydrate inhibitors (methanol, MEG) prevent hydrates but don't remove water
10. Gas quality specifications drive dehydration requirement
        """,
        key_factors=[
            "Hydrate prevention (pressure-temperature dependent)",
            "Corrosion prevention (water + CO2/H2S = corrosive)",
            "Liquid carryover damage to compressor",
            "Pipeline spec typically <7 lb H2O/MMscf",
            "TEG dehydration most common (to 7 lb/MMscf)",
            "Molecular sieve for cryogenic (to <1 lb/MMscf)",
            "Inlet scrubbers required per API 618/617"
        ],
        primary_authority=["GPSA Engineering Data Book Section 20", "API 618/617 inlet requirements", "Pipeline gas quality specs"],
        burden_holder="Process Engineering",
        adversary_position="Compress first, then dehydrate; avoid dehydration CAPEX upstream of compressor",
        counter_arguments=[
            "Compressor discharge temperature may exceed TEG/amine thermal stability",
            "Liquid water carryover to compressor destroys valves/impellers instantly",
            "Hydrate blockage in intercooler/aftercooler requires shutdown for clearing",
            "Corrosion from wet gas reduces compressor component life 50-75%",
            "Industry practice: dehydrate before compression for reliability and gas quality"
        ],
        resolution_strategy="Dehydrate before compression if gas >20 lb/MMscf or contains H2S/CO2; use inlet scrubbers minimum per API 618/617",
        entity_scope="Gas compression systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: Dehydration before compression is industry best practice for equipment protection and gas quality",
        controlling_precedent="GPSA Engineering Data Book Section 20, API 618/617 inlet requirements",
        issue_category=IssueCategory.DESIGN,
        compressor_types=[CompressorType.RECIPROCATING, CompressorType.CENTRIFUGAL, CompressorType.SCREW]
    ),

    DoctrineBlock(
        topic="compressor_driver_selection_engine_motor_turbine",
        keywords=["driver", "engine", "electric motor", "gas turbine", "VFD", "driver selection"],
        conclusion_template=[
            "Electric motor with VFD offers best efficiency and lowest maintenance for fixed installations with reliable power.",
            "Gas engine uses field gas as fuel suitable for remote locations without electric power.",
            "Gas turbine provides highest power density for large compressors but lowest fuel efficiency."
        ],
        reasoning_framework="""
1. Electric motor: 95%+ efficiency, low maintenance, requires reliable electric power
2. VFD enables variable speed control for capacity modulation and efficiency
3. Gas engine: 28-35% thermal efficiency, uses field gas (free fuel), higher maintenance
4. Gas turbine: 20-30% simple cycle efficiency, compact, high power density, expensive fuel
5. Driver selection criteria: power availability, fuel availability, efficiency, CAPEX, maintenance
6. Engine-driven common in field applications (gas lift, gathering, VRU)
7. Motor-driven preferred for central plants with electric power
8. Turbine-driven for very large compressors (>10,000 HP) or offshore platforms
9. Synchronous motor for constant speed, induction motor with VFD for variable speed
10. Power factor correction required for large induction motors
        """,
        key_factors=[
            "Electric motor: 95%+ efficiency, low maintenance, needs power",
            "VFD enables variable speed and efficiency",
            "Gas engine: 28-35% efficiency, field gas fuel, higher maintenance",
            "Gas turbine: 20-30% efficiency, compact, high power density",
            "Field applications: engine-driven (no power)",
            "Central plants: motor-driven (efficient, reliable power)",
            "Very large compressors: turbine-driven"
        ],
        primary_authority=["GPSA Engineering Data Book Section 13", "Driver vendor selection guides", "Economic comparison studies"],
        burden_holder="Mechanical/Electrical Engineering",
        adversary_position="Gas engine universally applicable; electric motor unnecessary complication and cost",
        counter_arguments=[
            "Electric motor + VFD saves 15-25% energy vs gas engine on variable load",
            "Motor maintenance 1/10th of engine maintenance cost annually",
            "Electric power available at central plants; wasting money on engine fuel",
            "VFD provides soft start reducing mechanical stress on compressor",
            "Engine emissions require permits and controls (NOx, CO); motor is emissions-free"
        ],
        resolution_strategy="Decision matrix: electric power available → motor+VFD; remote field → engine; very large → turbine; ROI analysis required",
        entity_scope="All compressor types",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: Driver selection depends on site-specific factors; efficiency and economics proven for each type",
        controlling_precedent="GPSA Engineering Data Book Section 13.24",
        issue_category=IssueCategory.DESIGN,
        compressor_types=[CompressorType.RECIPROCATING, CompressorType.CENTRIFUGAL, CompressorType.SCREW]
    ),

    DoctrineBlock(
        topic="compressor_station_design_layout",
        keywords=["compressor station", "layout", "piping design", "pulsation control", "spacing"],
        conclusion_template=[
            "Compressor station layout must consider pulsation control, maintenance access, safety spacing, and future expansion.",
            "Pulsation bottles and piping design per API 618 Chapter 3 or API 688 prevents vibration failures.",
            "Equipment spacing per NFPA and API RP 500 provides safety zones and maintenance access."
        ],
        reasoning_framework="""
1. Station layout: compressors, drivers, coolers, separators, controls, utilities
2. Pulsation analysis required per API 618/688 to size bottles and design piping
3. Reciprocating compressors generate pulsation requiring acoustic filters/bottles
4. Piping natural frequencies must avoid compressor operating frequencies
5. Maintenance access: overhead crane, laydown area, truck access
6. Safety spacing per NFPA 37 (engine-driven) and API RP 500 (electrical area classification)
7. Future expansion: reserve plot space for 50-100% capacity addition
8. Noise control: enclosures, barriers, distance from property line
9. Drainage and containment for oil spills
10. Control building separate from compressor building for safety
        """,
        key_factors=[
            "Pulsation analysis and control per API 618/688",
            "Acoustic bottles sized for frequency attenuation",
            "Piping design avoiding resonance",
            "Maintenance access (crane, laydown, truck)",
            "Safety spacing per NFPA 37 and API RP 500",
            "Future expansion plot space",
            "Noise control (enclosures, distance)",
            "Oil containment and drainage"
        ],
        primary_authority=["API 618 Chapter 3", "API 688 Pulsation Control", "NFPA 37", "API RP 500"],
        burden_holder="Facilities Engineering",
        adversary_position="Minimal station footprint saves cost; pulsation control and spacing are over-conservative",
        counter_arguments=[
            "Pulsation-induced piping failures cost $500K-$5M including compressor damage",
            "Inadequate maintenance access extends outage duration 2-5x",
            "NFPA 37 spacing prevents fire propagation between equipment",
            "Insurance underwriters require API 618/688 compliance for coverage",
            "Future expansion capability adds 10% to initial CAPEX but avoids 200% expansion cost later"
        ],
        resolution_strategy="Follow API 618/688 pulsation analysis; NFPA 37 spacing; provide 50% expansion space; economic analysis of layout options",
        entity_scope="Compressor stations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE: API and NFPA standards derived from field experience and failure analysis",
        controlling_precedent="API 618 Chapter 3, API 688, NFPA 37",
        issue_category=IssueCategory.DESIGN,
        compressor_types=[CompressorType.RECIPROCATING, CompressorType.CENTRIFUGAL]
    ),

    DoctrineBlock(
        topic="ngl_recovery_compression_refrigeration",
        keywords=["NGL", "cryogenic", "turboexpander", "refrigeration compression", "demethanizer"],
        conclusion_template=[
            "NGL recovery plants use cryogenic separation requiring refrigeration compression to achieve low temperatures (-20 to -150°F).",
            "Turboexpander process expands high-pressure gas generating refrigeration; residue gas recompression required.",
            "Propane refrigeration compression provides -40°F; ethylene or mixed refrigerant for lower temperatures."
        ],
        reasoning_framework="""
1. NGL recovery extracts C2+ (ethane+) or C3+ (propane+) from natural gas
2. Cryogenic separation requires -20°F to -150°F depending on ethane recovery target
3. Turboexpander: expand gas from high pressure generating cold via Joule-Thomson effect
4. Residue gas (methane) exits cold tower requiring recompression to pipeline pressure
5. Refrigeration compression: propane cycle (-40°F), ethylene cycle (-150°F), mixed refrigerant
6. Centrifugal compressors for large refrigeration duty (>5,000 HP)
7. Demethanizer tower separates methane from NGL; overhead gas recompressed
8. Compression work = major operating cost in NGL plants
9. Heat integration and turboexpander efficiency critical for economics
10. Molecular sieve dehydration required upstream to prevent hydrate/ice formation
        """,
        key_factors=[
            "Cryogenic temps -20 to -150°F for NGL recovery",
            "Turboexpander generates refrigeration, requires residue recompression",
            "Propane refrigeration -40°F, ethylene -150°F",
            "Centrifugal compressors for large refrigeration duty",
            "Compression = major operating cost",
            "Heat integration critical for economics",
            "Molecular sieve dehydration prevents ice formation"
        ],
        primary_authority=["GPSA Engineering Data Book Section 16", "Cryogenic process design references", "NGL plant operation manuals"],
        burden_holder="Process Engineering",
        adversary_position="Mechanical refrigeration cheaper than turboexpander for NGL recovery",
        counter_arguments=[
            "Turboexpander recovers 90%+ ethane vs 60% for mechanical refrigeration",
            "Turboexpander efficiency 80-88% vs Joule-Thomson throttling (0% efficiency)",
            "Large NGL plants (>100 MMscfd) universally use turboexpander economics",
            "Mechanical refrigeration limited to -40°F; turboexpander achieves -150°F",
            "Residue gas recompression work offset by turboexpander power generation"
        ],
        resolution_strategy="Economic analysis: turboexpander for >50 MMscfd and ethane recovery >70%; mechanical refrigeration for smaller plants",
        entity_scope="NGL recovery plants",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="AGGRESSIVE: Economics vary widely by plant size, gas composition, and NGL prices; detailed analysis required",
        controlling_precedent="GPSA Engineering Data Book Section 16",
        issue_category=IssueCategory.DESIGN,
        compressor_types=[CompressorType.CENTRIFUGAL]
    ),

    DoctrineBlock(
        topic="gas_gathering_compression_systems",
        keywords=["gathering", "field compression", "wellhead pressure", "low pressure", "booster compression"],
        conclusion_template=[
            "Gas gathering compression boosts low-pressure wellhead gas (20-100 psig) to pipeline pressure (400-1200 psig).",
            "Reciprocating compressors typical for gathering due to variable flow, pressure, and gas quality.",
            "Central gathering compression vs wellsite compression selected based on well count, flow rates, and terrain."
        ],
        reasoning_framework="""
1. Wellhead pressure declines over field life requiring compression to maintain production
2. Initial wellhead pressure 100-500 psig; after depletion 20-100 psig requiring boost
3. Low-pressure gathering system collects gas from multiple wells to central compressor
4. High-pressure gathering system compresses at wellsite then gathers compressed gas
5. Reciprocating compressors handle variable flow and pressure with good efficiency
6. Two-stage compression typical for 10-20:1 overall pressure ratio with intercooling
7. Inlet scrubbers remove liquids preventing compressor damage
8. Engine-driven compressors common using field gas as fuel
9. Central compression: lower CAPEX, easier maintenance, higher pipeline pressure drop
10. Wellsite compression: higher CAPEX, reduced pipeline pressure drop, unmanned operation challenges
        """,
        key_factors=[
            "Wellhead pressure declines requiring compression",
            "Low-pressure gathering 20-100 psig to pipeline 400-1200 psig",
            "Reciprocating compressors for variable conditions",
            "Two-stage with intercooling for 10-20:1 PR",
            "Inlet scrubbers prevent liquid carryover",
            "Engine-driven common (field gas fuel)",
            "Central vs wellsite compression tradeoffs"
        ],
        primary_authority=["GPSA Engineering Data Book Section 13", "Gas gathering system design manuals", "API 618 field compressor applications"],
        burden_holder="Production/Facilities Engineering",
        adversary_position="High-pressure gathering eliminates central compression; compress at every wellsite",
        counter_arguments=[
            "Wellsite compression CAPEX 3-5x higher than central compression",
            "Unmanned wellsite compressors have lower availability (85-90% vs 95%+ central)",
            "Central compression enables economies of scale and professional staffing",
            "High-pressure gathering pipeline more expensive (thicker wall, higher CAPEX)",
            "Industry trend: central compression for >10 wells, wellsite for remote single wells"
        ],
        resolution_strategy="Economic analysis: central compression if >10 wells within 5 miles; wellsite compression for remote wells or very low flow",
        entity_scope="Gas gathering systems",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="AGGRESSIVE: Central vs wellsite compression economics highly site-specific; both approaches proven",
        controlling_precedent="Economic analysis and field operating experience",
        issue_category=IssueCategory.DESIGN,
        compressor_types=[CompressorType.RECIPROCATING]
    ),
]


# ============================================================================
# COMPRESSOR ANALYSIS ENGINE
# ============================================================================

class CompressorAnalysisEngine:
    """TIE Gold Standard Engine for Compressor Engineering Analysis"""

    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.start_time = time.time()
        self.query_count = 0
        self.cache_hits = 0
        self.telemetry: List[TelemetryRecord] = []

        # Build keyword index for fast lookups
        self.keyword_index: Dict[str, List[DoctrineBlock]] = defaultdict(list)
        for doctrine in self.doctrines:
            for keyword in doctrine.keywords:
                self.keyword_index[keyword.lower()].append(doctrine)

        logger.info(f"Compressor Analysis Engine initialized with {len(self.doctrines)} doctrines")

    def three_layer_response(self, query: str, mode: ResponseMode, zone: AnalysisZone,
                            compressor_type: Optional[CompressorType] = None) -> Tuple[str, List[str], ConfidenceLevel]:
        """
        TIE-20 Component: Three-layer response system
        Layer 1: Doctrine cache (0-200ms)
        Layer 2: Semantic retrieval (fallback)
        Layer 3: Deep analysis (comprehensive)
        """
        query_lower = query.lower()

        # Layer 1: Doctrine cache lookup
        triggered_doctrines = self._match_doctrines(query_lower, compressor_type)

        if triggered_doctrines:
            self.cache_hits += 1
            response = self._synthesize_response(triggered_doctrines, query, mode, zone)
            confidence = self._aggregate_confidence(triggered_doctrines)
            doctrine_topics = [d.topic for d in triggered_doctrines]
            return response, doctrine_topics, confidence

        # Layer 2 would be semantic/vector search (not implemented in this engine)
        # Layer 3 would be deep LLM analysis (not implemented in this engine)

        # Fallback response
        return self._fallback_response(query, mode, zone), [], ConfidenceLevel.DISCLOSURE

    def _match_doctrines(self, query_lower: str, compressor_type: Optional[CompressorType]) -> List[DoctrineBlock]:
        """Match doctrines based on keywords and compressor type"""
        matches: Dict[str, int] = Counter()

        for keyword, doctrines_list in self.keyword_index.items():
            if keyword in query_lower:
                for doctrine in doctrines_list:
                    # Filter by compressor type if specified
                    if compressor_type and compressor_type not in doctrine.compressor_types:
                        continue
                    matches[doctrine.topic] += 1

        # Return top 3 matching doctrines
        top_topics = [topic for topic, _ in matches.most_common(3)]
        return [d for d in self.doctrines if d.topic in top_topics]

    def _synthesize_response(self, doctrines: List[DoctrineBlock], query: str,
                            mode: ResponseMode, zone: AnalysisZone) -> str:
        """Synthesize response from triggered doctrines based on mode and zone"""

        if mode == ResponseMode.FAST:
            # Concise response with key conclusions
            parts = [f"**Compressor Analysis ({zone.value} Zone)**\n"]
            for doctrine in doctrines:
                parts.append(f"\n**{doctrine.topic.replace('_', ' ').title()}:**")
                parts.append(doctrine.conclusion_template[0])
            return "\n".join(parts)

        elif mode == ResponseMode.DEFENSE:
            # Detailed audit-ready response with authority citations
            parts = [f"**Compressor Engineering Analysis - {zone.value} Zone**\n"]
            parts.append(f"**Query:** {query}\n")

            for doctrine in doctrines:
                parts.append(f"\n**Issue: {doctrine.topic.replace('_', ' ').title()}**")
                parts.append(f"**Category:** {doctrine.issue_category.value}")
                parts.append(f"**Compressor Types:** {', '.join([ct.value for ct in doctrine.compressor_types])}")

                parts.append(f"\n**Analysis:**")
                for conclusion in doctrine.conclusion_template:
                    parts.append(f"- {conclusion}")

                parts.append(f"\n**Key Factors:**")
                for factor in doctrine.key_factors[:5]:
                    parts.append(f"- {factor}")

                parts.append(f"\n**Authority:**")
                for auth in doctrine.primary_authority:
                    parts.append(f"- {auth}")

                parts.append(f"\n**Confidence:** {doctrine.confidence.value} - {doctrine.confidence_stratification}")

            return "\n".join(parts)

        else:  # MEMO mode
            # Comprehensive memorandum format
            parts = [
                "=" * 80,
                "COMPRESSOR ENGINEERING MEMORANDUM",
                f"Zone: {zone.value}",
                f"Date: {datetime.now().strftime('%Y-%m-%d')}",
                "=" * 80,
                f"\n**RE:** {query}\n"
            ]

            parts.append("**EXECUTIVE SUMMARY:**\n")
            for doctrine in doctrines:
                parts.append(f"- {doctrine.conclusion_template[0]}")

            parts.append("\n**DETAILED ANALYSIS:**\n")

            for i, doctrine in enumerate(doctrines, 1):
                parts.append(f"\n{i}. {doctrine.topic.replace('_', ' ').title()}")
                parts.append(f"   Category: {doctrine.issue_category.value}")
                parts.append(f"   Applicable to: {', '.join([ct.value for ct in doctrine.compressor_types])}")

                parts.append(f"\n   **Conclusions:**")
                for conclusion in doctrine.conclusion_template:
                    parts.append(f"   - {conclusion}")

                parts.append(f"\n   **Reasoning Framework:**")
                for line in doctrine.reasoning_framework.strip().split('\n'):
                    if line.strip():
                        parts.append(f"   {line}")

                parts.append(f"\n   **Key Factors:**")
                for factor in doctrine.key_factors:
                    parts.append(f"   - {factor}")

                parts.append(f"\n   **Counter-Arguments:**")
                for counter in doctrine.counter_arguments[:3]:
                    parts.append(f"   - {counter}")

                parts.append(f"\n   **Resolution Strategy:**")
                parts.append(f"   {doctrine.resolution_strategy}")

                parts.append(f"\n   **Authority References:**")
                for auth in doctrine.primary_authority:
                    parts.append(f"   - {auth}")

                parts.append(f"\n   **Confidence Assessment:** {doctrine.confidence.value}")
                parts.append(f"   {doctrine.confidence_stratification}")

            parts.append("\n" + "=" * 80)
            parts.append("END OF MEMORANDUM")
            parts.append("=" * 80)

            return "\n".join(parts)

    def _aggregate_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Aggregate confidence from multiple doctrines"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Use most conservative (lowest) confidence level
        confidence_order = [
            ConfidenceLevel.DEFENSIBLE,
            ConfidenceLevel.AGGRESSIVE,
            ConfidenceLevel.DISCLOSURE,
            ConfidenceLevel.HIGH_RISK
        ]

        doctrine_confidences = [d.confidence for d in doctrines]
        for level in confidence_order:
            if level in doctrine_confidences:
                return level

        return ConfidenceLevel.DISCLOSURE

    def _fallback_response(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
        """Fallback response when no doctrines match"""
        return f"""**Compressor Analysis ({zone.value} Zone)**

Query: {query}

**No Direct Doctrine Match**

This query did not trigger specific doctrine blocks in the compressor engineering knowledge base.

**General Guidance:**
- For reciprocating compressor questions, consult API 618 Fifth Edition
- For centrifugal compressor questions, consult API 617 Eighth Edition
- For screw compressor questions, consult API 619 Fifth Edition
- For general compressor engineering, consult GPSA Engineering Data Book Section 13

**Recommendation:**
Engage a professional compressor engineer for detailed analysis of this specific question. The query may require:
- Site-specific operational data
- Detailed equipment specifications
- Performance test results
- Thermodynamic modeling

**Confidence:** DISCLOSURE - This response is general guidance only and should not be relied upon for engineering decisions."""

    def _calculate_determinism_hash(self, query: str, response: str, mode: ResponseMode) -> str:
        """Calculate SHA-256 hash for reproducibility verification"""
        content = f"{query}|{mode.value}|{response}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _apply_epistemic_guardrails(self, response: str, confidence: ConfidenceLevel) -> List[str]:
        """Apply epistemic warnings based on confidence level"""
        warnings = []

        if confidence in [ConfidenceLevel.DISCLOSURE, ConfidenceLevel.HIGH_RISK]:
            warnings.append("This analysis involves significant uncertainty. Engage professional compressor engineer before making decisions.")

        if confidence == ConfidenceLevel.AGGRESSIVE:
            warnings.append("This analysis contains aggressive interpretations. Consider alternative perspectives and site-specific factors.")

        if "shall" in response.lower() or "must" in response.lower():
            warnings.append("Statements using 'shall' or 'must' may reflect code/standard requirements. Verify current edition of referenced standards.")

        return warnings

    def process_query(self, request: QueryRequest) -> QueryResponse:
        """Main query processing with full TIE-20 components"""
        query_id = hashlib.sha256(f"{request.query}{time.time()}".encode()).hexdigest()[:12]
        start = time.time()

        self.query_count += 1

        # Three-layer response
        response, doctrines_applied, confidence = self.three_layer_response(
            request.query, request.mode, request.zone, request.compressor_type
        )

        # Calculate metrics
        latency_ms = (time.time() - start) * 1000

        # Epistemic guardrails
        warnings = self._apply_epistemic_guardrails(response, confidence)

        # Determinism hash
        det_hash = self._calculate_determinism_hash(request.query, response, request.mode)

        # Telemetry
        telemetry = TelemetryRecord(
            query_id=query_id,
            timestamp=time.time(),
            mode=request.mode,
            cache_hit=len(doctrines_applied) > 0,
            doctrines_triggered=doctrines_applied,
            latency_ms=latency_ms,
            confidence=confidence,
            zone=request.zone
        )
        self.telemetry.append(telemetry)

        logger.info(f"Query {query_id} processed: {len(doctrines_applied)} doctrines, {latency_ms:.1f}ms, {confidence.value}")

        return QueryResponse(
            query_id=query_id,
            response=response,
            mode=request.mode,
            confidence=confidence,
            doctrines_applied=doctrines_applied,
            latency_ms=round(latency_ms, 2),
            determinism_hash=det_hash,
            epistemic_warnings=warnings,
            timestamp=datetime.now().isoformat()
        )

    def get_health(self) -> HealthResponse:
        """Health check endpoint"""
        uptime = time.time() - self.start_time
        cache_hit_rate = (self.cache_hits / self.query_count * 100) if self.query_count > 0 else 0.0

        return HealthResponse(
            status="healthy",
            version="1.0.0",
            port=9042,
            doctrines_loaded=len(self.doctrines),
            uptime_seconds=round(uptime, 2),
            total_queries=self.query_count,
            cache_hit_rate=round(cache_hit_rate, 2)
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="MECH02 - Compressor Analysis Engine",
    description="TIE Gold Standard Engine for Mechanical Engineering - Gas Compression Systems",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
engine = CompressorAnalysisEngine()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with three-layer response"""
    try:
        return engine.process_query(request)
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint"""
    return engine.get_health()


@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total": len(engine.doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "compressor_types": [ct.value for ct in d.compressor_types],
                "confidence": d.confidence.value,
                "keywords": d.keywords[:5]
            }
            for d in engine.doctrines
        ]
    }


@APP.get("/telemetry")
async def get_telemetry():
    """Get query telemetry statistics"""
    if not engine.telemetry:
        return {"message": "No telemetry data available"}

    recent = engine.telemetry[-100:]  # Last 100 queries

    avg_latency = sum(t.latency_ms for t in recent) / len(recent)
    cache_hit_rate = sum(1 for t in recent if t.cache_hit) / len(recent) * 100

    confidence_dist = Counter(t.confidence.value for t in recent)
    mode_dist = Counter(t.mode.value for t in recent)

    return {
        "total_queries": len(engine.telemetry),
        "recent_queries": len(recent),
        "avg_latency_ms": round(avg_latency, 2),
        "cache_hit_rate": round(cache_hit_rate, 2),
        "confidence_distribution": dict(confidence_dist),
        "mode_distribution": dict(mode_dist)
    }


if __name__ == "__main__":
    logger.info("Starting MECH02 Compressor Analysis Engine on port 9042")
    uvicorn.run(APP, host="0.0.0.0", port=9042)
