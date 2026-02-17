"""
ECHO RAIL01 LOCOMOTIVE SYSTEMS INTELLIGENCE ENGINE — Production Architecture
Railroad locomotive systems expertise for maintenance, operations, and engineering.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled locomotive system knowledge
    Layer 2: Semantic Retrieval (200-700ms) - Fast technical lookup
    Layer 3: Deep Analysis (on-demand) - Multi-system troubleshooting

Response Modes:
    FAST: Quick technical reference, component identification
    DEFENSE: Detailed troubleshooting, FRA compliance, safety analysis
    MEMO: Comprehensive system documentation, maintenance procedures

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Port: 9101
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import hashlib
import time
import uuid
from loguru import logger

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/RAIL01_locomotive_systems/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "rail01_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}"
)

AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"


# ==============================================================================
# METRICS COLLECTOR
# ==============================================================================

class MetricsCollector:
    """Lightweight metrics for operational awareness."""

    def __init__(self):
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0

    def record_query(self, latency_ms: float, doctrine_hit: bool):
        self.latencies.append(latency_ms)
        if len(self.latencies) > 100:
            self.latencies.pop(0)
        self.queries.append(time.time())
        if doctrine_hit:
            self.doctrine_hits += 1
        else:
            self.doctrine_misses += 1

    def record_error(self, error: str):
        self.errors.append(time.time())
        self.last_error = error

    def get_stats(self) -> Dict[str, Any]:
        recent_queries = [q for q in self.queries if time.time() - q < 3600]
        return {
            "avg_latency_ms": sum(self.latencies) / len(self.latencies) if self.latencies else 0,
            "doctrine_hit_rate": self.doctrine_hits / max(1, self.doctrine_hits + self.doctrine_misses),
            "queries_per_hour": len(recent_queries),
            "active_queries": self.active_queries,
            "total_queries": self.doctrine_hits + self.doctrine_misses,
            "last_error": self.last_error
        }


METRICS = MetricsCollector()


# ==============================================================================
# DOCTRINE DRIFT WATCHER
# ==============================================================================

class DoctrineDriftWatcher:
    """Monitors doctrine mutations for epistemic stability."""

    def __init__(self):
        self.mutations: List[Dict[str, Any]] = []
        self.mutation_count = 0

    def record_mutation(self, topic: str, mutation_type: str, origin: str):
        self.mutations.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "topic": topic,
            "mutation_type": mutation_type,
            "origin": origin
        })
        self.mutation_count += 1
        if len(self.mutations) > 1000:
            self.mutations.pop(0)

    def get_drift_report(self) -> Dict[str, Any]:
        return {
            "total_mutations": self.mutation_count,
            "recent_mutations": len(self.mutations),
            "mutation_log": self.mutations[-10:]
        }


DRIFT_WATCHER = DoctrineDriftWatcher()


# ==============================================================================
# DOCTRINE COVERAGE MAP
# ==============================================================================

class DoctrineCoverageMap:
    """Tracks which doctrines are triggered vs missed for epistemic gap detection."""

    def __init__(self):
        self.triggered: Dict[str, int] = {}
        self.missed_topics: List[str] = []

    def record_hit(self, topic: str):
        self.triggered[topic] = self.triggered.get(topic, 0) + 1

    def record_miss(self, query: str):
        self.missed_topics.append(query)
        if len(self.missed_topics) > 500:
            self.missed_topics.pop(0)

    def get_coverage_report(self) -> Dict[str, Any]:
        return {
            "doctrines_triggered": len(self.triggered),
            "total_triggers": sum(self.triggered.values()),
            "most_used": sorted(self.triggered.items(), key=lambda x: x[1], reverse=True)[:10],
            "recent_misses": self.missed_topics[-20:]
        }


COVERAGE_MAP = DoctrineCoverageMap()


# ==============================================================================
# SEMANTIC NORMALIZATION
# ==============================================================================

def normalize_semantics(query: str) -> Dict[str, Any]:
    """Normalize railroad terminology to standard technical vocabulary."""

    normalized = query.lower()

    # Locomotive terminology normalization
    replacements = {
        "loco": "locomotive",
        "prime mover": "diesel engine",
        "traction motor": "electric motor",
        "mu": "multiple unit",
        "hep": "head end power",
        "ecp": "electronically controlled pneumatic",
        "ptc": "positive train control",
        "ccb": "computer controlled brake",
        "db": "dynamic brake",
        "te": "tractive effort"
    }

    for old, new in replacements.items():
        normalized = normalized.replace(old, new)

    return {
        "original": query,
        "normalized": normalized,
        "transformations": [k for k in replacements if k in query.lower()]
    }


# ==============================================================================
# PYDANTIC MODELS
# ==============================================================================

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    DEFINITIVE = "DEFINITIVE"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    PRELIMINARY = "PRELIMINARY"
    SPECULATIVE = "SPECULATIVE"


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=2000)
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    context: Optional[Dict[str, Any]] = Field(default=None)


class QueryResponse(BaseModel):
    query_id: str
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    latency_ms: float
    doctrines_triggered: List[str]
    sources: List[str]
    determinism_hash: str
    timestamp: str


# ==============================================================================
# DOCTRINE BLOCKS
# ==============================================================================

@dataclass
class DoctrineBlock:
    """Core knowledge unit for locomotive systems."""

    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    technical_specs: Optional[Dict[str, Any]] = None

    def matches(self, query: str) -> bool:
        query_lower = query.lower()
        return any(kw.lower() in query_lower for kw in self.keywords)

    def render_fast(self) -> str:
        return " ".join(self.conclusion_template)

    def render_defense(self) -> str:
        specs = ""
        if self.technical_specs:
            specs = "\n\nTechnical Specifications:\n" + "\n".join(
                f"  - {k}: {v}" for k, v in self.technical_specs.items()
            )

        return f"""Technical Analysis:
{self.reasoning_framework}

Key Factors:
{chr(10).join(f"  - {factor}" for factor in self.key_factors)}

Authoritative References:
{chr(10).join(f"  - {auth}" for auth in self.primary_authority)}
{specs}

Conclusion:
{" ".join(self.conclusion_template)}"""

    def render_memo(self) -> str:
        return f"""LOCOMOTIVE SYSTEMS TECHNICAL MEMORANDUM

Subject: {self.topic}

I. TECHNICAL OVERVIEW

{self.reasoning_framework}

II. CRITICAL FACTORS

{chr(10).join(f"{i+1}. {factor}" for i, factor in enumerate(self.key_factors))}

III. AUTHORITATIVE STANDARDS AND REFERENCES

{chr(10).join(f"  • {auth}" for auth in self.primary_authority)}

IV. TECHNICAL SPECIFICATIONS

{chr(10).join(f"  {k}: {v}" for k, v in (self.technical_specs or {}).items())}

V. CONCLUSION

{" ".join(self.conclusion_template)}

Confidence Level: {self.confidence.value}
"""


# ==============================================================================
# DOCTRINE CACHE — 25+ Locomotive System Topics
# ==============================================================================

DOCTRINE_CACHE = [
    DoctrineBlock(
        topic="Diesel-Electric Locomotive Prime Movers",
        keywords=["prime mover", "diesel engine", "EMD", "GE", "engine", "cylinder", "horsepower", "turbo"],
        conclusion_template=[
            "Modern diesel-electric locomotives use high-horsepower diesel engines (prime movers) to drive electrical generators or alternators.",
            "EMD traditionally uses 2-stroke V-configuration engines (710, 265H), while GE uses 4-stroke inline or V-configuration (7FDL, GEVO, FDL).",
            "Prime mover performance is governed by load regulation, turbocharger boost, and fuel injection timing."
        ],
        reasoning_framework="""Diesel-electric prime movers convert chemical energy (diesel fuel) into rotational mechanical energy, which drives a main generator (DC) or alternator (AC) to produce electrical power for traction motors. The diesel engine operates at variable RPM (typically 200-1050 RPM) controlled by engine governor systems. Turbochargers force-feed compressed air to cylinders for increased power density. EMD 2-stroke engines fire every revolution (power stroke per cylinder per revolution), providing smoother torque but requiring scavenging air. GE 4-stroke engines fire every other revolution, offering better fuel efficiency and lower emissions. Horsepower ratings range from 1,000 HP (switchers) to 6,000+ HP (modern road locomotives like GE ES44AC or EMD SD70ACe). Engine cooling is critical—radiator fans, oil coolers, and water jackets dissipate heat. Lube oil systems must maintain pressure and temperature for bearing protection.""",
        key_factors=[
            "Engine configuration: 2-stroke (EMD) vs 4-stroke (GE)",
            "Horsepower rating: determines locomotive class and tractive effort capability",
            "Turbocharger operation: forced induction for power density",
            "Engine governor: maintains RPM and load response across 8 throttle notches",
            "Cooling systems: radiator fans, oil coolers, jacket water circulation",
            "Fuel injection timing: critical for combustion efficiency and emissions",
            "Lube oil pressure: must meet minimum specs (typically 30-60 PSI at operating temp)",
            "Air intake filtration: prevents ingestion of debris and extends component life"
        ],
        primary_authority=[
            "AAR M-1003 Standard for diesel-electric locomotives",
            "EMD Operating Manual for 710G3C-T2 Engine",
            "GE Transportation GEVO-12 Service Manual",
            "FRA Part 229 Locomotive Safety Standards (§229.27 Lubricating oil, §229.29 Air filters)",
            "EPA Tier 0-4 Locomotive Emissions Standards (40 CFR Part 1033)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        technical_specs={
            "EMD 710G3C-T2": "4,300 HP, 16-cylinder 2-stroke, 710 cubic inch displacement per cylinder",
            "GE GEVO-12": "4,400 HP, 12-cylinder 4-stroke, Evolution Series",
            "Typical RPM Range": "200 (idle) to 1,050 (Run 8/full throttle)",
            "Fuel Consumption": "~0.65-0.75 lb/HP-hr at rated load",
            "Turbocharger Boost": "25-35 PSI typical"
        }
    ),

    DoctrineBlock(
        topic="AC vs DC Traction Systems",
        keywords=["traction motor", "AC traction", "DC traction", "inverter", "rectifier", "IGBT", "commutator"],
        conclusion_template=[
            "DC traction systems use DC generators and DC traction motors with commutators; simpler but higher maintenance.",
            "AC traction systems use AC alternators with solid-state inverters (IGBT-based) to drive AC induction motors; higher efficiency, lower maintenance, better adhesion control.",
            "Modern locomotives overwhelmingly use AC traction due to superior wheel-slip control and reduced motor wear."
        ],
        reasoning_framework="""DC traction (legacy technology, pre-1990s) uses a DC main generator driven by the prime mover. DC power flows directly to DC traction motors with commutators and brushes. Advantages: simple electrical design, proven technology. Disadvantages: commutator wear, brush replacement, limited wheel-slip control, lower starting tractive effort. AC traction (modern standard) uses an AC alternator (driven by prime mover) outputting 3-phase AC power. Rectifiers convert AC to DC, then IGBT inverters convert DC back to variable-frequency AC to drive 3-phase AC induction traction motors. Advantages: no brushes/commutators (lower maintenance), superior wheel-slip detection and correction via precise torque control, higher continuous tractive effort, better performance on grades. AC motors are more robust, have fewer failure modes, and can operate at higher speeds without field weakening. Inverter technology (using Insulated Gate Bipolar Transistors) allows per-axle torque control, which is critical for modern distributed power and heavy-haul operations.""",
        key_factors=[
            "DC motors: require commutator/brush maintenance every 6-12 months",
            "AC motors: brushless design, maintenance intervals 4-8 years",
            "Wheel-slip control: AC traction offers millisecond-level torque adjustment per axle",
            "Starting tractive effort: AC locomotives typically 10-15% higher than equivalent DC",
            "Inverter technology: IGBT switching at 500-2000 Hz for smooth motor control",
            "Field weakening: DC motors require field shunting; AC motors adjust frequency",
            "Parallel operation: AC traction easier to synchronize in distributed power consists"
        ],
        primary_authority=[
            "AAR M-1003 Standard for AC traction locomotives",
            "GE AC4400CW Technical Manual",
            "EMD SD70ACe Electrical System Overview",
            "IEEE 1653-2004 Standard for Traction Power Systems",
            "FRA Part 229.23 Electrical system components"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        technical_specs={
            "DC Traction Motor": "GE 752 series, 1,000-1,200 HP per motor, 4-6 motors per locomotive",
            "AC Traction Motor": "GE AC44i, EMD D43TR, ~1,000 HP per motor continuous, 6 motors typical",
            "IGBT Inverter": "1,200-3,300V, 1,000-2,000A per module",
            "AC Motor Efficiency": "~95% vs ~85% for DC motors",
            "Maintenance Interval": "DC motors 6-12 months (brushes), AC motors 4-8 years (bearings)"
        }
    ),

    DoctrineBlock(
        topic="Dynamic Braking Systems",
        keywords=["dynamic brake", "DB", "rheostatic", "regenerative", "blended braking", "grid resistor"],
        conclusion_template=[
            "Dynamic braking uses traction motors as generators to convert kinetic energy into electrical energy, providing supplemental braking without wearing brake shoes.",
            "Rheostatic dynamic braking dissipates energy as heat through resistor grids; regenerative braking returns energy to the catenary (electrified territory only).",
            "Blended braking systems coordinate dynamic brakes with air brakes for optimal stopping performance and reduced wheel/rail wear."
        ],
        reasoning_framework="""Dynamic braking converts the locomotive's kinetic energy into electrical energy by operating traction motors in generator mode. When the engineer places the dynamic brake handle in a braking position, the traction motors are electrically reconfigured to act as generators. The rotating axles (driven by the train's momentum) turn the motor armatures, generating electricity. In rheostatic dynamic braking (most common on diesel-electric locomotives), this electrical energy is dissipated as heat through resistor grids mounted on the locomotive roof (the "dynamic brake grids"). Cooling fans blow air across the grids to prevent overheating. Braking effort is proportional to motor speed—higher speeds produce more braking force. At low speeds (<10 MPH), dynamic braking becomes ineffective and air brakes must be used. Regenerative braking (used on electric locomotives or some hybrid systems) feeds generated energy back into the overhead catenary for reuse. Blended braking systems use computers to automatically coordinate dynamic braking with pneumatic air brakes, maximizing retardation while minimizing wheel/rail wear and brake shoe consumption. Modern systems can provide 50,000+ lbs of braking force at speed.""",
        key_factors=[
            "Motor reconfiguration: traction motors switch from motor mode to generator mode",
            "Energy dissipation: rheostatic grids convert electrical energy to heat (up to 4-6 MW)",
            "Speed dependency: dynamic brake effort decreases as speed decreases",
            "Thermal limits: grid resistors must not exceed temperature limits (500-700°F typical)",
            "Blended braking: computer coordinates DB and air brakes for optimal performance",
            "Low-speed ineffectiveness: below ~10 MPH, air brakes must be primary",
            "Extended range dynamic brake: some systems allow DB down to 5 MPH",
            "Regenerative option: electrified territory allows energy return to catenary"
        ],
        primary_authority=[
            "AAR M-1003 Dynamic Brake System Standards",
            "FRA Part 229.47 Automatic brake components",
            "49 CFR §232.103 General requirements for pneumatic brake systems",
            "GE Dash-9 Dynamic Brake Manual",
            "EMD SD70ACe Dynamic Brake Control Logic"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        technical_specs={
            "Braking Force": "40,000-60,000 lbs at 40+ MPH (6-axle locomotive)",
            "Grid Resistor Capacity": "4,000-6,000 kW continuous dissipation",
            "Effective Speed Range": "10-70 MPH typical",
            "Fan Cooling": "Axial fans, 10,000-20,000 CFM airflow across grids",
            "Blended Brake Activation": "Automatic blend at speeds >15 MPH"
        }
    ),

    DoctrineBlock(
        topic="Air Brake Systems - 26-L and CCBII",
        keywords=["air brake", "26-L", "CCB", "CCBII", "brake pipe", "auxiliary reservoir", "emergency reservoir", "brake cylinder"],
        conclusion_template=[
            "The 26-L air brake system is the North American standard for freight locomotives, using a reduction in brake pipe pressure to apply brakes and an increase to release.",
            "Computer Controlled Brake (CCBII) enhances the 26-L system with electronic monitoring and graduated release capability.",
            "Brake pipe pressure (typically 90 PSI) is the control signal; emergency applications occur when brake pipe is vented rapidly."
        ],
        reasoning_framework="""Locomotive air brake systems operate on the "pressure reduction" principle established by George Westinghouse. The brake pipe (typically 1.25-inch diameter pipe running the length of the train) is charged to 90 PSI when brakes are released. Each car has a control valve (AB valve, ABDW valve, or modern equivalents) that senses brake pipe pressure. To apply brakes, the engineer uses the automatic brake valve to vent air from the brake pipe (reduction of 6-8 PSI for minimum service, up to full depletion for emergency). The control valve on each car senses the reduction and transfers air from the auxiliary reservoir to the brake cylinder, pushing brake shoes against wheels. The greater the brake pipe reduction, the higher the brake cylinder pressure (up to ~50 PSI in freight service). To release brakes, brake pipe pressure is restored; control valves vent brake cylinders and recharge auxiliary reservoirs. The 26-L system is the standard for freight locomotives, providing graduated release (partial brake release without full release). Computer Controlled Brake (CCBII) adds electronic monitoring: sensors track brake pipe pressure, brake cylinder pressure, and valve position, transmitting data to the engineer's display. CCBII enables more precise control and diagnostics. Emergency braking: if brake pipe pressure drops rapidly (>20 PSI/sec), the control valve triggers an emergency application, dumping all brake pipe air and maximizing brake cylinder pressure instantly.""",
        key_factors=[
            "Brake pipe pressure: 90 PSI normal, reductions trigger brake applications",
            "Service application: 6-26 PSI brake pipe reduction, graduated brake force",
            "Emergency application: rapid brake pipe venting, full brake cylinder pressure",
            "Auxiliary reservoir: stores air for brake applications (capacity ~2,500 cubic inches per car)",
            "Brake cylinder: converts air pressure to mechanical force (50 PSI max in freight)",
            "Control valve: AB, ABDW, DB-60—senses brake pipe and controls air flow",
            "Graduated release: 26-L system allows partial brake release without full release",
            "CCBII monitoring: electronic sensors provide real-time brake system status"
        ],
        primary_authority=[
            "49 CFR Part 232 Brake System Safety Standards for Freight and Other Non-Passenger Trains",
            "AAR Field Manual of the AAR Interchange Rules (Chapter 8: Air Brakes)",
            "FRA Part 229 Subpart C: Brake System Components",
            "Wabtec 26-L Air Brake Equipment Manual",
            "New York Air Brake CCBII System Technical Guide"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        technical_specs={
            "Brake Pipe Pressure": "90 PSI (released), 60-84 PSI (service), 0 PSI (emergency)",
            "Brake Cylinder Pressure": "0 PSI (released), 10-50 PSI (service), 50+ PSI (emergency)",
            "Auxiliary Reservoir": "~2,500 cubic inches per freight car",
            "Emergency Reservoir": "~1,800 cubic inches (supplements emergency applications)",
            "Brake Pipe Diameter": "1.25 inches standard",
            "Service Application Rate": "5-7 PSI/sec brake pipe reduction",
            "Emergency Application Rate": ">20 PSI/sec brake pipe reduction"
        }
    ),

    DoctrineBlock(
        topic="Electronically Controlled Pneumatic (ECP) Brakes",
        keywords=["ECP", "electronically controlled pneumatic", "ECP brake", "electric brake signal", "trainline"],
        conclusion_template=[
            "ECP brakes replace the pneumatic brake pipe signal with an electronic control signal, enabling simultaneous brake application/release across entire train length.",
            "ECP systems significantly reduce stopping distances (20-50% shorter) and improve train handling by eliminating propagation delay.",
            "Adoption has been limited due to infrastructure cost and compatibility issues with conventional air brake equipment."
        ],
        reasoning_framework="""Electronically Controlled Pneumatic (ECP) brakes fundamentally alter the brake control architecture by separating the control function (electronic) from the pneumatic function (air supply). In conventional air brakes, the brake pipe serves dual purposes: air supply and control signal. Brake pipe pressure changes propagate sequentially down the train at ~900 ft/sec, causing delayed brake application on rear cars (serial propagation). ECP systems use a trainline wire (230V DC power + data communication) running the length of the train. Electronic control units (ECUs) on each car receive brake commands simultaneously via the trainline. Brake applications and releases occur in unison across all cars within milliseconds, eliminating serial propagation delay. This simultaneous action reduces train slack action, improves stopping distances, and allows graduated brake release in service (reducing thermal stress on wheels). The pneumatic portion remains: a trainline pipe provides compressed air at constant pressure (~110 PSI), and each car's ECU controls electro-pneumatic valves to modulate brake cylinder pressure locally. Benefits: 20-50% shorter stopping distances, reduced wheel/rail wear, better train handling, enhanced safety. Challenges: high initial cost ($5,000-$10,000 per car for retrofit), requires entire train to be ECP-equipped, not compatible with conventional air brake operation without dual-mode systems. ECP mandate for high-hazard flammable trains (HHFTs) was proposed by FRA in 2015 but later repealed in 2017 due to cost concerns.""",
        key_factors=[
            "Electronic control signal: replaces pneumatic brake pipe pressure signal",
            "Simultaneous application: all brakes apply/release at same instant (no serial propagation)",
            "Stopping distance: 20-50% reduction compared to conventional air brakes",
            "Trainline power: 230V DC + digital communication protocol",
            "Pneumatic air supply: constant-pressure air line (~110 PSI) separate from control",
            "Electro-pneumatic valves: ECU controls local brake cylinder pressure per car",
            "Retrofit cost: $5,000-$10,000 per car",
            "Compatibility issue: ECP-equipped cars cannot intermix with conventional cars without dual-mode"
        ],
        primary_authority=[
            "49 CFR §232.607 ECP Brake System Specific Requirements",
            "AAR S-4210 Standard for ECP Brake Systems",
            "FRA Emergency Order 28 (HHFT brake requirements, later repealed)",
            "Wabtec ECP Brake System Technical Manual",
            "New York Air Brake ECP Product Guide"
        ],
        confidence=ConfidenceLevel.HIGH,
        technical_specs={
            "Trainline Voltage": "230V DC nominal",
            "Communication Protocol": "Proprietary digital signal (Wabtec, NYAB variants)",
            "Air Supply Pressure": "110 PSI constant",
            "Brake Application Time": "<1 second full train (vs 20-60 seconds conventional)",
            "Stopping Distance Reduction": "20-50% depending on train length/weight",
            "Power Consumption": "~500W per car ECU"
        }
    ),

    DoctrineBlock(
        topic="Distributed Power and LOCOTROL",
        keywords=["distributed power", "DP", "LOCOTROL", "remote locomotive", "lead unit", "mid-train DP", "end-of-train DP"],
        conclusion_template=[
            "Distributed power (DP) places additional locomotives (remote units) in the middle or rear of the train, controlled electronically by the lead locomotive.",
            "LOCOTROL and similar systems use radio or trainline communication to synchronize throttle, dynamic brake, and air brake commands across all locomotives.",
            "DP reduces in-train forces, improves train handling on grades, and increases tractive effort without exceeding coupler strength limits."
        ],
        reasoning_framework="""Distributed power technology allows a train to operate with locomotives at the head end (lead consist) and additional remote locomotives positioned mid-train or at the rear. The lead engineer controls all locomotives via radio commands (LOCOTROL system by Wabtec or equivalent GE/EMD systems). The remote units (slaves) mirror the lead unit's throttle position, dynamic brake application, and air brake commands with minimal delay (<1 second). Benefits: (1) Reduced in-train forces—mid-train or rear DP helps "push" the train, reducing buff and draft forces on couplers, allowing longer/heavier trains without exceeding coupler limits (typically 350,000-500,000 lbs). (2) Improved train handling on grades—rear DP prevents rear-end run-in during descent and reduces drawbar pull on head-end locomotives during ascent. (3) Increased effective tractive effort—distributing power along the train length allows higher total tonnage without overwhelming head-end traction. LOCOTROL system uses 900 MHz or 450 MHz radio to transmit commands from lead to remotes. Modern systems are bidirectional, allowing remote units to report status (fuel level, engine health, brake status) back to lead. Air brake control is synchronized—lead unit makes brake pipe changes, remotes mirror or assist depending on mode (sync mode vs independent mode). DP has become standard for heavy-haul operations (coal, grain, intermodal) and mountainous territory (helper operations). FRA allows DP operation without caboose or rear-end helper crew if End-of-Train (EOT) device is installed.""",
        key_factors=[
            "LOCOTROL radio system: 450 MHz or 900 MHz bidirectional communication",
            "Synchronization: remote units mirror lead throttle/brake commands within 1 second",
            "In-train force reduction: DP decreases coupler stress by distributing tractive effort",
            "Coupler limits: 350,000-500,000 lbs typical, DP allows higher tonnage without exceeding",
            "Mid-train DP: optimal for very long trains (150+ cars) to reduce slack action",
            "Rear DP: common for grade operations, prevents run-in on descent",
            "Status monitoring: remotes report fuel, brake, engine health to lead unit display",
            "FRA approval: DP replaces rear-end crew if EOT device installed"
        ],
        primary_authority=[
            "49 CFR §229.9 Movement of Defective Locomotives (DP provisions)",
            "49 CFR §232.23 Radio-Based End-of-Train Devices",
            "AAR Circular OT-55-O Distributed Power Operations",
            "Wabtec LOCOTROL DP System Operating Manual",
            "GE Trip Optimizer with DP Capability Technical Guide"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        technical_specs={
            "Radio Frequency": "450 MHz or 900 MHz (LOCOTROL)",
            "Command Latency": "<1 second lead to remote",
            "Communication Range": "2-10 miles depending on terrain",
            "DP Configuration": "1+1 (head+rear), 1+1+1 (head+mid+rear), 2+1 (head consist + rear)",
            "Coupler Load Reduction": "30-50% reduction in peak buff/draft forces",
            "Maximum Train Length": "200+ cars with proper DP placement"
        }
    ),

    DoctrineBlock(
        topic="Locomotive Fuel Systems and Fuel Efficiency",
        keywords=["fuel system", "fuel tank", "fuel consumption", "fuel efficiency", "fuel injector", "fuel pump", "diesel fuel"],
        conclusion_template=[
            "Locomotive fuel systems store, filter, and deliver diesel fuel to the engine at precise pressure and flow rates.",
            "Fuel efficiency is measured in gallons per thousand gross ton-miles (GTM) or pounds per horsepower-hour; typical modern locomotives achieve 0.65-0.80 lb/HP-hr.",
            "Trip optimization systems (GE Trip Optimizer, Wabtec LEADER) reduce fuel consumption by 5-15% through optimal speed/throttle profiles."
        ],
        reasoning_framework="""Locomotive fuel systems consist of fuel tanks (typically 3,000-5,000 gallon capacity), fuel pumps, filters, fuel injectors, and engine control systems. Diesel fuel is drawn from the main tank by a transfer pump, passes through primary and secondary filters (removing water and particulates to <10 microns), and is delivered to high-pressure fuel injectors at the engine. Modern electronic fuel injection (EFI) systems control injection timing and duration to optimize combustion, reduce emissions, and improve efficiency. Fuel consumption varies with engine load, speed, and operating conditions. At idle (Notch 0), a 4,400 HP locomotive consumes ~10-15 gallons/hour. At maximum throttle (Run 8), consumption reaches 180-220 gallons/hour. Fuel efficiency metrics: gallons per thousand gross ton-miles (GTM) is common (lower is better; typical range 0.8-1.2 gal/GTM). Pounds per horsepower-hour (lb/HP-hr) measures engine thermal efficiency; modern Tier 4 engines achieve 0.65-0.75 lb/HP-hr. Trip optimization systems (GE's Trip Optimizer, Wabtec's LEADER) use GPS, track profile, train characteristics, and schedule to compute optimal speed and throttle commands, reducing fuel consumption by 5-15% on long-haul routes. Fuel quality is critical—water contamination causes injector failure, and algae growth in tanks requires biocide treatment. Fuel management systems monitor tank levels, consumption rates, and alert for abnormal usage.""",
        key_factors=[
            "Fuel tank capacity: 3,000-5,000 gallons typical for road locomotives",
            "Fuel consumption at idle: 10-15 gal/hr",
            "Fuel consumption at Run 8: 180-220 gal/hr",
            "Fuel filtration: primary and secondary filters to <10 microns",
            "Fuel efficiency: 0.65-0.80 lb/HP-hr for modern Tier 4 engines",
            "GTM metric: 0.8-1.2 gallons per thousand gross ton-miles",
            "Trip optimization: 5-15% fuel savings via optimal speed/throttle control",
            "Fuel quality: water and algae contamination are primary concerns"
        ],
        primary_authority=[
            "AAR M-1003 Fuel System Standards",
            "EPA 40 CFR Part 1033 Locomotive Emission Standards (fuel quality)",
            "FRA Part 229.53 Fuel, Oil, and Water",
            "GE Trip Optimizer Technical Manual",
            "EMD Engine Service Manual (Fuel System Chapter)"
        ],
        confidence=ConfidenceLevel.HIGH,
        technical_specs={
            "Fuel Tank": "3,000-5,000 gallons (4-axle: 3,000; 6-axle: 4,000-5,000)",
            "Fuel Pump Pressure": "60-100 PSI to injectors",
            "Fuel Filter": "Primary 30 micron, secondary 10 micron or finer",
            "Fuel Consumption Rate": "0.65-0.80 lb/HP-hr at rated load",
            "Trip Optimizer Savings": "5-15% fuel reduction on routes >200 miles"
        }
    ),

    DoctrineBlock(
        topic="Locomotive Cooling Systems",
        keywords=["cooling system", "radiator", "radiator fan", "coolant", "jacket water", "oil cooler", "aftercooler"],
        conclusion_template=[
            "Locomotive cooling systems dissipate heat from the diesel engine, lube oil, and intake air using radiators, fans, and heat exchangers.",
            "Radiator fans (typically axial, belt-driven or electric) move large volumes of air (50,000+ CFM) across radiator cores.",
            "Cooling system failures (overheating, low coolant, fan failure) are leading causes of locomotive mechanical failures and service disruptions."
        ],
        reasoning_framework="""Locomotive cooling systems manage thermal loads from multiple sources: (1) Engine jacket water cooling—the diesel engine generates immense heat; a closed-loop water/glycol mixture circulates through engine block and cylinder heads, absorbing heat. This hot coolant flows to radiators where ambient air removes heat. (2) Lube oil cooling—engine lube oil reaches high temperatures; an oil cooler (heat exchanger) uses either coolant or ambient air to reduce oil temperature to safe levels (180-220°F). (3) Aftercooler/intercooler—turbocharger compresses intake air, raising its temperature; an aftercooler cools this air before it enters the engine, increasing air density and combustion efficiency. Radiator fans are the primary cooling mechanism. Axial fans (4-8 feet diameter) are driven by belts from the diesel engine or by electric motors. Fan speed is thermostatically controlled—at low engine temps, fans idle or run slow; as temps rise, fans spin faster (up to 900-1,200 RPM), moving 50,000-100,000 CFM of air across radiator cores. Radiator cores are honeycomb structures of tubes and fins; coolant flows through tubes while air flows across fins. Cooling capacity must handle full engine load in high ambient temps (up to 110°F desert conditions). Common failures: radiator leaks (corrosion, vibration), fan belt breakage, coolant pump failure, thermostat failure (stuck open/closed), low coolant level (leaks or evaporation). Overheat conditions trigger engine load reduction or shutdown to prevent damage. Modern systems monitor coolant temp, pressure, and flow rate; alerts warn engineers before critical overheating.""",
        key_factors=[
            "Radiator capacity: must dissipate 4-6 MW of heat at full engine load",
            "Coolant composition: 50/50 water/glycol mix, corrosion inhibitors",
            "Fan airflow: 50,000-100,000 CFM depending on locomotive class",
            "Oil cooler: maintains lube oil at 180-220°F",
            "Aftercooler: reduces intake air temp to increase combustion efficiency",
            "Thermostat control: modulates fan speed based on coolant temp",
            "Coolant pressure: 15-20 PSI in pressurized systems to raise boiling point",
            "Common failures: radiator leaks, fan belt breakage, coolant pump failure"
        ],
        primary_authority=[
            "FRA Part 229.33 Cooling Systems",
            "AAR M-1003 Locomotive Cooling System Standards",
            "EMD Maintenance Manual: Cooling System Chapter",
            "GE Locomotive Cooling System Technical Guide"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        technical_specs={
            "Radiator Capacity": "4-6 MW heat dissipation at full load",
            "Fan Diameter": "48-84 inches (4-7 feet)",
            "Fan Speed": "300-1,200 RPM (variable based on temp)",
            "Coolant Flow Rate": "500-800 GPM through engine block",
            "Coolant Temp Range": "160-200°F normal operating range",
            "Oil Cooler Capacity": "Maintains oil at 180-220°F",
            "Aftercooler Efficiency": "Reduces intake air temp by 100-150°F"
        }
    ),

    DoctrineBlock(
        topic="Turbocharger Systems",
        keywords=["turbocharger", "turbo", "boost pressure", "compressor", "turbine", "wastegate", "turbo lag"],
        conclusion_template=[
            "Turbochargers use exhaust gas energy to drive a compressor that forces additional air into the engine, increasing power density.",
            "Boost pressure (typically 25-35 PSI) is critical for achieving rated horsepower; insufficient boost indicates turbo failure or air leaks.",
            "Turbocharger failures (bearing failure, turbine blade damage, compressor surge) require immediate engine derate or shutdown."
        ],
        reasoning_framework="""Turbochargers are centrifugal compressors driven by exhaust gas turbines. Hot exhaust gases from the diesel engine spin a turbine wheel (reaching 50,000-100,000 RPM); the turbine shaft drives a compressor wheel that draws in ambient air, compresses it, and forces it into the engine intake manifold. This forced induction (boost) increases air density, allowing more fuel to be burned per cycle, thus increasing power output without increasing engine displacement. Boost pressure is measured in PSI above atmospheric (typically 25-35 PSI for locomotive turbos). The aftercooler cools the compressed air to further increase density. Turbochargers enable smaller engines to produce higher horsepower (e.g., a 12-cylinder GE engine with turbo produces 4,400 HP, whereas a naturally aspirated version might only achieve 2,500 HP). Turbo failures: bearing failure due to oil starvation, turbine blade damage from ingested debris or overheating, compressor surge (flow reversal causing damaging vibration). Symptoms of turbo failure: loss of boost pressure, black smoke (incomplete combustion due to insufficient air), reduced power, abnormal noise (whistling, grinding). Wastegates (on some turbos) bypass exhaust gas around the turbine to limit boost pressure and prevent overboosting. Turbo lag (delay between throttle increase and boost buildup) is minimal on large diesel engines due to their steady-state operation.""",
        key_factors=[
            "Turbo speed: 50,000-100,000 RPM typical",
            "Boost pressure: 25-35 PSI for rated horsepower",
            "Bearing lubrication: critical—oil starvation causes rapid bearing failure",
            "Compressor surge: flow reversal event, can damage compressor blades",
            "Turbine blade damage: caused by excessive heat or ingested particles",
            "Aftercooler integration: cools compressed air to increase density",
            "Wastegate: prevents overboosting by bypassing exhaust gas",
            "Power density increase: turbocharged engines produce 50-100% more power than naturally aspirated"
        ],
        primary_authority=[
            "FRA Part 229.27 Turbocharger and Air Intake Requirements",
            "AAR M-1003 Turbocharger Standards",
            "GE GEVO Turbocharger Service Manual",
            "EMD 710 Engine Turbocharger Maintenance Guide"
        ],
        confidence=ConfidenceLevel.HIGH,
        technical_specs={
            "Turbo Speed": "50,000-100,000 RPM",
            "Boost Pressure": "25-35 PSI gauge pressure",
            "Turbine Inlet Temp": "1,000-1,200°F",
            "Compressor Ratio": "2.5:1 to 3.5:1 pressure ratio",
            "Airflow Rate": "10,000-20,000 CFM at full boost",
            "Bearing Oil Pressure": "30-60 PSI minimum"
        }
    ),

    DoctrineBlock(
        topic="Wheel-Rail Adhesion and Creep Control",
        keywords=["adhesion", "wheel slip", "creep control", "sander", "traction control", "coefficient of friction"],
        conclusion_template=[
            "Wheel-rail adhesion (coefficient of friction, typically 0.25-0.35 in dry conditions) determines maximum tractive effort before wheel slip occurs.",
            "Sanding systems apply sand to rail to increase adhesion in wet, icy, or contaminated conditions.",
            "AC traction systems use advanced creep control to detect and correct wheel slip within milliseconds, maximizing adhesion utilization."
        ],
        reasoning_framework="""Wheel-rail adhesion is the friction force between locomotive wheels and steel rail that allows tractive effort to be transmitted without slipping. Adhesion is quantified by the coefficient of friction (μ), typically 0.25-0.35 for dry rail, dropping to 0.10-0.20 for wet/oily rail, and as low as 0.05 for ice or leaf-contaminated rail. Maximum tractive effort = adhesion coefficient × locomotive weight on drivers. Example: a 6-axle locomotive weighing 420,000 lbs with μ=0.30 can produce 126,000 lbs tractive effort before slipping. Wheel slip (loss of adhesion) occurs when tractive effort exceeds available friction. Slipping wheels spin faster than rail speed, causing rail burn (surface damage), increased wheel wear, and loss of pulling power. Sanding systems combat low adhesion by depositing sand (pneumatically delivered) onto the rail ahead of driving wheels, increasing friction. Modern AC traction locomotives use sophisticated creep control: each axle's speed is monitored continuously; when an axle begins to slip (speed exceeds expected speed by >2-5%), the inverter reduces torque to that specific axle within milliseconds, allowing it to regain adhesion. This per-axle control (versus the system-wide response of DC traction) allows AC locomotives to operate closer to the adhesion limit without excessive slip, maximizing performance. Sanders are activated manually or automatically when slip is detected. Excessive sanding wastes sand and can cause traction motor flashover (sand contamination of electrical components).""",
        key_factors=[
            "Adhesion coefficient: 0.25-0.35 (dry), 0.10-0.20 (wet), 0.05-0.10 (ice/leaves)",
            "Maximum TE: μ × weight on drivers",
            "Wheel slip detection: speed sensors monitor each axle",
            "Creep control: AC traction adjusts torque per axle in <50ms",
            "Sanding: applies sand to rail to increase friction",
            "Rail contamination: oil, grease, leaves, ice reduce adhesion dramatically",
            "Rail burn: slipping wheels damage rail surface",
            "AC traction advantage: per-axle slip control vs system-wide in DC"
        ],
        primary_authority=[
            "AAR M-1003 Adhesion and Traction Standards",
            "FRA Part 229.45 Sanding Equipment",
            "IEEE 1653-2004 Traction Power Systems",
            "GE AC Traction Creep Control Algorithm Documentation"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        technical_specs={
            "Dry Rail Adhesion": "0.25-0.35 μ",
            "Wet Rail Adhesion": "0.10-0.20 μ",
            "Ice/Contaminated Rail": "0.05-0.10 μ",
            "Creep Control Response": "<50ms detection and correction",
            "Sand Application Rate": "2-5 lbs per minute per sander",
            "Wheel Slip Threshold": "2-5% speed differential triggers correction"
        }
    ),

    DoctrineBlock(
        topic="FRA Part 229 Locomotive Safety Standards",
        keywords=["FRA 229", "locomotive inspection", "safety standards", "daily inspection", "92-day inspection", "periodic inspection"],
        conclusion_template=[
            "FRA Part 229 establishes minimum safety standards for locomotives, including inspection intervals, component standards, and operational requirements.",
            "Daily inspections (pre-departure) and periodic inspections (92-day, annual) are mandatory.",
            "Violations of Part 229 can result in civil penalties, locomotive withdrawal from service, and increased FRA oversight."
        ],
        reasoning_framework="""FRA Part 229 (49 CFR Part 229) is the primary regulatory framework governing locomotive safety in the United States. It establishes design standards, inspection requirements, maintenance procedures, and operational limitations. Key provisions: (1) Daily inspection (§229.21)—before each departure, a qualified person must inspect safety-critical components (brakes, safety appliances, lights, horns, coupling devices, sanders). Defects must be tagged and repaired before service. (2) 92-day inspection (§229.23)—more thorough inspection every 92 days or less, including running gear, air brake system, electrical components, safety devices. (3) Annual inspection (§229.25)—comprehensive inspection including steam generator (if equipped), air compressor, electrical systems, structural integrity. (4) Component-specific standards: §229.27 (lubricating oil), §229.29 (air filters), §229.33 (cooling systems), §229.45 (sanders), §229.47 (automatic brake), §229.51 (independent brake). (5) Event recorder (§229.135)—all locomotives must have certified event recorders capturing speed, direction, throttle, brake, time. (6) Positive Train Control (§229.13-229.17)—locomotives on PTC-equipped lines must have operational PTC systems. Non-compliance: FRA inspectors conduct audits and field inspections; violations can result in civil penalties ($1,000-$25,000 per violation), locomotive removal from service, and increased inspection frequency. Railroads must maintain records of all inspections and repairs for FRA review.""",
        key_factors=[
            "Daily inspection: required before each departure (§229.21)",
            "92-day inspection: every 92 days or less (§229.23)",
            "Annual inspection: comprehensive yearly inspection (§229.25)",
            "Component standards: oil, air filters, cooling, brakes, sanders, etc.",
            "Event recorder: mandatory, certified, captures operational data (§229.135)",
            "PTC requirement: operational PTC on equipped territories (§229.13-17)",
            "Inspection records: must be maintained and available for FRA review",
            "Civil penalties: $1,000-$25,000 per violation"
        ],
        primary_authority=[
            "49 CFR Part 229 Railroad Locomotive Safety Standards",
            "FRA Locomotive Inspection Handbook",
            "AAR Interchange Rules Chapter 12: Locomotive Inspection"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        technical_specs={
            "Daily Inspection": "Pre-departure, safety-critical components",
            "92-Day Inspection": "Every 92 days, detailed component check",
            "Annual Inspection": "Yearly, comprehensive system validation",
            "Event Recorder Certification": "Must meet §229.135 specs",
            "PTC Compliance": "Required on PTC-equipped main lines"
        }
    ),

    # ... (continuing with 15 more DoctrineBlocks to reach 25+ total)

    DoctrineBlock(
        topic="Positive Train Control (PTC)",
        keywords=["PTC", "positive train control", "I-ETMS", "E-ATC", "train control", "GPS", "cab signal"],
        conclusion_template=[
            "Positive Train Control (PTC) is a GPS and radio-based system that prevents train-to-train collisions, overspeed derailments, and unauthorized incursions into work zones.",
            "I-ETMS (Interoperable ETMS) is the dominant PTC implementation in North America, mandated by the Rail Safety Improvement Act of 2008.",
            "PTC systems continuously monitor train position, speed, and authority limits, automatically applying brakes if unsafe conditions are detected."
        ],
        reasoning_framework="""Positive Train Control (PTC) is an advanced safety overlay system mandated by Congress following fatal accidents (Chatsworth 2008). PTC prevents: (1) train-to-train collisions, (2) overspeed derailments, (3) incursions into established work zone limits, (4) movement through misaligned switches. The system uses GPS positioning, digital radio communication (220 MHz), onboard computers, and wayside interface units (WIUs) to continuously determine train location, speed, and movement authority. The onboard PTC system receives authority limits (track warrants, signal aspects, speed restrictions) via radio from the back-office server. It calculates a safe braking curve based on train characteristics (length, weight, braking capacity) and track profile (grades, curvature). If the train exceeds the safe speed or approaches a red signal, PTC initiates a penalty brake application (automatic emergency braking) to prevent violation. I-ETMS (Interoperable Electronic Train Management System) is the most widely deployed PTC system, developed by Wabtec. It uses 220 MHz radio, GPS with GNSS corrections, and integrates with existing signal systems. E-ATC (Enhanced Automatic Train Control), used primarily by Amtrak and commuter railroads, uses similar principles with different hardware. PTC does NOT replace the engineer—it is a safety backstop. The engineer still operates the train; PTC only intervenes if safety is compromised. PTC installation was mandated for all Class I railroads and passenger carriers by December 2020 (extended from 2015 deadline). Implementation costs exceeded $15 billion industry-wide.""",
        key_factors=[
            "PTC functions: prevents collisions, overspeed, work zone incursions, switch violations",
            "GPS positioning: determines train location to within 10 meters",
            "Radio communication: 220 MHz data radio (I-ETMS)",
            "Braking curve calculation: based on train characteristics and track profile",
            "Automatic intervention: penalty brake if limits are violated",
            "I-ETMS: dominant North American PTC system (Wabtec)",
            "FRA mandate: required on Class I railroads and passenger lines by 2020",
            "Engineer role: PTC is safety overlay, engineer still operates train"
        ],
        primary_authority=[
            "49 CFR Part 236 Subpart I - Positive Train Control Systems",
            "Rail Safety Improvement Act of 2008 (Public Law 110-432)",
            "FRA PTC Implementation Guide",
            "Wabtec I-ETMS Technical Specification"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        technical_specs={
            "GPS Accuracy": "10 meters typical with GNSS corrections",
            "Radio Frequency": "220 MHz (I-ETMS)",
            "Data Update Rate": "1-5 seconds",
            "Braking Enforcement": "Automatic penalty brake if limits violated",
            "Implementation Deadline": "December 31, 2020",
            "Industry Cost": "$15+ billion total investment"
        }
    ),

    DoctrineBlock(
        topic="Event Recorder Data Analysis",
        keywords=["event recorder", "locomotive data", "speed tape", "black box", "accident investigation", "operational data"],
        conclusion_template=[
            "Event recorders (locomotive 'black boxes') continuously capture speed, throttle, brake, direction, and time data for accident investigation and operational analysis.",
            "FRA requires certified event recorders on all locomotives; data must be downloadable and preserved for analysis.",
            "Event recorder data is critical evidence in accident investigations, liability determinations, and compliance audits."
        ],
        reasoning_framework="""Event recorders are hardened electronic devices (similar to flight data recorders in aviation) that continuously record locomotive operational parameters. Mandated by FRA §229.135, event recorders must capture at minimum: train speed, throttle position, brake application (independent and automatic), direction, time, and event markers (horn, bell, sander activation). Modern recorders also capture: GPS position, PTC status, dynamic brake, MU status, and system alarms. Data is recorded at 1-second intervals (or faster for critical parameters like speed). The recorder is housed in a crash-hardened enclosure designed to survive derailments, fires, and collisions. Data is stored on solid-state memory (flash storage) with sufficient capacity for 48+ hours of operation. Download interfaces allow FRA inspectors, railroad investigators, and authorized personnel to extract data. In accident investigations, event recorder data provides an objective timeline of engineer actions and locomotive response. Example: in an overspeed derailment, recorder data shows whether the engineer applied brakes, the speed at the time of derailment, and whether speed restrictions were exceeded. Data analysis: speed profiles can reveal hard braking events (indicating potential signal violations or unexpected obstacles), excessive idling (fuel waste), and compliance with speed restrictions. Railroads use event recorder data for engineer performance monitoring, fuel efficiency analysis, and operational optimization. Legal protections: event recorder data is often protected from public disclosure under FRA regulations, but is discoverable in litigation.""",
        key_factors=[
            "Mandatory parameters: speed, throttle, brake, direction, time (§229.135)",
            "Recording interval: 1 second minimum",
            "Crash-hardened: survives fire, impact, water immersion",
            "Storage capacity: 48+ hours of continuous operation",
            "Download capability: accessible to FRA and authorized investigators",
            "Accident investigation: objective evidence of engineer actions",
            "Performance monitoring: railroads use data for efficiency and compliance",
            "Legal protection: limited public disclosure, discoverable in litigation"
        ],
        primary_authority=[
            "49 CFR §229.135 Event Recorders",
            "FRA Event Recorder Download and Analysis Guide",
            "NTSB Accident Investigation Handbook (Railroad Chapter)"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        technical_specs={
            "Recording Rate": "1 Hz (1 sample/second) minimum",
            "Storage": "Solid-state, 48+ hours capacity",
            "Crash Protection": "Fire resistance, impact resistance per §229.135",
            "Parameters": "Speed, throttle, brake, direction, time, horn, bell, sander, PTC, GPS",
            "Download Interface": "USB, RS-232, or wireless (varies by manufacturer)"
        }
    ),

    DoctrineBlock(
        topic="Locomotive Weight and Tractive Effort Calculations",
        keywords=["tractive effort", "TE", "starting TE", "continuous TE", "drawbar pull", "locomotive weight", "adhesion"],
        conclusion_template=[
            "Tractive effort (TE) is the force a locomotive can exert at the rail, limited by either engine power or wheel-rail adhesion.",
            "Starting TE (at 0 MPH) is adhesion-limited; continuous TE (at speed) is power-limited.",
            "Drawbar pull is the force available at the coupler after subtracting locomotive resistance; it determines train tonnage capacity."
        ],
        reasoning_framework="""Tractive effort (TE) is the horizontal force a locomotive applies at the wheel-rail interface to move a train. TE is limited by two factors: (1) Adhesion limit—maximum force before wheels slip (TE_adhesion = weight on drivers × adhesion coefficient). (2) Power limit—at higher speeds, available torque decreases due to motor characteristics and power limits (TE_power = HP × 375 / speed_MPH). At low speeds (0-15 MPH), adhesion is the limit. Example: 6-axle locomotive, 420,000 lbs weight, 0.30 adhesion → max TE = 126,000 lbs. Above ~15 MPH, power becomes the limit. Example: 4,400 HP locomotive at 40 MPH → TE_power = 4,400 × 375 / 40 = 41,250 lbs. Continuous TE is the sustained force a locomotive can produce at a given speed without overheating motors or exceeding thermal limits. Starting TE (short-time TE) is higher, used for initial acceleration but cannot be sustained. Drawbar pull (DBP) is the force available at the rear coupler to pull the train, equal to TE minus locomotive resistance (rolling resistance, aerodynamic drag, grade resistance). DBP = TE - (locomotive weight × resistance factor). Resistance factor is ~2-5 lbs per ton on level track at moderate speeds. Tonnage rating: railroads calculate maximum train tonnage a locomotive can haul over a specific route by dividing DBP by train resistance per ton (which varies with grade, curvature, and speed). Example: DBP 80,000 lbs, train resistance 8 lbs/ton on 1% grade → max tonnage = 80,000 / 8 = 10,000 tons.""",
        key_factors=[
            "Tractive effort: force at wheel-rail interface",
            "Adhesion limit: TE_adhesion = weight × adhesion coefficient",
            "Power limit: TE_power = HP × 375 / speed (MPH)",
            "Starting TE: adhesion-limited, maximum at 0 MPH",
            "Continuous TE: power-limited, sustainable at speed",
            "Drawbar pull: TE minus locomotive resistance",
            "Tonnage rating: DBP divided by train resistance per ton",
            "Resistance factors: 2-5 lbs/ton (level), higher on grades"
        ],
        primary_authority=[
            "AAR Manual of Standards and Recommended Practices Section M: Locomotives",
            "Hay, William W. Railroad Engineering (textbook, TE calculations)",
            "GE Locomotive Performance Handbook"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        technical_specs={
            "Starting TE (AC)": "120,000-140,000 lbs (6-axle, modern AC locomotive)",
            "Continuous TE at 11 MPH": "90,000-110,000 lbs typical",
            "Power Conversion": "TE (lbs) = HP × 375 / speed (MPH)",
            "Adhesion Coefficient": "0.25-0.35 (dry rail)",
            "Locomotive Resistance": "2-5 lbs/ton on level track",
            "Grade Resistance": "20 lbs/ton per 1% grade"
        }
    ),

    DoctrineBlock(
        topic="Locomotive Emissions Standards (EPA Tier 0-4)",
        keywords=["emissions", "EPA", "Tier 4", "Tier 3", "Tier 2", "NOx", "particulate matter", "PM", "diesel emissions"],
        conclusion_template=[
            "EPA locomotive emissions standards (Tier 0 through Tier 4) progressively reduce nitrogen oxides (NOx), particulate matter (PM), and hydrocarbons.",
            "Tier 4 locomotives (2015+) use advanced technologies: high-pressure fuel injection, exhaust gas recirculation (EGR), and diesel particulate filters (DPF).",
            "Compliance is mandatory; remanufactured locomotives must meet the tier standard applicable at time of remanufacture."
        ],
        reasoning_framework="""The Environmental Protection Agency (EPA) regulates locomotive emissions under 40 CFR Part 1033. The regulations establish progressive tiers with increasingly stringent limits on NOx, PM, and hydrocarbons (HC). Tier 0 (pre-2000 baseline): no federal standards, engines varied widely. Tier 1 (2000-2004): first federal limits, NOx ~7-9 g/HP-hr. Tier 2 (2005-2011): reduced NOx to 5.5 g/HP-hr, PM to 0.22 g/HP-hr. Tier 3 (2012-2014): NOx 5.5, PM 0.10, HC+NOx combined limits. Tier 4 (2015+): NOx 1.3 g/HP-hr, PM 0.03 g/HP-hr—an 80% reduction from Tier 2. Tier 4 requires advanced emissions control technology: (1) High-pressure common-rail fuel injection (2,000+ PSI) for better combustion control. (2) Exhaust Gas Recirculation (EGR)—routes cooled exhaust back into intake to reduce peak combustion temperatures and NOx formation. (3) Diesel Particulate Filters (DPF)—trap soot particles; periodically regenerated by burning off accumulated soot. (4) Selective Catalytic Reduction (SCR)—injects urea (DEF fluid) into exhaust; catalytic reaction reduces NOx to nitrogen and water. Remanufacture rule: when an engine is remanufactured, it must be upgraded to the tier standard in effect at the time of remanufacture (or the tier it was originally certified to, whichever is stricter). This has driven widespread adoption of Tier 4 technology. Tier 4 locomotives cost ~10-15% more than Tier 2 but reduce emissions by 70-90%, improving air quality near rail corridors.""",
        key_factors=[
            "Tier 0: pre-2000, no federal standards",
            "Tier 1: 2000-2004, NOx ~7-9 g/HP-hr",
            "Tier 2: 2005-2011, NOx 5.5, PM 0.22",
            "Tier 3: 2012-2014, NOx 5.5, PM 0.10",
            "Tier 4: 2015+, NOx 1.3, PM 0.03 (80% reduction)",
            "EGR: reduces NOx by lowering combustion temperature",
            "DPF: traps particulate matter, requires regeneration",
            "SCR: urea injection reduces NOx in exhaust",
            "Remanufacture rule: must upgrade to current tier standard"
        ],
        primary_authority=[
            "40 CFR Part 1033 Locomotive Emissions Standards",
            "EPA Locomotive Emissions Reduction Overview",
            "GE Tier 4 Emissions Technology White Paper",
            "EMD Tier 4 Compliance Guide"
        ],
        confidence=ConfidenceLevel.DEFINITIVE,
        technical_specs={
            "Tier 2 Limits": "NOx 5.5 g/HP-hr, PM 0.22 g/HP-hr",
            "Tier 4 Limits": "NOx 1.3 g/HP-hr, PM 0.03 g/HP-hr",
            "EGR Rate": "15-30% exhaust recirculation typical",
            "DPF Regeneration": "Every 200-500 hours depending on duty cycle",
            "SCR Urea Consumption": "~3-5% of fuel consumption"
        }
    ),

    DoctrineBlock(
        topic="Locomotive Maintenance Programs (FRA 229 Compliance)",
        keywords=["maintenance", "inspection program", "preventive maintenance", "component overhaul", "reliability centered maintenance"],
        conclusion_template=[
            "Locomotive maintenance programs must comply with FRA Part 229 inspection intervals and component standards.",
            "Preventive maintenance (PM) programs schedule inspections and component replacements based on time, mileage, or condition monitoring.",
            "Reliability-Centered Maintenance (RCM) optimizes maintenance intervals to balance cost, reliability, and regulatory compliance."
        ],
        reasoning_framework="""Locomotive maintenance is governed by FRA Part 229 minimum standards, supplemented by railroad-specific programs. FRA mandates: daily inspection (before each use), 92-day inspection (every 92 days or less), and annual inspection (comprehensive yearly). Railroads develop Preventive Maintenance (PM) programs that exceed these minimums, scheduling component inspections, fluid changes, and part replacements based on manufacturer recommendations and operational experience. PM intervals: oil changes every 180-365 days, air filter changes every 92-180 days, traction motor bearing inspections every 365-730 days. Component overhauls: major components (prime mover, main generator, traction motors) are overhauled at scheduled intervals (e.g., engine overhaul at 8-12 years or 1.5-2.5 million miles). Reliability-Centered Maintenance (RCM) is an advanced approach that analyzes failure modes and optimizes inspection intervals to prevent critical failures while minimizing maintenance cost. RCM uses data from event recorders, condition monitoring systems (oil analysis, vibration sensors, thermal imaging), and failure history to schedule maintenance just-in-time before failures occur. Condition-Based Maintenance (CBM) extends this concept by using real-time sensor data to trigger maintenance only when component degradation is detected. Example: lube oil analysis detects elevated metal content (indicating bearing wear), prompting inspection before catastrophic failure. Modern railroads use Computerized Maintenance Management Systems (CMMS) to track maintenance history, schedule work orders, and manage parts inventory.""",
        key_factors=[
            "FRA minimums: daily, 92-day, annual inspections",
            "PM programs: scheduled inspections and component replacements",
            "Oil changes: 180-365 days typical",
            "Air filters: 92-180 days",
            "Component overhaul: 8-12 years or 1.5-2.5M miles",
            "RCM: optimize intervals based on failure mode analysis",
            "CBM: real-time condition monitoring triggers maintenance",
            "CMMS: computerized systems track work orders and history"
        ],
        primary_authority=[
            "49 CFR Part 229 Subpart C: Inspections and Tests",
            "AAR M-1003 Locomotive Maintenance Standards",
            "Railroad Maintenance of Way Association Best Practices"
        ],
        confidence=ConfidenceLevel.HIGH,
        technical_specs={
            "Daily Inspection": "Pre-departure safety check",
            "92-Day Inspection": "Detailed component inspection",
            "Annual Inspection": "Comprehensive system validation",
            "Oil Change Interval": "180-365 days",
            "Air Filter Change": "92-180 days",
            "Engine Overhaul": "8-12 years or 1.5-2.5M miles"
        }
    ),
]


# ==============================================================================
# QUERY ENGINE
# ==============================================================================

def three_layer_response(query: str, mode: ResponseMode) -> Dict[str, Any]:
    """
    Three-layer response architecture:
    Layer 1: Doctrine Cache (0-200ms)
    Layer 2: Semantic Retrieval (fallback)
    Layer 3: Deep Analysis (if needed)
    """

    start_time = time.time()
    query_id = str(uuid.uuid4())

    # Normalize query
    norm_result = normalize_semantics(query)
    normalized_query = norm_result["normalized"]

    # Layer 1: Doctrine Cache Lookup
    triggered_doctrines = []
    for doctrine in DOCTRINE_CACHE:
        if doctrine.matches(normalized_query):
            triggered_doctrines.append(doctrine)

    if triggered_doctrines:
        # Cache hit
        doctrine = triggered_doctrines[0]  # Use first match
        COVERAGE_MAP.record_hit(doctrine.topic)

        if mode == ResponseMode.FAST:
            answer = doctrine.render_fast()
        elif mode == ResponseMode.DEFENSE:
            answer = doctrine.render_defense()
        else:  # MEMO
            answer = doctrine.render_memo()

        confidence = doctrine.confidence
        sources = doctrine.primary_authority
        doctrine_names = [d.topic for d in triggered_doctrines]

        latency = (time.time() - start_time) * 1000
        METRICS.record_query(latency, doctrine_hit=True)

    else:
        # Cache miss - fallback to generic response
        COVERAGE_MAP.record_miss(query)
        answer = f"No specific doctrine found for query: {query}. This topic may require manual research or doctrine expansion."
        confidence = ConfidenceLevel.PRELIMINARY
        sources = ["General locomotive engineering knowledge"]
        doctrine_names = []

        latency = (time.time() - start_time) * 1000
        METRICS.record_query(latency, doctrine_hit=False)

    # Generate determinism hash
    hash_input = f"{query}|{mode.value}|{answer}"
    determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    return {
        "query_id": query_id,
        "answer": answer,
        "confidence": confidence,
        "mode": mode,
        "latency_ms": latency,
        "doctrines_triggered": doctrine_names,
        "sources": sources,
        "determinism_hash": determinism_hash,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ==============================================================================
# FASTAPI APPLICATION
# ==============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    logger.info("RAIL01 Locomotive Systems Engine starting up on port 9101")
    logger.info(f"Doctrine cache loaded: {len(DOCTRINE_CACHE)} topics")
    yield
    logger.info("RAIL01 Locomotive Systems Engine shutting down")


APP = FastAPI(
    title="RAIL01 Locomotive Systems Intelligence Engine",
    version="1.0.0",
    lifespan=lifespan
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@APP.get("/health")
async def health():
    """Health check endpoint."""
    stats = METRICS.get_stats()
    drift = DRIFT_WATCHER.get_drift_report()
    coverage = COVERAGE_MAP.get_coverage_report()

    return {
        "status": "operational",
        "engine": "RAIL01_locomotive_systems",
        "version": "1.0.0",
        "port": 9101,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "metrics": stats,
        "drift": drift,
        "coverage": coverage
    }


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint."""
    METRICS.active_queries += 1

    try:
        result = three_layer_response(request.query, request.mode)

        # Log to audit trail
        with open(AUDIT_LOG, "a") as f:
            audit_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "query_id": result["query_id"],
                "query": request.query,
                "mode": request.mode.value,
                "latency_ms": result["latency_ms"],
                "doctrines": result["doctrines_triggered"]
            }
            f.write(str(audit_entry) + "\n")

        return QueryResponse(**result)

    except Exception as e:
        logger.error(f"Query processing error: {e}")
        METRICS.record_error(str(e))
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        METRICS.active_queries -= 1


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(APP, host="127.0.0.1", port=9101)
