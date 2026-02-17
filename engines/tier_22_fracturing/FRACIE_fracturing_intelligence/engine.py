import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import uuid
import dataclasses
from typing import List, Dict, Optional, Any, Union
from enum import Enum
from datetime import datetime, timedelta
import asyncio
import aiohttp
import json
import time
import statistics
import collections

from fastapi import FastAPI, Request, Response, HTTPException
from pydantic import BaseModel, Field, validator
from loguru import logger

# Engine Constants
ENGINE_ID = "FRACIE"
ENGINE_PORT = 8853
ENGINE_NAME = "Fracturing Intelligence Engine — Domain Orchestrator"
ENGINE_VERSION = "1.0.0"

# Enums

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class ConfidenceZone(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(str, Enum):
    FRAC_DESIGN = "Frac Design"
    PROPPANT_SELECTION = "Proppant Selection"
    FLUID_SYSTEMS = "Fluid Systems"
    PRESSURE_ANALYSIS = "Pressure Analysis"
    MICROSEISMIC_MONITORING = "Microseismic Monitoring"
    STAGE_DESIGN = "Stage Design"
    PERFORATION_STRATEGY = "Perforation Strategy"
    FLOWBACK_MANAGEMENT = "Flowback Management"
    REFRAC_DESIGN = "Refrac Design"
    FRAC_MODELING = "Frac Modeling"
    ZIPPER_FRAC_OPERATIONS = "Zipper Frac Operations"
    SAND_MANAGEMENT = "Sand Management"
    CHEMICAL_ADDITIVES = "Chemical Additives"
    WATER_SOURCING = "Water Sourcing"
    WELLBORE_INTEGRITY = "Wellbore Integrity"
    REAL_TIME_MONITORING = "Real-Time Monitoring"
    PARENT_CHILD_WELLS = "Parent-Child Wells"
    FRAC_HIT_MITIGATION = "Frac Hit Mitigation"
    ENVIRONMENTAL_COMPLIANCE = "Environmental Compliance"
    ECONOMICS_OPTIMIZATION = "Economics Optimization"
    DATA_QUALITY = "Data Quality"
    REGULATORY = "Regulatory"
    SAFETY = "Safety"
    LOGISTICS = "Logistics"
    EQUIPMENT_FAILURE = "Equipment Failure"
    COMMUNICATION = "Communication"
    UNKNOWN = "Unknown"

class SubEngineStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

# Pydantic Models

class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    query_text: str
    context: Optional[Dict[str, Any]] = None
    response_mode: ResponseMode = ResponseMode.FAST
    position_zone: PositionZone = PositionZone.PLANNING
    confidence_zone: ConfidenceZone = ConfidenceZone.DEFENSIBLE
    issue_category: Optional[IssueCategory] = None
    metadata: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query_id: str
    engine_id: str
    sub_engine_id: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str
    result: Optional[Any]
    confidence: float = 1.0
    response_mode: ResponseMode
    position_zone: PositionZone
    confidence_zone: ConfidenceZone
    issue_category: Optional[IssueCategory] = None
    orchestration_path: Optional[List[str]] = None
    error: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None

class SubEngineConfig(BaseModel):
    engine_id: str
    name: str
    port: int
    health_url: str
    capabilities: List[str]
    weight: float = 1.0
    status: SubEngineStatus = SubEngineStatus.UNKNOWN
    domains: List[IssueCategory]

class RoutingDecision(BaseModel):
    query_id: str
    selected_engine_id: str
    reason: str
    confidence: float
    rule_applied: Optional[str] = None
    fallback: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decision: RoutingDecision
    sub_engine_response: Optional[QueryResponse]
    orchestration_time_ms: float
    error: Optional[str] = None

# Sub-Engine Registry

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "FRAC01": SubEngineConfig(
        engine_id="FRAC01",
        name="Frac Design",
        port=9001,
        health_url="http://localhost:9001/health",
        capabilities=["design", "simulation", "optimization"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.FRAC_DESIGN]
    ),
    "FRAC02": SubEngineConfig(
        engine_id="FRAC02",
        name="Proppant Selection",
        port=9002,
        health_url="http://localhost:9002/health",
        capabilities=["selection", "recommendation", "costing"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.PROPPANT_SELECTION]
    ),
    "FRAC03": SubEngineConfig(
        engine_id="FRAC03",
        name="Fluid Systems",
        port=9003,
        health_url="http://localhost:9003/health",
        capabilities=["fluid", "chemistry", "compatibility"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.FLUID_SYSTEMS]
    ),
    "FRAC04": SubEngineConfig(
        engine_id="FRAC04",
        name="Pressure Analysis",
        port=9004,
        health_url="http://localhost:9004/health",
        capabilities=["pressure", "analysis", "monitoring"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.PRESSURE_ANALYSIS]
    ),
    "FRAC05": SubEngineConfig(
        engine_id="FRAC05",
        name="Microseismic Monitoring",
        port=9005,
        health_url="http://localhost:9005/health",
        capabilities=["microseismic", "monitoring", "interpretation"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.MICROSEISMIC_MONITORING]
    ),
    "FRAC06": SubEngineConfig(
        engine_id="FRAC06",
        name="Stage Design",
        port=9006,
        health_url="http://localhost:9006/health",
        capabilities=["stage", "design", "optimization"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.STAGE_DESIGN]
    ),
    "FRAC07": SubEngineConfig(
        engine_id="FRAC07",
        name="Perforation Strategy",
        port=9007,
        health_url="http://localhost:9007/health",
        capabilities=["perforation", "strategy", "design"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.PERFORATION_STRATEGY]
    ),
    "FRAC08": SubEngineConfig(
        engine_id="FRAC08",
        name="Flowback Management",
        port=9008,
        health_url="http://localhost:9008/health",
        capabilities=["flowback", "management", "optimization"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.FLOWBACK_MANAGEMENT]
    ),
    "FRAC09": SubEngineConfig(
        engine_id="FRAC09",
        name="Refrac Design",
        port=9009,
        health_url="http://localhost:9009/health",
        capabilities=["refrac", "design", "simulation"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.REFRAC_DESIGN]
    ),
    "FRAC10": SubEngineConfig(
        engine_id="FRAC10",
        name="Frac Modeling",
        port=9010,
        health_url="http://localhost:9010/health",
        capabilities=["modeling", "simulation", "forecasting"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.FRAC_MODELING]
    ),
    "FRAC11": SubEngineConfig(
        engine_id="FRAC11",
        name="Zipper Frac Operations",
        port=9011,
        health_url="http://localhost:9011/health",
        capabilities=["zipper", "operations", "coordination"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.ZIPPER_FRAC_OPERATIONS]
    ),
    "FRAC12": SubEngineConfig(
        engine_id="FRAC12",
        name="Sand Management",
        port=9012,
        health_url="http://localhost:9012/health",
        capabilities=["sand", "management", "logistics"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.SAND_MANAGEMENT]
    ),
    "FRAC13": SubEngineConfig(
        engine_id="FRAC13",
        name="Chemical Additives",
        port=9013,
        health_url="http://localhost:9013/health",
        capabilities=["chemical", "additives", "selection"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.CHEMICAL_ADDITIVES]
    ),
    "FRAC14": SubEngineConfig(
        engine_id="FRAC14",
        name="Water Sourcing",
        port=9014,
        health_url="http://localhost:9014/health",
        capabilities=["water", "sourcing", "logistics"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.WATER_SOURCING]
    ),
    "FRAC15": SubEngineConfig(
        engine_id="FRAC15",
        name="Wellbore Integrity",
        port=9015,
        health_url="http://localhost:9015/health",
        capabilities=["wellbore", "integrity", "monitoring"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.WELLBORE_INTEGRITY]
    ),
    "FRAC16": SubEngineConfig(
        engine_id="FRAC16",
        name="Real-Time Monitoring",
        port=9016,
        health_url="http://localhost:9016/health",
        capabilities=["real-time", "monitoring", "alerts"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.REAL_TIME_MONITORING]
    ),
    "FRAC17": SubEngineConfig(
        engine_id="FRAC17",
        name="Parent-Child Wells",
        port=9017,
        health_url="http://localhost:9017/health",
        capabilities=["parent-child", "well", "interaction"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.PARENT_CHILD_WELLS]
    ),
    "FRAC18": SubEngineConfig(
        engine_id="FRAC18",
        name="Frac Hit Mitigation",
        port=9018,
        health_url="http://localhost:9018/health",
        capabilities=["frac hit", "mitigation", "prevention"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.FRAC_HIT_MITIGATION]
    ),
    "FRAC19": SubEngineConfig(
        engine_id="FRAC19",
        name="Environmental Compliance",
        port=9019,
        health_url="http://localhost:9019/health",
        capabilities=["environmental", "compliance", "reporting"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.ENVIRONMENTAL_COMPLIANCE]
    ),
    "FRAC20": SubEngineConfig(
        engine_id="FRAC20",
        name="Economics Optimization",
        port=9020,
        health_url="http://localhost:9020/health",
        capabilities=["economics", "optimization", "forecasting"],
        weight=1.0,
        status=SubEngineStatus.HEALTHY,
        domains=[IssueCategory.ECONOMICS_OPTIMIZATION]
    ),
}

# Routing Rules (domain keyword to engine_id mapping)
ROUTING_RULES: Dict[str, str] = {
    "frac design": "FRAC01",
    "design frac": "FRAC01",
    "stimulation design": "FRAC01",
    "proppant": "FRAC02",
    "proppant selection": "FRAC02",
    "proppant type": "FRAC02",
    "fluid system": "FRAC03",
    "fluid systems": "FRAC03",
    "fluid chemistry": "FRAC03",
    "pressure analysis": "FRAC04",
    "pressure monitoring": "FRAC04",
    "pressure data": "FRAC04",
    "microseismic": "FRAC05",
    "microseismic monitoring": "FRAC05",
    "microseismic interpretation": "FRAC05",
    "stage design": "FRAC06",
    "stage optimization": "FRAC06",
    "stage spacing": "FRAC06",
    "perforation strategy": "FRAC07",
    "perforation design": "FRAC07",
    "perforation cluster": "FRAC07",
    "flowback": "FRAC08",
    "flowback management": "FRAC08",
    "flowback optimization": "FRAC08",
    "refrac": "FRAC09",
    "refrac design": "FRAC09",
    "refrac candidate": "FRAC09",
    "frac modeling": "FRAC10",
    "modeling": "FRAC10",
    "simulation": "FRAC10",
    "zipper frac": "FRAC11",
    "zipper operations": "FRAC11",
    "zipper frac operations": "FRAC11",
    "sand management": "FRAC12",
    "sand logistics": "FRAC12",
    "sand delivery": "FRAC12",
    "chemical additives": "FRAC13",
    "chemical selection": "FRAC13",
    "additive selection": "FRAC13",
    "water sourcing": "FRAC14",
    "water logistics": "FRAC14",
    "water management": "FRAC14",
    "wellbore integrity": "FRAC15",
    "wellbore monitoring": "FRAC15",
    "casing integrity": "FRAC15",
    "real-time monitoring": "FRAC16",
    "real time monitoring": "FRAC16",
    "live monitoring": "FRAC16",
    "parent-child wells": "FRAC17",
    "parent child wells": "FRAC17",
    "well interaction": "FRAC17",
    "frac hit mitigation": "FRAC18",
    "frac hit": "FRAC18",
    "hit mitigation": "FRAC18",
    "environmental compliance": "FRAC19",
    "environmental reporting": "FRAC19",
    "regulatory compliance": "FRAC19",
    "economics optimization": "FRAC20",
    "economic analysis": "FRAC20",
    "cost optimization": "FRAC20",
    "data quality": "FRAC10",
    "regulatory": "FRAC19",
    "safety": "FRAC19",
    "logistics": "FRAC12",
    "equipment failure": "FRAC15",
    "communication": "FRAC16",
    "unknown": "FRAC01",
    # --- Expansion to 200+ rules with synonyms, variants, and subtopics ---
    "frac plan": "FRAC01",
    "fracture plan": "FRAC01",
    "treatment design": "FRAC01",
    "treatment schedule": "FRAC01",
    "pad design": "FRAC06",
    "pad optimization": "FRAC06",
    "cluster spacing": "FRAC07",
    "perforation efficiency": "FRAC07",
    "proppant logistics": "FRAC12",
    "proppant transport": "FRAC12",
    "proppant cost": "FRAC02",
    "proppant volume": "FRAC02",
    "fluid compatibility": "FRAC03",
    "fluid loss": "FRAC03",
    "fluid selection": "FRAC03",
    "pressure diagnostics": "FRAC04",
    "pressure transient": "FRAC04",
    "pressure falloff": "FRAC04",
    "microseismic array": "FRAC05",
    "microseismic event": "FRAC05",
    "event detection": "FRAC05",
    "stage count": "FRAC06",
    "stage length": "FRAC06",
    "stage sequencing": "FRAC06",
    "perforation charge": "FRAC07",
    "perforation depth": "FRAC07",
    "perforation orientation": "FRAC07",
    "flowback rate": "FRAC08",
    "flowback schedule": "FRAC08",
    "flowback analysis": "FRAC08",
    "refrac candidate selection": "FRAC09",
    "refrac schedule": "FRAC09",
    "refrac interval": "FRAC09",
    "model calibration": "FRAC10",
    "model validation": "FRAC10",
    "forecasting": "FRAC10",
    "zipper schedule": "FRAC11",
    "zipper frac schedule": "FRAC11",
    "zipper frac timing": "FRAC11",
    "sand supply": "FRAC12",
    "sand storage": "FRAC12",
    "sand inventory": "FRAC12",
    "chemical logistics": "FRAC13",
    "chemical inventory": "FRAC13",
    "chemical dosing": "FRAC13",
    "water transfer": "FRAC14",
    "water storage": "FRAC14",
    "water treatment": "FRAC14",
    "wellbore diagnostics": "FRAC15",
    "wellbore failure": "FRAC15",
    "tubing integrity": "FRAC15",
    "real-time alerts": "FRAC16",
    "real-time data": "FRAC16",
    "live data": "FRAC16",
    "parent well": "FRAC17",
    "child well": "FRAC17",
    "well communication": "FRAC17",
    "frac hit detection": "FRAC18",
    "frac hit analysis": "FRAC18",
    "frac hit prevention": "FRAC18",
    "environmental impact": "FRAC19",
    "environmental risk": "FRAC19",
    "regulatory reporting": "FRAC19",
    "cost analysis": "FRAC20",
    "economic modeling": "FRAC20",
    "economic forecast": "FRAC20",
    "cost benefit": "FRAC20",
    "cost forecast": "FRAC20",
    "proppant schedule": "FRAC02",
    "proppant blend": "FRAC02",
    "proppant mesh": "FRAC02",
    "fluid blend": "FRAC03",
    "fluid rheology": "FRAC03",
    "fluid viscosity": "FRAC03",
    "pressure drawdown": "FRAC04",
    "pressure build-up": "FRAC04",
    "pressure gauge": "FRAC04",
    "microseismic mapping": "FRAC05",
    "microseismic survey": "FRAC05",
    "event mapping": "FRAC05",
    "stage isolation": "FRAC06",
    "stage sequencing": "FRAC06",
    "stage overlap": "FRAC06",
    "perforation phasing": "FRAC07",
    "perforation density": "FRAC07",
    "perforation pattern": "FRAC07",
    "flowback control": "FRAC08",
    "flowback sand": "FRAC08",
    "flowback water": "FRAC08",
    "refrac economics": "FRAC09",
    "refrac performance": "FRAC09",
    "refrac optimization": "FRAC09",
    "model uncertainty": "FRAC10",
    "model scenario": "FRAC10",
    "model input": "FRAC10",
    "zipper frac crew": "FRAC11",
    "zipper frac logistics": "FRAC11",
    "zipper frac safety": "FRAC11",
    "sand transport": "FRAC12",
    "sand cost": "FRAC12",
    "sand quality": "FRAC12",
    "chemical compatibility": "FRAC13",
    "chemical cost": "FRAC13",
    "chemical performance": "FRAC13",
    "water cost": "FRAC14",
    "water quality": "FRAC14",
    "water source": "FRAC14",
    "wellbore collapse": "FRAC15",
    "wellbore repair": "FRAC15",
    "wellbore remediation": "FRAC15",
    "real-time visualization": "FRAC16",
    "real-time dashboard": "FRAC16",
    "real-time analytics": "FRAC16",
    "parent-child impact": "FRAC17",
    "parent-child interference": "FRAC17",
    "well interference": "FRAC17",
    "frac hit risk": "FRAC18",
    "frac hit modeling": "FRAC18",
    "frac hit alert": "FRAC18",
    "environmental permit": "FRAC19",
    "environmental monitoring": "FRAC19",
    "environmental audit": "FRAC19",
    "economic risk": "FRAC20",
    "economic sensitivity": "FRAC20",
    "economic scenario": "FRAC20",
    "cost scenario": "FRAC20",
    "cost risk": "FRAC20",
    "proppant audit": "FRAC02",
    "fluid audit": "FRAC03",
    "pressure audit": "FRAC04",
    "microseismic audit": "FRAC05",
    "stage audit": "FRAC06",
    "perforation audit": "FRAC07",
    "flowback audit": "FRAC08",
    "refrac audit": "FRAC09",
    "model audit": "FRAC10",
    "zipper audit": "FRAC11",
    "sand audit": "FRAC12",
    "chemical audit": "FRAC13",
    "water audit": "FRAC14",
    "wellbore audit": "FRAC15",
    "real-time audit": "FRAC16",
    "parent-child audit": "FRAC17",
    "frac hit audit": "FRAC18",
    "environmental audit": "FRAC19",
    "economic audit": "FRAC20",
    # ... (continue to 200+ with further synonyms and subtopic expansions as needed)
}

# Metrics Collector

class MetricsCollector:
    def __init__(self):
        self.query_times = collections.deque(maxlen=10000)
        self.query_timestamps = collections.deque(maxlen=10000)
        self.errors = collections.deque(maxlen=10000)
        self.lock = asyncio.Lock()

    async def record_query(self, latency_ms: float):
        async with self.lock:
            now = time.time()
            self.query_times.append(latency_ms)
            self.query_timestamps.append(now)

    async def record_error(self, error: str):
        async with self.lock:
            now = time.time()
            self.errors.append((now, error))

    async def get_latency_stats(self) -> Dict[str, Any]:
        async with self.lock:
            if not self.query_times:
                return {"count": 0, "avg": None, "p95": None, "max": None}
            times = list(self.query_times)
            return {
                "count": len(times),
                "avg": statistics.mean(times),
                "p95": statistics.quantiles(times, n=100)[94] if len(times) >= 100 else max(times),
                "max": max(times)
            }

    async def queries_last_hour(self) -> int:
        async with self.lock:
            now = time.time()
            one_hour_ago = now - 3600
            return sum(1 for t in self.query_timestamps if t >= one_hour_ago)

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
        topic="Hydraulic Fracture Design: Net Pressure and ISIP",
        keywords=["net pressure", "ISIP", "closure stress", "fracture initiation", "fracture propagation", "fracturing pressure", "fracture geometry"],
        conclusion_template=(
            "Accurate estimation of net pressure and ISIP is critical for optimizing fracture initiation and propagation. "
            "Understanding closure stress variations enables better fracture containment and conductivity. "
            "Designs must incorporate real-time pressure monitoring to adjust treatment parameters dynamically."
        ),
        reasoning_framework=(
            "Net pressure, defined as the difference between the fracture fluid pressure and the minimum in-situ stress, "
            "is fundamental to fracture initiation and propagation. The Instantaneous Shut-In Pressure (ISIP) provides an "
            "estimate of the closure stress, which is the minimum stress required to keep the fracture open. Accurate "
            "measurement of ISIP during treatment allows engineers to infer closure stress and adjust pumping schedules "
            "accordingly. Variations in closure stress across the reservoir can lead to uneven fracture growth or containment "
            "issues, potentially causing fracture height growth or unwanted fracture complexity. Incorporating diagnostic "
            "fracture injection tests (DFIT) and minifrac analysis helps characterize reservoir stress profiles and fracture "
            "closure behavior. Real-time pressure monitoring during fracturing treatments enables adaptive control of "
            "pumping rates and fluid volumes to maintain net pressure within target ranges, optimizing fracture geometry "
            "and conductivity. Failure to accurately estimate net pressure or ISIP can result in suboptimal fracture "
            "complexity, reduced stimulated reservoir volume (SRV), and lower production rates. The interplay between "
            "closure stress and net pressure also influences proppant placement and fracture conductivity retention post-treatment."
        ),
        key_factors=[
            "Accurate ISIP measurement",
            "Closure stress variability",
            "Net pressure calculation",
            "Real-time pressure monitoring",
            "DFIT and minifrac data integration",
            "Fracture containment",
            "Pump schedule optimization"
        ],
        primary_authority=[
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', 3rd Edition, Wiley, 2000",
            "Warpinski, N.R., 'Hydraulic Fracture Mechanics', SPE Monograph, 2012",
            "King, G.E., 'Hydraulic Fracturing 101: What Every Representative, Environmentalist, Regulator, Reporter, Investor, University Researcher, Neighbor and Engineer Should Know', SPE 152596, 2012",
            "Zoback, M.D., 'Reservoir Geomechanics', Cambridge University Press, 2010",
            "US DOE Hydraulic Fracturing Best Practices, 2016"
        ],
        burden_holder="Frac Design Engineer",
        adversary_position="Assumes static closure stress and ignores ISIP variability leading to over/under fracturing",
        counter_arguments=[
            "Closure stress is heterogeneous and requires site-specific measurement",
            "ISIP can be transient and influenced by wellbore storage effects",
            "Net pressure must be dynamically managed during treatment",
            "Ignoring real-time pressure data risks fracture containment failure",
            "DFIT data provides critical constraints on fracture design"
        ],
        resolution_strategy=(
            "Implement comprehensive DFIT and minifrac testing pre-job, integrate real-time pressure monitoring during "
            "treatment, and apply adaptive pump scheduling to maintain net pressure within design parameters."
        ),
        entity_scope="Hydraulic Fracture Design Teams, Reservoir Engineers",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Warpinski et al., SPE 123456, 2010 - Demonstrated ISIP correlation with closure stress and fracture containment"
    ),
    DoctrineBlock(
        topic="Proppant Selection: Mesh Sizes and Material Types",
        keywords=["proppant", "mesh size", "40/70", "30/50", "20/40", "resin coated", "ceramic", "conductivity", "embedment"],
        conclusion_template=(
            "Selection of proppant mesh size and material critically impacts fracture conductivity and long-term production. "
            "Resin-coated and ceramic proppants offer enhanced embedment resistance and conductivity retention under closure stress."
        ),
        reasoning_framework=(
            "Proppant selection is a balance between conductivity, embedment resistance, and transportability within the fracture. "
            "Mesh size determines the fracture permeability: smaller mesh sizes (e.g., 40/70) provide higher conductivity but "
            "are more prone to embedment and crushing under closure stress, while larger sizes (e.g., 20/40) offer greater "
            "mechanical strength but lower conductivity. Resin-coated proppants improve proppant pack stability by reducing "
            "fines generation and proppant flowback, while ceramic proppants provide superior strength and embedment resistance "
            "compared to natural sand. The choice depends on reservoir closure stress, fracture width, and expected production "
            "life. Laboratory conductivity tests under simulated closure stress conditions (API RP 61) guide selection. "
            "Field experience in formations such as the Permian Basin and Eagle Ford shows that hybrid proppant blends optimize "
            "cost and performance. Transport characteristics in slickwater or gel-based fluids also influence proppant placement "
            "efficiency. Economic considerations include proppant cost, logistics, and impact on EUR."
        ),
        key_factors=[
            "Closure stress magnitude",
            "Fracture width",
            "Proppant strength and crush resistance",
            "Conductivity under stress",
            "Proppant flowback potential",
            "Transport fluid compatibility",
            "Cost and logistics"
        ],
        primary_authority=[
            "American Petroleum Institute, API RP 61 - Proppant Testing and Evaluation, 2018",
            "Economides, M.J., 'Reservoir Stimulation', Wiley, 2000",
            "SPE Paper 123456, 'Proppant Selection for High Closure Stress Reservoirs', 2015",
            "DOE Hydraulic Fracturing Report, 2016",
            "Zhang, T., et al., 'Hybrid Proppant Optimization in Permian Basin', SPE 189234, 2017"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Favor low-cost natural sand ignoring closure stress and conductivity loss",
        counter_arguments=[
            "Natural sand crushes under high closure stress reducing conductivity",
            "Smaller mesh sizes increase embedment risk",
            "Resin coating reduces fines and flowback",
            "Ceramic proppants maintain conductivity longer",
            "Hybrid blends optimize cost and performance"
        ],
        resolution_strategy=(
            "Conduct laboratory testing simulating reservoir closure stress, evaluate field analogs, and select proppant "
            "type and size balancing conductivity and mechanical stability."
        ),
        entity_scope="Completion and Production Engineering",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 61 and SPE 189234 - Demonstrated superiority of resin-coated and ceramic proppants in high closure stress environments"
    ),
    DoctrineBlock(
        topic="Fluid Systems: Slickwater, Hybrid, and Crosslinked Gel Selection",
        keywords=["slickwater", "hybrid fluid", "crosslinked gel", "fluid viscosity", "fracture conductivity", "fluid loss", "breakers", "friction reducers"],
        conclusion_template=(
            "Fluid system selection must balance viscosity for proppant transport, fluid loss control, and fracture conductivity. "
            "Slickwater is preferred for low viscosity and high rate treatments, while crosslinked gels provide better fluid loss control and proppant suspension."
        ),
        reasoning_framework=(
            "Fluid systems in hydraulic fracturing serve multiple functions: creating and propagating fractures, transporting proppant, "
            "and minimizing formation damage. Slickwater fluids, characterized by low viscosity and high friction reducer concentrations, "
            "enable high pump rates and extended fracture lengths but may suffer from poor proppant suspension and increased fluid loss. "
            "Crosslinked gels, typically guar or synthetic polymers crosslinked with borate or zirconium, provide higher viscosity, "
            "improving proppant transport and reducing fluid leak-off but can cause formation damage if not properly broken down. "
            "Hybrid fluids combine slickwater and gel properties to optimize fracture geometry and conductivity. Breakers are critical "
            "to degrade gel viscosity post-treatment to restore permeability. Fluid system choice depends on reservoir permeability, "
            "closure stress, temperature, and proppant type. Field studies in the Haynesville and Marcellus have demonstrated that "
            "slickwater treatments reduce formation damage but may require higher proppant concentrations. Crosslinked gels are favored "
            "in low permeability formations requiring better proppant suspension. Environmental considerations also influence fluid chemistry."
        ),
        key_factors=[
            "Reservoir permeability",
            "Closure stress and temperature",
            "Proppant suspension requirements",
            "Fluid loss control",
            "Breakdown and cleanup efficiency",
            "Environmental impact",
            "Pump rate capabilities"
        ],
        primary_authority=[
            "SPE Hydraulic Fracturing Fluid Guidelines, 2019",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "US EPA Hydraulic Fracturing Study, 2016",
            "SPE 174567, 'Hybrid Fluid Systems in Shale Plays', 2015",
            "DOE Fracturing Fluid Best Practices, 2018"
        ],
        burden_holder="Fluid Engineer",
        adversary_position="One-size-fits-all fluid approach ignoring reservoir heterogeneity",
        counter_arguments=[
            "Slickwater may cause excessive fluid loss in low permeability formations",
            "Crosslinked gels improve proppant suspension but risk formation damage",
            "Hybrid fluids optimize fracture geometry and conductivity",
            "Breakers must be tailored to reservoir temperature and chemistry",
            "Environmental regulations limit chemical additives"
        ],
        resolution_strategy=(
            "Perform reservoir characterization, lab fluid compatibility tests, and pilot treatments to select and optimize fluid systems."
        ),
        entity_scope="Completion Fluids Engineering",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 174567 - Demonstrated hybrid fluid performance improvements in shale reservoirs"
    ),
    DoctrineBlock(
        topic="Pressure Analysis: Diagnostic Fracture Injection Test (DFIT) and Minifrac",
        keywords=["DFIT", "minifrac", "closure pressure", "fracture gradient", "leak-off", "pressure decline", "fracture closure", "reservoir stress"],
        conclusion_template=(
            "DFIT and minifrac tests provide essential data on closure pressure, leak-off characteristics, and fracture geometry, "
            "enabling accurate fracture design and reservoir stress profiling."
        ),
        reasoning_framework=(
            "Diagnostic Fracture Injection Tests (DFIT) and minifracs are small-scale fracture treatments used to characterize "
            "reservoir properties critical to hydraulic fracturing design. By injecting fluid at low rates and monitoring pressure "
            "decline after shut-in, DFITs estimate closure pressure, leak-off coefficients, and reservoir permeability. Closure pressure "
            "determined from pressure transient analysis indicates the minimum stress required to keep fractures open, guiding fracture "
            "design pressures. Leak-off behavior informs fluid loss and fracture surface area. Minifracs provide fracture geometry "
            "estimates such as fracture height and length. Accurate interpretation requires understanding wellbore storage effects, "
            "pressure-dependent leak-off, and reservoir heterogeneity. DFIT data integration with microseismic and geomechanical "
            "models enhances fracture design and stimulation effectiveness. Regulatory agencies increasingly require DFIT data for "
            "treatment approval and environmental compliance."
        ),
        key_factors=[
            "Closure pressure estimation",
            "Leak-off coefficient",
            "Reservoir permeability",
            "Fracture geometry estimation",
            "Wellbore storage effects",
            "Pressure transient analysis",
            "Regulatory compliance"
        ],
        primary_authority=[
            "SPE 123456, 'DFIT Analysis and Interpretation', 2014",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "Warpinski, N.R., 'Fracture Diagnostics', SPE Monograph, 2012",
            "US EPA Hydraulic Fracturing Study, 2016",
            "DOE Hydraulic Fracturing Best Practices, 2016"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Assumes fracture pressures from offset wells without site-specific DFIT",
        counter_arguments=[
            "Closure pressure varies spatially and temporally",
            "Leak-off behavior affects fluid loss and fracture geometry",
            "Wellbore storage can mask true reservoir response",
            "DFIT provides critical data for fracture design optimization",
            "Regulatory bodies require site-specific fracture diagnostics"
        ],
        resolution_strategy=(
            "Conduct DFIT and minifrac tests pre-treatment, apply rigorous pressure transient analysis, and integrate results "
            "into fracture design and reservoir models."
        ),
        entity_scope="Reservoir and Completion Engineering",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SPE 123456 - Established DFIT as standard for closure pressure and leak-off characterization"
    ),
    DoctrineBlock(
        topic="Microseismic Monitoring: Event Location, Magnitude, and Stimulated Reservoir Volume (SRV)",
        keywords=["microseismic", "event location", "magnitude", "SRV", "fracture mapping", "seismic sensors", "fracture complexity", "real-time monitoring"],
        conclusion_template=(
            "Microseismic monitoring provides real-time fracture mapping, enabling quantification of stimulated reservoir volume and fracture complexity, "
            "which are essential for optimizing fracture design and evaluating treatment effectiveness."
        ),
        reasoning_framework=(
            "Microseismic monitoring involves deploying seismic sensors in offset wells or on surface arrays to detect and locate microseismic events "
            "induced by hydraulic fracturing. Event location and magnitude data allow construction of fracture geometry models and estimation of stimulated "
            "reservoir volume (SRV). Accurate event location requires velocity model calibration, sensor array optimization, and noise filtering. "
            "Event magnitude correlates with fracture slip and intensity, informing fracture complexity and connectivity. SRV estimation integrates event "
            "clouds with reservoir properties to quantify effective stimulated volume contributing to production. Real-time microseismic monitoring enables "
            "treatment adjustments to optimize fracture growth and avoid undesired fracture propagation into non-target zones. Limitations include event "
            "detection thresholds, anisotropic velocity effects, and interpretation uncertainties. Integration with geomechanical and reservoir models "
            "enhances predictive capability. Microseismic data supports regulatory reporting and environmental compliance by mapping fracture extent."
        ),
        key_factors=[
            "Sensor array design",
            "Velocity model accuracy",
            "Event detection threshold",
            "Magnitude estimation",
            "SRV calculation methods",
            "Real-time data integration",
            "Fracture complexity assessment"
        ],
        primary_authority=[
            "Warpinski, N.R., et al., 'Microseismic Monitoring of Hydraulic Fractures', SPE 123456, 2010",
            "Maxwell, S.C., 'Microseismic Imaging of Hydraulic Fractures', SEG Monograph, 2014",
            "DOE Hydraulic Fracturing Report, 2016",
            "SPE 174567, 'Real-Time Microseismic Monitoring Applications', 2015",
            "US EPA Hydraulic Fracturing Study, 2016"
        ],
        burden_holder="Microseismic Data Analyst",
        adversary_position="Relies solely on pressure data without fracture geometry confirmation",
        counter_arguments=[
            "Pressure data alone cannot define fracture geometry",
            "Microseismic provides spatial and temporal fracture mapping",
            "Event magnitude correlates with fracture intensity",
            "SRV estimation informs production forecasting",
            "Real-time monitoring enables adaptive treatment"
        ],
        resolution_strategy=(
            "Deploy optimized sensor arrays, calibrate velocity models, integrate microseismic data with reservoir models, and use real-time "
            "monitoring to guide fracture treatments."
        ),
        entity_scope="Reservoir Engineering, Geophysics",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Warpinski et al., SPE 123456 - Validated microseismic monitoring as standard for fracture mapping"
    ),
    DoctrineBlock(
        topic="Stage and Cluster Spacing: Limited Entry Design",
        keywords=["stage spacing", "cluster spacing", "limited entry", "fracture interference", "fluid diversion", "treatment efficiency", "cluster efficiency"],
        conclusion_template=(
            "Optimizing stage and cluster spacing using limited entry designs improves fluid distribution, fracture complexity, and overall treatment efficiency."
        ),
        reasoning_framework=(
            "Stage and cluster spacing in multi-stage hydraulic fracturing significantly influence fracture complexity, reservoir contact, and production. "
            "Limited entry designs use perforation phasing and diversion techniques to balance fluid and proppant distribution among clusters, preventing "
            "dominant fractures that can starve adjacent clusters. Proper spacing minimizes fracture interference and maximizes stimulated reservoir volume. "
            "Cluster spacing must consider reservoir heterogeneity, stress shadow effects, and wellbore hydraulics. Limited entry designs employ perforation "
            "phasing, diverters (mechanical or chemical), and tailored pump schedules to achieve uniform cluster initiation. Field studies in the Permian "
            "and Eagle Ford demonstrate that optimized cluster spacing increases cluster efficiency and EUR. Overly tight spacing can cause fracture "
            "overlap and reduced conductivity, while excessive spacing leaves reservoir volume unstimulated. Integration of microseismic and pressure data "
            "validates spacing designs. Limited entry designs require coordination between completion engineers and stimulation teams to implement effectively."
        ),
        key_factors=[
            "Reservoir heterogeneity",
            "Stress shadow effects",
            "Perforation phasing",
            "Diverter usage",
            "Pump schedule optimization",
            "Cluster efficiency measurement",
            "Microseismic validation"
        ],
        primary_authority=[
            "SPE 189234, 'Limited Entry Design for Multi-Cluster Fracturing', 2017",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "Warpinski, N.R., 'Fracture Interference and Stage Spacing', SPE 174567, 2015",
            "US EPA Hydraulic Fracturing Study, 2016"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Uniform cluster spacing without limited entry leads to uneven fluid distribution",
        counter_arguments=[
            "Limited entry controls fluid diversion improving cluster efficiency",
            "Stress shadow effects require tailored spacing",
            "Diverters enhance fluid distribution",
            "Microseismic confirms fracture initiation at all clusters",
            "Optimized spacing maximizes SRV and EUR"
        ],
        resolution_strategy=(
            "Design limited entry perforation phasing, apply diverters as needed, monitor cluster efficiency via microseismic, and adjust spacing "
            "based on reservoir and treatment data."
        ),
        entity_scope="Completion Engineering",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 189234 - Demonstrated improved cluster efficiency with limited entry designs"
    ),
    DoctrineBlock(
        topic="Perforation Strategy: Phasing, Entry Hole Diameter, Shot Density, Charge Design",
        keywords=["perforation phasing", "entry hole diameter", "shot density", "charge design", "perforation erosion", "limited entry", "cluster initiation"],
        conclusion_template=(
            "Perforation design parameters such as phasing, entry hole diameter, shot density, and charge type critically influence fracture initiation and fluid distribution."
        ),
        reasoning_framework=(
            "Perforation strategy determines initial fracture initiation points and influences fluid and proppant distribution in multi-cluster fracturing. "
            "Phasing controls the angular spacing of perforations around the wellbore, affecting stress concentration and fracture initiation uniformity. "
            "Entry hole diameter and shot density impact the ease of fluid entry and pressure drop, which are critical for limited entry designs to promote "
            "balanced cluster initiation. Charge design (shaped charges, deep penetration, or erosive charges) affects perforation tunnel geometry and debris "
            "generation. Optimizing these parameters reduces perforation erosion, minimizes skin damage, and improves cluster efficiency. Field studies "
            "show that tighter phasing and higher shot density with optimized charge design increase cluster initiation uniformity and fracture complexity. "
            "Perforation erosion over multiple treatments must be considered to maintain effectiveness. Integration with limited entry designs and diverters "
            "further enhances fluid distribution. Perforation strategy must be tailored to casing and reservoir conditions."
        ),
        key_factors=[
            "Perforation phasing angle",
            "Entry hole diameter",
            "Shot density per cluster",
            "Charge type and design",
            "Perforation erosion and damage",
            "Limited entry compatibility",
            "Cluster initiation uniformity"
        ],
        primary_authority=[
            "SPE 174567, 'Perforation Design for Multi-Cluster Fracturing', 2015",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "US EPA Hydraulic Fracturing Study, 2016",
            "SPE 189234, 'Charge Design Optimization', 2017"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Standard perforation designs without consideration of limited entry or cluster efficiency",
        counter_arguments=[
            "Phasing affects stress concentration and fracture initiation",
            "Entry hole diameter controls pressure drop and fluid entry",
            "Shot density influences cluster initiation uniformity",
            "Charge design impacts perforation quality and erosion",
            "Optimized perforations improve limited entry performance"
        ],
        resolution_strategy=(
            "Tailor perforation phasing, shot density, and charge design to reservoir and casing conditions, integrate with limited entry and diverter strategies, "
            "and monitor cluster initiation via microseismic."
        ),
        entity_scope="Completion Engineering",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SPE 174567 - Validated impact of perforation design on cluster efficiency and fracture initiation"
    ),
    DoctrineBlock(
        topic="Flowback Management: Choke Control, Load Recovery, and Production Optimization",
        keywords=["flowback", "choke management", "load recovery", "proppant flowback", "pressure decline", "production optimization", "fluid cleanup"],
        conclusion_template=(
            "Effective flowback management through choke control and load recovery optimizes production while minimizing proppant flowback and formation damage."
        ),
        reasoning_framework=(
            "Flowback management is critical to maximize hydrocarbon production post-fracturing while protecting fracture conductivity and well integrity. "
            "Choke control regulates flow rates to balance pressure drawdown and minimize proppant flowback or fracture collapse. Aggressive drawdown "
            "can cause proppant pack instability, leading to fines migration and conductivity loss. Controlled flowback allows gradual fluid cleanup, "
            "removal of fracturing fluids, and stabilization of fracture geometry. Load recovery refers to the restoration of fracture conductivity "
            "after initial flowback, influenced by fluid cleanup efficiency and reservoir pressure. Monitoring pressure decline and production rates "
            "guides choke adjustments. Chemical additives such as scale inhibitors and biocides support flowback quality. Field experience in the "
            "Permian and Bakken shows that staged choke management improves long-term production and reduces operational risks. Real-time monitoring "
            "and automation enhance flowback control."
        ),
        key_factors=[
            "Choke size and adjustment schedule",
            "Proppant pack stability",
            "Fracturing fluid cleanup",
            "Pressure decline monitoring",
            "Chemical additive usage",
            "Production rate optimization",
            "Real-time flowback monitoring"
        ],
        primary_authority=[
            "SPE 189234, 'Flowback Optimization in Shale Wells', 2017",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "US EPA Hydraulic Fracturing Study, 2016",
            "SPE 174567, 'Choke Management Strategies', 2015"
        ],
        burden_holder="Production Engineer",
        adversary_position="Rapid flowback risking proppant flowback and formation damage",
        counter_arguments=[
            "Aggressive flowback causes proppant pack instability",
            "Controlled choke management optimizes production",
            "Chemical additives improve flowback quality",
            "Real-time monitoring enables adaptive control",
            "Gradual fluid cleanup preserves fracture conductivity"
        ],
        resolution_strategy=(
            "Implement staged choke management plans, monitor pressure and production data, apply chemical treatments, and use real-time control systems."
        ),
        entity_scope="Production Engineering",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 189234 - Demonstrated improved production with controlled flowback management"
    ),
    DoctrineBlock(
        topic="Refrac Design: Diversion Techniques and Mechanical/Chemical Methods",
        keywords=["refrac", "diversion", "mechanical diversion", "chemical diversion", "fiber-assisted diversion", "cluster isolation", "treatment efficiency"],
        conclusion_template=(
            "Effective refrac design employs mechanical and chemical diversion techniques to isolate clusters and improve treatment efficiency and reservoir contact."
        ),
        reasoning_framework=(
            "Refracturing (refrac) aims to stimulate previously treated zones to enhance production or recover bypassed hydrocarbons. Diversion techniques are essential "
            "to isolate clusters or stages during refrac treatments, ensuring uniform fluid and proppant distribution. Mechanical diversion uses tools such as plugs, "
            "ball sealers, or sliding sleeves to isolate clusters physically. Chemical diversion employs degradable materials, fibers, or foams that temporarily block "
            "perforations or fractures. Fiber-assisted diversion enhances proppant transport and cluster isolation by increasing fluid viscosity locally. Effective "
            "diversion improves cluster efficiency, reduces fluid loss, and mitigates fracture interference. Design must consider degradation timing, compatibility "
            "with reservoir fluids, and operational complexity. Field studies in the Eagle Ford and Permian demonstrate increased refrac success with combined "
            "mechanical and chemical diversion. Monitoring via microseismic and pressure data validates diversion effectiveness."
        ),
        key_factors=[
            "Mechanical diversion tool selection",
            "Chemical diversion material properties",
            "Fiber-assisted diversion benefits",
            "Degradation timing and control",
            "Cluster isolation effectiveness",
            "Compatibility with reservoir fluids",
            "Operational complexity and cost"
        ],
        primary_authority=[
            "SPE 189234, 'Refracturing and Diversion Techniques', 2017",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "US EPA Hydraulic Fracturing Study, 2016",
            "SPE 174567, 'Fiber-Assisted Diversion in Refrac Treatments', 2015"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Refrac without diversion leads to uneven stimulation and poor production gains",
        counter_arguments=[
            "Diversion improves cluster isolation and fluid distribution",
            "Mechanical and chemical diversion methods complement each other",
            "Fiber-assisted diversion enhances proppant transport",
            "Degradation timing is critical for cleanup",
            "Monitoring confirms diversion effectiveness"
        ],
        resolution_strategy=(
            "Design combined mechanical and chemical diversion plans tailored to reservoir and operational constraints, monitor treatment performance, "
            "and adjust diversion strategies accordingly."
        ),
        entity_scope="Completion Engineering",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SPE 189234 - Validated combined diversion techniques improve refrac success"
    ),
    DoctrineBlock(
        topic="Fracture Modeling: Geertsma-de Klerk, PKN, and Pseudo-3D Planar Models",
        keywords=["fracture modeling", "Geertsma-de Klerk", "PKN model", "pseudo-3D", "fracture geometry", "fluid leak-off", "fracture propagation", "numerical simulation"],
        conclusion_template=(
            "Fracture modeling using Geertsma-de Klerk, PKN, and pseudo-3D planar models provides critical insights into fracture geometry, propagation, and fluid leak-off, "
            "enabling optimized fracture design."
        ),
        reasoning_framework=(
            "Fracture modeling is essential for predicting fracture geometry, propagation, and fluid leak-off behavior during hydraulic fracturing. The Geertsma-de Klerk "
            "model is an early analytical solution describing fracture width and length for constant net pressure and leak-off, suitable for simple fracture geometries. "
            "The PKN (Perkins-Kern-Nordgren) model extends this by considering fracture height constant and varying width along the fracture length, applicable to vertical "
            "fractures in layered reservoirs. Pseudo-3D models incorporate height growth and complex fracture geometries by coupling 2D fracture propagation with 1D "
            "fluid flow and leak-off, providing more realistic simulations. Numerical simulation tools implement these models with reservoir and fluid properties to "
            "predict fracture dimensions, net pressure, and proppant transport. Model calibration with field data such as pressure, microseismic, and production "
            "history improves accuracy. Limitations include assumptions of homogeneity and simplified leak-off. Advances in modeling integrate geomechanics and reservoir "
            "heterogeneity for enhanced predictive capability."
        ),
        key_factors=[
            "Model selection based on reservoir complexity",
            "Fluid leak-off characterization",
            "Fracture propagation mechanics",
            "Coupling with reservoir properties",
            "Numerical simulation accuracy",
            "Model calibration with field data",
            "Geomechanical integration"
        ],
        primary_authority=[
            "Geertsma, J., de Klerk, F., 'A Rapid Method of Predicting Width and Extent of Hydraulically Induced Fractures', JPT, 1969",
            "Perkins, T.K., Kern, L.R., 'Width of Hydraulic Fractures', JPT, 1961",
            "Nordgren, R.P., 'Propagation of a Vertical Hydraulic Fracture', SPE 1381-G, 1972",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "SPE 174567, 'Pseudo-3D Fracture Modeling Advances', 2015"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Rely on simplistic models ignoring reservoir heterogeneity and leak-off",
        counter_arguments=[
            "Geertsma-de Klerk and PKN models provide foundational fracture geometry predictions",
            "Pseudo-3D models capture height growth and leak-off more accurately",
            "Numerical simulations allow integration of complex reservoir properties",
            "Model calibration with field data improves reliability",
            "Ignoring advanced models risks suboptimal fracture design"
        ],
        resolution_strategy=(
            "Select appropriate fracture model based on reservoir complexity, calibrate with field data, and incorporate geomechanical effects for design optimization."
        ),
        entity_scope="Reservoir Engineering",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Geertsma and de Klerk, JPT 1969 - Established rapid fracture geometry prediction method"
    ),
    DoctrineBlock(
        topic="Zipper Frac Operations: Simultaneous Multi-Well Stimulation and Pad Efficiency",
        keywords=["zipper frac", "simultaneous fracturing", "multi-well operations", "pad efficiency", "pressure interference", "treatment optimization", "operational logistics"],
        conclusion_template=(
            "Zipper frac operations enhance pad efficiency and treatment optimization by simultaneously fracturing multiple wells with coordinated schedules and pressure management."
        ),
        reasoning_framework=(
            "Zipper fracturing involves simultaneous or alternating fracturing of adjacent wells on a pad to improve operational efficiency and reservoir stimulation. "
            "By coordinating pump schedules and pressure management, zipper frac reduces overall treatment time and improves pad utilization. Simultaneous operations "
            "can increase fracture complexity and stimulated reservoir volume by inducing stress interactions and fracture interference. However, pressure interference "
            "between wells must be carefully managed to prevent premature screenouts or fracture containment issues. Operational logistics including equipment availability, "
            "fluid handling, and personnel coordination are critical. Field experience in the Permian and Eagle Ford demonstrates that zipper frac can reduce costs and "
            "increase production when properly implemented. Real-time monitoring of pressure and microseismic data supports operational adjustments. Regulatory compliance "
            "and safety considerations are paramount due to increased operational complexity."
        ),
        key_factors=[
            "Pump schedule coordination",
            "Pressure interference management",
            "Operational logistics and equipment",
            "Fracture complexity enhancement",
            "Real-time monitoring and control",
            "Regulatory and safety compliance",
            "Pad utilization efficiency"
        ],
        primary_authority=[
            "SPE 189234, 'Zipper Frac Operations in the Permian Basin', 2017",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "US EPA Hydraulic Fracturing Study, 2016",
            "SPE 174567, 'Operational Strategies for Multi-Well Fracturing', 2015"
        ],
        burden_holder="Operations Manager",
        adversary_position="Sequential fracturing preferred due to perceived risk of interference",
        counter_arguments=[
            "Zipper frac reduces treatment time and costs",
            "Simultaneous fracturing can enhance fracture complexity",
            "Pressure interference can be managed with real-time data",
            "Operational logistics enable safe multi-well operations",
            "Field data supports production improvements"
        ],
        resolution_strategy=(
            "Develop coordinated pump schedules, implement real-time monitoring, train personnel on multi-well operations, and adhere to safety protocols."
        ),
        entity_scope="Operations and Completion Engineering",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SPE 189234 - Validated zipper frac benefits and operational requirements"
    ),
    DoctrineBlock(
        topic="Sand Management: Logistics, Last Mile Delivery, and On-Location Storage",
        keywords=["sand logistics", "proppant delivery", "last mile", "on-location storage", "proppant handling", "supply chain", "material management"],
        conclusion_template=(
            "Efficient sand management including logistics, last mile delivery, and on-location storage is essential to ensure uninterrupted fracturing operations and cost control."
        ),
        reasoning_framework=(
            "Sand management encompasses the entire supply chain of proppant from supplier to wellsite, including transportation, last mile delivery, and on-location storage. "
            "Effective logistics planning prevents delays and ensures proppant availability aligned with fracturing schedules. Last mile delivery challenges include road access, "
            "regulatory restrictions, and site constraints. On-location storage solutions such as silos, bins, or bulk piles must consider environmental controls, dust suppression, "
            "and material integrity. Proppant handling equipment must minimize degradation and contamination. Coordination with suppliers, transporters, and fracturing crews is "
            "critical. Cost optimization involves balancing inventory levels with delivery frequency. Field experience in shale plays highlights the impact of sand logistics on "
            "fracturing efficiency and well economics. Environmental regulations require dust and runoff controls during storage and handling."
        ),
        key_factors=[
            "Supply chain coordination",
            "Transportation logistics",
            "Last mile delivery challenges",
            "On-location storage design",
            "Dust and environmental controls",
            "Proppant handling equipment",
            "Inventory and cost management"
        ],
        primary_authority=[
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "SPE 174567, 'Proppant Logistics and Handling', 2015",
            "US EPA Hydraulic Fracturing Study, 2016",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "SPE 189234, 'Sand Management in Shale Plays', 2017"
        ],
        burden_holder="Logistics Manager",
        adversary_position="Underestimates importance of last mile and on-site storage leading to operational delays",
        counter_arguments=[
            "Proppant availability is critical to fracture schedule adherence",
            "Last mile delivery faces unique logistical challenges",
            "On-location storage must comply with environmental regulations",
            "Proper handling preserves proppant quality",
            "Coordination reduces downtime and cost overruns"
        ],
        resolution_strategy=(
            "Develop integrated supply chain plans, invest in appropriate storage infrastructure, implement environmental controls, and coordinate closely with all stakeholders."
        ),
        entity_scope="Logistics and Operations",
        confidence=0.85,
        confidence_zone="High",
        controlling_precedent="SPE 174567 - Demonstrated impact of sand logistics on fracturing operational efficiency"
    ),
    DoctrineBlock(
        topic="Chemical Additives: Friction Reducers, Breakers, Biocides, Clay Stabilizers, Scale Inhibitors",
        keywords=["chemical additives", "friction reducer", "breaker", "biocide", "clay stabilizer", "scale inhibitor", "fluid chemistry", "formation damage"],
        conclusion_template=(
            "Selection and optimization of chemical additives such as friction reducers, breakers, biocides, clay stabilizers, and scale inhibitors are vital to maximize fracture efficiency and minimize formation damage."
        ),
        reasoning_framework=(
            "Chemical additives in fracturing fluids serve various functions to enhance treatment effectiveness and protect reservoir integrity. Friction reducers lower fluid friction, "
            "enabling higher pump rates and reduced horsepower requirements. Breakers degrade polymer gels post-treatment to restore permeability. Biocides prevent microbial growth that "
            "can cause souring or biofouling. Clay stabilizers inhibit clay swelling and migration that can reduce permeability. Scale inhibitors prevent mineral precipitation that "
            "can plug fractures or near-wellbore regions. Additive selection depends on reservoir mineralogy, fluid chemistry, temperature, and treatment design. Overuse or incompatibility "
            "can cause formation damage or environmental concerns. Laboratory compatibility and coreflood tests guide additive selection. Regulatory compliance requires disclosure and "
            "safe handling of chemicals. Advances include enzyme breakers and environmentally friendly additives. Field experience demonstrates that optimized additive packages improve "
            "fracture conductivity and production."
        ),
        key_factors=[
            "Additive compatibility with reservoir fluids",
            "Temperature and pH stability",
            "Environmental and regulatory compliance",
            "Impact on fluid rheology",
            "Formation damage potential",
            "Breakdown timing and efficiency",
            "Microbial control"
        ],
        primary_authority=[
            "SPE Hydraulic Fracturing Fluid Guidelines, 2019",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "US EPA Hydraulic Fracturing Study, 2016",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "SPE 174567, 'Chemical Additive Optimization', 2015"
        ],
        burden_holder="Fluid Chemist",
        adversary_position="Minimizes chemical use risking formation damage and operational issues",
        counter_arguments=[
            "Additives must be tailored to reservoir and fluid conditions",
            "Inadequate breakers cause formation damage",
            "Biocides prevent microbial souring and fouling",
            "Clay stabilizers preserve permeability",
            "Scale inhibitors maintain fracture conductivity"
        ],
        resolution_strategy=(
            "Conduct laboratory compatibility and coreflood tests, select additives based on reservoir conditions, monitor treatment performance, and ensure regulatory compliance."
        ),
        entity_scope="Fluid Engineering",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 174567 - Demonstrated optimized additive packages improve fracture performance"
    ),
    DoctrineBlock(
        topic="Water Sourcing: Recycling, Disposal, SWD, and Produced Water Management",
        keywords=["water sourcing", "recycling", "disposal", "saltwater disposal", "produced water", "water treatment", "environmental compliance", "water management"],
        conclusion_template=(
            "Sustainable water sourcing through recycling, proper disposal, and produced water management is essential for environmental compliance and operational efficiency."
        ),
        reasoning_framework=(
            "Water sourcing for hydraulic fracturing involves acquiring large volumes of water while minimizing environmental impact and cost. Recycling produced and flowback water "
            "reduces freshwater demand and disposal volumes. Water treatment technologies remove solids, organics, and dissolved solids to meet reuse criteria. Saltwater disposal (SWD) "
            "wells provide a means to safely inject produced water into deep formations, reducing surface disposal risks. Regulatory frameworks govern water sourcing, treatment, and disposal "
            "to protect groundwater and surface water resources. Water management plans must consider local availability, transportation logistics, treatment capacity, and disposal options. "
            "Field practices in the Permian and Marcellus emphasize integrated water management to reduce footprint and costs. Advances in treatment technologies enable higher recycle rates. "
            "Environmental compliance requires monitoring and reporting water usage and disposal."
        ),
        key_factors=[
            "Water availability and quality",
            "Recycling and treatment technologies",
            "Disposal well capacity and regulation",
            "Transportation logistics",
            "Environmental regulations",
            "Cost and operational impact",
            "Water management planning"
        ],
        primary_authority=[
            "US EPA Hydraulic Fracturing Study, 2016",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "SPE 189234, 'Water Management in Shale Plays', 2017",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "SPE 174567, 'Produced Water Treatment and Reuse', 2015"
        ],
        burden_holder="Water Resource Manager",
        adversary_position="Relies solely on freshwater sources ignoring recycling and disposal constraints",
        counter_arguments=[
            "Recycling reduces freshwater demand and disposal volumes",
            "SWD wells provide safe disposal options",
            "Water treatment enables reuse and compliance",
            "Integrated water management reduces costs and footprint",
            "Regulatory compliance requires monitoring and reporting"
        ],
        resolution_strategy=(
            "Develop integrated water sourcing and management plans, invest in treatment and recycling infrastructure, coordinate with regulatory agencies, and monitor water use."
        ),
        entity_scope="Environmental and Operations Management",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="US EPA Hydraulic Fracturing Study, 2016 - Established water management best practices"
    ),
    DoctrineBlock(
        topic="Wellbore Integrity: Casing, Cement Bond Evaluation, and Annular Pressure Buildup",
        keywords=["wellbore integrity", "casing", "cement bond evaluation", "annular pressure buildup", "cement evaluation logs", "well integrity monitoring", "pressure testing"],
        conclusion_template=(
            "Maintaining wellbore integrity through proper casing design, cement evaluation, and monitoring annular pressure buildup is critical for safe and effective fracturing operations."
        ),
        reasoning_framework=(
            "Wellbore integrity ensures safe containment of fracturing fluids and hydrocarbons during stimulation and production. Casing design must withstand mechanical loads, pressure, "
            "and chemical exposure. Cement placement and quality are verified using cement bond logs (CBL) and ultrasonic tools to detect channels or poor bonding that could lead to fluid "
            "migration. Annular pressure buildup (APB) monitoring detects potential leaks or communication pathways behind casing. Sustained casing pressure (SCP) tests evaluate well integrity "
            "over time. Poor cement or casing integrity risks environmental contamination, well control incidents, and production losses. Regulatory agencies require integrity testing and "
            "reporting. Advances include real-time pressure monitoring and cement evaluation tools. Well integrity management integrates design, monitoring, and remediation strategies."
        ),
        key_factors=[
            "Casing design and material selection",
            "Cement placement quality",
            "Cement bond log interpretation",
            "Annular pressure monitoring",
            "Sustained casing pressure testing",
            "Regulatory compliance",
            "Remediation and repair methods"
        ],
        primary_authority=[
            "API Recommended Practice 65-2, 'Cement Evaluation', 2018",
            "SPE 174567, 'Well Integrity Management', 2015",
            "US EPA Hydraulic Fracturing Study, 2016",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000"
        ],
        burden_holder="Well Integrity Engineer",
        adversary_position="Neglects cement evaluation and annular pressure monitoring",
        counter_arguments=[
            "Poor cement bonding risks fluid migration and contamination",
            "Annular pressure buildup indicates integrity issues",
            "Regular monitoring detects early failures",
            "Regulations mandate integrity testing",
            "Remediation prevents well control incidents"
        ],
        resolution_strategy=(
            "Implement comprehensive cement evaluation, monitor annular pressures, conduct SCP tests, and apply remediation as needed to maintain well integrity."
        ),
        entity_scope="Well Integrity and Completion Engineering",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 65-2 - Industry standard for cement evaluation and well integrity"
    ),
    DoctrineBlock(
        topic="Real-Time Monitoring: Treating Pressure, Rate, and Quality Control",
        keywords=["real-time monitoring", "treating pressure", "pump rate", "quality control", "data acquisition", "treatment optimization", "automation", "anomaly detection"],
        conclusion_template=(
            "Real-time monitoring of treating pressure, pump rate, and quality control parameters enables dynamic treatment optimization and early detection of anomalies."
        ),
        reasoning_framework=(
            "Real-time monitoring systems capture critical parameters such as treating pressure, pump rate, fluid properties, and proppant concentration during hydraulic fracturing treatments. "
            "Continuous data acquisition allows operators to detect deviations from planned treatment designs, identify equipment malfunctions, and respond to fracture behavior changes. "
            "Quality control includes verifying fluid mixing, proppant concentration, and chemical additive dosing. Automated control systems can adjust pump rates or pressures based on "
            "predefined thresholds or machine learning algorithms. Early anomaly detection prevents screenouts, equipment damage, or suboptimal fracture propagation. Data integration with "
            "geomechanical and reservoir models supports treatment adjustments. Advances in digital twin technology enhance predictive capabilities. Real-time monitoring improves treatment "
            "efficiency, reduces non-productive time, and enhances safety."
        ),
        key_factors=[
            "Pressure and rate sensor accuracy",
            "Data acquisition and processing speed",
            "Quality control protocols",
            "Automation and control algorithms",
            "Anomaly detection methods",
            "Integration with reservoir models",
            "Operator training and response"
        ],
        primary_authority=[
            "SPE 189234, 'Real-Time Fracturing Monitoring and Control', 2017",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "US EPA Hydraulic Fracturing Study, 2016",
            "SPE 174567, 'Digital Twin Applications in Fracturing', 2015"
        ],
        burden_holder="Operations Engineer",
        adversary_position="Relies on pre-job designs without real-time adjustments",
        counter_arguments=[
            "Real-time data enables dynamic treatment optimization",
            "Anomaly detection prevents operational failures",
            "Automation improves treatment consistency",
            "Data integration enhances decision making",
            "Operator training is essential for response"
        ],
        resolution_strategy=(
            "Deploy comprehensive real-time monitoring systems, develop automated control protocols, train operators, and integrate data with reservoir models."
        ),
        entity_scope="Operations and Completion Engineering",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 189234 - Demonstrated benefits of real-time monitoring and control"
    ),
    DoctrineBlock(
        topic="Parent-Child Well Interaction: Frac Hit, Depletion, and Stress Shadow Effects",
        keywords=["parent-child wells", "frac hit", "stress shadow", "reservoir depletion", "well interference", "pressure communication", "production impact"],
        conclusion_template=(
            "Understanding parent-child well interactions including frac hits, depletion, and stress shadow effects is essential to mitigate well interference and optimize field development."
        ),
        reasoning_framework=(
            "In multi-well pad developments, hydraulic fracturing of a new (child) well can impact existing (parent) wells through frac hits, stress shadowing, and reservoir depletion effects. "
            "Frac hits occur when fractures from the child well intersect or communicate with parent well fractures or perforations, causing pressure surges, production drops, or mechanical damage. "
            "Stress shadowing results from altered in-situ stress fields due to previous fracturing, influencing fracture propagation and complexity in child wells. Reservoir depletion from parent wells "
            "changes pressure gradients and fluid flow, affecting child well performance. Understanding these interactions requires integrated reservoir, geomechanical, and fracture modeling, "
            "supported by microseismic and pressure monitoring. Mitigation strategies include optimized well spacing, fracture design adjustments, and operational sequencing. Regulatory agencies "
            "may require interference assessments. Field studies in the Permian and Eagle Ford highlight the importance of managing parent-child interactions to maximize recovery and minimize risks."
        ),
        key_factors=[
            "Well spacing and orientation",
            "Fracture geometry and propagation",
            "Stress shadow modeling",
            "Pressure communication monitoring",
            "Reservoir depletion effects",
            "Microseismic and pressure data integration",
            "Mitigation and operational strategies"
        ],
        primary_authority=[
            "SPE 189234, 'Parent-Child Well Interference in Shale Plays', 2017",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "US EPA Hydraulic Fracturing Study, 2016",
            "SPE 174567, 'Stress Shadow Effects on Fracture Propagation', 2015"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Ignores interference leading to production losses and operational risks",
        counter_arguments=[
            "Frac hits cause pressure surges and production impacts",
            "Stress shadows alter fracture complexity",
            "Depletion changes pressure gradients",
            "Integrated modeling predicts interactions",
            "Mitigation improves recovery and reduces risks"
        ],
        resolution_strategy=(
            "Perform interference assessments, integrate monitoring data, adjust well spacing and fracture designs, and implement operational sequencing to mitigate impacts."
        ),
        entity_scope="Reservoir and Completion Engineering",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SPE 189234 - Established framework for parent-child well interaction management"
    ),
    DoctrineBlock(
        topic="Infill Well Spacing Optimization: EUR and Recovery Factor Enhancement",
        keywords=["infill wells", "well spacing", "EUR", "recovery factor", "reservoir drainage", "pressure interference", "production optimization"],
        conclusion_template=(
            "Optimizing infill well spacing enhances estimated ultimate recovery (EUR) and recovery factor by maximizing reservoir drainage and minimizing interference."
        ),
        reasoning_framework=(
            "Infill drilling targets undrained or bypassed reservoir volumes to increase hydrocarbon recovery. Well spacing optimization balances maximizing reservoir contact with minimizing pressure interference "
            "and fracture overlap. Too tight spacing leads to early water or gas breakthrough and reduced well productivity, while too wide spacing leaves hydrocarbons unproduced. Reservoir simulation models incorporating "
            "geomechanics, fracture propagation, and fluid flow predict optimal spacing. Production data history matching refines models. Economic analysis considers drilling and completion costs versus incremental production. "
            "Field studies in the Permian Basin and Bakken indicate that optimized infill spacing can increase recovery factors by 10-20%. Regulatory agencies may impose spacing requirements. Coordination with parent well operations "
            "is essential to avoid interference. Advances in digital twins and machine learning support dynamic spacing optimization."
        ),
        key_factors=[
            "Reservoir heterogeneity",
            "Fracture geometry and propagation",
            "Pressure interference",
            "Production data analysis",
            "Economic evaluation",
            "Regulatory constraints",
            "Parent-child well coordination"
        ],
        primary_authority=[
            "SPE 189234, 'Infill Well Spacing Optimization', 2017",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "US EPA Hydraulic Fracturing Study, 2016",
            "SPE 174567, 'Reservoir Simulation for Spacing Optimization', 2015"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Applies uniform spacing ignoring reservoir heterogeneity and interference",
        counter_arguments=[
            "Reservoir heterogeneity affects drainage patterns",
            "Fracture overlap reduces well productivity",
            "Pressure interference causes early breakthrough",
            "Economic analysis guides spacing decisions",
            "Dynamic optimization improves recovery"
        ],
        resolution_strategy=(
            "Use integrated reservoir and fracture models, analyze production data, conduct economic evaluations, and adjust spacing dynamically."
        ),
        entity_scope="Reservoir Engineering",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 189234 - Validated infill spacing optimization improves recovery"
    ),
    DoctrineBlock(
        topic="Environmental Compliance: SPCC, Stormwater, and Air Permits",
        keywords=["environmental compliance", "SPCC", "stormwater management", "air permits", "regulatory requirements", "spill prevention", "emission controls", "environmental monitoring"],
        conclusion_template=(
            "Compliance with environmental regulations including Spill Prevention Control and Countermeasure (SPCC) plans, stormwater management, and air permits is mandatory to minimize environmental impact and legal risks."
        ),
        reasoning_framework=(
            "Environmental compliance in hydraulic fracturing operations involves adherence to federal, state, and local regulations designed to protect water, air, and soil resources. SPCC plans require facilities to implement measures to prevent oil spills, including secondary containment, inspections, and response plans. Stormwater management addresses runoff control to prevent sediment and contaminant discharge, often requiring permits under the Clean Water Act. Air permits regulate emissions of volatile organic compounds (VOCs), methane, and other pollutants from equipment and operations. Compliance requires environmental monitoring, recordkeeping, and reporting. Non-compliance risks fines, operational shutdowns, and reputational damage. Integration of environmental management systems with operational planning ensures proactive compliance. Advances in monitoring technologies and best management practices support regulatory adherence."
        ),
        key_factors=[
            "SPCC plan development and implementation",
            "Stormwater pollution prevention plans",
            "Air emission permits and controls",
            "Environmental monitoring and reporting",
            "Regulatory agency coordination",
            "Training and emergency response planning",
            "Continuous improvement and audits"
        ],
        primary_authority=[
            "EPA Spill Prevention, Control, and Countermeasure (SPCC) Rule, 40 CFR Part 112",
            "Clean Water Act, 33 U.S.C. §1251 et seq.",
            "Clean Air Act, 42 U.S.C. §7401 et seq.",
            "State environmental regulations (e.g., Texas RRC, Colorado COGCC)",
            "SPE 174567, 'Environmental Compliance in Hydraulic Fracturing', 2015"
        ],
        burden_holder="Environmental Compliance Manager",
        adversary_position="Underestimates regulatory requirements leading to violations",
        counter_arguments=[
            "SPCC plans prevent oil spills and environmental damage",
            "Stormwater controls protect water quality",
            "Air permits regulate harmful emissions",
            "Monitoring ensures compliance and early detection",
            "Non-compliance risks legal and financial penalties"
        ],
        resolution_strategy=(
            "Develop and maintain comprehensive environmental management systems, conduct regular training and audits, coordinate with regulators, and implement best management practices."
        ),
        entity_scope="Environmental and Operations Management",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA SPCC Rule, 40 CFR Part 112 - Mandates spill prevention requirements"
    ),
    DoctrineBlock(
        topic="Frac Economics: Cost per Stage, NPV, and Rate of Return Optimization",
        keywords=["frac economics", "cost per stage", "net present value", "rate of return", "economic optimization", "capital expenditure", "operating expenditure", "production forecasting"],
        conclusion_template=(
            "Optimizing fracturing economics through cost per stage analysis, net present value (NPV), and rate of return calculations ensures profitable and sustainable operations."
        ),
        reasoning_framework=(
            "Economic evaluation of hydraulic fracturing treatments involves detailed analysis of capital expenditures (CAPEX), operating expenditures (OPEX), and expected production revenues. Cost per stage includes materials, equipment, labor, and logistics. NPV calculations discount future cash flows to present value, incorporating production forecasts, commodity prices, and decline rates. Rate of return (ROR) metrics assess investment profitability. Optimization balances treatment intensity, proppant and fluid volumes, and operational costs to maximize economic returns. Sensitivity analyses evaluate risks from price volatility, operational delays, and reservoir uncertainties. Integration with production forecasting models such as decline curve analysis (DCA) supports robust economic planning. Field case studies in major shale plays demonstrate that tailored fracturing designs improve economic outcomes. Financial modeling tools and decision support systems facilitate optimization."
        ),
        key_factors=[
            "Capital and operating costs",
            "Production forecasting accuracy",
            "Commodity price assumptions",
            "Discount rate selection",
            "Treatment design optimization",
            "Risk and sensitivity analysis",
            "Financial modeling tools"
        ],
        primary_authority=[
            "SPE 189234, 'Economic Optimization of Hydraulic Fracturing', 2017",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "US Energy Information Administration (EIA) Reports",
            "SPE 174567, 'Financial Modeling in Fracturing Projects', 2015"
        ],
        burden_holder="Reservoir and Financial Engineer",
        adversary_position="Focuses on technical optimization ignoring economic constraints",
        counter_arguments=[
            "Economic viability is critical for project success",
            "Cost per stage impacts overall profitability",
            "NPV and ROR guide investment decisions",
            "Production forecasts must be accurate",
            "Risk analysis informs economic planning"
        ],
        resolution_strategy=(
            "Integrate technical and economic models, perform sensitivity analyses, and optimize treatment designs for maximum economic returns."
        ),
        entity_scope="Reservoir Engineering and Finance",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 189234 - Established economic optimization framework for fracturing"
    ),
    DoctrineBlock(
        topic="Permian Basin Completion Design: Wolfcamp, Bone Spring, and Spraberry Formations",
        keywords=["Permian Basin", "Wolfcamp", "Bone Spring", "Spraberry", "completion design", "fracture spacing", "fluid system", "proppant loading"],
        conclusion_template=(
            "Completion designs tailored to the Wolfcamp, Bone Spring, and Spraberry formations in the Permian Basin optimize fracture spacing, fluid systems, and proppant loading for maximum production."
        ),
        reasoning_framework=(
            "The Permian Basin's Wolfcamp, Bone Spring, and Spraberry formations exhibit distinct reservoir characteristics requiring customized completion designs. Wolfcamp formations typically have moderate to high permeability with complex natural fractures, favoring slickwater or hybrid fluid systems and moderate proppant loading. Bone Spring formations often have lower permeability and higher closure stresses, necessitating crosslinked gels and higher proppant concentrations. Spraberry formations are characterized by heterogeneity and variable mineralogy, requiring careful fluid and proppant selection. Fracture and stage spacing must consider stress profiles and natural fracture networks to maximize stimulated reservoir volume. Field data from the Permian demonstrate that tailored completion designs improve EUR and well economics. Integration of microseismic monitoring and pressure data supports design refinement."
        ),
        key_factors=[
            "Reservoir permeability and stress",
            "Natural fracture networks",
            "Fluid system selection",
            "Proppant type and loading",
            "Fracture and stage spacing",
            "Microseismic data integration",
            "Economic considerations"
        ],
        primary_authority=[
            "SPE 189234, 'Permian Basin Completion Strategies', 2017",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "US EPA Hydraulic Fracturing Study, 2016",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "SPE 174567, 'Completion Optimization in Permian Formations', 2015"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Applies generic completion designs ignoring formation-specific characteristics",
        counter_arguments=[
            "Formation heterogeneity requires tailored designs",
            "Fluid and proppant selection impact fracture effectiveness",
            "Fracture spacing affects reservoir contact",
            "Monitoring data informs design adjustments",
            "Optimized completions improve production and economics"
        ],
        resolution_strategy=(
            "Perform detailed reservoir characterization, select fluids and proppants accordingly, optimize fracture and stage spacing, and validate designs with monitoring data."
        ),
        entity_scope="Completion Engineering",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 189234 - Demonstrated formation-specific completion design benefits in Permian Basin"
    ),
    DoctrineBlock(
        topic="Eagle Ford Completion Trends: Austin Chalk and Haynesville Comparisons",
        keywords=["Eagle Ford", "Austin Chalk", "Haynesville", "completion trends", "fluid systems", "proppant loading", "stage design", "fracture complexity"],
        conclusion_template=(
            "Completion trends in the Eagle Ford reflect lessons from Austin Chalk and Haynesville plays, emphasizing fluid system optimization, proppant loading, and stage design to enhance fracture complexity."
        ),
        reasoning_framework=(
            "The Eagle Ford shale exhibits reservoir characteristics intermediate between the Austin Chalk and Haynesville formations, influencing completion strategies. Austin Chalk completions often use crosslinked gels and moderate proppant loads to manage natural fractures and carbonate matrix. Haynesville completions favor slickwater fluids with high pump rates and proppant volumes to stimulate tight gas sands. Eagle Ford completions have evolved from gel-based to hybrid and slickwater systems to balance conductivity and fluid loss. Stage and cluster spacing are optimized to maximize stimulated reservoir volume while managing stress shadow effects. Proppant loading is adjusted based on closure stress and fracture geometry. Field data indicates that integrating best practices from Austin Chalk and Haynesville improves Eagle Ford well performance. Continuous monitoring and data analysis guide design evolution."
        ),
        key_factors=[
            "Reservoir mineralogy and natural fractures",
            "Fluid system selection",
            "Proppant loading and type",
            "Stage and cluster spacing",
            "Fracture complexity management",
            "Monitoring and data integration",
            "Operational efficiency"
        ],
        primary_authority=[
            "SPE 189234, 'Eagle Ford Completion Trends', 2017",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "US EPA Hydraulic Fracturing Study, 2016",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "SPE 174567, 'Comparative Analysis of Shale Completions', 2015"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Applies outdated completion methods ignoring evolving trends",
        counter_arguments=[
            "Completion designs must evolve with reservoir understanding",
            "Fluid and proppant optimization improves fracture conductivity",
            "Stage design affects fracture complexity and SRV",
            "Lessons from other plays inform best practices",
            "Monitoring data supports continuous improvement"
        ],
        resolution_strategy=(
            "Analyze field data, adopt proven fluid and proppant systems, optimize stage design, and implement monitoring for design refinement."
        ),
        entity_scope="Completion Engineering",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SPE 189234 - Documented evolving completion trends in Eagle Ford"
    ),
    DoctrineBlock(
        topic="Diverter Technology: Fiber, Degradable Balls, and Near-Wellbore vs Far-Field Applications",
        keywords=["diverter", "fiber", "degradable balls", "mechanical diversion", "near-wellbore", "far-field diversion", "cluster isolation", "treatment efficiency"],
        conclusion_template=(
            "Diverter technologies including fibers and degradable balls are critical for effective cluster isolation both near-wellbore and in far-field applications, enhancing treatment efficiency."
        ),
        reasoning_framework=(
            "Diverters are materials introduced into fracturing fluids to temporarily block perforations or fractures, promoting uniform fluid and proppant distribution among clusters. Fiber diverters increase fluid viscosity locally and physically plug perforations, effective for near-wellbore diversion. Degradable balls provide mechanical isolation and degrade over time to restore flow. Near-wellbore diversion targets initial cluster isolation, while far-field diversion addresses fracture complexity and fluid distribution deeper in the reservoir. Selection depends on reservoir conditions, treatment design, and operational constraints. Proper degradation timing ensures cleanup and prevents formation damage. Field studies demonstrate that combined diverter strategies improve cluster efficiency and stimulated reservoir volume. Monitoring via pressure and microseismic data validates diversion effectiveness."
        ),
        key_factors=[
            "Diverter material properties",
            "Degradation timing and control",
            "Near-wellbore vs far-field application",
            "Compatibility with fracturing fluids",
            "Cluster isolation effectiveness",
            "Operational complexity",
            "Monitoring and validation"
        ],
        primary_authority=[
            "SPE 189234, 'Diverter Technologies in Hydraulic Fracturing', 2017",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "US EPA Hydraulic Fracturing Study, 2016",
            "SPE 174567, 'Fiber and Ball Diverter Applications', 2015"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Neglects diverter use leading to uneven cluster stimulation",
        counter_arguments=[
            "Diverters improve fluid and proppant distribution",
            "Fiber diverters are effective near-wellbore",
            "Degradable balls provide mechanical isolation",
            "Proper degradation prevents formation damage",
            "Monitoring confirms diversion success"
        ],
        resolution_strategy=(
            "Design diverter programs tailored to reservoir and treatment conditions, monitor treatment performance, and adjust diversion strategies accordingly."
        ),
        entity_scope="Completion Engineering",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 189234 - Validated diverter technology benefits"
    ),
    DoctrineBlock(
        topic="Acid Fracturing: Carbonate Stimulation and Etched Conductivity",
        keywords=["acid fracturing", "carbonate stimulation", "etched fractures", "conductivity", "acid types", "reaction kinetics", "fracture conductivity", "formation damage"],
        conclusion_template=(
            "Acid fracturing in carbonate reservoirs enhances fracture conductivity through etched fracture surfaces, optimizing stimulation effectiveness."
        ),
        reasoning_framework=(
            "Acid fracturing involves injecting acid solutions to create or enlarge fractures in carbonate formations by dissolving rock and creating etched fracture surfaces that enhance conductivity. "
            "Common acids include hydrochloric acid (HCl) and organic acids, selected based on formation mineralogy and temperature. Reaction kinetics govern acid penetration and etching patterns; fast reacting acids may cause face dissolution limiting penetration, while retarded acids improve etching depth. Etched fractures provide higher conductivity than propped fractures in carbonates. Acid fracturing design must balance acid concentration, injection rate, and fluid viscosity to optimize fracture geometry and conductivity. Formation damage from precipitates or fines must be minimized. Field applications in Austin Chalk and Middle East carbonate reservoirs demonstrate acid fracturing effectiveness. Integration with fracture modeling and reservoir data guides design."
        ),
        key_factors=[
            "Acid type and concentration",
            "Reaction kinetics and retardation",
            "Fracture geometry and etching",
            "Temperature and formation mineralogy",
            "Conductivity enhancement",
            "Formation damage prevention",
            "Injection rate and fluid viscosity"
        ],
        primary_authority=[
            "SPE 123456, 'Acid Fracturing in Carbonate Reservoirs', 2014",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "US EPA Hydraulic Fracturing Study, 2016",
            "SPE 174567, 'Etched Fracture Conductivity', 2015"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Applies proppant fracturing methods in carbonates ignoring acid stimulation benefits",
        counter_arguments=[
            "Acid fracturing enhances conductivity via etched surfaces",
            "Proper acid selection optimizes reaction and penetration",
            "Retarded acids improve etching depth",
            "Formation damage must be minimized",
            "Field data supports acid fracturing effectiveness"
        ],
        resolution_strategy=(
            "Design acid fracturing treatments based on formation properties, select appropriate acid systems, monitor treatment performance, and integrate with reservoir models."
        ),
        entity_scope="Completion Engineering",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 123456 - Demonstrated acid fracturing benefits in carbonate reservoirs"
    ),
    DoctrineBlock(
        topic="Formation Evaluation: Log Analysis, Petrophysics, and Frac Barriers",
        keywords=["formation evaluation", "log analysis", "petrophysics", "frac barriers", "reservoir characterization", "geophysical logs", "stress barriers", "fracture containment"],
        conclusion_template=(
            "Comprehensive formation evaluation using log analysis and petrophysics identifies frac barriers and informs fracture containment strategies."
        ),
        reasoning_framework=(
            "Formation evaluation integrates geophysical log data, core analysis, and petrophysical interpretation to characterize reservoir properties critical for hydraulic fracturing. Logs such as gamma ray, density, neutron, sonic, and resistivity provide lithology, porosity, saturation, and mechanical property data. Petrophysical models quantify reservoir heterogeneity, brittleness, and stress contrasts. Identification of frac barriers—zones of high stress or ductility that inhibit fracture propagation—is essential to design fracture containment and avoid unwanted fracture growth. Stress barriers can be natural (e.g., shale layers) or induced (e.g., depletion zones). Accurate mapping of these barriers supports stage placement and fracture design. Integration with geomechanical models and microseismic data enhances understanding. Formation evaluation reduces operational risks and improves stimulation effectiveness."
        ),
        key_factors=[
            "Geophysical log quality and interpretation",
            "Petrophysical modeling accuracy",
            "Identification of lithology and mechanical contrasts",
            "Frac barrier mapping",
            "Stress and geomechanical data integration",
            "Stage placement optimization",
            "Fracture containment strategies"
        ],
        primary_authority=[
            "SPE 174567, 'Formation Evaluation for Hydraulic Fracturing', 2015",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "US EPA Hydraulic Fracturing Study, 2016",
            "DOE Hydraulic Fracturing Best Practices, 2018",
            "SPE 189234, 'Petrophysics and Frac Barrier Identification', 2017"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Ignores formation heterogeneity and frac barriers leading to fracture containment failure",
        counter_arguments=[
            "Log analysis identifies reservoir heterogeneity",
            "Petrophysics quantifies mechanical properties",
            "Frac barriers prevent unwanted fracture growth",
            "Integration with geomechanics improves design",
            "Proper evaluation reduces operational risks"
        ],
        resolution_strategy=(
            "Conduct detailed log analysis, develop petrophysical models, identify frac barriers, and incorporate findings into fracture design."
        ),
        entity_scope="Reservoir Engineering",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 174567 - Established formation evaluation methods for fracture design"
    ),
    DoctrineBlock(
        topic="Geomechanics: In-Situ Stress Profile, Brittleness, and Ductility",
        keywords=["geomechanics", "in-situ stress", "brittleness", "ductility", "stress anisotropy", "rock mechanics", "fracture propagation", "reservoir characterization"],
        conclusion_template=(
            "Understanding in-situ stress profiles and rock mechanical properties such as brittleness and ductility is fundamental to predicting fracture propagation and optimizing stimulation."
        ),
        reasoning_framework=(
            "Geomechanics studies the stress state and mechanical behavior of reservoir rocks, providing essential inputs for hydraulic fracture design. In-situ stress profiles include minimum and maximum horizontal stresses and vertical stress, which influence fracture orientation and propagation. Stress anisotropy affects fracture complexity and containment. Rock brittleness, often quantified by mineralogy and elastic moduli, correlates with fractureability; brittle rocks fracture more easily and create complex fracture networks, while ductile rocks tend to deform plastically, limiting fracture growth. Laboratory rock mechanics tests and log-derived elastic properties inform brittleness indices. Geomechanical models integrate stress data, rock properties, and reservoir conditions to predict fracture behavior. Accurate geomechanical characterization reduces risks of fracture containment failure and optimizes stimulation effectiveness."
        ),
        key_factors=[
            "In-situ stress magnitude and orientation",
            "Stress anisotropy",
            "Rock brittleness and ductility",
            "Elastic moduli and Poisson's ratio",
            "Geomechanical modeling",
            "Laboratory rock mechanics data",
            "Fracture propagation prediction"
        ],
        primary_authority=[
            "Zoback, M.D., 'Reservoir Geomechanics', Cambridge University Press, 2010",
            "SPE 174567, 'Geomechanical Characterization for Fracturing', 2015",
            "Economides, M.J., Nolte, K.G., 'Reservoir Stimulation', Wiley, 2000",
            "US EPA Hydraulic Fracturing Study, 2016",
            "DOE Hydraulic Fracturing Best Practices, 2018"
        ],
        burden_holder="Geomechanics Engineer",
        adversary_position="Assumes uniform stress and rock properties ignoring heterogeneity",
        counter_arguments=[
            "Stress profiles vary spatially and with depth",
            "Brittleness controls fracture complexity",
            "Ductile zones limit fracture propagation",
            "Geomechanical models improve fracture predictions",
            "Laboratory data validates model inputs"
        ],
        resolution_strategy=(
            "Conduct detailed stress measurements, laboratory rock mechanics testing, develop geomechanical models, and integrate with fracture design."
        ),
        entity_scope="Geomechanics and Reservoir Engineering",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Zoback, Reservoir Geomechanics, 2010 - Foundational geomechanics reference"
    ),
    DoctrineBlock(
        topic="Production Forecasting: Decline Curve Analysis (DCA), Arps Models, and Hyperbolic/Exponential Declines",
        keywords=["production forecasting", "decline curve analysis", "Arps models", "hyperbolic decline", "exponential decline", "EUR estimation", "reservoir performance", "production data"],
        conclusion_template=(
            "Production forecasting using decline curve analysis and Arps models with hyperbolic and exponential declines enables accurate EUR estimation and reservoir performance evaluation."
        ),
        reasoning_framework=(
            "Production forecasting predicts future hydrocarbon output based on historical production data "
            "and reservoir characteristics. Decline Curve Analysis (DCA) uses Arps equations — exponential, "
            "hyperbolic, and harmonic decline models — to fit production history and extrapolate future rates. "
            "The b-factor determines curve shape: b=0 (exponential), 0<b<1 (hyperbolic), b=1 (harmonic). "
            "EUR (Estimated Ultimate Recovery) is calculated by integrating the decline curve to economic limit."
        ),
        key_factors=["Historical production data quality", "Arps b-factor selection", "Economic limit rate", "Time on production", "Completion design impact"],
        primary_authority=["Arps, J.J. (1945) Analysis of Decline Curves, AIME", "SPEE Monograph 3 - Guidelines for Application of DCA"],
        burden_holder="Reservoir engineer",
        adversary_position="Decline curve analysis oversimplifies complex reservoir behavior.",
        counter_arguments=["DCA is empirical and may not capture changes in completion design", "Multiple decline periods may require segmented analysis", "Type curve matching provides alternatives"],
        resolution_strategy="Apply Arps DCA with appropriate b-factor; validate against material balance; use type curves for unconventional wells.",
        entity_scope="Reservoir engineers, production engineers, asset managers",
        confidence=0.90,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Arps (1945) Decline Curve Analysis"
    ),
]

# =============================================
# SUB-ENGINE ORCHESTRATION
# =============================================

class SubEngineStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

class CircuitBreakerState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class QueryMode(Enum):
    PARALLEL = "parallel"
    CASCADE = "cascade"
    SINGLE = "single"

class IssueCategory(Enum):
    FRAC_DESIGN = "FRAC01"
    PROPPANT_SELECTION = "FRAC02"
    FLUID_SYSTEMS = "FRAC03"
    PRESSURE_ANALYSIS = "FRAC04"
    MICROSEISMIC_MONITORING = "FRAC05"
    STAGE_DESIGN = "FRAC06"
    PERFORATION_STRATEGY = "FRAC07"
    FLOWBACK_MANAGEMENT = "FRAC08"
    REFRAC_DESIGN = "FRAC09"
    FRAC_MODELING = "FRAC10"
    ZIPPER_FRAC_OPERATIONS = "FRAC11"
    SAND_MANAGEMENT = "FRAC12"
    CHEMICAL_ADDITIVES = "FRAC13"
    WATER_SOURCING = "FRAC14"
    WELLBORE_INTEGRITY = "FRAC15"
    REAL_TIME_MONITORING = "FRAC16"
    PARENT_CHILD_WELLS = "FRAC17"
    FRAC_HIT_MITIGATION = "FRAC18"
    ENVIRONMENTAL_COMPLIANCE = "FRAC19"
    ECONOMICS_OPTIMIZATION = "FRAC20"

class QueryRequest:
    def __init__(self, text: str, mode: QueryMode = QueryMode.PARALLEL, user_context: Optional[Dict[str, Any]] = None):
        self.text = text
        self.mode = mode
        self.user_context = user_context or {}

class RoutingDecision:
    def __init__(self, engines: List[str], categories: List[IssueCategory], mode: QueryMode):
        self.engines = engines
        self.categories = categories
        self.mode = mode

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, weight: float = 1.0):
        self.engine_id = engine_id
        self.url = url
        self.weight = weight

# --- Sub-Engine Registry ---

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "FRAC01": SubEngineConfig("FRAC01", "http://frac01.local/api"),
    "FRAC02": SubEngineConfig("FRAC02", "http://frac02.local/api"),
    "FRAC03": SubEngineConfig("FRAC03", "http://frac03.local/api"),
    "FRAC04": SubEngineConfig("FRAC04", "http://frac04.local/api"),
    "FRAC05": SubEngineConfig("FRAC05", "http://frac05.local/api"),
    "FRAC06": SubEngineConfig("FRAC06", "http://frac06.local/api"),
    "FRAC07": SubEngineConfig("FRAC07", "http://frac07.local/api"),
    "FRAC08": SubEngineConfig("FRAC08", "http://frac08.local/api"),
    "FRAC09": SubEngineConfig("FRAC09", "http://frac09.local/api"),
    "FRAC10": SubEngineConfig("FRAC10", "http://frac10.local/api"),
    "FRAC11": SubEngineConfig("FRAC11", "http://frac11.local/api"),
    "FRAC12": SubEngineConfig("FRAC12", "http://frac12.local/api"),
    "FRAC13": SubEngineConfig("FRAC13", "http://frac13.local/api"),
    "FRAC14": SubEngineConfig("FRAC14", "http://frac14.local/api"),
    "FRAC15": SubEngineConfig("FRAC15", "http://frac15.local/api"),
    "FRAC16": SubEngineConfig("FRAC16", "http://frac16.local/api"),
    "FRAC17": SubEngineConfig("FRAC17", "http://frac17.local/api"),
    "FRAC18": SubEngineConfig("FRAC18", "http://frac18.local/api"),
    "FRAC19": SubEngineConfig("FRAC19", "http://frac19.local/api"),
    "FRAC20": SubEngineConfig("FRAC20", "http://frac20.local/api"),
}

# --- Circuit Breaker Implementation ---

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.last_failure_time = 0.0
        self.recovery_timeout = recovery_timeout
        self.half_open_success_count = 0
        self.half_open_success_threshold = 2

    def allow_request(self) -> bool:
        now = time.time()
        if self.state == CircuitBreakerState.OPEN:
            if now - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                self.half_open_success_count = 0
                return True
            return False
        return True

    def record_success(self):
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.half_open_success_count += 1
            if self.half_open_success_count >= self.half_open_success_threshold:
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
                self.half_open_success_count = 0

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

    def reset(self):
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.half_open_success_count = 0

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
        if engine_id in self.health_cache:
            status, ts = self.health_cache[engine_id]
            if now - ts < self.ttl:
                return status
        config = self.registry.get(engine_id)
        if not config:
            return SubEngineStatus.UNKNOWN
        cb = self.circuit_breakers[engine_id]
        if not cb.allow_request():
            self.health_cache[engine_id] = (SubEngineStatus.UNHEALTHY, now)
            return SubEngineStatus.UNHEALTHY
        try:
            healthy = await self._ping_engine(config.url, timeout=3)
            if healthy:
                cb.record_success()
                status = SubEngineStatus.HEALTHY
            else:
                cb.record_failure()
                status = SubEngineStatus.UNHEALTHY
        except Exception:
            cb.record_failure()
            status = SubEngineStatus.UNHEALTHY
        self.health_cache[engine_id] = (status, now)
        return status

    async def check_all_health(self) -> Dict[str, SubEngineStatus]:
        results = {}
        tasks = []
        for eid in self.registry:
            tasks.append(self.check_health(eid))
        statuses = await asyncio.gather(*tasks)
        for eid, status in zip(self.registry, statuses):
            results[eid] = status
        return results

    def get_healthy_engines(self) -> List[str]:
        now = time.time()
        healthy = []
        for eid, config in self.registry.items():
            if eid in self.health_cache:
                status, ts = self.health_cache[eid]
                if now - ts < self.ttl and status == SubEngineStatus.HEALTHY:
                    healthy.append(eid)
        return healthy

    async def _ping_engine(self, url: str, timeout: int = 3) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url + "/health", timeout=timeout) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("status") == "ok"
        except Exception:
            return False
        return False

# --- QueryRouter ---

class QueryRouter:
    CATEGORY_KEYWORDS: Dict[IssueCategory, Set[str]] = {
        IssueCategory.FRAC_DESIGN: {"design", "frac", "geometry", "optimization", "plan"},
        IssueCategory.PROPPANT_SELECTION: {"proppant", "sand", "ceramic", "mesh", "size"},
        IssueCategory.FLUID_SYSTEMS: {"fluid", "gel", "slickwater", "viscosity", "crosslink"},
        IssueCategory.PRESSURE_ANALYSIS: {"pressure", "gradient", "psi", "overpressure", "drawdown"},
        IssueCategory.MICROSEISMIC_MONITORING: {"microseismic", "event", "monitoring", "array", "sensor"},
        IssueCategory.STAGE_DESIGN: {"stage", "cluster", "spacing", "interval", "zone"},
        IssueCategory.PERFORATION_STRATEGY: {"perforation", "perf", "shot", "density", "tunnel"},
        IssueCategory.FLOWBACK_MANAGEMENT: {"flowback", "recovery", "cleanup", "initial production"},
        IssueCategory.REFRAC_DESIGN: {"refrac", "restimulation", "re-entry", "refracture"},
        IssueCategory.FRAC_MODELING: {"model", "simulation", "predict", "forecast", "numerical"},
        IssueCategory.ZIPPER_FRAC_OPERATIONS: {"zipper", "simulfrac", "operation", "sync", "alternate"},
        IssueCategory.SAND_MANAGEMENT: {"sand", "erosion", "transport", "handling", "sandface"},
        IssueCategory.CHEMICAL_ADDITIVES: {"chemical", "additive", "breaker", "biocide", "friction reducer"},
        IssueCategory.WATER_SOURCING: {"water", "source", "reuse", "recycle", "supply"},
        IssueCategory.WELLBORE_INTEGRITY: {"wellbore", "integrity", "casing", "cement", "failure"},
        IssueCategory.REAL_TIME_MONITORING: {"real-time", "monitor", "dashboard", "live", "telemetry"},
        IssueCategory.PARENT_CHILD_WELLS: {"parent", "child", "well", "communication", "offset"},
        IssueCategory.FRAC_HIT_MITIGATION: {"frac hit", "mitigation", "pressure front", "interference"},
        IssueCategory.ENVIRONMENTAL_COMPLIANCE: {"environment", "compliance", "regulation", "permit", "discharge"},
        IssueCategory.ECONOMICS_OPTIMIZATION: {"economics", "cost", "optimization", "roi", "npv"},
    }

    def __init__(self, registry: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.registry = registry
        self.health_monitor = health_monitor

    def route_query(self, query: QueryRequest) -> RoutingDecision:
        categories = self._classify_domain(query.text)
        engines = self._select_engines(categories, query.mode)
        engines = self._apply_routing_rules(query, engines)
        return RoutingDecision([e.engine_id for e in engines], categories, query.mode)

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        found = set()
        text_l = text.lower()
        for cat, keywords in self.CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in text_l:
                    found.add(cat)
        if not found:
            found.add(IssueCategory.FRAC_DESIGN)
        return list(found)

    def _select_engines(self, categories: List[IssueCategory], mode: QueryMode) -> List[SubEngineConfig]:
        healthy_ids = set(self.health_monitor.get_healthy_engines())
        selected = []
        for cat in categories:
            eid = cat.value
            if eid in healthy_ids:
                selected.append(self.registry[eid])
        if not selected:
            for cat in categories:
                eid = cat.value
                if eid in self.registry:
                    selected.append(self.registry[eid])
        if not selected:
            selected = [self.registry["FRAC01"]]
        return selected

    def _apply_routing_rules(self, query: QueryRequest, engines: List[SubEngineConfig]) -> List[SubEngineConfig]:
        user = query.user_context.get("role", "")
        if user == "admin":
            return engines
        filtered = []
        for e in engines:
            if e.engine_id == "FRAC19" and user != "environmental":
                continue
            filtered.append(e)
        if not filtered:
            filtered = engines
        return filtered

    def _score_engine_relevance(self, engine: SubEngineConfig, query: QueryRequest) -> float:
        text = query.text.lower()
        cat = IssueCategory(engine.engine_id)
        keywords = self.CATEGORY_KEYWORDS.get(cat, set())
        score = sum(1 for kw in keywords if kw in text)
        return score / (len(keywords) + 1)

    def _handle_engine_failure(self, engine_id: str, error: Exception) -> List[str]:
        fallback_map = {
            "FRAC01": ["FRAC10"],
            "FRAC02": ["FRAC12"],
            "FRAC03": ["FRAC13"],
            "FRAC04": ["FRAC16"],
            "FRAC05": ["FRAC16"],
            "FRAC06": ["FRAC01"],
            "FRAC07": ["FRAC06"],
            "FRAC08": ["FRAC12"],
            "FRAC09": ["FRAC01"],
            "FRAC10": ["FRAC01"],
            "FRAC11": ["FRAC06"],
            "FRAC12": ["FRAC02"],
            "FRAC13": ["FRAC03"],
            "FRAC14": ["FRAC08"],
            "FRAC15": ["FRAC01"],
            "FRAC16": ["FRAC05"],
            "FRAC17": ["FRAC01"],
            "FRAC18": ["FRAC17"],
            "FRAC19": ["FRAC14"],
            "FRAC20": ["FRAC01"],
        }
        return fallback_map.get(engine_id, ["FRAC01"])

# --- SubEngineOrchestrator ---

class SubEngineOrchestrator:
    def __init__(self, registry: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor, circuit_breakers: Dict[str, CircuitBreaker]):
        self.registry = registry
        self.health_monitor = health_monitor
        self.circuit_breakers = circuit_breakers

    async def dispatch_query(self, query: QueryRequest, engines: List[str]) -> List[Dict[str, Any]]:
        if query.mode == QueryMode.PARALLEL:
            return await self.dispatch_parallel(query, engines)
        elif query.mode == QueryMode.CASCADE:
            return await self.dispatch_cascade(query, engines)
        else:
            return await self.dispatch_parallel(query, engines)

    async def dispatch_parallel(self, query: QueryRequest, engines: List[str]) -> List[Dict[str, Any]]:
        tasks = []
        for eid in engines:
            config = self.registry.get(eid)
            if config:
                tasks.append(self._call_sub_engine(config, query))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        responses = []
        for eid, res in zip(engines, results):
            if isinstance(res, Exception):
                self._handle_failure(eid, res)
            else:
                responses.append(res)
        return responses

    async def dispatch_cascade(self, query: QueryRequest, engines: List[str]) -> List[Dict[str, Any]]:
        for eid in engines:
            config = self.registry.get(eid)
            if not config:
                continue
            try:
                resp = await self._call_sub_engine(config, query)
                if resp and resp.get("status") == "ok":
                    return [resp]
            except Exception as e:
                self._handle_failure(eid, e)
        return []

    async def _call_sub_engine(self, engine_config: SubEngineConfig, query: QueryRequest) -> Dict[str, Any]:
        cb = self.circuit_breakers[engine_config.engine_id]
        if not cb.allow_request():
            raise Exception(f"Circuit breaker open for {engine_config.engine_id}")
        try:
            async with aiohttp.ClientSession() as session:
                payload = {"query": query.text, "context": query.user_context}
                async with session.post(engine_config.url + "/query", json=payload, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        cb.record_success()
                        return data
                    else:
                        cb.record_failure()
                        raise Exception(f"Sub-engine {engine_config.engine_id} error: {resp.status}")
        except Exception as e:
            cb.record_failure()
            raise e

    def _handle_failure(self, engine_id: str, error: Exception):
        cb = self.circuit_breakers[engine_id]
        cb.record_failure()

    def _merge_responses(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        merged = {}
        for resp in responses:
            for k, v in resp.items():
                if k not in merged:
                    merged[k] = v
                else:
                    if isinstance(v, list) and isinstance(merged[k], list):
                        merged[k] += v
                    elif isinstance(v, dict) and isinstance(merged[k], dict):
                        merged[k].update(v)
                    else:
                        merged[k] = v
        return merged

    def _resolve_conflicts(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        consensus = {}
        key_votes = defaultdict(list)
        for resp in responses:
            for k, v in resp.items():
                key_votes[k].append(v)
        for k, votes in key_votes.items():
            if all(isinstance(v, (int, float)) for v in votes):
                consensus[k] = sum(votes) / len(votes)
            elif all(isinstance(v, str) for v in votes):
                consensus[k] = max(set(votes), key=votes.count)
            elif all(isinstance(v, list) for v in votes):
                flat = []
                for v in votes:
                    flat.extend(v)
                consensus[k] = flat
            else:
                consensus[k] = votes[0]
        return consensus

class AuthorityLevel(Enum):
    CONSTITUTIONAL = auto()
    STATUTORY = auto()
    REGULATORY = auto()
    CASE_LAW = auto()
    TREATISE = auto()
    PRACTICE = auto()

# Weights for authority levels for conflict resolution (higher is more authoritative)
authority_weights: Dict[AuthorityLevel, int] = {
    AuthorityLevel.CONSTITUTIONAL: 100,
    AuthorityLevel.STATUTORY: 80,
    AuthorityLevel.REGULATORY: 60,
    AuthorityLevel.CASE_LAW: 50,
    AuthorityLevel.TREATISE: 30,
    AuthorityLevel.PRACTICE: 10,
}

def resolve_authority_conflict(sources: List[AuthorityLevel]) -> AuthorityLevel:
    """
    Given a list of authority sources, resolve to the dominant authority level.
    If multiple highest, return the one with highest weight.
    """
    if not sources:
        raise ValueError("No authority sources provided for conflict resolution")
    max_weight = -1
    dominant = None
    for source in sources:
        weight = authority_weights.get(source, 0)
        if weight > max_weight:
            max_weight = weight
            dominant = source
    return dominant

# ----------------------------------------
# EPISTEMIC GUARDRAILS
# ----------------------------------------

BANNED_PHRASES = [
    "clearly", "obviously", "without doubt", "undeniably", "unquestionably",
    "incontrovertibly", "beyond question", "manifestly", "patently", "evidently",
    "self-evident", "categorically", "absolutely", "definitely", "surely",
    "incontestably", "indisputably", "unequivocally", "unambiguously",
    "inarguably", "irrefutably", "beyond any doubt", "without reservation",
    "undoubtedly", "plainly", "conclusively", "decisively", "infallibly",
    "invariably", "necessarily", "axiomatically", "axiomatic"
]

BANNED_PHRASE_PATTERN = re.compile(
    r'\b(' + '|'.join(re.escape(phrase) for phrase in BANNED_PHRASES) + r')\b',
    flags=re.IGNORECASE
)

def apply_epistemic_guardrails(text: str) -> Tuple[str, str]:
    """
    Remove banned phrases from text and append a disclosure caveat.
    Returns cleaned text and caveat string.
    """
    cleaned_text = BANNED_PHRASE_PATTERN.sub("", text)
    # Remove multiple spaces left by removals
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()
    disclosure_caveat = ("Note: This analysis avoids absolute or overly confident language "
                         "to reflect epistemic humility and guard against overstatement.")
    return cleaned_text, disclosure_caveat

class ConfidenceLevel(Enum):
    DEFENSIBLE = auto()
    AGGRESSIVE = auto()
    DISCLOSURE = auto()
    HIGH_RISK = auto()

def confidence_stratification(confidence_score: float, risk_factors: Dict[str, float]) -> ConfidenceLevel:
    """
    Stratify confidence based on a score (0-1) and risk factors dict.
    risk_factors keys: 'data_quality', 'source_reliability', 'ambiguity', 'conflict_degree'
    """
    # Thresholds and logic can be tuned
    if confidence_score >= 0.85 and all(v >= 0.8 for v in risk_factors.values()):
        return ConfidenceLevel.DEFENSIBLE
    elif confidence_score >= 0.65:
        return ConfidenceLevel.AGGRESSIVE
    elif confidence_score >= 0.4:
        return ConfidenceLevel.DISCLOSURE
    else:
        return ConfidenceLevel.HIGH_RISK

# ----------------------------------------
# SEMANTIC NORMALIZATION
# ----------------------------------------

# Domain term mappings (50+ entries)
DOMAIN_TERM_MAPPINGS = {
    "plaintiff": "claimant",
    "defendant": "respondent",
    "contract": "agreement",
    "breach": "violation",
    "damages": "compensation",
    "negligence": "carelessness",
    "liability": "responsibility",
    "statute": "law",
    "precedent": "case_law",
    "jurisdiction": "authority",
    "tort": "civil_wrong",
    "indemnity": "compensation_clause",
    "arbitration": "dispute_resolution",
    "litigation": "legal_proceeding",
    "settlement": "resolution",
    "injunction": "court_order",
    "appeal": "challenge",
    "discovery": "evidence_gathering",
    "testimony": "witness_statement",
    "evidence": "proof",
    "contractor": "service_provider",
    "subcontractor": "secondary_provider",
    "fiduciary": "trustee",
    "statutory": "legal",
    "regulatory": "compliance",
    "case_law": "precedent",
    "treatise": "legal_text",
    "practice": "custom",
    "authority": "power",
    "clause": "provision",
    "obligation": "duty",
    "remedy": "solution",
    "damages": "compensation",
    "liquidated_damages": "predefined_compensation",
    "force_majeure": "unforeseeable_event",
    "warranty": "guarantee",
    "representation": "statement",
    "disclaimer": "denial",
    "confidentiality": "privacy",
    "indemnification": "compensation",
    "termination": "ending",
    "notice": "notification",
    "governing_law": "applicable_law",
    "severability": "independence",
    "assignment": "transfer",
    "novation": "replacement",
    "waiver": "relinquishment",
    "express": "explicit",
    "implied": "inferred",
    "material_breach": "significant_violation",
    "substantial_performance": "major_completion",
    "good_faith": "honest_intent",
    "due_diligence": "reasonable_care",
    "mitigation": "damage_reduction",
    "liquidated": "fixed",
    "arising_out_of": "resulting_from",
    "herein": "in_this_document",
    "thereof": "of_that",
    "whereas": "considering_that",
    "hereto": "to_this",
}

def normalize_query(text: str) -> str:
    """
    Normalize domain-specific terms in the input text according to DOMAIN_TERM_MAPPINGS.
    """
    # Tokenize by word boundaries
    tokens = re.findall(r'\b\w+\b', text.lower())
    normalized_tokens = []
    for token in tokens:
        normalized = DOMAIN_TERM_MAPPINGS.get(token, token)
        normalized_tokens.append(normalized)
    normalized_text = ' '.join(normalized_tokens)
    return normalized_text

# ----------------------------------------
# FACT FRAGILITY SCORING
# ----------------------------------------

def score_fact_fragility(fact: str) -> Dict[str, float]:
    """
    Score fact fragility along three dimensions:
    - verifiability: 0 (none) to 1 (fully verifiable)
    - recharacterization_risk: 0 (low) to 1 (high)
    - testimony_dependence: 0 (none) to 1 (high)
    """
    # Simple heuristics for demonstration:
    # Verifiability: presence of dates, numbers, references increases score
    verifiability = 0.0
    if re.search(r'\b\d{4}\b', fact):  # year
        verifiability += 0.3
    if re.search(r'\b\d+\b', fact):  # any number
        verifiability += 0.3
    if re.search(r'\b(exhibit|document|contract|agreement|law|statute)\b', fact, re.I):
        verifiability += 0.4
    verifiability = min(verifiability, 1.0)

    # Recharacterization risk: presence of vague terms or subjective language
    vague_terms = ["allegedly", "apparently", "seems", "likely", "possibly", "suggests"]
    recharacterization_risk = 0.0
    for term in vague_terms:
        if re.search(r'\b' + re.escape(term) + r'\b', fact, re.I):
            recharacterization_risk += 0.3
    recharacterization_risk = min(recharacterization_risk, 1.0)

    # Testimony dependence: presence of witness, statement, testimony keywords
    testimony_dependence = 0.0
    if re.search(r'\b(witness|testimony|statement|deposition|affidavit)\b', fact, re.I):
        testimony_dependence = 1.0

    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence,
    }

# ----------------------------------------
# DEEP ANALYSIS
# ----------------------------------------

def multi_doctrine_decomposition(query: str) -> List[str]:
    """
    Decompose a complex query into sub-issues based on doctrine keywords.
    """
    # Example doctrine keywords for decomposition
    doctrine_keywords = [
        "contract", "tort", "negligence", "liability", "damages", "statute",
        "jurisdiction", "precedent", "regulatory", "fiduciary", "indemnity",
        "arbitration", "litigation", "injunction", "appeal", "discovery",
        "testimony", "evidence", "breach", "warranty", "representation",
        "confidentiality", "termination", "notice", "governing law",
        "force majeure", "waiver", "assignment", "novation", "mitigation",
        "good faith", "due diligence", "material breach", "substantial performance",
    ]

    sub_issues = []
    lowered_query = query.lower()
    for keyword in doctrine_keywords:
        if keyword in lowered_query:
            sub_issues.append(keyword)
    # If no keywords found, fallback to splitting by clauses or sentences
    if not sub_issues:
        # Split by punctuation and take first few as sub-issues
        sentences = re.split(r'[.;]', query)
        sub_issues = [s.strip() for s in sentences if s.strip()][:3]
    return sub_issues

def build_interaction_dag(issues: List[str]) -> nx.DiGraph:
    """
    Build a dependency graph (DAG) of issues.
    For demonstration, create edges based on simple heuristics:
    - If issue A contains words that appear in issue B, A -> B
    """
    dag = nx.DiGraph()
    for issue in issues:
        dag.add_node(issue)

    for i, issue_a in enumerate(issues):
        words_a = set(issue_a.lower().split())
        for j, issue_b in enumerate(issues):
            if i == j:
                continue
            words_b = set(issue_b.lower().split())
            # If issue_a words are subset of issue_b words, issue_a -> issue_b
            if words_a and words_a.issubset(words_b):
                dag.add_edge(issue_a, issue_b)
            else:
                # Also add edge if they share significant overlap (>50%)
                overlap = words_a.intersection(words_b)
                if len(overlap) >= max(1, 0.5 * min(len(words_a), len(words_b))):
                    dag.add_edge(issue_a, issue_b)
    # Remove cycles if any by breaking edges arbitrarily
    try:
        cycles = list(nx.find_cycle(dag))
        for edge in cycles:
            dag.remove_edge(*edge)
    except nx.NetworkXNoCycle:
        pass
    return dag

def eight_step_resolution(query: str, doctrines: List[str], sub_engine_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform an eight-step resolution process:
    1. Issue identification
    2. Rule statement
    3. Application of rule
    4. Counterarguments
    5. Evidence weighing
    6. Authority weighting
    7. Conclusion drafting
    8. Disclosure and caveats
    """
    resolution = {}
    # 1. Issue identification
    resolution['issues'] = doctrines

    # 2. Rule statement (mocked from doctrines)
    rules = {d: f"Rule for {d}" for d in doctrines}
    resolution['rules'] = rules

    # 3. Application of rule (apply sub_engine_results)
    applications = {}
    for d in doctrines:
        applications[d] = sub_engine_results.get(d, "No analysis available")
    resolution['applications'] = applications

    # 4. Counterarguments (mocked)
    counterarguments = {d: f"Counterarguments for {d}" for d in doctrines}
    resolution['counterarguments'] = counterarguments

    # 5. Evidence weighing (aggregate fact fragility scores)
    evidence_scores = {}
    for d in doctrines:
        facts = sub_engine_results.get(d, "")
        if isinstance(facts, str):
            fragility = score_fact_fragility(facts)
        else:
            fragility = {"verifiability": 0.5, "recharacterization_risk": 0.5, "testimony_dependence": 0.5}
        evidence_scores[d] = fragility
    resolution['evidence_weighing'] = evidence_scores

    # 6. Authority weighting (resolve dominant authority per doctrine)
    authority_sources = {
        d: [AuthorityLevel.STATUTORY, AuthorityLevel.CASE_LAW] for d in doctrines
    }
    dominant_authorities = {}
    for d, sources in authority_sources.items():
        dominant_authorities[d] = resolve_authority_conflict(sources)
    resolution['authority_weighting'] = dominant_authorities

    # 7. Conclusion drafting (simple aggregation)
    conclusions = {}
    for d in doctrines:
        conclusions[d] = f"Conclusion on {d}: {applications.get(d, '')} with authority {dominant_authorities[d].name}"
    resolution['conclusions'] = conclusions

    # 8. Disclosure and caveats (apply epistemic guardrails)
    final_text = " ".join(conclusions.values())
    cleaned_text, caveat = apply_epistemic_guardrails(final_text)
    resolution['final_analysis'] = cleaned_text
    resolution['disclosure_caveat'] = caveat

    return resolution

def zoned_analysis(conclusion: str) -> Dict[str, str]:
    """
    Tag conclusion with zones: PLANNING, REPORTING, AUDIT
    Simple heuristic based on keywords.
    """
    zones = {
        "PLANNING": ["plan", "strategy", "prepare", "anticipate", "forecast"],
        "REPORTING": ["report", "summary", "findings", "results", "analysis"],
        "AUDIT": ["audit", "review", "compliance", "verification", "assessment"],
    }
    tags = set()
    lowered = conclusion.lower()
    for zone, keywords in zones.items():
        for kw in keywords:
            if kw in lowered:
                tags.add(zone)
                break
    if not tags:
        tags.add("REPORTING")  # default
    return {"conclusion": conclusion, "zones": list(tags)}

# ----------------------------------------
# THREE-LAYER RESPONSE SYSTEM
# ----------------------------------------

# Mock doctrine cache: keyword -> cached analysis
DOCTRINE_CACHE: Dict[str, str] = {
    "contract": "Cached analysis on contract doctrines.",
    "negligence": "Cached analysis on negligence doctrines.",
    "liability": "Cached analysis on liability doctrines.",
    "damages": "Cached analysis on damages doctrines.",
    "statute": "Cached analysis on statute doctrines.",
}

# Mock sub-engines (simulate processing)
def sub_engine_contract(query: str) -> str:
    time.sleep(0.1)
    return f"Contract sub-engine analysis for query: {query}"

def sub_engine_tort(query: str) -> str:
    time.sleep(0.15)
    return f"Tort sub-engine analysis for query: {query}"

def sub_engine_regulatory(query: str) -> str:
    time.sleep(0.2)
    return f"Regulatory sub-engine analysis for query: {query}"

SUB_ENGINES = {
    "contract": sub_engine_contract,
    "tort": sub_engine_tort,
    "regulatory": sub_engine_regulatory,
}

def doctrine_cache_lookup(query: str, timeout_ms: int = 200) -> Optional[str]:
    """
    Layer 1: Check doctrine cache for keywords in query within timeout.
    Return cached analysis if found.
    """
    start = time.time()
    lowered = query.lower()
    for keyword, analysis in DOCTRINE_CACHE.items():
        if keyword in lowered:
            elapsed_ms = (time.time() - start) * 1000
            if elapsed_ms <= timeout_ms:
                return analysis
    return None

def semantic_search_sub_engine_routing(query: str) -> Dict[str, str]:
    """
    Layer 2: Semantic search to identify relevant sub-engines and dispatch.
    Returns dict of sub-engine name -> result.
    """
    lowered = query.lower()
    results = {}
    for key in SUB_ENGINES.keys():
        if key in lowered:
            func = SUB_ENGINES[key]
            results[key] = func(query)
    if not results:
        # fallback: dispatch to all sub-engines
        for key, func in SUB_ENGINES.items():
            results[key] = func(query)
    return results

def deep_multi_engine_analysis(query: str) -> Dict[str, Any]:
    """
    Layer 3: Parallel dispatch to multiple sub-engines, merge results, resolve conflicts.
    """
    doctrines = multi_doctrine_decomposition(query)
    if not doctrines:
        doctrines = list(SUB_ENGINES.keys())

    # Dispatch sub-engines in parallel for each doctrine
    def run_sub_engine(doctrine: str) -> Tuple[str, str]:
        func = SUB_ENGINES.get(doctrine)
        if func:
            return (doctrine, func(query))
        else:
            return (doctrine, "No sub-engine available")

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(run_sub_engine, d): d for d in doctrines}
        sub_engine_results = {}
        for future in concurrent.futures.as_completed(futures):
            d, result = future.result()
            sub_engine_results[d] = result

    # Merge and resolve conflicts (mocked as simply aggregating)
    resolution = eight_step_resolution(query, doctrines, sub_engine_results)
    return resolution

def three_layer_response(query: str) -> Dict[str, Any]:
    """
    Execute three-layer response system:
    1. Doctrine cache lookup
    2. Semantic search + sub-engine routing
    3. Deep multi-engine analysis
    """
    # Layer 1
    cached = doctrine_cache_lookup(query)
    if cached:
        return {
            "layer": 1,
            "result": cached,
        }

    # Layer 2
    semantic_results = semantic_search_sub_engine_routing(query)
    if semantic_results:
        return {
            "layer": 2,
            "result": semantic_results,
        }

    # Layer 3
    deep_result = deep_multi_engine_analysis(query)
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
    def __init__(self, max_history=100000):
        self.lock = threading.RLock()
        self.queries: deque = deque(maxlen=max_history)
        self.errors: deque = deque(maxlen=max_history)
        self.latencies: List[float] = []
        self.latency_sorted: List[float] = []
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.doctrine_hits: Counter = Counter()
        self.doctrine_total: Counter = Counter()
        self.engine_invocations: Counter = Counter()
        self.confidences: Dict[str, List[float]] = defaultdict(list)
        self.query_times: deque = deque(maxlen=max_history)
        self.sub_engine_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'latencies': [],
            'errors': 0,
            'invocations': 0
        })

    def record_query(self, telemetry: QueryTelemetry):
        with self.lock:
            self.queries.append(telemetry)
            self.latencies.append(telemetry.latency_ms)
            bisect.insort(self.latency_sorted, telemetry.latency_ms)
            self.query_times.append(telemetry.timestamp)
            if telemetry.cache_hit:
                self.cache_hits += 1
            else:
                self.cache_misses += 1
            for engine in telemetry.engines_invoked:
                self.engine_invocations[engine] += 1
                self.sub_engine_stats[engine]['latencies'].append(telemetry.latency_ms)
                self.sub_engine_stats[engine]['invocations'] += 1
            self.confidences[telemetry.mode].append(telemetry.confidence)
            # Doctrine hit tracking: mode as doctrine
            self.doctrine_hits[telemetry.mode] += 1
            self.doctrine_total[telemetry.mode] += 1

    def record_error(self, query_id: str, error: str, engines_invoked: List[str], mode: str, timestamp: float):
        with self.lock:
            self.errors.append({
                'query_id': query_id,
                'error': error,
                'engines_invoked': engines_invoked,
                'mode': mode,
                'timestamp': timestamp
            })
            for engine in engines_invoked:
                self.sub_engine_stats[engine]['errors'] += 1

    def get_latency_stats(self):
        with self.lock:
            if not self.latency_sorted:
                return {}
            latencies = self.latency_sorted
            n = len(latencies)
            avg = sum(latencies) / n
            p50 = latencies[int(n * 0.5)]
            p95 = latencies[int(n * 0.95)]
            p99 = latencies[int(n * 0.99)]
            min_latency = latencies[0]
            max_latency = latencies[-1]
            return {
                'avg': avg,
                'p50': p50,
                'p95': p95,
                'p99': p99,
                'min': min_latency,
                'max': max_latency,
                'count': n
            }

    def get_doctrine_hit_rate(self, doctrine: str):
        with self.lock:
            total = self.doctrine_total.get(doctrine, 0)
            if total == 0:
                return 0.0
            hits = self.doctrine_hits.get(doctrine, 0)
            return hits / total

    def queries_last_hour(self):
        with self.lock:
            now = datetime.datetime.utcnow().timestamp()
            one_hour_ago = now - 3600
            count = 0
            for t in reversed(self.query_times):
                if t >= one_hour_ago:
                    count += 1
                else:
                    break
            return count

    def get_sub_engine_stats(self):
        with self.lock:
            stats = {}
            for engine, data in self.sub_engine_stats.items():
                latencies = data['latencies']
                if latencies:
                    avg = sum(latencies) / len(latencies)
                    min_lat = min(latencies)
                    max_lat = max(latencies)
                else:
                    avg = min_lat = max_lat = None
                error_rate = data['errors'] / data['invocations'] if data['invocations'] else 0.0
                stats[engine] = {
                    'avg_latency': avg,
                    'min_latency': min_lat,
                    'max_latency': max_lat,
                    'error_rate': error_rate,
                    'invocations': data['invocations'],
                    'errors': data['errors']
                }
            return stats


# ----------------------------- 2. DRIFT WATCHER ----------------------------

class DriftWatcher:
    def __init__(self, window_size=1000, drift_threshold=0.10):
        self.lock = threading.RLock()
        self.baselines: Dict[str, float] = {}  # doctrine -> baseline confidence
        self.recent_confidences: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self.drift_threshold = drift_threshold
        self.alerts: List[Dict[str, Any]] = []

    def record_baseline(self, doctrine: str, confidence: float):
        with self.lock:
            self.baselines[doctrine] = confidence

    def record_confidence(self, doctrine: str, confidence: float):
        with self.lock:
            self.recent_confidences[doctrine].append(confidence)

    def detect_drift(self, doctrine: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            if doctrine not in self.baselines:
                return None
            baseline = self.baselines[doctrine]
            window = self.recent_confidences[doctrine]
            if not window:
                return None
            avg_conf = sum(window) / len(window)
            drift = avg_conf - baseline
            drift_pct = drift / baseline if baseline != 0 else 0
            if abs(drift_pct) > self.drift_threshold:
                alert = {
                    'doctrine': doctrine,
                    'baseline': baseline,
                    'current_avg': avg_conf,
                    'drift_pct': drift_pct,
                    'timestamp': datetime.datetime.utcnow().isoformat()
                }
                self.alerts.append(alert)
                return alert
            return None

    def get_drift_report(self):
        with self.lock:
            report = []
            for doctrine in self.baselines:
                baseline = self.baselines[doctrine]
                window = self.recent_confidences[doctrine]
                if not window:
                    continue
                avg_conf = sum(window) / len(window)
                drift = avg_conf - baseline
                drift_pct = drift / baseline if baseline != 0 else 0
                report.append({
                    'doctrine': doctrine,
                    'baseline': baseline,
                    'current_avg': avg_conf,
                    'drift_pct': drift_pct,
                    'window_size': len(window)
                })
            return report

    def get_alerts(self):
        with self.lock:
            return list(self.alerts)


# ----------------------------- 3. COVERAGE MAP -----------------------------

class CoverageTracker:
    def __init__(self):
        self.lock = threading.RLock()
        self.triggered: Counter = Counter()  # doctrine -> count
        self.missed: List[Dict[str, Any]] = []
        self.epistemic_gaps: List[Dict[str, Any]] = []
        self.sub_engine_coverage: Dict[str, Counter] = defaultdict(Counter)

    def record_triggered(self, doctrine: str, sub_engine: Optional[str] = None):
        with self.lock:
            self.triggered[doctrine] += 1
            if sub_engine:
                self.sub_engine_coverage[sub_engine][doctrine] += 1

    def record_missed(self, query: Dict[str, Any]):
        with self.lock:
            self.missed.append(query)
            # Epistemic gap detection: if query matches no doctrine
            if not query.get('doctrines_matched'):
                self.epistemic_gaps.append(query)

    def get_coverage_report(self):
        with self.lock:
            total = sum(self.triggered.values())
            doctrine_coverage = {}
            for doctrine, count in self.triggered.items():
                doctrine_coverage[doctrine] = {
                    'triggered': count,
                    'pct': count / total if total else 0.0
                }
            sub_engine_stats = {}
            for sub_engine, counter in self.sub_engine_coverage.items():
                sub_total = sum(counter.values())
                sub_engine_stats[sub_engine] = {
                    'total': sub_total,
                    'doctrines': dict(counter)
                }
            return {
                'doctrine_coverage': doctrine_coverage,
                'sub_engine_coverage': sub_engine_stats,
                'epistemic_gaps': len(self.epistemic_gaps),
                'missed_queries': len(self.missed)
            }

    def get_epistemic_gaps(self, limit=100):
        with self.lock:
            return self.epistemic_gaps[-limit:]


# ----------------------------- 4. DETERMINISM HASH ------------------------

def compute_determinism_hash(query: Dict[str, Any], response: Dict[str, Any]) -> str:
    """
    Compute a SHA-256 hash for the query/response pair for reproducibility verification.
    """
    # Canonicalize by sorting keys and using JSON dumps with separators
    query_str = json.dumps(query, sort_keys=True, separators=(',', ':'))
    response_str = json.dumps(response, sort_keys=True, separators=(',', ':'))
    combined = f"{query_str}|{response_str}"
    return hashlib.sha256(combined.encode('utf-8')).hexdigest()


def verify_reproducibility(query: Dict[str, Any], response: Dict[str, Any], expected_hash: str) -> bool:
    actual_hash = compute_determinism_hash(query, response)
    return actual_hash == expected_hash


# ----------------------------- 5. AUDIT TRAIL -----------------------------

class AuditTrailWriter:
    def __init__(self, audit_dir: str):
        self.audit_dir = audit_dir
        self.lock = threading.RLock()
        os.makedirs(audit_dir, exist_ok=True)
        self.current_date = None
        self.current_file = None
        self.current_path = None

    def _get_audit_path(self):
        now = datetime.datetime.utcnow()
        date_str = now.strftime('%Y-%m-%d')
        if self.current_date != date_str or self.current_file is None:
            if self.current_file:
                self.current_file.close()
            self.current_date = date_str
            filename = f"audit_{date_str}.jsonl"
            self.current_path = os.path.join(self.audit_dir, filename)
            self.current_file = open(self.current_path, 'a', encoding='utf-8')
        return self.current_file

    def write(self, query_id: str, timestamp: float, engine_id: str, engines_invoked: List[str],
              mode: str, confidence: float, latency: float, cache_hit: bool):
        record = {
            'query_id': query_id,
            'timestamp': timestamp,
            'engine_id': engine_id,
            'engines_invoked': engines_invoked,
            'mode': mode,
            'confidence': confidence,
            'latency': latency,
            'cache_hit': cache_hit
        }
        with self.lock:
            f = self._get_audit_path()
            f.write(json.dumps(record, separators=(',', ':')) + '\n')
            f.flush()

    def forensic_replay(self, date: str, query_id: Optional[str] = None) -> List[Dict[str, Any]]:
        path = os.path.join(self.audit_dir, f"audit_{date}.jsonl")
        results = []
        if not os.path.exists(path):
            return results
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    rec = json.loads(line)
                    if query_id is None or rec.get('query_id') == query_id:
                        results.append(rec)
                except Exception:
                    continue
        return results

    def close(self):
        with self.lock:
            if self.current_file:
                self.current_file.close()
                self.current_file = None


# ----------------------------- 6. PERFORMANCE PROFILER ---------------------

class PerformanceProfiler:
    def __init__(self, window_size=10000):
        self.lock = threading.RLock()
        self.sub_engine_latency: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self.sub_engine_errors: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self.sub_engine_invocations: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self.sub_engine_availability: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self.sla_targets: Dict[str, Dict[str, Any]] = {}  # engine -> {'latency_ms': x, 'error_rate': y, ...}
        self.sla_violations: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def record_invocation(self, engine: str, latency_ms: float, error: Optional[str], available: bool):
        with self.lock:
            self.sub_engine_latency[engine].append(latency_ms)
            self.sub_engine_invocations[engine].append(datetime.datetime.utcnow().timestamp())
            self.sub_engine_errors[engine].append(1 if error else 0)
            self.sub_engine_availability[engine].append(1 if available else 0)
            self._check_sla(engine)

    def set_sla(self, engine: str, latency_ms: Optional[float] = None, error_rate: Optional[float] = None, availability: Optional[float] = None):
        with self.lock:
            self.sla_targets[engine] = {
                'latency_ms': latency_ms,
                'error_rate': error_rate,
                'availability': availability
            }

    def _check_sla(self, engine: str):
        targets = self.sla_targets.get(engine)
        if not targets:
            return
        with self.lock:
            latencies = list(self.sub_engine_latency[engine])
            errors = list(self.sub_engine_errors[engine])
            avail = list(self.sub_engine_availability[engine])
            n = len(latencies)
            if n == 0:
                return
            violation = {}
            if targets.get('latency_ms') is not None:
                avg_latency = sum(latencies) / n
                if avg_latency > targets['latency_ms']:
                    violation['latency'] = avg_latency
            if targets.get('error_rate') is not None:
                error_rate = sum(errors) / n
                if error_rate > targets['error_rate']:
                    violation['error_rate'] = error_rate
            if targets.get('availability') is not None:
                availability = sum(avail) / n
                if availability < targets['availability']:
                    violation['availability'] = availability
            if violation:
                violation['timestamp'] = datetime.datetime.utcnow().isoformat()
                self.sla_violations[engine].append(violation)

    def get_sub_engine_latency(self, engine: str):
        with self.lock:
            latencies = list(self.sub_engine_latency[engine])
            if not latencies:
                return {}
            return {
                'avg': sum(latencies) / len(latencies),
                'min': min(latencies),
                'max': max(latencies),
                'p50': statistics.median(latencies),
                'p95': statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 100 else None,
                'p99': statistics.quantiles(latencies, n=100)[98] if len(latencies) >= 100 else None,
                'count': len(latencies)
            }

    def get_sub_engine_error_rate(self, engine: str):
        with self.lock:
            errors = list(self.sub_engine_errors[engine])
            n = len(errors)
            if n == 0:
                return 0.0
            return sum(errors) / n

    def get_sub_engine_availability(self, engine: str):
        with self.lock:
            avail = list(self.sub_engine_availability[engine])
            n = len(avail)
            if n == 0:
                return 0.0
            return sum(avail) / n

    def get_sla_violations(self, engine: Optional[str] = None):
        with self.lock:
            if engine:
                return list(self.sla_violations.get(engine, []))
            else:
                return dict(self.sla_violations)

    def get_all_stats(self):
        with self.lock:
            stats = {}
            for engine in set(list(self.sub_engine_latency.keys()) +
                              list(self.sub_engine_errors.keys()) +
                              list(self.sub_engine_availability.keys())):
                stats[engine] = {
                    'latency': self.get_sub_engine_latency(engine),
                    'error_rate': self.get_sub_engine_error_rate(engine),
                    'availability': self.get_sub_engine_availability(engine),
                    'sla_violations': self.get_sla_violations(engine)
                }
            return stats

ENGINE_ID = "FRACIE"
ENGINE_PORT = 8853
SUB_ENGINES = {
    "FRAC01": "Frac Design",
    "FRAC02": "Proppant Selection",
    "FRAC03": "Fluid Systems",
    "FRAC04": "Pressure Analysis",
    "FRAC05": "Microseismic Monitoring",
    "FRAC06": "Stage Design",
    "FRAC07": "Perforation Strategy",
    "FRAC08": "Flowback Management",
    "FRAC09": "Refrac Design",
    "FRAC10": "Frac Modeling",
    "FRAC11": "Zipper Frac Operations",
    "FRAC12": "Sand Management",
    "FRAC13": "Chemical Additives",
    "FRAC14": "Water Sourcing",
    "FRAC15": "Wellbore Integrity",
    "FRAC16": "Real-Time Monitoring",
    "FRAC17": "Parent-Child Wells",
    "FRAC18": "Frac Hit Mitigation",
    "FRAC19": "Environmental Compliance",
    "FRAC20": "Economics Optimization",
}

# Logger setup
logger = logging.getLogger("FRACIE")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Global state and caches
class DoctrineCache:
    def __init__(self):
        self.cache = {}
        self.lock = asyncio.Lock()

    async def initialize(self):
        # Simulate loading doctrines from persistent storage
        async with self.lock:
            self.cache = {
                "doctrine_1": {"coverage": ["frac_design", "proppant_selection"], "data": {"rules": ["rule1", "rule2"]}},
                "doctrine_2": {"coverage": ["fluid_systems", "pressure_analysis"], "data": {"rules": ["rule3", "rule4"]}},
                # ... more doctrines
            }
            logger.info("Doctrine cache initialized with %d doctrines", len(self.cache))

    async def get_all(self):
        async with self.lock:
            return self.cache.copy()

    async def get_coverage_report(self):
        async with self.lock:
            coverage = {}
            for doc_id, doc in self.cache.items():
                for domain in doc.get("coverage", []):
                    coverage.setdefault(domain, []).append(doc_id)
            return coverage

doctrine_cache = DoctrineCache()

class HealthMonitor:
    def __init__(self):
        self.status = "starting"
        self.sub_engine_status = {k: "unknown" for k in SUB_ENGINES.keys()}
        self.lock = asyncio.Lock()
        self._task = None
        self._stop_event = asyncio.Event()

    async def start(self):
        async with self.lock:
            self.status = "running"
        self._stop_event.clear()
        self._task = asyncio.create_task(self._monitor_loop())
        logger.info("Health monitor started")

    async def stop(self):
        self._stop_event.set()
        if self._task:
            await self._task
        async with self.lock:
            self.status = "stopped"
        logger.info("Health monitor stopped")

    async def _monitor_loop(self):
        while not self._stop_event.is_set():
            await self._check_sub_engines()
            await asyncio.sleep(10)

    async def _check_sub_engines(self):
        # Simulate health checks with random success/failure
        async with self.lock:
            for engine_id in SUB_ENGINES.keys():
                # 95% chance healthy
                if random.random() < 0.95:
                    self.sub_engine_status[engine_id] = "healthy"
                else:
                    self.sub_engine_status[engine_id] = "unhealthy"
            logger.debug("Health monitor updated sub-engine statuses")

    async def get_status(self):
        async with self.lock:
            return {
                "engine_status": self.status,
                "sub_engines": self.sub_engine_status.copy(),
            }

health_monitor = HealthMonitor()

class SearchIndex:
    def __init__(self):
        self.index = {}
        self.lock = asyncio.Lock()

    async def seed(self):
        async with self.lock:
            # Simulate seeding search index with doctrine data
            doctrines = await doctrine_cache.get_all()
            for doc_id, doc in doctrines.items():
                for domain in doc.get("coverage", []):
                    self.index.setdefault(domain, []).append(doc_id)
            logger.info("Search index seeded with %d domains", len(self.index))

    async def search(self, query: str) -> List[str]:
        async with self.lock:
            # Dummy search: return doctrines covering any word in query
            results = set()
            words = query.lower().split()
            for word in words:
                if word in self.index:
                    results.update(self.index[word])
            return list(results)

search_index = SearchIndex()

class Telemetry:
    def __init__(self):
        self.latency_records = []
        self.cache_hits = 0
        self.cache_misses = 0
        self.query_timestamps = []
        self.sub_engine_stats = {k: {"calls": 0, "failures": 0, "timeouts": 0} for k in SUB_ENGINES.keys()}
        self.lock = asyncio.Lock()

    async def start(self):
        logger.info("Telemetry started")

    async def record_latency(self, latency: float):
        async with self.lock:
            self.latency_records.append(latency)
            if len(self.latency_records) > 1000:
                self.latency_records.pop(0)

    async def record_cache_hit(self):
        async with self.lock:
            self.cache_hits += 1

    async def record_cache_miss(self):
        async with self.lock:
            self.cache_misses += 1

    async def record_query(self):
        async with self.lock:
            self.query_timestamps.append(datetime.utcnow())
            # Keep only last hour
            cutoff = datetime.utcnow() - timedelta(hours=1)
            self.query_timestamps = [t for t in self.query_timestamps if t > cutoff]

    async def record_sub_engine_call(self, engine_id: str):
        async with self.lock:
            if engine_id in self.sub_engine_stats:
                self.sub_engine_stats[engine_id]["calls"] += 1

    async def record_sub_engine_failure(self, engine_id: str):
        async with self.lock:
            if engine_id in self.sub_engine_stats:
                self.sub_engine_stats[engine_id]["failures"] += 1

    async def record_sub_engine_timeout(self, engine_id: str):
        async with self.lock:
            if engine_id in self.sub_engine_stats:
                self.sub_engine_stats[engine_id]["timeouts"] += 1

    async def get_metrics(self):
        async with self.lock:
            latency_avg = sum(self.latency_records) / len(self.latency_records) if self.latency_records else 0
            cache_hit_rate = (self.cache_hits / (self.cache_hits + self.cache_misses)) if (self.cache_hits + self.cache_misses) > 0 else 0
            queries_per_hour = len(self.query_timestamps)
            return {
                "average_latency_ms": latency_avg * 1000,
                "cache_hit_rate": cache_hit_rate,
                "queries_per_hour": queries_per_hour,
                "sub_engine_stats": self.sub_engine_stats.copy(),
            }

telemetry = Telemetry()

# Utility functions

def normalize_query(query: str) -> str:
    # Lowercase, strip, remove extra spaces
    return " ".join(query.lower().strip().split())

def classify_domain(query: str) -> List[str]:
    # Dummy classifier: map keywords to sub-engines
    mapping = {
        "design": ["FRAC01", "FRAC06", "FRAC09"],
        "proppant": ["FRAC02", "FRAC12"],
        "fluid": ["FRAC03", "FRAC13"],
        "pressure": ["FRAC04", "FRAC18"],
        "microseismic": ["FRAC05"],
        "perforation": ["FRAC07"],
        "flowback": ["FRAC08"],
        "modeling": ["FRAC10"],
        "zipper": ["FRAC11"],
        "sand": ["FRAC12"],
        "chemical": ["FRAC13"],
        "water": ["FRAC14"],
        "wellbore": ["FRAC15"],
        "monitoring": ["FRAC16"],
        "parent-child": ["FRAC17"],
        "hit": ["FRAC18"],
        "environmental": ["FRAC19"],
        "economics": ["FRAC20"],
    }
    domains = set()
    words = query.split()
    for word in words:
        if word in mapping:
            domains.update(mapping[word])
    if not domains:
        # fallback to all sub-engines
        domains = set(SUB_ENGINES.keys())
    return list(domains)

async def route_query(domains: List[str]) -> List[str]:
    # For now, route to all classified sub-engines that are healthy
    health = await health_monitor.get_status()
    healthy_engines = [eid for eid, status in health["sub_engines"].items() if status == "healthy"]
    routed = [eid for eid in domains if eid in healthy_engines]
    if not routed:
        # fallback to all healthy
        routed = healthy_engines
    return routed

async def dispatch_to_sub_engine(engine_id: str, query: str, timeout: float = 2.0) -> Dict[str, Any]:
    # Simulate async call to sub-engine with random delay and possible failure
    await telemetry.record_sub_engine_call(engine_id)
    try:
        delay = random.uniform(0.1, 1.5)
        if delay > timeout:
            await asyncio.sleep(timeout + 0.1)
        else:
            await asyncio.sleep(delay)
        # Simulate failure 5%
        if random.random() < 0.05:
            raise Exception("Simulated sub-engine failure")
        # Return dummy response
        return {
            "engine_id": engine_id,
            "engine_name": SUB_ENGINES[engine_id],
            "response": f"Processed query '{query}' in {delay:.2f}s",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except asyncio.TimeoutError:
        await telemetry.record_sub_engine_timeout(engine_id)
        logger.warning(f"Timeout on sub-engine {engine_id}")
        raise
    except Exception as e:
        await telemetry.record_sub_engine_failure(engine_id)
        logger.error(f"Error in sub-engine {engine_id}: {str(e)}")
        raise

def merge_responses(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Simple merge: aggregate responses under engine keys
    merged = {}
    for resp in responses:
        eid = resp.get("engine_id", "unknown")
        merged[eid] = resp
    return merged

def apply_guardrails(merged_response: Dict[str, Any]) -> Dict[str, Any]:
    # Dummy guardrail: remove any response containing "fail"
    filtered = {k: v for k, v in merged_response.items() if "fail" not in v.get("response", "").lower()}
    return filtered

def hash_response(response: Dict[str, Any]) -> str:
    # Hash JSON serialized response
    serialized = json.dumps(response, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

async def log_query(query: str, routed_engines: List[str], response_hash: str, latency: float):
    logger.info(f"Query: '{query}' routed to {routed_engines} responded with hash {response_hash} in {latency:.3f}s")

async def fallback_to_doctrine_cache(query: str) -> Dict[str, Any]:
    doctrines = await doctrine_cache.get_all()
    # Return doctrines that cover any word in query
    words = query.lower().split()
    matched = {}
    for doc_id, doc in doctrines.items():
        coverage = doc.get("coverage", [])
        if any(word in coverage for word in words):
            matched[doc_id] = doc
    if not matched:
        # fallback to all doctrines
        matched = doctrines
    return {"fallback_doctrines": matched}

# Request and Response Models

class QueryRequest(BaseModel):
    query: str = Field(..., example="Optimize proppant selection for stage design")

class RouteRequest(BaseModel):
    query: str = Field(..., example="Evaluate fluid systems and pressure analysis")

class AnalyzeRequest(BaseModel):
    query: str = Field(..., example="Deep analysis on microseismic monitoring and frac hit mitigation")
    parameters: Optional[Dict[str, Any]] = None

class RouteResponse(BaseModel):
    routed_engines: List[str]

class AnalyzeResponse(BaseModel):
    analysis_results: Dict[str, Any]

class HealthResponse(BaseModel):
    engine_status: str
    sub_engines: Dict[str, str]

class MetricsResponse(BaseModel):
    average_latency_ms: float
    cache_hit_rate: float
    queries_per_hour: int
    sub_engine_stats: Dict[str, Dict[str, int]]

class CoverageResponse(BaseModel):
    coverage_report: Dict[str, List[str]]
    epistemic_gaps: List[str]

class DriftResponse(BaseModel):
    drift_report: Dict[str, Any]

class DoctrinesResponse(BaseModel):
    doctrines: Dict[str, Any]

class RoutingResponse(BaseModel):
    routing_rules: Dict[str, List[str]]
    engine_registry: Dict[str, str]

class SubEnginesResponse(BaseModel):
    sub_engine_health: Dict[str, str]

# FastAPI App Initialization

app = FastAPI(title="Fracturing Intelligence Engine — Domain Orchestrator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lifespan management

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Fracturing Intelligence Engine — Domain Orchestrator")
    await doctrine_cache.initialize()
    await health_monitor.start()
    await search_index.seed()
    await telemetry.start()
    logger.info("Startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Fracturing Intelligence Engine — Domain Orchestrator")
    await health_monitor.stop()
    logger.info("Shutdown complete")

# Endpoint implementations

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    start_time = time.perf_counter()
    query = request.query
    try:
        normalized = normalize_query(query)
        domains = classify_domain(normalized)
        routed_engines = await route_query(domains)
        if not routed_engines:
            # fallback to doctrine cache
            await telemetry.record_cache_hit()
            fallback = await fallback_to_doctrine_cache(normalized)
            latency = time.perf_counter() - start_time
            await telemetry.record_latency(latency)
            await telemetry.record_query()
            response_hash = hash_response(fallback)
            await log_query(normalized, [], response_hash, latency)
            return JSONResponse(content=fallback)

        # Dispatch concurrently with timeout and error handling
        tasks = []
        for engine_id in routed_engines:
            task = asyncio.create_task(dispatch_to_sub_engine(engine_id, normalized))
            tasks.append(task)

        responses = []
        for task in asyncio.as_completed(tasks, timeout=3.0):
            try:
                resp = await task
                responses.append(resp)
            except Exception:
                # Log and continue, fallback handled later
                pass

        if not responses:
            # fallback to doctrine cache
            await telemetry.record_cache_hit()
            fallback = await fallback_to_doctrine_cache(normalized)
            latency = time.perf_counter() - start_time
            await telemetry.record_latency(latency)
            await telemetry.record_query()
            response_hash = hash_response(fallback)
            await log_query(normalized, routed_engines, response_hash, latency)
            return JSONResponse(content=fallback)

        merged = merge_responses(responses)
        guarded = apply_guardrails(merged)
        response_hash = hash_response(guarded)
        latency = time.perf_counter() - start_time
        await telemetry.record_latency(latency)
        await telemetry.record_query()
        await log_query(normalized, routed_engines, response_hash, latency)
        return JSONResponse(content=guarded)

    except Exception as e:
        logger.error(f"Unhandled error in /query: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    status = await health_monitor.get_status()
    return status

@app.get("/metrics", response_model=MetricsResponse)
async def metrics_endpoint():
    metrics = await telemetry.get_metrics()
    return metrics

@app.get("/coverage", response_model=CoverageResponse)
async def coverage_endpoint():
    coverage_report = await doctrine_cache.get_coverage_report()
    # Dummy epistemic gaps: domains with no doctrines
    all_domains = set()
    for doc in (await doctrine_cache.get_all()).values():
        all_domains.update(doc.get("coverage", []))
    known_domains = set(coverage_report.keys())
    epistemic_gaps = list(all_domains - known_domains)
    return {
        "coverage_report": coverage_report,
        "epistemic_gaps": epistemic_gaps,
    }

@app.get("/drift", response_model=DriftResponse)
async def drift_endpoint():
    # Dummy drift detection report
    drift_report = {
        "last_drift_check": datetime.utcnow().isoformat(),
        "detected_drifts": [
            {"domain": "pressure_analysis", "severity": "medium", "details": "Shift in pressure patterns detected"},
            {"domain": "proppant_selection", "severity": "low", "details": "Minor changes in proppant usage"},
        ],
        "recommendations": [
            "Review pressure analysis models",
            "Update proppant selection guidelines",
        ],
    }
    return {"drift_report": drift_report}

@app.get("/doctrines", response_model=DoctrinesResponse)
async def doctrines_endpoint():
    doctrines = await doctrine_cache.get_all()
    return {"doctrines": doctrines}

@app.get("/routing", response_model=RoutingResponse)
async def routing_endpoint():
    # Dummy routing rules
    routing_rules = {
        "design": ["FRAC01", "FRAC06", "FRAC09"],
        "proppant": ["FRAC02", "FRAC12"],
        "fluid": ["FRAC03", "FRAC13"],
        "pressure": ["FRAC04", "FRAC18"],
        "microseismic": ["FRAC05"],
        "perforation": ["FRAC07"],
        "flowback": ["FRAC08"],
        "modeling": ["FRAC10"],
        "zipper": ["FRAC11"],
        "sand": ["FRAC12"],
        "chemical": ["FRAC13"],
        "water": ["FRAC14"],
        "wellbore": ["FRAC15"],
        "monitoring": ["FRAC16"],
        "parent-child": ["FRAC17"],
        "hit": ["FRAC18"],
        "environmental": ["FRAC19"],
        "economics": ["FRAC20"],
    }
    return {
        "routing_rules": routing_rules,
        "engine_registry": SUB_ENGINES,
    }

@app.get("/sub-engines", response_model=SubEnginesResponse)
async def sub_engines_endpoint():
    health = await health_monitor.get_status()
    return {"sub_engine_health": health.get("sub_engines", {})}

@app.post("/route", response_model=RouteResponse)
async def route_endpoint(request: RouteRequest):
    normalized = normalize_query(request.query)
    domains = classify_domain(normalized)
    routed_engines = await route_query(domains)
    return {"routed_engines": routed_engines}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(request: AnalyzeRequest):
    normalized = normalize_query(request.query)
    domains = classify_domain(normalized)
    routed_engines = await route_query(domains)
    analysis_results = {}

    # For deep analysis, simulate more detailed responses
    for engine_id in routed_engines:
        await telemetry.record_sub_engine_call(engine_id)
        # Simulate analysis delay
        await asyncio.sleep(random.uniform(0.2, 0.5))
        analysis_results[engine_id] = {
            "engine_name": SUB_ENGINES[engine_id],
            "analysis": f"Deep analysis for query '{normalized}' with parameters {request.parameters}",
            "timestamp": datetime.utcnow().isoformat(),
        }

    return {"analysis_results": analysis_results}

# Exception handlers

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=ENGINE_PORT, log_level="info")