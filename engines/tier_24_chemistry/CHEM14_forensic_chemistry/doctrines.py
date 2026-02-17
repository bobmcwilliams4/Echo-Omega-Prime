from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

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
        topic="Presumptive Color Tests for Controlled Substances",
        keywords=["presumptive test", "colorimetric", "drug identification", "forensic chemistry", "field testing"],
        conclusion_template="The presumptive color test indicates the possible presence of {{substance}} based on observed color change.",
        reasoning_framework="""Presumptive color tests rely on chemical reactions between specific reagents and target substances, producing characteristic color changes. The test is rapid and inexpensive, suitable for field or preliminary laboratory screening. However, it is not confirmatory and may yield false positives due to cross-reactivity with non-target compounds. The interpretation requires comparison with reference standards and awareness of limitations. Results must be corroborated by confirmatory techniques such as GC-MS. The chain of custody and documentation of test conditions are essential for admissibility. The test's reliability is governed by published protocols (e.g., SWGDRUG, UNODC), and results are reported as 'presumptive positive' or 'negative.'""",
        key_factors=[
            "Specificity of reagent",
            "Color change interpretation",
            "Potential for false positives",
            "Documentation and chain of custody",
            "Comparison with reference standards"
        ],
        primary_authority=[
            "SWGDRUG Recommendations",
            "UNODC Guidelines",
            "ISO 17025"
        ],
        burden_holder="Prosecution",
        adversary_position="Presumptive tests are not definitive and may be unreliable due to cross-reactivity.",
        counter_arguments=[
            "Presumptive tests are validated for screening purposes.",
            "Results are corroborated by confirmatory analysis.",
            "Protocols minimize false positives."
        ],
        resolution_strategy="Use presumptive tests as preliminary evidence; require confirmatory analysis for definitive identification.",
        entity_scope="Forensic laboratory, law enforcement",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Brown, 2013"
    ),
    DoctrineBlock(
        topic="GC-MS Confirmatory Analysis for Controlled Substances",
        keywords=["GC-MS", "confirmatory", "drug identification", "forensic chemistry", "mass spectrometry"],
        conclusion_template="GC-MS analysis confirms the identity of {{substance}} based on retention time and mass spectral match.",
        reasoning_framework="""Gas Chromatography-Mass Spectrometry (GC-MS) is the gold standard for confirmatory identification of controlled substances. The technique separates compounds via chromatography and identifies them through mass spectral analysis. The process involves comparison of sample spectra to validated reference libraries (e.g., NIST, SWGDRUG). Proper calibration, instrument maintenance, and method validation are critical for reliable results. Chain of custody and sample integrity must be maintained. The analyst must interpret spectra, considering possible interferences and matrix effects. Results are reported with confidence levels and uncertainty estimates. The admissibility of GC-MS evidence is supported by peer-reviewed literature and forensic standards.""",
        key_factors=[
            "Instrument calibration",
            "Reference library match",
            "Sample integrity",
            "Method validation",
            "Chain of custody"
        ],
        primary_authority=[
            "SWGDRUG Recommendations",
            "NIST Mass Spectral Library",
            "ISO 17025"
        ],
        burden_holder="Prosecution",
        adversary_position="GC-MS results may be affected by matrix effects or instrument error.",
        counter_arguments=[
            "GC-MS is validated and widely accepted.",
            "Quality assurance protocols minimize error.",
            "Results are interpreted by qualified analysts."
        ],
        resolution_strategy="Present GC-MS results with supporting documentation and expert testimony.",
        entity_scope="Forensic laboratory",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Horn, 2002"
    ),
    DoctrineBlock(
        topic="Trace Fiber Evidence Comparison and Analysis",
        keywords=["fiber comparison", "trace evidence", "microscopy", "forensic analysis", "textile identification"],
        conclusion_template="The fiber evidence is consistent with originating from {{source}} based on comparative analysis.",
        reasoning_framework="""Trace fiber analysis involves the comparison of recovered fibers to known sources using microscopy (e.g., polarized light, fluorescence), FTIR, and other analytical techniques. The analyst examines physical and chemical characteristics, such as color, diameter, cross-section, and polymer composition. The significance of a match depends on the rarity of the fiber type and the context of recovery. Statistical assessment of fiber transfer and persistence is considered. Documentation of comparison criteria and chain of custody is essential. The limitations include the possibility of coincidental matches and environmental contamination. The analyst reports findings as 'consistent with' or 'cannot be excluded.'""",
        key_factors=[
            "Microscopic characteristics",
            "Chemical composition",
            "Context of recovery",
            "Statistical significance",
            "Chain of custody"
        ],
        primary_authority=[
            "SWGMAT Guidelines",
            "ASTM E2225",
            "ISO 17025"
        ],
        burden_holder="Prosecution",
        adversary_position="Fiber matches may be coincidental or result from environmental contamination.",
        counter_arguments=[
            "Analytical methods are validated.",
            "Chain of custody maintained.",
            "Statistical likelihood assessed."
        ],
        resolution_strategy="Report findings with statistical context and limitations.",
        entity_scope="Forensic laboratory",
        confidence=0.80,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Jones, 2010"
    ),
    DoctrineBlock(
        topic="Ignitable Liquid Residue Analysis for Arson Investigation",
        keywords=["ignitable liquid", "arson", "GC-MS", "fire debris", "forensic chemistry"],
        conclusion_template="Ignitable liquid residue consistent with {{liquid_type}} was detected in the fire debris sample.",
        reasoning_framework="""Analysis of fire debris for ignitable liquid residues employs GC-MS following extraction (e.g., passive headspace, SPME). The analyst compares chromatographic profiles to reference standards (e.g., ASTM E1618). Interpretation considers background interferences, substrate effects, and weathering. The presence of characteristic compounds (e.g., alkanes, aromatics) supports identification. Documentation includes sample collection, extraction method, and instrument parameters. Limitations include possible contamination and degradation. The analyst reports findings as 'consistent with' or 'no ignitable liquid detected.' Chain of custody and adherence to ASTM protocols are critical for admissibility.""",
        key_factors=[
            "Extraction method",
            "Chromatographic profile",
            "Reference comparison",
            "Substrate effects",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1618",
            "ISO 17025",
            "NFPA 921"
        ],
        burden_holder="Prosecution",
        adversary_position="Background materials may mimic ignitable liquid profiles.",
        counter_arguments=[
            "Reference standards used.",
            "Substrate effects considered.",
            "Protocols minimize false positives."
        ],
        resolution_strategy="Interpret results in context; corroborate with scene investigation.",
        entity_scope="Forensic laboratory, fire investigation",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Smith, 2015"
    ),
    DoctrineBlock(
        topic="Forensic Toxicology Immunoassay Screening and Confirmatory Testing",
        keywords=["toxicology", "immunoassay", "drug screening", "LC-MS/MS", "confirmation"],
        conclusion_template="Immunoassay screening indicates the presence of {{drug_class}}, confirmed by LC-MS/MS analysis.",
        reasoning_framework="""Forensic toxicology employs immunoassay screening for rapid detection of drug classes in biological matrices (e.g., blood, urine). Immunoassays are sensitive but may lack specificity, leading to false positives. Confirmatory testing by LC-MS/MS or GC-MS provides definitive identification and quantitation. The workflow includes sample preparation, calibration, and quality controls. Interpretation considers pharmacokinetics, matrix effects, and potential interferences. Documentation of analytical procedures and chain of custody is essential. Results are reported as 'screen positive/negative' and 'confirmed positive/negative.' Adherence to SOFT/AAFS guidelines ensures reliability.""",
        key_factors=[
            "Screening specificity",
            "Confirmatory method",
            "Sample integrity",
            "Quality controls",
            "Chain of custody"
        ],
        primary_authority=[
            "SOFT/AAFS Guidelines",
            "ISO 17025",
            "SAMHSA Regulations"
        ],
        burden_holder="Prosecution",
        adversary_position="Immunoassays may yield false positives; confirmation required.",
        counter_arguments=[
            "Confirmatory testing performed.",
            "Validated protocols used.",
            "Results interpreted by experts."
        ],
        resolution_strategy="Report screening and confirmatory results; explain limitations.",
        entity_scope="Forensic laboratory, medical examiner",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Williams, 2011"
    ),
    DoctrineBlock(
        topic="Gunshot Residue Analysis by SEM-EDS",
        keywords=["gunshot residue", "SEM-EDS", "firearm discharge", "particle analysis", "forensic chemistry"],
        conclusion_template="SEM-EDS analysis detected characteristic gunshot residue particles consistent with firearm discharge.",
        reasoning_framework="""Gunshot residue (GSR) analysis utilizes Scanning Electron Microscopy with Energy Dispersive X-ray Spectroscopy (SEM-EDS) to detect and characterize particles containing lead, barium, and antimony. The analyst examines morphology and elemental composition, comparing to reference criteria (e.g., ASTM E1588). Interpretation considers environmental contamination, transfer, and persistence. Documentation includes sample collection, instrument parameters, and chain of custody. Limitations include potential for secondary transfer and loss over time. Results are reported as 'characteristic', 'consistent with', or 'not detected.' Adherence to ASTM protocols is essential for admissibility.""",
        key_factors=[
            "Particle morphology",
            "Elemental composition",
            "Sample collection timing",
            "Environmental contamination",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1588",
            "ISO 17025",
            "SWGGSR Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="GSR may be transferred or lost; environmental sources may mimic GSR.",
        counter_arguments=[
            "Strict collection protocols followed.",
            "Reference criteria applied.",
            "Results interpreted in context."
        ],
        resolution_strategy="Report findings with limitations; corroborate with other evidence.",
        entity_scope="Forensic laboratory, law enforcement",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Garcia, 2016"
    ),
    DoctrineBlock(
        topic="Chain of Custody Protocols for Forensic Evidence",
        keywords=["chain of custody", "evidence handling", "documentation", "forensic protocols", "admissibility"],
        conclusion_template="The chain of custody for {{evidence_type}} was maintained from collection to analysis, ensuring evidentiary integrity.",
        reasoning_framework="""Chain of custody protocols require comprehensive documentation of evidence handling, including collection, packaging, storage, transfer, and analysis. Each handler must record time, date, and purpose of transfer. Proper labeling and tamper-evident packaging are essential. The chain must be unbroken and verifiable for evidence to be admissible in court. Deviations or gaps may lead to exclusion or diminished weight. Adherence to laboratory SOPs, ISO 17025, and legal requirements is mandatory. The chain of custody is reviewed during audits and legal proceedings. The burden is on the prosecution to demonstrate integrity.""",
        key_factors=[
            "Documentation completeness",
            "Tamper-evident packaging",
            "Unbroken chain",
            "Handler accountability",
            "Legal requirements"
        ],
        primary_authority=[
            "ISO 17025",
            "ASCLD/LAB Guidelines",
            "State Evidence Codes"
        ],
        burden_holder="Prosecution",
        adversary_position="Breaks or gaps in chain of custody compromise evidentiary integrity.",
        counter_arguments=[
            "Chain documented and audited.",
            "Protocols minimize risk.",
            "Evidence integrity maintained."
        ],
        resolution_strategy="Present chain of custody records; address any discrepancies.",
        entity_scope="Forensic laboratory, law enforcement",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Ladd, 1956"
    ),
    DoctrineBlock(
        topic="DNA Profiling by STR Analysis and CODIS Database Searching",
        keywords=["DNA profiling", "STR", "CODIS", "forensic genetics", "database search"],
        conclusion_template="STR analysis of {{sample_type}} yielded a DNA profile matching {{individual}} in the CODIS database.",
        reasoning_framework="""DNA profiling uses Short Tandem Repeat (STR) analysis to generate unique genetic profiles from biological samples. The process involves extraction, quantitation, amplification, and capillary electrophoresis. Profiles are compared to reference samples and searched in CODIS. Interpretation considers allelic dropout, stutter, and mixture analysis. Statistical calculation of match probability is performed using population databases. Chain of custody and laboratory accreditation (ISO 17025) are essential. Results are reported as 'match', 'inconclusive', or 'excluded.' Admissibility is governed by Daubert and Frye standards.""",
        key_factors=[
            "STR loci selection",
            "Profile interpretation",
            "Statistical match probability",
            "Chain of custody",
            "Database search criteria"
        ],
        primary_authority=[
            "FBI CODIS Standards",
            "ISO 17025",
            "SWGDAM Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="DNA mixtures and low-template samples may yield ambiguous profiles.",
        counter_arguments=[
            "Validated protocols used.",
            "Statistical calculations provided.",
            "Expert interpretation."
        ],
        resolution_strategy="Report match probability and limitations; expert testimony required.",
        entity_scope="Forensic laboratory",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, 1993"
    ),
    DoctrineBlock(
        topic="Fingerprint Chemistry: Cyanoacrylate Fuming and Ninhydrin Development",
        keywords=["fingerprint", "cyanoacrylate", "ninhydrin", "latent print", "forensic chemistry"],
        conclusion_template="Latent fingerprints were developed on {{surface_type}} using cyanoacrylate fuming and ninhydrin, revealing ridge detail suitable for comparison.",
        reasoning_framework="""Fingerprint chemistry utilizes cyanoacrylate fuming for non-porous surfaces and ninhydrin for porous materials. Cyanoacrylate polymerizes on fingerprint residues, creating visible prints. Ninhydrin reacts with amino acids, producing a purple coloration. The analyst selects development methods based on substrate and environmental conditions. Documentation includes reagent preparation, application parameters, and photographic records. Limitations include substrate compatibility and potential for overdevelopment. Results are reported as 'suitable for comparison' or 'not suitable.' Adherence to SWGFAST and ISO 17025 ensures reliability.""",
        key_factors=[
            "Substrate compatibility",
            "Reagent selection",
            "Development conditions",
            "Documentation",
            "Chain of custody"
        ],
        primary_authority=[
            "SWGFAST Guidelines",
            "ISO 17025",
            "ASTM E1968"
        ],
        burden_holder="Prosecution",
        adversary_position="Development may alter or destroy ridge detail; substrate limitations exist.",
        counter_arguments=[
            "Protocols minimize risk.",
            "Multiple methods used.",
            "Documentation supports findings."
        ],
        resolution_strategy="Select appropriate development method; document process and results.",
        entity_scope="Forensic laboratory, law enforcement",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Lee, 2012"
    ),
    DoctrineBlock(
        topic="ISO 17025 Laboratory Accreditation and Quality Management",
        keywords=["ISO 17025", "accreditation", "quality management", "forensic laboratory", "standards"],
        conclusion_template="The laboratory is accredited to ISO 17025, ensuring compliance with quality management and technical standards.",
        reasoning_framework="""ISO 17025 accreditation establishes requirements for forensic laboratory competence, impartiality, and consistent operation. The standard covers management systems, technical procedures, personnel qualifications, equipment calibration, and proficiency testing. Accreditation is granted by recognized bodies following rigorous assessment. Laboratories must demonstrate ongoing compliance through audits and corrective actions. Quality management includes control of documents, records, and nonconformities. Accreditation enhances credibility and admissibility of forensic evidence. Failure to comply may result in suspension or revocation.""",
        key_factors=[
            "Management system implementation",
            "Technical procedure validation",
            "Personnel competence",
            "Equipment calibration",
            "Proficiency testing"
        ],
        primary_authority=[
            "ISO 17025",
            "ILAC G19",
            "ASCLD/LAB Accreditation"
        ],
        burden_holder="Laboratory",
        adversary_position="Non-accredited laboratories may lack reliability and credibility.",
        counter_arguments=[
            "Accreditation demonstrates competence.",
            "Ongoing audits ensure compliance.",
            "Quality management system in place."
        ],
        resolution_strategy="Maintain accreditation; address nonconformities promptly.",
        entity_scope="Forensic laboratory",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Abel, 2014"
    ),
    DoctrineBlock(
        topic="Daubert Standard for Expert Testimony Admissibility",
        keywords=["Daubert", "expert testimony", "admissibility", "forensic evidence", "legal standards"],
        conclusion_template="Expert testimony regarding {{evidence_type}} is admissible under Daubert, based on scientific validity and relevance.",
        reasoning_framework="""The Daubert standard requires that expert testimony be based on scientifically valid principles, reliably applied, and relevant to the case. Courts evaluate methodology, peer review, error rates, and general acceptance. The burden is on the proponent to demonstrate admissibility. The adversary may challenge reliability or relevance. The court acts as gatekeeper, considering factors such as testability, publication, and standards. Daubert applies to federal courts and many states. Admissibility is determined case-by-case, considering the totality of evidence and expert qualifications.""",
        key_factors=[
            "Scientific validity",
            "Methodology reliability",
            "Peer review and publication",
            "Error rates",
            "General acceptance"
        ],
        primary_authority=[
            "Daubert v. Merrell Dow Pharmaceuticals, 1993",
            "Federal Rules of Evidence 702",
            "Kumho Tire v. Carmichael, 1999"
        ],
        burden_holder="Proponent of testimony",
        adversary_position="Expert testimony may lack scientific validity or relevance.",
        counter_arguments=[
            "Methodology validated and published.",
            "Expert qualifications demonstrated.",
            "Court reviews admissibility."
        ],
        resolution_strategy="Present evidence of scientific validity; respond to challenges.",
        entity_scope="Court, forensic laboratory",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, 1993"
    ),
    DoctrineBlock(
        topic="Paint Evidence Analysis and Comparison",
        keywords=["paint evidence", "layer analysis", "microscopy", "forensic comparison", "vehicle identification"],
        conclusion_template="Paint evidence recovered from {{scene}} is consistent with {{vehicle}} based on layer structure and composition.",
        reasoning_framework="""Paint evidence analysis involves examination of layer structure, color, and chemical composition using microscopy, FTIR, and SEM-EDS. The analyst compares recovered paint chips to known samples, considering layer sequence, pigment, and binder characteristics. Interpretation considers manufacturing variability and statistical likelihood of a match. Documentation includes analytical methods, comparison criteria, and chain of custody. Limitations include possible coincidental matches and environmental contamination. Results are reported as 'consistent with' or 'cannot be excluded.' Adherence to ASTM E1610 and ISO 17025 ensures reliability.""",
        key_factors=[
            "Layer structure comparison",
            "Chemical composition",
            "Manufacturing variability",
            "Statistical significance",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1610",
            "ISO 17025",
            "SWGMAT Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="Paint matches may be coincidental; environmental contamination possible.",
        counter_arguments=[
            "Analytical methods validated.",
            "Statistical likelihood assessed.",
            "Chain of custody maintained."
        ],
        resolution_strategy="Report findings with statistical context and limitations.",
        entity_scope="Forensic laboratory",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Carter, 2008"
    ),
    DoctrineBlock(
        topic="Glass Refractive Index Determination and Comparison",
        keywords=["glass evidence", "refractive index", "comparison", "forensic analysis", "microscopy"],
        conclusion_template="Glass fragments recovered from {{scene}} have refractive indices consistent with {{source}}.",
        reasoning_framework="""Glass evidence analysis includes determination of refractive index using immersion methods or automated systems. The analyst compares recovered fragments to known sources, considering measurement uncertainty and statistical likelihood. Interpretation considers manufacturing variability and environmental contamination. Documentation includes analytical procedures, calibration, and chain of custody. Results are reported as 'consistent with' or 'cannot be excluded.' Adherence to ASTM E1967 and ISO 17025 ensures reliability. Limitations include possible coincidental matches and measurement error.""",
        key_factors=[
            "Refractive index measurement",
            "Comparison criteria",
            "Measurement uncertainty",
            "Manufacturing variability",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1967",
            "ISO 17025",
            "SWGMAT Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="Glass matches may be coincidental; measurement error possible.",
        counter_arguments=[
            "Analytical methods validated.",
            "Statistical likelihood assessed.",
            "Chain of custody maintained."
        ],
        resolution_strategy="Report findings with statistical context and limitations.",
        entity_scope="Forensic laboratory",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Peterson, 2009"
    ),
    DoctrineBlock(
        topic="Questioned Document Examination and Ink Analysis",
        keywords=["questioned document", "ink analysis", "forensic chemistry", "authentication", "microscopy"],
        conclusion_template="Ink analysis of {{document}} reveals characteristics consistent with {{reference}}; document authenticity assessed.",
        reasoning_framework="""Questioned document examination includes analysis of inks, papers, and printing methods using microscopy, TLC, FTIR, and Raman spectroscopy. The analyst compares physical and chemical characteristics to reference samples. Interpretation considers manufacturing variability, aging, and environmental effects. Documentation includes analytical procedures, comparison criteria, and chain of custody. Limitations include possible coincidental matches and degradation. Results are reported as 'consistent with', 'cannot be excluded', or 'inconclusive.' Adherence to ASTM E1422 and ISO 17025 ensures reliability.""",
        key_factors=[
            "Ink composition",
            "Paper characteristics",
            "Comparison criteria",
            "Manufacturing variability",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1422",
            "ISO 17025",
            "SWGDOC Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="Ink matches may be coincidental; aging and degradation affect results.",
        counter_arguments=[
            "Analytical methods validated.",
            "Chain of custody maintained.",
            "Expert interpretation."
        ],
        resolution_strategy="Report findings with limitations; corroborate with other evidence.",
        entity_scope="Forensic laboratory",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Harris, 2011"
    ),
    DoctrineBlock(
        topic="Explosives Residue Analysis and Identification",
        keywords=["explosives residue", "forensic chemistry", "GC-MS", "LC-MS", "identification"],
        conclusion_template="Explosives residue consistent with {{explosive_type}} was detected in the sample.",
        reasoning_framework="""Explosives residue analysis employs GC-MS, LC-MS, and ion chromatography to detect and identify explosive compounds and their degradation products. The analyst compares chromatographic profiles to reference standards, considering possible interferences and environmental contamination. Documentation includes sample collection, extraction method, instrument parameters, and chain of custody. Limitations include possible degradation, contamination, and low concentration. Results are reported as 'consistent with', 'cannot be excluded', or 'not detected.' Adherence to ASTM E1589 and ISO 17025 ensures reliability.""",
        key_factors=[
            "Extraction method",
            "Chromatographic profile",
            "Reference comparison",
            "Contamination risk",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1589",
            "ISO 17025",
            "SWGEXP Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="Residue may be degraded or contaminated; false positives possible.",
        counter_arguments=[
            "Reference standards used.",
            "Protocols minimize risk.",
            "Results interpreted by experts."
        ],
        resolution_strategy="Report findings with limitations; corroborate with scene investigation.",
        entity_scope="Forensic laboratory, law enforcement",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Miller, 2013"
    ),
    DoctrineBlock(
        topic="Forensic Quality Assurance and Proficiency Testing Programs",
        keywords=["quality assurance", "proficiency testing", "forensic laboratory", "ISO 17025", "competence"],
        conclusion_template="The laboratory participates in regular proficiency testing and maintains a quality assurance program in compliance with ISO 17025.",
        reasoning_framework="""Forensic laboratories implement quality assurance programs to ensure competence, reliability, and compliance with ISO 17025. Proficiency testing assesses analyst performance and identifies areas for improvement. Quality assurance includes control of documents, records, equipment calibration, and corrective actions. Participation in external proficiency testing is required for accreditation. Results are reviewed, and nonconformities addressed. Quality assurance enhances credibility and admissibility of forensic evidence. Failure to comply may result in suspension or revocation of accreditation.""",
        key_factors=[
            "Proficiency testing participation",
            "Quality assurance procedures",
            "Equipment calibration",
            "Corrective actions",
            "Accreditation requirements"
        ],
        primary_authority=[
            "ISO 17025",
            "ILAC G19",
            "ASCLD/LAB Guidelines"
        ],
        burden_holder="Laboratory",
        adversary_position="Lack of proficiency testing may compromise reliability.",
        counter_arguments=[
            "Proficiency testing regularly performed.",
            "Quality assurance system in place.",
            "Ongoing compliance demonstrated."
        ],
        resolution_strategy="Maintain quality assurance and proficiency testing; address deficiencies promptly.",
        entity_scope="Forensic laboratory",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Abel, 2014"
    ),
    DoctrineBlock(
        topic="Forensic Alcohol Analysis by Headspace Gas Chromatography",
        keywords=["alcohol analysis", "headspace GC", "blood alcohol", "forensic toxicology", "driving under influence"],
        conclusion_template="Headspace GC analysis determined a blood alcohol concentration of {{bac}} g/dL in the sample.",
        reasoning_framework="""Headspace gas chromatography is the standard method for forensic alcohol analysis in blood and other biological samples. The technique separates ethanol from matrix components, allowing quantitation. Calibration and quality controls are essential for accuracy. Interpretation considers sample integrity, potential interferences, and instrument performance. Chain of custody and documentation of analytical procedures are critical for admissibility. Results are reported as blood alcohol concentration (BAC) with uncertainty estimates. Adherence to SOFT/AAFS and ISO 17025 ensures reliability.""",
        key_factors=[
            "Calibration and quality controls",
            "Sample integrity",
            "Instrument performance",
            "Chain of custody",
            "Documentation"
        ],
        primary_authority=[
            "SOFT/AAFS Guidelines",
            "ISO 17025",
            "SAMHSA Regulations"
        ],
        burden_holder="Prosecution",
        adversary_position="Sample contamination or instrument error may affect results.",
        counter_arguments=[
            "Validated protocols used.",
            "Quality controls performed.",
            "Chain of custody maintained."
        ],
        resolution_strategy="Present results with uncertainty estimates; address any discrepancies.",
        entity_scope="Forensic laboratory, law enforcement",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Johnson, 2014"
    ),
    DoctrineBlock(
        topic="Forensic Hair Comparison and Mitochondrial DNA Analysis",
        keywords=["hair comparison", "mitochondrial DNA", "forensic genetics", "trace evidence", "microscopy"],
        conclusion_template="Hair comparison and mitochondrial DNA analysis indicate {{individual}} cannot be excluded as a contributor.",
        reasoning_framework="""Forensic hair analysis includes microscopic comparison of physical characteristics and mitochondrial DNA (mtDNA) sequencing for identification. Microscopy assesses color, diameter, medullary structure, and pigmentation. mtDNA analysis is used for degraded or rootless hairs, comparing sequences to reference samples. Interpretation considers statistical likelihood and population databases. Documentation includes analytical procedures, comparison criteria, and chain of custody. Limitations include possible coincidental matches and contamination. Results are reported as 'cannot be excluded', 'excluded', or 'inconclusive.' Adherence to SWGMAT and ISO 17025 ensures reliability.""",
        key_factors=[
            "Microscopic characteristics",
            "mtDNA sequence comparison",
            "Statistical likelihood",
            "Chain of custody",
            "Contamination risk"
        ],
        primary_authority=[
            "SWGMAT Guidelines",
            "ISO 17025",
            "FBI mtDNA Protocols"
        ],
        burden_holder="Prosecution",
        adversary_position="Hair matches may be coincidental; mtDNA is not unique to individuals.",
        counter_arguments=[
            "Analytical methods validated.",
            "Population databases used.",
            "Chain of custody maintained."
        ],
        resolution_strategy="Report findings with statistical context and limitations.",
        entity_scope="Forensic laboratory",
        confidence=0.86,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Williams, 2012"
    ),
    DoctrineBlock(
        topic="Forensic Soil Analysis and Comparison",
        keywords=["soil analysis", "forensic comparison", "microscopy", "chemical composition", "trace evidence"],
        conclusion_template="Soil samples from {{scene}} are consistent with {{reference_location}} based on physical and chemical characteristics.",
        reasoning_framework="""Forensic soil analysis compares physical (color, texture, mineral content) and chemical (organic content, elemental composition) characteristics using microscopy, XRF, and FTIR. The analyst compares recovered samples to reference locations, considering environmental variability and contamination. Interpretation considers statistical likelihood and context of recovery. Documentation includes analytical procedures, comparison criteria, and chain of custody. Limitations include possible coincidental matches and environmental effects. Results are reported as 'consistent with', 'cannot be excluded', or 'inconclusive.' Adherence to ASTM E1658 and ISO 17025 ensures reliability.""",
        key_factors=[
            "Physical characteristics",
            "Chemical composition",
            "Comparison criteria",
            "Environmental variability",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1658",
            "ISO 17025",
            "SWGMAT Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="Soil matches may be coincidental; environmental effects may alter characteristics.",
        counter_arguments=[
            "Analytical methods validated.",
            "Statistical likelihood assessed.",
            "Chain of custody maintained."
        ],
        resolution_strategy="Report findings with statistical context and limitations.",
        entity_scope="Forensic laboratory",
        confidence=0.82,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Davis, 2010"
    ),
    DoctrineBlock(
        topic="Forensic Gunshot Distance Determination",
        keywords=["gunshot distance", "forensic ballistics", "pattern analysis", "GSR", "firearm discharge"],
        conclusion_template="Gunshot distance from {{target}} is estimated at {{distance}} based on pattern analysis and GSR distribution.",
        reasoning_framework="""Gunshot distance determination uses pattern analysis of GSR, soot, and stippling on targets. The analyst compares observed patterns to test firings at known distances. Interpretation considers ammunition type, firearm characteristics, and environmental conditions. Documentation includes test firing procedures, photographic records, and chain of custody. Limitations include variability in ammunition and target materials. Results are reported as estimated distance with uncertainty. Adherence to SWGGUN and ISO 17025 ensures reliability.""",
        key_factors=[
            "Pattern analysis",
            "Test firing comparison",
            "Ammunition variability",
            "Environmental conditions",
            "Chain of custody"
        ],
        primary_authority=[
            "SWGGUN Guidelines",
            "ISO 17025",
            "ASTM E1588"
        ],
        burden_holder="Prosecution",
        adversary_position="Ammunition and target variability may affect accuracy of distance estimation.",
        counter_arguments=[
            "Test firing protocols used.",
            "Documentation supports findings.",
            "Expert interpretation."
        ],
        resolution_strategy="Report estimated distance with uncertainty; corroborate with other evidence.",
        entity_scope="Forensic laboratory, law enforcement",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Robinson, 2011"
    ),
    DoctrineBlock(
        topic="Forensic Bloodstain Pattern Analysis",
        keywords=["bloodstain pattern", "forensic analysis", "crime scene", "pattern interpretation", "documentation"],
        conclusion_template="Bloodstain pattern analysis indicates {{event}} occurred at {{location}} based on pattern characteristics.",
        reasoning_framework="""Bloodstain pattern analysis interprets the size, shape, distribution, and location of bloodstains to reconstruct events at a crime scene. The analyst considers impact angle, velocity, and mechanism of formation. Documentation includes photographic records, measurements, and chain of custody. Interpretation is supported by test experiments and published literature. Limitations include environmental effects and subjective assessment. Results are reported as 'consistent with', 'cannot be excluded', or 'inconclusive.' Adherence to SWGSTAIN and ISO 17025 ensures reliability.""",
        key_factors=[
            "Pattern characteristics",
            "Impact angle",
            "Velocity and mechanism",
            "Documentation",
            "Chain of custody"
        ],
        primary_authority=[
            "SWGSTAIN Guidelines",
            "ISO 17025",
            "ASTM E2329"
        ],
        burden_holder="Prosecution",
        adversary_position="Subjective interpretation may affect reliability; environmental effects possible.",
        counter_arguments=[
            "Protocols minimize subjectivity.",
            "Documentation supports findings.",
            "Expert interpretation."
        ],
        resolution_strategy="Report findings with limitations; corroborate with other evidence.",
        entity_scope="Forensic laboratory, crime scene",
        confidence=0.81,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Thompson, 2012"
    ),
    DoctrineBlock(
        topic="Forensic Entomology for Postmortem Interval Estimation",
        keywords=["forensic entomology", "postmortem interval", "insect evidence", "decomposition", "crime scene"],
        conclusion_template="Forensic entomology estimates postmortem interval as {{interval}} based on insect development and species identification.",
        reasoning_framework="""Forensic entomology uses insect evidence (species, developmental stage) to estimate postmortem interval (PMI). The analyst collects and identifies insects from the body and scene, comparing development to published data. Interpretation considers environmental conditions, species variability, and potential for contamination. Documentation includes collection procedures, species identification, and chain of custody. Limitations include variability in insect development and environmental effects. Results are reported as estimated PMI with uncertainty. Adherence to AAFS and ISO 17025 ensures reliability.""",
        key_factors=[
            "Species identification",
            "Developmental stage",
            "Environmental conditions",
            "Documentation",
            "Chain of custody"
        ],
        primary_authority=[
            "AAFS Guidelines",
            "ISO 17025",
            "Published entomology data"
        ],
        burden_holder="Prosecution",
        adversary_position="Environmental variability may affect accuracy of PMI estimation.",
        counter_arguments=[
            "Published data used.",
            "Documentation supports findings.",
            "Expert interpretation."
        ],
        resolution_strategy="Report estimated PMI with uncertainty; corroborate with other evidence.",
        entity_scope="Forensic laboratory, crime scene",
        confidence=0.80,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Martinez, 2013"
    ),
    DoctrineBlock(
        topic="Forensic Firearm Identification by Toolmark Analysis",
        keywords=["firearm identification", "toolmark", "comparison microscope", "forensic ballistics", "individualization"],
        conclusion_template="Toolmark analysis indicates {{firearm}} fired the recovered cartridge case based on individual characteristics.",
        reasoning_framework="""Firearm identification uses toolmark analysis to compare marks on cartridge cases and bullets to test-fired samples. The analyst examines individual and class characteristics using comparison microscopy. Interpretation considers manufacturing variability, wear, and environmental effects. Documentation includes analytical procedures, comparison criteria, and chain of custody. Limitations include possible coincidental matches and subjective assessment. Results are reported as 'identification', 'inconclusive', or 'exclusion.' Adherence to SWGGUN and ISO 17025 ensures reliability.""",
        key_factors=[
            "Individual and class characteristics",
            "Comparison criteria",
            "Manufacturing variability",
            "Documentation",
            "Chain of custody"
        ],
        primary_authority=[
            "SWGGUN Guidelines",
            "ISO 17025",
            "ASTM E2386"
        ],
        burden_holder="Prosecution",
        adversary_position="Subjective interpretation may affect reliability; coincidental matches possible.",
        counter_arguments=[
            "Protocols minimize subjectivity.",
            "Documentation supports findings.",
            "Expert interpretation."
        ],
        resolution_strategy="Report findings with limitations; corroborate with other evidence.",
        entity_scope="Forensic laboratory, law enforcement",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Evans, 2014"
    ),
    DoctrineBlock(
        topic="Forensic Digital Evidence Acquisition and Preservation",
        keywords=["digital evidence", "acquisition", "preservation", "forensic protocols", "chain of custody"],
        conclusion_template="Digital evidence from {{device}} was acquired and preserved in accordance with forensic protocols, ensuring integrity.",
        reasoning_framework="""Digital evidence acquisition requires use of validated forensic tools and protocols to prevent alteration. The analyst documents acquisition procedures, hash values, and chain of custody. Preservation includes write-blocking, secure storage, and access control. Interpretation considers potential for contamination and alteration. Adherence to NIST guidelines and ISO 17025 ensures reliability. Results are reported with supporting documentation and hash verification. Limitations include possible encryption and device failure.""",
        key_factors=[
            "Validated acquisition tools",
            "Hash verification",
            "Secure storage",
            "Documentation",
            "Chain of custody"
        ],
        primary_authority=[
            "NIST Guidelines",
            "ISO 17025",
            "SWGDE Recommendations"
        ],
        burden_holder="Prosecution",
        adversary_position="Improper acquisition may alter evidence; chain of custody may be compromised.",
        counter_arguments=[
            "Validated tools used.",
            "Hash values verified.",
            "Chain of custody maintained."
        ],
        resolution_strategy="Present acquisition and preservation records; address any discrepancies.",
        entity_scope="Forensic laboratory, law enforcement",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Jackson, 2015"
    ),
    DoctrineBlock(
        topic="Forensic Document Dating by Ink and Paper Analysis",
        keywords=["document dating", "ink analysis", "paper analysis", "forensic chemistry", "authentication"],
        conclusion_template="Ink and paper analysis indicates {{document}} was produced within {{timeframe}}.",
        reasoning_framework="""Document dating uses ink and paper analysis to estimate the time of production. The analyst examines chemical composition, aging markers, and manufacturing characteristics using chromatography, spectroscopy, and microscopy. Interpretation considers environmental effects and manufacturing variability. Documentation includes analytical procedures, comparison criteria, and chain of custody. Limitations include possible coincidental matches and degradation. Results are reported as estimated timeframe with uncertainty. Adherence to ASTM E1422 and ISO 17025 ensures reliability.""",
        key_factors=[
            "Chemical composition",
            "Aging markers",
            "Manufacturing characteristics",
            "Environmental effects",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1422",
            "ISO 17025",
            "SWGDOC Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="Environmental effects and degradation may affect accuracy of dating.",
        counter_arguments=[
            "Analytical methods validated.",
            "Documentation supports findings.",
            "Expert interpretation."
        ],
        resolution_strategy="Report estimated timeframe with uncertainty; corroborate with other evidence.",
        entity_scope="Forensic laboratory",
        confidence=0.81,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Clark, 2011"
    ),
    DoctrineBlock(
        topic="Forensic Latent Print Comparison and Individualization",
        keywords=["latent print", "comparison", "individualization", "forensic analysis", "ridge detail"],
        conclusion_template="Latent print comparison indicates {{individual}} is the source of the recovered fingerprint based on ridge detail.",
        reasoning_framework="""Latent print comparison uses analysis of ridge detail, minutiae, and pattern characteristics to individualize prints. The analyst compares recovered prints to known samples, considering quality and quantity of detail. Interpretation considers substrate, development method, and environmental effects. Documentation includes analytical procedures, comparison criteria, and chain of custody. Limitations include possible coincidental matches and subjective assessment. Results are reported as 'identification', 'inconclusive', or 'exclusion.' Adherence to SWGFAST and ISO 17025 ensures reliability.""",
        key_factors=[
            "Ridge detail quality",
            "Minutiae comparison",
            "Pattern characteristics",
            "Documentation",
            "Chain of custody"
        ],
        primary_authority=[
            "SWGFAST Guidelines",
            "ISO 17025",
            "ASTM E2127"
        ],
        burden_holder="Prosecution",
        adversary_position="Subjective interpretation may affect reliability; coincidental matches possible.",
        counter_arguments=[
            "Protocols minimize subjectivity.",
            "Documentation supports findings.",
            "Expert interpretation."
        ],
        resolution_strategy="Report findings with limitations; corroborate with other evidence.",
        entity_scope="Forensic laboratory, law enforcement",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Turner, 2013"
    ),
    DoctrineBlock(
        topic="Forensic Shoeprint and Tire Tread Comparison",
        keywords=["shoeprint", "tire tread", "comparison", "forensic analysis", "pattern recognition"],
        conclusion_template="Shoeprint/tire tread comparison indicates {{source}} cannot be excluded as the origin of the recovered impression.",
        reasoning_framework="""Shoeprint and tire tread comparison uses pattern recognition and analysis of class and individual characteristics. The analyst compares recovered impressions to known samples, considering wear, manufacturing variability, and substrate effects. Interpretation considers statistical likelihood and context of recovery. Documentation includes analytical procedures, comparison criteria, and chain of custody. Limitations include possible coincidental matches and subjective assessment. Results are reported as 'cannot be excluded', 'excluded', or 'inconclusive.' Adherence to SWGSHOE and ISO 17025 ensures reliability.""",
        key_factors=[
            "Pattern recognition",
            "Class and individual characteristics",
            "Wear and manufacturing variability",
            "Documentation",
            "Chain of custody"
        ],
        primary_authority=[
            "SWGSHOE Guidelines",
            "ISO 17025",
            "ASTM E2224"
        ],
        burden_holder="Prosecution",
        adversary_position="Subjective interpretation may affect reliability; coincidental matches possible.",
        counter_arguments=[
            "Protocols minimize subjectivity.",
            "Documentation supports findings.",
            "Expert interpretation."
        ],
        resolution_strategy="Report findings with limitations; corroborate with other evidence.",
        entity_scope="Forensic laboratory, law enforcement",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Lopez, 2012"
    ),
    DoctrineBlock(
        topic="Forensic Fire Debris Analysis for Accelerant Detection",
        keywords=["fire debris", "accelerant detection", "GC-MS", "arson investigation", "forensic chemistry"],
        conclusion_template="GC-MS analysis detected accelerant residues consistent with {{accelerant_type}} in fire debris samples.",
        reasoning_framework="""Fire debris analysis for accelerant detection uses GC-MS following extraction (e.g., passive headspace, SPME). The analyst compares chromatographic profiles to reference standards, considering substrate effects and environmental contamination. Interpretation considers possible degradation and background interferences. Documentation includes sample collection, extraction method, instrument parameters, and chain of custody. Results are reported as 'consistent with', 'cannot be excluded', or 'not detected.' Adherence to ASTM E1618 and ISO 17025 ensures reliability.""",
        key_factors=[
            "Extraction method",
            "Chromatographic profile",
            "Reference comparison",
            "Substrate effects",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1618",
            "ISO 17025",
            "NFPA 921"
        ],
        burden_holder="Prosecution",
        adversary_position="Background materials may mimic accelerant profiles; contamination possible.",
        counter_arguments=[
            "Reference standards used.",
            "Protocols minimize risk.",
            "Results interpreted by experts."
        ],
        resolution_strategy="Report findings with limitations; corroborate with scene investigation.",
        entity_scope="Forensic laboratory, fire investigation",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Parker, 2015"
    ),
    DoctrineBlock(
        topic="Forensic Gunshot Residue Analysis by Ion Chromatography",
        keywords=["gunshot residue", "ion chromatography", "forensic chemistry", "firearm discharge", "particle analysis"],
        conclusion_template="Ion chromatography detected gunshot residue ions consistent with firearm discharge in the sample.",
        reasoning_framework="""Gunshot residue analysis by ion chromatography detects inorganic ions (e.g., nitrate, nitrite, thiocyanate) associated with firearm discharge. The analyst compares ion profiles to reference criteria, considering environmental contamination and transfer. Documentation includes sample collection, extraction method, instrument parameters, and chain of custody. Limitations include possible environmental sources and low concentration. Results are reported as 'consistent with', 'cannot be excluded', or 'not detected.' Adherence to ASTM E1588 and ISO 17025 ensures reliability.""",
        key_factors=[
            "Ion profile comparison",
            "Extraction method",
            "Environmental contamination",
            "Documentation",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1588",
            "ISO 17025",
            "SWGGSR Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="Environmental sources may mimic GSR ion profiles; transfer possible.",
        counter_arguments=[
            "Reference criteria applied.",
            "Protocols minimize risk.",
            "Results interpreted by experts."
        ],
        resolution_strategy="Report findings with limitations; corroborate with other evidence.",
        entity_scope="Forensic laboratory, law enforcement",
        confidence=0.86,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Ramirez, 2014"
    ),
    DoctrineBlock(
        topic="Forensic Controlled Substance Quantitation by LC-MS/MS",
        keywords=["controlled substance", "quantitation", "LC-MS/MS", "forensic chemistry", "drug analysis"],
        conclusion_template="LC-MS/MS quantitation determined {{concentration}} of {{substance}} in the sample.",
        reasoning_framework="""Quantitation of controlled substances uses LC-MS/MS for accurate measurement in biological and non-biological matrices. The analyst calibrates the instrument, prepares samples, and applies validated methods. Interpretation considers matrix effects, calibration curve, and uncertainty. Documentation includes analytical procedures, calibration records, and chain of custody. Results are reported as concentration with uncertainty estimates. Adherence to SOFT/AAFS and ISO 17025 ensures reliability. Limitations include possible interferences and instrument error.""",
        key_factors=[
            "Calibration and quality controls",
            "Matrix effects",
            "Method validation",
            "Documentation",
            "Chain of custody"
        ],
        primary_authority=[
            "SOFT/AAFS Guidelines",
            "ISO 17025",
            "SAMHSA Regulations"
        ],
        burden_holder="Prosecution",
        adversary_position="Matrix effects or instrument error may affect quantitation accuracy.",
        counter_arguments=[
            "Validated protocols used.",
            "Quality controls performed.",
            "Chain of custody maintained."
        ],
        resolution_strategy="Present results with uncertainty estimates; address any discrepancies.",
        entity_scope="Forensic laboratory",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Murphy, 2013"
    ),
    DoctrineBlock(
        topic="Forensic Analysis of Synthetic Cannabinoids",
        keywords=["synthetic cannabinoids", "drug identification", "forensic chemistry", "GC-MS", "LC-MS/MS"],
        conclusion_template="GC-MS/LC-MS/MS analysis identified synthetic cannabinoid {{compound}} in the sample.",
        reasoning_framework="""Analysis of synthetic cannabinoids uses GC-MS and LC-MS/MS for identification and quantitation. The analyst compares chromatographic and mass spectral profiles to reference standards, considering possible interferences and matrix effects. Documentation includes sample preparation, instrument parameters, and chain of custody. Interpretation considers legal status and structural variability. Results are reported as 'identified', 'not identified', or 'inconclusive.' Adherence to SWGDRUG and ISO 17025 ensures reliability. Limitations include rapid emergence of new compounds and limited reference data.""",
        key_factors=[
            "Reference standard comparison",
            "Instrument calibration",
            "Matrix effects",
            "Documentation",
            "Chain of custody"
        ],
        primary_authority=[
            "SWGDRUG Recommendations",
            "ISO 17025",
            "NIST Mass Spectral Library"
        ],
        burden_holder="Prosecution",
        adversary_position="Rapid emergence of new compounds may limit identification; reference data may be incomplete.",
        counter_arguments=[
            "Validated protocols used.",
            "Reference standards updated.",
            "Expert interpretation."
        ],
        resolution_strategy="Report findings with limitations; corroborate with legal status.",
        entity_scope="Forensic laboratory",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Patel, 2014"
    ),
    DoctrineBlock(
        topic="Forensic Analysis of Novel Psychoactive Substances",
        keywords=["novel psychoactive substances", "drug identification", "forensic chemistry", "GC-MS", "LC-MS/MS"],
        conclusion_template="GC-MS/LC-MS/MS analysis identified novel psychoactive substance {{compound}} in the sample.",
        reasoning_framework="""Analysis of novel psychoactive substances (NPS) uses GC-MS and LC-MS/MS for identification and quantitation. The analyst compares chromatographic and mass spectral profiles to reference standards, considering possible interferences and matrix effects. Documentation includes sample preparation, instrument parameters, and chain of custody. Interpretation considers legal status and structural variability. Results are reported as 'identified', 'not identified', or 'inconclusive.' Adherence to SWGDRUG and ISO 17025 ensures reliability. Limitations include rapid emergence of new compounds and limited reference data.""",
        key_factors=[
            "Reference standard comparison",
            "Instrument calibration",
            "Matrix effects",
            "Documentation",
            "Chain of custody"
        ],
        primary_authority=[
            "SWGDRUG Recommendations",
            "ISO 17025",
            "NIST Mass Spectral Library"
        ],
        burden_holder="Prosecution",
        adversary_position="Rapid emergence of new compounds may limit identification; reference data may be incomplete.",
        counter_arguments=[
            "Validated protocols used.",
            "Reference standards updated.",
            "Expert interpretation."
        ],
        resolution_strategy="Report findings with limitations; corroborate with legal status.",
        entity_scope="Forensic laboratory",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Nguyen, 2015"
    ),
    DoctrineBlock(
        topic="Forensic Analysis of Trace Gunshot Residue on Clothing",
        keywords=["gunshot residue", "trace evidence", "clothing analysis", "SEM-EDS", "forensic chemistry"],
        conclusion_template="SEM-EDS analysis detected trace gunshot residue particles on {{clothing_item}}, consistent with firearm discharge.",
        reasoning_framework="""Trace gunshot residue analysis on clothing uses SEM-EDS to detect and characterize particles containing lead, barium, and antimony. The analyst examines morphology and elemental composition, comparing to reference criteria. Interpretation considers environmental contamination, transfer, and persistence. Documentation includes sample collection, instrument parameters, and chain of custody. Limitations include potential for secondary transfer and loss over time. Results are reported as 'characteristic', 'consistent with', or 'not detected.' Adherence to ASTM E1588 and ISO 17025 ensures reliability.""",
        key_factors=[
            "Particle morphology",
            "Elemental composition",
            "Sample collection timing",
            "Environmental contamination",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1588",
            "ISO 17025",
            "SWGGSR Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="GSR may be transferred or lost; environmental sources may mimic GSR.",
        counter_arguments=[
            "Strict collection protocols followed.",
            "Reference criteria applied.",
            "Results interpreted in context."
        ],
        resolution_strategy="Report findings with limitations; corroborate with other evidence.",
        entity_scope="Forensic laboratory, law enforcement",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Kim, 2016"
    ),
    DoctrineBlock(
        topic="Forensic Analysis of Controlled Substance Residues on Surfaces",
        keywords=["controlled substance", "residue analysis", "surface sampling", "forensic chemistry", "drug identification"],
        conclusion_template="Surface sampling and analysis detected controlled substance residue {{substance}} on {{surface_type}}.",
        reasoning_framework="""Analysis of controlled substance residues on surfaces uses swabbing, extraction, and GC-MS or LC-MS/MS for identification. The analyst compares chromatographic and mass spectral profiles to reference standards, considering possible interferences and contamination. Documentation includes sample collection, extraction method, instrument parameters, and chain of custody. Interpretation considers environmental effects and legal status. Results are reported as 'identified', 'not identified', or 'inconclusive.' Adherence to SWGDRUG and ISO 17025 ensures reliability. Limitations include low concentration and possible contamination.""",
        key_factors=[
            "Sample collection method",
            "Extraction and analysis",
            "Reference standard comparison",
            "Contamination risk",
            "Chain of custody"
        ],
        primary_authority=[
            "SWGDRUG Recommendations",
            "ISO 17025",
            "NIST Mass Spectral Library"
        ],
        burden_holder="Prosecution",
        adversary_position="Low concentration or contamination may affect reliability of residue identification.",
        counter_arguments=[
            "Validated protocols used.",
            "Chain of custody maintained.",
            "Expert interpretation."
        ],
        resolution_strategy="Report findings with limitations; corroborate with other evidence.",
        entity_scope="Forensic laboratory",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Morgan, 2014"
    ),
    DoctrineBlock(
        topic="Forensic Analysis of Trace Explosives Residue on Hands",
        keywords=["explosives residue", "trace evidence", "hand sampling", "forensic chemistry", "GC-MS"],
        conclusion_template="GC-MS analysis detected trace explosives residue {{explosive_type}} on {{individual}}'s hands.",
        reasoning_framework="""Trace explosives residue analysis on hands uses swabbing, extraction, and GC-MS for identification. The analyst compares chromatographic profiles to reference standards, considering possible interferences and contamination. Documentation includes sample collection, extraction method, instrument parameters, and chain of custody. Interpretation considers environmental effects and legal status. Results are reported as 'identified', 'not identified', or 'inconclusive.' Adherence to ASTM E1589 and ISO 17025 ensures reliability. Limitations include low concentration and possible contamination.""",
        key_factors=[
            "Sample collection method",
            "Extraction and analysis",
            "Reference standard comparison",
            "Contamination risk",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1589",
            "ISO 17025",
            "SWGEXP Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="Low concentration or contamination may affect reliability of residue identification.",
        counter_arguments=[
            "Validated protocols used.",
            "Chain of custody maintained.",
            "Expert interpretation."
        ],
        resolution_strategy="Report findings with limitations; corroborate with other evidence.",
        entity_scope="Forensic laboratory",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Allen, 2013"
    ),
    DoctrineBlock(
        topic="Forensic Analysis of Trace Fiber Evidence on Clothing",
        keywords=["fiber evidence", "trace evidence", "clothing analysis", "microscopy", "forensic chemistry"],
        conclusion_template="Microscopic analysis detected trace fiber evidence on {{clothing_item}}, consistent with {{source}}.",
        reasoning_framework="""Trace fiber analysis on clothing uses microscopy (polarized light, fluorescence), FTIR, and other analytical techniques. The analyst examines physical and chemical characteristics, such as color, diameter, cross-section, and polymer composition. Interpretation considers environmental contamination and statistical likelihood. Documentation includes analytical procedures, comparison criteria, and chain of custody. Limitations include possible coincidental matches and contamination. Results are reported as 'consistent with', 'cannot be excluded', or 'inconclusive.' Adherence to SWGMAT and ISO 17025 ensures reliability.""",
        key_factors=[
            "Microscopic characteristics",
            "Chemical composition",
            "Comparison criteria",
            "Contamination risk",
            "Chain of custody"
        ],
        primary_authority=[
            "SWGMAT Guidelines",
            "ISO 17025",
            "ASTM E2225"
        ],
        burden_holder="Prosecution",
        adversary_position="Fiber matches may be coincidental or result from environmental contamination.",
        counter_arguments=[
            "Analytical methods validated.",
            "Chain of custody maintained.",
            "Statistical likelihood assessed."
        ],
        resolution_strategy="Report findings with statistical context and limitations.",
        entity_scope="Forensic laboratory",
        confidence=0.82,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Baker, 2012"
    ),
    DoctrineBlock(
        topic="Forensic Analysis of Trace Paint Evidence on Vehicles",
        keywords=["paint evidence", "trace evidence", "vehicle analysis", "microscopy", "forensic chemistry"],
        conclusion_template="Microscopic and chemical analysis detected trace paint evidence on {{vehicle}}, consistent with {{source}}.",
        reasoning_framework="""Trace paint analysis on vehicles uses microscopy, FTIR, and SEM-EDS to examine layer structure, color, and chemical composition. The analyst compares recovered paint chips to known samples, considering layer sequence, pigment, and binder characteristics. Interpretation considers manufacturing variability and statistical likelihood. Documentation includes analytical procedures, comparison criteria, and chain of custody. Limitations include possible coincidental matches and environmental contamination. Results are reported as 'consistent with', 'cannot be excluded', or 'inconclusive.' Adherence to ASTM E1610 and ISO 17025 ensures reliability.""",
        key_factors=[
            "Layer structure comparison",
            "Chemical composition",
            "Manufacturing variability",
            "Statistical significance",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1610",
            "ISO 17025",
            "SWGMAT Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="Paint matches may be coincidental; environmental contamination possible.",
        counter_arguments=[
            "Analytical methods validated.",
            "Statistical likelihood assessed.",
            "Chain of custody maintained."
        ],
        resolution_strategy="Report findings with statistical context and limitations.",
        entity_scope="Forensic laboratory",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Reed, 2011"
    ),
    DoctrineBlock(
        topic="Forensic Analysis of Trace Glass Evidence on Clothing",
        keywords=["glass evidence", "trace evidence", "clothing analysis", "refractive index", "forensic chemistry"],
        conclusion_template="Refractive index analysis detected trace glass evidence on {{clothing_item}}, consistent with {{source}}.",
        reasoning_framework="""Trace glass analysis on clothing includes determination of refractive index using immersion methods or automated systems. The analyst compares recovered fragments to known sources, considering measurement uncertainty and statistical likelihood. Interpretation considers manufacturing variability and environmental contamination. Documentation includes analytical procedures, calibration, and chain of custody. Results are reported as 'consistent with', 'cannot be excluded', or 'inconclusive.' Adherence to ASTM E1967 and ISO 17025 ensures reliability. Limitations include possible coincidental matches and measurement error.""",
        key_factors=[
            "Refractive index measurement",
            "Comparison criteria",
            "Measurement uncertainty",
            "Manufacturing variability",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1967",
            "ISO 17025",
            "SWGMAT Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="Glass matches may be coincidental; measurement error possible.",
        counter_arguments=[
            "Analytical methods validated.",
            "Statistical likelihood assessed.",
            "Chain of custody maintained."
        ],
        resolution_strategy="Report findings with statistical context and limitations.",
        entity_scope="Forensic laboratory",
        confidence=0.80,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Price, 2010"
    ),
    DoctrineBlock(
        topic="Forensic Analysis of Trace Soil Evidence on Shoes",
        keywords=["soil evidence", "trace evidence", "shoe analysis", "microscopy", "forensic chemistry"],
        conclusion_template="Microscopic and chemical analysis detected trace soil evidence on {{shoe}}, consistent with {{reference_location}}.",
        reasoning_framework="""Trace soil analysis on shoes compares physical (color, texture, mineral content) and chemical (organic content, elemental composition) characteristics using microscopy, XRF, and FTIR. The analyst compares recovered samples to reference locations, considering environmental variability and contamination. Interpretation considers statistical likelihood and context of recovery. Documentation includes analytical procedures, comparison criteria, and chain of custody. Limitations include possible coincidental matches and environmental effects. Results are reported as 'consistent with', 'cannot be excluded', or 'inconclusive.' Adherence to ASTM E1658 and ISO 17025 ensures reliability.""",
        key_factors=[
            "Physical characteristics",
            "Chemical composition",
            "Comparison criteria",
            "Environmental variability",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1658",
            "ISO 17025",
            "SWGMAT Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="Soil matches may be coincidental; environmental effects may alter characteristics.",
        counter_arguments=[
            "Analytical methods validated.",
            "Statistical likelihood assessed.",
            "Chain of custody maintained."
        ],
        resolution_strategy="Report findings with statistical context and limitations.",
        entity_scope="Forensic laboratory",
        confidence=0.79,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Foster, 2011"
    ),
    DoctrineBlock(
        topic="Forensic Analysis of Trace Blood Evidence on Surfaces",
        keywords=["blood evidence", "trace evidence", "surface analysis", "forensic chemistry", "crime scene"],
        conclusion_template="Trace blood evidence detected on {{surface_type}} was confirmed by presumptive and confirmatory tests.",
        reasoning_framework="""Trace blood evidence analysis on surfaces uses presumptive tests (e.g., Kastle-Meyer, luminol) and confirmatory tests (e.g., ABAcard, DNA analysis). The analyst documents sample collection, test conditions, and chain of custody. Interpretation considers possible false positives and environmental contamination. Results are reported as 'presumptive positive', 'confirmed', or 'not detected.' Adherence to SWGDAM and ISO 17025 ensures reliability. Limitations include low concentration and possible contamination.""",
        key_factors=[
            "Sample collection method",
            "Presumptive and confirmatory tests",
            "Contamination risk",
            "Documentation",
            "Chain of custody"
        ],
        primary_authority=[
            "SWGDAM Guidelines",
            "ISO 17025",
            "ASTM E2329"
        ],
        burden_holder="Prosecution",
        adversary_position="False positives or contamination may affect reliability of blood evidence.",
        counter_arguments=[
            "Validated protocols used.",
            "Chain of custody maintained.",
            "Expert interpretation."
        ],
        resolution_strategy="Report findings with limitations; corroborate with other evidence.",
        entity_scope="Forensic laboratory, crime scene",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Carter, 2012"
    ),
    DoctrineBlock(
        topic="Forensic Analysis of Trace DNA Evidence on Surfaces",
        keywords=["DNA evidence", "trace evidence", "surface analysis", "forensic genetics", "crime scene"],
        conclusion_template="Trace DNA evidence detected on {{surface_type}} yielded a profile matching {{individual}}.",
        reasoning_framework="""Trace DNA evidence analysis on surfaces uses swabbing, extraction, STR analysis, and comparison to reference samples. The analyst documents sample collection, extraction method, amplification parameters, and chain of custody. Interpretation considers possible contamination, low-template DNA, and mixture analysis. Results are reported as 'match', 'inconclusive', or 'excluded.' Adherence to SWGDAM and ISO 17025 ensures reliability. Limitations include low concentration and possible contamination.""",
        key_factors=[
            "Sample collection method",
            "Extraction and amplification",
            "Contamination risk",
            "Mixture analysis",
            "Chain of custody"
        ],
        primary_authority=[
            "SWGDAM Guidelines",
            "ISO 17025",
            "FBI CODIS Standards"
        ],
        burden_holder="Prosecution",
        adversary_position="Low-template DNA or contamination may affect reliability of profile.",
        counter_arguments=[
            "Validated protocols used.",
            "Chain of custody maintained.",
            "Expert interpretation."
        ],
        resolution_strategy="Report findings with limitations; corroborate with other evidence.",
        entity_scope="Forensic laboratory, crime scene",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Bell, 2013"
    ),
    DoctrineBlock(
        topic="Forensic Analysis of Trace Gunshot Residue on Hands",
        keywords=["gunshot residue", "trace evidence", "hand analysis", "SEM-EDS", "forensic chemistry"],
        conclusion_template="SEM-EDS analysis detected trace gunshot residue particles on {{individual}}'s hands, consistent with firearm discharge.",
        reasoning_framework="""Trace gunshot residue analysis on hands uses SEM-EDS to detect and characterize particles containing lead, barium, and antimony. The analyst examines morphology and elemental composition, comparing to reference criteria. Interpretation considers environmental contamination, transfer, and persistence. Documentation includes sample collection, instrument parameters, and chain of custody. Limitations include potential for secondary transfer and loss over time. Results are reported as 'characteristic', 'consistent with', or 'not detected.' Adherence to ASTM E1588 and ISO 17025 ensures reliability.""",
        key_factors=[
            "Particle morphology",
            "Elemental composition",
            "Sample collection timing",
            "Environmental contamination",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1588",
            "ISO 17025",
            "SWGGSR Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="GSR may be transferred or lost; environmental sources may mimic GSR.",
        counter_arguments=[
            "Strict collection protocols followed.",
            "Reference criteria applied.",
            "Results interpreted in context."
        ],
        resolution_strategy="Report findings with limitations; corroborate with other evidence.",
        entity_scope="Forensic laboratory, law enforcement",
        confidence=0.86,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Kim, 2016"
    ),
    DoctrineBlock(
        topic="Forensic Analysis of Trace Explosives Residue on Surfaces",
        keywords=["explosives residue", "trace evidence", "surface analysis", "forensic chemistry", "GC-MS"],
        conclusion_template="GC-MS analysis detected trace explosives residue {{explosive_type}} on {{surface_type}}.",
        reasoning_framework="""Trace explosives residue analysis on surfaces uses swabbing, extraction, and GC-MS for identification. The analyst compares chromatographic profiles to reference standards, considering possible interferences and contamination. Documentation includes sample collection, extraction method, instrument parameters, and chain of custody. Interpretation considers environmental effects and legal status. Results are reported as 'identified', 'not identified', or 'inconclusive.' Adherence to ASTM E1589 and ISO 17025 ensures reliability. Limitations include low concentration and possible contamination.""",
        key_factors=[
            "Sample collection method",
            "Extraction and analysis",
            "Reference standard comparison",
            "Contamination risk",
            "Chain of custody"
        ],
        primary_authority=[
            "ASTM E1589",
            "ISO 17025",
            "SWGEXP Guidelines"
        ],
        burden_holder="Prosecution",
        adversary_position="Low concentration or contamination may affect reliability of residue identification.",
        counter_arguments=[
            "Validated protocols used.",
            "Chain of custody maintained.",
            "Expert interpretation."
        ],
        resolution_strategy="Report findings with limitations; corroborate with other evidence.",
        entity_scope="Forensic laboratory",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="State v. Allen, 2013"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]