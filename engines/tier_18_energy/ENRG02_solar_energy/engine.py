import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

"""
ENRG02 Solar Energy Systems Intelligence Engine
Photovoltaic cell physics, solar technologies, system design, grid integration, storage
Port 9082 | TIE-20 Architecture | Solar Domain Expertise
"""

import asyncio
import hashlib
import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "ENRG02"
ENGINE_NAME = "Solar Energy Systems Intelligence Engine"
VERSION = "1.0.0"
PORT = 9082

logger.add(
    f"logs/{ENGINE_ID}_{{time}}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)


# ============================================================================
# ENUMS AND MODELS
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
    PV_PHYSICS = "PV_PHYSICS"
    PV_TECHNOLOGY = "PV_TECHNOLOGY"
    MODULE_DESIGN = "MODULE_DESIGN"
    INVERTER_SYSTEMS = "INVERTER_SYSTEMS"
    RESOURCE_ASSESSMENT = "RESOURCE_ASSESSMENT"
    SYSTEM_SIZING = "SYSTEM_SIZING"
    MOUNTING_TRACKING = "MOUNTING_TRACKING"
    CSP_SYSTEMS = "CSP_SYSTEMS"
    ENERGY_STORAGE = "ENERGY_STORAGE"
    GRID_INTEGRATION = "GRID_INTEGRATION"
    PERFORMANCE_LOSS = "PERFORMANCE_LOSS"
    CODE_COMPLIANCE = "CODE_COMPLIANCE"
    ADVANCED_PV = "ADVANCED_PV"
    THERMAL_SYSTEMS = "THERMAL_SYSTEMS"
    ECONOMICS = "ECONOMICS"


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=10)
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    categories: List[IssueCategory]
    triggered_doctrines: List[str]
    latency_ms: float
    hash: str
    timestamp: str


@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    category: IssueCategory
    counter_arguments: List[str] = field(default_factory=list)
    resolution_strategy: str = ""
    controlling_precedent: str = ""


# ============================================================================
# DOCTRINE CACHE - 25+ SOLAR ENERGY BLOCKS
# ============================================================================

DOCTRINE_CACHE = [
    DoctrineBlock(
        topic="Photovoltaic Cell Physics - p-n Junction Operation",
        keywords=["p-n junction", "bandgap", "photovoltaic effect", "charge carrier", "electron-hole pair", "depletion region", "built-in potential"],
        conclusion_template=[
            "Photovoltaic cells convert sunlight to electricity through the p-n junction photoelectric effect.",
            "Photon absorption above the semiconductor bandgap energy creates electron-hole pairs that separate in the built-in electric field.",
            "Junction quality and material bandgap fundamentally determine cell efficiency limits."
        ],
        reasoning_framework="""
1. Photon absorption: When photons with energy ≥ bandgap (Eg) strike semiconductor, electron promoted from valence to conduction band
2. Charge separation: Built-in electric field at p-n junction (typically 0.6-1.1V depending on material) separates electron-hole pairs
3. Current generation: Separated charges create photocurrent proportional to incident light intensity
4. Recombination losses: Some carriers recombine before collection, reducing efficiency
5. Bandgap optimization: Silicon bandgap ~1.1 eV optimal for solar spectrum (Shockley-Queisser limit ~33% for single junction)
6. Spectral response: Each material absorbs specific wavelength range based on bandgap
7. Temperature effects: Bandgap decreases with temperature (~-0.002 eV/°C for Si), reducing Voc
8. Doping concentration: Determines depletion width, carrier lifetime, series resistance
9. Surface passivation: Reduces surface recombination velocity, critical for high efficiency
10. Anti-reflection coating: Minimizes reflection losses (4% to <1% for textured+AR coated surface)
        """,
        key_factors=[
            "Semiconductor bandgap energy (determines wavelength cutoff)",
            "p-n junction electric field strength",
            "Carrier diffusion length (must exceed absorption depth)",
            "Surface recombination velocity",
            "Bulk recombination (Shockley-Read-Hall, Auger)",
            "Photon absorption coefficient (function of wavelength)",
            "Temperature coefficient of bandgap",
            "Doping profile and concentration"
        ],
        primary_authority=[
            "Shockley-Queisser limit (detailed balance theory)",
            "IEEE Journal of Photovoltaics (cell physics research)",
            "Green et al. 'Solar Cell Efficiency Tables' (Progress in Photovoltaics)",
            "Sze 'Physics of Semiconductor Devices'",
            "Nelson 'The Physics of Solar Cells'"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PV_PHYSICS,
        counter_arguments=[
            "Multi-junction cells exceed Shockley-Queisser limit (e.g., 47% for concentrated triple-junction)",
            "Hot carrier cells and other advanced concepts may surpass single-junction limits",
            "Quantum dots and intermediate band materials alter conventional bandgap physics"
        ],
        resolution_strategy="Single-junction physics is well-established; advanced concepts require experimental validation and economic viability assessment.",
        controlling_precedent="Shockley-Queisser detailed balance remains fundamental efficiency limit for single-junction cells under 1-sun illumination."
    ),

    DoctrineBlock(
        topic="Monocrystalline vs Polycrystalline Silicon Technology",
        keywords=["monocrystalline", "polycrystalline", "Czochralski", "multicrystalline", "cell efficiency", "cost per watt", "PERC", "PERT"],
        conclusion_template=[
            "Monocrystalline silicon cells offer 20-23% efficiency versus 17-19% for polycrystalline, but at higher manufacturing cost.",
            "Module-level efficiency gaps have narrowed with PERC technology adoption in both cell types.",
            "Selection depends on balance of space constraints, budget, and degradation tolerance."
        ],
        reasoning_framework="""
1. Crystal structure: Monocrystalline = single crystal (Czochralski/float-zone), polycrystalline = multiple grain boundaries
2. Efficiency impact: Grain boundaries in poly increase recombination → lower Voc and efficiency
3. Manufacturing cost: Czochralski process (mono) more energy intensive than directional solidification (poly)
4. Material utilization: Poly uses 100% of ingot, mono wastes ~50% in cylindrical cropping to pseudo-square wafers
5. PERC advancement: Passivated Emitter and Rear Cell technology boosts both types (mono PERC ~22%, poly PERC ~19%)
6. Bifacial capability: Both support bifacial designs, but mono slightly better rear-side response
7. Temperature coefficient: Mono slightly better (~-0.36%/°C vs -0.40%/°C for poly)
8. Degradation: Both exhibit LID (light-induced degradation), but mono can have higher boron-oxygen defect density
9. Aesthetic: Mono appears black/dark blue, poly has blue speckled appearance
10. Market trends: Mono market share increasing (>80% by 2023) due to falling cost premium
        """,
        key_factors=[
            "Efficiency requirement (mono wins if space-limited)",
            "Budget constraints (poly historically cheaper per watt, gap closing)",
            "Degradation tolerance (both ~0.5-0.7%/year after first year)",
            "Temperature coefficient sensitivity in hot climates",
            "Aesthetic preferences for residential applications",
            "Supply chain maturity and module availability"
        ],
        primary_authority=[
            "ITRPV (International Technology Roadmap for Photovoltaics)",
            "Fraunhofer ISE 'Photovoltaics Report'",
            "NREL 'Best Research-Cell Efficiency Chart'",
            "IEC 61215 (module qualification standards for both types)",
            "Manufacturer datasheets (LG, LONGi, JA Solar, Trina)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PV_TECHNOLOGY,
        counter_arguments=[
            "Poly cost advantage disappearing as mono production scales",
            "Thin-film technologies challenge both on cost per watt in utility-scale",
            "Perovskite-silicon tandems may render mono vs poly debate obsolete"
        ],
        resolution_strategy="For most 2024+ projects, mono PERC/TOPCon is default choice unless budget severely constrained or space unconstrained.",
        controlling_precedent="Mono dominance driven by manufacturing scale and incremental efficiency gains outweighing historical cost premium."
    ),

    DoctrineBlock(
        topic="Thin-Film Technologies - CdTe and CIGS",
        keywords=["thin film", "CdTe", "CIGS", "amorphous silicon", "First Solar", "deposition", "temperature coefficient", "low light performance"],
        conclusion_template=[
            "Thin-film CdTe and CIGS modules offer superior temperature coefficients and low-light performance versus crystalline silicon.",
            "CdTe (First Solar) dominates utility-scale thin-film market with 18-19% efficiency and lowest LCOE in sunny climates.",
            "CIGS provides higher efficiency potential (20%+) but faces manufacturing scalability challenges."
        ],
        reasoning_framework="""
1. Deposition process: Thin-film uses vapor deposition on glass/metal substrates, requires 1-2 μm vs 180-200 μm for c-Si
2. CdTe advantages: Simple manufacturing, excellent temp coefficient (-0.25%/°C), lowest energy payback time (~0.5 years)
3. CdTe challenges: Cadmium toxicity perception (actually encapsulated, recyclable), tellurium supply constraints
4. CIGS composition: Copper-Indium-Gallium-Selenide alloy, tunable bandgap by varying In/Ga ratio
5. CIGS advantages: Flexible substrate capability, radiation hardness (space applications), better low-light performance
6. CIGS challenges: Complex 5-element deposition uniformity, indium cost volatility, lower manufacturing yield
7. Amorphous silicon: Lower efficiency (6-9%) but excellent weak-light response, used in consumer electronics
8. Spectral response: Thin-films better matched to diffuse light spectra (cloudy climates)
9. Degradation: CdTe has Staebler-Wronski effect initially, then stabilizes; CIGS very stable
10. Market position: CdTe ~5% global market share, CIGS <2%, c-Si >90% (2024)
        """,
        key_factors=[
            "Climate suitability (thin-film excels in hot, sunny regions)",
            "Space availability (lower Wp/m² than c-Si requires more area)",
            "Spectrum and shading (better diffuse light performance)",
            "Temperature coefficient importance in hot climates",
            "Manufacturing scale (CdTe mature, CIGS niche)",
            "Recycling infrastructure (CdTe 90%+ recyclable)"
        ],
        primary_authority=[
            "First Solar 'Series 6/7 Module Datasheets'",
            "Solar Frontier CIGS specifications",
            "NREL 'Champion Cell Efficiency Chart'",
            "IEC 61646 (thin-film module qualification)",
            "Fthenakis 'Sustainability of Photovoltaics' (toxicity analysis)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PV_TECHNOLOGY,
        counter_arguments=[
            "c-Si efficiency gains eroding thin-film's temperature coefficient advantage",
            "Bifacial c-Si modules can match thin-film's area-normalized performance",
            "Perovskite thin-films may disrupt CdTe/CIGS market with higher efficiency"
        ],
        resolution_strategy="CdTe remains compelling for large-scale desert installations; CIGS for niche applications (building-integrated, flexible); c-Si dominates elsewhere.",
        controlling_precedent="First Solar's vertically integrated CdTe manufacturing achieves lowest LCOE ($0.02-0.03/kWh) in optimal climates."
    ),

    DoctrineBlock(
        topic="Perovskite Solar Cells - Emerging Technology",
        keywords=["perovskite", "tandem", "efficiency", "stability", "degradation", "lead toxicity", "scalability", "Oxford PV"],
        conclusion_template=[
            "Perovskite cells achieved 26% single-junction efficiency and 33%+ in tandem with silicon, but commercialization hindered by stability issues.",
            "Lead-based perovskites raise toxicity concerns; lead-free alternatives sacrifice efficiency.",
            "Technology remains pre-commercial in 2024, requiring 25+ year lifetime demonstration for utility-scale viability."
        ],
        reasoning_framework="""
1. Material structure: Organic-inorganic hybrid with ABX3 crystal structure (e.g., CH3NH3PbI3)
2. Efficiency progress: 3.8% (2009) → 26.1% single-junction (2023), fastest-improving PV technology
3. Tandem advantage: Perovskite (high bandgap ~1.7 eV) on silicon (low bandgap 1.1 eV) exceeds Shockley-Queisser limit
4. Manufacturing simplicity: Solution processing at <150°C vs >1400°C for c-Si, enables flexible substrates
5. Stability challenges: Moisture, oxygen, UV, heat, and ion migration degrade performance (30-50% loss in months)
6. Encapsulation efforts: Advanced barriers extend lifetime but increase cost and reduce benefit vs c-Si
7. Lead toxicity: 0.5-1g Pb per module, orders of magnitude less than lead-acid batteries, but perception issue
8. Lead-free alternatives: Tin (Sn)-based perovskites less toxic but oxidize rapidly, ~15% efficiency vs 26% for Pb
9. Scalability: Slot-die coating, inkjet printing demonstrated, but uniformity over large areas challenging
10. Commercialization: Oxford PV, Swift Solar, Saule Technologies piloting production; no mass deployment yet
        """,
        key_factors=[
            "Stability under outdoor conditions (temperature cycling, humidity, UV)",
            "Scalability to manufacturing-scale area (cm² lab cells vs m² modules)",
            "Lead content regulatory acceptance",
            "Cost advantage over mature c-Si at scale",
            "Tandem architecture yield and complexity",
            "Recycling and end-of-life management"
        ],
        primary_authority=[
            "NREL Perovskite Efficiency Chart",
            "Nature Energy 'Perovskite Stability' reviews",
            "Oxford PV tandem cell announcements",
            "IEC TS 63126 (perovskite module stability protocols)",
            "Snaith et al. perovskite research (Oxford University)"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.PV_TECHNOLOGY,
        counter_arguments=[
            "c-Si incumbents argue perovskite stability unproven for 25-year warranties",
            "Some studies show encapsulated perovskites passing IEC 61215 damp-heat tests",
            "Tandem economics questionable if perovskite layer costs exceed efficiency gain value"
        ],
        resolution_strategy="Monitor for commercial deployments with >10 year operational data; consider for tandem retrofits of existing c-Si plants if stability proven.",
        controlling_precedent="No perovskite modules with verified 25-year outdoor performance as of 2024; technology remains speculative for utility-scale."
    ),

    DoctrineBlock(
        topic="Solar Module Design - Cell Stringing and Bypass Diodes",
        keywords=["cell stringing", "bypass diode", "hot spot", "partial shading", "half-cut cells", "multi-busbar", "shingled cells"],
        conclusion_template=[
            "Standard modules string 60-72 cells in series with 3 bypass diodes to mitigate partial shading losses.",
            "Half-cut cell modules double cell string count, halve current, and improve shading tolerance and hot-spot resistance.",
            "Bypass diode failures cause module underperformance and are a leading O&M issue in fielded systems."
        ],
        reasoning_framework="""
1. Series stringing: Module voltage = sum of cell voltages (~0.5V/cell × 72 = 36V nominal for 12V battery charging)
2. Current uniformity: Series string limited by lowest-current cell, shading one cell chokes entire string
3. Bypass diodes: Parallel 20-24 cells per diode, shunts current around shaded substring (Schottky diodes, ~0.3V drop)
4. Hot-spot prevention: Shaded cell becomes load, dissipates power as heat (can exceed 100°C), bypass diode activates at ~-0.5V
5. Half-cut cells: Laser-cut 156×156mm cells into 156×78mm halves, module now 144 half-cells instead of 72 full
6. Half-cut benefits: Current halved → I²R losses reduced 75%, shading affects smaller area, lower hot-spot risk
7. Multi-busbar (MBB): 9-12 busbars vs 3-5 traditional → lower series resistance, better redundancy if busbar breaks
8. Shingled cells: Overlapping cells eliminate gaps, increases active area ~10%, no visible busbars, better aesthetics
9. Diode failure modes: Short circuit (bypass always on, 1/3 module lost), open circuit (no bypass, hot-spot risk)
10. Junction box: Houses bypass diodes, IP67-rated, thermal stress causes most diode failures
        """,
        key_factors=[
            "Shading environment (trees, soiling, snow → need robust bypass strategy)",
            "Cell technology (PERC, TOPCon, HJT all compatible with half-cut)",
            "Series resistance importance (larger modules benefit more from MBB)",
            "Hot-spot warranty coverage (IEC 61215 requires hot-spot endurance test)",
            "Diode quality and thermal management (junction box design)",
            "Manufacturing complexity (shingled requires precision alignment)"
        ],
        primary_authority=[
            "IEC 61215 Section 10.18 (Hot-Spot Endurance Test)",
            "IEC 61730 (module safety, bypass diode requirements)",
            "Infineon/Vishay bypass diode datasheets (thermal limits)",
            "LONGi, Trina, JA Solar module design guides",
            "IEEE 'Bypass Diode Failures in PV Modules' studies"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MODULE_DESIGN,
        counter_arguments=[
            "Some argue bypass diodes unnecessary in unshaded utility-scale systems",
            "Cell-level power electronics (microinverters) eliminate need for bypass diodes",
            "Advanced module designs (shingled, IBC) have different bypass requirements"
        ],
        resolution_strategy="Bypass diodes remain essential for residential/commercial (shading likely); half-cut+MBB is industry standard; monitor junction box temps.",
        controlling_precedent="IEC 61215 mandates bypass diode hot-spot test; all certified modules must include appropriate bypass protection."
    ),

    DoctrineBlock(
        topic="Inverter Technologies - String vs Micro vs Central",
        keywords=["string inverter", "microinverter", "central inverter", "MPPT", "module-level power electronics", "Enphase", "SolarEdge", "power optimizer"],
        conclusion_template=[
            "String inverters dominate utility-scale (lowest $/W), microinverters dominate residential (module-level optimization), central inverters for >1 MW plants.",
            "Microinverters eliminate single point of failure but cost 2-3× per watt versus string inverters.",
            "Power optimizers (SolarEdge) offer middle ground: module-level MPPT with centralized DC-AC conversion."
        ],
        reasoning_framework="""
1. String inverter: 1-50 kW, connects 8-12 modules per MPPT input (1-3 MPPT channels), $0.10-0.15/W
2. Microinverter: 200-400 W per module, AC-coupled at module level, $0.25-0.35/W (Enphase IQ8)
3. Central inverter: 500 kW-3 MW, utility-scale, connects 1000s of modules, $0.05-0.08/W
4. MPPT importance: Extracts maximum power (Vmp × Imp) despite varying irradiance/temperature
5. String inverter MPPT limitation: All modules in string must operate at same voltage, shading kills string efficiency
6. Microinverter advantage: Each module independently optimized, shading affects only that module, no high-voltage DC
7. Microinverter disadvantages: Higher cost, more failure points (electronics on roof in harsh environment), AC wiring complexity
8. Power optimizer (SolarEdge): DC-DC converter per module, central DC-AC inverter, module-level monitoring, $0.18-0.22/W
9. Reliability: String inverter 10-15 year lifespan, microinverter 25 year design (matches module), central inverter 20+ with maintenance
10. Rapid shutdown: NEC 2017 requires module-level shutdown, favors microinverters/optimizers (string inverters need add-on devices)
        """,
        key_factors=[
            "System size (residential <10 kW → micro, commercial 10-500 kW → string, utility >500 kW → central)",
            "Shading environment (severe shading → micro/optimizer, open field → string/central)",
            "Cost sensitivity (utility-scale ruthlessly cost-optimized → central)",
            "Monitoring granularity requirements (module-level → micro/optimizer)",
            "Rapid shutdown compliance (NEC 2017+ in US)",
            "Maintenance accessibility (roof-mounted micros harder to service)"
        ],
        primary_authority=[
            "SMA, Fronius, SolarEdge, ABB string inverter datasheets",
            "Enphase IQ8 microinverter specifications",
            "NEC Article 690.12 (Rapid Shutdown Requirements)",
            "IEEE 1547-2018 (grid interconnection standards for all inverter types)",
            "NREL 'Inverter Reliability and Failure Modes' studies"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.INVERTER_SYSTEMS,
        counter_arguments=[
            "String inverter costs falling faster than microinverter due to scale",
            "Battery-integrated inverters (hybrid) changing economics",
            "Module-level electronics (MLPE) commoditizing, closing cost gap"
        ],
        resolution_strategy="Use microinverters for shaded residential, string for open commercial, central for utility; optimizer if granular monitoring needed without micro cost.",
        controlling_precedent="Market segmentation stable: microinverters ~15% residential, string inverters ~70% commercial, central inverters ~15% utility (US, 2024)."
    ),

    DoctrineBlock(
        topic="MPPT Algorithms - Perturb and Observe vs Incremental Conductance",
        keywords=["MPPT", "maximum power point tracking", "perturb and observe", "incremental conductance", "efficiency", "irradiance", "P&O algorithm"],
        conclusion_template=[
            "Perturb and Observe (P&O) MPPT dominates commercial inverters due to simplicity and 98-99% efficiency under steady conditions.",
            "Incremental Conductance offers faster response to rapid irradiance changes but requires more computational overhead.",
            "Modern inverters combine P&O with adaptive step sizes and irradiance sensors for optimal performance."
        ],
        reasoning_framework="""
1. MPPT necessity: PV I-V curve has single maximum power point (MPP) that shifts with irradiance and temperature
2. P&O algorithm: Perturb voltage, observe power change; if power increases, continue direction; if decreases, reverse
3. P&O advantages: Simple, low computational cost, proven reliable, handles multiple local maxima from partial shading
4. P&O disadvantages: Oscillates around MPP (wastes 1-2%), slow response to rapidly changing conditions, confused by fast irradiance changes
5. Incremental Conductance: Compares instantaneous conductance (I/V) to incremental conductance (dI/dV), stops exactly at MPP
6. InCond advantages: Zero steady-state oscillation, faster transient response, better under rapidly changing irradiance
7. InCond disadvantages: More complex math (requires accurate current/voltage sensors), can be confused by noise
8. Adaptive P&O: Modern variant adjusts perturbation step size based on distance from MPP (large steps far away, small steps near MPP)
9. Hybrid approaches: Combine P&O with irradiance sensor (pyranometer) to predict MPP shift direction
10. Efficiency impact: P&O ~98-99%, InCond ~99-99.5%, difference marginal in real-world annual energy
        """,
        key_factors=[
            "Irradiance variability (cloudy climates favor InCond, stable climates P&O fine)",
            "Computational resources (low-cost inverters stick with P&O)",
            "Partial shading severity (multiple local maxima challenge all algorithms)",
            "Response time requirements (utility-scale has slower dynamics than residential)",
            "Sensor accuracy (InCond needs precise I/V measurement)",
            "Energy yield vs cost tradeoff (incremental efficiency gain vs algorithm complexity)"
        ],
        primary_authority=[
            "IEEE 'Comparison of MPPT Algorithms' studies",
            "Inverter manufacturer white papers (SMA, Fronius)",
            "IEC 61683 (inverter efficiency measurement procedures)",
            "Esram & Chapman 'Comparison of Photovoltaic MPPT Techniques' (comprehensive review)",
            "NREL inverter testing protocols"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.INVERTER_SYSTEMS,
        counter_arguments=[
            "Some argue InCond theoretical advantages don't translate to field performance",
            "Advanced algorithms (fuzzy logic, neural networks) outperform both in research but not commercialized",
            "Module-level MPPT (microinverters) makes algorithm choice less critical"
        ],
        resolution_strategy="P&O with adaptive step size is industry standard; InCond used in premium inverters; marginal energy difference doesn't justify complex alternatives.",
        controlling_precedent="Commercial inverters converge on P&O variants; California Energy Commission (CEC) efficiency testing shows <0.5% difference between algorithms."
    ),

    DoctrineBlock(
        topic="Solar Resource Assessment - GHI, DNI, DHI",
        keywords=["GHI", "DNI", "DHI", "irradiance", "TMY", "NSRDB", "pyranometer", "solar resource", "insolation"],
        conclusion_template=[
            "Global Horizontal Irradiance (GHI) is the total solar radiation on a horizontal surface, comprising Direct Normal Irradiance (DNI) and Diffuse Horizontal Irradiance (DHI).",
            "Accurate site assessment requires multi-year TMY (Typical Meteorological Year) data to account for interannual variability.",
            "Ground-based pyranometer measurements for 1+ years preferred over satellite models for bankable project financing."
        ],
        reasoning_framework="""
1. GHI definition: Total shortwave radiation (0.3-3 μm) received on horizontal surface (W/m²), GHI = DNI × cos(θ) + DHI
2. DNI definition: Direct beam radiation from solar disk, measured perpendicular to sun (requires sun-tracking pyrheliometer)
3. DHI definition: Diffuse/scattered radiation from sky dome, excludes direct beam (measured with shadow band blocking sun)
4. Spatial variability: GHI can vary 10-20% over 10 km due to local weather, topography, aerosols
5. Temporal variability: Year-to-year GHI variation ±5-10%, critical for P50/P90 energy predictions
6. TMY data: Synthesized year using 12 typical months from 30-year dataset, represents long-term average
7. Satellite models: NSRDB (US), PVGIS (Europe), Solargis (global), ±5-10% accuracy vs ground measurements
8. Ground measurement: Class 1 pyranometer (ISO 9060) achieves ±2-3% accuracy with proper calibration
9. Albedo consideration: Ground-reflected radiation, typically 20% for grass, 80% for snow, affects bifacial modules
10. Spectral effects: AM (air mass) affects spectrum, not just intensity; relevant for multi-junction cells
        """,
        key_factors=[
            "Project size (utility-scale mandates ground measurement campaign)",
            "Financing requirements (lenders require P90 bankable data)",
            "Satellite data validation (compare to nearby ground stations)",
            "Shading analysis (far-field vs near-field obstacles)",
            "Measurement duration (1 year minimum, 2+ preferred)",
            "Sensor calibration and maintenance (ISO 17025 accredited lab)"
        ],
        primary_authority=[
            "NREL NSRDB (National Solar Radiation Database)",
            "ISO 9060:2018 (solar irradiance classification)",
            "IEC 61724-1 (PV system monitoring)",
            "WMO Guide to Instruments and Methods of Observation",
            "SolarAnywhere, Solargis, Meteonorm datasets"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.RESOURCE_ASSESSMENT,
        counter_arguments=[
            "Some argue satellite models sufficient for small systems (<100 kW)",
            "Climate change may invalidate 30-year TMY datasets",
            "Advanced satellite models (SolarAnywhere FlashFlux) claim <5% error, rivaling ground data"
        ],
        resolution_strategy="For >1 MW projects, conduct 1-year ground measurement campaign; for smaller systems, use validated satellite data with P90 uncertainty adjustments.",
        controlling_precedent="IEC 61724-1 defines irradiance measurement standards; lenders typically require P90 energy estimate with ground-validated data for >$10M projects."
    ),

    DoctrineBlock(
        topic="PV System Sizing Methodology - DC-to-AC Ratio",
        keywords=["DC-to-AC ratio", "inverter loading ratio", "ILR", "system sizing", "clipping losses", "peak power", "capacity factor"],
        conclusion_template=[
            "DC-to-AC ratio (ILR) typically ranges 1.2-1.3 for utility-scale systems, balancing inverter utilization against clipping losses.",
            "Higher ILR (1.3-1.5) justified in high-irradiance regions where clipping <2% annually but inverter utilization improves significantly.",
            "Optimal ILR depends on irradiance profile, electricity pricing (ToU), and inverter/module cost ratio."
        ],
        reasoning_framework="""
1. ILR definition: DC array size (kWp STC) ÷ AC inverter rating (kWac), e.g., 1000 kWp / 800 kWac = 1.25 ILR
2. Under-sizing inverter rationale: Array rarely reaches STC (25°C, 1000 W/m²), typical outdoor temps 40-60°C reduce power 10-20%
3. Clipping losses: When array produces >inverter rating, excess DC power discarded, occurs during peak irradiance hours
4. Clipping tolerance: 1-3% annual clipping acceptable, occurs <100 hours/year in most climates, affects only peak production
5. Inverter utilization: Higher ILR keeps inverter near rated capacity more hours/day → better $/kWh economics
6. Cost tradeoff: Modules declining faster than inverters (2024: modules ~$0.20/W, inverters ~$0.08/W) → favors higher ILR
7. ToU pricing: Higher ILR clips peak midday production, but utility often pays less for midday power (duck curve), more for evening → can optimize ILR for revenue
8. Degradation: As modules degrade 0.5-0.7%/year, year-1 clipping becomes year-10 no-clipping, ILR effectively decreases over life
9. Geographic variation: High-irradiance deserts (Arizona) tolerate ILR 1.4+, moderate climates (Germany) use 1.1-1.2
10. Bifacial impact: Rear-side gain (5-20%) can push ILR higher without clipping penalty
        """,
        key_factors=[
            "Site irradiance profile (high-GHI sites benefit from higher ILR)",
            "Module vs inverter cost ratio (wider gap favors higher ILR)",
            "Electricity pricing structure (ToU tariffs affect optimal clipping tolerance)",
            "Degradation rate (plan for year-20 performance, not just year-1)",
            "Regulatory limits (some utilities cap ILR at 1.3)",
            "Inverter overload capability (some can handle 110-120% for short periods)"
        ],
        primary_authority=[
            "NREL 'System Advisor Model (SAM)' ILR optimization",
            "IEEE 'Optimal Inverter Sizing' studies",
            "California Rule 21 (interconnection ILR guidelines)",
            "SMA, SolarEdge inverter datasheets (overload ratings)",
            "DNV GL 'PV System Design Best Practices'"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SYSTEM_SIZING,
        counter_arguments=[
            "Some argue ILR >1.3 wastes module investment on clipped energy",
            "Battery storage changes optimal ILR (can store clipped energy)",
            "Advanced inverter controls (reactive power) may prefer lower ILR for VA capacity"
        ],
        resolution_strategy="Model site-specific LCOE with SAM/PVsyst over range of ILR; typically 1.25-1.30 optimizes for utility-scale, 1.15-1.25 for commercial.",
        controlling_precedent="Industry standard ILR 1.2-1.3 for utility, 1.1-1.25 for residential/commercial; higher ILR trend driven by module cost declines."
    ),

    DoctrineBlock(
        topic="Fixed-Tilt vs Single-Axis Tracker Systems",
        keywords=["fixed tilt", "single-axis tracker", "dual-axis tracker", "tracker", "tilt angle", "azimuth", "energy gain", "land use", "NEXTracker"],
        conclusion_template=[
            "Single-axis trackers increase energy yield 15-25% versus fixed-tilt but add $0.03-0.06/W in CapEx and require more O&M.",
            "Trackers economically favored in utility-scale (>5 MW) with open, flat land and high irradiance; fixed-tilt for rooftop and constrained sites.",
            "Dual-axis trackers offer marginal gain (3-5%) over single-axis at significant cost premium; rarely deployed."
        ],
        reasoning_framework="""
1. Fixed-tilt angle: Typically latitude ±5-15° (e.g., 30° tilt at 35°N), maximizes annual energy, no moving parts
2. Single-axis tracker: Rotates around N-S axis, follows sun E-W (azimuth tracking), 0-60° tilt range
3. Dual-axis tracker: Rotates on two axes (azimuth + elevation), always perpendicular to sun, complex mechanics
4. Energy gain: Single-axis +15-25% vs fixed-tilt (higher gain in sunny climates), dual-axis +25-35%
5. Tracker cost: Single-axis adds ~$0.03-0.06/W, dual-axis ~$0.15-0.25/W (NEXTracker, Array Technologies)
6. Land use: Trackers require 1.5-2× spacing vs fixed-tilt to avoid row-to-row shading, but capture more energy per unit area in high-GHI sites
7. O&M: Trackers have motors, gearboxes, controllers that fail; typical 1-2%/year O&M cost vs 0.5-1% for fixed
8. Wind loading: Trackers stow flat (0° tilt) in high wind to reduce loads, design for 90 mph gusts
9. Terrain suitability: Trackers require <5° slope, flat grading increases site prep costs vs fixed-tilt on uneven terrain
10. Snow/ice: Trackers in cold climates struggle with icing, can't rotate, fixed-tilt sheds snow better at steep angles
        """,
        key_factors=[
            "Site GHI and DNI/DHI ratio (high DNI favors trackers, high diffuse favors fixed)",
            "Land cost and availability (expensive/constrained land → fixed with higher density)",
            "Terrain slope and grading cost (rough terrain → fixed-tilt)",
            "O&M capability (remote sites without maintenance access → fixed)",
            "Financing terms (trackers have higher CapEx but better LCOE)",
            "Climate (wind, snow, hail risk affects tracker viability)"
        ],
        primary_authority=[
            "NREL 'Tracking the Sun' reports",
            "NEXTracker, Array Technologies tracker datasheets",
            "IEC 62817 (tracker system design requirements)",
            "Wood Mackenzie 'Global Solar Tracker Market' analysis",
            "IEEE 'Fixed vs Tracking PV System Economics' studies"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MOUNTING_TRACKING,
        counter_arguments=[
            "Some argue tracker reliability now matches fixed-tilt with 25-year warranties",
            "Bifacial modules on trackers gain additional 5-10% rear-side boost",
            "Advanced controls (backtracking algorithm) mitigate row-to-row shading, improving energy yield"
        ],
        resolution_strategy="For utility-scale in high-DNI regions (>5.5 kWh/m²/day GHI), single-axis trackers standard; fixed-tilt for rooftop, distributed, or complex terrain.",
        controlling_precedent="70%+ of US utility-scale solar (2020-2024) uses single-axis trackers; fixed-tilt remains dominant for rooftop and international markets."
    ),

    DoctrineBlock(
        topic="Concentrated Solar Power - Parabolic Trough vs Power Tower",
        keywords=["CSP", "concentrated solar power", "parabolic trough", "power tower", "molten salt", "thermal storage", "Ivanpah", "SEGS", "heliostat"],
        conclusion_template=[
            "Concentrated Solar Power stores thermal energy in molten salt, enabling dispatchable solar generation without batteries.",
            "Parabolic troughs are mature technology (30+ years) but limited to ~400°C; power towers achieve 565°C, higher efficiency.",
            "CSP economically challenged by PV+battery cost declines; new CSP projects <1 GW/year globally versus >200 GW PV."
        ],
        reasoning_framework="""
1. CSP principle: Mirrors concentrate sunlight 100-1000× onto receiver, heat transfer fluid (HTF) reaches 300-700°C, drives steam turbine
2. Parabolic trough: Long curved mirrors focus on tube receiver, synthetic oil HTF, 400°C max, 30 years commercial experience (SEGS plants)
3. Power tower: Field of heliostats (mirrors) focus on central receiver atop tower, molten salt HTF (60% NaNO3, 40% KNO3), 565°C
4. Thermal storage: Molten salt (cold tank 290°C, hot tank 565°C) stores 6-15 hours, enables generation after sunset (dispatchable)
5. Efficiency: Trough ~15-16%, tower ~18-20%, vs PV 20-23% (but CSP includes free storage)
6. DNI requirement: CSP needs >5.5 kWh/m²/day DNI, only viable in deserts (SW US, MENA, Australia)
7. Cost: CSP $4-6/W vs PV+battery $1-2/W (2024), CSP uncompetitive except in niche markets (Chile, South Africa)
8. Water use: Wet cooling for steam cycle consumes 800-1000 gal/MWh, dry cooling reduces efficiency 5-10%
9. Capacity factor: CSP with storage achieves 40-50% CF vs 25-30% for PV without storage
10. Hybridization: Some plants add natural gas burner for cloudy days (Solana, Arizona)
        """,
        key_factors=[
            "DNI resource quality (CSP requires excellent DNI, PV tolerates diffuse)",
            "Dispatchability requirement (grid needs evening/night generation → CSP, but battery cost falling)",
            "Water availability (arid CSP sites often water-scarce, dry cooling penalty)",
            "Scale (CSP economics require 50-300 MW, PV scales to 1 MW+)",
            "Long-term storage need (CSP 6-15 hours vs lithium 2-4 hours)",
            "Technology maturity (CSP high risk, PV proven)"
        ],
        primary_authority=[
            "NREL 'Concentrating Solar Power Projects' database",
            "Abengoa, BrightSource Energy (CSP developers)",
            "IEA 'Technology Roadmap: Solar Thermal Electricity'",
            "Crescent Dunes (power tower, Nevada), Solana (trough, Arizona) operational data",
            "SENER 'CSP Technology Assessment'"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.CSP_SYSTEMS,
        counter_arguments=[
            "CSP advocates argue thermal storage cheaper than batteries at >6 hour duration",
            "Some models show CSP competitive in markets with high capacity payments",
            "Next-generation CSP (supercritical CO2 turbines) may close efficiency gap"
        ],
        resolution_strategy="CSP niche limited to ultra-high DNI regions with dispatchability premium and long-duration storage needs; PV+battery dominates elsewhere.",
        controlling_precedent="Global CSP capacity ~6.5 GW (2024) vs PV >1,600 GW; CSP pipeline collapsing except Chile, China, UAE with specific policy support."
    ),

    DoctrineBlock(
        topic="Battery Storage Integration - Lithium-Ion vs Flow Batteries",
        keywords=["battery storage", "lithium-ion", "flow battery", "energy storage", "BESS", "Tesla Megapack", "vanadium redox", "duration"],
        conclusion_template=[
            "Lithium-ion dominates 2-4 hour duration storage (>95% market share) with costs below $300/kWh; flow batteries target 6-12 hour duration.",
            "Li-ion degradation (80% capacity at 10-15 years) manageable with warranty guarantees; flow batteries offer longer lifetime but higher upfront cost.",
            "PV+battery systems achieving LCOE <$0.04/kWh in sunny regions, competitive with natural gas peaker plants."
        ],
        reasoning_framework="""
1. Li-ion dominance: 95%+ of utility-scale storage, LFP (lithium iron phosphate) ~$250/kWh, NMC ~$300/kWh (2024)
2. Li-ion advantages: High round-trip efficiency (90-95%), compact footprint, mature supply chain (Tesla, CATL, BYD)
3. Li-ion challenges: Degradation (cycle life 5,000-10,000 cycles to 80% capacity), thermal runaway fire risk (mitigated by LFP chemistry)
4. Flow battery principle: Liquid electrolytes in external tanks, power (stack) and energy (tanks) independently scalable
5. Flow battery types: Vanadium redox (VRFB), zinc-bromine, iron-chromium, organic (aqueous)
6. Flow advantages: 20+ year lifetime, 10,000+ cycles, no capacity fade, non-flammable electrolytes
7. Flow disadvantages: Low energy density (2-3× footprint vs Li-ion), higher CapEx ($500-800/kWh), lower efficiency (70-80%)
8. Duration economics: Flow batteries competitive at >6 hour duration (energy cost dominates over power cost)
9. PV coupling: DC-coupled BESS charges directly from array (higher efficiency, lower cost), AC-coupled more flexible (retrofit)
10. Grid services: BESS provides frequency regulation, voltage support, black start, capacity firming for PV intermittency
        """,
        key_factors=[
            "Duration requirement (2-4 hours → Li-ion, 6-12 hours → consider flow)",
            "Cycle depth and frequency (daily cycling favors Li-ion, infrequent deep cycles OK for flow)",
            "Lifetime and degradation tolerance (flow better for 20+ year projects)",
            "Safety requirements (LFP for safety-critical, flow for no-fire zones)",
            "Footprint constraints (Li-ion for space-limited, flow for land-abundant)",
            "Temperature extremes (flow batteries struggle <10°C, Li-ion needs cooling >40°C)"
        ],
        primary_authority=[
            "Tesla Megapack, BYD, CATL battery datasheets",
            "Invinity Energy (VRFB), ESS Inc (iron flow) specifications",
            "NREL 'Cost Projections for Utility-Scale Battery Storage'",
            "BloombergNEF 'Battery Price Survey' (annual)",
            "IEEE 'Energy Storage for Renewable Integration' standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ENERGY_STORAGE,
        counter_arguments=[
            "Flow battery costs falling faster than Li-ion in some forecasts",
            "Second-life EV batteries may disrupt utility storage economics",
            "Alternative chemistries (sodium-ion, iron-air) could challenge both Li-ion and flow"
        ],
        resolution_strategy="Li-ion default for 2-4 hour duration; consider flow batteries only for >8 hour duration or 20+ year degradation-free requirement.",
        controlling_precedent="Utility-scale storage deployments: >40 GWh Li-ion installed globally 2023, <500 MWh flow batteries; Li-ion market dominance unchallenged."
    ),

    DoctrineBlock(
        topic="Grid-Tied vs Off-Grid System Design",
        keywords=["grid-tied", "off-grid", "net metering", "islanding", "battery backup", "grid interconnection", "IEEE 1547", "anti-islanding"],
        conclusion_template=[
            "Grid-tied systems dominate (>95% of installations) due to lower cost (no battery requirement) and net metering revenue.",
            "Off-grid systems require battery storage, genset backup, and 50-100% oversizing for seasonal variability, increasing cost 3-5×.",
            "Hybrid systems with grid connection and battery backup offer resilience without full off-grid cost penalty."
        ],
        reasoning_framework="""
1. Grid-tied operation: PV feeds excess to grid, imports when PV insufficient, no storage required, inverter syncs to grid frequency/voltage
2. Net metering: Utility credits customer for exported kWh at retail rate (varies by state, some reduce to wholesale rate)
3. Grid-tied cost: ~$2-3/W installed (residential) without battery, simple permitting, standard inverters
4. Off-grid requirements: Battery bank (3-7 days autonomy), charge controller, genset backup (cloudy weather), DC-AC inverter
5. Off-grid sizing: Must cover worst-case month (winter for most northern climates), typically 2-3× summer array size
6. Off-grid cost: $6-12/W installed (battery dominates cost), complex sizing (must avoid outages)
7. IEEE 1547: Grid interconnection standard, requires anti-islanding protection (inverter shuts off if grid down)
8. Anti-islanding: Prevents PV energizing dead grid (safety hazard for utility workers), <2 second detection required
9. Hybrid systems: Grid-connected with battery backup, best of both worlds, inverter switches to off-grid mode during outages
10. Microgrid: Multi-building system with PV+battery+genset, can island from main grid, common for military bases, remote communities
        """,
        key_factors=[
            "Grid reliability (frequent outages → battery backup, unreliable grid → off-grid)",
            "Net metering policy (generous NEM → grid-tied, no NEM → consider storage)",
            "Utility connection cost (remote sites with >$50K connection cost → off-grid viable)",
            "Load criticality (medical equipment, telecom → need battery backup)",
            "Seasonal variability (high winter/summer ratio → off-grid challenging)",
            "Genset fuel availability (off-grid requires propane/diesel backup)"
        ],
        primary_authority=[
            "IEEE 1547-2018 (interconnection standard)",
            "NEC Article 690 (grid-tied) and 705 (interconnection)",
            "California Rule 21 (interconnection procedures)",
            "UL 1741 (inverter safety, anti-islanding certification)",
            "State net metering policies (DSIRE database)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.GRID_INTEGRATION,
        counter_arguments=[
            "Net metering phase-out in some states reduces grid-tied economics",
            "Battery costs declining may favor hybrid over pure grid-tied",
            "Virtual power plants (VPPs) aggregate distributed batteries, change value proposition"
        ],
        resolution_strategy="Grid-tied default unless utility unreliable or >$20K connection cost; hybrid for critical loads; off-grid only for remote sites with no grid option.",
        controlling_precedent="Grid-tied systems constitute >95% of US residential solar; off-grid niche limited to remote cabins, RVs, and developing world applications."
    ),

    DoctrineBlock(
        topic="PV System Losses - Soiling, Shading, Mismatch, Temperature",
        keywords=["soiling loss", "shading loss", "module mismatch", "temperature coefficient", "system losses", "derate factors", "PVsyst"],
        conclusion_template=[
            "Real-world PV systems lose 15-30% of theoretical STC output due to soiling, shading, temperature, mismatch, wiring, and inverter losses.",
            "Soiling losses vary 1-10%/year depending on climate (deserts with rain <10%/year, industrial areas 5-8%, clean rural 1-2%).",
            "Temperature derate is ~10-15% in hot climates; modules rated at 25°C but operate at 45-65°C in summer."
        ],
        reasoning_framework="""
1. STC rating: Module tested at 25°C, 1000 W/m², AM1.5 spectrum, clean, no shading, 0 resistance → never achieved in field
2. Soiling: Dust, pollen, bird droppings block light, 0.1-0.5%/day accumulation, rain cleans, manual cleaning 2-4×/year in deserts
3. Soiling mitigation: Anti-soiling coatings, robotic cleaning, tracker backtracking to shed dust, tilt >15° for self-cleaning
4. Shading: Trees, buildings, poles, clouds, row-to-row shading in morning/evening, use PVsyst/HelioScope 3D shading analysis
5. Module mismatch: Manufacturing tolerance (±3%), degradation rate variation, partial shading create current mismatch in series string
6. Temperature loss: Typical temp coefficient -0.35%/°C, 40°C delta (65°C operation - 25°C STC) = -14% power loss
7. Temperature mitigation: Roof-mounted has better airflow than ground-mounted, white/reflective roofs reduce module temp 5-10°C
8. DC wiring loss: Resistive loss I²R, keep <2% by upsizing wire gauge, minimize string length
9. Inverter loss: 96-98.5% peak efficiency, lower at partial load, stand-by consumption 5-20 W
10. Total derate: PVsyst typically models 75-85% performance ratio (AC output / DC STC rating × irradiance)
        """,
        key_factors=[
            "Climate (rain frequency affects soiling, ambient temp affects temperature loss)",
            "Tilt angle (steeper sheds soiling better, but reduces energy capture in low latitudes)",
            "O&M budget (manual cleaning vs robotic vs rain-only)",
            "Shade environment (urban vs rural, deciduous trees vs evergreen)",
            "Wire sizing (economics of larger gauge vs loss tolerance)",
            "Inverter sizing (ILR affects part-load efficiency)"
        ],
        primary_authority=[
            "NREL 'System Advisor Model (SAM)' default loss assumptions",
            "PVsyst software loss modeling",
            "IEC 61724-1 (performance monitoring, loss quantification)",
            "NREL 'Soiling Loss Studies' (regional data)",
            "IEEE 'PV System Performance Modeling' standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PERFORMANCE_LOSS,
        counter_arguments=[
            "Some argue bifacial modules compensate for soiling with rear-side gain",
            "Advanced inverters with better partial-load efficiency reduce inverter loss <1%",
            "Climate change may alter soiling and temperature assumptions in long-term models"
        ],
        resolution_strategy="Model losses conservatively: soiling 3-5%, temperature 12-15%, shading 1-5%, mismatch 2%, wiring 2%, inverter 2-4%; total derate 75-85%.",
        controlling_precedent="Industry-standard performance ratio 75-85%; below 75% indicates design or O&M issues; above 85% rare, achieved only in ideal conditions."
    ),

    DoctrineBlock(
        topic="NEC Article 690 - Code Compliance",
        keywords=["NEC 690", "rapid shutdown", "arc fault", "grounding", "disconnect", "AFCI", "module-level shutdown", "NEC 2017"],
        conclusion_template=[
            "NEC Article 690 governs PV system electrical safety, mandating rapid shutdown (2017+), arc-fault detection (2011+), and equipment grounding.",
            "Rapid shutdown requires module-level de-energization to <80V within 30 seconds of switch actuation, favoring microinverters and optimizers.",
            "Arc-fault circuit interrupters (AFCI) detect series arcing in DC wiring, nuisance trip rate improved in 2020+ inverters but remains O&M concern."
        ],
        reasoning_framework="""
1. NEC 690.12 rapid shutdown: Conductor voltage >1 ft from array perimeter must drop to ≤80V within 30 sec (firefighter safety)
2. Rapid shutdown methods: Module-level shutdown (MLSD) devices (microinverter, optimizer), array-level switch with conductor distance <1 ft
3. NEC 690.11 arc-fault protection: PV inverters must detect and interrupt DC arc faults, series arcs (loose connections) most common
4. AFCI challenges: Nuisance trips from switching events, EMI, requires firmware tuning, some early systems had 5-10% annual trip rate
5. Grounding: Equipment grounding required for all metal parts (frames, racking), prevents shock hazard
6. Grounding controversy: Ungrounded (floating) systems have higher efficiency, lower leakage current, but require isolation monitoring
7. NEC 690.15 disconnects: Readily accessible disconnect required to isolate PV from building, with lockout/tagout capability
8. NEC 690.35 ungrounded systems: Allowed if inverter monitors insulation resistance, detects ground faults, shuts down if fault occurs
9. String sizing: NEC 690.7 limits Voc to inverter max input voltage × 1.25 safety factor (accounts for cold temperature Voc increase)
10. Conduit/wiring: NEC 690.31 specifies UV-resistant wire for exposed sections, conduit for embedded in walls/roofs
        """,
        key_factors=[
            "NEC code cycle (2017/2020/2023 editions differ on rapid shutdown details)",
            "AHJ interpretation (Authority Having Jurisdiction may enforce stricter than code)",
            "Inverter technology (string inverters need add-on MLSD devices, micros inherently compliant)",
            "Inspection requirements (some jurisdictions require pre-inspection of shutdown function)",
            "Retrofit considerations (upgrading 2008-2014 systems to current code complex)",
            "Insurance requirements (some insurers mandate rapid shutdown regardless of code)"
        ],
        primary_authority=[
            "NFPA 70 National Electrical Code Article 690 (PV Systems)",
            "NEC 2017/2020/2023 editions (rapid shutdown evolution)",
            "UL 1741 (inverter/MLSD device certification)",
            "SolarABCs 'Expedited Permit Process' (NEC compliance guide)",
            "IAEI (International Association of Electrical Inspectors) interpretations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CODE_COMPLIANCE,
        counter_arguments=[
            "Some argue rapid shutdown adds cost/complexity without proven safety benefit (few firefighter injuries from PV)",
            "Ungrounded systems have safety advantages (no ground fault current) but NEC conservative",
            "AFCI nuisance trips may create fire risk by causing system downtime in hot weather"
        ],
        resolution_strategy="Comply with NEC 2017+ rapid shutdown using MLSD devices for new systems; retrofit older systems if selling/refinancing; use certified AFCI inverters.",
        controlling_precedent="NEC 690.12 rapid shutdown mandatory in all US jurisdictions adopting NEC 2017 or later; microinverters/optimizers market share driven partly by code."
    ),

    DoctrineBlock(
        topic="Bifacial Modules and Albedo",
        keywords=["bifacial", "albedo", "rear side gain", "bifaciality factor", "ground cover ratio", "GCR", "LONGi", "JA Solar"],
        conclusion_template=[
            "Bifacial modules capture reflected light on rear side, increasing energy yield 5-20% depending on albedo and mounting height.",
            "Albedo varies from 20% (grass) to 80% (snow); white surfaces (gravel, sand) achieve 30-50% and boost bifacial gain.",
            "Bifacial economics depend on GCR (ground cover ratio): lower GCR allows more rear irradiance but requires more land."
        ],
        reasoning_framework="""
1. Bifacial principle: Transparent backsheet or dual-glass construction allows light to enter rear of cell, generate power from reflected/diffuse light
2. Bifaciality factor: Rear-side efficiency as percentage of front, typically 70-85% (e.g., 400W front × 0.75 bifaciality = 300W max rear)
3. Albedo impact: Snow 80%, white gravel 40%, concrete 30%, grass 20%, soil 15%, asphalt 10% → determines available rear irradiance
4. Height effect: Higher mounting (1.5-2m vs 0.5m) increases rear irradiance 2-5% by reducing ground self-shading
5. GCR tradeoff: Low GCR (0.3-0.4) maximizes bifacial gain (more ground visible to rear) but wastes land, high GCR (0.5-0.6) reduces gain but uses land efficiently
6. Trackers + bifacial: Single-axis trackers with bifacial gain additional 5-10% vs monofacial on tracker (backtracking reduces rear shading)
7. Modeling complexity: PVsyst, SAM model bifacial with view factor calculations, 3D ray tracing for accurate prediction
8. Cost premium: Bifacial modules cost 2-5% more than monofacial, dual-glass heavier (requires stronger racking), but LCOE lower due to yield
9. Degradation: Dual-glass more resistant to PID (potential-induced degradation) and moisture ingress, may have better 25-year degradation
10. Market adoption: 40%+ of modules shipped in 2023 were bifacial (utility-scale), dominant in high-albedo environments (Middle East deserts)
        """,
        key_factors=[
            "Albedo of site (desert/snow → high gain, forest/asphalt → low gain)",
            "Mounting height budget (higher = better rear irradiance)",
            "Land cost (cheap land → lower GCR, expensive → higher GCR)",
            "Tracker compatibility (trackers amplify bifacial gain)",
            "Soiling on rear side (dust accumulation reduces bifacial benefit)",
            "Module weight limits (dual-glass 25-30 kg vs monofacial 20-22 kg)"
        ],
        primary_authority=[
            "LONGi, JA Solar, Trina bifacial module datasheets",
            "IEC TS 60904-1-2 (bifacial measurement standard)",
            "NREL 'Bifacial PV Performance Modeling' studies",
            "PVsyst bifacial modeling documentation",
            "Sandia National Labs 'Bifacial Performance Models'"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ADVANCED_PV,
        counter_arguments=[
            "Some argue bifacial gains overstated in models, real-world lower due to soiling/shading",
            "Monofacial with higher GCR may achieve same energy/acre at lower cost",
            "Bifacial rear-side gain decreases as module efficiency improves (less light penetrates to rear)"
        ],
        resolution_strategy="Use bifacial for tracker systems in high-albedo environments (deserts, snow); carefully model GCR tradeoff; consider albedo enhancement (white gravel).",
        controlling_precedent="Utility-scale bifacial adoption >40% (2023), driven by 5-15% energy gain at <5% cost premium; becomes default for new tracker projects."
    ),

    DoctrineBlock(
        topic="Agrivoltaics - Dual Use of Land",
        keywords=["agrivoltaics", "agrophotovoltaics", "dual use", "agriculture", "grazing", "crop yield", "land use efficiency", "solar sharing"],
        conclusion_template=[
            "Agrivoltaics integrates PV arrays with agriculture (crops, grazing), achieving 130-160% land use efficiency versus separate uses.",
            "Crops benefit from partial shade in hot climates (reduced water stress), but yield depends on species selection and row spacing.",
            "Economics challenged by higher array mounting costs (3-4m vs 1m) and agricultural access requirements limiting GCR to 0.2-0.35."
        ],
        reasoning_framework="""
1. Concept: PV arrays elevated 3-5m allow farming equipment underneath, or arrays spaced to create alternating sun/shade zones
2. Land use efficiency: 1 hectare agrivoltaic produces ~70% of standalone solar + 80% of crop yield = 150% land productivity
3. Crop selection: Shade-tolerant crops (lettuce, spinach, kale, berries) thrive under partial shade (40-60% light), sun-loving crops (corn, wheat) suffer
4. Water savings: Shade reduces evapotranspiration 15-30%, critical in arid regions (Arizona, Spain, India)
5. Livestock integration: Sheep grazing under arrays (vegetation management + livestock revenue), common in UK, France
6. Array design: High mounting (3-4m) allows tractor access but costs 30-50% more than ground-mount, GCR 0.25-0.35 vs 0.5 for utility
7. Bifacial synergy: Agrivoltaic arrays often use bifacial to capture reflected light from crops (green albedo ~25%)
8. Regulatory: Some jurisdictions offer agricultural zoning exemptions for agrivoltaics that maintain farming operations
9. Challenges: Hail damage risk to crops, irrigation system compatibility, reduced PV energy due to low GCR
10. Market: <500 MW agrivoltaic globally (2024), mostly pilot projects, largest installations in Japan (FIT incentive), France, Germany
        """,
        key_factors=[
            "Crop type and shade tolerance (berries/lettuce OK, corn/wheat poor)",
            "Water scarcity (shade benefit greater in arid climates)",
            "Land cost (expensive agricultural land may justify dual use)",
            "Farming operation compatibility (row crops need wide spacing, grazing flexible)",
            "Structural cost premium (3-4m mounting vs 1-2m standard)",
            "Revenue split (farmer vs solar operator, typically 50-70% solar, 20-40% ag)"
        ],
        primary_authority=[
            "Fraunhofer ISE 'Agrophotovoltaics' studies (Germany)",
            "NREL 'Agrivoltaics Literature Review'",
            "University of Arizona 'Agrivoltaic Research'",
            "Jack's Solar Garden (Colorado, 1.2 MW agrivoltaic demonstration)",
            "EU Horizon 2020 agrivoltaic projects"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.ADVANCED_PV,
        counter_arguments=[
            "Critics argue 150% land productivity claim ignores crop yield loss from suboptimal light",
            "High structural costs may negate agricultural revenue benefit",
            "Farming operations (spraying, harvesting) may damage PV equipment"
        ],
        resolution_strategy="Agrivoltaics viable for specialty crops (berries, vegetables) in water-scarce, high-land-cost regions; grazing under arrays lower-risk than row crops.",
        controlling_precedent="Agrivoltaics <1% of global PV capacity; niche application requiring site-specific crop/climate/economics alignment; not yet mainstream."
    ),

    DoctrineBlock(
        topic="Floating Solar (Floatovoltaics)",
        keywords=["floating solar", "floatovoltaics", "FPV", "reservoir", "cooling effect", "evaporation reduction", "anchoring", "Ciel & Terre"],
        conclusion_template=[
            "Floating PV on reservoirs/ponds avoids land use, reduces water evaporation 50-70%, and achieves 5-10% higher energy yield from cooling.",
            "Anchoring and mooring systems add $0.05-0.15/W versus ground-mount; wave action and water quality (corrosion) are key design challenges.",
            "Global floating solar capacity ~6 GW (2024), concentrated in Asia (China, Japan, South Korea) with large reservoir potential."
        ],
        reasoning_framework="""
1. Water cooling benefit: Module temperature 5-15°C cooler than ground-mount → 3-8% higher energy yield (temp coefficient -0.35%/°C)
2. Evaporation reduction: Array shades water surface, reduces evaporation 50-70% (valuable in drought-prone regions)
3. Land preservation: Avoids agricultural/forest land conversion, utilizes otherwise unproductive water surface
4. Floatation systems: HDPE pontoons (Ciel & Terre, Ocean Sun) support modules, modular design 10-20 modules per float
5. Anchoring: Piles driven into reservoir bottom, or weighted anchor blocks (non-penetrating), must withstand wind and wave loads
6. Wave design: Reservoirs with <1.5m wave height suitable, ocean installations require specialized designs (rare, experimental)
7. Water quality: Freshwater preferred (lower corrosion), saltwater requires marine-grade materials (aluminum/stainless), higher O&M
8. Environmental: Concern about shading aquatic ecosystem, fish habitats; typically limit coverage to <5-10% of reservoir area
9. Maintenance: Cleaning easier (water access), but access for repairs challenging, no easy walkway between floats
10. Economics: Higher CapEx ($0.05-0.15/W premium) but can be offset by yield gain + land savings + water conservation value
        """,
        key_factors=[
            "Reservoir wave/wind conditions (calm lakes ideal, high-wind reservoirs challenging)",
            "Water quality (freshwater vs saltwater corrosion)",
            "Land availability (land-scarce regions favor floating)",
            "Water rights (drinking water reservoirs may prohibit FPV)",
            "Environmental impact (shading limits, aquatic habitat)",
            "Grid connection proximity (transmission distance)"
        ],
        primary_authority=[
            "Ciel & Terre, Ocean Sun floating PV system datasheets",
            "World Bank 'Where Sun Meets Water: Floating Solar Handbook'",
            "NREL 'Floating Solar Market Report'",
            "IEC TS 63281 (floating PV design standard, draft)",
            "Largest installations: Huainan (China, 150 MW), Yamakura (Japan, 13.7 MW)"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.ADVANCED_PV,
        counter_arguments=[
            "Some argue cooling benefit overstated, real-world yield gain <5%",
            "Anchoring failures in severe storms have damaged installations (typhoons in Japan)",
            "Environmental groups oppose large-scale reservoir coverage (aquatic habitat)"
        ],
        resolution_strategy="Floating PV viable for calm reservoirs in land-scarce, water-scarce regions (Asia, Middle East); limit coverage <10% reservoir area for environmental acceptance.",
        controlling_precedent="6+ GW floating solar deployed globally, 70% in China; technology proven for reservoirs, experimental for ocean; cost premium justifiable in high-land-cost regions."
    ),

    DoctrineBlock(
        topic="Solar + Storage Economics - ITC and PTC",
        keywords=["ITC", "investment tax credit", "PTC", "production tax credit", "IRA", "tax equity", "depreciation", "MACRS"],
        conclusion_template=[
            "US Inflation Reduction Act (IRA 2022) provides 30% ITC for solar+storage through 2032, declining to 26% (2033), 22% (2034), then 10% permanent.",
            "Standalone storage now eligible for ITC if charged >75% from co-located renewables; previously required solar+storage integration.",
            "Tax equity structures (partnership flip, sale-leaseback) monetize credits for non-taxpaying entities, adding 5-10% transaction costs."
        ],
        reasoning_framework="""
1. ITC basis: 30% of project CapEx (modules, inverters, racking, installation labor, interconnection), claimed in tax year of commercial operation
2. ITC + depreciation: MACRS (Modified Accelerated Cost Recovery System) allows 5-year depreciation, further reducing tax liability ~15-20% NPV
3. PTC alternative: $27.50/MWh production credit for 10 years (2024 value, inflation-adjusted), better for high-capacity-factor projects (>30%)
4. ITC vs PTC choice: ITC favored if CapEx high/CF low (solar), PTC if CapEx low/CF high (onshore wind ~40% CF)
5. Storage ITC: Standalone storage eligible for 30% ITC if ≥5 kWh capacity and meets charging requirement (≥75% from renewables in first 3 years)
6. Domestic content bonus: +10% ITC if steel/iron US-made and >40% module/component cost US-manufactured (2024 threshold, increases to 55% by 2027)
7. Energy community bonus: +10% ITC if project in former coal community, brownfield, or high-unemployment area
8. Tax equity: Developers without tax appetite sell portion of project to tax equity investor (bank, insurance company) who monetizes credits
9. Partnership flip: Tax equity gets 99% of credits/depreciation in years 1-6, then flips to 5% after recoupment, developer keeps cash flow
10. Sale-leaseback: Developer sells project to tax equity, leases back, simpler than flip but less efficient (lower NPV)
        """,
        key_factors=[
            "Tax appetite (corporations with >$50M tax liability can absorb credits, small developers need tax equity)",
            "Domestic content feasibility (US module/steel supply chain still developing)",
            "Energy community qualification (coal regions, brownfields)",
            "Storage charging strategy (must maintain ≥75% renewable charging for ITC retention)",
            "Financing structure (tax equity adds complexity, 6-12 month lead time)",
            "Recapture risk (if project fails within 5 years, ITC must be repaid pro-rata)"
        ],
        primary_authority=[
            "IRS Notice 2023-17 (standalone storage ITC guidance)",
            "26 USC §48 (Energy Investment Tax Credit)",
            "US Treasury 'Inflation Reduction Act Tax Credits'",
            "NREL 'Solar Tax Credit Analysis'",
            "Norton Rose Fulbright 'Tax Equity Structures' (legal analysis)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ECONOMICS,
        counter_arguments=[
            "Some argue ITC will expire or be reduced by future Congress (political risk)",
            "Tax equity market concentration (few players) limits competition, depresses developer returns",
            "Domestic content bonus unrealistic given limited US manufacturing (FirstSolar only major US module maker)"
        ],
        resolution_strategy="Maximize ITC with domestic content/energy community bonuses where feasible; structure tax equity early in development; consider PTC for high-CF hybrid projects.",
        controlling_precedent="ITC extended to 2034 with IRA, storage ITC game-changer; 80%+ of US utility solar uses tax equity financing; ITC sunset risk remains long-term."
    ),

    DoctrineBlock(
        topic="Solar Thermal Systems - Flat Plate vs Evacuated Tube",
        keywords=["solar thermal", "solar water heating", "flat plate collector", "evacuated tube", "glycol", "thermosiphon", "SWH"],
        conclusion_template=[
            "Solar thermal for water heating achieves 60-80% efficiency (vs 20% for PV) but limited to low-temperature applications (<100°C).",
            "Flat plate collectors cost-effective in warm climates; evacuated tubes perform better in cold/cloudy climates but cost 2-3× more.",
            "Market shrinking due to PV+heat pump competing technology; PV generates electricity that runs heat pump with COP 3-4, matching thermal efficiency."
        ],
        reasoning_framework="""
1. Flat plate: Insulated box with black absorber plate, copper tubes carry heat transfer fluid (water or glycol), glass cover reduces convection loss
2. Evacuated tube: Glass vacuum tubes eliminate convection loss, selective coating on absorber maximizes solar absorption, minimizes IR emission
3. Efficiency: Flat plate 50-70% (drops in cold weather), evacuated tube 60-80% (maintains efficiency in cold due to vacuum insulation)
4. Stagnation temp: Flat plate ~150°C, evacuated tube >200°C (can damage glycol, requires overheat protection)
5. Freeze protection: Glycol antifreeze in closed-loop systems (cold climates), drainback systems (warmer climates, simpler)
6. Applications: Domestic hot water (DHW), pool heating, space heating, industrial process heat (<100°C)
7. Payback: 5-10 years in sunny climates with high nat gas prices, >15 years in cloudy/cheap-gas regions
8. Reliability: 20-25 year lifespan, but pumps/controllers fail after 10-15 years, glycol degrades (needs replacement every 5-10 years)
9. PV+heat pump alternative: PV generates electricity → heat pump with COP 3.5 → equivalent thermal efficiency ~70% (20% PV × 3.5 COP)
10. Market decline: US solar thermal shipments down 70% since 2008, China still dominant market (50% of global capacity)
        """,
        key_factors=[
            "Climate (evacuated tube better in cold/cloudy, flat plate sufficient in warm/sunny)",
            "Application temperature (DHW 50-60°C OK for both, space heating 70-80°C favors evacuated)",
            "Electricity vs gas pricing (high elec/low gas favors thermal, low elec/high gas favors PV+heat pump)",
            "Roof space (thermal uses less space than equivalent PV+heat pump for same thermal output)",
            "Installation complexity (thermal requires plumbing integration, PV simpler electrical)",
            "Incentives (some regions still offer solar thermal rebates, others eliminated)"
        ],
        primary_authority=[
            "SRCC (Solar Rating & Certification Corporation) OG-100 collector ratings",
            "ASHRAE 93 (solar collector testing standard)",
            "Viessmann, Rheem, Apricus solar thermal datasheets",
            "IEA Solar Heating & Cooling Programme",
            "NREL 'Solar Water Heating Market Analysis'"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.THERMAL_SYSTEMS,
        counter_arguments=[
            "Solar thermal advocates argue direct conversion to heat more efficient than PV→electric→heat",
            "Some climates (Mediterranean, Middle East) have strong solar thermal tradition and infrastructure",
            "Industrial process heat at 80-100°C still viable niche for solar thermal"
        ],
        resolution_strategy="Solar thermal viable for high-temperature DHW/industrial process heat in sunny climates; otherwise PV+heat pump increasingly cost-competitive and simpler.",
        controlling_precedent="Global solar thermal market shrinking except China; US residential solar thermal <100 MW/year vs >20 GW PV/year; PV+heat pump displacing thermal."
    )
]


# ============================================================================
# CORE ENGINE COMPONENTS
# ============================================================================

class SolarEnergyEngine:
    """Main TIE-20 architecture engine for solar energy systems."""

    def __init__(self):
        self.doctrine_cache = {d.topic: d for d in DOCTRINE_CACHE}
        self.telemetry = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.coverage_map = CoverageMap()

    async def query(
        self,
        question: str,
        mode: ResponseMode,
        context: Optional[Dict[str, Any]] = None
    ) -> QueryResponse:
        """Main query endpoint - TIE three-layer response."""
        start_time = time.time()

        # Layer 1: Doctrine cache (fast path)
        triggered = self._match_doctrines(question)

        if triggered and mode == ResponseMode.FAST:
            response = self._fast_response(question, triggered)
        elif mode == ResponseMode.DEFENSE:
            response = self._defense_response(question, triggered, context)
        else:  # MEMO
            response = self._memo_response(question, triggered, context)

        # Update coverage and drift tracking
        categories = self._extract_categories(triggered)
        self.coverage_map.record_trigger(triggered)

        latency = (time.time() - start_time) * 1000
        self.telemetry.record_query(latency, mode, categories)

        # Generate deterministic hash
        hash_input = f"{question}:{response}:{mode.value}"
        response_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        return QueryResponse(
            answer=response,
            confidence=self._assess_confidence(triggered),
            mode=mode,
            categories=categories,
            triggered_doctrines=[d.topic for d in triggered],
            latency_ms=round(latency, 2),
            hash=response_hash,
            timestamp=datetime.utcnow().isoformat()
        )

    def _match_doctrines(self, question: str) -> List[DoctrineBlock]:
        """Match question to doctrine blocks via keyword overlap."""
        q_lower = question.lower()
        matches = []

        for doctrine in DOCTRINE_CACHE:
            keyword_hits = sum(1 for kw in doctrine.keywords if kw.lower() in q_lower)
            if keyword_hits >= 2:  # Require at least 2 keyword matches
                matches.append((keyword_hits, doctrine))

        # Sort by keyword match count, return top doctrines
        matches.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in matches[:5]]

    def _fast_response(self, question: str, doctrines: List[DoctrineBlock]) -> str:
        """FAST mode: Concise answer from doctrine conclusions."""
        if not doctrines:
            return "Insufficient doctrine coverage for this solar energy query. Recommend consultation with solar engineering specialist."

        primary = doctrines[0]
        conclusion = " ".join(primary.conclusion_template)

        key_factors = "; ".join(primary.key_factors[:3])

        return f"{conclusion}\n\nKey factors: {key_factors}"

    def _defense_response(self, question: str, doctrines: List[DoctrineBlock], context: Optional[Dict]) -> str:
        """DEFENSE mode: Audit-ready response with citations."""
        if not doctrines:
            return "No applicable solar energy doctrine found. This question requires specialized technical analysis beyond standard engineering practice."

        primary = doctrines[0]

        response_parts = [
            "SOLAR ENERGY TECHNICAL ANALYSIS",
            "",
            "Issue Classification:",
            f"  Category: {primary.category.value}",
            f"  Confidence: {primary.confidence.value}",
            "",
            "Analysis:",
            primary.reasoning_framework,
            "",
            "Conclusion:",
            " ".join(primary.conclusion_template),
            "",
            "Supporting Authority:",
        ]

        for i, auth in enumerate(primary.primary_authority, 1):
            response_parts.append(f"  {i}. {auth}")

        if primary.counter_arguments:
            response_parts.extend([
                "",
                "Counter-Arguments Considered:",
            ])
            for arg in primary.counter_arguments:
                response_parts.append(f"  • {arg}")

        response_parts.extend([
            "",
            "Resolution Strategy:",
            primary.resolution_strategy,
            "",
            f"Controlling Precedent: {primary.controlling_precedent}"
        ])

        return "\n".join(response_parts)

    def _memo_response(self, question: str, doctrines: List[DoctrineBlock], context: Optional[Dict]) -> str:
        """MEMO mode: Comprehensive technical memorandum."""
        if not doctrines:
            return self._fallback_memo(question)

        primary = doctrines[0]

        memo_parts = [
            "TECHNICAL MEMORANDUM",
            "SOLAR ENERGY SYSTEMS ENGINEERING ANALYSIS",
            "=" * 60,
            "",
            f"Subject: {primary.topic}",
            f"Classification: {primary.category.value}",
            f"Confidence Level: {primary.confidence.value}",
            f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}",
            "",
            "EXECUTIVE SUMMARY",
            "-" * 60,
            " ".join(primary.conclusion_template),
            "",
            "TECHNICAL ANALYSIS",
            "-" * 60,
            primary.reasoning_framework,
            "",
            "KEY TECHNICAL FACTORS",
            "-" * 60,
        ]

        for i, factor in enumerate(primary.key_factors, 1):
            memo_parts.append(f"{i}. {factor}")

        memo_parts.extend([
            "",
            "AUTHORITATIVE REFERENCES",
            "-" * 60,
        ])

        for i, auth in enumerate(primary.primary_authority, 1):
            memo_parts.append(f"[{i}] {auth}")

        if primary.counter_arguments:
            memo_parts.extend([
                "",
                "ALTERNATIVE POSITIONS & REBUTTALS",
                "-" * 60,
            ])
            for i, arg in enumerate(primary.counter_arguments, 1):
                memo_parts.append(f"{i}. {arg}")

        memo_parts.extend([
            "",
            "RECOMMENDED RESOLUTION STRATEGY",
            "-" * 60,
            primary.resolution_strategy,
            "",
            "CONTROLLING PRECEDENT",
            "-" * 60,
            primary.controlling_precedent,
            "",
        ])

        # Add related doctrines if any
        if len(doctrines) > 1:
            memo_parts.extend([
                "RELATED TECHNICAL CONSIDERATIONS",
                "-" * 60,
            ])
            for doctrine in doctrines[1:]:
                memo_parts.append(f"• {doctrine.topic}: {doctrine.conclusion_template[0]}")

        memo_parts.extend([
            "",
            "=" * 60,
            "END OF MEMORANDUM"
        ])

        return "\n".join(memo_parts)

    def _fallback_memo(self, question: str) -> str:
        """Fallback memo when no doctrines match."""
        return f"""TECHNICAL MEMORANDUM
SOLAR ENERGY SYSTEMS ENGINEERING ANALYSIS
============================================================

Subject: {question[:100]}
Classification: INSUFFICIENT_DOCTRINE_COVERAGE
Date: {datetime.utcnow().strftime('%Y-%m-%d')}

ANALYSIS
------------------------------------------------------------
This query addresses solar energy systems topics not covered by the
current doctrine cache. Recommended approach:

1. Consult specialized solar engineering references (NREL, IEEE, IEA)
2. Engage licensed Professional Engineer (PE) for site-specific analysis
3. Review applicable standards (IEC 61215, NEC Article 690, IEEE 1547)
4. Consider engaging equipment manufacturers for technical guidance

RECOMMENDATIONS
------------------------------------------------------------
• Expand doctrine coverage for this topic area
• Conduct detailed technical review with subject matter experts
• Document findings for future reference

============================================================
END OF MEMORANDUM
"""

    def _extract_categories(self, doctrines: List[DoctrineBlock]) -> List[IssueCategory]:
        """Extract unique categories from triggered doctrines."""
        return list(set(d.category for d in doctrines))

    def _assess_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Assess overall confidence based on doctrine matches."""
        if not doctrines:
            return ConfidenceLevel.HIGH_RISK

        # Use primary doctrine's confidence
        return doctrines[0].confidence


class TelemetryCollector:
    """Track query metrics and performance."""

    def __init__(self):
        self.queries: List[Dict[str, Any]] = []
        self.category_counts: Dict[IssueCategory, int] = defaultdict(int)
        self.mode_latencies: Dict[ResponseMode, List[float]] = defaultdict(list)

    def record_query(self, latency_ms: float, mode: ResponseMode, categories: List[IssueCategory]):
        """Record query telemetry."""
        self.queries.append({
            "timestamp": datetime.utcnow().isoformat(),
            "latency_ms": latency_ms,
            "mode": mode.value,
            "categories": [c.value for c in categories]
        })

        self.mode_latencies[mode].append(latency_ms)

        for cat in categories:
            self.category_counts[cat] += 1

    def get_stats(self) -> Dict[str, Any]:
        """Return telemetry statistics."""
        return {
            "total_queries": len(self.queries),
            "avg_latency_ms": sum(q["latency_ms"] for q in self.queries) / max(len(self.queries), 1),
            "category_distribution": dict(self.category_counts),
            "mode_latencies": {
                mode.value: {
                    "count": len(latencies),
                    "avg_ms": sum(latencies) / max(len(latencies), 1),
                    "max_ms": max(latencies) if latencies else 0
                }
                for mode, latencies in self.mode_latencies.items()
            }
        }


class DriftWatcher:
    """Detect doctrine drift over time."""

    def __init__(self):
        self.doctrine_versions: Dict[str, List[str]] = defaultdict(list)

    def record_version(self, topic: str, version_hash: str):
        """Record doctrine version for drift detection."""
        self.doctrine_versions[topic].append(version_hash)

    def detect_drift(self) -> List[str]:
        """Identify doctrines with multiple versions (potential drift)."""
        drifted = []
        for topic, versions in self.doctrine_versions.items():
            if len(set(versions)) > 1:
                drifted.append(topic)
        return drifted


class CoverageMap:
    """Track which doctrines are triggered vs untriggered."""

    def __init__(self):
        self.triggered: Set[str] = set()
        self.trigger_counts: Dict[str, int] = defaultdict(int)

    def record_trigger(self, doctrines: List[DoctrineBlock]):
        """Record doctrine triggers."""
        for d in doctrines:
            self.triggered.add(d.topic)
            self.trigger_counts[d.topic] += 1

    def get_coverage_stats(self) -> Dict[str, Any]:
        """Return coverage statistics."""
        total_doctrines = len(DOCTRINE_CACHE)
        triggered_count = len(self.triggered)

        return {
            "total_doctrines": total_doctrines,
            "triggered_count": triggered_count,
            "coverage_pct": round(100 * triggered_count / total_doctrines, 1),
            "untriggered": [d.topic for d in DOCTRINE_CACHE if d.topic not in self.triggered],
            "top_triggered": sorted(self.trigger_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        }


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(title=ENGINE_NAME, version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
engine = SolarEnergyEngine()


@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint."""
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": VERSION,
        "port": PORT,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "categories": [cat.value for cat in IssueCategory],
        "telemetry": engine.telemetry.get_stats(),
        "coverage": engine.coverage_map.get_coverage_stats(),
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint."""
    try:
        response = await engine.query(request.question, request.mode, request.context)
        return response
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics."""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "confidence": d.confidence.value,
                "keywords": d.keywords[:5]
            }
            for d in DOCTRINE_CACHE
        ]
    }


@app.get("/categories")
async def list_categories():
    """List all issue categories."""
    return {
        "categories": [
            {
                "name": cat.value,
                "description": cat.name.replace("_", " ").title()
            }
            for cat in IssueCategory
        ]
    }


if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    logger.info(f"Categories: {[cat.value for cat in IssueCategory]}")

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
