"""
OFE08 - Wellhead Equipment Analysis Engine
ECHO OMEGA PRIME - Tax Intelligence Engine (TIE) Architecture

Domain: Wellhead & Christmas Tree Equipment Engineering
Port: 9008
Version: 1.0.0
Lines: 1400+

API 6A compliant wellhead equipment analysis covering casing heads, tubing heads,
christmas trees, pressure ratings (2000-20000 PSI), material classes (AA-HH),
PSL levels, seal technologies, and manufacturer-specific systems.
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
    "logs/ofe08_wellhead_{time:YYYY-MM-DD}.log",
    rotation="500 MB",
    retention="30 days",
    level="DEBUG"
)


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS & DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════

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
    PRESSURE_RATING = "PRESSURE_RATING"
    MATERIAL_CLASS = "MATERIAL_CLASS"
    SEAL_TECHNOLOGY = "SEAL_TECHNOLOGY"
    API_COMPLIANCE = "API_COMPLIANCE"
    EQUIPMENT_SELECTION = "EQUIPMENT_SELECTION"
    TESTING_PROCEDURE = "TESTING_PROCEDURE"
    SAFETY_SYSTEM = "SAFETY_SYSTEM"
    INSTALLATION = "INSTALLATION"
    MAINTENANCE = "MAINTENANCE"
    MANUFACTURER_SPEC = "MANUFACTURER_SPEC"


@dataclass
class DoctrineBlock:
    """Single doctrine block with full reasoning framework"""
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
    last_accessed: Optional[datetime] = None
    access_count: int = 0


@dataclass
class TelemetryData:
    """Query telemetry tracking"""
    query_id: str
    timestamp: datetime
    doctrine_blocks_triggered: List[str]
    latency_ms: float
    response_mode: ResponseMode
    confidence_level: ConfidenceLevel
    error_domain: Optional[str] = None


class QueryRequest(BaseModel):
    query: str = Field(..., description="Wellhead equipment analysis query")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis context zone")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class QueryResponse(BaseModel):
    query_id: str
    response: str
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    latency_ms: float
    determinism_hash: str
    mode: ResponseMode
    zone: AnalysisZone
    timestamp: str


# ═══════════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 30+ WELLHEAD EQUIPMENT BLOCKS
# ═══════════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="API 6A Pressure Rating Selection",
        keywords=["pressure rating", "API 6A", "working pressure", "PSI", "rating class"],
        conclusion_template=[
            "Wellhead equipment must be rated for maximum anticipated surface pressure plus safety margin.",
            "API 6A pressure ratings range from 2000 PSI to 20000 PSI in standardized increments.",
            "Operating pressure should not exceed 75% of rated working pressure under normal conditions."
        ],
        reasoning_framework="""
API 6A-2018 establishes pressure rating requirements for wellhead equipment:
1) Standard pressure ratings: 2000, 3000, 5000, 10000, 15000, 20000 PSI
2) Rated working pressure = maximum allowable surface pressure
3) Test pressure = 1.5x rated working pressure (hydrostatic cold test)
4) Design margin: typically operate at ≤75% rated pressure
5) Temperature derating: ratings apply at specific temperature classes
6) Pressure containment verification through API 6A test procedures

Selection methodology:
- Calculate maximum anticipated surface pressure (MASP)
- Add safety margin (typically 25-50% depending on well conditions)
- Select next standard rating above calculated requirement
- Verify temperature class compatibility with expected service
- Ensure all wellhead components share same or higher rating
- Consider future well operations (stimulation, workover) that may increase pressure

Failure to properly rate equipment leads to catastrophic blowouts.
        """,
        key_factors=[
            "Maximum anticipated surface pressure (MASP) calculation",
            "Temperature class compatibility (K, L, M, N, P, Q, R, S, T, U)",
            "Safety margin above operating pressure",
            "Future operations pressure requirements",
            "Test pressure capabilities (1.5x rating)",
            "Component compatibility across wellhead stack",
            "Material class pressure-temperature limitations"
        ],
        primary_authority=[
            "API Spec 6A-2018 (Wellhead and Christmas Tree Equipment)",
            "API Spec 6AV1 (Validation of 6A Equipment)",
            "ASME B31.3 (Process Piping pressure design)"
        ],
        burden_holder="Equipment specifier/operator",
        adversary_position="Lower pressure rating reduces cost, may be adequate for current conditions",
        counter_arguments=[
            "Understated MASP due to incomplete reservoir data",
            "Future stimulation operations may exceed current pressure rating",
            "Wellbore integrity issues can cause unexpected pressure spikes",
            "Temperature effects on pressure rating often overlooked",
            "Test pressure requirements may exceed facility capabilities"
        ],
        resolution_strategy="Conservative rating selection with documented MASP calculation and future operations analysis",
        entity_scope="All wellhead equipment including casing heads, tubing heads, christmas trees",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API 6A provides clear pressure rating standards; MASP calculation requires reservoir data",
        controlling_precedent="API 6A-2018 Section 4 (Pressure Rating Requirements)",
        issue_category=IssueCategory.PRESSURE_RATING
    ),

    DoctrineBlock(
        topic="Material Class Selection (API 6A)",
        keywords=["material class", "AA BB CC DD EE FF HH", "H2S service", "sour service", "NACE"],
        conclusion_template=[
            "Material class must match service environment including H2S, CO2, chlorides, and temperature.",
            "Classes AA through HH provide increasing corrosion resistance and mechanical properties.",
            "H2S service requires NACE MR0175 compliance regardless of material class designation."
        ],
        reasoning_framework="""
API 6A material classes (AA, BB, CC, DD, EE, FF, HH) define:
1) Minimum yield strength (varies by class)
2) Corrosion resistance level
3) Temperature service limits
4) Hardness restrictions for sour service

Material class selection criteria:
AA - Carbon steel, sweet service, non-corrosive, <180°F
BB - Carbon steel, sweet service, upgraded mechanical properties
CC - Low alloy steel, mildly corrosive, higher temperature
DD - Chromium alloy (1-5% Cr), CO2 service, moderate H2S
EE - Chromium alloy (5-9% Cr), severe CO2, limited H2S
FF - High alloy (9-13% Cr), sour service, high temperature
HH - Corrosion resistant alloy (CRA), severe sour/corrosive

H2S service (sour) requires:
- NACE MR0175/ISO 15156 compliance
- Hardness limits: HRC 22 for carbon/low alloy steels
- Hardness testing of all pressure-containing components
- Material traceability documentation
- Specific welding procedures (NACE qualified)

Chloride stress corrosion cracking concerns with austenitic stainless steels.
Temperature limits vary by class; high temp may require upgrade.
        """,
        key_factors=[
            "H2S partial pressure (sour service threshold: >0.05 psia H2S)",
            "CO2 partial pressure and aqueous phase pH",
            "Chloride concentration (pitting/SCC risk)",
            "Operating temperature range",
            "Mechanical property requirements (yield strength)",
            "Hardness testing requirements for sour service",
            "Welding procedure compatibility",
            "Material traceability and MTR documentation"
        ],
        primary_authority=[
            "API Spec 6A-2018 Annex F (Material Classes)",
            "NACE MR0175/ISO 15156 (Sour Service)",
            "API Spec 6AV1 (Material validation testing)"
        ],
        burden_holder="Operator and equipment manufacturer",
        adversary_position="Lower material class reduces cost; lab data may not indicate H2S presence",
        counter_arguments=[
            "Reservoir souring over time introduces H2S not present initially",
            "Bacterial sulfate reduction can generate H2S in waterflood",
            "Temperature spikes during operations may exceed class limits",
            "Material class stamping errors in supply chain",
            "Inadequate hardness testing of welds and HAZ"
        ],
        resolution_strategy="Conservative material class selection with sour service assumption unless proven otherwise; full NACE compliance",
        entity_scope="All pressure-containing wellhead components",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API 6A and NACE standards well-defined; reservoir chemistry may evolve",
        controlling_precedent="API 6A Annex F + NACE MR0175 Table A.1",
        issue_category=IssueCategory.MATERIAL_CLASS
    ),

    DoctrineBlock(
        topic="PSL (Product Specification Level) Requirements",
        keywords=["PSL", "PSL-1", "PSL-2", "PSL-3", "PSL-4", "quality level", "testing"],
        conclusion_template=[
            "PSL levels (1-4) define manufacturing quality and testing requirements.",
            "PSL-3 and PSL-4 require supplemental NDE, PMI, and mechanical testing.",
            "Higher PSL increases equipment reliability but also cost and lead time."
        ],
        reasoning_framework="""
API 6A defines four Product Specification Levels:

PSL-1 (Standard):
- Basic manufacturing requirements
- Limited NDE (visual, dimensional)
- Standard material testing per ASTM
- Hydrostatic testing at 1.5x rated pressure
- Lowest cost, shortest lead time

PSL-2 (Enhanced):
- PSL-1 requirements plus:
- Supplemental NDE (MT or PT of critical areas)
- PMI (Positive Material Identification) verification
- Enhanced documentation and traceability

PSL-3 (Premium):
- PSL-2 requirements plus:
- 100% MT or PT of welds
- Full PMI of all pressure-containing materials
- Mechanical property testing of production lots
- Enhanced quality control documentation
- Pressure testing of each component

PSL-4 (Maximum):
- PSL-3 requirements plus:
- Ultrasonic testing (UT) of forgings and castings
- Radiographic testing (RT) of welds
- Impact testing (Charpy V-notch) for low temp service
- Full traceability to heat/lot for all materials
- Witnessed testing by third party

Selection criteria:
- Well criticality (development vs exploration)
- Consequence of failure (offshore, high pressure, populated area)
- Regulatory requirements (some jurisdictions mandate PSL-3+)
- Operator specifications (IOCs typically require PSL-3 minimum)
- Service conditions (sour service often requires PSL-3+)
        """,
        key_factors=[
            "Well criticality and consequence of failure",
            "Service environment severity (sour, high pressure, high temp)",
            "Regulatory requirements by jurisdiction",
            "Operator company specifications",
            "NDE coverage requirements",
            "Material traceability needs",
            "Cost and schedule constraints",
            "Quality assurance program capability of manufacturer"
        ],
        primary_authority=[
            "API Spec 6A-2018 Section 7 (PSL Requirements)",
            "API Spec 6AV1 (Validation and verification testing)",
            "ISO 10423 (Petroleum and natural gas industries wellhead equipment)"
        ],
        burden_holder="Purchaser specifies PSL; manufacturer executes",
        adversary_position="PSL-1 meets minimum API requirements at lower cost",
        counter_arguments=[
            "Hidden manufacturing defects only detected by PSL-3/4 NDE",
            "Material substitution/counterfeit parts not caught by PSL-1",
            "Weld defects in critical areas lead to catastrophic failures",
            "Cost of failure far exceeds incremental PSL upgrade cost",
            "Regulatory trends toward mandatory higher PSL levels"
        ],
        resolution_strategy="PSL-3 minimum for critical wells; PSL-4 for offshore/sour service/high consequence",
        entity_scope="All API 6A wellhead and tree components",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="PSL requirements clearly defined; selection depends on risk tolerance",
        controlling_precedent="API 6A Section 7 + ISO 10423",
        issue_category=IssueCategory.API_COMPLIANCE
    ),

    DoctrineBlock(
        topic="Casing Head (Braden Head) Configuration",
        keywords=["casing head", "braden head", "surface casing", "casing spool", "bottom flange"],
        conclusion_template=[
            "Casing head provides structural foundation and first pressure barrier for wellhead stack.",
            "Bottom connection must match surface casing size and thread type (welded or threaded).",
            "Top flange rating and size must accommodate subsequent casing strings and pressure."
        ],
        reasoning_framework="""
Casing head (historically "braden head") functions:
1) Structural support: transfers wellhead weight to surface casing
2) Primary pressure barrier: seals around intermediate casing
3) Annulus access: side outlets for monitoring/servicing casing annuli
4) Foundation: provides base flange for stacking additional wellhead components

Design considerations:
Bottom connection:
- Match surface casing OD (typically 13-3/8", 16", 18-5/8", 20")
- Threaded (API round, buttress) or weld-on (preferred for high pressure)
- Weld-on eliminates thread leak path, provides stronger connection
- Thread sealant selection critical for threaded connections

Top flange:
- API 6A flanged connection (studded or hub)
- Rating ≥ maximum anticipated casing pressure
- Size sufficient for next casing string to pass through bore
- Typical sizes: 11", 13-5/8", 16-3/4", 21-1/4" (API 6A standard)

Annulus outlets:
- Typically 2" NPT or flanged connections
- Monitor intermediate/surface casing annulus pressure
- Injection point for corrosion inhibitor
- Vent/kill operations access

Casing hanger:
- Slip type (most common): mechanical slips grip casing OD
- Mandrel type: threaded connection to casing
- Must seal annulus and support casing weight
- Seal types: elastomeric (low/medium temp) or metal (high temp/pressure)
        """,
        key_factors=[
            "Surface casing size and thread type",
            "Maximum surface/intermediate annulus pressure",
            "Next casing string size (determines bore requirement)",
            "Wellhead stack height and weight",
            "Annulus monitoring requirements",
            "Temperature service (affects seal selection)",
            "Casing hanger type compatibility",
            "Installation method (slip vs mandrel)"
        ],
        primary_authority=[
            "API Spec 6A-2018 (Casing head requirements)",
            "API RP 96 (Deepwater Well Design and Construction)",
            "NORSOK D-010 (Well integrity in drilling and well operations)"
        ],
        burden_holder="Well designer/drilling engineer",
        adversary_position="Standard casing head configuration adequate; cost-driven selection",
        counter_arguments=[
            "Underrated casing head for future pressure conditions",
            "Annulus pressure buildup (APB) exceeds casing head rating",
            "Inadequate bore size prevents running larger completion equipment",
            "Casing hanger seal failure due to temperature/pressure cycling",
            "Corrosion in casing annulus due to inadequate monitoring"
        ],
        resolution_strategy="Conservative pressure rating; weld-on connection; metal seals for harsh service",
        entity_scope="Surface and intermediate casing head assemblies",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established design practices; annulus pressure prediction uncertain",
        controlling_precedent="API 6A Section 5 (Wellhead components)",
        issue_category=IssueCategory.EQUIPMENT_SELECTION
    ),

    DoctrineBlock(
        topic="Tubing Head Spool and Hanger",
        keywords=["tubing head", "spool", "tubing hanger", "pack-off", "cross-over flange"],
        conclusion_template=[
            "Tubing head provides landing point for tubing hanger and seals production annulus.",
            "Must accommodate production pressure, temperature, and annulus fluids.",
            "Crossover flange transitions to christmas tree connection."
        ],
        reasoning_framework="""
Tubing head spool components and functions:

Bottom flange:
- Connects to top of uppermost casing spool
- Matches casing spool top flange size and rating
- Studded or hub-type connection per API 6A

Bore:
- Allows passage of tubing hanger
- Side outlet(s) for production casing annulus access
- Typically 7-1/16", 9", 11" nominal bore

Tubing hanger landing area:
- Precision machined surface for hanger seal
- Back-pressure valve (BPV) threading if applicable
- Test port access for hanger seal verification

Top flange (crossover):
- Connects to christmas tree bottom flange
- May be different size/rating than bottom flange (crossover spool)
- Typical tree connection: 7-1/16" or 9" for most production wells

Tubing hanger types:
1) Mandrel hanger:
   - Threaded directly to tubing string
   - Rotation during installation sets tubing depth
   - Seal bore in hanger body
   - Advantage: simple, reliable
   - Disadvantage: tubing rotation required

2) Slip hanger:
   - Mechanical slips grip tubing OD
   - Does not require tubing rotation
   - Seal bore in hanger body or spool
   - Advantage: no rotation needed, easier installation
   - Disadvantage: more complex mechanism

Pack-off/seal systems:
- Primary seal: metal-to-metal (high temp/pressure) or elastomeric
- Secondary seal: backup for primary
- Test port allows pressure testing of seal integrity
- Seal energization: some designs use annulus pressure to energize seal

Annulus access:
- Side outlet on spool body (typically 2" flanged)
- Monitor production casing annulus pressure
- Injection point for corrosion inhibitor
- Gas lift injection (if applicable)
- Kill/circulation operations

Test ports:
- Hanger seal test port: verify seal integrity after installation
- VR (valve removal) plug if tree has retrievable valves
        """,
        key_factors=[
            "Production pressure and temperature",
            "Tubing size and weight",
            "Annulus fluid type (gas, oil, water, corrosive)",
            "Seal technology (metal vs elastomeric)",
            "Hanger installation method (mandrel vs slip)",
            "Christmas tree compatibility",
            "Annulus access requirements (gas lift, monitoring)",
            "Seal testing procedure capability"
        ],
        primary_authority=[
            "API Spec 6A-2018 (Tubing head requirements)",
            "API RP 5C1 (Care and use of casing and tubing)",
            "Manufacturer specifications (Cameron, FMC, Dril-Quip)"
        ],
        burden_holder="Completion engineer",
        adversary_position="Standard tubing head adequate; seal testing optional",
        counter_arguments=[
            "Tubing hanger seal leak causes annulus pressure buildup",
            "Inadequate seal for high differential pressure across hanger",
            "Thermal cycling degrades elastomeric seals",
            "Hanger installation damage not detected without seal test",
            "Corrosion in production annulus due to seal bypass"
        ],
        resolution_strategy="Metal seals for high pressure/temp; mandatory seal testing; redundant seal design",
        entity_scope="All tubing head assemblies",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Design standards clear; seal performance depends on installation quality",
        controlling_precedent="API 6A Section 5.3 (Tubing heads)",
        issue_category=IssueCategory.EQUIPMENT_SELECTION
    ),

    DoctrineBlock(
        topic="Christmas Tree Selection (Vertical vs Horizontal)",
        keywords=["christmas tree", "vertical tree", "horizontal tree", "flowing tree", "tree configuration"],
        conclusion_template=[
            "Vertical trees provide inline flow path; traditional design for most applications.",
            "Horizontal trees offer side outlet flow; better for high rate wells and workover operations.",
            "Selection depends on flow rate, wellbore access needs, and platform layout."
        ],
        reasoning_framework="""
Christmas tree configurations:

VERTICAL TREE:
- Flow path: up through tubing hanger, through master valves, out side outlet
- Configuration: swab valve (top), upper master valve, lower master valve, wing valve
- Advantages:
  * Compact vertical footprint
  * Traditional design, widely available
  * Lower cost than horizontal tree
  * Simpler valve arrangement
- Disadvantages:
  * Side outlet flow introduces 90° turn (pressure drop, erosion)
  * Difficult to access wellbore through tree for wireline operations
  * Flow velocity through master valves can cause erosion
- Typical applications: low-moderate rate wells, land operations

HORIZONTAL TREE:
- Flow path: horizontal outlet aligned with tubing bore
- Configuration: master valves (vertical stack), wing valve (horizontal outlet)
- Advantages:
  * Inline flow path reduces pressure drop and erosion
  * Better for high rate gas wells (reduced velocity through valves)
  * Easier wellbore access for wireline/coiled tubing through swab valve
  * Production wing separate from kill wing (dual wing trees)
- Disadvantages:
  * Larger horizontal footprint (platform space consideration)
  * Higher cost
  * More complex valve arrangement
- Typical applications: high rate wells, offshore platforms, frequent intervention

DUAL-WING HORIZONTAL TREE:
- Two horizontal outlets: production wing + kill/injection wing
- Enhanced redundancy and operational flexibility
- Allows simultaneous production and annulus monitoring/injection
- Common in subsea and offshore platform wells

Component specifications:
- Master valves: gate or ball type, must match tree pressure rating
- Wing valves: isolate flowline, same or higher rating than tree
- Swab valve: top of tree, allows wellbore access for wireline
- Side outlets: typically 2-1/16" or 3-1/16" flanged connections
- Tree cap: blind flange or crown plug to seal top of tree

Tree pressure ratings follow API 6A standards (2000-20000 PSI).
All tree components must be same or higher rating as weakest link.
        """,
        key_factors=[
            "Production rate and fluid velocity",
            "Wellbore access frequency (wireline interventions)",
            "Platform space constraints",
            "Flow erosion considerations",
            "Pressure drop requirements",
            "Operational redundancy needs",
            "Cost constraints",
            "Offshore vs land installation"
        ],
        primary_authority=[
            "API Spec 6A-2018 (Christmas tree equipment)",
            "API Spec 6AV1 (Tree validation testing)",
            "ISO 10423 (Petroleum wellhead equipment)"
        ],
        burden_holder="Facilities/completion engineer",
        adversary_position="Vertical tree adequate and lower cost for most wells",
        counter_arguments=[
            "High velocity erosion in vertical tree side outlets",
            "Wireline operations difficult through vertical tree",
            "Pressure drop impacts deliverability in high rate wells",
            "Valve failure in single-wing tree shuts in well completely",
            "Platform expansion requires horizontal tree footprint"
        ],
        resolution_strategy="Horizontal tree for high rate, frequent intervention, offshore; vertical tree for land, low-moderate rate",
        entity_scope="All christmas tree assemblies",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Tree selection well-understood; site-specific factors vary",
        controlling_precedent="API 6A Section 5.4 (Christmas tree equipment)",
        issue_category=IssueCategory.EQUIPMENT_SELECTION
    ),

    DoctrineBlock(
        topic="Choke Valve Selection (Positive vs Adjustable)",
        keywords=["choke", "positive choke", "adjustable choke", "bean", "flow control"],
        conclusion_template=[
            "Positive chokes (fixed orifice beans) provide reliable erosion-resistant flow restriction.",
            "Adjustable chokes allow remote flow rate control but have higher erosion risk.",
            "Selection depends on well stability, production optimization needs, and fluid properties."
        ],
        reasoning_framework="""
Choke types and applications:

POSITIVE CHOKE (Fixed Bean):
Design:
- Fixed orifice (bean) installed in choke body
- Orifice sizes: 1/64" increments (e.g., 10/64", 12/64", 16/64")
- Tungsten carbide or ceramic bean material for erosion resistance
- Simple construction, no moving parts

Advantages:
- Highly erosion-resistant (hardened orifice material)
- No moving parts to fail
- Precise, repeatable flow restriction
- Lower cost than adjustable chokes
- Reliable in high-velocity gas/sand service

Disadvantages:
- Requires well shutdown to change bean size
- No remote flow rate adjustment
- Must stock multiple bean sizes
- Cannot respond to changing well conditions without intervention

Applications:
- High-velocity gas wells with erosive fluids
- Sand production (solids erosion concern)
- Wells with stable flow characteristics
- Remote locations where adjustability not critical

ADJUSTABLE CHOKE:
Design:
- Variable orifice (needle and seat or cage design)
- Manual (hand wheel) or automatic (pneumatic/hydraulic actuator)
- Trim materials: tungsten carbide, stellite, ceramic

Advantages:
- Remote flow rate control (if actuated)
- Optimize production without well shutdown
- Respond to changing reservoir conditions
- Single device covers wide flow range

Disadvantages:
- Erosion of trim in high-velocity service
- Mechanical complexity (moving parts)
- Higher cost and maintenance
- Potential for actuator failure
- Trim damage from solids production

Applications:
- Wells requiring frequent flow rate changes
- Automated well control systems
- Low-moderate erosion environments
- Gas lift optimization
- Offshore platforms with remote operation

Sizing methodology:
- Subcritical flow (liquid): ΔP < 0.5 × upstream pressure
- Critical flow (gas): sonic velocity at throat
- Multiphase flow requires iterative calculation
- Erosional velocity limit: Ve = C / √ρm (API RP 14E)
- C factor typically 100-150 for continuous service

Materials:
- Standard: 316 stainless steel body
- Erosive service: tungsten carbide trim
- Extreme service: ceramic (alumina, zirconia) trim
- Body may require armor for sand-laden fluids
        """,
        key_factors=[
            "Flow rate stability and adjustment needs",
            "Fluid erosivity (velocity, solids content)",
            "Remote operation requirements",
            "Pressure drop across choke",
            "Multiphase flow conditions",
            "Maintenance access and frequency",
            "Trim material compatibility",
            "Cost and reliability priorities"
        ],
        primary_authority=[
            "API RP 14E (Design and installation of offshore production platform piping systems)",
            "ISA 75.01 (Control valve sizing)",
            "Manufacturer specs (Mokveld, Master Flo, Cameron)"
        ],
        burden_holder="Production/facilities engineer",
        adversary_position="Adjustable choke provides operational flexibility worth erosion risk",
        counter_arguments=[
            "Adjustable choke trim erosion leads to uncontrolled flow",
            "Actuator failure in unmanned offshore platform",
            "Positive choke requires frequent bean changes (operational cost)",
            "Erosional velocity exceeded in high-rate gas wells",
            "Solids production destroys adjustable choke trim"
        ],
        resolution_strategy="Positive choke for erosive service; adjustable for stable wells with optimization needs",
        entity_scope="Surface chokes on christmas trees and flowlines",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Choke sizing well-defined; erosion prediction uncertain for new wells",
        controlling_precedent="API RP 14E Section 5 (Flow-induced erosion)",
        issue_category=IssueCategory.EQUIPMENT_SELECTION
    ),

    DoctrineBlock(
        topic="Wellhead Seal Technology (Metal vs Elastomeric)",
        keywords=["seal", "metal seal", "elastomeric seal", "energized seal", "pack-off"],
        conclusion_template=[
            "Metal-to-metal seals required for high temperature (>350°F) and high pressure applications.",
            "Elastomeric seals suitable for moderate conditions; lower cost but limited service life.",
            "Seal energization (pressure or mechanical) critical for reliability."
        ],
        reasoning_framework="""
Wellhead seal technologies:

ELASTOMERIC SEALS:
Materials:
- Nitrile (NBR): -40°F to 250°F, oil/gas service, economical
- Viton (FKM): -20°F to 400°F, sour gas, superior chemical resistance
- HNBR: -30°F to 300°F, high strength, sour service
- Aflas (FEPM): -10°F to 400°F, H2S and steam service, expensive

Design types:
- O-rings: static seals, radial or axial compression
- T-seals: pressure-energized (higher pressure enhances seal)
- V-packs: multi-lip seals for reciprocating applications

Advantages:
- Lower cost than metal seals
- Easy installation
- Tolerance for minor surface imperfections
- Immediate seal upon installation

Disadvantages:
- Temperature limited (<400°F typically)
- Aging/degradation over time (compression set)
- Chemical attack in sour/corrosive service
- Explosive decompression (rapid gas expansion damages seal)
- Limited reusability

METAL SEALS:
Materials:
- Soft iron ring (low pressure, single use)
- Stainless steel (reusable, moderate pressure)
- Inconel 625/718 (high temp, corrosive service)
- Duplex/super duplex (sour service)

Design types:
- Lens ring (oval cross-section): API 6A Type R flange
- RX/BX ring (pressure-energized): self-sealing with pressure
- Delta ring: spring-energized metal seal
- Flexitallic spiral wound: metal/graphite composite

Advantages:
- High temperature capability (>400°F to 1000°F+)
- High pressure rating (up to 20,000 PSI+)
- Chemical/corrosion resistance
- No aging/degradation
- Reusable (depending on type)
- Resistant to explosive decompression

Disadvantages:
- Higher cost than elastomers
- Requires precision machined sealing surfaces
- Installation more critical (torque, alignment)
- May require higher seating stress

SEAL ENERGIZATION:
Pressure-energized:
- Seal geometry directs pressure to enhance sealing force
- Higher differential pressure = tighter seal
- T-seals, RX rings designed for pressure energization

Mechanically energized:
- Spring or wave washer provides sealing force
- Independent of pressure
- Delta rings, spring-energized seals

Selection criteria:
- Temperature: >350°F requires metal seals
- Pressure: >10,000 PSI typically requires metal
- Cycling: thermal/pressure cycling degrades elastomers
- Chemical: H2S, CO2, aromatics may require metal or upgraded elastomer
- Reusability: metal seals often reusable; elastomers typically single-use
        """,
        key_factors=[
            "Maximum service temperature",
            "Pressure rating and differential pressure",
            "Chemical composition of fluids (H2S, CO2, aromatics)",
            "Thermal/pressure cycling frequency",
            "Reusability requirements",
            "Explosive decompression risk (high pressure gas)",
            "Seal surface finish and precision",
            "Installation procedure complexity"
        ],
        primary_authority=[
            "API 6A Annex B (Seal qualification testing)",
            "ASME B16.20 (Metallic gaskets for pipe flanges)",
            "Parker O-Ring Handbook (Elastomer selection)"
        ],
        burden_holder="Equipment designer and operator",
        adversary_position="Elastomeric seals adequate for most oil wells; metal seals over-specified",
        counter_arguments=[
            "Unexpected temperature excursions during operations exceed elastomer limits",
            "Seal degradation over time not detected until leakage occurs",
            "Explosive decompression during blowdown destroys elastomeric seals",
            "Chemical attack in mixed H2S/CO2 service accelerates elastomer failure",
            "Metal seal cost justified by long service life and reliability"
        ],
        resolution_strategy="Metal seals for high temp/pressure, sour service, critical applications; elastomers for moderate service",
        entity_scope="All wellhead flange connections and hanger seals",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Seal technology well-established; service conditions may exceed initial assumptions",
        controlling_precedent="API 6A Annex B (Seal performance testing)",
        issue_category=IssueCategory.SEAL_TECHNOLOGY
    ),

    DoctrineBlock(
        topic="Flanged vs Studded Connections",
        keywords=["flange", "studded connection", "hub flange", "compact flange", "API 6BX"],
        conclusion_template=[
            "Studded flanges (API 6BX) provide compact, high-integrity connections for wellhead stacks.",
            "Hub-type flanges (ASME B16.5) traditional but larger envelope and lower pressure rating.",
            "Studded connections preferred for high pressure and subsea applications."
        ],
        reasoning_framework="""
Wellhead flange connection types:

STUDDED CONNECTIONS (API 6BX):
Design:
- Threaded studs installed in lower flange
- Upper flange nuts down onto studs
- Metal ring gasket (lens or RX type) seals between flanges
- Compact design (smaller OD than equivalent hub flange)

Specifications:
- API 6BX: "Compact flanged connections" for wellhead service
- Pressure ratings: 2000-20000 PSI
- Sizes: 1-13/16" through 21-1/4"
- Ring gasket type designations (R, RX, BX)

Advantages:
- High pressure rating in compact envelope
- Positive gasket retention (trapped in groove)
- Reduced flange OD (space savings on platform)
- Better fatigue resistance (studs vs bolts)
- Preferred for subsea wellheads (compact, reliable)

Disadvantages:
- Studs must be installed/removed individually (time-consuming)
- Ring gasket required (higher cost than flat gasket)
- Precision machining required for ring groove

HUB-TYPE FLANGES (ASME B16.5):
Design:
- Raised face (RF) or ring-type joint (RTJ)
- Bolts pass through both flanges
- Spiral wound or flat gasket (RF) or metal ring (RTJ)

Specifications:
- ASME B16.5: Pipe flanges and flanged fittings
- Pressure class: 150-2500 (PSI rating varies with temp)
- Sizes: 1/2" through 24"

Advantages:
- Through-bolting faster to assemble/disassemble
- Standard industrial flange (widely available)
- Lower cost for low pressure applications
- Flat face (FF) or raised face (RF) for varied gasket types

Disadvantages:
- Larger OD than equivalent API 6BX studded flange
- Lower pressure rating than studded connections
- Gasket blowout risk at high pressure
- Class 2500 maximum (~6000 PSI at moderate temp)

API 6A FLANGE TYPES:
Type 6B: Studded and threaded connections
Type 6BX: Compact studded connections (most common wellhead)
Ring gasket types:
- R: Oval cross-section (API 6A Type R)
- RX: Pressure-energized ring
- BX: Pressure-energized ring (similar to RX)

Bolt/stud materials:
- ASTM A193 Grade B7 (chrome-moly): most common, -50°F to 1000°F
- ASTM A193 Grade B7M (modified): sour service (NACE)
- ASTM A193 Grade B16 (chrome-moly-vanadium): high temp
- L7M: low alloy for low temperature and sour service

Torque requirements:
- Controlled torque critical for proper seal
- Under-torque: insufficient gasket compression, leak
- Over-torque: stud yield, thread damage
- Torque tables in API 6A based on stud size and material
        """,
        key_factors=[
            "Pressure rating requirements",
            "Space constraints (platform envelope)",
            "Assembly/disassembly frequency",
            "Subsea vs surface application",
            "Temperature service",
            "Sour service (requires NACE studs)",
            "Gasket type compatibility",
            "Cost and availability"
        ],
        primary_authority=[
            "API Spec 6A-2018 (Flanged connections)",
            "API Spec 6BX (Compact flanged connections)",
            "ASME B16.5 (Pipe flanges and flanged fittings)"
        ],
        burden_holder="Equipment designer",
        adversary_position="ASME B16.5 flanges adequate and more economical",
        counter_arguments=[
            "B16.5 Class 2500 pressure rating inadequate for high pressure wells",
            "Hub flange OD too large for congested platform",
            "Gasket blowout in ASME flange during pressure transient",
            "Subsea service requires compact, high-integrity API 6BX connection",
            "Studded connection reduces leak risk through positive gasket retention"
        ],
        resolution_strategy="API 6BX studded connections for wellhead service; ASME B16.5 acceptable for low pressure auxiliary",
        entity_scope="All wellhead flange connections",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Flange standards well-defined; proper installation critical",
        controlling_precedent="API 6A Section 6 (Flanged connections)",
        issue_category=IssueCategory.API_COMPLIANCE
    ),

    DoctrineBlock(
        topic="Pressure Testing and Verification (API 6A)",
        keywords=["pressure test", "hydrostatic test", "pneumatic test", "1.5x rating", "test procedure"],
        conclusion_template=[
            "API 6A requires hydrostatic testing at 1.5x rated working pressure for all pressure-containing components.",
            "Test duration, fluid, and acceptance criteria defined by PSL level.",
            "In-service testing verifies integrity after installation and periodically during operation."
        ],
        reasoning_framework="""
API 6A pressure testing requirements:

FACTORY ACCEPTANCE TESTING (FAT):
Hydrostatic test (preferred):
- Test pressure: 1.5x rated working pressure (cold test)
- Test fluid: water, oil, or compatible liquid
- Duration: minimum per API 6A (varies by component and PSL)
- Temperature: ambient (cold test) or elevated (hot test if specified)
- Acceptance: no visible leakage, no pressure decay

Pneumatic test (if hydrostatic not feasible):
- Test gas: air or nitrogen
- Pressure: 1.5x rated working pressure
- Safety precautions: stored energy hazard
- Preferred to avoid pneumatic due to safety risk

PSL-specific test requirements:
PSL-1:
- Hydrostatic test of assembled components
- Visual inspection during test
- Pressure decay monitoring

PSL-2:
- PSL-1 requirements plus:
- Extended hold time
- NDE (MT/PT) of critical areas before test
- PMI verification

PSL-3:
- PSL-2 requirements plus:
- Component testing before assembly
- Assembly testing after component tests
- Documented test procedures and results
- Third-party witness optional

PSL-4:
- PSL-3 requirements plus:
- Mandatory third-party witness
- Full traceability of test results
- Enhanced NDE before and after testing
- Impact testing if low temp service

FIELD INSTALLATION TESTING:
Post-installation pressure test:
- After wellhead assembly, before tree installation
- Test tubing hanger seal: pressure on annulus
- Test casing hangers: pressure on casing annuli
- Verify all connections: flanges, threaded connections

Test methods:
1) Hanger seal test:
   - Isolate annulus below hanger seal
   - Pressure up through test port
   - Hold pressure (typically 30 minutes)
   - Acceptance: <10% pressure decay

2) Flange test:
   - After making up flange, apply test pressure
   - Hold per procedure
   - Inspect for leaks (soap solution, visual)

3) BOP test (if installed):
   - Low pressure (200-300 PSI) leak test
   - High pressure (70% of rating) function test
   - API Spec 53 (BOP testing) requirements

IN-SERVICE TESTING:
Periodic testing:
- Regulatory requirements vary by jurisdiction
- Typical: annual pressure test of wellhead and tree
- After workover: retest all connections and seals
- After pressure/temperature excursion: verify integrity

Test documentation:
- Test charts (pressure vs time)
- Test certification (signed by qualified person)
- NDE reports (if applicable)
- Material certifications (MTRs)
- Traceability to API 6A Monogram license

COMMON TEST FAILURES:
- Seal damage during installation
- Inadequate torque on flanged connections
- Foreign material in seal area
- Thermal expansion during test (false failure)
- Gauge calibration error
- Trapped air in test system (compressibility)
        """,
        key_factors=[
            "Test pressure (1.5x rating)",
            "PSL level requirements",
            "Test fluid selection",
            "Hold time and acceptance criteria",
            "Safety considerations for pneumatic test",
            "Temperature during test",
            "Documentation and traceability",
            "Third-party witness requirements"
        ],
        primary_authority=[
            "API Spec 6A-2018 Section 8 (Testing)",
            "API Spec 6AV1 (Validation testing)",
            "API Spec 53 (BOP testing if applicable)"
        ],
        burden_holder="Manufacturer for FAT; operator for field testing",
        adversary_position="Reduced test pressure or duration acceptable to save time/cost",
        counter_arguments=[
            "Undetected manufacturing defects only revealed by full test pressure",
            "Short hold time misses slow leaks",
            "Pneumatic test misses small leaks (gas more permeable than liquid)",
            "Field installation damage not detected without post-install test",
            "In-service degradation progresses unseen without periodic testing"
        ],
        resolution_strategy="Full API 6A test protocol compliance; no deviations without engineering justification",
        entity_scope="All API 6A wellhead and tree equipment",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Test procedures clearly defined; execution quality varies",
        controlling_precedent="API 6A Section 8 + 6AV1",
        issue_category=IssueCategory.TESTING_PROCEDURE
    ),

    DoctrineBlock(
        topic="Surface Safety Valve (SSV) Requirements",
        keywords=["SSV", "surface safety valve", "SCSSV", "fail-safe", "ESD", "shutdown"],
        conclusion_template=[
            "Surface safety valves (SSV) provide automatic well shutdown upon loss of control signal.",
            "Fail-safe design: valve closes on loss of hydraulic/pneumatic pressure.",
            "Required by regulation for most producing wells; critical safety barrier."
        ],
        reasoning_framework="""
Surface Safety Valve (SSV) systems:

FUNCTION:
- Automatic well shutdown on emergency condition
- Fail-safe closure (spring-close, pressure-open)
- Activated by ESD (Emergency Shutdown) system
- Last line of defense before blowout

TYPES:
Surface-Controlled Subsurface Safety Valve (SCSSV):
- Located downhole in tubing string
- Hydraulic control line from surface
- Flapper or ball valve design
- Discussed in separate doctrine (subsurface equipment)

Surface Safety Valve (SSV) on tree:
- Installed in tree wing or production outlet
- Gate or ball valve type
- Actuated (hydraulic, pneumatic, or electric)
- Fail-closed design

DESIGN REQUIREMENTS:
Fail-safe operation:
- Valve MUST close on loss of control medium (hydraulic/pneumatic pressure)
- Spring or weight-loaded closure
- Power loss, line break, or ESD signal causes closure

Actuation systems:
Hydraulic:
- Hydraulic fluid reservoir and pump
- Pressure opens valve, spring closes valve
- Control panel with manual/auto modes
- Accumulator for backup closure energy

Pneumatic:
- Instrument air or nitrogen supply
- Pressure opens valve, spring closes valve
- Simpler than hydraulic but requires reliable air supply

Electric (less common for fail-safe):
- Motor-operated valve (MOV)
- Requires battery backup for fail-safe operation
- Typically not preferred for primary SSV

Control logic:
- ESD system inputs: process sensors, manual buttons, fire/gas detection
- Redundant control circuits (1oo2, 2oo3 voting)
- Functional safety (SIL rating) per IEC 61508/61511
- Periodic proof testing to verify functionality

REGULATORY REQUIREMENTS:
US (BSEE, state regulations):
- SSV required on all oil/gas producing wells (with exceptions)
- Must close automatically on abnormal conditions
- Regular testing and maintenance required
- SCSSV also required for offshore and some onshore wells

International (varies by jurisdiction):
- NORSOK S-001 (Technical safety) requires SSV
- ISO 10418 (Petroleum and natural gas industries - offshore platforms)
- Country-specific regulations (UK, Norway, Middle East, etc.)

ESD ACTIVATION SCENARIOS:
Process conditions:
- High/low pressure
- High temperature
- High H2S concentration
- Flow rate deviation

Safety systems:
- Fire detection
- Gas detection
- Manual ESD button activation
- Loss of utilities (power, instrument air)

TESTING AND MAINTENANCE:
Functional testing:
- Partial stroke test (PST): verify valve movement without full closure
- Full stroke test (FST): complete open-close cycle
- Frequency: monthly PST, annual FST (typical)

Proof testing:
- Verify fail-safe closure on loss of control signal
- SIL verification per IEC 61508
- Document test results

Maintenance:
- Inspect actuator and valve internals
- Replace seals and wear parts
- Verify control system functionality
- Calibrate sensors and transmitters
        """,
        key_factors=[
            "Regulatory requirements (jurisdiction-specific)",
            "Well location (offshore vs onshore)",
            "Production rate and pressure",
            "ESD system architecture (SIL rating)",
            "Actuation method (hydraulic, pneumatic, electric)",
            "Fail-safe verification testing",
            "Control logic redundancy",
            "Maintenance accessibility"
        ],
        primary_authority=[
            "API Spec 6A (SSV valve requirements)",
            "API RP 14C (Analysis, design, installation, and testing of safety systems)",
            "IEC 61511 (Functional safety - process industry)",
            "BSEE regulations (30 CFR 250) for offshore US"
        ],
        burden_holder="Operator",
        adversary_position="SSV not required for low-risk wells; adds cost and complexity",
        counter_arguments=[
            "Regulatory mandate for SSV in most jurisdictions",
            "Well blowout risk without automatic shutdown capability",
            "Human reaction time insufficient in emergency",
            "Insurance/liability considerations require SSV",
            "SSV failure rate low; cost justified by safety benefit"
        ],
        resolution_strategy="Install SSV per regulatory requirements; SIL-rated ESD system; regular proof testing",
        entity_scope="All producing wells (with jurisdiction-specific exceptions)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory requirements clear; system reliability depends on maintenance",
        controlling_precedent="API RP 14C + jurisdiction-specific regulations",
        issue_category=IssueCategory.SAFETY_SYSTEM
    ),

    DoctrineBlock(
        topic="Cameron vs FMC vs Dril-Quip Systems",
        keywords=["Cameron", "FMC", "Dril-Quip", "manufacturer", "OEM", "wellhead system"],
        conclusion_template=[
            "Major OEMs (Cameron/Schlumberger, FMC Technologies, Dril-Quip) have proprietary wellhead systems.",
            "Systems are generally NOT interchangeable; components must match OEM.",
            "Selection affects long-term parts availability, service, and expansion options."
        ],
        reasoning_framework="""
Major wellhead equipment manufacturers:

CAMERON (now Schlumberger Cameron):
History:
- Founded 1920, industry pioneer
- Acquired by Schlumberger 2016
- Largest market share globally

Product lines:
- Type U: compact wellhead system for land/platform
- Type LWS: lightweight wellhead for shallow water
- Type DWR: deepwater riser wellhead
- Compact flanged systems: 2000-20000 PSI

Design characteristics:
- Rugged, field-proven designs
- Wide range of pressure ratings and sizes
- Global service network
- Premium pricing

Advantages:
- Largest installed base (parts availability)
- Comprehensive product line
- Strong engineering support
- Proven reliability

Disadvantages:
- Higher cost than some competitors
- Proprietary designs (vendor lock-in)
- Less customization flexibility

FMC TECHNOLOGIES (now TechnipFMC):
History:
- Merged FMC Corp with Technip 2017
- Strong in subsea systems

Product lines:
- High-pressure surface wellheads
- Subsea wellhead systems
- Horizontal and vertical trees

Design characteristics:
- Innovative designs (compact, lightweight)
- Focus on subsea and deepwater
- Modular systems

Advantages:
- Lightweight designs (weight-critical platforms)
- Subsea expertise
- Competitive pricing

Disadvantages:
- Smaller installed base than Cameron
- Less presence in land markets
- Proprietary designs

DRIL-QUIP:
History:
- Founded 1981
- Focused on premium wellhead systems
- Independent (not part of larger conglomerate)

Product lines:
- High-pressure land/platform wellheads
- Subsea wellhead systems
- Premium drilling and completion equipment

Design characteristics:
- High-quality manufacturing (PSL-3/4 standard)
- Advanced sealing technology
- Customizable designs

Advantages:
- Highest quality reputation
- Innovative seal designs (metal seals)
- Excellent for high-pressure/high-temp applications
- Responsive engineering support

Disadvantages:
- Premium pricing (highest cost)
- Smaller global service network
- Longer lead times

INTERCHANGEABILITY:
General rule: components NOT interchangeable between OEMs
- Flange dimensions may differ (even at same API size)
- Ring groove profiles proprietary
- Thread forms unique to OEM
- Hanger designs incompatible

Exceptions:
- API 6A flanges have standard dimensions (but groove details vary)
- Some aftermarket suppliers provide cross-compatible parts
- Adapter flanges available for some transitions (expensive)

SELECTION STRATEGY:
Greenfield project:
- Select single OEM for entire wellhead system
- Consider installed base in region (parts availability)
- Evaluate total cost of ownership (initial + lifecycle)
- Assess service network coverage

Brownfield/existing fields:
- Match existing OEM for consistency
- Adapter flanges if OEM change unavoidable
- Evaluate obsolescence risk (OEM discontinuing product line)

Factors favoring Cameron:
- Large field with many wells (parts economies of scale)
- Global operations (service network important)
- Standard applications (not pushing technology limits)

Factors favoring FMC:
- Weight-critical platform (lightweight designs)
- Deepwater/subsea wells
- Cost-competitive bid environment

Factors favoring Dril-Quip:
- Ultra-high pressure/temperature wells
- Premium quality requirements
- Custom/specialized applications
- Operator preference for highest reliability

LIFECYCLE CONSIDERATIONS:
Parts availability:
- Cameron: largest inventory, shortest lead times
- FMC: good for common items, longer for specialty
- Dril-Quip: premium parts, longer lead times

Service support:
- Cameron: global network, 24/7 support
- FMC: strong in major basins, limited remote areas
- Dril-Quip: excellent technical support, fewer field locations

Obsolescence risk:
- All OEMs discontinue older product lines over time
- Maintain critical spare parts inventory
- Plan for wellhead replacement in mature fields
        """,
        key_factors=[
            "Initial equipment cost",
            "Total cost of ownership (parts, service)",
            "Installed base in region",
            "Service network coverage",
            "Technical requirements (pressure, temperature, environment)",
            "Lead time and availability",
            "Quality and reliability track record",
            "Existing fleet standardization"
        ],
        primary_authority=[
            "Manufacturer specifications and catalogs",
            "API Spec 6A (minimum requirements, not OEM-specific)",
            "Industry experience and field performance data"
        ],
        burden_holder="Asset owner/operator",
        adversary_position="Lowest cost OEM adequate; interchangeability via adapters",
        counter_arguments=[
            "Proprietary designs create vendor lock-in",
            "Adapter flanges introduce leak points and cost",
            "Mixing OEMs complicates parts inventory and training",
            "Premium cost justified by superior reliability (Dril-Quip)",
            "Installed base drives long-term economics (Cameron)"
        ],
        resolution_strategy="Single OEM per field/platform; select based on technical requirements and lifecycle cost",
        entity_scope="All wellhead system procurement",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="OEM capabilities well-known; lifecycle costs harder to predict",
        controlling_precedent="Manufacturer specifications + field experience",
        issue_category=IssueCategory.MANUFACTURER_SPEC
    ),

    DoctrineBlock(
        topic="Subsea Wellhead vs Surface Wellhead",
        keywords=["subsea wellhead", "mudline wellhead", "subsea tree", "surface wellhead", "platform"],
        conclusion_template=[
            "Subsea wellheads operate on seafloor; require ROV-compatible interfaces and no direct access.",
            "Surface wellheads on platforms allow manual intervention and simpler design.",
            "Subsea systems exponentially more expensive but enable deepwater field development."
        ],
        reasoning_framework="""
Subsea vs Surface wellhead systems:

SUBSEA WELLHEAD (Mudline):
Installation:
- Jetted or drilled into seafloor
- Conductor casing cemented in place
- Wellhead installed during drilling operations
- No platform required (wells tied back to FPSO, spar, or shore)

Design characteristics:
- Compact, heavy-duty construction
- ROV (Remotely Operated Vehicle) interface
- All connections designed for remote actuation
- Vertical tree (horizontal not suitable for seafloor)
- Guide posts for stabbing tools/trees

Components:
- High-pressure wellhead housing
- Casing hangers (18", 16", 13-5/8", etc.)
- Tubing hanger (landed in tree or adapter)
- Subsea tree (wet tree or dry tree)
- Control module (hydraulic/electric)

Advantages:
- Enables deepwater development (no platform depth limit)
- Field layout flexibility (wells spread over area)
- Lower facility cost (no platform for each well)
- Expandable (add wells to existing infrastructure)

Disadvantages:
- Extremely high equipment cost ($5-20M per tree)
- No direct access (all operations via ROV)
- Long lead times (12-24 months for trees)
- Complex control systems (umbilicals, subsea electronics)
- Intervention difficulty (workover spreads, rigs)

SURFACE WELLHEAD (Platform):
Installation:
- Platform structure installed (jacket, jack-up, semi-sub, TLP)
- Conductor through platform to seafloor
- Wellhead installed on deck level
- Direct access for personnel

Design characteristics:
- Conventional land-type wellhead equipment
- Manual or automated valve actuation
- Horizontal or vertical tree options
- Accessible for maintenance

Components:
- Standard API 6A wellhead components
- Surface tree (more options than subsea)
- Flowline connections on deck
- Local ESD and control systems

Advantages:
- Lower equipment cost (1/10 to 1/20 of subsea)
- Direct access for intervention
- Wider range of equipment options
- Faster installation and commissioning
- Easier maintenance and monitoring

Disadvantages:
- Platform required (high cost for deepwater)
- Depth limited by platform type (TLP ~6000 ft, spar ~10,000 ft)
- Environmental exposure (deck equipment)
- Space constraints on platform

SUBSEA TREE TYPES:
Vertical tree:
- Most common subsea configuration
- Tree sits on wellhead via connector
- ROV panel for valve actuation
- Control umbilical to platform/FPSO

Horizontal tree:
- Inline flow path (like surface horizontal tree)
- Less common subsea (more complex connector)
- Better flow characteristics

Wet tree:
- Exposed to seawater
- Used with floating production (FPSO, spar)
- Flowlines along seafloor

Dry tree:
- Inside sealed housing or platform moonpool
- Used with TLP or spar (rigid riser connection)
- Accessible for maintenance (semi-direct access)

CONTROL SYSTEMS:
Subsea:
- Hydraulic control (most common): HPU on platform, umbilical to tree
- Electric control: electric actuators, power/signal in umbilical
- Electrohydraulic: hybrid system
- Multiplexed controls (reduce umbilical complexity)

Surface:
- Pneumatic, hydraulic, or electric local actuation
- Simpler control architecture
- Redundant local power sources

INTERVENTION:
Subsea:
- Workover rigs with riser systems
- Wireline through tree (if designed for it)
- Coiled tubing via riser
- ROV for tree removal/reinstallation
- Very expensive (mobilization, vessel costs)

Surface:
- Standard workover rig or wireline unit
- Direct tree removal
- Lower cost intervention

COST COMPARISON (Order of Magnitude):
Subsea tree system: $5-20M (tree + wellhead + controls)
Surface wellhead: $0.5-2M (wellhead + tree)
Platform: $100M - $1B+ (depends on water depth, capacity)

Economic decision:
- Few wells, shallow water → platform
- Many wells, deepwater → subsea (no platform per well)
- Ultra-deepwater (>5000 ft) → subsea only viable option
        """,
        key_factors=[
            "Water depth",
            "Number of wells in field",
            "Platform infrastructure availability",
            "Development timeline",
            "Intervention frequency expectations",
            "Harsh environment (hurricane, iceberg)",
            "Reservoir characteristics (pressure, temperature)",
            "Economic analysis (NPV, IRR)"
        ],
        primary_authority=[
            "API Spec 17D (Subsea wellhead and tree equipment)",
            "API RP 17B (Recommended practice for subsea systems)",
            "ISO 13628-4 (Subsea wellhead and tree equipment)"
        ],
        burden_holder="Field development planning team",
        adversary_position="Platform-based surface wellheads more cost-effective",
        counter_arguments=[
            "Platform cost prohibitive in deepwater (>3000 ft)",
            "Subsea allows incremental development (add wells as needed)",
            "Platform space limited (subsea adds capacity)",
            "Environmental/regulatory preference for subsea (smaller surface footprint)",
            "Technology maturity makes subsea reliable option"
        ],
        resolution_strategy="Subsea for deepwater, large fields, or no existing platform; surface for shallow water, small fields",
        entity_scope="Field development planning",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Technology selection well-understood; economic assumptions drive decision",
        controlling_precedent="API 17D + economic analysis",
        issue_category=IssueCategory.EQUIPMENT_SELECTION
    ),

    DoctrineBlock(
        topic="Casing Hanger Selection (Slip vs Mandrel)",
        keywords=["casing hanger", "slip hanger", "mandrel hanger", "casing support"],
        conclusion_template=[
            "Slip-type casing hangers use mechanical slips to grip casing OD; most common design.",
            "Mandrel-type hangers thread directly to casing; simpler but require casing rotation.",
            "Selection depends on casing size, weight, installation method, and seal requirements."
        ],
        reasoning_framework="""
Casing hanger design types:

SLIP-TYPE CASING HANGER:
Design:
- Mechanical slips (segments) with teeth grip casing OD
- Slip segments arranged circumferentially around casing
- Setting tool drives slips into casing OD
- Hanger body rests on wellhead bowl (landing shoulder)

Setting mechanism:
- Running tool lowers hanger to landing shoulder
- Hydraulic or mechanical force drives slips outward
- Slip teeth bite into casing OD (creates marks/indentations)
- Running tool released, casing weight transfers to slips

Advantages:
- No casing rotation required during installation
- Can hang casing at any depth (adjust slips before setting)
- Retrievable in some designs (slips can be released)
- Accommodates tolerance in casing OD

Disadvantages:
- More complex mechanism than mandrel
- Slip teeth damage casing OD (not removable without damage)
- Seal system separate from slips (additional components)
- Higher cost than mandrel hangers

Seal options:
- Elastomeric seal in hanger body
- Metal seal in hanger or wellhead bowl
- Test port for post-installation seal verification

MANDREL-TYPE CASING HANGER:
Design:
- Threaded connection directly to casing (male or female thread)
- Hanger body has external seal bore
- Simple, one-piece design

Installation:
- Hanger threaded to casing (requires casing rotation)
- Casing/hanger assembly lowered into wellhead
- Lands on shoulder in wellhead bowl
- No separate setting operation (gravity sets it)

Advantages:
- Simple, reliable design (fewer parts)
- Lower cost than slip-type
- Direct load path from casing to wellhead
- No casing damage (threads only)

Disadvantages:
- Requires casing rotation during installation
- Depth adjustment limited (thread engagement)
- Not easily retrievable (must unscrew casing)
- Thread leak path if sealant fails

Seal options:
- Seal bore on hanger OD (seal in wellhead bowl)
- Elastomeric or metal seals
- Thread sealant on mandrel threads (API modified, CSC, etc.)

PACKOFF-TYPE HANGER:
Design:
- Hybrid between slip and mandrel
- Threaded connection to casing (like mandrel)
- Packoff elements compressed to create seal
- Packoff energized by nut or hydraulic pressure

Installation:
- Thread hanger to casing
- Lower into wellhead
- Energize packoff (tighten nut or apply hydraulic pressure)

Advantages:
- Positive seal energization
- Test port for seal verification
- Combines mandrel simplicity with slip-type sealing

Disadvantages:
- More expensive than simple mandrel
- Requires energization operation (packoff tightening)

SELECTION CRITERIA:
Casing size and weight:
- Large, heavy casing (20", 18-5/8"): slip-type preferred (weight capacity)
- Smaller casing (13-3/8", 9-5/8"): mandrel acceptable

Installation method:
- No casing rotation capability: slip-type required
- Casing rotation acceptable: mandrel option

Seal requirements:
- High differential pressure: metal seals in slip or packoff-type
- Moderate pressure: elastomeric seals acceptable
- Seal testing required: slip or packoff with test port

Future operations:
- Casing may need removal: slip-type (retrievable design)
- Permanent installation: mandrel acceptable

Cost constraints:
- Budget limited: mandrel (lower cost)
- Premium reliability: slip-type (proven for critical wells)

LOAD CAPACITY:
Slip-type:
- Load capacity depends on slip area and tooth penetration
- Designed for full casing weight plus overpull
- Factor of safety typically 2:1 on static casing weight

Mandrel-type:
- Load capacity limited by thread strength
- API round thread: lower capacity
- API buttress thread: higher capacity
- Premium connections: highest capacity

Hanger/wellhead interface:
- Landing shoulder must support casing weight
- Anti-rotation features prevent hanger spin
- Seal bore machined to tight tolerances
        """,
        key_factors=[
            "Casing size and weight",
            "Installation rotation capability",
            "Seal pressure and temperature requirements",
            "Retrievability needs",
            "Cost constraints",
            "Seal testing requirements",
            "Wellhead bowl compatibility",
            "Operator preference and experience"
        ],
        primary_authority=[
            "API Spec 6A (Casing hanger requirements)",
            "Manufacturer specifications (Cameron, FMC, Dril-Quip)",
            "API RP 5C1 (Care and use of casing and tubing)"
        ],
        burden_holder="Drilling/completions engineer",
        adversary_position="Mandrel-type adequate and more economical",
        counter_arguments=[
            "Slip-type more reliable for heavy casing strings",
            "Mandrel threads potential leak path in high pressure wells",
            "Slip design allows field adjustment of hanger depth",
            "Elastomeric seal failure in mandrel hanger (no test port)",
            "Retrievability valuable for future well modifications"
        ],
        resolution_strategy="Slip-type for large casing, high pressure, critical wells; mandrel for smaller casing, cost-driven",
        entity_scope="All casing hanger installations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Design types well-established; installation quality critical",
        controlling_precedent="API 6A + manufacturer specifications",
        issue_category=IssueCategory.EQUIPMENT_SELECTION
    ),

    DoctrineBlock(
        topic="Temperature Class and Derating",
        keywords=["temperature class", "K L M N P Q R S T U", "derating", "temperature effect"],
        conclusion_template=[
            "API 6A temperature classes (K through U) define equipment service temperature ranges.",
            "Pressure ratings derate at elevated temperatures due to material strength reduction.",
            "Derating factors must be applied when operating temperature exceeds ambient."
        ],
        reasoning_framework="""
API 6A Temperature Classes:

STANDARD TEMPERATURE CLASSES:
K: -60°F to 170°F (-51°C to 77°C)
L: -60°F to 180°F (-51°C to 82°C)
M: -60°F to 210°F (-51°C to 99°C)
N: -60°F to 250°F (-51°C to 121°C)
P: -60°F to 300°F (-51°C to 149°C)
Q: -60°F to 350°F (-51°C to 177°C)
R: -60°F to 400°F (-51°C to 204°C)
S: -60°F to 450°F (-51°C to 232°C)
T: -60°F to 500°F (-51°C to 260°C)
U: -60°F to 650°F (-51°C to 343°C)

Lower temperature limit:
- -60°F minimum for all classes
- Impact testing required for service below -20°F (Charpy V-notch)
- Material selection critical for low temp (avoid brittle fracture)

Upper temperature limit:
- Defines maximum safe operating temperature
- Material strength decreases at elevated temperature
- Seal technology limits (elastomers typically <400°F)

MATERIAL STRENGTH vs TEMPERATURE:
Carbon steel:
- Strength decreases ~10% per 100°F above ambient
- Above 800°F: creep becomes concern (time-dependent deformation)

Alloy steels:
- Better high-temp strength retention than carbon steel
- Chrome-moly alloys good to ~1000°F
- Austenitic stainless good to ~1200°F+

PRESSURE DERATING:
Derating methodology:
- Pressure rating at elevated temp = ambient rating × derating factor
- Derating factors from ASME B31.3 Table A-1 (allowable stress)
- Material-specific derating curves

Example (Carbon steel A105):
- Ambient (70°F): 100% allowable stress
- 300°F: ~95% allowable stress (5% derating)
- 500°F: ~85% allowable stress (15% derating)
- 700°F: ~70% allowable stress (30% derating)

ASME B16.5 flange ratings (pressure-temperature):
- Class 150: 285 PSI @ ambient, 180 PSI @ 500°F (37% derating)
- Class 300: 740 PSI @ ambient, 535 PSI @ 500°F (28% derating)
- Class 600: 1480 PSI @ ambient, 1075 PSI @ 500°F (27% derating)

API 6A equipment:
- Rated at specific temperature class
- If operating above rated class: must derate or upgrade material
- Temperature cycling accelerates seal degradation

SEAL LIMITATIONS:
Elastomeric seals:
- NBR (Nitrile): max 250°F
- FKM (Viton): max 400°F
- FFKM (Kalrez): max 600°F
- Degradation accelerates above max temp

Metal seals:
- No temperature degradation in material
- Thermal expansion mismatch can affect sealing
- Required for >400°F service typically

THERMAL CYCLING EFFECTS:
Cycling damage:
- Repeated heating/cooling causes fatigue
- Seal compression set (permanent deformation)
- Differential thermal expansion creates stress
- Flange bolting requires periodic re-torque

Mitigation:
- Metal seals for high-cycle service
- Stress analysis for thermal transients
- Bolt tensioning vs torque (more reliable preload)

OPERATIONAL CONSIDERATIONS:
Start-up/shutdown:
- Temperature swings during operations
- Cold start-up may have different pressure limits than hot operation
- Thermal shock can crack components

Emergency scenarios:
- Well control operations may see temperature spikes
- Steam injection, hot oil circulation
- Must design for maximum credible temperature

SELECTION STRATEGY:
Conservative approach:
- Select temperature class 50-100°F above expected max
- Account for worst-case scenarios (summer ambient + process heat)
- Higher temp class = higher cost (alloy materials)

Material selection:
- Class K-M: carbon steel adequate
- Class N-P: carbon steel or low alloy
- Class Q-R: chrome-moly alloys
- Class S-U: high alloy, stainless, nickel alloys

Seal selection:
- <250°F: Nitrile acceptable
- 250-350°F: Viton recommended
- >350°F: Metal seals required
        """,
        key_factors=[
            "Maximum operating temperature (process + ambient)",
            "Temperature cycling frequency and magnitude",
            "Material strength derating at temperature",
            "Seal technology temperature limits",
            "Emergency/upset condition temperatures",
            "Low temperature impact requirements",
            "Cost of higher temperature class materials",
            "Thermal expansion effects"
        ],
        primary_authority=[
            "API Spec 6A Annex E (Temperature classes)",
            "ASME B31.3 Table A-1 (Allowable stress vs temperature)",
            "API RP 14E (Pressure-temperature ratings)"
        ],
        burden_holder="Equipment designer and process engineer",
        adversary_position="Ambient temperature class adequate; derating not necessary",
        counter_arguments=[
            "Operating temperature exceeds seal limits (leak)",
            "Thermal cycling not accounted for in initial design",
            "Emergency conditions (well control) exceed normal operating temp",
            "Solar heating in desert climates adds 50-100°F to ambient",
            "Derating factor reduces pressure capacity below process requirement"
        ],
        resolution_strategy="Select temperature class above maximum credible temperature; apply derating factors conservatively",
        entity_scope="All pressure-containing wellhead equipment",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Temperature effects well-documented; operating conditions may vary from design",
        controlling_precedent="API 6A Annex E + ASME B31.3",
        issue_category=IssueCategory.PRESSURE_RATING
    ),

    DoctrineBlock(
        topic="PR1 vs PR2 Performance Requirements",
        keywords=["PR1", "PR2", "performance requirement", "qualification", "validation"],
        conclusion_template=[
            "PR1 and PR2 define performance validation levels for API 6A equipment.",
            "PR2 requires supplemental testing including full-scale prototype validation.",
            "Higher PR level increases confidence in equipment performance but adds cost and lead time."
        ],
        reasoning_framework="""
API 6A Performance Requirements (PR):

PR1 (Standard):
Definition:
- Basic performance validation per API 6A
- Design validation through analysis and calculation
- Material testing per ASTM standards
- Prototype testing on critical functions

Requirements:
- Pressure containment verification (hydrostatic test)
- Functional testing (valve operation, seal installation)
- Dimensional verification
- Material certification (MTRs)

Validation approach:
- Engineering calculations demonstrate adequacy
- Limited prototype testing
- Production testing per PSL level

Documentation:
- Design calculations and FEA (if applicable)
- Material certifications
- Test reports (hydrostatic, functional)

PR2 (Enhanced):
Definition:
- Supplemental validation beyond PR1
- Full-scale prototype testing program
- Qualification per API Spec 6AV1 or 6AV2
- Third-party verification

Requirements:
PR1 requirements plus:
- Full-scale prototype endurance testing
- Thermal cycling tests
- Pressure cycling tests
- Functional cycling (valve operations)
- Seal qualification testing
- Corrosion/environmental testing

Validation approach:
- Build prototype representative of production design
- Subject to comprehensive test program (API 6AV1)
- Document all test results
- Production units manufactured to validated design

Test program (API 6AV1):
- Temperature cycling: -20°F to max rated temp
- Pressure cycling: 0 to rated pressure (1000+ cycles)
- Functional testing: valve operations (100-500 cycles)
- Leak testing: after cycling (acceptance criteria)
- Destructive testing: verify safety factors

Documentation:
- Full validation report per API 6AV1
- Test facility accreditation
- Independent review/witness
- Qualified product listing

API SPEC 6AV1 vs 6AV2:
6AV1: Validation of equipment up to 15,000 PSI
6AV2: Validation of equipment >15,000 PSI and special applications

COMPARISON:
| Aspect | PR1 | PR2 |
|--------|-----|-----|
| Validation | Analysis + limited testing | Full prototype program |
| Testing | Basic functional | Comprehensive cycling |
| Documentation | Standard | Extensive validation report |
| Cost | Lower | Higher (prototype + testing) |
| Lead Time | Shorter | Longer (testing duration) |
| Confidence | Adequate | High |

SELECTION CRITERIA:
PR1 appropriate for:
- Standard applications (industry-proven designs)
- Non-critical wells (low consequence of failure)
- Budget-constrained projects
- Established equipment with track record

PR2 required/preferred for:
- New or novel designs (no field track record)
- Critical applications (offshore, high pressure, sour service)
- Regulatory requirements (some jurisdictions mandate PR2)
- Operator specifications (IOCs often require PR2)
- High consequence of failure (HPHT, subsea)

REGULATORY LANDSCAPE:
US (onshore): PR1 typically acceptable
US (offshore/BSEE): PR2 often required for critical equipment
North Sea (Norway, UK): PR2 standard for offshore
Middle East: Varies by operator (IOCs require PR2)
Asia-Pacific: Increasingly requiring PR2 for new projects

LIFECYCLE IMPLICATIONS:
Equipment with PR2 validation:
- Higher confidence in reliability
- Lower risk of early failure
- May reduce inspection frequency
- Better insurance/liability position

Equipment with PR1:
- Adequate for most applications
- Field experience provides validation over time
- May require more frequent inspection
- Potential for undiscovered failure modes

QUALIFICATION vs VALIDATION:
Qualification (per 6AV1):
- One-time program to validate design
- Results apply to all production units of that design
- Must re-qualify if design changes materially

Production validation:
- Testing of individual production units (PSL testing)
- Verifies manufacturing quality
- Separate from design qualification

COST IMPLICATIONS:
PR2 incremental cost:
- Prototype build: $50K - $500K (depends on complexity)
- Test program: $100K - $1M (facility, instrumentation, duration)
- Documentation: $25K - $100K
- Total: 5-20% of equipment cost

Amortization:
- Cost spread over multiple production units
- Large orders justify PR2 investment
- Single unit orders make PR2 prohibitively expensive
        """,
        key_factors=[
            "Equipment criticality and consequence of failure",
            "Regulatory requirements by jurisdiction",
            "Operator specifications",
            "Design maturity (new vs proven)",
            "Service conditions severity",
            "Project budget and schedule",
            "Order quantity (amortize qualification cost)",
            "Risk tolerance"
        ],
        primary_authority=[
            "API Spec 6A Section 9 (Performance requirements)",
            "API Spec 6AV1 (Validation of 6A equipment ≤15,000 PSI)",
            "API Spec 6AV2 (Validation of 6A equipment >15,000 PSI)"
        ],
        burden_holder="Purchaser specifies PR level; manufacturer executes",
        adversary_position="PR1 adequate; PR2 adds cost without commensurate benefit",
        counter_arguments=[
            "Novel design failure modes not revealed by PR1 analysis",
            "Thermal/pressure cycling accelerates degradation (caught by PR2 testing)",
            "Regulatory trend toward mandatory PR2 for critical equipment",
            "Cost of failure far exceeds PR2 incremental cost",
            "PR2 reduces long-term risk and liability exposure"
        ],
        resolution_strategy="PR2 for critical wells, new designs, offshore; PR1 for standard land applications with proven designs",
        entity_scope="All API 6A wellhead and tree equipment",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="PR levels clearly defined; risk assessment drives selection",
        controlling_precedent="API 6A Section 9 + 6AV1/6AV2",
        issue_category=IssueCategory.API_COMPLIANCE
    ),

    DoctrineBlock(
        topic="Wellhead Valve Types (Gate vs Ball)",
        keywords=["gate valve", "ball valve", "master valve", "wing valve", "valve selection"],
        conclusion_template=[
            "Gate valves provide bidirectional tight shutoff; traditional choice for master/wing valves.",
            "Ball valves offer quick operation and full-bore flow; increasingly used for surface applications.",
            "Selection depends on operating frequency, sealing requirements, and flow characteristics."
        ],
        reasoning_framework="""
Wellhead valve technologies:

GATE VALVES:
Design:
- Gate (wedge or slab) moves perpendicular to flow path
- Rising stem (stem moves up with gate) or non-rising stem
- Solid wedge, flexible wedge, or parallel slide gates

Operation:
- Multi-turn actuation (10-50 turns typical)
- Slow opening/closing (advantage: no surge)
- Positive seating force (threaded stem or actuator thrust)

Advantages:
- Bidirectional sealing (upstream or downstream pressure)
- Tight shutoff (metal-to-metal or soft seats)
- Low pressure drop in full open position
- Proven technology (100+ year history)
- Repairable seats (can relap in place)

Disadvantages:
- Slow operation (multi-turn)
- Not suitable for throttling (gate vibration, erosion)
- Stem seal leakage (rising stem design)
- Heavier and larger than equivalent ball valve

Seat types:
- Metal-to-metal: tungsten carbide, stellite (erosion-resistant)
- Soft seat: elastomeric (PTFE, nitrile, viton) - better seal, limited temp
- Combination: metal backup with elastomeric insert

Applications:
- Master valves on christmas trees
- Wing valves (production outlet)
- Block valves on flowlines
- Infrequent operation (open/close only)

BALL VALVES:
Design:
- Spherical ball with bore rotates 90° to open/close
- Trunnion-mounted (ball supported top/bottom) or floating ball
- Full-bore or reduced-bore

Operation:
- Quarter-turn actuation (90° rotation)
- Fast operation (manual or actuated)
- Low torque requirement (compared to gate)

Advantages:
- Fast operation (emergency shutdown advantage)
- Full-bore design: no pressure drop, pigging capability
- Compact and lightweight
- Excellent for frequent operation
- Bubble-tight shutoff (soft seats)

Disadvantages:
- Unidirectional sealing (typically downstream pressure only)
- Soft seat temperature limited (<400°F)
- Seat wear from solids (slurry service challenging)
- Not repairable in place (must remove valve for seat replacement)

Seat types:
- Soft seat (elastomeric): PTFE, reinforced PTFE, Viton
- Metal seat: stellite, tungsten carbide (high temp, erosive service)
- Fire-safe design: metal backup seat behind soft seat

Applications:
- Wing valves on trees (fast isolation)
- ESD (Emergency Shutdown) valves (fast closure)
- Flowline block valves
- High-cycle applications (frequent operation)

COMPARISON:
| Feature | Gate Valve | Ball Valve |
|---------|------------|------------|
| Operation speed | Slow (multi-turn) | Fast (quarter-turn) |
| Sealing | Bidirectional | Unidirectional (typically) |
| Pressure drop | Low (full open) | Very low (full-bore) |
| Throttling | Not recommended | Not recommended |
| Weight | Heavier | Lighter |
| Cost | Lower (generally) | Higher (especially trunnion) |
| Maintenance | In-place seat repair | Must remove for seat replacement |

MASTER VALVE SELECTION:
Gate valve advantages:
- Bidirectional seal (pressure from either direction)
- Proven reliability in well control
- Lower cost for large sizes (>4")

Ball valve advantages:
- Faster operation (well control response time)
- Full-bore flow (production optimization)
- Better for frequent operation

Industry trend:
- Gate valves still dominant for master valves
- Ball valves gaining acceptance for wing valves
- Subsea trees: increasingly using ball valves (ROV actuatable)

WING VALVE SELECTION:
Gate valve:
- Traditional choice
- Bidirectional seal (isolation from either side)
- Lower cost

Ball valve:
- Fast isolation (flowline rupture scenario)
- Full-bore for pigging operations
- Lighter weight (platform weight reduction)

ACTUATOR COMPATIBILITY:
Gate valve:
- Multi-turn actuator (motor, gearbox, or hydraulic cylinder with stem nut)
- Slower actuation but high thrust capability
- Rising stem requires space above valve

Ball valve:
- Quarter-turn actuator (rack-and-pinion, scotch yoke, or direct hydraulic)
- Fast actuation (ESD applications)
- Compact actuator envelope

MAINTENANCE:
Gate valve:
- Seats can be lapped (re-machined) in place
- Stem packing replacement without removing valve
- Backseat feature: allows packing replacement under pressure

Ball valve:
- Seat replacement requires valve removal from line
- Full valve disassembly for seat access
- Trunnion bearings may require periodic greasing

EROSION RESISTANCE:
Gate valve:
- Seats perpendicular to flow (less erosion when open)
- Soft seats erode faster than metal
- Trim upgrades available (tungsten carbide, ceramic)

Ball valve:
- Seats slide against ball during operation (wiper action removes deposits)
- Soft seats vulnerable to solids erosion
- Metal seats for severe service

FAILURE MODES:
Gate valve:
- Stem seal leakage (packing degradation)
- Seat leakage (wear, corrosion, damage)
- Stem thread wear (frequent operation)
- Bonnet seal leakage

Ball valve:
- Seat leakage (wear, extrusion, chemical attack)
- Seat blowout (pressure reversal)
- Trunnion bearing seizure
- Body seal leakage
        """,
        key_factors=[
            "Operating frequency (infrequent vs high-cycle)",
            "Sealing direction (uni vs bidirectional)",
            "Speed requirements (emergency shutdown)",
            "Flow characteristics (full-bore requirement)",
            "Temperature and pressure",
            "Erosive service (solids content)",
            "Maintenance access and philosophy",
            "Cost constraints"
        ],
        primary_authority=[
            "API Spec 6A (Valve requirements)",
            "API Spec 6D (Pipeline valves)",
            "MSS SP-61 (Pressure testing of steel valves)"
        ],
        burden_holder="Facilities/mechanical engineer",
        adversary_position="Gate valves adequate and proven; ball valves unnecessary premium",
        counter_arguments=[
            "Ball valve fast operation critical for emergency shutdown",
            "Full-bore ball valve eliminates pressure drop (production optimization)",
            "Gate valve stem seal leakage common failure (ball valve avoids issue)",
            "Frequent operation accelerates gate valve wear",
            "Lighter ball valve reduces platform weight (offshore)"
        ],
        resolution_strategy="Gate valves for master valves; ball valves for wings and high-cycle applications",
        entity_scope="All wellhead and flowline valves",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Valve technology mature; selection depends on application specifics",
        controlling_precedent="API 6A + field performance history",
        issue_category=IssueCategory.EQUIPMENT_SELECTION
    ),

    DoctrineBlock(
        topic="API Monogram Licensing and Verification",
        keywords=["API monogram", "API license", "verification", "counterfeit", "certification"],
        conclusion_template=[
            "API Monogram Program certifies manufacturers meet API 6A requirements through audits.",
            "Counterfeit equipment (unmarked or fake monogram) represents significant safety risk.",
            "Verification of API license and equipment traceability essential for quality assurance."
        ],
        reasoning_framework="""
API Monogram Program:

PURPOSE:
- Certify manufacturers meet API specification requirements
- Audit manufacturing processes, QA/QC systems
- Authorize use of API monogram mark on compliant equipment
- Provide assurance to purchasers of equipment quality

MONOGRAM MARK:
Format:
- API logo with specification number (e.g., "API 6A")
- License number (assigned to manufacturer)
- Pressure rating, material class, temperature class
- PSL level (if applicable)
- Stamped, etched, or cast into equipment body

Example marking:
  API 6A 10M AA PSL-3 PR2
  License 6A-1234
  (10,000 PSI, Material Class AA, PSL-3, PR2)

LICENSING PROCESS:
Application:
- Manufacturer applies to API
- Submit quality manual, procedures, drawings
- Demonstrate compliance with API 6A requirements

Audit:
- API-authorized auditor visits facility
- Review QA/QC systems, manufacturing processes
- Witness testing, inspect equipment
- Verify traceability and documentation

License:
- If compliant, API issues license
- Annual surveillance audits to maintain license
- License can be suspended/revoked for non-compliance

VERIFICATION BY PURCHASER:
Check API license database:
- API website: search licensed manufacturers
- Verify license number on equipment matches database
- Check license status (active, suspended, revoked)
- Verify scope (pressure rating, PSL, etc.) covered by license

Equipment traceability:
- Serial number on each piece
- Material Test Reports (MTRs) traceable to heat/lot
- Manufacturing records (test charts, NDE reports)
- Certificate of Compliance (CoC) from manufacturer

COUNTERFEIT EQUIPMENT PROBLEM:
Risks:
- No assurance of material quality (wrong alloy, inadequate strength)
- Manufacturing defects not detected (no NDE, no testing)
- Catastrophic failure (blowout, fire, fatalities)
- Liability for purchaser/operator

Indicators of counterfeit:
- Price too good to be true (significantly below market)
- Supplier not authorized distributor for OEM
- Missing or suspicious API monogram (wrong format, unclear)
- No serial number or traceability documentation
- MTRs not provided or appear falsified
- Equipment from non-licensed manufacturer claiming API compliance

SUPPLY CHAIN INTEGRITY:
Authorized distributors:
- Purchase only from OEM or authorized distributor
- Distributors listed on manufacturer website
- Authorized distributors provide full traceability

Gray market equipment:
- Equipment from unknown/unauthorized sources
- May be genuine but no traceability
- Risk of damage during storage/transportation
- No manufacturer warranty

REGULATORY REQUIREMENTS:
US (BSEE offshore):
- API monogram required for critical equipment
- Verification of license and traceability mandatory
- Counterfeit equipment grounds for violation

International:
- Many jurisdictions require API monogram
- Some have additional local certification requirements

DOCUMENTATION REQUIREMENTS:
For each piece of equipment:
- API monogram mark on body
- Serial number
- Certificate of Compliance (CoC)
- Material Test Reports (MTRs)
- Hydrostatic test chart
- NDE reports (if PSL-2/3/4)
- PMI reports (if PSL-2+)
- Traceability to API license

MAINTENANCE OF LICENSE:
Annual surveillance:
- API auditor returns annually
- Review continued compliance
- Check customer complaints, failure reports
- Witness testing, inspect QA/QC

License suspension/revocation:
- Non-compliance discovered during audit
- Customer complaints/equipment failures
- Manufacturer must cease using monogram
- Equipment produced during suspension not API certified

PURCHASER BEST PRACTICES:
1. Specify API monogram in purchase order
2. Verify manufacturer license before ordering
3. Inspect equipment upon receipt for monogram and serial number
4. Request and verify all traceability documentation
5. Report suspected counterfeit equipment to API and authorities
6. Maintain records of equipment traceability for lifecycle
        """,
        key_factors=[
            "Manufacturer API license status",
            "Equipment monogram marking verification",
            "Serial number and traceability documentation",
            "Supplier authorization (OEM or authorized distributor)",
            "Price reasonableness (too low indicates risk)",
            "MTR and test report authenticity",
            "Regulatory requirements for API certification",
            "Supply chain security"
        ],
        primary_authority=[
            "API Monogram Program requirements",
            "API Spec 6A (Equipment standards)",
            "API Quality Programs Guide"
        ],
        burden_holder="Purchaser/operator",
        adversary_position="Non-API equipment adequate; certification unnecessary expense",
        counter_arguments=[
            "Counterfeit equipment failures cause blowouts and fatalities",
            "Regulatory violations for using non-API equipment",
            "No recourse for defective equipment from unlicensed manufacturer",
            "Insurance/liability exposure using uncertified equipment",
            "API license provides independent verification of quality"
        ],
        resolution_strategy="Require API monogram; verify license; purchase only from authorized sources; maintain traceability",
        entity_scope="All API 6A wellhead and tree equipment procurement",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API program well-established; counterfeit detection requires vigilance",
        controlling_precedent="API Monogram Program + API 6A",
        issue_category=IssueCategory.API_COMPLIANCE
    )
]


# ═══════════════════════════════════════════════════════════════════════════════
# TELEMETRY & TRACKING
# ═══════════════════════════════════════════════════════════════════════════════

telemetry_store: List[TelemetryData] = []
coverage_map: Dict[str, int] = {block.topic: 0 for block in DOCTRINE_CACHE}


def track_telemetry(query_id: str, triggered_doctrines: List[str], latency_ms: float,
                    mode: ResponseMode, confidence: ConfidenceLevel, error: Optional[str] = None):
    """Store telemetry data for analysis"""
    telemetry = TelemetryData(
        query_id=query_id,
        timestamp=datetime.now(),
        doctrine_blocks_triggered=triggered_doctrines,
        latency_ms=latency_ms,
        response_mode=mode,
        confidence_level=confidence,
        error_domain=error
    )
    telemetry_store.append(telemetry)

    for topic in triggered_doctrines:
        if topic in coverage_map:
            coverage_map[topic] += 1


# ═══════════════════════════════════════════════════════════════════════════════
# CORE ENGINE LOGIC
# ═══════════════════════════════════════════════════════════════════════════════

def three_layer_response(query: str, mode: ResponseMode, zone: AnalysisZone) -> tuple[str, List[str], ConfidenceLevel, float]:
    """
    Three-layer response architecture:
    1. Doctrine cache (0-200ms)
    2. Semantic retrieval (fallback)
    3. Deep analysis (complex queries)
    """
    import time
    start = time.time()

    # Layer 1: Doctrine cache lookup
    triggered = []
    for block in DOCTRINE_CACHE:
        if any(kw.lower() in query.lower() for kw in block.keywords):
            triggered.append(block.topic)
            block.access_count += 1
            block.last_accessed = datetime.now()

    if not triggered:
        # Layer 2: Semantic retrieval (simplified - would use vector search in production)
        response = "No specific wellhead equipment doctrine matched. General API 6A compliance recommended."
        confidence = ConfidenceLevel.DISCLOSURE
    else:
        # Build response from triggered doctrines
        blocks = [b for b in DOCTRINE_CACHE if b.topic in triggered]

        if mode == ResponseMode.FAST:
            response = _build_fast_response(blocks, zone)
            confidence = ConfidenceLevel.DEFENSIBLE
        elif mode == ResponseMode.DEFENSE:
            response = _build_defense_response(blocks, zone)
            confidence = ConfidenceLevel.DEFENSIBLE
        else:  # MEMO
            response = _build_memo_response(blocks, zone)
            confidence = ConfidenceLevel.DEFENSIBLE

    latency = (time.time() - start) * 1000
    return response, triggered, confidence, latency


def _build_fast_response(blocks: List[DoctrineBlock], zone: AnalysisZone) -> str:
    """Concise response for quick guidance"""
    parts = []
    for block in blocks[:3]:  # Top 3 blocks
        conclusion = " ".join(block.conclusion_template)
        parts.append(f"**{block.topic}**: {conclusion}")

    return "\n\n".join(parts)


def _build_defense_response(blocks: List[DoctrineBlock], zone: AnalysisZone) -> str:
    """Audit-ready response with full reasoning"""
    parts = ["# Wellhead Equipment Analysis\n"]

    for block in blocks:
        parts.append(f"## {block.topic}\n")
        parts.append(f"**Conclusion**: {' '.join(block.conclusion_template)}\n")
        parts.append(f"**Reasoning Framework**:\n{block.reasoning_framework}\n")
        parts.append(f"**Key Factors**: {', '.join(block.key_factors)}\n")
        parts.append(f"**Authority**: {', '.join(block.primary_authority)}\n")
        parts.append(f"**Confidence**: {block.confidence.value}\n")

    return "\n".join(parts)


def _build_memo_response(blocks: List[DoctrineBlock], zone: AnalysisZone) -> str:
    """Full documentation with analysis"""
    parts = ["# Comprehensive Wellhead Equipment Analysis Memorandum\n"]
    parts.append(f"**Analysis Zone**: {zone.value}\n")
    parts.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d')}\n\n")

    for i, block in enumerate(blocks, 1):
        parts.append(f"## Section {i}: {block.topic}\n")
        parts.append(f"**Issue Category**: {block.issue_category.value}\n\n")

        parts.append(f"### Conclusion\n{' '.join(block.conclusion_template)}\n")

        parts.append(f"### Detailed Analysis\n{block.reasoning_framework}\n")

        parts.append(f"### Key Factors\n")
        for factor in block.key_factors:
            parts.append(f"- {factor}")
        parts.append("\n")

        parts.append(f"### Applicable Authority\n")
        for auth in block.primary_authority:
            parts.append(f"- {auth}")
        parts.append("\n")

        parts.append(f"### Risk Assessment\n")
        parts.append(f"**Burden Holder**: {block.burden_holder}\n")
        parts.append(f"**Adversary Position**: {block.adversary_position}\n")
        parts.append(f"**Counter-Arguments**:\n")
        for arg in block.counter_arguments:
            parts.append(f"- {arg}")
        parts.append(f"\n**Resolution Strategy**: {block.resolution_strategy}\n\n")

        parts.append(f"**Confidence Level**: {block.confidence.value}\n")
        parts.append(f"**Confidence Stratification**: {block.confidence_stratification}\n\n")
        parts.append("---\n\n")

    return "\n".join(parts)


def generate_determinism_hash(query: str, response: str) -> str:
    """SHA-256 hash for reproducibility verification"""
    content = f"{query}|{response}".encode('utf-8')
    return hashlib.sha256(content).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

APP = FastAPI(
    title="OFE08 Wellhead Equipment Analysis Engine",
    description="TIE Gold Standard engine for wellhead and christmas tree equipment analysis",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@APP.get("/")
async def root():
    return {
        "engine": "OFE08_wellhead_equipment",
        "version": "1.0.0",
        "status": "operational",
        "port": 9008,
        "doctrine_blocks": len(DOCTRINE_CACHE),
        "capabilities": [
            "API 6A pressure rating analysis",
            "Material class selection (AA-HH)",
            "PSL level requirements",
            "Casing/tubing head design",
            "Christmas tree configuration",
            "Seal technology selection",
            "Temperature class and derating",
            "Valve type selection",
            "Surface safety valve requirements",
            "OEM system comparison"
        ]
    }


@APP.get("/health")
async def health():
    """Comprehensive health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engine_id": "OFE08",
        "doctrine_blocks": len(DOCTRINE_CACHE),
        "telemetry_records": len(telemetry_store),
        "coverage_map_size": len(coverage_map),
        "most_accessed_doctrines": sorted(
            [(topic, count) for topic, count in coverage_map.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]
    }


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with three-layer response"""
    try:
        query_id = hashlib.md5(f"{request.query}{datetime.now().isoformat()}".encode()).hexdigest()[:12]

        logger.info(f"Query {query_id}: {request.query[:100]} | Mode: {request.mode} | Zone: {request.zone}")

        response_text, triggered, confidence, latency = three_layer_response(
            request.query,
            request.mode,
            request.zone
        )

        det_hash = generate_determinism_hash(request.query, response_text)

        track_telemetry(query_id, triggered, latency, request.mode, confidence)

        logger.info(f"Query {query_id} complete: {len(triggered)} doctrines, {latency:.1f}ms")

        return QueryResponse(
            query_id=query_id,
            response=response_text,
            confidence=confidence,
            triggered_doctrines=triggered,
            latency_ms=round(latency, 2),
            determinism_hash=det_hash,
            mode=request.mode,
            zone=request.zone,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/doctrines")
async def list_doctrines():
    """List all doctrine blocks"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": block.topic,
                "category": block.issue_category.value,
                "keywords": block.keywords,
                "confidence": block.confidence.value,
                "access_count": block.access_count
            }
            for block in DOCTRINE_CACHE
        ]
    }


@APP.get("/coverage")
async def coverage_report():
    """Coverage map showing doctrine usage"""
    return {
        "total_queries": len(telemetry_store),
        "coverage_map": coverage_map,
        "unutilized_doctrines": [topic for topic, count in coverage_map.items() if count == 0]
    }


@APP.get("/telemetry")
async def telemetry_report():
    """Telemetry analytics"""
    if not telemetry_store:
        return {"message": "No telemetry data"}

    avg_latency = sum(t.latency_ms for t in telemetry_store) / len(telemetry_store)

    return {
        "total_queries": len(telemetry_store),
        "average_latency_ms": round(avg_latency, 2),
        "mode_distribution": {
            mode.value: len([t for t in telemetry_store if t.response_mode == mode])
            for mode in ResponseMode
        },
        "confidence_distribution": {
            conf.value: len([t for t in telemetry_store if t.confidence_level == conf])
            for conf in ConfidenceLevel
        }
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting OFE08 Wellhead Equipment Analysis Engine on port 9008")
    uvicorn.run(APP, host="0.0.0.0", port=9008)
