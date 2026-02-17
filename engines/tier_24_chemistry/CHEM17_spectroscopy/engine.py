"""
CHEM17 Spectroscopy Intelligence Engine
TIE-Grade Spectroscopic Analysis System v1.0.0
Port: 9299

Analyzes spectroscopic methods: UV-Vis, IR/FTIR, NMR, mass spectrometry,
Raman, X-ray techniques for chemical identification and quantification.

Authority: ACS Analytical Chemistry, IUPAC Spectroscopy Standards,
           FDA/ICH Method Validation, ASTM Spectroscopic Methods
"""

import sys
from pathlib import Path

# CRITICAL: Add parent to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, Counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ============================================================================
# ENUMS & DATA CLASSES
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


class SpectroscopyDomain(str, Enum):
    UV_VIS = "UV_VIS"
    IR_FTIR = "IR_FTIR"
    NMR = "NMR"
    MASS_SPEC = "MASS_SPEC"
    RAMAN = "RAMAN"
    XRAY = "XRAY"
    ATOMIC = "ATOMIC"
    FLUORESCENCE = "FLUORESCENCE"
    VALIDATION = "VALIDATION"
    HYPHENATED = "HYPHENATED"


@dataclass
class DoctrineBlock:
    """Real spectroscopic doctrine with expert reasoning"""
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: List[str]
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    domain: SpectroscopyDomain
    confidence: ConfidenceLevel
    controlling_precedent: Optional[str] = None


@dataclass
class QueryMetrics:
    """Telemetry for spectroscopic analysis"""
    query_id: str
    timestamp: float
    mode: ResponseMode
    domain: SpectroscopyDomain
    cache_hit: bool
    doctrines_triggered: List[str]
    doctrines_missed: List[str]
    latency_ms: float
    confidence: ConfidenceLevel
    epistemic_gaps: List[str]
    determinism_hash: str


# ============================================================================
# DOCTRINE CACHE - REAL SPECTROSCOPIC EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    # UV-Vis Spectroscopy Doctrines
    DoctrineBlock(
        topic="Beer-Lambert Law Application and Deviations",
        keywords=["beer-lambert", "absorbance", "molar absorptivity", "concentration", "path length", "linearity"],
        conclusion_template=[
            "The Beer-Lambert law (A = epsilon * b * c) holds under specific conditions.",
            "Deviations occur from chemical, instrumental, or concentration-related factors.",
            "Linearity validation is essential for quantitative UV-Vis analysis."
        ],
        reasoning_framework=[
            "The Beer-Lambert law states absorbance is proportional to concentration",
            "when molar absorptivity (epsilon) and path length (b) are constant.",
            "Epsilon is wavelength-dependent and species-specific, units L/(mol·cm).",
            "Path length b typically 1 cm for standard cuvettes, must be calibrated.",
            "Linearity holds only within a concentration range where epsilon is constant.",
            "",
            "Chemical deviations include: association/dissociation reactions changing",
            "the absorbing species concentration, solvent effects altering epsilon,",
            "pH changes affecting chromophore structure, temperature dependencies.",
            "Example: weak acid chromophores show pH-dependent spectra from protonation equilibria.",
            "",
            "Instrumental deviations: stray light causes negative deviations at high A,",
            "polychromatic radiation (finite bandwidth) averages epsilon across wavelengths,",
            "detector non-linearity at low or high light intensities, scattering from particles.",
            "Stray light effect becomes significant above A = 2 (1% transmittance).",
            "",
            "Concentration deviations: at high concentrations, molecules interact (aggregation),",
            "refractive index changes affect light path, self-absorption or inner-filter effects.",
            "Working range typically 0.2 < A < 0.8 for best precision (10-60% transmittance).",
            "",
            "Method validation requires demonstrating linearity over intended range,",
            "minimum 5 concentration levels, r^2 > 0.995, residuals analysis for systematic bias.",
            "LOD = 3.3 * sigma / slope, LOQ = 10 * sigma / slope from calibration curve.",
            "ICH Q2(R1) and FDA guidelines specify acceptance criteria for linearity testing.",
            "",
            "Multi-component analysis uses simultaneous equations when spectra overlap:",
            "absorbance at each wavelength is sum of individual contributions.",
            "Matrix algebra solves for concentrations from absorbances at n wavelengths.",
            "Requires epsilon values at each wavelength for each component, spectral deconvolution.",
            "",
            "Derivative spectroscopy enhances resolution of overlapping peaks,",
            "first derivative zeros at peak maximum, second derivative shows negative peak.",
            "Ratio spectra eliminate baseline slope, useful for mixtures with constant interferent."
        ],
        key_factors=[
            "Molar absorptivity epsilon values (temperature, solvent, pH dependent)",
            "Concentration range linearity limits (typically 0.01-100 micromolar)",
            "Stray light effects above A = 2",
            "Chemical equilibria affecting chromophore species distribution",
            "Instrumental bandwidth relative to absorption peak width",
            "Path length calibration and temperature control",
            "Matrix effects from sample composition",
            "Solvent transparency in measurement wavelength range"
        ],
        primary_authority=[
            "IUPAC Recommendations on UV-Vis Spectrophotometry",
            "ICH Q2(R1) Validation of Analytical Procedures",
            "ASTM E275 Standard Practice for Describing and Measuring Performance of Ultraviolet and Visible Spectrophotometers",
            "Skoog & West, Fundamentals of Analytical Chemistry, Chapter on Molecular Absorption Spectroscopy",
            "FDA Guidance for Industry: Analytical Procedures and Methods Validation (2015)"
        ],
        burden_holder="Analyst",
        adversary_position="Concentration measurements unreliable if Beer-Lambert assumptions violated",
        counter_arguments=[
            "Non-linearity at extreme concentrations due to molecular interactions",
            "Stray light causes underestimation of high absorbances",
            "Solvent effects change epsilon values between standards and samples",
            "Polychromatic radiation averages epsilon over bandwidth",
            "Chemical reactions during measurement alter analyte concentration"
        ],
        resolution_strategy="Validate linearity empirically over working range, use appropriate blanks, control temperature and pH, minimize stray light with high-quality instruments, use derivative or multivariate methods for overlapping spectra, report epsilon with measurement conditions.",
        domain=SpectroscopyDomain.UV_VIS,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ICH Q2(R1) Section 2.2.5 Linearity"
    ),

    DoctrineBlock(
        topic="Chromophore Identification and Woodward-Fieser Rules",
        keywords=["chromophore", "auxochrome", "bathochromic shift", "woodward-fieser", "conjugation", "lambda max"],
        conclusion_template=[
            "Chromophores are structural units responsible for UV-Vis absorption.",
            "Woodward-Fieser rules predict lambda-max for conjugated systems empirically.",
            "Conjugation extent and substituent effects determine absorption wavelength and intensity."
        ],
        reasoning_framework=[
            "A chromophore is a functional group with pi-electrons or non-bonding electrons",
            "capable of absorbing UV or visible radiation (200-800 nm range).",
            "Common chromophores: carbonyl (n→pi* ~280 nm), alkene (pi→pi* ~180 nm),",
            "aromatic rings (benzene ~254 nm), conjugated dienes, nitro groups, azo groups.",
            "",
            "Auxochromes are substituents (OH, NH2, Cl, Br) that shift chromophore absorption",
            "via resonance or inductive effects but do not absorb strongly themselves.",
            "Electron-donating groups (EDG) cause bathochromic (red) shift and hyperchromic effect",
            "(increased epsilon). Electron-withdrawing groups (EWG) cause hypsochromic (blue) shift.",
            "",
            "Woodward-Fieser rules empirically predict lambda-max for conjugated dienes and carbonyls:",
            "Base value (diene: 214 nm, enone: 215 nm) + increments for alkyl substituents,",
            "ring residues, exocyclic double bonds, extended conjugation (+30 nm per C=C),",
            "homoannular diene (+39 nm), heteroannular diene (+0 nm).",
            "Example: 1,3-butadiene (214 nm), 1,3-cyclohexadiene (256 nm from ring +39 nm).",
            "",
            "Extended conjugation lowers HOMO-LUMO gap, shifting absorption to longer wavelengths.",
            "Each additional conjugated double bond adds ~30 nm for linear polyenes.",
            "Beta-carotene (11 conjugated C=C) absorbs at 450 nm in visible range (orange).",
            "",
            "Solvent effects (solvatochromism): polar solvents stabilize excited states differentially.",
            "n→pi* transitions show hypsochromic shift in polar solvents (excited state less polar),",
            "pi→pi* transitions show bathochromic shift (excited state more polar).",
            "General guideline: polar solvents red-shift pi→pi*, blue-shift n→pi*.",
            "",
            "Steric effects: non-planar conjugated systems have reduced conjugation,",
            "twisted conformations increase HOMO-LUMO gap (hypsochromic shift).",
            "Example: biphenyl vs. ortho-substituted biphenyls with restricted rotation.",
            "",
            "Quantitative structure-activity relationships (QSAR) use computational methods",
            "to predict lambda-max from molecular orbital calculations (HOMO-LUMO gaps).",
            "Time-dependent DFT (TD-DFT) provides accurate predictions for many systems."
        ],
        key_factors=[
            "Conjugation length (number of alternating double bonds)",
            "Auxochrome electron-donating or withdrawing character",
            "Solvent polarity effects on n→pi* vs. pi→pi* transitions",
            "Steric constraints affecting planarity and conjugation",
            "Ring strain and homoannular vs. heteroannular diene geometry",
            "pH effects on protonation state of auxochromes",
            "Temperature effects on conformational equilibria"
        ],
        primary_authority=[
            "Woodward, R. B. (1941). Structure and the Absorption Spectra of alpha,beta-Unsaturated Ketones. J. Am. Chem. Soc., 63, 1123.",
            "Fieser, L. F., & Fieser, M. (1949). Natural Products Related to Phenanthrene. Reinhold.",
            "Silverstein, R. M., Webster, F. X., Kiemle, D. J. (2005). Spectrometric Identification of Organic Compounds, 7th ed.",
            "IUPAC Gold Book: Chromophore Definition",
            "Lambert, J. B., Shurvell, H. F., Organic Structural Spectroscopy, Chapter on UV-Vis"
        ],
        burden_holder="Analyst",
        adversary_position="Woodward-Fieser rules are empirical approximations, not exact predictions",
        counter_arguments=[
            "Sterically hindered conjugated systems deviate from planarity",
            "Heteroatoms in conjugation alter electron distribution unpredictably",
            "Solvent-solute specific interactions not captured by polarity alone",
            "Conformational mixtures average multiple absorption profiles",
            "Excited state dynamics beyond simple HOMO-LUMO model"
        ],
        resolution_strategy="Use Woodward-Fieser rules for initial prediction, validate with experimental measurement, apply computational TD-DFT for complex systems, consider solvent and temperature effects, measure in multiple solvents to assess solvatochromism, use literature precedent for similar structures.",
        domain=SpectroscopyDomain.UV_VIS,
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Woodward (1941) and Fieser (1949) empirical correlations"
    ),

    # IR/FTIR Spectroscopy Doctrines
    DoctrineBlock(
        topic="Functional Group Identification by IR Spectroscopy",
        keywords=["infrared", "functional group", "stretching", "bending", "fingerprint region", "wavenumber"],
        conclusion_template=[
            "IR spectroscopy identifies functional groups from characteristic vibrational frequencies.",
            "Stretching vibrations (2500-4000 cm^-1) are most diagnostic for group identification.",
            "Fingerprint region (600-1500 cm^-1) provides unique molecular signature but complex interpretation."
        ],
        reasoning_framework=[
            "Infrared absorption occurs when molecular vibration causes change in dipole moment.",
            "Vibrational frequency depends on bond strength (force constant k) and reduced mass (mu):",
            "wavenumber (cm^-1) proportional to sqrt(k/mu), Hooke's law approximation.",
            "Stronger bonds (higher k) and lighter atoms (lower mu) give higher frequencies.",
            "",
            "O-H stretch: broad 3200-3600 cm^-1 (alcohols, phenols, carboxylic acids),",
            "broadness from hydrogen bonding. Free OH ~3600 cm^-1 (sharp), bonded OH 3200-3400 cm^-1 (broad).",
            "Carboxylic acid O-H extremely broad 2500-3300 cm^-1 from strong dimer hydrogen bonding.",
            "",
            "N-H stretch: 3300-3500 cm^-1, primary amines show two peaks (symmetric and antisymmetric),",
            "secondary amines show one peak, tertiary amines no N-H absorption.",
            "Amides show N-H at lower frequency (~3300 cm^-1) from resonance reducing bond order.",
            "",
            "C-H stretch: sp C-H 3300 cm^-1 (alkynes, sharp), sp2 C-H 3000-3100 cm^-1 (alkenes, aromatics),",
            "sp3 C-H 2850-2960 cm^-1 (alkanes). Aldehyde C-H shows characteristic doublet 2720 and 2820 cm^-1.",
            "",
            "C=O stretch: carbonyl group 1650-1850 cm^-1, most intense and diagnostic absorption.",
            "Position depends on conjugation and inductive effects:",
            "Acid chlorides 1800 cm^-1 (high), esters 1735 cm^-1, ketones/aldehydes 1715 cm^-1,",
            "amides 1650 cm^-1 (low from resonance), conjugated carbonyls -20 to -30 cm^-1 shift.",
            "Ring strain increases frequency: cyclobutanone 1780 cm^-1 vs. cyclohexanone 1715 cm^-1.",
            "",
            "C=C stretch: 1620-1680 cm^-1 for alkenes, often weak or absent if symmetrical (no dipole change).",
            "Aromatic C=C: 1450-1600 cm^-1, multiple peaks from ring vibrations.",
            "C≡C stretch: 2100-2260 cm^-1 for alkynes, weak for symmetrical internal alkynes.",
            "",
            "Fingerprint region 600-1500 cm^-1: C-O stretch 1000-1300 cm^-1,",
            "C-N stretch 1020-1250 cm^-1, C-C stretch, bending vibrations (CH2 scissor 1465 cm^-1).",
            "Complex coupling of vibrations makes individual band assignment difficult,",
            "but overall pattern is highly specific to molecular structure (like a fingerprint).",
            "",
            "FTIR advantages: full spectrum acquisition in seconds (interferogram Fourier transform),",
            "higher sensitivity and resolution than dispersive IR, digital subtraction for background correction,",
            "ATR (attenuated total reflectance) sampling for solids/liquids without KBr pellets.",
            "",
            "Sample preparation: KBr pellet (1-2% analyte in KBr, pressed), Nujol mull (solid in mineral oil),",
            "ATR crystal (diamond or ZnSe), solution cells with NaCl or KBr windows (avoid water, dissolves salt).",
            "Avoid moisture: water absorbs broadly 3200-3600 cm^-1 and 1640 cm^-1, obscures sample peaks."
        ],
        key_factors=[
            "Bond strength and reduced mass determining vibrational frequency",
            "Hydrogen bonding effects on O-H and N-H stretching frequencies and band shape",
            "Conjugation and resonance lowering carbonyl frequencies by 20-30 cm^-1",
            "Ring strain increasing carbonyl frequency in small rings",
            "Symmetry considerations (symmetric vibrations may be IR-inactive)",
            "Inductive effects from electronegative substituents",
            "Sample purity and preparation method (KBr, ATR, solution)",
            "Moisture interference from atmospheric water absorption"
        ],
        primary_authority=[
            "ASTM E1252 Standard Practice for General Techniques for Obtaining Infrared Spectra for Qualitative Analysis",
            "Silverstein, R. M., Webster, F. X., Kiemle, D. J. (2005). Spectrometric Identification of Organic Compounds, IR Chapter",
            "Socrates, G. (2001). Infrared and Raman Characteristic Group Frequencies, 3rd ed.",
            "Colthup, N. B., Daly, L. H., Wiberley, S. E. (1990). Introduction to Infrared and Raman Spectroscopy, 3rd ed.",
            "NIST Chemistry WebBook: IR Spectra Database"
        ],
        burden_holder="Analyst",
        adversary_position="IR alone insufficient for definitive structure determination, only functional groups",
        counter_arguments=[
            "Overlapping absorptions from multiple functional groups complicate interpretation",
            "Weak or absent bands for symmetric vibrations",
            "Matrix effects from sample preparation alter band positions and intensities",
            "Hydrogen bonding strength varies with concentration and temperature",
            "Fingerprint region too complex for ab initio interpretation without reference spectra"
        ],
        resolution_strategy="Use IR in combination with NMR and MS for structure elucidation, compare fingerprint region with authentic standard or spectral database, use ATR to minimize sample preparation artifacts, control sample temperature and moisture, apply computational vibrational analysis (DFT frequency calculations) for complex molecules.",
        domain=SpectroscopyDomain.IR_FTIR,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASTM E1252 and Socrates (2001) Group Frequencies"
    ),

    # NMR Spectroscopy Doctrines
    DoctrineBlock(
        topic="1H NMR Chemical Shift Interpretation and Spin-Spin Coupling",
        keywords=["proton nmr", "chemical shift", "coupling constant", "multiplicity", "integration", "shielding"],
        conclusion_template=[
            "1H NMR chemical shifts reveal electronic environment of protons (0-12 ppm range).",
            "Spin-spin coupling (J values) indicates number of neighboring protons and bond connectivity.",
            "Integration gives relative number of protons in each environment, multiplicity follows n+1 rule."
        ],
        reasoning_framework=[
            "Chemical shift (delta, ppm) measures proton resonance frequency relative to TMS (tetramethylsilane) reference.",
            "Electron-withdrawing groups deshield protons, shifting signal downfield (higher ppm).",
            "Electron-donating groups shield protons, shifting signal upfield (lower ppm).",
            "",
            "Typical chemical shift ranges for 1H NMR in CDCl3:",
            "TMS reference 0 ppm, alkane CH3 0.8-1.0 ppm, alkane CH2 1.2-1.4 ppm,",
            "alkyne H 2.0-3.0 ppm, ether/alcohol CH 3.3-4.0 ppm,",
            "alkene H 4.5-6.0 ppm, aromatic H 6.5-8.5 ppm,",
            "aldehyde H 9-10 ppm, carboxylic acid H 10-13 ppm (very broad, exchangeable).",
            "",
            "Electronegative substituents (O, N, halogens) deshield adjacent protons:",
            "CH3-CH3 (0.9 ppm) vs. CH3-Cl (3.0 ppm), deshielding decreases with distance.",
            "Alpha protons to carbonyls appear at 2.0-2.5 ppm from anisotropic and inductive effects.",
            "",
            "Aromatic ring current creates anisotropic magnetic field: protons above/below ring shielded,",
            "protons in plane deshielded. Benzene protons at 7.3 ppm, ortho/meta/para substitution",
            "patterns distinguish isomers. Electron-donating substituents shift ortho/para upfield,",
            "electron-withdrawing shift downfield.",
            "",
            "Spin-spin coupling (J coupling): proton with n neighboring protons splits into n+1 peaks.",
            "Coupling constant J (Hz) independent of magnetic field strength, reflects dihedral angle.",
            "Vicinal coupling (3J, across 3 bonds H-C-C-H): 0-18 Hz, Karplus equation relates J to dihedral angle.",
            "Geminal coupling (2J, H-C-H): typically -12 to -15 Hz, negative (not directly observable).",
            "Long-range coupling (4J, 5J): 0-3 Hz, weak, observable in rigid systems or aromatic rings.",
            "",
            "Multiplicity nomenclature: singlet (s, 0 neighbors), doublet (d, 1 neighbor),",
            "triplet (t, 2 equivalent neighbors), quartet (q, 3 equivalent), multiplet (m, complex).",
            "Pascal's triangle predicts peak intensities: doublet 1:1, triplet 1:2:1, quartet 1:3:3:1.",
            "",
            "Integration: area under peak proportional to number of protons causing signal.",
            "Normalize integration to smallest peak, deduce relative ratios (e.g., 3:2:2 = 7 total H).",
            "Compare to molecular formula to assign absolute numbers.",
            "",
            "Exchangeable protons (OH, NH, COOH): broad peaks, position variable with concentration/temperature,",
            "D2O shake causes disappearance (exchange with deuterium, no NMR signal).",
            "Confirms presence of exchangeable protons, useful for distinguishing OH vs. CH.",
            "",
            "Second-order effects: when chemical shift difference (Hz) comparable to J coupling,",
            "simple n+1 rule breaks down, peaks lean toward each other, form complex multiplets (AB, ABX systems).",
            "Higher field magnets (600 MHz vs. 300 MHz) reduce second-order effects by increasing delta Hz."
        ],
        key_factors=[
            "Electronegativity of substituents causing deshielding (O, N, halogens)",
            "Anisotropic effects from pi systems (aromatic rings, carbonyls, alkenes)",
            "Number and equivalence of neighboring protons determining multiplicity",
            "Dihedral angle affecting vicinal coupling constant (Karplus relationship)",
            "Magnetic field strength influencing second-order effects",
            "Solvent effects (CDCl3 vs. DMSO-d6 vs. D2O) on chemical shifts",
            "Temperature and concentration effects on hydrogen bonding and exchange rates",
            "Sample purity and presence of water or other impurities"
        ],
        primary_authority=[
            "Karplus, M. (1959). Contact Electron-Spin Coupling of Nuclear Magnetic Moments. J. Chem. Phys., 30, 11.",
            "Silverstein, R. M., Webster, F. X., Kiemle, D. J. (2005). Spectrometric Identification of Organic Compounds, NMR Chapter",
            "Claridge, T. D. W. (2016). High-Resolution NMR Techniques in Organic Chemistry, 3rd ed.",
            "Keeler, J. (2010). Understanding NMR Spectroscopy, 2nd ed.",
            "Gottlieb, H. E., Kotlyar, V., Nudelman, A. (1997). NMR Chemical Shifts of Common Laboratory Solvents. J. Org. Chem., 62, 7512."
        ],
        burden_holder="Analyst",
        adversary_position="Complex coupling patterns and overlapping signals hinder unambiguous structure determination",
        counter_arguments=[
            "Accidentally equivalent protons obscure expected multiplicity",
            "Second-order coupling patterns deviate from simple n+1 rule",
            "Dynamic processes (rotation, exchange) average signals at room temperature",
            "Impurities and solvent peaks obscure analyte signals",
            "Overlapping multiplets in complex molecules require 2D NMR for resolution"
        ],
        resolution_strategy="Use high-field NMR (600+ MHz) to minimize second-order effects, perform D2O shake to identify exchangeable protons, use 2D NMR (COSY, HSQC, HMBC) to resolve overlapping multiplets and establish connectivity, measure variable temperature NMR to resolve dynamic processes, add shift reagents (lanthanides) or change solvent to resolve overlapping signals.",
        domain=SpectroscopyDomain.NMR,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Karplus Equation (1959) and Claridge (2016) NMR Interpretation"
    ),

    DoctrineBlock(
        topic="13C NMR Spectroscopy and DEPT Experiments",
        keywords=["carbon-13 nmr", "dept", "chemical shift", "quaternary carbon", "decoupling", "multiplicity editing"],
        conclusion_template=[
            "13C NMR provides carbon skeleton information with chemical shifts 0-220 ppm.",
            "Proton decoupling simplifies spectra to singlets, DEPT distinguishes CH3, CH2, CH, quaternary C.",
            "13C shifts are more sensitive to hybridization and substituent effects than 1H shifts."
        ],
        reasoning_framework=[
            "13C is 1.1% natural abundance, spin-1/2 nucleus, much lower sensitivity than 1H.",
            "Requires thousands of scans for adequate signal-to-noise, long relaxation times (T1 up to 100 s).",
            "Proton decoupling (broadband irradiation at 1H frequency) collapses 13C-1H multiplets to singlets,",
            "simplifies spectrum and increases signal intensity via nuclear Overhauser effect (NOE).",
            "",
            "13C chemical shift ranges (ppm from TMS):",
            "Alkane carbons 0-50 ppm, alcohols/ethers 50-90 ppm, alkenes 100-150 ppm,",
            "aromatic carbons 120-150 ppm, carbonyl carbons 160-220 ppm.",
            "Quaternary carbons (no attached H) often appear weaker due to slower relaxation.",
            "",
            "DEPT (Distortionless Enhancement by Polarization Transfer):",
            "DEPT-45: all C with attached H appear positive (CH, CH2, CH3).",
            "DEPT-90: only CH appear positive, CH2 and CH3 disappear.",
            "DEPT-135: CH and CH3 positive, CH2 negative, quaternary C disappear.",
            "Comparing DEPT-135 with regular 13C spectrum identifies quaternary carbons (present in 13C, absent in DEPT).",
            "",
            "DEPT editing strategy: DEPT-90 identifies CH, DEPT-135 phase distinguishes CH3/CH (up) from CH2 (down),",
            "quaternary carbons only in fully decoupled 13C spectrum.",
            "Example: carbonyl carbon (no H) only in 13C, not in any DEPT, confirms C=O.",
            "",
            "13C shifts highly sensitive to hybridization:",
            "sp3 carbon (alkane) 0-50 ppm, sp2 carbon (alkene, aromatic) 100-150 ppm,",
            "sp carbon (alkyne) 70-90 ppm, carbonyl sp2 160-220 ppm.",
            "Electronegative substituents deshield 13C: C-O 50-90 ppm, C-N 30-60 ppm, C-Cl 40-80 ppm.",
            "",
            "Carbonyl chemical shifts diagnostic for functional groups:",
            "Ketones/aldehydes 200-220 ppm, carboxylic acids/esters 160-180 ppm,",
            "amides 160-175 ppm, acid chlorides 165-180 ppm.",
            "Conjugation shifts carbonyl upfield by 10-20 ppm (reduced C=O bond order).",
            "",
            "Long-range correlations (2D NMR): HMQC/HSQC (1-bond C-H correlation),",
            "HMBC (2-bond, 3-bond C-H correlation) establishes carbon skeleton connectivity.",
            "INADEQUATE (13C-13C coupling) directly observes C-C bonds, but requires high concentration (low natural abundance).",
            "",
            "Relaxation considerations: quaternary carbons and carbons with few attached H",
            "have long T1 relaxation times, require longer recycle delays (5*T1) for quantitative integration.",
            "NOE enhancements vary by carbon type, making integration unreliable without inverse-gated decoupling."
        ],
        key_factors=[
            "Carbon hybridization state (sp3 vs. sp2 vs. sp) determining chemical shift range",
            "Electronegativity of directly bonded atoms (O, N, halogens) causing deshielding",
            "Number of attached hydrogens (determined by DEPT experiments)",
            "Relaxation time T1 affecting signal intensity and quantitation",
            "NOE enhancements from proton decoupling (varies by carbon type)",
            "Conjugation and resonance effects on carbonyl and aromatic carbon shifts",
            "Solvent effects and sample concentration influencing shifts and linewidths",
            "Magnetic field strength (higher field improves resolution and sensitivity)"
        ],
        primary_authority=[
            "Doddrell, D. M., Pegg, D. T., Bendall, M. R. (1982). Distortionless Enhancement of NMR Signals by Polarization Transfer. J. Magn. Reson., 48, 323.",
            "Breitmaier, E., Voelter, W. (1987). Carbon-13 NMR Spectroscopy, 3rd ed.",
            "Claridge, T. D. W. (2016). High-Resolution NMR Techniques in Organic Chemistry, 3rd ed.",
            "Pretsch, E., Bühlmann, P., Badertscher, M. (2009). Structure Determination of Organic Compounds, 13C NMR Tables",
            "Levy, G. C., Lichter, R. L., Nelson, G. L. (1980). Carbon-13 Nuclear Magnetic Resonance Spectroscopy, 2nd ed."
        ],
        burden_holder="Analyst",
        adversary_position="13C NMR alone insufficient for complete structure determination, requires correlation with 1H NMR",
        counter_arguments=[
            "Low natural abundance requires long acquisition times",
            "Quaternary carbons often weak or missing due to long T1 relaxation",
            "Integration unreliable without special decoupling sequences (inverse-gated)",
            "Overlapping signals in complex molecules require 2D NMR for resolution",
            "Solvent peaks (CDCl3 triplet at 77 ppm) can obscure analyte signals"
        ],
        resolution_strategy="Use DEPT experiments to determine carbon multiplicity, employ 2D NMR (HSQC, HMBC) for connectivity, use longer relaxation delays for quantitative work, compare with authentic standards or spectral databases, apply computational chemical shift prediction (DFT methods), measure at higher magnetic field for improved resolution.",
        domain=SpectroscopyDomain.NMR,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="DEPT Methodology (Doddrell et al., 1982)"
    ),

    # Mass Spectrometry Doctrines
    DoctrineBlock(
        topic="Electron Ionization Mass Spectrometry and Fragmentation Patterns",
        keywords=["ei-ms", "molecular ion", "fragmentation", "base peak", "nitrogen rule", "isotope pattern"],
        conclusion_template=[
            "EI-MS provides molecular weight from molecular ion peak and structural information from fragments.",
            "Fragmentation patterns reflect bond strengths and stability of resulting cations.",
            "Nitrogen rule and isotope patterns aid molecular formula determination."
        ],
        reasoning_framework=[
            "Electron ionization (EI): sample vaporized and bombarded with 70 eV electrons,",
            "energy exceeds ionization potential (~7-10 eV), produces radical cations M^+.",
            "70 eV is standard for reproducible fragmentation patterns, database comparison.",
            "",
            "Molecular ion peak [M]^+ gives molecular weight, highest m/z excluding isotope peaks.",
            "May be weak or absent for compounds with weak bonds or heteroatoms (alcohols, carbohydrates).",
            "Look for [M+1]^+ and [M+2]^+ isotope peaks to confirm molecular ion:",
            "13C natural abundance 1.1%, intensity of M+1 = 1.1% * number of carbons.",
            "Example: C10 compound shows M+1 peak at ~11% intensity of M peak.",
            "",
            "Nitrogen rule: odd molecular weight indicates odd number of nitrogens,",
            "even molecular weight indicates zero or even number of nitrogens.",
            "Applies to compounds containing only C, H, N, O, S, halogens.",
            "Exception: odd electron ions (M^+) follow rule, even electron fragments may not.",
            "",
            "Fragmentation mechanisms:",
            "Alpha cleavage: bond adjacent to heteroatom or carbonyl breaks, forms stable cation.",
            "Example: ketones lose alkyl radical R^. to form acylium [RCO]^+ ion (m/z = 43 for acetyl).",
            "McLafferty rearrangement: gamma-hydrogen transfer to carbonyl oxygen with bond cleavage,",
            "characteristic of carbonyl compounds with gamma-hydrogen, gives even-electron neutral loss.",
            "",
            "Stability of carbocations determines fragmentation preference:",
            "Tertiary > secondary > primary > methyl cation stability.",
            "Allylic and benzylic cations highly stable, favor formation of corresponding fragments.",
            "Tropylium cation [C7H7]^+ (m/z 91) diagnostic for benzyl systems (toluene derivatives).",
            "",
            "Common neutral losses:",
            "Loss of 15 (CH3), 29 (CHO or C2H5), 31 (OCH3 from methoxy), 18 (H2O from alcohols),",
            "44 (CO2 from carboxylic acids), 45 (COOH from acids), 46 (NO2 from nitro compounds).",
            "Sequential losses can be tracked: M - 15 - 15 = loss of two methyl groups.",
            "",
            "Isotope patterns for halogens:",
            "Chlorine: 35Cl and 37Cl in 3:1 ratio, M and M+2 peaks 3:1 intensity for one Cl,",
            "two Cl atoms give M, M+2, M+4 in 9:6:1 ratio.",
            "Bromine: 79Br and 81Br in 1:1 ratio, M and M+2 equal intensity for one Br,",
            "two Br give M, M+2, M+4 in 1:2:1 ratio.",
            "",
            "Base peak: most intense peak in spectrum (set to 100%), represents most stable fragment.",
            "Often not the molecular ion, reflects most favorable fragmentation pathway.",
            "Example: ethyl benzene base peak at m/z 91 (tropylium), not M^+ at 106.",
            "",
            "High-resolution MS (HRMS): determines exact mass to four decimal places,",
            "distinguishes isobaric ions (same nominal mass, different molecular formulas).",
            "Example: CO (27.9949) vs. N2 (28.0061) vs. C2H4 (28.0313) all nominal mass 28.",
            "Accuracy typically <5 ppm error, allows unambiguous molecular formula determination."
        ],
        key_factors=[
            "Ionization energy (70 eV standard for EI reproducibility)",
            "Molecular ion stability (heteroatoms, weak bonds reduce M^+ intensity)",
            "Carbocation stability governing fragmentation preference",
            "Isotope natural abundances (13C, 15N, 34S, 37Cl, 81Br patterns)",
            "Nitrogen rule for determining nitrogen count from molecular weight parity",
            "Characteristic neutral losses identifying functional groups",
            "Sample purity and volatility (non-volatile compounds unsuitable for EI)",
            "Background contamination (phthalates, siloxanes from septa/columns)"
        ],
        primary_authority=[
            "McLafferty, F. W., Turecek, F. (1993). Interpretation of Mass Spectra, 4th ed.",
            "Silverstein, R. M., Webster, F. X., Kiemle, D. J. (2005). Spectrometric Identification of Organic Compounds, MS Chapter",
            "NIST/EPA/NIH Mass Spectral Library: Standard Reference Database 1A",
            "Gross, J. H. (2017). Mass Spectrometry: A Textbook, 3rd ed.",
            "Busch, K. L., Glish, G. L., McLuckey, S. A. (1988). Mass Spectrometry/Mass Spectrometry"
        ],
        burden_holder="Analyst",
        adversary_position="Fragmentation patterns alone insufficient for structure determination without supporting data",
        counter_arguments=[
            "Molecular ion may be absent or very weak for labile compounds",
            "Rearrangement ions complicate interpretation, do not follow simple bond cleavages",
            "Isomers may give similar or identical fragmentation patterns",
            "Complex molecules produce too many fragments for unambiguous interpretation",
            "Background contamination from sample handling or instrument bleed"
        ],
        resolution_strategy="Use soft ionization (CI, ESI, MALDI) to observe molecular ion if EI shows weak M^+, compare fragmentation pattern with authentic standard or NIST library, use HRMS for molecular formula determination, combine with NMR and IR for complete structure elucidation, use MS/MS for fragmentation pathway confirmation.",
        domain=SpectroscopyDomain.MASS_SPEC,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="McLafferty and Turecek (1993) Fragmentation Principles"
    ),

    DoctrineBlock(
        topic="Electrospray Ionization and Soft Ionization Techniques",
        keywords=["esi", "soft ionization", "molecular ion", "adducts", "multiply charged ions", "maldi"],
        conclusion_template=[
            "Soft ionization (ESI, MALDI) produces intact molecular ions for thermally labile and high MW compounds.",
            "ESI generates multiply charged ions, extends mass range for large biomolecules.",
            "Adduct formation ([M+Na]^+, [M+K]^+, [M+NH4]^+) complicates spectrum but confirms molecular weight."
        ],
        reasoning_framework=[
            "Electrospray ionization (ESI): sample in solution sprayed through charged needle,",
            "solvent evaporates, ions transferred to gas phase with minimal fragmentation.",
            "Suitable for polar, ionic, thermally labile compounds (peptides, proteins, oligonucleides).",
            "Positive mode: protonation [M+H]^+, sodiation [M+Na]^+, potassiation [M+K]^+.",
            "Negative mode: deprotonation [M-H]^-, adducts with anions [M+Cl]^-, [M+acetate]^-.",
            "",
            "Multiply charged ions: proteins and peptides acquire multiple protons,",
            "z = charge state, observed m/z = (M + z*H) / z.",
            "Deconvolution algorithms determine molecular weight from charge state distribution.",
            "Example: protein MW 50,000 Da with z = +50 appears at m/z 1000.",
            "Extends practical mass range: quadrupole m/z 2000 limit can analyze MW 100,000+ proteins.",
            "",
            "Adduct ions: alkali metals (Na, K) from glassware or buffers form [M+Na]^+, [M+K]^+,",
            "shifts molecular ion by 22 Da (Na) or 38 Da (K) from [M+H]^+.",
            "Ammonium acetate buffers produce [M+NH4]^+ (+18 Da), [M+acetate]^- in negative mode.",
            "Multiple adducts complicate spectrum but confirm molecular weight:",
            "if [M+H]^+ and [M+Na]^+ differ by 22 Da, validates molecular ion assignment.",
            "",
            "Source parameters critical: spray voltage, desolvation temperature, gas flow rates,",
            "optimize for each compound class. Too harsh causes in-source fragmentation (loses soft ionization advantage),",
            "too gentle gives poor desolvation and broad peaks.",
            "",
            "Matrix-assisted laser desorption ionization (MALDI): sample co-crystallized with UV-absorbing matrix",
            "(alpha-cyano-4-hydroxycinnamic acid, sinapinic acid, 2,5-dihydroxybenzoic acid).",
            "Laser pulse ablates and ionizes sample, typically singly charged ions [M+H]^+ or [M+Na]^+.",
            "TOF (time-of-flight) mass analyzer common for MALDI, measures flight time to detector.",
            "Linear TOF: moderate resolution, reflectron TOF: high resolution by correcting kinetic energy spread.",
            "",
            "MALDI advantages: high salt tolerance, solid-state sampling (no chromatography required),",
            "high throughput (spot-to-spot acquisition <1 min), effective for MW 1,000-500,000 Da.",
            "Peptide mass fingerprinting: digest protein with trypsin, measure peptide masses,",
            "database search matches mass list to protein sequence.",
            "",
            "Soft ionization vs. EI: ESI/MALDI preserve molecular ion, minimal fragmentation,",
            "EI fragments extensively, provides structural information but often loses molecular ion.",
            "Complementary approaches: ESI/MALDI for MW determination, EI for structural elucidation,",
            "or use tandem MS (MS/MS) with ESI for both MW and fragmentation.",
            "",
            "Tandem MS (MS/MS) with ESI: select precursor ion in first analyzer (Q1),",
            "fragment by collision-induced dissociation (CID) in collision cell,",
            "analyze fragments in second analyzer (Q3). Combines soft ionization with structural information.",
            "Triple quadrupole (QqQ) for targeted quantitation, Q-TOF for high-resolution fragments."
        ],
        key_factors=[
            "Solvent composition and pH (affects ionization efficiency and adduct formation)",
            "Presence of alkali metals (Na, K) causing adduct ions instead of [M+H]^+",
            "Source parameters (spray voltage, temperature, gas flows) optimized per analyte",
            "Charge state distribution for large molecules (deconvolution accuracy)",
            "Matrix selection for MALDI (match matrix to analyte MW and polarity)",
            "Sample purity (salts and buffers affect ionization, cause ion suppression)",
            "Instrument type (quadrupole, TOF, ion trap, Orbitrap) determining resolution and mass accuracy",
            "Fragmentation control (in-source CID vs. MS/MS CID) for structural information"
        ],
        primary_authority=[
            "Fenn, J. B., et al. (1989). Electrospray Ionization for Mass Spectrometry of Large Biomolecules. Science, 246, 64. (Nobel Prize 2002)",
            "Karas, M., Hillenkamp, F. (1988). Laser Desorption Ionization of Proteins with Molecular Masses Exceeding 10,000 Daltons. Anal. Chem., 60, 2299.",
            "Gross, J. H. (2017). Mass Spectrometry: A Textbook, 3rd ed., ESI and MALDI Chapters",
            "Kebarle, P., Verkerk, U. H. (2009). Electrospray: From Ions in Solution to Ions in the Gas Phase. Mass Spectrom. Rev., 28, 898.",
            "Cole, R. B. (Ed.) (2010). Electrospray and MALDI Mass Spectrometry, 2nd ed."
        ],
        burden_holder="Analyst",
        adversary_position="Soft ionization provides molecular weight but limited structural information without MS/MS",
        counter_arguments=[
            "Ion suppression from matrix components (salts, detergents) reduces sensitivity",
            "Multiply charged ions complicate spectrum, require deconvolution",
            "Adduct formation unpredictable, multiple species ([M+H]^+, [M+Na]^+, [M+K]^+) reduce effective sensitivity",
            "Non-covalent interactions may survive ionization, giving anomalous MW (dimers, aggregates)",
            "Instrument-dependent ionization efficiency, quantitation requires internal standards"
        ],
        resolution_strategy="Use volatile buffers (ammonium acetate, formate) to minimize adducts, desalt samples (ZipTip, SPE) before ESI, optimize source parameters for each analyte class, use MS/MS for structural confirmation, compare [M+H]^+, [M+Na]^+, [M+NH4]^+ adducts to validate molecular weight, employ ion mobility separation (IMS) to resolve isobaric species.",
        domain=SpectroscopyDomain.MASS_SPEC,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Fenn (1989) ESI Principles and Karas/Hillenkamp (1988) MALDI Principles"
    ),

    # Raman Spectroscopy Doctrine
    DoctrineBlock(
        topic="Raman Spectroscopy and Surface-Enhanced Raman Scattering (SERS)",
        keywords=["raman", "stokes", "anti-stokes", "polarizability", "sers", "vibrational spectroscopy"],
        conclusion_template=[
            "Raman spectroscopy detects molecular vibrations via inelastic light scattering.",
            "Raman-active vibrations require change in polarizability, complementary to IR (dipole moment change).",
            "SERS enhances Raman signals 10^6-10^14 fold near metal nanoparticles, enables single-molecule detection."
        ],
        reasoning_framework=[
            "Raman effect: monochromatic light (typically laser) excites molecule to virtual state,",
            "inelastic scattering produces photons shifted in frequency by molecular vibration energy.",
            "Stokes scattering: molecule gains vibrational energy, scattered photon lower frequency (longer wavelength).",
            "Anti-Stokes scattering: molecule loses vibrational energy (requires initial vibrational excitation),",
            "scattered photon higher frequency. Stokes more intense at room temperature, typically measured.",
            "",
            "Raman shift: difference between incident and scattered photon frequency,",
            "reported in wavenumbers (cm^-1) independent of laser wavelength.",
            "Same vibrational frequency measured regardless of 532 nm, 785 nm, or 1064 nm laser excitation.",
            "",
            "Selection rules: Raman-active vibrations change molecular polarizability (electron cloud shape).",
            "Symmetric stretches typically strong in Raman, weak in IR (complementary to IR dipole selection rule).",
            "Example: C=C stretch strong in Raman for symmetric alkenes (no IR dipole change),",
            "C=O stretch strong in IR, weak in Raman (large dipole, small polarizability change).",
            "",
            "Advantages over IR: no water interference (water weak Raman scatterer, strong IR absorber),",
            "aqueous solutions easily measured, glass and quartz containers transparent,",
            "no sample preparation (direct measurement of liquids, solids, crystals, polymers).",
            "Lower frequency vibrations accessible (50-200 cm^-1 metal-ligand, lattice modes) difficult in IR.",
            "",
            "Disadvantages: fluorescence interference (background swamps weak Raman signal),",
            "low sensitivity (1 in 10^6-10^8 photons Raman scattered vs. 10^-2-10^-6 absorbed in IR),",
            "sample heating from laser (local hot spots, decomposition of sensitive compounds),",
            "sampling depth limited by laser penetration and scattering.",
            "",
            "Fluorescence mitigation: use near-IR lasers (785 nm, 1064 nm) with energy below",
            "electronic transitions (less fluorescence excitation), photobleach sample with prolonged laser exposure,",
            "use time-gated or shifted-excitation Raman to discriminate fast Raman from slow fluorescence.",
            "",
            "Surface-Enhanced Raman Scattering (SERS): electromagnetic field enhancement",
            "near metal nanoparticles (Au, Ag) amplifies Raman signal 10^6-10^14 fold.",
            "Mechanism: localized surface plasmon resonance (LSPR) at nanoparticle surface",
            "creates intense local electric field, Raman intensity proportional to E^4.",
            "Requires analyte adsorbed or within ~10 nm of metal surface (near-field effect).",
            "",
            "SERS substrates: colloidal nanoparticles, roughened metal electrodes,",
            "lithographically fabricated nanostructures (nanopillars, nanovoids), aggregated colloids.",
            "Reproducibility challenge: SERS signal highly dependent on nanoparticle aggregation state,",
            "hot spots (junctions between particles) dominate signal, spatial heterogeneity.",
            "",
            "SERS applications: trace detection (pesticides, explosives, drugs at ppm-ppb levels),",
            "single-molecule detection (reported for rhodamine 6G on Ag nanoparticles),",
            "biochemical sensing (DNA, proteins, glucose monitoring), art conservation (pigment identification),",
            "forensic analysis (gunshot residue, fibers, inks).",
            "",
            "Quantitation challenges: SERS enhancement factor varies with analyte position,",
            "particle aggregation state, laser polarization. Internal standards essential,",
            "often not possible for trace analysis. Semi-quantitative or qualitative use predominates."
        ],
        key_factors=[
            "Laser wavelength (visible vs. near-IR) affecting fluorescence interference",
            "Molecular polarizability determining Raman scattering cross-section",
            "Fluorescence quantum yield (high fluorescence obscures Raman signal)",
            "SERS substrate properties (particle size, shape, aggregation, metal type)",
            "Analyte-surface interaction (adsorption, distance from metal surface)",
            "Laser power and exposure time (sample heating, photodegradation risk)",
            "Detection sensitivity (CCD camera, confocal optics, signal averaging)",
            "Sample matrix effects (aqueous vs. organic solvents, pH, ionic strength)"
        ],
        primary_authority=[
            "Raman, C. V., Krishnan, K. S. (1928). A New Type of Secondary Radiation. Nature, 121, 501. (Nobel Prize 1930)",
            "Fleischmann, M., Hendra, P. J., McQuillan, A. J. (1974). Raman Spectra of Pyridine Adsorbed at a Silver Electrode. Chem. Phys. Lett., 26, 163. (First SERS report)",
            "Smith, E., Dent, G. (2019). Modern Raman Spectroscopy: A Practical Approach, 2nd ed.",
            "Moskovits, M. (1985). Surface-Enhanced Spectroscopy. Rev. Mod. Phys., 57, 783.",
            "ASTM E1840 Standard Guide for Raman Shift Standards for Spectrometer Calibration"
        ],
        burden_holder="Analyst",
        adversary_position="Raman spectroscopy limited by low sensitivity and fluorescence interference without SERS enhancement",
        counter_arguments=[
            "Fluorescence from sample or impurities overwhelms weak Raman signal",
            "Low scattering cross-section requires high laser power (sample damage risk)",
            "SERS enhancement highly variable, poor reproducibility for quantitation",
            "Laser heating causes thermal degradation of sensitive compounds",
            "Limited penetration depth compared to IR transmission measurements"
        ],
        resolution_strategy="Use near-IR lasers (785 nm, 1064 nm) to minimize fluorescence, apply SERS for trace-level detection, optimize substrate and analyte interaction time, use confocal Raman microscopy for spatial resolution, combine with multivariate analysis (PCA, PLS) for complex mixtures, validate with authentic standards and cross-check with complementary techniques (IR, MS).",
        domain=SpectroscopyDomain.RAMAN,
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Raman/Krishnan (1928) Raman Effect Discovery and Fleischmann et al. (1974) SERS Discovery"
    ),

    # X-ray Spectroscopy Doctrines
    DoctrineBlock(
        topic="X-ray Fluorescence (XRF) for Elemental Analysis",
        keywords=["xrf", "x-ray fluorescence", "elemental analysis", "ka line", "kb line", "energy dispersive"],
        conclusion_template=[
            "XRF identifies and quantifies elements from fluorescent X-ray emission characteristic of each element.",
            "Non-destructive, multi-element analysis with minimal sample preparation.",
            "Energy-dispersive XRF (EDXRF) vs. wavelength-dispersive XRF (WDXRF) trade speed for resolution."
        ],
        reasoning_framework=[
            "XRF principle: high-energy X-rays or gamma rays excite inner-shell electrons (K, L shells),",
            "eject electron creating core hole, outer-shell electron fills hole, emits fluorescent X-ray.",
            "Fluorescent X-ray energy characteristic of element (Moseley's law: E proportional to (Z-sigma)^2),",
            "detector measures energy (EDXRF) or wavelength (WDXRF) to identify element.",
            "",
            "K-alpha and K-beta lines: K-shell vacancy filled by L-shell electron (K-alpha, higher intensity)",
            "or M-shell electron (K-beta, lower intensity). K-alpha split into Ka1 and Ka2 doublet (L subshells).",
            "L-series lines from L-shell vacancies (La, Lb, Lg), lower energy than K-series, used for heavy elements.",
            "",
            "Energy-dispersive XRF (EDXRF): semiconductor detector (Si(Li), SDD) measures X-ray energy directly,",
            "simultaneous multi-element detection, rapid (minutes), portable instruments available.",
            "Resolution ~150 eV (cannot resolve adjacent elements in some cases, e.g., S and Pb L-lines overlap).",
            "Sample presentation: solids, liquids, powders, no vacuum required for elements Z > 11 (Na).",
            "",
            "Wavelength-dispersive XRF (WDXRF): crystal diffractometer selects X-ray wavelength by Bragg's law,",
            "sequential detection (scan wavelengths), higher resolution (~5-20 eV) and sensitivity than EDXRF.",
            "Better for trace analysis (sub-ppm detection limits) and light elements (Be to Na).",
            "Slower (hours for full scan), larger bench-top instruments, requires vacuum for light elements.",
            "",
            "Matrix effects: X-ray absorption and enhancement by sample matrix elements affect intensity.",
            "Heavy elements absorb X-rays from light elements (absorption), light elements scatter X-rays enhancing heavy elements.",
            "Fundamental parameters method corrects for matrix using physics-based calculations,",
            "empirical calibration with matrix-matched standards also used.",
            "",
            "Quantitation: calibration curves from standards with known element concentrations,",
            "intensity ratio (analyte/internal standard) vs. concentration, linear over limited range.",
            "Standardless analysis uses fundamental parameters to estimate concentrations,",
            "accuracy 5-20% relative error, suitable for screening, not regulatory compliance.",
            "",
            "Detection limits: EDXRF 10-100 ppm for most elements, WDXRF 1-10 ppm or better,",
            "depends on element, matrix, measurement time. Light elements (Z < 11) difficult, require vacuum and WDXRF.",
            "",
            "Applications: metals and alloys composition (stainless steel grade identification),",
            "mining and ore analysis, soil and sediment contamination (Pb, As, Hg),",
            "art and archaeology (pigment identification, provenance), electronics (RoHS compliance Pb, Cd, Hg),",
            "pharmaceutical contamination screening, cement and glass composition.",
            "",
            "Regulatory methods: EPA 6200 (field portable XRF for metals in soil),",
            "ASTM E1621 (XRF for Pb in paint), ASTM D6481 (sulfur in petroleum by EDXRF)."
        ],
        key_factors=[
            "Element atomic number (determines characteristic X-ray energies)",
            "Matrix composition (absorption and enhancement effects on fluorescence intensity)",
            "Sample preparation (homogeneity, surface smoothness, thickness)",
            "Excitation source (X-ray tube voltage and current, isotope source strength)",
            "Detector type (EDXRF vs. WDXRF resolution and sensitivity trade-offs)",
            "Measurement time (longer times improve counting statistics, lower detection limits)",
            "Calibration standards (matrix-matched vs. fundamental parameters correction)",
            "Interference from overlapping X-ray lines (e.g., As Ka and Pb La)"
        ],
        primary_authority=[
            "Jenkins, R., Gould, R. W., Gedcke, D. (1995). Quantitative X-ray Spectrometry, 2nd ed.",
            "Beckhoff, B., et al. (Eds.) (2006). Handbook of Practical X-Ray Fluorescence Analysis.",
            "ASTM E1621 Standard Guide for Elemental Analysis by Wavelength Dispersive X-Ray Fluorescence Spectrometry",
            "EPA Method 6200 Field Portable X-Ray Fluorescence Spectrometry for the Determination of Elemental Concentrations in Soil and Sediment",
            "Brouwer, P. (2010). Theory of XRF: Getting Acquainted with the Principles, 3rd ed."
        ],
        burden_holder="Analyst",
        adversary_position="Matrix effects and overlapping X-ray lines limit accuracy without careful calibration",
        counter_arguments=[
            "Matrix absorption reduces light element signals unpredictably",
            "Overlapping X-ray lines (e.g., Pb La at 10.55 keV, As Ka at 10.54 keV) require deconvolution",
            "Sample heterogeneity causes spot-to-spot variation (XRF probes ~mm scale)",
            "Standardless analysis has 10-20% error, insufficient for regulatory limits",
            "Light elements (Z < 11) require vacuum and WDXRF, not practical for field analysis"
        ],
        resolution_strategy="Use matrix-matched calibration standards for accurate quantitation, employ fundamental parameters correction software, measure multiple spots on heterogeneous samples and average, use high-resolution WDXRF for overlapping lines, validate with certified reference materials (CRMs), cross-check with ICP-OES or ICP-MS for trace elements.",
        domain=SpectroscopyDomain.XRAY,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASTM E1621 and EPA Method 6200"
    ),

    # Atomic Spectroscopy Doctrine
    DoctrineBlock(
        topic="Atomic Absorption Spectroscopy (AAS) and ICP-OES for Trace Metal Analysis",
        keywords=["aas", "icp-oes", "atomic emission", "flame", "graphite furnace", "trace metals", "ionization"],
        conclusion_template=[
            "AAS measures absorption of light by ground-state atoms, single-element analysis with high sensitivity.",
            "ICP-OES measures emission from excited atoms, simultaneous multi-element analysis.",
            "Graphite furnace AAS (GFAAS) achieves ppb detection limits, ICP-OES for ppm-ppb range."
        ],
        reasoning_framework=[
            "Atomic absorption spectroscopy (AAS): sample atomized (flame or graphite furnace),",
            "ground-state atoms absorb resonance wavelength from hollow cathode lamp (HCL),",
            "absorption proportional to atom concentration (Beer-Lambert law for atoms).",
            "Element-specific: each element requires separate HCL, sequential analysis.",
            "",
            "Flame AAS (FAAS): sample aspirated into air-acetylene or nitrous oxide-acetylene flame,",
            "flame atomizes sample (2000-3000 K), atoms absorb light from HCL.",
            "Detection limits: ppm range (0.1-10 ppm typical), precision 0.5-2% RSD.",
            "Matrix interferences: chemical (refractory compound formation), ionization (high temperature ionizes analyte),",
            "spectral (overlapping lines), background absorption (molecular species, scatter).",
            "",
            "Graphite furnace AAS (GFAAS): sample (5-50 microliters) injected into graphite tube,",
            "heated electrically in stages (dry, ash, atomize, clean), atomization temperature 2000-3000 K.",
            "Detection limits: ppb range (0.1-10 ppb), 10-100x more sensitive than FAAS.",
            "Eliminates dilution from flame, longer residence time of atoms (1-2 s vs. 0.001 s in flame).",
            "Matrix modifiers (Pd, Mg, NH4H2PO4) stabilize analyte during ashing, reduce matrix volatilization.",
            "",
            "Background correction: deuterium lamp (D2) correction for broad molecular absorption,",
            "Zeeman effect correction (magnetic field splits atomic lines, differentiates atomic from background),",
            "Smith-Hieftje correction (self-reversal of HCL at high current). Zeeman most effective, expensive.",
            "",
            "ICP-OES (inductively coupled plasma optical emission spectroscopy): sample nebulized into argon plasma,",
            "plasma temperature 6000-10,000 K atomizes and excites all elements simultaneously,",
            "atoms emit characteristic wavelengths upon relaxation, polychromator or echelle spectrometer measures emission.",
            "Multi-element capability: 20-70 elements in single analysis (3-5 min), simultaneous detection.",
            "",
            "ICP-OES detection limits: ppm to ppb range (1-100 ppb typical), depends on element and wavelength,",
            "sensitive for many elements (Cd, Pb, Cu, Zn), less sensitive for halogens, C, N, O.",
            "Precision 0.5-3% RSD, linear dynamic range 10^4-10^6 (measure major and trace elements together).",
            "",
            "ICP interferences: spectral (overlapping emission lines, requires spectral deconvolution or alternate lines),",
            "physical (viscosity, dissolved solids affect nebulization), chemical (minimal due to high temperature),",
            "ionization (easily ionized elements (EIE) like Na, K suppress analyte ionization, use ionization buffer).",
            "",
            "Sample preparation: acid digestion (HNO3, HCl, HF for silicates) to dissolve solid samples,",
            "microwave digestion (closed vessels, high temperature/pressure, rapid, safe),",
            "dilution to minimize matrix effects, match matrix of standards to samples.",
            "EPA 3050B (nitric acid digestion), EPA 3051A (microwave digestion) for environmental samples.",
            "",
            "Regulatory methods: EPA 200.7 (ICP-OES for metals in water), EPA 200.9 (GFAAS for trace metals),",
            "EPA 7000 series (FAAS for individual metals Pb, Cd, Cr), AOAC methods for food and agriculture."
        ],
        key_factors=[
            "Atomization method (flame vs. graphite furnace vs. ICP) determining sensitivity and matrix tolerance",
            "Background correction technique (D2, Zeeman, Smith-Hieftje) for accurate measurements",
            "Sample matrix composition (acids, salts, organics) affecting nebulization and ionization",
            "Element ionization potential (low IP elements ionize in flame, reducing atomic absorption)",
            "Spectral interferences from overlapping emission lines (ICP-OES) or molecular absorption (AAS)",
            "Sample digestion completeness (undissolved particles cause low recovery)",
            "Instrument operating conditions (flame temperature, plasma power, nebulizer flow)",
            "Calibration range and standard matrix matching for accuracy"
        ],
        primary_authority=[
            "Welz, B., Sperling, M. (1999). Atomic Absorption Spectrometry, 3rd ed.",
            "Boss, C. B., Fredeen, K. J. (1997). Concepts, Instrumentation and Techniques in Inductively Coupled Plasma Optical Emission Spectrometry, 2nd ed.",
            "EPA Method 200.7 Determination of Metals and Trace Elements in Water and Wastes by ICP-AES (Revision 4.4, 1994)",
            "EPA Method 200.9 Determination of Trace Elements by Stabilized Temperature Graphite Furnace AAS (Revision 2.2, 1994)",
            "ASTM D6919 Standard Test Method for Determination of Dissolved Alkali and Alkaline Earth Cations and Ammonium in Water and Wastewater by ICP-OES"
        ],
        burden_holder="Analyst",
        adversary_position="Matrix interferences and spectral overlaps require careful method development and validation",
        counter_arguments=[
            "Chemical interferences in flame AAS from refractory oxide formation (e.g., Ca-PO4)",
            "Ionization interferences from easily ionized elements (Na, K) in flame",
            "Spectral overlaps in ICP-OES (e.g., Fe has >4000 emission lines) require line selection",
            "Incomplete digestion of refractory matrices (silicates, ceramics) causes low recovery",
            "Memory effects from previous samples contaminating subsequent analyses (e.g., Hg, Ag)"
        ],
        resolution_strategy="Add releasing agents (La, Sr) for refractory compounds in flame AAS, use ionization suppressors (K, Cs) for ionization interference, select alternate emission lines for ICP-OES to avoid overlaps, optimize digestion with HF for silicates, use dedicated instruments or extensive rinse protocols for memory-prone elements, validate with certified reference materials (NIST SRMs).",
        domain=SpectroscopyDomain.ATOMIC,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="EPA Methods 200.7 (ICP-OES) and 200.9 (GFAAS)"
    ),

    # Method Validation Doctrine
    DoctrineBlock(
        topic="Analytical Method Validation for Spectroscopic Techniques",
        keywords=["method validation", "lod", "loq", "linearity", "precision", "accuracy", "ich q2"],
        conclusion_template=[
            "Method validation demonstrates an analytical procedure is suitable for intended purpose.",
            "ICH Q2(R1) and FDA guidelines specify validation parameters: specificity, linearity, accuracy, precision, range, LOD, LOQ.",
            "Validation is regulatory requirement for methods supporting product release and stability testing."
        ],
        reasoning_framework=[
            "Method validation confirms analytical procedure generates reliable, reproducible results",
            "for intended analyte, matrix, and concentration range. Required for regulatory submissions (FDA, EMA).",
            "",
            "Specificity (selectivity): ability to measure analyte unequivocally in presence of interferences.",
            "Demonstrate by analyzing blank (no analyte), placebo (matrix without analyte), spiked samples,",
            "forced degradation samples (oxidation, heat, light, acid/base). Spectroscopic methods:",
            "show lack of interference at analyte wavelength (UV-Vis, IR), resolved signals (NMR, MS).",
            "",
            "Linearity: proportional relationship between analyte concentration and response over specified range.",
            "Minimum 5 concentration levels spanning 80-120% of target concentration, measure in triplicate.",
            "Linear regression: correlation coefficient r^2 > 0.99 (typically r^2 > 0.995 expected),",
            "plot residuals to check for systematic bias (residuals random, no curvature).",
            "Report equation: y = mx + b, r^2, and concentration range.",
            "",
            "Range: interval between upper and lower concentrations where method validated.",
            "Typically 80-120% of test concentration, wider range (e.g., 50-150%) for content uniformity.",
            "Linearity, accuracy, precision demonstrated across entire range.",
            "",
            "Accuracy (trueness): closeness of measured value to true value, expressed as % recovery.",
            "Spike known amount into matrix (placebo or sample), measure, calculate recovery.",
            "Minimum 9 determinations: 3 concentrations (low, mid, high) in triplicate.",
            "Acceptance: 98-102% recovery for assay, 95-105% for impurities (ICH Q2 guidance).",
            "",
            "Precision: agreement among replicate measurements, expressed as %RSD (relative standard deviation).",
            "Repeatability (intra-day): same analyst, same day, 6 replicates, %RSD < 2% (assay), < 5-10% (impurities).",
            "Intermediate precision (inter-day): different days, different analysts, different instruments,",
            "demonstrates method robustness, %RSD < 3-5% typical acceptance.",
            "Reproducibility (inter-laboratory): different labs, used for compendial methods (USP, Ph. Eur.).",
            "",
            "Limit of Detection (LOD): lowest concentration giving detectable signal (S/N >= 3:1).",
            "Visual method: prepare serial dilutions until signal no longer distinguishable from noise.",
            "Signal-to-noise method: S/N = 3 (3 times baseline noise).",
            "Calculation method: LOD = 3.3 * sigma / slope (from linearity study, y-residual standard deviation).",
            "",
            "Limit of Quantitation (LOQ): lowest concentration quantified with acceptable precision and accuracy.",
            "S/N >= 10:1, %RSD < 10%, recovery 90-110%.",
            "Calculation: LOQ = 10 * sigma / slope. Verify by measuring 6 replicates at LOQ concentration.",
            "",
            "Robustness: method tolerance to deliberate variations in parameters.",
            "Examples: UV-Vis wavelength +/- 2 nm, pH +/- 0.2 units, flow rate +/- 10% (HPLC),",
            "temperature +/- 5 degrees C, reagent source/lot. Design of experiments (DOE) identifies critical parameters.",
            "Document which parameters affect results, set appropriate control limits in method.",
            "",
            "System suitability: parameters ensuring system operates properly before sample analysis.",
            "Examples: tailing factor (HPLC), resolution (NMR), mass accuracy (MS), baseline stability (UV-Vis).",
            "Run standards before sample batch, verify acceptance criteria met.",
            "",
            "Validation report: document all experiments, data, statistical analysis, conclusions,",
            "include raw data, representative chromatograms/spectra, validation protocol and SOP.",
            "Regulatory review: thorough documentation essential for approval, incomplete validation causes delays."
        ],
        key_factors=[
            "ICH Q2(R1) validation parameters applicable to method type (identity, assay, impurity)",
            "Specificity demonstration with forced degradation and interference testing",
            "Linearity range covering expected sample concentrations (80-120% typical)",
            "Accuracy at multiple spike levels (low, mid, high concentration)",
            "Precision repeatability (%RSD < 2% for assay) and intermediate precision",
            "LOD and LOQ determination method (S/N vs. statistical calculation)",
            "Robustness testing identifying critical method parameters",
            "System suitability criteria ensuring method performs correctly"
        ],
        primary_authority=[
            "ICH Q2(R1) Validation of Analytical Procedures: Text and Methodology (2005)",
            "FDA Guidance for Industry: Analytical Procedures and Methods Validation for Drugs and Biologics (2015)",
            "USP <1225> Validation of Compendial Procedures",
            "Ermer, J., Miller, J. H. M. (Eds.) (2005). Method Validation in Pharmaceutical Analysis.",
            "AOAC Guidelines for Single Laboratory Validation of Chemical Methods (2002)"
        ],
        burden_holder="Analyst / Method Developer",
        adversary_position="Incomplete or poorly documented validation leads to regulatory rejection or product recall",
        counter_arguments=[
            "Forced degradation conditions too harsh or too mild, not representative of real degradation",
            "Linearity demonstrated over narrow range, samples outside range fail validation",
            "Matrix effects not addressed, accuracy in real samples differs from spiked placebos",
            "Insufficient replicates or concentration levels for statistical significance",
            "Robustness testing omits critical parameters, method fails in routine use"
        ],
        resolution_strategy="Follow ICH Q2(R1) guidelines rigorously, consult regulatory guidance for product type (drug substance vs. drug product), design validation protocol before experiments, use quality-by-design (QbD) principles to identify critical parameters, perform full validation for regulatory submissions, use partial validation for method transfers, document all deviations and out-of-specification results with investigation.",
        domain=SpectroscopyDomain.VALIDATION,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ICH Q2(R1) Validation of Analytical Procedures (2005)"
    ),

    # Hyphenated Techniques Doctrine
    DoctrineBlock(
        topic="Hyphenated Techniques: GC-MS and LC-MS for Complex Mixture Analysis",
        keywords=["gc-ms", "lc-ms", "hyphenated", "chromatography", "mass spectrometry", "tandem ms"],
        conclusion_template=[
            "Hyphenated techniques combine separation (GC, LC) with detection (MS) for complex mixture analysis.",
            "GC-MS for volatile/thermally stable compounds, LC-MS for polar/non-volatile compounds.",
            "Tandem MS (MS/MS) provides structural confirmation and enhanced selectivity for trace analysis."
        ],
        reasoning_framework=[
            "Hyphenated techniques: online coupling of separation (chromatography) with spectroscopy (MS, IR, NMR),",
            "combines resolving power of chromatography with identification power of spectroscopy.",
            "GC-MS and LC-MS most common, routine in environmental, pharmaceutical, forensic, food analysis.",
            "",
            "Gas Chromatography-Mass Spectrometry (GC-MS): volatile compounds separated by GC,",
            "directly introduced to MS via heated transfer line (typically 280-300 C to prevent condensation).",
            "Ionization: electron ionization (EI, 70 eV hard ionization) provides fragmentation for structure elucidation,",
            "chemical ionization (CI, soft ionization with reagent gas) preserves molecular ion.",
            "Quadrupole MS most common (unit resolution, scan 50-500 amu in 0.5-1 s), TOF-MS for high resolution.",
            "",
            "GC-MS applications: volatile organic compounds (VOCs), pesticides, polychlorinated biphenyls (PCBs),",
            "polycyclic aromatic hydrocarbons (PAHs), drugs of abuse, explosives, flavors and fragrances,",
            "petroleum distillates, environmental contamination (soil, water, air).",
            "EPA 8270 (semivolatile organics by GC-MS), EPA 8260 (volatile organics), ASTM D2887 (petroleum boiling range).",
            "",
            "GC-MS advantages: EI fragmentation patterns in NIST library (300,000+ spectra) enable compound ID,",
            "high resolution (peak capacity >1000), sensitive (pg detection limits), robust and reproducible.",
            "Disadvantages: limited to volatile, thermally stable compounds (MW <600 Da typically),",
            "polar compounds require derivatization (silylation, acylation), no direct analysis of salts or polymers.",
            "",
            "Liquid Chromatography-Mass Spectrometry (LC-MS): polar, non-volatile, thermally labile compounds,",
            "reversed-phase HPLC (C18 column) with water-acetonitrile-formic acid gradient most common.",
            "Ionization: electrospray ionization (ESI) for polar compounds (peptides, proteins, metabolites),",
            "atmospheric pressure chemical ionization (APCI) for less polar (drugs, steroids, lipids),",
            "atmospheric pressure photoionization (APPI) for non-polar (PAHs, lipids).",
            "",
            "LC-MS applications: pharmaceuticals and metabolites, peptides and proteins (proteomics),",
            "environmental contaminants (pesticides, pharmaceuticals in water), food additives and contaminants,",
            "natural products, carbohydrates, nucleotides, vitamins.",
            "FDA guidance for bioanalytical method validation (LC-MS/MS for pharmacokinetics).",
            "",
            "LC-MS challenges: ion suppression from matrix components (salts, lipids, detergents),",
            "co-eluting compounds compete for ionization, reduces analyte signal unpredictably.",
            "Mitigation: sample cleanup (solid-phase extraction, SPE), use internal standards (stable isotope labeled),",
            "optimize chromatography to separate analyte from matrix peaks.",
            "",
            "Tandem Mass Spectrometry (MS/MS): select precursor ion in first analyzer (Q1),",
            "fragment by collision-induced dissociation (CID, inert gas collision cell),",
            "analyze product ions in second analyzer (Q3).",
            "Triple quadrupole (QqQ): Q1 selects precursor, q (collision cell) fragments, Q3 selects product.",
            "Selected reaction monitoring (SRM/MRM): monitor specific precursor-product transition (e.g., m/z 500 → 100),",
            "eliminates background, enhances selectivity and sensitivity (ppb-ppt detection limits).",
            "",
            "MS/MS applications: quantitation of target analytes in complex matrices (drugs in plasma, pesticides in food),",
            "newborn screening (tandem MS for inborn errors of metabolism), doping control (sports drug testing),",
            "environmental monitoring (PFAS, pharmaceuticals in wastewater), food safety (mycotoxins, veterinary drugs).",
            "",
            "High-resolution MS (HRMS): Q-TOF, Orbitrap provide accurate mass (<5 ppm error),",
            "enables molecular formula determination, distinguishes isobaric interferences,",
            "useful for unknown identification (non-targeted analysis) and confirmation of trace contaminants.",
            "Data-independent acquisition (DIA): fragment all ions in defined m/z windows,",
            "retrospective analysis possible (search data later for compounds not originally targeted).",
            "",
            "Quantitative LC-MS/MS: isotope dilution method with stable isotope labeled internal standards (SIL-IS),",
            "IS identical to analyte except 2H, 13C, 15N substitution, co-elutes and has same ionization efficiency,",
            "corrects for matrix effects, ion suppression, sample loss during preparation.",
            "Gold standard for bioanalytical quantitation (FDA guidance, EMA guidelines)."
        ],
        key_factors=[
            "Compound volatility and thermal stability (GC-MS vs. LC-MS selection)",
            "Ionization method (EI, CI for GC-MS; ESI, APCI, APPI for LC-MS) affecting fragmentation and sensitivity",
            "Chromatographic separation quality (resolution, peak width) for complex matrices",
            "Matrix effects causing ion suppression or enhancement in LC-MS",
            "MS/MS transitions (precursor and product ions) for selectivity and sensitivity",
            "Internal standard selection (structural analog vs. stable isotope labeled)",
            "Sample preparation (extraction, cleanup, derivatization) for analyte recovery and matrix removal",
            "Instrument type (quadrupole, TOF, Orbitrap, ion trap) determining resolution and mass accuracy"
        ],
        primary_authority=[
            "Gross, J. H. (2017). Mass Spectrometry: A Textbook, 3rd ed., Hyphenated Techniques Chapter",
            "FDA Guidance for Industry: Bioanalytical Method Validation (2018)",
            "EPA Method 8270E Semivolatile Organic Compounds by Gas Chromatography/Mass Spectrometry",
            "Niessen, W. M. A. (2006). Liquid Chromatography-Mass Spectrometry, 3rd ed.",
            "Ardrey, R. E. (2003). Liquid Chromatography-Mass Spectrometry: An Introduction."
        ],
        burden_holder="Analyst",
        adversary_position="Matrix effects and ion suppression limit LC-MS accuracy without proper internal standards and validation",
        counter_arguments=[
            "Ion suppression in LC-MS unpredictable, varies with matrix and co-eluting compounds",
            "GC-MS requires derivatization for polar compounds, adds complexity and potential artifacts",
            "MS/MS fragmentation not always predictable, multiple transitions needed for confirmation",
            "High-resolution MS generates massive datasets, requires advanced data processing tools",
            "Isotope-labeled internal standards expensive, not available for all analytes"
        ],
        resolution_strategy="Use isotope-labeled internal standards for accurate quantitation, optimize chromatography to minimize matrix effects (separate analyte from matrix peaks), validate method with matrix-matched standards and spiked samples, use HRMS for unknown identification and confirmation, employ post-column infusion to map ion suppression regions, perform method comparison with orthogonal techniques (ELISA, immunoassay).",
        domain=SpectroscopyDomain.HYPHENATED,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="FDA Bioanalytical Method Validation Guidance (2018) and EPA 8270E"
    ),

    # Additional UV-Vis Doctrine
    DoctrineBlock(
        topic="Fluorescence Spectroscopy for Sensitive Detection",
        keywords=["fluorescence", "emission", "excitation", "stokes shift", "quantum yield", "quenching"],
        conclusion_template=[
            "Fluorescence spectroscopy detects photon emission from excited electronic states, 10^3-10^6 times more sensitive than absorption.",
            "Stokes shift separates excitation and emission wavelengths, reduces background interference.",
            "Fluorescence quenching by oxygen, heavy atoms, or dynamic processes limits applicability."
        ],
        reasoning_framework=[
            "Fluorescence: molecule absorbs photon (excitation), reaches excited singlet state S1,",
            "relaxes to ground state S0 by emitting photon (emission, longer wavelength than excitation).",
            "Stokes shift: emission wavelength longer than excitation due to vibrational relaxation in S1,",
            "typical shift 20-100 nm, allows selective detection (excite at lambda1, detect at lambda2).",
            "",
            "Quantum yield (phi): fraction of absorbed photons resulting in fluorescence emission,",
            "phi = photons emitted / photons absorbed, ranges 0 to 1 (100%).",
            "High quantum yield fluorophores: fluorescein (phi ~0.9), rhodamine B (phi ~0.7), quantum dots (phi ~0.5-0.9).",
            "Low quantum yield: compounds with n→pi* transitions (carbonyls), heavy atom effect (iodine, bromine),",
            "intersystem crossing to triplet state (phosphorescence competes with fluorescence).",
            "",
            "Fluorescence intensity: proportional to concentration at low absorbance (A < 0.05),",
            "I_fluor = phi * I0 * epsilon * b * c, where I0 is excitation intensity, epsilon molar absorptivity.",
            "Inner filter effect: at high absorbance, excitation light absorbed before reaching full sample volume,",
            "emission light absorbed before exiting cuvette, causes non-linearity. Dilute samples to A < 0.05.",
            "",
            "Excitation and emission spectra: excitation spectrum (scan excitation wavelength, fix emission),",
            "mirrors absorption spectrum (but higher sensitivity). Emission spectrum (fix excitation, scan emission),",
            "shows Stokes-shifted emission profile. Both spectra fingerprint for compound identification.",
            "",
            "Quenching: reduction of fluorescence intensity by environmental factors or quencher molecules.",
            "Static quenching: fluorophore-quencher complex forms in ground state, complex non-fluorescent.",
            "Dynamic (collisional) quenching: excited state deactivated by collision with quencher (O2, I^-, acrylamide),",
            "Stern-Volmer equation: I0/I = 1 + Ksv[Q], Ksv is Stern-Volmer constant, [Q] quencher concentration.",
            "",
            "Oxygen quenching: dissolved O2 efficient quencher via energy transfer to triplet O2,",
            "degas samples (N2 purge, freeze-pump-thaw) for reproducible fluorescence measurements.",
            "Heavy atom effect: Br, I increase spin-orbit coupling, enhance intersystem crossing to triplet state,",
            "reduces fluorescence quantum yield (phosphorescence may increase).",
            "",
            "Applications: ultra-sensitive detection (ng/mL to pg/mL), immunoassays (fluorescent antibody labels),",
            "DNA sequencing (fluorescent dideoxy terminators), cell imaging (GFP, fluorescent dyes),",
            "environmental monitoring (PAHs, oil spills via fluorescence fingerprints),",
            "pharmaceutical analysis (vitamins, drugs with native fluorescence or derivatization).",
            "",
            "Time-resolved fluorescence: pulsed excitation, measure emission decay (fluorescence lifetime),",
            "discriminates short-lived autofluorescence (ns) from long-lived lanthanide chelates (microseconds).",
            "FRET (Förster resonance energy transfer): donor fluorophore transfers energy to acceptor non-radiatively,",
            "distance-dependent (1-10 nm range), used for protein-protein interactions, nucleic acid hybridization.",
            "",
            "Fluorescence polarization (anisotropy): measures rotational diffusion of fluorophore,",
            "large molecules rotate slowly (high polarization), small molecules rotate fast (low polarization).",
            "Binding assays: small fluorescent ligand binds large protein, polarization increases upon binding."
        ],
        key_factors=[
            "Quantum yield of fluorophore (structure-dependent, solvent-dependent)",
            "Stokes shift magnitude (affects spectral separation and sensitivity)",
            "Quenching by oxygen, heavy atoms, or dynamic quenchers (concentration-dependent)",
            "Inner filter effects at high absorbance (requires dilution to A < 0.05)",
            "Photobleaching of fluorophore under prolonged excitation (irreversible degradation)",
            "Solvent polarity effects on fluorescence (solvatochromism)",
            "Temperature effects on quantum yield and quenching rates",
            "Instrument sensitivity (detector PMT voltage, slit widths, integration time)"
        ],
        primary_authority=[
            "Lakowicz, J. R. (2006). Principles of Fluorescence Spectroscopy, 3rd ed.",
            "Valeur, B., Berberan-Santos, M. N. (2012). Molecular Fluorescence: Principles and Applications, 2nd ed.",
            "Guilbault, G. G. (Ed.) (1990). Practical Fluorescence, 2nd ed.",
            "ASTM E578 Standard Test Method for Linearity of Fluorescence Measuring Systems",
            "ICH Q2(R1) Section 2.1.4 Detection Limit and Quantitation Limit for Fluorescence"
        ],
        burden_holder="Analyst",
        adversary_position="Fluorescence quenching and photobleaching limit reproducibility and require careful control",
        counter_arguments=[
            "Oxygen quenching variable with dissolved O2 concentration (atmospheric pressure, temperature)",
            "Photobleaching reduces signal over time, especially under intense laser excitation",
            "Background fluorescence from solvents, cuvettes, impurities obscures weak signals",
            "Inner filter effects cause non-linearity at high concentrations",
            "Spectral overlap of excitation/emission with scattering (Rayleigh, Raman) complicates low-concentration measurements"
        ],
        resolution_strategy="Degas samples to eliminate oxygen quenching, use low excitation power to minimize photobleaching, subtract blank fluorescence from samples, dilute to avoid inner filter effects (A < 0.05), use synchronous fluorescence (scan excitation and emission simultaneously with constant offset) to reduce scatter, employ time-resolved fluorescence to discriminate autofluorescence from analyte signal.",
        domain=SpectroscopyDomain.FLUORESCENCE,
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Lakowicz (2006) Principles of Fluorescence Spectroscopy"
    ),

    # Additional IR Doctrine
    DoctrineBlock(
        topic="ATR-FTIR Sampling and Qualitative Analysis",
        keywords=["atr", "attenuated total reflectance", "ftir", "evanescent wave", "depth of penetration", "qualitative"],
        conclusion_template=[
            "ATR-FTIR enables direct solid and liquid analysis without sample preparation.",
            "Evanescent wave penetrates sample ~0.5-5 microns, surface-sensitive technique.",
            "Qualitative analysis by spectral library matching (correlation coefficient, hit quality index)."
        ],
        reasoning_framework=[
            "Attenuated Total Reflectance (ATR): IR beam undergoes total internal reflection at crystal-sample interface,",
            "evanescent wave extends into sample, absorbs at characteristic frequencies, reflected beam attenuated.",
            "ATR crystal materials: diamond (hardest, wide range 4000-400 cm^-1, expensive),",
            "ZnSe (3800-600 cm^-1, soft, scratches easily), Ge (5500-600 cm^-1, high refractive index, brittle).",
            "",
            "Depth of penetration (dp): distance evanescent wave extends into sample,",
            "dp = lambda / (2 * pi * n1 * sqrt(sin^2(theta) - (n2/n1)^2)), typically 0.5-5 microns.",
            "Depends on wavelength (longer wavelength, deeper penetration), refractive indices (crystal n1, sample n2),",
            "angle of incidence theta (45 degrees typical). Diamond ATR with 45 degree: dp ~2 microns at 1000 cm^-1.",
            "",
            "ATR advantages: no sample preparation (no KBr pellet, no Nujol mull), analyze solids directly,",
            "aqueous solutions (no NaCl windows), viscous liquids, powders, fibers, films, coatings.",
            "Single-reflection ATR for liquids, multiple-reflection (5-10 bounces) for higher sensitivity.",
            "",
            "ATR artifacts: band intensity distortion (stronger absorption at higher wavenumber compared to transmission),",
            "ATR correction algorithm (based on depth of penetration wavelength dependence) normalizes spectrum.",
            "Modern FTIR software applies ATR correction automatically, corrected spectra match transmission spectra.",
            "",
            "Pressure control: variable pressure ATR ensures good sample contact with crystal,",
            "critical for hard solids (polymers, pharmaceuticals). Insufficient pressure causes weak bands,",
            "excessive pressure may crack crystal (especially ZnSe, Ge).",
            "",
            "Qualitative analysis: compare unknown spectrum with reference library (10,000-100,000+ spectra),",
            "spectral matching algorithms calculate correlation coefficient or hit quality index (HQI).",
            "Match > 90-95% suggests same compound, 80-90% similar structure, <80% uncertain.",
            "Search algorithms: Euclidean distance, correlation coefficient, first derivative, absolute value.",
            "",
            "Spectral libraries: commercial (Aldrich, Sigma, Nicolet, Bio-Rad), NIST, user-created.",
            "Polymer libraries, pharmaceutical libraries, contaminant libraries specialized by industry.",
            "Unknown identification: search library, review top hits (compare functional groups),",
            "confirm structure with NMR, MS if available, not definitive structural determination.",
            "",
            "Limitations: weak bands from functional groups at low concentration may be missed,",
            "mixture spectra show overlapping bands (difficult to identify individual components without separation),",
            "library match quality depends on spectral preprocessing (baseline correction, normalization),",
            "subtle differences in crystalline form, solvation, or purity affect spectrum.",
            "",
            "Microspectroscopy: ATR coupled with IR microscope, analyze microgram samples,",
            "spot size ~100 microns, identify contaminants, defects, coatings, multilayer films.",
            "Mapping mode: collect spectra at grid of spatial positions, generate chemical image."
        ],
        key_factors=[
            "ATR crystal material (diamond vs. ZnSe vs. Ge) affecting wavelength range and durability",
            "Depth of penetration (wavelength-dependent, 0.5-5 microns typical) determining surface sensitivity",
            "Sample contact pressure (good contact essential for hard solids)",
            "ATR correction algorithm for band intensity normalization",
            "Spectral library quality and size (coverage of target compound classes)",
            "Spectral preprocessing (baseline correction, ATR correction, normalization) for accurate matching",
            "Sample heterogeneity (mixtures, coatings) complicating interpretation",
            "Moisture interference (atmospheric water vapor if sample hygroscopic)"
        ],
        primary_authority=[
            "Harrick, N. J. (1967). Internal Reflection Spectroscopy. Interscience Publishers.",
            "ASTM E1252 Standard Practice for General Techniques for Obtaining Infrared Spectra for Qualitative Analysis",
            "Perkins, W. D. (1986). Fourier Transform Infrared Spectroscopy, Part 4: ATR. J. Chem. Educ., 63, A5-A10.",
            "Smith, B. C. (2011). Fundamentals of Fourier Transform Infrared Spectroscopy, 2nd ed., ATR Chapter",
            "ASTM E2621 Standard Practice for Infrared Multivariate Quantitative Analysis"
        ],
        burden_holder="Analyst",
        adversary_position="ATR-FTIR qualitative ID by library match is presumptive, not definitive structural determination",
        counter_arguments=[
            "Library match may identify similar compounds incorrectly (isomers, homologs)",
            "Mixture spectra cause false matches if one component dominates",
            "Sample surface contamination analyzed instead of bulk (depth of penetration ~2 microns)",
            "Crystalline polymorphs have different spectra, library may not have all forms",
            "Poor contact from hard, irregular samples causes weak, distorted bands"
        ],
        resolution_strategy="Use multiple search algorithms (correlation, first derivative) and compare top hits, verify functional groups manually against reference spectra, analyze multiple spots on heterogeneous samples, use transmission FTIR (KBr pellet) to confirm ATR results for critical identifications, cross-check with complementary techniques (NMR, MS) for definitive structure, maintain updated user library with in-house compounds and standards.",
        domain=SpectroscopyDomain.IR_FTIR,
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="ASTM E1252 and Harrick (1967) ATR Fundamentals"
    ),
]


# ============================================================================
# SPECTROSCOPY ENGINE CLASS
# ============================================================================

class CHEM17SpectroscopyEngine:
    """
    TIE-Grade Spectroscopy Intelligence Engine
    Real spectroscopic expertise for UV-Vis, IR/FTIR, NMR, MS, Raman, XRF, AAS, ICP-OES analysis
    """

    def __init__(self):
        self.version = "1.0.0"
        self.port = 9299
        self.doctrines = DOCTRINE_CACHE
        self.query_count = 0
        self.metrics_history: List[QueryMetrics] = []
        self.coverage_stats = defaultdict(int)

        # Build keyword index for fast cache lookup
        self.keyword_index: Dict[str, List[int]] = defaultdict(list)
        for idx, doctrine in enumerate(self.doctrines):
            for keyword in doctrine.keywords:
                self.keyword_index[keyword.lower()].append(idx)

        logger.info(f"CHEM17 Spectroscopy Engine v{self.version} initialized on port {self.port}")
        logger.info(f"Loaded {len(self.doctrines)} doctrine blocks across {len(set(d.domain for d in self.doctrines))} domains")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        domain_filter: Optional[SpectroscopyDomain] = None
    ) -> Dict[str, Any]:
        """
        Three-layer spectroscopic analysis:
        Layer 1: Doctrine cache (0-50ms) - pre-compiled spectroscopic expertise
        Layer 2: Semantic retrieval (50-200ms) - keyword matching across doctrines
        Layer 3: Deep analysis (200-2000ms) - multi-doctrine synthesis
        """
        start_time = time.time()
        query_id = f"CHEM17_{self.query_count:06d}"
        self.query_count += 1

        # Normalize query for keyword matching
        query_lower = query.lower()
        query_tokens = set(query_lower.split())

        # Layer 1: Doctrine cache hit via keyword index
        triggered_doctrines = []
        for keyword, doctrine_indices in self.keyword_index.items():
            if keyword in query_lower:
                for idx in doctrine_indices:
                    doctrine = self.doctrines[idx]
                    if domain_filter is None or doctrine.domain == domain_filter:
                        if doctrine not in triggered_doctrines:
                            triggered_doctrines.append(doctrine)
                            self.coverage_stats[doctrine.topic] += 1

        cache_hit = len(triggered_doctrines) > 0

        # Layer 2: Semantic retrieval - if cache miss, find related doctrines
        if not cache_hit:
            triggered_doctrines = self._semantic_search(query_tokens, domain_filter)

        # Layer 3: Deep analysis - synthesize multiple doctrines
        response = self._synthesize_response(query, triggered_doctrines, mode)

        latency_ms = (time.time() - start_time) * 1000

        # Determine confidence level
        confidence = self._assess_confidence(triggered_doctrines, query)

        # Epistemic gaps - what we don't know
        epistemic_gaps = self._identify_gaps(query, triggered_doctrines)

        # Generate determinism hash
        determinism_hash = self._generate_determinism_hash(query, triggered_doctrines, mode)

        # Record metrics
        metrics = QueryMetrics(
            query_id=query_id,
            timestamp=time.time(),
            mode=mode,
            domain=triggered_doctrines[0].domain if triggered_doctrines else SpectroscopyDomain.UV_VIS,
            cache_hit=cache_hit,
            doctrines_triggered=[d.topic for d in triggered_doctrines],
            doctrines_missed=[d.topic for d in self.doctrines if d not in triggered_doctrines],
            latency_ms=latency_ms,
            confidence=confidence,
            epistemic_gaps=epistemic_gaps,
            determinism_hash=determinism_hash
        )
        self.metrics_history.append(metrics)

        return {
            "query_id": query_id,
            "query": query,
            "mode": mode.value,
            "response": response,
            "doctrines_applied": [d.topic for d in triggered_doctrines],
            "confidence": confidence.value,
            "latency_ms": round(latency_ms, 2),
            "cache_hit": cache_hit,
            "epistemic_gaps": epistemic_gaps,
            "determinism_hash": determinism_hash,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _semantic_search(
        self,
        query_tokens: Set[str],
        domain_filter: Optional[SpectroscopyDomain]
    ) -> List[DoctrineBlock]:
        """Semantic keyword matching fallback"""
        scored_doctrines = []

        for doctrine in self.doctrines:
            if domain_filter and doctrine.domain != domain_filter:
                continue

            # Score based on keyword overlap
            doctrine_keywords = set(kw.lower() for kw in doctrine.keywords)
            overlap = len(query_tokens & doctrine_keywords)

            # Also check reasoning framework for token matches
            reasoning_text = " ".join(doctrine.reasoning_framework).lower()
            framework_matches = sum(1 for token in query_tokens if token in reasoning_text)

            score = overlap * 3 + framework_matches

            if score > 0:
                scored_doctrines.append((score, doctrine))

        # Return top 5 by score
        scored_doctrines.sort(reverse=True, key=lambda x: x[0])
        return [d for _, d in scored_doctrines[:5]]

    def _synthesize_response(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode
    ) -> str:
        """Synthesize expert response from triggered doctrines"""
        if not doctrines:
            return self._generate_fallback_response(query)

        if mode == ResponseMode.FAST:
            return self._fast_response(doctrines)
        elif mode == ResponseMode.DEFENSE:
            return self._defense_response(doctrines, query)
        else:  # MEMO
            return self._memo_response(doctrines, query)

    def _fast_response(self, doctrines: List[DoctrineBlock]) -> str:
        """Concise response from doctrine conclusions"""
        primary = doctrines[0]
        response_lines = [
            f"**{primary.topic}**",
            "",
            *primary.conclusion_template,
            "",
            "**Key Factors:**"
        ]
        response_lines.extend(f"- {factor}" for factor in primary.key_factors[:5])

        if len(doctrines) > 1:
            response_lines.extend([
                "",
                "**Related Considerations:**"
            ])
            for doctrine in doctrines[1:3]:
                response_lines.append(f"- {doctrine.topic}: {doctrine.conclusion_template[0]}")

        return "\n".join(response_lines)

    def _defense_response(self, doctrines: List[DoctrineBlock], query: str) -> str:
        """Audit-ready response with full citations"""
        response_lines = [
            f"**Spectroscopic Analysis: {doctrines[0].topic}**",
            "",
            "**Executive Summary:**"
        ]
        response_lines.extend(doctrines[0].conclusion_template)
        response_lines.extend([
            "",
            "**Technical Foundation:**"
        ])

        # Full reasoning from primary doctrine
        response_lines.extend(doctrines[0].reasoning_framework[:20])

        response_lines.extend([
            "",
            "**Critical Factors:**"
        ])
        response_lines.extend(f"{i+1}. {factor}" for i, factor in enumerate(doctrines[0].key_factors))

        response_lines.extend([
            "",
            "**Authoritative References:**"
        ])
        response_lines.extend(f"- {ref}" for ref in doctrines[0].primary_authority)

        # Adversarial analysis
        response_lines.extend([
            "",
            "**Potential Challenges:**",
            f"- Adversary Position: {doctrines[0].adversary_position}",
            "",
            "**Counter-Arguments:**"
        ])
        response_lines.extend(f"- {arg}" for arg in doctrines[0].counter_arguments)

        response_lines.extend([
            "",
            "**Resolution Strategy:**",
            doctrines[0].resolution_strategy,
            "",
            f"**Confidence Level:** {doctrines[0].confidence.value}",
            f"**Controlling Precedent:** {doctrines[0].controlling_precedent or 'General Spectroscopic Principles'}"
        ])

        return "\n".join(response_lines)

    def _memo_response(self, doctrines: List[DoctrineBlock], query: str) -> str:
        """Comprehensive memo format"""
        response_lines = [
            "# TECHNICAL MEMORANDUM",
            f"## Subject: {doctrines[0].topic}",
            f"## Date: {datetime.utcnow().strftime('%Y-%m-%d')}",
            f"## Query: {query}",
            "",
            "---",
            "",
            "## 1. EXECUTIVE SUMMARY",
            ""
        ]
        response_lines.extend(doctrines[0].conclusion_template)

        response_lines.extend([
            "",
            "## 2. TECHNICAL ANALYSIS",
            ""
        ])
        response_lines.extend(doctrines[0].reasoning_framework)

        response_lines.extend([
            "",
            "## 3. CRITICAL FACTORS",
            ""
        ])
        for i, factor in enumerate(doctrines[0].key_factors, 1):
            response_lines.append(f"**{i}. {factor}**")

        response_lines.extend([
            "",
            "## 4. AUTHORITATIVE SUPPORT",
            ""
        ])
        response_lines.extend(f"- {ref}" for ref in doctrines[0].primary_authority)

        if doctrines[0].controlling_precedent:
            response_lines.extend([
                "",
                "**Controlling Precedent:**",
                f"{doctrines[0].controlling_precedent}"
            ])

        response_lines.extend([
            "",
            "## 5. ADVERSARIAL ANALYSIS",
            "",
            f"**Burden Holder:** {doctrines[0].burden_holder}",
            "",
            f"**Adversary Position:** {doctrines[0].adversary_position}",
            "",
            "**Counter-Arguments:**"
        ])
        response_lines.extend(f"- {arg}" for arg in doctrines[0].counter_arguments)

        response_lines.extend([
            "",
            "**Resolution Strategy:**",
            doctrines[0].resolution_strategy
        ])

        # Additional doctrines
        if len(doctrines) > 1:
            response_lines.extend([
                "",
                "## 6. RELATED CONSIDERATIONS",
                ""
            ])
            for doctrine in doctrines[1:]:
                response_lines.extend([
                    f"### {doctrine.topic}",
                    ""
                ])
                response_lines.extend(doctrine.conclusion_template)
                response_lines.append("")

        response_lines.extend([
            "",
            "## 7. CONFIDENCE ASSESSMENT",
            "",
            f"**Confidence Level:** {doctrines[0].confidence.value}",
            f"**Domain:** {doctrines[0].domain.value}",
            ""
        ])

        return "\n".join(response_lines)

    def _generate_fallback_response(self, query: str) -> str:
        """Fallback when no doctrines triggered"""
        return (
            f"**Query:** {query}\n\n"
            "**Status:** No direct spectroscopic doctrine matched this query.\n\n"
            "**Recommendation:** Please rephrase to include specific spectroscopic technique "
            "(UV-Vis, IR, NMR, MS, Raman, XRF, AAS, ICP-OES) or analytical parameter "
            "(Beer-Lambert law, chemical shift, fragmentation, fluorescence, etc.).\n\n"
            "**Available Domains:**\n"
            "- UV-Vis Spectroscopy (Beer-Lambert, chromophores, Woodward-Fieser rules)\n"
            "- IR/FTIR (functional groups, ATR, fingerprint region)\n"
            "- NMR (1H and 13C chemical shifts, coupling, DEPT)\n"
            "- Mass Spectrometry (EI, ESI, fragmentation patterns, isotope patterns)\n"
            "- Raman Spectroscopy (SERS, polarizability)\n"
            "- X-ray Techniques (XRF elemental analysis, XRD)\n"
            "- Atomic Spectroscopy (AAS, ICP-OES, trace metals)\n"
            "- Fluorescence (quantum yield, quenching, Stokes shift)\n"
            "- Method Validation (LOD, LOQ, linearity, accuracy, precision)\n"
            "- Hyphenated Techniques (GC-MS, LC-MS, MS/MS)"
        )

    def _assess_confidence(
        self,
        doctrines: List[DoctrineBlock],
        query: str
    ) -> ConfidenceLevel:
        """Assess confidence based on doctrine coverage and specificity"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        primary = doctrines[0]

        # Check query specificity
        query_lower = query.lower()
        specific_terms = sum(1 for kw in primary.keywords if kw.lower() in query_lower)

        if specific_terms >= 3 and len(doctrines) >= 2:
            return ConfidenceLevel.DEFENSIBLE
        elif specific_terms >= 2:
            return ConfidenceLevel.AGGRESSIVE
        elif specific_terms >= 1:
            return ConfidenceLevel.DISCLOSURE
        else:
            return ConfidenceLevel.HIGH_RISK

    def _identify_gaps(
        self,
        query: str,
        doctrines: List[DoctrineBlock]
    ) -> List[str]:
        """Identify epistemic gaps in coverage"""
        gaps = []

        # Check for multi-technique queries
        techniques_mentioned = []
        for domain in SpectroscopyDomain:
            if domain.value.lower().replace("_", " ") in query.lower():
                techniques_mentioned.append(domain.value)

        if len(techniques_mentioned) > len(set(d.domain for d in doctrines)):
            missing = set(techniques_mentioned) - set(d.domain.value for d in doctrines)
            if missing:
                gaps.append(f"Query mentions techniques not covered by triggered doctrines: {', '.join(missing)}")

        # Check for validation/quantitation keywords without validation doctrine
        validation_keywords = ["validation", "lod", "loq", "linearity", "accuracy", "precision"]
        if any(kw in query.lower() for kw in validation_keywords):
            if not any(d.domain == SpectroscopyDomain.VALIDATION for d in doctrines):
                gaps.append("Query implies method validation concerns, but validation doctrine not triggered")

        # Check for matrix effects
        matrix_keywords = ["matrix", "interference", "suppression", "enhancement"]
        if any(kw in query.lower() for kw in matrix_keywords):
            if not doctrines:
                gaps.append("Query concerns matrix effects, but no relevant doctrine covered this")

        return gaps

    def _generate_determinism_hash(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode
    ) -> str:
        """Generate SHA-256 hash for deterministic response verification"""
        determinism_input = f"{query}|{mode.value}|" + "|".join(d.topic for d in doctrines)
        return hashlib.sha256(determinism_input.encode()).hexdigest()[:16]

    def get_health(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        recent_metrics = self.metrics_history[-100:] if self.metrics_history else []

        if recent_metrics:
            avg_latency = sum(m.latency_ms for m in recent_metrics) / len(recent_metrics)
            cache_hit_rate = sum(1 for m in recent_metrics if m.cache_hit) / len(recent_metrics)
        else:
            avg_latency = 0
            cache_hit_rate = 0

        return {
            "status": "healthy",
            "version": self.version,
            "port": self.port,
            "doctrine_count": len(self.doctrines),
            "domains": list(set(d.domain.value for d in self.doctrines)),
            "query_count": self.query_count,
            "avg_latency_ms": round(avg_latency, 2),
            "cache_hit_rate": round(cache_hit_rate, 3),
            "top_triggered_doctrines": sorted(
                self.coverage_stats.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10],
            "timestamp": datetime.utcnow().isoformat()
        }


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., description="Spectroscopic analysis query")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    domain_filter: Optional[SpectroscopyDomain] = Field(None, description="Filter by spectroscopy domain")


class QueryResponse(BaseModel):
    query_id: str
    query: str
    mode: str
    response: str
    doctrines_applied: List[str]
    confidence: str
    latency_ms: float
    cache_hit: bool
    epistemic_gaps: List[str]
    determinism_hash: str
    timestamp: str


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

engine = CHEM17SpectroscopyEngine()
app = FastAPI(
    title="CHEM17 Spectroscopy Intelligence Engine",
    description="TIE-Grade spectroscopic analysis: UV-Vis, IR/FTIR, NMR, MS, Raman, XRF, AAS, ICP-OES",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main spectroscopic analysis endpoint"""
    try:
        result = engine.three_layer_response(
            query=request.query,
            mode=request.mode,
            domain_filter=request.domain_filter
        )
        return QueryResponse(**result)
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_endpoint():
    """Comprehensive health check"""
    return engine.get_health()


@app.get("/doctrines")
async def doctrines_endpoint(domain: Optional[SpectroscopyDomain] = None):
    """List available doctrines, optionally filtered by domain"""
    doctrines = engine.doctrines
    if domain:
        doctrines = [d for d in doctrines if d.domain == domain]

    return {
        "count": len(doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "domain": d.domain.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "authority_count": len(d.primary_authority)
            }
            for d in doctrines
        ]
    }


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "engine": "CHEM17 Spectroscopy Intelligence Engine",
        "version": engine.version,
        "port": engine.port,
        "status": "operational",
        "endpoints": {
            "POST /query": "Spectroscopic analysis query",
            "GET /health": "Engine health metrics",
            "GET /doctrines": "List available doctrines",
            "GET /domains": "List spectroscopy domains"
        },
        "domains": [d.value for d in SpectroscopyDomain],
        "modes": [m.value for m in ResponseMode]
    }


@app.get("/domains")
async def domains_endpoint():
    """List spectroscopy domains with counts"""
    domain_counts = Counter(d.domain for d in engine.doctrines)
    return {
        "domains": [
            {
                "domain": domain.value,
                "doctrine_count": domain_counts[domain],
                "description": {
                    SpectroscopyDomain.UV_VIS: "UV-Visible spectroscopy: Beer-Lambert, chromophores, Woodward-Fieser rules",
                    SpectroscopyDomain.IR_FTIR: "Infrared and FTIR: functional group identification, ATR sampling",
                    SpectroscopyDomain.NMR: "Nuclear Magnetic Resonance: 1H and 13C chemical shifts, coupling, DEPT",
                    SpectroscopyDomain.MASS_SPEC: "Mass Spectrometry: EI, ESI, fragmentation patterns, isotope patterns",
                    SpectroscopyDomain.RAMAN: "Raman spectroscopy: Stokes/anti-Stokes, SERS enhancement",
                    SpectroscopyDomain.XRAY: "X-ray techniques: XRF elemental analysis, XRD crystallography",
                    SpectroscopyDomain.ATOMIC: "Atomic spectroscopy: AAS, ICP-OES, trace metal analysis",
                    SpectroscopyDomain.FLUORESCENCE: "Fluorescence: emission, quantum yield, quenching, Stokes shift",
                    SpectroscopyDomain.VALIDATION: "Method validation: LOD, LOQ, linearity, accuracy, precision",
                    SpectroscopyDomain.HYPHENATED: "Hyphenated techniques: GC-MS, LC-MS, MS/MS"
                }[domain]
            }
            for domain in SpectroscopyDomain
        ]
    }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting CHEM17 Spectroscopy Engine on port {engine.port}")
    uvicorn.run(app, host="0.0.0.0", port=engine.port, log_level="info")
