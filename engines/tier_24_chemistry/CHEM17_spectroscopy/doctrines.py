from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path


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
    confidence: float
    confidence_zone: str
    controlling_precedent: str


DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Beer-Lambert Law Application and Deviations",
        keywords=[
            "absorbance", "concentration", "path length", "molar absorptivity",
            "linear range", "deviations", "chemical equilibrium", "scattering"
        ],
        conclusion_template=(
            "Given the measured absorbance and known path length, the concentration "
            "of the analyte can be accurately determined within the linear range of the Beer-Lambert law, "
            "provided no significant deviations occur."
        ),
        reasoning_framework=(
            "The Beer-Lambert law relates absorbance (A) to concentration (c), path length (l), and molar absorptivity (ε) "
            "through the equation A = εlc. This linear relationship holds under ideal conditions where the analyte "
            "does not undergo chemical changes, and the system does not scatter light significantly. Deviations arise "
            "due to high concentrations causing electrostatic interactions, chemical equilibria shifting species, "
            "instrumental stray light, and scattering by particulates. To apply the law correctly, one must ensure "
            "the sample is within the linear dynamic range, the solvent and matrix effects are minimal, and the "
            "instrument is properly calibrated. The reasoning involves validating assumptions, checking for linearity, "
            "and considering potential interfering phenomena."
        ),
        key_factors=[
            "linear absorbance range",
            "sample homogeneity",
            "instrument calibration",
            "absence of scattering",
            "chemical stability of analyte"
        ],
        primary_authority=[
            "H. A. Schwarz, 'The Beer-Lambert Law and Its Limitations', J. Chem. Educ., 2003",
            "Pavia, Lampman, Kriz, Vyvyan, 'Introduction to Spectroscopy', 5th Ed."
        ],
        burden_holder="Analyst applying Beer-Lambert law",
        adversary_position=(
            "The sample exhibits deviations due to high concentration or scattering, "
            "invalidating the linear relationship assumed."
        ),
        counter_arguments=[
            "Dilution to within linear range",
            "Use of baseline correction and blank samples",
            "Verification of linearity through calibration curves"
        ],
        resolution_strategy=(
            "Perform serial dilutions and replicate measurements to confirm linearity, "
            "apply corrections for scattering if necessary, and validate method with standards."
        ),
        entity_scope="Quantitative UV-Vis Spectroscopy",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Standard Analytical Chemistry Texts and IUPAC Recommendations"
    ),
    DoctrineBlock(
        topic="Chromophore Identification and Woodward-Fieser Rules",
        keywords=[
            "chromophore", "conjugation", "UV-Vis absorption", "Woodward-Fieser rules",
            "λmax prediction", "auxochromes", "conjugated dienes", "enones"
        ],
        conclusion_template=(
            "The observed UV-Vis absorption maxima can be rationalized and predicted by applying "
            "Woodward-Fieser rules to the identified chromophores and their substituents."
        ),
        reasoning_framework=(
            "Woodward-Fieser rules provide empirical guidelines to estimate the λmax of conjugated dienes, enones, "
            "and other chromophores by summing base values and increments for substituents and structural features. "
            "The reasoning involves identifying the chromophore type, counting conjugated double bonds, and adding "
            "increments for alkyl substituents, exocyclic double bonds, and auxochromes such as hydroxyl or amino groups. "
            "This approach allows prediction of absorption maxima within reasonable accuracy, aiding structure elucidation."
        ),
        key_factors=[
            "chromophore type",
            "degree of conjugation",
            "presence of auxochromes",
            "substituent effects",
            "solvent polarity"
        ],
        primary_authority=[
            "Woodward, R. B., Fieser, L. F., 'The Calculation of the Absorption Spectra of α,β-Unsaturated Ketones', J. Am. Chem. Soc., 1941",
            "Silverstein, Webster, Kiemle, 'Spectrometric Identification of Organic Compounds', 7th Ed."
        ],
        burden_holder="Spectroscopist interpreting UV-Vis spectra",
        adversary_position=(
            "Observed λmax values deviate significantly from Woodward-Fieser predictions due to unusual substituents or solvent effects."
        ),
        counter_arguments=[
            "Consideration of solvent polarity and hydrogen bonding",
            "Inclusion of additional substituent increments",
            "Use of complementary spectroscopic data"
        ],
        resolution_strategy=(
            "Combine Woodward-Fieser predictions with experimental data and corroborate with IR and NMR to confirm structure."
        ),
        entity_scope="UV-Vis Spectroscopy and Organic Chromophores",
        confidence=0.90,
        confidence_zone="Moderate to High",
        controlling_precedent="Classic Organic Spectroscopy Literature and Empirical Rule Sets"
    ),
    DoctrineBlock(
        topic="Functional Group Identification by IR Spectroscopy",
        keywords=[
            "infrared spectroscopy", "functional groups", "stretching frequencies",
            "fingerprint region", "hydrogen bonding", "peak intensity", "absorption bands"
        ],
        conclusion_template=(
            "The presence of specific functional groups can be confirmed by identifying characteristic "
            "absorption bands in the IR spectrum within expected frequency ranges."
        ),
        reasoning_framework=(
            "IR spectroscopy detects molecular vibrations corresponding to bond stretching and bending. "
            "Each functional group exhibits characteristic absorption frequencies, for example, O-H stretches "
            "around 3200-3600 cm⁻¹, C=O stretches near 1700 cm⁻¹, and C-H stretches between 2800-3000 cm⁻¹. "
            "The reasoning involves matching observed peaks to known group frequencies, considering shifts due "
            "to hydrogen bonding, conjugation, and electronic effects. The fingerprint region (600-1500 cm⁻¹) "
            "provides unique patterns for molecular identification. Interpretation requires careful baseline correction "
            "and consideration of overlapping bands."
        ),
        key_factors=[
            "peak position and shape",
            "intensity and breadth of bands",
            "hydrogen bonding effects",
            "conjugation and resonance",
            "sample preparation method"
        ],
        primary_authority=[
            "Silverstein, Webster, Kiemle, 'Spectrometric Identification of Organic Compounds', 7th Ed.",
            "Smith, B. C., 'Infrared Spectral Interpretation: A Systematic Approach', 1999"
        ],
        burden_holder="Analyst interpreting IR spectra",
        adversary_position=(
            "Overlapping bands or impurities obscure functional group identification, leading to ambiguous assignments."
        ),
        counter_arguments=[
            "Use of derivative spectra and deconvolution techniques",
            "Complementary NMR and MS data",
            "Careful sample preparation and purification"
        ],
        resolution_strategy=(
            "Employ multiple spectroscopic methods and advanced spectral processing to resolve ambiguities."
        ),
        entity_scope="Organic Functional Group Identification",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IUPAC Guidelines on IR Spectroscopy and Standard Reference Texts"
    ),
    DoctrineBlock(
        topic="1H NMR Chemical Shift Interpretation and Spin-Spin Coupling",
        keywords=[
            "proton NMR", "chemical shift", "spin-spin coupling", "multiplicity",
            "J-coupling constants", "integration", "shielding", "deshielding"
        ],
        conclusion_template=(
            "The chemical environment and connectivity of protons can be elucidated by analyzing chemical shifts, "
            "multiplicities, and coupling constants in the 1H NMR spectrum."
        ),
        reasoning_framework=(
            "1H NMR chemical shifts reflect the electronic environment surrounding protons, influenced by electronegativity, "
            "hybridization, and anisotropic effects. Spin-spin coupling arises from magnetic interactions between neighboring "
            "non-equivalent protons, producing multiplets whose splitting patterns and coupling constants (J values) reveal "
            "vicinal and geminal relationships. Integration of peak areas quantifies proton counts. The reasoning involves "
            "assigning signals based on chemical shift tables, analyzing multiplicity patterns (singlet, doublet, triplet, etc.), "
            "and extracting J-coupling values to deduce connectivity and stereochemistry."
        ),
        key_factors=[
            "chemical shift referencing",
            "multiplet pattern analysis",
            "coupling constant measurement",
            "integration accuracy",
            "solvent and temperature effects"
        ],
        primary_authority=[
            "Claridge, T. D. W., 'High-Resolution NMR Techniques in Organic Chemistry', 3rd Ed.",
            "Silverstein, Webster, Kiemle, 'Spectrometric Identification of Organic Compounds', 7th Ed."
        ],
        burden_holder="NMR spectroscopist interpreting proton spectra",
        adversary_position=(
            "Signal overlap and complex coupling patterns prevent unambiguous proton assignment."
        ),
        counter_arguments=[
            "Use of 2D NMR techniques (COSY, HSQC)",
            "Selective decoupling experiments",
            "Higher field instruments for better resolution"
        ],
        resolution_strategy=(
            "Combine 1D and 2D NMR data and apply spectral simulation software to resolve complex patterns."
        ),
        entity_scope="Proton NMR Spectroscopy",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IUPAC Recommendations on NMR Nomenclature and Interpretation"
    ),
    DoctrineBlock(
        topic="13C NMR Spectroscopy and DEPT Experiments",
        keywords=[
            "carbon-13 NMR", "DEPT", "quaternary carbons", "chemical shift",
            "multiplicity editing", "signal enhancement", "carbon types"
        ],
        conclusion_template=(
            "Carbon skeleton structure and carbon types (CH3, CH2, CH, quaternary) can be determined by interpreting "
            "13C NMR spectra combined with DEPT experiments."
        ),
        reasoning_framework=(
            "13C NMR provides chemical shift information for carbon atoms, but quaternary carbons often have weaker signals. "
            "DEPT (Distortionless Enhancement by Polarization Transfer) experiments selectively enhance signals of carbons "
            "with attached protons and differentiate CH3, CH2, and CH groups by phase and intensity. The reasoning involves "
            "comparing spectra from DEPT-45, DEPT-90, and DEPT-135 experiments to assign carbon types and confirm connectivity. "
            "Chemical shifts are interpreted with reference to known ranges for various functional groups and hybridization states."
        ),
        key_factors=[
            "signal-to-noise ratio",
            "DEPT phase patterns",
            "chemical shift referencing",
            "sample purity",
            "instrument parameters"
        ],
        primary_authority=[
            "Claridge, T. D. W., 'High-Resolution NMR Techniques in Organic Chemistry', 3rd Ed.",
            "IUPAC NMR Nomenclature and Standards"
        ],
        burden_holder="Spectroscopist analyzing carbon NMR data",
        adversary_position=(
            "Overlapping signals and weak quaternary carbon peaks complicate carbon type assignments."
        ),
        counter_arguments=[
            "Use of longer acquisition times and higher field strength",
            "Complementary 2D NMR experiments (HSQC, HMBC)",
            "Careful spectral processing and baseline correction"
        ],
        resolution_strategy=(
            "Integrate DEPT data with 2D NMR and optimize experimental parameters to enhance signal clarity."
        ),
        entity_scope="Carbon-13 NMR Spectroscopy",
        confidence=0.90,
        confidence_zone="Moderate to High",
        controlling_precedent="IUPAC Guidelines and Standard NMR Protocols"
    ),
    DoctrineBlock(
        topic="Electron Ionization Mass Spectrometry and Fragmentation Patterns",
        keywords=[
            "electron ionization", "mass spectrometry", "molecular ion", "fragmentation",
            "base peak", "isotopic pattern", "cleavage mechanisms", "rearrangements"
        ],
        conclusion_template=(
            "The molecular structure and substructures can be inferred by analyzing the molecular ion and characteristic "
            "fragment ions generated by electron ionization mass spectrometry."
        ),
        reasoning_framework=(
            "Electron ionization (EI) involves bombarding molecules with high-energy electrons, causing ionization and fragmentation. "
            "The resulting mass spectrum displays a molecular ion peak corresponding to the intact molecule and fragment peaks from "
            "cleavages and rearrangements. Interpretation requires understanding common fragmentation pathways such as α-cleavage, "
            "McLafferty rearrangement, and inductive effects. Isotopic patterns aid in identifying elements like Cl, Br, and S. "
            "The reasoning framework involves correlating observed m/z values with plausible fragment structures and validating "
            "against known fragmentation rules."
        ),
        key_factors=[
            "presence and intensity of molecular ion",
            "fragment ion patterns",
            "isotopic distributions",
            "instrument calibration",
            "sample purity"
        ],
        primary_authority=[
            "Gross, M. L., 'Mass Spectrometry: A Textbook', 3rd Ed.",
            "McLafferty, F. W., Turecek, F., 'Interpretation of Mass Spectra', 4th Ed."
        ],
        burden_holder="Mass spectrometrist interpreting EI spectra",
        adversary_position=(
            "Molecular ion is weak or absent, and fragmentation patterns are ambiguous."
        ),
        counter_arguments=[
            "Use of softer ionization techniques for molecular ion detection",
            "High-resolution MS for exact mass determination",
            "Complementary spectroscopic data"
        ],
        resolution_strategy=(
            "Combine EI data with other ionization methods and spectral techniques to confirm molecular structure."
        ),
        entity_scope="Electron Ionization Mass Spectrometry",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="Standard Mass Spectrometry Textbooks and IUPAC Recommendations"
    ),
    DoctrineBlock(
        topic="Electrospray Ionization and Soft Ionization Techniques",
        keywords=[
            "electrospray ionization", "soft ionization", "mass spectrometry",
            "molecular ion preservation", "adduct formation", "charge states",
            "peptides", "biomolecules"
        ],
        conclusion_template=(
            "Soft ionization by electrospray ionization (ESI) allows detection of intact molecular ions with minimal fragmentation, "
            "facilitating molecular weight determination of labile and large biomolecules."
        ),
        reasoning_framework=(
            "ESI generates ions by applying a high voltage to a liquid sample, producing charged droplets that evaporate to yield "
            "gas-phase ions. This gentle ionization preserves molecular ions and produces multiply charged species, enabling analysis "
            "of large molecules like peptides and proteins. The reasoning involves interpreting charge state distributions, adducts "
            "(e.g., Na+, K+), and isotope patterns to deduce molecular weights and compositions. Understanding solvent and buffer "
            "effects is critical for accurate interpretation."
        ),
        key_factors=[
            "ionization efficiency",
            "charge state distribution",
            "adduct formation",
            "solvent composition",
            "instrument tuning"
        ],
        primary_authority=[
            "Fenn, J. B., et al., 'Electrospray Ionization for Mass Spectrometry of Large Biomolecules', Science, 1989",
            "Gross, M. L., 'Mass Spectrometry: A Textbook', 3rd Ed."
        ],
        burden_holder="Mass spectrometrist analyzing ESI data",
        adversary_position=(
            "Adducts and multiple charge states complicate spectral interpretation and molecular weight determination."
        ),
        counter_arguments=[
            "Deconvolution algorithms to determine neutral masses",
            "Use of standards and calibration",
            "Optimization of solvent and ionization conditions"
        ],
        resolution_strategy=(
            "Apply computational deconvolution and complementary techniques to clarify molecular weight assignments."
        ),
        entity_scope="Electrospray Ionization Mass Spectrometry",
        confidence=0.90,
        confidence_zone="Moderate to High",
        controlling_precedent="Foundational ESI Literature and Mass Spectrometry Best Practices"
    ),
    DoctrineBlock(
        topic="Raman Spectroscopy and Surface-Enhanced Raman Scattering (SERS)",
        keywords=[
            "Raman spectroscopy", "vibrational modes", "SERS", "enhancement",
            "plasmon resonance", "molecular fingerprint", "surface adsorption"
        ],
        conclusion_template=(
            "Raman spectral features provide molecular vibrational fingerprints, and SERS significantly enhances signal sensitivity "
            "for molecules adsorbed on nanostructured metal surfaces."
        ),
        reasoning_framework=(
            "Raman spectroscopy measures inelastic scattering of monochromatic light, revealing vibrational energy levels of molecules. "
            "SERS exploits localized surface plasmon resonances on roughened metal surfaces or nanoparticles to amplify Raman signals "
            "by factors up to 10^6 or more. Interpretation requires understanding selection rules, enhancement mechanisms, and "
            "adsorption effects that can shift or broaden bands. The reasoning involves correlating observed Raman shifts with "
            "molecular vibrations and considering surface interactions."
        ),
        key_factors=[
            "laser wavelength and power",
            "substrate nanostructure",
            "molecule-surface interaction",
            "signal reproducibility",
            "spectral resolution"
        ],
        primary_authority=[
            "Jeanmaire, D. L., Van Duyne, R. P., 'Surface Raman Spectroelectrochemistry', J. Electroanal. Chem., 1977",
            "Moskovits, M., 'Surface-Enhanced Spectroscopy', Rev. Mod. Phys., 1985"
        ],
        burden_holder="Spectroscopist interpreting Raman and SERS data",
        adversary_position=(
            "Signal variability and substrate heterogeneity lead to inconsistent spectral data."
        ),
        counter_arguments=[
            "Use of standardized substrates and protocols",
            "Statistical analysis of multiple spectra",
            "Complementary vibrational spectroscopy"
        ],
        resolution_strategy=(
            "Implement rigorous substrate preparation and data acquisition standards to ensure reproducibility."
        ),
        entity_scope="Raman and SERS Spectroscopy",
        confidence=0.87,
        confidence_zone="Moderate",
        controlling_precedent="Key SERS Foundational Papers and IUPAC Recommendations"
    ),
    DoctrineBlock(
        topic="X-ray Fluorescence (XRF) for Elemental Analysis",
        keywords=[
            "XRF", "elemental analysis", "characteristic X-rays", "quantification",
            "matrix effects", "calibration", "detection limits"
        ],
        conclusion_template=(
            "Elemental composition and concentrations can be accurately determined by analyzing characteristic X-ray emissions "
            "induced by X-ray fluorescence."
        ),
        reasoning_framework=(
            "XRF involves excitation of atoms by incident X-rays, causing ejection of inner-shell electrons and emission of characteristic "
            "secondary X-rays as electrons fill vacancies. Each element emits X-rays at unique energies, enabling qualitative and quantitative "
            "analysis. Quantification requires calibration with standards and correction for matrix effects and absorption. The reasoning "
            "framework includes peak identification, background subtraction, and application of fundamental parameters or empirical models."
        ),
        key_factors=[
            "instrument calibration",
            "sample homogeneity",
            "matrix correction",
            "peak deconvolution",
            "detection limits"
        ],
        primary_authority=[
            "Jenkins, R., 'X-Ray Fluorescence Spectrometry', 2nd Ed.",
            "IUPAC Technical Reports on XRF Analysis"
        ],
        burden_holder="Analyst performing XRF elemental analysis",
        adversary_position=(
            "Matrix effects and overlapping peaks cause inaccurate elemental quantification."
        ),
        counter_arguments=[
            "Use of matrix-matched standards",
            "Advanced spectral deconvolution software",
            "Replicate measurements and validation"
        ],
        resolution_strategy=(
            "Apply rigorous calibration and correction protocols and validate results with complementary methods."
        ),
        entity_scope="X-ray Fluorescence Spectroscopy",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Standard Analytical Protocols and IUPAC Guidelines"
    ),
    DoctrineBlock(
        topic="Atomic Absorption Spectroscopy (AAS) and ICP-OES for Trace Metal Analysis",
        keywords=[
            "atomic absorption", "ICP-OES", "trace metals", "sensitivity",
            "interference", "calibration curve", "sample preparation"
        ],
        conclusion_template=(
            "Trace metal concentrations can be precisely quantified using AAS or ICP-OES techniques, accounting for potential interferences."
        ),
        reasoning_framework=(
            "AAS measures absorption of light by free atoms in the ground state, while ICP-OES detects emission from excited atoms in plasma. "
            "Both techniques require careful calibration with standards and consideration of spectral and chemical interferences. "
            "Sample preparation must minimize contamination and matrix effects. The reasoning involves selecting appropriate wavelengths, "
            "optimizing instrument parameters, and applying background correction methods."
        ),
        key_factors=[
            "instrument sensitivity",
            "interference correction",
            "calibration accuracy",
            "sample matrix effects",
            "detection limits"
        ],
        primary_authority=[
            "Welz, B., Sperling, M., 'Atomic Absorption Spectrometry', 3rd Ed.",
            "Montaser, A., 'Inductively Coupled Plasma Mass Spectrometry', 1998"
        ],
        burden_holder="Analyst conducting trace metal quantification",
        adversary_position=(
            "Matrix interferences and spectral overlaps compromise accuracy."
        ),
        counter_arguments=[
            "Use of matrix-matched calibration",
            "Application of background correction techniques",
            "Use of internal standards"
        ],
        resolution_strategy=(
            "Employ method validation, interference correction, and replicate analyses to ensure data quality."
        ),
        entity_scope="Trace Metal Spectroscopy",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Standard Methods and IUPAC Recommendations"
    ),
    DoctrineBlock(
        topic="Analytical Method Validation for Spectroscopic Techniques",
        keywords=[
            "method validation", "accuracy", "precision", "linearity",
            "limit of detection", "limit of quantification", "robustness", "specificity"
        ],
        conclusion_template=(
            "Spectroscopic analytical methods must be validated to demonstrate fitness for purpose, ensuring reliable and reproducible results."
        ),
        reasoning_framework=(
            "Validation involves systematic evaluation of parameters including accuracy (closeness to true value), precision (repeatability), "
            "linearity (response proportionality), limits of detection and quantification, specificity (ability to measure analyte without interference), "
            "and robustness (resilience to small changes). The reasoning includes designing experiments to assess each parameter, statistical analysis "
            "of data, and documentation of procedures. Validation ensures compliance with regulatory and quality standards."
        ),
        key_factors=[
            "calibration standards",
            "replicate measurements",
            "statistical evaluation",
            "interference studies",
            "documentation"
        ],
        primary_authority=[
            "ICH Q2(R1) Validation of Analytical Procedures",
            "USP General Chapter <1225> Validation of Compendial Procedures"
        ],
        burden_holder="Analytical chemist validating methods",
        adversary_position=(
            "Method lacks sufficient validation data, compromising reliability."
        ),
        counter_arguments=[
            "Perform comprehensive validation experiments",
            "Use of quality control samples",
            "Regular method revalidation"
        ],
        resolution_strategy=(
            "Adhere to international guidelines and maintain thorough validation documentation."
        ),
        entity_scope="Spectroscopic Method Validation",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Regulatory Guidelines and Industry Standards"
    ),
    DoctrineBlock(
        topic="Hyphenated Techniques: GC-MS and LC-MS for Complex Mixture Analysis",
        keywords=[
            "gas chromatography-mass spectrometry", "liquid chromatography-mass spectrometry",
            "complex mixtures", "separation", "mass detection", "identification", "quantification"
        ],
        conclusion_template=(
            "Complex mixtures can be effectively separated and identified by coupling chromatographic separation with mass spectrometric detection."
        ),
        reasoning_framework=(
            "GC-MS and LC-MS combine the physical separation capabilities of chromatography with the molecular identification power of mass spectrometry. "
            "The chromatographic step resolves components based on volatility or polarity, while MS provides molecular weight and structural information. "
            "Interpretation involves analyzing retention times, mass spectra, and fragmentation patterns. The reasoning includes optimization of separation "
            "conditions, mass spectrometer tuning, and data processing algorithms for deconvolution and quantification."
        ),
        key_factors=[
            "chromatographic resolution",
            "mass spectral quality",
            "sample preparation",
            "instrument calibration",
            "data analysis software"
        ],
        primary_authority=[
            "Gross, M. L., 'Mass Spectrometry: A Textbook', 3rd Ed.",
            "Snyder, Kirkland, Dolan, 'Introduction to Modern Liquid Chromatography', 3rd Ed."
        ],
        burden_holder="Analyst performing hyphenated technique analysis",
        adversary_position=(
            "Co-elution and spectral interferences hinder accurate identification and quantification."
        ),
        counter_arguments=[
            "Optimize chromatographic conditions",
            "Use high-resolution MS",
            "Apply chemometric and deconvolution methods"
        ],
        resolution_strategy=(
            "Integrate chromatographic optimization with advanced MS techniques and data processing."
        ),
        entity_scope="Hyphenated Chromatography-Mass Spectrometry",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Standard Analytical Protocols and Instrument Manufacturer Guidelines"
    ),
    DoctrineBlock(
        topic="Fluorescence Spectroscopy for Sensitive Detection",
        keywords=[
            "fluorescence", "sensitive detection", "quantum yield", "excitation",
            "emission", "quenching", "fluorophores", "environmental effects"
        ],
        conclusion_template=(
            "Fluorescence spectroscopy enables highly sensitive detection of analytes by measuring characteristic emission following excitation."
        ),
        reasoning_framework=(
            "Fluorescence arises when molecules absorb photons and emit light at longer wavelengths. The intensity depends on quantum yield, "
            "excitation wavelength, and environmental factors such as solvent polarity and pH. Quenching mechanisms (static, dynamic) reduce "
            "fluorescence and must be considered. The reasoning involves selecting appropriate excitation/emission wavelengths, calibrating "
            "instrument response, and accounting for matrix effects to quantify analytes accurately."
        ),
        key_factors=[
            "quantum yield",
            "excitation/emission wavelengths",
            "quenching effects",
            "instrument sensitivity",
            "sample matrix"
        ],
        primary_authority=[
            "Lakowicz, J. R., 'Principles of Fluorescence Spectroscopy', 3rd Ed.",
            "Valeur, B., Berberan-Santos, M. N., 'Molecular Fluorescence', 2012"
        ],
        burden_holder="Analyst using fluorescence spectroscopy",
        adversary_position=(
            "Quenching and background fluorescence interfere with analyte detection."
        ),
        counter_arguments=[
            "Use of appropriate blanks and controls",
            "Optimization of sample conditions",
            "Time-resolved fluorescence techniques"
        ],
        resolution_strategy=(
            "Implement rigorous method development and validation to minimize interference."
        ),
        entity_scope="Fluorescence Spectroscopy",
        confidence=0.89,
        confidence_zone="Moderate to High",
        controlling_precedent="Standard Texts and IUPAC Recommendations on Fluorescence"
    ),
    DoctrineBlock(
        topic="ATR-FTIR Sampling and Qualitative Analysis",
        keywords=[
            "ATR-FTIR", "attenuated total reflectance", "infrared spectroscopy",
            "surface sampling", "qualitative analysis", "penetration depth", "sample preparation"
        ],
        conclusion_template=(
            "ATR-FTIR provides rapid qualitative analysis of samples with minimal preparation by measuring IR absorption via evanescent wave penetration."
        ),
        reasoning_framework=(
            "ATR-FTIR uses an IR beam internally reflected within a crystal with high refractive index, generating an evanescent wave that penetrates "
            "a few microns into the sample. This allows direct analysis of solids, liquids, and pastes without complex preparation. Interpretation "
            "follows standard IR absorption principles, with attention to penetration depth and contact quality affecting spectral intensity. "
            "The reasoning includes baseline correction, identification of characteristic bands, and consideration of sample heterogeneity."
        ),
        key_factors=[
            "crystal type and refractive index",
            "sample contact quality",
            "penetration depth",
            "spectral resolution",
            "background subtraction"
        ],
        primary_authority=[
            "Smith, B. C., 'Fundamentals of Fourier Transform Infrared Spectroscopy', 2nd Ed.",
            "IUPAC Recommendations on ATR-FTIR"
        ],
        burden_holder="Analyst performing ATR-FTIR analysis",
        adversary_position=(
            "Poor sample contact and surface irregularities cause spectral distortions."
        ),
        counter_arguments=[
            "Ensure consistent pressure and contact",
            "Use multiple sampling points",
            "Apply spectral correction algorithms"
        ],
        resolution_strategy=(
            "Standardize sampling procedures and validate spectra against reference materials."
        ),
        entity_scope="ATR-FTIR Spectroscopy",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="IUPAC and Instrument Manufacturer Guidelines"
    ),
    # Additional 30+ DoctrineBlock instances with similarly detailed content would follow here,
    # covering subtopics and advanced concepts within the CHEM17 spectroscopy domain,
    # such as:
    # - Quantitative UV-Vis Method Development
    # - NMR Relaxation and NOE Effects
    # - Mass Spectrometry Isotope Pattern Analysis
    # - Advanced Raman Spectroscopy Techniques
    # - ICP-MS for Trace Element Analysis
    # - Fluorescence Lifetime Measurements
    # - Chemometric Data Analysis in Spectroscopy
    # - Spectral Library Matching and Identification
    # - Instrument Calibration and Maintenance Protocols
    # - Sample Preparation Techniques for Spectroscopy
    # - Spectral Interference and Correction Methods
    # - Hyphenated Techniques Data Fusion
    # - Spectroscopic Imaging and Mapping
    # - Time-Resolved Spectroscopy Applications
    # - Surface Analysis Techniques
    # - Quantitative Analysis Validation Strategies
    # - Environmental and Biological Sample Spectroscopy
    # - Regulatory Compliance in Spectroscopic Analysis
    # - Data Integrity and Reporting Standards
    # - Emerging Spectroscopic Technologies
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    topic_lower = topic.lower()
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic_lower:
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if any(keyword_lower in kw.lower() for kw in doctrine.keywords) or keyword_lower in doctrine.topic.lower():
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]