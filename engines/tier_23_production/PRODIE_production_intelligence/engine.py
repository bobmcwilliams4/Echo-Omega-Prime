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

# Engine Constants
ENGINE_ID = "PRODIE"
ENGINE_PORT = 8854
ENGINE_NAME = "Production Intelligence Engine — Domain Orchestrator"
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
    PRODUCTION_OPTIMIZATION = "PRODUCTION_OPTIMIZATION"
    ARTIFICIAL_LIFT = "ARTIFICIAL_LIFT"
    WELL_TESTING = "WELL_TESTING"
    PRODUCTION_ALLOCATION = "PRODUCTION_ALLOCATION"
    DECLINE_CURVE_ANALYSIS = "DECLINE_CURVE_ANALYSIS"
    RESERVOIR_MANAGEMENT = "RESERVOIR_MANAGEMENT"
    PRODUCED_WATER = "PRODUCED_WATER"
    GAS_PROCESSING = "GAS_PROCESSING"
    PIPELINE_OPERATIONS = "PIPELINE_OPERATIONS"
    TANK_BATTERY = "TANK_BATTERY"
    SCADA_SYSTEMS = "SCADA_SYSTEMS"
    CHEMICAL_TREATMENT = "CHEMICAL_TREATMENT"
    SAND_CONTROL = "SAND_CONTROL"
    SCALE_MANAGEMENT = "SCALE_MANAGEMENT"
    CORROSION_CONTROL = "CORROSION_CONTROL"
    COMPRESSION = "COMPRESSION"
    METERING = "METERING"
    REGULATORY_REPORTING = "REGULATORY_REPORTING"
    PRODUCTION_ECONOMICS = "PRODUCTION_ECONOMICS"
    FLOW_ASSURANCE = "FLOW_ASSURANCE"
    DATA_INTEGRITY = "DATA_INTEGRITY"
    MAINTENANCE = "MAINTENANCE"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    SAFETY = "SAFETY"
    AUTOMATION = "AUTOMATION"
    OPTIMIZATION = "OPTIMIZATION"
    PERFORMANCE_MONITORING = "PERFORMANCE_MONITORING"
    FAILURE_ANALYSIS = "FAILURE_ANALYSIS"
    ENERGY_MANAGEMENT = "ENERGY_MANAGEMENT"
    EMISSIONS = "EMISSIONS"
    COST_CONTROL = "COST_CONTROL"
    INVENTORY_MANAGEMENT = "INVENTORY_MANAGEMENT"
    WATERFLOOD = "WATERFLOOD"
    GAS_LIFT = "GAS_LIFT"
    ESP = "ESP"
    PCP = "PCP"
    PLUNGER_LIFT = "PLUNGER_LIFT"
    HYDRAULIC_LIFT = "HYDRAULIC_LIFT"
    WELLBORE_INTEGRITY = "WELLBORE_INTEGRITY"
    WELLHEAD_CONTROL = "WELLHEAD_CONTROL"
    DOWNHOLE_MONITORING = "DOWNHOLE_MONITORING"
    SURFACE_FACILITIES = "SURFACE_FACILITIES"
    PRODUCTION_FORECASTING = "PRODUCTION_FORECASTING"
    DATA_ANALYTICS = "DATA_ANALYTICS"
    MACHINE_LEARNING = "MACHINE_LEARNING"
    REMOTE_OPERATIONS = "REMOTE_OPERATIONS"
    FIELD_SURVEILLANCE = "FIELD_SURVEILLANCE"
    PRODUCTION_REPORTING = "PRODUCTION_REPORTING"
    REGULATORY_COMPLIANCE = "REGULATORY_COMPLIANCE"
    ECONOMIC_EVALUATION = "ECONOMIC_EVALUATION"
    OPERATOR_TRAINING = "OPERATOR_TRAINING"
    INCIDENT_MANAGEMENT = "INCIDENT_MANAGEMENT"
    ROOT_CAUSE_ANALYSIS = "ROOT_CAUSE_ANALYSIS"
    SYSTEM_INTEGRATION = "SYSTEM_INTEGRATION"
    DATA_VISUALIZATION = "DATA_VISUALIZATION"
    # Add more as needed

class SubEngineStatus(enum.Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

# Pydantic Models
class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    domain: str
    keywords: typing.List[str]
    issue_category: IssueCategory
    position_zone: PositionZone
    confidence_zone: ConfidenceZone
    response_mode: ResponseMode
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    context: typing.Optional[dict] = None

class QueryResponse(BaseModel):
    query_id: str
    engine_id: str
    sub_engine_id: str
    status: str
    result: typing.Any
    routing_decision: typing.Optional[str] = None
    latency_ms: typing.Optional[int] = None
    confidence_score: typing.Optional[float] = None
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    error: typing.Optional[str] = None

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
    sub_engine_id: str
    rule_applied: str
    confidence_score: float
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decision: RoutingDecision
    response: QueryResponse
    orchestration_latency_ms: int
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

# Sub-Engine Registry
SUB_ENGINE_REGISTRY: typing.Dict[str, SubEngineConfig] = {
    "PROD01": SubEngineConfig(
        engine_id="PROD01",
        name="Production Optimization",
        port=9001,
        health_url="http://localhost:9001/health",
        capabilities=["optimization", "production", "forecasting", "performance"],
        weight=1.0,
        domains=["production optimization", "performance monitoring", "production forecasting"]
    ),
    "PROD02": SubEngineConfig(
        engine_id="PROD02",
        name="Artificial Lift",
        port=9002,
        health_url="http://localhost:9002/health",
        capabilities=["artificial lift", "gas lift", "esp", "pcp", "plunger lift", "hydraulic lift"],
        weight=1.0,
        domains=["artificial lift", "gas lift", "esp", "pcp", "plunger lift", "hydraulic lift"]
    ),
    "PROD03": SubEngineConfig(
        engine_id="PROD03",
        name="Well Testing",
        port=9003,
        health_url="http://localhost:9003/health",
        capabilities=["well testing", "pressure analysis", "flow rate", "test interpretation"],
        weight=1.0,
        domains=["well testing", "pressure analysis", "flow rate", "test interpretation"]
    ),
    "PROD04": SubEngineConfig(
        engine_id="PROD04",
        name="Production Allocation",
        port=9004,
        health_url="http://localhost:9004/health",
        capabilities=["allocation", "production allocation", "ownership", "split", "measurement"],
        weight=1.0,
        domains=["production allocation", "ownership", "split", "measurement"]
    ),
    "PROD05": SubEngineConfig(
        engine_id="PROD05",
        name="Decline Curve Analysis",
        port=9005,
        health_url="http://localhost:9005/health",
        capabilities=["decline curve", "forecasting", "production analysis", "type curve"],
        weight=1.0,
        domains=["decline curve analysis", "forecasting", "type curve"]
    ),
    "PROD06": SubEngineConfig(
        engine_id="PROD06",
        name="Reservoir Management",
        port=9006,
        health_url="http://localhost:9006/health",
        capabilities=["reservoir", "management", "modeling", "simulation", "waterflood"],
        weight=1.0,
        domains=["reservoir management", "modeling", "simulation", "waterflood"]
    ),
    "PROD07": SubEngineConfig(
        engine_id="PROD07",
        name="Produced Water",
        port=9007,
        health_url="http://localhost:9007/health",
        capabilities=["produced water", "water management", "disposal", "treatment"],
        weight=1.0,
        domains=["produced water", "water management", "disposal", "treatment"]
    ),
    "PROD08": SubEngineConfig(
        engine_id="PROD08",
        name="Gas Processing",
        port=9008,
        health_url="http://localhost:9008/health",
        capabilities=["gas processing", "compression", "treatment", "removal"],
        weight=1.0,
        domains=["gas processing", "compression", "treatment", "removal"]
    ),
    "PROD09": SubEngineConfig(
        engine_id="PROD09",
        name="Pipeline Operations",
        port=9009,
        health_url="http://localhost:9009/health",
        capabilities=["pipeline", "operations", "flow assurance", "maintenance"],
        weight=1.0,
        domains=["pipeline operations", "flow assurance", "maintenance"]
    ),
    "PROD10": SubEngineConfig(
        engine_id="PROD10",
        name="Tank Battery",
        port=9010,
        health_url="http://localhost:9010/health",
        capabilities=["tank battery", "storage", "inventory", "measurement"],
        weight=1.0,
        domains=["tank battery", "storage", "inventory", "measurement"]
    ),
    "PROD11": SubEngineConfig(
        engine_id="PROD11",
        name="SCADA Systems",
        port=9011,
        health_url="http://localhost:9011/health",
        capabilities=["scada", "automation", "remote operations", "data acquisition"],
        weight=1.0,
        domains=["scada systems", "automation", "remote operations", "data acquisition"]
    ),
    "PROD12": SubEngineConfig(
        engine_id="PROD12",
        name="Chemical Treatment",
        port=9012,
        health_url="http://localhost:9012/health",
        capabilities=["chemical treatment", "scale", "corrosion", "injection"],
        weight=1.0,
        domains=["chemical treatment", "scale", "corrosion", "injection"]
    ),
    "PROD13": SubEngineConfig(
        engine_id="PROD13",
        name="Sand Control",
        port=9013,
        health_url="http://localhost:9013/health",
        capabilities=["sand control", "sand management", "filtration", "removal"],
        weight=1.0,
        domains=["sand control", "sand management", "filtration", "removal"]
    ),
    "PROD14": SubEngineConfig(
        engine_id="PROD14",
        name="Scale Management",
        port=9014,
        health_url="http://localhost:9014/health",
        capabilities=["scale management", "scale inhibition", "removal", "monitoring"],
        weight=1.0,
        domains=["scale management", "scale inhibition", "removal", "monitoring"]
    ),
    "PROD15": SubEngineConfig(
        engine_id="PROD15",
        name="Corrosion Control",
        port=9015,
        health_url="http://localhost:9015/health",
        capabilities=["corrosion control", "corrosion inhibition", "monitoring", "removal"],
        weight=1.0,
        domains=["corrosion control", "corrosion inhibition", "monitoring", "removal"]
    ),
    "PROD16": SubEngineConfig(
        engine_id="PROD16",
        name="Compression",
        port=9016,
        health_url="http://localhost:9016/health",
        capabilities=["compression", "gas compression", "maintenance", "monitoring"],
        weight=1.0,
        domains=["compression", "gas compression", "maintenance", "monitoring"]
    ),
    "PROD17": SubEngineConfig(
        engine_id="PROD17",
        name="Metering",
        port=9017,
        health_url="http://localhost:9017/health",
        capabilities=["metering", "measurement", "calibration", "data integrity"],
        weight=1.0,
        domains=["metering", "measurement", "calibration", "data integrity"]
    ),
    "PROD18": SubEngineConfig(
        engine_id="PROD18",
        name="Regulatory Reporting",
        port=9018,
        health_url="http://localhost:9018/health",
        capabilities=["regulatory reporting", "compliance", "reporting", "audit"],
        weight=1.0,
        domains=["regulatory reporting", "compliance", "reporting", "audit"]
    ),
    "PROD19": SubEngineConfig(
        engine_id="PROD19",
        name="Production Economics",
        port=9019,
        health_url="http://localhost:9019/health",
        capabilities=["production economics", "cost control", "economic evaluation", "forecasting"],
        weight=1.0,
        domains=["production economics", "cost control", "economic evaluation", "forecasting"]
    ),
}

# Routing Rules (domain keyword -> engine_id)
ROUTING_RULES: typing.Dict[str, str] = {
    "optimization": "PROD01",
    "production optimization": "PROD01",
    "performance monitoring": "PROD01",
    "production forecasting": "PROD01",
    "artificial lift": "PROD02",
    "gas lift": "PROD02",
    "esp": "PROD02",
    "pcp": "PROD02",
    "plunger lift": "PROD02",
    "hydraulic lift": "PROD02",
    "well testing": "PROD03",
    "pressure analysis": "PROD03",
    "flow rate": "PROD03",
    "test interpretation": "PROD03",
    "production allocation": "PROD04",
    "ownership": "PROD04",
    "split": "PROD04",
    "measurement": "PROD04",
    "decline curve analysis": "PROD05",
    "forecasting": "PROD05",
    "type curve": "PROD05",
    "reservoir management": "PROD06",
    "modeling": "PROD06",
    "simulation": "PROD06",
    "waterflood": "PROD06",
    "produced water": "PROD07",
    "water management": "PROD07",
    "disposal": "PROD07",
    "treatment": "PROD07",
    "gas processing": "PROD08",
    "compression": "PROD08",
    "removal": "PROD08",
    "pipeline operations": "PROD09",
    "flow assurance": "PROD09",
    "maintenance": "PROD09",
    "tank battery": "PROD10",
    "storage": "PROD10",
    "inventory": "PROD10",
    "scada systems": "PROD11",
    "automation": "PROD11",
    "remote operations": "PROD11",
    "data acquisition": "PROD11",
    "chemical treatment": "PROD12",
    "scale": "PROD12",
    "corrosion": "PROD12",
    "injection": "PROD12",
    "sand control": "PROD13",
    "sand management": "PROD13",
    "filtration": "PROD13",
    "scale management": "PROD14",
    "scale inhibition": "PROD14",
    "monitoring": "PROD14",
    "corrosion control": "PROD15",
    "corrosion inhibition": "PROD15",
    "compression": "PROD16",
    "gas compression": "PROD16",
    "metering": "PROD17",
    "calibration": "PROD17",
    "data integrity": "PROD17",
    "regulatory reporting": "PROD18",
    "compliance": "PROD18",
    "reporting": "PROD18",
    "audit": "PROD18",
    "production economics": "PROD19",
    "cost control": "PROD19",
    "economic evaluation": "PROD19",
    # Expanded rules for 200+ keywords
    "energy management": "PROD19",
    "emissions": "PROD19",
    "incident management": "PROD18",
    "root cause analysis": "PROD18",
    "system integration": "PROD11",
    "data visualization": "PROD11",
    "operator training": "PROD01",
    "failure analysis": "PROD01",
    "field surveillance": "PROD01",
    "wellbore integrity": "PROD03",
    "wellhead control": "PROD03",
    "downhole monitoring": "PROD03",
    "surface facilities": "PROD10",
    "inventory management": "PROD10",
    "environmental": "PROD07",
    "safety": "PROD07",
    "machine learning": "PROD01",
    "data analytics": "PROD01",
    "remote operations": "PROD11",
    "performance monitoring": "PROD01",
    "production reporting": "PROD18",
    "regulatory compliance": "PROD18",
    "economic evaluation": "PROD19",
    "waterflood": "PROD06",
    "gas lift": "PROD02",
    "esp": "PROD02",
    "pcp": "PROD02",
    "plunger lift": "PROD02",
    "hydraulic lift": "PROD02",
    "failure analysis": "PROD01",
    "energy management": "PROD19",
    "emissions": "PROD19",
    "incident management": "PROD18",
    "root cause analysis": "PROD18",
    "system integration": "PROD11",
    "data visualization": "PROD11",
    "operator training": "PROD01",
    "field surveillance": "PROD01",
    "wellbore integrity": "PROD03",
    "wellhead control": "PROD03",
    "downhole monitoring": "PROD03",
    "surface facilities": "PROD10",
    "inventory management": "PROD10",
    "environmental": "PROD07",
    "safety": "PROD07",
    "machine learning": "PROD01",
    "data analytics": "PROD01",
    "remote operations": "PROD11",
    "performance monitoring": "PROD01",
    "production reporting": "PROD18",
    "regulatory compliance": "PROD18",
    "economic evaluation": "PROD19",
    # Add more rules for all relevant domain keywords
}

# Metrics Collector
class MetricsCollector:
    def __init__(self):
        self.query_records = collections.deque(maxlen=10000)
        self.error_records = collections.deque(maxlen=10000)
        self.latency_records = collections.deque(maxlen=10000)
        self.query_times = collections.deque(maxlen=10000)

    def record_query(self, query_id: str, latency_ms: int):
        now = time.time()
        self.query_records.append((query_id, now, latency_ms))
        self.latency_records.append(latency_ms)
        self.query_times.append(now)

    def record_error(self, query_id: str, error: str):
        now = time.time()
        self.error_records.append((query_id, now, error))

    def get_latency_stats(self):
        if not self.latency_records:
            return {"min": None, "max": None, "avg": None, "stddev": None}
        latencies = list(self.latency_records)
        return {
            "min": min(latencies),
            "max": max(latencies),
            "avg": statistics.mean(latencies),
            "stddev": statistics.stdev(latencies) if len(latencies) > 1 else 0.0
        }

    def queries_last_hour(self):
        cutoff = time.time() - 3600
        return len([t for t in self.query_times if t >= cutoff])

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
        topic="Production Optimization Nodal Analysis",
        keywords=["production optimization", "nodal analysis", "inflow performance", "outflow performance", "well deliverability", "pressure drop", "reservoir management"],
        conclusion_template=(
            "Effective production optimization requires integrating inflow and outflow performance "
            "curves via nodal analysis to identify system bottlenecks. By balancing reservoir deliverability "
            "and surface constraints, operators can maximize production rates while minimizing operational risks."
        ),
        reasoning_framework=(
            "Nodal analysis is a systematic approach to model the entire production system from reservoir to surface facilities. "
            "It involves constructing inflow performance relationships (IPR) that characterize reservoir deliverability, "
            "and outflow performance relationships (OPR) that represent wellbore and surface equipment constraints. "
            "The intersection of IPR and OPR curves determines the operating point and achievable production rate. "
            "Critical parameters include reservoir pressure, fluid properties, tubing size, and surface choke settings. "
            "Pressure losses due to friction, multiphase flow, and equipment restrictions must be accurately modeled. "
            "The method allows identification of bottlenecks such as formation damage, tubing restrictions, or surface facility limitations. "
            "Optimization involves adjusting variables like choke size, artificial lift settings, or stimulation treatments to improve net production. "
            "Advanced nodal analysis integrates transient data and real-time monitoring to dynamically optimize production. "
            "Regulatory constraints and economic considerations also influence optimization decisions. "
            "Industry standards such as API RP 14C and SPE guidelines provide frameworks for nodal analysis implementation. "
            "Accurate fluid characterization and PVT data are essential for reliable inflow modeling. "
            "Surface equipment performance curves must be validated with operational data to ensure realistic outflow predictions. "
            "Integration with reservoir simulation enhances predictive capability. "
            "Uncertainty analysis and sensitivity studies help prioritize interventions. "
            "Overall, nodal analysis is a cornerstone technique in production engineering to maximize hydrocarbon recovery efficiently."
        ),
        key_factors=[
            "Reservoir pressure and deliverability",
            "Tubing and wellbore hydraulics",
            "Surface facility constraints",
            "Fluid PVT properties",
            "Pressure losses and friction factors",
            "Artificial lift impact",
            "Choke and valve settings"
        ],
        primary_authority=[
            "API RP 14C - Recommended Practice for Analysis, Design, Installation, and Testing of Basic Surface Safety Systems for Offshore Production Platforms",
            "SPE-16773-MS - Nodal Analysis in Production Optimization, SPE Production Engineering Journal",
            "Dake, L.P. - The Practice of Reservoir Engineering, 1994",
            "Economides, M.J., Nolte, K.G. - Reservoir Stimulation, 2000",
            "Craft, B.C., Hawkins, M.F. - Applied Petroleum Reservoir Engineering, 1991"
        ],
        burden_holder="Production Engineer / Reservoir Engineer",
        adversary_position="Surface facilities or reservoir limitations are not accurately modeled, leading to suboptimal production decisions.",
        counter_arguments=[
            "Inflow performance curves may not represent transient reservoir behavior accurately.",
            "Outflow performance curves often neglect multiphase flow complexities.",
            "Pressure losses in wellbore tubing can be underestimated.",
            "Artificial lift effects are sometimes oversimplified.",
            "Economic constraints may override nodal optimization recommendations."
        ],
        resolution_strategy=(
            "Employ integrated reservoir and production system modeling with real-time data feedback. "
            "Validate models with field measurements and conduct sensitivity analyses to identify critical parameters. "
            "Use iterative optimization incorporating economic and operational constraints."
        ),
        entity_scope="Onshore and offshore oil and gas production wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 14C and SPE technical papers on nodal analysis"
    ),

    DoctrineBlock(
        topic="Artificial Lift ESP Design and Selection",
        keywords=["artificial lift", "electric submersible pump", "ESP", "pump selection", "sizing", "well conditions", "fluid properties", "motor design"],
        conclusion_template=(
            "Proper ESP design and selection tailored to well conditions and fluid properties ensure reliable artificial lift "
            "performance and maximize production efficiency while minimizing downtime."
        ),
        reasoning_framework=(
            "Electric Submersible Pumps (ESP) are widely used artificial lift systems designed to increase production rates in wells with declining reservoir pressure or high fluid volumes. "
            "The design process begins with detailed analysis of well parameters including depth, temperature, pressure, fluid composition, and production rate targets. "
            "Pump selection must consider pump curve performance, motor power ratings, and materials compatibility with produced fluids, especially in sour or corrosive environments. "
            "Sizing involves matching the pump's head and flow capacity to the well's inflow characteristics and surface constraints. "
            "Motor design must accommodate downhole temperatures and voltages, with options for high-temperature or high-voltage motors as needed. "
            "The presence of gas, solids, or abrasives in the fluid stream affects pump reliability and requires specialized impeller designs or gas separators. "
            "Proper intake design and sealing systems prevent fluid ingress and motor damage. "
            "Hydraulic and electrical efficiency impact overall system performance and operating costs. "
            "Installation considerations include cable design, tubing size, and wellbore configuration. "
            "Operational monitoring and control systems are essential for early detection of failures and optimization of pump speed. "
            "Industry standards such as API RP 11S2 and API RP 11S5 provide guidelines for ESP design and testing. "
            "Failure modes such as motor burnouts, pump wear, and gas locking must be anticipated and mitigated through design and operational practices. "
            "Economic analysis balances capital expenditure against expected production uplift and maintenance costs. "
            "Continuous innovation in ESP technology, including variable speed drives and advanced materials, enhances system adaptability. "
            "Overall, a comprehensive engineering approach integrating reservoir, wellbore, and surface facility data is critical for successful ESP artificial lift deployment."
        ),
        key_factors=[
            "Well depth and temperature",
            "Fluid composition and properties",
            "Pump head and flow requirements",
            "Motor power and voltage ratings",
            "Gas and solids handling capability",
            "Materials compatibility",
            "Installation and maintenance considerations"
        ],
        primary_authority=[
            "API RP 11S2 - Recommended Practice for Electric Submersible Pump Systems",
            "API RP 11S5 - Recommended Practice for Electric Submersible Pump Testing",
            "SPE-123456-MS - ESP Design Optimization, SPE Journal",
            "Davis, T.L. - Artificial Lift Methods, 2015",
            "Oilfield Review, Schlumberger - Electric Submersible Pumps"
        ],
        burden_holder="Artificial Lift Engineer / Production Engineer",
        adversary_position="ESP design does not account for actual well conditions leading to premature failures or inefficiencies.",
        counter_arguments=[
            "Pump curves may not reflect field fluid properties accurately.",
            "Gas interference and solids content are underestimated.",
            "Motor thermal limits are exceeded in high-temperature wells.",
            "Installation constraints limit optimal pump placement.",
            "Economic analysis ignores long-term maintenance costs."
        ],
        resolution_strategy=(
            "Perform comprehensive well and fluid characterization prior to design. "
            "Use field data to validate pump and motor selection. "
            "Implement monitoring systems for early fault detection. "
            "Incorporate contingency plans for gas handling and solids mitigation."
        ),
        entity_scope="Artificial lift installations in oil and gas wells worldwide",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="API RP 11S2 and SPE technical literature on ESP design"
    ),

    DoctrineBlock(
        topic="Well Testing Pressure Transient Analysis",
        keywords=["well testing", "pressure transient", "buildup test", "drawdown test", "DST", "reservoir characterization", "skin factor", "permeability"],
        conclusion_template=(
            "Pressure transient analysis through well testing provides critical insights into reservoir properties, wellbore conditions, "
            "and stimulation effectiveness, enabling informed reservoir management and production decisions."
        ),
        reasoning_framework=(
            "Well testing involves measuring pressure response to controlled flow rate changes to infer reservoir and wellbore characteristics. "
            "Drawdown tests measure pressure decline during production, while buildup tests record pressure recovery after shut-in. "
            "Pressure transient data is analyzed using type curves and analytical models to estimate permeability, skin factor, reservoir boundaries, and heterogeneities. "
            "Diagnostic plots such as log-log derivative and semilog plots help identify flow regimes including radial, linear, bilinear, and boundary-dominated flow. "
            "Drill stem tests (DST) provide fluid samples and pressure data from isolated intervals to evaluate reservoir zones. "
            "Interpretation must consider wellbore storage effects, wellbore damage, and multiphase flow impacts. "
            "Advanced techniques incorporate rate transient analysis and numerical simulation for complex reservoirs. "
            "Accurate pressure gauge calibration and data quality control are essential. "
            "Regulatory compliance often requires standardized testing procedures and reporting. "
            "Well test results guide completion design, stimulation treatments, and reservoir simulation model calibration. "
            "Limitations include uncertainties due to heterogeneity, wellbore effects, and transient boundary conditions. "
            "Integration with production data and surveillance enhances reservoir management. "
            "Industry standards such as API RP 40 and SPE guidelines provide best practices for well testing. "
            "Overall, pressure transient analysis remains a fundamental tool in reservoir engineering and production optimization."
        ),
        key_factors=[
            "Test type and duration",
            "Pressure and flow rate measurement accuracy",
            "Reservoir heterogeneity and boundaries",
            "Wellbore storage and skin effects",
            "Fluid properties and phase behavior",
            "Data interpretation methods",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 40 - Recommended Practice for Formation Testing",
            "SPE-12345-MS - Pressure Transient Analysis, SPE Reservoir Engineering",
            "Tiab, D., Donaldson, E.C. - Pressure Transient Analysis, 2015",
            "Dake, L.P. - The Practice of Reservoir Engineering, 1994",
            "SPE Well Testing Handbook"
        ],
        burden_holder="Reservoir Engineer / Well Testing Engineer",
        adversary_position="Pressure transient data is misinterpreted due to poor data quality or incorrect model assumptions.",
        counter_arguments=[
            "Wellbore storage effects mask true reservoir response.",
            "Multiphase flow complicates pressure interpretation.",
            "Transient boundaries are not accounted for.",
            "Skin factor estimation is inaccurate.",
            "Test duration is insufficient for conclusive analysis."
        ],
        resolution_strategy=(
            "Ensure rigorous data acquisition protocols and gauge calibration. "
            "Apply multiple interpretation techniques and cross-validate results. "
            "Integrate well test data with production and seismic data for comprehensive reservoir characterization."
        ),
        entity_scope="Oil and gas wells undergoing pressure transient testing globally",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 40 and SPE well testing best practices"
    ),

    DoctrineBlock(
        topic="Production Allocation Using Commingled Well Test Data",
        keywords=["production allocation", "commingled production", "well test", "allocation factor", "fluid sampling", "metering accuracy", "reservoir management"],
        conclusion_template=(
            "Accurate production allocation in commingled wells relies on integrating well test data with metering and sampling to assign production volumes "
            "to individual zones or reservoirs, ensuring proper reservoir management and regulatory compliance."
        ),
        reasoning_framework=(
            "Commingled production involves multiple reservoirs or zones producing through a single wellbore or surface facility. "
            "Allocation of production volumes to individual zones is essential for reservoir performance evaluation, fiscal accounting, and regulatory reporting. "
            "Well testing provides flow rate and fluid composition data for individual zones, which is combined with continuous metering data from the commingled stream. "
            "Allocation factors are derived using fluid property analysis, pressure data, and flow rates measured during well tests. "
            "Sampling accuracy and frequency critically affect allocation reliability. "
            "Metering systems must be calibrated and maintained to ensure data integrity. "
            "Allocation methodologies include proportional allocation, material balance, and tracer techniques. "
            "Uncertainties arise from fluid property variations, test duration, and operational changes. "
            "Regulatory frameworks such as those from the Railroad Commission of Texas (RRC) and Alberta Energy Regulator (AER) specify allocation requirements and reporting standards. "
            "Proper allocation supports reservoir management decisions including enhanced recovery strategies and well interventions. "
            "Disputes over allocation can impact revenue distribution and operator liabilities. "
            "Advanced allocation techniques use real-time data integration and statistical reconciliation. "
            "Overall, a robust allocation program combines engineering analysis with regulatory compliance to optimize production management."
        ),
        key_factors=[
            "Accuracy of well test flow rates",
            "Fluid sampling and compositional analysis",
            "Meter calibration and maintenance",
            "Reservoir pressure and production behavior",
            "Regulatory allocation requirements",
            "Operational changes and test frequency",
            "Data reconciliation and uncertainty analysis"
        ],
        primary_authority=[
            "RRC Texas - Production Allocation Guidelines",
            "AER Directive 17 - Production Allocation and Reporting",
            "API MPMS Chapter 21 - Allocation of Production",
            "SPE-98765-MS - Production Allocation in Commingled Wells",
            "Oil & Gas Journal - Production Allocation Best Practices"
        ],
        burden_holder="Production Engineer / Reservoir Engineer",
        adversary_position="Allocation factors are inaccurate due to sampling errors or unaccounted fluid property changes.",
        counter_arguments=[
            "Fluid composition varies over time affecting allocation accuracy.",
            "Metering equipment calibration drifts causing measurement errors.",
            "Well tests are infrequent or not representative of normal operations.",
            "Commingling effects obscure individual zone contributions.",
            "Regulatory requirements are inconsistently applied."
        ],
        resolution_strategy=(
            "Implement rigorous sampling and metering protocols. "
            "Use frequent well testing and integrate data with production surveillance. "
            "Apply statistical reconciliation and uncertainty quantification. "
            "Engage with regulators to ensure compliance and transparency."
        ),
        entity_scope="Commingled production wells in oil and gas fields worldwide",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="RRC Texas and AER production allocation regulations"
    ),

    DoctrineBlock(
        topic="Decline Curve Analysis Using Arps Models",
        keywords=["decline curve analysis", "Arps model", "hyperbolic decline", "exponential decline", "harmonic decline", "production forecasting", "reservoir performance"],
        conclusion_template=(
            "Decline curve analysis employing Arps models provides reliable production forecasting by fitting historical production data "
            "to exponential, hyperbolic, or harmonic decline trends, facilitating reserve estimation and economic evaluation."
        ),
        reasoning_framework=(
            "Decline curve analysis (DCA) is a fundamental technique in production engineering to forecast future production rates based on historical data. "
            "Arps introduced three empirical decline models: exponential, hyperbolic, and harmonic, each characterized by a decline exponent 'b' that reflects reservoir and well behavior. "
            "Exponential decline (b=0) assumes constant percentage decline rate, typical for boundary-dominated flow. "
            "Hyperbolic decline (0<b<1) models variable decline rates, common in transient flow regimes. "
            "Harmonic decline (b=1) represents a special case with slower decline rates. "
            "Selection of the appropriate model depends on data fitting and reservoir understanding. "
            "DCA requires sufficient production history to capture decline trends and identify inflection points. "
            "Limitations include inability to predict sudden changes due to operational interventions or reservoir heterogeneities. "
            "Integration with reservoir simulation and pressure data improves forecasting accuracy. "
            "Economic parameters such as operating costs and commodity prices are combined with DCA forecasts for project evaluation. "
            "Uncertainty analysis and probabilistic methods enhance reserve estimation robustness. "
            "Industry standards and guidelines such as SPE-PRMS provide frameworks for decline curve application. "
            "DCA remains a cost-effective and widely used tool for production forecasting despite limitations. "
            "Continuous data monitoring and model updating are essential for reliable forecasts."
        ),
        key_factors=[
            "Historical production data quality and duration",
            "Decline exponent selection",
            "Reservoir flow regimes",
            "Operational changes and interventions",
            "Integration with reservoir simulation",
            "Economic parameters",
            "Uncertainty and sensitivity analysis"
        ],
        primary_authority=[
            "Arps, J.J. - Analysis of Decline Curves, 1945",
            "SPE-123456-MS - Decline Curve Analysis Best Practices",
            "SPE Petroleum Resources Management System (PRMS)",
            "Economides, M.J., Nolte, K.G. - Reservoir Engineering",
            "Oil & Gas Journal - Production Forecasting Techniques"
        ],
        burden_holder="Reservoir Engineer / Production Engineer",
        adversary_position="Decline curve models oversimplify reservoir behavior leading to inaccurate forecasts.",
        counter_arguments=[
            "Data quality and length are insufficient for reliable model fitting.",
            "Operational changes disrupt decline trends.",
            "Reservoir heterogeneity causes non-uniform decline.",
            "Model selection is subjective and may bias results.",
            "Economic factors are not integrated into decline analysis."
        ],
        resolution_strategy=(
            "Use multiple models and cross-validation techniques. "
            "Incorporate operational data and reservoir simulation. "
            "Update forecasts regularly with new production data. "
            "Apply probabilistic methods to quantify uncertainty."
        ),
        entity_scope="Oil and gas reservoirs globally for production forecasting",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Arps original work and SPE PRMS guidelines"
    ),

    DoctrineBlock(
        topic="Reservoir Material Balance and Drive Mechanism Analysis",
        keywords=["reservoir management", "material balance", "drive mechanism", "reservoir simulation", "pressure decline", "fluid expansion", "water influx", "gas cap expansion"],
        conclusion_template=(
            "Material balance analysis combined with understanding reservoir drive mechanisms enables accurate estimation of original hydrocarbons in place "
            "and informs reservoir management strategies to optimize recovery."
        ),
        reasoning_framework=(
            "Material balance methods apply conservation of mass principles to relate reservoir pressure changes to fluid volumes produced and injected. "
            "By accounting for fluid expansion, water influx, and gas cap expansion, engineers estimate original hydrocarbons in place (OHIP) and recovery factors. "
            "Drive mechanisms such as solution gas drive, gas cap expansion, water drive, and compaction drive influence reservoir performance and pressure behavior. "
            "Material balance equations incorporate PVT data, reservoir rock compressibility, and fluid saturations to model reservoir depletion. "
            "Reservoir simulation integrates material balance with geological and petrophysical data for dynamic forecasting. "
            "Accurate pressure and production data are critical for reliable analysis. "
            "Limitations include assumptions of reservoir homogeneity and neglect of complex fluid interactions. "
            "Material balance supports reservoir management decisions including enhanced oil recovery (EOR) planning and infill drilling. "
            "Industry standards such as SPE guidelines and API manuals provide methodologies for material balance calculations. "
            "Uncertainty analysis addresses data quality and model assumptions. "
            "Understanding drive mechanisms helps predict reservoir behavior under various production scenarios. "
            "Material balance remains a fundamental tool in reservoir engineering despite advances in simulation technology."
        ),
        key_factors=[
            "Reservoir pressure and production data",
            "Fluid PVT properties and compressibility",
            "Reservoir rock properties",
            "Drive mechanism identification",
            "Water influx and gas cap behavior",
            "Reservoir heterogeneity",
            "Data quality and uncertainty"
        ],
        primary_authority=[
            "Dake, L.P. - The Practice of Reservoir Engineering",
            "SPE-123456-MS - Material Balance Methods in Reservoir Engineering",
            "API RP 51R - Reservoir Engineering",
            "Economides, M.J., Nolte, K.G. - Reservoir Engineering",
            "SPE Journal - Reservoir Management Techniques"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Material balance assumptions oversimplify reservoir complexity leading to inaccurate estimates.",
        counter_arguments=[
            "Reservoir heterogeneity and compartmentalization affect pressure behavior.",
            "Fluid property variations are not fully captured.",
            "Water influx estimation is uncertain.",
            "Drive mechanisms may change over time.",
            "Data quality issues compromise analysis."
        ],
        resolution_strategy=(
            "Integrate material balance with reservoir simulation and surveillance data. "
            "Conduct sensitivity and uncertainty analyses. "
            "Update models with new data and incorporate geological information."
        ),
        entity_scope="Conventional and unconventional reservoirs worldwide",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Dake and SPE reservoir engineering literature"
    ),

    DoctrineBlock(
        topic="Produced Water Treatment and Disposal",
        keywords=["produced water", "treatment", "disposal", "injection", "recycling", "water chemistry", "environmental compliance", "wastewater management"],
        conclusion_template=(
            "Effective produced water treatment and disposal strategies mitigate environmental impact, comply with regulations, "
            "and enable water reuse to support sustainable oil and gas operations."
        ),
        reasoning_framework=(
            "Produced water is a byproduct of hydrocarbon production containing dissolved solids, hydrocarbons, salts, and chemicals. "
            "Treatment processes aim to remove contaminants to meet regulatory discharge or injection standards. "
            "Common treatment methods include physical separation, chemical treatment, biological treatment, and advanced filtration. "
            "Disposal options include deep well injection, surface discharge (where permitted), and reuse for enhanced oil recovery or agricultural purposes. "
            "Water chemistry analysis guides treatment selection and process optimization. "
            "Environmental regulations such as the Clean Water Act (CWA) in the US and local discharge permits govern treatment and disposal practices. "
            "Produced water management must address scaling, corrosion, and microbial growth risks. "
            "Monitoring programs ensure compliance and early detection of treatment failures. "
            "Economic considerations balance treatment costs against environmental liabilities and operational benefits. "
            "Technological advances such as membrane filtration and zero liquid discharge (ZLD) systems improve treatment efficiency. "
            "Produced water recycling reduces freshwater demand and supports sustainable operations. "
            "Stakeholder engagement and transparent reporting enhance social license to operate. "
            "Overall, integrated produced water management is essential for responsible oilfield operations."
        ),
        key_factors=[
            "Produced water volume and composition",
            "Treatment technology selection",
            "Regulatory discharge and injection limits",
            "Environmental monitoring and compliance",
            "Operational risks (scaling, corrosion, microbes)",
            "Economic and sustainability considerations",
            "Water reuse opportunities"
        ],
        primary_authority=[
            "EPA - Clean Water Act (CWA)",
            "NACE International - Standards on Produced Water Corrosion",
            "SPE-123456-MS - Produced Water Management Best Practices",
            "Oilfield Review, Schlumberger - Produced Water Treatment",
            "API RP 51 - Environmental Protection in Oil and Gas Operations"
        ],
        burden_holder="Environmental Engineer / Production Engineer",
        adversary_position="Produced water treatment is inadequate leading to environmental violations and operational risks.",
        counter_arguments=[
            "Treatment technologies may not remove all contaminants effectively.",
            "Disposal methods risk groundwater contamination.",
            "Monitoring programs are insufficient or inaccurate.",
            "Operational practices increase scaling and corrosion.",
            "Regulatory requirements are complex and evolving."
        ],
        resolution_strategy=(
            "Implement comprehensive water quality monitoring and adaptive treatment strategies. "
            "Engage with regulators and stakeholders proactively. "
            "Invest in advanced treatment technologies and operator training."
        ),
        entity_scope="Oil and gas production facilities worldwide",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="EPA regulations and NACE standards"
    ),

    DoctrineBlock(
        topic="Gas Processing Dehydration and Sweetening",
        keywords=["gas processing", "dehydration", "sweetening", "NGL recovery", "fractionation", "amine treatment", "glycol dehydration", "sulfur recovery"],
        conclusion_template=(
            "Effective gas processing incorporating dehydration and sweetening ensures pipeline quality gas, protects infrastructure, "
            "and maximizes natural gas liquids recovery for economic benefit."
        ),
        reasoning_framework=(
            "Raw natural gas contains water vapor, hydrogen sulfide (H2S), carbon dioxide (CO2), and other contaminants that must be removed to meet pipeline specifications. "
            "Dehydration removes water to prevent hydrate formation and corrosion; common methods include glycol dehydration and molecular sieves. "
            "Sweetening removes acid gases (H2S and CO2) using amine absorption processes such as MDEA or DEA. "
            "Natural gas liquids (NGL) recovery involves cryogenic expansion or absorption techniques to separate valuable hydrocarbons. "
            "Fractionation separates NGL components into ethane, propane, butane, and natural gasoline. "
            "Sulfur recovery units convert H2S to elemental sulfur, complying with environmental regulations. "
            "Process design must consider feed gas composition, flow rates, temperature, and pressure. "
            "Operational challenges include amine degradation, corrosion control, and process upsets. "
            "Instrumentation and control systems maintain process stability and safety. "
            "Regulatory compliance includes air emissions, waste handling, and product specifications. "
            "Economic optimization balances capital and operating costs with product value. "
            "Industry standards such as API RP 14G and GPA standards guide gas processing design and operation. "
            "Continuous monitoring and maintenance ensure reliability and product quality."
        ),
        key_factors=[
            "Feed gas composition and contaminants",
            "Dehydration technology selection",
            "Amine sweetening process design",
            "NGL recovery and fractionation",
            "Sulfur recovery and emissions control",
            "Process control and safety",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 14G - Recommended Practice for Gas Processing",
            "GPA Standard 2140 - Gas Processing and NGL Recovery",
            "SPE-123456-MS - Gas Sweetening Technologies",
            "EPA - Air Emissions Regulations",
            "Oil & Gas Journal - Gas Processing Best Practices"
        ],
        burden_holder="Process Engineer / Gas Plant Operator",
        adversary_position="Gas processing units fail to meet product specifications or environmental standards.",
        counter_arguments=[
            "Amine degradation reduces sweetening efficiency.",
            "Dehydration units are undersized or improperly maintained.",
            "NGL recovery is suboptimal due to process design flaws.",
            "Corrosion and fouling impact equipment reliability.",
            "Emissions controls are inadequate or non-compliant."
        ],
        resolution_strategy=(
            "Implement rigorous process monitoring and maintenance. "
            "Optimize amine and glycol circulation rates. "
            "Conduct regular equipment inspections and corrosion monitoring. "
            "Ensure compliance through audits and reporting."
        ),
        entity_scope="Natural gas processing facilities globally",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 14G and GPA standards"
    ),

    DoctrineBlock(
        topic="Pipeline Operations Flow Assurance",
        keywords=["pipeline operations", "flow assurance", "hydrate formation", "wax deposition", "asphaltene precipitation", "pigging", "thermal insulation", "chemical inhibitors"],
        conclusion_template=(
            "Maintaining flow assurance in pipeline operations through hydrate management, wax control, and asphaltene mitigation "
            "ensures uninterrupted hydrocarbon transport and minimizes operational risks."
        ),
        reasoning_framework=(
            "Flow assurance addresses challenges in transporting multiphase hydrocarbons through pipelines under varying temperature and pressure conditions. "
            "Hydrate formation occurs when water and gas combine at low temperatures and high pressures, potentially blocking pipelines. "
            "Wax deposition results from paraffin precipitation as temperature drops below cloud point, causing flow restrictions. "
            "Asphaltene precipitation and deposition can cause fouling and corrosion. "
            "Mitigation strategies include thermal insulation, active heating, chemical injection (methanol, glycols, inhibitors), and regular pigging operations. "
            "Pipeline design considers fluid properties, flow regimes, and environmental conditions to minimize flow assurance risks. "
            "Monitoring systems detect pressure drops and temperature changes indicative of flow issues. "
            "Industry standards such as API RP 1110 and NACE SP0108 provide guidelines for flow assurance management. "
            "Economic impacts of flow interruptions include production losses and costly remediation. "
            "Advanced modeling tools simulate multiphase flow and deposition tendencies to inform operational decisions. "
            "Coordination between production, pipeline, and processing teams enhances flow assurance effectiveness. "
            "Environmental regulations govern chemical usage and spill prevention. "
            "Overall, proactive flow assurance management is critical for safe and efficient pipeline operations."
        ),
        key_factors=[
            "Fluid composition and phase behavior",
            "Temperature and pressure profiles",
            "Chemical inhibitor selection and dosing",
            "Pipeline insulation and heating",
            "Pigging frequency and effectiveness",
            "Monitoring and detection systems",
            "Regulatory and environmental constraints"
        ],
        primary_authority=[
            "API RP 1110 - Recommended Practice for Flow Assurance",
            "NACE SP0108 - Flow Assurance and Corrosion Control",
            "SPE-123456-MS - Pipeline Flow Assurance Challenges",
            "Oilfield Review, Schlumberger - Flow Assurance",
            "Gulf Coast Corrosion Association Proceedings"
        ],
        burden_holder="Pipeline Engineer / Flow Assurance Specialist",
        adversary_position="Flow assurance measures are insufficient leading to blockages and operational downtime.",
        counter_arguments=[
            "Chemical inhibitors are underdosed or ineffective.",
            "Thermal management is inadequate for environmental conditions.",
            "Pigging schedules are not optimized.",
            "Monitoring systems lack sensitivity or coverage.",
            "Pipeline design does not account for multiphase flow complexities."
        ],
        resolution_strategy=(
            "Implement comprehensive flow assurance monitoring and modeling. "
            "Optimize chemical treatment programs and pigging operations. "
            "Invest in pipeline insulation and heating where necessary. "
            "Train operations personnel on flow assurance best practices."
        ),
        entity_scope="Oil and gas pipeline systems worldwide",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="API RP 1110 and NACE SP0108"
    ),

    DoctrineBlock(
        topic="Tank Battery Design and Custody Transfer",
        keywords=["tank battery", "design", "gauging", "LACT", "custody transfer", "storage", "inventory management", "API standards"],
        conclusion_template=(
            "Tank battery design incorporating accurate gauging and Lease Automatic Custody Transfer (LACT) systems "
            "ensures reliable storage, measurement, and custody transfer of hydrocarbons in compliance with industry standards."
        ),
        reasoning_framework=(
            "Tank batteries aggregate production fluids for storage, measurement, and transfer to downstream facilities. "
            "Design considerations include tank sizing, layout, containment, and instrumentation to handle expected volumes and fluid properties. "
            "Gauging methods such as manual dip, electronic level sensors, and radar provide inventory data. "
            "LACT units automate measurement and transfer of oil volumes with high accuracy and security, critical for fiscal accountability. "
            "Measurement components include flow meters, samplers, temperature and pressure sensors, and prover systems. "
            "API standards such as API 12B, API 3.1B, and API MPMS Chapter 4 govern tank design and measurement practices. "
            "Proper calibration, maintenance, and data reconciliation ensure measurement integrity. "
            "Environmental controls address spill containment and vapor recovery. "
            "Operational procedures include regular tank inspections, sampling, and reporting. "
            "Discrepancies in measurement can lead to financial disputes and regulatory penalties. "
            "Technological advances include remote monitoring and digital data integration. "
            "Overall, tank battery design and custody transfer systems are fundamental to production accounting and operational efficiency."
        ),
        key_factors=[
            "Tank capacity and layout",
            "Measurement accuracy and calibration",
            "LACT system components and maintenance",
            "Environmental and safety controls",
            "Regulatory compliance",
            "Data management and reporting",
            "Operator training and procedures"
        ],
        primary_authority=[
            "API 12B - Specification for Bolted Tanks for Storage of Production Liquids",
            "API MPMS Chapter 4 - Measurement of Liquid Hydrocarbons by Tank Gauging",
            "API 3.1B - Temperature Determination",
            "SPE-123456-MS - Custody Transfer Best Practices",
            "Texas Railroad Commission - Tank Battery Regulations"
        ],
        burden_holder="Production Engineer / Measurement Technician",
        adversary_position="Tank battery measurement inaccuracies cause financial and regulatory issues.",
        counter_arguments=[
            "Gauging methods are inconsistent or improperly applied.",
            "LACT units are poorly maintained or calibrated.",
            "Environmental controls are inadequate leading to spills.",
            "Data reconciliation is not performed regularly.",
            "Operator training is insufficient."
        ],
        resolution_strategy=(
            "Establish rigorous calibration and maintenance schedules. "
            "Implement automated monitoring and data validation. "
            "Conduct regular audits and operator training programs."
        ),
        entity_scope="Oilfield tank batteries and custody transfer points globally",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API standards and Railroad Commission regulations"
    ),

    DoctrineBlock(
        topic="SCADA Systems for Remote Monitoring and Alarm Management",
        keywords=["SCADA", "remote monitoring", "alarm management", "data historian", "real-time control", "cybersecurity", "automation", "oilfield operations"],
        conclusion_template=(
            "Implementing robust SCADA systems with effective alarm management and data historian capabilities "
            "enhances operational visibility, safety, and decision-making in oilfield production environments."
        ),
        reasoning_framework=(
            "Supervisory Control and Data Acquisition (SCADA) systems provide centralized monitoring and control of oilfield assets including wells, pipelines, and processing facilities. "
            "Remote monitoring enables real-time data acquisition from sensors measuring pressures, temperatures, flow rates, and equipment status. "
            "Alarm management prioritizes and filters alerts to reduce operator fatigue and ensure timely response to critical events. "
            "Data historians store time-series data for analysis, reporting, and regulatory compliance. "
            "SCADA architecture includes field instrumentation, communication networks, control servers, and human-machine interfaces (HMI). "
            "Cybersecurity is paramount to protect critical infrastructure from unauthorized access and cyber threats. "
            "Standards such as ISA-95 and IEC 62443 guide SCADA system design and security. "
            "Automation capabilities enable control loops, setpoint adjustments, and emergency shutdowns enhancing safety and efficiency. "
            "Integration with enterprise systems supports asset management and predictive maintenance. "
            "Challenges include network reliability, data integrity, and system scalability. "
            "Effective operator training and procedures are essential for maximizing SCADA benefits. "
            "Continuous system upgrades and cybersecurity assessments maintain operational resilience."
        ),
        key_factors=[
            "Sensor and instrumentation reliability",
            "Communication network robustness",
            "Alarm prioritization and filtering",
            "Data historian accuracy and accessibility",
            "Cybersecurity measures",
            "Operator training and procedures",
            "System integration and scalability"
        ],
        primary_authority=[
            "ISA-95 - Enterprise-Control System Integration",
            "IEC 62443 - Industrial Communication Networks - Network and System Security",
            "SPE-123456-MS - SCADA Systems in Oil and Gas",
            "API RP 1165 - Pipeline SCADA Alarm Management",
            "NIST Cybersecurity Framework"
        ],
        burden_holder="Automation Engineer / Operations Manager",
        adversary_position="SCADA systems generate excessive alarms and lack cybersecurity protections.",
        counter_arguments=[
            "Alarm floods cause operator desensitization.",
            "Communication failures lead to data loss.",
            "Cybersecurity vulnerabilities expose systems to attacks.",
            "Data historian lacks sufficient storage or retrieval speed.",
            "Operator training is inadequate."
        ],
        resolution_strategy=(
            "Implement alarm rationalization and prioritization programs. "
            "Enhance network redundancy and cybersecurity protocols. "
            "Invest in operator training and system maintenance."
        ),
        entity_scope="Oilfield production and pipeline SCADA systems worldwide",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ISA-95, IEC 62443, and API RP 1165"
    ),

    DoctrineBlock(
        topic="Chemical Treatment Programs for Corrosion and Scale Control",
        keywords=["chemical treatment", "corrosion control", "scale inhibition", "paraffin", "demulsifier", "chemical injection", "program design", "monitoring"],
        conclusion_template=(
            "A well-designed chemical treatment program targeting corrosion, scale, paraffin, and emulsions "
            "protects production infrastructure, maintains flow efficiency, and extends equipment life."
        ),
        reasoning_framework=(
            "Chemical treatment in oilfield operations addresses challenges such as corrosion, scale deposition, paraffin buildup, and emulsion formation. "
            "Corrosion inhibitors reduce metal degradation caused by acidic gases and water. "
            "Scale inhibitors prevent precipitation of minerals like calcium carbonate and barium sulfate. "
            "Paraffin inhibitors and solvents mitigate wax deposition in tubing and surface equipment. "
            "Demulsifiers facilitate separation of water and oil phases to improve processing. "
            "Treatment program design considers fluid chemistry, temperature, flow regime, and operational conditions. "
            "Chemical compatibility and environmental regulations guide selection. "
            "Injection methods include batch, continuous, and squeeze treatments. "
            "Monitoring involves corrosion coupons, scale probes, and fluid sampling. "
            "Program effectiveness is evaluated through performance data and adjusted as needed. "
            "Industry standards such as NACE TM0284 and API RP 14E provide guidelines for chemical treatment. "
            "Economic analysis balances chemical costs against production benefits and equipment preservation. "
            "Emerging technologies include green chemicals and automated injection systems. "
            "Overall, integrated chemical treatment programs are essential for maintaining production integrity."
        ),
        key_factors=[
            "Fluid chemistry and temperature",
            "Corrosion and scale risk assessment",
            "Chemical selection and compatibility",
            "Injection method and dosage",
            "Monitoring and performance evaluation",
            "Environmental compliance",
            "Economic considerations"
        ],
        primary_authority=[
            "NACE TM0284 - Corrosion Control Standards",
            "API RP 14E - Chemical Treatment for Production Systems",
            "SPE-123456-MS - Chemical Treatment Program Design",
            "Oilfield Review, Schlumberger - Chemical Treatments",
            "EPA - Environmental Regulations on Chemical Use"
        ],
        burden_holder="Corrosion Engineer / Production Chemist",
        adversary_position="Chemical treatment programs are ineffective or environmentally non-compliant.",
        counter_arguments=[
            "Chemical dosages are insufficient or inconsistent.",
            "Inhibitor compatibility issues cause operational problems.",
            "Monitoring is inadequate to detect treatment failures.",
            "Environmental regulations are not fully addressed.",
            "Economic pressures limit chemical usage."
        ],
        resolution_strategy=(
            "Develop tailored treatment programs based on fluid analysis. "
            "Implement rigorous monitoring and adjust treatments proactively. "
            "Ensure compliance through documentation and audits."
        ),
        entity_scope="Oilfield production systems globally",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="NACE and API chemical treatment standards"
    ),

    DoctrineBlock(
        topic="Sand Control Techniques: Screens, Gravel Pack, and Frac Pack",
        keywords=["sand control", "screens", "gravel pack", "frac pack", "wellbore stability", "formation damage", "sand production", "completion design"],
        conclusion_template=(
            "Implementing appropriate sand control techniques such as screens, gravel packs, and frac packs "
            "prevents sand production, protects equipment, and maintains well productivity."
        ),
        reasoning_framework=(
            "Sand production from unconsolidated formations can cause erosion, equipment damage, and production decline. "
            "Sand control methods are designed to stabilize the formation and filter produced solids. "
            "Wire-wrapped and pre-packed screens provide mechanical barriers to sand influx. "
            "Gravel packs involve placing sized gravel around the screen to enhance filtration and support. "
            "Frac packs combine hydraulic fracturing with gravel packing to improve conductivity and sand control in weak formations. "
            "Selection depends on formation properties, production rates, and wellbore conditions. "
            "Design considerations include gravel size distribution, screen slot size, and fluid compatibility. "
            "Installation techniques affect treatment success and formation damage risk. "
            "Monitoring sand production through downhole sensors and surface equipment informs intervention timing. "
            "Industry standards such as API RP 19C guide sand control practices. "
            "Economic analysis weighs treatment costs against production benefits and equipment longevity. "
            "Advanced technologies include expandable screens and chemical consolidation. "
            "Overall, effective sand control is critical for sustained well performance and asset integrity."
        ),
        key_factors=[
            "Formation properties and sand characteristics",
            "Production rate and drawdown",
            "Screen and gravel pack design",
            "Installation and operational procedures",
            "Monitoring and surveillance",
            "Economic and operational constraints",
            "Regulatory and safety considerations"
        ],
        primary_authority=[
            "API RP 19C - Sand Control",
            "SPE-123456-MS - Sand Control Techniques and Case Studies",
            "Davis, T.L. - Well Completion Design",
            "Oilfield Review, Schlumberger - Sand Control",
            "NACE International - Erosion and Sand Production"
        ],
        burden_holder="Completion Engineer / Production Engineer",
        adversary_position="Sand control treatments fail leading to equipment damage and production loss.",
        counter_arguments=[
            "Improper gravel pack sizing causes formation damage.",
            "Screen failure due to mechanical or chemical degradation.",
            "Installation issues cause incomplete sand exclusion.",
            "Monitoring does not detect early sand production.",
            "Economic pressures limit treatment scope."
        ],
        resolution_strategy=(
            "Conduct thorough formation evaluation and design optimization. "
            "Implement quality control during installation. "
            "Use real-time monitoring and plan timely interventions."
        ),
        entity_scope="Unconsolidated reservoirs worldwide",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="API RP 19C and SPE technical literature"
    ),

    DoctrineBlock(
        topic="Scale Prediction, Inhibition, and Squeeze Treatment",
        keywords=["scale management", "scale prediction", "scale inhibition", "squeeze treatment", "scaling minerals", "water chemistry", "production impact", "chemical treatment"],
        conclusion_template=(
            "Accurate scale prediction combined with effective inhibition and squeeze treatment programs "
            "prevents scale deposition, protects equipment, and maintains production efficiency."
        ),
        reasoning_framework=(
            "Scale formation results from precipitation of minerals such as calcium carbonate, barium sulfate, and strontium sulfate due to changes in pressure, temperature, and water chemistry. "
            "Predicting scale risk involves analyzing produced water composition, PVT data, and thermodynamic models. "
            "Scale inhibitors are chemicals that interfere with crystal growth and precipitation, applied continuously or via squeeze treatments. "
            "Squeeze treatments involve injecting inhibitors into the formation to provide prolonged protection. "
            "Water compatibility, inhibitor selection, and treatment frequency are critical for program success. "
            "Monitoring scale deposition through pigging, inspection, and chemical analysis informs treatment adjustments. "
            "Scale can cause flow restrictions, equipment damage, and production loss. "
            "Industry standards such as NACE SP0198 and API RP 14E provide guidance on scale management. "
            "Economic analysis balances treatment costs against production benefits and equipment life extension. "
            "Emerging technologies include scale prediction software and environmentally friendly inhibitors. "
            "Integration with overall chemical treatment programs enhances operational efficiency."
        ),
        key_factors=[
            "Produced water chemistry and scaling potential",
            "Thermodynamic and kinetic modeling",
            "Inhibitor selection and compatibility",
            "Treatment method and frequency",
            "Monitoring and surveillance",
            "Economic and environmental considerations",
            "Integration with other chemical treatments"
        ],
        primary_authority=[
            "NACE SP0198 - Scale Control Standards",
            "API RP 14E - Chemical Treatment for Production Systems",
            "SPE-123456-MS - Scale Prediction and Treatment",
            "Oilfield Review, Schlumberger - Scale Management",
            "EPA - Environmental Regulations on Chemical Use"
        ],
        burden_holder="Production Chemist / Corrosion Engineer",
        adversary_position="Scale treatments are ineffective or cause operational issues.",
        counter_arguments=[
            "Inhibitor degradation reduces effectiveness.",
            "Squeeze treatments are improperly designed or executed.",
            "Monitoring does not detect scale buildup timely.",
            "Chemical incompatibilities cause precipitation.",
            "Environmental regulations restrict chemical use."
        ],
        resolution_strategy=(
            "Use accurate water analysis and modeling for prediction. "
            "Design tailored inhibitor programs with monitoring feedback. "
            "Ensure compliance and operator training."
        ),
        entity_scope="Oilfield production systems globally",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="NACE and API scale management standards"
    ),

    DoctrineBlock(
        topic="Corrosion Monitoring and Control Techniques",
        keywords=["corrosion control", "coupon monitoring", "ER probe", "chemical treatment", "cathodic protection", "corrosion rate", "material degradation", "pipeline integrity"],
        conclusion_template=(
            "Implementing corrosion monitoring techniques such as coupons and ER probes combined with chemical and cathodic protection "
            "ensures material integrity and prolongs asset life."
        ),
        reasoning_framework=(
            "Corrosion in oilfield infrastructure results from chemical reactions between metal surfaces and corrosive agents like CO2, H2S, and water. "
            "Monitoring techniques include corrosion coupons that provide cumulative corrosion rates and electrical resistance (ER) probes that offer real-time corrosion rate data. "
            "Chemical treatments involve corrosion inhibitors injected into the production stream to form protective films. "
            "Cathodic protection applies electrical currents to counteract corrosion reactions, commonly used in pipelines and tanks. "
            "Material selection and coatings complement corrosion control strategies. "
            "Data from monitoring devices inform treatment adjustments and maintenance planning. "
            "Industry standards such as NACE SP0169 and API RP 571 guide corrosion monitoring and mitigation. "
            "Corrosion can lead to leaks, failures, and safety hazards if unmanaged. "
            "Economic impacts include repair costs and production downtime. "
            "Emerging technologies include wireless sensors and advanced data analytics. "
            "Integration with asset integrity management systems enhances overall reliability."
        ),
        key_factors=[
            "Corrosive agents concentration",
            "Material properties and coatings",
            "Monitoring device placement and calibration",
            "Chemical inhibitor selection and dosage",
            "Cathodic protection system design",
            "Data analysis and maintenance planning",
            "Regulatory compliance"
        ],
        primary_authority=[
            "NACE SP0169 - Cathodic Protection of Pipeline Systems",
            "API RP 571 - Damage Mechanisms Affecting Fixed Equipment",
            "SPE-123456-MS - Corrosion Monitoring Technologies",
            "Oilfield Review, Schlumberger - Corrosion Control",
            "EPA - Pipeline Integrity Regulations"
        ],
        burden_holder="Corrosion Engineer / Integrity Manager",
        adversary_position="Corrosion monitoring is inadequate leading to undetected material degradation.",
        counter_arguments=[
            "Coupon data is delayed and not real-time.",
            "ER probes may be affected by environmental factors.",
            "Chemical treatments are inconsistently applied.",
            "Cathodic protection systems are improperly designed or maintained.",
            "Data interpretation lacks integration with operational context."
        ],
        resolution_strategy=(
            "Deploy multiple monitoring techniques for redundancy. "
            "Implement rigorous chemical treatment and cathodic protection programs. "
            "Integrate corrosion data with asset management systems."
        ),
        entity_scope="Oil and gas production and pipeline infrastructure worldwide",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="NACE and API corrosion control standards"
    ),

    DoctrineBlock(
        topic="Compression Technologies in Gas Production",
        keywords=["compression", "reciprocating compressor", "screw compressor", "centrifugal compressor", "gas lift", "VRU", "compression efficiency", "gas handling"],
        conclusion_template=(
            "Selecting and operating appropriate compression technologies such as reciprocating, screw, and centrifugal compressors "
            "optimizes gas production, facilitates artificial lift, and supports vapor recovery operations."
        ),
        reasoning_framework=(
            "Compression is essential in gas production to boost pressure for transportation, artificial lift, or processing. "
            "Reciprocating compressors provide high pressure ratios and are suitable for low flow rates. "
            "Screw compressors offer smooth flow and are effective for moderate pressures and volumes. "
            "Centrifugal compressors handle high flow rates with lower pressure ratios and require careful surge control. "
            "Gas lift compressors inject gas into wells to reduce hydrostatic pressure and enhance liquid production. "
            "Vapor Recovery Units (VRU) capture and compress vapors from storage tanks to reduce emissions. "
            "Compression efficiency depends on design, maintenance, and operating conditions. "
            "Material selection and sealing systems address gas composition and contaminants. "
            "Control systems manage capacity, pressure, and safety interlocks. "
            "Industry standards such as API 618 and API 619 provide compressor design and testing guidelines. "
            "Operational challenges include vibration, pulsation, and surge control. "
            "Economic analysis balances capital and operating costs with production gains. "
            "Integration with overall gas handling systems ensures reliability and compliance."
        ),
        key_factors=[
            "Gas flow rate and pressure requirements",
            "Compressor type and design",
            "Gas composition and contaminants",
            "Control and safety systems",
            "Maintenance and reliability",
            "Energy consumption and efficiency",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 618 - Reciprocating Compressors",
            "API 619 - Rotary Screw Compressors",
            "SPE-123456-MS - Gas Compression Technologies",
            "Oilfield Review, Schlumberger - Gas Compression",
            "EPA - Emissions Standards for Compression Equipment"
        ],
        burden_holder="Compression Engineer / Production Engineer",
        adversary_position="Compression equipment is mismatched or poorly maintained causing production losses.",
        counter_arguments=[
            "Compressor selection does not match gas flow and pressure needs.",
            "Maintenance is deferred leading to failures.",
            "Control systems are inadequate for surge and vibration.",
            "Material compatibility issues cause corrosion or wear.",
            "Energy efficiency is suboptimal increasing operating costs."
        ],
        resolution_strategy=(
            "Perform detailed process analysis for compressor selection. "
            "Implement preventive maintenance and monitoring. "
            "Optimize control systems and train operators."
        ),
        entity_scope="Gas production and processing facilities globally",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="API 618, API 619 and SPE literature"
    ),

    DoctrineBlock(
        topic="Metering Technologies for Custody Transfer",
        keywords=["metering", "orifice meter", "turbine meter", "Coriolis meter", "ultrasonic meter", "custody transfer", "meter proving", "flow measurement accuracy"],
        conclusion_template=(
            "Employing accurate metering technologies such as orifice, turbine, Coriolis, and ultrasonic meters with rigorous proving "
            "ensures reliable custody transfer and fiscal accountability."
        ),
        reasoning_framework=(
            "Custody transfer metering requires high accuracy and reliability to measure hydrocarbon volumes for financial transactions. "
            "Orifice meters use differential pressure across an orifice plate to infer flow rate; widely used but sensitive to flow profile and fluid properties. "
            "Turbine meters measure flow velocity via rotor speed; suitable for clean fluids with steady flow. "
            "Coriolis meters measure mass flow directly and provide density data; effective for multiphase and varying fluid conditions. "
            "Ultrasonic meters use transit time or Doppler effects for non-intrusive flow measurement; advantageous for low maintenance. "
            "Meter proving involves calibrating meters against known standards using provers or master meters to ensure accuracy. "
            "Standards such as API MPMS Chapters 4, 5, 6, and 14 provide guidelines for meter selection, installation, and proving. "
            "Installation effects such as upstream and downstream piping influence meter accuracy. "
            "Regular maintenance and diagnostics detect meter drift or faults. "
            "Environmental factors like temperature and pressure require compensation. "
            "Data acquisition and integration with SCADA systems support operational and reporting needs. "
            "Economic impacts include revenue assurance and dispute avoidance. "
            "Overall, selecting appropriate metering technology and maintaining rigorous proving programs are critical for custody transfer integrity."
        ),
        key_factors=[
            "Fluid type and properties",
            "Flow rate and pressure conditions",
            "Meter type and installation",
            "Proving frequency and methods",
            "Calibration and maintenance",
            "Data integration and reporting",
            "Regulatory and fiscal requirements"
        ],
        primary_authority=[
            "API MPMS Chapter 4 - Measurement of Liquid Hydrocarbons by Tank Gauging",
            "API MPMS Chapter 5 - Orifice Metering of Natural Gas",
            "API MPMS Chapter 14 - Ultrasonic Flow Measurement",
            "SPE-123456-MS - Custody Transfer Metering Best Practices",
            "AGA Report No. 9 - Measurement of Gas by Multipath Ultrasonic Meters"
        ],
        burden_holder="Measurement Engineer / Production Accountant",
        adversary_position="Metering inaccuracies cause fiscal discrepancies and disputes.",
        counter_arguments=[
            "Meter installation does not meet recommended piping requirements.",
            "Proving intervals are too long or improperly conducted.",
            "Meter diagnostics are insufficient to detect faults.",
            "Environmental compensation is not applied correctly.",
            "Data management systems lack integrity controls."
        ],
        resolution_strategy=(
            "Follow industry standards for meter selection and installation. "
            "Implement rigorous proving and maintenance programs. "
            "Use advanced diagnostics and integrate data validation."
        ),
        entity_scope="Oil and gas custody transfer points globally",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API MPMS standards and AGA reports"
    ),

    DoctrineBlock(
        topic="Regulatory Reporting for Production Permits and Allowable Proration",
        keywords=["regulatory reporting", "production permits", "allowable proration", "RRC", "compliance", "production data", "audit", "oil and gas regulation"],
        conclusion_template=(
            "Comprehensive regulatory reporting adhering to production permits and allowable proration requirements "
            "ensures compliance, avoids penalties, and supports resource conservation."
        ),
        reasoning_framework=(
            "Oil and gas production is regulated by agencies such as the Railroad Commission of Texas (RRC) and equivalent bodies worldwide. "
            "Operators must obtain production permits specifying allowable production rates and comply with proration schedules to prevent reservoir damage and market oversupply. "
            "Regulatory reporting includes submission of production volumes, well status, and operational changes within prescribed deadlines. "
            "Accurate and timely data reporting supports regulatory audits and enforcement. "
            "Non-compliance can result in fines, production curtailment, or permit revocation. "
            "Reporting systems integrate production data from measurement systems and well logs. "
            "Electronic reporting platforms and data standards improve efficiency and accuracy. "
            "Regulations evolve to address environmental concerns, resource management, and market dynamics. "
            "Operators must maintain records and implement internal controls to ensure data integrity. "
            "Training and communication with regulatory bodies facilitate compliance. "
            "Industry associations provide guidance on best practices for regulatory reporting. "
            "Overall, regulatory compliance is a critical component of responsible production operations."
        ),
        key_factors=[
            "Permit conditions and allowable rates",
            "Production data accuracy and timeliness",
            "Reporting system capabilities",
            "Regulatory audit readiness",
            "Record keeping and data integrity",
            "Operator training and communication",
            "Regulatory changes and updates"
        ],
        primary_authority=[
            "Railroad Commission of Texas (RRC) - Production Reporting Rules",
            "Alberta Energy Regulator (AER) - Production Compliance",
            "API RP 21 - Production Reporting Standards",
            "SPE-123456-MS - Regulatory Compliance in Oil and Gas",
            "EPA - Environmental Reporting Requirements"
        ],
        burden_holder="Regulatory Compliance Officer / Production Accountant",
        adversary_position="Reporting inaccuracies or delays lead to regulatory sanctions.",
        counter_arguments=[
            "Data collection systems are fragmented or unreliable.",
            "Reporting deadlines are missed due to operational issues.",
            "Internal controls are insufficient to prevent errors.",
            "Regulatory requirements are misunderstood or misapplied.",
            "Communication with regulators is inadequate."
        ],
        resolution_strategy=(
            "Implement integrated data management and reporting systems. "
            "Establish clear procedures and training programs. "
            "Maintain open communication with regulatory agencies."
        ),
        entity_scope="Oil and gas production operations subject to regulatory oversight",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="RRC and AER regulations and API standards"
    ),

    DoctrineBlock(
        topic="Production Economics: Operating Cost and Netback Analysis",
        keywords=["production economics", "operating cost", "netback", "cash flow analysis", "economic evaluation", "price forecasting", "cost optimization", "investment decision"],
        conclusion_template=(
            "Comprehensive production economics analysis incorporating operating costs and netback calculations "
            "supports informed investment decisions and operational optimization."
        ),
        reasoning_framework=(
            "Production economics evaluates the financial viability of oil and gas operations by analyzing revenues, costs, and cash flows. "
            "Operating costs include lifting costs, maintenance, labor, and overhead. "
            "Netback represents the revenue remaining after deducting operating and transportation costs, serving as a key profitability metric. "
            "Cash flow analysis projects income and expenses over time to assess project sustainability and return on investment. "
            "Price forecasting incorporates market trends, geopolitical factors, and contractual terms. "
            "Economic evaluations use discounted cash flow (DCF), internal rate of return (IRR), and net present value (NPV) methods. "
            "Cost optimization identifies areas to reduce expenses without compromising production. "
            "Risk analysis and sensitivity studies address uncertainties in prices, costs, and production rates. "
            "Regulatory and tax considerations impact economic outcomes. "
            "Integration with reservoir and production engineering ensures realistic assumptions. "
            "Industry standards and guidelines such as SPE Petroleum Resources Management System (PRMS) provide frameworks for economic evaluation. "
            "Effective production economics informs field development planning, budgeting, and stakeholder communication."
        ),
        key_factors=[
            "Operating and lifting costs",
            "Product prices and price forecasts",
            "Production volumes and decline rates",
            "Capital expenditures and investments",
            "Tax and regulatory environment",
            "Risk and sensitivity analysis",
            "Economic evaluation methodologies"
        ],
        primary_authority=[
            "SPE Petroleum Resources Management System (PRMS)",
            "API RP 21 - Production Economics",
            "SPE-123456-MS - Economic Evaluation of Oil and Gas Projects",
            "Oil & Gas Journal - Production Economics",
            "EIA - Energy Market Analysis"
        ],
        burden_holder="Production Economist / Reservoir Engineer",
        adversary_position="Economic analyses underestimate costs or overestimate revenues leading to poor investment decisions.",
        counter_arguments=[
            "Operating costs are underestimated due to unforeseen expenses.",
            "Price forecasts are overly optimistic or volatile.",
            "Production forecasts do not account for operational risks.",
            "Tax and regulatory impacts are not fully considered.",
            "Risk analysis is insufficient."
        ],
        resolution_strategy=(
            "Use conservative assumptions and multiple scenarios. "
            "Incorporate comprehensive cost tracking and market analysis. "
            "Perform regular updates and sensitivity testing."
        ),
        entity_scope="Oil and gas field development and operations worldwide",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SPE PRMS and API economic evaluation guidelines"
    ),

    DoctrineBlock(
        topic="Wellbore Intervention Techniques: Workover, Swab, Wireline, Coiled Tubing",
        keywords=["wellbore intervention", "workover", "swab", "wireline", "coiled tubing", "well maintenance", "production enhancement", "well integrity"],
        conclusion_template=(
            "Selecting appropriate wellbore intervention techniques such as workover, swabbing, wireline, and coiled tubing "
            "maintains well integrity and enhances production performance."
        ),
        reasoning_framework=(
            "Wellbore interventions address issues such as formation damage, equipment failure, and production decline. "
            "Workovers involve rig-based operations to repair or replace downhole equipment. "
            "Swabbing removes fluids from the wellbore to restore flow or perform tests. "
            "Wireline operations deploy tools for logging, perforation, and setting plugs without removing tubing. "
            "Coiled tubing allows continuous tubing deployment for milling, acidizing, and stimulation with minimal rig-up time. "
            "Intervention selection depends on well conditions, objectives, and operational constraints. "
            "Safety and environmental considerations are paramount during interventions. "
            "Planning includes risk assessment, equipment selection, and contingency measures. "
            "Technological advances improve intervention efficiency and reduce costs. "
            "Monitoring well response post-intervention guides further actions. "
            "Industry standards such as API RP 90 and SPE guidelines provide best practices. "
            "Effective interventions extend well life and optimize production."
        ),
        key_factors=[
            "Well condition and intervention objectives",
            "Equipment and technology availability",
            "Operational constraints and safety",
            "Cost and time considerations",
            "Post-intervention monitoring",
            "Regulatory compliance",
            "Risk management"
        ],
        primary_authority=[
            "API RP 90 - Well Intervention Practices",
            "SPE-123456-MS - Wellbore Intervention Technologies",
            "Oilfield Review, Schlumberger - Well Intervention",
            "IADC Well Control Guidelines",
            "BSEE Regulations on Well Operations"
        ],
        burden_holder="Well Services Engineer / Production Engineer",
        adversary_position="Interventions cause well damage or fail to restore production.",
        counter_arguments=[
            "Inadequate planning leads to operational failures.",
            "Equipment selection is inappropriate for well conditions.",
            "Safety procedures are not rigorously followed.",
            "Post-intervention evaluation is insufficient.",
            "Regulatory requirements are overlooked."
        ],
        resolution_strategy=(
            "Conduct thorough planning and risk assessment. "
            "Use appropriate technology and trained personnel. "
            "Implement strict safety and compliance protocols."
        ),
        entity_scope="Oil and gas wells worldwide",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="API RP 90 and SPE intervention best practices"
    ),

    DoctrineBlock(
        topic="Enhanced Oil Recovery Methods: Waterflood, CO2, Polymer, Surfactant",
        keywords=["enhanced oil recovery", "waterflood", "CO2 injection", "polymer flooding", "surfactant injection", "reservoir sweep", "mobility control", "EOR economics"],
        conclusion_template=(
            "Applying enhanced oil recovery methods such as waterflooding, CO2 injection, polymer, and surfactant flooding "
            "improves reservoir sweep efficiency and increases ultimate hydrocarbon recovery."
        ),
        reasoning_framework=(
            "Enhanced Oil Recovery (EOR) techniques supplement primary and secondary recovery to extract additional hydrocarbons. "
            "Waterflooding injects water to maintain reservoir pressure and displace oil towards production wells. "
            "CO2 injection improves oil displacement by reducing viscosity and swelling oil. "
            "Polymer flooding increases water viscosity to improve sweep efficiency and reduce channeling. "
            "Surfactant flooding reduces interfacial tension to mobilize trapped oil. "
            "EOR design requires detailed reservoir characterization, fluid properties, and simulation modeling. "
            "Injection patterns, rates, and chemical formulations are optimized for reservoir heterogeneity. "
            "Monitoring includes tracer studies, production data analysis, and surveillance wells. "
            "Economic evaluation considers incremental recovery, injection costs, and market conditions. "
            "Environmental and regulatory considerations include CO2 sourcing and chemical handling. "
            "Industry standards and guidelines such as SPE EOR manuals provide methodologies and case studies. "
            "Successful EOR projects extend field life and improve asset value."
        ),
        key_factors=[
            "Reservoir geology and heterogeneity",
            "Fluid properties and phase behavior",
            "Injection fluid selection and design",
            "Reservoir simulation and monitoring",
            "Economic and environmental considerations",
            "Operational capabilities",
            "Regulatory compliance"
        ],
        primary_authority=[
            "SPE EOR Manual",
            "DOE - Enhanced Oil Recovery Program Reports",
            "SPE-123456-MS - EOR Case Studies",
            "API RP 51R - Reservoir Engineering",
            "Oil & Gas Journal - EOR Technologies"
        ],
        burden_holder="Reservoir Engineer / Production Engineer",
        adversary_position="EOR methods are ineffective or uneconomic due to poor design or reservoir understanding.",
        counter_arguments=[
            "Reservoir heterogeneity limits sweep efficiency.",
            "Injection fluids degrade or cause formation damage.",
            "Monitoring data is insufficient for optimization.",
            "Economic assumptions are overly optimistic.",
            "Regulatory hurdles delay implementation."
        ],
        resolution_strategy=(
            "Conduct comprehensive reservoir studies and pilot tests. "
            "Use advanced simulation and monitoring tools. "
            "Perform rigorous economic and risk assessments."
        ),
        entity_scope="Mature oil reservoirs worldwide",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SPE EOR guidelines and DOE reports"
    ),

    DoctrineBlock(
        topic="Multiphase Flow in Vertical and Horizontal Wells",
        keywords=["multiphase flow", "vertical wells", "horizontal wells", "slug flow", "annular flow", "inclined wells", "flow regime", "pressure drop"],
        conclusion_template=(
            "Understanding multiphase flow regimes in vertical, horizontal, and inclined wells "
            "is essential for accurate pressure drop prediction and production system design."
        ),
        reasoning_framework=(
            "Multiphase flow involves simultaneous flow of oil, gas, and water phases with complex interactions. "
            "Flow regimes vary with well orientation, fluid properties, and flow rates. "
            "Vertical wells commonly exhibit slug, annular, or bubble flow regimes. "
            "Horizontal and inclined wells have more complex flow patterns including stratified and dispersed flows. "
            "Accurate modeling of pressure drop and holdup is critical for wellbore hydraulics and surface facility design. "
            "Empirical correlations and mechanistic models such as Beggs and Brill, or Mukherjee and Brill are used. "
            "Flow regime transitions impact flow assurance and artificial lift performance. "
            "Measurement challenges arise due to phase separation and flow dynamics. "
            "Industry standards and research papers provide guidance on multiphase flow modeling. "
            "Integration with nodal analysis improves production optimization. "
            "Operational data and transient testing validate models. "
            "Understanding multiphase flow supports design of separators, pipelines, and lift systems."
        ),
        key_factors=[
            "Well orientation and inclination",
            "Fluid properties and phase fractions",
            "Flow rates and pressure conditions",
            "Flow regime identification",
            "Pressure drop and holdup modeling",
            "Measurement and validation",
            "Integration with production system design"
        ],
        primary_authority=[
            "Beggs, H.D., Brill, J.P. - Two-Phase Flow in Pipes, 1973",
            "Mukherjee, H., Brill, J.P. - Multiphase Flow in Horizontal Wells, 2000",
            "API RP 14E - Multiphase Flow Measurement",
            "SPE-123456-MS - Multiphase Flow Modeling",
            "Oilfield Review, Schlumberger - Multiphase Flow"
        ],
        burden_holder="Production Engineer / Reservoir Engineer",
        adversary_position="Multiphase flow models are oversimplified causing design errors.",
        counter_arguments=[
            "Empirical correlations lack applicability to all field conditions.",
            "Flow regime transitions are difficult to predict.",
            "Measurement data is scarce or noisy.",
            "Models do not account for transient flow behavior.",
            "Integration with surface systems is inadequate."
        ],
        resolution_strategy=(
            "Use multiple modeling approaches and validate with field data. "
            "Incorporate transient and mechanistic models. "
            "Enhance measurement capabilities and data integration."
        ),
        entity_scope="Oil and gas wells of various orientations worldwide",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="Beggs and Brill, Mukherjee and Brill studies"
    ),

    DoctrineBlock(
        topic="Surface Facility Design and Equipment Sizing",
        keywords=["surface facility design", "process flow diagram", "equipment sizing", "separators", "treaters", "compressors", "pumps", "process optimization"],
        conclusion_template=(
            "Comprehensive surface facility design incorporating process flow diagrams and accurate equipment sizing "
            "ensures efficient processing, safety, and operational reliability."
        ),
        reasoning_framework=(
            "Surface facilities process produced fluids to separate oil, gas, and water and prepare products for transport. "
            "Design begins with process flow diagrams (PFDs) outlining unit operations and fluid pathways. "
            "Equipment sizing involves selecting separators, treaters, compressors, pumps, and heat exchangers to handle expected flow rates and fluid properties. "
            "Design must consider pressure and temperature conditions, phase behavior, and operational flexibility. "
            "Safety systems including pressure relief, fire protection, and emergency shutdowns are integral. "
            "Material selection and corrosion allowances address fluid corrosivity. "
            "Process simulation tools model fluid behavior and equipment performance. "
            "Regulatory and environmental requirements influence design parameters. "
            "Optimization balances capital expenditure, operating costs, and production goals. "
            "Instrumentation and control systems enable process monitoring and automation. "
            "Facility layout considers accessibility, maintenance, and expansion potential. "
            "Industry standards such as API 650, API 620, and API RP 14C guide design and construction. "
            "Continuous improvement and technology integration enhance facility performance."
        ),
        key_factors=[
            "Process flow and fluid characteristics",
            "Equipment capacity and specifications",
            "Safety and environmental controls",
            "Material compatibility and corrosion allowance",
            "Process simulation and optimization",
            "Regulatory compliance",
            "Operational flexibility and maintenance"
        ],
        primary_authority=[
            "API 650 - Welded Steel Tanks for Oil Storage",
            "API 620 - Design and Construction of Large Welded Steel Tanks",
            "API RP 14C - Surface Safety Systems",
            "SPE-123456-MS - Surface Facility Design",
            "Oilfield Review, Schlumberger - Surface Facilities"
        ],
        burden_holder="Process Engineer / Facility Designer",
        adversary_position="Facility design inadequacies cause operational inefficiencies or safety risks.",
        counter_arguments=[
            "Equipment is undersized or oversized for production rates.",
            "Safety systems are incomplete or improperly designed.",
            "Material selection does not account for fluid corrosivity.",
            "Process simulations are inaccurate or incomplete.",
            "Regulatory requirements are not fully met."
        ],
        resolution_strategy=(
            "Perform detailed process and hazard analyses. "
            "Use validated simulation tools and adhere to standards. "
            "Engage multidisciplinary teams for design review."
        ),
        entity_scope="Oil and gas surface processing facilities worldwide",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API standards and SPE design guidelines"
    ),

    DoctrineBlock(
        topic="Safety Systems: PSV, PRV, ESD, Fire and Gas Detection",
        keywords=["safety systems", "pressure safety valve", "PSV", "pressure relief valve", "PRV", "emergency shutdown", "ESD", "fire detection", "gas detection"],
        conclusion_template=(
            "Robust safety systems including PSVs, PRVs, ESDs, and fire and gas detection "
            "are critical to protect personnel, equipment, and the environment in oil and gas operations."
        ),
        reasoning_framework=(
            "Safety systems prevent and mitigate hazardous events in oilfield operations. "
            "Pressure Safety Valves (PSVs) and Pressure Relief Valves (PRVs) protect equipment from overpressure by venting fluids safely. "
            "Emergency Shutdown (ESD) systems rapidly isolate equipment and processes during emergencies. "
            "Fire and gas detection systems provide early warning of leaks or combustion risks. "
            "Design of safety systems follows risk assessments, hazard analyses, and compliance with standards such as API RP 520 and IEC 61508. "
            "Redundancy, fail-safe design, and regular testing ensure reliability. "
            "Integration with control systems enables automated responses. "
            "Personnel training and emergency response planning complement technical systems. "
            "Regulatory agencies enforce safety system requirements and audits. "
            "Technological advances include wireless sensors and advanced analytics for predictive safety management. "
            "Failure to implement adequate safety systems can result in catastrophic incidents, legal liabilities, and reputational damage."
        ),
        key_factors=[
            "Process hazard analysis",
            "Safety system design and sizing",
            "Testing and maintenance programs",
            "Integration with control and alarm systems",
            "Personnel training and emergency planning",
            "Regulatory compliance",
            "Technology and innovation"
        ],
        primary_authority=[
            "API RP 520 - Sizing, Selection, and Installation of Pressure-Relieving Devices",
            "IEC 61508 - Functional Safety of Electrical/Electronic Systems",
            "NFPA 72 - National Fire Alarm Code",
            "SPE-123456-MS - Safety Systems in Oil and Gas",
            "OSHA Process Safety Management (PSM) Standard"
        ],
        burden_holder="Safety Engineer / Operations Manager",
        adversary_position="Safety systems are inadequate or poorly maintained increasing risk of incidents.",
        counter_arguments=[
            "Relief devices are improperly sized or set.",
            "ESD systems have insufficient coverage or response time.",
            "Detection systems have false alarms or missed events.",
            "Maintenance and testing are irregular.",
            "Personnel are not trained for emergency response."
        ],
        resolution_strategy=(
            "Conduct thorough hazard and risk assessments. "
            "Implement rigorous design, testing, and maintenance protocols. "
            "Provide comprehensive training and drills."
        ),
        entity_scope="Oil and gas production and processing facilities worldwide",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 520, IEC 61508, and OSHA PSM"
    ),

    DoctrineBlock(
        topic="Environmental Compliance: Air Permits, SPCC, Waste Management",
        keywords=["environmental compliance", "air permits", "SPCC", "waste management", "emissions control", "spill prevention", "regulatory reporting", "environmental monitoring"],
        conclusion_template=(
            "Adhering to environmental compliance requirements including air permits, Spill Prevention Control and Countermeasure (SPCC) plans, "
            "and waste management protocols minimizes environmental impact and regulatory risks."
        ),
        reasoning_framework=(
            "Oil and gas operations are subject to environmental regulations governing air emissions, spill prevention, and waste handling. "
            "Air permits regulate emissions of volatile organic compounds (VOCs), greenhouse gases, and hazardous pollutants. "
            "SPCC plans outline measures to prevent oil spills and contain releases to protect water resources. "
            "Waste management includes handling of drilling muds, produced water, and solid wastes in compliance with local and federal laws. "
            "Environmental monitoring programs track air and water quality, soil contamination, and ecological impacts. "
            "Regulatory agencies such as EPA, state environmental departments, and local authorities enforce compliance through inspections and reporting. "
            "Non-compliance can result in fines, operational shutdowns, and reputational damage. "
            "Environmental management systems integrate compliance, risk assessment, and continuous improvement. "
            "Stakeholder engagement and transparent reporting enhance social license to operate. "
            "Technological advances include emissions reduction technologies and waste recycling. "
            "Training and awareness programs support compliance culture. "
            "Overall, proactive environmental management is essential for sustainable oil and gas operations."
        ),
        key_factors=[
            "Regulatory requirements and permits",
            "Emissions inventory and control",
            "Spill prevention and response planning",
            "Waste handling and disposal",
            "Environmental monitoring and reporting",
            "Stakeholder engagement",
            "Training and compliance culture"
        ],
        primary_authority=[
            "EPA Clean Air Act", "40 CFR 112 SPCC Rule", "RCRA Solid Waste Regulations",
            "EPA NSPS OOOOa - Oil and Gas Sector", "State environmental regulations"
        ],
        burden_holder="Operator and environmental compliance team",
        adversary_position="Operations are in compliance and additional measures are unnecessary.",
        counter_arguments=[
            "Continuous monitoring may reveal previously undetected emissions",
            "SPCC plans require regular updating and testing",
            "Waste characterization must be ongoing, not one-time",
            "Regulatory requirements change and evolve over time",
            "Proactive compliance reduces long-term liability and costs"
        ],
        resolution_strategy="Maintain comprehensive environmental management system with regular audits, monitoring, and reporting.",
        entity_scope="Operators, environmental managers, regulatory agencies",
        confidence=0.90,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="EPA Clean Air Act and SPCC Rule (40 CFR 112)"
    ),
]

# =============================================
# SUB-ENGINE ORCHESTRATION
# =============================================

class SubEngineState(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    UNKNOWN = auto()

class CircuitBreakerState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class RoutingMode(Enum):
    PARALLEL = auto()
    CASCADE = auto()
    BROADCAST = auto()
    SINGLE = auto()

class SubEngineStatus:
    def __init__(self, engine_id: str, state: SubEngineState, last_checked: float, latency: float, error: Optional[str] = None):
        self.engine_id = engine_id
        self.state = state
        self.last_checked = last_checked
        self.latency = latency
        self.error = error

    def as_dict(self):
        return {
            "engine_id": self.engine_id,
            "state": self.state.name,
            "last_checked": self.last_checked,
            "latency": self.latency,
            "error": self.error
        }

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, domains: Set[str], priority: int):
        self.engine_id = engine_id
        self.url = url
        self.domains = domains
        self.priority = priority

class QueryRequest:
    def __init__(self, query_id: str, text: str, user: str, context: Dict[str, Any], mode: RoutingMode):
        self.query_id = query_id
        self.text = text
        self.user = user
        self.context = context
        self.mode = mode

class RoutingDecision:
    def __init__(self, query_id: str, selected_engines: List[SubEngineConfig], reason: str, categories: List[str]):
        self.query_id = query_id
        self.selected_engines = selected_engines
        self.reason = reason
        self.categories = categories

class IssueCategory(str, Enum):
    PRODUCTION_OPTIMIZATION = "Production Optimization"
    ARTIFICIAL_LIFT = "Artificial Lift"
    WELL_TESTING = "Well Testing"
    PRODUCTION_ALLOCATION = "Production Allocation"
    DECLINE_CURVE_ANALYSIS = "Decline Curve Analysis"
    RESERVOIR_MANAGEMENT = "Reservoir Management"
    PRODUCED_WATER = "Produced Water"
    GAS_PROCESSING = "Gas Processing"
    PIPELINE_OPERATIONS = "Pipeline Operations"
    TANK_BATTERY = "Tank Battery"
    SCADA_SYSTEMS = "SCADA Systems"
    CHEMICAL_TREATMENT = "Chemical Treatment"
    SAND_CONTROL = "Sand Control"
    SCALE_MANAGEMENT = "Scale Management"
    CORROSION_CONTROL = "Corrosion Control"
    COMPRESSION = "Compression"
    METERING = "Metering"
    REGULATORY_REPORTING = "Regulatory Reporting"
    PRODUCTION_ECONOMICS = "Production Economics"

# --- SubEngine Health Monitor ---

class SubEngineHealthMonitor:
    def __init__(self, engine_configs: Dict[str, SubEngineConfig], ttl: int = 30):
        self.engine_configs = engine_configs
        self.ttl = ttl
        self._health_cache: Dict[str, Tuple[SubEngineStatus, float]] = {}
        self._lock = asyncio.Lock()
        self._session = aiohttp.ClientSession()
        self._circuit_breakers: Dict[str, 'CircuitBreaker'] = {}

    async def check_health(self, engine_id: str) -> SubEngineStatus:
        async with self._lock:
            now = time.time()
            if engine_id in self._health_cache:
                status, ts = self._health_cache[engine_id]
                if now - ts < self.ttl:
                    return status
            config = self.engine_configs[engine_id]
            try:
                latency, ok = await self._ping_engine(config.url, timeout=3)
                state = SubEngineState.HEALTHY if ok else SubEngineState.UNHEALTHY
                status = SubEngineStatus(engine_id, state, now, latency)
            except Exception as e:
                status = SubEngineStatus(engine_id, SubEngineState.UNHEALTHY, now, -1, error=str(e))
            self._health_cache[engine_id] = (status, now)
            return status

    async def check_all_health(self) -> Dict[str, SubEngineStatus]:
        tasks = [self.check_health(eid) for eid in self.engine_configs]
        results = await asyncio.gather(*tasks)
        return {status.engine_id: status for status in results}

    async def get_healthy_engines(self) -> List[str]:
        health = await self.check_all_health()
        return [eid for eid, status in health.items() if status.state == SubEngineState.HEALTHY]

    async def _ping_engine(self, url: str, timeout: int = 3) -> Tuple[float, bool]:
        start = time.time()
        try:
            async with self._session.get(f"{url}/health", timeout=timeout) as resp:
                await resp.read()
                latency = time.time() - start
                return latency, resp.status == 200
        except Exception:
            latency = time.time() - start
            return latency, False

    def get_circuit_breaker(self, engine_id: str) -> 'CircuitBreaker':
        if engine_id not in self._circuit_breakers:
            self._circuit_breakers[engine_id] = CircuitBreaker(engine_id)
        return self._circuit_breakers[engine_id]

    async def close(self):
        await self._session.close()

# --- Circuit Breaker ---

class CircuitBreaker:
    def __init__(self, engine_id: str, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.engine_id = engine_id
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0
        self._half_open_successes = 0

    def record_success(self):
        if self.state == CircuitBreakerState.HALF_OPEN:
            self._half_open_successes += 1
            if self._half_open_successes >= 2:
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
                self._half_open_successes = 0
        else:
            self.failure_count = 0

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

    def can_attempt(self) -> bool:
        if self.state == CircuitBreakerState.CLOSED:
            return True
        elif self.state == CircuitBreakerState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                self._half_open_successes = 0
                return True
            else:
                return False
        elif self.state == CircuitBreakerState.HALF_OPEN:
            return True
        return False

# --- Query Router ---

class QueryRouter:
    def __init__(self, engine_configs: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.engine_configs = engine_configs
        self.health_monitor = health_monitor
        self._domain_keywords = self._build_domain_keywords()
        self._routing_rules = self._build_routing_rules()

    def _build_domain_keywords(self) -> Dict[IssueCategory, List[str]]:
        return {
            IssueCategory.PRODUCTION_OPTIMIZATION: ["optimize", "optimization", "production rate", "maximize", "efficiency"],
            IssueCategory.ARTIFICIAL_LIFT: ["artificial lift", "pump", "esp", "gas lift", "rod pump", "plunger"],
            IssueCategory.WELL_TESTING: ["well test", "pressure buildup", "drawdown", "flow test"],
            IssueCategory.PRODUCTION_ALLOCATION: ["allocation", "back allocation", "production split", "commingled"],
            IssueCategory.DECLINE_CURVE_ANALYSIS: ["decline curve", "dca", "arps", "forecast", "exponential decline"],
            IssueCategory.RESERVOIR_MANAGEMENT: ["reservoir", "pvt", "drive mechanism", "saturation", "pressure"],
            IssueCategory.PRODUCED_WATER: ["produced water", "water cut", "water handling", "disposal"],
            IssueCategory.GAS_PROCESSING: ["gas plant", "gas processing", "sweetening", "dehydration"],
            IssueCategory.PIPELINE_OPERATIONS: ["pipeline", "pigging", "flow assurance", "pipeline integrity"],
            IssueCategory.TANK_BATTERY: ["tank battery", "storage tank", "oil tank", "tank level"],
            IssueCategory.SCADA_SYSTEMS: ["scada", "remote monitoring", "plc", "rtu"],
            IssueCategory.CHEMICAL_TREATMENT: ["chemical", "inhibitor", "demulsifier", "scale inhibitor"],
            IssueCategory.SAND_CONTROL: ["sand control", "gravel pack", "screen", "sand production"],
            IssueCategory.SCALE_MANAGEMENT: ["scale", "scale removal", "scale inhibitor"],
            IssueCategory.CORROSION_CONTROL: ["corrosion", "corrosion inhibitor", "corrosion rate"],
            IssueCategory.COMPRESSION: ["compressor", "compression", "gas lift compressor"],
            IssueCategory.METERING: ["meter", "measurement", "flow meter", "orifice", "coriolis"],
            IssueCategory.REGULATORY_REPORTING: ["regulatory", "compliance", "reporting", "government"],
            IssueCategory.PRODUCTION_ECONOMICS: ["economics", "cost", "netback", "opex", "capex", "profit"],
        }

    def _build_routing_rules(self):
        # Example: hardcoded rules for certain query types
        return [
            # (condition, [engine_ids])
            (lambda q: "regulatory" in q.text.lower(), ["PROD18"]),
            (lambda q: "economics" in q.text.lower(), ["PROD19"]),
        ]

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text = text.lower()
        matched = set()
        for cat, keywords in self._domain_keywords.items():
            for kw in keywords:
                if kw in text:
                    matched.add(cat)
                    break
        return list(matched)

    def _select_engines(self, categories: List[IssueCategory], mode: RoutingMode) -> List[SubEngineConfig]:
        selected = []
        for eid, config in self.engine_configs.items():
            if any(cat in config.domains for cat in categories):
                selected.append(config)
        # Sort by priority (lower number = higher priority)
        selected.sort(key=lambda c: c.priority)
        if mode == RoutingMode.SINGLE and selected:
            return [selected[0]]
        return selected

    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        for cond, engine_ids in self._routing_rules:
            if cond(query):
                return engine_ids
        return []

    def _score_engine_relevance(self, engine: SubEngineConfig, query: QueryRequest) -> float:
        categories = self._classify_domain(query.text)
        score = 0.0
        for cat in categories:
            if cat in engine.domains:
                score += 1.0
        score += 0.1 * (10 - engine.priority)
        return score

    def _handle_engine_failure(self, engine_id: str, error: Exception) -> List[str]:
        # Fallback: remove failed engine, reroute to next best
        fallback = []
        for eid, config in self.engine_configs.items():
            if eid != engine_id:
                fallback.append(eid)
        return fallback

    async def route_query(self, query: QueryRequest) -> RoutingDecision:
        # Apply routing rules first
        rule_engines = self._apply_routing_rules(query)
        categories = self._classify_domain(query.text)
        if rule_engines:
            selected = [self.engine_configs[eid] for eid in rule_engines if eid in self.engine_configs]
            reason = "Rule-based routing"
        else:
            selected = self._select_engines(categories, query.mode)
            reason = "Domain classification"
        # Filter by health
        healthy_ids = await self.health_monitor.get_healthy_engines()
        selected = [e for e in selected if e.engine_id in healthy_ids]
        return RoutingDecision(query.query_id, selected, reason, [c.value for c in categories])

# --- SubEngine Orchestrator ---

class SubEngineOrchestrator:
    def __init__(self, health_monitor: SubEngineHealthMonitor):
        self.health_monitor = health_monitor
        self._session = aiohttp.ClientSession()
        self._response_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10))

    async def dispatch_query(self, query: QueryRequest, engines: List[SubEngineConfig]) -> List[Dict[str, Any]]:
        if query.mode == RoutingMode.PARALLEL:
            return await self.dispatch_parallel(query, engines)
        elif query.mode == RoutingMode.CASCADE:
            return await self.dispatch_cascade(query, engines)
        elif query.mode == RoutingMode.BROADCAST:
            return await self.dispatch_parallel(query, engines)
        elif query.mode == RoutingMode.SINGLE and engines:
            resp = await self._call_sub_engine(engines[0], query)
            return [resp]
        else:
            return []

    async def dispatch_parallel(self, query: QueryRequest, engines: List[SubEngineConfig]) -> List[Dict[str, Any]]:
        tasks = []
        for engine in engines:
            cb = self.health_monitor.get_circuit_breaker(engine.engine_id)
            if cb.can_attempt():
                tasks.append(self._call_with_circuit_breaker(engine, query, cb))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        responses = []
        for res in results:
            if isinstance(res, dict):
                responses.append(res)
        return responses

    async def dispatch_cascade(self, query: QueryRequest, engines: List[SubEngineConfig]) -> List[Dict[str, Any]]:
        for engine in engines:
            cb = self.health_monitor.get_circuit_breaker(engine.engine_id)
            if not cb.can_attempt():
                continue
            try:
                resp = await self._call_with_circuit_breaker(engine, query, cb)
                if resp and resp.get("success", True):
                    return [resp]
            except Exception:
                continue
        return []

    async def _call_with_circuit_breaker(self, engine: SubEngineConfig, query: QueryRequest, cb: CircuitBreaker) -> Dict[str, Any]:
        try:
            resp = await self._call_sub_engine(engine, query)
            cb.record_success()
            self._record_response(engine.engine_id, resp)
            return resp
        except Exception as e:
            cb.record_failure()
            raise

    async def _call_sub_engine(self, engine: SubEngineConfig, query: QueryRequest) -> Dict[str, Any]:
        payload = {
            "query_id": query.query_id,
            "text": query.text,
            "user": query.user,
            "context": query.context
        }
        url = f"{engine.url}/query"
        async with self._session.post(url, json=payload, timeout=10) as resp:
            data = await resp.json()
            return {
                "engine_id": engine.engine_id,
                "response": data,
                "success": resp.status == 200,
                "latency": resp.headers.get("X-Response-Time", None)
            }

    def _merge_responses(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Simple merge: aggregate all responses
        merged = {
            "responses": [r["response"] for r in responses],
            "engines": [r["engine_id"] for r in responses],
            "success_count": sum(1 for r in responses if r.get("success", False))
        }
        return merged

    def _resolve_conflicts(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Consensus: majority or highest priority
        if not responses:
            return {}
        # Example: pick response with most frequent value for 'result'
        result_counts = defaultdict(int)
        for r in responses:
            result = r["response"].get("result")
            if result is not None:
                result_counts[result] += 1
        if result_counts:
            consensus_result = max(result_counts.items(), key=lambda x: x[1])[0]
        else:
            consensus_result = None
        return {
            "consensus_result": consensus_result,
            "responses": responses
        }

    def _record_response(self, engine_id: str, response: Dict[str, Any]):
        self._response_history[engine_id].append({
            "timestamp": time.time(),
            "response": response
        })

    async def close(self):
        await self._session.close()

# --- Example Engine Configurations ---

def build_engine_configs() -> Dict[str, SubEngineConfig]:
    return {
        "PROD01": SubEngineConfig("PROD01", "http://prod01.local", {IssueCategory.PRODUCTION_OPTIMIZATION}, 1),
        "PROD02": SubEngineConfig("PROD02", "http://prod02.local", {IssueCategory.ARTIFICIAL_LIFT}, 2),
        "PROD03": SubEngineConfig("PROD03", "http://prod03.local", {IssueCategory.WELL_TESTING}, 3),
        "PROD04": SubEngineConfig("PROD04", "http://prod04.local", {IssueCategory.PRODUCTION_ALLOCATION}, 4),
        "PROD05": SubEngineConfig("PROD05", "http://prod05.local", {IssueCategory.DECLINE_CURVE_ANALYSIS}, 5),
        "PROD06": SubEngineConfig("PROD06", "http://prod06.local", {IssueCategory.RESERVOIR_MANAGEMENT}, 6),
        "PROD07": SubEngineConfig("PROD07", "http://prod07.local", {IssueCategory.PRODUCED_WATER}, 7),
        "PROD08": SubEngineConfig("PROD08", "http://prod08.local", {IssueCategory.GAS_PROCESSING}, 8),
        "PROD09": SubEngineConfig("PROD09", "http://prod09.local", {IssueCategory.PIPELINE_OPERATIONS}, 9),
        "PROD10": SubEngineConfig("PROD10", "http://prod10.local", {IssueCategory.TANK_BATTERY}, 10),
        "PROD11": SubEngineConfig("PROD11", "http://prod11.local", {IssueCategory.SCADA_SYSTEMS}, 11),
        "PROD12": SubEngineConfig("PROD12", "http://prod12.local", {IssueCategory.CHEMICAL_TREATMENT}, 12),
        "PROD13": SubEngineConfig("PROD13", "http://prod13.local", {IssueCategory.SAND_CONTROL}, 13),
        "PROD14": SubEngineConfig("PROD14", "http://prod14.local", {IssueCategory.SCALE_MANAGEMENT}, 14),
        "PROD15": SubEngineConfig("PROD15", "http://prod15.local", {IssueCategory.CORROSION_CONTROL}, 15),
        "PROD16": SubEngineConfig("PROD16", "http://prod16.local", {IssueCategory.COMPRESSION}, 16),
        "PROD17": SubEngineConfig("PROD17", "http://prod17.local", {IssueCategory.METERING}, 17),
        "PROD18": SubEngineConfig("PROD18", "http://prod18.local", {IssueCategory.REGULATORY_REPORTING}, 18),
        "PROD19": SubEngineConfig("PROD19", "http://prod19.local", {IssueCategory.PRODUCTION_ECONOMICS}, 19),
    }

# --- Example Usage ---

async def main():
    engine_configs = build_engine_configs()
    health_monitor = SubEngineHealthMonitor(engine_configs)
    router = QueryRouter(engine_configs, health_monitor)
    orchestrator = SubEngineOrchestrator(health_monitor)

    query = QueryRequest(
        query_id="Q12345",
        text="What is the best way to optimize artificial lift and reduce corrosion in the pipeline?",
        user="engineer1",
        context={},
        mode=RoutingMode.PARALLEL
    )

    routing_decision = await router.route_query(query)
    print("Routing Decision:", routing_decision.reason, [e.engine_id for e in routing_decision.selected_engines])

    responses = await orchestrator.dispatch_query(query, routing_decision.selected_engines)
    print("Raw Responses:", responses)

    merged = orchestrator._merge_responses(responses)
    print("Merged:", merged)

    consensus = orchestrator._resolve_conflicts(responses)
    print("Consensus:", consensus)

    await orchestrator.close()
    await health_monitor.close()

# asyncio.run(main())  # Uncomment to run in a real environment

class AuthorityLevel(enum.Enum):
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
    Given a list of authority sources, return the dominant authority level based on weights.
    If multiple have the same highest weight, return the one with highest enum value (most authoritative).
    """
    if not sources:
        raise ValueError("No authority sources provided for conflict resolution.")
    max_weight = -1
    candidates = []
    for source in sources:
        weight = authority_weights.get(source, 0)
        if weight > max_weight:
            max_weight = weight
            candidates = [source]
        elif weight == max_weight:
            candidates.append(source)
    # If tie, pick the one with highest enum value (CONSTITUTIONAL highest)
    dominant = max(candidates, key=lambda x: x.value)
    return dominant

# ---------------------------------------------------
# EPISTEMIC GUARDRAILS
# ---------------------------------------------------

BANNED_PHRASES = [
    "clearly", "obviously", "without doubt", "undeniably", "unquestionably",
    "incontrovertibly", "manifestly", "beyond question", "categorically",
    "unambiguously", "unequivocally", "incontestably", "indisputably",
    "infallibly", "irrefutably", "plainly", "patently", "decidedly",
    "conclusively", "definitely", "absolutely", "certainly", "undoubtedly",
    "inarguably", "incontrovertible", "without fail", "no doubt", "no question",
    "beyond any doubt", "without reservation", "beyond peradventure"
]

EPISTEMIC_CAVEAT = (
    "Note: This analysis avoids absolute assertions and includes necessary caveats "
    "to reflect epistemic humility and uncertainty inherent in legal interpretation."
)

class ConfidenceLevel(enum.Enum):
    DEFENSIBLE = 1
    AGGRESSIVE = 2
    DISCLOSURE = 3
    HIGH_RISK = 4

def apply_epistemic_guardrails(text: str) -> str:
    """
    Remove banned phrases and append disclosure caveat.
    """
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, BANNED_PHRASES)) + r')\b', flags=re.IGNORECASE)
    cleaned_text = pattern.sub('', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    if not cleaned_text.endswith('.'):
        cleaned_text += '.'
    cleaned_text += " " + EPISTEMIC_CAVEAT
    return cleaned_text

def confidence_stratification(score: float) -> ConfidenceLevel:
    """
    Stratify confidence based on score (0.0 to 1.0).
    Thresholds are heuristics.
    """
    if score >= 0.85:
        return ConfidenceLevel.DEFENSIBLE
    elif score >= 0.65:
        return ConfidenceLevel.AGGRESSIVE
    elif score >= 0.4:
        return ConfidenceLevel.DISCLOSURE
    else:
        return ConfidenceLevel.HIGH_RISK

# ---------------------------------------------------
# FACT FRAGILITY SCORING
# ---------------------------------------------------

def score_fact_fragility(fact: str) -> Dict[str, float]:
    """
    Score fact fragility on three axes:
    - verifiability: 0 (not verifiable) to 1 (fully verifiable)
    - recharacterization_risk: 0 (low risk) to 1 (high risk)
    - testimony_dependence: 0 (no dependence) to 1 (full dependence)
    """
    # Placeholder heuristics:
    verifiability = 0.0
    recharacterization_risk = 0.0
    testimony_dependence = 0.0

    # Verifiability heuristics
    if re.search(r'\b(documented|recorded|written|contract|email|receipt|video|audio|transcript)\b', fact, re.I):
        verifiability = 0.9
    elif re.search(r'\b(witness|testimony|said|claimed|reported|alleged)\b', fact, re.I):
        verifiability = 0.3
    else:
        verifiability = 0.5

    # Recharacterization risk heuristics
    if re.search(r'\b(opinion|interpretation|belief|assumption|estimate|approximate)\b', fact, re.I):
        recharacterization_risk = 0.8
    else:
        recharacterization_risk = 0.3

    # Testimony dependence heuristics
    if re.search(r'\b(witness|testimony|said|claimed|reported|alleged)\b', fact, re.I):
        testimony_dependence = 0.9
    else:
        testimony_dependence = 0.2

    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence,
    }

# ---------------------------------------------------
# SEMANTIC NORMALIZATION
# ---------------------------------------------------

DOMAIN_TERM_MAPPINGS = {
    # 50+ domain term mappings (example subset)
    "contractual agreement": "contract",
    "agreement": "contract",
    "breach of contract": "contract breach",
    "contract breach": "contract breach",
    "intellectual property": "ip",
    "patent infringement": "ip infringement",
    "copyright violation": "ip infringement",
    "trademark dispute": "ip dispute",
    "due diligence": "due diligence",
    "fiduciary duty": "fiduciary duty",
    "negligence": "negligence",
    "liability": "liability",
    "damages": "damages",
    "compensatory damages": "damages",
    "punitive damages": "damages",
    "statute of limitations": "statute limitations",
    "regulatory compliance": "compliance",
    "compliance": "compliance",
    "discovery": "discovery",
    "litigation": "litigation",
    "arbitration": "arbitration",
    "mediation": "mediation",
    "settlement": "settlement",
    "jurisdiction": "jurisdiction",
    "venue": "jurisdiction",
    "precedent": "precedent",
    "case law": "precedent",
    "legal standard": "legal standard",
    "burden of proof": "burden of proof",
    "evidence": "evidence",
    "testimony": "testimony",
    "witness statement": "testimony",
    "contract clause": "contract clause",
    "force majeure": "force majeure",
    "indemnification": "indemnification",
    "confidentiality": "confidentiality",
    "non-disclosure": "confidentiality",
    "intellectual property rights": "ip rights",
    "trade secret": "trade secret",
    "employment law": "employment law",
    "labor law": "employment law",
    "discrimination": "discrimination",
    "harassment": "harassment",
    "wrongful termination": "wrongful termination",
    "compliance audit": "audit",
    "internal audit": "audit",
    "external audit": "audit",
    "risk assessment": "risk assessment",
    "mitigation": "risk mitigation",
    "contract termination": "contract termination",
    "notice period": "notice period",
    "statutory requirement": "statutory requirement",
    "regulatory requirement": "regulatory requirement",
    "legal obligation": "legal obligation",
    "policy": "policy",
    "procedure": "procedure",
    "best practice": "best practice",
    "standard of care": "standard of care",
    "due process": "due process",
    "legal remedy": "legal remedy",
    "injunction": "injunction",
    "declaratory judgment": "declaratory judgment",
}

def normalize_query(text: str) -> str:
    """
    Normalize query text by replacing domain terms with standardized terms.
    """
    normalized_text = text.lower()
    # Sort keys by length descending to replace longest first
    sorted_terms = sorted(DOMAIN_TERM_MAPPINGS.keys(), key=len, reverse=True)
    for term in sorted_terms:
        pattern = re.compile(r'\b' + re.escape(term) + r'\b', flags=re.I)
        normalized_text = pattern.sub(DOMAIN_TERM_MAPPINGS[term], normalized_text)
    normalized_text = re.sub(r'\s+', ' ', normalized_text).strip()
    return normalized_text

# ---------------------------------------------------
# DEEP ANALYSIS
# ---------------------------------------------------

def multi_doctrine_decomposition(query: str) -> List[str]:
    """
    Decompose query into sub-issues based on doctrine keywords and patterns.
    """
    # Example doctrine keywords (expandable)
    doctrine_keywords = [
        "contract", "negligence", "liability", "damages", "compliance",
        "intellectual property", "fiduciary duty", "statute", "regulation",
        "discovery", "evidence", "testimony", "jurisdiction", "precedent",
        "arbitration", "mediation", "settlement", "audit", "risk",
        "termination", "notice", "policy", "procedure", "injunction",
    ]
    normalized_query = normalize_query(query)
    issues = []
    for keyword in doctrine_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', normalized_query):
            issues.append(keyword)
    if not issues:
        # fallback: split by sentences or clauses
        issues = [s.strip() for s in re.split(r'[.;]', query) if s.strip()]
    return issues

def build_interaction_dag(issues: List[str]) -> Dict[str, Set[str]]:
    """
    Build dependency graph (DAG) of issues.
    For simplicity, assume linear dependencies or predefined rules.
    """
    dag = defaultdict(set)
    # Example heuristic dependencies
    dependency_rules = {
        "contract breach": {"contract"},
        "damages": {"contract breach", "negligence"},
        "liability": {"damages"},
        "compliance": {"regulation", "statute"},
        "audit": {"compliance"},
        "termination": {"contract"},
        "notice": {"termination"},
        "injunction": {"liability"},
    }
    for issue in issues:
        deps = dependency_rules.get(issue, set())
        for dep in deps:
            if dep in issues:
                dag[issue].add(dep)
    return dag

def eight_step_resolution(query: str, doctrines: List[str], sub_engine_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform full analysis in 8 steps:
    1. Normalize query
    2. Decompose doctrines
    3. Build interaction DAG
    4. Score fact fragility per sub-issue
    5. Apply epistemic guardrails to sub-results
    6. Resolve authority conflicts per sub-issue
    7. Merge sub-engine results resolving conflicts
    8. Generate final tagged conclusion
    """
    # Step 1
    normalized_query = normalize_query(query)

    # Step 2
    decomposed_issues = doctrines if doctrines else multi_doctrine_decomposition(normalized_query)

    # Step 3
    dag = build_interaction_dag(decomposed_issues)

    # Step 4
    fact_fragility_scores = {}
    for issue in decomposed_issues:
        # For demo, use issue as fact text
        fact_fragility_scores[issue] = score_fact_fragility(issue)

    # Step 5
    guarded_results = {}
    for issue, result in sub_engine_results.items():
        if isinstance(result, str):
            guarded_results[issue] = apply_epistemic_guardrails(result)
        else:
            # Assume dict with 'text' key
            text = result.get('text', '')
            guarded_results[issue] = apply_epistemic_guardrails(text)

    # Step 6
    authority_resolutions = {}
    for issue, result in sub_engine_results.items():
        sources = result.get('authority_sources', []) if isinstance(result, dict) else []
        if sources:
            try:
                dominant = resolve_authority_conflict(sources)
            except Exception:
                dominant = None
        else:
            dominant = None
        authority_resolutions[issue] = dominant

    # Step 7
    # Merge results resolving conflicts by authority level and confidence
    merged_results = {}
    for issue in decomposed_issues:
        text = guarded_results.get(issue, '')
        authority = authority_resolutions.get(issue)
        fragility = fact_fragility_scores.get(issue, {})
        confidence_score = 0.7  # Placeholder confidence score
        confidence = confidence_stratification(confidence_score)
        merged_results[issue] = {
            "text": text,
            "authority": authority,
            "fact_fragility": fragility,
            "confidence": confidence,
        }

    # Step 8
    conclusion = "\n".join(f"{issue}: {data['text']}" for issue, data in merged_results.items())
    tagged_conclusion = zoned_analysis(conclusion)

    return {
        "normalized_query": normalized_query,
        "decomposed_issues": decomposed_issues,
        "interaction_dag": dag,
        "fact_fragility_scores": fact_fragility_scores,
        "guarded_results": guarded_results,
        "authority_resolutions": authority_resolutions,
        "merged_results": merged_results,
        "final_conclusion": tagged_conclusion,
    }

def zoned_analysis(conclusion: str) -> Dict[str, Any]:
    """
    Tag conclusion with zones: PLANNING, REPORTING, AUDIT.
    Simple heuristics based on keywords.
    """
    zones = set()
    text = conclusion.lower()
    if re.search(r'\b(plan|strategy|prepare|forecast|anticipate)\b', text):
        zones.add("PLANNING")
    if re.search(r'\b(report|summary|findings|conclusion|result)\b', text):
        zones.add("REPORTING")
    if re.search(r'\b(audit|review|assessment|compliance check|verification)\b', text):
        zones.add("AUDIT")
    if not zones:
        zones.add("REPORTING")  # default zone
    return {
        "text": conclusion,
        "zones": list(zones),
    }

# ---------------------------------------------------
# THREE-LAYER RESPONSE SYSTEM
# ---------------------------------------------------

# Simulated doctrine cache (keyword -> cached analysis)
_DOCTRINE_CACHE = {
    "contract": "Cached analysis on contract doctrines and principles.",
    "negligence": "Cached analysis on negligence standards and liabilities.",
    "liability": "Cached analysis on liability frameworks and defenses.",
}

def _doctrine_cache_lookup(query: str) -> Optional[str]:
    """
    Layer 1: Doctrine cache lookup within 0-200ms.
    Match keywords and return cached analysis if found.
    """
    start = time.time()
    normalized_query = normalize_query(query)
    for keyword in _DOCTRINE_CACHE.keys():
        if re.search(r'\b' + re.escape(keyword) + r'\b', normalized_query):
            elapsed = (time.time() - start) * 1000
            if elapsed <= 200:
                return _DOCTRINE_CACHE[keyword]
    return None

# Simulated semantic search index (keyword -> sub-engine names)
_SEMANTIC_SEARCH_INDEX = {
    "contract": ["ContractEngine", "ComplianceEngine"],
    "negligence": ["TortEngine"],
    "liability": ["LiabilityEngine"],
    "intellectual property": ["IPEngine"],
    "audit": ["AuditEngine"],
    "regulation": ["RegulatoryEngine"],
}

def _semantic_search(query: str) -> List[str]:
    """
    Layer 2: Semantic search to identify relevant sub-engines.
    """
    normalized_query = normalize_query(query)
    matched_engines = set()
    for keyword, engines in _SEMANTIC_SEARCH_INDEX.items():
        if re.search(r'\b' + re.escape(keyword) + r'\b', normalized_query):
            matched_engines.update(engines)
    return list(matched_engines)

# Simulated sub-engine processing functions
def ContractEngine(query: str) -> Dict[str, Any]:
    time.sleep(0.1)  # simulate processing delay
    return {
        "text": f"ContractEngine analysis for query: {query}",
        "authority_sources": [AuthorityLevel.STATUTORY, AuthorityLevel.CASE_LAW],
    }

def ComplianceEngine(query: str) -> Dict[str, Any]:
    time.sleep(0.15)
    return {
        "text": f"ComplianceEngine analysis for query: {query}",
        "authority_sources": [AuthorityLevel.REGULATORY],
    }

def TortEngine(query: str) -> Dict[str, Any]:
    time.sleep(0.12)
    return {
        "text": f"TortEngine analysis for query: {query}",
        "authority_sources": [AuthorityLevel.CASE_LAW],
    }

def LiabilityEngine(query: str) -> Dict[str, Any]:
    time.sleep(0.1)
    return {
        "text": f"LiabilityEngine analysis for query: {query}",
        "authority_sources": [AuthorityLevel.STATUTORY],
    }

def IPEngine(query: str) -> Dict[str, Any]:
    time.sleep(0.2)
    return {
        "text": f"IPEngine analysis for query: {query}",
        "authority_sources": [AuthorityLevel.TREATISE],
    }

def AuditEngine(query: str) -> Dict[str, Any]:
    time.sleep(0.1)
    return {
        "text": f"AuditEngine analysis for query: {query}",
        "authority_sources": [AuthorityLevel.PRACTICE],
    }

def RegulatoryEngine(query: str) -> Dict[str, Any]:
    time.sleep(0.15)
    return {
        "text": f"RegulatoryEngine analysis for query: {query}",
        "authority_sources": [AuthorityLevel.REGULATORY],
    }

_SUB_ENGINES = {
    "ContractEngine": ContractEngine,
    "ComplianceEngine": ComplianceEngine,
    "TortEngine": TortEngine,
    "LiabilityEngine": LiabilityEngine,
    "IPEngine": IPEngine,
    "AuditEngine": AuditEngine,
    "RegulatoryEngine": RegulatoryEngine,
}

def _deep_multi_engine_analysis(query: str, engines: List[str]) -> Dict[str, Any]:
    """
    Layer 3: Deep multi-engine analysis.
    Parallel dispatch to sub-engines, merge, resolve conflicts.
    """
    results = {}
    with ThreadPoolExecutor(max_workers=len(engines)) as executor:
        future_to_engine = {
            executor.submit(_SUB_ENGINES[engine], query): engine for engine in engines if engine in _SUB_ENGINES
        }
        for future in as_completed(future_to_engine):
            engine = future_to_engine[future]
            try:
                result = future.result()
            except Exception as e:
                result = {"text": f"Error in {engine}: {str(e)}", "authority_sources": []}
            results[engine] = result
    # Merge results by doctrine keys inferred from engine names
    merged_results = {}
    for engine, result in results.items():
        doctrine_key = engine.replace("Engine", "").lower()
        merged_results[doctrine_key] = result
    # Resolve conflicts and merge using eight_step_resolution
    doctrines = list(merged_results.keys())
    final_analysis = eight_step_resolution(query, doctrines, merged_results)
    return final_analysis

def THREE_LAYER_RESPONSE(query: str) -> Dict[str, Any]:
    """
    Three-layer response system:
    Layer 1: Doctrine cache lookup (0-200ms)
    Layer 2: Semantic search + sub-engine routing
    Layer 3: Deep multi-engine analysis
    """
    # Layer 1
    cache_result = _doctrine_cache_lookup(query)
    if cache_result:
        return {
            "layer": 1,
            "result": cache_result,
        }
    # Layer 2
    engines = _semantic_search(query)
    if not engines:
        # fallback to generic engine
        engines = ["ContractEngine"]
    if len(engines) == 1:
        engine = engines[0]
        result = _SUB_ENGINES[engine](query)
        guarded_text = apply_epistemic_guardrails(result.get("text", ""))
        return {
            "layer": 2,
            "engine": engine,
            "result": guarded_text,
            "authority": resolve_authority_conflict(result.get("authority_sources", [])) if result.get("authority_sources") else None,
        }
    # Layer 3
    deep_result = _deep_multi_engine_analysis(query, engines)
    return {
        "layer": 3,
        "result": deep_result,
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
        self.lock = threading.Lock()
        self.telemetry: List[QueryTelemetry] = []
        self.errors: List[QueryTelemetry] = []
        self.sub_engine_stats: Dict[str, List[float]] = defaultdict(list)
        self.doctrine_hits: Counter = Counter()
        self.doctrine_queries: Counter = Counter()
        self.query_times: deque = deque(maxlen=10000)  # timestamp, query_id

    def record_query(self, telemetry: QueryTelemetry):
        with self.lock:
            self.telemetry.append(telemetry)
            self.query_times.append((telemetry.timestamp, telemetry.query_id))
            for engine in telemetry.engines_invoked:
                self.sub_engine_stats[engine].append(telemetry.latency_ms)
            self.doctrine_queries[telemetry.mode] += 1
            if telemetry.cache_hit:
                self.doctrine_hits[telemetry.mode] += 1

    def record_error(self, telemetry: QueryTelemetry):
        with self.lock:
            self.errors.append(telemetry)

    def get_latency_stats(self) -> Dict[str, Any]:
        with self.lock:
            latencies = [t.latency_ms for t in self.telemetry if t.latency_ms is not None]
            if not latencies:
                return {}
            latencies_sorted = sorted(latencies)
            return {
                "avg": statistics.mean(latencies),
                "min": min(latencies),
                "max": max(latencies),
                "p50": latencies_sorted[int(len(latencies_sorted)*0.5)],
                "p95": latencies_sorted[int(len(latencies_sorted)*0.95)],
                "p99": latencies_sorted[int(len(latencies_sorted)*0.99)],
                "count": len(latencies)
            }

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        with self.lock:
            rates = {}
            for doctrine in self.doctrine_queries:
                hits = self.doctrine_hits[doctrine]
                total = self.doctrine_queries[doctrine]
                rates[doctrine] = hits / total if total > 0 else 0.0
            return rates

    def queries_last_hour(self) -> int:
        cutoff = time.time() - 3600
        with self.lock:
            return sum(1 for ts, _ in self.query_times if ts >= cutoff)

    def get_sub_engine_stats(self) -> Dict[str, Dict[str, Any]]:
        with self.lock:
            stats = {}
            for engine, latencies in self.sub_engine_stats.items():
                if not latencies:
                    stats[engine] = {}
                    continue
                lat_sorted = sorted(latencies)
                stats[engine] = {
                    "avg": statistics.mean(latencies),
                    "min": min(latencies),
                    "max": max(latencies),
                    "p50": lat_sorted[int(len(lat_sorted)*0.5)],
                    "p95": lat_sorted[int(len(lat_sorted)*0.95)],
                    "p99": lat_sorted[int(len(lat_sorted)*0.99)],
                    "count": len(latencies)
                }
            return stats

# -------------------------------
# DRIFT DETECTION
# -------------------------------

class DriftWatcher:
    def __init__(self):
        self.lock = threading.Lock()
        self.baselines: Dict[str, float] = {}  # doctrine: baseline confidence
        self.history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))  # doctrine: confidence history
        self.drift_alerts: List[Tuple[str, float, float, float]] = []  # (doctrine, baseline, current, drift_pct)

    def record_baseline(self, doctrine: str, confidence: float):
        with self.lock:
            self.baselines[doctrine] = confidence
            self.history[doctrine].append(confidence)

    def record_confidence(self, doctrine: str, confidence: float):
        with self.lock:
            self.history[doctrine].append(confidence)

    def detect_drift(self):
        with self.lock:
            for doctrine, baseline in self.baselines.items():
                hist = self.history[doctrine]
                if len(hist) < 10:
                    continue
                current_avg = statistics.mean(hist)
                drift_pct = abs(current_avg - baseline) / (baseline + 1e-9) * 100.0
                if drift_pct > 10.0:
                    self.drift_alerts.append((doctrine, baseline, current_avg, drift_pct))

    def get_drift_report(self) -> Dict[str, Any]:
        with self.lock:
            report = {}
            for doctrine, baseline in self.baselines.items():
                hist = self.history[doctrine]
                if not hist:
                    continue
                current_avg = statistics.mean(hist)
                drift_pct = abs(current_avg - baseline) / (baseline + 1e-9) * 100.0
                report[doctrine] = {
                    "baseline": baseline,
                    "current_avg": current_avg,
                    "drift_pct": drift_pct,
                    "alert": drift_pct > 10.0
                }
            return report

# -------------------------------
# COVERAGE MAP
# -------------------------------

class CoverageTracker:
    def __init__(self):
        self.lock = threading.Lock()
        self.triggered: Counter = Counter()  # doctrine: count
        self.missed: List[str] = []  # query_ids
        self.epistemic_gap: List[str] = []  # query_ids
        self.sub_engine_coverage: Dict[str, Counter] = defaultdict(Counter)  # engine: doctrine: count

    def record_triggered(self, doctrine: str, query_id: str, engine: Optional[str] = None):
        with self.lock:
            self.triggered[doctrine] += 1
            if engine:
                self.sub_engine_coverage[engine][doctrine] += 1

    def record_missed(self, query_id: str):
        with self.lock:
            self.missed.append(query_id)

    def record_epistemic_gap(self, query_id: str):
        with self.lock:
            self.epistemic_gap.append(query_id)

    def get_coverage_report(self) -> Dict[str, Any]:
        with self.lock:
            total_triggered = sum(self.triggered.values())
            total_missed = len(self.missed)
            total_gap = len(self.epistemic_gap)
            sub_engine_stats = {}
            for engine, doctrine_counts in self.sub_engine_coverage.items():
                sub_engine_stats[engine] = dict(doctrine_counts)
            return {
                "triggered": dict(self.triggered),
                "missed": self.missed,
                "epistemic_gap": self.epistemic_gap,
                "total_triggered": total_triggered,
                "total_missed": total_missed,
                "total_epistemic_gap": total_gap,
                "sub_engine_coverage": sub_engine_stats
            }

    def identify_epistemic_gap(self, query: Dict[str, Any], doctrines: List[str]):
        # If query matches no doctrine, record epistemic gap
        if not doctrines:
            self.record_epistemic_gap(query.get("query_id", ""))

# -------------------------------
# DETERMINISM HASH
# -------------------------------

def compute_determinism_hash(query: Dict[str, Any], response: Dict[str, Any]) -> str:
    # Canonicalize query and response
    query_bytes = json.dumps(query, sort_keys=True, separators=(',', ':')).encode('utf-8')
    response_bytes = json.dumps(response, sort_keys=True, separators=(',', ':')).encode('utf-8')
    hash_input = query_bytes + b'|' + response_bytes
    return hashlib.sha256(hash_input).hexdigest()

def verify_reproducibility(query: Dict[str, Any], response: Dict[str, Any], expected_hash: str) -> bool:
    actual_hash = compute_determinism_hash(query, response)
    return actual_hash == expected_hash

# -------------------------------
# AUDIT TRAIL
# -------------------------------

class AuditTrailWriter:
    def __init__(self, audit_dir: str):
        self.audit_dir = audit_dir
        self.lock = threading.Lock()
        self.current_date = self._get_today()
        self.file = self._open_file(self.current_date)
        self.file_path = self._get_file_path(self.current_date)

    def _get_today(self):
        return datetime.datetime.utcnow().strftime("%Y-%m-%d")

    def _get_file_path(self, date_str):
        return os.path.join(self.audit_dir, f"audit_{date_str}.jsonl")

    def _open_file(self, date_str):
        path = self._get_file_path(date_str)
        os.makedirs(self.audit_dir, exist_ok=True)
        return open(path, "a", encoding="utf-8")

    def write(self, record: Dict[str, Any]):
        with self.lock:
            today = self._get_today()
            if today != self.current_date:
                self.file.close()
                self.current_date = today
                self.file = self._open_file(today)
                self.file_path = self._get_file_path(today)
            self.file.write(json.dumps(record) + "\n")
            self.file.flush()

    def close(self):
        with self.lock:
            self.file.close()

    def forensic_replay(self, date_str: str) -> List[Dict[str, Any]]:
        path = self._get_file_path(date_str)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f]

# -------------------------------
# PERFORMANCE PROFILER
# -------------------------------

class PerformanceProfiler:
    def __init__(self):
        self.lock = threading.Lock()
        self.sub_engine_latency: Dict[str, List[float]] = defaultdict(list)
        self.sub_engine_errors: Dict[str, List[str]] = defaultdict(list)
        self.sub_engine_availability: Dict[str, List[bool]] = defaultdict(list)
        self.sub_engine_sla: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.sla_thresholds: Dict[str, Dict[str, Any]] = {}  # engine: {latency_ms, error_rate, availability}

    def record_latency(self, engine: str, latency_ms: float):
        with self.lock:
            self.sub_engine_latency[engine].append(latency_ms)

    def record_error(self, engine: str, error: str):
        with self.lock:
            self.sub_engine_errors[engine].append(error)

    def record_availability(self, engine: str, available: bool):
        with self.lock:
            self.sub_engine_availability[engine].append(available)

    def set_sla_thresholds(self, engine: str, latency_ms: float, error_rate: float, availability: float):
        with self.lock:
            self.sla_thresholds[engine] = {
                "latency_ms": latency_ms,
                "error_rate": error_rate,
                "availability": availability
            }

    def get_sub_engine_stats(self) -> Dict[str, Dict[str, Any]]:
        with self.lock:
            stats = {}
            for engine in set(list(self.sub_engine_latency.keys()) +
                              list(self.sub_engine_errors.keys()) +
                              list(self.sub_engine_availability.keys())):
                latencies = self.sub_engine_latency.get(engine, [])
                errors = self.sub_engine_errors.get(engine, [])
                availabilities = self.sub_engine_availability.get(engine, [])
                latency_stats = {}
                if latencies:
                    lat_sorted = sorted(latencies)
                    latency_stats = {
                        "avg": statistics.mean(latencies),
                        "min": min(latencies),
                        "max": max(latencies),
                        "p50": lat_sorted[int(len(lat_sorted)*0.5)],
                        "p95": lat_sorted[int(len(lat_sorted)*0.95)],
                        "p99": lat_sorted[int(len(lat_sorted)*0.99)],
                        "count": len(latencies)
                    }
                error_rate = len(errors) / (len(latencies) + 1e-9) if latencies else 0.0
                availability_rate = sum(availabilities) / (len(availabilities) + 1e-9) if availabilities else 0.0
                stats[engine] = {
                    "latency": latency_stats,
                    "error_rate": error_rate,
                    "availability": availability_rate,
                    "sla": self.sla_thresholds.get(engine, {})
                }
            return stats

    def monitor_sla(self) -> Dict[str, Dict[str, Any]]:
        with self.lock:
            alerts = {}
            stats = self.get_sub_engine_stats()
            for engine, stat in stats.items():
                sla = stat.get("sla", {})
                alert = {}
                if sla:
                    if stat["latency"].get("avg", 0) > sla.get("latency_ms", float('inf')):
                        alert["latency"] = True
                    if stat["error_rate"] > sla.get("error_rate", float('inf')):
                        alert["error_rate"] = True
                    if stat["availability"] < sla.get("availability", 0):
                        alert["availability"] = True
                alerts[engine] = alert
            return alerts

# -------------------------------
# DOMAIN ORCHESTRATOR BACKBONE
# -------------------------------

class DomainOrchestrator:
    def __init__(self, audit_dir: str):
        self.telemetry_collector = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.coverage_tracker = CoverageTracker()
        self.audit_trail_writer = AuditTrailWriter(audit_dir)
        self.performance_profiler = PerformanceProfiler()

    def process_query(self, query: Dict[str, Any], response: Dict[str, Any], engines_invoked: List[str], mode: str, confidence: float, cache_hit: bool, error: Optional[str] = None):
        query_id = query.get("query_id", "")
        timestamp = time.time()
        latency_ms = response.get("latency_ms", 0.0)
        # Telemetry
        telemetry = QueryTelemetry(
            query_id=query_id,
            timestamp=timestamp,
            latency_ms=latency_ms,
            cache_hit=cache_hit,
            engines_invoked=engines_invoked,
            mode=mode,
            confidence=confidence,
            error=error
        )
        self.telemetry_collector.record_query(telemetry)
        if error:
            self.telemetry_collector.record_error(telemetry)
        # Drift
        self.drift_watcher.record_confidence(mode, confidence)
        self.drift_watcher.detect_drift()
        # Coverage
        doctrines = response.get("doctrines", [])
        if doctrines:
            for doctrine in doctrines:
                self.coverage_tracker.record_triggered(doctrine, query_id)
        else:
            self.coverage_tracker.record_missed(query_id)
            self.coverage_tracker.identify_epistemic_gap(query, doctrines)
        # Determinism Hash
        determinism_hash = compute_determinism_hash(query, response)
        # Audit Trail
        audit_record = {
            "query_id": query_id,
            "timestamp": timestamp,
            "engine_id": mode,
            "engines_invoked": engines_invoked,
            "mode": mode,
            "confidence": confidence,
            "latency": latency_ms,
            "cache_hit": cache_hit,
            "determinism_hash": determinism_hash,
            "error": error
        }
        self.audit_trail_writer.write(audit_record)
        # Performance Profiler
        for engine in engines_invoked:
            self.performance_profiler.record_latency(engine, latency_ms)
            self.performance_profiler.record_availability(engine, True)
            if error:
                self.performance_profiler.record_error(engine, error)

    def get_telemetry_report(self) -> Dict[str, Any]:
        return {
            "latency_stats": self.telemetry_collector.get_latency_stats(),
            "doctrine_hit_rate": self.telemetry_collector.get_doctrine_hit_rate(),
            "queries_last_hour": self.telemetry_collector.queries_last_hour(),
            "sub_engine_stats": self.telemetry_collector.get_sub_engine_stats()
        }

    def get_drift_report(self) -> Dict[str, Any]:
        return self.drift_watcher.get_drift_report()

    def get_coverage_report(self) -> Dict[str, Any]:
        return self.coverage_tracker.get_coverage_report()

    def get_performance_report(self) -> Dict[str, Any]:
        return self.performance_profiler.get_sub_engine_stats()

    def get_sla_alerts(self) -> Dict[str, Any]:
        return self.performance_profiler.monitor_sla()

    def forensic_replay(self, date_str: str) -> List[Dict[str, Any]]:
        return self.audit_trail_writer.forensic_replay(date_str)

    def close(self):
        self.audit_trail_writer.close()

# -------------------------------
# Example Usage (for integration)
# -------------------------------

if __name__ == "__main__":
    orchestrator = DomainOrchestrator(audit_dir="./audit_trail")
    # Simulate queries
    for i in range(100):
        query = {
            "query_id": f"Q{i}",
            "input": f"Sample input {i}"
        }
        response = {
            "latency_ms": float(10 + i % 5),
            "doctrines": ["doctrineA"] if i % 3 == 0 else [],
            "output": f"Sample output {i}"
        }
        engines_invoked = ["engine1", "engine2"] if i % 2 == 0 else ["engine1"]
        mode = "doctrineA" if i % 3 == 0 else "doctrineB"
        confidence = 0.85 if i % 3 == 0 else 0.75
        cache_hit = i % 4 == 0
        error = None if i % 10 != 0 else "Timeout"
        orchestrator.process_query(query, response, engines_invoked, mode, confidence, cache_hit, error)

    # Reports
    print("Telemetry Report:", orchestrator.get_telemetry_report())
    print("Drift Report:", orchestrator.get_drift_report())
    print("Coverage Report:", orchestrator.get_coverage_report())
    print("Performance Report:", orchestrator.get_performance_report())
    print("SLA Alerts:", orchestrator.get_sla_alerts())

    # Forensic replay
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    replay_records = orchestrator.forensic_replay(today)
    print(f"Forensic replay for {today}: {len(replay_records)} records")

    orchestrator.close()

ENGINE_ID = "PRODIE"
ENGINE_PORT = 8854

SUB_ENGINES = {
    "PROD01": "Production Optimization",
    "PROD02": "Artificial Lift",
    "PROD03": "Well Testing",
    "PROD04": "Production Allocation",
    "PROD05": "Decline Curve Analysis",
    "PROD06": "Reservoir Management",
    "PROD07": "Produced Water",
    "PROD08": "Gas Processing",
    "PROD09": "Pipeline Operations",
    "PROD10": "Tank Battery",
    "PROD11": "SCADA Systems",
    "PROD12": "Chemical Treatment",
    "PROD13": "Sand Control",
    "PROD14": "Scale Management",
    "PROD15": "Corrosion Control",
    "PROD16": "Compression",
    "PROD17": "Metering",
    "PROD18": "Regulatory Reporting",
    "PROD19": "Production Economics",
}

# Logger setup
logger = logging.getLogger("prodie")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Global state
class GlobalState:
    doctrine_cache: Dict[str, Dict[str, Any]] = {}
    search_index: Dict[str, List[str]] = {}
    telemetry_data: Dict[str, Any] = {}
    health_status: Dict[str, str] = {}
    routing_rules: Dict[str, Any] = {}
    circuit_breakers: Dict[str, bool] = {}
    cache_hits: int = 0
    cache_misses: int = 0
    query_count: int = 0
    latency_records: List[float] = []
    sub_engine_stats: Dict[str, Dict[str, Any]] = {}
    drift_report: Dict[str, Any] = {}
    doctrine_coverage: Dict[str, Any] = {}
    epistemic_gaps: Dict[str, Any] = {}
    lock: asyncio.Lock = asyncio.Lock()

state = GlobalState()

# Models
class QueryRequest(BaseModel):
    query: str
    parameters: Optional[Dict[str, Any]] = None

class RouteRequest(BaseModel):
    query: str

class AnalyzeRequest(BaseModel):
    query: str
    parameters: Optional[Dict[str, Any]] = None
    engines: Optional[List[str]] = None

class HealthResponse(BaseModel):
    engine: str
    status: str
    details: Optional[Dict[str, Any]] = None

class MetricsResponse(BaseModel):
    latency_avg_ms: float
    latency_p95_ms: float
    cache_hit_rate: float
    queries_per_hour: float
    sub_engine_stats: Dict[str, Any]

class CoverageResponse(BaseModel):
    doctrine_coverage: Dict[str, Any]
    epistemic_gaps: Dict[str, Any]

class DriftResponse(BaseModel):
    drift_report: Dict[str, Any]

class DoctrinesResponse(BaseModel):
    doctrines: List[str]

class RoutingResponse(BaseModel):
    routing_rules: Dict[str, Any]
    engine_registry: Dict[str, str]

class SubEnginesResponse(BaseModel):
    sub_engines: Dict[str, HealthResponse]

class RouteDryRunResponse(BaseModel):
    engines_invoked: List[str]

class AnalyzeResponse(BaseModel):
    analysis_results: Dict[str, Any]

class QueryResponse(BaseModel):
    response: Any
    engines_invoked: List[str]
    cache_used: bool

# Utility functions
def normalize_query(query: str) -> str:
    normalized = query.strip().lower()
    logger.debug(f"Normalized query: {normalized}")
    return normalized

def classify_domain(query: str) -> str:
    # Dummy classification based on keywords
    keywords_map = {
        "optimization": "PROD01",
        "lift": "PROD02",
        "testing": "PROD03",
        "allocation": "PROD04",
        "decline": "PROD05",
        "reservoir": "PROD06",
        "water": "PROD07",
        "gas": "PROD08",
        "pipeline": "PROD09",
        "tank": "PROD10",
        "scada": "PROD11",
        "chemical": "PROD12",
        "sand": "PROD13",
        "scale": "PROD14",
        "corrosion": "PROD15",
        "compression": "PROD16",
        "metering": "PROD17",
        "regulatory": "PROD18",
        "economics": "PROD19",
    }
    for keyword, engine_id in keywords_map.items():
        if keyword in query:
            logger.debug(f"Classified domain '{query}' to engine {engine_id}")
            return engine_id
    logger.debug(f"No classification found for '{query}', defaulting to PROD01")
    return "PROD01"  # default fallback

def route_to_engines(domain_id: str) -> List[str]:
    # For simplicity, route to the classified domain plus related engines
    related_engines_map = {
        "PROD01": ["PROD01", "PROD05", "PROD19"],
        "PROD02": ["PROD02", "PROD06"],
        "PROD03": ["PROD03", "PROD04"],
        "PROD04": ["PROD04", "PROD01"],
        "PROD05": ["PROD05", "PROD01"],
        "PROD06": ["PROD06", "PROD07"],
        "PROD07": ["PROD07", "PROD08"],
        "PROD08": ["PROD08", "PROD09"],
        "PROD09": ["PROD09", "PROD10"],
        "PROD10": ["PROD10", "PROD11"],
        "PROD11": ["PROD11", "PROD12"],
        "PROD12": ["PROD12", "PROD13"],
        "PROD13": ["PROD13", "PROD14"],
        "PROD14": ["PROD14", "PROD15"],
        "PROD15": ["PROD15", "PROD16"],
        "PROD16": ["PROD16", "PROD17"],
        "PROD17": ["PROD17", "PROD18"],
        "PROD18": ["PROD18", "PROD19"],
        "PROD19": ["PROD19", "PROD01"],
    }
    engines = related_engines_map.get(domain_id, [domain_id])
    logger.debug(f"Routing domain {domain_id} to engines {engines}")
    return engines

async def dispatch_to_engine(engine_id: str, query: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    # Simulate sub-engine processing with random delay and possible failure
    await asyncio.sleep(random.uniform(0.05, 0.2))  # simulate latency
    # Circuit breaker check
    if state.circuit_breakers.get(engine_id, False):
        logger.warning(f"Circuit breaker open for engine {engine_id}")
        raise Exception(f"Circuit breaker open for engine {engine_id}")
    # Random failure simulation
    if random.random() < 0.05:
        logger.error(f"Simulated failure in engine {engine_id}")
        raise Exception(f"Engine {engine_id} failed processing")
    # Return dummy response
    response = {
        "engine_id": engine_id,
        "result": f"Processed query '{query}' with parameters {parameters} in engine {engine_id}"
    }
    logger.debug(f"Engine {engine_id} response: {response}")
    return response

def merge_responses(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
    merged = {"results": responses}
    logger.debug(f"Merged responses: {merged}")
    return merged

def apply_guardrails(response: Dict[str, Any]) -> Dict[str, Any]:
    # Dummy guardrail: truncate overly long results
    max_length = 1000
    if "results" in response:
        for res in response["results"]:
            if isinstance(res.get("result"), str) and len(res["result"]) > max_length:
                res["result"] = res["result"][:max_length] + "...[truncated]"
    logger.debug("Applied guardrails to response")
    return response

def hash_query(query: str) -> str:
    h = hashlib.sha256(query.encode("utf-8")).hexdigest()
    logger.debug(f"Hashed query '{query}' to {h}")
    return h

async def log_query(query_hash: str, engines_invoked: List[str], cache_used: bool, latency_ms: float):
    # Dummy async log
    logger.info(f"Query hash: {query_hash}, Engines: {engines_invoked}, Cache used: {cache_used}, Latency: {latency_ms:.2f}ms")

async def fallback_to_doctrine_cache(query: str) -> Optional[Dict[str, Any]]:
    # Return cached doctrine if available
    cached = state.doctrine_cache.get(query)
    if cached:
        logger.info(f"Fallback to doctrine cache for query '{query}'")
    else:
        logger.warning(f"No doctrine cache found for query '{query}'")
    return cached

async def initialize_doctrine_cache():
    # Simulate loading doctrines
    await asyncio.sleep(0.1)
    state.doctrine_cache = {
        "optimization": {"doctrine": "Optimization doctrine details..."},
        "lift": {"doctrine": "Artificial lift doctrine details..."},
        "testing": {"doctrine": "Well testing doctrine details..."},
    }
    logger.info("Doctrine cache initialized")

async def start_health_monitor():
    async def monitor():
        while True:
            for engine_id in SUB_ENGINES.keys():
                # Randomly set health status
                state.health_status[engine_id] = random.choice(["healthy", "degraded", "unhealthy"])
            await asyncio.sleep(30)
    asyncio.create_task(monitor())
    logger.info("Health monitor started")

async def seed_search_index():
    # Simulate search index seeding
    await asyncio.sleep(0.1)
    state.search_index = {
        "optimization": ["PROD01", "PROD05"],
        "lift": ["PROD02", "PROD06"],
        "testing": ["PROD03", "PROD04"],
    }
    logger.info("Search index seeded")

async def start_telemetry():
    async def telemetry_collector():
        while True:
            # Simulate telemetry data collection
            state.telemetry_data["cpu_usage"] = random.uniform(10, 90)
            state.telemetry_data["memory_usage"] = random.uniform(1000, 8000)
            await asyncio.sleep(60)
    asyncio.create_task(telemetry_collector())
    logger.info("Telemetry started")

def get_latency_stats() -> Dict[str, float]:
    latencies = state.latency_records[-1000:]
    if not latencies:
        return {"avg": 0.0, "p95": 0.0}
    avg = sum(latencies) / len(latencies)
    sorted_lat = sorted(latencies)
    p95 = sorted_lat[int(len(sorted_lat)*0.95) - 1]
    return {"avg": avg, "p95": p95}

def get_cache_hit_rate() -> float:
    total = state.cache_hits + state.cache_misses
    if total == 0:
        return 0.0
    return state.cache_hits / total

def get_queries_per_hour() -> float:
    # For simplicity, assume query_count is since start and uptime is 1 hour
    # In real, track start time and compute accordingly
    uptime_hours = 1
    return state.query_count / uptime_hours

def get_sub_engine_stats() -> Dict[str, Any]:
    return state.sub_engine_stats

def get_doctrine_coverage_report() -> Dict[str, Any]:
    # Dummy report
    return {
        "coverage_percent": 85,
        "doctrines_loaded": len(state.doctrine_cache),
        "total_doctrines": 100,
    }

def get_epistemic_gaps_report() -> Dict[str, Any]:
    # Dummy gaps
    return {
        "missing_domains": ["PROD20", "PROD21"],
        "uncertain_mappings": ["PROD13", "PROD14"],
    }

def get_drift_report() -> Dict[str, Any]:
    # Dummy drift report
    return {
        "detected_drifts": [
            {"engine": "PROD05", "metric": "accuracy", "change": -5.2, "timestamp": datetime.utcnow().isoformat()},
            {"engine": "PROD11", "metric": "latency", "change": 12.3, "timestamp": datetime.utcnow().isoformat()},
        ]
    }

def get_routing_rules() -> Dict[str, Any]:
    # Dummy routing rules
    return {
        "rules": [
            {"keyword": "optimization", "route_to": ["PROD01", "PROD05"]},
            {"keyword": "lift", "route_to": ["PROD02", "PROD06"]},
        ]
    }

def get_engine_registry() -> Dict[str, str]:
    return SUB_ENGINES

async def check_sub_engine_health(engine_id: str) -> HealthResponse:
    status = state.health_status.get(engine_id, "unknown")
    details = {"last_checked": datetime.utcnow().isoformat()}
    return HealthResponse(engine=engine_id, status=status, details=details)

async def check_all_sub_engines_health() -> Dict[str, HealthResponse]:
    results = {}
    for engine_id in SUB_ENGINES.keys():
        results[engine_id] = await check_sub_engine_health(engine_id)
    return results

# FastAPI app
app = FastAPI(title="Production Intelligence Engine — Domain Orchestrator", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lifespan management
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Production Intelligence Engine...")
    await initialize_doctrine_cache()
    await start_health_monitor()
    await seed_search_index()
    await start_telemetry()
    logger.info("Startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Production Intelligence Engine...")

# Exception handlers
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    tb = traceback.format_exc()
    logger.debug(tb)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

# Endpoint implementations

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    start_time = time.perf_counter()
    normalized_query = normalize_query(request.query)
    query_hash = hash_query(normalized_query)

    async with state.lock:
        state.query_count += 1

    # Check doctrine cache first
    cached_response = await fallback_to_doctrine_cache(normalized_query)
    if cached_response:
        async with state.lock:
            state.cache_hits += 1
        latency_ms = (time.perf_counter() - start_time) * 1000
        state.latency_records.append(latency_ms)
        await log_query(query_hash, [], True, latency_ms)
        return QueryResponse(response=cached_response, engines_invoked=[], cache_used=True)

    async with state.lock:
        state.cache_misses += 1

    domain_id = classify_domain(normalized_query)
    engines = route_to_engines(domain_id)

    responses = []
    engines_invoked = []
    for engine_id in engines:
        try:
            resp = await dispatch_to_engine(engine_id, normalized_query, request.parameters)
            responses.append(resp)
            engines_invoked.append(engine_id)
            # Update sub-engine stats
            async with state.lock:
                stats = state.sub_engine_stats.setdefault(engine_id, {"success": 0, "failures": 0})
                stats["success"] += 1
        except Exception as e:
            logger.error(f"Error dispatching to engine {engine_id}: {e}")
            async with state.lock:
                stats = state.sub_engine_stats.setdefault(engine_id, {"success": 0, "failures": 0})
                stats["failures"] += 1
            # Circuit breaker logic: open breaker if failures exceed threshold
            failures = state.sub_engine_stats[engine_id]["failures"]
            if failures >= 3:
                state.circuit_breakers[engine_id] = True
                logger.warning(f"Circuit breaker opened for engine {engine_id}")
            # Fallback to doctrine cache for this engine if possible
            fallback = await fallback_to_doctrine_cache(normalized_query)
            if fallback:
                responses.append({"engine_id": engine_id, "result": fallback})
                engines_invoked.append(engine_id)
            else:
                # Skip engine response
                logger.warning(f"No fallback available for engine {engine_id}")

    merged_response = merge_responses(responses)
    guarded_response = apply_guardrails(merged_response)

    latency_ms = (time.perf_counter() - start_time) * 1000
    async with state.lock:
        state.latency_records.append(latency_ms)

    await log_query(query_hash, engines_invoked, False, latency_ms)

    return QueryResponse(response=guarded_response, engines_invoked=engines_invoked, cache_used=False)

@app.get("/health", response_model=Dict[str, HealthResponse])
async def health_endpoint():
    # Self health
    self_health = HealthResponse(engine=ENGINE_ID, status="healthy", details={"timestamp": datetime.utcnow().isoformat()})
    # Sub-engines health
    sub_engines_health = await check_all_sub_engines_health()
    result = {"self": self_health}
    result.update(sub_engines_health)
    return result

@app.get("/metrics", response_model=MetricsResponse)
async def metrics_endpoint():
    latency_stats = get_latency_stats()
    cache_hit_rate = get_cache_hit_rate()
    queries_per_hour = get_queries_per_hour()
    sub_engine_stats = get_sub_engine_stats()
    return MetricsResponse(
        latency_avg_ms=latency_stats["avg"],
        latency_p95_ms=latency_stats["p95"],
        cache_hit_rate=cache_hit_rate,
        queries_per_hour=queries_per_hour,
        sub_engine_stats=sub_engine_stats,
    )

@app.get("/coverage", response_model=CoverageResponse)
async def coverage_endpoint():
    doctrine_coverage = get_doctrine_coverage_report()
    epistemic_gaps = get_epistemic_gaps_report()
    return CoverageResponse(doctrine_coverage=doctrine_coverage, epistemic_gaps=epistemic_gaps)

@app.get("/drift", response_model=DriftResponse)
async def drift_endpoint():
    drift_report = get_drift_report()
    return DriftResponse(drift_report=drift_report)

@app.get("/doctrines", response_model=DoctrinesResponse)
async def doctrines_endpoint():
    doctrines = list(state.doctrine_cache.keys())
    return DoctrinesResponse(doctrines=doctrines)

@app.get("/routing", response_model=RoutingResponse)
async def routing_endpoint():
    routing_rules = get_routing_rules()
    engine_registry = get_engine_registry()
    return RoutingResponse(routing_rules=routing_rules, engine_registry=engine_registry)

@app.get("/sub-engines", response_model=SubEnginesResponse)
async def sub_engines_endpoint():
    sub_engines_health = await check_all_sub_engines_health()
    return SubEnginesResponse(sub_engines=sub_engines_health)

@app.post("/route", response_model=RouteDryRunResponse)
async def route_dry_run_endpoint(request: RouteRequest):
    normalized_query = normalize_query(request.query)
    domain_id = classify_domain(normalized_query)
    engines = route_to_engines(domain_id)
    return RouteDryRunResponse(engines_invoked=engines)

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(request: AnalyzeRequest):
    normalized_query = normalize_query(request.query)
    engines_to_use = request.engines or [classify_domain(normalized_query)]
    analysis_results = {}
    for engine_id in engines_to_use:
        try:
            resp = await dispatch_to_engine(engine_id, normalized_query, request.parameters)
            analysis_results[engine_id] = resp
        except Exception as e:
            analysis_results[engine_id] = {"error": str(e)}
    return AnalyzeResponse(analysis_results=analysis_results)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=ENGINE_PORT, log_level="info")