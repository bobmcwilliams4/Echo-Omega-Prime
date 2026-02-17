"""
CHEM02 Inorganic Chemistry Intelligence Engine
Port: 9052
Version: 1.0.0

Comprehensive inorganic chemistry expertise covering coordination chemistry,
transition metals, solid state chemistry, organometallics, and industrial processes.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Literal
from dataclasses import dataclass, asdict, field
from enum import Enum

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# Configure loguru
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "logs" / "chem02_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)


class ResponseMode(str, Enum):
    """Query response modes."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    """Confidence stratification levels."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


@dataclass
class DoctrineBlock:
    """Fundamental knowledge block in inorganic chemistry."""
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    burden_holder: str = "query"
    adversary_position: str = ""
    counter_arguments: List[str] = field(default_factory=list)
    resolution_strategy: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class QueryRequest(BaseModel):
    """Inbound query structure."""
    question: str = Field(..., min_length=5, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    """Outbound response structure."""
    answer: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    reasoning_chain: List[str]
    authorities_cited: List[str]
    determinism_hash: str
    timestamp: str
    latency_ms: float


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float


# ============================================================================
# DOCTRINE CACHE - 25+ Real Inorganic Chemistry Doctrine Blocks
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    DoctrineBlock(
        topic="coordination_chemistry_fundamentals",
        keywords=["ligand", "coordination number", "chelate", "Werner", "EDTA", "denticity", "isomerism"],
        conclusion_template="Coordination chemistry analyzes metal-ligand bonding, predicts geometry from coordination number, and characterizes chelation stability via denticity and ring strain.",
        reasoning_framework="""
1. Werner's coordination theory established octahedral/tetrahedral geometries
2. Coordination number (CN) determines geometry: CN=2 linear, CN=4 square planar or tetrahedral, CN=6 octahedral
3. Chelate effect: polydentate ligands form more stable complexes than monodentate due to entropy gain
4. EDTA (hexadentate) forms very stable 1:1 complexes with most metal ions
5. Geometric isomerism (cis/trans) in square planar and octahedral complexes
6. Optical isomerism in octahedral complexes with chelating ligands (e.g., [Co(en)3]3+)
7. Ligand field strength affects geometry: strong field ligands favor low-spin octahedral
8. Hard-soft acid-base theory predicts ligand preference: hard metals (early TM) prefer hard ligands (O,F), soft metals (late TM) prefer soft ligands (S,P)
9. Spectrochemical series ranks ligands by field strength: I- < Br- < Cl- < F- < OH- < H2O < NH3 < en < NO2- < CN- < CO
10. Crystal field stabilization energy (CFSE) quantifies d-orbital splitting contribution to stability
11. Jahn-Teller distortion occurs in degenerate ground states (e.g., d9 Cu2+ elongates octahedral geometry)
12. Linkage isomerism (e.g., NO2- vs ONO-) in ambidentate ligands
13. Fluxional behavior in solution (Berry pseudorotation in trigonal bipyramidal)
14. Trans effect in square planar Pt(II) guides synthesis order
15. Stability constants (log K) measure complex formation equilibria
16. Irving-Williams series orders divalent 3d metal stability: Mn2+ < Fe2+ < Co2+ < Ni2+ < Cu2+ > Zn2+
17. Macrocyclic effect: cyclic ligands (porphyrins, crown ethers) show enhanced stability
18. Spin crossover in Fe(II) complexes between high-spin and low-spin states
19. Coordination polymers extend metal-ligand networks in 1D/2D/3D
20. Organometallic vs coordination: M-C sigma bonds vs dative bonds
""",
        key_factors=[
            "Coordination number and geometry",
            "Denticity and chelate effect",
            "Ligand field strength (spectrochemical series)",
            "Hard-soft acid-base matching",
            "CFSE and electronic configuration",
            "Isomerism types (geometric, optical, linkage)",
            "Stability constants and Irving-Williams order"
        ],
        primary_authority=[
            "Housecroft & Sharpe, Inorganic Chemistry (5th ed)",
            "Miessler, Fischer, Tarr, Inorganic Chemistry (5th ed)",
            "Cotton, Wilkinson, Murillo, Bochmann, Advanced Inorganic Chemistry (6th ed)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="crystal_field_theory",
        keywords=["d-orbital splitting", "CFSE", "high-spin", "low-spin", "octahedral", "tetrahedral", "Δo", "Δt"],
        conclusion_template="Crystal field theory (CFT) explains d-orbital energy splitting in ligand fields, predicts high-spin vs low-spin based on Δ vs pairing energy, and calculates CFSE contributions to thermodynamic stability.",
        reasoning_framework="""
1. CFT models ligands as point negative charges causing electrostatic repulsion with d-electrons
2. Octahedral field splits d-orbitals into t2g (dxy, dxz, dyz, lower energy) and eg (dx²-y², dz², higher energy)
3. Splitting parameter Δo (octahedral) or Δt (tetrahedral) depends on metal, oxidation state, and ligands
4. Δt ≈ 4/9 Δo for same metal and ligands (tetrahedral splitting smaller)
5. High-spin vs low-spin: if Δo < pairing energy P, electrons occupy all orbitals singly (high-spin); if Δo > P, electrons pair in t2g (low-spin)
6. Strong-field ligands (CN-, CO) → large Δo → low-spin; weak-field ligands (I-, Br-) → small Δo → high-spin
7. CFSE = (number in t2g × -0.4Δo) + (number in eg × +0.6Δo) for octahedral
8. d³ (Cr³+, low-spin) has CFSE = -1.2Δo (very stable)
9. d⁵ (Fe³+) has CFSE = 0 in high-spin (spherically symmetric, no stabilization)
10. d⁸ (Ni²+) always octahedral high-spin (3 unpaired), square planar in strong fields (0 unpaired)
11. Jahn-Teller theorem: degenerate electronic ground states distort to remove degeneracy (e.g., d⁹ Cu²+)
12. Color arises from d-d transitions: energy gap Δo determines wavelength absorbed
13. [Ti(H2O)6]³+ purple due to d¹ → single d-d transition in visible
14. Charge transfer transitions (LMCT, MLCT) more intense than d-d (Laporte forbidden)
15. Tanabe-Sugano diagrams predict electronic spectra for d² to d⁸ ions
16. Square planar splitting: dx²-y² highest, dxy next, then dxz/dyz, dz² lowest
17. Tetrahedral complexes usually high-spin (smaller Δt, no pairing)
18. CFT limitations: ignores covalency, orbital overlap, metal-ligand bonding
19. Ligand field theory (LFT) incorporates molecular orbital picture
20. Nephelauxetic effect: covalent bonding reduces interelectronic repulsion, redshifts spectra
""",
        key_factors=[
            "d-orbital splitting pattern (octahedral, tetrahedral, square planar)",
            "Magnitude of Δ vs pairing energy P",
            "CFSE calculation and thermodynamic contribution",
            "High-spin vs low-spin electron configuration",
            "Spectroscopic d-d transitions and color",
            "Jahn-Teller distortion in degenerate states"
        ],
        primary_authority=[
            "Orgel, An Introduction to Transition-Metal Chemistry: Ligand-Field Theory",
            "Figgis & Hitchman, Ligand Field Theory and Its Applications",
            "Housecroft & Sharpe, Inorganic Chemistry Ch 20"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="transition_metal_chemistry",
        keywords=["variable oxidation states", "catalysis", "magnetism", "color", "3d", "4d", "5d"],
        conclusion_template="Transition metals exhibit variable oxidation states, paramagnetism from unpaired d-electrons, catalytic activity via redox cycling, and intense colors from d-d/charge-transfer transitions.",
        reasoning_framework="""
1. d-block elements (Groups 3-12) have partially filled d-orbitals in ground state or common ions
2. Multiple oxidation states due to similar energy of (n)s and (n-1)d orbitals
3. Early TMs (Sc, Ti, V) show low → high OS progression; late TMs (Fe, Co, Ni) show +2/+3
4. Maximum OS = group number for Sc-Mn; +8 in OsO4, RuO4
5. +2 most common for late 3d (Fe, Co, Ni, Cu, Zn) due to loss of 4s electrons
6. Stability of high OS increases down group (4d, 5d more stable than 3d)
7. Catalysis: variable OS enables redox cycles (Haber: Fe 3d; Contact: V2O5)
8. Homogeneous catalysis: Wilkinson's catalyst [RhCl(PPh3)3] for alkene hydrogenation
9. Ziegler-Natta: TiCl4/AlEt3 polymerizes ethylene
10. Paramagnetism: unpaired electrons give magnetic moment μ = √(n(n+2)) BM
11. Ferromagnetism in metallic Fe, Co, Ni below Curie temperature
12. Antiferromagnetism in MnO, FeO (spins align antiparallel)
13. Color from d-d transitions (Laporte forbidden, weak) and charge transfer (allowed, intense)
14. [Cu(H2O)6]²+ blue, [MnO4]⁻ purple (LMCT), [Cr2O7]²⁻ orange
15. Lanthanide contraction: 4f electrons shield poorly, 5d/6s contract → 4d and 5d sizes similar
16. Platinum group metals (Ru, Rh, Pd, Os, Ir, Pt) are noble, resist corrosion
17. Coinage metals (Cu, Ag, Au) have filled d¹⁰, show +1 (soft, prefer S/P ligands)
18. Mercury unique: liquid at RT, high vapor pressure, toxic
19. Interstitial hydrides (PdH0.6) vs salt-like hydrides (CaH2)
20. Carbonyls: strong π-backbonding stabilizes low OS (Ni(CO)4, Fe(CO)5)
""",
        key_factors=[
            "Variable oxidation states and redox chemistry",
            "Paramagnetism and magnetic moment",
            "Catalytic redox cycles",
            "d-d and charge-transfer electronic transitions",
            "Lanthanide contraction effect on 5d elements",
            "Carbonyl π-backbonding"
        ],
        primary_authority=[
            "Cotton et al., Advanced Inorganic Chemistry Ch 16-22",
            "Shriver & Atkins, Inorganic Chemistry Ch 19",
            "Crabtree, The Organometallic Chemistry of the Transition Metals"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="main_group_chemistry",
        keywords=["p-block", "boron", "silicon", "nitrogen", "phosphorus", "sulfur", "halogens", "noble gases"],
        conclusion_template="Main group (s- and p-block) elements show diagonal relationships, variable catenation, stable oxidation states differing by 2 (inert pair effect), and form network solids (B, C, Si) vs molecular compounds (N, O, F).",
        reasoning_framework="""
1. s-block (Groups 1-2): alkali and alkaline earth metals, highly reactive, +1/+2 OS
2. p-block (Groups 13-18): diverse properties from metals (Al, Ga) to nonmetals (N, O, F)
3. Diagonal relationships: Li-Mg, Be-Al, B-Si due to similar charge/radius ratios
4. Inert pair effect: heavier p-block elements prefer OS 2 less than group number (Tl+, Pb²+, Bi³+)
5. Catenation: C >> Si > Ge; N, P, S form chains/rings (S8, P4)
6. Boron: electron-deficient, forms 3-center-2-electron bonds (B2H6, boranes)
7. Wade's rules classify boron hydrides by cluster geometry (closo, nido, arachno)
8. Carbon: sp³/sp²/sp hybridization, forms graphite (layers) and diamond (3D network)
9. Silicon: SiO2 network solid (quartz), silicates (zeolites, clays)
10. Nitrogen: N2 triple bond (945 kJ/mol) very stable, unreactive; N3- azide ion explosive
11. Phosphorus allotropes: white P4 (reactive), red P (polymeric), black P (layered)
12. Sulfur: S8 crown most stable, polysulfides Sn²-, SO2/SO3 acidic oxides
13. Halogens: F2 most reactive (low F-F bond energy), I2 least reactive
14. Interhalogen compounds: ClF3, BrF5 (hypervalent, sp³d, sp³d²)
15. Noble gases: Xe forms XeF2, XeF4, XeF6, XeO3; Kr, Ar compounds rare
16. Acid-base behavior: Group 13 Lewis acids (BF3, AlCl3), Group 15 Lewis bases (NH3, PH3)
17. Hydrides: ionic (NaH), covalent (CH4, NH3, H2O, HF), intermediate (B2H6)
18. Oxides: basic (Na2O, CaO), amphoteric (Al2O3), acidic (SO3, P4O10)
19. Silicones: (R2SiO)n polymers, hydrophobic, thermally stable
20. Organometallic compounds: Grignard (RMgX), organolithium (RLi) very reactive
""",
        key_factors=[
            "Diagonal relationships and periodic trends",
            "Inert pair effect in heavy p-block",
            "Catenation and allotropy",
            "Hypervalency in Period 3+ elements",
            "Network solids vs molecular structures",
            "Acid-base character of oxides and hydrides"
        ],
        primary_authority=[
            "Greenwood & Earnshaw, Chemistry of the Elements (2nd ed)",
            "Housecroft & Sharpe, Inorganic Chemistry Ch 12-17",
            "Cotton et al., Advanced Inorganic Chemistry Ch 7-15"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="lanthanides_actinides",
        keywords=["f-block", "rare earths", "4f", "5f", "uranium", "plutonium", "magnetic", "luminescence"],
        conclusion_template="Lanthanides (4f) and actinides (5f) show +3 predominant OS, similar chemical behavior (difficult separation), strong paramagnetism, and for actinides, radioactivity and variable OS due to 5f orbital energy.",
        reasoning_framework="""
1. Lanthanides: La-Lu, fill 4f orbitals, +3 most stable (Ce⁴+, Eu²+ exceptions)
2. Lanthanide contraction: progressive decrease in ionic radius across series due to poor 4f shielding
3. Chemical similarity: separation requires ion exchange or solvent extraction
4. Magnetic properties: large magnetic moments from unquenched orbital angular momentum
5. Luminescence: f-f transitions sharp, long-lived (Eu³+, Tb³+ in phosphors)
6. Nd:YAG laser: Nd³+ in Y3Al5O12 host
7. Actinides: Ac-Lr, fill 5f orbitals, all radioactive
8. Variable oxidation states in early actinides (U +3 to +6, Np, Pu similar)
9. UO2²+ uranyl ion linear, stable in aqueous solution
10. Plutonium chemistry complex: Pu³+, Pu⁴+, PuO2+, PuO2²+ can coexist in solution
11. Thorium chemistry resembles Zr, Hf (no 5f electrons in Th⁴+)
12. Transuranic elements (Np, Pu, Am, Cm) synthesized, short half-lives
13. Nuclear fuel cycle: UO2 fuel, Pu production in reactors
14. Separation: PUREX process extracts U, Pu with tributyl phosphate
15. Environmental chemistry: uranyl carbonate complexes mobile in groundwater
16. Magnetic ordering: rare earth metals show complex ferromagnetic/antiferromagnetic structures
17. Mixed valence oxides: Pr6O11 (Pr³+/Pr⁴+), Tb4O7
18. Coordination chemistry: high CNs (8-12) due to large ionic radii
19. Organometallic chemistry limited (4f/5f electrons buried), some Cp3M complexes
20. Superheavy elements (Rf-Og): gas-phase chemistry, extrapolate from periodic trends
""",
        key_factors=[
            "Lanthanide contraction and chemical similarity",
            "+3 predominant oxidation state",
            "Paramagnetism and luminescence from f-f transitions",
            "Actinide variable oxidation states (U, Np, Pu)",
            "Radioactivity and nuclear chemistry",
            "High coordination numbers"
        ],
        primary_authority=[
            "Cotton et al., Advanced Inorganic Chemistry Ch 23-24",
            "Katz, Seaborg, Morss (eds), The Chemistry of the Actinide and Transactinide Elements",
            "Greenwood & Earnshaw, Chemistry of the Elements Ch 25-26"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="bioinorganic_chemistry",
        keywords=["metalloenzyme", "hemoglobin", "chlorophyll", "ferredoxin", "zinc finger", "cobalamin", "oxygen transport"],
        conclusion_template="Bioinorganic chemistry examines metal cofactors in enzymes, oxygen transport via heme iron, electron transfer in iron-sulfur clusters, and structural roles of zinc in DNA-binding proteins.",
        reasoning_framework="""
1. ~30% of enzymes require metal cofactors for catalytic activity
2. Hemoglobin: Fe²+ in heme porphyrin binds O2 reversibly, cooperativity from quaternary structure
3. Myoglobin: monomeric, hyperbolic O2 binding curve
4. Deoxyhemoglobin Fe²+ high-spin (5-coord), oxyhemoglobin Fe²+ low-spin (6-coord)
5. CO binds Fe²+ 200x stronger than O2 (poisoning), distal His prevents linear binding
6. Chlorophyll: Mg²+ in porphyrin, light absorption for photosynthesis
7. Cytochrome P450: Fe heme, monooxygenase, drug metabolism, Fe³+/Fe⁴+=O species
8. Iron-sulfur clusters: [2Fe-2S], [4Fe-4S] in ferredoxins, electron transfer proteins
9. Superoxide dismutase (SOD): Cu/Zn-SOD, Mn-SOD, Fe-SOD dismutate O2⁻ to O2 + H2O2
10. Zinc finger proteins: Zn²+ tetrahedrally coordinated by Cys, His, stabilizes DNA-binding domain
11. Carbonic anhydrase: Zn²+ activates water for CO2 hydration (essential for respiration)
12. Nitrogenase: Mo-Fe-S cluster reduces N2 to NH3, requires 16 ATP per N2
13. Vitamin B12 (cobalamin): Co³+ in corrin ring, methyl/adenosyl derivatives, cofactor for isomerases
14. Copper proteins: Type 1 (blue, plastocyanin), Type 2 (EPR-active), Type 3 (binuclear, hemocyanin)
15. Hemocyanin: Cu-O2-Cu binds O2 in mollusks, arthropods (blue blood)
16. Calcium: structural (bones CaHPO4), signaling (calmodulin), muscle contraction
17. Magnesium: ATP complexes Mg-ATP²⁻, kinase substrates
18. Metalloregulation: Fe²+ uptake (ferritin storage, transferrin transport), toxic at high levels (Fenton chemistry)
19. Fenton reaction: Fe²+ + H2O2 → Fe³+ + OH• + OH⁻ (oxidative damage)
20. Chelation therapy: EDTA for Pb²+ poisoning, desferrioxamine for Fe overload
""",
        key_factors=[
            "Heme iron oxygen transport and cooperativity",
            "Electron transfer via iron-sulfur clusters",
            "Zinc structural and catalytic roles",
            "Copper redox and O2 binding",
            "Enzyme catalysis mechanisms (carbonic anhydrase, nitrogenase)",
            "Metal homeostasis and toxicity"
        ],
        primary_authority=[
            "Lippard & Berg, Principles of Bioinorganic Chemistry",
            "Bertini, Gray, Stiefel, Valentine, Biological Inorganic Chemistry",
            "Kaim, Schwederski, Bioinorganic Chemistry: Inorganic Elements in the Chemistry of Life"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="solid_state_chemistry",
        keywords=["crystal structure", "lattice energy", "band theory", "defects", "ionic conductivity", "perovskite", "spinel"],
        conclusion_template="Solid state chemistry analyzes crystal packing (fcc, bcc, hcp), predicts lattice energy via Born-Haber cycles, explains conductivity with band theory, and characterizes defects (Schottky, Frenkel) affecting properties.",
        reasoning_framework="""
1. Crystalline solids: long-range order, unit cell repeats in 3D
2. Bravais lattices: 14 types (cubic, tetragonal, orthorhombic, etc.)
3. Close packing: fcc (ABCABC), hcp (ABAB), ccp = fcc
4. Coordination number: fcc/hcp = 12, bcc = 8, simple cubic = 6
5. Ionic solids: cation/anion radius ratio determines structure (rock salt, CsCl, zinc blende, wurtzite, fluorite)
6. Rock salt (NaCl): fcc anions, octahedral cation sites, r+/r- = 0.414-0.732
7. CsCl structure: simple cubic anions, cubic cation site, r+/r- = 0.732-1.0
8. Zinc blende (ZnS): fcc anions, tetrahedral cation sites, r+/r- = 0.225-0.414
9. Lattice energy U: Born-Haber cycle, Coulombic attraction minus repulsion
10. Kapustinskii equation estimates U from charges and radii
11. Band theory: overlap of atomic orbitals forms bands, metals (overlapping bands), insulators (large gap), semiconductors (small gap ~1 eV)
12. Intrinsic semiconductors: Si, Ge, thermally excited electrons across band gap
13. Doping: n-type (P in Si, extra electrons), p-type (B in Si, holes)
14. Defects: Schottky (cation-anion pair missing), Frenkel (ion displaced to interstitial), color centers (F-center: anion vacancy with trapped electron)
15. Nonstoichiometry: Fe1-xO (wustite), variable composition, affects conductivity
16. Ionic conductivity: high in crystals with mobile defects (YSZ, beta-alumina)
17. Perovskite structure: ABO3 (CaTiO3), high-Tc superconductors YBa2Cu3O7-x
18. Spinel structure: AB2O4, normal (Mg2+ tetra, Al3+ octa) vs inverse (Fe3O4)
19. Layered structures: graphite, MoS2, clays (weak van der Waals between layers)
20. Zeolites: microporous aluminosilicates, cation exchange, molecular sieves, catalysis
""",
        key_factors=[
            "Crystal packing and coordination number",
            "Radius ratio rules for ionic structures",
            "Lattice energy and Born-Haber cycle",
            "Band theory: metals, semiconductors, insulators",
            "Point defects (Schottky, Frenkel) and nonstoichiometry",
            "Perovskite and spinel structure types"
        ],
        primary_authority=[
            "West, Solid State Chemistry and its Applications (2nd ed)",
            "Smart & Moore, Solid State Chemistry: An Introduction (4th ed)",
            "Greenwood & Earnshaw, Chemistry of the Elements Ch 5"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="catalysis_homogeneous_heterogeneous",
        keywords=["Wilkinson", "Ziegler-Natta", "Haber", "Contact", "hydrogenation", "polymerization", "oxidation"],
        conclusion_template="Catalysis accelerates reactions via alternate lower-energy pathways. Homogeneous catalysts (soluble metal complexes) offer selectivity; heterogeneous catalysts (solid surfaces) enable separation and continuous processing.",
        reasoning_framework="""
1. Catalyst lowers activation energy Ea, increases rate, not consumed
2. Homogeneous catalysis: catalyst in same phase as reactants (usually solution)
3. Wilkinson's catalyst: [RhCl(PPh3)3] hydrogenates alkenes (C=C + H2 → C-C)
4. Mechanism: oxidative addition of H2 to Rh(I) → Rh(III) dihydride, alkene insertion, reductive elimination
5. Monsanto process: [Rh(CO)2I2]⁻ carbonylates MeOH to acetic acid (CH3OH + CO → CH3COOH)
6. Wacker process: PdCl2/CuCl2 oxidizes ethylene to acetaldehyde (C2H4 + O2 → CH3CHO)
7. Olefin metathesis: Grubbs catalysts (Ru carbene) exchange C=C substituents (Nobel 2005)
8. Asymmetric hydrogenation: chiral Rh/Ru catalysts for enantioselective synthesis (Knowles, Noyori, Nobel 2001)
9. Heterogeneous catalysis: catalyst solid, reactants gas or liquid
10. Haber process: Fe/K2O/Al2O3 catalyst, N2 + 3H2 → 2NH3 (450°C, 200 atm)
11. Contact process: V2O5 catalyst, 2SO2 + O2 → 2SO3 (H2SO4 production)
12. Hydrogenation: Ni/Pd/Pt on carbon, alkene → alkane (edible oil hardening)
13. Catalytic converter: Pt/Pd/Rh on ceramic, oxidizes CO/HC, reduces NOx
14. Fluid catalytic cracking (FCC): zeolite catalyst breaks heavy hydrocarbons
15. Ziegler-Natta polymerization: TiCl4/AlEt3 stereoselectively polymerizes ethylene/propylene
16. Surface adsorption: chemisorption (strong, covalent), physisorption (weak, van der Waals)
17. Langmuir-Hinshelwood mechanism: both reactants adsorb before reaction
18. Eley-Rideal mechanism: one adsorbed, other gas-phase collision
19. Sabatier principle: optimal catalyst binds reactants not too weak, not too strong
20. Catalyst poisoning: sulfur poisons Pt, CO blocks Fe active sites
""",
        key_factors=[
            "Homogeneous: selectivity, mechanistic insight, separation difficulty",
            "Heterogeneous: separation, regeneration, industrial scale",
            "Oxidative addition/reductive elimination cycles",
            "Adsorption and surface reaction mechanisms",
            "Sabatier principle for catalyst optimization",
            "Poisoning and deactivation"
        ],
        primary_authority=[
            "Crabtree, The Organometallic Chemistry of the Transition Metals Ch 9",
            "Thomas & Thomas, Principles and Practice of Heterogeneous Catalysis",
            "Cornils & Herrmann (eds), Applied Homogeneous Catalysis with Organometallic Compounds"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="organometallic_chemistry",
        keywords=["metal-carbon bond", "18-electron rule", "backbonding", "carbonyl", "cyclopentadienyl", "metallocene"],
        conclusion_template="Organometallic chemistry studies M-C σ/π bonds, obeys 18-electron rule for stability, features π-backbonding (M → CO/alkene), and enables catalysis, synthesis, and materials.",
        reasoning_framework="""
1. Organometallic: at least one M-C bond (vs coordination chemistry: dative bonds)
2. 18-electron rule: valence count = 18 for stable d-block complexes (analogous to octet)
3. Electron counting: oxidation state method or neutral ligand method
4. Common ligands: CO (2e), Cp- (5e, η⁵), Cl- (1e, X-type), alkyl (1e, R-type)
5. Metal carbonyls: Ni(CO)4, Fe(CO)5, Cr(CO)6, linear or bent M-C-O
6. Synergistic bonding in carbonyls: M → CO σ donation, M ← CO π backbonding (dπ → π*)
7. Backbonding weakens C-O bond, strengthens M-C bond, IR ν(CO) < free CO (2143 cm⁻¹)
8. Bridging carbonyls: Fe2(CO)9 has CO bridging two Fe, IR ~1800 cm⁻¹
9. Metallocenes: Cp2Fe (ferrocene), sandwich structure, aromatic stability, 18e
10. Ferrocene: Fe²+ between two Cp⁻, rapid rotation in solution, orange solid
11. Chromocene Cp2Cr (16e), vanadocene Cp2V (15e), reactive (not 18e)
12. Half-sandwich complexes: CpMn(CO)3, Cp*Ir(CO)2 (Cp* = C5Me5)
13. Alkene complexes: Zeise's salt K[PtCl3(C2H4)], η² coordination, Dewar-Chatt-Duncanson model
14. Dewar-Chatt-Duncanson: alkene → M σ donation, M → alkene π backbonding (π*)
15. η⁶ arene complexes: (η⁶-C6H6)Cr(CO)3, activates arene for nucleophilic substitution
16. Oxidative addition: M + X-Y → M(X)(Y), increases OS by 2, adds 2 ligands (e.g., Vaska's complex + H2)
17. Reductive elimination: reverse of OA, forms X-Y bond, decreases OS by 2 (catalytic cycle step)
18. Insertion: CO inserts into M-R → M-C(O)R (acyl), key step in carbonylation
19. β-hydride elimination: alkyl with β-H → alkene + M-H, chain termination in polymerization
20. Schrock carbenes (M=C, high OS, electrophilic) vs Fischer carbenes (M=C, low OS, nucleophilic)
""",
        key_factors=[
            "18-electron rule and electron counting",
            "Synergistic π-backbonding (CO, alkenes)",
            "Metallocene stability and reactivity",
            "Elementary steps: OA, RE, insertion, β-H elimination",
            "Carbene types (Fischer vs Schrock)",
            "Catalytic cycle design"
        ],
        primary_authority=[
            "Crabtree, The Organometallic Chemistry of the Transition Metals (6th ed)",
            "Elschenbroich, Organometallics (3rd ed)",
            "Hartwig, Organotransition Metal Chemistry"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="symmetry_group_theory",
        keywords=["point group", "character table", "IR active", "Raman active", "irreducible representation", "C2v", "D3h"],
        conclusion_template="Symmetry and group theory classify molecules by point groups, predict spectroscopic selection rules (IR, Raman), simplify MO construction, and determine degeneracies in ligand field theory.",
        reasoning_framework="""
1. Symmetry element: point, line, or plane about which symmetry operation leaves molecule unchanged
2. Operations: E (identity), Cn (n-fold rotation), σ (reflection), i (inversion), Sn (improper rotation)
3. Point group: set of symmetry operations forming mathematical group
4. Common point groups: C1 (no symmetry), Cs (mirror), Ci (inversion), Cn, Cnv, Cnh, Dn, Dnh, Dnd, Td, Oh, Ih
5. H2O: C2v (C2 + 2σv), NH3: C3v, benzene: D6h, methane: Td, octahedral ML6: Oh
6. Character table: rows = irreducible representations (IRs), columns = symmetry operations
7. Characters: trace of matrix representation for each operation
8. Totally symmetric IR (A, A1, A1g): character +1 for all operations
9. IR active: vibration transforms as x, y, z (T1u, T2u in Oh)
10. Raman active: vibration transforms as x², xy, etc. (quadratic functions)
11. Mutual exclusion rule: centrosymmetric molecules have no overlap (IR ≠ Raman active)
12. CO2 (D∞h): asymmetric stretch IR active, symmetric stretch Raman active, bend both
13. H2O (C2v): all 3 modes IR and Raman active (no inversion center)
14. Octahedral ML6 (Oh): t1u IR active (triply degenerate), a1g + eg Raman active
15. Reducible representation reduces to sum of IRs via projection formula
16. Molecular orbitals: SALCs (symmetry-adapted linear combinations) from AOs of same IR
17. Splitting of d-orbitals: Oh splits d into t2g + eg
18. Jahn-Teller: degenerate electronic state (e.g., eg²) distorts to lower symmetry
19. Descent in symmetry: Oh → D4h (tetragonal) → C4v (square pyramidal)
20. Spectroscopic term symbols: ²S+¹L for free ions, Mulliken symbols for complexes
""",
        key_factors=[
            "Point group assignment from symmetry elements",
            "Character table interpretation",
            "IR vs Raman activity selection rules",
            "SALC construction for MO theory",
            "d-orbital splitting and term symbols",
            "Jahn-Teller distortion symmetry descent"
        ],
        primary_authority=[
            "Cotton, Chemical Applications of Group Theory (3rd ed)",
            "Harris & Bertolucci, Symmetry and Spectroscopy",
            "Housecroft & Sharpe, Inorganic Chemistry Ch 4"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="thermodynamics_inorganic_reactions",
        keywords=["ΔH", "ΔS", "ΔG", "Born-Haber", "lattice energy", "hydration enthalpy", "Ellingham diagram"],
        conclusion_template="Thermodynamics predicts reaction spontaneity via ΔG = ΔH - TΔS, quantifies lattice energies with Born-Haber cycles, and uses Ellingham diagrams to select reducing agents for metal oxide reduction.",
        reasoning_framework="""
1. First Law: ΔU = q + w (energy conserved)
2. Enthalpy H = U + PV, ΔH = qp (heat at constant pressure)
3. Standard enthalpy of formation ΔHf°: elements → compound at 298 K, 1 bar
4. Hess's Law: ΔH independent of path, sum of steps
5. Born-Haber cycle: enthalpy cycle for ionic solid formation
6. Steps: M(s) → M(g) (sublimation ΔHsub), M(g) → M+(g) (IE), X2(g) → 2X(g) (bond energy), X(g) → X-(g) (EA), M+(g) + X-(g) → MX(s) (lattice energy U)
7. Lattice energy U: energy to separate 1 mol ionic solid into gas ions
8. Coulombic model: U ∝ z+z-/r, larger charges and smaller radii → larger U
9. Kapustinskii equation: U (kJ/mol) ≈ 1202 × z+z- × ν / (r+ + r-) × (1 - 0.345/(r+ + r-))
10. Hydration enthalpy ΔHhyd: energy released dissolving gas ion in water (highly negative for small, high-charge ions)
11. Solubility: ΔHsol = U + ΔHhyd (if ΔHhyd very negative, soluble despite large U)
12. Entropy S: measure of disorder, ΔS positive for gas formation, dissolution
13. Gibbs free energy: ΔG = ΔH - TΔS, ΔG < 0 spontaneous
14. Temperature dependence: exothermic + entropy increase (ΔH < 0, ΔS > 0) always spontaneous; endothermic + entropy decrease never spontaneous; mixed cases depend on T
15. Ellingham diagram: ΔG° vs T for metal oxide formation, more negative = more stable
16. Reducing agent selection: for MxOy → M, use element with more negative ΔG(oxide formation) at T (e.g., C reduces Fe2O3, Al reduces Cr2O3)
17. van't Hoff equation: ln(K2/K1) = -ΔH°/R × (1/T2 - 1/T1)
18. Le Chatelier: system shifts to counteract stress (T, P, concentration)
19. Coupled reactions: nonspontaneous + spontaneous → overall spontaneous (e.g., ATP hydrolysis drives biosynthesis)
20. Metastable states: diamond thermodynamically unstable vs graphite but kinetic barrier prevents conversion at RT
""",
        key_factors=[
            "Born-Haber cycle and lattice energy",
            "ΔG = ΔH - TΔS spontaneity criterion",
            "Ellingham diagrams for metallurgy",
            "Hydration enthalpy and solubility",
            "Temperature dependence of equilibrium",
            "Coupled reactions"
        ],
        primary_authority=[
            "Atkins & de Paula, Physical Chemistry (10th ed) Ch 3-6",
            "Housecroft & Sharpe, Inorganic Chemistry Ch 6",
            "Greenwood & Earnshaw, Chemistry of the Elements Ch 8"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="kinetics_inorganic_reactions",
        keywords=["rate law", "mechanism", "activation energy", "substitution", "associative", "dissociative", "SN1", "SN2"],
        conclusion_template="Kinetics measures reaction rates via rate laws, distinguishes mechanisms (associative vs dissociative substitution), and quantifies activation barriers via Arrhenius equation or transition state theory.",
        reasoning_framework="""
1. Rate law: rate = k[A]^m[B]^n, orders m, n from experiment (not stoichiometry)
2. Rate constant k: temperature-dependent, units vary by order
3. Arrhenius equation: k = A × exp(-Ea/RT), Ea = activation energy, A = pre-exponential
4. Transition state theory: ΔG‡ = activation free energy, k ∝ exp(-ΔG‡/RT)
5. Mechanism: sequence of elementary steps (each molecularity 1 or 2)
6. Rate-determining step (RDS): slowest step controls overall rate
7. Steady-state approximation: d[intermediate]/dt ≈ 0
8. Pre-equilibrium: fast reversible step before slow step
9. Substitution mechanisms in octahedral complexes: associative (A), interchange (I), dissociative (D)
10. Dissociative (D): ligand leaves first (5-coord intermediate), then new ligand enters
11. Associative (A): new ligand enters first (7-coord intermediate), then old ligand leaves
12. Interchange (Ia, Id): concerted, associative or dissociative character
13. Square planar substitution: associative (5-coord transition state), trans effect guides selectivity
14. Trans effect: ligand trans to strong π-acceptor (CO, CN-) labilizes, cis to strong σ-donor labilizes
15. Examples: Pt(NH3)2Cl2 (cisplatin synthesis), trans effect of Cl- used to place NH3 cis
16. Electron transfer: inner-sphere (bridged ligand) vs outer-sphere (no bridge)
17. Marcus theory: outer-sphere ET rate depends on reorganization energy λ and driving force ΔG°
18. Self-exchange rates: [Fe(H2O)6]2+/3+ slow (high-spin/low-spin change), [Fe(CN)6]4-/3- fast (same spin)
19. Taube-type experiments: prove inner-sphere by ligand transfer (e.g., Cl- transfer in Cr2+/CoCl2+ redox)
20. Catalysis: catalyst provides lower-energy pathway, not in rate law if in fast pre-equilibrium
""",
        key_factors=[
            "Rate law determination from experimental data",
            "Arrhenius/transition state activation energy",
            "Associative vs dissociative substitution mechanisms",
            "Trans effect in square planar complexes",
            "Inner-sphere vs outer-sphere electron transfer",
            "Marcus theory reorganization energy"
        ],
        primary_authority=[
            "Atkins & de Paula, Physical Chemistry Ch 20-21",
            "Basolo & Pearson, Mechanisms of Inorganic Reactions (2nd ed)",
            "Wilkins, Kinetics and Mechanism of Reactions of Transition Metal Complexes"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="electrochemistry_redox",
        keywords=["standard potential", "Nernst", "Pourbaix", "galvanic cell", "electrolysis", "overpotential"],
        conclusion_template="Electrochemistry quantifies redox via standard potentials E°, predicts cell voltage with Nernst equation, maps stability with Pourbaix diagrams, and drives nonspontaneous reactions via electrolysis.",
        reasoning_framework="""
1. Redox: oxidation (loss e-), reduction (gain e-), simultaneous
2. Half-reactions: separate oxidation and reduction, balance electrons
3. Standard reduction potential E°: voltage vs SHE (standard hydrogen electrode, 0 V)
4. More positive E° = stronger oxidizing agent (easier to reduce)
5. Cell potential: E°cell = E°cathode - E°anode (positive if spontaneous)
6. ΔG° = -nFE°cell (F = 96485 C/mol, Faraday constant)
7. Nernst equation: E = E° - (RT/nF)lnQ, at 298 K: E = E° - (0.0592/n)logQ
8. Concentration cells: same electrodes, different concentrations, E from Nernst
9. Pourbaix diagram: E vs pH stability map for metal/oxide/ion species
10. Water stability window: 0 V (2H+ + 2e- → H2) to 1.23 V (O2 + 4H+ + 4e- → 2H2O)
11. Corrosion: oxidation of metal, prevented by coatings, cathodic protection, or passivation
12. Passivation: oxide layer (Al2O3 on Al, Cr2O3 on stainless steel) protects bulk
13. Galvanic series: ranks metals by corrosion tendency in seawater (Mg most active, Au most noble)
14. Electrolysis: nonspontaneous reaction driven by external voltage (e.g., H2O → H2 + O2)
15. Chloralkali process: electrolysis of NaCl(aq) → Cl2(g) + H2(g) + NaOH(aq)
16. Overpotential: extra voltage beyond thermodynamic minimum to achieve practical current
17. Tafel equation: η = a + b×log(i), overpotential η vs current density i
18. Batteries: galvanic cells, discharge spontaneously (Zn-carbon, alkaline, Li-ion)
19. Fuel cells: H2/O2 → H2O, continuous reactant supply, high efficiency
20. Reference electrodes: SHE (0 V), SCE (saturated calomel, +0.241 V), Ag/AgCl (+0.197 V)
""",
        key_factors=[
            "Standard potentials and cell voltage",
            "Nernst equation for concentration dependence",
            "Pourbaix diagrams and corrosion prediction",
            "Electrolysis and overpotential",
            "Galvanic vs electrolytic cells",
            "Batteries and fuel cells"
        ],
        primary_authority=[
            "Atkins & de Paula, Physical Chemistry Ch 6",
            "Bard & Faulkner, Electrochemical Methods (2nd ed)",
            "Greenwood & Earnshaw, Chemistry of the Elements Ch 8"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="corrosion_science",
        keywords=["rust", "passivation", "galvanic", "pitting", "cathodic protection", "anodizing"],
        conclusion_template="Corrosion degrades metals via electrochemical oxidation, prevented by passivation (oxide films), cathodic protection (sacrificial anode), or coatings; accelerated by galvanic coupling and chloride-induced pitting.",
        reasoning_framework="""
1. Corrosion: electrochemical oxidation of metal (M → M^n+ + ne-)
2. Rust: hydrated Fe2O3·xH2O from Fe + O2 + H2O
3. Anodic reaction: Fe → Fe²+ + 2e- (oxidation)
4. Cathodic reaction: O2 + 2H2O + 4e- → 4OH- (neutral/basic) or 2H+ + 2e- → H2 (acidic)
5. Overall: 2Fe + O2 + 2H2O → 2Fe(OH)2 → Fe2O3·H2O (rust)
6. Galvanic corrosion: two dissimilar metals in contact, more active (anode) corrodes faster
7. Galvanic series in seawater: Mg/Zn/Al (active) vs Cu/Ag/Au (noble)
8. Sacrificial anode: attach more active metal (Zn on steel hull) to protect structure
9. Cathodic protection: impress current to make structure cathode (steel pipelines)
10. Passivation: protective oxide layer (Al2O3 on Al, Cr2O3 on stainless steel)
11. Stainless steel: >10.5% Cr forms passive Cr2O3, self-healing in air
12. Pitting corrosion: localized attack, initiated by Cl- breaking passive film
13. Crevice corrosion: oxygen depletion in crevice → acidic, aggressive environment
14. Stress corrosion cracking (SCC): tensile stress + corrosive environment → brittle fracture
15. Intergranular corrosion: grain boundaries preferentially attacked (sensitized stainless steel)
16. Coatings: paints, polymers, electroplating (Zn on steel = galvanizing, Sn = tin plate)
17. Anodizing: electrochemical oxidation thickens oxide (Al2O3 on Al), can be dyed
18. Corrosion inhibitors: chemicals slow corrosion (chromates, phosphates, organic amines)
19. Pourbaix diagram: predicts stable species (metal, oxide, ion) at given E and pH
20. Atmospheric corrosion: depends on humidity, pollutants (SO2, NOx, salt spray)
""",
        key_factors=[
            "Anodic oxidation and cathodic reduction",
            "Galvanic series and dissimilar metal coupling",
            "Passivation and oxide film stability",
            "Pitting and crevice corrosion mechanisms",
            "Cathodic protection (sacrificial anode, impressed current)",
            "Coatings and inhibitors"
        ],
        primary_authority=[
            "Fontana, Corrosion Engineering (3rd ed)",
            "Revie & Uhlig, Corrosion and Corrosion Control (4th ed)",
            "ASM Handbook Vol 13A: Corrosion: Fundamentals, Testing, and Protection"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="materials_science_fundamentals",
        keywords=["phase diagram", "microstructure", "mechanical properties", "ceramics", "polymers", "composites"],
        conclusion_template="Materials science links atomic structure to macroscopic properties via processing, uses phase diagrams to control microstructure, and classifies materials as metals, ceramics, polymers, or composites with distinct mechanical behaviors.",
        reasoning_framework="""
1. Materials: metals (crystalline, ductile, conductive), ceramics (ionic/covalent, brittle, insulating), polymers (covalent chains, flexible, insulating), composites (multiphase)
2. Phase diagram: map of stable phases vs T, composition (binary: Fe-C, Cu-Ni)
3. Lever rule: calculate phase fractions in two-phase region
4. Eutectic: lowest melting composition, solidifies at constant T to two phases
5. Peritectic: liquid + solid → new solid on cooling
6. Fe-Fe3C (iron-carbon): austenite (γ-Fe, fcc), ferrite (α-Fe, bcc), cementite (Fe3C, brittle)
7. Steel: <2.1 wt% C, heat treatment (quench, temper) controls microstructure and hardness
8. Annealing: heat + slow cool, reduces dislocations, softens
9. Quenching: rapid cool, traps high-T phase (martensite in steel, very hard)
10. Tempering: reheat quenched steel, reduces brittleness, retains hardness
11. Grain boundaries: high-energy regions, nucleation sites for corrosion/cracking
12. Hall-Petch: strength ∝ d^(-1/2), smaller grains → stronger
13. Ceramics: Al2O3, SiC, Si3N4, high hardness, low toughness, high melting
14. Sintering: heat ceramic powder below melting to densify (diffusion bonding)
15. Glass: amorphous SiO2, supercooled liquid, no long-range order
16. Polymers: thermoplastics (melt/reform: PE, PVC) vs thermosets (crosslinked, infusible: epoxy)
17. Degree of polymerization: chain length, affects Tg (glass transition) and Tm (melting)
18. Composites: fiber-reinforced (carbon fiber/epoxy), particulate (concrete), layered (plywood)
19. Mechanical properties: stress σ = F/A, strain ε = ΔL/L0, Young's modulus E = σ/ε
20. Tensile test: yield strength, ultimate tensile strength (UTS), elongation, toughness (area under curve)
""",
        key_factors=[
            "Phase diagrams and microstructure control",
            "Heat treatment (annealing, quenching, tempering)",
            "Hall-Petch grain size strengthening",
            "Ceramic brittleness and sintering",
            "Polymer thermoplastics vs thermosets",
            "Composite reinforcement mechanisms"
        ],
        primary_authority=[
            "Callister & Rethwisch, Materials Science and Engineering: An Introduction (10th ed)",
            "Ashby & Jones, Engineering Materials (4th ed)",
            "Shackelford, Introduction to Materials Science for Engineers (8th ed)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="ceramic_chemistry",
        keywords=["alumina", "zirconia", "silicon carbide", "sintering", "refractory", "piezoelectric"],
        conclusion_template="Ceramic chemistry synthesizes oxide, carbide, nitride ceramics via powder processing and sintering, achieving high hardness, chemical inertness, and thermal stability for structural, electronic, and refractory applications.",
        reasoning_framework="""
1. Ceramics: inorganic, nonmetallic solids (oxides, carbides, nitrides, borides)
2. Alumina Al2O3: high hardness (9 Mohs), high melting (2072°C), electrical insulator, spark plugs, cutting tools
3. Zirconia ZrO2: polymorphs (monoclinic, tetragonal, cubic), stabilized by Y2O3 (YSZ)
4. YSZ (yttria-stabilized zirconia): high ionic conductivity at high T, solid oxide fuel cells (SOFC)
5. Toughening: tetragonal → monoclinic transformation absorbs crack energy (transformation toughening)
6. Silicon carbide SiC: covalent, very hard, high thermal conductivity, abrasives, armor
7. Silicon nitride Si3N4: covalent, high strength, thermal shock resistant, turbine blades
8. Boron carbide B4C: third-hardest material (after diamond, cubic BN), armor
9. Powder processing: ball milling, spray drying, pressing (uniaxial or isostatic)
10. Sintering: heat <Tm, diffusion bonds particles, densifies (eliminates porosity)
11. Liquid-phase sintering: additive melts, capillary flow accelerates densification
12. Hot pressing: simultaneous heat + pressure, full density, shorter time
13. Sol-gel: metal alkoxide hydrolysis → gel → ceramic, high purity, low T
14. Refractories: withstand high T without melting (firebrick MgO, Al2O3, SiC)
15. Piezoelectric ceramics: BaTiO3, PZT (Pb(Zr,Ti)O3), voltage from stress (sensors, actuators)
16. Ferroelectric: spontaneous polarization, switchable (PZT, memory devices)
17. Magnetic ceramics: ferrites (Fe3O4, MFe2O4), high resistivity (low eddy current), transformers
18. Dielectric ceramics: capacitors (BaTiO3, high permittivity)
19. Glass-ceramics: controlled crystallization of glass (Corning Pyroceram), low thermal expansion
20. Bioceramics: hydroxyapatite Ca10(PO4)6(OH)2 for bone implants
""",
        key_factors=[
            "Alumina and zirconia structural ceramics",
            "SiC and Si3N4 high-performance ceramics",
            "Sintering and densification mechanisms",
            "Piezoelectric and ferroelectric properties",
            "Refractories for high-temperature service",
            "Ionic conductivity in YSZ"
        ],
        primary_authority=[
            "Carter & Norton, Ceramic Materials: Science and Engineering (2nd ed)",
            "Richerson, Modern Ceramic Engineering (3rd ed)",
            "Kingery, Bowen, Uhlmann, Introduction to Ceramics (2nd ed)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="semiconductor_chemistry",
        keywords=["silicon", "doping", "p-type", "n-type", "band gap", "GaAs", "LED", "photovoltaic"],
        conclusion_template="Semiconductor chemistry controls electronic properties via doping (n-type P in Si, p-type B in Si), exploits band gaps for optoelectronics (LEDs, lasers, solar cells), and uses III-V compounds (GaAs) for high-speed devices.",
        reasoning_framework="""
1. Semiconductors: band gap Eg ~0.5-3 eV, conductivity increases with T (thermally excited carriers)
2. Intrinsic semiconductor: pure Si, Ge, equal electrons (n) and holes (p)
3. Doping: add impurity to increase n or p
4. n-type: Group 15 dopant (P, As, Sb) in Si, extra electron → donor level near conduction band
5. p-type: Group 13 dopant (B, Al, Ga) in Si, missing electron → acceptor level near valence band
6. Fermi level: shifts toward conduction band (n-type) or valence band (p-type)
7. p-n junction: p-type | n-type interface, depletion region, built-in potential
8. Diode: p-n junction, rectifies current (forward bias: low R, reverse bias: high R)
9. Transistor: bipolar (npn, pnp) or field-effect (MOSFET), switching/amplification
10. Integrated circuits: billions of transistors on Si wafer (Moore's Law)
11. Band gap engineering: Eg determines max wavelength absorbed/emitted (hν = Eg)
12. Si: Eg = 1.1 eV (indirect, poor LED), GaAs: Eg = 1.42 eV (direct, efficient LED)
13. Direct vs indirect: direct (GaAs, InP) efficient light emission, indirect (Si, Ge) phonon-assisted
14. III-V semiconductors: GaAs, InP, GaN, high electron mobility, optoelectronics
15. LED: forward-biased p-n junction, electron-hole recombination emits photon
16. Blue LED: GaN (Eg ~3.4 eV), Nobel 2014 (Nakamura, Akasaki, Amano)
17. Laser diode: stimulated emission in p-n junction, coherent light
18. Solar cell: photovoltaic, photon absorbed → electron-hole pair → current
19. II-VI semiconductors: CdTe, ZnSe, used in solar cells, light-emitting devices
20. Quantum dots: nanocrystals, size-tunable band gap, quantum confinement
""",
        key_factors=[
            "Doping to create n-type and p-type",
            "p-n junction and diode behavior",
            "Band gap and direct vs indirect transitions",
            "III-V semiconductors for optoelectronics",
            "LED, laser diode, solar cell operation",
            "Quantum confinement in nanocrystals"
        ],
        primary_authority=[
            "Streetman & Banerjee, Solid State Electronic Devices (7th ed)",
            "Sze & Ng, Physics of Semiconductor Devices (3rd ed)",
            "Greenwood & Earnshaw, Chemistry of the Elements Ch 9"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="nuclear_chemistry_basics",
        keywords=["radioactivity", "alpha", "beta", "gamma", "half-life", "fission", "fusion", "isotopes"],
        conclusion_template="Nuclear chemistry studies radioactive decay (α, β, γ), quantifies decay rates via half-life, harnesses fission (U-235) for energy and weapons, and pursues fusion (D-T) for clean power.",
        reasoning_framework="""
1. Nucleus: protons (Z) + neutrons (N), isotopes differ in N (¹²C, ¹³C, ¹⁴C)
2. Radioactivity: unstable nucleus emits radiation to reach stability
3. Alpha decay: ⁴He²+ emission, Z-2, A-4 (²³⁸U → ²³⁴Th + α)
4. Beta decay: β⁻ (electron, neutron → proton), β+ (positron, proton → neutron), electron capture
5. ¹⁴C → ¹⁴N + β⁻ (radiocarbon dating, t₁/₂ = 5730 y)
6. Gamma decay: high-energy photon, no change in Z/A, follows α/β to deexcite
7. Half-life t₁/₂: time for N to decrease by half, first-order kinetics N(t) = N0 × exp(-λt)
8. Activity A = λN (Bq or Ci), λ = ln(2)/t₁/₂
9. Decay series: ²³⁸U → ²³⁴Th → ... → ²⁰⁶Pb (stable)
10. Fission: heavy nucleus splits into fragments + neutrons + energy (¹n + ²³⁵U → ⁹²Kr + ¹⁴¹Ba + 3¹n)
11. Chain reaction: neutrons from fission induce more fissions, critical mass required
12. Nuclear reactor: controlled fission, moderator slows neutrons (H2O, graphite), control rods absorb neutrons (Cd, B)
13. Fusion: light nuclei combine, releases energy (D + T → ⁴He + n + 17.6 MeV)
14. Stellar fusion: pp chain (H → He in Sun), CNO cycle in massive stars
15. Thermonuclear weapons: fission trigger initiates fusion (H-bomb)
16. Binding energy per nucleon: maximum at Fe-56, fission/fusion release energy moving toward Fe
17. Transmutation: nuclear reaction changes element (²⁷Al + α → ³⁰P + n, Joliot-Curie 1934)
18. Neutron activation analysis: irradiate sample, measure γ from induced radioactivity, quantify elements
19. Radiometric dating: ¹⁴C (organic, <50,000 y), K-Ar (rocks, millions y), U-Pb (billions y)
20. Radiation units: Gy (absorbed dose), Sv (equivalent dose, accounts for biological effect)
""",
        key_factors=[
            "Alpha, beta, gamma decay modes",
            "Half-life and first-order decay kinetics",
            "Fission chain reaction and critical mass",
            "Fusion energy release and conditions",
            "Binding energy curve and stability",
            "Radiometric dating techniques"
        ],
        primary_authority=[
            "Friedlander, Kennedy, Macias, Miller, Nuclear and Radiochemistry (3rd ed)",
            "Choppin, Liljenzin, Rydberg, Radiochemistry and Nuclear Chemistry (3rd ed)",
            "Greenwood & Earnshaw, Chemistry of the Elements Ch 1"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="environmental_inorganic_chemistry",
        keywords=["heavy metals", "mercury", "lead", "arsenic", "cadmium", "bioaccumulation", "remediation"],
        conclusion_template="Environmental inorganic chemistry tracks toxic heavy metal speciation (Hg²+, CH3Hg+, As³+/As⁵+), mobility, bioaccumulation in food chains, and remediation via precipitation, adsorption, or phytoremediation.",
        reasoning_framework="""
1. Heavy metals: Pb, Hg, Cd, As, Cr (toxic at low concentrations, persist in environment)
2. Mercury: elemental Hg⁰ (volatile), Hg²+ (soluble, binds sulfhydryl), CH3Hg+ (methylmercury, neurotoxic)
3. Methylmercury: biomagnifies in fish, Minamata disease (Japan 1950s)
4. Hg sources: coal combustion, gold mining (amalgamation), chloralkali (historical)
5. Lead: Pb²+ (soluble), PbS (galena), Pb(OH)2, PbCO3 (minerals)
6. Pb toxicity: inhibits enzymes (δ-aminolevulinic acid dehydratase), neurological damage
7. Pb sources: leaded gasoline (banned), old paint, plumbing (soft water dissolves Pb from pipes)
8. Arsenic: As³+ (arsenite, more toxic), As⁵+ (arsenate, less toxic), both carcinogenic
9. Arsenic in groundwater: natural (dissolution of As-bearing minerals), affects millions (Bangladesh, West Bengal)
10. Chromium: Cr³+ (essential nutrient, low solubility), Cr⁶+ (chromate CrO4²⁻, toxic, carcinogenic)
11. Erin Brockovich case: Cr⁶+ in groundwater from industrial cooling tower
12. Cadmium: Cd²+ (toxic, substitutes for Zn²+ in enzymes), bioaccumulates
13. Itai-itai disease: Cd poisoning from rice (Japan), kidney damage, bone loss
14. Speciation: chemical form affects mobility, toxicity (e.g., Cr⁶+ mobile, Cr³+ precipitates)
15. pH dependence: metal solubility increases at low pH (acid mine drainage mobilizes metals)
16. Complexation: organic ligands (EDTA, humic acids) increase metal mobility
17. Adsorption: metals bind to clays, Fe/Mn oxides, reduce mobility
18. Remediation: precipitation (add lime to raise pH), ion exchange, reverse osmosis
19. Phytoremediation: hyperaccumulator plants (Thlaspi, ferns) extract metals from soil
20. Bioavailability: fraction available for uptake by organisms, depends on speciation, binding
""",
        key_factors=[
            "Toxic metal speciation (Hg, Pb, As, Cr, Cd)",
            "Methylmercury biomagnification",
            "Cr(VI) vs Cr(III) toxicity and mobility",
            "pH and complexation effects on solubility",
            "Adsorption and precipitation controls",
            "Remediation strategies (chemical, biological)"
        ],
        primary_authority=[
            "Stumm & Morgan, Aquatic Chemistry (3rd ed)",
            "Langmuir, Aqueous Environmental Geochemistry",
            "Manahan, Environmental Chemistry (9th ed)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="industrial_inorganic_processes",
        keywords=["Haber", "Contact", "chloralkali", "Solvay", "ammonia", "sulfuric acid", "sodium hydroxide"],
        conclusion_template="Industrial inorganic processes produce bulk chemicals at scale: Haber (NH3 from N2+H2, Fe catalyst, high P/T), Contact (H2SO4 via V2O5-catalyzed SO2 oxidation), chloralkali (Cl2, H2, NaOH electrolysis), Solvay (Na2CO3 from NaCl+CaCO3).",
        reasoning_framework="""
1. Haber-Bosch process: N2 + 3H2 → 2NH3, Fe/K2O/Al2O3 catalyst, 450°C, 200 atm
2. Haber: equilibrium favors NH3 at low T, but rate too slow → compromise at 450°C
3. High pressure shifts equilibrium right (fewer gas moles), increases NH3 yield
4. Ammonia uses: fertilizers (80%), explosives, nitric acid (Ostwald process)
5. Ostwald process: 4NH3 + 5O2 → 4NO + 6H2O (Pt catalyst), 2NO + O2 → 2NO2, 3NO2 + H2O → 2HNO3 + NO
6. Contact process: S + O2 → SO2, 2SO2 + O2 ⇌ 2SO3 (V2O5 catalyst, 450°C), SO3 + H2SO4 → H2S2O7, H2S2O7 + H2O → 2H2SO4
7. Sulfuric acid: most-produced chemical worldwide, fertilizers, petroleum refining, steel pickling
8. Chloralkali: electrolysis of NaCl(aq), cathode: 2H2O + 2e- → H2 + 2OH-, anode: 2Cl- → Cl2 + 2e-
9. Membrane cell: Nafion membrane separates anode/cathode, prevents Cl2 + NaOH reaction
10. Products: Cl2 (PVC, solvents, disinfection), H2 (fuel, Haber), NaOH (paper, soap, alumina)
11. Solvay process: NaCl + NH3 + CO2 + H2O → NaHCO3 + NH4Cl, 2NaHCO3 → Na2CO3 + H2O + CO2
12. Soda ash (Na2CO3): glass, detergents, sodium compounds
13. Limestone (CaCO3) calcined: CaCO3 → CaO + CO2 (CO2 recycled, CaO slakes NH4Cl to regenerate NH3)
14. Thermite reaction: Fe2O3 + 2Al → 2Fe + Al2O3, exothermic, railway welding
15. Hall-Héroult process: electrolysis of Al2O3 in molten cryolite (Na3AlF6), produces Al metal
16. Anodes: carbon, oxidized to CO2, replaced periodically; cathode: molten Al collects
17. Frasch process: extract sulfur from underground deposits, superheated water melts S
18. Water gas shift: CO + H2O → CO2 + H2, industrial H2 production (steam reforming + WGS)
19. Steam reforming: CH4 + H2O → CO + 3H2 (Ni catalyst, 800°C), major H2 source
20. Ammonia oxidation: 4NH3 + 3O2 → 2N2 + 6H2O (emergency detoxification)
""",
        key_factors=[
            "Haber process: Fe catalyst, high P/T, Le Chatelier",
            "Contact process: V2O5 catalyst, SO3 formation",
            "Chloralkali electrolysis: membrane cell technology",
            "Solvay process: NH3 recovery, CaCO3 calcination",
            "Hall-Héroult Al production from bauxite",
            "Economic and environmental impact of bulk chemicals"
        ],
        primary_authority=[
            "Hocking, Handbook of Chemical Technology and Pollution Control (3rd ed)",
            "Greenwood & Earnshaw, Chemistry of the Elements (industrial sections)",
            "Shreve's Chemical Process Industries (5th ed)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="water_treatment_chemistry",
        keywords=["coagulation", "flocculation", "chlorination", "ozonation", "ion exchange", "reverse osmosis"],
        conclusion_template="Water treatment removes contaminants via coagulation (Al2(SO4)3, FeCl3), filtration, disinfection (Cl2, O3, UV), and advanced methods (ion exchange, RO) to meet drinking water standards.",
        reasoning_framework="""
1. Water sources: surface (rivers, lakes), groundwater (aquifers), desalination (seawater)
2. Contaminants: suspended solids, dissolved organics, pathogens (bacteria, viruses), heavy metals, nitrate, arsenic
3. Coagulation: add Al2(SO4)3 (alum) or FeCl3, forms Al(OH)3 or Fe(OH)3 flocs
4. Flocculation: gentle mixing, flocs grow and settle (sedimentation)
5. Filtration: sand, anthracite, activated carbon beds remove particles
6. Disinfection: kill pathogens (Cl2, ClO2, O3, UV, chloramines)
7. Chlorination: Cl2 + H2O → HOCl + HCl, HOCl (hypochlorous acid) oxidizes cell membranes
8. Breakpoint chlorination: Cl2 oxidizes NH3 → N2 (eliminates chloramine odor)
9. Residual chlorine: maintain 0.2-0.5 mg/L in distribution to prevent regrowth
10. Ozonation: O3 powerful oxidant, no residual (decomposes), oxidizes organics, kills pathogens
11. UV disinfection: 254 nm damages DNA, no chemical addition, no residual
12. Activated carbon: adsorbs organics (taste, odor, THMs, pesticides), high surface area
13. Ion exchange: cation resin (H+ or Na+) exchanges for hardness (Ca²+, Mg²+)
14. Water softening: remove Ca²+, Mg²+ (soap scum, scale), lime-soda (Ca(OH)2 + Na2CO3) or ion exchange
15. Reverse osmosis (RO): high pressure forces water through semipermeable membrane, removes ions, organics
16. Desalination: RO or multistage flash (MSF) evaporation, energy-intensive
17. Fluoridation: add NaF or H2SiF6 to 0.7 mg/L F⁻, dental health (controversial in some regions)
18. pH adjustment: lime (raise), CO2 or H2SO4 (lower), optimal pH 6.5-8.5
19. Disinfection byproducts (DBPs): chlorination of organics → THMs (chloroform), HAAs (carcinogenic)
20. Advanced oxidation: H2O2 + UV or O3 + UV → OH• (hydroxyl radical), oxidizes recalcitrant organics
""",
        key_factors=[
            "Coagulation/flocculation with Al or Fe salts",
            "Chlorination chemistry and breakpoint",
            "Ozone and UV disinfection",
            "Activated carbon adsorption",
            "Ion exchange for hardness removal",
            "RO for desalination and trace contaminant removal"
        ],
        primary_authority=[
            "Crittenden et al., MWH's Water Treatment: Principles and Design (3rd ed)",
            "Sawyer, McCarty, Parkin, Chemistry for Environmental Engineering and Science (5th ed)",
            "AWWA, Water Quality and Treatment (6th ed)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="geochemistry",
        keywords=["silicate minerals", "weathering", "carbonate system", "Eh-pH", "clay minerals", "mineral stability"],
        conclusion_template="Geochemistry applies inorganic chemistry to Earth processes: silicate weathering releases cations, carbonate equilibria control pH and CO2, Eh-pH diagrams map mineral stability, and clay formation records weathering intensity.",
        reasoning_framework="""
1. Earth's crust: 46% O, 28% Si, 8% Al, 5% Fe, 4% Ca, silicate minerals dominant
2. Silicate structure: SiO4⁴⁻ tetrahedra polymerize (nesosilicates, chains, sheets, frameworks)
3. Olivine (Mg,Fe)2SiO4: isolated SiO4, weathering: Mg2SiO4 + 4H+ → 2Mg²+ + H4SiO4
4. Pyroxene (e.g., enstatite MgSiO3): single chains, amphibole (hornblende): double chains
5. Feldspar: aluminosilicate frameworks, orthoclase KAlSi3O8, plagioclase (Na,Ca)(Al,Si)4O8
6. Weathering of orthoclase: 2KAlSi3O8 + 2H+ + 9H2O → Al2Si2O5(OH)4 (kaolinite) + 2K+ + 4H4SiO4
7. Clay minerals: sheet silicates (kaolinite 1:1, montmorillonite 2:1), cation exchange capacity
8. Chemical weathering: hydrolysis (H+ attacks silicates), oxidation (Fe²+ → Fe³+), dissolution (CaCO3)
9. Physical weathering: freeze-thaw, thermal expansion (no chemical change)
10. Soil formation: weathering intensity → kaolinite (intense, tropics), smectite (moderate), illite (low)
11. Carbonate system: CO2 + H2O ⇌ H2CO3 ⇌ H+ + HCO3- ⇌ 2H+ + CO3²⁻
12. Ocean pH buffering: CaCO3 dissolution/precipitation regulates pH ~8.1
13. Ocean acidification: rising CO2 lowers pH, threatens coral reefs (CaCO3 dissolution)
14. Eh-pH (Pourbaix) diagrams: stability fields for minerals (hematite, magnetite, pyrite)
15. Oxidizing conditions (high Eh): Fe³+ oxides (hematite Fe2O3), sulfate SO4²⁻
16. Reducing conditions (low Eh): Fe²+ minerals (siderite FeCO3), sulfide S²⁻ (pyrite FeS2)
17. Acid mine drainage: pyrite oxidation 4FeS2 + 15O2 + 14H2O → 4Fe(OH)3 + 8H2SO4 (pH <3)
18. Hydrothermal systems: hot water dissolves metals, deposits ore minerals (chalcopyrite, galena, sphalerite)
19. Metamorphic reactions: heat/pressure transform minerals (calcite + quartz → wollastonite + CO2)
20. Rock cycle: igneous (crystallize from melt) → weathering → sedimentary → metamorphic → melt → igneous
""",
        key_factors=[
            "Silicate mineral structures and weathering reactions",
            "Clay mineral formation and ion exchange",
            "Carbonate equilibria and ocean buffering",
            "Eh-pH diagrams for redox mineral stability",
            "Acid mine drainage from pyrite oxidation",
            "Hydrothermal and metamorphic geochemistry"
        ],
        primary_authority=[
            "Faure, Principles and Applications of Geochemistry (2nd ed)",
            "Krauskopf & Bird, Introduction to Geochemistry (3rd ed)",
            "Langmuir, Aqueous Environmental Geochemistry"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="spectroscopic_methods_inorganic",
        keywords=["UV-Vis", "IR", "NMR", "EPR", "Mossbauer", "XRD", "XPS"],
        conclusion_template="Spectroscopic methods characterize inorganic compounds: UV-Vis (d-d transitions, LMCT), IR (vibrational modes), NMR (diamagnetic complexes), EPR (paramagnetic metal centers), Mössbauer (Fe oxidation state), XRD (crystal structure), XPS (surface oxidation states).",
        reasoning_framework="""
1. UV-Vis spectroscopy: electronic transitions, d-d (weak, 10-100 M⁻¹cm⁻¹), charge transfer (strong, 1000-10000)
2. [Ti(H2O)6]³+ purple: d¹ → single d-d transition, λmax ~500 nm
3. [MnO4]⁻ purple: LMCT (O²⁻ → Mn⁷+), intense, λmax ~525 nm
4. Beer's law: A = ε c l, measure concentration from absorbance
5. Spectrochemical series from UV-Vis: ligand field strength order
6. IR spectroscopy: vibrational modes, ν(M-O), ν(M-N), ν(C≡O), ν(N-O)
7. Metal carbonyls: ν(CO) 1850-2100 cm⁻¹, shifts indicate backbonding strength
8. Bridging CO: lower ν(CO) ~1800 cm⁻¹ vs terminal ~2000 cm⁻¹
9. Nitrosyl complexes: linear NO+ ~1900 cm⁻¹, bent NO⁰/NO⁻ ~1600 cm⁻¹
10. NMR: nuclear spin I≠0 (¹H, ¹³C, ³¹P, ¹⁹⁵Pt), paramagnetic centers broaden/shift signals
11. ³¹P NMR: phosphine ligands, ¹⁹⁵Pt-³¹P coupling in Pt complexes
12. Paramagnetic NMR: isotropic shifts (contact, pseudocontact), line broadening
13. EPR (ESR): unpaired electrons, g-factor, hyperfine splitting (A)
14. Cu²+ (d⁹): axial EPR, g∥ > g⊥ > 2.0, hyperfine from ⁶³Cu, ⁶⁵Cu (I=3/2)
15. Mössbauer: ⁵⁷Fe, measures isomer shift (oxidation state, coordination), quadrupole splitting, magnetic splitting
16. High-spin Fe²+ vs Fe³+: isomer shift distinguishes oxidation state
17. X-ray diffraction (XRD): Bragg's law nλ = 2d sinθ, determines crystal structure, unit cell
18. Powder XRD: polycrystalline sample, diffraction pattern identifies phases
19. Single-crystal XRD: full 3D structure, bond lengths, angles
20. XPS (X-ray photoelectron spectroscopy): surface-sensitive, measures binding energy → oxidation state, chemical environment
21. Mass spectrometry: MALDI-TOF for large complexes, ESI-MS for solution species
22. Magnetometry: SQUID measures magnetic moment vs T, determines spin state, magnetic ordering
""",
        key_factors=[
            "UV-Vis: d-d vs charge-transfer transitions",
            "IR: metal-ligand stretching frequencies",
            "NMR: nuclei in diamagnetic complexes (³¹P, ¹⁹⁵Pt)",
            "EPR: g-factor and hyperfine for paramagnetic centers",
            "Mössbauer: Fe oxidation state and spin state",
            "XRD: crystal structure determination",
            "XPS: surface oxidation state analysis"
        ],
        primary_authority=[
            "Nakamoto, Infrared and Raman Spectra of Inorganic and Coordination Compounds (6th ed)",
            "Drago, Physical Methods for Chemists (2nd ed)",
            "Lever, Inorganic Electronic Spectroscopy (2nd ed)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="acid_base_concepts",
        keywords=["Bronsted", "Lewis", "HSAB", "pKa", "amphoteric", "superacid"],
        conclusion_template="Acid-base theories extend from Brønsted (H+ donor/acceptor) to Lewis (e- pair donor/acceptor) to HSAB (hard-soft matching predicts stability), explaining reactivity across molecular and ionic inorganic chemistry.",
        reasoning_framework="""
1. Arrhenius: acid produces H+ in water, base produces OH-
2. Brønsted-Lowry: acid = H+ donor, base = H+ acceptor (broader, includes non-aqueous)
3. Conjugate pairs: HCl/Cl⁻, NH4+/NH3, stronger acid → weaker conjugate base
4. pKa: -log Ka, lower pKa = stronger acid (HCl pKa ~-7, acetic acid pKa 4.76)
5. Polyprotic acids: H3PO4 → H2PO4⁻ → HPO4²⁻ → PO4³⁻ (pKa1 < pKa2 < pKa3)
6. Amphoteric: acts as acid or base (Al(OH)3, Zn(OH)2, amino acids)
7. Al(OH)3 + OH⁻ → Al(OH)4⁻ (base), Al(OH)3 + 3H+ → Al³+ + 3H2O (acid)
8. Lewis: acid = electron pair acceptor (electrophile), base = electron pair donor (nucleophile)
9. BF3 (Lewis acid) + NH3 (Lewis base) → F3B-NH3 (adduct)
10. Metal ions Lewis acids: accept lone pairs from ligands (coordination complexes)
11. HSAB (Hard-Soft Acid-Base): hard acids prefer hard bases, soft prefer soft
12. Hard acids: small, high charge, low polarizability (H+, Li+, Mg²+, Al³+, Fe³+, BF3)
13. Soft acids: large, low charge, high polarizability (Cu+, Ag+, Hg²+, Pd²+, Pt²+)
14. Hard bases: small, high electronegativity, low polarizability (F⁻, OH⁻, H2O, NH3, Cl⁻)
15. Soft bases: large, low electronegativity, high polarizability (I⁻, RS⁻, PR3, CO, alkenes)
16. Prediction: Fe³+ (hard) prefers O-donors (H2O, EDTA), Ag+ (soft) prefers S-donors (thiourea, RS⁻)
17. Superacids: stronger than 100% H2SO4 (magic acid FSO3H-SbF5, triflic acid CF3SO3H)
18. Carbocation stabilization in superacids (C5H5+ from cyclohexane)
19. Pearson hardness: η = (I - A)/2, quantifies HSAB
20. Symbiotic effect: soft-soft or hard-hard pairs stabilize, mixed destabilize (e.g., [Pt(NH3)2Cl2] more stable cis than trans)
""",
        key_factors=[
            "Brønsted vs Lewis definitions",
            "pKa scale and conjugate acid-base pairs",
            "Amphoteric behavior (Al, Zn hydroxides)",
            "HSAB theory: hard-hard, soft-soft matching",
            "Pearson hardness and symbiotic effect",
            "Superacids and carbocation chemistry"
        ],
        primary_authority=[
            "Pearson, Hard and Soft Acids and Bases",
            "Housecroft & Sharpe, Inorganic Chemistry Ch 7",
            "Cotton et al., Advanced Inorganic Chemistry Ch 5"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

]


# ============================================================================
# ENGINE TELEMETRY
# ============================================================================

@dataclass
class QueryTelemetry:
    """Comprehensive telemetry for each query."""
    query_id: str
    timestamp: str
    question: str
    mode: ResponseMode
    latency_ms: float
    doctrines_triggered: List[str]
    confidence: ConfidenceLevel
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TelemetryCollector:
    """Collects and stores query telemetry."""

    def __init__(self):
        self.queries: List[QueryTelemetry] = []
        self.start_time = time.time()

    def record_query(self, telemetry: QueryTelemetry):
        """Record a query event."""
        self.queries.append(telemetry)
        logger.info(f"Query {telemetry.query_id}: {telemetry.latency_ms:.2f}ms, confidence={telemetry.confidence}")

    def get_stats(self) -> Dict[str, Any]:
        """Aggregate statistics."""
        if not self.queries:
            return {"total_queries": 0}

        latencies = [q.latency_ms for q in self.queries]
        return {
            "total_queries": len(self.queries),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "min_latency_ms": min(latencies),
            "max_latency_ms": max(latencies),
            "uptime_seconds": time.time() - self.start_time,
            "queries_per_minute": len(self.queries) / ((time.time() - self.start_time) / 60)
        }


# ============================================================================
# DRIFT WATCHER
# ============================================================================

class DriftWatcher:
    """Monitors doctrine usage patterns over time."""

    def __init__(self):
        self.triggered_counts: Dict[str, int] = {}
        self.missed_queries: List[str] = []

    def record_trigger(self, doctrine_topic: str):
        """Record doctrine block trigger."""
        self.triggered_counts[doctrine_topic] = self.triggered_counts.get(doctrine_topic, 0) + 1

    def record_miss(self, question: str):
        """Record query with no doctrine match."""
        self.missed_queries.append(question)
        logger.warning(f"Doctrine cache miss: {question[:100]}")

    def get_coverage_report(self) -> Dict[str, Any]:
        """Generate coverage report."""
        total_doctrines = len(DOCTRINE_CACHE)
        triggered = len(self.triggered_counts)
        return {
            "total_doctrines": total_doctrines,
            "triggered_doctrines": triggered,
            "untriggered_doctrines": total_doctrines - triggered,
            "coverage_pct": (triggered / total_doctrines * 100) if total_doctrines > 0 else 0,
            "missed_queries_count": len(self.missed_queries),
            "top_triggered": sorted(self.triggered_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        }


# ============================================================================
# COVERAGE MAP
# ============================================================================

class CoverageMap:
    """Maps query patterns to doctrine blocks."""

    def __init__(self):
        self.query_doctrine_map: Dict[str, List[str]] = {}

    def record_mapping(self, question_snippet: str, doctrine_topics: List[str]):
        """Record which doctrines answered a question."""
        key = question_snippet[:100].lower()
        self.query_doctrine_map[key] = doctrine_topics

    def get_coverage_stats(self) -> Dict[str, Any]:
        """Get coverage statistics."""
        return {
            "unique_query_patterns": len(self.query_doctrine_map),
            "avg_doctrines_per_query": sum(len(v) for v in self.query_doctrine_map.values()) / len(self.query_doctrine_map) if self.query_doctrine_map else 0
        }


# ============================================================================
# QUERY ENGINE
# ============================================================================

class CHEM02Engine:
    """Inorganic Chemistry Intelligence Engine."""

    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.telemetry = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.coverage_map = CoverageMap()
        logger.info(f"CHEM02 initialized with {len(self.doctrines)} doctrine blocks")

    async def process_query(self, request: QueryRequest) -> QueryResponse:
        """Main query processing pipeline."""
        start_time = time.time()
        query_id = hashlib.sha256(f"{request.question}{time.time()}".encode()).hexdigest()[:16]

        try:
            # Match relevant doctrines
            matched_doctrines = self._match_doctrines(request.question)

            if not matched_doctrines:
                self.drift_watcher.record_miss(request.question)
                matched_doctrines = [self.doctrines[0]]  # Fallback to coordination chemistry

            # Record triggers
            for doctrine in matched_doctrines:
                self.drift_watcher.record_trigger(doctrine.topic)

            # Build response
            answer, reasoning_chain, authorities, confidence = self._build_response(
                request.question, matched_doctrines, request.mode
            )

            # Record coverage
            self.coverage_map.record_mapping(
                request.question,
                [d.topic for d in matched_doctrines]
            )

            # Determinism hash
            det_hash = hashlib.sha256(
                f"{request.question}{answer}{request.mode}".encode()
            ).hexdigest()[:16]

            latency_ms = (time.time() - start_time) * 1000

            # Telemetry
            telemetry = QueryTelemetry(
                query_id=query_id,
                timestamp=datetime.utcnow().isoformat(),
                question=request.question,
                mode=request.mode,
                latency_ms=latency_ms,
                doctrines_triggered=[d.topic for d in matched_doctrines],
                confidence=confidence
            )
            self.telemetry.record_query(telemetry)

            return QueryResponse(
                answer=answer,
                mode=request.mode,
                confidence=confidence,
                reasoning_chain=reasoning_chain,
                authorities_cited=authorities,
                determinism_hash=det_hash,
                timestamp=telemetry.timestamp,
                latency_ms=latency_ms
            )

        except Exception as e:
            logger.error(f"Query processing error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    def _match_doctrines(self, question: str) -> List[DoctrineBlock]:
        """Match question to relevant doctrine blocks."""
        question_lower = question.lower()
        matched = []

        for doctrine in self.doctrines:
            # Keyword matching
            if any(kw.lower() in question_lower for kw in doctrine.keywords):
                matched.append(doctrine)
            # Topic matching
            elif doctrine.topic.replace("_", " ") in question_lower:
                matched.append(doctrine)

        # Sort by keyword overlap
        matched.sort(
            key=lambda d: sum(1 for kw in d.keywords if kw.lower() in question_lower),
            reverse=True
        )

        return matched[:3]  # Top 3 most relevant

    def _build_response(
        self,
        question: str,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode
    ) -> tuple[str, List[str], List[str], ConfidenceLevel]:
        """Build response from matched doctrines."""

        if mode == ResponseMode.FAST:
            # Concise answer from top doctrine
            doctrine = doctrines[0]
            answer = f"{doctrine.conclusion_template}\n\nKey factors: {', '.join(doctrine.key_factors[:3])}."
            reasoning = [f"Primary doctrine: {doctrine.topic}", "Conclusion template applied"]
            authorities = doctrine.primary_authority[:1]
            confidence = doctrine.confidence

        elif mode == ResponseMode.DEFENSE:
            # Comprehensive answer with full reasoning
            parts = []
            reasoning = []
            authorities_set = set()

            for doctrine in doctrines:
                parts.append(f"**{doctrine.topic.replace('_', ' ').title()}**:\n{doctrine.conclusion_template}")
                parts.append(f"\nReasoning framework:\n{doctrine.reasoning_framework[:500]}...")
                parts.append(f"\nKey factors:\n- " + "\n- ".join(doctrine.key_factors))
                reasoning.append(f"Applied doctrine: {doctrine.topic}")
                authorities_set.update(doctrine.primary_authority)

            answer = "\n\n".join(parts)
            authorities = list(authorities_set)
            confidence = ConfidenceLevel.DEFENSIBLE

        else:  # MEMO
            # Full memo format
            parts = [
                f"# Inorganic Chemistry Analysis: {question}\n",
                "## Summary\n",
                doctrines[0].conclusion_template,
                "\n## Detailed Analysis\n"
            ]

            reasoning = []
            authorities_set = set()

            for i, doctrine in enumerate(doctrines, 1):
                parts.append(f"\n### {i}. {doctrine.topic.replace('_', ' ').title()}\n")
                parts.append(f"**Conclusion**: {doctrine.conclusion_template}\n")
                parts.append(f"**Reasoning**:\n{doctrine.reasoning_framework}\n")
                parts.append(f"**Key Factors**:\n- " + "\n- ".join(doctrine.key_factors) + "\n")
                parts.append(f"**Authorities**: {', '.join(doctrine.primary_authority)}\n")
                reasoning.append(f"Doctrine {i}: {doctrine.topic}")
                authorities_set.update(doctrine.primary_authority)

            parts.append("\n## Confidence Assessment\n")
            parts.append(f"Overall confidence: {doctrines[0].confidence.value}\n")

            answer = "".join(parts)
            authorities = list(authorities_set)
            confidence = doctrines[0].confidence

        return answer, reasoning, authorities, confidence


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="CHEM02 Inorganic Chemistry Engine",
    description="TIE-grade inorganic chemistry intelligence engine",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Global engine instance
engine = CHEM02Engine()


@APP.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    uptime = time.time() - engine.telemetry.start_time
    return HealthResponse(
        status="healthy",
        engine="CHEM02_inorganic_chemistry",
        version="1.0.0",
        port=9052,
        doctrines_loaded=len(engine.doctrines),
        uptime_seconds=uptime
    )


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint."""
    logger.info(f"Query received: {request.question[:100]}... (mode={request.mode})")
    response = await engine.process_query(request)
    return response


@APP.get("/telemetry")
async def telemetry_endpoint():
    """Get telemetry statistics."""
    return {
        "query_stats": engine.telemetry.get_stats(),
        "drift_report": engine.drift_watcher.get_coverage_report(),
        "coverage_stats": engine.coverage_map.get_coverage_stats()
    }


@APP.get("/doctrines")
async def list_doctrines():
    """List all doctrine blocks."""
    return {
        "total": len(engine.doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "key_factors_count": len(d.key_factors),
                "authorities_count": len(d.primary_authority)
            }
            for d in engine.doctrines
        ]
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting CHEM02 Inorganic Chemistry Engine on port 9052")
    uvicorn.run(APP, host="0.0.0.0", port=9052, log_level="info")
