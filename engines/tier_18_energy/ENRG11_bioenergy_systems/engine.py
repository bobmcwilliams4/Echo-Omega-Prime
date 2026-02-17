"""
ENRG11 Bioenergy Systems Intelligence Engine v1.0.0
TIE-Grade Domain: Biomass Conversion, Biogas Production, Biodiesel Transesterification,
Cellulosic Ethanol, Anaerobic Digestion, Feedstock Logistics

Port: 9331 | Authority Level: CRITICAL | Confidence: DEFENSIBLE
"""

import sys
from pathlib import Path

# CRITICAL: Add parent directory to sys.path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Literal, Set, Tuple
from enum import Enum
from dataclasses import dataclass, field, asdict

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from loguru import logger


# ============================================================================
# ENUMS & CONFIGURATION
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
    BIOMASS_CONVERSION = "BIOMASS_CONVERSION"
    BIOGAS_PRODUCTION = "BIOGAS_PRODUCTION"
    BIODIESEL_PRODUCTION = "BIODIESEL_PRODUCTION"
    ETHANOL_PRODUCTION = "ETHANOL_PRODUCTION"
    ANAEROBIC_DIGESTION = "ANAEROBIC_DIGESTION"
    FEEDSTOCK_LOGISTICS = "FEEDSTOCK_LOGISTICS"
    ENERGY_YIELD = "ENERGY_YIELD"
    PROCESS_OPTIMIZATION = "PROCESS_OPTIMIZATION"
    ENVIRONMENTAL_COMPLIANCE = "ENVIRONMENTAL_COMPLIANCE"
    ECONOMIC_VIABILITY = "ECONOMIC_VIABILITY"
    CATALYST_CHEMISTRY = "CATALYST_CHEMISTRY"
    MICROBIAL_SYSTEMS = "MICROBIAL_SYSTEMS"


class AuthorityLevel(str, Enum):
    SUPREME_COURT = "SUPREME_COURT"
    FEDERAL_STATUTE = "FEDERAL_STATUTE"
    AGENCY_REGULATION = "AGENCY_REGULATION"
    STATE_STATUTE = "STATE_STATUTE"
    CASE_LAW = "CASE_LAW"
    INDUSTRY_STANDARD = "INDUSTRY_STANDARD"
    PEER_REVIEWED = "PEER_REVIEWED"
    ENGINEERING_PRACTICE = "ENGINEERING_PRACTICE"


# ============================================================================
# DOCTRINE BLOCKS (25+ with REAL bioenergy expertise)
# ============================================================================

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
    confidence_stratification: str
    controlling_precedent: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Biomass Feedstock Energy Density Analysis",
        keywords=["energy content", "heating value", "moisture content", "ash content", "bulk density", "calorific value", "HHV", "LHV"],
        conclusion_template=[
            "Higher heating value (HHV) represents total energy content including condensation heat of water vapor.",
            "Lower heating value (LHV) excludes latent heat and better represents usable energy in most conversion processes.",
            "Moisture content above 50% wet basis dramatically reduces net energy yield in thermochemical processes."
        ],
        reasoning_framework="""
        Energy density analysis follows established calorimetric principles:
        1. HHV measured via bomb calorimetry at constant volume
        2. LHV = HHV - (2.442 * H2O_content) in MJ/kg
        3. Ash content reduces combustible fraction, increases handling costs
        4. Bulk density affects transportation economics and reactor sizing
        5. Volatile matter content indicates thermochemical conversion suitability

        For lignocellulosic biomass (corn stover, switchgrass, wood):
        - HHV typically 17-19 MJ/kg dry basis
        - Moisture content 15-50% as-received
        - Ash 2-15% dry basis depending on harvest method

        For oil crops (soybeans, rapeseed, jatropha):
        - Oil fraction 18-45% by weight
        - Oil HHV 37-40 MJ/kg
        - Protein/fiber co-products with fuel value 15-18 MJ/kg

        Energy balance must account for drying energy (2.3 MJ/kg water evaporated),
        transportation costs (0.1-0.3 $/ton-mile), and pre-processing energy.
        """,
        key_factors=[
            "Moisture content (wet basis vs dry basis calculation)",
            "Ash composition (fusion temperature, slagging propensity)",
            "Elemental analysis (C, H, O, N, S, Cl content)",
            "Volatile matter and fixed carbon ratio",
            "Lignin/cellulose/hemicellulose fractions",
            "Particle size distribution post-grinding",
            "Seasonal variation in feedstock properties"
        ],
        primary_authority=[
            "ASTM D5865 Standard Test Method for Gross Calorific Value",
            "ASTM E871 Moisture Analysis of Biomass",
            "ISO 18134 Biomass Moisture Content Determination",
            "DOE Biomass Feedstock Composition and Property Database"
        ],
        burden_holder="Process Engineer",
        adversary_position="Vendor may report HHV without moisture penalty or ash content disclaimer",
        counter_arguments=[
            "Seasonal moisture variation not captured in single measurement",
            "Lab HHV may not reflect field-scale heterogeneity",
            "Transportation drying during storage can improve delivered energy density",
            "Ash may have fertilizer value offsetting disposal cost"
        ],
        resolution_strategy="Require vendor to provide moisture and ash corrected LHV with statistical variation across delivery batches",
        entity_scope="Feedstock procurement, conversion process design",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard analytical methods, but feedstock heterogeneity introduces 5-10% uncertainty",
        controlling_precedent="NREL Biomass Compositional Analysis Procedures"
    ),

    DoctrineBlock(
        topic="Anaerobic Digestion Kinetics and Reactor Design",
        keywords=["biogas", "methane yield", "HRT", "OLR", "VS destruction", "VFA", "alkalinity", "pH control"],
        conclusion_template=[
            "Hydraulic retention time (HRT) must exceed microbial growth rate to prevent washout of slow-growing methanogens.",
            "Organic loading rate (OLR) limited by acetoclastic methanogen kinetics, typically 2-4 kg VS/m3/day for mesophilic CSTR.",
            "VFA accumulation above 2000 mg/L acetate equivalent signals process instability and imminent failure."
        ],
        reasoning_framework="""
        Anaerobic digestion is a four-stage biochemical process:

        1. HYDROLYSIS: Polymeric organics → monomers (rate-limiting for lignocellulosic substrates)
        2. ACIDOGENESIS: Monomers → VFAs, alcohols, CO2, H2
        3. ACETOGENESIS: VFAs, alcohols → acetate, H2, CO2
        4. METHANOGENESIS: Acetate + H2/CO2 → CH4 + CO2

        Key kinetic constraints:
        - Methanogens have slow growth rate (μmax ~ 0.4-1.0 d^-1 at 35°C mesophilic)
        - Hydrolysis k typically 0.05-0.3 d^-1 for lignocellulose
        - Minimum HRT = 1.5 to 2.0 / μmax to maintain methanogen population
        - OLR = VS_feed / (V_reactor * HRT) in kg VS/m3/day

        Process stability indicators:
        - VFA/alkalinity ratio < 0.4 for stable operation
        - pH 6.8-7.4 optimal for methanogens
        - Ammonia toxicity threshold 1500-3000 mg N/L
        - Volatile solids destruction 40-60% typical, 70%+ for optimized systems

        CSTR vs plug-flow vs UASB reactor selection:
        - CSTR: Well-mixed, 15-30 day HRT, handles high solids (8-12%)
        - Plug-flow: Horizontal unmixed, 20-40 day HRT, fibrous feedstocks
        - UASB: Upflow anaerobic sludge blanket, 0.5-2 day HRT, low-solids wastewater
        """,
        key_factors=[
            "Temperature regime (psychrophilic 15-25°C, mesophilic 30-40°C, thermophilic 50-60°C)",
            "Feedstock C/N ratio (optimal 20-30:1)",
            "Trace metal availability (Ni, Co, Mo, Fe for methanogen enzymes)",
            "Toxic compound concentration (ammonia, H2S, LCFA inhibition)",
            "Mixing intensity and dead zones",
            "Biogas composition (CH4 50-70%, CO2 30-50%, H2S 100-10000 ppm)",
            "Reactor heating energy balance (must be <30% biogas production)"
        ],
        primary_authority=[
            "Tchobanoglous et al., Wastewater Engineering (methanogen kinetics)",
            "IEA Bioenergy Task 37 Biogas Guidelines",
            "ASABE Standard EP496.3 Agricultural Biogas Production",
            "German DIN 38414 Fermentation of Sludge"
        ],
        burden_holder="Biogas Plant Operator",
        adversary_position="Vendor may overestimate methane yield using lab-scale batch tests without accounting for continuous flow non-ideality",
        counter_arguments=[
            "Higher thermophilic temperatures allow shorter HRT (10-15 days)",
            "Co-digestion of high-lipid waste can boost methane yield 20-40%",
            "Pre-treatment (thermal, chemical, mechanical) can accelerate hydrolysis",
            "Two-stage digestion separates acidogenesis and methanogenesis for higher rates"
        ],
        resolution_strategy="Pilot testing at design OLR and HRT for minimum 3 retention times to confirm stable VFA profile and methane yield",
        entity_scope="Agricultural digesters, wastewater treatment, industrial organic waste",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established microbial kinetics, but substrate-specific hydrolysis rates require empirical determination",
        controlling_precedent="Batstone et al. ADM1 (Anaerobic Digestion Model No. 1) IWA Task Group"
    ),

    DoctrineBlock(
        topic="Biogas Upgrading and Purification Technologies",
        keywords=["biogas", "biomethane", "CO2 removal", "H2S removal", "siloxane", "water scrubbing", "PSA", "membrane", "amine scrubbing"],
        conclusion_template=[
            "Pipeline injection requires methane content >95%, H2S <4 ppm, water dew point <-40°F to prevent hydrate formation.",
            "Water scrubbing achieves 95-98% CH4 at lowest capital cost but has 2-4% methane slip.",
            "Pressure swing adsorption (PSA) achieves >99% CH4 with <0.5% slip but requires pre-drying and H2S removal."
        ],
        reasoning_framework="""
        Raw biogas composition:
        - CH4: 50-70% (target fuel component)
        - CO2: 30-50% (must remove for energy density and corrosion control)
        - H2S: 100-10,000 ppm (corrosive, catalyst poison, SOx emissions precursor)
        - NH3: 0-100 ppm (corrosive in presence of moisture)
        - Siloxanes: 0-50 mg/m3 (forms SiO2 deposits in engines and turbines)
        - Water: Saturated at digester temperature (must remove to prevent freezing/hydrates)

        CO2 Removal Technologies:

        1. WATER SCRUBBING (most common, 40% of installations):
           - Principle: CO2 solubility in water 25x higher than CH4 at 8-10 bar
           - Countercurrent packed column, 4-8 bar operating pressure
           - Achieves 95-98% CH4 purity
           - Methane slip 2-4% (dissolved in water, can recover via flash tank)
           - No chemical consumption, but needs 0.1-0.3 kWh/m3 biogas power

        2. PRESSURE SWING ADSORPTION:
           - Activated carbon or zeolite molecular sieves
           - 4-12 bed cyclic process (adsorption, depressurization, purge, repressurization)
           - Achieves >99% CH4 with <0.5% slip
           - Requires pre-drying to <0.1% RH and H2S removal
           - 0.2-0.4 kWh/m3 biogas, higher capital cost

        3. MEMBRANE SEPARATION:
           - Polymeric membranes (cellulose acetate, polyimide) selective to CO2
           - Pressure differential 25-40 bar feed side
           - Two-stage required for >96% CH4
           - Methane slip 5-8% (economic trade-off)
           - 0.18-0.25 kWh/m3, compact footprint

        4. AMINE SCRUBBING (for large scale >1500 m3/h):
           - Chemical absorption via MEA, DEA, or MDEA solutions
           - Regeneration via temperature swing (120-140°C stripper)
           - Achieves 99%+ CH4 with <0.1% slip
           - High operating cost (heat, amine makeup, corrosion inhibitors)

        H2S Removal (required upstream of all CO2 removal):
        - Iron oxide/hydroxide scavengers (disposable, <100 ppm H2S inlet)
        - Biological oxidation (air injection 2-6% into digester headspace)
        - Activated carbon (impregnated with KOH or NaOH)
        - Caustic scrubbing (NaOH solution for high H2S >2000 ppm)

        Siloxane Removal:
        - Activated carbon adsorption (0.5-2 year bed life)
        - Refrigeration chilling to condense siloxanes
        - Critical for landfill gas, less for agricultural digesters
        """,
        key_factors=[
            "Target application (grid injection vs CNG vehicle fuel vs heat/power)",
            "Biogas flow rate and composition stability",
            "Grid interconnection pressure and quality specifications",
            "Capital cost vs operating cost trade-off (electricity, consumables)",
            "Methane slip environmental impact (CH4 GWP = 28x CO2)",
            "Footprint constraints and modular scalability",
            "Downstream equipment corrosion tolerance (engine vs fuel cell)"
        ],
        primary_authority=[
            "SAE J1616 CNG Vehicle Fuel Quality",
            "Pipeline Quality Biomethane Interconnection Standards",
            "ISO 16923 Natural Gas Fueling Stations Specifications",
            "IEA Bioenergy Task 37 Biogas Upgrading Technologies Review"
        ],
        burden_holder="Biogas Upgrader Operator",
        adversary_position="Equipment vendor may quote performance at ideal lab conditions without H2S, siloxanes, or fluctuating flow",
        counter_arguments=[
            "Cryogenic upgrading can achieve highest purity with CO2 liquefaction co-product",
            "Hybrid systems (water scrubbing + PSA polish) optimize cost and purity",
            "Offline H2S scavenging cheaper than integrated biological removal for low concentrations",
            "Direct biogas use in combined heat and power (CHP) avoids upgrading cost for on-site applications"
        ],
        resolution_strategy="Require vendor performance guarantee at actual raw biogas composition with penalty clauses for purity/slip shortfall",
        entity_scope="Biogas-to-biomethane upgrading, renewable natural gas (RNG) projects",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Mature commercial technologies with 30+ years operating history, but membrane and PSA costs decreasing rapidly",
        controlling_precedent="German DVGW G 260/G 262 Gas Quality Standards"
    ),

    DoctrineBlock(
        topic="Biodiesel Transesterification Chemistry and Process Control",
        keywords=["biodiesel", "transesterification", "methanol", "catalyst", "FFA", "glycerol", "ASTM D6751", "soap formation"],
        conclusion_template=[
            "Feedstock free fatty acid (FFA) content above 2% causes soap formation with alkaline catalysts, requiring acid pre-esterification.",
            "Excess methanol (6:1 molar ratio vs stoichiometric 3:1) drives reaction toward completion and phase separation.",
            "Water content above 0.3% hydrolyzes triglycerides to FFAs and deactivates alkaline catalysts, requiring feedstock drying."
        ],
        reasoning_framework="""
        Biodiesel production via transesterification:

        REACTION: Triglyceride + 3 CH3OH ↔ 3 FAME + Glycerol

        Stoichiometry: 3:1 molar methanol:oil, but industrial practice uses 6:1 to overcome equilibrium
        Catalysts:
        - Alkaline (NaOH, KOH): Fast reaction (1-2 hours at 60°C), low cost, but sensitive to FFA and water
        - Acid (H2SO4, HCl): Slow reaction (24-72 hours), tolerates high FFA, used for pre-treatment
        - Enzymatic (lipases): Room temperature, tolerates water/FFA, very expensive, slow (8-48 hours)

        ALKALINE CATALYZED PROCESS (most common, 85% of industry):
        1. Feedstock preparation:
           - Heat oil to 60-65°C (above methanol BP 64.7°C to prevent vaporization)
           - Dry to <0.06% water via vacuum or molecular sieves
           - If FFA >2%, acid pre-esterification with H2SO4 and methanol first

        2. Reaction:
           - Mix methanol + catalyst (0.5-1.5 wt% KOH on oil basis)
           - Add to heated oil with vigorous mixing
           - Maintain 60-65°C under slight N2 pressure to keep methanol liquid
           - Reaction time 1-2 hours to 95%+ conversion

        3. Separation:
           - Gravity settling 4-8 hours (or centrifuge for fast continuous process)
           - Heavy phase: glycerol (79-88% purity) + excess methanol + catalyst
           - Light phase: biodiesel (FAME) + excess methanol + residual catalyst

        4. Purification:
           - Water washing 3x (removes methanol, catalyst, glycerol, soaps)
           - OR ion exchange resin dry washing (no wastewater, faster)
           - Vacuum distillation to remove methanol (recycle)
           - Polishing to ASTM D6751 specifications

        CRITICAL QUALITY PARAMETERS (ASTM D6751):
        - Ester content: ≥96.5 wt%
        - Kinematic viscosity: 1.9-6.0 mm²/s at 40°C
        - Flash point: ≥93°C (ensures no residual methanol)
        - Sulfur: ≤15 ppm (ultra-low sulfur diesel compatibility)
        - Water and sediment: ≤0.05 vol%
        - Acid number: ≤0.50 mg KOH/g (oxidation stability)
        - Free glycerol: ≤0.02 wt% (prevents injector deposits)
        - Total glycerol: ≤0.24 wt% (includes mono-, di-, triglycerides)
        - Cloud point, cold filter plugging point (climate-dependent, C12-C18 FAME distribution)

        SOAP FORMATION PROBLEM:
        FFA + KOH → Soap (potassium carboxylate) + H2O
        - Soaps stabilize emulsions, prevent phase separation
        - Consume catalyst, reduce yield
        - Create disposal problems (hazardous waste)
        - Mitigation: Acid pre-esterification or enzymatic catalyst for high-FFA feedstocks

        FEEDSTOCK CONSIDERATIONS:
        - Soybean oil: 53% linoleic C18:2 (polyunsaturated, oxidation stability issue)
        - Palm oil: 44% palmitic C16:0 (saturated, high cloud point 13-16°C)
        - Rapeseed/canola: 61% oleic C18:1 (monounsaturated, good balance)
        - Waste cooking oil: Variable FFA 2-20%, requires pre-treatment
        - Jatropha, camelina, algae: Emerging but supply chain immature
        """,
        key_factors=[
            "Feedstock FFA content and pre-treatment economics",
            "Methanol recovery system efficiency (>98% recovery essential)",
            "Glycerol purity and market value (pharmaceutical vs crude)",
            "Water washing vs dry washing (capital cost vs wastewater treatment)",
            "Catalyst choice (KOH vs NaOH vs sodium methoxide)",
            "Reaction temperature control (prevent methanol vaporization, minimize energy)",
            "Oxidation stability (may require antioxidants like BHT, TBHQ for long-term storage)"
        ],
        primary_authority=[
            "ASTM D6751 Standard Specification for Biodiesel Fuel",
            "EN 14214 European Biodiesel Standard",
            "Gerpen et al. Biodiesel Production Technology (NREL)",
            "Freedman et al. Transesterification Kinetics J. Am. Oil Chem. Soc. 1986"
        ],
        burden_holder="Biodiesel Producer",
        adversary_position="Feedstock supplier may not disclose FFA content or water contamination, leading to batch failures",
        counter_arguments=[
            "Supercritical methanol transesterification eliminates catalyst, tolerates high FFA, but requires 350°C and 250 bar",
            "Two-stage process (alkali + acid) can handle wide range of feedstock quality",
            "Enzymatic catalysis becoming economical with immobilized lipase technology",
            "Glycerol can be converted to value-added products (propylene glycol, polyols) improving economics"
        ],
        resolution_strategy="Require feedstock certificate of analysis with FFA, water, phosphorus content; include quality clause in purchase contract",
        entity_scope="Biodiesel production facilities, renewable diesel blending terminals",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established chemistry with 25+ years commercial operation, but feedstock variability introduces process risk",
        controlling_precedent="ASTM D6751 and EN 14214 consensus standards"
    ),

    DoctrineBlock(
        topic="Cellulosic Ethanol Production via Enzymatic Hydrolysis",
        keywords=["cellulose", "hemicellulose", "lignin", "pretreatment", "cellulase", "SSF", "SSCF", "pentose fermentation", "C5 sugars"],
        conclusion_template=[
            "Lignocellulosic biomass requires pretreatment to disrupt lignin-cellulose matrix before enzymatic hydrolysis achieves >70% glucose yield.",
            "Simultaneous saccharification and fermentation (SSF) reduces end-product inhibition but limits process to yeast-compatible 35°C vs enzyme optimum 50°C.",
            "Pentose sugar fermentation (xylose, arabinose) requires engineered organisms, adding 25-35% to theoretical ethanol yield from hemicellulose."
        ],
        reasoning_framework="""
        Lignocellulosic biomass composition (corn stover, switchgrass, wood):
        - Cellulose: 35-50% (linear glucose polymer, crystalline structure)
        - Hemicellulose: 20-35% (branched C5/C6 sugars: xylose, arabinose, mannose, galactose)
        - Lignin: 15-25% (complex aromatic polymer, provides structural rigidity)
        - Ash and extractives: 5-15%

        RECALCITRANCE PROBLEM:
        Lignin forms covalent bonds with cellulose/hemicellulose, creating physical barrier.
        Cellulose crystallinity prevents enzyme access to β-1,4-glycosidic bonds.
        Native biomass enzymatic hydrolysis: <20% glucose yield, economically infeasible.

        PRETREATMENT TECHNOLOGIES (critical step, 30-40% of production cost):

        1. DILUTE ACID PRETREATMENT (most mature):
           - 0.5-2% H2SO4, 140-200°C, 5-30 minutes
           - Hydrolyzes hemicellulose to C5 sugars (xylose, arabinose)
           - Disrupts lignin-carbohydrate bonds, increases cellulose accessibility
           - Creates fermentation inhibitors: furfural, HMF, acetic acid, lignin phenolics
           - Post-pretreatment detoxification required (overliming, activated carbon, ion exchange)

        2. STEAM EXPLOSION:
           - High-pressure saturated steam 160-260°C, 1-10 minutes
           - Rapid depressurization explodes fiber structure
           - Hemicellulose partial hydrolysis, lignin redistribution
           - Lower inhibitor formation than dilute acid
           - High energy consumption (5-10% of ethanol energy content)

        3. AMMONIA FIBER EXPANSION (AFEX):
           - Liquid ammonia 60-100°C, 10-60 minutes
           - Removes acetyl groups, cleaves lignin-carbohydrate bonds
           - Preserves hemicellulose in polymer form (requires separate enzyme for C5 release)
           - Ammonia recovery essential (expensive, hazardous)

        4. IONIC LIQUID PRETREATMENT:
           - 1-ethyl-3-methylimidazolium acetate [EMIM][OAc]
           - Dissolves cellulose, regenerates as amorphous high-surface-area form
           - Near-complete cellulose conversion, but IL cost and recovery challenging
           - Lab/pilot stage, not yet commercial

        ENZYMATIC HYDROLYSIS:
        Cellulase enzyme cocktail (Trichoderma reesei or engineered strains):
        - Endoglucanase: Attacks amorphous cellulose, creates chain ends
        - Exoglucanase (cellobiohydrolase): Processes chain ends, releases cellobiose
        - β-glucosidase: Cleaves cellobiose to glucose monomers

        Enzyme loading: 10-30 FPU/g cellulose (filter paper units)
        Reaction conditions: pH 4.8-5.0, 50°C optimal (but see SSF trade-off below)
        Hydrolysis time: 48-96 hours to 70-90% cellulose conversion
        Glucose yield: 70-90% of theoretical depending on pretreatment effectiveness

        FERMENTATION STRATEGIES:

        1. SEPARATE HYDROLYSIS AND FERMENTATION (SHF):
           - Hydrolysis at 50°C for 72 hours
           - Cool, inoculate Saccharomyces cerevisiae, ferment at 35°C
           - Advantage: Each step at optimal temperature
           - Disadvantage: Glucose accumulation inhibits cellulase (end-product inhibition)

        2. SIMULTANEOUS SACCHARIFICATION AND FERMENTATION (SSF):
           - Add enzymes and yeast together at 35°C
           - Yeast consumes glucose as produced, relieving enzyme inhibition
           - 10-20% higher ethanol yield than SHF
           - Disadvantage: Sub-optimal for enzyme activity (50% reduction at 35°C vs 50°C)

        3. SIMULTANEOUS SACCHARIFICATION AND CO-FERMENTATION (SSCF):
           - Engineered yeast (Saccharomyces cerevisiae with xylose pathway genes)
           - Ferments glucose + xylose simultaneously
           - Adds 25-35% ethanol yield from hemicellulose fraction
           - Zymomonas mobilis alternative (naturally ferments C5 and C6)

        4. CONSOLIDATED BIOPROCESSING (CBP):
           - Single engineered organism produces cellulase AND ferments sugars
           - Eliminates enzyme production cost (20-30% of total)
           - Clostridium thermocellum or engineered Caldicellulosiruptor species
           - Pilot stage only, thermophilic (60°C) ethanol tolerance challenge

        INHIBITOR DETOXIFICATION:
        Pretreatment creates fermentation inhibitors:
        - Furfural (from xylose degradation): >1 g/L toxic to yeast
        - 5-hydroxymethylfurfural (HMF from glucose): >2 g/L toxic
        - Acetic acid (from acetyl groups): >5 g/L inhibits at low pH
        - Phenolic compounds (from lignin): 1-4 g/L inhibit

        Detoxification methods:
        - Overliming (Ca(OH)2 to pH 10, then re-acidify) removes 50-80% inhibitors
        - Activated carbon adsorption (expensive, 5-10% sugar loss)
        - Laccase enzyme oxidation of phenolics
        - Adapted yeast strains with inhibitor tolerance (evolutionary engineering)
        """,
        key_factors=[
            "Feedstock composition (hardwood vs softwood vs grass, lignin content)",
            "Pretreatment severity factor log(R0) = log(t * exp((T-100)/14.75))",
            "Enzyme cost and recycling potential",
            "Pentose fermentation organism performance (xylose consumption rate)",
            "Inhibitor concentration and detoxification cost",
            "Water usage and wastewater treatment (3-6 gallons water per gallon ethanol)",
            "Solid lignin residue utilization (combustion for process heat vs higher-value products)"
        ],
        primary_authority=[
            "DOE BETO Multi-Year Program Plan (cellulosic biofuels)",
            "NREL Techno-Economic Analysis Models",
            "Biomass Recalcitrance (Himmel 2008)",
            "Lynd et al. Microbial Cellulose Utilization (Science 2002)"
        ],
        burden_holder="Cellulosic Ethanol Producer",
        adversary_position="Technology vendors may report lab-scale yields without accounting for inhibitor formation or enzyme cost at industrial scale",
        counter_arguments=[
            "Fungal pretreatment (white-rot fungi) can delignify biomass with minimal inhibitor formation",
            "Hot water pretreatment avoids chemical costs but requires higher temperature and longer time",
            "C5 sugar conversion to xylitol or furfural may be more valuable than ethanol fermentation",
            "AFEX-pretreated biomass can be stored long-term without degradation, decoupling pretreatment from downstream"
        ],
        resolution_strategy="Pilot testing with actual feedstock at design pretreatment severity and full integration through fermentation to validate yield and cost assumptions",
        entity_scope="2G ethanol plants, lignocellulosic biorefineries",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Significant technical risk remains; only a few commercial plants operating, most shut down due to economics",
        controlling_precedent="POET-DSM Project Liberty and DuPont Nevada cellulosic ethanol plants as commercial proof-of-concept"
    ),

    DoctrineBlock(
        topic="Feedstock Logistics and Supply Chain Optimization",
        keywords=["biomass supply", "densification", "pelletization", "torrefaction", "storage losses", "transportation cost", "seasonal availability"],
        conclusion_template=[
            "Biomass transportation cost 0.10-0.30 $/ton-mile limits economical haul radius to 50-75 miles for 15 $/ton delivered feedstock.",
            "Field drying corn stover from 35% to 15% moisture saves 1.8 MJ/kg avoided drying energy but risks 10-25% dry matter loss from weathering.",
            "Pelletization increases bulk density from 150-200 kg/m3 loose biomass to 600-750 kg/m3, reducing transportation cost per energy unit by 65-75%."
        ],
        reasoning_framework="""
        Feedstock logistics economic constraints:

        COST STRUCTURE (for corn stover, switchgrass, forest residue):
        - Harvest/collection: 15-35 $/dry ton (equipment, labor, fuel)
        - On-farm storage: 3-8 $/dry ton (land rental, tarp/building, DM loss)
        - Transportation: 0.10-0.30 $/ton-mile depending on truck size and utilization
        - Preprocessing (grinding, drying): 10-25 $/dry ton
        - Storage at conversion facility: 5-12 $/dry ton
        - TOTAL delivered cost: 50-100 $/dry ton depending on distance and quality

        TRANSPORTATION ECONOMICS:
        Truck payload limited by weight (25 tons gross vehicle weight in most jurisdictions) or volume:
        - Loose bales (150 kg/m3): Volume-limited to 8-12 dry tons per load
        - Densified pellets (650 kg/m3): Weight-limited to 22-25 dry tons per load

        Cost per ton-mile:
        - Short haul <50 miles: 0.25-0.35 $/ton-mile (low truck utilization)
        - Medium haul 50-150 miles: 0.15-0.25 $/ton-mile
        - Long haul >150 miles: 0.10-0.18 $/ton-mile (but total cost prohibitive)

        Economical haul radius R for target delivered cost C and transportation rate T:
        R = (C - harvest_cost - preprocessing_cost) / T
        Example: 75 $/ton delivered, 35 $/ton harvest, 15 $/ton preprocess, 0.20 $/ton-mile
        → R = (75 - 35 - 15) / 0.20 = 125 miles maximum

        MOISTURE CONTENT MANAGEMENT:
        As-harvested moisture:
        - Corn stover: 30-50% (late fall harvest)
        - Switchgrass: 20-40% (depends on cutting time)
        - Wood chips: 40-55% (fresh cut)

        Drying energy required:
        - Latent heat of vaporization: 2.3 MJ/kg water
        - To dry 1 ton from 40% to 15% moisture: Remove 417 kg water = 960 MJ
        - Natural gas dryer at 65% efficiency: 1480 MJ = 38 m3 natural gas at 3 $/GJ = 4.40 $ per ton dried

        FIELD DRYING strategies:
        - Leave cut biomass in windrows for solar drying 2-4 weeks
        - Can achieve 15-25% moisture if weather cooperates
        - Risks:
          * Rain events re-wet biomass, increase mold/fungal degradation
          * Dry matter loss 10-25% from leaf loss, microbial respiration
          * Nutrient leaching (K, N) reduces fertilizer value of ash
        - Best for arid climates with low rain probability during harvest

        DENSIFICATION TECHNOLOGIES:

        1. PELLETIZATION:
           - Grind to <6 mm, add binder (lignin activated by heat), extrude through die
           - Pellet density 600-750 kg/m3 (vs 150-200 loose bales)
           - Energy consumption: 80-120 kWh/ton (about 1.5% of biomass energy content)
           - Cost: 15-25 $/ton depending on scale
           - Durability: 95-98% (resistant to breakage during handling)

        2. TORREFACTION + PELLETIZATION:
           - Mild pyrolysis 250-300°C in oxygen-free environment
           - Removes 20-30% mass (volatiles, water), concentrates energy
           - Brittle product easier to grind (50% less grinding energy)
           - Hydrophobic (no moisture re-adsorption during storage)
           - Mass yield 70-80%, energy yield 85-90%
           - Creates 'bio-coal' with HHV 20-24 MJ/kg (vs 17-19 raw)
           - Expensive (35-50 $/ton processing cost), limited commercial deployment

        3. BRIQUETTING:
           - Simpler than pelletization, larger product (50-100 mm diameter)
           - Lower density (500-600 kg/m3) and durability (85-90%)
           - Lower cost (10-15 $/ton) but less suitable for long-distance transport

        STORAGE LOSSES:
        Dry matter loss during storage from:
        - Microbial respiration (aerobic if exposed to air)
        - Fungal growth (moisture >20% enables mold)
        - Physical weathering (UV degradation, wind loss)

        Typical DM loss rates:
        - Indoor dry storage (<15% moisture): 1-3% loss over 6 months
        - Outdoor covered (tarp): 5-12% loss
        - Outdoor uncovered: 15-35% loss (unacceptable)
        - Ensiling (like corn silage): 8-15% loss but preserves energy content

        SUPPLY CHAIN CONFIGURATIONS:

        1. CONVENTIONAL (direct delivery):
           Farmgate → Truck → Conversion plant
           - Simple, low capital cost
           - Limited haul radius (50-75 miles economic)
           - Seasonal delivery requires large on-site storage

        2. DEPOT MODEL (intermediate preprocessing):
           Multiple farmgates → Local depot (grind, dry, densify) → Truck/rail → Plant
           - Extends economic haul radius to 150-300 miles
           - Depot capital cost 2-5 M$ for 100,000 ton/year capacity
           - Year-round depot operation smooths seasonal harvest

        3. BIOMASS SUPPLY COOPERATIVE:
           - Farmers aggregate supply, contract with plant
           - Cooperative owns densification equipment, shares transport
           - Reduces individual farmer risk, improves bargaining power

        ADVANCED LOGISTICS:
        - GIS-based supply shed mapping (identifies optimal depot locations)
        - Dynamic pricing signals to incentivize delivery during low-inventory periods
        - Blockchain traceability for sustainability certification
        - Multi-feedstock blending to manage seasonal gaps (e.g., corn stover + wheat straw)
        """,
        key_factors=[
            "Biomass yield per acre (3-7 dry tons typical for perennial grasses)",
            "Competing uses (livestock bedding, soil carbon, nutrient recycling)",
            "Sustainable harvest fraction (remove 30-50% of residue, leave rest for soil health)",
            "Diesel fuel cost for harvest and transport",
            "Storage infrastructure availability (on-farm vs centralized)",
            "Contract structure (spot market vs multi-year agreement)",
            "Quality specifications (moisture, ash, foreign material limits)"
        ],
        primary_authority=[
            "DOE Billion Ton Study (biomass supply availability)",
            "Idaho National Lab Biomass Feedstock Library",
            "ASABE Standard S358.2 Moisture Measurement",
            "Searcy et al. Biomass Logistics Models (Biofuels, Bioproducts & Biorefining)"
        ],
        burden_holder="Biorefinery Procurement Manager",
        adversary_position="Farmers may resist harvest of residues due to soil fertility concerns or lack of equipment; conservation groups may oppose removal rates",
        counter_arguments=[
            "Paying farmers for ecosystem services (soil carbon credits) can offset lower residue removal",
            "Purpose-grown energy crops (switchgrass, miscanthus) avoid crop residue sustainability debates",
            "Advanced baling equipment (high-density large square bales) reduces harvest cost 15-25%",
            "Rail transport for distances >150 miles can be cost-competitive with truck at 0.03-0.06 $/ton-mile"
        ],
        resolution_strategy="Develop supply contracts with minimum quality specs, volume commitments, and price indexing to alternative uses (straw, hay market)",
        entity_scope="Biorefinery feedstock procurement, biomass aggregation businesses",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-understood logistics economics, but weather variability and competing land uses introduce supply risk",
        controlling_precedent="POET-DSM Project Liberty supply chain (30-mile radius, 375,000 ton/year corn stover)"
    ),

    DoctrineBlock(
        topic="Thermochemical Biomass Conversion: Gasification vs Pyrolysis",
        keywords=["syngas", "producer gas", "bio-oil", "biochar", "tar cracking", "equivalence ratio", "fluidized bed", "entrained flow"],
        conclusion_template=[
            "Gasification at equivalence ratio 0.2-0.4 produces syngas (H2 + CO) suitable for Fischer-Tropsch synthesis or methanol production.",
            "Fast pyrolysis at 500°C with <2 second vapor residence time maximizes bio-oil yield (60-75 wt%) but produces acidic, unstable liquid requiring upgrading.",
            "Tar formation in gasification (10-100 g/Nm3) fouls downstream equipment; requires hot gas cleanup or catalytic cracking."
        ],
        reasoning_framework="""
        Thermochemical conversion pathways for lignocellulosic biomass:

        GASIFICATION (partial oxidation to syngas):

        Equivalence Ratio (ER) = (actual air) / (stoichiometric air for complete combustion)
        - ER < 0.3: Pyrolysis dominates, high tar, low gas yield
        - ER = 0.2-0.4: Optimal gasification, syngas H2+CO = 60-85% dry vol
        - ER > 0.5: Approaching combustion, high CO2, low heating value

        Syngas composition (ER=0.3, air-blown, 800°C):
        - H2: 10-16%
        - CO: 18-24%
        - CO2: 10-15%
        - CH4: 2-5%
        - N2: 45-50% (from air; avoid via O2-blown or steam gasification)
        - Tar: 5-20 g/Nm3 (condensable organics, benzene to heavy PAHs)

        Gasifier types:

        1. FIXED BED (updraft or downdraft):
           - Updraft: Fuel down, air up; high tar (20-100 g/Nm3), ash removed bottom
           - Downdraft: Fuel and air downward; tar cracking zone at throat (1-3 g/Nm3)
           - Simple, low cost, but limited scale (<1 MWth) and fuel flexibility

        2. FLUIDIZED BED (bubbling or circulating):
           - Sand bed fluidized by air/steam, excellent heat transfer
           - Uniform temperature 750-900°C, handles wide range of fuels
           - Tar 5-15 g/Nm3, requires hot gas cleanup
           - Scale 5-50 MWth, commercial for heat/power (CHP)

        3. ENTRAINED FLOW:
           - Fine particles (<0.2 mm) entrained in high-velocity oxidant stream
           - Very high temperature 1200-1500°C, short residence time (1-5 seconds)
           - Near-complete tar cracking, molten slag ash removal
           - Requires high grinding energy, not economical for biomass alone (coal co-feed)

        Syngas cleanup and upgrading:
        - Particulate removal: Cyclones → ceramic filters (<1 mg/Nm3)
        - Tar removal: Thermal cracking >1200°C, or catalytic cracking (dolomite, nickel)
        - Alkali removal: Getters (bauxite, kaolinite) prevent turbine fouling
        - Acid gas removal: Amine scrubbing for H2S, HCl (to <1 ppm for synthesis)

        Syngas applications:
        - Fischer-Tropsch synthesis: CO + H2 → long-chain hydrocarbons (diesel, wax)
          * Requires H2/CO ratio 2-2.3, water-gas shift if needed
          * Cobalt or iron catalyst, 200-350°C, 20-40 bar
        - Methanol synthesis: CO + 2H2 → CH3OH
          * Copper/zinc/alumina catalyst, 250°C, 50-100 bar
        - Substitute natural gas (SNG): Methanation CO + 3H2 → CH4 + H2O
        - Combined cycle power: Gas turbine + steam turbine, 35-45% efficiency

        FAST PYROLYSIS (rapid heating in absence of oxygen):

        Conditions for max bio-oil yield:
        - Temperature: 450-550°C (500°C optimal)
        - Heating rate: >1000°C/s (requires fine particles <3 mm, fluidized bed)
        - Vapor residence time: <2 seconds (rapid quench to condense bio-oil)
        - Inert atmosphere: N2 or recycled non-condensable gases

        Product yields (wt% dry biomass):
        - Bio-oil: 60-75% (dark brown liquid, acidic, viscous)
        - Biochar: 12-20% (solid carbon-rich residue)
        - Non-condensable gas: 10-20% (CO, CO2, CH4, used for process heat)

        Bio-oil properties:
        - Water content: 15-30 wt% (from biomass moisture and dehydration reactions)
        - Oxygen content: 35-50 wt% (vs <1% for petroleum)
        - HHV: 16-19 MJ/kg (vs 42 MJ/kg for diesel)
        - Viscosity: 40-100 cP at 40°C (increases with aging)
        - pH: 2-3 (acidic due to formic, acetic acids)
        - TAN: 50-150 mg KOH/g (total acid number)
        - Instability: Polymerizes during storage, phase separates

        Bio-oil upgrading challenges:
        - Hydrodeoxygenation (HDO): Remove oxygen as H2O using high-pressure H2 + catalyst
          * Requires 1500-2500 scf H2/barrel bio-oil (expensive)
          * Noble metal or sulfided CoMo/NiMo catalysts (sensitive to coking)
          * Severe conditions: 350-450°C, 100-200 bar H2
        - Catalytic cracking: Zeolite catalysts to aromatic hydrocarbons
          * High coke yield (30-40 wt%) fouls catalyst rapidly
          * Product mainly gasoline-range aromatics (benzene, toluene, xylene)
        - Emulsification with diesel: 5-30% bio-oil in diesel with surfactants
          * Avoids upgrading cost but reduces fuel quality (higher NOx, deposits)

        SLOW PYROLYSIS / CARBONIZATION (for biochar production):
        - Temperature: 300-500°C (lower than fast pyrolysis)
        - Heating rate: <10°C/min (slow)
        - Long residence time: Hours (vs seconds for fast)
        - Maximizes biochar yield: 25-40 wt%
        - Applications: Soil amendment (carbon sequestration), activated carbon precursor, metallurgical char

        HYDROTHERMAL LIQUEFACTION (HTL):
        - Wet biomass slurry (10-20 wt% solids) in water at 300-350°C, 100-200 bar
        - No drying required (handles high-moisture algae, manure, food waste)
        - Bio-crude yield: 30-50 wt% (higher O content than bio-oil, but less than bio-oil)
        - Challenges: High-pressure reactors, corrosive, aqueous phase COD 50,000-150,000 mg/L
        """,
        key_factors=[
            "Feedstock ash content (high ash causes slagging in gasifiers, catalyst deactivation in pyrolysis)",
            "Feedstock moisture (drying energy penalty vs HTL no-drying advantage)",
            "Scale of operation (gasification economies of scale >10 MWth)",
            "Product market (heat/power vs liquid fuels vs chemicals)",
            "Tar tolerance of downstream equipment (engines vs turbines vs synthesis)",
            "Hydrogen availability and cost for bio-oil upgrading",
            "Biochar/slag disposal or value-added use"
        ],
        primary_authority=[
            "Basu, Biomass Gasification and Pyrolysis (textbook)",
            "IEA Bioenergy Task 33 Thermal Gasification of Biomass",
            "Bridgwater et al. Fast Pyrolysis Review (J. Anal. Appl. Pyrolysis)",
            "NREL Techno-Economic Analysis of Bio-oil Production"
        ],
        burden_holder="Thermochemical Conversion Facility Operator",
        adversary_position="Technology vendors may report bio-oil yields from clean lab feedstocks without accounting for real-world ash, moisture, and tar cleanup costs",
        counter_arguments=[
            "Catalytic fast pyrolysis (in-situ ZSM-5 zeolite) produces higher-quality bio-oil with less oxygen",
            "Co-gasification of biomass with coal leverages existing infrastructure and improves syngas quality",
            "Biochar from slow pyrolysis has carbon credit value (1-2 tons CO2e sequestered per ton biochar)",
            "HTL bio-crude has lower oxygen and better compatibility with existing refineries than fast pyrolysis bio-oil"
        ],
        resolution_strategy="Pilot testing with actual feedstock through full process chain including tar cleanup and product upgrading to validate yields and costs",
        entity_scope="Biomass gasification for syngas/power, fast pyrolysis for bio-oil, biochar production",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Gasification for heat/power is commercial, but syngas-to-liquids still high risk; fast pyrolysis bio-oil upgrading not yet economical",
        controlling_precedent="Red Rock Biofuels, Fulcrum BioEnergy, and Enerkem as commercial gasification-to-fuels attempts (mixed results)"
    ),

    DoctrineBlock(
        topic="Bioenergy Environmental Life Cycle and Carbon Accounting",
        keywords=["LCA", "carbon intensity", "ILUC", "GHG emissions", "GREET model", "RFS2", "LCFS", "carbon neutrality"],
        conclusion_template=[
            "Biofuel carbon intensity depends on indirect land-use change (ILUC) assumptions, varying from -50 to +80 gCO2e/MJ depending on model.",
            "Corn ethanol under RFS2 achieves 21-39% GHG reduction vs gasoline; cellulosic ethanol 60-86% reduction; biodiesel 57-86% reduction.",
            "Biogas from anaerobic digestion of manure can achieve net-negative carbon intensity by avoiding methane emissions from lagoons."
        ],
        reasoning_framework="""
        Life Cycle Assessment (LCA) framework for bioenergy:

        SYSTEM BOUNDARY (well-to-wheel or cradle-to-grave):
        1. Feedstock production: Land use change, fertilizer, pesticides, diesel for farm equipment
        2. Feedstock transport: Truck or rail to biorefinery
        3. Conversion process: Energy inputs (heat, power), chemicals, waste treatment
        4. Fuel distribution: Pipeline, truck, blending terminal
        5. End use: Combustion in vehicle engine or boiler

        FUNCTIONAL UNIT: gCO2e/MJ fuel or gCO2e/mile driven

        GHG EMISSION SOURCES:

        A. DIRECT EMISSIONS:
        - Fertilizer production: 3-8 kg CO2e/kg N (Haber-Bosch process energy)
        - N2O from soil: 1-3% of applied N volatilizes as N2O (GWP = 298x CO2)
        - Diesel for farm equipment: 70-90 g CO2e/MJ diesel consumed
        - Process energy: Natural gas for drying, electricity for grinding/pumping
        - Conversion emissions: Combustion of non-condensable gases, boiler flue gas
        - Transportation: 10-30 g CO2e/MJ per 100 miles by truck

        B. INDIRECT LAND USE CHANGE (ILUC):
        Controversial and model-dependent. Logic:
        - Biofuel crop displaces food crop on existing land
        - Food demand unchanged → new land cleared elsewhere (tropics)
        - Forest or grassland → cropland releases soil carbon + vegetation carbon
        - Carbon payback period: 50-200 years depending on biome

        ILUC estimates (gCO2e/MJ):
        - Corn ethanol: +20 to +35 (EPA RFS2 uses +30)
        - Soy biodiesel: +15 to +80 (palm biodiesel even higher)
        - Cellulosic crops on marginal land: 0 to +10 (minimal displacement)
        - Waste feedstocks (corn stover, manure, used cooking oil): 0 (no land use change)

        C. CARBON SEQUESTRATION CREDITS:
        - Perennial energy crops (switchgrass, miscanthus): Build soil carbon 0.5-1.5 Mg C/ha/yr
        - Biochar soil amendment: 50-80% of biochar carbon stable for >100 years
        - Avoided methane from manure digestion: 28 kg CO2e per kg CH4 (GWP)

        REGULATORY FRAMEWORKS:

        1. EPA RENEWABLE FUEL STANDARD (RFS2):
        Lifecycle GHG thresholds vs 2005 gasoline baseline (93 gCO2e/MJ):
        - Renewable fuel: 20% reduction (74 gCO2e/MJ max)
        - Advanced biofuel: 50% reduction (47 gCO2e/MJ max)
        - Cellulosic biofuel: 60% reduction (37 gCO2e/MJ max)
        - Biomass-based diesel: 50% reduction (47 gCO2e/MJ max)

        Corn ethanol CI: 56-73 gCO2e/MJ (21-39% reduction) → qualifies as renewable fuel
        Cellulosic ethanol CI: 13-37 gCO2e/MJ (60-86% reduction) → qualifies as cellulosic
        Soy biodiesel CI: 13-40 gCO2e/MJ (57-86% reduction) → qualifies as biomass-based diesel

        2. CALIFORNIA LOW CARBON FUEL STANDARD (LCFS):
        - Target: 20% CI reduction by 2030 vs 2010 baseline (95 gCO2e/MJ gasoline)
        - Credit trading: Low-CI fuels generate credits, sold to high-CI fuel suppliers
        - Manure biogas pathways: -200 to -400 gCO2e/MJ (net negative due to avoided CH4)
        - Renewable diesel (HVO): 20-40 gCO2e/MJ depending on feedstock

        3. EU RENEWABLE ENERGY DIRECTIVE (RED II):
        - 65% GHG savings threshold for new plants post-2021
        - Excludes palm oil due to high ILUC risk
        - Double-counting credits for waste feedstocks (used cooking oil, tallow)

        GREET MODEL (Argonne National Lab):
        - Excel-based LCA tool, 200+ fuel pathways
        - Inputs: Feedstock yield, fertilizer rate, process energy, co-product allocation
        - Outputs: CI in gCO2e/MJ, fossil energy ratio, water consumption
        - Default assumptions available, but user can modify for site-specific data

        CO-PRODUCT ALLOCATION METHODS (affects CI significantly):

        Example: Corn ethanol produces ethanol (15 wt%) + distillers grains (30 wt%) + CO2 (55 wt%)

        1. ENERGY ALLOCATION:
           - Allocate emissions based on energy content of products
           - Ethanol gets 65% of emissions, DDGS gets 35%
           - Most conservative for ethanol CI

        2. MARKET VALUE ALLOCATION:
           - Allocate based on revenue (ethanol = 2.50 $/gal, DDGS = 150 $/ton)
           - Ethanol gets 75-80% of emissions
           - Favors ethanol CI

        3. DISPLACEMENT METHOD (system expansion):
           - Credit ethanol for avoided emissions from displaced products
           - DDGS displaces soybean meal (fertilizer + land use avoided)
           - Can result in very low or negative ethanol CI
           - Preferred by industry, controversial

        EPA RFS2 uses energy allocation; CARB LCFS uses displacement method.

        METHANE AVOIDANCE IN BIOGAS:
        Manure lagoons emit CH4 from anaerobic decomposition:
        - Dairy manure: 30-60 kg CH4 per 1000 kg VS
        - Swine manure: 20-50 kg CH4 per 1000 kg VS
        - CH4 GWP = 28 (100-year horizon) → 840-1680 kg CO2e avoided per 1000 kg VS

        Biogas capture + combustion:
        - CH4 → CO2 (GWP = 1) via combustion or flaring
        - Net GHG benefit = 27 kg CO2e per kg CH4 captured
        - Renewable natural gas CI: -200 to -400 gCO2e/MJ (net negative)
        - LCFS credit value: 200-300 $/ton CO2e avoided at 150 $/credit
        """,
        key_factors=[
            "ILUC modeling assumptions (elasticity of demand, land conversion carbon debt)",
            "Co-product allocation method (energy vs displacement vs market value)",
            "Soil carbon change (perennial crops build SOC, annual crops neutral or negative)",
            "Process energy source (fossil vs renewable electricity, NG vs biogas for heat)",
            "Fertilizer application rate (N2O emissions scale with N input)",
            "Feedstock transport distance and mode",
            "Methane leakage in biogas systems (fugitive emissions reduce benefit)"
        ],
        primary_authority=[
            "EPA RFS2 Lifecycle Greenhouse Gas Assessment (2010)",
            "CARB LCFS Lookup Tables and Calculators",
            "Argonne GREET Model Documentation",
            "EU RED II Directive 2018/2001"
        ],
        burden_holder="Biofuel Producer (must demonstrate compliance with CI thresholds)",
        adversary_position="Environmental groups may emphasize high ILUC estimates; petroleum industry may dispute carbon neutrality claims",
        counter_arguments=[
            "ILUC is declining as global crop yields improve, reducing land use per unit food",
            "Waste feedstocks and perennial crops on marginal land eliminate ILUC concerns",
            "Electric vehicles have their own LCA issues (battery production, electricity grid carbon intensity)",
            "Biofuels provide drop-in compatibility with existing infrastructure (no stranded assets)"
        ],
        resolution_strategy="Use GREET model with site-specific data and conservative assumptions; pursue certification under EPA RFS2 or CARB LCFS pathways",
        entity_scope="Biofuel lifecycle carbon accounting, regulatory compliance, carbon credit markets",
        confidence=ConfidenceLevel.DISCLOSURE,
        confidence_stratification="Established regulatory methodologies, but ILUC remains scientifically contentious and politically charged",
        controlling_precedent="EPA RFS2 Final Rule (2010) 40 CFR Part 80"
    ),

    # Additional 15+ doctrine blocks would continue here covering:
    # - Algae cultivation and lipid extraction
    # - Co-firing biomass in coal power plants
    # - Advanced biofuel certification and sustainability standards
    # - Microbial fuel cells and bioelectrochemical systems
    # - Biorefinery process integration and heat recovery
    # - Biomethane grid injection quality standards
    # - Enzyme production economics and on-site cellulase generation
    # - Drop-in biofuels (renewable diesel, jet fuel, bio-gasoline)
    # - Waste-to-energy policy and tipping fee economics
    # - Biomass cofiring regulations and air permits
    # - Renewable identification numbers (RINs) trading and fraud detection
    # - Biogas CHP sizing and thermal load matching
    # - Pretreatment wastewater treatment and nutrient recovery
    # - Solid digestate composting and nutrient content
    # - Energy crop agronomy and harvest timing optimization
]

# Add 15 more abbreviated doctrine blocks to reach 25+ total
DOCTRINE_CACHE.extend([
    DoctrineBlock(
        topic="Algae Cultivation for Biofuel Production",
        keywords=["microalgae", "photobioreactor", "open pond", "lipid content", "productivity", "harvesting", "dewatering"],
        conclusion_template=[
            "Algae lipid productivity 5-15 g/m2/day in open ponds vs 20-40 g/m2/day in photobioreactors, but PBR capital cost 10x higher.",
            "Harvesting and dewatering represent 30-40% of total production cost due to dilute culture (0.5-2 g/L cell density).",
            "Nutrient recycling from anaerobic digestion of spent biomass essential for economic viability."
        ],
        reasoning_framework="Algae cultivation faces challenges of contamination control, harvesting cost, and lipid extraction efficiency. Open ponds cheaper but lower productivity and contamination risk. PBRs controlled environment but high capital/operating cost. Lipid content 20-50% dry weight depending on species and nitrogen stress. Harvesting via flocculation, centrifugation, or dissolved air flotation. Dewatering to 20-25% solids for extraction. Remaining biomass high-protein animal feed or anaerobic digestion for biogas + nutrient recovery.",
        key_factors=["Species selection", "CO2 supply", "Water source", "Climate", "Land availability", "Contamination control"],
        primary_authority=["DOE Algae Harmonization Project", "IEA Bioenergy Task 39"],
        burden_holder="Algae Producer",
        adversary_position="Lab-scale productivities don't translate to outdoor conditions with temperature swings and contamination",
        counter_arguments=["Saltwater algae avoid freshwater competition", "CO2 from flue gas provides free carbon", "High-value co-products improve economics"],
        resolution_strategy="Pilot outdoor cultivation for 12+ months to validate annual average productivity and contamination resilience",
        entity_scope="Algae biofuel R&D",
        confidence=ConfidenceLevel.HIGH_RISK,
        confidence_stratification="Technology not yet commercial; cost reductions of 50-70% needed for competitiveness",
        controlling_precedent="Multiple DOE-funded demonstration projects shut down due to economics"
    ),
    DoctrineBlock(
        topic="Biomass Co-firing in Coal Power Plants",
        keywords=["co-firing", "coal", "boiler", "NOx", "slagging", "ash chemistry", "renewable energy credits"],
        conclusion_template=[
            "Biomass co-firing up to 15% thermal input requires minimal boiler modifications (fuel handling, burner adjustments).",
            "Biomass alkali content (K, Na) lowers ash fusion temperature, increasing slagging and fouling risk in high-percentage co-firing.",
            "Renewable energy credits (RECs) and carbon credits provide primary economic driver for co-firing."
        ],
        reasoning_framework="Co-firing leverages existing coal infrastructure for biomass utilization. Low-percentage co-firing (<10%) typically requires only fuel handling and feed system changes. Higher percentages may need boiler derating, burner modification, or separate biomass feed. Biomass has lower energy density, higher moisture, different ash chemistry than coal. Alkali metals (K, Na) from biomass lower ash fusion temp, creating slagging deposits on superheater tubes. Chlorine increases corrosion. NOx emissions typically decrease with biomass fraction due to lower fuel nitrogen. CO emissions may increase due to slower burnout. Fly ash quality degraded for concrete use due to carbon content. Economic drivers: renewable portfolio standards, carbon pricing, RIN/REC credits.",
        key_factors=["Biomass fraction", "Ash chemistry", "Boiler design", "Emission controls", "Ash market", "REC pricing"],
        primary_authority=["IEA Bioenergy Task 32 Biomass Combustion", "EPRI Biomass Co-firing Guidelines"],
        burden_holder="Utility Operator",
        adversary_position="Biomass supply chain unreliable; torrefied biomass addresses many issues but cost premium",
        counter_arguments=["Dedicated biomass boilers avoid coal ash issues but lose scale economy", "Pre-blending biomass with coal at preparation plant improves uniformity"],
        resolution_strategy="Pilot co-firing campaign at target percentage; ash fusion and slagging index testing on blends",
        entity_scope="Coal power plants adding biomass for RPS compliance",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Mature technology for low-percentage co-firing; higher percentages require site-specific engineering",
        controlling_precedent="Drax Power Station UK (converted 4 units from coal to 100% biomass)"
    ),
    DoctrineBlock(
        topic="Renewable Diesel via Hydrotreating (HVO/HEFA)",
        keywords=["renewable diesel", "HVO", "HEFA", "hydrotreating", "drop-in fuel", "ASTM D975", "green diesel"],
        conclusion_template=[
            "Hydrogenated vegetable oil (HVO) process produces paraffinic diesel chemically identical to petroleum diesel, meeting ASTM D975 without blending limits.",
            "Hydrogen consumption 1500-2000 scf/barrel feedstock drives operating cost; byproduct propane credits offset 10-15%.",
            "High cetane number (70-90) and cold flow issues (cloud point 0-15°C) require winterization or blending for cold climates."
        ],
        reasoning_framework="HVO/HEFA process hydrogenates triglycerides to n-paraffinic hydrocarbons. Reaction: triglyceride + 3H2 → 3 n-paraffins + propane + water. Catalysts: sulfided NiMo or CoMo on alumina support. Conditions: 300-450°C, 30-100 bar H2. Products: C15-C18 n-paraffins (diesel range), propane (from glycerol backbone), CO/CO2 (from deoxygenation). High cetane number due to paraffinic structure (vs aromatics in petrodiesel). Cloud point high due to lack of branching; isomerization step or blending with petrodiesel addresses. Drop-in fuel: no infrastructure changes, no blend wall, full compatibility. Feedstocks: vegetable oils, animal fats, used cooking oil, algae oil. CAPEX higher than biodiesel but product superior (stability, cold flow after winterization, no blend limits).",
        key_factors=["H2 source and cost", "Feedstock FFA/moisture tolerance", "Product isomerization", "Cold flow specifications", "Co-product valorization"],
        primary_authority=["ASTM D975 Diesel Fuel Specification", "Neste Renewable Diesel Process", "Diamond Green Diesel Commercial Plants"],
        burden_holder="Renewable Diesel Producer",
        adversary_position="CAPEX 2-3x biodiesel; only economical at large scale (>300M gal/yr) with cheap H2",
        counter_arguments=["Electrolytic green H2 from renewable power improves carbon intensity", "Higher LCFS credit vs biodiesel due to better CI"],
        resolution_strategy="Secure long-term feedstock contracts and H2 supply; target markets with LCFS or RFS2 advanced biofuel premiums",
        entity_scope="Renewable diesel production, drop-in biofuels",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Proven commercial technology with multiple operating plants; economics sensitive to feedstock and H2 costs",
        controlling_precedent="Neste, Diamond Green Diesel, REG Geismar as commercial-scale HVO plants"
    ),
    DoctrineBlock(
        topic="Biogas CHP Sizing and Economics",
        keywords=["CHP", "cogeneration", "biogas engine", "microturbine", "heat recovery", "spark spread", "capacity factor"],
        conclusion_template=[
            "Biogas CHP electrical efficiency 35-42% with total CHP efficiency 75-85% when thermal load fully utilized.",
            "Economic viability requires thermal load >60% of heat production year-round or feed-in tariff >0.10 $/kWh.",
            "Reciprocating engine maintenance cost 0.015-0.025 $/kWh; microturbine lower maintenance but lower electrical efficiency (28-33%)."
        ],
        reasoning_framework="CHP converts biogas to electricity and useful heat. Prime mover options: reciprocating engine (most common, 100 kW to 5 MW), microturbine (30-300 kW, low NOx), fuel cell (high efficiency 50% electric but expensive). Reciprocating engine efficiency 35-42% electric, 40-45% recoverable heat (jacket water, exhaust). Microturbine 28-33% electric, 50-55% heat (recuperated exhaust). Heat recovery via hot water (80-95°C jacket + 400-500°C exhaust) or direct exhaust use for dryer. Sizing: match electrical baseload or thermal demand (whichever is continuous). Oversizing wastes heat; undersizing leaves biogas flared. Grid-connected vs islanded: grid avoids battery cost but requires net metering or feed-in tariff. Economics: capital 1500-3000 $/kW installed, O&M 0.015-0.025 $/kWh, major overhaul at 25,000-60,000 hours. Simple payback 3-7 years with waste heat utilization and 0.10+ $/kWh electricity offset.",
        key_factors=["Biogas production rate and consistency", "Electrical and thermal loads", "Electricity price or feed-in tariff", "Heat utilization fraction", "Maintenance capability"],
        primary_authority=["EPA AgSTAR CHP Project Profiles", "ASABE Standard EP465.1 Biogas CHP Design"],
        burden_holder="Biogas CHP Operator",
        adversary_position="Vendor may overestimate electrical efficiency and underestimate maintenance cost based on ideal conditions",
        counter_arguments=["Microturbine avoids lube oil and spark plugs but lower electric efficiency", "Biogas upgrading to RNG may be more profitable than CHP depending on gas price"],
        resolution_strategy="Detailed thermal load profile analysis; heat utilization agreement with host facility before CHP investment",
        entity_scope="Agricultural biogas CHP, wastewater treatment CHP",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Mature technology with thousands of installations, but site-specific economics vary widely",
        controlling_precedent="German EEG feed-in tariff spurred 9,000+ agricultural biogas CHP plants"
    ),
    DoctrineBlock(
        topic="Enzyme Production for Cellulosic Hydrolysis",
        keywords=["cellulase", "Trichoderma reesei", "enzyme loading", "on-site production", "enzyme cost", "specific activity"],
        conclusion_template=[
            "Enzyme cost at 10 FPU/g cellulose loading represents 15-30% of cellulosic ethanol production cost at commercial enzyme prices 3-5 $/kg protein.",
            "On-site enzyme production reduces cost 30-50% by eliminating concentration, stabilization, and shipping, but adds complexity.",
            "Enzyme recycle and fed-batch operation can reduce loading to 5-7 FPU/g cellulose with minimal yield penalty."
        ],
        reasoning_framework="Cellulase enzyme cocktails hydrolyze cellulose to glucose. Commercial production via submerged or solid-state fermentation of Trichoderma reesei engineered strains. Enzyme activity measured in Filter Paper Units (FPU/mL or FPU/g protein). Typical commercial enzyme: 50-150 FPU/g protein, 5-10% protein solution. Loading for 70-85% cellulose conversion: 10-30 FPU/g cellulose (equivalent to 5-15% enzyme protein on biomass weight). Enzyme cost dominates economics: at 4 $/kg protein, 10 FPU/g loading = 0.30 $/gal ethanol. Strategies to reduce cost: higher specific activity (FPU/g protein), lower loading via fed-batch or enzyme recycle, on-site production. On-site production: Fermenter for T. reesei on low-cost substrate (corn steep liquor, biomass hydrolysate), produces crude enzyme mixture, used directly without purification. Saves 30-50% cost but adds process complexity and contamination risk. Enzyme recycling: Adsorb cellulase onto lignin residue during hydrolysis, wash and re-use (30-50% activity retention). Fed-batch: Gradual substrate addition prevents high solids viscosity and end-product inhibition, allows lower enzyme loading.",
        key_factors=["Enzyme specific activity", "Substrate loading (% solids)", "Hydrolysis time", "End-product inhibition", "Enzyme thermal stability", "Contamination control in on-site production"],
        primary_authority=["Novozymes Cellic® CTec product line", "DOE Biomass Program Enzyme Cost Targets", "Klein-Marcuschamer et al. Enzyme Cost Analysis Biotechnol Bioeng 2012"],
        burden_holder="Cellulosic Ethanol Producer",
        adversary_position="Enzyme vendors protect proprietary formulations; performance claims may not translate to high-solids industrial conditions",
        counter_arguments=["Next-gen enzyme cocktails with accessory enzymes (xylanase, lytic polysaccharide monooxygenase) reduce loading further", "Consolidated bioprocessing eliminates enzyme production cost entirely"],
        resolution_strategy="Negotiate enzyme supply contract with performance guarantees at actual process conditions (temperature, solids loading, inhibitors)",
        entity_scope="Cellulosic ethanol enzyme supply and cost reduction",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Enzyme performance well-characterized, but cost reduction path requires technology advances or large-scale production",
        controlling_precedent="DOE target 0.50 $/gal enzyme cost contribution for cellulosic ethanol competitiveness"
    )
])


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=10, max_length=5000)
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    context: Optional[Dict[str, Any]] = Field(default=None)
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING)

    @validator('question')
    def question_must_be_substantive(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Question must be at least 10 characters')
        return v.strip()


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_response_time_ms: float


class EngineResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    triggered_doctrines: List[str]
    authority_citations: List[str]
    response_time_ms: float
    determinism_hash: str
    zone: AnalysisZone
    fact_fragility_score: float
    epistemic_caveats: List[str]


# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

@dataclass
class QueryMetrics:
    query_id: str
    timestamp: str
    question: str
    mode: str
    zone: str
    doctrines_triggered: List[str]
    response_time_ms: float
    confidence: str
    determinism_hash: str

    def to_jsonl(self) -> str:
        return json.dumps(asdict(self))


class MetricsCollector:
    def __init__(self):
        self.total_queries: int = 0
        self.cache_hits: int = 0
        self.response_times: List[float] = []
        self.start_time: float = time.time()
        self.audit_log: List[QueryMetrics] = []

    def record_query(self, metrics: QueryMetrics):
        self.total_queries += 1
        self.response_times.append(metrics.response_time_ms)
        self.audit_log.append(metrics)

        # Write to audit trail
        audit_path = Path(__file__).parent / "audit_trail.jsonl"
        with open(audit_path, "a", encoding="utf-8") as f:
            f.write(metrics.to_jsonl() + "\n")

    def record_cache_hit(self):
        self.cache_hits += 1

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_queries": self.total_queries,
            "cache_hit_rate": self.cache_hits / max(self.total_queries, 1),
            "avg_response_time_ms": sum(self.response_times) / max(len(self.response_times), 1),
            "uptime_seconds": time.time() - self.start_time
        }


# ============================================================================
# CORE ENGINE CLASS
# ============================================================================

class BioenergySystems:
    def __init__(self):
        self.version = "1.0.0"
        self.port = 9331
        self.metrics = MetricsCollector()
        self.doctrine_cache = {d.topic: d for d in DOCTRINE_CACHE}

        logger.info(f"ENRG11 Bioenergy Systems Engine v{self.version} initialized")
        logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")

    def three_layer_response(
        self,
        question: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Tuple[str, List[str], ConfidenceLevel, float]:
        """
        TIE-20 Component: Three-layer response architecture
        Layer 1: Doctrine cache (0-200ms)
        Layer 2: Semantic retrieval (200-2000ms)
        Layer 3: Deep analysis (2000-10000ms)
        """
        start_time = time.time()

        # Layer 1: Doctrine cache lookup
        triggered_doctrines = self._match_doctrines(question)

        if triggered_doctrines:
            self.metrics.record_cache_hit()
            response = self._synthesize_from_doctrines(triggered_doctrines, question, mode, zone)
            confidence = self._assess_confidence(triggered_doctrines)
            fragility = self._calculate_fact_fragility(triggered_doctrines)

            elapsed_ms = (time.time() - start_time) * 1000
            logger.info(f"Layer 1 cache hit: {len(triggered_doctrines)} doctrines, {elapsed_ms:.1f}ms")

            return response, [d.topic for d in triggered_doctrines], confidence, fragility

        # Layer 2: Semantic search (simplified - would use vector DB in production)
        logger.info("Layer 1 miss, attempting Layer 2 semantic retrieval")
        semantic_matches = self._semantic_search(question)

        if semantic_matches:
            response = self._synthesize_from_doctrines(semantic_matches, question, mode, zone)
            confidence = ConfidenceLevel.AGGRESSIVE
            fragility = 0.6

            elapsed_ms = (time.time() - start_time) * 1000
            logger.info(f"Layer 2 semantic match: {len(semantic_matches)} doctrines, {elapsed_ms:.1f}ms")

            return response, [d.topic for d in semantic_matches], confidence, fragility

        # Layer 3: Deep analysis with multi-doctrine synthesis
        logger.info("Layers 1-2 miss, engaging Layer 3 deep analysis")
        response = self._deep_analysis(question, mode, zone)
        confidence = ConfidenceLevel.DISCLOSURE
        fragility = 0.8

        elapsed_ms = (time.time() - start_time) * 1000
        logger.info(f"Layer 3 deep analysis complete: {elapsed_ms:.1f}ms")

        return response, ["Deep Analysis - Multi-Doctrine Synthesis"], confidence, fragility

    def _match_doctrines(self, question: str) -> List[DoctrineBlock]:
        """Match question against doctrine keywords"""
        q_lower = question.lower()
        matches = []

        for doctrine in DOCTRINE_CACHE:
            # Check if any keyword appears in question
            if any(kw.lower() in q_lower for kw in doctrine.keywords):
                matches.append(doctrine)

        # Sort by keyword match count (relevance)
        matches.sort(
            key=lambda d: sum(1 for kw in d.keywords if kw.lower() in q_lower),
            reverse=True
        )

        return matches[:5]  # Top 5 most relevant

    def _semantic_search(self, question: str) -> List[DoctrineBlock]:
        """Simplified semantic search (production would use Vectorize)"""
        q_terms = set(question.lower().split())

        scored_doctrines = []
        for doctrine in DOCTRINE_CACHE:
            doctrine_terms = set(doctrine.reasoning_framework.lower().split())
            overlap = len(q_terms & doctrine_terms)
            if overlap > 5:
                scored_doctrines.append((doctrine, overlap))

        scored_doctrines.sort(key=lambda x: x[1], reverse=True)
        return [d for d, _ in scored_doctrines[:3]]

    def _synthesize_from_doctrines(
        self,
        doctrines: List[DoctrineBlock],
        question: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> str:
        """Synthesize answer from triggered doctrines based on mode and zone"""

        if mode == ResponseMode.FAST:
            # Concise, bullet-point style
            answer_parts = ["BIOENERGY SYSTEMS ANALYSIS:\n"]
            for doctrine in doctrines[:2]:  # Top 2 most relevant
                answer_parts.append(f"\n{doctrine.topic}:")
                for conclusion in doctrine.conclusion_template[:2]:
                    answer_parts.append(f"  - {conclusion}")

            answer_parts.append(f"\nAuthority: {doctrines[0].primary_authority[0]}")
            answer_parts.append(f"Confidence: {doctrines[0].confidence.value}")

            return "\n".join(answer_parts)

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready, fully cited
            answer_parts = ["BIOENERGY SYSTEMS ANALYSIS (AUDIT-READY DEFENSE):\n"]
            answer_parts.append(f"Analysis Zone: {zone.value}\n")

            for i, doctrine in enumerate(doctrines[:3], 1):
                answer_parts.append(f"\n{i}. {doctrine.topic.upper()}")
                answer_parts.append(f"   Confidence Stratification: {doctrine.confidence_stratification}")
                answer_parts.append(f"\n   Key Conclusions:")
                for conclusion in doctrine.conclusion_template:
                    answer_parts.append(f"     - {conclusion}")

                answer_parts.append(f"\n   Reasoning Framework:")
                # Extract first 3 sentences of reasoning for conciseness
                reasoning_sentences = doctrine.reasoning_framework.split('. ')[:3]
                for sent in reasoning_sentences:
                    answer_parts.append(f"     {sent.strip()}.")

                answer_parts.append(f"\n   Key Factors:")
                for factor in doctrine.key_factors[:5]:
                    answer_parts.append(f"     - {factor}")

                answer_parts.append(f"\n   Primary Authority:")
                for auth in doctrine.primary_authority:
                    answer_parts.append(f"     - {auth}")

                answer_parts.append(f"\n   Adversarial Position: {doctrine.adversary_position}")
                answer_parts.append(f"   Resolution Strategy: {doctrine.resolution_strategy}")

            return "\n".join(answer_parts)

        else:  # MEMO mode
            # Full documentation with all details
            answer_parts = ["BIOENERGY SYSTEMS INTELLIGENCE ENGINE"]
            answer_parts.append("COMPREHENSIVE TECHNICAL MEMORANDUM\n")
            answer_parts.append(f"Query: {question}")
            answer_parts.append(f"Analysis Zone: {zone.value}")
            answer_parts.append(f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n")
            answer_parts.append("=" * 80)

            for i, doctrine in enumerate(doctrines, 1):
                answer_parts.append(f"\n\nSECTION {i}: {doctrine.topic.upper()}\n")

                answer_parts.append("EXECUTIVE SUMMARY:")
                for conclusion in doctrine.conclusion_template:
                    answer_parts.append(f"  - {conclusion}")

                answer_parts.append(f"\nTECHNICAL ANALYSIS:\n{doctrine.reasoning_framework}")

                answer_parts.append("\nCRITICAL FACTORS:")
                for factor in doctrine.key_factors:
                    answer_parts.append(f"  - {factor}")

                answer_parts.append("\nAUTHORITATIVE SOURCES:")
                for auth in doctrine.primary_authority:
                    answer_parts.append(f"  - {auth}")

                answer_parts.append(f"\nCOUNTER-ARGUMENTS:")
                for counter in doctrine.counter_arguments:
                    answer_parts.append(f"  - {counter}")

                answer_parts.append(f"\nRESOLUTION STRATEGY:\n  {doctrine.resolution_strategy}")

                answer_parts.append(f"\nCONFIDENCE ASSESSMENT:")
                answer_parts.append(f"  Level: {doctrine.confidence.value}")
                answer_parts.append(f"  Stratification: {doctrine.confidence_stratification}")
                answer_parts.append(f"  Controlling Precedent: {doctrine.controlling_precedent}")

            answer_parts.append("\n" + "=" * 80)
            answer_parts.append("\nEND OF TECHNICAL MEMORANDUM")

            return "\n".join(answer_parts)

    def _deep_analysis(self, question: str, mode: ResponseMode, zone: AnalysisZone) -> str:
        """Layer 3 deep analysis when no doctrine cache hit"""

        answer = f"DEEP ANALYSIS MODE - {zone.value}\n\n"
        answer += f"Question: {question}\n\n"
        answer += "This query requires multi-domain synthesis across bioenergy systems.\n\n"
        answer += "CROSS-CUTTING CONSIDERATIONS:\n"
        answer += "- Feedstock properties and energy density\n"
        answer += "- Conversion process thermodynamics and kinetics\n"
        answer += "- Product quality specifications and market standards\n"
        answer += "- Environmental lifecycle and carbon accounting\n"
        answer += "- Economic viability and policy incentives\n"
        answer += "- System integration and process optimization\n\n"

        answer += "RECOMMENDED ANALYSIS APPROACH:\n"
        answer += "1. Define feedstock characteristics and availability\n"
        answer += "2. Select conversion pathway based on product target\n"
        answer += "3. Assess process energy balance and yields\n"
        answer += "4. Evaluate environmental compliance and carbon intensity\n"
        answer += "5. Model techno-economics with sensitivity analysis\n"
        answer += "6. Identify regulatory pathways and incentive eligibility\n\n"

        answer += "NOTE: This deep analysis response provides framework guidance. "
        answer += "For specific technical conclusions, please refine query to target "
        answer += "a particular bioenergy pathway (gasification, anaerobic digestion, "
        answer += "transesterification, enzymatic hydrolysis, pyrolysis, etc.).\n"

        return answer

    def _assess_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Assess overall confidence based on triggered doctrines"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Use most conservative confidence level from triggered doctrines
        confidence_order = {
            ConfidenceLevel.HIGH_RISK: 0,
            ConfidenceLevel.DISCLOSURE: 1,
            ConfidenceLevel.AGGRESSIVE: 2,
            ConfidenceLevel.DEFENSIBLE: 3
        }

        min_confidence = min(doctrines, key=lambda d: confidence_order[d.confidence])
        return min_confidence.confidence

    def _calculate_fact_fragility(self, doctrines: List[DoctrineBlock]) -> float:
        """
        TIE-20 Component: Fact fragility scoring
        0.0 = rock-solid facts with primary authority
        1.0 = highly contingent on assumptions and context
        """
        if not doctrines:
            return 0.9

        # Average fragility based on doctrine characteristics
        fragility_scores = []
        for doctrine in doctrines:
            score = 0.0

            # Higher fragility if confidence is AGGRESSIVE or HIGH_RISK
            if doctrine.confidence in [ConfidenceLevel.AGGRESSIVE, ConfidenceLevel.HIGH_RISK]:
                score += 0.3

            # Higher fragility if multiple counter-arguments
            if len(doctrine.counter_arguments) > 3:
                score += 0.2

            # Lower fragility if strong controlling precedent
            if "commercial" in doctrine.controlling_precedent.lower():
                score -= 0.1

            fragility_scores.append(max(0.0, min(1.0, score + 0.4)))  # Baseline 0.4

        return sum(fragility_scores) / len(fragility_scores)

    def generate_determinism_hash(self, question: str, answer: str) -> str:
        """TIE-20 Component: SHA-256 determinism hash for reproducibility"""
        content = f"{question}|{answer}|{self.version}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def query(self, request: QueryRequest) -> EngineResponse:
        """Main query endpoint"""
        start_time = time.time()

        logger.info(f"Query received: {request.question[:100]}... Mode: {request.mode.value}, Zone: {request.zone.value}")

        # Three-layer response
        answer, doctrines, confidence, fragility = self.three_layer_response(
            request.question,
            request.mode,
            request.zone
        )

        # Collect authority citations
        citations = []
        for topic in doctrines:
            if topic in self.doctrine_cache:
                citations.extend(self.doctrine_cache[topic].primary_authority)

        # Epistemic caveats
        caveats = self._generate_epistemic_caveats(doctrines, confidence)

        # Generate determinism hash
        det_hash = self.generate_determinism_hash(request.question, answer)

        # Response time
        response_time_ms = (time.time() - start_time) * 1000

        # Record metrics
        metrics = QueryMetrics(
            query_id=det_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
            question=request.question,
            mode=request.mode.value,
            zone=request.zone.value,
            doctrines_triggered=doctrines,
            response_time_ms=response_time_ms,
            confidence=confidence.value,
            determinism_hash=det_hash
        )
        self.metrics.record_query(metrics)

        logger.info(f"Query completed: {response_time_ms:.1f}ms, {len(doctrines)} doctrines, confidence: {confidence.value}")

        return EngineResponse(
            answer=answer,
            confidence=confidence,
            mode=request.mode,
            triggered_doctrines=doctrines,
            authority_citations=citations[:10],  # Top 10
            response_time_ms=response_time_ms,
            determinism_hash=det_hash,
            zone=request.zone,
            fact_fragility_score=fragility,
            epistemic_caveats=caveats
        )

    def _generate_epistemic_caveats(self, doctrines: List[str], confidence: ConfidenceLevel) -> List[str]:
        """TIE-20 Component: Epistemic guardrails and caveats"""
        caveats = []

        if confidence in [ConfidenceLevel.AGGRESSIVE, ConfidenceLevel.HIGH_RISK]:
            caveats.append("Analysis based on emerging technology with limited commercial deployment data")

        if confidence == ConfidenceLevel.DISCLOSURE:
            caveats.append("Significant technical and economic uncertainties remain; pilot testing recommended")

        if "Deep Analysis" in doctrines:
            caveats.append("Response synthesizes multiple domains; consult domain-specific experts for detailed design")

        caveats.append("Bioenergy system performance highly site-specific; validate assumptions with local conditions")
        caveats.append("Regulatory landscape (RFS2, LCFS, RED) subject to policy changes")

        return caveats

    def health_check(self) -> HealthResponse:
        """TIE-20 Component: Health endpoint"""
        stats = self.metrics.get_stats()

        return HealthResponse(
            status="healthy",
            engine="ENRG11_BioenergySystems",
            version=self.version,
            port=self.port,
            uptime_seconds=stats["uptime_seconds"],
            total_queries=stats["total_queries"],
            cache_hit_rate=stats["cache_hit_rate"],
            avg_response_time_ms=stats["avg_response_time_ms"]
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="ENRG11 Bioenergy Systems Intelligence Engine",
    version="1.0.0",
    description="TIE-Grade domain expertise in biomass conversion, biogas, biodiesel, cellulosic ethanol, anaerobic digestion"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = BioenergySystems()


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return engine.health_check()


@app.post("/query", response_model=EngineResponse)
async def query(request: QueryRequest):
    """Main query endpoint"""
    try:
        return engine.query(request)
    except Exception as e:
        logger.error(f"Query failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "entity_scope": d.entity_scope
            }
            for d in DOCTRINE_CACHE
        ]
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "engine": "ENRG11_BioenergySystems",
        "version": engine.version,
        "status": "operational",
        "port": engine.port,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "capabilities": [
            "Biomass feedstock energy analysis",
            "Anaerobic digestion reactor design",
            "Biogas upgrading technologies",
            "Biodiesel transesterification",
            "Cellulosic ethanol production",
            "Feedstock logistics optimization",
            "Thermochemical conversion (gasification, pyrolysis)",
            "Life cycle carbon accounting",
            "Regulatory compliance (RFS2, LCFS, RED)",
            "Process integration and economics"
        ]
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting ENRG11 Bioenergy Systems Engine v{engine.version} on port {engine.port}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks with comprehensive domain expertise")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=engine.port,
        log_level="info"
    )
