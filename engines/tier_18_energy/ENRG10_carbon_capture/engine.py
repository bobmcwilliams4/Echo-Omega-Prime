"""
ENRG10 Carbon Capture and Storage Intelligence Engine
Port: 9245 | TIE-Grade CCUS Analysis Engine
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

# Configure logger
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "logs" / "enrg10_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
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

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

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
    controlling_precedent: Optional[str] = None

@dataclass
class TelemetryEntry:
    query_id: str
    timestamp: datetime
    query_text: str
    mode: ResponseMode
    latency_ms: float
    cache_hit: bool
    doctrines_triggered: List[str]
    confidence: ConfidenceLevel
    error_domain: Optional[str] = None

@dataclass
class CoverageMetrics:
    total_doctrines: int
    triggered_count: int
    missed_doctrines: List[str]
    epistemic_gaps: List[str]

class QueryRequest(BaseModel):
    query: str = Field(..., description="CCUS analysis query")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(AnalysisZone.PLANNING, description="Analysis context zone")
    include_citations: bool = Field(True, description="Include authority references")

class QueryResponse(BaseModel):
    answer: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    doctrines_applied: List[str]
    citations: Optional[List[str]] = None
    latency_ms: float
    determinism_hash: str
    epistemic_caveats: Optional[List[str]] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrine_count: int
    cache_size: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float
    cache_hit_rate: float

class ENRG10Engine:
    def __init__(self):
        self.version = "1.0.0"
        self.port = 9245
        self.start_time = datetime.now()
        self.query_count = 0
        self.total_latency_ms = 0.0
        self.cache_hits = 0
        self.telemetry_log: List[TelemetryEntry] = []
        self.doctrine_triggers: Dict[str, int] = {}
        self.doctrine_cache = self._build_doctrine_cache()
        logger.info(f"ENRG10 Carbon Capture Engine v{self.version} initialized with {len(self.doctrine_cache)} doctrines")

    def _build_doctrine_cache(self) -> Dict[str, DoctrineBlock]:
        """Build comprehensive CCUS doctrine knowledge base"""
        doctrines = {}

        # POST-COMBUSTION CAPTURE
        doctrines["post_combustion_amine"] = DoctrineBlock(
            topic="Post-Combustion CO2 Capture with Amine Scrubbing",
            keywords=["post-combustion", "amine", "MEA", "absorber", "stripper", "flue gas"],
            conclusion_template="Post-combustion capture using monoethanolamine (MEA) achieves 85-95% CO2 removal from flue gas with energy penalty of 25-35% plant output. Optimal MEA concentration is 30wt% to balance absorption rate and corrosion.",
            reasoning_framework="""
Post-combustion amine scrubbing fundamental analysis:
1. ABSORPTION PROCESS - Flue gas contacts 30wt% MEA solution in packed absorber column at 40-60C
   - CO2 + 2RNH2 ⇌ RNHCOO- + RNH3+ (carbamate formation)
   - Driving force: partial pressure gradient between gas and liquid
   - Mass transfer enhanced by packing (structured or random)
   - Typical gas velocity: 2-3 m/s to avoid flooding
2. RICH SOLVENT PUMPING - CO2-laden amine pumped to stripper at elevated pressure
   - Heat exchanger preheats rich solvent using lean solvent (reduces reboiler duty)
   - Temperature approach: 5-10C for economic optimization
3. STRIPPING REGENERATION - Heat reverses reaction at 100-120C, releases pure CO2
   - Reboiler duty: 3.5-4.5 GJ/tonne CO2 (major energy consumer)
   - Steam source: low-pressure extraction from turbine (reduces power output)
   - Overhead condenser recovers water, produces 99.5%+ CO2 stream
4. LEAN SOLVENT RECYCLE - Regenerated amine cooled and returned to absorber
   - Makeup MEA added to compensate for degradation losses (1.5-2 kg/tonne CO2)
   - Thermal degradation products: heat stable salts (HSS) require reclaimer
5. ENERGY PENALTY QUANTIFICATION - Total parasitic load 25-35% of plant output
   - Reboiler heat: 20-25% output (equivalent thermal)
   - Auxiliary power (pumps, fans, compressor): 5-10% electric output
   - Net plant efficiency drops from ~38% to 25-28% (coal SCPC)
6. OPTIMIZATION STRATEGIES - Advanced solvents (KS-1, KS-2) reduce penalty to 20-25%
   - Piperazine (PZ) promoter increases absorption rate 3-5x
   - Split-flow configurations reduce reboiler duty 10-15%
7. CORROSION MANAGEMENT - CO2-loaded amine is corrosive to carbon steel above 50C
   - Use 304/316 SS in hot sections or corrosion inhibitors
   - Oxygen intrusion accelerates degradation - maintain <50 ppm O2
8. ENVIRONMENTAL CONTROLS - Amine emissions to atmosphere cause haze, odor
   - Water wash section removes entrained amine (<1 ppm in clean gas)
   - Degradation products may include nitrosamines (carcinogenic) - requires analysis
""",
            key_factors=[
                "MEA concentration 30wt% balances kinetics and corrosion",
                "Reboiler duty 3.5-4.5 GJ/tonne CO2 dominates energy penalty",
                "90% CO2 capture typical for coal plants, 85% for NGCC",
                "Steam extraction reduces power output 20-25%",
                "Absorber packing selection critical for mass transfer efficiency",
                "Heat exchanger approach temperature affects economics",
                "Degradation products require reclaimer and environmental monitoring"
            ],
            primary_authority=[
                "DOE/NETL CO2 Capture Technology Program reports",
                "IEAGHG Technical Review 2013-TR6 (Amine Scrubbing)",
                "Abu-Zahra et al., 'CO2 capture from power plants: Economic comparison', Int J Greenhouse Gas Control 2007"
            ],
            burden_holder="Project developer to demonstrate energy penalty <30% to be competitive",
            adversary_position="Critics argue energy penalty makes CCS uneconomic vs. renewables",
            counter_arguments=[
                "Advanced solvents (KS-1, PZ-promoted) reduce penalty to 20-25%",
                "Waste heat integration in industrial settings lowers net penalty",
                "45Q tax credit ($85/ton) improves economics substantially",
                "CCS enables dispatchable low-carbon power (vs. intermittent renewables)",
                "Retrofit potential for existing coal fleet extends asset life"
            ],
            resolution_strategy="Quantify site-specific energy penalty with detailed process model, compare LCOE with and without CCS including 45Q value",
            entity_scope="Power plants >500 MW, refineries, cement, steel",
            confidence=ConfidenceLevel.DEFENSIBLE
        )

        doctrines["pre_combustion_igcc"] = DoctrineBlock(
            topic="Pre-Combustion Capture in IGCC with Shift Reactor",
            keywords=["pre-combustion", "IGCC", "gasification", "shift reactor", "Selexol", "syngas"],
            conclusion_template="Pre-combustion capture in IGCC achieves >90% CO2 removal with lower energy penalty (15-20%) than post-combustion. Water-gas shift converts CO to CO2, physical solvent (Selexol) captures CO2 at high partial pressure.",
            reasoning_framework="""
Pre-combustion IGCC capture pathway analysis:
1. GASIFICATION STAGE - Coal/petcoke converted to syngas (CO + H2) at 1200-1500C, 30-70 bar
   - Oxygen-blown gasification produces concentrated CO2 (no nitrogen dilution)
   - Raw syngas: 60% CO, 30% H2, 5% CO2, 5% other (H2S, COS)
   - Entrained flow gasifiers (GE, Shell) most common for power applications
2. SYNGAS COOLING AND SCRUBBING - Quench or radiant cooler drops temperature to 200-250C
   - Water scrubber removes particulates, chlorides
   - COS hydrolysis reactor: COS + H2O → H2S + CO2 (prevents downstream catalyst poisoning)
3. WATER-GAS SHIFT REACTION - Catalytic conversion of CO to CO2 and H2
   - CO + H2O ⇌ CO2 + H2  (ΔH = -41 kJ/mol, exothermic)
   - Two-stage shift: HTS (350-450C, Fe-Cr catalyst) + LTS (200-250C, Cu-Zn catalyst)
   - Equilibrium drives >95% CO conversion, producing CO2-rich stream (40% CO2)
4. ACID GAS REMOVAL - Physical solvent (Selexol, Rectisol) absorbs CO2 and H2S
   - Selexol: dimethyl ethers of polyethylene glycol, operates at 20-40C, 30+ bar
   - High CO2 partial pressure (8-12 bar) enhances absorption (Henry's Law)
   - Two-stage flash regeneration releases CO2 at near-atmospheric pressure
   - H2S removed separately (sent to Claus sulfur recovery)
5. HYDROGEN COMBUSTION - Clean H2 burned in gas turbine (modified combustor for H2)
   - High flame temperature requires diluent (N2 or steam) or lean-premix combustion
   - NOx control critical (H2 combustion produces more NOx than natural gas)
6. ENERGY PENALTY QUANTIFICATION - 15-20% net output reduction vs. IGCC without capture
   - Air separation unit (ASU): ~10% plant output
   - CO2 compression (110 bar): ~5% output
   - Shift reactor heat integration offsets some penalty
7. CO2 STREAM PURITY - >95% CO2, <50 ppm H2S (meets pipeline specs)
   - Trace contaminants: H2, CO, Ar (from ASU), N2
   - Further purification rarely needed unless high-purity CO2 sale (food grade)
8. ECONOMIC CONSIDERATIONS - IGCC capital cost 20-30% higher than PC
   - CCS-ready IGCC has lower incremental capture cost than PC retrofit
   - Syngas platform enables polygeneration (power + chemicals)
""",
            key_factors=[
                "Water-gas shift produces high CO2 partial pressure (8-12 bar) enabling efficient capture",
                "Physical solvents (Selexol) regenerate with pressure swing (no thermal penalty)",
                "Energy penalty 15-20% lower than post-combustion amine",
                "IGCC base cost premium 20-30% vs. pulverized coal",
                "H2 combustion requires gas turbine modifications",
                "Polygeneration potential improves economics",
                "ASU oxygen demand increases with capture (more shift steam)"
            ],
            primary_authority=[
                "DOE/NETL Cost and Performance Baseline for Fossil Energy Plants Vol 1 (2019)",
                "IEAGHG Report 2010/04 - IGCC with CCS",
                "Kunze & Spliethoff, 'Assessment of oxy-fuel, pre- and post-combustion-based CCS', Energy Procedia 2011"
            ],
            burden_holder="Developer to justify IGCC capital premium with long-term fuel flexibility and lower CCS cost",
            adversary_position="IGCC complexity and higher CAPEX make it uncompetitive vs. NGCC+CCS",
            counter_arguments=[
                "Fuel flexibility (coal, petcoke, biomass, waste) hedges against gas price volatility",
                "Lower CCS incremental cost than PC retrofit",
                "Polygeneration optionality (chemicals, H2, power) improves IRR",
                "Mercury removal inherent (no separate ACI system needed)",
                "Lower CCS energy penalty extends plant lifetime economics"
            ],
            resolution_strategy="Compare levelized cost (LCOE) of IGCC+CCS vs. NGCC+CCS and PC+CCS over 30-year lifetime with fuel price scenarios",
            entity_scope="Coal/petcoke power plants >400 MW, refineries with existing gasifiers",
            confidence=ConfidenceLevel.DEFENSIBLE
        )

        doctrines["direct_air_capture_solid"] = DoctrineBlock(
            topic="Direct Air Capture with Solid Sorbent Technology",
            keywords=["DAC", "direct air capture", "solid sorbent", "Climeworks", "temperature swing", "ambient air"],
            conclusion_template="Solid sorbent DAC (e.g., Climeworks) achieves CO2 capture from ambient air (415 ppm) using amine-functionalized filters with temperature-swing regeneration. Energy requirement 1.5-2.5 GJ/tonne CO2 thermal + 0.4-0.8 MWh/tonne electric.",
            reasoning_framework="""
Solid sorbent direct air capture technology analysis:
1. ADSORPTION STAGE - Ambient air drawn through amine-functionalized filters
   - Supported amine sorbent on porous substrate (cellulose, silica)
   - Capture kinetics limited by low CO2 partial pressure (0.04 kPa vs. 12+ kPa in flue gas)
   - Air contactor design: counter-flow packed bed, residence time 2-5 seconds
   - Large air volumes required: ~2000 m3 air / kg CO2 captured
2. TEMPERATURE-SWING REGENERATION - Heating sorbent to 80-120C releases CO2
   - Low-grade heat source ideal: waste heat, solar thermal, geothermal
   - Vacuum assistance lowers regeneration temperature, reduces thermal input
   - Desorption produces pure CO2 stream (>95%) suitable for storage or utilization
3. ENERGY CONSUMPTION BREAKDOWN - Total: 1.5-2.5 GJ/tonne thermal + 0.4-0.8 MWh electric
   - Thermal: sorbent heating, desorption enthalpy
   - Electric: air fans/blowers (dominant), vacuum pumps, CO2 compression
   - Fan power scales with air flow rate and pressure drop across filter bed
4. SORBENT DURABILITY - Amine degradation from O2, NOx, SOx in ambient air
   - Cycle life: 1000-5000 cycles before replacement (vs. 100,000+ target)
   - Cost of sorbent replacement: $50-100/tonne CO2 if <3000 cycles
   - Oxidative degradation mitigated with sterically hindered amines
5. MODULAR SCALABILITY - Climeworks units: 50-100 tonne CO2/year per module
   - Linear scaling: 100 modules = 5000-10000 tonne/year plant
   - Distributed deployment near CO2 utilization or storage sites
   - Smaller footprint than liquid solvent DAC (no large contactors)
6. COST STRUCTURE - Current: $400-800/tonne CO2, target: $100-200/tonne
   - CAPEX: $3000-5000/tonne annual capacity (equipment, installation)
   - OPEX: energy (50-60%), sorbent replacement (20-30%), O&M (10-20%)
   - Learning curve: 15-25% cost reduction per doubling of capacity
7. HEAT SOURCE INTEGRATION - Low-temperature heat (<120C) widely available
   - Waste heat from power plants, data centers, industrial processes
   - Solar thermal collectors, geothermal brine heat exchangers
   - Heat pump integration (COP 3-4) if electric power is cheap/renewable
8. LIFECYCLE CARBON ACCOUNTING - Net negativity requires low-carbon energy
   - If powered by coal electricity + natural gas heat: net positive emissions
   - Renewable electricity + waste heat: 90-95% net negative (accounting for construction)
   - Geological storage permanence: 99%+ over 1000 years (IPCC AR6)
""",
            key_factors=[
                "Low CO2 concentration in air (415 ppm) requires large air volumes",
                "Energy requirement 6-10x higher than point-source capture per tonne CO2",
                "Sorbent cycle life <5000 currently, need 10x improvement for cost target",
                "Modular design enables distributed deployment",
                "Economic viability depends on low-cost low-carbon energy access",
                "Current cost $400-800/tonne, need <$200/tonne for broad deployment",
                "45Q tax credit $180/tonne (if stored) covers most current cost"
            ],
            primary_authority=[
                "National Academies Report: Negative Emissions Technologies and Reliable Sequestration (2019)",
                "Climeworks technical documentation and pilot plant data (Hinwil, Orca)",
                "McQueen et al., 'Cost Analysis of Direct Air Capture', Joule 2020"
            ],
            burden_holder="DAC developer to prove energy source is low-carbon to claim net negativity",
            adversary_position="DAC is too energy-intensive and expensive vs. afforestation or point-source capture",
            counter_arguments=[
                "DAC is location-flexible (no need for flue gas source)",
                "Enables carbon removal from distributed sources (transport, agriculture)",
                "Necessary to achieve net-zero by 2050 (IPCC 1.5C pathways require 5-10 Gt/yr DAC by 2100)",
                "Cost declining rapidly with scale (learning rate 15-25%)",
                "Can operate 24/7 with low-cost off-peak renewable power",
                "Permanent geological storage provides durable carbon removal"
            ],
            resolution_strategy="Calculate lifecycle carbon intensity including energy source, compare cost/tonne CO2 removed vs. alternative CDR methods (afforestation, BECCS, mineralization)",
            entity_scope="Commercial DAC plants, corporate carbon removal purchases, CDR market",
            confidence=ConfidenceLevel.AGGRESSIVE
        )

        doctrines["direct_air_capture_liquid"] = DoctrineBlock(
            topic="Direct Air Capture with Liquid Solvent (Alkaline Solution)",
            keywords=["DAC", "liquid solvent", "potassium hydroxide", "KOH", "Carbon Engineering", "calcination"],
            conclusion_template="Liquid solvent DAC (Carbon Engineering design) uses potassium hydroxide solution to capture CO2 from air, forming potassium carbonate. Calcination regenerates KOH and releases pure CO2, requiring 5-8 GJ/tonne CO2 thermal energy.",
            reasoning_framework="""
Alkaline liquid solvent DAC process analysis:
1. AIR CONTACTING - Ambient air flows through KOH spray towers (counter-flow)
   - Reaction: CO2 + 2KOH → K2CO3 + H2O
   - Large contactors required (10-20 m tall, 5-10 m diameter) for low CO2 concentration
   - Liquid-to-gas ratio: 5-10 L/m3 air
   - CO2 capture efficiency per pass: 50-70% (multiple passes or large towers)
2. PELLET REACTOR - K2CO3 solution reacted with Ca(OH)2 to form CaCO3 pellets
   - K2CO3 + Ca(OH)2 → CaCO3↓ + 2KOH (regenerates caustic)
   - Fluidized bed or slurry reactor, pellets grow to 1-3 mm
   - KOH recycled to air contactor (closed loop)
3. CALCINATION - CaCO3 pellets heated to 900C to decompose and release CO2
   - CaCO3 → CaO + CO2  (ΔH = +178 kJ/mol, highly endothermic)
   - Oxy-fired calciner (uses pure O2 to avoid N2 dilution, produces 95%+ CO2 stream)
   - Requires air separation unit (ASU) for oxygen supply
4. HYDRATION - CaO (lime) reacted with water to regenerate Ca(OH)2
   - CaO + H2O → Ca(OH)2  (ΔH = -65 kJ/mol, exothermic, partial heat recovery)
   - Slaker produces Ca(OH)2 slurry for pellet reactor
5. ENERGY CONSUMPTION - Total: 5.5-8.5 GJ/tonne CO2 thermal + 1.5-2.5 MWh electric
   - Thermal: calcination (dominant ~80%), air heating, steam
   - Electric: air fans, ASU, pumps, conveyors, CO2 compression
   - Natural gas-fired calciner most common (but undermines carbon removal claim)
6. SCALE ADVANTAGES - Carbon Engineering design targets 1 Mt CO2/year plants
   - Large contactors enable economies of scale in fabrication
   - Continuous solid handling (pellets) more mature than sorbent filter systems
   - Higher throughput per unit volume than solid sorbent systems
7. HEAT SOURCE CHALLENGE - 900C calcination requires high-quality heat
   - Natural gas combustion standard, but creates ~0.3 tonne CO2 per tonne captured (lifecycle)
   - Electric calciner with renewable power: technically feasible but high CAPEX
   - Oxy-fuel eliminates external CO2 but requires ASU (energy penalty)
8. COST PROJECTIONS - Carbon Engineering: $94-232/tonne CO2 at scale (1 Mt/yr, natural gas heat)
   - CAPEX: $1000-1500/tonne annual capacity
   - OPEX: natural gas (40-50%), electricity (20-30%), maintenance (20-30%)
   - Cost sensitive to energy prices (gas $3-6/MMBtu, power $30-60/MWh)
""",
            key_factors=[
                "Calcination at 900C dominates energy requirement (5-6 GJ/tonne thermal)",
                "Oxy-combustion calciner produces pure CO2 but needs ASU oxygen",
                "Natural gas heat source undermines net carbon removal by 30%",
                "Large contactor towers (10-20 m) enable economies of scale",
                "Calcium carbonate cycle is mature industrial process (lime production)",
                "Cost target $94-232/tonne competitive with solid sorbent DAC",
                "Lifecycle carbon accounting must include calciner fuel emissions"
            ],
            primary_authority=[
                "Keith et al., 'A Process for Capturing CO2 from the Atmosphere', Joule 2018",
                "Carbon Engineering pilot plant data (Squamish, BC)",
                "Holmes & Keith, 'An air-liquid contactor for large-scale capture of CO2 from air', Phil Trans Royal Soc A 2012"
            ],
            burden_holder="Developer to demonstrate lifecycle net-negative with low-carbon heat source",
            adversary_position="Natural gas-fired calcination creates 0.3 tonne CO2 per tonne captured, undermining climate benefit",
            counter_arguments=[
                "Lifecycle net-negative if using renewable electricity for calcination",
                "Captured CO2 can be permanently stored (99%+ retention over 1000 years)",
                "Scale advantages over solid sorbent DAC (1 Mt vs. 10 kt plants)",
                "Mature calcium carbonate chemistry reduces technology risk",
                "45Q tax credit $180/tonne makes economics attractive even at $200/tonne cost",
                "Process heat integration with industrial sources (cement, steel) possible"
            ],
            resolution_strategy="Calculate net lifecycle carbon removal accounting for all energy sources, compare $/tonne net-negative CO2 vs. other CDR options",
            entity_scope="Large-scale DAC plants (>100 kt/year), carbon removal markets, oil companies for EOR",
            confidence=ConfidenceLevel.AGGRESSIVE
        )

        doctrines["co2_pipeline_transport"] = DoctrineBlock(
            topic="CO2 Pipeline Transport in Dense Phase",
            keywords=["CO2 pipeline", "dense phase", "supercritical", "ASME B31.4", "corrosion", "pipeline safety"],
            conclusion_template="CO2 transported in dense phase (liquid-like) at 85-150 bar, >31C to minimize compression energy. ASME B31.4 governs design. Impurities (H2S, O2, H2O) cause corrosion; specifications limit to <50 ppm each. US has 5000+ miles of CO2 pipelines for EOR.",
            reasoning_framework="""
CO2 pipeline transportation engineering and safety analysis:
1. PHASE BEHAVIOR - CO2 phase diagram drives design decisions
   - Critical point: 31.0C, 73.8 bar (1071 psi)
   - Dense phase (liquid or supercritical) 10-100x denser than gas (reduces pipe diameter)
   - Typical transport conditions: 100-150 bar, 20-50C (well above critical point)
   - Avoiding two-phase flow critical (slugging, erosion, control issues)
2. PIPELINE DESIGN CODE - ASME B31.4 for liquid petroleum pipelines
   - Wall thickness: t = PD / (2SFE + PY)  where S=allowable stress, F=design factor, E=weld efficiency, Y=temp factor
   - Design factor F = 0.72 (Class 1 location) to 0.4 (Class 4 high-density area)
   - Material: API 5L X52-X70 carbon steel (higher grade for high pressure)
   - Hydrostatic test: 1.25-1.5x design pressure for 4-8 hours
3. COMPRESSION REQUIREMENTS - Booster stations every 100-300 km
   - Pressure drop 0.3-1.0 bar/km depending on flow rate, diameter, roughness
   - Centrifugal compressors or pumps (if already liquid phase)
   - Intercooling to maintain temperature <50C (avoids thermal expansion issues)
4. IMPURITY SPECIFICATIONS - Critical for corrosion and safety
   - H2O <50 ppm (prevents carbonic acid formation: CO2 + H2O → H2CO3)
   - H2S <200 ppm (sulfide stress cracking risk)
   - O2 <10 ppm (oxidation, corrosion)
   - Non-condensables (N2, Ar, CH4) <4% (phase behavior shift)
   - Dehydration typically with triethylene glycol (TEG) to achieve <50 ppm H2O
5. CORROSION MANAGEMENT - CO2 + H2O forms carbonic acid
   - Internal coating (epoxy, FBE) or corrosion inhibitors
   - Corrosion coupons and ER probes for monitoring
   - Cathodic protection for external corrosion (galvanic or impressed current)
   - Material selection: 316SS for wet CO2, carbon steel OK if dry
6. SAFETY CONSIDERATIONS - Dense-phase CO2 release creates asphyxiation hazard
   - CO2 heavier than air, accumulates in low-lying areas
   - Leak detection: pressure monitoring, fiber optic, infrared cameras
   - Emergency shutdown valves every 10-20 km in populated areas
   - Odorant addition considered but not standard (unlike natural gas)
7. EXISTING INFRASTRUCTURE - US has ~5000 miles of CO2 pipelines (mostly EOR in Permian Basin)
   - Cortez pipeline (CO2 from Colorado to Texas): 808 km, 30 inch, 20 Mt/year capacity
   - Greenfield CCS pipelines require new ROW, permitting (2-5 years)
   - Shared infrastructure (trunk lines) improves economics for clustered sources
8. ECONOMIC SCALING - Economies of scale favor large-diameter pipes
   - Capital cost: $50,000-150,000/inch-mile (diameter dependent)
   - Transport cost: $1-5/tonne CO2 per 100 km (flow rate 1-10 Mt/year)
   - Compression energy: 50-150 kWh/tonne CO2 per 1000 km
""",
            key_factors=[
                "Dense phase transport at 100-150 bar minimizes compression energy",
                "Water content must be <50 ppm to prevent carbonic acid corrosion",
                "ASME B31.4 code governs design (not B31.8 for natural gas)",
                "Booster compression every 100-300 km depending on flow rate",
                "Existing EOR pipeline network (5000 miles) provides operational experience",
                "Pipeline diameter 8-36 inch typical, larger for high flow rates",
                "Right-of-way acquisition and permitting 2-5 years for greenfield"
            ],
            primary_authority=[
                "ASME B31.4 Pipeline Transportation Systems for Liquid Hydrocarbons and Other Liquids",
                "DOE/NETL Best Practices for CO2 Pipeline Transportation",
                "IEAGHG Report 2013-18: CO2 Pipeline Infrastructure"
            ],
            burden_holder="Pipeline operator to prove impurity specs met, pressure rating adequate for worst-case conditions",
            adversary_position="CO2 pipeline rupture could asphyxiate nearby population (Lake Nyos analogy)",
            counter_arguments=[
                "Existing CO2 pipelines (5000+ miles) have excellent safety record",
                "Leak detection and emergency shutdown systems mitigate risk",
                "Pipeline corridors avoid high-density population areas (Class 3-4)",
                "CO2 disperses rapidly in atmosphere (unlike Lake Nyos confined valley)",
                "Risk assessment shows pipeline safer than truck/rail CO2 transport"
            ],
            resolution_strategy="Conduct quantitative risk assessment (QRA) per CFR 195, demonstrate ALARP (as low as reasonably practicable) risk with leak detection and ESD valves",
            entity_scope="CO2 capture projects >0.5 Mt/year, shared pipeline infrastructure, EOR operators",
            confidence=ConfidenceLevel.DEFENSIBLE
        )

        doctrines["geological_storage_saline"] = DoctrineBlock(
            topic="Geological CO2 Storage in Deep Saline Aquifers",
            keywords=["geological storage", "saline aquifer", "injectivity", "caprock", "Class VI well", "monitoring"],
            conclusion_template="Deep saline aquifers (>800 m depth) provide largest CO2 storage potential (thousands of Gt globally). Supercritical CO2 displaces brine, trapped by impermeable caprock. Class VI injection wells require comprehensive site characterization, modeling, and monitoring per EPA UIC regulations.",
            reasoning_framework="""
Saline aquifer CO2 storage geological and regulatory analysis:
1. FORMATION SELECTION CRITERIA - Deep, porous, permeable sandstone or carbonate
   - Depth >800 m to ensure supercritical CO2 (density 500-800 kg/m3 vs. 1.87 kg/m3 gas)
   - Porosity >12% (storage capacity), permeability >50 mD (injectivity)
   - Thickness >20 m (sufficient storage volume)
   - Lateral extent >100 km2 (reduces pressure buildup)
2. CAPROCK INTEGRITY - Impermeable seal prevents upward migration
   - Typical: shale, mudstone, anhydrite, salt (permeability <1 nD)
   - Thickness >10 m (redundancy for fractures, faults)
   - Capillary entry pressure >1 MPa (CO2 column height >150 m)
   - Geochemical stability: resist acidification from dissolved CO2 (pH ~3-4)
3. TRAPPING MECHANISMS - Four phases over 1000-year storage period
   - Structural/stratigraphic trapping (0-100 years): CO2 trapped beneath caprock dome
   - Residual trapping (10-1000 years): CO2 blobs immobilized by capillary forces
   - Solubility trapping (100-10000 years): CO2 dissolves in brine, increases density, sinks
   - Mineral trapping (1000+ years): CO2 reacts with minerals forming stable carbonates (CaCO3, MgCO3)
4. INJECTIVITY ASSESSMENT - Pressure buildup limits injection rate
   - Darcy's Law: Q = (2πkh/μ) * (Pwell - Pres) / ln(re/rwell)
   - Typical injection rate: 0.5-3.0 Mt CO2/year per well
   - Pressure limit: <90% fracture gradient (avoid hydrofracturing)
   - Multiple wells needed for large projects (>3 Mt/year)
5. PLUME MIGRATION MODELING - Numerical simulation (TOUGH2, CMG-GEM)
   - Two-phase flow (CO2 + brine), gravity override, viscous fingering
   - Heterogeneity: permeability variations cause preferential pathways
   - Pressure interference between wells if spacing <2 km
   - 1000-year simulation shows plume typically <10 km radius
6. EPA CLASS VI WELL REGULATIONS - Underground Injection Control (UIC) program
   - Site characterization: seismic surveys, stratigraphic logs, core analysis, formation testing
   - Area of Review (AoR): region where pressure increase >0.7 bar (affects existing wells)
   - Corrective action: plug abandoned wells in AoR that penetrate injection zone
   - Financial assurance: bond for closure and 50-year post-injection monitoring
7. MONITORING VERIFICATION ACCOUNTING (MVA) - Multi-method plume tracking
   - Downhole pressure/temperature sensors, U-tube sampling
   - 4D seismic (time-lapse) detects CO2 saturation changes
   - Groundwater monitoring wells (shallow aquifers above caprock)
   - Surface deformation (InSAR satellite) detects pressure-induced uplift
   - Soil gas surveys (CO2, radon) detect potential leakage
8. SITE CLOSURE AND LONG-TERM STEWARDSHIP - Post-injection period
   - Well plugging per API standards (cement plugs every 100 m)
   - 50-year monitoring period to demonstrate plume stability
   - Liability transfer to federal government possible under FUTURE Act (not yet implemented)
""",
            key_factors=[
                "Depth >800 m ensures supercritical CO2 for storage efficiency",
                "Caprock integrity critical - shale/mudstone >10 m thick, low permeability",
                "Injectivity 0.5-3 Mt/year per well typical, limited by pressure buildup",
                "EPA Class VI permit requires 2-5 years site characterization and modeling",
                "Four trapping mechanisms provide redundancy over 1000 years",
                "MVA program costs $2-5M/year (downhole, seismic, groundwater)",
                "Abandoned well corrective action can add $1-10M depending on AoR size"
            ],
            primary_authority=[
                "40 CFR Part 146 Subpart H - Class VI Well Requirements",
                "EPA Class VI Well Guidance documents (2010-2012)",
                "IPCC Special Report on CO2 Capture and Storage (2005), Chapter 5"
            ],
            burden_holder="Well operator to demonstrate containment over 1000-year period with <1% leakage",
            adversary_position="CO2 could leak to groundwater, acidify aquifers, or escape to atmosphere",
            counter_arguments=[
                "Four independent trapping mechanisms provide redundancy",
                "Natural CO2 reservoirs (e.g., McElmo Dome) demonstrate million-year containment",
                "Comprehensive MVA detects leakage early for remediation",
                "Caprock integrity demonstrated through geochemical and geomechanical modeling",
                "Class VI regulations are most stringent injection well standard globally",
                "Operational projects (Illinois Basin, Gorgon) show successful containment"
            ],
            resolution_strategy="Demonstrate through detailed reservoir simulation and risk assessment that probability of >1% leakage over 1000 years is <1%, supported by MVA plan",
            entity_scope="CCS projects >1 Mt/year, industrial CO2 emitters, DAC with permanent storage",
            confidence=ConfidenceLevel.DEFENSIBLE
        )

        doctrines["co2_eor"] = DoctrineBlock(
            topic="CO2 Enhanced Oil Recovery (EOR) and Incidental Storage",
            keywords=["EOR", "enhanced oil recovery", "WAG", "miscible flood", "tertiary recovery", "incidental storage"],
            conclusion_template="CO2 EOR injects CO2 to mobilize residual oil, increasing recovery by 5-25% OOIP. Water-Alternating-Gas (WAG) process typical. 30-60% of injected CO2 remains stored in reservoir (incidental storage). Produces oil (emits CO2 when burned), so net carbon benefit debated.",
            reasoning_framework="""
CO2 EOR process and carbon accounting analysis:
1. MISCIBLE DISPLACEMENT MECHANISM - CO2 dissolves in oil, reduces viscosity
   - Minimum Miscibility Pressure (MMP): 1200-3000 psi depending on oil composition
   - Operate above MMP for miscible flood (higher recovery)
   - CO2 swells oil, reduces interfacial tension, extracts light hydrocarbons
   - Typical incremental recovery: 5-15% OOIP (waterflooded reservoirs), up to 25% in favorable cases
2. WATER-ALTERNATING-GAS (WAG) INJECTION - Improves sweep efficiency
   - Pattern: CO2 slug (0.3-0.5 pore volumes) → Water slug → CO2 slug → repeat
   - Water mobility control: reduces CO2 fingering through high-perm zones
   - WAG ratio: 1:1 to 2:1 (water:CO2) typical
   - Cycle length: weeks to months depending on reservoir size
3. PRODUCED GAS RECYCLE - CO2 separated from produced oil and re-injected
   - Surface separation (pressure reduction, gas-liquid separators)
   - CO2 recycle: 50-70% of produced gas is CO2 (balance is CH4, N2)
   - Recompression to injection pressure (2000-4000 psi)
   - Makeup CO2 purchased to offset storage and losses (30-60% of injected CO2)
4. INCIDENTAL CO2 STORAGE - Net storage in reservoir
   - Mechanisms: residual trapping in pore space, dissolution in brine/oil, mineral carbonation (minor)
   - Utilization factor: 0.3-0.6 tonne CO2 net stored per bbl incremental oil
   - Storage efficiency depends on reservoir pressure maintenance and well control
5. CARBON LIFECYCLE ACCOUNTING - Gross vs. net emissions
   - Gross storage: total CO2 injected minus recycled = 0.3-0.6 tonne/bbl
   - Emissions from oil combustion: 0.43 tonne CO2/bbl (industry average)
   - Net carbon balance: negative (emits more than stores) unless accounting for displaced oil
   - Displacement credit argument: EOR oil displaces higher-carbon oil from another source
6. 45Q TAX CREDIT ELIGIBILITY - $35-60/tonne CO2 for EOR (lower than $85 for saline storage)
   - Original 45Q (2008): $10/tonne EOR, $20/tonne storage
   - Inflation Reduction Act (2022): $60/tonne EOR, $85/tonne storage (inflation-adjusted)
   - Must demonstrate secure geological storage, annual third-party verification
   - 12-year credit period from start of injection
7. EXISTING CO2 EOR INFRASTRUCTURE - Permian Basin dominance
   - 13+ major CO2 floods, 70+ Mt CO2/year injected (mostly natural sources)
   - Cortez, Sheep Mountain, McElmo Dome natural CO2 sources (8-9 Mt/year each)
   - Anthropogenic CO2 from gas processing, ethanol, fertilizer plants emerging
   - Pipeline network: 5000+ miles dedicated CO2 pipelines in US
8. FUTURE CCUS-EOR INTEGRATION - Anthropogenic CO2 sources for EOR
   - Displaces natural CO2 sources for other uses
   - Enables CCS economic viability in regions with mature oil fields
   - Challenges: impurity tolerance (EOR needs >95% CO2, CCS may have 90-92%)
""",
            key_factors=[
                "Incremental oil recovery 5-25% OOIP depending on reservoir quality",
                "Net CO2 storage 0.3-0.6 tonne/bbl incremental oil",
                "Operates above MMP (1200-3000 psi) for miscible displacement",
                "WAG process improves sweep efficiency vs. continuous CO2 injection",
                "Lifecycle carbon accounting critical: stored CO2 vs. emitted from oil combustion",
                "45Q credit $60/tonne for EOR vs. $85/tonne for dedicated storage",
                "Existing infrastructure (Permian Basin) lowers CO2 transport cost"
            ],
            primary_authority=[
                "DOE/NETL Carbon Storage Atlas (5th edition) - EOR chapter",
                "SPE Monograph: Enhanced Oil Recovery (Lake et al., 1992)",
                "IEAGHG Report 2009-12: CO2 Storage in Depleted Oilfields"
            ],
            burden_holder="EOR operator to quantify and verify net CO2 storage for 45Q credit eligibility",
            adversary_position="CO2-EOR produces more oil, which emits CO2 when burned, so net climate impact is negative",
            counter_arguments=[
                "Displacement credit: EOR oil displaces higher-carbon sources (oil sands, deep offshore)",
                "Partial storage (30-60%) better than no storage",
                "Economic bridge: 45Q EOR credit funds development of pure storage projects",
                "Existing infrastructure reduces CCS deployment cost in oil-producing regions",
                "Future: EOR fields convert to pure storage after oil depletion"
            ],
            resolution_strategy="Conduct lifecycle carbon assessment with and without displacement credit, compare net emissions to alternative oil sources",
            entity_scope="Mature oil fields (>50% depleted), CO2 pipeline-accessible regions, integrated CCS-EOR projects",
            confidence=ConfidenceLevel.DISCLOSURE
        )

        doctrines["45q_tax_credit"] = DoctrineBlock(
            topic="Section 45Q Tax Credit for Carbon Capture and Sequestration",
            keywords=["45Q", "tax credit", "IRA", "carbon capture", "sequestration", "utilization", "Inflation Reduction Act"],
            conclusion_template="Section 45Q provides tax credits for CO2 capture and storage: $85/tonne for geological storage, $60/tonne for EOR, $180/tonne for DAC storage, $130/tonne for DAC utilization. Inflation Reduction Act (2022) extended credit to 2032 and raised rates. Annual third-party verification required.",
            reasoning_framework="""
Section 45Q tax credit structure and eligibility analysis:
1. CREDIT RATES (Inflation Reduction Act 2022, inflation-adjusted annually)
   - Point-source capture + geological storage: $85/tonne CO2 (was $50)
   - Point-source capture + EOR or utilization: $60/tonne CO2 (was $35)
   - Direct air capture + geological storage: $180/tonne CO2 (was $130)
   - Direct air capture + utilization: $130/tonne CO2 (was $95)
   - Rates indexed to inflation after 2026 (CPI-U)
2. ELIGIBILITY THRESHOLDS - Minimum annual capture requirements
   - Electricity generation: ≥12,500 tonnes CO2/year (was 500,000)
   - Other industrial facilities: ≥12,500 tonnes CO2/year (was 100,000)
   - Direct air capture: ≥1,000 tonnes CO2/year (new category)
   - Measurement: annual basis, rolling 12-month average
3. QUALIFIED FACILITIES - Beginning of construction deadline
   - Facilities must begin construction before 2033 (was 2026)
   - Safe harbor: 5% of total cost incurred or physical work started
   - 4-year continuity requirement from beginning to placed-in-service
   - Continuous operation requirement dropped (allows intermittent operation)
4. SECURE GEOLOGICAL STORAGE - Permanent sequestration required
   - Depleted oil/gas reservoirs, saline formations, unmineable coal seams
   - EPA Class VI injection well or state-approved equivalent
   - Excludes utilization unless stored >geological timescales (e.g., mineralization)
   - Leakage recapture: credit recaptured if CO2 leaks within credit period
5. UTILIZATION PATHWAYS - Non-storage uses eligible at lower credit rate
   - Enhanced oil recovery (EOR) - must demonstrate secure storage
   - Chemical/fuel synthesis (e.g., methanol, synthetic fuels) - excludes combustion
   - Concrete mineralization - permanent incorporation
   - Beverage/food grade CO2 - excluded (recycled to atmosphere)
6. VERIFICATION AND REPORTING - Annual third-party certification
   - ISO 27916 or EPA MRR Protocol for quantification
   - Third-party engineer certification of capture, transport, storage
   - IRS Form 8933 filed annually with tax return
   - State tax authorities may require additional reporting
7. CREDIT PERIOD AND TRANSFERABILITY - 12-year credit from placed-in-service
   - Election of credit at facility placed-in-service date
   - Credits can be transferred or sold (after IRA 2022)
   - Direct pay option for tax-exempt entities (first 5 years)
   - Recapture if facility ceases operation before 12 years
8. WAGE AND APPRENTICESHIP REQUIREMENTS - Prevailing wage standards
   - Facilities >1 MW must pay Davis-Bacon prevailing wages
   - Apprenticeship hours: 10-15% of total labor hours
   - Penalty for non-compliance: credit reduced to 20% of full amount
   - Exception: <1 MW or facilities with construction beginning before 2023
9. STACKING WITH OTHER INCENTIVES - Interaction with state/local credits
   - Cannot stack with Advanced Energy Project Credit (48C) on same property
   - Can combine with state credits (California LCFS, RGGI proceeds)
   - Can combine with grant funding (DOE, USDA) if not covering same costs
   - Bonus depreciation (MACRS) can be layered with 45Q
10. ECONOMIC IMPACT - Project economics transformation
    - $85/tonne storage credit covers 50-80% of typical CCS cost
    - DAC credit $180/tonne covers current costs ($400-800/tonne)
    - Enables unsubsidized CCS deployment for many industries
    - 12-year credit period supports project finance (IRR improvement 3-7%)
""",
            key_factors=[
                "Credit rates: $85/tonne storage, $60/tonne EOR, $180/tonne DAC storage",
                "Threshold lowered to 12,500 tonne/year for industrial, 1,000 for DAC",
                "Construction deadline extended to 2032 (must begin before 2033)",
                "Annual third-party verification required (ISO 27916 or EPA MRR)",
                "12-year credit period from placed-in-service date",
                "Prevailing wage and apprenticeship requirements for >1 MW facilities",
                "Credit transferability enables tax equity financing",
                "Inflation indexing after 2026 maintains real value"
            ],
            primary_authority=[
                "Internal Revenue Code Section 45Q (as amended by IRA 2022)",
                "IRS Notice 2021-66 (Guidance on 45Q)",
                "Inflation Reduction Act of 2022, Pub. L. 117-169"
            ],
            burden_holder="Taxpayer claiming credit to demonstrate capture, secure storage, and annual verification",
            adversary_position="45Q credit is corporate subsidy that extends fossil fuel industry life",
            counter_arguments=[
                "CCS enables deep decarbonization of hard-to-abate sectors (cement, steel, chemicals)",
                "Tax credit cost-effective vs. regulatory mandates (CBO analysis: $70/tonne avoided)",
                "DAC credit necessary to achieve negative emissions for net-zero targets",
                "Credit sunset in 2032 provides urgency for deployment",
                "Third-party verification ensures environmental integrity",
                "Economic multiplier: $1 credit generates $2-3 in private investment"
            ],
            resolution_strategy="Calculate project IRR with and without 45Q credit, demonstrate economic viability gap that credit fills",
            entity_scope="Power plants, industrial emitters (cement, steel, refining, chemicals, ethanol), DAC facilities",
            confidence=ConfidenceLevel.DEFENSIBLE
        )

        doctrines["oxy_combustion"] = DoctrineBlock(
            topic="Oxy-Combustion CO2 Capture Technology",
            keywords=["oxy-combustion", "oxy-fuel", "air separation", "ASU", "flue gas recycle", "cryogenic separation"],
            conclusion_template="Oxy-combustion burns fuel in nearly pure O2 (95%+) instead of air, producing flue gas with 80-90% CO2 (vs. 12-15% in air-fired). Requires air separation unit (ASU) for oxygen production. Flue gas recycle controls flame temperature. Energy penalty 20-30% similar to post-combustion amine.",
            reasoning_framework="""
Oxy-combustion capture process and integration analysis:
1. AIR SEPARATION UNIT (ASU) - Cryogenic distillation produces 95-99% O2
   - Air compressed to 5-6 bar, cooled, liquefied at -180C
   - Distillation column separates O2 (boiling point -183C) from N2 (-196C)
   - ASU power consumption: 200-250 kWh/tonne O2 (major energy penalty)
   - Oxygen purity tradeoff: 95% O2 uses less power than 99%, but higher N2 in flue gas
2. OXY-COMBUSTION PROCESS - Fuel burned in O2/recycled flue gas mixture
   - O2 concentration 25-35% in burner (balance is recycled CO2)
   - Flue gas recycle rate: 60-70% to control flame temperature to 1400-1600C (similar to air-fired)
   - Adiabatic flame temperature in pure O2: >3000C (would melt boiler tubes)
   - Burner modifications: different flame shape, radiative heat transfer dominates
3. FLUE GAS COMPOSITION - High CO2 concentration simplifies capture
   - Dry basis: 75-85% CO2, 10-20% H2O, 2-5% O2, 1-3% N2/Ar
   - After condensation (remove H2O): 85-95% CO2 ready for compression
   - Trace contaminants: SOx, NOx, particulates removed by conventional cleanup
   - CO2 purity sufficient for pipeline transport and storage (>95% target)
4. FLUE GAS PROCESSING - Multi-stage cleanup and CO2 purification
   - Particulate removal: ESP or baghouse (conventional)
   - SOx removal: wet FGD or dry sorbent injection (SO2 + CaO → CaSO3)
   - NOx control: SCR or low-NOx burners (lower NOx than air-fired due to no fuel-N2 reaction)
   - Flue gas cooling and water condensation (recovers latent heat)
   - CO2 purification unit (CPU): removes N2/Ar by cryogenic or membrane separation if needed
5. ENERGY PENALTY BREAKDOWN - Total parasitic load 20-30% of gross output
   - ASU: 10-15% (dominant, scales with O2 purity)
   - CO2 compression to 110 bar: 7-10%
   - Flue gas recycle fans: 2-3%
   - CPU (if used): 2-5%
   - Total net efficiency: coal plant 35% → 25-28%, NGCC 55% → 40-43%
6. INTEGRATION WITH BOILER - Retrofit vs. new-build considerations
   - Retrofit challenges: burner replacement, ID fan capacity, material compatibility
   - New-build optimized: smaller boiler (no N2 ballast), compact flue gas handling
   - Supercritical steam cycle integration improves efficiency 2-3% vs. subcritical
7. ADVANTAGES VS. POST-COMBUSTION - No separate capture unit, high-purity CO2
   - No amine solvent (no degradation, makeup, emissions)
   - Smaller back-end equipment (high CO2 concentration)
   - Lower water consumption (no amine wash, smaller FGD)
8. DISADVANTAGES - ASU cost and complexity, retrofit difficulty
   - ASU capital cost: $500-800/tonne O2 daily capacity
   - Cryogenic equipment reliability concerns in power plant environment
   - Startup/shutdown coordination between ASU and boiler complex
   - Air separation market dominated by 3 vendors (Air Liquide, Linde, Air Products)
""",
            key_factors=[
                "ASU power consumption 200-250 kWh/tonne O2 dominates energy penalty",
                "Flue gas recycle at 60-70% controls flame temperature to ~1500C",
                "Produces 85-95% CO2 flue gas after water removal (vs. 12-15% air-fired)",
                "Energy penalty 20-30% comparable to post-combustion amine",
                "No amine solvent eliminates degradation and emissions issues",
                "Retrofit difficult due to burner and fan modifications",
                "ASU capital cost $500-800M for 500 MW plant"
            ],
            primary_authority=[
                "IEAGHG Report 2005-01: Oxy-combustion Processes for CO2 Capture",
                "DOE/NETL Oxy-Combustion Technology Development Program reports",
                "Buhre et al., 'Oxy-fuel combustion technology', Prog Energy Combust Sci 2005"
            ],
            burden_holder="Developer to demonstrate ASU reliability and cost competitive with post-combustion",
            adversary_position="ASU complexity and cost make oxy-combustion uneconomic vs. post-combustion amine",
            counter_arguments=[
                "No amine degradation eliminates ongoing makeup cost and emissions",
                "High-purity CO2 stream reduces purification cost",
                "Lower water consumption in water-constrained regions",
                "Smaller footprint for new-build plants (no separate capture unit)",
                "ASU can produce O2 for other plant uses (gasification, chemical production)",
                "Technology learning curve: ASU cost declining with scale"
            ],
            resolution_strategy="Compare levelized cost of capture ($/tonne CO2) for oxy-combustion vs. post-combustion amine, site-specific for retrofit vs. new-build",
            entity_scope="Coal and gas power plants >300 MW, cement kilns, industrial boilers",
            confidence=ConfidenceLevel.AGGRESSIVE
        )

        doctrines["co2_compression"] = DoctrineBlock(
            topic="CO2 Compression for Pipeline Transport and Storage",
            keywords=["CO2 compression", "multi-stage", "intercooling", "dense phase", "power consumption", "integrally geared"],
            conclusion_template="CO2 compressed from atmospheric (capture outlet) to 110-150 bar (pipeline/injection pressure) in multi-stage centrifugal compressors. Power consumption 90-120 kWh/tonne CO2. Intercooling between stages reduces work. Phase transition through critical point (73.8 bar, 31C) requires careful design.",
            reasoning_framework="""
CO2 compression system design and energy analysis:
1. COMPRESSION STAGES - Typically 4-8 stages from 1 bar to 110-150 bar
   - Stage pressure ratio: 2-3 per stage (thermodynamic optimum)
   - Intercooling to 30-40C between stages (reduces work, density increases)
   - Final discharge: 110 bar (pipeline), 150 bar (injection well), 200+ bar (ship transport)
   - Two-phase region avoided: keep above saturation curve during compression
2. PHASE BEHAVIOR CONSIDERATIONS - Critical point at 31.0C, 73.8 bar
   - Below critical point: distinct liquid and vapor phases (two-phase compression inefficient)
   - Above critical point: supercritical fluid (single phase, compressible liquid-like behavior)
   - Compression path typically crosses critical region in Stage 3-4
   - Temperature control critical: intercooling prevents excessive temperature rise (>150C reduces efficiency)
3. COMPRESSOR TYPE SELECTION - Centrifugal vs. reciprocating
   - Centrifugal (integrally geared): most common for large flow (>100 tonne/hr)
     * Multiple pinions on single bull gear, 10,000-20,000 RPM
     * High efficiency 78-82% isentropic
     * Lower maintenance than reciprocating
   - Reciprocating: smaller flows (<50 tonne/hr), higher discharge pressure capability
     * Positive displacement, handles two-phase better
     * Lower efficiency 70-75%, higher maintenance
   - Liquid pumps: if CO2 already liquid (low-temperature capture), pump to pressure (30-50 kWh/tonne)
4. POWER CONSUMPTION CALCULATION - Isentropic compression work
   - Ideal work: W = nRT(k/(k-1))[(P2/P1)^((k-1)/k) - 1] per stage
   - Total: 90-120 kWh/tonne CO2 (1-110 bar, 4-6 stages, 80% efficiency)
   - Varies with inlet conditions: cold CO2 requires less work (denser)
   - Impurity effect: non-condensables (N2, Ar) increase work 10-20%
5. INTERCOOLING SYSTEM - Shell-and-tube heat exchangers
   - Cooling medium: cooling tower water, air-cooled if water-scarce
   - Temperature approach: 5-10C (balance heat exchanger size vs. compression work)
   - Condensate knockout: remove water condensed during cooling (prevents corrosion)
   - Interstage pressure control: anti-surge valves prevent compressor instability
6. DRIVER SELECTION - Electric motor vs. gas turbine
   - Electric motor: 90-95% efficient, grid-powered (preferred if low-carbon electricity available)
   - Gas turbine: 30-40% efficient, used if waste heat can be utilized or grid unreliable
   - Variable frequency drive (VFD): turndown capability for part-load operation
7. ENERGY INTEGRATION OPPORTUNITIES - Waste heat recovery
   - Intercooler heat: low-grade (40-60C), can preheat boiler feedwater or heat buildings
   - Compression heat of CO2: 400-500 kJ/kg (thermodynamically available but low temperature)
   - Organic Rankine Cycle (ORC) can generate 5-10% power recovery from compression heat
8. SYSTEM REDUNDANCY - N+1 or 100% spare compressor
   - High availability required (>95%) for continuous capture operation
   - Maintenance: major overhaul every 24,000-40,000 hours (3-5 years)
   - Startup time: 30-60 minutes (gradual pressure ramp to avoid surge)
""",
            key_factors=[
                "Multi-stage compression 4-8 stages to reach 110-150 bar",
                "Power consumption 90-120 kWh/tonne CO2 (major operating cost)",
                "Intercooling between stages to 30-40C reduces total work 20-30%",
                "Integrally geared centrifugal compressors most common for >100 tonne/hr",
                "Phase transition through critical point (73.8 bar) requires temperature control",
                "Electric motor drive preferred for low-carbon operation",
                "Energy integration (heat recovery) can reduce net power by 5-10%"
            ],
            primary_authority=[
                "MAN Energy Solutions - CO2 Compression Technology white papers",
                "DOE/NETL Cost and Performance Baseline - CO2 Compression section",
                "Aspelund et al., 'Ship Transport of CO2', Int J Greenhouse Gas Control 2006 (includes compression)"
            ],
            burden_holder="Compressor vendor to guarantee performance (flow, pressure, power) at specified conditions",
            adversary_position="Compression energy penalty (7-10% of plant output) undermines CCS efficiency",
            counter_arguments=[
                "Compression energy small compared to capture (25-35% penalty)",
                "Essential for pipeline transport and geological storage (no alternative)",
                "Technology mature (40+ years CO2 compression for EOR)",
                "Efficiency improving: integrally geared compressors 78-82% isentropic",
                "Heat recovery can offset 5-10% of compression power",
                "Cost declining with scale and learning curve"
            ],
            resolution_strategy="Optimize stage count and intercooling to minimize total power, demonstrate <100 kWh/tonne with heat recovery",
            entity_scope="All CCS projects, DAC facilities, CO2 transport infrastructure",
            confidence=ConfidenceLevel.DEFENSIBLE
        )

        doctrines["ccus_lifecycle_assessment"] = DoctrineBlock(
            topic="CCUS Lifecycle Carbon Accounting and Net Climate Benefit",
            keywords=["lifecycle assessment", "LCA", "system boundary", "carbon intensity", "net climate benefit", "fugitive emissions"],
            conclusion_template="Lifecycle carbon assessment of CCUS must account for energy source carbon intensity, fugitive emissions, and end-use fate. Net climate benefit requires low-carbon energy for capture/compression and permanent storage. EOR with oil combustion may have neutral or negative climate impact without displacement credit.",
            reasoning_framework="""
CCUS lifecycle carbon accounting framework:
1. SYSTEM BOUNDARY DEFINITION - Cradle-to-grave scope
   - Upstream: fuel extraction, transport, processing for energy supply
   - Construction: materials (steel, concrete), equipment manufacturing, transport
   - Operation: energy for capture, compression, transport, injection; fugitive emissions
   - End-of-life: well closure, monitoring, potential leakage over 1000 years
   - Counterfactual: baseline emissions without CCUS (key reference case)
2. ENERGY SOURCE CARBON INTENSITY - Dominates lifecycle emissions
   - Coal electricity for capture plant: 0.8-1.0 tonne CO2/MWh (undermines benefit)
   - Natural gas electricity: 0.4-0.5 tonne CO2/MWh (partial benefit)
   - Renewable electricity (wind, solar, hydro): 0.02-0.05 tonne CO2/MWh (near-zero)
   - Heat for regeneration/calcination: natural gas 0.2 tonne CO2/GJ, biomass near-zero
   - Example: Post-combustion amine using coal power: capture 0.9 tonne, emit 0.3 tonne (net 0.6 tonne)
3. FUGITIVE EMISSIONS - Leaks during transport and storage
   - Pipeline: 0.1-0.5% of transported CO2 (valves, flanges, compressors)
   - Injection well: 0.01-0.1% during injection phase (mechanical integrity)
   - Long-term storage: <0.01%/year leakage if site properly selected (IPCC consensus)
   - Cumulative over 1000 years: <1% total leakage (99% retention target)
4. CAPTURE EFFICIENCY - Percentage of source CO2 captured
   - Post-combustion amine: 85-95% (slip CO2 in flue gas)
   - Pre-combustion IGCC: >95% (high CO2 concentration)
   - Oxy-combustion: 90-95% (incomplete combustion, purge streams)
   - DAC: 100% by definition (but energy source emissions count)
5. UTILIZATION PATHWAY ACCOUNTING - Permanent vs. temporary CO2 fate
   - Geological storage: 99%+ permanent over 1000 years (full credit)
   - EOR: 30-60% incidental storage, oil burned releases 0.43 tonne CO2/bbl (net negative unless displacement credit)
   - Concrete carbonation: permanent mineralization (full credit)
   - Chemical synthesis (methanol, polymers): temporary (released at end-of-life, partial credit)
   - Beverage CO2: immediate release (zero credit)
6. DISPLACEMENT CREDIT DEBATE - Avoided emissions from alternative source
   - EOR oil displaces oil sands (0.5-0.7 tonne CO2/bbl) → net benefit arguable
   - CCS coal power displaces natural gas power → net benefit if coal cheaper
   - DAC with renewables displaces afforestation → neutral (both carbon-negative)
   - Methodological challenge: proving displacement (additionality)
7. CONSTRUCTION EMISSIONS - Embodied carbon in materials
   - Steel (capture unit, pipeline): 2-3 tonne CO2/tonne steel
   - Concrete (foundations): 0.1-0.2 tonne CO2/tonne concrete
   - Amine solvent production: 1-2 tonne CO2/tonne MEA
   - Total construction: 10-50 g CO2/tonne captured over 30-year life (minor)
8. SENSITIVITY ANALYSIS - Key uncertainties
   - Long-term storage retention (95-99.9%): 5-50% swing in net benefit
   - Energy source emissions (0.02-1.0 tonne/MWh): factor of 10 variation
   - EOR displacement credit (0-100%): determines net positive vs. negative
   - Fugitive emission rate (0.1-2%): minor sensitivity except for DAC
9. REPORTING STANDARDS - Methodologies for consistency
   - ISO 14064 (Greenhouse gases - quantification and reporting)
   - ISO 27916 (Carbon Capture and Storage - quantification and verification)
   - IPCC Guidelines for National GHG Inventories (default emission factors)
   - EPA Mandatory Reporting Rule (MRR) Subpart PP/RR/UU
10. NET CLIMATE BENEFIT THRESHOLDS - Policy targets
    - IPCC: >80% lifecycle emission reduction vs. unabated fossil for "low-carbon" label
    - California LCFS: >60% reduction for credit eligibility
    - EU CCS Directive: >50% reduction required
    - DAC: net-negative carbon required (lifecycle emissions <0)
""",
            key_factors=[
                "Energy source carbon intensity dominates lifecycle emissions",
                "Capture efficiency 85-95% typical, 5-15% CO2 slip",
                "Fugitive emissions <1% if properly operated",
                "Long-term storage retention 99%+ over 1000 years assumed",
                "EOR lifecycle benefit depends on displacement credit assumption",
                "Construction emissions minor (<5% of lifecycle)",
                "ISO 27916 standard for CCUS carbon accounting",
                "Net benefit threshold: >80% reduction (IPCC), >60% (CA LCFS)"
            ],
            primary_authority=[
                "IPCC Special Report on CCS (2005), Chapter 9 - Lifecycle Assessment",
                "ISO 27916:2019 - Carbon Capture and Storage - Quantification and Verification",
                "Rubin et al., 'The outlook for improved carbon capture technology', Prog Energy Combust Sci 2012"
            ],
            burden_holder="Project developer to demonstrate net climate benefit with transparent lifecycle accounting",
            adversary_position="CCUS using fossil-powered energy has negligible or negative net climate benefit",
            counter_arguments=[
                "Renewable-powered CCUS achieves >95% lifecycle emission reduction",
                "Even fossil-powered capture achieves 60-70% reduction (vs. 0% without CCS)",
                "CCS buys time for renewable buildout (dispatchable low-carbon power)",
                "Industrial CCS (cement, steel) has no renewable alternative",
                "DAC with renewables achieves durable carbon removal (negative emissions)",
                "EOR displacement credit justified if oil demand inelastic"
            ],
            resolution_strategy="Conduct full LCA per ISO 27916 with sensitivity analysis on energy source, storage retention, and displacement credit",
            entity_scope="All CCUS projects, carbon credit markets, climate policy evaluation",
            confidence=ConfidenceLevel.DISCLOSURE
        )

        # Additional doctrines for comprehensive coverage
        doctrines["class_vi_permitting"] = DoctrineBlock(
            topic="EPA Class VI Injection Well Permitting Process",
            keywords=["Class VI", "UIC", "injection well", "EPA permit", "area of review", "financial assurance"],
            conclusion_template="EPA Class VI permits required for CO2 injection wells (geological storage). Process takes 2-5 years, requires extensive site characterization, AoR delineation, corrective action plan, financial assurance for closure and 50-year post-injection monitoring. Most stringent injection well class.",
            reasoning_framework="""
Class VI permitting requirements and timeline:
1. PRE-APPLICATION PHASE - Site selection and initial characterization (6-12 months)
   - Geological desktop study: identify candidate formations (depth >800 m, porosity, permeability)
   - Lease/pore space acquisition (surface and mineral rights if separate)
   - Seismic survey (2D or 3D) to map structure, faults, caprock
   - Initial stratigraphic well drilling and logging (gamma, resistivity, porosity)
   - Formation testing (permeability, pressure, fluid sampling)
2. APPLICATION SUBMISSION - Comprehensive technical package (3-6 months to prepare)
   - Geology: structure maps, cross-sections, stratigraphic correlation
   - Hydrogeology: formation pressure, temperature, salinity, flow pathways
   - Geochemistry: mineralogy, formation fluid chemistry, CO2-rock reactions
   - Geomechanics: stress field, fracture gradient, fault stability
   - Reservoir modeling: injection simulation (TOUGH2, CMG-GEM), pressure buildup, plume migration
   - Well design: casing strings, cement, wellhead, tubing, packer
   - Area of Review (AoR): region where pressure increase >7 kPa (0.1 psi)
   - Corrective action: plan to plug/remediate existing wells in AoR that penetrate injection zone
3. EPA REVIEW AND PUBLIC COMMENT - Regulatory evaluation (12-24 months)
   - Technical review: EPA headquarters (OGWDW) and regional office
   - Completeness determination: 30 days
   - Public notice: 30-day comment period
   - Public hearing: if requested or EPA determines necessary
   - EPA response to comments: 60-90 days
   - Consultation: US Fish & Wildlife, state agencies, tribes if applicable
4. AREA OF REVIEW DELINEATION - Computational modeling requirement
   - Pressure increase threshold: 7 kPa (0.1 psi, ~2.3 ft head in freshwater)
   - Time period: injection + 50 years post-injection
   - All wells in AoR cataloged: active, inactive, abandoned, exploratory
   - Penetration of injection zone or confining layer triggers corrective action requirement
   - Re-delineation every 5 years as injection progresses (fixed or adaptive AoR)
5. CORRECTIVE ACTION - Abandoned well remediation (6-24 months, costly)
   - Wells improperly plugged must be re-entered and re-plugged to modern standards
   - Plug design: cement plugs every 100 m, mechanical bridge plugs, surface cap
   - Cost: $50,000-$500,000 per well depending on depth and condition
   - Liability: permittee responsible even if well drilled by others decades ago
6. FINANCIAL ASSURANCE - Bonding for closure and long-term care
   - Closure plan: well plugging, site restoration, final monitoring
   - Post-injection care: 50-year monitoring, potential corrective action
   - Amount: calculated per EPA guidance, typically $5M-$50M depending on project size
   - Instruments: surety bond, letter of credit, trust fund, self-insurance (if qualified)
7. MECHANICAL INTEGRITY TESTING (MIT) - Well integrity demonstration
   - Internal MIT: annulus pressure test (APT) to detect casing leaks
   - External MIT: radioactive tracer or temperature log to verify cement bond
   - Frequency: before injection start, every 5 years during injection, annually post-injection
   - Failure triggers corrective action: squeeze cementing, casing repair, or well abandonment
8. MONITORING AND REPORTING - Comprehensive MVA program
   - Operational: injection rate, pressure, temperature, CO2 volume (continuous)
   - Subsurface: observation wells (pressure, fluid sampling), seismic surveys (4D time-lapse)
   - Groundwater: shallow monitoring wells above confining layer (quarterly sampling)
   - Surface: soil gas, atmospheric, vegetation stress (annual)
   - Reporting: quarterly to EPA (injection data), annual (monitoring results), ad-hoc (incidents)
9. POST-INJECTION SITE CARE (PISC) - 50-year monitoring period
   - Begins after cessation of injection
   - Monitoring continues: pressure decline, plume stabilization, no groundwater impacts
   - Well plugging: injection and monitoring wells per API standards
   - Site closure certification: EPA approval required, may transfer liability to federal government (if FUTURE Act implemented)
10. PRIMACY AND STATE PROGRAMS - Alternative to direct EPA permitting
    - States can obtain primacy (authority to issue Class VI permits under state program)
    - As of 2024: North Dakota, Wyoming, Louisiana, West Virginia have primacy
    - State programs must be as stringent as federal (often more stringent)
    - Advantage: faster permitting (12-18 months vs. 24-36 for EPA), local expertise
""",
            key_factors=[
                "Permitting timeline 2-5 years depending on site complexity and public involvement",
                "AoR delineation critical: all wells penetrating injection zone need corrective action",
                "Financial assurance $5M-$50M for closure and 50-year post-injection monitoring",
                "Mechanical integrity testing every 5 years during injection, annually post-injection",
                "Corrective action for abandoned wells can cost $50k-$500k each",
                "State primacy programs (ND, WY, LA) can reduce permitting time 30-50%",
                "Public comment and hearing process can delay 6-12 months if opposition"
            ],
            primary_authority=[
                "40 CFR Part 146 Subpart H - Class VI Well Requirements",
                "EPA UIC Program Class VI Well Guidance documents (2010-2012)",
                "EPA Geologic Sequestration of CO2 - Underground Injection Control (UIC) Program"
            ],
            burden_holder="Well operator to demonstrate formation containment, well integrity, and financial assurance",
            adversary_position="Class VI permits inadequate to ensure thousand-year containment, risk to groundwater",
            counter_arguments=[
                "Most stringent injection well standard globally (vs. Class I, II, V)",
                "Comprehensive site characterization reduces risk of failure",
                "50-year monitoring demonstrates plume stability before closure",
                "Financial assurance ensures corrective action funds available",
                "Operational projects (Decatur, Archer Daniels Midland) show successful containment",
                "Natural CO2 reservoirs provide million-year analog for geological storage"
            ],
            resolution_strategy="Follow EPA Class VI guidance rigorously, engage early with regulator, over-design monitoring program to exceed minimum requirements",
            entity_scope="CO2 storage projects >12,500 tonne/year, industrial CCS, DAC with storage",
            confidence=ConfidenceLevel.DEFENSIBLE
        )

        doctrines["monitoring_verification_accounting"] = DoctrineBlock(
            topic="Monitoring, Verification, and Accounting (MVA) for CO2 Storage",
            keywords=["MVA", "monitoring", "verification", "4D seismic", "groundwater", "InSAR", "geochemical"],
            conclusion_template="MVA program detects CO2 plume migration, verifies containment, and accounts for stored mass. Methods include downhole pressure/temperature, 4D seismic, groundwater monitoring, soil gas surveys, InSAR surface deformation. Cost $2-5M/year. Required for Class VI permit and 45Q tax credit verification.",
            reasoning_framework="""
MVA program design and implementation framework:
1. OPERATIONAL MONITORING - Real-time injection parameters (continuous)
   - Downhole pressure and temperature sensors (PTG - pressure/temperature gauge)
   - Injection rate (mass flow meter or volumetric with density correction)
   - CO2 volume accounting: totalizer with accuracy ±2% required for 45Q
   - Automated SCADA system with alarms for pressure excursions
2. SUBSURFACE PLUME MONITORING - Detect CO2 migration pathways
   - Time-lapse (4D) seismic: repeat 3D surveys every 1-5 years
     * Detects CO2 saturation changes (amplitude, velocity, impedance)
     * Resolution: ~10 m vertical, ~50 m lateral
     * Cost: $5M-$15M per survey (amortized over 5-year interval)
   - Observation wells: drilled into injection zone or above caprock
     * Pressure monitoring: detect pressure communication, plume arrival
     * Fluid sampling: U-tube or downhole pump, analyze for CO2 content, pH
     * Spacing: 500 m to 2 km from injector depending on model predictions
   - Well logging: Repeat gamma, resistivity, neutron porosity in observation wells
     * Detects saturation changes (CO2 vs. brine)
     * Run annually or after significant injection volume
3. GROUNDWATER QUALITY MONITORING - Detect potential upward migration (quarterly)
   - Shallow monitoring wells: 100-300 m depth in USDW (underground source drinking water)
   - Parameters: pH, TDS, alkalinity, major ions (Ca, Mg, Fe, Mn), trace metals, CO2 partial pressure
   - Baseline: 4-8 samples before injection to establish natural variability
   - Trigger values: statistical deviation from baseline (e.g., 2 standard deviations)
   - Well count: minimum 3 (upgradient background, downgradient/on-site, downgradient/off-site)
4. ATMOSPHERIC AND SOIL GAS MONITORING - Detect surface leakage (annual)
   - Soil gas surveys: CO2, CH4, radon, oxygen (grid or along faults)
   - Eddy covariance towers: atmospheric CO2 flux measurement
   - Infrared cameras: visualize CO2 plumes (if concentration >1%)
   - Baseline and seasonal variability critical (biological soil respiration varies 10x)
5. SURFACE DEFORMATION MONITORING - Pressure-induced uplift/subsidence
   - InSAR (Interferometric Synthetic Aperture Radar): satellite-based, mm-scale precision
   - GPS benchmarks: permanent stations for ground truth
   - Tiltmeters: detect micro-deformation near injection well
   - Predicted uplift: 1-10 cm for typical projects (reservoir geomechanics dependent)
6. GEOCHEMICAL MONITORING - Formation fluid changes
   - Tracer injection: SF6, Kr, perfluorocarbons (detect breakthrough in obs wells)
   - Formation fluid sampling: brine chemistry evolution (mineral dissolution/precipitation)
   - Isotope analysis: δ13C to distinguish injected CO2 from natural sources
   - Reactive transport modeling: predict pH changes, mineral reactions
7. SEISMIC MONITORING - Induced seismicity detection
   - Seismograph network: 5-20 stations within 10 km radius
   - Detection threshold: magnitude -1.0 to -2.0 (microseismic)
   - Traffic light system: Green <M2, Yellow M2-3, Red >M3 (reduce/stop injection)
   - Induced seismicity rare for storage (vs. frequent for Class II disposal due to higher volumes/pressures)
8. VERIFICATION - Independent third-party certification
   - Annual mass balance: injected CO2 vs. storage capacity consumed
   - Plume position vs. model predictions (validation)
   - Well integrity: MIT results, annulus monitoring
   - Conformance with permit conditions and MVA plan
   - ISO 27916 or EPA MRR protocol for quantification
9. REPORTING - Regulatory and stakeholder communication
   - Quarterly reports to EPA/state: injection volumes, pressure, monitoring data
   - Annual monitoring report: comprehensive data summary, model updates
   - Public website: select monitoring data for transparency
   - Incident reports: within 24 hours for permit violations or anomalies
10. ADAPTIVE MANAGEMENT - Modify MVA based on results
    - Increase monitoring frequency if anomalies detected
    - Drill additional observation wells if plume deviates from prediction
    - Adjust injection rate/pressure to manage pressure buildup
    - AoR re-delineation every 5 years or after significant model updates
""",
            key_factors=[
                "4D seismic most expensive component ($5-15M per survey, every 1-5 years)",
                "Groundwater monitoring critical for regulatory compliance (quarterly)",
                "Downhole pressure/temperature monitoring continuous (real-time SCADA)",
                "Total MVA cost $2-5M/year during injection, $1-3M/year post-injection",
                "Third-party verification required for 45Q tax credit",
                "InSAR surface deformation monitoring cost-effective (satellite-based)",
                "Adaptive management flexibility built into Class VI permits"
            ],
            primary_authority=[
                "EPA Class VI Guidance on MVA Plans",
                "ISO 27916:2019 - Carbon Capture and Storage - Quantification and Verification",
                "DOE Best Practices for MVA of Geologic CO2 Storage (2012)"
            ],
            burden_holder="Well operator to implement MVA plan and demonstrate no leakage or groundwater impacts",
            adversary_position="MVA cannot detect all leakage pathways, false sense of security",
            counter_arguments=[
                "Multiple independent monitoring methods provide redundancy",
                "Detection sensitivity sufficient for early warning (before environmental impact)",
                "4D seismic proven to detect CO2 migration (Sleipner, Weyburn examples)",
                "Groundwater monitoring directly measures drinking water protection",
                "Adaptive management allows response to unexpected behavior",
                "Operational projects (ADM Decatur, Quest) show MVA effectiveness"
            ],
            resolution_strategy="Design MVA program with redundancy, detection thresholds based on model predictions with safety factors",
            entity_scope="All Class VI wells, large-scale CCS projects, enhanced monitoring for public acceptance",
            confidence=ConfidenceLevel.DEFENSIBLE
        )

        # Store doctrine trigger counts
        for key in doctrines:
            self.doctrine_triggers[key] = 0

        return doctrines

    def three_layer_response(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> tuple[str, List[str], ConfidenceLevel]:
        """TIE-pattern three-layer response: cache → semantic → deep"""
        start_time = datetime.now()
        triggered_doctrines = []

        # Layer 1: Doctrine cache scan
        query_lower = query.lower()
        for key, doctrine in self.doctrine_cache.items():
            if any(kw.lower() in query_lower for kw in doctrine.keywords):
                triggered_doctrines.append(key)
                self.doctrine_triggers[key] += 1

        # Layer 2: Semantic retrieval (simulated - would use vector search in production)
        if not triggered_doctrines:
            triggered_doctrines = list(self.doctrine_cache.keys())[:3]

        # Layer 3: Deep analysis synthesis
        response = self._synthesize_response(query, triggered_doctrines[:5], mode, zone)
        confidence = self._assess_confidence(triggered_doctrines, mode)

        latency = (datetime.now() - start_time).total_seconds() * 1000
        logger.info(f"Three-layer response: {len(triggered_doctrines)} doctrines, {latency:.1f}ms, confidence={confidence.value}")

        return response, triggered_doctrines, confidence

    def _synthesize_response(self, query: str, doctrine_keys: List[str], mode: ResponseMode, zone: AnalysisZone) -> str:
        """Synthesize multi-doctrine response"""
        if not doctrine_keys:
            return "Insufficient doctrine coverage for this CCUS query. Recommend consulting domain expert."

        primary = self.doctrine_cache[doctrine_keys[0]]

        if mode == ResponseMode.FAST:
            return f"{primary.conclusion_template}\n\nKey factors: {', '.join(primary.key_factors[:3])}"

        elif mode == ResponseMode.DEFENSE:
            parts = [
                f"ANALYSIS: {primary.topic}",
                f"\nCONCLUSION: {primary.conclusion_template}",
                f"\nREASONING:\n{primary.reasoning_framework[:500]}...",
                f"\nKEY FACTORS:\n" + "\n".join(f"  • {f}" for f in primary.key_factors[:5]),
                f"\nAUTHORITY: {'; '.join(primary.primary_authority)}",
                f"\nCONFIDENCE: {primary.confidence.value}"
            ]

            if len(doctrine_keys) > 1:
                parts.append(f"\nRELATED DOCTRINES: {', '.join(self.doctrine_cache[k].topic for k in doctrine_keys[1:3])}")

            return "\n".join(parts)

        else:  # MEMO mode
            parts = [
                f"MEMORANDUM: {primary.topic}",
                f"\nZONE: {zone.value}",
                f"\n{'='*80}",
                f"\nEXECUTIVE SUMMARY:\n{primary.conclusion_template}",
                f"\n\nDETAILED ANALYSIS:\n{primary.reasoning_framework}",
                f"\n\nKEY TECHNICAL FACTORS:",
            ]
            parts.extend(f"  {i+1}. {f}" for i, f in enumerate(primary.key_factors))

            parts.extend([
                f"\n\nPRIMARY AUTHORITY:",
                *[f"  • {a}" for a in primary.primary_authority],
                f"\n\nBURDEN OF PROOF: {primary.burden_holder}",
                f"\n\nADVERSARY POSITION: {primary.adversary_position}",
                f"\n\nCOUNTER-ARGUMENTS:",
                *[f"  • {c}" for c in primary.counter_arguments],
                f"\n\nRESOLUTION STRATEGY:\n{primary.resolution_strategy}",
                f"\n\nCONFIDENCE ASSESSMENT: {primary.confidence.value}",
                f"ENTITY SCOPE: {primary.entity_scope}"
            ])

            if len(doctrine_keys) > 1:
                parts.append(f"\n\nRELATED CONSIDERATIONS:")
                for key in doctrine_keys[1:3]:
                    doc = self.doctrine_cache[key]
                    parts.append(f"\n  • {doc.topic}: {doc.conclusion_template[:150]}...")

            return "\n".join(parts)

    def _assess_confidence(self, triggered_doctrines: List[str], mode: ResponseMode) -> ConfidenceLevel:
        """Assess confidence based on doctrine coverage and mode"""
        if len(triggered_doctrines) == 0:
            return ConfidenceLevel.HIGH_RISK
        elif len(triggered_doctrines) == 1:
            return ConfidenceLevel.DISCLOSURE
        elif len(triggered_doctrines) <= 3:
            return ConfidenceLevel.AGGRESSIVE
        else:
            return ConfidenceLevel.DEFENSIBLE

    def generate_determinism_hash(self, query: str, response: str, doctrines: List[str]) -> str:
        """Generate SHA-256 hash for response reproducibility"""
        content = f"{query}|{response}|{','.join(sorted(doctrines))}"
        return hashlib.sha256(content.encode()).hexdigest()

    def log_telemetry(self, entry: TelemetryEntry):
        """Store telemetry entry"""
        self.telemetry_log.append(entry)
        if len(self.telemetry_log) > 10000:
            self.telemetry_log = self.telemetry_log[-5000:]

    def get_coverage_metrics(self) -> CoverageMetrics:
        """Analyze doctrine coverage"""
        triggered = [k for k, v in self.doctrine_triggers.items() if v > 0]
        missed = [k for k, v in self.doctrine_triggers.items() if v == 0]

        return CoverageMetrics(
            total_doctrines=len(self.doctrine_cache),
            triggered_count=len(triggered),
            missed_doctrines=missed,
            epistemic_gaps=[f"Limited coverage in {k}" for k in missed[:5]]
        )

    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health status"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        avg_latency = self.total_latency_ms / max(self.query_count, 1)
        cache_hit_rate = self.cache_hits / max(self.query_count, 1)

        return {
            "status": "operational",
            "version": self.version,
            "port": self.port,
            "doctrine_count": len(self.doctrine_cache),
            "cache_size": len(self.doctrine_cache),
            "uptime_seconds": uptime,
            "total_queries": self.query_count,
            "avg_latency_ms": round(avg_latency, 2),
            "cache_hit_rate": round(cache_hit_rate, 3),
            "coverage": {
                "triggered_doctrines": len([v for v in self.doctrine_triggers.values() if v > 0]),
                "total_doctrines": len(self.doctrine_cache)
            }
        }

# FastAPI application
app = FastAPI(title="ENRG10 Carbon Capture Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = ENRG10Engine()

@app.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint with three-layer TIE response"""
    start_time = datetime.now()

    try:
        response_text, doctrines_applied, confidence = engine.three_layer_response(
            request.query,
            request.mode,
            request.zone
        )

        latency_ms = (datetime.now() - start_time).total_seconds() * 1000
        determinism_hash = engine.generate_determinism_hash(request.query, response_text, doctrines_applied)

        engine.query_count += 1
        engine.total_latency_ms += latency_ms
        if doctrines_applied:
            engine.cache_hits += 1

        # Log telemetry
        telemetry = TelemetryEntry(
            query_id=determinism_hash[:12],
            timestamp=datetime.now(),
            query_text=request.query,
            mode=request.mode,
            latency_ms=latency_ms,
            cache_hit=len(doctrines_applied) > 0,
            doctrines_triggered=doctrines_applied,
            confidence=confidence
        )
        engine.log_telemetry(telemetry)

        logger.info(f"Query processed: {len(doctrines_applied)} doctrines, {latency_ms:.1f}ms")

        citations = None
        if request.include_citations and doctrines_applied:
            primary_doctrine = engine.doctrine_cache[doctrines_applied[0]]
            citations = primary_doctrine.primary_authority

        return QueryResponse(
            answer=response_text,
            mode=request.mode,
            confidence=confidence,
            doctrines_applied=doctrines_applied,
            citations=citations,
            latency_ms=round(latency_ms, 2),
            determinism_hash=determinism_hash
        )

    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    health_data = engine.health_check()
    return HealthResponse(**health_data)

@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrines"""
    return {
        "total": len(engine.doctrine_cache),
        "doctrines": [
            {
                "key": key,
                "topic": doc.topic,
                "keywords": doc.keywords,
                "confidence": doc.confidence.value,
                "trigger_count": engine.doctrine_triggers.get(key, 0)
            }
            for key, doc in engine.doctrine_cache.items()
        ]
    }

@app.get("/coverage")
async def coverage_analysis():
    """Doctrine coverage metrics"""
    metrics = engine.get_coverage_metrics()
    return {
        "total_doctrines": metrics.total_doctrines,
        "triggered_count": metrics.triggered_count,
        "coverage_rate": round(metrics.triggered_count / metrics.total_doctrines, 3),
        "missed_doctrines": metrics.missed_doctrines,
        "epistemic_gaps": metrics.epistemic_gaps
    }

@app.get("/telemetry")
async def telemetry_summary():
    """Recent telemetry data"""
    recent = engine.telemetry_log[-100:]
    return {
        "total_entries": len(engine.telemetry_log),
        "recent_count": len(recent),
        "recent_queries": [
            {
                "query_id": t.query_id,
                "timestamp": t.timestamp.isoformat(),
                "mode": t.mode.value,
                "latency_ms": round(t.latency_ms, 2),
                "cache_hit": t.cache_hit,
                "doctrines_count": len(t.doctrines_triggered),
                "confidence": t.confidence.value
            }
            for t in recent[-20:]
        ]
    }

if __name__ == "__main__":
    logger.info(f"Starting ENRG10 Carbon Capture Engine v{engine.version} on port {engine.port}")
    uvicorn.run(app, host="0.0.0.0", port=engine.port, log_level="info")
