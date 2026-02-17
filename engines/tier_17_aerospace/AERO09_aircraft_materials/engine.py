"""
AERO09 Aircraft Materials Intelligence Engine
TIE-Grade Aviation Materials Analysis System

Analyzes aerospace materials including composites (CFRP, GFRP), aluminum alloys,
titanium alloys, superalloys, material fatigue, damage tolerance, and qualification testing.

Port: 9204
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict, Counter

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger


# ============================================================================
# ENUMS AND TYPES
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
    COMPOSITE_DESIGN = "COMPOSITE_DESIGN"
    ALUMINUM_ALLOYS = "ALUMINUM_ALLOYS"
    TITANIUM_ALLOYS = "TITANIUM_ALLOYS"
    SUPERALLOYS = "SUPERALLOYS"
    FATIGUE_ANALYSIS = "FATIGUE_ANALYSIS"
    DAMAGE_TOLERANCE = "DAMAGE_TOLERANCE"
    MATERIAL_QUALIFICATION = "MATERIAL_QUALIFICATION"
    CORROSION_PROTECTION = "CORROSION_PROTECTION"
    ADDITIVE_MANUFACTURING = "ADDITIVE_MANUFACTURING"
    MATERIAL_SELECTION = "MATERIAL_SELECTION"
    TESTING_VALIDATION = "TESTING_VALIDATION"
    CERTIFICATION = "CERTIFICATION"


class AuthorityLevel(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    TERTIARY = "TERTIARY"


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=10, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    context: Optional[Dict[str, Any]] = None


class DoctrineMatch(BaseModel):
    topic: str
    confidence: float
    category: IssueCategory
    keywords_matched: List[str]
    authority_level: AuthorityLevel


class TelemetryData(BaseModel):
    query_time_ms: float
    cache_hits: int
    vector_searches: int
    doctrines_triggered: List[str]
    confidence_level: ConfidenceLevel


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    doctrines_used: List[DoctrineMatch]
    telemetry: TelemetryData
    determinism_hash: str
    timestamp: str
    audit_trail_id: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    avg_response_ms: float
    cache_hit_rate: float


# ============================================================================
# DOCTRINE BLOCK
# ============================================================================

@dataclass
class DoctrineBlock:
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
    category: IssueCategory
    authority_level: AuthorityLevel = AuthorityLevel.PRIMARY

    def matches(self, query: str) -> Tuple[bool, int]:
        query_lower = query.lower()
        matches = sum(1 for kw in self.keywords if kw.lower() in query_lower)
        return (matches >= 2, matches)


# ============================================================================
# DOCTRINE CACHE - 30+ REAL AEROSPACE MATERIALS BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    # COMPOSITE_DESIGN Doctrines
    DoctrineBlock(
        topic="CFRP Quasi-Isotropic Layup Design",
        keywords=["carbon fiber", "composite", "layup", "quasi-isotropic", "ply orientation", "stacking sequence", "laminate"],
        conclusion_template="Quasi-isotropic CFRP laminates provide balanced in-plane properties through symmetric ply stacking with typical [0/+45/90/-45]s orientation. Material allowables must be established per CMH-17 statistical methods.",
        reasoning_framework="""
Analysis of carbon fiber reinforced polymer quasi-isotropic laminate design:

1. PLY ORIENTATION REQUIREMENTS:
   - Standard quasi-isotropic: [0/+45/90/-45]s or [0/60/-60]s
   - Equal proportion of 0°, ±45°, 90° plies
   - Symmetric layup to prevent warping
   - Balanced construction: equal +/- plies
   - Minimum 10% plies in any principal direction

2. STACKING SEQUENCE CONSIDERATIONS:
   - No more than 4 consecutive plies of same orientation
   - Avoid [90/0/90] interfaces (high interlaminar stress)
   - Surface plies typically 0° or ±45° for impact resistance
   - Midplane symmetry for dimensional stability
   - Ply drops must be staggered and tapered

3. MECHANICAL PROPERTY IMPLICATIONS:
   - In-plane stiffness: Ex ≈ Ey (quasi-isotropic condition)
   - Reduced stiffness vs unidirectional (~50% in primary direction)
   - Improved damage tolerance over unidirectional
   - Shear properties: G12 typically 4-6 GPa for AS4/3501-6
   - Poisson's ratio: ν ≈ 0.3 (isotropic-like behavior)

4. MANUFACTURING CONSIDERATIONS:
   - Hand layup: labor intensive, ply tracking critical
   - Automated fiber placement (AFP): precise control, complex geometries
   - Autoclave cure: 250-350°F, 85-100 psi pressure
   - Vacuum bag pressure: minimum 14.7 psi (vacuum only)
   - Cure cycle monitoring: exotherm control, pressure application timing

5. MATERIAL ALLOWABLES DEVELOPMENT (CMH-17):
   - A-basis: 99% probability, 95% confidence (critical structure)
   - B-basis: 90% probability, 95% confidence (fail-safe structure)
   - Minimum 100 test specimens per material/environment
   - Statistical analysis per MMPDS methodology
   - Environmental knockdown factors: hot/wet conditions

6. ENVIRONMENTAL EFFECTS:
   - Moisture absorption: typical 1.5% saturation for epoxy matrix
   - Hot/wet: Tg reduction, 20-30% compression strength loss
   - Cold/dry: improved properties, potential brittleness
   - UV degradation: surface ply erosion over time
   - Galvanic corrosion: carbon/aluminum interface requires isolation

7. DAMAGE TOLERANCE:
   - BVID (Barely Visible Impact Damage): 0.1 inch dent depth threshold
   - CAI (Compression After Impact): critical design parameter
   - Impact energy: 50 ft-lb typical for 0.125 inch laminate
   - Delamination resistance: improved with toughened resins
   - Repair considerations: scarf vs bolted repairs

The quasi-isotropic layup is the workhorse of aerospace composites, trading
optimal directional stiffness for balanced multi-directional capability and
improved damage tolerance. Proper layup design, cure cycle control, and
statistical allowables establishment per CMH-17 are non-negotiable for
flight-critical structure. Environmental conditioning and damage tolerance
must be characterized for the entire operational envelope.
        """,
        key_factors=[
            "Balanced ply proportions (0/±45/90) for quasi-isotropic properties",
            "Symmetric stacking sequence to prevent warping and coupling",
            "Stacking rules: max 4 consecutive plies, avoid 90/0/90 interfaces",
            "Autoclave cure cycle: temperature, pressure, exotherm control",
            "A-basis and B-basis allowables per CMH-17 statistical methods",
            "Hot/wet environmental knockdown: 20-30% compression strength loss",
            "BVID and CAI characterization for damage tolerance",
            "Surface ply selection: 0° or ±45° for impact resistance"
        ],
        primary_authority=[
            "CMH-17 Composite Materials Handbook (statistical allowables methodology)",
            "FAA AC 20-107B (Composite Aircraft Structure)",
            "ASTM D3039 (Tensile Properties of Polymer Matrix Composites)",
            "ASTM D7136/D7137 (CAI Testing)",
            "Boeing BSS 7260 (Advanced Composite Compression Tests)"
        ],
        burden_holder="Design Engineer",
        adversary_position="Unidirectional layup provides higher stiffness and strength in primary load direction with simpler analysis.",
        counter_arguments=[
            "Quasi-isotropic provides balanced properties critical for multi-directional loading",
            "Improved damage tolerance reduces inspection burden and increases reliability",
            "Standard layup simplifies certification across multiple applications",
            "Easier analysis with isotropic-like properties reduces analytical complexity",
            "Better resistance to off-axis loads and thermal expansion mismatches"
        ],
        resolution_strategy="Use quasi-isotropic for multi-directional loads, damage tolerance requirements, or where load paths are uncertain. Use unidirectional only when load direction is well-defined and damage tolerance can be managed through redundancy.",
        entity_scope="All aerospace composite structure design",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - industry standard practice with extensive qualification heritage",
        controlling_precedent="CMH-17 quasi-isotropic laminate design guidelines",
        category=IssueCategory.COMPOSITE_DESIGN,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Aluminum 7075-T6 vs 2024-T3 Alloy Selection",
        keywords=["aluminum", "7075", "2024", "alloy selection", "temper", "strength", "fracture toughness"],
        conclusion_template="7075-T6 provides higher strength (83 ksi yield) but lower fracture toughness than 2024-T3 (50 ksi yield, superior toughness). Selection depends on whether design is strength-critical or damage-tolerance-critical.",
        reasoning_framework="""
Analysis of aluminum alloy selection for aerospace structure:

1. ALUMINUM 7075-T6 (7xxx SERIES - ZINC):
   - Composition: 5.6% Zn, 2.5% Mg, 1.6% Cu, 0.23% Cr
   - Yield strength: 73-83 ksi (temper dependent)
   - Ultimate tensile: 83-88 ksi
   - Fracture toughness (Kc): 24-28 ksi*sqrt(in.)
   - Fatigue strength: good but inferior to 2024
   - Corrosion resistance: poor without cladding/coating
   - Primary use: high-strength structural members, fittings

2. ALUMINUM 2024-T3 (2xxx SERIES - COPPER):
   - Composition: 4.4% Cu, 1.5% Mg, 0.6% Mn
   - Yield strength: 47-50 ksi
   - Ultimate tensile: 64-70 ksi
   - Fracture toughness (Kc): 60-100 ksi*sqrt(in.) (2-3x better than 7075)
   - Fatigue strength: excellent, superior crack growth resistance
   - Corrosion resistance: moderate, alclad versions available
   - Primary use: fuselage skins, damage-tolerant structure

3. STRENGTH VS TOUGHNESS TRADEOFF:
   - 7075-T6: ~65% higher strength, ~60% lower toughness
   - Strength-critical: landing gear, wing spar caps, highly loaded fittings
   - Toughness-critical: fuselage pressure shells, fail-safe structure
   - Stress corrosion cracking: 7075 susceptible in T6 temper
   - Overaging to T73 temper: improved SCC resistance, 10% strength loss

4. DAMAGE TOLERANCE IMPLICATIONS:
   - Critical crack length: inversely proportional to (Kc/σ)²
   - 2024-T3: larger critical cracks, longer inspection intervals
   - 7075-T6: smaller critical cracks, more frequent inspection
   - da/dN (crack growth rate): 2024 superior across all ΔK levels
   - MSD (Multiple Site Damage): 2024 preferred for fatigue-critical

5. MANUFACTURING CONSIDERATIONS:
   - Formability: 2024-T3 excellent, 7075-T6 poor (requires annealing)
   - Machinability: 7075-T6 good, 2024-T3 moderate (gummy)
   - Weldability: both poor (use mechanical fastening)
   - Heat treatment: 7075 requires solution heat + artificial aging
   - Clad vs bare: alclad adds corrosion protection, reduces strength 5-8%

6. ENVIRONMENTAL DURABILITY:
   - Exfoliation corrosion: 7075 susceptible, requires coating
   - Intergranular corrosion: 2024 resistant in T3 temper
   - Stress corrosion cracking: 7075-T6 highly susceptible (short transverse)
   - Protective finishes: anodize (Type II, Type III), alodine, primer
   - Galvanic compatibility: both require isolation from carbon fiber

7. QUALIFICATION AND CERTIFICATION:
   - MMPDS (Metallic Materials Properties Development and Standardization)
   - Material form: sheet, plate, extrusion, forging (different allowables)
   - Grain direction: L (longitudinal), LT (long transverse), ST (short transverse)
   - ST properties critical for thick sections (directionality effects)
   - Buy-to-fly ratio: 7075 forgings can be 20:1 due to machining

The fundamental tradeoff is strength vs toughness. 7075-T6 is the go-to for
highly loaded structure where stress is the limiting factor and inspectability
is good. 2024-T3 dominates in damage-tolerant design where fatigue, crack growth,
and large critical crack sizes enable safe-life or retire-for-cause philosophy.
Modern transport aircraft use 2024 for fuselage (damage tolerance) and 7075 for
wing structure (strength). The T73 temper of 7075 splits the difference with
improved SCC resistance at slight strength penalty.
        """,
        key_factors=[
            "7075-T6: 73-83 ksi yield, 24-28 ksi*sqrt(in.) toughness (high strength, low toughness)",
            "2024-T3: 47-50 ksi yield, 60-100 ksi*sqrt(in.) toughness (moderate strength, high toughness)",
            "Strength-critical applications favor 7075 (wing spars, landing gear)",
            "Damage-tolerance-critical applications favor 2024 (fuselage, fail-safe structure)",
            "7075 susceptible to stress corrosion cracking in T6 temper (T73 mitigates)",
            "2024 superior fatigue crack growth resistance (da/dN curves)",
            "Both require corrosion protection (anodize, alclad, coatings)",
            "MMPDS provides design allowables with grain direction effects"
        ],
        primary_authority=[
            "MMPDS (Metallic Materials Properties Development and Standardization)",
            "MIL-HDBK-5 (predecessor to MMPDS, historical reference)",
            "ASTM B209 (Aluminum and Aluminum-Alloy Sheet and Plate)",
            "ASTM E399 (Plane-Strain Fracture Toughness Testing)",
            "FAA AC 25.571-1D (Damage Tolerance and Fatigue Evaluation)"
        ],
        burden_holder="Structures Engineer",
        adversary_position="Use highest strength material (7075) for weight savings and structural efficiency.",
        counter_arguments=[
            "Damage tolerance requirements mandate fracture toughness consideration",
            "2024 enables larger critical cracks and longer inspection intervals",
            "Fatigue is often the design driver, where 2024 excels",
            "7075 SCC susceptibility requires costly protective measures",
            "Weight savings from 7075 may be offset by increased inspection burden"
        ],
        resolution_strategy="Use 7075-T6 (or T73) for strength-limited structure with good inspectability. Use 2024-T3 for fatigue and damage-tolerance-critical structure. Hybrid designs use both alloys optimally.",
        entity_scope="All aluminum aerospace structure",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - well-established material property data and design practice",
        controlling_precedent="MMPDS design allowables and FAA damage tolerance regulations",
        category=IssueCategory.ALUMINUM_ALLOYS,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Titanium Ti-6Al-4V Applications and Heat Treatment",
        keywords=["titanium", "ti-6al-4v", "heat treatment", "annealing", "solution treat", "alpha-beta"],
        conclusion_template="Ti-6Al-4V (Grade 5) is the workhorse aerospace titanium alloy, offering 130 ksi yield at room temperature with excellent corrosion resistance. Heat treatment (mill annealed vs STA) controls strength-toughness balance.",
        reasoning_framework="""
Analysis of Ti-6Al-4V titanium alloy for aerospace applications:

1. COMPOSITION AND MICROSTRUCTURE:
   - Nominal composition: 6% Al (alpha stabilizer), 4% V (beta stabilizer)
   - Alpha-beta alloy: two-phase microstructure at room temperature
   - Alpha phase: HCP structure, high strength, low ductility
   - Beta phase: BCC structure, lower strength, high ductility
   - Microstructure control: lamellar vs equiaxed vs bimodal
   - Beta transus: ~1830°F (phase transformation temperature)

2. HEAT TREATMENT CONDITIONS:
   - Mill Annealed: 1300-1450°F / 2-4 hours, air cool
     * Yield: 120-130 ksi, UTS: 130-140 ksi, elongation: 10-15%
     * Equiaxed alpha grains, good balance of properties
   - Solution Treat + Age (STA): 1625-1750°F / quench + 900-1000°F age
     * Yield: 150-170 ksi, UTS: 160-180 ksi, elongation: 6-10%
     * Higher strength, reduced ductility and toughness
   - Beta Anneal: >1830°F, transforms all to beta, slow cool
     * Lamellar microstructure, improved fracture toughness, lower fatigue

3. MECHANICAL PROPERTIES (MILL ANNEALED):
   - Room temp yield: 120-130 ksi
   - Elevated temp (600°F): 90 ksi yield (retains 70% strength)
   - Elevated temp (800°F): 60 ksi yield (50% retention)
   - Fracture toughness: 60-80 ksi*sqrt(in.) (mill annealed)
   - Fatigue strength: 65-75 ksi (smooth specimen, R=-1)
   - Modulus: 16.5 Msi (less than half of steel)

4. CORROSION AND OXIDATION RESISTANCE:
   - Passive TiO2 film: self-healing, excellent corrosion resistance
   - Seawater: virtually immune (better than stainless steel)
   - Salt spray: no degradation (ideal for marine/coastal aircraft)
   - Oxidation: begins ~1000°F, protective scale to ~1500°F
   - Hydrogen embrittlement: susceptible during improper pickling/cleaning
   - Galvanic: cathodic to aluminum (will corrode aluminum in contact)

5. MANUFACTURING CONSIDERATIONS:
   - Machinability: difficult (low thermal conductivity, work hardening)
   - Cutting tools: carbide or PCD required, slow speeds, high feed
   - Welding: GTAW (TIG) common, requires inert gas shielding (argon trailing)
   - Hot forming: 1400-1700°F for significant deformation
   - Superplastic forming: 1600-1700°F, slow strain rates (10^-4 /sec)
   - SPF/DB (Superplastic Forming + Diffusion Bonding): complex hollow structures

6. AEROSPACE APPLICATIONS:
   - Airframe: high-strength fasteners, flap tracks, landing gear components
   - Engines: compressor blades/discs (700-800°F), casings, mounts
   - Weight savings: 40% lighter than steel for same strength
   - Temperature limit: 600-800°F for sustained service (creep onset)
   - High cycle fatigue: excellent notch sensitivity, good in vibration environment
   - Damage tolerance: good fracture toughness in mill annealed condition

7. MATERIAL SPECIFICATION AND PROCUREMENT:
   - AMS 4911: Sheet, strip, plate (annealed)
   - AMS 4928: Bar and billet (annealed)
   - AMS 4965: Castings (annealed)
   - AMS 4967: Forgings (annealed)
   - ASTM B265: General titanium sheet/plate specification
   - Material certifications: chemistry, tensile, grain size, alpha case

Ti-6Al-4V is specified when strength-to-weight ratio, corrosion resistance,
and moderate temperature capability are required. Mill annealed is the default
for good balance. STA is used for maximum strength at cost of toughness.
Beta anneal improves toughness and fatigue at slight strength penalty. The
1000°F temperature limit and difficult machinability are the primary constraints.
Typical applications: landing gear (strength, corrosion resistance), engine
mounts (fatigue, temperature), and any high-strength fastener or bracket where
weight savings justify the 10x material cost vs aluminum.
        """,
        key_factors=[
            "Ti-6Al-4V: alpha-beta alloy, 6% Al (alpha stabilizer), 4% V (beta stabilizer)",
            "Mill annealed: 120-130 ksi yield, 10-15% elongation, balanced properties",
            "Solution treat + age (STA): 150-170 ksi yield, higher strength, lower toughness",
            "Elevated temperature: 70% strength retention at 600°F, 50% at 800°F",
            "Corrosion resistance: excellent via passive TiO2 film (seawater immune)",
            "Difficult machinability: low thermal conductivity, work hardening, carbide tools",
            "Applications: landing gear, engine mounts, fasteners, flap tracks (600-800°F limit)",
            "40% weight savings vs steel, but 10x material cost vs aluminum"
        ],
        primary_authority=[
            "AMS 4911 (Ti-6Al-4V Sheet/Plate Specification)",
            "AMS 4928 (Ti-6Al-4V Bar Specification)",
            "MMPDS (Titanium Design Allowables)",
            "ASM Metals Handbook Vol. 2 (Titanium Properties)",
            "ASTM B265 (Titanium Sheet and Plate)"
        ],
        burden_holder="Materials Engineer",
        adversary_position="Steel or aluminum alloys are cheaper and easier to machine.",
        counter_arguments=[
            "Ti-6Al-4V provides 40% weight savings over steel at equivalent strength",
            "Superior corrosion resistance eliminates coating requirements",
            "Elevated temperature capability (600-800°F) exceeds aluminum",
            "Excellent fatigue properties for vibration-prone applications",
            "Long-term cost savings from reduced maintenance and corrosion"
        ],
        resolution_strategy="Use Ti-6Al-4V where strength-to-weight, corrosion resistance, or moderate temperature capability justify the cost. Use steel for very high loads or temperatures >1000°F. Use aluminum for low-temp, low-cost applications.",
        entity_scope="All aerospace titanium alloy applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - most common aerospace titanium alloy with extensive data",
        controlling_precedent="AMS specifications and MMPDS design allowables",
        category=IssueCategory.TITANIUM_ALLOYS,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Nickel Superalloys for Turbine Hot Section",
        keywords=["superalloy", "inconel", "718", "waspaloy", "turbine", "hot section", "creep", "precipitation hardening"],
        conclusion_template="Inconel 718 and Waspaloy are precipitation-hardened nickel superalloys for gas turbine hot section (1200-1400°F). Selection depends on temperature capability vs fabricability tradeoff.",
        reasoning_framework="""
Analysis of nickel-based superalloys for turbine hot section components:

1. INCONEL 718 (WROUGHT, PRECIPITATION HARDENED):
   - Composition: 52% Ni, 19% Cr, 18% Fe, 5% Nb, 3% Mo, 1% Ti, 0.5% Al
   - Precipitation hardening: Gamma-double-prime (Ni3Nb) coherent precipitates
   - Heat treatment: Solution 1750°F + age 1325°F/8hr + 1150°F/8hr
   - Yield strength: 150 ksi (RT), 140 ksi (1000°F), 120 ksi (1200°F)
   - Temperature limit: 1200°F for sustained service (precipitate dissolution)
   - Fabricability: excellent (weldable, forgeable, machinable)
   - Applications: turbine discs, shafts, casings, combustor cans

2. WASPALOY (WROUGHT, PRECIPITATION HARDENED):
   - Composition: 58% Ni, 19% Cr, 14% Co, 4% Mo, 3% Ti, 1.3% Al
   - Precipitation hardening: Gamma-prime (Ni3(Al,Ti)) coherent precipitates
   - Heat treatment: Solution 1975°F + age 1550°F/4hr + 1400°F/16hr
   - Yield strength: 140 ksi (RT), 130 ksi (1200°F), 110 ksi (1400°F)
   - Temperature limit: 1400°F sustained, 1600°F short-term
   - Fabricability: moderate (difficult welding, requires controlled aging)
   - Applications: turbine blades, vanes, high-temp bolting

3. PRECIPITATION HARDENING MECHANISMS:
   - Gamma-prime: Ni3(Al,Ti), L12 ordered structure, coherent with matrix
   - Gamma-double-prime: Ni3Nb, BCT ordered structure, metastable above 1200°F
   - Coherency strains: impede dislocation motion, provide strengthening
   - Overaging: precipitate coarsening reduces strength
   - Solutioning: dissolve precipitates, recrystallize, then re-age
   - Volume fraction: 15-30% precipitates for optimal strength

4. HIGH-TEMPERATURE CREEP RESISTANCE:
   - Creep: time-dependent plastic deformation under stress at elevated temp
   - Power law: strain rate ∝ stress^n * exp(-Q/RT)
   - Larson-Miller Parameter: LMP = T(°R) * (20 + log(t_rupture))
   - 718: LMP ~40,000 (1000-hr rupture at 1200°F, 100 ksi)
   - Waspaloy: LMP ~43,000 (1000-hr rupture at 1400°F, 80 ksi)
   - Grain size: coarse grains improve creep, fine grains improve fatigue

5. OXIDATION AND CORROSION RESISTANCE:
   - Chromia (Cr2O3) scale: protective oxide at high temperatures
   - Minimum 15% Cr required for oxidation resistance
   - Hot corrosion: sulfate-induced attack from fuel impurities
   - Type I hot corrosion: 1600-1800°F, Na2SO4-induced
   - Type II hot corrosion: 1200-1400°F, low-melting sulfates
   - Coatings: aluminide or MCrAlY overlay coatings for blade protection

6. MANUFACTURING PROCESSES:
   - Forging: isothermal or conventional, requires preheating and slow cooling
   - Machining: difficult (work hardening, abrasive), carbide or ceramic tools
   - Welding: 718 weldable (no cracking), Waspaloy difficult (strain-age cracking)
   - Heat treatment: critical for achieving target properties, tight control
   - Grain flow: forging orientation affects fatigue properties
   - Inspection: 100% ultrasonic for critical rotating parts (disc bore, blade roots)

7. QUALIFICATION AND LIFING:
   - Low cycle fatigue (LCF): thermal cycling, strain-controlled
   - High cycle fatigue (HCF): vibratory stresses, stress-controlled
   - Creep-fatigue interaction: combined damage at elevated temperature
   - Safe-life: retirement at predetermined cycles (no crack propagation assumed)
   - Damage tolerance: rare in hot section (inspectability limited)
   - Lifing models: linear damage rule, strain-range partitioning, fracture mechanics

The 718 vs Waspaloy tradeoff is temperature capability vs fabricability. Inconel 718
dominates for parts up to 1200°F where weldability and forgeability are critical
(discs, cases, structural components). Waspaloy extends to 1400°F for turbine
airfoils and high-temp bolts, accepting more difficult processing. Both rely on
precipitation hardening via coherent intermetallic phases that resist dislocation
motion at temperature. Creep, LCF, and HCF are all design drivers. Hot section
components typically operate on safe-life philosophy due to inspection difficulty
and catastrophic failure consequences. Modern engines push to single-crystal
castings (no grain boundaries) and thermal barrier coatings for even higher
temperatures (1800-2000°F+ turbine inlet).
        """,
        key_factors=[
            "Inconel 718: gamma-double-prime (Ni3Nb) hardened, 1200°F limit, excellent fabricability",
            "Waspaloy: gamma-prime (Ni3(Al,Ti)) hardened, 1400°F limit, difficult fabrication",
            "Precipitation hardening: coherent intermetallic particles impede dislocations",
            "Creep resistance: Larson-Miller Parameter characterizes stress-rupture at temperature",
            "Chromia scale: minimum 15% Cr for oxidation resistance at high temperatures",
            "Low cycle fatigue (LCF) and high cycle fatigue (HCF) both critical design drivers",
            "Safe-life philosophy: retirement at predetermined cycles (hot section norm)",
            "Applications: 718 for discs/cases (weldable), Waspaloy for blades/vanes (higher temp)"
        ],
        primary_authority=[
            "AMS 5663 (Inconel 718 Bar/Forging Specification)",
            "AMS 5704 (Waspaloy Bar Specification)",
            "MMPDS (Superalloy Design Allowables)",
            "ASM Metals Handbook Vol. 1 (Superalloy Properties)",
            "GE Aircraft Engines Design Practices (internal, industry reference)"
        ],
        burden_holder="Propulsion Engineer",
        adversary_position="Lower-cost stainless steels can be used for moderate temperatures.",
        counter_arguments=[
            "Superalloys provide 2-3x strength at 1200°F+ vs austenitic stainless",
            "Creep resistance enables turbine operation at high efficiency (high temp)",
            "Precipitation hardening allows tailored strength via heat treatment",
            "Weight savings critical in rotating components (disc burst margin)",
            "Engine performance directly tied to turbine inlet temperature capability"
        ],
        resolution_strategy="Use Inconel 718 for 1000-1200°F applications requiring weldability and forgeability. Use Waspaloy for 1200-1400°F turbine airfoils. Use single-crystal castings with TBC for >1600°F extreme hot section.",
        entity_scope="All gas turbine hot section applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - industry standard materials with extensive operational history",
        controlling_precedent="AMS specifications and engine OEM design practices",
        category=IssueCategory.SUPERALLOYS,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="S-N Curve Fatigue Analysis and Endurance Limit",
        keywords=["fatigue", "s-n curve", "endurance limit", "high cycle fatigue", "stress amplitude", "mean stress"],
        conclusion_template="S-N (stress-life) curves characterize high cycle fatigue (HCF) endurance. Steel exhibits endurance limit (~50% UTS), while aluminum does not. Mean stress effects require Goodman or Gerber corrections.",
        reasoning_framework="""
Analysis of S-N curve fatigue methodology for aerospace structures:

1. S-N CURVE FUNDAMENTALS:
   - S-N: Stress (S) vs Number of cycles (N) to failure
   - Log-log plot: stress amplitude vs cycles (10^3 to 10^9)
   - High cycle fatigue (HCF): N > 10^4 to 10^5 cycles, elastic strains
   - Low cycle fatigue (LCF): N < 10^4 cycles, plastic strains
   - Endurance limit: stress level below which infinite life is achieved
   - Fatigue strength: stress for given life (e.g., 10^6 cycles)

2. MATERIAL BEHAVIOR - ENDURANCE LIMIT:
   - Steel (ferrous alloys): exhibits endurance limit at ~10^6 cycles
     * Endurance limit ≈ 0.5 * UTS (tensile strength)
     * Below this stress, no fatigue failure (infinite life)
   - Aluminum (non-ferrous): NO endurance limit
     * S-N curve continues to decline (fatigue strength at 5x10^8 cycles used)
     * Fatigue strength ≈ 0.3-0.4 * UTS at 10^8 cycles
   - Titanium: similar to aluminum, no true endurance limit
   - Composites: anisotropic, matrix-dominated fatigue below endurance

3. MEAN STRESS EFFECTS (GOODMAN CORRECTION):
   - Fully reversed: mean stress = 0, R = σ_min / σ_max = -1
   - Pulsating tension: mean > 0, R = 0 (min stress = 0)
   - Goodman relation: σ_a / σ_e + σ_m / σ_uts = 1
     * σ_a = stress amplitude (alternating)
     * σ_m = mean stress
     * σ_e = endurance limit (fully reversed)
     * σ_uts = ultimate tensile strength
   - Gerber relation: (σ_a / σ_e)² + (σ_m / σ_uts)² = 1 (less conservative)
   - Modified Goodman: more conservative, commonly used in aerospace

4. STRESS CONCENTRATION EFFECTS (Kt vs Kf):
   - Kt (theoretical stress concentration): geometry-based
     * Kt = σ_max / σ_nom (elastic stress concentration)
     * Hole: Kt ≈ 3, sharp notch: Kt = 5-10+
   - Kf (fatigue notch factor): accounts for material sensitivity
     * Kf = 1 + q(Kt - 1), where q = notch sensitivity (0 to 1)
     * q increases with material strength and notch radius
   - Fatigue stress concentration reduces allowable stress significantly
   - Notch radius: increasing radius reduces Kt (blending critical)

5. SURFACE FINISH AND TREATMENT EFFECTS:
   - Surface finish factor: polished = 1.0, machined = 0.9, as-rolled = 0.7
   - Shot peening: induces compressive residual stress, improves fatigue 20-50%
   - Anodizing (aluminum): Type II minimal effect, Type III can reduce fatigue
   - Corrosion pits: act as stress concentrations, severely degrade fatigue
   - Surface treatments critical for fatigue-critical components

6. TESTING AND DATA GENERATION:
   - ASTM E466: Constant amplitude axial fatigue testing
   - Minimum 10-12 specimens per S-N curve (statistical variation)
   - R-ratio testing: R = -1 (fully reversed), R = 0.1 (tension-tension)
   - Stress ratio: different R-ratios produce different S-N curves
   - Scatter: fatigue data has large scatter (factor of 2-3 in life)
   - Design curves: typically mean - 3 standard deviations (99.9% survival)

7. DESIGN APPLICATIONS:
   - Safe-life: design for finite life, retire before fatigue failure
   - Fail-safe: assume fatigue crack, design for residual strength
   - Damage tolerance: assume crack exists, demonstrate slow growth
   - Scatter factor: 4 on life (S-N approach) for safe-life design
   - Inspection intervals: based on crack growth analysis (damage tolerance)
   - Component examples: engine rotating components (HCF), landing gear (LCF+HCF)

S-N curves are the foundation of high cycle fatigue analysis for aerospace
components subjected to millions of stress cycles. The key insights are:
(1) steel has endurance limit, aluminum does not; (2) mean stress significantly
reduces fatigue strength (Goodman correction); (3) stress concentrations (Kt/Kf)
are fatigue killers requiring careful design; (4) surface finish and treatments
directly impact fatigue life. Modern damage-tolerant design often uses fracture
mechanics (da/dN) instead of S-N for fail-safe structure, but S-N remains the
workhorse for HCF analysis of rotating machinery, landing gear, and other
highly cycled components where cracks are not assumed to exist initially.
        """,
        key_factors=[
            "S-N curve: stress amplitude vs cycles to failure (log-log plot)",
            "Steel: endurance limit at ~10^6 cycles (~0.5 * UTS), aluminum has none",
            "Mean stress: Goodman relation (σ_a/σ_e + σ_m/σ_uts = 1) reduces allowable",
            "Stress concentration: Kf (fatigue notch factor) = 1 + q(Kt - 1)",
            "Surface finish: polished = 1.0, machined = 0.9, as-rolled = 0.7 (multipliers)",
            "Shot peening: compressive residual stress improves fatigue 20-50%",
            "Design curves: mean - 3σ for 99.9% survival, scatter factor of 4 on life",
            "Applications: HCF for engine rotors, landing gear, airframe highly cycled components"
        ],
        primary_authority=[
            "ASTM E466 (Constant Amplitude Axial Fatigue Testing)",
            "MIL-HDBK-5 / MMPDS (S-N Data for Aerospace Alloys)",
            "Shigley's Mechanical Engineering Design (Fatigue Analysis Methods)",
            "FAA AC 25.571-1D (Fatigue Evaluation of Structure)",
            "ASME Boiler Code Section VIII (Fatigue Design Curves)"
        ],
        burden_holder="Fatigue and Damage Tolerance Engineer",
        adversary_position="Static strength analysis is sufficient for low-cycle applications.",
        counter_arguments=[
            "Fatigue is cumulative and occurs at stresses well below static failure",
            "High cycle fatigue dominates in vibration and rotating component environments",
            "Mean stress and stress concentrations significantly reduce fatigue capability",
            "Statistical scatter in fatigue requires conservative design factors",
            "Inspection and retirement schedules depend on accurate fatigue analysis"
        ],
        resolution_strategy="Use S-N curves for HCF analysis of components with stress cycles >10^5. Apply Goodman corrections for mean stress. Account for Kf and surface finish. Use fracture mechanics (da/dN) for damage-tolerant fail-safe analysis.",
        entity_scope="All fatigue-critical aerospace components",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - fundamental fatigue methodology validated over decades",
        controlling_precedent="ASTM E466 and MMPDS S-N data",
        category=IssueCategory.FATIGUE_ANALYSIS,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Paris Law Crack Growth and Damage Tolerance",
        keywords=["crack growth", "paris law", "damage tolerance", "fracture mechanics", "stress intensity", "da/dn"],
        conclusion_template="Paris Law (da/dN = C * ΔK^m) governs fatigue crack propagation in damage-tolerant design. Critical crack size derived from K_Ic and applied stress enables inspection interval determination.",
        reasoning_framework="""
Analysis of Paris Law crack growth for damage tolerance methodology:

1. PARIS LAW FUNDAMENTALS:
   - da/dN = C * (ΔK)^m
     * da/dN = crack growth rate (inch/cycle)
     * ΔK = stress intensity range = K_max - K_min
     * C, m = material constants from testing
   - Log-log plot: log(da/dN) vs log(ΔK) is linear (Region II)
   - Region I: threshold (ΔK_th), very slow growth
   - Region II: Paris Law regime, stable crack growth
   - Region III: rapid acceleration approaching K_Ic

2. STRESS INTENSITY FACTOR (K):
   - K = σ * sqrt(π*a) * Y (geometry correction)
     * σ = applied stress
     * a = crack length (half-crack for through-crack, full depth for surface)
     * Y = geometry factor (1.0 for infinite plate, >1.0 for finite geometry)
   - K_Ic = fracture toughness (critical stress intensity)
   - Critical crack: a_crit = (K_Ic / (σ * Y))² / π
   - Crack becomes unstable when K reaches K_Ic

3. MATERIAL CRACK GROWTH PROPERTIES:
   - Aluminum 2024-T3: C ≈ 3x10^-8, m ≈ 3.2 (inch, ksi, cycles)
   - Aluminum 7075-T6: C ≈ 5x10^-8, m ≈ 3.0 (faster growth than 2024)
   - Titanium Ti-6Al-4V: C ≈ 1.5x10^-8, m ≈ 3.5
   - Steel 4340: C ≈ 6x10^-10, m ≈ 3.0 (slower growth)
   - Threshold ΔK_th: 2-4 ksi*sqrt(in.) for most aerospace alloys
   - Environment: moisture, salt spray increase crack growth rate

4. INSPECTION INTERVAL DETERMINATION:
   - Initial crack assumption: a_i (typically detectable flaw size)
     * Visual: 0.05-0.10 inch
     * Eddy current: 0.03 inch
     * Ultrasonic: 0.01 inch
   - Final crack: a_f = a_crit / Factor of Safety (FoS ≈ 2)
   - Crack growth integration: N = ∫[da / C*(ΔK)^m] from a_i to a_f
   - Inspection interval: N / 2 (factor of 2 safety on life)
   - Repeat inspections: detect cracks before they reach critical size

5. R-RATIO EFFECTS (STRESS RATIO):
   - R = K_min / K_max = σ_min / σ_max
   - Fully reversed: R = -1 (compression to tension)
   - Tension-tension: R = 0.1 to 0.7
   - Walker equation: accounts for R-ratio effects on da/dN
   - Higher R-ratio: faster crack growth (less crack closure)
   - Compression (R < 0): crack closure reduces effective ΔK

6. RETARDATION AND VARIABLE AMPLITUDE:
   - Overload retardation: single large load slows subsequent growth
     * Plastic zone at crack tip creates compressive residual stress
     * Retardation factor can extend life 2-5x
   - Variable amplitude: flight-by-flight spectrum loading
     * Rainflow counting: extract stress cycles from spectrum
     * Linear damage rule: sum cycle damage (Miner's rule)
   - Crack closure: premature contact of crack faces reduces effective ΔK

7. DAMAGE TOLERANCE PHILOSOPHY:
   - Assume crack exists (initial quality, fatigue nucleation, or service damage)
   - Demonstrate sufficient residual strength with crack
   - Establish inspection program to detect cracks before critical
   - Slow crack growth: enables economic inspection intervals
   - Fail-safe: alternate load paths if primary cracks
   - Certification: 14 CFR 25.571 mandates damage tolerance evaluation

Paris Law enables quantitative damage tolerance analysis. By characterizing
material da/dN vs ΔK behavior, engineers can predict crack growth life from
assumed initial flaw to critical size, establishing inspection intervals to
detect and repair cracks before failure. The methodology assumes cracks exist
(conservative for certification) and relies on slow, stable crack propagation
in Region II. Critical parameters are fracture toughness K_Ic (sets critical
crack size) and Paris constants C, m (set growth rate). This has revolutionized
aerospace structural integrity, moving from safe-life (no cracks assumed) to
damage-tolerant (cracks assumed, managed via inspection). Modern transport
aircraft fuselages are designed entirely on damage tolerance principles,
with periodic inspections detecting fatigue cracks for repair before they
threaten structural integrity.
        """,
        key_factors=[
            "Paris Law: da/dN = C * (ΔK)^m governs stable crack growth (Region II)",
            "Stress intensity: K = σ * sqrt(π*a) * Y, critical when K = K_Ic",
            "Critical crack: a_crit = (K_Ic / σ*Y)² / π determines failure size",
            "Inspection interval: integrate Paris Law from initial to final crack / 2",
            "Material constants: 2024-T3 slower growth than 7075-T6 (better damage tolerance)",
            "Initial flaw assumption: 0.05-0.10 inch (visual), 0.01 inch (UT)",
            "R-ratio effects: higher R = faster growth (less crack closure)",
            "Damage tolerance philosophy: assume cracks exist, demonstrate residual strength + inspections"
        ],
        primary_authority=[
            "14 CFR 25.571 (Damage Tolerance and Fatigue Evaluation)",
            "FAA AC 25.571-1D (Damage Tolerance Advisory Circular)",
            "ASTM E647 (Fatigue Crack Growth Rate Testing)",
            "NASGRO (Fracture Mechanics Software and Database)",
            "Anderson, Fracture Mechanics: Fundamentals and Applications"
        ],
        burden_holder="Damage Tolerance Engineer",
        adversary_position="Safe-life design (no cracks assumed) is simpler and doesn't require inspections.",
        counter_arguments=[
            "Damage tolerance accounts for real-world flaws and fatigue initiation",
            "Inspection programs detect cracks early, preventing catastrophic failures",
            "Paris Law enables quantitative life prediction with safety factors",
            "Regulatory requirement (14 CFR 25.571) for transport aircraft",
            "Economic: allows longer service life with managed inspections vs early retirement"
        ],
        resolution_strategy="Use damage tolerance for fail-safe and inspection-accessible structure (fuselage, wings). Use safe-life for non-inspectable or catastrophic single-failure components (engine discs). Hybrid approach common.",
        entity_scope="All damage-tolerant aerospace structure",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - regulatory mandate with extensive validation",
        controlling_precedent="14 CFR 25.571 and FAA AC 25.571-1D",
        category=IssueCategory.DAMAGE_TOLERANCE,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="CMH-17 Statistical Allowables Development",
        keywords=["cmh-17", "statistical allowables", "a-basis", "b-basis", "material qualification", "basis values"],
        conclusion_template="CMH-17 methodology establishes A-basis (99% probability, 95% confidence) and B-basis (90/95) material allowables through statistical analysis of minimum 100 test specimens per material/environment/direction.",
        reasoning_framework="""
Analysis of CMH-17 statistical allowables development for aerospace composites:

1. BASIS VALUE DEFINITIONS:
   - A-basis: 99% of population exceeds value, 95% confidence
     * Used for critical structure (single load path, catastrophic failure)
     * Minimum 100 specimens required (299 for improved accuracy)
     * Example: wing spar cap (primary bending member)
   - B-basis: 90% of population exceeds value, 95% confidence
     * Used for fail-safe structure (redundant load paths)
     * Minimum 30 specimens (100 preferred)
     * Example: fuselage skin (multiple frames provide alternate paths)
   - Typical (mean) basis: 50% of population (not used for design)

2. SPECIMEN REQUIREMENTS AND TEST MATRIX:
   - Material forms: prepreg batch, fabric lot, resin lot variability
   - Fiber orientations: 0°, 90°, ±45° (unidirectional and fabric)
   - Laminate configurations: unidirectional, quasi-isotropic, fabric
   - Environmental conditions: CTD (Cold-Temperature-Dry), RTD, ETW (Elevated-Temp-Wet), ETD
   - Test types: tension, compression, shear, bearing, open-hole, filled-hole
   - Minimum test matrix: 6 environments × 3 orientations × 5 test types = 90+ test series

3. STATISTICAL ANALYSIS METHODOLOGY:
   - Normal distribution assumption: verify with Anderson-Darling, Shapiro-Wilk
   - Outlier detection: Dixon's test, Grubbs' test (remove only if justified)
   - One-sided tolerance limit: X̄ - k*s
     * X̄ = sample mean
     * s = sample standard deviation
     * k = tolerance limit factor (from tables, depends on n, basis, confidence)
   - A-basis, n=100: k ≈ 3.0-3.5 (99/95 one-sided)
   - B-basis, n=100: k ≈ 2.0-2.3 (90/95 one-sided)

4. ENVIRONMENTAL KNOCKDOWN FACTORS:
   - Hot/wet (180°F, moisture saturated): most severe for compression
     * Compression strength: 60-80% of CTD (20-40% knockdown)
     * Tg depression: epoxy matrix softens with moisture
     * Compression failure: matrix-dominated (kink band formation)
   - Cold/dry (-65°F): typically improves properties slightly
   - Elevated/dry (180°F): moderate knockdown (10-20%)
   - Moisture absorption: 1.0-1.5% weight gain at saturation (epoxy)

5. FIBER AND RESIN VARIABILITY:
   - Fiber: tensile strength variability 5-10% CoV (Coefficient of Variation)
   - Resin: compression and shear variability 10-20% CoV
   - Prepreg: fiber areal weight (FAW), resin content (RC) batch variability
   - Qualification: establish process limits (FAW ± 5%, RC ± 3%)
   - Requalification: required for process changes outside limits

6. LAMINA VS LAMINATE PROPERTIES:
   - Lamina: single ply properties (0°, 90°, ±45°)
     * Measure: E1, E2, G12, ν12, F1t, F1c, F2t, F2c, F6 (shear)
   - Laminate: multi-ply laminate properties (quasi-isotropic, fabric)
     * Classical lamination theory (CLT): predict from lamina + stacking
     * Test validation: quasi-isotropic tension, compression, shear
   - Open-hole and filled-hole: notch sensitivity, bearing-bypass interaction

7. MATERIAL QUALIFICATION PROCESS:
   - Material specification: chemistry, process, cure cycle
   - Screening tests: initial evaluation (small sample size)
   - Qualification tests: full test matrix, 100+ specimens per cell
   - Statistical analysis: basis value calculation, pooling analysis
   - Material qualification report: document all data, analysis, basis values
   - Approval: submit to CMH-17 for industry-wide acceptance
   - Time and cost: 12-24 months, $500K-$2M for full qualification

CMH-17 statistical allowables are the gold standard for aerospace composite
material qualification. The methodology rigorously characterizes material
variability through extensive testing (100+ specimens) and applies statistical
tolerance limits to establish design values with high confidence. A-basis
(99/95) is used for critical single-load-path structure where failure is
catastrophic. B-basis (90/95) is used for fail-safe redundant structure.
The hot/wet environmental condition typically drives compression allowables,
with 20-40% knockdowns common. Fiber properties are relatively consistent
(low variability), while matrix-dominated properties (compression, shear) show
higher variability. The entire process takes 1-2 years and significant cost,
but produces statistically defensible design allowables accepted across the
aerospace industry. Modern efforts focus on reducing test requirements through
virtual testing and building-block approaches, but the CMH-17 framework remains
the certification standard.
        """,
        key_factors=[
            "A-basis: 99% probability, 95% confidence (critical structure, single load path)",
            "B-basis: 90% probability, 95% confidence (fail-safe, redundant structure)",
            "Minimum specimens: 100 for A-basis, 30 for B-basis (more is better)",
            "Statistical method: one-sided tolerance limit X̄ - k*s (k from tables)",
            "Hot/wet environment: 20-40% compression knockdown (matrix softening)",
            "Test matrix: 6 environments × 3 orientations × 5 test types = 90+ series",
            "Qualification: 12-24 months, $500K-$2M for full material dataset",
            "CMH-17 approval: industry-wide acceptance for certified aircraft"
        ],
        primary_authority=[
            "CMH-17 Composite Materials Handbook (Volumes 1-6)",
            "ASTM D3039 (Tensile Testing of Composites)",
            "ASTM D6641 (Compression Testing of Composites)",
            "ASTM D5379 (Shear Testing V-Notched Beam)",
            "FAA AC 20-107B (Composite Aircraft Structure)"
        ],
        burden_holder="Materials and Process Engineer",
        adversary_position="Manufacturer's typical data is sufficient for design.",
        counter_arguments=[
            "Certification requires statistically-based allowables with defined confidence",
            "Material variability (batch-to-batch) necessitates large sample sizes",
            "A-basis provides safety margin for critical single-failure-point structure",
            "Environmental knockdowns (hot/wet) are substantial and must be characterized",
            "CMH-17 approval provides industry-wide credibility and regulatory acceptance"
        ],
        resolution_strategy="Use CMH-17 methodology for certified aircraft structure. Use manufacturer's typical data only for preliminary design or non-critical applications. Building-block testing reduces cost while maintaining statistical rigor.",
        entity_scope="All aerospace composite material qualification",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - industry and regulatory standard",
        controlling_precedent="CMH-17 and FAA AC 20-107B",
        category=IssueCategory.MATERIAL_QUALIFICATION,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="BVID and Compression After Impact (CAI) Testing",
        keywords=["bvid", "impact damage", "compression after impact", "cai", "delamination", "damage tolerance"],
        conclusion_template="BVID (Barely Visible Impact Damage) threshold typically 0.10 inch dent depth. CAI (Compression After Impact) testing per ASTM D7137 establishes residual strength after impact for composite damage tolerance.",
        reasoning_framework="""
Analysis of impact damage and CAI testing for composite damage tolerance:

1. BVID DEFINITION AND SIGNIFICANCE:
   - BVID: impact damage barely visible to naked eye (0.10 inch dent depth typical)
   - Damage mechanisms: matrix cracking, delamination, fiber breakage
   - Surface visibility: small dent, paint cracking, but no obvious penetration
   - Internal damage: delaminations 2-5x larger than visible surface damage
   - Design philosophy: structure must sustain limit load with BVID present
   - Inspection: BVID may not be detected during walk-around inspections

2. IMPACT ENERGY AND DAMAGE CORRELATION:
   - Impact energy: E = m*v²/2 (mass × velocity²)
   - Typical aircraft threats: tool drops, hail, runway debris, service vehicle impact
   - Energy levels: 50-100 ft-lb for 0.125-0.25 inch thick laminates
   - Dent depth: correlates with impact energy and laminate stiffness
   - Threshold: 0.10 inch dent = BVID, 0.20+ inch = VID (Visible Impact Damage)
   - Contact area: hemispherical impactor (1-2 inch diameter typical)

3. DAMAGE MECHANISMS (COMPOSITE IMPACT):
   - Top surface: matrix cracking in compression (impactor contact)
   - Delamination: interlaminar failure between plies (primary damage)
   - Bottom surface: tensile fiber failure (bending-induced)
   - Peanut-shaped delamination: larger at deeper interfaces
   - Damage volume: truncated cone or peanut shape through thickness
   - Quasi-isotropic: more delamination than unidirectional (mismatch in ply angles)

4. ASTM D7137 CAI TEST PROCEDURE:
   - Specimen: 5 inch × 10 inch flat panel, 0.125-0.25 inch thick
   - Impact: ASTM D7136 drop-weight impact (50-100 ft-lb to achieve BVID)
   - Measurement: dent depth with depth gage (0.001 inch resolution)
   - Compression fixture: anti-buckling guide (prevents Euler buckling)
   - Loading: compression along 5 inch dimension until failure
   - Failure: typically delamination propagation leading to buckling/crushing
   - CAI strength: residual compression strength (ksi)

5. CAI STRENGTH TRENDS AND DESIGN VALUES:
   - Baseline (unidirectional): 50-60 ksi compression strength
   - Post-impact (BVID): 30-40 ksi CAI (40-50% retention)
   - Quasi-isotropic: better CAI retention than unidirectional (damage arrest)
   - Toughened resins: 8552, 977-3 improve CAI 10-20% over 3501-6
   - Thin laminates: lower CAI (less confinement of damage)
   - Thick laminates: better CAI (damage more confined)

6. DESIGN ALLOWABLES AND CERTIFICATION:
   - No-growth threshold: impact energy that produces no strength loss
     * Typically 5-15 ft-lb for aerospace laminates
   - Damage tolerance: design ultimate load with BVID damage present
   - Allowables: mean CAI - 3 standard deviations (statistical)
   - Damage size: assume BVID over large area (conservative)
   - Inspection threshold: define energy above which repair required

7. MITIGATION STRATEGIES:
   - Toughened resins: thermoplastic-modified epoxy (8552, 977-3, CYCOM 5320)
   - Fiber architecture: woven fabric, stitching, z-pins through-thickness
   - Hybrid laminates: GFRP surface plies (better impact resistance)
   - Protective coatings: polyurethane film, Tedlar, sacrificial layers
   - Design: avoid single-load-path critical structure in impact-prone areas
   - Inspection: periodic ultrasonic or thermographic inspection for hidden damage

BVID and CAI testing establish the residual strength of composite structure
after impact damage that may not be visible during routine inspections. The
0.10 inch dent depth threshold defines BVID, and the structure must sustain
limit load with this damage present (damage tolerance requirement). CAI testing
per ASTM D7137 quantifies the compression strength after standardized impact,
typically showing 40-60% retention vs undamaged baseline. Design allowables
are established using statistical analysis of CAI data. Toughened resins,
woven fabrics, and through-thickness reinforcement improve CAI performance.
The fundamental challenge is that impact creates subsurface delaminations
far larger than the visible dent, and these delaminations propagate under
compression loading, leading to premature failure. CAI is a critical design
parameter for composite fuselage and wing skins, and has driven significant
material development toward toughened resin systems.
        """,
        key_factors=[
            "BVID threshold: 0.10 inch dent depth (barely visible, may escape detection)",
            "Subsurface delaminations: 2-5x larger than visible surface damage",
            "ASTM D7137 CAI: compression test after ASTM D7136 impact",
            "CAI retention: 40-60% of undamaged strength (material dependent)",
            "Toughened resins: 8552, 977-3 improve CAI 10-20% over 3501-6",
            "Design requirement: sustain limit load with BVID present",
            "Damage mechanisms: matrix cracking, delamination, fiber breakage",
            "Mitigation: toughened resins, woven fabrics, z-pins, protective coatings"
        ],
        primary_authority=[
            "ASTM D7136 (Measuring Damage Resistance of Composites Under Drop-Weight Impact)",
            "ASTM D7137 (Compressive Residual Strength After Impact)",
            "FAA AC 20-107B (Composite Aircraft Structure)",
            "CMH-17 Volume 3 (Damage Resistance and Tolerance)",
            "Boeing BSS 7260 (Advanced Composite Compression Tests)"
        ],
        burden_holder="Composite Structures Engineer",
        adversary_position="Design for no impact damage (protective measures sufficient).",
        counter_arguments=[
            "Impact damage is inevitable in service (tools, hail, debris, service equipment)",
            "BVID may not be detected during routine walk-around inspections",
            "Damage tolerance requires demonstrating residual strength with damage present",
            "FAA certification (14 CFR 25.571) mandates damage tolerance evaluation",
            "CAI testing provides quantitative data for allowables and safety margin"
        ],
        resolution_strategy="Design for damage tolerance with BVID assumption. Use CAI testing to establish allowables. Implement protective measures where practical. Define inspection thresholds for repair.",
        entity_scope="All composite aerospace structure subject to impact",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - regulatory requirement with standard test methods",
        controlling_precedent="ASTM D7137 and FAA AC 20-107B",
        category=IssueCategory.DAMAGE_TOLERANCE,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Corrosion Protection Schemes for Aluminum Alloys",
        keywords=["corrosion", "anodize", "alodine", "primer", "alclad", "chromate", "protection"],
        conclusion_template="Aluminum corrosion protection requires multi-layer system: alclad or conversion coating (alodine) + primer + topcoat. Anodizing (Type II/III) provides enhanced protection for high-risk areas.",
        reasoning_framework="""
Analysis of corrosion protection for aerospace aluminum alloys:

1. CORROSION MECHANISMS IN ALUMINUM:
   - General corrosion: uniform surface attack (white powder Al2O3)
   - Pitting corrosion: localized penetration (chloride environments)
   - Intergranular corrosion: grain boundary attack (improper heat treatment)
   - Exfoliation corrosion: layer-by-layer separation (7xxx alloys)
   - Stress corrosion cracking (SCC): combined stress + corrosive environment
   - Galvanic corrosion: aluminum anodic to steel, titanium, carbon fiber

2. ALCLAD ALUMINUM (SACRIFICIAL LAYER):
   - Cladding: pure aluminum (1230) or Al-1%Zn (7072) rolled onto core alloy
   - Thickness: 2.5-5% per side (0.003-0.005 inch on 0.125 inch sheet)
   - Mechanism: sacrificial anode protects core alloy
   - Strength penalty: 5-10% reduction vs bare alloy (cladding is soft)
   - Applications: fuselage skins, wing skins (corrosion-prone areas)
   - Limitations: edge protection still required (cladding not on edges)

3. CHEMICAL CONVERSION COATINGS (ALODINE/IRIDITE):
   - Chromate conversion (MIL-DTL-5541 Type I): hexavalent chromium
     * Yellow-gold iridescent film, 0.00001-0.00005 inch thick
     * Excellent paint adhesion and corrosion protection
     * Environmental concerns: Cr(VI) toxic, being phased out
   - Non-chromate conversion (MIL-DTL-5541 Type II): trivalent chromium or non-Cr
     * Clear to light tan film, slightly inferior performance
     * Environmentally compliant (Cr(VI) banned in EU, restricted in US)
   - Process: immersion or spray, acid etch + conversion solution
   - Applications: all aluminum parts prior to priming

4. ANODIZING (ELECTROCHEMICAL OXIDE):
   - Type II (MIL-A-8625 Type II): sulfuric acid anodize
     * Film thickness: 0.0002-0.001 inch
     * Hardness: Rockwell 40-70 (depending on alloy and thickness)
     * Corrosion protection: good, sealed film is best
     * Color: clear, can be dyed for identification
     * Applications: brackets, fittings, interior parts
   - Type III (MIL-A-8625 Type III): hard coat anodize
     * Film thickness: 0.001-0.004 inch
     * Hardness: Rockwell 60-70+ (very hard, wear-resistant)
     * Corrosion protection: excellent, thicker film
     * Color: dark gray to black (dyes not effective)
     * Applications: high-wear areas, severe corrosion environment
   - Fatigue penalty: anodize can reduce fatigue 10-30% (surface tensile stress)
   - Sealing: hot water or dichromate seal (closes pores, improves corrosion resistance)

5. PRIMER SYSTEMS:
   - Epoxy primer (MIL-PRF-23377): standard for aerospace
     * Chromate-pigmented (yellow): traditional, excellent corrosion inhibition
     * Non-chromate (gray/green): modern, environmentally compliant
     * Dry film thickness: 0.0003-0.0008 inch (0.3-0.8 mil)
   - Wash primer (MIL-C-8514): thin etch primer for difficult substrates
   - Application: spray (HVLP, electrostatic), brush for touch-up
   - Cure: air dry, force dry (140-180°F), or 2-part catalyzed

6. TOPCOAT SYSTEMS:
   - Polyurethane topcoat (MIL-PRF-85285): 2-part, UV-resistant
     * Aliphatic polyurethane: maintains color and gloss
     * Color: white, gray, tactical colors (infrared reflectivity)
     * Dry film thickness: 0.001-0.003 inch (1-3 mil)
   - Epoxy topcoat: not UV-stable, chalks and fades (used for interior)
   - Camouflage: IR-reflective pigments for signature reduction

7. SYSTEM SELECTION AND BEST PRACTICES:
   - STANDARD (exterior structure): alclad or alodine + epoxy primer + polyurethane topcoat
   - HIGH CORROSION (landing gear, marine): Type III anodize + epoxy primer + polyurethane
   - INTERIOR (cabin, cargo): alodine + epoxy primer (topcoat optional)
   - FASTENER HOLES: wet install with sealant (PR-1422, PR-1776)
   - Galvanic isolation: glass fabric, sealant, or isolation washers (Al/CF interface)
   - Edge sealing: primer + sealant on all sheared/machined edges
   - Touchup: any damage to coating must be repaired (bare aluminum rapidly corrodes)

Effective corrosion protection for aluminum aerospace structure requires a
multi-layer barrier system. Alclad provides sacrificial anode protection but
has strength penalty. Conversion coatings (alodine) provide paint adhesion and
light corrosion protection. Anodizing (Type II or III) provides hard, thick
oxide for severe environments but can reduce fatigue. Primer (epoxy, chromate or
non-chromate) is the primary corrosion barrier. Topcoat (polyurethane) provides
UV protection and aesthetic finish. The standard exterior system is alodine +
epoxy primer + polyurethane topcoat. High-corrosion areas (landing gear, marine)
use Type III anodize. Fastener holes are wet-installed with sealant. Galvanic
couples (aluminum/carbon fiber, aluminum/steel) require isolation. Any damage
to the coating system must be repaired promptly, as bare aluminum corrodes
rapidly in humid or salt environments.
        """,
        key_factors=[
            "Alclad: 2.5-5% sacrificial aluminum cladding, 5-10% strength penalty",
            "Alodine (conversion coating): chromate (Type I) or non-chromate (Type II) adhesion layer",
            "Anodize Type II: 0.0002-0.001 inch sulfuric acid oxide, good corrosion protection",
            "Anodize Type III: 0.001-0.004 inch hard coat, excellent protection but fatigue penalty",
            "Epoxy primer: chromate or non-chromate, 0.3-0.8 mil primary corrosion barrier",
            "Polyurethane topcoat: UV-resistant, 1-3 mil, maintains color and gloss",
            "Galvanic isolation: required for Al/CF or Al/steel interfaces",
            "Standard system: alodine + epoxy primer + polyurethane topcoat"
        ],
        primary_authority=[
            "MIL-DTL-5541 (Chemical Conversion Coatings)",
            "MIL-A-8625 (Anodic Coatings for Aluminum)",
            "MIL-PRF-23377 (Epoxy Primer)",
            "MIL-PRF-85285 (Polyurethane Topcoat)",
            "ASTM B117 (Salt Spray Testing)"
        ],
        burden_holder="Corrosion Control Engineer",
        adversary_position="Bare aluminum with periodic recoating is sufficient.",
        counter_arguments=[
            "Corrosion initiates rapidly in bare aluminum (especially 2024, 7075)",
            "Multi-layer system provides defense-in-depth against coating damage",
            "Touchup is difficult in service; initial complete coating is critical",
            "Galvanic corrosion (Al/CF) is severe without isolation",
            "Long-term maintenance cost of corrosion far exceeds initial protection cost"
        ],
        resolution_strategy="Use alodine + epoxy primer + polyurethane topcoat as standard. Upgrade to alclad or Type III anodize for high-risk areas. Isolate galvanic couples. Wet-install fasteners with sealant.",
        entity_scope="All aluminum aerospace structure",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - industry standard practice",
        controlling_precedent="MIL specifications for coatings",
        category=IssueCategory.CORROSION_PROTECTION,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Additive Manufacturing Qualification for Aerospace",
        keywords=["additive manufacturing", "3d printing", "laser powder bed fusion", "ti-6al-4v", "qualification", "porosity"],
        conclusion_template="Laser powder bed fusion (L-PBF) Ti-6Al-4V qualification requires porosity control (<0.2% typical), HIP post-processing, mechanical testing per ASTM F3049/F3301, and fractography to validate build quality.",
        reasoning_framework="""
Analysis of additive manufacturing qualification for aerospace applications:

1. L-PBF PROCESS FUNDAMENTALS (TITANIUM):
   - Laser Powder Bed Fusion (L-PBF): layer-by-layer melting of metal powder
   - Powder: Ti-6Al-4V spherical atomized, -45/+15 micron size distribution
   - Laser: 200-400W fiber laser, 50-100 micron spot size
   - Layer thickness: 30-60 micron (0.001-0.002 inch)
   - Build rate: 5-20 cm³/hour (very slow vs conventional manufacturing)
   - Inert atmosphere: argon or nitrogen (prevent oxidation)
   - Part orientation: affects surface finish, residual stress, support structure

2. MICROSTRUCTURE AND AS-BUILT PROPERTIES:
   - Microstructure: acicular alpha-prime (martensitic) due to rapid cooling
   - Grain structure: columnar grains aligned with build direction (anisotropy)
   - Residual stress: high tensile (thermal gradients), can cause warping/cracking
   - As-built strength: 130-140 ksi yield (higher than wrought due to fine microstructure)
   - As-built ductility: 5-10% elongation (lower than wrought)
   - Fatigue: as-built surface is poor (rough, stress concentrations)

3. DEFECTS AND POROSITY CONTROL:
   - Lack-of-fusion: incomplete melting between layers (irregular voids)
   - Gas porosity: trapped argon or powder contamination (spherical voids)
   - Keyholing: excessive energy input causes vapor cavity collapse (elongated voids)
   - Porosity target: <0.2% for aerospace (CT scan or Archimedes density)
   - Process parameters: laser power, scan speed, hatch spacing optimization
   - Powder quality: moisture, contamination, reuse limits (max 5-10 builds)

4. POST-PROCESSING (CRITICAL FOR QUALIFICATION):
   - Stress relief: 650-750°F / 2 hours (reduce residual stress, prevent distortion)
   - Hot Isostatic Pressing (HIP): 1650-1750°F, 15-30 ksi pressure, 2-4 hours
     * Closes internal porosity to <0.01%
     * Improves ductility and fatigue (critical for aerospace)
     * Microstructure: transforms alpha-prime to alpha+beta (more ductile)
   - Machining: remove support structure, machine critical surfaces to tolerance
   - Surface finishing: shot peening, polishing, or machining (improve fatigue)
   - Heat treatment: optional mill anneal or STA (tailor properties)

5. MECHANICAL TESTING AND QUALIFICATION (ASTM F3049/F3301):
   - Tensile testing: room temp and elevated temp (per AMS 4999 allowables)
     * Post-HIP: 120-135 ksi yield, 10-15% elongation (comparable to wrought)
   - Fatigue testing: smooth and notched, establish S-N curves
     * As-built surface: 50% reduction vs machined (surface roughness)
     * Machined surface + HIP: comparable to wrought fatigue
   - Fracture toughness: K_Ic testing (ASTM E399)
   - CT scan: 100% volumetric inspection for porosity and defects
   - Microstructure: metallography, grain size, alpha case measurement

6. BUILD ORIENTATION EFFECTS (ANISOTROPY):
   - Z-direction (vertical, build direction): columnar grains, lower ductility
   - XY-direction (horizontal): better ductility, higher fatigue
   - Design consideration: orient critical stress direction in XY plane
   - Qualification: test all three principal directions (X, Y, Z)
   - Anisotropy: 10-20% variation in properties typical (HIP reduces anisotropy)

7. CERTIFICATION AND APPLICATIONS:
   - FAA acceptance: AC 33.15-2 (additive manufacturing in engines)
   - Material specification: AMS 4999 (Ti-6Al-4V L-PBF), AMS 7003 (Ti-6Al-4V powder)
   - Design allowables: establish per MMPDS methodology (statistical basis)
   - Applications: brackets, manifolds, ducts, complex geometries (topology optimized)
   - Weight savings: 30-60% via topology optimization and lattice structures
   - Lead time: 1-2 weeks vs 6-12 months for forgings (low volume, complex parts)
   - Cost: economical for low quantity (<100), expensive for high volume

Additive manufacturing (L-PBF) for aerospace titanium parts requires rigorous
qualification to ensure porosity control, mechanical properties, and fatigue
performance. The as-built material has martensitic microstructure with high
strength but low ductility and poor surface finish. Hot Isostatic Pressing (HIP)
is essential to close porosity, improve ductility, and enable fatigue performance
approaching wrought material. Post-HIP mechanical testing per ASTM F3049 and
CT scanning for porosity validation are required for aerospace qualification.
Build orientation creates anisotropy (columnar grains in Z-direction), requiring
testing in all principal directions. The process is economical for complex,
low-volume parts where topology optimization enables significant weight savings
(30-60%). Material specification AMS 4999 and FAA AC 33.15-2 provide the
regulatory framework. The key challenges are porosity control, surface finish,
anisotropy, and establishing statistically-based design allowables. HIP is the
critical enabler, transforming marginal as-built properties into aerospace-grade
performance.
        """,
        key_factors=[
            "L-PBF: layer-by-layer laser melting, 30-60 micron layers, argon atmosphere",
            "As-built: acicular alpha-prime, high strength (140 ksi), low ductility (5-10%)",
            "Porosity target: <0.2% (CT scan validation required)",
            "HIP post-processing: 1650-1750°F, 15-30 ksi, closes porosity to <0.01%",
            "Post-HIP properties: 120-135 ksi yield, 10-15% elongation (comparable to wrought)",
            "Build orientation: Z-direction lower ductility due to columnar grains",
            "Surface finish: as-built poor fatigue, requires machining or shot peening",
            "Applications: complex low-volume parts, 30-60% weight savings via topology optimization"
        ],
        primary_authority=[
            "ASTM F3049 (Standard Guide for Characterizing Properties of Metal Powders Used for Additive Manufacturing)",
            "ASTM F3301 (Standard for Additive Manufacturing - Post Processing Methods)",
            "AMS 4999 (Titanium Alloy, Additive Manufacturing Powder Bed)",
            "AMS 7003 (Titanium Alloy Powder 6Al-4V, Additive Manufacturing)",
            "FAA AC 33.15-2 (Additive Manufacturing of Engines and Propellers)"
        ],
        burden_holder="Additive Manufacturing Engineer",
        adversary_position="Conventional machining from wrought or forged stock is proven and reliable.",
        counter_arguments=[
            "Additive enables complex geometries impossible with conventional machining",
            "Topology optimization achieves 30-60% weight savings vs conventional design",
            "Lead time 1-2 weeks vs 6-12 months for forgings (low-volume production)",
            "HIP post-processing delivers properties comparable to wrought material",
            "CT scanning provides 100% volumetric inspection (better QA than conventional)"
        ],
        resolution_strategy="Use additive for complex, low-volume parts where weight savings justify qualification cost. Use conventional machining for high-volume, simple geometries. HIP is mandatory for aerospace.",
        entity_scope="All aerospace additive manufacturing of titanium alloys",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - emerging standards with growing qualification data",
        controlling_precedent="ASTM F3049/F3301 and AMS 4999",
        category=IssueCategory.ADDITIVE_MANUFACTURING,
        authority_level=AuthorityLevel.PRIMARY
    ),

    # Additional shorter doctrines to reach 30+

    DoctrineBlock(
        topic="Fiber Volume Fraction and Void Content",
        keywords=["fiber volume", "void content", "composite quality", "fiber fraction", "voids"],
        conclusion_template="Optimal fiber volume fraction for aerospace composites is 55-65%. Void content must be <2% (preferably <1%) to meet structural performance requirements.",
        reasoning_framework="""
Fiber volume fraction (Vf) and void content are critical quality parameters:

FIBER VOLUME FRACTION:
- Rule of mixtures: composite modulus proportional to Vf
- Optimal range: 55-65% for aerospace (balance of strength, processability)
- Too low (<50%): resin-rich, lower strength, higher weight
- Too high (>70%): dry spots, voids, difficult impregnation
- Measurement: resin burnoff (ASTM D2584), acid digestion (ASTM D3171)

VOID CONTENT:
- Voids: entrapped air or volatiles during cure
- Acceptance: <2% for aerospace, <1% for critical structure
- Effects: 10% void = 30-40% reduction in interlaminar shear strength
- Detection: ultrasonic C-scan, microscopy of polished cross-section
- Causes: improper debulking, insufficient vacuum, volatiles, moisture

PROCESS CONTROL:
- Prepreg: 33-42% resin content by weight (controls Vf)
- Autoclave: pressure compacts plies, drives out air/volatiles
- Vacuum bagging: minimum 1 full vacuum (14.7 psi), autoclave adds 85 psi
- Bleeder plies: absorb excess resin to control Vf
        """,
        key_factors=[
            "Optimal Vf: 55-65% for aerospace composites",
            "Void content: <2% acceptable, <1% preferred",
            "10% voids reduce ILSS by 30-40%",
            "Measurement: resin burnoff, acid digestion, microscopy"
        ],
        primary_authority=[
            "ASTM D2584 (Ignition Loss of Cured Reinforced Resins)",
            "ASTM D3171 (Fiber Content by Matrix Digestion)",
            "ASTM D2734 (Void Content of Reinforced Plastics)"
        ],
        burden_holder="Process Engineer",
        adversary_position="Visual inspection sufficient for quality control.",
        counter_arguments=[
            "Voids are internal defects not visible on surface",
            "Quantitative measurement required for certification",
            "Interlaminar shear strength highly sensitive to void content"
        ],
        resolution_strategy="Measure Vf and void content per ASTM methods. Optimize autoclave cycle and bleeder system to achieve target Vf with <1% voids.",
        entity_scope="All aerospace composite manufacturing",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - fundamental quality metrics",
        controlling_precedent="ASTM D2584/D3171/D2734",
        category=IssueCategory.MATERIAL_QUALIFICATION,
        authority_level=AuthorityLevel.PRIMARY
    ),

    DoctrineBlock(
        topic="Resin Transfer Molding (RTM) Process",
        keywords=["rtm", "resin transfer", "liquid molding", "dry fiber", "infusion"],
        conclusion_template="RTM injects resin into dry fiber preform in closed mold, enabling complex shapes and automated production. Requires careful permeability analysis and injection strategy to avoid voids.",
        reasoning_framework="""
Resin Transfer Molding process analysis:

PROCESS STEPS:
1. Dry fiber preform: fabric or NCF laid up in mold
2. Mold closure: matched tooling, seals around perimeter
3. Resin injection: pump resin into mold under pressure (30-100 psi)
4. Cure: heated mold accelerates cure (250-350°F)
5. Demold: open mold, remove part

ADVANTAGES:
- Complex shapes: double-curved geometry
- Both-side surface finish: Class A surfaces
- Automation: preform can be automated (reduce labor)
- Void control: pressure compaction, resin front control

CHALLENGES:
- Permeability: resin flow resistance through fiber bed
- Race-tracking: resin flows along edges faster than through thickness
- Dry spots: air entrapment if flow fronts merge improperly
- Injection strategy: gate and vent locations critical
- Tooling cost: matched metal tooling expensive ($100K-$1M)

MATERIALS:
- Resins: low-viscosity epoxy, vinyl ester (viscosity <500 cP)
- Fabrics: dry woven, non-crimp fabric (NCF), unidirectional
- Fiber volume: 50-60% achievable with good compaction
        """,
        key_factors=[
            "RTM: inject resin into dry fiber preform in closed mold",
            "Advantages: complex shapes, automation, both-side finish",
            "Challenges: permeability, race-tracking, dry spots",
            "Injection strategy: gate/vent placement critical to avoid voids"
        ],
        primary_authority=[
            "ASTM D3518 (In-Plane Shear Response of Composites)",
            "Advani & Sozer, Process Modeling in Composites Manufacturing",
            "Handbook of Composites (Peters, ed.)"
        ],
        burden_holder="Manufacturing Engineer",
        adversary_position="Prepreg autoclave provides better quality control.",
        counter_arguments=[
            "RTM enables automation and reduced labor vs hand layup",
            "Complex shapes difficult or impossible with prepreg",
            "Both-side surface finish superior to bag-side prepreg",
            "Lower material cost (dry fabric vs prepreg)"
        ],
        resolution_strategy="Use RTM for complex shapes, high-rate production, or Class A surface requirements. Use prepreg autoclave for highest performance structure. Hybrid approaches possible.",
        entity_scope="Composite manufacturing process selection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Moderate confidence - process-dependent quality",
        controlling_precedent="Industry practice and material specifications",
        category=IssueCategory.MATERIAL_QUALIFICATION,
        authority_level=AuthorityLevel.SECONDARY
    ),

    DoctrineBlock(
        topic="Honeycomb Core Selection and Properties",
        keywords=["honeycomb", "core", "sandwich", "shear", "nomex", "aluminum honeycomb"],
        conclusion_template="Honeycomb core provides high bending stiffness at low weight. Aluminum (5052, 5056) for high strength, Nomex (aramid) for lower density and moisture resistance.",
        reasoning_framework="""
Honeycomb sandwich structure analysis:

SANDWICH CONSTRUCTION:
- Face sheets: carry bending loads (tension/compression)
- Core: resist shear, stabilize faces, space faces apart
- Bending stiffness: I = b*h²/12 (proportional to spacing squared)
- Weight: dominated by face sheets, core is <10%

ALUMINUM HONEYCOMB:
- Alloys: 5052, 5056 (non-heat-treatable, corrosion-resistant)
- Cell size: 1/8 inch, 3/16 inch, 1/4 inch, 3/8 inch
- Density: 3-10 pcf (pounds per cubic foot)
- Shear strength: 200-600 psi (density-dependent)
- Shear modulus: 40-120 ksi
- Applications: control surfaces, flooring, high-strength panels

NOMEX HONEYCOMB (ARAMID FIBER + PHENOLIC RESIN):
- Density: 2-8 pcf
- Shear strength: 100-300 psi
- Shear modulus: 10-50 ksi
- Advantages: lighter than aluminum, moisture-resistant, electrically non-conductive
- Disadvantages: lower strength and modulus than aluminum, higher cost
- Applications: fuselage panels, interior panels, radomes

DESIGN CONSIDERATIONS:
- Core crushing: compression facesheet can crush core (need strong enough core)
- Shear crimping: shear loads can buckle cell walls
- Flatwise tension: core peel strength (adhesive bond critical)
- Moisture ingress: sealed edges required, drill holes require potting
        """,
        key_factors=[
            "Sandwich: high bending stiffness via face spacing (I proportional to h²)",
            "Aluminum honeycomb: 5052/5056, 3-10 pcf, 200-600 psi shear strength",
            "Nomex honeycomb: aramid, 2-8 pcf, lighter but lower strength than aluminum",
            "Design limits: core crushing, shear crimping, flatwise tension"
        ],
        primary_authority=[
            "ASTM C365 (Flatwise Compressive Properties of Sandwich Cores)",
            "ASTM C273 (Shear Properties of Sandwich Core Materials)",
            "HexWeb Honeycomb Sandwich Design Guide (Hexcel)"
        ],
        burden_holder="Structures Engineer",
        adversary_position="Solid laminate simpler to design and manufacture.",
        counter_arguments=[
            "Sandwich provides 5-10x bending stiffness per unit weight vs solid laminate",
            "Core adds minimal weight while greatly increasing stiffness",
            "Critical for control surfaces and large panels where weight is paramount"
        ],
        resolution_strategy="Use sandwich for high stiffness-to-weight applications. Use solid laminate where through-thickness loads or impact damage are concerns.",
        entity_scope="Sandwich composite structure",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - mature technology",
        controlling_precedent="ASTM C365/C273 and manufacturer data",
        category=IssueCategory.COMPOSITE_DESIGN,
        authority_level=AuthorityLevel.PRIMARY
    ),

]


# ============================================================================
# TELEMETRY AND METRICS
# ============================================================================

class MetricsCollector:
    def __init__(self):
        self.query_count = 0
        self.total_query_time_ms = 0.0
        self.cache_hits = 0
        self.vector_searches = 0
        self.doctrine_triggers: Counter = Counter()
        self.start_time = datetime.now()

    def record_query(self, query_time_ms: float, cache_hit: bool,
                    vector_search: bool, doctrines: List[str]):
        self.query_count += 1
        self.total_query_time_ms += query_time_ms
        if cache_hit:
            self.cache_hits += 1
        if vector_search:
            self.vector_searches += 1
        for doctrine in doctrines:
            self.doctrine_triggers[doctrine] += 1

    def get_stats(self) -> Dict[str, Any]:
        uptime = (datetime.now() - self.start_time).total_seconds()
        avg_time = self.total_query_time_ms / self.query_count if self.query_count > 0 else 0
        hit_rate = self.cache_hits / self.query_count if self.query_count > 0 else 0

        return {
            "total_queries": self.query_count,
            "avg_response_ms": round(avg_time, 2),
            "cache_hit_rate": round(hit_rate, 3),
            "uptime_seconds": round(uptime, 1),
            "vector_searches": self.vector_searches,
            "top_doctrines": self.doctrine_triggers.most_common(10)
        }


# ============================================================================
# CORE ENGINE
# ============================================================================

class AERO09Engine:
    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.metrics = MetricsCollector()
        self.audit_log_path = Path(__file__).parent / "audit_trail.jsonl"
        logger.info(f"AERO09 Aircraft Materials Engine initialized with {len(self.doctrines)} doctrines")

    def semantic_normalize(self, query: str) -> str:
        """Normalize aerospace materials terminology"""
        normalizations = {
            "carbon fiber": ["cfrp", "carbon composite", "carbon-fiber", "graphite epoxy"],
            "aluminum": ["al", "aluminium"],
            "titanium": ["ti", "ti6al4v", "ti-64"],
            "composite": ["frp", "fiber reinforced", "laminate"],
            "crack growth": ["fatigue crack", "da/dn", "crack propagation"],
            "stress intensity": ["k factor", "k-ic", "fracture toughness"],
        }

        query_lower = query.lower()
        for canonical, variants in normalizations.items():
            for variant in variants:
                if variant in query_lower:
                    query_lower = query_lower.replace(variant, canonical)

        return query_lower

    def doctrine_cache_lookup(self, query: str) -> List[DoctrineBlock]:
        """Three-layer response: Doctrine Cache (0-200ms)"""
        normalized = self.semantic_normalize(query)
        matches = []

        for doctrine in self.doctrines:
            matched, score = doctrine.matches(normalized)
            if matched:
                matches.append((doctrine, score))

        matches.sort(key=lambda x: x[1], reverse=True)
        return [m[0] for m in matches[:5]]

    def confidence_stratification(self, doctrines: List[DoctrineBlock],
                                 context: Optional[Dict]) -> ConfidenceLevel:
        """Determine confidence level based on doctrine strength and context"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        primary_count = sum(1 for d in doctrines if d.authority_level == AuthorityLevel.PRIMARY)

        if primary_count >= 2:
            return ConfidenceLevel.DEFENSIBLE
        elif primary_count == 1:
            return ConfidenceLevel.AGGRESSIVE
        else:
            return ConfidenceLevel.DISCLOSURE

    def apply_response_mode(self, doctrines: List[DoctrineBlock],
                          mode: ResponseMode, zone: AnalysisZone) -> str:
        """Format response based on mode and zone"""
        if not doctrines:
            return "No specific aerospace materials doctrine matched. Recommend consulting CMH-17 or MMPDS for material allowables and industry standards."

        primary = doctrines[0]

        if mode == ResponseMode.FAST:
            return f"{primary.conclusion_template}\n\nKey factors: {', '.join(primary.key_factors[:3])}"

        elif mode == ResponseMode.DEFENSE:
            response = f"POSITION:\n{primary.conclusion_template}\n\n"
            response += f"AUTHORITY:\n{', '.join(primary.primary_authority)}\n\n"
            response += f"SUPPORTING REASONING:\n{primary.reasoning_framework[:800]}...\n\n"
            response += f"ADVERSARY POSITION: {primary.adversary_position}\n\n"
            response += f"COUNTER-ARGUMENTS:\n" + "\n".join(f"- {arg}" for arg in primary.counter_arguments[:3])
            return response

        else:  # MEMO
            response = f"MEMORANDUM - AEROSPACE MATERIALS ANALYSIS\n\n"
            response += f"ISSUE:\n{primary.topic}\n\n"
            response += f"CONCLUSION:\n{primary.conclusion_template}\n\n"
            response += f"ANALYSIS:\n{primary.reasoning_framework}\n\n"
            response += f"KEY FACTORS:\n" + "\n".join(f"• {kf}" for kf in primary.key_factors) + "\n\n"
            response += f"AUTHORITY:\n" + "\n".join(f"• {auth}" for auth in primary.primary_authority) + "\n\n"
            response += f"CONFIDENCE: {primary.confidence.value}\n"
            response += f"STRATIFICATION: {primary.confidence_stratification}"
            return response

    def determinism_hash(self, query: str, doctrines: List[str]) -> str:
        """Generate SHA-256 hash for reproducibility verification"""
        content = f"{query}|{'|'.join(sorted(doctrines))}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def audit_trail(self, query: str, response: str, doctrines: List[str],
                   confidence: ConfidenceLevel, telemetry: Dict):
        """Append audit entry to JSONL log"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response_preview": response[:200],
            "doctrines_used": doctrines,
            "confidence": confidence.value,
            "telemetry": telemetry,
        }

        with open(self.audit_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def query(self, request: QueryRequest) -> QueryResponse:
        """Main query processing pipeline"""
        start_time = datetime.now()

        # Doctrine cache lookup
        matched_doctrines = self.doctrine_cache_lookup(request.question)
        cache_hit = len(matched_doctrines) > 0

        # Generate response
        response_text = self.apply_response_mode(matched_doctrines, request.mode, request.zone)

        # Confidence stratification
        confidence = self.confidence_stratification(matched_doctrines, request.context)

        # Telemetry
        query_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        doctrine_topics = [d.topic for d in matched_doctrines]

        telemetry = TelemetryData(
            query_time_ms=round(query_time_ms, 2),
            cache_hits=1 if cache_hit else 0,
            vector_searches=0,
            doctrines_triggered=doctrine_topics,
            confidence_level=confidence
        )

        # Metrics
        self.metrics.record_query(query_time_ms, cache_hit, False, doctrine_topics)

        # Determinism hash
        det_hash = self.determinism_hash(request.question, doctrine_topics)

        # Audit trail
        self.audit_trail(request.question, response_text, doctrine_topics, confidence, asdict(telemetry))

        # Build doctrine matches
        doctrine_matches = [
            DoctrineMatch(
                topic=d.topic,
                confidence=0.95,
                category=d.category,
                keywords_matched=d.keywords[:3],
                authority_level=d.authority_level
            )
            for d in matched_doctrines
        ]

        return QueryResponse(
            answer=response_text,
            confidence=confidence,
            doctrines_used=doctrine_matches,
            telemetry=telemetry,
            determinism_hash=det_hash,
            timestamp=datetime.now().isoformat(),
            audit_trail_id=str(self.audit_log_path)
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="AERO09 Aircraft Materials Intelligence Engine",
    description="TIE-grade aerospace materials analysis system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = AERO09Engine()


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint - aircraft materials analysis"""
    try:
        return engine.query(request)
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    stats = engine.metrics.get_stats()

    return HealthResponse(
        status="operational",
        engine="AERO09_aircraft_materials",
        version="1.0.0",
        port=9204,
        doctrines_loaded=len(engine.doctrines),
        uptime_seconds=stats["uptime_seconds"],
        total_queries=stats["total_queries"],
        avg_response_ms=stats["avg_response_ms"],
        cache_hit_rate=stats["cache_hit_rate"]
    )


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total": len(engine.doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "authority_level": d.authority_level.value,
                "keywords": d.keywords
            }
            for d in engine.doctrines
        ]
    }


@app.get("/metrics")
async def get_metrics():
    """Retrieve engine metrics"""
    return engine.metrics.get_stats()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting AERO09 Aircraft Materials Intelligence Engine on port 9204")
    uvicorn.run(app, host="0.0.0.0", port=9204)
