"""
CHEM15 Water Chemistry Intelligence Engine
TIE-Grade Compliance | Port 9297 | Version 1.0.0

Domain: Water quality analysis, treatment processes, disinfection, scale/corrosion control,
produced water treatment, regulatory compliance (CWA, SDWA).

Authority: EPA regulations, AWWA standards, API RP 45, NACE guidelines, state NPDES permits,
water chemistry textbooks (Stumm & Morgan, Snoeyink & Jenkins).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# =========================================================
# CONFIGURATION
# =========================================================

ENGINE_ID = "CHEM15"
ENGINE_NAME = "Water Chemistry Intelligence Engine"
VERSION = "1.0.0"
PORT = 9297
DOCTRINE_COUNT = 28
LOG_FILE = Path(__file__).parent / "chem15_audit.jsonl"

# =========================================================
# ENUMS & DATA MODELS
# =========================================================

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
    WATER_QUALITY = "WATER_QUALITY"
    SCALE_CORROSION = "SCALE_CORROSION"
    TREATMENT_DESIGN = "TREATMENT_DESIGN"
    DISINFECTION = "DISINFECTION"
    PRODUCED_WATER = "PRODUCED_WATER"
    REGULATORY = "REGULATORY"
    ANALYTICAL = "ANALYTICAL"

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
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    category: IssueCategory

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    answer: str
    mode: ResponseMode
    zone: AnalysisZone
    doctrines_triggered: List[str]
    confidence: ConfidenceLevel
    reasoning_chain: List[str]
    authorities: List[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float
    cache_hit_rate: float

# =========================================================
# DOCTRINE CACHE - 28 BLOCKS
# =========================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="pH_control_treatment_systems",
        keywords=["ph", "acid", "base", "neutralization", "carbonate", "hydroxide", "buffer"],
        conclusion_template="pH control is critical for {purpose}. Target pH range is {range} based on {factors}. Adjustment strategy involves {method} with monitoring at {frequency}.",
        reasoning_framework="""
        pH fundamentally affects every aspect of water chemistry:

        1. CORROSION CONTROL: Low pH (<6.5) increases metal dissolution. Aggressive water attacks
           pipes, tanks, equipment. Langelier Saturation Index (LSI) must be positive for
           scale-forming water (protective calcium carbonate layer) or near-zero for neutral water.

        2. SCALE FORMATION: High pH (>8.5) promotes calcium carbonate precipitation. In boilers,
           scale reduces heat transfer efficiency. In injection water, scale plugs formation.
           Optimal pH balances corrosion protection vs scale risk.

        3. DISINFECTION EFFICIENCY: Chlorine speciation is pH-dependent. At pH <7.5, hypochlorous
           acid (HOCl) dominates—50-100x more effective than hypochlorite ion (OCl-). Free chlorine
           disinfection requires pH 6.5-7.5 for maximum kill rate.

        4. COAGULATION OPTIMIZATION: Alum works best at pH 5.5-7.0 (aluminum hydroxide precipitation).
           Ferric chloride optimal at pH 4.0-6.5. Charge neutralization and sweep floc formation
           are pH-sensitive. Jar testing determines optimal pH for turbidity removal.

        5. PRECIPITATION REACTIONS: Metal hydroxide solubility is pH-dependent (amphoteric behavior
           for Al, Zn). Softening via lime addition (pH >10.5) precipitates Mg(OH)2 and CaCO3.

        6. REGULATORY: Safe Drinking Water Act requires pH 6.5-8.5 for distribution. NPDES permits
           often specify pH 6.0-9.0 for discharge. Produced water injection may need pH 6.0-7.5.

        7. ADJUSTMENT METHODS:
           - Acid feed: Sulfuric acid (cheaper), hydrochloric acid (no sulfate), CO2 (soft acid)
           - Base feed: Sodium hydroxide (caustic), lime (also adds hardness), soda ash (Na2CO3)
           - Buffer systems: Carbonate/bicarbonate for stability

        8. MONITORING: Continuous pH probes for critical systems. Calibration with pH 4/7/10 buffers.
           Automatic dosing with feedback control for ±0.1 pH unit accuracy.
        """,
        key_factors=[
            "Target pH range for specific application (corrosion, disinfection, coagulation)",
            "Existing alkalinity/buffering capacity (resistance to pH change)",
            "Chemical feed equipment and dosing accuracy",
            "Temperature effects on pH electrode calibration and dissociation constants",
            "Downstream impacts (distribution system corrosion, biological growth)",
            "Regulatory constraints (SDWA, NPDES permit limits)",
            "Cost of acid/base chemicals vs operational benefits"
        ],
        primary_authority=[
            "EPA Lead and Copper Rule (pH optimization for corrosion control)",
            "AWWA M48 Waterborne Pathogens Manual (pH for disinfection)",
            "NACE SP0169 Control of External Corrosion (pH in injection water)",
            "Stumm & Morgan Aquatic Chemistry (pH equilibrium fundamentals)",
            "ASTM D1293 pH measurement in water"
        ],
        burden_holder="System designer/operator",
        adversary_position="pH adjustment is unnecessary cost; natural pH is acceptable",
        counter_arguments=[
            "Corrosion costs (pipe replacement, metal leaching) far exceed chemical costs",
            "Disinfection failure at suboptimal pH risks public health (SDWA violation)",
            "Scale formation reduces system capacity and increases energy consumption",
            "Regulatory compliance is non-negotiable (NPDES permit violations = fines)",
            "Jar testing proves coagulation efficiency gain justifies pH adjustment"
        ],
        resolution_strategy="Calculate Langelier/Ryznar indices; run jar tests; model disinfection CT requirements; compare chemical cost vs avoided corrosion/scale damage over 20-year lifecycle.",
        entity_scope="Municipal water systems, industrial cooling water, produced water treatment, boiler feedwater",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="pH measurement and control are well-established; uncertainty in long-term corrosion rates and site-specific water chemistry variations",
        controlling_precedent="EPA Lead and Copper Rule treatment technique for optimal corrosion control",
        category=IssueCategory.WATER_QUALITY
    ),

    DoctrineBlock(
        topic="langelier_saturation_index_lsi",
        keywords=["lsi", "langelier", "saturation", "corrosion", "scale", "calcium carbonate", "stability"],
        conclusion_template="LSI = {value} indicates {interpretation}. Water is {tendency} with respect to CaCO3. Recommended action: {action}.",
        reasoning_framework="""
        Langelier Saturation Index quantifies calcium carbonate saturation:

        LSI = pH - pHs
        where pHs = (pK2 - pKs) + pCa + pAlk

        1. CALCULATION INPUTS:
           - pH (measured)
           - Calcium hardness (mg/L as CaCO3)
           - Total alkalinity (mg/L as CaCO3)
           - Total Dissolved Solids (mg/L)
           - Temperature (°C)

        2. INTERPRETATION:
           LSI > 0: Supersaturated—water will precipitate CaCO3 (scale-forming)
           LSI = 0: Saturated—equilibrium, no tendency to dissolve or precipitate
           LSI < 0: Undersaturated—water will dissolve CaCO3 (corrosive)

        3. TARGET RANGES:
           Drinking water distribution: LSI = 0 to +0.5 (slight scale forms protective film)
           Cooling towers: LSI = +1.5 to +2.5 (controlled scaling acceptable)
           Boiler feedwater: LSI near 0 (minimize scale on heat transfer surfaces)
           Injection water: LSI = -0.5 to 0 (avoid formation plugging)

        4. LIMITATIONS:
           - Assumes pure CaCO3 system (ignores other minerals)
           - Does not predict corrosion rate (only tendency)
           - Requires accurate alkalinity and hardness measurements
           - Temperature-sensitive (recalculate for different T)

        5. COMPLEMENTARY INDICES:
           Ryznar Stability Index (RSI) = 2(pHs) - pH
             RSI < 6: Scale-forming | RSI 6-7: Stable | RSI > 7: Corrosive
           Puckorius Scaling Index (PSI): Accounts for buffering capacity

        6. ADJUSTMENT STRATEGIES:
           Corrosive water (LSI < 0):
             - Increase pH with caustic/lime
             - Increase alkalinity with soda ash
             - Blending with harder water
             - Corrosion inhibitors (polyphosphates, silicates)
           Scale-forming water (LSI > 2):
             - Lower pH with acid feed
             - Antiscalants (phosphonates, polymers)
             - Softening to remove Ca/Mg

        7. FIELD APPLICATION:
           Use portable meters or lab analysis. Recalculate LSI after any treatment change.
           Monitor at multiple points (source, post-treatment, distribution extremities).
           Seasonal variation in temperature affects LSI—adjust treatment seasonally.
        """,
        key_factors=[
            "pH, calcium hardness, alkalinity, TDS, temperature (all inputs required)",
            "LSI value and trend over time",
            "Target range for specific application (protective film vs scale avoidance)",
            "System materials (concrete vs steel vs plastic—susceptibility varies)",
            "Historical corrosion/scale problems in the system",
            "Regulatory requirements (SDWA corrosion control)",
            "Cost of chemical treatment vs asset replacement"
        ],
        primary_authority=[
            "AWWA C652 Standard for Disinfection of Water Storage Facilities",
            "NACE SP0169 (LSI for injection water quality)",
            "Langelier, W.F. 1936 original paper on saturation index",
            "ASTM D3739 LSI calculation standard",
            "EPA Optimal Corrosion Control Treatment Evaluation Technical Recommendations"
        ],
        burden_holder="Water system owner/operator",
        adversary_position="LSI is academic; real-world corrosion depends on many factors beyond CaCO3",
        counter_arguments=[
            "LSI is foundational—EPA requires it for corrosion control evaluation",
            "Proven correlation between negative LSI and lead/copper exceedances",
            "Complementary indices (RSI, PSI) refine but confirm LSI predictions",
            "Field observations (red water, pinhole leaks) align with LSI < -1",
            "Cost-benefit: LSI adjustment via pH/alkalinity control is low-cost insurance"
        ],
        resolution_strategy="Calculate LSI monthly with lab-verified inputs; correlate with system corrosion indicators (metal sampling, pipe coupon weight loss); adjust treatment to achieve target LSI; document in NPDES/SDWA compliance reports.",
        entity_scope="Potable water systems, cooling water, injection water, any system with CaCO3 potential",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="LSI calculation is deterministic; interpretation requires judgment on acceptable range for specific system",
        controlling_precedent="EPA guidance on corrosion control (LSI optimization is standard practice)",
        category=IssueCategory.SCALE_CORROSION
    ),

    DoctrineBlock(
        topic="coagulation_flocculation_jar_testing",
        keywords=["coagulation", "flocculation", "jar test", "alum", "ferric", "turbidity", "colloid", "zeta potential"],
        conclusion_template="Optimal coagulant is {chemical} at {dose} mg/L and pH {ph}. Expected turbidity reduction from {initial} to <{target} NTU. Flocculation time {minutes} min at {g_value} sec^-1.",
        reasoning_framework="""
        Coagulation/flocculation removes suspended particles and colloidal matter:

        1. COLLOIDAL STABILITY:
           Particles <1 micron carry negative surface charge (zeta potential -10 to -40 mV).
           Electrostatic repulsion prevents agglomeration. Stable suspension = high turbidity.

        2. COAGULATION MECHANISMS:
           a) Charge neutralization: Cationic coagulants (Al3+, Fe3+) adsorb to negative colloids,
              reducing zeta potential to near-zero. Destabilization allows particle contact.
           b) Sweep floc: Excess coagulant forms metal hydroxide precipitate (Al(OH)3, Fe(OH)3)
              that enmeshes particles as it settles. Higher dose, less pH-sensitive.
           c) Bridging: Polymers with charged sites attach to multiple particles, linking them.

        3. COAGULANTS:
           - Aluminum sulfate (alum): Al2(SO4)3·14H2O. Optimal pH 5.5-7.0. Dose 10-100 mg/L.
             Generates Al(OH)3 floc. Lowers pH (requires alkalinity for buffering).
           - Ferric chloride: FeCl3. Optimal pH 4.0-6.5. Effective over wider pH range than alum.
             Produces denser floc, faster settling. More corrosive.
           - Polyaluminum chloride (PACl): Pre-hydrolyzed, wider pH range, lower sludge volume.
           - Cationic polymers: Charge neutralization at low dose. Used alone or as coagulant aid.

        4. JAR TEST PROTOCOL:
           - Fill six 1-liter beakers with raw water (record pH, temp, turbidity, alkalinity)
           - Dose coagulant in series (e.g., 0, 10, 20, 30, 40, 50 mg/L)
           - Rapid mix: 100-150 rpm for 1-3 min (G = 700-1000 sec^-1)
           - Slow mix: 20-40 rpm for 15-20 min (G = 20-80 sec^-1)
           - Settle: 30-60 min quiescent
           - Measure supernatant turbidity, pH
           - Optimal dose: Minimum turbidity with acceptable pH and floc characteristics

        5. FLOCCULATION DESIGN:
           G-value (velocity gradient) = sqrt(P/(μ·V))
             P = power input (W), μ = dynamic viscosity (Pa·s), V = volume (m^3)
           Gt (Camp number) = 20,000 to 200,000 (product of G and detention time)
           Tapered flocculation: High G initially (70-90 sec^-1), then lower (20-30 sec^-1)
             to build floc without shear breakup.

        6. TURBIDITY TARGETS:
           Surface water treatment: <0.3 NTU (SWTR)
           Pre-RO: <1.0 NTU (protect membranes)
           Produced water: <10 NTU (injection water spec)

        7. pH ADJUSTMENT:
           If alkalinity <50 mg/L as CaCO3, may need to add lime/soda ash to buffer pH drop
           from alum. Ferric sulfate generates more acidity than ferric chloride.

        8. SLUDGE HANDLING:
           Coagulation produces 2-5% solids sludge. Volume depends on raw water turbidity and
           coagulant dose. Dewatering (belt press, centrifuge) or thickening required before disposal.
        """,
        key_factors=[
            "Raw water quality (turbidity, pH, alkalinity, temperature, organic content)",
            "Coagulant type and optimal dose from jar tests",
            "pH range for effective coagulation (may need acid/base addition)",
            "Flocculation kinetics (G-value, detention time, tapered mixing)",
            "Settling characteristics (sludge volume, floc strength)",
            "Regulatory turbidity limit (<0.3 NTU for filtered water under SWTR)",
            "Chemical cost and sludge disposal cost"
        ],
        primary_authority=[
            "EPA Surface Water Treatment Rule (SWTR) turbidity requirements",
            "AWWA B403 Aluminum Sulfate standard",
            "AWWA M37 Operational Control of Coagulation and Filtration Processes",
            "Camp, T.R. 1955 flocculation theory",
            "ASTM D2035 jar test procedure"
        ],
        burden_holder="Treatment plant operator",
        adversary_position="Coagulation is unnecessary; sedimentation alone will clarify water",
        counter_arguments=[
            "Colloidal particles (<1 micron) will NOT settle in reasonable time without coagulation",
            "SWTR mandates <0.3 NTU—impossible to achieve without coagulation+filtration",
            "Jar tests empirically demonstrate 95%+ turbidity removal with optimal coagulant dose",
            "Failure to coagulate risks filter clogging, short runs, high backwash water loss",
            "Regulatory violations result in fines and potential boil-water orders"
        ],
        resolution_strategy="Run jar tests with multiple coagulants at various doses and pH; select lowest-cost option meeting <0.3 NTU; design flocculation basin for Gt = 50,000-100,000; pilot test at full scale if feasible.",
        entity_scope="Surface water treatment plants, produced water clarification, industrial wastewater",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Jar test results are reproducible; scale-up to full plant requires pilot testing for hydraulic validation",
        controlling_precedent="EPA SWTR turbidity requirement drives coagulation/flocculation necessity",
        category=IssueCategory.TREATMENT_DESIGN
    ),

    DoctrineBlock(
        topic="chlorination_disinfection_ct_values",
        keywords=["chlorine", "disinfection", "ct value", "free chlorine", "hypochlorous acid", "giardia", "cryptosporidium", "contact time"],
        conclusion_template="Required CT for {pathogen} inactivation ({log_reduction}-log) at pH {ph} and {temp}°C is {ct_value} mg-min/L. Chlorine residual {residual} mg/L with contact time {time} min achieves compliance.",
        reasoning_framework="""
        Chlorine disinfection efficacy is quantified by CT (concentration × time):

        1. CHLORINE CHEMISTRY:
           Chlorine gas (Cl2), sodium hypochlorite (NaOCl), or calcium hypochlorite (Ca(OCl)2)
           dissolve in water to form hypochlorous acid (HOCl) and hypochlorite ion (OCl-):

           Cl2 + H2O ↔ HOCl + H+ + Cl-
           HOCl ↔ H+ + OCl-  (pKa = 7.5)

           At pH 6: ~96% HOCl, 4% OCl-
           At pH 7.5: ~50% HOCl, 50% OCl-
           At pH 9: ~3% HOCl, 97% OCl-

           HOCl is 50-100x more effective disinfectant than OCl-. pH control critical.

        2. CT CONCEPT:
           CT = C × T
           C = disinfectant residual concentration (mg/L) at end of contact time
           T = contact time (minutes) in baffled contact basin (T10 = time for 10% of flow to pass)

           Required CT increases with:
           - Higher target log inactivation (3-log = 99.9%, 4-log = 99.99%)
           - Lower temperature (cold water requires higher CT)
           - Higher pH (more OCl-, less HOCl)

        3. PATHOGEN SUSCEPTIBILITY:
           Bacteria (E. coli): Low CT (0.02-0.05 mg-min/L for 99.99%)
           Viruses (Hepatitis A): Medium CT (3-12 mg-min/L for 99.99%)
           Giardia cysts: High CT (50-150 mg-min/L for 99.9%)
           Cryptosporidium oocysts: VERY high CT (7,200+ mg-min/L for 99.9%—chlorine ineffective)

        4. SWTR REQUIREMENTS:
           Surface water must achieve:
           - 3-log (99.9%) Giardia inactivation
           - 4-log (99.99%) virus inactivation

           Alternatively, combination of filtration (physical removal) + disinfection credits.

        5. CT TABLE LOOKUP (EPA SWTR Guidance):
           Example: 2-log Giardia inactivation at pH 7.0, 10°C:
           Required CT = 73 mg-min/L

           If free chlorine residual = 0.5 mg/L, required T10 = 73/0.5 = 146 min

        6. CONTACT BASIN DESIGN:
           Baffled or serpentine configuration to approach plug flow (T10/T ≥ 0.7)
           T10 measured via tracer study (lithium, fluoride)
           Volume = Q × T10 (flow rate × contact time)

        7. RESIDUAL MAINTENANCE:
           Distribution system: 0.2-2.0 mg/L free chlorine to suppress regrowth
           SDWA requires detectable residual entering distribution
           Total trihalomethanes (THMs) byproduct limit: 80 μg/L (Stage 2 DBP Rule)

        8. CHLORINE DEMAND:
           Oxidation of organics, Fe/Mn, H2S consumes chlorine before disinfection.
           Breakpoint chlorination: Add enough Cl2 to oxidize all reduced species + NH3,
           then free chlorine residual appears. Dose = demand + residual.
        """,
        key_factors=[
            "Target pathogen and required log reduction (SWTR mandates)",
            "pH and temperature (affect CT requirement via HOCl/OCl- ratio)",
            "Free chlorine residual at end of contact time (measured, not dosed)",
            "Contact basin T10 (tracer test to validate hydraulic efficiency)",
            "Chlorine demand (raw water quality, organics, reduced metals)",
            "DBP formation potential (THMs, HAAs—limit chlorine dose)",
            "Cryptosporidium presence (requires UV or ozone, not chlorine alone)"
        ],
        primary_authority=[
            "EPA Surface Water Treatment Rule (CT tables for Giardia/viruses)",
            "EPA Disinfection Profiling and Benchmarking Guidance",
            "AWWA M20 Water Chlorination Principles and Practices",
            "40 CFR 141.72 Disinfection requirements",
            "White's Handbook of Chlorination (industry standard reference)"
        ],
        burden_holder="Water utility",
        adversary_position="Chlorine residual alone ensures disinfection; CT calculation is theoretical",
        counter_arguments=[
            "EPA SWTR explicitly requires CT compliance, not just residual maintenance",
            "Outbreaks (Milwaukee 1993—Cryptosporidium) prove inadequate disinfection kills people",
            "Tracer studies demonstrate many basins have T10 < 0.5T (short-circuiting = inadequate CT)",
            "pH 8.5 water with 0.5 mg/L Cl2 may fail CT for Giardia despite detectable residual",
            "SDWA compliance = federal law; violations trigger consent decrees and fines"
        ],
        resolution_strategy="Conduct tracer study to measure T10; sample for free chlorine at basin outlet; calculate achieved CT using EPA tables; adjust dose or detention time to meet 3-log Giardia + 4-log virus; document in monthly operating reports.",
        entity_scope="Public water systems treating surface water or groundwater under influence of surface water",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="CT tables are EPA-mandated; uncertainty in actual T10 (tracer test required for validation)",
        controlling_precedent="40 CFR 141.72 disinfection CT requirements under SWTR",
        category=IssueCategory.DISINFECTION
    ),

    DoctrineBlock(
        topic="membrane_filtration_microfiltration_ultrafiltration",
        keywords=["membrane", "microfiltration", "ultrafiltration", "mf", "uf", "pore size", "tff", "flux", "backwash"],
        conclusion_template="Recommended membrane process is {type} with pore size {pore_size} microns for removal of {target}. Expected flux {flux} gfd. Backwash frequency every {interval} based on TMP rise to {tmp_limit} psi.",
        reasoning_framework="""
        Membrane filtration provides physical barrier for particle/pathogen removal:

        1. MEMBRANE CLASSIFICATION BY PORE SIZE:
           Microfiltration (MF): 0.1-10 μm pores
             - Removes bacteria, cysts (Giardia 8-12 μm, Crypto 4-6 μm), suspended solids
             - Does NOT remove viruses (0.02-0.3 μm) or dissolved organics
             - Typical flux: 50-150 gfd (gallons per sq ft per day)

           Ultrafiltration (UF): 0.01-0.1 μm (10-100 nm) pores
             - Removes viruses, colloids, macromolecules (proteins, polysaccharides)
             - Does NOT remove dissolved salts or small organics
             - Typical flux: 30-80 gfd

           Nanofiltration (NF): 0.001-0.01 μm (1-10 nm)
             - Removes divalent ions (Ca2+, Mg2+, SO4 2-), organics >200 MW
             - Partial salt rejection (50-90%)
             - Typical flux: 10-30 gfd

           Reverse Osmosis (RO): <0.001 μm (<1 nm)
             - Removes all ions, organics, essentially produces distilled water
             - >95% salt rejection
             - Typical flux: 5-20 gfd, requires 150-400 psi pressure

        2. FILTRATION MODES:
           Dead-end: Feed perpendicular to membrane, all water passes through (cake builds up)
           Cross-flow (tangential flow): Feed parallel to membrane, creates shear to limit fouling

           MF/UF typically use inside-out (feed inside hollow fibers, permeate exits outside)
           or outside-in configuration. RO uses cross-flow spiral-wound or hollow fiber.

        3. TRANSMEMBRANE PRESSURE (TMP):
           TMP = (Pfeed + Pretentate)/2 - Ppermeate

           As membrane fouls (pore blockage, cake layer), TMP rises for constant flux.
           Or flux declines at constant TMP. Set alarm limits for backwash trigger.

        4. FOULING MECHANISMS:
           Pore blockage: Particles plug pores (irreversible unless chemically cleaned)
           Cake formation: Particles accumulate on surface (reversible via backwash)
           Concentration polarization: Rejected species accumulate near membrane (reduce flux)
           Biofouling: Microbial growth on membrane (requires disinfection)
           Scaling: Mineral precipitation (Ca/Mg/Ba salts—requires antiscalant)

        5. BACKWASH/CLEANING:
           Hydraulic backwash: Reverse flow with permeate to dislodge cake (every 30-60 min)
           Air scour: Bubbles create turbulence for mechanical cleaning
           Chemical cleaning: NaOCl (biofouling), citric acid (scaling), NaOH (organics)
           Frequency: Daily chemical clean, weekly CIP (clean-in-place) with stronger chemicals

        6. REGULATORY CREDITS:
           EPA LT2ESWTR: UF membranes with integrity testing earn 4-log virus removal credit
           MF earns 2-log Crypto credit (but not virus removal unless demonstrated)
           Continuous turbidity monitoring <0.15 NTU required for credit
           Integrity testing: Pressure decay, bubble point, or particle challenge

        7. PRETREATMENT:
           Coagulation ahead of MF/UF improves flux, reduces fouling (charge neutralization)
           Cartridge filters (5-10 μm) protect membranes from large debris
           Antiscalant (phosphonates) prevents scaling in NF/RO

        8. APPLICATION EXAMPLES:
           Produced water: UF for oil/solids removal before RO desalting
           Drinking water: UF for pathogen removal (replace conventional filtration)
           Boiler feedwater: RO for high-purity makeup water
           Wastewater reuse: MBR (membrane bioreactor) combines biotreatment + MF/UF
        """,
        key_factors=[
            "Target contaminant size and removal requirement (bacteria, virus, TDS)",
            "Membrane pore size and material (PVDF, PES, cellulose acetate)",
            "Feed water quality (turbidity, organics, hardness—fouling potential)",
            "Flux rate and recovery (% of feed that becomes permeate)",
            "TMP and energy consumption (RO requires high pressure = high cost)",
            "Backwash/cleaning frequency and chemical cost",
            "Regulatory credits (LT2ESWTR log removal for Crypto, Giardia, virus)",
            "Capital cost ($/gpm) and membrane replacement interval (3-7 years)"
        ],
        primary_authority=[
            "EPA LT2ESWTR membrane filtration guidance (log removal credits)",
            "AWWA M53 Microfiltration and Ultrafiltration Membranes",
            "NSF/ANSI 61 drinking water system components (membrane certification)",
            "Membrane Filtration Guidance Manual (EPA 2005)",
            "ASTM D6908 integrity testing for MF/UF membranes"
        ],
        burden_holder="Water system owner",
        adversary_position="Conventional filtration is cheaper; membranes are unproven and high-maintenance",
        counter_arguments=[
            "LT2ESWTR for Crypto compliance drives utilities to membranes (alternative is UV)",
            "Membrane footprint is 1/10th of conventional plant (land cost savings)",
            "Automated operation reduces labor vs sand filter backwash and media replacement",
            "Consistent <0.1 NTU permeate quality (conventional varies 0.1-0.5 NTU)",
            "Life-cycle cost analysis (20-year NPV) often favors membranes for small-medium plants"
        ],
        resolution_strategy="Pilot test UF and MF with site water for 6-12 months; measure flux decline, cleaning frequency, permeate quality; calculate LCOE ($/1000 gal); compare to conventional treatment capital + O&M; select based on NPV and regulatory certainty.",
        entity_scope="Municipal drinking water, industrial process water, produced water treatment, wastewater reuse",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Technology is mature; site-specific fouling behavior requires pilot testing for accurate cost projection",
        controlling_precedent="EPA LT2ESWTR membrane filtration criteria for Cryptosporidium compliance",
        category=IssueCategory.TREATMENT_DESIGN
    ),

    DoctrineBlock(
        topic="produced_water_oil_removal_daf",
        keywords=["produced water", "oil water separator", "daf", "dissolved air flotation", "tph", "walnut shell filter", "api separator"],
        conclusion_template="Oil removal strategy for {flow_rate} bpd: {primary_unit} followed by {polishing_unit}. Expected effluent oil {concentration} mg/L TPH. Meets {regulatory_standard} for {disposal_method}.",
        reasoning_framework="""
        Produced water from oil/gas operations contains oil, grease, suspended solids:

        1. PRODUCED WATER CHARACTERISTICS:
           Oil content: 50-5,000 mg/L (varies by formation, well age, production method)
           Forms: Free oil (droplets >150 μm), dispersed oil (20-150 μm), dissolved oil (<20 μm)
           Solids: Sand, clay, scale particles, corrosion products (10-2,000 mg/L TSS)
           Salinity: Often high TDS (10,000-200,000 mg/L—seawater to brine)

        2. DISPOSAL/REUSE OPTIONS:
           Injection (waterflooding or disposal): Requires <10-30 mg/L oil, <5-10 mg/L TSS
           Discharge (offshore NPDES): 29 mg/L monthly average oil/grease (40 CFR 435)
           Beneficial reuse: Irrigation, livestock, dust control (varies by state)

        3. API SEPARATOR (PRIMARY TREATMENT):
           Gravity settling for free oil (Stokes' Law: large droplets rise fast)
           Sized for 3-5 min retention at design flow rate
           Removes ~60-80% of oil (mostly >150 μm droplets)
           Skimmed oil sent to slop tank for recovery
           Limitations: Does NOT remove dispersed or dissolved oil

        4. INDUCED GAS FLOTATION (IGF):
           Induces gas bubbles (natural gas) via venturi or sparger
           Bubbles attach to oil droplets, float to surface for skimming
           Removes 80-95% of dispersed oil (down to 20 μm)
           Simple, low maintenance, common in offshore platforms

        5. DISSOLVED AIR FLOTATION (DAF):
           Pressurize recycle stream to 60-90 psi, saturate with air
           Release through nozzles into tank—microbubbles (10-100 μm) form
           Bubbles attach to oil/solids, float to surface as froth
           Removes 95-99% of oil + TSS (can achieve <10 mg/L effluent)
           Chemical coagulants enhance oil droplet aggregation

           Advantages over IGF: Better for small droplets, cleaner effluent
           Disadvantages: Higher capital cost, more complex, requires air compressor

        6. WALNUT SHELL FILTER (POLISHING):
           Granular media (crushed walnut shells) adsorbs residual oil
           Operates like sand filter but oil sticks to shell surface
           Removes 90-95% of remaining oil (polish to <5 mg/L)
           Backwash with high-velocity water to strip oil, send to API separator
           Filter run time: 12-48 hours before backwash (depends on influent oil load)

        7. CERAMIC MEMBRANE (ADVANCED):
           UF/MF ceramic membranes with chemical resistance (pH 0-14)
           Achieve <2 mg/L oil, <2 mg/L TSS (injection water quality)
           High capital cost but produces reusable water (zero discharge)

        8. DESIGN SEQUENCE:
           High oil (>200 mg/L): API separator → IGF/DAF → walnut shell → injection
           Medium oil (50-200 mg/L): DAF → walnut shell → injection
           Low oil (<50 mg/L): Walnut shell or cartridge filter → injection

        9. REGULATORY:
           EPA offshore discharge: 29 mg/L oil monthly average (42 mg/L daily max)
           Onshore injection: State regulations (e.g., Texas RRC, NDIC)—often <30 mg/L oil
           Beneficial reuse: Case-by-case permitting (NPDES or state non-discharge)
        """,
        key_factors=[
            "Produced water volume (bpd) and oil concentration (mg/L TPH)",
            "Target effluent quality (injection spec, discharge limit, reuse standard)",
            "Oil droplet size distribution (free vs dispersed vs dissolved)",
            "Solids content and type (sand, clay, scale—affects filter loading)",
            "Space constraints (offshore platform vs onshore facility)",
            "Capital budget and O&M cost (chemicals, backwash water, energy)",
            "Disposal method (injection, discharge, reuse—drives treatment stringency)"
        ],
        primary_authority=[
            "40 CFR 435 Offshore Effluent Limitations (oil/grease 29 mg/L)",
            "API RP 45 Recommended Practice for Oil Mist Eliminators",
            "EPA Development Document for Offshore Oil/Gas Extraction (1993)",
            "State injection regulations (TX RRC Rule 46, ND Admin Code 43-02-03)",
            "ASTM D3921 oil/grease measurement (hexane extractable material)"
        ],
        burden_holder="Operator (oil/gas producer)",
        adversary_position="Single API separator is sufficient; additional treatment is unnecessary expense",
        counter_arguments=[
            "API separator alone achieves 50-100 mg/L—exceeds injection spec and discharge limit",
            "Formation plugging from high oil/solids costs millions in well workovers and lost injection",
            "NPDES violations result in $37,500/day fines plus citizen lawsuits",
            "DAF + walnut shell reliably achieves <10 mg/L for <$0.50/bbl operational cost",
            "Peer operators with same formation require polishing—industry standard"
        ],
        resolution_strategy="Pilot test DAF and walnut shell with actual produced water; measure effluent oil/TSS over 30-day trial; compare to injection well injectivity (step-rate test before/after); calculate ROI from avoided workover costs vs treatment CAPEX/OPEX.",
        entity_scope="Onshore and offshore oil/gas produced water treatment for injection, discharge, or reuse",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Treatment performance is well-documented; site-specific oil chemistry and emulsion stability may require pilot testing",
        controlling_precedent="40 CFR 435 Subpart A offshore discharge limits; state injection rules for oil/TSS",
        category=IssueCategory.PRODUCED_WATER
    ),

    DoctrineBlock(
        topic="ion_exchange_water_softening",
        keywords=["ion exchange", "softening", "resin", "hardness", "calcium", "magnesium", "regeneration", "brine"],
        conclusion_template="Ion exchange softening will reduce hardness from {initial} to <{target} mg/L as CaCO3. Resin capacity {capacity} kgr/ft^3, regeneration every {volume} gallons with {salt_dose} lb NaCl per ft^3 resin.",
        reasoning_framework="""
        Ion exchange removes hardness (Ca2+, Mg2+) by exchanging for Na+:

        1. HARDNESS CLASSIFICATION:
           Soft: <60 mg/L as CaCO3
           Moderately hard: 60-120 mg/L
           Hard: 120-180 mg/L
           Very hard: >180 mg/L

           Problems from hardness:
           - Scale in pipes, boilers, heat exchangers (CaCO3, Mg(OH)2, CaSO4)
           - Soap scum (Ca/Mg react with soap to form precipitate)
           - Reduced efficiency (boiler scale = fuel waste, heat exchanger fouling)

        2. ION EXCHANGE CHEMISTRY:
           Strong acid cation (SAC) resin with sulfonic acid groups (-SO3-)
           Resin in sodium form: Resin-Na+

           Service cycle (softening):
           Ca2+ + 2(Resin-Na+) → (Resin)2-Ca + 2Na+
           Mg2+ + 2(Resin-Na+) → (Resin)2-Mg + 2Na+

           Hardness ions (Ca/Mg) are captured; sodium is released.
           Effluent is soft but higher in sodium (2.3 mg Na per 1 mg/L hardness removed).

        3. RESIN CAPACITY:
           Typical SAC resin: 25-35 kilograins (kgr) per cubic foot at 15 lb/ft^3 salt regeneration
           1 grain = 17.1 mg as CaCO3

           Example: 30 kgr/ft^3 resin, 200 mg/L hardness feedwater
           Volume treated per cycle = (30,000 gr/ft^3) / (200 mg/L / 17.1) = 2,565 gallons per ft^3

        4. REGENERATION:
           Exhaust cycle: Resin saturated with Ca/Mg, hardness breakthrough detected (>1 mg/L)
           Backwash: Upflow water to fluidize bed, remove fines and trapped solids (10-15 min)
           Brine injection: 10% NaCl solution displaces Ca/Mg, converts resin back to Na+ form

           (Resin)2-Ca + 2NaCl → 2(Resin-Na+) + CaCl2

           Salt dose: 6-15 lb NaCl per ft^3 resin (higher dose = higher capacity but more waste)
           Contact time: 30-60 min slow brine flow
           Rinse: Fast flow to remove residual brine and displaced Ca/Mg (20-30 min)

        5. SYSTEM CONFIGURATION:
           Simplex: Single tank, no soft water during regeneration (batch systems)
           Duplex: Two tanks alternating, continuous soft water supply
           Triplex: Three tanks, one always in service, one regenerating, one standby

           Flow rate: 2-10 gpm per ft^2 bed area (avoid channeling or excessive pressure drop)
           Bed depth: 24-36 inches for adequate contact time
           Freeboard: 50-80% (bed expands during backwash)

        6. ALTERNATIVE: LIME SOFTENING (CHEMICAL PRECIPITATION):
           Add lime (Ca(OH)2) to raise pH >10.5
           Mg(HCO3)2 + 2Ca(OH)2 → 2CaCO3 ↓ + Mg(OH)2 ↓ + 2H2O
           Ca(HCO3)2 + Ca(OH)2 → 2CaCO3 ↓ + 2H2O

           Advantages: Treats high-hardness water (>300 mg/L), no brine disposal
           Disadvantages: Sludge handling, pH adjustment, incomplete Mg removal unless very high pH

        7. SODIUM CONCERNS:
           Softening increases sodium: Each mg/L hardness removed adds 0.46 mg/L Na
           500 mg/L hardness → 230 mg/L Na increase
           SDWA does not regulate Na, but health advisory is 20 mg/L for sodium-restricted diets
           Option: Bypass blending (mix soft + hard water to achieve target hardness + lower Na)

        8. RESIN FOULING:
           Iron fouling: Fe2+ oxidizes to Fe3+, precipitates on resin (brown color, capacity loss)
             Prevention: Pre-oxidation + filtration, or chelating resin
           Organic fouling: Tannins, humic acids coat resin (reduces capacity)
             Prevention: Activated carbon or anion resin pre-treatment
           Bacterial growth: Biofilm on resin (odor, pressure drop)
             Treatment: Sanitize with NaOCl (100-200 ppm, 4-hour contact)
        """,
        key_factors=[
            "Feed water hardness and target hardness (boiler <1 mg/L, general <50 mg/L)",
            "Flow rate and peaking factor (size for max demand, not average)",
            "Resin volume and bed configuration (simplex vs duplex for continuous supply)",
            "Regeneration frequency and salt consumption (lb/kgr hardness removed)",
            "Brine disposal method (sanitary sewer, evaporation pond, deep well injection)",
            "Sodium loading in treated water (health advisory, taste concerns)",
            "Iron and organic content in feed (fouling potential, pre-treatment needed)"
        ],
        primary_authority=[
            "AWWA B300 Cation Exchange Resin standard",
            "NSF/ANSI 44 Residential Cation Exchange Water Softeners",
            "WQA S-100 Softener performance standard",
            "ASTM D6161 Ion exchange resin capacity",
            "Nalco Water Handbook (industry reference for IX design)"
        ],
        burden_holder="Water user (industrial, municipal, or residential)",
        adversary_position="Hardness is natural and harmless; softening is cosmetic and wastes salt",
        counter_arguments=[
            "Scale buildup in boilers reduces thermal efficiency by 20-40% (fuel cost increase)",
            "Heat exchanger fouling increases pressure drop and maintenance frequency",
            "Soap consumption doubles in hard water (detergent cost savings justify softening)",
            "Boiler tube failure from scale = unplanned shutdown and lost production",
            "Many industrial processes require <10 mg/L hardness (textiles, food/beverage, electronics)"
        ],
        resolution_strategy="Calculate scale formation potential (LSI, RSI); estimate cost of scale (energy loss, maintenance, equipment replacement); compare to softening CAPEX + salt + disposal cost over 10-year period; demonstrate ROI <2 years for industrial applications.",
        entity_scope="Boiler feedwater, cooling water makeup, industrial process water, residential water treatment",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="IX softening technology is mature with predictable performance; site-specific resin capacity and regeneration efficiency confirmed via pilot test",
        controlling_precedent="ASME Boiler and Pressure Vessel Code (water quality specifications drive softening need)",
        category=IssueCategory.TREATMENT_DESIGN
    ),

    DoctrineBlock(
        topic="npdes_permit_discharge_limits",
        keywords=["npdes", "discharge", "permit", "effluent", "bod", "tss", "ph", "clean water act", "wqbel"],
        conclusion_template="NPDES permit {permit_number} requires {parameter} ≤ {limit_monthly} mg/L monthly average, {limit_daily} mg/L daily maximum. Monitoring frequency {frequency}. Compliance strategy: {approach}.",
        reasoning_framework="""
        National Pollutant Discharge Elimination System (NPDES) regulates wastewater discharge:

        1. CLEAN WATER ACT AUTHORITY:
           Section 402: Prohibits discharge of pollutants without NPDES permit
           EPA or authorized state issues permits (Texas TCEQ, California SWRCB, etc.)
           Violators subject to $37,500-$50,000 per day civil penalties + criminal liability

        2. PERMIT LIMITS TYPES:
           Technology-Based Effluent Limits (TBEL): Based on treatment technology available
             - Secondary treatment: BOD5 30 mg/L monthly, 45 daily; TSS 30/45
             - Advanced treatment: Nutrient removal (N, P), lower BOD/TSS

           Water Quality-Based Effluent Limits (WQBEL): Based on receiving stream standards
             - If TBEL not protective enough, WQBEL are more stringent
             - Calculated from stream flow (7Q10 = lowest 7-day flow in 10 years), mixing zone,
               and water quality criteria (e.g., dissolved oxygen >5 mg/L, ammonia <1 mg/L)

        3. COMMON PARAMETERS:
           BOD5 (Biochemical Oxygen Demand): Organic matter (municipal 30/45, industrial varies)
           TSS (Total Suspended Solids): Particulates (30/45 for secondary treatment)
           pH: 6.0-9.0 standard units (instant min/max, not average)
           Ammonia (NH3-N): Toxic to fish (varies 0.5-10 mg/L depending on pH, temp, species)
           Total Nitrogen (TN): Eutrophication concern (3-10 mg/L in sensitive waters)
           Total Phosphorus (TP): Eutrophication (0.1-1.0 mg/L in sensitive waters)
           Fecal Coliform: Pathogen indicator (200/100 mL geometric mean)
           Oil & Grease: Industrial discharge (often 10-30 mg/L)
           Metals: Copper, lead, zinc, chromium (varies by hardness-based criteria)

        4. AVERAGING PERIODS:
           Daily Maximum: Highest single-day result (grab or 24-hour composite)
           Weekly Average: Mean of all samples in a week
           Monthly Average: Mean of all samples in a month (typically 4-8 samples)
           Quarterly or Annual: Long-term trend limits

           Compliance assessed independently for each averaging period.
           One daily exceedance = violation even if monthly average is compliant.

        5. MONITORING REQUIREMENTS:
           Frequency: Daily, weekly, monthly, or quarterly (risk-based—higher pollutant = more frequent)
           Sample type: Grab (instant) or composite (24-hour flow-proportional)
           Methods: EPA-approved (40 CFR Part 136—Standard Methods, ASTM)
           DMR (Discharge Monitoring Report): Monthly submittal to EPA/state via NetDMR

        6. COMPLIANCE STRATEGIES:
           Treatment upgrade: Add clarifier, upgrade aeration, install membrane bioreactor
           Operational optimization: Adjust aeration DO, SRT, chemical dose
           Blending/equalization: Dilute high-strength waste with low-strength
           Pretreatment: Require industrial users to treat before discharge to sewer
           Flow reduction: Water conservation, reuse to stay below design capacity

        7. RECEIVING STREAM PROTECTION:
           Mixing zone: Designated area where dilution with stream flow occurs
           Acute toxicity: Protect from immediate fish kills (1-hour average)
           Chronic toxicity: Protect from long-term reproductive/growth impacts (4-day average)
           Biomonitoring: Whole effluent toxicity (WET) testing with fathead minnows or Ceriodaphnia

        8. INDUSTRIAL CATEGORICAL PRETREATMENT:
           40 CFR Part 403: National Pretreatment Program
           Industries discharging to POTW must meet categorical standards (e.g., metal finishing,
           petroleum refining) to prevent pass-through or interference with municipal treatment.

        9. STORMWATER NPDES:
           Construction (>1 acre disturbed): SWPPP, erosion control, turbidity monitoring
           Industrial (SIC codes with outdoor material handling): Sampling for metals, oil, TSS
           MS4 (Municipal Separate Storm Sewer System): Non-structural BMPs, public education
        """,
        key_factors=[
            "Permit limits for each parameter (monthly avg, daily max, instantaneous min/max)",
            "Current treatment performance and margin of safety",
            "Monitoring frequency and analytical method detection limits",
            "Receiving stream classification and designated uses (aquatic life, drinking water, recreation)",
            "Variability in influent load (seasonal, industrial batch discharges)",
            "Treatment capacity headroom (design flow vs permitted flow vs actual flow)",
            "Cost of treatment upgrade vs penalty risk (expected violation frequency × $37,500/day)"
        ],
        primary_authority=[
            "40 CFR 122 NPDES Permit Program",
            "40 CFR 136 Analytical Methods",
            "Clean Water Act Section 402",
            "EPA NPDES Permit Writers' Manual (2010)",
            "State water quality standards (e.g., Texas Surface Water Quality Standards 30 TAC 307)"
        ],
        burden_holder="Discharger (permittee)",
        adversary_position="Permit limits are overly conservative; dilution in stream provides adequate protection",
        counter_arguments=[
            "WQBEL calculations use 7Q10 low flow—worst-case scenario for aquatic life protection",
            "Historical fish kills and impaired waters listings prove inadequate treatment harms ecosystems",
            "CWA is strict liability—no intent required for violations, penalties are mandatory",
            "Citizen suits under CWA allow public to enforce (no EPA discretion to overlook violations)",
            "Permit limits are technology-feasible—secondary treatment achieves 30/45 BOD/TSS reliably"
        ],
        resolution_strategy="Review 3-year DMR history for exceedances; identify root causes (hydraulic overload, upset, influent spike); pilot test treatment upgrades (MBBR, MBR, nutrient removal); calculate capital + 20-year O&M cost; compare to projected violation penalties + consent decree costs; present business case for proactive compliance.",
        entity_scope="Municipal wastewater treatment plants, industrial direct dischargers, stormwater dischargers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Permit limits are legally binding; treatment performance prediction requires pilot testing and operational optimization",
        controlling_precedent="Clean Water Act strict liability for NPDES violations",
        category=IssueCategory.REGULATORY
    ),

    DoctrineBlock(
        topic="safe_drinking_water_act_mcl_compliance",
        keywords=["sdwa", "mcl", "mclg", "primary standard", "coliform", "lead", "arsenic", "nitrate", "dbp"],
        conclusion_template="Primary MCL for {contaminant} is {mcl_value} {units}. Current level {current_value}. Compliance status: {status}. Recommended action: {action} to achieve <{target_value} with safety factor.",
        reasoning_framework="""
        Safe Drinking Water Act establishes Maximum Contaminant Levels (MCLs) for public water:

        1. SDWA FRAMEWORK:
           MCL: Enforceable standard, highest level allowed in drinking water
           MCLG: Health goal, level at which no adverse health effects expected (non-enforceable)
           Action Level (AL): Trigger for corrosion control treatment (lead/copper)
           Treatment Technique (TT): Required process when MCL not feasible (Giardia, Crypto)

        2. MAJOR CONTAMINANT CATEGORIES:
           Microbiological: Total coliform, E. coli, Giardia, Cryptosporidium, viruses
           Inorganics: Lead, copper, arsenic, nitrate, fluoride, mercury, chromium
           Organics: VOCs (benzene, TCE), SOCs (pesticides, PCBs)
           Disinfectants: Chlorine, chloramine, chlorine dioxide
           Disinfection Byproducts: THMs, HAAs
           Radionuclides: Radium, uranium, radon, gross alpha

        3. SELECTED MCLs (CRITICAL):
           Total Coliform: <5% positive samples/month (systems collecting ≥40 samples)
           E. coli: Zero tolerance (any positive = violation, public notice required)
           Lead: Action Level 0.015 mg/L (15 ppb) at consumer tap (90th percentile)
           Copper: Action Level 1.3 mg/L at consumer tap (90th percentile)
           Arsenic: 0.010 mg/L (10 ppb)—lowered from 50 ppb in 2006
           Nitrate: 10 mg/L (as N)—methemoglobinemia (blue baby syndrome) concern
           TTHMs: 0.080 mg/L (80 ppb) running annual average
           HAA5: 0.060 mg/L (60 ppb) running annual average
           Uranium: 30 μg/L (radiological and chemical toxicity)

        4. LEAD AND COPPER RULE (LCR):
           Sample at high-risk taps (lead service lines, copper with lead solder, homes built 1982-1988)
           90th percentile: Sort results, value at 90th position is compared to AL
           If >10% samples exceed AL: Trigger corrosion control treatment, public education, LSL replacement

           Corrosion control: Adjust pH, alkalinity (achieve LSI near 0), add phosphate inhibitor
           LSL replacement: Replace lead service lines within 3 years (LCRR accelerates timeline)

        5. DISINFECTION BYPRODUCT RULE (STAGE 2 DBP):
           TTHMs and HAA5 form when chlorine reacts with organics (humic/fulvic acids)
           Cancer risk (chloroform, bromodichloromethane)

           Compliance: Running annual average at each monitoring location <80 ppb TTHM, <60 ppb HAA5
           Reduction strategies:
           - Remove precursors: Enhanced coagulation, activated carbon, membrane filtration
           - Alternative disinfectants: Chloramines (lower DBP but higher nitrification risk), UV, ozone
           - Minimize contact time: Move chlorination point closer to distribution

        6. ARSENIC RULE:
           MCL lowered to 10 ppb in 2006 (was 50 ppb)
           Natural occurrence in groundwater (volcanic rock, geothermal areas, agricultural runoff)
           Chronic exposure: Skin, bladder, lung cancer; cardiovascular disease

           Treatment: Coagulation/filtration (ferric chloride), adsorptive media (iron oxide, activated alumina),
           ion exchange, membrane (RO, NF)

        7. NITRATE RULE:
           MCL 10 mg/L (as N) = 45 mg/L (as NO3)
           Source: Agricultural fertilizer, septic systems, animal feedlots
           Health: Methemoglobinemia in infants <6 months (hemoglobin cannot carry oxygen)

           Treatment: Ion exchange (selective nitrate resin), RO, biological denitrification

        8. PUBLIC NOTIFICATION:
           Tier 1 (acute): 24-hour notice (E. coli, nitrate >10 mg/L)—radio, TV, social media
           Tier 2 (chronic): 30-day notice (MCL exceedance)—mail, newspaper
           Tier 3 (monitoring): Annual CCR (Consumer Confidence Report)

        9. ENFORCEMENT:
           EPA or primacy state issues compliance order, administrative penalties ($16,000/day)
           Persistent violations: Consent decree, system takeover by state
           Criminal penalties for willful violations (knowingly falsifying data)
        """,
        key_factors=[
            "Contaminant concentration and frequency of detection (MCL, MCLG, AL comparison)",
            "Source of contamination (natural, agricultural, industrial, distribution system)",
            "Population served and sensitive subgroups (infants, immune-compromised)",
            "Treatment feasibility and cost (small systems may get variance or exemption)",
            "Monitoring schedule and sample location (compliance vs non-compliance points)",
            "Public notification tier and timeline (acute vs chronic health risk)",
            "Enforcement history and consent decree status"
        ],
        primary_authority=[
            "40 CFR 141 National Primary Drinking Water Regulations",
            "40 CFR 142 State Primacy Requirements",
            "Safe Drinking Water Act Section 1412 (MCL setting process)",
            "EPA Drinking Water Standards and Health Advisories (2018)",
            "AWWA M58 Internal Corrosion Control in Water Distribution Systems"
        ],
        burden_holder="Public Water System (PWS)",
        adversary_position="MCLs are overly conservative; low-level exceedances pose minimal risk",
        counter_arguments=[
            "MCLG is set at level with NO adverse effects; MCL is compromise with treatment feasibility",
            "Sensitive populations (infants, pregnant, elderly) are at higher risk than healthy adults",
            "Lead has NO safe level (MCLG = 0)—neurotoxic effects at any detectable concentration",
            "SDWA violations trigger mandatory public notification—loss of public trust and property values",
            "Long-term exposure to arsenic/nitrate increases cancer/disease risk—epidemiological evidence"
        ],
        resolution_strategy="Review 3-year MCL compliance data; identify exceedances and seasonal trends; pilot test treatment options (IX, membrane, oxidation); calculate capital + 20-year NPV; apply for state loan/grant funding; implement treatment and monitor for 12 months to confirm <MCL; update CCR and public notification.",
        entity_scope="Community water systems, non-transient non-community systems (schools, factories)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="MCLs are federal law with strict liability; treatment effectiveness varies by site-specific water quality",
        controlling_precedent="40 CFR 141 enforceable MCLs under SDWA",
        category=IssueCategory.REGULATORY
    ),

    DoctrineBlock(
        topic="reverse_osmosis_desalination_design",
        keywords=["reverse osmosis", "ro", "desalination", "membrane", "salt rejection", "recovery", "flux", "pressure", "fouling"],
        conclusion_template="RO system design for {feedwater_tds} mg/L TDS: {stages} stages, {pressure} psi, {recovery}% recovery. Expected permeate TDS <{permeate_tds} mg/L. Pretreatment: {pretreatment}. Antiscalant: {chemical}.",
        reasoning_framework="""
        Reverse Osmosis (RO) removes dissolved salts by semi-permeable membrane:

        1. OSMOSIS vs REVERSE OSMOSIS:
           Osmosis: Water moves from low to high salt concentration across membrane
           Osmotic pressure (π) = iCRT (van't Hoff equation)
             i = ion dissociation factor, C = molar concentration, R = gas constant, T = temp

           Example: Seawater (35,000 mg/L TDS) has π ≈ 400 psi

           Reverse Osmosis: Apply pressure >π to force water through membrane, leaving salts behind
           Feed pressure: 150-400 psi (brackish), 800-1,200 psi (seawater)

        2. MEMBRANE MATERIALS:
           Thin-film composite (TFC): Polyamide active layer on polysulfone support
           - High salt rejection (96-99.5%), moderate flux (10-20 gfd)
           - Chlorine intolerant (must dechlorinate feed)

           Cellulose acetate (CA): Older technology, chlorine tolerant, lower rejection (90-96%)

           Configuration: Spiral-wound (most common), hollow fiber (compact but fouling-sensitive)

        3. KEY PERFORMANCE METRICS:
           Salt Rejection: (1 - Cp/Cf) × 100%
             Cp = permeate concentration, Cf = feed concentration
             Example: 5,000 mg/L feed, 50 mg/L permeate → 99% rejection

           Recovery: (Permeate flow / Feed flow) × 100%
             Brackish water: 75-85% recovery
             Seawater: 35-50% recovery (limited by scaling and osmotic pressure)

           Flux: Permeate flow per membrane area (gfd or L/m²/hr)
             Typical: 10-20 gfd (brackish), 5-12 gfd (seawater)

           Specific Energy Consumption (SEC): kWh per m³ permeate
             Brackish: 0.5-2.5 kWh/m³
             Seawater: 2.5-6.0 kWh/m³ (energy recovery devices reduce by 30-40%)

        4. PRETREATMENT (CRITICAL):
           RO membranes are sensitive to fouling and scaling:

           Particulate fouling: Requires <SDI 5 (Silt Density Index)
             Treatment: Multimedia filter, cartridge filter (5 μm), UF/MF

           Scaling: CaCO3, CaSO4, BaSO4, SiO2 precipitate as recovery increases (concentrate supersaturates)
             Treatment: Antiscalants (phosphonates, polycarboxylates), acid dosing (lower pH to prevent CaCO3)

           Biofouling: Bacterial growth on membrane surface
             Treatment: Chlorination (then dechlorination for TFC membranes), UV, biocides

           Oxidant damage: Chlorine degrades polyamide membranes
             Treatment: Bisulfite (sodium metabisulfite) dechlorination, activated carbon

        5. STAGING AND ARRAY:
           Single-stage: All membranes in parallel (low recovery, simple)
           Two-stage: Concentrate from 1st stage feeds 2nd stage (higher recovery, common for brackish)
           Tapered array: More vessels in 1st stage than 2nd (balance flow and flux)

           Interstage boost pump: Compensate for pressure drop in 1st stage

        6. CONCENTRATE DISPOSAL:
           Brackish inland: Deep well injection, evaporation pond, land application (if salinity permits)
           Seawater coastal: Ocean outfall with diffuser (dilution to meet WQS)
           Zero Liquid Discharge (ZLD): Evaporator + crystallizer (expensive, used for high-value water recovery)

        7. ENERGY RECOVERY:
           Seawater RO concentrate at 50% recovery exits at ~1,100 psi (still pressurized)
           Energy recovery devices (ERD):
           - Pelton wheel turbine: Generates electricity from concentrate (60-70% recovery)
           - Pressure exchanger (PX): Isobaric transfer of pressure from concentrate to feed (90-96% recovery)

           Modern SWRO with ERD: 2.5-3.5 kWh/m³ (vs 5-6 without ERD)

        8. POST-TREATMENT:
           RO permeate is aggressive (low TDS, low alkalinity, negative LSI)
           Stabilization:
           - Increase pH: Caustic or lime
           - Increase alkalinity: CO2 or lime
           - Remineralize: Blend with bypass water, add calcite contactor
           - Disinfection: Chlorination (no dechlorination needed—no more membranes)

        9. APPLICATIONS:
           Brackish groundwater: Reduce TDS from 2,000-10,000 to <500 mg/L (drinking water)
           Seawater: Reduce 35,000 mg/L to <500 mg/L (coastal municipal supply)
           Boiler feedwater: Achieve <10 mg/L TDS for high-pressure boilers
           Produced water reuse: Desalt for reuse in hydraulic fracturing or beneficial use
        """,
        key_factors=[
            "Feed water TDS and composition (Ca, Mg, Ba, SiO2—scaling potential)",
            "Target permeate quality (drinking water <500 mg/L, boiler <10 mg/L)",
            "Recovery target (75-85% brackish, 35-50% seawater—balance yield vs scaling)",
            "Pretreatment requirements (SDI, turbidity, chlorine, hardness)",
            "Energy cost ($/kWh) and ERD selection (justifies capital for seawater)",
            "Concentrate disposal method (regulatory approval, cost)",
            "Membrane replacement interval (3-7 years, 20-40% of OPEX)"
        ],
        primary_authority=[
            "AWWA M46 Reverse Osmosis and Nanofiltration Manual",
            "ASTM D4516 Standard Practice for Standardizing RO Performance Data",
            "Filmtec/DOW RO Membrane Design Software (WAVE, ROSA)",
            "EPA Drinking Water Treatment Technology Comparison (RO vs IX vs distillation)",
            "Desalination and Water Purification Roadmap (USBR 2003)"
        ],
        burden_holder="Water provider or industrial user",
        adversary_position="RO is too expensive; alternative sources or treatment are cheaper",
        counter_arguments=[
            "For high-TDS brackish water (>2,000 mg/L), RO is lowest-cost desalination (vs distillation, IX)",
            "Coastal cities with no freshwater alternative MUST use seawater RO (e.g., San Diego, Perth)",
            "Energy costs declined 80% since 1980s (ERD + efficient pumps + membrane improvements)",
            "Life-cycle cost (20-year NPV) for RO beats long-distance water imports",
            "Zero-discharge regulations drive industrial RO+ZLD despite high cost (regulatory compliance)"
        ],
        resolution_strategy="Conduct feed water analysis (full suite + scaling indices); use membrane vendor software (ROSA, WAVE) to design stages, recovery, pressure; pilot test for 6-12 months to validate fouling rates and CIP frequency; calculate LCOE including pretreatment, energy, membrane replacement, concentrate disposal; compare to alternative water sources.",
        entity_scope="Municipal drinking water, industrial process water, produced water reuse, seawater desalination",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="RO design software is validated; site-specific fouling and scaling behavior requires pilot testing for accurate cost estimation",
        controlling_precedent="EPA drinking water standards (TDS <500 mg/L recommended, not enforceable)",
        category=IssueCategory.TREATMENT_DESIGN
    ),

    DoctrineBlock(
        topic="uv_disinfection_cryptosporidium",
        keywords=["uv", "ultraviolet", "disinfection", "cryptosporidium", "crypto", "dose", "log inactivation", "lt2eswtr"],
        conclusion_template="UV dose of {dose} mJ/cm^2 achieves {log_reduction}-log Cryptosporidium inactivation per LT2ESWTR. Required lamp output {lamps} × {watts} W. UVT {uvt}%. Flow {flow} MGD at {intensity} mW/cm^2.",
        reasoning_framework="""
        UV disinfection inactivates pathogens via DNA/RNA damage without chemicals:

        1. UV MECHANISM:
           UV-C wavelength (254 nm) absorbed by nucleic acids (DNA/RNA)
           Thymine dimers form, preventing replication → pathogen cannot infect
           No chemical residual (unlike chlorine)—no taste/odor, no DBP formation

        2. UV DOSE (FLUENCE):
           Dose (mJ/cm²) = Intensity (mW/cm²) × Time (seconds)
           Delivered dose depends on:
           - Lamp power and geometry
           - UV Transmittance (UVT) of water (absorption by organics, iron, turbidity)
           - Flow rate and hydraulic residence time
           - Lamp aging (output declines over 8,000-12,000 hours)

        3. LT2ESWTR UV REQUIREMENTS:
           EPA Long Term 2 Enhanced Surface Water Treatment Rule (2006):
           Cryptosporidium removal/inactivation required based on bin classification:

           Bin 1 (<0.075 oocysts/L): No additional treatment
           Bin 2 (0.075-1.0): 1-log additional
           Bin 3 (1.0-3.0): 2-log additional
           Bin 4 (>3.0): 2.5-log additional

           UV inactivation credits:
           - 1-log: 5 mJ/cm² validated dose
           - 2-log: 8 mJ/cm²
           - 3-log: 12 mJ/cm²
           - 4-log: 18 mJ/cm² (assuming low-pressure high-output lamps)

           Validation: Dose must be VALIDATED per UV Disinfection Guidance Manual (UVDGM)
           Bioassay with MS2 or T7 bacteriophage to confirm delivered dose

        4. UV REACTOR TYPES:
           Low-Pressure (LP): Monochromatic 254 nm, high electrical efficiency (35-40%)
             Lamps: 15-150 W each, long life (12,000 hr)

           Low-Pressure High-Output (LPHO): Higher power per lamp (200-1,000 W)
             More intense UV, smaller reactor footprint

           Medium-Pressure (MP): Polychromatic (200-300 nm), broader spectrum
             High power per lamp (5-30 kW), faster inactivation kinetics for Crypto
             Lower efficiency (10-15%), higher operating cost, shorter lamp life (4,000-8,000 hr)

        5. UVT (UV TRANSMITTANCE):
           Percentage of 254 nm light transmitted through 1 cm water path
           UVT = 10^(-absorbance) × 100%

           High-quality water: UVT >95% (low organics, no iron, <0.1 NTU)
           Poor quality: UVT <75% (high organics, iron >0.3 mg/L, turbidity >1 NTU)

           Low UVT requires higher lamp power or lower flow rate to deliver same dose.
           Pretreatment (coagulation/filtration, GAC) to improve UVT is cost-effective.

        6. REACTOR DESIGN:
           Lamp orientation: Perpendicular to flow (maximize exposure time)
           Baffling: Prevent short-circuiting (ensure every particle sees target dose)
           CFD modeling: Validate dose distribution (identify dead zones)

           Online monitoring:
           - UV intensity sensor (mW/cm²)
           - UVT sensor (detect fouling or water quality change)
           - Flow meter (calculate dose = intensity × time)
           - Alarm if delivered dose <setpoint → divert flow or shut down

        7. LAMP MAINTENANCE:
           Fouling: Mineral scale, biofilm, iron deposits on quartz sleeves reduce intensity
             Cleaning: Mechanical wiper (continuous or periodic), chemical (citric acid)

           Lamp aging: UV output declines 10-20% over lifetime
             Replacement: At 8,000-12,000 hours or when intensity <80% of rated

           Ballast: Electronic ballast more efficient than magnetic, dims with age

        8. COMPARISON TO CHLORINE:
           UV Advantages:
           - Effective against Cryptosporidium (chlorine requires 7,200 mg-min/L—impractical)
           - No DBP formation (THMs, HAAs)
           - No chemical handling or residual
           - Fast inactivation (seconds vs minutes contact time)

           UV Disadvantages:
           - No residual (requires secondary disinfection in distribution with chlorine/chloramine)
           - UVT-dependent (high organics or iron = high cost)
           - Requires continuous power (no disinfection if power fails)
           - Capital cost for large systems ($500K-$5M+ depending on flow)

        9. APPLICATIONS:
           Drinking water: LT2ESWTR Crypto compliance (post-filtration, pre-distribution)
           Wastewater: Tertiary disinfection for reuse (no chlorine residual toxicity to aquatic life)
           Produced water: Injection water bacteria control (no chemical addition)
           Aquaculture: Pathogen control without chlorine (toxic to fish)
        """,
        key_factors=[
            "Target pathogen and required log inactivation (Crypto 2-log = 8 mJ/cm²)",
            "Feed water UVT (>95% ideal, <80% requires pretreatment or higher lamp power)",
            "Flow rate and peaking factor (size reactor for max day + fire flow)",
            "Lamp type (LPHO vs MP—tradeoff between efficiency and footprint)",
            "Validation protocol (bioassay with challenge microorganism per UVDGM)",
            "Maintenance plan (lamp replacement, sleeve cleaning, intensity monitoring)",
            "Secondary disinfection (chlorine/chloramine residual for distribution)",
            "Power reliability (backup generator if UV is sole barrier)"
        ],
        primary_authority=[
            "EPA LT2ESWTR UV Disinfection Guidance Manual (UVDGM 2006)",
            "40 CFR 141.720 LT2ESWTR Cryptosporidium treatment requirements",
            "NWRI UV Guidelines (2012)",
            "NSF/ANSI 55 UV Microbiological Water Treatment Systems",
            "IUVA UV FAQs for Drinking Water (International UV Association)"
        ],
        burden_holder="Water system owner",
        adversary_position="UV is unproven and expensive; chlorine alone is sufficient",
        counter_arguments=[
            "Cryptosporidium is chlorine-resistant—CT >7,200 mg-min/L is impossible for distribution",
            "Milwaukee 1993 outbreak (400,000 ill, 104 deaths) from Crypto proves need for UV/ozone",
            "LT2ESWTR MANDATES Crypto treatment for Bin 2-4 systems—UV or ozone are only options",
            "UV capital cost ($1-2M for 5 MGD) is less than ozone and lower O&M than ozone",
            "No DBP formation vs chlorine (Stage 2 DBP Rule limits THMs/HAAs—UV avoids this)"
        ],
        resolution_strategy="Conduct Crypto monitoring per LT2ESWTR to determine bin; if Bin 2+, evaluate UV vs ozone via pilot test; measure UVT seasonally; design UV reactor for peak flow + validated dose; calculate NPV including lamp replacement, energy, and avoided DBP compliance costs; implement UV + chloramine for distribution residual.",
        entity_scope="Surface water and GWUDI systems under LT2ESWTR, wastewater reuse, industrial process water",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="UV dose-response for Crypto is validated via EPA UVDGM; site-specific UVT and hydraulic performance require on-site measurement",
        controlling_precedent="40 CFR 141.720 LT2ESWTR Cryptosporidium inactivation requirements",
        category=IssueCategory.DISINFECTION
    ),

    DoctrineBlock(
        topic="water_quality_parameters_monitoring",
        keywords=["ph", "turbidity", "tds", "tss", "bod", "cod", "do", "hardness", "alkalinity", "conductivity"],
        conclusion_template="Key parameters for {application}: {param1} target {value1}, {param2} target {value2}. Monitoring frequency {frequency}. Method: {method}. Compliance with {standard}.",
        reasoning_framework="""
        Water quality parameters characterize physical, chemical, and biological properties:

        1. PHYSICAL PARAMETERS:

           Turbidity (NTU—Nephelometric Turbidity Units):
           - Measure of suspended particles scattering light
           - Caused by clay, silt, algae, microorganisms
           - SWTR: <0.3 NTU filtered water, <1.0 NTU raw water for 95% of time
           - Method: Nephelometer (EPA 180.1)
           - High turbidity shelters pathogens from disinfection, interferes with UV

           Total Suspended Solids (TSS, mg/L):
           - Mass of particles retained on 0.45 μm filter
           - Method: Gravimetric (ASTM D5907, SM 2540 D)
           - NPDES secondary treatment: TSS 30 mg/L monthly, 45 daily max
           - Affects biofilm growth, sedimentation, filter loading

           Total Dissolved Solids (TDS, mg/L):
           - Mass of dissolved ions passing through 0.45 μm filter
           - Method: Gravimetric (evaporate filtrate, weigh residue) or conductivity correlation
           - Drinking water: <500 mg/L secondary standard (aesthetic—taste/hardness)
           - Irrigation: <450 mg/L (no restriction), 450-2,000 mg/L (slight to moderate restriction)
           - Boiler feedwater: <10 mg/L for high-pressure boilers

           Temperature (°C):
           - Affects density, viscosity, gas solubility (O2, CO2), reaction rates
           - Disinfection CT increases with lower temperature (cold water needs more CT)
           - NPDES thermal discharge limits (protect aquatic life from thermal shock)

           Conductivity (μS/cm):
           - Measure of water's ability to conduct electricity (proportional to TDS)
           - Conversion: TDS (mg/L) ≈ 0.5-0.7 × Conductivity (μS/cm)
           - Online monitoring easy, real-time indication of salinity changes

        2. CHEMICAL PARAMETERS (INORGANIC):

           pH (standard units):
           - Log scale of hydrogen ion concentration: pH = -log[H+]
           - Range 0-14 (acidic <7, neutral 7, basic >7)
           - Affects corrosion, scale, disinfection, coagulation, metal solubility
           - SDWA: 6.5-8.5, NPDES: 6.0-9.0 typically
           - Method: Electrode (EPA 150.1), field meter calibrated with pH 4/7/10 buffers

           Hardness (mg/L as CaCO3):
           - Total hardness = [Ca²⁺] + [Mg²⁺] expressed as CaCO3 equivalent
           - Causes: Calcium and magnesium from limestone, dolomite dissolution
           - Classification: Soft <60, Moderate 60-120, Hard 120-180, Very Hard >180 mg/L
           - Method: EDTA titration (SM 2340 C), ICP-MS
           - Problems: Scale in pipes/boilers, soap scum, aesthetic (taste, spotting)

           Alkalinity (mg/L as CaCO3):
           - Buffering capacity, ability to neutralize acid
           - Forms: HCO3⁻ (bicarbonate), CO3²⁻ (carbonate), OH⁻ (hydroxide)
           - Method: Titration to pH 4.5 endpoint (SM 2320 B)
           - Low alkalinity (<50 mg/L): pH unstable, corrosive water
           - High alkalinity (>200 mg/L): Scale-forming, high pH after chlorination

           Dissolved Oxygen (DO, mg/L):
           - Critical for aerobic aquatic life and aerobic treatment processes
           - Saturation: ~14 mg/L at 0°C, ~9 mg/L at 20°C, ~7 mg/L at 30°C (decreases with temp)
           - Water quality standard: >5 mg/L for cold-water fisheries, >4 mg/L warm-water
           - Method: Membrane electrode (EPA 360.1), Winkler titration (SM 4500-O C)
           - Wastewater aeration: Maintain 1.5-3.0 mg/L DO for activated sludge

           Chloride (Cl⁻, mg/L):
           - Indicator of salinity, road salt, wastewater infiltration
           - Corrosive to metals (stainless steel pitting, concrete rebar)
           - SDWA secondary: 250 mg/L (taste threshold)
           - Method: Ion chromatography (EPA 300.0), argentometric titration

           Sulfate (SO4²⁻, mg/L):
           - Natural from gypsum, industrial discharge, acid mine drainage
           - Laxative effect >500 mg/L (infant diarrhea)
           - Contributes to scaling (calcium sulfate, barium sulfate)
           - Method: Turbidimetric (EPA 375.4), ion chromatography

        3. CHEMICAL PARAMETERS (ORGANIC):

           Biochemical Oxygen Demand (BOD5, mg/L):
           - Oxygen consumed by bacteria degrading organic matter over 5 days at 20°C
           - Indicator of organic pollution (sewage, food processing, pulp/paper)
           - Method: Incubate sample 5 days, measure DO before/after (SM 5210 B)
           - NPDES secondary: BOD5 30 mg/L monthly, 45 daily max
           - Raw sewage: 200-400 mg/L, treated effluent: <10 mg/L

           Chemical Oxygen Demand (COD, mg/L):
           - Oxygen equivalent to oxidize all organic + reduced inorganics by dichromate
           - Faster than BOD (2-hour test vs 5 days)
           - COD > BOD always (includes non-biodegradable organics)
           - Method: Closed reflux colorimetric (SM 5220 D)
           - Industrial wastewater: COD used for process control, BOD for permit

           Total Organic Carbon (TOC, mg/L):
           - Carbon content of dissolved + particulate organics
           - DBP precursor (THM/HAA formation potential correlates with TOC)
           - Method: Combustion IR (SM 5310 B)
           - Surface water: 2-10 mg/L, groundwater: <1 mg/L
           - Stage 2 DBP Rule: Enhanced coagulation to reduce TOC 15-50% (depends on alk/TOC ratio)

           Oil & Grease (mg/L):
           - Hexane-extractable material (HEM)—includes petroleum, fats, waxes
           - Method: Liquid-liquid extraction, gravimetric (EPA 1664A)
           - NPDES offshore: 29 mg/L monthly, 42 daily
           - Produced water: <30 mg/L for injection, <10 mg/L for discharge in some states

        4. MICROBIOLOGICAL PARAMETERS:

           Total Coliform (MPN/100 mL or CFU/100 mL):
           - Indicator bacteria (E. coli, Klebsiella, Enterobacter)
           - Presence indicates potential fecal contamination or treatment failure
           - Method: Membrane filtration (SM 9222 B), multiple-tube fermentation (SM 9221)
           - SDWA: <5% positive samples/month (systems with ≥40 samples)

           E. coli (MPN/100 mL):
           - Fecal coliform, definitive indicator of recent fecal contamination
           - SDWA: Zero tolerance—any positive triggers repeat sampling + investigation
           - Method: Defined substrate (Colilert), membrane filtration with selective media

           Fecal Coliform (MPN/100 mL):
           - Subset of total coliform that grow at 44.5°C (thermotolerant)
           - NPDES recreational water: Geometric mean 200/100 mL
           - Replaced by E. coli in SDWA (E. coli more specific for fecal contamination)
        """,
        key_factors=[
            "Regulatory driver (SDWA, NPDES, state standards) and applicable limits",
            "Monitoring frequency (daily, weekly, monthly—based on parameter and system size)",
            "Sample location (raw, treated, distribution, effluent—compliance vs diagnostic)",
            "Analytical method and detection limit (EPA-approved, NELAC-certified lab)",
            "Quality control (field blanks, duplicates, spikes—validate data accuracy)",
            "Seasonal variability (temperature, runoff, algae blooms—adjust treatment)",
            "Trend analysis (early warning of treatment failure or source contamination)"
        ],
        primary_authority=[
            "Standard Methods for the Examination of Water and Wastewater (23rd Ed)",
            "40 CFR Part 136 EPA Analytical Methods",
            "SDWA regulations (40 CFR 141) for drinking water parameters",
            "NPDES regulations (40 CFR 122) for discharge parameters",
            "ASTM water testing standards (D-series)"
        ],
        burden_holder="Water/wastewater system operator",
        adversary_position="Continuous monitoring is expensive; grab samples are sufficient",
        counter_arguments=[
            "Grab samples miss transient upsets (slugs, spills)—online monitoring catches them",
            "SDWA requires continuous turbidity monitoring for filtration credit (not grab samples)",
            "NPDES 24-hour composite sampling (flow-weighted) is mandatory for BOD/TSS",
            "Process control (DO, pH, conductivity) requires real-time data for automated adjustments",
            "Liability: Undetected exceedance discovered later = evidence of inadequate monitoring"
        ],
        resolution_strategy="Review regulatory monitoring requirements (SDWA, NPDES permit); install online probes for critical parameters (pH, turbidity, DO, conductivity); calibrate and maintain per manufacturer protocol; collect composite samples for organics/nutrients per permit schedule; use certified lab (NELAC/ELAP); trend data in SCADA for early warning; document QA/QC in annual reports.",
        entity_scope="All water and wastewater systems (municipal, industrial, agricultural)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Analytical methods are standardized and validated; interpretation of trends and corrective actions requires operator expertise",
        controlling_precedent="40 CFR Part 136 defines approved analytical methods for regulatory compliance",
        category=IssueCategory.ANALYTICAL
    ),

    DoctrineBlock(
        topic="stiff_diagram_water_typing",
        keywords=["stiff diagram", "water type", "piper diagram", "cation", "anion", "hydrochemical facies", "geochemistry"],
        conclusion_template="Water type classified as {type} based on dominant ions {cations}/{anions}. Stiff diagram shows {pattern}. Implications for {application}: {interpretation}.",
        reasoning_framework="""
        Stiff diagrams and water typing classify water based on major ion composition:

        1. MAJOR IONS (meq/L basis for comparison):
           Cations: Ca²⁺, Mg²⁺, Na⁺, K⁺
           Anions: HCO3⁻, SO4²⁻, Cl⁻, CO3²⁻

           Convert mg/L to meq/L: meq/L = (mg/L) / (equivalent weight)
           Equivalent weight = atomic weight / valence

           Example:
           Ca²⁺: EW = 40/2 = 20, 100 mg/L Ca = 5 meq/L
           Cl⁻: EW = 35.5/1 = 35.5, 71 mg/L Cl = 2 meq/L

        2. STIFF DIAGRAM CONSTRUCTION:
           Horizontal bar chart with cations on left, anions on right:

           Left (cations):         Center   Right (anions):
           Na+ + K+         <---  |  --->   Cl-
           Ca2+             <---  |  --->   HCO3-
           Mg2+             <---  |  --->   SO4_2-

           Bar length proportional to meq/L
           Connect endpoints to form polygon shape

           Shape interpretation:
           - Narrow tall: Low TDS, bicarbonate-dominated (fresh groundwater)
           - Wide squat: High TDS, chloride/sulfate-dominated (saline water, produced water)
           - Asymmetric: Mixed water (blending, ion exchange processes)

        3. WATER TYPE CLASSIFICATION:
           Based on dominant cation and anion (>50% of total meq/L):

           Calcium-Bicarbonate (Ca-HCO3): Fresh groundwater, limestone/dolomite dissolution
           Sodium-Chloride (Na-Cl): Seawater, formation water, halite dissolution
           Calcium-Sulfate (Ca-SO4): Gypsum dissolution, acid mine drainage
           Sodium-Bicarbonate (Na-HCO3): Ion exchange (Ca-HCO3 water through Na-resin softener)
           Magnesium-Bicarbonate (Mg-HCO3): Dolomite-rich aquifers

           Mixed types: If no ion >50%, classify as Ca-Mg-HCO3 or Na-Ca-Cl, etc.

        4. PIPER DIAGRAM (TRILINEAR):
           Plots cation and anion composition on two ternary diagrams, projects to central diamond
           Identifies water type evolution:
           - Recharge water: Ca-Mg-HCO3 corner
           - Evolved groundwater: Moves toward Na-Cl corner (longer residence time)
           - Mixing: Linear trend between two end-members

        5. HYDROCHEMICAL FACIES:
           Facies: Distinct ion composition zones in aquifer or treatment process

           Example—Freshwater aquifer evolution:
           1. Recharge zone: Ca-HCO3 (recent rainfall, carbonate dissolution)
           2. Intermediate: Ca-Mg-HCO3 or Na-HCO3 (ion exchange on clays)
           3. Deep/old water: Na-Cl (long residence, halite dissolution, seawater intrusion)

        6. APPLICATIONS:

           Source identification:
           - Production well A: Ca-HCO3 (shallow fresh aquifer)
           - Production well B: Na-Cl (deep saline aquifer or seawater intrusion)
           - Stiff diagrams visually distinguish sources instantly

           Treatment design:
           - Ca-SO4 water: High scaling potential (gypsum), needs antiscalant
           - Na-Cl water: High TDS, requires RO for desalination
           - Ca-HCO3 water: Moderate hardness, lime softening or IX effective

           Produced water characterization:
           - High Na-Cl: Formation brine, high salinity (10,000-200,000 mg/L TDS)
           - Ca-Cl type: Deep formation water (oil/gas wells)
           - Compare to injection water (avoid incompatible mixing—scaling)

           Mixing analysis:
           - Blend two sources with different Stiff shapes → intermediate shape
           - Detect unauthorized discharge or cross-contamination

           Geothermal water:
           - High SiO2, Na-Cl, elevated temperature (>50°C)
           - Scaling potential from silica, carbonate (when cooled/depressurized)

        7. INTERPRETATION PITFALLS:
           - Temperature and pH affect equilibrium (recalculate speciation if conditions change)
           - Redox state: Fe²⁺ vs Fe³⁺, SO4²⁻ vs H2S (anaerobic vs aerobic)
           - Trace metals not shown (but critical for toxicity—As, Pb, Hg)
           - Alkalinity as HCO3 assumes pH <8.3 (if pH >10, CO3²⁻ dominates)
        """,
        key_factors=[
            "Major ion concentrations (Ca, Mg, Na, K, HCO3, SO4, Cl) in meq/L",
            "Dominant cation and anion (>50% of total meq/L defines type)",
            "TDS level (low <1,000, moderate 1,000-10,000, high >10,000 mg/L)",
            "Aquifer geology or water source (correlates with expected ion ratios)",
            "Treatment objectives (scaling, corrosion, desalination, blending)",
            "Regulatory limits (TDS, chloride, sulfate for discharge or beneficial use)",
            "Temporal trends (seasonal variation, contamination, aquifer depletion)"
        ],
        primary_authority=[
            "Hem, J.D. 1985 Study and Interpretation of Chemical Characteristics of Natural Water (USGS)",
            "ASTM D1126 Hardness in Water",
            "ASTM D512 Chloride in Water",
            "Freeze and Cherry Groundwater (1979)—hydrochemical facies",
            "Stiff, H.A. 1951 original paper on diagram method"
        ],
        burden_holder="Water manager, hydrogeologist, treatment designer",
        adversary_position="TDS alone is sufficient; ion composition detail is academic",
        counter_arguments=[
            "TDS doesn't reveal scaling risk—Ca-SO4 at 2,000 mg/L scales, Na-Cl at 5,000 doesn't",
            "Blending design requires ion balance—Ca-HCO3 + Na-Cl mixing may precipitate CaCO3",
            "Regulatory compliance for specific ions (Cl 250 mg/L, SO4 250 mg/L)—TDS misses this",
            "Corrosion (Cl/SO4 ratio affects pitting)—need composition, not just TDS",
            "Source fingerprinting: Stiff diagrams identify contamination source in minutes"
        ],
        resolution_strategy="Collect water samples from all sources and key process points; analyze full suite (Ca, Mg, Na, K, HCO3, SO4, Cl, TDS); convert to meq/L; construct Stiff diagrams; classify water type; overlay on Piper diagram to assess mixing or evolution; use for treatment design (softening, RO, blending) and regulatory reporting.",
        entity_scope="Groundwater resource management, drinking water treatment, produced water, industrial process water, geothermal",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Ion analysis is standard and accurate; interpretation of geochemical processes requires hydrogeologic expertise",
        controlling_precedent="Standard Methods for major ion analysis (EPA-approved for regulatory use)",
        category=IssueCategory.ANALYTICAL
    ),

    DoctrineBlock(
        topic="boiler_feedwater_quality_specs",
        keywords=["boiler", "feedwater", "tds", "hardness", "silica", "oxygen", "alkalinity", "asme", "deaeration"],
        conclusion_template="Boiler operating at {pressure} psi requires feedwater: TDS <{tds} mg/L, hardness <{hardness} mg/L, silica <{silica} mg/L, DO <{oxygen} ppb. Treatment: {process}.",
        reasoning_framework="""
        Boiler feedwater quality prevents scale, corrosion, carryover, and equipment failure:

        1. ASME BOILER WATER QUALITY GUIDELINES:
           ASME (American Society of Mechanical Engineers) Consensus for Industrial Boilers:

           Low-Pressure (<300 psi / 2 MPa):
           - TDS <3,500 mg/L (boiler water), <500 mg/L (feedwater preferred)
           - Total Hardness <0.3 mg/L as CaCO3 (feedwater)
           - Silica <150 mg/L (boiler water)
           - Alkalinity <700 mg/L (boiler water)

           Medium-Pressure (300-600 psi / 2-4 MPa):
           - TDS <2,500 mg/L (boiler), <100 mg/L (feedwater)
           - Hardness <0.1 mg/L
           - Silica <90 mg/L (boiler)

           High-Pressure (600-1,000 psi / 4-7 MPa):
           - TDS <1,000 mg/L (boiler), <10 mg/L (feedwater)
           - Hardness <0.05 mg/L (essentially zero)
           - Silica <20 mg/L (boiler)

           Very High-Pressure (>1,000 psi / >7 MPa):
           - TDS <200 mg/L (boiler), <1 mg/L (feedwater—demineralized)
           - Hardness <0.01 mg/L (zero tolerance)
           - Silica <5 mg/L
           - Dissolved oxygen <7 ppb (high-purity steam for turbines)

        2. SCALE FORMATION:
           Calcium carbonate (CaCO3): Forms above 200°F when hardness present
           - Thermal decomposition: Ca(HCO3)2 → CaCO3 ↓ + H2O + CO2
           - Hardness must be <0.3 mg/L for low-pressure, near-zero for high-pressure

           Calcium sulfate (CaSO4): Inverse solubility—less soluble at high temp
           - Gypsum scale in high-sulfate water
           - Limit SO4 and Ca to prevent precipitation

           Magnesium hydroxide (Mg(OH)2): Forms at pH >10.5, high alkalinity
           - Also known as magnesium silicate (serpentine) in high-SiO2 water

           Silica (SiO2): Polymerizes at high temp/pressure, forms hard glassy scale
           - Very difficult to remove (requires HF acid)
           - Limit <20 mg/L for high-pressure boilers

           Impact: Scale on heat transfer surfaces reduces efficiency (1/16 inch scale = 10% fuel loss),
           causes tube overheating and failure (catastrophic rupture risk).

        3. CORROSION:
           Dissolved Oxygen (DO): Pitting corrosion of steel
           - Fe + ½O2 + H2O → Fe(OH)2 (rust)
           - Target: <7 ppb DO for high-pressure boilers
           - Removal: Deaerator (physical—heat to 220-240°F, vent O2 and CO2)
                      + Oxygen scavenger (chemical—sodium sulfite, hydrazine, DEHA)

           Carbon Dioxide (CO2): Forms carbonic acid, lowers pH, corrodes condensate lines
           - CO2 + H2O → H2CO3 → H+ + HCO3-
           - Removed in deaerator (volatile, vented with steam)
           - Neutralization: Ammonia or neutralizing amines in condensate

           Low pH: Acidic water (<7) corrodes steel, leaches metals
           - Maintain boiler water pH 10.5-11.5 (alkaline with caustic or phosphate)
           - Feedwater pH 8.5-9.5 (ammonia or amines)

        4. CARRYOVER:
           Entrainment: Liquid droplets carried with steam (mechanical carryover)
           - Caused by high TDS, foaming, high water level, surging
           - Deposits in superheaters, turbine blades (reduces efficiency, causes imbalance)

           Vaporization: Volatile impurities (silica, sodium) evaporate with steam
           - Silica vaporization above 600 psi—redeposits in turbine as hard glassy scale
           - Limit boiler water silica <20 mg/L for turbine protection

        5. TREATMENT PROCESSES:

           Softening (for low-pressure):
           - Lime softening (chemical precipitation) or ion exchange (zeolite)
           - Reduces hardness to <0.3 mg/L
           - Still leaves TDS (sodium replaces calcium)

           Demineralization (for high-pressure):
           - Two-bed IX: Strong acid cation (SAC) removes all cations → H+
             + Strong base anion (SBA) removes all anions → OH-
             → H+ + OH- = H2O (pure)
           - Mixed-bed polishing: Cation + anion resin mixed, achieves <0.1 μS/cm conductivity
           - Produces <1 mg/L TDS, <0.01 mg/L hardness

           Reverse Osmosis (alternative):
           - 95-99% TDS removal, lower operating cost than IX for high-TDS feedwater
           - Still requires IX polishing for very high-purity (>1,000 psi) boilers

           Deaeration:
           - Spray-type or tray-type deaerator heats water to 220-240°F (5-10 psig)
           - Reduces DO to <20 ppb
           - Oxygen scavenger (sodium sulfite) reduces to <7 ppb: Na2SO3 + ½O2 → Na2SO4

        6. INTERNAL CHEMICAL TREATMENT:

           Phosphate programs: Precipitate hardness as hydroxyapatite (not scale-forming)
           - 3Ca²⁺ + 2PO4³⁻ → Ca3(PO4)2 ↓ (removed in blowdown)

           Chelants: EDTA sequesters hardness, prevents scale without sludge formation
           - For low-pressure boilers (<300 psi) only (chelants break down at high temp)

           Polymers: Dispersants keep particles suspended, prevent agglomeration
           - Combine with phosphate for sludge conditioning

           Alkalinity control: Caustic (NaOH) or soda ash (Na2CO3) maintain pH 10.5-11.5

        7. BLOWDOWN:
           Continuous or intermittent removal of boiler water to control TDS buildup
           Blowdown rate = Feedwater TDS / (Max boiler TDS - Feedwater TDS)

           Example: Feedwater 100 mg/L, max boiler 2,500 mg/L → Blowdown = 100/(2500-100) = 4.2%

           Heat recovery: Flash tank + heat exchanger recover energy from blowdown

        8. MONITORING:
           Feedwater: TDS, hardness, pH, DO (daily or continuous)
           Boiler water: TDS, pH, phosphate, silica, sulfite (daily)
           Condensate: Conductivity, pH, iron, copper (detect condenser leaks or corrosion)
        """,
        key_factors=[
            "Boiler operating pressure (determines TDS, hardness, silica limits per ASME)",
            "Makeup water quality (softened, demineralized, or RO—matches pressure requirement)",
            "Deaerator performance (DO reduction to <7 ppb for high-pressure)",
            "Internal treatment program (phosphate, chelant, or polymer—pressure-dependent)",
            "Blowdown rate and heat recovery (minimize water and energy loss)",
            "Monitoring frequency (daily for high-pressure, weekly for low-pressure)",
            "Consequences of failure (tube rupture = explosion risk, turbine damage = $millions)"
        ],
        primary_authority=[
            "ASME Consensus on Operating Practices for the Control of Feedwater and Boiler Water Chemistry",
            "ASTM D1426 Ammonia in Water",
            "ASTM D3370 Hardness in Boiler Water",
            "ABMA (American Boiler Manufacturers Association) guidelines",
            "Nalco/Ecolab Boiler Water Handbook (industry standard reference)"
        ],
        burden_holder="Boiler owner/operator",
        adversary_position="Softened water is sufficient for all boilers; demineralization is overkill",
        counter_arguments=[
            "ASME guidelines are engineering consensus—not opinion, based on 100+ years of failures",
            "High-pressure boilers (>600 psi) with softened water WILL scale and fail within months",
            "Tube failure = unplanned shutdown ($10K-100K/day lost production) + repair ($50K-500K)",
            "Turbine blade deposits from silica carryover = $1M+ turbine overhaul",
            "Insurance may deny claims if ASME water quality standards not followed"
        ],
        resolution_strategy="Determine boiler operating pressure and steam use (process vs turbine); select treatment to meet ASME limits (softening, RO, demin); design deaerator for <7 ppb DO; implement internal chemical program; monitor daily per ASME; calculate blowdown rate to control TDS; conduct annual tube inspection and water-side cleaning.",
        entity_scope="Industrial boilers (refineries, chemical plants, power generation), institutional (hospitals, universities)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ASME limits are industry standard; site-specific treatment performance validated via water analysis and boiler inspection",
        controlling_precedent="ASME Boiler and Pressure Vessel Code (water quality specifications)",
        category=IssueCategory.TREATMENT_DESIGN
    )
]

# =========================================================
# WATER CHEMISTRY INTELLIGENCE ENGINE
# =========================================================

class CHEM15Engine:
    """Water Chemistry Intelligence Engine - TIE-Grade"""

    def __init__(self):
        self.start_time = time.time()
        self.query_count = 0
        self.cache_hits = 0
        self.total_latency = 0.0

        self.doctrines = {d.topic: d for d in DOCTRINE_CACHE}
        self.metrics: Dict[str, Any] = defaultdict(int)
        self.audit_log: List[Dict[str, Any]] = []

        logger.info(f"{ENGINE_NAME} initialized | {len(self.doctrines)} doctrines loaded")

    def normalize_query(self, text: str) -> str:
        """Semantic normalization of water chemistry terms"""
        text = text.lower().strip()

        normalizations = {
            r'\bph\b': 'pH',
            r'\btds\b': 'total dissolved solids',
            r'\btss\b': 'total suspended solids',
            r'\bbod5?\b': 'biochemical oxygen demand',
            r'\bcod\b': 'chemical oxygen demand',
            r'\bdo\b': 'dissolved oxygen',
            r'\blsi\b': 'langelier saturation index',
            r'\brsi\b': 'ryznar stability index',
            r'\bct\b': 'concentration time',
            r'\bmcl\b': 'maximum contaminant level',
            r'\bnpdes\b': 'national pollutant discharge elimination system',
            r'\bsdwa\b': 'safe drinking water act',
            r'\buv\b': 'ultraviolet',
            r'\bro\b': 'reverse osmosis',
            r'\bix\b': 'ion exchange',
            r'\bmf\b': 'microfiltration',
            r'\buf\b': 'ultrafiltration',
            r'\bnf\b': 'nanofiltration',
            r'\bdaf\b': 'dissolved air flotation',
            r'\bapi\b': 'american petroleum institute',
            r'\bwqbel\b': 'water quality based effluent limit',
            r'\btbel\b': 'technology based effluent limit',
            r'\bswtr\b': 'surface water treatment rule',
            r'\blt2eswtr\b': 'long term 2 enhanced surface water treatment rule',
            r'\basme\b': 'american society of mechanical engineers',
            r'\bppb\b': 'parts per billion',
            r'\bppm\b': 'parts per million',
            r'\bntu\b': 'nephelometric turbidity units',
            r'\bgfd\b': 'gallons per square foot per day',
            r'\btmp\b': 'transmembrane pressure'
        }

        for pattern, replacement in normalizations.items():
            text = text.replace(pattern, replacement)

        return text

    def search_doctrines(self, query: str) -> List[DoctrineBlock]:
        """Keyword and semantic search across doctrine cache"""
        query_normalized = self.normalize_query(query)
        query_terms = set(query_normalized.split())

        scored_doctrines = []
        for doctrine in DOCTRINE_CACHE:
            score = 0.0

            # Keyword matching
            keywords_lower = [k.lower() for k in doctrine.keywords]
            for term in query_terms:
                if any(term in kw for kw in keywords_lower):
                    score += 10.0

            # Topic matching
            if any(term in doctrine.topic.lower() for term in query_terms):
                score += 15.0

            # Category matching
            if doctrine.category.value.lower() in query_normalized:
                score += 8.0

            # Reasoning framework search (substring)
            reasoning_lower = doctrine.reasoning_framework.lower()
            matches = sum(1 for term in query_terms if len(term) > 3 and term in reasoning_lower)
            score += matches * 2.0

            if score > 0:
                scored_doctrines.append((score, doctrine))

        scored_doctrines.sort(reverse=True, key=lambda x: x[0])
        return [d for _, d in scored_doctrines[:5]]

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Tuple[str, List[str], List[str], ConfidenceLevel]:
        """
        TIE-20 Component: Three-layer response architecture
        Layer 1: Doctrine cache (0-200ms)
        Layer 2: Semantic retrieval (fallback)
        Layer 3: Deep analysis (complex queries)
        """

        # Layer 1: Doctrine Cache
        triggered_doctrines = self.search_doctrines(query)

        if triggered_doctrines:
            self.cache_hits += 1
            reasoning_chain = [f"Doctrine cache hit: {d.topic}" for d in triggered_doctrines]
            answer = self.synthesize_answer(query, triggered_doctrines, mode, zone)
            authorities = list(set([auth for d in triggered_doctrines for auth in d.primary_authority]))
            confidence = triggered_doctrines[0].confidence
            return answer, reasoning_chain, authorities, confidence

        # Layer 2: Semantic fallback (simplified—no vector DB in this implementation)
        reasoning_chain = ["No direct doctrine match; applying general water chemistry principles"]
        answer = f"General water chemistry analysis for: {query}\n\nThis query requires expert review. Consult AWWA/EPA guidelines."
        authorities = ["AWWA Standards", "EPA Drinking Water Regulations", "Standard Methods"]
        confidence = ConfidenceLevel.DISCLOSURE

        return answer, reasoning_chain, authorities, confidence

    def synthesize_answer(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> str:
        """Generate response based on mode and zone"""

        primary = doctrines[0]

        if mode == ResponseMode.FAST:
            # Concise, bullet-point response
            answer = f"**{primary.topic.replace('_', ' ').title()}**\n\n"
            answer += f"{primary.conclusion_template}\n\n"
            answer += "**Key Factors:**\n"
            for factor in primary.key_factors[:3]:
                answer += f"- {factor}\n"
            answer += f"\n**Authority:** {primary.primary_authority[0]}"

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready, detailed analysis
            answer = f"# {primary.topic.replace('_', ' ').title()}\n\n"
            answer += f"## Analysis Zone: {zone.value}\n\n"
            answer += f"### Conclusion\n{primary.conclusion_template}\n\n"
            answer += f"### Reasoning Framework\n{primary.reasoning_framework}\n\n"
            answer += "### Critical Factors\n"
            for i, factor in enumerate(primary.key_factors, 1):
                answer += f"{i}. {factor}\n"
            answer += "\n### Primary Authority\n"
            for auth in primary.primary_authority:
                answer += f"- {auth}\n"
            answer += f"\n### Confidence Stratification\n{primary.confidence_stratification}\n"
            answer += f"\n### Adversarial Analysis\n"
            answer += f"**Opposing Position:** {primary.adversary_position}\n"
            answer += f"**Counter-Arguments:**\n"
            for arg in primary.counter_arguments:
                answer += f"- {arg}\n"
            answer += f"\n**Resolution Strategy:** {primary.resolution_strategy}\n"

        else:  # MEMO
            # Full documentation
            answer = f"# MEMORANDUM: {primary.topic.replace('_', ' ').title()}\n\n"
            answer += f"**Category:** {primary.category.value} | **Confidence:** {primary.confidence.value}\n"
            answer += f"**Zone:** {zone.value} | **Entity Scope:** {primary.entity_scope}\n\n"
            answer += f"## Executive Summary\n{primary.conclusion_template}\n\n"
            answer += f"## Detailed Analysis\n{primary.reasoning_framework}\n\n"
            answer += "## Key Determinative Factors\n"
            for i, factor in enumerate(primary.key_factors, 1):
                answer += f"{i}. {factor}\n"
            answer += "\n## Legal and Technical Authority\n"
            for auth in primary.primary_authority:
                answer += f"- {auth}\n"
            answer += f"\n## Controlling Precedent\n{primary.controlling_precedent}\n"
            answer += f"\n## Burden of Proof\n{primary.burden_holder}\n"
            answer += f"\n## Counter-Position Analysis\n"
            answer += f"**Adversary Likely Argues:** {primary.adversary_position}\n\n"
            answer += "**Our Rebuttals:**\n"
            for arg in primary.counter_arguments:
                answer += f"- {arg}\n"
            answer += f"\n## Recommended Strategy\n{primary.resolution_strategy}\n"
            answer += f"\n## Confidence Assessment\n{primary.confidence_stratification}\n"

        # Add multiple doctrines if relevant
        if len(doctrines) > 1 and mode != ResponseMode.FAST:
            answer += "\n\n---\n## Related Doctrines\n"
            for doctrine in doctrines[1:3]:
                answer += f"\n### {doctrine.topic.replace('_', ' ').title()}\n"
                answer += f"{doctrine.conclusion_template}\n"

        return answer

    def calculate_determinism_hash(self, query: str, answer: str) -> str:
        """SHA-256 hash for reproducibility verification"""
        content = f"{query}|{answer}|{VERSION}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def log_audit_trail(self, query: str, response: QueryResponse):
        """Append-only JSONL audit log"""
        audit_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query": query,
            "mode": response.mode.value,
            "zone": response.zone.value,
            "doctrines": response.doctrines_triggered,
            "confidence": response.confidence.value,
            "latency_ms": response.latency_ms,
            "hash": response.determinism_hash
        }

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry) + "\n")

    async def query(self, request: QueryRequest) -> QueryResponse:
        """Main query endpoint - TIE-20 full stack"""
        start = time.time()
        self.query_count += 1

        # Three-layer response
        answer, reasoning_chain, authorities, confidence = self.three_layer_response(
            request.question, request.mode, request.zone
        )

        # Collect triggered doctrines
        doctrines_triggered = [d.topic for d in self.search_doctrines(request.question)]

        # Calculate hash
        determinism_hash = self.calculate_determinism_hash(request.question, answer)

        # Latency
        latency_ms = (time.time() - start) * 1000
        self.total_latency += latency_ms

        response = QueryResponse(
            answer=answer,
            mode=request.mode,
            zone=request.zone,
            doctrines_triggered=doctrines_triggered,
            confidence=confidence,
            reasoning_chain=reasoning_chain,
            authorities=authorities,
            determinism_hash=determinism_hash,
            latency_ms=round(latency_ms, 2),
            timestamp=datetime.now(timezone.utc).isoformat()
        )

        # Audit trail
        self.log_audit_trail(request.question, response)

        logger.info(f"Query processed | {latency_ms:.0f}ms | {len(doctrines_triggered)} doctrines | {confidence.value}")

        return response

    def health_check(self) -> HealthResponse:
        """TIE-20 Component: Health endpoint"""
        uptime = time.time() - self.start_time
        avg_latency = self.total_latency / self.query_count if self.query_count > 0 else 0.0
        cache_hit_rate = self.cache_hits / self.query_count if self.query_count > 0 else 0.0

        return HealthResponse(
            status="operational",
            engine_id=ENGINE_ID,
            version=VERSION,
            port=PORT,
            doctrines_loaded=len(self.doctrines),
            uptime_seconds=round(uptime, 1),
            total_queries=self.query_count,
            avg_latency_ms=round(avg_latency, 2),
            cache_hit_rate=round(cache_hit_rate, 3)
        )

# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title=ENGINE_NAME,
    description="Water Chemistry Intelligence Engine - TIE-Grade Compliance",
    version=VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

engine = CHEM15Engine()

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint"""
    try:
        return await engine.query(request)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint"""
    return engine.health_check()

@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine topics"""
    return {
        "count": len(DOCTRINE_CACHE),
        "topics": [d.topic for d in DOCTRINE_CACHE],
        "categories": list(set(d.category.value for d in DOCTRINE_CACHE))
    }

# =========================================================
# MAIN ENTRY POINT
# =========================================================

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
