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
        topic="Gas Chromatography Fundamentals",
        keywords=[
            "gas chromatography",
            "GC",
            "retention time",
            "stationary phase",
            "mobile phase",
            "carrier gas",
            "column efficiency",
            "detector types"
        ],
        conclusion_template=(
            "The separation efficiency and analyte identification in gas chromatography "
            "depend primarily on the choice of stationary phase, carrier gas flow rate, "
            "and detector sensitivity."
        ),
        reasoning_framework=(
            "Gas Chromatography (GC) operates on the principle of partitioning analytes between "
            "a mobile gas phase and a stationary liquid or solid phase coated on the column. "
            "The retention time of each analyte is influenced by its volatility and affinity for "
            "the stationary phase. Optimizing carrier gas flow rate enhances resolution by balancing "
            "analysis time and peak broadening. Detector selection (FID, TCD, ECD) impacts sensitivity "
            "and selectivity. Column temperature programming allows for improved separation of complex mixtures. "
            "Understanding these parameters enables accurate qualitative and quantitative analysis."
        ),
        key_factors=[
            "stationary phase polarity",
            "carrier gas type and flow rate",
            "column temperature",
            "detector sensitivity",
            "sample injection technique"
        ],
        primary_authority=[
            "McNair, H.M., Miller, J.M. - Basic Gas Chromatography, 2nd Edition, Wiley, 1998",
            "Snyder, L.R., Kirkland, J.J., Dolan, J.W. - Introduction to Modern Liquid Chromatography, 3rd Edition, Wiley, 2010"
        ],
        burden_holder="Analyst performing GC method development",
        adversary_position=(
            "Claims that carrier gas flow rate has minimal impact on resolution and that detector "
            "choice is secondary to column selection."
        ),
        counter_arguments=[
            "Empirical data shows that flow rate adjustments directly affect peak shape and resolution.",
            "Detector sensitivity determines detection limits and selectivity, critical for trace analysis."
        ],
        resolution_strategy=(
            "Conduct controlled experiments varying flow rate and detector types while holding other "
            "parameters constant to demonstrate their impact on chromatographic performance."
        ),
        entity_scope="Analytical laboratories employing gas chromatography for volatile compound analysis",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="McNair & Miller, 1998; Snyder et al., 2010"
    ),
    DoctrineBlock(
        topic="High Performance Liquid Chromatography",
        keywords=[
            "HPLC",
            "liquid chromatography",
            "stationary phase",
            "mobile phase",
            "gradient elution",
            "isocratic elution",
            "column packing",
            "detectors"
        ],
        conclusion_template=(
            "HPLC separation quality is governed by the interaction between analytes and stationary phase, "
            "mobile phase composition, and system parameters such as flow rate and temperature."
        ),
        reasoning_framework=(
            "High Performance Liquid Chromatography (HPLC) separates analytes based on their differential "
            "partitioning between a liquid mobile phase and a solid or bonded stationary phase. The choice "
            "of stationary phase (e.g., C18, phenyl, ion-exchange) determines selectivity. Mobile phase "
            "composition, pH, and ionic strength influence analyte ionization and retention. Gradient elution "
            "improves separation of complex mixtures by changing mobile phase polarity over time. Flow rate and "
            "column temperature affect efficiency and peak shape. Detector types (UV-Vis, fluorescence, MS) "
            "enable qualitative and quantitative detection."
        ),
        key_factors=[
            "stationary phase chemistry",
            "mobile phase composition and pH",
            "gradient vs isocratic elution",
            "flow rate and temperature control",
            "detector selection"
        ],
        primary_authority=[
            "Snyder, L.R., Kirkland, J.J., Dolan, J.W. - Introduction to Modern Liquid Chromatography, 3rd Edition, Wiley, 2010",
            "Dong, M.W. - Modern HPLC for Practicing Scientists, Wiley, 2006"
        ],
        burden_holder="Chromatographer optimizing HPLC methods",
        adversary_position=(
            "Argues that isocratic elution is sufficient for all sample types and that temperature control "
            "has negligible effect on separation."
        ),
        counter_arguments=[
            "Gradient elution is essential for resolving complex mixtures with wide polarity ranges.",
            "Temperature influences solvent viscosity and analyte interaction kinetics, affecting resolution."
        ],
        resolution_strategy=(
            "Demonstrate improved peak resolution and reduced analysis time using gradient elution and "
            "controlled temperature experiments."
        ),
        entity_scope="Pharmaceutical, environmental, and food analysis laboratories utilizing HPLC",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Snyder et al., 2010; Dong, 2006"
    ),
    DoctrineBlock(
        topic="Mass Spectrometry Principles",
        keywords=[
            "mass spectrometry",
            "ionization",
            "mass analyzer",
            "detector",
            "mass-to-charge ratio",
            "fragmentation",
            "resolution",
            "sensitivity"
        ],
        conclusion_template=(
            "Mass spectrometry provides molecular weight and structural information through ionization, "
            "mass analysis, and detection of charged species."
        ),
        reasoning_framework=(
            "Mass Spectrometry (MS) involves ionizing chemical species to generate charged molecules or fragments, "
            "which are then separated based on their mass-to-charge (m/z) ratios using mass analyzers such as "
            "quadrupole, time-of-flight, or ion trap. Ionization techniques (EI, ESI, MALDI) affect the type and "
            "extent of fragmentation, influencing spectral interpretation. Detector systems convert ion signals "
            "to electrical signals for analysis. High resolution and accurate mass measurements enable "
            "identification of molecular formulas and structural elucidation. Tandem MS (MS/MS) provides further "
            "fragmentation data for complex mixtures."
        ),
        key_factors=[
            "ionization method",
            "mass analyzer type",
            "detector sensitivity",
            "resolution and mass accuracy",
            "sample introduction technique"
        ],
        primary_authority=[
            "Gross, M.L. - Mass Spectrometry: A Textbook, 3rd Edition, Springer, 2017",
            "de Hoffmann, E., Stroobant, V. - Mass Spectrometry: Principles and Applications, 3rd Edition, Wiley, 2007"
        ],
        burden_holder="Analyst interpreting mass spectra for compound identification",
        adversary_position=(
            "Claims that ionization method does not significantly affect fragmentation patterns and "
            "that low-resolution instruments suffice for all analyses."
        ),
        counter_arguments=[
            "Ionization technique critically influences fragmentation pathways and spectral complexity.",
            "High-resolution MS is necessary for distinguishing isobaric species and accurate mass determination."
        ],
        resolution_strategy=(
            "Compare spectra obtained with different ionization methods and resolutions to illustrate "
            "differences in identification confidence."
        ),
        entity_scope="Analytical laboratories employing MS for qualitative and quantitative analysis",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Gross, 2017; de Hoffmann & Stroobant, 2007"
    ),
    DoctrineBlock(
        topic="UV-Visible Spectroscopy",
        keywords=[
            "UV-Vis spectroscopy",
            "absorbance",
            "Beer-Lambert law",
            "chromophores",
            "wavelength",
            "molar absorptivity",
            "spectral scanning"
        ],
        conclusion_template=(
            "UV-Visible absorbance measurements allow quantitative determination of analytes based on "
            "their chromophore properties and adherence to the Beer-Lambert law."
        ),
        reasoning_framework=(
            "UV-Visible Spectroscopy measures the absorption of light in the ultraviolet and visible regions "
            "by molecules containing chromophores. The Beer-Lambert law relates absorbance (A) to concentration (c), "
            "path length (l), and molar absorptivity (ε) as A = εlc, enabling quantitative analysis. "
            "Spectral scanning identifies characteristic absorption maxima for qualitative analysis. "
            "Instrumental parameters such as slit width, detector linearity, and baseline correction affect "
            "accuracy. Sample preparation and solvent selection are critical to avoid interference."
        ),
        key_factors=[
            "chromophore presence",
            "wavelength selection",
            "path length accuracy",
            "instrument calibration",
            "sample matrix effects"
        ],
        primary_authority=[
            "Skoog, D.A., Holler, F.J., Crouch, S.R. - Principles of Instrumental Analysis, 7th Edition, Cengage, 2017",
            "Pavia, D.L., Lampman, G.M., Kriz, G.S., Vyvyan, J.R. - Introduction to Spectroscopy, 5th Edition, Cengage, 2014"
        ],
        burden_holder="Analyst performing quantitative UV-Vis measurements",
        adversary_position=(
            "Argues that Beer-Lambert law is universally valid regardless of concentration and matrix."
        ),
        counter_arguments=[
            "At high concentrations, deviations occur due to molecular interactions and stray light.",
            "Matrix components can cause scattering and baseline shifts affecting accuracy."
        ],
        resolution_strategy=(
            "Validate linearity range and perform matrix-matched calibrations to ensure reliable quantitation."
        ),
        entity_scope="Chemical, pharmaceutical, and environmental laboratories using UV-Vis spectroscopy",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Skoog et al., 2017; Pavia et al., 2014"
    ),
    DoctrineBlock(
        topic="Infrared Spectroscopy",
        keywords=[
            "infrared spectroscopy",
            "IR",
            "functional groups",
            "vibrational modes",
            "FTIR",
            "absorption bands",
            "fingerprint region"
        ],
        conclusion_template=(
            "Infrared spectroscopy enables identification of molecular functional groups through characteristic "
            "vibrational absorption bands."
        ),
        reasoning_framework=(
            "Infrared (IR) Spectroscopy detects molecular vibrations caused by absorption of IR radiation. "
            "Different functional groups absorb at characteristic frequencies, producing a spectrum with "
            "distinct bands. The fingerprint region (600-1500 cm⁻¹) provides unique patterns for compound identification. "
            "Fourier Transform Infrared (FTIR) instruments improve sensitivity and resolution. Sample preparation "
            "methods (KBr pellets, ATR) affect spectral quality. Interpretation relies on correlating absorption "
            "bands with known vibrational modes."
        ),
        key_factors=[
            "functional group identification",
            "spectral resolution",
            "sample preparation technique",
            "baseline correction",
            "instrument calibration"
        ],
        primary_authority=[
            "Smith, B.C. - Fundamentals of Fourier Transform Infrared Spectroscopy, 2nd Edition, CRC Press, 2011",
            "Silverstein, R.M., Webster, F.X., Kiemle, D.J. - Spectrometric Identification of Organic Compounds, 7th Edition, Wiley, 2005"
        ],
        burden_holder="Spectroscopist interpreting IR spectra for structural elucidation",
        adversary_position=(
            "Claims that IR spectra alone are insufficient for functional group identification due to overlapping bands."
        ),
        counter_arguments=[
            "While overlapping occurs, combined analysis of multiple regions and complementary techniques "
            "enhances identification confidence."
        ],
        resolution_strategy=(
            "Use derivative spectra, spectral libraries, and complementary NMR or MS data to confirm assignments."
        ),
        entity_scope="Organic chemistry and materials laboratories employing IR spectroscopy",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Smith, 2011; Silverstein et al., 2005"
    ),
    DoctrineBlock(
        topic="Nuclear Magnetic Resonance Spectroscopy",
        keywords=[
            "NMR",
            "chemical shift",
            "spin-spin coupling",
            "relaxation",
            "proton NMR",
            "carbon-13 NMR",
            "spectral interpretation"
        ],
        conclusion_template=(
            "NMR spectroscopy provides detailed molecular structure information through analysis of chemical shifts, "
            "coupling constants, and relaxation times."
        ),
        reasoning_framework=(
            "Nuclear Magnetic Resonance (NMR) spectroscopy exploits magnetic properties of certain nuclei (e.g., ¹H, ¹³C) "
            "in a magnetic field. Chemical shifts reflect electronic environment, while spin-spin coupling reveals "
            "neighboring nuclei interactions. Relaxation times (T1, T2) influence signal intensity and line shape. "
            "Multidimensional NMR techniques (COSY, HSQC, HMBC) enable correlation of nuclei for complex structure elucidation. "
            "Sample purity, solvent, and temperature affect spectral quality. Interpretation requires understanding "
            "of magnetic properties and molecular symmetry."
        ),
        key_factors=[
            "chemical shift referencing",
            "coupling pattern analysis",
            "sample concentration and purity",
            "magnetic field strength",
            "pulse sequence selection"
        ],
        primary_authority=[
            "Claridge, T.D.W. - High-Resolution NMR Techniques in Organic Chemistry, 3rd Edition, Elsevier, 2016",
            "Keeler, J. - Understanding NMR Spectroscopy, 2nd Edition, Wiley, 2010"
        ],
        burden_holder="NMR spectroscopist interpreting spectra for molecular structure determination",
        adversary_position=(
            "Suggests that NMR data alone is insufficient for definitive structure without complementary techniques."
        ),
        counter_arguments=[
            "While complementary data aids confirmation, high-quality NMR data can provide unambiguous structural assignments."
        ],
        resolution_strategy=(
            "Combine 1D and 2D NMR experiments and validate with synthetic or known reference compounds."
        ),
        entity_scope="Organic synthesis, pharmaceutical, and biochemical research laboratories",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Claridge, 2016; Keeler, 2010"
    ),
    DoctrineBlock(
        topic="Potentiometry and pH Measurement",
        keywords=[
            "potentiometry",
            "pH measurement",
            "electrode calibration",
            "reference electrode",
            "glass electrode",
            "Nernst equation",
            "ionic strength"
        ],
        conclusion_template=(
            "Accurate pH measurement requires proper electrode calibration, stable reference electrodes, and consideration "
            "of sample ionic strength."
        ),
        reasoning_framework=(
            "Potentiometric pH measurement uses a glass electrode sensitive to hydrogen ion activity and a stable reference electrode. "
            "The Nernst equation relates electrode potential to pH, with a theoretical slope of approximately 59 mV per pH unit at 25°C. "
            "Calibration with standard buffer solutions ensures accuracy. Ionic strength and temperature affect electrode response. "
            "Electrode maintenance and proper sample conditioning prevent measurement errors. Understanding these factors is essential "
            "for reliable pH determination."
        ),
        key_factors=[
            "electrode calibration frequency",
            "reference electrode stability",
            "sample ionic strength and temperature",
            "electrode conditioning",
            "buffer solution quality"
        ],
        primary_authority=[
            "Skoog, D.A., Holler, F.J., Crouch, S.R. - Principles of Instrumental Analysis, 7th Edition, Cengage, 2017",
            "Bates, R.G. - Determination of pH: Theory and Practice, Wiley, 1973"
        ],
        burden_holder="Analyst performing pH measurements in laboratory or field settings",
        adversary_position=(
            "Claims that electrode calibration is unnecessary if the instrument is recently serviced."
        ),
        counter_arguments=[
            "Regular calibration is critical to compensate for electrode drift and sample matrix effects."
        ],
        resolution_strategy=(
            "Implement routine calibration protocols using fresh standard buffers before measurements."
        ),
        entity_scope="Environmental, pharmaceutical, and chemical laboratories conducting pH analysis",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Skoog et al., 2017; Bates, 1973"
    ),
    DoctrineBlock(
        topic="Voltammetry and Electrochemical Detection",
        keywords=[
            "voltammetry",
            "electrochemical detection",
            "working electrode",
            "reference electrode",
            "counter electrode",
            "redox reactions",
            "current-potential curves"
        ],
        conclusion_template=(
            "Voltammetric techniques provide sensitive detection of electroactive species by measuring current response "
            "as a function of applied potential."
        ),
        reasoning_framework=(
            "Voltammetry involves applying a potential sweep to a working electrode immersed in an electrolyte containing "
            "the analyte. Redox-active species undergo oxidation or reduction at characteristic potentials, generating "
            "current peaks proportional to concentration. The reference electrode maintains a stable potential, while the "
            "counter electrode completes the circuit. Different voltammetric methods (cyclic, differential pulse, square wave) "
            "offer varying sensitivity and selectivity. Parameters such as scan rate, electrode material, and solution composition "
            "affect analytical performance."
        ),
        key_factors=[
            "electrode material and surface area",
            "scan rate and potential range",
            "supporting electrolyte composition",
            "analyte redox properties",
            "instrumental noise and baseline stability"
        ],
        primary_authority=[
            "Bard, A.J., Faulkner, L.R. - Electrochemical Methods: Fundamentals and Applications, 2nd Edition, Wiley, 2000",
            "Wang, J. - Analytical Electrochemistry, 3rd Edition, Wiley, 2006"
        ],
        burden_holder="Electrochemist developing voltammetric detection methods",
        adversary_position=(
            "Asserts that voltammetry lacks sensitivity compared to spectroscopic methods."
        ),
        counter_arguments=[
            "Voltammetry can achieve nanomolar detection limits with proper electrode design and technique optimization."
        ],
        resolution_strategy=(
            "Demonstrate detection limits and selectivity through controlled experiments and comparison with alternative methods."
        ),
        entity_scope="Environmental monitoring, clinical diagnostics, and industrial process control",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Bard & Faulkner, 2000; Wang, 2006"
    ),
    DoctrineBlock(
        topic="Acid-Base Titration",
        keywords=[
            "acid-base titration",
            "equivalence point",
            "indicator",
            "pH curve",
            "strong acid",
            "strong base",
            "weak acid",
            "weak base"
        ],
        conclusion_template=(
            "Accurate acid-base titration requires appropriate indicator selection and precise determination of the equivalence point."
        ),
        reasoning_framework=(
            "Acid-base titration quantifies analyte concentration by neutralization with a titrant of known concentration. "
            "The equivalence point corresponds to stoichiometric neutralization, detectable by pH changes or color indicators. "
            "Strong acid-strong base titrations show sharp pH jumps, while weak acid/base titrations have buffered regions and "
            "less distinct endpoints. Selection of an indicator with a pKa near the equivalence point ensures accurate endpoint detection. "
            "Titration curves and derivative plots aid in equivalence point determination. Proper technique minimizes systematic errors."
        ),
        key_factors=[
            "indicator pKa and color change range",
            "titrant concentration accuracy",
            "sample preparation and dilution",
            "endpoint detection method",
            "temperature control"
        ],
        primary_authority=[
            "Vogel, A.I. - Vogel's Textbook of Quantitative Chemical Analysis, 6th Edition, Pearson, 2000",
            "Skoog, D.A., West, D.M., Holler, F.J. - Fundamentals of Analytical Chemistry, 8th Edition, Brooks Cole, 2004"
        ],
        burden_holder="Analyst performing volumetric titrations",
        adversary_position=(
            "Claims that any indicator can be used regardless of titration type."
        ),
        counter_arguments=[
            "Mismatch between indicator pKa and equivalence point leads to inaccurate endpoint detection."
        ],
        resolution_strategy=(
            "Select indicators based on titration type and validate endpoint via pH meter or potentiometric methods."
        ),
        entity_scope="Chemical laboratories performing routine volumetric analyses",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Vogel, 2000; Skoog et al., 2004"
    ),
    DoctrineBlock(
        topic="Redox and Complexometric Titration",
        keywords=[
            "redox titration",
            "complexometric titration",
            "oxidation-reduction",
            "EDTA",
            "indicator",
            "equivalence point",
            "potentiometric titration"
        ],
        conclusion_template=(
            "Redox and complexometric titrations require careful selection of titrants and indicators to accurately determine analyte concentration."
        ),
        reasoning_framework=(
            "Redox titrations involve electron transfer reactions between analyte and titrant, with equivalence points detected by indicators or potentiometry. "
            "Complexometric titrations use chelating agents like EDTA to form stable complexes with metal ions. Indicators change color upon complex formation or release. "
            "Titration conditions such as pH, ionic strength, and masking agents influence selectivity and endpoint clarity. Potentiometric titrations provide objective endpoint detection. "
            "Understanding reaction stoichiometry and kinetics is essential for accurate quantitation."
        ),
        key_factors=[
            "titrant standardization",
            "indicator specificity",
            "pH and ionic strength control",
            "presence of interfering ions",
            "endpoint detection method"
        ],
        primary_authority=[
            "Vogel, A.I. - Vogel's Textbook of Quantitative Chemical Analysis, 6th Edition, Pearson, 2000",
            "Skoog, D.A., West, D.M., Holler, F.J. - Fundamentals of Analytical Chemistry, 8th Edition, Brooks Cole, 2004"
        ],
        burden_holder="Analyst conducting redox or complexometric titrations",
        adversary_position=(
            "Suggests that visual indicators are always sufficient for endpoint detection."
        ),
        counter_arguments=[
            "Visual endpoints may be subjective; potentiometric methods improve accuracy and reproducibility."
        ],
        resolution_strategy=(
            "Implement potentiometric endpoint detection and validate indicator performance under sample conditions."
        ),
        entity_scope="Environmental, pharmaceutical, and industrial laboratories",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Vogel, 2000; Skoog et al., 2004"
    ),
    DoctrineBlock(
        topic="Gravimetric Analysis",
        keywords=[
            "gravimetric analysis",
            "precipitation",
            "filtering",
            "drying",
            "weighing",
            "stoichiometry",
            "purity"
        ],
        conclusion_template=(
            "Gravimetric analysis yields accurate quantitative results through complete precipitation, proper sample handling, and precise weighing."
        ),
        reasoning_framework=(
            "Gravimetric analysis quantifies analytes by converting them into a stable, insoluble compound that can be isolated and weighed. "
            "Complete precipitation is critical to avoid analyte loss. The precipitate must be thoroughly washed to remove impurities, dried or ignited to constant weight, and weighed accurately. "
            "Stoichiometric relationships between analyte and precipitate allow calculation of analyte concentration. Errors arise from incomplete precipitation, co-precipitation, or moisture retention. "
            "Careful procedural control and validation ensure reliable results."
        ),
        key_factors=[
            "precipitate purity and stability",
            "washing and drying techniques",
            "weighing precision",
            "stoichiometric calculations",
            "sample homogeneity"
        ],
        primary_authority=[
            "Vogel, A.I. - Vogel's Textbook of Quantitative Chemical Analysis, 6th Edition, Pearson, 2000",
            "Skoog, D.A., West, D.M., Holler, F.J. - Fundamentals of Analytical Chemistry, 8th Edition, Brooks Cole, 2004"
        ],
        burden_holder="Analyst performing gravimetric determinations",
        adversary_position=(
            "Claims that gravimetric methods are outdated and less accurate than instrumental techniques."
        ),
        counter_arguments=[
            "Gravimetric analysis remains a gold standard for accuracy when properly executed, providing traceable results."
        ],
        resolution_strategy=(
            "Demonstrate method validation and comparison with instrumental methods to confirm accuracy."
        ),
        entity_scope="Quality control and research laboratories requiring precise quantitation",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Vogel, 2000; Skoog et al., 2004"
    ),
    DoctrineBlock(
        topic="Method Validation Parameters",
        keywords=[
            "method validation",
            "accuracy",
            "precision",
            "linearity",
            "limit of detection",
            "limit of quantitation",
            "specificity",
            "robustness"
        ],
        conclusion_template=(
            "Analytical methods must be validated for accuracy, precision, linearity, sensitivity, specificity, and robustness to ensure reliability."
        ),
        reasoning_framework=(
            "Method validation establishes the performance characteristics of an analytical procedure. Accuracy assesses closeness to true value, precision evaluates repeatability and reproducibility, and linearity confirms proportional response over concentration range. "
            "Limit of Detection (LOD) and Limit of Quantitation (LOQ) define sensitivity thresholds. Specificity ensures the method measures the analyte without interference. Robustness tests method resilience to small variations in parameters. "
            "Validation protocols follow regulatory guidelines (ICH, FDA, USP) and require statistical evaluation of data."
        ),
        key_factors=[
            "accuracy and recovery studies",
            "repeatability and intermediate precision",
            "calibration curve linearity",
            "LOD and LOQ determination",
            "interference and specificity testing",
            "robustness evaluation"
        ],
        primary_authority=[
            "ICH Q2(R1) - Validation of Analytical Procedures: Text and Methodology, 2005",
            "FDA Guidance for Industry - Analytical Procedures and Methods Validation, 2015"
        ],
        burden_holder="Method developer and quality assurance personnel",
        adversary_position=(
            "Argues that partial validation is sufficient for method acceptance."
        ),
        counter_arguments=[
            "Comprehensive validation ensures method reliability and regulatory compliance."
        ],
        resolution_strategy=(
            "Perform full validation studies following established guidelines and document results."
        ),
        entity_scope="Pharmaceutical, environmental, and food testing laboratories",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="ICH Q2(R1), 2005; FDA Guidance, 2015"
    ),
    DoctrineBlock(
        topic="Quality Control and Statistical Analysis",
        keywords=[
            "quality control",
            "statistical process control",
            "control charts",
            "outlier detection",
            "repeatability",
            "reproducibility",
            "measurement uncertainty"
        ],
        conclusion_template=(
            "Effective quality control employs statistical tools to monitor analytical performance and ensure data integrity."
        ),
        reasoning_framework=(
            "Quality Control (QC) involves systematic procedures to maintain analytical method performance within defined limits. "
            "Statistical Process Control (SPC) uses control charts (e.g., Shewhart, CUSUM) to detect trends and outliers. "
            "Repeatability and reproducibility studies quantify method precision. Measurement uncertainty estimates the range within which true values lie. "
            "Outlier tests (Grubbs, Dixon) identify aberrant data points. QC samples, blanks, and standards are integral to monitoring. "
            "Data evaluation and corrective actions maintain compliance with regulatory standards."
        ),
        key_factors=[
            "control chart implementation",
            "precision and accuracy monitoring",
            "outlier and trend analysis",
            "measurement uncertainty estimation",
            "documentation and corrective actions"
        ],
        primary_authority=[
            "Harris, D.C. - Quantitative Chemical Analysis, 9th Edition, W.H. Freeman, 2015",
            "ISO/IEC 17025 - General requirements for the competence of testing and calibration laboratories, 2017"
        ],
        burden_holder="Quality control managers and laboratory supervisors",
        adversary_position=(
            "Suggests that visual inspection of data suffices for quality assurance."
        ),
        counter_arguments=[
            "Statistical analysis provides objective and quantitative assessment of method performance."
        ],
        resolution_strategy=(
            "Implement SPC tools and train personnel in statistical data interpretation."
        ),
        entity_scope="All analytical laboratories requiring data quality assurance",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Harris, 2015; ISO/IEC 17025, 2017"
    ),
    DoctrineBlock(
        topic="Good Laboratory Practices and Compliance",
        keywords=[
            "good laboratory practices",
            "GLP",
            "documentation",
            "traceability",
            "audit trails",
            "standard operating procedures",
            "regulatory compliance"
        ],
        conclusion_template=(
            "Adherence to Good Laboratory Practices ensures data integrity, traceability, and regulatory compliance in analytical laboratories."
        ),
        reasoning_framework=(
            "Good Laboratory Practices (GLP) encompass organizational processes and conditions under which laboratory studies are planned, performed, monitored, recorded, and reported. "
            "Key elements include thorough documentation, traceability of samples and reagents, validated methods, and equipment calibration. "
            "Audit trails and training records support compliance verification. GLP adherence minimizes errors, ensures reproducibility, and facilitates regulatory inspections. "
            "Implementation requires management commitment, staff training, and continuous improvement."
        ),
        key_factors=[
            "comprehensive documentation",
            "method and equipment validation",
            "sample traceability",
            "training and competency records",
            "internal and external audits"
        ],
        primary_authority=[
            "OECD Principles of Good Laboratory Practice, 1998",
            "FDA 21 CFR Part 58 - Good Laboratory Practice for Nonclinical Laboratory Studies, 2009"
        ],
        burden_holder="Laboratory management and quality assurance personnel",
        adversary_position=(
            "Claims that GLP requirements are bureaucratic and impede scientific flexibility."
        ),
        counter_arguments=[
            "GLP ensures reliability and credibility of data critical for regulatory acceptance and public trust."
        ],
        resolution_strategy=(
            "Balance procedural rigor with scientific innovation through risk-based approaches and continuous training."
        ),
        entity_scope="Contract research organizations, pharmaceutical, and regulatory laboratories",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="OECD GLP, 1998; FDA 21 CFR Part 58, 2009"
    ),
    DoctrineBlock(
        topic="Calibration Methods and Standards",
        keywords=[
            "calibration",
            "standards",
            "traceability",
            "primary standards",
            "secondary standards",
            "instrument calibration",
            "uncertainty"
        ],
        conclusion_template=(
            "Accurate calibration using traceable standards is essential for reliable analytical measurements."
        ),
        reasoning_framework=(
            "Calibration aligns instrument response with known standards to ensure measurement accuracy. "
            "Primary standards are highly pure substances with well-characterized properties, used to prepare secondary standards. "
            "Traceability to national or international standards ensures comparability. Calibration procedures must consider uncertainty sources and be documented. "
            "Regular calibration intervals and verification maintain instrument performance. Calibration curves relate instrument response to analyte concentration."
        ),
        key_factors=[
            "standard purity and stability",
            "traceability chain",
            "calibration frequency",
            "instrument response linearity",
            "uncertainty estimation"
        ],
        primary_authority=[
            "Taylor, B.N., Kuyatt, C.E. - Guidelines for Evaluating and Expressing the Uncertainty of NIST Measurement Results, NIST Technical Note 1297, 1994",
            "ISO/IEC 17025 - General requirements for the competence of testing and calibration laboratories, 2017"
        ],
        burden_holder="Analyst and quality assurance personnel responsible for calibration",
        adversary_position=(
            "Suggests that calibration can be skipped if instrument shows stable performance."
        ),
        counter_arguments=[
            "Instrument drift and environmental factors necessitate regular calibration to maintain accuracy."
        ],
        resolution_strategy=(
            "Establish and adhere to calibration schedules with documented verification."
        ),
        entity_scope="All analytical laboratories requiring quantitative measurements",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Taylor & Kuyatt, 1994; ISO/IEC 17025, 2017"
    ),
    DoctrineBlock(
        topic="Atomic Absorption Spectroscopy",
        keywords=[
            "atomic absorption spectroscopy",
            "AAS",
            "flame atomization",
            "graphite furnace",
            "absorbance",
            "elemental analysis",
            "interferences"
        ],
        conclusion_template=(
            "Atomic Absorption Spectroscopy enables sensitive elemental quantification through atomization and absorbance measurement."
        ),
        reasoning_framework=(
            "AAS measures the absorption of light by free atoms in the ground state. Samples are atomized in a flame or graphite furnace to produce atomic vapor. "
            "Element-specific hollow cathode lamps provide radiation at characteristic wavelengths. Absorbance is proportional to element concentration following Beer-Lambert law. "
            "Matrix interferences, background absorption, and chemical interferences affect accuracy and require correction techniques such as background correction and matrix matching. "
            "Proper calibration and instrument optimization are essential for reliable results."
        ),
        key_factors=[
            "atomization technique",
            "lamp selection and alignment",
            "background correction",
            "sample matrix effects",
            "calibration and standards"
        ],
        primary_authority=[
            "Welz, B., Sperling, M. - Atomic Absorption Spectrometry, 3rd Edition, Wiley-VCH, 1999",
            "Skoog, D.A., Holler, F.J., Crouch, S.R. - Principles of Instrumental Analysis, 7th Edition, Cengage, 2017"
        ],
        burden_holder="Analyst performing elemental analysis by AAS",
        adversary_position=(
            "Claims that flame atomization is universally superior to graphite furnace atomization."
        ),
        counter_arguments=[
            "Graphite furnace offers higher sensitivity and lower detection limits for trace elements."
        ],
        resolution_strategy=(
            "Select atomization technique based on analyte concentration and matrix complexity."
        ),
        entity_scope="Environmental, clinical, and industrial elemental analysis laboratories",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Welz & Sperling, 1999; Skoog et al., 2017"
    ),
    DoctrineBlock(
        topic="Inductively Coupled Plasma Spectroscopy",
        keywords=[
            "inductively coupled plasma",
            "ICP-OES",
            "ICP-MS",
            "elemental analysis",
            "plasma source",
            "mass spectrometry",
            "optical emission"
        ],
        conclusion_template=(
            "ICP spectroscopy provides multi-elemental analysis with high sensitivity and dynamic range using plasma excitation."
        ),
        reasoning_framework=(
            "Inductively Coupled Plasma (ICP) sources generate high-temperature plasma to atomize and excite elements in samples. "
            "ICP-OES measures emitted light at element-specific wavelengths, while ICP-MS detects ions based on mass-to-charge ratio. "
            "ICP techniques offer rapid, multi-element analysis with low detection limits. Sample introduction systems and plasma stability affect performance. "
            "Interferences such as spectral overlap and matrix effects require correction strategies. Calibration with standards ensures quantitative accuracy."
        ),
        key_factors=[
            "plasma stability and power",
            "sample introduction efficiency",
            "spectral interferences",
            "calibration and internal standards",
            "instrument sensitivity"
        ],
        primary_authority=[
            "Montaser, A., Golightly, D.W. - Inductively Coupled Plasma in Analytical Atomic Spectrometry, 2nd Edition, Wiley, 1992",
            "Skoog, D.A., Holler, F.J., Crouch, S.R. - Principles of Instrumental Analysis, 7th Edition, Cengage, 2017"
        ],
        burden_holder="Analyst conducting elemental analysis by ICP techniques",
        adversary_position=(
            "Argues that ICP-MS is prone to excessive interferences making it unreliable."
        ),
        counter_arguments=[
            "Advanced collision/reaction cells and mathematical corrections mitigate interferences effectively."
        ],
        resolution_strategy=(
            "Implement interference correction protocols and validate with certified reference materials."
        ),
        entity_scope="Environmental, pharmaceutical, and materials laboratories",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Montaser & Golightly, 1992; Skoog et al., 2017"
    ),
    DoctrineBlock(
        topic="Sampling Theory and Representative Sampling",
        keywords=[
            "sampling theory",
            "representative sampling",
            "sample heterogeneity",
            "sampling error",
            "composite sampling",
            "incremental sampling",
            "sample size"
        ],
        conclusion_template=(
            "Representative sampling minimizes bias and error, ensuring analytical results accurately reflect the bulk material."
        ),
        reasoning_framework=(
            "Sampling theory addresses the principles for obtaining samples that accurately represent the whole population or lot. "
            "Heterogeneity in materials introduces sampling error, which can be minimized by appropriate sample size, number of increments, and mixing. "
            "Composite and incremental sampling strategies reduce variability. Proper sample handling and preservation prevent alteration. "
            "Statistical methods quantify sampling uncertainty and guide sampling plan design. Representative sampling is foundational for valid analysis."
        ),
        key_factors=[
            "material heterogeneity",
            "sample size and number of increments",
            "sampling method and tools",
            "sample preservation",
            "statistical evaluation of sampling error"
        ],
        primary_authority=[
            "Gy, P.M. - Sampling of Particulate Materials: Theory and Practice, Elsevier, 1998",
            "ASTM D6913 - Standard Practice for Particle-Size Distribution of Soils, 2017"
        ],
        burden_holder="Sampling personnel and analysts relying on sample representativeness",
        adversary_position=(
            "Claims that small grab samples suffice regardless of material heterogeneity."
        ),
        counter_arguments=[
            "Insufficient sampling leads to biased results and poor decision-making."
        ],
        resolution_strategy=(
            "Design sampling plans based on material characteristics and validate representativeness statistically."
        ),
        entity_scope="Environmental, mining, agricultural, and industrial sampling operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Gy, 1998; ASTM D6913, 2017"
    ),
    DoctrineBlock(
        topic="Sample Preparation and Extraction",
        keywords=[
            "sample preparation",
            "extraction",
            "solid phase extraction",
            "liquid-liquid extraction",
            "digestion",
            "matrix effects",
            "clean-up"
        ],
        conclusion_template=(
            "Effective sample preparation and extraction techniques are critical for isolating analytes and minimizing matrix interferences."
        ),
        reasoning_framework=(
            "Sample preparation transforms raw samples into forms suitable for analysis, often involving extraction of analytes from complex matrices. "
            "Techniques include solid phase extraction (SPE), liquid-liquid extraction (LLE), microwave digestion, and filtration. "
            "Proper selection depends on analyte properties and matrix complexity. Clean-up steps reduce matrix interferences enhancing detection. "
            "Recovery efficiency and reproducibility are key performance metrics. Inadequate preparation leads to inaccurate results and instrument contamination."
        ),
        key_factors=[
            "extraction efficiency",
            "matrix complexity",
            "clean-up procedures",
            "sample stability",
            "method reproducibility"
        ],
        primary_authority=[
            "Poole, C.F. - Sample Preparation for Trace Element Analysis, Elsevier, 2003",
            "Skoog, D.A., Holler, F.J., Crouch, S.R. - Principles of Instrumental Analysis, 7th Edition, Cengage, 2017"
        ],
        burden_holder="Analyst responsible for sample preparation protocols",
        adversary_position=(
            "Suggests minimal sample preparation is adequate for all analyses."
        ),
        counter_arguments=[
            "Complex matrices require tailored preparation to avoid interferences and ensure analyte recovery."
        ],
        resolution_strategy=(
            "Validate extraction methods with recovery studies and matrix-matched standards."
        ),
        entity_scope="Environmental, pharmaceutical, and food safety laboratories",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Poole, 2003; Skoog et al., 2017"
    ),
    DoctrineBlock(
        topic="Environmental Analysis Methods",
        keywords=[
            "environmental analysis",
            "trace contaminants",
            "water quality",
            "air monitoring",
            "soil analysis",
            "regulatory standards",
            "sample preservation"
        ],
        conclusion_template=(
            "Environmental analysis requires sensitive, validated methods and strict sample handling to meet regulatory standards."
        ),
        reasoning_framework=(
            "Environmental analysis monitors pollutants in water, air, and soil to assess compliance and ecological impact. "
            "Methods must detect trace levels with high specificity and accuracy. Sample collection, preservation, and transport protocols prevent analyte degradation or contamination. "
            "Regulatory guidelines (EPA, ISO) dictate method performance criteria. Quality control includes blanks, spikes, and duplicates. "
            "Data interpretation considers temporal and spatial variability. Method selection balances sensitivity, throughput, and cost."
        ),
        key_factors=[
            "method sensitivity and specificity",
            "sample preservation and storage",
            "regulatory compliance",
            "quality control procedures",
            "data interpretation and reporting"
        ],
        primary_authority=[
            "EPA Methods for Chemical Analysis of Water and Wastes, 1983",
            "ISO 17025 - General requirements for the competence of testing and calibration laboratories, 2017"
        ],
        burden_holder="Environmental analysts and regulatory compliance officers",
        adversary_position=(
            "Claims that rapid screening methods can replace validated quantitative methods."
        ),
        counter_arguments=[
            "Screening methods lack the accuracy and precision required for regulatory decisions."
        ],
        resolution_strategy=(
            "Use screening for preliminary assessment and confirmatory validated methods for compliance."
        ),
        entity_scope="Environmental monitoring agencies and contract laboratories",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA, 1983; ISO 17025, 2017"
    ),
    DoctrineBlock(
        topic="Pharmaceutical and Clinical Analysis",
        keywords=[
            "pharmaceutical analysis",
            "clinical analysis",
            "bioanalytical methods",
            "stability testing",
            "assay validation",
            "therapeutic drug monitoring",
            "sample matrix"
        ],
        conclusion_template=(
            "Pharmaceutical and clinical analyses require validated, sensitive methods to ensure drug safety, efficacy, and patient monitoring."
        ),
        reasoning_framework=(
            "Pharmaceutical analysis encompasses assay of active ingredients, impurities, and degradation products. "
            "Clinical analysis involves quantifying drugs and biomarkers in biological matrices. "
            "Methods must be validated for accuracy, precision, selectivity, and sensitivity considering complex matrices like plasma or urine. "
            "Stability testing ensures drug integrity over shelf life. Therapeutic drug monitoring optimizes dosing. "
            "Regulatory guidelines (ICH, FDA) govern method development and validation. Sample handling and storage are critical to prevent analyte degradation."
        ),
        key_factors=[
            "method validation parameters",
            "matrix effects and sample preparation",
            "stability and degradation products",
            "regulatory compliance",
            "quality control and documentation"
        ],
        primary_authority=[
            "ICH Q2(R1) - Validation of Analytical Procedures, 2005",
            "FDA Guidance for Industry - Bioanalytical Method Validation, 2018"
        ],
        burden_holder="Pharmaceutical analysts and clinical laboratory scientists",
        adversary_position=(
            "Suggests that non-validated methods suffice for clinical decision-making."
        ),
        counter_arguments=[
            "Validated methods ensure reliability and patient safety."
        ],
        resolution_strategy=(
            "Implement rigorous validation and quality assurance protocols."
        ),
        entity_scope="Pharmaceutical manufacturing and clinical diagnostic laboratories",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="ICH Q2(R1), 2005; FDA Guidance, 2018"
    ),
    DoctrineBlock(
        topic="Food and Agricultural Analysis",
        keywords=[
            "food analysis",
            "agricultural analysis",
            "pesticide residues",
            "nutritional content",
            "contaminants",
            "sample preparation",
            "regulatory limits"
        ],
        conclusion_template=(
            "Food and agricultural analyses require sensitive, validated methods to detect contaminants and assess nutritional quality."
        ),
        reasoning_framework=(
            "Food and agricultural analysis monitors pesticide residues, contaminants, and nutritional components to ensure safety and compliance. "
            "Sample preparation often involves extraction and clean-up to isolate analytes from complex matrices. "
            "Analytical methods must meet regulatory limits (FDA, EFSA) and be validated for accuracy and precision. "
            "Quality control includes use of certified reference materials and proficiency testing. Data support risk assessment and labeling."
        ),
        key_factors=[
            "sample representativeness",
            "extraction and clean-up efficiency",
            "method sensitivity and specificity",
            "regulatory compliance",
            "quality assurance procedures"
        ],
        primary_authority=[
            "AOAC Official Methods of Analysis, 21st Edition, AOAC International, 2019",
            "Codex Alimentarius Commission - General Standard for Contaminants and Toxins in Food and Feed, 2019"
        ],
        burden_holder="Food safety analysts and agricultural chemists",
        adversary_position=(
            "Claims that rapid test kits replace validated laboratory methods."
        ),
        counter_arguments=[
            "Rapid kits provide screening but lack quantitative accuracy and specificity."
        ],
        resolution_strategy=(
            "Use rapid tests for screening and confirm positives with validated laboratory methods."
        ),
        entity_scope="Food safety laboratories, agricultural testing facilities",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AOAC, 2019; Codex Alimentarius, 2019"
    ),
    DoctrineBlock(
        topic="Forensic Chemistry and Toxicology",
        keywords=[
            "forensic chemistry",
            "toxicology",
            "drug analysis",
            "trace evidence",
            "chain of custody",
            "method validation",
            "legal admissibility"
        ],
        conclusion_template=(
            "Forensic chemical analyses require validated, defensible methods and strict chain of custody to ensure legal admissibility."
        ),
        reasoning_framework=(
            "Forensic chemistry applies analytical techniques to identify substances relevant to legal investigations. "
            "Toxicological analysis quantifies drugs and poisons in biological samples. "
            "Methods must be validated for sensitivity, specificity, and reproducibility. "
            "Chain of custody documentation ensures sample integrity. Analytical results must withstand legal scrutiny, requiring robust quality assurance and documentation. "
            "Interpretation considers pharmacokinetics and toxicodynamics. Collaboration with legal professionals ensures proper evidence handling."
        ),
        key_factors=[
            "method validation and documentation",
            "sample integrity and chain of custody",
            "instrument calibration and maintenance",
            "data interpretation and reporting",
            "legal and ethical compliance"
        ],
        primary_authority=[
            "Houck, M.M., Siegel, J.A. - Fundamentals of Forensic Science, 3rd Edition, Academic Press, 2015",
            "SWGTOX - Scientific Working Group for Forensic Toxicology Guidelines, 2013"
        ],
        burden_holder="Forensic chemists and toxicologists",
        adversary_position=(
            "Claims that rapid or unvalidated methods are sufficient for forensic conclusions."
        ),
        counter_arguments=[
            "Validated methods and strict protocols are essential for evidentiary reliability."
        ],
        resolution_strategy=(
            "Adhere to SWGTOX guidelines and document all procedures thoroughly."
        ),
        entity_scope="Forensic laboratories and legal institutions",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="Houck & Siegel, 2015; SWGTOX, 2013"
    ),
    # Additional 26 DoctrineBlock instances with similarly detailed domain content would continue here...
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
        if (keyword_lower in doctrine.topic.lower() or
            any(keyword_lower in kw.lower() for kw in doctrine.keywords) or
            keyword_lower in doctrine.reasoning_framework.lower() or
            keyword_lower in doctrine.conclusion_template.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]