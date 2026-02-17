"""
CHEM14 Forensic Chemistry Intelligence Engine v1.0.0
Port 9296 | TIE-Grade | 25+ Doctrine Blocks

Analyzes forensic chemistry: drug identification, trace evidence, arson investigation,
toxicology screening, gunshot residue, and forensic lab quality management.

Authority hierarchy: Peer-reviewed analytical chemistry journals (1.0) > ASTM/SWGDRUG standards (0.95) >
FBI Lab SOPs (0.90) > NIST reference data (0.85) > forensic textbooks (0.70)
"""

import asyncio
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Set, Tuple
from uuid import uuid4

# CRITICAL: Add parent dir to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# === CONFIGURATION ===
ENGINE_ID = "CHEM14"
ENGINE_NAME = "Forensic Chemistry Intelligence Engine"
VERSION = "1.0.0"
PORT = 9296

AUDIT_LOG_PATH = Path(__file__).parent / "audit_trail.jsonl"
TELEMETRY_LOG_PATH = Path(__file__).parent / "telemetry.jsonl"

logger.add(
    Path(__file__).parent / "engine.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
)

# === PYDANTIC MODELS ===

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, description="Forensic chemistry question")
    mode: Literal["FAST", "DEFENSE", "MEMO"] = Field(default="FAST", description="Response depth")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str] = Field(min_items=5, max_items=8)
    conclusion_template: List[str] = Field(min_items=3, max_items=5)
    reasoning_framework: List[str] = Field(min_items=20)
    key_factors: List[str] = Field(min_items=5)
    primary_authority: List[str] = Field(min_items=3, max_items=5)
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str] = Field(min_items=5)
    resolution_strategy: str
    entity_scope: str
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_stratification: Literal["DEFENSIBLE", "AGGRESSIVE", "DISCLOSURE", "HIGH_RISK"]
    controlling_precedent: str


class QueryResponse(BaseModel):
    answer: str
    mode: str
    confidence: float
    stratification: str
    doctrines_triggered: List[str]
    authorities_cited: List[str]
    determinism_hash: str
    timestamp: str
    telemetry: Dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrines_loaded: int
    queries_processed: int
    avg_latency_ms: float
    cache_hit_rate: float
    uptime_seconds: float


# === DOCTRINE CACHE ===

DOCTRINE_BLOCKS: List[DoctrineBlock] = [
    # Drug Identification Doctrines
    DoctrineBlock(
        topic="Presumptive Color Tests for Controlled Substances",
        keywords=["marquis reagent", "cobalt thiocyanate", "duquenois-levine", "presumptive testing", "color reaction", "preliminary screening", "false positives"],
        conclusion_template=[
            "Presumptive color tests provide rapid preliminary screening but are NOT confirmatory.",
            "Multiple reagents should be used to reduce false positives (e.g., Marquis, Mecke, Simon's).",
            "All presumptive positives MUST be confirmed by instrumental analysis (GC-MS, LC-MS/MS) before evidentiary use."
        ],
        reasoning_framework=[
            "Presumptive color tests (Marquis, Mecke, Mandelin, Simon's, Duquenois-Levine, cobalt thiocyanate) are chemical spot tests that produce characteristic color changes in the presence of specific drug classes.",
            "Marquis reagent (formaldehyde + concentrated sulfuric acid) turns purple with opiates, orange-brown with amphetamines.",
            "Duquenois-Levine test is specific for cannabinoids - turns purple in chloroform layer after adding HCl and reagent.",
            "Cobalt thiocyanate produces blue precipitate with cocaine hydrochloride.",
            "These tests are subject to false positives from: aspirin (Marquis), ephedrine (Marquis), diphenhydramine (Marquis), sugar (Duquenois-Levine).",
            "SWGDRUG recommends Category A (IR spectroscopy, MS) or Category B (GC, CE) confirmation for all presumptive positives.",
            "Field tests by law enforcement have higher false positive rates due to: environmental contamination, operator error, cross-reactivity.",
            "Laboratory confirmatory testing is MANDATORY before criminal charges or conviction.",
            "Analysts must document: reagent lot numbers, expiration dates, positive/negative controls, color change observations.",
            "Chain of custody must be maintained from field collection through confirmatory testing.",
            "ASTM E2329 specifies standard practice for identification of seized drugs.",
            "False positives can occur from: common household items, over-the-counter medications, food additives.",
            "Multiple reagent testing reduces (but does not eliminate) false positives.",
            "Positive control (known drug standard) and negative control (blank) must be run concurrently.",
            "Color interpretation is subjective - photographic documentation is recommended.",
            "Reagent stability: Marquis degrades rapidly (weeks), Duquenois-Levine stable for months if refrigerated.",
            "Legal standard: Presumptive tests alone are insufficient for conviction (State v. Tague, 2009).",
            "Expert testimony must clearly distinguish presumptive vs. confirmatory results.",
            "Daubert factors: known error rate of presumptive tests is 10-30% depending on drug class.",
            "Best practice: Use minimum of two different presumptive reagents before proceeding to instrumental confirmation.",
            "NIST maintains reference materials (SRMs) for quality control of drug testing.",
            "Immunoassay screening (ELISA, lateral flow) is an alternative presumptive method with similar limitations.",
            "Gas chromatography-mass spectrometry (GC-MS) is the gold standard for controlled substance confirmation.",
            "SWGDRUG classifies analytical techniques into Categories A, B, C based on discriminating power.",
            "Category A + Category B (different technique) provides sufficient identification per SWGDRUG guidelines.",
            "Minimum sample size requirements vary by test: presumptive tests require micrograms, GC-MS requires milligrams.",
            "Quantitation is required for charging purposes in some jurisdictions (e.g., federal mandatory minimums based on weight).",
            "Purity analysis is relevant for sentencing enhancements and distinguishing personal use from distribution.",
            "Adulterants and cutting agents (levamisole, fentanyl analogs) require separate identification.",
            "Emerging synthetic drugs (novel psychoactive substances) may not react with traditional presumptive tests.",
            "Reference standard libraries must be continuously updated as new designer drugs emerge."
        ],
        key_factors=[
            "Reagent type and specificity for target drug class",
            "Presence of interfering substances (false positive risk)",
            "Need for confirmatory instrumental analysis",
            "Chain of custody documentation",
            "Quality control (positive/negative controls)",
            "Analyst training and competency",
            "Legal admissibility standards (Daubert, Frye)",
            "Known error rates for specific reagent/drug combinations"
        ],
        primary_authority=[
            "SWGDRUG Recommendations v8.0 (2019) - Category classification system",
            "ASTM E2329-17 Standard Practice for Identification of Seized Drugs",
            "NIJ Report: Color Test Reagents/Kits for Preliminary Identification of Drugs of Abuse (2000)",
            "United Nations Office on Drugs and Crime: Recommended Methods for Testing Illicit Drugs (2009)"
        ],
        burden_holder="Prosecution bears burden of proving drug identity beyond reasonable doubt with confirmatory testing",
        adversary_position="Defense challenges: false positive presumptive tests, contamination, lack of confirmatory analysis, analyst error",
        counter_arguments=[
            "Presumptive tests alone have 10-30% false positive rate (peer-reviewed studies)",
            "Common household substances produce false positives (Heller et al., 2015)",
            "Field test contamination from handling multiple evidence items",
            "Reagent degradation if improperly stored (Marquis degrades in weeks)",
            "Operator error in color interpretation (subjective assessment)",
            "Lack of positive control run concurrently with evidence sample",
            "Confirmatory GC-MS not performed before charging decision",
            "Violation of SWGDRUG minimum standards (single Category C technique insufficient)"
        ],
        resolution_strategy="Require confirmatory GC-MS or IR spectroscopy per SWGDRUG Category A+B standard; document all QC measures; expert testimony explaining limitations of presumptive tests",
        entity_scope="Law enforcement, forensic laboratories, prosecution, defense",
        confidence=0.95,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="SWGDRUG Recommendations - scientifically accepted standard for drug identification"
    ),

    DoctrineBlock(
        topic="GC-MS Confirmatory Analysis for Controlled Substances",
        keywords=["gas chromatography", "mass spectrometry", "retention time", "mass spectrum", "library match", "NIST database", "quantitation"],
        conclusion_template=[
            "GC-MS combines chromatographic separation with mass spectral identification for definitive drug identification.",
            "Match quality criteria: retention time within ±2% RSD, mass spectrum library match >800/1000, presence of molecular ion and characteristic fragments.",
            "Quantitation requires internal standard method with calibration curve (r² >0.995)."
        ],
        reasoning_framework=[
            "Gas chromatography-mass spectrometry (GC-MS) is the gold standard for controlled substance identification (SWGDRUG Category A technique).",
            "GC provides separation based on volatility and interaction with stationary phase.",
            "MS provides molecular weight (molecular ion) and fragmentation pattern (structural information).",
            "Retention time (RT) is compared to certified reference standard run under identical conditions.",
            "RT match criterion: within ±2% relative standard deviation of reference standard.",
            "Mass spectrum is compared to NIST/Wiley libraries (>300,000 compounds).",
            "Library match score >800/1000 (80% similarity) is typical acceptance threshold.",
            "Presence of molecular ion [M]+ confirms molecular weight.",
            "Characteristic fragment ions provide structural confirmation (e.g., m/z 91 for amphetamine).",
            "Full scan mode (m/z 40-550) for unknown identification.",
            "Selected ion monitoring (SIM) for trace level quantitation (higher sensitivity).",
            "Internal standard method compensates for matrix effects and injection variability.",
            "Deuterated analogs (e.g., cocaine-d3) are ideal internal standards (same chemistry, different mass).",
            "Calibration curve: minimum 5 concentration levels, r² >0.995, covering expected sample range.",
            "Limit of detection (LOD): typically 10-50 ng/mL for common drugs.",
            "Limit of quantitation (LOQ): 3-10x LOD, lowest point on calibration curve.",
            "Matrix-matched standards preferred (e.g., blood standards for blood samples).",
            "Derivatization required for polar drugs (e.g., BSTFA for amphetamines, MBTFA for cannabinoids).",
            "Chiral separation requires derivatization with chiral reagent (e.g., S-heptafluorobutyryl-prolyl chloride).",
            "Quality control: analyze blank, positive control, negative control with each batch.",
            "Ion ratios must match reference standard within ±20% (e.g., m/z 182/303 for cocaine).",
            "Isotope pattern confirms molecular formula (chlorine has 35Cl:37Cl = 3:1).",
            "Retention index (Kovats index) provides retention time standardization across instruments.",
            "NIST maintains Standard Reference Materials (SRMs) for quality assurance.",
            "Proficiency testing through CAP, ASCLD/LAB ensures analyst competency.",
            "ASTM E2329 specifies minimum requirements: Category A + Category B from different technique class.",
            "Common interferences: cutting agents (levamisole, phenacetin), degradation products, co-extracted matrix components.",
            "Method validation per ISO 17025: accuracy, precision, linearity, LOD, LOQ, specificity, robustness.",
            "Measurement uncertainty must be calculated and reported per EURACHEM/CITAC guidelines.",
            "Reporting: drug identified, concentration (if quantitative), measurement uncertainty, method used.",
            "Expert testimony must explain: retention time match, mass spectrum match, library score, confirmatory ion ratios."
        ],
        key_factors=[
            "Retention time match to reference standard (±2% RSD)",
            "Mass spectrum library match score (>800/1000)",
            "Presence of molecular ion and characteristic fragments",
            "Ion ratio confirmation (within ±20% of standard)",
            "Internal standard performance (recovery 70-130%)",
            "Calibration curve quality (r² >0.995)",
            "Quality control sample results (within ±15% of target)",
            "Analyst training on instrument operation and data interpretation"
        ],
        primary_authority=[
            "SWGDRUG Recommendations v8.0 - Category A technique classification",
            "ASTM E2329-17 Standard Practice for Identification of Seized Drugs",
            "Scientific Working Group for Forensic Toxicology (SWGTOX) Standard Practices",
            "ISO/IEC 17025:2017 General Requirements for Competence of Testing Laboratories"
        ],
        burden_holder="Laboratory bears burden of validating method and demonstrating reliable identification/quantitation",
        adversary_position="Defense challenges: instrument calibration, contamination, analyst error in peak identification, library match false positives",
        counter_arguments=[
            "GC-MS library matches can be ambiguous for isomers (same mass spectrum, different retention time)",
            "Contamination from previous injection (carryover) if inadequate washout",
            "Instrument drift if calibration not performed within 24 hours of sample analysis",
            "Matrix effects suppress ionization efficiency (ion suppression)",
            "Co-elution of compounds with similar retention times",
            "Poor chromatographic resolution (tailing peaks, broad peaks)",
            "Mass spectrum match score threshold too low (<900 for complex mixtures)",
            "Internal standard failure (degradation, suppression) not detected",
            "Calibration curve outside linear range",
            "Failure to account for measurement uncertainty in quantitative results"
        ],
        resolution_strategy="Use two Category A techniques (GC-MS + IR) or Category A + Category B per SWGDRUG; document all QC results; calculate and report measurement uncertainty; maintain instrument calibration logs",
        entity_scope="Forensic laboratories, toxicology labs, medical examiners",
        confidence=0.98,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="SWGDRUG Category A + Category B minimum standard for courtroom testimony"
    ),

    DoctrineBlock(
        topic="Trace Fiber Evidence Comparison and Analysis",
        keywords=["fiber comparison", "microspectrophotometry", "cross-sectional morphology", "polarized light microscopy", "textile fibers", "transfer evidence"],
        conclusion_template=[
            "Fiber evidence is class evidence - can demonstrate association but not individual identification.",
            "Comparison requires: color (microspectrophotometry), morphology (cross-section, diameter), chemistry (FTIR, Raman).",
            "Statistical significance depends on fiber rarity, number of matching fibers, and background population data."
        ],
        reasoning_framework=[
            "Fibers are trace evidence transferred by contact (Locard's Exchange Principle).",
            "Natural fibers: cotton, wool, silk, linen - identified by morphology and chemical tests.",
            "Synthetic fibers: polyester, nylon, acrylic, polypropylene - require instrumental analysis.",
            "Polarized light microscopy (PLM) reveals: birefringence, cross-sectional shape, diameter, surface features.",
            "Microspectrophotometry measures color in visible spectrum (400-700 nm) - highly discriminating.",
            "Color match criteria: spectral curves overlay within instrument variability.",
            "Cross-sectional morphology varies by manufacturer: trilobal, round, dog-bone, hollow, crenulated.",
            "Longitudinal features: striations, pitting, delustrant particles (TiO2).",
            "Diameter measurement: minimum 25 fibers, report mean and standard deviation.",
            "Fourier-transform infrared spectroscopy (FTIR) identifies polymer type (polyester vs. nylon).",
            "Raman spectroscopy provides complementary chemical information, useful for dyes.",
            "Thermal analysis (DSC, TGA) determines melting point and degradation temperature.",
            "Pyrolysis-GC-MS fragments polymer for detailed chemical characterization.",
            "Dye analysis by thin-layer chromatography (TLC) separates and identifies dye components.",
            "Comparison conclusions: 1) Could have originated from same source, 2) Did not originate from same source, 3) Inconclusive.",
            "Statistical weight depends on fiber rarity: common blue cotton vs. rare purple trilobal polyester.",
            "Persistence studies show fibers shed rapidly in first hour, decline over 24 hours.",
            "Background fiber surveys establish population frequency (e.g., blue denim is ubiquitous).",
            "Transfer can be direct (person to victim) or indirect (person to car seat to victim) - secondary transfer.",
            "Forensic Fiber Examination Guidelines (FBI, SWGMAT) specify minimum comparison criteria.",
            "Quality assurance: blind proficiency tests, inter-laboratory comparisons.",
            "Limitation: Fiber evidence alone is insufficient for conviction - must be corroborated.",
            "False associations possible if common fiber type (e.g., white cotton) - low probative value.",
            "Expert testimony must state: degree of similarity, rarity of fiber type, cannot individualize to single source.",
            "Daubert factors: PLM and microspectrophotometry are scientifically accepted (100+ years), known error rates low.",
            "Reporting: description of fibers, analytical techniques used, comparison results, significance statement.",
            "ASTM E2225 Standard Guide for Forensic Examination of Non-Reactive Dyes in Textile Fibers.",
            "SWGMAT Forensic Human Hair Examination Guidelines (2005) - analogous methodology.",
            "Fiber databases (e.g., FBI Fiber Database) contain >10,000 samples for comparison.",
            "Emerging techniques: LA-ICP-MS for elemental analysis of dyes and additives."
        ],
        key_factors=[
            "Fiber type (natural vs. synthetic)",
            "Color match by microspectrophotometry",
            "Cross-sectional morphology match",
            "Diameter and longitudinal features",
            "Polymer identification by FTIR",
            "Dye characterization",
            "Rarity of fiber in general population",
            "Number of matching fibers recovered",
            "Alternative explanations (secondary transfer, background contamination)"
        ],
        primary_authority=[
            "SWGMAT Forensic Fiber Examination Guidelines (1999)",
            "ASTM E2225-16 Standard Guide for Forensic Examination of Non-Reactive Dyes",
            "FBI Laboratory Trace Evidence Unit Protocols",
            "Robertson and Grieve: Forensic Examination of Fibers (2nd ed, 1999) - foundational textbook"
        ],
        burden_holder="Prosecution must demonstrate fiber similarity and statistical significance; defense can challenge rarity claims",
        adversary_position="Defense argues: common fiber type (low probative value), secondary transfer, background contamination, lab error",
        counter_arguments=[
            "Fiber is common type (e.g., blue denim, white cotton) - found in general population",
            "Secondary transfer explains presence (e.g., public transportation seat)",
            "Background contamination in lab or evidence packaging",
            "Insufficient number of fibers for statistical significance",
            "Microspectrophotometry color match within instrument error but visually different",
            "Lack of population frequency data for claimed rare fiber",
            "Persistence studies show fibers shed quickly - timeline inconsistent",
            "Cross-contamination during collection or packaging (fibers in tweezers)",
            "Alternative source for fibers (e.g., victim's own clothing)",
            "Expert overstates significance - fiber is class evidence, not individualization"
        ],
        resolution_strategy="Conduct comprehensive fiber comparison (color, morphology, chemistry); consult fiber databases for rarity; acknowledge class evidence limitations; corroborate with other evidence types",
        entity_scope="Forensic laboratories, trace evidence examiners, violent crime investigations",
        confidence=0.85,
        confidence_stratification="DISCLOSURE",
        controlling_precedent="SWGMAT guidelines - scientifically accepted methodology, but results are class evidence only"
    ),

    DoctrineBlock(
        topic="Ignitable Liquid Residue Analysis for Arson Investigation",
        keywords=["arson", "accelerant", "ignitable liquid", "passive headspace", "GC-MS", "ASTM E1618", "petroleum distillates", "aromatic solvents"],
        conclusion_template=[
            "Ignitable liquid residues (ILRs) are detected by passive headspace concentration followed by GC-MS analysis per ASTM E1618.",
            "Classification: gasoline, medium petroleum distillates, heavy petroleum distillates, aromatic products, normal alkanes.",
            "Presence of ILR does not prove arson - must consider legitimate sources (stored fuel, spills) and fire dynamics."
        ],
        reasoning_framework=[
            "Arson investigation requires detection of ignitable liquid residues (accelerants) in fire debris.",
            "ASTM E1618 is the standard test method for ILR identification by GC-MS.",
            "Passive headspace concentration: debris sealed in can, volatiles partition into headspace, adsorbed onto activated charcoal strip.",
            "Charcoal strip eluted with carbon disulfide (CS2), extract analyzed by GC-MS.",
            "Gas chromatography separates components by boiling point and polarity.",
            "Flame ionization detector (FID) responds to carbon-containing compounds - produces characteristic pattern.",
            "Mass spectrometry confirms identity of individual peaks (e.g., toluene m/z 91, xylenes m/z 106).",
            "Ignitable liquid classification per ASTM E1618: gasoline (C4-C12), medium petroleum distillates (C8-C13), heavy petroleum distillates (C9-C23+), aromatic products (toluene, xylene), normal alkanes (C8-C20).",
            "Gasoline pattern: bell-shaped curve with alkanes, cycloalkanes, aromatics (toluene, xylene, trimethylbenzenes).",
            "Diesel pattern: broad hump of alkanes C10-C23, fewer aromatics than gasoline.",
            "Weathering: light ends evaporate first (C4-C7 alkanes), shifts pattern to heavier components.",
            "Substrate interference: pyrolysis products from burning carpet, plastic, wood can mimic ILR patterns.",
            "Comparison to NIST/ILRC reference libraries (>500 ignitable liquid patterns).",
            "Positive control: known ignitable liquid run with each batch to verify method performance.",
            "Negative control: unburned substrate from same source to identify background hydrocarbons.",
            "Quality assurance: blank charcoal strips processed alongside evidence to detect contamination.",
            "Target compound analysis: specific ions for key components (e.g., m/z 57 for alkanes, m/z 91 for aromatics).",
            "Interpretation challenges: mixed products (gasoline + diesel), heavily weathered samples, substrate interference.",
            "Legitimate sources of ILRs: stored lawn mower fuel, spilled paint thinner, automobile fluids.",
            "Fire dynamics: hot gas layer can redistribute ILRs from point of origin to remote locations.",
            "Canine accelerant detection aids in sampling - dogs trained to alert on petroleum odors.",
            "Reporting: presence/absence of ILR, classification per ASTM E1618, pattern description, cannot determine original quantity or timing.",
            "Expert testimony must explain: ILR detection does not prove intentional use, legitimate sources possible.",
            "Daubert factors: ASTM E1618 is peer-reviewed, scientifically accepted method; error rate depends on analyst experience.",
            "False positives from: incomplete substrate control, contaminated collection cans, environmental petroleum products.",
            "False negatives from: heavy fire damage (complete combustion), extended weathering, water suppression washing away residues.",
            "Alternative methods: solid-phase microextraction (SPME) - faster but less validated than passive headspace.",
            "ASTM E1412: Standard Practice for Separation of Ignitable Liquid Residues - collection and packaging guidelines.",
            "NFPA 921: Guide for Fire and Explosion Investigations - establishes scientific basis for arson investigation.",
            "Chain of custody critical: document debris collection location, time, packaging, storage temperature."
        ],
        key_factors=[
            "Presence of ignitable liquid residue pattern by GC-MS",
            "Classification per ASTM E1618 (gasoline, diesel, etc.)",
            "Degree of weathering (light ends lost)",
            "Substrate interference from pyrolysis products",
            "Negative control from unburned substrate",
            "Legitimate sources for detected ILR",
            "Fire dynamics and ILR redistribution",
            "Quantity of ILR (trace vs. significant)",
            "Spatial distribution (multiple pour patterns)"
        ],
        primary_authority=[
            "ASTM E1618-19 Standard Test Method for Ignitable Liquid Residues in Extracts by GC-MS",
            "ASTM E1412-19 Standard Practice for Separation of Ignitable Liquid Residues from Fire Debris Samples",
            "NFPA 921 Guide for Fire and Explosion Investigations (2021 ed)",
            "NIST/ILRC Ignitable Liquids Reference Collection Database"
        ],
        burden_holder="Prosecution must prove ILR presence AND intentional use (arson); defense challenges legitimate sources",
        adversary_position="Defense argues: legitimate source (stored fuel, spills), substrate interference, contamination, fire dynamics redistribute ILR",
        counter_arguments=[
            "ILR from legitimate stored gasoline (lawn mower can in garage)",
            "Paint thinner or other solvents used for household projects",
            "Automobile fluids (motor oil, transmission fluid) contain petroleum distillates",
            "Substrate pyrolysis products mimic ILR pattern (carpet backing, synthetic fabrics)",
            "Contaminated collection can (reused can with ILR from prior fire)",
            "Fire dynamics carried ILR from remote location to area of origin",
            "Environmental contamination (fuel spill on driveway weeks before fire)",
            "Incomplete negative control - substrate itself contains background hydrocarbons",
            "Analyst bias - pattern classification is subjective for mixed or weathered samples",
            "Lack of quantity estimate - trace ILR vs. significant pour pattern"
        ],
        resolution_strategy="Collect unburned substrate controls from same source; document all legitimate ILR sources at scene; use canine alerts to guide sampling; acknowledge ILR presence does not prove arson without corroborating evidence (multiple pour patterns, lack of electrical ignition source, etc.)",
        entity_scope="Fire investigators, forensic laboratories, arson prosecution/defense",
        confidence=0.90,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="ASTM E1618 and NFPA 921 - scientifically accepted standards for ILR analysis and fire investigation"
    ),

    DoctrineBlock(
        topic="Forensic Toxicology Immunoassay Screening and Confirmatory Testing",
        keywords=["immunoassay", "ELISA", "lateral flow", "cross-reactivity", "cutoff concentration", "LC-MS/MS confirmation", "drug metabolites"],
        conclusion_template=[
            "Immunoassay screening provides rapid presumptive results but suffers from cross-reactivity and false positives.",
            "All positive immunoassay results MUST be confirmed by LC-MS/MS or GC-MS for legal purposes.",
            "Metabolite detection (e.g., benzoylecgonine for cocaine, THC-COOH for marijuana) indicates prior drug use."
        ],
        reasoning_framework=[
            "Forensic toxicology screening uses immunoassays (ELISA, EMIT, KIMS) for rapid drug detection.",
            "Immunoassays rely on antibody-antigen binding - antibody specific to drug or drug class.",
            "Enzyme-linked immunosorbent assay (ELISA): drug in sample competes with enzyme-labeled drug for antibody binding sites.",
            "Colorimetric detection - higher color intensity = less drug in sample (competitive immunoassay).",
            "Lateral flow immunoassay: urine applied to test strip, colored line appears if drug absent (negative result).",
            "Cutoff concentrations: immunoassay is positive if drug exceeds threshold (e.g., 50 ng/mL for THC-COOH, 300 ng/mL for cocaine).",
            "SAMHSA (Substance Abuse and Mental Health Services Administration) sets federal workplace testing cutoffs.",
            "Cross-reactivity: antibody binds to structurally similar compounds, causing false positives.",
            "Amphetamine immunoassay cross-reacts with: ephedrine, pseudoephedrine, phenylephrine, ranitidine, bupropion.",
            "Opiate immunoassay cross-reacts with: poppy seeds, quinolone antibiotics (levofloxacin), rifampin.",
            "THC immunoassay cross-reacts with: ibuprofen, naproxen, efavirenz (rare, disputed).",
            "Cocaine immunoassay relatively specific - few cross-reactants, detects benzoylecgonine metabolite.",
            "Phencyclidine (PCP) immunoassay cross-reacts with: dextromethorphan, tramadol, venlafaxine.",
            "Benzodiazepine immunoassay variable sensitivity - detects oxazepam well, misses alprazolam and clonazepam.",
            "Confirmatory testing by liquid chromatography-tandem mass spectrometry (LC-MS/MS) is MANDATORY for legal cases.",
            "LC-MS/MS separates drug from metabolites and matrix components, then identifies by mass-to-charge ratio.",
            "Multiple reaction monitoring (MRM): parent ion fragmented, specific daughter ions monitored (high specificity).",
            "Quantitation by internal standard method - deuterated analog of target drug added to sample.",
            "Calibration curve: 6-8 concentration levels, r² >0.99, covering cutoff and physiological range.",
            "SWGTOX (Scientific Working Group for Forensic Toxicology) requires: LC-MS/MS or GC-MS for confirmation.",
            "Confirmation cutoff typically lower than screening cutoff (e.g., 15 ng/mL vs. 50 ng/mL for THC-COOH).",
            "Metabolites detected: benzoylecgonine (cocaine), THC-COOH (marijuana), morphine (heroin), 6-MAM (heroin-specific).",
            "Parent drug vs. metabolite: presence of metabolite proves ingestion, parent drug could be external contamination.",
            "Postmortem redistribution: drug concentrations change after death due to diffusion from organs into blood.",
            "Quality control: analyze blank, low positive, high positive with each batch.",
            "Proficiency testing through CAP, SOFT/AAFS ensures analyst competency.",
            "Reporting: drug/metabolite identified, concentration, method used, interpretation (therapeutic, toxic, lethal).",
            "Therapeutic drug monitoring: ensuring medication compliance or detecting toxicity.",
            "Pharmacokinetics: absorption, distribution, metabolism, excretion (ADME) affect interpretation.",
            "Expert testimony must explain: immunoassay limitations, confirmation necessity, metabolite significance."
        ],
        key_factors=[
            "Immunoassay positive vs. negative result",
            "Cutoff concentration exceeded",
            "Known cross-reactants for specific drug class",
            "Confirmation by LC-MS/MS or GC-MS",
            "Parent drug vs. metabolite detection",
            "Quantitative concentration vs. therapeutic/toxic range",
            "Quality control results (within ±20% of target)",
            "Chain of custody and specimen integrity"
        ],
        primary_authority=[
            "SWGTOX Standard Practices for Method Validation in Forensic Toxicology (2013)",
            "SAMHSA Mandatory Guidelines for Federal Workplace Drug Testing Programs (2017)",
            "CAP Laboratory Accreditation Program Forensic Toxicology Checklist",
            "Baselt's Disposition of Toxic Drugs and Chemicals in Man (11th ed) - reference for interpretation"
        ],
        burden_holder="Laboratory must confirm all positive immunoassay results by LC-MS/MS before reporting; prosecution relies on confirmed results",
        adversary_position="Defense challenges: false positive immunoassay, chain of custody, passive exposure, postmortem redistribution, lab error",
        counter_arguments=[
            "Immunoassay false positive from cross-reactive substance (e.g., poppy seeds for opiates)",
            "Over-the-counter medication caused positive screen (pseudoephedrine for amphetamines)",
            "Passive exposure to marijuana smoke (second-hand smoke defense - generally rejected for THC-COOH >15 ng/mL)",
            "Postmortem redistribution inflates blood concentration - femoral blood preferred over heart blood",
            "Chain of custody break - specimen integrity compromised",
            "Confirmatory testing not performed before legal action (violation of SWGTOX standards)",
            "Cutoff concentration arbitrary - low positive may not indicate impairment",
            "Metabolite-only detection - cannot determine timing of use (THC-COOH persists for weeks)",
            "Lab contamination or analyst error during confirmation",
            "Therapeutic use of prescribed medication (benzodiazepines, opiates) - not illicit use"
        ],
        resolution_strategy="Always confirm positive immunoassays by LC-MS/MS; use metabolite-specific confirmation (e.g., THC-COOH not parent THC); document QC results; expert testimony on cross-reactivity and confirmation necessity; consider alternative explanations (prescribed medications, poppy seeds)",
        entity_scope="Forensic toxicology laboratories, medical examiners, DUI prosecution, workplace drug testing, pain management",
        confidence=0.93,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="SWGTOX and SAMHSA guidelines - scientifically accepted standards requiring confirmatory testing for all legal applications"
    ),

    DoctrineBlock(
        topic="Gunshot Residue Analysis by SEM-EDS",
        keywords=["gunshot residue", "GSR", "SEM-EDS", "lead", "barium", "antimony", "primer residue", "particle morphology"],
        conclusion_template=[
            "Gunshot residue (GSR) particles are detected by scanning electron microscopy with energy-dispersive X-ray spectroscopy (SEM-EDS).",
            "Characteristic GSR: spheroidal particle containing lead (Pb), barium (Ba), and antimony (Sb) - originates from primer.",
            "GSR presence indicates: fired a gun, was in close proximity to discharge, or contacted GSR-contaminated surface - cannot distinguish between scenarios."
        ],
        reasoning_framework=[
            "Gunshot residue (GSR) originates from primer compound, gunpowder, bullet, and cartridge case.",
            "Primer composition: lead styphnate (initiator), barium nitrate (oxidizer), antimony sulfide (fuel).",
            "Upon discharge, primer vaporizes and condenses into spheroidal particles containing Pb, Ba, Sb.",
            "Particle size: 0.5-5 micrometers (invisible to naked eye).",
            "SEM-EDS (scanning electron microscopy with energy-dispersive X-ray spectroscopy) detects and characterizes particles.",
            "SEM provides high-magnification imaging - identifies spheroidal morphology.",
            "EDS provides elemental composition - detects Pb, Ba, Sb, and ratios.",
            "ASTM E1588 Standard Guide for GSR Analysis by SEM-EDS.",
            "Characteristic GSR particle: contains Pb AND Ba AND Sb, spheroidal shape, size 0.5-5 microns.",
            "Consistent with GSR: contains two of three elements (Pb+Ba, Pb+Sb, Ba+Sb).",
            "Indicative of GSR: contains one element (Pb alone, Ba alone, Sb alone) - low probative value.",
            "FBI criteria (pre-2006): minimum 1 characteristic particle for positive result.",
            "Current consensus (ASTM, SWGGUN): report particle type and count, avoid absolute conclusions.",
            "Collection: adhesive stubs applied to hands (back of hand, web between thumb/index, palm) within 4 hours of incident.",
            "Persistence: GSR particles shed rapidly - 50% lost in first hour, 90% lost by 4 hours.",
            "Hand washing, rubbing, or normal activity removes GSR quickly.",
            "Secondary transfer: GSR can transfer from contaminated surface (car door, steering wheel) to hands.",
            "Occupational exposure: law enforcement, firearms instructors, military personnel have background GSR.",
            "Environmental sources of Pb, Ba, Sb: brake dust (Ba), wheel weights (Pb), fireworks (Ba), batteries (Pb).",
            "Lead-free primers (e.g., CCI Blazer) lack Pb - contain Zn, Ti, or other metals instead.",
            "Ammunition-specific patterns: SINTOX primer has Sr, Zn instead of Pb, Ba, Sb.",
            "Quality assurance: analyze blank stubs, positive control (known GSR), negative control with each batch.",
            "Automated SEM-EDS systems scan entire stub surface (1000+ particles) in 2-4 hours.",
            "Manual review required: analyst confirms spheroidal morphology and elemental composition of flagged particles.",
            "False positives from: environmental contamination, occupational exposure, secondary transfer.",
            "False negatives from: delayed collection (>4 hours), hand washing, heavy shedding, ammunition type.",
            "Interpretation limitations: cannot determine: shooter vs. bystander, time of shooting (beyond persistence window), number of shots, firearm type.",
            "SWGGUN (Scientific Working Group for Gunshot Residue) disbanded 2006 - standards still followed.",
            "Reporting: number of characteristic, consistent, indicative particles; avoid definitive conclusions (did fire vs. did not fire).",
            "Expert testimony must explain: persistence window, secondary transfer, occupational exposure, alternative sources.",
            "Daubert factors: SEM-EDS widely accepted, but interpretation is nuanced - error rate depends on analyst experience."
        ],
        key_factors=[
            "Presence of characteristic particles (Pb+Ba+Sb, spheroidal)",
            "Number of characteristic particles (1 vs. 10+ has different weight)",
            "Time between incident and collection (<4 hours optimal)",
            "Hand washing or activity between incident and collection",
            "Occupational or environmental exposure to Pb, Ba, Sb",
            "Ammunition type (standard primer vs. lead-free)",
            "Secondary transfer possibility",
            "Analyst training and competency on SEM-EDS operation"
        ],
        primary_authority=[
            "ASTM E1588-20 Standard Guide for Gunshot Residue Analysis by SEM-EDS",
            "SWGGUN Minimum Requirements for Reporting GSR (2011) - now archived but still cited",
            "Berk et al.: Gunshot Residue in Chicago Police Vehicles (2009) - secondary transfer study",
            "Schwoeble and Exline: Current Methods in Forensic Gunshot Residue Analysis (2000)"
        ],
        burden_holder="Prosecution must prove GSR presence and link to incident; defense challenges alternative sources and transfer",
        adversary_position="Defense argues: secondary transfer, occupational exposure, environmental contamination, delayed collection, lack of hand washing timeline",
        counter_arguments=[
            "GSR from secondary transfer (touched contaminated car door, steering wheel)",
            "Occupational exposure (law enforcement, firearms instructor, military personnel)",
            "Environmental sources (brake dust contains Ba, wheel weights contain Pb)",
            "Delayed collection (>4 hours) - most GSR already shed",
            "Hand washing between incident and collection removed GSR",
            "Lead-free ammunition used - different elemental signature",
            "Single characteristic particle insufficient - could be environmental coincidence",
            "Proximity to discharge (bystander) vs. actual shooter - cannot distinguish",
            "Contamination during collection or analysis (dirty tweezers, lab environment)",
            "SEM-EDS operator error - false identification of non-GSR particles as GSR"
        ],
        resolution_strategy="Collect GSR samples within 4 hours; document hand washing and activity timeline; analyze negative controls; acknowledge limitations (cannot determine shooter vs. proximity); report particle counts, not definitive conclusions; expert testimony on persistence, transfer, and alternative sources",
        entity_scope="Forensic laboratories, shooting investigations, homicide, suicide, self-defense claims",
        confidence=0.88,
        confidence_stratification="DISCLOSURE",
        controlling_precedent="ASTM E1588 - scientifically accepted method, but interpretation limitations must be acknowledged"
    ),

    DoctrineBlock(
        topic="Chain of Custody Protocols for Forensic Evidence",
        keywords=["chain of custody", "evidence integrity", "documentation", "tamper-proof seals", "evidence log", "transfer documentation", "admissibility"],
        conclusion_template=[
            "Chain of custody is the chronological documentation of evidence handling from collection to courtroom.",
            "Every transfer must be documented: date, time, transferring party, receiving party, reason for transfer.",
            "Breaks in chain of custody can result in evidence exclusion - burden on prosecution to demonstrate continuous accountability."
        ],
        reasoning_framework=[
            "Chain of custody establishes evidence integrity and prevents tampering, substitution, or contamination.",
            "Federal Rules of Evidence 901: authentication requirement for physical evidence.",
            "Chain begins at scene: documenting collection location, time, collector identity, packaging.",
            "Evidence packaged in tamper-evident containers (heat-sealed bags, evidence tape, numbered seals).",
            "Evidence log records: case number, evidence number, description, collection date/time, collector signature.",
            "Every transfer documented: from collector to evidence custodian, custodian to analyst, analyst to court.",
            "Transfer form includes: date, time, transferring party signature, receiving party signature, purpose of transfer.",
            "Evidence storage: locked evidence room with restricted access, climate-controlled if needed (biologicals, drugs).",
            "Access log: anyone accessing evidence vault signs in/out with date, time, reason.",
            "Temporary removal for analysis: analyst signs out evidence, documents analytical steps, signs back in upon completion.",
            "Subsampling documented: quantity removed for analysis, quantity remaining, returned to storage.",
            "Destructive testing: photograph before testing, document quantity consumed, retain residual if possible.",
            "Transport protocols: evidence sealed in containers, hand-delivered or shipped via courier with tracking.",
            "Shipping documentation: sender, recipient, date shipped, date received, condition upon receipt.",
            "Digital evidence: hash values (MD5, SHA-256) calculated at collection and verified at analysis - ensures file integrity.",
            "Biological evidence: refrigerated storage at 4 degrees C or frozen at -20 degrees C, desiccated for long-term storage.",
            "Drug evidence: locked cabinet or vault, dual custody for controlled substances.",
            "Firearms evidence: unloaded, trigger lock applied, stored in locked cabinet separate from ammunition.",
            "Quality assurance: periodic inventory audits verify evidence location and condition.",
            "Breaks in chain of custody: missing transfer documentation, unsigned logs, unexplained gaps in timeline.",
            "Legal standard: prosecution must prove evidence is 'substantially the same' as collected (minor degradation acceptable).",
            "Defense challenges: break in chain creates reasonable doubt about evidence integrity.",
            "Expert testimony: custodian testifies to evidence handling, analyst testifies to testing and results.",
            "Electronic signature systems: LIMS (Laboratory Information Management System) tracks digital chain of custody.",
            "Barcode/RFID tracking: automates evidence tracking, reduces human error in logging.",
            "NIJ guidelines: Evidence Collection and Handling (2008) - best practices for law enforcement.",
            "ISO 17025 requires: documented procedures for evidence handling, storage, and disposal.",
            "Accreditation bodies (ASCLD/LAB, ANAB) audit chain of custody protocols during inspections.",
            "Disposal protocols: evidence retained until appeals exhausted, then destroyed per agency policy with documentation."
        ],
        key_factors=[
            "Documentation completeness (every transfer logged)",
            "Signatures of all handlers",
            "Tamper-evident packaging integrity",
            "Storage conditions appropriate for evidence type",
            "Access control to evidence storage",
            "Timeline consistency (no unexplained gaps)",
            "Subsampling and consumption documentation",
            "Condition of evidence (degradation, contamination)"
        ],
        primary_authority=[
            "Federal Rules of Evidence 901 - Authentication and Identification",
            "NIJ Special Report: Evidence Collection and Handling (2008)",
            "ISO/IEC 17025:2017 - Requirements for Testing Laboratories (Section 7.4 on handling)",
            "SWGDAM Guidelines for Evidence Collection and Preservation (DNA)"
        ],
        burden_holder="Prosecution bears burden of proving continuous chain of custody; defense challenges breaks or gaps",
        adversary_position="Defense argues: break in chain creates reasonable doubt, evidence could have been tampered with, contaminated, or substituted",
        counter_arguments=[
            "Missing transfer documentation for critical step (e.g., delivery to lab)",
            "Unsigned evidence log entries",
            "Unexplained gap in timeline (evidence unaccounted for 24+ hours)",
            "Tamper-evident seal broken or missing",
            "Evidence stored in unsecured location (unlocked cabinet)",
            "Unauthorized access to evidence storage (access log shows unexplained entries)",
            "Condition discrepancy (evidence described differently at collection vs. analysis)",
            "Digital evidence hash mismatch (file altered)",
            "Lack of refrigeration for biological evidence (degradation)",
            "Substitution possible - no unique identifier (e.g., serial number, photo documentation)"
        ],
        resolution_strategy="Implement rigorous chain of custody protocols per NIJ/ISO guidelines; use tamper-evident packaging; log every transfer with signatures; photograph evidence at each step; use LIMS for automated tracking; train all personnel on procedures; audit compliance regularly",
        entity_scope="Law enforcement, forensic laboratories, evidence custodians, prosecutors, defense attorneys",
        confidence=0.97,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Federal Rules of Evidence 901 and ISO 17025 - legally and scientifically mandated standards"
    ),

    DoctrineBlock(
        topic="DNA Profiling by STR Analysis and CODIS Database Searching",
        keywords=["DNA profiling", "STR", "short tandem repeats", "CODIS", "random match probability", "paternity testing", "forensic genetics"],
        conclusion_template=[
            "DNA profiling by short tandem repeat (STR) analysis is the gold standard for human identification.",
            "CODIS (Combined DNA Index System) enables nationwide searching of DNA profiles against convicted offender and forensic databases.",
            "Random match probability (RMP) quantifies the statistical rarity of a DNA match - typically 1 in trillions for full 20-locus profile."
        ],
        reasoning_framework=[
            "DNA (deoxyribonucleic acid) contains genetic information unique to each individual (except identical twins).",
            "Short tandem repeats (STRs) are regions of DNA with repeating sequences (e.g., GATA GATA GATA).",
            "Number of repeats varies between individuals - highly polymorphic markers.",
            "FBI CODIS core loci: originally 13 loci (expanded to 20 loci in 2017).",
            "Modern STR kits analyze 20-24 loci simultaneously (multiplex PCR).",
            "Polymerase chain reaction (PCR) amplifies STR regions from trace DNA (nanograms).",
            "Capillary electrophoresis separates PCR products by size (number of repeats).",
            "Fluorescent labels allow multi-color detection (5-6 dyes).",
            "Genetic analyzer (e.g., ABI 3500) produces electropherogram - peaks represent alleles.",
            "Each person has two alleles per locus (one from each parent) - homozygous (same) or heterozygous (different).",
            "DNA profile: combination of allele calls at all loci (e.g., 10,12 at D3S1358; 14,16 at vWA).",
            "CODIS database: National DNA Index System (NDIS) contains >14 million offender profiles, >1 million forensic profiles.",
            "Forensic profile uploaded to CODIS if: minimum 8 core loci, quality standards met.",
            "Database hit: forensic profile matches convicted offender or another case (cold hit).",
            "Random match probability (RMP): likelihood that random unrelated person has same profile.",
            "Product rule: multiply allele frequencies at each locus across all loci.",
            "Example: RMP = 1 in 1 quadrillion (1 in 10^15) for full 20-locus profile.",
            "Theta correction (coancestry coefficient): accounts for subpopulation structure (relatives more likely to share alleles).",
            "FBI population databases: African American, Caucasian, Hispanic, Asian - used for frequency calculations.",
            "Likelihood ratio: compares probability of evidence if suspect is source vs. random person is source.",
            "Paternity testing: probability of paternity >99.9% if alleged father has matching alleles at all loci.",
            "Mixed DNA profiles: multiple contributors (e.g., rape kit with victim + perpetrator DNA).",
            "Deconvolution: separating mixed profile into individual contributor profiles (complex, probabilistic).",
            "Probabilistic genotyping software (e.g., STRmix, TrueAllele) calculates likelihood ratios for mixtures.",
            "Quality assurance: positive control (known DNA), negative control (no DNA), allelic ladder (size standard).",
            "Contamination prevention: analysts wear gloves, use disposable supplies, work in separate pre-PCR and post-PCR areas.",
            "SWGDAM (Scientific Working Group on DNA Analysis Methods) validation guidelines.",
            "ISO 17025 accreditation required for CODIS-participating laboratories.",
            "Expert testimony: explain RMP, database search procedures, mixture interpretation (if applicable).",
            "Limitations: identical twins have same DNA profile; degraded DNA yields partial profiles (reduced RMP)."
        ],
        key_factors=[
            "Number of STR loci analyzed (20 vs. 13 vs. partial)",
            "Quality of DNA profile (full profile vs. partial, peak heights)",
            "Random match probability (RMP) calculation",
            "Database search result (CODIS hit or no match)",
            "Single-source vs. mixed DNA profile",
            "Contamination controls (negative controls clean)",
            "Degradation or inhibition (affects PCR success)",
            "Chain of custody for DNA evidence"
        ],
        primary_authority=[
            "FBI CODIS and NDIS Fact Sheet (2020) - database statistics and procedures",
            "SWGDAM Interpretation Guidelines for Autosomal STR Typing (2017)",
            "National Research Council: The Evaluation of Forensic DNA Evidence (1996) - foundational report",
            "Butler, J.M.: Forensic DNA Typing (3rd ed, 2015) - authoritative textbook"
        ],
        burden_holder="Prosecution relies on DNA match and RMP; defense challenges contamination, chain of custody, mixture interpretation",
        adversary_position="Defense argues: contamination, improper handling, mixture interpretation errors, database search bias (cold hit), coincidental match",
        counter_arguments=[
            "DNA contamination during collection (analyst DNA transferred to evidence)",
            "Secondary transfer (DNA from handshake transferred to object never touched)",
            "Chain of custody break - evidence integrity compromised",
            "Mixed profile misinterpretation - software assumptions flawed",
            "Database search bias - cold hit is weaker than suspect-driven match (prosecutor's fallacy)",
            "Partial profile - RMP overstated due to missing loci",
            "Degraded DNA - allele dropout (false homozygote)",
            "Coincidental match - RMP assumes random mating, but population substructure increases likelihood",
            "Laboratory error - proficiency test failures, contamination incidents",
            "Identical twin or close relative could be actual source"
        ],
        resolution_strategy="Follow SWGDAM contamination prevention guidelines; document chain of custody; use probabilistic genotyping for mixtures; calculate RMP with theta correction; expert testimony explains statistics and limitations; verify CODIS hit with independent retest",
        entity_scope="Forensic DNA laboratories, law enforcement, violent crime investigations, paternity testing, mass disaster victim identification",
        confidence=0.99,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="SWGDAM guidelines and FBI CODIS standards - scientifically validated, legally accepted for 30+ years"
    ),

    DoctrineBlock(
        topic="Fingerprint Chemistry: Cyanoacrylate Fuming and Ninhydrin Development",
        keywords=["latent fingerprints", "cyanoacrylate", "superglue fuming", "ninhydrin", "amino acids", "ridge detail", "fingerprint development"],
        conclusion_template=[
            "Latent fingerprints are developed using chemical or physical methods depending on substrate and age.",
            "Cyanoacrylate (superglue) fuming polymerizes on lipid and protein residues, producing white polymer ridges.",
            "Ninhydrin reacts with amino acids in fingerprint residue, producing purple Ruhemann's purple product - effective on porous surfaces."
        ],
        reasoning_framework=[
            "Latent fingerprints are invisible deposits of sweat, oils, amino acids, and salts transferred from fingers.",
            "Eccrine sweat: water, amino acids (glycine, serine), salts, urea - originates from sweat glands on ridges.",
            "Sebaceous secretions: lipids, fatty acids, squalene - originate from sebaceous glands (not on fingertips, transferred from face/hair).",
            "Fingerprint development techniques: physical (powder dusting), chemical (cyanoacrylate, ninhydrin), instrumental (laser, ALS).",
            "Cyanoacrylate fuming (superglue fuming): cyanoacrylate ester vaporized, polymerizes on fingerprint residue.",
            "Polymerization initiated by: water, amino acids, proteins in latent print.",
            "White polycyanoacrylate polymer forms along fingerprint ridges - visualized with oblique lighting or fluorescent dye.",
            "Fuming chamber: enclosed space, cyanoacrylate heated to 120-150 degrees F, humidity 80% optimal.",
            "Fuming time: 10-30 minutes depending on chamber size, temperature, humidity.",
            "Post-fuming enhancement: Basic Yellow 40 (BY40) dye, Rhodamine 6G - fluorescent dyes adhere to polymer, viewed with ALS.",
            "Ninhydrin development: reacts with amino acids (glycine, serine, alanine) in fingerprint sweat.",
            "Ruhemann's purple: purple product of ninhydrin-amino acid reaction (absorption max 570 nm).",
            "Ninhydrin solution: 0.5% ninhydrin in acetone or HFE-7100 (environmentally friendly solvent).",
            "Application: dip, spray, or brush ninhydrin onto porous surface (paper, cardboard, unfinished wood).",
            "Development: air dry, then heat (80-100 degrees C) or humidity treatment (80% RH, 60-80 degrees F) for 24-48 hours.",
            "DFO (1,8-diazafluoren-9-one): alternative to ninhydrin, more sensitive, fluorescent product (viewed with ALS).",
            "Sequence of techniques: non-destructive first (visual, oblique lighting, ALS), then cyanoacrylate, then ninhydrin/DFO.",
            "Cyanoacrylate over-fuming: excessive polymer obscures ridge detail - irreversible.",
            "Ninhydrin drawbacks: destroys DNA, toxic fumes (work in fume hood), permanent staining of evidence.",
            "Silver nitrate: older method, reacts with chloride ions in sweat, produces brown silver chloride - less sensitive than ninhydrin.",
            "Physical Developer (PD): iron-based suspension, deposits on lipid residues - useful for wet documents after ninhydrin fails.",
            "Vacuum metal deposition (VMD): gold or zinc evaporated onto fingerprint in vacuum chamber - high sensitivity.",
            "Quality assurance: process known fingerprint controls alongside evidence to verify technique effectiveness.",
            "SWGFAST (Scientific Working Group on Friction Ridge Analysis) guidelines for fingerprint processing.",
            "ACE-V methodology: Analysis, Comparison, Evaluation, Verification - fingerprint examiner protocol.",
            "Reporting: number of latent prints developed, quality (1st, 2nd, 3rd class), suitable for comparison (identifiable ridge detail).",
            "Expert testimony: explain development technique used, quality of developed prints, comparison results (identification, exclusion, inconclusive).",
            "Limitation: chemical development can destroy other evidence (DNA, trace evidence) - prioritize which evidence to pursue first."
        ],
        key_factors=[
            "Substrate type (porous vs. non-porous)",
            "Age of latent print (fresh vs. aged)",
            "Environmental conditions (humidity, temperature)",
            "Development technique sequence (non-destructive first)",
            "Quality of developed print (ridge detail clarity)",
            "Over-development risk (excessive fuming, over-staining)",
            "Preservation of other evidence types (DNA priority)",
            "Analyst training on technique application"
        ],
        primary_authority=[
            "SWGFAST Friction Ridge Examination Methodology for Latent Print Examiners (2012)",
            "NIJ Special Report: Fingerprint Sourcebook (2011) - Chapter 7 on Chemical Development",
            "Champod et al.: Fingerprints and Other Ridge Skin Impressions (2nd ed, 2016)",
            "ASTM E1789-18 Standard Guide for Writing Conclusions in Friction Ridge Examinations"
        ],
        burden_holder="Laboratory processes evidence using appropriate development techniques; examiner identifies or excludes suspect based on ridge detail",
        adversary_position="Defense challenges: improper development (over-fuming, wrong technique), contamination, misidentification, lack of verification",
        counter_arguments=[
            "Over-fuming with cyanoacrylate obscured ridge detail - print quality degraded",
            "Wrong development sequence - destructive technique (ninhydrin) applied before DNA sampling",
            "Contamination during fuming (multiple items in chamber, prints transferred)",
            "Ninhydrin over-development - background staining obscures ridge detail",
            "Latent print too old or degraded - insufficient ridge detail for comparison",
            "Examiner error in comparison (false identification, confirmation bias)",
            "Lack of verification by second examiner (ACE-V protocol violated)",
            "Environmental factors (humidity, heat) caused ridge distortion during development",
            "Substrate interference (patterned background) creates false ridge detail",
            "Insufficient training or competency testing of examiner"
        ],
        resolution_strategy="Follow SWGFAST guidelines for technique sequencing; prioritize DNA vs. fingerprint evidence based on case needs; use appropriate development method for substrate; document fuming parameters; second examiner verification (ACE-V); photograph before and after development; limit over-fuming by monitoring process",
        entity_scope="Forensic laboratories, latent print examiners, crime scene investigators, burglary/theft investigations",
        confidence=0.92,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="SWGFAST guidelines and ACE-V methodology - scientifically accepted for fingerprint development and comparison"
    ),

    DoctrineBlock(
        topic="ISO 17025 Laboratory Accreditation and Quality Management",
        keywords=["ISO 17025", "accreditation", "quality assurance", "proficiency testing", "measurement uncertainty", "validation", "competency testing"],
        conclusion_template=[
            "ISO/IEC 17025 is the international standard for competence of testing and calibration laboratories.",
            "Accreditation requires: validated methods, proficiency testing, measurement uncertainty estimation, competency demonstration, quality control.",
            "Accredited laboratories undergo annual audits and proficiency testing to maintain certification."
        ],
        reasoning_framework=[
            "ISO/IEC 17025:2017 General Requirements for the Competence of Testing and Calibration Laboratories.",
            "Accreditation bodies: ANAB (ANSI National Accreditation Board), A2LA (American Association for Laboratory Accreditation), ASCLD/LAB.",
            "Scope of accreditation: specific test methods and matrices (e.g., drug identification by GC-MS in blood).",
            "Method validation required: accuracy, precision, linearity, LOD, LOQ, specificity, robustness.",
            "Validation protocol: analyze spiked samples at multiple concentrations (n=5 replicates), calculate %CV, %bias.",
            "Accuracy (trueness): percent difference between measured value and true value (bias <15%).",
            "Precision (repeatability): coefficient of variation (%CV) <15% at high concentration, <20% at LOQ.",
            "Linearity: correlation coefficient (r²) >0.99 over working range.",
            "Limit of detection (LOD): concentration at which signal = blank + 3 × SD of blank.",
            "Limit of quantitation (LOQ): concentration at which signal = blank + 10 × SD of blank, lowest calibrator on curve.",
            "Specificity: absence of interference from matrix components or similar compounds.",
            "Robustness: method performance under deliberate variations (temperature, pH, reagent lot).",
            "Measurement uncertainty (MU): quantifies range of doubt around measured value.",
            "MU sources: calibration, standard preparation, instrument variability, analyst variability, sample matrix.",
            "MU calculation: GUM (Guide to Expression of Uncertainty in Measurement) or top-down approach (proficiency testing data).",
            "Expanded uncertainty (U): MU × coverage factor (k=2 for 95% confidence interval).",
            "Reporting: result ± U (e.g., 1.2 ± 0.2 mg/L).",
            "Proficiency testing (PT): external blind samples analyzed 2-4 times per year.",
            "PT providers: CAP (College of American Pathologists), NIST, Collaborative Testing Services.",
            "PT evaluation: z-score = (lab result - consensus mean) / consensus SD; |z| <2 acceptable, |z| >3 unacceptable.",
            "Corrective action required for PT failure: root cause analysis, method review, retraining, follow-up PT.",
            "Internal quality control (IQC): analyze control samples (low, medium, high) with each batch.",
            "IQC acceptance criteria: within ±2 SD of target value (Westgard rules).",
            "Competency assessment: initial demonstration (analyze 5 known samples), annual requalification.",
            "Training records: document training received, competency tests passed, ongoing education.",
            "Equipment qualification: installation qualification (IQ), operational qualification (OQ), performance qualification (PQ).",
            "Calibration: instruments calibrated annually or per manufacturer specifications (traceable to NIST standards).",
            "Preventive maintenance: documented schedule for routine maintenance (e.g., GC-MS source cleaning, LC column replacement).",
            "Document control: SOPs (standard operating procedures) version-controlled, reviewed every 2 years.",
            "Audit: accreditation body conducts on-site audit annually, assesses compliance with ISO 17025.",
            "Nonconformances: corrective action plans required for deficiencies identified during audit.",
            "Surveillance assessment: annual or biennial depending on accreditation body.",
            "Reaccreditation cycle: every 4-5 years, full reassessment."
        ],
        key_factors=[
            "Scope of accreditation (specific tests/matrices)",
            "Method validation documentation (accuracy, precision, etc.)",
            "Proficiency testing performance (z-scores)",
            "Measurement uncertainty calculated and reported",
            "Internal quality control compliance (Westgard rules)",
            "Analyst competency demonstration",
            "Equipment calibration and maintenance records",
            "Audit findings and corrective actions"
        ],
        primary_authority=[
            "ISO/IEC 17025:2017 General Requirements for Competence of Testing Laboratories",
            "EURACHEM/CITAC Guide: Quantifying Uncertainty in Analytical Measurement (2012)",
            "ASCLD/LAB International Supplemental Requirements for Forensic Laboratories (2019)",
            "NIST Technical Note 1297: Guidelines for Evaluating and Expressing Uncertainty"
        ],
        burden_holder="Laboratory must demonstrate compliance with ISO 17025 to obtain and maintain accreditation",
        adversary_position="Defense challenges: accreditation lapses, PT failures, QC out of range, lack of MU reporting, analyst competency gaps",
        counter_arguments=[
            "Proficiency test failure not addressed - lab continued testing without corrective action",
            "Method validation incomplete - LOD and LOQ not determined experimentally",
            "Measurement uncertainty not calculated or reported - violates ISO 17025 requirement",
            "Internal quality control out of range - batch results reported despite QC failure",
            "Analyst competency not demonstrated - no documented training or testing",
            "Equipment not calibrated within required interval - results questionable",
            "Accreditation lapsed - testing performed without valid accreditation",
            "Audit found nonconformances - corrective actions not implemented before sample analysis",
            "SOP not followed - analyst deviated from validated procedure",
            "Chain of custody break - violates ISO 17025 evidence handling requirements"
        ],
        resolution_strategy="Obtain and maintain ISO 17025 accreditation from recognized body (ANAB, A2LA, ASCLD/LAB); pass proficiency tests; calculate and report measurement uncertainty; document all validation, QC, competency, calibration per standard; implement corrective actions for audit findings; expert testimony on accreditation status and compliance",
        entity_scope="Forensic laboratories, toxicology labs, calibration labs, environmental testing labs",
        confidence=0.96,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="ISO/IEC 17025 - internationally recognized standard for laboratory competence, often legally required for accreditation"
    ),

    DoctrineBlock(
        topic="Daubert Standard for Expert Testimony Admissibility",
        keywords=["Daubert", "expert testimony", "scientific reliability", "peer review", "error rate", "general acceptance", "gatekeeping"],
        conclusion_template=[
            "Daubert v. Merrell Dow Pharmaceuticals (1993) established criteria for admissibility of scientific expert testimony in federal court.",
            "Daubert factors: testing, peer review, known error rate, standards, general acceptance.",
            "Judge acts as gatekeeper - determines if methodology is scientifically valid before allowing expert testimony to jury."
        ],
        reasoning_framework=[
            "Daubert v. Merrell Dow Pharmaceuticals, 509 U.S. 579 (1993) - landmark Supreme Court case.",
            "Federal Rules of Evidence 702: expert testimony admissible if: (1) based on sufficient facts/data, (2) product of reliable principles/methods, (3) expert applied principles reliably.",
            "Daubert factors (non-exhaustive list for assessing reliability):",
            "1. Testing: Has the theory/technique been tested? Empirical validation preferred.",
            "2. Peer review and publication: Has the methodology been subjected to peer review and published in scientific journals?",
            "3. Known error rate: What is the known or potential rate of error? Quantified error rates strengthen reliability.",
            "4. Standards controlling operation: Do standards exist for applying the technique (e.g., ASTM, SWGDRUG)?",
            "5. General acceptance: Is the methodology generally accepted in relevant scientific community (Frye standard incorporated)?",
            "Judge's gatekeeping role: determine scientific validity and relevance before evidence reaches jury (pretrial Daubert hearing).",
            "Daubert applies to: all expert testimony (scientific, technical, specialized knowledge) per Kumho Tire v. Carmichael (1999).",
            "Burden of proof: proponent of expert testimony (usually prosecution) must demonstrate reliability by preponderance of evidence.",
            "Flexible analysis: not all factors apply to every case; judge has discretion.",
            "Federal courts: Daubert standard applies; state courts: vary (some Daubert, some Frye, some hybrid).",
            "Frye standard (pre-Daubert): general acceptance in relevant scientific community - more conservative (Frye v. United States, 1923).",
            "Post-Daubert forensic challenges: fingerprint comparison (U.S. v. Llera Plaza, 2002), bite marks (Innocence Project challenges), hair microscopy (FBI admitted flaws 2015).",
            "GC-MS drug identification: passes Daubert - extensively tested, peer-reviewed, known error rates, ASTM standards, general acceptance.",
            "DNA profiling: passes Daubert - validated, peer-reviewed, RMP quantifies reliability, SWGDAM standards, universal acceptance.",
            "Arson investigation: NFPA 921 improved reliability after Daubert scrutiny; old myths (crazed glass, alligatoring) discredited.",
            "Bullet lead analysis: FBI discontinued (2005) after National Academy of Sciences review found lack of scientific foundation.",
            "Bite mark analysis: increasing Daubert exclusions due to: lack of validation studies, high error rates, absence of standards.",
            "National Academy of Sciences (2009): Strengthening Forensic Science - criticized many forensic disciplines for lack of scientific rigor.",
            "PCAST Report (2016): Forensic Science in Criminal Courts - recommended foundational validity and validity as applied.",
            "Foundational validity: underlying scientific principle is sound (e.g., PCR amplifies DNA).",
            "Validity as applied: specific implementation is reliable (e.g., lab's DNA protocol validated, analyst competent).",
            "Defense Daubert challenges: attack methodology, error rates, analyst qualifications, lack of standards, novel techniques.",
            "Prosecution Daubert defense: cite peer-reviewed studies, proficiency test pass rates, accreditation, published standards.",
            "Expert qualifications: education, training, experience, publications, certifications (e.g., board certification).",
            "Cross-examination: Daubert allows vigorous cross-examination of methodology and conclusions even if admitted."
        ],
        key_factors=[
            "Empirical testing of methodology",
            "Peer review and publication in scientific journals",
            "Quantified error rate (if available)",
            "Existence of controlling standards (ASTM, SWGDRUG, etc.)",
            "General acceptance in relevant scientific community",
            "Expert's qualifications and experience",
            "Proper application of methodology in specific case",
            "Relevance to issue in case (FRE 702 requirement)"
        ],
        primary_authority=[
            "Daubert v. Merrell Dow Pharmaceuticals, 509 U.S. 579 (1993) - established admissibility standard",
            "Kumho Tire Co. v. Carmichael, 526 U.S. 137 (1999) - extended Daubert to all expert testimony",
            "Federal Rules of Evidence 702 (amended 2000) - codifies Daubert factors",
            "PCAST Report: Forensic Science in Criminal Courts (2016) - foundational validity framework"
        ],
        burden_holder="Proponent of expert testimony (prosecution) bears burden of proving reliability by preponderance of evidence",
        adversary_position="Defense challenges expert testimony reliability using Daubert factors; seeks pretrial exclusion",
        counter_arguments=[
            "Methodology not empirically tested - no validation studies published",
            "Technique not peer-reviewed - only internal lab studies (not independent)",
            "High or unknown error rate - no proficiency testing data available",
            "No controlling standards - technique is ad hoc, subjective",
            "Lack of general acceptance - novel method not widely adopted by scientific community",
            "Expert unqualified - insufficient training, no relevant publications, failed proficiency tests",
            "Improper application - analyst deviated from validated protocol",
            "Irrelevant to issue - technique does not address question at hand (FRE 702(b))",
            "National Academy of Sciences or PCAST criticized specific forensic discipline (e.g., bite marks)",
            "Better alternative methodology exists but was not used"
        ],
        resolution_strategy="Proponent should: cite peer-reviewed validation studies, present proficiency test data, reference published standards (ASTM, SWGDRUG), demonstrate general acceptance, qualify expert (credentials, experience), show proper application; anticipate defense Daubert motion and prepare rebuttal evidence",
        entity_scope="Federal courts, state courts adopting Daubert, prosecution and defense in criminal cases, civil litigation involving scientific evidence",
        confidence=0.94,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals - Supreme Court precedent governing expert testimony admissibility in federal court"
    ),

    # Additional doctrine blocks for comprehensive coverage
    DoctrineBlock(
        topic="Paint Evidence Analysis and Comparison",
        keywords=["automotive paint", "architectural paint", "layer structure", "microchemical tests", "pyrolysis GC-MS", "FTIR spectroscopy"],
        conclusion_template=[
            "Paint evidence is class evidence - comparison determines if samples could have common origin.",
            "Layer structure (number, sequence, color, thickness) is highly discriminating for automotive paint.",
            "Chemical analysis by FTIR and pyrolysis GC-MS identifies polymer binder and pigment composition."
        ],
        reasoning_framework=[
            "Paint evidence: transfers during hit-and-run, burglary (tool marks with paint), vandalism.",
            "Paint composition: pigments (color, opacity), binder (polymer resin), solvents (evaporate), additives (dryers, stabilizers).",
            "Automotive paint layers: electrocoat primer, primer surfacer, basecoat (color), clearcoat (4+ layers typical).",
            "Architectural paint: usually single layer or 2-3 layers (primer, topcoat).",
            "Physical comparison: stereomicroscope examines color, texture, layer sequence, thickness.",
            "Layer structure match: automotive paint with 6 layers in specific sequence is highly discriminating.",
            "Color comparison: microspectrophotometry measures color across visible spectrum - objective color matching.",
            "FTIR (Fourier-transform infrared spectroscopy): identifies polymer binder (acrylic, alkyd, epoxy, polyurethane).",
            "FTIR sample preparation: cross-section mounted, individual layers analyzed separately.",
            "Pyrolysis GC-MS: paint pyrolyzed at 600-750 degrees C, fragments analyzed by GC-MS - identifies polymer and pigments.",
            "SEM-EDS (scanning electron microscopy with energy-dispersive X-ray): elemental analysis of pigments (Ti for white, Fe for red, Pb for yellow).",
            "Raman spectroscopy: identifies pigments (TiO2, chrome yellow, carbon black) non-destructively.",
            "Microchemical tests: solubility in acetone, toluene, MEK - distinguishes polymer types.",
            "Paint databases: RCMP (Royal Canadian Mounted Police) PDQ (Paint Data Query) - 70,000+ automotive samples.",
            "PDQ search: layer structure, color, chemistry - provides vehicle make/model/year.",
            "Architectural paint databases less developed - manufacturer identification difficult.",
            "Statistical significance: unique layer structure (e.g., 7 layers with specific colors) has low population frequency.",
            "Weathering: UV exposure, oxidation alter paint chemistry - fresh vs. aged paint comparison challenging.",
            "SWGMAT Paint Analysis Guidelines (1999) - standard practices.",
            "Comparison conclusions: indistinguishable, could have common origin, different sources.",
            "Limitation: class evidence only - cannot individualize to single vehicle (millions of cars same make/model/color).",
            "Corroborating evidence: paint evidence combined with vehicle damage, witness statements, etc.",
            "Expert testimony: describe layer structure match, chemical analysis results, statistical rarity of layer sequence.",
            "Daubert considerations: physical/chemical methods well-validated, but statistical population data limited for some paint types.",
            "Quality assurance: analyze known standards, blind samples for competency testing.",
            "ASTM E1610: Standard Guide for Forensic Paint Analysis and Comparison.",
            "Emerging techniques: LA-ICP-MS (laser ablation inductively coupled plasma mass spectrometry) for trace element profiling of paint layers."
        ],
        key_factors=[
            "Number of paint layers and sequence",
            "Color match by microspectrophotometry",
            "Layer thickness measurements",
            "Polymer identification by FTIR",
            "Pigment composition by pyrolysis GC-MS or SEM-EDS",
            "Comparison to PDQ or other paint databases",
            "Degree of weathering or aging",
            "Alternative sources for paint (multiple vehicles with same paint system)"
        ],
        primary_authority=[
            "SWGMAT Forensic Paint Analysis and Comparison Guidelines (1999)",
            "ASTM E1610-18 Standard Guide for Forensic Paint Analysis and Comparison",
            "Caddy et al.: Forensic Examination of Glass and Paint (2001) - foundational text",
            "RCMP PDQ (Paint Data Query) Database"
        ],
        burden_holder="Prosecution demonstrates paint similarity and statistical significance; defense challenges commonality and alternative sources",
        adversary_position="Defense argues: common automotive paint (low probative value), multiple vehicles with same paint, environmental paint contamination, lab error",
        counter_arguments=[
            "Common automotive color (e.g., silver, white) - millions of vehicles with same paint",
            "Generic layer structure (primer + basecoat + clearcoat) - not distinctive",
            "PDQ search yields multiple vehicle makes/models - not narrowed to suspect vehicle",
            "Weathering differences between questioned and known samples - inconsistent aging",
            "Paint from environmental source (parked cars, painted surfaces) not suspect vehicle",
            "Cross-contamination in lab during sample preparation or analysis",
            "Insufficient sample size for complete analysis",
            "Layer thickness measurement variability - overlapping ranges",
            "Alternative explanation: paint from victim's own vehicle transferred during impact",
            "Expert overstates significance - paint is class evidence, cannot prove individual vehicle"
        ],
        resolution_strategy="Comprehensive paint analysis (physical exam, color, FTIR, pyrolysis GC-MS); compare to PDQ database; document layer structure uniqueness; corroborate with other evidence (vehicle damage, location); acknowledge class evidence limitations in testimony",
        entity_scope="Forensic laboratories, hit-and-run investigations, burglary tool mark analysis",
        confidence=0.87,
        confidence_stratification="DISCLOSURE",
        controlling_precedent="SWGMAT and ASTM E1610 - scientifically accepted methods, but statistical weight varies by paint type complexity"
    ),

    DoctrineBlock(
        topic="Glass Refractive Index Determination and Comparison",
        keywords=["glass evidence", "refractive index", "density", "elemental analysis", "tempered glass", "float glass", "glass fragments"],
        conclusion_template=[
            "Glass evidence comparison relies on refractive index (RI) measurement - highly discriminating physical property.",
            "Refractive index measured by: immersion method with temperature variation or automated GRIM (Glass Refractive Index Measurement) instrument.",
            "Glass RI match (within ±0.0002) combined with density and elemental composition provides strong association."
        ],
        reasoning_framework=[
            "Glass evidence: burglary (broken windows), hit-and-run (headlight fragments), assault (broken bottles).",
            "Refractive index (RI): ratio of speed of light in vacuum to speed in material - characteristic physical property.",
            "RI depends on: glass composition (SiO2, Na2O, CaO percentages), annealing temperature, presence of additives.",
            "Float glass (windows, windshields): RI typically 1.518-1.520.",
            "Container glass (bottles, jars): RI range 1.510-1.525.",
            "Tempered glass (side windows, safety glass): RI similar to float glass but fragments into small cubes.",
            "Laminated glass (windshields): two glass layers with plastic interlayer - fragments adhere to plastic.",
            "Immersion method: glass fragment placed in oil, temperature varied until glass disappears (RI match point).",
            "Becke line: bright halo at glass-oil interface - moves toward higher RI material when temperature changed.",
            "GRIM (Glass Refractive Index Measurement): automated instrument measures RI to ±0.00002.",
            "GRIM method: laser beam refracted through glass, angle measured, RI calculated.",
            "Density determination: sink-float method using density gradient column or pycnometry.",
            "Density range: float glass 2.50-2.52 g/cm³, container glass 2.40-2.60 g/cm³.",
            "Elemental analysis: ICP-MS, SEM-EDS, or LA-ICP-MS detects trace elements (Fe, Mg, Al, Ba).",
            "Trace element profile: discriminates between glass sources from different manufacturers.",
            "ASTM E2927: Standard Test Method for Determination of Trace Elements in Soda-Lime Glass by LA-ICP-MS.",
            "Comparison protocol: measure RI, density, elemental composition of questioned and known glass.",
            "Match criteria: RI within ±0.0002, density within ±0.001 g/cm³, elemental profiles consistent.",
            "Statistical significance: RI match probability depends on glass type - float glass is more homogeneous (less discriminating) than container glass.",
            "SWGMAT Glass Fracture Guidelines (2005) - standard practices.",
            "Fracture pattern analysis: radial cracks (emanate from impact), concentric cracks (circular around impact).",
            "Sequence of impacts: radial cracks from first impact terminate at cracks from second impact.",
            "Direction of force: concentric fracture surface has rib marks perpendicular to side of force application.",
            "Transfer evidence: glass fragments on suspect clothing or tools link to crime scene.",
            "Persistence: glass sheds from clothing within hours - prompt collection critical.",
            "Quality assurance: analyze glass standards with known RI, participate in proficiency testing.",
            "Interpretation limitations: glass is class evidence - cannot individualize to single pane (manufacturing batch shares RI).",
            "Expert testimony: explain RI match significance, fracture pattern analysis (if applicable), acknowledge class evidence limitations.",
            "Daubert factors: RI measurement scientifically validated, ASTM standards exist, error rates low (<0.00002 RI uncertainty)."
        ],
        key_factors=[
            "Refractive index match (within ±0.0002)",
            "Density match (within ±0.001 g/cm³)",
            "Elemental composition similarity",
            "Glass type (float, container, tempered)",
            "Fracture pattern analysis (if applicable)",
            "Transfer and persistence timeline",
            "Number of matching fragments recovered",
            "Alternative sources for glass (other windows, bottles)"
        ],
        primary_authority=[
            "SWGMAT Forensic Glass Analysis Guidelines (2005)",
            "ASTM E2927-16 Standard Test Method for Determination of Trace Elements in Soda-Lime Glass by LA-ICP-MS",
            "Koons and Buscaglia: The Forensic Significance of Glass Composition and Refractive Index (2002)",
            "Caddy et al.: Forensic Examination of Glass and Paint (2001)"
        ],
        burden_holder="Prosecution demonstrates glass similarity and transfer from crime scene to suspect; defense challenges match significance and alternative sources",
        adversary_position="Defense argues: common glass type (low probative value), environmental glass contamination, RI measurement error, alternative glass sources",
        counter_arguments=[
            "Float glass is homogeneous - millions of windows have same RI (low probative value)",
            "Environmental glass contamination (glass fragments on clothing from unrelated source)",
            "RI measurement uncertainty - values overlap within instrument error",
            "Insufficient sample size for density and elemental analysis",
            "Glass from suspect's own vehicle or residence, not crime scene",
            "Cross-contamination during collection or packaging (multiple glass items in same container)",
            "Tempered glass fragments lack diagnostic features - cannot determine source window",
            "Alternative explanation: glass transferred during legitimate activity (e.g., prior visit to scene)",
            "Elemental analysis not performed - incomplete comparison",
            "Expert overstates significance - glass is class evidence, cannot prove single source pane"
        ],
        resolution_strategy="Comprehensive glass analysis (RI, density, elemental composition); use GRIM for precise RI measurement; compare to glass database (if available); corroborate with other evidence (fracture pattern, location of fragments on suspect); acknowledge class evidence limitations; expert testimony on statistical rarity of RI match",
        entity_scope="Forensic laboratories, burglary investigations, hit-and-run cases, assault with glass weapon",
        confidence=0.89,
        confidence_stratification="DISCLOSURE",
        controlling_precedent="SWGMAT and ASTM standards - scientifically validated methods, but glass is class evidence with varying discriminating power"
    ),

    DoctrineBlock(
        topic="Questioned Document Examination and Ink Analysis",
        keywords=["handwriting comparison", "ink dating", "TLC", "Raman spectroscopy", "indented writing", "ESDA", "paper composition"],
        conclusion_template=[
            "Questioned document examination includes: handwriting comparison, ink analysis, paper composition, indented writing recovery.",
            "Ink analysis by TLC (thin-layer chromatography) or Raman spectroscopy distinguishes ink formulations.",
            "ESDA (Electrostatic Detection Apparatus) recovers indented writing from pages beneath written page - non-destructive technique."
        ],
        reasoning_framework=[
            "Questioned document examination: fraud, forgery, altered documents, anonymous letters, ransom notes.",
            "Handwriting comparison: analyze stroke characteristics, letter formations, spacing, slant, pressure patterns.",
            "Known standards: request writings (suspect asked to write specific text) or collected writings (pre-existing documents).",
            "ACE-V methodology (Analysis, Comparison, Evaluation, Verification) applied to handwriting comparison.",
            "Handwriting identification: individualization possible due to unique motor patterns, but subjective - Daubert challenges increasing.",
            "ASTM E2290: Standard Guide for Examination of Handwritten Items.",
            "Ink analysis: distinguish between inks, determine if multiple inks used, attempt dating.",
            "TLC (thin-layer chromatography): ink extracted, separated on silica gel plate, dye components visualized.",
            "Raman spectroscopy: non-destructive technique identifies ink pigments and dyes by molecular vibration.",
            "FTIR spectroscopy: identifies ink binder (resin) and additives.",
            "LA-ICP-MS: elemental analysis of ink trace elements (Ti, Al, Cu) - discriminates formulations.",
            "Ink library: databases from ink manufacturers (e.g., U.S. Secret Service International Ink Library) - 9,500+ inks.",
            "Ink dating: relative (which entry written first) vs. absolute (calendar date ink applied).",
            "Relative dating: ink layer stratigraphy (crossings of ink strokes), solvent extraction tests.",
            "Absolute dating: volatile solvent loss over time - controversial, high error rates, limited applicability.",
            "Paper analysis: watermark examination, fiber composition (cotton vs. wood pulp), optical brighteners.",
            "Indented writing: impressions on pages beneath written page - recovered by ESDA or oblique lighting.",
            "ESDA (Electrostatic Detection Apparatus): charges document, toner applied, indented writing visualized.",
            "ESDA non-destructive - does not damage document or interfere with other examinations.",
            "Alterations and erasures: chemical erasures detected by UV/IR imaging, mechanical erasures by microscopy.",
            "Obliterations: ink or correction fluid covering original text - IR or hyperspectral imaging reveals underlying writing.",
            "Typewriter/printer identification: defects in typeface or print head link document to specific machine.",
            "Laser printer tracking dots: yellow dots encoding printer serial number and timestamp (privacy concern but forensically useful).",
            "Photocopier artifacts: trash marks, roller defects - link copy to specific machine.",
            "Digital forensics integration: metadata in electronic documents (author, creation date, modification history).",
            "Quality assurance: blind proficiency tests, inter-examiner comparison (verification), ASTM standards.",
            "Handwriting comparison limitations: subjective, lack of objective criteria, high error rates in some studies (NAS 2009 report).",
            "SWGDOC (Scientific Working Group for Forensic Document Examination) disbanded 2016 but guidelines still cited.",
            "Expert testimony: explain methodology, comparison results, limitations (especially for handwriting identification).",
            "Daubert challenges: handwriting comparison faces scrutiny due to subjective nature, lack of validation studies, variable error rates."
        ],
        key_factors=[
            "Handwriting characteristics match between questioned and known",
            "Ink composition by TLC, Raman, or LA-ICP-MS",
            "Ink library database search results",
            "Indented writing content and significance",
            "Paper composition and watermark match",
            "Alterations or erasures detected",
            "Typewriter/printer defects linking to specific machine",
            "Expert's training and proficiency test performance"
        ],
        primary_authority=[
            "ASTM E2290-19 Standard Guide for Examination of Handwritten Items",
            "ASTM E1422-14 Standard Guide for Test Methods for Forensic Writing Ink Comparison",
            "SWGDOC Guidelines (archived) - still cited as best practices",
            "Morris: Forensic Handwriting Identification (2000) - foundational text"
        ],
        burden_holder="Prosecution demonstrates document authenticity/forgery; defense challenges expert methodology and error rates",
        adversary_position="Defense challenges: subjective handwriting comparison, lack of validation, ink dating unreliability, ESDA contamination",
        counter_arguments=[
            "Handwriting comparison is subjective - no objective criteria, high inter-examiner variability",
            "Lack of validation studies for handwriting identification - NAS 2009 report criticized discipline",
            "Error rates unknown or high - proficiency test failures documented",
            "Disguised writing or imitation - difficult to detect reliably",
            "Ink dating by solvent loss unreliable - high error rates, environmental factors affect evaporation",
            "Ink library inconclusive - multiple manufacturers use same formulation",
            "ESDA contamination - indented writing from unrelated document",
            "Alterations misinterpreted - normal wear or damage mistaken for intentional alteration",
            "Printer tracking dots - multiple users of same printer (e.g., office printer)",
            "Expert lacks sufficient training or proficiency testing - unqualified opinion"
        ],
        resolution_strategy="Use ACE-V with independent verification for handwriting; combine multiple ink analysis techniques (TLC + Raman + LA-ICP-MS); ESDA on questioned and control pages; acknowledge limitations (especially handwriting and ink dating); expert testimony with conservative conclusions; Daubert proffer addressing methodology validation",
        entity_scope="Forensic document examiners, fraud investigations, forgery cases, ransom notes, altered contracts",
        confidence=0.78,
        confidence_stratification="HIGH_RISK",
        controlling_precedent="ASTM standards - accepted methodology, but handwriting comparison faces increasing Daubert challenges due to subjectivity and validation concerns"
    ),

    DoctrineBlock(
        topic="Explosives Residue Analysis and Identification",
        keywords=["explosives", "TNT", "PETN", "RDX", "nitroglycerin", "IMS", "GC-MS", "ion chromatography", "post-blast residue"],
        conclusion_template=[
            "Explosives residue analysis identifies explosive compounds in post-blast debris or on suspect's hands/clothing.",
            "Detection methods: ion mobility spectrometry (IMS) for screening, GC-MS or LC-MS for confirmation.",
            "Common explosives: TNT (trinitrotoluene), RDX (cyclotrimethylenetrinitramine), PETN (pentaerythritol tetranitrate), nitroglycerin, TATP (triacetone triperoxide)."
        ],
        reasoning_framework=[
            "Explosives: materials that rapidly decompose producing gas, heat, and pressure (detonation or deflagration).",
            "High explosives: detonation (supersonic reaction) - TNT, RDX, PETN, C-4, dynamite, Semtex.",
            "Low explosives: deflagration (subsonic burning) - black powder, smokeless powder, flash powder.",
            "Post-blast residue: undetonated explosive particles, decomposition products, device components.",
            "Collection: debris vacuumed or swabbed, hands/clothing swabbed within 4 hours.",
            "Screening: ion mobility spectrometry (IMS) - portable field instrument, detects ppb-ppm levels.",
            "IMS mechanism: explosives ionized, ions separated by drift time in electric field, detected.",
            "IMS detects: TNT, RDX, PETN, nitroglycerin, TATP - false positives from perfumes, hand lotions.",
            "Confirmatory testing: GC-MS, LC-MS, or ion chromatography (IC).",
            "GC-MS: separates volatile explosives (TNT, nitroglycerin, EGDN), mass spectrum confirms identity.",
            "LC-MS: non-volatile or thermally labile explosives (RDX, PETN, TATP), electrospray ionization.",
            "Ion chromatography: inorganic explosives (ammonium nitrate, chlorate, perchlorate) - anionic separation.",
            "FTIR spectroscopy: identifies explosive functional groups (nitro, nitrate ester).",
            "Raman spectroscopy: non-destructive explosive identification, useful for intact samples.",
            "X-ray diffraction: crystalline explosive identification (e.g., military-grade RDX vs. commercial).",
            "Taggants: Identitag microparticles in commercial explosives (required by law) - color-coded layers identify manufacturer and lot.",
            "ASTM E1588: Standard Practice for Gunshot Residue Analysis (analogous methodology for explosives residue).",
            "SWGEX (Scientific Working Group for Explosives Analysis) disbanded but guidelines archived.",
            "Common improvised explosives: ANFO (ammonium nitrate + fuel oil), TATP (acetone + peroxide), urea nitrate.",
            "TATP detection challenging: unstable, decomposes rapidly, low vapor pressure - requires specialized techniques.",
            "Contamination prevention: separate tools for each sample, clean work surfaces, blanks analyzed.",
            "Quality control: analyze explosive standards (TNT, RDX, PETN) with each batch, proficiency testing.",
            "False positives: nitroglycerin in heart medication, nitrate in fertilizer, cosmetics/lotions trigger IMS.",
            "False negatives: explosive completely consumed in blast, weathering degrades residue, water washout.",
            "Interpretation: presence of explosive residue does not prove device origin - could be environmental contamination (mining, military, agricultural).",
            "Expert testimony: explain explosive identified, significance, limitations (cannot determine quantity, timing, intent).",
            "Daubert factors: GC-MS and LC-MS well-validated, ASTM standards exist, error rates low for confirmatory methods.",
            "Safety protocols: explosives residue handled in ventilated hood, small quantities only, no open flames."
        ],
        key_factors=[
            "Type of explosive identified (TNT, RDX, PETN, etc.)",
            "Concentration of explosive residue",
            "Location of residue (post-blast debris vs. suspect's hands)",
            "Time between blast and collection (<4 hours optimal for hands)",
            "Confirmatory test results (GC-MS, LC-MS)",
            "Presence of taggants (manufacturer/lot identification)",
            "Alternative sources for explosive residue (occupational, environmental)",
            "Quality control and blank sample results"
        ],
        primary_authority=[
            "ASTM E1412-19 Standard Practice for Separation of Ignitable Liquid Residues (analogous explosives method)",
            "SWGEX Recommended Guidelines (archived) - still cited as best practices",
            "Yinon and Zitrin: Modern Methods and Applications in Analysis of Explosives (1996)",
            "Beveridge: Forensic Investigation of Explosions (2nd ed, 2012)"
        ],
        burden_holder="Prosecution proves explosive presence and links to defendant; defense challenges contamination, alternative sources, timing",
        adversary_position="Defense argues: environmental contamination (mining, fireworks, agriculture), occupational exposure, IMS false positive, lack of confirmatory test",
        counter_arguments=[
            "IMS false positive from perfume, hand lotion, fertilizer, or heart medication (nitroglycerin)",
            "Environmental contamination from mining operations, military base, agricultural fertilizer",
            "Occupational exposure (demolition worker, fireworks technician, military personnel)",
            "Delayed collection (>4 hours) - explosive residue shed or degraded",
            "Hand washing between incident and collection removed residue",
            "Confirmatory test not performed - reliance on IMS screening alone insufficient",
            "Post-blast residue from commercial blasting at construction site (legitimate source)",
            "Contamination during collection or analysis (dirty swabs, lab environment)",
            "Explosive quantity too small to determine intent (trace contamination vs. device construction)",
            "Lack of taggant identification - cannot link to specific manufacturer or lot"
        ],
        resolution_strategy="Use IMS for screening, confirm all positives by GC-MS or LC-MS; document time between incident and collection; analyze blanks and controls; search for taggants; consider alternative sources (occupational, environmental); expert testimony acknowledging limitations (cannot determine quantity, timing, or intent without other evidence)",
        entity_scope="Forensic laboratories, bomb squads, ATF investigations, terrorism cases, illegal fireworks",
        confidence=0.91,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="ASTM standards and SWGEX guidelines - scientifically validated methods, but interpretation requires context (occupational/environmental sources)"
    ),

    # Add more doctrines to reach 25+ total
    DoctrineBlock(
        topic="Forensic Quality Assurance and Proficiency Testing Programs",
        keywords=["proficiency testing", "CAP", "quality control", "z-score", "blind testing", "competency assessment", "Westgard rules"],
        conclusion_template=[
            "Proficiency testing (PT) is external blind sample analysis to verify analyst competency and method performance.",
            "PT providers: CAP, NIST, Collaborative Testing Services - samples analyzed 2-4 times per year.",
            "PT failure requires root cause analysis, corrective action, and follow-up testing before resuming casework."
        ],
        reasoning_framework=[
            "Proficiency testing: external quality assessment using blind samples of known composition.",
            "Purpose: verify analyst competency, detect systematic errors, validate method performance.",
            "CAP (College of American Pathologists): largest PT provider for forensic toxicology, chemistry.",
            "NIST (National Institute of Standards and Technology): PT for DNA, trace evidence, ballistics.",
            "Collaborative Testing Services (CTS): comprehensive PT for forensic disciplines.",
            "PT frequency: ISO 17025 requires minimum annual PT, most labs participate 2-4 times per year.",
            "Blind testing: analyst unaware sample is PT (treated as routine casework).",
            "PT evaluation: laboratory result compared to consensus value (mean of all participants).",
            "Z-score: (lab result - consensus mean) / consensus standard deviation.",
            "Acceptable performance: |z| <2 (within 2 SD of consensus).",
            "Questionable performance: 2< |z| <3 (marginal, investigate but may continue testing).",
            "Unacceptable performance: |z| >3 (PT failure, requires corrective action).",
            "False positive: laboratory reports substance present when actually absent (critical error).",
            "False negative: laboratory reports substance absent when actually present (critical error).",
            "Corrective action for PT failure: root cause analysis, method review, retraining, repeat PT.",
            "Root cause examples: calibration drift, contamination, analyst error, instrument malfunction.",
            "Suspension of testing: casework halted until corrective action completed and verified by follow-up PT.",
            "Internal quality control (IQC): daily/batch analysis of control samples (low, medium, high concentration).",
            "Westgard rules: IQC acceptance criteria (e.g., 1-2s: reject if >2 SD from target; 2-2s: reject if consecutive controls >2 SD same direction).",
            "Levey-Jennings charts: plot IQC results over time, detect trends or shifts.",
            "Reagent lot verification: new reagent lots tested against old lot before implementation.",
            "Equipment maintenance: preventive maintenance schedule, documentation of repairs and recalibration.",
            "Method validation: initial and ongoing verification of accuracy, precision, linearity, LOD, LOQ.",
            "Competency assessment: initial demonstration (5+ known samples), annual requalification.",
            "Testimony review: senior analysts review reports and testimony of junior analysts (technical review).",
            "External audits: accreditation bodies (ASCLD/LAB, ANAB, A2LA) assess compliance with ISO 17025.",
            "Nonconformances: deficiencies identified during audit, require corrective action plan.",
            "Measurement uncertainty: quantify and report uncertainty per ISO 17025 requirement.",
            "Traceability: calibration traceable to NIST standards or international SI units.",
            "Document control: SOPs version-controlled, reviewed every 2 years, training documented.",
            "Emerging practices: blind quality control samples (mimics PT but internally generated)."
        ],
        key_factors=[
            "PT participation frequency (2-4x per year)",
            "PT performance (z-scores, false positive/negative rate)",
            "Corrective action for PT failures (documented, verified)",
            "IQC compliance (Westgard rules, Levey-Jennings charts)",
            "Competency testing results (initial and ongoing)",
            "External audit findings (nonconformances, corrective actions)",
            "Method validation documentation",
            "Measurement uncertainty reported"
        ],
        primary_authority=[
            "ISO/IEC 17025:2017 Section 7.7 - Ensuring Validity of Results",
            "CAP Laboratory Accreditation Program Forensic Toxicology Checklist",
            "ASCLD/LAB International Supplemental Requirements (2019)",
            "NIST Handbook 150 - NVLAP Procedures and General Requirements"
        ],
        burden_holder="Laboratory must demonstrate PT participation and acceptable performance to maintain accreditation",
        adversary_position="Defense challenges: PT failures, lack of corrective action, IQC out of range, analyst competency gaps",
        counter_arguments=[
            "PT failure not addressed - casework continued without corrective action",
            "Multiple PT failures in same discipline - systemic problem",
            "IQC out of range - batch results reported despite QC failure (violation of protocol)",
            "Corrective action incomplete - root cause not identified or resolved",
            "Analyst lacked competency testing before performing casework",
            "PT not blind - analyst aware it was proficiency test (compromises validity)",
            "External audit found nonconformances - corrective actions not implemented before sample analysis",
            "Measurement uncertainty not calculated or reported (ISO 17025 violation)",
            "Method validation insufficient - accuracy, precision, or LOD not determined",
            "Equipment not calibrated within required interval - results unreliable"
        ],
        resolution_strategy="Participate in accredited PT programs (CAP, NIST, CTS); implement robust IQC (Westgard rules); document all corrective actions for PT failures; maintain competency testing records; undergo regular external audits; calculate and report measurement uncertainty; ensure method validation complete per ISO 17025",
        entity_scope="Forensic laboratories, toxicology labs, accreditation bodies, regulatory oversight",
        confidence=0.97,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="ISO/IEC 17025 - international standard mandating PT and QC for accredited laboratories"
    )
]

# === GLOBAL STATE ===
queries_processed = 0
total_latency_ms = 0.0
cache_hits = 0
cache_misses = 0
start_time = datetime.now()


# === CORE ENGINE FUNCTIONS ===

def semantic_normalize(text: str) -> str:
    """Normalize forensic chemistry terminology."""
    text_lower = text.lower()
    replacements = {
        "gcms": "GC-MS", "gc/ms": "GC-MS", "gas chromatography mass spectrometry": "GC-MS",
        "lcms": "LC-MS", "lc/ms": "LC-MS", "liquid chromatography mass spectrometry": "LC-MS",
        "sem-eds": "SEM-EDS", "sem/eds": "SEM-EDS",
        "ftir": "FTIR", "ft-ir": "FTIR", "fourier transform infrared": "FTIR",
        "cyanoacrylate": "cyanoacrylate fuming", "superglue": "cyanoacrylate fuming",
        "str": "STR analysis", "short tandem repeat": "STR analysis",
        "codis": "CODIS database", "dna database": "CODIS database",
        "gunshot residue": "GSR", "primer residue": "GSR",
        "ignitable liquid": "ignitable liquid residue", "accelerant": "ignitable liquid residue",
        "immunoassay": "immunoassay screening", "elisa": "immunoassay screening"
    }
    for old, new in replacements.items():
        text_lower = text_lower.replace(old, new)
    return text_lower


def search_doctrine_cache(question: str) -> List[DoctrineBlock]:
    """Search doctrine cache for matching blocks."""
    global cache_hits, cache_misses
    question_norm = semantic_normalize(question)
    matches = []

    for block in DOCTRINE_BLOCKS:
        keyword_match = any(kw.lower() in question_norm for kw in block.keywords)
        topic_match = any(word in question_norm for word in block.topic.lower().split())

        if keyword_match or topic_match:
            matches.append(block)

    if matches:
        cache_hits += 1
    else:
        cache_misses += 1

    return matches


def apply_authority_hardening(doctrines: List[DoctrineBlock]) -> List[Tuple[DoctrineBlock, float]]:
    """Apply authority hierarchy weighting."""
    authority_weights = {
        "peer-reviewed": 1.0,
        "ASTM": 0.95,
        "SWGDRUG": 0.95,
        "SWGMAT": 0.95,
        "SWGTOX": 0.95,
        "FBI": 0.90,
        "NIST": 0.85,
        "textbook": 0.70
    }

    weighted = []
    for doctrine in doctrines:
        max_weight = 0.70
        for auth in doctrine.primary_authority:
            for key, weight in authority_weights.items():
                if key.lower() in auth.lower():
                    max_weight = max(max_weight, weight)
        weighted.append((doctrine, max_weight * doctrine.confidence))

    return sorted(weighted, key=lambda x: x[1], reverse=True)


def three_layer_response(question: str, mode: str) -> Dict[str, Any]:
    """TIE-20 Component: Three-layer response architecture."""
    start = datetime.now()

    # Layer 1: Doctrine Cache (0-200ms target)
    cache_results = search_doctrine_cache(question)

    if cache_results:
        weighted = apply_authority_hardening(cache_results)
        top_doctrines = [d for d, w in weighted[:3]]

        if mode == "FAST":
            answer = "\n\n".join([
                f"**{d.topic}**: " + " ".join(d.conclusion_template[:2])
                for d in top_doctrines[:2]
            ])
        elif mode == "DEFENSE":
            answer = ""
            for d in top_doctrines[:2]:
                answer += f"\n\n## {d.topic}\n\n"
                answer += "\n".join(d.conclusion_template) + "\n\n"
                answer += "**Key Factors**: " + "; ".join(d.key_factors[:5]) + "\n\n"
                answer += "**Primary Authority**: " + "; ".join(d.primary_authority[:3])
        else:  # MEMO
            answer = ""
            for d in top_doctrines:
                answer += f"\n\n## {d.topic}\n\n"
                answer += "**Conclusions**:\n" + "\n".join([f"- {c}" for c in d.conclusion_template]) + "\n\n"
                answer += "**Reasoning Framework**:\n" + "\n".join([f"{i+1}. {r}" for i, r in enumerate(d.reasoning_framework[:15])]) + "\n\n"
                answer += "**Key Factors**: " + "; ".join(d.key_factors) + "\n\n"
                answer += "**Primary Authority**: " + "\n".join([f"- {a}" for a in d.primary_authority]) + "\n\n"
                answer += f"**Confidence**: {d.confidence} ({d.confidence_stratification})\n\n"
                answer += f"**Controlling Precedent**: {d.controlling_precedent}"

        latency = (datetime.now() - start).total_seconds() * 1000

        return {
            "answer": answer,
            "doctrines_triggered": [d.topic for d in top_doctrines],
            "authorities": list(set([a for d in top_doctrines for a in d.primary_authority])),
            "confidence": weighted[0][1],
            "stratification": top_doctrines[0].confidence_stratification,
            "layer": "CACHE",
            "latency_ms": latency
        }

    # Layer 2: Vector search (not implemented - would query external vector DB)
    # Layer 3: Deep analysis (not implemented - would use LLM synthesis)

    return {
        "answer": "No matching doctrine blocks found in cache. Vector search and deep analysis layers not yet implemented.",
        "doctrines_triggered": [],
        "authorities": [],
        "confidence": 0.0,
        "stratification": "DISCLOSURE",
        "layer": "NONE",
        "latency_ms": (datetime.now() - start).total_seconds() * 1000
    }


def calculate_determinism_hash(question: str, answer: str, mode: str) -> str:
    """TIE-20 Component: SHA-256 determinism hash."""
    content = f"{question}|{answer}|{mode}|{VERSION}"
    return hashlib.sha256(content.encode()).hexdigest()


def log_audit_trail(query_id: str, question: str, answer: str, mode: str, telemetry: Dict[str, Any]):
    """TIE-20 Component: Audit trail logging."""
    audit_entry = {
        "query_id": query_id,
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "mode": mode,
        "answer_preview": answer[:200],
        "telemetry": telemetry
    }

    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(audit_entry) + "\n")


def log_telemetry(query_id: str, latency_ms: float, layer: str, doctrines_triggered: int):
    """TIE-20 Component: Telemetry logging."""
    telemetry_entry = {
        "query_id": query_id,
        "timestamp": datetime.now().isoformat(),
        "latency_ms": latency_ms,
        "layer": layer,
        "doctrines_triggered": doctrines_triggered,
        "cache_hit": layer == "CACHE"
    }

    with open(TELEMETRY_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(telemetry_entry) + "\n")


# === FASTAPI APPLICATION ===

APP = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    description="TIE-grade forensic chemistry intelligence engine with 25+ doctrine blocks"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@APP.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest) -> QueryResponse:
    """Main query endpoint with TIE-20 architecture."""
    global queries_processed, total_latency_ms

    query_id = str(uuid4())
    logger.info(f"Query {query_id}: {request.question[:100]}")

    result = three_layer_response(request.question, request.mode)

    determinism_hash = calculate_determinism_hash(
        request.question,
        result["answer"],
        request.mode
    )

    telemetry = {
        "latency_ms": result["latency_ms"],
        "layer": result["layer"],
        "doctrines_triggered": len(result["doctrines_triggered"]),
        "cache_hit_rate": cache_hits / (cache_hits + cache_misses) if (cache_hits + cache_misses) > 0 else 0.0
    }

    log_audit_trail(query_id, request.question, result["answer"], request.mode, telemetry)
    log_telemetry(query_id, result["latency_ms"], result["layer"], len(result["doctrines_triggered"]))

    queries_processed += 1
    total_latency_ms += result["latency_ms"]

    return QueryResponse(
        answer=result["answer"],
        mode=request.mode,
        confidence=result["confidence"],
        stratification=result["stratification"],
        doctrines_triggered=result["doctrines_triggered"],
        authorities_cited=result["authorities"],
        determinism_hash=determinism_hash,
        timestamp=datetime.now().isoformat(),
        telemetry=telemetry
    )


@APP.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """TIE-20 Component: Health endpoint."""
    uptime = (datetime.now() - start_time).total_seconds()
    avg_latency = total_latency_ms / queries_processed if queries_processed > 0 else 0.0
    hit_rate = cache_hits / (cache_hits + cache_misses) if (cache_hits + cache_misses) > 0 else 0.0

    return HealthResponse(
        status="operational",
        engine_id=ENGINE_ID,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_BLOCKS),
        queries_processed=queries_processed,
        avg_latency_ms=round(avg_latency, 2),
        cache_hit_rate=round(hit_rate, 3),
        uptime_seconds=round(uptime, 1)
    )


@APP.get("/doctrines")
async def list_doctrines():
    """List all doctrine blocks."""
    return {
        "total": len(DOCTRINE_BLOCKS),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence,
                "stratification": d.confidence_stratification
            }
            for d in DOCTRINE_BLOCKS
        ]
    }


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_BLOCKS)} doctrine blocks")
    uvicorn.run(APP, host="0.0.0.0", port=PORT)
