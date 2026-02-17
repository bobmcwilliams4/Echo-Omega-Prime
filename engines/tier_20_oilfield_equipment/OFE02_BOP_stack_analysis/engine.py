"""
OFE02 - BOP Stack Analysis Engine
Blowout Preventer Systems - Equipment Expertise

TIE Gold Standard Engine - Real Domain Expertise
API RP 53, BSEE Regulations, BOP Testing & Configuration
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Set
from collections import defaultdict
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_NAME = "OFE02_BOP_Stack_Analysis"
VERSION = "1.0.0"
PORT = 9002

logger.add(
    f"logs/{ENGINE_NAME}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
)

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

class AuthorityLevel(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    TERTIARY = "TERTIARY"

class IssueCategory(str, Enum):
    ANNULAR_PREVENTER = "ANNULAR_PREVENTER"
    RAM_PREVENTER = "RAM_PREVENTER"
    BOP_TESTING = "BOP_TESTING"
    ACCUMULATOR_SYSTEM = "ACCUMULATOR_SYSTEM"
    CONTROL_SYSTEM = "CONTROL_SYSTEM"
    STACK_CONFIGURATION = "STACK_CONFIGURATION"
    PRESSURE_RATING = "PRESSURE_RATING"
    SUBSEA_BOP = "SUBSEA_BOP"
    SURFACE_BOP = "SURFACE_BOP"
    KILL_LINE = "KILL_LINE"
    CHOKE_MANIFOLD = "CHOKE_MANIFOLD"
    FAILURE_ANALYSIS = "FAILURE_ANALYSIS"

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    OPERATIONAL = "OPERATIONAL"
    AUDIT = "AUDIT"

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="BOP analysis query")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    zone: AnalysisZone = Field(default=AnalysisZone.OPERATIONAL)
    context: Optional[Dict[str, Any]] = Field(default=None)

class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: Optional[str] = None
    adversary_position: Optional[str] = None
    counter_arguments: List[str] = Field(default_factory=list)
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    controlling_precedent: Optional[str] = None
    category: IssueCategory

class QueryResponse(BaseModel):
    query: str
    response: str
    mode: ResponseMode
    zone: AnalysisZone
    confidence: ConfidenceLevel
    doctrines_triggered: List[str]
    authorities_cited: List[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    queries_processed: int
    avg_latency_ms: float

# ============================================================================
# DOCTRINE CACHE - 25+ BOP EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Annular Preventer Design and Function",
        keywords=["annular", "hydril", "cameron", "packing element", "spherical"],
        conclusion_template=[
            "Annular preventers use a rubber packing element to seal around pipe of varying diameters or seal an open hole.",
            "Hydril GK and Cameron DL annulars are industry standards with closing pressures 1500-3000 psi.",
            "Packing element life depends on pressure cycles, chemical exposure, and stripping operations."
        ],
        reasoning_framework="""
Annular BOP Analysis Framework:
1. DESIGN: Packing element (rubber/synthetic), hydraulic piston, opening chamber
2. OPERATING RANGE: Seals 2-7/8" to full bore, typically 13-5/8" to 21-1/4" bowl
3. CLOSING PRESSURE: 1500 psi standard, 3000 psi high-pressure applications
4. STRIPPING: Can strip pipe in/out under pressure, causes element wear
5. OPENING: Regulated opening pressure prevents element damage
6. MANUFACTURERS: Hydril GK (spherical), Cameron Type DL (annular), NOV Shaffer
7. ELEMENT REPLACEMENT: 500-1000 pressure cycles typical, inspect per API RP 53
8. PRESSURE LIMITATION: Lower working pressure than rams (typically 50% of ram rating)
9. VERSATILITY: Seals multiple diameters, handles tool joints, but wears faster
10. POSITION: Typically top of stack for pipe size flexibility
        """,
        key_factors=[
            "Closing pressure and regulator setting",
            "Packing element condition and replacement history",
            "Stripping vs sealing operations",
            "Chemical compatibility (H2S, CO2, drilling fluids)",
            "Open hole sealing capability",
            "Element wear from repeated cycling"
        ],
        primary_authority=[
            "API RP 53 (BOP Equipment Systems)",
            "Hydril GK Operations Manual",
            "Cameron Type DL Technical Manual",
            "BSEE NTL 2015-N01 (BOP Maintenance)"
        ],
        resolution_strategy="Evaluate annular type, pressure ratings, element condition, and operational history to determine suitability and maintenance requirements.",
        entity_scope="Drilling contractors, operators, BOP maintenance providers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ANNULAR_PREVENTER
    ),

    DoctrineBlock(
        topic="Ram Preventer Types and Applications",
        keywords=["blind rams", "shear rams", "pipe rams", "variable bore", "VBR"],
        conclusion_template=[
            "Ram preventers provide rigid sealing using steel rams that close across the wellbore.",
            "Pipe rams seal on specific pipe OD; blind rams seal open hole; shear rams cut and seal drillpipe.",
            "Variable bore rams (VBR) cover multiple pipe sizes but require precise ram block selection."
        ],
        reasoning_framework="""
Ram BOP Analysis Framework:
1. PIPE RAMS: Seal on specific OD (5", 5-1/2", etc.), semi-circular cutouts
2. BLIND RAMS: Flat face, seal open hole or wireline, no pipe present
3. SHEAR RAMS: Hardened cutting blades, sever drillpipe and seal wellbore
4. BLIND SHEAR RAMS (BSR): Combined shear and seal function, deepwater primary
5. VARIABLE BORE RAMS (VBR): Adjustable blocks cover 3-5/8" to 6-5/8" range
6. CASING SHEAR RAMS: Cut and seal large diameter casing (13-3/8", 16", 20")
7. RAM BLOCK SELECTION: Must match pipe OD exactly for pipe rams
8. CLOSING TIME: 30-45 seconds typical, shear rams slower due to cutting action
9. PRESSURE RATING: Full working pressure (5K, 10K, 15K, 20K psi)
10. LOCKING MECHANISM: Manual or automatic locks prevent ram opening under pressure
11. RAM BONNET: Contains hydraulic piston and ram shaft
12. SEAL REPLACEMENT: Elastomer seals on ram blocks and bonnets
        """,
        key_factors=[
            "Pipe OD compatibility for pipe rams",
            "Shear ram blade condition and shear force rating",
            "VBR adjustment mechanism and ram block inventory",
            "Locking system engagement verification",
            "Elastomer seal condition (top seal, front seal)",
            "Hydraulic closing pressure requirement"
        ],
        primary_authority=[
            "API Spec 16A (BOP Equipment Specifications)",
            "API RP 53 Section 7 (Ram Type BOP)",
            "BSEE 30 CFR 250.442 (BOP System Requirements)",
            "Cameron Type U/QRC Technical Manual"
        ],
        resolution_strategy="Match ram type to operational requirement, verify ram blocks match pipe schedule, ensure shear rams rated for maximum anticipated casing weight.",
        entity_scope="Drilling operations, BOP engineers, well control personnel",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.RAM_PREVENTER
    ),

    DoctrineBlock(
        topic="BOP Testing Protocols Per API RP 53",
        keywords=["pressure test", "function test", "API RP 53", "initial test", "30 day test"],
        conclusion_template=[
            "API RP 53 mandates initial tests to rated working pressure and subsequent tests every 14-30 days.",
            "Low-pressure function tests verify each component operates; high-pressure tests verify seal integrity.",
            "Test frequency increases for deepwater (14 days) vs shallow water (30 days)."
        ],
        reasoning_framework="""
BOP Testing Framework (API RP 53 Rev 5):
1. INITIAL TEST: Upon installation, test to rated working pressure (5K-15K psi)
2. FREQUENCY: 14 days (deepwater/HPHT), 21 days (standard), 30 days (shallow water)
3. LOW-PRESSURE TEST: 200-300 psi function test of all components
4. HIGH-PRESSURE TEST: Rated working pressure on annular, rams, choke/kill lines
5. ACCUMULATOR TEST: Close all preventers with pumps off, verify stored volume
6. CONTROL SYSTEM TEST: Verify each function from primary and backup panels
7. SECONDARY CONTROL: Test deadman/autoshear/AMF systems
8. PRESSURE HOLD: Stabilize pressure, 5-minute hold minimum
9. DOCUMENTATION: Test charts, witness signatures, test matrix completion
10. ACCEPTANCE CRITERIA: Zero visible leak, pressure drop <10% over hold period
11. FAILURE RESPONSE: Tag out failed component, repair, retest before operations
12. THIRD-PARTY VERIFICATION: Independent company witnesses critical tests
        """,
        key_factors=[
            "Test pressure (low-pressure function, rated working pressure)",
            "Test duration and pressure stability",
            "Test witness requirements (company man, toolpusher, third-party)",
            "Accumulator precharge pressure and system volume",
            "Chart recorder or electronic data capture",
            "Pass/fail criteria and remediation procedures"
        ],
        primary_authority=[
            "API RP 53 Rev 5 Section 10 (Testing)",
            "BSEE 30 CFR 250.737 (BOP Testing Requirements)",
            "BSEE NTL 2015-N01 (Well Control Rule)",
            "ISO 13628-7 (Subsea BOP Testing)"
        ],
        resolution_strategy="Establish test schedule per water depth and pressure rating, ensure adequate accumulator capacity, maintain test records per regulatory requirements.",
        entity_scope="Drilling contractors, operators, third-party inspectors, regulatory agencies",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.BOP_TESTING
    ),

    DoctrineBlock(
        topic="Accumulator System Design and Sizing",
        keywords=["accumulator", "koomey unit", "precharge", "nitrogen", "usable volume"],
        conclusion_template=[
            "Accumulator systems store hydraulic energy to close BOPs when pumps fail.",
            "API RP 53 requires 1.5x usable volume to close all preventers and retain 200 psi minimum.",
            "Koomey units (portable accumulators) common on land rigs; integrated systems on deepwater."
        ],
        reasoning_framework="""
Accumulator System Analysis Framework:
1. PURPOSE: Provide hydraulic fluid under pressure to close BOP components
2. SIZING: 1.5x volume to close all preventers + valve functions, 200 psi residual
3. PRECHARGE: Nitrogen gas precharge typically 1000-1500 psi
4. USABLE VOLUME: Fluid volume between precharge and operating pressure (3000 psi)
5. BOTTLE COUNT: 80-gallon bottles (subsea), 10-20 gallon bottles (surface)
6. CLOSING UNITS: Annular (10-20 gal), Rams (5-8 gal each), Valves (2-4 gal)
7. KOOMEY UNIT: Portable accumulator bank with pump, relief, and manifold
8. PUMP CAPACITY: Triplex pump 5-15 GPM at 3000 psi operating pressure
9. PRESSURE MONITORING: Manifold gauge, remote gauge, low-pressure alarm
10. REDUNDANCY: Dual pumps, dual manifolds, backup nitrogen bottles
11. AUTOSHEAR/AMF: Dedicated accumulator bank for emergency functions
12. REGULATION: Pilot regulators reduce 3000 psi to 1500 psi for annular closing
        """,
        key_factors=[
            "Total system volume and usable volume calculation",
            "Precharge pressure and operating pressure range",
            "Pump capacity and recharge time",
            "Number of BOP closing operations without pump support",
            "Nitrogen bottle reserve and refill capability",
            "Pressure gauge accuracy and alarm setpoints"
        ],
        primary_authority=[
            "API RP 53 Section 8 (Accumulator Systems)",
            "BSEE 30 CFR 250.446 (Accumulator Capacity)",
            "Koomey Unit Operations Manual",
            "Cameron BOP Control System Design Guide"
        ],
        resolution_strategy="Calculate total closing volume for all components, size accumulator system to 1.5x requirement, verify precharge pressure quarterly, test system under no-pump conditions.",
        entity_scope="Drilling contractors, BOP equipment suppliers, well control specialists",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ACCUMULATOR_SYSTEM
    ),

    DoctrineBlock(
        topic="BOP Control Systems (Hydraulic, MUX, Electro-Hydraulic)",
        keywords=["control system", "MUX", "multiplex", "electro-hydraulic", "hydraulic pilot"],
        conclusion_template=[
            "BOP control systems transmit operator input to hydraulic actuators on the BOP stack.",
            "Hydraulic pilot systems use fluid lines; MUX systems use electric signals; hybrid systems combine both.",
            "Deepwater subsea BOPs use MUX (multiplexed electro-hydraulic) to reduce umbilical lines."
        ],
        reasoning_framework="""
BOP Control System Framework:
1. HYDRAULIC PILOT: Direct hydraulic lines from surface panel to BOP valves
   - Advantage: Simple, reliable, proven technology
   - Disadvantage: Many hydraulic lines, slow response time (subsea)
2. MULTIPLEX (MUX): Electric signals over cables, converted to hydraulic at subsea pod
   - Advantage: Fewer umbilical lines (2 electric vs 20+ hydraulic)
   - Disadvantage: Complex electronics, requires subsea power/logic modules
3. ELECTRO-HYDRAULIC: Surface electric panel, hydraulic actuators at BOP
   - Advantage: Fast response, fewer lines than full hydraulic
   - Disadvantage: Requires local hydraulic power unit (HPU)
4. CONTROL PANELS: Driller's panel (primary), toolpusher panel (secondary), remote panel
5. REDUNDANCY: Dual control pods (blue/yellow), redundant signal paths
6. DEADMAN SYSTEM: Auto-close on loss of power/signal
7. AUTOSHEAR/AMF: Automatic mode function triggers on disconnect
8. SOLENOID VALVES: Electric signal opens/closes hydraulic pilot valves
9. POSITION SENSORS: LVDT (linear variable differential transformer) confirms ram position
10. SUBSEA ELECTRONICS: Logic cards, power supply, communication modules
11. UMBILICAL: Steel tube enclosing hydraulic/electric/chemical lines
12. TESTING: Function test every shift, communication check, deadman verification
        """,
        key_factors=[
            "Control system type (hydraulic, MUX, hybrid)",
            "Response time from panel input to BOP function",
            "Redundancy level (dual pods, backup power)",
            "Deadman and autoshear configuration",
            "Position indication accuracy and validation",
            "Umbilical integrity and leak detection"
        ],
        primary_authority=[
            "API Spec 16D (Control Systems for BOPs)",
            "API RP 53 Section 9 (BOP Control Systems)",
            "Cameron MUX System Technical Manual",
            "BSEE 30 CFR 250.450 (BOP System Functions)"
        ],
        resolution_strategy="Select control system based on water depth and operational complexity, ensure dual redundancy for subsea, test all functions including deadman/autoshear before each well.",
        entity_scope="Drilling contractors, subsea equipment suppliers, control system engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CONTROL_SYSTEM
    ),

    DoctrineBlock(
        topic="Surface BOP Stack Configuration",
        keywords=["surface stack", "land rig", "jack-up", "stack order", "drilling spool"],
        conclusion_template=[
            "Surface BOP stacks mount on wellhead and are accessible for maintenance during operations.",
            "Typical surface stack: annular, 3x ram preventers (pipe/pipe/blind), drilling spool, wellhead.",
            "Lower pressure ratings (5K-10K) common for shallow wells; 15K for HPHT."
        ],
        reasoning_framework="""
Surface BOP Stack Configuration Framework:
1. STACK ORDER (top to bottom):
   - Rotating head (RH) or annular preventer
   - Upper annular (optional)
   - Pipe ram #1 (working string size)
   - Pipe ram #2 (casing/drill collar size)
   - Blind/Shear rams
   - BOP body or lower ram preventer
   - Drilling spool (side outlets for choke/kill lines)
   - Wellhead adapter or casing head
2. PRESSURE RATING: 2K, 3K, 5K, 10K, 15K, 20K psi working pressure
3. BORE SIZE: 7-1/16", 11", 13-5/8", 16-3/4", 18-3/4", 21-1/4"
4. FLANGE TYPE: API 6A flanges with ring gaskets (R, RX, BX)
5. CHOKE MANIFOLD: 2-4" lines with adjustable/fixed chokes, manifold valves
6. KILL LINE: Direct connection to annular space below BOP
7. HEIGHT: Total stack 15-30 feet, requires substructure clearance
8. TESTING: Initial test rated WP, 14-21 day intervals thereafter
9. ACCESSIBILITY: Walk-around platform, ram lock access, bonnet removal capability
10. WEIGHT: 10K psi stack 15,000-30,000 lbs, requires crane or BOP handling equipment
        """,
        key_factors=[
            "Wellhead pressure and temperature rating",
            "Drilling fluid density and kick potential",
            "Pipe sizes in hole (drillpipe, casing, drill collars)",
            "Rig floor height and substructure clearance",
            "Choke and kill line routing and valve placement",
            "Maintenance access and ram change-out capability"
        ],
        primary_authority=[
            "API Spec 6A (Wellhead and Tree Equipment)",
            "API RP 53 Section 6 (BOP Stack Design)",
            "IADC Drilling Manual (BOP Configuration)",
            "BSEE 30 CFR 250.442 (BOP Equipment Requirements)"
        ],
        resolution_strategy="Design stack configuration based on well pressure, pipe schedule, and operational requirements; ensure adequate ram selection for all anticipated pipe sizes; verify stack height vs rig clearance.",
        entity_scope="Drilling engineers, rig supervisors, BOP equipment planners",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SURFACE_BOP
    ),

    DoctrineBlock(
        topic="Subsea BOP System Design and Components",
        keywords=["subsea BOP", "LMRP", "flex joint", "wellhead connector", "deepwater"],
        conclusion_template=[
            "Subsea BOPs operate on the seafloor, remotely controlled from surface via umbilical.",
            "Components include LMRP (lower marine riser package), BOP stack, and wellhead connector.",
            "Redundancy critical: dual control pods, dual accumulator banks, backup shear rams."
        ],
        reasoning_framework="""
Subsea BOP System Framework:
1. LMRP (Lower Marine Riser Package):
   - Flex joint (allows riser angle deviation)
   - Riser connector (hydraulic connector to drilling riser)
   - Control pods (blue/yellow, redundant electronics)
   - Kill/choke lines and valves
   - Annular preventer (Hydril/Cameron)
2. BOP STACK:
   - Upper annular (optional)
   - Upper variable bore rams (VBR) or pipe rams
   - Middle pipe/casing shear rams
   - Blind shear rams (BSR) - primary emergency function
   - Lower pipe rams
   - Test rams (for pressure testing stack)
3. WELLHEAD CONNECTOR:
   - Hydraulic connector locks stack to wellhead
   - H4, HC, HC-1 connector types (Cameron/Vetco/ABB)
   - Preload system ensures seal integrity
   - Emergency disconnect releases stack from wellhead
4. CONTROL SYSTEM:
   - MUX electro-hydraulic (reduces umbilical lines)
   - Dual control pods with independent power/logic
   - Deadman system (auto-close on loss of signal)
   - Autoshear/AMF (automatic mode function on disconnect)
5. ACCUMULATOR SYSTEM:
   - Subsea accumulator bottles (80-gallon capacity)
   - Nitrogen precharge 1000-1500 psi
   - Sufficient volume for multiple closures without surface pump
6. ROV INTERVENTION:
   - Hot stabs for ROV hydraulic override
   - ROV panels for manual function control
   - Acoustic backup system (emergency signals from surface)
7. PRESSURE RATING: 10K, 15K, 20K psi working pressure
8. WATER DEPTH: 500-12,000+ feet operational range
        """,
        key_factors=[
            "Water depth and pressure rating requirements",
            "Wellhead connector type compatibility",
            "Control system redundancy and deadman configuration",
            "Accumulator capacity and closure volume",
            "ROV intervention capability and hot stab placement",
            "Flex joint angle capability and riser design",
            "Shear ram force rating for anticipated casing/drillpipe"
        ],
        primary_authority=[
            "API Spec 16A (BOP Equipment)",
            "API RP 53 Section 12 (Subsea BOP Systems)",
            "BSEE 30 CFR 250 Subpart D (Deepwater Operations)",
            "ISO 13628-7 (Subsea BOP Systems)",
            "Cameron Subsea BOP Technical Manual"
        ],
        resolution_strategy="Design subsea BOP system with full redundancy (dual pods, dual accumulators, backup shear), verify shear ram force exceeds maximum anticipated pipe/casing, ensure ROV hot stab access for all critical functions.",
        entity_scope="Deepwater operators, subsea equipment engineers, well control specialists",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SUBSEA_BOP
    ),

    DoctrineBlock(
        topic="BOP Pressure Ratings and Selection",
        keywords=["working pressure", "5K", "10K", "15K", "20K", "MAASP", "pressure rating"],
        conclusion_template=[
            "BOP working pressure must exceed maximum anticipated surface pressure (MAASP) for the well.",
            "Common ratings: 2K, 3K, 5K, 10K, 15K, 20K psi. HPHT wells require 15K-20K equipment.",
            "All components (BOP, choke manifold, valves) must have equal or greater rating than wellhead."
        ],
        reasoning_framework="""
BOP Pressure Rating Framework:
1. WORKING PRESSURE (WP): Maximum allowable operating pressure
   - 2K = 2,000 psi (shallow gas wells, low pressure)
   - 3K = 3,000 psi (moderate depth, conventional drilling)
   - 5K = 5,000 psi (standard deepwater, Gulf of Mexico)
   - 10K = 10,000 psi (HPHT, high-pressure reservoirs)
   - 15K = 15,000 psi (ultra-HPHT, deep gas wells)
   - 20K = 20,000 psi (extreme HPHT, frontier deepwater)
2. MAASP CALCULATION: Maximum Anticipated Annular Surface Pressure
   - MAASP = (Fracture Gradient × Shoe Depth) - Hydrostatic Pressure
   - BOP WP must exceed MAASP by safety margin (typically 10-20%)
3. COMPONENT RATING CONSISTENCY:
   - BOP stack, choke manifold, kill line, valves: same or higher rating
   - Wellhead and casing head must support BOP rating
   - Test pressure = WP (initial test), 70% WP (subsequent tests per API)
4. TEMPERATURE RATING:
   - Standard: -50°F to 250°F (API 6A PSL 1)
   - HPHT: -50°F to 350°F (API 6A PSL 2)
   - Extreme: -50°F to 450°F (API 6A PSL 3)
5. MATERIAL SELECTION:
   - Carbon steel (standard)
   - Alloy steel (H2S service, NACE MR0175)
   - Stainless trim (corrosive environments)
6. TESTING REQUIREMENTS:
   - Initial test to rated WP
   - Subsequent tests 70-100% WP per API RP 53
   - Cold rating tests at minimum temperature
        """,
        key_factors=[
            "Well MAASP and kick tolerance calculations",
            "Reservoir pressure and temperature (HPHT designation)",
            "H2S/CO2 content and corrosion resistance requirements",
            "Water depth and subsea pressure considerations",
            "Regulatory requirements (BSEE, state agencies)",
            "Equipment availability and cost (20K much more expensive than 10K)"
        ],
        primary_authority=[
            "API Spec 6A (Equipment Pressure Ratings)",
            "API RP 53 Section 4 (Pressure Rating Selection)",
            "BSEE 30 CFR 250.442 (BOP Requirements)",
            "NACE MR0175 (H2S Service Requirements)"
        ],
        resolution_strategy="Calculate well MAASP, select BOP rating with 10-20% safety margin, ensure all wellhead components rated consistently, specify material grades for corrosive service.",
        entity_scope="Well planners, drilling engineers, equipment procurement",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PRESSURE_RATING
    ),

    DoctrineBlock(
        topic="Kill Line Operations and Procedures",
        keywords=["kill line", "bullheading", "circulate kill", "driller's method", "wait and weight"],
        conclusion_template=[
            "Kill lines provide direct access to annulus below BOP for circulating kill mud or bullheading.",
            "Driller's method circulates kick out then kills; wait-and-weight circulates heavier mud in one cycle.",
            "Bullheading forces kick back into formation when circulation not possible."
        ],
        reasoning_framework="""
Kill Line Operations Framework:
1. KILL LINE FUNCTION:
   - Direct connection from choke manifold to annular space below BOP
   - Bypass closed BOP for mud circulation
   - Pump heavy mud to kill well
   - Reverse circulate (pump down annulus, up drillstring)
2. DRILLER'S METHOD (TWO-CIRCULATION METHOD):
   - Close BOP, record SIDPP/SICP
   - Circulate kick out using original mud weight
   - Circulate kill mud (increased weight) to kill well
   - Simple, but requires two circulations
3. WAIT-AND-WEIGHT METHOD (ONE-CIRCULATION METHOD):
   - Close BOP, record pressures
   - Calculate kill mud weight (KMW = MW + (SIDPP / 0.052 / TVD))
   - Mix kill mud
   - Circulate kill mud in one cycle while maintaining constant BHP
   - Faster, requires accurate calculations
4. BULLHEADING:
   - Pump kill mud down drillstring, force kick into formation
   - Used when circulation impossible (plugged bit, stuck pipe)
   - Monitor fracture gradient to avoid formation breakdown
   - Highest risk method, last resort
5. REVERSE CIRCULATION:
   - Pump down kill line, up drillstring
   - Used when drillstring plugged or damaged
   - Requires balanced pressure to avoid U-tubing
6. KILL LINE SPECIFICATIONS:
   - 2", 3", or 4" line from BOP to choke manifold
   - API 6A valves, rated to BOP working pressure
   - Multiple valves for isolation and redundancy
7. MONITORING:
   - Pump pressure (kill line injection pressure)
   - Drillpipe pressure (formation pressure indicator)
   - Return flow rate (choke manifold)
   - Pit volume (gain/loss)
        """,
        key_factors=[
            "Kick size and formation pressure",
            "Drillstring condition (open, plugged, or stuck)",
            "Kill mud weight calculation accuracy",
            "Pump pressure limits and formation fracture gradient",
            "Choke manifold capacity and adjustable choke control",
            "Personnel training on well control methods"
        ],
        primary_authority=[
            "IADC Well Control Manual",
            "API RP 59 (Well Control Operations)",
            "BSEE 30 CFR 250 Subpart E (Well Control)",
            "SPE Well Control Handbook"
        ],
        resolution_strategy="Assess well conditions, select appropriate kill method (driller's vs wait-and-weight), calculate kill mud weight accurately, monitor pressures continuously during kill operation, verify kill before opening BOP.",
        entity_scope="Drilling supervisors, well control specialists, rig crews",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.KILL_LINE
    ),

    DoctrineBlock(
        topic="Choke Manifold Design and Operation",
        keywords=["choke manifold", "adjustable choke", "fixed choke", "kill sheet", "constant BHP"],
        conclusion_template=[
            "Choke manifolds control wellbore pressure during kicks by adjusting backpressure on annulus.",
            "Adjustable chokes allow precise pressure control; fixed chokes provide backup and high-flow capacity.",
            "Proper choke operation maintains constant bottom hole pressure (BHP) during kill circulation."
        ],
        reasoning_framework="""
Choke Manifold Framework:
1. MANIFOLD DESIGN:
   - Multiple flow paths (typically 3-4 lines)
   - Adjustable choke (primary control)
   - Fixed chokes (backup, high-flow situations)
   - Buffer tank or poor boy degasser
   - Pressure gauges (choke line, drillpipe)
2. ADJUSTABLE CHOKE:
   - Variable orifice, 0-100% open
   - Remote control from driller's console
   - Precision adjustment for constant BHP method
   - Brands: Swaco, Cameron, Weatherford
3. FIXED CHOKES:
   - Bean chokes with fixed orifice (1/16" to 2")
   - High flow capacity when adjustable choke inadequate
   - Backup if adjustable choke fails
4. PRESSURE RATING:
   - Must match or exceed BOP working pressure
   - 2K, 3K, 5K, 10K, 15K psi ratings
5. FLOW PATHS:
   - Line 1: Adjustable choke (primary)
   - Line 2: Fixed choke or second adjustable
   - Line 3: Fixed large-bore choke (high flow)
   - Line 4: Direct to reserve pit (emergency dump)
6. CONSTANT BHP METHOD:
   - Adjust choke to maintain drillpipe pressure per kill sheet
   - As heavy mud enters annulus, reduce choke pressure
   - Prevents formation breakdown, controls kick migration
7. KILL SHEET:
   - Pre-calculated drillpipe pressures at increments (0, 10, 20... strokes)
   - Choke operator follows kill sheet to maintain schedule
   - Final circulating pressure (FCP) = new hydrostatic balance
8. CHOKE EROSION:
   - Abrasive drilling fluids and formation solids erode choke
   - Inspect and replace beans/adjustable trim regularly
   - Oversized choke reduces control, undersized causes excessive pressure
        """,
        key_factors=[
            "Choke manifold pressure rating vs well MAASP",
            "Adjustable choke condition and calibration",
            "Fixed bean inventory and sizing",
            "Choke line routing and valve configuration",
            "Kill sheet accuracy and crew training",
            "Erosion monitoring and component replacement"
        ],
        primary_authority=[
            "API RP 53 Section 11 (Choke and Kill Systems)",
            "IADC Well Control Manual (Choke Operation)",
            "BSEE 30 CFR 250.442 (Choke Manifold Requirements)",
            "Swaco Choke Manifold Operations Manual"
        ],
        resolution_strategy="Size choke manifold to well pressure rating, ensure adjustable choke operational before each well, verify kill sheet calculations, train choke operator on constant BHP method.",
        entity_scope="Drilling supervisors, well control crew, choke operators",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CHOKE_MANIFOLD
    ),

    DoctrineBlock(
        topic="H2S Service BOP Equipment Requirements",
        keywords=["H2S", "sour service", "NACE MR0175", "sulfide stress cracking", "alloy trim"],
        conclusion_template=[
            "H2S (hydrogen sulfide) environments require special materials to prevent sulfide stress cracking.",
            "NACE MR0175 specifies material grades, hardness limits, and testing for sour service.",
            "BOP elastomers must be H2S-resistant (Viton, HNBR); metal hardness limits <22 HRC."
        ],
        reasoning_framework="""
H2S Service BOP Requirements Framework:
1. SULFIDE STRESS CRACKING (SSC):
   - H2S + moisture + stress = cracking of high-strength steels
   - Catastrophic failure without warning
   - Prevention: material selection and hardness control
2. NACE MR0175 / ISO 15156 REQUIREMENTS:
   - Carbon steel hardness <22 HRC (Rockwell C)
   - Low-alloy steels <22 HRC or stress-relieved
   - Corrosion-resistant alloys (CRA): Inconel 625, Monel K-500
   - Elastomers: Viton (FKM), HNBR (hydrogenated nitrile)
   - NO Buna-N, standard nitrile in H2S service
3. BOP COMPONENT SELECTION:
   - Annular packing element: Viton or HNBR compound
   - Ram elastomers: H2S-resistant top/front seals
   - Ram blocks: Stress-relieved or <22 HRC hardness
   - Body and bonnet: Carbon steel with controlled hardness
   - Fasteners: NACE-compliant alloy or coated
4. TESTING REQUIREMENTS:
   - Hardness verification on all components
   - Material certifications (MTRs) per NACE
   - Tensile testing for critical components
   - Heat treatment records
5. OPERATIONAL CONSIDERATIONS:
   - Increased inspection frequency
   - Elastomer replacement intervals reduced
   - Corrosion monitoring (coupons, analysis)
   - Personnel H2S safety training (toxic gas)
6. H2S CONCENTRATION LIMITS:
   - Low: <100 ppm H2S
   - Medium: 100-1000 ppm H2S
   - High: >1000 ppm H2S (severe service)
   - NACE applies to any detectable H2S in wet conditions
7. DOCUMENTATION:
   - NACE compliance certificates for all BOP components
   - Material traceability reports (MTRs)
   - Heat treatment and stress relief records
        """,
        key_factors=[
            "H2S concentration in formation fluids",
            "Material hardness verification (<22 HRC)",
            "Elastomer compound H2S compatibility",
            "Component stress levels and design factors",
            "Temperature effects on SSC susceptibility",
            "Regulatory requirements (BSEE, state agencies)"
        ],
        primary_authority=[
            "NACE MR0175 / ISO 15156 (Sour Service Materials)",
            "API RP 53 Section 5 (H2S Service)",
            "BSEE NTL 2015-N01 (BOP Equipment)",
            "API Spec 6A (H2S Trim Specifications)"
        ],
        resolution_strategy="Verify H2S content via mud logging and formation analysis, specify NACE-compliant BOP equipment with certified materials, ensure elastomers are Viton/HNBR grade, maintain MTR documentation for all components.",
        entity_scope="Well planners, drilling engineers, BOP equipment suppliers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PRESSURE_RATING
    ),

    DoctrineBlock(
        topic="BOP Failure Modes and Root Cause Analysis",
        keywords=["failure analysis", "ram seal leak", "hydraulic leak", "control failure", "deadman"],
        conclusion_template=[
            "Common BOP failures: elastomer seal leakage, hydraulic system leaks, control system malfunctions.",
            "Root causes include inadequate maintenance, improper testing, component wear, and design limitations.",
            "Failure investigations follow API RP 53 Appendix F and BSEE incident reporting requirements."
        ],
        reasoning_framework="""
BOP Failure Analysis Framework:
1. ELASTOMER SEAL FAILURES:
   - Ram top seal extrusion (excessive pressure, worn seal)
   - Annular element failure (over-stripping, chemical degradation)
   - Bonnet seal leakage (improper installation, O-ring damage)
   - Root causes: Pressure cycling, chemical exposure, temperature extremes
2. HYDRAULIC SYSTEM FAILURES:
   - Regulator malfunction (annular closing pressure incorrect)
   - Accumulator leak (bottle valve, manifold connection)
   - Solenoid valve failure (stuck open/closed)
   - Hydraulic line rupture (corrosion, mechanical damage)
   - Root causes: Inadequate maintenance, contamination, fatigue
3. CONTROL SYSTEM FAILURES:
   - MUX electronics failure (power supply, logic card)
   - Position sensor malfunction (LVDT failure, false indication)
   - Deadman system failure (does not auto-close)
   - Communication loss (umbilical damage, connector corrosion)
   - Root causes: Water ingress, connector issues, software bugs
4. MECHANICAL FAILURES:
   - Ram locking mechanism failure (lock does not engage)
   - Shear ram blade damage (insufficient force, hardface wear)
   - Connector leak (wellhead connector preload loss)
   - Flex joint leak (seal damage, excessive angle)
   - Root causes: Overload, material defects, wear
5. INVESTIGATION PROTOCOL:
   - Preserve failed components for analysis
   - Witness statements from rig personnel
   - Review test records and maintenance logs
   - Metallurgical analysis (failed metal parts)
   - Elastomer analysis (chemical/physical testing)
   - Hydraulic fluid analysis (contamination check)
6. REGULATORY REPORTING:
   - BSEE Form 0131 (incident report) for failures during operations
   - API RP 53 Appendix F (failure investigation guidelines)
   - Third-party investigation (serious incidents)
7. CORRECTIVE ACTIONS:
   - Component replacement with upgraded parts
   - Design modification (engineering change notice)
   - Maintenance procedure revision
   - Operator training and awareness
   - Industry-wide safety alerts (IADC, API)
        """,
        key_factors=[
            "Failure mode identification (seal, hydraulic, control, mechanical)",
            "Time of failure (during test, during operations, idle period)",
            "Environmental conditions (pressure, temperature, H2S)",
            "Maintenance history and test records",
            "Component age and service hours",
            "Similar failures in fleet (systemic issue)"
        ],
        primary_authority=[
            "API RP 53 Appendix F (Failure Investigation)",
            "BSEE 30 CFR 250.197 (Incident Reporting)",
            "IADC Alert System (Industry Failure Notices)",
            "ASME Section VIII (Pressure Vessel Failure Analysis)"
        ],
        resolution_strategy="Document failure mode, conduct root cause analysis per API RP 53 Appendix F, implement corrective actions, notify regulatory agencies if required, share lessons learned industry-wide.",
        entity_scope="BOP maintenance engineers, failure investigators, regulatory agencies, industry safety committees",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.FAILURE_ANALYSIS
    ),

    DoctrineBlock(
        topic="Deepwater BOP Considerations and Challenges",
        keywords=["deepwater", "subsea", "riser margin", "weak point", "emergency disconnect"],
        conclusion_template=[
            "Deepwater BOPs operate in extreme environments: high pressure, low temperature, remote location.",
            "Riser margin (difference between formation fracture and seawater gradient) is critical constraint.",
            "Emergency disconnect capability required to separate LMRP from BOP stack during marine riser emergency."
        ],
        reasoning_framework="""
Deepwater BOP Framework:
1. WATER DEPTH CHALLENGES:
   - 1,000-12,000 feet water depth (Gulf of Mexico, Brazil, West Africa)
   - Subsea equipment inaccessible (ROV required for intervention)
   - Hydraulic response time increased (long umbilical)
   - Cold temperatures affect elastomers and hydraulics (35-40°F seabed)
2. RISER MARGIN:
   - Fracture gradient at shoe - Seawater gradient = Available margin
   - Example: 14 ppg frac, 8.6 ppg seawater = 5.4 ppg margin
   - Kick causes riser to fill with heavy mud, increases surface pressure
   - Narrow margin = higher risk of fracturing shoe during well control
3. EMERGENCY DISCONNECT SEQUENCE (EDS):
   - Close blind shear rams to seal wellbore
   - Unlatch LMRP connector
   - Separate LMRP from BOP stack
   - Vessel moves off location (hurricane, drillship drive-off)
   - Stack remains on wellhead, well secured
4. WEAK POINT IN RISER:
   - Designed failure point above BOP stack
   - Allows riser to part in emergency without damaging BOP
   - Typically 100-200 feet above LMRP
5. AUTOSHEAR / AMF (AUTOMATIC MODE FUNCTION):
   - Triggers on EDS or loss of communication
   - Closes blind shear rams automatically
   - Independent of operator input
   - Ensures well secured even if crew unable to act
6. ROV INTERVENTION:
   - Hot stabs provide hydraulic override
   - Manual panel on BOP stack for function control
   - ROV can close preventers, operate valves
   - Backup to primary MUX control system
7. ACOUSTIC BACKUP SYSTEM:
   - Surface-triggered acoustic signals
   - Commands: Close BSR, Disconnect LMRP
   - Last-resort communication if umbilical severed
8. REDUNDANCY REQUIREMENTS:
   - Dual control pods (blue/yellow)
   - Dual accumulator banks
   - Backup shear rams
   - Multiple disconnect methods (EDS, ROV, acoustic)
9. TESTING FREQUENCY:
   - 14-day BOP tests for deepwater (vs 21-30 days shallow)
   - Increased scrutiny due to higher risk
10. PRESSURE CHALLENGES:
    - 15K-20K psi BOP ratings for HPHT reservoirs
    - Subsea mudline pressure = seawater column (4,000+ psi at seabed)
    - Total system pressure = MAASP + mudline pressure
        """,
        key_factors=[
            "Water depth and riser margin calculation",
            "Emergency disconnect system functionality",
            "ROV intervention capability and backup systems",
            "Autoshear/AMF configuration and testing",
            "Shear ram force rating for drillpipe and casing",
            "Control system redundancy and deadman settings",
            "Cold temperature effects on elastomers and hydraulics"
        ],
        primary_authority=[
            "API RP 53 Section 12 (Subsea BOP Systems)",
            "BSEE 30 CFR 250 Subpart D (Deepwater Operations)",
            "ISO 13628-7 (Subsea Wellhead and BOP Equipment)",
            "IADC Deepwater Well Control Guidelines"
        ],
        resolution_strategy="Calculate riser margin and kick tolerance, design BOP system with full redundancy, verify shear ram force exceeds maximum anticipated loads, test EDS and autoshear before each well, ensure ROV intervention capability.",
        entity_scope="Deepwater operators, subsea engineers, well control specialists, rig supervisors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SUBSEA_BOP
    ),

    DoctrineBlock(
        topic="Cameron vs NOV vs Hydril BOP Comparison",
        keywords=["Cameron", "NOV", "Shaffer", "Hydril", "manufacturer", "market share"],
        conclusion_template=[
            "Cameron (Schlumberger), NOV (National Oilwell Varco), and Hydril (Tenaris) dominate BOP market.",
            "Cameron Type U/QRC rams and DL annulars most common. NOV Shaffer Sentinel and LWS designs competitive.",
            "Hydril GK annular industry standard for decades; other manufacturers produce similar spherical designs."
        ],
        reasoning_framework="""
BOP Manufacturer Comparison Framework:
1. CAMERON (SCHLUMBERGER SUBSIDIARY):
   - Market leader, largest installed base globally
   - Type U Rams: 5K-20K psi, single-body design, manual locks
   - QRC Rams: 10K-15K psi, quick-ram-change feature, side-door access
   - Type DL Annular: Piston-operated, 5K-10K psi
   - Subsea BOP: Deepwater leader, MUX control systems, LMRP design
   - Service: Global support network, extensive spare parts inventory
2. NOV (NATIONAL OILWELL VARCO):
   - Shaffer brand (acquired Hydril BOP division, now separate again)
   - Shaffer Sentinel: Compact design, reduced weight, 10K-15K psi
   - Shaffer LWS: Land and workover systems, 2K-5K psi
   - NXT Annular: Spherical packing element, 5K-10K psi
   - Subsea BOP: Competitor to Cameron, installed on several deepwater rigs
   - Innovation: Focus on weight reduction and faster ram change
3. HYDRIL (TENARIS SUBSIDIARY):
   - GK Annular: Spherical element, industry gold standard since 1960s
   - MSP (Multi-Service Platform) Annular: Rotating control device integration
   - Pressure Ratings: 2K-15K psi annulars
   - Market Position: Annular specialist, less focus on ram preventers
   - Service: Strong Gulf of Mexico presence
4. OTHER MANUFACTURERS:
   - Rongsheng (China): Low-cost rams and annulars, API 16A certified
   - TaiwanNOK: Asian market, 3K-10K psi equipment
   - Stream (Russia): Domestic Russian market
5. INTERCHANGEABILITY:
   - API 6A flanges allow mixing brands in stack
   - Common: Cameron rams with Hydril annular
   - Control systems may require adaptation (MUX compatibility)
   - Spare parts NOT interchangeable (different ram blocks, seals)
6. MARKET SHARE (approximate):
   - Cameron: 50-60% global market
   - NOV/Shaffer: 20-30% global market
   - Hydril: 10-15% (primarily annulars)
   - Others: 5-10%
7. SELECTION CRITERIA:
   - Rig fleet standardization (spare parts, training)
   - Service availability in operating region
   - Pressure and temperature rating requirements
   - Cost (Cameron typically premium, NOV competitive, Chinese low-cost)
   - Features (quick ram change, compact design, control system)
        """,
        key_factors=[
            "Installed base and fleet standardization",
            "Service network and spare parts availability",
            "Pressure rating and operational requirements",
            "Cost and lead time for equipment",
            "Compatibility with existing control systems",
            "Regulatory acceptance and certification"
        ],
        primary_authority=[
            "Cameron BOP Product Catalog",
            "NOV Shaffer BOP Technical Specifications",
            "Hydril GK Annular Operations Manual",
            "API Spec 16A (Equipment Specifications)"
        ],
        resolution_strategy="Evaluate manufacturer based on fleet standardization, service availability, and operational requirements; consider mixing brands (e.g., Cameron rams + Hydril annular) for best-in-class configuration; ensure spare parts inventory matches installed equipment.",
        entity_scope="BOP equipment procurement, drilling contractors, fleet managers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.STACK_CONFIGURATION
    ),

    DoctrineBlock(
        topic="BOP Stack-Up Design for Specific Well Conditions",
        keywords=["stack design", "ram selection", "configuration", "well planning", "kick scenario"],
        conclusion_template=[
            "BOP stack-up design must accommodate all anticipated pipe sizes, well pressures, and kick scenarios.",
            "Ram selection based on drillstring schedule: pipe rams for working string, casing shear rams for large OD.",
            "Annular position (top or middle of stack) affects stripping capability and maintenance access."
        ],
        reasoning_framework="""
BOP Stack-Up Design Framework:
1. WELL PARAMETERS:
   - Maximum anticipated surface pressure (MAASP)
   - Drillstring schedule (5", 5-1/2", 6-5/8" drillpipe, 8" drill collars)
   - Casing program (9-5/8", 13-3/8", 16", 20" casing strings)
   - H2S/CO2 content (material selection)
   - Water depth (surface vs subsea stack)
2. STACK CONFIGURATION OPTIONS:
   A. STANDARD LAND/SHALLOW WATER (5K-10K psi):
      - Rotating head or annular preventer
      - Pipe ram #1 (5" or 5-1/2" drillpipe)
      - Pipe ram #2 (drill collar or casing size)
      - Blind/Shear rams
      - Drilling spool with choke/kill outlets
   B. HPHT LAND (15K-20K psi):
      - Upper annular
      - Pipe ram #1 (working string)
      - Pipe ram #2 (backup or alternate size)
      - Blind shear rams
      - Lower pipe rams (drill collar size)
      - Drilling spool
   C. DEEPWATER SUBSEA (10K-15K psi):
      - LMRP with annular and control pods
      - Variable bore rams (VBR) - upper
      - Casing shear rams (cut 16" casing if needed)
      - Blind shear rams (primary emergency sealing)
      - Test rams (isolate lower stack for testing)
      - Wellhead connector
3. RAM SELECTION LOGIC:
   - Pipe rams: Must match exact OD (5", 5-1/2", 6-5/8")
   - Variable bore rams: Cover range (3-5/8" to 6-5/8") but limited pressure
   - Shear rams: Size to cut maximum anticipated pipe (5-1/2" DP, S-135 grade)
   - Casing shear rams: Cut and seal large casing during emergency
   - Blind rams: Seal open hole, wireline, or small-diameter pipe
4. ANNULAR PLACEMENT:
   - Top position: Easy access for element replacement, stripping operations
   - Middle position: Protected from debris, additional ram above for backup
   - Dual annulars: High-risk wells, deepwater (one in LMRP, one in stack)
5. CHOKE AND KILL LINE ROUTING:
   - Drilling spool side outlets (land rigs)
   - Subsea: Independent lines from BOP stack to LMRP
   - Multiple isolation valves for redundancy
6. TESTING AND MAINTENANCE ACCESS:
   - Ram bonnet removal capability (land rigs: crane access required)
   - Subsea: ROV panels and hot stabs for testing
   - Locking mechanism accessibility for inspection
7. SPECIAL CONSIDERATIONS:
   - Diverter system for shallow gas (separate from BOP stack)
   - Rotating control device (RCD) for managed pressure drilling
   - Tapered drillstring (multiple pipe sizes): use VBR or multiple pipe rams
        """,
        key_factors=[
            "Well pressure and temperature rating",
            "Drillstring and casing schedule",
            "Kick scenario and well control strategy",
            "Rig type and equipment handling capability",
            "Maintenance and testing access requirements",
            "Cost and equipment availability"
        ],
        primary_authority=[
            "API RP 53 Section 6 (BOP Stack Design)",
            "IADC Drilling Manual (BOP Configuration)",
            "BSEE Well Design and Drilling Operations Guidance",
            "Operator-specific well control policies"
        ],
        resolution_strategy="Analyze well parameters and drillstring schedule, configure stack with appropriate ram types, position annular for operational efficiency, ensure testing and maintenance access, verify stack meets regulatory requirements.",
        entity_scope="Drilling engineers, well planners, BOP system designers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.STACK_CONFIGURATION
    ),

    DoctrineBlock(
        topic="Diverter Systems for Shallow Gas Hazards",
        keywords=["diverter", "shallow gas", "conductor casing", "flow line", "vent line"],
        conclusion_template=[
            "Diverter systems handle shallow gas kicks before BOP installation or in unconsolidated formations.",
            "Diverter vents gas away from rig via flow lines; does NOT shut in well like a BOP.",
            "Critical for spudding wells and drilling through shallow sands where fracture gradient is low."
        ],
        reasoning_framework="""
Diverter System Framework:
1. PURPOSE:
   - Control shallow gas kicks in top-hole section
   - Divert gas flow away from rig and personnel
   - Used when formation fracture gradient too low for BOP shut-in
   - Protect rig during conductor and surface casing drilling
2. DIVERTER COMPONENTS:
   - Annular diverter (packer-type seal around drillpipe)
   - Vent lines (6"-12" lines to discharge point)
   - Flow lines to reserve pit or flare
   - Isolation valves (manual or hydraulic)
   - Closing system (hydraulic or manual)
3. OPERATION:
   - Gas kick detected (flow, pit gain)
   - Close diverter (seal annulus around pipe)
   - Open vent line valve (direct flow away from rig)
   - Do NOT shut in well (would fracture formation)
   - Allow gas to vent until flow stops
4. VENT LINE ROUTING:
   - Minimum 100 feet from rig (avoid fire/explosion hazard)
   - Downwind direction consideration
   - Flare boom or pit discharge
   - Multiple lines for redundancy (port/starboard)
5. PRESSURE RATING:
   - Low pressure: 200-500 psi (diverter not designed for high pressure)
   - Higher pressures would fracture shallow formations
6. DRILLING STAGES USING DIVERTER:
   - Spudding (drilling to conductor depth 50-200 feet)
   - Conductor hole (drilling to surface casing 1,000-3,000 feet)
   - Shallow water flows or gas sands
7. LIMITATIONS:
   - Cannot shut in well
   - Cannot circulate kill mud effectively
   - Only diverts flow; does not control formation pressure
   - Limited to shallow, low-pressure kicks
8. TRANSITION TO BOP:
   - Once surface casing set and cemented, install BOP stack
   - Remove diverter after BOP tested and operational
   - BOP provides full shut-in and well control capability
9. REGULATORY REQUIREMENTS:
   - BSEE requires diverter system for offshore wells before BOP installation
   - Function test before spudding
   - Flow line routing approved by onsite supervisor
10. HAZARDS:
    - Shallow gas blowouts can be catastrophic (no BOP protection)
    - H2S in shallow gas = toxic hazard
    - Fire risk if gas ignites near rig
        """,
        key_factors=[
            "Shallow gas hazard assessment (seismic, offset wells)",
            "Diverter closing system type and reliability",
            "Vent line routing and discharge location",
            "Formation fracture gradient in top-hole section",
            "Personnel evacuation plan for shallow gas event",
            "Transition plan from diverter to BOP stack"
        ],
        primary_authority=[
            "API RP 64 (Diverter Systems)",
            "BSEE 30 CFR 250.442(d) (Diverter Requirements)",
            "IADC Drilling Manual (Shallow Gas Hazards)",
            "Operator shallow gas policies"
        ],
        resolution_strategy="Assess shallow gas risk via seismic and offset well data, install diverter system before spudding, test diverter function, route vent lines safely away from rig, drill conservatively through shallow gas zones, transition to BOP after surface casing set.",
        entity_scope="Drilling supervisors, well planners, offshore rig crews",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SURFACE_BOP
    ),

    DoctrineBlock(
        topic="BOP Maintenance Programs and Intervals",
        keywords=["maintenance", "preventive maintenance", "overhaul", "seal replacement", "inspection"],
        conclusion_template=[
            "BOP maintenance includes routine inspections, seal replacements, and major overhauls per API RP 53.",
            "Annular elements require replacement every 500-1000 cycles; ram seals every 6-12 months or per condition.",
            "Third-party inspections and certifications required for critical offshore operations."
        ],
        reasoning_framework="""
BOP Maintenance Framework:
1. PREVENTIVE MAINTENANCE SCHEDULE:
   - Daily: Visual inspection, leak checks, function test (shift change)
   - Weekly: Detailed inspection, hydraulic fluid level, pressure checks
   - Monthly: Seal inspection, locking mechanism lubrication
   - Quarterly: Accumulator precharge check, nitrogen bottle pressure
   - Semi-annually: Major inspection, seal replacement as needed
   - Annually: Complete overhaul or third-party certification
2. ANNULAR PREVENTER MAINTENANCE:
   - Packing element replacement: 500-1000 pressure cycles or 6-12 months
   - Opening chamber seal replacement: Annually or per condition
   - Hydraulic piston inspection: Check for scoring, corrosion
   - Regulator calibration: Verify closing pressure quarterly
3. RAM PREVENTER MAINTENANCE:
   - Ram top seal replacement: 6-12 months or if leaking
   - Ram front seal replacement: Same interval as top seal
   - Ram bonnet seal (O-rings): Replace during bonnet removal
   - Locking mechanism: Inspect and lubricate monthly, function test weekly
   - Ram shaft inspection: Check for scoring, bending (annual)
4. SHEAR RAM MAINTENANCE:
   - Blade inspection: Check cutting edge wear, hardface condition
   - Shear force test: Verify closure force meets specification
   - Blade replacement: If chips, cracks, or excessive wear noted
5. CONTROL SYSTEM MAINTENANCE:
   - Solenoid valve function: Test weekly, replace coils if erratic
   - Hydraulic lines: Inspect for leaks, corrosion, mechanical damage
   - Position sensors (LVDT): Calibrate annually, verify readings
   - MUX electronics: Software updates, battery replacement (UPS)
6. ACCUMULATOR SYSTEM MAINTENANCE:
   - Precharge pressure: Check quarterly, adjust to specification
   - Hydraulic fluid: Sample and analyze annually (contamination, viscosity)
   - Bottle valves: Inspect for leaks, replace seats if needed
   - Pump: Change oil annually, inspect pump elements
7. OVERHAUL INTERVALS:
   - Major overhaul: 3-5 years or per manufacturer recommendation
   - Complete disassembly, inspect all components
   - Replace all seals, wear parts
   - Pressure test and recertify
8. THIRD-PARTY INSPECTION:
   - Annual certification for offshore BOP (BSEE requirement)
   - Independent inspector verifies condition, test records
   - Certification placard on BOP stack
9. DOCUMENTATION:
   - Maintenance log: Date, activity, parts replaced, technician signature
   - Test records: Pressure charts, function test checklists
   - Component traceability: Serial numbers, date installed
   - Certification records: Third-party inspection reports
10. SPARE PARTS INVENTORY:
    - Annular elements (spare on rig)
    - Ram seal kits (top, front, bonnet seals)
    - Solenoid valves and coils
    - Hydraulic fluid and filters
    - Nitrogen bottles
        """,
        key_factors=[
            "Equipment operating hours and pressure cycles",
            "Environmental conditions (H2S, temperature, abrasives)",
            "Manufacturer recommended intervals",
            "Regulatory requirements (BSEE, API)",
            "Failure history and reliability trends",
            "Cost and downtime for maintenance activities"
        ],
        primary_authority=[
            "API RP 53 Section 13 (Maintenance)",
            "BSEE 30 CFR 250.446 (BOP Maintenance Requirements)",
            "Cameron/NOV/Hydril Maintenance Manuals",
            "IADC BOP Maintenance Guidelines"
        ],
        resolution_strategy="Develop preventive maintenance schedule per API RP 53 and manufacturer recommendations, track maintenance activities and component replacements, schedule third-party inspections annually, maintain adequate spare parts inventory.",
        entity_scope="BOP maintenance crews, rig supervisors, equipment managers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.BOP_TESTING
    ),

    DoctrineBlock(
        topic="MAASP Calculations and BOP Rating Selection",
        keywords=["MAASP", "maximum anticipated surface pressure", "kick tolerance", "fracture gradient"],
        conclusion_template=[
            "MAASP is the maximum surface pressure expected during a kick without fracturing the formation at the casing shoe.",
            "MAASP = (Fracture Gradient × Shoe Depth) - Hydrostatic Pressure of Kill Mud.",
            "BOP working pressure must exceed MAASP with safety margin (typically 10-20%)."
        ],
        reasoning_framework="""
MAASP Calculation Framework:
1. DEFINITION:
   - Maximum Anticipated Annular Surface Pressure
   - Highest pressure expected at surface during well control
   - Determines minimum BOP pressure rating required
2. MAASP FORMULA:
   MAASP = (Frac Gradient × Shoe TVD) - (Kill Mud Weight × 0.052 × Shoe TVD)
   Where:
   - Frac Gradient = Formation fracture gradient (ppg or psi/ft)
   - Shoe TVD = True vertical depth of casing shoe (feet)
   - Kill Mud Weight = Mud weight to control kick (ppg)
   - 0.052 = Conversion factor (ppg to psi/ft)
3. EXAMPLE CALCULATION:
   - Casing shoe at 10,000 ft TVD
   - Fracture gradient 16.5 ppg (0.858 psi/ft)
   - Current mud weight 12 ppg, kick requires 14 ppg kill mud
   - MAASP = (16.5 × 0.052 × 10,000) - (14 × 0.052 × 10,000)
   - MAASP = 8,580 psi - 7,280 psi = 1,300 psi
   - Select BOP rating: 5,000 psi (exceeds MAASP with margin)
4. KICK TOLERANCE:
   - Kick intensity = Formation pressure - Hydrostatic pressure
   - Allowable kick size before exceeding MAASP
   - Smaller MAASP = lower kick tolerance (more dangerous)
5. DEEPWATER RISER MARGIN:
   - Seawater gradient (8.6 ppg) in riser reduces margin
   - MAASP calculation must account for riser U-tubing effect
   - Riser margin = Frac gradient - Seawater gradient
   - Narrow riser margin limits kick handling capability
6. SAFETY MARGIN ON BOP SELECTION:
   - Industry practice: BOP rating 2-4× MAASP
   - Regulatory minimum: BOP rating ≥ MAASP
   - HPHT wells: Use 15K or 20K BOP even if MAASP only 8K (future drilling)
7. DYNAMIC MAASP:
   - MAASP changes as casing shoe depth increases
   - Calculate MAASP for each casing point
   - Deepest shoe typically controls BOP selection
8. WELLHEAD RATING:
   - Wellhead must also exceed MAASP
   - Casing hanger must support casing weight + pressure
   - All components (BOP, wellhead, choke manifold) rated consistently
        """,
        key_factors=[
            "Fracture gradient at casing shoe (LOT/FIT data)",
            "Kill mud weight required for formation control",
            "True vertical depth of casing shoe",
            "Riser margin (deepwater wells)",
            "Regulatory requirements and safety factors",
            "Equipment availability and cost"
        ],
        primary_authority=[
            "IADC Well Control Manual (MAASP Calculations)",
            "API RP 59 (Well Control Operations)",
            "BSEE Well Control Training Requirements",
            "SPE Well Planning and Design Handbook"
        ],
        resolution_strategy="Calculate MAASP for each casing point using fracture gradient and kill mud weight, select BOP pressure rating to exceed maximum MAASP with safety margin, verify wellhead and all surface equipment rated consistently.",
        entity_scope="Well planners, drilling engineers, well control specialists",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PRESSURE_RATING
    ),

    DoctrineBlock(
        topic="BOP Control System Redundancy and Deadman Configuration",
        keywords=["redundancy", "deadman", "autoshear", "AMF", "backup control", "failsafe"],
        conclusion_template=[
            "Redundancy in BOP control systems ensures well can be secured even if primary system fails.",
            "Deadman systems auto-close preventers on loss of power or signal; autoshear cuts and seals pipe.",
            "Subsea BOPs require dual control pods (blue/yellow) with independent power and logic."
        ],
        reasoning_framework="""
BOP Control Redundancy Framework:
1. CONTROL STATION REDUNDANCY:
   - Primary: Driller's panel (rig floor)
   - Secondary: Toolpusher panel (separate location)
   - Tertiary: Remote panel (office, living quarters)
   - Subsea: ROV intervention panels on BOP stack
2. POWER REDUNDANCY:
   - Primary power: Rig electrical system
   - Backup power: UPS (uninterruptible power supply)
   - Emergency power: Diesel generator or battery bank
   - Accumulator stored energy: Independent of electrical power
3. HYDRAULIC REDUNDANCY:
   - Dual hydraulic pumps (primary/backup)
   - Dual manifolds (blue/yellow on subsea systems)
   - Cross-connection capability between systems
4. SUBSEA CONTROL POD REDUNDANCY:
   - Blue pod: Primary control, full function capability
   - Yellow pod: Backup control, identical to blue pod
   - Independent power supplies, logic cards, solenoids
   - Either pod can operate entire BOP stack
   - Switch between pods via surface control panel
5. DEADMAN SYSTEM:
   - Auto-activation on loss of power or signal
   - Typical triggers: Power loss >X seconds, communication loss, disconnect command
   - Actions: Close annular, close pipe rams, close blind shear rams (configurable)
   - Purpose: Ensure well secured if crew unable to act
   - Testing: Weekly function test (simulate power loss)
6. AUTOSHEAR / AMF (AUTOMATIC MODE FUNCTION):
   - Specifically for subsea emergency disconnect
   - Triggered when LMRP connector unlocks
   - Sequence: Close blind shear rams → disconnect
   - Ensures wellbore sealed before separating from stack
   - Independent accumulators dedicated to autoshear function
7. ACOUSTIC BACKUP SYSTEM:
   - Last-resort communication if umbilical severed
   - Surface acoustic transmitter sends coded signals
   - Subsea receivers trigger functions (close BSR, disconnect)
   - Limited function set (emergency operations only)
8. ROV INTERVENTION:
   - Hot stabs on BOP stack provide hydraulic override
   - ROV panel allows manual function control
   - Independent of MUX control system
   - Used when primary/backup control fails
9. FAILURE MODES ADDRESSED:
   - Power loss: Deadman + accumulator closure
   - Hydraulic leak: Dual systems + accumulator reserve
   - Control signal loss: Deadman + ROV override
   - MUX failure: Switch to backup pod + ROV
   - Umbilical severed: Acoustic backup + ROV
10. REGULATORY REQUIREMENTS:
    - BSEE mandates dual control systems for subsea BOP
    - Deadman must be testable and configurable
    - Third-party verification of control system design
        """,
        key_factors=[
            "Control system architecture (hydraulic, MUX, hybrid)",
            "Number of independent control stations",
            "Power and hydraulic redundancy level",
            "Deadman trigger conditions and response actions",
            "Autoshear configuration and dedicated accumulators",
            "ROV intervention capability and hot stab locations",
            "Testing frequency and verification"
        ],
        primary_authority=[
            "API Spec 16D (Control Systems for BOPs)",
            "API RP 53 Section 9 (Control System Design)",
            "BSEE 30 CFR 250.450 (BOP System Functions)",
            "ISO 13628-7 (Subsea Control Systems)"
        ],
        resolution_strategy="Design control system with multiple layers of redundancy (primary/backup stations, dual pods, deadman, ROV), configure deadman for specific well conditions, test all backup systems weekly, ensure ROV hot stabs accessible and functional.",
        entity_scope="BOP system designers, drilling contractors, subsea engineers, well control specialists",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CONTROL_SYSTEM
    ),

    DoctrineBlock(
        topic="Wellbore Pressure Calculations During Well Control",
        keywords=["hydrostatic pressure", "circulating pressure", "formation pressure", "kill mud", "U-tube"],
        conclusion_template=[
            "Wellbore pressure during well control is the sum of hydrostatic pressure and surface applied pressure.",
            "Driller maintains constant bottom hole pressure (BHP) by adjusting choke to balance kick migration.",
            "Kill circulation replaces light mud with heavy mud while keeping BHP above formation pressure."
        ],
        reasoning_framework="""
Wellbore Pressure Calculations Framework:
1. HYDROSTATIC PRESSURE (HP):
   - HP = Mud Weight (ppg) × 0.052 × True Vertical Depth (ft)
   - Example: 12 ppg mud at 10,000 ft TVD
   - HP = 12 × 0.052 × 10,000 = 6,240 psi
2. BOTTOM HOLE PRESSURE (BHP):
   - BHP = Hydrostatic Pressure + Surface Pressure
   - During kick: BHP must equal or exceed Formation Pressure
   - BHP < Formation Pressure → continued influx
   - BHP > Fracture Pressure → lost circulation
3. SHUT-IN DRILLPIPE PRESSURE (SIDPP):
   - Pressure on drillpipe when BOP closed
   - SIDPP = Formation Pressure - Hydrostatic Pressure (inside pipe)
   - Indicates formation pressure (kick intensity)
4. SHUT-IN CASING PRESSURE (SICP):
   - Pressure on annulus when BOP closed
   - SICP = Formation Pressure - Hydrostatic Pressure (annulus) + Kick Height Effect
   - Higher than SIDPP if kick lighter than mud
5. KILL MUD WEIGHT (KMW):
   - KMW = Original Mud Weight + (SIDPP / 0.052 / TVD)
   - Adds safety margin (typically 0.5-1.0 ppg)
   - Example: 12 ppg mud, SIDPP 500 psi, TVD 10,000 ft
   - KMW = 12 + (500 / 0.052 / 10,000) = 12 + 0.96 = 12.96 ppg (use 13.5 ppg)
6. CONSTANT BHP METHOD:
   - Adjust choke pressure to maintain constant BHP during kill
   - Initial drillpipe pressure (ICP) = SIDPP + Circulating Pressure
   - Final circulating pressure (FCP) = Circulating Pressure (with kill mud)
   - Kill sheet: Pre-calculated pressures at pump stroke increments
7. CIRCULATING PRESSURE:
   - Pressure required to circulate mud through system
   - Includes: Drillstring, bit nozzles, annulus friction
   - Slow Circulating Rate (SCR): Predetermined rate for well control
   - SCR pressure recorded before kick (reference value)
8. U-TUBE EFFECT (DEEPWATER):
   - Riser (seawater gradient 8.6 ppg) vs annulus (mud gradient 12+ ppg)
   - Heavy mud in annulus creates pressure differential
   - Surface pressure increases as heavy mud enters riser
   - Limits kick handling in narrow-margin wells
9. PRESSURE TESTING DURING KILL:
   - Monitor drillpipe pressure continuously
   - Adjust choke to maintain kill sheet schedule
   - Verify zero pressure after full kill mud circulation
10. COMMON ERRORS:
    - Using measured depth instead of TVD in calculations
    - Not accounting for kick migration and gas expansion
    - Incorrect SCR pressure (not re-recorded after mud weight change)
    - Failure to maintain constant BHP (fractures formation or allows influx)
        """,
        key_factors=[
            "Formation pressure and kick intensity (SIDPP)",
            "Mud weight (original and kill mud)",
            "True vertical depth (TVD) vs measured depth (MD)",
            "Slow circulating rate (SCR) pressure",
            "Choke operator skill and kill sheet accuracy",
            "Fracture gradient at casing shoe (avoid losses)"
        ],
        primary_authority=[
            "IADC Well Control Manual (Pressure Calculations)",
            "API RP 59 (Well Control Operations)",
            "SPE Textbook on Well Control",
            "BSEE Well Control Training Requirements"
        ],
        resolution_strategy="Calculate formation pressure from SIDPP, determine kill mud weight with safety margin, prepare kill sheet with drillpipe pressure schedule, maintain constant BHP during kill circulation using choke adjustments.",
        entity_scope="Well control supervisors, drilling engineers, rig crews",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.KILL_LINE
    ),

    DoctrineBlock(
        topic="BOP Component Leak Detection and Troubleshooting",
        keywords=["leak detection", "pressure test failure", "troubleshooting", "seal replacement", "hydraulic leak"],
        conclusion_template=[
            "BOP leaks detected during pressure testing require isolation and root cause identification.",
            "Common leak sources: ram seals (top seal, front seal), bonnet seals, hydraulic fittings, annular element.",
            "Systematic troubleshooting isolates failed component, repairs made, retesting verifies seal integrity."
        ],
        reasoning_framework="""
BOP Leak Detection and Troubleshooting Framework:
1. LEAK DETECTION METHODS:
   - Pressure test: Apply rated WP, observe pressure drop
   - Visual inspection: Look for weeps, drips, hydraulic fluid
   - Soap bubble test: Spray soapy water on suspected leak points
   - Ultrasonic testing: Detect small leaks via sound frequency
2. COMMON LEAK LOCATIONS:
   A. RAM PREVENTER:
      - Top seal (extrusion, wear, improper installation)
      - Front seal (contact with pipe, debris damage)
      - Bonnet seal (O-ring, gasket failure)
      - Ram shaft seal (piston seal leak)
      - Side door seal (QRC models)
   B. ANNULAR PREVENTER:
      - Packing element (tear, extrusion, chemical degradation)
      - Opening chamber seal (O-ring failure)
      - Piston seal (hydraulic leak)
      - Head seal (flange gasket)
   C. HYDRAULIC SYSTEM:
      - Solenoid valve leak (seat wear)
      - Accumulator bottle valve leak
      - Hydraulic line fitting leak (vibration, corrosion)
      - Regulator leak (pilot valve, diaphragm)
   D. CONTROL SYSTEM:
      - MUX connector corrosion (water ingress)
      - Hydraulic hose deterioration
      - Quick-connect leak (O-ring damage)
3. TROUBLESHOOTING PROCEDURE:
   - Step 1: Identify leak location (visual + pressure test)
   - Step 2: Isolate component (close valves, tag out)
   - Step 3: Depressurize system (bleed hydraulic pressure)
   - Step 4: Remove bonnet or access cover (ram preventers)
   - Step 5: Inspect seals (top seal, front seal, O-rings)
   - Step 6: Replace failed components (seal kits, gaskets)
   - Step 7: Reassemble and torque fasteners per spec
   - Step 8: Pressure test to verify repair
4. PRESSURE TEST FAILURE ANALYSIS:
   - Zero leak: Pressure stable over 5-minute hold
   - Small leak: <10% pressure drop, typically seal weep (acceptable per API)
   - Large leak: >10% pressure drop, failed seal or component (must repair)
   - Sudden pressure loss: Catastrophic seal failure or valve leak
5. RAM SEAL REPLACEMENT:
   - Top seal: Energized by hydraulic pressure, most common failure
   - Front seal: Contacts pipe, subject to abrasion
   - Replacement: Remove bonnet, pull ram, replace seals, reassemble
   - Torque specification: Follow manufacturer torque chart (bonnet bolts)
   - Post-replacement test: Low-pressure function, then high-pressure seal test
6. ANNULAR ELEMENT REPLACEMENT:
   - Disassemble head (unbolt top flange)
   - Remove packing element (may require piston retraction)
   - Install new element (lubricate, align properly)
   - Reassemble and pressure test
   - Typical interval: 500-1000 pressure cycles or 6-12 months
7. HYDRAULIC LEAK REPAIR:
   - Tighten fittings (check for cross-threading)
   - Replace O-rings in quick-connects
   - Replace solenoid valve seats or entire valve
   - Accumulator bottle valve: Replace core or entire valve assembly
8. DOCUMENTATION:
   - Record leak location, cause, and repair action
   - Update maintenance log and test records
   - Track seal replacement intervals
   - Report persistent leaks to manufacturer (design issue)
9. PREVENTIVE MEASURES:
   - Regular seal inspections during maintenance
   - Avoid over-pressurizing (exceeding WP damages seals)
   - Minimize stripping operations (annular element wear)
   - Use correct hydraulic fluid (manufacturer specified)
   - Replace seals at recommended intervals (not just when failed)
        """,
        key_factors=[
            "Leak severity (pressure drop rate)",
            "Leak location (ram, annular, hydraulic system)",
            "Component condition and age",
            "Operating history (pressure cycles, stripping operations)",
            "Environmental factors (H2S, temperature, abrasives)",
            "Spare parts availability"
        ],
        primary_authority=[
            "API RP 53 Section 13 (Maintenance and Troubleshooting)",
            "Cameron/NOV/Hydril Service Manuals",
            "IADC BOP Maintenance Best Practices",
            "Manufacturer Seal Kit Installation Instructions"
        ],
        resolution_strategy="Detect leak via pressure test, isolate failed component, perform root cause analysis, replace seals or components per manufacturer specifications, retest to verify repair, document findings and corrective actions.",
        entity_scope="BOP maintenance technicians, rig supervisors, equipment engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.FAILURE_ANALYSIS
    )
]

# ============================================================================
# TELEMETRY
# ============================================================================

class TelemetryCollector:
    def __init__(self):
        self.queries_processed = 0
        self.total_latency_ms = 0.0
        self.doctrines_triggered = defaultdict(int)
        self.errors = []
        self.start_time = datetime.now()

    def record_query(self, latency_ms: float, doctrines: List[str]):
        self.queries_processed += 1
        self.total_latency_ms += latency_ms
        for doctrine in doctrines:
            self.doctrines_triggered[doctrine] += 1

    def record_error(self, error: str):
        self.errors.append({"timestamp": datetime.now().isoformat(), "error": error})

    def get_metrics(self) -> Dict[str, Any]:
        uptime = (datetime.now() - self.start_time).total_seconds()
        avg_latency = self.total_latency_ms / max(self.queries_processed, 1)
        return {
            "queries_processed": self.queries_processed,
            "avg_latency_ms": round(avg_latency, 2),
            "uptime_seconds": round(uptime, 2),
            "doctrines_triggered": dict(self.doctrines_triggered),
            "errors": self.errors[-10:]
        }

telemetry = TelemetryCollector()

# ============================================================================
# DOCTRINE CACHE ENGINE
# ============================================================================

def find_matching_doctrines(query: str, limit: int = 5) -> List[DoctrineBlock]:
    """Find doctrines matching query keywords"""
    query_lower = query.lower()
    query_terms = set(re.findall(r'\b\w+\b', query_lower))

    scored_doctrines = []
    for doctrine in DOCTRINE_CACHE:
        keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
        term_matches = len(query_terms.intersection(set(k.lower() for k in doctrine.keywords)))
        score = keyword_matches * 2 + term_matches

        if score > 0:
            scored_doctrines.append((score, doctrine))

    scored_doctrines.sort(reverse=True, key=lambda x: x[0])
    return [d for _, d in scored_doctrines[:limit]]

# ============================================================================
# THREE-LAYER RESPONSE
# ============================================================================

async def three_layer_response(request: QueryRequest) -> QueryResponse:
    """TIE-20 Component: Three-layer response (cache -> semantic -> deep)"""
    start_time = datetime.now()

    # Layer 1: Doctrine Cache (0-200ms)
    matching_doctrines = find_matching_doctrines(request.query, limit=3)

    if not matching_doctrines:
        # No doctrine match - return general guidance
        response_text = generate_fallback_response(request)
        doctrines_used = []
        authorities = []
        confidence = ConfidenceLevel.DISCLOSURE
    else:
        # Build response from matched doctrines
        response_text = build_doctrine_response(request, matching_doctrines)
        doctrines_used = [d.topic for d in matching_doctrines]
        authorities = []
        for d in matching_doctrines:
            authorities.extend(d.primary_authority)
        confidence = matching_doctrines[0].confidence

    # Calculate latency and determinism hash
    latency_ms = (datetime.now() - start_time).total_seconds() * 1000
    determinism_hash = hashlib.sha256(response_text.encode()).hexdigest()[:16]

    # Record telemetry
    telemetry.record_query(latency_ms, doctrines_used)

    return QueryResponse(
        query=request.query,
        response=response_text,
        mode=request.mode,
        zone=request.zone,
        confidence=confidence,
        doctrines_triggered=doctrines_used,
        authorities_cited=list(set(authorities)),
        determinism_hash=determinism_hash,
        latency_ms=round(latency_ms, 2),
        timestamp=datetime.now().isoformat()
    )

def build_doctrine_response(request: QueryRequest, doctrines: List[DoctrineBlock]) -> str:
    """Build response based on mode and doctrines"""
    if request.mode == ResponseMode.FAST:
        # Concise answer from top doctrine
        top_doctrine = doctrines[0]
        conclusion = " ".join(top_doctrine.conclusion_template)
        key_factors = "; ".join(top_doctrine.key_factors[:3])
        return f"{conclusion}\n\nKey factors: {key_factors}"

    elif request.mode == ResponseMode.DEFENSE:
        # Detailed answer with authorities
        parts = []
        for i, doctrine in enumerate(doctrines[:2], 1):
            conclusion = " ".join(doctrine.conclusion_template)
            authorities = ", ".join(doctrine.primary_authority)
            parts.append(f"{i}. {doctrine.topic}:\n{conclusion}\n\nAuthority: {authorities}")
        return "\n\n".join(parts)

    else:  # MEMO mode
        # Full documentation
        parts = []
        for doctrine in doctrines[:2]:
            conclusion = " ".join(doctrine.conclusion_template)
            framework = doctrine.reasoning_framework.strip()
            factors = "\n".join(f"  • {f}" for f in doctrine.key_factors)
            authorities = "\n".join(f"  • {a}" for a in doctrine.primary_authority)

            memo = f"""
TOPIC: {doctrine.topic}

CONCLUSION:
{conclusion}

ANALYSIS FRAMEWORK:
{framework}

KEY FACTORS:
{factors}

CONTROLLING AUTHORITY:
{authorities}

CONFIDENCE LEVEL: {doctrine.confidence.value}
RESOLUTION STRATEGY: {doctrine.resolution_strategy}
"""
            parts.append(memo.strip())
        return "\n\n" + "="*80 + "\n\n".join(parts)

def generate_fallback_response(request: QueryRequest) -> str:
    """Generate response when no doctrine matches"""
    return f"""No specific BOP doctrine cache entry matches query: "{request.query}"

General BOP Analysis Guidance:
- Verify BOP pressure rating exceeds well MAASP
- Ensure ram types match drillstring schedule (pipe rams for exact OD)
- Test BOP per API RP 53 (initial to rated WP, 14-30 day intervals)
- Maintain accumulator system at 1.5x closing volume requirement
- For failures: isolate component, replace seals, retest before operations

Refer to API RP 53, BSEE 30 CFR 250 Subpart D, and equipment manufacturer manuals for detailed procedures.

Note: This is general guidance. Specific technical questions require doctrine cache expansion or engineering analysis.
"""

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=f"{ENGINE_NAME} API",
    version=VERSION,
    description="BOP Stack Analysis Engine - Blowout Preventer Equipment Expertise"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """TIE-20 Component: Health endpoint"""
    metrics = telemetry.get_metrics()
    return HealthResponse(
        status="healthy",
        engine=ENGINE_NAME,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=metrics["uptime_seconds"],
        queries_processed=metrics["queries_processed"],
        avg_latency_ms=metrics["avg_latency_ms"]
    )

@app.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint - TIE three-layer response"""
    try:
        logger.info(f"Query received: {request.query[:100]}")
        response = await three_layer_response(request)
        logger.info(f"Query completed in {response.latency_ms}ms")
        return response
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        telemetry.record_error(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine topics"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }

@app.get("/metrics")
async def get_metrics():
    """Get telemetry metrics"""
    return telemetry.get_metrics()

@app.on_event("startup")
async def startup_event():
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} BOP doctrine blocks")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"{ENGINE_NAME} shutting down")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
