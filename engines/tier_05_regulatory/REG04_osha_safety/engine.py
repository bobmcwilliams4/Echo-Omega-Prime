"""
REG04 OSHA Safety Compliance Engine v1.0.0
Port 9124 | TIE-Grade Regulatory Intelligence

Domains: 29 CFR 1910 General Industry, 29 CFR 1926 Construction, PSM, LOTO,
Confined Space, Fall Protection, HazCom GHS, OSHA 300 Logs, Citations/Penalties
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import time
from contextlib import asynccontextmanager
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# =====================================================================
# CONFIGURATION
# =====================================================================
ENGINE_ID = "REG04"
ENGINE_NAME = "OSHA Safety Compliance Engine"
VERSION = "1.0.0"
PORT = 9124

# =====================================================================
# ENUMS
# =====================================================================
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
    GENERAL_INDUSTRY = "GENERAL_INDUSTRY"
    CONSTRUCTION = "CONSTRUCTION"
    PSM = "PROCESS_SAFETY_MANAGEMENT"
    HAZARD_COMMUNICATION = "HAZARD_COMMUNICATION"
    LOCKOUT_TAGOUT = "LOCKOUT_TAGOUT"
    CONFINED_SPACE = "CONFINED_SPACE"
    FALL_PROTECTION = "FALL_PROTECTION"
    PPE = "PERSONAL_PROTECTIVE_EQUIPMENT"
    RECORDKEEPING = "RECORDKEEPING"
    CITATIONS = "CITATIONS_PENALTIES"
    MULTI_EMPLOYER = "MULTI_EMPLOYER_WORKSITE"
    WHISTLEBLOWER = "WHISTLEBLOWER_RETALIATION"

# =====================================================================
# DOCTRINE CACHE
# =====================================================================
class DoctrineBlock(BaseModel):
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
    controlling_precedent: Optional[str] = None

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="General Duty Clause 5(a)(1) Application",
        keywords=["general duty", "5(a)(1)", "recognized hazard", "serious harm", "feasible abatement"],
        conclusion_template=[
            "Section 5(a)(1) requires employers to furnish employment free from recognized hazards causing or likely to cause death or serious physical harm.",
            "OSHA may cite under General Duty Clause only when no specific standard applies.",
            "Employer must prove hazard not recognized in industry or abatement not feasible."
        ],
        reasoning_framework="""
1. No Specific Standard: General Duty applies only where no standard addresses hazard directly
2. Recognized Hazard: Must show industry recognition (trade publications, industry standards, expert testimony)
3. Likely to Cause Serious Harm: Probability analysis and severity assessment
4. Feasible Abatement: Employer must show measures available and economically/technologically feasible
5. Employee Exposure: At least one employee must be exposed to hazard
4-Element Test: (1) hazard recognized (2) causing/likely to cause death/serious harm (3) feasible means to abate (4) employer failed to implement
General Duty citations require substantial evidence of industry recognition. Not a catch-all for novel hazards.
Feasibility defense: economic burden analysis, technological availability, whether measures would create greater hazards.
""",
        key_factors=[
            "Absence of specific standard covering hazard",
            "Industry recognition through publications/standards/practice",
            "Probability and severity of injury",
            "Availability of feasible protective measures",
            "Employee exposure to hazard",
            "Employer knowledge actual or constructive",
            "Greater hazard defense if abatement creates new risks"
        ],
        primary_authority=[
            "29 USC 654(a)(1) - OSH Act Section 5(a)(1)",
            "29 CFR 1903 - Inspections, Citations and Proposed Penalties",
            "Nat'l Realty & Constr. Co. v. OSHRC, 489 F.2d 1257 (D.C. Cir. 1973) - 4-element test",
            "Pepperidge Farm v. Sec'y of Labor, 17 F.3d 1003 (7th Cir. 1994) - feasibility burden"
        ],
        burden_holder="OSHA bears initial burden to prove 4 elements; employer has burden on feasibility defense",
        adversary_position="OSHA argues hazard widely recognized in industry and abatement readily available",
        counter_arguments=[
            "No specific standard exists because hazard novel or not generally recognized",
            "Industry practice does not constitute recognition",
            "Abatement measures not technologically feasible or create greater hazards",
            "Economic burden disproportionate to risk reduction",
            "Employees not actually exposed to hazard zone"
        ],
        resolution_strategy="Conduct industry recognition survey, document technological/economic infeasibility, propose alternative measures, show employee exposure limited",
        entity_scope="All employers under OSH Act jurisdiction",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="General Duty Clause highly fact-specific; strong defenses on feasibility and recognition",
        controlling_precedent="National Realty 4-element test binding"
    ),
    DoctrineBlock(
        topic="PSM 29 CFR 1910.119 Covered Processes Threshold",
        keywords=["psm", "1910.119", "threshold quantity", "highly hazardous chemicals", "covered process"],
        conclusion_template=[
            "PSM applies to processes involving chemicals at or above threshold quantities per Appendix A or any flammable liquid/gas over 10,000 lbs in one location.",
            "Process means any activity involving a highly hazardous chemical including use, storage, manufacturing, handling, or on-site movement.",
            "Exemptions for retail facilities, oil/gas well drilling, and normally unoccupied remote facilities."
        ],
        reasoning_framework="""
1. Threshold Determination: Check chemical against Appendix A (140+ chemicals with TQs ranging from 100 lbs to 20,000 lbs)
2. Flammable Liquids/Gases: Any process with 10,000 lbs or more triggers PSM regardless of Appendix A
3. One Location: Entire plant site considered one location; cannot segregate inventory to avoid threshold
4. Process Definition: Broad - includes vessels, piping, equipment, any activity with HHC
5. Exemptions: 1910.119(a)(2)(i)-(iii) narrow exemptions for retail, drilling, remote facilities
Common threshold chemicals: Chlorine (1,500 lbs), Ammonia (10,000 lbs), Hydrogen Sulfide (1,500 lbs), Propane (10,000 lbs)
Total inventory across all vessels/tanks/pipes counts toward threshold. Cannot avoid by distributing inventory.
""",
        key_factors=[
            "Chemical identity matches Appendix A",
            "Quantity on-site at any one time vs threshold",
            "Flammable liquid/gas classification and total quantity",
            "Manufacturing, processing, use, storage, handling, or movement activity",
            "Retail facility exemption (consumer packaged quantities)",
            "Normally unoccupied remote facility status",
            "Entire facility as single location for inventory aggregation"
        ],
        primary_authority=[
            "29 CFR 1910.119 - Process Safety Management of Highly Hazardous Chemicals",
            "29 CFR 1910.119(a)(1) - Application and threshold quantities",
            "29 CFR 1910.119 Appendix A - List of Highly Hazardous Chemicals",
            "OSHA CPL 02-02-045 - PSM Covered Chemical Facilities NEP"
        ],
        burden_holder="Employer must determine applicability; OSHA presumes coverage if HHC present",
        adversary_position="OSHA treats entire facility as one location and aggregates all inventory including in-process",
        counter_arguments=[
            "Inventory never reaches threshold quantity simultaneously",
            "Retail facility exemption applies",
            "Normally unoccupied remote facility",
            "Chemical not listed in Appendix A and not flammable over 10,000 lbs",
            "Hydrocarbon fuels exemption for flammable liquids used solely as fuel"
        ],
        resolution_strategy="Detailed chemical inventory with TQs, process flow diagrams, daily maximum inventory calculations, exemption documentation",
        entity_scope="Facilities with highly hazardous chemicals above threshold quantities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Threshold determination objective; exemptions narrowly construed",
        controlling_precedent="None - regulatory text controls"
    ),
    DoctrineBlock(
        topic="Lockout/Tagout 1910.147 Energy Control Procedures",
        keywords=["loto", "lockout", "tagout", "energy control", "servicing", "maintenance"],
        conclusion_template=[
            "LOTO requires written energy control procedures for servicing/maintenance where unexpected energization or startup could cause injury.",
            "Procedures must identify energy sources, isolation methods, verification of zero energy, and authorized employee training.",
            "Lockout preferred; tagout only if locks impossible and employer shows tagout equally effective."
        ],
        reasoning_framework="""
1. Coverage: Applies to servicing/maintenance on machines/equipment where unexpected energization/startup/stored energy release could injure employees
2. Exclusions: Normal production operations, cord/plug connected equipment, hot tap operations under 1910.147(a)(2)(ii)
3. Energy Control Procedure Elements: (1) scope/purpose/authorization (2) procedural steps (3) energy types/magnitudes (4) isolation means (5) verification
4. Lockout Devices: Positive restraint, durable, standardized, substantial enough to prevent removal without tools/force
5. Tagout Alone: Only if employer demonstrates tags provide equivalent protection (rare - high burden)
6. Training: Authorized employees perform lockout; affected employees informed; other employees aware
7. Periodic Inspection: Annual review by authorized employee other than one using procedure
Group lockout, shift change, outside contractors require specific procedures per 1910.147(f)-(h).
""",
        key_factors=[
            "Servicing/maintenance vs normal production operation",
            "Unexpected energization or startup potential",
            "Stored energy sources (electrical, mechanical, hydraulic, pneumatic, thermal, chemical, gravity)",
            "Energy isolation devices available (circuit breakers, valves, blind flanges)",
            "Written procedure identifying all energy sources",
            "Lockout device application and removal by authorized employee only",
            "Verification of zero energy state before work begins",
            "Annual periodic inspection documentation"
        ],
        primary_authority=[
            "29 CFR 1910.147 - The Control of Hazardous Energy (Lockout/Tagout)",
            "29 CFR 1910.147(c)(4) - Energy control procedure requirements",
            "29 CFR 1910.147(c)(7) - Lockout vs tagout standards",
            "OSHA 3120 - Control of Hazardous Energy (Lockout/Tagout) Booklet"
        ],
        burden_holder="Employer must develop procedures, provide devices, train employees; burden on employer to show tagout equivalent if no locks",
        adversary_position="OSHA requires lockout in nearly all cases; tagout alone rarely accepted",
        counter_arguments=[
            "Normal production operations exception applies",
            "Cord and plug connected equipment under employee exclusive control",
            "Hot tap operations under 1910.147(a)(2)(ii)(E)",
            "Minor tool changes/adjustments during normal production with effective alternative measures",
            "Tagout devices provide equivalent protection (requires proof)"
        ],
        resolution_strategy="Document all energy sources, detailed isolation procedures, employee training records, annual inspection logs, group lockout protocols",
        entity_scope="General industry employers with machinery/equipment servicing",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="LOTO strictly enforced; compliance well-defined but procedurally intensive",
        controlling_precedent="None - regulatory compliance determinative"
    ),
    DoctrineBlock(
        topic="Confined Space Entry 1910.146 Permit Requirements",
        keywords=["confined space", "permit-required", "entry", "atmospheric testing", "attendant"],
        conclusion_template=[
            "Permit-required confined spaces have limited entry/exit, not designed for continuous occupancy, and contain/potential to contain atmospheric or other serious hazards.",
            "Entry requires written permit, atmospheric testing, attendant, rescue arrangements, and entrant/attendant/supervisor training.",
            "Alternative 1910.146(c)(5) procedures available if all hazards eliminated and space reclassified."
        ],
        reasoning_framework="""
1. Confined Space Definition: (1) large enough for employee entry (2) limited means of entry/exit (3) not designed for continuous occupancy
2. Permit-Required: Contains or potential to contain (a) hazardous atmosphere (b) engulfment material (c) configuration could trap/asphyxiate (d) other serious safety/health hazard
3. Hazardous Atmosphere: <19.5% O2, >23.5% O2, >10% LEL, PEL exceeded, any condition immediately dangerous to life/health
4. Permit System: Written entry permit authorizing entry, valid only for specific entry duration, identifies hazards, controls, acceptable conditions
5. Atmospheric Testing: Test for O2, flammable gases/vapors, toxic substances in that order before entry and continuously during entry
6. Attendant: Stationed outside, monitors entrants, summons rescue, does NOT enter
7. Entry Supervisor: Authorizes entry, ensures permit conditions met, terminates entry if conditions change
8. Rescue: On-site rescue capability or <5 minute response time for rescue service
Alternative Procedures 1910.146(c)(5): Eliminate all hazards, continuous forced air ventilation, reclassify as non-permit space, maintain controls
""",
        key_factors=[
            "Space meets 3-part confined space definition",
            "Actual or potential atmospheric hazard present",
            "Engulfment, configuration, or other serious hazard exists",
            "Written entry permit completed before entry",
            "Atmospheric testing O2/flammable/toxic pre-entry and continuous",
            "Attendant present outside space during all entries",
            "Entry supervisor authorization and ongoing monitoring",
            "Rescue service arrangements on-site or <5 min response",
            "All entrants/attendants/supervisors trained and documented"
        ],
        primary_authority=[
            "29 CFR 1910.146 - Permit-Required Confined Spaces",
            "29 CFR 1910.146(c) - General requirements for permit spaces",
            "29 CFR 1910.146(d) - Permit system requirements",
            "29 CFR 1910.146(g) - Training requirements",
            "OSHA 3138 - Permit-Required Confined Spaces Guide"
        ],
        burden_holder="Employer must identify permit spaces, develop procedures, provide equipment, train employees",
        adversary_position="OSHA broadly construes potential hazards; alternative procedures rarely accepted",
        counter_arguments=[
            "Space not confined space (continuous occupancy design or adequate entry/exit)",
            "No actual or potential atmospheric hazard after testing/ventilation",
            "Alternative procedures 1910.146(c)(5) eliminate all hazards",
            "Reclassification to non-permit space with continuous controls",
            "Construction industry follows 1926 Subpart AA not 1910.146"
        ],
        resolution_strategy="Comprehensive space inventory, hazard assessment, written entry program, atmospheric monitoring equipment, rescue plan, training documentation",
        entity_scope="General industry employers with confined spaces (construction uses 1926 Subpart AA)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Permit-required status often clear from atmospheric testing; alternative procedures high compliance burden",
        controlling_precedent="None - regulatory compliance determinative"
    ),
    DoctrineBlock(
        topic="Fall Protection 1926.501 Construction Standards",
        keywords=["fall protection", "guardrails", "safety nets", "personal fall arrest", "6 feet", "construction"],
        conclusion_template=[
            "Construction employees on walking/working surfaces 6 feet or more above lower level must be protected by guardrail systems, safety net systems, or personal fall arrest systems.",
            "Leading edge work, hoist areas, holes, ramps/runways have specific requirements under 1926.501(b).",
            "Fall protection plan alternative for certain operations under 1926.502(k) if conventional protection infeasible."
        ],
        reasoning_framework="""
1. Trigger Height: 6 feet above lower level (general construction); 4 feet for scaffolds; varies by operation
2. Three Primary Systems: (1) Guardrail systems (2) Safety net systems (3) Personal fall arrest systems (PFAS)
3. Guardrail: Top rail 42 inches +/- 3 inches, midrail, toeboard, 200 lb top rail strength
4. Safety Nets: Maximum 30 feet below working level, extend 8-13 feet beyond edge, tested for impact
5. PFAS: Full body harness, lanyard/lifeline, anchorage 5,000 lbs per person or 2:1 safety factor, limit free fall to 6 feet
6. Leading Edge: Guardrail, safety net, or PFAS; fall protection plan if conventional protection creates greater hazard
7. Holes: Covers or guardrails; covers must support 2x anticipated load and marked HOLE or COVER
8. Residential Construction: 1926.501(b)(13) allows specific alternatives for framing/roofing operations
Fall protection plan under 1926.502(k): Must show conventional systems infeasible or create greater hazard, designate competent person, document site-specific plan.
""",
        key_factors=[
            "Walking/working surface 6+ feet above lower level",
            "Type of operation (general, leading edge, hoist area, holes, roofing, steel erection)",
            "Feasibility of guardrails vs safety nets vs PFAS",
            "Anchorage points and strength for PFAS",
            "Free fall distance limitation (6 feet maximum)",
            "Competent person training and designation",
            "Fall protection plan documentation if conventional systems infeasible",
            "Residential construction exemptions under 1926.501(b)(13)"
        ],
        primary_authority=[
            "29 CFR 1926.501 - Duty to Have Fall Protection",
            "29 CFR 1926.502 - Fall Protection Systems Criteria and Practices",
            "29 CFR 1926.503 - Training Requirements",
            "29 CFR 1926 Subpart M - Fall Protection",
            "OSHA 3146 - Fall Protection in Construction Guide"
        ],
        burden_holder="Employer must provide and ensure use of fall protection; burden on employer to show infeasibility for fall protection plan",
        adversary_position="OSHA presumes conventional fall protection feasible; fall protection plans scrutinized heavily",
        counter_arguments=[
            "Below 6 feet trigger height (unless specific operation requires lower)",
            "Conventional fall protection creates greater hazard",
            "Fall protection plan properly documented and implemented",
            "Residential construction exemption applies",
            "Steel erection governed by 1926 Subpart R specific rules",
            "Scaffolding fall protection under 1926 Subpart L not Subpart M"
        ],
        resolution_strategy="Site-specific fall hazard analysis, system selection justification, anchorage engineering, competent person designation, employee training records",
        entity_scope="Construction industry employers (general industry uses 1910.28-30)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="6-foot rule bright-line; fall protection plan narrow exception with high burden",
        controlling_precedent="None - regulatory compliance determinative"
    ),
    DoctrineBlock(
        topic="HazCom 2012 GHS SDS and Labeling Requirements",
        keywords=["hazcom", "ghs", "sds", "safety data sheet", "labeling", "pictograms"],
        conclusion_template=[
            "Hazard Communication Standard requires chemical manufacturers to provide Safety Data Sheets and GHS-compliant labels; employers must train employees on hazards and protective measures.",
            "SDS must contain 16 sections in prescribed order; labels must include product identifier, signal word, hazard statements, precautionary statements, pictograms, supplier info.",
            "Employers must maintain SDSs accessible to employees during each work shift and provide training at initial assignment and when new hazards introduced."
        ],
        reasoning_framework="""
1. Scope: All hazardous chemicals in workplace; exemptions for consumer products, food, drugs, cosmetics, tobacco
2. Chemical Manufacturer/Importer Duties: Classify hazards, prepare SDS, provide GHS labels
3. Employer Duties: Maintain SDSs, ensure containers labeled, train employees, written HazCom program
4. SDS 16 Sections: (1) Identification (2) Hazard(s) ID (3) Composition (4) First Aid (5) Firefighting (6) Accidental Release (7) Handling/Storage (8) Exposure Controls/PPE (9) Physical/Chemical Properties (10) Stability/Reactivity (11) Toxicological Info (12) Ecological Info (13) Disposal (14) Transport (15) Regulatory (16) Other Info
5. Label Elements: Product identifier, signal word (Danger/Warning), hazard statements, precautionary statements, pictograms (9 GHS types), supplier identification
6. Training: Initial assignment and when new physical/health hazards introduced; methods to detect release, physical/health hazards, protective measures, SDS location/use
7. Trade Secrets: May withhold specific chemical identity if trade secret, but must provide properties/effects and emergency treatment info
GHS Revision 2012 (HCS 2012) aligned with UN GHS; superseded 1994 HazCom. Pictograms: Flame, Exclamation Mark, Health Hazard, Gas Cylinder, Corrosion, Exploding Bomb, Flame Over Circle, Skull and Crossbones, Environment (not OSHA-required).
""",
        key_factors=[
            "Chemical hazardous per GHS classification (physical, health, environmental)",
            "SDS provided by manufacturer/importer/distributor with all 16 sections",
            "Container label includes all 6 GHS elements",
            "SDSs readily accessible to employees during work shift",
            "Written HazCom program documenting container labeling, SDS system, employee training",
            "Employee training initial and when new hazards introduced",
            "Trade secret claims with supporting statement and alternative chemical identification",
            "Secondary container labeling program"
        ],
        primary_authority=[
            "29 CFR 1910.1200 - Hazard Communication",
            "29 CFR 1910.1200(g) - Safety Data Sheets requirements",
            "29 CFR 1910.1200(f) - Labels and other forms of warning",
            "29 CFR 1910.1200(h) - Employee information and training",
            "OSHA 3844 - GHS/HazCom 2012 Brief"
        ],
        burden_holder="Chemical manufacturers classify and provide SDS/labels; employers maintain SDSs, ensure labeling, train employees",
        adversary_position="OSHA treats SDS/label deficiencies as serious violations; training must be effective not just documented",
        counter_arguments=[
            "Chemical not hazardous under GHS classification criteria",
            "Consumer product exemption (used in same manner and concentration as consumer)",
            "Laboratory use under Chemical Hygiene Plan 1910.1450",
            "Wood, articles, food/drug/cosmetic exemptions apply",
            "SDS provided but missing sections due to no data available (must state)",
            "Trade secret protection with alternative identification and medical emergency disclosure procedures"
        ],
        resolution_strategy="Chemical inventory with hazard classifications, SDS acquisition and maintenance system, label compliance audit, written HazCom program, training documentation",
        entity_scope="All employers with hazardous chemicals in workplace",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="GHS requirements objective and well-defined; compliance straightforward if system in place",
        controlling_precedent="None - regulatory compliance determinative"
    ),
    DoctrineBlock(
        topic="OSHA 300 Log Recordkeeping Requirements",
        keywords=["osha 300", "recordkeeping", "injury", "illness", "log", "form 301", "annual summary"],
        conclusion_template=[
            "Employers with 11+ employees must record work-related injuries and illnesses on OSHA 300 Log within 7 calendar days of learning of recordable case.",
            "Recordable cases include work-related death, days away from work, restricted work/job transfer, medical treatment beyond first aid, loss of consciousness, significant injury/illness diagnosed by healthcare professional.",
            "Annual summary (Form 300A) must be posted Feb 1 - April 30 and retained 5 years; electronic reporting required for establishments 250+ or specific industries 20-249."
        ],
        reasoning_framework="""
1. Coverage: Employers with 11+ employees (previous year); exemptions for certain low-hazard industries under Appendix A
2. Recordable Determination: (1) Work-related? (2) New case? (3) Meets recording criteria?
3. Work-Relatedness: Injury/illness results from event/exposure in work environment; presumed work-related unless specific exception applies (1904.5(b)(2) exceptions)
4. General Recording Criteria: Death, days away from work, restricted work or job transfer, medical treatment beyond first aid, loss of consciousness, significant injury/illness
5. Medical Treatment: Treatment beyond first aid per 1904.7(b)(5)(ii) list; first aid includes bandages, non-prescription drugs, tetanus shots, cleaning/bandaging minor injuries
6. Days Away/Restricted: Count calendar days even if no work scheduled; cap at 180 days; restricted work = cannot perform routine functions or cannot work full scheduled shift
7. Forms: OSHA 300 Log (running log), OSHA 301 Incident Report (detail), OSHA 300A Annual Summary (totals)
8. Retention: 5 years; annual summary posted Feb 1 - Apr 30
9. Electronic Reporting: Establishments 250+ submit 300A annually; establishments 20-249 in high-hazard industries (NAICS listed) submit 300A annually
Privacy cases (1904.29): Injuries to intimate body parts, sexual assault, mental illness, HIV/TB/hepatitis/bloodborne - record as privacy case without employee name.
""",
        key_factors=[
            "11+ employees in previous calendar year",
            "Injury/illness occurred in work environment",
            "Event/exposure in work environment caused/contributed to condition",
            "Work-relatedness exceptions (pre-existing, voluntary wellness, eating/drinking, common cold, blood donation) do not apply",
            "Case meets general recording criteria (death, DAFW, RW, medical treatment, LOC, significant injury)",
            "Medical treatment beyond first aid administrated or recommended",
            "Form 300 entry within 7 calendar days of knowledge",
            "Annual summary Form 300A completed, certified, posted Feb 1 - Apr 30",
            "5-year retention of all forms",
            "Electronic submission if 250+ employees or 20-249 in high-hazard NAICS"
        ],
        primary_authority=[
            "29 CFR 1904 - Recording and Reporting Occupational Injuries and Illnesses",
            "29 CFR 1904.4 - Recording Criteria",
            "29 CFR 1904.7 - General Recording Criteria",
            "29 CFR 1904.29 - Forms (300, 301, 300A)",
            "29 CFR 1904.41 - Electronic Submission Requirements",
            "OSHA 3169 - Recordkeeping Forms and Instructions"
        ],
        burden_holder="Employer determines recordability and maintains records; employee privacy protected for certain cases",
        adversary_position="OSHA presumes work-relatedness if injury in work environment; employer must rebut with specific exception",
        counter_arguments=[
            "Fewer than 11 employees in previous year",
            "Low-hazard industry partial exemption under 1904.1 and Appendix A (still must report fatalities/hospitalizations)",
            "Injury not work-related under 1904.5(b)(2) exceptions (pre-existing, voluntary participation, eating/drinking personal food, common cold/flu)",
            "First aid only per 1904.7(b)(5)(ii) list (no medical treatment)",
            "No days away, no restricted work, no medical treatment, no LOC, not significant diagnosed injury",
            "Privacy case protections prevent disclosure of employee name"
        ],
        resolution_strategy="Recordability determination flowchart, work-relatedness analysis with exception documentation, medical treatment classification, timely 7-day logging, annual review and certification, electronic submission compliance if applicable",
        entity_scope="Most private sector employers with 11+ employees (some low-hazard industry exemptions)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Recording criteria detailed and objective; work-relatedness presumption shifts burden to employer to prove exception",
        controlling_precedent="None - regulatory compliance determinative"
    ),
    DoctrineBlock(
        topic="Citation Classifications and Penalty Calculations",
        keywords=["citation", "willful", "serious", "repeat", "other-than-serious", "penalty", "de minimis"],
        conclusion_template=[
            "OSHA citations classified as willful, serious, other-than-serious, repeat, or de minimis; willful carries up to $156,259 per violation, serious/other-than-serious up to $15,625 per violation, repeat up to $156,259.",
            "Serious violation exists where substantial probability death or serious physical harm could result and employer knew or should have known of hazard.",
            "Willful violation requires employer acted with intentional disregard or plain indifference to law; repeat violation requires citation for substantially similar violation within 5 years."
        ],
        reasoning_framework="""
1. De Minimis: No direct/immediate relationship to safety/health; no penalty; notice issued but not citation
2. Other-Than-Serious: Direct relationship to safety/health but probably would not cause death/serious harm; up to $15,625 per violation
3. Serious: Substantial probability death/serious physical harm could result from hazard; employer knew/should have known (constructive knowledge); up to $15,625 per violation
4. Willful: Employer committed violation with intentional disregard or plain indifference to Act; up to $156,259 per violation; criminal if death results
5. Repeat: Substantially similar violation cited within 5 years (federal-wide, not state-by-state); up to $156,259 per violation
6. Failure to Abate: Original violation not corrected by abatement date; $15,625 per day beyond date
7. Penalty Factors: Gravity (severity + probability), employer size, good faith, history; gravity accounts for 60-80% of penalty
8. Gravity-Based Penalty (GBP): High gravity $15,625, medium $10,949, low $7,792; adjusted for size/good faith/history
9. Size Reduction: 1-25 employees (60%), 26-100 (40%), 101-250 (20%), 251+ (0%)
10. Good Faith Reduction: Up to 25% for comprehensive safety program beyond regulatory minimums
11. History Reduction: Up to 10% if no citations in past 3 years
Willful vs Serious: Intent/state of mind; serious = should have known (negligence); willful = knew and didn't care or intentionally violated. Constructive knowledge = reasonable diligence would have discovered.
""",
        key_factors=[
            "Type of violation (de minimis, other-than-serious, serious, willful, repeat)",
            "Employer knowledge actual or constructive",
            "Intentional disregard or plain indifference (willful)",
            "Substantially similar violation within 5 years (repeat)",
            "Severity of injury/illness probable from hazard",
            "Probability of injury/illness occurrence",
            "Employer size for penalty adjustment",
            "Good faith safety program for reduction",
            "Citation history in past 3-5 years"
        ],
        primary_authority=[
            "29 USC 666 - OSH Act Section 17 Civil and Criminal Penalties",
            "29 CFR 1903.15 - Proposed Penalties",
            "OSHA FOM Ch. 6 - Penalties and Debt Collection",
            "2024 Penalty Inflation Adjustments (89 FR 1202)"
        ],
        burden_holder="OSHA bears burden to prove violation type and employer knowledge; employer may raise affirmative defenses",
        adversary_position="OSHA argues constructive knowledge broad - employer should have known through reasonable diligence",
        counter_arguments=[
            "Violation de minimis with no direct safety/health impact",
            "No substantial probability of serious harm (other-than-serious not serious)",
            "Lack of employer knowledge actual or constructive (unpreventable employee misconduct defense)",
            "No intentional disregard or plain indifference (serious not willful)",
            "Prior citation not substantially similar (not repeat)",
            "Isolated violation or employee misconduct with adequate work rules and enforcement",
            "Good faith comprehensive safety program and history justify penalty reduction"
        ],
        resolution_strategy="Knowledge documentation (training records, audits, safety programs), violation classification challenge, penalty calculation verification, size/good faith/history reduction arguments, unpreventable employee misconduct defense",
        entity_scope="All employers subject to OSHA citations",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Willful vs serious heavily fact-dependent; penalty reductions negotiable; unpreventable misconduct defense available",
        controlling_precedent="Constructive knowledge = reasonable diligence would have discovered; willful requires heightened state of mind beyond negligence"
    ),
    DoctrineBlock(
        topic="Multi-Employer Worksite Citation Policy",
        keywords=["multi-employer", "controlling employer", "exposing employer", "creating employer", "correcting employer"],
        conclusion_template=[
            "On multi-employer worksites, OSHA may cite controlling, creating, exposing, or correcting employers depending on their role and ability to prevent/correct hazards.",
            "Controlling employer has general supervisory authority over worksite and must ensure all employers correct hazards.",
            "Exposing employer whose employees exposed to hazard must protect own employees even if another employer created hazard."
        ],
        reasoning_framework="""
1. Four Employer Categories:
   - Creating Employer: Causes hazardous condition (liable unless reasonable care to prevent and no control over hazard creation)
   - Exposing Employer: Employees exposed to hazard (liable unless reasonable care to detect/prevent/abate)
   - Correcting Employer: Responsible for correcting hazard (liable if fails to correct with reasonable promptness/care)
   - Controlling Employer: General supervisory authority over worksite (liable if fails to exercise reasonable care to prevent/detect/correct)
2. Controlling Employer: Must have authority over worksite/other employers; measures required reasonable given degree of control
3. Exposing Employer: Cannot rely on other employers to protect own employees; must conduct own inspections and take protective measures
4. Creating Employer: Liable even if employees not exposed if created hazard and others exposed; defense if no control over hazard creation
5. Correcting Employer: Liable only if undertaken duty to correct and failed; no duty to correct unless accepted responsibility
Multiple employers may be cited for same hazard under different categories. General contractor often cited as controlling employer.
""",
        key_factors=[
            "Multi-employer worksite (two or more employers)",
            "Employer role: creating, exposing, correcting, or controlling",
            "General supervisory authority over worksite (controlling)",
            "Created hazardous condition (creating)",
            "Own employees exposed to hazard (exposing)",
            "Accepted responsibility to correct hazard (correcting)",
            "Reasonable care exercised to prevent/detect/correct within employer's scope of control",
            "Degree of control over area where hazard exists"
        ],
        primary_authority=[
            "OSHA Multi-Employer Citation Policy (CPL 02-00-124)",
            "29 USC 654(a)(2) - Each employer shall comply with standards",
            "Reich v. Simpson, Gumpertz & Heger, 3 F.3d 1 (1st Cir. 1993) - controlling employer liability",
            "Solis v. Summit Contractors, 558 F.3d 815 (8th Cir. 2009) - multi-employer worksite"
        ],
        burden_holder="OSHA bears burden to prove employer falls within category and failed to exercise reasonable care; employer may show lack of control or reasonable care",
        adversary_position="OSHA broadly interprets controlling employer status for general contractors; reasonable care requires active inspection not reliance on subcontractors",
        counter_arguments=[
            "Not controlling employer - no general supervisory authority over worksite or other employers",
            "Not exposing employer - own employees not exposed to cited hazard",
            "Not creating employer - did not cause hazardous condition or no control over hazard creation",
            "Not correcting employer - never accepted responsibility to correct hazard",
            "Reasonable care exercised given degree of control (inspection, safety meetings, contractual requirements, correction requests)",
            "Hazard in area controlled exclusively by another employer with no right of access"
        ],
        resolution_strategy="Document employer role and scope of control, inspection records, safety contract provisions, hazard correction requests, lack of authority over cited area or hazard",
        entity_scope="All employers on multi-employer worksites (construction, maintenance, shared facilities)",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Multi-employer citations heavily fact-dependent; controlling employer status often disputed; reasonable care standard flexible",
        controlling_precedent="Simpson Gumpertz - controlling employer liability; reasonable care standard case-by-case"
    ),
    DoctrineBlock(
        topic="Abatement Requirements and Verification",
        keywords=["abatement", "correction", "verification", "abatement date", "certification", "interim protection"],
        conclusion_template=[
            "Employers must abate cited violations by date specified in citation; if abatement cannot be completed by date, may request extension showing good faith and all available interim steps taken.",
            "Abatement verification required for serious, willful, repeat violations; employer must certify in writing and provide documentation (photos, inspection reports, receipts).",
            "Failure to abate timely results in failure-to-abate citation with per-day penalties until corrected."
        ],
        reasoning_framework="""
1. Abatement Date: Shortest reasonable time to correct violation, considering complexity and availability of materials; no more than 30 days unless employer shows longer needed
2. Extension Requests: Must file before abatement date with reasons for additional time, steps taken to abate, interim steps to protect employees, new proposed date
3. Abatement Verification: Tags/certification required for serious/willful/repeat; employer must certify abated and provide documentation (photos, inspection records, receipts, engineering reports)
4. Abatement Methods: Remove hazard, guard hazard, reduce exposure (engineering controls), administrative controls, PPE (last resort)
5. Interim Protection: While abatement in progress, employer must implement interim steps to protect employees (warnings, PPE, restricted access)
6. Failure to Abate: Separate citation if not corrected by abatement date; $15,625 per day; continues until hazard corrected
7. Abatement Certification: Must state how/when corrected, signed by responsible official; tags visible at worksite; detailed documentation submitted
Abatement hierarchy: (1) eliminate hazard (2) engineering controls (3) administrative controls (4) PPE. OSHA disfavors PPE-only abatement.
""",
        key_factors=[
            "Abatement date specified in citation reasonable given violation complexity",
            "Abatement method eliminates hazard or reduces exposure below standard",
            "Engineering controls preferred over administrative/PPE",
            "Extension request filed before abatement date with good cause",
            "All available interim steps taken to protect employees during abatement period",
            "Abatement certification signed by official and supported by documentation",
            "Photos, inspection reports, receipts, engineering documents verify abatement complete",
            "Tags posted at worksite until abatement verified",
            "Failure-to-abate exposure if not corrected by abatement date"
        ],
        primary_authority=[
            "29 CFR 1903.19 - Abatement Verification",
            "29 USC 658(a) - OSH Act Section 9(a) - Citation shall fix reasonable time for abatement",
            "29 CFR 1903.14a - Petitions for Modification of Abatement Date",
            "OSHA FOM Ch. 7 - Abatement Verification"
        ],
        burden_holder="Employer must abate by date and provide verification; burden on employer to show extension needed and interim protection in place",
        adversary_position="OSHA sets tight abatement dates and requires detailed verification documentation; extensions granted reluctantly",
        counter_arguments=[
            "Abatement date unreasonably short given violation complexity and equipment/materials availability",
            "Good faith extension request with detailed justification and interim protection measures",
            "Abatement completed by date but verification documentation delayed (still cite failure to verify)",
            "Hazard corrected through alternative method achieving equivalent protection",
            "Unpreventable employee misconduct caused re-occurrence after abatement (work rules and enforcement documented)"
        ],
        resolution_strategy="Timely abatement with documentation, extension request before abatement date with good cause, interim protection measures, certification with supporting photos/records, permanent correction verification",
        entity_scope="All employers with OSHA citations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Abatement requirements clear; extensions require good cause and interim protection; failure-to-abate penalties significant",
        controlling_precedent="None - regulatory compliance determinative"
    ),
    DoctrineBlock(
        topic="Whistleblower Retaliation Section 11(c) Protection",
        keywords=["whistleblower", "retaliation", "section 11(c)", "discrimination", "protected activity", "adverse action"],
        conclusion_template=[
            "Section 11(c) prohibits employers from retaliating against employees for exercising rights under OSH Act, including filing complaints, participating in inspections, or refusing dangerous work.",
            "Employee must file retaliation complaint with OSHA within 30 days of adverse action; OSHA investigates and may file litigation in district court.",
            "Employer liable if employee engaged in protected activity, employer knew, and adverse action causally connected; dual motive cases employer must show would have taken action anyway."
        ],
        reasoning_framework="""
1. Protected Activities: Filing complaint with OSHA, participating in inspection, testifying in proceeding, refusing dangerous work where no time for OSHA inspection and reasonable belief of serious injury/death
2. Adverse Actions: Discharge, discipline, demotion, denial of promotion, reduction in pay/benefits, blacklisting, intimidation, harassment, unfavorable reassignment
3. Causal Connection: Timing (proximity of protected activity to adverse action), employer knowledge, comparative treatment, deviation from policy, shifting explanations
4. Burden Shifting: Employee proves prima facie (protected activity, employer knowledge, adverse action, causal connection) -> Employer proves legitimate non-retaliatory reason -> Employee proves reason pretextual or dual motive
5. Dual Motive: If employer had both lawful and unlawful motives, employer must prove by preponderance would have taken same action absent protected activity
6. Reasonable Belief: Employee refusing dangerous work need not be correct about danger; only must have reasonable, good faith belief serious injury/death imminent
7. Remedies: Reinstatement, back pay, restoration of benefits, compensatory damages, attorney fees; no punitive damages in 11(c) cases
8. 30-Day Filing Deadline: Jurisdictional; employee must file with OSHA within 30 days of adverse action; extensions rare
Private right of action: Employee may file in federal district court if OSHA does not file within 90 days or Secretary issues final decision.
""",
        key_factors=[
            "Employee engaged in protected activity (complaint, inspection, testimony, work refusal)",
            "Employer knowledge of protected activity",
            "Adverse employment action taken against employee",
            "Causal connection (temporal proximity, shifting explanations, comparative treatment)",
            "Legitimate non-retaliatory reason for action (performance, misconduct, reduction in force)",
            "Pretext evidence (deviation from policy, inconsistent enforcement, proximity timing)",
            "Reasonable good faith belief of imminent serious injury/death (work refusal cases)",
            "30-day filing deadline met"
        ],
        primary_authority=[
            "29 USC 660(c) - OSH Act Section 11(c) Discrimination Prohibition",
            "29 CFR 1977 - Discrimination Against Employees Exercising Rights Under OSH Act",
            "Bechtel Constr. Co. v. Sec'y of Labor, 50 F.3d 926 (11th Cir. 1995) - dual motive test",
            "Reich v. Hoy Shoe Co., 32 F.3d 361 (8th Cir. 1994) - burden shifting framework"
        ],
        burden_holder="Employee bears initial burden on prima facie case; employer must prove legitimate reason; employee must prove pretext or employer fails dual motive burden",
        adversary_position="OSHA/employee argues temporal proximity and comparative treatment show causal connection; legitimate reasons pretextual",
        counter_arguments=[
            "Employee did not engage in protected activity or employer unaware of activity",
            "Adverse action taken for legitimate non-retaliatory reasons (performance, misconduct, RIF)",
            "No causal connection (long time gap, consistent enforcement, pre-existing discipline)",
            "Employer would have taken same action absent protected activity (dual motive defense)",
            "Work refusal unreasonable - no imminent serious injury/death threat or time available for OSHA inspection",
            "Complaint filed >30 days after adverse action (jurisdictional bar)"
        ],
        resolution_strategy="Document legitimate business reasons for employment decisions, consistent enforcement of policies, performance/misconduct evidence, lack of knowledge of protected activity, 30-day deadline jurisdictional bar",
        entity_scope="All employers under OSH Act jurisdiction",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Retaliation claims heavily fact-dependent; temporal proximity strong evidence but rebuttable; dual motive defense available",
        controlling_precedent="Dual motive test from Bechtel - employer must prove would have taken same action"
    )
]

# =====================================================================
# TELEMETRY
# =====================================================================
class QueryTelemetry(BaseModel):
    query_id: str
    timestamp: datetime
    mode: ResponseMode
    zone: AnalysisZone
    cache_hit: bool
    cache_topics: List[str]
    semantic_retrieval: bool
    deep_analysis: bool
    latency_ms: float
    doctrine_count: int
    confidence: ConfidenceLevel
    determinism_hash: str

class TelemetryCollector:
    def __init__(self):
        self.queries: List[QueryTelemetry] = []
        self.doctrine_hits: Dict[str, int] = {}
        self.doctrine_misses: Set[str] = set()

    def record(self, telemetry: QueryTelemetry):
        self.queries.append(telemetry)
        for topic in telemetry.cache_topics:
            self.doctrine_hits[topic] = self.doctrine_hits.get(topic, 0) + 1

    def get_metrics(self) -> Dict[str, Any]:
        if not self.queries:
            return {"total_queries": 0}
        latencies = [q.latency_ms for q in self.queries]
        return {
            "total_queries": len(self.queries),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "cache_hit_rate": sum(1 for q in self.queries if q.cache_hit) / len(self.queries),
            "semantic_retrieval_rate": sum(1 for q in self.queries if q.semantic_retrieval) / len(self.queries),
            "deep_analysis_rate": sum(1 for q in self.queries if q.deep_analysis) / len(self.queries),
            "top_doctrines": sorted(self.doctrine_hits.items(), key=lambda x: x[1], reverse=True)[:10]
        }

telemetry_collector = TelemetryCollector()

# =====================================================================
# PYDANTIC MODELS
# =====================================================================
class AnalysisRequest(BaseModel):
    query: str = Field(..., description="OSHA safety regulatory question or scenario")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis context zone")

class AnalysisResponse(BaseModel):
    query_id: str
    timestamp: datetime
    mode: ResponseMode
    zone: AnalysisZone
    answer: str
    doctrines_applied: List[str]
    confidence: ConfidenceLevel
    reasoning_chain: List[str]
    key_factors: List[str]
    authorities: List[str]
    recommended_actions: List[str]
    risk_assessment: str
    determinism_hash: str
    latency_ms: float

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    engine_name: str
    version: str
    port: int
    doctrines_loaded: int
    total_queries: int
    avg_latency_ms: float
    cache_hit_rate: float
    uptime_seconds: float

# =====================================================================
# ENGINE CORE
# =====================================================================
class OSHASafetyEngine:
    def __init__(self):
        self.start_time = time.time()
        logger.info(f"{ENGINE_NAME} v{VERSION} initializing on port {PORT}")

    def _normalize_query(self, query: str) -> str:
        """Normalize query for deterministic matching"""
        normalized = query.lower().strip()
        replacements = {
            "lock out tag out": "lockout tagout",
            "lock-out tag-out": "lockout tagout",
            "loto": "lockout tagout",
            "psm": "process safety management",
            "permit required confined space": "permit-required confined space",
            "prcs": "permit-required confined space",
            "pfas": "personal fall arrest",
            "ghs": "globally harmonized system",
            "hcs": "hazard communication standard",
            "hazcom": "hazard communication",
            "sds": "safety data sheet",
            "msds": "material safety data sheet"
        }
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)
        return normalized

    def _search_doctrine_cache(self, query: str) -> List[DoctrineBlock]:
        """Layer 1: Fast doctrine cache lookup"""
        normalized = self._normalize_query(query)
        matches = []
        for doctrine in DOCTRINE_CACHE:
            if any(kw in normalized for kw in doctrine.keywords):
                matches.append(doctrine)
        return matches[:5]

    def _apply_three_layer_response(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> tuple:
        """Three-layer TIE response architecture"""
        start = time.time()

        # Layer 1: Doctrine Cache (0-200ms)
        cache_matches = self._search_doctrine_cache(query)
        cache_hit = len(cache_matches) > 0

        # Layer 2: Semantic Retrieval (200-1000ms) - simulated
        semantic_retrieval = not cache_hit

        # Layer 3: Deep Analysis (1000-5000ms) - simulated
        deep_analysis = mode == ResponseMode.MEMO

        latency_ms = (time.time() - start) * 1000

        return cache_matches, cache_hit, semantic_retrieval, deep_analysis, latency_ms

    def _build_response(self, query: str, doctrines: List[DoctrineBlock], mode: ResponseMode, zone: AnalysisZone) -> str:
        """Build response based on mode and zone"""
        if not doctrines:
            return self._build_fallback_response(query, mode)

        primary = doctrines[0]

        if mode == ResponseMode.FAST:
            return "\n".join(primary.conclusion_template)

        elif mode == ResponseMode.DEFENSE:
            response = f"OSHA COMPLIANCE ANALYSIS:\n\n"
            response += f"PRIMARY AUTHORITY:\n"
            for auth in primary.primary_authority[:3]:
                response += f"  - {auth}\n"
            response += f"\nCONCLUSION:\n"
            response += "\n".join(primary.conclusion_template)
            response += f"\n\nKEY COMPLIANCE FACTORS:\n"
            for factor in primary.key_factors[:5]:
                response += f"  - {factor}\n"
            response += f"\n\nADVERSARY POSITION:\n{primary.adversary_position}\n"
            response += f"\nDEFENSE STRATEGY:\n{primary.resolution_strategy}"
            return response

        else:  # MEMO
            response = f"COMPREHENSIVE OSHA SAFETY MEMORANDUM\n"
            response += f"{'='*70}\n\n"
            response += f"TOPIC: {primary.topic}\n\n"
            response += f"REGULATORY FRAMEWORK:\n{primary.reasoning_framework}\n\n"
            response += f"PRIMARY AUTHORITIES:\n"
            for auth in primary.primary_authority:
                response += f"  - {auth}\n"
            response += f"\nANALYSIS:\n"
            response += "\n".join(primary.conclusion_template)
            response += f"\n\nKEY COMPLIANCE FACTORS:\n"
            for i, factor in enumerate(primary.key_factors, 1):
                response += f"  {i}. {factor}\n"
            response += f"\nBURDEN OF PROOF:\n{primary.burden_holder}\n"
            response += f"\nOSHA ENFORCEMENT POSITION:\n{primary.adversary_position}\n"
            response += f"\nDEFENSE ARGUMENTS:\n"
            for i, arg in enumerate(primary.counter_arguments, 1):
                response += f"  {i}. {arg}\n"
            response += f"\nRECOMMENDED STRATEGY:\n{primary.resolution_strategy}\n"
            response += f"\nCONFIDENCE LEVEL: {primary.confidence.value}\n"
            response += f"STRATIFICATION: {primary.confidence_stratification}"

            if len(doctrines) > 1:
                response += f"\n\nRELATED DOCTRINES:\n"
                for doc in doctrines[1:3]:
                    response += f"  - {doc.topic}\n"
            return response

    def _build_fallback_response(self, query: str, mode: ResponseMode) -> str:
        """Fallback when no doctrine match"""
        return f"No specific OSHA doctrine cache match for query. General guidance: Consult 29 CFR 1910 (General Industry) or 29 CFR 1926 (Construction) for applicable standards. Common OSHA areas: Fall Protection, HazCom, Lockout/Tagout, Confined Space, PSM, Recordkeeping (OSHA 300), PPE. For specific regulatory interpretation, contact OSHA compliance assistance or consult OSHA letter of interpretation database."

    def _calculate_determinism_hash(self, query: str, doctrines: List[DoctrineBlock], mode: ResponseMode) -> str:
        """SHA-256 hash for reproducibility"""
        content = f"{query}|{mode.value}|" + "|".join(d.topic for d in doctrines)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def analyze(self, request: AnalysisRequest) -> AnalysisResponse:
        """Main analysis endpoint with full TIE architecture"""
        query_id = hashlib.sha256(f"{request.query}{time.time()}".encode()).hexdigest()[:12]
        start_time = time.time()

        # Three-layer response
        doctrines, cache_hit, semantic_retrieval, deep_analysis, layer_latency = self._apply_three_layer_response(
            request.query, request.mode, request.zone
        )

        # Build response
        answer = self._build_response(request.query, doctrines, request.mode, request.zone)

        # Extract data
        doctrines_applied = [d.topic for d in doctrines]
        confidence = doctrines[0].confidence if doctrines else ConfidenceLevel.DISCLOSURE
        authorities = doctrines[0].primary_authority if doctrines else []
        key_factors = doctrines[0].key_factors if doctrines else []

        # Reasoning chain
        reasoning_chain = []
        if cache_hit:
            reasoning_chain.append(f"Doctrine cache hit: {len(doctrines)} matches")
        if semantic_retrieval:
            reasoning_chain.append("Semantic retrieval layer engaged")
        if deep_analysis:
            reasoning_chain.append("Deep analysis mode for comprehensive memorandum")

        # Recommended actions
        recommended_actions = []
        if doctrines:
            recommended_actions.append(f"Review primary authorities: {', '.join(doctrines[0].primary_authority[:2])}")
            recommended_actions.append(f"Strategy: {doctrines[0].resolution_strategy}")

        # Risk assessment
        risk_assessment = f"Confidence: {confidence.value}"
        if doctrines:
            risk_assessment += f" | Burden: {doctrines[0].burden_holder}"

        # Determinism hash
        determinism_hash = self._calculate_determinism_hash(request.query, doctrines, request.mode)

        total_latency = (time.time() - start_time) * 1000

        # Telemetry
        telemetry = QueryTelemetry(
            query_id=query_id,
            timestamp=datetime.utcnow(),
            mode=request.mode,
            zone=request.zone,
            cache_hit=cache_hit,
            cache_topics=doctrines_applied,
            semantic_retrieval=semantic_retrieval,
            deep_analysis=deep_analysis,
            latency_ms=total_latency,
            doctrine_count=len(doctrines),
            confidence=confidence,
            determinism_hash=determinism_hash
        )
        telemetry_collector.record(telemetry)

        return AnalysisResponse(
            query_id=query_id,
            timestamp=datetime.utcnow(),
            mode=request.mode,
            zone=request.zone,
            answer=answer,
            doctrines_applied=doctrines_applied,
            confidence=confidence,
            reasoning_chain=reasoning_chain,
            key_factors=key_factors,
            authorities=authorities,
            recommended_actions=recommended_actions,
            risk_assessment=risk_assessment,
            determinism_hash=determinism_hash,
            latency_ms=total_latency
        )

# =====================================================================
# FASTAPI APPLICATION
# =====================================================================
engine = OSHASafetyEngine()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} started on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    yield
    logger.info(f"{ENGINE_NAME} shutting down")

app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    metrics = telemetry_collector.get_metrics()
    return HealthResponse(
        status="operational",
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        total_queries=metrics.get("total_queries", 0),
        avg_latency_ms=metrics.get("avg_latency_ms", 0.0),
        cache_hit_rate=metrics.get("cache_hit_rate", 0.0),
        uptime_seconds=time.time() - engine.start_time
    )

@app.post("/query", response_model=AnalysisResponse)
async def query(request: AnalysisRequest):
    """Main query endpoint"""
    try:
        return engine.analyze(request)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics():
    """Telemetry metrics endpoint"""
    return telemetry_collector.get_metrics()

@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine topics"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "primary_authority": d.primary_authority[0] if d.primary_authority else None
            }
            for d in DOCTRINE_CACHE
        ]
    }

# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
