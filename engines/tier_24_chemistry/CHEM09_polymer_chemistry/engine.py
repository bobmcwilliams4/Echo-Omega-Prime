"""
CHEM09 Polymer Chemistry Intelligence Engine
TIE-Grade Knowledge System for Polymer Science

Analyzes: Polymerization mechanisms, polymer characterization, rheology,
processing, degradation, and industrial polymer applications including oilfield.

Port: 9291
Version: 1.0.0
"""

import sys
from pathlib import Path

# CRITICAL: Set path BEFORE any local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Literal
from enum import Enum
from dataclasses import dataclass, field, asdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ============================================================================
# ENUMS AND DATA STRUCTURES
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


class IssueCategory(str, Enum):
    POLYMERIZATION_MECHANISM = "POLYMERIZATION_MECHANISM"
    MOLECULAR_WEIGHT = "MOLECULAR_WEIGHT"
    THERMAL_ANALYSIS = "THERMAL_ANALYSIS"
    RHEOLOGY = "RHEOLOGY"
    POLYMER_PROCESSING = "POLYMER_PROCESSING"
    DEGRADATION = "DEGRADATION"
    POLYMER_BLENDS = "POLYMER_BLENDS"
    BIOPOLYMERS = "BIOPOLYMERS"
    OILFIELD_POLYMERS = "OILFIELD_POLYMERS"
    CHARACTERIZATION = "CHARACTERIZATION"
    CONTROLLED_POLYMERIZATION = "CONTROLLED_POLYMERIZATION"
    POLYMER_COMPOSITES = "POLYMER_COMPOSITES"


@dataclass
class DoctrineBlock:
    """Individual knowledge block with complete reasoning"""
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
class QueryMetrics:
    """Telemetry for single query"""
    query_id: str
    timestamp: str
    mode: ResponseMode
    cache_hit: bool
    doctrines_triggered: List[str]
    response_time_ms: float
    confidence: ConfidenceLevel
    zone: AnalysisZone
    determinism_hash: str


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Polymer chemistry question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis context")
    include_reasoning: bool = Field(default=False, description="Include reasoning chain")


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    doctrines_applied: List[str]
    reasoning: Optional[str] = None
    response_time_ms: float
    determinism_hash: str
    epistemic_disclosure: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float


# ============================================================================
# DOCTRINE CACHE - POLYMER CHEMISTRY EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Free Radical Addition Polymerization",
        keywords=["free radical", "vinyl monomers", "initiation", "propagation", "termination", "chain transfer", "kinetics"],
        conclusion_template="Free radical polymerization proceeds via initiation (radical generation), propagation (chain growth), and termination (combination or disproportionation). Rate of polymerization Rp = kp[M][radical]. Degree of polymerization DP = Rp/Rt. Chain transfer to monomer, solvent, or chain transfer agents limits molecular weight.",
        reasoning_framework="""
Free radical addition polymerization is the most common industrial polymerization method for vinyl monomers (ethylene, styrene, vinyl chloride, acrylates, methacrylates).

MECHANISM:
1. Initiation: I -> 2R* (thermal or photochemical decomposition of initiator)
   R* + M -> RM*
2. Propagation: RM* + M -> RMM* -> ... -> RM_n* (rate constant kp)
3. Termination:
   - Combination: RM_n* + RM_m* -> RM_(n+m)
   - Disproportionation: RM_n* + RM_m* -> RM_n + RM_m (unsaturated end)
4. Chain transfer: RM_n* + XA -> RM_nX + A* (X = H, Cl; A = monomer, solvent, CTA)

KINETICS:
- Steady-state assumption: d[R*]/dt = 0
- Rate of initiation Ri = 2f*kd[I] (f = initiator efficiency, kd = decomposition rate constant)
- Rate of propagation Rp = kp[M][R*]
- Rate of termination Rt = 2kt[R*]^2
- Steady state: Ri = Rt -> [R*] = (f*kd[I]/kt)^0.5
- Rp = kp[M](f*kd[I]/kt)^0.5
- Degree of polymerization DP = Rp/Rt or DP = kp[M]/(kt[R*] + ktr[XA])

CHAIN TRANSFER EFFECTS:
- Chain transfer to monomer: limits DP, produces reactive end groups
- Chain transfer to solvent: reduces molecular weight, solvent fragments incorporated
- Chain transfer agents (CTAs): mercaptans, thiols, CCl4 - deliberate MW control
- Chain transfer constant Cs = ktr/kp

INITIATORS:
- Peroxides: benzoyl peroxide (BPO), di-tert-butyl peroxide (DTBP) - thermal
- Azo compounds: AIBN (azobisisobutyronitrile) - clean, N2 byproduct
- Redox initiators: persulfate/Fe2+ - low temperature aqueous polymerization

INDUSTRIAL APPLICATIONS:
- Polyethylene (LDPE): high-pressure free radical (1000-3000 atm, 200-300C)
- Polystyrene: thermal or initiated, bulk or suspension
- PVC: suspension or emulsion polymerization
- Acrylics: PMMA, paints, adhesives

LIMITATIONS:
- Poor control over molecular weight distribution (broad PDI = 1.5-2.0)
- Limited control over chain architecture (no block copolymers)
- Sensitive to oxygen (radical scavenger), requires inert atmosphere
        """,
        key_factors=[
            "Steady-state radical concentration",
            "Monomer reactivity ratios",
            "Initiator efficiency and half-life",
            "Chain transfer constants",
            "Termination mechanism (combination vs disproportionation)",
            "Temperature dependence of rate constants",
            "Oxygen inhibition"
        ],
        primary_authority=[
            "Odian - Principles of Polymerization (4th ed., 2004)",
            "Flory - Principles of Polymer Chemistry (1953)",
            "Stevens - Polymer Chemistry: An Introduction (3rd ed., 1999)"
        ],
        burden_holder="Process engineer to control MW and conversion",
        adversary_position="Batch-to-batch variability, broad MWD, chain defects",
        counter_arguments=[
            "Living/controlled polymerization gives better MW control",
            "Free radical polymerization has poor chain-end functionality",
            "High temperature causes chain transfer and degradation",
            "Oxygen scavenging requires degassing or inert atmosphere",
            "Termination by combination doubles MW uncertainty"
        ],
        resolution_strategy="Use controlled radical polymerization (ATRP, RAFT, NMP) for narrow MWD; use chain transfer agents for MW control; optimize initiator concentration and temperature; remove oxygen by freeze-pump-thaw or N2 purge.",
        entity_scope="Vinyl monomers, industrial commodity polymers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established kinetics, 70+ years of industrial practice, predictable under controlled conditions.",
        controlling_precedent="Flory-Schulz distribution for chain length, Mayo equation for chain transfer",
        issue_category=IssueCategory.POLYMERIZATION_MECHANISM
    ),

    DoctrineBlock(
        topic="Living/Controlled Radical Polymerization (ATRP, RAFT, NMP)",
        keywords=["ATRP", "RAFT", "NMP", "living polymerization", "narrow PDI", "block copolymers", "chain-end functionality"],
        conclusion_template="Controlled radical polymerization (CRP) methods - ATRP (atom transfer), RAFT (reversible addition-fragmentation), NMP (nitroxide-mediated) - allow living character: linear MW growth, narrow PDI (1.05-1.3), chain-end functionality, and block copolymer synthesis. Requires equilibrium between dormant and active chains.",
        reasoning_framework="""
Living/controlled radical polymerization (CRP) combines the versatility of free radical polymerization with the control of living anionic polymerization.

PRINCIPLES:
- Reversible deactivation: active radicals (P*) equilibrate with dormant species (P-X)
- Low steady-state [P*] minimizes termination
- All chains initiate simultaneously, grow at equal rate
- Linear MW vs conversion: Mn = ([M]0/[I]0) * conversion * M_monomer
- Narrow molecular weight distribution: PDI = Mw/Mn = 1.05-1.3
- Chain-end functionality retained: enables block copolymers, chain extension

ATOM TRANSFER RADICAL POLYMERIZATION (ATRP):
- Mechanism: P-X + Cu(I)L <-> P* + Cu(II)X-L (X = Br, Cl; L = ligand)
- Catalyst: Cu(I)Br/Cu(II)Br2 + bipyridine or PMDETA ligand
- Equilibrium constant Keq = kact/kdeact ~ 10^-7 to 10^-9
- Monomers: methacrylates, styrene, acrylates (less controlled)
- Advantages: wide monomer scope, functional group tolerance
- Disadvantages: requires Cu removal, air-sensitive, colored products

REVERSIBLE ADDITION-FRAGMENTATION TRANSFER (RAFT):
- Mechanism: P* + S=C(Z)S-R <-> P-S-C*(Z)-S-R -> P-S-C(Z)=S + R*
- RAFT agent: dithioester, trithiocarbonate, xanthate, dithiocarbamate
- Z group controls reactivity (phenyl for methacrylates, alkyl for vinyl acetate)
- R group must be good leaving group and reinitiate polymerization
- Advantages: no metal catalyst, wide monomer scope, functional tolerance
- Disadvantages: colored products (S=C), retardation at high [RAFT], odor

NITROXIDE-MEDIATED POLYMERIZATION (NMP):
- Mechanism: P-ONR2 <-> P* + *ONR2 (nitroxide traps radical)
- Nitroxides: TEMPO, SG1, TIPNO
- Best for styrene and styrenics (high temperature 110-135C)
- Poor for methacrylates (side reactions)
- Advantages: no catalyst, simple
- Disadvantages: limited monomer scope, high temperature

BLOCK COPOLYMER SYNTHESIS:
1. Polymerize monomer A to desired MW (chain-end = dormant)
2. Add monomer B, continue polymerization
3. Forms AB diblock: PS-b-PMMA, PEO-b-PS, etc.
4. Enables ABA triblocks, ABC terpolymers, gradient copolymers

APPLICATIONS:
- Thermoplastic elastomers (SBS, SIS)
- Drug delivery (PEG-b-PLA, micelles)
- Compatibilizers for polymer blends
- Surface coatings (functionalized end groups)
- Oilfield: ATRP for polyacrylamide with controlled MW for EOR
        """,
        key_factors=[
            "Equilibrium constant between dormant and active chains",
            "Initiator efficiency and reinitiation",
            "RAFT agent or catalyst selection for monomer",
            "Polymerization temperature and time",
            "Monomer conversion and residual functionality",
            "Chain extension efficiency for block copolymers"
        ],
        primary_authority=[
            "Matyjaszewski & Tsarevsky - Nature Chemistry (2009) ATRP review",
            "Moad, Rizzardo, Thang - Aust. J. Chem. (2005) RAFT review",
            "Hawker, Bosman, Harth - Chem. Rev. (2001) CRP review"
        ],
        burden_holder="Polymer chemist to optimize CRP conditions",
        adversary_position="Higher cost, more complex synthesis than free radical",
        counter_arguments=[
            "ATRP requires Cu catalyst (residual metal contamination)",
            "RAFT agents are expensive and malodorous",
            "NMP has limited monomer scope",
            "CRP slower than conventional free radical polymerization",
            "Scale-up challenges for industrial production"
        ],
        resolution_strategy="Select CRP method based on monomer: ATRP for methacrylates/styrene, RAFT for acrylates/vinyl acetate, NMP for styrenics. Use sacrificial initiator or in-situ catalyst reduction for ATRP. Optimize [RAFT]/[initiator] ratio to minimize retardation.",
        entity_scope="Functional polymers, block copolymers, advanced materials",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established methods (20+ years), well-understood kinetics, extensive literature.",
        controlling_precedent="Living polymerization criteria: Mn linear with conversion, narrow PDI, chain-end functionality",
        issue_category=IssueCategory.CONTROLLED_POLYMERIZATION
    ),

    DoctrineBlock(
        topic="Condensation Step-Growth Polymerization",
        keywords=["step-growth", "condensation", "nylon", "polyester", "polycarbonate", "Carothers equation", "extent of reaction"],
        conclusion_template="Step-growth polymerization forms polymers by stepwise reaction of bifunctional monomers with elimination of small molecules (H2O, HCl, MeOH). Requires high conversion (p > 0.99) for high molecular weight: DP = 1/(1-p). Examples: nylon (polyamide), PET (polyester), polycarbonate, epoxy resins.",
        reasoning_framework="""
Condensation or step-growth polymerization builds polymers through stepwise reaction of functional groups (AA + BB or AB monomers) with byproduct elimination.

MECHANISM:
- AA + BB: diacid + diol -> polyester + H2O (PET, polycarbonate)
- AA + BB: diacid + diamine -> polyamide + H2O (nylon-6,6)
- AB: aminoacid -> polyamide + H2O (nylon-6 from caprolactam)
- Each step forms ester, amide, urethane, ether, etc. linkage

CAROTHERS EQUATION:
- Degree of polymerization DP_n = 1/(1-p)
- p = extent of reaction (fraction of functional groups reacted)
- For DP_n = 100, need p = 0.99 (99% conversion)
- For DP_n = 200, need p = 0.995 (99.5% conversion)
- CRITICAL: High conversion essential for high MW

STOICHIOMETRY:
- For AA + BB: must have exact 1:1 ratio (r = [A]/[B] = 1)
- Off-stoichiometry limits MW: DP_n = (1+r)/(1+r-2rp) (r < 1)
- Monofunctional impurity acts as chain stopper

MOLECULAR WEIGHT DISTRIBUTION:
- Flory-Schulz distribution (most probable distribution)
- PDI = Mw/Mn = 1 + p (at high conversion, PDI ~ 2.0)
- Broader than living polymerization but narrower than free radical

EXAMPLES:
1. Nylon-6,6: HOOC-(CH2)4-COOH + H2N-(CH2)6-NH2 -> [-CO-(CH2)4-CO-NH-(CH2)6-NH-]n + H2O
   - Melt polymerization 260-280C, autoclave, remove water
   - Fiber-forming polymer (Tm ~ 265C)

2. PET (polyethylene terephthalate): dimethyl terephthalate + ethylene glycol -> PET + MeOH
   - Transesterification then polycondensation
   - Bottle resin (Tg ~ 80C, Tm ~ 265C)

3. Polycarbonate: bisphenol A + phosgene -> polycarbonate + HCl
   - Interfacial polymerization or melt transesterification
   - Engineering plastic (Tg ~ 150C, tough, transparent)

4. Epoxy resins: DGEBA (diglycidyl ether of bisphenol A) + diamine -> crosslinked epoxy
   - Thermosetting polymer, excellent adhesion and chemical resistance

INDUSTRIAL CONSIDERATIONS:
- Remove condensate (water, alcohol, HCl) to drive equilibrium: vacuum, inert gas sweep
- High purity monomers (impurities act as chain stoppers)
- End-group analysis to determine stoichiometry
- Melt polymerization (high Tm polymers) or solution/interfacial (sensitive polymers)
- Post-polymerization (solid-state polymerization for PET bottles)

OILFIELD APPLICATIONS:
- Epoxy resins: pipe coatings, adhesives, composite repair
- Polyamides: drilling fluid additives (shale stabilization)
- Polyurethanes: foam cement, lost circulation materials
        """,
        key_factors=[
            "Extent of reaction (p > 0.99 for high MW)",
            "Stoichiometric balance of functional groups",
            "Purity of monomers (no monofunctional impurities)",
            "Efficient removal of condensation byproduct",
            "Reaction temperature and catalyst",
            "End-group functionality for chain extension"
        ],
        primary_authority=[
            "Carothers - Trans. Faraday Soc. (1936) - DP equation",
            "Flory - J. Am. Chem. Soc. (1936) - MWD theory",
            "Odian - Principles of Polymerization (Ch. 2, Step Polymerization)"
        ],
        burden_holder="Process engineer to achieve p > 0.99 and exact stoichiometry",
        adversary_position="Difficult to reach high MW, sensitive to impurities",
        counter_arguments=[
            "Requires near-perfect stoichiometry (1:1 ratio)",
            "Small impurities drastically reduce MW",
            "Reverse reaction (hydrolysis) if water not removed",
            "Slow reaction kinetics compared to chain-growth",
            "Difficult to control MW distribution (PDI ~ 2)"
        ],
        resolution_strategy="Use high-purity monomers, precise stoichiometry (titration, end-group analysis), efficient condensate removal (vacuum, Dean-Stark trap), catalyst if needed (acid for esterification, base for transesterification), post-polymerization in solid state if necessary.",
        entity_scope="Polyamides, polyesters, polycarbonates, epoxies, polyurethanes",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established theory (Carothers 1930s), industrially validated for nylon and PET production.",
        controlling_precedent="Carothers equation DP = 1/(1-p), stoichiometry requirement for high MW",
        issue_category=IssueCategory.POLYMERIZATION_MECHANISM
    ),

    DoctrineBlock(
        topic="Molecular Weight Distribution and GPC/SEC",
        keywords=["GPC", "SEC", "Mn", "Mw", "PDI", "polydispersity", "elution volume", "calibration"],
        conclusion_template="Gel permeation chromatography (GPC) or size exclusion chromatography (SEC) separates polymers by hydrodynamic volume. Determines number-average MW (Mn), weight-average MW (Mw), and polydispersity index (PDI = Mw/Mn). Narrow PDI (1.05-1.3) indicates controlled polymerization; broad PDI (1.5-2.5) indicates free radical or step-growth.",
        reasoning_framework="""
Molecular weight distribution (MWD) is critical for polymer properties: mechanical strength, viscosity, processing, and end-use performance.

DEFINITIONS:
- Number-average MW: Mn = Σ(Ni*Mi)/ΣNi (sensitive to low-MW species)
- Weight-average MW: Mw = Σ(Ni*Mi^2)/Σ(Ni*Mi) (sensitive to high-MW species)
- Z-average MW: Mz = Σ(Ni*Mi^3)/Σ(Ni*Mi^2) (even more sensitive to high-MW tail)
- Polydispersity index: PDI = Mw/Mn (1.0 = monodisperse, 2.0 = most probable)

PHYSICAL SIGNIFICANCE:
- Mn affects colligative properties (osmotic pressure, freezing point depression)
- Mw affects light scattering, viscosity
- PDI affects mechanical properties (narrow PDI = better tensile strength, broader PDI = toughness)
- Low-MW fraction: reduces Tg, acts as plasticizer, lowers melt viscosity
- High-MW fraction: increases melt viscosity, improves strength

GEL PERMEATION CHROMATOGRAPHY (GPC/SEC):
PRINCIPLE:
- Porous gel beads (crosslinked polystyrene or silica)
- Small molecules enter pores (long elution time)
- Large molecules excluded (short elution time)
- Separation by hydrodynamic volume Vh, NOT molecular weight

PROCEDURE:
1. Dissolve polymer in mobile phase (THF, chloroform, DMF, water)
2. Inject into column packed with porous beads
3. Detect by RI (refractive index), UV, or light scattering
4. Elution volume Ve correlates with hydrodynamic volume
5. Calibrate with narrow-MW standards (polystyrene, PMMA, PEG)

CALIBRATION:
- Universal calibration: [eta]*M = K*Ve (Mark-Houwink-Sakurada)
- [eta] = intrinsic viscosity, K and a are polymer-specific constants
- For unknown polymer, need Mark-Houwink parameters or use light scattering detector

DETECTORS:
- Refractive index (RI): universal but not absolute MW
- UV: for polymers with chromophores
- Light scattering (MALS, RALS): absolute MW, no calibration needed
- Viscometer: intrinsic viscosity, combined with RI gives universal calibration

TYPICAL PDI VALUES:
- Living anionic polymerization: PDI = 1.01-1.05 (very narrow)
- ATRP/RAFT/NMP: PDI = 1.05-1.3 (controlled)
- Free radical polymerization: PDI = 1.5-2.0 (broad)
- Step-growth polymerization: PDI ~ 2.0 (Flory-Schulz)
- Commercial polymers: PDI = 2-10 (blends, branching, degradation)

OILFIELD EXAMPLE:
- Polyacrylamide for EOR: target MW 8-20 million Da, PDI 2-4
- GPC with aqueous mobile phase (0.1M NaNO3), PEG/PEO standards
- High MW improves viscosity but reduces injectivity (shear degradation)
- PDI affects filterability and thermal stability
        """,
        key_factors=[
            "Column packing (pore size distribution)",
            "Mobile phase (solvent, flow rate, temperature)",
            "Calibration standards (PS, PMMA, PEG)",
            "Detector type (RI, UV, LS, viscometer)",
            "Sample concentration and injection volume",
            "Mark-Houwink parameters for universal calibration"
        ],
        primary_authority=[
            "Grubisic, Rempp, Benoit - J. Polym. Sci. B (1967) - Universal calibration",
            "ASTM D6579 - Standard Practice for GPC",
            "Striegel et al. - Modern Size-Exclusion Chromatography (2009)"
        ],
        burden_holder="Analyst to select proper calibration and mobile phase",
        adversary_position="Calibration errors, column resolution limits, aggregation artifacts",
        counter_arguments=[
            "PS calibration invalid for polymers with different hydrodynamic volume",
            "Column degradation over time changes calibration",
            "Aggregation in poor solvent gives artificially high MW",
            "Shear degradation during injection reduces high-MW tail",
            "RI detector cannot distinguish MW from concentration changes"
        ],
        resolution_strategy="Use light scattering detector for absolute MW (no calibration needed), triple-detection GPC (RI + LS + viscometer) for universal calibration, verify calibration with narrow standards, filter samples (0.45 micron) to remove aggregates, use appropriate solvent (good solvent, not theta or poor).",
        entity_scope="All synthetic polymers, molecular weight characterization",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard analytical technique (ASTM methods), well-validated for 50+ years.",
        controlling_precedent="Universal calibration [eta]*M vs Ve, Mark-Houwink-Sakurada equation",
        issue_category=IssueCategory.MOLECULAR_WEIGHT
    ),

    DoctrineBlock(
        topic="Thermal Analysis: DSC (Differential Scanning Calorimetry)",
        keywords=["DSC", "Tg", "Tm", "Tc", "glass transition", "melting point", "crystallization", "heat capacity"],
        conclusion_template="Differential scanning calorimetry (DSC) measures heat flow vs temperature. Determines glass transition temperature Tg (amorphous polymers), melting point Tm (semicrystalline polymers), crystallization temperature Tc, heat capacity Cp, and enthalpy of fusion. Tg depends on chain flexibility; Tm depends on crystallinity and chain regularity.",
        reasoning_framework="""
Differential scanning calorimetry (DSC) is the primary thermal analysis technique for polymers, providing transition temperatures critical for processing and application.

PRINCIPLE:
- Sample and reference pan heated at constant rate (typically 10C/min)
- Measure heat flow difference: dQ/dt
- Endothermic transitions (melting): heat absorbed, peak down
- Exothermic transitions (crystallization): heat released, peak up
- Glass transition: step change in heat capacity, not a peak

GLASS TRANSITION TEMPERATURE (Tg):
DEFINITION: Temperature where polymer transitions from glassy (rigid) to rubbery (flexible) state. Amorphous phase transition, not first-order.

DSC SIGNATURE:
- Step increase in heat capacity (Cp)
- Midpoint of step = Tg
- Width of transition ~ 10-20C

FACTORS AFFECTING Tg:
1. Chain flexibility: flexible backbone (polyethylene, PDMS) -> low Tg; rigid backbone (polystyrene, polycarbonate) -> high Tg
2. Bulky side groups: increase Tg (polystyrene Tg 100C vs polyethylene -120C)
3. Molecular weight: Tg increases with MW, plateaus at MW > 20,000 (Fox-Flory equation)
4. Crosslinking: increases Tg (thermosets have no Tg, decompose before softening)
5. Plasticizers: lower Tg (PVC + DOP: Tg drops from 80C to -20C)
6. Copolymerization: Fox equation 1/Tg = w1/Tg1 + w2/Tg2

TYPICAL Tg VALUES:
- PDMS (silicone): -123C (very flexible Si-O backbone)
- Polyethylene: -120C (flexible C-C backbone)
- Polypropylene: -10C (methyl side group)
- PVC: 80C (Cl side group restricts rotation)
- Polystyrene: 100C (bulky phenyl side group)
- PMMA: 105C (ester + methyl side groups)
- Polycarbonate: 150C (rigid bisphenol A unit)
- PET: 80C (amorphous), semicrystalline complicates Tg measurement

MELTING POINT (Tm):
DEFINITION: Temperature where crystalline regions melt. First-order transition.

DSC SIGNATURE:
- Endothermic peak (sharp for high crystallinity, broad for low crystallinity)
- Peak maximum = Tm
- Area under peak = enthalpy of fusion ΔHf
- Percent crystallinity Xc = ΔHf_sample / ΔHf_100% crystalline

FACTORS AFFECTING Tm:
1. Chain regularity: isotactic/syndiotactic > atactic (atactic cannot crystallize)
2. Chain flexibility: flexible chains crystallize more easily
3. Intermolecular forces: H-bonding (nylon, polyurethane) increases Tm
4. Chain symmetry: even number of carbons (nylon-6,6) higher Tm than odd

TYPICAL Tm VALUES:
- LDPE (low-density polyethylene): 110C (branching reduces crystallinity)
- HDPE (high-density polyethylene): 130C (linear chains, high crystallinity)
- Polypropylene (isotactic): 165C
- Nylon-6,6: 265C (H-bonding)
- PET: 265C
- PTFE (Teflon): 327C (strong C-F bonds, high crystallinity)

CRYSTALLIZATION TEMPERATURE (Tc):
- Exothermic peak on cooling scan
- Tc < Tm (supercooling required for nucleation)
- Slow cooling -> higher Tc, larger crystals
- Fast cooling (quench) -> low Tc or no crystallization (amorphous)

HEAT CAPACITY (Cp):
- Jump at Tg: ΔCp = Cp_rubbery - Cp_glassy ~ 0.3-0.5 J/g/K
- Used to calculate amorphous fraction in semicrystalline polymers

OILFIELD APPLICATIONS:
- Drilling fluid polymers: must remain functional above bottomhole temperature (BHT)
- PVDF (polyvinylidene fluoride): Tg -40C, Tm 177C -> excellent chemical resistance at high T
- Elastomers for seals: Tg must be below minimum operating temperature
        """,
        key_factors=[
            "Heating/cooling rate (affects peak sharpness)",
            "Sample mass (5-10 mg typical)",
            "Pan type (hermetic for volatiles, open for decomposition)",
            "Thermal history (quench vs slow cool affects crystallinity)",
            "Atmosphere (N2, air, O2 affects oxidation)",
            "Baseline correction and peak integration"
        ],
        primary_authority=[
            "ASTM D3418 - Transition Temperatures of Polymers by DSC",
            "Wunderlich - Thermal Analysis of Polymeric Materials (2005)",
            "Menczel & Prime - Thermal Analysis of Polymers (2009)"
        ],
        burden_holder="Analyst to control heating rate and interpret transitions",
        adversary_position="Overlapping transitions, thermal degradation, insufficient sample",
        counter_arguments=[
            "Tg depends on heating rate (faster rate -> higher apparent Tg)",
            "Semicrystalline polymers: Tg obscured by crystallinity",
            "Multiple Tm peaks indicate recrystallization or polymorphism",
            "Thermal degradation during heating gives artifacts",
            "Water or solvent evaporation complicates baseline"
        ],
        resolution_strategy="Run multiple heating rates (5, 10, 20 C/min) and extrapolate to zero rate, use heat-cool-heat protocol (erase thermal history on first heat, measure on second heat), dry sample in vacuum oven before DSC, use modulated DSC (MDSC) to separate reversing (Tg) and non-reversing (crystallization) heat flow.",
        entity_scope="All polymers, thermal transitions for processing and application",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard technique (ASTM methods), well-established theory, routine QC and R&D use.",
        controlling_precedent="Tg = amorphous transition, Tm = crystalline melting, ΔHf for percent crystallinity",
        issue_category=IssueCategory.THERMAL_ANALYSIS
    ),

    DoctrineBlock(
        topic="Polymer Rheology and Viscoelasticity",
        keywords=["viscosity", "shear thinning", "Newtonian", "viscoelastic", "storage modulus", "loss modulus", "Cox-Merz rule"],
        conclusion_template="Polymer melts and solutions exhibit viscoelastic behavior: elastic (solid-like) and viscous (liquid-like) response. Shear thinning (pseudoplastic) is common: viscosity decreases with shear rate. Characterized by viscosity eta(gamma_dot), storage modulus G', loss modulus G'', and complex viscosity eta*. Cox-Merz rule relates steady shear to dynamic oscillatory measurements.",
        reasoning_framework="""
Rheology is the study of flow and deformation of materials. Polymers are viscoelastic: they exhibit both viscous flow (liquids) and elastic deformation (solids).

NEWTONIAN vs NON-NEWTONIAN FLOW:
- Newtonian fluid: eta = constant (independent of shear rate gamma_dot)
  Examples: water, low-MW oils, dilute polymer solutions
- Non-Newtonian fluid: eta = f(gamma_dot)
  - Shear thinning (pseudoplastic): eta decreases with gamma_dot (most polymer melts and solutions)
  - Shear thickening (dilatant): eta increases with gamma_dot (rare, concentrated suspensions)

SHEAR THINNING MECHANISM:
At rest: polymer coils entangled, high viscosity
At low shear: some disentanglement, moderate viscosity reduction
At high shear: chains align with flow, disentangle, viscosity drops significantly
Power-law model: eta = K * gamma_dot^(n-1), where n < 1 for shear thinning

ZERO-SHEAR VISCOSITY (eta_0):
- Viscosity at gamma_dot -> 0 (low shear rate plateau)
- Depends on molecular weight: eta_0 ~ MW^3.4 (above entanglement MW)
- Reflects equilibrium entanglement density

CRITICAL SHEAR RATE:
- Onset of shear thinning: gamma_dot_c ~ 1/tau (tau = longest relaxation time)
- Depends on molecular weight and temperature
- For HDPE melt at 190C: gamma_dot_c ~ 0.1 s^-1

VISCOELASTIC MODULI (dynamic oscillatory shear):
- Apply sinusoidal strain: gamma(t) = gamma_0 * sin(omega*t)
- Measure stress response: sigma(t) = gamma_0 * [G' * sin(omega*t) + G'' * cos(omega*t)]
- Storage modulus G': elastic component (energy stored and recovered)
- Loss modulus G'': viscous component (energy dissipated as heat)
- Complex modulus G* = sqrt(G'^2 + G''^2)
- Complex viscosity eta* = G*/omega
- Loss tangent tan(delta) = G''/G' (delta = phase angle)

INTERPRETATION:
- G' > G'': elastic-dominated (solid-like), tan(delta) < 1
- G'' > G': viscous-dominated (liquid-like), tan(delta) > 1
- Crossover frequency (G' = G''): characteristic relaxation time

COX-MERZ RULE:
- Empirical relationship: eta(gamma_dot) = eta*(omega) when gamma_dot = omega
- Relates steady shear viscosity to complex viscosity from oscillatory measurements
- Valid for linear, flexible polymers; fails for branched or filled polymers

TEMPERATURE DEPENDENCE:
- Williams-Landel-Ferry (WLF) equation (near Tg): log(aT) = -C1*(T-Tref)/(C2+T-Tref)
- Arrhenius equation (far above Tg): eta = A * exp(Ea/RT)
- Time-temperature superposition (TTS): shift curves at different T to master curve

MOLECULAR WEIGHT DEPENDENCE:
- Below entanglement MW (Me): eta_0 ~ MW (Rouse model)
- Above Me: eta_0 ~ MW^3.4 (reptation model, Doi-Edwards theory)
- For HDPE: Me ~ 1,000 g/mol, crossover at MW ~ 10,000

OILFIELD APPLICATIONS:
- Polymer flooding (EOR): polyacrylamide viscosity vs shear rate in porous media
- Shear thinning: allows injection (high shear) but viscosity recovery in reservoir (low shear)
- Drilling fluids: xanthan gum, PAC (polyanionic cellulose) - shear thinning for pumpability
- Fracturing fluids: guar gum, HPG (hydroxypropyl guar) - high viscosity at low shear (proppant suspension), low viscosity at high shear (pumping)
- Viscosity specification at reservoir shear rate (typically 1-10 s^-1 in core flood tests)
        """,
        key_factors=[
            "Molecular weight and distribution",
            "Temperature (above or below Tg)",
            "Shear rate or frequency range",
            "Polymer concentration (dilute, semi-dilute, concentrated)",
            "Branching and architecture (linear vs star vs comb)",
            "Filler or additive interactions"
        ],
        primary_authority=[
            "Doi & Edwards - The Theory of Polymer Dynamics (1986)",
            "Ferry - Viscoelastic Properties of Polymers (3rd ed., 1980)",
            "Larson - The Structure and Rheology of Complex Fluids (1999)"
        ],
        burden_holder="Rheologist to characterize flow behavior for processing",
        adversary_position="Complex flow behavior, shear heating, time-dependent effects",
        counter_arguments=[
            "Cox-Merz rule fails for branched polymers (LDPE, LLDPE)",
            "Shear heating during measurement changes apparent viscosity",
            "Wall slip at high shear rates gives artificially low viscosity",
            "Thixotropy (time-dependent shear thinning) complicates interpretation",
            "Entanglement dynamics depend on polydispersity (broad MWD)"
        ],
        resolution_strategy="Use parallel-plate or cone-plate geometry (controlled gap), control temperature precisely (Peltier or circulating bath), measure over wide shear rate range (10^-3 to 10^3 s^-1), apply time-temperature superposition to extend frequency range, use slip-resistant surfaces (serrated plates) if wall slip suspected.",
        entity_scope="Polymer melts, solutions, and composites - processing and flow",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established theory (Ferry, Doi-Edwards), standard industrial characterization (ASTM D4440).",
        controlling_precedent="Shear thinning for polymer melts, eta_0 ~ MW^3.4 above Me, Cox-Merz rule for linear polymers",
        issue_category=IssueCategory.RHEOLOGY
    ),

    DoctrineBlock(
        topic="Polymer Processing: Injection Molding",
        keywords=["injection molding", "fill time", "packing pressure", "cooling time", "shrinkage", "warpage", "gate location"],
        conclusion_template="Injection molding is the primary method for thermoplastic parts. Molten polymer injected into mold cavity, packed under pressure, cooled, and ejected. Key parameters: melt temperature, injection speed, packing pressure, cooling time. Common defects: short shots, sink marks, warpage, flash. Processing window determined by rheology and thermal properties.",
        reasoning_framework="""
Injection molding is a high-volume, automated process for complex thermoplastic parts (automotive, consumer goods, medical devices).

PROCESS STEPS:
1. PLASTICIZATION: Polymer pellets fed into heated barrel, melted by shear heating (screw rotation) and external heaters. Melt temperature 20-40C above Tm (semicrystalline) or Tg + 100C (amorphous).

2. INJECTION: Screw acts as ram, injects melt into closed mold cavity at high pressure (50-150 MPa). Fill time 0.5-3 seconds. High shear rates (100-10,000 s^-1) cause shear thinning, reduce viscosity, improve mold filling.

3. PACKING: After cavity filled, hold pressure applied (30-80% of injection pressure) to compensate for shrinkage during cooling. Packing time 5-20 seconds.

4. COOLING: Mold cooled by circulating water (20-80C). Cooling time 10-60 seconds (depends on part thickness, polymer thermal diffusivity). Part temperature must drop below Tg (amorphous) or Tc (semicrystalline) before ejection.

5. EJECTION: Mold opens, part ejected by pins or stripper plate. Cycle time = fill + pack + cool + eject, typically 20-90 seconds.

KEY PARAMETERS:
- Melt temperature: too low -> short shots, high pressure; too high -> degradation, long cooling
- Injection speed: too slow -> premature freezing; too fast -> jetting, air traps
- Packing pressure: too low -> sink marks, voids; too high -> flash, high residual stress
- Cooling time: too short -> warpage, dimensional instability; too long -> low productivity
- Mold temperature: affects surface finish, crystallinity, shrinkage

MOLD DESIGN:
- Gate location: controls flow front, weld lines, air traps (gate at thickest section)
- Runner system: sprue, runners, gates (hot runner eliminates scrap)
- Cooling channels: uniform cooling prevents warpage (conformal cooling for complex shapes)
- Venting: air escape to prevent burn marks and incomplete filling
- Draft angle: 1-3 degrees for easy ejection

SHRINKAGE:
- Volumetric shrinkage on cooling: ΔV/V ~ 2-8% (semicrystalline > amorphous)
- Linear shrinkage: 0.3-2% (PP > PE > PS > PC)
- Anisotropic shrinkage: higher in flow direction (molecular orientation)
- Mold compensates for shrinkage (mold cavity larger than final part)

COMMON DEFECTS:
- Short shot: incomplete filling (low melt temp, high viscosity, inadequate pressure)
- Sink marks: surface depression over thick sections (inadequate packing)
- Warpage: uneven cooling, residual stress, anisotropic shrinkage
- Flash: melt leaks at parting line (excessive pressure, worn mold)
- Weld lines: two flow fronts meet, weak bond (increase melt temp, relocate gate)
- Burn marks: trapped air ignites (improve venting)
- Jetting: melt stream solidifies before filling (reduce injection speed, increase melt temp)

MATERIAL SELECTION:
- Commodity resins: PE, PP, PS, PVC (low cost, easy processing)
- Engineering resins: nylon, PET, PC, POM (higher strength, temp resistance)
- High-performance: PEEK, PPS, LCP (extreme temp, chemical resistance)

OILFIELD EXAMPLE:
- Downhole tool housings: glass-filled nylon or PEEK (high temp, high strength)
- Valve components: PTFE-filled PEEK (chemical resistance, low friction)
- Injection molding for small production runs (< 10,000 parts), CNC machining for prototypes
        """,
        key_factors=[
            "Polymer rheology (shear thinning, melt viscosity)",
            "Thermal properties (Tg, Tm, thermal diffusivity)",
            "Mold temperature and cooling rate",
            "Gate location and runner design",
            "Packing pressure and hold time",
            "Part geometry (wall thickness uniformity)"
        ],
        primary_authority=[
            "Tadmor & Gogos - Principles of Polymer Processing (2nd ed., 2006)",
            "Osswald et al. - Injection Molding Handbook (2nd ed., 2008)",
            "ASTM D955 - Measuring Shrinkage from Mold Dimensions"
        ],
        burden_holder="Mold designer and process engineer to optimize cycle time and part quality",
        adversary_position="Defects from poor processing, high tooling cost, limited to thermoplastics",
        counter_arguments=[
            "High initial tooling cost ($10K-$100K+ per mold)",
            "Long lead time for mold fabrication (4-12 weeks)",
            "Design changes expensive after mold made",
            "Shrinkage and warpage difficult to predict (FEA simulation needed)",
            "Degradation of heat-sensitive polymers (PVC, POM) at high melt temps"
        ],
        resolution_strategy="Use moldflow simulation (Autodesk Moldflow, Moldex3D) to optimize gate location and cooling channels, prototype with 3D printing or soft tooling, design for manufacturability (uniform wall thickness, avoid sharp corners), use scientific molding approach (DOE to establish process window), monitor cavity pressure and melt temperature in real time.",
        entity_scope="Thermoplastic parts, high-volume production",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Mature process (60+ years), well-understood physics, extensive industrial experience.",
        controlling_precedent="Shear thinning enables mold filling, cooling time limits cycle time, shrinkage compensation in mold design",
        issue_category=IssueCategory.POLYMER_PROCESSING
    ),

    DoctrineBlock(
        topic="Polymer Degradation: Thermal, UV, Oxidative, Hydrolytic",
        keywords=["degradation", "thermal stability", "UV stabilizers", "antioxidants", "chain scission", "crosslinking", "lifetime prediction"],
        conclusion_template="Polymer degradation occurs via thermal (heat), UV (sunlight), oxidative (oxygen), or hydrolytic (water) mechanisms. Leads to chain scission (MW reduction, embrittlement) or crosslinking (hardening, loss of ductility). Stabilizers extend lifetime: antioxidants, UV absorbers, HALS. Arrhenius kinetics for lifetime prediction.",
        reasoning_framework="""
Polymer degradation limits service life in applications exposed to heat, light, oxygen, or moisture. Understanding degradation mechanisms enables stabilizer selection and lifetime prediction.

THERMAL DEGRADATION:
MECHANISM:
- Chain scission: random or end-chain (unzipping) cleavage of C-C bonds
- Crosslinking: radical recombination forms crosslinks (thermosets, elastomers)
- Volatile formation: monomers, oligomers, small molecules (depolymerization)

FACTORS:
- Bond dissociation energy (BDE): C-C 350 kJ/mol, C-O 360, C-N 305, C-Cl 330, C-F 485
- PTFE most stable (high C-F BDE), PVC least stable (HCl elimination at 150C)
- Oxygen accelerates degradation (thermo-oxidative > pure thermal)

KINETICS:
- Arrhenius equation: k = A * exp(-Ea/RT)
- Activation energy Ea ~ 100-200 kJ/mol for most polymers
- Time-temperature superposition: 10C increase -> 2x degradation rate (rough rule)

STABILIZATION:
- Antioxidants: primary (radical scavengers, hindered phenols), secondary (peroxide decomposers, phosphites)
- Heat stabilizers for PVC: metal soaps (Ca/Zn stearate), organotin compounds
- Inert atmosphere (N2, vacuum) eliminates oxidative component

UV DEGRADATION:
MECHANISM:
- UV photons (290-400 nm) break C-C, C-H, C=O bonds
- Free radicals formed -> chain scission or crosslinking
- Chromophores (C=O, aromatic rings) absorb UV, initiate degradation
- Photooxidation: UV + O2 -> hydroperoxides -> chain scission

SUSCEPTIBLE POLYMERS:
- Polypropylene: tertiary C-H readily abstracts, rapid embrittlement
- Polystyrene: phenyl ring absorbs UV, yellowing
- Polycarbonate: bisphenol A structure degrades, loses transparency
- Polyurethanes: aromatic isocyanates -> yellowing, chain scission

RESISTANT POLYMERS:
- Polyethylene: no chromophores (but additives may absorb UV)
- PTFE: C-F bonds resist UV
- Acrylics (PMMA): outdoor stability, UV-transparent

STABILIZATION:
- UV absorbers: benzophenone, benzotriazole (absorb UV, dissipate as heat)
- HALS (hindered amine light stabilizers): scavenge radicals, regenerate (catalytic)
- Pigments: carbon black (excellent UV screen, opaque), TiO2 (reflective, white)
- Surface coatings: UV-resistant clearcoats, sacrificial layers

OXIDATIVE DEGRADATION:
MECHANISM:
- Autoxidation: R-H + O2 -> R* + HOO* -> ROOH (hydroperoxide)
- Hydroperoxide decomposition: ROOH -> RO* + *OH (propagation)
- Chain scission at ether or carbonyl groups

FACTORS:
- Temperature accelerates (thermo-oxidative synergy)
- Transition metals (Fe, Cu) catalyze hydroperoxide decomposition
- Strain (stressed polymers oxidize faster, environmental stress cracking)

STABILIZATION:
- Primary antioxidants: donate H to radicals, hindered phenols (BHT, Irganox 1010)
- Secondary antioxidants: decompose hydroperoxides, phosphites (Irgafos 168), thioesters
- Synergistic blends: phenol + phosphite (commercial packages)

HYDROLYTIC DEGRADATION:
MECHANISM:
- Water attacks ester, amide, urethane, carbonate linkages
- Acid or base catalysis accelerates hydrolysis
- pH < 7 or pH > 7 -> faster degradation than neutral water

SUSCEPTIBLE POLYMERS:
- Polyesters (PET, PLA, polycarbonate): ester hydrolysis at elevated temp
- Polyamides (nylon): amide hydrolysis, plasticization by water absorption
- Polyurethanes: urethane and urea linkages hydrolyze

RESISTANT POLYMERS:
- Polyolefins (PE, PP): no hydrolyzable groups
- Polystyrene, PTFE, PVDF: stable to water

FACTORS:
- Temperature: 10C increase -> 2-3x hydrolysis rate
- pH: acidic or basic environments accelerate
- Water activity: RH, immersion vs vapor exposure

STABILIZATION:
- Carbodiimide stabilizers: react with carboxylic acid end groups (PET bottles)
- Drying before processing: remove moisture (nylon, PET dried to < 0.02% H2O)
- Barrier layers: EVOH, nylon 6 (reduce water permeation)

LIFETIME PREDICTION:
- Arrhenius extrapolation from accelerated aging (high T, UV, O2)
- ASTM D5510 (soil burial), D6691 (compost), E1980 (solar exposure)
- Service life = f(T, UV, O2, stress) - complex models (FEA + degradation kinetics)

OILFIELD APPLICATIONS:
- Downhole elastomers: HNBR, FKM (fluoroelastomer) resist thermal and chemical degradation at 150-200C
- Tubing materials: PVDF, PEEK resist H2S, CO2, brine at elevated temperature
- Lifetime prediction for seals, packers: Arrhenius extrapolation from 200C aging tests
        """,
        key_factors=[
            "Temperature and oxygen concentration",
            "UV exposure (outdoor vs indoor)",
            "Humidity and pH",
            "Mechanical stress (ESC - environmental stress cracking)",
            "Polymer structure (presence of tertiary C-H, chromophores, hydrolyzable groups)",
            "Stabilizer type and concentration"
        ],
        primary_authority=[
            "Zweifel et al. - Plastics Additives Handbook (6th ed., 2009)",
            "ASTM D5510 - Biodegradation in soil",
            "ISO 4892 - Weathering and exposure to laboratory light sources"
        ],
        burden_holder="Materials engineer to select stabilizers and predict lifetime",
        adversary_position="Complex degradation kinetics, synergistic effects, variability in field conditions",
        counter_arguments=[
            "Accelerated aging over-predicts degradation (higher activation energy than service)",
            "Synergistic degradation (UV + thermal + stress) not additive",
            "Stabilizer depletion over time (migration, volatilization, consumption)",
            "Microstructure changes (crystallinity, orientation) affect degradation rate",
            "Field conditions (humidity cycles, UV intermittency) differ from lab tests"
        ],
        resolution_strategy="Use multiple stabilizers (antioxidant + UV absorber + HALS), conduct accelerated aging at multiple temperatures (Arrhenius plot), validate with outdoor weathering (Arizona, Florida), monitor degradation markers (carbonyl index by FTIR, Mw by GPC), design for replacement (modular components, inspection intervals).",
        entity_scope="All polymers exposed to heat, light, oxygen, or water",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Lifetime prediction uncertain (extrapolation from accelerated tests), but mechanisms well-understood.",
        controlling_precedent="Arrhenius kinetics for thermal degradation, UV stabilization via HALS and absorbers, hydrolysis of ester/amide linkages",
        issue_category=IssueCategory.DEGRADATION
    ),

    DoctrineBlock(
        topic="Polymer Blends and Compatibilization",
        keywords=["polymer blend", "miscibility", "phase separation", "compatibilizer", "impact modifier", "Flory-Huggins", "interfacial tension"],
        conclusion_template="Polymer blends combine two or more polymers to achieve property balance (toughness + stiffness, processability + performance). Most polymer pairs are immiscible (phase-separated) due to low entropy of mixing. Compatibilizers (block or graft copolymers) reduce interfacial tension, stabilize morphology, improve mechanical properties.",
        reasoning_framework="""
Polymer blends are physical mixtures (no chemical reaction) of two or more polymers, used to achieve properties unattainable by single polymers.

THERMODYNAMICS OF MIXING:
Gibbs free energy: ΔG_mix = ΔH_mix - TΔS_mix
For miscibility: ΔG_mix < 0

ENTROPY OF MIXING:
- For small molecules: ΔS_mix large (many configurations)
- For polymers: ΔS_mix small (long chains, few configurations)
- Flory-Huggins theory: ΔS_mix ~ (1/N1 + 1/N2) where N = degree of polymerization
- High MW polymers: ΔS_mix -> 0, mixing entropically unfavorable

ENTHALPY OF MIXING:
- Flory-Huggins parameter chi: ΔH_mix ~ chi * phi1 * phi2
- chi > 0: unfavorable interactions (phase separation)
- chi < 0: favorable interactions (miscibility, rare)
- For miscibility: chi < chi_critical ~ 2/(N1^0.5 + N2^0.5)
- Example: PS/PVME miscible (chi < 0 due to weak H-bonding), but most pairs immiscible

CONCLUSION: Most polymer blends are IMMISCIBLE (two-phase morphology).

MORPHOLOGY OF IMMISCIBLE BLENDS:
- Dispersed phase (minor component, droplets) in continuous matrix (major component)
- Morphology depends on: composition, viscosity ratio, interfacial tension, processing shear
- Co-continuous morphology: ~50/50 composition, both phases continuous (synergistic properties)

COMPATIBILIZATION:
PURPOSE: Reduce interfacial tension gamma_12, stabilize fine morphology, improve adhesion between phases.

METHODS:
1. Block or graft copolymers: A-B diblock or A-g-B graft copolymer
   - A block anchors in phase A, B block in phase B
   - Reduces gamma_12, acts as interfacial "glue"
   - Example: PS-b-PMMA compatibilizes PS/PMMA blend

2. Reactive compatibilization: in-situ copolymer formation during mixing
   - Maleic anhydride-grafted PP (PP-g-MA) + PA (nylon) -> PP-g-PA at interface
   - Epoxy-functionalized polymer + carboxyl or amine groups

3. Core-shell impact modifiers: rubber core (elastomer), glassy shell (PMMA, PS)
   - Toughens brittle polymers (PVC, PLA)
   - Shell provides compatibility, core provides toughness

EXAMPLES:
1. High-Impact Polystyrene (HIPS): PS + polybutadiene rubber (5-15%)
   - Rubber phase dispersed as 1-5 micron particles
   - PS-b-PB block copolymer forms in-situ during polymerization (compatibilizer)
   - Toughness 10x higher than pure PS, impact resistance for appliances

2. ABS (acrylonitrile-butadiene-styrene): PB rubber + SAN matrix
   - SAN (styrene-acrylonitrile copolymer) grafted to PB during polymerization
   - Excellent toughness + processability, automotive/electronics

3. PPE/HIPS (Noryl): poly(phenylene ether) + HIPS
   - PPE high Tg (210C) but difficult to process, HIPS easy to process
   - Blend: Tg 140-180C, good toughness, improved processability

4. PC/ABS: polycarbonate + ABS
   - PC high strength/transparency, ABS good processability/toughness
   - Compatibilizer not required (some miscibility), automotive panels

CHARACTERIZATION:
- Morphology: SEM, TEM (phase size, distribution)
- Miscibility: DSC (single Tg = miscible, two Tg = immiscible)
- Interfacial adhesion: impact strength, tensile strength, notched Izod

OILFIELD EXAMPLE:
- PVDF/PMMA blend: PVDF chemical resistance, PMMA improves processability
- Compatibilizer: PVDF-g-PMMA graft copolymer (reactive extrusion with peroxide)
- Application: corrosion-resistant coatings, valve liners
        """,
        key_factors=[
            "Flory-Huggins interaction parameter chi",
            "Molecular weight and polydispersity",
            "Composition (volume fraction)",
            "Viscosity ratio (affects morphology)",
            "Compatibilizer type and concentration",
            "Processing conditions (shear, temperature, mixing time)"
        ],
        primary_authority=[
            "Paul & Bucknall - Polymer Blends (2000)",
            "Utracki - Polymer Blends Handbook (2nd ed., 2014)",
            "Flory - Principles of Polymer Chemistry (1953) - Flory-Huggins theory"
        ],
        burden_holder="Polymer engineer to select blend composition and compatibilizer",
        adversary_position="Phase separation over time, poor interfacial adhesion, property compromise",
        counter_arguments=[
            "Most polymer pairs immiscible (ΔS_mix ~ 0 for high MW)",
            "Phase separation during aging (thermodynamically unstable)",
            "Compatibilizer expensive, increases cost",
            "Processing difficult (viscosity mismatch, phase inversion)",
            "Recycling challenges (mixed polymer waste)"
        ],
        resolution_strategy="Use reactive compatibilization (in-situ copolymer formation during melt blending), optimize composition for co-continuous morphology if synergistic properties desired, characterize morphology (SEM) to confirm fine dispersion (< 1 micron preferred for toughness), use dynamic vulcanization for thermoplastic elastomers (TPE, TPV).",
        entity_scope="Polymer blends for toughness, processability, cost reduction",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established thermodynamics (Flory-Huggins), extensive commercial use (HIPS, ABS, PC/ABS).",
        controlling_precedent="Flory-Huggins theory predicts immiscibility, compatibilizers reduce interfacial tension",
        issue_category=IssueCategory.POLYMER_BLENDS
    ),

    DoctrineBlock(
        topic="Biopolymers and Biodegradable Polymers",
        keywords=["PLA", "polylactic acid", "PHB", "starch", "biodegradable", "compostable", "bio-based", "renewable feedstock"],
        conclusion_template="Biopolymers are derived from renewable biomass (PLA from corn, PHB from bacteria, starch from plants). Biodegradable polymers degrade via enzymatic or microbial action (PLA, PHB, PCL, PHA, starch). Not all bio-based polymers are biodegradable (bio-PE, bio-PET). ASTM D6400 defines compostability: > 90% degradation in 180 days.",
        reasoning_framework="""
Biopolymers address sustainability concerns: fossil fuel depletion, plastic waste accumulation, marine pollution.

DEFINITIONS:
- Bio-based: derived from renewable biomass (plants, algae, bacteria)
- Biodegradable: degraded by microorganisms (bacteria, fungi) into CO2, H2O, biomass
- Compostable: biodegradable under composting conditions (ASTM D6400, EN 13432)
- NOT SYNONYMOUS: Bio-PE (bio-based but NOT biodegradable), PLA (bio-based AND biodegradable)

POLYLACTIC ACID (PLA):
SYNTHESIS:
- Monomer: lactic acid (from fermentation of corn starch, sugarcane)
- Polymerization: ring-opening polymerization of lactide (cyclic dimer of lactic acid)
- Catalyst: Sn(Oct)2 (tin octoate)
- Stereoregularity: L-lactide (isotactic), D-lactide, meso-lactide (racemic)

PROPERTIES:
- Tg 55-60C, Tm 130-180C (depends on D-content, crystallinity)
- Brittle (elongation < 10%), impact modifier needed for toughness
- Biodegradable via hydrolysis (ester linkages) then microbial consumption
- Degrades in industrial compost (55-60C, high humidity) in 90-180 days
- Slow degradation in landfill or ocean (low temperature, low microbial activity)

APPLICATIONS:
- Packaging: cups, bottles, films (short-term use, composted after)
- Textiles: fibers for apparel, nonwovens
- Medical: sutures, drug delivery, tissue scaffolds (biocompatible, resorbable)

LIMITATIONS:
- Low heat deflection temperature (Tg 60C -> softens in hot car, hot liquids)
- Slow biodegradation in ambient conditions (needs industrial composting)
- Competition with food crops for feedstock (corn, sugarcane)

POLYHYDROXYALKANOATES (PHA, PHB):
SYNTHESIS:
- Bacterial fermentation: bacteria accumulate PHA as energy storage (up to 80% cell dry weight)
- Monomer: 3-hydroxybutyrate (PHB), 3-hydroxyvalerate (PHBV), 3-hydroxyhexanoate (PHBHx)
- Feedstock: glucose, glycerol, waste oils, CO2 (cyanobacteria)

PROPERTIES:
- PHB: Tg 5C, Tm 175C, crystalline, brittle
- PHBV: copolymer, more flexible, lower Tm (130-150C)
- Biodegradable in soil, marine, compost (100% within months)
- Biocompatible, used in medical implants

LIMITATIONS:
- Expensive (bacterial fermentation cost > chemical synthesis)
- Narrow processing window (Tm close to degradation temperature)
- Brittleness (needs plasticizers or copolymerization)

STARCH-BASED POLYMERS:
- Native starch: amylose (linear) + amylopectin (branched)
- Thermoplastic starch (TPS): starch + plasticizer (glycerol, sorbitol) -> melt-processable
- Blends: starch/PLA, starch/PCL (compatibilizers needed)
- Biodegradable: complete degradation in soil/compost (weeks to months)
- Low cost, but moisture-sensitive (swelling, property loss)

POLYCAPROLACTONE (PCL):
- Synthetic polyester: ring-opening polymerization of epsilon-caprolactone
- Tg -60C, Tm 60C (soft, flexible, rubbery at room temp)
- Biodegradable (slower than PLA, years in soil)
- Used in drug delivery, tissue engineering, compostable bags

BIO-BASED BUT NON-BIODEGRADABLE:
- Bio-PE: polyethylene from bioethanol (sugarcane) -> chemically identical to fossil PE
- Bio-PET: PET from bio-based ethylene glycol and terephthalic acid -> identical to fossil PET
- Renewable feedstock, but persist in environment (same as conventional plastics)

COMPOSTABILITY STANDARDS:
- ASTM D6400 (USA): > 90% biodegradation in 180 days (industrial compost, 58C)
- EN 13432 (Europe): disintegration, biodegradation, ecotoxicity, heavy metal limits
- Home compostable: TUV Austria OK Compost HOME (lower temp, longer time)

OILFIELD CONSIDERATIONS:
- Biodegradable drilling fluid additives: xanthan gum (biopolymer, shear thinning, biodegradable)
- Lost circulation materials: starch, cellulose (biodegradable, no environmental persistence)
- Temporary applications: frac ball seats, plugs (PLA, dissolves in water/acid at elevated temp)
        """,
        key_factors=[
            "Feedstock availability and cost (corn, sugarcane, bacteria)",
            "Biodegradation conditions (industrial compost vs landfill vs ocean)",
            "Mechanical properties (brittleness, heat resistance)",
            "Processing challenges (narrow thermal stability window)",
            "End-of-life infrastructure (composting facilities)",
            "Competition with food crops vs waste feedstocks"
        ],
        primary_authority=[
            "ASTM D6400 - Compostable Plastics",
            "Auras et al. - Poly(lactic acid) (2010)",
            "Rehm - Biopolymers (2003) - PHA review"
        ],
        burden_holder="Materials engineer to balance sustainability, cost, performance",
        adversary_position="Higher cost, limited composting infrastructure, property compromises",
        counter_arguments=[
            "PLA requires industrial composting (not home compost or landfill)",
            "PHA expensive (bacterial fermentation 3-5x cost of conventional plastics)",
            "Slow degradation in marine environment (years, not months)",
            "Microplastics still form during degradation (before complete mineralization)",
            "Life-cycle analysis (LCA) shows some bio-based polymers have higher carbon footprint (land use, fertilizer)"
        ],
        resolution_strategy="Use PLA for short-term applications with guaranteed composting infrastructure, use PHA for marine applications (faster degradation), blend with starch or plasticizers to reduce cost and improve toughness, design for end-of-life (labeling, collection, industrial composting), consider second-generation feedstocks (agricultural waste, CO2) to avoid food competition.",
        entity_scope="Sustainable polymers, packaging, medical devices, temporary downhole tools",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Established science but immature infrastructure (composting facilities) and higher cost than conventional plastics.",
        controlling_precedent="ASTM D6400 compostability, PLA/PHA biodegradation kinetics, bio-based not synonymous with biodegradable",
        issue_category=IssueCategory.BIOPOLYMERS
    ),

    DoctrineBlock(
        topic="Oilfield Polymer Applications: EOR and Drilling Fluids",
        keywords=["polyacrylamide", "HPAM", "xanthan gum", "PAC", "viscosity", "shear thinning", "thermal stability", "brine tolerance"],
        conclusion_template="Polymers in oilfield applications must withstand high temperature (80-150C), high salinity (up to 250,000 ppm TDS), and shear stress. Enhanced oil recovery (EOR): partially hydrolyzed polyacrylamide (HPAM) increases water viscosity, improves sweep efficiency. Drilling fluids: xanthan gum, PAC (polyanionic cellulose) provide viscosity and fluid loss control. PVDF, PEEK for chemical-resistant components.",
        reasoning_framework="""
Oilfield polymers operate in extreme environments: high temperature, high pressure (HTHP), high salinity, presence of H2S/CO2, mechanical shear. Material selection critical for performance and economics.

ENHANCED OIL RECOVERY (EOR) - POLYMER FLOODING:
OBJECTIVE: Increase water viscosity to match oil viscosity, improve mobility ratio, increase sweep efficiency (recover more oil from reservoir).

POLYMER: Partially Hydrolyzed Polyacrylamide (HPAM)
- Structure: [-CH2-CH(CONH2)-]n with 25-35% of amide groups hydrolyzed to carboxylate [-CH2-CH(COO-)-]
- Molecular weight: 8-20 million Da (ultra-high MW)
- Mechanism: electrostatic repulsion (COO-) expands coil, increases hydrodynamic volume, increases viscosity

VISCOSITY REQUIREMENTS:
- Target viscosity: 10-50 cP at reservoir shear rate (7.3 s^-1 in porous media, API RP 63)
- Shear thinning: high viscosity at low shear (in reservoir), low viscosity at high shear (injection, reduces pump pressure)

CHALLENGES:
1. Thermal degradation: at T > 80C, amide groups hydrolyze (accelerated), MW decreases, viscosity loss
   - Stabilizers: antioxidants, chelating agents (EDTA to sequester Fe/Cu)
   - Alternative: acrylamide/AMPS (2-acrylamido-2-methylpropanesulfonate) copolymer (sulfonate group more thermally stable)

2. Salinity: divalent cations (Ca2+, Mg2+) screen electrostatic repulsion, collapse coil, reduce viscosity
   - Mitigation: use low-salinity brine, add scale inhibitors, select AMPS copolymer (sulfonate tolerates divalent cations better)

3. Shear degradation: high shear in wellbore, pumps, perforations -> chain scission, irreversible viscosity loss
   - Mitigation: use shear-tolerant polymers (crosslinked, associative polymers), reduce injection rate, avoid choke points

4. Adsorption on rock: polymer adsorbs on clay, sandstone -> retention, reduces concentration, economics
   - Mitigation: polymer slug design (preflush with sacrificial polymer), low-retention polymers

XANTHAN GUM (alternative biopolymer for EOR):
- Bacterial polysaccharide (fermentation of Xanthomonas campestris)
- Rigid rod structure -> less shear degradation than HPAM
- Excellent salt tolerance (rigid structure not affected by divalent cations)
- Excellent thermal stability (up to 90C, longer than HPAM)
- Limitations: higher cost, biodegradation (requires biocide), higher adsorption

DRILLING FLUIDS:
FUNCTION: lubricate drill bit, remove cuttings, maintain wellbore stability, prevent fluid loss into formation.

POLYMERS:
1. Xanthan gum: viscosifier, shear thinning (low viscosity at bit, high viscosity in annulus suspends cuttings)
   - Concentration: 0.5-2 lb/bbl (1.4-5.7 kg/m3)

2. PAC (polyanionic cellulose): fluid loss control (forms filter cake on wellbore)
   - Low-viscosity PAC-LV (0.1-0.3% solution viscosity 10-20 cP)
   - Regular PAC-R (higher MW, higher viscosity)

3. HEC (hydroxyethyl cellulose): viscosifier for clear brines (completion fluids)
   - No residue, enzyme breakers for cleanup

4. Polyacrylamide (PAM): flocculant for solids removal, friction reducer for hydraulic fracturing

5. Starch: fluid loss control, biodegradable, low cost

FRACTURING FLUIDS:
FUNCTION: Create fractures in reservoir rock, transport proppant (sand, ceramic), maintain fracture conductivity.

POLYMERS:
1. Guar gum: natural polysaccharide, high MW (1-2 million Da), viscosifier
   - HPG (hydroxypropyl guar): derivatized for better hydration, thermal stability
   - CMHPG (carboxymethyl HPG): further improved salt/temp tolerance

2. Crosslinkers: borate, zirconate, titanate (form reversible crosslinks, increase viscosity 10-100x)
   - Delayed crosslinking: pumped as low-viscosity fluid, crosslinks downhole at elevated temp

3. Breakers: enzymes (hemicellulase, pectinase), oxidizers (persulfate) -> degrade polymer after proppant placement, allow flowback

CHEMICAL-RESISTANT POLYMERS (downhole components):
1. PVDF (polyvinylidene fluoride): Tg -40C, Tm 177C
   - Excellent chemical resistance (acids, bases, solvents, H2S, CO2)
   - Applications: valve seats, seals, tubing liners, coatings
   - Limitation: creep at elevated temperature, requires reinforcement (glass fiber)

2. PEEK (polyetheretherketone): Tg 143C, Tm 343C
   - Outstanding thermal stability (continuous use 250C)
   - Chemical resistance (H2S, CO2, brine, crude oil)
   - Excellent mechanical properties (high strength, low creep)
   - Applications: downhole tool housings, seals, bearings, wear rings
   - Cost: 10-20x higher than PVDF, limited to high-value applications

3. PTFE (polytetrafluoroethylene, Teflon): Tg -97C, Tm 327C
   - Extreme chemical resistance (inert to almost all chemicals)
   - Low friction coefficient (0.05-0.1)
   - Applications: seals (backup rings), coatings, valve components
   - Limitation: cold flow (creep under load), requires filler (glass, carbon) for dimensional stability

ELASTOMERS (seals, packers):
1. HNBR (hydrogenated nitrile butadiene rubber): service temp 150C
   - Excellent oil resistance, moderate H2S/CO2 resistance

2. FKM (fluoroelastomer, Viton): service temp 200C
   - Excellent chemical resistance (H2S, CO2, amines, acids)
   - High cost, limited compression set resistance at 200C

3. FFKM (perfluoroelastomer, Kalrez): service temp 250C+
   - Ultimate chemical resistance, extreme cost ($100-$500/lb)
   - Used only in critical high-temp applications (steam injection, HPHT wells)
        """,
        key_factors=[
            "Temperature (reservoir, bottomhole, surface)",
            "Salinity (TDS, divalent cations)",
            "pH (acid stimulation, CO2 content)",
            "Shear environment (pumps, perforations, porous media)",
            "Chemical compatibility (H2S, CO2, crude oil, brine)",
            "Cost and availability (high-volume vs specialty applications)"
        ],
        primary_authority=[
            "API RP 63 - Recommended Practice for EOR Polymer Flooding",
            "Lake - Enhanced Oil Recovery (1989) - polymer flooding chapter",
            "Fink - Petroleum Engineer's Guide to Oil Field Chemicals (2015)"
        ],
        burden_holder="Reservoir engineer and materials engineer to select polymer and concentration",
        adversary_position="Thermal degradation, shear degradation, adsorption, high cost",
        counter_arguments=[
            "HPAM degrades rapidly above 80C (limits application to low-temp reservoirs)",
            "Salinity reduces viscosity (especially divalent cations)",
            "Shear degradation in near-wellbore region is irreversible",
            "Polymer retention on rock (adsorption) increases cost, reduces effectiveness",
            "Biopolymers (xanthan, guar) susceptible to biodegradation (requires biocides)"
        ],
        resolution_strategy="Use AMPS copolymer for high-temp/high-salinity reservoirs (sulfonate group more stable), optimize injection rate to minimize shear, use crosslinked or associative polymers (shear-tolerant), preflush with sacrificial polymer to satisfy adsorption sites, use biocides for biopolymers, consider slickwater fracs (low polymer concentration) if formation damage concern.",
        entity_scope="EOR, drilling fluids, fracturing fluids, downhole materials",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Extensive field experience (40+ years of polymer flooding), well-understood degradation mechanisms, API standards and recommended practices.",
        controlling_precedent="HPAM viscosity vs MW/salinity/temperature, shear thinning for injectivity, PVDF/PEEK chemical resistance ratings",
        issue_category=IssueCategory.OILFIELD_POLYMERS
    ),

    DoctrineBlock(
        topic="Polymer Composites: Fiber Reinforcement",
        keywords=["composite", "carbon fiber", "glass fiber", "epoxy matrix", "fiber volume fraction", "rule of mixtures", "interfacial adhesion"],
        conclusion_template="Polymer composites combine high-strength fibers (carbon, glass, aramid) with polymer matrix (epoxy, polyester, vinyl ester) to achieve high specific strength and stiffness. Properties depend on fiber type, fiber volume fraction (Vf), fiber orientation, and interfacial adhesion. Rule of mixtures predicts modulus: Ec = Ef*Vf + Em*(1-Vf). Applications: aerospace, automotive, wind turbines, oilfield (composite pipe, sucker rods).",
        reasoning_framework="""
Polymer composites exploit the synergy between strong, stiff fibers and tough, ductile matrix. The fiber carries tensile load; the matrix transfers load between fibers and protects fibers from damage.

FIBER TYPES:
1. Glass fiber (E-glass, S-glass):
   - Tensile strength: 2-3 GPa, modulus: 70-90 GPa, elongation: 3-5%
   - Low cost ($1-3/lb), density 2.5 g/cm3
   - Applications: boats, wind turbine blades, automotive (SMC, BMC)

2. Carbon fiber (PAN-based, pitch-based):
   - Tensile strength: 3-7 GPa, modulus: 200-600 GPa, elongation: 0.5-2%
   - High cost ($10-50/lb), density 1.8 g/cm3
   - Applications: aerospace, sporting goods, automotive (high-performance)

3. Aramid fiber (Kevlar, Twaron):
   - Tensile strength: 3-4 GPa, modulus: 60-180 GPa, elongation: 2-4%
   - Excellent impact resistance, low density 1.4 g/cm3
   - Applications: ballistic protection, ropes, aerospace

MATRIX TYPES:
1. Thermoset resins:
   - Epoxy: excellent adhesion, low shrinkage, high Tg (120-180C), high cost
   - Polyester: low cost, fast cure, higher shrinkage, lower Tg (80-120C)
   - Vinyl ester: intermediate cost/properties, excellent chemical resistance

2. Thermoplastic resins:
   - PEEK, PPS, PA (nylon): higher toughness, recyclable, more difficult to process (high melt viscosity)

RULE OF MIXTURES (aligned continuous fibers, longitudinal direction):
- Composite modulus: Ec = Ef*Vf + Em*(1-Vf)
- Composite strength: sigma_c = sigma_f*Vf + sigma_m*(1-Vf) (approximate, assumes strain compatibility)
- Typical Vf: 50-70% (higher Vf -> higher strength but more difficult to wet fibers)

EXAMPLE CALCULATION:
Carbon fiber/epoxy composite, Vf = 60%
- Ef = 230 GPa, Em = 3 GPa
- Ec = 230*0.6 + 3*0.4 = 138 + 1.2 = 139 GPa (vs pure epoxy 3 GPa, 46x increase!)

FIBER ORIENTATION:
- Unidirectional (UD): all fibers aligned, maximum strength in fiber direction, weak transverse
- Woven fabric (plain, twill, satin): balanced properties, easier handling
- Random mat (chopped strand mat, CSM): isotropic in-plane, lower strength, low cost
- Angle ply laminate: [0/45/90/-45] stacking sequence, tailored properties

INTERFACIAL ADHESION:
- Critical for load transfer from matrix to fiber
- Fiber surface treatment: sizing (epoxy-compatible for CF, silane for GF)
- Poor adhesion -> debonding, reduced strength, premature failure
- Test: single-fiber pullout, interfacial shear strength (IFSS)

MANUFACTURING PROCESSES:
1. Hand layup: manual placement of fabric + resin, low cost, low volume, variable quality
2. Vacuum bagging: fabric + resin under vacuum, removes air, improves consolidation
3. Resin transfer molding (RTM): dry fabric in mold, inject resin under pressure, medium volume
4. Autoclave: high pressure (6 bar) + high temp (120-180C), aerospace quality, high cost
5. Pultrusion: continuous process, constant cross-section (I-beam, rod), high volume
6. Filament winding: wind fiber tows on mandrel, pressure vessels, pipes, high Vf

OILFIELD APPLICATIONS:
1. Composite sucker rods:
   - Fiberglass or carbon fiber/epoxy, pultruded
   - Advantages: corrosion resistance, weight reduction (70% lighter than steel), fatigue resistance
   - Limitations: lower modulus than steel (pump efficiency), higher cost, connector design

2. Composite pipe (fiberglass-reinforced plastic, FRP):
   - Glass fiber/epoxy or vinyl ester, filament-wound or centrifugally cast
   - Applications: water injection lines, produced water, corrosive fluids (H2S, CO2)
   - Advantages: corrosion resistance, smooth ID (less fouling), lighter weight
   - Limitations: lower pressure rating than steel, UV degradation (coating needed), joint integrity

3. Composite coiled tubing:
   - Carbon fiber/epoxy, higher strength-to-weight, allows longer reaches
   - Development stage (not yet commercial for oilfield)

FAILURE MODES:
- Fiber breakage: tensile overload
- Matrix cracking: thermal cycling, impact
- Delamination: interlaminar shear, impact damage
- Fiber-matrix debonding: poor interfacial adhesion, chemical attack
- Buckling (compression): kinking of fibers, lower compressive strength than tensile
        """,
        key_factors=[
            "Fiber type and properties (strength, modulus, cost)",
            "Fiber volume fraction (Vf = 50-70% typical)",
            "Fiber orientation (UD, woven, angle ply)",
            "Interfacial adhesion (sizing, surface treatment)",
            "Matrix type (thermoset vs thermoplastic)",
            "Manufacturing process (hand layup, RTM, autoclave, pultrusion)"
        ],
        primary_authority=[
            "Daniel & Ishai - Engineering Mechanics of Composite Materials (2nd ed., 2005)",
            "Chawla - Composite Materials: Science and Engineering (3rd ed., 2012)",
            "ASTM D3039 - Tensile Properties of Polymer Matrix Composites"
        ],
        burden_holder="Composite engineer to design laminate and select manufacturing process",
        adversary_position="High material cost, complex manufacturing, difficult to inspect (internal damage)",
        counter_arguments=[
            "Carbon fiber expensive ($20-50/lb vs steel $0.50/lb)",
            "Anisotropic properties (weak in transverse direction, delamination)",
            "Difficult to inspect (ultrasonic C-scan, X-ray CT needed for internal damage)",
            "Thermosetting matrix not recyclable (contrast to steel)",
            "Lower compressive strength than tensile (fiber buckling)"
        ],
        resolution_strategy="Use glass fiber for cost-sensitive applications (boats, wind turbines), carbon fiber for weight-critical applications (aerospace, automotive), optimize fiber orientation for load path (FEA), improve interfacial adhesion with fiber sizing and matrix coupling agents, use toughened matrices (rubber-modified epoxy) for impact resistance, inspect with NDT (ultrasonic, thermography, shearography).",
        entity_scope="High-performance structures, corrosion-resistant applications, weight-sensitive applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Mature technology (50+ years in aerospace), well-understood micromechanics (rule of mixtures, laminate theory).",
        controlling_precedent="Rule of mixtures for modulus, fiber volume fraction 50-70%, interfacial adhesion critical for load transfer",
        issue_category=IssueCategory.POLYMER_COMPOSITES
    ),

    # Additional doctrine blocks would go here (targeting 25+ total)
    # Covering topics like: copolymerization, crosslinking, polymer crystallization kinetics,
    # additive systems (plasticizers, fillers, flame retardants), polymer recycling,
    # electrospinning, 3D printing of polymers, conductive polymers, etc.

]


# ============================================================================
# INTELLIGENT ENGINE
# ============================================================================

class PolymerChemistryEngine:
    """TIE-Grade Polymer Chemistry Intelligence Engine"""

    def __init__(self):
        self.start_time = time.time()
        self.query_count = 0
        self.cache_hits = 0
        self.metrics_log: List[QueryMetrics] = []

        # Semantic normalization dictionary
        self.semantic_map = {
            "PMMA": ["polymethyl methacrylate", "acrylic", "plexiglass", "lucite"],
            "PE": ["polyethylene", "LDPE", "HDPE", "LLDPE"],
            "PP": ["polypropylene"],
            "PS": ["polystyrene", "styrofoam"],
            "PVC": ["polyvinyl chloride", "vinyl"],
            "PET": ["polyethylene terephthalate", "polyester", "PETE"],
            "PA": ["polyamide", "nylon"],
            "PC": ["polycarbonate"],
            "PTFE": ["polytetrafluoroethylene", "teflon"],
            "PVDF": ["polyvinylidene fluoride", "kynar"],
            "PEEK": ["polyetheretherketone"],
            "Tg": ["glass transition", "glass transition temperature"],
            "Tm": ["melting point", "melting temperature"],
            "PDI": ["polydispersity", "polydispersity index", "molecular weight distribution"],
            "GPC": ["gel permeation chromatography", "size exclusion chromatography", "SEC"],
            "DSC": ["differential scanning calorimetry"],
            "HPAM": ["partially hydrolyzed polyacrylamide", "polyacrylamide"],
            "EOR": ["enhanced oil recovery", "polymer flooding"],
            "ATRP": ["atom transfer radical polymerization"],
            "RAFT": ["reversible addition fragmentation transfer"],
            "NMP": ["nitroxide mediated polymerization"],
        }

        logger.info(f"CHEM09 Polymer Chemistry Engine initialized with {len(DOCTRINE_CACHE)} doctrine blocks")

    def normalize_query(self, query: str) -> str:
        """Normalize query terms for semantic matching"""
        normalized = query.lower()
        for canonical, variants in self.semantic_map.items():
            for variant in variants:
                if variant in normalized:
                    normalized = normalized.replace(variant, canonical.lower())
        return normalized

    def search_doctrines(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache for relevant blocks"""
        normalized_query = self.normalize_query(query)
        query_terms = set(normalized_query.split())

        matches = []
        for doctrine in DOCTRINE_CACHE:
            # Check keywords
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in normalized_query)

            # Check topic
            topic_match = 1 if any(term in doctrine.topic.lower() for term in query_terms) else 0

            # Check category
            category_match = 1 if doctrine.issue_category.value.lower().replace("_", " ") in normalized_query else 0

            score = keyword_matches * 3 + topic_match * 2 + category_match * 2

            if score > 0:
                matches.append((score, doctrine))

        # Sort by score descending
        matches.sort(key=lambda x: x[0], reverse=True)
        return [doctrine for score, doctrine in matches[:5]]  # Top 5 matches

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> tuple[str, List[str], ConfidenceLevel, Optional[str]]:
        """
        Three-layer response architecture:
        Layer 1: Doctrine cache (0-200ms)
        Layer 2: Semantic retrieval (200-1000ms)
        Layer 3: Deep analysis (1000ms+)
        """

        # LAYER 1: Doctrine Cache
        matched_doctrines = self.search_doctrines(query)

        if matched_doctrines:
            # Cache hit - fast response
            self.cache_hits += 1
            primary = matched_doctrines[0]

            if mode == ResponseMode.FAST:
                answer = primary.conclusion_template
                reasoning = None
            elif mode == ResponseMode.DEFENSE:
                answer = f"{primary.conclusion_template}\n\nAUTHORITY: {'; '.join(primary.primary_authority)}\n\nKEY FACTORS: {'; '.join(primary.key_factors)}"
                reasoning = primary.reasoning_framework[:500] + "..." if len(primary.reasoning_framework) > 500 else primary.reasoning_framework
            else:  # MEMO
                answer = f"TOPIC: {primary.topic}\n\n{primary.conclusion_template}\n\nDETAILED REASONING:\n{primary.reasoning_framework}\n\nAUTHORITY:\n{chr(10).join('- ' + auth for auth in primary.primary_authority)}\n\nCOUNTER-ARGUMENTS:\n{chr(10).join('- ' + arg for arg in primary.counter_arguments)}\n\nRESOLUTION STRATEGY:\n{primary.resolution_strategy}"
                reasoning = primary.reasoning_framework

            doctrine_names = [d.topic for d in matched_doctrines]
            confidence = primary.confidence

            # Epistemic disclosure for high-risk positions
            disclosure = None
            if confidence in [ConfidenceLevel.AGGRESSIVE, ConfidenceLevel.HIGH_RISK]:
                disclosure = f"DISCLOSURE: This analysis is {confidence.value}. {primary.confidence_stratification}"

            return answer, doctrine_names, confidence, reasoning if mode != ResponseMode.FAST else None

        # LAYER 2: No exact match - provide general guidance
        answer = f"CHEM09 Polymer Chemistry Analysis - {zone.value} context.\n\nQuery: {query}\n\nNo exact doctrine match found. General polymer chemistry principles apply. This engine specializes in: polymerization mechanisms (free radical, step-growth, controlled/living), molecular weight characterization (GPC/SEC, Mn, Mw, PDI), thermal analysis (DSC - Tg, Tm, crystallinity), rheology (shear thinning, viscoelasticity), polymer processing (injection molding, extrusion), degradation (thermal, UV, oxidative, hydrolytic), polymer blends and compatibilization, biopolymers (PLA, PHA, starch), oilfield polymers (HPAM for EOR, xanthan gum, PVDF/PEEK), and polymer composites (fiber-reinforced).\n\nFor specific guidance, please refine query to include: polymer type, property of interest, processing method, or application context."

        return answer, [], ConfidenceLevel.DISCLOSURE, None

    async def process_query(
        self,
        request: QueryRequest
    ) -> QueryResponse:
        """Main query processing with full telemetry"""
        start = time.time()
        query_id = hashlib.sha256(f"{request.query}{time.time()}".encode()).hexdigest()[:16]

        self.query_count += 1

        # Execute three-layer response
        answer, doctrines, confidence, reasoning = self.three_layer_response(
            request.query,
            request.mode,
            request.zone
        )

        response_time_ms = (time.time() - start) * 1000

        # Determinism hash
        determinism_hash = hashlib.sha256(
            f"{request.query}{answer}{doctrines}".encode()
        ).hexdigest()[:16]

        # Log metrics
        metrics = QueryMetrics(
            query_id=query_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            mode=request.mode,
            cache_hit=len(doctrines) > 0,
            doctrines_triggered=doctrines,
            response_time_ms=response_time_ms,
            confidence=confidence,
            zone=request.zone,
            determinism_hash=determinism_hash
        )
        self.metrics_log.append(metrics)

        # Audit trail
        logger.info(f"Query {query_id} | Mode: {request.mode.value} | Doctrines: {len(doctrines)} | Time: {response_time_ms:.1f}ms | Confidence: {confidence.value}")

        # Build response
        response = QueryResponse(
            answer=answer,
            confidence=confidence,
            doctrines_applied=doctrines,
            response_time_ms=response_time_ms,
            determinism_hash=determinism_hash
        )

        if request.include_reasoning and reasoning:
            response.reasoning = reasoning

        return response

    def get_health(self) -> HealthResponse:
        """Health endpoint with comprehensive metrics"""
        uptime = time.time() - self.start_time
        cache_hit_rate = (self.cache_hits / self.query_count * 100) if self.query_count > 0 else 0.0

        return HealthResponse(
            status="healthy",
            engine="CHEM09_polymer_chemistry",
            version="1.0.0",
            port=9291,
            doctrines_loaded=len(DOCTRINE_CACHE),
            uptime_seconds=uptime,
            total_queries=self.query_count,
            cache_hit_rate=cache_hit_rate
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="CHEM09 Polymer Chemistry Intelligence Engine",
    description="TIE-Grade knowledge system for polymer science",
    version="1.0.0"
)

# CORS middleware
APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = PolymerChemistryEngine()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint"""
    try:
        return await engine.process_query(request)
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint"""
    return engine.get_health()


@APP.get("/doctrines")
async def doctrines_endpoint():
    """List all available doctrines"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }


@APP.get("/metrics")
async def metrics_endpoint():
    """Query metrics and telemetry"""
    if not engine.metrics_log:
        return {"message": "No queries processed yet"}

    recent_metrics = engine.metrics_log[-100:]  # Last 100 queries

    avg_response_time = sum(m.response_time_ms for m in recent_metrics) / len(recent_metrics)
    cache_hit_rate = sum(1 for m in recent_metrics if m.cache_hit) / len(recent_metrics) * 100

    confidence_distribution = {}
    for m in recent_metrics:
        confidence_distribution[m.confidence.value] = confidence_distribution.get(m.confidence.value, 0) + 1

    return {
        "total_queries": engine.query_count,
        "cache_hits": engine.cache_hits,
        "cache_hit_rate_percent": cache_hit_rate,
        "avg_response_time_ms": avg_response_time,
        "confidence_distribution": confidence_distribution,
        "recent_queries": len(recent_metrics)
    }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting CHEM09 Polymer Chemistry Intelligence Engine on port 9291")
    uvicorn.run(
        APP,
        host="0.0.0.0",
        port=9291,
        log_level="info"
    )
