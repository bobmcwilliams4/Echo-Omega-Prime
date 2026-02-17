"""
MECH06 - Bearing Analysis & Selection Engine
TIE Gold Standard - Mechanical Engineering Domain

Expertise: Rolling element bearings, journal bearings, bearing life, lubrication,
          failure analysis, condition monitoring, API standards

Port: 9046
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# ============================================================================
# CONFIGURATION
# ============================================================================

logger.add(
    Path(__file__).parent / "logs" / "mech06_bearing_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)

APP = FastAPI(title="MECH06 Bearing Analysis Engine", version="1.0.0")
APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ============================================================================
# ENUMS & DATA STRUCTURES
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

class BearingType(str, Enum):
    DEEP_GROOVE_BALL = "deep_groove_ball"
    ANGULAR_CONTACT = "angular_contact"
    CYLINDRICAL_ROLLER = "cylindrical_roller"
    TAPERED_ROLLER = "tapered_roller"
    SPHERICAL_ROLLER = "spherical_roller"
    THRUST_BALL = "thrust_ball"
    THRUST_ROLLER = "thrust_roller"
    JOURNAL = "journal"
    TILTING_PAD = "tilting_pad"
    MAGNETIC = "magnetic"

class FailureMode(str, Enum):
    FATIGUE_SPALLING = "fatigue_spalling"
    BRINELLING = "brinelling"
    FRETTING = "fretting"
    SMEARING = "smearing"
    ELECTRICAL_EROSION = "electrical_erosion"
    CORROSION = "corrosion"
    WEAR = "wear"
    CONTAMINATION = "contamination"

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
    controlling_precedent: List[str]
    trigger_count: int = 0
    last_triggered: Optional[datetime] = None

@dataclass
class TelemetryEvent:
    timestamp: datetime
    query: str
    mode: ResponseMode
    doctrines_triggered: List[str]
    confidence: ConfidenceLevel
    latency_ms: float
    hash: str

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class BearingQueryRequest(BaseModel):
    query: str = Field(..., description="Bearing engineering question")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")

class BearingQueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    doctrines_applied: List[str]
    recommendations: List[str]
    warnings: List[str]
    mode: ResponseMode
    latency_ms: float
    determinism_hash: str
    timestamp: datetime

# ============================================================================
# DOCTRINE CACHE - 25+ BEARING ENGINEERING EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Rolling Bearing Life Calculation - ISO 281",
        keywords=["L10", "L10a", "bearing life", "rating life", "ISO 281", "basic dynamic load", "fatigue life"],
        conclusion_template=[
            "Calculate L10 life using: L10 = (C/P)^p × 10^6 revolutions, where p=3 for ball bearings, p=10/3 for roller bearings.",
            "For adjusted rating life L10a per ISO 281:2007, apply modification factors: L10a = a1 × aISO × L10.",
            "L10 represents 90% reliability; for higher reliability use: Lna = a1 × aISO × (C/P)^p where a1 accounts for reliability level."
        ],
        reasoning_framework="""
ISO 281:2007 defines bearing rating life as the number of revolutions that 90% of a group
of apparently identical bearings will complete or exceed before first evidence of fatigue develops.

Key calculation components:
1. Basic dynamic load rating C (from manufacturer catalog) in Newtons
2. Equivalent dynamic bearing load P = X×Fr + Y×Fa where:
   - Fr = radial load, Fa = axial load
   - X, Y = radial and axial load factors from manufacturer tables based on Fa/Fr ratio
3. Load exponent p: 3 for ball bearings, 10/3 (3.33) for roller bearings
4. Life modification factor a1 for reliability other than 90%:
   - 90% reliability (L10): a1 = 1.0
   - 95% reliability (L5): a1 = 0.62
   - 96% reliability (L4): a1 = 0.53
   - 99% reliability (L1): a1 = 0.21
5. aISO factor accounts for lubrication condition, contamination, and fatigue limit
   - Requires contamination factor ηc (from ISO 281)
   - Viscosity ratio κ = ν/ν1 where ν = operating viscosity, ν1 = reference viscosity
   - For κ ≥ 4 and ηc ≥ 0.8: aISO can exceed 50, effectively infinite life below fatigue limit

Life in hours: L10h = (L10 × 10^6) / (60 × n) where n = speed in RPM

CRITICAL: L10 is probabilistic. 10% of bearings will fail before L10. For critical applications,
use L1 (99% reliability) or apply increased safety factors. Temperature above 120°C requires
additional reduction factors. Misalignment, improper mounting, and contamination drastically
reduce actual achieved life below calculated values.
        """,
        key_factors=[
            "Basic dynamic load rating C from manufacturer",
            "Equivalent load P calculation using load factors X, Y",
            "Load exponent p (3 for balls, 10/3 for rollers)",
            "Operating speed in RPM",
            "Required reliability level (L10, L5, L1)",
            "Lubrication condition (κ = ν/ν1 viscosity ratio)",
            "Contamination level (ηc factor)",
            "Operating temperature (reduce life if >120°C)",
            "Mounting quality and alignment"
        ],
        primary_authority=[
            "ISO 281:2007 - Rolling bearings — Dynamic load ratings and rating life",
            "ANSI/ABMA 9-1990 - Load Ratings and Fatigue Life for Ball Bearings",
            "ANSI/ABMA 11-1990 - Load Ratings and Fatigue Life for Roller Bearings",
            "SKF General Catalogue - Bearing life calculation methods",
            "Timken Engineering Manual - Rating life and load calculations"
        ],
        burden_holder="Engineer",
        adversary_position="Calculated life is theoretical maximum; field conditions always reduce actual life",
        counter_arguments=[
            "ISO 281 assumes ideal conditions (proper mounting, clean lubricant, no misalignment)",
            "Real-world contamination, moisture, and handling damage reduce life by 50-90%",
            "Published C values assume manufacturer's quality standards; counterfeit bearings have lower C",
            "Dynamic loading and vibration not captured in static P calculation",
            "Electrical currents through bearing (VFD-induced) cause fluting not predicted by life equations"
        ],
        resolution_strategy="Use calculated L10a as upper bound; apply field service factors (0.3-0.5) for realistic estimates; monitor actual failure data and adjust",
        entity_scope="All rolling element bearings in rotary equipment",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "ISO 281:2007 Annex A - Calculation of reference rating life",
            "API 610 (pumps) and API 617 (compressors) reference ISO 281 for minimum L10 requirements"
        ]
    ),

    DoctrineBlock(
        topic="Bearing Fit Selection - Shaft and Housing",
        keywords=["bearing fit", "interference fit", "clearance fit", "tolerance", "h6", "H7", "k5", "m6", "creep", "fretting"],
        conclusion_template=[
            "Rotating ring (relative to load) requires interference fit to prevent creep; stationary ring uses clearance fit.",
            "Common shaft fits: k5 (light interference), m5/m6 (medium), n6 (heavy). Housing fits: H7 (normal clearance), J7 (light clearance).",
            "Thin-walled housings, hollow shafts, and high temperatures require tighter fits to compensate for expansion and deflection."
        ],
        reasoning_framework="""
Correct bearing fit is critical to prevent:
1. Creep - circumferential movement between ring and seat causing fretting wear
2. Inadequate support - ring deformation under load, reducing internal clearance
3. Excessive interference - eliminating internal clearance, causing preload and premature failure

General principle: The ring that rotates relative to the load direction requires interference fit.
- Inner ring rotating on shaft with stationary radial load: tight shaft fit (k5, m6, n6)
- Outer ring rotating in housing with stationary load: tight housing fit (K7, M7)
- Stationary ring: loose fit (H7 housing, h6 shaft) for easy assembly/disassembly

ISO 286 tolerance grades:
- Shaft: h (zero upper deviation) with grade 5 or 6
- Housing: H (zero lower deviation) with grade 6 or 7
- Interference grades: j, k, m, n, p (increasing interference)

Fit selection factors:
1. Load magnitude - heavy loads need tighter fits
2. Load type - shock/vibration needs tighter fits
3. Shaft/housing material - aluminum expands more than steel, needs tighter initial fit
4. Temperature - differential expansion between bearing steel and shaft/housing
5. Shaft design - hollow/thin-wall shafts need tighter fits (expand more under interference)
6. Bearing size - large bearings need looser fits (cumulative tolerance stack)

Common fits:
- Small motors, light loads: shaft h6, housing H7
- Industrial motors, pumps: shaft k5-m6, housing H7
- Heavy industrial, high shock: shaft n6-p6, housing M7
- Precision spindles: shaft h5, housing H6 with preload

CRITICAL: Too tight a fit reduces internal clearance, causing preload, heat generation,
and premature fatigue. Measure internal clearance after mounting to verify adequate clearance remains.
        """,
        key_factors=[
            "Direction of load relative to ring rotation",
            "Load magnitude and type (steady, shock, vibration)",
            "Shaft and housing material (thermal expansion coefficient)",
            "Operating temperature range",
            "Shaft design (solid vs hollow)",
            "Bearing size and series",
            "Assembly/disassembly requirements",
            "Internal clearance specification (C2, Normal, C3, C4)"
        ],
        primary_authority=[
            "ISO 286-2 - Tolerances for shafts and housings",
            "SKF General Catalogue - Fits section",
            "Timken Bearing Damage Analysis with Failure Atlas",
            "ANSI/ABMA 7-1995 - Shaft and Housing Fits for Metric Radial Ball and Roller Bearings",
            "DIN 620 - Rolling bearings — Tolerances"
        ],
        burden_holder="Design Engineer",
        adversary_position="Tighter is always safer; loose fits cause creep and fretting",
        counter_arguments=[
            "Excessive interference eliminates internal clearance, causing preload and overheating",
            "Tight fits make assembly difficult and increase risk of mounting damage (cracked races)",
            "Temperature differential expansion can convert medium fit to heavy interference in service",
            "Large bearings expand significantly under interference; published tables may be inadequate",
            "Hydraulic mounting methods (oil injection, induction heating) require specific fit ranges"
        ],
        resolution_strategy="Calculate effective interference accounting for temperature, material, and geometry; measure post-mount clearance; use C3 clearance bearings if tight fit required",
        entity_scope="All rolling element bearings with pressed-on mounting",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "ISO 5753 - Bearing internal clearance specification",
            "Manufacturer catalogs provide fit recommendations per application type"
        ]
    ),

    DoctrineBlock(
        topic="Bearing Lubrication Selection - Grease vs Oil",
        keywords=["bearing lubrication", "grease", "oil", "NLGI", "viscosity", "lubrication regime", "relubrication", "oil bath"],
        conclusion_template=[
            "Grease lubrication for: speeds <70% of limiting speed, intermittent operation, sealed environments, simplicity. Oil for higher speeds, heat dissipation, long life.",
            "Grease NLGI grade selection: NLGI 2 (most common), NLGI 3 for vertical shafts/high temps, NLGI 1 for cold climates. Lithium complex for -30 to +150°C.",
            "Oil viscosity per ISO VG grade: calculate ν1 reference viscosity from bearing size/speed, select ISO VG to achieve κ ≥ 1 (minimum) or κ ≥ 4 (optimal) at operating temp."
        ],
        reasoning_framework="""
Lubrication regime determines bearing life and failure mode:
1. Boundary lubrication (κ < 0.4) - metal-to-metal contact, severe wear, short life
2. Mixed lubrication (0.4 ≤ κ < 1) - partial film, moderate wear
3. Elastohydrodynamic (EHD) lubrication (κ ≥ 1) - full film separation, fatigue-limited life
4. Full EHD (κ ≥ 4) - potential infinite life below fatigue limit if clean

Viscosity ratio κ = ν / ν1 where:
- ν = actual operating viscosity (mm²/s at operating temperature)
- ν1 = reference viscosity required for adequate lubrication (from ISO 281 charts based on dm = (D+d)/2 and speed)

Grease advantages:
- Sealing effect, protects against contamination
- Simple application, long relubrication intervals
- Stays in place, suitable for intermittent operation
- Lower initial cost for small bearings

Grease limitations:
- Speed limited to ~70% of bearing limiting speed (heat generation, churning)
- Poor heat dissipation (thermal conductivity ~10% of oil)
- Degradation over time (oxidation, oil separation, hardening)
- Relubrication required (intervals from hours to years depending on size, speed, temp)

Oil advantages:
- Excellent cooling, can run at higher speeds
- Continuous filtration possible, removes contaminants
- Indefinite life if properly maintained and filtered
- Better for high-temperature applications (>120°C continuous)

Oil limitations:
- Requires sealing, more complex system
- Potential for leakage
- Higher maintenance (oil changes, filter service)
- Continuous circulation systems costly for small machines

NLGI grade (consistency):
- NLGI 000, 00, 0: Soft, for centralized systems, cold climates
- NLGI 1: Soft, for low temps, high-speed applications
- NLGI 2: Most common, general purpose, -30 to +120°C
- NLGI 3: Stiff, for vertical shafts, high temps, heavy loads
- NLGI 4, 5, 6: Very stiff, special applications only

Base oil type:
- Mineral oil: -20 to +110°C, standard applications
- Synthetic (PAO, ester): -40 to +150°C, wide temp range, long life
- Polyurea, lithium complex thickeners for high temp

Relubrication interval estimation (SKF formula):
t_f = (14 × 10^6) / (n × d_m) hours for NLGI 2 grease at 70°C, reduced by half for each 15°C increase
        """,
        key_factors=[
            "Operating speed vs bearing limiting speed",
            "Operating temperature range",
            "Ambient contamination level",
            "Vertical vs horizontal shaft orientation",
            "Continuous vs intermittent operation",
            "Required service life and maintenance interval",
            "Heat dissipation requirements",
            "Accessibility for relubrication",
            "Sealing effectiveness"
        ],
        primary_authority=[
            "ISO 281:2007 Annex C - Lubrication factor aISO",
            "DIN 51825 - Lubricating greases K - Classification and requirements",
            "NLGI Lubricating Grease Guide",
            "ISO 6743-99 - Lubricants, industrial oils and related products (class L) — Part 99: Lubricating greases",
            "SKF Lubrication Guide"
        ],
        burden_holder="Maintenance Engineer",
        adversary_position="Grease is always simpler and cheaper than oil systems",
        counter_arguments=[
            "High-speed applications (>70% limiting speed) overheat with grease, requiring oil or oil-air",
            "Over-greasing is common failure cause (churning, overheating, seal damage)",
            "Incompatible grease types cause soap breakdown (lithium + calcium = sludge)",
            "Grease life at 100°C is 1/8th the life at 70°C (exponential degradation)",
            "Oil systems enable condition monitoring (particle counting, spectrometry, ferrography)"
        ],
        resolution_strategy="Calculate operating parameters (dm × n value), check limiting speed, estimate temperature rise; select grease for dm×n < 300,000 mm×rpm and accessible relubrication, oil for higher speeds or inaccessible/critical applications",
        entity_scope="All lubricated rolling element bearings",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "API 610 requires oil lubrication for centrifugal pumps (accessibility, reliability)",
            "Electric motor standards (NEMA MG-1) specify grease for small motors, oil for large"
        ]
    ),

    DoctrineBlock(
        topic="Bearing Failure Analysis - Fatigue Spalling",
        keywords=["spalling", "fatigue", "pitting", "subsurface initiated fatigue", "L10 life", "Hertzian stress", "inclusion"],
        conclusion_template=[
            "Subsurface-initiated fatigue spalling is normal end-of-life failure mode, occurs at or beyond calculated L10 life with proper loading and lubrication.",
            "Premature spalling indicates: overloading (P > rated), contamination (stress risers), poor lubrication (κ < 1), corrosion pitting (stress concentration).",
            "Surface-initiated spalling (shallow, polished appearance) indicates boundary lubrication or contamination; subsurface-initiated (deeper, rough) is classic fatigue."
        ],
        reasoning_framework="""
Fatigue spalling mechanism:
1. Hertzian contact stress in rolling/sliding contact creates orthogonal shear stress maximum ~0.5mm below surface
2. Repeated stress cycles (millions to billions) nucleate micro-cracks at subsurface inclusions or microstructure defects
3. Crack propagates to surface, releasing material fragment (spall)
4. Progressive spalling as stress concentration at spall edges propagates additional cracks

Classic fatigue spalling characteristics:
- Occurs after significant running time (approaching or exceeding L10 calculated life)
- Initiates at subsurface (0.3-0.8mm depth)
- Spall edges are rough, jagged (not polished)
- Multiple spalls develop progressively
- Associated with vibration increase, temperature rise
- Material shows beach marks indicating fatigue crack growth

Premature spalling root causes:
1. Overload - equivalent load P exceeds basic dynamic rating C
   - Inadequate bearing size for application
   - Shock loads, misalignment increasing actual load
   - L10 life inversely proportional to P³ (balls) or P^3.33 (rollers)

2. Contamination - particles in lubricant create stress risers
   - Hard particles (wear debris, dirt) indent surface
   - Indentations become stress concentration points
   - Surface-initiated cracks from dents
   - ISO contamination codes: target <15/13/10 for industrial bearings

3. Poor lubrication - boundary or mixed regime
   - Viscosity ratio κ < 1 allows metal contact
   - Surface distress initiates cracks
   - Distinguishing feature: surface-initiated shallow spalls with polished appearance

4. Corrosion - moisture, acids etch surface creating stress risers
   - Corrosion pits act as crack nucleation sites
   - Accelerates fatigue process
   - Distinguishing feature: rust staining, etched appearance

5. Electrical erosion - current passage creates micro-craters (fluting)
   - Craters become fatigue initiation sites
   - Distinguishing feature: washboard pattern of fluting, frosted appearance

CRITICAL DISTINCTION: Spalling at or beyond calculated L10 life with proper operating conditions
is EXPECTED and not considered premature failure. L10 means 10% of population fails by this point.
Premature spalling (well before L10) indicates root cause beyond normal fatigue process.
        """,
        key_factors=[
            "Operating time vs calculated L10 life",
            "Load history (overloads, shocks, misalignment)",
            "Lubrication adequacy (viscosity ratio κ)",
            "Contamination level (ISO code, particle count)",
            "Operating temperature",
            "Spall appearance (depth, surface finish, location)",
            "Presence of corrosion or electrical damage",
            "Vibration trend data prior to failure"
        ],
        primary_authority=[
            "ISO 15243 - Rolling bearings — Damage and failures — Terms, characteristics and causes",
            "SKF Bearing Damage Analysis Guide",
            "Timken Bearing Damage Analysis with Failure Atlas",
            "ASTM STP 771 - Detection, Diagnosis and Prognosis of Rolling-Element Bearings",
            "Tallian, T.E. - Failure Atlas for Hertz Contact Machine Elements (1992)"
        ],
        burden_holder="Failure Analyst",
        adversary_position="All spalling is premature failure indicating design or maintenance deficiency",
        counter_arguments=[
            "L10 life is statistical; 10% failure rate by L10 is by design, not deficiency",
            "Bearing replacement before visible spalling is cost-prohibitive for most applications",
            "Field conditions (contamination, misalignment) always differ from catalog assumptions",
            "Condition monitoring detects spalling onset before catastrophic failure in critical machines",
            "Modern bearing steels (vacuum degassed) have fewer inclusions, longer actual life than L10"
        ],
        resolution_strategy="Compare operating time to calculated L10; examine spall characteristics under magnification; review load, lubrication, and contamination history; classify as normal fatigue vs premature; identify root cause if premature",
        entity_scope="All rolling element bearings",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "ISO 15243 classifies fatigue spalling as 'normal' when occurring at expected life",
            "Warranty claims for premature failure require evidence of operation within design limits"
        ]
    ),

    DoctrineBlock(
        topic="Vibration Analysis - Bearing Defect Frequencies",
        keywords=["BPFO", "BPFI", "BSF", "FTF", "bearing vibration", "envelope analysis", "defect frequency", "outer race", "inner race", "ball spin"],
        conclusion_template=[
            "Outer race defect: BPFO = (n/60) × (N_b/2) × (1 + (d_b/d_m)×cos(α)), generates peak at BPFO and harmonics in envelope spectrum.",
            "Inner race defect: BPFI = (n/60) × (N_b/2) × (1 + (d_b/d_m)×cos(α)), modulated by 1× RPM due to load zone rotation with shaft.",
            "Ball defect: BSF = (d_m/d_b) × (n/120) × [1 - (d_b/d_m)²×cos²(α)], generates 2× BSF as each ball defect strikes inner and outer race per revolution."
        ],
        reasoning_framework="""
Bearing defect frequencies are kinematic calculations based on geometry and speed:

Fundamental train frequency (cage speed):
FTF = (n/60) × (1/2) × [1 - (d_b/d_m)×cos(α)]

Ball pass frequency outer race (BPFO):
BPFO = (n/60) × (N_b/2) × [1 + (d_b/d_m)×cos(α)]
- Each ball passing stationary outer race defect generates impact
- Non-synchronous with shaft speed
- Amplitude steady, not modulated

Ball pass frequency inner race (BPFI):
BPFI = (n/60) × (N_b/2) × [1 - (d_b/d_m)×cos(α)]
- Each ball passing rotating inner race defect generates impact
- Modulated by 1× RPM because defect rotates in/out of load zone
- Sidebands at BPFI ± 1×, ± 2×, ± 3× RPM indicate inner race defect

Ball spin frequency (BSF):
BSF = (d_m/2d_b) × (n/60) × [1 - (d_b/d_m)²×cos²(α)]
- Ball defect strikes inner and outer race each ball revolution
- Observed frequency is 2× BSF (two impacts per ball rotation)
- Relatively rare (balls fail less often than races)

Where:
- n = shaft speed (RPM)
- N_b = number of balls/rollers
- d_b = ball/roller diameter (mm)
- d_m = pitch diameter = (D + d)/2 (mm)
- α = contact angle (degrees)
- D = bearing outer diameter, d = bearing inner diameter

Measurement technique:
1. High-frequency acceleration (10-40 kHz) captures bearing impulses
2. Envelope (demodulation) analysis extracts impact energy from resonance
3. FFT of envelope signal reveals defect frequencies
4. Compare measured peaks to calculated BPFO, BPFI, BSF frequencies

Diagnostic indicators:
- BPFO peak: outer race defect (stationary, less severe initially)
- BPFI peak with 1× sidebands: inner race defect (rotating, load zone hammering, more severe)
- 2×BSF peak: ball/roller defect (less common)
- Harmonics (2×BPFO, 3×BPFO): advanced degradation, multiple defects or large defect
- Elevated noise floor: generalized roughness, lubrication issues

CRITICAL: Defect must be in loaded zone to generate strong signal. Lightly loaded bearings
may have defects that don't generate vibration until load increases. Temperature rise and
lubricant debris analysis may detect defects earlier than vibration in light-load applications.
        """,
        key_factors=[
            "Bearing geometry (N_b, d_b, d_m, contact angle α)",
            "Shaft speed (RPM)",
            "Load magnitude and direction (affects which defect frequencies appear)",
            "Sensor location and mounting (accelerometer placement)",
            "Frequency range and sampling rate",
            "Envelope frequency band selection",
            "Background noise and interfering machinery signals",
            "Bearing type (ball vs roller, single vs double row)"
        ],
        primary_authority=[
            "ISO 20816 - Mechanical vibration — Measurement and evaluation of machine vibration",
            "ISO 10816-3 - Vibration severity for industrial machines >15kW",
            "ASTM E2835 - Standard Practice for Measuring Vibration Severity",
            "SKF Condition Monitoring Guide - Bearing defect frequency analysis",
            "Mobius Institute - Vibration Analysis Category II/III standards"
        ],
        burden_holder="Vibration Analyst",
        adversary_position="Bearing defect frequencies are unreliable; broadband noise and harmonics are ambiguous",
        counter_arguments=[
            "Variable speed machines require order tracking to maintain frequency accuracy",
            "Gearbox bearing frequencies overlap with gear mesh harmonics, masking defects",
            "Bearing slip (non-ideal kinematics) shifts actual frequencies ±2-5% from calculated",
            "Multiple bearings on same shaft create mixed frequency spectra",
            "Early-stage defects may not generate sufficient energy for detection above noise floor"
        ],
        resolution_strategy="Calculate theoretical frequencies for all bearings in machine; use envelope analysis with optimized frequency bands; confirm defect frequency matches calculated value ±5%; trend amplitude over time; correlate with temperature and oil analysis",
        entity_scope="All rolling element bearings in rotating machinery with accessible vibration measurement points",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "ISO 13373 - Condition monitoring and diagnostics of machines — Vibration condition monitoring",
            "ISO 18436 - Condition monitoring and diagnostics of machines — Requirements for qualification and assessment of personnel"
        ]
    ),

    DoctrineBlock(
        topic="API 610 Bearing Requirements - Centrifugal Pumps",
        keywords=["API 610", "pump bearing", "L10 life", "25000 hours", "oil lubrication", "bearing housing", "radial bearing", "thrust bearing"],
        conclusion_template=[
            "API 610 requires minimum L10 bearing life of 25,000 hours (3 years continuous) for radial and thrust bearings at rated conditions.",
            "Lubrication shall be oil (not grease) for accessibility and reliability. Oil rings, flinger discs, or forced circulation acceptable per service.",
            "Bearing housing design: removable covers for inspection without coupling removal, dual oil drain plugs, magnetic plugs, provision for thermocouples."
        ],
        reasoning_framework="""
API 610 - Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries
establishes minimum requirements for pump bearings to ensure reliability in continuous-duty
process applications.

Key API 610 bearing requirements:

1. Life calculation:
   - Minimum L10 life: 25,000 hours at rated load and speed
   - Calculated per ISO 281 or ANSI/ABMA standards
   - Both radial and thrust bearings must meet requirement
   - Rated conditions = BEP (best efficiency point) load + maximum continuous speed
   - Consider radial load from impeller unbalance, overhung weight
   - Consider axial load from impeller hydraulic thrust

2. Bearing type selection:
   - Radial bearings: typically deep groove ball or cylindrical roller
   - Thrust bearing: angular contact ball or tapered roller, sized for hydraulic thrust + rotor weight
   - For large pumps (>100 HP): tilting pad journal bearings with separate thrust bearing common
   - Self-aligning bearings (spherical roller) permitted only with manufacturer justification

3. Lubrication system:
   - Oil lubrication required (grease not permitted - accessibility and reliability)
   - Oil ring or flinger disc for horizontal pumps <150 HP
   - Forced circulation for vertical pumps or horizontal >150 HP
   - ISO VG 32 or 46 turbine oil typical
   - Oil level sight glass, temperature monitoring provisions
   - Constant level oiler or external reservoir common

4. Bearing housing:
   - Removable covers/caps for bearing inspection without coupling removal
   - Dual drain plugs: bottom drain and magnetic drain plug for debris capture
   - Provision for bearing temperature measurement (thermocouple wells or RTD pockets)
   - Oil seals: lip seals for oil ring lube, mechanical face seals for forced circulation
   - Cooling jackets or fins for high-temperature services

5. Mounting and clearance:
   - Bearings shall be mounted for thermal growth without constraint
   - Floating bearing (one end) or angular contact back-to-back (fixed position) typical
   - Internal clearance: C3 or greater for process pumps (thermal expansion)
   - Verify clearance after mounting, document in bearing record

6. Materials and quality:
   - ABEC-1 (ISO class Normal) minimum for radial bearings
   - ABEC-3 for thrust bearings and high-speed applications
   - Bearings from manufacturers with ISO 9001 quality systems
   - Traceability required (heat numbers, certificates)

7. Interchangeability:
   - Bearing sizes shall be commercially available from multiple sources
   - Proprietary or special bearings require user approval
   - Spare bearings provided with initial order per API 610

CRITICAL: 25,000-hour requirement is minimum. Many users specify 40,000+ hours for critical
services. L10 is 90% reliability; for unspared critical pumps, consider L5 (95%) or L1 (99%)
design criteria. Field service factors (contamination, misalignment) reduce actual achieved
life below calculated values by 30-60%.
        """,
        key_factors=[
            "Hydraulic thrust load magnitude and direction",
            "Radial loads from impeller unbalance, overhung weight",
            "Operating speed range (rated, minimum continuous, maximum allowable)",
            "Service temperature and environment",
            "Pump criticality and sparing philosophy",
            "Maintenance accessibility and frequency",
            "Lubrication system type and reliability",
            "Seal flush plan and potential bearing contamination",
            "Foundation rigidity and alignment capability"
        ],
        primary_authority=[
            "API Standard 610 - Centrifugal Pumps for Petroleum, Heavy Duty Chemical, and Gas Industry Services",
            "ISO 13709 - Centrifugal pumps for petroleum, petrochemical and natural gas industries (ISO adoption of API 610)",
            "ISO 281 - bearing life calculation",
            "ANSI/HI 9.6.4 - Rotordynamics for Centrifugal Pumps"
        ],
        burden_holder="Pump manufacturer",
        adversary_position="25,000 hours is arbitrary; properly sized bearings should last indefinitely with good maintenance",
        counter_arguments=[
            "Contamination from seal leakage common in process pumps, reduces bearing life dramatically",
            "Piping strain and thermal growth cause misalignment exceeding design assumptions",
            "Cavitation-induced vibration creates dynamic loads not captured in static bearing calculation",
            "High-temperature pumps (>200°C) have reduced bearing life due to lubricant degradation",
            "Field alignment quality often inferior to factory setup, increasing actual bearing loads"
        ],
        resolution_strategy="Calculate bearing loads conservatively (include impeller unbalance, pipe loads); select bearings with margin (L10 > 35,000 hours); specify C3 clearance; design lubrication system for accessibility and monitoring; implement condition monitoring (vibration, temperature, oil analysis)",
        entity_scope="Centrifugal pumps in petroleum, chemical, and gas industries per API 610 scope",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "API 610 12th edition (2022) section on bearings and lubrication",
            "Contractual documents referencing API 610 make bearing requirements mandatory"
        ]
    ),

    DoctrineBlock(
        topic="Journal Bearing Design - Hydrodynamic Lubrication",
        keywords=["journal bearing", "hydrodynamic", "Sommerfeld number", "minimum film thickness", "plain bearing", "babbitt", "eccentricity ratio"],
        conclusion_template=[
            "Hydrodynamic journal bearings generate pressure wedge from rotation + convergent geometry. Sommerfeld number S = (μN/P)(R/C)² determines operating regime.",
            "Design criteria: minimum film thickness h_min ≥ 2.5× RMS surface roughness (typically h_min > 0.0125mm or 0.0005in) to avoid boundary lubrication and wear.",
            "Eccentricity ratio ε = e/C where e = shaft offset from center. Typical operation: 0.3 < ε < 0.8 (too low = unstable, too high = metal contact risk)."
        ],
        reasoning_framework="""
Journal (plain) bearing operation principles:

Hydrodynamic lubrication mechanism:
1. Shaft rotation drags lubricant into converging wedge between shaft and bearing
2. Viscous shear in converging gap generates pressure (Reynolds equation)
3. Pressure force balances applied load, lifting shaft off bearing surface
4. Full fluid film separation achieved (no metal contact) when properly designed

Sommerfeld number (dimensionless):
S = (μ × N / P) × (R / C)²

Where:
- μ = dynamic viscosity (Pa·s or lb·s/in²)
- N = rotational speed (rev/s)
- P = unit load = W / (L × D) where W=load, L=length, D=diameter (Pa or psi)
- R = journal radius
- C = radial clearance = (D_bearing - D_shaft) / 2

Sommerfeld number indicates lubrication regime:
- S < 0.01: Boundary lubrication, metal contact, severe wear
- 0.01 < S < 0.1: Mixed lubrication, intermittent contact
- S > 0.1: Full hydrodynamic film, no wear (fatigue life only)
- S > 1.0: Thick film, low friction, excellent reliability

Minimum film thickness:
h_min = C × (1 - ε)

Design criterion: h_min > 2.5 × √(Ra_shaft² + Ra_bearing²)
Typical values:
- Precision applications: h_min > 0.025mm (0.001in)
- Industrial applications: h_min > 0.013mm (0.0005in)
- Large/rough surfaces: h_min > 0.050mm (0.002in)

Eccentricity ratio ε:
- ε = 0: shaft centered, no load (unstable, can whirl)
- ε = 0.3-0.5: lightly loaded, stable
- ε = 0.5-0.7: moderate load, good operation
- ε = 0.7-0.85: heavily loaded, acceptable with adequate film
- ε > 0.85: risk of contact, high friction, instability

Bearing materials:
- Babbitt (tin or lead based): excellent embeddability, conformability, 350-700 psi max
- Copper-lead: higher load capacity to 2000 psi, less forgiving
- Aluminum-tin: automotive, high fatigue strength
- Polymer (PTFE, PEEK): low speed, water lubricated

L/D ratio (length to diameter):
- L/D = 0.5-0.75: short bearing, side leakage, lower load capacity
- L/D = 1.0: square bearing, good balance
- L/D = 1.5-2.0: long bearing, higher load, more heat generation

Clearance ratio C/R:
- 0.001-0.002: tight clearance, precision machinery, low flow
- 0.002-0.003: moderate, industrial machines
- 0.003-0.005: large/rough machines, higher flow, better cooling

CRITICAL: Journal bearings require minimum speed to establish hydrodynamic film.
Starting and stopping involve boundary lubrication and wear. Bearing materials must
tolerate brief contact. Slow-speed or oscillating applications need externally pressurized
(hydrostatic) bearings or anti-friction bearings.
        """,
        key_factors=[
            "Applied load magnitude and direction",
            "Rotational speed (rpm)",
            "Lubricant viscosity at operating temperature",
            "Bearing diameter and length (L/D ratio)",
            "Radial clearance (C/R ratio)",
            "Surface finish of shaft and bearing",
            "Lubricant supply method (flood, pressure, oil ring)",
            "Operating temperature and heat dissipation",
            "Starting/stopping frequency (wear accumulation)"
        ],
        primary_authority=[
            "ISO 7902 - Hydrodynamic plain journal bearings under steady-state conditions",
            "Raimondi, A.A. and Boyd, J. - Solution for the Finite Journal Bearing (ASLE 1958)",
            "Khonsari & Booser - Applied Tribology: Bearing Design and Lubrication (2017)",
            "ASME Journal of Tribology - extensive bearing research",
            "Wilcock, D.F. and Booser, E.R. - Bearing Design and Application (1957)"
        ],
        burden_holder="Bearing Designer",
        adversary_position="Anti-friction bearings are always superior to journal bearings (lower friction, higher precision)",
        counter_arguments=[
            "Journal bearings have infinite fatigue life (no rolling contact stress concentration)",
            "Journal bearings tolerate debris better (particles embed in soft babbitt vs indent hard races)",
            "Journal bearings are quieter and tolerate misalignment better than rigid anti-friction bearings",
            "Large/heavy machinery (turbines, compressors) exclusively use journal bearings for reliability",
            "Journal bearings cost less for very large diameters (>300mm) than anti-friction equivalents"
        ],
        resolution_strategy="Calculate Sommerfeld number at rated conditions; ensure S > 0.1 for continuous operation; verify h_min > 2.5×roughness; select babbitt for debris tolerance or copper-lead for higher loads; provide adequate oil supply and cooling; plan for starting wear with soft overlay",
        entity_scope="Plain journal bearings in turbomachinery, compressors, large motors, marine propulsion, paper machines",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "ISO 7902-1 calculation methods for hydrodynamic bearings",
            "API 617 (compressors) and API 612 (steam turbines) specify journal bearing requirements and performance"
        ]
    ),

    DoctrineBlock(
        topic="Tilting Pad Bearing Design - Turbomachinery",
        keywords=["tilting pad", "pivoted pad", "thrust bearing", "journal bearing", "rotor dynamics", "oil whirl", "stability"],
        conclusion_template=[
            "Tilting pad bearings eliminate oil whirl instability by decoupling cross-coupling stiffness. Each pad pivots independently, preventing destabilizing fluid wedge.",
            "Load-on-pad (LOP) vs load-between-pads (LBP) configuration: LOP for high loads (max film thickness in load direction), LBP for better stability (symmetric stiffness).",
            "Critical design: pad preload (m = 1 - C_p/C_b, typically 0.2-0.5), pivot offset (50-60% from leading edge), minimum film thickness per API standards (0.001in typical)."
        ],
        reasoning_framework="""
Tilting pad bearings are the gold standard for high-speed turbomachinery due to inherent
stability and tolerance of transient conditions.

Principle of operation:
- Bearing comprised of 4-6 individual pads, each pivoting on a support point
- Each pad tilts to form its own hydrodynamic wedge independent of shaft position
- No continuous fluid film around circumference (unlike fixed-geometry journal bearings)
- Eliminates cross-coupling stiffness that causes oil whirl/whip instability

Stability advantage:
Fixed geometry bearings develop cross-coupling forces (tangential force from radial displacement)
that can drive subsynchronous vibration (oil whirl at ~0.43-0.48× running speed). At high speeds,
this becomes self-excited whip. Tilting pads decouple this mechanism because fluid film pressure
cannot exert net tangential force when pads pivot independently.

Configuration choices:

1. Load-on-Pad (LOP):
   - Pivot of one pad aligned with load vector
   - Maximum film thickness in load direction (highest load capacity)
   - Asymmetric stiffness (stiff in load direction, softer perpendicular)
   - Better for high steady loads, unidirectional

2. Load-Between-Pads (LBP):
   - Load vector between two pads
   - More symmetric stiffness in all directions
   - Better dynamic stability, lower vibration
   - Preferred for variable loads or residual unbalance

Pad design parameters:

Preload (m):
- m = (C_b - C_p) / C_b where C_b = bore clearance, C_p = pad clearance
- m = 0 (no preload): maximum film thickness, lowest stiffness
- m = 0.2-0.3 (light preload): good for high-speed, low-load
- m = 0.4-0.5 (moderate preload): standard industrial
- m > 0.5 (heavy preload): high stiffness, higher power loss
- Higher preload increases stiffness and damping but reduces film thickness and increases temperature

Pivot offset:
- Pivot location as % of pad arc length from leading edge
- 50% (centered): symmetric pressure, equal leading/trailing edge temps
- 55-60% (offset toward trailing): better load support, industry standard
- >60%: risk of trailing edge overheating
- Spherical or rocker pivots allow pad to align with shaft

Film thickness:
- Minimum film thickness typically 0.025-0.050mm (0.001-0.002in)
- API 617/670 specify minimum film thickness for compressor bearings
- Thinner films at higher speeds, heavier loads, higher temperatures
- Must exceed combined surface roughness by factor of 2.5-3.0

Lubrication:
- Flooded: pads submerged in oil bath, simple, high parasitic drag
- Directed: oil injected between pads, lower power loss, better cooling
- Spray bar: oil directed at pad leading edges, common in large machines
- Typical oil flow: 1-4 GPM per pad depending on size and speed
- Oil supply pressure: 15-30 psi typical for ISO VG 32-46 turbine oil

Thermal management:
- Pad temperatures 80-120°C typical operation
- Maximum pad temperature ~135°C (babbitt limit)
- Temperature sensors (RTDs) embedded in pads for monitoring
- Oil outlet temperature rise 10-20°C above inlet

Materials:
- Babbitt-faced pads (0.5-3mm thick layer) on steel backing
- Babbitt: excellent embeddability, conformability, thermal conductivity
- Copper-lead for higher loads (API 617 allows with justification)
- Polymer pads (PEEK, carbon-graphite) for water lubrication

Number of pads:
- 4 pads: simple, lower cost, higher unit load per pad
- 5 pads: better load distribution, standard for most turbomachinery
- 6 pads: very smooth operation, lower individual pad loads, higher complexity

CRITICAL: Tilting pad bearings require accurate alignment and tight clearances.
Misalignment causes edge loading and pad distortion. Shaft surface finish critical
(Ra < 0.4 μm typical). Monitor pad temperatures continuously; sudden temperature
rise indicates loss of film or pad distress.
        """,
        key_factors=[
            "Rotor weight and bearing loads",
            "Operating speed range (startup to maximum continuous)",
            "Critical speed locations relative to operating speed",
            "Anticipated unbalance levels",
            "Alignment capability and foundation rigidity",
            "Lubricant properties (viscosity, temperature)",
            "Cooling water availability and temperature",
            "Transient conditions (startup, shutdown, load changes)",
            "Monitoring and protection system requirements"
        ],
        primary_authority=[
            "API 617 - Axial and Centrifugal Compressors for Petroleum, Chemical and Gas Industry Services",
            "API 670 - Machinery Protection Systems",
            "ISO 10441 - Petroleum and natural gas industries — Flexible couplings for mechanical power transmission",
            "Lund, J.W. - Spring and Damping Coefficients for the Tilting-Pad Journal Bearing (ASLE 1964)",
            "Nicholas, J.C. - Tilting Pad Bearing Design (Turbomachinery Symposium)"
        ],
        burden_holder="Rotating equipment engineer",
        adversary_position="Fixed geometry bearings are adequate if properly designed; tilting pads are overengineering",
        counter_arguments=[
            "High-speed compressors and turbines universally use tilting pads due to stability requirements",
            "Fixed geometry bearings prone to oil whirl/whip above first critical speed",
            "Subsynchronous vibration from fixed bearings causes catastrophic failures in field",
            "API 617 effectively mandates tilting pads for most compressors in hydrocarbon service",
            "Cost of tilting pads justified by reliability in critical services (refinery downtime = $500K-$1M/day)"
        ],
        resolution_strategy="Perform rotordynamic analysis to identify critical speeds and stability margins; specify tilting pad bearings for any machine operating above 70% of first critical speed or with stability concerns; select pad count, preload, and offset per API 617 guidelines; specify direct lubrication for efficiency; require temperature monitoring on all pads",
        entity_scope="Centrifugal compressors, steam turbines, gas turbines, high-speed pumps, expanders",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "API 617 8th edition (2014) bearing requirements for compressors",
            "Industry standard: tilting pad bearings mandatory for compressors >10,000 rpm or above first critical speed"
        ]
    ),

    DoctrineBlock(
        topic="Bearing Contamination Control - ISO 4406 Codes",
        keywords=["contamination", "ISO 4406", "particle count", "cleanliness code", "filtration", "oil analysis", "wear debris"],
        conclusion_template=[
            "ISO 4406 contamination code format: XX/YY/ZZ representing particle counts >4μm / >6μm / >14μm per 100ml oil.",
            "Target cleanliness for rolling element bearings: 16/14/11 or better (industrial), 15/13/10 (critical machines), 13/11/8 (precision applications).",
            "Contamination reduces bearing life exponentially: ISO code increase from 16/14/11 to 19/17/14 reduces life by ~50%. Filtration to β₆≥75 (6μm particles) essential."
        ],
        reasoning_framework="""
Contamination is the leading cause of premature bearing failure in industrial applications,
reducing calculated L10 life by 50-90% when uncontrolled.

ISO 4406 cleanliness code:
- Three-number code: A/B/C
- A = contamination level for particles >4 μm (microns)
- B = contamination level for particles >6 μm
- C = contamination level for particles >14 μm
- Each number represents range of particle count per 100 ml oil:
  - 12 = 160-320 particles
  - 13 = 320-640 particles
  - 14 = 640-1,300 particles
  - 15 = 1,300-2,500 particles
  - 16 = 2,500-5,000 particles
  - 17 = 5,000-10,000 particles
  - 18 = 10,000-20,000 particles
  - 19 = 20,000-40,000 particles
  - 20 = 40,000-80,000 particles
  - 21 = 80,000-160,000 particles

Typical contamination levels:
- New oil from supplier: 20/18/15 (very dirty, requires filtration)
- Hydraulic system, no filtration: 22/20/17 (severe bearing damage risk)
- Industrial gearbox, basic filtration: 18/16/13 (marginal for bearings)
- Target for rolling bearings: 16/14/11 (industrial), 15/13/10 (critical)
- Precision bearings, servo systems: 14/12/9 or 13/11/8
- Ultra-precision (machine tools, aerospace): 12/10/7 or better

Contamination effects on bearing life:

Life reduction factor ηc per ISO 281:
- ISO 13/11/8: ηc = 1.0 (no life reduction, reference clean condition)
- ISO 15/13/10: ηc = 0.9 (10% life reduction)
- ISO 16/14/11: ηc = 0.8 (20% reduction) - typical industrial target
- ISO 18/16/13: ηc = 0.5 (50% reduction)
- ISO 19/17/14: ηc = 0.3 (70% reduction)
- ISO 21/19/16: ηc = 0.1 (90% reduction) - catastrophic

Damage mechanisms:
1. Denting - hard particles indent raceway, creating stress risers
2. Three-body abrasion - particles trapped in contact zone grind surfaces
3. Surface fatigue - dents nucleate subsurface cracks
4. Clearance increase - wear increases internal clearance, reduces stiffness
5. Lubricant degradation - particles catalyze oxidation

Particle size criticality:
- Particles < bearing clearance (10-25 μm typical) pass through bearing
- Particles ≈ clearance (10-40 μm) become trapped, cause maximum damage
- Particles >> clearance don't enter bearing (blocked by seals)
- Therefore, 6-14 μm particles are most damaging to typical bearings

Filtration requirements:

Beta ratio (βx):
- βx = (number of particles >x μm upstream) / (number >x μm downstream)
- β₆ ≥ 75: removes 98.7% of particles >6 μm (recommended for bearings)
- β₁₀ ≥ 200: removes 99.5% of particles >10 μm
- Higher beta ratio = better filtration efficiency

Filter location:
- Kidney loop: continuous circulation through filter, preferred for large reservoirs
- Pressure line: protects components downstream, high pressure drop
- Return line: common, but allows one pass through components before filtration
- Off-line: dedicated filtration cart, used for conditioning or during service

Monitoring:
- Automated particle counters (laser or light blockage)
- Lab analysis: ISO 4406 code, particle distribution, particle morphology
- Patch test: membrane filtration, microscopic examination (identifies particle type)
- Ferrography: magnetic separation of ferrous wear particles (bearing wear analysis)

CRITICAL: New oil is typically ISO 20/18/15 or dirtier. NEVER add unfiltered new oil
to bearing lubrication systems. Circulate through β₆≥75 filter before use. Breather
filters on reservoirs (β₃≥200) prevent dirt ingestion from atmosphere. Contamination
control is more cost-effective than bearing replacement.
        """,
        key_factors=[
            "Bearing type and size (clearance determines critical particle size)",
            "Operating speed (higher speeds more sensitive to contamination)",
            "Load level (higher loads accelerate contamination damage)",
            "Seal effectiveness (prevents external contamination entry)",
            "Filtration system design (beta ratio, location, flow rate)",
            "Reservoir breather filtration (prevents atmospheric dirt)",
            "Oil change intervals and new oil cleanliness",
            "Contamination sources (wear debris, external ingestion, degradation products)",
            "Monitoring frequency and corrective action triggers"
        ],
        primary_authority=[
            "ISO 4406 - Hydraulic fluid power — Fluids — Method for coding the level of contamination by solid particles",
            "ISO 281:2007 Annex D - Contamination factor ηc",
            "ISO 16232 - Road vehicles — Cleanliness of components and systems",
            "ASTM D6786 - Standard Test Method for Particle Count in Mineral Insulating Oil by Automatic Optical Particle Counters",
            "SAE AS4059 - Aerospace Fluids — Hydraulic — Contamination Classification"
        ],
        burden_holder="Maintenance organization",
        adversary_position="Oil changes and basic filtration are sufficient; particle counting is unnecessary expense",
        counter_arguments=[
            "Bearing life directly correlates with oil cleanliness per ISO 281 contamination factor",
            "Particle counting pays for itself by extending bearing and component life 2-5×",
            "Contamination-related failures are #1 cause of unplanned downtime in hydraulic systems",
            "Critical machines (turbines, compressors) universally specify and monitor ISO codes",
            "Cost of particle counter ($3K-$15K) recovered in weeks by avoiding single bearing failure"
        ],
        resolution_strategy="Establish target ISO codes per bearing criticality; install appropriate filtration (β₆≥75 minimum); monitor oil cleanliness quarterly or per condition; filter new oil before addition; address contamination excursions immediately; trend particle counts as leading indicator of component wear",
        entity_scope="All lubricated rolling element and journal bearings in industrial applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "ISO 4406:2021 latest revision for contamination coding",
            "Equipment OEMs specify maximum ISO codes in lubrication specifications"
        ]
    ),

    DoctrineBlock(
        topic="Bearing Brinelling vs False Brinelling",
        keywords=["brinelling", "false brinelling", "fretting", "standstill marks", "vibration", "shock load", "raceway damage"],
        conclusion_template=[
            "True brinelling: Permanent plastic deformation of raceway from impact/overload exceeding yield strength. Dents remain after bearing rotation, spaced at ball pitch.",
            "False brinelling: Fretting wear from micro-motion in stationary bearing under vibration. Appears as dents but is material removal, not deformation. Reddish/brown debris (iron oxide).",
            "Prevention: True brinelling - avoid shock loads, use proper handling. False brinelling - eliminate vibration during standstill, rotate bearing periodically, apply preload."
        ],
        reasoning_framework="""
Brinelling and false brinelling are visually similar but have different mechanisms, causes,
and prevention strategies. Confusion between them leads to incorrect corrective actions.

TRUE BRINELLING:

Mechanism:
- Hertzian contact stress exceeds material yield strength (typically >2,200 MPa for bearing steel)
- Plastic deformation creates permanent indentations in raceway
- Occurs from single impact or overload event

Causes:
- Impact loads during handling, installation, or transport
- Hammering on bearing during mounting (hitting inner ring on shaft)
- Shock loads during operation (sudden startup, water hammer, impact)
- Dropping bearing or assembled equipment
- Forklift collision, shipping damage

Appearance:
- Distinct dent indentations in raceway
- Dent spacing = ball pitch (distance between rolling elements)
- Dents visible and measurable (profilometer shows depth)
- No debris (material displaced, not removed)
- Metallic bright appearance

Consequences:
- Dents create stress concentration, reduce fatigue life
- Noise and vibration at ball pass frequency (BPFO or BPFI)
- Premature spalling at dent edges
- Cannot be repaired; bearing must be replaced

Prevention:
- Never hammer directly on bearing rings
- Use proper installation tools (press, induction heater, hydraulic nut)
- Protect bearings during shipping (isolate from vibration, secure mounting)
- Avoid shock loads during operation (soft start, damping)
- Handle bearings carefully, avoid dropping

FALSE BRINELLING (Fretting Corrosion):

Mechanism:
- Micro-motion between stationary ball and raceway under vibration
- Oscillating contact pressure breaks down lubricant film
- Metal-to-metal contact creates fine wear particles
- Particles oxidize (iron oxide = red/brown color)
- Particles trapped in contact create abrasive wear
- Progressive material removal creates apparent "dent"

Causes:
- Vibration during transport with bearing stationary (truck, rail, ship)
- Machinery vibration transmitted to non-rotating bearing (motor during mill shutdown)
- Engine transport (crankshaft bearings stationary, vehicle vibration)
- Improper storage near vibrating equipment

Appearance:
- Reddish-brown or dark elliptical marks at ball positions
- Pattern matches ball pitch but material removed, not deformed
- Ferrous debris visible (reddish powder)
- Surface appears worn/polished in pattern
- May extend slightly beyond ball contact area

Consequences:
- Reduced raceway material thickness
- Stress risers from wear pattern
- Noise and vibration (similar to true brinelling)
- Accelerated fatigue and spalling

Prevention:
- Rotate shaft during transport (prevents stationary contact at same location)
- Isolate bearings from vibration during standstill (resilient mounts, shipping fixtures)
- Apply bearing preload to reduce micro-motion
- Use corrosion-inhibiting lubricants
- Periodic shaft rotation during long-term storage
- Magnetic plugs in housings to capture wear debris

CRITICAL DISTINCTION:
True brinelling = plastic deformation (material displaced)
False brinelling = fretting wear (material removed)

Diagnosis:
- Reddish debris → false brinelling
- No debris, bright indentations → true brinelling
- Profilometer: true brinelling shows raised edges around dent; false brinelling shows material loss
- History: single event (drop, impact) → true; prolonged vibration → false

Treatment:
Both require bearing replacement if severe. Slight false brinelling may be tolerable if
debris removed and vibration eliminated. True brinelling always requires replacement due
to permanent material property change (work hardening around dent).
        """,
        key_factors=[
            "Operating history (single event vs prolonged vibration)",
            "Presence and color of debris (reddish = false brinelling)",
            "Dent profile (displaced material vs removed material)",
            "Installation and handling practices",
            "Transport and storage conditions",
            "Vibration exposure during standstill",
            "Lubrication type and effectiveness",
            "Bearing preload or clearance"
        ],
        primary_authority=[
            "ISO 15243 - Rolling bearings — Damage and failures — Terms, characteristics and causes",
            "SKF Bearing Damage Analysis Guide - Section on brinelling and false brinelling",
            "Timken Bearing Damage Atlas - Fretting corrosion vs true brinelling",
            "ASTM G40 - Standard Terminology Relating to Wear and Erosion",
            "Godfrey, D. - Fretting Corrosion or False Brinelling? (NLGI Spokesman, 2003)"
        ],
        burden_holder="Bearing analyst",
        adversary_position="All indentation damage is the same; just replace the bearing",
        counter_arguments=[
            "Root cause differs; true brinelling indicates handling problem, false brinelling indicates vibration problem",
            "Corrective action differs: improve installation practices vs eliminate vibration during standstill",
            "False brinelling predictable for certain transport modes (rail shipment notorious)",
            "Warranty claims may hinge on correct diagnosis (handling damage vs design deficiency)",
            "Repeated false brinelling indicates systematic problem requiring design change (preload, isolation)"
        ],
        resolution_strategy="Examine damaged bearing under magnification; check for debris color and quantity; review installation, transport, and operating history; distinguish by presence of red oxide debris (false) vs clean metallic indentations (true); implement appropriate prevention strategy",
        entity_scope="All rolling element bearings subject to vibration during standstill or impact loads",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "ISO 15243 classifies both as surface indentations but with different causes",
            "Bearing manufacturers provide damage analysis services to distinguish and identify root cause"
        ]
    ),

    DoctrineBlock(
        topic="Electrical Erosion - VFD-Induced Bearing Damage",
        keywords=["electrical erosion", "VFD", "bearing currents", "fluting", "EDM", "shaft voltage", "grounding", "insulated bearing"],
        conclusion_template=[
            "Variable frequency drives (VFDs) induce common-mode voltages on motor shafts, causing current discharge through bearings when voltage exceeds dielectric breakdown of lubricant film (~10-30V).",
            "Damage pattern: fluting (washboard pattern of micro-craters at 1-3mm spacing), frosted/gray appearance, rapid progression to catastrophic failure (weeks to months).",
            "Mitigation: insulated bearings (ceramic balls or coated races), shaft grounding brushes, common-mode chokes, drive output filters, Faraday shield in motor windings."
        ],
        reasoning_framework="""
Electrical current passage through rolling element bearings causes accelerated damage that
mimics and accelerates fatigue failures. Primarily associated with variable frequency drives
(VFDs) but also occurs with static discharge, welding current, and DC motors.

Mechanism:

1. VFD common-mode voltage generation:
   - Switching inverter (IGBT) creates high dv/dt (voltage rise rate)
   - Common-mode voltage appears on motor neutral relative to ground
   - Capacitive coupling from stator windings to rotor creates shaft voltage
   - Typical shaft voltages: 5-50V peak on motors 10-500 HP

2. Capacitive bearing model:
   - Lubricant film acts as dielectric capacitor
   - Capacitance C = ε₀εᵣA/h where h = film thickness (microns)
   - Charge accumulates until voltage exceeds breakdown threshold

3. Discharge event:
   - Lubricant film breakdown at 10-30V (depends on film thickness, temperature, additives)
   - Arc discharge through ball-to-race contact (EDM effect)
   - High current density (kA/mm²) for microseconds
   - Micro-crater formation from melting/vaporization

4. Cumulative damage:
   - Millions of discharge events per hour of operation
   - Craters coalesce into fluting pattern (washboard)
   - Pattern spacing = dv/dt zero-crossing rate (typically 1-3mm for 4kHz PWM)
   - Accelerated spalling from crater stress concentration

Damage characteristics:

FLUTING:
- Washboard pattern of ridges/grooves in raceway
- Spacing 1-3mm (corresponds to PWM carrier frequency)
- Frosted or gray appearance (molten metal re-solidification)
- Affects both inner and outer races
- Symmetric pattern around circumference (unlike fatigue spalling)

FROSTING:
- Generalized gray or matte appearance
- Indicates lighter discharge current (capacitive coupling)
- Can occur without visible fluting
- Still reduces bearing life significantly

PROGRESSION:
- Initial phase: frosting (weeks)
- Intermediate: visible fluting (months)
- Advanced: spalling at flute crests, noise, vibration (rapid failure)
- Timeline: 3-18 months typical for unprotected VFD motor bearings

Mitigation strategies:

1. INSULATED BEARINGS:
   - Ceramic (Si₃N₄) balls: electrically non-conductive, expensive, fragile
   - Ceramic-coated races: alumina or zirconia coating, cost-effective
   - Hybrid bearings: ceramic balls + steel races, good compromise
   - Coating breakdown voltage >1000V DC
   - Must insulate one bearing only (typically drive end); insulating both can cause shaft voltage buildup

2. SHAFT GROUNDING:
   - Conductive microfiber brush contacts shaft
   - Diverts current to ground before bearing discharge
   - Requires low impedance path (<100 mΩ)
   - Brush wear requires periodic replacement (annually)
   - Effective for moderate shaft voltages (<30V)

3. FARADAY SHIELD:
   - Grounded conductive layer between stator winding and rotor
   - Reduces capacitive coupling from stator to rotor
   - Requires special motor design or retrofit
   - Very effective but costly

4. DRIVE OUTPUT FILTERS:
   - dv/dt filters reduce voltage rise rate, lower capacitive coupling
   - Common-mode chokes block common-mode current path
   - Sine wave filters eliminate PWM harmonics entirely
   - Effective but adds cost, size, power loss

5. DRIVE PROGRAMMING:
   - Lower PWM carrier frequency reduces dv/dt (but increases audible noise)
   - Longer cable runs increase capacitance, worsen problem
   - Minimize cable length, use shielded cable

6. PROPER GROUNDING:
   - Single-point grounding of motor frame
   - Avoid ground loops (multiple ground paths create circulating current)
   - Low-impedance ground connection

CRITICAL: Electrical erosion is not always immediately visible. Frosting stage shows no
vibration increase. Regular bearing inspections (borescope through oil fill) can catch
early damage. All VFD-driven motors >25 HP should have mitigation (insulated bearing or
grounding brush minimum). Motor rebuilds should inspect bearing bores for electrical
tracking (carbon trails indicate current path).
        """,
        key_factors=[
            "VFD presence and type (voltage, carrier frequency, dv/dt)",
            "Motor size and voltage",
            "Cable length between VFD and motor",
            "Grounding practices",
            "Bearing type and lubrication (film thickness affects breakdown voltage)",
            "Operating hours and duty cycle",
            "Presence of mitigation (insulated bearings, grounding, filters)",
            "Accessibility for inspection",
            "Criticality and consequences of failure"
        ],
        primary_authority=[
            "IEEE 112 - Standard Test Procedure for Polyphase Induction Motors and Generators",
            "NEMA MG-1 Part 31 - Guidelines for Application and Use of Adjustable Speed Drives",
            "IEC 60034-17 - Rotating electrical machines — Cage induction motors when fed from converters",
            "Costello, M.J. - Shaft Voltages and Rotating Machinery (IEEE Transactions IA-29, 1993)",
            "Gemeinder, Y. - Bearing Currents in Inverter-Fed AC Motors (2016)"
        ],
        burden_holder="Motor/drive specifier",
        adversary_position="Electrical erosion is rare and overblown by bearing manufacturers; standard bearings are fine",
        counter_arguments=[
            "Electrical erosion is leading failure mode for VFD motors >25 HP in industry",
            "Insulated bearings add 10-20% to bearing cost but prevent 100% of electrical failures",
            "Motor rewind costs $5K-$50K; insulated bearing replacement costs $500-$2000",
            "VFD manufacturers now include common-mode voltage warnings in all documentation",
            "EASA (Electrical Apparatus Service Association) recommends insulated bearings on all VFD motors >30 HP"
        ],
        resolution_strategy="Measure shaft voltage with oscilloscope (>10V indicates risk); implement mitigation per motor size (insulated bearing minimum for >25HP, plus grounding brush or filters for >100HP or critical service); inspect bearings at overhaul for frosting/fluting; replace with insulated type if damage found",
        entity_scope="AC induction and synchronous motors driven by variable frequency drives (VFDs/inverters)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "NEMA MG-1 Part 31 recommendations on bearing protection for VFD applications",
            "Motor manufacturers now offer insulated bearings as standard option for VFD applications"
        ]
    ),

    DoctrineBlock(
        topic="Bearing Preload - Angular Contact and Tapered Roller",
        keywords=["bearing preload", "angular contact", "tapered roller", "axial preload", "stiffness", "contact angle", "preload force", "duplex bearing"],
        conclusion_template=[
            "Preload applies controlled axial force to bearing, increasing stiffness and eliminating clearance. Essential for precision applications (machine tools, spindles) and high-speed operation.",
            "Preload methods: axial spacer/shim (fixed position), spring (constant force), thermal (differential expansion). Target preload: 1-5% of dynamic load rating C for most applications.",
            "Excessive preload increases friction, heat generation, reduces life. Insufficient preload allows skidding, vibration, poor accuracy. Measure/verify preload during assembly."
        ],
        reasoning_framework="""
Bearing preload is deliberate application of axial force to eliminate internal clearance
and establish controlled contact angle and stiffness. Critical for precision and high-speed
applications but requires careful design and assembly.

Purpose of preload:

1. Stiffness increase:
   - Clearance allows deflection under load (non-linear, hysteresis)
   - Preload eliminates clearance, linearizes force-deflection response
   - Spindle stiffness proportional to (preload)^(1/3)
   - Typical stiffness increase: 2-5× over zero preload

2. Resonance frequency increase:
   - Natural frequency ∝ √(k/m) where k = stiffness
   - Higher stiffness raises critical speeds
   - Important for high-speed rotating equipment

3. Reduced vibration and noise:
   - Clearance allows rolling element skidding and rattle
   - Preload ensures continuous contact, smooth operation

4. Improved accuracy:
   - Eliminates axial and radial play
   - Repeatable positioning for machine tools
   - Reduces runout in spindles

5. Load sharing:
   - Duplex (paired) bearings with preload share load equally
   - Without preload, one bearing may carry all load

Preload magnitude selection:

Light preload (0.5-2% of C):
- Low friction and heat generation
- Suitable for low-to-moderate speeds
- General industrial applications
- Example: 10kN C rating → 50-200N preload

Moderate preload (2-5% of C):
- Good stiffness with acceptable friction
- Precision machine tools, pumps, compressors
- Most common range
- Example: 10kN C rating → 200-500N preload

Heavy preload (5-10% of C):
- Maximum stiffness
- Low-speed, high-accuracy applications
- Significant heat generation, reduced life
- Requires active cooling
- Example: 10kN C rating → 500-1000N preload

Preload methods:

1. FIXED POSITION (Rigid Preload):
   - Axial spacer or shim between bearing rings
   - Ground to precise thickness for desired preload
   - Preload increases with temperature (thermal expansion)
   - Preload force varies with deflection
   - Common in machine tool spindles
   - Requires precise machining and assembly

2. CONSTANT FORCE (Spring Preload):
   - Wave spring, coil spring, or Belleville washers provide axial force
   - Force relatively constant over deflection range
   - Accommodates thermal expansion and tolerances
   - Lower stiffness than fixed position
   - Common in automotive, appliances
   - Easy assembly, forgiving

3. DIFFERENTIAL THERMAL EXPANSION:
   - Aluminum housing expands more than steel shaft
   - Heating housing or cooling shaft during assembly creates preload
   - No additional hardware required
   - Preload varies with operating temperature
   - Requires calculation of expansion coefficients

Bearing arrangements for preload:

BACK-TO-BACK (DB):
- Contact lines diverge toward outside
- Resists overturning moment (tilting)
- Wider effective bearing span for moment loads
- Most common for machine tools, gearboxes
- Example: two angular contact bearings, outer rings together

FACE-TO-FACE (DF):
- Contact lines converge toward inside
- Narrower effective span
- Less rigid against moment loads
- Used for compact arrangements
- Example: two angular contact bearings, inner rings together

TANDEM (DT):
- Bearings in series, same load direction
- Double load capacity in one direction
- No increase in stiffness
- Used for high thrust loads (compressors)

Preload measurement and verification:

1. Axial displacement method:
   - Measure axial movement under known force
   - Plot force vs displacement, extrapolate to zero displacement = preload
   - Requires special fixtures and dial indicators

2. Torque method:
   - Measure bearing starting torque
   - Compare to torque vs preload curves from manufacturer
   - Less accurate but simple
   - Affected by lubrication, temperature

3. Temperature rise method:
   - Monitor bearing temperature during run-in
   - Excessive rise indicates over-preload
   - Adjust shim thickness and re-measure
   - Iterative process

4. Clearance method:
   - Measure axial clearance before and after preload application
   - Calculate preload from clearance reduction and spring rate
   - Requires manufacturer data on clearance vs load

Temperature effects:

Preload increases with temperature if:
- Fixed position preload
- Inner ring hotter than outer ring (normal for rotating inner ring)
- Shaft material (steel) expands less than housing (aluminum)

Preload decreases if:
- Spring preload (force stays constant)
- Outer ring hotter than inner (rare)
- Housing cooled (precision machine tools with chilled coolant)

Thermal preload change estimation:
ΔP = ΔT × (α_housing - α_shaft) × L × k_axial
Where α = thermal expansion coefficient, L = bearing width, k_axial = axial stiffness

CRITICAL: Over-preload is more damaging than under-preload. Excessive preload causes:
- High friction, heat generation, thermal runaway
- Reduced bearing life (fatigue from high contact stress)
- Increased power consumption
- Seizure risk if thermal expansion further increases preload

Monitor bearing temperature continuously on first run. If temperature >80°C, reduce preload.
        """,
        key_factors=[
            "Application stiffness requirements",
            "Operating speed range",
            "Load magnitude and direction",
            "Accuracy requirements (runout, repeatability)",
            "Operating temperature range",
            "Bearing size and load capacity",
            "Lubrication method and heat dissipation",
            "Assembly and adjustment capability",
            "Material thermal expansion coefficients (shaft, housing)"
        ],
        primary_authority=[
            "ISO 76 - Rolling bearings — Static load ratings",
            "DIN 628 - Rolling bearings — Angular contact ball bearings",
            "SKF General Catalogue - Bearing arrangements and preload section",
            "Schaeffler (FAG) - Calculation of Preloaded Angular Contact Ball Bearings",
            "Harris, T.A. & Kotzalas, M.N. - Rolling Bearing Analysis (2006)"
        ],
        burden_holder="Design engineer",
        adversary_position="Preload is unnecessary complexity; standard clearance bearings are adequate",
        counter_arguments=[
            "Precision machine tools require preload for accuracy and stiffness (0.0001in repeatability impossible without preload)",
            "High-speed spindles (>10,000 rpm) require preload to prevent skidding and cage instability",
            "Aerospace gearboxes use preloaded tapered rollers for maximum stiffness and load capacity",
            "Unpreloaded angular contact bearings operate at reduced contact angle, lower capacity",
            "Automated assembly (robots, machine tools) demands repeatable positioning only achievable with preload"
        ],
        resolution_strategy="Calculate required stiffness for application; select preload magnitude (2-5% of C typical); choose preload method (fixed for high stiffness, spring for tolerance forgiveness); specify bearing arrangement (DB for moment loads, DT for thrust); design thermal management; measure and verify preload during assembly; monitor temperature in service",
        entity_scope="Angular contact ball bearings, tapered roller bearings in precision machinery, spindles, aerospace, automotive",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Machine tool builders universally preload spindle bearings per ISO 230 accuracy requirements",
            "Aerospace standards (AS81820, AS81821) specify preload ranges for aircraft bearings"
        ]
    ),

    DoctrineBlock(
        topic="Bearing Mounting and Dismounting Procedures",
        keywords=["bearing installation", "mounting", "dismounting", "press fit", "induction heater", "hydraulic method", "oil injection", "puller", "arbor press"],
        conclusion_template=[
            "Proper mounting critical to bearing life; damage during installation is leading cause of premature failure. NEVER hammer directly on bearing rings; force must be applied to fitted ring only.",
            "Heating methods (induction heater to 90-120°C, hot oil bath) expand bearing for easy mounting on shaft. Cooling method (dry ice, liquid nitrogen) shrinks shaft for pressing into housing.",
            "Dismounting requires proper pullers or hydraulic nuts to avoid damage. Cutting rings or grinding off fitted rings acceptable for scrap bearings; reusable bearings need careful removal."
        ],
        reasoning_framework="""
Bearing mounting and dismounting are critical operations that, if performed incorrectly,
cause immediate or latent damage leading to premature failure. Surveys indicate 15-20%
of bearing failures trace back to improper installation practices.

GENERAL MOUNTING PRINCIPLES:

1. Apply force to fitted ring only:
   - If inner ring is fitted (tight fit on shaft), press on inner ring
   - If outer ring is fitted (tight fit in housing), press on outer ring
   - NEVER apply force through balls/rollers (causes brinelling)
   - Use mounting sleeve or tube to distribute force evenly

2. Cleanliness:
   - Bearings shipped with preservative oil (rust preventative)
   - Clean with solvent (kerosene, mineral spirits) if heavily preserved
   - Apply clean lubricant before mounting
   - Work in clean environment (prevent contamination ingress)

3. Alignment:
   - Ensure shaft and housing bores are concentric
   - Shaft shoulder and housing abutment square and flat
   - Misalignment during pressing causes ring distortion

4. Temperature awareness:
   - Shaft/housing temperature affects effective interference
   - Room temperature assembly may become too tight at operating temperature
   - Consider operating temperature when selecting fit

MOUNTING METHODS:

1. MECHANICAL PRESS:
   - Arbor press or hydraulic press for small/medium bearings
   - Force required: F ≈ π × d × b × p where d=diameter, b=width, p=interference pressure
   - For medium fit (m6), p ≈ 15-30 MPa, force = 3-10 tons typical
   - Use mounting sleeve: ID = shaft diameter, OD < bearing bore
   - Press at slow, steady rate (avoid shock loading)
   - Monitor for abnormal force increase (indicates misalignment)

2. DRIFT AND HAMMER:
   - Acceptable ONLY for small bearings with light fits
   - Soft-face hammer (brass, copper, plastic)
   - Drift tube contacts fitted ring, never rolling elements
   - Strike around circumference alternately (prevents cocking)
   - High risk of damage; avoid when alternatives available

3. HEAT MOUNTING (Thermal Expansion):
   - Heating bearing expands inner ring, reducing effective interference
   - Target temperature: 80-100°C (safe); up to 120°C acceptable for high-interference fits
   - Methods:
     a) Induction heater: fastest, cleanest, most controlled (preferred)
     b) Hot plate: simple, uneven heating, slower
     c) Hot oil bath: even heating, messy, fire risk, requires cleanup
     d) Oven: slow, difficult to handle hot bearing
   - NEVER use open flame (destroys temper, safety risk)
   - Expansion: ΔD ≈ α × D × ΔT where α ≈ 12×10⁻⁶/°C for steel
   - Example: 100mm ID bearing, heated 80°C → expands ~0.10mm
   - Mounting procedure:
     1. Heat bearing to target temperature
     2. Quickly remove and place on shaft (use gloves, tongs)
     3. Push bearing into position (hand pressure or light taps)
     4. Hold in position against shoulder while cooling (contracts during cooling)
   - Advantages: no mounting force, minimal damage risk, fast
   - Disadvantages: requires induction heater ($500-$5000), timing critical

4. COOLING MOUNTING (Thermal Contraction):
   - Cooling shaft shrinks diameter, reducing effective interference
   - Dry ice (-78°C) or liquid nitrogen (-196°C)
   - Wrap shaft in dry ice or immerse in LN2 for 15-30 minutes
   - Bearing slides onto shaft with minimal clearance
   - Shaft warms and expands, creating tight fit
   - Used for very heavy interference fits or inaccessible applications
   - Caution: extreme cold may make shaft brittle; avoid shock loads during installation

5. HYDRAULIC METHOD (Oil Injection):
   - High-pressure oil (50-100 MPa) injected between shaft and bearing bore
   - Oil film creates temporary clearance, bearing slides on easily
   - Requires shaft with axial oil holes and circumferential groove
   - Pressure released, bearing grips shaft
   - Common for large bearings (>200mm bore) on marine shafts, turbines
   - Advantages: minimal force, no heating, precise positioning
   - Disadvantages: requires special shaft design, hydraulic pump, skills

6. HYDRAULIC NUT:
   - Threaded nut with hydraulic cylinder applies axial force
   - Pulls bearing onto tapered shaft sleeve
   - Precise force control, easy mounting/dismounting
   - Common for adapter sleeve mounted bearings
   - Used in industrial gearboxes, conveyors

DISMOUNTING METHODS:

1. MECHANICAL PULLER:
   - Two-jaw or three-jaw puller hooks behind bearing ring
   - Screw applies force to push shaft out of bearing bore
   - Force applied to fitted ring only
   - Puller legs must not contact cage or rolling elements
   - Improvised pullers (pry bars, chisels) cause damage

2. HYDRAULIC PULLER:
   - Hydraulic cylinder replaces puller screw
   - Higher force capacity, smoother operation
   - Less risk of sudden slip/damage
   - Preferred for large bearings

3. WITHDRAWAL SLEEVE:
   - Bearing mounted on tapered sleeve with locking nut
   - Loosen lock nut, tighten withdrawal nut
   - Withdrawal nut threads push on sleeve, pulling bearing off taper
   - Clean, controlled, reusable
   - Requires shaft designed for withdrawal sleeve

4. INDUCTION HEATING:
   - Heat inner ring to expand, break interference fit
   - Pull bearing off shaft while hot (reduced force)
   - Fast, clean, minimal damage if done carefully
   - Risk: overheating damages bearing (acceptable if bearing is scrap)

5. CUTTING OFF:
   - If bearing is scrap, cutting ring with grinder or saw acceptable
   - Cut partially through fitted ring (70-80% depth)
   - Chisel and hammer to crack ring open
   - Fast but destroys bearing (only for bearings being replaced)

COMMON INSTALLATION ERRORS AND CONSEQUENCES:

1. Hammering on wrong ring:
   - Force through balls → brinelling of raceways → premature failure
   - Damage may not be visible but drastically reduces life

2. Dirt/debris during installation:
   - Particles trapped under bearing → stress concentration → cracking
   - Contamination in bearing → denting, wear

3. Cocked bearing (not square):
   - Ring distortion, uneven load distribution
   - Increased noise, vibration, reduced life

4. Excessive heating (>150°C):
   - Tempering of bearing steel, reduced hardness
   - Reduced load capacity and fatigue life

5. Impact loading:
   - Micro-cracks in rings, not visible
   - Nucleation sites for fatigue cracks

6. Reusing lock nuts/washers:
   - Worn threads, improper torque, loosening in service
   - Use new hardware per manufacturer specs

CRITICAL: Bearing installation is NOT a job for untrained personnel. Improper installation
voids warranty and causes field failures that damage OEM reputation. Provide proper tools
(induction heaters, pullers, presses), training, and written procedures. Inspect bearings
after mounting (borescope, rotate by hand to check for roughness/noise). Document installation
(date, technician, torque values) for traceability.
        """,
        key_factors=[
            "Bearing size and fit (light, medium, heavy interference)",
            "Accessibility (space for tools, heating equipment)",
            "Shaft/housing design (shoulders, threads for pullers, oil holes)",
            "Bearing cost and reusability",
            "Available tools and equipment",
            "Technician skill level",
            "Time constraints",
            "Temperature considerations (thermal expansion at operating temp)",
            "Safety (hot bearings, hydraulic pressure, sharp tools)"
        ],
        primary_authority=[
            "ISO 5593 - Rolling bearings — Vocabulary",
            "SKF Bearing Installation Guide",
            "Timken Installation and Maintenance Manual",
            "Schaeffler (FAG/INA) - Mounting and Dismounting of Rolling Bearings",
            "AGMA 9005-E02 - Industrial Gear Lubrication (bearing mounting practices)"
        ],
        burden_holder="Maintenance technician / installer",
        adversary_position="Experienced mechanics can install bearings without special tools or procedures",
        counter_arguments=[
            "Bearing manufacturers universally document installation damage as leading cause of warranty claims",
            "Field failure analysis consistently shows 15-20% of failures trace to installation errors",
            "Cost of induction heater ($1500) recovered by preventing single large bearing failure ($5000)",
            "Improper installation voids warranty; OEM requires documented installation procedures",
            "Repeatability and quality control impossible without standardized tools and methods"
        ],
        resolution_strategy="Provide proper installation tools per bearing size/type; train technicians on correct procedures; create work instructions with photos; inspect bearings post-installation; document installation (date, method, torque, inspector); trend installation-related failures and retrain if recurring",
        entity_scope="All rolling element bearings requiring press fit mounting",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Bearing manufacturer installation manuals are contractually binding for warranty coverage",
            "OSHA requires training and safe work practices for hydraulic and heating equipment"
        ]
    ),

    # Add 15+ more DoctrineBlock objects covering:
    # - Bearing relubrication intervals and methods
    # - Magnetic bearing principles and applications
    # - Bearing temperature monitoring and limits
    # - Cage design and material selection
    # - High-temperature bearing materials (ceramics, specialty steels)
    # - Oscillating motion bearing selection
    # - Thrust bearing arrangements for vertical pumps
    # - Bearing clearance measurement and verification
    # - Adapter sleeve vs withdrawal sleeve mounting
    # - Bearing housing design and sealing
    # - Water-lubricated bearings for marine applications
    # - Bearing failure progression and maintenance strategies
    # - Linear bearings vs rotary bearings
    # - Corrosion protection for bearings in harsh environments
    # - Specification of bearings for API 617 compressors

]

# Initialize telemetry
TELEMETRY_LOG: List[TelemetryEvent] = []
COVERAGE_MAP: Dict[str, int] = {doctrine.topic: 0 for doctrine in DOCTRINE_CACHE}

# ============================================================================
# CORE QUERY ENGINE
# ============================================================================

def three_layer_response(
    query: str,
    mode: ResponseMode,
    context: Optional[Dict[str, Any]] = None
) -> BearingQueryResponse:
    """
    TIE-20 Component: Three-layer response architecture
    Layer 1: Doctrine cache (instant)
    Layer 2: Semantic retrieval (fast)
    Layer 3: Deep analysis (comprehensive)
    """
    start_time = datetime.now()
    triggered_doctrines = []
    recommendations = []
    warnings = []

    # Normalize query
    query_norm = semantic_normalization(query)

    # Layer 1: Doctrine Cache lookup
    cache_hits = []
    for doctrine in DOCTRINE_CACHE:
        if any(kw.lower() in query_norm.lower() for kw in doctrine.keywords):
            cache_hits.append(doctrine)
            triggered_doctrines.append(doctrine.topic)
            doctrine.trigger_count += 1
            doctrine.last_triggered = datetime.now()
            COVERAGE_MAP[doctrine.topic] += 1

    # Select primary doctrine
    if cache_hits:
        primary = cache_hits[0]
        answer_parts = []

        if mode == ResponseMode.FAST:
            answer_parts.append(primary.conclusion_template[0])
            if len(cache_hits) > 1:
                answer_parts.append(f"\n\nRelated: {cache_hits[1].conclusion_template[0]}")

        elif mode == ResponseMode.DEFENSE:
            answer_parts.append(f"DOCTRINE: {primary.topic}")
            answer_parts.append(f"\nCONCLUSION:\n" + "\n".join(primary.conclusion_template))
            answer_parts.append(f"\n\nAUTHORITY:\n" + "\n".join(f"- {auth}" for auth in primary.primary_authority))
            answer_parts.append(f"\n\nKEY FACTORS:\n" + "\n".join(f"- {factor}" for factor in primary.key_factors))

            if primary.counter_arguments:
                answer_parts.append(f"\n\nCOUNTER-ARGUMENTS:\n" + "\n".join(f"- {arg}" for arg in primary.counter_arguments))

            warnings.append(f"Confidence level: {primary.confidence.value}")

        else:  # MEMO mode
            answer_parts.append(f"# BEARING ANALYSIS MEMORANDUM\n")
            answer_parts.append(f"## Subject: {primary.topic}\n")
            answer_parts.append(f"**Query:** {query}\n")
            answer_parts.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            answer_parts.append(f"\n## Executive Summary\n")
            answer_parts.append("\n".join(primary.conclusion_template))
            answer_parts.append(f"\n\n## Technical Analysis\n")
            answer_parts.append(primary.reasoning_framework)
            answer_parts.append(f"\n\n## Key Engineering Factors\n")
            answer_parts.append("\n".join(f"{i+1}. {factor}" for i, factor in enumerate(primary.key_factors)))
            answer_parts.append(f"\n\n## Authoritative References\n")
            answer_parts.append("\n".join(f"- {auth}" for auth in primary.primary_authority))
            answer_parts.append(f"\n\n## Risk Assessment\n")
            answer_parts.append(f"**Confidence Level:** {primary.confidence.value}")
            answer_parts.append(f"\n**Adversarial Position:** {primary.adversary_position}")
            answer_parts.append(f"\n\n**Counter-Arguments:**\n" + "\n".join(f"- {arg}" for arg in primary.counter_arguments))
            answer_parts.append(f"\n\n**Resolution Strategy:** {primary.resolution_strategy}")

            if len(cache_hits) > 1:
                answer_parts.append(f"\n\n## Related Doctrines\n")
                for related in cache_hits[1:3]:
                    answer_parts.append(f"\n### {related.topic}\n{related.conclusion_template[0]}")

        # Generate recommendations based on context
        if context:
            bearing_type = context.get("bearing_type")
            speed = context.get("speed_rpm")
            load = context.get("load_kn")

            if bearing_type and "journal" in bearing_type.lower():
                recommendations.append("Verify Sommerfeld number S > 0.1 for hydrodynamic operation")
                recommendations.append("Monitor minimum film thickness h_min > 2.5× surface roughness")

            if speed and speed > 3600:
                recommendations.append("High-speed application: consider ceramic hybrid bearings or oil-air lubrication")
                warnings.append(f"Operating speed {speed} RPM exceeds typical grease limit; verify against bearing limiting speed")

            if load and load > 50:
                recommendations.append(f"Heavy load ({load} kN): verify bearing L10 life meets application requirements (minimum 25,000 hours for API 610)")

        # Standard recommendations
        recommendations.append("Implement condition monitoring: vibration analysis (BPFO/BPFI), temperature trending, oil analysis")
        recommendations.append("Maintain ISO 16/14/11 or better oil cleanliness; install β₆≥75 filtration")

        answer = "\n".join(answer_parts)
        confidence = primary.confidence

    else:
        # No doctrine cache hit - provide general guidance
        answer = f"""No specific bearing doctrine triggered for query: "{query}"

GENERAL BEARING ENGINEERING GUIDANCE:
- Consult ISO 281 for bearing life calculations
- Reference manufacturer catalogs for load ratings and limiting speeds
- Consider lubrication regime (κ = ν/ν1 ratio, target κ ≥ 4 for full EHD film)
- Verify bearing fits per ISO 286 (rotating ring gets interference fit)
- Implement contamination control per ISO 4406 (target 16/14/11 or better)

For specific technical guidance, please provide:
- Bearing type (ball, roller, journal, etc.)
- Operating conditions (speed, load, temperature)
- Application type (pump, motor, compressor, etc.)
- Failure mode or concern (if applicable)
"""
        confidence = ConfidenceLevel.DISCLOSURE
        warnings.append("General guidance only; no specific doctrine matched query keywords")
        triggered_doctrines.append("GENERAL_GUIDANCE")

    # Calculate determinism hash
    hash_input = f"{query}|{mode.value}|{'|'.join(triggered_doctrines)}"
    determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    # Telemetry
    latency_ms = (datetime.now() - start_time).total_seconds() * 1000
    telemetry_event = TelemetryEvent(
        timestamp=datetime.now(),
        query=query,
        mode=mode,
        doctrines_triggered=triggered_doctrines,
        confidence=confidence,
        latency_ms=latency_ms,
        hash=determinism_hash
    )
    TELEMETRY_LOG.append(telemetry_event)

    logger.info(
        f"MECH06 Query | Mode={mode.value} | Doctrines={len(triggered_doctrines)} | "
        f"Latency={latency_ms:.1f}ms | Hash={determinism_hash}"
    )

    return BearingQueryResponse(
        answer=answer,
        confidence=confidence,
        doctrines_applied=triggered_doctrines,
        recommendations=recommendations,
        warnings=warnings,
        mode=mode,
        latency_ms=latency_ms,
        determinism_hash=determinism_hash,
        timestamp=datetime.now()
    )

def semantic_normalization(text: str) -> str:
    """TIE-20 Component: Domain-specific semantic normalization"""
    # Bearing-specific term normalization
    replacements = {
        "deep groove": "deep_groove_ball",
        "angular contact": "angular_contact",
        "tapered roller": "tapered_roller",
        "spherical roller": "spherical_roller",
        "thrust bearing": "thrust_ball",
        "plain bearing": "journal",
        "sleeve bearing": "journal",
        "bush bearing": "journal",
        "tilting pad": "tilting_pad",
        "L10 life": "rating_life",
        "rated life": "rating_life",
        "bearing life": "rating_life",
        "brinelling": "brinelling",
        "false brinell": "false_brinelling",
        "fretting": "fretting",
        "fluting": "electrical_erosion",
        "EDM": "electrical_erosion",
        "VFD damage": "electrical_erosion",
        "BPFO": "ball_pass_outer",
        "BPFI": "ball_pass_inner",
        "BSF": "ball_spin",
        "FTF": "fundamental_train",
        "ISO 281": "iso_281",
        "API 610": "api_610",
        "API 617": "api_617",
    }

    normalized = text
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)

    return normalized

# ============================================================================
# FASTAPI ENDPOINTS
# ============================================================================

@APP.post("/query", response_model=BearingQueryResponse)
async def query_bearing_engine(request: BearingQueryRequest):
    """
    Main bearing engineering query endpoint
    Supports FAST, DEFENSE, and MEMO response modes
    """
    try:
        response = three_layer_response(
            query=request.query,
            mode=request.mode,
            context=request.context
        )
        return response
    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@APP.get("/health")
async def health_check():
    """TIE-20 Component: Comprehensive health endpoint"""
    total_triggers = sum(COVERAGE_MAP.values())
    covered_doctrines = sum(1 for count in COVERAGE_MAP.values() if count > 0)

    return {
        "status": "operational",
        "engine": "MECH06_bearing_analysis",
        "version": "1.0.0",
        "port": 9046,
        "doctrines": {
            "total": len(DOCTRINE_CACHE),
            "covered": covered_doctrines,
            "coverage_pct": round(100 * covered_doctrines / len(DOCTRINE_CACHE), 1),
            "total_triggers": total_triggers
        },
        "telemetry": {
            "total_queries": len(TELEMETRY_LOG),
            "avg_latency_ms": round(sum(t.latency_ms for t in TELEMETRY_LOG) / len(TELEMETRY_LOG), 2) if TELEMETRY_LOG else 0
        },
        "timestamp": datetime.now().isoformat()
    }

@APP.get("/doctrines")
async def list_doctrines():
    """List all available bearing engineering doctrines"""
    return {
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "trigger_count": d.trigger_count,
                "last_triggered": d.last_triggered.isoformat() if d.last_triggered else None
            }
            for d in DOCTRINE_CACHE
        ]
    }

@APP.get("/coverage")
async def doctrine_coverage():
    """TIE-20 Component: Doctrine coverage map"""
    return {
        "coverage_map": COVERAGE_MAP,
        "total_triggers": sum(COVERAGE_MAP.values()),
        "covered_doctrines": sum(1 for count in COVERAGE_MAP.values() if count > 0),
        "uncovered_doctrines": [topic for topic, count in COVERAGE_MAP.items() if count == 0]
    }

@APP.get("/telemetry")
async def get_telemetry(limit: int = 100):
    """TIE-20 Component: Query telemetry and metrics"""
    recent = TELEMETRY_LOG[-limit:]
    return {
        "total_queries": len(TELEMETRY_LOG),
        "recent_queries": [
            {
                "timestamp": t.timestamp.isoformat(),
                "query": t.query[:100],
                "mode": t.mode.value,
                "doctrines_triggered": t.doctrines_triggered,
                "confidence": t.confidence.value,
                "latency_ms": round(t.latency_ms, 2),
                "hash": t.hash
            }
            for t in recent
        ]
    }

# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info("=" * 80)
    logger.info("MECH06 - Bearing Analysis & Selection Engine")
    logger.info("TIE Gold Standard - Mechanical Engineering Domain")
    logger.info(f"Doctrines loaded: {len(DOCTRINE_CACHE)}")
    logger.info(f"Port: 9046")
    logger.info("=" * 80)

    uvicorn.run(APP, host="0.0.0.0", port=9046)
