"""
DRL09 Formation Evaluation Engine v1.0.0
TIE Gold Standard - Formation Analysis & Petrophysical Interpretation

Covers: Gamma ray, resistivity (laterolog, induction, micro), Archie equation, porosity tools
(density, neutron, sonic), SP, caliper, NMR, formation pressure testing (MDT/RFT/DST),
mud logging, LWD vs wireline, cross-plots (neutron-density, M-N, MID), thin bed analysis,
invasion profiles, Rw determination, formation damage, core correlation, pay zone ID,
net-to-gross, petrophysical cutoffs, Permian Basin formations (Spraberry, Wolfcamp, etc).

Port: 9019
Author: ECHO OMEGA PRIME - Architect Mode
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Set
from collections import defaultdict, Counter
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "DRL09"
ENGINE_NAME = "Formation Evaluation Engine"
VERSION = "1.0.0"
PORT = 9019

logger.add(
    f"logs/{ENGINE_ID}_{{time}}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)

# ============================================================================
# ENUMS
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

class IssueCategory(str, Enum):
    GAMMA_RAY = "GAMMA_RAY"
    RESISTIVITY = "RESISTIVITY"
    POROSITY = "POROSITY"
    SATURATION = "SATURATION"
    PRESSURE = "PRESSURE"
    MUD_LOGGING = "MUD_LOGGING"
    CROSS_PLOT = "CROSS_PLOT"
    THIN_BED = "THIN_BED"
    INVASION = "INVASION"
    FORMATION_DAMAGE = "FORMATION_DAMAGE"
    PAY_ZONE = "PAY_ZONE"
    PETROPHYSICS = "PETROPHYSICS"

class AnalysisZone(str, Enum):
    LOG_INTERPRETATION = "LOG_INTERPRETATION"
    RESERVOIR_QUALITY = "RESERVOIR_QUALITY"
    SATURATION_ANALYSIS = "SATURATION_ANALYSIS"

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., description="Formation evaluation question")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    context: Optional[Dict[str, Any]] = Field(default=None)

class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    category: IssueCategory
    zone: AnalysisZone

class QueryResponse(BaseModel):
    engine_id: str
    version: str
    query: str
    mode: ResponseMode
    response: str
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    reasoning_chain: List[str]
    determinism_hash: str
    timestamp: str
    latency_ms: float

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float

# ============================================================================
# DOCTRINE CACHE - REAL FORMATION EVALUATION EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    # GAMMA RAY INTERPRETATION
    DoctrineBlock(
        topic="Gamma Ray Log Lithology Identification",
        keywords=["gamma ray", "GR", "lithology", "shale", "sandstone", "clean sand", "API units"],
        conclusion_template=[
            "Gamma ray log distinguishes shale from clean formations based on natural radioactivity.",
            "Shale baseline (typically 80-150 API) vs clean sand baseline (10-30 API) establishes Vshale.",
            "Linear, Larionov, or Clavier models calculate shale volume from GR deflection."
        ],
        reasoning_framework="""
        GR measures natural gamma radiation from K40, U238, Th232 isotopes.
        High GR = shale/clay (potassium-rich clays). Low GR = clean sand/carbonate.
        Vshale = (GR_log - GR_clean) / (GR_shale - GR_clean) [linear].
        Tertiary rocks: Vshale = 0.083 * (2^(3.7*IGR) - 1) [Larionov older].
        Mesozoic: Vshale = 0.33 * (2^(2*IGR) - 1) [Larionov younger].
        Clavier: Vshale = 1.7 - sqrt(3.38 - (IGR+0.7)^2).
        Spectral gamma ray separates K, U, Th — identifies hot shales, uranium zones, potassic feldspars.
        """,
        key_factors=["GR baseline selection", "shale volume model", "spectral components", "thin bed resolution", "borehole size effect"],
        primary_authority=["Asquith & Krygowski: Basic Well Log Analysis", "Schlumberger Log Interpretation Principles", "Dresser Atlas Well Logging & Interpretation"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.GAMMA_RAY,
        zone=AnalysisZone.LOG_INTERPRETATION
    ),

    DoctrineBlock(
        topic="Shale Volume Calculation Models",
        keywords=["Vshale", "IGR", "Larionov", "Clavier", "linear", "tertiary", "mesozoic"],
        conclusion_template=[
            "Linear Vshale model overestimates in dispersed shale; Larionov/Clavier correct for non-linear clay distribution.",
            "Tertiary formations use older rocks equation; Mesozoic use younger rocks equation.",
            "Spectral gamma ray improves accuracy by separating uranium, thorium, potassium contributions."
        ],
        reasoning_framework="""
        Linear: Vshale = IGR (oversimplified).
        Larionov (Tertiary/older): Vshale = 0.083*(2^(3.7*IGR)-1).
        Larionov (Mesozoic/younger): Vshale = 0.33*(2^(2*IGR)-1).
        Clavier: Vshale = 1.7 - sqrt(3.38-(IGR+0.7)^2).
        IGR = (GR_log - GR_min)/(GR_max - GR_min).
        Dispersed shale (clay coating grains) vs laminated shale (discrete layers) affects porosity/permeability differently.
        High uranium shales (organic-rich) create false high GR — spectral GR separates U from clay signal.
        """,
        key_factors=["geological age", "shale distribution type", "uranium content", "calibration points"],
        primary_authority=["Larionov 1969", "Clavier et al 1971", "SPE-5541-PA"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.GAMMA_RAY,
        zone=AnalysisZone.LOG_INTERPRETATION
    ),

    # RESISTIVITY LOGGING
    DoctrineBlock(
        topic="Deep Resistivity Tools - Laterolog vs Induction",
        keywords=["laterolog", "induction", "Rt", "deep resistivity", "LLD", "ILD", "invasion"],
        conclusion_template=[
            "Laterolog (focused electrode) preferred in conductive muds and high-resistivity formations.",
            "Induction (electromagnetic coils) preferred in oil-based mud and low-resistivity zones.",
            "Deep resistivity (Rt) represents uninvaded zone for accurate water saturation calculation."
        ],
        reasoning_framework="""
        Laterolog: Focused current beam, measures true formation resistivity Rt.
        LLD (Laterolog Deep), LLS (Laterolog Shallow) — shallow detects invasion.
        Effective in salt muds, high Rt contrast, thin beds.
        Induction: Transmitter coil induces eddy currents, receiver measures secondary field.
        ILD (Induction Deep), ILM (Induction Medium) — unaffected by borehole in OBM.
        Best in freshwater muds, non-conductive boreholes, low Rt formations.
        Skin effect limits induction in very high Rt (>200 ohm-m).
        Tornado charts: Rxo (flushed zone) vs Rt (virgin zone) indicates invasion profile.
        """,
        key_factors=["mud type", "formation resistivity range", "invasion depth", "bed thickness"],
        primary_authority=["Schlumberger Wireline & Testing", "Halliburton Logging Services Manual", "SPE-13133-PA"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.RESISTIVITY,
        zone=AnalysisZone.LOG_INTERPRETATION
    ),

    DoctrineBlock(
        topic="Micro-Resistivity and Rxo Measurement",
        keywords=["MSFL", "MLL", "Rxo", "flushed zone", "microlog", "proximity log"],
        conclusion_template=[
            "Micro-resistivity tools (MSFL, MLL) measure flushed zone resistivity Rxo for invasion correction.",
            "Rxo > Rt indicates oil/gas (mud filtrate replaces hydrocarbons); Rxo < Rt indicates water.",
            "Microlog detects permeable beds via caliper and differential resistivity response."
        ],
        reasoning_framework="""
        MSFL (Micro-Spherically Focused Log): button electrode, Rxo in flushed zone.
        MLL (Micro-Laterolog): focused pad tool, similar to MSFL.
        Proximity Log (old): 1" and 2" depth of investigation.
        Rxo used in dual-water model, invasion corrections for Archie.
        Rxo/Rt ratio: >1 = oil/gas show, <1 = water, =1 = no invasion or similar fluids.
        Microlog: mud cake builds in permeable zones, positive separation = permeability.
        Caliper log shows borehole enlargement (washout in shales) or tight hole (hard formations).
        """,
        key_factors=["mud filtrate resistivity Rmf", "invasion depth di", "permeability indicator", "mudcake thickness"],
        primary_authority=["Dewan: Essentials of Modern Open-Hole Log Interpretation", "Schlumberger Chart Book"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.RESISTIVITY,
        zone=AnalysisZone.LOG_INTERPRETATION
    ),

    # POROSITY TOOLS
    DoctrineBlock(
        topic="Density Log - Bulk Density and Porosity",
        keywords=["density log", "FDC", "rhob", "bulk density", "photoelectric", "Pe", "lithology"],
        conclusion_template=[
            "Density log measures bulk density (rhob) via gamma-gamma scattering for porosity calculation.",
            "Porosity_D = (rho_matrix - rho_bulk) / (rho_matrix - rho_fluid).",
            "Photoelectric factor Pe identifies lithology: sandstone 1.8, limestone 5.08, dolomite 3.14."
        ],
        reasoning_framework="""
        Cesium-137 source emits gamma rays, Compton scattering proportional to electron density.
        Electron density ≈ bulk density (rhob).
        Matrix densities: sandstone 2.65 g/cc, limestone 2.71, dolomite 2.87, anhydrite 2.98.
        Fluid density: freshwater 1.0, saltwater 1.1, oil 0.7-0.85, gas 0.3.
        Gas effect: density porosity reads too high (gas has low density).
        Mudcake, borehole rugosity degrade density — standoff correction applied.
        Photoelectric index Pe: low-Z elements (sandstone) vs high-Z (carbonates, barite).
        """,
        key_factors=["matrix lithology", "fluid type", "gas correction", "borehole conditions", "Pe crossplot"],
        primary_authority=["Schlumberger Cased-Hole Log Interpretation Principles", "SPE-10175-PA"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.POROSITY,
        zone=AnalysisZone.LOG_INTERPRETATION
    ),

    DoctrineBlock(
        topic="Neutron Log - Hydrogen Index Porosity",
        keywords=["neutron log", "CNL", "SNP", "hydrogen index", "gas crossover", "shale effect"],
        conclusion_template=[
            "Neutron log measures hydrogen concentration (HI) as proxy for porosity.",
            "Gas causes neutron-density crossover (low HI, low rhob); shale increases neutron response.",
            "Neutron-density crossplot distinguishes lithology and identifies gas zones."
        ],
        reasoning_framework="""
        Americium-Beryllium source emits fast neutrons, thermalized by hydrogen collisions.
        Thermal neutron count inversely proportional to hydrogen content.
        Water, oil: high HI ≈ porosity. Gas: low HI (underestimates porosity).
        Shale: bound water in clays increases neutron response (overestimates porosity).
        Neutron-density crossover: gas zone (neutron < density), shale (neutron > density).
        Limestone-equivalent units standard; sandstone/dolomite corrections needed.
        Epithermal neutron tools reduce borehole/salinity effects.
        """,
        key_factors=["gas presence", "shale content", "lithology matrix", "borehole salinity", "tool calibration"],
        primary_authority=["Ellis & Singer: Well Logging for Earth Scientists", "Schlumberger Log Interpretation Charts"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.POROSITY,
        zone=AnalysisZone.LOG_INTERPRETATION
    ),

    DoctrineBlock(
        topic="Sonic Log - Wyllie Time Average Equation",
        keywords=["sonic log", "DT", "compressional", "shear", "Wyllie", "porosity", "transit time"],
        conclusion_template=[
            "Sonic log measures interval transit time (Δt) for porosity via Wyllie equation.",
            "Porosity = (Δt_log - Δt_matrix) / (Δt_fluid - Δt_matrix) * correction factor.",
            "Shear wave (DTS) with compressional (DTC) derives Poisson ratio, rock mechanical properties."
        ],
        reasoning_framework="""
        Wyllie time-average: Phi = (DTlog - DTma)/(DTfl - DTma).
        DTma: sandstone 55.5 μs/ft, limestone 47.5, dolomite 43.5.
        DTfl: mud 189 μs/ft (freshwater), 185 (saltwater).
        Compaction correction factor Cp: unconsolidated sands need Cp<1.
        Shear wave derives Vp/Vs ratio, Poisson's ratio for fracture detection.
        Cycle skipping in gas zones (low density) causes errors.
        Formation strength: higher Δt = weaker rock (unconsolidated).
        """,
        key_factors=["compaction state", "lithology matrix", "gas presence", "unconsolidated sands", "shear data availability"],
        primary_authority=["Wyllie et al 1956", "SPE-16666-PA", "Raymer-Hunt-Gardner model"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.POROSITY,
        zone=AnalysisZone.LOG_INTERPRETATION
    ),

    # ARCHIE EQUATION & SATURATION
    DoctrineBlock(
        topic="Archie Equation - Water Saturation Calculation",
        keywords=["Archie", "Sw", "water saturation", "cementation exponent", "saturation exponent", "tortuosity"],
        conclusion_template=[
            "Archie equation: Sw^n = (a * Rw) / (Phi^m * Rt) calculates water saturation in clean formations.",
            "Cementation exponent m (typically 2.0 for carbonates, 1.8-2.2 for sands) reflects tortuosity.",
            "Saturation exponent n (typically 2.0) accounts for wettability; a (0.62-1.0) is tortuosity factor."
        ],
        reasoning_framework="""
        Archie (1942): Sw^n = (a*Rw)/(Phi^m*Rt).
        Formation factor F = a/Phi^m = Ro/Rw (100% water-saturated resistivity).
        Resistivity Index RI = Rt/Ro = 1/Sw^n.
        Typical values: a=1.0 (consolidated), 0.62 (unconsolidated), m=2.0 (intergranular), n=2.0 (water-wet).
        Rw: formation water resistivity from SP, water catalog, Pickett plot.
        Limitations: assumes clean formation (no shale), homogeneous pore system.
        Shaly sands need Simandoux, Indonesia, dual-water models.
        Low-resistivity pay (LRP): conductive minerals bypass Archie assumptions.
        """,
        key_factors=["Rw determination accuracy", "cementation exponent m", "shale volume", "wettability", "formation cleanliness"],
        primary_authority=["Archie 1942 AIME", "Schlumberger Log Interpretation Principles", "SPE-6542-PA"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SATURATION,
        zone=AnalysisZone.SATURATION_ANALYSIS
    ),

    DoctrineBlock(
        topic="Formation Water Resistivity (Rw) Determination",
        keywords=["Rw", "SP log", "Pickett plot", "Rmf", "water catalog", "salinity"],
        conclusion_template=[
            "Rw derived from SP deflection (SSP = -K * log(Rmf/Rw)), Pickett plot, or water samples.",
            "Accurate Rw critical for Archie equation; errors propagate exponentially into Sw.",
            "Temperature correction mandatory: resistivity decreases with increasing temperature."
        ],
        reasoning_framework="""
        SP method: SSP (static SP) = -K*log(Rmf/Rw_eqv), K = 60+0.133*T°F.
        Pickett plot: log(Rt) vs log(Phi), 100% water line slope = -m, intercept = Rw.
        Formation water samples from MDT, DST (if available).
        Resistivity-temperature: Rt2 = Rt1 * (T1+6.77)/(T2+6.77) [Arps equation].
        Salinity: NaCl concentration affects Rw (higher salinity = lower Rw).
        Rmf (mud filtrate): measured surface, corrected to formation temp.
        Regional water catalogs: Permian Basin Wolfcamp Rw ≈ 0.02-0.04 ohm-m @ formation temp.
        """,
        key_factors=["SP quality", "temperature gradient", "salinity data", "mud filtrate properties", "regional water chemistry"],
        primary_authority=["Bateman & Konen 1977", "Schlumberger Chart Gen-9", "SPE-4532-PA"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SATURATION,
        zone=AnalysisZone.SATURATION_ANALYSIS
    ),

    # SP LOG
    DoctrineBlock(
        topic="Spontaneous Potential (SP) Log Interpretation",
        keywords=["SP", "SSP", "shale baseline", "permeable bed", "Rw", "electrochemical"],
        conclusion_template=[
            "SP log measures natural electrochemical potential between borehole and formation.",
            "Negative deflection (to left) indicates permeable, porous bed with salinity contrast.",
            "SSP amplitude proportional to Rmf/Rw ratio; baseline shift identifies impermeable shales."
        ],
        reasoning_framework="""
        SP arises from electrochemical (Ec) + electrokinetic (Ek) potentials.
        Ec dominant: ion diffusion + membrane potential at shale interfaces.
        SSP = -K*log(Rmf/Rw_eqv), K = 60+0.133*T°F.
        Permeable sands: sharp negative deflection. Shales: flat baseline (no ion flow).
        Shale baseline drift: varying shale conductivity, hydrocarbon effects.
        No SP in oil-based mud (non-conductive), air-drilled holes, or cased holes.
        Resistive beds (anhydrite, tight carbonates): small or no SP deflection.
        """,
        key_factors=["mud type", "salinity contrast", "permeability", "shale conductivity variations", "bed thickness"],
        primary_authority=["Doll 1948 (Schlumberger pioneer)", "SPE-1238-G", "Asquith Basic Well Log Analysis"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.GAMMA_RAY,
        zone=AnalysisZone.LOG_INTERPRETATION
    ),

    # CALIPER
    DoctrineBlock(
        topic="Caliper Log - Borehole Size and Formation Quality",
        keywords=["caliper", "borehole diameter", "washout", "breakout", "tight hole", "mudcake"],
        conclusion_template=[
            "Caliper measures borehole diameter; washouts (enlarged hole) indicate shale or unconsolidated formations.",
            "Tight hole (reduced diameter) indicates hard, competent formations or mudcake buildup.",
            "Caliper correction essential for density, neutron, resistivity log accuracy."
        ],
        reasoning_framework="""
        Multi-arm caliper (3-6 arms) measures diameter, detects elliptical breakouts.
        Washout: hole > bit size, shales swell/cave, friable sands erode.
        Tight hole: hole < bit size, hard carbonates, dense shales, thick mudcake.
        Mudcake: permeable zones build filter cake (microlog positive separation).
        Borehole corrections: density/neutron tools assume 8.5" hole; washouts degrade readings.
        Breakouts (stress-induced): indicate max horizontal stress direction (geomechanics).
        Rugosity: caliper variance measures formation heterogeneity.
        """,
        key_factors=["bit size", "formation competency", "mud weight", "permeability", "stress regime"],
        primary_authority=["Schlumberger Log Interpretation Principles", "SPE-16792-PA (breakout analysis)"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.GAMMA_RAY,
        zone=AnalysisZone.LOG_INTERPRETATION
    ),

    # NMR LOGGING
    DoctrineBlock(
        topic="NMR Logging - T2 Distributions and Permeability",
        keywords=["NMR", "T2", "T1", "CPMG", "free fluid index", "BVI", "permeability", "Timur-Coates"],
        conclusion_template=[
            "NMR measures hydrogen relaxation times (T2) to derive porosity, fluid types, and permeability.",
            "Short T2 = bound water in clay/small pores; long T2 = free fluids in large pores.",
            "Permeability estimated via Timur-Coates: k = (Phi^4 * FFI^2) / C or SDR model."
        ],
        reasoning_framework="""
        NMR (nuclear magnetic resonance): polarize H atoms, measure T1/T2 decay.
        T2 distribution: tri-modal (clay-bound, capillary-bound, free fluid).
        T2 cutoff (typically 33 ms): BVI (bulk volume irreducible) vs FFI (free fluid index).
        Total porosity = amplitude of T2 spectrum (independent of lithology).
        Permeability models: Timur-Coates k=(a*Phi^4*FFI^2)/BVI^2, SDR k=a*Phi^b*T2gm^c.
        Gas detection: long T2, diffusion effects, lower signal amplitude.
        Wettability: oil-wet shifts T2 distribution (oil relaxes faster at surface).
        """,
        key_factors=["T2 cutoff selection", "clay-bound water volume", "diffusion regime", "wettability", "gas presence"],
        primary_authority=["Coates et al SPE-49294", "Kenyon 1997 NMR Review", "Schlumberger CMR/MR Scanner manuals"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.PETROPHYSICS,
        zone=AnalysisZone.RESERVOIR_QUALITY
    ),

    # FORMATION PRESSURE TESTING
    DoctrineBlock(
        topic="Formation Pressure Testing - MDT, RFT, DST",
        keywords=["MDT", "RFT", "DST", "formation pressure", "mobility", "permeability", "fluid gradient"],
        conclusion_template=[
            "MDT (Modular Dynamic Tester) and RFT (Repeat Formation Tester) measure formation pressure, fluid samples.",
            "Pressure gradient identifies fluid contacts: gas 0.1 psi/ft, oil 0.3-0.35, water 0.43-0.52.",
            "DST (Drill Stem Test) provides reservoir deliverability, skin, permeability from pressure transient analysis."
        ],
        reasoning_framework="""
        Wireline formation testers: probe seals on borehole wall, withdraws fluid, measures pressure.
        Pretests: 1-5 cc withdrawal, establish formation pressure, check seal.
        Mobility: pressure buildup rate indicates permeability*thickness/viscosity.
        Fluid gradients: plot pressure vs depth, slope = fluid density.
        Gas/oil contact (GOC), oil/water contact (OWC) identified by gradient change.
        Supercharging: overbalanced mud increases measured pressure (time-dependent).
        DST: drill string isolated packer, flow periods + shut-in, full reservoir test.
        Horner plot, type-curve match: derive k, skin, boundaries.
        """,
        key_factors=["seal quality", "mud overbalance", "time since drilling", "formation permeability", "sample contamination"],
        primary_authority=["Schlumberger Wireline Formation Testing", "SPE-103204-PA", "Earlougher: Advances in Well Test Analysis"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PRESSURE,
        zone=AnalysisZone.RESERVOIR_QUALITY
    ),

    # MUD LOGGING
    DoctrineBlock(
        topic="Mud Logging - Gas Shows and Cuttings Analysis",
        keywords=["mud logging", "gas shows", "C1", "C2-C5", "ratios", "cuttings", "ROP", "lithology"],
        conclusion_template=[
            "Mud logging monitors drilling parameters, gas chromatography (C1-C5), and cuttings for real-time formation evaluation.",
            "Gas ratios (C1/C2, balance, character) indicate reservoir quality: wet gas, oil, condensate.",
            "ROP (rate of penetration) correlation with gamma ray, cuttings lithology guides geosteering."
        ],
        reasoning_framework="""
        Gas detector: FID (flame ionization), catalytic, infrared measures C1-C5 hydrocarbons.
        Total gas (TG), background gas (BG), connection gas (CG), trip gas.
        Ratios: Wetness = (C2+C3)/(C1+C2+C3), Balance = (C2/C3), Character = (C4+C5)/(C2+C3).
        Dry gas: C1 dominant, low wetness. Wet gas: C2-C5 present. Oil: high C4-C5.
        Cuttings description: lithology, color, texture, porosity (visual, UV fluorescence).
        ROP vs depth: faster in porous sands, slower in shales/carbonates.
        Lagtime: time for cuttings to reach surface (depth/annular velocity).
        """,
        key_factors=["gas extraction efficiency", "lagtime calculation", "drilling fluid type", "contamination", "bit hydraulics"],
        primary_authority=["EXLOG/Schlumberger Mudlogging Services", "SPE-27018-PA", "SPWLA Mud Logging Guidelines"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.MUD_LOGGING,
        zone=AnalysisZone.LOG_INTERPRETATION
    ),

    # LWD VS WIRELINE
    DoctrineBlock(
        topic="LWD (Logging While Drilling) vs Wireline Comparison",
        keywords=["LWD", "MWD", "wireline", "real-time", "invasion", "borehole conditions", "geosteering"],
        conclusion_template=[
            "LWD measures formation properties while drilling (minimal invasion, better borehole conditions).",
            "Wireline logs run after drilling (deeper invasion, potential washout, higher resolution).",
            "LWD advantages: real-time data, geosteering, horizontal wells; wireline: full suite, higher precision."
        ],
        reasoning_framework="""
        LWD: gamma ray, resistivity, neutron-density, sonic integrated into drill collar.
        Measured shortly after bit penetration: less filtrate invasion, near-original Sw.
        Real-time data for geosteering, kick detection, pore pressure monitoring.
        Downside: lower resolution (tool rotation, vibration), limited tool suite.
        Wireline: full physics suite (NMR, dielectric, imaging, formation testing).
        Run hours/days after drilling: deeper invasion (Rxo ≠ Rt zone), possible rugosity.
        Advantage: stationary measurement, better signal/noise, more sensor options.
        Horizontal wells: wireline difficult/impossible → LWD essential.
        """,
        key_factors=["well trajectory", "time-dependent invasion", "data quality needs", "real-time decision requirements"],
        primary_authority=["SPE-56424-MS", "Schlumberger LWD Services", "Halliburton Sperry Drilling"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MUD_LOGGING,
        zone=AnalysisZone.LOG_INTERPRETATION
    ),

    # CROSS-PLOT TECHNIQUES
    DoctrineBlock(
        topic="Neutron-Density Crossplot for Lithology and Gas",
        keywords=["neutron-density", "crossplot", "lithology triangle", "gas crossover", "matrix identification"],
        conclusion_template=[
            "Neutron-density crossplot identifies lithology (sandstone, limestone, dolomite) and gas zones.",
            "Gas: neutron porosity < density porosity (crossover); shale: neutron > density.",
            "Points plot toward matrix endpoints; porosity increases outward from matrix."
        ],
        reasoning_framework="""
        X-axis: bulk density (rhob). Y-axis: neutron porosity (NPHI).
        Matrix endpoints: sandstone (2.65 g/cc, varies), limestone (2.71, 0), dolomite (2.87, 0).
        Clean formation: plots on lithology line connecting matrix to fluid point.
        Gas zone: low rhob + low NPHI → plots below/left of hydrocarbon line.
        Shale: high NPHI (clay-bound water), moderate rhob → above sand line.
        Secondary porosity (vugs, fractures): shifts off matrix line.
        Overlay Pe (photoelectric) confirms lithology: sandstone ~1.8, limestone ~5.0, dolomite ~3.0.
        """,
        key_factors=["gas presence", "shale content", "lithology mixing", "secondary porosity", "tool calibration"],
        primary_authority=["Schlumberger Chart CP-18", "Dresser Atlas Neutron-Density Crossplot", "SPE-13133-PA"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CROSS_PLOT,
        zone=AnalysisZone.LOG_INTERPRETATION
    ),

    DoctrineBlock(
        topic="M-N Plot and MID Plot for Complex Lithology",
        keywords=["M-N plot", "MID plot", "sonic-density-neutron", "complex lithology", "matrix identification"],
        conclusion_template=[
            "M-N plot uses sonic and density/neutron data to identify complex lithologies independent of porosity.",
            "M = (Δt_f - Δt_log)/(rhob - rho_f), N = (NPHI_f - NPHI_log)/(rhob - rho_f).",
            "MID plot adds Pe (photoelectric) for definitive mineral identification in carbonates."
        ],
        reasoning_framework="""
        M-N plot: eliminates porosity variable, plots matrix properties.
        M = (189 - DT)/(rhob - 1.0) for freshwater mud.
        N = (NPHI_f - NPHI)/(rhob - 1.0).
        Matrix clusters: quartz, calcite, dolomite, anhydrite, salt separate distinctly.
        Mixed lithology: linear combination plots between endmembers.
        MID plot: combines M-N with Pe (photoelectric cross-section).
        Pe crossplot with M or N improves dolomite/limestone/anhydrite separation.
        Applications: evaporite sections, carbonates with chert, volcanic clastics.
        """,
        key_factors=["fluid density assumption", "tool calibration", "shale effect correction", "gas presence"],
        primary_authority=["Burke et al SPE-13083-PA", "Schlumberger MID Plot Chart", "Dresser Atlas Litho-Density Applications"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.CROSS_PLOT,
        zone=AnalysisZone.LOG_INTERPRETATION
    ),

    # THIN BED ANALYSIS
    DoctrineBlock(
        topic="Thin Bed Analysis and Vertical Resolution",
        keywords=["thin bed", "vertical resolution", "laminated", "deconvolution", "shoulder bed"],
        conclusion_template=[
            "Thin beds (<2 ft) require vertical resolution correction; logging tools average thicker intervals.",
            "Resistivity tools: laterolog ~2 ft resolution, induction ~6-8 ft; deconvolution improves.",
            "Laminated sands (sand-shale interbeds <tool resolution) need Thomas-Stieber or Worthington models."
        ],
        reasoning_framework="""
        Vertical resolution: tool's ability to resolve bed boundaries.
        Density/neutron: ~1 ft. Laterolog: ~2 ft. Induction: 4-8 ft (depends on array).
        Shoulder bed effect: adjacent bed resistivity biases reading in thin targets.
        Deconvolution: inverse filtering sharpens log response (Pita-Flaum technique).
        Laminated reservoirs: sand layers <6 inches interbedded with shale.
        Thomas-Stieber: Vshale_laminar, Vshale_dispersed, total Vshale from neutron-density.
        Effective porosity in laminates: Phi_e = Phi_t * (1 - Vsh_lam).
        Anisotropic resistivity: Rv (vertical) ≠ Rh (horizontal) in laminates.
        """,
        key_factors=["bed thickness", "tool resolution", "invasion profile", "lamination scale", "deconvolution availability"],
        primary_authority=["Thomas & Stieber SPE-8925-PA", "Worthington SPE-21794-PA", "Schlumberger Dipmeter/Array Tools"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.THIN_BED,
        zone=AnalysisZone.LOG_INTERPRETATION
    ),

    # INVASION PROFILES
    DoctrineBlock(
        topic="Invasion Profile and Radial Resistivity Variations",
        keywords=["invasion", "Rxo", "Ri", "Rt", "flushed zone", "transition zone", "tornado chart"],
        conclusion_template=[
            "Mud filtrate invades permeable formations, creating radial resistivity profile: Rxo (flushed) → Ri (transition) → Rt (virgin).",
            "Deep resistivity (Rt) for Archie; shallow/micro (Rxo) detects hydrocarbons via movable oil calculation.",
            "Invasion depth varies with permeability, mud properties, time; tornado chart models resistivity vs depth."
        ],
        reasoning_framework="""
        Invasion zones: flushed (di ~10-40 inches, Rxo), invaded annulus (Ri), virgin (Rt).
        Step profile (sharp transition) vs gradual (diffusion-dominated).
        Rxo/Rt > 1: oil/gas (filtrate replaces HC). Rxo/Rt < 1: water-bearing.
        Movable oil: Sxo (flushed) vs Sw (virgin) → Sxo-Sw = moved hydrocarbons.
        Array induction/laterolog tools measure multiple radial depths → inversion for Rxo, Ri, Rt, di.
        Tornado chart: overlay Rxo, medium, deep resistivity curves for visual invasion interpretation.
        Time-dependent: invasion deepens with time since drilling (hours to days).
        """,
        key_factors=["permeability", "mud overbalance", "time since drilling", "mud filtrate properties", "tool array configuration"],
        primary_authority=["Schlumberger AIT (Array Induction) Manual", "SPE-13133-PA", "Dresser Atlas Dual Laterolog"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.INVASION,
        zone=AnalysisZone.SATURATION_ANALYSIS
    ),

    # FORMATION DAMAGE
    DoctrineBlock(
        topic="Formation Damage Identification via Logs",
        keywords=["formation damage", "skin", "near-wellbore", "permeability reduction", "invasion", "filtercake"],
        conclusion_template=[
            "Formation damage (reduced permeability near wellbore) detected via resistivity/porosity tool comparison.",
            "Shallow resistivity reduction (Rxo low, Rt normal) indicates clay swelling, fines migration, or emulsion blocking.",
            "NMR T2 shift to short values, reduced permeability estimate confirms damage; DST skin factor quantifies."
        ],
        reasoning_framework="""
        Damage mechanisms: clay swelling (freshwater filtrate), fines migration, emulsions, scale precipitation.
        Resistivity signature: Rxo < Rt (opposite of hydrocarbon invasion) in water-bearing zone.
        Porosity logs: density-neutron crossplot shift toward lower effective porosity.
        NMR: increased clay-bound water (short T2), reduced FFI → lower calculated perm.
        Caliper: thick mudcake (tight hole) indicates heavy filtration but may protect formation.
        DST/well test: positive skin factor (S>0) confirms near-wellbore restriction.
        Remediation: acid stimulation (carbonates), clay stabilizers, solvent treatments.
        """,
        key_factors=["mud filtrate compatibility", "clay content", "time-dependent damage", "production history"],
        primary_authority=["SPE-31104-PA (formation damage)", "Civan: Reservoir Formation Damage", "Schlumberger Stimulation Services"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.FORMATION_DAMAGE,
        zone=AnalysisZone.RESERVOIR_QUALITY
    ),

    # CORE ANALYSIS CORRELATION
    DoctrineBlock(
        topic="Core Analysis Correlation with Log Data",
        keywords=["core", "core analysis", "SCAL", "RCAL", "log-core calibration", "porosity permeability"],
        conclusion_template=[
            "Core data (porosity, permeability, saturation, grain density) calibrates log-derived parameters.",
            "Log porosity typically reads higher than core due to shale, borehole effects; depth-shift cores to logs.",
            "SCAL (special core) provides capillary pressure, relative permeability for reservoir simulation."
        ],
        reasoning_framework="""
        Routine core analysis (RCAL): porosity, permeability (Kair, Kliq), grain density, fluid saturations.
        Special core (SCAL): capillary pressure Pc, relative perm kr, wettability, electrical properties.
        Depth matching: core depth (driller's) vs log depth (wireline) → shift 0.5-3 ft common.
        Porosity calibration: core Phi (helium/summation of fluids) vs log Phi (density, neutron, sonic).
        Log reads total porosity; core can separate effective vs isolated porosity.
        Permeability correlation: log-derived (NMR, Timur-Coates) vs core Kair → build transform.
        Saturation: Dean-Stark core Sw vs Archie Sw → verify Rw, m, n parameters.
        """,
        key_factors=["depth shift accuracy", "core preservation quality", "measurement conditions (net confining stress)", "core plugs representativeness"],
        primary_authority=["API RP-40 Core Analysis", "SPE-10011-PA", "Tiab & Donaldson Petrophysics"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PETROPHYSICS,
        zone=AnalysisZone.RESERVOIR_QUALITY
    ),

    # PAY ZONE IDENTIFICATION
    DoctrineBlock(
        topic="Pay Zone Identification Criteria",
        keywords=["pay zone", "net pay", "cutoffs", "Vsh", "porosity", "Sw", "reservoir quality"],
        conclusion_template=[
            "Pay zone defined by cutoffs: Vshale <30-40%, porosity >8-12%, water saturation <60-70%, permeability >0.1 mD.",
            "Net pay vs gross pay: net excludes non-reservoir rock (shale stringers, tight streaks).",
            "Economic cutoffs (production rate, EUR) may differ from petrophysical cutoffs."
        ],
        reasoning_framework="""
        Multi-parameter cutoffs: all must be met simultaneously.
        Vshale cutoff: <40% for sandstones (excludes shaly sands), <15% for tight reservoirs.
        Porosity cutoff: >10% typical, >6% for tight gas, >8% for oil.
        Sw cutoff: <60-70% for conventional, <50% for high-quality pay, <80% for tight oil.
        Permeability cutoff: >1 mD conventional, >0.1 mD tight, >0.01 mD ultra-tight.
        Bulk volume water (BVW = Phi*Sw): constant BVW across reservoir indicates common transition zone.
        Net-to-Gross (NTG): ratio of net pay to gross interval, critical for reserves.
        Pay flags: binary classification per depth point, summed for net pay thickness.
        """,
        key_factors=["reservoir type", "fluid type", "economic threshold", "regional benchmarks", "completion technology"],
        primary_authority=["SPE-15135-PA (cutoff selection)", "Worthington SPE-71361-MS", "Permian Basin regional studies"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PAY_ZONE,
        zone=AnalysisZone.RESERVOIR_QUALITY
    ),

    DoctrineBlock(
        topic="Net-to-Gross Calculation and Reservoir Volume",
        keywords=["net-to-gross", "NTG", "gross pay", "net pay", "reservoir thickness", "HCPV"],
        conclusion_template=[
            "Net-to-Gross ratio (NTG) = net pay thickness / gross interval thickness.",
            "HCPV (hydrocarbon pore volume) = bulk volume * NTG * porosity * (1-Sw).",
            "Low NTG (<0.5) indicates heterogeneous reservoir with shale/tight interbeds."
        ],
        reasoning_framework="""
        Gross interval: total reservoir thickness from top to base marker.
        Net pay: footage meeting all cutoff criteria (Vsh, Phi, Sw, perm).
        NTG calculation: sum net pay flags / total interval.
        NTG variability: well-sorted clean sand NTG>0.8, laminated sand-shale NTG=0.3-0.6.
        Volumetrics: OOIP = 7758 * Area * h_net * Phi * (1-Sw) / Bo.
        Upscaling for simulation: log-scale net pay → grid-block average properties.
        Economic impact: low NTG requires more wells to drain same pore volume.
        """,
        key_factors=["cutoff sensitivity", "lamination frequency", "vertical resolution", "upscaling method"],
        primary_authority=["SPE-113320-MS (NTG determination)", "Reservoir Engineering Handbook", "SPWLA NTG guidelines"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PAY_ZONE,
        zone=AnalysisZone.RESERVOIR_QUALITY
    ),

    # PETROPHYSICAL CUTOFFS
    DoctrineBlock(
        topic="Petrophysical Cutoff Optimization",
        keywords=["cutoffs", "optimization", "porosity cutoff", "Sw cutoff", "permeability cutoff", "economic"],
        conclusion_template=[
            "Cutoffs balance technical deliverability (perm, Sw) with economic viability (EUR, NPV).",
            "Winland R35 relates porosity-permeability-pore throat: k = 10^(0.732 + 0.588*log(Phi) - 0.864*log(R35)).",
            "Probabilistic cutoffs (P10/P50/P90) account for uncertainty in reserves estimation."
        ],
        reasoning_framework="""
        Porosity cutoff: from capillary pressure (height above FWL where Sw=100%), or permeability threshold.
        Sw cutoff: irreducible (Swirr) from core Pc, or economic (flowing Sw from relative perm).
        Permeability cutoff: minimum for economic flow rate (darcy flow + well completion).
        Winland R35: pore throat radius at 35% Hg saturation, correlates k-Phi.
        Flow Zone Indicator (FZI): groups similar pore systems, k = (1014*Phi^3)/(Vsh*(1-Phi))^2.
        Rock typing: classify into bins (RT1, RT2...) with distinct k-Phi-Sw trends.
        Sensitivity analysis: vary cutoffs ±10%, observe impact on reserves (tornado chart).
        """,
        key_factors=["production mechanism", "completion type (frac vs natural)", "fluid properties (viscosity)", "economic assumptions"],
        primary_authority=["Winland 1972 Amoco internal", "SPE-71317-MS (cutoff optimization)", "Amaefule FZI SPE-26436"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.PETROPHYSICS,
        zone=AnalysisZone.RESERVOIR_QUALITY
    ),

    # PERMIAN BASIN FORMATIONS
    DoctrineBlock(
        topic="Permian Basin - Spraberry Formation Characteristics",
        keywords=["Spraberry", "Permian Basin", "Midland Basin", "low permeability", "tight oil", "natural fractures"],
        conclusion_template=[
            "Spraberry Trend (Midland Basin): tight silty sandstone/siltstone, porosity 8-15%, permeability <0.1 mD.",
            "Natural fractures critical for production; horizontal drilling + multi-stage frac standard completion.",
            "Log response: low gamma ray (clean silt), moderate density-neutron porosity, high resistivity (oil-saturated, tight)."
        ],
        reasoning_framework="""
        Stratigraphy: Leonardian age (lower Permian), Dean/Spraberry/lower Clearfork interval.
        Lithology: very fine sand to silt, well-sorted, low matrix perm (0.01-0.1 mD).
        Porosity: 8-15% (density/neutron), sonic often overstates due to low compaction.
        Fractures: natural fracture swarms (N-S, NE-SW trends) enhance effective perm 10-100x.
        GR: 30-60 API (clean to slightly silty), lower than adjacent shales.
        Resistivity: Rt 20-200+ ohm-m (oil zone), Archie m~1.9-2.1, n~2.0.
        Water saturation: Sw 20-40% in pay (low Rw ~0.018 ohm-m @ 180°F).
        Completion: 5000-10000 ft laterals, 20-40 frac stages, 100-200K lbs proppant/stage.
        """,
        key_factors=["natural fracture intensity", "frac design", "EUR 200-600 MBO typical", "decline analysis"],
        primary_authority=["Handford 1981 Spraberry depositional", "SPE-171658-MS (Spraberry geomechanics)", "Midland Basin operator presentations"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PETROPHYSICS,
        zone=AnalysisZone.RESERVOIR_QUALITY
    ),

    DoctrineBlock(
        topic="Permian Basin - Wolfcamp Formation Evaluation",
        keywords=["Wolfcamp", "Wolfcamp A B C D", "Delaware Basin", "Midland Basin", "shale oil", "mixed lithology"],
        conclusion_template=[
            "Wolfcamp A/B/C/D: interbedded shale, siltstone, limestone; primary unconventional oil target in Permian.",
            "Mixed lithology requires neutron-density-Pe crossplot; TOC from density-resistivity (Passey ΔlogR).",
            "Pay zones: Wolfcamp A upper/lower, Wolfcamp B (Delaware); porosity 6-12%, Sw 20-50%."
        ],
        reasoning_framework="""
        Stratigraphy: Pennsylvanian-lower Permian, underlies Spraberry/Bone Spring, overlies Mississippian.
        Four members: Wolfcamp A (youngest) → D (oldest), each 100-400 ft thick.
        Lithology: organic-rich shale + carbonate/siltstone beds (HRZ = high resistivity zones).
        GR: 80-200 API (shale-dominated), spikes to 250+ in hot shales (uranium).
        Resistivity: Rt 10-500 ohm-m, high Rt in silty/carbonate beds = sweet spots.
        Porosity: 4-12%, density-neutron crossover in organic-rich intervals (kerogen has low density).
        TOC: Passey ΔlogR = log(Rt/Rt_baseline) + 0.02*(Dt - Dt_baseline), TOC = ΔlogR * 10^(2.297-0.1688*LOM).
        Brittleness: Young's modulus from sonic, Poisson's ratio → frac stimulation design.
        """,
        key_factors=["TOC >2% for best EUR", "carbonate content (brittleness)", "natural fractures", "landing zone selection"],
        primary_authority=["SPE-187512-MS (Wolfcamp characterization)", "Passey et al AAPG 1990 ΔlogR", "Delaware Basin studies"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PETROPHYSICS,
        zone=AnalysisZone.RESERVOIR_QUALITY
    ),

    DoctrineBlock(
        topic="Permian Basin - Bone Spring Formation (Delaware Basin)",
        keywords=["Bone Spring", "Delaware Basin", "1st 2nd 3rd Bone Spring", "sandstone", "siltstone", "turbidites"],
        conclusion_template=[
            "Bone Spring 1st/2nd/3rd sands: turbidite deposits, better reservoir quality than Wolfcamp (porosity 8-14%, perm 0.01-1 mD).",
            "Lower shale content, higher quartz; neutron-density separation identifies porous sands.",
            "Log markers: clean GR (40-80 API in sands), moderate-high resistivity, sonic transit time increases in porous zones."
        ],
        reasoning_framework="""
        Stratigraphy: Leonardian, overlies Wolfcamp, three main intervals (1st/2nd/3rd Bone Spring sands).
        Depositional: deep-water turbidites (channel/lobe complexes), interbedded with basinal shales.
        Lithology: fine-grained sandstone/siltstone, quartz-rich, less carbonate than Wolfcamp.
        GR: 40-100 API (cleaner than Wolfcamp), sharp-based sand packages.
        Porosity: 8-14% (neutron-density average), better sorting improves reservoir quality.
        Resistivity: Rt 15-100 ohm-m in oil zones, water legs show low Rt (3-10 ohm-m).
        Permeability: 0.01-1 mD matrix (higher than Wolfcamp), natural fractures less critical.
        Completion: shorter laterals (3000-7000 ft), tighter stage spacing, proppant loading varies.
        """,
        key_factors=["sand continuity (channel vs lobe)", "water saturation gradients", "frac height containment"],
        primary_authority=["SPE-189823-MS (Bone Spring geomechanics)", "Delaware Basin geological studies", "Operator type logs"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PETROPHYSICS,
        zone=AnalysisZone.RESERVOIR_QUALITY
    )
]

# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class Telemetry:
    def __init__(self):
        self.query_count = 0
        self.doctrine_hits = Counter()
        self.latencies = []
        self.errors = []
        self.start_time = time.time()

    def record_query(self, latency_ms: float, doctrines: List[str], error: Optional[str] = None):
        self.query_count += 1
        self.latencies.append(latency_ms)
        for d in doctrines:
            self.doctrine_hits[d] += 1
        if error:
            self.errors.append(error)

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "total_queries": self.query_count,
            "avg_latency_ms": sum(self.latencies) / len(self.latencies) if self.latencies else 0,
            "p95_latency_ms": sorted(self.latencies)[int(len(self.latencies) * 0.95)] if self.latencies else 0,
            "error_count": len(self.errors),
            "top_doctrines": dict(self.doctrine_hits.most_common(10)),
            "uptime_seconds": time.time() - self.start_time
        }

telemetry = Telemetry()

# ============================================================================
# DOCTRINE CACHE QUERY
# ============================================================================

def query_doctrine_cache(query: str, top_k: int = 5) -> List[DoctrineBlock]:
    """Fast keyword-based doctrine retrieval."""
    query_lower = query.lower()
    query_terms = set(re.findall(r'\b\w+\b', query_lower))

    scores = []
    for doctrine in DOCTRINE_CACHE:
        keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
        topic_match = 3 if any(term in doctrine.topic.lower() for term in query_terms) else 0
        total_score = keyword_matches * 2 + topic_match
        if total_score > 0:
            scores.append((total_score, doctrine))

    scores.sort(reverse=True, key=lambda x: x[0])
    return [d for _, d in scores[:top_k]]

# ============================================================================
# THREE-LAYER RESPONSE
# ============================================================================

def three_layer_response(query: str, mode: ResponseMode) -> Dict[str, Any]:
    """TIE-20 Component: Three-layer response architecture."""
    start = time.time()

    # Layer 1: Doctrine cache (0-200ms)
    triggered = query_doctrine_cache(query, top_k=5)

    if not triggered:
        # Layer 2: Semantic fallback (simulated)
        logger.warning(f"No doctrine cache hit for: {query}")
        triggered = [DOCTRINE_CACHE[0]]  # Fallback to first doctrine

    # Layer 3: Deep analysis (mode-dependent)
    response_text = generate_response(query, triggered, mode)
    confidence = aggregate_confidence(triggered)
    reasoning = build_reasoning_chain(triggered)

    latency = (time.time() - start) * 1000
    return {
        "response": response_text,
        "confidence": confidence,
        "triggered_doctrines": [d.topic for d in triggered],
        "reasoning_chain": reasoning,
        "latency_ms": latency
    }

def generate_response(query: str, doctrines: List[DoctrineBlock], mode: ResponseMode) -> str:
    """Generate mode-appropriate response."""
    if mode == ResponseMode.FAST:
        # Concise summary
        primary = doctrines[0]
        return f"{' '.join(primary.conclusion_template)} Key factors: {', '.join(primary.key_factors[:3])}."

    elif mode == ResponseMode.DEFENSE:
        # Audit-ready with authorities
        parts = []
        for d in doctrines[:3]:
            parts.append(f"**{d.topic}**: {' '.join(d.conclusion_template)}")
            parts.append(f"Authority: {'; '.join(d.primary_authority[:2])}")
        return "\n\n".join(parts)

    else:  # MEMO
        # Full documentation
        parts = [f"# Formation Evaluation Analysis\n\n**Query**: {query}\n"]
        for i, d in enumerate(doctrines, 1):
            parts.append(f"## {i}. {d.topic}\n")
            parts.append(f"**Conclusion**: {' '.join(d.conclusion_template)}\n")
            parts.append(f"**Framework**: {d.reasoning_framework[:300]}...\n")
            parts.append(f"**Key Factors**: {', '.join(d.key_factors)}\n")
            parts.append(f"**Authority**: {'; '.join(d.primary_authority)}\n")
        return "\n".join(parts)

def aggregate_confidence(doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
    """Aggregate confidence from triggered doctrines."""
    levels = [d.confidence for d in doctrines]
    if ConfidenceLevel.HIGH_RISK in levels:
        return ConfidenceLevel.HIGH_RISK
    if ConfidenceLevel.DISCLOSURE in levels:
        return ConfidenceLevel.DISCLOSURE
    if ConfidenceLevel.AGGRESSIVE in levels:
        return ConfidenceLevel.AGGRESSIVE
    return ConfidenceLevel.DEFENSIBLE

def build_reasoning_chain(doctrines: List[DoctrineBlock]) -> List[str]:
    """Build reasoning chain from doctrines."""
    chain = []
    for d in doctrines:
        chain.append(f"{d.topic}: {d.reasoning_framework[:150]}...")
    return chain

# ============================================================================
# DETERMINISM HASH
# ============================================================================

def compute_determinism_hash(query: str, response: str, doctrines: List[str]) -> str:
    """TIE-20 Component: SHA-256 determinism hash."""
    content = f"{query}|{response}|{'|'.join(sorted(doctrines))}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(title=ENGINE_NAME, version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with three-layer response."""
    try:
        result = three_layer_response(request.query, request.mode)

        response = QueryResponse(
            engine_id=ENGINE_ID,
            version=VERSION,
            query=request.query,
            mode=request.mode,
            response=result["response"],
            confidence=result["confidence"],
            triggered_doctrines=result["triggered_doctrines"],
            reasoning_chain=result["reasoning_chain"],
            determinism_hash=compute_determinism_hash(
                request.query,
                result["response"],
                result["triggered_doctrines"]
            ),
            timestamp=datetime.utcnow().isoformat(),
            latency_ms=result["latency_ms"]
        )

        telemetry.record_query(result["latency_ms"], result["triggered_doctrines"])
        logger.info(f"Query processed: {request.query[:50]}... | Mode: {request.mode} | Latency: {result['latency_ms']:.1f}ms")

        return response

    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        telemetry.record_query(0, [], str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    metrics = telemetry.get_metrics()
    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=metrics["uptime_seconds"]
    )

@app.get("/metrics")
async def metrics():
    """Telemetry metrics endpoint."""
    return telemetry.get_metrics()

@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrines."""
    return {
        "total": len(DOCTRINE_CACHE),
        "by_category": {cat.value: len([d for d in DOCTRINE_CACHE if d.category == cat]) for cat in IssueCategory},
        "doctrines": [{"topic": d.topic, "category": d.category.value, "keywords": d.keywords} for d in DOCTRINE_CACHE]
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} formation evaluation doctrines")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
