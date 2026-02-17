"""
MECH07 - Vibration Analysis & Diagnostics Engine
TIE Gold Standard - Mechanical Engineering Domain
Port: 9047
Version: 1.0.0

Domain: Machinery vibration analysis, fault diagnostics, rotor dynamics, balancing
Authority: ISO 10816, ISO 7919, API 670, industry standards
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ============================================================================
# DOMAIN ENUMS
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
    DIAGNOSTIC = "DIAGNOSTIC"
    REPORTING = "REPORTING"
    MAINTENANCE = "MAINTENANCE"

class FaultType(str, Enum):
    UNBALANCE = "UNBALANCE"
    MISALIGNMENT = "MISALIGNMENT"
    BEARING_DEFECT = "BEARING_DEFECT"
    GEAR_FAULT = "GEAR_FAULT"
    LOOSENESS = "LOOSENESS"
    RESONANCE = "RESONANCE"
    BENT_SHAFT = "BENT_SHAFT"
    OIL_WHIRL = "OIL_WHIRL"
    BLADE_PASS = "BLADE_PASS"
    ELECTRICAL = "ELECTRICAL"

class VibrationMetric(str, Enum):
    DISPLACEMENT = "DISPLACEMENT"
    VELOCITY = "VELOCITY"
    ACCELERATION = "ACCELERATION"

class BearingFrequency(str, Enum):
    BPFO = "BPFO"  # Ball Pass Frequency Outer race
    BPFI = "BPFI"  # Ball Pass Frequency Inner race
    BSF = "BSF"    # Ball Spin Frequency
    FTF = "FTF"    # Fundamental Train Frequency


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class VibrationQuery(BaseModel):
    query_text: str = Field(..., description="Vibration analysis question")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    context: Optional[Dict[str, Any]] = Field(default=None)
    machine_type: Optional[str] = Field(default=None)
    rpm: Optional[float] = Field(default=None)
    zones: List[AnalysisZone] = Field(default=[AnalysisZone.DIAGNOSTIC])

class VibrationResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    analysis_zone: AnalysisZone
    response_mode: ResponseMode
    fault_indicators: List[str]
    recommendations: List[str]
    standards_referenced: List[str]
    determinism_hash: str
    telemetry: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrine_count: int
    cache_size: int
    uptime_seconds: float


# ============================================================================
# DOCTRINE BLOCK
# ============================================================================

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    zone: AnalysisZone
    fault_type: Optional[FaultType] = None
    counter_arguments: List[str] = field(default_factory=list)
    measurement_considerations: List[str] = field(default_factory=list)


# ============================================================================
# DOCTRINE CACHE - 25+ VIBRATION ANALYSIS BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    DoctrineBlock(
        topic="unbalance_diagnosis",
        keywords=["unbalance", "1x", "running speed", "radial vibration", "static couple dynamic"],
        conclusion_template=[
            "Unbalance produces strong 1X vibration component (at running speed) predominantly in radial direction",
            "Phase analysis differentiates static (in-phase), couple (180° out-of-phase), and dynamic unbalance",
            "Vibration amplitude typically proportional to square of speed; vector balancing most effective remedy"
        ],
        reasoning_framework="""
UNBALANCE DIAGNOSTIC FRAMEWORK:
1. FREQUENCY SIGNATURE: Pure 1X running speed dominance in FFT spectrum
   - Little to no harmonics (2X, 3X minimal compared to 1X)
   - Narrow peak width indicates stable frequency

2. DIRECTIONAL CHARACTERISTICS:
   - Radial vibration far exceeds axial (typically >10:1 ratio)
   - Horizontal and vertical magnitudes similar for static unbalance
   - Phase difference between bearings reveals type:
     * Static: 0° phase difference (centerline bow)
     * Couple: 180° phase difference (rocking motion)
     * Dynamic: Variable phase (combination of static + couple)

3. SPEED DEPENDENCE:
   - Vibration amplitude ∝ RPM² (centrifugal force = mrω²)
   - Below first critical: amplitude increases with speed
   - Near critical speed: resonance amplification occurs
   - Above critical: amplitude may decrease but phase shifts 90°

4. BALANCING APPROACH:
   - Single-plane balancing: adequate for static unbalance (length/diameter < 0.5)
   - Two-plane balancing: required for couple/dynamic (length/diameter > 0.5)
   - Influence coefficient method: measures system response to trial weights
   - Trim balancing: fine-tune after initial correction

5. ACCEPTANCE CRITERIA (ISO 21940-11):
   - Balance quality grade G: G = (e·ω)/1000 where e=eccentricity, ω=angular velocity
   - Rigid rotors: G2.5 (precision grinding), G6.3 (general machinery), G16 (agricultural)
""",
        key_factors=[
            "1X vibration dominance with minimal harmonics",
            "Radial >> axial vibration amplitude",
            "Phase relationship between bearing locations",
            "Amplitude increases with square of speed",
            "Rotor length-to-diameter ratio determines balancing planes needed",
            "Proximity to critical speeds amplifies unbalance response"
        ],
        primary_authority=[
            "ISO 21940-11 (Rotodynamic balancing)",
            "ISO 1940-1 (Balance quality requirements)",
            "API 610 (Centrifugal pumps vibration limits)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.DIAGNOSTIC,
        fault_type=FaultType.UNBALANCE,
        counter_arguments=[
            "1X vibration alone insufficient—misalignment also produces 1X but with higher axial component",
            "Bent shaft produces 1X but 180° phase across coupling unlike unbalance",
            "Eccentric rotor (machining error) mimics unbalance but cannot be corrected by adding weight"
        ],
        measurement_considerations=[
            "Measure at both bearings in horizontal, vertical, axial directions",
            "Record phase using tachometer/keyphasor for vector analysis",
            "Separate measurements before and after balancing for influence coefficients"
        ]
    ),

    DoctrineBlock(
        topic="misalignment_diagnosis",
        keywords=["misalignment", "2x", "axial vibration", "angular parallel offset", "coupling"],
        conclusion_template=[
            "Misalignment generates elevated 2X and 3X harmonics with significant axial vibration component",
            "Angular misalignment produces axial vibration; parallel offset produces high radial vibration",
            "Phase measurements across coupling reveal 180° difference for angular misalignment"
        ],
        reasoning_framework="""
MISALIGNMENT DIAGNOSTIC FRAMEWORK:
1. FREQUENCY SPECTRUM PATTERN:
   - 1X, 2X, 3X harmonics all significant (not just 1X like unbalance)
   - 2X often exceeds 1X in severe cases
   - Harmonic amplitudes increase disproportionately with speed

2. ANGULAR MISALIGNMENT (shaft centerlines intersect but not parallel):
   - High AXIAL vibration (often exceeds radial)
   - 180° phase difference in axial direction across coupling
   - Flex coupling bends twice per revolution → 2X vibration prominent

3. PARALLEL OFFSET (shaft centerlines parallel but offset):
   - High RADIAL vibration
   - Phase same or 180° across coupling in radial direction
   - Coupling operates in constant bending state

4. COMBINATION MISALIGNMENT (most common):
   - Both angular and parallel components present
   - Complex phase patterns requiring 3D analysis
   - Soft foot often underlying cause

5. VERIFICATION METHODS:
   - Dial indicator/laser alignment: quantify offset/angularity
   - Reverse dial method: measures actual shaft positions
   - Hot alignment: account for thermal growth during operation
   - Soft foot check: <0.002" movement when loosening hold-down bolts

6. COUPLING TYPE INFLUENCE:
   - Gear coupling: tolerates angular, sensitive to parallel
   - Disc coupling: very sensitive to misalignment
   - Elastomeric: masks misalignment but wears rapidly
""",
        key_factors=[
            "Multiple harmonics (2X, 3X) comparable to or exceeding 1X",
            "High axial vibration indicates angular misalignment",
            "180° axial phase across coupling confirms angular component",
            "Thermal growth changes alignment—hot vs cold alignment critical",
            "Soft foot amplifies misalignment effects",
            "Coupling type determines tolerance and vibration signature"
        ],
        primary_authority=[
            "ISO 10816-3 (Rotating machinery vibration evaluation)",
            "API 670 (Machinery protection systems)",
            "ANSI/ASA S2.75 (Laser-based alignment)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.DIAGNOSTIC,
        fault_type=FaultType.MISALIGNMENT,
        counter_arguments=[
            "High 2X can also indicate looseness, cocked bearing, or eccentric shaft",
            "Bent shaft produces axial vibration but different phase pattern",
            "Foundation resonance at 2X running speed can mimic misalignment"
        ],
        measurement_considerations=[
            "Measure axial vibration on both bearing housings and coupling faces",
            "Record phase in all three axes at multiple locations",
            "Perform measurements hot and cold to assess thermal growth"
        ]
    ),

    DoctrineBlock(
        topic="bearing_defect_frequencies",
        keywords=["bearing", "BPFO", "BPFI", "BSF", "FTF", "sidebands", "envelope", "demodulation"],
        conclusion_template=[
            "Rolling element bearing defects generate vibration at specific non-synchronous frequencies calculable from geometry",
            "Outer race defects (BPFO) modulated by shaft speed produce sidebands; inner race (BPFI) produce different pattern",
            "Envelope/demodulation analysis reveals bearing tones obscured in raw spectrum by higher energy components"
        ],
        reasoning_framework="""
BEARING DEFECT FREQUENCY FRAMEWORK:
1. FUNDAMENTAL BEARING FREQUENCIES:
   BPFO = (N_b/2) × (1 - (B_d/P_d)cosφ) × RPM/60  [Outer race defect]
   BPFI = (N_b/2) × (1 + (B_d/P_d)cosφ) × RPM/60  [Inner race defect]
   BSF  = (P_d/2B_d) × (1 - (B_d/P_d)²cos²φ) × RPM/60  [Ball/roller defect]
   FTF  = (1/2) × (1 - (B_d/P_d)cosφ) × RPM/60  [Cage defect]

   Where: N_b = number of balls/rollers, B_d = ball diameter,
          P_d = pitch diameter, φ = contact angle

2. OUTER RACE DEFECT (BPFO) SIGNATURE:
   - Defect stationary in space, rotating load passes over it
   - Peak at BPFO with sidebands at 1X running speed (RPM/60)
   - Amplitude modulation: BPFO ± 1X, BPFO ± 2X, etc.
   - Relatively stable amplitude as load zone doesn't change

3. INNER RACE DEFECT (BPFI) SIGNATURE:
   - Defect rotates with shaft, load zone stationary
   - Peak at BPFI with sidebands spaced at FTF (cage frequency)
   - Higher BPFI frequency than BPFO (inner race spins faster relative to balls)
   - Amplitude modulation varies as defect enters/exits load zone

4. ROLLING ELEMENT DEFECT (BSF):
   - Each ball impacts defect twice per revolution (inner + outer race)
   - Peak at BSF, often weak in spectrum
   - Generates high-frequency impacts—better seen in envelope analysis

5. CAGE DEFECT (FTF):
   - Lowest frequency (cage rotates at ~40% shaft speed)
   - Often accompanied by nonsynchronous 1X sideband clusters
   - Typically indicates lubrication failure or cage wear

6. ENVELOPE (DEMODULATION) ANALYSIS:
   - High-pass filter (10-40 kHz) isolates bearing resonance band
   - Rectify and low-pass filter to extract modulation envelope
   - Bearing defect frequencies appear clearly without 1X masking
   - Essential for early detection before vibration becomes severe

7. PROGRESSION PATTERN:
   - Stage 1: Ultrasonic frequencies (SPM, shock pulse)
   - Stage 2: Bearing frequencies appear in envelope spectrum
   - Stage 3: Bearing tones visible in raw velocity spectrum
   - Stage 4: Elevated broadband noise, increased overall levels
   - Stage 5: Discrete harmonics of defect frequencies
""",
        key_factors=[
            "Bearing frequencies are non-synchronous (not integer multiples of RPM)",
            "BPFI > BPFO always (inner race frequency higher)",
            "Sidebands spacing identifies defect location (1X=outer, FTF=inner)",
            "Envelope analysis 100-1000X more sensitive than raw spectrum",
            "Bearing manufacturer data required for exact frequency calculation",
            "Defect progression follows predictable stages over time"
        ],
        primary_authority=[
            "ISO 29821-1 (Bearing vibration measurement)",
            "ISO 20816-1 (Condition monitoring of bearing vibration)",
            "SKF bearing maintenance handbook"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.DIAGNOSTIC,
        fault_type=FaultType.BEARING_DEFECT,
        counter_arguments=[
            "Non-bearing sources can create similar non-synchronous tones (gear mesh, electrical)",
            "Bearing frequencies vary with load—calculated values are theoretical",
            "Some bearing designs (cylindrical roller, spherical) have different formulas",
            "Integrated bearing housings complicate frequency transmission path"
        ],
        measurement_considerations=[
            "Mount accelerometer on bearing housing near load zone",
            "Use high-frequency accelerometer (>10 kHz bandwidth) for envelope analysis",
            "Obtain bearing geometry from manufacturer for accurate frequency calculation",
            "Trending envelope amplitude (gE, gSE) more reliable than spot checks"
        ]
    ),

    DoctrineBlock(
        topic="vibration_severity_standards",
        keywords=["ISO 10816", "ISO 7919", "velocity", "displacement", "zone A B C D", "alarm trip"],
        conclusion_template=[
            "ISO 10816 evaluates vibration severity based on velocity (mm/s RMS) for rigid-mounted machines",
            "ISO 7919 uses shaft relative displacement for machines with fluid-film bearings and proximity probes",
            "Four zones (A=new, B=acceptable, C=tolerable, D=unacceptable) guide maintenance decisions"
        ],
        reasoning_framework="""
VIBRATION SEVERITY EVALUATION FRAMEWORK:
1. ISO 10816 STRUCTURE (velocity-based):
   - Part 1: General guidelines
   - Part 3: Industrial machines (15-300 kW, rigid foundations)
   - Part 6: Reciprocating machines >100 kW
   - Part 7: Rotodynamic pumps
   - Part 21: Horizontal axis wind turbines

2. SEVERITY ZONES (ISO 10816):
   Zone A (Green): Newly commissioned machines, vibration of new machines
   Zone B (Yellow): Acceptable for unrestricted long-term operation
   Zone C (Orange): Tolerable for limited period; corrective action required
   Zone D (Red): Unacceptable; damage likely; immediate shutdown recommended

3. MACHINE CLASSIFICATION GROUPS:
   Group 1: Small machines (15-75 kW), rigidly mounted
     - Zone B/C boundary: 2.8 mm/s, Zone C/D boundary: 7.1 mm/s
   Group 2: Medium machines (75-300 kW), rigid or flexible foundation
     - Zone B/C boundary: 4.5 mm/s, Zone C/D boundary: 11.2 mm/s
   Group 3: Large machines (>300 kW), rigid foundation
     - Zone B/C boundary: 7.1 mm/s, Zone C/D boundary: 18 mm/s
   Group 4: Large machines (>300 kW), flexible foundation
     - Zone B/C boundary: 11.2 mm/s, Zone C/D boundary: 28 mm/s

4. ISO 7919 STRUCTURE (displacement-based):
   - Measures shaft vibration relative to bearing using proximity probes
   - Applicable to machines with sleeve bearings and speeds >600 RPM
   - Part 1: General guidelines
   - Part 3: Coupled industrial machines
   - Part 4: Gas turbine sets (excluding aircraft)
   - Part 5: Hydraulic turbine generator sets

5. SHAFT DISPLACEMENT ZONES (ISO 7919-1):
   - Criteria based on peak-to-peak displacement in micrometers
   - Zone boundaries scale with machine rated speed and bearing type
   - Typical large turbine: Zone C/D boundary = 200-250 μm pk-pk

6. API 670 CRITERIA (MACHINERY PROTECTION):
   - Alert level: typically 60-70% of trip setpoint
   - Trip level: Zone D boundary or machine-specific limit
   - Provides for both radial and axial vibration limits

7. MEASUREMENT LOCATIONS:
   - Bearing housing vibration (ISO 10816): on bearing cap, near shaft centerline
   - Shaft vibration (ISO 7919): proximity probes 45° or 90° apart (X-Y)
   - Axial position: thrust bearing location

8. FREQUENCY RANGE:
   - 10 Hz to 1000 Hz typical evaluation range
   - Broadband RMS value used for zone classification
   - Narrowband analysis identifies fault frequencies
""",
        key_factors=[
            "Machine size and mounting type determine applicable severity limits",
            "Velocity (mm/s RMS) for bearing housing, displacement (μm pk-pk) for shaft",
            "Zone C indicates need for corrective action before reaching Zone D",
            "Baseline trending more valuable than absolute zone classification",
            "API 670 trip setpoints typically align with Zone D boundaries",
            "Different standards apply to different machine types—verify applicability"
        ],
        primary_authority=[
            "ISO 10816 series (Mechanical vibration—Evaluation of machine vibration)",
            "ISO 7919 series (Mechanical vibration—Evaluation of shaft vibration)",
            "API 670 (Machinery protection systems)",
            "API 610/API 617 (Pump/compressor vibration limits)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.REPORTING,
        counter_arguments=[
            "Zone boundaries are guidelines, not absolute limits—some machines operate safely in Zone C",
            "Standards developed for constant-speed machines—variable speed may require adjustment",
            "Proximity probe measurements affected by shaft runout and electrical noise",
            "Single-point measurements may miss vibration at other bearing locations"
        ],
        measurement_considerations=[
            "Measure at multiple bearing locations and directions (H, V, A)",
            "Document machine operating condition (load, speed, temperature)",
            "Establish baseline when machine is new or recently overhauled",
            "Trend measurements over time—sudden changes more significant than absolute values"
        ]
    ),

    DoctrineBlock(
        topic="resonance_identification",
        keywords=["resonance", "natural frequency", "critical speed", "amplification", "mode shape", "coast down"],
        conclusion_template=[
            "Resonance occurs when excitation frequency coincides with system natural frequency, amplifying vibration 10-50X",
            "Critical speed is resonance of rotor system; operational speeds should avoid ±20% of critical",
            "Impact testing or coast-down analysis reveals natural frequencies and mode shapes"
        ],
        reasoning_framework="""
RESONANCE DIAGNOSTIC FRAMEWORK:
1. RESONANCE PHYSICS:
   - Every mechanical system has natural frequencies determined by mass, stiffness, damping
   - When forcing frequency = natural frequency: X = F/(k-mω²+jcω) → maximum amplitude
   - Amplification factor Q = 1/(2ζ) where ζ = damping ratio
   - Lightly damped systems (ζ < 0.05): Q > 10, severe resonance

2. CRITICAL SPEED (ROTOR RESONANCE):
   - First critical: fundamental bending mode of rotor
   - Second critical: first harmonic bending mode (S-shape)
   - Rigid rotor (operates below first critical): vibration ∝ unbalance force
   - Flexible rotor (operates above first critical): vibration limited by damping
   - Operating speeds should be >20% away from criticals (separation margin)

3. STRUCTURAL RESONANCE IDENTIFICATION:
   - Coast-down/run-up analysis: plot vibration vs. speed (waterfall, Bode)
   - Peak at constant frequency during speed change = structural resonance
   - Peak tracking with speed (1X line) = forced response
   - Impact testing: tap structure, measure FRF (frequency response function)
   - Modal analysis: identifies mode shape, damping ratio, natural frequency

4. RESONANCE INDICATORS IN SPECTRUM:
   - Very narrow peak (high Q factor)
   - Amplitude sensitive to small speed changes
   - 90° phase shift through resonance
   - Multiple harmonics may excite same resonance (2X, 3X, etc.)

5. CAMPBELL DIAGRAM (CRITICAL SPEED MAP):
   - Plots natural frequencies vs. rotor speed
   - Diagonal lines represent excitation orders (1X, 2X, blade pass, etc.)
   - Intersections = potential resonances
   - Exclusion zones marked ±20% around criticals

6. RESONANCE MITIGATION STRATEGIES:
   - Change stiffness: add/remove supports, increase/decrease span
   - Change mass: add/remove material, relocate components
   - Add damping: elastomeric mounts, constrained-layer damping
   - Detune: shift natural frequency away from excitation
   - Operating speed change: avoid resonant region entirely
   - Balancing: reduce forcing function amplitude

7. COMMON RESONANT STRUCTURES:
   - Baseplates and sole plates: 20-80 Hz typical
   - Motor/pump frames: 50-150 Hz
   - Piping systems: 10-50 Hz
   - Foundation: 5-30 Hz (most critical to avoid)
   - Rolling element bearing cages: 0.35-0.45X running speed
""",
        key_factors=[
            "Narrow spectral peak with high amplitude indicates resonance",
            "Phase shift of 90° through resonance peak is diagnostic",
            "Vibration amplitude extremely sensitive to small speed changes at resonance",
            "Coast-down waterfall shows constant-frequency peak for structural resonance",
            "Operating speed should avoid ±20% of any critical speed",
            "Foundation resonance most dangerous—can destroy equipment rapidly"
        ],
        primary_authority=[
            "ISO 10816-3 (Evaluation of vibration in industrial machines)",
            "API 684 (Rotor dynamics tutorial)",
            "ISO 20806 (Modal testing for rotating machinery)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.DIAGNOSTIC,
        fault_type=FaultType.RESONANCE,
        counter_arguments=[
            "High vibration at constant frequency could be external forcing, not resonance",
            "Phase measurements can be misleading if multiple modes overlap",
            "Nonlinear systems have amplitude-dependent natural frequencies",
            "Coupled modes (rotor + foundation) complicate Campbell diagram interpretation"
        ],
        measurement_considerations=[
            "Measure during coast-down to separate forced response from resonance",
            "Record phase vs. speed for 90° shift confirmation",
            "Impact test in non-operating state to identify unloaded natural frequencies",
            "Multiple measurement points reveal mode shape (in-phase vs out-of-phase motion)"
        ]
    ),

    DoctrineBlock(
        topic="gear_mesh_frequency_analysis",
        keywords=["gear", "GMF", "tooth mesh", "sidebands", "hunting tooth", "backlash", "wear"],
        conclusion_template=[
            "Gear mesh frequency (GMF) = number of teeth × shaft RPM appears prominently in healthy gears",
            "Sidebands around GMF spaced at shaft speed indicate modulation from eccentricity, wear, or tooth damage",
            "Hunting tooth frequency and its harmonics indicate distributed wear; localized faults produce once-per-rev impacts"
        ],
        reasoning_framework="""
GEAR FAULT DIAGNOSTIC FRAMEWORK:
1. FUNDAMENTAL GEAR FREQUENCIES:
   GMF = N_teeth × (RPM/60)  [Gear Mesh Frequency]
   Hunting Tooth Frequency = GMF / GCF(N_pinion, N_gear)

   Where GCF = greatest common factor

2. HEALTHY GEAR SIGNATURE:
   - Dominant peak at GMF (tooth mesh fundamental)
   - Small harmonics at 2×GMF, 3×GMF (typically <25% of GMF amplitude)
   - Minimal sidebands around GMF (<10% of GMF peak)
   - Low noise floor between mesh harmonics

3. ECCENTRIC GEAR (RUNOUT):
   - Sidebands at GMF ± 1X shaft speed
   - Amplitude modulation: (GMF - 1X), GMF, (GMF + 1X) pattern
   - Sidebands evenly spaced and symmetrical
   - Caused by: bent shaft, bearing wear, gear bore eccentricity

4. TOOTH WEAR (DISTRIBUTED):
   - Elevated GMF amplitude (increasing over time)
   - Multiple sidebands: GMF ± 1X, GMF ± 2X, GMF ± 3X, etc.
   - Harmonics of GMF also develop sidebands
   - Noise floor increases (broadband energy between peaks)
   - Hunting tooth frequency prominent if wear pattern repeats

5. TOOTH DAMAGE (LOCALIZED):
   - Impact once per revolution of damaged gear
   - Sidebands around GMF at 1X shaft speed of damaged gear
   - Asymmetric sideband pattern (lower sideband may exceed upper)
   - Time waveform shows periodic impulse
   - Higher-order GMF harmonics increase disproportionately

6. BACKLASH / LOOSENESS:
   - Sub-harmonics of GMF (GMF/2, GMF/3, etc.)
   - Chaotic modulation pattern
   - High-amplitude 1X component (gear rattle)
   - Bidirectional load reversal creates double impacts

7. MISALIGNMENT (GEAR):
   - Elevated 2×GMF and 3×GMF (harmonics dominate)
   - Axial vibration component significant
   - Phase difference across gearbox housing
   - Often combined with coupling misalignment signature

8. LUBRICATION FAILURE:
   - Broadband noise increase (1-10 kHz range)
   - Ultrasonic energy elevation (20-40 kHz)
   - GMF amplitude increases as friction rises
   - Temperature rise accompanies vibration increase

9. SIDEBAND ANALYSIS RULES:
   - Sidebands on input (driving) side: problem on that shaft
   - Sidebands on output (driven) side: problem on that shaft
   - Equal sidebands both sides: external modulation (load variation, coupling)
   - Sideband spacing identifies modulation source frequency
""",
        key_factors=[
            "GMF amplitude and harmonic pattern indicate gear health",
            "Sidebands around GMF reveal modulation source (which shaft has the problem)",
            "Hunting tooth frequency indicates distributed contact pattern issues",
            "Localized tooth damage produces once-per-rev impulse in time waveform",
            "Ratio of sideband to GMF amplitude quantifies severity",
            "Increasing noise floor suggests progressive wear"
        ],
        primary_authority=[
            "ISO 10825 (Gearbox vibration monitoring)",
            "AGMA 6025-A16 (Sound of enclosed gear drives)",
            "ANSI/AGMA 2001-D04 (Fundamental rating factors)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.DIAGNOSTIC,
        fault_type=FaultType.GEAR_FAULT,
        counter_arguments=[
            "GMF sidebands can result from external load variation, not gear fault",
            "Belt drives and couplings can create similar modulation patterns",
            "Multi-stage gearboxes have overlapping GMFs from each stage",
            "Helical gears produce axial vibration that complicates radial measurements"
        ],
        measurement_considerations=[
            "Measure on gearbox housing near each mesh location",
            "Accelerometer preferred over velocity for high-frequency GMF",
            "Record both input and output shaft speeds for correct GMF calculation",
            "Time-synchronous averaging isolates specific gear's contribution in multi-stage gearbox"
        ]
    ),

    DoctrineBlock(
        topic="mechanical_looseness_diagnosis",
        keywords=["looseness", "harmonics", "2x 3x 4x", "impacting", "soft foot", "foundation bolts"],
        conclusion_template=[
            "Mechanical looseness generates multiple harmonics (2X, 3X, 4X+) with non-linear amplitude growth",
            "Type A looseness (structural) shows many harmonics; Type B (bearing fit) shows 2X dominance; Type C (component) shows broad spectrum",
            "Soft foot check and bolt torque verification essential before balancing or alignment"
        ],
        reasoning_framework="""
MECHANICAL LOOSENESS DIAGNOSTIC FRAMEWORK:
1. LOOSENESS CLASSIFICATION:
   Type A: Structural looseness (loose foundation bolts, weak baseplate)
   Type B: Looseness in bearing fit (bearing outer race loose in housing)
   Type C: Component looseness (impeller on shaft, coupling hub, gear on shaft)

2. TYPE A (STRUCTURAL) SIGNATURE:
   - Many harmonics: 1X, 2X, 3X, 4X, 5X... up to 10X or higher
   - Harmonics increase disproportionately with force (non-linear)
   - Direction-dependent: may be strong in vertical, weak horizontal
   - Foundation natural frequency often excited
   - Intermittent impacting creates "noisy" waveform

3. TYPE B (BEARING FIT) SIGNATURE:
   - Dominant 2X vibration (≥50% of 1X or greater)
   - Bearing housing "rocks" in loose fit
   - Clearance allows eccentric motion at 2× shaft speed
   - May produce sub-synchronous vibration <1X
   - Axial vibration component typically low

4. TYPE C (COMPONENT) SIGNATURE:
   - Broadband spectrum (noise-like, many frequencies)
   - Whole-order harmonics (1X, 2X, 3X...) and half-orders (0.5X, 1.5X, 2.5X)
   - Time waveform shows clipping or flat-topping
   - Impacts occur at multiple times per revolution
   - High crest factor (peak/RMS > 4) indicates impacting

5. SOFT FOOT DIAGNOSIS:
   - Measure vertical vibration at each foot with dial indicator
   - Loosen one hold-down bolt at a time, observe movement
   - Movement >0.002" (50 μm) indicates soft foot
   - Types: parallel (improper shimming), angular (bent foot), induced (over-torqued bolts)
   - Soft foot amplifies ALL other vibration problems

6. DETECTION METHODS:
   - Coherence function: looseness shows poor coherence (random response)
   - Impact testing: looseness creates multiple resonance peaks (normal structure has clear peaks)
   - Time waveform: impacting shows sharp spikes, clipping, or truncation
   - Orbit analysis: erratic, changing orbit shape indicates looseness

7. PROGRESSION PATTERN:
   - Stage 1: Slight increase in harmonics, stable orbit
   - Stage 2: 2X and 3X become significant, orbit less stable
   - Stage 3: Many harmonics, broadband noise, erratic orbit
   - Stage 4: Sub-synchronous components appear, severe impacting
   - Stage 5: Catastrophic failure (broken bolts, cracked feet, bearing seizure)

8. CORRECTIVE ACTIONS:
   - Structural: re-torque foundation bolts, repair grout, add stiffness
   - Bearing fit: bearing replacement, Loctite, knurling, oversized bearing
   - Component: keyway repair, interference fit, set screws, retaining compounds
   - Soft foot: precision shimming, machining feet, proper bolt torque sequence
""",
        key_factors=[
            "Multiple harmonics with non-linear growth pattern diagnostic for looseness",
            "Type A produces many high-order harmonics; Type B produces 2X dominance",
            "Poor coherence between input force and vibration response indicates looseness",
            "Soft foot must be corrected before alignment or balancing",
            "Impacting time waveform and high crest factor confirm looseness",
            "Directional dependency (vertical >> horizontal) suggests foundation looseness"
        ],
        primary_authority=[
            "ISO 10816-3 (Vibration evaluation for industrial machines)",
            "API 686 (Machinery installation and installation design)",
            "Mobius Institute Category II training (fault diagnosis)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.DIAGNOSTIC,
        fault_type=FaultType.LOOSENESS,
        counter_arguments=[
            "Harmonics can also result from misalignment, bent shaft, or cracked frame",
            "Non-linear behavior appears in rubs, which create similar spectrum",
            "Over-tightened bolts (not looseness) can create foundation distortion and vibration",
            "Resonance at harmonic frequency can amplify specific harmonic without looseness"
        ],
        measurement_considerations=[
            "Soft foot check performed with machine uncoupled and unloaded",
            "Measure vibration before and after bolt tightening to confirm looseness source",
            "Check grout condition—cracked grout indicates foundation problem",
            "Torque wrench verification of all structural bolts"
        ]
    ),

    DoctrineBlock(
        topic="rotor_dynamics_critical_speeds",
        keywords=["critical speed", "campbell diagram", "bode plot", "rotor dynamics", "flexible rotor"],
        conclusion_template=[
            "Critical speeds are rotor natural frequencies where resonance amplifies vibration; operating speeds must avoid ±20% margin",
            "Campbell diagram maps critical speeds vs. excitation orders to identify potential resonances across operating range",
            "Bode plot (amplitude and phase vs. speed) confirms critical speeds by 90° phase shift and amplitude peak"
        ],
        reasoning_framework="""
ROTOR DYNAMICS FRAMEWORK:
1. CRITICAL SPEED THEORY:
   - Rotor acts as beam with distributed mass and stiffness
   - Natural frequency: ω_n = √(k/m) for simple rotor
   - Critical speed: when shaft rotation speed = natural frequency
   - Jeffcott rotor: simplest model with single disk on massless shaft
   - Multi-mass rotors: multiple critical speeds (1st, 2nd, 3rd...)

2. ROTOR CLASSIFICATIONS:
   Rigid rotor: operates well below 1st critical (< 70% of critical)
     - Vibration response primarily from unbalance
     - Amplitude ∝ unbalance × (speed)² / (1 - (speed/critical)²)
     - Balancing effective across entire speed range

   Flexible rotor: operates above 1st critical (> 120% of critical)
     - Self-centering above critical (phase shifts 180°)
     - Vibration limited by damping, less sensitive to unbalance
     - Speed-dependent balancing required (different weights for different speeds)

   Semi-flexible: operates near critical (70-120% of critical)
     - AVOID THIS REGION—high amplification, unpredictable behavior
     - Requires careful design or operational restrictions

3. CAMPBELL DIAGRAM CONSTRUCTION:
   - X-axis: rotor speed (RPM)
   - Y-axis: frequency (Hz or CPM)
   - Horizontal lines: structural natural frequencies (bearing, foundation)
   - Curved lines: rotor natural frequencies (vary with speed due to gyroscopic effects)
   - Diagonal lines: excitation orders (1X, 2X, blade pass, etc.)
   - Intersections: potential resonances requiring investigation
   - Exclusion zones: ±20% around each critical speed

4. BODE PLOT INTERPRETATION:
   - Amplitude plot: vibration magnitude vs. speed during run-up or coast-down
   - Phase plot: phase angle vs. speed (referenced to keyphasor)
   - Critical speed indicators:
     * Peak amplitude at critical speed
     * 90° phase shift through critical (lags by 90° at resonance)
     * Narrow peak if lightly damped, broad peak if well-damped
   - Multiple peaks indicate multiple critical speeds

5. MODE SHAPES:
   1st critical (fundamental): single-loop bending (C-shape)
   2nd critical: two-loop bending (S-shape)
   3rd critical: three-loop bending (W-shape)
   - Node points: zero deflection locations (bearing locations often at nodes)
   - Anti-nodes: maximum deflection points
   - Mode shapes measured via roving probe or impact testing

6. GYROSCOPIC EFFECTS:
   - Disk polar moment of inertia creates gyroscopic stiffening
   - Forward whirl: rotor whirls in same direction as rotation (lower critical)
   - Backward whirl: rotor whirls opposite to rotation (higher critical)
   - Gyroscopic coupling splits critical speeds into forward/backward modes

7. CRITICAL SPEED MODIFICATION:
   Increase critical speed:
     - Increase shaft diameter (stiffness ∝ diameter⁴)
     - Decrease bearing span (shorter = stiffer)
     - Reduce overhang (cantilever) mass
     - Increase bearing stiffness

   Decrease critical speed:
     - Add shaft length or overhang mass
     - Decrease shaft diameter
     - Reduce bearing stiffness (softer mounts)
     - Add distributed mass to shaft

8. DAMPING CONSIDERATIONS:
   - Damping reduces peak amplitude at critical but doesn't change critical speed
   - Internal damping (material hysteresis): speed-dependent, destabilizing above critical
   - External damping (bearings, seals): speed-independent, stabilizing
   - Critical damping ratio ζ = c/(2√(km)) determines amplification factor
""",
        key_factors=[
            "Operating speed must maintain ±20% separation margin from all critical speeds",
            "90° phase shift through resonance confirms critical speed",
            "Campbell diagram identifies all potential resonances across operating range",
            "Flexible rotors self-center above critical with 180° phase change",
            "Gyroscopic effects split critical speeds into forward and backward whirl modes",
            "Shaft stiffness (diameter⁴) most effective parameter for critical speed modification"
        ],
        primary_authority=[
            "API 684 (Tutorial on rotor dynamics)",
            "API 617 (Axial and centrifugal compressors)",
            "ISO 1940-1 (Balance quality requirements for rotors)",
            "Vance, J.M. 'Rotordynamics of Turbomachinery'"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.DIAGNOSTIC,
        counter_arguments=[
            "Campbell diagram predicts potential resonances but actual amplitude depends on forcing function magnitude and damping",
            "Simplified models may miss coupled modes (rotor-bearing-foundation interaction)",
            "Thermal growth and load changes alter bearing stiffness, shifting critical speeds during operation",
            "Anisotropic bearing stiffness creates different critical speeds in horizontal vs. vertical directions"
        ],
        measurement_considerations=[
            "Perform coast-down (not run-up) analysis to avoid process load effects",
            "Measure shaft displacement (proximity probes) and bearing housing acceleration simultaneously",
            "Record phase referenced to keyphasor for Bode plot construction",
            "Multiple measurement points along shaft length reveal mode shapes"
        ]
    ),

    DoctrineBlock(
        topic="balancing_methodology",
        keywords=["balancing", "influence coefficient", "single plane", "two plane", "trim balance", "trial weight"],
        conclusion_template=[
            "Influence coefficient method uses measured response to trial weights to calculate correction weights",
            "Single-plane balancing adequate for static unbalance (L/D < 0.5); two-plane required for dynamic unbalance",
            "Balancing reduces 1X vibration to acceptable levels but cannot fix other faults (misalignment, looseness, etc.)"
        ],
        reasoning_framework="""
BALANCING METHODOLOGY FRAMEWORK:
1. BALANCING FUNDAMENTALS:
   - Unbalance force: F = m·r·ω² (mass × eccentricity × angular velocity²)
   - Goal: add correction mass to create equal and opposite centrifugal force
   - Centrifugal force acts radially outward from center of rotation
   - 180° from heavy spot creates pure couple; same angular location creates static correction

2. SINGLE-PLANE vs. TWO-PLANE DETERMINATION:
   Single-plane (static balancing):
     - Length/Diameter ratio < 0.5 (disk-like rotor)
     - Vibration predominantly in-phase at both bearings
     - Single correction plane adequate
     - Examples: fans, flywheels, grinding wheels

   Two-plane (dynamic balancing):
     - Length/Diameter ratio > 0.5 (shaft-like rotor)
     - Phase difference between bearings indicates couple unbalance
     - Requires correction in two planes to eliminate static + couple components
     - Examples: motors, pumps, compressors, turbines

3. INFLUENCE COEFFICIENT METHOD (SINGLE-PLANE):
   Step 1: Measure initial vibration (amplitude A₀, phase φ₀)
   Step 2: Add trial weight W_trial at arbitrary angle θ_trial
   Step 3: Run machine, measure new vibration (A₁, φ₁)
   Step 4: Calculate influence coefficient: α = (A₁∠φ₁ - A₀∠φ₀) / W_trial
   Step 5: Calculate correction weight: W_corr = -A₀∠φ₀ / α
   Step 6: Install W_corr at calculated angle, verify result

   Influence coefficient α represents system sensitivity: change in vibration per unit unbalance

4. TWO-PLANE BALANCING (FOUR-RUN METHOD):
   Plane 1 and Plane 2 typically near bearing locations or accessible flanges

   Run 1 (initial): Measure vibration at both bearings (A₁₀, φ₁₀) and (A₂₀, φ₂₀)
   Run 2: Add trial weight W₁ in Plane 1, measure (A₁₁, φ₁₁) and (A₂₁, φ₂₁)
   Run 3: Remove W₁, add trial weight W₂ in Plane 2, measure (A₁₂, φ₁₂) and (A₂₂, φ₂₂)
   Run 4: Calculate correction weights C₁, C₂ from influence coefficient matrix, install, verify

   Influence coefficient matrix:
   [α₁₁  α₁₂]   Δvibration at bearing 1 due to weight in planes 1,2
   [α₂₁  α₂₂]   Δvibration at bearing 2 due to weight in planes 1,2

5. VECTOR CALCULATIONS:
   - All measurements are vectors (magnitude + phase angle)
   - Vector subtraction: A₁∠φ₁ - A₀∠φ₀ = change due to trial weight
   - Correction weight often expressed in g·mm or oz·in (mass × radius)
   - Phase angle referenced to keyphasor or tachometer mark

6. TRIAL WEIGHT SELECTION:
   - Too small: insufficient response change, poor influence coefficient accuracy
   - Too large: excessive vibration during trial run, potential damage
   - Rule of thumb: trial weight should change vibration by 30-50%
   - For 1000 RPM rotor at 100 mm radius: 10 grams produces ~1.1 N force

7. TRIM BALANCING:
   - Fine-tuning after initial correction achieves target level
   - Splits correction weight: 60-70% initial, 30-40% trim
   - Allows verification without over-correction
   - Multiple trim iterations may be needed for tight tolerances

8. BALANCING TOLERANCES (ISO 21940-11):
   Balance quality grade G = (e·ω)/1000  where e = eccentricity (μm), ω = rad/s

   G0.4: Ultra-precision (hard disk drives, spindles)
   G1.0: Precision grinders, high-speed machines
   G2.5: Machine tool drives, turbines, compressors
   G6.3: General industrial machinery (motors, pumps)
   G16: Agricultural machinery, construction equipment
   G40: Large, slow-speed equipment (concrete mixers)

9. FIELD BALANCING LIMITATIONS:
   - Cannot fix problems other than unbalance (misalignment, looseness, resonance)
   - Rotor must be cleanly supported (fix looseness first)
   - Non-linear systems (rubs, cracks) yield inconsistent influence coefficients
   - Thermal distortion may require hot balancing
   - Balancing above critical speed requires different technique (modal balancing)
""",
        key_factors=[
            "Influence coefficient method calculates exact correction from measured response to trial weight",
            "Single-plane adequate for L/D < 0.5; two-plane required for L/D > 0.5",
            "Trial weight should produce 30-50% vibration change for accurate influence coefficient",
            "Vector (magnitude + phase) calculations essential—magnitude alone insufficient",
            "Balance quality grade G from ISO 21940-11 defines acceptable residual unbalance",
            "Field balancing only corrects unbalance—verify no other faults before balancing"
        ],
        primary_authority=[
            "ISO 21940-11 (Procedures for balancing rigid rotors)",
            "ISO 21940-12 (Procedures for balancing flexible rotors)",
            "API 610 (Centrifugal pump balancing requirements)",
            "ISO 1940-1 (Balance quality requirements)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.MAINTENANCE,
        counter_arguments=[
            "Influence coefficients assume linear system—non-linearities from cracks or rubs invalidate method",
            "Thermal growth can shift mass distribution, requiring re-balance under operating conditions",
            "Multi-mode flexible rotors require modal balancing, not two-plane balancing",
            "Measurement accuracy limits achievable balance—noise in signal degrades results"
        ],
        measurement_considerations=[
            "Consistent measurement location and sensor orientation for all runs",
            "Tachometer/keyphasor signal quality critical for accurate phase measurement",
            "Document trial weight mass and radial location precisely",
            "Verify rotor can reach stable speed before taking measurements"
        ]
    ),

    DoctrineBlock(
        topic="proximity_probe_installation",
        keywords=["proximity probe", "eddy current", "shaft displacement", "gap voltage", "runout", "calibration"],
        conclusion_template=[
            "Proximity probes measure shaft displacement using eddy current principle; require proper gap voltage setup (typically -8 to -10 VDC)",
            "Electrical runout from shaft surface imperfections must be measured and compensated during installation",
            "Probe installation requires: proper target area (non-magnetic, smooth), correct gap (40-60% of probe range), secure mounting"
        ],
        reasoning_framework="""
PROXIMITY PROBE INSTALLATION FRAMEWORK:
1. EDDY CURRENT OPERATING PRINCIPLE:
   - Probe generates high-frequency magnetic field (1-2 MHz)
   - Eddy currents induced in conductive shaft surface
   - Gap change alters eddy current magnitude → changes probe output voltage
   - Output voltage inversely proportional to gap distance
   - Typical sensitivity: 200 mV/mil (7.87 mV/μm) for 8mm probe

2. PROBE SPECIFICATIONS:
   Common sizes: 5mm, 8mm, 11mm, 14mm, 25mm diameter
   - Larger probe: greater range but lower frequency response
   - 8mm probe: ±1mm (±40 mil) range, up to 10 kHz bandwidth
   - Target area requirement: 3× probe diameter minimum
   - Non-magnetic shaft material: stainless steel 400 series, 4140 steel, chrome plating

3. GAP VOLTAGE SETUP:
   - Initial gap voltage (cold): -8 to -10 VDC typical (mid-range of -18V to -2V scale)
   - Gap voltage = probe output with shaft stationary
   - Proper gap ensures linear region operation (not saturated at either extreme)
   - Gap = (Gap Voltage - Bias Voltage) / Probe Sensitivity
   - Example: -8V gap, -18V bias, 200mV/mil sensitivity → 50 mil (1.27mm) gap

4. ELECTRICAL RUNOUT COMPENSATION:
   Electrical runout: apparent displacement from non-uniform shaft surface
   Sources: magnetic permeability variation, surface hardness variation, scratches, coatings

   Procedure:
   - Lift shaft using hydraulic jack to center it in bearing clearance
   - Slowly rotate shaft by hand, record probe output (full revolution)
   - Runout waveform = electrical runout (shaft surface variation)
   - Store runout vector in analyzer for glitch removal
   - Measured vibration = (dynamic signal) - (stored runout vector)

   Acceptable runout: <25% of total bearing clearance
   Excessive runout (>50%): shaft must be re-ground or probe relocated

5. INSTALLATION MOUNTING:
   - Rigid mounting essential—vibration of probe itself creates error
   - Probe holder: threaded mount with locknut, or clamp-style
   - Mounting surface: bearing housing or separate bracket (not flexible piping)
   - Orientation: perpendicular to shaft surface (not angled)
   - XY probe pair: 90° apart, typically horizontal and vertical or 45° orientation

6. RADIAL PROBE POSITIONING:
   - Install probes near bearing locations (close to support)
   - Avoid probe placement at nodal points for critical speed mode shapes
   - Clearance verification: shaft must not contact probe at maximum eccentricity
   - Minimum edge distance: 1.5× probe diameter from shaft end or keyway

7. AXIAL PROBE INSTALLATION (THRUST POSITION):
   - Measures shaft axial position (thrust bearing wear, thermal growth)
   - Mounted on thrust bearing housing, viewing collar or shoulder
   - Gap voltage: -9 to -11 VDC (allows for thermal expansion in both directions)
   - Alarm setpoints: ±10-20 mil (±0.25-0.5mm) from normal operating position

8. CABLE CONSIDERATIONS:
   - Extension cable: low-capacitance coaxial cable (matches proximitor system)
   - Maximum cable length: typically 6 meters (20 feet) from proximitor to probe
   - Cable routing: avoid running parallel to power cables (EMI/RFI interference)
   - Connector inspection: corrosion or moisture creates intermittent signals

9. CALIBRATION VERIFICATION:
   - Use calibration fixture with precision micrometer adjustment
   - Verify probe sensitivity (mV/mil or mV/μm) matches manufacturer specification
   - Check linearity over full operating range
   - Proximitor output verification: -2V to -18V corresponds to full range
   - Re-calibrate annually or after any probe replacement

10. API 670 REQUIREMENTS:
    - Dual probe redundancy for critical machines (2 probes per bearing, XY pairs)
    - Alarm setpoint: typically 50-70% of trip setpoint
    - Trip setpoint: 75% of bearing clearance (API 610) or machine-specific analysis
    - OK status: vibration <25% of trip
    - Alert status: 25-50% of trip
    - Danger status: 50-75% of trip
    - Trip: >75% of trip setpoint → automatic shutdown
""",
        key_factors=[
            "Gap voltage must be set to mid-range (-8 to -10 VDC) for linear operation",
            "Electrical runout from shaft surface imperfections must be measured and compensated",
            "Probe target area requires 3× probe diameter of non-magnetic, smooth surface",
            "Rigid mounting essential—probe vibration creates measurement error",
            "XY probe pairs at 90° reveal shaft orbit and vibration direction",
            "API 670 requires dual redundancy and alarm/trip setpoints for critical machines"
        ],
        primary_authority=[
            "API 670 (Machinery protection systems)",
            "ISO 7919 (Shaft vibration evaluation)",
            "Bently Nevada System 1 Installation Manual"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.MAINTENANCE,
        counter_arguments=[
            "Proximity probes only measure relative displacement—cannot detect rigid-body motion of entire rotor-bearing system",
            "Shaft coatings (chrome, Inconel) alter probe sensitivity—requires specific calibration",
            "Electrical runout compensation assumes runout is stationary—thermal distortion invalidates stored vector",
            "High-frequency bandwidth limited by cable length and capacitance"
        ],
        measurement_considerations=[
            "Verify target area surface finish <32 μin RMS for accurate measurements",
            "Document initial gap voltage and electrical runout vector for future comparison",
            "Check cable shield grounding—improper grounding causes 60 Hz interference",
            "Thermal growth can change gap voltage—monitor during startup"
        ]
    ),

    DoctrineBlock(
        topic="accelerometer_selection_mounting",
        keywords=["accelerometer", "piezoelectric", "IEPE", "ICP", "mounting", "stud", "magnet", "frequency response"],
        conclusion_template=[
            "Accelerometer selection depends on frequency range (piezo for >1 kHz, MEMS for low-frequency), amplitude range, and mounting method",
            "Stud mounting provides highest frequency response (~10 kHz); magnetic mount limited to ~2 kHz; probe/handheld <1 kHz",
            "IEPE/ICP accelerometers require constant-current power supply; check for sensor open/short circuit before measurements"
        ],
        reasoning_framework="""
ACCELEROMETER SELECTION AND MOUNTING FRAMEWORK:
1. ACCELEROMETER TYPES:
   Piezoelectric (Quartz or Ceramic):
     - Frequency range: 0.5 Hz to 10-50 kHz (depending on mounting)
     - Sensitivity: 10-100 mV/g typical
     - High-temperature capable (up to 650°C for quartz)
     - Charge output (requires charge amplifier) or IEPE (Integrated Electronics)

   IEPE/ICP (Integrated Circuit Piezoelectric):
     - Built-in amplifier, constant-current powered (2-20 mA, typically 4 mA)
     - Low-impedance output, long cable runs possible (100+ feet)
     - Temperature limited (~125°C typical)
     - Most common for industrial vibration monitoring

   MEMS (Micro-Electro-Mechanical Systems):
     - DC response (true 0 Hz to several kHz)
     - Measures static acceleration and dynamic vibration
     - Lower cost, smaller size
     - Limited to ~200°C, lower sensitivity than piezoelectric

2. FREQUENCY RESPONSE CONSIDERATIONS:
   - Mounted resonance frequency: accelerometer resonates when stud-mounted
   - Usable frequency range: up to 1/3 of mounted resonance
   - Example: 30 kHz resonance → usable to 10 kHz
   - Smaller, lighter accelerometer → higher resonance frequency
   - Heavier accelerometer mass-loads structure → lowers measured natural frequency

3. AMPLITUDE RANGE:
   - Low-sensitivity (10 mV/g): high-amplitude measurements (0.1 to 500 g)
   - Medium-sensitivity (100 mV/g): general-purpose (0.01 to 50 g)
   - High-sensitivity (500-1000 mV/g): low-amplitude precision (0.001 to 10 g)
   - Overload protection: most accelerometers survive 5000-10000 g shock

4. MOUNTING METHODS (best to worst frequency response):

   A. STUD MOUNTING (BEST):
     - Drilled/tapped hole in machine surface (10-32 or M5 thread typical)
     - Thin layer of grease or oil on mating surface (no air gap)
     - Torque to specification (typically 18-30 in-lb / 2-3.5 N-m)
     - Frequency response: DC to 10 kHz+
     - Most rigid coupling, highest resonance frequency
     - Permanent installation for continuous monitoring

   B. ADHESIVE MOUNTING:
     - Cyanoacrylate (super glue) or epoxy bond
     - Surface preparation: clean, degrease, roughen with sandpaper
     - Frequency response: DC to ~7 kHz
     - Semi-permanent, easier removal than stud
     - Good for temporary or trial measurements

   C. MAGNETIC MOUNTING:
     - Rare-earth magnet base, quick attachment
     - Flat, smooth, ferrous surface required
     - Frequency response: 10 Hz to 2 kHz
     - Mounting resonance ~2-3 kHz limits high-frequency accuracy
     - Convenient for route-based monitoring
     - Pull force >30 lbs (>130 N) for secure attachment

   D. PROBE/HANDHELD:
     - Spring-loaded tip or hand pressure
     - Frequency response: 10 Hz to 1 kHz (highly dependent on pressure)
     - Suitable for quick surveys, not precision measurements
     - Operator technique creates variability

5. MOUNTING SURFACE PREPARATION:
   - Flat surface (flatness <0.001" / 25 μm)
   - Smooth finish (surface roughness <63 μin / 1.6 μm)
   - Clean: remove paint, rust, oil (except thin oil film for stud mounting)
   - Ferrous metal preferred for magnetic mounting
   - Avoid flexible panels or thin sheet metal (local resonance)

6. MOUNTING LOCATION SELECTION:
   - Near bearing housing, on solid structure
   - Avoid piping, thin covers, bolt heads (local resonances)
   - Measure in three axes: radial horizontal, radial vertical, axial
   - Same location for trending (mark with paint or engraved ID number)
   - Avoid nodal points for modes of interest

7. CABLE CONSIDERATIONS:
   - Low-noise coaxial cable for IEPE accelerometers
   - Secure cable to prevent whipping (cable whip creates noise)
   - Strain relief near connector (avoid bending stresses)
   - Cable loop secured to machine (not hanging free)
   - Maximum cable length: 1000 feet (300m) for IEPE with proper cable

8. ELECTRICAL CHECKS (IEPE/ICP):
   - Open circuit (broken sensor or cable): voltage output ~24V (supply voltage)
   - Short circuit (damaged sensor): voltage output ~0V
   - Normal operation: voltage output 8-12V DC bias + AC signal
   - Bias voltage check before measurement verifies sensor integrity
   - Ground loop check: measure isolation between sensor case and ground

9. ENVIRONMENTAL CONSIDERATIONS:
   - Temperature: verify accelerometer rated for ambient temperature
   - Moisture: sealed (IP67) accelerometers for wet environments
   - Explosion hazard: intrinsically safe (IS) accelerometers for Class I Div 1
   - EMI/RFI: shielded cable, avoid routing near VFDs or welders

10. CALIBRATION:
    - Back-to-back calibration: compare test accelerometer against reference
    - Shaker table calibration: known acceleration input, measure output
    - Sensitivity typically stable (±5% over 10+ years for quartz)
    - Drop test: verify accelerometer functional (should show sharp impact)
    - Calibration frequency: annual or per ISO 10816-1 requirements
""",
        key_factors=[
            "Mounting method determines usable frequency range: stud (10 kHz), magnet (2 kHz), probe (1 kHz)",
            "IEPE accelerometers require constant-current supply; check bias voltage before measurement",
            "Accelerometer mass loading affects measured resonance—use lightweight sensor for high frequencies",
            "Mounting surface must be flat, smooth, and rigid to achieve specified frequency response",
            "Route-based measurements require consistent mounting location for valid trending",
            "Higher sensitivity (mV/g) provides better resolution for low-amplitude vibration"
        ],
        primary_authority=[
            "ISO 5348 (Mechanical mounting of accelerometers)",
            "ISO 16063-1 (Vibration calibration by comparison)",
            "PCB Piezotronics installation guidelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.MAINTENANCE,
        counter_arguments=[
            "Stud mounting not always practical—requires machine modification",
            "Magnetic mounting adequate for <1 kHz measurements (covers most industrial machinery)",
            "High-sensitivity accelerometers saturate on high-vibration machines",
            "Cable whip noise can overwhelm low-amplitude signals—secure cabling critical"
        ],
        measurement_considerations=[
            "Verify bias voltage (8-12 VDC) before trusting measurement data",
            "Use same accelerometer and location for trending—changing sensors invalidates comparison",
            "Document mounting method and location in measurement report",
            "Test accelerometer on known-good machine to verify functionality"
        ]
    ),

    DoctrineBlock(
        topic="oil_whirl_whip_instability",
        keywords=["oil whirl", "oil whip", "subsynchronous", "0.42X 0.43X 0.47X", "journal bearing", "instability"],
        conclusion_template=[
            "Oil whirl occurs at ~0.42-0.48X shaft speed, caused by fluid-film instability in lightly-loaded journal bearings",
            "Oil whip is violent resonance when whirl frequency coincides with rotor critical speed, requires immediate shutdown",
            "Increasing bearing preload, reducing clearance, or adding external damping can suppress instability"
        ],
        reasoning_framework="""
OIL WHIRL AND WHIP INSTABILITY FRAMEWORK:
1. JOURNAL BEARING FLUID-FILM MECHANICS:
   - Hydrodynamic pressure wedge supports rotor
   - Oil film has tangential velocity ~50% of shaft surface speed
   - Lightly loaded bearings: rotor eccentricity low, film uniformity high
   - Oil film acts as spring-damper system with cross-coupling stiffness

2. OIL WHIRL MECHANISM:
   - Rotor centerline orbits at subsynchronous frequency
   - Whirl frequency ≈ 0.42-0.48× shaft speed (typically 0.43-0.47X)
   - Caused by: tangential drag from oil film exceeds radial stiffness
   - Average oil velocity ≈ 0.5× shaft surface velocity → whirl at ~0.5X
   - Forward whirl (same direction as rotation)

3. OIL WHIRL ONSET CONDITIONS:
   - Light bearing load (W/Ld² < 10 psi, where W=load, L=length, d=diameter)
   - Low viscosity oil or high temperature (thins oil film)
   - Excessive bearing clearance (loose fit, wear)
   - High length-to-diameter ratio bearing (L/D > 1.0)
   - Smooth journal surface (low surface roughness)

4. OIL WHIP TRANSITION:
   - As shaft speed increases, whirl frequency increases (~0.47X)
   - When whirl frequency reaches rotor 1st critical speed → OIL WHIP
   - Whip locks onto critical speed, no longer tracks 0.47X
   - Amplitude increases rapidly and catastrophically
   - Example: 1st critical = 2800 CPM, whip onset at ~6000 RPM (2800/0.47)

5. DIAGNOSTIC SIGNATURES:
   Oil Whirl:
     - Subsynchronous peak at 0.42-0.48X shaft speed
     - Whirl frequency increases linearly with shaft speed
     - Moderate amplitude, often 1-3 mils pk-pk (25-75 μm)
     - Orbit analysis: stable forward whirl, elliptical or circular
     - Waterfall plot: diagonal line from origin with slope ~0.45

   Oil Whip:
     - Subsynchronous peak locks onto critical speed frequency
     - Amplitude increases dramatically (5-20+ mils, 125-500+ μm)
     - Whip frequency constant despite speed changes
     - Orbit becomes large, erratic, unstable
     - Waterfall plot: diagonal line becomes horizontal at critical frequency

6. DIFFERENTIATION FROM OTHER SUBSYNCHRONOUS VIBRATION:
   - Looseness: subsynchronous at 0.5X, 1.5X, etc., often whole and half-orders
   - Rub: subsynchronous at fractions (1/2X, 1/3X), reverse whirl possible
   - Misalignment: typically 2X, 3X (super-synchronous), not subsynchronous
   - Mechanical resonance: subsynchronous but constant frequency (doesn't track speed)

7. MITIGATION STRATEGIES:
   Increase Bearing Preload:
     - Offset-halves bearing: upper half bored smaller diameter (creates preload)
     - Lemon-bore bearing: elliptical bore shape
     - Pressure dam bearing: adds local high-pressure zone
     - Target: increase W/Ld² to >20 psi

   Reduce Bearing Clearance:
     - Tighter clearance reduces average oil velocity
     - Typical clearance: 0.001-0.002" per inch of journal diameter
     - Caution: too tight causes heat generation and seizure

   Increase External Damping:
     - Squeeze-film damper: secondary oil film around bearing housing
     - Elastomeric mounts: external damping in parallel with bearing

   Change Oil Viscosity:
     - Higher viscosity increases film stiffness (but also increases power loss)
     - Temperature control: cooler oil = higher viscosity

   Bearing Design Modification:
     - Tilting-pad bearing: inherently stable (each pad self-aligns)
     - Multi-lobe bearing: 3-lobe or 4-lobe design (higher stiffness)
     - Reduce L/D ratio: shorter bearing length relative to diameter

8. OPERATIONAL RESPONSE:
   Oil Whirl Detected:
     - Monitor amplitude trend—may stabilize at acceptable level
     - Reduce speed if amplitude increasing
     - Increase bearing load if possible (change process parameters)

   Oil Whip Detected:
     - IMMEDIATE SHUTDOWN required
     - Do not attempt to accelerate through whip condition
     - Bearing modification necessary before return to service

9. ACCEPTANCE CRITERIA:
   - Oil whirl amplitude <25% of bearing clearance: typically acceptable
   - Oil whirl amplitude >50% of bearing clearance: modification required
   - Any oil whip indication: unacceptable, design change mandatory
   - API 617 limit: subsynchronous vibration <50% of synchronous vibration
""",
        key_factors=[
            "Oil whirl occurs at 0.42-0.48X shaft speed, increases linearly with speed",
            "Oil whip locks onto critical speed frequency, amplitude increases catastrophically",
            "Lightly loaded bearings most susceptible (W/Ld² < 10 psi)",
            "Tilting-pad bearings inherently stable, eliminate oil whirl",
            "Waterfall plot slope ~0.45 diagnostic for oil whirl; horizontal line = whip",
            "Whip onset speed = critical speed / 0.47 (approximately)"
        ],
        primary_authority=[
            "API 684 (Rotor dynamics tutorial—Chapter on fluid-film bearing instabilities)",
            "API 617 (Axial and centrifugal compressors)",
            "Muszynska, A. 'Rotordynamics' (instability theory)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.DIAGNOSTIC,
        fault_type=FaultType.OIL_WHIRL,
        counter_arguments=[
            "Some subsynchronous vibration may result from structural resonance, not bearing instability",
            "Rub can create similar subsynchronous signature but typically includes reverse whirl component",
            "Magnetic bearing systems exhibit different instability mechanisms (not oil whirl)",
            "Variable-speed machines complicate whirl/whip distinction due to continuous speed changes"
        ],
        measurement_considerations=[
            "Shaft displacement (proximity probes) essential—bearing housing measurement misses shaft motion",
            "Orbit plots reveal whirl direction (forward = instability, reverse = rub)",
            "Waterfall plot during coast-down clearly shows whirl-to-whip transition",
            "Measure bearing temperature—instability often accompanied by temperature rise"
        ]
    ),

    DoctrineBlock(
        topic="fft_spectrum_analysis",
        keywords=["FFT", "spectrum", "frequency domain", "resolution", "hanning", "windowing", "leakage"],
        conclusion_template=[
            "FFT (Fast Fourier Transform) converts time waveform to frequency spectrum, revealing fault frequencies",
            "Frequency resolution = sample rate / number of lines; higher resolution requires longer time record",
            "Windowing (Hanning, Flattop) reduces spectral leakage but trades off frequency resolution"
        ],
        reasoning_framework="""
FFT SPECTRUM ANALYSIS FRAMEWORK:
1. FOURIER TRANSFORM FUNDAMENTALS:
   - Time domain → frequency domain transformation
   - Any periodic signal = sum of sinusoids at different frequencies
   - FFT: computationally efficient algorithm (N×log₂N vs. N² operations)
   - Result: amplitude vs. frequency plot (spectrum)

2. SAMPLING PARAMETERS:
   Sample Rate (f_s): samples per second (Hz)
     - Nyquist theorem: f_s ≥ 2× highest frequency of interest
     - Anti-aliasing filter: low-pass filter at 0.4-0.5× f_s
     - Typical: 2.56× maximum analysis frequency
     - Example: 1000 Hz F_max → 2560 Hz sample rate

   Number of Lines (N): frequency resolution
     - 400, 800, 1600, 3200, 6400 lines common
     - Frequency resolution Δf = f_s / (2N)
     - Example: 2560 Hz sample rate, 800 lines → 1.6 Hz resolution
     - Higher N = better resolution but longer acquisition time

   Time Record Length: T = N / f_s
     - Example: 800 lines, 2560 Hz → 0.3125 seconds
     - Longer time = better low-frequency resolution
     - Shorter time = faster updates for transient capture

3. WINDOWING FUNCTIONS:
   Uniform (Rectangular):
     - No windowing, assumes signal repeats perfectly in time record
     - Spectral leakage if signal not periodic in window
     - Use: transient signals, impacts, synchronized averaging

   Hanning:
     - Smooth taper to zero at edges, reduces leakage
     - Amplitude accuracy: ±1.5 dB
     - Frequency accuracy: excellent
     - Use: general-purpose, continuous signals

   Flattop:
     - Flat passband, excellent amplitude accuracy (±0.1 dB)
     - Poor frequency resolution (wide peak)
     - Use: calibration, amplitude measurements

   Exponential:
     - Emphasizes beginning of time record
     - Use: impact testing, decay measurements

4. SPECTRAL LEAKAGE:
   - Non-integer number of cycles in time window → energy spreads to adjacent bins
   - Appears as "skirts" around peaks, elevated noise floor
   - Windowing reduces leakage but slightly widens peaks
   - Synchronous sampling (trigger from tachometer) eliminates leakage for rotating machinery

5. AVERAGING METHODS:
   Linear Averaging:
     - Average of multiple spectra: reduces random noise
     - Number of averages: 4-16 typical, √N improvement in SNR
     - Stable, continuous signals

   Peak Hold:
     - Retains maximum value at each frequency bin
     - Captures transient events in continuous monitoring
     - Use: variable-speed machines, intermittent faults

   Exponential Averaging:
     - Weighted average favoring recent data
     - Time constant determines memory
     - Use: real-time displays, trending

6. FREQUENCY SPAN SELECTION:
   - F_max determines what frequencies are visible
   - 0-1000 Hz: general machinery (unbalance, misalignment, bearing faults)
   - 0-10 kHz: gear mesh frequencies, bearing defects
   - 0-40 kHz: ultrasonic, envelope analysis
   - Zoom FFT: high-resolution analysis of narrow frequency band

7. AMPLITUDE UNITS:
   Displacement: mils pk-pk or μm pk-pk (low frequency, <1000 Hz)
   Velocity: in/s pk or mm/s RMS (general machinery, 10-1000 Hz)
   Acceleration: g pk or m/s² RMS (high frequency, >1000 Hz)

   Conversions (for sinusoid at frequency f):
     Velocity = 2πf × Displacement
     Acceleration = 2πf × Velocity = (2πf)² × Displacement

8. SPECTRUM INTERPRETATION:
   Discrete Peaks:
     - Specific fault frequencies (1X, 2X, GMF, BPFO, etc.)
     - Narrow peaks = stable sources
     - Amplitude proportional to severity

   Harmonics:
     - Integer multiples of fundamental (2X, 3X, 4X...)
     - Indicate non-linearity or repetitive impacts
     - Many harmonics = looseness, misalignment, electrical faults

   Sidebands:
     - Peaks spaced around carrier frequency
     - Indicate modulation (amplitude or frequency)
     - Spacing = modulation frequency (identifies source)

   Broadband Noise:
     - Elevated across wide frequency range
     - Indicates wear, cavitation, turbulence, looseness
     - Rising noise floor = progressive fault (bearings, gears)

   Sub-synchronous:
     - Below 1X running speed
     - Oil whirl (0.42-0.48X), rub, looseness

   Super-synchronous:
     - Above 1X: harmonics, gear mesh, blade pass

9. ADVANCED TECHNIQUES:
   Order Tracking:
     - Spectrum in orders (multiples of running speed) not Hz
     - Compensates for speed variations
     - Essential for variable-speed machines

   Cepstrum:
     - FFT of log(FFT) → reveals periodicity in spectrum
     - Family of sidebands appears as single peak
     - Use: gear fault diagnosis (sideband family detection)

   Envelope Analysis:
     - High-pass filter, rectify, FFT
     - Reveals bearing defect frequencies hidden in raw spectrum
     - 100-1000× more sensitive than raw FFT for bearing faults
""",
        key_factors=[
            "Frequency resolution Δf = sample rate / (2 × number of lines)",
            "Hanning window reduces spectral leakage, best for continuous signals",
            "Synchronous sampling (tacho trigger) eliminates leakage for rotating machinery",
            "Averaging improves SNR by factor of √N (N = number of averages)",
            "Velocity (mm/s RMS) standard for ISO 10816 severity evaluation",
            "Narrow peaks indicate stable sources; broad peaks suggest instability or modulation"
        ],
        primary_authority=[
            "ISO 10816 (Vibration evaluation—velocity-based)",
            "ISO 7919 (Vibration evaluation—displacement-based)",
            "Bruel & Kjaer 'Vibration Analysis Handbook'"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.DIAGNOSTIC,
        counter_arguments=[
            "FFT assumes stationary signals—transients and impacts require time-frequency analysis (wavelet, STFT)",
            "High-resolution FFT requires long time record—misses rapid changes",
            "Windowing trades leakage reduction for frequency resolution—no perfect window",
            "Aliasing from inadequate sample rate creates false low-frequency peaks"
        ],
        measurement_considerations=[
            "Verify anti-aliasing filter engaged (typically 0.4-0.5× sample rate)",
            "Use synchronous sampling (tacho trigger) for rotating machinery when possible",
            "Document FFT parameters (lines, window, averaging) for repeatability",
            "Check for overload (clipping) in time waveform—invalidates FFT"
        ]
    ),

    DoctrineBlock(
        topic="time_waveform_analysis",
        keywords=["time waveform", "time domain", "crest factor", "kurtosis", "impacting", "clipping"],
        conclusion_template=[
            "Time waveform reveals transient events and impacts not visible in averaged frequency spectrum",
            "Crest factor (peak/RMS) >3 indicates impacting; kurtosis >3 indicates bearing defects",
            "Clipping or truncation in waveform indicates overload or looseness"
        ],
        reasoning_framework="""
TIME WAVEFORM ANALYSIS FRAMEWORK:
1. TIME DOMAIN vs. FREQUENCY DOMAIN:
   Time domain: amplitude vs. time (shows when events occur)
   Frequency domain (FFT): amplitude vs. frequency (shows what frequencies present)
   - Time waveform complements FFT, reveals detail FFT averages away

2. WAVEFORM CHARACTERISTICS:
   Sinusoidal (pure tone):
     - Smooth, repetitive sine wave
     - Indicates single dominant frequency (unbalance at 1X)
     - Crest factor = √2 ≈ 1.414 (for pure sinusoid)

   Complex periodic:
     - Repeating pattern, multiple frequency components
     - Misalignment (2X+3X), gear mesh (GMF + harmonics)
     - Crest factor 1.5-2.5 typical

   Impacting:
     - Sharp spikes, narrow pulses
     - Bearing defects, looseness, rubs
     - Crest factor >3, often >5
     - Kurtosis >3 (normal distribution = 3, impacting >>3)

   Random:
     - No repeating pattern, noise-like
     - Cavitation, turbulence, aerodynamic forces
     - Broadband spectrum, low crest factor

3. CREST FACTOR (CF):
   CF = Peak amplitude / RMS amplitude

   CF = 1.414: Pure sinusoid (healthy machine, single frequency)
   CF = 2-3: Multiple frequencies, typical machinery
   CF > 3: Impacting, bearing defects, looseness
   CF > 5: Severe impacting, advanced bearing damage
   CF < 1.3: Clipping (overload) or limiting

4. KURTOSIS (K):
   K = measure of "peakedness" of probability distribution
   Normal distribution: K = 3
   K < 3: Distributed energy, no sharp peaks
   K > 3: Concentrated energy in peaks (impacting)
   K > 5: Early bearing defect (impacts beginning)
   K > 10: Advanced bearing defect (severe impacts)

   Kurtosis more sensitive than RMS or crest factor for early bearing detection

5. CLIPPING AND TRUNCATION:
   Flat-topping (clipping):
     - Waveform flat at peaks (should be rounded)
     - Indicates: accelerometer overload, amplifier saturation, or looseness
     - Overload: increase accelerometer range or reduce sensitivity
     - Looseness: component hitting mechanical stop

   Truncation:
     - Waveform abruptly cut off (not smooth)
     - Indicates looseness, impacts, or clearance limiting

6. REPETITION RATE ANALYSIS:
   - Count peaks per revolution (requires tachometer)
   - Once per rev: unbalance, bent shaft, eccentric rotor
   - Twice per rev: misalignment, ovality, cocked bearing
   - Irregular: looseness, rub, bearing defect
   - Example: 6 impacts per rev with 8-ball bearing → outer race defect (BPFO = N_b/2 × (1-B_d/P_d·cosφ) ≈ 3.5-4X → ~6 visible peaks accounting for harmonics)

7. SYNCHRONOUS TIME AVERAGING:
   - Average waveform synchronized to shaft revolution
   - Repetitive events (unbalance, gear mesh) reinforce
   - Random noise and asynchronous events cancel
   - Result: clean waveform showing only shaft-synchronous components
   - Use: isolate specific shaft's contribution in multi-shaft gearbox

8. RESIDUAL WAVEFORM:
   - Original waveform minus synchronous average
   - Reveals non-synchronous events (bearing defects, random impacts)
   - Bearing defects not locked to shaft rotation appear clearly

9. ENVELOPE (DEMODULATED) TIME WAVEFORM:
   - High-pass filter (isolate bearing resonance band, 1-10 kHz)
   - Rectify (absolute value)
   - Low-pass filter (extract modulation envelope)
   - Result: bearing defect impacts appear as repetitive pulses
   - Count pulses per revolution → identify BPFO, BPFI, BSF, FTF

10. WAVEFORM PATTERN RECOGNITION:
    Unbalance: Smooth sinusoid at 1X, same amplitude each rev
    Misalignment: Double-hump per rev (2X component), varying amplitude
    Looseness: Erratic, truncated peaks, varying amplitude
    Bent shaft: Smooth but different amplitude across coupling (1X, 180° phase)
    Bearing outer race: Impacts spaced evenly, 3-5 per rev typical
    Bearing inner race: Impact spacing varies (modulated by cage rotation)
    Rub: Sudden amplitude change, often reverse whirl component
    Gear mesh: Teeth-meshing frequency visible as fine ripple on waveform
""",
        key_factors=[
            "Crest factor >3 indicates impacting; kurtosis >3 indicates bearing defect initiation",
            "Time waveform reveals transient events averaged away in FFT",
            "Clipping (flat-top waveform) indicates overload or looseness",
            "Synchronous time averaging isolates shaft-synchronous from non-synchronous events",
            "Repetition rate (impacts per revolution) identifies fault type and location",
            "Envelope time waveform 100X more sensitive than raw waveform for bearing defects"
        ],
        primary_authority=[
            "ISO 13373-1 (Condition monitoring vibration diagnostic training)",
            "ISO 29821-1 (Bearing vibration measurement methods)",
            "Mobius Institute Category II training (waveform analysis)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.DIAGNOSTIC,
        counter_arguments=[
            "Kurtosis sensitive to signal processing (filtering changes kurtosis value)",
            "Crest factor alone insufficient—must combine with spectrum and other indicators",
            "Synchronous averaging requires stable speed—variable-speed machines complicate technique",
            "Bearing defect impacts may be obscured by high 1X vibration—envelope analysis essential"
        ],
        measurement_considerations=[
            "Record at least 10 revolutions for pattern recognition",
            "Use tachometer/keyphasor for synchronous averaging",
            "Verify no accelerometer overload (clipping) before interpreting waveform",
            "Compare time waveform to FFT—both required for complete diagnosis"
        ]
    ),

    DoctrineBlock(
        topic="orbit_analysis_shaft_centerline",
        keywords=["orbit", "shaft centerline", "XY plot", "keyphasor", "preload", "precession"],
        conclusion_template=[
            "Orbit plot (XY plot) shows shaft vibration path within bearing clearance using dual proximity probes at 90°",
            "Forward precession (same direction as rotation) indicates unbalance/misalignment; reverse indicates rub",
            "Shaft centerline plot reveals average shaft position (preload direction and thermal growth)"
        ],
        reasoning_framework="""
ORBIT ANALYSIS FRAMEWORK:
1. ORBIT PLOT FUNDAMENTALS:
   - XY plot: X-probe (horizontal) vs. Y-probe (vertical) at 90°
   - Shows actual shaft motion path (trajectory) within bearing
   - Requires two proximity probes measuring radial displacement
   - Time information lost—only spatial path visible
   - Keyphasor adds timing reference (1 dot per revolution)

2. ORBIT CHARACTERISTICS:
   Shape:
     - Circular: single-frequency component (pure 1X unbalance)
     - Elliptical: two frequencies with different amplitudes
     - Figure-8: twice-per-rev component (2X from misalignment)
     - Banana: combination of 1X + 2X
     - Irregular: multiple frequencies or instability

   Size:
     - Small orbit (<25% bearing clearance): acceptable
     - Medium orbit (25-50% clearance): monitor
     - Large orbit (>50% clearance): corrective action required
     - Orbit touching clearance circle: severe, likely damage

   Precession Direction:
     - Forward (same as rotation): unbalance, misalignment, oil whirl
     - Reverse (opposite rotation): rub, looseness, crack
     - Mixed: complex fault, often rub during part of cycle

3. KEYPHASOR INTERPRETATION:
   - Keyphasor mark (dot) indicates shaft position at notch/key location
   - Single dot per revolution for 1X vibration (stationary in space)
   - Multiple dots indicate sub-synchronous or super-synchronous components
   - Dot position shows high spot location relative to keyphasor
   - Heavy spot 180° from high spot

4. UNBALANCE ORBIT:
   - Smooth ellipse or circle
   - Forward precession
   - Single keyphasor dot (1X vibration)
   - Orbit size increases with speed (∝ RPM²)
   - Major axis direction indicates flexibility/stiffness direction

5. MISALIGNMENT ORBIT:
   - Figure-8 or banana shape (1X + 2X components)
   - Forward precession overall
   - Two keyphasor dots 180° apart (2X component)
   - May show loop or crossing at center
   - Different across coupling (compare inboard/outboard orbits)

6. RUB ORBIT:
   - Irregular, erratic shape
   - Reverse precession during contact
   - Sudden direction change when rub occurs
   - Orbit may include sharp corners or flat sections
   - Sub-synchronous components create multiple keyphasor dots

7. OIL WHIRL ORBIT:
   - Large, smooth orbit
   - Forward precession at 0.42-0.48X shaft speed
   - Orbit grows as speed increases
   - May include small 1X component superimposed
   - Multiple keyphasor dots (non-integer frequency)

8. LOOSENESS ORBIT:
   - Erratic, changing shape
   - Non-repeatable from rev to rev
   - May show clipping (flat edges) indicating mechanical stops
   - Multiple keyphasor dots scattered randomly
   - Reverse precession segments possible

9. SHAFT CENTERLINE PLOT:
   - Plot of average shaft position vs. time or speed
   - Shows shaft movement during startup/shutdown
   - Reveals:
     * Bearing preload direction (shaft rests off-center when stopped)
     * Thermal growth (shaft moves as temperature rises)
     * Critical speed passage (shaft centerline shifts ~90° through critical)
     * Operating position stability

   Construction:
     - Take slow-roll vectors (shaft at 100-300 RPM)
     - Subtract slow-roll from operating speed measurements
     - Plot DC component (average position) vs. speed

10. FILTERED ORBITS:
    - Narrow-band filter around specific frequency (1X, 2X, etc.)
    - Isolates contribution of single frequency component
    - 1X orbit: pure unbalance response
    - 2X orbit: pure misalignment response
    - Compare filtered orbits to diagnose complex faults

11. FULL SPECTRUM (FFT OF ORBIT):
    - Apply FFT to orbit data (complex signal: X + jY)
    - Separates forward and reverse precession components
    - Positive frequencies: forward precession
    - Negative frequencies: reverse precession
    - Identifies subsynchronous instabilities clearly
""",
        key_factors=[
            "Forward precession (same as rotation) indicates forced response: unbalance, misalignment, oil whirl",
            "Reverse precession indicates self-excited instability: rub, crack, looseness",
            "Keyphasor dots indicate frequency content: 1 dot=1X, 2 dots=2X or 0.5X, many dots=subsynchronous",
            "Orbit size relative to bearing clearance quantifies severity",
            "Shaft centerline plot reveals thermal growth and preload direction",
            "Figure-8 or banana orbit diagnostic for 2X misalignment component"
        ],
        primary_authority=[
            "API 670 (Machinery protection systems—orbit analysis requirements)",
            "Bently Nevada Orbit Analysis training",
            "ISO 7919 (Shaft vibration evaluation)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.DIAGNOSTIC,
        counter_arguments=[
            "Orbit analysis requires dual probes at 90°—single probe insufficient for orbit",
            "2D orbit projects 3D shaft motion onto plane—axial motion not visible",
            "Electrical runout in probes distorts orbit shape—must compensate with slow-roll vector",
            "Complex orbits difficult to interpret—filtered orbits (1X-only, 2X-only) clarify"
        ],
        measurement_considerations=[
            "Verify probes at exactly 90° (or known angle) for accurate orbit shape",
            "Compensate electrical runout by subtracting slow-roll vectors",
            "Record orbits at multiple speeds during startup/shutdown for complete picture",
            "Compare orbits at both bearings—different shapes indicate local vs. global fault"
        ]
    ),

    DoctrineBlock(
        topic="electrical_motor_vibration",
        keywords=["motor", "electrical", "2X line frequency", "120 Hz", "rotor bar", "eccentric air gap", "slip frequency"],
        conclusion_template=[
            "Electrical motor faults produce vibration at 2× line frequency (120 Hz for 60 Hz power), slip frequency, and pole-pass frequency",
            "Broken rotor bars create sidebands around running speed spaced at 2× slip frequency",
            "Eccentric air gap produces 1× and 2× line frequency vibration; loose stator laminations produce 2× line frequency"
        ],
        reasoning_framework="""
ELECTRICAL MOTOR VIBRATION FRAMEWORK:
1. ELECTRICAL FREQUENCIES:
   Line Frequency (f_L): 50 Hz (Europe) or 60 Hz (North America)
   Synchronous Speed (N_s): N_s = 120 × f_L / P  (RPM, P = pole pairs)

   Examples:
     2-pole (3600/3000 RPM): N_s = 3600 RPM @ 60 Hz
     4-pole (1800/1500 RPM): N_s = 1800 RPM @ 60 Hz
     6-pole (1200/1000 RPM): N_s = 1200 RPM @ 60 Hz

   Slip: S = (N_s - N_actual) / N_s  (typically 1-5% full load)
   Slip Frequency (f_s): f_s = S × f_L

2. ELECTROMAGNETIC VIBRATION (HEALTHY MOTOR):
   2× Line Frequency:
     - 120 Hz (60 Hz power) or 100 Hz (50 Hz power)
     - Radial magnetic pull from stator field
     - Small amplitude (typically <0.1 in/s velocity)
     - Present in all motors—not necessarily a fault
     - Indicates: normal electromagnetic forces

   1× Line Frequency:
     - 60 Hz or 50 Hz
     - Usually much lower amplitude than 2× f_L
     - May indicate asymmetry (eccentric air gap, unequal windings)

3. BROKEN ROTOR BARS:
   Diagnostic Signature:
     - Sidebands around running speed (1X)
     - Sideband spacing: ±(2 × slip frequency)
     - Lower sideband: 1X - 2f_s
     - Upper sideband: 1X + 2f_s

   Physical Mechanism:
     - Broken bar reduces local current, creates magnetic asymmetry
     - Modulates rotor magnetic field at 2× slip frequency
     - Torque pulsation creates mechanical vibration

   Severity Assessment:
     - Sideband amplitude <-40 dB relative to 1X: likely healthy
     - Sideband amplitude -30 to -40 dB: monitor, possible defect
     - Sideband amplitude >-30 dB: significant defect, plan repair

   Confirmation:
     - Current signature analysis (MCSA): same sidebands in current spectrum
     - Load test: sidebands increase with load (slip increases)
     - Multiple broken bars: additional sideband families

4. ECCENTRIC AIR GAP:
   Types:
     - Static eccentricity: rotor centerline offset from bore centerline (constant offset)
     - Dynamic eccentricity: rotor centerline whirls (rotating high spot)

   Static Eccentricity:
     - 1× line frequency (60 Hz) vibration
     - Radial vibration, same amplitude at all positions around stator
     - Caused by: bent shaft, oval bore, bearing wear

   Dynamic Eccentricity:
     - Running speed (1X) sidebands around 2× line frequency
     - 2f_L ± 1X
     - Rotating magnetic force couples with shaft rotation
     - May also produce harmonics: 4f_L, 6f_L

   Combined Eccentricity:
     - Both 1× f_L and sidebands present
     - Most common in practice

5. LOOSE STATOR LAMINATIONS:
   Signature:
     - Dominant 2× line frequency (120 Hz or 100 Hz)
     - High amplitude (may exceed running speed component)
     - Buzzing/rattling audible noise
     - Harmonics at 4f_L, 6f_L also possible

   Cause:
     - Lamination stack loosened by thermal cycling
     - Inadequate clamping pressure or broken lamination welds

6. POLE-PASS FREQUENCY:
   Pole-Pass Frequency: f_pp = (Number of Poles) × (Running Speed / 60)

   Examples:
     - 4-pole motor at 1750 RPM: f_pp = 4 × 1750/60 = 116.7 Hz
     - 6-pole motor at 1165 RPM: f_pp = 6 × 1165/60 = 116.5 Hz

   Indicates:
     - Eccentric rotor or stator asymmetry
     - Non-uniform air gap
     - Usually low amplitude unless severe eccentricity

7. VARIABLE FREQUENCY DRIVE (VFD) EFFECTS:
   PWM Switching Frequency:
     - Carrier frequency typically 2-20 kHz
     - May excite structural resonances
     - Sidebands around switching frequency

   Harmonic Currents:
     - 5th, 7th, 11th, 13th harmonics of fundamental
     - Create additional vibration frequencies
     - Torque ripple at 6× fundamental (6f_L)

   Common-Mode Voltage:
     - Bearing currents from shaft voltage
     - Bearing damage (fluting, frosting) over time
     - Irregular broadband noise in spectrum

8. PHASE UNBALANCE:
   Single-Phase Operation:
     - One phase open (blown fuse, contactor failure)
     - High 2× line frequency vibration
     - Motor overheats rapidly
     - Loud humming noise

   Voltage Unbalance:
     - Unequal phase voltages
     - 2× line frequency increases
     - Negative sequence current creates reverse torque
     - 1% voltage unbalance → 6-10% current unbalance

9. DIFFERENTIATION FROM MECHANICAL FAULTS:
   Electrical faults:
     - Frequencies related to line frequency (60, 120, 180 Hz)
     - Constant frequency regardless of speed (VFD variable)
     - Sidebands at slip frequency (load-dependent)
     - Current signature confirms (MCSA)

   Mechanical faults:
     - Frequencies related to running speed (1X, 2X, etc.)
     - Frequency proportional to speed
     - Phase relationships different across coupling
     - No corresponding current signature
""",
        key_factors=[
            "2× line frequency (120 Hz @ 60 Hz power) indicates electromagnetic forces or loose laminations",
            "Sidebands at running speed ± 2× slip frequency indicate broken rotor bars",
            "1× line frequency suggests eccentric air gap or stator asymmetry",
            "VFD switching frequency (2-20 kHz) may excite structural resonances",
            "Motor current signature analysis (MCSA) confirms electrical faults",
            "Electrical fault frequencies constant; mechanical fault frequencies track speed"
        ],
        primary_authority=[
            "IEEE 1415 (Guide for induction machinery maintenance testing)",
            "NEMA MG-1 (Motors and generators standards)",
            "ISO 20958 (Condition monitoring using motor current signature analysis)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.DIAGNOSTIC,
        fault_type=FaultType.ELECTRICAL,
        counter_arguments=[
            "2× line frequency present in all motors—amplitude relative to 1X determines significance",
            "Broken rotor bar sidebands may be obscured by high 1X unbalance—trend over time",
            "VFD variable frequency complicates spectrum—order tracking relative to fundamental required",
            "Bearing currents from VFDs create broadband noise, difficult to separate from mechanical bearing faults"
        ],
        measurement_considerations=[
            "Measure vibration on motor frame near bearing locations (not feet—too flexible)",
            "Record motor nameplate data: rated speed, poles, full-load slip",
            "Calculate expected slip frequency and check for ±2f_s sidebands",
            "Perform motor current signature analysis (MCSA) to confirm electrical faults"
        ]
    )
]


# ============================================================================
# ENGINE CORE
# ============================================================================

class MECH07Engine:
    def __init__(self):
        self.version = "1.0.0"
        self.port = 9047
        self.start_time = datetime.now()
        self.query_count = 0
        self.doctrine_hits = defaultdict(int)
        self.response_times = []

        logger.info(f"MECH07 Vibration Analysis Engine v{self.version} initialized on port {self.port}")

    def _normalize_text(self, text: str) -> str:
        """Normalize text for semantic matching"""
        return text.lower().strip()

    def _match_doctrines(self, query: str, context: Optional[Dict] = None) -> List[DoctrineBlock]:
        """Match query to relevant doctrine blocks"""
        query_norm = self._normalize_text(query)
        matched = []

        for doctrine in DOCTRINE_CACHE:
            # Keyword matching
            keyword_score = sum(1 for kw in doctrine.keywords if kw in query_norm)

            # Context matching
            context_score = 0
            if context:
                if context.get("fault_type") == doctrine.fault_type:
                    context_score += 5
                if context.get("zone") == doctrine.zone:
                    context_score += 2

            total_score = keyword_score + context_score

            if total_score > 0:
                matched.append((total_score, doctrine))

        # Sort by score descending, take top matches
        matched.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in matched[:5]]  # Top 5 doctrines

    def _generate_response(self, query: str, mode: ResponseMode,
                          doctrines: List[DoctrineBlock],
                          zones: List[AnalysisZone]) -> Tuple[str, List[str], List[str], List[str]]:
        """Generate response based on mode and matched doctrines"""

        if not doctrines:
            return (
                "No specific vibration analysis doctrines matched your query. Please provide more details about the machinery type, observed vibration characteristics, or specific fault symptoms.",
                [],
                ["Provide FFT spectrum data", "Describe time waveform characteristics", "Specify machine type and operating speed"],
                []
            )

        # Combine reasoning from top doctrines
        primary = doctrines[0]

        if mode == ResponseMode.FAST:
            answer = "\n\n".join(primary.conclusion_template)
            recommendations = primary.key_factors[:3]

        elif mode == ResponseMode.DEFENSE:
            answer = f"{primary.reasoning_framework}\n\nKEY FACTORS:\n"
            answer += "\n".join(f"- {factor}" for factor in primary.key_factors)
            answer += f"\n\nAUTHORITY:\n"
            answer += "\n".join(f"- {auth}" for auth in primary.primary_authority)
            recommendations = [
                f"Verify {primary.key_factors[0]}",
                f"Cross-reference with {primary.primary_authority[0]}",
                "Document all measurement parameters for audit trail"
            ]

        else:  # MEMO
            answer = f"VIBRATION ANALYSIS MEMORANDUM\n\n"
            answer += f"TOPIC: {primary.topic.replace('_', ' ').title()}\n\n"
            answer += f"EXECUTIVE SUMMARY:\n{primary.conclusion_template[0]}\n\n"
            answer += f"TECHNICAL ANALYSIS:\n{primary.reasoning_framework}\n\n"
            answer += f"KEY DIAGNOSTIC FACTORS:\n"
            answer += "\n".join(f"{i+1}. {factor}" for i, factor in enumerate(primary.key_factors))
            answer += f"\n\nCOUNTERARGUMENTS AND ALTERNATIVE DIAGNOSES:\n"
            answer += "\n".join(f"- {arg}" for arg in primary.counter_arguments)
            answer += f"\n\nMEASUREMENT PROTOCOL:\n"
            answer += "\n".join(f"- {cons}" for cons in primary.measurement_considerations)
            answer += f"\n\nAUTHORITATIVE REFERENCES:\n"
            answer += "\n".join(f"- {auth}" for auth in primary.primary_authority)

            recommendations = primary.key_factors + primary.measurement_considerations

        # Extract fault indicators
        fault_indicators = []
        for d in doctrines:
            if d.fault_type:
                fault_indicators.append(d.fault_type.value)

        # Extract standards
        standards = []
        for d in doctrines:
            standards.extend(d.primary_authority)

        return answer, fault_indicators, recommendations, list(set(standards))

    def _calculate_confidence(self, doctrines: List[DoctrineBlock], query: str) -> ConfidenceLevel:
        """Calculate confidence level based on doctrine matches"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        primary = doctrines[0]

        # High confidence if multiple doctrines align
        if len(doctrines) >= 3:
            return ConfidenceLevel.DEFENSIBLE

        # Use primary doctrine's confidence
        return primary.confidence

    def process_query(self, request: VibrationQuery) -> VibrationResponse:
        """Main query processing with TIE-20 components"""
        start_time = datetime.now()
        self.query_count += 1

        # Match doctrines (three-layer approach: cache → semantic → deep)
        matched_doctrines = self._match_doctrines(request.query_text, request.context)

        # Log doctrine hits
        for d in matched_doctrines:
            self.doctrine_hits[d.topic] += 1

        # Generate response based on mode
        answer, fault_indicators, recommendations, standards = self._generate_response(
            request.query_text,
            request.mode,
            matched_doctrines,
            request.zones
        )

        # Calculate confidence
        confidence = self._calculate_confidence(matched_doctrines, request.query_text)

        # Determinism hash (SHA-256 of query + mode + doctrines)
        hash_input = f"{request.query_text}|{request.mode.value}|{','.join(d.topic for d in matched_doctrines)}"
        determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        # Telemetry
        elapsed = (datetime.now() - start_time).total_seconds()
        self.response_times.append(elapsed)

        telemetry = {
            "query_number": self.query_count,
            "elapsed_ms": int(elapsed * 1000),
            "doctrines_matched": len(matched_doctrines),
            "doctrine_topics": [d.topic for d in matched_doctrines],
            "avg_response_time_ms": int(sum(self.response_times) / len(self.response_times) * 1000)
        }

        logger.info(f"Query {self.query_count}: {len(matched_doctrines)} doctrines, {elapsed*1000:.1f}ms")

        return VibrationResponse(
            answer=answer,
            confidence=confidence,
            triggered_doctrines=[d.topic for d in matched_doctrines],
            analysis_zone=request.zones[0] if request.zones else AnalysisZone.DIAGNOSTIC,
            response_mode=request.mode,
            fault_indicators=list(set(fault_indicators)),
            recommendations=recommendations[:5],  # Top 5
            standards_referenced=list(set(standards))[:5],
            determinism_hash=determinism_hash,
            telemetry=telemetry
        )


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="MECH07 - Vibration Analysis & Diagnostics Engine",
    version="1.0.0",
    description="TIE Gold Standard vibration analysis engine for machinery diagnostics"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = MECH07Engine()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    uptime = (datetime.now() - engine.start_time).total_seconds()
    return HealthResponse(
        status="operational",
        version=engine.version,
        port=engine.port,
        doctrine_count=len(DOCTRINE_CACHE),
        cache_size=len(DOCTRINE_CACHE),
        uptime_seconds=uptime
    )


@app.post("/query", response_model=VibrationResponse)
async def query_endpoint(request: VibrationQuery):
    """Main query endpoint - vibration analysis"""
    try:
        return engine.process_query(request)
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "fault_type": d.fault_type.value if d.fault_type else None,
                "zone": d.zone.value,
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }


@app.get("/stats")
async def get_stats():
    """Engine statistics"""
    return {
        "total_queries": engine.query_count,
        "avg_response_time_ms": int(sum(engine.response_times) / len(engine.response_times) * 1000) if engine.response_times else 0,
        "uptime_seconds": (datetime.now() - engine.start_time).total_seconds(),
        "doctrine_hits": dict(engine.doctrine_hits),
        "top_doctrines": sorted(engine.doctrine_hits.items(), key=lambda x: x[1], reverse=True)[:10]
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting MECH07 Vibration Analysis Engine on port {engine.port}")
    uvicorn.run(app, host="0.0.0.0", port=engine.port)
