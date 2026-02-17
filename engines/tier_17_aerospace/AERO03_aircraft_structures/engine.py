import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

"""
AERO03 - Aircraft Structures & Materials Intelligence Engine
Port: 9073
Version: 1.0.0

Provides expert analysis of aircraft structural design, materials science, stress analysis,
fatigue, fracture mechanics, composites, metallurgy, corrosion, NDT, and certification.
"""

import asyncio
import hashlib
import json
import time
from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

ENGINE_ID = "AERO03"
ENGINE_NAME = "Aircraft Structures & Materials Engine"
VERSION = "1.0.0"
PORT = 9073

logger.add(
    f"logs/{ENGINE_ID}_{{time}}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)


# ═══════════════════════════════════════════════════════════════════════════
# ENUMS
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
    STRUCTURAL_DESIGN = "STRUCTURAL_DESIGN"
    STRESS_ANALYSIS = "STRESS_ANALYSIS"
    FATIGUE_ANALYSIS = "FATIGUE_ANALYSIS"
    FRACTURE_MECHANICS = "FRACTURE_MECHANICS"
    COMPOSITE_MATERIALS = "COMPOSITE_MATERIALS"
    METALLIC_MATERIALS = "METALLIC_MATERIALS"
    CORROSION = "CORROSION"
    NDT_INSPECTION = "NDT_INSPECTION"
    STRUCTURAL_REPAIR = "STRUCTURAL_REPAIR"
    CERTIFICATION = "CERTIFICATION"
    PRESSURIZED_STRUCTURES = "PRESSURIZED_STRUCTURES"
    WING_STRUCTURES = "WING_STRUCTURES"


# ═══════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════

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
    category: IssueCategory


class QueryRequest(BaseModel):
    query: str = Field(..., description="Aircraft structures/materials question")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class QueryResponse(BaseModel):
    query: str
    mode: ResponseMode
    answer: str
    confidence: ConfidenceLevel
    sources: List[str]
    reasoning_chain: Optional[List[str]] = None
    related_topics: List[str]
    determinism_hash: str
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_response_time_ms: float


# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ PRE-COMPILED EXPERT REASONING BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="safe_life_design_philosophy",
        keywords=["safe life", "design philosophy", "structural design", "finite life", "retirement life"],
        conclusion_template=[
            "Safe-life design requires structure to withstand design loads without failure for specified service life.",
            "Component must be retired at predetermined life limit regardless of condition.",
            "Design accounts for fatigue, corrosion, and stress through conservative factors and testing."
        ],
        reasoning_framework="""Safe-life design is one of three fundamental structural design philosophies (safe-life, fail-safe, damage tolerant).
In safe-life approach, the structure is designed and tested to demonstrate it can withstand all anticipated loads throughout
its specified service life without failure. Key principles: (1) Conservative design factors applied to all loads, (2) Full-scale
fatigue testing to 2x design service life minimum, (3) Mandatory retirement at life limit (e.g., 50,000 flight hours),
(4) No credit taken for inspections or repairs. This philosophy was dominant in early jet aircraft (1950s-1960s) but has
largely been superseded by damage tolerant design for primary structures. Still used for landing gear, engine mounts, and
other components where multiple load paths or inspectability are impractical. FAA AC 25.571-1D defines safe-life as
"a design that substantiates that catastrophic failure due to fatigue, corrosion, or accidental damage is avoided throughout
the operational life of the airplane by removal at an approved life limit." Critical distinction from fail-safe: safe-life
assumes zero defects at manufacture and no in-service damage detection, therefore requires complete component replacement
at life limit. Economic impact is high due to premature replacement of serviceable parts. Design validation requires
extensive testing: static ultimate load test (1.5x limit load), fatigue testing to demonstrate scatter factor (typically
4x expected life), environmental testing for corrosion effects, and spectrum loading representing operational usage.""",
        key_factors=[
            "Finite service life with mandatory retirement",
            "Conservative design factors (1.5x limit load for ultimate)",
            "Full-scale fatigue testing to 2x+ design life",
            "No credit for inspections or damage detection",
            "Zero defect assumption at manufacture",
            "High replacement cost at life limit",
            "Used for non-inspectable or single-load-path components"
        ],
        primary_authority=[
            "14 CFR 25.571 - Damage Tolerance and Fatigue Evaluation",
            "AC 25.571-1D - Damage Tolerance and Fatigue Evaluation",
            "MIL-STD-1530D - Aircraft Structural Integrity Program",
            "FAA Order 8110.4C - Type Certification"
        ],
        burden_holder="Manufacturer",
        adversary_position="Operator seeks extended service life beyond design limit",
        counter_arguments=[
            "Conservative factors already account for uncertainty",
            "In-service inspections reveal no damage or defects",
            "Economic burden of premature replacement",
            "Statistical analysis shows component still safe"
        ],
        resolution_strategy="Safe-life limits are non-negotiable absent new certification basis. Extension requires full re-analysis and testing per 25.571, treating it as new type design. Manufacturer must demonstrate additional life with same confidence level (typically 99.9% probability of survival). Requires: metallurgical analysis of retired parts, fractography, updated fatigue spectrum, additional testing, and FAA approval via amended type certificate. Alternative is conversion to damage tolerant approach with inspections.",
        entity_scope="Transport category aircraft (Part 25), commuter aircraft (Part 23)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - well-established regulatory framework and 70+ years operational experience",
        controlling_precedent="AC 25.571-1D Section 5.2 - Safe-Life Evaluation",
        category=IssueCategory.STRUCTURAL_DESIGN
    ),

    DoctrineBlock(
        topic="fail_safe_design_philosophy",
        keywords=["fail safe", "redundant structure", "multiple load paths", "load redistribution", "residual strength"],
        conclusion_template=[
            "Fail-safe design provides multiple load paths so partial failure does not lead to catastrophic outcome.",
            "Structure must sustain design loads with one element failed for sufficient period to detect damage.",
            "Design incorporates crack arresters, tear straps, and redundant members."
        ],
        reasoning_framework="""Fail-safe design ensures that partial failure of a structural element does not result in
catastrophic failure of the entire structure. Achieved through: (1) Multiple load paths - load can redistribute to alternate
paths if one fails, (2) Crack arresters - features that stop crack propagation (tear straps, thick sections, material changes),
(3) Residual strength - structure maintains adequate strength with damage for inspection interval. Classic example: pressurized
fuselage with longitudinal stringers, circumferential frames, and tear straps. If skin cracks between two stringers, frames
and adjacent stringers carry load until next inspection. FAA requires demonstration that structure with "obvious" damage can
withstand limit load (1.0g). Key regulatory requirement: structure must maintain required residual strength for period between
inspections, typically linked to inspection interval and detectability. More economical than safe-life because components
need not be retired at arbitrary limit - continue in service with inspection program. However, requires inspectability and
access. Common in fuselage structures, wing skins, and control surfaces. Design validation: demonstrate by analysis or test
that single-element failure allows load redistribution without exceeding ultimate stress in remaining structure, and that
damage is detectable within inspection interval at stress levels that maintain required residual strength.""",
        key_factors=[
            "Multiple independent load paths",
            "Crack arresters (tear straps, frame/stringer grids)",
            "Residual strength requirement with damage",
            "Inspectability and damage detectability",
            "Load redistribution capability",
            "Inspection interval tied to damage growth rate",
            "Economic - no mandatory retirement"
        ],
        primary_authority=[
            "14 CFR 25.571(b) - Fail-safe evaluation",
            "AC 25.571-1D Section 5.3 - Fail-Safe Evaluation",
            "AC 20-107B - Composite Aircraft Structure",
            "Boeing D6-82479 - Fail-Safe Design Handbook"
        ],
        burden_holder="Manufacturer",
        adversary_position="Single load path more weight-efficient, claim inspections unnecessary",
        counter_arguments=[
            "Weight penalty of redundant structure reduces performance",
            "Modern materials and analysis reduce failure probability",
            "Cost of inspection program exceeds benefit",
            "Statistical analysis shows low failure rate"
        ],
        resolution_strategy="Fail-safe is mandatory for transport category primary structures per 25.571. No exceptions for weight or cost. If single load path is unavoidable (e.g., main landing gear trunnion), must use damage tolerant approach with frequent inspections. For composite structures where multiple load paths difficult to achieve, damage arrest features (ply drops, toughened interlayers) required. Demonstrate residual strength with discrete source damage per AC 20-107B.",
        entity_scope="Transport category aircraft primary structures",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Foundational requirement - no regulatory flexibility",
        controlling_precedent="AC 25.571-1D Section 5.3.1 - Fail-safe criteria must be met for all flight conditions",
        category=IssueCategory.STRUCTURAL_DESIGN
    ),

    DoctrineBlock(
        topic="damage_tolerant_design",
        keywords=["damage tolerance", "fatigue crack growth", "inspection intervals", "slow crack growth", "residual strength"],
        conclusion_template=[
            "Damage tolerant design assumes flaws exist and ensures safe operation through inspections.",
            "Structure must tolerate damage detectable by scheduled inspections until repaired.",
            "Crack growth analysis determines inspection intervals to maintain structural safety."
        ],
        reasoning_framework="""Damage tolerance is the current standard for transport aircraft primary structures,
mandated by FAA after Aloha Airlines Flight 243 fuselage failure (1988). Philosophy: assume initial manufacturing defects
and in-service damage exist; design structure and inspection program to ensure cracks detected and repaired before reaching
critical size. Four-step process: (1) Define initial flaw sizes (based on NDT detectability: 0.05 inch surface crack, 0.10 inch corner
crack typical), (2) Analyze crack growth under operational spectrum loading using fracture mechanics (Paris law: da/dN = C(ΔK)^m),
(3) Determine inspection intervals based on crack growth to critical size with safety factors, (4) Establish supplemental
inspection programs (SIP/SSI). AC 25.571-1D requires damage tolerance evaluation for PSE (principal structural elements)
showing structure can tolerate threshold damage (based on NDT limit of detection) for two inspection intervals. Critical crack
length determined by residual strength requirement: structure with maximum expected damage must withstand limit load.
Inspection interval = (crack growth life from threshold to critical) / (safety factor x 2). Safety factors account for:
scatter in crack growth rates (typically 2x), load spectrum uncertainty, and NDT reliability. Aging aircraft programs (AAWG)
extend damage tolerance to widespread fatigue damage (WFD) - must prevent simultaneous failure of multiple elements.""",
        key_factors=[
            "Initial flaw assumption based on NDT capability",
            "Fracture mechanics crack growth analysis (Paris law)",
            "Two-lifetime inspection interval requirement",
            "Residual strength with limit load and damage",
            "Safety factors for scatter and uncertainty",
            "Widespread fatigue damage (WFD) prevention",
            "Supplemental inspection programs mandatory"
        ],
        primary_authority=[
            "14 CFR 25.571(a) - Damage tolerance evaluation mandatory",
            "AC 25.571-1D - Complete DT methodology",
            "FAA Order 8100.8 - Aging Aircraft Program",
            "ASTM E647 - Fatigue Crack Growth Testing"
        ],
        burden_holder="Manufacturer and operator (shared)",
        adversary_position="Perfect manufacturing and QC eliminate initial flaws",
        counter_arguments=[
            "Modern manufacturing has zero defects claim",
            "Statistical analysis shows low crack probability",
            "Inspection costs outweigh risk",
            "Probabilistic approach sufficient without DT"
        ],
        resolution_strategy="Damage tolerance is non-negotiable for Part 25 aircraft per 25.571(a). Zero-defect claim rejected by Aloha accident evidence and metallurgical studies showing ubiquitous manufacturing flaws below NDT threshold. Inspection program is not optional - required for continued airworthiness per 25.1529. Economic argument irrelevant to safety mandate. If operator refuses inspections, airworthiness certificate revoked per 39.3. Alternative: prove component is fail-safe with multiple load paths, eliminating single-point failure mode.",
        entity_scope="All Part 25 aircraft, principal structural elements",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Absolute regulatory requirement post-1998",
        controlling_precedent="AC 25.571-1D Section 6 - Damage Tolerance Evaluation Process",
        category=IssueCategory.FATIGUE_ANALYSIS
    ),

    DoctrineBlock(
        topic="stress_analysis_methods",
        keywords=["stress analysis", "tension", "compression", "shear", "bending", "torsion", "combined loading", "von Mises"],
        conclusion_template=[
            "Structural stress analysis determines internal forces and stresses under applied loads.",
            "Combined loading requires interaction equations or von Mises criterion for failure prediction.",
            "Margin of safety must be positive (MS = Allowable/Applied - 1 >= 0) for structural adequacy."
        ],
        reasoning_framework="""Stress analysis is fundamental to structural design, quantifying internal forces and stresses
to ensure strength requirements are met. Six basic stress states: (1) Tension (axial load, uniform stress σ = P/A),
(2) Compression (buckling critical for slender members, Euler equation for columns), (3) Shear (τ = V/A, important in webs
and fasteners), (4) Bending (σ = My/I, critical in beams/spars), (5) Torsion (τ = Tr/J, critical in shafts/fuselages),
(6) Combined loading (real structures experience multiple simultaneous stresses). For combined loading, interaction equations
or failure criteria required: Von Mises (yield): σ_vm = √(σ_x² + σ_y² - σ_x·σ_y + 3τ²) <= σ_yield; Maximum shear (Tresca):
τ_max = (σ_1 - σ_3)/2 <= τ_yield; Principal stress: σ_1,2 = (σ_x + σ_y)/2 +/- √((σ_x - σ_y)²/4 + τ²). Margin of safety:
MS = (F_allow / F_applied) - 1, where F is stress, load, or strain. Positive MS required; MS = 0 is limit (exactly at allowable);
MS < 0 is failure. Ultimate factor of safety = 1.5 for Part 25 (ultimate load = 1.5 x limit load). Modern analysis uses
finite element analysis (FEA) for complex geometries, but hand calculations still required for verification and engineering
judgment. Material allowables from MIL-HDBK-5 (now MMPDS) provide A-basis (99% probability, 95% confidence) and B-basis
(90%/95%) values. Temperature effects critical - aluminum loses 50% strength at 300°F, titanium stable to 600°F.""",
        key_factors=[
            "Six basic stress states (tension, compression, shear, bending, torsion, combined)",
            "Von Mises criterion for ductile materials (aluminum, titanium)",
            "Maximum shear (Tresca) for brittle materials",
            "Margin of safety MS = Allowable/Applied - 1 >= 0",
            "Ultimate factor of safety 1.5 for Part 25",
            "Material allowables from MMPDS (MIL-HDBK-5)",
            "Temperature degradation of strength"
        ],
        primary_authority=[
            "14 CFR 25.303 - Factor of safety",
            "14 CFR 25.305 - Strength and deformation",
            "MMPDS (Metallic Materials Properties Development and Standardization)",
            "Bruhn 'Analysis and Design of Flight Vehicle Structures'"
        ],
        burden_holder="Design engineer",
        adversary_position="FEA sufficient without hand calculations",
        counter_arguments=[
            "Modern FEA more accurate than hand methods",
            "Hand calculations too conservative waste weight",
            "Computer analysis faster and cheaper",
            "Legacy methods outdated for complex structures"
        ],
        resolution_strategy="FEA is powerful tool but not substitute for engineering judgment. FAA requires rational analysis, not blind computer output. Hand calculations validate FEA models, check for gross errors, and provide physical insight. AC 20-107B requires verification of FEA results through test or independent analysis. For certification, both approaches complement each other: hand calc for simple elements and validation, FEA for complex geometries and load distributions. MS < 0 from either method is certification finding requiring redesign or test substantiation.",
        entity_scope="All aircraft structures",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Fundamental engineering principles with 100+ years validation",
        controlling_precedent="Bruhn Chapter C7 - Combined Stresses",
        category=IssueCategory.STRESS_ANALYSIS
    ),

    DoctrineBlock(
        topic="fatigue_life_prediction_SN_curves",
        keywords=["fatigue", "S-N curve", "stress-life", "endurance limit", "Miner's rule", "cumulative damage"],
        conclusion_template=[
            "S-N curves relate stress amplitude to fatigue life (cycles to failure) for constant amplitude loading.",
            "Miner's rule sums cumulative damage fractions (n/N) for variable amplitude spectrum loading.",
            "Fatigue failure occurs when Σ(n_i/N_i) >= 1.0, where n_i is applied cycles and N_i is cycles to failure."
        ],
        reasoning_framework="""Stress-life (S-N) approach is classical method for high-cycle fatigue analysis (>10^4 cycles).
S-N curve plots stress amplitude (S) vs. cycles to failure (N) on log-log scale. Key features: (1) Finite life region - stress
above endurance limit, failure in finite cycles, (2) Endurance limit - stress below which infinite life expected (ferrous
metals ~40% UTS; aluminum has NO true endurance limit but practical limit ~10^8 cycles), (3) Low cycle fatigue (<10^4 cycles)
- strain-life approach more appropriate. S-N curves developed from rotating beam tests (R=-1 fully reversed bending) or
axial tests at various stress ratios (R = σ_min/σ_max). Mean stress effects significant: tensile mean stress reduces fatigue
life, compressive mean stress increases life. Corrections: Goodman diagram (linear), Gerber (parabolic), Soderberg (conservative).
For variable amplitude loading (aircraft operational spectrum), Miner's rule (Palmgren-Miner linear damage hypothesis):
D = Σ(n_i/N_i), where n_i = applied cycles at stress S_i, N_i = cycles to failure at S_i from S-N curve. Failure when D >= 1.0.
Limitations: (1) No account for load sequence effects, (2) Linear assumption may not reflect actual damage accumulation,
(3) Does not predict crack initiation vs. propagation. Despite limitations, widely used for preliminary design. More accurate
methods: strain-life approach (Coffin-Manson) for low-cycle fatigue, fracture mechanics for crack propagation. Aircraft spectra
complex - count cycles using rainflow method to extract stress ranges from irregular time history.""",
        key_factors=[
            "S-N curve from material testing at specific R-ratio",
            "Endurance limit (ferrous) vs. practical limit (aluminum ~10^8 cycles)",
            "Mean stress corrections (Goodman, Gerber, Soderberg)",
            "Miner's rule: D = Σ(n_i/N_i), failure at D >= 1.0",
            "Rainflow counting for variable amplitude spectra",
            "Load sequence effects not captured",
            "Conservative for design, not predictive for crack growth"
        ],
        primary_authority=[
            "MIL-STD-1530D - ASIP standard fatigue methodology",
            "ASTM E466 - Constant Amplitude Fatigue Testing",
            "AC 25.571-1D Section 7 - Fatigue evaluation",
            "MMPDS Chapter 9 - Fatigue data"
        ],
        burden_holder="Design engineer",
        adversary_position="Single high load invalidates Miner's rule",
        counter_arguments=[
            "Load sequence effects cause non-linear damage",
            "High load creates beneficial residual stress",
            "Miner's rule non-conservative for certain spectra",
            "Crack initiation vs propagation not distinguished"
        ],
        resolution_strategy="Miner's rule is accepted engineering practice for preliminary fatigue design despite known limitations. FAA accepts D < 1.0 with scatter factor (typically 4x on life or 2x on stress). For critical structures, supplement with: (1) Fracture mechanics analysis for crack growth, (2) Full-scale fatigue testing to validate analysis, (3) Conservative scatter factors to account for sequence effects. If challenger claims non-conservatism, burden shifts to prove alternative method is more accurate through testing or service experience. Single overload effects can be accounted through retardation models (Wheeler, Willenborg) in fracture mechanics analysis.",
        entity_scope="All fatigue-critical structures",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Widely used but known limitations - supplement with testing",
        controlling_precedent="AC 25.571-1D requires both S-N and fracture mechanics for complete evaluation",
        category=IssueCategory.FATIGUE_ANALYSIS
    ),

    DoctrineBlock(
        topic="fracture_mechanics_paris_law",
        keywords=["fracture mechanics", "stress intensity factor", "Paris law", "crack growth rate", "critical crack length", "da/dN"],
        conclusion_template=[
            "Paris law describes fatigue crack growth rate: da/dN = C(ΔK)^m, where ΔK is stress intensity range.",
            "Critical crack length occurs when K_I = K_Ic (fracture toughness) at maximum applied stress.",
            "Crack growth life integrates Paris law from initial flaw to critical size: N = ∫(da / C(ΔK)^m)."
        ],
        reasoning_framework="""Fracture mechanics is the foundation of damage tolerant design, analyzing crack growth and
residual strength. Stress intensity factor K quantifies crack-tip stress field: K = σ√(πa) x β, where σ = applied stress,
a = crack length, β = geometry correction factor (depends on crack type, structure geometry, loading). Three modes: Mode I
(opening, most critical), Mode II (sliding shear), Mode III (tearing shear). Failure criterion: K_I >= K_Ic (plane strain
fracture toughness). Paris law describes subcritical crack growth under cyclic loading: da/dN = C(ΔK)^m, where da/dN = crack
growth rate (inches/cycle), ΔK = K_max - K_min (stress intensity range), C and m = material constants from testing (m typically
2-4 for aluminum). Three regions on log(da/dN) vs log(ΔK) plot: Region I (threshold, ΔK_th ~2-3 ksi√in for aluminum, no
growth below), Region II (Paris region, linear on log-log plot, stable growth), Region III (unstable, approaching K_Ic).
Critical crack size: a_crit where K_I(σ_max, a_crit) = K_Ic. Residual strength: σ_residual = K_Ic / (β√(πa)). Crack growth
integration: N = ∫[a_i to a_f] da / [C(ΔK)^m], typically solved numerically using block integration or closed-form if β constant.
For variable amplitude loading, cycle-by-cycle integration with retardation models (overloads slow crack growth). Material
properties from testing per ASTM E399 (K_Ic), ASTM E647 (da/dN curves). Inspection interval = N_growth / (2 x scatter factor).""",
        key_factors=[
            "Stress intensity factor K = σ√(πa) x β",
            "Paris law: da/dN = C(ΔK)^m",
            "Fracture toughness K_Ic (material property)",
            "Critical crack length where K = K_Ic",
            "Threshold ΔK_th (no growth below)",
            "Crack growth integration for life prediction",
            "Residual strength decreases with crack growth"
        ],
        primary_authority=[
            "ASTM E399 - K_Ic fracture toughness testing",
            "ASTM E647 - Fatigue crack growth rate testing",
            "AC 25.571-1D Section 8 - Crack growth analysis",
            "NASGRO database - Crack growth properties"
        ],
        burden_holder="Damage tolerance analyst",
        adversary_position="Initial flaw assumption too large reduces economic life",
        counter_arguments=[
            "Modern QC ensures no defects at manufacture",
            "Initial flaw size overly conservative",
            "Material improvements reduce crack growth rates",
            "Probabilistic approach more realistic than deterministic"
        ],
        resolution_strategy="Initial flaw size is based on NDT limit of detection (LOD), not manufacturing capability. AC 25.571-1D specifies 0.05 inch surface crack, 0.10 inch corner crack for eddy current inspection as typical thresholds. These are not assumed defect sizes but detection capability limits. Even with perfect manufacturing, assume flaw at threshold because: (1) NDT cannot guarantee zero defects below LOD, (2) In-service damage (corrosion, impact) creates new flaws, (3) Regulatory conservatism for safety. Probabilistic fracture mechanics (PFM) allowed but must demonstrate equivalent safety level to deterministic approach. Material improvements (7050-T7451 vs 7075-T6) reduce C value or increase K_Ic, but Paris law framework unchanged. Economic argument rejected - safety mandate requires conservative assumptions.",
        entity_scope="Damage tolerance evaluation of PSE",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established theory with 50+ years application and validation",
        controlling_precedent="AC 25.571-1D Section 8.2 - Paris law integration is standard method",
        category=IssueCategory.FRACTURE_MECHANICS
    ),

    DoctrineBlock(
        topic="composite_materials_carbon_fiber",
        keywords=["composites", "carbon fiber", "CFRP", "layup", "laminate", "ply orientation", "0/90/+/-45"],
        conclusion_template=[
            "Carbon fiber composites offer high strength-to-weight ratio but are anisotropic and notch-sensitive.",
            "Layup design balances load requirements using 0°, 90°, and +/-45° plies for tension, compression, and shear.",
            "Out-of-plane loads (through-thickness) are weak due to matrix-dominated properties."
        ],
        reasoning_framework="""Carbon fiber reinforced polymers (CFRP) are dominant in modern aircraft primary structures
(Boeing 787, Airbus A350, F-22/F-35). Advantages: (1) High specific strength (strength/density) - 3-5x aluminum, (2) High
specific stiffness, (3) Fatigue resistance superior to metals, (4) Corrosion immunity, (5) Tailorable properties through
ply orientation. Disadvantages: (1) Anisotropic - properties vary by direction, (2) Notch-sensitive - stress concentrations
more critical than metals, (3) Through-thickness weakness - matrix-dominated, (4) Impact damage tolerance lower than metals,
(5) Environmental sensitivity (moisture, temperature), (6) Galvanic corrosion with aluminum, (7) High material and labor cost.
Typical prepreg tape: unidirectional fibers (60% volume fraction) in epoxy matrix. Fiber: T300, T800, IM7 (increasing modulus).
Matrix: 350°F cure (moderate performance) vs 350°F cure (high performance). Layup design: Orient plies to match load paths.
0° plies carry axial tension/compression (fiber-dominated, E ~20 Msi). 90° plies carry transverse loads. +/-45° plies carry
shear (matrix-dominated, lower strength). Quasi-isotropic layup [0/+/-45/90] provides balanced in-plane properties. Symmetry
required to prevent warping - [0/90]s not [0/90]. Stacking sequence affects: interlaminar stresses, delamination resistance,
damage tolerance. Design rules: no more than 4 plies same orientation consecutive, +/-45° plies on surface for impact resistance,
10% rule (min 10% of plies in each direction 0/90/+/-45). Thickness buildup by 0.005 inch per ply typical. Analysis: laminated
plate theory (ABD matrices), classical lamination theory, or FEA with layered shell elements.""",
        key_factors=[
            "High specific strength/stiffness (3-5x aluminum)",
            "Anisotropic - properties vary by direction",
            "Fiber-dominated (0°) vs matrix-dominated (90°, +/-45°)",
            "Quasi-isotropic layup [0/+/-45/90] for balanced properties",
            "Symmetry and 10% rule for each direction",
            "Notch-sensitive - fastener holes critical",
            "Galvanic corrosion with aluminum - isolation required"
        ],
        primary_authority=[
            "AC 20-107B - Composite Aircraft Structure",
            "CMH-17 (formerly MIL-HDBK-17) - Composite materials handbook",
            "ASTM D3039 - Tensile testing of composites",
            "Boeing BSS 7260 - Carbon fiber prepreg specification"
        ],
        burden_holder="Composite structures engineer",
        adversary_position="Composite superior to aluminum in all respects",
        counter_arguments=[
            "Higher strength allows thinner structure",
            "Fatigue and corrosion immunity simplifies maintenance",
            "Tailorability optimizes for every load case",
            "Cost justified by fuel savings over life"
        ],
        resolution_strategy="Composites are not universally superior - trade-offs exist. Through-thickness weakness makes composites poor for bolted joints (bearing stress limited by matrix, ~70 ksi vs 120+ ksi for aluminum). Impact damage tolerance inferior - Barely Visible Impact Damage (BVID) can cause significant strength reduction invisible to naked eye. Requires ultrasonic inspection for damage detection. Moisture absorption degrades matrix properties (10-15% strength loss at saturation). Lightning strike requires protection (copper mesh or aluminum foil outer ply). Repair more complex than aluminum - scarf or stepped repairs, cure cycle required. For high-bearing areas (fittings, attachments), metallic inserts or hybrid construction preferred. Certification requires extensive testing per AC 20-107B: static strength (notched/unnotched), fatigue, damage tolerance (impact + CAI compression after impact), environmental knockdowns, bearing/bypass interaction.",
        entity_scope="Primary and secondary structures using CFRP",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Material advantages clear but application-dependent trade-offs",
        controlling_precedent="AC 20-107B Section 4 - Material characterization and design values",
        category=IssueCategory.COMPOSITE_MATERIALS
    ),

    DoctrineBlock(
        topic="composite_failure_criteria_tsai_wu",
        keywords=["Tsai-Wu", "failure criterion", "composite failure", "first ply failure", "progressive damage"],
        conclusion_template=[
            "Tsai-Wu failure criterion is quadratic interaction equation for composite ply failure prediction.",
            "Failure Index FI = Σ(F_i·σ_i) + Σ(F_ij·σ_i·σ_j), with failure when FI >= 1.0.",
            "Progressive damage analysis required beyond first ply failure for ultimate strength."
        ],
        reasoning_framework="""Composite failure prediction is complex due to multiple failure modes (fiber tension/compression,
matrix tension/compression, delamination) and anisotropic properties. Several failure criteria exist: Maximum Stress (independent
criteria for each stress component - overly conservative), Maximum Strain (similar but strain-based), Tsai-Hill (quadratic
interaction, no interaction term F_12), Tsai-Wu (quadratic with full interaction, most general), Hashin (distinguishes fiber
vs matrix modes), Puck (physically-based, complex). Tsai-Wu is widely used: F_1·σ_1 + F_2·σ_2 + F_11·σ_1² + F_22·σ_2² +
F_66·τ_12² + 2·F_12·σ_1·σ_2 >= 1.0 for failure. Coefficients from uniaxial and biaxial tests: F_1 = 1/X_t - 1/X_c,
F_11 = 1/(X_t·X_c), F_2 = 1/Y_t - 1/Y_c, F_22 = 1/(Y_t·Y_c), F_66 = 1/S², F_12 = -0.5/√(X_t·X_c·Y_t·Y_c) typical.
Failure Index FI = left side of equation; FI < 1.0 safe, FI >= 1.0 failure predicted. Reserve Factor RF = 1/√FI (factor
to multiply loads to reach failure). Limitation: predicts first ply failure (FPF), not ultimate laminate failure. After
FPF, damage ply carries reduced load (property degradation rules: E_damaged = 0.1·E_original typical for matrix mode, zero
for fiber mode), load redistributes to other plies. Progressive damage analysis: apply load increments, check all plies for
failure, degrade failed plies, continue until ultimate failure (unstable load redistribution). Hashin criterion preferred
for progressive analysis because separates fiber/matrix modes allowing different degradation rules. Delamination not captured
by in-plane criteria - requires separate analysis (strain energy release rate, cohesive zone modeling).""",
        key_factors=[
            "Tsai-Wu quadratic failure criterion with interaction",
            "Failure Index FI >= 1.0 indicates ply failure",
            "Reserve Factor RF = 1/√FI",
            "First ply failure ≠ ultimate laminate failure",
            "Progressive damage analysis for ultimate strength",
            "Property degradation rules after ply failure",
            "Delamination requires separate analysis"
        ],
        primary_authority=[
            "CMH-17 Volume 3 - Polymer matrix composites failure analysis",
            "AC 20-107B Appendix A - Failure criteria overview",
            "NASA/TP-2004-213500 - World-Wide Failure Exercise (WWFE)",
            "ASTM D5766 - Open-hole tensile (OHT) strength"
        ],
        burden_holder="Composite stress analyst",
        adversary_position="FPF is adequate design criterion, progressive analysis unnecessary",
        counter_arguments=[
            "Conservative factor of safety covers FPF to ultimate gap",
            "Testing shows FPF close to ultimate for many laminates",
            "Progressive analysis too complex and uncertain",
            "Linear extrapolation from FPF acceptable"
        ],
        resolution_strategy="FAA position per AC 20-107B: FPF alone is insufficient for ultimate strength prediction. Laminate may have significant reserve strength beyond FPF (quasi-isotropic layup continues to carry load as individual plies fail), or may have little reserve (0° tension-dominated layup fails catastrophically when 0° fibers break). Testing required to validate analysis. For certification: (1) Use progressive damage analysis validated by element tests (OHT, open-hole compression, filled-hole tension/compression, bearing/bypass), (2) Demonstrate ultimate strength with test factors (A-basis material, scatter in manufacturing, environment), (3) Full-scale test validates analysis and accounts for factors not captured in models (e.g., load redistribution, residual stresses). FPF acceptable for preliminary design sizing but final certification requires ultimate strength demonstration.",
        entity_scope="Composite primary structures requiring Part 25 certification",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Analysis method widely used but test validation mandatory",
        controlling_precedent="AC 20-107B Section 5.5.3 - Ultimate strength requires progressive failure analysis or test",
        category=IssueCategory.COMPOSITE_MATERIALS
    ),

    DoctrineBlock(
        topic="aluminum_alloys_2024_7075",
        keywords=["aluminum alloy", "2024-T3", "7075-T6", "temper", "heat treatment", "clad", "alclad"],
        conclusion_template=[
            "2024-T3 is ductile, fatigue-resistant aluminum for fuselage skins; 7075-T6 is high-strength for wings/fittings.",
            "Temper designation indicates heat treatment: -T3 is solution heat treated + cold worked, -T6 is solution + aged.",
            "Alclad (thin pure aluminum coating) provides corrosion protection but reduces fatigue strength 10-15%."
        ],
        reasoning_framework="""Aluminum alloys dominate aircraft structures due to excellent strength-to-weight, machinability,
and cost. Designation system: XXXX-TY format. First digit = alloy series (2xxx = Al-Cu, 7xxx = Al-Zn-Mg-Cu). Four digits
= specific composition. T = temper (heat treatment state). Key alloys: 2024-T3 (Al-4.4Cu-1.5Mg-0.6Mn): F_tu = 64 ksi,
F_ty = 42 ksi, excellent fatigue resistance, high ductility (elongation ~18%), used for fuselage skins, wing skins (lower
surface tension). T3 = solution heat treated + cold worked (stretched 1-3% for stress relief). 7075-T6 (Al-5.6Zn-2.5Mg-1.6Cu-0.23Cr):
F_tu = 78 ksi, F_ty = 68 ksi, highest strength widely used aluminum, lower ductility (~11%), used for wing spars, stringers,
fittings, landing gear. T6 = solution heat treated + artificially aged (120°C for 24 hours). 7050-T7451 (Al-6.2Zn-2.3Mg-2.3Cu):
improved 7075, better fracture toughness and stress corrosion resistance, F_tu = 76 ksi, F_ty = 66 ksi, T7451 = overaged +
stress-relieved (compression), used for thick sections. 6061-T6 (Al-1.0Mg-0.6Si): moderate strength (F_tu = 45 ksi), excellent
corrosion resistance, weldable, used for non-critical structures, brackets, frames. Alclad: thin layer (0.002-0.004") of
pure aluminum (1230 alloy) rolled onto surface, pure aluminum anodic to core, sacrificial corrosion protection. Reduces
fatigue strength by 10-15% due to soft surface layer initiating cracks. Trade-off: corrosion protection vs fatigue. For
pressurized fuselage (high fatigue loads), alclad preferred despite fatigue penalty. For wing spars (high static loads,
low corrosion exposure), bare aluminum preferred.""",
        key_factors=[
            "2024-T3: ductile, fatigue-resistant, fuselage skins (F_tu=64ksi)",
            "7075-T6: highest strength, wing structures (F_tu=78ksi)",
            "7050-T7451: improved toughness/SCC resistance, thick sections",
            "Temper -T3: solution + cold work; -T6: solution + age; -T7: overaged",
            "Alclad: corrosion protection but 10-15% fatigue penalty",
            "Temperature limits: 200°F continuous, 250°F short-term",
            "Grain direction: L (longitudinal) strongest, ST (short transverse) weakest"
        ],
        primary_authority=[
            "MMPDS-01 (formerly MIL-HDBK-5) - Material properties database",
            "AMS 4037 - 2024-T3 alclad sheet specification",
            "AMS 4050 - 7075-T6 bare plate specification",
            "ASM Handbook Vol. 2 - Properties and Selection: Nonferrous Alloys"
        ],
        burden_holder="Materials engineer",
        adversary_position="Higher strength alloy always preferable for weight reduction",
        counter_arguments=[
            "7075-T6 strength allows thinner structure, saves weight",
            "Modern corrosion prevention systems eliminate need for alclad",
            "Fatigue not critical for all applications",
            "Higher strength reduces part count and fasteners"
        ],
        resolution_strategy="Material selection requires trade study balancing strength, fatigue, corrosion, formability, cost. 7075-T6 inappropriate for fuselage skins because: (1) Lower ductility (11% vs 18%) reduces damage tolerance, (2) Higher strength means higher operating stress, reducing fatigue life, (3) Greater susceptibility to stress corrosion cracking (SCC) in marine/coastal environments. Aloha Airlines failure was 7075-T6 fuselage - multiple site damage from fatigue. Modern fuselages use 2024-T3 alclad specifically for fatigue resistance. For wing spars, 7075-T6 appropriate because static strength critical and fatigue loads lower (flight cycles vs pressurization cycles). Corrosion prevention: primers, sealants, anodizing supplement or replace alclad. Material must be matched to application - no universal 'best' alloy.",
        entity_scope="Metallic aircraft primary and secondary structures",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established material selection principles with 80+ years experience",
        controlling_precedent="MMPDS provides design allowables - use appropriate alloy for application",
        category=IssueCategory.METALLIC_MATERIALS
    ),

    DoctrineBlock(
        topic="corrosion_types_galvanic_pitting",
        keywords=["corrosion", "galvanic", "pitting", "exfoliation", "stress corrosion cracking", "intergranular"],
        conclusion_template=[
            "Galvanic corrosion occurs when dissimilar metals contact in electrolyte; anode corrodes preferentially.",
            "Pitting creates localized deep corrosion in protective oxide layer; stress concentrations for crack initiation.",
            "Exfoliation is subsurface grain boundary attack lifting surface layers; critical for aluminum alloys."
        ],
        reasoning_framework="""Corrosion is electrochemical metal degradation, major aircraft maintenance burden and airworthiness
concern. Six primary types: (1) Galvanic corrosion: dissimilar metals in electrical contact with electrolyte form galvanic
cell. More anodic metal corrodes, more cathodic protected. Galvanic series (seawater): magnesium (most anodic) > aluminum
alloys > cadmium > steel > stainless steel > titanium > graphite (most cathodic). Example: aluminum skin fastened with steel
fasteners - aluminum corrodes. Prevention: isolation (paint, sealant, anodize), use similar metals in series, protect anode
with sacrificial coating (zinc chromate primer). (2) Pitting corrosion: localized breakdown of passive oxide film creates
deep pits. Chloride ions (salt spray) initiate pitting. Anodic pit interior, cathodic surrounding surface. Autocatalytic
process accelerates. Danger: stress concentration at pit bottom (Kt = 3-6) initiates fatigue cracks. Detection difficult
until deep. (3) Exfoliation: subsurface intergranular attack parallel to surface, lifts layers like pages in book. Occurs
in 7xxx series alloys (7075, 7178) due to grain boundary precipitates anodic to matrix. Progressive - starts at edge, moves
inward. Detection: surface lifting, paint blistering, ultrasonic thickness loss. Prevented by alloy selection (7050-T7451
vs 7075-T6), T7 temper overaging. (4) Stress corrosion cracking (SCC): tensile stress + corrosive environment cause crack
growth without fatigue. 7xxx alloys susceptible in marine environments. Cracks perpendicular to stress (intergranular).
Time-dependent - may take years to appear. (5) Intergranular corrosion: grain boundary attack without stress, due to precipitates
or segregation. (6) Crevice corrosion: oxygen depletion in crevice (lap joints, fastener interfaces) creates potential
difference, accelerates attack. Prevention: sealant, eliminate crevices, corrosion inhibitors.""",
        key_factors=[
            "Galvanic: dissimilar metals + electrolyte, anode corrodes (Al + steel = Al corrodes)",
            "Pitting: localized oxide breakdown, stress concentrations initiate cracks",
            "Exfoliation: subsurface grain boundary attack, 7xxx alloys, T7 temper resists",
            "SCC: stress + environment + susceptible alloy (7xxx), intergranular cracking",
            "Crevice: oxygen depletion in gaps accelerates corrosion",
            "Marine environment (salt spray) most aggressive",
            "Prevention: coatings, sealants, alloy selection, drainage"
        ],
        primary_authority=[
            "AC 43-4B - Corrosion Control for Aircraft",
            "ASTM G48 - Pitting and crevice corrosion resistance testing",
            "MIL-STD-889 - Dissimilar metals (galvanic compatibility)",
            "AMS 2700 - Passivation of corrosion-resistant steels"
        ],
        burden_holder="Maintenance and corrosion engineers",
        adversary_position="Modern coatings eliminate corrosion concerns",
        counter_arguments=[
            "Primers and paints provide complete protection",
            "Composite structures eliminate corrosion",
            "Sealants prevent moisture ingress",
            "Environmental controls (hangars, dry climates) reduce risk"
        ],
        resolution_strategy="Coatings are first defense but not absolute protection. Mechanical damage (assembly, service), UV degradation, and thermal cycling create coating defects allowing corrosion initiation. AC 43-4B requires inspections because coatings fail over time. Composites eliminate corrosion of structural material but create new galvanic pairs (carbon fiber is cathodic relative to aluminum - accelerates aluminum corrosion at interfaces). Isolation required: glass fiber barrier ply, sealant, anodize aluminum. Sealants degrade over time - reseal intervals in maintenance manual. Environmental controls help but aircraft operate globally including marine, tropical environments. Corrosion prevention is multi-layered approach: material selection (7050-T7 vs 7075-T6, titanium vs steel for landing gear), coatings (anodize, alodine, primers, topcoats), design (eliminate crevices, drainage holes, accessibility for inspection/cleaning), maintenance (washing, inspection, touch-up repair). Regulatory: corrosion prevention and control program (CPCP) mandatory for transport aircraft per FAA aging aircraft programs.",
        entity_scope="All metallic aircraft structures",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Corrosion is inevitable in aircraft service - prevention and management mandatory",
        controlling_precedent="AC 43-4B Section 3 - Corrosion types and prevention methods",
        category=IssueCategory.CORROSION
    ),

    DoctrineBlock(
        topic="ndt_methods_ultrasonic_eddy_current",
        keywords=["NDT", "NDI", "ultrasonic", "eddy current", "radiography", "penetrant", "magnetic particle"],
        conclusion_template=[
            "Ultrasonic testing detects internal flaws (cracks, voids, delamination) using high-frequency sound waves.",
            "Eddy current detects surface and near-surface cracks in conductive materials (aluminum, titanium).",
            "Method selection depends on flaw type, location, material, and required sensitivity."
        ],
        reasoning_framework="""Non-destructive testing (NDT/NDI - inspection) is critical for damage tolerance programs,
quality control, and maintenance. Five primary methods: (1) Ultrasonic testing (UT): high-frequency sound waves (2-10 MHz)
propagate through material, reflect from flaws or back surface. Pulse-echo mode: single transducer transmits and receives.
Through-transmission: separate transmitter/receiver, detects attenuation. Detects: internal cracks, voids, porosity, delamination
in composites, corrosion thinning. Advantages: detects internal flaws, depth information, portable. Limitations: requires
couplant (water, gel), surface must be accessible, skilled operator required, reference standards needed. Typical sensitivity:
0.030 inch diameter flat-bottom hole equivalent. (2) Eddy current (EC): alternating current in probe coil induces eddy currents
in conductive material, flaws disrupt eddy current flow changing coil impedance. Detects: surface and near-surface cracks
(0-0.100 inch deep), corrosion, material properties. Advantages: no couplant, fast scanning, detects through coatings. Limitations:
conductive materials only, shallow penetration, geometry sensitivity, lift-off variations. Typical crack detection: 0.050 inch
long x 0.010 inch deep. High frequency (100+ kHz) = surface sensitive; low frequency (1-10 kHz) = deeper penetration. (3) Radiography
(X-ray, gamma): penetrating radiation, film or digital detector, flaws appear as density variations. Detects: internal voids,
porosity, inclusions, cracks (if orientation favorable). Limitations: radiation safety, cracks must be aligned with beam,
expensive, not field-portable. (4) Dye penetrant (PT): liquid penetrant drawn into surface-breaking cracks by capillary
action, developer draws penetrant out, visible indication. Detects: surface cracks, porosity. Advantages: inexpensive, simple,
works on any non-porous material. Limitations: surface flaws only, surface prep critical (must be clean). (5) Magnetic particle
(MT): ferromagnetic materials magnetized, magnetic particles accumulate at surface/near-surface flaws distorting field.
Detects: surface and near-surface cracks in steel, iron. Limitations: ferromagnetic materials only, demagnetization may be
required after inspection.""",
        key_factors=[
            "Ultrasonic: internal flaws, through-transmission, 0.030 inch sensitivity",
            "Eddy current: surface/near-surface cracks in conductors, 0.050\" detection",
            "Radiography: internal voids/porosity, radiation safety concerns",
            "Dye penetrant: surface cracks only, simple and inexpensive",
            "Magnetic particle: ferromagnetic materials only, surface cracks",
            "Probability of detection (POD) curves quantify reliability",
            "Operator skill and certification critical (NAS410, SNT-TC-1A)"
        ],
        primary_authority=[
            "AC 43.13-1B - Acceptable Methods, Techniques, and Practices (NDT)",
            "ASTM E1417 - Liquid penetrant examination",
            "ASTM E1444 - Magnetic particle testing",
            "MIL-STD-410 - NDT personnel qualification and certification"
        ],
        burden_holder="NDT technician and engineering (method selection)",
        adversary_position="Advanced NDT can detect all defects, 100% reliability",
        counter_arguments=[
            "Modern phased array UT detects smallest flaws",
            "Eddy current array scans large areas quickly",
            "Computed tomography (CT) provides complete 3D flaw map",
            "Automated systems eliminate human error"
        ],
        resolution_strategy="No NDT method has 100% probability of detection (POD). AC 25.571-1D recognizes this - damage tolerance initial flaw assumptions based on NDT limit of detection (LOD), not capability claims. POD curves (from designed experiments with seeded flaws) show detection probability vs flaw size. Typical results: POD = 90% at 0.100 inch crack for eddy current, 50% at 0.050 in. Missed flaw probability always non-zero. Factors affecting POD: operator skill/fatigue, surface condition, access/geometry, flaw orientation, equipment calibration. Multiple methods often used in combination - eddy current for surface, UT for internal. Automated systems improve consistency but cannot eliminate physics-based limitations (shallow eddy current penetration, UT dead zones). For critical inspections (damage tolerance), demonstrate POD via round-robin testing per MIL-HDBK-1823, use conservative assumptions (LOD not best-case detection), and design inspection intervals accounting for missed flaws (that's why two-lifetime requirement exists).",
        entity_scope="All aircraft inspections - manufacturing and in-service",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="NDT limitations well-documented but often overstated by vendors",
        controlling_precedent="AC 25.571-1D Appendix C - NDT capabilities and initial flaw sizes",
        category=IssueCategory.NDT_INSPECTION
    ),

    DoctrineBlock(
        topic="structural_repair_manual_procedures",
        keywords=["SRM", "structural repair manual", "damage limits", "allowable damage", "repair design", "doubler", "splice"],
        conclusion_template=[
            "Structural Repair Manual (SRM) provides approved repair procedures for typical damage scenarios.",
            "Allowable damage limits define when repair vs. replacement required; exceed limits = engineering disposition.",
            "Repair design must restore original strength, stiffness, and fatigue life without penalty."
        ],
        reasoning_framework="""Structural Repair Manual (SRM) is FAA-approved document (part of ICA - Instructions for
Continued Airworthiness per 25.1529) providing standardized repair procedures for typical damage. Organized by: (1) Aircraft
zone (fuselage, wing, empennage, etc.), (2) Damage type (dent, crack, hole, corrosion), (3) Damage limits (BVID, allowable,
non-allowable). Allowable damage: cosmetic, no repair required, aircraft airworthy. Example: dent <0.10 inch deep in non-critical
skin. Repairable damage: within SRM limits, follow approved procedure. Example: crack <2 inch in frame web - doubler plate repair
per SRM. Non-repairable damage: exceeds SRM limits, requires engineering disposition (DER or OEM). Example: crack in primary
wing spar cap. Repair design principles: (1) Restore original strength - static ultimate load (1.5x limit), (2) Restore stiffness
to prevent load redistribution, (3) Match fatigue life or better, (4) Minimize weight penalty, (5) Maintain fail-safe characteristics.
Common repair types: Doubler patch: additional layer(s) bonded or riveted over damage, shares load, simple but adds weight.
Flush patch: remove damaged material, install flush patch, aerodynamically smooth. Splice: cut out damage, install replacement
section with doubler or butt splice. Bonded repair: adhesive film bonds patch to parent structure, excellent fatigue, requires
cure (heat or room temp), sensitive to surface prep. Bolted repair: mechanical fasteners, easier field repair, fastener holes
can be stress concentrations. Hybrid: bonded + bolted for redundancy. Key design parameters: patch thickness (match parent
or thicker for reduced area), overlap length (stress transfer via fasteners or adhesive, typically 20-30x skin thickness for
bonded), fastener pitch (load transfer, typically 4-6 diameters), edge distance (2-3 diameters minimum), row spacing. Analysis:
joint efficiency = joint strength / parent material strength, target >100%. Fatigue: repair must not create new fatigue
hotspot - smooth transitions, no abrupt stiffness change, shot peen edges if needed.""",
        key_factors=[
            "SRM provides approved repairs for typical damage within limits",
            "Allowable damage: no repair; Repairable: SRM procedure; Non-repairable: engineering",
            "Repair must restore strength, stiffness, fatigue life",
            "Doubler vs flush vs splice - trade-offs in complexity, weight, aerodynamics",
            "Bonded repair: excellent fatigue, requires cure, surface prep critical",
            "Bolted repair: field-friendly, fastener holes are stress risers",
            "Joint efficiency >100%, smooth load transitions"
        ],
        primary_authority=[
            "14 CFR 25.1529 - Instructions for Continued Airworthiness",
            "AC 43.13-1B Chapter 4 - Metallic Structure Repairs",
            "AC 20-107B Section 13 - Composite Structure Repairs",
            "FAA Order 8300.16 - Airworthiness Directive Manual"
        ],
        burden_holder="Repair designer (DER or OEM) and maintenance organization",
        adversary_position="Any repair that looks good is acceptable",
        counter_arguments=[
            "Visual inspection shows smooth contour and good rivet pattern",
            "Repair has been in service without issue",
            "Patch is thicker than original so must be stronger",
            "Certified mechanic installed so must be approved"
        ],
        resolution_strategy="Visual appearance does not validate structural adequacy. AC 43.13-1B repairs acceptable for non-critical structures and small damage only - explicitly states not for primary structures or damage exceeding limits. For transport aircraft primary structures, SRM or engineering disposition mandatory. Improper repairs cause accidents: Aloha Airlines (cold bond repair that failed), China Airlines (improper 727 tail doubler repair), many others. Repair analysis required: stress analysis showing MS > 0, fatigue analysis if applicable, demonstration of fail-safe/damage tolerance. 'Thicker patch' alone insufficient - must consider stress concentrations at fastener holes, load transfer into parent structure, stiffness mismatch creating peel stresses. Service experience alone does not validate - latent damage accumulating. Certification basis: 14 CFR 43.13(a) requires repairs use methods acceptable to Administrator - SRM or engineering data. Unapproved repair is unairworthy per 39.3, grounds aircraft until properly repaired. Enforcement: re-repair per SRM or engineering disposition with DER sign-off, then inspection by FAA.",
        entity_scope="All aircraft structural repairs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory requirement - no flexibility on unapproved repairs",
        controlling_precedent="14 CFR 43.13(a) - repairs must be acceptable to Administrator (SRM or approved data)",
        category=IssueCategory.STRUCTURAL_REPAIR
    ),

    DoctrineBlock(
        topic="pressurized_fuselage_hoop_stress",
        keywords=["pressurized fuselage", "hoop stress", "longitudinal stress", "pressure differential", "cabin altitude"],
        conclusion_template=[
            "Hoop stress in pressurized cylinder: σ_hoop = (P·r)/t, twice the longitudinal stress.",
            "Pressure differential ΔP = P_cabin - P_ambient drives structural loads; 8-9 psi typical for transport aircraft.",
            "Fuselage design optimized for hoop stress - circumferential stringers carry tension loads."
        ],
        reasoning_framework="""Pressurized fuselage is thin-walled cylindrical pressure vessel. Pressure differential creates
biaxial stress state: (1) Hoop stress (circumferential): σ_hoop = (P·r)/t, where P = internal pressure differential, r = radius,
t = skin thickness. Tension stress perpendicular to axis. (2) Longitudinal stress (axial): σ_long = (P·r)/(2t) = σ_hoop/2.
Tension stress parallel to axis. Hoop stress is 2x longitudinal - design driver. Typical values: Transport aircraft ΔP = 8-9 psi
(cabin altitude 8,000 ft at 40,000 ft cruise), fuselage radius 75-100 inches, skin thickness 0.040-0.080 in. Example 737:
ΔP = 8.9 psi, r = 74", t = 0.050 in. -> σ_hoop = 13,200 psi, σ_long = 6,600 psi. Compare allowable: 2024-T3 F_ty = 42,000 psi,
F_tu = 64,000 psi -> MS_yield = 42/13.2 - 1 = 2.2, MS_ultimate = 64/(1.5x13.2) - 1 = 2.2 (factor 1.5 for ultimate). Design
features: Longitudinal stringers (hat sections, Z-sections) stiffen skin against hoop compression during ground loads and
bending, also provide fail-safe load paths. Stringers run lengthwise every 6-10 inches. Circumferential frames (rings)
maintain fuselage shape, prevent ovalization, transfer loads to keel beam and wing. Frames spaced 15-22 inches apart. Tear
straps: heavy doublers between stringers, stop crack propagation. Pressure bulkheads: forward and aft, flat or domed, carry
pressure load to fuselage. Doors and windows: major stress concentrations, require heavy doublers and edge reinforcement.
Fatigue critical: 40,000-60,000 pressurization cycles over aircraft life. Cracks initiate at rivet holes, grow between stringers.
Damage tolerance: fuselage designed with crack arresters so two-bay crack (skin between two frames) can be tolerated at limit
load. Aloha Airlines accident (1988): widespread fatigue damage, multiple cracks linked up, explosive decompression. Led to
aging aircraft programs and WFD inspections.""",
        key_factors=[
            "Hoop stress σ_hoop = P·r/t (2x longitudinal stress)",
            "Pressure differential ΔP = 8-9 psi for transport aircraft",
            "Stringers (longitudinal) and frames (circumferential) stiffen skin",
            "Tear straps arrest crack propagation",
            "Doors/windows are stress concentrations requiring doublers",
            "Fatigue critical: 40,000-60,000 pressurization cycles",
            "Widespread fatigue damage (WFD) inspections mandatory"
        ],
        primary_authority=[
            "14 CFR 25.365 - Pressurized compartment loads",
            "AC 25.571-1D Section 10 - Widespread fatigue damage",
            "NTSB AAR-89-03 - Aloha Airlines accident report",
            "Roark's Formulas for Stress and Strain - Thin cylinders"
        ],
        burden_holder="Fuselage structures engineer",
        adversary_position="Higher pressure differential increases cabin comfort without penalty",
        counter_arguments=[
            "Modern materials handle higher stress easily",
            "Passengers prefer lower cabin altitude (higher ΔP)",
            "Composites eliminate fatigue concerns",
            "Thicker skin compensates for higher pressure"
        ],
        resolution_strategy="Pressure differential directly drives weight and fatigue life. Increasing ΔP from 8.9 to 10 psi (to achieve 6,000 ft cabin altitude vs 8,000 ft) increases hoop stress by 12%, requiring thicker skin or more stringers. Weight penalty: ~1,000 lbs for 737-size aircraft per psi increase. Fatigue life: stress range scales linearly, cycles to crack initiation decreases exponentially (S-N curve). Higher ΔP reduces inspection intervals and increases maintenance costs. Composites (787) allow higher ΔP (8.9 psi to 6,000 ft cabin) because superior fatigue resistance and damage tolerance through lack of rivet holes (barrel sections co-bonded, not mechanically fastened). But composite fuselages still subject to impact damage, require inspections. Economic trade: passenger comfort vs weight vs maintenance cost. Industry consensus: 8-9 psi ΔP optimal for aluminum, up to 9.4 psi for composite. Boeing 787 and A350 use 6,000 ft cabin (ΔP ~9.4 psi at 43,000 ft) but pay weight and inspection penalty. Older aluminum aircraft (737, A320) remain at 8,000 ft cabin for economic reasons.",
        entity_scope="Pressurized transport aircraft fuselages",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Fundamental pressure vessel theory - well-established engineering",
        controlling_precedent="AC 25.571-1D Section 10 - WFD prevention tied to pressure cycle fatigue",
        category=IssueCategory.PRESSURIZED_STRUCTURES
    ),

    DoctrineBlock(
        topic="wing_structural_design_spar_rib_skin",
        keywords=["wing structure", "spar", "rib", "skin", "stringer", "shear web", "bending moment", "torque"],
        conclusion_template=[
            "Wing primary structure: spars carry bending (wing root moment), ribs maintain shape, skin/stringers resist shear/compression.",
            "Main spar(s) at 20-40% chord carry vertical bending and landing loads; rear spar at 60-70% chord closes torsion box.",
            "Stringers stiffen skin against buckling under compression and shear; spacing determined by buckling analysis."
        ],
        reasoning_framework="""Wing is complex three-dimensional structure carrying bending, shear, and torsion from aerodynamic
and inertia loads. Four primary elements: (1) Spars: main load-carrying members running spanwise. Typically 2-3 spars (front,
main, rear). Caps (upper/lower flanges) carry bending moment tension/compression. Web carries shear. Main spar at 20-40%
chord carries vertical shear and wing root bending moment (massive - several inches thick at root). Front spar defines leading
edge box. Rear spar closes torsion box. (2) Ribs: chordwise members maintain airfoil shape, distribute loads, support skin
against buckling. Spaced 15-30 inches apart. Transfer flight loads from skin to spars. Concentrated load ribs at engine pylon,
landing gear, flap/slat actuators. (3) Skin: aluminum sheet (0.040-0.125 inch typical) forms aerodynamic surface, carries shear
loads (shear flow q = T/2A for torsion, where T = torque, A = enclosed area), carries compression when lower skin in bending.
(4) Stringers: hat sections, Z-sections, or blade stiffeners run spanwise, riveted to inner skin surface. Increase skin buckling
resistance - buckling stress proportional to (t/b)² where t = skin thickness, b = stringer spacing. Typical spacing 3-6 inches.
Load paths: Lift force -> skin -> ribs -> spar web -> spar cap -> wing root. Torsion -> skin shear flow -> spar webs -> root.
Compression -> upper skin/stringers -> buckling analysis critical. Critical loads: (1) Limit maneuver (2.5g positive, -1.0g negative
Part 25) -> bending moment, (2) Gust loads -> dynamic response, (3) Landing -> vertical impact + side load, (4) Engine failure
-> yaw moment, (5) Ground loads (taxiing, braking) -> torsion. Wing box: torsion-resistant structure formed by front spar, rear
spar, upper skin, lower skin. High torsional rigidity GJ prevents twist. Fuel tanks inside wing box - wing carries bending
relief from fuel weight. Wing design: optimize weight subject to strength, stiffness, flutter, buckling constraints. Tapering
(thickness and chord) reduces weight while maintaining strength where needed. Composite wings: fewer parts (co-cured skin/stringer
panels), optimized layups for load direction, weight savings 15-20% vs aluminum.""",
        key_factors=[
            "Spars (spanwise) carry bending moment, main spar at 20-40% chord",
            "Ribs (chordwise) maintain shape, transfer loads to spars, 15-30\" spacing",
            "Skin carries shear (torsion), forms pressure boundary (integral tanks)",
            "Stringers stiffen skin against buckling, spacing 3-6\" typical",
            "Torsion box: front spar + rear spar + upper/lower skin",
            "Upper skin/stringers critical for compression buckling",
            "Wing root bending moment drives spar cap sizing"
        ],
        primary_authority=[
            "14 CFR 25.301 - Loads",
            "14 CFR 25.305 - Strength and deformation",
            "Bruhn Chapter C5 - Wing Beams",
            "Niu 'Airframe Structural Design' - Wing design methodology"
        ],
        burden_holder="Wing structures engineer",
        adversary_position="More spars always better for strength",
        counter_arguments=[
            "Additional spars increase strength and fail-safe",
            "Multiple load paths reduce criticality of single spar",
            "Manufacturing prefers repetitive structure",
            "Thick single spar has buckling issues"
        ],
        resolution_strategy="Additional spars increase weight, cost, and complexity without proportional benefit. Two-spar wing (main + rear) is industry standard for transport aircraft. Front spar often lighter torque-box closure or leading edge structure. Three-spar configurations (some early designs) heavier and complicate fuel tank access. Weight penalty: each spar adds caps, web, fasteners, and attachments. Weight optimization: concentrate material where bending moment highest (wing root), taper toward tip. Single thick spar has web buckling issues - thin webs with stiffeners more efficient. Fail-safe: achieved through multiple stringers (15-30 each surface), not multiple spars. Loss of single stringer (crack, corrosion) does not compromise wing - load redistributes to adjacent stringers. Multi-spar weight penalty outweighs fail-safe benefit. Modern trend: two-spar composite wings (787, A350) with co-cured skin/stringer panels, optimized layups per load direction, weight savings 15-20% vs aluminum. Trade study required for each design - no universal 'right' answer but two-spar configuration proven optimal for most applications.",
        entity_scope="Transport aircraft wing primary structure",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Standard industry practice but trade-offs exist for specific designs",
        controlling_precedent="Industry practice - 2-spar wing optimal for most transport aircraft",
        category=IssueCategory.WING_STRUCTURES
    ),

    DoctrineBlock(
        topic="certification_AC25571_damage_tolerance",
        keywords=["certification", "AC 25.571", "damage tolerance", "fatigue evaluation", "limit of validity", "LOV"],
        conclusion_template=[
            "AC 25.571-1D provides acceptable means of compliance for damage tolerance and fatigue evaluation per 14 CFR 25.571.",
            "Limit of Validity (LOV) defines maximum operational life for fatigue-critical structure; beyond LOV requires new evaluation.",
            "Damage tolerance evaluation demonstrates structure tolerates threshold damage for two inspection intervals."
        ],
        reasoning_framework="""14 CFR 25.571 Damage Tolerance and Fatigue Evaluation is foundational certification requirement
for transport aircraft structural safety. Mandates: (1) Damage tolerance evaluation for principal structural elements (PSE)
- must demonstrate structure tolerates damage (based on NDT detectability) for two inspection intervals while maintaining
required residual strength, (2) Fatigue evaluation - show structure maintains required strength for design service goal (DSG)
accounting for environmental effects, (3) Widespread fatigue damage (WFD) prevention - establish limit of validity (LOV)
beyond which WFD may occur. AC 25.571-1D (advisory circular) provides acceptable means but not only means of compliance.
Key concepts: Principal structural element (PSE): element contributing significantly to carrying flight/ground/pressurization
loads, whose failure could result in catastrophic loss. Includes: wing/fuselage/empennage primary structure, landing gear,
engine mounts, control surfaces. Threshold damage: damage size at NDT limit of detection - assume present initially or develop
during service. Typical: 0.05 inch surface crack (eddy current), 0.10 inch corner crack, 1.0 inch dent (visual). Two-lifetime requirement:
structure with threshold damage must withstand repeated loads for two inspection intervals without residual strength falling
below limit load capability. Scatter factor accounts for variability in crack growth rates, loads, material properties (typically
2-4x). Residual strength: load-carrying capability with damage present. Must be >= limit load at end of two inspection intervals.
Limit of Validity (LOV): operational limitation (flight cycles or hours) beyond which airplane must not be operated without
new fatigue evaluation. Set to prevent WFD - prevent multiple-site damage or multiple-element damage from reducing structure
below ultimate load capability. Established through testing (full-scale fatigue test to 2x DSG minimum) and analysis. Compliance
methods: (1) Analysis using fracture mechanics (Paris law) for crack growth, (2) Full-scale testing to demonstrate scatter
factor, (3) Fleet service experience (if adequate sample size and usage). Design service goal (DSG): target operational life
in flight cycles or hours - design objective but not operational limit. LOV >= DSG typically.""",
        key_factors=[
            "25.571(a): Damage tolerance evaluation mandatory for PSE",
            "25.571(b): Fatigue evaluation for DSG + environmental effects",
            "Threshold damage based on NDT limit of detection",
            "Two-lifetime requirement: tolerate damage for 2x inspection interval",
            "Residual strength >= limit load at end of interval",
            "Limit of Validity (LOV): max operational life, prevent WFD",
            "AC 25.571-1D is acceptable means, not only means"
        ],
        primary_authority=[
            "14 CFR 25.571 - Damage Tolerance and Fatigue Evaluation",
            "AC 25.571-1D - FAA advisory guidance",
            "FAA Order 8100.8 - Aging Aircraft Program",
            "Type Certificate Data Sheet - LOV specified"
        ],
        burden_holder="Manufacturer (type certification) and operator (continued airworthiness)",
        adversary_position="Statistical analysis shows damage probability negligible, inspections unnecessary",
        counter_arguments=[
            "Modern QC ensures zero manufacturing defects",
            "Service history shows no cracks in this area",
            "Probabilistic analysis demonstrates adequate safety",
            "Economic burden of inspections outweighs risk"
        ],
        resolution_strategy="Damage tolerance is non-negotiable per 25.571(a). Zero-defect argument rejected by Aloha accident and metallurgical studies showing manufacturing flaws below NDT threshold ubiquitous. 'No service cracks' is absence of evidence not evidence of absence - fleet may not have reached critical life yet, or cracks present but undetected. Probabilistic approach allowed but must demonstrate equivalent safety to deterministic AC 25.571-1D method - requires extensive validation. Economic argument is irrelevant - safety mandate. Inspection program is not optional - required for continued airworthiness. If operator refuses, certificate of airworthiness revoked per 39.3. Path forward: (1) Follow AC 25.571-1D - establish inspection program based on crack growth analysis and NDT capability, or (2) Demonstrate fail-safe design eliminating single-point failure, or (3) Retire structure at safe-life limit. No fourth option. LOV is regulatory compliance item specified in TCDS - operating beyond LOV without approved fatigue re-evaluation is violation.",
        entity_scope="Part 25 transport category aircraft certification and continued airworthiness",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Absolute regulatory requirement - no flexibility",
        controlling_precedent="14 CFR 25.571 mandatory, AC 25.571-1D acceptable means of compliance",
        category=IssueCategory.CERTIFICATION
    ),

    # Add 13+ more DoctrineBlock objects covering remaining topics:
    # - Flutter analysis, bird strike (FAR 25.631), bonded repairs, fastener selection,
    #   landing gear structural analysis, lightning strike, structural health monitoring,
    #   Ti-6Al-4V titanium alloy, composites failure modes (Hashin criterion),
    #   certification testing (static ultimate, fatigue test), material selection trade studies, etc.

    DoctrineBlock(
        topic="fastener_selection_rivets_hilok",
        keywords=["fastener", "rivet", "Hi-Lok", "blind fastener", "shear", "tension", "grip length"],
        conclusion_template=[
            "Solid rivets (2117-T4, AD) are standard for non-critical structures; flush head for aerodynamic surfaces.",
            "Hi-Lok/Hi-Tigue are precision interference-fit fasteners for fatigue-critical primary structures.",
            "Blind fasteners (Cherry Max, Avex) allow one-sided installation but have lower strength."
        ],
        reasoning_framework="""Fastener selection balances strength, fatigue, weight, cost, accessibility. Types: (1) Solid
rivets: driven (upset) to form shop head, creates interference fit, compressive residual stress beneficial for fatigue.
2117-T4 (AD rivet) most common - F_su = 30 ksi shear, used for non-critical structures. 2024-T4 (DD) higher strength F_su = 41 ksi.
Flush head (100° countersunk) for external surfaces, universal/brazier head for internal. Installation requires access both
sides (bucking bar). (2) Hi-Lok: two-piece precision fastener (pin + collar). Installed with torque wrench, collar breaks
off at design torque. Tight tolerance creates interference fit (0.0015-0.003 inch hole undersize). Reduces scatter in preload,
improves fatigue. F_su = 95 ksi tension, 65 ksi shear (alloy steel). Used for primary structures, landing gear, wing/fuselage
joints. Hi-Tigue variant has higher fatigue from rolled threads. (3) Lockbolts (Huck, Eddie-Bolt): similar to Hi-Lok but
installed with special tooling (swaging). Very high clamping force, excellent fatigue. (4) Blind fasteners: installed from
one side, mandrel pulls to form blind head then breaks off. CherryMax (bulbed), Avex, Olympic. Lower strength than solid
rivets (F_su = 30-40 ksi) due to hollow core, but essential where backside inaccessible (inside fuel tank, control surfaces).
(5) Screws/bolts: removable, used for access panels, inspection plates. AN3-AN20 (hex head), NAS (close tolerance). Key
parameters: Grip length = material thickness clamped. Shank must extend through all material. Diameter: 3/32 inch to 3/4 inch common,
sized for shear/bearing loads. Edge distance: 2D minimum for shear-loaded holes, 3D for high loads. Spacing: 4-6D typical
(too close causes fretting, too far reduces joint efficiency). Materials: aluminum (2117, 2024) for matching aluminum structure,
steel (NAS1097) for high loads or dissimilar metals, titanium for weight-critical titanium structures. Corrosion: aluminum
fasteners corrode with steel, use isolation (cadmium plate) or all-aluminum.""",
        key_factors=[
            "Solid rivets: 2117-T4 (AD) standard, 2024-T4 (DD) higher strength, flush or universal head",
            "Hi-Lok: precision interference fit, torque-controlled, F_su=95ksi, fatigue-critical",
            "Blind fasteners: one-side installation, lower strength, inaccessible areas",
            "Grip length must match material thickness",
            "Edge distance 2-3D, spacing 4-6D",
            "Material: aluminum with aluminum, steel for high load, isolation for dissimilar metals",
            "Installation quality critical - hole prep, countersink depth, upset force"
        ],
        primary_authority=[
            "AC 43.13-1B Chapter 4 - Riveting practices",
            "NASM1312 series - Rivet specifications",
            "NAS1097-NAS1099 - Hi-Lok specifications",
            "MIL-HDBK-5 - Fastener design allowables"
        ],
        burden_holder="Structures designer and assembler",
        adversary_position="Higher grade fastener always preferable",
        counter_arguments=[
            "Hi-Lok superior to rivets in all respects",
            "Blind fasteners easier to install saves labor",
            "Steel fasteners stronger than aluminum",
            "More fasteners always increases strength"
        ],
        resolution_strategy="Fastener selection requires trade study. Hi-Lok is superior to rivets for fatigue-critical primary structures (3-5x fatigue improvement from interference fit and controlled preload) but costs 10x more and requires precise hole tolerance (reaming). For non-critical secondary structures, solid rivets adequate and economical. Blind fasteners have 30-40% strength penalty vs solid rivets due to hollow core - acceptable where accessibility drives design but not for highly-loaded joints. Steel fasteners in aluminum structure create galvanic corrosion (steel cathodic, aluminum anodic) unless isolated with cadmium plate or anodize - adds cost and maintenance. Excessive fasteners increase cost, weight, and stress concentrations (each hole reduces net section). Optimal fastener count balances load transfer efficiency vs hole damage. Joint design: bearing strength (fastener crushes hole) vs shear strength (fastener fails in shear). Bearing failure preferred (gradual, visual damage) over shear (sudden, catastrophic). Size fastener so bearing failure occurs at lower load than shear failure. Installation quality affects performance: over-driven rivets (upset too much) crack head, under-driven don't develop interference. Countersink too deep weakens, too shallow creates stress concentration. Quality control and inspector training critical. FAA position: use fastener appropriate for application per AC 43.13-1B, not universal 'best' fastener.",
        entity_scope="All mechanically-fastened aircraft structures",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Well-established practices but application-specific trade-offs",
        controlling_precedent="AC 43.13-1B Chapter 4 - Fastener selection guidelines",
        category=IssueCategory.STRUCTURAL_DESIGN
    ),

    # Continue with remaining topics to reach 25+ total blocks...
]


# ═══════════════════════════════════════════════════════════════════════════
# METRICS AND TELEMETRY
# ═══════════════════════════════════════════════════════════════════════════

class MetricsCollector:
    def __init__(self):
        self.start_time = time.time()
        self.total_queries = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.response_times: List[float] = []
        self.error_count = 0

    def record_query(self, cache_hit: bool, response_time_ms: float):
        self.total_queries += 1
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        self.response_times.append(response_time_ms)

    def record_error(self):
        self.error_count += 1

    @property
    def uptime_seconds(self) -> float:
        return time.time() - self.start_time

    @property
    def cache_hit_rate(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return self.cache_hits / self.total_queries

    @property
    def avg_response_time_ms(self) -> float:
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)


metrics = MetricsCollector()


# ═══════════════════════════════════════════════════════════════════════════
# QUERY PROCESSING ENGINE
# ═══════════════════════════════════════════════════════════════════════════

class StructuresEngine:
    def __init__(self):
        self.doctrine_cache = {block.topic: block for block in DOCTRINE_CACHE}
        self.coverage_map: Dict[str, int] = defaultdict(int)
        self.drift_events: List[Dict[str, Any]] = []

    def normalize_query(self, query: str) -> str:
        """Semantic normalization for consistent lookups."""
        normalized = query.lower().strip()

        # Structural design synonyms
        if any(kw in normalized for kw in ["safe life", "safelife", "finite life"]):
            normalized += " safe_life_design_philosophy"
        if any(kw in normalized for kw in ["fail safe", "failsafe", "redundant"]):
            normalized += " fail_safe_design_philosophy"
        if any(kw in normalized for kw in ["damage tolerant", "damage tolerance", "dt", "slow crack"]):
            normalized += " damage_tolerant_design"

        # Stress analysis
        if any(kw in normalized for kw in ["von mises", "vonmises", "combined stress"]):
            normalized += " stress_analysis_methods"

        # Fatigue
        if any(kw in normalized for kw in ["s-n curve", "sn curve", "miner", "cumulative damage"]):
            normalized += " fatigue_life_prediction_SN_curves"
        if any(kw in normalized for kw in ["paris law", "paris equation", "crack growth", "da/dn"]):
            normalized += " fracture_mechanics_paris_law"

        # Materials
        if any(kw in normalized for kw in ["carbon fiber", "cfrp", "composite"]):
            normalized += " composite_materials_carbon_fiber"
        if any(kw in normalized for kw in ["tsai-wu", "tsai wu", "failure criterion"]):
            normalized += " composite_failure_criteria_tsai_wu"
        if any(kw in normalized for kw in ["2024", "7075", "aluminum alloy"]):
            normalized += " aluminum_alloys_2024_7075"

        # Corrosion
        if any(kw in normalized for kw in ["galvanic", "pitting", "exfoliation", "scc"]):
            normalized += " corrosion_types_galvanic_pitting"

        # NDT
        if any(kw in normalized for kw in ["ultrasonic", "eddy current", "ndt", "ndi"]):
            normalized += " ndt_methods_ultrasonic_eddy_current"

        # Repair
        if any(kw in normalized for kw in ["srm", "repair manual", "doubler", "patch"]):
            normalized += " structural_repair_manual_procedures"

        # Pressurized structures
        if any(kw in normalized for kw in ["hoop stress", "pressure", "fuselage cylinder"]):
            normalized += " pressurized_fuselage_hoop_stress"

        # Wing structures
        if any(kw in normalized for kw in ["wing spar", "wing rib", "wing structure"]):
            normalized += " wing_structural_design_spar_rib_skin"

        # Certification
        if any(kw in normalized for kw in ["25.571", "ac 25.571", "certification", "lov", "limit of validity"]):
            normalized += " certification_AC25571_damage_tolerance"

        # Fasteners
        if any(kw in normalized for kw in ["rivet", "hi-lok", "hilok", "fastener"]):
            normalized += " fastener_selection_rivets_hilok"

        return normalized

    def find_relevant_doctrines(self, query: str) -> List[DoctrineBlock]:
        """Find doctrine blocks matching query keywords."""
        normalized = self.normalize_query(query)
        query_lower = query.lower()

        scored_blocks = []
        for block in DOCTRINE_CACHE:
            score = 0
            # Exact topic match
            if block.topic in normalized:
                score += 100
            # Keyword matches
            for keyword in block.keywords:
                if keyword.lower() in query_lower:
                    score += 10
            # Category relevance
            if block.category.value.lower().replace("_", " ") in query_lower:
                score += 5

            if score > 0:
                scored_blocks.append((score, block))
                self.coverage_map[block.topic] += 1

        scored_blocks.sort(key=lambda x: x[0], reverse=True)
        return [block for score, block in scored_blocks[:3]]

    def generate_response(
        self,
        query: str,
        mode: ResponseMode,
        relevant_doctrines: List[DoctrineBlock]
    ) -> Dict[str, Any]:
        """Generate structured response based on mode and doctrines."""

        if not relevant_doctrines:
            return {
                "answer": f"No specific aircraft structures/materials doctrine found for query: {query}. "
                         f"This engine covers structural design (safe-life, fail-safe, damage tolerant), "
                         f"stress analysis, fatigue, fracture mechanics, composites, metals (aluminum, titanium), "
                         f"corrosion, NDT, repairs, pressurized structures, wing structures, and certification. "
                         f"Please refine your question to one of these areas.",
                "confidence": ConfidenceLevel.DISCLOSURE,
                "sources": ["General aircraft structures knowledge"],
                "reasoning_chain": None,
                "related_topics": [
                    "Damage tolerant design",
                    "Composite failure criteria",
                    "Fatigue crack growth (Paris law)",
                    "Aluminum alloy selection",
                    "NDT methods",
                    "AC 25.571 certification"
                ]
            }

        primary_doctrine = relevant_doctrines[0]

        if mode == ResponseMode.FAST:
            answer = " ".join(primary_doctrine.conclusion_template)
            reasoning_chain = None

        elif mode == ResponseMode.DEFENSE:
            answer = f"**Conclusion:** {' '.join(primary_doctrine.conclusion_template)}\n\n"
            answer += f"**Analysis:** {primary_doctrine.reasoning_framework[:500]}...\n\n"
            answer += f"**Key Factors:**\n"
            for factor in primary_doctrine.key_factors[:5]:
                answer += f"  • {factor}\n"
            answer += f"\n**Controlling Authority:** {primary_doctrine.controlling_precedent}"
            reasoning_chain = [
                f"Issue Category: {primary_doctrine.category.value}",
                f"Confidence Stratification: {primary_doctrine.confidence_stratification}",
                f"Primary Authority: {', '.join(primary_doctrine.primary_authority[:2])}"
            ]

        else:  # MEMO
            answer = f"# Aircraft Structures Analysis - {primary_doctrine.topic.replace('_', ' ').title()}\n\n"
            answer += f"## Executive Summary\n{' '.join(primary_doctrine.conclusion_template)}\n\n"
            answer += f"## Detailed Analysis\n{primary_doctrine.reasoning_framework}\n\n"
            answer += f"## Key Technical Factors\n"
            for i, factor in enumerate(primary_doctrine.key_factors, 1):
                answer += f"{i}. {factor}\n"
            answer += f"\n## Regulatory Basis\n"
            for auth in primary_doctrine.primary_authority:
                answer += f"  • {auth}\n"
            answer += f"\n## Adversarial Position\n{primary_doctrine.adversary_position}\n\n"
            answer += f"## Counter-Arguments\n"
            for arg in primary_doctrine.counter_arguments:
                answer += f"  • {arg}\n"
            answer += f"\n## Resolution Strategy\n{primary_doctrine.resolution_strategy}\n\n"
            answer += f"## Confidence Assessment\n"
            answer += f"Level: {primary_doctrine.confidence.value} - {primary_doctrine.confidence_stratification}"

            reasoning_chain = [
                f"Category: {primary_doctrine.category.value}",
                f"Entity Scope: {primary_doctrine.entity_scope}",
                f"Burden Holder: {primary_doctrine.burden_holder}",
                f"Controlling Precedent: {primary_doctrine.controlling_precedent}"
            ]

        sources = primary_doctrine.primary_authority.copy()
        related_topics = [
            block.topic.replace("_", " ").title()
            for block in relevant_doctrines[1:3]
        ] if len(relevant_doctrines) > 1 else []

        return {
            "answer": answer,
            "confidence": primary_doctrine.confidence,
            "sources": sources,
            "reasoning_chain": reasoning_chain,
            "related_topics": related_topics
        }

    def compute_determinism_hash(self, query: str, mode: ResponseMode, answer: str) -> str:
        """SHA-256 hash for reproducibility verification."""
        content = f"{query}|{mode.value}|{answer}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]


engine = StructuresEngine()


# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    description="Aircraft Structures & Materials Expert System"
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
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        port=PORT,
        uptime_seconds=metrics.uptime_seconds,
        total_queries=metrics.total_queries,
        cache_hit_rate=metrics.cache_hit_rate,
        avg_response_time_ms=metrics.avg_response_time_ms
    )


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with three-layer response."""
    start_time = time.time()

    try:
        logger.info(f"Query received: {request.query[:100]} | Mode: {request.mode}")

        # Find relevant doctrines (cache layer)
        relevant_doctrines = engine.find_relevant_doctrines(request.query)
        cache_hit = len(relevant_doctrines) > 0

        # Generate response
        response_data = engine.generate_response(
            request.query,
            request.mode,
            relevant_doctrines
        )

        # Compute determinism hash
        det_hash = engine.compute_determinism_hash(
            request.query,
            request.mode,
            response_data["answer"]
        )

        response_time_ms = (time.time() - start_time) * 1000
        metrics.record_query(cache_hit, response_time_ms)

        logger.info(f"Query completed in {response_time_ms:.2f}ms | Cache hit: {cache_hit}")

        return QueryResponse(
            query=request.query,
            mode=request.mode,
            answer=response_data["answer"],
            confidence=response_data["confidence"],
            sources=response_data["sources"],
            reasoning_chain=response_data["reasoning_chain"],
            related_topics=response_data["related_topics"],
            determinism_hash=det_hash,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

    except Exception as e:
        metrics.record_error()
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "engine": ENGINE_NAME,
        "version": VERSION,
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "query": "/query",
            "docs": "/docs"
        }
    }


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Doctrine cache loaded: {len(DOCTRINE_CACHE)} topics")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
