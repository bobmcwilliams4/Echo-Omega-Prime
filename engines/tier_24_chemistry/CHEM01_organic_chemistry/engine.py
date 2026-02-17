"""
CHEM01 - Organic Chemistry Intelligence Engine
Port: 9051
Version: 1.0.0

Comprehensive organic chemistry knowledge engine covering reaction mechanisms,
functional group transformations, stereochemistry, named reactions, spectroscopy,
and industrial applications.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Literal
from enum import Enum

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "logs" / "chem01_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)

# ============================================================================
# ENUMS AND MODELS
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFINITIVE = "DEFINITIVE"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    REQUIRES_VERIFICATION = "REQUIRES_VERIFICATION"

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=5000)
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    context: Optional[Dict[str, Any]] = Field(default=None)

class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    triggered_doctrines: List[str]
    reasoning_chain: Optional[List[str]] = None
    determinism_hash: str
    timestamp: str
    telemetry: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float

# ============================================================================
# DOCTRINE BLOCKS
# ============================================================================

class DoctrineBlock:
    """Encapsulates expert organic chemistry knowledge."""

    def __init__(
        self,
        topic: str,
        keywords: List[str],
        conclusion_template: str,
        reasoning_framework: str,
        key_factors: List[str],
        primary_authority: List[str],
        confidence: ConfidenceLevel,
        mechanism_details: Optional[str] = None,
        safety_notes: Optional[str] = None
    ):
        self.topic = topic
        self.keywords = keywords
        self.conclusion_template = conclusion_template
        self.reasoning_framework = reasoning_framework
        self.key_factors = key_factors
        self.primary_authority = primary_authority
        self.confidence = confidence
        self.mechanism_details = mechanism_details
        self.safety_notes = safety_notes
        self.hit_count = 0
        self.last_triggered = None

# Define comprehensive doctrine library
DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="SN2_Nucleophilic_Substitution",
        keywords=["SN2", "nucleophile", "backside attack", "inversion", "methyl halide", "primary"],
        conclusion_template="SN2 reactions proceed via concerted backside attack with inversion of configuration. Rate depends on both nucleophile and electrophile concentration (second-order kinetics).",
        reasoning_framework="""
SN2 Mechanism Analysis:
1. Nucleophile approaches from backside (180° from leaving group)
2. Pentavalent transition state with partial bonds
3. Complete inversion of stereochemistry (Walden inversion)
4. One-step concerted process (no intermediate)
5. Rate = k[Nu][R-X]

Substrate Reactivity Order: CH3-X > 1° > 2° >> 3° (sterically hindered, no SN2)

Nucleophile Strength Factors:
- Charge: Anions > neutral species
- Electronegativity: Less electronegative = stronger Nu
- Solvent: Polar aprotic favors SN2 (doesn't solvate Nu-)
- Steric bulk: Small nucleophiles react faster

Leaving Group Quality:
- Weak bases are best LG (I⁻ > Br⁻ > Cl⁻ > F⁻)
- Resonance-stabilized anions (OTs, OMs, OTf)
- Protonation can convert poor LG to good LG (ROH → ROH2+)

Solvent Effects:
- Polar aprotic (DMSO, DMF, acetone) accelerates SN2
- Polar protic (H2O, ROH) slows SN2 via Nu⁻ solvation
- Nonpolar solvents disfavor ionic mechanisms
""",
        key_factors=[
            "Substrate sterics (methyl > 1° > 2°, no 3°)",
            "Nucleophile strength and steric bulk",
            "Leaving group ability (weak base)",
            "Solvent polarity (aprotic > protic)",
            "Stereochemical inversion (complete)",
            "Second-order kinetics",
            "No carbocation rearrangements"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 17",
            "Anslyn & Dougherty, Modern Physical Organic Chemistry (2006), Ch. 7",
            "Smith & March, March's Advanced Organic Chemistry (7th ed., 2013)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        mechanism_details="Nu:⁻ + R-X → [Nu···R···X]‡ → Nu-R + X⁻ (concerted, one step)"
    ),

    DoctrineBlock(
        topic="SN1_Nucleophilic_Substitution",
        keywords=["SN1", "carbocation", "tertiary", "racemization", "solvolysis", "ionization"],
        conclusion_template="SN1 reactions proceed via carbocation intermediate with first-order kinetics. Tertiary substrates favored. Racemization occurs at chiral centers.",
        reasoning_framework="""
SN1 Mechanism Analysis:
1. Slow ionization: R-X → R⁺ + X⁻ (rate-determining step)
2. Fast nucleophilic attack from both faces
3. Racemization at chiral centers (planar carbocation)
4. Carbocation rearrangements possible (1,2-hydride/alkyl shifts)
5. Rate = k[R-X] (first-order, independent of [Nu])

Substrate Reactivity Order: 3° > 2° >> 1° > CH3 (follows carbocation stability)

Carbocation Stability:
- Hyperconjugation: More alkyl groups = more stable
- Resonance: Allylic/benzylic cations highly stabilized
- Inductive effects: Electron-donating groups stabilize
- Order: 3° > 2° > 1° > CH3⁺ (methyl almost never forms)

Solvent Effects:
- Polar protic solvents (H2O, ROH) stabilize ions, accelerate SN1
- Ionizing power crucial (Y-scale: TFE > HFIP > EtOH > H2O)
- Polar aprotic solvents less effective for SN1

Competing Processes:
- E1 elimination (same intermediate, high temp favors)
- Carbocation rearrangements to more stable forms
- Wagner-Meerwein shifts in cyclic systems

Stereochemistry:
- Racemization (50/50 mixture) for isolated chiral center
- Partial inversion if intimate ion pair hasn't separated
- Neighboring group participation can give retention
""",
        key_factors=[
            "Carbocation stability (3° > 2° > 1°)",
            "First-order kinetics (rate independent of Nu)",
            "Polar protic solvent required",
            "Racemization at chiral centers",
            "Carbocation rearrangements possible",
            "Competes with E1 elimination",
            "No reaction at methyl or 1° substrates"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 17",
            "Carroll, Perspectives on Structure and Mechanism in Organic Chemistry (2nd ed., 2010)",
            "Lowry & Richardson, Mechanism and Theory in Organic Chemistry (3rd ed., 1987)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        mechanism_details="Step 1: R-X → R⁺ + X⁻ (slow). Step 2: R⁺ + Nu → R-Nu (fast, from both faces)"
    ),

    DoctrineBlock(
        topic="E2_Elimination",
        keywords=["E2", "elimination", "anti-periplanar", "alkene", "strong base", "Zaitsev"],
        conclusion_template="E2 elimination requires anti-periplanar geometry of H and leaving group. Strong bases favor E2. Zaitsev rule predicts major product (most substituted alkene) unless steric hindrance dictates Hofmann.",
        reasoning_framework="""
E2 Mechanism Analysis:
1. Concerted one-step process (no intermediate)
2. Anti-periplanar geometry required (H and LG 180° apart)
3. Base removes β-hydrogen as LG departs
4. Double bond forms simultaneously
5. Rate = k[Base][R-X] (second-order)

Stereoelectronic Requirements:
- Anti-periplanar conformation mandatory (H-C-C-X dihedral = 180°)
- Syn elimination rare, requires special constraints
- Rigid cyclic systems: H must be trans-diaxial to LG
- Cyclohexanes: LG must be axial for E2

Regioselectivity:
- Zaitsev rule: More substituted alkene favored (thermodynamic product)
- Hofmann rule: Less substituted alkene with bulky base (steric)
- Bulky bases (t-BuOK, LDA) give Hofmann product
- Small bases (EtO⁻, OH⁻) give Zaitsev product

Base Strength and Substrate:
- Strong bases (NaH, LDA, t-BuOK) promote E2 over SN2
- Tertiary substrates favor E2 over SN2
- High temperature shifts equilibrium toward elimination

Stereochemistry:
- Anti-elimination gives E-alkene (trans)
- Syn-elimination (rare) gives Z-alkene (cis)
- E/Z ratio depends on substrate substitution pattern
""",
        key_factors=[
            "Anti-periplanar geometry required",
            "Concerted one-step mechanism",
            "Strong base favors elimination",
            "Zaitsev vs Hofmann regioselectivity",
            "Axial LG required in cyclohexanes",
            "Competes with SN2 for 1°/2° substrates",
            "Second-order kinetics"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 19",
            "Smith & March, March's Advanced Organic Chemistry (7th ed., 2013)",
            "Carey & Sundberg, Advanced Organic Chemistry Part A (5th ed., 2007)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        mechanism_details="Base abstracts β-H as C-X bond breaks and C=C forms (concerted)"
    ),

    DoctrineBlock(
        topic="Grignard_Reagent_Chemistry",
        keywords=["Grignard", "RMgX", "nucleophile", "carbonyl addition", "ether", "anhydrous"],
        conclusion_template="Grignard reagents (RMgX) are powerful carbon nucleophiles that add to carbonyls. Require anhydrous conditions and inert atmosphere. React with aldehydes, ketones, esters, CO2, epoxides.",
        reasoning_framework="""
Grignard Reagent Preparation and Use:
1. Formation: R-X + Mg → R-MgX (in dry Et2O or THF)
2. Highly nucleophilic carbon (carbanion character)
3. Strong base (pKa ~50 for conjugate acid R-H)
4. Moisture-sensitive (destroyed by H2O, ROH, RCOOH)

Reactivity with Carbonyls:
- Formaldehyde → 1° alcohol (after H3O⁺ workup)
- Higher aldehydes → 2° alcohols
- Ketones → 3° alcohols
- CO2 → carboxylic acids (after acidic workup)
- Esters → 3° alcohols (two equiv RMgX adds)
- Acyl chlorides → 3° alcohols (via ketone intermediate)

Mechanism:
1. Nucleophilic addition to C=O
2. Tetrahedral alkoxide intermediate
3. Aqueous acid workup protonates alkoxide
4. No loss of Mg until workup

Side Reactions and Limitations:
- Enolization of ketones (competing deprotonation)
- Reduction of ketones to alcohols (via β-hydride transfer)
- Proton abstraction from acidic H (R-H pKa < 25)
- Incompatible with: NH, OH, SH, COOH, NO2, CN, C=C-CO

Protective Strategies:
- Protect acidic groups (acetals for carbonyls, silyl ethers for OH)
- Use Grignard at low temp to minimize enolization
- Order of addition matters (add Grignard to carbonyl, not reverse)

Variants:
- Alkyllithium reagents (RLi) even more reactive
- Organocerium reagents (RCeCl2) less basic, reduce enolization
- Organozinc reagents (R2Zn) milder, more selective
""",
        key_factors=[
            "Requires anhydrous conditions (no H2O, ROH)",
            "Strong nucleophile and strong base",
            "Adds to aldehydes, ketones, esters, CO2",
            "Two equiv add to esters (→ 3° alcohol)",
            "Incompatible with acidic protons",
            "Formed in ether solvents (Et2O, THF)",
            "Workup with H3O⁺ to protonate alkoxide"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 9",
            "Wakefield, Organomagnesium Methods in Organic Synthesis (1995)",
            "Rappoport & Marek, The Chemistry of Organolithium Compounds (2004)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        mechanism_details="R-MgX + R'CHO → R'CH(O-MgX)R → (H3O⁺) → R'CH(OH)R",
        safety_notes="Grignard reagents pyrophoric (ignite in air). Handle under inert atmosphere (N2 or Ar). Exothermic reaction with water/acids."
    ),

    DoctrineBlock(
        topic="Wittig_Reaction",
        keywords=["Wittig", "ylide", "phosphonium", "alkene synthesis", "olefination", "carbonyl"],
        conclusion_template="Wittig reaction converts carbonyls to alkenes via phosphonium ylide. Stabilized ylides give E-alkenes; unstabilized ylides give Z-alkenes. Tolerates many functional groups.",
        reasoning_framework="""
Wittig Reaction Mechanism and Scope:
1. Ylide formation: Ph3P + R-X → [Ph3P⁺-R]X⁻ → (base) → Ph3P=CR2
2. [2+2] cycloaddition with C=O → oxaphosphetane intermediate
3. Retro-[2+2] → alkene + Ph3P=O (driving force)

Ylide Types and Stereoselectivity:
- Unstabilized ylides (R = alkyl): Z-selective (kinetic control)
  Mechanism: cis-oxaphosphetane forms faster
- Stabilized ylides (R = CO2R, COR, CN): E-selective (thermodynamic control)
  Mechanism: reversible, trans-oxaphosphetane more stable
- Semi-stabilized ylides: mixture of E/Z

Ylide Generation:
- Strong base (n-BuLi, NaH, t-BuOK) for unstabilized ylides
- Weaker base (NaOEt, K2CO3) sufficient for stabilized ylides
- Deprotonation α to P⁺ (pKa ~15-20 depending on substitution)

Substrate Scope:
- Aldehydes: excellent reactivity, high yields
- Ketones: slower, may require forcing conditions
- Esters, amides: unreactive (less electrophilic)
- α,β-Unsaturated carbonyls: 1,2-addition (not 1,4)

Advantages and Limitations:
+ Mild conditions, wide functional group tolerance
+ Predictable regiochemistry (C=O becomes C=C)
+ Stable ylides can be isolated and stored
- Ph3P=O byproduct difficult to remove
- Unstabilized ylides air/moisture sensitive
- Limited to terminal or monosubstituted alkenes from aldehydes

Modern Variants:
- Horner-Wadsworth-Emmons (HWE): phosphonate esters, E-selective, easier workup
- Still-Gennari: E-selective HWE variant
- Ando modification: Z-selective HWE
""",
        key_factors=[
            "Ylide stabilization controls E/Z selectivity",
            "Unstabilized ylides → Z-alkenes",
            "Stabilized ylides → E-alkenes",
            "Ph3P=O drives reaction (strong P=O bond)",
            "Aldehydes more reactive than ketones",
            "Functional group tolerant",
            "HWE variant gives easier purification"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 14",
            "Maryanoff & Reitz, Chem. Rev. 1989, 89, 863 (comprehensive review)",
            "Nicolaou & Sorensen, Classics in Total Synthesis (1996)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        mechanism_details="Ph3P=CHR + R'CHO → [Ph3P-CHR-O-CHR'] → R'CH=CHR + Ph3P=O"
    ),

    DoctrineBlock(
        topic="Diels_Alder_Reaction",
        keywords=["Diels-Alder", "cycloaddition", "diene", "dienophile", "endo", "retro-Diels-Alder"],
        conclusion_template="Diels-Alder is [4+2] cycloaddition forming cyclohexenes. Concerted, stereospecific, endo-selective. Electron-rich diene + electron-poor dienophile optimal.",
        reasoning_framework="""
Diels-Alder Cycloaddition Mechanism:
1. Concerted [4+2] cycloaddition (pericyclic reaction)
2. Six-electron aromatic transition state
3. Suprafacial with respect to both components
4. Thermal reaction (Δ), photochemical [2+2] different
5. Reversible at high temp (retro-Diels-Alder)

Frontier Molecular Orbital Analysis:
- HOMO(diene) - LUMO(dienophile) interaction dominant
- Electron-donating groups on diene (EDG) raise HOMO
- Electron-withdrawing groups on dienophile (EWG) lower LUMO
- Optimal: EDG-diene + EWG-dienophile (normal electron demand)
- Inverse demand possible: EWG-diene + EDG-dienophile

Stereochemistry:
- Endo rule: EWG on dienophile points toward diene (secondary orbital overlap)
- Endo product kinetic (faster forming)
- Exo product thermodynamic (more stable, less steric clash)
- Syn addition to both components (suprafacial-suprafacial)
- Relative stereochemistry preserved from starting materials

Diene Requirements:
- s-cis conformation required (s-trans cannot react)
- Cyclic dienes (cyclopentadiene, furan) locked in s-cis, highly reactive
- Acyclic dienes may need heating to populate s-cis
- Bulky substituents disfavor s-cis, slow reaction

Regioselectivity:
- 1,2-disubstituted alkenes: ortho/para directing
- 1,1-disubstituted alkenes: meta directing
- Can be predicted by matching partial charges (HOMO/LUMO coefficients)

Catalysis and Variants:
- Lewis acids (AlCl3, BF3, TiCl4) activate dienophile, increase rate
- High pressure accelerates reaction (ΔV‡ negative)
- Hetero-Diels-Alder: O, N, S in diene or dienophile
- Intramolecular DA: excellent for fused/bridged rings
""",
        key_factors=[
            "Concerted [4+2] cycloaddition",
            "Diene must be in s-cis conformation",
            "Endo selectivity (kinetic product)",
            "Suprafacial-suprafacial geometry",
            "EDG-diene + EWG-dienophile optimal",
            "Stereospecific (geometry preserved)",
            "Reversible at high temperature"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 35",
            "Fleming, Molecular Orbitals and Organic Chemical Reactions (2010)",
            "Nicolaou & Snyder, Classics in Total Synthesis (2003)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        mechanism_details="Concerted asynchronous transition state, aromatic 6e⁻ Hückel system"
    ),

    DoctrineBlock(
        topic="Aldol_Condensation",
        keywords=["aldol", "enolate", "β-hydroxy carbonyl", "crossed aldol", "dehydration", "α,β-unsaturated"],
        conclusion_template="Aldol reaction forms β-hydroxy carbonyls via enolate addition to aldehyde/ketone. Dehydration yields α,β-unsaturated carbonyls. Crossed aldol requires one non-enolizable partner.",
        reasoning_framework="""
Aldol Reaction Mechanism and Variants:
1. Enolate formation: Base abstracts α-proton (pKa ~20)
2. Nucleophilic addition to carbonyl C=O
3. Protonation of alkoxide → β-hydroxy carbonyl
4. Optional dehydration (acid or heat) → α,β-unsaturated carbonyl

Base-Catalyzed Aldol:
- Base: NaOH, NaOEt, LDA
- Enolate adds to carbonyl partner
- Reversible, thermodynamic control
- E1cb elimination if heated (dehydration)

Acid-Catalyzed Aldol:
- Enol (not enolate) is nucleophile
- Carbonyl activated by protonation
- Irreversible dehydration under acidic conditions
- Less common for synthesis (mixed products)

Regioselectivity (Unsymmetric Ketones):
- Kinetic enolate: LDA, -78°C, less substituted α-carbon
- Thermodynamic enolate: NaH, reflux, more substituted α-carbon
- Kinetic faster (less steric hindrance)
- Thermodynamic more stable (better conjugation)

Crossed Aldol Strategies:
- One partner non-enolizable (no α-H): formaldehyde, benzaldehyde, ArCHO
- Enolate preformed, then add electrophile (directed aldol)
- Mukaiyama aldol: silyl enol ether + Lewis acid
- Avoid statistical mixtures (4 products from two enolizable ketones)

Stereochemistry:
- Syn/anti selectivity from chair-like Zimmerman-Traxler TS
- Lithium enolates (LDA): kinetic, Z-enolate → syn-aldol
- Boron enolates (R2BCl + Et3N): excellent syn selectivity
- Anti-aldol possible with E-enolate or chelation control

Intramolecular Aldol (Robinson Annulation):
- Excellent for ring formation (5-, 6-membered favored)
- Dehydration spontaneous (conjugation drives)
- Key step in steroid synthesis
""",
        key_factors=[
            "Enolate (or enol) adds to carbonyl",
            "Forms β-hydroxy carbonyl (or α,β-unsaturated)",
            "Crossed aldol needs non-enolizable partner",
            "Kinetic vs thermodynamic enolate control",
            "Zimmerman-Traxler TS predicts syn/anti",
            "Intramolecular version excellent for rings",
            "Reversible under base (irreversible if dehydrated)"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 27",
            "Evans, Asymmetric Synthesis, Vol. 3 (1984)",
            "Heathcock, Comp. Org. Syn., Vol. 2 (1991)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        mechanism_details="Enolate + RCHO → R-CH(O⁻)-CH2-COR' → (H⁺) → R-CH(OH)-CH2-COR'"
    ),

    DoctrineBlock(
        topic="Protecting_Groups_Strategy",
        keywords=["protecting group", "acetal", "silyl ether", "BOC", "Fmoc", "orthogonal"],
        conclusion_template="Protecting groups temporarily mask reactive functional groups. Must be stable to reaction conditions but removable under orthogonal conditions. Common: acetals (aldehydes/ketones), silyl ethers (alcohols), BOC/Fmoc (amines).",
        reasoning_framework="""
Protecting Group Strategy and Selection:
1. Identify functional groups needing protection
2. Select PG stable to planned reaction conditions
3. Install PG with high yield, no side reactions
4. Perform target transformations
5. Remove PG under orthogonal conditions (not affecting product)

Alcohol Protection:
- TMS (trimethylsilyl): very labile, fluoride cleaved (TBAF)
- TBS (tert-butyldimethylsilyl): moderate stability, fluoride cleaved
- TIPS (triisopropylsilyl): stable, fluoride cleaved
- TBDPS (tert-butyldiphenylsilyl): very stable, fluoride cleaved
- Benzyl (Bn): acid-stable, removed by hydrogenolysis (H2/Pd)
- PMB (p-methoxybenzyl): removed by DDQ or CAN oxidation
- Acetate: base/acid labile, mild
- Order of stability: TBDPS > TIPS > TBS > TMS

Carbonyl Protection (Aldehydes/Ketones):
- Acetals: acid-labile, base-stable (ethylene glycol + TsOH)
- Dithianes: thioacetals, desulfurization (Raney Ni) or oxidation (NBS)
- 1,3-Dithiane: umpolung reagent (nucleophilic acyl anion equivalent)

Amine Protection:
- BOC (tert-butoxycarbonyl): TFA cleaved, base-stable
- Fmoc (fluorenylmethoxycarbonyl): base-labile (piperidine), acid-stable
- Cbz (benzyloxycarbonyl): H2/Pd cleaved, acid-stable
- Ts (tosyl): harsh removal, but very stable
- Orthogonal: BOC/Fmoc pair for solid-phase synthesis

Carboxylic Acid Protection:
- Methyl/ethyl ester: base hydrolysis
- tert-Butyl ester: acid cleaved (TFA), base-stable
- Benzyl ester: hydrogenolysis (H2/Pd)
- Allyl ester: Pd(0) isomerization then hydrolysis

Orthogonality Principles:
- Multiple PGs must be removable independently
- Peptide synthesis: Fmoc (temporary) + Boc/Bn (semi-permanent)
- Solid-phase synthesis: linker cleavage orthogonal to side-chain PGs
- Plan removal order (most labile → most stable)

Common Pitfalls:
- Steric hindrance slows PG installation/removal
- Migration of PGs (especially silyl groups under acidic/basic conditions)
- Incomplete removal leaves trace PG (affects characterization)
- Over-protection (unnecessary PGs reduce efficiency)
""",
        key_factors=[
            "Stable to reaction conditions",
            "Removable under orthogonal conditions",
            "High-yielding installation and removal",
            "Common alcohol PGs: silyl ethers, benzyl",
            "Common amine PGs: BOC, Fmoc, Cbz",
            "Acetal protection for carbonyls",
            "Orthogonal sets for complex syntheses"
        ],
        primary_authority=[
            "Wuts & Greene, Greene's Protective Groups in Organic Synthesis (5th ed., 2014)",
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 24",
            "Kocieński, Protecting Groups (3rd ed., 2004)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        mechanism_details="Varies by PG: silyl ethers (fluoride), acetals (H3O⁺), BOC (TFA), Fmoc (piperidine)"
    ),

    DoctrineBlock(
        topic="Oxidation_Reactions_Alcohols",
        keywords=["oxidation", "PCC", "PDC", "Swern", "DMP", "Jones", "chromium", "alcohol"],
        conclusion_template="Alcohol oxidation: 1° → aldehyde (mild) or COOH (strong); 2° → ketone; 3° no reaction. PCC/PDC stop at aldehyde; Jones/KMnO4 go to acid. Swern/DMP mild and selective.",
        reasoning_framework="""
Alcohol Oxidation Reagents and Selectivity:
1. Primary alcohols: RCH2OH → RCHO → RCOOH
2. Secondary alcohols: R2CHOH → R2C=O
3. Tertiary alcohols: R3COH → no oxidation (no α-H)

Chromium-Based Oxidants:
- Jones reagent (CrO3/H2SO4/H2O): strong, 1° → COOH, 2° → ketone
- PCC (pyridinium chlorochromate): stops at aldehyde (anhydrous, CH2Cl2)
- PDC (pyridinium dichromate): similar to PCC, slightly milder
- Mechanism: chromate ester intermediate, β-hydride elimination

Swern Oxidation:
- Reagents: (COCl)2 + DMSO, then Et3N
- Very mild, stops at aldehyde/ketone
- No overoxidation, high yields
- Mechanism: alkoxysulfonium ion, then elimination
- Procedure: -78°C for activation, then warm to RT

Dess-Martin Periodinane (DMP):
- Hypervalent iodine reagent (I(V) species)
- Extremely mild, neutral pH, room temperature
- Stops at aldehyde/ketone, no overoxidation
- Expensive but reliable, used in complex molecule synthesis
- Byproduct: iodobenzoic acid (easily removed)

Parikh-Doering Oxidation:
- SO3•pyridine + DMSO + Et3N
- Milder variant of Swern
- Room temperature, no COCl2

TEMPO Oxidations:
- TEMPO (2,2,6,6-tetramethylpiperidine-N-oxyl) + bleach or PhI(OAc)2
- Catalytic in TEMPO, eco-friendly
- Selective for 1° alcohols over 2° (steric)
- Aqueous or organic conditions

Selective Oxidation Strategies:
- Allylic/benzylic alcohols: MnO2 (very selective, mild)
- Selective 1° vs 2°: TEMPO, MnO2 (steric discrimination)
- Large-scale: bleach + TEMPO (industrial)
- Sensitive substrates: DMP, Swern (no acidic/basic conditions)

Functional Group Compatibility:
- Alkenes: MnO2, DMP, Swern (avoid KMnO4, Jones)
- Alkynes: PCC, DMP (avoid strong oxidants)
- Esters, amides: compatible with most mild oxidants
- Ethers: generally compatible
""",
        key_factors=[
            "1° alcohols → aldehydes (mild) or acids (strong)",
            "2° alcohols → ketones",
            "3° alcohols not oxidized (no α-H)",
            "PCC/PDC stop at aldehyde (anhydrous)",
            "Swern/DMP very mild, no overoxidation",
            "Jones/KMnO4 strong, 1° → COOH",
            "TEMPO catalytic, eco-friendly"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 24",
            "Smith & March, March's Advanced Organic Chemistry (7th ed., 2013)",
            "Tojo & Fernández, Oxidation of Alcohols to Aldehydes and Ketones (2006)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        mechanism_details="PCC: chromate ester → elimination. Swern: DMSO-oxalyl chloride → alkoxysulfonium → E2.",
        safety_notes="Chromium reagents toxic/carcinogenic (waste disposal). Swern uses COCl2 (highly toxic gas, handle in hood)."
    ),

    DoctrineBlock(
        topic="Reduction_Reactions_Carbonyls",
        keywords=["reduction", "LiAlH4", "NaBH4", "DIBAL", "hydride", "carbonyl", "selectivity"],
        conclusion_template="Carbonyl reduction: LiAlH4 reduces all C=O (strong); NaBH4 selective for aldehydes/ketones (mild); DIBAL stops esters at aldehyde. Hydride donors add nucleophilically to C=O.",
        reasoning_framework="""
Hydride Reduction Reagents and Selectivity:
1. LiAlH4 (lithium aluminum hydride): very strong, reduces C=O, COOR, CONR2, CN
2. NaBH4 (sodium borohydride): mild, reduces aldehydes/ketones only
3. DIBAL (diisobutylaluminum hydride): reduces esters to aldehydes at -78°C
4. BH3 or BH3•THF: reduces carbonyls and alkenes

LiAlH4 Characteristics:
- Powerful hydride donor (H⁻)
- Reacts violently with H2O, ROH, RCOOH (proton sources)
- Requires ether solvent (Et2O, THF), anhydrous conditions
- Reduces: aldehydes → 1° alcohols, ketones → 2° alcohols
- Reduces esters → 1° alcohols (via aldehyde intermediate)
- Reduces amides → amines
- Reduces nitriles → primary amines
- Workup: careful addition of water (exothermic, H2 gas)

NaBH4 Characteristics:
- Milder hydride donor (less reactive)
- Stable to water, can be used in aqueous alcoholic solutions
- Reduces aldehydes/ketones → alcohols
- Does NOT reduce esters, amides, carboxylic acids, nitriles
- Excellent chemoselectivity (aldehydes/ketones in presence of COOR)
- Workup: simple aqueous quench

DIBAL Selectivity:
- Bulky aluminum hydride (Al-H bond)
- Reduces esters to aldehydes at -78°C (1 equiv)
- Reduces nitriles to aldehydes
- Reduces amides to aldehydes
- Over-reduction to alcohol if warmed or excess reagent
- Quench: Rochelle salt (potassium sodium tartrate) to break Al complex

Other Reducing Agents:
- L-Selectride (LiB(sec-Bu)3H): stereoselective ketone reduction (axial alcohol)
- K-Selectride (KB(sec-Bu)3H): stereoselective (equatorial alcohol)
- Red-Al (NaAlH2(OCH2CH2OMe)2): similar to LiAlH4, more soluble
- Super-Hydride (LiBEt3H): very powerful, reduces hindered ketones

Catalytic Hydrogenation:
- H2 + metal catalyst (Pd/C, Pt, Ni)
- Reduces C=C, C≡C, C=O (less common), aromatics (harsh), nitro → amine
- Heterogeneous (Pd/C) or homogeneous (Wilkinson's catalyst)
- Syn addition to C=C (both H from same face)

Stereochemistry and Selectivity:
- Hydride adds from less hindered face
- Cyclohexanones: axial attack (equatorial alcohol, sterics)
- Bulky reducing agents enhance selectivity
- Chelation control possible (Cram's rule, Felkin-Anh model)
""",
        key_factors=[
            "LiAlH4 reduces all C=O, COOR, CONR2, CN",
            "NaBH4 selective: aldehydes/ketones only",
            "DIBAL reduces esters to aldehydes (-78°C)",
            "LiAlH4 requires anhydrous conditions",
            "NaBH4 can be used in H2O/ROH",
            "Hydride attacks less hindered face",
            "Catalytic hydrogenation reduces C=C, C=O"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 24",
            "Seyden-Penne, Reductions by the Alumino- and Borohydrides (1997)",
            "Smith & March, March's Advanced Organic Chemistry (7th ed., 2013)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        mechanism_details="H⁻ adds to C=O, tetrahedral intermediate, protonation on workup",
        safety_notes="LiAlH4 pyrophoric (ignites in air), violent with water. Always add to solvent, never solvent to LiAlH4."
    ),

    DoctrineBlock(
        topic="Electrophilic_Aromatic_Substitution",
        keywords=["EAS", "aromatic", "benzene", "electrophile", "nitration", "halogenation", "Friedel-Crafts"],
        conclusion_template="Electrophilic aromatic substitution (EAS) adds electrophile to benzene ring. Mechanism: σ-complex (arenium ion) intermediate. Substituent effects: activating/deactivating and ortho/para vs meta directing.",
        reasoning_framework="""
EAS Mechanism and Reactivity:
1. Generation of electrophile (E⁺)
2. Electrophile attacks aromatic π-system
3. σ-Complex (arenium ion, Wheland intermediate) forms
4. Deprotonation restores aromaticity
5. Rate-determining step: formation of σ-complex

Common EAS Reactions:
- Nitration: HNO3 + H2SO4 → NO2⁺ (nitronium ion)
- Sulfonation: SO3 + H2SO4 → SO3H (reversible, thermodynamic control)
- Halogenation: X2 + FeX3 → X⁺ (Br2/FeBr3 or Cl2/AlCl3)
- Friedel-Crafts Alkylation: R-X + AlCl3 → R⁺ (carbocation)
- Friedel-Crafts Acylation: RCOCl + AlCl3 → RCO⁺ (acylium ion)

Substituent Effects (Directing and Activation):
Ortho/Para Directors (electron-donating):
- OH, OR (strongly activating, resonance donors)
- NH2, NHR, NR2 (strongly activating)
- Alkyl groups (weakly activating, inductive donors)
- Halogen (weakly deactivating but o/p directing, resonance donor)

Meta Directors (electron-withdrawing):
- NO2, CN, SO3H, COOH, COR, CHO (strongly deactivating)
- NR3⁺ (quaternary ammonium, strongly deactivating)
- CF3 (inductive withdrawing)

Activating Groups:
- Donate electron density to ring (resonance or inductive)
- Stabilize σ-complex intermediate
- Increase reaction rate

Deactivating Groups:
- Withdraw electron density from ring
- Destabilize σ-complex
- Decrease reaction rate

Halogen Paradox:
- Halogens deactivate (inductive withdrawal) but direct o/p (resonance donation)
- Resonance effect controls regiochemistry
- Inductive effect controls reactivity

Friedel-Crafts Limitations:
- Cannot be done on strongly deactivated rings (NO2, NR3⁺, etc.)
- Alkylation gives carbocation rearrangements
- Alkylation gives polyalkylation (product more reactive than starting material)
- Acylation no rearrangement (acylium ion stable)
- Acylation stops at mono (acyl group deactivating)

Multiple Substituents:
- Activating group dominates directing over deactivating
- Two o/p directors on opposite sides → meta to both (steric)
- Ipso substitution possible (replaces existing substituent)
""",
        key_factors=[
            "σ-Complex (arenium ion) intermediate",
            "Electrophile attacks aromatic ring",
            "Substituents control rate and regiochemistry",
            "EDG → o/p directing, activating",
            "EWG → m-directing, deactivating",
            "Halogens: deactivating but o/p directing",
            "Friedel-Crafts fails on deactivated rings"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 22",
            "Smith & March, March's Advanced Organic Chemistry (7th ed., 2013)",
            "Carey & Sundberg, Advanced Organic Chemistry Part A (5th ed., 2007)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        mechanism_details="E⁺ + ArH → [Ar-H-E]⁺ (σ-complex) → ArE + H⁺"
    ),

    DoctrineBlock(
        topic="Nucleophilic_Aromatic_Substitution",
        keywords=["SNAr", "Meisenheimer complex", "electron-withdrawing", "nitro", "fluoride", "nucleophile"],
        conclusion_template="Nucleophilic aromatic substitution (SNAr) requires electron-withdrawing groups (NO2, CN) ortho/para to leaving group. Mechanism: addition-elimination via Meisenheimer complex.",
        reasoning_framework="""
SNAr Mechanism and Requirements:
1. Nucleophile attacks aromatic carbon (ipso position)
2. Meisenheimer complex (anionic σ-complex) forms
3. Leaving group departs, restoring aromaticity
4. Rate-determining step: nucleophile addition (step 1)

Substrate Requirements:
- Strong electron-withdrawing groups (EWG) required
- EWG must be ortho or para to LG (stabilize negative charge)
- Multiple EWGs increase reactivity
- Best LG: F > Cl > Br > I (opposite of aliphatic, F stabilizes Meisenheimer)

Activating Groups for SNAr:
- NO2 (nitro): strongest activator, resonance stabilization
- CN (cyano): strong activator
- COR, CHO (carbonyl): good activators
- SO2R (sulfone): good activator
- CF3 (trifluoromethyl): inductive activation

Nucleophiles:
- Alkoxides (RO⁻), phenoxides (ArO⁻)
- Amines (NH3, RNH2, R2NH)
- Thiols (RS⁻)
- Carbanions (weaker nucleophiles sufficient due to activated ring)

Leaving Groups:
- Fluoride best (most electronegative, stabilizes Meisenheimer)
- Chloride, bromide acceptable
- Iodide poorest (least stabilizing)
- Other LG: NO2, OTs, OMs (if sufficiently activated)

Special Cases:
- 2,4-Dinitrofluorobenzene (Sanger's reagent): very reactive, labels amino acids
- Picryl chloride (2,4,6-trinitro): extremely reactive SNAr substrate
- Heteroaromatic rings (pyridine, pyrimidine): activate SNAr at certain positions

Comparison to EAS:
- SNAr: nucleophile attacks, EWG activates
- EAS: electrophile attacks, EDG activates
- Opposite electronic requirements
- SNAr requires harsh conditions (heat, strong Nu)
- EAS mild conditions for activated substrates

Variants:
- SRN1 mechanism: radical anion intermediate (stimulated by light)
- Benzyne mechanism: very strong base, elimination-addition via benzyne
- VNS (vicarious nucleophilic substitution): H replaced, not LG
""",
        key_factors=[
            "Addition-elimination mechanism",
            "Meisenheimer complex intermediate",
            "EWG ortho/para to LG required",
            "Fluoride best leaving group",
            "NO2, CN strongly activate",
            "Opposite activation vs EAS",
            "Harsh conditions (heat, strong Nu)"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 23",
            "Smith & March, March's Advanced Organic Chemistry (7th ed., 2013)",
            "Terrier, Modern Nucleophilic Aromatic Substitution (2013)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        mechanism_details="Nu⁻ + Ar-X → [Nu-Ar-X]⁻ (Meisenheimer) → Nu-Ar + X⁻"
    ),

    DoctrineBlock(
        topic="Stereochemistry_Chirality",
        keywords=["stereochemistry", "chirality", "enantiomer", "diastereomer", "R/S", "optical rotation"],
        conclusion_template="Chirality: molecule non-superimposable on mirror image. Enantiomers are mirror images; diastereomers are non-mirror stereoisomers. R/S nomenclature by Cahn-Ingold-Prelog priority rules.",
        reasoning_framework="""
Stereochemistry Fundamentals and Classification:
1. Stereoisomers: same connectivity, different 3D arrangement
2. Enantiomers: non-superimposable mirror images (equal/opposite optical rotation)
3. Diastereomers: stereoisomers that are NOT mirror images
4. Meso compounds: achiral despite having stereocenters (internal plane of symmetry)

Chirality Requirements:
- No plane of symmetry (achiral if σ-plane present)
- No center of inversion (i)
- No improper rotation axis (Sn)
- Most common: tetrahedral carbon with 4 different substituents (stereocenter)
- Other: axial chirality (allenes, BINOL), planar chirality, helical chirality

Cahn-Ingold-Prelog R/S Nomenclature:
1. Assign priority to substituents (1 = highest, 4 = lowest)
   - Priority by atomic number (higher Z = higher priority)
   - If tied, go to next atom (isotopes by mass number)
2. Orient molecule so lowest priority (4) points away
3. Trace path 1→2→3
4. Clockwise = R (rectus), counterclockwise = S (sinister)

Fischer Projections:
- Horizontal bonds project forward (wedges)
- Vertical bonds project back (dashes)
- Rotation by 90° inverts configuration
- Rotation by 180° preserves configuration
- Switching two groups inverts configuration

Optical Activity:
- Enantiomers rotate plane-polarized light equally but opposite directions
- (+) dextrorotatory (d), (-) levorotatory (l)
- Racemic mixture: 50:50 enantiomers, no net rotation
- Specific rotation: [α] = α/(l·c) (α = observed, l = path length dm, c = g/mL)
- Configuration (R/S) does NOT predict rotation sign (+/-)

Multiple Stereocenters:
- n stereocenters → max 2ⁿ stereoisomers (unless symmetry)
- Diastereomers have different physical properties (BP, MP, solubility, Rf)
- Enantiomers identical physical properties except optical rotation
- Meso compounds reduce number of stereoisomers (internal symmetry)

Strategies for Assignment:
- Build model (physical or mental visualization)
- Fischer projections for sugars/amino acids
- Newman projections for conformational analysis
- Use wedge-dash notation for clarity
""",
        key_factors=[
            "Enantiomers: mirror images, opposite rotation",
            "Diastereomers: non-mirror stereoisomers",
            "R/S by Cahn-Ingold-Prelog priority rules",
            "Chirality requires no symmetry plane",
            "Meso: achiral despite stereocenters",
            "n stereocenters → max 2ⁿ stereoisomers",
            "Optical rotation independent of R/S"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 16",
            "Eliel & Wilen, Stereochemistry of Organic Compounds (1994)",
            "Anslyn & Dougherty, Modern Physical Organic Chemistry (2006)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE
    ),

    DoctrineBlock(
        topic="Retrosynthetic_Analysis",
        keywords=["retrosynthesis", "disconnection", "synthon", "FGA", "umpolung", "Corey"],
        conclusion_template="Retrosynthetic analysis: work backward from target to available starting materials. Identify disconnections, synthons, and functional group interconversions (FGI). Transform retrosynthetic arrows into forward synthetic steps.",
        reasoning_framework="""
Retrosynthetic Analysis Strategy (Corey's Approach):
1. Identify target molecule structure and functionality
2. Work backward (retrosynthetic arrow ⇒)
3. Simplify via disconnections (break C-C or C-X bonds)
4. Transform retrosynthetic synthons into real reagents
5. Iterate until reaching simple/available starting materials

Key Principles:
- Start with target, not starting materials (goal-oriented)
- Simplify complexity at each step
- Consider multiple disconnection sites
- Evaluate each disconnection for synthetic feasibility

Strategic Bond Disconnections:
- Disconnect C-C bonds adjacent to FG (carbonyl, C=C, heteroatom)
- 1,2-Difunctionalized: aldol, Grignard, Wittig disconnection
- 1,3-Difunctionalized: Michael addition, Claisen disconnection
- 1,4-Difunctionalized: conjugate addition, Diels-Alder
- 1,5-Difunctionalized: Diels-Alder, Robinson annulation
- Aromatic: EAS sequence planning

Functional Group Interconversions (FGI):
- C=C → C-C (hydrogenation)
- Alcohol → alkyl halide, alkene, carbonyl
- Carbonyl → alcohol, imine, alkene (Wittig)
- Carboxylic acid → ester, amide, alcohol, alkyl
- Plan FGI to enable disconnection

Synthons and Synthetic Equivalents:
- Synthon: idealized charged fragment
- Reagent: real chemical that acts as synthon
- Example: R⁺ synthon = R-X + Lewis acid (electrophile)
- Example: R⁻ synthon = R-Li or R-MgX (nucleophile)

Umpolung (Polarity Reversal):
- Normal: carbonyl C is electrophilic (δ+)
- Umpolung: make carbonyl C nucleophilic (δ-)
- 1,3-Dithiane: acyl anion equivalent (R-CO⁻ → dithiane)
- Cyanide addition: acyl anion behavior
- Reverses normal reactivity, enables new disconnections

Guidelines for Disconnection Selection:
- Prefer disconnections that generate stable synthons
- Avoid generating high-energy intermediates (CH3⁺, vinyl⁻)
- Consider stereochemistry (stereospecific reactions)
- Prefer convergent over linear synthesis (efficiency)
- Check for hidden symmetry (simplifies disconnection)

Common Disconnection Patterns:
- β-Hydroxy carbonyl ⇒ aldol disconnection
- α,β-Unsaturated carbonyl ⇒ aldol + dehydration or Wittig
- 1,4-Dicarbonyl ⇒ Michael addition
- Cyclohexene ⇒ Diels-Alder
- 3° Alcohol ⇒ Grignard + ketone

Evaluation Criteria:
- Step count (shorter better)
- Overall yield (fewer steps, higher yield)
- Availability of starting materials
- Selectivity (regio-, stereo-, chemo-)
- Scalability and cost
""",
        key_factors=[
            "Work backward from target",
            "Disconnect C-C bonds near FGs",
            "Synthon → real reagent conversion",
            "FGI to enable disconnections",
            "Umpolung reverses polarity",
            "Convergent > linear synthesis",
            "Minimize steps, maximize yield"
        ],
        primary_authority=[
            "Corey & Cheng, The Logic of Chemical Synthesis (1995)",
            "Warren, Organic Synthesis: The Disconnection Approach (2nd ed., 2008)",
            "Nicolaou & Sorensen, Classics in Total Synthesis (1996)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE
    ),

    DoctrineBlock(
        topic="NMR_Spectroscopy",
        keywords=["NMR", "chemical shift", "coupling", "integration", "1H-NMR", "13C-NMR"],
        conclusion_template="NMR identifies structure via chemical shifts (δ ppm), integration (# H), splitting patterns (n+1 rule for J-coupling), and 2D techniques (COSY, HSQC, HMBC). ¹H-NMR for connectivity; ¹³C-NMR for carbon framework.",
        reasoning_framework="""
NMR Spectroscopy Principles and Interpretation:
1. Nuclear spin (I = 1/2 for ¹H, ¹³C) in magnetic field splits energy levels
2. Radiofrequency pulse flips spins
3. Relaxation emits signal (free induction decay, FID)
4. Fourier transform → frequency-domain spectrum

¹H-NMR Chemical Shifts (δ ppm, relative to TMS):
- Alkyl C-H: 0.5-2.0 ppm (saturated, upfield)
- Allylic C-H: 1.5-2.5 ppm
- α to carbonyl: 2.0-2.5 ppm
- Alkyne C-H: 2.5-3.0 ppm
- α to O/N: 3.0-4.5 ppm
- Vinylic C-H: 4.5-6.5 ppm
- Aromatic C-H: 6.5-8.5 ppm
- Aldehyde C-H: 9-10 ppm (far downfield)
- Carboxylic acid O-H: 10-13 ppm (very broad, exchangeable)

Integration:
- Area under peak proportional to # H
- Ratio of integrals gives H ratio (relative, not absolute)
- Compare to molecular formula to assign absolute H count

Splitting Patterns (J-coupling):
- n+1 rule: n equivalent neighbors → n+1 peaks
- Singlet (s): 0 neighbors
- Doublet (d): 1 neighbor
- Triplet (t): 2 neighbors
- Quartet (q): 3 neighbors
- Multiplet (m): many neighbors or complex
- Coupling constant J (Hz) measures interaction strength
- Geminal (²J), vicinal (³J), long-range (⁴J+)

¹³C-NMR Chemical Shifts:
- Alkyl: 10-50 ppm
- α to O/N: 50-80 ppm
- Alkyne: 70-90 ppm
- Alkene: 100-150 ppm
- Aromatic: 110-160 ppm
- Carbonyl: 160-220 ppm (C=O far downfield)
- Typically proton-decoupled (singlets only)

2D NMR Techniques:
- COSY (¹H-¹H correlation): identifies coupled protons (neighbors)
- HSQC (¹H-¹³C one-bond): assigns H to directly attached C
- HMBC (¹H-¹³C long-range): 2-3 bond correlations, key for connectivity
- NOESY/ROESY: spatial proximity (through-space, not bonds)

Interpretation Strategy:
1. Count # signals → # unique H/C environments
2. Integration → # H per signal
3. Chemical shift → functional group type
4. Splitting → # neighbors, connectivity
5. 2D NMR → assign connectivities and build structure

Common Pitfalls:
- Exchangeable protons (OH, NH) vary with solvent/temp
- Aromatic coupling complex (not simple n+1)
- ¹³C quaternary carbons weak signal (no attached H)
- Impurities: H2O (δ ~1.5 in CDCl3), TMS (δ 0)
""",
        key_factors=[
            "Chemical shift (δ) indicates functional group",
            "Integration gives H count ratio",
            "Splitting (n+1 rule) shows neighbors",
            "J-coupling (Hz) measures interaction",
            "¹³C-NMR for carbon skeleton",
            "2D NMR (COSY, HSQC, HMBC) for connectivity",
            "Exchangeable protons (OH, NH) variable"
        ],
        primary_authority=[
            "Silverstein et al., Spectrometric Identification of Organic Compounds (8th ed., 2014)",
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 11",
            "Friebolin, Basic One- and Two-Dimensional NMR Spectroscopy (5th ed., 2010)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE
    ),

    DoctrineBlock(
        topic="IR_Spectroscopy",
        keywords=["IR", "infrared", "stretching", "carbonyl", "OH", "NH", "fingerprint"],
        conclusion_template="IR spectroscopy identifies functional groups via characteristic vibrational frequencies. Key: O-H broad 3200-3600, N-H sharp 3300-3500, C=O 1650-1750, fingerprint <1500 cm⁻¹.",
        reasoning_framework="""
IR Spectroscopy Principles and Functional Group Identification:
1. Molecular vibrations (stretch, bend) absorb IR radiation
2. Frequency depends on bond strength and atomic masses
3. Hooke's law: ν ∝ √(k/μ) (k = force constant, μ = reduced mass)
4. Only IR-active vibrations (dipole change) absorb

Key Functional Group Frequencies (cm⁻¹):
- O-H (alcohol): 3200-3600 broad (H-bonding)
- N-H (amine/amide): 3300-3500 sharp (1° two peaks, 2° one peak)
- C-H (alkane): 2850-3000 (sp³)
- C-H (alkene): 3000-3100 (sp²)
- C-H (alkyne): ~3300 (sp, terminal alkyne)
- C≡C (alkyne): 2100-2260 (weak or absent if symmetrical)
- C≡N (nitrile): 2210-2260 (sharp, strong)
- C=O (carbonyl): 1650-1750 (varies by type, very strong)
  * Carboxylic acid: 1700-1725
  * Ester: 1735-1750
  * Ketone: 1705-1725
  * Aldehyde: 1720-1740
  * Amide: 1650-1680 (resonance lowers frequency)
  * Anhydride: two peaks 1750 and 1820
- C=C (alkene): 1620-1680 (variable intensity)
- Aromatic C=C: 1450-1600 (multiple peaks)
- Fingerprint region: <1500 cm⁻¹ (complex, unique to molecule)

Carbonyl Stretching Trends:
- Conjugation lowers frequency (resonance decreases C=O bond order)
- Ring strain increases frequency (angle strain stiffens bond)
- α,β-Unsaturation: lowers by ~30 cm⁻¹
- 5-membered ring (lactone/lactam): increases by ~30 cm⁻¹
- 4-membered ring (β-lactam/β-lactone): increases by ~60 cm⁻¹

O-H vs N-H Distinction:
- O-H: broad peak (extensive H-bonding)
- N-H: sharp peak(s) (less H-bonding)
- 1° amine (NH2): two peaks (symmetric + antisymmetric stretch)
- 2° amine (NHR): one peak
- 3° amine (NR3): no N-H peak

Interpretation Strategy:
1. Check 3000-3500 cm⁻¹ for O-H, N-H (diagnostic)
2. Check 1650-1750 cm⁻¹ for C=O (diagnostic)
3. Check 2100-2300 cm⁻¹ for C≡C, C≡N (diagnostic)
4. Check 1600-1680 cm⁻¹ for C=C (often weak)
5. Fingerprint <1500 cm⁻¹ for confirmation (match library)

Complementary to NMR:
- IR identifies functional groups (O-H, C=O, N-H)
- NMR identifies connectivity and substitution pattern
- Together: full structure elucidation
- Mass spec adds molecular weight and formula
""",
        key_factors=[
            "O-H broad 3200-3600 cm⁻¹",
            "N-H sharp 3300-3500 cm⁻¹",
            "C=O strong 1650-1750 cm⁻¹",
            "C≡C, C≡N 2100-2260 cm⁻¹",
            "Conjugation lowers C=O frequency",
            "Ring strain raises C=O frequency",
            "Fingerprint <1500 cm⁻¹ unique"
        ],
        primary_authority=[
            "Silverstein et al., Spectrometric Identification of Organic Compounds (8th ed., 2014)",
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 11",
            "Pavia et al., Introduction to Spectroscopy (5th ed., 2014)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE
    ),

    DoctrineBlock(
        topic="Mass_Spectrometry",
        keywords=["mass spec", "MS", "M+", "fragmentation", "base peak", "molecular ion", "isotope"],
        conclusion_template="Mass spectrometry determines molecular weight (M⁺ peak) and structure via fragmentation. Base peak = most abundant. Isotope patterns (Cl, Br) diagnostic. High-res MS gives molecular formula.",
        reasoning_framework="""
Mass Spectrometry Principles and Interpretation:
1. Sample ionized (electron impact, ESI, MALDI, etc.)
2. Ions accelerated and separated by m/z (mass-to-charge ratio)
3. Detector counts ions at each m/z
4. Spectrum: intensity vs m/z

Molecular Ion Peak (M⁺):
- Highest m/z peak (excluding isotopes and impurities)
- Gives molecular weight
- Odd MW → odd # N (nitrogen rule)
- Even MW → even # N (or no N)
- M⁺ often weak or absent (especially in EI for large molecules)

Fragmentation Patterns:
- M⁺ breaks into fragments (cation + neutral radical)
- Positive ion detected, radical lost
- Cleavage α to heteroatom or π-bond (stabilizes cation)
- McLafferty rearrangement: γ-H transfer to carbonyl O
- α-Cleavage: break bond adjacent to C=O or C=C

Base Peak:
- Most abundant peak in spectrum (set to 100%)
- Often most stable cation fragment
- Not necessarily M⁺

Common Neutral Losses:
- 18 (H2O): from alcohols, carboxylic acids
- 28 (CO): from aldehydes, ketones, esters
- 29 (CHO): from aldehydes
- 31 (OCH3): from methyl esters
- 45 (OEt or CO2H): from ethyl esters or acids
- 15, 29, 43, 57: loss of alkyl groups (CH3, C2H5, C3H7, C4H9)

Isotope Patterns (Diagnostic):
- Chlorine (Cl): M and M+2 in 3:1 ratio (³⁵Cl:³⁷Cl)
- Bromine (Br): M and M+2 in 1:1 ratio (⁷⁹Br:⁸¹Br)
- Sulfur (S): M+2 ~4.4% of M (³⁴S natural abundance)
- Two Cl: M, M+2, M+4 in 9:6:1 ratio
- Two Br: M, M+2, M+4 in 1:2:1 ratio

High-Resolution MS (HRMS):
- Measures m/z to 4+ decimal places
- Determines exact molecular formula
- Distinguishes isobaric species (e.g., CO vs N2 both ~28)
- TOF, Orbitrap, FT-ICR instruments

Ionization Methods:
- EI (electron impact): hard ionization, extensive fragmentation, for volatile organics
- CI (chemical ionization): soft, gives M+H⁺ (protonation)
- ESI (electrospray): soft, for polar, high MW compounds (proteins, polymers)
- MALDI (matrix-assisted laser desorption): soft, for very large biomolecules

Interpretation Strategy:
1. Identify M⁺ peak (or M+H⁺, M+Na⁺ in soft ionization)
2. Calculate molecular formula (HRMS or isotope pattern)
3. Check nitrogen rule (odd MW → odd N)
4. Identify base peak and major fragments
5. Look for neutral losses (H2O, CO, etc.)
6. Check isotope pattern for Cl, Br, S
7. Propose structure consistent with fragmentation
""",
        key_factors=[
            "M⁺ peak gives molecular weight",
            "Base peak = most abundant ion",
            "Fragmentation shows structure",
            "Nitrogen rule: odd MW → odd # N",
            "Cl/Br isotope patterns diagnostic",
            "HRMS gives exact molecular formula",
            "Soft ionization (ESI) for large molecules"
        ],
        primary_authority=[
            "Silverstein et al., Spectrometric Identification of Organic Compounds (8th ed., 2014)",
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 11",
            "McLafferty & Tureček, Interpretation of Mass Spectra (4th ed., 1993)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE
    ),

    DoctrineBlock(
        topic="Radical_Reactions",
        keywords=["radical", "NBS", "AIBN", "peroxide", "chain", "initiation", "propagation", "termination"],
        conclusion_template="Radical reactions: initiation (homolytic cleavage), propagation (chain), termination (coupling). NBS for allylic/benzylic bromination. Peroxides give anti-Markovnikov HBr addition.",
        reasoning_framework="""
Radical Reaction Mechanisms and Types:
1. Initiation: R-R → 2 R• (homolytic cleavage, heat or light)
2. Propagation: R• + X-Y → R-X + Y• (chain reaction)
3. Termination: R• + R• → R-R (or other radical coupling)

Common Radical Initiators:
- AIBN (azobisisobutyronitrile): heat → N2 + 2 (CH3)2C•CN
- Benzoyl peroxide (BPO): heat → 2 PhCO2• → 2 Ph• + 2 CO2
- Di-tert-butyl peroxide: heat → 2 (CH3)3CO•
- Light (hν): Cl2 → 2 Cl• (UV light)

Halogenation of Alkanes:
- Cl2 + hν → 2 Cl• (initiation)
- Cl• + R-H → HCl + R• (propagation)
- R• + Cl2 → R-Cl + Cl• (propagation, regenerates Cl•)
- Selectivity: 3° > 2° > 1° (follows radical stability)
- Chlorination less selective than bromination

Allylic and Benzylic Bromination (NBS):
- NBS (N-bromosuccinimide) + light or AIBN
- Br• abstracts allylic/benzylic H (most stable radical)
- High selectivity for allylic/benzylic positions
- Mechanism: NBS maintains low [Br2] (avoids alkene addition)

Anti-Markovnikov Addition (Peroxide Effect):
- HBr + peroxide → adds opposite to Markovnikov
- Radical mechanism: RO• + HBr → ROH + Br•
- Br• adds to less substituted C (steric, more stable radical)
- Only works for HBr (bond strengths), not HCl or HI

Radical Stability:
- Resonance: allyl•, benzyl• (delocalized)
- Hyperconjugation: 3° > 2° > 1° > CH3•
- Captodative effect: radical α to both donor and acceptor groups

Autoxidation:
- R• + O2 → ROO• (very fast, O2 biradical)
- ROO• + R-H → ROOH + R• (chain)
- Antioxidants (BHT, vitamin E) trap radicals, stop chain

Radical Polymerization:
- Initiation: initiator → R•
- Propagation: R• + CH2=CHX → R-CH2-CHX•
- R-CH2-CHX• + CH2=CHX → polymer• (chain growth)
- Termination: coupling or disproportionation
- Used for polyethylene, polystyrene, PVC, etc.
""",
        key_factors=[
            "Initiation: homolytic cleavage (heat, light)",
            "Propagation: chain reaction",
            "Termination: radical coupling",
            "Radical stability: 3° > 2° > 1° > CH3•",
            "NBS for allylic/benzylic bromination",
            "Peroxide + HBr → anti-Markovnikov",
            "Autoxidation with O2 (chain reaction)"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 39",
            "Smith & March, March's Advanced Organic Chemistry (7th ed., 2013)",
            "Fossey et al., Free Radicals in Organic Chemistry (1995)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        mechanism_details="Chain: R• propagates by abstracting H or adding to C=C",
        safety_notes="Peroxides explosive hazard. AIBN shock-sensitive when dry. Store cool, use dilute solutions."
    ),

    DoctrineBlock(
        topic="Pericyclic_Reactions",
        keywords=["pericyclic", "Woodward-Hoffmann", "concerted", "electrocyclic", "sigmatropic", "cycloaddition"],
        conclusion_template="Pericyclic reactions: concerted, no intermediates, governed by orbital symmetry (Woodward-Hoffmann rules). Types: electrocyclic, cycloaddition ([4+2], [2+2]), sigmatropic rearrangements (Cope, Claisen).",
        reasoning_framework="""
Pericyclic Reaction Classes and Orbital Symmetry:
1. Concerted mechanism (single transition state, no intermediates)
2. Stereochemistry determined by orbital symmetry
3. Thermal vs photochemical conditions give opposite outcomes

Woodward-Hoffmann Rules:
- Thermal: antarafacial or (4n+2)π suprafacial allowed
- Photochemical: conrotatory or 4nπ suprafacial allowed
- HOMO-LUMO interactions control selectivity

Electrocyclic Reactions:
- Ring opening/closing of conjugated polyenes
- Thermal 4nπ: conrotatory (e.g., cyclobutene → butadiene)
- Thermal (4n+2)π: disrotatory (e.g., hexatriene → cyclohexadiene)
- Photochemical: opposite stereochemistry
- Example: cyclobutene (thermal) → cis,trans-butadiene (con)

Cycloaddition Reactions:
- [4+2] Diels-Alder: thermally allowed, suprafacial-suprafacial
- [2+2] cycloaddition: thermally forbidden, photochemically allowed
- [2+2] (photochemical): cyclobutane formation from alkenes
- 1,3-Dipolar cycloaddition: [3+2], forms 5-membered heterocycles

Sigmatropic Rearrangements:
- [i,j] notation: bond migrates i atoms in one component, j in other
- [3,3] Cope rearrangement: 1,5-diene → isomeric 1,5-diene
- [3,3] Claisen rearrangement: allyl vinyl ether → γ,δ-unsaturated carbonyl
- [1,5] H-shift: suprafacial (thermal allowed)
- [1,7] H-shift: antarafacial (thermal allowed)

Cope Rearrangement:
- Thermally allowed [3,3] sigmatropic
- Chair-like transition state (preferred over boat)
- Can create new stereogenic centers
- Oxy-Cope: accelerated by alkoxide (β to migrating bond)

Claisen Rearrangement:
- [3,3] sigmatropic, allyl vinyl ether → γ,δ-unsaturated carbonyl
- Ireland-Claisen: silyl ketene acetal → carboxylic acid after hydrolysis
- Eschenmoser-Claisen: N,N-dimethylacetamide acetal
- Johnson-Claisen: orthoester variant

Ene Reaction:
- Alkene + alkene with allylic H → 1,4-addition product
- Thermal, concerted, no catalyst
- Pericyclic [2+2+2] formally

Stereochemical Outcomes:
- Suprafacial: same face of π-system
- Antarafacial: opposite faces
- Conrotatory: substituents rotate same direction
- Disrotatory: substituents rotate opposite directions
- Transition state geometry determines product stereochemistry
""",
        key_factors=[
            "Concerted, no intermediates",
            "Orbital symmetry (Woodward-Hoffmann)",
            "Thermal vs photochemical opposite",
            "Electrocyclic: con vs disrotatory",
            "Cycloaddition: [4+2] thermal allowed",
            "Sigmatropic: [3,3] Cope/Claisen",
            "Stereochemistry predictable by rules"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 35-36",
            "Fleming, Molecular Orbitals and Organic Chemical Reactions (2010)",
            "Woodward & Hoffmann, The Conservation of Orbital Symmetry (1970)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE
    ),

    DoctrineBlock(
        topic="Green_Chemistry_Principles",
        keywords=["green chemistry", "atom economy", "E-factor", "sustainable", "catalysis", "renewable"],
        conclusion_template="Green chemistry minimizes waste and hazards. Principles: atom economy, catalysis, renewable feedstocks, safer solvents, energy efficiency. Metrics: E-factor (kg waste/kg product), atom economy (MW product/MW reactants).",
        reasoning_framework="""
Twelve Principles of Green Chemistry (Anastas & Warner):
1. Waste prevention (better than treatment)
2. Atom economy (maximize incorporation into product)
3. Less hazardous synthesis (minimize toxicity)
4. Designing safer chemicals (efficacy with minimal toxicity)
5. Safer solvents and auxiliaries (water, scCO2, ionic liquids, or none)
6. Energy efficiency (ambient temp/pressure preferred)
7. Renewable feedstocks (bio-based materials)
8. Reduce derivatives (avoid protecting groups when possible)
9. Catalysis (catalytic > stoichiometric reagents)
10. Design for degradation (biodegradable products)
11. Real-time pollution prevention (in-process monitoring)
12. Inherently safer chemistry (minimize accident potential)

Atom Economy:
- Formula: (MW desired product / Σ MW all reactants) × 100%
- High atom economy: most atoms incorporated
- Ideal reactions: addition, rearrangement, cycloaddition
- Low atom economy: substitution with large leaving groups
- Example: Diels-Alder 100% (all atoms in product)
- Example: Wittig ~50% (Ph3P=O byproduct)

E-Factor (Environmental Factor):
- Formula: kg waste / kg product
- Includes all materials (solvents, reagents, byproducts)
- Pharma: E-factor 25-100 (high waste per drug)
- Bulk chemicals: E-factor <5 (economies of scale)
- Lower E-factor = greener process

Safer Solvents:
- Water: non-toxic, non-flammable, abundant
- Supercritical CO2 (scCO2): non-toxic, recyclable, good for extractions
- Ionic liquids: non-volatile, recyclable, tunable
- Ethanol, ethyl acetate: bio-derived, low toxicity
- Avoid: chlorinated solvents (CHCl3, CH2Cl2), benzene, DMF

Catalysis Advantages:
- Turnover number (TON): moles product / moles catalyst
- Reduces waste (stoichiometric reagents avoided)
- Enzymes: highly selective, mild conditions, biodegradable
- Organocatalysts: metal-free, low toxicity (proline, thiourea)
- Transition metal catalysts: Pd, Ru, etc. (cross-coupling, hydrogenation)

Renewable Feedstocks:
- Biomass: carbohydrates, lipids, lignin
- Bio-based monomers: lactic acid (PLA), succinic acid
- Terpenes: limonene, pinene (platform chemicals)
- Replace petroleum-derived starting materials

Energy Efficiency:
- Microwave heating: faster, selective heating
- Flow chemistry: continuous, better heat transfer
- Photochemistry: solar energy, mild conditions
- Avoid cryogenic temperatures, high pressure when possible

Examples of Green Transformations:
- Sharpless epoxidation: catalytic, high ee, mild
- Olefin metathesis: atom-economical, catalytic (Grubbs catalyst)
- Click chemistry: high yield, mild, no byproducts (azide-alkyne cycloaddition)
- Enzymatic resolutions: biocatalysis, mild, selective

Life Cycle Assessment (LCA):
- Cradle-to-grave analysis of environmental impact
- Includes raw material extraction, synthesis, use, disposal
- Identifies hotspots for improvement
- Holistic view beyond just reaction step
""",
        key_factors=[
            "Maximize atom economy",
            "Minimize E-factor (waste)",
            "Use catalysis over stoichiometric",
            "Safer solvents (H2O, scCO2, EtOH)",
            "Renewable feedstocks (biomass)",
            "Energy efficiency (ambient conditions)",
            "Design for degradation"
        ],
        primary_authority=[
            "Anastas & Warner, Green Chemistry: Theory and Practice (1998)",
            "Sheldon, Green Chem. 2007, 9, 1273 (E-factor review)",
            "Trost, Science 1991, 254, 1471 (atom economy)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE
    ),

    DoctrineBlock(
        topic="Polymer_Chemistry_Fundamentals",
        keywords=["polymer", "monomer", "degree of polymerization", "tacticity", "chain growth", "step growth"],
        conclusion_template="Polymers: long chains of repeating monomer units. Chain-growth (radical, cationic, anionic) vs step-growth (condensation). Tacticity (atactic, isotactic, syndiotactic) affects properties. Degree of polymerization (DP) = # repeat units.",
        reasoning_framework="""
Polymer Classification and Mechanisms:
1. Chain-growth (addition): unsaturated monomers, no byproducts
2. Step-growth (condensation): bifunctional monomers, small molecule eliminated
3. Degree of polymerization (DP): n = MW polymer / MW monomer
4. Polydispersity index (PDI): MW_w / MW_n (breadth of MW distribution)

Chain-Growth Polymerization:
- Radical: AIBN or peroxide initiator, propagates via R•
  Examples: polyethylene, polystyrene, PVC, PMMA
- Cationic: Lewis acid (BF3, AlCl3), propagates via R⁺
  Monomers with EDG (isobutylene, vinyl ethers)
- Anionic: strong base (n-BuLi, RO⁻), propagates via R⁻
  Monomers with EWG (acrylonitrile, styrene)
  Living polymerization (no termination, narrow PDI)
- Coordination (Ziegler-Natta): TiCl4/AlEt3, isotactic/syndiotactic control

Step-Growth Polymerization:
- Condensation: A-A + B-B → polymer + small molecule (H2O, HCl)
- Examples: polyester (diacid + diol), polyamide (diacid + diamine), polycarbonate
- Nylon 6,6: hexamethylenediamine + adipic acid
- PET (polyethylene terephthalate): terephthalic acid + ethylene glycol
- MW increases slowly, high DP only near full conversion

Tacticity (Stereochemistry):
- Atactic: random stereochemistry, amorphous, weak
- Isotactic: all substituents same side, crystalline, strong
- Syndiotactic: alternating sides, crystalline
- Ziegler-Natta catalysts give isotactic/syndiotactic control
- Free radical polymerization gives atactic

Polymer Properties:
- Crystallinity: isotactic/syndiotactic > atactic
- T_g (glass transition): amorphous → rubbery
- T_m (melting point): crystalline → liquid
- Molecular weight affects strength, viscosity, processability
- Cross-linking: thermosets (irreversible) vs thermoplastics (reversible)

Living Polymerization:
- No termination or chain transfer
- All chains grow at same rate
- Narrow PDI (PDI → 1)
- Anionic (styrene + n-BuLi) classic example
- ATRP (atom transfer radical polymerization): controlled radical
- RAFT (reversible addition-fragmentation chain transfer): controlled radical

Copolymers:
- Random: A and B monomers random sequence
- Alternating: -A-B-A-B- strict alternation
- Block: -AAAA-BBBB- blocks of each
- Graft: backbone A, side chains B
- Reactivity ratios (r1, r2) determine sequence distribution

Common Polymers:
- LDPE/HDPE: low/high density polyethylene (branching affects density)
- PP: polypropylene (isotactic for rigidity)
- PS: polystyrene (atactic, brittle)
- PVC: polyvinyl chloride (requires plasticizers)
- PMMA: poly(methyl methacrylate), Plexiglas
- Nylon: polyamides (H-bonding → strength)
- PET: polyester (bottles, fibers)
""",
        key_factors=[
            "Chain-growth: no byproducts",
            "Step-growth: condensation, small molecule lost",
            "Tacticity: isotactic/syndiotactic > atactic",
            "DP = # monomer units",
            "Living polymerization: narrow PDI",
            "Copolymers: random/block/alternating",
            "Crystallinity and T_g affect properties"
        ],
        primary_authority=[
            "Odian, Principles of Polymerization (4th ed., 2004)",
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 52",
            "Stevens, Polymer Chemistry: An Introduction (3rd ed., 1999)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE
    ),

    DoctrineBlock(
        topic="Carbohydrate_Chemistry",
        keywords=["carbohydrate", "glucose", "glycosidic", "anomeric", "mutarotation", "Haworth"],
        conclusion_template="Carbohydrates: polyhydroxy aldehydes/ketones. Cyclic forms via hemiacetal formation. Anomers (α/β) at anomeric carbon. Mutarotation equilibrates anomers. Glycosidic bonds link sugars.",
        reasoning_framework="""
Carbohydrate Structure and Nomenclature:
1. Monosaccharides: simple sugars (glucose, fructose)
2. Disaccharides: two monosaccharides (sucrose, lactose, maltose)
3. Oligosaccharides: 3-10 sugars
4. Polysaccharides: >10 sugars (starch, cellulose, glycogen)

Monosaccharide Classification:
- Aldoses: aldehyde (glucose, ribose, galactose)
- Ketoses: ketone (fructose, ribulose)
- Triose, tetrose, pentose, hexose (3, 4, 5, 6 carbons)
- D/L configuration: based on highest-numbered stereocenter (Fischer)

Cyclic Hemiacetal Formation:
- Aldohexose: 6-membered ring (pyranose) or 5-membered (furanose)
- Ketohexose: typically furanose (fructose)
- Anomeric carbon: new stereocenter from cyclization
- α-anomer: OH down (Haworth projection, D-sugar)
- β-anomer: OH up (Haworth projection, D-sugar)

Mutarotation:
- Equilibration of α/β anomers in solution
- Ring opens (aldehyde form), re-closes
- D-Glucose: 36% α, 64% β at equilibrium (β more stable, equatorial OH)
- Optical rotation changes until equilibrium

Glycosidic Bonds:
- Acetal linkage between anomeric C and another OH
- α-glycosidic: down linkage
- β-glycosidic: up linkage
- Hydrolyzed by acid or enzymes (glycosidases)
- Examples: maltose (α-1,4), lactose (β-1,4), sucrose (α-1,β-2)

Disaccharides:
- Maltose: Glc-α(1→4)-Glc (reducing, one free anomeric OH)
- Lactose: Gal-β(1→4)-Glc (reducing)
- Sucrose: Glc-α(1↔2β)-Fru (non-reducing, no free anomeric)
- Reducing sugar: free anomeric OH (can be oxidized)

Polysaccharides:
- Starch: amylose (α-1,4 linear) + amylopectin (α-1,4 + α-1,6 branched)
- Glycogen: highly branched (α-1,4 + α-1,6), animal starch
- Cellulose: β-1,4 linkages (humans cannot digest, no cellulase)
- Chitin: β-1,4 N-acetylglucosamine (insect exoskeleton, fungal cell wall)

Reactions:
- Glycosylation: install glycosidic bond (protecting groups + Lewis acid)
- Oxidation: aldose → aldaric acid (both ends oxidized)
- Reduction: aldose → alditol (sorbitol from glucose)
- Osazone formation: phenylhydrazine → crystalline derivatives (identification)

Fischer vs Haworth Projections:
- Fischer: flat, vertical = C chain
- Haworth: ring perspective, shows α/β clearly
- Convert: R on Fischer → down on Haworth (D-sugar)
""",
        key_factors=[
            "Cyclic hemiacetal (pyranose/furanose)",
            "Anomeric carbon: α (down) vs β (up)",
            "Mutarotation equilibrates anomers",
            "Glycosidic bond: acetal linkage",
            "Reducing sugar: free anomeric OH",
            "Starch (α-1,4) vs cellulose (β-1,4)",
            "D/L based on highest stereocenter"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 38",
            "Lindhorst, Essentials of Carbohydrate Chemistry (2007)",
            "Stick & Williams, Carbohydrates: The Essential Molecules of Life (2009)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE
    ),

    DoctrineBlock(
        topic="Amino_Acid_Peptide_Chemistry",
        keywords=["amino acid", "peptide", "zwitterion", "isoelectric point", "protecting group", "coupling"],
        conclusion_template="Amino acids: NH2-CHR-COOH, zwitterionic at pH 7. Peptide bond formed via amide linkage (coupling reagents: DCC, EDC). Protecting groups (BOC, Fmoc) prevent side reactions. Solid-phase synthesis (Merrifield) builds peptides.",
        reasoning_framework="""
Amino Acid Structure and Properties:
1. α-Amino acid: NH2, COOH on same carbon (except proline)
2. 20 standard amino acids (proteinogenic)
3. Zwitterion: +NH3-CHR-COO⁻ at neutral pH
4. Isoelectric point (pI): pH where net charge = 0
5. L-configuration (S except cysteine which is R)

Classification by Side Chain:
- Nonpolar: Ala, Val, Leu, Ile, Met, Phe, Trp, Pro
- Polar uncharged: Ser, Thr, Cys, Tyr, Asn, Gln
- Acidic (negatively charged): Asp, Glu (pKa ~4)
- Basic (positively charged): Lys, Arg, His (pKa 6-13)

Acid-Base Properties:
- Three pKa values: α-COOH (~2), α-NH3⁺ (~9), side chain (if ionizable)
- Titration curve: two (or three) equivalence points
- Isoelectric point: pI = (pKa1 + pKa2) / 2 (for neutral AA)
- Buffer capacity near pKa values

Peptide Bond Formation:
- Amide bond: -CO-NH- (planar, partial double bond character)
- Nucleophilic acyl substitution: COOH + NH2 → CONH + H2O
- Requires activation (coupling reagents to overcome thermodynamics)
- Protecting groups essential (prevent self-coupling, side reactions)

Coupling Reagents:
- DCC (dicyclohexylcarbodiimide): activates COOH
- EDC (1-ethyl-3-(3-dimethylaminopropyl)carbodiimide): water-soluble variant
- HOBt/HOAt: suppress racemization
- HATU, HBTU: modern activators with better efficiency
- Mechanism: O-acylurea intermediate → aminolysis

Protecting Groups for Peptide Synthesis:
- N-terminal protection (prevent self-coupling):
  * BOC (tert-butoxycarbonyl): TFA-labile, base-stable
  * Fmoc (9-fluorenylmethoxycarbonyl): base-labile (piperidine), acid-stable
  * Cbz (benzyloxycarbonyl): H2/Pd-labile
- C-terminal protection: methyl/benzyl ester
- Side chain protection: orthogonal to N-terminal strategy
  * Ser/Thr: t-Bu ether
  * Asp/Glu: t-Bu ester
  * Lys: BOC or Fmoc (depending on N-terminal PG)
  * Cys: trityl or Acm (S-acetamidomethyl)

Solid-Phase Peptide Synthesis (SPPS, Merrifield):
1. Attach first AA to resin (C-terminus anchored)
2. Deprotect N-terminus (Fmoc → piperidine, BOC → TFA)
3. Couple next AA (activated by coupling reagent)
4. Repeat deprotection-coupling cycles
5. Cleave peptide from resin + remove side-chain PGs
6. Purify by HPLC

Advantages of SPPS:
- Excess reagents easily washed away
- Automation (peptide synthesizers)
- No purification between steps
- Can make long peptides (50+ AA)

Peptide Sequencing (Edman Degradation):
- N-terminal labeling: phenyl isothiocyanate (PITC)
- Cyclization → release N-terminal AA as PTH derivative
- Identify by HPLC/MS
- Repeat for next AA (sequencing one residue at a time)

Disulfide Bonds:
- Cys-Cys oxidation → cystine (S-S bridge)
- Stabilizes 3D structure
- Formation: air oxidation (iodine, DMSO)
- Reduction: DTT, β-mercaptoethanol, TCEP
""",
        key_factors=[
            "Zwitterion at pH 7 (±NH3-COO⁻)",
            "Peptide bond: amide linkage",
            "Coupling reagents (DCC, EDC) activate COOH",
            "Protecting groups (BOC, Fmoc) required",
            "SPPS: solid-phase synthesis on resin",
            "Isoelectric point: net charge = 0",
            "Disulfide bonds stabilize structure"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 49",
            "Chan & White, Fmoc Solid Phase Peptide Synthesis (2000)",
            "Greenstein & Winitz, Chemistry of the Amino Acids (1961, classic)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE
    ),

    DoctrineBlock(
        topic="Lipid_Chemistry",
        keywords=["lipid", "fatty acid", "triglyceride", "saponification", "phospholipid", "membrane"],
        conclusion_template="Lipids: hydrophobic biomolecules. Fatty acids (long-chain COOH), triglycerides (glycerol + 3 fatty acids), phospholipids (membrane components). Saponification: ester hydrolysis → soap. Unsaturation lowers melting point.",
        reasoning_framework="""
Lipid Classification and Structure:
1. Fatty acids: long-chain carboxylic acids (C12-C20)
2. Triglycerides (triacylglycerols): glycerol esterified with 3 fatty acids
3. Phospholipids: glycerol + 2 fatty acids + phosphate + head group
4. Steroids: fused ring systems (cholesterol, hormones)
5. Waxes: long-chain alcohol + fatty acid ester

Fatty Acid Structure:
- Saturated: no C=C (palmitic C16, stearic C18)
- Unsaturated: one or more C=C (oleic C18:1, linoleic C18:2)
- Omega notation: ω-3, ω-6 (position of first C=C from methyl end)
- IUPAC: Δ9 means C=C between C9 and C10 (from COOH)
- Natural fatty acids: even # carbons (biosynthesis from acetyl-CoA)
- cis-Unsaturation: common (introduces kink, lowers MP)

Physical Properties:
- Saturated fatty acids: straight chains, pack tightly, high MP (solid at RT)
- Unsaturated fatty acids: kinks from cis-C=C, lower MP (liquid at RT)
- Chain length: longer chain → higher MP (more van der Waals)
- Triglycerides: MP depends on fatty acid composition
  * Saturated fats: animal fats, butter, lard (solid)
  * Unsaturated fats: vegetable oils (liquid)

Saponification:
- Base hydrolysis of ester: triglyceride + NaOH → glycerol + 3 RCOONa (soap)
- Soap: fatty acid salt (amphiphilic, forms micelles)
- Hydrophobic tail (R-), hydrophilic head (COO⁻)
- Emulsifies oils (solubilizes in water)

Phospholipids:
- Structure: glycerol + 2 fatty acids + phosphate + head group
- Common head groups: choline (phosphatidylcholine, lecithin), ethanolamine, serine
- Amphipathic: hydrophobic tails, hydrophilic head
- Bilayer formation: basis of cell membranes
- Fluidity depends on saturation, chain length, cholesterol content

Steroids:
- Fused ring system: three 6-membered rings + one 5-membered (ABCD)
- Cholesterol: membrane component, precursor to steroid hormones
- Testosterone, estrogen, cortisol: all derived from cholesterol
- Trans ring junctions (rigid, planar structure)

Prostaglandins and Eicosanoids:
- Derived from arachidonic acid (C20:4 ω-6)
- COX enzyme oxidizes to prostaglandins (inflammation, pain)
- NSAIDs (aspirin, ibuprofen) inhibit COX
- Leukotrienes, thromboxanes also from arachidonic acid

Reactions:
- Hydrogenation: unsaturated → saturated (Ni catalyst, H2)
  Used industrially to harden vegetable oils (margarine)
  Trans fats as byproduct (health concerns)
- Oxidation: C=C → peroxides (rancidity, autoxidation)
  Antioxidants (vitamin E, BHT) prevent
- Hydrolysis: lipase enzymes → fatty acids + glycerol

Biological Roles:
- Energy storage: triglycerides (9 kcal/g vs 4 for carbs/protein)
- Cell membranes: phospholipid bilayer
- Signaling: prostaglandins, steroids
- Insulation: subcutaneous fat
- Vitamins: A, D, E, K (fat-soluble)
""",
        key_factors=[
            "Fatty acids: long-chain COOH",
            "Triglycerides: glycerol + 3 fatty acids",
            "Saponification: base hydrolysis → soap",
            "Unsaturation (cis) lowers melting point",
            "Phospholipids: membrane bilayer",
            "Steroids: fused rings (cholesterol)",
            "Omega-3/6: essential fatty acids"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 51",
            "Gunstone, The Chemistry of Oils and Fats (2004)",
            "Voet & Voet, Biochemistry (4th ed., 2011)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE
    ),

    DoctrineBlock(
        topic="Organometallic_Cross_Coupling",
        keywords=["cross-coupling", "Suzuki", "Heck", "Stille", "Negishi", "palladium", "C-C bond"],
        conclusion_template="Transition metal-catalyzed cross-coupling forms C-C bonds. Suzuki (boronic acid), Heck (alkene), Stille (tin), Negishi (zinc). Palladium(0) catalysts. Mechanism: oxidative addition, transmetalation, reductive elimination.",
        reasoning_framework="""
Cross-Coupling Reaction Mechanisms (General Pd Cycle):
1. Oxidative addition: Pd(0) + R-X → R-Pd(II)-X
2. Transmetalation: R-Pd-X + R'-M → R-Pd-R' + M-X
3. Reductive elimination: R-Pd-R' → R-R' + Pd(0)
4. Pd(0) catalyst regenerated

Suzuki-Miyaura Coupling:
- Reactants: R-X (halide/triflate) + R'-B(OH)2 (boronic acid)
- Catalyst: Pd(PPh3)4 or Pd(OAc)2 + ligand
- Base: K2CO3, Na2CO3, or CsF (activates boron)
- Mechanism: oxidative addition → transmetalation (boron) → reductive elimination
- Advantages: boronic acids air-stable, low toxicity, functional group tolerant
- R' = aryl, vinyl, alkyl (less common)

Heck Reaction:
- Reactants: R-X (halide/triflate) + alkene
- Catalyst: Pd(OAc)2 + phosphine ligand
- Base: triethylamine or K2CO3
- Mechanism: oxidative addition → alkene insertion → β-H elimination
- Forms substituted alkene (usually E-isomer)
- Regioselectivity: bulky groups at less substituted C
- Intramolecular Heck: excellent for ring formation

Stille Coupling:
- Reactants: R-X + R'-SnR3 (organostannane)
- Catalyst: Pd(PPh3)4
- No base required (tin more reactive than boron)
- Mechanism: standard Pd cycle, transmetalation with tin
- Advantages: high functional group tolerance, mild
- Disadvantages: tin reagents toxic, difficult to remove

Negishi Coupling:
- Reactants: R-X + R'-ZnX (organozinc)
- Catalyst: Pd(PPh3)4 or Ni catalyst
- Organozinc reagents less stable (air/moisture sensitive)
- Mechanism: standard Pd cycle
- Advantages: versatile (aryl, vinyl, alkyl), high yields
- Requires anhydrous conditions

Ligand Effects:
- Electron-rich phosphines (e.g., P(t-Bu)3) accelerate oxidative addition
- Bulky ligands (e.g., XPhos, SPhos) enhance reductive elimination
- Bidentate ligands (dppe, dppf) stabilize Pd(0)
- Ligand choice crucial for difficult substrates (aryl chlorides, alkyl halides)

Leaving Group Reactivity:
- Triflate (OTf) > I > Br > Cl >> F
- Chlorides require more active catalyst/ligand
- Tosylates, mesylates also viable

Scope and Limitations:
- Aryl halides: excellent substrates
- Vinyl halides: good (retain geometry)
- Alkyl halides: challenging (β-H elimination competes)
- Heteroaryl: generally compatible
- Functional groups: esters, amides, nitriles, ethers compatible
- Free amines, thiols can poison catalyst (protect or use less nucleophilic variants)

Applications:
- Natural product synthesis (complex C-C bond formation)
- Pharmaceuticals (aryl-aryl, aryl-heteroaryl bonds)
- Materials (conjugated polymers, OLEDs)
- Agriculture (agrochemical synthesis)

Nobel Prize (2010):
- Heck, Negishi, Suzuki awarded for palladium-catalyzed cross-coupling
""",
        key_factors=[
            "Pd(0) catalyst, 3-step cycle",
            "Oxidative addition: Pd + R-X",
            "Transmetalation: M transfers R'",
            "Reductive elimination: forms R-R'",
            "Suzuki: boronic acid (air-stable)",
            "Heck: alkene (β-H elimination)",
            "Stille: tin (toxic but mild)"
        ],
        primary_authority=[
            "Clayden, Organic Chemistry (2nd ed., 2012), Ch. 31",
            "Negishi, Handbook of Organopalladium Chemistry (2002)",
            "de Meijere & Diederich, Metal-Catalyzed Cross-Coupling Reactions (2004)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        safety_notes="Organotin reagents (Stille) toxic. Pd catalysts expensive, recover when possible."
    ),

    DoctrineBlock(
        topic="Safety_Handling_Organic_Reagents",
        keywords=["safety", "pyrophoric", "flammable", "toxic", "carcinogen", "SDS", "hood"],
        conclusion_template="Organic chemistry safety: use fume hood, PPE (gloves, goggles, lab coat). Pyrophoric reagents (n-BuLi, Grignard) ignite in air. Carcinogens (benzene, CCl4, chromium) require extreme caution. Always consult SDS.",
        reasoning_framework="""
General Safety Principles:
1. Fume hood for volatile/toxic substances
2. PPE: nitrile gloves, safety goggles, lab coat
3. No open flames near flammable solvents
4. Fire extinguisher, eyewash, safety shower accessible
5. Never work alone with hazardous materials

Pyrophoric Reagents (ignite in air):
- n-Butyllithium (n-BuLi): handle under inert atmosphere (N2, Ar)
- tert-Butyllithium (t-BuLi): more reactive than n-BuLi
- Grignard reagents (RMgX): ignite if exposed to air/moisture
- Alkylaluminum compounds (AlEt3, AlMe3): extremely pyrophoric
- Handling: Schlenk line or glovebox, syringe transfer

Flammable Solvents:
- Diethyl ether (Et2O): highly flammable, low BP, forms peroxides
- Tetrahydrofuran (THF): flammable, peroxide former
- Hexane, pentane: extremely flammable
- Acetone, methanol, ethanol: flammable
- No open flames, hot plates preferred over Bunsen burners
- Ground all equipment to prevent static spark

Peroxide Formation:
- Ethers (Et2O, THF, dioxane) form explosive peroxides on storage
- Test with peroxide strips before distillation
- Distill with BHT or LiAlH4 to suppress peroxides
- Never distill to dryness (peroxides concentrate, explosive)
- Dispose of old ether bottles (>1 year) carefully

Toxic Substances:
- Benzene: carcinogen (avoid, use toluene substitute)
- Carbon tetrachloride (CCl4): carcinogen, liver damage (obsolete)
- Chloroform (CHCl3): suspected carcinogen, use with caution
- Dimethyl sulfate: extreme toxicity, carcinogen (avoid)
- Acrylamide: neurotoxin, carcinogen (wear gloves)
- Mercury: heavy metal, toxic vapor (avoid thermometers, use alcohol/digital)

Corrosive Reagents:
- Sulfuric acid (H2SO4): concentrated is corrosive, exothermic with H2O
- Hydrofluoric acid (HF): extreme hazard, penetrates skin (Ca²⁺ antidote gel)
- Trifluoroacetic acid (TFA): corrosive, volatile (hood)
- Sodium/potassium hydroxide: caustic, burns

Chromium Reagents (carcinogenic):
- Chromic acid, Jones reagent (CrO3/H2SO4): carcinogen
- PCC, PDC: less hazardous but still Cr(VI)
- Proper disposal required (reduce to Cr(III) before disposal)
- Prefer non-chromium oxidants (DMP, Swern, TEMPO)

Cryogenic Hazards:
- Dry ice (solid CO2): frostbite, asphyxiation in confined space
- Liquid nitrogen: frostbite, oxygen displacement
- Wear cryo-gloves, eye protection
- Ensure adequate ventilation

Compressed Gas Cylinders:
- Secure with chains/straps
- Regulators specific to gas type
- H2, O2, CO, Ar, N2 cylinders
- Never use oil on O2 regulator (explosion risk)

Explosive Hazards:
- Peroxides: test and dispose carefully
- Azides: shock-sensitive, never isolate large amounts
- Diazonium salts: explosive when dry
- Perchloric acid: explosive with organics
- Nitrations: exothermic, runaway risk

Waste Disposal:
- Separate halogenated from non-halogenated solvents
- Aqueous vs organic waste
- Heavy metals (Cr, Hg, Pd) separate stream
- Consult institutional EH&S for disposal protocols
- Never pour organics down drain

Emergency Procedures:
- Fire: use ABC extinguisher, evacuate if uncontrollable
- Spill: contain, neutralize if possible, notify EH&S for large spills
- Exposure: eyewash 15 min, remove contaminated clothing, seek medical attention
- Ingestion: do not induce vomiting, call poison control

Safety Data Sheets (SDS):
- Read before using new chemical
- Hazards, PPE, first aid, disposal
- GHS pictograms (flame, skull, exclamation)
""",
        key_factors=[
            "Use fume hood for volatile/toxic",
            "PPE: gloves, goggles, lab coat",
            "Pyrophoric: n-BuLi, Grignard (air-sensitive)",
            "Carcinogens: benzene, CCl4, chromium",
            "Peroxide formers: test ethers before distillation",
            "Flammable solvents: no open flames",
            "Always consult SDS before use"
        ],
        primary_authority=[
            "ACS Guide to Safety in the Chemistry Laboratory (2012)",
            "Prudent Practices in the Laboratory (National Research Council, 2011)",
            "Institutional EH&S protocols"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        safety_notes="This doctrine block itself is safety-focused. Follow all protocols rigorously."
    ),
]

# ============================================================================
# ENGINE CORE
# ============================================================================

class CHEM01Engine:
    """Organic Chemistry Intelligence Engine."""

    def __init__(self):
        self.doctrines = DOCTRINES
        self.start_time = datetime.now()
        self.query_count = 0
        self.cache_hits = 0
        self.drift_events = []
        self.coverage_map = {d.topic: 0 for d in self.doctrines}

        logger.info(f"CHEM01 Engine initialized with {len(self.doctrines)} doctrines")

    def query(self, request: QueryRequest) -> QueryResponse:
        """Process organic chemistry query."""
        start = datetime.now()
        self.query_count += 1

        query_lower = request.query.lower()
        triggered = []
        reasoning_chain = []

        # Match doctrines by keyword
        for doctrine in self.doctrines:
            if any(kw.lower() in query_lower for kw in doctrine.keywords):
                triggered.append(doctrine.topic)
                doctrine.hit_count += 1
                doctrine.last_triggered = datetime.now().isoformat()
                self.coverage_map[doctrine.topic] += 1

        # Generate response based on mode
        if not triggered:
            answer = "No specific organic chemistry doctrines matched. Please provide more chemical context (reaction mechanisms, functional groups, spectroscopy, synthesis strategy, etc.)."
            confidence = ConfidenceLevel.REQUIRES_VERIFICATION
        else:
            # Get top matched doctrine
            top_doctrine = next(d for d in self.doctrines if d.topic == triggered[0])

            if request.mode == ResponseMode.FAST:
                answer = f"{top_doctrine.conclusion_template}\n\nKey factors: {', '.join(top_doctrine.key_factors[:3])}"
                reasoning_chain = None
            elif request.mode == ResponseMode.DEFENSE:
                answer = f"{top_doctrine.conclusion_template}\n\n"
                answer += f"Reasoning Framework:\n{top_doctrine.reasoning_framework[:500]}...\n\n"
                answer += f"Primary Authority:\n" + "\n".join(f"- {auth}" for auth in top_doctrine.primary_authority)
                reasoning_chain = [
                    f"Matched doctrine: {top_doctrine.topic}",
                    f"Confidence: {top_doctrine.confidence.value}",
                    "Full reasoning framework applied"
                ]
            else:  # MEMO
                answer = f"ORGANIC CHEMISTRY ANALYSIS MEMORANDUM\n\n"
                answer += f"Topic: {top_doctrine.topic}\n\n"
                answer += f"Conclusion:\n{top_doctrine.conclusion_template}\n\n"
                answer += f"Detailed Reasoning:\n{top_doctrine.reasoning_framework}\n\n"
                answer += f"Key Factors:\n" + "\n".join(f"{i+1}. {factor}" for i, factor in enumerate(top_doctrine.key_factors)) + "\n\n"
                answer += f"Primary Authority:\n" + "\n".join(f"- {auth}" for auth in top_doctrine.primary_authority) + "\n\n"
                if top_doctrine.mechanism_details:
                    answer += f"Mechanism Details:\n{top_doctrine.mechanism_details}\n\n"
                if top_doctrine.safety_notes:
                    answer += f"Safety Notes:\n{top_doctrine.safety_notes}\n\n"
                answer += f"Confidence Level: {top_doctrine.confidence.value}"

                reasoning_chain = [
                    f"Comprehensive analysis of {top_doctrine.topic}",
                    f"Authority sources: {len(top_doctrine.primary_authority)}",
                    f"Key factors enumerated: {len(top_doctrine.key_factors)}",
                    "Full mechanism and safety considerations included"
                ]

            confidence = top_doctrine.confidence

        # Calculate determinism hash
        hash_input = f"{request.query}|{request.mode.value}|{','.join(triggered)}"
        det_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        # Telemetry
        elapsed = (datetime.now() - start).total_seconds()
        telemetry = {
            "query_time_ms": round(elapsed * 1000, 2),
            "doctrines_triggered": len(triggered),
            "total_queries": self.query_count,
            "cache_hit_rate": round(self.cache_hits / max(1, self.query_count), 3)
        }

        logger.info(f"Query processed: {len(triggered)} doctrines, {elapsed*1000:.1f}ms, mode={request.mode.value}")

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            mode=request.mode,
            triggered_doctrines=triggered,
            reasoning_chain=reasoning_chain,
            determinism_hash=det_hash,
            timestamp=datetime.now().isoformat(),
            telemetry=telemetry
        )

    def get_health(self) -> HealthResponse:
        """Health check endpoint data."""
        uptime = (datetime.now() - self.start_time).total_seconds()
        return HealthResponse(
            status="operational",
            engine="CHEM01_Organic_Chemistry",
            version="1.0.0",
            port=9051,
            doctrines_loaded=len(self.doctrines),
            uptime_seconds=round(uptime, 2)
        )

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="CHEM01 Organic Chemistry Engine",
    description="Comprehensive organic chemistry knowledge engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = CHEM01Engine()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return engine.get_health()

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process organic chemistry query."""
    try:
        return engine.query(request)
    except Exception as e:
        logger.error(f"Query processing error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "engine": "CHEM01_Organic_Chemistry",
        "version": "1.0.0",
        "status": "operational",
        "doctrines": len(engine.doctrines),
        "endpoints": {
            "health": "/health",
            "query": "/query (POST)"
        }
    }

if __name__ == "__main__":
    import uvicorn

    # Ensure logs directory exists
    Path(__file__).parent.joinpath("logs").mkdir(exist_ok=True)

    logger.info("Starting CHEM01 Organic Chemistry Engine on port 9051")
    uvicorn.run(app, host="0.0.0.0", port=9051, log_level="info")
