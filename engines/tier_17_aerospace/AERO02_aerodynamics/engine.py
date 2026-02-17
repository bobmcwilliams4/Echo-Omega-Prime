"""
AERO02 - Aerodynamics & Flight Mechanics Intelligence Engine
TIE Gold Standard - Real Domain Expertise

Port: 9072
Covers: Lift generation, drag analysis, airfoil design, boundary layers, stall characteristics,
        high-lift devices, wing planform, compressibility, supersonic aerodynamics, stability,
        performance, propeller/rotary wing, testing, CFD, ground effect, atmospheric effects
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
from dataclasses import dataclass, field, asdict
from collections import defaultdict

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

ENGINE_ID = "AERO02"
ENGINE_NAME = "Aerodynamics & Flight Mechanics Intelligence Engine"
VERSION = "1.0.0"
PORT = 9072

logger.add(
    f"aero02_engine_{datetime.now().strftime('%Y%m%d')}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)


# ═══════════════════════════════════════════════════════════════════════════
# ENUMS & DATA CLASSES
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


class IssueCategory(str, Enum):
    LIFT_GENERATION = "LIFT_GENERATION"
    DRAG_ANALYSIS = "DRAG_ANALYSIS"
    AIRFOIL_DESIGN = "AIRFOIL_DESIGN"
    BOUNDARY_LAYER = "BOUNDARY_LAYER"
    STALL_CHARACTERISTICS = "STALL_CHARACTERISTICS"
    HIGH_LIFT_DEVICES = "HIGH_LIFT_DEVICES"
    WING_PLANFORM = "WING_PLANFORM"
    COMPRESSIBILITY = "COMPRESSIBILITY"
    SUPERSONIC_AERO = "SUPERSONIC_AERO"
    STABILITY_CONTROL = "STABILITY_CONTROL"
    AIRCRAFT_PERFORMANCE = "AIRCRAFT_PERFORMANCE"
    PROPELLER_AERO = "PROPELLER_AERO"
    ROTARY_WING = "ROTARY_WING"
    TESTING_CFD = "TESTING_CFD"
    GROUND_EFFECT = "GROUND_EFFECT"
    ATMOSPHERIC_EFFECTS = "ATMOSPHERIC_EFFECTS"


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
    controlling_precedent: List[str]
    category: IssueCategory
    triggered_count: int = 0


@dataclass
class TelemetryRecord:
    timestamp: str
    query: str
    mode: ResponseMode
    categories: List[IssueCategory]
    doctrines_triggered: List[str]
    cache_hit: bool
    latency_ms: float
    confidence: ConfidenceLevel
    response_length: int


# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ REAL AERODYNAMICS EXPERTISE BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Bernoulli vs Circulation Theory of Lift",
        keywords=["bernoulli", "circulation", "kutta-joukowski", "lift generation", "vorticity"],
        conclusion_template=[
            "Lift generation is most accurately explained by circulation theory (Kutta-Joukowski theorem) which states L = ρVΓ.",
            "Bernoulli's equation describes pressure distribution but does not explain why circulation exists.",
            "The starting vortex at takeoff establishes bound circulation around the airfoil per Kelvin's theorem."
        ],
        reasoning_framework="""
        1. BERNOULLI LIMITATION: Bernoulli's equation (p + ½ρV² + ρgh = constant) describes pressure-velocity relationship
           but cannot predict the flow pattern around an airfoil. It describes consequences, not causes.

        2. CIRCULATION THEORY: Per Kutta-Joukowski theorem, lift per unit span L' = ρ∞V∞Γ, where Γ is circulation.
           This is exact for inviscid 2D flow and closely approximates real 3D flow.

        3. KUTTA CONDITION: Flow leaves the trailing edge smoothly (no infinite velocity). This boundary condition
           uniquely determines the circulation magnitude for a given airfoil at a given angle of attack.

        4. STARTING VORTEX: When airfoil accelerates, Kelvin's circulation theorem (DΓ/Dt = 0 for inviscid flow)
           requires a starting vortex shed downstream, equal and opposite to bound circulation.

        5. PHYSICAL MECHANISM: Circulation bends streamlines. Curved streamlines require centripetal acceleration,
           which manifests as pressure gradients. Net pressure difference = lift.

        6. PRANDTL LIFTING-LINE: Extends 2D theory to finite wings. Wing produces trailing vortex sheet,
           inducing downwash, causing induced drag and reducing effective angle of attack.
        """,
        key_factors=[
            "Circulation magnitude Γ determined by Kutta condition at trailing edge",
            "Vorticity generation at sharp trailing edge due to viscosity",
            "Conservation of circulation (Kelvin's theorem) in inviscid flow",
            "Downwash from trailing vortex system on finite wings",
            "Velocity field around airfoil is superposition of freestream and vortex",
            "Pressure distribution integrates to net lift force perpendicular to freestream"
        ],
        primary_authority=[
            "Anderson, Fundamentals of Aerodynamics (6th ed.), McGraw-Hill, 2017",
            "Kuethe & Chow, Foundations of Aerodynamics (5th ed.), Wiley, 1998",
            "Prandtl, Applications of Modern Hydrodynamics to Aeronautics, NACA Report 116, 1921"
        ],
        burden_holder="Designer must select appropriate theory for analysis depth",
        adversary_position="Bernoulli equation alone is sufficient for basic lift explanation",
        counter_arguments=[
            "Bernoulli describes pressure field but not flow pattern - incomplete",
            "Equal transit time theory is false - upper surface flow is faster but not due to equal transit",
            "Circulation theory quantitatively predicts lift coefficient: CL = 2πα for thin airfoil",
            "Experimental validation: measured circulation matches Kutta-Joukowski prediction",
            "CFD simulations solving Navier-Stokes confirm circulation-based lift"
        ],
        resolution_strategy="Use circulation theory for rigorous analysis; Bernoulli for qualitative pressure discussion",
        entity_scope="All fixed-wing aircraft, helicopter rotors in forward flight",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Circulation theory is established science with 100+ years validation",
        controlling_precedent=[
            "Kutta-Joukowski theorem (1906)",
            "Prandtl lifting-line theory (1918-1921)",
            "Lanchester's circulation theory (1907)"
        ],
        category=IssueCategory.LIFT_GENERATION
    ),

    DoctrineBlock(
        topic="Drag Decomposition: Parasitic, Induced, Wave",
        keywords=["parasitic drag", "induced drag", "wave drag", "drag polar", "CDi"],
        conclusion_template=[
            "Total drag is sum of parasitic (CD0), induced (CDi = CL²/πeAR), and wave (above Mcrit).",
            "Parasitic drag is Reynolds-dependent; induced drag is lift-dependent; wave drag is Mach-dependent.",
            "Minimum drag occurs at (L/D)max, typically at CL = sqrt(CD0 × πeAR)."
        ],
        reasoning_framework="""
        1. PARASITIC DRAG (CD0): Skin friction + form drag + interference drag.
           - Skin friction: dominant on streamlined bodies, scales with wetted area and Re
           - Form drag: pressure drag from flow separation, large on bluff bodies
           - Interference drag: flow interaction between components (wing-fuselage junction)

        2. INDUCED DRAG (CDi): Fundamental consequence of finite wing generating lift.
           CDi = CL² / (π × e × AR), where e = span efficiency factor (0.7-0.95), AR = aspect ratio.
           Physical cause: trailing vortex system induces downwash, tilts local lift vector aft.

        3. WAVE DRAG (CDw): Appears when local Mach > 1.0 (shock waves form).
           Drag divergence at Mcrit (critical Mach number). Shock strength increases with M∞.
           Supersonic: CDw proportional to thickness ratio, volume distribution per area rule.

        4. DRAG POLAR: CD = CD0 + K×CL², where K = 1/(πeAR) for subsonic.
           Parabolic in incompressible flow. Non-parabolic with compressibility, separation.

        5. MINIMUM DRAG: Occurs at CL for (L/D)max. For parabolic polar: CL,opt = sqrt(CD0/K).
           Cruise condition for maximum range (propeller) or endurance (jet at lower CL).

        6. COMPRESSIBILITY CORRECTION: Prandtl-Glauert in subsonic (CD increases with M).
           Transonic: drag rise curve, empirical methods. Supersonic: wave drag dominates.
        """,
        key_factors=[
            "Aspect ratio AR: higher AR reduces induced drag (CDi ∝ 1/AR)",
            "Reynolds number Re: affects transition, separation, skin friction",
            "Mach number M: compressibility effects, wave drag above Mcrit",
            "Surface roughness: increases skin friction, trips boundary layer",
            "Wingtip devices (winglets): increase effective AR, reduce CDi by 5-10%",
            "Laminar flow: much lower Cf than turbulent (1/10), hard to maintain"
        ],
        primary_authority=[
            "Hoerner, Fluid-Dynamic Drag, Hoerner Fluid Dynamics, 1965",
            "Anderson, Aircraft Performance and Design, McGraw-Hill, 1999",
            "Shevell, Fundamentals of Flight (2nd ed.), Prentice Hall, 1989"
        ],
        burden_holder="Designer must minimize total drag for mission efficiency",
        adversary_position="Drag reduction is secondary to structural weight, cost constraints",
        counter_arguments=[
            "Fuel cost over aircraft lifetime far exceeds incremental manufacturing cost",
            "1% drag reduction = 0.75% fuel savings per Airbus/Boeing studies",
            "Induced drag dominates at low speed (takeoff/landing), parasitic at cruise",
            "Wave drag penalty severe - transonic drag rise can double total drag",
            "Drag cleanup (seal gaps, smooth surfaces) is low-cost, high-return"
        ],
        resolution_strategy="Optimize AR for mission (high for endurance, moderate for speed), laminar flow where possible, supercritical airfoils for transonic cruise",
        entity_scope="All aircraft, missiles, automotive aerodynamics",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Drag theory validated by 70+ years wind tunnel and flight test",
        controlling_precedent=[
            "Prandtl induced drag theory (1918)",
            "Von Karman wave drag theory (1935)",
            "NASA supercritical airfoil research (1960s-70s)"
        ],
        category=IssueCategory.DRAG_ANALYSIS
    ),

    DoctrineBlock(
        topic="NACA Airfoil Designation and Characteristics",
        keywords=["NACA", "4-digit", "5-digit", "6-series", "camber", "thickness"],
        conclusion_template=[
            "NACA 4-digit: MPXX where M=max camber (% chord), P=position (tenths chord), XX=thickness (%).",
            "NACA 6-series designed for laminar flow, low drag at design CL, used on high-speed aircraft.",
            "Thickness ratio affects CLmax (thicker = higher), Mcrit (thinner = higher), structural depth."
        ],
        reasoning_framework="""
        1. NACA 4-DIGIT (e.g., NACA 2412):
           - First digit (2): maximum camber = 2% chord
           - Second digit (4): location of max camber at 40% chord from leading edge
           - Last two digits (12): maximum thickness = 12% chord
           - Symmetric if first two digits are 00 (e.g., NACA 0012)

        2. NACA 5-DIGIT (e.g., NACA 23012):
           - Designed for higher CL. First digit × 3/2 = design CL in tenths (2 → CL = 0.3)
           - Second/third digits: position of max camber (30 code = 15% chord, 20 code = 10%)
           - Last two digits: thickness ratio

        3. NACA 6-SERIES (e.g., NACA 65₂-215):
           - Designed for laminar flow. "6" = series, "5" = min pressure at 50% chord.
           - Subscript (2): CL range for low drag = ±0.2 from design CL
           - Next digit (2): design CL in tenths = 0.2
           - Last two (15): thickness = 15%
           - Laminar bucket: range of CL with low CD, sensitive to surface roughness

        4. THICKNESS EFFECTS:
           - Thin airfoils (6-9%): higher Mcrit, lower CLmax, less structural depth
           - Thick airfoils (15-21%): higher CLmax, lower Mcrit, more fuel volume, stronger spar
           - Compressibility: Mcrit decreases with thickness. Supercritical airfoils manage Mcrit.

        5. CAMBER EFFECTS:
           - Positive camber shifts CL curve upward (lift at α=0), increases CLmax
           - Zero-lift angle α₀ negative for cambered airfoils
           - Reflex camber (trailing edge curves up): stabilizes flying wings, reduces Cm

        6. REYNOLDS NUMBER EFFECTS:
           - Low Re (< 500k): laminar separation bubble, early stall, low CLmax
           - High Re (> 3M): thin boundary layer, higher CLmax, attached flow
           - Roughness: trips BL to turbulent, reduces CLmax but can improve low-Re performance
        """,
        key_factors=[
            "Thickness-to-chord ratio t/c: 6% (transonic fighters) to 18% (GA aircraft)",
            "Camber: 0% (symmetric, aerobatic) to 4% (high-lift GA)",
            "Leading edge radius: affects stall behavior (sharp = abrupt, round = gentle)",
            "Trailing edge angle: affects zero-lift pitching moment and Kutta condition",
            "Design CL: 6-series optimized for specific CL, off-design penalty",
            "Surface finish: critical for laminar flow (< 0.0002 inch roughness)"
        ],
        primary_authority=[
            "Abbott & Von Doenhoff, Theory of Wing Sections, Dover, 1959",
            "Jacobs & Sherman, Airfoil Section Characteristics, NACA Report 460, 1937",
            "Selig, Airfoils at Low Speeds, SoarTech Publications, 1989"
        ],
        burden_holder="Designer selects airfoil balancing CLmax, Mcrit, L/D, structural depth",
        adversary_position="Modern supercritical and computational airfoils obsolete NACA series",
        counter_arguments=[
            "NACA airfoils remain baseline for GA, UAV, rotor blades due to extensive data",
            "6-series still used on gliders, business jets for laminar flow benefit",
            "Modification of NACA sections (supercritical derivative) common practice",
            "Wind tunnel database for NACA airfoils unmatched in Re range coverage",
            "Simple geometry aids manufacturing, inspection, maintenance"
        ],
        resolution_strategy="Use NACA for preliminary design and teaching; CFD-optimized for cutting-edge performance",
        entity_scope="General aviation, UAVs, wind turbines, propellers, helicopter rotors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="NACA airfoil theory and data validated across 10 million flight hours",
        controlling_precedent=[
            "NACA Technical Reports (1930s-1950s)",
            "Abbott & Von Doenhoff compilation (1949)",
            "Subsequent NASA/university extensions"
        ],
        category=IssueCategory.AIRFOIL_DESIGN
    ),

    DoctrineBlock(
        topic="Boundary Layer Transition and Turbulence",
        keywords=["laminar", "turbulent", "transition", "Reynolds number", "critical Re"],
        conclusion_template=[
            "Laminar-to-turbulent transition occurs at Recrit ≈ 500k for smooth flat plate, lower with roughness/pressure gradient.",
            "Turbulent boundary layer is thicker, higher skin friction (5-10× laminar), but more resistant to separation.",
            "Natural laminar flow (NLF) maintains laminar BL to 60-70% chord, reducing drag 15-25%."
        ],
        reasoning_framework="""
        1. LAMINAR BOUNDARY LAYER:
           - Smooth, layered flow. Velocity profile: u/U = f(y/δ), parabolic shape.
           - Skin friction: Cf = 1.328/sqrt(Re_x) for flat plate (Blasius solution)
           - Thin: δ/x = 5/sqrt(Re_x). Low drag but prone to separation under adverse pressure gradient.

        2. TURBULENT BOUNDARY LAYER:
           - Chaotic, mixing flow. Velocity profile: u/U = (y/δ)^(1/7) power law approximation.
           - Skin friction: Cf = 0.074/Re_x^(1/5) (smooth flat plate, empirical)
           - Thick: δ/x ≈ 0.37/Re_x^(1/5). Higher drag but energizes flow, delays separation.

        3. TRANSITION MECHANISMS:
           - Natural transition: Tollmien-Schlichting waves amplify, break down to turbulence
           - Bypass transition: freestream turbulence, surface roughness trip BL directly
           - Critical Re: depends on pressure gradient, roughness, freestream turbulence
           - Favorable pressure gradient (accelerating flow): stabilizes laminar BL, delays transition
           - Adverse gradient (decelerating): destabilizes, promotes transition and separation

        4. SEPARATION:
           - Laminar separation: occurs at low Re or strong adverse gradient. Forms bubble, often turbulent reattachment.
           - Turbulent separation: requires stronger adverse gradient. Massively separated = stall.
           - Separation criteria: du/dy|wall = 0 (zero wall shear stress)

        5. NATURAL LAMINAR FLOW (NLF):
           - Design airfoil for favorable pressure gradient over first 50-70% chord
           - Maintain surface smoothness < 0.0002 inch, no steps/gaps
           - Benefit: 15-25% drag reduction at cruise, significant fuel savings
           - Challenge: insect contamination, manufacturing tolerances, off-design performance

        6. TURBULENCE MODELS (CFD):
           - RANS: k-ε, k-ω SST models for engineering accuracy, computationally efficient
           - LES/DNS: resolves turbulent scales, research-level accuracy, expensive
           - Transition prediction: eN method, γ-Reθ models for RANS
        """,
        key_factors=[
            "Reynolds number Re = ρVL/μ: primary parameter for transition",
            "Pressure gradient: favorable delays transition, adverse promotes it",
            "Surface roughness: k/δ > 0.01 trips turbulent, k < 0.0002 inch for NLF",
            "Freestream turbulence: high Tu bypasses Tollmien-Schlichting route",
            "Suction/blowing: active flow control can stabilize laminar BL",
            "Compressibility: stabilizes BL in subsonic, destabilizes in supersonic"
        ],
        primary_authority=[
            "Schlichting & Gersten, Boundary-Layer Theory (9th ed.), Springer, 2017",
            "White, Viscous Fluid Flow (3rd ed.), McGraw-Hill, 2006",
            "Green, Laminar Flow Control - Back to the Future, AIAA Paper 2008-3738"
        ],
        burden_holder="Designer must specify surface finish, inspect for laminar flow achievement",
        adversary_position="Turbulent flow is acceptable; laminar flow impractical in service",
        counter_arguments=[
            "NLF demonstrated on Boeing 787 (≈1% fuel savings), Airbus A350, F-16XL",
            "Gliders achieve 60:1 L/D with NLF, 40:1 without - decisive performance gain",
            "Hybrid laminar flow control (HLFC) uses suction to extend laminar region",
            "Manufacturing advances (laser inspection) enable NLF production tolerances",
            "Insect contamination managed by Krueger flaps, leading-edge wash systems"
        ],
        resolution_strategy="Pursue NLF for long-range cruise aircraft; accept turbulent for short-haul, high-maneuver applications",
        entity_scope="Transport aircraft, business jets, gliders, UAVs, wind turbines",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="BL theory validated since Prandtl (1904), NLF in production on multiple aircraft",
        controlling_precedent=[
            "Prandtl boundary layer equations (1904)",
            "Tollmien-Schlichting instability theory (1929-1935)",
            "NASA NLF flight experiments (X-21, F-111 TACT, 757 NLF glove)"
        ],
        category=IssueCategory.BOUNDARY_LAYER
    ),

    DoctrineBlock(
        topic="Stall Characteristics: Leading Edge vs Trailing Edge",
        keywords=["stall", "CLmax", "separation", "leading edge stall", "trailing edge stall"],
        conclusion_template=[
            "Thin airfoils stall abruptly at leading edge (flow separates from sharp LE), thick airfoils gradually from TE.",
            "CLmax typically 1.0-1.2 for symmetric, 1.4-1.6 for cambered, 2.0-3.0 with high-lift devices.",
            "Stall warning and docile characteristics require trailing-edge stall progression with gentle pitch break."
        ],
        reasoning_framework="""
        1. LEADING EDGE STALL:
           - Occurs on thin airfoils (< 12% t/c), sharp leading edge, or high sweep
           - Flow separates at leading edge as α increases beyond critical
           - Abrupt loss of lift, sharp pitch break, often wing drop (asymmetric stall)
           - Little warning: pressure gradient at LE strengthens, sudden separation
           - Remedy: leading edge devices (slats, slots), vortex generators

        2. TRAILING EDGE STALL:
           - Occurs on thick airfoils (> 15% t/c), round leading edge
           - Separation starts at TE, moves forward with increasing α
           - Gradual CLmax, gentle stall, buffet warning as separation grows
           - Docile: pilot feels mushiness, buffet before full stall
           - Characteristic of GA aircraft (Cessna 172 NACA 2412, etc.)

        3. COMBINATION STALL:
           - Moderate thickness (12-15%), separation begins at TE and LE simultaneously
           - Behavior depends on Re, surface condition, details of pressure distribution
           - Common on many aircraft, stall character varies with wing design

        4. WING PLANFORM EFFECTS:
           - Rectangular wing: root stalls first (lower Re, higher α_eff), ailerons remain effective
           - Tapered wing: tip stalls first (higher local CL), aileron loss, possible spin entry
           - Washout (geometric twist): decreases tip α, ensures root stalls first
           - Elliptical lift distribution: uniform stall along span, ideal but hard to build

        5. REYNOLDS NUMBER:
           - Low Re (< 500k): laminar separation bubble, early stall, low CLmax
           - High Re (> 3M): thin turbulent BL, higher CLmax (1.2→1.6 for same airfoil)
           - Roughness at low Re: can improve CLmax by tripping BL, energizing flow

        6. POST-STALL:
           - Deep stall: separated flow on wing, tail in wake, elevator ineffective (T-tail risk)
           - Spin: autorotation with one wing stalled more than other, requires yaw + pitch + roll
           - Recovery: reduce α, increase Re (speed), ensure attached flow on control surfaces
        """,
        key_factors=[
            "Thickness ratio: thin = LE stall, thick = TE stall",
            "Leading edge radius: sharp = abrupt, round = gentle",
            "Wing twist (washout): ensures root-first stall, 3-5° typical",
            "Stall strips: force root stall, provide buffet warning",
            "Stick shaker/pusher: artificial stall warning, prevent entry",
            "Aspect ratio: high AR delays tip stall, low AR more tolerant"
        ],
        primary_authority=[
            "McCormick, Aerodynamics, Aeronautics, and Flight Mechanics (2nd ed.), Wiley, 1995",
            "Anderson, Introduction to Flight (8th ed.), McGraw-Hill, 2015",
            "NACA TN 2502, Characteristics of Airfoil Stall"
        ],
        burden_holder="Designer must ensure benign stall with adequate warning",
        adversary_position="High CLmax justifies abrupt stall if performance gains significant",
        counter_arguments=[
            "FAA Part 23/25 require stall warning and controllability in stall",
            "Loss of control in stall is leading cause of GA fatal accidents",
            "Docile stall achieved via wing design costs minimal performance (2-3% washout)",
            "Leading edge devices add weight/complexity but enable safe high-lift",
            "Flight test must demonstrate stall recovery in all configurations"
        ],
        resolution_strategy="Design for trailing-edge stall via washout, stall strips, or leading-edge devices; verify in wind tunnel and flight test",
        entity_scope="All aircraft requiring stall-spin certification (Part 23, Part 25)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Stall aerodynamics well-understood, extensive NACA/NASA research, regulatory requirements clear",
        controlling_precedent=[
            "14 CFR Part 23.201-207 (stall characteristics)",
            "14 CFR Part 25.201-207 (transport category stall)",
            "NACA research on stall (1930s-1950s)"
        ],
        category=IssueCategory.STALL_CHARACTERISTICS
    ),

    DoctrineBlock(
        topic="High-Lift Devices: Slats, Flaps, Krueger Flaps",
        keywords=["slats", "flaps", "high-lift", "CLmax", "leading edge devices"],
        conclusion_template=[
            "Leading edge slats increase CLmax 40-50% by re-energizing upper surface BL, delaying stall.",
            "Trailing edge flaps increase CLmax (plain 40%, split 60%, Fowler 90%) and camber, trading L/D for CL.",
            "Combined LE + TE devices achieve CLmax = 2.5-3.5, enabling short-field performance and low approach speeds."
        ],
        reasoning_framework="""
        1. LEADING EDGE SLATS:
           - Slot forms between slat and wing, accelerates flow over wing upper surface
           - Energizes boundary layer, delays separation, increases CLmax by 40-50%
           - Automatic slats: deploy aerodynamically under suction. Fixed slots: always open (drag penalty).
           - Boeing 737, Airbus A320: slats on inboard wing, improve root stall characteristics

        2. KRUEGER FLAPS:
           - Hinged panel on lower LE, deflects forward and down, increases camber and LE radius
           - Used on thin wings (swept, low t/c) where slat mechanisms difficult
           - Boeing 747, 777: Krueger flaps on inboard, slats on outboard
           - Provides insect shield in cruise (when retracted), smooth surface for NLF

        3. PLAIN FLAPS:
           - Hinged TE section, deflects down, increases camber and CLmax ≈ 40%
           - Simple, light, but generates large pitching moment (nose down)
           - Used on GA aircraft (Cessna, Piper) for low cost/weight

        4. SPLIT FLAPS:
           - Lower surface plate deflects, upper surface unchanged
           - High drag, moderate CLmax increase (60%), nose-down moment
           - Used on early jets (DC-3), dive brakes, some GA aircraft

        5. SLOTTED FLAPS:
           - Gap between flap and wing, slot energizes BL on flap upper surface
           - Single-slotted: +65% CLmax. Double-slotted: +85%. Triple-slotted: +100%.
           - Boeing 727 triple-slotted: CLmax ≈ 3.5, exceptional short-field performance

        6. FOWLER FLAPS:
           - Flap translates aft then rotates down, increasing wing area + camber
           - CLmax increase 90-100%, less drag penalty than plain flap at same CL
           - Boeing 737, 747, 777, Airbus family: Fowler or double-slotted Fowler
           - Tracks and mechanisms complex, heavy, but performance gain decisive

        7. PERFORMANCE IMPACT:
           - Takeoff: 5-15° flap, balances CLmax (short field) vs drag (climb rate)
           - Landing: full flap (30-40°), maximize CLmax for low Vstall, steep approach
           - L/D penalty: flaps decrease L/D, increase drag, enable slower speeds
        """,
        key_factors=[
            "CLmax increase: plain 40%, split 60%, slotted 65-85%, Fowler 90-100%",
            "Slats add 40-50% CLmax, delay stall, improve handling",
            "Drag increase: proportional to deflection, limits cruise use",
            "Pitching moment: flaps create nose-down moment, require trim",
            "Complexity/weight: Fowler heaviest, plain lightest",
            "Certification: must demonstrate safe deployment/retraction, no asymmetry hazards"
        ],
        primary_authority=[
            "Mair & Birdsall, Aircraft Performance, Cambridge University Press, 1992",
            "Shevell, Fundamentals of Flight (2nd ed.), Prentice Hall, 1989",
            "Smith, High-Lift Aerodynamics, Journal of Aircraft Vol. 12 No. 6, 1975"
        ],
        burden_holder="Designer optimizes flap type, deflection schedule for mission (field length, approach speed)",
        adversary_position="Simple flaps adequate; complex Fowler/slotted not worth weight/cost",
        counter_arguments=[
            "Runway-limited operations require maximum CLmax - Fowler enables access to short fields",
            "Approach speed reduction by 10 knots decreases landing distance by 20% (kinetic energy)",
            "Noise reduction: lower approach speed = less thrust = quieter (FAA Part 36)",
            "Boeing 787, A350 use simple flaps due to large wing area, but legacy aircraft need Fowler",
            "Operational flexibility: high CLmax allows increased payload or fuel without field length penalty"
        ],
        resolution_strategy="Use Fowler/slotted for transport, GA cross-country; plain flaps for trainers, light aircraft; slats for swept wings",
        entity_scope="All aircraft except aerobatic, some fighters (simple leading-edge flaps)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High-lift technology mature, proven over 70 years, extensive flight experience",
        controlling_precedent=[
            "NACA high-lift research (1930s-1950s)",
            "Boeing multi-element airfoil development (1960s-1980s)",
            "FAA Part 25.125 (landing climb requirements drive CLmax needs)"
        ],
        category=IssueCategory.HIGH_LIFT_DEVICES
    ),

    DoctrineBlock(
        topic="Wing Planform Design: Aspect Ratio, Sweep, Taper",
        keywords=["aspect ratio", "sweep", "taper ratio", "elliptical", "induced drag"],
        conclusion_template=[
            "High aspect ratio reduces induced drag (CDi ∝ 1/AR) but increases wing weight and bending moment.",
            "Wing sweep delays drag divergence (Mcrit increases) but causes tip stall, spanwise flow, and complexity.",
            "Taper ratio λ ≈ 0.4-0.5 approximates elliptical lift distribution, minimizes induced drag for given AR."
        ],
        reasoning_framework="""
        1. ASPECT RATIO (AR = b²/S):
           - High AR (gliders 20-40): low induced drag, excellent L/D, but heavy wing structure
           - Moderate AR (transport 7-12): balance efficiency vs weight, typical for jets
           - Low AR (fighters 2-4): high roll rate, low wave drag, structural efficiency, but high induced drag
           - Induced drag: CDi = CL²/(π·e·AR), so doubling AR cuts CDi in half (if e constant)
           - Weight penalty: bending moment ∝ b², spar weight ∝ AR^1.5, diminishing returns above AR=12

        2. WING SWEEP (Λ):
           - Sweepback delays compressibility: effective Mach M_eff = M∞·cos(Λ), increases Mcrit
           - 25° sweep: Mcrit ≈ 0.75. 35° sweep: Mcrit ≈ 0.85. Enables high-subsonic cruise.
           - Penalties: spanwise flow causes tip stall, lower CLmax, complex structure
           - Sweep necessary for M > 0.7 cruise (Boeing 737+, all jets except regional turboprops)

        3. TAPER RATIO (λ = ctip/croot):
           - Rectangular (λ=1): simple build, root stalls first, but non-elliptical (higher induced drag)
           - Elliptical (λ≈0.4): minimum induced drag (e=1.0), but tip stalls first, complex build
           - Moderate taper (λ=0.4-0.5): near-elliptical, good compromise, typical for modern aircraft
           - Extreme taper (λ<0.3): light wing tip, but severe tip stall, avoid unless swept

        4. SPAN EFFICIENCY FACTOR (e):
           - Elliptical distribution: e = 1.0 (theoretical ideal)
           - Tapered wing (λ=0.4): e ≈ 0.95-0.97
           - Rectangular: e ≈ 0.85
           - Swept wing: e ≈ 0.75-0.85 (vortex drag, spanwise flow)
           - Winglets: increase effective AR, e by 5-10%, worthwhile on long-range aircraft

        5. STRUCTURAL CONSIDERATIONS:
           - Bending moment maximum at root: M_b = ½ · q · S · b · (lift distribution factor)
           - Spar depth limited by t/c, affects fuel volume, landing gear stowage
           - Flutter: low AR, high taper increase flutter speed (stiffness vs inertia)
           - Aeroelasticity: sweep + high AR → divergence risk, requires careful design

        6. MISSION OPTIMIZATION:
           - Glider: AR=25+, λ=0.5, no sweep, maximize L/D
           - Airliner: AR=8-10, λ=0.25-0.3, sweep=25-35°, balance cruise efficiency vs Mcrit
           - Fighter: AR=2-4, λ=0.2, sweep=40-50° or delta, minimize wave drag, maximize agility
           - GA: AR=6-8, λ=0.5-0.6, no sweep, simple build, benign stall
        """,
        key_factors=[
            "Aspect ratio: gliders 20-40, transport 8-10, fighters 2-4",
            "Sweep angle: 0° subsonic, 25° high-subsonic, 35° transonic, 50° supersonic",
            "Taper ratio: 0.4-0.5 optimal for induced drag, 0.25-0.35 common on swept wings",
            "Span efficiency e: 0.95-1.0 ideal, 0.75-0.85 typical swept wing",
            "Wing loading W/S: low (10-15 psf) for STOL, high (100-150 psf) for speed",
            "Dihedral/anhedral: affects lateral stability, often combined with sweep"
        ],
        primary_authority=[
            "Raymer, Aircraft Design: A Conceptual Approach (6th ed.), AIAA, 2018",
            "Nicolai & Carichner, Fundamentals of Aircraft Design (2nd ed.), AIAA, 2010",
            "Anderson, Aircraft Performance and Design, McGraw-Hill, 1999"
        ],
        burden_holder="Designer selects AR, sweep, taper to meet speed, range, field length, weight constraints",
        adversary_position="Low AR acceptable for speed, maneuverability; high AR impractical",
        counter_arguments=[
            "Long-range mission: induced drag dominates (60% cruise drag), high AR essential (Boeing 787 AR=11)",
            "Modern composites reduce weight penalty of high AR (Boeing 787, Airbus A350)",
            "Sailplanes prove high AR practical: ASH 31 AR=33, DG-1000 AR=28, producible and robust",
            "Sweep unavoidable for M>0.75: all jets since 1950s swept, proven technology",
            "Taper ratio optimization via CFD/wind tunnel yields 2-5% drag reduction, significant over lifetime"
        ],
        resolution_strategy="Maximize AR within structural/aeroelastic limits; use sweep for Mcrit>0.70; taper for near-elliptical load; verify in wind tunnel",
        entity_scope="All fixed-wing aircraft, UAVs, missiles",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Planform theory validated by 80 years of aircraft development, CFD refinement ongoing",
        controlling_precedent=[
            "Prandtl lifting-line theory (minimum induced drag)",
            "Jones sweep theory (1945)",
            "Empirical data from thousands of aircraft types"
        ],
        category=IssueCategory.WING_PLANFORM
    ),

    DoctrineBlock(
        topic="Compressibility Effects and Critical Mach Number",
        keywords=["Mcrit", "compressibility", "Prandtl-Glauert", "drag divergence", "transonic"],
        conclusion_template=[
            "Critical Mach (Mcrit) is freestream M at which local flow first reaches M=1.0, typically on upper wing surface.",
            "Above Mcrit, shock waves form, causing drag divergence, buffet, and pitch changes.",
            "Supercritical airfoils delay Mcrit by flattening upper surface, enabling cruise at M=0.80-0.85."
        ],
        reasoning_framework="""
        1. INCOMPRESSIBLE TO COMPRESSIBLE TRANSITION:
           - Below M ≈ 0.3: air behaves incompressibly (ρ = constant)
           - M = 0.3-0.7: compressibility corrections (Prandtl-Glauert) apply
           - M > 0.7: nonlinear effects, shock waves, drag rise

        2. PRANDTL-GLAUERT COMPRESSIBILITY CORRECTION:
           - Pressure coefficient: Cp,comp = Cp,incomp / sqrt(1 - M²)
           - Lift coefficient: CL,comp = CL,incomp / sqrt(1 - M²)
           - Valid up to Mcrit, breaks down when shocks form
           - Explains why CL increases with M in subsonic (favorable until Mcrit)

        3. CRITICAL MACH NUMBER (Mcrit):
           - Defined: freestream M at which local M = 1.0 somewhere on airfoil (usually upper surface)
           - Typical values: thin airfoil Mcrit ≈ 0.75, supercritical Mcrit ≈ 0.85
           - Factors: thickness ratio (thinner = higher Mcrit), camber, CL (higher CL = lower Mcrit)
           - Beyond Mcrit: shock wave forms, boundary layer separates behind shock, drag rises

        4. DRAG DIVERGENCE:
           - MDD (drag divergence Mach): M where dCD/dM increases sharply, ≈ Mcrit + 0.03-0.05
           - Wave drag appears, CDw ∝ (M - Mcrit)^n, n ≈ 3-4 in transonic regime
           - Total drag can double from M=0.75 to M=0.85 if Mcrit=0.75
           - Airlines cruise just below MDD for fuel efficiency (Boeing 737: M=0.78, 777: M=0.84)

        5. SUPERCRITICAL AIRFOILS:
           - Flat upper surface reduces peak suction, delays shock formation
           - Aft camber for lift, thickened trailing edge for structural depth
           - Developed by NASA (R. Whitcomb, 1960s-70s), standard on modern jets
           - Boeing 767-787, Airbus A310-A350: supercritical sections enable M=0.82-0.85

        6. TRANSONIC AERODYNAMICS:
           - Mixed subsonic/supersonic flow, shock-BL interaction, separation
           - Buffet: shock oscillation, felt in cockpit, limits operational envelope
           - Mach tuck: shock moves aft, CP shifts aft, nose-down pitching moment
           - Control: must retain effectiveness through transonic (shock on elevator can reverse control)
        """,
        key_factors=[
            "Thickness ratio: 6% Mcrit ≈ 0.85, 12% Mcrit ≈ 0.75, 18% Mcrit ≈ 0.65",
            "Lift coefficient: Mcrit decreases with increasing CL (heavier aircraft = lower Mcrit)",
            "Sweep: increases effective Mcrit by factor 1/cos(Λ)",
            "Surface finish: roughness trips BL, promotes separation, lowers Mcrit slightly",
            "Altitude: higher altitude = lower Reynolds, but M effects same",
            "Area rule: fuselage contouring reduces transonic wave drag (F-102, B-58)"
        ],
        primary_authority=[
            "Anderson, Modern Compressible Flow (4th ed.), McGraw-Hill, 2021",
            "Kuethe & Chow, Foundations of Aerodynamics (5th ed.), Wiley, 1998",
            "Harris, An Introduction to Supercritical Wing Design, NASA TM X-72711, 1975"
        ],
        burden_holder="Designer must select airfoil, sweep for target cruise Mach without excessive drag",
        adversary_position="Cruise below M=0.75 to avoid compressibility penalties",
        counter_arguments=[
            "High-subsonic cruise (M=0.82-0.85) reduces trip time by 10-15%, valuable for long-haul",
            "Fuel burn per nautical mile optimizes at just below MDD, not at low speed",
            "Supercritical airfoils enable efficient cruise at M=0.85, proven on 787, A350",
            "Time savings on transoceanic routes justifies slight fuel penalty (if any) from higher M",
            "Competition: A380 M=0.85, 787 M=0.85, must match for market competitiveness"
        ],
        resolution_strategy="Use supercritical airfoils, moderate sweep (25-35°), thin sections for high-speed cruise; thicker sections for low-speed where Mcrit not limiting",
        entity_scope="All high-subsonic and transonic aircraft (jets, turboprops >M=0.5)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Compressibility theory established by Prandtl (1920s), supercritical tech proven over 50 years",
        controlling_precedent=[
            "Prandtl-Glauert rule (1928)",
            "Whitcomb supercritical airfoil (1965-1972)",
            "Boeing 787, Airbus A350 flight test validation"
        ],
        category=IssueCategory.COMPRESSIBILITY
    ),

    DoctrineBlock(
        topic="Supersonic Aerodynamics: Shocks, Expansion Fans, Wave Drag",
        keywords=["supersonic", "shock wave", "expansion fan", "Mach number", "wave drag"],
        conclusion_template=[
            "Supersonic flow is governed by oblique shocks (compression) and expansion fans (expansion), both isentropic except across shocks.",
            "Wave drag CDw ∝ (thickness ratio)² × (volume distribution non-ideality), minimized by slender bodies and area rule.",
            "Supersonic L/D is 4-8 (vs 15-20 subsonic) due to wave drag dominance, requiring high thrust and fuel consumption."
        ],
        reasoning_framework="""
        1. NORMAL SHOCK:
           - Sudden compression across infinitesimally thin wave, flow M>1 → M<1
           - Relations: M2 = sqrt[(1 + ((γ-1)/2)M1²) / (γM1² - (γ-1)/2)]
           - Pressure ratio: p2/p1 = 1 + (2γ/(γ+1))(M1² - 1)
           - Total pressure loss: entropy increases, Pt2/Pt1 < 1 (inefficiency)
           - Occurs on blunt noses, in intakes at off-design, detached bow shock

        2. OBLIQUE SHOCK:
           - Flow deflects by angle θ, shock at angle β to freestream
           - Tangential component M_t unchanged, normal component undergoes normal shock
           - Weak shock (small θ): attached to leading edge, less total pressure loss
           - Strong shock (large θ): detached, becomes bow shock, high losses
           - Cone shock: 3D analog, used on supersonic inlets (SR-71, Concorde)

        3. EXPANSION FAN (PRANDTL-MEYER):
           - Isentropic expansion around convex corner, M increases, p decreases
           - Continuous process (not sudden like shock), no entropy rise
           - Prandtl-Meyer function ν(M): relates turning angle to Mach change
           - Flow accelerates smoothly, favorable for supersonic design (aft body, nozzles)

        4. WAVE DRAG:
           - Volume wave drag: proportional to (thickness/length)², dominates for slender bodies
           - Lift wave drag: CDi,supersonic = CL² / (π·M·sqrt(M²-1)) for flat plate
           - Area rule (Whitcomb): smooth longitudinal area distribution reduces wave drag
           - Applied to F-102 (fuselage waist), B-58, all supersonic aircraft

        5. SUPERSONIC AIRFOILS:
           - Thin, sharp leading edge: attached shock, low wave drag
           - Biconvex, double wedge, hexagonal: analytical solutions, good starting points
           - L/D: 4-6 typical (Concorde), vs 15-20 subsonic
           - CLmax low (≈0.5): high wing loading, high approach speeds

        6. INLET DESIGN:
           - Subsonic diffusion required: M>1 → M<0.4 for combustor
           - Normal shock inlet (F-16): simple, but 28% total pressure loss at M=2
           - External compression (SR-71, F-15): oblique shocks + normal, Pt recovery >90% at M=2
           - Variable geometry: ramps, spikes adjust for Mach range (SR-71 spike translates 26 inches)

        7. SONIC BOOM:
           - N-wave: overpressure then underpressure, perceived as double boom
           - Pressure ∝ (weight/length)^(3/4) / altitude, minimized by slender body, high altitude
           - Regulations: FAA bans supersonic overland (14 CFR 91.817), limits commercial supersonic
        """,
        key_factors=[
            "Mach number M: subsonic <1, transonic 0.8-1.2, supersonic 1.2-5, hypersonic >5",
            "Shock angle β: strong shock (near 90°) vs weak shock (small deflection)",
            "Area rule: smooth A(x) reduces wave drag by 20-40% (Concorde, F-102)",
            "Slenderness ratio L/D: >10 for low wave drag (SR-71 L/D ≈ 6 at M=3.2)",
            "Inlet recovery: >90% Pt at design Mach essential for engine performance",
            "Sonic boom: Concorde 2 psf overpressure, audible 50 miles, regulatory barrier"
        ],
        primary_authority=[
            "Anderson, Modern Compressible Flow (4th ed.), McGraw-Hill, 2021",
            "Liepmann & Roshko, Elements of Gas Dynamics, Dover, 2001",
            "Shapiro, The Dynamics and Thermodynamics of Compressible Fluid Flow, Wiley, 1953"
        ],
        burden_holder="Supersonic designer must minimize wave drag, manage inlet shock system, accept low L/D",
        adversary_position="Supersonic flight impractical due to fuel consumption, sonic boom, costs",
        counter_arguments=[
            "Military necessity: fighters require supersonic capability for intercept, combat",
            "Concorde operated profitably for 27 years, proved technical feasibility",
            "Boom-shaping (NASA X-59): elongated nose, distributed lift reduce boom to acceptable levels",
            "Laminar flow at supersonic possible: reduces skin friction 50%, NASA research ongoing",
            "Hypersonic scramjet: combustion at M>5 enables efficient high-speed flight (X-51, X-43)"
        ],
        resolution_strategy="Accept low L/D for supersonic; use area rule, slender body, efficient inlets; pursue boom-shaping for overland",
        entity_scope="Military fighters, supersonic transports, missiles, space launch vehicles",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Supersonic theory validated since 1940s, extensive flight experience (fighters, Concorde, SR-71)",
        controlling_precedent=[
            "Prandtl-Meyer expansion theory (1908)",
            "Whitcomb area rule (1952)",
            "Concorde, SR-71 flight test data (1960s-2003)"
        ],
        category=IssueCategory.SUPERSONIC_AERO
    ),

    DoctrineBlock(
        topic="Longitudinal Stability: Static Margin and Neutral Point",
        keywords=["static margin", "neutral point", "stability", "CG", "pitch"],
        conclusion_template=[
            "Static margin SM = (xnp - xcg)/MAC where xnp is neutral point, xcg is CG location.",
            "Positive SM (CG ahead of NP) → stable, negative → unstable. Typical SM = 5-15% MAC for conventional aircraft.",
            "Neutral point is AC of complete aircraft; moving CG aft decreases stability, improves performance but requires active control."
        ],
        reasoning_framework="""
        1. AERODYNAMIC CENTER (AC):
           - Point where pitching moment is independent of angle of attack
           - Airfoil AC at ≈25% chord (subsonic), ≈50% chord (supersonic)
           - Lift acts at AC; moment about AC is constant (Cm,ac)

        2. NEUTRAL POINT (NP):
           - AC of complete aircraft (wing + tail + fuselage)
           - If CG at NP, aircraft is neutrally stable (∂Cm/∂α = 0)
           - Calculated: xnp = xac,wb + (Vbar·ηh·CLα,t/CLα,wb)·lt/MAC
           - Vbar = tail volume ratio = (St·lt)/(S·MAC)

        3. STATIC MARGIN:
           - SM = (xnp - xcg) / MAC, expressed as % MAC
           - Positive SM: CG ahead of NP → stable (restoring moment opposes disturbance)
           - Negative SM: CG behind NP → unstable (divergent)
           - Zero SM: neutral, constant stick force for all speeds (dangerous)

        4. STICK-FIXED STABILITY:
           - ∂Cm/∂α = -(xnp - xcg)/MAC · CLα,total
           - Negative slope required for stability (pitch-up → nose-down moment)
           - Stick gradient: ∂elevator/∂speed, should be positive (pull to slow, push to speed)

        5. CG LIMITS:
           - Forward limit: excessive stick force (nose-heavy), tail stall on landing
           - Aft limit: insufficient stability, poor stall recovery, possible uncontrollable
           - Typical range: 10-20% MAC for GA, 15-35% MAC for transport (wider range)
           - Loading: fuel burn, passenger distribution change CG, must stay in envelope

        6. RELAXED STATIC STABILITY (RSS):
           - Modern fighters: CG at or behind NP (SM = -5% to +5%), active FBW control
           - Benefits: reduced trim drag (less tail down-force), improved maneuverability
           - Penalty: requires redundant flight control computers, sensors (F-16, F-22, all modern fighters)

        7. CANARD CONFIGURATION:
           - Canard ahead of wing, both generate positive lift
           - NP farther forward than conventional (tail), wider CG range
           - Advantage: no tail blanking in stall, efficient trim
           - Disadvantage: canard stall → pitch-up (dangerous), complex coupling
        """,
        key_factors=[
            "Static margin: 5-10% conservative (trainers), 10-15% typical (transport), -5% to +5% fighters (RSS)",
            "Tail volume Vbar: 0.35-0.50 for GA, 0.50-0.70 for transport, ensures adequate authority",
            "CG range: 15-25% MAC typical for transport, certified limits in AFM/POH",
            "Elevator effectiveness: must overcome Cm at all CG, speeds, configurations",
            "Downwash ε: reduces tail AoA, affects stability (∂ε/∂α from wing wake)",
            "Power effects: thrust line, slipstream change Cm, must account in stability analysis"
        ],
        primary_authority=[
            "Etkin & Reid, Dynamics of Flight: Stability and Control (3rd ed.), Wiley, 1996",
            "Nelson, Flight Stability and Automatic Control (2nd ed.), McGraw-Hill, 1998",
            "Roskam, Airplane Flight Dynamics and Automatic Flight Controls, DARcorporation, 1998"
        ],
        burden_holder="Designer must ensure positive SM across CG envelope, meet handling quality specs",
        adversary_position="Relaxed stability acceptable with FBW, reduces drag, improves performance",
        counter_arguments=[
            "FAA Part 23/25 require positive static stability (stick-fixed) for certification",
            "RSS requires redundant systems: F-16 has quad-redundant FCS, costly and complex",
            "Loss of FCS in RSS aircraft = immediate loss of control (AF447-like scenario)",
            "Conventional stability provides inherent safety: pilot can recover from upsets",
            "Trim drag reduction from RSS only 1-2%, marginal benefit vs risk for civil aircraft"
        ],
        resolution_strategy="Conventional stability (SM 5-15%) for civil, trainers; RSS for fighters with mil-spec FBW; canards for specific advantages (visibility, efficiency)",
        entity_scope="All aircraft, UAVs, missiles with aerodynamic control",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Stability theory mature since 1920s, regulatory requirements clear, extensive validation",
        controlling_precedent=[
            "14 CFR Part 23.171-175 (stability requirements)",
            "14 CFR Part 25.171-177 (transport stability)",
            "MIL-F-8785C (military handling qualities)"
        ],
        category=IssueCategory.STABILITY_CONTROL
    ),

    DoctrineBlock(
        topic="Aircraft Performance: Breguet Range Equation",
        keywords=["range", "endurance", "Breguet", "specific fuel consumption", "L/D"],
        conclusion_template=[
            "Breguet range equation: R = (V/c)·(L/D)·ln(Wi/Wf) for jets, R = (η/c)·(L/D)·ln(Wi/Wf) for props.",
            "Maximum range occurs at (L/D)max for jets, at CL = sqrt(3·CD0/(πeAR)) for props.",
            "Endurance maximized at minimum power (props) or minimum fuel flow (jets), lower speed than max range."
        ],
        reasoning_framework="""
        1. JET AIRCRAFT RANGE (BREGUET):
           - Derivation: dR = -V·(L/D)·dW/(c·W), integrate to R = (V/c)·(L/D)·ln(Wi/Wf)
           - V = cruise speed, c = TSFC (lb fuel / lb thrust / hour), L/D, Wi/Wf = initial/final weight ratio
           - Maximize range: fly at (L/D)max speed, altitude for best TSFC, minimize reserves
           - Typical values: airliner L/D ≈ 18, TSFC ≈ 0.55, Wi/Wf ≈ 1.5, R ≈ 5000 nm

        2. PROPELLER AIRCRAFT RANGE:
           - R = (η/c)·(L/D)·ln(Wi/Wf), where η = propeller efficiency, c = BSFC (lb/hp/hr)
           - Propeller converts power to thrust: T = ηP/V, so V cancels in derivation
           - Max range: (L/D)max but at higher CL than jet (lower speed for given weight)
           - CL for max range: CL = sqrt(3·CD0/(πeAR)), approximately 30% above (L/D)max speed

        3. ENDURANCE:
           - Time aloft = (1/c)·(L/D)·ln(Wi/Wf) for jets: maximize (L/D), minimize TSFC
           - For props: E = (η/c)·(L/D)·(1/V)·ln(Wi/Wf), maximize L^1.5/D, fly slower than range
           - Jet endurance: often at loiter altitude (lower TSFC), speed for max L/D
           - Prop endurance: minimum power speed, CL for (L/D)/V maximum

        4. ALTITUDE EFFECTS:
           - TSFC improves with altitude (lower temperature for given thrust), but levels off at tropopause
           - Jet optimal altitude: 35,000-43,000 ft for long-range cruise (B777, A350)
           - Propeller: lower altitude (< 25,000 ft), engine power decreases with altitude
           - Step climbs: as weight decreases (fuel burn), climb to maintain optimal altitude

        5. WIND EFFECTS:
           - Headwind: reduces range proportional to wind speed, severe on long routes
           - Tailwind: increases range, flight planning critical (ETOPS, oceanic routes)
           - Jet streams: 100+ knot tailwind at altitude, can reduce trip time/fuel 10-20%

        6. PAYLOAD-RANGE DIAGRAM:
           - Maximum payload: limited by MTOW, short range (fuel limited)
           - Maximum fuel: reduced payload (weight limited), maximum range
           - Ferry range: zero payload, maximum fuel, > 2× normal range
           - Design point: matches mission (e.g., 3000 nm with full passengers)

        7. OPERATIONAL CONSIDERATIONS:
           - Reserves: FAA requires 45 min (domestic) or destination + 200 nm + 30 min (international)
           - Contingency fuel: 5-10% trip fuel for weather, ATC delays
           - Alternate: sufficient fuel to reach alternate airport if destination unavailable
           - ETOPS: extended range twin ops, 120-330 min from diversion airport depending on certification
        """,
        key_factors=[
            "L/D: 18-20 for modern jets (787, A350), 15-17 for older (737, A320), 8-12 for fighters",
            "TSFC: 0.45-0.55 for high-bypass turbofans, 0.8-1.2 for turbojets, 0.4-0.5 for turboprops (BSFC)",
            "Weight ratio Wi/Wf: 1.3-1.6 typical (30-40% fuel fraction)",
            "Propeller efficiency η: 0.80-0.85 cruise, variable-pitch constant-speed prop",
            "Cruise altitude: 35k-43k ft jets, 15k-25k ft turboprops, 8k-12k ft piston",
            "Mach number: M=0.78-0.85 for jets (just below MDD), M<0.5 for props"
        ],
        primary_authority=[
            "Anderson, Aircraft Performance and Design, McGraw-Hill, 1999",
            "Mair & Birdsall, Aircraft Performance, Cambridge University Press, 1992",
            "Shevell, Fundamentals of Flight (2nd ed.), Prentice Hall, 1989"
        ],
        burden_holder="Operator must plan fuel load, altitude, speed for mission range/endurance requirements",
        adversary_position="Fly faster to reduce trip time, even if fuel burn increases",
        counter_arguments=[
            "Cost index optimization: balance fuel cost vs time cost, airlines use CI = 0 (max range) to CI = 100 (max speed)",
            "Long-range international: fuel cost dominates, fly at max range speed (M=0.82-0.84)",
            "Short-haul: time cost dominates, fly faster (M=0.76-0.78), less efficient but fewer cycles",
            "Wind optimization: fly higher/lower to exploit jet stream or avoid headwind, can save 5-10% fuel",
            "Step climbs: increase altitude as weight decreases, maintain optimal altitude, 2-3% fuel savings"
        ],
        resolution_strategy="Fly at (L/D)max for max range, minimize TSFC via altitude, account for wind, reserves per regulations; use cost index for time-fuel trade",
        entity_scope="All aircraft with range/endurance requirements (commercial, GA, military transport)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Breguet equation derived from first principles, validated over 100 years of flight operations",
        controlling_precedent=[
            "Breguet range equation (1919)",
            "14 CFR Part 121.645 (fuel reserves)",
            "ICAO Annex 6 (international fuel requirements)"
        ],
        category=IssueCategory.AIRCRAFT_PERFORMANCE
    ),

    DoctrineBlock(
        topic="V-Speeds: Vs, Vmc, Vr, V1, Vx, Vy, Vne",
        keywords=["V-speeds", "stall speed", "rotation", "decision speed", "never exceed"],
        conclusion_template=[
            "Vs (stall speed) = sqrt(2W/(ρSCLmax)), increases with weight, altitude, bank angle.",
            "V1 (decision speed) is maximum speed to abort takeoff, critical for balanced field length.",
            "Vne (never exceed speed) limited by flutter, structural loads, or compressibility; exceedance risks catastrophic failure."
        ],
        reasoning_framework="""
        1. STALL SPEED (Vs):
           - Vs = sqrt(2W / (ρ·S·CLmax)), function of weight, density, wing area, CLmax
           - Vs0: stall speed landing configuration (full flaps, gear down)
           - Vs1: stall speed takeoff configuration (takeoff flaps)
           - 1.3 Vs used for approach speed (Part 23), 1.23 Vsr for Part 25
           - Bank angle: Vs,bank = Vs·sqrt(1/cos(φ)), e.g., 60° bank → 1.41× Vs

        2. MINIMUM CONTROL SPEED (Vmc):
           - Multi-engine: minimum speed to maintain directional control with one engine inoperative
           - Critical: most unfavorable conditions (aft CG, takeoff power, out-of-ground effect)
           - 5° bank toward good engine allowed, full rudder deflection
           - Vmca (air): < Vs for certification, else placard "flight prohibited"
           - Vmcg (ground): on ground, nosewheel steering + rudder + brakes

        3. ROTATION SPEED (Vr):
           - Speed at which pilot rotates (pulls back) to lift off
           - Vr ≥ 1.05 Vmc (multi-engine), Vr ≥ Vs (single-engine)
           - Too low: inadequate control authority, tail strike. Too high: excess runway used.

        4. DECISION SPEED (V1):
           - Maximum speed to abort takeoff and stop within runway (ASDA)
           - Below V1: abort for any malfunction. Above V1: continue takeoff.
           - Balanced field length: accelerate-stop distance = accelerate-go distance at V1
           - V1 ≤ Vr ≤ V2 (takeoff safety speed), gap narrows with higher weights

        5. BEST ANGLE (Vx) AND BEST RATE (Vy) CLIMB:
           - Vx: maximum angle of climb (altitude gain per distance), clears obstacle
           - Vx occurs at (L/D)max for jets, slightly higher CL for props
           - Vy: maximum rate of climb (altitude gain per time), fastest to cruise altitude
           - Vy occurs at minimum power required for props, (T-D)·V maximum for jets

        6. MANEUVERING SPEED (Va):
           - Maximum speed for full control deflection without exceeding limit load factor
           - Va = Vs·sqrt(n_limit), e.g., n=3.8g → Va = 1.95×Vs
           - Below Va: aircraft stalls before reaching limit load (safe)
           - Above Va: full control deflection can overstress (avoid in turbulence)

        7. NEVER EXCEED SPEED (Vne):
           - Red line, absolute structural/aeroelastic limit
           - Limited by flutter (dynamic instability), Mach effects, or ultimate load
           - Typically 1.5-2.0× Vc (cruise speed) for GA, Mach limit for jets
           - Exceedance: structural failure (tail loss, wing failure), often fatal

        8. MAXIMUM OPERATING SPEED (Vmo/Mmo):
           - Highest speed for normal operations (placard, not red line)
           - Vmo: IAS limit (low altitude), Mmo: Mach limit (high altitude)
           - Overspeed warning (clacker) at Vmo/Mmo, allows margin to Vne/Mne
        """,
        key_factors=[
            "Stall speed Vs: 50-60 knots (GA), 100-140 knots (jets, clean), 120-180 knots (heavy jets)",
            "V1: 80-120 knots (GA), 140-180 knots (jets), depends on weight, runway, temp",
            "Vr: slightly above V1, 5-10 knots typically",
            "Vy: 1.3-1.5× Vs for props, higher for jets (excess thrust)",
            "Va: varies with weight (lighter = lower Va), typically 1.7-2.0× Vs0",
            "Vne: 150-200 knots (GA), 300-400 knots (jets IAS), or Mmo (M=0.82-0.92)"
        ],
        primary_authority=[
            "FAA Airplane Flying Handbook (FAA-H-8083-3C), 2021",
            "14 CFR Part 23.49, 23.51, 23.149, 23.1505 (V-speeds definitions)",
            "14 CFR Part 25.107, 25.109, 25.149 (transport category V-speeds)"
        ],
        burden_holder="Pilot must know, adhere to V-speeds for safe operations; exceed = certificate action",
        adversary_position="V-speeds are conservative; experienced pilots can exceed slightly",
        counter_arguments=[
            "V-speeds determined by certification flight test, account for production variation, aging",
            "Vne exceedance: multiple fatal accidents (Cessna 210, Beech Bonanza in-flight breakups)",
            "Va exceedance in turbulence: American Airlines 587 (A300 tail loss), excessive rudder inputs",
            "V1 critical: Comair 5191 (incorrect runway, insufficient length, V1 decision failure)",
            "Stall-spin at low altitude: leading GA fatal cause, respect Vs + margin"
        ],
        resolution_strategy="Adhere strictly to V-speeds, especially Vne, V1, Vs; understand weight/configuration effects; plan takeoff for balanced field or adequate margin",
        entity_scope="All aircraft, mandatory for certification and operations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="V-speed definitions and limits established by 80+ years certification practice, accident data validation",
        controlling_precedent=[
            "14 CFR Part 23/25 (certification standards)",
            "NTSB accident reports (V-speed exceedances)",
            "FAA Advisory Circulars (AC 23-8C, etc.)"
        ],
        category=IssueCategory.AIRCRAFT_PERFORMANCE
    ),

    DoctrineBlock(
        topic="Propeller Aerodynamics: Blade Element Theory",
        keywords=["propeller", "blade element", "advance ratio", "efficiency", "thrust"],
        conclusion_template=[
            "Propeller thrust T and power P derived by integrating blade element forces over radius.",
            "Advance ratio J = V/(nD) determines operating point; efficiency η peaks at design J, typically 0.80-0.85.",
            "Variable-pitch propellers maintain optimal blade AoA across speed range, constant-speed governor controls RPM."
        ],
        reasoning_framework="""
        1. BLADE ELEMENT THEORY:
           - Divide blade into radial elements, analyze each as 2D airfoil
           - Local velocity = vector sum of freestream V and rotational ωr
           - Inflow angle φ = arctan(V / (ωr)), blade pitch angle β, AoA α = β - φ
           - Lift and drag on element → thrust dT and torque dQ
           - Integrate: T = ∫ dT, Q = ∫ dQ, P = ωQ

        2. ADVANCE RATIO:
           - J = V / (n·D), where V = freestream speed, n = RPS, D = diameter
           - Low J (takeoff, climb): high thrust, low efficiency
           - Design J (cruise): maximum efficiency η = T·V / P
           - High J (dive): thrust → 0 or negative (windmilling), low efficiency

        3. PROPELLER EFFICIENCY:
           - η = T·V / P = (thrust power) / (shaft power)
           - Ideal efficiency (actuator disk): η = 2 / (1 + sqrt(1 + T/(½ρV²A)))
           - Real efficiency: 0.80-0.85 at design J, 0.70-0.75 at static (J=0), 0.60-0.70 at high J
           - Losses: profile drag, tip vortex, compressibility at blade tips (Mtip), swirl

        4. FIXED-PITCH PROPELLER:
           - Single blade angle, optimized for one flight condition (cruise or climb)
           - Climb prop: low pitch, high RPM, good static thrust, poor cruise efficiency
           - Cruise prop: high pitch, low RPM, poor static thrust, good cruise efficiency
           - Simple, light, cheap, but compromise performance

        5. VARIABLE-PITCH / CONSTANT-SPEED:
           - Governor controls blade pitch to maintain constant RPM (set by pilot)
           - Takeoff: low pitch (fine), high RPM, max thrust
           - Cruise: high pitch (coarse), lower RPM, max efficiency
           - Enables wide operating range, optimum performance at each condition
           - Standard on multi-engine, high-performance singles

        6. FEATHERING:
           - Blade rotates to ~90° (edge into wind), minimizes drag from windmilling
           - Critical for multi-engine: feather failed engine, reduce drag, maintain control
           - Unfeathered windmilling prop: huge drag, yaw moment, loss of performance

        7. REVERSE THRUST:
           - Negative blade pitch, thrust directed forward, used for braking after landing
           - Turboprops: power applied with reverse pitch, significant deceleration
           - Reduces brake wear, landing distance, especially on wet/icy runways

        8. TIP EFFECTS:
           - Mtip = M∞ + (ωR/a), can exceed M=1 even when aircraft subsonic
           - Compressibility drag, noise (blade vortex interaction), limits RPM/diameter
           - Scimitar tips, swept blades reduce Mtip effects, lower noise
        """,
        key_factors=[
            "Efficiency η: 0.80-0.85 peak, 0.70-0.75 static, depends on advance ratio J",
            "Blade number: 2 (light GA), 3-4 (twins, turboprops), 5-6 (high power turboprops)",
            "Diameter: larger = higher efficiency (lower disk loading), but weight, tip Mach limits",
            "Activity factor: blade solidity, affects thrust capability and efficiency",
            "Constant-speed: maintains optimal blade AoA, improves efficiency 10-15% vs fixed",
            "Reverse thrust: reduces landing roll 20-30%, critical on short/slippery runways"
        ],
        primary_authority=[
            "McCormick, Aerodynamics, Aeronautics, and Flight Mechanics (2nd ed.), Wiley, 1995",
            "Seddon & Newman, Basic Helicopter Aerodynamics (3rd ed.), Wiley, 2011",
            "Leishman, Principles of Helicopter Aerodynamics (2nd ed.), Cambridge, 2006"
        ],
        burden_holder="Designer selects blade number, diameter, pitch for mission; pilot operates within limits",
        adversary_position="Fixed-pitch adequate for simple aircraft; constant-speed complexity not worth cost",
        counter_arguments=[
            "Constant-speed improves takeoff performance (critical for high-density altitude), climb rate, cruise speed",
            "Multi-engine: feathering essential for safety after engine failure (14 CFR Part 23.2135)",
            "Efficiency gain 10-15%: significant fuel savings over aircraft lifetime",
            "Turboprops: all use variable-pitch for optimal performance across Mach 0.1-0.6 range",
            "Certification: Part 23 requires feathering for twins above 6000 lb"
        ],
        resolution_strategy="Use constant-speed for high-performance singles, all twins, turboprops; fixed-pitch for trainers, light singles; feathering mandatory for twins",
        entity_scope="All propeller aircraft, turboprops, some UAVs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Blade element theory validated since 1920s, extensive flight experience",
        controlling_precedent=[
            "Glauert blade element momentum theory (1926)",
            "Hamilton Standard constant-speed prop (1930s)",
            "14 CFR Part 23/25 propeller requirements"
        ],
        category=IssueCategory.PROPELLER_AERO
    ),

    DoctrineBlock(
        topic="Rotary Wing Aerodynamics: Momentum Theory and Blade Flapping",
        keywords=["helicopter", "rotor", "momentum theory", "induced velocity", "flapping"],
        conclusion_template=[
            "Momentum theory: induced velocity vi = sqrt(T/(2ρA)), power P = T·vi in hover, 1.15× in ground effect.",
            "Blade flapping equalizes lift between advancing and retreating blades, prevents rollover, requires flapping hinge or flexure.",
            "Forward flight: advancing blade sees higher V, retreating blade lower; cyclic pitch modulates lift to balance moments."
        ],
        reasoning_framework="""
        1. MOMENTUM THEORY (HOVER):
           - Actuator disk: rotor accelerates air downward, creates thrust
           - Induced velocity: vi = sqrt(T / (2ρA)), where A = πR² (disk area)
           - Power: P = T·vi = T^(3/2) / sqrt(2ρA), ideal (no profile drag, no swirl)
           - Figure of merit FM = Pideal / Pactual, typical FM = 0.70-0.75
           - Ground effect (IGE): reduces vi (ground blocks downwash), P decreases 15-25% at 1 rotor diameter height

        2. BLADE ELEMENT THEORY (ROTOR):
           - Similar to propeller: integrate lift/drag over blade radius
           - Twist: blade pitch decreases toward tip (optimal AoA distribution)
           - Collective pitch: changes all blades equally, controls thrust/altitude
           - Cyclic pitch: varies pitch once per revolution, tilts rotor disk, controls horizontal movement

        3. BLADE FLAPPING:
           - Advancing blade (forward flight): sees V∞ + ωR, high dynamic pressure, high lift
           - Retreating blade: sees ωR - V∞, low dynamic pressure, low lift
           - Without flapping: huge rolling moment toward retreating side → rollover
           - Flapping hinge: blade flaps up on advancing side, down on retreating, equalizes lift
           - Flapping angle β: proportional to advance ratio μ = V∞/(ωR)

        4. DISSYMMETRY OF LIFT:
           - Forward flight: advancing blade generates more lift than retreating
           - Cyclic pitch: decrease pitch on advancing, increase on retreating
           - Reverse flow region: inner part of retreating blade, flow reversed (no lift)
           - Retreating blade stall: high AoA to compensate, can stall, limits max speed

        5. AUTOROTATION:
           - Engine failure: rotor windmills, air flows up through disk, sustains RPM
           - Regions: driven (inner), driving (mid), stall (outer), net positive torque maintains RPM
           - Descent rate: 1500-2000 fpm typical, collective flare before landing arrests descent
           - Safe landing possible with zero power, unique helicopter capability

        6. RETREATING BLADE STALL:
           - High-speed / high-G maneuver: retreating blade AoA exceeds stall
           - Symptoms: vibration, nose pitch-up, roll toward retreating blade
           - Limits Vne: typically 150-200 knots for conventional helicopters
           - Advancing blade tip Mach: also limits speed (compressibility effects)

        7. TAIL ROTOR:
           - Provides anti-torque (counters main rotor torque), directional control
           - Thrust = main rotor torque / tail boom length
           - Loss of tail rotor (LTE): loss of yaw control, especially in right quartering tailwind
           - NOTAR: no tail rotor, uses jet + Coanda effect, quieter, safer, more expensive
        """,
        key_factors=[
            "Disk loading T/A: 5-10 psf (light helos), 10-20 psf (heavy), lower = better hover efficiency",
            "Figure of merit FM: 0.70-0.75 typical, measures hover efficiency",
            "Advance ratio μ: V∞/(ωR), typically < 0.4 (stall limit), racers up to 0.5",
            "Blade loading T/(bcR): lower = less retreating blade stall, more blades or larger radius",
            "Tip speed ωR: 650-750 fps typical, limited by Mach (compressibility noise)",
            "Ground effect: 15-25% power reduction in hover at < 1 diameter height"
        ],
        primary_authority=[
            "Leishman, Principles of Helicopter Aerodynamics (2nd ed.), Cambridge, 2006",
            "Seddon & Newman, Basic Helicopter Aerodynamics (3rd ed.), Wiley, 2011",
            "Prouty, Helicopter Performance, Stability, and Control, Krieger, 2002"
        ],
        burden_holder="Designer balances disk loading, blade number, tip speed for performance; pilot stays within flight envelope",
        adversary_position="Helicopters inherently inefficient, limited speed, high cost vs fixed-wing",
        counter_arguments=[
            "Unique capabilities: hover, vertical takeoff/landing, low-speed maneuver justify helicopter",
            "Autorotation: inherent safety mechanism, dead-stick landing possible (unlike jet)",
            "Missions: search/rescue, offshore oil, air ambulance, military assault require hover",
            "Speed limitations: tiltrotor (V-22) overcomes via transition to airplane mode (300+ knots)",
            "Efficiency improving: composite blades, advanced airfoils, active vibration control reduce costs"
        ],
        resolution_strategy="Accept helicopter limitations for missions requiring hover; pursue compound/tiltrotor for high-speed; optimize rotor design for specific mission",
        entity_scope="All rotary-wing aircraft (helicopters, tiltrotors, compound helicopters)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Rotor aerodynamics established since 1940s, extensive flight validation, ongoing CFD refinement",
        controlling_precedent=[
            "Glauert momentum theory (1926)",
            "Lock flapping equation (1927)",
            "14 CFR Part 27/29 (rotorcraft certification)"
        ],
        category=IssueCategory.ROTARY_WING
    ),

    DoctrineBlock(
        topic="Wind Tunnel Testing: Scaling, Reynolds Number Effects",
        keywords=["wind tunnel", "Reynolds number", "Mach number", "similarity", "testing"],
        conclusion_template=[
            "Wind tunnel testing requires geometric similarity (scale model), kinematic similarity (Re match), dynamic similarity (M match).",
            "Low-Re wind tunnels (model < full scale Re) overpredict drag, underpredict CLmax; corrections applied via boundary layer trips, empirical data.",
            "Transonic wind tunnels require slotted/perforated walls to avoid blockage, choking; cryogenic tunnels achieve high Re at moderate size."
        ],
        reasoning_framework="""
        1. SIMILARITY REQUIREMENTS:
           - Geometric: model is scaled replica (1:10, 1:20 common for large aircraft)
           - Kinematic: flow patterns identical, Re_model = Re_full (ρVL/μ match)
           - Dynamic: force ratios identical, M_model = M_full for compressibility
           - Impossible to match both Re and M in conventional tunnel (size, power limits)

        2. REYNOLDS NUMBER SCALING:
           - Full-scale Re: 10-50 million (transport wing), 1-5 million (GA)
           - Model Re: 0.5-5 million typical (limited by tunnel speed, model size)
           - Low Re effects: early transition, thick BL, higher drag, lower CLmax
           - Corrections: boundary layer trips (zigzag tape, grit), empirical factors

        3. MACH NUMBER SCALING:
           - Subsonic tunnels: M < 0.3 (incompressible), up to M = 0.9 (high-subsonic)
           - Transonic tunnels: M = 0.7-1.2, slotted walls (vent pressure waves, avoid choking)
           - Supersonic tunnels: M = 1.5-5, fixed Mach (nozzle sets M), blow-down or continuous
           - Hypersonic: M > 5, shock tunnels, limited run time (seconds)

        4. BLOCKAGE CORRECTIONS:
           - Model blocks tunnel cross-section, accelerates flow, overpredicts dynamic pressure
           - Rule: model frontal area < 5% tunnel area to minimize blockage
           - Corrections: empirical (Pope, Barlow), CFD, or open-jet (free boundaries)

        5. WALL INTERFERENCE:
           - Solid walls: constrain streamlines, increase lift (false AoA increase)
           - Slotted/perforated walls: reduce interference, essential for transonic (M > 0.7)
           - Open jet: no walls, but jet boundary unstable, limited to low speed

        6. TURBULENCE LEVEL:
           - Freestream turbulence affects transition, separation, CLmax
           - Low-turbulence tunnels: Tu < 0.1%, screens, honeycomb, contraction ratio 9:1+
           - Atmospheric turbulence Tu ≈ 1%, wind tunnel Tu ≈ 0.05-0.5% (cleaner than flight)

        7. FORCE BALANCE MEASUREMENT:
           - 6-component balance: lift, drag, side force, pitch, roll, yaw moments
           - Sting mount (rear) vs floor mount, strut interference corrections
           - Accuracy: ±0.5% force, ±0.1° angle, high-precision calibration

        8. FLOW VISUALIZATION:
           - Tufts: yarn strands show flow direction, separation regions
           - Smoke/dye: visualize streamlines, vortices (low speed)
           - Schlieren: density gradients, shock waves (supersonic)
           - Pressure-sensitive paint (PSP): surface pressure distribution, full-field
           - Particle image velocimetry (PIV): velocity field measurement

        9. CRYOGENIC TUNNELS:
           - NASA National Transonic Facility (NTF): liquid nitrogen, -250°F
           - Increases Re by 3× (higher ρ, lower μ), enables full-scale Re at 1:10 model
           - Expensive to operate, used for critical programs (787, A350)

        10. FLIGHT TEST CORRELATION:
            - Wind tunnel + CFD → flight test validation
            - Discrepancies: Re effects, tunnel interference, installation effects (engines, pylons)
            - Typical: wind tunnel within 5% drag, 10% CLmax of flight test
        """,
        key_factors=[
            "Reynolds number: match critical for BL transition, separation, CLmax",
            "Mach number: match critical for compressibility, shock position, wave drag",
            "Blockage: model < 5% tunnel area to minimize corrections",
            "Wall type: slotted for transonic, solid for low-speed, open-jet for external flows",
            "Turbulence level: low Tu for laminar flow research, moderate for transition studies",
            "Balance accuracy: 6-component, ±0.5% forces, ±0.1° angles"
        ],
        primary_authority=[
            "Barlow, Rae, & Pope, Low-Speed Wind Tunnel Testing (3rd ed.), Wiley, 1999",
            "Anderson, Fundamentals of Aerodynamics (6th ed.), McGraw-Hill, 2017 (Chapter 4)",
            "NASA SP-440, The Role of Flight Testing in Aerospace (1976)"
        ],
        burden_holder="Test engineer must account for scaling effects, apply corrections, validate with flight test",
        adversary_position="CFD has replaced wind tunnels; testing is legacy, expensive, unnecessary",
        counter_arguments=[
            "CFD limitations: turbulence modeling, separation prediction, grid resolution at high Re",
            "Wind tunnel validation: Boeing 787, A350, F-35 all wind tunnel tested (1000+ hours)",
            "Cost: $10M wind tunnel campaign vs $100M+ flight test program rework if issues found late",
            "Unsteady flows: buffet, flutter, dynamic stall require physical testing or very advanced CFD",
            "Flight test risk: discovering issues in flight is dangerous, expensive, schedule-impacting"
        ],
        resolution_strategy="Use wind tunnel for design validation, CFD for optimization, flight test for final verification; match Re/M as closely as possible, apply empirical corrections",
        entity_scope="All aircraft development (GA, transport, military), UAVs, automotive, sports aerodynamics",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Wind tunnel methods validated over 100+ years, extensive correlation databases, standard practice",
        controlling_precedent=[
            "Wright Brothers wind tunnel (1901)",
            "NACA/NASA wind tunnel programs (1920s-present)",
            "FAA/EASA accept wind tunnel data for certification with flight test validation"
        ],
        category=IssueCategory.TESTING_CFD
    ),

    DoctrineBlock(
        topic="Ground Effect: Reduced Induced Drag, Increased Lift",
        keywords=["ground effect", "wing-in-ground", "induced drag", "floating"],
        conclusion_template=[
            "Ground effect reduces induced drag and increases lift when height < wingspan, significant below 0.5 wingspan.",
            "Wing-in-ground (WIG) craft exploit ground effect for high L/D (20-40), efficient high-speed water/land transport.",
            "Pilots must anticipate ground effect: aircraft floats during landing, requires higher AoA after liftoff to maintain climb."
        ],
        reasoning_framework="""
        1. PHYSICAL MECHANISM:
           - Trailing vortex system weakened by ground proximity (vortices can't develop fully)
           - Downwash reduced: effective AoA increases, lift increases for same geometric AoA
           - Induced drag decreases: CDi ∝ (downwash)², ground effect cuts downwash, cuts CDi
           - Effect strongest at h/b < 0.5 (height / wingspan < 50%)

        2. LIFT INCREASE:
           - CL increases 10-20% in ground effect (h/b < 0.1)
           - Effective AoA increase: Δα ≈ 1-2° at h/b = 0.1
           - Enables flight at lower speed than out of ground effect (OGE)
           - Tail downwash also reduced: elevator effectiveness changes

        3. DRAG REDUCTION:
           - Induced drag decreases 50-70% at h/b = 0.05 (very low)
           - CDi,IGE / CDi,OGE ≈ (16·h/b)² / [1 + (16·h/b)²], empirical formula
           - At h/b = 0.1: CDi reduced ~40%
           - Parasitic drag unchanged (pressure, friction same)

        4. TAKEOFF / LANDING EFFECTS:
           - Takeoff: aircraft lifts off in ground effect, accelerates, climbs OGE
           - Rotation: adequate speed required, if Vr too low, may not climb OGE (sinks back)
           - Landing: aircraft floats (more lift, less drag), touchdown farther down runway
           - Technique: reduce power smoothly, increase AoA gradually, land in 1/3 of float distance

        5. WING-IN-GROUND (WIG) CRAFT:
           - Ekranoplan (Soviet): 300+ knot, 500+ ton capacity, flies at 10-20 ft above water
           - L/D: 20-40 in ground effect (vs 15-20 for aircraft OGE), highly efficient
           - Stability: pitch instability when leaving ground effect (nose up → climb → lose effect → sink)
           - Regulations: IMO classifies as marine vessel (not aircraft), limited adoption

        6. RAM WING EFFECT:
           - High-pressure air trapped between wing and ground (ram pressure)
           - Adds to lift, especially for low AR wings close to ground
           - Combined with vortex reduction, explains WIG high L/D

        7. REVERSE GROUND EFFECT (DIFFUSER):
           - Race cars: undertray / diffuser creates low pressure, increases downforce
           - Ground proximity essential: downforce ∝ 1/(h²), doubling height cuts downforce 75%
           - Aerodynamic principle same as wing ground effect, but inverted (downforce, not lift)
        """,
        key_factors=[
            "Height ratio h/b: effect significant < 0.5, strong < 0.2, dramatic < 0.1",
            "Induced drag reduction: 40-70% at low heights (h/b < 0.1)",
            "Lift increase: 10-20%, enables lower stall speed in ground effect",
            "Aspect ratio: high AR wings (gliders) more sensitive to ground effect than low AR",
            "Takeoff rotation: adequate Vr to ensure OGE climb, not just IGE liftoff",
            "Landing float: plan for 10-20% longer landing roll due to ground effect"
        ],
        primary_authority=[
            "McCormick, Aerodynamics, Aeronautics, and Flight Mechanics (2nd ed.), Wiley, 1995",
            "Barber, Ground Effect on Aircraft and Automobile Aerodynamics, SAE, 1984",
            "Rozhdestvensky, Wing-in-Ground Effect Vehicles, Progress in Aerospace Sciences, 2006"
        ],
        burden_holder="Pilot must account for ground effect in takeoff/landing technique; designer considers for V-speeds",
        adversary_position="Ground effect is minor, negligible for normal operations",
        counter_arguments=[
            "Accidents: inadequate Vr, pilot lifts off in ground effect, cannot climb OGE, crashes (runway overrun, obstacle strike)",
            "Landing: failure to anticipate float causes long landing, runway excursion (especially short fields)",
            "WIG craft: demonstrated practical application, Soviet ekranoplans operated for decades",
            "Helicopter IGE hover: 15-25% power reduction, critical for high-altitude, hot-day operations",
            "FAA guidance: POH/AFM must account for ground effect in performance charts"
        ],
        resolution_strategy="Train pilots on ground effect (float, rotation speed), design V-speeds with margin, exploit for WIG applications where feasible",
        entity_scope="All aircraft (especially low-wing), WIG craft, helicopters, race cars (inverted)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Ground effect well-understood since 1920s, flight test validated, incorporated in all performance models",
        controlling_precedent=[
            "NACA research on ground effect (1930s-1950s)",
            "WIG craft development (Soviet ekranoplans, 1960s-1990s)",
            "14 CFR Part 23/25 performance charts include ground effect"
        ],
        category=IssueCategory.GROUND_EFFECT
    ),

    DoctrineBlock(
        topic="Atmospheric Effects: Density Altitude, Wind Shear, Icing",
        keywords=["density altitude", "wind shear", "icing", "performance degradation"],
        conclusion_template=[
            "Density altitude DA = pressure altitude + 120(OAT - ISA), high DA degrades performance (takeoff, climb, landing).",
            "Wind shear (sudden change in wind direction/speed) causes airspeed changes, energy loss, possible loss of control during critical phases.",
            "Icing increases drag 20-40%, decreases lift 30%, disrupts airflow, causes loss of control; anti-ice/de-ice systems or avoidance required."
        ],
        reasoning_framework="""
        1. DENSITY ALTITUDE:
           - Standard atmosphere: 59°F (15°C) at sea level, -3.57°F per 1000 ft (ISA)
           - Density altitude: pressure altitude corrected for non-standard temperature
           - High DA (hot, high elevation): thin air, low ρ, reduced lift, thrust, propeller efficiency
           - Example: 5000 ft airport, 95°F → DA ≈ 9000 ft (double performance degradation)
           - Effects: longer takeoff roll (20-50%), lower climb rate (50%+), reduced engine power (3% per 1000 ft DA)

        2. TAKEOFF PERFORMANCE DEGRADATION:
           - Takeoff distance ∝ ρ⁻¹ (halve density → double distance, approximately)
           - Climb rate ∝ (T-D), but T ∝ ρ, so climb rate drops drastically
           - Hot, high, heavy: worst case (density altitude + weight, limited runway)
           - Rule of thumb: add 10-15% takeoff distance per 1000 ft DA above sea level

        3. WIND SHEAR:
           - Microburst: downdraft from thunderstorm, spreads radially near ground
           - Performance-decreasing shear: headwind → tailwind, or downdraft
           - Energy equation: ½V² - ½(V-ΔV)² ≈ V·ΔV, lose kinetic energy, sink
           - Recovery: max thrust, minimize pitch change (don't trade speed for altitude)
           - Avoidance: low-level wind shear alert systems (LLWAS), Doppler radar, go-around if suspected

        4. ICING:
           - Supercooled water droplets (0°C to -40°C) freeze on impact, accumulate on leading edges
           - Effects: disrupted airflow (rough surface), increased drag (20-40%), decreased lift (30%+), increased weight
           - Types: rime (rough, white, light), clear (smooth, heavy, strong adhesion), mixed
           - Critical: tailplane stall (ice on horizontal stabilizer, flap extension → nose-down moment, elevator ineffective)
           - Anti-ice: prevents ice formation (heated leading edges, glycol spray), de-ice: removes ice (pneumatic boots)

        5. KNOWN ICING CONDITIONS:
           - Visible moisture + OAT 0°C to -20°C (worst -10°C to -15°C)
           - Regulations: cannot operate in known icing unless certified (14 CFR 91.527, Part 23/25 Appendix C/O)
           - Certification: demonstrate ice accretion, handling, system performance in icing wind tunnel + flight test
           - FIKI (Flight Into Known Icing): FAA certification, anti-ice systems on wings, tail, engine, windshield, pitot

        6. TURBULENCE:
           - Clear-air turbulence (CAT): high-altitude, no visual cues, jet stream, mountain waves
           - Convective: thunderstorms, severe up/downdrafts, hail, lightning
           - Mechanical: low-altitude, terrain, buildings, wake turbulence from large aircraft
           - Response: slow to Va (maneuvering speed) or turbulence penetration speed, reduce pitch inputs, maintain wings level

        7. WAKE TURBULENCE:
           - Trailing vortices from large aircraft, especially heavy jets on takeoff/landing
           - Strength ∝ weight, inversely ∝ speed (strongest: heavy, slow, clean config)
           - Duration: 2-3 minutes, drift with wind (crosswind hazard)
           - Avoidance: wait 2-3 min, stay above/upwind of preceding aircraft flight path
           - ATC separation: 3-6 nm depending on weight category, prevents most encounters
        """,
        key_factors=[
            "Density altitude: add 120 ft per °C above ISA for performance degradation estimate",
            "High DA: reduces climb rate 50%+, doubles takeoff roll, critical for mountain airports",
            "Wind shear: 10-knot headwind → tailwind loss = ~20 ft altitude loss or 10 knot airspeed loss",
            "Icing: 30% lift loss, 40% drag increase, elevator may be ineffective (tailplane stall)",
            "FIKI certification: required for intentional flight in known icing (Part 135, 121 ops)",
            "Wake turbulence: 3-6 nm separation, avoid by staying above/upwind of heavy's path"
        ],
        primary_authority=[
            "FAA Airplane Flying Handbook (FAA-H-8083-3C), Chapters 10, 11, 12",
            "14 CFR 91.527 (operating in icing conditions)",
            "AC 91-74B (Pilot Guide: Flight in Icing Conditions)",
            "AC 00-54 (Pilot Windshear Guide)"
        ],
        burden_holder="Pilot must assess atmospheric conditions, calculate performance, avoid hazardous wx or carry required equipment",
        adversary_position="Modern aircraft handle weather; these concerns are overblown",
        counter_arguments=[
            "Density altitude accidents: common in mountain West (Colorado, Utah, New Mexico), hot summer days",
            "Wind shear: Delta 191 (1985, microburst, 137 fatalities), led to LLWAS, training changes",
            "Icing: Colgan Air 3407 (2009, 50 fatalities), ice-contaminated tailplane stall, inadequate response",
            "Wake turbulence: fatal accidents behind heavy jets, especially light aircraft in trail",
            "Performance degradation real: POH charts show 2-3× takeoff distance at high DA vs sea level standard"
        ],
        resolution_strategy="Calculate performance at actual DA, not pressure altitude; avoid icing without FIKI cert; respect wind shear alerts; maintain wake turbulence separation",
        entity_scope="All aircraft, all operations, especially GA (less equipped than transport)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Atmospheric hazards documented in decades of accident reports, regulations based on data",
        controlling_precedent=[
            "14 CFR 91.527 (icing), 14 CFR 25.1419-1423 (ice protection)",
            "FAA Advisory Circulars on wind shear, icing, wake turbulence",
            "NTSB accident reports (Delta 191, Colgan 3407, numerous DA accidents)"
        ],
        category=IssueCategory.ATMOSPHERIC_EFFECTS
    ),
]


# ═══════════════════════════════════════════════════════════════════════════
# TELEMETRY & METRICS
# ═══════════════════════════════════════════════════════════════════════════

class TelemetryCollector:
    def __init__(self):
        self.records: List[TelemetryRecord] = []
        self.doctrine_triggers: Dict[str, int] = defaultdict(int)
        self.category_counts: Dict[IssueCategory, int] = defaultdict(int)

    def record_query(
        self,
        query: str,
        mode: ResponseMode,
        categories: List[IssueCategory],
        doctrines: List[str],
        cache_hit: bool,
        latency_ms: float,
        confidence: ConfidenceLevel,
        response_length: int
    ):
        record = TelemetryRecord(
            timestamp=datetime.now().isoformat(),
            query=query[:200],
            mode=mode,
            categories=categories,
            doctrines_triggered=doctrines,
            cache_hit=cache_hit,
            latency_ms=latency_ms,
            confidence=confidence,
            response_length=response_length
        )
        self.records.append(record)

        for doctrine in doctrines:
            self.doctrine_triggers[doctrine] += 1
        for category in categories:
            self.category_counts[category] += 1

        logger.info(f"Telemetry: {mode.value} query, {len(doctrines)} doctrines, {latency_ms:.1f}ms, confidence={confidence.value}")

    def get_metrics(self) -> Dict[str, Any]:
        if not self.records:
            return {"total_queries": 0}

        total = len(self.records)
        cache_hits = sum(1 for r in self.records if r.cache_hit)
        avg_latency = sum(r.latency_ms for r in self.records) / total

        return {
            "total_queries": total,
            "cache_hit_rate": cache_hits / total,
            "avg_latency_ms": round(avg_latency, 2),
            "top_doctrines": dict(sorted(self.doctrine_triggers.items(), key=lambda x: x[1], reverse=True)[:10]),
            "category_distribution": {k.value: v for k, v in self.category_counts.items()},
            "mode_distribution": {
                mode.value: sum(1 for r in self.records if r.mode == mode)
                for mode in ResponseMode
            }
        }


telemetry = TelemetryCollector()


# ═══════════════════════════════════════════════════════════════════════════
# THREE-LAYER RESPONSE ENGINE
# ═══════════════════════════════════════════════════════════════════════════

def match_doctrines(query: str) -> List[DoctrineBlock]:
    """Match query against doctrine cache."""
    query_lower = query.lower()
    matched = []

    for doctrine in DOCTRINE_CACHE:
        keyword_matches = sum(1 for kw in doctrine.keywords if kw in query_lower)
        if keyword_matches >= 2 or any(kw in query_lower for kw in doctrine.topic.lower().split()):
            matched.append(doctrine)
            doctrine.triggered_count += 1

    return sorted(matched, key=lambda d: d.triggered_count, reverse=True)[:5]


def three_layer_response(query: str, mode: ResponseMode) -> Dict[str, Any]:
    """
    TIE-20 Component: Three-layer response architecture
    Layer 1: Doctrine Cache (0-200ms)
    Layer 2: Semantic Retrieval (fallback, not implemented here - would use vector DB)
    Layer 3: Deep Analysis (full reasoning chain)
    """
    start = time.time()

    matched_doctrines = match_doctrines(query)
    cache_hit = len(matched_doctrines) > 0

    categories = list(set(d.category for d in matched_doctrines))
    confidence = matched_doctrines[0].confidence if matched_doctrines else ConfidenceLevel.DISCLOSURE

    if mode == ResponseMode.FAST:
        if matched_doctrines:
            response = {
                "answer": " ".join(matched_doctrines[0].conclusion_template),
                "doctrines": [d.topic for d in matched_doctrines],
                "confidence": confidence.value,
                "source": "doctrine_cache"
            }
        else:
            response = {
                "answer": "No direct doctrine match. Aerodynamics query requires more context. Please specify: subsonic/supersonic, lift/drag analysis, specific aircraft type, or flight regime.",
                "doctrines": [],
                "confidence": ConfidenceLevel.DISCLOSURE.value,
                "source": "fallback"
            }

    elif mode == ResponseMode.DEFENSE:
        if matched_doctrines:
            primary = matched_doctrines[0]
            response = {
                "executive_summary": " ".join(primary.conclusion_template),
                "reasoning_framework": primary.reasoning_framework,
                "key_factors": primary.key_factors,
                "primary_authority": primary.primary_authority,
                "controlling_precedent": primary.controlling_precedent,
                "confidence_stratification": primary.confidence_stratification,
                "adversary_position": primary.adversary_position,
                "counter_arguments": primary.counter_arguments,
                "resolution_strategy": primary.resolution_strategy,
                "doctrines_applied": [d.topic for d in matched_doctrines],
                "confidence": confidence.value,
                "source": "doctrine_cache"
            }
        else:
            response = {
                "executive_summary": "Insufficient data for defense-grade analysis.",
                "recommendation": "Specify aerodynamic regime (subsonic/transonic/supersonic), aircraft type, or problem domain for targeted analysis.",
                "confidence": ConfidenceLevel.DISCLOSURE.value,
                "source": "fallback"
            }

    else:  # MEMO
        if matched_doctrines:
            primary = matched_doctrines[0]
            memo_sections = {
                "title": f"Aerodynamics Analysis: {primary.topic}",
                "executive_summary": " ".join(primary.conclusion_template),
                "background": f"Analysis based on {len(matched_doctrines)} doctrine blocks covering {', '.join(c.value for c in categories)}.",
                "detailed_analysis": primary.reasoning_framework,
                "key_factors": primary.key_factors,
                "supporting_authority": primary.primary_authority,
                "risk_assessment": {
                    "confidence_level": confidence.value,
                    "stratification": primary.confidence_stratification,
                    "adversary_position": primary.adversary_position,
                    "counter_arguments": primary.counter_arguments
                },
                "recommendations": primary.resolution_strategy,
                "controlling_precedent": primary.controlling_precedent,
                "scope": primary.entity_scope,
                "related_doctrines": [d.topic for d in matched_doctrines[1:]]
            }
            response = memo_sections
        else:
            response = {
                "title": "Aerodynamics Query - Insufficient Doctrine Match",
                "executive_summary": "No cached doctrine blocks matched query terms.",
                "recommendation": "Refine query with specific terms: lift, drag, airfoil, boundary layer, stall, compressibility, supersonic, stability, performance, propeller, rotor, testing, ground effect, atmospheric effects.",
                "confidence": ConfidenceLevel.DISCLOSURE.value
            }

    latency_ms = (time.time() - start) * 1000

    telemetry.record_query(
        query=query,
        mode=mode,
        categories=categories,
        doctrines=[d.topic for d in matched_doctrines],
        cache_hit=cache_hit,
        latency_ms=latency_ms,
        confidence=confidence,
        response_length=len(str(response))
    )

    return response


def determinism_hash(data: Dict) -> str:
    """Generate SHA-256 hash for reproducibility verification."""
    canonical = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode()).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Aerodynamics question or analysis request")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")


class QueryResponse(BaseModel):
    result: Dict[str, Any]
    latency_ms: float
    determinism_hash: str
    engine_id: str = ENGINE_ID
    version: str = VERSION


class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrines_loaded: int
    total_queries: int
    cache_hit_rate: float
    uptime_seconds: float


# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    description="TIE Gold Standard - Real Aerodynamics & Flight Mechanics Expertise"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

startup_time = time.time()


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    """Main query endpoint - three-layer response with doctrine cache."""
    start = time.time()

    try:
        result = three_layer_response(req.query, req.mode)
        latency_ms = (time.time() - start) * 1000

        return QueryResponse(
            result=result,
            latency_ms=round(latency_ms, 2),
            determinism_hash=determinism_hash(result)
        )

    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """TIE-20 Component: Health endpoint with comprehensive status."""
    metrics = telemetry.get_metrics()

    return HealthResponse(
        status="operational",
        engine_id=ENGINE_ID,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        total_queries=metrics.get("total_queries", 0),
        cache_hit_rate=round(metrics.get("cache_hit_rate", 0.0), 3),
        uptime_seconds=round(time.time() - startup_time, 1)
    )


@app.get("/metrics")
async def get_metrics():
    """Detailed telemetry metrics."""
    return telemetry.get_metrics()


@app.get("/doctrines")
async def list_doctrines():
    """List all loaded doctrine blocks."""
    return {
        "total": len(DOCTRINE_CACHE),
        "categories": {cat.value: sum(1 for d in DOCTRINE_CACHE if d.category == cat) for cat in IssueCategory},
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords,
                "triggered_count": d.triggered_count,
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }


@app.get("/")
async def root():
    """Engine info."""
    return {
        "engine": ENGINE_NAME,
        "id": ENGINE_ID,
        "version": VERSION,
        "port": PORT,
        "doctrines": len(DOCTRINE_CACHE),
        "categories": len(IssueCategory),
        "endpoints": ["/query", "/health", "/metrics", "/doctrines"],
        "status": "operational"
    }


# ═══════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks across {len(IssueCategory)} categories")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=PORT,
        log_level="info"
    )
