import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import uuid
import dataclasses
import typing
import enum
import datetime
import asyncio
import aiohttp
import json
import time
import statistics
import collections

from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
from loguru import logger

# Engine constants
ENGINE_ID = "AEROIE"
ENGINE_PORT = 8859
ENGINE_NAME = "Aerospace Intelligence Engine — Domain Orchestrator"
ENGINE_VERSION = "1.0.0"

# Enums
class ResponseMode(enum.Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class PositionZone(enum.Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class ConfidenceZone(enum.Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(enum.Enum):
    AERODYNAMICS = "AERODYNAMICS"
    PROPULSION = "PROPULSION"
    STRUCTURES = "STRUCTURES"
    AVIONICS = "AVIONICS"
    FLIGHT_MECHANICS = "FLIGHT_MECHANICS"
    AIRCRAFT_DESIGN = "AIRCRAFT_DESIGN"
    SPACE_SYSTEMS = "SPACE_SYSTEMS"
    MATERIALS_AEROSPACE = "MATERIALS_AEROSPACE"
    MAINTENANCE_MRO = "MAINTENANCE_MRO"
    AIR_TRAFFIC_MANAGEMENT = "AIR_TRAFFIC_MANAGEMENT"
    SYSTEMS_INTEGRATION = "SYSTEMS_INTEGRATION"
    SAFETY = "SAFETY"
    REGULATORY_COMPLIANCE = "REGULATORY_COMPLIANCE"
    PERFORMANCE = "PERFORMANCE"
    ENVIRONMENTAL_IMPACT = "ENVIRONMENTAL_IMPACT"
    COST_ANALYSIS = "COST_ANALYSIS"
    MANUFACTURING = "MANUFACTURING"
    TESTING = "TESTING"
    FAILURE_ANALYSIS = "FAILURE_ANALYSIS"
    RELIABILITY = "RELIABILITY"
    MAINTAINABILITY = "MAINTAINABILITY"
    HUMAN_FACTORS = "HUMAN_FACTORS"
    CERTIFICATION = "CERTIFICATION"
    SUPPLY_CHAIN = "SUPPLY_CHAIN"
    QUALITY_ASSURANCE = "QUALITY_ASSURANCE"

class SubEngineStatus(enum.Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

# Pydantic Models
class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    query_text: str
    domain: str
    response_mode: ResponseMode = ResponseMode.FAST
    position_zone: PositionZone = PositionZone.PLANNING
    confidence_zone: ConfidenceZone = ConfidenceZone.DEFENSIBLE
    issue_category: IssueCategory = IssueCategory.AERODYNAMICS
    metadata: typing.Optional[dict] = None

    @validator('timestamp', pre=True, always=True)
    def ensure_datetime(cls, v):
        if isinstance(v, str):
            return datetime.datetime.fromisoformat(v)
        return v

class QueryResponse(BaseModel):
    query_id: str
    engine_id: str
    response: str
    status: str
    confidence_score: float
    latency_ms: int
    sub_engine_id: str
    orchestration_trace: typing.Optional[list] = None
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    metadata: typing.Optional[dict] = None

class SubEngineConfig(BaseModel):
    engine_id: str
    name: str
    port: int
    health_url: str
    capabilities: typing.List[str]
    weight: float
    domains: typing.List[str]
    status: SubEngineStatus = SubEngineStatus.UNKNOWN

class RoutingDecision(BaseModel):
    query_id: str
    domain: str
    engine_id: str
    sub_engine_name: str
    rule_applied: str
    confidence: float
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    metadata: typing.Optional[dict] = None

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decisions: typing.List[RoutingDecision]
    responses: typing.List[QueryResponse]
    overall_status: str
    orchestration_latency_ms: int
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    metadata: typing.Optional[dict] = None

# Sub-engine registry
SUB_ENGINE_REGISTRY = {
    "AERO01": SubEngineConfig(
        engine_id="AERO01",
        name="Aerodynamics",
        port=8861,
        health_url="http://localhost:8861/health",
        capabilities=["lift", "drag", "flow", "CFD", "wind tunnel", "boundary layer", "aeroelasticity", "stall", "turbulence"],
        weight=1.0,
        domains=["aerodynamics", "flow", "CFD", "lift", "drag", "stall", "turbulence"]
    ),
    "AERO02": SubEngineConfig(
        engine_id="AERO02",
        name="Propulsion",
        port=8862,
        health_url="http://localhost:8862/health",
        capabilities=["engine", "thrust", "fuel", "combustion", "jet", "propeller", "nozzle", "turbo", "rocket"],
        weight=1.0,
        domains=["propulsion", "engine", "thrust", "combustion", "fuel", "jet", "rocket", "nozzle"]
    ),
    "AERO03": SubEngineConfig(
        engine_id="AERO03",
        name="Structures",
        port=8863,
        health_url="http://localhost:8863/health",
        capabilities=["stress", "strain", "fatigue", "composite", "metal", "frame", "fuselage", "wing", "buckling"],
        weight=1.0,
        domains=["structures", "stress", "strain", "fatigue", "composite", "frame", "fuselage", "wing", "buckling"]
    ),
    "AERO04": SubEngineConfig(
        engine_id="AERO04",
        name="Avionics",
        port=8864,
        health_url="http://localhost:8864/health",
        capabilities=["sensor", "radar", "navigation", "communication", "autopilot", "flight control", "electronics"],
        weight=1.0,
        domains=["avionics", "sensor", "radar", "navigation", "communication", "autopilot", "flight control", "electronics"]
    ),
    "AERO05": SubEngineConfig(
        engine_id="AERO05",
        name="Flight Mechanics",
        port=8865,
        health_url="http://localhost:8865/health",
        capabilities=["trajectory", "performance", "stability", "control", "maneuver", "dynamics", "simulation"],
        weight=1.0,
        domains=["flight mechanics", "trajectory", "performance", "stability", "control", "maneuver", "dynamics", "simulation"]
    ),
    "AERO06": SubEngineConfig(
        engine_id="AERO06",
        name="Aircraft Design",
        port=8866,
        health_url="http://localhost:8866/health",
        capabilities=["configuration", "layout", "sizing", "optimization", "requirements", "trade study", "concept"],
        weight=1.0,
        domains=["aircraft design", "configuration", "layout", "sizing", "optimization", "requirements", "trade study", "concept"]
    ),
    "AERO07": SubEngineConfig(
        engine_id="AERO07",
        name="Space Systems",
        port=8867,
        health_url="http://localhost:8867/health",
        capabilities=["satellite", "orbital", "launch", "spacecraft", "payload", "mission", "propulsion", "thermal"],
        weight=1.0,
        domains=["space systems", "satellite", "orbital", "launch", "spacecraft", "payload", "mission", "propulsion", "thermal"]
    ),
    "AERO08": SubEngineConfig(
        engine_id="AERO08",
        name="Materials Aerospace",
        port=8868,
        health_url="http://localhost:8868/health",
        capabilities=["material", "alloy", "composite", "ceramic", "polymer", "testing", "failure", "properties"],
        weight=1.0,
        domains=["materials aerospace", "material", "alloy", "composite", "ceramic", "polymer", "testing", "failure", "properties"]
    ),
    "AERO09": SubEngineConfig(
        engine_id="AERO09",
        name="Maintenance MRO",
        port=8869,
        health_url="http://localhost:8869/health",
        capabilities=["maintenance", "repair", "operations", "inspection", "logistics", "downtime", "schedule", "spare"],
        weight=1.0,
        domains=["maintenance mro", "maintenance", "repair", "operations", "inspection", "logistics", "downtime", "schedule", "spare"]
    ),
    "AERO10": SubEngineConfig(
        engine_id="AERO10",
        name="Air Traffic Management",
        port=8870,
        health_url="http://localhost:8870/health",
        capabilities=["traffic", "control", "ATC", "airspace", "routing", "flight plan", "coordination", "safety"],
        weight=1.0,
        domains=["air traffic management", "traffic", "control", "ATC", "airspace", "routing", "flight plan", "coordination", "safety"]
    ),
}

# Routing rules (domain keyword to engine_id mapping)
ROUTING_RULES = {
    "lift": "AERO01",
    "drag": "AERO01",
    "flow": "AERO01",
    "CFD": "AERO01",
    "wind tunnel": "AERO01",
    "boundary layer": "AERO01",
    "aeroelasticity": "AERO01",
    "stall": "AERO01",
    "turbulence": "AERO01",
    "engine": "AERO02",
    "thrust": "AERO02",
    "fuel": "AERO02",
    "combustion": "AERO02",
    "jet": "AERO02",
    "propeller": "AERO02",
    "nozzle": "AERO02",
    "turbo": "AERO02",
    "rocket": "AERO02",
    "stress": "AERO03",
    "strain": "AERO03",
    "fatigue": "AERO03",
    "composite": "AERO03",
    "metal": "AERO03",
    "frame": "AERO03",
    "fuselage": "AERO03",
    "wing": "AERO03",
    "buckling": "AERO03",
    "sensor": "AERO04",
    "radar": "AERO04",
    "navigation": "AERO04",
    "communication": "AERO04",
    "autopilot": "AERO04",
    "flight control": "AERO04",
    "electronics": "AERO04",
    "trajectory": "AERO05",
    "performance": "AERO05",
    "stability": "AERO05",
    "control": "AERO05",
    "maneuver": "AERO05",
    "dynamics": "AERO05",
    "simulation": "AERO05",
    "configuration": "AERO06",
    "layout": "AERO06",
    "sizing": "AERO06",
    "optimization": "AERO06",
    "requirements": "AERO06",
    "trade study": "AERO06",
    "concept": "AERO06",
    "satellite": "AERO07",
    "orbital": "AERO07",
    "launch": "AERO07",
    "spacecraft": "AERO07",
    "payload": "AERO07",
    "mission": "AERO07",
    "thermal": "AERO07",
    "material": "AERO08",
    "alloy": "AERO08",
    "ceramic": "AERO08",
    "polymer": "AERO08",
    "testing": "AERO08",
    "failure": "AERO08",
    "properties": "AERO08",
    "maintenance": "AERO09",
    "repair": "AERO09",
    "operations": "AERO09",
    "inspection": "AERO09",
    "logistics": "AERO09",
    "downtime": "AERO09",
    "schedule": "AERO09",
    "spare": "AERO09",
    "traffic": "AERO10",
    "ATC": "AERO10",
    "airspace": "AERO10",
    "routing": "AERO10",
    "flight plan": "AERO10",
    "coordination": "AERO10",
    "safety": "AERO10",
    # Expanded rules (sample, up to 200+)
    "vortex": "AERO01",
    "pressure distribution": "AERO01",
    "laminar flow": "AERO01",
    "turbulent flow": "AERO01",
    "Mach number": "AERO01",
    "Reynolds number": "AERO01",
    "shock wave": "AERO01",
    "supersonic": "AERO01",
    "subsonic": "AERO01",
    "compressibility": "AERO01",
    "afterburner": "AERO02",
    "fuel efficiency": "AERO02",
    "engine cycle": "AERO02",
    "turbofan": "AERO02",
    "turboprop": "AERO02",
    "ramjet": "AERO02",
    "scramjet": "AERO02",
    "oxidizer": "AERO02",
    "propellant": "AERO02",
    "engine failure": "AERO02",
    "structural integrity": "AERO03",
    "load path": "AERO03",
    "shear": "AERO03",
    "torsion": "AERO03",
    "bending": "AERO03",
    "joint": "AERO03",
    "riveting": "AERO03",
    "welding": "AERO03",
    "damage tolerance": "AERO03",
    "crack propagation": "AERO03",
    "inertial navigation": "AERO04",
    "GPS": "AERO04",
    "data link": "AERO04",
    "transponder": "AERO04",
    "flight data recorder": "AERO04",
    "weather radar": "AERO04",
    "sensor fusion": "AERO04",
    "actuator": "AERO04",
    "servo": "AERO04",
    "flight envelope": "AERO05",
    "turn rate": "AERO05",
    "climb rate": "AERO05",
    "glide slope": "AERO05",
    "pitch": "AERO05",
    "yaw": "AERO05",
    "roll": "AERO05",
    "autopilot logic": "AERO05",
    "mission profile": "AERO06",
    "payload capacity": "AERO06",
    "range": "AERO06",
    "endurance": "AERO06",
    "weight estimation": "AERO06",
    "cost trade": "AERO06",
    "design optimization": "AERO06",
    "launch vehicle": "AERO07",
    "re-entry": "AERO07",
    "space debris": "AERO07",
    "orbital mechanics": "AERO07",
    "thermal protection": "AERO07",
    "solar array": "AERO07",
    "attitude control": "AERO07",
    "radiation shielding": "AERO07",
    "carbon fiber": "AERO08",
    "titanium": "AERO08",
    "aluminum": "AERO08",
    "glass fiber": "AERO08",
    "resin": "AERO08",
    "surface treatment": "AERO08",
    "material fatigue": "AERO08",
    "NDT": "AERO08",
    "scheduled maintenance": "AERO09",
    "unscheduled maintenance": "AERO09",
    "inspection interval": "AERO09",
    "spare parts": "AERO09",
    "maintenance log": "AERO09",
    "repair order": "AERO09",
    "fleet management": "AERO09",
    "maintenance cost": "AERO09",
    "runway": "AERO10",
    "approach": "AERO10",
    "departure": "AERO10",
    "holding pattern": "AERO10",
    "airspace sector": "AERO10",
    "controller": "AERO10",
    "flight schedule": "AERO10",
    "NOTAM": "AERO10",
    "wake turbulence": "AERO10",
    "collision avoidance": "AERO10",
    "emergency": "AERO10",
    "weather impact": "AERO10",
    "capacity": "AERO10",
    "slot allocation": "AERO10",
    "system integration": "AERO04",
    "regulatory compliance": "AERO06",
    "certification": "AERO06",
    "safety audit": "AERO10",
    "failure analysis": "AERO03",
    "reliability": "AERO03",
    "maintainability": "AERO09",
    "human factors": "AERO06",
    "quality assurance": "AERO08",
    "supply chain": "AERO09",
    "manufacturing": "AERO08",
    "testing": "AERO08",
    "cost analysis": "AERO06",
    "environmental impact": "AERO06",
    "performance analysis": "AERO05",
    "flight simulation": "AERO05",
    "mission simulation": "AERO07",
    "thermal analysis": "AERO07",
    "payload integration": "AERO07",
    "mission planning": "AERO07",
    "space mission": "AERO07",
    "space launch": "AERO07",
    "flight test": "AERO05",
    "flight certification": "AERO06",
    "flight safety": "AERO10",
    "flight operations": "AERO09",
    "flight monitoring": "AERO10",
    "flight data": "AERO04",
    "flight control system": "AERO04",
    "flight management": "AERO10",
    "flight scheduling": "AERO10",
    "flight coordination": "AERO10",
    "flight reporting": "AERO10",
    "flight audit": "AERO10",
    "flight envelope protection": "AERO05",
    "flight dynamics": "AERO05",
    "flight stability": "AERO05",
    "flight performance": "AERO05",
    "flight optimization": "AERO06",
    "flight design": "AERO06",
    "flight maintenance": "AERO09",
    "flight reliability": "AERO03",
    "flight quality": "AERO08",
    "flight materials": "AERO08",
    "flight structures": "AERO03",
    "flight propulsion": "AERO02",
    "flight aerodynamics": "AERO01",
    "flight avionics": "AERO04",
    "flight mechanics": "AERO05",
    "flight systems": "AERO04",
    "flight integration": "AERO04",
    "flight certification audit": "AERO06",
    "flight regulatory": "AERO06",
    "flight compliance": "AERO06",
    "flight safety audit": "AERO10",
    "flight supply chain": "AERO09",
    "flight manufacturing": "AERO08",
    "flight testing": "AERO08",
    "flight cost": "AERO06",
    "flight environmental": "AERO06",
    "flight failure": "AERO03",
    "flight maintainability": "AERO09",
    "flight human factors": "AERO06",
    "flight quality assurance": "AERO08",
    "flight supply": "AERO09",
    "flight logistics": "AERO09",
    "flight downtime": "AERO09",
    "flight inspection": "AERO09",
    "flight repair": "AERO09",
    "flight operations audit": "AERO09",
    "flight spare": "AERO09",
    "flight schedule audit": "AERO10",
    "flight slot allocation": "AERO10",
    "flight capacity": "AERO10",
    "flight emergency": "AERO10",
    "flight collision avoidance": "AERO10",
    "flight wake turbulence": "AERO10",
    "flight NOTAM": "AERO10",
    "flight controller": "AERO10",
    "flight airspace": "AERO10",
    "flight runway": "AERO10",
    "flight approach": "AERO10",
    "flight departure": "AERO10",
    "flight holding pattern": "AERO10",
    "flight airspace sector": "AERO10",
    "flight data recorder": "AERO04",
    "flight weather radar": "AERO04",
    "flight sensor fusion": "AERO04",
    "flight actuator": "AERO04",
    "flight servo": "AERO04",
    "flight autopilot logic": "AERO05",
    "flight mission profile": "AERO06",
    "flight payload capacity": "AERO06",
    "flight range": "AERO06",
    "flight endurance": "AERO06",
    "flight weight estimation": "AERO06",
    "flight cost trade": "AERO06",
    "flight design optimization": "AERO06",
    "flight launch vehicle": "AERO07",
    "flight re-entry": "AERO07",
    "flight space debris": "AERO07",
    "flight orbital mechanics": "AERO07",
    "flight thermal protection": "AERO07",
    "flight solar array": "AERO07",
    "flight attitude control": "AERO07",
    "flight radiation shielding": "AERO07",
    "flight carbon fiber": "AERO08",
    "flight titanium": "AERO08",
    "flight aluminum": "AERO08",
    "flight glass fiber": "AERO08",
    "flight resin": "AERO08",
    "flight surface treatment": "AERO08",
    "flight material fatigue": "AERO08",
    "flight NDT": "AERO08",
    "flight scheduled maintenance": "AERO09",
    "flight unscheduled maintenance": "AERO09",
    "flight inspection interval": "AERO09",
    "flight spare parts": "AERO09",
    "flight maintenance log": "AERO09",
    "flight repair order": "AERO09",
    "flight fleet management": "AERO09",
    "flight maintenance cost": "AERO09",
    # ... (continue for all domain keywords, up to 200+)
}

# Metrics Collector
class MetricsCollector:
    def __init__(self):
        self.query_times = collections.deque(maxlen=10000)
        self.error_times = collections.deque(maxlen=10000)
        self.latencies = collections.deque(maxlen=10000)
        self.query_records = collections.defaultdict(list)
        self.error_records = collections.defaultdict(list)
        self.last_hour_queries = collections.deque(maxlen=3600)
        self.lock = asyncio.Lock()

    async def record_query(self, query_id: str, timestamp: datetime.datetime, latency_ms: int):
        async with self.lock:
            self.query_times.append((query_id, timestamp))
            self.latencies.append(latency_ms)
            self.last_hour_queries.append((query_id, timestamp))
            self.query_records[query_id].append({
                "timestamp": timestamp,
                "latency_ms": latency_ms
            })

    async def record_error(self, query_id: str, timestamp: datetime.datetime, error_msg: str):
        async with self.lock:
            self.error_times.append((query_id, timestamp))
            self.error_records[query_id].append({
                "timestamp": timestamp,
                "error_msg": error_msg
            })

    def get_latency_stats(self):
        latencies = list(self.latencies)
        if not latencies:
            return {"mean": 0, "median": 0, "stdev": 0, "min": 0, "max": 0}
        return {
            "mean": statistics.mean(latencies),
            "median": statistics.median(latencies),
            "stdev": statistics.stdev(latencies) if len(latencies) > 1 else 0,
            "min": min(latencies),
            "max": max(latencies)
        }

    def queries_last_hour(self):
        now = datetime.datetime.utcnow()
        one_hour_ago = now - datetime.timedelta(hours=1)
        return [q for q, ts in self.last_hour_queries if ts >= one_hour_ago]

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
    confidence: float
    confidence_zone: str
    controlling_precedent: str

DOCTRINE_CACHE: List[DoctrineBlock] = [

    DoctrineBlock(
        topic="Aerodynamics Lift Generation",
        keywords=["lift", "Bernoulli", "airfoil", "pressure differential", "angle of attack", "boundary layer", "circulation", "Newton's third law"],
        conclusion_template=(
            "Lift on an airfoil is primarily generated through a combination of pressure differentials "
            "across the wing surfaces and the deflection of airflow downward. The Bernoulli principle "
            "explains the pressure variation, while Newton's third law accounts for the reaction force "
            "due to airflow deflection. Accurate prediction of lift requires consideration of boundary "
            "layer behavior and angle of attack."
        ),
        reasoning_framework=(
            "The generation of lift on an airfoil is a fundamental aerodynamic phenomenon governed by fluid "
            "dynamics principles. Bernoulli's equation describes how an increase in flow velocity over the "
            "upper surface of the wing reduces pressure relative to the lower surface, creating a net upward "
            "force. However, this explanation alone is insufficient; the Kutta condition ensures smooth flow "
            "leaving the trailing edge, establishing circulation around the airfoil. Newton's third law "
            "provides a complementary perspective: the wing deflects air downwards, and the reaction force "
            "pushes the wing upwards. The boundary layer's state (laminar or turbulent) affects flow separation "
            "and stall onset, influencing lift magnitude and stability. Angle of attack changes alter the "
            "effective camber and flow attachment, directly impacting lift coefficient. Empirical data and "
            "wind tunnel testing validate these theories, with computational fluid dynamics (CFD) offering "
            "high-fidelity predictions. The integration of these principles is essential for aircraft design, "
            "performance optimization, and flight safety."
        ),
        key_factors=[
            "Pressure differential between upper and lower wing surfaces",
            "Flow velocity distribution and Bernoulli effect",
            "Angle of attack and stall angle",
            "Boundary layer characteristics and flow separation",
            "Circulation and Kutta condition enforcement",
            "Newton's third law and downward momentum imparted to air",
            "Airfoil geometry and camber",
            "Reynolds number effects"
        ],
        primary_authority=[
            "Anderson, J.D., 'Fundamentals of Aerodynamics', 6th Edition, McGraw-Hill, 2016",
            "Abbott, I.H. and Doenhoff, A.E., 'Theory of Wing Sections', Dover Publications, 1959",
            "NASA SP-367, 'Introduction to Flight', 8th Edition, 2015",
            "FAA Advisory Circular AC 25-7D, 'Flight Test Guide for Certification of Transport Category Airplanes', 2017",
            "Houghton, E.L. and Carpenter, P.W., 'Aerodynamics for Engineering Students', 6th Edition, 2017"
        ],
        burden_holder="Aircraft aerodynamicist and flight test engineer",
        adversary_position=(
            "Lift is solely explained by Bernoulli's principle without considering Newtonian mechanics or "
            "boundary layer effects; angle of attack effects are negligible at normal flight conditions."
        ),
        counter_arguments=[
            "Bernoulli's principle alone cannot explain lift at zero angle of attack or stalled conditions.",
            "Newton's third law provides a necessary force balance perspective missing in Bernoulli-only views.",
            "Boundary layer separation drastically changes lift characteristics, which Bernoulli's principle does not address.",
            "Empirical data shows lift varies significantly with angle of attack, contradicting the adversary's claim.",
            "Modern CFD and wind tunnel results confirm the combined effect of pressure and momentum theories."
        ],
        resolution_strategy=(
            "Demonstrate through wind tunnel data, CFD simulations, and flight test results that lift generation "
            "is a multifaceted phenomenon requiring both Bernoulli and Newtonian explanations, supported by "
            "boundary layer theory and angle of attack considerations."
        ),
        entity_scope="Fixed-wing aircraft aerodynamic design and flight testing",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FAA FAR Part 25 Appendix C - Aerodynamic Data Requirements for Certification"
    ),

    DoctrineBlock(
        topic="Drag Components and Reduction Techniques",
        keywords=["drag", "parasite drag", "induced drag", "skin friction", "form drag", "wave drag", "drag reduction", "laminar flow"],
        conclusion_template=(
            "Aircraft drag consists of parasite and induced components, each influenced by different physical "
            "mechanisms. Effective drag reduction requires minimizing skin friction and form drag on surfaces, "
            "optimizing lift-to-drag ratio to reduce induced drag, and managing wave drag at transonic speeds."
        ),
        reasoning_framework=(
            "Drag on an aircraft arises from multiple sources: parasite drag, which includes skin friction, form, "
            "and interference drag, and induced drag, which is a byproduct of lift generation. Skin friction drag "
            "results from viscous shear stresses in the boundary layer and can be reduced by maintaining laminar "
            "flow or using smooth surface finishes. Form drag arises from pressure differentials caused by shape "
            "and bluff bodies; streamlined shapes reduce this component. Interference drag occurs where surfaces "
            "intersect, such as wing-fuselage junctions, and can be mitigated by fairings. Induced drag is related "
            "to wingtip vortices and increases with lift coefficient; winglets and optimized planforms reduce it. "
            "At transonic speeds, wave drag due to shock formation becomes significant; supercritical airfoils and "
            "area ruling help minimize this. Aerodynamicists employ computational methods and wind tunnel testing "
            "to quantify drag components and validate reduction strategies. These principles are codified in FAA "
            "certification standards and industry best practices."
        ),
        key_factors=[
            "Skin friction coefficient and boundary layer state",
            "Airfoil and fuselage shape and streamlining",
            "Lift coefficient and induced drag relationship",
            "Wingtip vortex strength and mitigation devices",
            "Mach number and wave drag onset",
            "Surface roughness and contamination effects",
            "Interference drag at component junctions",
            "Use of laminar flow control technologies"
        ],
        primary_authority=[
            "Torenbeek, E., 'Synthesis of Subsonic Airplane Design', Delft University Press, 1982",
            "Raymer, D.P., 'Aircraft Design: A Conceptual Approach', 6th Edition, AIAA, 2018",
            "FAA Advisory Circular AC 25-7D, 'Flight Test Guide for Certification of Transport Category Airplanes', 2017",
            "McCormick, B.W., 'Aerodynamics, Aeronautics, and Flight Mechanics', 2nd Edition, Wiley, 1995",
            "NASA TP-2004-213253, 'Drag Reduction Technologies for Commercial Transport Aircraft', 2004"
        ],
        burden_holder="Aerodynamicist and aircraft design engineer",
        adversary_position=(
            "Drag is predominantly caused by parasite drag; induced drag and wave drag are negligible or secondary."
        ),
        counter_arguments=[
            "Induced drag can constitute a significant portion of total drag at typical cruise lift coefficients.",
            "Wave drag dominates near and above critical Mach numbers, impacting high-speed aircraft performance.",
            "Parasite drag reduction alone cannot achieve optimal fuel efficiency without addressing induced drag.",
            "Wingtip devices demonstrably reduce induced drag and improve range and endurance.",
            "Empirical and CFD data confirm the multi-component nature of drag."
        ],
        resolution_strategy=(
            "Present comprehensive drag breakdown analyses from flight test data and CFD, showing the relative "
            "importance of each drag component and the effectiveness of reduction techniques."
        ),
        entity_scope="Subsonic and transonic fixed-wing aircraft aerodynamic design",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FAA FAR Part 25.101 - Flight Characteristics and Performance"
    ),

    DoctrineBlock(
        topic="Turbofan Engine Thermodynamics and Performance",
        keywords=["turbofan", "thermodynamic cycle", "bypass ratio", "compressor", "turbine", "specific fuel consumption", "thrust", "engine efficiency"],
        conclusion_template=(
            "Turbofan engines operate on the Brayton thermodynamic cycle with a high bypass ratio to maximize "
            "propulsive efficiency. Compressor and turbine stages optimize pressure and temperature ratios, "
            "balancing thrust output with fuel consumption and emissions."
        ),
        reasoning_framework=(
            "The turbofan engine is a complex thermodynamic system where air is drawn in and compressed by axial "
            "compressors, mixed with fuel in the combustion chamber, and expanded through turbines and a fan. The "
            "high bypass ratio characteristic of modern turbofans directs a large mass of air around the core, "
            "increasing thrust via momentum exchange with lower exhaust velocity, improving propulsive efficiency "
            "and reducing noise. The Brayton cycle describes the idealized thermodynamic process, with real engines "
            "incorporating component efficiencies, pressure losses, and temperature limits. Compressor pressure ratio "
            "and turbine inlet temperature are critical parameters influencing thermal efficiency and thrust. "
            "Specific fuel consumption (SFC) is a key performance metric, reflecting fuel efficiency relative to thrust. "
            "Advancements in materials and cooling technologies allow higher turbine inlet temperatures, enhancing "
            "performance. Emissions regulations and noise abatement also influence engine design. The FAA and ICAO "
            "provide certification standards governing engine performance and environmental compliance."
        ),
        key_factors=[
            "Bypass ratio and fan design",
            "Compressor pressure ratio and stage count",
            "Turbine inlet temperature and cooling",
            "Specific fuel consumption (SFC)",
            "Thrust-to-weight ratio",
            "Emissions and noise regulations",
            "Component efficiencies and losses",
            "Material temperature limits"
        ],
        primary_authority=[
            "Mattingly, J.D., 'Elements of Gas Turbine Propulsion', 2nd Edition, AIAA, 2006",
            "Turns, S.R., 'An Introduction to Combustion: Concepts and Applications', 3rd Edition, McGraw-Hill, 2012",
            "FAA Advisory Circular AC 33.75-1, 'Gas Turbine Engine Certification', 2016",
            "ICAO Annex 16, Volume II - Aircraft Engine Emissions, 2017",
            "Rolls-Royce plc, 'Turbofan Engine Technology Overview', Technical Paper, 2018"
        ],
        burden_holder="Engine manufacturer and propulsion engineer",
        adversary_position=(
            "Turbofan engines operate similarly to turbojets; bypass ratio and fan stages have minimal impact on efficiency."
        ),
        counter_arguments=[
            "High bypass ratio turbofans achieve significantly better propulsive efficiency than turbojets.",
            "Fan design and bypass flow reduce exhaust velocity, lowering fuel consumption and noise.",
            "Compressor and turbine stage optimization directly affect thermal efficiency and thrust.",
            "Empirical engine performance data confirm the importance of bypass ratio.",
            "Regulatory standards differentiate turbofan and turbojet certification requirements."
        ],
        resolution_strategy=(
            "Use thermodynamic cycle analysis, engine test data, and certification documentation to demonstrate "
            "the critical role of bypass ratio and component design in turbofan performance."
        ),
        entity_scope="Commercial and military turbofan engine design and certification",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA FAR Part 33 - Airworthiness Standards: Aircraft Engines"
    ),

    DoctrineBlock(
        topic="Monocoque and Semi-Monocoque Aircraft Structures",
        keywords=["monocoque", "semi-monocoque", "aircraft structures", "load distribution", "skin stress", "stringers", "frames", "fatigue"],
        conclusion_template=(
            "Monocoque and semi-monocoque structures provide the primary load-bearing framework of aircraft, "
            "with semi-monocoque designs balancing skin and internal reinforcements to optimize strength, "
            "weight, and damage tolerance."
        ),
        reasoning_framework=(
            "Aircraft structural design employs monocoque and semi-monocoque concepts to efficiently carry aerodynamic "
            "and inertial loads. Monocoque structures rely on the external skin to bear all loads, providing a lightweight "
            "but less damage-tolerant solution. Semi-monocoque structures incorporate internal supports such as stringers, "
            "frames, and bulkheads, distributing stresses between skin and internal members. This approach enhances "
            "structural integrity, damage tolerance, and fatigue resistance. Load paths are carefully analyzed using "
            "finite element methods to ensure stress concentrations are minimized. Material selection (aluminum alloys, "
            "titanium, composites) influences structural behavior and fatigue life. Damage tolerance requirements, "
            "including crack growth and fail-safe design, are critical for certification under FAA FAR Part 25. "
            "Inspection and maintenance programs are designed based on structural concepts to detect and mitigate fatigue "
            "and damage."
        ),
        key_factors=[
            "Load distribution between skin and internal members",
            "Material properties and fatigue characteristics",
            "Stringer and frame spacing and design",
            "Damage tolerance and fail-safe design principles",
            "Stress concentration and crack propagation",
            "Manufacturing processes and quality control",
            "Inspection intervals and nondestructive testing methods",
            "Certification requirements under FAR Part 25"
        ],
        primary_authority=[
            "Bruhn, E.F., 'Analysis and Design of Flight Vehicle Structures', 2nd Edition, Tri-State Offset Company, 1973",
            "FAA FAR Part 25 - Airworthiness Standards: Transport Category Airplanes",
            "MIL-HDBK-5J, 'Metallic Materials and Elements for Aerospace Vehicle Structures', 2016",
            "FAA Advisory Circular AC 43.13-1B, 'Acceptable Methods, Techniques, and Practices – Aircraft Inspection and Repair', 2008",
            "Niu, M.C.Y., 'Airframe Structural Design', Conmilit Press, 1999"
        ],
        burden_holder="Structural design engineer and maintenance organization",
        adversary_position=(
            "Monocoque structures are sufficient for all aircraft; internal reinforcements add unnecessary weight."
        ),
        counter_arguments=[
            "Semi-monocoque structures provide superior damage tolerance and fatigue resistance.",
            "Internal reinforcements distribute loads and prevent catastrophic failure from skin cracks.",
            "Certification standards require fail-safe design features not achievable with pure monocoque.",
            "Operational experience shows monocoque-only designs have limited fatigue life.",
            "Maintenance and inspection programs rely on semi-monocoque structural concepts."
        ],
        resolution_strategy=(
            "Present structural analysis, fatigue test data, and certification requirements demonstrating the necessity "
            "of semi-monocoque design for safe, durable aircraft."
        ),
        entity_scope="Fixed-wing aircraft primary structure design and maintenance",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FAA FAR Part 25.571 - Damage Tolerance and Fatigue Evaluation"
    ),

    DoctrineBlock(
        topic="Avionics Flight Management Systems (FMS)",
        keywords=["flight management system", "navigation", "performance optimization", "autopilot integration", "waypoint sequencing", "VNAV", "LNAV", "data link"],
        conclusion_template=(
            "Flight Management Systems integrate navigation, performance, and guidance functions to optimize "
            "flight trajectories, reduce pilot workload, and enhance safety through precise waypoint sequencing "
            "and autopilot interface."
        ),
        reasoning_framework=(
            "Flight Management Systems (FMS) are critical avionics components that automate and optimize flight operations. "
            "They integrate inputs from navigation sensors (GPS, inertial reference systems), performance databases, and "
            "aircraft systems to compute optimal flight paths, fuel consumption, and time estimates. The FMS interfaces "
            "with autopilot and flight director systems to execute lateral (LNAV) and vertical (VNAV) navigation commands. "
            "Waypoint sequencing and route management reduce pilot workload and enhance situational awareness. Performance "
            "optimization includes climb, cruise, and descent profiles tailored to aircraft weight, weather, and airspace "
            "constraints. Data link capabilities enable real-time updates and clearance delivery. Certification standards "
            "such as RTCA DO-178C and DO-254 govern software and hardware reliability. Human factors considerations ensure "
            "interface usability and error mitigation."
        ),
        key_factors=[
            "Navigation sensor integration and accuracy",
            "Performance database and optimization algorithms",
            "Autopilot and flight director coupling",
            "Waypoint management and route sequencing",
            "VNAV and LNAV guidance modes",
            "Human-machine interface design",
            "Software certification and reliability standards",
            "Data link and communication capabilities"
        ],
        primary_authority=[
            "RTCA DO-178C, 'Software Considerations in Airborne Systems and Equipment Certification', 2011",
            "RTCA DO-254, 'Design Assurance Guidance for Airborne Electronic Hardware', 2000",
            "FAA AC 20-138D, 'Airborne Software Assurance', 2017",
            "FAA AC 25.1322-1, 'Flight Management Systems', 2015",
            "Jeppesen Sanderson, 'FMS Operational Manual', 2019"
        ],
        burden_holder="Avionics system integrator and certification engineer",
        adversary_position=(
            "FMS functions can be replaced by manual pilot navigation without loss of safety or efficiency."
        ),
        counter_arguments=[
            "FMS reduces pilot workload and human error, improving safety and operational efficiency.",
            "Automated performance optimization reduces fuel consumption and emissions.",
            "Integration with autopilot enables precise adherence to ATC clearances and procedures.",
            "Certification standards require rigorous validation of FMS functionality.",
            "Operational data shows FMS reduces navigation errors and improves situational awareness."
        ],
        resolution_strategy=(
            "Demonstrate through operational data, certification documentation, and human factors studies the critical "
            "role of FMS in modern aircraft safety and efficiency."
        ),
        entity_scope="Commercial and business aircraft avionics systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA FAR Part 25.1322 - Flight Management Systems Requirements"
    ),

    DoctrineBlock(
        topic="Flight Mechanics Stability and Control",
        keywords=["flight mechanics", "stability", "control surfaces", "longitudinal stability", "lateral stability", "yaw control", "dynamic stability", "control effectiveness"],
        conclusion_template=(
            "Aircraft stability and control are governed by aerodynamic forces and moments acting on control surfaces, "
            "ensuring predictable and safe handling characteristics in all flight regimes."
        ),
        reasoning_framework=(
            "Flight mechanics studies the forces and moments acting on an aircraft and their effects on stability and control. "
            "Static stability ensures the aircraft returns to equilibrium after disturbance; longitudinal stability depends "
            "on the relative position of the center of gravity and aerodynamic center, typically managed by horizontal tail design. "
            "Lateral and directional stability involve dihedral effect, vertical tail size, and control surface effectiveness. "
            "Dynamic stability considers time-dependent response, including damping of oscillations such as phugoid and Dutch roll. "
            "Control surfaces (ailerons, elevators, rudders) provide pilot inputs to manage attitude and heading. Control effectiveness "
            "varies with airspeed, altitude, and configuration. Flight control laws and stability augmentation systems enhance handling. "
            "Certification requires demonstration of stability and control characteristics under FAR Part 25 standards."
        ),
        key_factors=[
            "Center of gravity location relative to aerodynamic center",
            "Tail volume coefficients and control surface sizing",
            "Static and dynamic stability derivatives",
            "Control surface deflection and hinge moments",
            "Damping characteristics of oscillatory modes",
            "Effect of configuration changes (flaps, gear)",
            "Flight control system augmentation",
            "Certification flight test requirements"
        ],
        primary_authority=[
            "Nelson, R.C., 'Flight Stability and Automatic Control', 2nd Edition, McGraw-Hill, 1998",
            "FAA FAR Part 25 - Airworthiness Standards: Transport Category Airplanes",
            "Roskam, J., 'Airplane Flight Dynamics and Automatic Flight Controls', DARcorporation, 2001",
            "MIL-F-8785C, 'Flying Qualities of Piloted Airplanes', 1980",
            "FAA Advisory Circular AC 25-7D, 'Flight Test Guide for Certification of Transport Category Airplanes', 2017"
        ],
        burden_holder="Flight test engineer and aerodynamicist",
        adversary_position=(
            "Stability and control are primarily pilot skill dependent; aerodynamic design has minimal impact."
        ),
        counter_arguments=[
            "Aerodynamic design directly affects stability margins and control responsiveness.",
            "Certification requires demonstration of stability and control characteristics independent of pilot skill.",
            "Flight control augmentation systems rely on predictable aerodynamic behavior.",
            "Poor stability characteristics increase pilot workload and risk of loss of control.",
            "Empirical flight test data validate aerodynamic stability and control theories."
        ],
        resolution_strategy=(
            "Use flight test data, aerodynamic modeling, and certification standards to confirm the essential role of "
            "stability and control design in safe aircraft operation."
        ),
        entity_scope="Fixed-wing aircraft flight mechanics and certification",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FAA FAR Part 25.171 - Controllability and Maneuverability"
    ),

    DoctrineBlock(
        topic="Aircraft Configuration: Wing, Fuselage, Empennage Integration",
        keywords=["aircraft configuration", "wing design", "fuselage", "empennage", "aerodynamic interference", "structural integration", "weight distribution", "control effectiveness"],
        conclusion_template=(
            "The integrated design of wing, fuselage, and empennage is critical to aircraft aerodynamic efficiency, "
            "structural integrity, and control performance, requiring careful management of interference effects and load paths."
        ),
        reasoning_framework=(
            "Aircraft configuration involves the spatial arrangement and integration of major components: wings, fuselage, "
            "and empennage (horizontal and vertical stabilizers). Aerodynamic interference effects arise where these components "
            "intersect, altering local flow fields and pressure distributions, potentially increasing drag or affecting control "
            "authority. Structural integration ensures load transfer between components without excessive weight penalties. "
            "Weight distribution affects center of gravity location, influencing stability and control. The empennage provides "
            "pitch and yaw stability and control, sized relative to wing geometry and expected flight envelope. Computational "
            "aerodynamics and wind tunnel testing quantify interference effects and optimize shapes. Certification standards "
            "require demonstration of structural integrity and control effectiveness of integrated configurations."
        ),
        key_factors=[
            "Aerodynamic interference drag and flow separation",
            "Load paths and structural joint design",
            "Weight and balance considerations",
            "Empennage sizing relative to wing planform",
            "Control surface effectiveness and redundancy",
            "Manufacturing and maintenance accessibility",
            "Certification requirements for structural and control integrity",
            "Computational and experimental validation methods"
        ],
        primary_authority=[
            "Raymer, D.P., 'Aircraft Design: A Conceptual Approach', 6th Edition, AIAA, 2018",
            "Torres, C., 'Aircraft Configuration Design', Wiley, 2015",
            "FAA FAR Part 25 - Airworthiness Standards: Transport Category Airplanes",
            "NASA TP-2006-214203, 'Aerodynamic Interference Effects in Transport Aircraft', 2006",
            "MIL-HDBK-17-1F, 'Composite Materials Handbook', 2012"
        ],
        burden_holder="Aircraft configuration and structural design engineers",
        adversary_position=(
            "Component integration has negligible effect on overall aircraft performance and can be treated independently."
        ),
        counter_arguments=[
            "Interference effects can increase drag and reduce control effectiveness if not properly managed.",
            "Structural integration impacts weight and fatigue life, affecting safety and efficiency.",
            "Weight distribution from component placement influences stability and control.",
            "Certification requires integrated system demonstration, not isolated component analysis.",
            "Empirical and CFD data confirm the importance of integrated design."
        ],
        resolution_strategy=(
            "Present integrated aerodynamic and structural analyses, supported by certification documentation, "
            "to demonstrate the necessity of coordinated configuration design."
        ),
        entity_scope="Fixed-wing aircraft preliminary and detailed design",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FAA FAR Part 25.301 - Strength Requirements"
    ),

    DoctrineBlock(
        topic="Orbital Mechanics: Keplerian Trajectories and Transfers",
        keywords=["orbital mechanics", "Kepler's laws", "trajectory", "Hohmann transfer", "delta-v", "orbital insertion", "gravity assist", "spacecraft maneuvering"],
        conclusion_template=(
            "Spacecraft trajectories are governed by Keplerian orbital mechanics, with transfer maneuvers such as Hohmann "
            "transfers and gravity assists optimizing delta-v requirements for orbital insertion and interplanetary travel."
        ),
        reasoning_framework=(
            "Orbital mechanics is the study of spacecraft motion under gravitational forces, primarily governed by Kepler's laws. "
            "Orbits are conic sections characterized by parameters such as semi-major axis, eccentricity, inclination, and period. "
            "Transfer maneuvers, including Hohmann transfers, bi-elliptic transfers, and gravity assists, enable efficient changes "
            "in orbit with minimal propellant use. Delta-v quantifies the velocity change required for maneuvers, directly impacting "
            "fuel consumption and mission feasibility. Orbital insertion requires precise timing and velocity matching to achieve "
            "stable orbits. Perturbations such as atmospheric drag, third-body effects, and non-spherical Earth gravity influence "
            "trajectory planning. Mission design integrates these principles with propulsion capabilities and spacecraft constraints. "
            "International standards and NASA procedural requirements govern mission planning and execution."
        ),
        key_factors=[
            "Orbital elements and Keplerian parameters",
            "Delta-v budget and propulsion system performance",
            "Transfer orbit selection and timing",
            "Gravity assist opportunities and constraints",
            "Perturbation effects and orbit maintenance",
            "Spacecraft mass and propulsion limitations",
            "Navigation and guidance precision",
            "Mission objectives and constraints"
        ],
        primary_authority=[
            "Bate, R.R., Mueller, D.D., and White, J.E., 'Fundamentals of Astrodynamics', Dover Publications, 1971",
            "Curtis, H.D., 'Orbital Mechanics for Engineering Students', 3rd Edition, Elsevier, 2014",
            "NASA SP-8013, 'NASA Systems Engineering Handbook', 2016",
            "NASA Procedural Requirements NPR 7120.5E, 'NASA Space Flight Program and Project Management Requirements', 2016",
            "Vallado, D.A., 'Fundamentals of Astrodynamics and Applications', 4th Edition, Microcosm Press, 2013"
        ],
        burden_holder="Mission design engineer and spacecraft navigation team",
        adversary_position=(
            "Orbital transfers can be approximated by simple velocity changes without detailed Keplerian analysis."
        ),
        counter_arguments=[
            "Keplerian mechanics provides accurate prediction of spacecraft trajectories essential for mission success.",
            "Ignoring orbital mechanics leads to inefficient fuel use and mission failure risks.",
            "Delta-v optimization is critical for payload capacity and mission cost.",
            "Gravity assists enable missions otherwise impossible with direct propulsion.",
            "Navigation and guidance systems rely on precise orbital calculations."
        ],
        resolution_strategy=(
            "Use mission simulation data, navigation logs, and propulsion performance analyses to validate the necessity "
            "of detailed orbital mechanics."
        ),
        entity_scope="Spacecraft mission planning and trajectory design",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="NASA NPR 8705.4 - Risk Classification for NASA Payloads"
    ),

    DoctrineBlock(
        topic="Aerospace Materials: Aluminum, Titanium, and Composite Usage",
        keywords=["aerospace materials", "aluminum alloys", "titanium alloys", "composites", "CFRP", "fatigue resistance", "corrosion", "material selection"],
        conclusion_template=(
            "Material selection in aerospace balances strength, weight, fatigue resistance, and corrosion properties, "
            "with aluminum alloys, titanium alloys, and carbon fiber reinforced polymers (CFRP) each offering distinct advantages."
        ),
        reasoning_framework=(
            "Aerospace materials are selected based on mechanical properties, environmental resistance, manufacturability, and cost. "
            "Aluminum alloys, such as 2024 and 7075, offer good strength-to-weight ratios and ease of fabrication but are susceptible "
            "to corrosion and fatigue. Titanium alloys provide superior strength, corrosion resistance, and high-temperature capability, "
            "at higher cost and manufacturing complexity. Composites, especially CFRP, offer exceptional strength-to-weight ratios and "
            "fatigue resistance, with anisotropic properties requiring careful design and quality control. Material behavior under cyclic "
            "loads, damage tolerance, and repairability influence selection. Certification standards such as MIL-HDBK-5J and FAA AC 20-107B "
            "guide material qualification and usage. Advances in composite manufacturing and hybrid structures continue to evolve aerospace "
            "material applications."
        ),
        key_factors=[
            "Mechanical strength and stiffness",
            "Fatigue life and crack propagation resistance",
            "Corrosion susceptibility and environmental durability",
            "Manufacturing processes and cost",
            "Thermal properties and high-temperature performance",
            "Damage tolerance and repairability",
            "Material anisotropy and design considerations",
            "Certification and qualification standards"
        ],
        primary_authority=[
            "MIL-HDBK-5J, 'Metallic Materials and Elements for Aerospace Vehicle Structures', 2016",
            "FAA AC 20-107B, 'Composite Aircraft Structure', 2013",
            "ASM International, 'Properties and Selection: Nonferrous Alloys and Special-Purpose Materials', 1990",
            "Gibson, R.F., 'Principles of Composite Material Mechanics', 3rd Edition, CRC Press, 2016",
            "Toray Industries, 'Carbon Fiber Composite Materials Technical Data', 2019"
        ],
        burden_holder="Materials engineer and structural design team",
        adversary_position=(
            "Traditional aluminum alloys remain the best choice for all aerospace structural applications."
        ),
        counter_arguments=[
            "Titanium alloys offer superior performance in high-temperature and corrosive environments.",
            "Composites provide unmatched strength-to-weight ratios and fatigue resistance.",
            "Modern aircraft increasingly rely on hybrid material systems for optimized performance.",
            "Certification standards recognize and regulate composite usage.",
            "Repair and inspection techniques have advanced to support composite structures."
        ],
        resolution_strategy=(
            "Present comparative material property data, certification guidance, and operational experience to justify "
            "material selection diversity."
        ),
        entity_scope="Aerospace structural materials selection and certification",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FAA FAR Part 25.603 - Materials and Parts"
    ),

    DoctrineBlock(
        topic="Maintenance, Repair, and Overhaul (MRO) Inspection and Documentation",
        keywords=["maintenance", "repair", "overhaul", "inspection", "airworthiness directives", "service bulletins", "scheduled maintenance", "non-destructive testing"],
        conclusion_template=(
            "Effective MRO programs rely on rigorous inspection protocols, adherence to airworthiness directives and service bulletins, "
            "and comprehensive documentation to ensure continued aircraft safety and regulatory compliance."
        ),
        reasoning_framework=(
            "Maintenance, Repair, and Overhaul (MRO) activities are essential to sustain aircraft airworthiness and operational readiness. "
            "Inspections are conducted at scheduled intervals based on flight hours, cycles, or calendar time, guided by manufacturer "
            "recommendations and regulatory requirements. Airworthiness Directives (ADs) issued by the FAA and other authorities mandate "
            "corrective actions for identified safety issues. Service Bulletins (SBs) provide manufacturer guidance for recommended "
            "maintenance and modifications. Non-destructive testing (NDT) methods such as ultrasonic, eddy current, and radiography "
            "detect structural and system defects without damage. Accurate record-keeping and traceability are mandated by regulations "
            "to document compliance and support continued certification. MRO organizations must maintain trained personnel, calibrated "
            "equipment, and quality assurance programs to meet FAA FAR Part 145 standards."
        ),
        key_factors=[
            "Scheduled inspection intervals and criteria",
            "Compliance with Airworthiness Directives (ADs)",
            "Implementation of Service Bulletins (SBs)",
            "Non-destructive testing (NDT) techniques",
            "Maintenance record accuracy and traceability",
            "Personnel training and certification",
            "Quality assurance and audit programs",
            "Regulatory compliance with FAA FAR Part 145"
        ],
        primary_authority=[
            "FAA FAR Part 145 - Repair Stations",
            "FAA FAR Part 43 - Maintenance, Preventive Maintenance, Rebuilding, and Alteration",
            "FAA Airworthiness Directives (AD) Database",
            "SAE ARP4754A, 'Guidelines for Development of Civil Aircraft and Systems', 2010",
            "ATA Spec 100 and iSpec 2200 - Maintenance Documentation Standards"
        ],
        burden_holder="MRO organization and maintenance personnel",
        adversary_position=(
            "Maintenance inspections and documentation are overly burdensome and do not significantly impact safety."
        ),
        counter_arguments=[
            "Regulatory data and accident investigations link maintenance compliance to safety outcomes.",
            "ADs and SBs address known safety risks and prevent failures.",
            "NDT methods detect hidden defects critical to structural integrity.",
            "Accurate documentation ensures traceability and accountability.",
            "Quality assurance programs reduce human error and improve reliability."
        ],
        resolution_strategy=(
            "Use safety data, regulatory mandates, and audit findings to demonstrate the essential role of MRO inspection "
            "and documentation."
        ),
        entity_scope="Commercial and general aviation maintenance programs",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FAA FAR Part 145 - Repair Station Certification"
    ),

    DoctrineBlock(
        topic="Air Traffic Management: ATC Separation and Surveillance",
        keywords=["air traffic management", "ATC", "separation standards", "radar surveillance", "ADS-B", "conflict detection", "traffic flow management", "controller workload"],
        conclusion_template=(
            "Air Traffic Management relies on established ATC separation standards and advanced surveillance technologies "
            "to maintain safe and efficient aircraft operations within controlled airspace."
        ),
        reasoning_framework=(
            "Air Traffic Control (ATC) ensures safe separation between aircraft through procedural and radar-based methods. "
            "Separation minima vary by airspace class, aircraft performance, and surveillance capabilities, defined by ICAO and "
            "FAA regulations. Radar surveillance provides real-time position data, enabling controllers to detect and resolve "
            "conflicts. Automatic Dependent Surveillance-Broadcast (ADS-B) enhances situational awareness and supports reduced "
            "separation standards. Traffic flow management balances demand and capacity, minimizing delays and congestion. "
            "Controller workload and human factors are critical considerations in system design and procedure development. "
            "Technological advancements such as NextGen and SESAR aim to improve surveillance accuracy and automation. "
            "Regulatory frameworks codify separation standards and operational procedures."
        ),
        key_factors=[
            "Separation minima and airspace classification",
            "Radar and ADS-B surveillance capabilities",
            "Conflict detection and resolution procedures",
            "Traffic flow management and slot allocation",
            "Controller workload and human factors",
            "Communication protocols and phraseology",
            "Technological modernization programs",
            "Regulatory standards (ICAO Annex 11, FAA Order JO 7110.65)"
        ],
        primary_authority=[
            "ICAO Annex 11 - Air Traffic Services, 2018",
            "FAA Order JO 7110.65, 'Air Traffic Control', 2023",
            "RTCA DO-260B, 'Minimum Operational Performance Standards for ADS-B', 2013",
            "FAA NextGen Implementation Plan, 2020",
            "EU SESAR Joint Undertaking Publications, 2019"
        ],
        burden_holder="Air traffic controllers and ATM system operators",
        adversary_position=(
            "Procedural separation alone is sufficient; advanced surveillance technologies add minimal safety benefit."
        ),
        counter_arguments=[
            "Surveillance technologies enable reduced separation minima, increasing airspace capacity.",
            "ADS-B improves situational awareness and conflict detection.",
            "Procedural separation is conservative and limits efficiency.",
            "Automation reduces controller workload and human error.",
            "Regulatory bodies mandate integration of modern surveillance systems."
        ],
        resolution_strategy=(
            "Present operational data, safety studies, and regulatory mandates supporting surveillance technology adoption "
            "and reduced separation standards."
        ),
        entity_scope="Controlled airspace and en route air traffic management",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FAA Order JO 7110.65 - Air Traffic Control"
    ),

    DoctrineBlock(
        topic="FAA Certification: FAR Part 25 and Part 23 Airworthiness Standards",
        keywords=["FAA certification", "FAR Part 25", "FAR Part 23", "airworthiness", "transport category", "normal category", "design standards", "compliance"],
        conclusion_template=(
            "FAA certification under FAR Part 25 and Part 23 establishes airworthiness standards for transport and normal category "
            "aircraft, ensuring safety through rigorous design, testing, and compliance verification."
        ),
        reasoning_framework=(
            "The FAA's Federal Aviation Regulations (FAR) Parts 23 and 25 define airworthiness standards for normal, utility, acrobatic, "
            "commuter, and transport category airplanes. Part 23 applies to smaller aircraft with maximum takeoff weights up to 19,000 "
            "lbs or nine passenger seats, focusing on prescriptive design and testing requirements. Part 25 governs larger transport "
            "category airplanes, emphasizing performance-based standards and comprehensive safety analyses. Certification involves design "
            "approval, compliance demonstration through analysis, testing, and flight trials, and continued operational safety monitoring. "
            "The regulations cover structural integrity, flight performance, systems reliability, occupant protection, and environmental "
            "considerations. Amendments and advisory circulars provide guidance on acceptable means of compliance. The certification process "
            "is iterative and involves coordination between manufacturers, FAA engineers, and test pilots."
        ),
        key_factors=[
            "Applicability criteria for Part 23 vs Part 25",
            "Structural and systems design requirements",
            "Flight performance and handling qualities",
            "Systems and equipment reliability",
            "Occupant safety and emergency provisions",
            "Environmental and noise standards",
            "Compliance demonstration methods",
            "Continued airworthiness and service monitoring"
        ],
        primary_authority=[
            "FAA FAR Part 23 - Airworthiness Standards: Normal Category Airplanes",
            "FAA FAR Part 25 - Airworthiness Standards: Transport Category Airplanes",
            "FAA Advisory Circular AC 23-8C, 'Certification of Normal Category Airplanes', 2017",
            "FAA Advisory Circular AC 25-7D, 'Flight Test Guide for Certification of Transport Category Airplanes', 2017",
            "FAA Order 8110.4C, 'Type Certification', 2018"
        ],
        burden_holder="Aircraft manufacturer and certification team",
        adversary_position=(
            "Certification requirements are overly burdensome and stifle innovation without improving safety."
        ),
        counter_arguments=[
            "Certification standards are based on decades of safety data and lessons learned from accidents.",
            "Rigorous testing and analysis prevent design flaws and operational hazards.",
            "Performance-based standards allow flexibility and innovation within safety margins.",
            "Continued airworthiness programs ensure ongoing safety beyond initial certification.",
            "Regulatory oversight protects public safety and industry reputation."
        ],
        resolution_strategy=(
            "Demonstrate certification process benefits through safety statistics, regulatory rationale, and industry best practices."
        ),
        entity_scope="Civil aircraft design and certification",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FAA FAR Parts 23 and 25"
    ),

    DoctrineBlock(
        topic="Gas Turbine Engine Brayton Cycle and Efficiency",
        keywords=["gas turbine engine", "Brayton cycle", "thermodynamics", "pressure ratio", "turbine inlet temperature", "thermal efficiency", "specific fuel consumption", "component efficiencies"],
        conclusion_template=(
            "Gas turbine engine performance is governed by the Brayton thermodynamic cycle, where pressure ratio and turbine inlet "
            "temperature critically influence thermal efficiency and specific fuel consumption."
        ),
        reasoning_framework=(
            "The Brayton cycle describes the idealized thermodynamic process of gas turbine engines, involving isentropic compression, "
            "constant pressure combustion, and isentropic expansion. Real engines deviate due to component inefficiencies and pressure "
            "losses. Increasing compressor pressure ratio raises cycle efficiency by increasing the temperature difference across the "
            "turbine. Turbine inlet temperature is limited by material and cooling technology but higher temperatures improve thermal "
            "efficiency. Component efficiencies (compressor, turbine, combustor) affect overall engine performance. Specific fuel consumption "
            "(SFC) measures fuel efficiency relative to thrust output. Advanced materials and cooling techniques enable higher turbine inlet "
            "temperatures, improving efficiency. Cycle modifications such as intercooling, regeneration, and reheating can further enhance "
            "performance. FAA certification requires demonstration of engine performance and emissions compliance."
        ),
        key_factors=[
            "Compressor pressure ratio",
            "Turbine inlet temperature and cooling",
            "Component isentropic efficiencies",
            "Combustion chamber pressure losses",
            "Specific fuel consumption (SFC)",
            "Material temperature limits",
            "Cycle modifications (intercooling, regeneration)",
            "Emissions and noise regulations"
        ],
        primary_authority=[
            "Mattingly, J.D., 'Elements of Gas Turbine Propulsion', 2nd Edition, AIAA, 2006",
            "Turns, S.R., 'An Introduction to Combustion: Concepts and Applications', 3rd Edition, McGraw-Hill, 2012",
            "FAA Advisory Circular AC 33.75-1, 'Gas Turbine Engine Certification', 2016",
            "NASA TM-2004-213253, 'Gas Turbine Engine Performance and Emissions', 2004",
            "Rolls-Royce plc, 'Gas Turbine Engine Thermodynamics', Technical Paper, 2017"
        ],
        burden_holder="Engine design and certification engineer",
        adversary_position=(
            "Gas turbine engine efficiency is primarily determined by fuel type and has limited dependence on thermodynamic cycle parameters."
        ),
        counter_arguments=[
            "Thermodynamic cycle parameters directly influence engine efficiency and performance.",
            "Higher pressure ratios and turbine inlet temperatures improve thermal efficiency.",
            "Fuel type affects emissions but not fundamental cycle efficiency.",
            "Empirical engine test data validate thermodynamic performance models.",
            "Certification standards require demonstration of cycle efficiency and emissions."
        ],
        resolution_strategy=(
            "Use thermodynamic analysis, engine test data, and certification documentation to confirm the central role of Brayton cycle parameters."
        ),
        entity_scope="Gas turbine engine design and certification",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA FAR Part 33 - Airworthiness Standards: Aircraft Engines"
    ),

    DoctrineBlock(
        topic="Computational Aerodynamics: CFD, Panel Method, and Vortex Lattice",
        keywords=["computational fluid dynamics", "CFD", "panel method", "vortex lattice method", "aerodynamic modeling", "flow simulation", "turbulence modeling", "mesh generation"],
        conclusion_template=(
            "Computational aerodynamics employs CFD, panel methods, and vortex lattice techniques to simulate airflow and predict "
            "aerodynamic characteristics, each suited to different fidelity and computational cost requirements."
        ),
        reasoning_framework=(
            "Computational aerodynamics uses numerical methods to solve fluid flow equations around aircraft geometries. CFD solves the "
            "Navier-Stokes equations, including turbulence models, providing high-fidelity predictions of complex flows including viscous "
            "effects and flow separation. Panel methods solve potential flow equations assuming inviscid, incompressible flow, suitable for "
            "external aerodynamics at subsonic speeds with attached flow. Vortex lattice methods model lifting surfaces as discrete vortices, "
            "efficiently predicting lift and induced drag for wings and tails. Mesh generation quality and turbulence modeling critically affect "
            "accuracy. Validation against wind tunnel and flight test data is essential. Computational cost and turnaround time influence method "
            "selection during design phases. Regulatory bodies accept CFD results as part of certification when validated."
        ),
        key_factors=[
            "Governing equations and assumptions",
            "Turbulence modeling approaches",
            "Mesh quality and resolution",
            "Computational resources and time",
            "Validation with experimental data",
            "Flow regimes and applicability",
            "Prediction of lift, drag, and moments",
            "Integration with design optimization"
        ],
        primary_authority=[
            "Anderson, J.D., 'Computational Fluid Dynamics: The Basics with Applications', 2nd Edition, McGraw-Hill, 1995",
            "Houghton, E.L. and Carpenter, P.W., 'Aerodynamics for Engineering Students', 6th Edition, 2017",
            "NASA CFD Vision 2030 Study, NASA/CR-2014-218178, 2014",
            "FAA AC 20-136B, 'Guidance for the Use of CFD in Aircraft Certification', 2018",
            "Celik, I.B., et al., 'Turbulence Modeling for CFD', NASA TM-2008-215861, 2008"
        ],
        burden_holder="Aerodynamicist and CFD analyst",
        adversary_position=(
            "Simplified aerodynamic methods suffice; high-fidelity CFD is unnecessary and unreliable for certification."
        ),
        counter_arguments=[
            "CFD provides detailed flow physics unattainable by simplified methods.",
            "Panel and vortex lattice methods have limited applicability in complex flows.",
            "Validation and verification ensure CFD reliability for certification.",
            "CFD accelerates design cycles and reduces wind tunnel costs.",
            "Regulatory guidance supports CFD use with proper validation."
        ],
        resolution_strategy=(
            "Demonstrate CFD validation cases, regulatory acceptance, and design benefits to justify computational aerodynamics use."
        ),
        entity_scope="Aircraft aerodynamic analysis and certification",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FAA AC 20-136B - Guidance for CFD Use in Certification"
    ),

    DoctrineBlock(
        topic="Flight Testing: Instrumentation and Data Acquisition",
        keywords=["flight testing", "instrumentation", "data acquisition", "flight envelope", "sensor calibration", "telemetry", "flight test instrumentation", "data analysis"],
        conclusion_template=(
            "Flight testing requires precise instrumentation and data acquisition systems to accurately capture aircraft performance "
            "and handling characteristics across the flight envelope for certification and development."
        ),
        reasoning_framework=(
            "Flight testing validates aircraft design and performance through controlled maneuvers and data collection. Instrumentation includes "
            "air data sensors, inertial measurement units, strain gauges, accelerometers, and GPS receivers. Data acquisition systems must "
            "sample at appropriate rates with synchronized timing and high resolution. Sensor calibration and error characterization are critical "
            "to ensure data integrity. Telemetry systems enable real-time monitoring and safety oversight. Flight envelope expansion tests "
            "explore aircraft behavior at operational limits. Data analysis involves filtering, correction, and statistical evaluation to derive "
            "performance parameters and handling qualities. Compliance with FAA AC 25-7D and MIL-STD-1553B ensures instrumentation reliability. "
            "Flight test engineers coordinate instrumentation design, installation, and data validation."
        ),
        key_factors=[
            "Sensor selection and calibration",
            "Data acquisition sampling rates and resolution",
            "Telemetry and data storage systems",
            "Flight envelope and test point selection",
            "Data processing and error correction",
            "Safety monitoring and redundancy",
            "Compliance with regulatory guidance",
            "Coordination between flight test and engineering teams"
        ],
        primary_authority=[
            "FAA AC 25-7D, 'Flight Test Guide for Certification of Transport Category Airplanes', 2017",
            "MIL-STD-1553B, 'Digital Time Division Command/Response Multiplex Data Bus', 1978",
            "NASA TP-2010-216769, 'Flight Test Instrumentation Handbook', 2010",
            "Society of Flight Test Engineers (SFTE), 'Flight Test Engineering Handbook', 2018",
            "RTCA DO-160G, 'Environmental Conditions and Test Procedures for Airborne Equipment', 2010"
        ],
        burden_holder="Flight test engineer and instrumentation specialist",
        adversary_position=(
            "Flight test instrumentation complexity is excessive; pilot observations suffice for certification."
        ),
        counter_arguments=[
            "Quantitative data is essential for objective performance and safety evaluation.",
            "Instrumentation enables detection of subtle phenomena not observable by pilots.",
            "Regulatory certification requires documented data supporting compliance.",
            "Telemetry enhances safety and test monitoring.",
            "Data analysis informs design improvements and risk mitigation."
        ],
        resolution_strategy=(
            "Present regulatory requirements, flight test plans, and data analysis reports to justify instrumentation complexity."
        ),
        entity_scope="Flight test programs for certification and development",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FAA AC 25-7D - Flight Test Guide"
    ),

    DoctrineBlock(
        topic="Satellite Systems: Communication, Earth Observation, and Navigation",
        keywords=["satellite systems", "communication satellites", "earth observation", "navigation satellites", "payload integration", "orbital parameters", "data downlink", "space segment"],
        conclusion_template=(
            "Satellite systems integrate communication, earth observation, and navigation payloads with orbital parameters and ground "
            "segment coordination to fulfill mission objectives."
        ),
        reasoning_framework=(
            "Satellite systems encompass space segment hardware, payloads, and ground infrastructure. Communication satellites provide "
            "data relay and broadcasting services using transponders and antennas optimized for frequency bands and coverage areas. Earth "
            "observation satellites carry sensors such as multispectral imagers and radar to monitor environmental and geospatial phenomena. "
            "Navigation satellites form constellations providing global positioning and timing services, requiring precise orbital control and "
            "clock stability. Payload integration involves mass, power, thermal, and data interface management. Orbital parameters (altitude, "
            "inclination, eccentricity) are selected based on mission requirements, balancing coverage, revisit time, and launch constraints. "
            "Data downlink utilizes radio frequency or optical communication links with ground stations. System reliability and redundancy "
            "are critical for mission success. International regulations govern frequency allocation and orbital slot assignments."
        ),
        key_factors=[
            "Payload type and mission requirements",
            "Orbital altitude and inclination",
            "Power and thermal management",
            "Data handling and downlink capabilities",
            "Spacecraft bus and subsystem integration",
            "Reliability and redundancy design",
            "Regulatory frequency and orbital coordination",
            "Ground segment infrastructure"
        ],
        primary_authority=[
            "NASA Systems Engineering Handbook, NASA/SP-2007-6105 Rev1, 2007",
            "ITU Radio Regulations, International Telecommunication Union, 2020",
            "European Space Agency (ESA) Earth Observation Handbook, 2019",
            "GPS Interface Specification IS-GPS-200, 2019",
            "CCSDS Blue Book, 'Space Data Link Protocols', 2017"
        ],
        burden_holder="Satellite system engineer and mission planner",
        adversary_position=(
            "Satellite payloads and orbital parameters can be selected independently without integrated system considerations."
        ),
        counter_arguments=[
            "Payload performance depends on orbital environment and spacecraft bus capabilities.",
            "Orbital parameters affect coverage, revisit, and communication latency.",
            "Integrated design optimizes mass, power, and thermal constraints.",
            "Regulatory coordination is mandatory for frequency and orbital slots.",
            "Mission success depends on holistic system engineering."
        ],
        resolution_strategy=(
            "Use system engineering documentation, mission analyses, and regulatory filings to demonstrate integrated satellite system design."
        ),
        entity_scope="Space segment design and mission planning",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NASA NPR 7120.5E - Space Flight Program and Project Management Requirements"
    ),

    DoctrineBlock(
        topic="UAV, UAS, and Drone Operations: Regulations and Airspace Integration",
        keywords=["UAV", "UAS", "drone operations", "regulations", "airspace integration", "remote pilot", "sense and avoid", "flight authorization"],
        conclusion_template=(
            "Unmanned Aerial Vehicle operations require compliance with regulations governing remote pilot certification, airspace "
            "integration, and safety measures including sense-and-avoid capabilities and flight authorization procedures."
        ),
        reasoning_framework=(
            "UAV and UAS operations are subject to evolving regulatory frameworks to ensure safety and integration with manned aviation. "
            "Remote pilot certification and operational limitations are defined by authorities such as the FAA under Part 107 and EASA "
            "regulations. Airspace integration requires coordination with Air Traffic Management, including flight authorization, "
            "communication protocols, and adherence to separation standards. Sense-and-avoid technologies are critical to prevent "
            "collisions with manned aircraft and obstacles. Operational risk assessments and contingency planning are mandated. "
            "Privacy, security, and environmental considerations influence regulatory policies. International harmonization efforts "
            "seek to standardize UAV operations globally. Compliance with these regulations is essential for legal and safe UAV deployment."
        ),
        key_factors=[
            "Remote pilot certification and training",
            "Airspace classification and flight restrictions",
            "Sense-and-avoid system capabilities",
            "Flight authorization and notification procedures",
            "Operational risk assessment and mitigation",
            "Communication and command link reliability",
            "Privacy and security regulations",
            "International regulatory harmonization"
        ],
        primary_authority=[
            "FAA Part 107 - Small Unmanned Aircraft Systems, 2021",
            "EASA Regulation 2019/947 on UAS Operations, 2019",
            "ICAO RPAS Concept of Operations, 2018",
            "RTCA DO-365, 'Minimum Operational Performance Standards for Detect and Avoid Systems', 2017",
            "ASTM F38 Committee on Unmanned Aircraft Systems Standards"
        ],
        burden_holder="UAV operator and remote pilot",
        adversary_position=(
            "UAV operations can be conducted without strict regulatory oversight or integration with manned airspace."
        ),
        counter_arguments=[
            "Regulations ensure safety of all airspace users and the public.",
            "Sense-and-avoid systems prevent collisions and incidents.",
            "Flight authorizations coordinate traffic and prevent conflicts.",
            "Certification and training reduce operational risks.",
            "International standards promote interoperability and safety."
        ],
        resolution_strategy=(
            "Demonstrate regulatory requirements, safety data, and operational procedures to justify UAV operation controls."
        ),
        entity_scope="Civil and commercial UAV operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FAA Part 107 and EASA UAS Regulations"
    ),

    DoctrineBlock(
        topic="Human Factors in Cockpit Design and Crew Resource Management (CRM)",
        keywords=["human factors", "cockpit design", "crew resource management", "fatigue", "workload", "situational awareness", "ergonomics", "error management"],
        conclusion_template=(
            "Human factors considerations in cockpit design and CRM enhance flight safety by optimizing ergonomics, reducing fatigue, "
            "and improving situational awareness and communication among flight crew."
        ),
        reasoning_framework=(
            "Human factors engineering addresses the interaction between pilots and aircraft systems to minimize errors and enhance performance. "
            "Cockpit design incorporates ergonomic principles to ensure controls and displays are intuitive, accessible, and reduce pilot workload. "
            "Crew Resource Management (CRM) fosters effective communication, decision-making, and teamwork among flight crew, mitigating human error. "
            "Fatigue management programs address circadian rhythms and duty time limitations to maintain alertness. Workload assessment ensures tasks "
            "are balanced to prevent overload or underload. Situational awareness is supported by integrated displays and alerting systems. "
            "Training programs incorporate human factors principles to improve safety culture. Regulatory guidance such as FAA AC 120-51E and ICAO "
            "Doc 9683 provide frameworks for human factors integration."
        ),
        key_factors=[
            "Ergonomic layout of controls and displays",
            "Communication protocols and CRM training",
            "Fatigue risk management and duty limitations",
            "Workload monitoring and task allocation",
            "Situational awareness enhancement tools",
            "Error management and recovery strategies",
            "Training and simulation programs",
            "Regulatory guidance and compliance"
        ],
        primary_authority=[
            "FAA AC 120-51E, 'Crew Resource Management Training', 2015",
            "ICAO Doc 9683, 'Manual on Human Factors in Aircraft Maintenance', 2013",
            "Wickens, C.D., 'Engineering Psychology and Human Performance', 4th Edition, Pearson, 2008",
            "NASA Ames Research Center, 'Human Factors in Aviation', Technical Reports, 2010-2020",
            "Eurocontrol Human Factors Integration Handbook, 2017"
        ],
        burden_holder="Aircraft designers and airline training organizations",
        adversary_position=(
            "Human factors and CRM have limited impact on flight safety compared to technical systems."
        ),
        counter_arguments=[
            "Human error remains a leading cause of aviation incidents and accidents.",
            "CRM improves communication and decision-making, reducing errors.",
            "Ergonomic cockpit design reduces pilot workload and fatigue.",
            "Training incorporating human factors improves safety culture.",
            "Regulatory mandates require human factors integration."
        ],
        resolution_strategy=(
            "Present accident analyses, safety studies, and regulatory frameworks demonstrating human factors' critical role."
        ),
        entity_scope="Commercial aviation cockpit design and operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FAA AC 120-51E - Crew Resource Management Training"
    ),

    DoctrineBlock(
        topic="Reliability of Aircraft Systems: MTBF, MTTR, and Dispatch Rate",
        keywords=["reliability", "mean time between failures", "mean time to repair", "dispatch reliability", "system redundancy", "failure modes", "maintenance planning", "operational availability"],
        conclusion_template=(
            "Aircraft system reliability is quantified by MTBF and MTTR metrics, with system redundancy and maintenance planning critical "
            "to achieving high dispatch reliability and operational availability."
        ),
        reasoning_framework=(
            "Reliability engineering in aviation focuses on ensuring systems perform without failure over intended intervals. Mean Time Between "
            "Failures (MTBF) measures average operational time before failure, while Mean Time To Repair (MTTR) quantifies repair duration. "
            "High MTBF and low MTTR improve dispatch reliability, minimizing flight delays and cancellations. Redundancy in critical systems "
            "provides fail-safe capability, enhancing safety and availability. Failure modes and effects analysis (FMEA) identifies potential "
            "failure points and guides design improvements. Maintenance planning schedules preventive and corrective actions to optimize reliability. "
            "Operational availability balances reliability, maintainability, and logistics support. Regulatory standards such as FAA AC 25.1309-1A "
            "govern system safety and reliability requirements. Data collection and analysis support continuous improvement."
        ),
        key_factors=[
            "MTBF and MTTR statistical analysis",
            "System redundancy and fault tolerance",
            "Failure modes and effects analysis (FMEA)",
            "Maintenance scheduling and planning",
            "Dispatch reliability metrics",
            "Operational availability calculations",
            "Data collection and reliability growth",
            "Regulatory compliance and certification"
        ],
        primary_authority=[
            "FAA AC 25.1309-1A, 'System Design and Analysis', 2002",
            "MIL-STD-1629A, 'Failure Mode, Effects and Criticality Analysis', 1980",
            "SAE ARP4754A, 'Guidelines for Development of Civil Aircraft and Systems', 2010",
            "Reliability Engineering Handbook, IEEE Press, 1996",
            "Boeing Statistical Reliability Data, Technical Reports, 2015"
        ],
        burden_holder="Reliability engineer and maintenance planner",
        adversary_position=(
            "Reliability metrics are theoretical and do not reflect real operational conditions."
        ),
        counter_arguments=[
            "Operational data validates reliability metrics and guides maintenance.",
            "Redundancy and fault tolerance improve real-world system availability.",
            "Regulatory certification requires demonstrated reliability.",
            "Maintenance planning based on reliability reduces unscheduled downtime.",
            "Continuous data collection supports accurate reliability modeling."
        ],
        resolution_strategy=(
            "Present operational reliability data, maintenance records, and certification documentation to confirm metric validity."
        ),
        entity_scope="Aircraft systems reliability and maintenance",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1309-1A - System Design and Analysis"
    ),

    DoctrineBlock(
        topic="Environmental Impact of Aviation: Noise, Emissions, and Contrails",
        keywords=["environmental impact", "noise pollution", "emissions", "contrails", "sustainable aviation fuel", "carbon footprint", "ICAO CAEP", "noise abatement procedures"],
        conclusion_template=(
            "Aviation environmental impact encompasses noise, emissions, and contrail formation, with mitigation strategies including "
            "noise abatement procedures and sustainable aviation fuel adoption to reduce carbon footprint."
        ),
        reasoning_framework=(
            "Aviation contributes to environmental concerns through noise pollution near airports, greenhouse gas emissions, and contrail-induced "
            "cloudiness. Noise arises from engine exhaust, fan blades, and airframe interactions, affecting communities and wildlife. Emissions "
            "include CO2, NOx, and particulate matter, contributing to climate change and air quality degradation. Contrails form from water vapor "
            "condensation in engine exhaust, influencing radiative forcing. Regulatory bodies such as ICAO's Committee on Aviation Environmental "
            "Protection (CAEP) set standards for noise and emissions. Sustainable aviation fuels (SAF) offer carbon lifecycle reductions. Noise abatement "
            "procedures optimize flight paths and operations to minimize noise impact. Continuous monitoring and modeling inform policy and technology "
            "development. Aircraft and engine manufacturers incorporate environmental considerations into design and certification."
        ),
        key_factors=[
            "Aircraft noise sources and measurement",
            "Emissions composition and impact",
            "Contrail formation conditions and effects",
            "Sustainable aviation fuel properties and availability",
            "ICAO CAEP standards and recommendations",
            "Noise abatement operational procedures",
            "Environmental monitoring and modeling",
            "Certification and regulatory compliance"
        ],
        primary_authority=[
            "ICAO Annex 16, Volume I and II - Environmental Protection",
            "FAA Part 36 - Noise Standards: Aircraft Type and Airworthiness Certification",
            "ICAO CAEP Reports and Recommendations",
            "International Air Transport Association (IATA) Environmental Report, 2020",
            "ASTM D7566 - Standard Specification for Aviation Turbine Fuel Containing Synthesized Hydrocarbons"
        ],
        burden_holder="Aircraft operators and manufacturers",
        adversary_position=(
            "Environmental regulations impose unnecessary costs without significant environmental benefits."
        ),
        counter_arguments=[
            "Scientific consensus confirms aviation's environmental impact.",
            "Regulations drive technology innovation and operational improvements.",
            "Sustainable fuels reduce lifecycle emissions.",
            "Noise abatement improves community relations and health.",
            "International agreements mandate environmental responsibility."
        ],
        resolution_strategy=(
            "Present environmental impact studies, regulatory frameworks, and technology adoption data to justify mitigation efforts."
        ),
        entity_scope="Civil aviation environmental management",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ICAO Annex 16 - Environmental Protection"
    ),

    DoctrineBlock(
        topic="Hypersonic Aerothermodynamics and Reentry Thermal Protection",
        keywords=["hypersonic", "aerothermodynamics", "reentry", "thermal protection system", "shock waves", "boundary layer heating", "ablative materials", "heat flux"],
        conclusion_template=(
            "Hypersonic flight and atmospheric reentry impose severe aerothermodynamic heating challenges, necessitating advanced thermal "
            "protection systems utilizing ablative and insulating materials to manage heat flux and ensure vehicle integrity."
        ),
        reasoning_framework=(
            "Hypersonic aerothermodynamics involves complex flow phenomena including strong shock waves, high-temperature gas chemistry, and "
            "boundary layer interactions. Reentry vehicles encounter extreme aerodynamic heating due to compression and viscous dissipation. "
            "Thermal protection systems (TPS) employ ablative materials that absorb and dissipate heat through controlled erosion, and insulating "
            "materials that reduce heat conduction to the structure. Heat flux predictions require coupled fluid dynamics and heat transfer modeling. "
            "Material selection balances thermal resistance, structural integrity, and weight. Aerothermal loads vary with trajectory, velocity, "
            "and atmospheric density. Testing includes arc-jet facilities and flight experiments. Certification and qualification standards "
            "govern TPS performance and reliability."
        ),
        key_factors=[
            "Shock wave strength and location",
            "Boundary layer state and transition",
            "Heat flux magnitude and duration",
            "Ablative material properties and erosion rates",
            "Thermal conductivity and insulation",
            "Trajectory and velocity profiles",
            "Material testing and qualification",
            "Structural integration and safety margins"
        ],
        primary_authority=[
            "Anderson, J.D., 'Hypersonic and High Temperature Gas Dynamics', 2nd Edition, AIAA, 2006",
            "NASA SP-8080, 'Thermal Protection Materials and Systems', 1995",
            "MIL-STD-2105C, 'Thermal Protection System Materials', 1990",
            "ESA Thermal Protection System Design Guidelines, 2018",
            "NASA Technical Memorandum TM-2004-213253, 'Aerothermodynamics of Reentry Vehicles', 2004"
        ],
        burden_holder="Thermal protection system engineer and vehicle designer",
        adversary_position=(
            "Conventional materials and cooling methods suffice for hypersonic and reentry thermal protection."
        ),
        counter_arguments=[
            "Hypersonic heating exceeds capabilities of conventional materials.",
            "Ablative TPS are proven for managing extreme heat fluxes.",
            "Material testing confirms performance under reentry conditions.",
            "Failure to provide adequate TPS risks vehicle loss and crew safety.",
            "Advanced modeling and testing are essential for design validation."
        ],
        resolution_strategy=(
            "Use aerothermodynamic analyses, material test data, and flight experience to justify advanced TPS requirements."
        ),
        entity_scope="Hypersonic vehicle and reentry spacecraft design",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NASA SP-8080 - Thermal Protection Materials and Systems"
    ),

    DoctrineBlock(
        topic="Composite Manufacturing: Layup, Autoclave, RTM, and Repair",
        keywords=["composite manufacturing", "layup", "autoclave curing", "resin transfer molding", "repair techniques", "fiber orientation", "void content", "quality control"],
        conclusion_template=(
            "Composite manufacturing employs techniques such as manual layup, autoclave curing, and resin transfer molding (RTM), "
            "with repair methods focusing on damage assessment, material compatibility, and restoration of structural integrity."
        ),
        reasoning_framework=(
            "Composite manufacturing involves layering fiber reinforcements impregnated with resin matrix materials to form structural components. "
            "Manual layup places prepreg or dry fibers in molds, followed by autoclave curing under heat and pressure to consolidate and cure the resin, "
            "achieving high fiber volume fraction and low void content. Resin Transfer Molding (RTM) injects resin into a closed mold with dry fibers, "
            "enabling complex shapes and automation. Fiber orientation critically affects mechanical properties and load paths. Quality control includes "
            "non-destructive evaluation and process monitoring to detect defects. Repair techniques involve damage detection, removal of compromised material, "
            "and application of patch or scarf repairs with compatible materials and curing methods. Certification standards such as FAA AC 20-107B guide "
            "composite manufacturing and repair."
        ),
        key_factors=[
            "Fiber type and orientation",
            "Resin system and curing parameters",
            "Manufacturing process selection (layup, autoclave, RTM)",
            "Void content and defect control",
            "Non-destructive inspection methods",
            "Repair material compatibility and techniques",
            "Process monitoring and quality assurance",
            "Certification and regulatory compliance"
        ],
        primary_authority=[
            "FAA AC 20-107B, 'Composite Aircraft Structure', 2013",
            "MIL-HDBK-17-1F, 'Composite Materials Handbook', 2012",
            "ASTM D3171, 'Standard Test Methods for Constituent Content of Composite Materials', 2017",
            "SAE ARP4754A, 'Guidelines for Development of Civil Aircraft and Systems', 2010",
            "Toray Industries, 'Composite Manufacturing Technical Data', 2019"
        ],
        burden_holder="Composite manufacturing engineer and repair technician",
        adversary_position=(
            "Composite manufacturing and repair processes are interchangeable with metallic methods without special considerations."
        ),
        counter_arguments=[
            "Composite materials require specialized processes for curing and consolidation.",
            "Fiber orientation and resin curing critically affect mechanical properties.",
            "Repair techniques must restore load paths and material integrity.",
            "Certification standards differentiate composite from metallic structures.",
            "Quality control is essential to detect manufacturing defects unique to composites."
        ],
        resolution_strategy=(
            "Present manufacturing process documentation, repair procedures, and certification guidance to justify specialized composite methods."
        ),
        entity_scope="Aerospace composite structure manufacturing and repair",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FAA AC 20-107B - Composite Aircraft Structure"
    ),

    DoctrineBlock(
        topic="Engine Control: FADEC, Fuel Metering, and Thrust Management",
        keywords=["engine control", "FADEC", "fuel metering", "thrust management", "digital control", "engine parameters", "redundancy", "performance optimization"],
        conclusion_template=(
            "Full Authority Digital Engine Control (FADEC) systems manage fuel metering and thrust commands digitally, optimizing engine "
            "performance, improving reliability, and enabling precise control across operating conditions."
        ),
        reasoning_framework=(
            "FADEC systems replace mechanical engine controls with digital computers that monitor and adjust engine parameters including fuel flow, "
            "ignition timing, and variable geometry components. Fuel metering accuracy directly affects combustion efficiency and emissions. "
            "Thrust management integrates pilot commands with engine health monitoring to optimize performance and prevent exceedances. "
            "Redundancy and fault tolerance are incorporated to ensure safe operation. FADEC enables automatic engine start, idle control, and "
            "engine limit protections. Integration with aircraft systems supports thrust reversers and auto-throttle functions. Certification "
            "requires software and hardware validation per RTCA DO-178C and DO-254. FADEC improves fuel efficiency, reduces pilot workload, "
            "and enhances engine life."
        ),
        key_factors=[
            "Digital control algorithms and software reliability",
            "Fuel flow measurement and metering accuracy",
            "Thrust command interface and response",
            "Redundancy and fault management",
            "Integration with aircraft systems",
            "Certification and validation standards",
            "Performance optimization and emissions control",
            "Pilot interface and override capabilities"
        ],
        primary_authority=[
            "RTCA DO-178C, 'Software Considerations in Airborne Systems and Equipment Certification', 2011",
            "RTCA DO-254, 'Design Assurance Guidance for Airborne Electronic Hardware', 2000",
            "FAA AC 33.75-1, 'Gas Turbine Engine Certification', 2016",
            "Pratt & Whitney, 'FADEC System Overview', Technical Paper, 2018",
            "Rolls-Royce plc, 'Digital Engine Control Systems', 2019"
        ],
        burden_holder="Engine control system designer and certification engineer",
        adversary_position=(
            "Mechanical engine controls are sufficient; digital FADEC systems add unnecessary complexity and risk."
        ),
        counter_arguments=[
            "FADEC improves engine efficiency and reduces pilot workload.",
            "Digital controls enable precise fuel metering and thrust management.",
            "Redundancy and fault tolerance enhance safety.",
            "Certification standards ensure software and hardware reliability.",
            "Operational data shows improved engine performance with FADEC."
        ],
        resolution_strategy=(
            "Use certification documentation, operational performance data, and safety analyses to justify FADEC adoption."
        ),
        entity_scope="Gas turbine engine control systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA FAR Part 33 - Airworthiness Standards: Aircraft Engines"
    ),

    DoctrineBlock(
        topic="Landing Gear Design: Retraction, Shock Absorber, Tire, and Brake Systems",
        keywords=["landing gear", "retraction mechanism", "shock absorber", "tires", "brakes", "structural loads", "hydraulic actuation", "energy absorption"],
        conclusion_template=(
            "Landing gear systems incorporate retraction mechanisms, shock absorbers, tires, and brakes designed to absorb landing loads, "
            "enable ground maneuvering, and ensure safe deceleration."
        ),
        reasoning_framework=(
            "Landing gear design addresses structural loads during landing, taxi, and takeoff. Retraction mechanisms reduce drag during flight, "
            "requiring reliable actuation systems often hydraulic or electric. Shock absorbers (oleo struts) dissipate kinetic energy, reducing "
            "structural stress and improving passenger comfort. Tires must withstand loads, wear, and provide adequate friction for braking and "
            "steering. Brake systems, typically hydraulic with multiple redundancies, provide controlled deceleration and stopping power. "
            "Load analysis includes impact forces, side loads during taxi, and emergency braking. Materials and components are selected for durability "
            "and maintainability. Certification standards such as FAA FAR Part 25.735 govern landing gear design and testing."
        ),
        key_factors=[
            "Retraction system reliability and actuation method",
            "Shock absorber energy absorption capacity",
            "Tire load rating and friction characteristics",
            "Brake system redundancy and performance",
            "Structural load analysis and fatigue considerations",
            "Materials selection and corrosion protection",
            "Maintenance and inspection requirements",
            "Certification and testing standards"
        ],
        primary_authority=[
            "FAA FAR Part 25.735 - Landing Gear Design and Construction",
            "Raymer, D.P., 'Aircraft Design: A Conceptual Approach', 6th Edition, AIAA, 2018",
            "SAE ARP 4754A, 'Guidelines for Development of Civil Aircraft and Systems', 2010",
            "Boeing Commercial Airplane Group, 'Landing Gear Design Manual', 2015",
            "ASTM F1166, 'Standard Guide for Human Engineering Design for Marine Systems, Equipment, and Facilities', 2003"
        ],
        burden_holder="Landing gear design engineer and certification team",
        adversary_position=(
            "Simplified fixed landing gear designs suffice; complex retraction and shock absorption systems add weight and cost without benefit."
        ),
        counter_arguments=[
            "Retractable gear reduces aerodynamic drag, improving fuel efficiency.",
            "Shock absorbers protect airframe and improve passenger comfort.",
            "Brake systems provide essential stopping performance and safety.",
            "Certification standards require demonstration of gear performance.",
            "Operational experience supports complex gear system benefits."
        ],
        resolution_strategy=(
            "Present aerodynamic performance data, certification test results, and operational safety records to justify landing gear design."
        ),
        entity_scope="Fixed-wing aircraft landing gear systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FAA FAR Part 25.735 - Landing Gear Design and Construction"
    ),

    DoctrineBlock(
        topic="Aircraft Fuel Systems: Tank, Boost Pump, Transfer and Distribution",
        keywords=["fuel system", "fuel tank", "boost pump", "fuel transfer", "fuel quantity indicating", "refueling", "defueling", "fuel contamination"],
        conclusion_template="Aircraft fuel systems encompass storage, transfer, and distribution of aviation fuel from tanks to engines, requiring redundancy, contamination prevention, and precise quantity indication per FAR Part 25 Subpart E.",
        reasoning_framework=(
            "Aircraft fuel systems must provide uninterrupted fuel flow to engines under all flight conditions including negative-g maneuvers and turbulence. "
            "Integral fuel tanks in wing structures maximize capacity while structural tanks use bladders for containment. "
            "Boost pumps pressurize fuel to prevent vapor lock at altitude, with redundant pumps per tank for safety. "
            "Fuel transfer systems manage center-of-gravity by sequencing tank usage, critical for longitudinal stability. "
            "Fuel quantity indicating systems (FQIS) use capacitance probes to measure fuel volume and mass. "
            "Cross-feed valves allow any engine to draw from any tank, providing redundancy in engine-out scenarios. "
            "Contamination control includes water separators, filters, and fuel sampling procedures per ASTM D1655. "
            "Refueling/defueling operations follow strict grounding and bonding procedures to prevent static discharge ignition."
        ),
        key_factors=["Tank integrity and venting", "Boost pump redundancy", "Fuel transfer sequencing", "FQIS accuracy", "Contamination control", "Refueling safety"],
        primary_authority=[
            "14 CFR Part 25 Subpart E - Powerplant, Fuel System Requirements",
            "AC 25.981-2A Fuel Tank Flammability Reduction Means",
            "ASTM D1655 Standard Specification for Aviation Turbine Fuels",
        ],
        burden_holder="Aircraft fuel system design engineer",
        adversary_position="Simplified fuel systems reduce weight but increase single-point failure risk",
        counter_arguments=[
            "Modern composite tanks eliminate corrosion but introduce new failure modes",
            "Electronic fuel management reduces manual errors but adds software certification burden",
            "Biofuel blends require material compatibility verification across all wetted components",
        ],
        resolution_strategy="Design per FAR 25 fuel system requirements with redundant pumps, cross-feed capability, and FQIS meeting accuracy requirements of AC 25-11B",
        entity_scope="Transport category aircraft fuel systems",
        confidence=0.94,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="TWA 800 Investigation — NTSB/AAR-00/03 Fuel Tank Flammability",
    ),
]

# =============================================================
# SUB-ENGINE ORCHESTRATION
# =============================================================

class SubEngineStatus(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    UNKNOWN = auto()

class CircuitBreakerState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class IssueCategory(Enum):
    AERODYNAMICS = "AERO01"
    PROPULSION = "AERO02"
    STRUCTURES = "AERO03"
    AVIONICS = "AERO04"
    FLIGHT_MECHANICS = "AERO05"
    AIRCRAFT_DESIGN = "AERO06"
    SPACE_SYSTEMS = "AERO07"
    MATERIALS_AEROSPACE = "AERO08"
    MAINTENANCE_MRO = "AERO09"
    AIR_TRAFFIC_MANAGEMENT = "AERO10"

class QueryRequest:
    def __init__(self, text: str, mode: str = "default", meta: Optional[dict] = None):
        self.text = text
        self.mode = mode
        self.meta = meta or {}

class RoutingDecision:
    def __init__(self, selected_engines: List[str], categories: List[IssueCategory], reason: str = ""):
        self.selected_engines = selected_engines
        self.categories = categories
        self.reason = reason

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, priority: int = 1):
        self.engine_id = engine_id
        self.url = url
        self.priority = priority

# --- Sub-Engine Registry ---

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "AERO01": SubEngineConfig("AERO01", "http://aero01.local/api/query", 3),
    "AERO02": SubEngineConfig("AERO02", "http://aero02.local/api/query", 3),
    "AERO03": SubEngineConfig("AERO03", "http://aero03.local/api/query", 2),
    "AERO04": SubEngineConfig("AERO04", "http://aero04.local/api/query", 2),
    "AERO05": SubEngineConfig("AERO05", "http://aero05.local/api/query", 2),
    "AERO06": SubEngineConfig("AERO06", "http://aero06.local/api/query", 1),
    "AERO07": SubEngineConfig("AERO07", "http://aero07.local/api/query", 1),
    "AERO08": SubEngineConfig("AERO08", "http://aero08.local/api/query", 1),
    "AERO09": SubEngineConfig("AERO09", "http://aero09.local/api/query", 1),
    "AERO10": SubEngineConfig("AERO10", "http://aero10.local/api/query", 2),
}

# --- Circuit Breaker Implementation ---

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=30):
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.last_failure_time = 0
        self.recovery_timeout = recovery_timeout

    def allow_request(self) -> bool:
        if self.state == CircuitBreakerState.OPEN:
            if (time.time() - self.last_failure_time) > self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                return True
            return False
        return True

    def record_success(self):
        self.failure_count = 0
        self.state = CircuitBreakerState.CLOSED

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

    def __repr__(self):
        return f"CircuitBreaker(state={self.state}, failures={self.failure_count})"

# --- SubEngineHealthMonitor ---

class SubEngineHealthMonitor:
    def __init__(self, registry: Dict[str, SubEngineConfig], ttl: int = 30):
        self.registry = registry
        self.health_cache: Dict[str, Tuple[SubEngineStatus, float]] = {}
        self.ttl = ttl
        self.circuit_breakers: Dict[str, CircuitBreaker] = {
            eid: CircuitBreaker() for eid in registry
        }

    async def check_health(self, engine_id: str) -> SubEngineStatus:
        now = time.time()
        cached = self.health_cache.get(engine_id)
        if cached and (now - cached[1]) < self.ttl:
            return cached[0]
        config = self.registry.get(engine_id)
        if not config:
            return SubEngineStatus.UNKNOWN
        try:
            status = await self._ping_engine(config.url, timeout=3)
        except Exception:
            status = SubEngineStatus.UNHEALTHY
        self.health_cache[engine_id] = (status, now)
        return status

    async def check_all_health(self) -> Dict[str, SubEngineStatus]:
        tasks = [self.check_health(eid) for eid in self.registry]
        results = await asyncio.gather(*tasks)
        return {eid: status for eid, status in zip(self.registry, results)}

    def get_healthy_engines(self) -> List[str]:
        now = time.time()
        healthy = []
        for eid, config in self.registry.items():
            cached = self.health_cache.get(eid)
            if cached and (now - cached[1]) < self.ttl and cached[0] == SubEngineStatus.HEALTHY:
                healthy.append(eid)
        return healthy

    async def _ping_engine(self, url: str, timeout: int = 3) -> SubEngineStatus:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}/health", timeout=timeout) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("status") == "healthy":
                            return SubEngineStatus.HEALTHY
                        elif data.get("status") == "degraded":
                            return SubEngineStatus.DEGRADED
                        else:
                            return SubEngineStatus.UNHEALTHY
                    else:
                        return SubEngineStatus.UNHEALTHY
        except Exception:
            return SubEngineStatus.UNHEALTHY

    def get_circuit_breaker(self, engine_id: str) -> CircuitBreaker:
        return self.circuit_breakers[engine_id]

# --- QueryRouter ---

class QueryRouter:
    # Keyword mapping for domain classification
    CATEGORY_KEYWORDS: Dict[IssueCategory, Set[str]] = {
        IssueCategory.AERODYNAMICS: {"lift", "drag", "flow", "wing", "aero", "stall", "boundary layer", "turbulence"},
        IssueCategory.PROPULSION: {"engine", "thrust", "propulsion", "turbine", "jet", "combustion", "nozzle", "afterburner"},
        IssueCategory.STRUCTURES: {"stress", "strain", "fatigue", "structure", "frame", "spar", "rib", "buckling"},
        IssueCategory.AVIONICS: {"avionics", "flight computer", "navigation", "autopilot", "sensor", "radar", "communication"},
        IssueCategory.FLIGHT_MECHANICS: {"trajectory", "maneuver", "stability", "control", "pitch", "yaw", "roll", "flight path"},
        IssueCategory.AIRCRAFT_DESIGN: {"design", "configuration", "layout", "concept", "trade-off", "optimization"},
        IssueCategory.SPACE_SYSTEMS: {"satellite", "orbital", "spacecraft", "launch", "re-entry", "payload", "propellant"},
        IssueCategory.MATERIALS_AEROSPACE: {"material", "composite", "alloy", "fatigue", "corrosion", "coating", "titanium"},
        IssueCategory.MAINTENANCE_MRO: {"maintenance", "inspection", "repair", "overhaul", "mro", "downtime", "lifecycle"},
        IssueCategory.AIR_TRAFFIC_MANAGEMENT: {"atm", "air traffic", "control", "atc", "slot", "clearance", "separation"},
    }

    def __init__(self, registry: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.registry = registry
        self.health_monitor = health_monitor

    def route_query(self, query: QueryRequest) -> RoutingDecision:
        categories = self._classify_domain(query.text)
        if not categories:
            categories = [IssueCategory.AIRCRAFT_DESIGN]  # Default fallback
        engines = self._select_engines(categories, query.mode)
        # Apply routing rules (e.g., exclude unhealthy)
        selected = self._apply_routing_rules(query)
        if not selected:
            selected = [e.engine_id for e in engines]
        reason = f"Categories: {[c.value for c in categories]}, Engines: {selected}"
        return RoutingDecision(selected, categories, reason)

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text_lower = text.lower()
        found = set()
        for cat, keywords in self.CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    found.add(cat)
        return list(found)

    def _select_engines(self, categories: List[IssueCategory], mode: str) -> List[SubEngineConfig]:
        # Select engines by category, prioritize by config priority
        engines = []
        for cat in categories:
            eid = cat.value
            config = self.registry.get(eid)
            if config:
                engines.append(config)
        # Mode can affect selection (e.g., "parallel" = all, "cascade" = by priority)
        if mode == "parallel":
            return engines
        elif mode == "cascade":
            return sorted(engines, key=lambda c: -c.priority)
        else:
            return engines

    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        # Exclude unhealthy or circuit-open engines
        healthy = self.health_monitor.get_healthy_engines()
        # If none healthy, fallback to all
        if not healthy:
            return []
        categories = self._classify_domain(query.text)
        eids = [cat.value for cat in categories]
        return [eid for eid in eids if eid in healthy]

    def _score_engine_relevance(self, engine: SubEngineConfig, query: QueryRequest) -> float:
        # Simple scoring: keyword overlap + priority
        text = query.text.lower()
        cat = IssueCategory(engine.engine_id)
        keywords = self.CATEGORY_KEYWORDS.get(cat, set())
        score = sum(1 for kw in keywords if kw in text)
        return score + engine.priority * 0.5

    def _handle_engine_failure(self, engine_id: str, error: Exception):
        cb = self.health_monitor.get_circuit_breaker(engine_id)
        cb.record_failure()
        # Fallback: if circuit open, remove from routing for 30s
        if cb.state == CircuitBreakerState.OPEN:
            # Optionally, log or trigger alert
            pass

# --- SubEngineOrchestrator ---

class SubEngineOrchestrator:
    def __init__(self, registry: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.registry = registry
        self.health_monitor = health_monitor

    async def dispatch_query(self, query: QueryRequest, engines: List[str]) -> List[Any]:
        # Default: parallel dispatch, collect all responses
        return await self.dispatch_parallel(query, engines)

    async def dispatch_parallel(self, query: QueryRequest, engines: List[str]) -> List[Any]:
        tasks = []
        for eid in engines:
            config = self.registry.get(eid)
            if not config:
                continue
            cb = self.health_monitor.get_circuit_breaker(eid)
            if not cb.allow_request():
                continue
            tasks.append(self._call_sub_engine(config, query, cb))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        responses = []
        for eid, res in zip(engines, results):
            if isinstance(res, Exception):
                self.health_monitor.get_circuit_breaker(eid).record_failure()
            else:
                self.health_monitor.get_circuit_breaker(eid).record_success()
                responses.append(res)
        return responses

    async def dispatch_cascade(self, query: QueryRequest, engines: List[str]) -> Any:
        # Try engines in order, return first successful response
        for eid in engines:
            config = self.registry.get(eid)
            if not config:
                continue
            cb = self.health_monitor.get_circuit_breaker(eid)
            if not cb.allow_request():
                continue
            try:
                resp = await self._call_sub_engine(config, query, cb)
                cb.record_success()
                return resp
            except Exception as e:
                cb.record_failure()
                continue
        return {"error": "All sub-engines failed"}

    async def _call_sub_engine(self, config: SubEngineConfig, query: QueryRequest, cb: CircuitBreaker) -> Any:
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "query": query.text,
                    "mode": query.mode,
                    "meta": query.meta
                }
                async with session.post(config.url, json=payload, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {"engine_id": config.engine_id, "response": data}
                    else:
                        raise Exception(f"Sub-engine {config.engine_id} returned {resp.status}")
        except Exception as e:
            cb.record_failure()
            raise

    def _merge_responses(self, responses: List[Any]) -> Any:
        # Merge logic: aggregate responses by engine_id
        merged = {"responses": []}
        for resp in responses:
            merged["responses"].append(resp)
        return merged

    def _resolve_conflicts(self, responses: List[Any]) -> Any:
        # Simple consensus: majority vote on answer field if present
        answers = {}
        for resp in responses:
            answer = resp.get("response", {}).get("answer")
            if answer:
                answers[answer] = answers.get(answer, 0) + 1
        if not answers:
            return {"consensus": None, "responses": responses}
        consensus = max(answers.items(), key=lambda x: x[1])[0]
        return {"consensus": consensus, "responses": responses}

class AuthorityLevel(Enum):
    CONSTITUTIONAL = auto()
    STATUTORY = auto()
    REGULATORY = auto()
    CASE_LAW = auto()
    TREATISE = auto()
    PRACTICE = auto()

authority_weights = {
    AuthorityLevel.CONSTITUTIONAL: 100,
    AuthorityLevel.STATUTORY: 80,
    AuthorityLevel.REGULATORY: 60,
    AuthorityLevel.CASE_LAW: 50,
    AuthorityLevel.TREATISE: 40,
    AuthorityLevel.PRACTICE: 20,
}

def resolve_authority_conflict(sources: List[AuthorityLevel]) -> AuthorityLevel:
    if not sources:
        raise ValueError("No authority sources provided")
    weighted = [(authority_weights[src], src) for src in sources if src in authority_weights]
    if not weighted:
        raise ValueError("No recognized authority levels in sources")
    weighted.sort(reverse=True, key=lambda x: x[0])
    top_weight = weighted[0][0]
    top_authorities = [auth for w, auth in weighted if w == top_weight]
    # If multiple top authorities, apply tie-breaker by enum order (lowest enum value wins)
    top_authorities.sort(key=lambda x: x.value)
    return top_authorities[0]

# --- EPISTEMIC GUARDRAILS ---

BANNED_PHRASES = [
    "clearly", "obviously", "without doubt", "undeniably", "unquestionably",
    "beyond question", "incontrovertibly", "manifestly", "patently", "plainly",
    "self-evident", "categorically", "definitely", "absolutely", "surely",
    "certainly", "indisputably", "incontestably", "unequivocally", "beyond dispute",
    "decidedly", "positively", "infallibly", "irrefutably", "unambiguously",
    "conclusively", "categorically", "inarguably", "incontrovertibly", "undoubtedly",
    "without fail", "incontestably", "without question"
]

DISCLOSURE_CAVEAT = (
    "Note: The following analysis is subject to limitations in data and interpretation; "
    "statements avoid unwarranted certainty."
)

class ConfidenceLevel(Enum):
    DEFENSIBLE = auto()
    AGGRESSIVE = auto()
    DISCLOSURE = auto()
    HIGH_RISK = auto()

def apply_epistemic_guardrails(text: str) -> Tuple[str, ConfidenceLevel]:
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, BANNED_PHRASES)) + r')\b', re.IGNORECASE)
    found = pattern.findall(text)
    cleaned_text = pattern.sub("[REDACTED]", text)
    cleaned_text = cleaned_text.strip()
    cleaned_text += "\n\n" + DISCLOSURE_CAVEAT
    # Stratify confidence based on banned phrase count
    count = len(found)
    if count == 0:
        confidence = ConfidenceLevel.DEFENSIBLE
    elif count <= 2:
        confidence = ConfidenceLevel.AGGRESSIVE
    elif count <= 5:
        confidence = ConfidenceLevel.DISCLOSURE
    else:
        confidence = ConfidenceLevel.HIGH_RISK
    return cleaned_text, confidence

# --- SEMANTIC NORMALIZATION ---

DOMAIN_TERM_MAPPINGS = {
    # Aerospace domain terms normalization (50+ entries)
    "aerodynamic drag": "drag",
    "lift force": "lift",
    "thrust vectoring": "thrust_vectoring",
    "flight control system": "flight_control_system",
    "avionics suite": "avionics",
    "propulsion system": "propulsion",
    "fuel consumption": "fuel_usage",
    "altitude hold": "altitude_control",
    "navigation system": "navigation",
    "autopilot mode": "autopilot",
    "stall warning": "stall_alert",
    "angle of attack": "aoa",
    "flight envelope": "flight_envelope",
    "engine thrust": "engine_thrust",
    "payload capacity": "payload",
    "structural integrity": "structure_integrity",
    "thermal protection": "thermal_protection",
    "mission planning": "mission_plan",
    "ground control": "ground_station",
    "data link": "communication_link",
    "flight path": "trajectory",
    "emergency procedures": "emergency_protocols",
    "system redundancy": "redundancy",
    "sensor fusion": "sensor_integration",
    "launch vehicle": "rocket",
    "orbital insertion": "orbit_insertion",
    "reentry trajectory": "reentry_path",
    "spacecraft attitude": "attitude_control",
    "guidance system": "guidance",
    "payload deployment": "payload_release",
    "mission timeline": "mission_schedule",
    "flight duration": "flight_time",
    "ground support equipment": "ground_support",
    "flight data recorder": "black_box",
    "flight safety": "safety",
    "weather conditions": "weather",
    "air traffic control": "atc",
    "flight clearance": "clearance",
    "emergency landing": "emergency_landing",
    "flight manual": "flight_manual",
    "maintenance schedule": "maintenance",
    "system diagnostics": "diagnostics",
    "flight simulator": "simulator",
    "pilot training": "training",
    "mission objectives": "objectives",
    "flight authorization": "authorization",
    "operational limits": "operational_limits",
    "flight test": "test_flight",
    "performance metrics": "performance",
    "fuel efficiency": "fuel_efficiency",
    "aircraft certification": "certification",
    "flight readiness": "readiness",
}

def normalize_query(text: str) -> str:
    lowered = text.lower()
    for phrase, normalized in DOMAIN_TERM_MAPPINGS.items():
        pattern = re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE)
        lowered = pattern.sub(normalized, lowered)
    # Remove extra spaces
    lowered = re.sub(r'\s+', ' ', lowered).strip()
    return lowered

# --- FACT FRAGILITY SCORING ---

def score_fact_fragility(fact: str) -> Dict[str, float]:
    """
    Scores a fact for:
    - verifiability: 0.0 (not verifiable) to 1.0 (fully verifiable)
    - recharacterization_risk: 0.0 (low risk) to 1.0 (high risk)
    - testimony_dependence: 0.0 (no dependence) to 1.0 (high dependence)
    """
    verifiability = 0.0
    recharacterization_risk = 0.0
    testimony_dependence = 0.0

    # Simple heuristics for demonstration:
    # Verifiability: presence of numeric data, references, or official terms
    if re.search(r'\b\d+(\.\d+)?\b', fact):
        verifiability += 0.4
    if re.search(r'\b(report|document|record|log|transcript|database|sensor)\b', fact, re.I):
        verifiability += 0.4
    if re.search(r'\b(witness|pilot|operator|engineer|controller)\b', fact, re.I):
        testimony_dependence += 0.5
    if re.search(r'\b(alleged|reported|claimed|suspected|purported)\b', fact, re.I):
        recharacterization_risk += 0.6
    if re.search(r'\b(approximate|estimated|likely|possible|probable)\b', fact, re.I):
        recharacterization_risk += 0.5
    # Clamp values
    verifiability = min(verifiability, 1.0)
    recharacterization_risk = min(recharacterization_risk, 1.0)
    testimony_dependence = min(testimony_dependence, 1.0)

    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence,
    }

# --- DEEP ANALYSIS ---

def multi_doctrine_decomposition(query: str) -> List[str]:
    """
    Decompose query into sub-issues based on doctrine keywords and semantic cues.
    """
    # For demonstration, split by conjunctions and known doctrine keywords
    doctrine_keywords = [
        "liability", "negligence", "causation", "damages", "breach",
        "standard of care", "foreseeability", "duty", "defense", "remedy",
        "jurisdiction", "authority", "compliance", "regulation", "procedure",
        "evidence", "testimony", "expert opinion", "statute", "precedent"
    ]
    lowered = query.lower()
    # Split by common conjunctions
    sub_issues = re.split(r'\b(?:and|or|but|however|although|whereas|while)\b', lowered)
    # Further split by doctrine keywords
    refined_issues = []
    for issue in sub_issues:
        issue = issue.strip()
        if not issue:
            continue
        # Check if doctrine keyword present
        matched = False
        for kw in doctrine_keywords:
            if kw in issue:
                refined_issues.append(issue)
                matched = True
                break
        if not matched:
            refined_issues.append(issue)
    # Deduplicate and clean
    unique_issues = list(dict.fromkeys([i.strip() for i in refined_issues if i.strip()]))
    return unique_issues

def build_interaction_dag(issues: List[str]) -> nx.DiGraph:
    """
    Build a dependency graph of issues.
    For demonstration, randomly assign dependencies based on keyword overlap.
    """
    G = nx.DiGraph()
    for i, issue in enumerate(issues):
        G.add_node(i, text=issue)
    # Simple heuristic: if issue A contains keywords that appear in issue B, A -> B
    for i, issue_i in enumerate(issues):
        words_i = set(issue_i.split())
        for j, issue_j in enumerate(issues):
            if i == j:
                continue
            words_j = set(issue_j.split())
            if words_i & words_j:
                # Add edge from i to j if i's words overlap with j's words
                G.add_edge(i, j)
    # Remove cycles if any
    try:
        cycles = list(nx.find_cycle(G))
        for edge in cycles:
            if G.has_edge(*edge):
                G.remove_edge(*edge)
    except nx.NetworkXNoCycle:
        pass
    return G

def eight_step_resolution(query: str, doctrines: List[str], sub_engine_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform full analysis with 8 steps:
    1. Normalize query
    2. Decompose into sub-issues
    3. Build interaction DAG
    4. Analyze each sub-issue with sub-engines
    5. Aggregate results
    6. Resolve conflicts
    7. Apply epistemic guardrails
    8. Generate final conclusion
    """
    normalized_query = normalize_query(query)
    sub_issues = multi_doctrine_decomposition(normalized_query)
    dag = build_interaction_dag(sub_issues)

    # Step 4: Analyze each sub-issue with sub-engines (simulate with sub_engine_results)
    analysis_results = {}
    for idx, issue in enumerate(sub_issues):
        key = issue
        # Use provided sub_engine_results or default placeholder
        analysis_results[key] = sub_engine_results.get(key, {"analysis": f"Analysis of '{issue}'", "confidence": ConfidenceLevel.DEFENSIBLE})

    # Step 5: Aggregate results (concatenate analyses)
    aggregated_analysis = "\n".join([res["analysis"] for res in analysis_results.values()])

    # Step 6: Resolve conflicts (simulate by checking confidence levels)
    confidences = [res["confidence"] for res in analysis_results.values()]
    if ConfidenceLevel.HIGH_RISK in confidences:
        final_confidence = ConfidenceLevel.HIGH_RISK
    elif ConfidenceLevel.DISCLOSURE in confidences:
        final_confidence = ConfidenceLevel.DISCLOSURE
    elif ConfidenceLevel.AGGRESSIVE in confidences:
        final_confidence = ConfidenceLevel.AGGRESSIVE
    else:
        final_confidence = ConfidenceLevel.DEFENSIBLE

    # Step 7: Apply epistemic guardrails
    cleaned_text, confidence_after_guardrails = apply_epistemic_guardrails(aggregated_analysis)

    # Step 8: Generate final conclusion object
    conclusion = {
        "original_query": query,
        "normalized_query": normalized_query,
        "sub_issues": sub_issues,
        "interaction_dag": dag,
        "aggregated_analysis": aggregated_analysis,
        "cleaned_analysis": cleaned_text,
        "final_confidence": final_confidence,
        "confidence_after_guardrails": confidence_after_guardrails,
    }
    return conclusion

def zoned_analysis(conclusion: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tag conclusion with zones: PLANNING, REPORTING, AUDIT
    Based on confidence and content heuristics.
    """
    text = conclusion.get("cleaned_analysis", "").lower()
    confidence = conclusion.get("confidence_after_guardrails", ConfidenceLevel.DEFENSIBLE)

    zones = set()

    # Heuristics:
    if confidence in {ConfidenceLevel.DEFENSIBLE, ConfidenceLevel.AGGRESSIVE}:
        zones.add("PLANNING")
    if "report" in text or "summary" in text or "analysis" in text:
        zones.add("REPORTING")
    if "audit" in text or "compliance" in text or "verification" in text:
        zones.add("AUDIT")
    if not zones:
        zones.add("REPORTING")  # Default zone

    conclusion["zones"] = list(zones)
    return conclusion

# --- THREE LAYER RESPONSE SYSTEM ---

# Simulated doctrine cache for layer 1
_DOCTRINE_CACHE = {
    "stall warning": "Cached analysis: Stall warning procedures and implications.",
    "fuel consumption": "Cached analysis: Fuel consumption optimization techniques.",
    "flight control system": "Cached analysis: Flight control system reliability and failure modes.",
}

# Simulated sub-engines for layer 2
def sub_engine_a(query: str) -> str:
    time.sleep(0.1)  # simulate processing delay
    return f"Sub-engine A analysis for '{query}'"

def sub_engine_b(query: str) -> str:
    time.sleep(0.15)
    return f"Sub-engine B analysis for '{query}'"

def sub_engine_c(query: str) -> str:
    time.sleep(0.2)
    return f"Sub-engine C analysis for '{query}'"

_SUB_ENGINES = {
    "performance": sub_engine_a,
    "safety": sub_engine_b,
    "regulatory": sub_engine_c,
}

def doctrine_cache_lookup(query: str) -> Optional[str]:
    """
    Layer 1: Lookup doctrine cache for keywords within 200ms.
    """
    start = time.time()
    lowered = query.lower()
    for key in _DOCTRINE_CACHE:
        if key in lowered:
            elapsed = (time.time() - start) * 1000
            if elapsed <= 200:
                return _DOCTRINE_CACHE[key]
    return None

def semantic_search_sub_engine_routing(query: str) -> Dict[str, str]:
    """
    Layer 2: Semantic search + sub-engine routing.
    Dispatch query to relevant sub-engines based on keyword matching.
    """
    lowered = query.lower()
    results = {}
    for domain_key, engine_func in _SUB_ENGINES.items():
        if domain_key in lowered:
            results[domain_key] = engine_func(query)
    if not results:
        # Default dispatch to all sub-engines if no keyword matched
        for domain_key, engine_func in _SUB_ENGINES.items():
            results[domain_key] = engine_func(query)
    return results

def deep_multi_engine_analysis(query: str) -> Dict[str, Any]:
    """
    Layer 3: Parallel dispatch to multiple engines, merge results, resolve conflicts.
    """
    # For demonstration, dispatch to all sub-engines in parallel
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(_SUB_ENGINES)) as executor:
        future_to_key = {executor.submit(engine, query): key for key, engine in _SUB_ENGINES.items()}
        for future in concurrent.futures.as_completed(future_to_key):
            key = future_to_key[future]
            try:
                result = future.result()
            except Exception as exc:
                result = f"Error in {key}: {exc}"
            results[key] = result

    # Merge results: concatenate with conflict resolution (simulate)
    merged_text = "\n".join(results.values())
    # Conflict resolution: if conflicting keywords found, append note
    conflicts = []
    if "error" in merged_text.lower():
        conflicts.append("Error detected in sub-engine results.")
    merged_result = {
        "merged_text": merged_text,
        "conflicts": conflicts,
        "resolved": len(conflicts) == 0,
    }
    return merged_result

class AerospaceIntelligenceEngine:
    """
    Aerospace Intelligence Engine — Domain Orchestrator — Domain orchestrator
    """

    def __init__(self):
        self.lock = threading.Lock()
        self.doctrine_cache = _DOCTRINE_CACHE.copy()
        self.sub_engines = _SUB_ENGINES.copy()

    def three_layer_response(self, query: str) -> Dict[str, Any]:
        """
        Implements the three-layer response system:
        Layer 1: Doctrine cache lookup (0-200ms)
        Layer 2: Semantic search + sub-engine routing
        Layer 3: Deep multi-engine analysis
        """
        # Layer 1
        cache_result = doctrine_cache_lookup(query)
        if cache_result:
            return {
                "layer": 1,
                "result": cache_result,
            }

        # Layer 2
        layer2_results = semantic_search_sub_engine_routing(query)
        if layer2_results:
            return {
                "layer": 2,
                "result": layer2_results,
            }

        # Layer 3
        layer3_result = deep_multi_engine_analysis(query)
        return {
            "layer": 3,
            "result": layer3_result,
        }

# Instantiate singleton engine
aerospace_engine = AerospaceIntelligenceEngine()

@dataclass
class QueryTelemetry:
    query_id: str
    timestamp: float
    latency_ms: float
    cache_hit: bool
    engines_invoked: List[str]
    mode: str
    confidence: float
    error: Optional[str] = None

class TelemetryCollector:
    def __init__(self):
        self._lock = threading.Lock()
        self._queries: Deque[QueryTelemetry] = deque(maxlen=100000)
        self._errors: Deque[QueryTelemetry] = deque(maxlen=10000)
        self._doctrine_hits: Counter = Counter()
        self._doctrine_total: Counter = Counter()
        self._sub_engine_stats: Dict[str, List[float]] = defaultdict(list)
        self._sub_engine_errors: Dict[str, int] = defaultdict(int)
        self._sub_engine_invocations: Dict[str, int] = defaultdict(int)

    def record_query(self, telemetry: QueryTelemetry):
        with self._lock:
            self._queries.append(telemetry)
            for engine in telemetry.engines_invoked:
                self._sub_engine_stats[engine].append(telemetry.latency_ms)
                self._sub_engine_invocations[engine] += 1
            if telemetry.cache_hit:
                self._doctrine_hits[telemetry.mode] += 1
            self._doctrine_total[telemetry.mode] += 1

    def record_error(self, telemetry: QueryTelemetry):
        with self._lock:
            self._errors.append(telemetry)
            for engine in telemetry.engines_invoked:
                self._sub_engine_errors[engine] += 1

    def get_latency_stats(self) -> Dict[str, Any]:
        with self._lock:
            latencies = [q.latency_ms for q in self._queries]
            if not latencies:
                return {}
            latencies_sorted = sorted(latencies)
            n = len(latencies_sorted)
            stats = {
                "avg": statistics.mean(latencies_sorted),
                "p50": latencies_sorted[int(n * 0.5)],
                "p95": latencies_sorted[int(n * 0.95) - 1],
                "p99": latencies_sorted[int(n * 0.99) - 1],
                "min": latencies_sorted[0],
                "max": latencies_sorted[-1],
                "count": n,
            }
            return stats

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        with self._lock:
            rates = {}
            for mode in self._doctrine_total:
                total = self._doctrine_total[mode]
                hits = self._doctrine_hits.get(mode, 0)
                rates[mode] = hits / total if total > 0 else 0.0
            return rates

    def queries_last_hour(self) -> int:
        one_hour_ago = time.time() - 3600
        with self._lock:
            return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_sub_engine_stats(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            stats = {}
            for engine, latencies in self._sub_engine_stats.items():
                if not latencies:
                    continue
                lat_sorted = sorted(latencies)
                n = len(lat_sorted)
                stats[engine] = {
                    "avg_latency": statistics.mean(lat_sorted),
                    "p95_latency": lat_sorted[int(n * 0.95) - 1],
                    "invocations": self._sub_engine_invocations[engine],
                    "errors": self._sub_engine_errors[engine],
                    "error_rate": self._sub_engine_errors[engine] / self._sub_engine_invocations[engine]
                        if self._sub_engine_invocations[engine] > 0 else 0.0
                }
            return stats

# 2. DRIFT_WATCHER

class DriftWatcher:
    def __init__(self, window_size: int = 1000, alert_threshold: float = 0.10):
        self._lock = threading.Lock()
        self._baselines: Dict[str, float] = {}  # doctrine -> baseline confidence
        self._history: Dict[str, Deque[float]] = defaultdict(lambda: deque(maxlen=window_size))
        self._alert_threshold = alert_threshold
        self._last_alerted: Dict[str, float] = {}

    def record_baseline(self, doctrine: str, confidence: float):
        with self._lock:
            if doctrine not in self._baselines:
                self._baselines[doctrine] = confidence
            self._history[doctrine].append(confidence)

    def detect_drift(self, doctrine: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            if doctrine not in self._baselines or not self._history[doctrine]:
                return None
            baseline = self._baselines[doctrine]
            recent = list(self._history[doctrine])
            if not recent:
                return None
            avg_recent = statistics.mean(recent)
            drift = avg_recent - baseline
            drift_pct = drift / baseline if baseline != 0 else 0.0
            last_alert = self._last_alerted.get(doctrine, 0)
            now = time.time()
            # Alert if drift exceeds threshold and not alerted in last 10 min
            if abs(drift_pct) > self._alert_threshold and now - last_alert > 600:
                self._last_alerted[doctrine] = now
                return {
                    "doctrine": doctrine,
                    "baseline_confidence": baseline,
                    "recent_avg_confidence": avg_recent,
                    "drift": drift,
                    "drift_pct": drift_pct,
                    "alert": True,
                    "timestamp": now
                }
            return {
                "doctrine": doctrine,
                "baseline_confidence": baseline,
                "recent_avg_confidence": avg_recent,
                "drift": drift,
                "drift_pct": drift_pct,
                "alert": False,
                "timestamp": now
            }

    def get_drift_report(self) -> List[Dict[str, Any]]:
        with self._lock:
            report = []
            for doctrine in self._baselines:
                d = self.detect_drift(doctrine)
                if d:
                    report.append(d)
            return report

# 3. COVERAGE_MAP

class CoverageTracker:
    def __init__(self):
        self._lock = threading.Lock()
        self._triggered: Counter = Counter()  # doctrine -> count
        self._missed: Deque[Tuple[str, float]] = deque(maxlen=10000)  # (query_id, timestamp)
        self._sub_engine_coverage: Dict[str, Counter] = defaultdict(Counter)
        self._epistemic_gap: Deque[Tuple[str, float, str]] = deque(maxlen=10000)  # (query_id, timestamp, query_text)

    def record_triggered(self, doctrine: str, sub_engine: Optional[str] = None):
        with self._lock:
            self._triggered[doctrine] += 1
            if sub_engine:
                self._sub_engine_coverage[sub_engine][doctrine] += 1

    def record_missed(self, query_id: str, query_text: str):
        with self._lock:
            self._missed.append((query_id, time.time()))
            self._epistemic_gap.append((query_id, time.time(), query_text))

    def get_coverage_report(self) -> Dict[str, Any]:
        with self._lock:
            total = sum(self._triggered.values())
            doctrine_coverage = dict(self._triggered)
            missed = list(self._missed)
            epistemic_gap = list(self._epistemic_gap)
            sub_engine_stats = {
                se: dict(cnt) for se, cnt in self._sub_engine_coverage.items()
            }
            return {
                "total_triggered": total,
                "doctrine_coverage": doctrine_coverage,
                "missed_queries": missed,
                "epistemic_gaps": epistemic_gap,
                "sub_engine_coverage": sub_engine_stats
            }

    def identify_epistemic_gaps(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [
                {"query_id": qid, "timestamp": ts, "query_text": qtxt}
                for (qid, ts, qtxt) in self._epistemic_gap
            ]

    def get_sub_engine_coverage_stats(self) -> Dict[str, Dict[str, int]]:
        with self._lock:
            return {
                se: dict(cnt) for se, cnt in self._sub_engine_coverage.items()
            }

# 4. DETERMINISM_HASH

def compute_determinism_hash(query: Any, response: Any) -> str:
    def _serialize(obj):
        if isinstance(obj, (dict, list, tuple)):
            return json.dumps(obj, sort_keys=True, separators=(',', ':'))
        return str(obj)
    query_bytes = _serialize(query).encode('utf-8')
    response_bytes = _serialize(response).encode('utf-8')
    h = hashlib.sha256()
    h.update(query_bytes)
    h.update(response_bytes)
    return h.hexdigest()

def verify_reproducibility(query: Any, response: Any, expected_hash: str) -> bool:
    actual_hash = compute_determinism_hash(query, response)
    return actual_hash == expected_hash

# 5. AUDIT_TRAIL

class AuditTrailWriter:
    def __init__(self, audit_dir: str = "./audit_trail"):
        self.audit_dir = audit_dir
        os.makedirs(audit_dir, exist_ok=True)
        self._lock = threading.Lock()
        self._current_date = None
        self._file = None
        self._open_new_file()

    def _get_audit_filename(self, date: datetime.date) -> str:
        return os.path.join(self.audit_dir, f"audit_{date.isoformat()}.jsonl")

    def _open_new_file(self):
        with self._lock:
            today = datetime.date.today()
            if self._current_date != today:
                if self._file:
                    self._file.close()
                self._current_date = today
                filename = self._get_audit_filename(today)
                self._file = open(filename, "a", encoding="utf-8")

    def write(self, query_id: str, timestamp: float, engine_id: str, engines_invoked: List[str],
              mode: str, confidence: float, latency: float, cache_hit: bool):
        with self._lock:
            self._open_new_file()
            record = {
                "query_id": query_id,
                "timestamp": timestamp,
                "engine_id": engine_id,
                "engines_invoked": engines_invoked,
                "mode": mode,
                "confidence": confidence,
                "latency": latency,
                "cache_hit": cache_hit
            }
            self._file.write(json.dumps(record, separators=(',', ':')) + "\n")
            self._file.flush()

    def close(self):
        with self._lock:
            if self._file:
                self._file.close()
                self._file = None

    def forensic_replay(self, date: datetime.date) -> List[Dict[str, Any]]:
        filename = self._get_audit_filename(date)
        if not os.path.exists(filename):
            return []
        with open(filename, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f]

# 6. PERFORMANCE_PROFILER

class PerformanceProfiler:
    def __init__(self):
        self._lock = threading.Lock()
        self._latency: Dict[str, List[float]] = defaultdict(list)
        self._errors: Dict[str, int] = defaultdict(int)
        self._invocations: Dict[str, int] = defaultdict(int)
        self._availability: Dict[str, List[bool]] = defaultdict(list)
        self._sla_targets: Dict[str, Dict[str, float]] = {}  # sub_engine -> {"max_latency": ms, "min_availability": float}

    def set_sla(self, sub_engine: str, max_latency: float, min_availability: float):
        with self._lock:
            self._sla_targets[sub_engine] = {
                "max_latency": max_latency,
                "min_availability": min_availability
            }

    def record(self, sub_engine: str, latency_ms: float, error: bool, available: bool):
        with self._lock:
            self._latency[sub_engine].append(latency_ms)
            self._invocations[sub_engine] += 1
            if error:
                self._errors[sub_engine] += 1
            self._availability[sub_engine].append(available)

    def get_stats(self, sub_engine: str) -> Dict[str, Any]:
        with self._lock:
            lat = self._latency[sub_engine]
            if not lat:
                return {}
            lat_sorted = sorted(lat)
            n = len(lat_sorted)
            error_count = self._errors[sub_engine]
            invocations = self._invocations[sub_engine]
            avail = self._availability[sub_engine]
            availability_rate = sum(avail) / len(avail) if avail else 1.0
            sla = self._sla_targets.get(sub_engine, {})
            stats = {
                "avg_latency": statistics.mean(lat_sorted),
                "p95_latency": lat_sorted[int(n * 0.95) - 1],
                "max_latency": max(lat_sorted),
                "min_latency": min(lat_sorted),
                "invocations": invocations,
                "errors": error_count,
                "error_rate": error_count / invocations if invocations else 0.0,
                "availability": availability_rate,
                "sla": sla,
                "sla_breach": False
            }
            if sla:
                if stats["p95_latency"] > sla.get("max_latency", float('inf')) or \
                   availability_rate < sla.get("min_availability", 0.0):
                    stats["sla_breach"] = True
            return stats

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return {se: self.get_stats(se) for se in self._latency}

    def get_sla_breaches(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return {se: stats for se, stats in self.get_all_stats().items() if stats.get("sla_breach")}

# --- END OF PART 5 ---

logger = logging.getLogger("aeroie")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Constants
ENGINE_ID = "AEROIE"
ENGINE_PORT = 8859
SUB_ENGINES = {
    "AERO01": "Aerodynamics",
    "AERO02": "Propulsion",
    "AERO03": "Structures",
    "AERO04": "Avionics",
    "AERO05": "Flight Mechanics",
    "AERO06": "Aircraft Design",
    "AERO07": "Space Systems",
    "AERO08": "Materials Aerospace",
    "AERO09": "Maintenance MRO",
    "AERO10": "Air Traffic Management",
}
SUB_ENGINE_TIMEOUT = 5  # seconds timeout for sub-engine calls
CIRCUIT_BREAKER_THRESHOLD = 3  # failures before open circuit
CIRCUIT_BREAKER_RESET_TIME = 60  # seconds before trying closed again

# Global state for telemetry and cache
class Telemetry:
    def __init__(self):
        self.latencies = []
        self.cache_hits = 0
        self.cache_misses = 0
        self.query_timestamps = []
        self.sub_engine_stats = {k: {"calls": 0, "failures": 0, "latencies": []} for k in SUB_ENGINES.keys()}

    def record_latency(self, latency: float):
        self.latencies.append(latency)

    def record_cache_hit(self):
        self.cache_hits += 1

    def record_cache_miss(self):
        self.cache_misses += 1

    def record_query(self):
        self.query_timestamps.append(time.time())

    def record_sub_engine_call(self, engine_id: str, latency: float, success: bool):
        stats = self.sub_engine_stats.get(engine_id)
        if stats is None:
            stats = {"calls": 0, "failures": 0, "latencies": []}
            self.sub_engine_stats[engine_id] = stats
        stats["calls"] += 1
        if not success:
            stats["failures"] += 1
        stats["latencies"].append(latency)

    def queries_per_hour(self) -> float:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self.query_timestamps if t >= one_hour_ago)
        return count

    def cache_hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return self.cache_hits / total

telemetry = Telemetry()

# Circuit breaker state per sub-engine
class CircuitBreaker:
    def __init__(self):
        self.failures = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF-OPEN
        self.last_failure_time = None

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= CIRCUIT_BREAKER_THRESHOLD:
            self.state = "OPEN"
            logger.warning(f"Circuit breaker OPEN due to failures")

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_time = None

    def can_call(self) -> bool:
        if self.state == "CLOSED":
            return True
        elif self.state == "OPEN":
            # Check if reset time passed
            if self.last_failure_time and (time.time() - self.last_failure_time) > CIRCUIT_BREAKER_RESET_TIME:
                self.state = "HALF-OPEN"
                return True
            return False
        elif self.state == "HALF-OPEN":
            return True
        return False

circuit_breakers = {k: CircuitBreaker() for k in SUB_ENGINES.keys()}

# Doctrine cache and search index (mocked)
class DoctrineCache:
    def __init__(self):
        self.cache = {}  # key: doctrine_id, value: doctrine data

    async def initialize(self):
        # Simulate loading doctrines from DB or file
        await asyncio.sleep(0.1)
        # Seed with dummy doctrines
        for i in range(1, 21):
            doctrine_id = f"DOC{i:03d}"
            self.cache[doctrine_id] = {
                "id": doctrine_id,
                "title": f"Doctrine {i}",
                "domain": random.choice(list(SUB_ENGINES.values())),
                "content": f"Content of doctrine {i}",
                "coverage": random.uniform(0.5, 1.0),
                "epistemic_gaps": random.uniform(0.0, 0.5),
            }
        logger.info("Doctrine cache initialized with %d doctrines", len(self.cache))

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self.cache.values())

    def get(self, doctrine_id: str) -> Optional[Dict[str, Any]]:
        return self.cache.get(doctrine_id)

doctrine_cache = DoctrineCache()

# Search index (mocked)
class SearchIndex:
    def __init__(self):
        self.index = {}  # simplistic inverted index

    async def seed(self, doctrines: List[Dict[str, Any]]):
        await asyncio.sleep(0.1)
        self.index.clear()
        for doc in doctrines:
            words = doc["content"].lower().split()
            for w in words:
                self.index.setdefault(w, set()).add(doc["id"])
        logger.info("Search index seeded with %d doctrines", len(doctrines))

    def search(self, query: str) -> List[str]:
        words = query.lower().split()
        if not words:
            return []
        sets = [self.index.get(w, set()) for w in words]
        if not sets:
            return []
        result = set.intersection(*sets)
        return list(result)

search_index = SearchIndex()

# Health monitor (mocked)
class HealthMonitor:
    def __init__(self):
        self.status = "starting"
        self.sub_engine_health = {k: {"status": "unknown", "last_checked": None} for k in SUB_ENGINES.keys()}
        self._task = None
        self._stop_event = asyncio.Event()

    async def start(self):
        self.status = "running"
        self._stop_event.clear()
        self._task = asyncio.create_task(self._monitor_loop())
        logger.info("Health monitor started")

    async def stop(self):
        self.status = "stopping"
        self._stop_event.set()
        if self._task:
            await self._task
        self.status = "stopped"
        logger.info("Health monitor stopped")

    async def _monitor_loop(self):
        while not self._stop_event.is_set():
            await self._check_sub_engines()
            await asyncio.sleep(10)

    async def _check_sub_engines(self):
        for engine_id in SUB_ENGINES.keys():
            # Simulate health check with random success/failure
            success = random.random() > 0.05
            self.sub_engine_health[engine_id]["status"] = "healthy" if success else "unhealthy"
            self.sub_engine_health[engine_id]["last_checked"] = datetime.datetime.utcnow().isoformat()
            logger.debug(f"Health check {engine_id}: {self.sub_engine_health[engine_id]['status']}")

health_monitor = HealthMonitor()

# Telemetry system (mocked)
class TelemetrySystem:
    def __init__(self):
        self.running = False

    async def start(self):
        self.running = True
        logger.info("Telemetry system started")

    async def stop(self):
        self.running = False
        logger.info("Telemetry system stopped")

telemetry_system = TelemetrySystem()

# Models for requests and responses
class QueryRequest(BaseModel):
    query: str
    parameters: Optional[Dict[str, Any]] = None

class RouteRequest(BaseModel):
    query: str

class AnalyzeRequest(BaseModel):
    query: str
    depth: Optional[int] = 3

class SubEngineResponse(BaseModel):
    engine_id: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    latency: float

class QueryResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    metadata: Dict[str, Any]

class HealthResponse(BaseModel):
    engine_status: str
    sub_engines: Dict[str, Dict[str, Any]]

class MetricsResponse(BaseModel):
    latency_stats: Dict[str, float]
    cache_hit_rate: float
    queries_per_hour: float
    sub_engine_stats: Dict[str, Dict[str, Any]]

class CoverageResponse(BaseModel):
    doctrines: List[Dict[str, Any]]
    epistemic_gaps_summary: Dict[str, float]

class DriftResponse(BaseModel):
    drift_detected: bool
    details: Optional[Dict[str, Any]]

class DoctrinesResponse(BaseModel):
    doctrines: List[Dict[str, Any]]

class RoutingResponse(BaseModel):
    routing_rules: Dict[str, Any]
    engine_registry: Dict[str, str]

class SubEnginesResponse(BaseModel):
    health_dashboard: Dict[str, Dict[str, Any]]

class RouteDryRunResponse(BaseModel):
    engines_invoked: List[str]

class AnalyzeResponse(BaseModel):
    analysis: Dict[str, Any]

# Helper functions for query flow
async def normalize_query(query: str) -> str:
    normalized = query.strip().lower()
    logger.debug(f"Normalized query: {normalized}")
    return normalized

async def classify_domain(query: str) -> str:
    # Simple keyword-based classification for demo
    keywords_map = {
        "aero01": ["lift", "drag", "airflow", "wing"],
        "aero02": ["engine", "thrust", "combustion", "propulsion"],
        "aero03": ["stress", "strain", "material", "structure"],
        "aero04": ["avionics", "navigation", "radar", "communication"],
        "aero05": ["flight", "trajectory", "control", "maneuver"],
        "aero06": ["design", "configuration", "layout", "optimization"],
        "aero07": ["space", "orbit", "satellite", "rocket"],
        "aero08": ["composite", "alloy", "fatigue", "corrosion"],
        "aero09": ["maintenance", "inspection", "repair", "mro"],
        "aero10": ["traffic", "airspace", "controller", "routing"],
    }
    query_lower = query.lower()
    for engine_id, kws in keywords_map.items():
        for kw in kws:
            if kw in query_lower:
                logger.debug(f"Classified domain {engine_id} for query '{query}'")
                return engine_id.upper()
    logger.debug(f"Default classification to AERO06 for query '{query}'")
    return "AERO06"  # default fallback

async def route_query(domain: str) -> List[str]:
    # For demo, route to classified domain plus one random related engine
    routes = [domain]
    related = list(SUB_ENGINES.keys())
    related.remove(domain)
    if related:
        routes.append(random.choice(related))
    logger.debug(f"Routing query to engines: {routes}")
    return routes

async def dispatch_to_sub_engine(engine_id: str, query: str, parameters: Optional[Dict[str, Any]]) -> SubEngineResponse:
    if not circuit_breakers[engine_id].can_call():
        logger.warning(f"Circuit breaker open for {engine_id}, skipping call")
        return SubEngineResponse(engine_id=engine_id, success=False, error="Circuit breaker open", latency=0.0)
    start = time.perf_counter()
    try:
        # Simulate network call with random delay and random failure
        delay = random.uniform(0.1, 1.0)
        await asyncio.sleep(delay)
        if random.random() < 0.1:
            raise Exception("Simulated sub-engine failure")
        # Simulated response data
        data = {
            "engine": engine_id,
            "response": f"Processed query '{query}' with parameters {parameters}",
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }
        latency = time.perf_counter() - start
        circuit_breakers[engine_id].record_success()
        telemetry.record_sub_engine_call(engine_id, latency, True)
        logger.debug(f"Sub-engine {engine_id} responded in {latency:.3f}s")
        return SubEngineResponse(engine_id=engine_id, success=True, data=data, latency=latency)
    except Exception as e:
        latency = time.perf_counter() - start
        circuit_breakers[engine_id].record_failure()
        telemetry.record_sub_engine_call(engine_id, latency, False)
        logger.error(f"Sub-engine {engine_id} failed: {str(e)}")
        return SubEngineResponse(engine_id=engine_id, success=False, error=str(e), latency=latency)

async def merge_responses(responses: List[SubEngineResponse]) -> List[Dict[str, Any]]:
    merged = []
    for resp in responses:
        if resp.success and resp.data:
            merged.append(resp.data)
    logger.debug(f"Merged {len(merged)} successful sub-engine responses")
    return merged

async def apply_guardrails(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # For demo, filter out any results containing forbidden words
    forbidden = ["error", "fail"]
    filtered = []
    for r in results:
        text = str(r).lower()
        if any(f in text for f in forbidden):
            logger.warning("Guardrail filtered out a result due to forbidden content")
            continue
        filtered.append(r)
    return filtered

def hash_response(results: List[Dict[str, Any]]) -> str:
    m = hashlib.sha256()
    for r in results:
        m.update(str(r).encode("utf-8"))
    digest = m.hexdigest()
    logger.debug(f"Response hash: {digest}")
    return digest

async def log_query(query: str, response_hash: str, latency: float):
    logger.info(f"Query logged: '{query}' hash={response_hash} latency={latency:.3f}s")

# FastAPI app and lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting {ENGINE_ID} engine on port {ENGINE_PORT}")
    await doctrine_cache.initialize()
    await search_index.seed(doctrine_cache.get_all())
    await health_monitor.start()
    await telemetry_system.start()
    yield
    # Shutdown
    await health_monitor.stop()
    await telemetry_system.stop()
    logger.info(f"Stopped {ENGINE_ID} engine")

app = FastAPI(title="Aerospace Intelligence Engine — Domain Orchestrator", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

# Endpoint implementations

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    start_time = time.perf_counter()
    telemetry.record_query()
    query = req.query
    parameters = req.parameters or {}

    # Query flow: normalize -> classify -> route -> dispatch -> merge -> guardrails -> hash -> log -> respond
    normalized_query = await normalize_query(query)
    domain = await classify_domain(normalized_query)
    routes = await route_query(domain)

    # Dispatch concurrently with timeout and circuit breaker checks
    tasks = []
    for engine_id in routes:
        tasks.append(dispatch_to_sub_engine(engine_id, normalized_query, parameters))
    try:
        responses = await asyncio.wait_for(asyncio.gather(*tasks), timeout=SUB_ENGINE_TIMEOUT)
    except asyncio.TimeoutError:
        logger.warning("Timeout waiting for sub-engine responses")
        # Fallback: try doctrine cache
        cached_doctrines = doctrine_cache.get_all()
        telemetry.record_cache_hit()
        latency = time.perf_counter() - start_time
        response_hash = hash_response(cached_doctrines)
        await log_query(query, response_hash, latency)
        return QueryResponse(
            query=query,
            results=cached_doctrines,
            metadata={"source": "doctrine_cache", "latency": latency, "cache_hit": True},
        )

    # Check if all failed
    if all(not r.success for r in responses):
        # Fallback to doctrine cache
        cached_doctrines = doctrine_cache.get_all()
        telemetry.record_cache_hit()
        latency = time.perf_counter() - start_time
        response_hash = hash_response(cached_doctrines)
        await log_query(query, response_hash, latency)
        return QueryResponse(
            query=query,
            results=cached_doctrines,
            metadata={"source": "doctrine_cache", "latency": latency, "cache_hit": True},
        )

    telemetry.record_cache_miss()
    merged_results = await merge_responses(responses)
    guarded_results = await apply_guardrails(merged_results)
    latency = time.perf_counter() - start_time
    response_hash = hash_response(guarded_results)
    await log_query(query, response_hash, latency)
    telemetry.record_latency(latency)

    return QueryResponse(
        query=query,
        results=guarded_results,
        metadata={
            "source": "sub_engines",
            "latency": latency,
            "cache_hit": False,
            "engines_queried": routes,
            "response_hash": response_hash,
        },
    )

@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    # Compose health from self + sub-engines
    engine_status = "healthy" if health_monitor.status == "running" else "unhealthy"
    sub_engines_health = health_monitor.sub_engine_health
    return HealthResponse(engine_status=engine_status, sub_engines=sub_engines_health)

@app.get("/metrics", response_model=MetricsResponse)
async def metrics_endpoint():
    latencies = telemetry.latencies
    latency_stats = {}
    if latencies:
        latency_stats = {
            "min": min(latencies),
            "max": max(latencies),
            "mean": statistics.mean(latencies),
            "median": statistics.median(latencies),
            "p90": statistics.quantiles(latencies, n=10)[8],
        }
    else:
        latency_stats = {"min": 0, "max": 0, "mean": 0, "median": 0, "p90": 0}

    cache_hit_rate = telemetry.cache_hit_rate()
    queries_per_hour = telemetry.queries_per_hour()
    sub_engine_stats = {}
    for engine_id, stats in telemetry.sub_engine_stats.items():
        calls = stats["calls"]
        failures = stats["failures"]
        lat_list = stats["latencies"]
        if lat_list:
            avg_latency = statistics.mean(lat_list)
        else:
            avg_latency = 0.0
        sub_engine_stats[engine_id] = {
            "calls": calls,
            "failures": failures,
            "avg_latency": avg_latency,
            "failure_rate": failures / calls if calls > 0 else 0.0,
        }

    return MetricsResponse(
        latency_stats=latency_stats,
        cache_hit_rate=cache_hit_rate,
        queries_per_hour=queries_per_hour,
        sub_engine_stats=sub_engine_stats,
    )

@app.get("/coverage", response_model=CoverageResponse)
async def coverage_endpoint():
    doctrines = doctrine_cache.get_all()
    if not doctrines:
        return CoverageResponse(doctrines=[], epistemic_gaps_summary={})
    coverage_values = [d.get("coverage", 0.0) for d in doctrines]
    epistemic_gaps = [d.get("epistemic_gaps", 0.0) for d in doctrines]
    summary = {
        "average_coverage": sum(coverage_values) / len(coverage_values),
        "max_coverage": max(coverage_values),
        "min_coverage": min(coverage_values),
        "average_epistemic_gaps": sum(epistemic_gaps) / len(epistemic_gaps),
        "max_epistemic_gaps": max(epistemic_gaps),
        "min_epistemic_gaps": min(epistemic_gaps),
    }
    return CoverageResponse(doctrines=doctrines, epistemic_gaps_summary=summary)

@app.get("/drift", response_model=DriftResponse)
async def drift_endpoint():
    # Simulate drift detection logic
    drift_detected = random.random() < 0.1
    details = None
    if drift_detected:
        details = {
            "detected_at": datetime.datetime.utcnow().isoformat(),
            "affected_domains": random.sample(list(SUB_ENGINES.values()), k=2),
            "severity": random.choice(["low", "medium", "high"]),
        }
    return DriftResponse(drift_detected=drift_detected, details=details)

@app.get("/doctrines", response_model=DoctrinesResponse)
async def doctrines_endpoint():
    doctrines = doctrine_cache.get_all()
    return DoctrinesResponse(doctrines=doctrines)

@app.get("/routing", response_model=RoutingResponse)
async def routing_endpoint():
    # For demo, static routing rules
    routing_rules = {
        "keywords_map": {
            "lift": "AERO01",
            "engine": "AERO02",
            "stress": "AERO03",
            "avionics": "AERO04",
            "flight": "AERO05",
            "design": "AERO06",
            "space": "AERO07",
            "composite": "AERO08",
            "maintenance": "AERO09",
            "traffic": "AERO10",
        },
        "default_route": "AERO06",
    }
    engine_registry = SUB_ENGINES
    return RoutingResponse(routing_rules=routing_rules, engine_registry=engine_registry)

@app.get("/sub-engines", response_model=SubEnginesResponse)
async def sub_engines_endpoint():
    health_dashboard = health_monitor.sub_engine_health
    return SubEnginesResponse(health_dashboard=health_dashboard)

@app.post("/route", response_model=RouteDryRunResponse)
async def route_dry_run_endpoint(req: RouteRequest):
    normalized_query = await normalize_query(req.query)
    domain = await classify_domain(normalized_query)
    routes = await route_query(domain)
    return RouteDryRunResponse(engines_invoked=routes)

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(req: AnalyzeRequest):
    query = req.query
    depth = req.depth or 3
    # Simulate deep multi-engine analysis with dummy data
    analysis = {
        "query": query,
        "depth": depth,
        "steps": [],
        "summary": None,
    }
    current_query = query
    for i in range(depth):
        domain = await classify_domain(current_query)
        routes = await route_query(domain)
        analysis["steps"].append({
            "step": i + 1,
            "domain": domain,
            "routes": routes,
            "analysis_result": f"Simulated analysis result for step {i + 1}",
        })
        # For demo, next query is previous plus step number
        current_query = f"{current_query} step{i+1}"
    analysis["summary"] = f"Completed {depth} steps of multi-engine analysis"
    return AnalyzeResponse(analysis=analysis)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=ENGINE_PORT, log_level="info")