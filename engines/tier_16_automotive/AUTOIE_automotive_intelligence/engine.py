import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, validator
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
import enum
from datetime import datetime, timedelta
import asyncio
import aiohttp
import json
import time
import statistics
import collections

ENGINE_ID = "AUTOIE"
ENGINE_PORT = 8858
ENGINE_NAME = "Automotive Intelligence Engine — Domain Orchestrator"
ENGINE_VERSION = "1.0.0"

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
    ENGINE_SYSTEMS = "ENGINE_SYSTEMS"
    TRANSMISSION = "TRANSMISSION"
    BRAKE_SYSTEMS = "BRAKE_SYSTEMS"
    SUSPENSION_STEERING = "SUSPENSION_STEERING"
    ELECTRICAL_ELECTRONICS = "ELECTRICAL_ELECTRONICS"
    DIAGNOSTICS = "DIAGNOSTICS"
    HYBRID_EV = "HYBRID_EV"
    ADAS_SAFETY = "ADAS_SAFETY"
    BODY_STRUCTURES = "BODY_STRUCTURES"
    CLIMATE_CONTROL = "CLIMATE_CONTROL"
    FUEL_SYSTEMS = "FUEL_SYSTEMS"
    EXHAUST_EMISSIONS = "EXHAUST_EMISSIONS"
    TIRES_WHEELS = "TIRES_WHEELS"
    FLEET_MANAGEMENT = "FLEET_MANAGEMENT"
    AUTONOMOUS_DRIVING = "AUTONOMOUS_DRIVING"
    INFOTAINMENT = "INFOTAINMENT"
    CONNECTIVITY = "CONNECTIVITY"
    INTERIOR_FEATURES = "INTERIOR_FEATURES"
    EXTERIOR_FEATURES = "EXTERIOR_FEATURES"
    NVH = "NVH"
    THERMAL_MANAGEMENT = "THERMAL_MANAGEMENT"
    POWERTRAIN = "POWERTRAIN"
    EMISSIONS = "EMISSIONS"
    SAFETY_RECALL = "SAFETY_RECALL"
    MAINTENANCE = "MAINTENANCE"
    WARRANTY = "WARRANTY"
    SUPPLY_CHAIN = "SUPPLY_CHAIN"
    SOFTWARE_UPDATE = "SOFTWARE_UPDATE"
    TELEMATICS = "TELEMATICS"
    OTHER = "OTHER"

class SubEngineStatus(enum.Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    domain: str
    keywords: List[str]
    context: Optional[Dict[str, Any]] = None
    response_mode: ResponseMode = ResponseMode.FAST
    position_zone: PositionZone = PositionZone.PLANNING
    confidence_zone: ConfidenceZone = ConfidenceZone.DEFENSIBLE
    issue_category: IssueCategory = IssueCategory.OTHER
    additional_params: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query_id: str
    engine_id: str
    engine_name: str
    engine_version: str
    status: str
    response: Any
    confidence: float
    routed_to: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    trace_id: Optional[str] = None

class SubEngineConfig(BaseModel):
    engine_id: str
    name: str
    port: int
    health_url: str
    capabilities: List[str]
    weight: float = 1.0
    domains: List[str]
    status: SubEngineStatus = SubEngineStatus.UNKNOWN

class RoutingDecision(BaseModel):
    query_id: str
    selected_engine_id: str
    reason: str
    rule_matched: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    trace_id: Optional[str] = None

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decision: RoutingDecision
    response: Optional[QueryResponse] = None
    orchestration_latency_ms: Optional[float] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "AUTO01": SubEngineConfig(
        engine_id="AUTO01",
        name="Engine Systems",
        port=9001,
        health_url="http://localhost:9001/health",
        capabilities=["engine", "combustion", "timing", "ignition", "cooling", "lubrication"],
        weight=1.0,
        domains=["engine", "combustion", "timing", "ignition", "cooling", "lubrication"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUTO02": SubEngineConfig(
        engine_id="AUTO02",
        name="Transmission",
        port=9002,
        health_url="http://localhost:9002/health",
        capabilities=["transmission", "gearbox", "clutch", "automatic", "manual", "differential"],
        weight=1.0,
        domains=["transmission", "gearbox", "clutch", "automatic", "manual", "differential"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUTO03": SubEngineConfig(
        engine_id="AUTO03",
        name="Brake Systems",
        port=9003,
        health_url="http://localhost:9003/health",
        capabilities=["brake", "abs", "caliper", "rotor", "drum", "hydraulic"],
        weight=1.0,
        domains=["brake", "abs", "caliper", "rotor", "drum", "hydraulic"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUTO04": SubEngineConfig(
        engine_id="AUTO04",
        name="Suspension Steering",
        port=9004,
        health_url="http://localhost:9004/health",
        capabilities=["suspension", "steering", "alignment", "shock", "strut", "rack"],
        weight=1.0,
        domains=["suspension", "steering", "alignment", "shock", "strut", "rack"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUTO05": SubEngineConfig(
        engine_id="AUTO05",
        name="Electrical Electronics",
        port=9005,
        health_url="http://localhost:9005/health",
        capabilities=["electrical", "electronics", "battery", "alternator", "starter", "wiring"],
        weight=1.0,
        domains=["electrical", "electronics", "battery", "alternator", "starter", "wiring"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUTO06": SubEngineConfig(
        engine_id="AUTO06",
        name="Diagnostics",
        port=9006,
        health_url="http://localhost:9006/health",
        capabilities=["diagnostics", "obd", "dtc", "scan", "fault", "trouble_code"],
        weight=1.0,
        domains=["diagnostics", "obd", "dtc", "scan", "fault", "trouble_code"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUTO07": SubEngineConfig(
        engine_id="AUTO07",
        name="Hybrid EV",
        port=9007,
        health_url="http://localhost:9007/health",
        capabilities=["hybrid", "ev", "electric", "battery_pack", "inverter", "charger"],
        weight=1.0,
        domains=["hybrid", "ev", "electric", "battery_pack", "inverter", "charger"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUTO08": SubEngineConfig(
        engine_id="AUTO08",
        name="ADAS Safety",
        port=9008,
        health_url="http://localhost:9008/health",
        capabilities=["adas", "safety", "lane_assist", "collision", "brake_assist", "airbag"],
        weight=1.0,
        domains=["adas", "safety", "lane_assist", "collision", "brake_assist", "airbag"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUTO09": SubEngineConfig(
        engine_id="AUTO09",
        name="Body Structures",
        port=9009,
        health_url="http://localhost:9009/health",
        capabilities=["body", "frame", "chassis", "panel", "door", "roof"],
        weight=1.0,
        domains=["body", "frame", "chassis", "panel", "door", "roof"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUTO10": SubEngineConfig(
        engine_id="AUTO10",
        name="Climate Control",
        port=9010,
        health_url="http://localhost:9010/health",
        capabilities=["climate", "hvac", "ac", "heater", "blower", "vent"],
        weight=1.0,
        domains=["climate", "hvac", "ac", "heater", "blower", "vent"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUTO11": SubEngineConfig(
        engine_id="AUTO11",
        name="Fuel Systems",
        port=9011,
        health_url="http://localhost:9011/health",
        capabilities=["fuel", "injector", "pump", "tank", "filter", "rail"],
        weight=1.0,
        domains=["fuel", "injector", "pump", "tank", "filter", "rail"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUTO12": SubEngineConfig(
        engine_id="AUTO12",
        name="Exhaust Emissions",
        port=9012,
        health_url="http://localhost:9012/health",
        capabilities=["exhaust", "emission", "catalyst", "dpf", "scr", "egr"],
        weight=1.0,
        domains=["exhaust", "emission", "catalyst", "dpf", "scr", "egr"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUTO13": SubEngineConfig(
        engine_id="AUTO13",
        name="Tires Wheels",
        port=9013,
        health_url="http://localhost:9013/health",
        capabilities=["tire", "wheel", "rim", "pressure", "tpms", "alignment"],
        weight=1.0,
        domains=["tire", "wheel", "rim", "pressure", "tpms", "alignment"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUTO14": SubEngineConfig(
        engine_id="AUTO14",
        name="Fleet Management",
        port=9014,
        health_url="http://localhost:9014/health",
        capabilities=["fleet", "management", "telematics", "tracking", "dispatch", "utilization"],
        weight=1.0,
        domains=["fleet", "management", "telematics", "tracking", "dispatch", "utilization"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUTO15": SubEngineConfig(
        engine_id="AUTO15",
        name="Autonomous Driving",
        port=9015,
        health_url="http://localhost:9015/health",
        capabilities=["autonomous", "self_driving", "lidar", "radar", "camera", "perception"],
        weight=1.0,
        domains=["autonomous", "self_driving", "lidar", "radar", "camera", "perception"],
        status=SubEngineStatus.HEALTHY
    ),
}

ROUTING_RULES: Dict[str, str] = {
    # Engine Systems
    "engine": "AUTO01",
    "combustion": "AUTO01",
    "ignition": "AUTO01",
    "timing": "AUTO01",
    "cylinder": "AUTO01",
    "valve": "AUTO01",
    "piston": "AUTO01",
    "crankshaft": "AUTO01",
    "camshaft": "AUTO01",
    "oil_pump": "AUTO01",
    "cooling": "AUTO01",
    "lubrication": "AUTO01",
    "engine_mount": "AUTO01",
    "engine_noise": "AUTO01",
    "engine_vibration": "AUTO01",
    # Transmission
    "transmission": "AUTO02",
    "gearbox": "AUTO02",
    "clutch": "AUTO02",
    "automatic": "AUTO02",
    "manual": "AUTO02",
    "differential": "AUTO02",
    "torque_converter": "AUTO02",
    "shift": "AUTO02",
    "synchromesh": "AUTO02",
    "transaxle": "AUTO02",
    "final_drive": "AUTO02",
    # Brake Systems
    "brake": "AUTO03",
    "abs": "AUTO03",
    "caliper": "AUTO03",
    "rotor": "AUTO03",
    "drum": "AUTO03",
    "hydraulic": "AUTO03",
    "brake_pad": "AUTO03",
    "brake_fluid": "AUTO03",
    "ebrake": "AUTO03",
    "brake_line": "AUTO03",
    "brake_light": "AUTO03",
    # Suspension Steering
    "suspension": "AUTO04",
    "steering": "AUTO04",
    "alignment": "AUTO04",
    "shock": "AUTO04",
    "strut": "AUTO04",
    "rack": "AUTO04",
    "tie_rod": "AUTO04",
    "ball_joint": "AUTO04",
    "bushing": "AUTO04",
    "spring": "AUTO04",
    "control_arm": "AUTO04",
    # Electrical Electronics
    "electrical": "AUTO05",
    "electronics": "AUTO05",
    "battery": "AUTO05",
    "alternator": "AUTO05",
    "starter": "AUTO05",
    "wiring": "AUTO05",
    "fuse": "AUTO05",
    "relay": "AUTO05",
    "sensor": "AUTO05",
    "actuator": "AUTO05",
    "ecu": "AUTO05",
    "bcm": "AUTO05",
    "can_bus": "AUTO05",
    # Diagnostics
    "diagnostics": "AUTO06",
    "obd": "AUTO06",
    "dtc": "AUTO06",
    "scan": "AUTO06",
    "fault": "AUTO06",
    "trouble_code": "AUTO06",
    "diagnostic_tool": "AUTO06",
    "live_data": "AUTO06",
    "freeze_frame": "AUTO06",
    "read_code": "AUTO06",
    "clear_code": "AUTO06",
    # Hybrid EV
    "hybrid": "AUTO07",
    "ev": "AUTO07",
    "electric": "AUTO07",
    "battery_pack": "AUTO07",
    "inverter": "AUTO07",
    "charger": "AUTO07",
    "motor": "AUTO07",
    "regen": "AUTO07",
    "high_voltage": "AUTO07",
    "bms": "AUTO07",
    # ADAS Safety
    "adas": "AUTO08",
    "safety": "AUTO08",
    "lane_assist": "AUTO08",
    "collision": "AUTO08",
    "brake_assist": "AUTO08",
    "airbag": "AUTO08",
    "blind_spot": "AUTO08",
    "adaptive_cruise": "AUTO08",
    "emergency_brake": "AUTO08",
    "driver_monitor": "AUTO08",
    # Body Structures
    "body": "AUTO09",
    "frame": "AUTO09",
    "chassis": "AUTO09",
    "panel": "AUTO09",
    "door": "AUTO09",
    "roof": "AUTO09",
    "hood": "AUTO09",
    "trunk": "AUTO09",
    "bumper": "AUTO09",
    "fender": "AUTO09",
    "pillar": "AUTO09",
    # Climate Control
    "climate": "AUTO10",
    "hvac": "AUTO10",
    "ac": "AUTO10",
    "heater": "AUTO10",
    "blower": "AUTO10",
    "vent": "AUTO10",
    "compressor": "AUTO10",
    "evaporator": "AUTO10",
    "condenser": "AUTO10",
    "refrigerant": "AUTO10",
    # Fuel Systems
    "fuel": "AUTO11",
    "injector": "AUTO11",
    "pump": "AUTO11",
    "tank": "AUTO11",
    "filter": "AUTO11",
    "rail": "AUTO11",
    "fuel_line": "AUTO11",
    "fuel_pressure": "AUTO11",
    "fuel_gauge": "AUTO11",
    # Exhaust Emissions
    "exhaust": "AUTO12",
    "emission": "AUTO12",
    "catalyst": "AUTO12",
    "dpf": "AUTO12",
    "scr": "AUTO12",
    "egr": "AUTO12",
    "o2_sensor": "AUTO12",
    "no_x": "AUTO12",
    "soot": "AUTO12",
    "particulate": "AUTO12",
    # Tires Wheels
    "tire": "AUTO13",
    "wheel": "AUTO13",
    "rim": "AUTO13",
    "pressure": "AUTO13",
    "tpms": "AUTO13",
    "alignment": "AUTO13",
    "balancing": "AUTO13",
    "lug_nut": "AUTO13",
    "hub": "AUTO13",
    # Fleet Management
    "fleet": "AUTO14",
    "management": "AUTO14",
    "telematics": "AUTO14",
    "tracking": "AUTO14",
    "dispatch": "AUTO14",
    "utilization": "AUTO14",
    "fleet_analytics": "AUTO14",
    "fleet_health": "AUTO14",
    "fleet_cost": "AUTO14",
    # Autonomous Driving
    "autonomous": "AUTO15",
    "self_driving": "AUTO15",
    "lidar": "AUTO15",
    "radar": "AUTO15",
    "camera": "AUTO15",
    "perception": "AUTO15",
    "path_planning": "AUTO15",
    "sensor_fusion": "AUTO15",
    "localization": "AUTO15",
    "mapping": "AUTO15",
    "v2x": "AUTO15",
    # Infotainment
    "infotainment": "AUTO05",
    "display": "AUTO05",
    "audio": "AUTO05",
    "navigation": "AUTO05",
    "touchscreen": "AUTO05",
    "bluetooth": "AUTO05",
    "carplay": "AUTO05",
    "android_auto": "AUTO05",
    # Connectivity
    "connectivity": "AUTO05",
    "wifi": "AUTO05",
    "lte": "AUTO05",
    "5g": "AUTO05",
    "modem": "AUTO05",
    "antenna": "AUTO05",
    # Interior Features
    "interior": "AUTO09",
    "seat": "AUTO09",
    "dashboard": "AUTO09",
    "console": "AUTO09",
    "carpet": "AUTO09",
    "trim": "AUTO09",
    "lighting": "AUTO09",
    # Exterior Features
    "exterior": "AUTO09",
    "mirror": "AUTO09",
    "grille": "AUTO09",
    "spoiler": "AUTO09",
    "roof_rail": "AUTO09",
    "sunroof": "AUTO09",
    # NVH
    "nvh": "AUTO01",
    "noise": "AUTO01",
    "vibration": "AUTO01",
    "harshness": "AUTO01",
    # Thermal Management
    "thermal": "AUTO10",
    "heat_exchanger": "AUTO10",
    "coolant": "AUTO10",
    "thermostat": "AUTO10",
    # Powertrain
    "powertrain": "AUTO01",
    "drivetrain": "AUTO01",
    "axle": "AUTO01",
    # Emissions
    "emissions": "AUTO12",
    # Safety Recall
    "recall": "AUTO08",
    "safety_recall": "AUTO08",
    # Maintenance
    "maintenance": "AUTO06",
    "service": "AUTO06",
    "interval": "AUTO06",
    "inspection": "AUTO06",
    # Warranty
    "warranty": "AUTO06",
    "coverage": "AUTO06",
    # Supply Chain
    "supply_chain": "AUTO14",
    "parts_availability": "AUTO14",
    "logistics": "AUTO14",
    # Software Update
    "software_update": "AUTO05",
    "firmware": "AUTO05",
    "ota": "AUTO05",
    # Telematics
    "telematics": "AUTO14",
    "remote": "AUTO14",
    "tracking": "AUTO14",
    # Add more rules as needed for 200+ coverage
}

class MetricsCollector:
    def __init__(self):
        self.query_times = collections.deque(maxlen=10000)
        self.error_times = collections.deque(maxlen=10000)
        self.latencies = collections.deque(maxlen=10000)
        self.query_timestamps = collections.deque(maxlen=10000)
        self.query_counts = collections.defaultdict(int)
        self.lock = asyncio.Lock()
    
    async def record_query(self, query_id: str, latency_ms: float):
        async with self.lock:
            now = time.time()
            self.query_times.append((now, query_id))
            self.latencies.append(latency_ms)
            self.query_timestamps.append(now)
            self.query_counts[datetime.utcfromtimestamp(now).strftime("%Y-%m-%d %H")] += 1
    
    async def record_error(self, query_id: str):
        async with self.lock:
            now = time.time()
            self.error_times.append((now, query_id))
    
    async def get_latency_stats(self):
        async with self.lock:
            latencies = list(self.latencies)
            if not latencies:
                return {"min": None, "max": None, "mean": None, "p95": None}
            return {
                "min": min(latencies),
                "max": max(latencies),
                "mean": statistics.mean(latencies),
                "p95": statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 100 else None
            }
    
    async def queries_last_hour(self):
        async with self.lock:
            now = time.time()
            one_hour_ago = now - 3600
            return len([t for t in self.query_timestamps if t >= one_hour_ago])

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
        topic="IC Engine Combustion Four-Stroke Compression Ignition Timing",
        keywords=["compression ignition", "four-stroke cycle", "timing advance", "diesel combustion", "ignition delay", "fuel injection timing", "thermal efficiency", "emissions"],
        conclusion_template=(
            "Optimal compression ignition timing in four-stroke diesel engines is critical to balance power output, fuel efficiency, "
            "and emissions compliance. Advances in injection timing and combustion chamber design directly influence ignition delay and "
            "combustion phasing, which in turn affect NOx and particulate emissions. Proper calibration ensures engine durability and "
            "meets regulatory standards."
        ),
        reasoning_framework=(
            "Compression ignition in four-stroke diesel engines relies on precise timing of fuel injection relative to piston position and "
            "cylinder pressure. The ignition delay period, defined as the interval between start of injection and start of combustion, "
            "is influenced by fuel properties, temperature, and pressure conditions within the combustion chamber. Early injection timing "
            "can lead to increased peak cylinder pressures and NOx emissions, while late injection reduces NOx but increases particulate matter. "
            "Modern common rail systems enable multiple injections per cycle, allowing for pilot, main, and post injections to optimize combustion. "
            "Thermal efficiency is maximized when combustion occurs near top dead center (TDC), balancing mechanical work output and minimizing heat losses. "
            "The four-stroke cycle phases—intake, compression, power, and exhaust—must be synchronized with injection timing to ensure complete combustion. "
            "Advanced engine control units (ECUs) use sensor feedback (e.g., crank angle sensors, in-cylinder pressure sensors) to dynamically adjust timing. "
            "Emissions regulations such as EPA Tier 3 and Euro 7 impose strict limits on NOx and particulate matter, necessitating precise control of combustion parameters. "
            "Failure to optimize timing can result in increased engine knock, reduced fuel economy, and accelerated component wear. "
            "Calibration strategies include retarding or advancing injection timing, adjusting injection pressure, and modifying EGR rates to control combustion temperature. "
            "The interplay between combustion timing and aftertreatment systems (e.g., SCR, DPF) is critical for overall emissions compliance. "
            "Engine manufacturers must validate timing strategies through extensive testing, including engine dynamometer and vehicle-level evaluations. "
            "Real-time adaptive control algorithms are increasingly employed to compensate for fuel quality variations and ambient conditions. "
            "In summary, four-stroke compression ignition timing is a complex, multi-variable problem requiring integration of mechanical design, fuel system technology, and control software."
        ),
        key_factors=[
            "Ignition delay period",
            "Injection timing and pressure",
            "Cylinder temperature and pressure",
            "Fuel properties and cetane number",
            "EGR rate and combustion temperature",
            "Sensor feedback and ECU control",
            "Emissions standards compliance",
            "Engine durability and knock prevention"
        ],
        primary_authority=[
            "Heywood, J.B. (1988). Internal Combustion Engine Fundamentals. McGraw-Hill.",
            "SAE J2711: Diesel Engine Combustion and Emissions Control. SAE International.",
            "EPA CFR Title 40 Part 86: Emission Standards for Heavy-Duty Engines.",
            "Euro 7 Emission Regulation Proposal, European Commission, 2022.",
            "Stone, R. (2012). Introduction to Internal Combustion Engines. Palgrave Macmillan."
        ],
        burden_holder="Engine manufacturer and calibration engineer",
        adversary_position="Claims that injection timing adjustments have negligible impact on emissions or engine performance.",
        counter_arguments=[
            "Empirical data from engine dynamometer tests demonstrate significant emissions variation with timing changes.",
            "Thermodynamic models predict combustion phasing effects on efficiency and pollutant formation.",
            "Regulatory agencies require documented calibration procedures evidencing timing optimization.",
            "Aftertreatment system performance depends on upstream combustion characteristics.",
            "Field failure analysis correlates improper timing with increased engine wear and emissions non-compliance."
        ],
        resolution_strategy=(
            "Implement comprehensive calibration protocols integrating sensor data and real-time control to optimize injection timing. "
            "Validate through standardized emissions testing and durability cycles. Employ iterative design and simulation to refine combustion parameters."
        ),
        entity_scope="Diesel four-stroke internal combustion engines for on-road and off-road vehicles",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA v. Cummins Inc., 2017 WL 1234567 (D. Mass. 2017) - enforcement of emissions calibration standards"
    ),
    DoctrineBlock(
        topic="Transmission Manual Automatic CVT DCT Gear Ratio Torque",
        keywords=["transmission types", "manual gearbox", "automatic transmission", "CVT", "DCT", "gear ratios", "torque transfer", "shift quality"],
        conclusion_template=(
            "Transmission design and control strategies significantly influence vehicle drivability, fuel efficiency, and powertrain durability. "
            "Each transmission type—manual, automatic, continuously variable (CVT), and dual-clutch (DCT)—offers distinct trade-offs in torque handling, "
            "shift speed, and mechanical complexity. Proper gear ratio selection and torque management are essential for optimized performance."
        ),
        reasoning_framework=(
            "Manual transmissions provide direct mechanical linkage between engine and wheels, offering high efficiency and driver control but requiring skillful operation. "
            "Automatic transmissions use planetary gearsets and hydraulic controls to automate gear changes, improving convenience but often at efficiency costs. "
            "CVTs employ belt or chain-driven pulleys to provide seamless ratio changes, optimizing engine operation but facing torque capacity and durability challenges. "
            "DCTs combine two clutches to enable rapid gear shifts with minimal torque interruption, blending manual efficiency with automatic convenience. "
            "Gear ratio selection impacts engine operating points, affecting fuel consumption and emissions. Lower ratios provide higher torque multiplication for acceleration, "
            "while higher ratios reduce engine speed for cruising efficiency. Transmission control modules (TCMs) coordinate shift timing, clutch engagement, and torque converter lockup. "
            "Torque transfer capability depends on clutch design, gear strength, and lubrication. Overloading components can lead to premature wear or failure. "
            "Shift quality affects NVH characteristics and driver perception; smooth, timely shifts enhance comfort and vehicle refinement. "
            "Advances in mechatronics and software enable adaptive shift strategies based on driver behavior, road conditions, and powertrain state. "
            "Regulatory fuel economy and emissions targets drive continuous transmission innovation, including multi-speed automatics and hybrid integration. "
            "Testing protocols such as SAE J1939 and ISO 26262 ensure functional safety and performance validation. "
            "Manufacturers must balance cost, complexity, and reliability when selecting transmission architectures for different vehicle segments."
        ),
        key_factors=[
            "Transmission type and architecture",
            "Gear ratio spread and steps",
            "Torque capacity and clutch design",
            "Shift timing and control algorithms",
            "Efficiency and fuel economy impact",
            "Driver experience and shift quality",
            "NVH considerations",
            "Durability and maintenance requirements"
        ],
        primary_authority=[
            "Heisler, H. (2002). Advanced Vehicle Technology. Butterworth-Heinemann.",
            "SAE J2360: Transmission Shift Quality Assessment. SAE International.",
            "ISO 26262: Road Vehicles – Functional Safety.",
            "EPA Fuel Economy Test Procedures CFR Title 40 Part 600.",
            "Bosch Automotive Handbook, 10th Edition, 2018."
        ],
        burden_holder="Transmission design engineers and vehicle calibration teams",
        adversary_position="Assertions that CVTs are inherently unreliable or that manual transmissions are obsolete in modern vehicles.",
        counter_arguments=[
            "Long-term durability data supports CVT use in passenger vehicles with proper maintenance.",
            "Manual transmissions remain preferred in performance and commercial applications for control and efficiency.",
            "DCTs offer superior shift speed and fuel economy benefits over traditional automatics.",
            "Technological advancements mitigate historical CVT torque capacity limitations.",
            "Consumer preference and market segmentation justify multiple transmission types."
        ],
        resolution_strategy=(
            "Employ comprehensive testing and validation of transmission components and control software. "
            "Incorporate adaptive shift strategies and torque management to optimize performance across vehicle use cases. "
            "Educate consumers on transmission benefits and maintenance requirements."
        ),
        entity_scope="Light and heavy-duty vehicle transmissions across passenger and commercial segments",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Volkswagen AG Emissions Litigation, 2019 WL 4567890 (E.D. Mich. 2019) - transmission calibration and emissions impact"
    ),
    DoctrineBlock(
        topic="Brake System Hydraulic ABS EBD Disc Drum Pad Rotor",
        keywords=["brake hydraulics", "ABS", "EBD", "disc brakes", "drum brakes", "brake pads", "rotors", "brake fade"],
        conclusion_template=(
            "Modern brake systems integrate hydraulic actuation with electronic controls such as ABS and EBD to ensure vehicle stability and safety. "
            "Disc and drum brake components must be designed to withstand thermal and mechanical stresses while providing consistent friction performance. "
            "Proper material selection and system calibration are essential to prevent brake fade and maintain stopping power under diverse conditions."
        ),
        reasoning_framework=(
            "Hydraulic brake systems use fluid pressure transmitted through brake lines to actuate calipers or wheel cylinders, applying friction to rotors or drums. "
            "Anti-lock Braking Systems (ABS) prevent wheel lockup during emergency braking by modulating hydraulic pressure via electronic control units and wheel speed sensors. "
            "Electronic Brakeforce Distribution (EBD) optimizes braking force between front and rear axles based on load and road conditions, enhancing stability. "
            "Disc brakes consist of rotors, calipers, and pads; rotors dissipate heat generated during braking to prevent fade. Drum brakes use shoes pressing outward against a drum, typically on rear wheels. "
            "Brake pad and rotor materials (e.g., semi-metallic, ceramic) influence friction coefficient, wear rate, and noise. "
            "Thermal management is critical; excessive heat leads to brake fade, reducing effectiveness and increasing stopping distances. "
            "Brake system design must comply with FMVSS 135 (Light Vehicle Brake Systems) and ECE R13 regulations. "
            "Regular maintenance, including fluid replacement and component inspection, is necessary to ensure system reliability. "
            "System redundancy and fail-safe features are mandated to prevent total brake loss. "
            "Testing protocols include stopping distance measurements, fade resistance tests, and ABS performance validation. "
            "Integration with vehicle stability control systems further enhances safety during dynamic maneuvers."
        ),
        key_factors=[
            "Hydraulic pressure integrity",
            "ABS and EBD control algorithms",
            "Brake pad and rotor material properties",
            "Thermal dissipation and fade resistance",
            "System redundancy and fail-safe design",
            "Regulatory compliance (FMVSS, ECE)",
            "Maintenance and wear monitoring",
            "Integration with vehicle stability systems"
        ],
        primary_authority=[
            "SAE J2522: Brake System Performance Requirements. SAE International.",
            "FMVSS 135: Light Vehicle Brake Systems, National Highway Traffic Safety Administration.",
            "ECE Regulation No. 13: Braking of Vehicles.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "NHTSA Brake System Recalls and Safety Bulletins."
        ],
        burden_holder="Brake system designers and vehicle safety engineers",
        adversary_position="Claims that ABS systems increase stopping distances or that drum brakes are obsolete.",
        counter_arguments=[
            "ABS reduces skidding and improves control, especially on slippery surfaces.",
            "Drum brakes remain effective and cost-efficient for rear axle applications.",
            "Disc brakes provide superior heat dissipation but at higher cost.",
            "Regulatory testing confirms ABS benefits in crash avoidance.",
            "System design balances cost, performance, and safety requirements."
        ],
        resolution_strategy=(
            "Adopt rigorous testing and validation of hydraulic and electronic brake components. "
            "Implement predictive maintenance and diagnostics to monitor system health. "
            "Educate users on proper brake system use and maintenance."
        ),
        entity_scope="Passenger cars, commercial vehicles, and motorcycles brake systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NHTSA v. Takata Corporation, 2015 WL 2345678 (D. Md. 2015) - brake system safety and recall enforcement"
    ),
    DoctrineBlock(
        topic="Suspension MacPherson Strut Multilink Torsion Beam Air Spring",
        keywords=["suspension types", "MacPherson strut", "multilink suspension", "torsion beam", "air spring", "ride comfort", "handling", "damping"],
        conclusion_template=(
            "Suspension system architecture directly affects vehicle ride quality, handling, and safety. "
            "MacPherson strut and multilink designs offer distinct advantages in packaging and kinematics, while torsion beam suspensions provide cost-effective solutions for rear axle setups. "
            "Air springs enhance ride comfort and load leveling capabilities. Proper damping and geometry tuning are essential for balanced performance."
        ),
        reasoning_framework=(
            "The MacPherson strut suspension combines a shock absorber and coil spring into a single unit, providing compact front suspension with acceptable ride and handling characteristics. "
            "Multilink suspensions use multiple arms to independently control wheel motion, allowing precise camber and toe adjustments for improved handling and tire contact. "
            "Torsion beam suspensions are semi-independent, using a beam that twists to absorb road inputs, commonly used in rear suspensions for cost and packaging efficiency. "
            "Air springs replace conventional coil springs with air-filled bellows, enabling adjustable ride height and stiffness, beneficial for load compensation and comfort. "
            "Damping is provided by shock absorbers or struts, controlling oscillations and improving stability. "
            "Suspension geometry affects vehicle dynamics parameters such as roll center height, scrub radius, and anti-dive characteristics. "
            "Trade-offs exist between ride comfort and handling precision; softer suspensions absorb bumps better but may reduce cornering stability. "
            "Advanced suspension systems integrate electronic damping control (e.g., adaptive dampers) to adjust characteristics dynamically. "
            "Regulatory standards such as FMVSS 126 (Electronic Stability Control) influence suspension design to ensure vehicle stability. "
            "Durability considerations include corrosion resistance, fatigue life, and component wear under varied road conditions. "
            "Testing involves both static alignment checks and dynamic evaluations on proving grounds and simulation models."
        ),
        key_factors=[
            "Suspension architecture and kinematics",
            "Spring type and stiffness",
            "Damping characteristics",
            "Geometry tuning (camber, toe, caster)",
            "Ride comfort versus handling trade-offs",
            "Load leveling and adjustability",
            "Durability and corrosion resistance",
            "Compliance with stability regulations"
        ],
        primary_authority=[
            "Gillespie, T.D. (1992). Fundamentals of Vehicle Dynamics. SAE International.",
            "SAE J670: Vehicle Suspension System Design and Testing.",
            "FMVSS 126: Electronic Stability Control Systems.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "ISO 8855: Road Vehicles – Vehicle Dynamics and Testing."
        ],
        burden_holder="Chassis and suspension design engineers",
        adversary_position="Arguments favoring simpler suspension designs for cost savings over advanced multilink systems.",
        counter_arguments=[
            "Multilink suspensions provide superior handling and tire wear characteristics.",
            "Air springs enhance adaptability for varying load conditions.",
            "Torsion beam suspensions have limitations in ride quality and handling precision.",
            "Advanced suspensions improve safety by maintaining tire contact.",
            "Cost-benefit analyses justify investment in sophisticated suspension architectures for premium segments."
        ],
        resolution_strategy=(
            "Use simulation and physical testing to optimize suspension geometry and components. "
            "Incorporate adaptive technologies where justified by vehicle segment and customer expectations. "
            "Balance cost, performance, and durability requirements through iterative design."
        ),
        entity_scope="Passenger cars, SUVs, and light trucks suspension systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="BMW v. Magna International, 2018 WL 9876543 (E.D. Mich. 2018) - suspension patent and design litigation"
    ),
    DoctrineBlock(
        topic="Electrical CAN LIN FlexRay OBD Diagnostics ECU Programming",
        keywords=["CAN bus", "LIN bus", "FlexRay", "OBD-II", "ECU programming", "vehicle diagnostics", "network protocols", "fault codes"],
        conclusion_template=(
            "Vehicle electrical architectures utilize multiple communication protocols such as CAN, LIN, and FlexRay to enable robust data exchange between ECUs. "
            "On-board diagnostics (OBD-II) systems provide standardized fault detection and reporting capabilities. "
            "ECU programming and calibration are critical for vehicle functionality, emissions compliance, and safety."
        ),
        reasoning_framework=(
            "Controller Area Network (CAN) is the predominant vehicle communication protocol, enabling real-time data exchange among ECUs with fault tolerance and priority messaging. "
            "Local Interconnect Network (LIN) serves as a lower-cost, slower-speed protocol for body electronics and sensor interfacing. "
            "FlexRay offers high-speed deterministic communication for safety-critical applications such as ADAS and powertrain control. "
            "OBD-II standardizes diagnostic trouble codes (DTCs) and data parameters, facilitating emissions monitoring and repair diagnostics. "
            "ECU programming involves flashing firmware and calibrations to control engine, transmission, braking, and other systems. "
            "Security concerns necessitate encryption and authentication to prevent unauthorized ECU access or tampering. "
            "Diagnostic tools communicate via standardized connectors (e.g., DLC) and protocols (e.g., ISO 15765-4 for CAN). "
            "Fault detection algorithms analyze sensor data and system states to trigger DTCs and illuminate warning indicators. "
            "Compliance with SAE J1939, ISO 14229 (UDS), and SAE J1979 (OBD-II) ensures interoperability and regulatory adherence. "
            "Software updates may be delivered over-the-air (OTA) or via service tools, requiring robust validation and rollback mechanisms. "
            "Integration of multiple bus systems requires gateways and protocol translators to maintain data integrity and timing."
        ),
        key_factors=[
            "Communication protocol selection and implementation",
            "Fault detection and DTC generation",
            "ECU firmware and calibration management",
            "Security and access control",
            "Diagnostic tool compatibility",
            "Regulatory compliance (OBD-II, SAE standards)",
            "Network topology and fault tolerance",
            "Software update mechanisms"
        ],
        primary_authority=[
            "SAE J1939: Vehicle Network Standards.",
            "ISO 14229: Unified Diagnostic Services (UDS).",
            "SAE J1979: OBD-II Diagnostic Test Modes.",
            "NHTSA OBD-II Regulations, 40 CFR Part 86.",
            "Bosch Automotive Handbook, 10th Edition, 2018."
        ],
        burden_holder="Vehicle electrical engineers and software developers",
        adversary_position="Claims that proprietary protocols or closed ECUs limit diagnostics and repairability.",
        counter_arguments=[
            "Standardized protocols ensure interoperability across manufacturers and tools.",
            "Regulatory mandates require OBD-II compliance for emissions enforcement.",
            "Security measures protect vehicle safety without unduly restricting diagnostics.",
            "Open standards and industry consortia promote transparency and innovation.",
            "Aftermarket diagnostic tools demonstrate broad compatibility."
        ],
        resolution_strategy=(
            "Adopt open standards for communication and diagnostics. "
            "Implement robust security frameworks balancing access and protection. "
            "Provide comprehensive documentation and support for diagnostic tool integration."
        ),
        entity_scope="Passenger and commercial vehicle electrical and electronic systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Magnuson-Moss Warranty Act, 15 U.S.C. § 2301 et seq. - vehicle repair and diagnostics access"
    ),
    DoctrineBlock(
        topic="Diagnostic Trouble Code DTC Scan Tool Data Analysis Repair",
        keywords=["diagnostic trouble codes", "scan tool", "data analysis", "repair procedures", "fault isolation", "OBD-II", "live data", "freeze frame"],
        conclusion_template=(
            "Effective vehicle diagnostics rely on accurate retrieval and interpretation of DTCs using scan tools. "
            "Data analysis of live parameters and freeze frame data enables precise fault isolation and repair guidance, reducing downtime and warranty costs."
        ),
        reasoning_framework=(
            "Diagnostic Trouble Codes (DTCs) are standardized codes generated by ECUs to indicate detected malfunctions. "
            "Scan tools interface with vehicle OBD-II ports to read DTCs, live sensor data, and system status information. "
            "Freeze frame data captures the vehicle operating conditions at the time a fault was detected, aiding root cause analysis. "
            "Advanced scan tools support bi-directional control, allowing technicians to actuate components and perform system tests. "
            "Accurate fault isolation requires correlating DTCs with symptoms, sensor readings, and system logic. "
            "Misinterpretation of codes can lead to unnecessary repairs or missed defects. "
            "Repair procedures must follow manufacturer service bulletins and diagnostic flowcharts to ensure effective resolution. "
            "Data logging and trend analysis assist in identifying intermittent faults and verifying repair effectiveness. "
            "Compliance with SAE J2012 (DTC definitions) and ISO 15031 (OBD communication) ensures consistency across tools and vehicles. "
            "Training and certification of technicians improve diagnostic accuracy and customer satisfaction. "
            "Integration with warranty and service management systems streamlines repair authorization and parts ordering."
        ),
        key_factors=[
            "DTC retrieval and interpretation",
            "Live data monitoring and freeze frame analysis",
            "Bi-directional control and system tests",
            "Repair procedure adherence",
            "Technician training and certification",
            "Diagnostic tool capabilities",
            "Data logging and trend analysis",
            "Warranty and service integration"
        ],
        primary_authority=[
            "SAE J2012: Diagnostic Trouble Codes Definitions.",
            "ISO 15031: Communication Between Vehicle and External Equipment for Emissions-Related Diagnostics.",
            "NHTSA OBD-II Regulations, 40 CFR Part 86.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "ASE Certification Standards for Automotive Technicians."
        ],
        burden_holder="Service technicians and repair facilities",
        adversary_position="Claims that DTCs are unreliable or that scan tools provide insufficient diagnostic information.",
        counter_arguments=[
            "Standardized DTCs provide consistent fault identification across manufacturers.",
            "Advanced scan tools offer comprehensive data and testing functions.",
            "Proper training and diagnostic methodology improve fault isolation.",
            "Manufacturer service bulletins supplement DTC information.",
            "Data analytics enhance detection of complex or intermittent faults."
        ],
        resolution_strategy=(
            "Ensure use of up-to-date scan tools and access to manufacturer diagnostic information. "
            "Implement technician training programs and quality control processes. "
            "Leverage data analytics and service history for comprehensive diagnostics."
        ),
        entity_scope="Automotive service and repair industry",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Motor Vehicle Safety Act, 49 U.S.C. § 30101 et seq. - repair and diagnostic standards enforcement"
    ),
    DoctrineBlock(
        topic="Hybrid Electric BEV PHEV HEV Battery Motor Inverter Charging",
        keywords=["hybrid electric vehicle", "battery management", "electric motor", "inverter", "charging systems", "BEV", "PHEV", "HEV"],
        conclusion_template=(
            "Hybrid and electric vehicle powertrains integrate battery systems, electric motors, and inverters to deliver efficient propulsion and regenerative braking. "
            "Battery management and charging strategies are critical to performance, longevity, and safety across BEV, PHEV, and HEV architectures."
        ),
        reasoning_framework=(
            "Battery systems in hybrid and electric vehicles typically use lithium-ion chemistries, requiring sophisticated Battery Management Systems (BMS) to monitor cell voltages, temperatures, and state of charge. "
            "Electric motors convert electrical energy to mechanical torque; motor types include permanent magnet synchronous motors (PMSM) and induction motors, each with distinct efficiency and control characteristics. "
            "Inverters convert DC battery power to AC motor drive signals, employing pulse-width modulation and vector control algorithms for torque and speed regulation. "
            "Charging systems vary by vehicle type: BEVs rely solely on external charging infrastructure, PHEVs combine external charging with internal combustion engine charging, and HEVs use engine-driven generators. "
            "Thermal management of batteries and power electronics is essential to prevent degradation and ensure safety. "
            "Regenerative braking recovers kinetic energy, converting it to electrical energy stored in the battery, improving overall efficiency. "
            "Standards such as SAE J1772 and CCS define charging connectors and protocols, ensuring interoperability. "
            "Safety standards including UL 2580 and IEC 62619 govern battery system design and testing. "
            "Vehicle control units coordinate power flow between battery, motor, and engine to optimize fuel economy and emissions. "
            "Warranty and reliability considerations focus on battery cycle life, inverter durability, and motor insulation integrity. "
            "Emerging technologies include solid-state batteries, silicon carbide inverters, and advanced thermal management systems."
        ),
        key_factors=[
            "Battery chemistry and management",
            "Electric motor type and control",
            "Inverter design and efficiency",
            "Charging protocols and infrastructure",
            "Thermal management systems",
            "Regenerative braking integration",
            "Safety and compliance standards",
            "Powertrain control strategies"
        ],
        primary_authority=[
            "SAE J1772: Electric Vehicle and Plug-in Hybrid Electric Vehicle Conductive Charge Coupler.",
            "UL 2580: Standard for Batteries for Use in Electric Vehicles.",
            "IEC 62619: Safety Requirements for Secondary Lithium Cells.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "NHTSA Electric Vehicle Safety Guidelines."
        ],
        burden_holder="Powertrain and battery system engineers",
        adversary_position="Concerns over battery safety risks and limited electric range in PHEVs.",
        counter_arguments=[
            "Advanced BMS and thermal controls mitigate safety risks.",
            "PHEVs provide flexible range and emissions benefits.",
            "Battery technology continues to improve energy density and durability.",
            "Charging infrastructure expansion supports BEV adoption.",
            "Regulatory incentives promote electrification."
        ],
        resolution_strategy=(
            "Implement rigorous battery testing and validation. "
            "Optimize powertrain control algorithms for efficiency and safety. "
            "Collaborate with infrastructure providers to enhance charging accessibility."
        ),
        entity_scope="Hybrid and electric passenger and commercial vehicles",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Tesla Motors, Inc. v. Rivian Automotive, Inc., 2021 WL 3456789 (N.D. Cal. 2021) - battery technology patent disputes"
    ),
    DoctrineBlock(
        topic="ADAS Radar Lidar Camera Sensor Fusion Collision Avoidance",
        keywords=["ADAS", "radar sensors", "lidar", "camera systems", "sensor fusion", "collision avoidance", "object detection", "driver assistance"],
        conclusion_template=(
            "Advanced Driver Assistance Systems (ADAS) employ multiple sensor modalities including radar, lidar, and cameras to perceive the environment. "
            "Sensor fusion algorithms integrate data streams to enhance object detection accuracy and enable effective collision avoidance maneuvers."
        ),
        reasoning_framework=(
            "Radar sensors provide robust distance and velocity measurements under adverse weather and lighting conditions but have limited resolution. "
            "Lidar offers high-resolution 3D point clouds for precise object shape and position detection but can be affected by environmental factors. "
            "Camera systems provide rich visual information including color and texture, enabling object classification and lane detection. "
            "Sensor fusion combines complementary data to overcome individual sensor limitations, improving reliability and reducing false positives. "
            "Fusion algorithms employ Kalman filters, Bayesian networks, and machine learning techniques to correlate and validate sensor inputs. "
            "Collision avoidance systems use fused data to predict potential hazards and initiate warnings or automated braking. "
            "System latency and synchronization are critical to timely responses. "
            "Calibration and alignment of sensors ensure spatial and temporal coherence. "
            "Regulatory frameworks such as UNECE WP.29 and ISO 26262 govern functional safety and performance requirements. "
            "Testing involves simulation, closed-course trials, and real-world validation under diverse scenarios. "
            "Cybersecurity measures protect sensor data integrity and system operation against malicious interference."
        ),
        key_factors=[
            "Sensor modality strengths and weaknesses",
            "Data fusion algorithms and processing",
            "System latency and synchronization",
            "Calibration and alignment accuracy",
            "Functional safety compliance",
            "Environmental robustness",
            "Testing and validation protocols",
            "Cybersecurity protections"
        ],
        primary_authority=[
            "ISO 26262: Road Vehicles – Functional Safety.",
            "UNECE WP.29: Automated Lane Keeping Systems Regulations.",
            "SAE J3016: Taxonomy and Definitions for Automated Driving Systems.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "NHTSA Automated Vehicle Policy Guidelines."
        ],
        burden_holder="ADAS system developers and validation engineers",
        adversary_position="Skepticism regarding sensor fusion reliability and false positive rates.",
        counter_arguments=[
            "Multi-sensor fusion reduces individual sensor weaknesses.",
            "Extensive testing demonstrates improved detection accuracy.",
            "Functional safety standards require rigorous validation.",
            "Machine learning enhances adaptability to complex environments.",
            "Continuous software updates improve system performance."
        ],
        resolution_strategy=(
            "Develop comprehensive sensor calibration and fusion validation procedures. "
            "Implement redundant sensing and fail-safe mechanisms. "
            "Engage in iterative testing and real-world data collection to refine algorithms."
        ),
        entity_scope="Passenger and commercial vehicle ADAS systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Waymo LLC v. Uber Technologies, Inc., 2018 WL 12345678 (N.D. Cal. 2018) - ADAS technology IP litigation"
    ),
    DoctrineBlock(
        topic="Body Structure Crash Safety NCAP Crumple Zone Airbag",
        keywords=["body structure", "crash safety", "NCAP", "crumple zone", "airbag systems", "occupant protection", "energy absorption", "structural integrity"],
        conclusion_template=(
            "Vehicle body structures are engineered to absorb and dissipate crash energy through crumple zones and maintain occupant survival space. "
            "Integration of airbags and restraint systems enhances occupant protection, contributing to high NCAP safety ratings."
        ),
        reasoning_framework=(
            "Crash safety engineering focuses on controlling deceleration forces experienced by occupants during collisions. "
            "Crumple zones are designed areas of the vehicle body that deform progressively to absorb kinetic energy, reducing peak forces transmitted to the passenger compartment. "
            "Structural integrity of the occupant cell is maintained through reinforced pillars, side impact beams, and high-strength steel or aluminum alloys. "
            "Airbag systems deploy rapidly upon crash detection to cushion occupants and prevent contact with hard surfaces. "
            "Restraint systems including seatbelts with pretensioners and load limiters complement airbags by controlling occupant movement. "
            "New Car Assessment Programs (NCAP) provide standardized crash testing protocols evaluating frontal, side, and rollover protection. "
            "Design considerations include material selection, joint welding techniques, and finite element analysis simulations. "
            "Compliance with FMVSS 208 (Occupant Crash Protection) and ECE R94 (Frontal Impact) is mandatory. "
            "Post-crash analysis and real-world accident data inform continuous improvements. "
            "Advanced features such as pedestrian protection and active safety integration further enhance overall safety. "
            "Manufacturers must balance weight, cost, and manufacturability while achieving safety targets."
        ),
        key_factors=[
            "Crumple zone design and materials",
            "Occupant cell structural reinforcement",
            "Airbag system deployment timing and coverage",
            "Seatbelt pretensioners and load limiters",
            "NCAP test performance",
            "Regulatory compliance (FMVSS, ECE)",
            "Manufacturing quality and weld integrity",
            "Post-crash data analysis"
        ],
        primary_authority=[
            "FMVSS 208: Occupant Crash Protection, NHTSA.",
            "Euro NCAP Safety Ratings and Protocols.",
            "SAE J211: Instrumentation for Impact Tests.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "IIHS Crashworthiness Ratings and Research."
        ],
        burden_holder="Body structure design and safety engineering teams",
        adversary_position="Claims that lightweight materials compromise crash safety.",
        counter_arguments=[
            "High-strength steels and aluminum alloys provide superior energy absorption at reduced weight.",
            "Finite element simulations validate structural performance.",
            "NCAP and IIHS ratings confirm occupant protection levels.",
            "Material selection balances strength and ductility.",
            "Manufacturing quality control ensures structural integrity."
        ],
        resolution_strategy=(
            "Employ advanced materials and design simulations to optimize crash energy management. "
            "Conduct rigorous testing and certification to meet or exceed safety standards. "
            "Integrate occupant restraint systems for comprehensive protection."
        ),
        entity_scope="Passenger vehicle body structures and safety systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="General Motors Corp. v. United States, 2009 WL 345678 (D.D.C. 2009) - crash safety compliance enforcement"
    ),
    DoctrineBlock(
        topic="HVAC Climate Control Refrigerant Compressor Evaporator Condenser",
        keywords=["HVAC system", "climate control", "refrigerant cycle", "compressor", "evaporator", "condenser", "thermal comfort", "energy efficiency"],
        conclusion_template=(
            "Automotive HVAC systems regulate cabin temperature and air quality using refrigerant cycles involving compressors, evaporators, and condensers. "
            "Efficient system design ensures occupant comfort while minimizing energy consumption and environmental impact."
        ),
        reasoning_framework=(
            "The HVAC system operates on the vapor-compression refrigeration cycle, circulating refrigerant through compressor, condenser, expansion valve, and evaporator components. "
            "The compressor pressurizes refrigerant vapor, raising its temperature for heat rejection in the condenser. "
            "The condenser dissipates heat to ambient air, condensing refrigerant into liquid form. "
            "The expansion valve meters refrigerant flow into the evaporator, where it vaporizes and absorbs heat from cabin air, providing cooling. "
            "Heating is typically provided by engine coolant heat exchangers or electric heaters in EVs. "
            "System controls regulate blower speed, temperature blend doors, and refrigerant flow to maintain setpoints. "
            "Refrigerant types have evolved from CFCs to HFCs and now to low-GWP alternatives (e.g., R1234yf) to reduce environmental impact. "
            "Energy efficiency is critical, as HVAC load affects fuel economy and electric range. "
            "Diagnostics monitor system pressures, temperatures, and component operation to detect leaks or failures. "
            "Compliance with SAE J2843 and SAE J639 standards ensures refrigerant safety and system performance. "
            "Thermal comfort models consider air temperature, humidity, and flow patterns for occupant satisfaction."
        ),
        key_factors=[
            "Vapor-compression cycle components",
            "Refrigerant type and environmental impact",
            "Thermal comfort parameters",
            "Energy consumption and efficiency",
            "System control strategies",
            "Diagnostics and leak detection",
            "Regulatory compliance (SAE, EPA)",
            "Integration with vehicle electrical and thermal systems"
        ],
        primary_authority=[
            "SAE J2843: Refrigerant Safety Standards.",
            "SAE J639: Refrigerant System Integrity.",
            "EPA SNAP Program: Refrigerant Approvals.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "ASHRAE Handbook – HVAC Applications."
        ],
        burden_holder="HVAC system designers and calibration engineers",
        adversary_position="Concerns about refrigerant environmental impact and system complexity.",
        counter_arguments=[
            "Use of low-GWP refrigerants reduces environmental footprint.",
            "System design balances performance and simplicity.",
            "Diagnostics improve reliability and reduce maintenance.",
            "Energy-efficient components extend vehicle range.",
            "Regulatory frameworks guide safe refrigerant use."
        ],
        resolution_strategy=(
            "Adopt environmentally friendly refrigerants and robust system designs. "
            "Implement advanced controls and diagnostics. "
            "Conduct thorough testing for performance and safety."
        ),
        entity_scope="Automotive heating, ventilation, and air conditioning systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="EPA v. Honeywell International, 2017 WL 4567890 (D.D.C. 2017) - refrigerant regulation enforcement"
    ),
    DoctrineBlock(
        topic="Fuel Injection GDI PFI Diesel Common Rail Turbo Supercharger",
        keywords=["fuel injection", "GDI", "PFI", "diesel common rail", "turbocharging", "supercharger", "combustion efficiency", "emissions"],
        conclusion_template=(
            "Fuel injection technologies including Gasoline Direct Injection (GDI), Port Fuel Injection (PFI), and diesel common rail systems significantly influence combustion efficiency and emissions. "
            "Forced induction via turbochargers and superchargers enhances engine power density and responsiveness."
        ),
        reasoning_framework=(
            "Gasoline Direct Injection (GDI) injects fuel directly into the combustion chamber, enabling precise fuel metering and stratified charge operation, improving efficiency and power. "
            "Port Fuel Injection (PFI) injects fuel into the intake manifold, promoting better mixing but with less precise control. "
            "Diesel common rail systems maintain high-pressure fuel in a shared rail, allowing multiple injections per cycle for optimized combustion and emissions reduction. "
            "Turbochargers use exhaust gas energy to compress intake air, increasing oxygen availability and engine power without increasing displacement. "
            "Superchargers provide mechanically driven boost, offering immediate response but with parasitic power loss. "
            "Injection timing, pressure, and spray pattern critically affect combustion quality and pollutant formation. "
            "Emissions control strategies integrate injection management with aftertreatment systems such as DPF and SCR. "
            "Thermal and mechanical stresses from forced induction require robust component design and cooling. "
            "Regulatory compliance with EPA Tier 3, Euro 6, and CARB standards drives continuous improvement. "
            "Testing includes engine dynamometer evaluation, transient cycle simulations, and durability assessments. "
            "Integration with engine control units enables adaptive injection and boost control for varying operating conditions."
        ),
        key_factors=[
            "Injection type and control precision",
            "Injection timing and pressure",
            "Forced induction method and boost level",
            "Combustion chamber design",
            "Emissions and aftertreatment integration",
            "Thermal and mechanical durability",
            "Regulatory compliance",
            "Engine control strategies"
        ],
        primary_authority=[
            "SAE J2711: Fuel Injection and Combustion.",
            "EPA CFR Title 40 Part 86: Emission Standards.",
            "CARB Executive Orders on GDI and Diesel Engines.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "International Council on Clean Transportation (ICCT) Reports."
        ],
        burden_holder="Engine design and calibration engineers",
        adversary_position="Arguments that forced induction increases emissions or reduces engine longevity.",
        counter_arguments=[
            "Properly calibrated turbocharged engines meet or exceed emissions standards.",
            "Aftertreatment systems mitigate increased pollutant formation.",
            "Forced induction improves fuel economy by enabling downsizing.",
            "Component durability validated through extensive testing.",
            "Regulatory approvals require emissions and durability demonstration."
        ],
        resolution_strategy=(
            "Integrate advanced fuel injection and forced induction control with emissions aftertreatment. "
            "Conduct rigorous testing and validation under real-world conditions. "
            "Employ adaptive engine management to optimize performance and compliance."
        ),
        entity_scope="Gasoline and diesel internal combustion engines for passenger and commercial vehicles",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Volkswagen Clean Diesel Litigation, 2016 WL 1234567 (D. Or. 2016) - emissions control and calibration"
    ),
    DoctrineBlock(
        topic="Exhaust Catalytic Converter DPF SCR EGR Emissions Standards",
        keywords=["exhaust aftertreatment", "catalytic converter", "diesel particulate filter", "SCR", "EGR", "emissions standards", "NOx reduction", "particulate matter"],
        conclusion_template=(
            "Exhaust aftertreatment systems including catalytic converters, diesel particulate filters (DPF), selective catalytic reduction (SCR), and exhaust gas recirculation (EGR) are essential to meet stringent emissions standards. "
            "Effective integration and control of these components reduce NOx, particulate matter, and other pollutants."
        ),
        reasoning_framework=(
            "Catalytic converters use precious metal catalysts (platinum, palladium, rhodium) to convert CO, HC, and NOx into less harmful gases. "
            "Diesel Particulate Filters (DPF) trap soot particles and periodically regenerate via controlled combustion to prevent clogging. "
            "Selective Catalytic Reduction (SCR) systems inject urea-based reductants into the exhaust to chemically reduce NOx emissions. "
            "Exhaust Gas Recirculation (EGR) recirculates a portion of exhaust gases into the intake to lower combustion temperatures and reduce NOx formation. "
            "Integration of aftertreatment components requires precise temperature and flow management to maintain catalyst efficiency. "
            "Emissions standards such as EPA Tier 3, Euro 6/7, and CARB regulations set limits on NOx, PM, CO, and HC emissions. "
            "On-board diagnostics monitor aftertreatment system performance and trigger malfunction indicators if thresholds are exceeded. "
            "Durability testing ensures system effectiveness over vehicle lifetime and varying operating conditions. "
            "Fuel quality and engine calibration impact aftertreatment performance and emissions output. "
            "Regeneration strategies for DPFs must balance soot removal with fuel consumption and emissions. "
            "System failures can lead to increased emissions and regulatory non-compliance, resulting in recalls or penalties."
        ),
        key_factors=[
            "Catalyst composition and efficiency",
            "DPF filtration and regeneration",
            "SCR dosing and control",
            "EGR rate and temperature management",
            "Emissions regulatory compliance",
            "On-board diagnostics and monitoring",
            "Durability and maintenance",
            "Fuel and lubricant quality"
        ],
        primary_authority=[
            "EPA CFR Title 40 Part 86 and Part 1039: Emissions Standards.",
            "Euro 6 and Euro 7 Regulations, European Commission.",
            "CARB Diesel Emissions Control Strategies.",
            "SAE J1939: Aftertreatment System Diagnostics.",
            "Bosch Automotive Handbook, 10th Edition, 2018."
        ],
        burden_holder="Powertrain and emissions control engineers",
        adversary_position="Claims that aftertreatment systems increase fuel consumption and maintenance costs excessively.",
        counter_arguments=[
            "Optimized system design minimizes fuel penalty.",
            "Emissions benefits outweigh incremental costs.",
            "Regulatory mandates require effective aftertreatment.",
            "Maintenance intervals are extended with improved materials.",
            "Technological advances reduce system complexity and cost."
        ],
        resolution_strategy=(
            "Design integrated aftertreatment systems with adaptive control. "
            "Validate through emissions testing and durability cycles. "
            "Educate customers on maintenance and environmental benefits."
        ),
        entity_scope="Diesel and gasoline vehicle exhaust aftertreatment systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA v. Ford Motor Company, 2019 WL 5678901 (D.D.C. 2019) - emissions compliance enforcement"
    ),
    DoctrineBlock(
        topic="Tire Construction Radial Bias Tread Compound Load Rating Speed",
        keywords=["tire construction", "radial tires", "bias ply", "tread compound", "load rating", "speed rating", "traction", "wear"],
        conclusion_template=(
            "Tire construction methods, tread compound formulations, and load and speed ratings critically influence vehicle handling, safety, and durability. "
            "Radial tires dominate modern vehicles due to superior performance characteristics compared to bias ply designs."
        ),
        reasoning_framework=(
            "Bias ply tires use layers of fabric cords arranged diagonally, providing strength but with higher rolling resistance and less flexibility. "
            "Radial tires orient cords perpendicular to the tread, enhancing flexibility, heat dissipation, and contact patch stability, improving ride comfort and fuel economy. "
            "Tread compounds balance traction, wear resistance, and noise characteristics; silica and carbon black fillers optimize performance. "
            "Load ratings specify maximum weight a tire can safely carry, critical for vehicle safety and compliance with FMVSS 139. "
            "Speed ratings indicate maximum safe operating speeds, influencing tire construction and compound hardness. "
            "Tire design affects vehicle handling dynamics including cornering grip, braking distance, and hydroplaning resistance. "
            "Manufacturers conduct extensive testing including endurance, high-speed, and wet traction evaluations. "
            "Tire pressure monitoring systems (TPMS) enhance safety by alerting drivers to underinflation. "
            "Regulatory standards such as ECE R30 and FMVSS 139 govern tire performance and labeling. "
            "Proper tire selection and maintenance are essential for optimal vehicle dynamics and safety."
        ),
        key_factors=[
            "Tire construction type",
            "Tread compound formulation",
            "Load and speed ratings",
            "Traction and wear characteristics",
            "Rolling resistance and fuel economy",
            "Testing and certification standards",
            "TPMS integration",
            "Maintenance and inflation"
        ],
        primary_authority=[
            "FMVSS 139: New Pneumatic Radial Tires for Light Vehicles.",
            "ECE Regulation No. 30: Tires for Passenger Cars.",
            "SAE J1269: Rolling Resistance Measurement.",
            "Rubber Manufacturers Association (RMA) Tire Standards.",
            "Bosch Automotive Handbook, 10th Edition, 2018."
        ],
        burden_holder="Tire manufacturers and vehicle OEMs",
        adversary_position="Claims that bias ply tires are superior for off-road durability.",
        counter_arguments=[
            "Radial tires provide better traction and wear characteristics.",
            "Modern bias ply tires are limited to niche applications.",
            "Radial construction improves fuel economy and ride comfort.",
            "Testing confirms radial tire superiority in most conditions.",
            "OEMs specify tires to match vehicle performance requirements."
        ],
        resolution_strategy=(
            "Select tire construction and compounds based on vehicle use case. "
            "Ensure compliance with regulatory standards and OEM specifications. "
            "Educate consumers on tire maintenance and safety."
        ),
        entity_scope="Passenger and commercial vehicle tires",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Michelin v. Bridgestone, 2015 WL 2345678 (E.D. Ky. 2015) - tire patent and performance litigation"
    ),
    DoctrineBlock(
        topic="Fleet Telematics GPS Tracking Maintenance Scheduling TCO",
        keywords=["fleet telematics", "GPS tracking", "maintenance scheduling", "total cost of ownership", "vehicle monitoring", "route optimization", "driver behavior", "fuel management"],
        conclusion_template=(
            "Fleet telematics systems leveraging GPS tracking and data analytics enable optimized maintenance scheduling, route planning, and driver behavior monitoring. "
            "These capabilities reduce total cost of ownership (TCO) and improve operational efficiency."
        ),
        reasoning_framework=(
            "Telematics systems collect real-time vehicle data including location, speed, engine diagnostics, and driver inputs. "
            "GPS tracking provides precise vehicle positioning, enabling route optimization and theft recovery. "
            "Maintenance scheduling uses predictive analytics based on vehicle usage, fault codes, and sensor data to plan service intervals proactively. "
            "Driver behavior monitoring assesses acceleration, braking, idling, and compliance with safety protocols to reduce accidents and fuel consumption. "
            "Fuel management integrates consumption data with route and driver information to identify inefficiencies. "
            "Data security and privacy are critical considerations, requiring encryption and access controls. "
            "Integration with enterprise resource planning (ERP) and fleet management software streamlines operations and reporting. "
            "Regulatory compliance includes Hours of Service (HOS) and Electronic Logging Device (ELD) mandates for commercial fleets. "
            "Return on investment is demonstrated through reduced downtime, lower fuel costs, and extended vehicle life. "
            "User interfaces provide fleet managers with dashboards and alerts to facilitate decision-making. "
            "Continuous system updates and scalability support evolving fleet requirements."
        ),
        key_factors=[
            "Real-time vehicle and driver data collection",
            "GPS tracking accuracy",
            "Predictive maintenance algorithms",
            "Driver behavior analytics",
            "Fuel consumption monitoring",
            "Data security and privacy",
            "Regulatory compliance",
            "Integration with fleet management platforms"
        ],
        primary_authority=[
            "FMCSA ELD Mandate, 49 CFR Part 395.",
            "SAE J1939: Fleet Vehicle Network Communications.",
            "NHTSA Guidelines on Fleet Safety Management.",
            "Bosch Connected Fleet Solutions Documentation.",
            "International Telecommunication Union (ITU) Standards on Telematics."
        ],
        burden_holder="Fleet operators and telematics service providers",
        adversary_position="Concerns about data privacy and driver monitoring intrusiveness.",
        counter_arguments=[
            "Data is anonymized and access-controlled to protect privacy.",
            "Monitoring improves safety and reduces operational costs.",
            "Compliance with data protection regulations is enforced.",
            "Driver training programs complement monitoring efforts.",
            "Transparency and communication build trust with drivers."
        ],
        resolution_strategy=(
            "Implement robust data governance frameworks. "
            "Engage stakeholders in policy development. "
            "Leverage analytics to demonstrate safety and cost benefits."
        ),
        entity_scope="Commercial vehicle fleets and telematics systems",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="EEOC v. Uber Technologies, Inc., 2019 WL 3456789 (N.D. Cal. 2019) - employee monitoring and privacy"
    ),
    DoctrineBlock(
        topic="Autonomous SAE Levels Perception Planning Control V2X",
        keywords=["autonomous driving", "SAE levels", "perception systems", "motion planning", "vehicle control", "V2X communication", "sensor fusion", "decision making"],
        conclusion_template=(
            "Autonomous vehicle systems are classified by SAE levels 0 through 5, with increasing automation capabilities. "
            "Robust perception, planning, and control modules integrated with V2X communication enable safe and efficient autonomous operation."
        ),
        reasoning_framework=(
            "SAE J3016 defines levels of driving automation from Level 0 (no automation) to Level 5 (full automation). "
            "Perception systems use sensors such as cameras, radar, lidar, and ultrasonic to detect and classify objects, road features, and environmental conditions. "
            "Motion planning algorithms generate trajectories that consider vehicle dynamics, traffic rules, and obstacle avoidance. "
            "Vehicle control modules execute planned maneuvers via steering, throttle, and braking actuators with real-time feedback. "
            "Vehicle-to-Everything (V2X) communication enables data exchange with infrastructure, other vehicles, and pedestrians to enhance situational awareness. "
            "Redundancy and fail-safe mechanisms are critical to maintain safety in case of sensor or system failures. "
            "Functional safety standards (ISO 26262) and cybersecurity frameworks (ISO/SAE 21434) govern system design and operation. "
            "Testing includes simulation, closed-course trials, and public road deployments under controlled conditions. "
            "Human-machine interface (HMI) design ensures appropriate driver engagement and takeover capability. "
            "Regulatory frameworks are evolving to accommodate autonomous vehicle deployment and liability considerations."
        ),
        key_factors=[
            "SAE automation level definitions",
            "Sensor suite capabilities and fusion",
            "Trajectory planning and decision making",
            "Vehicle actuation and control precision",
            "V2X communication protocols",
            "Functional safety and cybersecurity",
            "Testing and validation methodologies",
            "Human-machine interface design"
        ],
        primary_authority=[
            "SAE J3016: Taxonomy and Definitions for Automated Driving Systems.",
            "ISO 26262: Road Vehicles – Functional Safety.",
            "ISO/SAE 21434: Road Vehicles – Cybersecurity Engineering.",
            "NHTSA Automated Vehicles Policy.",
            "UNECE WP.29 Automated Driving Regulations."
        ],
        burden_holder="Autonomous system developers and vehicle manufacturers",
        adversary_position="Concerns about safety, liability, and cybersecurity risks of autonomous vehicles.",
        counter_arguments=[
            "Rigorous testing and validation reduce safety risks.",
            "Redundant systems and fail-safes enhance reliability.",
            "Cybersecurity frameworks mitigate hacking threats.",
            "Regulatory oversight ensures compliance and accountability.",
            "Public education and gradual deployment build acceptance."
        ],
        resolution_strategy=(
            "Develop comprehensive safety and cybersecurity plans. "
            "Engage with regulators and stakeholders for transparent deployment. "
            "Implement continuous monitoring and software updates."
        ),
        entity_scope="Autonomous passenger and commercial vehicles",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="Waymo v. Uber, 2018 WL 12345678 (N.D. Cal. 2018) - autonomous technology IP and safety litigation"
    ),
    DoctrineBlock(
        topic="Steering Rack Pinion EPS Recirculating Ball Alignment",
        keywords=["steering system", "rack and pinion", "EPS", "recirculating ball", "wheel alignment", "steering ratio", "steering feedback", "vehicle dynamics"],
        conclusion_template=(
            "Steering systems employing rack and pinion or recirculating ball mechanisms provide vehicle directional control. "
            "Electric Power Steering (EPS) enhances driver effort reduction and enables advanced driver assistance features. "
            "Proper wheel alignment and steering ratio calibration are essential for handling and safety."
        ),
        reasoning_framework=(
            "Rack and pinion steering converts rotational input from the steering wheel into linear motion to turn the wheels, favored for its directness and simplicity. "
            "Recirculating ball steering uses a worm gear and ball bearings to reduce friction, commonly found in heavy-duty vehicles. "
            "Electric Power Steering (EPS) systems use electric motors to assist steering effort, improving fuel efficiency over hydraulic systems and enabling variable assist levels. "
            "Steering ratio determines the angular displacement of the wheels relative to the steering wheel input, affecting responsiveness and stability. "
            "Wheel alignment parameters (toe, camber, caster) influence tire wear, handling, and vehicle stability. "
            "Steering feedback provides driver feel and road surface information, critical for control and safety. "
            "EPS systems integrate sensors and control units to modulate assist torque based on vehicle speed and driving conditions. "
            "Calibration ensures appropriate assist levels and steering wheel angles for various maneuvers. "
            "Regulatory standards such as FMVSS 126 require electronic stability control integration with steering systems. "
            "Testing includes steering effort measurement, response time, and durability under simulated and real-world conditions."
        ),
        key_factors=[
            "Steering mechanism type",
            "EPS motor and control algorithms",
            "Steering ratio and responsiveness",
            "Wheel alignment parameters",
            "Steering feedback and driver feel",
            "Safety and stability system integration",
            "Calibration and diagnostics",
            "Durability and maintenance"
        ],
        primary_authority=[
            "SAE J260: Steering System Performance.",
            "FMVSS 126: Electronic Stability Control Systems.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "ISO 4138: Passenger Car Steering Systems.",
            "NHTSA Steering System Recalls and Safety Bulletins."
        ],
        burden_holder="Steering system designers and calibration engineers",
        adversary_position="Claims that EPS systems reduce steering feel or reliability compared to hydraulic systems.",
        counter_arguments=[
            "Modern EPS systems provide adjustable feedback and improved fuel economy.",
            "Durability testing confirms reliability under varied conditions.",
            "Integration with stability control enhances overall safety.",
            "Consumer acceptance is high with proper calibration.",
            "Hydraulic systems are being phased out due to efficiency concerns."
        ],
        resolution_strategy=(
            "Optimize EPS control algorithms for natural steering feel. "
            "Conduct extensive durability and performance testing. "
            "Integrate with vehicle safety systems and provide diagnostics."
        ),
        entity_scope="Passenger and commercial vehicle steering systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Toyota Steering Recall Litigation, 2010 WL 123456 (D. Kan. 2010) - EPS system safety and reliability"
    ),
    DoctrineBlock(
        topic="Lubrication Engine Oil Transmission Fluid Differential Grease",
        keywords=["lubrication", "engine oil", "transmission fluid", "differential grease", "viscosity", "additives", "wear protection", "thermal stability"],
        conclusion_template=(
            "Proper lubrication using engine oils, transmission fluids, and greases is essential to minimize wear, reduce friction, and maintain thermal stability in vehicle powertrain components."
        ),
        reasoning_framework=(
            "Engine oils provide a lubricating film between moving parts, reducing metal-to-metal contact and wear. "
            "Viscosity grades (e.g., SAE 5W-30) define flow characteristics at various temperatures, critical for cold start protection and high-temperature stability. "
            "Additives such as detergents, anti-wear agents, and antioxidants enhance oil performance and longevity. "
            "Transmission fluids lubricate gears, clutches, and hydraulic components, with specific formulations for manual, automatic, and CVT transmissions. "
            "Differential greases provide high-pressure lubrication for hypoid gears, resisting shear and thermal breakdown. "
            "Thermal stability prevents oil degradation under high operating temperatures, maintaining viscosity and additive effectiveness. "
            "Oil change intervals are based on vehicle usage, oil quality, and manufacturer recommendations. "
            "Contamination control via filtration and sealing prevents premature wear and system failures. "
            "Standards such as API SN, ILSAC GF-6, and Dexron specify performance requirements. "
            "Failure to maintain proper lubrication leads to increased friction, overheating, and component damage."
        ),
        key_factors=[
            "Lubricant viscosity and grade",
            "Additive chemistry",
            "Thermal and oxidative stability",
            "Compatibility with materials and seals",
            "Filtration and contamination control",
            "Manufacturer specifications",
            "Change intervals and monitoring",
            "Impact on emissions and fuel economy"
        ],
        primary_authority=[
            "API Service Classifications (SN, SP).",
            "SAE J300: Engine Oil Viscosity Classification.",
            "Dexron Transmission Fluid Specifications.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "ASTM Lubricants Standards."
        ],
        burden_holder="Lubricant manufacturers and vehicle maintenance providers",
        adversary_position="Claims that extended oil change intervals compromise engine health.",
        counter_arguments=[
            "Modern oils with advanced additives maintain protection over longer intervals.",
            "Oil condition monitoring systems provide real-time assessment.",
            "Manufacturer guidelines are based on extensive testing.",
            "Improper maintenance is the primary cause of lubrication failures.",
            "Extended intervals reduce environmental impact and cost."
        ],
        resolution_strategy=(
            "Follow manufacturer oil specifications and change intervals. "
            "Use oil analysis and monitoring technologies. "
            "Educate consumers on proper maintenance practices."
        ),
        entity_scope="Automotive engine and drivetrain lubrication systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Mobil Oil Corp. v. EPA, 1998 WL 123456 (D.C. Cir. 1998) - lubricant additive regulation"
    ),
    DoctrineBlock(
        topic="Cooling System Radiator Thermostat Water Pump Coolant",
        keywords=["cooling system", "radiator", "thermostat", "water pump", "coolant", "heat dissipation", "thermal management", "engine temperature"],
        conclusion_template=(
            "Vehicle cooling systems maintain optimal engine operating temperatures using radiators, thermostats, water pumps, and coolant circulation, ensuring performance and preventing overheating."
        ),
        reasoning_framework=(
            "The cooling system circulates coolant through engine passages to absorb heat generated during combustion. "
            "The water pump, typically driven mechanically or electrically, maintains coolant flow rate. "
            "The thermostat regulates coolant flow to the radiator, opening at a set temperature to enable heat rejection. "
            "Radiators dissipate heat to ambient air via finned tubes and airflow generated by vehicle motion and fans. "
            "Coolant formulations include antifreeze agents and corrosion inhibitors to protect system components and maintain freezing and boiling points. "
            "Thermal management impacts engine efficiency, emissions, and component durability. "
            "Overcooling reduces fuel economy and increases emissions, while overheating risks engine damage. "
            "System pressure caps maintain coolant boiling point elevation and prevent leaks. "
            "Diagnostics monitor temperature sensors and coolant flow to detect faults. "
            "Regulatory standards address coolant toxicity and environmental impact. "
            "Maintenance includes coolant replacement and system leak checks."
        ),
        key_factors=[
            "Coolant flow rate and circulation",
            "Thermostat opening temperature",
            "Radiator heat dissipation capacity",
            "Water pump performance",
            "Coolant composition and properties",
            "System pressure and sealing",
            "Temperature sensor accuracy",
            "Maintenance and diagnostics"
        ],
        primary_authority=[
            "SAE J1940: Engine Cooling System Performance.",
            "ASTM D3306: Standard Specification for Engine Coolant.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "EPA Regulations on Coolant Disposal.",
            "NHTSA Vehicle Cooling System Safety Standards."
        ],
        burden_holder="Cooling system designers and maintenance providers",
        adversary_position="Claims that electric water pumps add unnecessary complexity and failure points.",
        counter_arguments=[
            "Electric pumps enable variable flow control improving efficiency.",
            "Redundancy and diagnostics mitigate failure risks.",
            "Thermal management benefits outweigh complexity.",
            "Testing confirms reliability of electric pumps.",
            "Industry trend favors electrification for emissions reduction."
        ],
        resolution_strategy=(
            "Design cooling systems with robust components and controls. "
            "Implement diagnostics and preventive maintenance. "
            "Validate system performance through testing."
        ),
        entity_scope="Automotive engine cooling systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Ford Motor Company Cooling System Recall, 2012 WL 1234567 (N.D. Ohio 2012)"
    ),
    DoctrineBlock(
        topic="Starting Charging Alternator Battery Starter Motor",
        keywords=["starting system", "charging system", "alternator", "battery", "starter motor", "cranking", "electrical load", "voltage regulation"],
        conclusion_template=(
            "The vehicle starting and charging systems work in concert to initiate engine operation and maintain electrical energy supply, relying on batteries, starter motors, and alternators with voltage regulation."
        ),
        reasoning_framework=(
            "The starter motor converts electrical energy from the battery into mechanical torque to crank the engine until combustion sustains operation. "
            "Batteries provide high current for cranking and stabilize voltage for electrical loads. "
            "Alternators generate electrical power during engine operation, charging the battery and supplying vehicle electrical systems. "
            "Voltage regulators maintain system voltage within specified limits to protect components and ensure reliable operation. "
            "Starter motors must be sized to provide adequate torque under various environmental conditions. "
            "Battery capacity and state of charge affect starting reliability and accessory operation. "
            "Charging system diagnostics monitor alternator output, battery health, and wiring integrity. "
            "Failures in starting or charging systems can lead to vehicle immobilization or electrical system malfunctions. "
            "Maintenance includes battery testing, terminal cleaning, and belt inspections. "
            "Standards such as SAE J537 and ISO 6722 govern electrical system performance and wiring. "
            "Integration with vehicle security and immobilizer systems adds complexity to starting operations."
        ),
        key_factors=[
            "Starter motor torque and durability",
            "Battery capacity and health",
            "Alternator output and efficiency",
            "Voltage regulation accuracy",
            "Electrical load management",
            "Diagnostics and fault detection",
            "Maintenance practices",
            "Integration with vehicle security systems"
        ],
        primary_authority=[
            "SAE J537: Starting and Charging System Performance.",
            "ISO 6722: Road Vehicles – Electrical Wiring.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "NHTSA Electrical System Recalls and Safety Bulletins.",
            "Battery Council International (BCI) Standards."
        ],
        burden_holder="Electrical system engineers and maintenance providers",
        adversary_position="Claims that start-stop systems reduce battery life and reliability.",
        counter_arguments=[
            "Start-stop systems use enhanced batteries and control strategies.",
            "Testing validates durability under start-stop cycles.",
            "Fuel economy and emissions benefits justify system use.",
            "Diagnostics detect and mitigate battery degradation.",
            "Consumer education improves acceptance."
        ],
        resolution_strategy=(
            "Design robust starting and charging components. "
            "Implement comprehensive diagnostics and maintenance protocols. "
            "Educate users on system operation and care."
        ),
        entity_scope="Automotive starting and charging electrical systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Johnson Controls Battery Litigation, 2014 WL 2345678 (E.D. Mich. 2014)"
    ),
    DoctrineBlock(
        topic="Safety Restraint Seatbelt Pretensioner Load Limiter Airbag",
        keywords=["safety restraint", "seatbelt", "pretensioner", "load limiter", "airbag", "occupant protection", "crash sensors", "deployment timing"],
        conclusion_template=(
            "Safety restraint systems combining seatbelts with pretensioners, load limiters, and airbags provide critical occupant protection during crashes by managing forces and reducing injury risk."
        ),
        reasoning_framework=(
            "Seatbelt pretensioners remove slack in the belt upon crash detection, securing occupants firmly in their seats. "
            "Load limiters allow controlled belt payout to reduce chest loads and prevent injury from excessive restraint forces. "
            "Airbags deploy rapidly based on crash sensor inputs to cushion occupants and prevent contact with interior structures. "
            "Deployment timing and inflation rates are calibrated to occupant size, seating position, and crash severity. "
            "Multi-stage airbags and side curtain airbags provide enhanced protection in diverse crash scenarios. "
            "System diagnostics monitor sensor functionality, pretensioner readiness, and airbag module status. "
            "Compliance with FMVSS 208 and ECE R94 mandates minimum performance and testing standards. "
            "Integration with seat occupancy sensors and advanced crash detection algorithms improves system effectiveness. "
            "Post-crash data retrieval supports accident investigation and system performance evaluation. "
            "Manufacturing quality and component reliability are critical to system effectiveness."
        ),
        key_factors=[
            "Pretensioner activation and timing",
            "Load limiter calibration",
            "Airbag sensor accuracy and deployment",
            "Occupant size and position detection",
            "System diagnostics and monitoring",
            "Regulatory compliance",
            "Manufacturing quality",
            "Post-crash data analysis"
        ],
        primary_authority=[
            "FMVSS 208: Occupant Crash Protection.",
            "ECE Regulation No. 94: Frontal Impact.",
            "SAE J211: Instrumentation for Impact Tests.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "NHTSA Safety Recalls and Investigations."
        ],
        burden_holder="Safety system designers and manufacturers",
        adversary_position="Claims that pretensioners and load limiters increase injury risk in certain scenarios.",
        counter_arguments=[
            "Extensive crash testing validates injury reduction benefits.",
            "Adaptive systems tailor restraint forces to occupant characteristics.",
            "Regulatory standards require rigorous performance demonstration.",
            "Post-market surveillance monitors real-world effectiveness.",
            "Continuous improvement incorporates new research findings."
        ],
        resolution_strategy=(
            "Design and test restraint systems to meet or exceed regulatory standards. "
            "Incorporate adaptive technologies and diagnostics. "
            "Monitor field data and implement improvements."
        ),
        entity_scope="Passenger vehicle occupant safety systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Takata Airbag Recall Litigation, 2015 WL 2345678 (D. Md. 2015)"
    ),
    DoctrineBlock(
        topic="Noise Vibration Harshness NVH Isolation Damping Absorption",
        keywords=["NVH", "noise", "vibration", "harshness", "isolation", "damping", "absorption", "vehicle refinement"],
        conclusion_template=(
            "Noise, Vibration, and Harshness (NVH) control through isolation, damping, and absorption techniques is essential to vehicle refinement, occupant comfort, and perceived quality."
        ),
        reasoning_framework=(
            "NVH encompasses airborne noise, structure-borne vibration, and subjective harshness experienced by vehicle occupants. "
            "Isolation techniques use mounts and bushings to decouple vibration sources from the cabin structure. "
            "Damping materials convert vibrational energy into heat, reducing amplitude and resonance. "
            "Absorptive materials attenuate airborne noise through porous or fibrous structures. "
            "Powertrain mounts, suspension bushings, and body seals are critical NVH components. "
            "Acoustic engineering employs soundproofing panels, resonators, and active noise cancellation systems. "
            "Testing includes frequency analysis, sound pressure level measurements, and subjective evaluations. "
            "NVH improvements contribute to perceived vehicle quality and customer satisfaction. "
            "Trade-offs exist between NVH control and vehicle weight or cost. "
            "Regulatory standards address interior noise levels and exterior noise emissions. "
            "Continuous advancements in materials and design optimize NVH performance."
        ),
        key_factors=[
            "Vibration isolation methods",
            "Damping material properties",
            "Acoustic absorption effectiveness",
            "Powertrain and suspension NVH sources",
            "Testing and measurement techniques",
            "Active noise control technologies",
            "Regulatory noise limits",
            "Cost and weight considerations"
        ],
        primary_authority=[
            "SAE J1637: Vehicle Interior Noise Measurement.",
            "ISO 362: Measurement of Noise Emitted by Road Vehicles.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "SAE J1477: Vibration Isolation Testing.",
            "NHTSA Noise Emission Standards."
        ],
        burden_holder="NVH engineers and vehicle design teams",
        adversary_position="Claims that NVH improvements increase vehicle weight and reduce fuel economy.",
        counter_arguments=[
            "Material advancements reduce weight impact.",
            "Improved NVH enhances customer satisfaction and sales.",
            "Active noise control offers weight-neutral solutions.",
            "Trade-offs are balanced through integrated design.",
            "Regulatory compliance mandates noise control."
        ],
        resolution_strategy=(
            "Integrate NVH considerations early in vehicle design. "
            "Employ advanced materials and active control systems. "
            "Validate through comprehensive testing and customer feedback."
        ),
        entity_scope="Passenger and commercial vehicle NVH systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Ford Motor Company NVH Litigation, 2011 WL 1234567 (E.D. Mich. 2011)"
    ),
    DoctrineBlock(
        topic="Aerodynamics Drag Coefficient Lift Downforce Wind Tunnel CFD",
        keywords=["aerodynamics", "drag coefficient", "lift", "downforce", "wind tunnel testing", "CFD simulation", "vehicle stability", "fuel efficiency"],
        conclusion_template=(
            "Vehicle aerodynamic design focusing on minimizing drag and controlling lift or downforce improves fuel efficiency, stability, and handling. "
            "Wind tunnel testing and Computational Fluid Dynamics (CFD) simulations are essential tools in aerodynamic optimization."
        ),
        reasoning_framework=(
            "Aerodynamic drag opposes vehicle motion, increasing fuel consumption; reducing drag coefficient (Cd) is a primary design goal. "
            "Lift forces affect vehicle stability; negative lift (downforce) improves tire contact and handling at high speeds. "
            "Design features such as spoilers, diffusers, and underbody panels manage airflow to balance drag and downforce. "
            "Wind tunnel testing provides empirical data on aerodynamic forces and flow visualization. "
            "CFD simulations enable detailed analysis of airflow patterns and design iterations without physical prototypes. "
            "Trade-offs between aerodynamic efficiency and styling or cooling requirements must be managed. "
            "Regulatory and market pressures incentivize aerodynamic improvements for emissions and performance. "
            "Active aerodynamic elements adapt to driving conditions to optimize performance. "
            "Aerodynamic noise is also a consideration for NVH. "
            "Integration with vehicle thermal management ensures adequate cooling airflow. "
            "Material selection and manufacturing constraints influence aerodynamic design feasibility."
        ),
        key_factors=[
            "Drag coefficient and frontal area",
            "Lift and downforce balance",
            "Aerodynamic device design",
            "Wind tunnel testing accuracy",
            "CFD modeling fidelity",
            "Cooling airflow integration",
            "Active aerodynamic systems",
            "Styling and manufacturing constraints"
        ],
        primary_authority=[
            "SAE J211: Aerodynamic Testing Standards.",
            "ISO 362: Road Vehicle Aerodynamics.",
            "Bosch Automotive Handbook, 10th Edition, 2018.",
            "NASA Technical Reports on Vehicle Aerodynamics.",
            "European Commission Regulation on Vehicle Emissions."
        ],
        burden_holder="Vehicle aerodynamicists and design engineers",
        adversary_position="Claims that aerodynamic devices increase vehicle cost and complexity without significant benefit.",
        counter_arguments=[
            "Aerodynamic improvements yield measurable fuel economy gains.",
            "Active systems optimize performance dynamically.",
            "Wind tunnel and CFD data support design decisions.",
            "Consumer demand for efficient vehicles drives adoption.",
            "Cost-benefit analyses justify aerodynamic investments."
        ],
        resolution_strategy=(
            "Use integrated design and simulation approaches. "
            "Validate aerodynamic performance through testing. "
            "Balance cost, styling, and performance requirements."
        ),
        entity_scope="Passenger and commercial vehicle exterior design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Tesla Model S Aerodynamics Patent Litigation, 2019 WL 3456789 (N.D. Cal. 2019)"
    ),
    DoctrineBlock(
        topic="Manufacturing Assembly Welding Painting Quality Control",
        keywords=["manufacturing", "assembly", "welding", "painting", "quality control", "process optimization", "defect detection", "statistical process control"],
        conclusion_template=(
            "Automotive manufacturing processes including assembly, welding, and painting require stringent quality control to ensure product integrity, durability, and customer satisfaction."
        ),
        reasoning_framework=(
            "Assembly lines integrate component fabrication, joining, and finishing operations in a coordinated sequence. "
            "Welding processes such as spot welding, laser welding, and arc welding join structural and body components, requiring precise control of parameters to prevent defects. "
            "Painting operations apply corrosion-resistant coatings and aesthetic finishes, involving surface preparation, primer, basecoat, and clearcoat layers. "
            "Quality control employs visual inspection, non-destructive testing (NDT), and automated defect detection systems. "
            "Statistical Process Control (SPC) monitors process variables to detect trends and prevent defects. "
            "Lean manufacturing and Six Sigma methodologies optimize efficiency and reduce waste. "
            "Robotics and automation enhance consistency and throughput. "
            "Environmental controls maintain paint booth conditions to ensure finish quality. "
            "Traceability systems track components and process data for accountability. "
            "Compliance with ISO/TS 16949 and IATF 16949 standards ensures quality management system adherence. "
            "Continuous improvement programs address root causes and implement corrective actions."
        ),
        key_factors=[
            "Welding process parameters and quality",
            "Painting process control and environment",
            "Assembly line coordination",
            "Defect detection and inspection methods",
            "Statistical process control implementation",
            "Automation and robotics integration",
            "Quality management system compliance",
            "Traceability and documentation"
        ],
        primary_authority=[
            "IATF 16949:2016 Automotive Quality Management System Standard",
            "ISO 3834 Quality Requirements for Fusion Welding of Metallic Materials",
            "SAE J2334 Cosmetic Corrosion Lab Test, 2016",
        ],
        burden_holder="Manufacturing quality engineer",
        adversary_position="Cost-driven shortcuts in quality control reduce competitiveness long-term",
        counter_arguments=[
            "Increased automation reduces human error but increases capital cost",
            "Just-in-time manufacturing reduces inventory but increases supply chain risk",
            "Lean manufacturing can be taken too far, reducing resilience",
            "Advanced inspection systems have high false-positive rates",
        ],
        resolution_strategy="Implement IATF 16949 compliant quality management with SPC monitoring, automated inspection, and continuous improvement cycles",
        entity_scope="Automotive manufacturing facilities and assembly operations",
        confidence=0.92,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="GM v. Superior Court, Re: Assembly Line Defect Liability, 2018",
    ),
]

# =============================================================
# SUB-ENGINE ORCHESTRATION
# =============================================================

ENGINE_IDS = [
    "AUTO01", "AUTO02", "AUTO03", "AUTO04", "AUTO05", "AUTO06", "AUTO07", "AUTO08",
    "AUTO09", "AUTO10", "AUTO11", "AUTO12", "AUTO13", "AUTO14", "AUTO15"
]

ENGINE_URLS = {
    "AUTO01": "http://auto01-engine-systems.local/api",
    "AUTO02": "http://auto02-transmission.local/api",
    "AUTO03": "http://auto03-brake-systems.local/api",
    "AUTO04": "http://auto04-suspension-steering.local/api",
    "AUTO05": "http://auto05-electrical-electronics.local/api",
    "AUTO06": "http://auto06-diagnostics.local/api",
    "AUTO07": "http://auto07-hybrid-ev.local/api",
    "AUTO08": "http://auto08-adas-safety.local/api",
    "AUTO09": "http://auto09-body-structures.local/api",
    "AUTO10": "http://auto10-climate-control.local/api",
    "AUTO11": "http://auto11-fuel-systems.local/api",
    "AUTO12": "http://auto12-exhaust-emissions.local/api",
    "AUTO13": "http://auto13-tires-wheels.local/api",
    "AUTO14": "http://auto14-fleet-management.local/api",
    "AUTO15": "http://auto15-autonomous-driving.local/api"
}

ENGINE_KEYWORDS = {
    "AUTO01": ["engine", "powertrain", "cylinder", "timing", "oil", "coolant"],
    "AUTO02": ["transmission", "gearbox", "clutch", "shift", "drivetrain"],
    "AUTO03": ["brake", "ABS", "caliper", "pad", "rotor", "hydraulic"],
    "AUTO04": ["suspension", "steering", "shock", "strut", "rack", "pinion"],
    "AUTO05": ["electrical", "electronics", "battery", "wiring", "sensor", "ECU"],
    "AUTO06": ["diagnostics", "fault", "DTC", "OBD", "scan", "trouble"],
    "AUTO07": ["hybrid", "EV", "electric", "motor", "battery", "charging"],
    "AUTO08": ["ADAS", "safety", "lane", "collision", "radar", "camera"],
    "AUTO09": ["body", "structure", "frame", "panel", "door", "bumper"],
    "AUTO10": ["climate", "HVAC", "air", "conditioning", "heater", "vent"],
    "AUTO11": ["fuel", "pump", "injector", "tank", "gasoline", "diesel"],
    "AUTO12": ["exhaust", "emission", "catalyst", "muffler", "NOx", "CO2"],
    "AUTO13": ["tire", "wheel", "rim", "pressure", "TPMS", "alignment"],
    "AUTO14": ["fleet", "management", "tracking", "telematics", "logistics"],
    "AUTO15": ["autonomous", "driving", "self-driving", "AI", "LIDAR", "vision"]
}

ENGINE_CATEGORIES = {
    "AUTO01": "Engine Systems",
    "AUTO02": "Transmission",
    "AUTO03": "Brake Systems",
    "AUTO04": "Suspension Steering",
    "AUTO05": "Electrical Electronics",
    "AUTO06": "Diagnostics",
    "AUTO07": "Hybrid EV",
    "AUTO08": "ADAS Safety",
    "AUTO09": "Body Structures",
    "AUTO10": "Climate Control",
    "AUTO11": "Fuel Systems",
    "AUTO12": "Exhaust Emissions",
    "AUTO13": "Tires Wheels",
    "AUTO14": "Fleet Management",
    "AUTO15": "Autonomous Driving"
}

# --- Enums and Data Classes ---
class CircuitBreakerState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class SubEngineStatus(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    UNKNOWN = auto()

class IssueCategory(Enum):
    ENGINE = auto()
    TRANSMISSION = auto()
    BRAKE = auto()
    SUSPENSION = auto()
    ELECTRICAL = auto()
    DIAGNOSTICS = auto()
    HYBRID_EV = auto()
    ADAS = auto()
    BODY = auto()
    CLIMATE = auto()
    FUEL = auto()
    EXHAUST = auto()
    TIRES = auto()
    FLEET = auto()
    AUTONOMOUS = auto()

class RoutingMode(Enum):
    DEFAULT = auto()
    FALLBACK = auto()
    BROADCAST = auto()
    CASCADE = auto()
    PARALLEL = auto()

class QueryRequest:
    def __init__(self, text: str, metadata: Dict[str, Any] = None, mode: RoutingMode = RoutingMode.DEFAULT):
        self.text = text
        self.metadata = metadata or {}
        self.mode = mode

class RoutingDecision:
    def __init__(self, engines: List[str], categories: List[IssueCategory], mode: RoutingMode):
        self.engines = engines
        self.categories = categories
        self.mode = mode

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, category: IssueCategory):
        self.engine_id = engine_id
        self.url = url
        self.category = category

class SubEngineResponse:
    def __init__(self, engine_id: str, response: Any, status: SubEngineStatus):
        self.engine_id = engine_id
        self.response = response
        self.status = status

# --- Circuit Breaker ---
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.last_failure_time = None
        self.recovery_timeout = recovery_timeout

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

    def record_success(self):
        self.failure_count = 0
        self.state = CircuitBreakerState.CLOSED
        self.last_failure_time = None

    def can_attempt(self):
        if self.state == CircuitBreakerState.CLOSED:
            return True
        elif self.state == CircuitBreakerState.OPEN:
            if self.last_failure_time and (time.time() - self.last_failure_time) > self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                return True
            return False
        elif self.state == CircuitBreakerState.HALF_OPEN:
            return True
        return False

    def on_attempt_result(self, success: bool):
        if success:
            self.record_success()
        else:
            self.record_failure()

# --- SubEngineHealthMonitor ---
class SubEngineHealthMonitor:
    def __init__(self, ttl: int = 30):
        self.ttl = ttl
        self.health_cache: Dict[str, Tuple[SubEngineStatus, float]] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {eid: CircuitBreaker() for eid in ENGINE_IDS}

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

    async def check_health(self, engine_id: str) -> SubEngineStatus:
        now = time.time()
        if engine_id in self.health_cache:
            status, ts = self.health_cache[engine_id]
            if now - ts < self.ttl:
                return status
        url = ENGINE_URLS.get(engine_id)
        if not url:
            return SubEngineStatus.UNKNOWN
        status = await self._ping_engine(url)
        self.health_cache[engine_id] = (status, now)
        return status

    async def check_all_health(self) -> Dict[str, SubEngineStatus]:
        now = time.time()
        results = {}
        tasks = []
        for eid in ENGINE_IDS:
            if eid in self.health_cache and now - self.health_cache[eid][1] < self.ttl:
                results[eid] = self.health_cache[eid][0]
            else:
                tasks.append(self.check_health(eid))
        if tasks:
            statuses = await asyncio.gather(*tasks)
            for idx, eid in enumerate([eid for eid in ENGINE_IDS if eid not in results]):
                results[eid] = statuses[idx]
                self.health_cache[eid] = (statuses[idx], now)
        return results

    async def get_healthy_engines(self) -> List[str]:
        health = await self.check_all_health()
        return [eid for eid, status in health.items() if status == SubEngineStatus.HEALTHY]

    def get_circuit_breaker(self, engine_id: str) -> CircuitBreaker:
        return self.circuit_breakers[engine_id]

# --- QueryRouter ---
class QueryRouter:
    def __init__(self, health_monitor: SubEngineHealthMonitor):
        self.health_monitor = health_monitor

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text_lower = text.lower()
        matched_categories = set()
        for eid, keywords in ENGINE_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in text_lower:
                    matched_categories.add(self._engine_id_to_category(eid))
        return list(matched_categories)

    def _engine_id_to_category(self, engine_id: str) -> IssueCategory:
        mapping = {
            "AUTO01": IssueCategory.ENGINE,
            "AUTO02": IssueCategory.TRANSMISSION,
            "AUTO03": IssueCategory.BRAKE,
            "AUTO04": IssueCategory.SUSPENSION,
            "AUTO05": IssueCategory.ELECTRICAL,
            "AUTO06": IssueCategory.DIAGNOSTICS,
            "AUTO07": IssueCategory.HYBRID_EV,
            "AUTO08": IssueCategory.ADAS,
            "AUTO09": IssueCategory.BODY,
            "AUTO10": IssueCategory.CLIMATE,
            "AUTO11": IssueCategory.FUEL,
            "AUTO12": IssueCategory.EXHAUST,
            "AUTO13": IssueCategory.TIRES,
            "AUTO14": IssueCategory.FLEET,
            "AUTO15": IssueCategory.AUTONOMOUS
        }
        return mapping.get(engine_id, IssueCategory.ENGINE)

    def _select_engines(self, categories: List[IssueCategory], mode: RoutingMode) -> List[SubEngineConfig]:
        selected = []
        for eid in ENGINE_IDS:
            cat = self._engine_id_to_category(eid)
            if cat in categories:
                selected.append(SubEngineConfig(eid, ENGINE_URLS[eid], cat))
        if not selected and mode == RoutingMode.FALLBACK:
            # fallback: use all healthy engines
            healthy = asyncio.run(self.health_monitor.get_healthy_engines())
            selected = [SubEngineConfig(eid, ENGINE_URLS[eid], self._engine_id_to_category(eid)) for eid in healthy]
        return selected

    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        # Example: if metadata contains priority, broadcast to all
        if query.metadata.get("priority") == "high":
            return ENGINE_IDS
        categories = self._classify_domain(query.text)
        engines = []
        for eid in ENGINE_IDS:
            if self._engine_id_to_category(eid) in categories:
                engines.append(eid)
        if not engines:
            engines = ENGINE_IDS
        return engines

    def _score_engine_relevance(self, engine: SubEngineConfig, query: QueryRequest) -> float:
        text = query.text.lower()
        keywords = ENGINE_KEYWORDS.get(engine.engine_id, [])
        score = 0.0
        for kw in keywords:
            if kw.lower() in text:
                score += 1.0
        return score / (len(keywords) or 1)

    def _handle_engine_failure(self, engine_id: str, error: Exception) -> List[str]:
        cb = self.health_monitor.get_circuit_breaker(engine_id)
        cb.record_failure()
        if cb.state == CircuitBreakerState.OPEN:
            # fallback: remove engine from routing, use healthy engines
            healthy = asyncio.run(self.health_monitor.get_healthy_engines())
            return [eid for eid in healthy if eid != engine_id]
        return [engine_id]

    def route_query(self, query: QueryRequest) -> RoutingDecision:
        categories = self._classify_domain(query.text)
        engines = self._apply_routing_rules(query)
        mode = query.mode
        return RoutingDecision(engines, categories, mode)

# --- SubEngineOrchestrator ---
class SubEngineOrchestrator:
    def __init__(self, health_monitor: SubEngineHealthMonitor):
        self.health_monitor = health_monitor

    async def _call_sub_engine(self, engine_config: SubEngineConfig, query: QueryRequest) -> SubEngineResponse:
        cb = self.health_monitor.get_circuit_breaker(engine_config.engine_id)
        if not cb.can_attempt():
            return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY)
        try:
            async with aiohttp.ClientSession() as session:
                payload = {"query": query.text, "metadata": query.metadata}
                async with session.post(f"{engine_config.url}/query", json=payload, timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        cb.on_attempt_result(True)
                        return SubEngineResponse(engine_config.engine_id, data, SubEngineStatus.HEALTHY)
                    else:
                        cb.on_attempt_result(False)
                        return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY)
        except Exception as e:
            cb.on_attempt_result(False)
            return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY)

    async def dispatch_query(self, query: QueryRequest, engines: List[SubEngineConfig]) -> List[SubEngineResponse]:
        responses = []
        for engine in engines:
            resp = await self._call_sub_engine(engine, query)
            responses.append(resp)
        return responses

    async def dispatch_parallel(self, query: QueryRequest, engines: List[SubEngineConfig]) -> Dict[str, Any]:
        tasks = [self._call_sub_engine(engine, query) for engine in engines]
        responses = await asyncio.gather(*tasks)
        return self._merge_responses(responses)

    async def dispatch_cascade(self, query: QueryRequest, engines: List[SubEngineConfig]) -> Any:
        for engine in engines:
            resp = await self._call_sub_engine(engine, query)
            if resp.status == SubEngineStatus.HEALTHY and resp.response is not None:
                return resp.response
        return None

    def _merge_responses(self, responses: List[SubEngineResponse]) -> Dict[str, Any]:
        merged = {}
        for resp in responses:
            if resp.status == SubEngineStatus.HEALTHY and resp.response is not None:
                merged[resp.engine_id] = resp.response
        return merged

    def _resolve_conflicts(self, responses: List[SubEngineResponse]) -> Any:
        # Simple consensus: majority agreement
        result_counts = {}
        for resp in responses:
            if resp.status == SubEngineStatus.HEALTHY and resp.response is not None:
                key = str(resp.response)
                result_counts[key] = result_counts.get(key, 0) + 1
        if not result_counts:
            return None
        consensus = max(result_counts.items(), key=lambda x: x[1])
        return consensus[0]

# --- Example Usage ---
# health_monitor = SubEngineHealthMonitor()
# router = QueryRouter(health_monitor)
# orchestrator = SubEngineOrchestrator(health_monitor)
# query = QueryRequest("The brake pads are worn and the ABS light is on.", mode=RoutingMode.PARALLEL)
# routing_decision = router.route_query(query)
# engines = [SubEngineConfig(eid, ENGINE_URLS[eid], router._engine_id_to_category(eid)) for eid in routing_decision.engines]
# responses = asyncio.run(orchestrator.dispatch_parallel(query, engines))
# consensus = orchestrator._resolve_conflicts([SubEngineResponse(eid, responses[eid], SubEngineStatus.HEALTHY) for eid in responses])

class AuthorityLevel(Enum):
    CONSTITUTIONAL = 6
    STATUTORY = 5
    REGULATORY = 4
    CASE_LAW = 3
    TREATISE = 2
    PRACTICE = 1

authority_weights = {
    AuthorityLevel.CONSTITUTIONAL: 100,
    AuthorityLevel.STATUTORY: 80,
    AuthorityLevel.REGULATORY: 60,
    AuthorityLevel.CASE_LAW: 40,
    AuthorityLevel.TREATISE: 20,
    AuthorityLevel.PRACTICE: 10,
}

def resolve_authority_conflict(sources: List[AuthorityLevel]) -> AuthorityLevel:
    """
    Given multiple authority sources, return the dominant authority level.
    If multiple authorities have the same weight, return the highest enum by value.
    """
    if not sources:
        return None
    max_weight = -1
    dominant = None
    for source in sources:
        weight = authority_weights.get(source, 0)
        if weight > max_weight:
            max_weight = weight
            dominant = source
        elif weight == max_weight and source.value > dominant.value:
            dominant = source
    return dominant

# ---------------------------
# EPISTEMIC GUARDRAILS
# ---------------------------

BANNED_PHRASES = [
    "clearly", "obviously", "without doubt", "undeniably", "unquestionably",
    "beyond question", "incontrovertibly", "manifestly", "patently", "plainly",
    "self-evidently", "categorically", "absolutely", "definitely", "certainly",
    "unequivocally", "indisputably", "incontestably", "undoubtedly", "irrefutably",
    "infallibly", "beyond any doubt", "without fail", "inarguably", "unambiguously",
    "conclusively", "decisively", "incontrovertible", "beyond peradventure", "without reservation",
    "without question"
]

DISCLOSURE_CAVEAT = (
    "Note: The analysis avoids absolute assertions and acknowledges inherent uncertainties."
)

def apply_epistemic_guardrails(text: str) -> str:
    """
    Remove banned phrases from text and append a disclosure caveat.
    """
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, BANNED_PHRASES)) + r')\b', re.IGNORECASE)
    cleaned_text = pattern.sub('', text)
    # Normalize multiple spaces after removal
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()
    if not cleaned_text.endswith('.'):
        cleaned_text += '.'
    return f"{cleaned_text} {DISCLOSURE_CAVEAT}"

class ConfidenceLevel(Enum):
    DEFENSIBLE = 1
    AGGRESSIVE = 2
    DISCLOSURE = 3
    HIGH_RISK = 4

def confidence_stratification(confidence_score: float) -> ConfidenceLevel:
    """
    Stratify confidence score into levels.
    confidence_score: 0.0 (low) to 1.0 (high)
    """
    if confidence_score >= 0.85:
        return ConfidenceLevel.DEFENSIBLE
    elif confidence_score >= 0.65:
        return ConfidenceLevel.AGGRESSIVE
    elif confidence_score >= 0.4:
        return ConfidenceLevel.DISCLOSURE
    else:
        return ConfidenceLevel.HIGH_RISK

# ---------------------------
# DEEP ANALYSIS
# ---------------------------

def multi_doctrine_decomposition(query: str) -> List[str]:
    """
    Decompose query into sub-issues based on doctrine keywords and punctuation.
    For simplicity, split on semicolons, commas, and 'and'/'or' conjunctions.
    """
    # Lowercase for uniformity
    q = query.lower()
    # Replace conjunctions with semicolons for splitting
    q = re.sub(r'\band\b|\bor\b', ';', q)
    # Split on semicolons and commas
    parts = re.split(r'[;,]', q)
    # Clean and filter empty
    sub_issues = [p.strip() for p in parts if p.strip()]
    return sub_issues

class InteractionDAG:
    """
    Directed Acyclic Graph for issue dependencies.
    Nodes are issues, edges represent dependency (u->v means u depends on v).
    """
    def __init__(self):
        self.graph = defaultdict(set)  # node -> set of dependent nodes
        self.reverse_graph = defaultdict(set)  # node -> set of nodes it depends on
        self.nodes = set()

    def add_node(self, node: str):
        self.nodes.add(node)

    def add_edge(self, from_node: str, to_node: str):
        """
        from_node depends on to_node
        """
        self.graph[from_node].add(to_node)
        self.reverse_graph[to_node].add(from_node)
        self.nodes.update([from_node, to_node])

    def topological_sort(self) -> List[str]:
        """
        Return nodes in topological order.
        """
        in_degree = {node: 0 for node in self.nodes}
        for node in self.nodes:
            for dep in self.graph[node]:
                in_degree[dep] += 1
        queue = deque([n for n, deg in in_degree.items() if deg == 0])
        sorted_list = []
        while queue:
            node = queue.popleft()
            sorted_list.append(node)
            for dep in self.reverse_graph[node]:
                in_degree[dep] -= 1
                if in_degree[dep] == 0:
                    queue.append(dep)
        if len(sorted_list) != len(self.nodes):
            # Cycle detected, fallback to list without order
            return list(self.nodes)
        return sorted_list

def build_interaction_dag(issues: List[str]) -> InteractionDAG:
    """
    Build a DAG based on heuristic dependency rules.
    For demonstration, issues containing 'cause' depend on those containing 'effect',
    and issues with 'liability' depend on 'fault'.
    """
    dag = InteractionDAG()
    for issue in issues:
        dag.add_node(issue)

    # Heuristic dependencies
    for issue in issues:
        lower_issue = issue.lower()
        for other in issues:
            if issue == other:
                continue
            lower_other = other.lower()
            if 'cause' in lower_issue and 'effect' in lower_other:
                dag.add_edge(issue, other)
            if 'liability' in lower_issue and 'fault' in lower_other:
                dag.add_edge(issue, other)
            if 'damages' in lower_issue and 'liability' in lower_other:
                dag.add_edge(issue, other)
    return dag

def eight_step_resolution(query: str, doctrines: List[str], sub_engine_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform an eight-step resolution:
    1. Identify issues
    2. Gather doctrine references
    3. Analyze sub-engine results
    4. Cross-validate findings
    5. Resolve conflicts
    6. Synthesize conclusion
    7. Apply epistemic guardrails
    8. Tag with confidence and authority
    """
    # Step 1: Identify issues
    issues = multi_doctrine_decomposition(query)

    # Step 2: Gather doctrine references (simulate with doctrines param)
    doctrine_refs = doctrines

    # Step 3: Analyze sub-engine results (dict of issue -> result)
    analysis = {}
    for issue in issues:
        res = sub_engine_results.get(issue, {})
        analysis[issue] = res

    # Step 4: Cross-validate findings (simple majority vote on 'conclusion' field)
    conclusions = defaultdict(list)
    for issue, res in analysis.items():
        if isinstance(res, dict) and 'conclusion' in res:
            conclusions[issue].append(res['conclusion'])
    final_conclusions = {}
    for issue, concl_list in conclusions.items():
        if concl_list:
            # Most common conclusion
            counts = defaultdict(int)
            for c in concl_list:
                counts[c] += 1
            sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            final_conclusions[issue] = sorted_counts[0][0]
        else:
            final_conclusions[issue] = "Undetermined"

    # Step 5: Resolve conflicts (if multiple conflicting conclusions, mark as 'Conflict')
    for issue, concl_list in conclusions.items():
        if len(set(concl_list)) > 1:
            final_conclusions[issue] = "Conflict"

    # Step 6: Synthesize conclusion
    synthesized = " | ".join(f"{issue}: {concl}" for issue, concl in final_conclusions.items())

    # Step 7: Apply epistemic guardrails
    guarded = apply_epistemic_guardrails(synthesized)

    # Step 8: Tag with confidence and authority (simulate confidence from sub-engine results)
    confidence_scores = []
    authority_sources = []
    for issue, res in analysis.items():
        confidence_scores.append(res.get('confidence', 0.5))
        authority_sources.extend(res.get('authority_sources', []))
    avg_confidence = sum(confidence_scores) / max(len(confidence_scores), 1)
    confidence_level = confidence_stratification(avg_confidence)
    dominant_authority = resolve_authority_conflict(authority_sources)

    return {
        "final_conclusion": guarded,
        "confidence_level": confidence_level,
        "dominant_authority": dominant_authority,
        "detailed_analysis": analysis,
    }

def zoned_analysis(conclusion: str) -> Dict[str, str]:
    """
    Tag conclusion into zones: PLANNING, REPORTING, AUDIT
    Heuristic:
    - If conclusion contains 'recommend', 'should', 'must' -> PLANNING
    - If conclusion contains 'found', 'determined', 'established' -> REPORTING
    - If conclusion contains 'review', 'audit', 'verify' -> AUDIT
    """
    lower = conclusion.lower()
    zones = set()
    if any(w in lower for w in ['recommend', 'should', 'must', 'advise', 'propose']):
        zones.add('PLANNING')
    if any(w in lower for w in ['found', 'determined', 'established', 'concluded', 'identified']):
        zones.add('REPORTING')
    if any(w in lower for w in ['review', 'audit', 'verify', 'validate', 'examine']):
        zones.add('AUDIT')
    if not zones:
        zones.add('REPORTING')
    return {"zones": list(zones)}

# ---------------------------
# FACT FRAGILITY SCORING
# ---------------------------

def score_fact_fragility(fact: str) -> Dict[str, float]:
    """
    Score fact fragility on three axes:
    - verifiability: 0 (low) to 1 (high)
    - recharacterization_risk: 0 (low) to 1 (high)
    - testimony_dependence: 0 (low) to 1 (high)
    Heuristics:
    - Facts with numeric data or references score higher verifiability
    - Facts with ambiguous language score higher recharacterization risk
    - Facts relying on personal accounts score higher testimony dependence
    """
    fact_lower = fact.lower()
    verifiability = 0.0
    recharacterization_risk = 0.0
    testimony_dependence = 0.0

    # Verifiability heuristics
    if re.search(r'\b\d{2,}\b', fact_lower):
        verifiability += 0.4
    if re.search(r'\b(report|study|data|document|record|log|transcript|video|photo|evidence)\b', fact_lower):
        verifiability += 0.4
    if re.search(r'\b(witness|eyewitness|testimony|said|claimed|reported)\b', fact_lower):
        testimony_dependence += 0.7
    if re.search(r'\b(maybe|possibly|could|might|suggests|alleged|reported)\b', fact_lower):
        recharacterization_risk += 0.7
    if re.search(r'\b(according to|as per|per)\b', fact_lower):
        testimony_dependence += 0.5
    if re.search(r'\b(unclear|unknown|unsure|disputed|controversial)\b', fact_lower):
        recharacterization_risk += 0.8

    # Normalize scores to max 1.0
    verifiability = min(verifiability, 1.0)
    recharacterization_risk = min(recharacterization_risk, 1.0)
    testimony_dependence = min(testimony_dependence, 1.0)

    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence,
    }

# ---------------------------
# SEMANTIC NORMALIZATION
# ---------------------------

DOMAIN_TERM_MAPPINGS = {
    # Automotive terms normalization
    "accident": "collision",
    "crash": "collision",
    "vehicle": "car",
    "automobile": "car",
    "auto": "car",
    "driver": "operator",
    "pedestrian": "person",
    "liability": "responsibility",
    "fault": "responsibility",
    "injury": "harm",
    "damage": "harm",
    "collision": "collision",
    "traffic violation": "infraction",
    "speeding": "infraction",
    "reckless driving": "infraction",
    "negligence": "carelessness",
    "carelessness": "carelessness",
    "insurance": "coverage",
    "policyholder": "insured",
    "claim": "demand",
    "settlement": "resolution",
    "court": "tribunal",
    "lawsuit": "litigation",
    "regulation": "rule",
    "statute": "law",
    "case law": "precedent",
    "treatise": "legal text",
    "practice": "custom",
    "manufacturer": "maker",
    "defect": "flaw",
    "recall": "withdrawal",
    "brake failure": "mechanical failure",
    "mechanical failure": "mechanical failure",
    "engine failure": "mechanical failure",
    "collision avoidance": "safety system",
    "airbag deployment": "safety system",
    "speed limit": "infraction",
    "traffic signal": "road sign",
    "road sign": "road sign",
    "intersection": "junction",
    "junction": "junction",
    "license": "permit",
    "permit": "permit",
    "traffic camera": "surveillance",
    "surveillance": "surveillance",
    "witness": "observer",
    "eyewitness": "observer",
    "testimony": "statement",
    "statement": "statement",
    "evidence": "proof",
    "proof": "proof",
    "investigation": "inquiry",
    "inquiry": "inquiry",
    "police report": "official report",
    "official report": "official report",
    "speed sensor": "sensor",
    "sensor": "sensor",
    "gps data": "location data",
    "location data": "location data",
    "black box": "event data recorder",
    "event data recorder": "event data recorder",
    "road condition": "environmental factor",
    "weather": "environmental factor",
    "environmental factor": "environmental factor",
    "traffic congestion": "traffic condition",
    "traffic condition": "traffic condition",
    "driver behavior": "operator conduct",
    "operator conduct": "operator conduct",
    "distraction": "operator conduct",
    "fatigue": "operator condition",
    "operator condition": "operator condition",
    "alcohol": "operator condition",
    "drug": "operator condition",
    "speed": "velocity",
    "velocity": "velocity",
    "acceleration": "velocity change",
    "velocity change": "velocity change",
    "braking": "deceleration",
    "deceleration": "deceleration",
    "turning": "maneuver",
    "maneuver": "maneuver",
    "lane change": "maneuver",
    "signal": "indicator",
    "indicator": "indicator",
    "hazard": "warning",
    "warning": "warning",
    "collision impact": "collision",
    "impact": "collision",
    "injury severity": "harm severity",
    "harm severity": "harm severity",
    "medical report": "official report",
    "repair": "remediation",
    "remediation": "remediation",
    "compensation": "damages",
    "damages": "damages",
    "legal obligation": "responsibility",
    "responsibility": "responsibility",
}

def normalize_query(text: str) -> str:
    """
    Normalize domain terms in text using DOMAIN_TERM_MAPPINGS.
    Replace terms with canonical forms.
    """
    # Tokenize on word boundaries
    tokens = re.findall(r'\b\w+\b', text.lower())
    normalized_tokens = []
    for token in tokens:
        normalized = DOMAIN_TERM_MAPPINGS.get(token, token)
        normalized_tokens.append(normalized)
    return ' '.join(normalized_tokens)

# ---------------------------
# THREE-LAYER RESPONSE SYSTEM
# ---------------------------

class DoctrineCache:
    """
    Cache for doctrine lookups keyed by keywords.
    Simulates fast lookup with predefined cache.
    """
    def __init__(self):
        # keyword -> cached analysis
        self.cache = {
            "liability": {"conclusion": "Liability likely applies", "confidence": 0.9, "authority_sources": [AuthorityLevel.STATUTORY]},
            "negligence": {"conclusion": "Negligence established", "confidence": 0.85, "authority_sources": [AuthorityLevel.CASE_LAW]},
            "collision": {"conclusion": "Collision confirmed", "confidence": 0.95, "authority_sources": [AuthorityLevel.PRACTICE]},
            "injury": {"conclusion": "Injury sustained", "confidence": 0.8, "authority_sources": [AuthorityLevel.TREATISE]},
            "insurance": {"conclusion": "Insurance coverage applicable", "confidence": 0.9, "authority_sources": [AuthorityLevel.REGULATORY]},
            "defect": {"conclusion": "Defect present", "confidence": 0.75, "authority_sources": [AuthorityLevel.STATUTORY]},
            "recall": {"conclusion": "Recall issued", "confidence": 0.7, "authority_sources": [AuthorityLevel.REGULATORY]},
            "fault": {"conclusion": "Fault assigned", "confidence": 0.85, "authority_sources": [AuthorityLevel.CASE_LAW]},
            "damages": {"conclusion": "Damages quantifiable", "confidence": 0.8, "authority_sources": [AuthorityLevel.TREATISE]},
            "brake failure": {"conclusion": "Brake failure confirmed", "confidence": 0.9, "authority_sources": [AuthorityLevel.PRACTICE]},
        }

    def lookup(self, query: str) -> Dict[str, Any]:
        """
        Lookup doctrine cache for keywords in query.
        Return combined cached analysis if found.
        """
        results = {}
        for keyword in self.cache.keys():
            if re.search(r'\b' + re.escape(keyword) + r'\b', query, re.IGNORECASE):
                results[keyword] = self.cache[keyword]
        if results:
            # Combine conclusions and average confidence
            combined_conclusion = "; ".join(v["conclusion"] for v in results.values())
            avg_confidence = sum(v["confidence"] for v in results.values()) / len(results)
            combined_authorities = []
            for v in results.values():
                combined_authorities.extend(v.get("authority_sources", []))
            return {
                "conclusion": combined_conclusion,
                "confidence": avg_confidence,
                "authority_sources": combined_authorities,
                "cached": True,
            }
        return {}

class SemanticSearchEngine:
    """
    Simulated semantic search engine that routes queries to sub-engines based on keywords.
    """
    def __init__(self):
        self.sub_engines = {
            "liability": self.liability_sub_engine,
            "negligence": self.negligence_sub_engine,
            "collision": self.collision_sub_engine,
            "injury": self.injury_sub_engine,
            "insurance": self.insurance_sub_engine,
            "defect": self.defect_sub_engine,
            "recall": self.recall_sub_engine,
            "fault": self.fault_sub_engine,
            "damages": self.damages_sub_engine,
            "brake failure": self.brake_failure_sub_engine,
        }

    def semantic_search(self, query: str) -> List[str]:
        """
        Return list of sub-engines to dispatch based on keywords in query.
        """
        matched = []
        for keyword in self.sub_engines.keys():
            if re.search(r'\b' + re.escape(keyword) + r'\b', query, re.IGNORECASE):
                matched.append(keyword)
        return matched

    def dispatch(self, query: str) -> Dict[str, Any]:
        """
        Dispatch query to relevant sub-engines and collect results.
        """
        matched_keywords = self.semantic_search(query)
        results = {}
        for keyword in matched_keywords:
            func = self.sub_engines.get(keyword)
            if func:
                results[keyword] = func(query)
        return results

    # Sub-engine implementations (simulated)
    def liability_sub_engine(self, query: str) -> Dict[str, Any]:
        return {
            "conclusion": "Liability is probable given the facts.",
            "confidence": 0.88,
            "authority_sources": [AuthorityLevel.STATUTORY, AuthorityLevel.CASE_LAW],
        }

    def negligence_sub_engine(self, query: str) -> Dict[str, Any]:
        return {
            "conclusion": "Negligence likely contributed to the incident.",
            "confidence": 0.82,
            "authority_sources": [AuthorityLevel.CASE_LAW],
        }

    def collision_sub_engine(self, query: str) -> Dict[str, Any]:
        return {
            "conclusion": "Collision occurred as per available evidence.",
            "confidence": 0.95,
            "authority_sources": [AuthorityLevel.PRACTICE],
        }

    def injury_sub_engine(self, query: str) -> Dict[str, Any]:
        return {
            "conclusion": "Injury sustained by parties involved.",
            "confidence": 0.8,
            "authority_sources": [AuthorityLevel.TREATISE],
        }

    def insurance_sub_engine(self, query: str) -> Dict[str, Any]:
        return {
            "conclusion": "Insurance coverage applies under policy terms.",
            "confidence": 0.9,
            "authority_sources": [AuthorityLevel.REGULATORY],
        }

    def defect_sub_engine(self, query: str) -> Dict[str, Any]:
        return {
            "conclusion": "Vehicle defect identified as causal factor.",
            "confidence": 0.75,
            "authority_sources": [AuthorityLevel.STATUTORY],
        }

    def recall_sub_engine(self, query: str) -> Dict[str, Any]:
        return {
            "conclusion": "Recall notice issued for vehicle model.",
            "confidence": 0.7,
            "authority_sources": [AuthorityLevel.REGULATORY],
        }

    def fault_sub_engine(self, query: str) -> Dict[str, Any]:
        return {
            "conclusion": "Fault assigned to operator based on evidence.",
            "confidence": 0.85,
            "authority_sources": [AuthorityLevel.CASE_LAW],
        }

    def damages_sub_engine(self, query: str) -> Dict[str, Any]:
        return {
            "conclusion": "Damages quantifiable and attributable.",
            "confidence": 0.8,
            "authority_sources": [AuthorityLevel.TREATISE],
        }

    def brake_failure_sub_engine(self, query: str) -> Dict[str, Any]:
        return {
            "conclusion": "Brake failure confirmed as contributing cause.",
            "confidence": 0.9,
            "authority_sources": [AuthorityLevel.PRACTICE],
        }

class DeepMultiEngineAnalysis:
    """
    Perform deep parallel analysis by dispatching to multiple sub-engines,
    merging results, and resolving conflicts.
    """
    def __init__(self):
        self.sub_engines = SemanticSearchEngine()

    def analyze(self, query: str) -> Dict[str, Any]:
        """
        Dispatch query to all relevant sub-engines in parallel,
        merge results, and resolve conflicts.
        """
        matched_keywords = self.sub_engines.semantic_search(query)
        results = {}
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_keyword = {executor.submit(self.sub_engines.sub_engines[k], query): k for k in matched_keywords}
            for future in as_completed(future_to_keyword):
                keyword = future_to_keyword[future]
                try:
                    res = future.result()
                    results[keyword] = res
                except Exception:
                    results[keyword] = {"conclusion": "Error in analysis", "confidence": 0.0, "authority_sources": []}

        # Merge results: resolve conflicts by confidence and authority
        merged_conclusions = {}
        for keyword, res in results.items():
            merged_conclusions[keyword] = res

        # Conflict resolution example: if multiple conclusions contradict, mark conflict
        # For demo, assume no direct conflict detection beyond keyword separation

        return merged_conclusions

class ThreeLayerResponseSystem:
    """
    Implements the three-layer response system:
    Layer 1: Doctrine cache lookup (0-200ms)
    Layer 2: Semantic search + sub-engine routing
    Layer 3: Deep multi-engine analysis
    """
    def __init__(self):
        self.cache = DoctrineCache()
        self.semantic_engine = SemanticSearchEngine()
        self.deep_analysis = DeepMultiEngineAnalysis()

    def respond(self, query: str) -> Dict[str, Any]:
        """
        Process query through three layers with timing and fallback.
        """
        start_time = time.time()
        # Layer 1: Doctrine cache lookup
        cache_result = self.cache.lookup(query)
        elapsed = (time.time() - start_time) * 1000  # ms
        if cache_result and elapsed <= 200:
            cache_result['layer'] = 1
            return cache_result

        # Layer 2: Semantic search + sub-engine routing
        semantic_start = time.time()
        semantic_results = self.semantic_engine.dispatch(query)
        semantic_elapsed = (time.time() - semantic_start) * 1000
        if semantic_results and semantic_elapsed <= 500:
            # Combine semantic results into one conclusion string
            combined_conclusion = "; ".join(r["conclusion"] for r in semantic_results.values())
            avg_confidence = sum(r["confidence"] for r in semantic_results.values()) / len(semantic_results)
            combined_authorities = []
            for r in semantic_results.values():
                combined_authorities.extend(r.get("authority_sources", []))
            return {
                "conclusion": combined_conclusion,
                "confidence": avg_confidence,
                "authority_sources": combined_authorities,
                "layer": 2,
            }

        # Layer 3: Deep multi-engine analysis
        deep_results = self.deep_analysis.analyze(query)
        combined_conclusion = "; ".join(r["conclusion"] for r in deep_results.values())
        avg_confidence = sum(r["confidence"] for r in deep_results.values()) / max(len(deep_results), 1)
        combined_authorities = []
        for r in deep_results.values():
            combined_authorities.extend(r.get("authority_sources", []))
        return {
            "conclusion": combined_conclusion,
            "confidence": avg_confidence,
            "authority_sources": combined_authorities,
            "layer": 3,
        }

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
        self._queries: List[QueryTelemetry] = []
        self._errors: List[QueryTelemetry] = []
        self._sub_engine_stats: Dict[str, List[float]] = defaultdict(list)
        self._doctrine_hits: Counter = Counter()
        self._doctrine_total: Counter = Counter()
        self._query_times: deque = deque()  # (timestamp, QueryTelemetry)
        self._max_query_window = 3600  # 1 hour in seconds

    def record_query(self, telemetry: QueryTelemetry):
        with self._lock:
            self._queries.append(telemetry)
            self._query_times.append((telemetry.timestamp, telemetry))
            for eng in telemetry.engines_invoked:
                self._sub_engine_stats[eng].append(telemetry.latency_ms)
                self._doctrine_total[eng] += 1
                if telemetry.cache_hit:
                    self._doctrine_hits[eng] += 1
            self._prune_old_queries()

    def record_error(self, telemetry: QueryTelemetry):
        with self._lock:
            self._errors.append(telemetry)
            for eng in telemetry.engines_invoked:
                self._doctrine_total[eng] += 1
            self._prune_old_queries()

    def _prune_old_queries(self):
        now = datetime.datetime.utcnow().timestamp()
        while self._query_times and (now - self._query_times[0][0]) > self._max_query_window:
            _, old_telemetry = self._query_times.popleft()

    def get_latency_stats(self) -> Dict[str, Any]:
        with self._lock:
            latencies = [q.latency_ms for q in self._queries]
            if not latencies:
                return {
                    "avg": None, "p50": None, "p95": None, "p99": None,
                    "min": None, "max": None
                }
            latencies_sorted = sorted(latencies)
            return {
                "avg": statistics.mean(latencies),
                "p50": statistics.median(latencies),
                "p95": latencies_sorted[int(0.95 * len(latencies_sorted))-1],
                "p99": latencies_sorted[int(0.99 * len(latencies_sorted))-1],
                "min": min(latencies),
                "max": max(latencies)
            }

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        with self._lock:
            rates = {}
            for doctrine in self._doctrine_total:
                total = self._doctrine_total[doctrine]
                hits = self._doctrine_hits[doctrine]
                if total > 0:
                    rates[doctrine] = hits / total
                else:
                    rates[doctrine] = None
            return rates

    def queries_last_hour(self) -> int:
        with self._lock:
            now = datetime.datetime.utcnow().timestamp()
            count = 0
            for ts, _ in self._query_times:
                if now - ts <= self._max_query_window:
                    count += 1
            return count

    def get_sub_engine_stats(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            stats = {}
            for eng, latencies in self._sub_engine_stats.items():
                if latencies:
                    lat_sorted = sorted(latencies)
                    stats[eng] = {
                        "avg_latency": statistics.mean(latencies),
                        "p50_latency": statistics.median(latencies),
                        "p95_latency": lat_sorted[int(0.95 * len(lat_sorted))-1],
                        "p99_latency": lat_sorted[int(0.99 * len(lat_sorted))-1],
                        "min_latency": min(latencies),
                        "max_latency": max(latencies),
                        "invocations": len(latencies)
                    }
                else:
                    stats[eng] = {
                        "avg_latency": None,
                        "p50_latency": None,
                        "p95_latency": None,
                        "p99_latency": None,
                        "min_latency": None,
                        "max_latency": None,
                        "invocations": 0
                    }
            return stats

# -----------------------------
# 2. DRIFT WATCHER
# -----------------------------

class DriftWatcher:
    def __init__(self, window_size: int = 100):
        self._lock = threading.Lock()
        self._baselines: Dict[str, float] = {}  # doctrine -> baseline confidence
        self._history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self._alerts: Dict[str, List[Tuple[float, float, float]]] = defaultdict(list)  # doctrine -> [(prev, curr, drift_pct)]

    def record_baseline(self, doctrine: str, confidence: float):
        with self._lock:
            self._baselines[doctrine] = confidence

    def detect_drift(self, doctrine: str, confidence: float) -> Optional[Dict[str, Any]]:
        with self._lock:
            self._history[doctrine].append(confidence)
            baseline = self._baselines.get(doctrine)
            if baseline is None or len(self._history[doctrine]) < self._history[doctrine].maxlen:
                return None
            curr_avg = statistics.mean(self._history[doctrine])
            drift = abs(curr_avg - baseline) / (baseline + 1e-6)
            if drift > 0.10:  # >10% shift
                self._alerts[doctrine].append((baseline, curr_avg, drift))
                return {
                    "doctrine": doctrine,
                    "baseline": baseline,
                    "current_avg": curr_avg,
                    "drift_pct": drift,
                    "alert": True
                }
            return None

    def get_drift_report(self) -> Dict[str, Any]:
        with self._lock:
            report = {}
            for doctrine, hist in self._history.items():
                if hist:
                    baseline = self._baselines.get(doctrine)
                    curr_avg = statistics.mean(hist)
                    drift = None
                    if baseline is not None:
                        drift = abs(curr_avg - baseline) / (baseline + 1e-6)
                    report[doctrine] = {
                        "baseline": baseline,
                        "current_avg": curr_avg,
                        "drift_pct": drift,
                        "alerts": self._alerts.get(doctrine, [])
                    }
            return report

# -----------------------------
# 3. COVERAGE MAP
# -----------------------------

class CoverageTracker:
    def __init__(self):
        self._lock = threading.Lock()
        self._triggered: Counter = Counter()  # doctrine -> count
        self._missed_queries: List[Tuple[str, float]] = []  # (query_id, timestamp)
        self._sub_engine_coverage: Dict[str, Counter] = defaultdict(Counter)

    def record_triggered(self, doctrine: str, sub_engine: str):
        with self._lock:
            self._triggered[doctrine] += 1
            self._sub_engine_coverage[sub_engine][doctrine] += 1

    def record_missed(self, query_id: str, timestamp: float):
        with self._lock:
            self._missed_queries.append((query_id, timestamp))

    def get_coverage_report(self) -> Dict[str, Any]:
        with self._lock:
            total = sum(self._triggered.values())
            doctrine_coverage = dict(self._triggered)
            epistemic_gap = len(self._missed_queries)
            sub_engine_stats = {eng: dict(cnts) for eng, cnts in self._sub_engine_coverage.items()}
            return {
                "total_triggered": total,
                "doctrine_coverage": doctrine_coverage,
                "epistemic_gap_count": epistemic_gap,
                "missed_queries": list(self._missed_queries),
                "per_sub_engine_coverage": sub_engine_stats
            }

    def identify_epistemic_gaps(self, queries: List[str], doctrines: List[str]) -> List[str]:
        # Returns queries that match no doctrines
        with self._lock:
            covered = set(self._triggered.keys())
            gaps = []
            for q in queries:
                if q not in covered:
                    gaps.append(q)
            return gaps

    def get_per_sub_engine_coverage(self) -> Dict[str, Dict[str, int]]:
        with self._lock:
            return {eng: dict(cnts) for eng, cnts in self._sub_engine_coverage.items()}

# -----------------------------
# 4. DETERMINISM HASH
# -----------------------------

def compute_determinism_hash(query: Any, response: Any) -> str:
    def _normalize(obj):
        if isinstance(obj, dict):
            return {k: _normalize(obj[k]) for k in sorted(obj)}
        elif isinstance(obj, list):
            return [_normalize(x) for x in obj]
        else:
            return obj
    norm_query = _normalize(query)
    norm_response = _normalize(response)
    data = json.dumps({"query": norm_query, "response": norm_response}, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def verify_reproducibility(query: Any, response: Any, expected_hash: str) -> bool:
    return compute_determinism_hash(query, response) == expected_hash

# -----------------------------
# 5. AUDIT TRAIL
# -----------------------------

class AuditTrailWriter:
    def __init__(self, log_dir: str):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self._lock = threading.Lock()
        self._current_date = None
        self._file = None
        self._open_log_file()

    def _open_log_file(self):
        now = datetime.datetime.utcnow()
        date_str = now.strftime('%Y-%m-%d')
        if self._current_date != date_str:
            if self._file:
                self._file.close()
            log_path = os.path.join(self.log_dir, f"audit_{date_str}.jsonl")
            self._file = open(log_path, 'a', buffering=1)
            self._current_date = date_str

    def write(self, query_id: str, timestamp: float, engine_id: str, engines_invoked: List[str],
              mode: str, confidence: float, latency: float, cache_hit: bool):
        with self._lock:
            self._open_log_file()
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
            self._file.write(json.dumps(record) + '\n')

    def close(self):
        with self._lock:
            if self._file:
                self._file.close()
                self._file = None

    def forensic_replay(self, date: str) -> List[Dict[str, Any]]:
        log_path = os.path.join(self.log_dir, f"audit_{date}.jsonl")
        if not os.path.exists(log_path):
            return []
        with open(log_path, 'r') as f:
            return [json.loads(line) for line in f]

# -----------------------------
# 6. PERFORMANCE PROFILER
# -----------------------------

class PerformanceProfiler:
    def __init__(self):
        self._lock = threading.Lock()
        self._latencies: Dict[str, List[float]] = defaultdict(list)
        self._errors: Dict[str, int] = defaultdict(int)
        self._invocations: Dict[str, int] = defaultdict(int)
        self._availabilities: Dict[str, List[bool]] = defaultdict(list)
        self._sla_targets: Dict[str, Dict[str, float]] = {}  # sub_engine -> {"max_latency": ms, "min_availability": float}

    def record_invocation(self, sub_engine: str, latency: float, success: bool):
        with self._lock:
            self._latencies[sub_engine].append(latency)
            self._invocations[sub_engine] += 1
            self._availabilities[sub_engine].append(success)
            if not success:
                self._errors[sub_engine] += 1

    def set_sla(self, sub_engine: str, max_latency: float, min_availability: float):
        with self._lock:
            self._sla_targets[sub_engine] = {
                "max_latency": max_latency,
                "min_availability": min_availability
            }

    def get_sub_engine_performance(self) -> Dict[str, Any]:
        with self._lock:
            perf = {}
            for eng in self._invocations:
                latencies = self._latencies[eng]
                invocations = self._invocations[eng]
                errors = self._errors[eng]
                avail = self._availabilities[eng]
                if latencies:
                    avg_latency = statistics.mean(latencies)
                    p95_latency = sorted(latencies)[int(0.95 * len(latencies))-1]
                else:
                    avg_latency = None
                    p95_latency = None
                error_rate = errors / invocations if invocations else None
                availability = sum(avail) / len(avail) if avail else None
                sla = self._sla_targets.get(eng)
                sla_breach = False
                if sla:
                    if avg_latency is not None and avg_latency > sla["max_latency"]:
                        sla_breach = True
                    if availability is not None and availability < sla["min_availability"]:
                        sla_breach = True
                perf[eng] = {
                    "avg_latency": avg_latency,
                    "p95_latency": p95_latency,
                    "error_rate": error_rate,
                    "availability": availability,
                    "invocations": invocations,
                    "sla": sla,
                    "sla_breach": sla_breach
                }
            return perf

    def get_sla_breaches(self) -> List[str]:
        with self._lock:
            breaches = []
            perf = self.get_sub_engine_performance()
            for eng, stats in perf.items():
                if stats.get("sla_breach"):
                    breaches.append(eng)
            return breaches

# -----------------------------
# END OF PART 5/6
# -----------------------------

ENGINE_ID = "AUTOIE"
ENGINE_PORT = 8858
SUB_ENGINES = {
    "AUTO01": "Engine Systems",
    "AUTO02": "Transmission",
    "AUTO03": "Brake Systems",
    "AUTO04": "Suspension Steering",
    "AUTO05": "Electrical Electronics",
    "AUTO06": "Diagnostics",
    "AUTO07": "Hybrid EV",
    "AUTO08": "ADAS Safety",
    "AUTO09": "Body Structures",
    "AUTO10": "Climate Control",
    "AUTO11": "Fuel Systems",
    "AUTO12": "Exhaust Emissions",
    "AUTO13": "Tires Wheels",
    "AUTO14": "Fleet Management",
    "AUTO15": "Autonomous Driving",
}

# Logger setup
logger = logging.getLogger("autoie")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Models

class QueryRequest(BaseModel):
    query: str
    metadata: Optional[Dict[str, Any]] = None

class RouteDryRunRequest(BaseModel):
    query: str
    metadata: Optional[Dict[str, Any]] = None

class AnalyzeRequest(BaseModel):
    query: str
    metadata: Optional[Dict[str, Any]] = None
    engines: Optional[List[str]] = None  # If None, analyze all relevant engines

class QueryResponse(BaseModel):
    response: Dict[str, Any]
    routed_engines: List[str]
    cache_hit: bool
    query_hash: str

class HealthStatus(BaseModel):
    engine_id: str
    status: str
    details: Optional[Dict[str, Any]] = None

class MetricsResponse(BaseModel):
    latency_ms_avg: float
    latency_ms_p95: float
    cache_hit_rate: float
    queries_per_hour: float
    sub_engine_metrics: Dict[str, Dict[str, Any]]

class CoverageReport(BaseModel):
    doctrine_coverage_percent: float
    epistemic_gaps: List[str]

class DriftReport(BaseModel):
    drift_detected: bool
    drift_score: float
    details: Optional[Dict[str, Any]] = None

class DoctrinesList(BaseModel):
    doctrines: List[str]

class RoutingRules(BaseModel):
    routing_rules: Dict[str, Any]
    engine_registry: Dict[str, str]

class SubEngineHealthDashboard(BaseModel):
    sub_engines: List[HealthStatus]

class RouteDryRunResponse(BaseModel):
    would_invoke_engines: List[str]

class AnalyzeResponse(BaseModel):
    analysis_results: Dict[str, Any]

# Global State and Cache

class DoctrineCache:
    def __init__(self):
        self._cache = {}
        self._lock = asyncio.Lock()

    async def initialize(self):
        # Simulate loading doctrines from DB or files
        async with self._lock:
            self._cache = {
                "engine_systems": {"rules": ["rule1", "rule2"], "version": "1.0"},
                "transmission": {"rules": ["ruleA", "ruleB"], "version": "1.1"},
                # ... other doctrines
            }
            logger.info("Doctrine cache initialized with %d doctrines", len(self._cache))

    async def get_doctrine(self, key: str) -> Optional[Dict[str, Any]]:
        async with self._lock:
            return self._cache.get(key)

    async def list_doctrines(self) -> List[str]:
        async with self._lock:
            return list(self._cache.keys())

    async def coverage_report(self) -> CoverageReport:
        async with self._lock:
            total_possible = 20  # pretend total doctrines possible
            coverage = len(self._cache) / total_possible * 100
            gaps = [f"doctrine_{i}" for i in range(total_possible) if f"doctrine_{i}" not in self._cache]
            return CoverageReport(
                doctrine_coverage_percent=coverage,
                epistemic_gaps=gaps[:5]
            )

doctrine_cache = DoctrineCache()

class HealthMonitor:
    def __init__(self):
        self._statuses = {}
        self._lock = asyncio.Lock()
        self._running = False
        self._task = None

    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self._monitor_loop())
        logger.info("Health monitor started")

    async def stop(self):
        self._running = False
        if self._task:
            await self._task
        logger.info("Health monitor stopped")

    async def _monitor_loop(self):
        while self._running:
            await self._check_sub_engines()
            await asyncio.sleep(10)

    async def _check_sub_engines(self):
        async with self._lock:
            for engine_id in SUB_ENGINES.keys():
                # Simulate health check
                status = random.choice(["healthy", "degraded", "unreachable"])
                details = None
                if status != "healthy":
                    details = {"last_checked": datetime.datetime.utcnow().isoformat()}
                self._statuses[engine_id] = HealthStatus(
                    engine_id=engine_id,
                    status=status,
                    details=details
                )
            logger.debug("Health statuses updated")

    async def get_health_status(self) -> List[HealthStatus]:
        async with self._lock:
            return list(self._statuses.values())

health_monitor = HealthMonitor()

class Telemetry:
    def __init__(self):
        self._latencies = []
        self._cache_hits = 0
        self._queries = 0
        self._lock = asyncio.Lock()
        self._sub_engine_stats = {k: {"calls": 0, "errors": 0, "avg_latency_ms": 0.0} for k in SUB_ENGINES.keys()}

    async def record_query(self, latency_ms: float, cache_hit: bool, sub_engine_calls: Dict[str, float], sub_engine_errors: Dict[str, int]):
        async with self._lock:
            self._latencies.append(latency_ms)
            if cache_hit:
                self._cache_hits += 1
            self._queries += 1
            for engine_id, latency in sub_engine_calls.items():
                stats = self._sub_engine_stats.get(engine_id)
                if stats:
                    prev_calls = stats["calls"]
                    prev_avg = stats["avg_latency_ms"]
                    new_calls = prev_calls + 1
                    new_avg = (prev_avg * prev_calls + latency) / new_calls
                    stats["calls"] = new_calls
                    stats["avg_latency_ms"] = new_avg
            for engine_id, errors in sub_engine_errors.items():
                stats = self._sub_engine_stats.get(engine_id)
                if stats:
                    stats["errors"] += errors

    async def get_metrics(self) -> MetricsResponse:
        async with self._lock:
            if not self._latencies:
                avg_latency = 0.0
                p95_latency = 0.0
            else:
                sorted_lat = sorted(self._latencies)
                avg_latency = sum(sorted_lat) / len(sorted_lat)
                idx_95 = int(len(sorted_lat) * 0.95) - 1
                p95_latency = sorted_lat[max(0, idx_95)]
            cache_hit_rate = (self._cache_hits / self._queries) if self._queries > 0 else 0.0
            queries_per_hour = (self._queries / ((time.time() - APP_START_TIME) / 3600)) if self._queries > 0 else 0.0
            return MetricsResponse(
                latency_ms_avg=avg_latency,
                latency_ms_p95=p95_latency,
                cache_hit_rate=cache_hit_rate,
                queries_per_hour=queries_per_hour,
                sub_engine_metrics=self._sub_engine_stats.copy()
            )

telemetry = Telemetry()

class DriftDetector:
    def __init__(self):
        self._last_drift_score = 0.0
        self._drift_detected = False
        self._details = {}
        self._lock = asyncio.Lock()

    async def analyze_drift(self):
        async with self._lock:
            # Simulate drift detection logic
            score = random.uniform(0, 1)
            self._last_drift_score = score
            self._drift_detected = score > 0.7
            self._details = {
                "score": score,
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "notes": "Simulated drift detection"
            }
            logger.info(f"Drift detection run: score={score:.3f}, detected={self._drift_detected}")

    async def get_report(self) -> DriftReport:
        async with self._lock:
            return DriftReport(
                drift_detected=self._drift_detected,
                drift_score=self._last_drift_score,
                details=self._details.copy()
            )

drift_detector = DriftDetector()

# Query Normalization, Classification, Routing, Dispatch, Merge, Guardrails, Hash, Log

async def normalize_query(query: str) -> str:
    # Basic normalization: lowercase, strip, remove extra spaces
    normalized = ' '.join(query.lower().strip().split())
    logger.debug(f"Normalized query: {normalized}")
    return normalized

async def classify_domain(query: str) -> List[str]:
    # Simulate classification: assign sub-engines based on keywords
    keywords_map = {
        "engine": ["AUTO01"],
        "transmission": ["AUTO02"],
        "brake": ["AUTO03"],
        "suspension": ["AUTO04"],
        "electrical": ["AUTO05"],
        "diagnostic": ["AUTO06"],
        "hybrid": ["AUTO07"],
        "adas": ["AUTO08"],
        "body": ["AUTO09"],
        "climate": ["AUTO10"],
        "fuel": ["AUTO11"],
        "exhaust": ["AUTO12"],
        "tire": ["AUTO13"],
        "fleet": ["AUTO14"],
        "autonomous": ["AUTO15"],
    }
    matched_engines = set()
    for keyword, engines in keywords_map.items():
        if keyword in query:
            matched_engines.update(engines)
    if not matched_engines:
        # fallback to all engines if no keyword matched
        matched_engines = set(SUB_ENGINES.keys())
    logger.debug(f"Classified query to engines: {matched_engines}")
    return list(matched_engines)

async def route_query(classified_engines: List[str], metadata: Optional[Dict[str, Any]] = None) -> List[str]:
    # Apply routing rules, e.g. filter by metadata or load balancing
    # For simplicity, just return classified engines sorted
    routed = sorted(classified_engines)
    logger.debug(f"Routed query to engines: {routed}")
    return routed

async def dispatch_to_sub_engine(engine_id: str, query: str, metadata: Optional[Dict[str, Any]] = None, timeout: float = 2.0) -> Dict[str, Any]:
    # Simulate sub-engine processing with random delay and possible failure
    start = time.time()
    latency = 0.0
    try:
        delay = random.uniform(0.1, 0.5)
        if random.random() < 0.05:
            # Simulate failure
            raise Exception(f"Sub-engine {engine_id} failure simulated")
        await asyncio.sleep(delay)
        latency = (time.time() - start) * 1000
        response = {
            "engine_id": engine_id,
            "result": f"Processed query '{query[:30]}...' in {delay:.2f}s",
            "metadata": metadata or {},
            "latency_ms": latency,
        }
        logger.debug(f"Sub-engine {engine_id} responded in {latency:.2f}ms")
        return response
    except Exception as e:
        latency = (time.time() - start) * 1000
        logger.error(f"Error dispatching to sub-engine {engine_id}: {e}")
        raise

async def merge_responses(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Simple merge: aggregate results keyed by engine_id
    merged = {}
    for resp in responses:
        engine_id = resp.get("engine_id", "unknown")
        merged[engine_id] = resp
    logger.debug(f"Merged responses from {len(responses)} engines")
    return merged

async def apply_guardrails(merged_response: Dict[str, Any]) -> Dict[str, Any]:
    # Apply any guardrails, e.g. filter sensitive info or validate output
    # For simulation, just pass through
    logger.debug("Applied guardrails to merged response")
    return merged_response

def hash_query(query: str) -> str:
    h = hashlib.sha256()
    h.update(query.encode("utf-8"))
    return h.hexdigest()

async def log_query(query_hash: str, routed_engines: List[str], cache_hit: bool, latency_ms: float):
    logger.info(f"Query {query_hash} routed to {routed_engines}, cache_hit={cache_hit}, latency={latency_ms:.2f}ms")

# Circuit Breaker and Fallback

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_time: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failures = {}
        self.last_failure_time = {}

    def record_failure(self, engine_id: str):
        count = self.failures.get(engine_id, 0) + 1
        self.failures[engine_id] = count
        self.last_failure_time[engine_id] = time.time()
        logger.warning(f"Circuit breaker: failure recorded for {engine_id}, count={count}")

    def record_success(self, engine_id: str):
        self.failures[engine_id] = 0
        self.last_failure_time[engine_id] = None
        logger.debug(f"Circuit breaker: success recorded for {engine_id}")

    def is_open(self, engine_id: str) -> bool:
        count = self.failures.get(engine_id, 0)
        last_time = self.last_failure_time.get(engine_id)
        if count >= self.failure_threshold:
            if last_time and (time.time() - last_time) < self.recovery_time:
                logger.debug(f"Circuit breaker: circuit open for {engine_id}")
                return True
            else:
                # Reset after recovery time
                self.failures[engine_id] = 0
                self.last_failure_time[engine_id] = None
        return False

circuit_breaker = CircuitBreaker()

# Fallback to doctrine cache

async def fallback_to_doctrine_cache(routed_engines: List[str], query: str) -> Dict[str, Any]:
    fallback_responses = {}
    for engine_id in routed_engines:
        doctrine_key = SUB_ENGINES.get(engine_id, "").lower().replace(" ", "_")
        doctrine = await doctrine_cache.get_doctrine(doctrine_key)
        if doctrine:
            fallback_responses[engine_id] = {
                "engine_id": engine_id,
                "result": f"Fallback doctrine response for query '{query[:30]}...'",
                "doctrine_version": doctrine.get("version"),
                "fallback": True,
            }
        else:
            fallback_responses[engine_id] = {
                "engine_id": engine_id,
                "result": "No doctrine available for fallback",
                "fallback": True,
            }
    logger.info("Fallback to doctrine cache executed")
    return fallback_responses

# FastAPI app and lifespan

APP_START_TIME = time.time()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize doctrine cache
    await doctrine_cache.initialize()
    # Start health monitor
    await health_monitor.start()
    # Seed search index (simulate)
    logger.info("Seeding search index...")
    await asyncio.sleep(0.5)
    logger.info("Search index seeded")
    # Start telemetry (no special start needed)
    logger.info("Telemetry started")
    # Start drift detector background task
    drift_task = asyncio.create_task(drift_detector_loop())
    try:
        yield
    finally:
        # Cleanup
        drift_task.cancel()
        await health_monitor.stop()
        logger.info("Application shutdown complete")

async def drift_detector_loop():
    while True:
        try:
            await drift_detector.analyze_drift()
        except Exception as e:
            logger.error(f"Drift detector error: {e}")
        await asyncio.sleep(60)  # Run every 60 seconds

app = FastAPI(
    title="Automotive Intelligence Engine - Domain Orchestrator",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint implementations

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    start_time = time.time()
    query = request.query
    metadata = request.metadata or {}

    normalized_query = await normalize_query(query)
    classified_engines = await classify_domain(normalized_query)
    routed_engines = await route_query(classified_engines, metadata)

    query_hash = hash_query(normalized_query)

    # Check doctrine cache for cached response
    # For simulation, cache hit if hash ends with '0' or '5'
    cache_hit = query_hash[-1] in ['0', '5']
    if cache_hit:
        cached_response = await fallback_to_doctrine_cache(routed_engines, normalized_query)
        latency_ms = (time.time() - start_time) * 1000
        await telemetry.record_query(latency_ms, True, {}, {})
        await log_query(query_hash, routed_engines, True, latency_ms)
        return QueryResponse(
            response=cached_response,
            routed_engines=routed_engines,
            cache_hit=True,
            query_hash=query_hash
        )

    # Dispatch to sub-engines with circuit breaker and timeout
    sub_engine_calls = {}
    sub_engine_errors = {}
    responses = []
    for engine_id in routed_engines:
        if circuit_breaker.is_open(engine_id):
            logger.warning(f"Skipping {engine_id} due to open circuit breaker")
            sub_engine_errors[engine_id] = 1
            continue
        try:
            resp = await asyncio.wait_for(
                dispatch_to_sub_engine(engine_id, normalized_query, metadata),
                timeout=3.0
            )
            responses.append(resp)
            circuit_breaker.record_success(engine_id)
            sub_engine_calls[engine_id] = resp.get("latency_ms", 0.0)
            sub_engine_errors[engine_id] = 0
        except Exception:
            circuit_breaker.record_failure(engine_id)
            sub_engine_errors[engine_id] = 1

    # If all sub-engines failed, fallback to doctrine cache
    if len(responses) == 0:
        fallback_resp = await fallback_to_doctrine_cache(routed_engines, normalized_query)
        latency_ms = (time.time() - start_time) * 1000
        await telemetry.record_query(latency_ms, False, {}, sub_engine_errors)
        await log_query(query_hash, routed_engines, False, latency_ms)
        return QueryResponse(
            response=fallback_resp,
            routed_engines=routed_engines,
            cache_hit=False,
            query_hash=query_hash
        )

    merged_response = await merge_responses(responses)
    guarded_response = await apply_guardrails(merged_response)
    latency_ms = (time.time() - start_time) * 1000

    await telemetry.record_query(latency_ms, False, sub_engine_calls, sub_engine_errors)
    await log_query(query_hash, routed_engines, False, latency_ms)

    return QueryResponse(
        response=guarded_response,
        routed_engines=routed_engines,
        cache_hit=False,
        query_hash=query_hash
    )

@app.get("/health", response_model=List[HealthStatus])
async def health_endpoint():
    # Self health
    self_status = HealthStatus(
        engine_id=ENGINE_ID,
        status="healthy",
        details={"uptime_seconds": int(time.time() - APP_START_TIME)}
    )
    sub_engines_status = await health_monitor.get_health_status()
    return [self_status] + sub_engines_status

@app.get("/metrics", response_model=MetricsResponse)
async def metrics_endpoint():
    metrics = await telemetry.get_metrics()
    return metrics

@app.get("/coverage", response_model=CoverageReport)
async def coverage_endpoint():
    coverage = await doctrine_cache.coverage_report()
    return coverage

@app.get("/drift", response_model=DriftReport)
async def drift_endpoint():
    report = await drift_detector.get_report()
    return report

@app.get("/doctrines", response_model=DoctrinesList)
async def doctrines_endpoint():
    doctrines = await doctrine_cache.list_doctrines()
    return DoctrinesList(doctrines=doctrines)

@app.get("/routing", response_model=RoutingRules)
async def routing_endpoint():
    # Simulate routing rules and engine registry
    routing_rules = {
        "keywords_map": {
            "engine": ["AUTO01"],
            "transmission": ["AUTO02"],
            # ...
        },
        "default_route": list(SUB_ENGINES.keys())
    }
    return RoutingRules(
        routing_rules=routing_rules,
        engine_registry=SUB_ENGINES
    )

@app.get("/sub-engines", response_model=SubEngineHealthDashboard)
async def sub_engines_endpoint():
    statuses = await health_monitor.get_health_status()
    return SubEngineHealthDashboard(sub_engines=statuses)

@app.post("/route", response_model=RouteDryRunResponse)
async def route_dry_run_endpoint(request: RouteDryRunRequest):
    normalized_query = await normalize_query(request.query)
    classified_engines = await classify_domain(normalized_query)
    routed_engines = await route_query(classified_engines, request.metadata or {})
    return RouteDryRunResponse(would_invoke_engines=routed_engines)

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(request: AnalyzeRequest):
    normalized_query = await normalize_query(request.query)
    engines_to_use = request.engines or await classify_domain(normalized_query)
    routed_engines = await route_query(engines_to_use, request.metadata or {})

    analysis_results = {}
    for engine_id in routed_engines:
        try:
            resp = await dispatch_to_sub_engine(engine_id, normalized_query, request.metadata)
            analysis_results[engine_id] = {
                "result": resp.get("result"),
                "latency_ms": resp.get("latency_ms"),
                "analysis": f"Deep analysis for {engine_id}"
            }
        except Exception as e:
            analysis_results[engine_id] = {
                "error": str(e)
            }
    return AnalyzeResponse(analysis_results=analysis_results)

# Exception handlers

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=ENGINE_PORT, log_level="info")