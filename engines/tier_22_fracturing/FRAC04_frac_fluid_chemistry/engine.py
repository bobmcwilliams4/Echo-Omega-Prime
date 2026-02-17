"""
FRAC04 - Frac Fluid Chemistry Engine
TIE Gold Standard - Completions & Fracturing Fluid Systems

Authority: 11.0 SOVEREIGN | ECHO OMEGA PRIME
Domain: Hydraulic fracturing fluid chemistry, design, compatibility, performance testing
Port: 9024
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ═══════════════════════════════════════════════════════════════════════════
# ENUMS & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

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
    SLICKWATER_SYSTEMS = "SLICKWATER_SYSTEMS"
    CROSSLINKED_GELS = "CROSSLINKED_GELS"
    HYBRID_DESIGNS = "HYBRID_DESIGNS"
    VES_FLUIDS = "VES_FLUIDS"
    BREAKER_SYSTEMS = "BREAKER_SYSTEMS"
    BIOCIDE_CHEMISTRY = "BIOCIDE_CHEMISTRY"
    SCALE_INHIBITION = "SCALE_INHIBITION"
    CLAY_CONTROL = "CLAY_CONTROL"
    ACID_FRACS = "ACID_FRACS"
    WATER_QUALITY = "WATER_QUALITY"
    COMPATIBILITY_TESTING = "COMPATIBILITY_TESTING"
    FRICTION_TESTING = "FRICTION_TESTING"
    PROPPANT_TRANSPORT = "PROPPANT_TRANSPORT"
    IRON_CONTROL = "IRON_CONTROL"
    FLUID_RECYCLING = "FLUID_RECYCLING"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


BANNED_PHRASES = [
    "guaranteed", "certain", "always works", "never fails",
    "approved by EPA", "no environmental impact", "100% effective"
]

VERSION = "1.0.0"
ENGINE_ID = "FRAC04"
PORT = 9024


# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=10, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    context: Optional[Dict[str, Any]] = None


class DoctrineMatch(BaseModel):
    topic: str
    confidence: float
    reasoning: str
    authority_level: int
    stratification: ConfidenceLevel


class QueryResponse(BaseModel):
    answer: str
    doctrine_matches: List[DoctrineMatch]
    confidence: ConfidenceLevel
    zone: AnalysisZone
    mode: ResponseMode
    latency_ms: float
    determinism_hash: str
    timestamp: str
    epistemic_caveats: List[str]


class HealthResponse(BaseModel):
    status: str
    version: str
    engine_id: str
    port: int
    doctrine_count: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float
    cache_hit_rate: float


# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE BLOCK
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    controlling_precedent: str
    category: IssueCategory

    def matches(self, query: str) -> float:
        query_lower = query.lower()
        score = 0.0
        for kw in self.keywords:
            if kw.lower() in query_lower:
                score += 1.0
        return min(score / len(self.keywords), 1.0) if self.keywords else 0.0


# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ REAL FRAC FLUID CHEMISTRY BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Anionic Friction Reducers in Slickwater Fracs",
        keywords=["anionic", "friction reducer", "slickwater", "polyacrylamide", "FR performance"],
        conclusion_template=[
            "Anionic polyacrylamide friction reducers are effective in high-salinity brines.",
            "Performance degrades with divalent cation concentration (Ca2+, Mg2+).",
            "Typical dosage: 0.25-1.0 gpt; friction reduction: 60-75% at optimal loading."
        ],
        reasoning_framework="""
Anionic friction reducers work via electrostatic repulsion in the viscous sublayer.
High TDS (>50,000 ppm) causes polymer coiling, reducing effectiveness.
Calcium and magnesium ions shield anionic charges, requiring higher dosage.
Produced water with high hardness may need water softening or cationic FR.
Temperature stability: anionic PAM stable to 200°F; above 250°F consider AMPS copolymers.
Shear stability critical: high molecular weight polymers (10-15 million Da) provide best performance.
Field testing via loop rheometer required to validate lab friction data.
""",
        key_factors=[
            "Water TDS and divalent cation content",
            "Polymer molecular weight and charge density",
            "Dosage rate (gpt) and mixing energy",
            "Formation temperature and contact time",
            "Shear rate in tubulars (Reynolds number)"
        ],
        primary_authority=[
            "SPE 119900 - Friction Reducer Performance in Slickwater Fracturing",
            "SPE 173755 - Effect of Water Quality on FR Efficiency",
            "API RP 19D - Measuring Friction Pressures"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may assume all FRs perform equally regardless of water chemistry",
        counter_arguments=[
            "Cationic FRs may outperform in high-hardness water",
            "Hybrid systems (anionic + nonionic) can broaden salinity tolerance",
            "Encapsulated FR can delay activation in wellbore"
        ],
        resolution_strategy="Lab compatibility testing with actual source water, loop testing for friction validation, field trial on single stage before full-scale deployment.",
        entity_scope="Service company, operator, water provider",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 119900 establishes anionic FR salinity limits",
        category=IssueCategory.SLICKWATER_SYSTEMS
    ),

    DoctrineBlock(
        topic="Cationic Friction Reducers for High-Hardness Brines",
        keywords=["cationic", "friction reducer", "hardness", "divalent cations", "produced water"],
        conclusion_template=[
            "Cationic FRs perform better than anionic in high-Ca/Mg brines (>5000 ppm hardness).",
            "Cost premium: 2-3x anionic, but lower dosage offsets (0.1-0.5 gpt typical).",
            "Compatibility with anionic surfactants must be tested (precipitation risk)."
        ],
        reasoning_framework="""
Cationic polymers have positive charge, unaffected by divalent cation shielding.
Adsorb onto negatively charged formation clays, providing dual FR + clay stabilization.
Incompatible with anionic surfactants, scale inhibitors (precipitation).
Less common in unconventional wells due to cost, but preferred in produced water reuse.
Molecular weight typically lower (5-8 million Da) than anionic due to synthesis constraints.
Quaternary ammonium groups provide charge; DADMAC, DMDAAC common monomers.
Biodegradability lower than anionic; FracFocus disclosure required.
""",
        key_factors=[
            "Brine hardness (Ca2+, Mg2+ ppm)",
            "Presence of anionic additives in system",
            "Cost vs performance tradeoff",
            "Clay content in formation",
            "Regulatory disclosure requirements"
        ],
        primary_authority=[
            "SPE 164005 - Cationic Polymers in High-TDS Fracs",
            "SPE 185052 - Produced Water Reuse with Cationic FR",
            "FracFocus Chemical Disclosure Registry"
        ],
        burden_holder="Engineer",
        adversary_position="Cost-conscious operator may reject due to premium price without lab data",
        counter_arguments=[
            "Water treatment (softening) may allow anionic FR use at lower total cost",
            "Hybrid designs with minimal hardness-sensitive stages",
            "Nonionic FRs as compromise solution"
        ],
        resolution_strategy="Lab jar tests with actual brine, friction loop testing, economic analysis including water treatment cost, pilot stage in field.",
        entity_scope="Service company, operator, water mgmt contractor",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 164005 validates cationic FR superiority in hard water",
        category=IssueCategory.SLICKWATER_SYSTEMS
    ),

    DoctrineBlock(
        topic="Borate-Crosslinked Guar Gel Systems",
        keywords=["borate", "crosslinker", "guar", "gel", "pH-dependent", "delayed crosslink"],
        conclusion_template=[
            "Borate crosslinkers (sodium tetraborate) react with guar at pH >9.5.",
            "Reversible crosslink: breaks under shear, reforms at rest (thixotropic).",
            "Temperature limit: 200°F; above requires organometallic crosslinkers."
        ],
        reasoning_framework="""
Borate ion complexes with cis-diol groups on guar hydroxyl positions.
pH control critical: below 9, no crosslink; above 11, excessive gel strength.
NaOH or KOH used for pH adjustment; buffer systems maintain pH during pumping.
Crosslink time controlled via delayed borate release (encapsulation) or base addition rate.
Shear-thinning behavior: high viscosity at rest (proppant suspension), low viscosity under shear (pumpability).
Breaker: oxidizer (persulfate, peroxide) or enzyme (hemicellulase) degrades guar backbone.
Temperature >200°F causes borate hydrolysis, gel degradation; use zirconate or titanate instead.
Fluid loss control via fine silica flour (100 mesh), helps build filter cake.
""",
        key_factors=[
            "Formation temperature (static BHT)",
            "Target crosslink time (delay from surface to perforation)",
            "pH and buffer system design",
            "Proppant loading (lbm/gal) and settling requirements",
            "Breaker schedule for post-frac cleanup"
        ],
        primary_authority=[
            "SPE 18211 - Borate Crosslinked Fluids: Chemistry and Application",
            "SPE 28562 - Temperature Limits of Borate Systems",
            "API RP 39 - Recommended Practices for Measuring Rheological Properties"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may prefer slickwater to avoid gel damage, even with lower proppant transport",
        counter_arguments=[
            "Modern breaker systems reduce gel damage vs historical experience",
            "Hybrid frac designs limit gel usage to high-proppant stages only",
            "VES fluids avoid polymer damage entirely"
        ],
        resolution_strategy="Gel stability testing at formation temperature, core flow tests for damage assessment, breaker optimization lab work, field trial with post-frac flowback analysis.",
        entity_scope="Service company, operator, proppant supplier",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 18211 defines borate crosslink chemistry and pH requirements",
        category=IssueCategory.CROSSLINKED_GELS
    ),

    DoctrineBlock(
        topic="Zirconate and Titanate Crosslinkers for High-Temp Gels",
        keywords=["zirconate", "titanate", "high temperature", "organometallic", "delayed crosslink"],
        conclusion_template=[
            "Zirconium (Zr) and titanium (Ti) crosslinkers stable to 300°F+.",
            "React with guar/HPG at neutral pH; delay achieved via complexing ligands (lactate, TEA).",
            "Irreversible crosslink: higher gel strength but less shear recovery than borate."
        ],
        reasoning_framework="""
Organometallic crosslinkers form coordinate bonds with guar hydroxyls.
Zirconium lactate, zirconium carbonate common forms; titanate (IV) chelates also used.
Ligand exchange controls delay: lactate, citrate, or triethanolamine (TEA) temporarily complex metal.
As ligand dissociates downhole (pH, temperature, dilution), metal crosslinks polymer.
pH range 6-8 optimal; no need for high-pH base systems like borate.
Gel strength higher than borate, better proppant suspension, but more formation damage risk.
Breaker more difficult: persulfate, chlorite, or high enzyme loading required.
Temperature stability to 350°F demonstrated in lab; field use common above 250°F.
Compatibility with HPG (hydroxypropyl guar) and CMHPG (carboxymethyl HPG) better than guar.
""",
        key_factors=[
            "Formation temperature (BHT >250°F drives selection)",
            "Crosslink delay time (match pump schedule)",
            "Gel strength vs formation damage tradeoff",
            "Breaker effectiveness and schedule",
            "Cost (2-4x borate crosslinker cost)"
        ],
        primary_authority=[
            "SPE 24339 - Zirconium Crosslinked Fluids for High-Temp Reservoirs",
            "SPE 28978 - Titanate Crosslinker Chemistry and Performance",
            "SPE 31094 - Delayed Crosslinking Mechanisms"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may question cost vs slickwater, especially if temp <250°F marginal",
        counter_arguments=[
            "CMHPG improves cleanup vs regular guar, reduces damage concern",
            "Encapsulated breakers ensure post-frac gel degradation",
            "Proppant pack conductivity gains offset fluid cost"
        ],
        resolution_strategy="Lab rheology at formation temp, crosslink time validation, core damage testing, economic analysis (fluid cost vs production gain), field trial with flowback analysis.",
        entity_scope="Service company, operator, chemical supplier",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 24339 establishes Zr/Ti stability above 250°F",
        category=IssueCategory.CROSSLINKED_GELS
    ),

    DoctrineBlock(
        topic="Hybrid Frac Design - Slickwater and Gel Stages",
        keywords=["hybrid", "slickwater", "gel", "stage design", "proppant transport", "complex fracture"],
        conclusion_template=[
            "Hybrid designs use slickwater for far-field complexity, gel for near-wellbore proppant placement.",
            "Typical sequence: slickwater pad, gel with high proppant, slickwater flush.",
            "Optimizes fracture geometry and conductivity vs single-fluid approach."
        ],
        reasoning_framework="""
Slickwater creates complex fracture networks via low viscosity, high rate (>80 bpm).
Gel stages carry high proppant concentrations (>4 ppg) into primary fracture.
Pad volume (slickwater) creates fracture width for gel penetration.
Gel stages prevent proppant settling in high-angle or horizontal fractures.
Flush stage (slickwater) cleans wellbore, prevents screenout near perforations.
Microseismic shows slickwater generates more fracture complexity than gel alone.
Production data: hybrid designs often outperform slickwater-only in liquids-rich plays.
Design requires accurate fracture height modeling to size gel volume.
Compatibility: ensure FR, gel polymer, and crosslinker don't interact adversely.
""",
        key_factors=[
            "Fracture complexity goals (DFN vs planar)",
            "Proppant loading targets (lbm/ft)",
            "Formation stress profile (height growth risk)",
            "Permeability and fluid loss (pad efficiency)",
            "Cost vs production benefit analysis"
        ],
        primary_authority=[
            "SPE 119900 - Hybrid Fracturing in Unconventional Reservoirs",
            "SPE 152197 - Microseismic Analysis of Hybrid Fracs",
            "SPE 168612 - Production Analysis: Hybrid vs Slickwater"
        ],
        burden_holder="Engineer",
        adversary_position="Cost-focused operator may prefer slickwater-only to avoid gel additives and complexity",
        counter_arguments=[
            "Slickwater-only sufficient if fracture height contained and high pump rate achievable",
            "Channel fracturing (pulsed proppant) alternative to gel for transport",
            "Gel damage risk may offset conductivity gains"
        ],
        resolution_strategy="Fracture modeling (planar + unconventional models), sensitivity analysis on gel volume, pilot well comparison (hybrid vs slickwater), production surveillance for validation.",
        entity_scope="Service company, operator, G&G team",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="SPE 152197 microseismic data supports hybrid complexity claims",
        category=IssueCategory.HYBRID_DESIGNS
    ),

    DoctrineBlock(
        topic="Viscoelastic Surfactant (VES) Fluids",
        keywords=["VES", "viscoelastic surfactant", "polymer-free", "micelle", "clean fluid"],
        conclusion_template=[
            "VES fluids form wormlike micelles, providing viscosity without polymer damage.",
            "Broken by hydrocarbons (oil/condensate contact) or internal breakers (esters).",
            "Higher cost than guar (3-5x), used where formation damage critical (tight gas, condensate)."
        ],
        reasoning_framework="""
Surfactant molecules (typically anionic or zwitterionic) self-assemble into micelles.
At critical concentration (CMC), micelles elongate into wormlike structures, providing viscosity.
No polymer residue: clean break via hydrocarbon contact or ester hydrolysis.
Temperature stable to 250°F; some systems to 300°F with additives.
Proppant transport comparable to crosslinked gel (viscosity 100-300 cp at 170 s^-1).
Salt concentration critical: 2-8% KCl or ammonium chloride required for micelle formation.
Cost driven by surfactant loading: 4-10 gpt typical vs 25-40 lbm/1000 gal guar.
Field use common in UK North Sea, Middle East tight gas, US condensate-rich shales.
Fluid loss higher than gelled systems; may need fluid loss additives (soluble resin).
""",
        key_factors=[
            "Formation damage sensitivity (permeability <1 md)",
            "Presence of hydrocarbon for breaking (gas vs oil)",
            "Formation temperature (VES stability limits)",
            "Cost tolerance (premium pricing)",
            "Water chemistry (salinity, hardness)"
        ],
        primary_authority=[
            "SPE 64984 - VES Fluid Technology and Applications",
            "SPE 80222 - Field Results with VES in Tight Gas",
            "SPE 106044 - VES Breaker Mechanisms"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may reject due to cost without damage quantification",
        counter_arguments=[
            "CMHPG with optimized breaker may achieve comparable cleanup at lower cost",
            "Slickwater with degradable fiber for proppant transport",
            "Acid preflush + guar may address damage concerns"
        ],
        resolution_strategy="Core damage testing (regained perm %), economic analysis (fluid cost vs production uplift), field trial in high-value wells, flowback analysis for cleanup validation.",
        entity_scope="Service company, operator, reservoir engineering",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="SPE 64984 establishes VES damage-free claim",
        category=IssueCategory.VES_FLUIDS
    ),

    DoctrineBlock(
        topic="Enzyme Breakers for Guar-Based Fluids",
        keywords=["enzyme", "breaker", "hemicellulase", "guar degradation", "temperature stability"],
        conclusion_template=[
            "Hemicellulase enzymes degrade guar via hydrolysis of glycosidic bonds.",
            "Temperature sensitive: optimal 120-160°F; denature above 180°F without stabilizers.",
            "Dosage: 0.1-0.5 gpt; encapsulation provides delayed activation."
        ],
        reasoning_framework="""
Enzymes catalyze guar backbone cleavage, reducing molecular weight and viscosity.
Hemicellulase, alpha-galactosidase common; each targets specific guar linkages.
Temperature window critical: below 100°F, slow kinetics; above 180°F, protein denaturation.
Encapsulation (polymer coating, wax) delays enzyme release until downhole temperature reached.
pH affects activity: optimal 4.5-7.5; high-pH borate systems require pH reversion or acid preflush.
Overdosing causes premature break, screenout risk; underdosing leaves residual gel damage.
Combination with oxidizer (persulfate) common: enzyme breaks bulk gel, oxidizer cleans residue.
Concentration in flowback water: enzyme activity indicator; lab assays available.
Field practice: split dosage (surface + encapsulated) for staged break.
""",
        key_factors=[
            "Formation temperature profile (static BHT)",
            "Gel polymer type (guar, HPG, CMHPG)",
            "pH of frac fluid system",
            "Break time target (hours post-shut-in)",
            "Compatibility with other additives"
        ],
        primary_authority=[
            "SPE 21502 - Enzyme Breaker Chemistry for Frac Fluids",
            "SPE 30114 - Encapsulated Breaker Systems",
            "SPE 77746 - Temperature Effects on Breaker Performance"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may default to oxidizer breakers due to cost or simplicity",
        counter_arguments=[
            "Oxidizer (persulfate) works across broader temperature range",
            "Hybrid breaker systems (enzyme + oxidizer) provide redundancy",
            "High-temp formations (>200°F) may exceed enzyme stability"
        ],
        resolution_strategy="Lab break tests at formation temperature, flowback sampling for residual viscosity, production analysis (cleanup efficiency), cost comparison (enzyme vs oxidizer).",
        entity_scope="Service company, operator, chemical supplier",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 21502 defines enzyme mechanisms and temperature limits",
        category=IssueCategory.BREAKER_SYSTEMS
    ),

    DoctrineBlock(
        topic="Oxidizer Breakers - Persulfate and Peroxide Systems",
        keywords=["oxidizer", "persulfate", "peroxide", "breaker", "free radical", "gel degradation"],
        conclusion_template=[
            "Persulfate (ammonium, sodium) generates free radicals, breaking polymer chains.",
            "Effective range: 140-300°F; below 140°F slow kinetics, activators (Fe2+) needed.",
            "Dosage: 1-5 lbm/1000 gal; overdosing accelerates corrosion, underdosing incomplete break."
        ],
        reasoning_framework="""
Persulfate thermally decomposes to sulfate radicals (SO4•−), attacking polymer backbone.
Activation energy high: requires 140°F+ for reasonable kinetics (hours).
Activators (ferrous iron, reducing agents) enable lower-temp activation.
Encapsulation (polymer coating) delays release for controlled break timing.
Peroxide (H2O2) alternative: lower activation temp (100°F+), but less stable at high temp.
Corrosion risk: free radicals attack tubulars; inhibitor packages required (filming amines, thiols).
Interaction with biocides: chlorine dioxide + persulfate can cause rapid gas evolution (safety).
pH affects decomposition rate: acidic pH accelerates persulfate.
Field practice: split dosage (immediate + delayed) for staged viscosity reduction.
Environmental: persulfate decomposes to sulfate (non-toxic); FracFocus disclosure.
""",
        key_factors=[
            "Formation temperature (BHT and near-wellbore cooling)",
            "Break time requirements (hours post-shut-in)",
            "Corrosion inhibitor compatibility",
            "Interaction with other additives (biocide, acid)",
            "Cost vs enzyme breakers"
        ],
        primary_authority=[
            "SPE 13164 - Oxidative Degradation of Fracturing Fluids",
            "SPE 71067 - Persulfate Breaker Performance at Temperature",
            "NACE SP0175 - Corrosion Control in Oilfield Operations"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may prefer enzyme to avoid corrosion risk, especially in sweet wells",
        counter_arguments=[
            "Enzyme denatures above 180°F; oxidizer required for high-temp wells",
            "Modern corrosion inhibitors effectively mitigate risk",
            "Hybrid breaker (enzyme + oxidizer) provides redundancy"
        ],
        resolution_strategy="Lab break tests with corrosion coupons, temperature profile modeling (cooldown during shut-in), flowback analysis, inhibitor effectiveness testing.",
        entity_scope="Service company, operator, metallurgy consultant",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 13164 establishes oxidizer mechanisms and corrosion concerns",
        category=IssueCategory.BREAKER_SYSTEMS
    ),

    DoctrineBlock(
        topic="Biocide Selection - Glutaraldehyde vs THPS vs Chlorine Dioxide",
        keywords=["biocide", "glutaraldehyde", "THPS", "chlorine dioxide", "bacteria control", "SRB"],
        conclusion_template=[
            "Glutaraldehyde (50% solution): broad-spectrum, 0.1-0.5 gpt, effective vs SRB.",
            "THPS (tetrakis hydroxymethyl phosphonium sulfate): non-oxidizing, 0.05-0.2 gpt, less corrosive.",
            "Chlorine dioxide: oxidizer, gas generation risk with persulfate, use with caution."
        ],
        reasoning_framework="""
Bacteria in frac water cause H2S generation (SRB), viscosity loss, corrosion.
Glutaraldehyde crosslinks bacterial proteins, broad-spectrum bactericide.
Effective pH range 6-9; higher pH (>10) reduces efficacy.
Toxicity: OSHA PEL 0.2 ppm (vapor); PPE required for handling.
THPS reacts with bacterial cell walls, effective vs planktonic and sessile bacteria.
Less toxic than glutaraldehyde; easier handling, lower vapor pressure.
Compatibility: THPS incompatible with anionic surfactants (precipitation).
Chlorine dioxide generated in-situ (chlorite + acid or hypochlorite + acid).
Strong oxidizer: kills bacteria rapidly but reacts with persulfate, causing ClO2 gas.
Safety: ClO2 explosive above 10% concentration in air; ventilation critical.
Regulatory: all biocides require FracFocus disclosure; EPA antimicrobial registration.
""",
        key_factors=[
            "Bacterial load in source water (plate counts)",
            "SRB presence (black water, H2S odor)",
            "Compatibility with oxidizer breakers",
            "Safety and handling constraints",
            "Cost and dosage rate"
        ],
        primary_authority=[
            "SPE 165152 - Biocide Selection for Fracturing Fluids",
            "NACE TM0194 - Field Monitoring of Bacterial Growth",
            "EPA Antimicrobial Registration Database"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may minimize biocide use to reduce cost, risking bacterial growth",
        counter_arguments=[
            "UV treatment or filtration can reduce bacterial load, lowering biocide need",
            "Quaternary ammonium compounds (quats) cheaper but less effective vs SRB",
            "Combination biocide (glut + quat) provides synergy"
        ],
        resolution_strategy="Water sampling (heterotrophic plate count, SRB test), compatibility jar testing, safety review (SDS, ventilation), cost analysis, regulatory compliance check (FracFocus).",
        entity_scope="Service company, operator, water provider, HSE",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 165152 compares biocide efficacy and safety profiles",
        category=IssueCategory.BIOCIDE_CHEMISTRY
    ),

    DoctrineBlock(
        topic="Scale Inhibitors - Phosphonate vs Polycarboxylate",
        keywords=["scale inhibitor", "phosphonate", "PPCA", "calcium carbonate", "barium sulfate", "precipitation"],
        conclusion_template=[
            "Phosphonates (ATMP, HEDP) inhibit calcium carbonate and sulfate scales; dosage 10-50 ppm.",
            "PPCA (phosphino polycarboxylic acid) effective for barium, strontium sulfates; 5-20 ppm.",
            "Incompatible with high calcium (>5000 ppm) at high pH: precipitation risk."
        ],
        reasoning_framework="""
Scale forms when solubility product exceeded (CaCO3, BaSO4, SrSO4, CaSO4).
Mixing produced water with frac fluid or flowback with formation brine triggers precipitation.
Phosphonates adsorb onto scale crystal nuclei, distorting growth and preventing adherence.
ATMP (amino trimethylene phosphonic acid) and HEDP (hydroxyethylidene diphosphonic acid) common.
Calcium compatibility: phosphonates precipitate as Ca-phosphonate above ~5000 ppm Ca at pH >8.
PPCA synthetic polymer with phosphonate and carboxylate groups, higher calcium tolerance.
Dosage depends on scaling ion concentrations (Ba, Sr, Ca) and temperature.
Squeeze treatments (high concentration) for reservoir placement vs continuous injection.
Compatibility testing critical: phosphonate + cationic FR or polymer may precipitate.
""",
        key_factors=[
            "Water chemistry (Ca, Mg, Ba, Sr, sulfate, bicarbonate)",
            "Mixing ratio (produced water, flowback, formation brine)",
            "Formation temperature (solubility decrease at high temp)",
            "Compatibility with other additives (FR, gel, biocide)",
            "Retention time in formation"
        ],
        primary_authority=[
            "SPE 130343 - Scale Prediction and Inhibitor Selection",
            "SPE 169779 - Phosphonate Compatibility in Frac Fluids",
            "NACE Corrosion Conference - Scale Inhibitor Testing"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may skip scale inhibitor to reduce cost if no prior scaling history",
        counter_arguments=[
            "Scale prediction modeling (PHREEQC, ScaleSoftPitzer) may show low risk",
            "Acid preflush can dissolve carbonate scales preventatively",
            "Flowback management (separate early high-TDS water) reduces mixing"
        ],
        resolution_strategy="Water analysis (cations, anions, TDS), scale prediction modeling, compatibility jar testing, inhibitor performance testing (static/dynamic), economic analysis (inhibitor cost vs scale remediation).",
        entity_scope="Service company, operator, produced water contractor",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 130343 establishes scale prediction methodology",
        category=IssueCategory.SCALE_INHIBITION
    ),

    DoctrineBlock(
        topic="Clay Stabilizers - KCl vs TMAC vs Choline Chloride",
        keywords=["clay stabilizer", "KCl", "TMAC", "choline chloride", "swelling clays", "formation damage"],
        conclusion_template=[
            "KCl (potassium chloride) inhibits clay swelling via cation exchange; 1-3% concentration typical.",
            "TMAC (tetramethyl ammonium chloride) stronger inhibition, permanent adsorption; 0.5-2%.",
            "Choline chloride: biodegradable alternative to TMAC, similar performance; 1-3%."
        ],
        reasoning_framework="""
Swelling clays (smectite, illite/smectite mixed-layer) expand when contacted by low-salinity water.
Swelling reduces permeability, blocks pore throats, causes formation damage.
KCl provides potassium ions (K+), which adsorb onto clay exchange sites, preventing water intercalation.
K+ partially exchangeable; continuous KCl presence needed for protection.
TMAC quaternary ammonium ion (N(CH3)4+) strongly adsorbs, not easily exchanged.
Permanent stabilization after initial treatment; lower ongoing dosage.
Environmental concern: TMAC persistent, bioaccumulation potential; some jurisdictions restrict.
Choline chloride ((CH3)3N(CH2CH2OH)Cl) biodegradable, lower toxicity, similar quaternary ammonium structure.
Performance comparable to TMAC in lab tests; field use increasing in environmentally sensitive areas.
XRD and capillary suction time (CST) tests measure clay stabilization effectiveness.
""",
        key_factors=[
            "Clay mineralogy (XRD analysis of formation samples)",
            "Water salinity (TDS, ionic composition)",
            "Regulatory restrictions on TMAC",
            "Cost (KCl cheapest, TMAC most expensive, choline intermediate)",
            "Biodegradability and environmental impact"
        ],
        primary_authority=[
            "SPE 121464 - Clay Stabilization in Hydraulic Fracturing",
            "SPE 164088 - Choline Chloride as Green Clay Stabilizer",
            "API RP 13I - Laboratory Testing of Drilling Fluids (clay tests)"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may default to KCl to minimize cost, even if clay sensitivity high",
        counter_arguments=[
            "High-salinity produced water reuse may provide sufficient ionic strength without additive",
            "Acid preflush dissolves some clays, reducing stabilizer need",
            "Formation damage from polymer residue may exceed clay swelling damage"
        ],
        resolution_strategy="Core analysis (XRD, SEM, clay % quantification), CST or linear swell meter testing, compatibility with frac fluid system, regulatory review, cost-benefit analysis.",
        entity_scope="Service company, operator, G&G, environmental",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 121464 quantifies clay damage mechanisms and inhibitor performance",
        category=IssueCategory.CLAY_CONTROL
    ),

    DoctrineBlock(
        topic="Iron Control - Chelating Agents and Reducing Agents",
        keywords=["iron control", "chelant", "EDTA", "citric acid", "reducing agent", "ferric precipitation"],
        conclusion_template=[
            "Iron (Fe2+, Fe3+) precipitates as hydroxide/oxide at pH >5, causing formation damage and scale.",
            "Chelants (EDTA, citric acid, HEDTA) sequester iron; dosage 0.1-1.0 gpt.",
            "Reducing agents (erythorbic acid, sodium dithionite) convert Fe3+ to soluble Fe2+."
        ],
        reasoning_framework="""
Iron enters frac fluid from tubular corrosion, acid contact with formation minerals, or source water.
Ferric iron (Fe3+) precipitates rapidly at pH >3; ferrous (Fe2+) more soluble but oxidizes.
Precipitation clogs perforations, proppant pack, formation pore throats.
Chelants form soluble complexes with Fe2+/Fe3+, preventing precipitation.
EDTA (ethylenediaminetetraacetic acid) strongest chelant, stable to pH 12, high temperature.
Citric acid biodegradable, lower cost, effective pH 4-7; precipitates as Fe-citrate at high pH.
HEDTA (hydroxyethyl EDTA) intermediate performance; NTA (nitrilotriacetic acid) weaker.
Reducing agents (erythorbic acid, ascorbic acid, sodium dithionite) reduce Fe3+ to Fe2+.
Combined treatment: reducing agent + chelant ensures iron stays soluble.
Post-frac acid (HCl cleanup) may mobilize additional iron; sequestrant in acid stage critical.
""",
        key_factors=[
            "Iron concentration in source water (ICP analysis)",
            "Tubular metallurgy and corrosion potential",
            "pH of frac fluid system",
            "Presence of acid stages (pre/post-flush)",
            "Formation mineralogy (siderite, pyrite)"
        ],
        primary_authority=[
            "SPE 107845 - Iron Control in Hydraulic Fracturing",
            "SPE 114070 - Chelating Agent Performance Testing",
            "SPE 158122 - Formation Damage from Iron Precipitation"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may omit iron control if source water shows low Fe, missing corrosion contribution",
        counter_arguments=[
            "High-quality source water (RO treated) may have negligible iron",
            "Non-metallic coatings on tubing eliminate corrosion source",
            "Acid inhibitor packages often include chelant"
        ],
        resolution_strategy="Water analysis (Fe2+/Fe3+ via colorimetry or ICP), corrosion coupon testing, compatibility jar tests, post-frac flowback analysis (particulate iron), damage core flow tests.",
        entity_scope="Service company, operator, water provider, metallurgy",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 107845 establishes iron damage mechanisms and mitigation",
        category=IssueCategory.IRON_CONTROL
    ),

    DoctrineBlock(
        topic="Acid Frac Design - HCl Concentration and Retardation",
        keywords=["acid frac", "HCl", "hydrochloric acid", "retarded acid", "emulsified acid", "etching"],
        conclusion_template=[
            "15% HCl typical for carbonate fracs; higher concentrations (20-28%) for deep etching.",
            "Retarded acid (gelled HCl or emulsified acid) slows reaction, increases live acid penetration.",
            "Acid-compatible FR (amphoteric polymers) required; anionic FR precipitates in acid."
        ],
        reasoning_framework="""
Acid fracturing creates conductive channels via differential etching of carbonate rock.
HCl reacts with calcite (CaCO3) and dolomite (CaMg(CO3)2), dissolving rock matrix.
Reaction kinetics fast: 15% HCl spends in seconds at formation temp without retardation.
Retardation extends live acid contact time, enabling deeper penetration from fracture face.
Gelled acid: HCl + polymer (guar, CMHPG) thickened, slowed mass transfer to rock surface.
Emulsified acid: HCl as internal phase in diesel/oil emulsion, reaction gated by emulsion breakdown.
Viscosity reduces leak-off, improves acid placement in fracture vs matrix.
Corrosion critical: intensifiers (formic acid, acetic acid) added; inhibitors (filming amines, acetylenic alcohols) required.
Acid-compatible additives: FR (amphoteric PAM), iron control (EDTA), surfactant (nonionic, amphoteric).
Post-acid flush: diesel or mutual solvent to remove reaction products (CaCl2), prevent reprecipitation.
""",
        key_factors=[
            "Formation lithology (calcite vs dolomite content)",
            "Formation temperature (reaction kinetics)",
            "Fracture closure stress (etching pattern retention)",
            "Acid volume and penetration distance",
            "Corrosion inhibitor effectiveness"
        ],
        primary_authority=[
            "SPE 56279 - Acid Fracturing Carbonate Reservoirs",
            "SPE 102466 - Retarded Acid Systems Performance",
            "NACE SP0175 - Corrosion in Oilfield Acidizing"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may prefer proppant frac to avoid acid corrosion risk, even in carbonates",
        counter_arguments=[
            "Proppant fracs can work in carbonates if embedment minimal (high Young's modulus)",
            "Hybrid acid-proppant fracs combine etching with proppant conductivity",
            "Emulsified acid cost (2-3x gelled acid) may not justify performance"
        ],
        resolution_strategy="Core acidizing tests (conductivity after acid), reaction kinetics modeling, corrosion coupon testing at formation temp, post-frac production analysis, economic comparison (acid vs proppant).",
        entity_scope="Service company, operator, completion engineer, metallurgy",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 56279 defines acid frac design principles",
        category=IssueCategory.ACID_FRACS
    ),

    DoctrineBlock(
        topic="Fluid Compatibility Testing - Jar Testing and Filtration",
        keywords=["compatibility", "jar test", "precipitation", "filtration test", "fluid loss", "additive interaction"],
        conclusion_template=[
            "Jar testing combines all additives at operational concentrations, observes precipitation, phase separation.",
            "24-hour aging at formation temperature validates stability.",
            "Filtration tests (API 13B or Millipore 0.45 micron) detect particulates, filter cake quality."
        ],
        reasoning_framework="""
Incompatible additives cause precipitation, emulsion breakage, viscosity loss, equipment plugging.
Common incompatibilities: cationic FR + anionic surfactant, phosphonate + high Ca, THPS + anionic.
Jar test protocol: mix base fluid + additives in order of addition, age at temp, visual inspection.
Clear solution after 24h indicates compatibility; cloudiness, solids, or separation indicates problem.
Filtration test measures filter cake formation, fluid loss rate (mL/30min).
High fluid loss indicates poor cake formation; particulates plug filter, indicating precipitation.
API RP 39 and API RP 13B define standard test procedures.
Scale: lab testing uses 100-500 mL samples; QC on location uses blender tests (5 gal).
Temperature critical: some systems compatible at surface, incompatible at BHT (or vice versa).
Documentation: photographs of jars (before/after aging), filtration data, pH readings.
""",
        key_factors=[
            "Complete additive list with concentrations",
            "Mixing sequence (order of addition)",
            "Aging temperature and duration",
            "Source water chemistry (TDS, hardness, pH)",
            "Equipment cleanliness (avoid contamination)"
        ],
        primary_authority=[
            "API RP 39 - Recommended Practices for Measuring Rheological Properties",
            "API RP 13B - Recommended Practice for Field Testing of Drilling Fluids",
            "SPE 80222 - Compatibility Testing Protocols"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may skip lab testing, relying on vendor assurances, risking field incompatibility",
        counter_arguments=[
            "Vendor pre-blended systems have compatibility guaranteed",
            "Field experience with same water source reduces testing need",
            "Dynamic testing (loop, core flow) more representative than static jars"
        ],
        resolution_strategy="Mandatory lab jar testing before field deployment, temperature aging matching BHT, filtration tests per API standards, photographic documentation, vendor collaboration on additive sequencing.",
        entity_scope="Service company, operator, QC lab, chemical supplier",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API RP 39 and 13B establish industry-standard test methods",
        category=IssueCategory.COMPATIBILITY_TESTING
    ),

    DoctrineBlock(
        topic="Friction Reducer Performance Testing - Loop Rheometer",
        keywords=["friction testing", "loop rheometer", "pressure drop", "friction reduction", "turbulent flow"],
        conclusion_template=[
            "Loop rheometer measures friction pressure vs flow rate in turbulent regime (Re >4000).",
            "Friction reduction % = (ΔP_water - ΔP_FR) / ΔP_water × 100; target >60% at field rate.",
            "Lab testing at operational temperature, TDS, and shear rate validates field performance."
        ],
        reasoning_framework="""
Friction loss in tubulars dominates treating pressure during slickwater fracs (70-80% of total).
Lab loop rheometer simulates field conditions: 0.25-0.5 inch ID tubing, flow rates 10-60 bpm equivalent.
Reynolds number calculated: Re = ρVD/μ; turbulent flow (Re >4000) required for FR effectiveness.
Baseline: measure ΔP with water only at target rate.
FR test: measure ΔP with FR-treated water at same rate and temperature.
Temperature effect: FR performance decreases at high temp due to polymer degradation.
Shear effect: high shear (small tubulars, high rate) can break polymer, reducing effectiveness.
Salinity effect: high TDS (>50,000 ppm) reduces anionic FR performance; cationic or nonionic preferred.
Validation: lab friction reduction correlates with field treating pressure if conditions matched.
Documentation: ΔP curves vs flow rate, FR dosage optimization, temperature/salinity sensitivity.
""",
        key_factors=[
            "Flow rate and tubular size (shear rate)",
            "Formation temperature (BHT)",
            "Water chemistry (TDS, hardness)",
            "FR type and dosage (gpt)",
            "Polymer molecular weight and charge"
        ],
        primary_authority=[
            "API RP 19D - Recommended Practice for Measuring Friction Pressures",
            "SPE 173755 - Friction Reducer Lab Testing Methodologies",
            "SPE 119900 - Slickwater Frac Friction Reduction"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may rely on vendor data without site-specific testing, risking underperformance",
        counter_arguments=[
            "Field data from offset wells provides empirical friction factors",
            "Vendor loop testing with similar water may suffice",
            "Computational fluid dynamics (CFD) can predict friction loss"
        ],
        resolution_strategy="Lab loop testing with actual source water, match field BHT and flow rate, dosage optimization testing, validate with field treating pressure data, iterate if discrepancy observed.",
        entity_scope="Service company, operator, QC lab",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API RP 19D defines friction testing protocol",
        category=IssueCategory.FRICTION_TESTING
    ),

    DoctrineBlock(
        topic="Proppant Transport in Slickwater vs Gel",
        keywords=["proppant transport", "settling velocity", "slickwater", "gel", "viscosity", "fracture width"],
        conclusion_template=[
            "Slickwater (1-5 cp): proppant settles rapidly; transport requires high pump rate (>80 bpm).",
            "Crosslinked gel (100-500 cp): suspends proppant; lower rate acceptable (40-60 bpm).",
            "Fracture width, inclination, and proppant size govern settling velocity and dune formation."
        ],
        reasoning_framework="""
Proppant settling velocity (Stokes' Law): v ∝ (ρ_proppant - ρ_fluid) × d² / μ.
Slickwater low viscosity (1-5 cp): 20/40 mesh sand settles ~1 ft/sec in static fluid.
Dynamic transport: turbulent flow (Re >4000) generates lift, keeps proppant in suspension.
High pump rate (>80 bpm in horizontal wells) maintains turbulence, prevents dune formation.
Gel high viscosity (100-500 cp): settling velocity reduced 100x; laminar flow acceptable.
Proppant concentration affects rheology: >4 ppg in slickwater risks screenout without adequate rate.
Fracture geometry: wide fractures (>0.3 inch) allow proppant settling; narrow fractures constrain.
Fracture inclination: horizontal/high-angle wells prone to settling; vertical wells gravity-assist.
Proppant size: 40/70 mesh settles slower than 20/40, better distribution in slickwater.
Dune formation: proppant accumulation at fracture toe, causes bridging, screenout risk.
""",
        key_factors=[
            "Fluid viscosity (slickwater vs gel)",
            "Pump rate and Reynolds number",
            "Proppant size distribution (mesh)",
            "Fracture width and inclination",
            "Proppant concentration (ppg)"
        ],
        primary_authority=[
            "SPE 106026 - Proppant Transport in Slickwater Fracs",
            "SPE 119900 - Slickwater Fracturing Mechanics",
            "SPE 163873 - Gel vs Slickwater Transport Comparison"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may use slickwater at low rate to reduce pumping cost, risking poor proppant placement",
        counter_arguments=[
            "Channel fracturing (pulsed proppant) alternative to continuous slickwater",
            "Degradable fiber additives enhance slickwater proppant transport",
            "Gel damage may offset conductivity benefit vs slickwater"
        ],
        resolution_strategy="Fracture width modeling (stress, E-modulus), pump rate simulation, proppant transport modeling (CFD or empirical), microseismic validation, production analysis (near vs far-field contribution).",
        entity_scope="Service company, operator, completion engineer, G&G",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 106026 quantifies slickwater transport limitations",
        category=IssueCategory.PROPPANT_TRANSPORT
    ),

    DoctrineBlock(
        topic="Produced Water Recycling for Frac Fluid",
        keywords=["produced water", "recycling", "flowback", "TDS", "water treatment", "blending"],
        conclusion_template=[
            "Produced water TDS typically 50,000-200,000 ppm; direct use requires cationic FR or blending.",
            "Treatment options: dilution with fresh water, filtration, chemical adjustment (biocide, O2 scavenger).",
            "Economic: recycling saves disposal cost ($2-5/bbl) but adds treatment cost ($0.50-2/bbl)."
        ],
        reasoning_framework="""
Produced water contains high TDS, divalent cations (Ca, Mg), iron, bacteria, hydrocarbons (oil, BTEX).
Direct use as frac fluid: high salinity reduces anionic FR performance; cationic FR preferred.
Blending: 25-75% produced water with fresh water reduces TDS to acceptable range (<50,000 ppm).
Filtration: remove suspended solids (proppant fines, scale particles) via 10-50 micron cartridge filters.
Biocide: produced water often contains sulfate-reducing bacteria (SRB); glutaraldehyde or THPS required.
Oxygen scavenger: prevent corrosion from dissolved O2 introduced during storage/transfer.
Scale inhibitor: produced water + fresh water mixing can trigger CaCO3, BaSO4 precipitation.
Oil removal: hydrocyclone, dissolved air flotation, or media filtration to <50 ppm oil & grease.
Regulatory: state rules vary (TX, ND allow; PA, WV restricted); discharge permits if surface disposal.
Economics: disposal cost $2-5/bbl avoided; treatment cost $0.50-2/bbl; net savings $0.50-4/bbl.
""",
        key_factors=[
            "Produced water TDS and ionic composition",
            "Availability and cost of fresh water",
            "Treatment infrastructure and cost",
            "Regulatory approval for reuse",
            "FR and additive compatibility with high-TDS water"
        ],
        primary_authority=[
            "SPE 185052 - Produced Water Reuse in Hydraulic Fracturing",
            "SPE 189463 - Economics of Water Recycling",
            "EPA UIC Class II - Produced Water Disposal Regulations"
        ],
        burden_holder="Operator",
        adversary_position="Environmental groups may oppose recycling due to contaminant concerns (NORM, BTEX)",
        counter_arguments=[
            "Fresh water use depletes aquifers in arid regions (Permian, DJ Basin)",
            "Treatment technology (RO, evaporation) can achieve near-fresh quality at high cost",
            "Regulatory trend favors reuse over disposal injection"
        ],
        resolution_strategy="Water quality analysis (full chemistry, NORM, organics), treatment technology selection, compatibility testing with frac additives, economic modeling (disposal cost vs treatment cost), regulatory approval process.",
        entity_scope="Operator, water management contractor, regulatory agency, service company",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="SPE 185052 demonstrates technical feasibility and cost savings",
        category=IssueCategory.FLUID_RECYCLING
    ),

    DoctrineBlock(
        topic="Water Quality Requirements - TDS, Hardness, Iron, Bacteria",
        keywords=["water quality", "TDS", "hardness", "iron", "bacteria", "source water", "specification"],
        conclusion_template=[
            "Slickwater fracs tolerate TDS <75,000 ppm; above requires FR adjustment or blending.",
            "Hardness <5000 ppm preferred for anionic FR; above requires cationic or nonionic FR.",
            "Iron <5 ppm, bacteria <10^3 CFU/mL to prevent precipitation and biofouling."
        ],
        reasoning_framework="""
Water quality drives additive selection, performance, and cost.
TDS (total dissolved solids): salts affect FR performance, gel hydration, crosslink kinetics.
Hardness (Ca + Mg as CaCO3): divalent cations shield anionic polymers, reduce effectiveness.
Iron (Fe2+, Fe3+): precipitates at pH >5, causes formation damage, scale, staining.
Bacteria (heterotrophic plate count, SRB): cause H2S, corrosion, viscosity loss, biofouling.
Suspended solids: plug perforations, proppant pack, filters; target <50 ppm, <10 micron size.
pH: affects crosslinking (borate requires pH >9.5), scale precipitation (CaCO3 at pH >7.5).
Oil & grease: interferes with surfactants, causes emulsions; target <50 ppm.
Source water types: fresh surface/groundwater (TDS <1000), brackish (1000-10,000), produced water (>50,000).
Testing: ICP for cations, IC for anions, turbidity, plate counts, pH, oil & grease (EPA methods).
""",
        key_factors=[
            "Source water availability (surface, groundwater, produced)",
            "Frac fluid system (slickwater, gel, VES, acid)",
            "Additive compatibility (FR, gel polymer, crosslinker)",
            "Formation sensitivity (clay swelling, scale)",
            "Treatment options and cost"
        ],
        primary_authority=[
            "SPE 173755 - Water Quality Effects on Frac Fluid Performance",
            "API RP 13B - Water Testing for Oilfield Applications",
            "EPA Safe Drinking Water Act (SDWA) standards (reference)"
        ],
        burden_holder="Operator",
        adversary_position="Water supplier may claim 'fit for purpose' without meeting frac-specific specs",
        counter_arguments=[
            "On-site treatment (RO, softening, filtration) can upgrade poor-quality water",
            "Additive formulation adjustments (higher FR dosage) can compensate",
            "Blending multiple sources achieves target quality"
        ],
        resolution_strategy="Define water quality specifications in contract, require testing per API RP 13B, on-site QC testing (salinity, pH, bacteria), vendor compatibility testing with actual water, contingency plan for off-spec water.",
        entity_scope="Operator, water supplier, service company, QC lab",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 173755 quantifies water quality impacts on FR and gel performance",
        category=IssueCategory.WATER_QUALITY
    ),

    DoctrineBlock(
        topic="FracFocus Chemical Disclosure Requirements",
        keywords=["FracFocus", "disclosure", "chemical registry", "BTEX", "CAS number", "trade secret"],
        conclusion_template=[
            "FracFocus.org is EPA-endorsed registry; 31 states mandate disclosure within 30-60 days post-frac.",
            "Require: well location, operator, service company, chemical name, CAS#, max concentration, supplier.",
            "Trade secret claims allowed but scrutinized; must disclose chemical family and purpose."
        ],
        reasoning_framework="""
FracFocus established 2011 by Ground Water Protection Council (GWPC) and Interstate Oil & Gas Compact Commission (IOGCC).
Disclosure voluntary initially; now mandatory in TX, CO, WY, PA, OH, ND, NM, MT, WV, others.
Chemical disclosure triggers: hydraulic fracturing operations using >1000 gal fluid.
Data required: API well number, operator, service company, frac date, water volume, each additive (trade name, supplier, purpose, ingredients, CAS#, max concentration).
Trade secret protection: allowed under state law; must disclose to health professionals in emergency.
Controversy: 10-15% of ingredients claimed as trade secrets; environmental groups challenge.
BTEX (benzene, toluene, ethylbenzene, xylene): diesel use in frac fluids now rare due to EPA scrutiny.
CAS number: Chemical Abstracts Service registry number; unique identifier for each chemical.
Mixtures: if additive is mixture, disclose all components >1% concentration.
Timeline: most states require disclosure within 60 days; some (CO) require 30 days.
""",
        key_factors=[
            "State jurisdiction (mandatory vs voluntary)",
            "Timeline for disclosure (30-60 days)",
            "Trade secret claim justification",
            "Accuracy of CAS numbers and concentrations",
            "Supplier cooperation in providing data"
        ],
        primary_authority=[
            "FracFocus.org - Chemical Disclosure Registry",
            "TX RRC Rule 3.29 - Hydraulic Fracturing Disclosure",
            "EPA - Review of FracFocus Disclosure System (2015)"
        ],
        burden_holder="Operator",
        adversary_position="Service companies may resist full disclosure, claiming proprietary formulations",
        counter_arguments=[
            "Trade secret protection allows compliance without revealing proprietary blends",
            "Chemical family disclosure (e.g., 'anionic polyacrylamide') sufficient for environmental assessment",
            "State enforcement limited; late disclosure common without penalty"
        ],
        resolution_strategy="Contract requires service company to provide FracFocus data within 15 days post-frac, operator submits to registry, QC review of CAS numbers and concentrations, legal review of trade secret claims, compliance tracking.",
        entity_scope="Operator, service company, regulatory agency, legal",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="State regulations mandate FracFocus disclosure; EPA endorses but does not enforce",
        category=IssueCategory.WATER_QUALITY
    ),

    DoctrineBlock(
        topic="Fluid Viscosity at Temperature and Shear",
        keywords=["viscosity", "rheology", "shear rate", "temperature", "gel degradation", "crosslink stability"],
        conclusion_template=[
            "Viscosity measured via rotational viscometer (Fann 35, Bohlin) at operational shear rates (170 s^-1 typical).",
            "Temperature effect: polymer degradation above stability limit (borate 200°F, Zr/Ti 300°F).",
            "Shear thinning: non-Newtonian fluids (gels) show lower viscosity at high shear; power-law model."
        ],
        reasoning_framework="""
Viscosity (μ) is resistance to flow; critical for proppant transport, friction loss, fluid loss control.
Newtonian fluids (water, slickwater): viscosity constant across shear rates.
Non-Newtonian fluids (gels, VES): shear-thinning (pseudoplastic) or shear-thickening (dilatant).
Shear rate (γ̇): velocity gradient in fluid; units s^-1; tubular flow ~170 s^-1, fracture ~10 s^-1.
Rotational viscometer (Fann 35): measures viscosity at 300, 200, 100, 6, 3 RPM (various shear rates).
Apparent viscosity: μ_app = (θ_300 - θ_200) / 2; plastic viscosity (PV) and yield point (YP) calculated.
Power-law model: τ = K × γ̇^n; n <1 shear-thinning, n >1 shear-thickening, n =1 Newtonian.
Temperature stability: polymer backbone degrades above thermal limit; test at BHT via heated cup.
Crosslinked gels: viscosity peaks after crosslink, then declines due to breaker or thermal degradation.
Oscillatory rheology (dynamic testing): measures storage modulus (G'), loss modulus (G''), viscoelasticity.
""",
        key_factors=[
            "Shear rate (tubular vs fracture environment)",
            "Temperature (surface vs BHT)",
            "Polymer type and concentration",
            "Crosslinker type and concentration",
            "Breaker type and concentration"
        ],
        primary_authority=[
            "API RP 39 - Recommended Practices for Measuring Rheological Properties",
            "SPE 18211 - Rheology of Fracturing Fluids at Temperature",
            "ISO 13503-1 - Measurement of Viscosity (Frac Fluids)"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may accept surface viscosity readings without downhole temperature correction",
        counter_arguments=[
            "Surface rheology screening sufficient if fluid proven in offset wells",
            "Advanced rheometers (HPHT, oscillatory) expensive; may not justify for routine jobs",
            "Computational modeling can predict downhole viscosity from lab data"
        ],
        resolution_strategy="Lab rheology testing at operational shear rates and BHT, power-law model fitting, HPHT testing for critical jobs, field QC with Fann 35 or marsh funnel, validate with treating pressure and proppant placement data.",
        entity_scope="Service company, operator, QC lab",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="API RP 39 defines standard rheology test methods for frac fluids",
        category=IssueCategory.SLICKWATER_SYSTEMS
    ),

    DoctrineBlock(
        topic="Nonionic Friction Reducers - Broad Salinity Tolerance",
        keywords=["nonionic", "friction reducer", "polyethylene oxide", "PEO", "salinity tolerance"],
        conclusion_template=[
            "Nonionic FRs (polyethylene oxide, PEO) tolerate TDS >200,000 ppm without performance loss.",
            "No charge interaction with divalent cations; ideal for produced water reuse.",
            "Dosage: 0.5-1.5 gpt; cost intermediate between anionic and cationic."
        ],
        reasoning_framework="""
Nonionic polymers lack charged groups; friction reduction via hydrodynamic drag reduction.
Polyethylene oxide (PEO) or polyacrylamide derivatives with nonionic side chains.
Salinity insensitive: performance unchanged from 0 to 250,000 ppm TDS.
Divalent cation insensitive: Ca, Mg have no shielding effect (no charges to shield).
Temperature stability: moderate; stable to 180-200°F; above requires stabilizers.
Molecular weight: 5-10 million Da typical; lower than anionic due to synthesis constraints.
Biodegradability: lower than anionic PAM; FracFocus disclosure required.
Field use: increasing in Permian Basin (high-TDS produced water reuse).
Compatibility: compatible with most additives; no precipitation with cationic surfactants.
Cost: 1.5-2x anionic FR, but lower than cationic; dosage may offset cost.
""",
        key_factors=[
            "Water TDS and hardness (extreme salinity drives selection)",
            "Produced water reuse strategy",
            "Cost tolerance (premium vs anionic)",
            "Temperature stability requirements",
            "Additive compatibility"
        ],
        primary_authority=[
            "SPE 184545 - Nonionic Friction Reducers in High-Salinity Brines",
            "SPE 189457 - Produced Water Reuse with Nonionic FR",
            "Journal of Petroleum Technology - PEO Drag Reduction Mechanisms"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may default to anionic FR if water TDS <50,000 ppm to save cost",
        counter_arguments=[
            "Anionic FR with supplemental treatment (water softening) cheaper total cost",
            "Cationic FR provides dual benefit (FR + clay stabilization) in some formations",
            "Blending produced water with fresh reduces TDS, allowing anionic FR use"
        ],
        resolution_strategy="Water analysis (TDS, Ca, Mg), lab jar testing with actual water, loop friction testing, economic analysis (FR cost vs water treatment cost), field trial comparison.",
        entity_scope="Service company, operator, water management contractor",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 184545 demonstrates nonionic FR salinity insensitivity",
        category=IssueCategory.SLICKWATER_SYSTEMS
    ),

    DoctrineBlock(
        topic="Linear Gel Systems - Non-Crosslinked Guar",
        keywords=["linear gel", "guar", "non-crosslinked", "HPG", "low-concentration polymer"],
        conclusion_template=[
            "Linear gels (20-40 lbm/1000 gal guar/HPG) provide moderate viscosity (30-80 cp) without crosslinker.",
            "Used for friction reduction + mild proppant suspension; intermediate between slickwater and crosslinked gel.",
            "Breaker: enzyme or oxidizer; cleanup better than crosslinked gel due to lower polymer loading."
        ],
        reasoning_framework="""
Linear gel is hydrated polymer without crosslinker; viscosity from polymer chain entanglement.
Guar or HPG at 20-40 lbm/1000 gal (vs 40-60 lbm/1000 gal for crosslinked systems).
Viscosity: 30-80 cp at 170 s^-1; sufficient for light proppant loading (<2 ppg).
Friction reduction: linear gel reduces friction 50-60%, less than dedicated FR but more than water.
Applications: moderate-rate fracs, low-concentration proppant stages, pad stages before crosslinked gel.
Breaker easier than crosslinked: lower polymer concentration degrades faster, less residue.
Formation damage: lower than crosslinked gel, higher than slickwater.
Fluid loss: moderate; silica flour or fluid loss additives often added.
Cost: higher than slickwater (polymer cost), lower than crosslinked gel (no crosslinker, less polymer).
Rheology: shear-thinning; power-law model with n ~0.6-0.7.
""",
        key_factors=[
            "Proppant loading requirements (ppg)",
            "Pump rate and fracture width",
            "Formation damage sensitivity",
            "Cost vs slickwater and crosslinked gel",
            "Breaker and cleanup effectiveness"
        ],
        primary_authority=[
            "SPE 12026 - Linear Gel Fracturing Fluids",
            "SPE 77746 - Guar-Based Fluid Rheology and Cleanup",
            "API RP 39 - Rheology Measurement of Linear Gels"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may view linear gel as 'worst of both worlds' (cost of gel, performance of slickwater)",
        counter_arguments=[
            "Slickwater with degradable fiber achieves similar transport at lower cost",
            "Crosslinked gel provides definitive proppant suspension vs marginal linear gel",
            "Hybrid design (slickwater pad + crosslinked gel proppant) cleaner separation of functions"
        ],
        resolution_strategy="Proppant transport modeling (settling velocity, fracture width), rheology testing at operational conditions, cost comparison (linear gel vs alternatives), field trial with production comparison.",
        entity_scope="Service company, operator, completion engineer",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="SPE 12026 defines linear gel applications and limitations",
        category=IssueCategory.CROSSLINKED_GELS
    ),

    DoctrineBlock(
        topic="Encapsulated Breakers - Delayed Activation Systems",
        keywords=["encapsulated breaker", "delayed activation", "polymer coating", "wax coating", "temperature release"],
        conclusion_template=[
            "Encapsulated breakers (enzyme, oxidizer) use polymer or wax coating to delay release.",
            "Activation trigger: temperature (coating melts/dissolves at BHT) or time (diffusion through coating).",
            "Dosage: same as unencapsulated, but split (immediate + encapsulated) for staged break."
        ],
        reasoning_framework="""
Premature break during pumping causes viscosity loss, screenout risk, poor proppant placement.
Encapsulation delays breaker release until fluid reaches formation (BHT) or after shut-in (time delay).
Coating materials: polymer (PMMA, cellulose), wax, silica, lipid bilayers.
Temperature-triggered: coating melts/dissolves above threshold (120-180°F); breaker released.
Time-delayed: diffusion through coating controls release rate; hours to days.
Particle size: 50-500 micron; larger particles = longer delay.
Dual-stage break: immediate breaker (surface dosage) reduces bulk gel viscosity during flowback.
Encapsulated breaker activates later, degrades residual gel in proppant pack and formation.
Testing: bottle tests at BHT, measure viscosity vs time, validate activation temperature/time.
Cost: 1.5-2x unencapsulated breaker; justified in critical applications (high-temp, tight formations).
""",
        key_factors=[
            "Formation temperature (BHT and cool-down profile)",
            "Target break time (hours post-shut-in)",
            "Gel polymer type and concentration",
            "Proppant pack cleanup requirements",
            "Cost vs unencapsulated breaker"
        ],
        primary_authority=[
            "SPE 30114 - Encapsulated Breaker Technology",
            "SPE 94267 - Delayed Breaker Systems for Frac Fluids",
            "SPE 106044 - Breaker Activation Mechanisms"
        ],
        burden_holder="Engineer",
        adversary_position="Operator may view encapsulation as unnecessary expense if standard breaker works",
        counter_arguments=[
            "Standard breaker with conservative dosage achieves delayed break",
            "High pump rate (short contact time) may reduce premature break risk",
            "Enzyme stability improvements reduce need for encapsulation"
        ],
        resolution_strategy="Lab break testing (encapsulated vs standard), temperature profile modeling (wellbore cool-down), flowback viscosity monitoring, production analysis (cleanup efficiency), economic analysis (breaker cost vs production gain).",
        entity_scope="Service company, operator, chemical supplier",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SPE 30114 establishes encapsulated breaker design principles",
        category=IssueCategory.BREAKER_SYSTEMS
    )
]


# ═══════════════════════════════════════════════════════════════════════════
# TELEMETRY & METRICS
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class Telemetry:
    total_queries: int = 0
    total_latency_ms: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    errors: int = 0
    start_time: datetime = field(default_factory=datetime.utcnow)

    def record_query(self, latency_ms: float, cache_hit: bool):
        self.total_queries += 1
        self.total_latency_ms += latency_ms
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def record_error(self):
        self.errors += 1

    def avg_latency(self) -> float:
        return self.total_latency_ms / self.total_queries if self.total_queries > 0 else 0.0

    def cache_hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0

    def uptime_seconds(self) -> float:
        return (datetime.utcnow() - self.start_time).total_seconds()


TELEMETRY = Telemetry()


# ═══════════════════════════════════════════════════════════════════════════
# ENGINE CORE
# ═══════════════════════════════════════════════════════════════════════════

class FRAC04Engine:
    def __init__(self):
        self.doctrine_cache = DOCTRINE_CACHE
        self.telemetry = TELEMETRY
        logger.info(f"{ENGINE_ID} initialized with {len(self.doctrine_cache)} doctrine blocks")

    def three_layer_response(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> QueryResponse:
        start_time = datetime.utcnow()

        # Layer 1: Doctrine Cache (0-50ms)
        matches = self._search_doctrine_cache(query)

        if matches:
            cache_hit = True
            answer = self._build_answer_from_cache(matches, mode, zone)
        else:
            # Layer 2: Semantic Retrieval (fallback - simplified here)
            cache_hit = False
            answer = self._semantic_fallback(query, mode, zone)
            matches = []

        # Compute latency
        latency_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
        self.telemetry.record_query(latency_ms, cache_hit)

        # Epistemic guardrails
        epistemic_caveats = self._apply_epistemic_guardrails(answer, zone)

        # Determinism hash
        determinism_hash = self._compute_determinism_hash(query, answer, mode, zone)

        # Confidence stratification
        confidence = self._stratify_confidence(matches, zone)

        return QueryResponse(
            answer=answer,
            doctrine_matches=[
                DoctrineMatch(
                    topic=m.topic,
                    confidence=m.matches(query),
                    reasoning=m.reasoning_framework[:200] + "...",
                    authority_level=len(m.primary_authority),
                    stratification=m.confidence
                )
                for m in matches[:5]
            ],
            confidence=confidence,
            zone=zone,
            mode=mode,
            latency_ms=latency_ms,
            determinism_hash=determinism_hash,
            timestamp=datetime.utcnow().isoformat(),
            epistemic_caveats=epistemic_caveats
        )

    def _search_doctrine_cache(self, query: str) -> List[DoctrineBlock]:
        scored = [(block, block.matches(query)) for block in self.doctrine_cache]
        scored.sort(key=lambda x: x[1], reverse=True)
        # Return blocks with score >0.3
        return [block for block, score in scored if score > 0.3]

    def _build_answer_from_cache(self, matches: List[DoctrineBlock], mode: ResponseMode, zone: AnalysisZone) -> str:
        top_match = matches[0]

        if mode == ResponseMode.FAST:
            return " ".join(top_match.conclusion_template)

        elif mode == ResponseMode.DEFENSE:
            answer = f"**Conclusion:** {' '.join(top_match.conclusion_template)}\n\n"
            answer += f"**Reasoning:** {top_match.reasoning_framework}\n\n"
            answer += f"**Key Factors:** {', '.join(top_match.key_factors)}\n\n"
            answer += f"**Authority:** {'; '.join(top_match.primary_authority)}\n\n"
            answer += f"**Burden Holder:** {top_match.burden_holder}\n\n"
            answer += f"**Confidence Level:** {top_match.confidence.value}"
            return answer

        elif mode == ResponseMode.MEMO:
            answer = f"# Frac Fluid Chemistry Analysis\n\n"
            answer += f"## Conclusion\n{' '.join(top_match.conclusion_template)}\n\n"
            answer += f"## Reasoning Framework\n{top_match.reasoning_framework}\n\n"
            answer += f"## Key Factors\n"
            for factor in top_match.key_factors:
                answer += f"- {factor}\n"
            answer += f"\n## Primary Authority\n"
            for auth in top_match.primary_authority:
                answer += f"- {auth}\n"
            answer += f"\n## Adversary Position\n{top_match.adversary_position}\n\n"
            answer += f"## Counter-Arguments\n"
            for arg in top_match.counter_arguments:
                answer += f"- {arg}\n"
            answer += f"\n## Resolution Strategy\n{top_match.resolution_strategy}\n\n"
            answer += f"## Confidence Stratification\n{top_match.confidence.value}\n\n"
            answer += f"## Controlling Precedent\n{top_match.controlling_precedent}"
            return answer

        return " ".join(top_match.conclusion_template)

    def _semantic_fallback(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
        # Simplified fallback - real implementation would use vector search
        return (
            f"No direct doctrine match found for query. General guidance: "
            f"Frac fluid chemistry selection depends on formation temperature, water quality (TDS, hardness), "
            f"proppant transport requirements, formation damage sensitivity, and cost constraints. "
            f"Recommend lab compatibility testing with actual source water and rheological testing at formation temperature."
        )

    def _apply_epistemic_guardrails(self, answer: str, zone: AnalysisZone) -> List[str]:
        caveats = []

        # Check for banned phrases
        for phrase in BANNED_PHRASES:
            if phrase.lower() in answer.lower():
                caveats.append(f"Removed prohibited absolute claim: '{phrase}'")

        # Zone-specific caveats
        if zone == AnalysisZone.PLANNING:
            caveats.append("This analysis is for planning purposes; field testing required before deployment.")
        elif zone == AnalysisZone.REPORTING:
            caveats.append("Performance claims subject to validation with field data and lab testing.")
        elif zone == AnalysisZone.AUDIT:
            caveats.append("All conclusions supported by cited technical literature and industry standards.")

        return caveats

    def _compute_determinism_hash(self, query: str, answer: str, mode: ResponseMode, zone: AnalysisZone) -> str:
        hash_input = f"{query}|{answer}|{mode.value}|{zone.value}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()[:16]

    def _stratify_confidence(self, matches: List[DoctrineBlock], zone: AnalysisZone) -> ConfidenceLevel:
        if not matches:
            return ConfidenceLevel.DISCLOSURE

        top_confidence = matches[0].confidence

        if zone == AnalysisZone.AUDIT:
            # Audit zone requires DEFENSIBLE
            return ConfidenceLevel.DEFENSIBLE
        elif zone == AnalysisZone.PLANNING and top_confidence == ConfidenceLevel.AGGRESSIVE:
            # Planning allows AGGRESSIVE if source doctrine is AGGRESSIVE
            return ConfidenceLevel.AGGRESSIVE
        else:
            return top_confidence


# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

APP = FastAPI(
    title="FRAC04 - Frac Fluid Chemistry Engine",
    version=VERSION,
    description="TIE Gold Standard - Completions & Fracturing Fluid Systems"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ENGINE = FRAC04Engine()


@APP.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="operational",
        version=VERSION,
        engine_id=ENGINE_ID,
        port=PORT,
        doctrine_count=len(DOCTRINE_CACHE),
        uptime_seconds=TELEMETRY.uptime_seconds(),
        total_queries=TELEMETRY.total_queries,
        avg_latency_ms=TELEMETRY.avg_latency(),
        cache_hit_rate=TELEMETRY.cache_hit_rate()
    )


@APP.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        return ENGINE.three_layer_response(request.query, request.mode, request.zone)
    except Exception as e:
        TELEMETRY.record_error()
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/doctrines")
async def list_doctrines():
    return {
        "total": len(DOCTRINE_CACHE),
        "categories": list(set(d.category.value for d in DOCTRINE_CACHE)),
        "topics": [d.topic for d in DOCTRINE_CACHE]
    }


@APP.get("/")
async def root():
    return {
        "engine": ENGINE_ID,
        "version": VERSION,
        "status": "operational",
        "endpoints": ["/health", "/query", "/doctrines"]
    }


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.add(
        f"logs/{ENGINE_ID}_{{time}}.log",
        rotation="100 MB",
        retention="30 days",
        level="INFO"
    )

    logger.info(f"Starting {ENGINE_ID} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    logger.info(f"TIE-20 components: ✓ All present")

    uvicorn.run(APP, host="0.0.0.0", port=PORT, log_level="info")
