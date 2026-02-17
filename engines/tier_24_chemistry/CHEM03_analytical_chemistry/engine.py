"""
CHEM03 - Analytical Chemistry Intelligence Engine
Comprehensive analytical methods, instrumentation, and quality assurance knowledge.
Port: 9053 | Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ============================================================================
# CONFIGURATION & ENUMS
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

class IssueCategory(str, Enum):
    CHROMATOGRAPHY = "CHROMATOGRAPHY"
    SPECTROSCOPY = "SPECTROSCOPY"
    ELECTROCHEMISTRY = "ELECTROCHEMISTRY"
    TITRATION = "TITRATION"
    GRAVIMETRIC = "GRAVIMETRIC"
    SAMPLING = "SAMPLING"
    QUALITY_ASSURANCE = "QUALITY_ASSURANCE"
    METHOD_VALIDATION = "METHOD_VALIDATION"
    DATA_ANALYSIS = "DATA_ANALYSIS"
    CALIBRATION = "CALIBRATION"
    ATOMIC_METHODS = "ATOMIC_METHODS"
    XRAY_METHODS = "XRAY_METHODS"
    THERMAL_ANALYSIS = "THERMAL_ANALYSIS"
    SURFACE_ANALYSIS = "SURFACE_ANALYSIS"
    SEPARATION_SCIENCE = "SEPARATION_SCIENCE"
    SAMPLE_PREP = "SAMPLE_PREP"
    SAFETY = "SAFETY"
    COMPLIANCE = "COMPLIANCE"
    APPLICATION = "APPLICATION"

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class DoctrineBlock:
    """Encapsulated analytical chemistry knowledge block"""
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    category: IssueCategory
    adversarial_considerations: List[str] = field(default_factory=list)
    common_errors: List[str] = field(default_factory=list)
    method_requirements: List[str] = field(default_factory=list)

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query: str
    response: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    doctrines_triggered: List[str]
    reasoning_chain: List[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str

# ============================================================================
# DOCTRINE CACHE - ANALYTICAL CHEMISTRY EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    # === CHROMATOGRAPHY ===
    DoctrineBlock(
        topic="Gas Chromatography Fundamentals",
        keywords=["GC", "gas chromatography", "column", "detector", "retention time", "peak resolution"],
        conclusion_template=[
            "Gas chromatography separates volatile compounds based on partition coefficients between mobile gas phase and stationary phase.",
            "Retention time is characteristic for compound identification; peak area/height quantifies concentration.",
            "Resolution depends on column efficiency (N), selectivity (α), and retention factor (k)."
        ],
        reasoning_framework="""
Gas chromatography analysis requires:
1. Sample injection system (split/splitless, on-column, headspace)
2. Carrier gas selection (He, H2, N2) affects efficiency
3. Column type: packed vs capillary, polar vs nonpolar stationary phase
4. Temperature programming: isothermal vs gradient for separation optimization
5. Detector selection: FID (organics), TCD (universal), ECD (halogens), MS (identification)
6. Van Deemter equation describes relationship between plate height and flow rate
7. Resolution equation: Rs = 0.25N^0.5(α-1/α)(k/(1+k))
8. Peak tailing indicates active sites or overload; fronting indicates column overload
9. Internal standard corrects for injection variability and detector drift
10. Derivatization extends GC to non-volatile compounds
        """,
        key_factors=[
            "Column selection based on analyte polarity and volatility",
            "Carrier gas flow rate optimization for efficiency",
            "Injection technique appropriate for sample matrix",
            "Temperature program for adequate resolution",
            "Detector sensitivity and selectivity for target analytes",
            "Calibration method and linearity verification",
            "Chromatographic peak integration parameters"
        ],
        primary_authority=[
            "ASTM D3525: Gasoline Analysis by GC",
            "EPA Method 8000: Gas Chromatography",
            "USP <621> Chromatography General Chapter"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CHROMATOGRAPHY,
        adversarial_considerations=[
            "Co-elution of matrix interferences can cause false positives",
            "Detector saturation leads to non-linear response",
            "Carryover from previous injections affects quantitation"
        ],
        common_errors=[
            "Inadequate column conditioning before analysis",
            "Improper split ratio causing discrimination",
            "Ghost peaks from column bleed or contamination"
        ],
        method_requirements=[
            "Column performance test (resolution, efficiency, symmetry)",
            "Carrier gas purity specification (>99.999%)",
            "Routine maintenance schedule for inlet and detector"
        ]
    ),

    DoctrineBlock(
        topic="High Performance Liquid Chromatography",
        keywords=["HPLC", "liquid chromatography", "reversed phase", "gradient", "UV detector", "retention"],
        conclusion_template=[
            "HPLC separates compounds in liquid mobile phase using differential partitioning with stationary phase.",
            "Reversed-phase HPLC (C18, C8) retains nonpolar compounds; normal phase retains polar compounds.",
            "Method development balances resolution, analysis time, and sensitivity through mobile phase and gradient optimization."
        ],
        reasoning_framework="""
HPLC method development and validation:
1. Stationary phase selection: RP (C18, C8), NP (silica, cyano), ion exchange, size exclusion
2. Mobile phase composition: aqueous/organic ratio, pH, buffer type, additives
3. Gradient vs isocratic elution for complex vs simple mixtures
4. Flow rate affects backpressure and resolution (typical 0.5-2.0 mL/min)
5. Column dimensions: 4.6 mm ID standard, 2.1 mm for LC-MS, 150-250 mm length
6. Detector selection: UV-Vis (chromophores), fluorescence (sensitivity), RI (universal), MS (identification)
7. Sample preparation: filtration, extraction, dilution to match solvent strength
8. System suitability testing: retention time, peak shape, resolution, plate count
9. Validation parameters: linearity, accuracy, precision, LOD, LOQ, robustness
10. Troubleshooting: pressure changes indicate column degradation or blockage
        """,
        key_factors=[
            "Column chemistry matched to analyte properties",
            "Mobile phase pH control for ionizable compounds",
            "Gradient optimization for retention and resolution",
            "Detector wavelength selection for maximum absorbance",
            "Sample solvent compatibility with mobile phase",
            "Temperature control for reproducibility",
            "Injection volume within linear range"
        ],
        primary_authority=[
            "USP <621> Chromatography",
            "ICH Q2(R1) Validation of Analytical Procedures",
            "FDA Bioanalytical Method Validation Guidance"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CHROMATOGRAPHY,
        adversarial_considerations=[
            "Buffer precipitation at high organic content causes blockages",
            "pH changes during gradient affect ionization and retention",
            "Column void volume from particulate contamination"
        ],
        common_errors=[
            "Mismatch between sample solvent and mobile phase strength",
            "Inadequate equilibration time between injections",
            "Air bubbles in mobile phase causing baseline noise"
        ]
    ),

    DoctrineBlock(
        topic="Mass Spectrometry Principles",
        keywords=["mass spec", "MS", "fragmentation", "molecular ion", "m/z", "ionization"],
        conclusion_template=[
            "Mass spectrometry measures mass-to-charge ratio of ions to identify and quantify compounds.",
            "Ionization method (EI, CI, ESI, APCI, MALDI) determines fragmentation pattern and sensitivity.",
            "Tandem MS (MS/MS) provides selectivity through precursor ion selection and product ion monitoring."
        ],
        reasoning_framework="""
Mass spectrometry analysis workflow:
1. Ionization methods: EI (70 eV fragmentation), CI (soft ionization), ESI (biomolecules), APCI (small molecules), MALDI (polymers)
2. Mass analyzers: quadrupole (unit resolution), TOF (accurate mass), ion trap (MSn), orbitrap (ultra-high resolution)
3. Fragmentation patterns for structural elucidation: McLafferty rearrangement, alpha cleavage, loss of stable neutrals
4. Selected Ion Monitoring (SIM) for quantitation with high sensitivity
5. Multiple Reaction Monitoring (MRM) in triple quadrupole for selectivity
6. Accurate mass measurement for elemental composition determination (±5 ppm)
7. Isotope patterns confirm presence of Cl, Br, S atoms
8. Matrix effects in ESI require isotope dilution or matrix-matched standards
9. Collision-induced dissociation (CID) for fragmentation control
10. Data-dependent acquisition for untargeted screening
        """,
        key_factors=[
            "Ionization efficiency depends on analyte polarity and pH",
            "Mass resolution adequate for separation of isobaric ions",
            "Fragmentation voltage optimization for molecular ion vs fragments",
            "Dwell time in SIM/MRM affects sensitivity and duty cycle",
            "Calibration with mass standard for accurate mass",
            "Ion suppression/enhancement from matrix components",
            "Desolvation temperature for complete solvent removal"
        ],
        primary_authority=[
            "ASTM E2456: Mass Spectrometry Terminology",
            "EPA Method 8270: GC-MS for Semivolatiles",
            "SWGDRUG Mass Spectral Library Guidelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SPECTROSCOPY
    ),

    DoctrineBlock(
        topic="UV-Visible Spectroscopy",
        keywords=["UV-Vis", "absorbance", "Beer's law", "chromophore", "lambda max", "extinction coefficient"],
        conclusion_template=[
            "UV-Vis spectroscopy measures absorption of electromagnetic radiation in 200-800 nm range.",
            "Beer's Law (A = εbc) relates absorbance to concentration through molar absorptivity and path length.",
            "Chromophores with conjugated systems or aromatic rings exhibit characteristic absorption maxima."
        ],
        reasoning_framework="""
UV-Vis spectroscopic analysis:
1. Wavelength range: UV (200-400 nm), Visible (400-800 nm)
2. Beer's Law: A = εbc, where ε = molar absorptivity (L/mol·cm), b = path length (cm), c = concentration (M)
3. Deviations from linearity: high absorbance (>1.5), stray light, chemical interactions, non-monochromatic light
4. Single vs dual beam instruments: dual beam corrects for source drift
5. Derivative spectroscopy resolves overlapping peaks
6. Difference spectroscopy detects small changes (binding studies)
7. Solvent selection: transparency at wavelength of interest, minimal analyte interaction
8. Baseline correction for scattering and background absorption
9. Kinetic measurements: reaction rate monitoring at fixed wavelength
10. Quantitation: calibration curve from standards, single-point if ε known
        """,
        key_factors=[
            "Wavelength selection at absorption maximum for sensitivity",
            "Path length choice for absorbance in linear range (0.1-1.0)",
            "Blank correction for solvent and cuvette absorption",
            "Sample concentration within Beer's Law range",
            "Spectral bandwidth narrower than absorption band",
            "Temperature control for thermochromic compounds",
            "Cuvette cleanliness and matching for paired measurements"
        ],
        primary_authority=[
            "USP <857> Ultraviolet-Visible Spectroscopy",
            "ASTM E169: UV-Vis Spectrophotometry",
            "IUPAC Recommendations on UV-Vis Nomenclature"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SPECTROSCOPY
    ),

    DoctrineBlock(
        topic="Infrared Spectroscopy",
        keywords=["IR", "FTIR", "vibrational", "functional group", "wavenumber", "transmittance"],
        conclusion_template=[
            "IR spectroscopy identifies functional groups through characteristic vibrational frequencies (4000-400 cm⁻¹).",
            "FTIR provides rapid scanning with high resolution and signal-to-noise ratio via interferometry.",
            "Sample preparation (KBr pellet, ATR, film) affects spectral quality and interpretation."
        ],
        reasoning_framework="""
Infrared spectroscopy fundamentals:
1. Molecular vibrations: stretching (symmetric, asymmetric), bending (scissoring, rocking, wagging, twisting)
2. Selection rule: change in dipole moment required for IR activity
3. Functional group frequencies: O-H (3200-3600), N-H (3300-3500), C=O (1650-1750), C-C (800-1500) cm⁻¹
4. Fingerprint region (<1500 cm⁻¹) for compound identification
5. FTIR advantages: multiplex (Fellgett), throughput (Jacquinot), wavenumber accuracy (Connes)
6. ATR (Attenuated Total Reflectance) for direct solid/liquid analysis without preparation
7. Transmission mode requires thin samples or dilution in KBr/Nujol
8. Hydrogen bonding causes broadening and shifts O-H, N-H peaks
9. Sample thickness affects peak intensity (too thick causes saturation)
10. Spectral subtraction removes solvent or background interference
        """,
        key_factors=[
            "Resolution setting (2-4 cm⁻¹ typical) balances detail vs noise",
            "Number of scans averaged for improved signal-to-noise",
            "Sample contact with ATR crystal for reproducible depth of penetration",
            "Moisture removal for hygroscopic samples (interferes 3200-3600 cm⁻¹)",
            "Baseline correction for sloped backgrounds",
            "Wavenumber calibration with polystyrene standard",
            "Clean optics to prevent CO2/H2O vapor interference"
        ],
        primary_authority=[
            "ASTM E1252: General IR Spectroscopy",
            "ASTM E168: Practices for General Techniques of IR Quantitative Analysis",
            "USP <197.1> Infrared Spectroscopy Theory"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SPECTROSCOPY
    ),

    DoctrineBlock(
        topic="Nuclear Magnetic Resonance Spectroscopy",
        keywords=["NMR", "chemical shift", "coupling", "integration", "multiplicity", "proton"],
        conclusion_template=[
            "NMR spectroscopy elucidates molecular structure through chemical shifts, coupling patterns, and integration.",
            "¹H-NMR provides information on hydrogen environments; ¹³C-NMR reveals carbon skeleton.",
            "2D NMR (COSY, HSQC, HMBC) establishes connectivity and spatial relationships."
        ],
        reasoning_framework="""
NMR spectroscopy for structure determination:
1. Chemical shift (δ ppm): electron density around nucleus determines resonance frequency
2. ¹H-NMR regions: aromatic (6-8), vinyl (4.5-6), alpha to heteroatom (2.5-4.5), aliphatic (0-2.5) ppm
3. ¹³C-NMR regions: carbonyl (160-220), aromatic (100-160), aliphatic (0-100) ppm
4. Spin-spin coupling: J-coupling (Hz) through bonds follows n+1 rule for multiplicity
5. Integration: area under peak proportional to number of equivalent protons
6. Decoupling experiments: ¹H-decoupled ¹³C shows singlets for all carbons
7. DEPT (Distortionless Enhancement by Polarization Transfer): distinguishes CH3, CH2, CH, quaternary C
8. COSY (Correlation Spectroscopy): ¹H-¹H correlations through 2-3 bonds
9. HSQC (Heteronuclear Single Quantum Coherence): direct ¹H-¹³C correlations
10. HMBC (Heteronuclear Multiple Bond Correlation): long-range ¹H-¹³C (2-4 bonds)
        """,
        key_factors=[
            "Field strength (60-900 MHz) affects resolution and sensitivity",
            "Solvent selection: deuterated for field lock (CDCl3, DMSO-d6, D2O)",
            "Sample concentration (1-10 mg/mL typical) for adequate signal",
            "Shimming for homogeneous magnetic field",
            "Number of scans for signal-to-noise improvement",
            "Relaxation delay between pulses for quantitative analysis",
            "Temperature control for exchangeable protons"
        ],
        primary_authority=[
            "ASTM E386: NMR Data Presentation",
            "IUPAC Recommendations on NMR Nomenclature",
            "USP <761> Nuclear Magnetic Resonance Spectroscopy"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SPECTROSCOPY
    ),

    # === ELECTROCHEMISTRY ===
    DoctrineBlock(
        topic="Potentiometry and pH Measurement",
        keywords=["potentiometry", "pH", "electrode", "Nernst equation", "ISE", "reference electrode"],
        conclusion_template=[
            "Potentiometry measures electrode potential at zero current to determine analyte concentration or activity.",
            "pH measurement uses glass electrode with Nernst response: E = E° + (RT/nF)ln(a), slope ~59.16 mV/pH at 25°C.",
            "Ion-selective electrodes (ISE) provide direct concentration measurement for specific ions."
        ],
        reasoning_framework="""
Potentiometric analysis principles:
1. Nernst equation: E = E° + (2.303RT/nF)log(a), where a = activity
2. pH electrode: glass membrane selective for H⁺, internal Ag/AgCl reference
3. Reference electrodes: SCE (saturated calomel), Ag/AgCl (saturated KCl), stable potential
4. Junction potential from liquid junction requires minimization via salt bridge
5. Electrode calibration: minimum 2-point with buffers bracketing sample pH
6. Temperature correction: slope changes with temperature (Nernstian factor RT/F)
7. ISE selectivity coefficient: Nicolsky-Eisenman equation accounts for interferences
8. Response time: equilibration required, stirring accelerates (1-5 min typical)
9. Electrode maintenance: hydration of glass membrane, reference junction flow check
10. Activity vs concentration: ionic strength correction via Debye-Hückel equation
        """,
        key_factors=[
            "Buffer selection for calibration bracketing sample pH range",
            "Temperature equilibration of standards and samples",
            "Electrode conditioning before measurement (soaking, rinsing)",
            "Stirring consistency for reproducible junction potential",
            "Sample ionic strength matching or adjustment (TISAB)",
            "Electrode slope verification (95-105% of theoretical)",
            "Reference electrode junction contamination check"
        ],
        primary_authority=[
            "ASTM E70: pH Measurement Standard",
            "USP <791> pH Determination",
            "IUPAC Recommendations on pH Measurement"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ELECTROCHEMISTRY
    ),

    DoctrineBlock(
        topic="Voltammetry and Electrochemical Detection",
        keywords=["voltammetry", "cyclic voltammetry", "electrochemical", "redox", "electrode", "current"],
        conclusion_template=[
            "Voltammetry measures current as function of applied potential to study redox reactions and quantify electroactive species.",
            "Cyclic voltammetry (CV) provides mechanistic information: peak separation, reversibility, diffusion vs adsorption.",
            "Electrochemical detection in HPLC offers high sensitivity for phenols, thiols, and easily oxidized/reduced compounds."
        ],
        reasoning_framework="""
Voltammetric techniques and applications:
1. Linear sweep voltammetry: potential ramped linearly, current measured
2. Cyclic voltammetry: triangular waveform, forward and reverse scans reveal reversibility
3. Reversible system: ΔEp = 59/n mV, ip proportional to ν^0.5 (diffusion-controlled)
4. Irreversible system: larger peak separation, only cathodic or anodic peak
5. Working electrodes: glassy carbon, Pt, Au, Hg (hanging drop, static mercury drop)
6. Three-electrode system: working, reference (Ag/AgCl, SCE), counter (Pt wire)
7. Differential pulse voltammetry (DPV): improved sensitivity by measuring current difference
8. Square wave voltammetry (SWV): fast scanning with excellent sensitivity
9. Stripping voltammetry: preconcentration step for trace metal analysis (ASV, CSV)
10. Electrochemical detector for HPLC: oxidation or reduction at fixed potential, high selectivity
        """,
        key_factors=[
            "Scan rate affects peak current and resolution",
            "Supporting electrolyte provides conductivity without interference",
            "Oxygen removal (N2 purge) prevents reduction peaks",
            "Electrode surface preparation (polishing, activation) for reproducibility",
            "Potential window of solvent and electrolyte limits usable range",
            "Reference electrode stability and calibration",
            "Cell geometry and stirring for stripping voltammetry"
        ],
        primary_authority=[
            "ASTM D6307: Asphaltene Precipitation by Voltammetry",
            "IUPAC Recommendations on Electrochemical Nomenclature",
            "Journal of Electroanalytical Chemistry (peer-reviewed methods)"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.ELECTROCHEMISTRY
    ),

    # === TITRATION & GRAVIMETRIC ===
    DoctrineBlock(
        topic="Acid-Base Titration",
        keywords=["titration", "acid-base", "equivalence point", "indicator", "pH curve", "neutralization"],
        conclusion_template=[
            "Acid-base titration determines analyte concentration via neutralization reaction with standard titrant.",
            "Equivalence point occurs when moles acid = moles base; endpoint detected by indicator or pH meter.",
            "Titration curve shape depends on strength of acid and base: strong-strong has sharp inflection at pH 7."
        ],
        reasoning_framework="""
Acid-base titration theory and practice:
1. Strong acid-strong base: equivalence point pH = 7, large pH jump (4-10), any indicator in range works
2. Weak acid-strong base: equivalence point pH > 7, use phenolphthalein (8.0-10.0)
3. Weak base-strong acid: equivalence point pH < 7, use methyl orange (3.1-4.4)
4. Polyprotic acids: multiple equivalence points, titrate stepwise if pKa difference ≥4
5. Buffer region: pH = pKa ± 1, maximum buffering capacity at pKa
6. Indicator selection: transition range within 1 pH unit of equivalence point
7. Standardization: primary standards (KHP for bases, Na2CO3 for acids) with high purity
8. Titrant preparation: standardize against primary standard, calculate molarity
9. Buret technique: rinse with titrant, eliminate air bubbles, read meniscus at eye level
10. Blank titration: corrects for CO2 absorption, impurities in water
        """,
        key_factors=[
            "Primary standard purity and drying conditions",
            "Standardization replicates for precision assessment",
            "Indicator blank correction for volume consumed",
            "Carbon dioxide exclusion for carbonate-free NaOH",
            "Sample size appropriate for titrant volume (20-40 mL)",
            "Titration rate near endpoint (drop-wise addition)",
            "Temperature control for accurate volume measurement"
        ],
        primary_authority=[
            "ASTM E200: Standard Practice for Acid-Base Titration",
            "USP <541> Titrimetry",
            "AOAC Official Methods for Acidity/Alkalinity"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.TITRATION
    ),

    DoctrineBlock(
        topic="Redox and Complexometric Titration",
        keywords=["redox titration", "complexometric", "EDTA", "permanganate", "iodometry", "chelate"],
        conclusion_template=[
            "Redox titrations use change in oxidation state; equivalence point detected by color change or potentiometry.",
            "Complexometric titrations with EDTA determine metal ions via 1:1 chelate formation.",
            "Standardization and pH control are critical for accurate results."
        ],
        reasoning_framework="""
Advanced titration methods:
1. Redox titrations: electron transfer at equivalence point, nEoxidant = nEreductant
2. Permanganate titrations: KMnO4 is self-indicating (purple to colorless), oxidizes in acidic medium
3. Iodometric titrations: I2 + starch indicator (blue complex), indirect for oxidizing agents
4. Cerimetric titrations: Ce⁴⁺ strong oxidant, no self-indication, use ferroin indicator
5. Dichromate titrations: K2Cr2O7 primary standard, used for Fe²⁺ determination
6. EDTA complexometry: forms 1:1 chelate with most metal ions regardless of charge
7. Metal indicators: Eriochrome Black T (EBT) for Ca²⁺/Mg²⁺, change color when EDTA displaces metal
8. pH control: EDTA complexation strength increases with pH, buffer to optimal range
9. Masking agents: prevent interference by selective complexation (cyanide masks Cu, Zn)
10. Back titration: excess EDTA added, unreacted titrated with metal standard
        """,
        key_factors=[
            "Standardization of permanganate against oxalic acid or As2O3",
            "Acidification for redox reactions (H2SO4 preferred over HCl)",
            "Temperature control for permanganate titrations (55-60°C)",
            "Starch indicator addition near endpoint in iodometry",
            "Buffer pH for EDTA titrations (ammonia buffer for Ca/Mg)",
            "Indicator blank determination for complexometric methods",
            "Titration speed to allow equilibration of complexation"
        ],
        primary_authority=[
            "ASTM D1126: Water Hardness by EDTA Titration",
            "ASTM E200: Redox Titration Methods",
            "AOAC Official Method 920.196: Iodine Number of Fats"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.TITRATION
    ),

    DoctrineBlock(
        topic="Gravimetric Analysis",
        keywords=["gravimetric", "precipitation", "volatilization", "drying", "crucible", "mass measurement"],
        conclusion_template=[
            "Gravimetric analysis determines analyte concentration by measuring mass of pure product formed.",
            "Precipitation methods require low solubility precipitate, specific for analyte, easily filtered and dried.",
            "Crucible preparation, drying to constant weight, and weighing technique are critical for accuracy."
        ],
        reasoning_framework="""
Gravimetric analysis methodology:
1. Precipitation gravimetry: analyte converted to insoluble compound, filtered, dried, weighed
2. Ideal precipitate properties: low solubility (Ksp <10⁻⁸), large particle size (easy filtration), pure composition, stable composition
3. Precipitation conditions: hot dilute solutions, slow addition with stirring, digestion (Ostwald ripening)
4. Coprecipitation errors: surface adsorption, occlusion, mixed crystal formation
5. Washing precipitate: remove soluble impurities without dissolving precipitate (use dilute electrolyte)
6. Drying vs ignition: 110°C for hydrated salts, 500-1000°C for oxides/sulfates
7. Constant weight criterion: successive weighings agree within 0.5 mg
8. Analytical balance: 0.1 mg precision, calibration with certified masses
9. Volatilization gravimetry: moisture, ash content, volatile components driven off by heat
10. Calculation: gravimetric factor converts precipitate mass to analyte mass
        """,
        key_factors=[
            "Crucible pre-treatment (cleaning, ignition to constant weight)",
            "Precipitate formation conditions (pH, temperature, reagent excess)",
            "Digestion time for improved particle size (30-60 min)",
            "Filter paper selection (ashless for ignition methods)",
            "Drying temperature and time to avoid decomposition",
            "Desiccator cooling before weighing to prevent moisture absorption",
            "Multiple determinations for precision (RSD <0.2% achievable)"
        ],
        primary_authority=[
            "ASTM E1131: Compositional Analysis by Thermogravimetry",
            "AOAC Official Methods for Ash and Moisture",
            "USP <731> Loss on Drying"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.GRAVIMETRIC
    ),

    # === QUALITY ASSURANCE ===
    DoctrineBlock(
        topic="Method Validation Parameters",
        keywords=["validation", "LOD", "LOQ", "linearity", "precision", "accuracy", "robustness"],
        conclusion_template=[
            "Analytical method validation demonstrates that method is suitable for intended purpose.",
            "ICH Q2(R1) defines validation parameters: specificity, linearity, accuracy, precision, LOD, LOQ, range, robustness.",
            "Acceptance criteria depend on application: pharmaceuticals require tighter limits than environmental methods."
        ],
        reasoning_framework="""
Comprehensive method validation protocol:
1. Specificity/Selectivity: demonstrates method measures only analyte, no interference from matrix
2. Linearity: correlation coefficient r² ≥0.995, residuals random, back-calculated concentrations within ±15%
3. Range: concentration interval where linearity/precision/accuracy meet requirements (typically LOQ to 120% spec)
4. Accuracy (trueness): recovery of known amount, certified reference material (CRM), spike recovery 85-115%
5. Precision: repeatability (same day, same analyst), intermediate (different days/analysts), reproducibility (different labs)
   - RSD ≤2% for major components, ≤5% for trace, ≤20% at LOQ
6. LOD (Limit of Detection): 3.3σ/S, where σ = standard deviation of blank, S = slope of calibration
7. LOQ (Limit of Quantitation): 10σ/S, or lowest concentration with RSD ≤10% and accuracy 80-120%
8. Robustness: deliberate variation of parameters (pH ±0.2, temperature ±5°C, flow rate ±10%) shows method stability
9. System suitability: daily verification that system performs adequately (resolution, tailing, retention time)
10. Measurement uncertainty: combined standard uncertainty from all sources (calibration, repeatability, recovery)
        """,
        key_factors=[
            "Sample matrix matching for recovery studies",
            "Minimum 6 concentration levels for linearity (LOQ to 120%)",
            "Replication: 3 concentrations × 3 replicates minimum for precision",
            "Blank subtraction for trace analysis LOD/LOQ",
            "Statistical tests: ANOVA for precision, t-test for accuracy",
            "Outlier detection and handling (Grubbs' test, Dixon's Q-test)",
            "Documentation of validation protocol and acceptance criteria before study"
        ],
        primary_authority=[
            "ICH Q2(R1): Validation of Analytical Procedures",
            "FDA Bioanalytical Method Validation Guidance (2018)",
            "ISO/IEC 17025: General Requirements for Competence of Testing Labs"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.METHOD_VALIDATION
    ),

    DoctrineBlock(
        topic="Quality Control and Statistical Analysis",
        keywords=["QC", "control chart", "standard deviation", "confidence interval", "t-test", "outliers"],
        conclusion_template=[
            "Quality control ensures analytical results meet accuracy and precision requirements through statistical monitoring.",
            "Control charts (Shewhart, CUSUM) detect trends and out-of-control conditions in real-time.",
            "Statistical tests validate method performance and identify significant differences between results."
        ],
        reasoning_framework="""
Statistical quality control in analytical chemistry:
1. Control charts: plot QC sample results vs time, action limits at mean ±3SD (99.7% confidence)
2. Westgard rules: multirule QC decision criteria (1-3s, 2-2s, R-4s, 4-1s, 10-x)
3. QC sample types: reagent blank, method blank, calibration verification, duplicate, matrix spike, CRM
4. Frequency: minimum 1 per batch, 5-10% of samples, each analytical run
5. Acceptance criteria: QC within ±2SD or specified % of true value
6. Corrective action: investigate when QC fails, recalibrate, reanalyze affected samples
7. Precision metrics: standard deviation (s), relative standard deviation (RSD%), coefficient of variation (CV%)
8. Accuracy metrics: % recovery, bias (measured - true), % error
9. Significant figures: report results with precision matching uncertainty
10. Confidence intervals: 95% CI = mean ± t(α,df) × s/√n
        """,
        key_factors=[
            "QC sample concentration near decision level or mid-range",
            "Control limits established from minimum 20 independent measurements",
            "Random vs systematic errors distinguished by control chart patterns",
            "Propagation of error for calculated results",
            "Degrees of freedom for t-distribution selection",
            "Homogeneity and stability of QC materials",
            "Blind QC samples for analyst proficiency testing"
        ],
        primary_authority=[
            "ISO Guide 98-3: Uncertainty of Measurement (GUM)",
            "CLSI C24-Ed4: Statistical Quality Control",
            "ASTM E2554: Estimation and Monitoring of Uncertainty"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.QUALITY_ASSURANCE
    ),

    DoctrineBlock(
        topic="Good Laboratory Practices and Compliance",
        keywords=["GLP", "21 CFR 58", "documentation", "SOP", "audit trail", "CAPA"],
        conclusion_template=[
            "Good Laboratory Practice (GLP) ensures quality and integrity of nonclinical safety studies through organizational processes and conditions.",
            "21 CFR Part 58 (FDA) and OECD GLP Principles define requirements for facilities, personnel, equipment, SOPs, and documentation.",
            "Compliance demonstrated through written procedures, training records, instrument qualification, and audit trails."
        ],
        reasoning_framework="""
GLP compliance framework:
1. Organization: management responsibilities, quality assurance unit (QAU) independence, study director accountability
2. Personnel: education/training/experience documented, job descriptions, training records, competency assessment
3. Facilities: adequate space, separate areas for test systems, archive for records, waste disposal
4. Equipment: design/capacity adequate, maintenance/calibration schedules, standard operating procedures (SOPs)
5. Testing facilities operation: SOPs for all procedures, reagent characterization, animal care (if applicable)
6. Test and control articles: identity/strength/purity/composition characterized, stability determined, storage conditions
7. Protocol and conduct of study: written protocol approved before initiation, deviations documented, data integrity
8. Records and reports: raw data retained, reports signed by study director, amendments documented
9. Quality assurance program: inspections of studies, audits of final reports, findings communicated
10. Computer systems: 21 CFR Part 11 electronic records/signatures, audit trails, access controls, validation
        """,
        key_factors=[
            "Master schedule of ongoing studies maintained",
            "SOPs written, approved, version-controlled, accessible",
            "Equipment qualification: IQ (installation), OQ (operation), PQ (performance)",
            "Calibration traceable to national/international standards",
            "Raw data retention per regulatory requirements (FDA 2 years after filing)",
            "Deviation and CAPA (Corrective and Preventive Action) systems",
            "Periodic internal audits and management review"
        ],
        primary_authority=[
            "21 CFR Part 58: Good Laboratory Practice for Nonclinical Studies",
            "OECD Principles of Good Laboratory Practice",
            "ISO/IEC 17025: General Requirements for Testing and Calibration Labs"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.COMPLIANCE
    ),

    # === CALIBRATION ===
    DoctrineBlock(
        topic="Calibration Methods and Standards",
        keywords=["calibration", "standard curve", "internal standard", "external standard", "standard addition", "matrix matching"],
        conclusion_template=[
            "Calibration establishes relationship between instrument signal and analyte concentration.",
            "External standard calibration uses separate standards; internal standard corrects for injection variability.",
            "Standard addition method compensates for matrix effects when standards cannot match sample matrix."
        ],
        reasoning_framework="""
Calibration strategies for quantitative analysis:
1. External standard: plot signal vs concentration, determine unknowns from curve
   - Requires matrix matching or matrix-free standards if no matrix effect
   - Minimum 5 concentration levels spanning expected range
   - Replicate standards at each level (duplicate minimum)
2. Internal standard: add constant amount of IS to all standards and samples
   - Plot signal ratio (analyte/IS) vs concentration ratio
   - Corrects for injection volume, extraction efficiency, detector drift
   - IS must not be present in sample, similar properties to analyte, not interfere
3. Standard addition: spike sample with known analyte amounts, extrapolate to zero addition
   - y-intercept / slope = original concentration
   - Compensates for matrix enhancement or suppression
   - Requires linear response, minimum 3-4 addition levels
4. Bracketing: analyze standards before and after samples, interpolate for drift correction
5. Single-point calibration: acceptable only if response linear and through origin (rarely true)
6. Calibration verification: independent standard (second source) confirms accuracy
7. Calibration curve evaluation: r² ≥0.995, residual plot random, QC standards within ±15%
8. Recalibration frequency: daily for drift-prone methods, each sequence, after maintenance
9. Matrix-matched standards: prepare standards in blank matrix to match sample
10. Certified reference materials (CRM): NIST SRMs, proficiency testing samples for validation
        """,
        key_factors=[
            "Calibration range encompasses all sample concentrations",
            "Weighting for heteroscedastic data (1/x, 1/x²)",
            "Blank subtraction before calculating concentrations",
            "Carryover check with high-low-blank sequence",
            "IS concentration similar to analyte for optimal precision",
            "Standard stability (refrigeration, protection from light)",
            "Traceability chain to SI units via certified standards"
        ],
        primary_authority=[
            "ISO/IEC Guide 98-3: Measurement Uncertainty",
            "EURACHEM Guide: Quantifying Uncertainty in Analytical Measurement",
            "ASTM E1655: Infrared Multivariate Quantitative Analysis"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CALIBRATION
    ),

    # === ATOMIC SPECTROSCOPY ===
    DoctrineBlock(
        topic="Atomic Absorption Spectroscopy",
        keywords=["AAS", "atomic absorption", "flame", "graphite furnace", "hollow cathode lamp", "atomization"],
        conclusion_template=[
            "AAS measures absorption of light by free atoms in gaseous state, highly selective for elemental analysis.",
            "Flame AAS (FAAS) for mg/L levels; graphite furnace AAS (GFAAS) for μg/L with improved sensitivity.",
            "Matrix modifiers, background correction, and calibration with matrix-matched standards minimize interferences."
        ],
        reasoning_framework="""
Atomic absorption spectroscopy principles:
1. Atomization methods: flame (air-acetylene, N2O-acetylene), graphite furnace (electrothermal), hydride generation, cold vapor (Hg)
2. Hollow cathode lamp (HCL): element-specific light source, narrow emission line matching absorption line
3. Flame AAS: sample nebulized into flame, atoms absorb resonance radiation, Beer's law applies
4. GFAAS: sample dried, ashed, atomized in graphite tube, transient signal, temperature program optimization
5. Chemical interferences: formation of refractory compounds (PO4³⁻ with Ca), use of releasing agents (La, Sr)
6. Ionization interference: low ionization potential elements (Na, K) in hot flames, add ionization suppressant (Cs, La)
7. Spectral interferences: rare due to narrow line widths, overlap corrected by background correction
8. Background correction methods: deuterium lamp, Zeeman effect, Smith-Hieftje
9. Matrix modifiers (GFAAS): Pd-Mg, NH4H2PO4 stabilize analyte during ashing, remove matrix
10. Detection limits: FAAS ~0.001-1 mg/L, GFAAS ~0.00001-0.1 mg/L
        """,
        key_factors=[
            "HCL current optimization for intensity without self-reversal",
            "Flame type selection based on element (oxidizing vs reducing)",
            "Burner height adjustment for maximum absorbance",
            "Graphite furnace temperature program (dry, ash, atomize, clean)",
            "Sample dilution to minimize matrix effects and extend linear range",
            "Nitric acid matrix for most metals (1-5% HNO3)",
            "Calibration in same acid and matrix as samples"
        ],
        primary_authority=[
            "EPA Method 7000B: Atomic Absorption Methods",
            "ASTM D4691: Water Analysis by GFAAS",
            "Standard Methods 3111: Metals by AAS"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ATOMIC_METHODS
    ),

    DoctrineBlock(
        topic="Inductively Coupled Plasma Spectroscopy",
        keywords=["ICP", "ICP-OES", "ICP-MS", "plasma", "multi-element", "argon", "mass spectrometry"],
        conclusion_template=[
            "ICP-OES measures element-specific emission from atoms/ions in argon plasma (6000-8000 K).",
            "ICP-MS detects ions by mass-to-charge ratio, superior sensitivity (ng/L to pg/L) and multi-element capability.",
            "Sample introduction, plasma conditions, and interference correction are critical for accurate results."
        ],
        reasoning_framework="""
ICP spectroscopy for trace elemental analysis:
1. ICP-OES: sample nebulized into argon plasma, atoms/ions emit characteristic wavelengths, intensity proportional to concentration
2. ICP-MS: ions extracted from plasma into mass spectrometer, quadrupole or TOF analyzer, counts per second measured
3. Sample introduction: pneumatic nebulizer (most common), ultrasonic nebulizer (improved sensitivity), direct injection (slurries)
4. Plasma power: 1-1.5 kW RF power, self-sustaining plasma via inductive coupling
5. Wavelength selection (OES): avoid spectral overlaps, use alternate lines, background correction
6. Isotope selection (MS): choose abundant isotope free from isobaric interferences
7. Spectroscopic interferences (OES): line overlap, background emission, corrected by inter-element correction
8. Isobaric interferences (MS): same m/z (40Ar+ on 40Ca+, 40ArO+ on 56Fe+), use collision/reaction cell or high resolution
9. Polyatomic interferences (MS): argon-based (ArO+, ArH+), corrected by collision cell with He/H2
10. Internal standardization: multi-element IS (Sc, Y, In, Bi) corrects for matrix suppression, drift
        """,
        key_factors=[
            "Sample dilution to <0.2% total dissolved solids (TDS) for ICP-MS",
            "Acid concentration matched between standards and samples (2-5% HNO3)",
            "Peristaltic pump tubing: Tygon for aqueous, Viton for organics",
            "Plasma viewing: axial (higher sensitivity) vs radial (less interference)",
            "Collision/reaction cell gases: He (kinetic energy discrimination), H2 (chemical reaction)",
            "Mass calibration and tuning for resolution and sensitivity",
            "Rinse blank between samples to prevent carryover"
        ],
        primary_authority=[
            "EPA Method 6010D: ICP-OES for Metals",
            "EPA Method 6020B: ICP-MS for Trace Elements",
            "ASTM D5185: Multi-element Analysis by ICP-OES"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ATOMIC_METHODS
    ),

    # === SAMPLING & SAMPLE PREP ===
    DoctrineBlock(
        topic="Sampling Theory and Representative Sampling",
        keywords=["sampling", "representative", "homogeneous", "heterogeneous", "composite", "sample size"],
        conclusion_template=[
            "Representative sampling ensures sample composition reflects population being measured.",
            "Sampling error minimized by random sampling, adequate sample size, and proper preservation.",
            "Heterogeneous materials require larger samples or composite sampling to reduce variance."
        ],
        reasoning_framework="""
Sampling strategies for analytical chemistry:
1. Sampling theory (Gy's theory): total sampling error = sampling error + analytical error
2. Fundamental sampling error: inherent heterogeneity of material, reduced by larger sample mass
3. Sample size determination: variance, confidence level, acceptable error determine minimum mass/volume
4. Random vs systematic sampling: random eliminates bias, systematic (grid) ensures coverage
5. Composite sampling: combine aliquots from multiple locations/times, reduces cost, averages variability
6. Stratified sampling: divide population into strata, sample proportionally from each
7. Preservation techniques: refrigeration, acidification (pH <2), chemical preservatives (no headspace for volatiles)
8. Holding times: EPA maximum holding times (e.g., nutrients 48h, metals 6 months, volatiles 14 days)
9. Chain of custody: documentation of sample handling from collection to disposal
10. Sample preparation: filtration, extraction, digestion, dilution, derivatization before analysis
        """,
        key_factors=[
            "Sampling plan design before collection (objectives, locations, frequency)",
            "Container material compatible with analytes (glass for organics, plastic for metals)",
            "Pre-cleaning of containers (acid wash for metals, solvent rinse for organics)",
            "Headspace minimization for volatile analytes",
            "Temperature control during transport (coolers with ice)",
            "Field blanks, equipment blanks, trip blanks for contamination assessment",
            "Homogenization of sample before aliquoting for analysis"
        ],
        primary_authority=[
            "EPA SESDPROC-111-R3: Environmental Sampling SOPs",
            "ISO 10381: Soil Sampling Guidance",
            "ASTM D3694: Water Sampling Standard Practices"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SAMPLING
    ),

    DoctrineBlock(
        topic="Sample Preparation and Extraction",
        keywords=["extraction", "SPE", "LLE", "digestion", "derivatization", "cleanup", "concentration"],
        conclusion_template=[
            "Sample preparation isolates analytes from matrix, concentrates to detectable levels, and removes interferences.",
            "Solid-phase extraction (SPE) and liquid-liquid extraction (LLE) separate analytes based on partitioning.",
            "Digestion converts samples to analyzable form; derivatization improves detection or separation."
        ],
        reasoning_framework="""
Sample preparation techniques:
1. Solid-phase extraction (SPE): analyte binds to solid sorbent, matrix washed away, eluted with strong solvent
   - Sorbent selection: C18 (nonpolar), silica (polar), ion exchange (charged), mixed-mode
   - Conditioning, load, wash, elute steps require optimization
   - Breakthrough volume: maximum sample volume before analyte loss
2. Liquid-liquid extraction (LLE): analyte partitions between immiscible solvents based on polarity
   - Distribution coefficient K = [analyte]organic / [analyte]aqueous
   - Multiple extractions more efficient than single large volume
   - Salting out, pH adjustment optimize extraction efficiency
3. Acid digestion: microwave (closed vessel, high pressure/temperature), hotplate (open vessel, atmospheric)
   - HNO3 (oxidizing), HCl (complexing), HF (silicates), HClO4 (organics with caution)
   - EPA Method 3051A (microwave), Method 3050B (hotplate) for metals
4. Derivatization: improve volatility (GC), enhance detection (fluorescence), stabilize analytes
   - Silylation (TMS, BSTFA) for alcohols, amines, carboxylic acids
   - Alkylation (methyl, ethyl esters) for acidic compounds
   - Acylation (MSTFA, BSTFA) for amines, amino acids
5. Cleanup: remove co-extracted matrix components that interfere
   - Gel permeation chromatography (GPC) for lipid removal
   - Florisil, alumina for pigment removal
   - Sulfur removal for pesticide analysis
6. Concentration: rotary evaporation, nitrogen blowdown, lyophilization
   - Avoid complete dryness for volatile analytes, reconstitute in known volume
        """,
        key_factors=[
            "Recovery studies with spiked samples to validate extraction",
            "Solvent compatibility with detection method (UV-transparent for HPLC)",
            "pH optimization for ionizable compounds",
            "Temperature and time control for digestion completeness",
            "Blank digestion to assess reagent contamination",
            "Evaporation temperature below analyte boiling point",
            "Reconstitution solvent strength weaker than mobile phase"
        ],
        primary_authority=[
            "EPA Method 3500: Organic Extraction Methods",
            "EPA Method 3051A: Microwave Acid Digestion",
            "AOAC Official Methods for Sample Preparation"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SAMPLE_PREP
    ),

    # === APPLICATIONS ===
    DoctrineBlock(
        topic="Environmental Analysis Methods",
        keywords=["environmental", "water quality", "soil", "air", "EPA method", "pollutants", "contaminants"],
        conclusion_template=[
            "Environmental analysis determines pollutants in water, air, soil to ensure regulatory compliance.",
            "EPA methods specify sample collection, preservation, preparation, analysis, and QC requirements.",
            "Detection limits, matrix complexity, and regulatory reporting limits drive method selection."
        ],
        reasoning_framework="""
Environmental analytical chemistry:
1. Water analysis: EPA 500 series (organics), 6000 series (metals), 300 series (inorganics), 1600 series (microbiology)
2. Soil/solid waste: EPA 3000 series (preparation), 8000 series (organics), 6000 series (metals)
3. Air analysis: EPA TO series (toxic organics), IP series (inorganic pollutants), CTM series (continuous monitoring)
4. Priority pollutants: 126 EPA-listed compounds in Clean Water Act, routine monitoring required
5. Drinking water: Safe Drinking Water Act MCLs (maximum contaminant levels), required monitoring frequency
6. Wastewater: NPDES permits specify discharge limits, self-monitoring requirements
7. VOCs (volatile organic compounds): purge and trap GC-MS, Method 524.2 (drinking water), Method 8260 (soil/water)
8. SVOCs (semivolatile organic compounds): extraction + GC-MS, Method 525.2 (water), Method 8270 (soil)
9. Pesticides/herbicides: extraction + GC-ECD or GC-MS, Method 508.1 (organophosphorus), Method 8081 (organochlorine)
10. Metals: ICP-MS (Method 200.8), ICP-OES (Method 200.7), GFAAS (Method 200.9)
        """,
        key_factors=[
            "Method detection limit (MDL) must be below regulatory limit",
            "Sample preservation prevents biodegradation or chemical change",
            "Holding time compliance from collection to analysis",
            "Surrogate standards assess matrix effects and extraction efficiency",
            "Laboratory fortified blank (LFB) and matrix spike (MS/MSD) for QC",
            "Proficiency testing samples for external QC verification",
            "Data reporting with qualifiers (J for estimated, U for non-detect)"
        ],
        primary_authority=[
            "EPA SW-846: Test Methods for Solid Waste",
            "EPA 600 Series: Water Analysis Methods",
            "Standard Methods for Examination of Water and Wastewater"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.APPLICATION
    ),

    DoctrineBlock(
        topic="Pharmaceutical and Clinical Analysis",
        keywords=["pharmaceutical", "drug", "USP", "dissolution", "assay", "impurities", "clinical chemistry"],
        conclusion_template=[
            "Pharmaceutical analysis ensures drug products meet identity, strength, quality, and purity specifications.",
            "USP methods define compendial procedures; ICH guidelines harmonize validation globally.",
            "Clinical chemistry analyzes biological fluids for disease diagnosis and monitoring."
        ],
        reasoning_framework="""
Pharmaceutical and clinical analytical methods:
1. Identity testing: IR, UV, HPLC retention time, MS fragmentation pattern
2. Assay (potency): quantify active ingredient(s), typically 95-105% of label claim
3. Impurities: related substances (degradation products, synthetic impurities), residual solvents, heavy metals
   - Reporting threshold: 0.05%, identification threshold: 0.1%, qualification threshold: varies by dose
4. Dissolution testing: USP Apparatus 1 (basket) or 2 (paddle), measure drug release over time
   - Specifications: Q value (% dissolved at specified time), multi-point profile for modified release
5. Content uniformity: dose-to-dose consistency, 10 units tested, acceptance value (AV) ≤15
6. Stability studies: ICH Q1A guidelines, accelerated (40°C/75% RH) and long-term (25°C/60% RH)
7. Clinical chemistry: glucose, cholesterol, enzymes (AST, ALT), electrolytes (Na, K, Cl)
   - Point-of-care vs central lab, CLIA regulations for quality
8. Therapeutic drug monitoring (TDM): measure drug concentrations in blood to optimize dosing
   - Narrow therapeutic index drugs (digoxin, lithium, immunosuppressants)
9. Bioanalysis: pharmacokinetics, bioequivalence studies, LC-MS/MS for sensitivity
10. Cleaning validation: swab sampling, TOC (total organic carbon), conductivity for residue limits
        """,
        key_factors=[
            "Compendial vs non-compendial methods (USP reference standards)",
            "Forced degradation studies to demonstrate stability-indicating methods",
            "System suitability testing before sample analysis (tailing factor, resolution, RSD)",
            "Reference standard qualification and certificate of analysis",
            "Specificity for excipients and degradation products",
            "Biological matrix effects (protein binding, ion suppression)",
            "Regulatory submission requirements (eCTD format, ANDA, NDA)"
        ],
        primary_authority=[
            "USP <1225> Validation of Compendial Procedures",
            "ICH Q2(R1) Validation of Analytical Procedures",
            "21 CFR Part 211: Current Good Manufacturing Practice"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.APPLICATION
    ),

    DoctrineBlock(
        topic="Food and Agricultural Analysis",
        keywords=["food", "agricultural", "pesticide residue", "nutrition", "AOAC", "adulteration", "contamination"],
        conclusion_template=[
            "Food analysis ensures safety, quality, and label compliance for nutritional content and contaminants.",
            "AOAC International provides validated methods for food composition and residue analysis.",
            "Multi-residue methods screen for hundreds of pesticides; targeted methods confirm and quantify."
        ],
        reasoning_framework="""
Food and agricultural analytical chemistry:
1. Proximate analysis: moisture (oven drying, Karl Fischer), ash (muffle furnace), protein (Kjeldahl, Dumas), fat (Soxhlet, Mojonnier), carbohydrate (by difference)
2. Nutritional labeling: FDA Nutrition Facts, vitamins (HPLC), minerals (ICP-OES), fatty acids (GC-FID)
3. Pesticide residues: QuEChERS (quick, easy, cheap, effective, rugged, safe) extraction, GC-MS/MS or LC-MS/MS
   - Multi-residue methods: screen 200+ pesticides, confirmatory analysis by MS/MS
   - Maximum residue limits (MRL): Codex, EPA tolerance levels
4. Mycotoxins: aflatoxin, ochratoxin, fumonisin, deoxynivalenol via HPLC-fluorescence or LC-MS/MS
5. Adulterants: economic adulteration (olive oil purity by fatty acid profile), melamine in milk (LC-MS/MS)
6. Allergens: ELISA for milk, egg, peanut, soy, gluten proteins
7. Microbial contamination: plate count, PCR for pathogens (Salmonella, E. coli O157:H7, Listeria)
8. Antibiotics/veterinary drug residues: LC-MS/MS for multi-class screening
9. Heavy metals: ICP-MS for Pb, Cd, As, Hg in food (EPA Method 6020B adapted)
10. GMO detection: PCR for transgenic DNA sequences (CaMV 35S promoter, NOS terminator)
        """,
        key_factors=[
            "Representative sampling of heterogeneous food matrices",
            "Homogenization (grinding, blending) before analysis",
            "Fat removal for pesticide analysis in high-fat foods",
            "Matrix-matched calibration for complex food extracts",
            "Cleanup with dispersive SPE (dSPE) for QuEChERS",
            "Confirmation with second column or MS/MS transition",
            "Proficiency testing (FAPAS, AOAC-CAEAL) for laboratory competence"
        ],
        primary_authority=[
            "AOAC Official Methods of Analysis",
            "FDA Pesticide Analytical Manual (PAM)",
            "Codex Alimentarius Commission Guidelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.APPLICATION
    ),

    DoctrineBlock(
        topic="Forensic Chemistry and Toxicology",
        keywords=["forensic", "toxicology", "drug screening", "gunshot residue", "trace evidence", "chain of custody"],
        conclusion_template=[
            "Forensic chemistry applies analytical techniques to legal questions: drug identification, toxicology, trace evidence.",
            "Chain of custody documentation maintains evidence integrity for court admissibility.",
            "Confirmation with second independent technique (GCMS after immunoassay) is standard practice."
        ],
        reasoning_framework="""
Forensic analytical chemistry:
1. Drug identification: presumptive tests (color, crystal), confirmatory (GC-MS, IR, NMR)
   - Controlled substances: SWGDRUG recommendations for Category A/B/C techniques
2. Toxicology screening: immunoassay (ELISA, CEDIA) for rapid screening, GC-MS or LC-MS/MS confirmation
   - Drugs of abuse: amphetamines, opiates, cannabinoids, cocaine, PCP, benzodiazepines
   - Cutoff concentrations: workplace (50 ng/mL THC-COOH), clinical, forensic (may differ)
3. Blood alcohol: headspace GC-FID, enzymatic methods, legal limits (0.08% in most US states)
4. Postmortem toxicology: interpretation complicated by redistribution, putrefaction
5. Gunshot residue (GSR): SEM-EDS for Pb, Ba, Sb particle identification
6. Trace evidence: fibers (microscopy, IR), glass (refractive index), paint (pyrolysis GC-MS)
7. Arson investigation: fire debris analysis for ignitable liquid residues (GC-MS)
8. Explosives: ion mobility spectrometry (IMS), GC-ECD, LC-MS for nitroaromatics, peroxides
9. DNA analysis: PCR-STR typing (not traditional analytical chemistry but integral to forensics)
10. Questioned documents: ink analysis (HPLC), paper analysis (SEM, XRF)
        """,
        key_factors=[
            "Chain of custody form with every transfer, sealed evidence bags",
            "Tamper-evident seals on all evidence containers",
            "Two-analyst verification for controlled substance identification",
            "Cutoff confirmation: screening positive confirmed by quantitative method",
            "Reference standards from DEA or commercial sources with CoA",
            "Retention of evidence and extracts per jurisdiction requirements",
            "Expert witness testimony: method validation, results interpretation, limitations"
        ],
        primary_authority=[
            "SWGDRUG Recommendations (Scientific Working Group for Drug Analysis)",
            "SOFT/AAFS Guidelines for Forensic Toxicology",
            "NIJ (National Institute of Justice) Forensic Science Standards"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.APPLICATION
    )
]

# ============================================================================
# ENGINE CORE
# ============================================================================

class CHEM03Engine:
    """Analytical Chemistry Intelligence Engine"""

    def __init__(self):
        self.cache = {d.topic: d for d in DOCTRINE_CACHE}
        self.metrics = {
            "queries": 0,
            "cache_hits": 0,
            "latencies": [],
            "errors": defaultdict(int)
        }
        self.coverage_map = defaultdict(int)
        self.drift_log = []

        logger.info(f"CHEM03 Engine initialized with {len(DOCTRINE_CACHE)} doctrine blocks")

    def query(self, query_text: str, mode: ResponseMode = ResponseMode.FAST, context: Optional[Dict] = None) -> QueryResponse:
        """Main query interface"""
        start_time = time.time()
        self.metrics["queries"] += 1

        try:
            # Match doctrines
            triggered = self._match_doctrines(query_text, context or {})

            if not triggered:
                return self._fallback_response(query_text, mode, start_time)

            # Build response based on mode
            if mode == ResponseMode.FAST:
                response_text = self._fast_response(triggered)
            elif mode == ResponseMode.DEFENSE:
                response_text = self._defense_response(triggered, query_text)
            else:  # MEMO
                response_text = self._memo_response(triggered, query_text)

            # Extract reasoning chain
            reasoning_chain = [d.reasoning_framework[:200] + "..." for d in triggered[:3]]

            # Calculate determinism hash
            hash_input = query_text + mode.value + "".join([d.topic for d in triggered])
            det_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

            latency = (time.time() - start_time) * 1000
            self.metrics["latencies"].append(latency)

            # Update coverage
            for doctrine in triggered:
                self.coverage_map[doctrine.topic] += 1

            return QueryResponse(
                query=query_text,
                response=response_text,
                mode=mode,
                confidence=triggered[0].confidence if triggered else ConfidenceLevel.DISCLOSURE,
                doctrines_triggered=[d.topic for d in triggered],
                reasoning_chain=reasoning_chain,
                determinism_hash=det_hash,
                latency_ms=round(latency, 2),
                timestamp=datetime.utcnow().isoformat() + "Z"
            )

        except Exception as e:
            logger.error(f"Query failed: {e}")
            self.metrics["errors"]["query_failure"] += 1
            raise HTTPException(status_code=500, detail=str(e))

    def _match_doctrines(self, query: str, context: Dict) -> List[DoctrineBlock]:
        """Match query to doctrine blocks"""
        query_lower = query.lower()
        matches = []

        for doctrine in DOCTRINE_CACHE:
            score = 0
            for keyword in doctrine.keywords:
                if keyword.lower() in query_lower:
                    score += 2

            # Context boosting
            if context.get("category") and doctrine.category.value.lower() in str(context.get("category")).lower():
                score += 5

            if score > 0:
                matches.append((score, doctrine))

        matches.sort(reverse=True, key=lambda x: x[0])
        return [m[1] for m in matches[:5]]

    def _fast_response(self, doctrines: List[DoctrineBlock]) -> str:
        """Concise response mode"""
        primary = doctrines[0]
        response_parts = primary.conclusion_template[:2]

        if len(doctrines) > 1:
            response_parts.append(f"Related considerations: {doctrines[1].topic}")

        return " ".join(response_parts)

    def _defense_response(self, doctrines: List[DoctrineBlock], query: str) -> str:
        """Audit-ready response with full reasoning"""
        primary = doctrines[0]

        response = f"ANALYTICAL CHEMISTRY ANALYSIS\n\n"
        response += f"Query: {query}\n\n"
        response += "CONCLUSION:\n" + "\n".join(f"• {c}" for c in primary.conclusion_template) + "\n\n"
        response += "REASONING FRAMEWORK:\n" + primary.reasoning_framework + "\n\n"
        response += "KEY FACTORS:\n" + "\n".join(f"• {f}" for f in primary.key_factors) + "\n\n"
        response += "AUTHORITATIVE REFERENCES:\n" + "\n".join(f"• {a}" for a in primary.primary_authority) + "\n\n"

        if primary.adversarial_considerations:
            response += "ADVERSARIAL CONSIDERATIONS:\n" + "\n".join(f"• {a}" for a in primary.adversarial_considerations) + "\n\n"

        if primary.common_errors:
            response += "COMMON ERRORS TO AVOID:\n" + "\n".join(f"• {e}" for e in primary.common_errors) + "\n\n"

        response += f"Confidence Level: {primary.confidence.value}\n"
        response += f"Category: {primary.category.value}"

        return response

    def _memo_response(self, doctrines: List[DoctrineBlock], query: str) -> str:
        """Full documentation mode"""
        response = f"ANALYTICAL CHEMISTRY TECHNICAL MEMORANDUM\n"
        response += "=" * 80 + "\n\n"
        response += f"Subject: {query}\n"
        response += f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}\n"
        response += f"Doctrines Applied: {len(doctrines)}\n\n"

        for idx, doctrine in enumerate(doctrines, 1):
            response += f"\n{idx}. {doctrine.topic.upper()}\n"
            response += "-" * 80 + "\n"
            response += "Conclusion:\n" + "\n".join(f"  • {c}" for c in doctrine.conclusion_template) + "\n\n"
            response += "Detailed Framework:\n" + doctrine.reasoning_framework + "\n\n"
            response += "Critical Factors:\n" + "\n".join(f"  • {f}" for f in doctrine.key_factors) + "\n\n"
            response += "References:\n" + "\n".join(f"  • {a}" for a in doctrine.primary_authority) + "\n\n"

            if doctrine.method_requirements:
                response += "Method Requirements:\n" + "\n".join(f"  • {r}" for r in doctrine.method_requirements) + "\n\n"

        response += "\n" + "=" * 80 + "\n"
        response += "END OF MEMORANDUM"

        return response

    def _fallback_response(self, query: str, mode: ResponseMode, start_time: float) -> QueryResponse:
        """Response when no doctrines match"""
        self.metrics["errors"]["no_match"] += 1

        response_text = (
            "No specific analytical chemistry doctrine matched this query. "
            "This query may require domain knowledge outside the current scope of "
            "chromatography, spectroscopy, electrochemistry, titration, gravimetric analysis, "
            "method validation, quality assurance, calibration, atomic methods, X-ray methods, "
            "thermal analysis, surface analysis, sampling, sample preparation, and applications. "
            "Please rephrase or provide additional context."
        )

        latency = (time.time() - start_time) * 1000

        return QueryResponse(
            query=query,
            response=response_text,
            mode=mode,
            confidence=ConfidenceLevel.DISCLOSURE,
            doctrines_triggered=[],
            reasoning_chain=[],
            determinism_hash=hashlib.sha256(query.encode()).hexdigest()[:16],
            latency_ms=round(latency, 2),
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health status"""
        avg_latency = sum(self.metrics["latencies"][-100:]) / len(self.metrics["latencies"][-100:]) if self.metrics["latencies"] else 0

        return {
            "status": "healthy",
            "engine": "CHEM03_analytical_chemistry",
            "version": "1.0.0",
            "port": 9053,
            "doctrines": len(DOCTRINE_CACHE),
            "categories": len(set(d.category for d in DOCTRINE_CACHE)),
            "metrics": {
                "total_queries": self.metrics["queries"],
                "cache_hits": self.metrics["cache_hits"],
                "avg_latency_ms": round(avg_latency, 2),
                "error_count": sum(self.metrics["errors"].values())
            },
            "coverage": {
                "total_doctrines": len(DOCTRINE_CACHE),
                "triggered": len(self.coverage_map),
                "most_used": sorted(self.coverage_map.items(), key=lambda x: x[1], reverse=True)[:5]
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(title="CHEM03 Analytical Chemistry Engine", version="1.0.0")

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

engine = CHEM03Engine()

@APP.get("/health")
async def health():
    """Health check endpoint"""
    return engine.health_check()

@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint"""
    return engine.query(request.query, request.mode, request.context)

@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrines"""
    return {
        "total": len(DOCTRINE_CACHE),
        "categories": {cat.value: len([d for d in DOCTRINE_CACHE if d.category == cat]) for cat in IssueCategory},
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords[:3],
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }

@APP.get("/metrics")
async def get_metrics():
    """Detailed metrics"""
    return {
        "queries": engine.metrics["queries"],
        "errors": dict(engine.metrics["errors"]),
        "latency_stats": {
            "count": len(engine.metrics["latencies"]),
            "avg_ms": round(sum(engine.metrics["latencies"]) / len(engine.metrics["latencies"]), 2) if engine.metrics["latencies"] else 0,
            "min_ms": round(min(engine.metrics["latencies"]), 2) if engine.metrics["latencies"] else 0,
            "max_ms": round(max(engine.metrics["latencies"]), 2) if engine.metrics["latencies"] else 0
        },
        "coverage": dict(engine.coverage_map)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(APP, host="0.0.0.0", port=9053)
