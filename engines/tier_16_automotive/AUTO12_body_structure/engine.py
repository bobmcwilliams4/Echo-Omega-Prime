"""
AUTO12 Body Structure Analysis Engine v1.0.0
TIE-Grade Automotive Body Engineering Intelligence

Covers: Body-in-White design, crash structure analysis, corrosion protection,
NVH evaluation, aerodynamic body optimization, structural integrity testing.

Port: 9322
"""

import sys
from pathlib import Path

# CRITICAL: Add parent to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import re
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict, Counter

from loguru import logger
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# ============================================================================
# ENUMS & MODELS
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
    DESIGN = "DESIGN"
    TESTING = "TESTING"
    EVALUATION = "EVALUATION"


class IssueCategory(str, Enum):
    CRASH_STRUCTURE = "CRASH_STRUCTURE"
    BIW_DESIGN = "BIW_DESIGN"
    CORROSION = "CORROSION"
    NVH = "NVH"
    AERODYNAMICS = "AERODYNAMICS"
    STRUCTURAL_INTEGRITY = "STRUCTURAL_INTEGRITY"
    MATERIAL_SELECTION = "MATERIAL_SELECTION"
    JOINING_METHODS = "JOINING_METHODS"
    WEIGHT_OPTIMIZATION = "WEIGHT_OPTIMIZATION"
    MANUFACTURING = "MANUFACTURING"


class QueryRequest(BaseModel):
    query: str = Field(..., description="Body structure question or scenario")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: Optional[AnalysisZone] = Field(default=None, description="Analysis context zone")
    include_alternatives: bool = Field(default=False, description="Include alternative approaches")


class QueryResponse(BaseModel):
    query: str
    mode: ResponseMode
    answer: str
    confidence: ConfidenceLevel
    categories: List[IssueCategory]
    doctrines_triggered: List[str]
    response_time_ms: float
    determinism_hash: str
    zone: Optional[AnalysisZone]
    alternatives: Optional[List[str]] = None
    fragility_score: Optional[float] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrine_count: int
    categories: int
    uptime_seconds: float
    total_queries: int
    avg_response_ms: float
    cache_hit_rate: float


# ============================================================================
# DOCTRINE BLOCKS - REAL AUTOMOTIVE BODY ENGINEERING EXPERTISE
# ============================================================================

class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    category: IssueCategory
    zone: AnalysisZone


DOCTRINE_CACHE = [
    DoctrineBlock(
        topic="body_in_white_design_principles",
        keywords=["biw", "body-in-white", "structural design", "platform architecture", "body structure"],
        conclusion_template="BIW design must balance structural rigidity, crash performance, weight targets, and manufacturing feasibility. The body structure serves as the foundation for all subsequent assembly and must meet conflicting requirements: maximum stiffness for handling/NVH, strategic deformation zones for crash, minimal weight for efficiency, and cost-effective manufacturing.",
        reasoning_framework="""
        BIW design fundamentals:
        1. Platform architecture defines hard points (suspension mounts, powertrain, seat tracks)
        2. Torsional rigidity target typically 15,000-25,000 Nm/deg for passenger vehicles
        3. First body mode should exceed 35-40 Hz to avoid resonance with suspension
        4. Load paths must be continuous from impact zones through structure to opposite side
        5. Material selection hierarchy: UHSS for A/B pillars, mild steel for non-critical, aluminum for mass reduction
        6. Joining strategy affects stiffness: laser welds > spot welds > adhesive bonding
        7. Tunnel and rocker stiffness critical for torsional rigidity
        8. Roof structure must support rollover loads (3x vehicle weight minimum)
        9. Firewall separates engine bay from cabin, must seal against noise/fumes/fire
        10. Package efficiency: maximize interior volume while minimizing exterior dimensions

        Design validation sequence:
        - CAE torsional rigidity analysis (target correlation within 5% of physical)
        - Modal analysis for body modes and NVH frequencies
        - Crash simulation for frontal, side, rear, roof crush, pole impact
        - Durability analysis for 150,000 mile equivalent loading
        - Manufacturing feasibility review (stamping, welding, assembly sequence)

        Common failure modes:
        - Insufficient tunnel stiffness causing body flex and door closing issues
        - Inadequate spot weld count leading to fatigue cracks
        - Panel buckling under load due to insufficient reinforcement
        - Corrosion in closed box sections where drainage is blocked
        - NVH issues from resonant frequencies matching powertrain excitation
        """,
        key_factors=[
            "Torsional rigidity target (Nm/deg)",
            "First body mode frequency (Hz)",
            "Weight target (kg) vs. structural requirements",
            "Manufacturing constraints (stamping depth, weld accessibility)",
            "Crash load path continuity",
            "Material gauge optimization",
            "Joint stiffness and fatigue life"
        ],
        primary_authority=[
            "SAE J1100 Motor Vehicle Dimensions",
            "FMVSS 216 Roof Crush Resistance",
            "Euro NCAP Assessment Protocol",
            "ISO 20766 Road Vehicles - Torsional Stiffness",
            "Automotive Steel Design Manual (AISI)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.BIW_DESIGN,
        zone=AnalysisZone.DESIGN
    ),

    DoctrineBlock(
        topic="frontal_crash_structure_design",
        keywords=["frontal crash", "crumple zone", "crash energy management", "fwrd crash", "barrier impact"],
        conclusion_template="Frontal crash structure must manage kinetic energy through controlled deformation while maintaining survival space integrity. The structure creates a deceleration pulse profile that keeps occupant forces below injury thresholds (40g chest acceleration, 1000 HIC head injury criterion) through staged collapse of crush zones.",
        reasoning_framework="""
        Frontal crash energy management (40 mph NCAP, 35 mph IIHS):
        1. Front rails are primary energy absorbers, designed for progressive buckling
        2. Crash box (sacrificial element) initiates collapse at predetermined load
        3. Front rail cross-section optimized for stable folding (typically octagonal or rectangular)
        4. Shotgun/tunnel interface must not intrude into footwell during crash
        5. Firewall designed as secondary barrier if front rail collapse is insufficient
        6. Bumper beam distributes impact load to left/right rail structures
        7. Subframe designed to separate from body at controlled load to manage intrusion

        Energy absorption calculation:
        Kinetic energy = 0.5 * mass * velocity^2
        For 1500 kg vehicle at 40 mph (17.88 m/s): E = 239 kJ
        Front rail stroke typically 300-500 mm
        Required crush force = Energy / stroke = 239,000 J / 0.4 m = 597 kN (60 tons)
        Distributed between two rails: ~30 tons each

        Load path analysis:
        - Small overlap crash (25% IIHS): wheel must be driven rearward/outboard, not into footwell
        - Offset deformable barrier: energy shared between vehicles, lower pulse than rigid barrier
        - Pole impact: concentrated load requires local reinforcement at rail tip

        Material selection for crash rails:
        - Mild steel (300 MPa) for ductile progressive collapse
        - UHSS (1500 MPa) for B-pillar and rocker to resist side intrusion during frontal offset
        - Tailor-welded blanks to vary thickness along rail length
        - Hot stamping for complex shapes with high strength and controlled collapse zones

        Validation testing:
        - Full frontal rigid barrier (FMVSS 208): uniform deceleration, airbag deployment timing
        - Offset deformable barrier (40% overlap): asymmetric loading, door opening after crash
        - Small overlap (25% IIHS): critical for driver footwell intrusion and lower leg injury
        - Compatibility testing: assess aggressivity to other vehicles (FWDB, MPDB protocols)
        """,
        key_factors=[
            "Front rail stroke distance (mm)",
            "Crush force magnitude and consistency",
            "Deceleration pulse shape (g vs. time)",
            "Survival space intrusion limits",
            "Crash box trigger load",
            "Load path distribution efficiency",
            "Compatibility with offset and small overlap scenarios"
        ],
        primary_authority=[
            "FMVSS 208 Occupant Crash Protection",
            "Euro NCAP Frontal Impact Protocol",
            "IIHS Small Overlap Crash Test",
            "SAE J2194 Collision Deformation Classification",
            "ISO 6487 Road Vehicles - Measurement Techniques in Impact Tests"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CRASH_STRUCTURE,
        zone=AnalysisZone.TESTING
    ),

    DoctrineBlock(
        topic="side_impact_structure_design",
        keywords=["side impact", "b-pillar", "door intrusion", "lateral crash", "side barrier"],
        conclusion_template="Side impact protection requires high-strength door beams, reinforced B-pillar, and rocker structure to resist lateral intrusion. The challenge is managing energy with minimal crush space (150-200 mm door cavity vs. 400-500 mm frontal structure), necessitating ultra-high strength materials and load distribution to sills and roof rails.",
        reasoning_framework="""
        Side impact scenarios (FMVSS 214, Euro NCAP, IIHS):
        1. Moving deformable barrier (MDB): 1368 kg barrier at 31 mph (50 km/h) into driver door
        2. Pole test: rigid 254 mm pole impacting driver door at 20 mph (32 km/h)
        3. Far-side occupant: lateral motion into center console or opposite occupant

        Structural strategy:
        - Door beams (typically 2 per door): outer beam at waist, inner beam at hip level
        - B-pillar reinforcement: hot-stamped 1500 MPa steel, extends from rocker to roof rail
        - Rocker (sill): box section distributes load from B-pillar to front/rear of vehicle
        - Roof rail: resists B-pillar rotation during side impact, critical for roof strength
        - Cross-car load path: tunnel and floor cross-members transfer energy to opposite sill
        - Seat structure: must resist lateral loading without excessive occupant movement

        Material selection:
        - Door beams: UHSS 1000-1500 MPa, often hot-stamped for complex shapes
        - B-pillar inner/outer: tailor-welded blank with 1500 MPa at critical sections
        - Rocker: 600-1000 MPa steel, closed section for torsional contribution
        - Roof rail: 800-1200 MPa, must support roof crush and side impact

        Intrusion limits (Euro NCAP good rating):
        - B-pillar lower: <120 mm
        - B-pillar upper: <100 mm
        - Door center: <200 mm
        - Footwell: <100 mm
        - Rocker: <50 mm (critical for pelvic protection)

        Energy absorption mechanisms:
        - Door beam bending: limited energy due to small stroke
        - B-pillar rotation and crushing: primary energy absorber
        - Rocker deformation: spreads load longitudinally
        - Door panel and trim compression: minimal contribution
        - Seat deformation: absorbs some energy but limits occupant protection space

        Critical design details:
        - B-pillar attachment to rocker: high-strength bolts or welds, typical failure point
        - Door beam anchorage: must not pull out during impact
        - Hinge pillar reinforcement: prevents door jamming, allows egress after crash
        - Rear door overlap: load transfer from rear door into B-pillar structure
        """,
        key_factors=[
            "B-pillar intrusion (mm)",
            "Door beam strength and attachment",
            "Rocker stiffness and load distribution",
            "Cross-car load path efficiency",
            "Material strength in critical sections",
            "Intrusion into pelvic and thorax zones",
            "Post-crash door operability"
        ],
        primary_authority=[
            "FMVSS 214 Side Impact Protection",
            "Euro NCAP Side Impact Protocol",
            "IIHS Side Impact Crash Test",
            "SAE J2882 Side Impact Barrier Specifications",
            "ISO 12097 Road Vehicles - Side Impact Test Procedures"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CRASH_STRUCTURE,
        zone=AnalysisZone.TESTING
    ),

    DoctrineBlock(
        topic="roof_crush_and_rollover_protection",
        keywords=["roof crush", "rollover", "roof strength", "pillar strength", "fmvss 216"],
        conclusion_template="Roof structure must withstand compressive loading equivalent to 3.0x vehicle weight (FMVSS 216a) with intrusion not exceeding 5 inches, ensuring survival space during rollover. The roof ring (A/B/C/D pillars plus rails) acts as an integrated structure, with any weak link causing catastrophic failure.",
        reasoning_framework="""
        Roof crush testing (FMVSS 216a):
        - Quasi-static loading: rigid plate at 5 degrees forward, 25 degrees inboard
        - Load requirement: 3.0x unloaded vehicle weight (UVW) for vehicles ≤6000 lbs
        - Maximum intrusion: 5 inches (127 mm) measured from rigid plane
        - Residual headroom must allow for occupant clearance with restraints

        Roof ring structural design:
        1. A-pillar: must support front of roof, angled for aerodynamics but reduces strength
        2. B-pillar: primary vertical support, hot-stamped 1500 MPa typical
        3. C-pillar: often weakest link due to styling (fastback, coupe), requires reinforcement
        4. D-pillar (if present): SUV/wagon rear pillar, critical for rear passenger protection
        5. Roof rails (left/right): longitudinal beams connecting pillars
        6. Roof cross-members: lateral beams preventing rail spread during crush
        7. Rear header: crossbar at rear of roof opening (above rear window)

        Load path in rollover:
        - Initial contact typically on A-pillar or roof rail corner
        - Load distributes through roof ring as structure deforms
        - Weak pillar buckles, concentrating load on adjacent structures
        - Floor pan and tunnel resist downward intrusion of roof
        - Seats must not collapse rearward during rollover (FMVSS 207)

        Material and design strategies:
        - Hot-stamped A/B/C pillars: 1500 MPa martensitic steel, formed at 900°C
        - Roof rail: closed box section, 1000-1500 MPa depending on vehicle size
        - Roof cross-members: strategically placed to prevent rail buckling
        - Windshield and rear glass bonding: adhesive bonded glass adds 20-30% roof stiffness
        - Sunroof opening: major structural compromise, requires heavy reinforcement around opening

        Validation approach:
        - CAE prediction of crush force vs. displacement curve
        - Physical testing with correlation to CAE within 10% at critical loads
        - Intrusion measured with photogrammetry or laser scanning
        - Dynamic rollover testing (Jordan Rollover System) for real-world validation
        - Roof strength-to-weight ratio (SWR): strength/weight, higher is better

        Common design failures:
        - C-pillar buckling due to thin gauge or poor geometry
        - A-pillar folding from excessive windshield rake angle
        - Roof rail separation from pillar at attachment welds
        - Sunroof reinforcement inadequate for opening size
        - Cross-member count insufficient to prevent rail inward buckling
        """,
        key_factors=[
            "Roof crush force (multiple of vehicle weight)",
            "Maximum intrusion (inches)",
            "Pillar buckling resistance",
            "Roof rail continuity and stiffness",
            "Sunroof reinforcement adequacy",
            "Windshield bonding contribution",
            "Strength-to-weight ratio"
        ],
        primary_authority=[
            "FMVSS 216a Roof Crush Resistance",
            "IIHS Roof Strength Test",
            "SAE J2412 Roof Crush Resistance Rating",
            "Euro NCAP Rollover Protection",
            "ISO 3560 Road Vehicles - Rollover Test Procedures"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CRASH_STRUCTURE,
        zone=AnalysisZone.TESTING
    ),

    DoctrineBlock(
        topic="corrosion_protection_strategies",
        keywords=["corrosion", "rust prevention", "galvanizing", "e-coat", "cavity wax", "perforation warranty"],
        conclusion_template="Corrosion protection requires multi-layer strategy: zinc coating on steel substrate (galvanizing), electro-deposition coating (e-coat) for complete coverage, PVC sealers for joints/seams, and cavity wax for closed box sections. Failure of any layer accelerates corrosion, with perforation typically occurring 5-12 years depending on environment and protection quality.",
        reasoning_framework="""
        Corrosion mechanisms in automotive structures:
        1. Surface corrosion: cosmetic rust on exposed surfaces, minimal structural impact
        2. Crevice corrosion: concentrated in gaps (spot welds, hemmed flanges), leads to perforation
        3. Galvanic corrosion: dissimilar metals (steel-aluminum contact) accelerate degradation
        4. Stress corrosion: cracks propagate in high-stress areas (suspension mounts)
        5. Filiform corrosion: threadlike corrosion under paint, common in humid climates

        Corrosion protection layers (barrier system):

        Layer 1 - Substrate protection:
        - Hot-dip galvanizing: zinc coating 60-90 g/m² (both sides), provides sacrificial protection
        - Electrogalvanizing: thinner zinc layer (20-40 g/m²), better surface finish for Class A panels
        - Galvanneal: zinc-iron alloy, improves paint adhesion and formability
        - Aluminum-silicon coating (Al-Si): used for hot-stamped parts, 150 g/m² typical

        Layer 2 - Electro-coat (E-coat):
        - Cathodic electrophoretic deposition, 15-25 microns thickness
        - Complete coverage including box sections (e-coat floods interior cavities)
        - Provides electrical isolation and paint adhesion base
        - Typical bake: 175-185°C for 20-30 minutes

        Layer 3 - Primer and basecoat:
        - Primer: 30-40 microns, fills surface imperfections
        - Basecoat: 15-20 microns, provides color and UV protection
        - Clearcoat: 40-50 microns, gloss and scratch resistance

        Layer 4 - Sealers and underbody protection:
        - PVC sealer: applied to joints, seams, hemmed flanges (1-3 mm thick)
        - Underbody coating: rubberized or wax-based, 2-4 mm on floor pan and wheel wells
        - Cavity wax: liquid wax injected into closed sections (rockers, pillars, doors)
        - Chip guards: thick coating on leading edges and rocker panels

        Critical corrosion-prone areas:
        - Rocker panels and sills: stone impact damage, road salt accumulation
        - Wheel wells: constant wet/dry cycling, stone impacts
        - Door hems: moisture trapping in fold, incomplete e-coat penetration
        - Spot weld edges: crevice corrosion starting point
        - Suspension attachment points: stress corrosion from cyclic loading
        - Tailgate and decklid: lower edge moisture accumulation
        - Windshield cowl: water drainage area, poor cavity wax penetration

        Corrosion testing protocols:
        - Cyclic corrosion test (CCT): salt spray, wet, dry, freeze cycles (ASTM B117, ISO 11997)
        - Scab corrosion test: scribes through paint to bare metal, measure spread from scribe
        - Perforation test: time to through-rust on structural panels
        - CASS test: accelerated salt spray with acetic acid
        - Real-world exposure: Arizona (UV), Florida (humidity/salt), Michigan (road salt)

        Warranty implications:
        - Cosmetic corrosion warranty: 3-5 years (surface rust, paint blistering)
        - Perforation warranty: 5-12 years (hole through body panel)
        - Extended warranties require more robust protection (thicker e-coat, better cavity wax)
        """,
        key_factors=[
            "Zinc coating weight (g/m²)",
            "E-coat thickness and coverage completeness",
            "Cavity wax penetration into closed sections",
            "PVC sealer application at critical joints",
            "Dissimilar metal isolation (aluminum-steel contact)",
            "Drainage design to prevent moisture accumulation",
            "Cyclic corrosion test performance (cycles to perforation)"
        ],
        primary_authority=[
            "SAE J2334 Cosmetic Corrosion Test",
            "ASTM B117 Salt Spray Testing",
            "ISO 11997 Paints and Varnishes - Corrosion Test",
            "GMW3286 Corrosion Protection Performance",
            "VDA 621-415 Corrosion Testing of Automotive Components"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CORROSION,
        zone=AnalysisZone.TESTING
    ),

    DoctrineBlock(
        topic="nvh_body_structure_contribution",
        keywords=["nvh", "noise vibration harshness", "body boom", "drumming", "panel resonance", "road noise"],
        conclusion_template="Body structure contributes to NVH through panel resonances (drumming), structural vibration transmission (boom), and inadequate stiffness allowing suspension/powertrain excitation to propagate. Effective NVH control requires first body mode above 35 Hz, localized panel damping, strategic bead patterns to shift resonant frequencies, and discontinuous load paths to block vibration transmission.",
        reasoning_framework="""
        NVH phenomena related to body structure:

        1. Body boom (25-80 Hz):
        - Caused by structural resonance excited by road inputs or powertrain
        - First body mode (torsion) typically 32-40 Hz, second mode (bending) 35-45 Hz
        - Mitigation: increase torsional stiffness, isolate excitation sources
        - Target: first body mode >35 Hz to avoid overlap with suspension resonance (10-15 Hz)

        2. Panel drumming (100-300 Hz):
        - Large unsupported panels (roof, floor, doors) vibrate like drumhead
        - Excited by tire cavity resonance (200-250 Hz) or road roughness
        - Mitigation: add bead patterns, local reinforcements, damping material
        - Target: shift panel modes outside tire cavity resonance band

        3. Road noise (200-1000 Hz):
        - Transmitted through suspension mounts, tire contact patch
        - Body structure acts as sounding board amplifying tire/road interaction
        - Mitigation: isolate suspension from body, add damping to transmission paths
        - Target: transmission loss >30 dB in 200-500 Hz critical band

        4. Wind noise (500-5000 Hz):
        - Primarily sealing issue, but body stiffness affects door/window sealing
        - A-pillar and mirror turbulence excites side glass and door panels
        - Mitigation: improve seal compression, stiffen door frame, optimize A-pillar shape

        Structural design for NVH:

        Body stiffness targets:
        - Torsional rigidity: 15,000-25,000 Nm/deg (higher for performance vehicles)
        - Bending stiffness: typically 10-20% of torsional rigidity value
        - Local stiffness at suspension mounts: limit displacement to <0.5 mm at ride loads
        - Door frame stiffness: minimize frame distortion during door closing

        Panel design strategies:
        - Beads and embossments: increase panel stiffness 2-5x, shift resonance 20-40 Hz
        - Double-wall construction: floor pan with cross-car tunnels creates stiff structure
        - Ribbing patterns: use finite element analysis to place ribs at anti-nodes
        - Constrained layer damping: viscoelastic layer between two metal sheets
        - Acoustic blankets: mass-loaded vinyl or foam attached to floor, dash, roof

        Vibration transmission paths:
        - Suspension to body: rubber bushings (50-80 Shore A), tuned for compliance vs. NVH
        - Powertrain to body: 3 or 4 mounts with hydraulic isolation for idle shake
        - Exhaust to body: flexible hangers, avoid rigid contact with floor pan
        - Driveshaft to body: center bearing isolation, CV joint phasing

        Material effects on NVH:
        - Steel: good damping, high density provides mass barrier for sound
        - Aluminum: lower damping than steel, requires more aggressive damping treatment
        - Composite panels: excellent damping, difficult to achieve stiffness targets
        - Adhesive bonding: increases stiffness 10-30% vs. spot welding, improves damping

        Testing and validation:
        - Modal analysis: measure body modes with impact hammer and accelerometers
        - Transfer path analysis (TPA): quantify contribution of each path to interior noise
        - Sound intensity mapping: identify primary noise radiation surfaces
        - On-road coastdown: measure noise vs. speed on smooth/rough roads
        - Powertrain operating NVH: measure at key speeds (idle, 2000 rpm, WOT)

        Common NVH issues and root causes:
        - Roof boom at 35-40 Hz: insufficient roof cross-members or weak roof rail attachment
        - Floor drumming at 200 Hz: floor pan resonance excited by tire cavity mode
        - Door wind noise: poor seal compression from door frame flex
        - Suspension thud: inadequate bushing compliance or body mount stiffness
        - Powertrain vibration: mount tuning too stiff or broken damping elements
        """,
        key_factors=[
            "First body mode frequency (Hz)",
            "Torsional and bending stiffness",
            "Panel resonant frequency distribution",
            "Damping material coverage (%)",
            "Suspension mount isolation effectiveness",
            "Door frame stiffness and seal compression",
            "Acoustic package mass and coverage"
        ],
        primary_authority=[
            "SAE J1477 Measurement of Interior Sound Levels",
            "ISO 362 Vehicle Noise Measurement",
            "SAE J2563 Vibration Testing Methods",
            "ISO 3744 Sound Power Determination",
            "SAE J1400 Laboratory Measurement of NVH"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.NVH,
        zone=AnalysisZone.TESTING
    ),

    DoctrineBlock(
        topic="aerodynamic_body_optimization",
        keywords=["aerodynamics", "drag coefficient", "cd", "downforce", "cooling airflow", "wind tunnel"],
        conclusion_template="Aerodynamic body optimization balances conflicting objectives: minimize drag (Cd) for fuel economy, generate downforce for stability, provide adequate cooling airflow, and manage wind noise. A 0.01 reduction in Cd improves highway fuel economy by approximately 1-2%, making aerodynamics critical for efficiency and range (especially EVs).",
        reasoning_framework="""
        Aerodynamic forces on vehicle body:

        1. Drag force: Fd = 0.5 × ρ × V² × Cd × A
        - ρ = air density (1.225 kg/m³ at sea level, 15°C)
        - V = vehicle velocity (m/s)
        - Cd = coefficient of drag (dimensionless, typical 0.25-0.35 for modern cars)
        - A = frontal area (m², typically 2.0-2.5 m² for sedans)
        - At 70 mph (31.3 m/s), Cd 0.30, A 2.2 m²: Fd = 380 N (equivalent to 8% grade)

        2. Lift force: Fl = 0.5 × ρ × V² × Cl × A
        - Cl = coefficient of lift (positive = lift, negative = downforce)
        - Passenger cars: Cl = -0.05 to +0.15 (target near zero for stability)
        - Sports cars: Cl = -0.20 to -0.60 (active aero can vary with speed)
        - Front lift balance: 45-50% front, 50-55% rear for neutral handling

        Drag breakdown by source (typical sedan):
        - Skin friction (boundary layer): 10-15%
        - Form drag (pressure difference front/rear): 50-60%
        - Induced drag (lift-related vortices): 5-10%
        - Interference drag (mirrors, A-pillar, wheelwells): 15-20%
        - Internal flow drag (cooling, ventilation): 10-15%
        - Protrusions (antennas, wipers, door handles): 2-5%

        Body design strategies for low drag:

        Front end:
        - Low hood angle: reduce stagnation pressure at leading edge
        - Smooth transition from bumper to hood: eliminate separation bubble
        - Active grille shutters: close at highway speed when cooling demand is low
        - Front air dam: seal gap under bumper, direct air around vs. under vehicle
        - Wheel deflectors: prevent air entering wheelwell (high turbulence region)

        Underbody:
        - Flat floor panels: eliminate turbulence from exhaust, suspension components
        - Rear diffuser: expand flow area gradually to recover pressure, reduce base drag
        - Engine undertray: smooth airflow from front dam to cabin floor
        - Transmission tunnel fairing: reduce drag from exposed driveshaft, exhaust

        Rear end (critical for drag, accounts for 40% of total):
        - Kamm back or boat tail: truncated rear reduces wake size vs. full taper
        - Rear spoiler: generates downforce, can increase or decrease drag depending on design
        - Decklid trailing edge: sharp edge promotes flow separation at consistent location
        - Rear window angle: 25-35 degrees optimal, steeper causes separation, shallower increases length
        - Rear bumper diffuser: accelerate underbody flow to reduce base pressure deficit

        Side surfaces:
        - A-pillar shape: minimize cross-sectional area, round leading edge
        - Side mirrors: streamline shape, reduce frontal area (replace with cameras when legal)
        - Flush door handles: pop-out or retract to eliminate protrusion
        - Wheel design: aerodynamic wheels can reduce drag 0.01-0.02 Cd vs. open spoke
        - Side skirts: prevent air spilling under vehicle from wheelwell turbulence

        Cooling airflow management:
        - Grille opening size: balance cooling demand (worst case: max speed, AC on, uphill, hot day)
        - Radiator pressure drop: minimize to reduce required inlet size
        - Wheelwell exhaust: vent cooling air through wheelwell vs. under car (lower drag)
        - Engine bay sealing: prevent recirculation of hot air back through radiator
        - Active shutters: close when cooling not needed, reduce drag 0.005-0.015 Cd

        CFD and wind tunnel validation:
        - CFD (Computational Fluid Dynamics): full vehicle simulation, 10-20 million cells
        - Wind tunnel: 1:4 or 1:5 scale model, or full-scale (preferred for accuracy)
        - Correlation: CFD typically predicts Cd within 5% of wind tunnel
        - On-road coastdown: measure actual drag force, includes rolling resistance
        - Real-world drag often 0.01-0.02 higher than wind tunnel due to cooling airflow, soiling

        Aerodynamic development process:
        1. Initial shape study: parametric CFD to explore form, target Cd <0.30 for efficiency
        2. Detail optimization: mirrors, wheels, underbody, grilles
        3. Cooling integration: size grille openings, validate cooling at worst case
        4. Wind tunnel testing: measure forces, visualize flow with smoke/tufts
        5. On-road validation: coastdown testing to correlate prediction
        6. Production intent: verify clay model or final tooling matches CAD geometry

        Trade-offs and constraints:
        - Lower hood for aero vs. pedestrian impact regulations (require energy-absorbing space)
        - Aggressive front air dam vs. approach angle and snow/debris accumulation
        - Smooth underbody vs. ground clearance and service access
        - Small grille openings vs. cooling at low speed (traffic, towing)
        - Rear spoiler downforce vs. drag increase
        """,
        key_factors=[
            "Coefficient of drag (Cd)",
            "Frontal area (m²)",
            "Lift coefficient and front/rear balance",
            "Cooling airflow requirement vs. drag penalty",
            "Underbody smoothness and rear diffuser effectiveness",
            "Mirror drag contribution (2-4% of total drag)",
            "Active aero element control logic"
        ],
        primary_authority=[
            "SAE J1252 Wind Tunnel Test Procedure",
            "SAE J2263 Road Load Measurement",
            "ISO 12021 Road Vehicles - Aerodynamic Drag Measurement",
            "SAE J2071 Aerodynamic Testing of Road Vehicles",
            "Hucho - Aerodynamics of Road Vehicles (reference text)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.AERODYNAMICS,
        zone=AnalysisZone.TESTING
    ),

    DoctrineBlock(
        topic="structural_durability_and_fatigue",
        keywords=["durability", "fatigue", "crack propagation", "stress cycling", "proving ground", "mileage accumulation"],
        conclusion_framework="""
        Structural durability ensures body can withstand 150,000-200,000 mile lifetime (10-15 years) without cracks, permanent deformation, or functional degradation. Fatigue cracks typically initiate at stress concentrations (spot welds, holes, notches) and propagate under cyclic loading from road inputs, eventually leading to structural failure or water/noise leaks.

        Fatigue life prediction:
        - S-N curve (stress vs. cycles to failure) for each material grade
        - Weld fatigue life significantly lower than base material (reduction factor 3-10x)
        - Multiaxial stress requires equivalent stress calculation (von Mises)
        - Load spectrum from proving ground or customer usage data
        - Miner's rule for cumulative damage: Σ(ni/Ni) < 1.0 for infinite life

        Critical fatigue locations in body structure:
        1. Suspension attachment points: cyclic load from road inputs, 10⁷-10⁸ cycles
        2. Spot welds in high-stress areas: weld nugget edge is crack initiation site
        3. Door hinges and latches: repeated open/close cycling, 100,000+ operations
        4. Seat track and mount: occupant load cycling, crash load capability
        5. Powertrain mounts: engine vibration, 10⁸+ cycles over vehicle life
        6. Exhaust hangers: thermal cycling and vibration combined stress
        7. Tow hook and recovery points: infrequent but high magnitude loading

        Durability testing strategy:

        Proving ground testing:
        - Belgian block (cobblestone): high-amplitude vertical input, shock loads
        - Washboard (corrugated road): 10-15 Hz suspension resonance excitation
        - Potholes: single high-amplitude impact, tests peak stress capability
        - High-speed oval: sustained high-speed stability and cooling validation
        - Handling course: lateral acceleration, body torsion from cornering
        - Target: 10,000-20,000 proving ground miles = 100,000-150,000 customer miles

        4-post rig testing:
        - Hydraulic actuators at each wheel position replay road profile
        - Accelerated testing: 24/7 operation, complete 150K equivalent in 4-8 weeks
        - Load spectrum: measured from instrumented vehicle on proving ground
        - Failure mode identification: cracks, rattles, squeaks, water leaks

        Finite element analysis (FEA) for durability:
        - Static stress analysis: identify high-stress areas for reinforcement
        - Modal analysis: avoid resonance between body modes and excitation frequencies
        - Transient dynamics: simulate pothole impact, curb strike events
        - Fatigue analysis: predict crack initiation location and cycles to failure
        - Correlation: FEA stress within 15% of strain gauge measurement on prototype

        Material fatigue properties:
        - Mild steel (300 MPa): fatigue limit ~150 MPa at 10⁷ cycles
        - AHSS (600 MPa): fatigue limit ~250 MPa, but weld strength same as mild steel
        - UHSS (1500 MPa): fatigue limit ~400 MPa, sensitive to notches and surface defects
        - Aluminum 6061-T6: no true fatigue limit, requires finite-life design
        - Weld fatigue strength: 40-60% of base material, highly sensitive to weld quality

        Design for durability:
        - Generous fillet radii at stress concentrations (R ≥5 mm preferred)
        - Avoid abrupt section changes (taper thickness transitions over 50+ mm)
        - Weld placement away from peak stress locations when possible
        - Redundant load paths: structure can redistribute load if one path cracks
        - Corrosion protection: corrosion pits act as crack initiation sites, reduce fatigue life 50%+
        - Shot peening or surface rolling: induce compressive residual stress, improve fatigue life 20-40%

        Failure criteria and acceptance:
        - No cracks: zero tolerance for cracks in primary structure after durability test
        - Permanent deformation: <2 mm at critical dimensions (door opening, glass fit)
        - Functional degradation: doors must open/close, latches engage, glass seals intact
        - NVH degradation: no new squeaks, rattles, or booming after durability
        - Corrosion: no perforation or significant surface corrosion after salt spray + durability
        """,
        reasoning_framework="""See conclusion_framework for complete reasoning.""",
        key_factors=[
            "Fatigue life prediction (cycles to failure)",
            "Proving ground mileage accumulation factor",
            "Stress concentration locations and mitigation",
            "Weld quality and fatigue strength reduction",
            "Load spectrum representativeness",
            "FEA correlation to physical test",
            "Post-durability functional assessment"
        ],
        primary_authority=[
            "SAE J2749 Accelerated Exposure Test",
            "ISO 16750 Road Vehicles - Environmental Conditions",
            "SAE J1211 Recommended Practice for Proving Ground Durability",
            "ASTM E466 Force Controlled Fatigue Testing",
            "BS 7608 Code of Practice for Fatigue Design and Assessment"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.STRUCTURAL_INTEGRITY,
        zone=AnalysisZone.TESTING
    ),

    DoctrineBlock(
        topic="advanced_high_strength_steel_selection",
        keywords=["ahss", "uhss", "dual phase", "trip steel", "martensitic", "hot stamping", "tailor welded blank"],
        conclusion_template="Advanced High-Strength Steels (AHSS) enable simultaneous weight reduction and crashworthiness improvement through strategic material placement. The challenge is managing formability (AHSS is less ductile), weld strength (often lower than base material), and springback (requires compensation in die design). Material selection must balance strength targets, manufacturing feasibility, and cost.",
        reasoning_framework="""
        AHSS material classes and applications:

        1. Dual Phase (DP) steel: 300-1000 MPa
        - Microstructure: ferrite matrix with martensite islands (20-40% volume)
        - Properties: continuous yielding (no yield point), high work hardening, good energy absorption
        - Applications: bumper beams, door beams, B-pillar reinforcement (lower grades)
        - Formability: moderate, can achieve 15-25% elongation at 600 MPa
        - Weld strength: 70-80% of base material strength

        2. TRIP (Transformation-Induced Plasticity): 600-800 MPa
        - Microstructure: retained austenite transforms to martensite during deformation
        - Properties: excellent energy absorption, high work hardening exponent
        - Applications: door rings, B-pillar outer, rocker outer (Class A surface capability)
        - Formability: excellent for strength level, 25-30% elongation at 700 MPa
        - Weld strength: 65-75% of base material

        3. Complex Phase (CP): 800-1000 MPa
        - Microstructure: fine ferrite/bainite/martensite, precipitation strengthening
        - Properties: high yield strength, good edge stretch capability
        - Applications: bumper beams, seat structures, cross-members
        - Formability: moderate, 10-15% elongation at 1000 MPa
        - Weld strength: 70-80% of base material

        4. Martensitic (MS): 900-1700 MPa
        - Microstructure: primarily martensite, extremely high strength
        - Properties: very high yield and tensile strength, limited elongation
        - Applications: hot-stamped parts (A/B-pillars, door beams, roof rails)
        - Formability: poor in cold forming, hot stamping required for complex shapes
        - Weld strength: 50-70% of base material, sensitive to heat input

        5. Hot-stamped (Press-Hardened Steel): 1300-1700 MPa
        - Process: heat blank to 900-950°C, transfer to press, quench in die to form martensite
        - Properties: ultimate strength 1500 MPa typical, minimal springback
        - Applications: A/B/C pillars, door beams, roof rails, side sills (any critical safety structure)
        - Formability: excellent when hot, can form complex shapes impossible with cold forming
        - Coating: Al-Si coating prevents oxidation during heating, provides corrosion protection
        - Challenges: slow cycle time (3-5 min vs. 10-15 sec for cold stamping), expensive tooling

        6. Tailor-Welded Blanks (TWB):
        - Concept: laser weld dissimilar thickness or grades before stamping
        - Applications: door inner (thick at hinge, thin at center), B-pillar (1500 MPa at belt, 600 MPa at roof)
        - Benefits: optimized material placement, reduce weight by 5-10%, eliminate assembly welds
        - Challenges: weld line movement during forming, weld strength lower than base material

        7. Tailor-Rolled Blanks (TRB):
        - Concept: continuously vary thickness along blank length before stamping
        - Applications: longitudinal rails (thick at crush box, thin at rear), roof rails
        - Benefits: smoother thickness transition than TWB, better formability
        - Challenges: limited availability, higher material cost than uniform gauge

        Material selection decision matrix:

        For crash structures (energy absorption):
        - Front/rear rails: DP 600-800 or MS 1200 (progressive buckling required)
        - B-pillar inner: hot-stamped MS 1500 (intrusion resistance priority)
        - Door beams: hot-stamped MS 1500 or DP 1000 (space constraint, need max strength)
        - Roof rails: hot-stamped MS 1500 (roof crush performance)

        For body stiffness:
        - Tunnel reinforcement: DP 600-800 (balance stiffness and weight)
        - Rocker inner: CP 800-1000 (high bending stiffness required)
        - Shock tower: DP 600 (point load from suspension, fatigue critical)
        - Cross-members: CP 800 or DP 600 (depends on load magnitude)

        For Class A surfaces (visible exterior):
        - Door outer: TRIP 600-700 (excellent formability, no surface defects)
        - Fender: Mild steel or TRIP 600 (complex shape, Class A quality)
        - Hood outer: Mild steel or aluminum (large panel, dent resistance)
        - Roof outer: Mild steel (minimal stress, cosmetic priority)

        Manufacturing considerations:

        Formability limits:
        - Mild steel 300 MPa: can form 90-degree bends with R/t = 1.0
        - DP 600 MPa: requires R/t ≥2.0 for 90-degree bend
        - MS 1200 MPa: cold forming limited to gentle bends, hot stamping for complex shapes
        - Edge stretching: AHSS prone to edge cracking, requires burr-free laser cut edges

        Springback compensation:
        - DP and TRIP: 2-5 degrees overbend required to achieve target angle
        - MS cold formed: 5-10 degrees overbend, highly sensitive to material variation
        - Hot stamped: minimal springback (<1 degree), excellent dimensional accuracy

        Welding challenges:
        - Spot weld strength: AHSS requires higher current, longer time, larger electrodes
        - Weld count increase: 20-30% more welds needed vs. mild steel for equivalent joint strength
        - Laser welding: preferred for UHSS, full penetration welds, minimize HAZ softening
        - Adhesive bonding: increasingly used with AHSS, distributes stress, improves stiffness

        Cost considerations:
        - Mild steel baseline: $0.60-0.80/kg
        - DP 600: $0.80-1.00/kg (30% premium)
        - TRIP 700: $1.00-1.20/kg (50% premium)
        - Hot-stamped MS 1500: $1.50-2.00/kg + expensive tooling (200% premium on part cost)
        - Aluminum 6061: $2.50-3.50/kg, but 40% lower density partially offsets
        """,
        key_factors=[
            "Tensile strength (MPa) vs. formability (% elongation)",
            "Weld strength reduction factor",
            "Springback magnitude and compensation strategy",
            "Manufacturing cycle time (hot stamping 3-5 min)",
            "Material cost premium over mild steel baseline",
            "Coating system compatibility (galvanizing, Al-Si)",
            "Crashworthiness vs. weight trade-off"
        ],
        primary_authority=[
            "WorldAutoSteel AHSS Application Guidelines",
            "SAE J2745 High-Strength Steel Properties",
            "ISO 16630 Advanced High-Strength Steels",
            "ULSAB (UltraLight Steel Auto Body) Program",
            "AISI Steel Design Manual"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MATERIAL_SELECTION,
        zone=AnalysisZone.DESIGN
    ),

    DoctrineBlock(
        topic="joining_methods_comparison",
        keywords=["spot welding", "laser welding", "adhesive bonding", "riveting", "fsw", "clinching", "hem flange"],
        conclusion_template="Joining method selection affects structural stiffness, fatigue life, NVH, manufacturing cost, and repair feasibility. Modern multi-material bodies require multiple joining technologies: resistance spot welding (RSW) for steel-to-steel, laser welding for steel-to-aluminum, adhesive bonding for stiffness enhancement, and self-piercing rivets (SPR) for aluminum-to-aluminum or mixed materials.",
        reasoning_framework="""
        Resistance Spot Welding (RSW) - baseline steel joining:
        - Process: electric current (8,000-12,000 A) melts interface between two sheets
        - Weld nugget diameter: 4-8 mm (4√t where t = thinner sheet thickness in mm)
        - Joint strength: 3-6 kN per spot for mild steel, 4-8 kN for AHSS
        - Weld spacing: 25-50 mm typical (closer spacing for high loads)
        - Cycle time: 1-3 seconds per weld
        - Advantages: fast, low cost capital, proven process, easy automation
        - Disadvantages: weld fatigue life 50% of base material, stress concentration at nugget edge
        - AHSS challenges: higher current required, electrode life reduced, weld expulsion risk

        Laser Welding - precision joining:
        - Process: focused laser beam (CO2 or fiber laser) melts material, creates deep penetration weld
        - Weld width: 0.5-2 mm (much narrower than spot weld)
        - Joint strength: full penetration welds = 100% base material strength
        - Weld speed: 1-10 m/min (much faster than RSW for long seams)
        - Advantages: high strength, minimal distortion, excellent fatigue life, can weld dissimilar materials
        - Disadvantages: high capital cost ($200K-500K per cell), tight fit-up tolerance (<0.3 mm gap)
        - Applications: roof seam, door ring, tailgate hem flange, aluminum space frame nodes

        Adhesive Bonding - stiffness enhancement:
        - Process: two-part epoxy or urethane applied to flange, cured during e-coat bake (180°C)
        - Bond width: 5-20 mm depending on application
        - Joint strength: 10-30 MPa shear strength, load distributed over large area
        - Stiffness contribution: 20-40% increase in body torsional rigidity vs. spot welds alone
        - Advantages: distributes stress, excellent fatigue life, seals against water/noise, increases crash energy absorption
        - Disadvantages: requires surface preparation, cure time, difficult to rework, sensitive to contamination
        - Applications: roof to side frame, floor to rockers, hood/deck lid inner-to-outer hem
        - Common adhesives: Betamate (Dow), Terostat (Henkel), 3M Panel Bond

        Self-Piercing Rivets (SPR) - multi-material joining:
        - Process: rivet pierces top sheet, flares into bottom sheet (no pre-drilled hole)
        - Rivet diameter: 5-6 mm typical
        - Joint strength: 4-8 kN per rivet (comparable to spot weld)
        - Advantages: joins aluminum, steel, composites, no heat-affected zone, excellent fatigue life
        - Disadvantages: slower than spot welding (3-5 sec/rivet), requires access from both sides, consumable cost
        - Applications: aluminum body panels, hybrid steel-aluminum structures, closure panels
        - Rivet spacing: 30-60 mm (similar to spot weld spacing)

        Flow-Drill Screws (FDS) - single-sided fastening:
        - Process: rotating screw melts through top sheets, forms threads in bottom sheet
        - Screw diameter: 4-6 mm
        - Joint strength: 3-6 kN per screw
        - Advantages: single-sided access, removable for service, joins dissimilar materials
        - Disadvantages: slow (5-8 sec/screw), requires precise hole location, consumable cost
        - Applications: inner body structure where access is limited, service-removable panels

        Friction Stir Welding (FSW) - solid-state joining:
        - Process: rotating tool plasticizes material, translates along joint, creates solid-state weld
        - Weld width: 8-15 mm
        - Joint strength: 80-95% base material strength (better than fusion welding for aluminum)
        - Weld speed: 0.5-2 m/min
        - Advantages: no melting, excellent properties for aluminum, minimal distortion
        - Disadvantages: slow, requires backing support, leaves exit hole, high tool wear for steel
        - Applications: aluminum space frame rails, battery enclosures, EV skateboard platforms

        Clinching - mechanical interlock:
        - Process: punch and die deform sheets to create mechanical interlock
        - Joint diameter: 5-8 mm
        - Joint strength: 2-4 kN (lower than welding or riveting)
        - Advantages: no consumables, fast (1-2 sec), joins dissimilar materials, no heat
        - Disadvantages: requires access from both sides, lower strength, potential stress concentration
        - Applications: low-load applications, non-structural panels, aluminum assemblies

        Hem Flange Joining - closure panels:
        - Process: outer panel folded over inner panel edge, creating 180-degree bend
        - Hem types: flat hem (180° fold), rope hem (rolled edge)
        - Adhesive application: applied before hemming for sealing and stiffness
        - Advantages: clean appearance, seals edge, distributes stress
        - Disadvantages: requires precise edge geometry, difficult to rework, prone to springback
        - Applications: hood, decklid, door inner-to-outer, liftgate

        Joining method selection matrix:

        Steel-to-steel (same thickness):
        - RSW: cost-effective baseline, 30-60 mm spacing
        - Adhesive + RSW: premium stiffness, 60-100 mm RSW spacing (adhesive carries load between welds)
        - Laser weld: long seams (roof, rocker), high-strength requirement

        Steel-to-steel (different thickness, >2:1 ratio):
        - RSW: requires special electrodes, risk of burn-through on thin sheet
        - Laser weld: preferred for large thickness mismatch
        - SPR: alternative if laser not available

        Aluminum-to-aluminum:
        - SPR: primary method, 30-50 mm spacing
        - Adhesive + SPR: premium stiffness
        - Laser weld: space frame nodes, extruded structures
        - FSW: thick sections (battery trays), long straight welds
        - RSW: possible but requires special equipment, electrode life short

        Steel-to-aluminum (multi-material):
        - SPR: most common, rivet pierces aluminum into steel
        - Flow-drill screws: alternative for thicker sections
        - Adhesive bonding: can supplement mechanical fasteners
        - Laser weld: possible with filler wire, complex process
        - RSW: not recommended (brittle intermetallic compounds form)

        Closure panels (inner-to-outer):
        - Hem flange + adhesive: standard for doors, hood, decklid
        - Laser weld + adhesive: alternative for aluminum closures
        - Roller hem: automated process for flat hem
        - Die hem: higher quality, requires dedicated tooling

        Structural performance comparison:
        - Static strength: laser weld > adhesive > SPR ≈ RSW > clinching
        - Fatigue life: adhesive > laser weld > SPR > RSW > clinching
        - Stiffness contribution: adhesive >> laser weld > RSW > SPR > clinching
        - NVH performance: adhesive (excellent damping) > laser weld > SPR > RSW
        - Crash energy absorption: adhesive + RSW > RSW alone (distributed load)

        Cost comparison (relative, RSW = 1.0):
        - RSW: 1.0 (baseline)
        - Adhesive: 1.3-1.5 (material + process)
        - SPR: 1.5-2.0 (equipment + consumables)
        - Laser weld: 2.0-3.0 (capital intensive)
        - FSW: 2.5-4.0 (slow, high tool cost)
        - FDS: 2.0-2.5 (consumables)
        """,
        key_factors=[
            "Joint strength (kN per fastener)",
            "Fatigue life (cycles to failure)",
            "Stiffness contribution to body structure",
            "Manufacturing cycle time (sec per joint)",
            "Capital and consumable cost",
            "Material compatibility (steel, aluminum, composite)",
            "Access requirements (single-sided vs. both sides)"
        ],
        primary_authority=[
            "AWS D8.1 Automotive Welding Specification",
            "SAE J1523 Classification of Automotive Adhesives",
            "DVS 2935 Self-Piercing Riveting Guidelines",
            "ISO 14272 Resistance Spot Welding",
            "ASTM D1002 Shear Strength of Adhesive Bonds"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.JOINING_METHODS,
        zone=AnalysisZone.DESIGN
    ),

    DoctrineBlock(
        topic="body_structure_weight_optimization",
        keywords=["lightweight", "mass reduction", "weight target", "specific stiffness", "material substitution"],
        conclusion_template="Weight reduction improves fuel economy (10% mass reduction = 6-8% fuel economy gain), acceleration, handling, and brake performance. The challenge is achieving mass targets without compromising crash safety, stiffness, NVH, or durability. Effective lightweighting combines material substitution (AHSS, aluminum, composites), topology optimization, and packaging efficiency.",
        reasoning_framework="""
        Weight reduction strategies and impact:

        Fuel economy benefit:
        - ICE vehicles: 10% mass reduction → 6-8% fuel economy improvement
        - EVs: 10% mass reduction → 8-10% range improvement (regenerative braking recovers some energy)
        - Compounding effect: lighter vehicle → smaller engine/battery → lighter powertrain → further weight reduction

        Performance impact:
        - Acceleration: 10% lighter → 0-60 mph time reduced by ~0.5 sec (for 8-sec baseline)
        - Braking: 10% lighter → 60-0 mph distance reduced by ~10 feet (120 ft baseline)
        - Handling: lower polar moment of inertia, improved transient response
        - Ride quality: lighter unsprung mass (wheels, suspension) improves ride isolation

        Material substitution strategies:

        1. Steel grade optimization:
        - Replace mild steel (300 MPa) with AHSS (600-1000 MPa) in non-Class A panels
        - Gauge reduction: 1.5 mm mild steel → 1.0 mm DP600 for equivalent strength
        - Weight savings: 30-35% per part, body structure 5-10% overall
        - Cost: +10-20% material cost, offset by reduced forming/assembly cost

        2. Aluminum substitution:
        - Density advantage: aluminum 2.7 g/cm³ vs. steel 7.8 g/cm³ (65% lighter per volume)
        - Stiffness penalty: aluminum modulus 70 GPa vs. steel 210 GPa (need thicker gauge for equal stiffness)
        - Net weight savings: 40-50% vs. steel for equivalent stiffness (1.8 mm Al vs. 1.0 mm steel)
        - Applications: hood, decklid, fenders (closures), space frame (Audi A8, F-150 body)
        - Cost: 2-3x steel material cost, offset by reduced fuel consumption over vehicle life
        - Challenges: higher forming cost, requires different joining methods (SPR, laser, FSW)

        3. Composites (carbon fiber, glass fiber):
        - Density: CFRP 1.6 g/cm³, GFRP 1.8 g/cm³ (50-60% lighter than aluminum per volume)
        - Stiffness: CFRP modulus 70-180 GPa (fiber orientation dependent)
        - Weight savings: 50-60% vs. steel, 20-30% vs. aluminum for equivalent structure
        - Applications: hood, roof, liftgate (Class A surface), floor pan (low-volume sports cars)
        - Cost: 10-50x steel depending on manufacturing process (hand layup vs. compression molding)
        - Challenges: long cycle time (5-30 min), difficult repair, energy-intensive manufacturing
        - Volume feasibility: viable for <50K units/year, mass market requires faster processes (HP-RTM)

        4. Magnesium:
        - Density: 1.8 g/cm³ (75% lighter than steel, 35% lighter than aluminum)
        - Applications: instrument panel beam, seat frames, liftgate inner
        - Weight savings: 25-35% vs. aluminum for equivalent part
        - Challenges: corrosion when in contact with steel/aluminum, flammability during machining, higher cost

        Topology optimization (design for minimum mass):
        - FEA-based optimization: remove material from low-stress regions
        - Constraints: manufacturing (stamping draw depth), package space, attachment points
        - Result: organic shapes with material only in load paths
        - Applications: shock towers, cross-members, seat frames
        - Weight savings: 15-30% vs. traditional design for same stiffness
        - Implementation: often requires casting or additive manufacturing for complex shapes

        Packaging efficiency:
        - Reduce hard point spacing: shorter wheelbase/track for same interior volume
        - Minimize overhang: front/rear overhang adds mass without interior benefit
        - Optimize body section: tall narrow body more efficient than wide low body for torsional stiffness
        - Monocoque vs. body-on-frame: monocoque 20-30% lighter for same rigidity

        Body structure weight breakdown (typical mid-size sedan, 1500 kg curb weight):
        - BIW (body-in-white): 250-320 kg (17-21% of curb weight)
        - Closures (doors, hood, decklid): 80-110 kg (5-7%)
        - Glazing (windows): 40-50 kg (3%)
        - Interior trim and seats: 100-130 kg (7-9%)
        - Powertrain: 250-350 kg (ICE) or 400-600 kg (EV with battery)
        - Chassis (suspension, brakes, wheels, tires): 200-280 kg (13-19%)
        - Electrical/electronics: 60-80 kg (4-5%)
        - Fluids (fuel, coolant, oil): 60-80 kg (4-5%)

        BIW weight reduction targets by component:
        - Floor pan: 60-80 kg → reduce to 45-60 kg (25% reduction via AHSS, topology optimization)
        - Side frames (left/right): 40-55 kg → reduce to 30-42 kg (25% via AHSS, aluminum rails)
        - Front structure: 30-45 kg → reduce to 25-35 kg (20% via aluminum crash boxes)
        - Roof frame: 25-35 kg → reduce to 18-25 kg (30% via aluminum roof rails, carbon roof panel)
        - Rear structure: 20-30 kg → reduce to 15-22 kg (25% via AHSS, aluminum liftgate)

        Trade-offs and constraints:
        - Crash performance: cannot reduce mass in primary load paths (front rails, B-pillar)
        - Stiffness: lighter structure requires better material/geometry optimization to maintain rigidity
        - NVH: lighter panels may have lower resonant frequencies (more drumming), require damping
        - Durability: thinner gauge materials more susceptible to fatigue, corrosion perforation
        - Cost: lightweight materials and processes typically more expensive, need lifecycle cost analysis
        - Manufacturing: changing materials requires new tooling, process validation, supply chain

        Lightweight body examples:
        - Audi A8 (2018): all-aluminum space frame, 282 kg BIW (40% lighter than steel equivalent)
        - BMW 7 Series (2016): carbon core (CFRP roof, pillars), 190 kg mass reduction vs. previous generation
        - Ford F-150 (2015): aluminum cab and bed, 320 kg lighter than steel predecessor
        - Tesla Model 3: aluminum front/rear castings, steel body center (cost-optimized multi-material)
        - Chevrolet Corvette C8: aluminum frame, carbon fiber floors/fenders, 145 kg body weight
        """,
        key_factors=[
            "Target body weight (kg) vs. vehicle class",
            "Material density and specific stiffness (stiffness/weight)",
            "Manufacturing feasibility and cost",
            "Crash performance maintenance with reduced mass",
            "Stiffness target achievement (Nm/deg torsional rigidity)",
            "NVH impact from lighter panels",
            "Lifecycle cost vs. fuel savings"
        ],
        primary_authority=[
            "SAE J1100 Motor Vehicle Dimensions (mass categories)",
            "ULSAB (UltraLight Steel Auto Body) Study",
            "Aluminum Association Automotive Manual",
            "WorldAutoSteel Future Steel Vehicle Program",
            "ISO 14040 Life Cycle Assessment"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.WEIGHT_OPTIMIZATION,
        zone=AnalysisZone.DESIGN
    )
]


# ============================================================================
# TIE-20 CORE ENGINE
# ============================================================================

class AUTO12BodyStructureEngine:
    """Body structure analysis engine with automotive engineering expertise"""

    def __init__(self):
        self.version = "1.0.0"
        self.port = 9322
        self.start_time = datetime.utcnow()
        self.query_count = 0
        self.total_response_time_ms = 0.0
        self.cache_hits = 0
        self.cache_misses = 0

        # Telemetry
        self.category_distribution = Counter()
        self.mode_usage = Counter()
        self.zone_distribution = Counter()

        # Audit trail
        self.audit_log_path = Path(__file__).parent / "audit_trail.jsonl"

        logger.info(f"AUTO12 Body Structure Engine v{self.version} initialized on port {self.port}")

    def three_layer_response(self, query: str, mode: ResponseMode, zone: Optional[AnalysisZone]) -> Tuple[str, List[str], ConfidenceLevel, List[IssueCategory]]:
        """
        TIE Component 1: Three-layer response (cache → semantic → deep)
        """
        start = datetime.utcnow()

        # Layer 1: Doctrine cache (fast path, 0-50ms)
        triggered_doctrines = []
        query_lower = query.lower()

        for doctrine in DOCTRINE_CACHE:
            if any(kw in query_lower for kw in doctrine.keywords):
                triggered_doctrines.append(doctrine.topic)

        if triggered_doctrines:
            self.cache_hits += 1
            # Use first matching doctrine for response
            primary_doctrine = next(d for d in DOCTRINE_CACHE if d.topic == triggered_doctrines[0])

            if mode == ResponseMode.FAST:
                answer = primary_doctrine.conclusion_template
            elif mode == ResponseMode.DEFENSE:
                answer = f"{primary_doctrine.conclusion_template}\n\nReasoning:\n{primary_doctrine.reasoning_framework[:800]}..."
            else:  # MEMO
                answer = f"{primary_doctrine.conclusion_template}\n\n{primary_doctrine.reasoning_framework}\n\nKey Factors:\n" + "\n".join(f"- {kf}" for kf in primary_doctrine.key_factors)

            categories = [primary_doctrine.category]
            confidence = primary_doctrine.confidence

        else:
            # Layer 2: Semantic search (fallback, 50-200ms)
            self.cache_misses += 1
            answer = self._semantic_search_fallback(query, mode)
            categories = [IssueCategory.BIW_DESIGN]  # Default category
            confidence = ConfidenceLevel.DISCLOSURE
            triggered_doctrines = ["semantic_fallback"]

        elapsed = (datetime.utcnow() - start).total_seconds() * 1000
        logger.info(f"Three-layer response: {elapsed:.1f}ms, cache_hit={len(triggered_doctrines) > 0}")

        return answer, triggered_doctrines, confidence, categories

    def _semantic_search_fallback(self, query: str, mode: ResponseMode) -> str:
        """Layer 2: Semantic search when cache misses"""
        # Simple keyword-based fallback
        keywords_found = []
        for doctrine in DOCTRINE_CACHE:
            for kw in doctrine.keywords:
                if kw in query.lower():
                    keywords_found.append(doctrine.topic)
                    break

        if keywords_found:
            topics = ", ".join(keywords_found[:3])
            return f"Query relates to: {topics}. Recommended analysis: review doctrine cache entries for detailed guidance on body structure design, crash performance, and material selection. For comprehensive assessment, specify vehicle class, target metrics (weight, stiffness, crash ratings), and design constraints."

        return "Query requires domain-specific context. Body structure analysis encompasses: BIW design (rigidity, weight), crash structures (frontal, side, roof), corrosion protection, NVH, aerodynamics, and structural integrity. Please specify: vehicle type, analysis objective (design, testing, evaluation), and technical requirements."

    def multi_doctrine_decomposition(self, query: str) -> Dict[str, Any]:
        """
        TIE Component 19: Break complex query into sub-issues
        """
        categories_involved = set()
        doctrines_applicable = []

        for doctrine in DOCTRINE_CACHE:
            if any(kw in query.lower() for kw in doctrine.keywords):
                categories_involved.add(doctrine.category)
                doctrines_applicable.append(doctrine.topic)

        return {
            "categories": list(categories_involved),
            "doctrines": doctrines_applicable,
            "complexity": len(categories_involved)
        }

    def confidence_stratification(self, categories: List[IssueCategory], triggered_doctrines: List[str]) -> ConfidenceLevel:
        """
        TIE Component 5: Stratify confidence based on doctrine coverage
        """
        if len(triggered_doctrines) >= 3:
            return ConfidenceLevel.DEFENSIBLE
        elif len(triggered_doctrines) == 2:
            return ConfidenceLevel.AGGRESSIVE
        elif len(triggered_doctrines) == 1:
            return ConfidenceLevel.DISCLOSURE
        else:
            return ConfidenceLevel.HIGH_RISK

    def fact_fragility_scoring(self, answer: str, doctrines: List[str]) -> float:
        """
        TIE Component 14: Score answer reliability
        """
        # More doctrines = more robust answer
        doctrine_score = min(len(doctrines) / 5.0, 1.0)

        # Check for quantitative data (numbers, units)
        quantitative_markers = len(re.findall(r'\d+\.?\d*\s*(MPa|mm|kg|kN|Hz|Nm)', answer))
        quant_score = min(quantitative_markers / 10.0, 1.0)

        # Authority citations
        citation_score = 0.8 if any(d in answer for d in ["SAE", "ISO", "FMVSS", "ASTM"]) else 0.3

        fragility = 1.0 - (doctrine_score * 0.4 + quant_score * 0.3 + citation_score * 0.3)
        return round(fragility, 2)

    def determinism_hash_sha256(self, query: str, answer: str, mode: ResponseMode) -> str:
        """
        TIE Component 16: Generate deterministic hash for reproducibility
        """
        content = f"{query}|{answer}|{mode.value}|{self.version}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def audit_trail_jsonl(self, request: QueryRequest, response: QueryResponse):
        """
        TIE Component 15: Append-only audit log
        """
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": request.query,
            "mode": request.mode.value,
            "zone": request.zone.value if request.zone else None,
            "doctrines_triggered": response.doctrines_triggered,
            "confidence": response.confidence.value,
            "response_time_ms": response.response_time_ms,
            "hash": response.determinism_hash
        }

        with open(self.audit_log_path, "a") as f:
            f.write(json.dumps(audit_entry) + "\n")

    def metrics_collector(self) -> Dict[str, Any]:
        """
        TIE Component 11: Collect performance metrics
        """
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        avg_response = self.total_response_time_ms / max(self.query_count, 1)
        cache_rate = self.cache_hits / max(self.cache_hits + self.cache_misses, 1)

        return {
            "uptime_seconds": uptime,
            "total_queries": self.query_count,
            "avg_response_ms": round(avg_response, 2),
            "cache_hit_rate": round(cache_rate, 2),
            "category_distribution": dict(self.category_distribution),
            "mode_usage": dict(self.mode_usage)
        }

    async def process_query(self, request: QueryRequest) -> QueryResponse:
        """Main query processing with all TIE components"""
        start = datetime.utcnow()

        # Multi-doctrine decomposition
        decomposition = self.multi_doctrine_decomposition(request.query)

        # Three-layer response
        answer, doctrines, confidence, categories = self.three_layer_response(
            request.query, request.mode, request.zone
        )

        # Confidence stratification
        final_confidence = self.confidence_stratification(categories, doctrines)

        # Fact fragility scoring
        fragility = self.fact_fragility_scoring(answer, doctrines)

        # Calculate response time
        elapsed_ms = (datetime.utcnow() - start).total_seconds() * 1000

        # Determinism hash
        det_hash = self.determinism_hash_sha256(request.query, answer, request.mode)

        # Update metrics
        self.query_count += 1
        self.total_response_time_ms += elapsed_ms
        self.mode_usage[request.mode.value] += 1
        for cat in categories:
            self.category_distribution[cat.value] += 1

        response = QueryResponse(
            query=request.query,
            mode=request.mode,
            answer=answer,
            confidence=final_confidence,
            categories=categories,
            doctrines_triggered=doctrines,
            response_time_ms=round(elapsed_ms, 2),
            determinism_hash=det_hash,
            zone=request.zone,
            fragility_score=fragility
        )

        # Audit trail
        self.audit_trail_jsonl(request, response)

        logger.info(f"Query processed: {elapsed_ms:.1f}ms, doctrines={len(doctrines)}, confidence={final_confidence.value}")

        return response


# ============================================================================
# FASTAPI SERVER
# ============================================================================

app = FastAPI(title="AUTO12 Body Structure Analysis Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = AUTO12BodyStructureEngine()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """TIE Component 12: Health endpoint"""
    metrics = engine.metrics_collector()

    return HealthResponse(
        status="healthy",
        version=engine.version,
        port=engine.port,
        doctrine_count=len(DOCTRINE_CACHE),
        categories=len(IssueCategory),
        uptime_seconds=metrics["uptime_seconds"],
        total_queries=metrics["total_queries"],
        avg_response_ms=metrics["avg_response_ms"],
        cache_hit_rate=metrics["cache_hit_rate"]
    )


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with TIE-20 intelligence"""
    try:
        response = await engine.process_query(request)
        return response
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "count": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords[:5],
                "zone": d.zone.value
            }
            for d in DOCTRINE_CACHE
        ]
    }


@app.get("/categories")
async def list_categories():
    """List all issue categories"""
    return {
        "categories": [cat.value for cat in IssueCategory]
    }


@app.get("/metrics")
async def get_metrics():
    """TIE Component 11: Detailed metrics"""
    return engine.metrics_collector()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting AUTO12 Body Structure Analysis Engine v{engine.version}")
    logger.info(f"Doctrine cache: {len(DOCTRINE_CACHE)} blocks loaded")
    logger.info(f"Categories: {len(IssueCategory)}")
    logger.info(f"Listening on port {engine.port}")

    uvicorn.run(app, host="0.0.0.0", port=engine.port, log_level="info")
