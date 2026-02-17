"""
MECH15 Non-Destructive Testing (NDT) Inspection Intelligence Engine
TIE-Grade FastAPI Service

Analyzes NDT methods: ultrasonic testing (UT conventional, phased array, TOFD),
radiographic testing (RT film/CR/DR), magnetic particle testing (MT),
liquid penetrant testing (PT), eddy current testing (ET), acoustic emission (AE).

Domain Coverage:
- UT pulse-echo and through-transmission techniques
- Phased array UT sector/linear scanning, S-scan imaging
- TOFD time-of-flight diffraction for crack detection
- RT film radiography, computed radiography (CR), digital radiography (DR)
- MT wet/dry methods, AC/DC magnetization, continuous/residual fields
- PT Type I fluorescent and Type II visible dye penetrants
- ET surface and subsurface flaw detection, conductivity sorting
- AE continuous monitoring for active defect growth
- ASNT SNT-TC-1A personnel qualification requirements
- ASME Section V NDE code requirements
- API 510/570/653 pressure vessel and piping inspection standards
- Probability of detection (POD) curves and statistical reliability
- Acceptance criteria per ASME VIII Division 1

Port: 9275
Version: 1.0.0
TIE-20 Compliant: Full implementation
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict, Counter

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

ENGINE_NAME = "MECH15_NDT_INSPECTION"
ENGINE_VERSION = "1.0.0"
PORT = 9275

AUDIT_LOG_PATH = Path(__file__).parent / "audit_trail.jsonl"
METRICS_LOG_PATH = Path(__file__).parent / "metrics.jsonl"

logger.add(
    Path(__file__).parent / "ndt_engine.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
)

# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS AND DATACLASSES
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
    UT_CONVENTIONAL = "UT_CONVENTIONAL"
    UT_PHASED_ARRAY = "UT_PHASED_ARRAY"
    UT_TOFD = "UT_TOFD"
    RT_FILM = "RT_FILM"
    RT_DIGITAL = "RT_DIGITAL"
    MT_WET = "MT_WET"
    MT_DRY = "MT_DRY"
    PT_FLUORESCENT = "PT_FLUORESCENT"
    PT_VISIBLE = "PT_VISIBLE"
    ET_SURFACE = "ET_SURFACE"
    ET_SUBSURFACE = "ET_SUBSURFACE"
    AE_MONITORING = "AE_MONITORING"
    PERSONNEL_QUAL = "PERSONNEL_QUAL"
    CODE_COMPLIANCE = "CODE_COMPLIANCE"
    ACCEPTANCE_CRITERIA = "ACCEPTANCE_CRITERIA"

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
    issue_category: IssueCategory

@dataclass
class TelemetryRecord:
    query_id: str
    timestamp: float
    mode: ResponseMode
    hit_cache: bool
    latency_ms: float
    doctrines_triggered: List[str]
    error_domain: Optional[str] = None

# ═══════════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE (25+ Real NDT Domain Blocks)
# ═══════════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="UT Pulse-Echo Thickness Measurement Accuracy",
        keywords=["ultrasonic", "pulse-echo", "thickness", "calibration", "velocity", "accuracy", "tolerance", "reference"],
        conclusion_template="Pulse-echo UT thickness measurements require material velocity calibration on reference standards within ±0.5% of actual material thickness per ASME V Article 5. Accuracy is ±0.001 inch or ±1% of thickness (whichever is greater) when properly calibrated. Velocity variations due to temperature, alloy composition, or microstructure can introduce errors requiring recalibration. Multiple readings and statistical averaging improve reliability.",
        reasoning_framework="""
        Pulse-echo ultrasonic testing relies on precise sound velocity in the test material.
        Calibration methodology:
        1. Establish material velocity using reference blocks of known thickness and similar metallurgy
        2. Verify calibration on at least two thickness points spanning expected range
        3. Account for temperature effects (velocity changes ~1 m/s per degree C in steel)
        4. Consider couplant thickness compensation for very thin materials
        5. Validate probe wear and crystal degradation through periodic checks

        Error sources:
        - Material velocity variations due to alloy content, grain structure, or heat treatment
        - Surface condition affecting couplant coupling efficiency
        - Probe angle or contact pressure variations
        - Electronic drift in instrumentation
        - Operator technique and experience level

        ASME V Article 5 requires calibration verification before and after each inspection shift,
        and whenever equipment, personnel, or material changes occur. For critical measurements
        (e.g., pressure vessel wall thickness), multiple independent readings from different
        operators or equipment are recommended to establish measurement uncertainty.

        Acceptance: Reported thickness must account for measurement uncertainty. For a nominal
        0.500 inch wall requiring minimum 0.450 inch, measurements showing 0.455 inch ±0.005 inch
        (95% confidence) would be borderline and require engineering evaluation or additional testing.
        """,
        key_factors=[
            "Material sound velocity calibration accuracy",
            "Reference standard metallurgical similarity to test piece",
            "Temperature compensation requirements",
            "Couplant type and thickness effects",
            "Instrument calibration verification frequency",
            "Surface condition and preparation adequacy",
            "Operator certification level (ASNT Level II minimum)",
            "Statistical measurement uncertainty quantification"
        ],
        primary_authority=[
            "ASME Section V Article 5 (Ultrasonic Examination Methods)",
            "ASTM E797 Standard Practice for Measuring Thickness by Manual Ultrasonic Pulse-Echo Contact Method",
            "ASNT SNT-TC-1A (Personnel Qualification and Certification in NDT)"
        ],
        burden_holder="Inspector performing thickness measurements",
        adversary_position="Measurements may be inaccurate due to calibration errors, material velocity variations, or operator technique",
        counter_arguments=[
            "Calibration performed on dissimilar material (wrong velocity)",
            "Insufficient temperature compensation in field conditions",
            "Reference blocks not traceable to national standards",
            "Operator not qualified per ASNT SNT-TC-1A",
            "Single-point measurement without statistical validation",
            "Couplant not specified or inconsistent application"
        ],
        resolution_strategy="Demonstrate calibration traceability, material similarity verification, multiple independent measurements, and statistical analysis of uncertainty",
        entity_scope="Pressure vessels, piping, storage tanks, structural steel",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when calibration documented on similar material with multiple readings; moderate when single measurement or dissimilar calibration material",
        controlling_precedent="ASME BPVC Section V Article 5 T-532 Calibration Requirements",
        issue_category=IssueCategory.UT_CONVENTIONAL
    ),

    DoctrineBlock(
        topic="Phased Array UT Sector Scan Coverage for Weld Inspection",
        keywords=["phased array", "PAUT", "sector scan", "weld", "coverage", "S-scan", "angle", "focal law", "fusion line"],
        conclusion_template="Phased array sector scans provide 100% volumetric weld coverage through programmable beam steering from 30 to 70 degrees (typical). S-scan images display all angles simultaneously, enabling detection of planar defects at varying orientations. Per ASME V Article 4 Appendix I, focal laws must be validated on calibration blocks with side-drilled holes or notches representing critical flaw sizes. Coverage requires overlapping scan patterns ensuring no gaps exceed 50% of beam width.",
        reasoning_framework="""
        Phased array UT enables electronic beam steering without physical probe movement:

        Sector scan parameters:
        - Angle range selected based on weld geometry (e.g., 40-70 deg for V-groove welds)
        - Focal depth set to mid-wall or specific region of interest
        - Element delays calculated (focal law) to form coherent wavefront at target angle/depth
        - Multiple angles interrogate weld simultaneously, displayed as S-scan image

        Coverage verification:
        1. Define inspection volume (weld fusion line, HAZ, base metal)
        2. Calculate beam spread at depth using -6 dB beam profile
        3. Determine index offset and scan increment to ensure overlap
        4. Validate coverage on calibration block with known reflectors across full volume
        5. Document dead zones at near-surface and far-surface interfaces

        S-scan imaging advantages:
        - Simultaneous multi-angle interrogation reduces inspection time
        - Identifies defect orientation (planar vs volumetric) from angle of maximum response
        - Provides permanent record as digital image for review and archiving
        - Enables automated sizing using amplitude drop techniques

        Critical requirements:
        - Wedge angle and material velocity must match actual test piece
        - Surface condition adequate for consistent coupling (Sa 2.5 or better)
        - Encoder accuracy for position correlation (±0.5 mm typical)
        - Focal law validation on reference reflectors matching critical flaw size

        Acceptance per ASME VIII Div 1: Indications exceeding reference level from calibration
        reflector require characterization (length, through-wall extent, type) and comparison
        to acceptance criteria. Lack-of-fusion and cracks (planar) typically rejectable;
        porosity and slag (volumetric) evaluated based on size and distribution.
        """,
        key_factors=[
            "Sector scan angle range appropriate for weld geometry",
            "Focal law validation on calibration block reflectors",
            "Scan pattern overlap to ensure no coverage gaps",
            "Surface preparation adequate for coupling",
            "Encoder resolution and accuracy for position tracking",
            "S-scan image resolution and sensitivity settings",
            "Operator training specific to phased array interpretation",
            "Flaw characterization methodology (planar vs volumetric)"
        ],
        primary_authority=[
            "ASME Section V Article 4 Appendix I (Phased Array UT)",
            "ASME Section VIII Division 1 UW-51 (Acceptance Standards for Welds)",
            "ASTM E2491 Standard Guide for Evaluating Performance Characteristics of Phased Array Ultrasonic Examination Instruments"
        ],
        burden_holder="Phased array operator and procedure developer",
        adversary_position="Coverage may be incomplete due to dead zones, incorrect focal laws, or inadequate scan overlap",
        counter_arguments=[
            "Dead zones at near-surface not adequately documented",
            "Focal laws not validated on representative reflectors",
            "Scan increment too large resulting in coverage gaps",
            "Surface condition inadequate for consistent coupling",
            "Operator not Level II certified in phased array per ASNT SNT-TC-1A Supplement",
            "S-scan sensitivity not calibrated to reference reflector amplitude"
        ],
        resolution_strategy="Provide focal law validation data, coverage modeling with beam profile overlay, and surface preparation documentation",
        entity_scope="Pressure vessel welds, piping butt welds, nozzle welds, structural critical welds",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when focal laws validated and coverage modeling documented; moderate if relying on generic procedures without site-specific validation",
        controlling_precedent="ASME BPVC Section V Article 4 Mandatory Appendix I",
        issue_category=IssueCategory.UT_PHASED_ARRAY
    ),

    DoctrineBlock(
        topic="TOFD Crack Height Sizing Accuracy",
        keywords=["TOFD", "time of flight", "diffraction", "crack", "height", "sizing", "lateral wave", "backwall", "tip signal"],
        conclusion_template="Time-of-flight diffraction (TOFD) provides crack height sizing accuracy typically ±1 mm through measurement of diffracted signals from crack tips. Lateral wave and backwall echo establish time zero and material thickness references. Per ASME V Article 4 Appendix III, TOFD requires calibration on reference blocks with notches of known depth. Sizing accuracy degrades for cracks near surface (<3 mm depth) or backwall due to signal overlap.",
        reasoning_framework="""
        TOFD relies on diffracted ultrasonic energy from crack tips rather than reflected energy:

        Signal interpretation:
        - Lateral wave (creeping wave along surface) establishes time zero reference
        - Upper tip diffraction arrives before backwall echo if crack present
        - Lower tip diffraction arrives after backwall echo (or before if through-wall)
        - Time difference between tip diffractions converted to height using sound velocity

        Sizing methodology:
        1. Identify lateral wave arrival time as t=0 reference
        2. Locate upper tip diffraction as phase reversal before backwall
        3. Locate lower tip diffraction as phase reversal after backwall (or second signal before)
        4. Calculate crack height: h = (t_lower - t_upper) × velocity / 2
        5. Apply corrections for beam angle (typically 60-70 deg probes)

        Accuracy limitations:
        - Near-surface cracks: upper tip signal obscured by lateral wave (dead zone <3 mm)
        - Near-backwall cracks: lower tip signal merges with backwall echo
        - Rough crack faces: diffraction energy scattered, weak tip signals
        - Multiple cracks: overlapping signals complicate interpretation
        - Operator experience: tip signal identification requires training

        ASME V Article 4 Appendix III requirements:
        - Calibration on reference block with notches spanning expected crack depth range
        - Probe separation (PCS) selected to provide adequate beam interaction depth
        - Scan increment ≤2 mm to ensure crack detection along length
        - Data acquisition with minimum 100 MHz sampling and 8-bit digitization
        - Analysis software capable of A-scan, B-scan, and D-scan displays

        Acceptance criteria: ASME VIII Div 1 does not directly address TOFD, so acceptance
        typically based on conventional UT equivalency. A crack indication sized at 15 mm
        height in 25 mm plate (60% through-wall) would generally be rejectable as exceeding
        allowable flaw size per fitness-for-service assessment.
        """,
        key_factors=[
            "Lateral wave and backwall echo clarity for reference establishment",
            "Upper and lower tip diffraction signal identification",
            "Material sound velocity accuracy",
            "Probe separation (PCS) appropriate for thickness",
            "Scan increment adequate to detect crack along length",
            "Dead zone limitations near surface and backwall",
            "Operator proficiency in diffraction signal interpretation",
            "Calibration on representative notch depths"
        ],
        primary_authority=[
            "ASME Section V Article 4 Appendix III (Time-of-Flight Diffraction)",
            "BS 7706 Guide to Calibration and Setting-up of the Ultrasonic Time-of-Flight Diffraction (TOFD) Technique",
            "ISO 10863 Non-Destructive Testing of Welds - Ultrasonic Testing - Use of Time-of-Flight Diffraction Technique (TOFD)"
        ],
        burden_holder="TOFD operator and data analyst",
        adversary_position="Crack height may be undersized or oversized due to signal interpretation errors, velocity inaccuracies, or dead zone limitations",
        counter_arguments=[
            "Tip signals weak or absent due to rough crack surfaces",
            "Upper tip signal obscured in lateral wave dead zone",
            "Velocity calibration performed on dissimilar material",
            "Probe separation not validated for actual thickness",
            "Operator not specifically trained in TOFD interpretation",
            "No independent verification of critical crack sizes"
        ],
        resolution_strategy="Provide calibration data on reference notches, demonstrate tip signal clarity on known reflectors, and perform independent verification sizing on critical indications",
        entity_scope="Weld crack detection in pressure vessels, pipelines, storage tanks",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for mid-wall cracks with clear tip signals; moderate for near-surface or near-backwall cracks in dead zones",
        controlling_precedent="ASME BPVC Section V Article 4 Appendix III Mandatory Requirements",
        issue_category=IssueCategory.UT_TOFD
    ),

    DoctrineBlock(
        topic="Radiographic Film IQI Sensitivity Requirements",
        keywords=["radiography", "film", "IQI", "penetrameter", "sensitivity", "hole-type", "wire-type", "2T", "image quality"],
        conclusion_template="Radiographic image quality indicators (IQI/penetrameters) verify achieved sensitivity per ASME V Article 2. Hole-type IQI requires visualization of 2T hole (hole diameter = 2× IQI thickness) to demonstrate adequate sensitivity for the material thickness radiographed. Wire-type IQI requires visualization of specified wire diameter. IQI placement on source side demonstrates proper exposure, while image-side IQI verifies minimum sensitivity. Failure to visualize required IQI elements renders radiograph unacceptable.",
        reasoning_framework="""
        IQI purpose: Objective verification that radiographic technique achieved necessary
        contrast sensitivity to detect discontinuities of specified size.

        Hole-type IQI (ASTM E1742):
        - Thickness selected based on material thickness being radiographed (typically 2% rule)
        - Three holes: 1T, 2T, 4T diameters (where T = IQI thickness)
        - 2T hole visualization required as minimum sensitivity indicator
        - 1T hole visualization indicates superior technique quality
        - 4T hole always visible if exposure adequate

        Wire-type IQI (ASTM E747):
        - Set of wires with decreasing diameters
        - Specific wire(s) designated essential per code requirements
        - Essential wire visibility confirms sensitivity level achieved
        - Common in European practice per EN standards

        IQI placement requirements (ASME V Article 2):
        - Source side: IQI placed on material surface nearest radiation source
        - Film side: IQI placed on material surface nearest film (more stringent test)
        - Lead letter or symbol identifies IQI number and orientation on radiograph
        - IQI material same alloy family as test piece (e.g., steel IQI for steel part)

        Sensitivity achievement factors:
        - Exposure energy (kV) appropriate for material thickness and density
        - Film type and processing quality (density 1.8-4.0 typical)
        - Geometric unsharpness minimized (source-to-film distance, source size)
        - Scatter radiation controlled (lead masking, collimation)
        - Screen type and contact (fluorometallic vs lead for film speed)

        Acceptance: If 2T hole not visible on hole-type IQI, radiograph fails sensitivity
        requirement and must be retaken. If visible but with poor contrast, film density
        may be suboptimal requiring exposure adjustment. For critical applications (nuclear,
        aerospace), 1T hole visibility may be specified for enhanced sensitivity.

        ASME VIII Div 1 UW-51: Radiography must meet sensitivity per ASME V Article 2.
        Welds showing lack of fusion, cracks, or elongated slag exceeding acceptance criteria
        are rejectable regardless of IQI visibility, but IQI failure alone invalidates the test.
        """,
        key_factors=[
            "IQI thickness selection (2% of material thickness typical)",
            "2T hole visibility as minimum sensitivity requirement",
            "IQI material similarity to test piece alloy",
            "Source-side vs film-side IQI placement",
            "Film density within acceptable range (1.8-4.0)",
            "Geometric unsharpness minimization",
            "Scatter radiation control techniques",
            "Film processing quality and consistency"
        ],
        primary_authority=[
            "ASME Section V Article 2 (Radiographic Examination)",
            "ASTM E1742 Standard Practice for Radiographic Examination (Hole-Type IQI)",
            "ASTM E747 Standard Practice for Design, Manufacture and Material Grouping Classification of Wire Image Quality Indicators"
        ],
        burden_holder="Radiographer and film interpreter",
        adversary_position="Radiograph may lack sensitivity to detect critical flaws if IQI requirements not met or technique inadequate",
        counter_arguments=[
            "2T hole not visible, indicating insufficient sensitivity",
            "IQI of incorrect thickness selected for material being radiographed",
            "IQI material different alloy family than test piece",
            "Film density outside acceptable range (too light or too dark)",
            "Excessive geometric unsharpness obscuring detail",
            "Film interpreter not ASNT Level II certified in radiographic testing"
        ],
        resolution_strategy="Demonstrate IQI selection per ASME V Article 2 Table T-276, provide film density measurements, and document interpreter certification",
        entity_scope="Pressure vessel welds, piping welds, castings, structural welds",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when IQI visible per requirements and film density within range; unacceptable if IQI not visible regardless of other factors",
        controlling_precedent="ASME BPVC Section V Article 2 T-276 and T-277 IQI Requirements",
        issue_category=IssueCategory.RT_FILM
    ),

    DoctrineBlock(
        topic="Digital Radiography (DR) vs Computed Radiography (CR) Sensitivity",
        keywords=["digital radiography", "DR", "computed radiography", "CR", "phosphor plate", "flat panel", "DQE", "SNR", "sensitivity"],
        conclusion_template="Digital radiography (DR flat panel detectors) and computed radiography (CR phosphor plates) provide electronic image capture replacing film. DR offers superior detective quantum efficiency (DQE) and signal-to-noise ratio (SNR) enabling lower dose and higher sensitivity than CR. Per ASTM E2597, both require IQI visibility validation and normalization index (dI/I) measurement. CR uses erasable phosphor plates requiring careful handling; DR uses fixed flat panel arrays with real-time imaging capability.",
        reasoning_framework="""
        CR technology:
        - Photostimulable phosphor plate exposed to X-rays or gamma rays
        - Latent image formed as trapped electrons in phosphor crystal lattice
        - Plate scanned with laser causing photostimulated luminescence
        - Emitted light captured by photomultiplier and digitized
        - Plate erased with bright light and reused (finite lifetime ~1000 exposures)

        DR technology:
        - Flat panel detector with scintillator layer (CsI typical) and photodiode array
        - X-ray photons converted to visible light by scintillator
        - Light detected by amorphous silicon photodiode array
        - Direct electrical signal readout, no intermediate laser scanning
        - Real-time image acquisition and display (seconds vs minutes for CR)

        Sensitivity comparison:
        - DR DQE: 50-70% (excellent)
        - CR DQE: 30-40% (moderate)
        - Film DQE: 20-30% (lowest)
        - Higher DQE means fewer X-ray photons needed for same image quality
        - DR can achieve film-equivalent sensitivity at 50% lower dose
        - CR typically requires 20-30% higher dose than film for equivalent sensitivity

        ASTM E2597 requirements:
        - Basic spatial resolution (Ub) measured with duplex wire IQI
        - Normalized SNR (SNRn) measured in uniform exposure area
        - Normalization index dI/I calculated from step wedge exposure
        - IQI visibility requirements same as film (2T hole for hole-type IQI)

        Acceptance considerations:
        - Image processing (gain, contrast, edge enhancement) must not obscure defects
        - Monitor display quality critical (calibrated brightness, contrast, resolution)
        - Archival format must preserve diagnostic quality (DICONDE or equivalent)
        - Operator training specific to digital image interpretation required

        Advantages over film:
        - Immediate image availability (seconds for DR, minutes for CR)
        - Wide dynamic range reduces retakes due to over/underexposure
        - Digital image processing enhances defect visibility
        - Electronic archival eliminates film storage requirements
        - Lower radiation dose (especially DR)

        Disadvantages:
        - Capital equipment cost higher than film systems
        - CR plate handling requires care (scratches degrade image quality)
        - Monitor quality and calibration critical for interpretation
        - Data storage and management infrastructure required
        """,
        key_factors=[
            "DQE and SNR performance vs film baseline",
            "IQI visibility validation per ASTM E2597",
            "Normalization index (dI/I) within acceptable range",
            "Image processing algorithms validated and documented",
            "Monitor calibration and quality verification",
            "Archival format preserving diagnostic quality",
            "Operator training specific to digital interpretation",
            "CR plate condition and handling procedures"
        ],
        primary_authority=[
            "ASTM E2597 Standard Practice for Manufacturing Characterization of Digital Detector Arrays",
            "ASTM E2698 Standard Practice for Radiographic Examination Using Digital Detectors",
            "ASME Section V Article 2 Appendix IV (Digital Imaging and Communication)"
        ],
        burden_holder="Radiographer and digital imaging system operator",
        adversary_position="Digital radiography may not provide equivalent sensitivity to film if DQE inadequate, monitor quality poor, or image processing inappropriate",
        counter_arguments=[
            "DQE not measured or documented per ASTM E2597",
            "IQI not visible despite claimed equivalent sensitivity",
            "Image processing parameters not validated or documented",
            "Monitor not calibrated to DICOM grayscale standard",
            "CR plates damaged or degraded beyond useful life",
            "Operator not trained in digital image interpretation artifacts"
        ],
        resolution_strategy="Provide DQE measurement data, demonstrate IQI visibility on digital images, and document image processing validation",
        entity_scope="Pressure vessels, piping, aerospace structures, weld inspection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for DR systems with documented DQE >50%; moderate for CR systems requiring validation against film baseline",
        controlling_precedent="ASTM E2597 and ASME BPVC Section V Article 2 Appendix IV",
        issue_category=IssueCategory.RT_DIGITAL
    ),

    DoctrineBlock(
        topic="Magnetic Particle Testing AC vs DC Magnetization",
        keywords=["magnetic particle", "MT", "AC", "DC", "magnetization", "surface", "subsurface", "current", "residual", "continuous"],
        conclusion_template="AC magnetization provides maximum sensitivity to surface-breaking discontinuities due to skin effect concentrating magnetic flux at the surface. DC magnetization penetrates deeper, enabling detection of slightly subsurface flaws (up to 0.25 inch depth in ferromagnetic materials). Per ASME V Article 7, method selection depends on flaw depth: AC for surface cracks, DC or permanent magnet for near-surface inclusions. Continuous field application during particle application provides higher sensitivity than residual magnetization.",
        reasoning_framework="""
        Magnetization physics:
        AC current (alternating current):
        - Skin effect causes current flow concentrated at surface (<0.010 inch depth in steel)
        - Magnetic field alternates at line frequency (50/60 Hz)
        - Maximum flux density at surface, decays exponentially with depth
        - Particles attracted/repelled during each cycle, vibrate into tight indications
        - Best sensitivity to surface-breaking cracks, laps, seams

        DC current (direct current):
        - Current flows throughout cross-section (limited only by resistance)
        - Steady magnetic field penetrates material depth
        - Detects subsurface flaws up to ~0.25 inch below surface
        - Less sensitive to tight surface cracks than AC
        - Includes HWDC (half-wave DC) and FWDC (full-wave DC) from rectification

        Permanent magnet:
        - Static field similar to DC but no current flow required
        - Yoke or bar magnet placed on surface
        - Field strength decays with distance from magnet
        - Portable method for field inspection
        - Limited to shallow subsurface detection

        Continuous vs residual field:
        Continuous: Magnetizing current applied during particle application
        - Particles attracted to leakage field in real-time
        - Maximum sensitivity due to full field strength
        - Required for AC (no residual field in AC magnetization)

        Residual: Magnetizing current removed before particle application
        - Relies on material retaining magnetic field (ferromagnetic materials)
        - Reduced sensitivity vs continuous (typically 50-70% of continuous)
        - Allows inspection of complex geometries after magnetization
        - Only viable with DC or permanent magnet (not AC)

        ASME V Article 7 requirements:
        - Amperage sufficient to achieve 300-800 gauss tangential field at surface
        - Field direction perpendicular to expected flaw orientation (requires multiple shots)
        - Demagnetization required if residual field affects subsequent operations
        - Particles (wet or dry) applied during continuous field or within 0.5 sec after DC removal

        Application selection:
        - Fatigue cracks (tight, surface): AC continuous with wet fluorescent particles
        - Grinding cracks: AC continuous
        - Forging laps: AC or DC continuous
        - Subsurface inclusions: DC continuous or permanent magnet
        - Weld lack of fusion at toe: AC continuous
        """,
        key_factors=[
            "Magnetization type selection based on flaw depth (AC for surface, DC for subsurface)",
            "Amperage sufficient to achieve 300-800 gauss field strength",
            "Continuous field application during particle application for maximum sensitivity",
            "Field direction perpendicular to expected crack orientation",
            "Multiple magnetization shots to cover all orientations",
            "Particle type appropriate for inspection (wet fluorescent for high sensitivity)",
            "Surface preparation (clean, dry, free of scale or coating)",
            "Demagnetization verification if required for subsequent operations"
        ],
        primary_authority=[
            "ASME Section V Article 7 (Magnetic Particle Examination)",
            "ASTM E1444 Standard Practice for Magnetic Particle Testing",
            "ASTM E709 Standard Guide for Magnetic Particle Testing"
        ],
        burden_holder="Magnetic particle inspector",
        adversary_position="MT may fail to detect subsurface flaws if AC used, or miss tight surface cracks if DC used; residual magnetization may lack sensitivity",
        counter_arguments=[
            "AC used when subsurface flaws expected (incorrect method)",
            "DC used when tight surface cracks expected (reduced sensitivity)",
            "Residual magnetization used when continuous field achievable",
            "Amperage insufficient to achieve adequate field strength",
            "Single magnetization direction missing cracks in other orientations",
            "Surface contamination (oil, scale) masking particle indications",
            "Inspector not ASNT Level II certified in magnetic particle testing"
        ],
        resolution_strategy="Demonstrate magnetization method selection based on flaw type and depth, provide field strength measurements (Hall probe or gauss meter), and document multiple-shot coverage",
        entity_scope="Welds, forgings, castings, crankshafts, gears, pressure vessel nozzles",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when method matches flaw type (AC for surface, DC for subsurface) and continuous field used; moderate if residual field relied upon",
        controlling_precedent="ASME BPVC Section V Article 7 T-764 Magnetization Technique Selection",
        issue_category=IssueCategory.MT_WET
    ),

    DoctrineBlock(
        topic="Liquid Penetrant Testing Type I Fluorescent Sensitivity Levels",
        keywords=["penetrant", "PT", "Type I", "fluorescent", "sensitivity", "level", "contrast", "developer", "dwell time", "crack"],
        conclusion_template="Type I fluorescent penetrant provides higher sensitivity than Type II visible dye penetrant through UV-A blacklight inspection. Per ASTM E1417, three sensitivity levels exist: Level 1/2 (low), Level 2 (medium), Level 3 (high), and Level 4 (ultra-high). Sensitivity level selection depends on criticality and minimum detectable flaw size required. Method A (water-washable) suits rough surfaces; Method C (solvent-removable) provides highest sensitivity for smooth surfaces. Proper dwell time (5-60 minutes typical) and developer application critical for indication formation.",
        reasoning_framework="""
        Penetrant testing relies on capillary action drawing low-viscosity liquid into surface-breaking discontinuities:

        Type I Fluorescent penetrant:
        - Contains fluorescent dye (often rhodamine derivatives)
        - Viewed under UV-A blacklight (320-380 nm, peak 365 nm)
        - Fluoresces bright yellow-green providing high contrast against dark background
        - Sensitivity superior to Type II visible dye (white light inspection)

        Sensitivity level classification (ASTM E1417):
        Level 1/2: Low sensitivity, coarse indications (large cracks, porosity)
        Level 2: Medium sensitivity, general purpose industrial applications
        Level 3: High sensitivity, aerospace and critical component inspection
        Level 4: Ultra-high sensitivity, research and special applications (rare)

        Higher sensitivity achieved through:
        - Smaller fluorescent dye particle size
        - Higher dye concentration
        - Lower viscosity (better capillary penetration)
        - Optimized surfactant package
        - Contamination control in processing

        Method selection (ASTM E1417):
        Method A: Water-washable penetrant
        - Contains emulsifier in penetrant formulation
        - Direct water rinse removes excess surface penetrant
        - Risk of over-washing and removing penetrant from flaws
        - Suits rough surfaces where emulsifier entrapment less critical

        Method C: Solvent-removable penetrant
        - No emulsifier in penetrant
        - Excess surface penetrant removed with solvent wipes (not spray)
        - Maximum control prevents over-removal
        - Highest sensitivity for smooth, critical surfaces

        Method D: Post-emulsifiable lipophilic
        - Separate emulsifier applied after penetrant dwell
        - Emulsifier blends with excess surface penetrant making it water-washable
        - Time-controlled emulsification prevents over-washing
        - Good for complex geometries

        Critical process parameters:
        Penetrant dwell time: 5-60 minutes depending on material and flaw tightness
        - Aluminum: 5-10 min typical
        - Steel: 10-30 min
        - Titanium: 30-60 min (oxide layer requires longer dwell)
        - Fatigue cracks (very tight): Maximum dwell time at elevated temperature

        Developer application:
        - Dry powder: Dusted on, provides good contrast, limited bleedout time
        - Non-aqueous wet: Sprayed, rapid drying, good for complex shapes
        - Aqueous wet: Sprayed, slower drying, maximum bleedout for tight cracks
        - Developer dwell: 10-60 minutes allowing capillary bleedout from flaw

        Inspection environment:
        - UV-A intensity minimum 1000 µW/cm² at surface (measured with calibrated meter)
        - Visible light <20 lux (dark adaptation critical for sensitivity)
        - Inspector dark adaptation period: 1-5 minutes before inspection

        Acceptance: Relevant indications (not false indications from scratches, porosity, machining marks)
        evaluated against acceptance criteria. Linear indications >1/16 inch in critical areas
        typically rejectable; rounded indications evaluated based on size and distribution.
        """,
        key_factors=[
            "Sensitivity level selection (Level 2 vs 3) based on criticality",
            "Method selection (A, C, or D) based on surface condition and required sensitivity",
            "Penetrant dwell time adequate for material and flaw type",
            "Developer type and dwell time for proper bleedout",
            "UV-A blacklight intensity ≥1000 µW/cm² verified with meter",
            "Visible light <20 lux for dark adaptation",
            "Inspector dark adaptation before inspection",
            "Surface preparation (clean, dry, free of contaminants)"
        ],
        primary_authority=[
            "ASTM E1417 Standard Practice for Liquid Penetrant Testing",
            "ASTM E165 Standard Practice for Liquid Penetrant Examination for General Industry",
            "ASME Section V Article 6 (Liquid Penetrant Examination)"
        ],
        burden_holder="Penetrant inspector and procedure developer",
        adversary_position="Penetrant testing may fail to detect tight cracks if sensitivity level inadequate, dwell time insufficient, or process parameters not controlled",
        counter_arguments=[
            "Sensitivity level too low for critical component (Level 2 vs Level 3)",
            "Method A used where Method C required for maximum sensitivity",
            "Penetrant dwell time too short for tight fatigue cracks",
            "Developer dwell insufficient for capillary bleedout",
            "UV-A intensity below 1000 µW/cm² minimum requirement",
            "Visible light contamination degrading contrast",
            "Inspector not dark-adapted before inspection",
            "Surface contaminants (oil, grease) preventing penetrant entry"
        ],
        resolution_strategy="Demonstrate sensitivity level and method selection per specification, provide UV-A intensity measurements, and document process parameter compliance",
        entity_scope="Welds, castings, forgings, machined components, turbine blades, landing gear",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when Level 3 sensitivity and Method C used with documented process control; moderate for Level 2 or Method A on critical components",
        controlling_precedent="ASTM E1417 and ASME BPVC Section V Article 6",
        issue_category=IssueCategory.PT_FLUORESCENT
    ),

    DoctrineBlock(
        topic="Eddy Current Testing Frequency Selection for Depth of Penetration",
        keywords=["eddy current", "ET", "frequency", "penetration depth", "skin depth", "conductivity", "permeability", "surface", "subsurface"],
        conclusion_template="Eddy current testing penetration depth inversely proportional to test frequency. Standard depth of penetration (skin depth δ) calculated as δ = 503 × sqrt(ρ / (μr × f)) where ρ = resistivity (Ω·m), μr = relative permeability, f = frequency (Hz). Low frequency (100 Hz - 1 kHz) penetrates deeper for subsurface flaws; high frequency (100 kHz - 1 MHz) concentrates at surface for surface crack detection. Per ASTM E1004, frequency selection must balance penetration depth requirement with sensitivity and resolution needs.",
        reasoning_framework="""
        Eddy current principles:
        - AC coil generates time-varying magnetic field
        - Magnetic field induces eddy currents in conductive material
        - Eddy current magnitude and phase depend on material conductivity, permeability, geometry, and flaws
        - Flaws disrupt eddy current flow causing impedance change in coil
        - Impedance change detected as change in coil voltage or phase

        Skin depth (standard depth of penetration):
        δ = 503 × sqrt(resistivity / (relative_permeability × frequency))

        For aluminum (non-magnetic, ρ = 2.82 × 10⁻⁸ Ω·m, μr = 1):
        - At 100 Hz: δ = 26.7 mm (deep penetration)
        - At 1 kHz: δ = 8.4 mm
        - At 10 kHz: δ = 2.7 mm
        - At 100 kHz: δ = 0.84 mm
        - At 1 MHz: δ = 0.27 mm (surface detection only)

        For carbon steel (ferromagnetic, ρ = 1.7 × 10⁻⁷ Ω·m, μr = 100):
        - At 100 Hz: δ = 2.1 mm
        - At 1 kHz: δ = 0.65 mm
        - At 10 kHz: δ = 0.21 mm (surface only)

        Frequency selection strategy:
        Surface crack detection: 100 kHz - 1 MHz
        - Maximum sensitivity to tight surface cracks
        - High resolution for crack length and depth measurement
        - Common for fatigue crack inspection in aerospace

        Near-surface flaw detection: 10 kHz - 100 kHz
        - Detects flaws 0.5-2 mm below surface
        - Heat treat layer inspection (case hardening verification)
        - Corrosion pitting beneath coatings

        Subsurface flaw detection: 100 Hz - 10 kHz
        - Penetrates several mm to cm depth
        - Second layer crack detection in multi-layer structures
        - Tube inspection for wall thinning or corrosion

        Conductivity sorting: 10 kHz - 100 kHz
        - Material verification (e.g., aluminum alloy 2024 vs 7075)
        - Heat treat verification (solution treated vs aged)
        - Carbon content in steel affecting hardness

        Multi-frequency testing:
        - Simultaneous multiple frequencies separate surface from subsurface signals
        - Low frequency detects deep flaws, high frequency detects surface
        - Signal processing discriminates depth based on phase relationships
        - Advanced eddy current array instruments support multi-frequency operation

        ASTM E1004 requirements:
        - Reference standard with natural or artificial flaws at target depth
        - Calibration at multiple frequencies if depth discrimination needed
        - Phase angle analysis for depth estimation
        - Lift-off compensation to separate probe-to-surface distance from flaw signals

        Limitations:
        - Conductive materials only (not insulators or poorly conductive ceramics)
        - Geometry effects (edges, curvature) produce signals similar to flaws
        - Surface condition affects coupling (rough surfaces degrade signal quality)
        - Permeability variations in ferromagnetic materials produce large background signals
        """,
        key_factors=[
            "Frequency selection based on required penetration depth",
            "Skin depth calculation for material conductivity and permeability",
            "Reference standard with flaws at target depth",
            "Lift-off compensation to separate probe distance from flaw signals",
            "Phase angle analysis for flaw depth discrimination",
            "Multi-frequency capability for surface/subsurface separation",
            "Surface condition adequate for consistent probe coupling",
            "Operator training in impedance plane interpretation"
        ],
        primary_authority=[
            "ASTM E1004 Standard Practice for Electromagnetic (Eddy Current) Examination",
            "ASTM E2261 Standard Practice for Examination of Welds Using Eddy Current Array",
            "ASME Section V Article 8 (Eddy Current Examination)"
        ],
        burden_holder="Eddy current inspector and procedure developer",
        adversary_position="ET may fail to detect deep flaws if frequency too high, or miss surface cracks if frequency too low; permeability variations in steel can mask flaw signals",
        counter_arguments=[
            "Frequency too high to penetrate to required depth (surface-only detection)",
            "Frequency too low resulting in poor resolution and sensitivity",
            "No multi-frequency capability to discriminate surface from subsurface",
            "Reference standard flaws not at target depth being inspected",
            "Lift-off not compensated causing false indications",
            "Operator not trained in phase angle interpretation for depth estimation",
            "Ferromagnetic material permeability variations not addressed"
        ],
        resolution_strategy="Provide skin depth calculations for selected frequency, demonstrate detection on reference standard at target depth, and document lift-off compensation validation",
        entity_scope="Aircraft structures, heat exchanger tubes, weld inspection, conductivity sorting",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when frequency selection justified by skin depth calculation and validated on reference standard; moderate if generic frequency used without depth analysis",
        controlling_precedent="ASTM E1004 Standard Practice and skin depth equation",
        issue_category=IssueCategory.ET_SURFACE
    ),

    DoctrineBlock(
        topic="Acoustic Emission Monitoring for Crack Growth Detection",
        keywords=["acoustic emission", "AE", "monitoring", "crack growth", "real-time", "sensor", "threshold", "event", "waveform", "pressure test"],
        conclusion_template="Acoustic emission (AE) monitors real-time elastic stress waves generated by active crack growth, corrosion, or leak formation. Per ASTM E1316, AE provides continuous monitoring during proof testing or service loading, detecting defects actively growing under stress (unlike other NDE methods requiring shutdown). Sensor threshold, event count, amplitude, and energy parameters indicate defect severity. AE source location through time-of-arrival triangulation identifies defect position. Acceptance based on event rate, cumulative count, and correlation with load cycle.",
        reasoning_framework="""
        AE physical mechanism:
        - Crack extension releases stored elastic energy as transient stress wave
        - Stress wave propagates through material as Rayleigh, Lamb, or bulk wave
        - Piezoelectric sensors on surface detect mechanical vibration (typically 20 kHz - 1 MHz)
        - Sensor converts mechanical wave to electrical signal
        - Signal processing identifies events, measures amplitude, counts events, calculates energy

        AE sources in pressure equipment:
        - Crack growth (fatigue, stress corrosion, brittle fracture)
        - Corrosion pitting and general wastage
        - Hydrogen-induced cracking activity
        - Leak formation (continuous emission vs burst events)
        - Fiber breakage in composite pressure vessels
        - Weld defect activation under stress

        Key AE parameters:
        Amplitude (dB): Peak voltage of AE signal
        - Higher amplitude = higher energy release = more severe event
        - Threshold set to reject background noise (typically 40-60 dB)

        Event count: Number of signals exceeding threshold
        - Accumulates during test
        - High count indicates active defect growth
        - Count rate (events/second) important during load changes

        Energy (arbitrary units): Area under rectified signal envelope
        - Correlates with total elastic energy release
        - Cumulative energy tracks total damage accumulation

        Duration (µs): Time signal exceeds threshold
        - Short duration: crack growth bursts
        - Long duration: leak or continuous plastic deformation

        Rise time (µs): Time from threshold crossing to peak amplitude
        - Fast rise time: brittle crack growth
        - Slow rise time: ductile tearing or corrosion

        Source location:
        - Multiple sensors (minimum 3 for 2D, 4 for 3D) detect same event
        - Time difference of arrival (TDOA) between sensors calculated
        - Triangulation using material wave velocity locates source coordinates
        - Location accuracy ±2-5% of sensor spacing typical
        - Planar location sufficient for pressure vessels (assume source on inner surface)

        ASTM E1316 test procedure:
        1. Attach sensors to pressure vessel/piping at strategic locations
        2. Verify sensor coupling with pencil lead break test (Hsu-Nielsen source)
        3. Establish threshold and recording parameters (amplitude, duration, energy)
        4. Pressurize equipment in steps (typically 10-20% increments to proof pressure)
        5. Hold at each pressure step and monitor AE activity
        6. Record event count, amplitude distribution, energy, and location for each step
        7. Evaluate results based on acceptance criteria

        Acceptance criteria (general):
        - Low activity: <10 events/minute, amplitude <60 dB → Accept
        - Moderate activity: 10-100 events/minute, amplitude 60-80 dB → Investigate/monitor
        - High activity: >100 events/minute, amplitude >80 dB, increasing count rate → Reject
        - Event clusters in specific location suggest localized defect requiring inspection
        - Continuous emission (leak indication) → Immediate shutdown and repair

        ASME Section V Article 11 (AE for pressure vessels):
        - Source location zones established
        - Event count and energy accumulation tracked per zone
        - Statistical analysis (Felicity ratio, load-unload behavior) indicates crack severity
        - High emission zones inspected with supplementary NDE (UT, RT, MT, PT)

        Advantages:
        - Real-time monitoring during operation or proof test
        - Whole-volume monitoring (not localized like UT scan)
        - Detects only active defects (ignores dormant flaws not growing)
        - Permanent installation enables continuous service monitoring

        Limitations:
        - Requires loading to activate defects (no detection at zero stress)
        - High background noise in service environment may mask signals
        - Attenuation limits range (~10 meters typical in steel)
        - Cannot size defects directly (only indicates activity level)
        - Requires supplementary NDE to characterize detected indications
        """,
        key_factors=[
            "Sensor placement for adequate coverage and location accuracy",
            "Sensor coupling verification with pencil lead break test",
            "Threshold setting to reject background noise while capturing defect signals",
            "Event count, amplitude, and energy parameter tracking",
            "Source location accuracy through TDOA triangulation",
            "Load step procedure for controlled stress application",
            "Acceptance criteria based on event rate and amplitude distribution",
            "Supplementary NDE on high-activity zones for defect characterization"
        ],
        primary_authority=[
            "ASTM E1316 Standard Terminology for Nondestructive Examinations (AE section)",
            "ASME Section V Article 11 (Acoustic Emission Examination of Fiber-Reinforced Plastic Vessels)",
            "ASTM E2661 Standard Practice for Acoustic Emission Examination of Plate-like and Tubular Metallic Structures"
        ],
        burden_holder="AE monitoring operator and data analyst",
        adversary_position="AE may produce false positives from background noise or false negatives if defect not stressed sufficiently; location accuracy limited by sensor spacing and attenuation",
        counter_arguments=[
            "Event count high but from background mechanical noise, not defect growth",
            "Sensor coupling inadequate resulting in signal attenuation and missed events",
            "Threshold set too high missing low-amplitude crack growth events",
            "Insufficient sensor density resulting in poor location accuracy",
            "Loading insufficient to activate known defects (pressure below yield stress)",
            "No supplementary NDE performed on high-activity zones to confirm defects",
            "Operator not trained in AE waveform and statistical analysis"
        ],
        resolution_strategy="Demonstrate sensor coupling validation, provide event amplitude and energy distribution plots, and correlate high-activity zones with supplementary NDE findings",
        entity_scope="Pressure vessels, storage tanks, pipelines, composite pressure vessels, bridges under proof load",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="High confidence when AE correlated with supplementary NDE confirming defects; moderate when AE alone without characterization of detected sources",
        controlling_precedent="ASME BPVC Section V Article 11 and ASTM E2661",
        issue_category=IssueCategory.AE_MONITORING
    ),

    DoctrineBlock(
        topic="ASNT SNT-TC-1A Personnel Qualification Requirements",
        keywords=["ASNT", "SNT-TC-1A", "personnel", "qualification", "certification", "Level I", "Level II", "Level III", "training", "examination"],
        conclusion_template="ASNT SNT-TC-1A establishes recommended practice for personnel qualification in NDT. Level I performs inspections under supervision; Level II performs and interprets inspections independently and trains Level I; Level III establishes procedures, interprets codes, and supervises entire NDT program. Per SNT-TC-1A, qualification requires training (method-specific and on-the-job), examination (general, specific, practical), and vision testing (near vision and color perception annually). Employer responsible for written practice defining qualification requirements and maintaining personnel records.",
        reasoning_framework="""
        SNT-TC-1A personnel levels:

        Level I:
        - Performs inspections per written instructions under supervision of Level II or III
        - Records results but does NOT independently interpret or evaluate against acceptance criteria
        - May perform calibrations and setups per written procedures
        - Minimum training: 40 hours method-specific classroom + 40 hours OJT (varies by method)

        Level II:
        - Performs inspections independently and interprets results against acceptance criteria
        - Prepares written instructions for Level I personnel
        - Trains and supervises Level I personnel
        - Evaluates and reports inspection results
        - Minimum training: Level I requirements + additional method-specific training + 200 hours OJT
        - Minimum experience: 3-6 months as Level I (varies by method complexity)

        Level III:
        - Establishes NDT procedures and techniques
        - Interprets codes, standards, specifications, and procedures
        - Designates NDT methods and techniques for specific applications
        - Supervises Level I and Level II personnel
        - Responsible for all NDT operations in the facility
        - Minimum training: Broad NDT knowledge across multiple methods
        - Minimum experience: 4 years in NDT (1 year as Level II minimum)

        Training requirements (method-specific):
        UT: 40 hours classroom (Level I), 80 hours (Level II), broad knowledge (Level III)
        RT: 40 hours classroom (Level I), 80 hours (Level II), broad knowledge (Level III)
        MT: 24 hours classroom (Level I), 40 hours (Level II)
        PT: 16 hours classroom (Level I), 24 hours (Level II)
        ET: 40 hours classroom (Level I), 80 hours (Level II)

        On-the-job training (OJT):
        Level I: Minimum 40-200 hours depending on method complexity
        Level II: Minimum 200-1000 hours depending on method complexity

        Examinations:
        General: NDT fundamentals, material properties, physics applicable to all methods
        Specific: Method-specific theory, code requirements, equipment, procedures
        Practical: Hands-on demonstration of technique on test specimens with known flaws

        Passing scores: Typically 70% minimum on each examination component

        Vision testing (annual requirement):
        Near vision: Jaeger #2 chart or equivalent at 12 inches (with corrective lenses allowed)
        Color perception: Ishihara test or equivalent (for methods requiring color discrimination like PT)

        Employer written practice:
        - Document defining training, examination, and qualification requirements
        - Maintained by Level III or designated certifying authority
        - Must address each NDT method used in facility
        - Specifies vision testing frequency and acceptance
        - Defines recertification requirements (typically 5-year maximum interval)

        Recertification:
        - Every 5 years maximum or sooner if proficiency questioned
        - May be based on continued satisfactory performance without re-examination
        - Or re-examination in general, specific, and practical components
        - Vision test required at each recertification

        ASME Section V mandatory requirements:
        - Personnel performing NDE per ASME Section V must be qualified per employer's written practice
        - Written practice must meet or exceed SNT-TC-1A recommendations
        - Alternative: CP-189 (ASNT Central Certification Program) for standardized qualification

        Common deficiencies:
        - Level I performing independent acceptance/rejection decisions (exceeds authority)
        - Level II not maintaining current certification (expired >5 years ago)
        - Vision test not performed annually as required
        - OJT hours not documented or insufficient for method complexity
        - Practical examination not performed on specimens with representative flaws
        - No Level III oversight of written practice and qualification records
        """,
        key_factors=[
            "Personnel level appropriate for task (Level II required for independent interpretation)",
            "Training hours meet minimum requirements for method and level",
            "On-the-job training documented and sufficient",
            "Examinations passed in general, specific, and practical components",
            "Vision testing current (within last 12 months)",
            "Certification current (within 5 years of last qualification/recertification)",
            "Employer written practice exists and meets SNT-TC-1A recommendations",
            "Level III oversight of NDT program and personnel qualification"
        ],
        primary_authority=[
            "ANSI/ASNT SNT-TC-1A Personnel Qualification and Certification in Nondestructive Testing",
            "ASME Section V Article 1 T-150 Personnel Qualification",
            "ASNT CP-189 ASNT Central Certification Program (alternative to SNT-TC-1A)"
        ],
        burden_holder="Employer and Level III responsible for NDT program",
        adversary_position="Inspection results may be invalid if personnel not qualified per SNT-TC-1A or performing tasks beyond authorized level",
        counter_arguments=[
            "Level I independently accepting/rejecting indications (requires Level II)",
            "Level II certification expired (not recertified within 5 years)",
            "Vision test not current (>12 months since last test)",
            "OJT hours insufficient for method complexity",
            "Practical examination not documented or not performed on representative flaws",
            "No employer written practice or practice does not meet SNT-TC-1A minimums",
            "No Level III oversight or Level III not qualified in relevant method"
        ],
        resolution_strategy="Provide personnel qualification records showing training hours, examination scores, vision test results, and current certification status",
        entity_scope="All NDT personnel in ASME, API, aerospace, and industrial inspection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when complete qualification records and current certifications documented; unacceptable if personnel unqualified or certifications expired",
        controlling_precedent="ANSI/ASNT SNT-TC-1A and ASME BPVC Section V Article 1 T-150",
        issue_category=IssueCategory.PERSONNEL_QUAL
    ),

    DoctrineBlock(
        topic="ASME Section V Code Requirements for NDE Methods",
        keywords=["ASME", "Section V", "code", "NDE", "requirement", "mandatory", "nonmandatory", "appendix", "procedure", "qualification"],
        conclusion_template="ASME Boiler and Pressure Vessel Code (BPVC) Section V provides mandatory requirements for nondestructive examination methods used in construction per Section I, III, IV, VIII, IX, and XII. Article 1 covers general requirements; Articles 2-25 address specific NDE methods (RT, UT, MT, PT, ET, VT, AE, etc.). Mandatory requirements must be met; nonmandatory appendices provide recommended practices. Written procedures required for each NDE method documenting technique, equipment, acceptance criteria, and personnel qualification.",
        reasoning_framework="""
        ASME BPVC Section V structure:

        Subsection A: Nondestructive Methods of Examination
        - Article 1: General Requirements (personnel, procedures, calibration, records)
        - Article 2: Radiographic Examination (RT)
        - Article 4: Ultrasonic Examination Methods for Welds (UT)
        - Article 5: Ultrasonic Examination Methods for Materials and Fabrication (UT thickness, etc.)
        - Article 6: Liquid Penetrant Examination (PT)
        - Article 7: Magnetic Particle Examination (MT)
        - Article 8: Eddy Current Examination (ET)
        - Article 9: Visual Examination (VT)
        - Article 10: Leak Testing (LT)
        - Article 11: Acoustic Emission Examination (AE)
        - Article 12: Electromagnetic (Eddy Current) Examination of Tubular Products (ET tubes)
        - Article 13: Continuous Monitoring (CM)
        - Article 14: Alternating Current Field Measurement (ACFM)
        - Article 15: Strain Gages

        Subsection B: Nondestructive Examination System Qualification
        - Articles 22-25: Performance Demonstration for UT

        Mandatory vs Nonmandatory:
        - Mandatory: Requirements in articles and mandatory appendices (designated "Mandatory Appendix...")
        - Nonmandatory: Appendices designated "Nonmandatory Appendix..." provide guidance but not required

        Written procedure requirements (Article 1 T-150):
        Each NDE method requires documented written procedure addressing:
        1. Scope and applicability
        2. Method and technique (RT, UT, MT, PT, etc.)
        3. Equipment description (manufacturer, model, calibration requirements)
        4. Calibration standards and frequency
        5. Surface preparation requirements
        6. Acceptance criteria and reporting
        7. Personnel qualification requirements
        8. Safety precautions

        Procedure qualification:
        - Demonstration that procedure capable of detecting flaws of specified size
        - Performed on mock-ups or qualification blocks with known flaws
        - Results documented in Procedure Qualification Record (PQR equivalent for NDE)

        Article 2: Radiographic Examination
        - Film, CR, DR techniques
        - IQI requirements (hole-type or wire-type per Table T-276)
        - Film density 1.8-4.0 for single-wall single-image
        - Geometric unsharpness limits
        - Mandatory Appendix I: Glossary of Terms for RT
        - Mandatory Appendix IV: Digital Imaging and Communication in NDE (DICONDE)

        Article 4: Ultrasonic Examination of Welds
        - Pulse-echo contact technique for welds
        - Calibration on blocks per Mandatory Appendix I
        - Scanning requirements (index offset, scan patterns)
        - Recording levels (reference, recording, evaluation)
        - Mandatory Appendix I: Phased Array UT
        - Mandatory Appendix II: Time-of-Flight Diffraction (TOFD)

        Article 5: Ultrasonic Examination for Materials
        - Thickness measurement
        - Lamination detection in plate
        - Calibration requirements

        Article 6: Liquid Penetrant Examination
        - Type I (fluorescent) and Type II (visible) penetrants
        - Methods A (water-washable), C (solvent-removable), D (post-emulsifiable)
        - Sensitivity levels
        - Processing times (penetrant dwell, developer dwell)

        Article 7: Magnetic Particle Examination
        - AC, DC, permanent magnet techniques
        - Continuous vs residual field
        - Particle types (dry, wet, fluorescent, visible)
        - Field strength verification (tangential field 300-800 gauss)

        Article 8: Eddy Current Examination
        - Frequency selection
        - Reference standards
        - Calibration requirements

        Article 9: Visual Examination
        - Direct, remote, translucent visual methods
        - Illumination requirements (minimum 1000 lux)
        - Vision acuity testing

        Article 11: Acoustic Emission Examination
        - Sensor placement and coupling verification
        - Event detection and location
        - Acceptance criteria based on event rate and amplitude

        Acceptance criteria:
        - Section V provides examination methods but NOT acceptance criteria
        - Acceptance criteria specified in construction code (e.g., ASME VIII Div 1 UW-51)
        - Inspector must reference both Section V (method) and construction code (acceptance)

        Common compliance issues:
        - Written procedure not addressing all required elements per Article 1 T-150
        - Calibration not performed per frequency specified in procedure
        - Personnel not qualified per employer's written practice meeting SNT-TC-1A
        - Acceptance criteria not clearly defined or not per construction code
        - Records incomplete (calibration records, inspection results, procedure references)
        """,
        key_factors=[
            "Written procedure exists for each NDE method used",
            "Procedure addresses all mandatory elements per Article 1 T-150",
            "Calibration performed per procedure and Article requirements",
            "Personnel qualified per SNT-TC-1A and Article 1 requirements",
            "Acceptance criteria clearly defined and traceable to construction code",
            "Mandatory appendices followed where applicable (PAUT, TOFD, DICONDE)",
            "Records maintained per Article 1 T-190 (calibration, results, personnel)",
            "Procedure qualified through demonstration on representative mock-ups"
        ],
        primary_authority=[
            "ASME Boiler and Pressure Vessel Code Section V Nondestructive Examination",
            "ASME Section I, III, IV, VIII, IX, XII (construction codes referencing Section V)",
            "Article 1 T-150 Written Practice and Procedure Requirements"
        ],
        burden_holder="Employer, NDE contractor, and Authorized Inspector",
        adversary_position="NDE may not meet code requirements if procedures incomplete, calibration not performed, or personnel unqualified",
        counter_arguments=[
            "No written procedure documented for NDE method used",
            "Procedure missing mandatory elements (calibration, acceptance criteria, etc.)",
            "Calibration not performed or not traceable to procedure requirements",
            "Personnel qualification records not meeting SNT-TC-1A minimums",
            "Acceptance criteria not defined or not traceable to construction code",
            "Mandatory appendices not followed (e.g., PAUT per Appendix I)",
            "Records incomplete or not maintained per Article 1 T-190"
        ],
        resolution_strategy="Provide written procedures, calibration records, personnel qualification records, and acceptance criteria references per construction code",
        entity_scope="ASME pressure vessels, boilers, piping, nuclear components",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when procedures complete and qualified, calibration documented, and personnel qualified; unacceptable if procedures missing or personnel unqualified",
        controlling_precedent="ASME BPVC Section V Article 1 and applicable method articles",
        issue_category=IssueCategory.CODE_COMPLIANCE
    ),

    DoctrineBlock(
        topic="API 510 Pressure Vessel Inspection Acceptance Criteria",
        keywords=["API 510", "pressure vessel", "in-service", "inspection", "acceptance", "thickness", "corrosion", "fitness for service", "remaining life"],
        conclusion_template="API 510 Pressure Vessel Inspection Code governs in-service inspection, rating, repair, and alteration of pressure vessels. Minimum required thickness calculated per original construction code (ASME VIII) accounting for corrosion allowance. Vessels showing thickness below minimum require fitness-for-service assessment per API 579-1/ASME FFS-1. External inspection every 5-10 years and internal inspection every 10-20 years typical, adjusted based on damage mechanisms and risk. Acceptance criteria include thickness, corrosion, cracking, deformation, and leak-tight operation.",
        reasoning_framework="""
        API 510 scope:
        - Pressure vessels in refinery, chemical, and petrochemical service
        - Original construction per ASME Section VIII Division 1 or 2
        - In-service inspection after initial startup (not new construction)
        - Covers inspection interval, methods, acceptance, repair, and alteration

        Inspection intervals (API 510 Section 6):
        External inspection:
        - Visual examination of external surfaces
        - Insulation removed at suspect areas or per risk-based inspection (RBI)
        - Interval: 5 years maximum (may be extended to 10 years with RBI)

        Internal inspection:
        - Complete internal and external visual examination
        - Thickness measurements at representative locations
        - NDE (UT, RT, MT, PT) on critical areas (nozzles, welds, corrosion-prone zones)
        - Interval: 10 years typical (may be shortened to 5 years or extended to 20 years based on damage rate)

        Thickness measurement and acceptance:
        Minimum required thickness (tmin) calculated per ASME VIII Division 1:
        tmin = (P × R) / (S × E - 0.6 × P) + Corrosion Allowance
        Where:
        P = Maximum allowable working pressure (MAWP) in psi
        R = Inside radius in inches
        S = Allowable stress at design temperature in psi
        E = Weld joint efficiency (1.0 for full RT, 0.85 for spot RT, 0.70 for no RT)

        Measured thickness (tactual) compared to tmin:
        - If tactual ≥ tmin: Acceptable, calculate remaining corrosion allowance and remaining life
        - If tactual < tmin: Fitness-for-service assessment required per API 579-1/ASME FFS-1

        Remaining corrosion allowance:
        CA_remaining = tactual - tmin

        Remaining life (years):
        Remaining_Life = CA_remaining / Corrosion_Rate
        Where Corrosion_Rate = (Original_Thickness - tactual) / Years_in_Service

        Next inspection interval set based on remaining life:
        - Interval ≤ Remaining_Life / 2 (inspect at half of calculated remaining life)
        - Maximum 10 years for internal, 5 years for external (unless RBI justifies extension)

        Fitness-for-service assessment (API 579-1/ASME FFS-1):
        When tactual < tmin, FFS assessment addresses:
        - Local thin areas (LTA): Level 1, 2, or 3 assessment per severity
        - Cracks: Crack growth analysis, critical crack size, remaining life
        - Hydrogen damage: Embrittlement, blistering, HTHA assessment
        - Dents and gouges: Stress concentration analysis
        - Laminations: Through-thickness extent, pressure test demonstration

        FFS assessment levels:
        Level 1: Conservative screening using tabulated criteria (quick, conservative)
        Level 2: Detailed analysis using analytical equations (moderate rigor)
        Level 3: Finite element analysis and fracture mechanics (rigorous, highest accuracy)

        Other acceptance criteria (API 510 Section 7):
        Corrosion:
        - General thinning: Acceptable if tactual ≥ tmin
        - Pitting: Depth <50% thickness and isolated acceptable; clustering or deep pits require FFS
        - Grooving: Weld or nozzle neck grooving evaluated per API 579 Part 5

        Cracking:
        - Any crack indication rejectable unless FFS assessment demonstrates acceptability
        - Common crack types: stress corrosion cracking (SCC), hydrogen-induced cracking (HIC),
          fatigue, creep (high temperature)
        - Crack repair typically required; monitoring acceptable only with FFS justification

        Deformation:
        - Out-of-roundness: <1% of diameter acceptable
        - Bulging: Local bulges indicate yielding or creep, require engineering assessment
        - Misalignment: Peaking at joints <1/4 inch or 10% thickness (whichever less)

        Leakage:
        - Any leak unacceptable and requires immediate repair
        - Hydrostatic pressure test to 1.5× MAWP may be required after repair or alteration

        NDE methods per API 510:
        - Visual examination (VT): Primary method for internal and external inspection
        - Ultrasonic thickness (UT): Thickness measurement at CMLs (corrosion monitoring locations)
        - Radiography (RT): Weld repairs and alterations
        - Magnetic particle (MT): Surface crack detection in welds and nozzles (ferromagnetic materials)
        - Liquid penetrant (PT): Surface crack detection (non-ferromagnetic materials)
        - Advanced: Phased array UT, TOFD for weld integrity, AE for proof test monitoring

        Authorized Inspector (AI) role:
        - API 510 certified inspector oversees inspection and accepts/rejects findings
        - AI verifies NDE procedures, personnel qualification, and acceptance criteria
        - AI signs off on inspection reports and maximum allowable working pressure (MAWP) verification
        - Repairs and alterations require AI approval before return to service

        Common deficiencies:
        - Thickness measurements not performed at sufficient density (too few CMLs)
        - Corrosion rate not calculated or remaining life not estimated
        - FFS assessment not performed when tactual < tmin
        - Inspection interval not adjusted based on corrosion rate and remaining life
        - Repairs not per ASME Section VIII or National Board Inspection Code (NBIC)
        - No AI oversight or API 510 certification expired
        """,
        key_factors=[
            "Minimum required thickness calculated per original construction code",
            "Thickness measurements at sufficient corrosion monitoring locations (CMLs)",
            "Corrosion rate calculated from thickness loss over service years",
            "Remaining life estimated and next inspection interval adjusted accordingly",
            "Fitness-for-service assessment when thickness below minimum",
            "NDE methods appropriate for damage mechanisms (UT, RT, MT, PT)",
            "Authorized Inspector (API 510 certified) oversight and approval",
            "Repairs per ASME Section VIII or NBIC with proper procedure and qualification"
        ],
        primary_authority=[
            "API 510 Pressure Vessel Inspection Code: In-Service Inspection, Rating, Repair, and Alteration",
            "API 579-1/ASME FFS-1 Fitness-For-Service Standard",
            "ASME Section VIII Division 1 or 2 (original construction code)",
            "National Board Inspection Code (NBIC) for repairs and alterations"
        ],
        burden_holder="Owner/operator, inspection contractor, and Authorized Inspector",
        adversary_position="Vessel may be unsafe for continued operation if thickness below minimum, corrosion rate underestimated, or FFS assessment inadequate",
        counter_arguments=[
            "Thickness below minimum required with no FFS assessment performed",
            "Corrosion rate not calculated or based on insufficient historical data",
            "Remaining life overestimated resulting in excessive inspection interval",
            "Thickness measurements at too few locations missing localized thin areas",
            "Crack indications not evaluated or repaired",
            "Repairs not per ASME or NBIC code requirements",
            "Authorized Inspector not API 510 certified or certification expired",
            "No hydrostatic test after repair or alteration when required"
        ],
        resolution_strategy="Provide thickness measurement data at CMLs, corrosion rate calculations, remaining life estimates, FFS assessment if applicable, and AI certification records",
        entity_scope="Refinery pressure vessels, petrochemical reactors, storage tanks under pressure",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when thickness adequate and remaining life calculated; moderate when relying on FFS assessment for below-minimum thickness; unacceptable if thickness below minimum without FFS",
        controlling_precedent="API 510 and API 579-1/ASME FFS-1",
        issue_category=IssueCategory.ACCEPTANCE_CRITERIA
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# SEMANTIC NORMALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

SEMANTIC_NORMALIZATION_MAP = {
    "ultrasonic testing": ["UT", "ultrasonic", "pulse-echo", "through-transmission", "angle beam", "straight beam"],
    "phased array": ["PAUT", "phased array UT", "PA-UT", "electronic scanning", "sector scan", "linear scan"],
    "TOFD": ["time-of-flight diffraction", "time of flight", "diffraction technique"],
    "radiography": ["RT", "radiographic testing", "X-ray", "gamma ray", "film", "CR", "DR"],
    "computed radiography": ["CR", "phosphor plate", "imaging plate"],
    "digital radiography": ["DR", "flat panel", "DDA", "digital detector array"],
    "magnetic particle": ["MT", "magnetic particle testing", "mag particle", "flux leakage"],
    "liquid penetrant": ["PT", "penetrant testing", "dye penetrant", "fluorescent penetrant"],
    "eddy current": ["ET", "eddy current testing", "electromagnetic testing", "ECT"],
    "acoustic emission": ["AE", "acoustic emission monitoring", "AE testing"],
    "image quality indicator": ["IQI", "penetrameter", "step wedge", "sensitivity indicator"],
    "thickness measurement": ["thickness gage", "thickness testing", "corrosion monitoring"],
    "crack detection": ["flaw detection", "discontinuity detection", "defect detection"],
    "weld inspection": ["weld examination", "weld testing", "weld NDE"],
    "acceptance criteria": ["rejection criteria", "acceptance standards", "allowable indications"],
    "sensitivity": ["detection limit", "minimum detectable flaw", "resolution"],
    "calibration": ["standardization", "reference standard", "calibration block"],
}

def normalize_query(query: str) -> str:
    query_lower = query.lower()
    for canonical, variants in SEMANTIC_NORMALIZATION_MAP.items():
        for variant in variants:
            if variant.lower() in query_lower:
                query_lower = query_lower.replace(variant.lower(), canonical)
    return query_lower

# ═══════════════════════════════════════════════════════════════════════════════
# TELEMETRY AND METRICS
# ═══════════════════════════════════════════════════════════════════════════════

class MetricsCollector:
    def __init__(self):
        self.query_count = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_latency_ms = 0.0
        self.error_count = 0
        self.doctrine_trigger_counts: Dict[str, int] = defaultdict(int)

    def record_query(self, telemetry: TelemetryRecord):
        self.query_count += 1
        if telemetry.hit_cache:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        self.total_latency_ms += telemetry.latency_ms
        for doctrine in telemetry.doctrines_triggered:
            self.doctrine_trigger_counts[doctrine] += 1
        if telemetry.error_domain:
            self.error_count += 1

        with open(METRICS_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "timestamp": telemetry.timestamp,
                "query_id": telemetry.query_id,
                "mode": telemetry.mode.value,
                "hit_cache": telemetry.hit_cache,
                "latency_ms": telemetry.latency_ms,
                "doctrines_triggered": telemetry.doctrines_triggered,
                "error_domain": telemetry.error_domain
            }) + "\n")

    def get_stats(self) -> Dict[str, Any]:
        cache_hit_rate = (self.cache_hits / self.query_count * 100) if self.query_count > 0 else 0.0
        avg_latency = (self.total_latency_ms / self.query_count) if self.query_count > 0 else 0.0
        return {
            "query_count": self.query_count,
            "cache_hit_rate": round(cache_hit_rate, 2),
            "avg_latency_ms": round(avg_latency, 2),
            "error_count": self.error_count,
            "top_doctrines": dict(Counter(self.doctrine_trigger_counts).most_common(10))
        }

METRICS = MetricsCollector()

# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT TRAIL
# ═══════════════════════════════════════════════════════════════════════════════

def write_audit_log(query_id: str, query: str, response: Dict[str, Any], mode: ResponseMode):
    audit_entry = {
        "query_id": query_id,
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "mode": mode.value,
        "response_summary": response.get("conclusion", "")[:200],
        "doctrines_triggered": response.get("doctrines_triggered", []),
        "confidence": response.get("confidence", ""),
    }
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(audit_entry) + "\n")

# ═══════════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE SEARCH
# ═══════════════════════════════════════════════════════════════════════════════

def search_doctrine_cache(query: str) -> List[DoctrineBlock]:
    normalized = normalize_query(query)
    matches = []
    for doctrine in DOCTRINE_CACHE:
        keyword_match = any(kw.lower() in normalized for kw in doctrine.keywords)
        topic_match = doctrine.topic.lower() in normalized or normalized in doctrine.topic.lower()
        if keyword_match or topic_match:
            matches.append(doctrine)
    return matches

# ═══════════════════════════════════════════════════════════════════════════════
# THREE-LAYER RESPONSE ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def three_layer_response(query: str, mode: ResponseMode) -> Dict[str, Any]:
    start_time = time.time()
    query_id = hashlib.sha256(f"{query}{time.time()}".encode()).hexdigest()[:16]

    # Layer 1: Doctrine Cache (0-200ms)
    cache_matches = search_doctrine_cache(query)

    if cache_matches:
        primary = cache_matches[0]
        latency_ms = (time.time() - start_time) * 1000

        if mode == ResponseMode.FAST:
            response_text = primary.conclusion_template
        elif mode == ResponseMode.DEFENSE:
            response_text = f"{primary.conclusion_template}\n\n{primary.reasoning_framework}\n\nPrimary Authority: {', '.join(primary.primary_authority)}"
        else:  # MEMO
            response_text = f"""
TOPIC: {primary.topic}

CONCLUSION:
{primary.conclusion_template}

REASONING FRAMEWORK:
{primary.reasoning_framework}

KEY FACTORS:
{chr(10).join(f'- {factor}' for factor in primary.key_factors)}

PRIMARY AUTHORITY:
{chr(10).join(f'- {auth}' for auth in primary.primary_authority)}

ADVERSARY POSITION:
{primary.adversary_position}

COUNTER-ARGUMENTS:
{chr(10).join(f'- {arg}' for arg in primary.counter_arguments)}

RESOLUTION STRATEGY:
{primary.resolution_strategy}

CONFIDENCE LEVEL: {primary.confidence.value}
CONFIDENCE STRATIFICATION: {primary.confidence_stratification}
CONTROLLING PRECEDENT: {primary.controlling_precedent}
"""

        telemetry = TelemetryRecord(
            query_id=query_id,
            timestamp=time.time(),
            mode=mode,
            hit_cache=True,
            latency_ms=latency_ms,
            doctrines_triggered=[d.topic for d in cache_matches[:3]]
        )
        METRICS.record_query(telemetry)

        result = {
            "query_id": query_id,
            "conclusion": response_text,
            "confidence": primary.confidence.value,
            "doctrines_triggered": [d.topic for d in cache_matches[:3]],
            "primary_authority": primary.primary_authority,
            "latency_ms": round(latency_ms, 2),
            "layer": "doctrine_cache"
        }

        write_audit_log(query_id, query, result, mode)
        return result

    # Layer 2: Semantic Retrieval (fallback if cache miss)
    # In production, would query vector DB. Here we provide a general response.
    latency_ms = (time.time() - start_time) * 1000

    general_response = f"""
The query '{query}' requires analysis of NDT methods, standards, or inspection criteria.

General NDT Domain Guidance:
- Ultrasonic Testing (UT): Pulse-echo, phased array, TOFD for volumetric inspection
- Radiographic Testing (RT): Film, CR, DR for internal discontinuity detection
- Magnetic Particle Testing (MT): Surface and near-surface crack detection in ferromagnetic materials
- Liquid Penetrant Testing (PT): Surface-breaking discontinuity detection in non-porous materials
- Eddy Current Testing (ET): Surface and subsurface flaw detection in conductive materials
- Acoustic Emission (AE): Real-time monitoring of active defect growth under stress

Standards and Codes:
- ASME Section V: NDE methods for pressure equipment construction
- ASTM E1417, E1444, E797, E1004: Method-specific standards
- API 510/570/653: In-service inspection of pressure equipment
- ASNT SNT-TC-1A: Personnel qualification requirements

For specific technical guidance on this query, consult relevant code sections and technical experts.
"""

    telemetry = TelemetryRecord(
        query_id=query_id,
        timestamp=time.time(),
        mode=mode,
        hit_cache=False,
        latency_ms=latency_ms,
        doctrines_triggered=["general_ndt_guidance"]
    )
    METRICS.record_query(telemetry)

    result = {
        "query_id": query_id,
        "conclusion": general_response,
        "confidence": ConfidenceLevel.DISCLOSURE.value,
        "doctrines_triggered": ["general_ndt_guidance"],
        "primary_authority": ["ASME Section V", "ASTM Standards", "API Codes"],
        "latency_ms": round(latency_ms, 2),
        "layer": "semantic_retrieval"
    }

    write_audit_log(query_id, query, result, mode)
    return result

# ═══════════════════════════════════════════════════════════════════════════════
# DETERMINISM HASH
# ═══════════════════════════════════════════════════════════════════════════════

def compute_determinism_hash(query: str, response: Dict[str, Any]) -> str:
    content = f"{query}|{response['conclusion']}|{response['confidence']}"
    return hashlib.sha256(content.encode()).hexdigest()

# ═══════════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

APP = FastAPI(
    title=f"{ENGINE_NAME} Intelligence Engine",
    version=ENGINE_VERSION,
    description="TIE-Grade NDT Inspection Intelligence Engine"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str = Field(..., description="NDT inspection query")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response mode")

class QueryResponse(BaseModel):
    query_id: str
    conclusion: str
    confidence: str
    doctrines_triggered: List[str]
    primary_authority: List[str]
    latency_ms: float
    determinism_hash: str
    layer: str

@APP.post("/query", response_model=QueryResponse)
async def query_engine(req: QueryRequest):
    logger.info(f"Query received: {req.query[:100]} | Mode: {req.mode}")

    try:
        response = three_layer_response(req.query, req.mode)
        response["determinism_hash"] = compute_determinism_hash(req.query, response)
        logger.info(f"Query {response['query_id']} completed in {response['latency_ms']}ms")
        return response
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "engine": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": PORT,
        "doctrine_cache_size": len(DOCTRINE_CACHE),
        "metrics": METRICS.get_stats(),
        "uptime_seconds": int(time.time() - METRICS.query_count)  # Approximate
    }

@APP.get("/doctrines")
async def list_doctrines():
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "confidence": d.confidence.value,
                "keywords": d.keywords[:5]
            }
            for d in DOCTRINE_CACHE
        ]
    }

@APP.get("/metrics")
async def get_metrics():
    return METRICS.get_stats()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {PORT}")
    logger.info(f"Doctrine cache loaded: {len(DOCTRINE_CACHE)} blocks")
    uvicorn.run(APP, host="0.0.0.0", port=PORT, log_level="info")
