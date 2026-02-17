"""
REG09 Transportation Regulatory Engine v1.0.0
Port 9129 | TIE-Grade | 49 CFR FMCSA/PHMSA/FRA + 14 CFR FAA + State DOT

Handles: DOT regulations, FMCSA motor carrier safety, PHMSA hazmat transport,
FRA railroad safety, FAA aviation, CDL requirements, HOS rules, ELD mandate,
drug/alcohol testing, vehicle inspection, weight limits, oversize permits.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "REG09"
ENGINE_NAME = "Transportation Regulatory Engine"
VERSION = "1.0.0"
PORT = 9129

logger.add(f"REG09_engine_{datetime.now():%Y%m%d}.log", rotation="100 MB", retention="30 days", level="INFO")

# ============================================================================
# ENUMS
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
    FMCSA_MOTOR_CARRIER = "FMCSA_MOTOR_CARRIER"
    HOS_ELD = "HOS_ELD"
    CDL_DRIVER_QUAL = "CDL_DRIVER_QUAL"
    DRUG_ALCOHOL = "DRUG_ALCOHOL"
    VEHICLE_INSPECTION = "VEHICLE_INSPECTION"
    WEIGHT_SIZE = "WEIGHT_SIZE"
    PHMSA_HAZMAT = "PHMSA_HAZMAT"
    FRA_RAILROAD = "FRA_RAILROAD"
    FAA_AVIATION = "FAA_AVIATION"
    STATE_DOT = "STATE_DOT"
    PERMITS_OVERSIZE = "PERMITS_OVERSIZE"
    INSURANCE_FILING = "INSURANCE_FILING"

# ============================================================================
# DATA MODELS
# ============================================================================

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
    confidence_stratification: str
    controlling_precedent: str

class QueryRequest(BaseModel):
    question: str
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)

class QueryResponse(BaseModel):
    answer: str
    confidence: str
    mode: str
    zone: str
    doctrines_triggered: List[str]
    reasoning_chain: List[str]
    authorities_cited: List[str]
    response_time_ms: float
    determinism_hash: str
    epistemic_disclosure: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float

# ============================================================================
# DOCTRINE CACHE - 25+ TRANSPORTATION LAW BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="CDL Requirements 49 CFR 383",
        keywords=["CDL", "commercial driver license", "Class A", "Class B", "endorsements", "383"],
        conclusion_template=[
            "CDL requirements under 49 CFR Part 383 mandate specific license classes based on vehicle GVWR and operation type.",
            "Class A CDL required for combination vehicles over 26,001 lbs GVWR with towed unit over 10,000 lbs.",
            "Class B for single vehicles over 26,001 lbs or towing under 10,000 lbs; Class C for hazmat or 16+ passengers."
        ],
        reasoning_framework="""
49 CFR 383.91 defines three CDL classes: Class A (combination vehicles, GVWR 26,001+ lbs, towed 10,000+ lbs),
Class B (single vehicle 26,001+ lbs or towing under 10,000 lbs), Class C (hazmat placarded or 16+ passengers).
Endorsements required: H (hazmat), N (tank), P (passenger), S (school bus), T (double/triple trailers), X (tank+hazmat).
Air brake restriction if tested on non-air brake vehicle (49 CFR 383.95). Medical certification required every 2 years
(49 CFR 391.45). CDL must be obtained in state of domicile. Out-of-service for driving CMV without proper CDL (49 CFR 383.51).
States must disqualify drivers for serious violations: 60 days (1st), 120 days (2nd), 1 year (3rd) within 3 years (49 CFR 383.51).
Lifetime disqualification for using CMV in felony involving controlled substances.
        """,
        key_factors=["Vehicle GVWR", "Towed unit weight", "Cargo type (hazmat/passengers)", "Air brake equipment", "Medical certification", "State of domicile"],
        primary_authority=["49 CFR Part 383", "49 CFR 391.45 Medical", "49 CFR 383.51 Disqualification"],
        burden_holder="Driver and Motor Carrier",
        adversary_position="No CDL needed for intrastate farm vehicles or RVs under state exemptions",
        counter_arguments=["49 CFR 383.3(f) exempts farm vehicles in some states within 150 miles", "RV exception 49 CFR 383.3(c)", "Military exemption 49 CFR 383.3(d)"],
        resolution_strategy="Verify vehicle use (for-hire vs private), GVWR, state-specific exemptions, and domicile requirements",
        entity_scope="Interstate/Intrastate CMV operators",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="GVWR and class definitions are bright-line; exemptions require fact-intensive analysis",
        controlling_precedent="49 CFR 383 mandatory nationwide; states may have additional requirements but cannot reduce federal minimums"
    ),
    DoctrineBlock(
        topic="Hours of Service 49 CFR 395",
        keywords=["HOS", "hours of service", "11 hour", "14 hour", "70 hour", "395", "logbook"],
        conclusion_template=[
            "49 CFR Part 395 HOS rules limit driving to 11 hours after 10 consecutive off-duty hours.",
            "14-hour window: cannot drive after 14th hour from coming on duty, regardless of breaks.",
            "60/70 hour limit: cannot drive after 60 hours in 7 days or 70 hours in 8 days without 34-hour restart."
        ],
        reasoning_framework="""
49 CFR 395.3(a): 11-hour driving limit after 10 consecutive off-duty hours. 49 CFR 395.3(b): 14-hour on-duty window.
Once on duty, driver cannot drive after 14th hour even if 11 driving hours not used. 30-minute break required if
8+ hours since last 30-minute break (395.3(a)(3)ii). 60/70 hour rule: 60 hours in 7 consecutive days or 70 hours in
8 consecutive days (395.3(b)). 34-hour restart resets 60/70 clock if includes two 1am-5am periods (395.3(c)).
Sleeper berth provision: 10 hours can be split into 8+2 or 7+3 (395.1(g)). Short-haul exemption: 100 air-mile radius,
12-hour duty period, no sleeper berth, return to work reporting location (395.1(e)). Adverse driving conditions
exception adds 2 hours to 11/14 limits (395.1(b)). Agricultural exemption during planting/harvest (395.1(k)).
ELD mandate 49 CFR 395.8 requires electronic logging devices (exceptions: pre-2000 trucks, driveaway, short-haul).
        """,
        key_factors=["Duty status (on-duty, driving, sleeper, off-duty)", "14-hour window", "30-minute break timing", "34-hour restart", "Exemptions applicability"],
        primary_authority=["49 CFR 395.3 HOS limits", "49 CFR 395.8 ELD", "49 CFR 395.1 Exceptions"],
        burden_holder="Driver and Motor Carrier",
        adversary_position="Adverse conditions or agricultural exemptions apply to extend hours",
        counter_arguments=["Adverse conditions require unforeseeable event (not traffic)", "Ag exemption limited to 150 air-miles, planting/harvest only", "Short-haul must meet all 4 criteria"],
        resolution_strategy="Review ELD data, verify exemption eligibility, confirm 30-minute break compliance, check restart periods",
        entity_scope="Interstate CMV property carriers (passengers have different rules under 395.5)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Bright-line hour limits; exemptions require documentation of qualifying conditions",
        controlling_precedent="49 CFR 395 mandatory; violations subject to civil penalties and out-of-service orders"
    ),
    DoctrineBlock(
        topic="ELD Mandate 49 CFR 395.8",
        keywords=["ELD", "electronic logging device", "AOBRD", "395.8", "e-log"],
        conclusion_template=[
            "ELD mandate under 49 CFR 395.8 requires electronic logging devices for most CMVs as of December 2017.",
            "Exceptions: pre-2000 model year trucks, driveaway-towaway, short-haul (100 air-mile), 8-day-or-fewer drivers.",
            "AOBRDs grandfathered until December 2019; all new must be registered ELDs."
        ],
        reasoning_framework="""
49 CFR 395.8(a) mandates ELDs for CMVs required to keep records of duty status (RODS). Effective December 18, 2017.
ELD must be registered with FMCSA, self-certified by manufacturer (395.16). Exceptions (395.8(a)): pre-2000 model year,
driveaway-towaway operations, drivers using short-haul 395.1(e) exception, drivers keeping RODS 8 days or fewer per
30-day period. AOBRD (Automatic On-Board Recording Device) grandfathered if installed before Dec 18, 2017, until
Dec 16, 2019 (395.8(a)(1)(iii)). ELD must automatically record engine hours, vehicle motion, miles driven, location
(395.24). Driver edits must be annotated and approved. Malfunction requires notation and paper logs within 8 days
(395.34). Harassment policy required: carrier cannot use ELD to harass drivers (395.30(c)). Violations: driving with
malfunctioning ELD beyond 8 days, tampering with ELD, failing to transfer records upon request.
        """,
        key_factors=["Vehicle model year", "Operation type", "Short-haul eligibility", "8-day rule", "ELD malfunction procedures"],
        primary_authority=["49 CFR 395.8 ELD mandate", "49 CFR 395.16 Registration", "49 CFR 395.24 Data elements", "49 CFR 395.34 Malfunction"],
        burden_holder="Motor Carrier and Driver",
        adversary_position="Pre-2000 truck or short-haul exemption applies, no ELD needed",
        counter_arguments=["Pre-2000 exemption requires model year verification", "Short-haul requires 100 air-mile, 12-hour, return daily", "8-day rule requires careful counting per 30-day period"],
        resolution_strategy="Verify vehicle VIN for model year, confirm daily operations meet short-haul, review ELD registration on FMCSA list, check malfunction documentation",
        entity_scope="Interstate and Intrastate CMV operators subject to HOS",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ELD requirement is bright-line with narrow exceptions; malfunction procedures strict",
        controlling_precedent="49 CFR 395.8 mandatory; Owner-Operator Independent Drivers Assn v. FMCSA upheld ELD mandate (7th Cir. 2016)"
    ),
    DoctrineBlock(
        topic="Drug and Alcohol Testing 49 CFR 382",
        keywords=["drug test", "alcohol test", "DOT testing", "382", "random", "post-accident"],
        conclusion_template=[
            "49 CFR Part 382 requires motor carriers to conduct pre-employment, random, post-accident, reasonable suspicion, and return-to-duty drug/alcohol testing.",
            "Random testing: 50% of average drivers annually for drugs, 10% for alcohol.",
            "Post-accident testing required within 32 hours if fatality, injury, or disabling damage with citation."
        ],
        reasoning_framework="""
49 CFR 382.301: Pre-employment drug test required before first drive. 382.305: Random testing at 50% annual rate (drugs),
10% (alcohol), selections must be unpredictable. 382.303: Post-accident testing if: (1) fatality, (2) bodily injury
with immediate medical treatment away from scene, (3) disabling damage to any vehicle requiring tow, and driver
receives citation within 8 hours or citation not known within 8 hours. Alcohol within 8 hours, drugs within 32 hours.
382.307: Reasonable suspicion testing if trained supervisor observes behavior/appearance indicating drug/alcohol use.
382.309: Return-to-duty and follow-up after violation, evaluated by SAE (Substance Abuse Professional). 382.213:
Driver cannot perform safety-sensitive functions with 0.04% or higher BAC. 382.601: Consortium/third-party testing
allowed. MRO (Medical Review Officer) must verify positive drug tests (49 CFR 40). Refusal to test = positive test.
        """,
        key_factors=["Test type trigger", "Timing (8hr alcohol, 32hr drug)", "Citation for post-accident", "BAC threshold 0.04%", "SAE return process"],
        primary_authority=["49 CFR Part 382", "49 CFR Part 40 Testing Procedures", "382.303 Post-accident", "382.213 BAC limit"],
        burden_holder="Motor Carrier (testing programs), Driver (compliance)",
        adversary_position="Post-accident test not required if no citation or beyond time window",
        counter_arguments=["Citation requirement waived if LEO unavailable or delays beyond 8 hours", "Fatality requires test regardless of citation", "Reasonable suspicion requires trained supervisor documentation"],
        resolution_strategy="Verify supervisor training, document post-accident timelines and citations, confirm MRO verification, review random selection process for true randomness",
        entity_scope="All CDL drivers performing safety-sensitive functions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Testing triggers are well-defined; reasonable suspicion requires contemporaneous documentation",
        controlling_precedent="49 CFR 382 mandatory; Skinner v. Railway Labor Executives upheld random drug testing (SCOTUS 1989)"
    ),
    DoctrineBlock(
        topic="Vehicle Inspection and Maintenance 49 CFR 396",
        keywords=["inspection", "maintenance", "DVIR", "396", "annual inspection", "brake"],
        conclusion_template=[
            "49 CFR Part 396 requires motor carriers to systematically inspect, repair, and maintain all CMVs.",
            "Annual inspection required; inspection report must be completed and retained for 14 months (396.21).",
            "Driver Vehicle Inspection Report (DVIR) required if defects found; carrier must certify repairs (396.11)."
        ],
        reasoning_framework="""
49 CFR 396.3: Carrier must inspect, repair, maintain CMVs to ensure safe operational condition. 396.11: DVIR required
at end of each day's work if driver discovers defect. Driver signs, carrier reviews within 24 hours, certifies repairs
before next dispatch. 396.17: Maintenance records must include ID of vehicle, date, nature of repairs, who performed.
Retain for 1 year + 6 months after vehicle leaves control. 396.21: Annual inspection required, documented on form per
Appendix A or B. Inspection must cover brake system, coupling devices, exhaust, fuel system, lighting, safe loading,
steering, suspension, tires, wheels, windshield. Inspector must be qualified. Inspection report retained 14 months.
396.9(c): Brake standard - 20% service brake on each axle, parking brake holds 20% grade, no audible air leaks.
Out-of-service if critical defects (e.g., brake failure, steering, tires flat/exposed cords).
        """,
        key_factors=["Annual inspection timing", "DVIR defect reporting", "Repair certification before dispatch", "Brake performance standards", "Inspector qualifications"],
        primary_authority=["49 CFR Part 396", "396.11 DVIR", "396.21 Annual inspection", "396.9 Brake standards"],
        burden_holder="Motor Carrier (inspection/maintenance), Driver (DVIR reporting)",
        adversary_position="Minor defects don't require DVIR or can be deferred to annual inspection",
        counter_arguments=["DVIR required only if defect affects safe operation (396.11)", "Annual inspection mandatory regardless of defect presence", "Out-of-service criteria 396.9(c) are strict"],
        resolution_strategy="Review DVIR logs, verify annual inspection dates and inspector qualifications, test brake performance, document repair completion",
        entity_scope="All motor carriers operating CMVs in interstate commerce",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Annual inspection and DVIR bright-line; brake standards measurable; critical defects trigger out-of-service",
        controlling_precedent="49 CFR 396 mandatory; violations subject to civil penalties and out-of-service orders"
    ),
    DoctrineBlock(
        topic="Weight Limits and Bridge Formula 23 USC 127",
        keywords=["weight limit", "bridge formula", "axle weight", "80,000", "federal weight", "23 USC 127"],
        conclusion_template=[
            "Federal weight limit on Interstate highways is 80,000 lbs gross vehicle weight under 23 USC 127.",
            "Axle limits: 20,000 lbs single axle, 34,000 lbs tandem axle; Bridge Formula determines spacing.",
            "States may grant permits for overweight loads; violations subject to fines and load restrictions."
        ],
        reasoning_framework="""
23 USC 127(a): 80,000 lbs maximum gross weight on Interstate highways. Single axle max 20,000 lbs, tandem 34,000 lbs.
Bridge Formula (127(a)): W = 500[(LN/(N-1)) + 12N + 36] where W=max weight (lbs), L=distance (ft) between extremes of
axle group, N=number of axles. Formula prevents damage to bridges by distributing weight. States enforce via weigh
stations and portable scales. Overweight penalties vary by state, often $0.01-$0.10 per pound over, plus potential
load reduction/escort requirements. Special permits available for divisible loads (can be broken down) vs indivisible
(single piece equipment). Grandfather rights: some states allow higher weights on non-Interstate roads (e.g., Michigan
164,000 lbs on designated routes). Federal-aid highways must comply with federal limits or risk funding loss.
        """,
        key_factors=["Gross vehicle weight", "Axle spacing", "Single vs tandem axles", "Interstate vs state highway", "Permit requirements"],
        primary_authority=["23 USC 127", "Bridge Formula 23 USC 127(a)", "State weight laws"],
        burden_holder="Motor Carrier and Driver",
        adversary_position="State permit allows higher weight; grandfather routes exempt from federal limits",
        counter_arguments=["Permits require specific route and conditions", "Grandfather routes limited to pre-1982 designated roads", "Interstate system strictly 80K federal limit"],
        resolution_strategy="Weigh vehicle, calculate Bridge Formula compliance, verify permit validity and route restrictions, check state-specific regulations",
        entity_scope="All CMVs on federal-aid highways",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="80K federal limit bright-line on Interstates; Bridge Formula requires calculation; state permits fact-specific",
        controlling_precedent="23 USC 127 mandatory; states risk federal highway funding if non-compliant"
    ),
    DoctrineBlock(
        topic="Oversize Permits and Routing",
        keywords=["oversize", "overweight", "permit", "wide load", "pilot car", "superload"],
        conclusion_template=[
            "Oversize/overweight (OS/OW) loads require state-issued permits specifying route, time, and escort requirements.",
            "Typical thresholds: over 8.5 ft wide, 13.5-14 ft high, 53 ft long, or state weight limits.",
            "Pilot car/escort required for loads exceeding width (12 ft+), length (100 ft+), or at state discretion."
        ],
        reasoning_framework="""
Each state issues OS/OW permits under own regulations. Common dimensions: width over 8.5 ft (some states 8.0 ft),
height over 13.5-14.0 ft (varies), length over 53 ft (varies). Single-trip vs annual permits. Route surveys required
for superloads (over 16 ft wide, 16 ft high, 200K+ lbs). Pilot car requirements: front for 12-14 ft wide, front+rear
for 14+ ft or 100+ ft long. Flags (red/orange) required on protrusions. Travel time restrictions (daylight only,
no weekends/holidays for wide loads). Insurance requirements: $1M+ liability. Multi-state permits: coordination via
reciprocity agreements or individual state permits. Notification to utilities, DOT, law enforcement for superloads.
Cost varies: $15-$500+ per permit depending on size, weight, distance. Violations: fines, impoundment, load reduction.
        """,
        key_factors=["Load dimensions", "Weight", "Route restrictions", "Pilot car requirements", "Travel time windows", "Multi-state coordination"],
        primary_authority=["State DOT permit regulations", "FHWA Compilation of OS/OW Regulations", "State-specific statutes"],
        burden_holder="Motor Carrier (permit application, compliance)",
        adversary_position="Load within legal limits, no permit needed; annual permit covers all routes",
        counter_arguments=["Annual permits often restricted to specific routes and dimensions", "Legal limits vary by state and road type", "Enforcement via weigh stations and portable checks"],
        resolution_strategy="Measure load, apply for permits in all states on route, verify pilot car certifications, confirm travel time and route compliance, maintain permits on board",
        entity_scope="All OS/OW loads on public highways",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="State regulations vary widely; permit conditions are contract terms; route/time restrictions fact-specific",
        controlling_precedent="State authority over highways; permits are privileges, not rights"
    ),
    DoctrineBlock(
        topic="Hazmat Transportation 49 CFR 171-180 PHMSA",
        keywords=["hazmat", "hazardous materials", "PHMSA", "placards", "HM-181", "171-180"],
        conclusion_template=[
            "49 CFR Parts 171-180 regulate hazmat transportation: classification, packaging, labeling, placarding, and documentation.",
            "Hazmat endorsement required on CDL for placarded quantities (49 CFR 383.93).",
            "Shipping papers must include proper shipping name, hazard class, ID number, packing group (172.202)."
        ],
        reasoning_framework="""
49 CFR 171: Applicability and definitions. Hazmat = substance on Hazardous Materials Table (49 CFR 172.101) posing
unreasonable risk. 172.101: 3,600+ materials listed with class, packing group, labels, packaging. 9 hazard classes:
explosives, gases, flammable liquids, flammable solids, oxidizers, toxic/infectious, radioactive, corrosives,
miscellaneous. 172.200: Marking and labeling per material. 172.504: Placarding if >1,001 lbs aggregate gross weight
or any quantity of certain materials (e.g., explosives, radioactive). 4 placards on vehicle (front, rear, sides).
172.202: Shipping paper must include: proper shipping name, hazard class, ID number (UN/NA), packing group, quantity.
Emergency response info required (172.602). Hazmat employee training every 3 years (172.704). Security plan required
for Tier 1 (high-risk) materials (172.800). 173: Packaging must meet performance standards, tested/certified. 177:
Carriage by public highway (loading, segregation, attendance). 49 CFR 385.403: Safety permit required for placarded
or bulk hazmat carriers. PHMSA enforces; violations subject to civil penalties up to $96,624 per violation, criminal
for knowing violations causing death.
        """,
        key_factors=["Material classification", "Quantity (placarded threshold)", "Proper shipping name", "Packaging standards", "Training certification", "Security plan (Tier 1)"],
        primary_authority=["49 CFR Parts 171-180", "172.101 Hazmat Table", "172.504 Placarding", "172.702 Training", "385.403 Safety permit"],
        burden_holder="Shipper (classification, packaging, shipping papers), Carrier (placarding, training, transport), Driver (CDL endorsement)",
        adversary_position="Material not listed on Hazmat Table, or below placarded quantity, no endorsement needed",
        counter_arguments=["Residue shipments still require placards (172.504)", "Some materials require placards at any quantity", "ORM-D consumer commodity exceptions limited (173.155)"],
        resolution_strategy="Check 172.101 Table, verify packaging certifications, review shipping papers for all 5 elements, confirm driver hazmat endorsement and training dates, inspect placards",
        entity_scope="All shippers and carriers of hazardous materials",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Classification and placarding bright-line; packaging standards technical; training every 3 years strict",
        controlling_precedent="49 CFR 171-180 mandatory; PHMSA jurisdiction; severe civil and criminal penalties for violations"
    ),
    DoctrineBlock(
        topic="Railroad Safety FRA 49 CFR 213-243",
        keywords=["FRA", "railroad", "track safety", "49 CFR 213", "signal systems", "grade crossing"],
        conclusion_template=[
            "FRA 49 CFR Part 213 sets track safety standards with 9 track classes based on speed limits.",
            "49 CFR Part 234 regulates highway-rail grade crossings; active warnings required for high-speed/volume.",
            "49 CFR Part 240 requires locomotive engineer certification; Part 242 conductor certification."
        ],
        reasoning_framework="""
49 CFR 213: Track Safety Standards. Class 1 (10 mph freight, 15 passenger) to Class 9 (200 mph). Inspection frequency:
Class 1-2 weekly, Class 3-5 twice weekly to weekly, Class 6+ varies. Track geometry, rail wear, joint bars, crossties,
ballast, drainage all specified. 213.109: Minimum number of ties per 39-ft rail: Class 1 (5), Class 2 (8), Class 3+ (12).
Rail wear limits (213.103), gauge (213.63). 49 CFR 214: Roadway worker protection (on-track safety). 49 CFR 218:
Railroad operating practices (blue signal protection). 49 CFR 234: Grade crossing signal systems. Active warnings
(gates, lights) required when product of trains/day × highway vehicles/day exceeds threshold or speed >60 mph.
Crossing surface within 2 ft of rail top (234.207). 49 CFR 240: Engineer certification requires training, testing,
vision/hearing, no certain violations (DUI, moving violations). 49 CFR 242: Conductor certification. PTC (Positive
Train Control) mandated on passenger/high-hazmat lines by 49 USC 20157. FRA enforces via track inspections, audits.
        """,
        key_factors=["Track class and speed limit", "Inspection frequency", "Tie count and condition", "Grade crossing traffic volume", "Engineer/conductor certification"],
        primary_authority=["49 CFR Part 213 Track", "49 CFR Part 234 Grade Crossings", "49 CFR 240 Engineers", "49 CFR 242 Conductors", "49 USC 20157 PTC"],
        burden_holder="Railroad (track maintenance, crossing safety, employee certification)",
        adversary_position="Track meets minimum standards for lower class, downgrade speed limits to reduce requirements",
        counter_arguments=["Speed downgrade reduces service and revenue", "Grade crossing improvements expensive, prioritized by risk", "PTC mandate multi-billion dollar cost but safety benefit"],
        resolution_strategy="Inspect track per 213, test crossing warning systems, verify employee certifications, review FRA inspection reports, assess PTC implementation",
        entity_scope="All railroads subject to FRA jurisdiction",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Track standards measurable; grade crossing thresholds bright-line; certification procedural",
        controlling_precedent="49 CFR 213-243 mandatory; FRA jurisdiction over railroad safety; PTC mandate federally imposed"
    ),
    DoctrineBlock(
        topic="Aviation FAA 14 CFR Part 91 General Operating",
        keywords=["FAA", "14 CFR", "Part 91", "VFR", "IFR", "airspace", "pilot certificate"],
        conclusion_template=[
            "14 CFR Part 91 governs general aviation operations: pilot certification, aircraft airworthiness, flight rules.",
            "VFR weather minimums: 3 SM visibility, 500 ft below/1000 above/2000 horizontal from clouds in Class E.",
            "IFR requires instrument rating, current IPC or 6 approaches/holds in 6 months, filed flight plan."
        ],
        reasoning_framework="""
14 CFR 91.3: Pilot in command responsible for operation. 91.7: Aircraft must be airworthy (annual inspection, 100-hr
if for hire). 91.103: Preflight action (weather, NOTAMs, fuel, alternates). 91.155: VFR weather minimums vary by
airspace class: Class B (3 SM, clear of clouds), Class C/D/E (3 SM, 500/1000/2000), Class G day (1 SM, clear of clouds
below 1200 AGL). 91.167: IFR fuel requirement (destination + approach + 45 min). 91.175: IFR approach minimums per
instrument approach chart. 91.205: Required equipment VFR day (ATOMATOFLAMES mnemonic), VFR night (add position lights,
landing light if for hire), IFR (add gyros, radios, clock). 91.211: Oxygen above 12,500 ft. 91.215: Mode C transponder
in Class A/B/C and above 10,000 MSL. 91.303: Aerobatic flight restrictions (not over congested, below 1500 AGL, <3 SM).
91.409: Annual inspection required. Pilot certificates: student, sport, recreational, private, commercial, ATP. Medical:
Class 1 (ATP), Class 2 (commercial), Class 3 (private), BasicMed alternative.
        """,
        key_factors=["Airspace class", "Weather conditions", "Pilot certification and currency", "Aircraft inspections", "Required equipment"],
        primary_authority=["14 CFR Part 91", "91.155 VFR minimums", "91.167/175 IFR", "91.409 Inspections", "61.51/.57 Pilot currency"],
        burden_holder="Pilot in Command (91.3)",
        adversary_position="Special VFR clearance allows operations below VFR minimums in controlled airspace (91.157)",
        counter_arguments=["SVFR requires clearance and 1 SM visibility", "Night SVFR requires instrument rating", "Uncontrolled airspace (Class G) has lower minimums"],
        resolution_strategy="Check weather (METARs, TAFs), verify pilot certificates and medical, review logbook for currency (90-day landings, IFR approaches), inspect aircraft logs for annual/100-hr",
        entity_scope="All civil aviation in the United States",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="VFR/IFR minimums bright-line; airworthiness inspection dates clear; pilot currency requires logbook review",
        controlling_precedent="14 CFR Part 91 mandatory; FAA jurisdiction; violations subject to certificate suspension/revocation and civil penalties"
    ),
    DoctrineBlock(
        topic="FAA Part 121 Air Carrier Operations",
        keywords=["Part 121", "air carrier", "scheduled airline", "OpSpecs", "MEL", "dispatch"],
        conclusion_template=[
            "14 CFR Part 121 governs scheduled air carriers with 10+ seats: training, maintenance, dispatch, OpSpecs.",
            "OpSpecs (Operations Specifications) authorize routes, aircraft types, special operations (ETOPS, Cat II/III).",
            "MEL (Minimum Equipment List) allows dispatch with inoperative items under approved conditions."
        ],
        reasoning_framework="""
14 CFR Part 121: Scheduled air carriers (airlines). Requires Air Carrier Certificate and OpSpecs from FAA. 121.135:
Manual requirements (General, Flight Ops, Aircraft Ops, Maintenance). 121.400-121.453: Flight crew qualifications,
training, checking (initial, recurrent, line checks). 121.471: Flight time limits (8/9 hours flight time, augmented
crew for longer). 121.481: Flight attendant requirements (1 per 50+ seats). 121.500: Dispatch centers required;
dispatcher shares responsibility with PIC for flight planning, release, monitoring. 121.619: Weather minimums for
takeoff/landing. 121.628: Preflight fuel (destination + alternate + 45 min + 15% contingency or 10 min holding).
121.700-121.715: Maintenance programs (continuous airworthiness, progressive/overnight checks, sampling inspections).
MEL approved per 121.628: allows dispatch with inop items if compensating procedures/limitations met. OpSpecs Part C:
Aircraft authorization. Part D: En route/area operations. Part E: Special ops (ETOPS, RNP, RVSM). ETOPS (Extended
Operations) allows 2-engine flights >60 min from alternate. Cat II/III ILS approaches to lower minimums.
        """,
        key_factors=["OpSpecs authorizations", "Crew training/currency", "Dispatch release", "MEL compliance", "Maintenance program", "Fuel planning"],
        primary_authority=["14 CFR Part 121", "121.135 Manuals", "121.400 Training", "121.628 MEL", "OpSpecs", "ETOPS 121 Appendix P"],
        burden_holder="Air Carrier (certificate holder)",
        adversary_position="MEL allows flight with inoperative systems; dispatcher authorized release despite weather",
        counter_arguments=["MEL requires FAA approval and specific procedures", "Dispatcher must verify weather meets minimums at ETA", "OpSpecs strictly limit authorized operations"],
        resolution_strategy="Review OpSpecs for authorization, verify crew training records, confirm dispatch release and fuel, check MEL for inop item approval, audit maintenance program",
        entity_scope="Scheduled air carriers operating under Part 121",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="OpSpecs and MEL approvals documented; training/checking records auditable; fuel rules bright-line",
        controlling_precedent="14 CFR Part 121 mandatory; FAA enforcement via inspections, audits, certificate actions"
    ),
    DoctrineBlock(
        topic="USDOT Number and Operating Authority",
        keywords=["USDOT number", "MC number", "operating authority", "FMCSA registration", "for-hire"],
        conclusion_template=[
            "USDOT number required for all CMVs in interstate commerce; MC number for for-hire carriers.",
            "Must apply via FMCSA Unified Registration System (URS); biennial updates required.",
            "New entrant safety audit within 18 months; satisfactory rating needed to continue operations."
        ],
        reasoning_framework="""
49 CFR 390.201: USDOT number required for interstate CMVs (GVWR 10,001+ lbs or hazmat placarded). Intrastate in many
states also require USDOT number per state law. Apply at fmcsa.dot.gov/registration. MC (Motor Carrier) number
required for for-hire carriers transporting property or passengers (49 USC 13902). FF (Freight Forwarder) number for
freight forwarders. 49 CFR 390.19: Biennial update of MCS-150 form required; failure results in deactivation.
49 CFR 385.101-385.119: New entrant program. Safety audit within 18 months of registration. If fail audit, must pass
within 45 days or registration revoked. Must maintain $750K cargo insurance (for-hire property), $5M passenger insurance.
BOC-3 (Blanket of Coverage) designating process agents in all states required (49 CFR 366.4). Display USDOT number on
both sides of CMV in 2-inch lettering, contrasting color (390.21). Operating without authority subject to $25,000+
civil penalties and out-of-service.
        """,
        key_factors=["Interstate vs intrastate", "For-hire vs private", "GVWR/hazmat triggers", "Biennial update", "Safety audit compliance", "Insurance amounts"],
        primary_authority=["49 CFR 390.201 USDOT", "49 USC 13902 MC authority", "49 CFR 385.101 New entrant", "49 CFR 366.4 BOC-3", "49 CFR 390.21 Marking"],
        burden_holder="Motor Carrier",
        adversary_position="Private carrier exempt from MC number; intrastate only, no USDOT needed",
        counter_arguments=["USDOT required even for private carriers in interstate", "Intrastate requirements vary by state", "Any interstate movement triggers federal registration"],
        resolution_strategy="Verify USDOT/MC numbers on FMCSA SAFER database, confirm biennial update dates, review insurance certificates, check BOC-3 filing, inspect vehicle markings",
        entity_scope="All CMV motor carriers in interstate commerce; state-specific for intrastate",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="USDOT number registration bright-line; for-hire definition clear; new entrant audit pass/fail documented",
        controlling_precedent="49 CFR 390/385 mandatory; FMCSA enforcement; severe penalties for operating without authority"
    ),
    DoctrineBlock(
        topic="State DOT Compliance and UCR",
        keywords=["state DOT", "UCR", "unified carrier registration", "intrastate", "state permits"],
        conclusion_template=[
            "States require additional permits, UCR registration, fuel tax reporting (IFTA), and state-specific regulations.",
            "UCR (Unified Carrier Registration) annual fee based on fleet size; required for interstate carriers.",
            "IFTA (International Fuel Tax Agreement) license required for multi-state operations; quarterly reporting."
        ],
        reasoning_framework="""
UCR (49 USC 14504a): Annual registration fee for interstate carriers, brokers, freight forwarders. Fee tiers based on
fleet size (0-2 vehicles = $76, 3-5 = $229, etc., up to 1000+ = $87,988 in 2024). Base state collects, distributes to
participating states. Must register by Jan 1; grace period to Jan 31. Proof of UCR required; fines for non-compliance.
IFTA (International Fuel Tax Agreement): Apportions fuel taxes among states/provinces based on miles driven. Quarterly
reports due last day of month after quarter (Apr 30, Jul 31, Oct 31, Jan 31). License displays decals on qualified
motor vehicles (QMV: 2+ axles, GVWR 26,001+ lbs or 3+ axles regardless of weight). Non-compliant penalties and interest.
State intrastate permits: Each state has own requirements for intrastate carriers (e.g., California MCP number, Texas
TxDMV number). Some states require drug/alcohol testing consortium registration, vehicle registration/titling, oversize
permits separately. States may have stricter HOS, weight, inspection rules than federal. Check each state DOT website.
        """,
        key_factors=["Fleet size (UCR tier)", "Multi-state operations (IFTA)", "Intrastate vs interstate", "State-specific permits", "Quarterly reporting deadlines"],
        primary_authority=["49 USC 14504a UCR", "IFTA Articles of Agreement", "State DOT regulations"],
        burden_holder="Motor Carrier",
        adversary_position="Single-state operation, no UCR or IFTA needed; only federal USDOT required",
        counter_arguments=["Interstate commerce requires UCR even if 1 vehicle", "IFTA required once operating in 2+ jurisdictions", "States enforce intrastate permits strictly"],
        resolution_strategy="Verify UCR registration and payment, review IFTA license and quarterly reports, check state-specific permits for all operating states, confirm fuel tax compliance",
        entity_scope="All interstate carriers (UCR); multi-state carriers (IFTA); state carriers per state law",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="UCR and IFTA requirements clear but multi-state complexity high; state intrastate rules vary widely",
        controlling_precedent="Federal UCR and IFTA agreements; state enforcement via roadside inspections and audits"
    ),
    DoctrineBlock(
        topic="CSA Safety Measurement System",
        keywords=["CSA", "SMS", "BASICs", "safety score", "intervention", "385.15"],
        conclusion_template=[
            "CSA (Compliance, Safety, Accountability) SMS tracks carrier safety via 7 BASICs (Behavior Analysis and Safety Improvement Categories).",
            "High BASIC percentiles trigger FMCSA interventions: warning letters, investigations, downgrade to Conditional/Unsatisfactory.",
            "Unsafe Driving, HOS Compliance, Driver Fitness, Controlled Substances/Alcohol, Vehicle Maintenance, Hazmat Compliance, Crash Indicator."
        ],
        reasoning_framework="""
CSA SMS (49 CFR 385.15): FMCSA's data-driven safety program. 7 BASICs: (1) Unsafe Driving, (2) HOS Compliance,
(3) Driver Fitness, (4) Controlled Substances/Alcohol, (5) Vehicle Maintenance, (6) Hazmat Compliance, (7) Crash
Indicator. Violations from roadside inspections, investigations, crashes assigned severity weights and time weights
(recent violations weighted higher). Percentile ranking vs peer group (similar carriers). Thresholds vary by BASIC and
carrier type. Intervention levels: Warning letter (65-79 percentile), Targeted investigation (80+), Cooperative Safety
Plan, Comprehensive onsite investigation. Safety rating: Satisfactory, Conditional (correctable deficiencies),
Unsatisfactory (imminent hazard, cease operations). DataQs process to challenge incorrect violations (30-day window).
Public display on FMCSA SAFER website (carrier snapshot). High scores impact insurance, customer contracts. Pre-employment
screening (PSP) reports show driver history. Points expire after 24 months.
        """,
        key_factors=["BASIC percentiles", "Violation severity and recency", "Intervention thresholds", "Safety rating", "DataQ challenges"],
        primary_authority=["49 CFR 385.15 CSA", "FMCSA SMS Methodology", "DataQs 49 CFR 386.12"],
        burden_holder="Motor Carrier (safety management)",
        adversary_position="Violations disputed via DataQs; carrier has corrective action plan to reduce scores",
        counter_arguments=["DataQs must be filed within 30 days of inspection", "Corrective action doesn't remove points, only prevents future violations", "Percentiles relative, not absolute"],
        resolution_strategy="Monitor BASIC scores monthly, file DataQs for incorrect violations, implement corrective actions (training, maintenance), review driver PSP reports pre-hire",
        entity_scope="All motor carriers with USDOT number",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="BASIC methodology complex; percentiles vs peers; intervention thresholds documented but safety rating determination fact-intensive",
        controlling_precedent="49 CFR 385.15; FMCSA SMS policy; DataQs administrative process; judicial review limited"
    ),
    DoctrineBlock(
        topic="Medical Certification 49 CFR 391.41-391.49",
        keywords=["medical certification", "DOT physical", "391.41", "diabetes", "vision", "hearing"],
        conclusion_template=[
            "CDL drivers must hold valid medical certificate per 49 CFR 391.41; exam every 2 years by certified medical examiner.",
            "Vision: 20/40 acuity each eye (with/without correction), 70-degree field each eye. Hearing: 5-ft forced whisper or audiometric.",
            "Diabetes: insulin-dependent requires exemption or intrastate-only; non-insulin controlled allowed."
        ],
        reasoning_framework="""
49 CFR 391.41: Physical qualifications. Medical exam required before first drive, every 2 years. Examiner must be
listed on FMCSA National Registry. 391.43: Standards: no loss of limb/impairment interfering with safe operation, no
condition likely to cause sudden incapacitation (epilepsy, heart attack risk), BP <140/90 (or 160/100 with 3-month
card if controlled), diabetes controlled without insulin (or exemption), vision 20/40 Snellen in each eye (corrected
or uncorrected), 70-degree peripheral in each eye, hearing 5-ft forced whisper or audiometric. 391.45: Diabetes on
insulin requires individual exemption from FFMCSA (391.64) or intrastate-only. Vision exemption available for one-eye
drivers (391.64). Sleep apnea: no specific regulation but examiners often require CPAP compliance if diagnosed.
391.49: Diabetes exemption program (sunset 2018, now individual determinations). Medical certificate on driver at all
times; copy to employer. Medical Examiner's Certificate (MEC) form MCSA-5876. Self-certification categories: Interstate
non-excepted (must have medical card), Intrastate non-excepted (state requirements), Excepted interstate/intrastate.
        """,
        key_factors=["Vision 20/40 each eye", "Hearing 5-ft whisper", "BP control", "Diabetes insulin use", "Examiner certification", "2-year expiration"],
        primary_authority=["49 CFR 391.41 Qualifications", "49 CFR 391.43 Standards", "49 CFR 391.45 Diabetes", "49 CFR 391.64 Exemptions"],
        burden_holder="Driver (obtain/maintain certificate), Examiner (perform exam), Carrier (verify on file)",
        adversary_position="Driver has medical condition but controlled, still qualifies; exemption process allows continued driving",
        counter_arguments=["Controlled conditions must meet standards (BP <160/100 max with 3-month card)", "Exemptions require individual FMCSA approval, time-consuming", "Sleep apnea lack of federal rule creates examiner discretion"],
        resolution_strategy="Verify medical certificate dates, check examiner on National Registry, review medical conditions vs 391.43 standards, confirm exemption if insulin-dependent",
        entity_scope="All CDL drivers requiring medical certification (non-excepted interstate/intrastate)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Vision/hearing standards bright-line; BP thresholds clear; diabetes insulin rule strict unless exemption; sleep apnea discretionary",
        controlling_precedent="49 CFR 391.41-391.49 mandatory; FMCSA medical examiner program enforced; exemptions available but limited"
    ),
    DoctrineBlock(
        topic="Cargo Securement 49 CFR 393.100-393.142",
        keywords=["cargo securement", "tie-down", "393.100", "working load limit", "WLL", "aggregate"],
        conclusion_template=[
            "49 CFR 393.100-393.142 requires cargo secured to prevent shifting, loss, leakage; aggregate WLL at least 50% of cargo weight.",
            "Tiedowns must be in good condition, proper WLL (1/2 marked or 50% if unmarked), edge protection if abrasion risk.",
            "Specific rules for logs, metal coils, paper rolls, concrete pipe, vehicles, heavy machinery, intermodal containers."
        ],
        reasoning_framework="""
49 CFR 393.100: Cargo must be secured to prevent forward/rearward/side-to-side/vertical movement. Performance criteria:
0.8g forward, 0.5g rearward/side. 393.102: Securement systems (tiedowns, dunnage, shoring bars, anchor points). Working
Load Limit (WLL): max load securement device can handle. Aggregate WLL of tiedowns must be at least 50% of cargo weight.
393.104: Anchor points on vehicle must be rated for WLL. 393.106: Tiedowns (chain, wire rope, webbing, cordage) must have
WLL marked or meet minimum unmarked WLL. Edge protection required if tiedown could be cut/abraded. 393.110: General
tiedown requirements: 1 tiedown for <=5 ft cargo, 2 for >5-10 ft, 1 additional per 10 ft beyond. Commodity-specific:
393.116 Logs (bunks, bolsters, stakes, 2+ tiedowns), 393.118 Metal coils (eyes vertical: prevent roll), 393.120 Paper
rolls, 393.122 Concrete pipe, 393.124 Intermodal containers (twist locks, chains if no integral securement), 393.126
Automobiles, 393.128 Heavy machinery, 393.130 Flattened/crushed vehicles, 393.132 Roll-on/roll-off containers. CVSA
out-of-service criteria: <50% WLL, damaged/improper securement, cargo shifted.
        """,
        key_factors=["Aggregate WLL 50% of cargo weight", "Tiedown condition and rating", "Edge protection", "Commodity-specific rules", "Number of tiedowns per length"],
        primary_authority=["49 CFR Part 393 Subpart I", "393.100 Performance criteria", "393.102 WLL", "393.116-393.136 Commodity rules"],
        burden_holder="Driver and Motor Carrier",
        adversary_position="Cargo hasn't shifted, securement adequate; unmarked tiedowns assumed sufficient WLL",
        counter_arguments=["Unmarked tiedowns have minimum WLL per material (chain=1/4 diameter, wire=1/8, etc.)", "CVSA out-of-service if WLL deficient", "Commodity rules prescriptive, not performance-based"],
        resolution_strategy="Calculate cargo weight, verify aggregate WLL (marked or per 393.106 table), inspect tiedowns for damage, confirm edge protection, count tiedowns per cargo length, review commodity-specific rules",
        entity_scope="All CMVs transporting cargo on public highways",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="WLL calculation bright-line (50% cargo weight); tiedown condition inspectable; commodity rules specific but require application to facts",
        controlling_precedent="49 CFR 393.100-393.142 mandatory; CVSA enforcement; cargo securement violations leading cause of out-of-service"
    ),
    DoctrineBlock(
        topic="Insurance and Financial Responsibility 49 CFR 387",
        keywords=["insurance", "387", "BMC-91", "MCS-90", "$750K", "financial responsibility"],
        conclusion_template=[
            "49 CFR Part 387 requires minimum insurance: $750K for-hire property, $5M passengers 16+, $1.5M oil/hazmat.",
            "Form BMC-91X or MCS-90 endorsement required, filed with FMCSA; 30-day notice for cancellation.",
            "Self-insurance and surety bonds allowed if approved by FMCSA; aggregate limit must meet minimums."
        ],
        reasoning_framework="""
49 CFR 387.9: For-hire property carriers require $750K minimum (non-hazmat), $5M if transporting hazmat in bulk or
quantities requiring placarding. For-hire passenger carriers: $1.5M (vehicles 16+ passengers), $5M (seating 16+).
Private carriers (non-for-hire) not subject to 387 but state laws may impose minimums. 387.13: Forms of security:
insurance, surety bond, self-insurance (if approved). BMC-91 (property), BMC-90 (passenger), MCS-90 (endorsement on
commercial policy), BMC-91X (property broker $75K). Form filed electronically with FMCSA. 387.15: Surety bonds as
alternative. 387.17: Self-insurance requires FMCSA approval, net worth/liquidity requirements. 387.307: 30-day notice
for cancellation; carrier must cease operations or obtain replacement. Aggregate limit must cover all potential claims
simultaneously. Leased equipment: both lessor and lessee must have insurance, non-trucking liability if lessor. State
minimums may exceed federal (e.g., Texas $350K intrastate). Proof of insurance: OP-1 filing for interstate authority.
        """,
        key_factors=["Cargo type (hazmat/non-hazmat)", "For-hire vs private", "Passenger capacity", "Aggregate limits", "Form filing", "30-day cancellation notice"],
        primary_authority=["49 CFR Part 387", "387.9 Minimum levels", "387.13 Forms", "387.307 Cancellation notice"],
        burden_holder="Motor Carrier (maintain insurance), Insurer (file forms, provide notice)",
        adversary_position="State minimum sufficient for intrastate; private carrier exempt from federal insurance",
        counter_arguments=["Federal minimums apply only to interstate for-hire; states may require insurance for private/intrastate", "Inadequate insurance voids operating authority"],
        resolution_strategy="Verify insurance certificate amounts, confirm BMC-91/MCS-90 on file with FMCSA, check cargo type for correct minimum, review lease agreements for coverage gaps",
        entity_scope="Interstate for-hire carriers; state-specific for intrastate",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Minimum amounts bright-line; form filing procedural; aggregate limit interpretation fact-specific for multiple claims",
        controlling_precedent="49 CFR 387 mandatory; inadequate insurance results in authority revocation; MCS-90 endorsement creates direct federal cause of action"
    ),
    DoctrineBlock(
        topic="Roadside Inspection Levels and CVSA",
        keywords=["roadside inspection", "CVSA", "Level I", "Level II", "out-of-service", "BASIC"],
        conclusion_template=[
            "CVSA (Commercial Vehicle Safety Alliance) roadside inspections come in 6 levels; Level I most comprehensive (37-step).",
            "Out-of-service (OOS) violations require immediate correction before continuing; driver/vehicle placed OOS.",
            "Inspection results feed CSA BASIC scores; violations assigned severity weights."
        ],
        reasoning_framework="""
CVSA inspection levels: Level I (North American Standard, 37-step walkaround, driver/vehicle/cargo), Level II
(walkaround, driver/vehicle, less detailed), Level III (driver only, credentials/logbook), Level IV (special inspection,
one-time exam), Level V (vehicle only, no driver), Level VI (enhanced NAS, radioactive/bulk liquid materials). OOS
criteria (CVSA handbook): Critical violations require immediate correction. Driver OOS: no valid CDL, medical card
expired, HOS violation, BAC 0.04+, drugs. Vehicle OOS: brake defects (<20% effectiveness), tire flat/exposed cords,
steering defects, coupling devices loose, lighting inoperative, hazmat placard missing/wrong. Cargo OOS: securement
<50% WLL, shifted load. OOS order binds driver/carrier; moving vehicle subject to penalties. Inspection reports sent
to FMCSA, entered into Motor Carrier Management Information System (MCMIS), feed CSA BASIC scores. Violations assigned
severity 1-10, time weight (recent=higher). Carrier receives inspection report copy; 30-day window to file DataQ
challenge. Decal issued if Level I/II passed with no critical violations. Inspection frequency: weigh stations, mobile
units, saturation patrols, targeted carriers (high BASIC).
        """,
        key_factors=["Inspection level", "OOS criteria met", "Violation severity", "Time to correct", "DataQ filing deadline"],
        primary_authority=["CVSA Out-of-Service Criteria", "49 CFR 396.9 OOS vehicle", "49 CFR 392.5 OOS driver", "FMCSA MCMIS database"],
        burden_holder="Driver (compliance during inspection), Carrier (correct violations, challenge via DataQ)",
        adversary_position="Violation not severe enough for OOS; maintenance records show repair attempted",
        counter_arguments=["OOS criteria specific and published; inspector discretion limited", "Maintenance records don't override current condition", "DataQ process available but must file within 30 days"],
        resolution_strategy="Review CVSA OOS criteria for cited violations, verify inspector certification, document corrective actions, file DataQ if inspection error, monitor CSA impact",
        entity_scope="All CMVs subject to roadside inspections",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="OOS criteria bright-line for most violations; inspector judgment on some items (e.g., 'imminent hazard'); DataQ process administrative",
        controlling_precedent="CVSA OOS criteria adopted by reference in federal regulations; inspector authority under 49 CFR 390.15; DataQ process 49 CFR 386.12"
    ),
    DoctrineBlock(
        topic="Wireless Communication Prohibition 49 CFR 392.82",
        keywords=["texting", "cell phone", "handheld", "392.82", "distracted driving"],
        conclusion_template=[
            "49 CFR 392.82 prohibits texting while driving CMV; 49 CFR 392.80 prohibits handheld mobile phone use.",
            "Texting = manually entering alphanumeric text, reading, sending. Handheld = holding phone to make call.",
            "Violations subject to $2,750+ driver fine, $11,000+ carrier fine, disqualification on repeat offenses."
        ],
        reasoning_framework="""
49 CFR 392.82: Texting while driving prohibited. Texting defined as manually entering alphanumeric text, or reading
text (emails, SMS, instant messaging, web browsing) on electronic device. Applies while CMV in motion. Exceptions:
911 emergency, dispatch to relay safety information if truck stopped and gear shifted to park/neutral. Violation =
driver $2,750 civil penalty, carrier $11,000 if allows/requires. 49 CFR 383.51: Multiple texting violations result
in CDL disqualification (2 within 3 years = 60 days, 3 = 120 days). 49 CFR 392.80: Handheld mobile phone use while
driving prohibited. Use = holding phone to conduct voice communication. Hands-free allowed (Bluetooth, earpiece,
speakerphone) if single button press to activate. Dialing by pressing single button allowed (speed dial, voice command).
Multi-step dialing prohibited. Mounting device within reach allowed. Same penalties as texting. State laws may be
stricter. Distracted driving leading cause of CMV crashes. FMCSA enforcement via roadside, witness reports, post-crash.
        """,
        key_factors=["Vehicle in motion", "Manually entering/reading text", "Holding phone vs hands-free", "Single button press limit", "Repeat violations"],
        primary_authority=["49 CFR 392.82 Texting", "49 CFR 392.80 Handheld phone", "49 CFR 383.51 Disqualification"],
        burden_holder="Driver (refrain from prohibited use), Carrier (policy and enforcement)",
        adversary_position="Phone mounted and hands-free, single-button activation, not 'use'; vehicle stopped at light, not 'driving'",
        counter_arguments=["Hands-free with single-button allowed per 392.80(b)", "Stopped at light still considered 'driving' unless gear in park", "Reading texts prohibited even if not responding"],
        resolution_strategy="Review phone records/data if crash involved, check carrier policy on cell phone use, witness statements, inspect phone mounting location",
        entity_scope="All CMV drivers subject to FMCSRs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Texting and handheld definitions bright-line; hands-free exceptions clear; 'in motion' vs 'stopped' at light gray area",
        controlling_precedent="49 CFR 392.80/392.82 mandatory; severe penalties; disqualification escalates with repeat violations"
    ),
    DoctrineBlock(
        topic="Broker Authority and Bond 49 CFR 371",
        keywords=["broker", "freight broker", "MC number", "$75K bond", "371", "BMC-84"],
        conclusion_template=[
            "Freight brokers require MC number, $75K surety bond or trust fund, and compliance with 49 CFR 371.",
            "Broker arranges transportation but does not provide equipment; unauthorized brokering illegal.",
            "Bond protects shippers/carriers from fraud; claims filed via FMCSA process."
        ],
        reasoning_framework="""
49 USC 13904: Broker authority required to arrange transportation as intermediary. Apply via FMCSA URS for MC number.
49 CFR 371.3: Broker must maintain $75K surety bond (BMC-84) or trust fund. Bond protects shippers and motor carriers
from broker fraud (non-payment, double brokering). 371.7: Bond must be continuous (no expiration) or provide 30-day
cancellation notice. 371.11: Broker must keep records of transactions 3 years. 371.13: Broker cannot provide
transportation without separate motor carrier authority. Unauthorized brokering = arranging transportation without
MC number, subject to $10K+ penalties. Double brokering = broker re-brokers load without shipper consent, fraud risk.
TIA (Transportation Intermediaries Association) best practices. Broker must contract with authorized carriers (verify
USDOT/MC on SAFER). Factoring companies buy carrier receivables; not brokers unless arranging transportation. Dispatchers
working for single carrier not brokers. Freight forwarders (FF number) take possession and liability; different than
brokers. Claims process: shipper/carrier files claim against bond with surety, FMCSA revokes authority if bond cancelled.
        """,
        key_factors=["MC number active", "$75K bond on file", "Broker vs carrier distinction", "Double brokering prevention", "Record retention 3 years"],
        primary_authority=["49 USC 13904", "49 CFR Part 371", "371.3 Bond requirement", "BMC-84 form"],
        burden_holder="Broker (maintain authority, bond, records)",
        adversary_position="Broker claims carrier authority, no bond needed; dispatcher exception applies",
        counter_arguments=["Broker cannot provide equipment per 371.13", "Dispatcher must work for single carrier, not multiple", "Bond required before arranging any transportation"],
        resolution_strategy="Verify MC number on FMCSA SAFER, confirm BMC-84 or trust fund on file, review broker-carrier contracts, check for double brokering (carrier contract prohibits re-brokering), audit records retention",
        entity_scope="All freight brokers arranging interstate transportation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="MC number and bond requirements bright-line; broker vs carrier distinction clear in regulation but fact-specific in practice; double brokering fraud analysis",
        controlling_precedent="49 USC 13904 and 49 CFR 371 mandatory; unauthorized brokering subject to penalties and authority revocation; bond claims process via surety"
    ),
    DoctrineBlock(
        topic="Passenger Carrier Safety 49 CFR 390-399",
        keywords=["passenger", "motorcoach", "bus", "charter", "tour", "school bus"],
        conclusion_template=[
            "Passenger carriers subject to stricter rules: 15+ passengers require CDL with P endorsement, medical, pre-trip.",
            "School buses: S endorsement, state certification, annual inspection, no cell phone use (49 CFR 392.80).",
            "Charter/tour: DOT number, insurance $5M (16+ seats), HOS 10-hour drive/15-hour on-duty (49 CFR 395.5)."
        ],
        reasoning_framework="""
49 CFR 383.91: CDL with passenger endorsement (P) required for vehicles designed to transport 16+ passengers (including
driver). School bus endorsement (S) additional requirement. 49 CFR 391: Medical, driver qualification, drug/alcohol
testing same as property carriers. 49 CFR 393.95: Emergency exits required (every 12 ft on large buses). 49 CFR 395.5:
Passenger carrier HOS (different than property): 10-hour drive limit after 8 consecutive off-duty, 15-hour on-duty
limit, 60/70 hour rule same. No 30-minute break requirement. Sleeper berth not allowed for passenger carriers.
49 CFR 396: Inspection/maintenance same; school buses often have state annual inspection beyond federal. 49 CFR 387.33:
Insurance $5M for 16+ passengers, $1.5M for 15 or fewer. School bus state rules vary (e.g., flashing lights, stop arm,
student loading procedures). Charter/tour operators often subject to state PUC (Public Utilities Commission) regulation.
Motorcoach Enhanced Safety Act (2012) added seatbelts, rollover standards, window glazing for new buses. Pre-trip
inspection mandatory (392.7). No standees forward of rear of driver's seat (392.60).
        """,
        key_factors=["Passenger capacity 16+ (vs 15-)", "P/S endorsement", "HOS 10/15 limits", "Insurance $5M", "Emergency exits", "School bus state rules"],
        primary_authority=["49 CFR 383.91 P/S endorsements", "49 CFR 395.5 Passenger HOS", "49 CFR 387.33 Insurance", "49 CFR 393.95 Emergency exits"],
        burden_holder="Passenger Carrier and Driver",
        adversary_position="15-passenger van exempt from CDL P endorsement (only 15 including driver, not 16+)",
        counter_arguments=["15-passenger vans (15 total) exempt from P endorsement but subject to other FMCSRs if GVWR 10,001+ or interstate for-hire", "School bus S endorsement required regardless of passenger count"],
        resolution_strategy="Count seating capacity, verify P/S endorsements, review HOS records for 10/15 limits, confirm $5M insurance, inspect emergency exits, check state school bus certifications",
        entity_scope="All passenger carriers operating CMVs; school buses per state law",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Passenger capacity thresholds bright-line; HOS 10/15 clear; insurance amounts set; school bus state rules vary",
        controlling_precedent="49 CFR 383/390-399 mandatory for interstate; states regulate school buses and intrastate passenger carriers; Motorcoach Enhanced Safety Act federal mandate"
    ),
    DoctrineBlock(
        topic="Transportation Worker Identification Credential TWIC",
        keywords=["TWIC", "port security", "maritime", "TSA", "facility access"],
        conclusion_template=[
            "TWIC (Transportation Worker Identification Credential) required for unescorted access to secure maritime facilities.",
            "TSA and Coast Guard administer; background check (criminal, immigration, terrorism) required.",
            "Valid 5 years; $125.25 fee; must be US citizen/national or lawful permanent resident."
        ],
        reasoning_framework="""
33 CFR 105.255: TWIC required for access to vessels and facilities subject to Maritime Transportation Security Act (MTSA).
Secure areas include ports, terminals, refineries, chemical facilities near water. TSA conducts background check:
disqualifying crimes (espionage, sedition, treason, terrorism), immigration status, FBI database. Coast Guard validates
credential. Application at enrollment center (fingerprints, photo). Card valid 5 years from issuance. Renewal $125.25,
replacement if lost $60. Card has biometric (fingerprint) and smart chip. Facilities use card readers at access points.
Escort allowed for non-TWIC individuals if facility permits. Lost/stolen card must be reported immediately. Criminal
convictions during validity require re-screening. TWIC not required for truck drivers who never leave cab in secure area
(remaining in truck exception). Facility Security Officer (FSO) determines access requirements. Violations: unauthorized
access subject to criminal penalties (18 USC 1001), civil penalties, removal from facility.
        """,
        key_factors=["Facility covered by MTSA", "Unescorted access needed", "Background check pass/fail", "5-year validity", "Biometric verification"],
        primary_authority=["33 CFR 105.255 TWIC requirement", "46 USC 70105 MTSA", "49 CFR 1572 TSA background checks"],
        burden_holder="Individual worker (obtain TWIC), Facility (verify TWIC)",
        adversary_position="Driver doesn't need TWIC if escorted or never leaves vehicle in secure area",
        counter_arguments=["Escort exceptions facility-specific", "Leaving cab to hook/unhook trailer may require TWIC", "Facility can impose stricter requirements than federal minimum"],
        resolution_strategy="Verify facility MTSA coverage, determine if unescorted access needed, confirm TWIC validity (5 years), check background for disqualifying crimes, use card reader for biometric",
        entity_scope="Workers requiring access to MTSA-regulated facilities (ports, refineries, terminals)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="TWIC requirement for secure facilities bright-line; background disqualifications listed; escort exceptions facility-dependent",
        controlling_precedent="33 CFR 105 and 49 CFR 1572 mandatory; TSA/Coast Guard enforcement; criminal penalties for unauthorized access"
    ),
    DoctrineBlock(
        topic="Fatality Analysis Reporting System FARS",
        keywords=["FARS", "fatal crash", "NHTSA", "crash reporting", "49 CFR 390.15"],
        conclusion_template=[
            "FARS (Fatality Analysis Reporting System) collects data on all fatal traffic crashes; NHTSA administers.",
            "State reporting required within 30 days of crash resulting in fatality within 30 days of crash.",
            "Used for safety analysis, rulemaking, CSA Crash Indicator BASIC; crash reports public record."
        ],
        reasoning_framework="""
FARS: Census of fatal traffic crashes (fatality within 30 days of crash) in 50 states, DC, Puerto Rico. NHTSA (National
Highway Traffic Safety Administration) compiles. Data from state police crash reports, coroner/medical examiner, vehicle
registration, driver license, roadway. Over 100 data elements: crash location, vehicles, drivers, pedestrians, fatalities,
contributing factors (speeding, alcohol, distraction). Used for Highway Safety Improvement Program (HSIP), rulemaking
(e.g., seatbelt mandates), CSA Crash Indicator BASIC (carriers with higher crash rates flagged). 49 CFR 390.15: Crashes
involving CMVs must be reported to FMCSA if fatality or injury with immediate medical treatment or disabling damage.
State submits to FMCSA MCMIS database. Carrier can challenge crash preventability via DataQ (49 CFR 386.12) or Crash
Preventability Determination Program (CPDP). Non-preventable crashes removed from CSA (e.g., struck from rear while
stopped, animal strike). Crash reports subject to state FOIA; insurance subrogation, litigation discovery. CMV fatal
crashes trigger FMCSA investigation if serious pattern or high-profile.
        """,
        key_factors=["Fatality within 30 days", "CMV involvement", "Crash preventability", "State reporting to MCMIS", "DataQ/CPDP challenge process"],
        primary_authority=["FARS program (NHTSA)", "49 CFR 390.15 Crash reporting", "FMCSA Crash Preventability Determination Program", "49 CFR 386.12 DataQ"],
        burden_holder="State (report crash), Carrier (challenge if non-preventable)",
        adversary_position="Crash was non-preventable (rear-end while stopped, animal, other driver at fault), should not count in CSA",
        counter_arguments=["CPDP only removes certain crash types (16 categories)", "Non-preventable determination fact-intensive", "Crash remains in FARS even if removed from CSA"],
        resolution_strategy="Review crash report for causation factors, file CPDP request if non-preventable (evidence: photos, police report), track CSA Crash Indicator impact, preserve evidence for litigation",
        entity_scope="All fatal traffic crashes; CMV crashes for CSA purposes",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="FARS reporting mandatory; crash preventability determination fact-intensive; CPDP criteria narrow; DataQ process administrative",
        controlling_precedent="FARS program established by statute; 49 CFR 390.15 reporting; CPDP policy by FMCSA; crash data public record subject to state FOIA"
    )
]

# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

START_TIME = time.time()

class Telemetry:
    def __init__(self):
        self.query_count = 0
        self.total_latency_ms = 0.0
        self.doctrines_triggered_count = 0
        self.error_count = 0
        self.mode_usage = {mode: 0 for mode in ResponseMode}

    def record_query(self, latency_ms: float, doctrines_triggered: int, mode: ResponseMode, error: bool = False):
        self.query_count += 1
        self.total_latency_ms += latency_ms
        self.doctrines_triggered_count += doctrines_triggered
        self.mode_usage[mode] += 1
        if error:
            self.error_count += 1

    def get_metrics(self) -> Dict[str, Any]:
        avg_latency = self.total_latency_ms / self.query_count if self.query_count > 0 else 0
        return {
            "total_queries": self.query_count,
            "avg_latency_ms": round(avg_latency, 2),
            "total_doctrines_triggered": self.doctrines_triggered_count,
            "error_count": self.error_count,
            "mode_usage": {k.value: v for k, v in self.mode_usage.items()}
        }

telemetry = Telemetry()

# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

def normalize_query(text: str) -> str:
    """Transportation-specific normalization."""
    norm = text.lower().strip()
    norm = norm.replace("d.o.t.", "dot").replace("f.m.c.s.a.", "fmcsa").replace("c.d.l.", "cdl")
    norm = norm.replace("h.o.s.", "hos").replace("e.l.d.", "eld").replace("d.v.i.r.", "dvir")
    norm = norm.replace("p.h.m.s.a.", "phmsa").replace("f.r.a.", "fra").replace("f.a.a.", "faa")
    return norm

def search_doctrines(question: str) -> List[DoctrineBlock]:
    """Match question keywords to doctrine blocks."""
    norm_q = normalize_query(question)
    words = set(norm_q.split())

    matches = []
    for doctrine in DOCTRINE_CACHE:
        kw_lower = [k.lower() for k in doctrine.keywords]
        score = sum(1 for kw in kw_lower if kw in norm_q)
        if score > 0:
            matches.append((score, doctrine))

    matches.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in matches[:5]]

def three_layer_response(question: str, mode: ResponseMode, zone: AnalysisZone) -> Tuple[str, List[DoctrineBlock], List[str]]:
    """Three-layer: doctrine cache -> semantic retrieval -> deep analysis."""
    doctrines = search_doctrines(question)
    reasoning_chain = []

    if not doctrines:
        reasoning_chain.append("No doctrine cache hits; using general transportation regulatory principles.")
        answer = generate_general_answer(question, mode, zone)
        return answer, [], reasoning_chain

    reasoning_chain.append(f"Doctrine cache hit: {len(doctrines)} blocks matched.")

    top_doctrine = doctrines[0]
    reasoning_chain.append(f"Primary doctrine: {top_doctrine.topic}")

    if mode == ResponseMode.FAST:
        answer = " ".join(top_doctrine.conclusion_template)
    elif mode == ResponseMode.DEFENSE:
        answer = build_defense_response(top_doctrine, question, reasoning_chain)
    else:  # MEMO
        answer = build_memo_response(doctrines, question, reasoning_chain)

    return answer, doctrines, reasoning_chain

def generate_general_answer(question: str, mode: ResponseMode, zone: AnalysisZone) -> str:
    """Fallback when no doctrine match."""
    base = (
        "Transportation regulatory compliance requires review of applicable DOT regulations (FMCSA, PHMSA, FRA, FAA), "
        "state DOT requirements, and industry standards. Specific analysis depends on vehicle type, operation mode "
        "(interstate/intrastate, for-hire/private), cargo, and driver qualifications. Recommend consultation with "
        "transportation counsel and review of 49 CFR Parts 300-399 and state-specific regulations."
    )
    if mode == ResponseMode.MEMO:
        base += (
            "\n\nKey areas to investigate: (1) FMCSA motor carrier safety regulations (CDL, HOS, ELD, drug/alcohol), "
            "(2) Vehicle inspection and maintenance requirements, (3) Weight and size limits (federal Bridge Formula, state permits), "
            "(4) Hazmat transportation rules (PHMSA 49 CFR 171-180), (5) Insurance and financial responsibility (49 CFR 387), "
            "(6) CSA safety measurement and roadside inspection compliance."
        )
    return base

def build_defense_response(doctrine: DoctrineBlock, question: str, reasoning_chain: List[str]) -> str:
    """Audit-ready defense mode response."""
    parts = []
    parts.append("CONCLUSION:\n" + " ".join(doctrine.conclusion_template))
    parts.append("\n\nLEGAL FRAMEWORK:\n" + doctrine.reasoning_framework.strip())
    parts.append("\n\nKEY FACTORS:\n" + "\n".join(f"- {f}" for f in doctrine.key_factors))
    parts.append("\n\nPRIMARY AUTHORITY:\n" + "\n".join(f"- {a}" for a in doctrine.primary_authority))
    parts.append(f"\n\nBURDEN OF COMPLIANCE: {doctrine.burden_holder}")
    parts.append(f"\n\nADVERSARY POSITION: {doctrine.adversary_position}")
    parts.append("\n\nCOUNTER-ARGUMENTS:\n" + "\n".join(f"- {c}" for c in doctrine.counter_arguments))
    parts.append(f"\n\nRESOLUTION STRATEGY: {doctrine.resolution_strategy}")
    parts.append(f"\n\nCONFIDENCE ASSESSMENT: {doctrine.confidence_stratification}")

    reasoning_chain.append("Built defense-mode response with full legal framework and counter-arguments.")
    return "".join(parts)

def build_memo_response(doctrines: List[DoctrineBlock], question: str, reasoning_chain: List[str]) -> str:
    """Comprehensive memo synthesizing multiple doctrines."""
    parts = []
    parts.append("MEMORANDUM: Transportation Regulatory Analysis\n")
    parts.append("="*60 + "\n\n")

    parts.append("EXECUTIVE SUMMARY:\n")
    for i, d in enumerate(doctrines[:3], 1):
        parts.append(f"{i}. {d.topic}: {d.conclusion_template[0]}\n")

    parts.append("\n\nDETAILED ANALYSIS:\n")
    for i, doctrine in enumerate(doctrines, 1):
        parts.append(f"\n{i}. {doctrine.topic.upper()}\n")
        parts.append("-" * 60 + "\n")
        parts.append("Applicable Standards:\n" + doctrine.reasoning_framework.strip()[:500] + "...\n")
        parts.append(f"\nPrimary Authority: {', '.join(doctrine.primary_authority[:3])}\n")
        parts.append(f"Confidence: {doctrine.confidence.value} - {doctrine.confidence_stratification}\n")

    parts.append("\n\nRECOMMENDATIONS:\n")
    parts.append("1. Verify compliance with all applicable regulations identified above.\n")
    parts.append("2. Conduct internal audit of documentation (CDL, medical certificates, insurance, permits).\n")
    parts.append("3. Review carrier safety rating and CSA BASIC scores for intervention thresholds.\n")
    parts.append("4. Ensure driver training programs cover all regulatory requirements.\n")
    parts.append("5. Maintain up-to-date vehicle inspection and maintenance records.\n")

    reasoning_chain.append("Synthesized memo from multiple doctrine blocks with recommendations.")
    return "".join(parts)

def compute_determinism_hash(question: str, answer: str, doctrines: List[str]) -> str:
    """SHA-256 for reproducibility."""
    content = f"{question}|{answer}|{','.join(sorted(doctrines))}"
    return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(title=ENGINE_NAME, version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    uptime = time.time() - START_TIME
    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=round(uptime, 2)
    )

@app.post("/query", response_model=QueryResponse)
async def query_engine(req: QueryRequest):
    """Main query endpoint with TIE-20 response."""
    start = time.time()

    try:
        answer, doctrines, reasoning_chain = three_layer_response(req.question, req.mode, req.zone)

        doctrines_triggered = [d.topic for d in doctrines]
        authorities = []
        for d in doctrines:
            authorities.extend(d.primary_authority)
        authorities = list(dict.fromkeys(authorities))[:10]

        confidence_level = doctrines[0].confidence.value if doctrines else "DISCLOSURE"

        elapsed_ms = (time.time() - start) * 1000
        det_hash = compute_determinism_hash(req.question, answer, doctrines_triggered)

        telemetry.record_query(elapsed_ms, len(doctrines_triggered), req.mode)

        logger.info(f"Query processed | Mode={req.mode.value} | Doctrines={len(doctrines_triggered)} | Time={elapsed_ms:.2f}ms")

        epistemic_disclosure = None
        if "exemption" in req.question.lower() or "permit" in req.question.lower():
            epistemic_disclosure = (
                "Transportation exemptions and permits are jurisdiction-specific and fact-intensive. "
                "This analysis provides general regulatory framework; consult applicable state DOT and "
                "verify current exemption/permit requirements before relying on this guidance."
            )

        return QueryResponse(
            answer=answer,
            confidence=confidence_level,
            mode=req.mode.value,
            zone=req.zone.value,
            doctrines_triggered=doctrines_triggered,
            reasoning_chain=reasoning_chain,
            authorities_cited=authorities,
            response_time_ms=round(elapsed_ms, 2),
            determinism_hash=det_hash,
            epistemic_disclosure=epistemic_disclosure
        )

    except Exception as e:
        telemetry.record_query((time.time() - start) * 1000, 0, req.mode, error=True)
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_metrics():
    """Telemetry metrics endpoint."""
    return telemetry.get_metrics()

@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine topics."""
    return {
        "count": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "primary_authority": d.primary_authority[:3]
            }
            for d in DOCTRINE_CACHE
        ]
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
