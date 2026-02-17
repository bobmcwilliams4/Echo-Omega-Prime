"""
AUTO05 - Automotive HVAC & Climate Control Systems Intelligence Engine
TIE Gold Standard Implementation

Port: 9065
Domain: Automotive air conditioning, heating, climate control systems
Authority: ASE A7 Certification standards + SAE J639 + EPA 608/609
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from enum import Enum

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# Pydantic Models
class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = None

class DoctrineMatch(BaseModel):
    topic: str
    confidence: float
    reasoning: str
    authority: List[str]

class QueryResponse(BaseModel):
    query: str
    response: str
    mode: ResponseMode
    doctrine_matches: List[DoctrineMatch]
    confidence_level: ConfidenceLevel
    response_time_ms: float
    determinism_hash: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    avg_response_time_ms: float
    cache_hit_rate: float


# Doctrine Block Class
class DoctrineBlock:
    def __init__(self, topic: str, keywords: List[str], conclusion_template: List[str],
                 reasoning_framework: str, key_factors: List[str], primary_authority: List[str],
                 confidence: float, confidence_stratification: ConfidenceLevel):
        self.topic = topic
        self.keywords = [k.lower() for k in keywords]
        self.conclusion_template = conclusion_template
        self.reasoning_framework = reasoning_framework
        self.key_factors = key_factors
        self.primary_authority = primary_authority
        self.confidence = confidence
        self.confidence_stratification = confidence_stratification

# Doctrine 1: Refrigeration Cycle
DOCTRINE_REFRIGERATION_CYCLE = DoctrineBlock(
    topic="Refrigeration Cycle Fundamentals",
    keywords=["refrigeration", "cycle", "thermodynamics", "r-134a", "r-1234yf", "heat transfer"],
    conclusion_template=[
        "The automotive refrigeration cycle operates on vapor-compression principles with four key stages.",
        "Heat absorption occurs at the evaporator (low pressure/temperature), heat rejection at the condenser.",
        "Refrigerant state changes enable heat transfer from cabin to ambient environment."
    ],
    reasoning_framework="""
Vapor-compression cycle: Compression → Condensation → Expansion → Evaporation
- Compressor: Raises pressure/temp (30→250 psi, 40→180°F, 3-5 HP)
- Condenser: Heat rejection 15-20k BTU/hr, vapor→liquid
- Expansion: Pressure drop via TXV/orifice, temp drops to 32-40°F
- Evaporator: Heat absorption 12-18k BTU/hr, liquid→vapor
R-134a vs R-1234yf: GWP 1430 vs 4, similar pressures, different oils""",
    key_factors=[
        "High-side pressure 200-300 psi, low-side 25-35 psi (normal)",
        "Superheat indicates proper charge (8-12°F)",
        "R-1234yf is mildly flammable (A2L class)",
        "COP typically 2.5-3.5 for automotive A/C"
    ],
    primary_authority=["SAE J639", "ASE A7", "EPA Section 609"],
    confidence=0.95,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE
)


# Doctrine 2: Compressor Types
DOCTRINE_COMPRESSOR_TYPES = DoctrineBlock(
    topic="Compressor Technology & Diagnosis",
    keywords=["compressor", "scroll", "variable displacement", "electric", "clutch"],
    conclusion_template=[
        "Compressor type determines control strategy and efficiency.",
        "Variable displacement compressors modulate without clutch cycling.",
        "Electric compressors enable heat pump operation in EVs."
    ],
    reasoning_framework="""
Types: Fixed piston (clutch cycling), Variable (wobble plate), Scroll (smooth), Electric (HV)
- Fixed: 80-180 cc/rev, cycles 2-6/min, clutch coil 2.5-4.5A
- Variable: Internal control valve, no cycling, Sanden SD7/Denso 10S
- Electric: 300-800V, 2-7 kW, 0-8000 RPM, enables heat pump mode
Oil: PAG for R-134a, POE for R-1234yf, POE ND-11 for hybrid (non-conductive)""",
    key_factors=[
        "Clutch gap 0.014-0.030 inch affects engagement",
        "Electric compressors need HV isolation test >500 MΩ",
        "Variable displacement eliminates cycling wear",
        "Oil type MUST match refrigerant"
    ],
    primary_authority=["SAE J2765", "ASE A7"],
    confidence=0.93,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE
)

# Doctrine 3: Condenser Design
DOCTRINE_CONDENSER = DoctrineBlock(
    topic="Condenser Design & Airflow",
    keywords=["condenser", "parallel flow", "airflow", "fan", "heat rejection"],
    conclusion_template=[
        "Parallel-flow design maximizes heat transfer efficiency.",
        "Adequate airflow (2000-4000 CFM) is critical for capacity.",
        "Blocked condenser causes high-pressure cutout."
    ],
    reasoning_framework="""
Parallel-flow multiport tubes (0.8-2.0mm ports), 2-4 passes, 15-25k BTU/hr
Mounted ahead of radiator, requires ram air + electric fans
Fan control: A/C pressure switch (225-275 psi) + coolant temp
Blocked condenser: High-side >350 psi, poor cooling at idle
Subcool condenser: Extra passes, 5-15°F subcooling, 5-8% capacity gain""",
    key_factors=[
        "Parallel-flow 20-30% more efficient than tube-fin",
        "Fans must run when A/C on (especially idle/low speed)",
        "Subcooling 5-15°F indicates adequate capacity",
        "Blocked/dirty condenser: high-side +50-100 psi"
    ],
    primary_authority=["SAE J2765", "ASE A7"],
    confidence=0.92,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE
)

# Doctrine 4: Evaporator Design
DOCTRINE_EVAPORATOR = DoctrineBlock(
    topic="Evaporator Design & Icing Prevention",
    keywords=["evaporator", "icing", "superheat", "vent temperature"],
    conclusion_template=[
        "Evaporator must stay above 32°F to prevent icing.",
        "Superheat 8-12°F ensures complete evaporation.",
        "Vent temperature 38-48°F indicates proper operation."
    ],
    reasoning_framework="""
Plate-fin aluminum, 200-300mm × 200-250mm × 40-60mm, 12-18k BTU/hr
Temp control: 35-45°F target (above freezing, below dew point)
Icing causes: Low charge, restricted airflow, TXV stuck open, dirty cabin filter
Prevention: TXV maintains 8-12°F superheat, CCOT cycles at 23-28 psi, EXV real-time control
Condensate: 1-3 pints/hr drains via tube""",
    key_factors=[
        "Vent temp 38-48°F is normal",
        "Low charge CAUSES icing (counterintuitive)",
        "Dirty cabin filter restricts airflow → icing",
        "Superheat 8-12°F prevents ice while maximizing cooling",
        "Musty odor = microbial growth (needs cleaning)"
    ],
    primary_authority=["SAE J2765", "ASE A7"],
    confidence=0.94,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE
)

# Doctrine 5: Expansion Devices
DOCTRINE_EXPANSION = DoctrineBlock(
    topic="Expansion Devices - TXV vs. Orifice Tube",
    keywords=["txv", "expansion valve", "orifice tube", "superheat"],
    conclusion_template=[
        "TXV modulates flow based on superheat; orifice tube uses fixed restriction.",
        "TXV systems use receiver-drier, orifice tube systems use accumulator.",
        "System type determines diagnostic approach."
    ],
    reasoning_framework="""
TXV: Variable orifice, superheat-controlled (8-12°F target), receiver-drier, stable performance
Orifice Tube: Fixed 0.047-0.072" orifice, compressor cycles 23-28 psi, accumulator
EXV: Stepper motor ECU-controlled, real-time temp sensors, multi-zone capable
TXV failures: Stuck open (low superheat, icing), stuck closed (high superheat)
Orifice failures: Clogged (low-side low, high-side high), oversized (pressures equalize)""",
    key_factors=[
        "TXV = receiver-drier, Orifice = accumulator",
        "Superheat test critical for TXV diagnosis",
        "Orifice tube can clog with debris",
        "Low-pressure switch prevents icing in orifice systems"
    ],
    primary_authority=["ASE A7", "MACS Training", "SAE J639"],
    confidence=0.95,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE
)


# Doctrine 6: Receiver-Drier vs Accumulator
DOCTRINE_RECEIVER_ACCUMULATOR = DoctrineBlock(
    topic="Receiver-Drier vs. Accumulator Function",
    keywords=["receiver-drier", "accumulator", "desiccant", "moisture"],
    conclusion_template=[
        "Receiver-driers store liquid on high side (TXV systems).",
        "Accumulators separate vapor/liquid on low side (orifice systems).",
        "Both contain desiccant and filters, replace when system opened."
    ],
    reasoning_framework="""
Receiver-Drier: High-side, TXV systems, ensures 100% liquid to TXV, 30-60g desiccant
Accumulator: Low-side, orifice systems, prevents liquid slugging, 1-2L capacity, U-tube outlet
Desiccant: XH-7/XH-9, absorbs 8-12% weight in water (3-5g capacity)
Replace: System contamination, open >24hrs, major component replacement
Moisture consequences: Acid formation, copper plating, TXV/orifice icing""",
    key_factors=[
        "Receiver = high-side TXV, Accumulator = low-side orifice",
        "Sight glass (receiver): Clear=good, bubbles=low charge",
        "Frost on accumulator normal, frost on receiver = restriction",
        "Replace when system opened (desiccant saturates)"
    ],
    primary_authority=["ASE A7", "MACS Training"],
    confidence=0.93,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE
)

# Doctrine 7: Pressure Diagnosis
DOCTRINE_PRESSURE = DoctrineBlock(
    topic="A/C System Pressure Diagnosis",
    keywords=["pressure", "gauge", "high side", "low side", "diagnosis"],
    conclusion_template=[
        "Pressure patterns reveal charge status and component failures.",
        "Normal: Low 25-35 psi, High 200-250 psi (75-85°F ambient).",
        "Abnormal patterns indicate specific faults."
    ],
    reasoning_framework="""
Normal: Low 25-35 psi, High 200-250 psi (pressure ratio 6:1 to 10:1)
Both low: Undercharge (most common leak scenario)
Both high: Overcharge or poor condenser airflow
Low-side low + high-side high: Restriction (clogged orifice, TXV, line)
Low-side high + high-side low: Compressor failure or expansion device stuck open
Both equal (running): Compressor not pumping
Static pressure (off): Equalizes to ambient temp (65°F=60-70psi, 95°F=120-130psi)
Subcooling (TXV): 10-20°F, Superheat (orifice): 8-15°F""",
    key_factors=[
        "High-side increases with ambient temp",
        "Both low = undercharge, both high = overcharge/airflow",
        "Restriction: Low-side low + high-side high",
        "Static pressure should equalize in 1-2 min when off"
    ],
    primary_authority=["ASE A7", "MACS Training", "SAE J639"],
    confidence=0.96,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE
)

# Doctrine 8: Refrigerant Recovery
DOCTRINE_RECOVERY = DoctrineBlock(
    topic="Refrigerant Recovery & EPA 609 Compliance",
    keywords=["recovery", "recycling", "epa", "section 609", "certification"],
    conclusion_template=[
        "EPA 609 mandates certified equipment and technicians.",
        "Refrigerant must be recovered before system opening; venting illegal ($37,500 fine).",
        "R-134a and R-1234yf require separate equipment."
    ],
    reasoning_framework="""
Certification: Technicians + equipment (SAE J2788 R-134a, SAE J2843 R-1234yf)
Recovery: Identifier first, evacuate to 0-5 psi, 5+ min, record quantity
Recycling: R/R machine filters/dries, 98% purity (SAE J2788)
R-1234yf: Mildly flammable (A2L), unique fittings (8mm/14mm), dedicated equipment
Cross-contamination: NEVER mix refrigerants, separate machines/hoses/tanks
Vacuum test: 28-29" Hg for 30-45 min, rise <0.5" = leak-free
Charge: By weight (most accurate), ±0.5 oz critical for R-1234yf""",
    key_factors=[
        "Venting refrigerant = $37,500 fine per violation",
        "R-1234yf mildly flammable, needs safety precautions",
        "Separate recovery equipment (NO mixing R-134a/R-1234yf)",
        "Vacuum hold 30-45 min confirms system integrity"
    ],
    primary_authority=["EPA Section 609", "SAE J2788", "SAE J2843", "ASE A7"],
    confidence=0.97,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE
)

# Doctrine 9: Cabin Air Filter
DOCTRINE_CABIN_FILTER = DoctrineBlock(
    topic="Cabin Air Filtration & Air Quality",
    keywords=["cabin filter", "hvac filter", "pollen", "activated carbon"],
    conclusion_template=[
        "Cabin air filters remove particulates, pollen, and odors.",
        "Clogged filters reduce airflow and strain blower motors.",
        "Replace every 12,000-15,000 miles or annually."
    ],
    reasoning_framework="""
Types: Particulate (90-95% >3 micron), Activated carbon (+ odor absorption), HEPA (99.97% >0.3 micron)
Location: Behind glove box (most common), under dash, under hood
Clogged symptoms: Reduced airflow, weak defrost, musty odor, blower noise, evaporator icing
Replacement: 12-15k miles or 1 year
Installation: Note airflow direction arrow (critical)
Advanced: VOC sensor, PM2.5 sensor, auto recirculation, air ionizer""",
    key_factors=[
        "Critical maintenance 12-15k mile interval",
        "Clogged filter causes blower motor strain/failure",
        "Activated carbon removes odors + particulates",
        "Airflow direction arrow must face correctly",
        "Musty odor = clogged filter or evaporator growth"
    ],
    primary_authority=["OEM Service Schedules", "ASE A7", "SAE J1980"],
    confidence=0.90,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE
)


# Doctrine 10: Heater Core
DOCTRINE_HEATER_CORE = DoctrineBlock(
    topic="Heater Core Operation & Diagnosis",
    keywords=["heater core", "coolant", "heat", "blend door"],
    conclusion_template=[
        "Heater core transfers engine coolant heat to cabin air.",
        "Blend door modulates air mix for temperature control.",
        "Failure causes coolant leaks, poor heat, sweet odor."
    ],
    reasoning_framework="""
Miniature radiator 6-8" × 6-8", 190-210°F coolant, 15-25k BTU/hr heat transfer
Flow control: Full-flow (always on, blend door only) or flow-control valve (older/luxury)
Blend door: Cable/vacuum (manual) or electric actuator (ATC)
No heat causes: Low coolant/air pocket, thermostat stuck open, clogged core, blend door stuck, valve closed
Leak symptoms: Sweet smell, coolant on passenger floor, foggy windshield, low coolant
Replacement: Labor-intensive (dash removal, 6-12 hrs)""",
    key_factors=[
        "Low coolant causes air pockets = no heat",
        "Leak: sweet odor, foggy windshield, floor puddle",
        "Clogged core: inlet hot, outlet cool",
        "Dash removal typically required for replacement"
    ],
    primary_authority=["ASE A7", "OEM Service Procedures"],
    confidence=0.92,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE
)

# Doctrine 11: Blend Door Actuators
DOCTRINE_ACTUATORS = DoctrineBlock(
    topic="Blend Door Actuators & Mode Door Control",
    keywords=["actuator", "blend door", "mode door", "stepper motor"],
    conclusion_template=[
        "Electric actuators control air delivery and temperature.",
        "Failure causes clicking noises, incorrect distribution.",
        "Scan tool calibration required after replacement."
    ],
    reasoning_framework="""
Types: Blend (temperature), Mode (distribution), Recirculation (fresh/recirc)
Construction: DC motor, gear reduction 50-100:1, position sensor (pot or hall-effect)
Failure: Clicking noise (stripped gears), incorrect temp/mode, intermittent
Diagnosis: Scan tool displays position, command test mode
Replacement: Behind dash (1-3 hrs labor), calibration REQUIRED (actuator learns full range)
Calibration: Scan tool command, actuator drives min→max, stores endpoints""",
    key_factors=[
        "Clicking noise = stripped gears",
        "Scan tool can command actuators for testing",
        "Calibration mandatory after replacement",
        "Behind-dash location = labor-intensive"
    ],
    primary_authority=["ASE A7", "OEM Service Procedures"],
    confidence=0.91,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE
)

# Doctrine 12: Automatic Temperature Control
DOCTRINE_ATC = DoctrineBlock(
    topic="Automatic Climate Control Systems",
    keywords=["atc", "automatic", "climate control", "sensors", "dual zone"],
    conclusion_template=[
        "ATC maintains set temperature via sensor feedback loops.",
        "Sensors: in-cabin, ambient, sunload, evaporator temperature.",
        "System modulates blower, blend doors, compressor operation."
    ],
    reasoning_framework="""
Sensors: In-cabin (thermistor + fan), ambient (bumper/mirror), sunload (photodiode), evaporator temp
HVAC module logic: Inputs → Outputs (blower PWM, blend/mode/recirc actuators, compressor, fans)
Heating mode: Wait coolant >100°F, blend hot, floor mode, A/C off (unless defrost)
Cooling mode: A/C on, blend variable, vent/bi-level, high blower initially
Sunload compensation: Increase blower, shift blend cooler
Dual-zone: Independent driver/passenger actuators, shared evaporator/heater core""",
    key_factors=[
        "In-cabin sensor fan draws air sample (failure = poor control)",
        "Sunload sensor compensates solar heat gain",
        "System delays blower until coolant >100°F (winter)",
        "Scan tool displays all sensor readings + actuator commands"
    ],
    primary_authority=["ASE A7", "OEM Service Training"],
    confidence=0.94,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE
)

# Doctrine 13: Heat Pump for EVs
DOCTRINE_HEAT_PUMP = DoctrineBlock(
    topic="Heat Pump Systems for Electric Vehicles",
    keywords=["heat pump", "ev", "electric vehicle", "reverse cycle", "cop"],
    conclusion_template=[
        "Heat pumps reverse refrigeration cycle for cabin heating.",
        "COP 2-4 vs. 1 for resistive heaters (improves EV range).",
        "Four-way valve reverses flow; outdoor coil becomes evaporator."
    ],
    reasoning_framework="""
Why: EVs lack engine waste heat, must generate heat electrically
Resistive: COP 1.0 (1kW in = 1kW heat), Heat pump: COP 2.5-4.0 (1kW in = 2.5-4kW heat)
Cooling mode: Compressor→Outdoor(condenser)→Expansion→Indoor(evaporator)→Compressor
Heating mode: Four-way valve reverses → Compressor→Indoor(condenser)→Expansion→Outdoor(evaporator)→Compressor
COP vs temp: 45°F=3.5, 32°F=2.5, 0°F=1.5-2.0, <-10°F <1.5 (resistive better)
Defrost cycle: Outdoor coil ices in heat mode (25-45°F + humidity), reverse briefly to melt ice
Supplemental PTC heater: 3-7kW for extreme cold, rapid heating, defrost""",
    key_factors=[
        "Heat pump reduces heating energy by 50-75% vs. resistive",
        "Four-way valve switches cool/heat modes",
        "COP decreases as outdoor temp drops",
        "Defrost cycle interrupts cabin heating (PTC supplements)",
        "Range impact critical in cold climates"
    ],
    primary_authority=["SAE J2765", "OEM EV Service Training", "ASHRAE"],
    confidence=0.93,
    confidence_stratification=ConfidenceLevel.AGGRESSIVE
)

# Doctrine 14: Leak Detection
DOCTRINE_LEAK_DETECTION = DoctrineBlock(
    topic="A/C System Leak Detection Methods",
    keywords=["leak detection", "uv dye", "electronic sniffer", "nitrogen"],
    conclusion_template=[
        "Leaks reduce capacity and must be repaired before recharging.",
        "Methods: UV dye (pinpoints location), electronic sniffer (fast screening), nitrogen test (confirms repair).",
        "EPA requires leak repair if system loses >1.5 oz/year."
    ],
    reasoning_framework="""
Visual: Oil residue at leak points (compressor seal, fittings, condenser, evaporator, service ports)
Electronic sniffer: Heated diode/IR sensor, 0.1-0.5 oz/yr sensitivity, audible/visual alarm
UV dye: Fluorescent dye circulates, deposits at leak, UV lamp illuminates (yellow-green glow)
Nitrogen test: Evacuate, pressurize 150-250 psi N2 + trace refrigerant, use sniffer to locate
Bubble test: Soapy water on suspected areas, pressurize with nitrogen, bubbles at leak
Repair: O-rings (most common), Schrader cores, compressor seal, condenser/evaporator replacement
Post-repair: Vacuum 28-29" Hg for 30-45 min, rise <0.5" = leak-free
EPA: Repair required if >1.5 oz/yr loss""",
    key_factors=[
        "Electronic sniffer = fast screening, needs refrigerant in system",
        "UV dye = pinpoints exact location (1-2 weeks circulation)",
        "Nitrogen test = confirms repair before recharge",
        "O-ring leaks most common (hose fittings)",
        "EPA: Leak repair required if >1.5 oz/year"
    ],
    primary_authority=["EPA Section 609", "ASE A7", "MACS Training", "SAE J2791"],
    confidence=0.94,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE
)

# Build doctrine cache
DOCTRINE_CACHE = [
    DOCTRINE_REFRIGERATION_CYCLE,
    DOCTRINE_COMPRESSOR_TYPES,
    DOCTRINE_CONDENSER,
    DOCTRINE_EVAPORATOR,
    DOCTRINE_EXPANSION,
    DOCTRINE_RECEIVER_ACCUMULATOR,
    DOCTRINE_PRESSURE,
    DOCTRINE_RECOVERY,
    DOCTRINE_CABIN_FILTER,
    DOCTRINE_HEATER_CORE,
    DOCTRINE_ACTUATORS,
    DOCTRINE_ATC,
    DOCTRINE_HEAT_PUMP,
    DOCTRINE_LEAK_DETECTION,
]


# Telemetry Collector
class TelemetryCollector:
    def __init__(self):
        self.start_time = time.time()
        self.total_queries = 0
        self.total_response_time = 0.0
        self.cache_hits = 0
        self.cache_misses = 0
        self.error_count = 0

    def record_query(self, response_time_ms: float, cache_hit: bool, error: bool = False):
        self.total_queries += 1
        self.total_response_time += response_time_ms
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        if error:
            self.error_count += 1

    def get_avg_response_time(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return self.total_response_time / self.total_queries

    def get_cache_hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return self.cache_hits / total

    def get_uptime(self) -> float:
        return time.time() - self.start_time

# HVAC Intelligence Engine
class HVACIntelligenceEngine:
    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.telemetry = TelemetryCollector()
        logger.info(f"AUTO05 Engine initialized with {len(self.doctrines)} doctrine blocks")

    def three_layer_response(self, query: str, mode: ResponseMode) -> QueryResponse:
        start_time = time.time()
        matches = self._search_doctrine_cache(query)

        if matches:
            response_text = self._format_response(matches, mode)
            cache_hit = True
        else:
            response_text = self._deep_analysis(query, mode)
            cache_hit = False

        response_time_ms = (time.time() - start_time) * 1000
        determinism_hash = self._compute_hash(query + response_text)
        confidence_level = self._assess_confidence(matches)

        doctrine_matches = [
            DoctrineMatch(
                topic=m.topic,
                confidence=m.confidence,
                reasoning=m.reasoning_framework[:200] + "...",
                authority=m.primary_authority
            )
            for m in matches[:3]
        ]

        self.telemetry.record_query(response_time_ms, cache_hit)

        return QueryResponse(
            query=query,
            response=response_text,
            mode=mode,
            doctrine_matches=doctrine_matches,
            confidence_level=confidence_level,
            response_time_ms=round(response_time_ms, 2),
            determinism_hash=determinism_hash,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

    def _search_doctrine_cache(self, query: str) -> List[DoctrineBlock]:
        query_lower = query.lower()
        scored_doctrines = []
        for doctrine in self.doctrines:
            keyword_hits = sum(1 for kw in doctrine.keywords if kw in query_lower)
            if keyword_hits > 0:
                score = (keyword_hits / len(doctrine.keywords)) * doctrine.confidence
                scored_doctrines.append((score, doctrine))
        scored_doctrines.sort(key=lambda x: x[0], reverse=True)
        return [d for score, d in scored_doctrines if score > 0.3]

    def _deep_analysis(self, query: str, mode: ResponseMode) -> str:
        return f"""Deep analysis mode for: "{query}"

This query requires synthesis beyond pre-compiled doctrines. Recommend:
- Consult ASE A7 certification materials
- Review OEM service manual for specific vehicle
- Use scan tool diagnostics for system data
- Verify refrigerant type and system configuration

Provide additional context (make/model/year, system type, symptoms) for targeted guidance."""

    def _format_response(self, matches: List[DoctrineBlock], mode: ResponseMode) -> str:
        if not matches:
            return "No doctrine match found."
        
        primary = matches[0]

        if mode == ResponseMode.FAST:
            response = "\n".join(primary.conclusion_template)
            response += f"\n\nKey Factors:\n"
            response += "\n".join(f"• {kf}" for kf in primary.key_factors[:5])
            return response

        elif mode == ResponseMode.DEFENSE:
            response = f"TOPIC: {primary.topic}\n\n"
            response += "CONCLUSION:\n" + "\n".join(primary.conclusion_template)
            response += f"\n\nREASONING:\n{primary.reasoning_framework[:800]}"
            response += f"\n\nAUTHORITY:\n" + "\n".join(f"• {a}" for a in primary.primary_authority)
            response += f"\n\nCONFIDENCE: {primary.confidence_stratification.value}"
            return response

        else:  # MEMO
            response = f"# {primary.topic}\n\n## Executive Summary\n"
            response += "\n".join(primary.conclusion_template)
            response += f"\n\n## Technical Analysis\n{primary.reasoning_framework}"
            response += f"\n\n## Key Factors\n" + "\n".join(f"{i+1}. {kf}" for i, kf in enumerate(primary.key_factors))
            response += f"\n\n## Authority\n" + "\n".join(f"• {a}" for a in primary.primary_authority)
            if len(matches) > 1:
                response += f"\n\n## Related Topics\n" + "\n".join(f"• {m.topic}" for m in matches[1:4])
            return response

    def _assess_confidence(self, matches: List[DoctrineBlock]) -> ConfidenceLevel:
        if not matches:
            return ConfidenceLevel.DISCLOSURE
        return matches[0].confidence_stratification

    def _compute_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()[:16]


# FastAPI Application
app = FastAPI(
    title="AUTO05 - Automotive HVAC Intelligence Engine",
    version="1.0.0",
    description="TIE Gold Standard engine for automotive HVAC & climate control systems"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = HVACIntelligenceEngine()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        port=9065,
        doctrines_loaded=len(engine.doctrines),
        uptime_seconds=round(engine.telemetry.get_uptime(), 2),
        total_queries=engine.telemetry.total_queries,
        avg_response_time_ms=round(engine.telemetry.get_avg_response_time(), 2),
        cache_hit_rate=round(engine.telemetry.get_cache_hit_rate(), 4)
    )

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        logger.info(f"Query received: {request.query[:100]}... (mode={request.mode})")
        response = engine.three_layer_response(request.query, request.mode)
        logger.info(f"Query processed in {response.response_time_ms}ms")
        return response
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        engine.telemetry.record_query(0, False, error=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/doctrines")
async def list_doctrines():
    return {
        "total": len(engine.doctrines),
        "topics": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence,
                "authority": d.primary_authority
            }
            for d in engine.doctrines
        ]
    }

@app.get("/")
async def root():
    return {
        "engine": "AUTO05 - Automotive HVAC & Climate Control Intelligence",
        "version": "1.0.0",
        "port": 9065,
        "status": "operational",
        "doctrines": len(engine.doctrines),
        "endpoints": {
            "health": "/health",
            "query": "/query (POST)",
            "doctrines": "/doctrines"
        }
    }

if __name__ == "__main__":
    logger.info("AUTO05 - Automotive HVAC Intelligence Engine starting on port 9065")
    uvicorn.run(app, host="0.0.0.0", port=9065, log_level="info")
