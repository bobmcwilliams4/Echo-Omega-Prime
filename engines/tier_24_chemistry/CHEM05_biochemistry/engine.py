import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

"""
CHEM05 Biochemistry Intelligence Engine
Comprehensive biochemistry knowledge covering protein structure, enzyme kinetics,
metabolic pathways, molecular biology, signal transduction, and clinical applications.
Port 9055.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from loguru import logger
import hashlib
import json

# Configure logger
logger.add(
    Path(__file__).parent / "logs" / "chem05_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)

APP = FastAPI(title="CHEM05 Biochemistry Engine", version="1.0.0")

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    resolution_strategy: str


# Doctrine Cache - 25+ biochemistry doctrine blocks
DOCTRINE_CACHE = [
    DoctrineBlock(
        topic="protein_primary_structure",
        keywords=["amino acid", "sequence", "peptide bond", "primary structure", "polypeptide"],
        conclusion_template=[
            "Primary structure is the linear amino acid sequence",
            "Peptide bonds link amino acids through condensation reactions",
            "Sequence determines all higher-order structures and function"
        ],
        reasoning_framework="""
        Primary structure foundation:
        1. 20 standard amino acids with unique R groups
        2. Peptide bond formation: CO-NH linkage with water loss
        3. N-terminus (free amino) to C-terminus (free carboxyl) directionality
        4. Sequence encoded by mRNA codon sequence
        5. Post-translational modifications can occur after synthesis
        6. Single amino acid changes (mutations) can drastically alter function
        7. Sanger sequencing and mass spectrometry reveal primary structure
        """,
        key_factors=[
            "Amino acid composition and order",
            "Peptide bond planarity restricts rotation",
            "Disulfide bridges between cysteine residues",
            "Post-translational modifications (phosphorylation, glycosylation)",
            "Genetic mutations affecting sequence"
        ],
        primary_authority=[
            "Biochemistry textbooks (Lehninger, Voet & Voet)",
            "Protein Data Bank (PDB) structural data",
            "UniProt protein sequence databases"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Analyze amino acid sequence data, identify functional motifs, predict impact of mutations"
    ),

    DoctrineBlock(
        topic="protein_secondary_structure",
        keywords=["alpha helix", "beta sheet", "turn", "loop", "hydrogen bond"],
        conclusion_template=[
            "Secondary structures arise from hydrogen bonding patterns in backbone",
            "Alpha helices and beta sheets are most common regular structures",
            "Ramachandran plots define allowed phi/psi angles"
        ],
        reasoning_framework="""
        Secondary structure principles:
        1. Alpha helix: right-handed coil, 3.6 residues/turn, i to i+4 H-bonds
        2. Beta sheet: extended strands, parallel or antiparallel arrangement
        3. Beta turns: reverse direction, often contain proline or glycine
        4. Stabilized by backbone C=O···H-N hydrogen bonds
        5. Phi (φ) and psi (ψ) dihedral angles define backbone geometry
        6. Ramachandran plot shows allowed conformations
        7. Proline disrupts helices, glycine allows tight turns
        """,
        key_factors=[
            "Backbone hydrogen bonding patterns",
            "Amino acid propensities (helix formers vs breakers)",
            "Ramachandran allowed regions",
            "Proline and glycine special roles",
            "Helix stability factors (charge interactions, helix dipole)"
        ],
        primary_authority=[
            "Pauling and Corey helix models",
            "Ramachandran conformational analysis",
            "Chou-Fasman and GOR prediction algorithms"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Predict secondary structure from sequence, validate with circular dichroism or NMR"
    ),

    DoctrineBlock(
        topic="protein_tertiary_structure",
        keywords=["folding", "hydrophobic effect", "tertiary structure", "domain", "active site"],
        conclusion_template=[
            "Tertiary structure is the 3D arrangement of a single polypeptide",
            "Hydrophobic effect drives core formation",
            "Multiple weak interactions stabilize folded state"
        ],
        reasoning_framework="""
        Tertiary structure determinants:
        1. Hydrophobic amino acids buried in core, hydrophilic on surface
        2. Disulfide bonds (cysteine-cysteine) provide covalent crosslinks
        3. Hydrogen bonds, van der Waals, electrostatic interactions
        4. Entropy-enthalpy balance drives folding thermodynamics
        5. Anfinsen principle: sequence determines structure
        6. Molecular chaperones assist proper folding in vivo
        7. Active sites formed by convergence of distant sequence regions
        8. Domains are independently folding structural units
        """,
        key_factors=[
            "Hydrophobic effect (primary driving force)",
            "Disulfide bond formation",
            "Electrostatic interactions (salt bridges)",
            "Hydrogen bonding networks",
            "Conformational entropy loss upon folding"
        ],
        primary_authority=[
            "Anfinsen's folding experiments",
            "Levinthal paradox and folding pathways",
            "Protein crystallography and NMR structure determination"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Use X-ray crystallography or cryo-EM for structure, predict with AlphaFold, validate function"
    ),

    DoctrineBlock(
        topic="protein_quaternary_structure",
        keywords=["subunit", "oligomer", "quaternary structure", "hemoglobin", "cooperativity"],
        conclusion_template=[
            "Quaternary structure involves multiple polypeptide subunits",
            "Subunit interfaces stabilized by non-covalent interactions",
            "Cooperativity and allostery common in multi-subunit proteins"
        ],
        reasoning_framework="""
        Quaternary structure organization:
        1. Multiple polypeptide chains assemble into functional complex
        2. Homooligomers (identical subunits) vs heterooligomers (different subunits)
        3. Subunit interfaces: hydrophobic patches, complementary surfaces
        4. Hemoglobin: classic example with α2β2 tetramer
        5. Positive cooperativity: binding enhances subsequent binding
        6. Allosteric regulation: binding at one site affects distant sites
        7. Symmetry common (C2, D2, icosahedral for viruses)
        """,
        key_factors=[
            "Number and type of subunits",
            "Interface area and binding energy",
            "Cooperativity mechanisms (MWC vs KNF models)",
            "Allosteric effector binding sites",
            "Subunit stoichiometry"
        ],
        primary_authority=[
            "Perutz hemoglobin structure studies",
            "Monod-Wyman-Changeux (MWC) allosteric model",
            "Koshland-Némethy-Filmer (KNF) induced fit model"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Determine oligomeric state by size exclusion, analytical ultracentrifugation, native MS"
    ),

    DoctrineBlock(
        topic="enzyme_kinetics_michaelis_menten",
        keywords=["Km", "Vmax", "Michaelis-Menten", "enzyme kinetics", "turnover number"],
        conclusion_template=[
            "Michaelis-Menten equation describes enzyme velocity vs substrate concentration",
            "Km reflects substrate affinity, Vmax reflects catalytic capacity",
            "kcat/Km defines catalytic efficiency"
        ],
        reasoning_framework="""
        Michaelis-Menten kinetics:
        1. E + S ⇌ ES → E + P (rapid equilibrium or steady-state assumption)
        2. v = (Vmax[S])/(Km + [S])
        3. Km = (k-1 + k2)/k1 (substrate concentration at half Vmax)
        4. Vmax = kcat[E]total (maximum velocity)
        5. kcat = turnover number (catalytic events per enzyme per time)
        6. kcat/Km = specificity constant (catalytic efficiency)
        7. Diffusion limit: kcat/Km ≈ 10^8 - 10^9 M^-1 s^-1
        8. Lineweaver-Burk plot: 1/v vs 1/[S] linearizes data
        """,
        key_factors=[
            "Km value (substrate affinity indicator)",
            "Vmax and enzyme concentration",
            "kcat (turnover number)",
            "kcat/Km (catalytic efficiency)",
            "Substrate concentration range relative to Km"
        ],
        primary_authority=[
            "Michaelis and Menten original 1913 paper",
            "Briggs-Haldane steady-state treatment",
            "Lineweaver-Burk, Eadie-Hofstee linearizations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Measure initial velocities at varied [S], fit to Michaelis-Menten, determine Km and Vmax"
    ),

    DoctrineBlock(
        topic="enzyme_inhibition",
        keywords=["competitive", "noncompetitive", "uncompetitive", "inhibitor", "Ki"],
        conclusion_template=[
            "Competitive inhibitors increase apparent Km, no effect on Vmax",
            "Noncompetitive inhibitors decrease Vmax, no effect on Km",
            "Uncompetitive inhibitors decrease both Km and Vmax"
        ],
        reasoning_framework="""
        Enzyme inhibition mechanisms:
        1. Competitive: I binds active site, competes with S
           - Apparent Km increases (Km(1 + [I]/Ki))
           - Vmax unchanged (can overcome with high [S])
           - Lineweaver-Burk: lines intersect on y-axis
        2. Noncompetitive: I binds enzyme or ES complex equally
           - Vmax decreases (Vmax/(1 + [I]/Ki))
           - Km unchanged
           - Lineweaver-Burk: lines intersect on x-axis
        3. Uncompetitive: I binds only ES complex
           - Both Km and Vmax decrease proportionally
           - Lineweaver-Burk: parallel lines
        4. Mixed inhibition: I binds E or ES with different affinities
        """,
        key_factors=[
            "Inhibitor type (competitive, noncompetitive, uncompetitive)",
            "Ki value (inhibitor dissociation constant)",
            "Effect on Km and Vmax",
            "Reversibility (reversible vs irreversible)",
            "Lineweaver-Burk plot pattern"
        ],
        primary_authority=[
            "Enzyme kinetics textbooks (Segel, Cornish-Bowden)",
            "Dixon plot for Ki determination",
            "Lineweaver-Burk diagnostic patterns"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Measure kinetics with/without inhibitor, plot Lineweaver-Burk, determine inhibition type and Ki"
    ),

    DoctrineBlock(
        topic="allosteric_regulation",
        keywords=["allosteric", "cooperativity", "Hill coefficient", "sigmoidal", "effector"],
        conclusion_template=[
            "Allosteric enzymes show sigmoidal kinetics, not hyperbolic",
            "Positive cooperativity (Hill coefficient > 1) amplifies response",
            "Effectors bind regulatory sites distinct from active site"
        ],
        reasoning_framework="""
        Allosteric regulation principles:
        1. Sigmoidal velocity vs [S] curve indicates cooperativity
        2. Hill equation: v = (Vmax[S]^n)/(K0.5^n + [S]^n)
        3. Hill coefficient (n): n=1 (no cooperativity), n>1 (positive), n<1 (negative)
        4. MWC model: T (tense, low affinity) ⇌ R (relaxed, high affinity) states
        5. Positive effectors shift T→R equilibrium, negative effectors shift R→T
        6. Hemoglobin: classic example (n ≈ 2.8 for O2 binding)
        7. Feedback inhibition: end product inhibits first committed step
        """,
        key_factors=[
            "Hill coefficient magnitude",
            "K0.5 (substrate concentration at half Vmax)",
            "Positive vs negative effectors",
            "T and R state populations",
            "Physiological significance of cooperativity"
        ],
        primary_authority=[
            "MWC (Monod-Wyman-Changeux) concerted model",
            "KNF (Koshland-Némethy-Filmer) sequential model",
            "Hill plot and coefficient determination"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Plot Hill plot (log[v/(Vmax-v)] vs log[S]), determine n, identify effectors"
    ),

    DoctrineBlock(
        topic="glycolysis",
        keywords=["glucose", "pyruvate", "ATP", "glycolysis", "phosphorylation"],
        conclusion_template=[
            "Glycolysis converts glucose to 2 pyruvate, net 2 ATP, 2 NADH",
            "Three irreversible steps: hexokinase, PFK-1, pyruvate kinase",
            "PFK-1 is primary regulatory enzyme"
        ],
        reasoning_framework="""
        Glycolysis pathway analysis:
        1. Investment phase: glucose → fructose-1,6-bisphosphate (consumes 2 ATP)
        2. Payoff phase: F-1,6-BP → 2 pyruvate (produces 4 ATP, 2 NADH)
        3. Net: glucose + 2 NAD+ + 2 ADP + 2 Pi → 2 pyruvate + 2 NADH + 2 ATP
        4. Key regulated steps:
           - Hexokinase/glucokinase (glucose → G6P)
           - PFK-1 (F6P → F-1,6-BP, rate-limiting, allosteric)
           - Pyruvate kinase (PEP → pyruvate)
        5. PFK-1 regulation: inhibited by ATP, citrate; activated by AMP, F-2,6-BP
        6. Anaerobic: pyruvate → lactate (regenerates NAD+)
        7. Aerobic: pyruvate → acetyl-CoA → TCA cycle
        """,
        key_factors=[
            "Net ATP yield (2 per glucose)",
            "NADH production (2 per glucose)",
            "PFK-1 as committed step",
            "Allosteric regulation by energy charge",
            "Substrate-level phosphorylation"
        ],
        primary_authority=[
            "Embden-Meyerhof-Parnas pathway",
            "Biochemistry textbooks (Berg, Tymoczko, Stryer)",
            "KEGG pathway maps"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Trace pathway steps, calculate ATP/NADH yields, identify regulatory points"
    ),

    DoctrineBlock(
        topic="tca_cycle",
        keywords=["citric acid cycle", "Krebs cycle", "acetyl-CoA", "oxaloacetate", "NADH"],
        conclusion_template=[
            "TCA cycle oxidizes acetyl-CoA to 2 CO2, producing 3 NADH, 1 FADH2, 1 GTP",
            "Oxaloacetate regenerated each cycle",
            "Central hub for catabolism and anabolism"
        ],
        reasoning_framework="""
        TCA cycle operation:
        1. Acetyl-CoA + oxaloacetate → citrate (citrate synthase, irreversible)
        2. Citrate → isocitrate → α-ketoglutarate → succinyl-CoA → succinate → fumarate → malate → oxaloacetate
        3. Per acetyl-CoA: 3 NADH, 1 FADH2, 1 GTP, 2 CO2
        4. Regulated steps:
           - Citrate synthase (inhibited by ATP, NADH, succinyl-CoA)
           - Isocitrate dehydrogenase (activated by ADP, Ca2+; inhibited by NADH, ATP)
           - α-ketoglutarate dehydrogenase (inhibited by succinyl-CoA, NADH)
        5. Amphibolic: both catabolic (energy) and anabolic (biosynthetic precursors)
        6. Anaplerotic reactions replenish intermediates (e.g., pyruvate carboxylase)
        """,
        key_factors=[
            "NADH and FADH2 production for ETC",
            "CO2 release points (decarboxylation steps)",
            "Substrate-level phosphorylation (succinyl-CoA → succinate)",
            "Allosteric regulation by energy state",
            "Biosynthetic precursor roles"
        ],
        primary_authority=[
            "Hans Krebs original work",
            "Metabolic pathway databases (KEGG, BioCyc)",
            "Biochemistry textbooks"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Follow carbon atoms through cycle, sum energy equivalents, identify regulatory control points"
    ),

    DoctrineBlock(
        topic="oxidative_phosphorylation",
        keywords=["electron transport chain", "ATP synthase", "chemiosmotic", "proton gradient"],
        conclusion_template=[
            "ETC generates proton gradient across inner mitochondrial membrane",
            "ATP synthase uses gradient to synthesize ATP",
            "Approximately 2.5 ATP per NADH, 1.5 ATP per FADH2"
        ],
        reasoning_framework="""
        Oxidative phosphorylation mechanism:
        1. Complex I: NADH → NAD+, pumps 4 H+
        2. Complex II: FADH2 → FAD, no proton pumping
        3. Complex III: cytochrome bc1, pumps 4 H+
        4. Complex IV: cytochrome oxidase, pumps 2 H+, O2 → H2O
        5. Total: 10 H+ per NADH, 6 H+ per FADH2
        6. ATP synthase: ~3-4 H+ per ATP (ratio debated)
        7. P/O ratio: ~2.5 ATP/NADH, ~1.5 ATP/FADH2
        8. Uncouplers (DNP) dissipate gradient without ATP synthesis
        9. Inhibitors: rotenone (I), antimycin (III), cyanide (IV), oligomycin (synthase)
        """,
        key_factors=[
            "Proton-motive force (ΔΨ + ΔpH)",
            "ETC complex stoichiometry",
            "P/O ratios (ATP per reducing equivalent)",
            "Coupling efficiency",
            "Inhibitor and uncoupler effects"
        ],
        primary_authority=[
            "Peter Mitchell's chemiosmotic theory",
            "Walker's ATP synthase structure (Nobel Prize)",
            "Experimental P/O ratio determinations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Calculate total ATP from glucose oxidation, measure oxygen consumption, determine P/O ratios"
    ),

    DoctrineBlock(
        topic="gluconeogenesis",
        keywords=["glucose synthesis", "pyruvate", "gluconeogenesis", "bypass", "liver"],
        conclusion_template=[
            "Gluconeogenesis synthesizes glucose from non-carbohydrate precursors",
            "Four bypass reactions circumvent irreversible glycolysis steps",
            "Energetically expensive: 6 ATP equivalents per glucose"
        ],
        reasoning_framework="""
        Gluconeogenesis pathway:
        1. Precursors: lactate, amino acids, glycerol
        2. Bypass 1: pyruvate → PEP (pyruvate carboxylase + PEPCK)
        3. Bypass 2: F-1,6-BP → F6P (fructose-1,6-bisphosphatase)
        4. Bypass 3: G6P → glucose (glucose-6-phosphatase, liver only)
        5. Reciprocal regulation with glycolysis:
           - F-2,6-BP inhibits FBPase-1, activates PFK-1
           - Acetyl-CoA activates pyruvate carboxylase
           - High ATP/AMP favors gluconeogenesis
        6. Cost: 2 pyruvate → glucose requires 4 ATP, 2 GTP, 2 NADH
        7. Cori cycle: muscle lactate → liver glucose → muscle
        """,
        key_factors=[
            "Bypass enzyme locations",
            "Energy cost (6 ATP equivalents)",
            "Reciprocal regulation with glycolysis",
            "Hormonal control (glucagon stimulates, insulin inhibits)",
            "Substrate sources"
        ],
        primary_authority=[
            "Biochemistry textbooks",
            "Metabolic pathway databases",
            "Hormonal regulation literature"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Identify bypass steps, calculate energy cost, analyze reciprocal regulation with glycolysis"
    ),

    DoctrineBlock(
        topic="fatty_acid_oxidation",
        keywords=["beta-oxidation", "fatty acid", "acetyl-CoA", "FADH2", "NADH"],
        conclusion_template=[
            "Beta-oxidation cleaves 2-carbon units as acetyl-CoA",
            "Each cycle produces 1 FADH2, 1 NADH, 1 acetyl-CoA",
            "Palmitoyl-CoA (C16) yields 8 acetyl-CoA, 7 FADH2, 7 NADH"
        ],
        reasoning_framework="""
        Beta-oxidation process:
        1. Activation: fatty acid + CoA + ATP → acyl-CoA (cytosol)
        2. Carnitine shuttle transports acyl-CoA into mitochondria
        3. Spiral pathway (each cycle):
           - Acyl-CoA dehydrogenase: FAD → FADH2
           - Hydration
           - 3-hydroxyacyl-CoA dehydrogenase: NAD+ → NADH
           - Thiolase cleavage: releases acetyl-CoA, shortened acyl-CoA
        4. For palmitoyl-CoA (C16): 7 cycles → 8 acetyl-CoA
        5. ATP yield: 8 acetyl-CoA × 10 + 7 FADH2 × 1.5 + 7 NADH × 2.5 - 2 = 106 ATP
        6. Regulation: inhibited by malonyl-CoA (first step of FA synthesis)
        """,
        key_factors=[
            "Cycle count (n/2 - 1 for n-carbon FA)",
            "Products per cycle (acetyl-CoA, FADH2, NADH)",
            "Carnitine shuttle role",
            "Total ATP yield calculation",
            "Malonyl-CoA inhibition"
        ],
        primary_authority=[
            "Knoop's beta-oxidation theory",
            "Biochemistry textbooks",
            "Metabolic flux studies"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Count cycles, sum products, calculate total ATP, consider activation cost"
    ),

    DoctrineBlock(
        topic="fatty_acid_synthesis",
        keywords=["malonyl-CoA", "fatty acid synthase", "palmitate", "NADPH", "acetyl-CoA carboxylase"],
        conclusion_template=[
            "Fatty acid synthesis uses acetyl-CoA and malonyl-CoA building blocks",
            "FAS complex performs iterative condensation cycles",
            "Palmitate (C16) synthesis requires 8 acetyl-CoA, 14 NADPH, 7 ATP"
        ],
        reasoning_framework="""
        Fatty acid synthesis pathway:
        1. Acetyl-CoA carboxylase: acetyl-CoA + CO2 + ATP → malonyl-CoA (committed step)
        2. Fatty acid synthase (FAS) multi-enzyme complex:
           - Condensation: acetyl-ACP + malonyl-ACP → acetoacetyl-ACP + CO2
           - Reduction: NADPH → NADP+
           - Dehydration
           - Reduction: NADPH → NADP+
           - Cycle repeats 7 times to build palmitate (C16)
        3. 8 acetyl-CoA + 7 ATP + 14 NADPH → palmitate + 7 ADP + 14 NADP+ + 7 CoA
        4. Regulation:
           - ACC activated by citrate, inhibited by palmitoyl-CoA, AMP
           - Hormonal: insulin activates, glucagon/epinephrine inhibit
        5. NADPH sources: pentose phosphate pathway, malic enzyme
        """,
        key_factors=[
            "Acetyl-CoA carboxylase as rate-limiting step",
            "FAS cycle iterations",
            "NADPH requirement (14 per palmitate)",
            "Citrate shuttle from mitochondria",
            "Reciprocal regulation with beta-oxidation"
        ],
        primary_authority=[
            "Wakil's fatty acid synthase studies",
            "Biochemistry textbooks",
            "Metabolic regulation literature"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Count condensation cycles, calculate NADPH and ATP costs, identify regulatory mechanisms"
    ),

    DoctrineBlock(
        topic="amino_acid_metabolism",
        keywords=["transamination", "deamination", "urea cycle", "nitrogen", "glutamate"],
        conclusion_template=[
            "Transamination transfers amino groups between amino acids and α-keto acids",
            "Oxidative deamination converts glutamate to α-ketoglutarate, releasing NH4+",
            "Urea cycle converts toxic ammonia to urea for excretion"
        ],
        reasoning_framework="""
        Amino acid catabolism:
        1. Transamination: amino acid + α-ketoglutarate ⇌ α-keto acid + glutamate
           - PLP (vitamin B6) cofactor
           - Aminotransferases (ALT, AST) central to AA metabolism
        2. Oxidative deamination: glutamate + NAD+ → α-ketoglutarate + NH4+ + NADH
           - Glutamate dehydrogenase in mitochondria
        3. Urea cycle (liver):
           - NH4+ + CO2 + 2 ATP → carbamoyl phosphate (CPS1)
           - Carbamoyl-P + ornithine → citrulline
           - Citrulline + aspartate → argininosuccinate → fumarate + arginine
           - Arginine → urea + ornithine (regenerated)
        4. Carbon skeletons enter TCA cycle or gluconeogenesis
        5. Essential amino acids must be obtained from diet
        """,
        key_factors=[
            "PLP-dependent transamination",
            "Glutamate as nitrogen collector",
            "Urea cycle ATP cost (4 per urea)",
            "Essential vs non-essential amino acids",
            "Tissue-specific metabolism (liver, muscle, brain)"
        ],
        primary_authority=[
            "Krebs and Henseleit urea cycle",
            "Amino acid metabolism reviews",
            "Clinical biochemistry references"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Trace nitrogen flow, identify transamination and deamination reactions, calculate urea cycle cost"
    ),

    DoctrineBlock(
        topic="purine_metabolism",
        keywords=["purine", "IMP", "AMP", "GMP", "salvage pathway", "PRPP"],
        conclusion_template=[
            "De novo purine synthesis builds IMP on ribose-5-phosphate scaffold",
            "IMP converted to AMP or GMP",
            "Salvage pathways recycle free bases (HGPRT, APRT)"
        ],
        reasoning_framework="""
        Purine nucleotide metabolism:
        1. De novo synthesis:
           - PRPP (5-phosphoribosyl-1-pyrophosphate) starting point
           - 10-step pathway builds IMP (inosine monophosphate)
           - IMP → AMP (adenylosuccinate synthetase + lyase)
           - IMP → GMP (IMP dehydrogenase + GMP synthetase)
        2. Regulation:
           - PRPP amidotransferase (committed step) inhibited by AMP, GMP
           - Feedback inhibition maintains balance
        3. Salvage pathways:
           - HGPRT: hypoxanthine/guanine + PRPP → IMP/GMP
           - APRT: adenine + PRPP → AMP
           - Lesch-Nyhan syndrome: HGPRT deficiency
        4. Degradation: purines → uric acid (humans lack uricase)
        5. Gout: uric acid accumulation and crystal deposition
        """,
        key_factors=[
            "PRPP availability",
            "Feedback inhibition by AMP/GMP",
            "Salvage pathway efficiency",
            "Uric acid as end product in humans",
            "Clinical disorders (Lesch-Nyhan, gout)"
        ],
        primary_authority=[
            "Buchanan's purine biosynthesis studies",
            "Biochemistry textbooks",
            "Clinical genetics references"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Map de novo and salvage pathways, identify regulatory points, relate to clinical conditions"
    ),

    DoctrineBlock(
        topic="pyrimidine_metabolism",
        keywords=["pyrimidine", "UMP", "CTP", "orotate", "carbamoyl phosphate"],
        conclusion_template=[
            "Pyrimidine ring assembled first, then attached to ribose",
            "UMP is precursor to CTP and TMP",
            "Orotic aciduria results from defective UMP synthase"
        ],
        reasoning_framework="""
        Pyrimidine nucleotide metabolism:
        1. De novo synthesis:
           - Carbamoyl phosphate synthetase II (cytosolic, glutamine-dependent)
           - Carbamoyl-P + aspartate → carbamoyl aspartate
           - Ring closure → dihydroorotate → orotate
           - Orotate + PRPP → orotidine-5'-P → UMP (UMP synthase)
        2. UMP → UDP → UTP → CTP (CTP synthetase)
        3. dUMP → dTMP (thymidylate synthase, THF-dependent)
        4. Regulation:
           - CPS-II inhibited by UTP, activated by ATP, PRPP
           - Aspartate transcarbamoylase feedback inhibition
        5. Degradation: pyrimidines → β-alanine, β-aminoisobutyrate (not toxic)
        6. Clinical: orotic aciduria (UMP synthase deficiency)
        """,
        key_factors=[
            "Ring synthesized before ribose attachment",
            "CPS-II as regulatory enzyme",
            "Thymidylate synthase as chemotherapy target",
            "Salvage pathways less prominent than purines",
            "Non-toxic degradation products"
        ],
        primary_authority=[
            "Jones and Lipmann pyrimidine synthesis",
            "Biochemistry textbooks",
            "Clinical case studies"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Outline synthesis pathway, identify committed steps, connect to clinical relevance"
    ),

    DoctrineBlock(
        topic="dna_replication",
        keywords=["DNA polymerase", "replication fork", "Okazaki fragment", "primase", "helicase"],
        conclusion_template=[
            "DNA replication is semiconservative, bidirectional from origins",
            "Leading strand continuous, lagging strand discontinuous (Okazaki fragments)",
            "Multiple polymerases and accessory proteins ensure fidelity"
        ],
        reasoning_framework="""
        DNA replication mechanism:
        1. Initiation: origin recognition, helicase unwinds DNA
        2. Primase synthesizes RNA primers
        3. DNA polymerase III (prokaryotes) or δ/ε (eukaryotes):
           - Leading strand: continuous 5'→3' synthesis
           - Lagging strand: discontinuous Okazaki fragments (1-2 kb eukaryotes, ~1000 nt prokaryotes)
        4. DNA polymerase I (prokaryotes) or δ (eukaryotes) removes primers, fills gaps
        5. DNA ligase seals nicks
        6. Proofreading: 3'→5' exonuclease activity (error rate ~10^-10)
        7. Processivity: sliding clamp (β-clamp prokaryotes, PCNA eukaryotes)
        8. Telomerase extends telomeres in eukaryotes
        """,
        key_factors=[
            "Semiconservative replication",
            "Bidirectional from origins",
            "Leading vs lagging strand synthesis",
            "Primer requirement (RNA)",
            "Proofreading and fidelity mechanisms"
        ],
        primary_authority=[
            "Meselson-Stahl semiconservative replication proof",
            "Kornberg DNA polymerase studies",
            "Okazaki fragment discovery"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Describe fork dynamics, identify enzyme roles, calculate error rates with/without proofreading"
    ),

    DoctrineBlock(
        topic="dna_repair",
        keywords=["mismatch repair", "nucleotide excision", "base excision", "repair", "mutation"],
        conclusion_template=[
            "Multiple repair pathways correct different DNA lesions",
            "Mismatch repair fixes replication errors",
            "Excision repair removes bulky adducts and damaged bases"
        ],
        reasoning_framework="""
        DNA repair mechanisms:
        1. Mismatch repair (MMR):
           - MutS recognizes mismatch, MutL recruits MutH
           - Hemimethylated DNA identifies parental strand
           - Excision and resynthesis of daughter strand
           - Defects cause Lynch syndrome (colon cancer)
        2. Nucleotide excision repair (NER):
           - Removes bulky lesions (UV dimers, chemical adducts)
           - Transcription-coupled NER repairs expressed genes faster
           - Xeroderma pigmentosum: NER deficiency
        3. Base excision repair (BER):
           - DNA glycosylase removes damaged base → AP site
           - AP endonuclease, polymerase, ligase complete repair
        4. Direct reversal: photolyase (UV dimer reversal), MGMT (alkyl transfer)
        5. Double-strand break repair: HR (homologous recombination), NHEJ (non-homologous end joining)
        """,
        key_factors=[
            "Lesion type determines repair pathway",
            "Strand discrimination in MMR",
            "Transcription-coupled vs global NER",
            "Clinical syndromes from repair defects",
            "Cancer predisposition from repair deficiency"
        ],
        primary_authority=[
            "Modrich mismatch repair studies",
            "Sancar NER mechanism",
            "Lindahl BER discovery"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Classify lesion, select appropriate pathway, assess clinical implications of defects"
    ),

    DoctrineBlock(
        topic="transcription",
        keywords=["RNA polymerase", "promoter", "transcription factor", "TATA box", "enhancer"],
        conclusion_template=[
            "RNA polymerase synthesizes RNA from DNA template",
            "Promoters and enhancers regulate transcription initiation",
            "Eukaryotic transcription requires assembly of preinitiation complex"
        ],
        reasoning_framework="""
        Transcription process:
        1. Prokaryotes:
           - RNA polymerase holoenzyme (core + σ factor)
           - σ factor recognizes -10 and -35 boxes
           - Rho-dependent or intrinsic termination
        2. Eukaryotes (RNA Pol II for mRNA):
           - TFIID (TBP binds TATA box) nucleates preinitiation complex
           - TFIIB, TFIIF, TFIIE, TFIIH assemble
           - TFIIH has helicase and kinase (CTD phosphorylation)
           - Mediator complex links transcription factors to Pol II
        3. Elongation: Pol II processivity, CTD phosphorylation pattern changes
        4. Termination: cleavage and polyadenylation signals
        5. RNA Pol I (rRNA), Pol III (tRNA, 5S rRNA) have distinct systems
        """,
        key_factors=[
            "Core promoter elements (TATA, Inr, DPE)",
            "Transcription factor binding sites",
            "Mediator complex role",
            "CTD phosphorylation code",
            "Enhancers and long-range regulation"
        ],
        primary_authority=[
            "Kornberg RNA polymerase structure",
            "Roeder eukaryotic transcription factor identification",
            "ENCODE project regulatory element mapping"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Map promoter architecture, identify transcription factors, analyze regulatory mechanisms"
    ),

    DoctrineBlock(
        topic="rna_processing",
        keywords=["splicing", "5' cap", "polyadenylation", "intron", "exon"],
        conclusion_template=[
            "Eukaryotic pre-mRNA undergoes capping, splicing, and polyadenylation",
            "Spliceosome removes introns, joins exons",
            "Alternative splicing generates protein diversity from single genes"
        ],
        reasoning_framework="""
        RNA processing steps:
        1. 5' capping:
           - 7-methylguanosine cap added co-transcriptionally
           - Protects from degradation, enhances translation
        2. Splicing:
           - Spliceosome (snRNPs U1, U2, U4, U5, U6) removes introns
           - Consensus sequences: 5' GU donor, 3' AG acceptor, branch point A
           - Two transesterification reactions
           - Alternative splicing: exon skipping, intron retention, alternative 5'/3' sites
        3. 3' polyadenylation:
           - AAUAAA signal, cleavage 10-30 nt downstream
           - Poly(A) polymerase adds ~200 A residues
        4. RNA editing: A→I (ADAR) or C→U (APOBEC) deamination
        5. Self-splicing introns: Group I (guanosine cofactor), Group II (intron catalytic)
        """,
        key_factors=[
            "Spliceosome assembly and catalysis",
            "Splice site recognition sequences",
            "Alternative splicing regulation",
            "SR proteins and hnRNPs",
            "Coupling to transcription and export"
        ],
        primary_authority=[
            "Sharp and Roberts split gene discovery",
            "Steitz spliceosome studies",
            "Alternative splicing databases (ASD, ASTD)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Identify splice junctions, predict alternative isoforms, assess regulatory factors"
    ),

    DoctrineBlock(
        topic="translation",
        keywords=["ribosome", "tRNA", "codon", "initiation", "elongation"],
        conclusion_template=[
            "Ribosomes decode mRNA codons into polypeptide sequence",
            "tRNAs bring amino acids, match anticodon to codon",
            "Initiation, elongation, termination phases controlled by protein factors"
        ],
        reasoning_framework="""
        Translation mechanism:
        1. Initiation:
           - Prokaryotes: Shine-Dalgarno sequence, fMet-tRNA, 30S → 70S
           - Eukaryotes: 5' cap recognition, scanning to AUG, Met-tRNA, 40S → 80S
           - Initiation factors (IF/eIF) required
        2. Elongation:
           - EF-Tu (prokaryotes) or eEF1A (eukaryotes) delivers aminoacyl-tRNA to A site
           - Peptidyl transferase catalyzes peptide bond (23S rRNA catalytic)
           - Translocation: EF-G/eEF2 moves mRNA and tRNAs
           - Energy: 2 GTP per amino acid
        3. Termination:
           - Stop codons (UAA, UAG, UGA) recognized by release factors
           - Peptide released, ribosome dissociates
        4. Fidelity: aminoacyl-tRNA synthetases, proofreading, error rate ~10^-4
        """,
        key_factors=[
            "Ribosome structure (30S+50S or 40S+60S)",
            "Genetic code and wobble pairing",
            "Aminoacyl-tRNA synthetase specificity",
            "Energy cost (4 ATP equivalents per peptide bond)",
            "Polysome formation on mRNA"
        ],
        primary_authority=[
            "Ramakrishnan, Steitz, Yonath ribosome structures",
            "Nirenberg and Khorana genetic code elucidation",
            "Crick wobble hypothesis"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Trace ribosome cycle, calculate energy cost, analyze codon usage and fidelity"
    ),

    DoctrineBlock(
        topic="signal_transduction_gpcr",
        keywords=["GPCR", "G protein", "cAMP", "second messenger", "adenylyl cyclase"],
        conclusion_template=[
            "GPCRs transduce extracellular signals via heterotrimeric G proteins",
            "Activated Gα or Gβγ modulate effector enzymes or channels",
            "Second messengers (cAMP, IP3, DAG) amplify signals"
        ],
        reasoning_framework="""
        GPCR signaling pathway:
        1. Ligand binding induces conformational change in 7-TM receptor
        2. GPCR acts as GEF: Gα exchanges GDP for GTP
        3. Gα-GTP and Gβγ dissociate, activate effectors:
           - Gαs activates adenylyl cyclase → cAMP → PKA
           - Gαi inhibits adenylyl cyclase
           - Gαq activates phospholipase C → IP3 (Ca2+ release) + DAG (PKC activation)
        4. GTPase activity of Gα terminates signal (aided by RGS proteins)
        5. β-arrestin recruitment desensitizes receptor, promotes endocytosis
        6. Amplification: one receptor activates many G proteins, each Gα activates many effectors
        """,
        key_factors=[
            "G protein subtypes (s, i, q, 12/13)",
            "Second messenger systems",
            "Signal amplification cascades",
            "Desensitization and downregulation",
            "Spatiotemporal organization"
        ],
        primary_authority=[
            "Rodbell and Gilman G protein discovery",
            "Lefkowitz GPCR regulation studies",
            "Kobilka GPCR structure determination"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Identify receptor-G protein-effector pathway, calculate amplification, assess desensitization"
    ),

    DoctrineBlock(
        topic="signal_transduction_rtk",
        keywords=["receptor tyrosine kinase", "autophosphorylation", "SH2 domain", "MAPK", "Ras"],
        conclusion_template=[
            "RTKs dimerize and autophosphorylate upon ligand binding",
            "Phosphotyrosines recruit SH2/PTB domain proteins",
            "Ras-MAPK cascade propagates mitogenic signals"
        ],
        reasoning_framework="""
        RTK signaling pathway:
        1. Ligand (growth factor) binds extracellular domain
        2. Receptor dimerization, trans-autophosphorylation of tyrosines
        3. Phosphotyrosines recognized by SH2 or PTB domains:
           - Grb2-SOS → Ras activation (GEF activity)
           - PI3K → PIP3 → Akt/PKB pathway
           - PLCγ → IP3/DAG pathway
           - STATs → direct transcription activation
        4. Ras-MAPK cascade:
           - Ras-GTP activates Raf (MAPKKK)
           - Raf phosphorylates MEK (MAPKK)
           - MEK phosphorylates ERK (MAPK)
           - ERK enters nucleus, phosphorylates transcription factors
        5. Negative regulation: phosphatases, Ras-GAP, ubiquitin-proteasome
        """,
        key_factors=[
            "Ligand-induced dimerization",
            "Autophosphorylation sites and docking proteins",
            "Ras activation/inactivation cycle",
            "MAPK cascade amplification",
            "Crosstalk with other pathways"
        ],
        primary_authority=[
            "Ullrich and Schlessinger RTK studies",
            "Hunter tyrosine kinase discovery",
            "Weinberg Ras oncogene characterization"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Map ligand-receptor-adapter-effector chain, identify phosphorylation sites, analyze pathway outputs"
    ),

    DoctrineBlock(
        topic="membrane_transport",
        keywords=["ion channel", "pump", "transporter", "Na-K ATPase", "glucose transporter"],
        conclusion_template=[
            "Channels allow passive ion flow down gradients",
            "Pumps use ATP to move solutes against gradients",
            "Transporters couple solute movement (symport/antiport)"
        ],
        reasoning_framework="""
        Membrane transport mechanisms:
        1. Ion channels:
           - Voltage-gated (Na+, K+, Ca2+ channels in neurons)
           - Ligand-gated (nAChR, GABA receptors)
           - Selectivity filters, gating mechanisms
           - High flux rates (~10^6 ions/sec)
        2. Primary active transport (pumps):
           - Na+/K+-ATPase: 3 Na+ out, 2 K+ in per ATP (electrogenic)
           - Ca2+-ATPase (SERCA): maintains low cytosolic Ca2+
           - H+/K+-ATPase: gastric acid secretion
           - ABC transporters: multidrug resistance (P-glycoprotein)
        3. Secondary active transport:
           - Na+-glucose symporter (SGLT1): uses Na+ gradient to drive glucose uptake
           - Na+/Ca2+ exchanger: extrudes Ca2+ using Na+ gradient
        4. Facilitated diffusion: GLUT transporters (down gradient, no ATP)
        """,
        key_factors=[
            "Gradient direction (with or against)",
            "Energy source (ATP, ion gradient, none)",
            "Stoichiometry and electrogenicity",
            "Regulation by phosphorylation, Ca2+",
            "Clinical relevance (digitalis, cystic fibrosis)"
        ],
        primary_authority=[
            "Skou Na+/K+-ATPase discovery",
            "MacKinnon K+ channel structure",
            "Wright Na+-glucose cotransporter studies"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Classify transport type, determine energy coupling, analyze physiological role"
    ),

    DoctrineBlock(
        topic="vitamins_coenzymes",
        keywords=["vitamin", "coenzyme", "cofactor", "NAD", "FAD", "coenzyme A"],
        conclusion_template=[
            "Vitamins are essential organic nutrients, often precursors to coenzymes",
            "Water-soluble vitamins (B, C) function in metabolism",
            "Fat-soluble vitamins (A, D, E, K) have diverse roles"
        ],
        reasoning_framework="""
        Vitamin and coenzyme functions:
        1. Vitamin B1 (thiamine) → TPP: decarboxylations (pyruvate, α-ketoglutarate DH)
        2. Vitamin B2 (riboflavin) → FAD, FMN: redox reactions (ETC, β-oxidation)
        3. Vitamin B3 (niacin) → NAD+, NADP+: redox reactions (glycolysis, TCA, biosynthesis)
        4. Vitamin B5 (pantothenic acid) → Coenzyme A: acyl group transfer (acetyl-CoA)
        5. Vitamin B6 (pyridoxine) → PLP: transaminations, decarboxylations
        6. Vitamin B12 (cobalamin): methylmalonyl-CoA mutase, methionine synthase
        7. Folate (B9) → THF: one-carbon transfers (thymidylate, purine synthesis)
        8. Biotin (B7): carboxylations (pyruvate, acetyl-CoA carboxylases)
        9. Vitamin C (ascorbate): antioxidant, collagen hydroxylation
        10. Vitamin A (retinol): vision (retinal), gene regulation (retinoic acid)
        11. Vitamin D (calciferol): Ca2+ homeostasis, bone health
        12. Vitamin E (tocopherol): lipid antioxidant
        13. Vitamin K: γ-carboxylation (clotting factors, osteocalcin)
        """,
        key_factors=[
            "Water vs fat solubility",
            "Coenzyme vs structural roles",
            "Deficiency diseases (beriberi, scurvy, pellagra, rickets)",
            "RDA and toxicity limits",
            "Metabolic pathways requiring each vitamin"
        ],
        primary_authority=[
            "Nutritional biochemistry textbooks",
            "Vitamin deficiency clinical studies",
            "Enzyme mechanism literature"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Identify coenzyme form, link to metabolic pathways, assess deficiency consequences"
    ),

    DoctrineBlock(
        topic="clinical_biochemistry",
        keywords=["biomarker", "liver function", "renal function", "cardiac marker", "diabetes"],
        conclusion_template=[
            "Clinical biochemistry tests assess organ function and disease states",
            "Enzyme elevation indicates tissue damage",
            "Metabolite levels reflect metabolic status"
        ],
        reasoning_framework="""
        Clinical biochemistry markers:
        1. Liver function:
           - ALT, AST: hepatocellular damage (AST also in heart, muscle)
           - ALP: cholestasis, bone disease
           - Bilirubin: jaundice, hemolysis, liver dysfunction
           - Albumin: synthetic function
        2. Renal function:
           - Creatinine: GFR estimation
           - BUN (blood urea nitrogen): renal clearance, protein catabolism
           - Electrolytes (Na+, K+, Cl-, HCO3-): acid-base, hydration
        3. Cardiac markers:
           - Troponin I/T: myocardial infarction (highly specific)
           - CK-MB: cardiac muscle damage (less specific)
           - BNP/NT-proBNP: heart failure
        4. Diabetes:
           - Fasting glucose: diagnosis (≥126 mg/dL diabetic)
           - HbA1c: 2-3 month average glucose (≥6.5% diabetic)
           - Oral glucose tolerance test
        5. Lipid panel: cholesterol, LDL, HDL, triglycerides (cardiovascular risk)
        """,
        key_factors=[
            "Reference ranges and critical values",
            "Sensitivity and specificity",
            "Timing of sample collection",
            "Organ-specific isoenzymes",
            "Longitudinal monitoring"
        ],
        primary_authority=[
            "Clinical chemistry textbooks",
            "American Association for Clinical Chemistry guidelines",
            "Laboratory reference manuals"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        resolution_strategy="Select appropriate tests, interpret in clinical context, correlate with symptoms/imaging"
    ),
]


class QueryRequest(BaseModel):
    question: str = Field(..., description="Biochemistry query")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class QueryResponse(BaseModel):
    answer: str
    confidence: str
    mode: str
    doctrines_used: List[str]
    reasoning_chain: List[str]
    determinism_hash: str
    timestamp: str


class TelemetryCollector:
    def __init__(self):
        self.queries: List[Dict[str, Any]] = []
        self.start_time = datetime.now()

    def log_query(self, question: str, mode: str, doctrines_triggered: List[str], latency_ms: float):
        self.queries.append({
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "mode": mode,
            "doctrines": doctrines_triggered,
            "latency_ms": latency_ms
        })
        logger.info(f"Query logged: {len(doctrines_triggered)} doctrines, {latency_ms:.2f}ms")

    def get_stats(self) -> Dict[str, Any]:
        if not self.queries:
            return {"total_queries": 0}

        latencies = [q["latency_ms"] for q in self.queries]
        return {
            "total_queries": len(self.queries),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds()
        }


class DriftWatcher:
    def __init__(self):
        self.doctrine_usage: Dict[str, int] = {d.topic: 0 for d in DOCTRINE_CACHE}

    def record_usage(self, doctrines: List[str]):
        for topic in doctrines:
            if topic in self.doctrine_usage:
                self.doctrine_usage[topic] += 1

    def get_coverage(self) -> Dict[str, Any]:
        total = sum(self.doctrine_usage.values())
        used = sum(1 for count in self.doctrine_usage.values() if count > 0)
        return {
            "total_doctrines": len(DOCTRINE_CACHE),
            "doctrines_used": used,
            "coverage_pct": (used / len(DOCTRINE_CACHE) * 100) if DOCTRINE_CACHE else 0,
            "total_invocations": total
        }


telemetry = TelemetryCollector()
drift_watcher = DriftWatcher()


def search_doctrines(question: str) -> List[DoctrineBlock]:
    """Search doctrine cache for relevant blocks"""
    question_lower = question.lower()
    matched = []

    for doctrine in DOCTRINE_CACHE:
        # Check if any keyword appears in question
        if any(kw.lower() in question_lower for kw in doctrine.keywords):
            matched.append(doctrine)
        # Or if topic appears
        elif doctrine.topic.replace("_", " ") in question_lower:
            matched.append(doctrine)

    return matched


def generate_answer(question: str, doctrines: List[DoctrineBlock], mode: ResponseMode) -> str:
    """Generate answer based on matched doctrines and mode"""
    if not doctrines:
        return "No specific biochemistry doctrines matched. Please provide more context or rephrase your question to focus on protein structure, enzyme kinetics, metabolic pathways, molecular biology, signal transduction, or clinical biochemistry."

    # Build answer from doctrine blocks
    answer_parts = []

    if mode == ResponseMode.FAST:
        # Concise answer
        for doctrine in doctrines[:2]:  # Use top 2 doctrines
            answer_parts.extend(doctrine.conclusion_template)
        return " ".join(answer_parts)

    elif mode == ResponseMode.DEFENSE:
        # Detailed with authorities
        for doctrine in doctrines:
            answer_parts.append(f"**{doctrine.topic.replace('_', ' ').title()}**")
            answer_parts.extend(doctrine.conclusion_template)
            answer_parts.append(f"Key factors: {', '.join(doctrine.key_factors)}")
            answer_parts.append(f"Authority: {'; '.join(doctrine.primary_authority)}")
            answer_parts.append("")
        return "\n".join(answer_parts)

    else:  # MEMO mode
        # Comprehensive analysis
        for doctrine in doctrines:
            answer_parts.append(f"### {doctrine.topic.replace('_', ' ').title()}")
            answer_parts.append("")
            answer_parts.append("**Conclusion:**")
            for conclusion in doctrine.conclusion_template:
                answer_parts.append(f"- {conclusion}")
            answer_parts.append("")
            answer_parts.append("**Reasoning Framework:**")
            answer_parts.append(doctrine.reasoning_framework.strip())
            answer_parts.append("")
            answer_parts.append("**Key Factors:**")
            for factor in doctrine.key_factors:
                answer_parts.append(f"- {factor}")
            answer_parts.append("")
            answer_parts.append("**Resolution Strategy:**")
            answer_parts.append(doctrine.resolution_strategy)
            answer_parts.append("")
            answer_parts.append("**Primary Authority:**")
            for auth in doctrine.primary_authority:
                answer_parts.append(f"- {auth}")
            answer_parts.append("")
            answer_parts.append(f"**Confidence Level:** {doctrine.confidence.value}")
            answer_parts.append("")
            answer_parts.append("---")
            answer_parts.append("")

        return "\n".join(answer_parts)


def calculate_hash(question: str, answer: str) -> str:
    """Generate deterministic SHA-256 hash"""
    content = f"{question}|{answer}"
    return hashlib.sha256(content.encode()).hexdigest()


@APP.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint"""
    start_time = datetime.now()

    logger.info(f"Query received: {request.question[:100]}... | Mode: {request.mode}")

    # Search doctrines
    matched_doctrines = search_doctrines(request.question)
    doctrine_topics = [d.topic for d in matched_doctrines]

    # Generate answer
    answer = generate_answer(request.question, matched_doctrines, request.mode)

    # Calculate hash
    determinism_hash = calculate_hash(request.question, answer)

    # Build reasoning chain
    reasoning_chain = []
    if matched_doctrines:
        reasoning_chain.append(f"Matched {len(matched_doctrines)} doctrine blocks")
        for doctrine in matched_doctrines[:3]:
            reasoning_chain.append(f"- {doctrine.topic}: {doctrine.confidence.value}")
    else:
        reasoning_chain.append("No direct doctrine matches found")

    # Determine overall confidence
    if matched_doctrines:
        confidence = matched_doctrines[0].confidence.value
    else:
        confidence = ConfidenceLevel.DISCLOSURE.value

    # Log telemetry
    latency_ms = (datetime.now() - start_time).total_seconds() * 1000
    telemetry.log_query(request.question, request.mode.value, doctrine_topics, latency_ms)
    drift_watcher.record_usage(doctrine_topics)

    logger.info(f"Query completed in {latency_ms:.2f}ms | Doctrines: {len(matched_doctrines)}")

    return QueryResponse(
        answer=answer,
        confidence=confidence,
        mode=request.mode.value,
        doctrines_used=doctrine_topics,
        reasoning_chain=reasoning_chain,
        determinism_hash=determinism_hash,
        timestamp=datetime.now().isoformat()
    )


@APP.get("/health")
async def health_check():
    """Health check endpoint"""
    stats = telemetry.get_stats()
    coverage = drift_watcher.get_coverage()

    return {
        "status": "healthy",
        "engine": "CHEM05_biochemistry",
        "version": "1.0.0",
        "port": 9055,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "telemetry": stats,
        "coverage": coverage,
        "timestamp": datetime.now().isoformat()
    }


@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total": len(DOCTRINE_CACHE),
        "topics": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting CHEM05 Biochemistry Engine on port 9055")
    uvicorn.run(APP, host="0.0.0.0", port=9055)
