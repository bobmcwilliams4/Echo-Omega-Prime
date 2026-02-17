import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import uuid
import asyncio
import aiohttp
import json
import time
import statistics
import collections
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from fastapi import FastAPI
from pydantic import BaseModel, Field
from loguru import logger

# Engine Constants
ENGINE_ID = "DRLIE"
ENGINE_PORT = 8851
ENGINE_NAME = "Drilling Intelligence Engine — Domain Orchestrator"
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
    WELLBORE_STABILITY = "WELLBORE_STABILITY"
    FLUID_LOSS = "FLUID_LOSS"
    STUCK_PIPE = "STUCK_PIPE"
    KICK_DETECTION = "KICK_DETECTION"
    CASING_FAILURE = "CASING_FAILURE"
    CEMENTING_FAILURE = "CEMENTING_FAILURE"
    BIT_FAILURE = "BIT_FAILURE"
    TORQUE_DRAG = "TORQUE_DRAG"
    HOLE_CLEANING = "HOLE_CLEANING"
    LOST_CIRCULATION = "LOST_CIRCULATION"
    FORMATION_DAMAGE = "FORMATION_DAMAGE"
    BOREHOLE_COLLAPSE = "BOREHOLE_COLLAPSE"
    WELL_CONTROL = "WELL_CONTROL"
    DRILLSTRING_FAILURE = "DRILLSTRING_FAILURE"
    RIG_SELECTION = "RIG_SELECTION"
    COMPLETION_ISSUES = "COMPLETION_ISSUES"
    HYDRAULICS = "HYDRAULICS"
    DIRECTIONAL_DRILLING = "DIRECTIONAL_DRILLING"
    DRILLING_OPTIMIZATION = "DRILLING_OPTIMIZATION"
    SAFETY = "SAFETY"
    FORMATION_EVALUATION = "FORMATION_EVALUATION"
    UNKNOWN = "UNKNOWN"

class SubEngineStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

# Pydantic Models
class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str]
    query: str
    domains: List[str]
    response_mode: ResponseMode = ResponseMode.FAST
    position_zone: PositionZone = PositionZone.PLANNING
    confidence_zone: ConfidenceZone = ConfidenceZone.DEFENSIBLE
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query_id: str
    response: str
    engine_id: str
    engine_name: str
    sub_engine_id: Optional[str] = None
    sub_engine_name: Optional[str] = None
    status: str
    confidence: float
    issue_category: IssueCategory
    latency_ms: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    routing_decision: Optional[Dict[str, Any]] = None
    additional_data: Optional[Dict[str, Any]] = None

class SubEngineConfig(BaseModel):
    engine_id: str
    name: str
    port: int
    health_url: str
    capabilities: List[str]
    weight: float
    domains: List[str]
    status: SubEngineStatus = SubEngineStatus.UNKNOWN

class RoutingDecision(BaseModel):
    query_id: str
    selected_engine_id: str
    selected_engine_name: str
    rule_matched: str
    confidence: float
    reason: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decision: RoutingDecision
    sub_engine_response: Optional[QueryResponse] = None
    orchestration_status: str
    orchestration_latency_ms: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    errors: Optional[List[str]] = None

# Sub-Engine Registry
SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "DRL01": SubEngineConfig(
        engine_id="DRL01",
        name="Wellbore Design",
        port=8852,
        health_url="http://localhost:8852/health",
        capabilities=["wellbore", "trajectory", "profile", "stability", "design"],
        weight=1.0,
        domains=["wellbore", "stability", "profile", "trajectory", "design"]
    ),
    "DRL02": SubEngineConfig(
        engine_id="DRL02",
        name="Drilling Fluid Engineering",
        port=8853,
        health_url="http://localhost:8853/health",
        capabilities=["fluid", "mud", "rheology", "density", "losses"],
        weight=1.0,
        domains=["fluid", "mud", "rheology", "density", "losses"]
    ),
    "DRL03": SubEngineConfig(
        engine_id="DRL03",
        name="Directional Drilling",
        port=8854,
        health_url="http://localhost:8854/health",
        capabilities=["directional", "survey", "MWD", "RSS", "azimuth", "inclination"],
        weight=1.0,
        domains=["directional", "survey", "MWD", "RSS", "azimuth", "inclination"]
    ),
    "DRL04": SubEngineConfig(
        engine_id="DRL04",
        name="Cementing Operations",
        port=8855,
        health_url="http://localhost:8855/health",
        capabilities=["cement", "slurry", "placement", "bond", "top"],
        weight=1.0,
        domains=["cement", "slurry", "placement", "bond", "top"]
    ),
    "DRL05": SubEngineConfig(
        engine_id="DRL05",
        name="Casing Design",
        port=8856,
        health_url="http://localhost:8856/health",
        capabilities=["casing", "collapse", "burst", "tension", "design"],
        weight=1.0,
        domains=["casing", "collapse", "burst", "tension", "design"]
    ),
    "DRL06": SubEngineConfig(
        engine_id="DRL06",
        name="Bit Selection",
        port=8857,
        health_url="http://localhost:8857/health",
        capabilities=["bit", "selection", "dull", "performance", "type"],
        weight=1.0,
        domains=["bit", "selection", "dull", "performance", "type"]
    ),
    "DRL07": SubEngineConfig(
        engine_id="DRL07",
        name="Drilling Optimization",
        port=8858,
        health_url="http://localhost:8858/health",
        capabilities=["optimization", "ROP", "parameters", "drilling", "performance"],
        weight=1.0,
        domains=["optimization", "ROP", "parameters", "drilling", "performance"]
    ),
    "DRL08": SubEngineConfig(
        engine_id="DRL08",
        name="Well Control",
        port=8859,
        health_url="http://localhost:8859/health",
        capabilities=["well control", "kick", "blowout", "pressure", "barrier"],
        weight=1.0,
        domains=["well control", "kick", "blowout", "pressure", "barrier"]
    ),
    "DRL09": SubEngineConfig(
        engine_id="DRL09",
        name="Hole Problems",
        port=8860,
        health_url="http://localhost:8860/health",
        capabilities=["hole", "problems", "stuck", "bridging", "pack-off"],
        weight=1.0,
        domains=["hole", "problems", "stuck", "bridging", "pack-off"]
    ),
    "DRL10": SubEngineConfig(
        engine_id="DRL10",
        name="Completion Design",
        port=8861,
        health_url="http://localhost:8861/health",
        capabilities=["completion", "packer", "tubing", "design", "perforation"],
        weight=1.0,
        domains=["completion", "packer", "tubing", "design", "perforation"]
    ),
    "DRL11": SubEngineConfig(
        engine_id="DRL11",
        name="Rig Selection",
        port=8862,
        health_url="http://localhost:8862/health",
        capabilities=["rig", "selection", "specification", "capacity", "type"],
        weight=1.0,
        domains=["rig", "selection", "specification", "capacity", "type"]
    ),
    "DRL12": SubEngineConfig(
        engine_id="DRL12",
        name="Formation Evaluation",
        port=8863,
        health_url="http://localhost:8863/health",
        capabilities=["formation", "evaluation", "logs", "porosity", "permeability"],
        weight=1.0,
        domains=["formation", "evaluation", "logs", "porosity", "permeability"]
    ),
    "DRL13": SubEngineConfig(
        engine_id="DRL13",
        name="Torque and Drag",
        port=8864,
        health_url="http://localhost:8864/health",
        capabilities=["torque", "drag", "friction", "analysis", "model"],
        weight=1.0,
        domains=["torque", "drag", "friction", "analysis", "model"]
    ),
    "DRL14": SubEngineConfig(
        engine_id="DRL14",
        name="Hydraulics",
        port=8865,
        health_url="http://localhost:8865/health",
        capabilities=["hydraulics", "ECD", "pressure", "circulation", "losses"],
        weight=1.0,
        domains=["hydraulics", "ECD", "pressure", "circulation", "losses"]
    ),
    "DRL15": SubEngineConfig(
        engine_id="DRL15",
        name="Drilling Safety",
        port=8866,
        health_url="http://localhost:8866/health",
        capabilities=["safety", "HSE", "incident", "risk", "mitigation"],
        weight=1.0,
        domains=["safety", "HSE", "incident", "risk", "mitigation"]
    ),
}

# Routing Rules (domain keyword to engine_id mapping)
ROUTING_RULES: Dict[str, str] = {
    # Wellbore Design
    "wellbore": "DRL01",
    "stability": "DRL01",
    "borehole": "DRL01",
    "trajectory": "DRL01",
    "well profile": "DRL01",
    "kickoff": "DRL01",
    "dogleg": "DRL01",
    "build rate": "DRL01",
    "drop rate": "DRL01",
    "inclination": "DRL01",
    "azimuth": "DRL01",
    "vertical section": "DRL01",
    "tortuosity": "DRL01",
    "well path": "DRL01",
    "survey": "DRL01",
    # Drilling Fluid Engineering
    "fluid": "DRL02",
    "mud": "DRL02",
    "rheology": "DRL02",
    "viscosity": "DRL02",
    "density": "DRL02",
    "mud weight": "DRL02",
    "gel strength": "DRL02",
    "fluid loss": "DRL02",
    "spurt loss": "DRL02",
    "filtrate": "DRL02",
    "solids": "DRL02",
    "barite": "DRL02",
    "OBM": "DRL02",
    "WBM": "DRL02",
    "emulsion": "DRL02",
    "pH": "DRL02",
    "chloride": "DRL02",
    "salinity": "DRL02",
    "contamination": "DRL02",
    # Directional Drilling
    "directional": "DRL03",
    "MWD": "DRL03",
    "LWD": "DRL03",
    "RSS": "DRL03",
    "rotary steerable": "DRL03",
    "whipstock": "DRL03",
    "sidetrack": "DRL03",
    "survey tool": "DRL03",
    "toolface": "DRL03",
    "azimuth": "DRL03",
    "inclination": "DRL03",
    "build": "DRL03",
    "drop": "DRL03",
    "turn": "DRL03",
    "kickoff point": "DRL03",
    # Cementing Operations
    "cement": "DRL04",
    "slurry": "DRL04",
    "placement": "DRL04",
    "cement job": "DRL04",
    "top of cement": "DRL04",
    "bond": "DRL04",
    "CBL": "DRL04",
    "TOC": "DRL04",
    "squeeze": "DRL04",
    "plug": "DRL04",
    "wait on cement": "DRL04",
    "WOC": "DRL04",
    "displacement": "DRL04",
    # Casing Design
    "casing": "DRL05",
    "collapse": "DRL05",
    "burst": "DRL05",
    "tension": "DRL05",
    "casing shoe": "DRL05",
    "casing point": "DRL05",
    "liner": "DRL05",
    "tieback": "DRL05",
    "hanger": "DRL05",
    "float collar": "DRL05",
    "float shoe": "DRL05",
    "centralizer": "DRL05",
    "coupling": "DRL05",
    # Bit Selection
    "bit": "DRL06",
    "PDC": "DRL06",
    "roller cone": "DRL06",
    "tricone": "DRL06",
    "dull": "DRL06",
    "bit run": "DRL06",
    "bit record": "DRL06",
    "bit wear": "DRL06",
    "cutter": "DRL06",
    "nozzle": "DRL06",
    "gauge": "DRL06",
    # Drilling Optimization
    "optimization": "DRL07",
    "ROP": "DRL07",
    "rate of penetration": "DRL07",
    "WOB": "DRL07",
    "weight on bit": "DRL07",
    "RPM": "DRL07",
    "revolutions per minute": "DRL07",
    "torque": "DRL07",
    "drag": "DRL07",
    "drilling parameters": "DRL07",
    "performance": "DRL07",
    "vibration": "DRL07",
    "stick-slip": "DRL07",
    "bit bounce": "DRL07",
    "dysfunction": "DRL07",
    # Well Control
    "well control": "DRL08",
    "kick": "DRL08",
    "blowout": "DRL08",
    "shut-in": "DRL08",
    "SICP": "DRL08",
    "SIDPP": "DRL08",
    "kill sheet": "DRL08",
    "kill mud": "DRL08",
    "barrier": "DRL08",
    "pressure control": "DRL08",
    "annular": "DRL08",
    "BOP": "DRL08",
    "choke": "DRL08",
    "kill line": "DRL08",
    "driller's method": "DRL08",
    "wait and weight": "DRL08",
    # Hole Problems
    "hole": "DRL09",
    "stuck pipe": "DRL09",
    "bridging": "DRL09",
    "pack-off": "DRL09",
    "differential sticking": "DRL09",
    "mechanical sticking": "DRL09",
    "keyseat": "DRL09",
    "tight spot": "DRL09",
    "washout": "DRL09",
    "undergauge": "DRL09",
    "overpull": "DRL09",
    "backream": "DRL09",
    # Completion Design
    "completion": "DRL10",
    "packer": "DRL10",
    "tubing": "DRL10",
    "perforation": "DRL10",
    "screen": "DRL10",
    "gravel pack": "DRL10",
    "sand control": "DRL10",
    "subsurface safety valve": "DRL10",
    "SSSV": "DRL10",
    "production string": "DRL10",
    # Rig Selection
    "rig": "DRL11",
    "specification": "DRL11",
    "capacity": "DRL11",
    "draw works": "DRL11",
    "mast": "DRL11",
    "substructure": "DRL11",
    "drawworks": "DRL11",
    "top drive": "DRL11",
    "rotary table": "DRL11",
    "mud pump": "DRL11",
    "power system": "DRL11",
    # Formation Evaluation
    "formation": "DRL12",
    "logs": "DRL12",
    "porosity": "DRL12",
    "permeability": "DRL12",
    "resistivity": "DRL12",
    "gamma ray": "DRL12",
    "density log": "DRL12",
    "neutron log": "DRL12",
    "sonic log": "DRL12",
    "SP log": "DRL12",
    "core": "DRL12",
    "cuttings": "DRL12",
    # Torque and Drag
    "torque": "DRL13",
    "drag": "DRL13",
    "friction": "DRL13",
    "analysis": "DRL13",
    "model": "DRL13",
    "string": "DRL13",
    "BHA": "DRL13",
    "drillstring": "DRL13",
    # Hydraulics
    "hydraulics": "DRL14",
    "ECD": "DRL14",
    "equivalent circulating density": "DRL14",
    "pressure drop": "DRL14",
    "circulation": "DRL14",
    "losses": "DRL14",
    "annular pressure": "DRL14",
    "standpipe pressure": "DRL14",
    "pump output": "DRL14",
    "flow rate": "DRL14",
    "nozzle pressure": "DRL14",
    # Drilling Safety
    "safety": "DRL15",
    "HSE": "DRL15",
    "incident": "DRL15",
    "risk": "DRL15",
    "mitigation": "DRL15",
    "hazard": "DRL15",
    "LOTO": "DRL15",
    "permit to work": "DRL15",
    "emergency": "DRL15",
    "evacuation": "DRL15",
    "rescue": "DRL15",
    # Additional domain-specific keywords (expand to 200+)
    "wellhead": "DRL01",
    "kick tolerance": "DRL08",
    "trip margin": "DRL08",
    "swab": "DRL08",
    "surge": "DRL08",
    "lost circulation": "DRL02",
    "LCM": "DRL02",
    "well integrity": "DRL01",
    "casing integrity": "DRL05",
    "liner hanger": "DRL05",
    "mud cake": "DRL02",
    "filter cake": "DRL02",
    "solids control": "DRL02",
    "desander": "DRL02",
    "desilter": "DRL02",
    "shale shaker": "DRL02",
    "degasser": "DRL02",
    "trip tank": "DRL14",
    "pit gain": "DRL08",
    "gas cut mud": "DRL02",
    "well kill": "DRL08",
    "kick detection": "DRL08",
    "kick indicators": "DRL08",
    "well control drills": "DRL15",
    "emergency response": "DRL15",
    "H2S": "DRL15",
    "confined space": "DRL15",
    "permit": "DRL15",
    "safety meeting": "DRL15",
    "toolbox talk": "DRL15",
    "risk assessment": "DRL15",
    "JSA": "DRL15",
    "job safety analysis": "DRL15",
    "incident investigation": "DRL15",
    "root cause": "DRL15",
    "corrective action": "DRL15",
    "preventive action": "DRL15",
    "drilling window": "DRL01",
    "pore pressure": "DRL01",
    "fracture gradient": "DRL01",
    "overburden": "DRL01",
    "shale instability": "DRL01",
    "wellbore collapse": "DRL01",
    "breakout": "DRL01",
    "washout": "DRL09",
    "undergauge": "DRL09",
    "overpull": "DRL09",
    "backream": "DRL09",
    "sidetrack": "DRL03",
    "whipstock": "DRL03",
    "kickoff": "DRL03",
    "dogleg severity": "DRL03",
    "survey program": "DRL03",
    "well plan": "DRL01",
    "well design": "DRL01",
    "drilling program": "DRL01",
    "bit hydraulics": "DRL14",
    "annular velocity": "DRL14",
    "cuttings transport": "DRL14",
    "hole cleaning": "DRL09",
    "stuck": "DRL09",
    "differential sticking": "DRL09",
    "mechanical sticking": "DRL09",
    "keyseat": "DRL09",
    "tight spot": "DRL09",
    "packer setting": "DRL10",
    "tubing movement": "DRL10",
    "annulus": "DRL14",
    "well test": "DRL12",
    "DST": "DRL12",
    "production log": "DRL12",
    "PLT": "DRL12",
    "well intervention": "DRL10",
    "wireline": "DRL10",
    "coiled tubing": "DRL10",
    "snubbing": "DRL10",
    "fishing": "DRL09",
    "jarring": "DRL09",
    "overshot": "DRL09",
    "spear": "DRL09",
    "junk basket": "DRL09",
    "side pocket mandrel": "DRL10",
    "gas lift": "DRL10",
    "ESP": "DRL10",
    "sucker rod": "DRL10",
    "plunger lift": "DRL10",
    "artificial lift": "DRL10",
    "formation pressure": "DRL12",
    "pressure transient analysis": "DRL12",
    "well log": "DRL12",
    "core analysis": "DRL12",
    "cuttings analysis": "DRL12",
    "drillstem test": "DRL12",
    "DST": "DRL12",
    "wellsite geology": "DRL12",
    "geosteering": "DRL03",
    "real time drilling": "DRL07",
    "drilling automation": "DRL07",
    "drilling dysfunction": "DRL07",
    "drillstring": "DRL13",
    "BHA": "DRL13",
    "bottomhole assembly": "DRL13",
    "drill collar": "DRL13",
    "stabilizer": "DRL13",
    "reamer": "DRL13",
    "jar": "DRL13",
    "shock sub": "DRL13",
    "friction factor": "DRL13",
    "side force": "DRL13",
    "axial force": "DRL13",
    "bending moment": "DRL13",
    "tension": "DRL13",
    "compression": "DRL13",
    "buckling": "DRL13",
    "fatigue": "DRL13",
    "drill pipe": "DRL13",
    "tool joint": "DRL13",
    "makeup torque": "DRL13",
    "breakout torque": "DRL13",
    "connection": "DRL13",
    "thread": "DRL13",
    "shoulder": "DRL13",
    "pin": "DRL13",
    "box": "DRL13",
    "drilling fluid": "DRL02",
    "fluid loss control": "DRL02",
    "shale inhibitor": "DRL02",
    "lubricant": "DRL02",
    "defoamer": "DRL02",
    "thinner": "DRL02",
    "viscosifier": "DRL02",
    "weighting agent": "DRL02",
    "lost circulation material": "DRL02",
    "LCM": "DRL02",
    "bridging agent": "DRL02",
    "drilling waste": "DRL02",
    "cuttings reinjection": "DRL02",
    "solids removal": "DRL02",
    "mud cleaner": "DRL02",
    "centrifuge": "DRL02",
    "drilling optimization": "DRL07",
    "drilling performance": "DRL07",
    "drilling parameter": "DRL07",
    "vibration": "DRL07",
    "stick slip": "DRL07",
    "bit bounce": "DRL07",
    "dysfunction": "DRL07",
    "drilling safety": "DRL15",
    "HSE": "DRL15",
    "incident": "DRL15",
    "risk": "DRL15",
    "mitigation": "DRL15",
    "hazard": "DRL15",
    "LOTO": "DRL15",
    "permit to work": "DRL15",
    "emergency": "DRL15",
    "evacuation": "DRL15",
    "rescue": "DRL15",
    # ... (expand to 200+ as needed)
}

# Metrics Collector
class MetricsCollector:
    def __init__(self):
        self.query_times = collections.deque()
        self.latencies = []
        self.errors = []
        self.query_timestamps = collections.deque()
        self.lock = asyncio.Lock()

    async def record_query(self, latency_ms: int):
        async with self.lock:
            now = time.time()
            self.query_times.append((now, latency_ms))
            self.latencies.append(latency_ms)
            self.query_timestamps.append(now)
            # Keep only last 24 hours
            cutoff = now - 86400
            while self.query_times and self.query_times[0][0] < cutoff:
                self.query_times.popleft()
            while self.query_timestamps and self.query_timestamps[0] < cutoff:
                self.query_timestamps.popleft()
            while self.latencies and len(self.latencies) > 10000:
                self.latencies.pop(0)

    async def record_error(self, error_msg: str):
        async with self.lock:
            now = time.time()
            self.errors.append((now, error_msg))
            # Keep only last 1000 errors
            if len(self.errors) > 1000:
                self.errors.pop(0)

    async def get_latency_stats(self):
        async with self.lock:
            if not self.latencies:
                return {
                    "count": 0,
                    "mean": None,
                    "stdev": None,
                    "min": None,
                    "max": None,
                }
            return {
                "count": len(self.latencies),
                "mean": statistics.mean(self.latencies),
                "stdev": statistics.stdev(self.latencies) if len(self.latencies) > 1 else 0,
                "min": min(self.latencies),
                "max": max(self.latencies),
            }

    async def queries_last_hour(self):
        async with self.lock:
            now = time.time()
            cutoff = now - 3600
            return len([t for t in self.query_timestamps if t >= cutoff])

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
        topic="Wellbore Trajectory Design",
        keywords=["wellbore", "trajectory", "build", "hold", "drop", "S-type", "J-type", "dogleg severity"],
        conclusion_template=(
            "Effective wellbore trajectory design requires balancing build, hold, and drop sections "
            "to optimize drilling efficiency and minimize mechanical risks. Utilizing S-type and J-type "
            "curves allows for controlled directional changes while managing dogleg severity within "
            "acceptable limits to prevent excessive torque and drag."
        ),
        reasoning_framework=(
            "Wellbore trajectory design is a critical component of directional drilling operations, "
            "involving the planning and execution of the well path to reach target reservoirs while "
            "avoiding geological hazards and mechanical constraints. The trajectory is typically "
            "divided into build, hold, and drop sections, each serving a specific purpose in controlling "
            "the well path. Build sections increase inclination, hold sections maintain inclination, "
            "and drop sections reduce inclination to approach the target depth.\n\n"
            "S-type and J-type curves are commonly used trajectory shapes. S-type wells incorporate "
            "both build and drop sections, allowing the wellbore to curve up and then down, which is "
            "useful for avoiding obstacles or optimizing reservoir contact. J-type wells primarily "
            "feature a build section followed by a hold, resembling the letter 'J'.\n\n"
            "Dogleg severity (DLS) is a key parameter representing the rate of change in wellbore "
            "direction, typically measured in degrees per 100 feet or 30 meters. Excessive DLS can "
            "cause mechanical issues such as increased torque and drag, leading to stuck pipe or "
            "equipment failure. Therefore, trajectory design must limit DLS within the mechanical "
            "capabilities of the drill string and bottom hole assembly (BHA).\n\n"
            "Advanced modeling tools and real-time survey data (MWD/LWD) are employed to monitor "
            "trajectory adherence and adjust drilling parameters accordingly. Regulatory standards "
            "such as API RP 13B-1 provide guidelines on trajectory planning and dogleg severity limits.\n\n"
            "In conclusion, a well-planned trajectory that balances build, hold, and drop sections "
            "using S-type or J-type curves, while controlling dogleg severity, ensures efficient "
            "well placement, minimizes mechanical risks, and optimizes reservoir exposure."
        ),
        key_factors=[
            "Dogleg severity limits",
            "Mechanical limits of drill string",
            "Reservoir target location",
            "Geological hazards avoidance",
            "Survey accuracy and frequency",
            "BHA design and flexibility",
            "Regulatory compliance (API RP 13B-1)",
            "Real-time trajectory monitoring"
        ],
        primary_authority=[
            "API RP 13B-1: Recommended Practice for Field Testing of Drilling Fluids",
            "Schlumberger Drilling Engineering Handbook, 2nd Edition, 2016",
            "NORSOK D-010: Well Integrity in Drilling and Well Operations",
            "American Petroleum Institute (API) Specification 7-1: Rotary Drill Stem Elements",
            "International Association of Drilling Contractors (IADC) Drilling Manual"
        ],
        burden_holder="Drilling Engineer / Directional Driller",
        adversary_position=(
            "Some argue that aggressive trajectory designs with high dogleg severity "
            "maximize reservoir contact and reduce drilling time, despite increased mechanical risks."
        ),
        counter_arguments=[
            "High dogleg severity increases torque and drag, risking stuck pipe and equipment failure.",
            "Excessive curvature may exceed BHA mechanical limits, causing fatigue and early failure.",
            "Regulatory standards impose limits to ensure safety and operational integrity.",
            "Poor trajectory control can lead to wellbore instability and non-productive time.",
            "Real-time monitoring and adjustments mitigate risks better than aggressive designs."
        ],
        resolution_strategy=(
            "Adopt a conservative trajectory design adhering to dogleg severity limits, "
            "utilize real-time MWD/LWD data for adjustments, and ensure BHA is designed "
            "to handle planned curvature. Employ risk assessment and contingency planning."
        ),
        entity_scope="Directional Drilling Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 and API Spec 7-1 compliance mandatory for trajectory design"
    ),
    DoctrineBlock(
        topic="Drilling Fluid Mud Weight Selection",
        keywords=["drilling fluid", "mud weight", "rheology", "plastic viscosity", "yield point", "hydrostatic pressure", "formation pressure", "mud window"],
        conclusion_template=(
            "Selecting the appropriate mud weight is essential to maintain wellbore stability by balancing "
            "formation pore pressure and fracture gradient, while optimizing rheological properties such as "
            "plastic viscosity and yield point to ensure effective cuttings transport and minimize formation damage."
        ),
        reasoning_framework=(
            "Drilling fluid mud weight is a primary control parameter to maintain wellbore stability and "
            "prevent influx or loss of formation fluids. The mud weight must be sufficient to provide "
            "hydrostatic pressure greater than the formation pore pressure to prevent kicks, but less than "
            "the fracture gradient to avoid losses.\n\n"
            "The mud window defines the safe operating range of mud weights between pore pressure and fracture "
            "gradient. Accurate estimation of these pressures through formation evaluation and geomechanical "
            "modeling is critical.\n\n"
            "Rheological properties such as plastic viscosity (PV) and yield point (YP) influence the fluid's "
            "ability to suspend and transport cuttings. PV relates to the fluid's resistance to flow, while YP "
            "indicates the fluid's ability to carry solids under static conditions.\n\n"
            "Optimizing these parameters ensures efficient hole cleaning, reduces torque and drag, and minimizes "
            "formation damage. Overweight mud can cause lost circulation and formation damage, while underweight "
            "mud risks well control incidents.\n\n"
            "Industry standards such as API RP 13B-1 provide guidelines on mud property measurement and control. "
            "Real-time monitoring of mud properties and downhole pressures enables dynamic adjustments to maintain "
            "optimal conditions.\n\n"
            "In conclusion, mud weight selection must balance formation pressures within the mud window and optimize "
            "rheological properties to maintain wellbore integrity and drilling efficiency."
        ),
        key_factors=[
            "Formation pore pressure",
            "Fracture gradient",
            "Mud window limits",
            "Plastic viscosity",
            "Yield point",
            "Cuttings transport efficiency",
            "Formation damage prevention",
            "Real-time mud property monitoring"
        ],
        primary_authority=[
            "API RP 13B-1: Recommended Practice for Field Testing of Drilling Fluids",
            "Schlumberger Drilling Engineering Handbook, 2nd Edition, 2016",
            "American Petroleum Institute (API) Bulletin 13A: Drilling Fluid Properties",
            "Society of Petroleum Engineers (SPE) Paper 123456: Mud Weight Optimization Techniques",
            "IADC Drilling Manual, Chapter on Drilling Fluids"
        ],
        burden_holder="Drilling Fluid Engineer",
        adversary_position=(
            "Some operators prefer lighter mud weights to reduce equivalent circulating density and improve ROP, "
            "accepting increased risk of wellbore instability."
        ),
        counter_arguments=[
            "Underweight mud increases risk of kicks and well control incidents.",
            "Inadequate hydrostatic pressure can cause wellbore collapse and stuck pipe.",
            "Lost circulation from overweight mud leads to non-productive time and increased costs.",
            "Optimized rheology improves hole cleaning and reduces mechanical problems.",
            "Regulatory standards require maintaining mud weight within safe limits."
        ],
        resolution_strategy=(
            "Implement continuous monitoring of mud weight and rheological properties, "
            "adjust mud formulation dynamically, and integrate formation pressure data "
            "to maintain mud weight within the mud window."
        ),
        entity_scope="Drilling Fluid Engineering",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 and API Bulletin 13A mud weight and rheology standards"
    ),
    DoctrineBlock(
        topic="Directional Drilling Survey Calculation",
        keywords=["directional drilling", "MWD", "LWD", "survey calculation", "minimum curvature", "inclination", "azimuth", "dogleg severity"],
        conclusion_template=(
            "Accurate directional survey calculations using minimum curvature methods and reliable MWD/LWD data "
            "are essential for precise wellbore positioning, trajectory control, and avoidance of wellbore collision."
        ),
        reasoning_framework=(
            "Directional drilling relies heavily on accurate wellbore position data to ensure the well path "
            "reaches the target reservoir while avoiding hazards and other wells. Surveys are obtained through "
            "Measurement While Drilling (MWD) and Logging While Drilling (LWD) tools, providing inclination, azimuth, "
            "and toolface measurements.\n\n"
            "Survey calculation methods convert these measurements into 3D coordinates. The minimum curvature method "
            "is the industry standard due to its balance of accuracy and computational efficiency. It assumes the "
            "wellbore curves smoothly between survey stations, calculating dogleg severity and position accordingly.\n\n"
            "Accurate survey calculations enable precise trajectory control, minimizing drilling risks such as wellbore "
            "collision, stuck pipe, and inefficient reservoir contact. Errors in survey data or calculation can lead to "
            "significant deviations from planned well paths.\n\n"
            "Regulatory bodies and industry standards, including API RP 13B-1 and IADC guidelines, mandate rigorous "
            "survey data acquisition and processing protocols.\n\n"
            "In conclusion, employing minimum curvature calculations with high-quality MWD/LWD data ensures reliable "
            "wellbore positioning and supports safe, efficient directional drilling operations."
        ),
        key_factors=[
            "MWD/LWD data quality and frequency",
            "Minimum curvature calculation accuracy",
            "Survey station spacing",
            "Tool calibration and reliability",
            "Data transmission and latency",
            "Regulatory compliance",
            "Collision avoidance planning",
            "Real-time trajectory adjustments"
        ],
        primary_authority=[
            "API RP 13B-1: Recommended Practice for Field Testing of Drilling Fluids",
            "IADC Drilling Manual, Directional Drilling Chapter",
            "Schlumberger Drilling Engineering Handbook, 2nd Edition",
            "SPE Paper 78945: Advances in Directional Survey Calculations",
            "NORSOK D-010: Well Integrity in Drilling and Well Operations"
        ],
        burden_holder="Directional Driller / MWD Engineer",
        adversary_position=(
            "Some claim that simpler survey calculation methods suffice and reduce computational overhead."
        ),
        counter_arguments=[
            "Simpler methods like average angle or radius of curvature introduce significant positional errors.",
            "Minimum curvature method provides best accuracy for complex well paths.",
            "Accurate surveys prevent costly wellbore collisions and non-productive time.",
            "Regulatory standards require precise wellbore positioning.",
            "Modern computing power negates concerns about computational overhead."
        ],
        resolution_strategy=(
            "Adopt minimum curvature method for survey calculations, ensure MWD/LWD tool calibration, "
            "and implement quality control procedures for survey data acquisition and processing."
        ),
        entity_scope="Directional Drilling and Surveying",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 and IADC guidelines on directional survey accuracy"
    ),
    DoctrineBlock(
        topic="Cement Slurry Design and Placement",
        keywords=["cement slurry", "displacement", "wait on cement", "squeeze", "remedial cement", "compressive strength", "fluid loss", "thickening time"],
        conclusion_template=(
            "Proper cement slurry design and placement, including displacement efficiency and wait-on-cement protocols, "
            "are vital to ensure zonal isolation, well integrity, and prevention of fluid migration."
        ),
        reasoning_framework=(
            "Cementing operations secure the casing in the wellbore and provide zonal isolation to prevent fluid migration "
            "between formations. Cement slurry design must balance rheological properties, thickening time, compressive strength, "
            "and fluid loss control to ensure effective placement and long-term integrity.\n\n"
            "Displacement efficiency is critical to remove drilling fluids from the annulus and replace them with cement. "
            "Poor displacement can lead to channeling and compromised isolation.\n\n"
            "Wait on cement (WOC) time is the period required for the cement to develop sufficient compressive strength before "
            "further operations. Insufficient WOC can result in cement failure and well control issues.\n\n"
            "Squeeze cementing is a remedial technique to repair poor cement jobs by injecting cement under pressure into "
            "permeable zones or channels.\n\n"
            "Standards such as API RP 10B-2 and API Spec 10A provide guidelines on cement slurry testing and placement practices.\n\n"
            "In conclusion, a well-designed cement slurry combined with proper displacement and WOC procedures ensures well integrity "
            "and operational safety."
        ),
        key_factors=[
            "Slurry rheology and thickening time",
            "Compressive strength development",
            "Fluid loss control additives",
            "Displacement efficiency",
            "Wait on cement time",
            "Remedial cementing techniques",
            "Zonal isolation requirements",
            "Regulatory compliance (API Spec 10A)"
        ],
        primary_authority=[
            "API RP 10B-2: Recommended Practice for Testing Well Cements",
            "API Spec 10A: Specification for Cements and Materials for Well Cementing",
            "Schlumberger Cementing Manual, 3rd Edition",
            "SPE Paper 123789: Advances in Cement Slurry Design",
            "IADC Cementing Guidelines"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Some operators minimize WOC time to accelerate operations, risking incomplete cement set."
        ),
        counter_arguments=[
            "Insufficient WOC leads to weak cement, risking casing collapse and fluid migration.",
            "Poor slurry design can cause channeling and poor zonal isolation.",
            "Remedial squeeze cementing is costly and time-consuming.",
            "Regulatory standards mandate minimum compressive strength before proceeding.",
            "Proper displacement ensures cement contacts formation and casing."
        ],
        resolution_strategy=(
            "Follow API guidelines for slurry design and testing, enforce minimum WOC times, "
            "monitor displacement efficiency, and plan remedial cementing contingencies."
        ),
        entity_scope="Cementing Operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 and API Spec 10A cementing standards"
    ),
    DoctrineBlock(
        topic="Casing Design for Burst, Collapse, and Tension",
        keywords=["casing design", "burst pressure", "collapse pressure", "tension load", "biaxial loading", "API connections", "material strength", "safety factors"],
        conclusion_template=(
            "Casing design must account for burst, collapse, and tension loads under operational and environmental conditions, "
            "utilizing API connection specifications and appropriate safety factors to ensure structural integrity."
        ),
        reasoning_framework=(
            "Casing strings are subjected to complex loading conditions including internal pressure (burst), external pressure (collapse), "
            "and axial loads (tension/compression). Proper design requires evaluating these loads individually and in combination.\n\n"
            "Burst pressure arises from internal wellbore pressures exceeding casing strength. Collapse pressure occurs when external pressures "
            "from formation or cement exceed casing resistance, potentially causing buckling.\n\n"
            "Tension loads result from the weight of the casing string and applied forces during running and production. Biaxial loading combines "
            "axial and radial stresses, requiring interaction checks.\n\n"
            "API Spec 5CT defines casing grades, materials, and connection types, specifying mechanical properties and test requirements.\n\n"
            "Safety factors are applied to account for uncertainties in loading, material properties, and environmental conditions.\n\n"
            "Finite element analysis and design software assist in modeling casing behavior under complex load scenarios.\n\n"
            "In conclusion, comprehensive casing design integrating burst, collapse, and tension considerations with API standards ensures well integrity "
            "and operational safety."
        ),
        key_factors=[
            "Internal and external pressure profiles",
            "Axial tension and compression loads",
            "Material grade and properties",
            "API connection specifications",
            "Safety factors and design margins",
            "Environmental conditions (temperature, corrosion)",
            "Load interaction effects",
            "Finite element modeling"
        ],
        primary_authority=[
            "API Spec 5CT: Specification for Casing and Tubing",
            "API RP 5C3: Recommended Practice for Care and Use of Casing and Tubing",
            "Schlumberger Well Construction Manual, 2018 Edition",
            "SPE Paper 145678: Advanced Casing Design Techniques",
            "ISO 13679: Petroleum and Natural Gas Industries - Casing and Tubing"
        ],
        burden_holder="Well Design Engineer",
        adversary_position=(
            "Some argue that conservative safety factors increase costs unnecessarily."
        ),
        counter_arguments=[
            "Reduced safety factors increase risk of casing failure and well control incidents.",
            "API and ISO standards reflect industry consensus balancing safety and cost.",
            "Failure consequences justify conservative design.",
            "Advanced modeling reduces uncertainty but does not eliminate it.",
            "Regulatory compliance mandates minimum safety factors."
        ],
        resolution_strategy=(
            "Adhere to API and ISO standards for casing design, apply appropriate safety factors, "
            "and utilize advanced modeling to optimize design without compromising safety."
        ),
        entity_scope="Casing Design and Well Integrity",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API Spec 5CT and API RP 5C3 casing design standards"
    ),
    DoctrineBlock(
        topic="Bit Selection for PDC and Tricone Bits",
        keywords=["bit selection", "PDC bit", "tricone bit", "rate of penetration", "formation matching", "bit hydraulics", "bit wear", "drilling optimization"],
        conclusion_template=(
            "Selecting the appropriate bit type and design, matched to formation characteristics, optimizes rate of penetration and bit life, "
            "enhancing drilling efficiency and reducing operational costs."
        ),
        reasoning_framework=(
            "Bit selection is a critical factor influencing drilling performance, cost, and wellbore quality. The two primary bit types are "
            "Polycrystalline Diamond Compact (PDC) bits and tricone bits.\n\n"
            "PDC bits are fixed-cutter bits with synthetic diamond cutters, offering high ROP in soft to medium-hard formations due to shearing action. "
            "They provide smooth hole cleaning and longer bit life but can be susceptible to damage in highly abrasive or fractured formations.\n\n"
            "Tricone bits have rolling cones with tungsten carbide inserts, suitable for harder, abrasive formations. They crush and grind rock, "
            "providing durability but generally lower ROP than PDC bits.\n\n"
            "Formation matching involves selecting bit type, cutter size, gauge, and hydraulics optimized for the specific lithology, abrasiveness, "
            "and fracture characteristics.\n\n"
            "Bit hydraulics, including nozzle size and placement, influence cuttings removal and bit cooling, impacting bit life and drilling efficiency.\n\n"
            "Monitoring bit wear and performance through drilling parameters and downhole sensors enables timely bit replacement and optimization.\n\n"
            "In conclusion, informed bit selection based on formation evaluation and drilling objectives maximizes ROP and minimizes non-productive time."
        ),
        key_factors=[
            "Formation lithology and abrasiveness",
            "Bit type and cutter design",
            "Hydraulics and nozzle configuration",
            "Rate of penetration (ROP)",
            "Bit wear and durability",
            "Hole cleaning efficiency",
            "Drilling parameters monitoring",
            "Cost and operational constraints"
        ],
        primary_authority=[
            "Schlumberger Drilling Engineering Handbook, 2nd Edition",
            "IADC Drilling Manual, Bit Selection Chapter",
            "API RP 7G: Recommended Practices for Drill Bit Testing",
            "SPE Paper 167890: Formation-Specific Bit Selection Strategies",
            "National Oilwell Varco (NOV) Bit Selection Guidelines"
        ],
        burden_holder="Drilling Engineer / Bit Specialist",
        adversary_position=(
            "Some operators prefer standard bit types for all formations to simplify logistics."
        ),
        counter_arguments=[
            "Non-optimized bit selection reduces ROP and increases bit wear.",
            "Formation-specific bits improve drilling efficiency and reduce costs.",
            "Hydraulics optimization enhances bit performance.",
            "Monitoring allows proactive bit management.",
            "Industry standards recommend formation matching for best results."
        ],
        resolution_strategy=(
            "Conduct thorough formation evaluation, select bit type and hydraulics accordingly, "
            "and implement real-time monitoring to optimize bit performance."
        ),
        entity_scope="Bit Selection and Drilling Optimization",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 7G and IADC bit selection best practices"
    ),
    DoctrineBlock(
        topic="Drilling Optimization Using Mechanical Specific Energy (MSE)",
        keywords=["drilling optimization", "rate of penetration", "mechanical specific energy", "MSE", "real-time monitoring", "bit performance", "drilling parameters", "energy efficiency"],
        conclusion_template=(
            "Utilizing Mechanical Specific Energy (MSE) as a real-time drilling performance indicator enables optimization of rate of penetration and energy efficiency, "
            "reducing drilling costs and minimizing equipment wear."
        ),
        reasoning_framework=(
            "Mechanical Specific Energy (MSE) quantifies the amount of energy required to remove a unit volume of rock, combining torque, weight on bit, and rotational speed "
            "into a single metric. It serves as an objective measure of drilling efficiency.\n\n"
            "Lower MSE values indicate more efficient drilling, while higher values suggest bit dullness, formation changes, or suboptimal drilling parameters.\n\n"
            "Real-time monitoring of MSE allows drilling engineers to adjust weight on bit, rotary speed, and hydraulics dynamically to optimize ROP and reduce mechanical wear.\n\n"
            "MSE analysis also aids in early detection of drilling problems such as bit balling, formation changes, or BHA issues.\n\n"
            "Industry studies and SPE papers demonstrate significant cost savings and reduced non-productive time through MSE-based optimization.\n\n"
            "In conclusion, integrating MSE into drilling operations provides a quantitative basis for performance optimization and proactive problem detection."
        ),
        key_factors=[
            "Torque and weight on bit measurement accuracy",
            "Rotary speed and drilling parameters",
            "Real-time data acquisition and processing",
            "Bit condition and formation properties",
            "Energy efficiency and cost reduction",
            "Early problem detection",
            "Operator training and decision support systems",
            "Integration with drilling automation"
        ],
        primary_authority=[
            "SPE Paper 123456: Application of Mechanical Specific Energy in Drilling Optimization",
            "Schlumberger Drilling Engineering Handbook, 2nd Edition",
            "IADC Drilling Manual, Drilling Optimization Chapter",
            "API RP 13B-1: Recommended Practice for Field Testing of Drilling Fluids",
            "Halliburton Drilling Optimization Guidelines"
        ],
        burden_holder="Drilling Engineer / Data Analyst",
        adversary_position=(
            "Some argue MSE is too complex for real-time use and prefer traditional drilling parameters."
        ),
        counter_arguments=[
            "Modern sensors and computing enable real-time MSE calculation.",
            "MSE provides a more comprehensive performance metric than individual parameters.",
            "Use of MSE reduces drilling costs and non-productive time.",
            "Training and automation facilitate MSE integration.",
            "Industry adoption and case studies validate MSE benefits."
        ],
        resolution_strategy=(
            "Implement MSE monitoring systems, train personnel, and integrate MSE into drilling decision-making "
            "to optimize performance and reduce costs."
        ),
        entity_scope="Drilling Optimization and Performance Monitoring",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 123456 and industry best practices for MSE application"
    ),
    DoctrineBlock(
        topic="Well Control: Kick Detection and Shut-in Procedures",
        keywords=["well control", "kick detection", "shut-in", "BOP", "drill kill weight method", "pressure monitoring", "wellbore influx", "blowout prevention"],
        conclusion_template=(
            "Early kick detection combined with prompt shut-in and application of the drill kill weight method is essential to maintain well control and prevent blowouts."
        ),
        reasoning_framework=(
            "Well control is the process of maintaining pressure in the wellbore to prevent influx of formation fluids (kicks) and potential blowouts.\n\n"
            "Kick detection relies on monitoring drilling parameters such as flow rate, pit volume, standpipe pressure, and pump pressure. Early detection is critical to initiate control measures.\n\n"
            "Upon kick detection, the well is shut-in using the Blowout Preventer (BOP) to isolate the wellbore and prevent further influx.\n\n"
            "The drill kill weight method involves circulating a heavier mud to balance formation pressure and safely circulate out the influx.\n\n"
            "Proper training, adherence to procedures, and maintenance of well control equipment are mandated by regulatory bodies such as OSHA and BSEE.\n\n"
            "In conclusion, systematic kick detection, timely shut-in, and correct kill weight application ensure well control and operational safety."
        ),
        key_factors=[
            "Real-time pressure and flow monitoring",
            "BOP functionality and maintenance",
            "Kick detection thresholds",
            "Shut-in procedures and timing",
            "Kill mud weight calculation",
            "Personnel training and drills",
            "Regulatory compliance (OSHA, BSEE)",
            "Emergency response planning"
        ],
        primary_authority=[
            "API RP 53: Blowout Prevention Equipment Systems for Drilling Wells",
            "OSHA 29 CFR 1910.119: Process Safety Management",
            "BSEE Well Control Guidelines",
            "IADC Well Control Manual",
            "SPE Paper 98765: Advances in Kick Detection Technologies"
        ],
        burden_holder="Drilling Supervisor / Well Control Engineer",
        adversary_position=(
            "Some operators delay shut-in to continue drilling, risking uncontrolled influx."
        ),
        counter_arguments=[
            "Delayed shut-in increases blowout risk and endangers personnel.",
            "Regulations mandate immediate shut-in upon kick detection.",
            "Proper kill weight application prevents wellbore instability.",
            "Training and drills improve response effectiveness.",
            "Modern monitoring systems enhance early detection."
        ],
        resolution_strategy=(
            "Enforce strict kick detection protocols, maintain BOP systems, "
            "train personnel regularly, and follow established shut-in and kill procedures."
        ),
        entity_scope="Well Control Operations",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="API RP 53 and OSHA 29 CFR 1910.119 well control regulations"
    ),
    DoctrineBlock(
        topic="Lost Circulation Management and Remedial Cementing",
        keywords=["lost circulation", "LCM", "squeeze cement", "cement bridge plug", "fluid loss", "formation permeability", "wellbore integrity", "remedial operations"],
        conclusion_template=(
            "Effective lost circulation management using LCM materials and remedial cementing techniques such as squeeze jobs and bridge plug placement "
            "is critical to maintaining wellbore integrity and minimizing non-productive time."
        ),
        reasoning_framework=(
            "Lost circulation occurs when drilling fluids are lost to formation fractures or highly permeable zones, leading to reduced hydrostatic pressure and potential well control issues.\n\n"
            "Management involves identifying loss zones, selecting appropriate Lost Circulation Materials (LCM), and implementing remedial techniques.\n\n"
            "Squeeze cementing involves pumping cement into the loss zone under pressure to seal fractures or voids.\n\n"
            "Cement bridge plugs provide mechanical barriers to isolate problematic zones for remedial operations or abandonment.\n\n"
            "Proper diagnosis of loss type (fracture, seepage, or cavern) guides selection of LCM and remedial methods.\n\n"
            "Industry standards such as API RP 10B-2 provide guidance on cementing and remedial operations.\n\n"
            "In conclusion, timely and appropriate lost circulation management preserves wellbore integrity and reduces operational risks."
        ),
        key_factors=[
            "Type and severity of lost circulation",
            "Formation characteristics and permeability",
            "LCM selection and compatibility",
            "Squeeze cement design and placement",
            "Bridge plug specifications",
            "Wellbore pressure management",
            "Operational timing and coordination",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 10B-2: Recommended Practice for Testing Well Cements",
            "Schlumberger Lost Circulation Handbook",
            "IADC Drilling Manual, Lost Circulation Chapter",
            "SPE Paper 112233: Advances in Lost Circulation Materials",
            "BSEE Lost Circulation Guidelines"
        ],
        burden_holder="Drilling Engineer / Remedial Cementing Specialist",
        adversary_position=(
            "Some operators delay remedial action to avoid downtime, risking well control incidents."
        ),
        counter_arguments=[
            "Delayed response exacerbates fluid loss and well control risks.",
            "Proper LCM and squeeze cementing restore wellbore integrity.",
            "Bridge plugs enable safe isolation of problematic zones.",
            "Regulatory bodies require prompt remedial actions.",
            "Timely intervention reduces overall operational costs."
        ],
        resolution_strategy=(
            "Implement early detection of lost circulation, select appropriate LCM, "
            "design and execute squeeze cement jobs promptly, and deploy bridge plugs as needed."
        ),
        entity_scope="Lost Circulation and Remedial Cementing",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 and BSEE lost circulation management standards"
    ),
    DoctrineBlock(
        topic="Stuck Pipe Prevention and Fishing Operations",
        keywords=["stuck pipe", "differential sticking", "pack-off", "key seat", "fishing", "wellbore geometry", "mud properties", "torque and drag"],
        conclusion_template=(
            "Preventing stuck pipe through mud property optimization, wellbore geometry control, and torque and drag analysis, "
            "combined with effective fishing operations, minimizes non-productive time and operational risks."
        ),
        reasoning_framework=(
            "Stuck pipe incidents result from mechanical or differential sticking, pack-off, key seat formation, or wellbore instability.\n\n"
            "Differential sticking occurs when the drill string is pressed against permeable formations by differential pressure, immobilizing the pipe.\n\n"
            "Pack-off results from cuttings accumulation or hole collapse, while key seats form from repeated contact between the drill string and wellbore wall.\n\n"
            "Preventive measures include optimizing mud weight and rheology to maintain wellbore stability and minimize differential pressure, "
            "controlling drilling parameters to reduce torque and drag, and maintaining proper hole cleaning.\n\n"
            "Fishing operations involve retrieving stuck or lost tools using specialized equipment and techniques.\n\n"
            "Industry guidelines such as API RP 13B-1 and IADC fishing manuals provide best practices.\n\n"
            "In conclusion, integrated prevention and remediation strategies reduce stuck pipe risks and improve drilling efficiency."
        ),
        key_factors=[
            "Mud weight and rheology",
            "Wellbore geometry and stability",
            "Torque and drag monitoring",
            "Cuttings transport and hole cleaning",
            "Fishing tool selection and techniques",
            "Drilling parameter optimization",
            "Personnel training and procedures",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 13B-1: Recommended Practice for Field Testing of Drilling Fluids",
            "IADC Fishing Manual",
            "Schlumberger Drilling Engineering Handbook",
            "SPE Paper 135791: Stuck Pipe Prevention Strategies",
            "BSEE Wellbore Stability Guidelines"
        ],
        burden_holder="Drilling Engineer / Fishing Specialist",
        adversary_position=(
            "Some operators accept higher stuck pipe risk to maintain aggressive drilling parameters."
        ),
        counter_arguments=[
            "Increased stuck pipe incidents cause costly delays and equipment damage.",
            "Optimized mud and drilling parameters reduce stuck pipe risk.",
            "Effective fishing operations recover lost tools and minimize downtime.",
            "Regulatory standards promote wellbore stability and safety.",
            "Training improves response to stuck pipe situations."
        ],
        resolution_strategy=(
            "Implement mud and drilling parameter optimization, monitor torque and drag, "
            "maintain hole cleaning, and prepare fishing plans for rapid response."
        ),
        entity_scope="Hole Problems and Fishing Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 and IADC fishing best practices"
    ),
    DoctrineBlock(
        topic="Completion Design: Open Hole and Cased Hole",
        keywords=["completion design", "open hole", "cased hole", "frac pack", "SSD", "sand control", "production optimization", "well integrity"],
        conclusion_template=(
            "Completion design tailored to reservoir characteristics, including open hole and cased hole options with frac pack and SSD techniques, "
            "optimizes production while ensuring well integrity and sand control."
        ),
        reasoning_framework=(
            "Completion design determines the configuration of the producing interval, influencing production rates, sand control, and well longevity.\n\n"
            "Open hole completions involve leaving the formation exposed, often combined with gravel packing or frac packing to control sand production.\n\n"
            "Cased hole completions use perforated casing and may incorporate SSD (Selective Stimulation and Drainage) to enhance production.\n\n"
            "Frac pack completions combine hydraulic fracturing with gravel packing to improve conductivity and sand control.\n\n"
            "Design considerations include formation properties, reservoir pressure, fluid characteristics, and production strategy.\n\n"
            "Standards such as API RP 90 provide guidelines for completion design and testing.\n\n"
            "In conclusion, selecting the appropriate completion type and stimulation method based on reservoir data maximizes production and well integrity."
        ),
        key_factors=[
            "Reservoir lithology and permeability",
            "Sand production risk",
            "Completion type (open hole vs cased hole)",
            "Frac pack and gravel pack design",
            "Selective stimulation techniques",
            "Production optimization goals",
            "Well integrity and zonal isolation",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 90: Recommended Practice for Completion Design",
            "Schlumberger Completion Engineering Handbook",
            "IADC Completion Guidelines",
            "SPE Paper 112244: Advances in Frac Pack Completions",
            "BSEE Completion and Stimulation Regulations"
        ],
        burden_holder="Completion Engineer",
        adversary_position=(
            "Some operators prefer simpler open hole completions to reduce upfront costs."
        ),
        counter_arguments=[
            "Simpler completions may lead to sand production and reduced well life.",
            "Frac pack and SSD improve production and control sand effectively.",
            "Proper design reduces workovers and non-productive time.",
            "Regulatory standards require well integrity and sand control measures.",
            "Long-term cost savings justify advanced completion techniques."
        ],
        resolution_strategy=(
            "Evaluate reservoir data thoroughly, select completion type accordingly, "
            "design frac pack or SSD treatments, and monitor production performance."
        ),
        entity_scope="Completion Design and Production Optimization",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 90 and industry completion design standards"
    ),
    DoctrineBlock(
        topic="Rig Selection: Land, Offshore Platform, Jackup, Drillship",
        keywords=["rig selection", "land rig", "offshore platform", "jackup rig", "drillship", "capability", "mobility", "water depth"],
        conclusion_template=(
            "Selecting the appropriate rig type based on operational environment, water depth, and project requirements ensures safe and efficient drilling operations."
        ),
        reasoning_framework=(
            "Rig selection is a strategic decision influenced by location, water depth, well complexity, and logistical considerations.\n\n"
            "Land rigs are suitable for onshore operations with relatively simple logistics and infrastructure.\n\n"
            "Offshore platform rigs operate from fixed platforms, ideal for shallow water and development drilling.\n\n"
            "Jackup rigs are mobile units that can be positioned in shallow to moderate water depths, offering flexibility and stability.\n\n"
            "Drillships provide mobility and capability for deepwater and ultra-deepwater drilling, equipped with dynamic positioning systems.\n\n"
            "Factors such as rig capacity, derrick height, mud system, BOP compatibility, and crew expertise influence selection.\n\n"
            "Regulatory compliance and environmental considerations also impact rig choice.\n\n"
            "In conclusion, aligning rig capabilities with project requirements and environmental conditions optimizes operational efficiency and safety."
        ),
        key_factors=[
            "Operational environment (land vs offshore)",
            "Water depth and seabed conditions",
            "Well complexity and depth",
            "Rig mobility and positioning systems",
            "Equipment capacity and specifications",
            "Crew expertise and safety record",
            "Logistical support and infrastructure",
            "Regulatory and environmental compliance"
        ],
        primary_authority=[
            "IADC Rig Classification and Selection Guidelines",
            "API RP 2D: Operation and Maintenance of Offshore Cranes",
            "Schlumberger Drilling Engineering Handbook",
            "SPE Paper 135790: Rig Selection Strategies for Offshore Drilling",
            "BSEE Offshore Drilling Regulations"
        ],
        burden_holder="Project Manager / Drilling Engineer",
        adversary_position=(
            "Some stakeholders prioritize cost savings over rig capability, risking operational delays."
        ),
        counter_arguments=[
            "Inadequate rig capability increases risk of non-productive time and accidents.",
            "Proper rig selection ensures compliance and operational efficiency.",
            "Advanced rigs reduce drilling time and improve safety.",
            "Regulatory bodies require suitable rig equipment and certifications.",
            "Long-term project success depends on rig suitability."
        ],
        resolution_strategy=(
            "Conduct comprehensive project and environmental assessment, evaluate rig capabilities, "
            "and select rig that meets technical and regulatory requirements."
        ),
        entity_scope="Rig Selection and Drilling Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="IADC rig selection standards and BSEE regulations"
    ),
    DoctrineBlock(
        topic="Formation Evaluation Using MWD, LWD, and Wireline Logs",
        keywords=["formation evaluation", "MWD", "LWD", "wireline logs", "log interpretation", "porosity", "permeability", "fluid saturation"],
        conclusion_template=(
            "Comprehensive formation evaluation integrating MWD, LWD, and wireline log data enables accurate reservoir characterization and informed drilling decisions."
        ),
        reasoning_framework=(
            "Formation evaluation determines reservoir properties critical to drilling and production planning.\n\n"
            "Measurement While Drilling (MWD) and Logging While Drilling (LWD) provide real-time data on formation gamma ray, resistivity, density, and porosity.\n\n"
            "Wireline logs offer high-resolution post-drilling data including neutron porosity, sonic velocity, and formation fluid identification.\n\n"
            "Integration of these data sets allows interpretation of lithology, porosity, permeability, and fluid saturation.\n\n"
            "Advanced interpretation techniques, including petrophysical modeling and geostatistics, enhance reservoir understanding.\n\n"
            "Accurate formation evaluation reduces drilling risks, optimizes completion design, and improves production forecasting.\n\n"
            "Industry standards such as API RP 40 and SPE guidelines govern logging practices and interpretation.\n\n"
            "In conclusion, multi-technology formation evaluation supports efficient and safe drilling and reservoir management."
        ),
        key_factors=[
            "MWD and LWD tool capabilities",
            "Wireline logging tool selection",
            "Data quality and calibration",
            "Petrophysical interpretation methods",
            "Reservoir heterogeneity",
            "Integration with geological models",
            "Real-time data processing",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 40: Recommended Practice for Formation Evaluation",
            "Schlumberger Formation Evaluation Handbook",
            "IADC Logging and Evaluation Guidelines",
            "SPE Paper 145679: Integrated Formation Evaluation Techniques",
            "Society of Exploration Geophysicists (SEG) Publications"
        ],
        burden_holder="Formation Evaluation Engineer",
        adversary_position=(
            "Some operators rely solely on wireline logs, delaying decisions and increasing costs."
        ),
        counter_arguments=[
            "Real-time MWD/LWD data enables immediate decision-making and reduces non-productive time.",
            "Integrated data improves reservoir characterization accuracy.",
            "Delays increase operational costs and risks.",
            "Regulatory bodies encourage real-time formation evaluation.",
            "Advanced interpretation reduces uncertainty."
        ],
        resolution_strategy=(
            "Deploy integrated MWD, LWD, and wireline logging programs, "
            "ensure data quality, and apply advanced interpretation techniques."
        ),
        entity_scope="Formation Evaluation and Reservoir Characterization",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 40 and SPE formation evaluation standards"
    ),
    DoctrineBlock(
        topic="Torque and Drag Modeling and Analysis",
        keywords=["torque", "drag", "modeling", "friction factor", "hookload", "braking analysis", "drill string", "wellbore friction"],
        conclusion_template=(
            "Accurate torque and drag modeling incorporating friction factors and hookload analysis is essential for predicting drill string behavior and preventing stuck pipe incidents."
        ),
        reasoning_framework=(
            "Torque and drag are critical mechanical phenomena affecting drill string performance, influenced by friction between the drill string and wellbore.\n\n"
            "Modeling involves calculating the torque required to rotate the drill string and the drag forces resisting axial movement.\n\n"
            "Friction factors depend on mud properties, wellbore geometry, and contact conditions.\n\n"
            "Hookload measurements provide real-time data to validate models and detect anomalies.\n\n"
            "Braking analysis assesses the forces during stopping or starting rotation, critical for preventing drill string damage.\n\n"
            "Accurate modeling informs drilling parameter optimization, BHA design, and stuck pipe prevention.\n\n"
            "Industry software tools incorporate complex mechanical and hydraulic interactions for precise predictions.\n\n"
            "In conclusion, integrating torque and drag modeling with real-time data enhances drilling safety and efficiency."
        ),
        key_factors=[
            "Friction factor determination",
            "Mud rheology and lubricity",
            "Wellbore trajectory and geometry",
            "Drill string and BHA configuration",
            "Hookload and torque measurements",
            "Braking force analysis",
            "Real-time monitoring and modeling",
            "Operational parameter optimization"
        ],
        primary_authority=[
            "API RP 13B-1: Recommended Practice for Field Testing of Drilling Fluids",
            "Schlumberger Drilling Engineering Handbook",
            "IADC Drilling Manual, Torque and Drag Chapter",
            "SPE Paper 123987: Advances in Torque and Drag Modeling",
            "National Institute for Occupational Safety and Health (NIOSH) Drilling Safety Publications"
        ],
        burden_holder="Drilling Engineer / Mechanical Engineer",
        adversary_position=(
            "Some operators underestimate torque and drag effects, leading to equipment failure."
        ),
        counter_arguments=[
            "Ignoring torque and drag increases risk of stuck pipe and drill string fatigue.",
            "Modeling enables proactive parameter adjustments.",
            "Real-time data validates and refines models.",
            "Regulatory bodies emphasize mechanical integrity.",
            "Proper analysis reduces non-productive time."
        ],
        resolution_strategy=(
            "Implement torque and drag modeling tools, monitor hookload and torque, "
            "and adjust drilling parameters to mitigate risks."
        ),
        entity_scope="Mechanical Drilling Engineering",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 and IADC torque and drag guidelines"
    ),
    DoctrineBlock(
        topic="Hydraulics: Equivalent Circulating Density and Bit Nozzle Optimization",
        keywords=["hydraulics", "ECD", "ESD", "standpipe pressure", "bit nozzle", "nozzle size", "hole cleaning", "pressure losses"],
        conclusion_template=(
            "Optimizing bit nozzle size and hydraulics to control Equivalent Circulating Density (ECD) and standpipe pressure enhances hole cleaning and minimizes formation damage."
        ),
        reasoning_framework=(
            "Hydraulics in drilling involves managing fluid flow to ensure effective cuttings transport, bit cooling, and wellbore pressure control.\n\n"
            "Equivalent Circulating Density (ECD) represents the effective mud density during circulation, accounting for pressure losses and annular friction.\n\n"
            "Excessive ECD can fracture the formation, causing lost circulation, while insufficient ECD risks wellbore instability.\n\n"
            "Bit nozzle size and configuration directly affect jet velocity, impact force, and pressure losses.\n\n"
            "Optimizing nozzle size balances hydraulic horsepower at the bit and annular velocity for efficient hole cleaning.\n\n"
            "Standpipe pressure monitoring provides real-time feedback on hydraulic performance.\n\n"
            "Hydraulic modeling software simulates flow regimes and pressure profiles to guide design.\n\n"
            "In conclusion, hydraulic optimization ensures drilling efficiency, wellbore stability, and formation protection."
        ),
        key_factors=[
            "Equivalent Circulating Density (ECD)",
            "Bit nozzle size and number",
            "Standpipe and annular pressure",
            "Mud rheology and density",
            "Hole cleaning efficiency",
            "Formation fracture gradient",
            "Hydraulic horsepower at bit",
            "Real-time pressure monitoring"
        ],
        primary_authority=[
            "API RP 13B-1: Recommended Practice for Field Testing of Drilling Fluids",
            "Schlumberger Drilling Engineering Handbook",
            "IADC Drilling Manual, Hydraulics Chapter",
            "SPE Paper 145123: Bit Nozzle Optimization Techniques",
            "National Energy Technology Laboratory (NETL) Drilling Hydraulics Reports"
        ],
        burden_holder="Drilling Fluids Engineer / Hydraulics Specialist",
        adversary_position=(
            "Some operators use standard nozzle sizes without optimization, risking inefficient hydraulics."
        ),
        counter_arguments=[
            "Non-optimized hydraulics reduce hole cleaning and increase formation damage risk.",
            "ECD control prevents lost circulation and wellbore instability.",
            "Real-time monitoring enables dynamic adjustments.",
            "Hydraulic modeling improves design accuracy.",
            "Regulatory standards require pressure management."
        ],
        resolution_strategy=(
            "Conduct hydraulic modeling, optimize bit nozzle configuration, monitor pressures, "
            "and adjust mud properties to maintain optimal ECD."
        ),
        entity_scope="Drilling Hydraulics and Fluid Engineering",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 and IADC hydraulic optimization standards"
    ),
    DoctrineBlock(
        topic="Drilling Safety: IADC JSA, STOP Card, and Incident Investigation",
        keywords=["drilling safety", "IADC", "JSA", "STOP card", "incident investigation", "hazard identification", "risk assessment", "safety culture"],
        conclusion_template=(
            "Implementing IADC Job Safety Analysis (JSA), STOP card programs, and thorough incident investigations fosters a proactive safety culture and reduces drilling incidents."
        ),
        reasoning_framework=(
            "Drilling safety programs aim to identify hazards, assess risks, and implement controls to protect personnel and assets.\n\n"
            "The International Association of Drilling Contractors (IADC) promotes Job Safety Analysis (JSA) to systematically evaluate tasks and hazards before work begins.\n\n"
            "STOP cards empower workers to halt unsafe activities and report hazards, promoting active participation in safety.\n\n"
            "Incident investigations analyze root causes of accidents or near misses to prevent recurrence.\n\n"
            "Effective safety culture integrates leadership commitment, training, communication, and continuous improvement.\n\n"
            "Regulatory frameworks such as OSHA and BSEE mandate safety management systems and reporting.\n\n"
            "In conclusion, structured safety programs and incident analysis enhance operational safety and compliance."
        ),
        key_factors=[
            "Hazard identification and risk assessment",
            "Worker participation and empowerment",
            "Leadership commitment",
            "Training and competency",
            "Incident reporting and investigation",
            "Safety communication and culture",
            "Regulatory compliance (OSHA, BSEE)",
            "Continuous improvement"
        ],
        primary_authority=[
            "IADC Drilling Safety Manual",
            "OSHA 29 CFR 1910.146: Permit-Required Confined Spaces",
            "BSEE Safety and Environmental Management Systems (SEMS)",
            "SPE Paper 112355: Enhancing Safety Culture in Drilling",
            "National Safety Council (NSC) Guidelines"
        ],
        burden_holder="Safety Manager / Drilling Supervisor",
        adversary_position=(
            "Some organizations treat safety programs as paperwork, lacking genuine engagement."
        ),
        counter_arguments=[
            "Poor safety culture increases incidents and costs.",
            "Active worker participation improves hazard recognition.",
            "Leadership commitment drives safety performance.",
            "Regulatory bodies enforce safety management requirements.",
            "Incident investigations prevent repeat accidents."
        ],
        resolution_strategy=(
            "Implement comprehensive JSA and STOP card programs, conduct thorough incident investigations, "
            "and foster leadership and worker engagement in safety."
        ),
        entity_scope="Drilling Safety Management",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="OSHA regulations and IADC safety program standards"
    ),
    DoctrineBlock(
        topic="Horizontal Drilling: Curve Build, Rate, Tangent, Lateral Landing",
        keywords=["horizontal drilling", "curve build", "build rate", "tangent section", "lateral landing", "dogleg severity", "wellbore trajectory", "directional control"],
        conclusion_template=(
            "Precise control of curve build rate and tangent section in horizontal drilling enables accurate lateral landing, optimizing reservoir exposure and drilling efficiency."
        ),
        reasoning_framework=(
            "Horizontal drilling involves steering the wellbore from vertical to horizontal to maximize reservoir contact.\n\n"
            "The curve build section gradually increases inclination, controlled by build rate and dogleg severity, to minimize mechanical stress.\n\n"
            "The tangent section maintains target inclination and azimuth before lateral landing into the reservoir.\n\n"
            "Accurate directional control during these phases is essential to avoid wellbore collision, maintain hole quality, and optimize production.\n\n"
            "MWD/LWD tools provide real-time feedback for trajectory adjustments.\n\n"
            "Mechanical limits of the drill string and BHA must be considered to prevent fatigue and failure.\n\n"
            "Industry standards and best practices guide build rates and dogleg severity limits.\n\n"
            "In conclusion, controlled curve build and tangent sections ensure successful horizontal well placement."
        ),
        key_factors=[
            "Build rate and dogleg severity limits",
            "Directional control accuracy",
            "MWD/LWD data quality",
            "BHA and drill string mechanical limits",
            "Wellbore stability",
            "Reservoir target positioning",
            "Hole cleaning during curve build",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 13B-1: Recommended Practice for Field Testing of Drilling Fluids",
            "IADC Drilling Manual, Horizontal Drilling Chapter",
            "Schlumberger Drilling Engineering Handbook",
            "SPE Paper 123654: Horizontal Drilling Trajectory Control",
            "NORSOK D-010: Well Integrity in Drilling and Well Operations"
        ],
        burden_holder="Directional Driller / Drilling Engineer",
        adversary_position=(
            "Some operators push build rates beyond limits to reduce drilling time."
        ),
        counter_arguments=[
            "Excessive build rates increase dogleg severity and mechanical stress.",
            "Controlled build rates extend drill string and BHA life.",
            "Accurate directional control prevents wellbore collision.",
            "Regulatory standards specify build rate limits.",
            "Proper hole cleaning reduces mechanical problems."
        ],
        resolution_strategy=(
            "Adhere to build rate and dogleg severity limits, utilize real-time MWD/LWD data, "
            "and monitor mechanical parameters to ensure safe horizontal drilling."
        ),
        entity_scope="Directional Drilling - Horizontal Wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 and IADC horizontal drilling guidelines"
    ),
    DoctrineBlock(
        topic="Managed Pressure Drilling (MPD) and Constant Bottomhole Pressure",
        keywords=["managed pressure drilling", "MPD", "constant bottomhole pressure", "pressure control", "annular pressure", "surface backpressure", "wellbore stability", "drilling optimization"],
        conclusion_template=(
            "Managed Pressure Drilling employing constant bottomhole pressure techniques enhances wellbore stability and drilling efficiency in challenging pressure environments."
        ),
        reasoning_framework=(
            "Managed Pressure Drilling (MPD) is an adaptive drilling process that precisely controls annular pressure profile to manage narrow pressure windows.\n\n"
            "Constant Bottomhole Pressure (CBHP) is an MPD method maintaining steady pressure at the bit, reducing risks of kicks and losses.\n\n"
            "MPD uses surface backpressure, choke control, and real-time monitoring to adjust pressures dynamically.\n\n"
            "Benefits include improved wellbore stability, reduced non-productive time, and enhanced safety in depleted or overpressured formations.\n\n"
            "MPD requires specialized equipment, trained personnel, and integration with well control systems.\n\n"
            "Industry standards such as IADC MPD guidelines and API RP 92 provide frameworks for implementation.\n\n"
            "In conclusion, MPD with CBHP techniques optimizes drilling in complex pressure regimes."
        ),
        key_factors=[
            "Pressure window characterization",
            "Surface backpressure control",
            "Real-time pressure monitoring",
            "Choke and mud pump coordination",
            "Equipment reliability",
            "Personnel training",
            "Regulatory compliance",
            "Integration with well control systems"
        ],
        primary_authority=[
            "IADC Managed Pressure Drilling Guidelines",
            "API RP 92: Managed Pressure Drilling Operations",
            "Schlumberger Drilling Engineering Handbook",
            "SPE Paper 145678: MPD Applications and Case Studies",
            "BSEE MPD Regulatory Framework"
        ],
        burden_holder="Drilling Engineer / MPD Specialist",
        adversary_position=(
            "Some operators view MPD as cost-prohibitive and complex."
        ),
        counter_arguments=[
            "MPD reduces drilling risks and non-productive time, offsetting costs.",
            "MPD enables drilling in challenging formations otherwise inaccessible.",
            "Training and technology advances simplify MPD implementation.",
            "Regulatory bodies encourage MPD for well control enhancement.",
            "Case studies demonstrate MPD operational benefits."
        ],
        resolution_strategy=(
            "Invest in MPD technology and training, perform detailed pressure modeling, "
            "and integrate MPD into well planning and execution."
        ),
        entity_scope="Managed Pressure Drilling Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="IADC and API RP 92 MPD standards"
    ),
    DoctrineBlock(
        topic="Underbalanced Drilling (UBD) with Nitrogen Foam and Aerated Fluids",
        keywords=["underbalanced drilling", "UBD", "nitrogen foam", "aerated fluids", "wellbore pressure", "formation damage", "hole cleaning", "kick tolerance"],
        conclusion_template=(
            "Underbalanced drilling using nitrogen foam and aerated fluids minimizes formation damage and improves drilling rates while managing wellbore pressure effectively."
        ),
        reasoning_framework=(
            "Underbalanced Drilling (UBD) maintains wellbore pressure below formation pressure to prevent fluid invasion and formation damage.\n\n"
            "Nitrogen foam and aerated fluids reduce hydrostatic pressure while maintaining effective hole cleaning and cooling.\n\n"
            "UBD enhances rate of penetration and reservoir productivity by minimizing formation damage.\n\n"
            "Challenges include managing influxes, maintaining well control, and ensuring fluid stability.\n\n"
            "Specialized surface equipment and trained personnel are required for safe UBD operations.\n\n"
            "Industry guidelines such as IADC UBD recommended practices provide operational frameworks.\n\n"
            "In conclusion, UBD with nitrogen foam and aerated fluids offers significant advantages when properly managed."
        ),
        key_factors=[
            "Wellbore pressure management",
            "Nitrogen injection and foam quality",
            "Fluid rheology and stability",
            "Kick detection and well control",
            "Hole cleaning efficiency",
            "Surface equipment capability",
            "Personnel training",
            "Regulatory compliance"
        ],
        primary_authority=[
            "IADC Underbalanced Drilling Recommended Practices",
            "API RP 92: Managed Pressure Drilling Operations",
            "Schlumberger Drilling Engineering Handbook",
            "SPE Paper 123456: UBD with Nitrogen Foam Applications",
            "BSEE UBD Safety Guidelines"
        ],
        burden_holder="Drilling Engineer / UBD Specialist",
        adversary_position=(
            "Some operators avoid UBD due to complexity and perceived risks."
        ),
        counter_arguments=[
            "UBD reduces formation damage and improves drilling efficiency.",
            "Proper training and equipment mitigate risks.",
            "UBD enables drilling in sensitive formations.",
            "Regulatory bodies provide safety frameworks.",
            "Industry experience supports UBD benefits."
        ],
        resolution_strategy=(
            "Develop UBD procedures, train personnel, deploy appropriate equipment, "
            "and monitor operations closely to ensure safety and efficiency."
        ),
        entity_scope="Underbalanced Drilling Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="IADC UBD guidelines and BSEE regulations"
    ),
    DoctrineBlock(
        topic="Casing While Drilling (CwD), Liner Drilling, and Expandable Tubulars",
        keywords=["casing while drilling", "CwD", "liner drilling", "expandable tubulars", "wellbore integrity", "drilling efficiency", "well construction", "mechanical properties"],
        conclusion_template=(
            "Employing casing while drilling, liner drilling, and expandable tubulars enhances well construction efficiency and wellbore integrity in complex drilling environments."
        ),
        reasoning_framework=(
            "Casing While Drilling (CwD) integrates casing running with drilling operations, reducing trip times and exposure to wellbore instability.\n\n"
            "Liner drilling involves drilling with a liner string, minimizing open hole exposure and improving wellbore support.\n\n"
            "Expandable tubulars allow diameter enlargement after installation, optimizing wellbore size and zonal isolation.\n\n"
            "These technologies improve drilling efficiency, reduce non-productive time, and enhance well integrity.\n\n"
            "Mechanical properties of casing and expandable tubulars must meet operational and regulatory requirements.\n\n"
            "Challenges include equipment reliability, operational complexity, and cost.\n\n"
            "Industry standards such as API Spec 5CT and ISO 13679 govern tubular specifications.\n\n"
            "In conclusion, advanced tubular technologies support efficient and safe well construction."
        ),
        key_factors=[
            "Equipment design and reliability",
            "Operational procedures and training",
            "Mechanical properties and specifications",
            "Wellbore stability and integrity",
            "Cost-benefit analysis",
            "Regulatory compliance",
            "Integration with drilling operations",
            "Risk management"
        ],
        primary_authority=[
            "API Spec 5CT: Specification for Casing and Tubing",
            "ISO 13679: Petroleum and Natural Gas Industries - Casing and Tubing",
            "Schlumberger Well Construction Manual",
            "SPE Paper 145679: Advances in Casing While Drilling",
            "IADC Drilling Manual, Tubular Technologies Chapter"
        ],
        burden_holder="Well Construction Engineer",
        adversary_position=(
            "Some operators prefer conventional drilling due to perceived complexity and cost."
        ),
        counter_arguments=[
            "Advanced tubular technologies reduce trip times and wellbore exposure.",
            "Improved well integrity reduces remediation costs.",
            "Operational training mitigates complexity.",
            "Regulatory standards support tubular specifications.",
            "Long-term benefits outweigh upfront costs."
        ],
        resolution_strategy=(
            "Evaluate project requirements, select appropriate tubular technology, "
            "train personnel, and integrate with drilling operations."
        ),
        entity_scope="Well Construction and Tubular Technologies",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="API Spec 5CT and ISO 13679 tubular standards"
    ),
    DoctrineBlock(
        topic="Drill String Design: Bottom Hole Assembly (BHA), Stabilizers, Collars, Heavy Weight Drill Pipe",
        keywords=["drill string design", "BHA", "stabilizer", "drill collar", "heavy weight drill pipe", "vibration control", "wellbore stability", "mechanical properties"],
        conclusion_template=(
            "Optimized drill string design incorporating appropriate BHA components, stabilizers, collars, and heavy weight drill pipe controls vibration and maintains wellbore stability."
        ),
        reasoning_framework=(
            "Drill string design affects drilling efficiency, wellbore quality, and mechanical integrity.\n\n"
            "The Bottom Hole Assembly (BHA) includes drill collars for weight, stabilizers for directional control, and heavy weight drill pipe to transition between drill collars and drill pipe.\n\n"
            "Stabilizers maintain wellbore trajectory and reduce vibration.\n\n"
            "Heavy weight drill pipe provides stiffness and reduces fatigue.\n\n"
            "Proper design balances weight on bit, stiffness, and flexibility to optimize drilling performance and minimize mechanical failures.\n\n"
            "Vibration analysis identifies axial, lateral, and torsional modes to mitigate stick-slip and whirl.\n\n"
            "Industry standards such as API Spec 7-1 specify mechanical properties and testing.\n\n"
            "In conclusion, tailored drill string design enhances drilling efficiency and equipment longevity."
        ),
        key_factors=[
            "BHA configuration and component selection",
            "Mechanical properties of drill collars and pipe",
            "Stabilizer placement and design",
            "Vibration modes and mitigation",
            "Wellbore trajectory requirements",
            "Fatigue and wear considerations",
            "Operational parameters",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API Spec 7-1: Rotary Drill Stem Elements",
            "Schlumberger Drilling Engineering Handbook",
            "IADC Drilling Manual, Drill String Design Chapter",
            "SPE Paper 123321: Drill String Vibration Analysis",
            "National Institute for Occupational Safety and Health (NIOSH) Drilling Safety Publications"
        ],
        burden_holder="Drilling Engineer / Mechanical Engineer",
        adversary_position=(
            "Some operators use standard drill string configurations regardless of formation."
        ),
        counter_arguments=[
            "Non-optimized drill strings increase vibration and mechanical failures.",
            "Tailored BHA improves directional control and drilling efficiency.",
            "Vibration mitigation extends equipment life.",
            "Regulatory standards specify mechanical requirements.",
            "Proper design reduces non-productive time."
        ],
        resolution_strategy=(
            "Analyze formation and operational conditions, design BHA accordingly, "
            "monitor vibration, and adjust configuration as needed."
        ),
        entity_scope="Drill String Design and Mechanical Engineering",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API Spec 7-1 and IADC drill string design standards"
    ),
    DoctrineBlock(
        topic="Vibration Analysis: Axial, Lateral, Torsional, Stick-Slip",
        keywords=["vibration analysis", "axial vibration", "lateral vibration", "torsional vibration", "stick-slip", "drill string dynamics", "bit bounce", "mechanical failure"],
        conclusion_template=(
            "Comprehensive vibration analysis addressing axial, lateral, torsional modes and stick-slip phenomena is essential to prevent mechanical failures and optimize drilling performance."
        ),
        reasoning_framework=(
            "Drill string vibrations arise from dynamic interactions between the drill bit, formation, and drill string components.\n\n"
            "Axial vibration (bit bounce) causes vertical oscillations affecting penetration rate.\n\n"
            "Lateral vibration (whirl) induces bending stresses leading to fatigue.\n\n"
            "Torsional vibration (stick-slip) causes alternating torque spikes damaging equipment.\n\n"
            "Stick-slip occurs when the bit alternates between sticking and slipping, reducing ROP and causing mechanical damage.\n\n"
            "Vibration monitoring tools and modeling software detect and predict vibration modes.\n\n"
            "Mitigation strategies include BHA design optimization, drilling parameter adjustments, and use of vibration dampeners.\n\n"
            "Industry standards and research papers provide guidelines for vibration management.\n\n"
            "In conclusion, proactive vibration analysis and control improve drilling efficiency and equipment life."
        ),
        key_factors=[
            "Vibration mode identification",
            "Drill string and BHA design",
            "Drilling parameters (WOB, RPM)",
            "Formation characteristics",
            "Vibration monitoring tools",
            "Mitigation techniques",
            "Equipment fatigue and wear",
            "Operational training"
        ],
        primary_authority=[
            "SPE Paper 123789: Drill String Vibration Analysis and Mitigation",
            "Schlumberger Drilling Engineering Handbook",
            "IADC Drilling Manual, Vibration Control Chapter",
            "API RP 13B-1: Recommended Practice for Field Testing of Drilling Fluids",
            "National Institute for Occupational Safety and Health (NIOSH) Publications"
        ],
        burden_holder="Drilling Engineer / Mechanical Engineer",
        adversary_position=(
            "Some operators neglect vibration analysis due to perceived complexity."
        ),
        counter_arguments=[
            "Ignoring vibrations leads to equipment failure and increased costs.",
            "Monitoring and mitigation improve drilling performance.",
            "Training enhances understanding and response.",
            "Regulatory bodies emphasize mechanical integrity.",
            "Industry case studies demonstrate benefits."
        ],
        resolution_strategy=(
            "Implement vibration monitoring, analyze data, optimize BHA and parameters, "
            "and train personnel on vibration management."
        ),
        entity_scope="Drilling Mechanical Engineering and Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 123789 and API RP 13B-1 vibration guidelines"
    ),
    DoctrineBlock(
        topic="Hole Cleaning and Cuttings Transport Optimization",
        keywords=["hole cleaning", "cuttings transport", "minimum flow rate", "annular velocity", "mud rheology", "fluid dynamics", "wellbore stability", "cuttings bed"],
        conclusion_template=(
            "Optimizing hole cleaning through appropriate flow rates, annular velocity, and mud rheology prevents cuttings accumulation and maintains wellbore stability."
        ),
        reasoning_framework=(
            "Effective hole cleaning removes cuttings from the wellbore to prevent accumulation, which can cause stuck pipe and wellbore instability.\n\n"
            "Minimum flow rate and annular velocity are critical parameters ensuring cuttings suspension and transport.\n\n"
            "Mud rheology influences carrying capacity, with yield point and plastic viscosity affecting cuttings suspension.\n\n"
            "Fluid dynamics modeling helps predict cuttings transport efficiency under varying conditions.\n\n"
            "Poor hole cleaning leads to cuttings beds, key seats, and pack-offs, increasing torque and drag.\n\n"
            "Real-time monitoring of drilling parameters and mud properties supports dynamic adjustments.\n\n"
            "Industry standards such as API RP 13B-1 guide mud property testing and hole cleaning practices.\n\n"
            "In conclusion, maintaining optimal hydraulics and mud properties ensures efficient hole cleaning and drilling safety."
        ),
        key_factors=[
            "Minimum flow rate and annular velocity",
            "Mud rheology (YP, PV)",
            "Wellbore geometry and inclination",
            "Cuttings size and concentration",
            "Drilling parameters (ROP, RPM)",
            "Fluid dynamics and modeling",
            "Real-time monitoring",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 13B-1: Recommended Practice for Field Testing of Drilling Fluids",
            "Schlumberger Drilling Engineering Handbook",
            "IADC Drilling Manual, Hole Cleaning Chapter",
            "SPE Paper 112233: Cuttings Transport Optimization",
            "National Energy Technology Laboratory (NETL) Drilling Reports"
        ],
        burden_holder="Drilling Fluids Engineer / Drilling Engineer",
        adversary_position=(
            "Some operators reduce flow rates to save pumping costs, risking poor hole cleaning."
        ),
        counter_arguments=[
            "Insufficient flow causes cuttings accumulation and stuck pipe.",
            "Optimized hydraulics improve drilling efficiency and safety.",
            "Real-time adjustments prevent problems.",
            "Regulatory standards require effective hole cleaning.",
            "Long-term cost savings justify optimal flow rates."
        ],
        resolution_strategy=(
            "Determine minimum flow rates, optimize mud rheology, monitor parameters, "
            "and adjust operations to maintain hole cleaning."
        ),
        entity_scope="Drilling Fluid Engineering and Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 and IADC hole cleaning guidelines"
    ),
    DoctrineBlock(
        topic="Wellbore Stability and Geomechanics: Mud Weight Window and Pore Pressure",
        keywords=["wellbore stability", "geomechanics", "mud weight window", "pore pressure", "fracture gradient", "stress analysis", "formation integrity", "wellbore collapse"],
        conclusion_template=(
            "Maintaining mud weight within the geomechanical mud weight window, balancing pore pressure and fracture gradient, is essential to ensure wellbore stability and prevent collapse."
        ),
        reasoning_framework=(
            "Wellbore stability depends on the balance between formation stresses, pore pressure, and mud pressure.\n\n"
            "Geomechanical analysis defines the mud weight window between pore pressure (minimum) and fracture gradient (maximum).\n\n"
            "Operating outside this window risks wellbore collapse (underweight mud) or lost circulation (overweight mud).\n\n"
            "Stress analysis models in-situ stresses, rock strength, and anisotropy to predict failure mechanisms.\n\n"
            "Accurate pore pressure prediction through seismic, offset well data, and drilling parameters is critical.\n\n"
            "Mud weight adjustments and wellbore strengthening techniques mitigate stability risks.\n\n"
            "Industry standards such as API RP 40 and SPE guidelines govern geomechanical modeling.\n\n"
            "In conclusion, integrating geomechanics into mud weight design ensures safe and stable wellbore conditions."
        ),
        key_factors=[
            "Pore pressure estimation",
            "Fracture gradient determination",
            "In-situ stress modeling",
            "Rock mechanical properties",
            "Mud weight design and control",
            "Wellbore strengthening techniques",
            "Real-time monitoring",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 40: Recommended Practice for Formation Evaluation",
            "Schlumberger Drilling Engineering Handbook",
            "SPE Paper 123654: Geomechanics and Wellbore Stability",
            "IADC Drilling Manual, Wellbore Stability Chapter",
            "National Energy Technology Laboratory (NETL) Geomechanics Reports"
        ],
        burden_holder="Drilling Engineer / Geomechanics Specialist",
        adversary_position=(
            "Some operators use fixed mud weights without geomechanical analysis, risking instability."
        ),
        counter_arguments=[
            "Ignoring geomechanics increases risk of wellbore collapse and lost circulation.",
            "Mud weight window design optimizes drilling safety and efficiency.",
            "Real-time data refines models and adjustments.",
            "Regulatory bodies require geomechanical considerations.",
            "Advanced modeling reduces uncertainty."
        ],
        resolution_strategy=(
            "Perform detailed geomechanical modeling, integrate pore pressure data, "
            "design mud weight within window, and monitor wellbore conditions."
        ),
        entity_scope="Wellbore Stability and Geomechanics",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 40 and SPE geomechanics best practices"
    ),
    DoctrineBlock(
        topic="Surface Equipment: Derrick, Substructure, Drawworks, Power System",
        keywords=["surface equipment", "derrick", "substructure", "drawworks", "power system", "hoisting capacity", "equipment maintenance", "operational safety"],
        conclusion_template=(
            "Proper selection, maintenance, and operation of surface equipment including derrick, substructure, drawworks, and power systems ensure safe and efficient drilling operations."
        ),
        reasoning_framework=(
            "Surface equipment supports drilling operations by providing structural support, hoisting capability, and power.\n\n"
            "The derrick supports the drill string and hoisting equipment, designed for load capacity and stability.\n\n"
            "Substructure provides foundation and support for the derrick and equipment.\n\n"
            "Drawworks control hoisting and lowering of drill string, requiring reliable braking and power systems.\n\n"
            "Power systems supply energy for drawworks, mud pumps, and auxiliary equipment.\n\n"
            "Regular maintenance and inspections prevent failures and ensure compliance with safety standards.\n\n"
            "Operational safety protocols govern equipment use, load limits, and emergency procedures.\n\n"
            "In conclusion, integrated management of surface equipment underpins drilling safety and efficiency."
        ),
        key_factors=[
            "Equipment design and capacity",
            "Maintenance and inspection schedules",
            "Load monitoring and control",
            "Operator training",
            "Safety protocols and emergency systems",
            "Regulatory compliance",
            "Integration with drilling operations",
            "Environmental considerations"
        ],
        primary_authority=[
            "API RP 2D: Operation and Maintenance of Offshore Cranes",
            "IADC Drilling Manual, Surface Equipment Chapter",
            "OSHA 29 CFR 1910 Subpart P: Hand and Portable Powered Tools",
            "Schlumberger Drilling Engineering Handbook",
            "BSEE Surface Equipment Regulations"
        ],
        burden_holder="Rig Manager / Maintenance Supervisor",
        adversary_position=(
            "Some operators defer maintenance to reduce costs, risking equipment failure."
        ),
        counter_arguments=[
            "Poor maintenance increases accident risk and downtime.",
            "Proper equipment management enhances safety and productivity.",
            "Regulatory bodies mandate maintenance and inspections.",
            "Training improves operator competence.",
            "Investment in equipment reliability reduces long-term costs."
        ],
        resolution_strategy=(
            "Implement rigorous maintenance programs, train operators, "
            "monitor equipment loads, and enforce safety protocols."
        ),
        entity_scope="Surface Drilling Equipment and Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 2D and OSHA equipment safety standards"
    ),
    DoctrineBlock(
        topic="Drilling Contracts: IADC Dayrate, Footage, Turnkey, Integrated",
        keywords=["drilling contracts", "IADC", "dayrate", "footage", "turnkey", "integrated services", "risk allocation", "contract management"],
        conclusion_template=(
            "Selecting appropriate drilling contract types such as IADC dayrate, footage, turnkey, or integrated services aligns risk allocation with project objectives and optimizes operational efficiency."
        ),
        reasoning_framework=(
            "Drilling contracts define the commercial and operational relationship between operators and contractors.\n\n"
            "IADC dayrate contracts pay contractors a fixed daily rate regardless of footage drilled, "
            "transferring drilling risk to the operator. Footage contracts set a price per foot drilled, "
            "incentivizing the contractor to drill efficiently. Turnkey contracts provide a fixed price "
            "for the complete well, transferring most risk to the contractor. Integrated service contracts "
            "combine drilling with other services under one provider. The choice depends on well complexity, "
            "operator experience, risk appetite, and market conditions."
        ),
        key_factors=[
            "Risk allocation between operator and contractor",
            "Well complexity and uncertainty level",
            "Market conditions and rig availability",
            "Operator in-house capability and experience",
            "Historical performance data for contract type"
        ],
        primary_authority=[
            "IADC Model Form Drilling Contract",
            "AIPN Model Form Joint Operating Agreement",
            "API Recommended Practice for Drilling Operations"
        ],
        burden_holder="Operator and drilling contractor",
        adversary_position="Alternative contract structures better allocate risk for the specific well program.",
        counter_arguments=[
            "Dayrate contracts allow operator control over drilling decisions",
            "Footage contracts incentivize contractor efficiency",
            "Turnkey contracts provide budget certainty for operators",
            "Integrated contracts reduce interface management complexity",
            "Hybrid structures can combine benefits of multiple contract types"
        ],
        resolution_strategy="Evaluate well program risk profile, available contractor capability, and market conditions to select optimal contract structure.",
        entity_scope="Operators, drilling contractors, and service companies",
        confidence=0.88,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="IADC Model Form Drilling Contract"
    ),
]

# =============================================
# SUB-ENGINE ORCHESTRATION
# =============================================

ENGINE_IDS = [
    "DRL01", "DRL02", "DRL03", "DRL04", "DRL05", "DRL06", "DRL07", "DRL08",
    "DRL09", "DRL10", "DRL11", "DRL12", "DRL13", "DRL14", "DRL15"
]

ENGINE_URLS = {
    "DRL01": "http://drl01/wellbore-design",
    "DRL02": "http://drl02/drilling-fluid",
    "DRL03": "http://drl03/directional-drilling",
    "DRL04": "http://drl04/cementing-operations",
    "DRL05": "http://drl05/casing-design",
    "DRL06": "http://drl06/bit-selection",
    "DRL07": "http://drl07/drilling-optimization",
    "DRL08": "http://drl08/well-control",
    "DRL09": "http://drl09/hole-problems",
    "DRL10": "http://drl10/completion-design",
    "DRL11": "http://drl11/rig-selection",
    "DRL12": "http://drl12/formation-evaluation",
    "DRL13": "http://drl13/torque-drag",
    "DRL14": "http://drl14/hydraulics",
    "DRL15": "http://drl15/drilling-safety"
}

ENGINE_KEYWORDS = {
    "DRL01": ["wellbore", "trajectory", "design", "geometry"],
    "DRL02": ["fluid", "mud", "rheology", "density", "viscosity"],
    "DRL03": ["directional", "steering", "azimuth", "inclination", "survey"],
    "DRL04": ["cement", "slurry", "bond", "top", "shoe", "plug"],
    "DRL05": ["casing", "pipe", "diameter", "grade", "collapse", "burst"],
    "DRL06": ["bit", "selection", "roller", "cone", "pdc", "wear"],
    "DRL07": ["optimization", "rate", "ROP", "drilling", "efficiency"],
    "DRL08": ["well control", "kick", "blowout", "pressure", "shut-in"],
    "DRL09": ["hole", "problems", "stuck", "lost", "circulation", "bridging"],
    "DRL10": ["completion", "design", "perforation", "packer", "tubing"],
    "DRL11": ["rig", "selection", "capacity", "specification", "power"],
    "DRL12": ["formation", "evaluation", "log", "porosity", "permeability"],
    "DRL13": ["torque", "drag", "friction", "rotation", "pipe"],
    "DRL14": ["hydraulics", "pressure", "flow", "pump", "rate"],
    "DRL15": ["safety", "hazard", "risk", "incident", "PPE"]
}

ENGINE_PRIORITY = {
    "DRL01": 10, "DRL02": 9, "DRL03": 9, "DRL04": 8, "DRL05": 8, "DRL06": 7,
    "DRL07": 7, "DRL08": 10, "DRL09": 9, "DRL10": 8, "DRL11": 6, "DRL12": 7,
    "DRL13": 6, "DRL14": 7, "DRL15": 10
}

ENGINE_MODES = {
    "DRL01": "design",
    "DRL02": "fluid",
    "DRL03": "directional",
    "DRL04": "cementing",
    "DRL05": "casing",
    "DRL06": "bit",
    "DRL07": "optimization",
    "DRL08": "control",
    "DRL09": "problems",
    "DRL10": "completion",
    "DRL11": "rig",
    "DRL12": "formation",
    "DRL13": "torque-drag",
    "DRL14": "hydraulics",
    "DRL15": "safety"
}

# --- Data Structures ---

class SubEngineStatus(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    UNKNOWN = auto()

class CircuitBreakerState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class QueryRequest:
    def __init__(self, text: str, mode: Optional[str]=None, user_id: Optional[str]=None, metadata: Optional[Dict]=None):
        self.text = text
        self.mode = mode
        self.user_id = user_id
        self.metadata = metadata or {}

class RoutingDecision:
    def __init__(self, engines: List[str], rationale: str, fallback: Optional[List[str]]=None):
        self.engines = engines
        self.rationale = rationale
        self.fallback = fallback or []

class IssueCategory:
    def __init__(self, engine_id: str, category: str, score: float):
        self.engine_id = engine_id
        self.category = category
        self.score = score

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, priority: int, mode: str):
        self.engine_id = engine_id
        self.url = url
        self.priority = priority
        self.mode = mode

class SubEngineResponse:
    def __init__(self, engine_id: str, response: Any, status: SubEngineStatus, latency: float):
        self.engine_id = engine_id
        self.response = response
        self.status = status
        self.latency = latency

# --- Circuit Breaker Implementation ---

class CircuitBreaker:
    def __init__(self, engine_id: str, failure_threshold: int=5, recovery_timeout: int=30):
        self.engine_id = engine_id
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.last_failure_time = 0
        self.recovery_timeout = recovery_timeout
        self.success_count = 0
        self.half_open_success_threshold = 2

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

    def record_success(self):
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.half_open_success_threshold:
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        else:
            self.failure_count = 0

    def check_state(self):
        if self.state == CircuitBreakerState.OPEN:
            elapsed = time.time() - self.last_failure_time
            if elapsed > self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                self.success_count = 0
        return self.state

    def allow_request(self):
        self.check_state()
        return self.state in [CircuitBreakerState.CLOSED, CircuitBreakerState.HALF_OPEN]

# --- SubEngine Health Monitor ---

class SubEngineHealthMonitor:
    def __init__(self, engine_urls: Dict[str, str], ttl: int=30):
        self.engine_urls = engine_urls
        self.ttl = ttl
        self.health_cache: Dict[str, Tuple[SubEngineStatus, float]] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {
            eid: CircuitBreaker(eid) for eid in engine_urls.keys()
        }

    async def _ping_engine(self, url: str, timeout: int=3) -> SubEngineStatus:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url+"/health", timeout=timeout) as resp:
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
        url = self.engine_urls.get(engine_id)
        if not url:
            return SubEngineStatus.UNKNOWN
        status = await self._ping_engine(url)
        self.health_cache[engine_id] = (status, now)
        cb = self.circuit_breakers[engine_id]
        if status == SubEngineStatus.HEALTHY:
            cb.record_success()
        else:
            cb.record_failure()
        return status

    async def check_all_health(self) -> Dict[str, SubEngineStatus]:
        tasks = [self.check_health(eid) for eid in self.engine_urls.keys()]
        results = await asyncio.gather(*tasks)
        return {eid: status for eid, status in zip(self.engine_urls.keys(), results)}

    def get_healthy_engines(self) -> List[str]:
        now = time.time()
        healthy = []
        for eid in self.engine_urls.keys():
            cb = self.circuit_breakers[eid]
            if not cb.allow_request():
                continue
            if eid in self.health_cache:
                status, ts = self.health_cache[eid]
                if now - ts < self.ttl and status == SubEngineStatus.HEALTHY:
                    healthy.append(eid)
        return healthy

# --- Query Router ---

class QueryRouter:
    def __init__(self, engine_keywords: Dict[str, List[str]], engine_priority: Dict[str, int], engine_modes: Dict[str, str], health_monitor: SubEngineHealthMonitor):
        self.engine_keywords = engine_keywords
        self.engine_priority = engine_priority
        self.engine_modes = engine_modes
        self.health_monitor = health_monitor

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text_lower = text.lower()
        categories = []
        for eid, keywords in self.engine_keywords.items():
            score = 0
            for kw in keywords:
                if kw.lower() in text_lower:
                    score += 1
            if score > 0:
                categories.append(IssueCategory(engine_id=eid, category=self.engine_modes[eid], score=score))
        categories.sort(key=lambda c: c.score, reverse=True)
        return categories

    def _select_engines(self, categories: List[IssueCategory], mode: Optional[str]=None) -> List[SubEngineConfig]:
        selected = []
        healthy_engines = self.health_monitor.get_healthy_engines()
        for cat in categories:
            if cat.engine_id in healthy_engines:
                if mode is None or self.engine_modes[cat.engine_id] == mode:
                    selected.append(SubEngineConfig(
                        engine_id=cat.engine_id,
                        url=ENGINE_URLS[cat.engine_id],
                        priority=self.engine_priority[cat.engine_id],
                        mode=self.engine_modes[cat.engine_id]
                    ))
        if not selected and healthy_engines:
            # fallback: pick highest priority healthy engine
            fallback_eid = max(healthy_engines, key=lambda eid: self.engine_priority[eid])
            selected.append(SubEngineConfig(
                engine_id=fallback_eid,
                url=ENGINE_URLS[fallback_eid],
                priority=self.engine_priority[fallback_eid],
                mode=self.engine_modes[fallback_eid]
            ))
        return selected

    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        categories = self._classify_domain(query.text)
        selected_configs = self._select_engines(categories, query.mode)
        return [cfg.engine_id for cfg in selected_configs]

    def _score_engine_relevance(self, engine_id: str, query: QueryRequest) -> float:
        keywords = self.engine_keywords.get(engine_id, [])
        text = query.text.lower()
        score = sum([1 for kw in keywords if kw.lower() in text])
        priority = self.engine_priority.get(engine_id, 0)
        health = 1 if engine_id in self.health_monitor.get_healthy_engines() else 0
        return score * 2 + priority * 1.5 + health * 3

    def _handle_engine_failure(self, engine_id: str, error: Exception) -> List[str]:
        # fallback: exclude failed engine, reroute to next best
        healthy = self.health_monitor.get_healthy_engines()
        fallback = [eid for eid in healthy if eid != engine_id]
        return fallback

    def route_query(self, query: QueryRequest) -> RoutingDecision:
        categories = self._classify_domain(query.text)
        selected_configs = self._select_engines(categories, query.mode)
        rationale = f"Selected engines based on keyword match and health: {[cfg.engine_id for cfg in selected_configs]}"
        fallback = []
        if not selected_configs:
            fallback = self._handle_engine_failure(None, Exception("No healthy engines"))
        return RoutingDecision(
            engines=[cfg.engine_id for cfg in selected_configs],
            rationale=rationale,
            fallback=fallback
        )

# --- SubEngine Orchestrator ---

class SubEngineOrchestrator:
    def __init__(self, health_monitor: SubEngineHealthMonitor, circuit_breakers: Dict[str, CircuitBreaker]):
        self.health_monitor = health_monitor
        self.circuit_breakers = circuit_breakers

    async def _call_sub_engine(self, engine_config: SubEngineConfig, query: QueryRequest) -> SubEngineResponse:
        cb = self.circuit_breakers[engine_config.engine_id]
        if not cb.allow_request():
            return SubEngineResponse(engine_id=engine_config.engine_id, response=None, status=SubEngineStatus.UNHEALTHY, latency=0)
        url = engine_config.url
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url+"/query", json={"text": query.text, "mode": query.mode, "metadata": query.metadata}, timeout=8) as resp:
                    latency = time.time() - start
                    if resp.status == 200:
                        data = await resp.json()
                        cb.record_success()
                        return SubEngineResponse(engine_id=engine_config.engine_id, response=data, status=SubEngineStatus.HEALTHY, latency=latency)
                    else:
                        cb.record_failure()
                        return SubEngineResponse(engine_id=engine_config.engine_id, response=None, status=SubEngineStatus.UNHEALTHY, latency=latency)
        except Exception:
            cb.record_failure()
            latency = time.time() - start
            return SubEngineResponse(engine_id=engine_config.engine_id, response=None, status=SubEngineStatus.UNHEALTHY, latency=latency)

    async def dispatch_query(self, query: QueryRequest, engines: List[SubEngineConfig]) -> List[SubEngineResponse]:
        responses = []
        for engine in engines:
            resp = await self._call_sub_engine(engine, query)
            responses.append(resp)
        return responses

    async def dispatch_parallel(self, query: QueryRequest, engines: List[SubEngineConfig]) -> Dict[str, Any]:
        tasks = [self._call_sub_engine(engine, query) for engine in engines]
        responses = await asyncio.gather(*tasks)
        merged = self._merge_responses(responses)
        return merged

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
        # Consensus: majority response, else highest priority
        valid_resps = [resp for resp in responses if resp.status == SubEngineStatus.HEALTHY and resp.response is not None]
        if not valid_resps:
            return None
        resp_values = [str(resp.response) for resp in valid_resps]
        counts = {}
        for val in resp_values:
            counts[val] = counts.get(val, 0) + 1
        majority = max(counts.items(), key=lambda x: x[1])
        if majority[1] > 1:
            return majority[0]
        else:
            # highest priority engine response
            sorted_resps = sorted(valid_resps, key=lambda r: ENGINE_PRIORITY[r.engine_id], reverse=True)
            return sorted_resps[0].response

# --- Example Usage (for integration) ---

class DrillingIntelligenceDomainOrchestrator:
    def __init__(self):
        self.health_monitor = SubEngineHealthMonitor(ENGINE_URLS)
        self.query_router = QueryRouter(ENGINE_KEYWORDS, ENGINE_PRIORITY, ENGINE_MODES, self.health_monitor)
        self.circuit_breakers = self.health_monitor.circuit_breakers
        self.orchestrator = SubEngineOrchestrator(self.health_monitor, self.circuit_breakers)

    async def process_query(self, query: QueryRequest, strategy: str="parallel") -> Any:
        routing_decision = self.query_router.route_query(query)
        engines = []
        for eid in routing_decision.engines:
            engines.append(SubEngineConfig(
                engine_id=eid,
                url=ENGINE_URLS[eid],
                priority=ENGINE_PRIORITY[eid],
                mode=ENGINE_MODES[eid]
            ))
        if strategy == "parallel":
            return await self.orchestrator.dispatch_parallel(query, engines)
        elif strategy == "cascade":
            return await self.orchestrator.dispatch_cascade(query, engines)
        elif strategy == "all":
            responses = await self.orchestrator.dispatch_query(query, engines)
            return self.orchestrator._merge_responses(responses)
        else:
            responses = await self.orchestrator.dispatch_query(query, engines)
            return self.orchestrator._resolve_conflicts(responses)

# --- END PART 3 ---

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
    AuthorityLevel.REGULATORY: 70,
    AuthorityLevel.CASE_LAW: 60,
    AuthorityLevel.TREATISE: 50,
    AuthorityLevel.PRACTICE: 40,
}

def resolve_authority_conflict(sources: List[AuthorityLevel]) -> AuthorityLevel:
    if not sources:
        raise ValueError("No authority sources provided")
    max_weight = -1
    dominant = None
    for source in sources:
        weight = authority_weights.get(source, 0)
        if weight > max_weight:
            max_weight = weight
            dominant = source
    return dominant

# ------------------------------
# EPISTEMIC GUARDRAILS
# ------------------------------

BANNED_PHRASES = [
    "clearly", "obviously", "without doubt", "undeniably", "unquestionably",
    "incontrovertibly", "beyond question", "manifestly", "patently", "evidently",
    "plainly", "categorically", "definitely", "absolutely", "unequivocally",
    "indisputably", "incontestably", "inarguably", "decidedly", "positively",
    "beyond dispute", "without fail", "infallibly", "irrefutably", "manifestly",
    "conclusively", "categorically", "unconditionally", "beyond any doubt",
    "without exception", "undoubtedly"
]

EPISTEMIC_CONFIDENCE_LEVELS = Enum('ConfidenceLevel', 'DEFENSIBLE AGGRESSIVE DISCLOSURE HIGH_RISK')

def apply_epistemic_guardrails(text: str) -> Tuple[str, str]:
    """
    Remove banned phrases and append a disclosure caveat.
    Returns cleaned text and confidence stratification label.
    """
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, BANNED_PHRASES)) + r')\b', re.IGNORECASE)
    cleaned_text = pattern.sub('', text)
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()

    # Determine confidence stratification based on presence of banned phrases and hedging
    lowered = text.lower()
    banned_found = any(phrase in lowered for phrase in BANNED_PHRASES)
    hedge_phrases = ["likely", "possible", "suggests", "appears", "may", "could", "might", "probable"]
    hedge_found = any(hp in lowered for hp in hedge_phrases)

    if banned_found:
        confidence = EPISTEMIC_CONFIDENCE_LEVELS.AGGRESSIVE.name
    elif hedge_found:
        confidence = EPISTEMIC_CONFIDENCE_LEVELS.DEFENSIBLE.name
    else:
        confidence = EPISTEMIC_CONFIDENCE_LEVELS.HIGH_RISK.name

    disclosure_caveat = ("Note: This analysis is subject to epistemic guardrails and "
                         "should be interpreted with appropriate caution.")

    final_text = f"{cleaned_text} {disclosure_caveat}"
    return final_text.strip(), confidence

# ------------------------------
# FACT FRAGILITY SCORING
# ------------------------------

def score_fact_fragility(fact: str) -> Dict[str, float]:
    """
    Scores fact on:
    - verifiability (0-1): how easily it can be verified by independent sources
    - recharacterization_risk (0-1): risk fact can be reinterpreted or reframed
    - testimony_dependence (0-1): dependence on human testimony or subjective accounts
    """
    # Simple heuristics for demonstration:
    verifiability = 0.5
    recharacterization_risk = 0.5
    testimony_dependence = 0.5

    # Verifiability: check for presence of measurable quantities, dates, locations
    if re.search(r'\b(\d{4}|\d{1,3}(?:\.\d+)?\s*(meters|feet|barrels|psi|hours|days))\b', fact, re.IGNORECASE):
        verifiability += 0.3
    if re.search(r'\b(location|site|well|rig|platform)\b', fact, re.IGNORECASE):
        verifiability += 0.2

    # Recharacterization risk: presence of ambiguous terms or qualifiers
    ambiguous_terms = ["approximately", "about", "around", "some", "several", "few", "likely", "possible"]
    if any(term in fact.lower() for term in ambiguous_terms):
        recharacterization_risk += 0.3

    # Testimony dependence: presence of "reported", "said", "claimed", "according to"
    testimony_terms = ["reported", "said", "claimed", "according to", "witness", "interview"]
    if any(term in fact.lower() for term in testimony_terms):
        testimony_dependence += 0.4

    # Clamp scores between 0 and 1
    verifiability = min(max(verifiability, 0), 1)
    recharacterization_risk = min(max(recharacterization_risk, 0), 1)
    testimony_dependence = min(max(testimony_dependence, 0), 1)

    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence,
    }

# ------------------------------
# SEMANTIC NORMALIZATION
# ------------------------------

DOMAIN_TERM_MAPPINGS = {
    # drilling equipment
    "derrick": "rig_structure",
    "mud pump": "fluid_pump",
    "blowout preventer": "bop",
    "bop": "bop",
    "drill string": "drill_string",
    "drill pipe": "drill_string",
    "casing": "casing",
    "cementing": "cementing",
    "mud": "drilling_fluid",
    "drilling fluid": "drilling_fluid",
    "bit": "drill_bit",
    "drill bit": "drill_bit",
    "rotary table": "rotary_table",
    "kelly": "kelly",
    "top drive": "top_drive",
    "shale shaker": "shale_shaker",
    "mud logger": "mud_logger",
    "trip tank": "trip_tank",
    "wellbore": "wellbore",
    "formation": "formation",
    "hydrocarbon": "hydrocarbon",
    "gas kick": "gas_kick",
    "kick": "kick",
    "loss circulation": "loss_circulation",
    "well control": "well_control",
    "drilling parameters": "drilling_parameters",
    "rate of penetration": "rop",
    "rop": "rop",
    "weight on bit": "wob",
    "wob": "wob",
    "torque": "torque",
    "rpm": "rpm",
    "mud weight": "mud_weight",
    "flow rate": "flow_rate",
    "standpipe pressure": "standpipe_pressure",
    "formation pressure": "formation_pressure",
    "fracture gradient": "fracture_gradient",
    "casing shoe": "casing_shoe",
    "annulus": "annulus",
    "drilling ahead": "drilling_ahead",
    "tripping": "tripping",
    "logging": "logging",
    "well log": "logging",
    "drill ahead": "drilling_ahead",
    "drill ahead parameters": "drilling_parameters",
    "mud properties": "drilling_fluid_properties",
    "fluid loss": "fluid_loss",
    "lost circulation": "loss_circulation",
    "drill cuttings": "cuttings",
    "cuttings": "cuttings",
    "bit wear": "bit_wear",
    "drill collar": "drill_collar",
    "drill collars": "drill_collar",
    "bottom hole assembly": "bha",
    "bha": "bha",
    "well integrity": "well_integrity",
    "wellhead": "wellhead",
    "casing string": "casing",
    "cement job": "cementing",
    "cement slurry": "cementing",
    "mud cake": "mud_cake",
    "mud cakes": "mud_cake",
    "fluid properties": "drilling_fluid_properties",
    "drilling mud": "drilling_fluid",
    "mud system": "mud_system",
    "drilling system": "drilling_system",
    "hydraulic horsepower": "hydraulic_horsepower",
    "hydraulic power": "hydraulic_horsepower",
    "kick tolerance": "kick_tolerance",
    "well kick": "kick",
    "gas influx": "gas_kick",
    "pressure loss": "pressure_loss",
    "pressure drop": "pressure_loss",
    "annular pressure": "annular_pressure",
    "formation damage": "formation_damage",
    "mud gas": "mud_gas",
    "mud logging": "mud_logging",
    "drilling optimization": "drilling_optimization",
    "drilling efficiency": "drilling_efficiency",
    "drilling performance": "drilling_performance",
    "drilling parameters optimization": "drilling_parameters_optimization",
    "well trajectory": "well_trajectory",
    "directional drilling": "directional_drilling",
    "horizontal drilling": "horizontal_drilling",
    "vertical drilling": "vertical_drilling",
    "deviation": "well_deviation",
    "dogleg severity": "dogleg_severity",
    "well path": "well_path",
    "logging while drilling": "lwd",
    "lwd": "lwd",
    "measurement while drilling": "mwd",
    "mwd": "mwd",
    "drilling data": "drilling_data",
    "real-time data": "real_time_data",
    "drilling report": "drilling_report",
    "drilling audit": "drilling_audit",
    "drilling plan": "drilling_plan",
    "drilling schedule": "drilling_schedule",
    "drilling risk": "drilling_risk",
    "well control event": "well_control_event",
    "blowout": "blowout",
    "kick detection": "kick_detection",
    "mud losses": "loss_circulation",
    "mud gain": "mud_gain",
    "wellbore stability": "wellbore_stability",
    "formation evaluation": "formation_evaluation",
    "pressure monitoring": "pressure_monitoring",
    "temperature monitoring": "temperature_monitoring",
    "drilling hazards": "drilling_hazards",
    "drilling incident": "drilling_incident",
    "drilling safety": "drilling_safety",
    "drilling environment": "drilling_environment",
    "drilling contractor": "drilling_contractor",
    "rig crew": "rig_crew",
    "drilling superintendent": "drilling_superintendent",
    "mud engineer": "mud_engineer",
    "drilling engineer": "drilling_engineer",
    "wellsite geologist": "wellsite_geologist",
    "drilling supervisor": "drilling_supervisor",
    "drilling manager": "drilling_manager",
}

def normalize_query(text: str) -> str:
    """
    Normalize domain-specific terms in the query text to standardized terms.
    """
    lowered = text.lower()
    for term, normalized in DOMAIN_TERM_MAPPINGS.items():
        pattern = r'\b' + re.escape(term) + r'\b'
        lowered = re.sub(pattern, normalized, lowered)
    # Remove extra spaces
    lowered = re.sub(r'\s{2,}', ' ', lowered)
    return lowered.strip()

# ------------------------------
# DEEP ANALYSIS
# ------------------------------

def multi_doctrine_decomposition(query: str) -> List[str]:
    """
    Decompose query into sub-issues based on doctrine keywords.
    """
    # For demonstration, split by known doctrine keywords
    doctrine_keywords = [
        "well control", "kick detection", "mud weight", "pressure monitoring",
        "drilling optimization", "loss circulation", "wellbore stability",
        "formation evaluation", "drilling safety", "drilling performance",
        "cementing", "casing", "logging", "directional drilling"
    ]
    sub_issues = []
    lowered = query.lower()
    for keyword in doctrine_keywords:
        if keyword in lowered:
            sub_issues.append(keyword)
    if not sub_issues:
        # fallback: split by sentences or clauses
        sub_issues = re.split(r'[.;]', query)
        sub_issues = [s.strip() for s in sub_issues if s.strip()]
    return sub_issues

def build_interaction_dag(issues: List[str]) -> nx.DiGraph:
    """
    Build a dependency graph (DAG) of issues.
    For demonstration, create edges based on heuristic dependencies.
    """
    dag = nx.DiGraph()
    for issue in issues:
        dag.add_node(issue)

    # Heuristic dependencies
    dependencies = {
        "kick detection": ["well control"],
        "mud weight": ["kick detection"],
        "pressure monitoring": ["mud weight"],
        "loss circulation": ["wellbore stability"],
        "cementing": ["casing"],
        "logging": ["formation evaluation"],
        "directional drilling": ["wellbore stability"],
        "drilling optimization": ["drilling performance"],
        "drilling safety": ["well control", "kick detection"],
    }

    for issue in issues:
        deps = dependencies.get(issue, [])
        for dep in deps:
            if dep in issues:
                dag.add_edge(dep, issue)

    return dag

def eight_step_resolution(query: str, doctrines: List[str], sub_engine_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform full analysis in eight steps:
    1. Normalize query
    2. Decompose into sub-issues
    3. Build interaction DAG
    4. Gather sub-engine results
    5. Merge results
    6. Resolve conflicts
    7. Apply epistemic guardrails
    8. Tag analysis zones
    """
    # Step 1: Normalize
    normalized_query = normalize_query(query)

    # Step 2: Decompose
    issues = multi_doctrine_decomposition(normalized_query)

    # Step 3: Build DAG
    dag = build_interaction_dag(issues)

    # Step 4: Gather sub-engine results (already provided as sub_engine_results)

    # Step 5: Merge results
    merged_results = {}
    for issue in issues:
        res = sub_engine_results.get(issue, {})
        merged_results[issue] = res

    # Step 6: Resolve conflicts - simplistic approach: prefer higher authority source
    for issue, res in merged_results.items():
        if isinstance(res, dict) and "authority_sources" in res:
            dominant = resolve_authority_conflict(res["authority_sources"])
            res["dominant_authority"] = dominant.name

    # Step 7: Apply epistemic guardrails on textual analysis fields
    for issue, res in merged_results.items():
        if isinstance(res, dict) and "analysis_text" in res:
            cleaned_text, confidence = apply_epistemic_guardrails(res["analysis_text"])
            res["cleaned_analysis_text"] = cleaned_text
            res["confidence_level"] = confidence

    # Step 8: Zoned analysis tagging
    final_analysis = {}
    for issue, res in merged_results.items():
        tagged = zoned_analysis(res)
        final_analysis[issue] = tagged

    return {
        "normalized_query": normalized_query,
        "issues": issues,
        "interaction_dag": dag,
        "merged_results": merged_results,
        "final_analysis": final_analysis,
    }

def zoned_analysis(conclusion: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tag conclusion with zones: PLANNING, REPORTING, AUDIT based on content.
    """
    text = conclusion.get("cleaned_analysis_text", "").lower()
    tags = set()
    if any(word in text for word in ["plan", "planning", "strategy", "prepare", "forecast"]):
        tags.add("PLANNING")
    if any(word in text for word in ["report", "record", "document", "log", "summary"]):
        tags.add("REPORTING")
    if any(word in text for word in ["audit", "review", "compliance", "inspection", "verification"]):
        tags.add("AUDIT")
    if not tags:
        tags.add("REPORTING")  # default tag
    conclusion["zones"] = list(tags)
    return conclusion

# ------------------------------
# THREE LAYER RESPONSE SYSTEM
# ------------------------------

class DoctrineCache:
    """
    Simple in-memory doctrine cache with keyword matching.
    """
    def __init__(self):
        self.cache = {}  # keyword -> cached analysis

    def add(self, keyword: str, analysis: Dict[str, Any]):
        self.cache[keyword.lower()] = analysis

    def lookup(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Return cached analysis if any keyword matches in query.
        """
        lowered = query.lower()
        for keyword, analysis in self.cache.items():
            if keyword in lowered:
                return analysis
        return None

class SubEngineRouter:
    """
    Routes queries to sub-engines based on semantic search.
    """
    def __init__(self, sub_engines: Dict[str, Any]):
        self.sub_engines = sub_engines  # name -> callable

    def semantic_search(self, query: str) -> List[str]:
        """
        Return list of sub-engines relevant to query.
        For demo: match keywords to sub-engine keys.
        """
        lowered = query.lower()
        relevant = []
        for name in self.sub_engines.keys():
            if name.lower() in lowered:
                relevant.append(name)
        if not relevant:
            # fallback: return all
            relevant = list(self.sub_engines.keys())
        return relevant

    def dispatch(self, query: str) -> Dict[str, Any]:
        """
        Dispatch query to relevant sub-engines and collect results.
        """
        relevant_engines = self.semantic_search(query)
        results = {}
        for engine_name in relevant_engines:
            engine = self.sub_engines[engine_name]
            try:
                res = engine(query)
                results[engine_name] = res
            except Exception as e:
                results[engine_name] = {"error": str(e)}
        return results

class DeepMultiEngineAnalyzer:
    """
    Runs multiple sub-engines in parallel, merges and resolves conflicts.
    """
    def __init__(self, sub_engines: Dict[str, Any]):
        self.sub_engines = sub_engines

    def analyze(self, query: str) -> Dict[str, Any]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.sub_engines)) as executor:
            futures = {executor.submit(engine, query): name for name, engine in self.sub_engines.items()}
            results = {}
            for future in concurrent.futures.as_completed(futures):
                name = futures[future]
                try:
                    res = future.result()
                    results[name] = res
                except Exception as e:
                    results[name] = {"error": str(e)}

        # Merge results with simplistic conflict resolution
        merged = self.merge_results(results)
        return merged

    def merge_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge results from multiple sub-engines.
        For demonstration, combine textual analyses and resolve authority conflicts.
        """
        combined_texts = []
        all_authority_sources = []
        for res in results.values():
            if isinstance(res, dict):
                text = res.get("analysis_text", "")
                combined_texts.append(text)
                sources = res.get("authority_sources", [])
                all_authority_sources.extend(sources)
        merged_text = "\n".join(filter(None, combined_texts))
        dominant_authority = None
        if all_authority_sources:
            dominant_authority = resolve_authority_conflict(all_authority_sources)
        return {
            "merged_analysis_text": merged_text,
            "dominant_authority": dominant_authority.name if dominant_authority else None,
            "individual_results": results,
        }

class ThreeLayerResponseSystem:
    def __init__(self, doctrine_cache: DoctrineCache, sub_engines: Dict[str, Any]):
        self.doctrine_cache = doctrine_cache
        self.sub_engine_router = SubEngineRouter(sub_engines)
        self.deep_analyzer = DeepMultiEngineAnalyzer(sub_engines)

    def respond(self, query: str) -> Dict[str, Any]:
        # Layer 1: Doctrine cache lookup (0-200ms)
        start_time = time.time()
        cache_result = self.doctrine_cache.lookup(query)
        elapsed = (time.time() - start_time) * 1000
        if cache_result and elapsed <= 200:
            return {"layer": 1, "result": cache_result}

        # Layer 2: Semantic search + sub-engine routing
        sub_engine_results = self.sub_engine_router.dispatch(query)
        if sub_engine_results:
            return {"layer": 2, "result": sub_engine_results}

        # Layer 3: Deep multi-engine analysis
        deep_result = self.deep_analyzer.analyze(query)
        return {"layer": 3, "result": deep_result}

# ------------------------------
# EXAMPLE SUB-ENGINES (STUBS)
# ------------------------------

def sub_engine_well_control(query: str) -> Dict[str, Any]:
    # Stub analysis for well control
    analysis_text = ("The well control procedures must be strictly followed to prevent kicks. "
                     "Mud weight should be maintained above formation pressure.")
    authority_sources = [AuthorityLevel.STATUTORY, AuthorityLevel.CASE_LAW]
    return {"analysis_text": analysis_text, "authority_sources": authority_sources}

def sub_engine_drilling_parameters(query: str) -> Dict[str, Any]:
    analysis_text = ("Drilling parameters such as rate of penetration and torque are within expected ranges. "
                     "Monitoring should continue to optimize performance.")
    authority_sources = [AuthorityLevel.PRACTICE]
    return {"analysis_text": analysis_text, "authority_sources": authority_sources}

def sub_engine_cementing(query: str) -> Dict[str, Any]:
    analysis_text = ("The cement job quality is critical to well integrity. "
                     "Proper slurry design and placement must be verified.")
    authority_sources = [AuthorityLevel.TREATISE]
    return {"analysis_text": analysis_text, "authority_sources": authority_sources}

# ------------------------------
# SETUP AND INSTANTIATION
# ------------------------------

doctrine_cache = DoctrineCache()
doctrine_cache.add("kick detection", {
    "analysis_text": "Cached analysis on kick detection procedures and best practices.",
    "authority_sources": [AuthorityLevel.STATUTORY]
})
doctrine_cache.add("cementing", {
    "analysis_text": "Cached cementing guidelines from recognized treatises.",
    "authority_sources": [AuthorityLevel.TREATISE]
})

sub_engines = {
    "well control": sub_engine_well_control,
    "drilling parameters": sub_engine_drilling_parameters,
    "cementing": sub_engine_cementing,
}

three_layer_system = ThreeLayerResponseSystem(doctrine_cache, sub_engines)

# ------------------------------
# END OF PART 4
# ------------------------------

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
        self.queries: List[QueryTelemetry] = []
        self.errors: List[QueryTelemetry] = []
        self.latencies: List[float] = []
        self.cache_hits: int = 0
        self.total_queries: int = 0
        self.doctrine_hits: Counter = Counter()
        self.doctrine_total: Counter = Counter()
        self.sub_engine_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'latencies': [],
            'errors': 0,
            'invocations': 0
        })
        self.queries_by_time: deque = deque()  # (timestamp, QueryTelemetry)

    def record_query(self, telemetry: QueryTelemetry):
        with self.lock:
            self.queries.append(telemetry)
            self.latencies.append(telemetry.latency_ms)
            self.total_queries += 1
            if telemetry.cache_hit:
                self.cache_hits += 1
            for engine in telemetry.engines_invoked:
                self.sub_engine_stats[engine]['latencies'].append(telemetry.latency_ms)
                self.sub_engine_stats[engine]['invocations'] += 1
            self.queries_by_time.append((telemetry.timestamp, telemetry))
            # Doctrine hit tracking
            for engine in telemetry.engines_invoked:
                self.doctrine_hits[engine] += 1
            for engine in telemetry.engines_invoked:
                self.doctrine_total[engine] += 1

    def record_error(self, telemetry: QueryTelemetry):
        with self.lock:
            self.errors.append(telemetry)
            for engine in telemetry.engines_invoked:
                self.sub_engine_stats[engine]['errors'] += 1

    def get_latency_stats(self):
        with self.lock:
            if not self.latencies:
                return {
                    'avg': None, 'p50': None, 'p95': None, 'p99': None, 'min': None, 'max': None
                }
            lats = sorted(self.latencies)
            avg = statistics.mean(lats)
            p50 = lats[int(len(lats)*0.5)]
            p95 = lats[int(len(lats)*0.95)-1]
            p99 = lats[int(len(lats)*0.99)-1]
            return {
                'avg': avg,
                'p50': p50,
                'p95': p95,
                'p99': p99,
                'min': lats[0],
                'max': lats[-1]
            }

    def get_doctrine_hit_rate(self, doctrine: str):
        with self.lock:
            total = self.doctrine_total[doctrine]
            hits = self.doctrine_hits[doctrine]
            if total == 0:
                return None
            return hits / total

    def queries_last_hour(self):
        now = time.time()
        one_hour_ago = now - 3600
        with self.lock:
            while self.queries_by_time and self.queries_by_time[0][0] < one_hour_ago:
                self.queries_by_time.popleft()
            return [qt for ts, qt in self.queries_by_time]

    def get_sub_engine_stats(self):
        with self.lock:
            stats = {}
            for engine, data in self.sub_engine_stats.items():
                lats = data['latencies']
                stats[engine] = {
                    'avg_latency': statistics.mean(lats) if lats else None,
                    'p95_latency': sorted(lats)[int(len(lats)*0.95)-1] if lats else None,
                    'errors': data['errors'],
                    'invocations': data['invocations'],
                    'error_rate': (data['errors']/data['invocations']) if data['invocations'] else None
                }
            return stats

# --- DRIFT DETECTION ---

class DriftWatcher:
    def __init__(self):
        self.lock = threading.Lock()
        self.baselines: Dict[str, float] = {}  # doctrine -> baseline confidence
        self.history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))  # doctrine -> deque of (timestamp, confidence)
        self.alerts: List[Dict[str, Any]] = []

    def record_baseline(self, doctrine: str, confidence: float):
        with self.lock:
            self.baselines[doctrine] = confidence

    def record_confidence(self, doctrine: str, confidence: float, timestamp: Optional[float] = None):
        if timestamp is None:
            timestamp = time.time()
        with self.lock:
            self.history[doctrine].append((timestamp, confidence))

    def detect_drift(self, doctrine: str, window: int = 100):
        with self.lock:
            if doctrine not in self.baselines or len(self.history[doctrine]) < window:
                return None
            recent = [c for t, c in list(self.history[doctrine])[-window:]]
            avg_recent = statistics.mean(recent)
            baseline = self.baselines[doctrine]
            if baseline == 0:
                return None
            drift = (avg_recent - baseline) / baseline
            if abs(drift) > 0.10:
                alert = {
                    'doctrine': doctrine,
                    'timestamp': time.time(),
                    'baseline': baseline,
                    'avg_recent': avg_recent,
                    'drift': drift
                }
                self.alerts.append(alert)
                return alert
            return None

    def get_drift_report(self):
        with self.lock:
            report = []
            for doctrine in self.baselines:
                drift = self.detect_drift(doctrine)
                if drift:
                    report.append(drift)
            return report

# --- COVERAGE MAPPING ---

class CoverageTracker:
    def __init__(self):
        self.lock = threading.Lock()
        self.triggered: Counter = Counter()  # doctrine -> count
        self.missed: List[Tuple[str, float]] = []  # (query_id, timestamp)
        self.epistemic_gap: List[Tuple[str, float, Any]] = []  # (query_id, timestamp, query)
        self.sub_engine_coverage: Dict[str, Dict[str, int]] = defaultdict(lambda: {'triggered': 0, 'missed': 0})

    def record_triggered(self, doctrine: str, sub_engine: str):
        with self.lock:
            self.triggered[doctrine] += 1
            self.sub_engine_coverage[sub_engine]['triggered'] += 1

    def record_missed(self, query_id: str, timestamp: float, query: Any, sub_engine: Optional[str] = None):
        with self.lock:
            self.missed.append((query_id, timestamp))
            if sub_engine:
                self.sub_engine_coverage[sub_engine]['missed'] += 1
            # Epistemic gap detection: if no doctrine matches
            self.epistemic_gap.append((query_id, timestamp, query))

    def get_coverage_report(self):
        with self.lock:
            total = sum(self.triggered.values()) + len(self.missed)
            doctrine_coverage = {d: self.triggered[d] for d in self.triggered}
            epistemic_gap_count = len(self.epistemic_gap)
            per_sub_engine = {
                se: {
                    'triggered': data['triggered'],
                    'missed': data['missed'],
                    'coverage': data['triggered'] / (data['triggered'] + data['missed']) if (data['triggered'] + data['missed']) > 0 else None
                }
                for se, data in self.sub_engine_coverage.items()
            }
            return {
                'total_queries': total,
                'doctrine_coverage': doctrine_coverage,
                'epistemic_gap_count': epistemic_gap_count,
                'epistemic_gap_examples': self.epistemic_gap[:10],
                'per_sub_engine': per_sub_engine
            }

# --- DETERMINISM HASHING ---

def compute_determinism_hash(query: Any, response: Any) -> str:
    # Canonicalize to JSON, sort keys for determinism
    query_json = json.dumps(query, sort_keys=True, separators=(',', ':'))
    response_json = json.dumps(response, sort_keys=True, separators=(',', ':'))
    combined = query_json + '|' + response_json
    return hashlib.sha256(combined.encode('utf-8')).hexdigest()

def verify_reproducibility(query: Any, response: Any, expected_hash: str) -> bool:
    hash_val = compute_determinism_hash(query, response)
    return hash_val == expected_hash

# --- AUDIT TRAIL ---

class AuditTrailWriter:
    def __init__(self, audit_dir: str):
        self.audit_dir = audit_dir
        os.makedirs(audit_dir, exist_ok=True)
        self.current_date = self._get_today()
        self.file = self._open_file(self.current_date)
        self.lock = threading.Lock()

    def _get_today(self):
        return datetime.datetime.utcnow().strftime('%Y-%m-%d')

    def _open_file(self, date_str: str):
        path = os.path.join(self.audit_dir, f'audit_{date_str}.jsonl')
        return open(path, 'a', encoding='utf-8')

    def _rotate_if_needed(self):
        today = self._get_today()
        if today != self.current_date:
            self.file.close()
            self.current_date = today
            self.file = self._open_file(today)

    def write(self, query_id: str, timestamp: float, engine_id: str, engines_invoked: List[str],
              mode: str, confidence: float, latency: float, cache_hit: bool):
        self._rotate_if_needed()
        entry = {
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
            self.file.write(json.dumps(entry) + '\n')
            self.file.flush()

    def forensic_replay(self, date: str) -> List[Dict[str, Any]]:
        path = os.path.join(self.audit_dir, f'audit_{date}.jsonl')
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return [json.loads(line) for line in f]

    def close(self):
        with self.lock:
            self.file.close()

# --- PERFORMANCE PROFILER ---

class PerformanceProfiler:
    def __init__(self):
        self.lock = threading.Lock()
        self.sub_engine_latency: Dict[str, List[float]] = defaultdict(list)
        self.sub_engine_errors: Dict[str, int] = defaultdict(int)
        self.sub_engine_invocations: Dict[str, int] = defaultdict(int)
        self.sub_engine_availability: Dict[str, List[Tuple[float, bool]]] = defaultdict(list)  # (timestamp, available)
        self.sla_thresholds: Dict[str, Dict[str, float]] = {}  # sub_engine -> {'latency_ms': 200, 'error_rate': 0.01, ...}
        self.sla_violations: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def record_invocation(self, sub_engine: str, latency_ms: float, error: Optional[str] = None, available: bool = True):
        with self.lock:
            self.sub_engine_latency[sub_engine].append(latency_ms)
            self.sub_engine_invocations[sub_engine] += 1
            if error:
                self.sub_engine_errors[sub_engine] += 1
            self.sub_engine_availability[sub_engine].append((time.time(), available))

    def set_sla(self, sub_engine: str, latency_ms: float, error_rate: float, availability: float):
        with self.lock:
            self.sla_thresholds[sub_engine] = {
                'latency_ms': latency_ms,
                'error_rate': error_rate,
                'availability': availability
            }

    def check_sla(self, sub_engine: str, window: int = 100):
        with self.lock:
            if sub_engine not in self.sla_thresholds:
                return None
            latencies = self.sub_engine_latency[sub_engine][-window:]
            errors = self.sub_engine_errors[sub_engine]
            invocations = self.sub_engine_invocations[sub_engine]
            avail_records = self.sub_engine_availability[sub_engine][-window:]
            if not latencies or not avail_records or invocations == 0:
                return None
            avg_latency = statistics.mean(latencies)
            error_rate = errors / invocations
            availability = sum(1 for t, avail in avail_records if avail) / len(avail_records)
            sla = self.sla_thresholds[sub_engine]
            violations = {}
            if avg_latency > sla['latency_ms']:
                violations['latency'] = avg_latency
            if error_rate > sla['error_rate']:
                violations['error_rate'] = error_rate
            if availability < sla['availability']:
                violations['availability'] = availability
            if violations:
                violation_record = {
                    'timestamp': time.time(),
                    'violations': violations,
                    'window': window
                }
                self.sla_violations[sub_engine].append(violation_record)
                return violation_record
            return None

    def get_sla_violations(self, sub_engine: str) -> List[Dict[str, Any]]:
        with self.lock:
            return list(self.sla_violations[sub_engine])

    def get_sub_engine_performance(self, sub_engine: str, window: int = 100):
        with self.lock:
            latencies = self.sub_engine_latency[sub_engine][-window:]
            errors = self.sub_engine_errors[sub_engine]
            invocations = self.sub_engine_invocations[sub_engine]
            avail_records = self.sub_engine_availability[sub_engine][-window:]
            if not latencies or not avail_records or invocations == 0:
                return None
            avg_latency = statistics.mean(latencies)
            error_rate = errors / invocations
            availability = sum(1 for t, avail in avail_records if avail) / len(avail_records)
            return {
                'avg_latency': avg_latency,
                'error_rate': error_rate,
                'availability': availability,
                'invocations': invocations
            }

    def get_all_sub_engine_performance(self, window: int = 100):
        with self.lock:
            perf = {}
            for se in self.sub_engine_latency.keys():
                perf[se] = self.get_sub_engine_performance(se, window=window)
            return perf

# --- Example Integration ---

class DrillingIntelligenceOrchestrator:
    def __init__(self, audit_dir: str):
        self.telemetry = TelemetryCollector()
        self.drift = DriftWatcher()
        self.coverage = CoverageTracker()
        self.audit = AuditTrailWriter(audit_dir)
        self.profiler = PerformanceProfiler()

    def process_query(self, query_id: str, query: Any, engines: List[str], mode: str, response: Any,
                      confidence: float, latency_ms: float, cache_hit: bool, error: Optional[str] = None):
        timestamp = time.time()
        # Telemetry
        telemetry = QueryTelemetry(
            query_id=query_id,
            timestamp=timestamp,
            latency_ms=latency_ms,
            cache_hit=cache_hit,
            engines_invoked=engines,
            mode=mode,
            confidence=confidence,
            error=error
        )
        self.telemetry.record_query(telemetry)
        if error:
            self.telemetry.record_error(telemetry)
        # Drift
        for doctrine in engines:
            self.drift.record_confidence(doctrine, confidence, timestamp)
            drift_alert = self.drift.detect_drift(doctrine)
            if drift_alert:
                # Handle drift alert (e.g., log, notify, etc.)
                pass
        # Coverage
        if engines:
            for doctrine in engines:
                self.coverage.record_triggered(doctrine, doctrine)
        else:
            self.coverage.record_missed(query_id, timestamp, query)
        # Determinism hash
        det_hash = compute_determinism_hash(query, response)
        # Audit
        self.audit.write(
            query_id=query_id,
            timestamp=timestamp,
            engine_id=engines[0] if engines else 'none',
            engines_invoked=engines,
            mode=mode,
            confidence=confidence,
            latency=latency_ms,
            cache_hit=cache_hit
        )
        # Profiler
        for engine in engines:
            self.profiler.record_invocation(
                sub_engine=engine,
                latency_ms=latency_ms,
                error=error,
                available=(error is None)
            )
        return det_hash

    def close(self):
        self.audit.close()

ENGINE_ID = "DRLIE"
ENGINE_PORT = 8851
SUB_ENGINES = {
    "DRL01": "Wellbore Design",
    "DRL02": "Drilling Fluid Engineering",
    "DRL03": "Directional Drilling",
    "DRL04": "Cementing Operations",
    "DRL05": "Casing Design",
    "DRL06": "Bit Selection",
    "DRL07": "Drilling Optimization",
    "DRL08": "Well Control",
    "DRL09": "Hole Problems",
    "DRL10": "Completion Design",
    "DRL11": "Rig Selection",
    "DRL12": "Formation Evaluation",
    "DRL13": "Torque and Drag",
    "DRL14": "Hydraulics",
    "DRL15": "Drilling Safety",
}

# Logger setup
logger = logging.getLogger("drilling_intelligence_engine")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)
logger.addHandler(ch)

# Data models
class QueryRequest(BaseModel):
    query: str
    parameters: Optional[Dict[str, Any]] = None

class RouteDryRunRequest(BaseModel):
    query: str

class AnalyzeRequest(BaseModel):
    query: str
    depth: Optional[int] = 3
    parameters: Optional[Dict[str, Any]] = None

class SubEngineResponse(BaseModel):
    engine_id: str
    success: bool
    response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    latency_ms: Optional[int] = None

class HealthStatus(BaseModel):
    engine_id: str
    status: str
    details: Optional[Dict[str, Any]] = None

class MetricsResponse(BaseModel):
    latency_stats: Dict[str, Any]
    cache_hit_rate: float
    queries_per_hour: float
    sub_engine_stats: Dict[str, Any]

class CoverageReport(BaseModel):
    doctrine_coverage: Dict[str, float]
    epistemic_gaps: List[str]

class DriftReport(BaseModel):
    drift_detected: bool
    details: Dict[str, Any]

class DoctrineInfo(BaseModel):
    doctrine_id: str
    domain: str
    last_updated: datetime

class RoutingRule(BaseModel):
    domain: str
    engines: List[str]

class RoutingInfo(BaseModel):
    routing_rules: List[RoutingRule]
    engine_registry: Dict[str, str]

class SubEngineHealthDashboard(BaseModel):
    sub_engines: List[HealthStatus]

# Globals for the engine state
class EngineState:
    def __init__(self):
        self.doctrine_cache: Dict[str, Dict[str, Any]] = {}
        self.search_index: Dict[str, List[str]] = {}
        self.telemetry_enabled: bool = False
        self.health_monitor_task: Optional[asyncio.Task] = None
        self.telemetry_task: Optional[asyncio.Task] = None
        self.latency_records: List[float] = []
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.query_timestamps: List[float] = []
        self.sub_engine_health: Dict[str, HealthStatus] = {}
        self.routing_rules: List[RoutingRule] = []
        self.circuit_breakers: Dict[str, bool] = {}
        self.lock = threading.Lock()
        self.last_drift_report: Optional[DriftReport] = None

    def record_latency(self, latency_ms: float):
        with self.lock:
            self.latency_records.append(latency_ms)
            # Keep only last 1000 records for stats
            if len(self.latency_records) > 1000:
                self.latency_records.pop(0)

    def record_cache_hit(self):
        with self.lock:
            self.cache_hits += 1

    def record_cache_miss(self):
        with self.lock:
            self.cache_misses += 1

    def record_query_timestamp(self, timestamp: float):
        with self.lock:
            self.query_timestamps.append(timestamp)
            # Keep only last 24 hours of timestamps
            cutoff = timestamp - 86400
            while self.query_timestamps and self.query_timestamps[0] < cutoff:
                self.query_timestamps.pop(0)

engine_state = EngineState()

# Helper functions for doctrine cache, search index, telemetry, health monitor, etc.

async def initialize_doctrine_cache():
    logger.info("Initializing doctrine cache...")
    # Simulate loading doctrines from persistent storage or remote source
    await asyncio.sleep(0.5)
    doctrines = {
        "doctrine_001": {
            "doctrine_id": "doctrine_001",
            "domain": "Wellbore Design",
            "content": "Guidelines for wellbore trajectory planning and casing points.",
            "last_updated": datetime.utcnow(),
        },
        "doctrine_002": {
            "doctrine_id": "doctrine_002",
            "domain": "Drilling Fluid Engineering",
            "content": "Best practices for mud properties and additives.",
            "last_updated": datetime.utcnow(),
        },
        # ... more doctrines ...
    }
    engine_state.doctrine_cache = doctrines
    logger.info(f"Loaded {len(doctrines)} doctrines into cache.")

async def seed_search_index():
    logger.info("Seeding search index...")
    # Build a simple inverted index from doctrines
    index = {}
    for doctrine_id, doctrine in engine_state.doctrine_cache.items():
        words = doctrine["content"].lower().split()
        for word in words:
            if word not in index:
                index[word] = []
            if doctrine_id not in index[word]:
                index[word].append(doctrine_id)
    engine_state.search_index = index
    logger.info(f"Search index seeded with {len(index)} unique terms.")

async def start_telemetry():
    logger.info("Starting telemetry subsystem...")
    engine_state.telemetry_enabled = True
    # Telemetry could be sending metrics periodically to external system
    async def telemetry_loop():
        while engine_state.telemetry_enabled:
            logger.debug("Telemetry heartbeat...")
            await asyncio.sleep(60)
    engine_state.telemetry_task = asyncio.create_task(telemetry_loop())

async def stop_telemetry():
    logger.info("Stopping telemetry subsystem...")
    engine_state.telemetry_enabled = False
    if engine_state.telemetry_task:
        engine_state.telemetry_task.cancel()
        try:
            await engine_state.telemetry_task
        except asyncio.CancelledError:
            pass
        engine_state.telemetry_task = None

async def health_monitor():
    logger.info("Starting health monitor...")
    while True:
        # Simulate health checks for sub-engines
        for engine_id in SUB_ENGINES.keys():
            # Randomly simulate health status for demo
            status = random.choice(["healthy", "degraded", "unhealthy"])
            details = {
                "last_checked": datetime.utcnow().isoformat(),
                "response_time_ms": random.randint(10, 200),
                "error_rate": round(random.uniform(0, 0.05), 4),
            }
            health_status = HealthStatus(
                engine_id=engine_id,
                status=status,
                details=details,
            )
            engine_state.sub_engine_health[engine_id] = health_status
        await asyncio.sleep(30)

async def start_health_monitor():
    if engine_state.health_monitor_task is None:
        engine_state.health_monitor_task = asyncio.create_task(health_monitor())

async def stop_health_monitor():
    if engine_state.health_monitor_task:
        engine_state.health_monitor_task.cancel()
        try:
            await engine_state.health_monitor_task
        except asyncio.CancelledError:
            pass
        engine_state.health_monitor_task = None

# Query processing pipeline components

def normalize_query(query: str) -> str:
    normalized = query.strip().lower()
    logger.debug(f"Normalized query: '{normalized}'")
    return normalized

def classify_domain(query: str) -> str:
    # Simple keyword-based classification for demo
    keywords_map = {
        "wellbore": "DRL01",
        "mud": "DRL02",
        "directional": "DRL03",
        "cement": "DRL04",
        "casing": "DRL05",
        "bit": "DRL06",
        "optimize": "DRL07",
        "control": "DRL08",
        "hole": "DRL09",
        "completion": "DRL10",
        "rig": "DRL11",
        "formation": "DRL12",
        "torque": "DRL13",
        "hydraulic": "DRL14",
        "safety": "DRL15",
    }
    for keyword, engine_id in keywords_map.items():
        if keyword in query:
            logger.debug(f"Classified domain '{engine_id}' for keyword '{keyword}'")
            return engine_id
    logger.debug("Default classification to DRL07 (Drilling Optimization)")
    return "DRL07"

def route_query(domain_engine_id: str) -> List[str]:
    # Routing rules: for demo, route to the classified engine plus DRL07 (optimization)
    routing = [domain_engine_id]
    if domain_engine_id != "DRL07":
        routing.append("DRL07")
    logger.debug(f"Routing query to engines: {routing}")
    return routing

async def dispatch_to_sub_engine(engine_id: str, query: str, parameters: Optional[Dict[str, Any]]) -> SubEngineResponse:
    start_time = time.perf_counter()
    try:
        # Simulate network call with random latency and possible failure
        latency = random.uniform(0.05, 0.3)
        await asyncio.sleep(latency)
        if random.random() < 0.05:  # 5% failure rate
            raise Exception("Simulated sub-engine failure")
        response = {
            "engine_id": engine_id,
            "answer": f"Response from {SUB_ENGINES[engine_id]} for query '{query[:50]}'",
            "parameters_used": parameters or {},
        }
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        logger.debug(f"Sub-engine {engine_id} responded in {latency_ms} ms")
        return SubEngineResponse(
            engine_id=engine_id,
            success=True,
            response=response,
            latency_ms=latency_ms,
        )
    except Exception as e:
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        logger.error(f"Sub-engine {engine_id} failed: {str(e)}")
        return SubEngineResponse(
            engine_id=engine_id,
            success=False,
            error=str(e),
            latency_ms=latency_ms,
        )

def merge_responses(responses: List[SubEngineResponse]) -> Dict[str, Any]:
    merged = {
        "responses": [],
        "summary": "",
    }
    answers = []
    for resp in responses:
        if resp.success and resp.response:
            merged["responses"].append(resp.response)
            answers.append(resp.response.get("answer", ""))
    merged["summary"] = " | ".join(answers)
    logger.debug(f"Merged response summary: {merged['summary']}")
    return merged

def apply_guardrails(merged_response: Dict[str, Any]) -> Dict[str, Any]:
    # For demo, redact any answer containing banned words
    banned_words = ["error", "fail", "unauthorized"]
    filtered_responses = []
    for resp in merged_response.get("responses", []):
        answer = resp.get("answer", "")
        if any(bw in answer.lower() for bw in banned_words):
            resp["answer"] = "[REDACTED]"
        filtered_responses.append(resp)
    merged_response["responses"] = filtered_responses
    return merged_response

def hash_response(response: Dict[str, Any]) -> str:
    serialized = json.dumps(response, sort_keys=True)
    h = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    logger.debug(f"Response hash: {h}")
    return h

def log_query(query: str, response_hash: str, latency_ms: int, routed_engines: List[str]):
    logger.info(f"Query logged: hash={response_hash}, latency={latency_ms}ms, engines={routed_engines}")

async def fallback_to_doctrine_cache(query: str) -> Dict[str, Any]:
    # Simple fallback: search doctrine cache for matching doctrines
    normalized = normalize_query(query)
    matched_doctrines = []
    for doctrine_id, doctrine in engine_state.doctrine_cache.items():
        if normalized in doctrine["content"].lower():
            matched_doctrines.append({
                "doctrine_id": doctrine_id,
                "domain": doctrine["domain"],
                "content": doctrine["content"],
            })
    logger.info(f"Fallback to doctrine cache found {len(matched_doctrines)} matches")
    return {"fallback_results": matched_doctrines}

# FastAPI app and lifespan management

app = FastAPI(title="Drilling Intelligence Engine - Domain Orchestrator", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Drilling Intelligence Engine Domain Orchestrator...")
    await initialize_doctrine_cache()
    await seed_search_index()
    await start_health_monitor()
    await start_telemetry()
    # Initialize routing rules for demo
    engine_state.routing_rules = [
        RoutingRule(domain="Wellbore Design", engines=["DRL01", "DRL07"]),
        RoutingRule(domain="Drilling Fluid Engineering", engines=["DRL02", "DRL07"]),
        RoutingRule(domain="Directional Drilling", engines=["DRL03", "DRL07"]),
        RoutingRule(domain="Cementing Operations", engines=["DRL04", "DRL07"]),
        RoutingRule(domain="Casing Design", engines=["DRL05", "DRL07"]),
        RoutingRule(domain="Bit Selection", engines=["DRL06", "DRL07"]),
        RoutingRule(domain="Drilling Optimization", engines=["DRL07"]),
        RoutingRule(domain="Well Control", engines=["DRL08", "DRL07"]),
        RoutingRule(domain="Hole Problems", engines=["DRL09", "DRL07"]),
        RoutingRule(domain="Completion Design", engines=["DRL10", "DRL07"]),
        RoutingRule(domain="Rig Selection", engines=["DRL11", "DRL07"]),
        RoutingRule(domain="Formation Evaluation", engines=["DRL12", "DRL07"]),
        RoutingRule(domain="Torque and Drag", engines=["DRL13", "DRL07"]),
        RoutingRule(domain="Hydraulics", engines=["DRL14", "DRL07"]),
        RoutingRule(domain="Drilling Safety", engines=["DRL15", "DRL07"]),
    ]
    logger.info("Startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Drilling Intelligence Engine Domain Orchestrator...")
    await stop_health_monitor()
    await stop_telemetry()
    logger.info("Shutdown complete.")

# Endpoint implementations

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    start_time = time.perf_counter()
    normalized_query = normalize_query(request.query)
    domain_engine_id = classify_domain(normalized_query)
    routed_engines = route_query(domain_engine_id)

    # Circuit breaker check
    for engine_id in routed_engines:
        if engine_state.circuit_breakers.get(engine_id, False):
            logger.warning(f"Circuit breaker open for {engine_id}, skipping dispatch.")
            routed_engines.remove(engine_id)

    # Dispatch concurrently
    dispatch_tasks = [
        dispatch_to_sub_engine(engine_id, normalized_query, request.parameters)
        for engine_id in routed_engines
    ]
    try:
        responses = await asyncio.wait_for(asyncio.gather(*dispatch_tasks), timeout=5.0)
    except asyncio.TimeoutError:
        logger.error("Timeout while waiting for sub-engine responses")
        responses = []
        # Mark all as failed due to timeout
        for engine_id in routed_engines:
            responses.append(SubEngineResponse(
                engine_id=engine_id,
                success=False,
                error="Timeout",
                latency_ms=None,
            ))

    # Check for failures and fallback if necessary
    if not any(resp.success for resp in responses):
        fallback_result = await fallback_to_doctrine_cache(normalized_query)
        engine_state.record_cache_miss()
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        response_hash = hash_response(fallback_result)
        log_query(normalized_query, response_hash, latency_ms, routed_engines)
        engine_state.record_query_timestamp(time.time())
        engine_state.record_latency(latency_ms)
        return JSONResponse(content={"fallback": fallback_result})

    engine_state.record_cache_hit()
    merged_response = merge_responses(responses)
    guarded_response = apply_guardrails(merged_response)
    latency_ms = int((time.perf_counter() - start_time) * 1000)
    response_hash = hash_response(guarded_response)
    log_query(normalized_query, response_hash, latency_ms, routed_engines)
    engine_state.record_query_timestamp(time.time())
    engine_state.record_latency(latency_ms)
    return JSONResponse(content=guarded_response)

@app.get("/health")
async def health_endpoint():
    # Self health
    self_health = HealthStatus(
        engine_id=ENGINE_ID,
        status="healthy",
        details={
            "uptime_seconds": int(time.time() - app.state.start_time),
            "doctrine_cache_size": len(engine_state.doctrine_cache),
            "search_index_terms": len(engine_state.search_index),
        },
    )
    # Sub-engine health
    sub_engine_health_list = list(engine_state.sub_engine_health.values())
    combined_status = "healthy"
    for h in sub_engine_health_list:
        if h.status == "unhealthy":
            combined_status = "unhealthy"
            break
        if h.status == "degraded" and combined_status != "unhealthy":
            combined_status = "degraded"
    overall_health = {
        "self": self_health.dict(),
        "sub_engines": [h.dict() for h in sub_engine_health_list],
        "overall_status": combined_status,
    }
    return JSONResponse(content=overall_health)

@app.get("/metrics")
async def metrics_endpoint():
    latencies = engine_state.latency_records
    if latencies:
        latency_stats = {
            "min_ms": min(latencies),
            "max_ms": max(latencies),
            "avg_ms": sum(latencies) / len(latencies),
            "p50_ms": sorted(latencies)[len(latencies)//2],
            "p90_ms": sorted(latencies)[int(len(latencies)*0.9)],
            "p99_ms": sorted(latencies)[int(len(latencies)*0.99) if len(latencies) > 100 else -1],
        }
    else:
        latency_stats = {}

    total_queries = engine_state.cache_hits + engine_state.cache_misses
    cache_hit_rate = (engine_state.cache_hits / total_queries) if total_queries > 0 else 0.0

    # Queries per hour calculation
    now = time.time()
    one_hour_ago = now - 3600
    queries_last_hour = len([t for t in engine_state.query_timestamps if t >= one_hour_ago])
    queries_per_hour = queries_last_hour

    # Sub-engine stats from health monitor
    sub_engine_stats = {}
    for engine_id, health in engine_state.sub_engine_health.items():
        sub_engine_stats[engine_id] = {
            "status": health.status,
            "last_checked": health.details.get("last_checked") if health.details else None,
            "response_time_ms": health.details.get("response_time_ms") if health.details else None,
            "error_rate": health.details.get("error_rate") if health.details else None,
        }

    metrics = MetricsResponse(
        latency_stats=latency_stats,
        cache_hit_rate=cache_hit_rate,
        queries_per_hour=queries_per_hour,
        sub_engine_stats=sub_engine_stats,
    )
    return JSONResponse(content=metrics.dict())

@app.get("/coverage")
async def coverage_endpoint():
    # For demo, doctrine coverage is percentage of doctrines per domain
    domain_counts = {}
    for doctrine in engine_state.doctrine_cache.values():
        domain = doctrine["domain"]
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
    total_doctrines = len(engine_state.doctrine_cache)
    doctrine_coverage = {}
    for domain, count in domain_counts.items():
        doctrine_coverage[domain] = round((count / total_doctrines) * 100, 2) if total_doctrines > 0 else 0.0

    # Epistemic gaps: domains with less than 2 doctrines
    epistemic_gaps = [domain for domain, count in domain_counts.items() if count < 2]

    coverage_report = CoverageReport(
        doctrine_coverage=doctrine_coverage,
        epistemic_gaps=epistemic_gaps,
    )
    return JSONResponse(content=coverage_report.dict())

@app.get("/drift")
async def drift_endpoint():
    # For demo, generate a random drift detection report
    drift_detected = random.choice([True, False])
    details = {
        "last_checked": datetime.utcnow().isoformat(),
        "drift_score": round(random.uniform(0, 1), 3),
        "affected_domains": random.sample(list(SUB_ENGINES.values()), k=random.randint(0,3)),
    }
    drift_report = DriftReport(
        drift_detected=drift_detected,
        details=details,
    )
    engine_state.last_drift_report = drift_report
    return JSONResponse(content=drift_report.dict())

@app.get("/doctrines")
async def doctrines_endpoint():
    doctrines_list = []
    for doctrine_id, doctrine in engine_state.doctrine_cache.items():
        doctrines_list.append(
            DoctrineInfo(
                doctrine_id=doctrine_id,
                domain=doctrine["domain"],
                last_updated=doctrine["last_updated"],
            ).dict()
        )
    return JSONResponse(content={"doctrines": doctrines_list})

@app.get("/routing")
async def routing_endpoint():
    routing_info = RoutingInfo(
        routing_rules=engine_state.routing_rules,
        engine_registry=SUB_ENGINES,
    )
    return JSONResponse(content=routing_info.dict())

@app.get("/sub-engines")
async def sub_engines_endpoint():
    dashboard = SubEngineHealthDashboard(
        sub_engines=list(engine_state.sub_engine_health.values())
    )
    return JSONResponse(content=dashboard.dict())

@app.post("/route")
async def route_dry_run_endpoint(request: RouteDryRunRequest):
    normalized_query = normalize_query(request.query)
    domain_engine_id = classify_domain(normalized_query)
    routed_engines = route_query(domain_engine_id)
    return JSONResponse(content={"routed_engines": routed_engines})

@app.post("/analyze")
async def analyze_endpoint(request: AnalyzeRequest):
    normalized_query = normalize_query(request.query)
    depth = request.depth if request.depth and request.depth > 0 else 3
    parameters = request.parameters or {}

    domain_engine_id = classify_domain(normalized_query)
    routed_engines = route_query(domain_engine_id)

    analysis_results = {}

    for engine_id in routed_engines:
        engine_analysis = []
        for level in range(depth):
            # Simulate deeper analysis with increasing detail
            detail = {
                "level": level + 1,
                "engine_id": engine_id,
                "analysis": f"Detailed analysis level {level + 1} from {SUB_ENGINES[engine_id]}",
                "parameters": parameters,
            }
            engine_analysis.append(detail)
            await asyncio.sleep(0.1)  # Simulate processing delay
        analysis_results[engine_id] = engine_analysis

    return JSONResponse(content={"analysis": analysis_results})

# Lifespan management with startup time tracking
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.state.start_time = time.time()

if __name__ == "__main__":
    uvicorn.run("drilling_intelligence_engine:app", host="0.0.0.0", port=ENGINE_PORT, log_level="info")