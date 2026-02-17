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

# ENGINE CONSTANTS
ENGINE_ID = "RAILIE"
ENGINE_PORT = 8860
ENGINE_NAME = "Railroad Intelligence Engine — Domain Orchestrator"
ENGINE_VERSION = "1.0.0"

# ENUMS

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
    TRACK_DEFECT = "TRACK_DEFECT"
    SIGNAL_FAILURE = "SIGNAL_FAILURE"
    LOCOMOTIVE_MALFUNCTION = "LOCOMOTIVE_MALFUNCTION"
    FREIGHT_DELAY = "FREIGHT_DELAY"
    SAFETY_INCIDENT = "SAFETY_INCIDENT"
    STRUCTURAL_DAMAGE = "STRUCTURAL_DAMAGE"
    ROLLING_STOCK_ISSUE = "ROLLING_STOCK_ISSUE"
    ELECTRIFICATION_FAULT = "ELECTRIFICATION_FAULT"
    TRAIN_CONTROL_ERROR = "TRAIN_CONTROL_ERROR"
    YARD_CONGESTION = "YARD_CONGESTION"
    PASSENGER_COMPLAINT = "PASSENGER_COMPLAINT"
    SCHEDULE_VARIANCE = "SCHEDULE_VARIANCE"
    WEATHER_IMPACT = "WEATHER_IMPACT"
    MAINTENANCE_OVERDUE = "MAINTENANCE_OVERDUE"
    CREW_SHORTAGE = "CREW_SHORTAGE"
    ENVIRONMENTAL_HAZARD = "ENVIRONMENTAL_HAZARD"
    SECURITY_BREACH = "SECURITY_BREACH"
    MATERIAL_SHORTAGE = "MATERIAL_SHORTAGE"
    EQUIPMENT_FAILURE = "EQUIPMENT_FAILURE"
    OPERATIONAL_BOTTLENECK = "OPERATIONAL_BOTTLENECK"
    CUSTOMER_SERVICE = "CUSTOMER_SERVICE"
    REGULATORY_COMPLIANCE = "REGULATORY_COMPLIANCE"
    INCIDENT_REPORT = "INCIDENT_REPORT"
    SYSTEM_UPGRADE = "SYSTEM_UPGRADE"
    DATA_INTEGRITY = "DATA_INTEGRITY"

class SubEngineStatus(enum.Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

# PYDANTIC MODELS

class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    user_id: str
    domain: str
    keywords: typing.List[str]
    response_mode: ResponseMode = ResponseMode.FAST
    position_zone: PositionZone = PositionZone.PLANNING
    confidence_zone: ConfidenceZone = ConfidenceZone.DEFENSIBLE
    issue_category: IssueCategory
    additional_context: typing.Optional[dict] = None

    @validator('keywords', pre=True)
    def ensure_keywords(cls, v):
        if not v or not isinstance(v, list):
            raise ValueError("keywords must be a non-empty list")
        return v

class QueryResponse(BaseModel):
    query_id: str
    engine_id: str
    sub_engine_id: str
    status: str
    result: typing.Any
    confidence: float
    latency_ms: float
    routing_decision: typing.Optional[str] = None
    orchestration_result: typing.Optional[dict] = None
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

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
    selected_engine_id: str
    reason: str
    matched_keywords: typing.List[str]
    confidence: float
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decision: RoutingDecision
    responses: typing.List[QueryResponse]
    overall_confidence: float
    orchestration_time_ms: float
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

# SUB ENGINE REGISTRY

SUB_ENGINE_REGISTRY: typing.Dict[str, SubEngineConfig] = {
    "RAIL01": SubEngineConfig(
        engine_id="RAIL01",
        name="Track Engineering",
        port=8871,
        health_url="http://localhost:8871/health",
        capabilities=["track_analysis", "track_design", "track_maintenance", "track_defect_detection"],
        weight=1.0,
        domains=["track", "railbed", "ballast", "geometry", "alignment", "switch", "curve", "grade", "rail", "weld", "joint"]
    ),
    "RAIL02": SubEngineConfig(
        engine_id="RAIL02",
        name="Locomotive Systems",
        port=8872,
        health_url="http://localhost:8872/health",
        capabilities=["locomotive_diagnostics", "engine_performance", "fuel_management", "traction_control"],
        weight=1.0,
        domains=["locomotive", "engine", "diesel", "electric", "traction", "brake", "cab", "control", "cooling", "power"]
    ),
    "RAIL03": SubEngineConfig(
        engine_id="RAIL03",
        name="Signal Systems",
        port=8873,
        health_url="http://localhost:8873/health",
        capabilities=["signal_monitoring", "signal_design", "signal_failure_detection", "interlocking"],
        weight=1.0,
        domains=["signal", "interlocking", "block", "aspect", "track_circuit", "relay", "cab_signal", "wayside", "crossing"]
    ),
    "RAIL04": SubEngineConfig(
        engine_id="RAIL04",
        name="Freight Operations",
        port=8874,
        health_url="http://localhost:8874/health",
        capabilities=["freight_scheduling", "cargo_tracking", "load_management", "freight_delay_analysis"],
        weight=1.0,
        domains=["freight", "cargo", "manifest", "consist", "load", "shipment", "delivery", "car", "wagon", "container"]
    ),
    "RAIL05": SubEngineConfig(
        engine_id="RAIL05",
        name="Rail Safety",
        port=8875,
        health_url="http://localhost:8875/health",
        capabilities=["safety_audit", "incident_analysis", "risk_assessment", "compliance"],
        weight=1.0,
        domains=["safety", "incident", "risk", "audit", "hazard", "report", "regulation", "inspection", "compliance"]
    ),
    "RAIL06": SubEngineConfig(
        engine_id="RAIL06",
        name="Rail Structures",
        port=8876,
        health_url="http://localhost:8876/health",
        capabilities=["structure_analysis", "bridge_monitoring", "tunnel_inspection", "station_design"],
        weight=1.0,
        domains=["structure", "bridge", "tunnel", "station", "platform", "viaduct", "culvert", "abutment", "pier", "foundation"]
    ),
    "RAIL07": SubEngineConfig(
        engine_id="RAIL07",
        name="Rolling Stock",
        port=8877,
        health_url="http://localhost:8877/health",
        capabilities=["rolling_stock_management", "car_diagnostics", "maintenance_tracking", "fleet_analysis"],
        weight=1.0,
        domains=["rolling_stock", "car", "wagon", "coach", "bogie", "axle", "wheel", "coupler", "brake", "door"]
    ),
    "RAIL08": SubEngineConfig(
        engine_id="RAIL08",
        name="Electrification",
        port=8878,
        health_url="http://localhost:8878/health",
        capabilities=["electrification_design", "power_supply_monitoring", "catenary_analysis", "substation_management"],
        weight=1.0,
        domains=["electrification", "catenary", "substation", "overhead", "power", "voltage", "current", "transformer", "switchgear"]
    ),
    "RAIL09": SubEngineConfig(
        engine_id="RAIL09",
        name="Train Control",
        port=8879,
        health_url="http://localhost:8879/health",
        capabilities=["train_control_systems", "automatic_train_operation", "ptc_monitoring", "dispatch"],
        weight=1.0,
        domains=["train_control", "ptc", "cbtc", "dispatch", "schedule", "movement", "routing", "control", "authority"]
    ),
    "RAIL10": SubEngineConfig(
        engine_id="RAIL10",
        name="Yard Operations",
        port=8880,
        health_url="http://localhost:8880/health",
        capabilities=["yard_management", "switching", "classification", "yard_congestion_analysis"],
        weight=1.0,
        domains=["yard", "switching", "classification", "hump", "retarder", "track", "arrival", "departure", "shunting"]
    ),
    "RAIL11": SubEngineConfig(
        engine_id="RAIL11",
        name="Passenger Rail",
        port=8881,
        health_url="http://localhost:8881/health",
        capabilities=["passenger_scheduling", "ticketing", "customer_service", "passenger_complaint_analysis"],
        weight=1.0,
        domains=["passenger", "ticket", "schedule", "service", "complaint", "coach", "car", "platform", "boarding", "fare"]
    ),
}

# ROUTING RULES (domain keyword to engine_id mapping)
ROUTING_RULES: typing.Dict[str, str] = {
    # Track Engineering
    "track": "RAIL01",
    "railbed": "RAIL01",
    "ballast": "RAIL01",
    "geometry": "RAIL01",
    "alignment": "RAIL01",
    "switch": "RAIL01",
    "curve": "RAIL01",
    "grade": "RAIL01",
    "rail": "RAIL01",
    "weld": "RAIL01",
    "joint": "RAIL01",
    "maintenance": "RAIL01",
    "defect": "RAIL01",
    "inspection": "RAIL01",
    "track_design": "RAIL01",
    "track_analysis": "RAIL01",
    "track_maintenance": "RAIL01",
    "track_defect_detection": "RAIL01",
    "track_upgrade": "RAIL01",
    "track_replacement": "RAIL01",
    "track_survey": "RAIL01",
    "track_capacity": "RAIL01",
    "track_speed": "RAIL01",
    "track_wear": "RAIL01",
    "track_life": "RAIL01",
    "track_utilization": "RAIL01",
    "track_condition": "RAIL01",
    "track_monitoring": "RAIL01",
    "track_repair": "RAIL01",
    "track_failure": "RAIL01",
    "track_geometry": "RAIL01",
    "track_alignment": "RAIL01",
    "track_gradient": "RAIL01",
    "track_gauge": "RAIL01",
    "track_clearance": "RAIL01",
    "track_profile": "RAIL01",
    "track_safety": "RAIL01",
    "track_audit": "RAIL01",
    "track_risk": "RAIL01",
    "track_regulation": "RAIL01",
    "track_compliance": "RAIL01",
    # Locomotive Systems
    "locomotive": "RAIL02",
    "engine": "RAIL02",
    "diesel": "RAIL02",
    "electric": "RAIL02",
    "traction": "RAIL02",
    "brake": "RAIL02",
    "cab": "RAIL02",
    "control": "RAIL02",
    "cooling": "RAIL02",
    "power": "RAIL02",
    "locomotive_diagnostics": "RAIL02",
    "engine_performance": "RAIL02",
    "fuel_management": "RAIL02",
    "traction_control": "RAIL02",
    "locomotive_maintenance": "RAIL02",
    "locomotive_failure": "RAIL02",
    "locomotive_repair": "RAIL02",
    "locomotive_upgrade": "RAIL02",
    "locomotive_monitoring": "RAIL02",
    "locomotive_audit": "RAIL02",
    "locomotive_compliance": "RAIL02",
    "locomotive_risk": "RAIL02",
    "locomotive_safety": "RAIL02",
    "locomotive_report": "RAIL02",
    # Signal Systems
    "signal": "RAIL03",
    "interlocking": "RAIL03",
    "block": "RAIL03",
    "aspect": "RAIL03",
    "track_circuit": "RAIL03",
    "relay": "RAIL03",
    "cab_signal": "RAIL03",
    "wayside": "RAIL03",
    "crossing": "RAIL03",
    "signal_monitoring": "RAIL03",
    "signal_design": "RAIL03",
    "signal_failure_detection": "RAIL03",
    "interlocking_design": "RAIL03",
    "signal_upgrade": "RAIL03",
    "signal_replacement": "RAIL03",
    "signal_audit": "RAIL03",
    "signal_compliance": "RAIL03",
    "signal_safety": "RAIL03",
    "signal_report": "RAIL03",
    "signal_risk": "RAIL03",
    "signal_maintenance": "RAIL03",
    "signal_inspection": "RAIL03",
    # Freight Operations
    "freight": "RAIL04",
    "cargo": "RAIL04",
    "manifest": "RAIL04",
    "consist": "RAIL04",
    "load": "RAIL04",
    "shipment": "RAIL04",
    "delivery": "RAIL04",
    "car": "RAIL04",
    "wagon": "RAIL04",
    "container": "RAIL04",
    "freight_scheduling": "RAIL04",
    "cargo_tracking": "RAIL04",
    "load_management": "RAIL04",
    "freight_delay_analysis": "RAIL04",
    "freight_audit": "RAIL04",
    "freight_compliance": "RAIL04",
    "freight_risk": "RAIL04",
    "freight_report": "RAIL04",
    "freight_maintenance": "RAIL04",
    "freight_upgrade": "RAIL04",
    "freight_monitoring": "RAIL04",
    "freight_inspection": "RAIL04",
    # Rail Safety
    "safety": "RAIL05",
    "incident": "RAIL05",
    "risk": "RAIL05",
    "audit": "RAIL05",
    "hazard": "RAIL05",
    "report": "RAIL05",
    "regulation": "RAIL05",
    "inspection": "RAIL05",
    "compliance": "RAIL05",
    "safety_audit": "RAIL05",
    "incident_analysis": "RAIL05",
    "risk_assessment": "RAIL05",
    "safety_report": "RAIL05",
    "safety_monitoring": "RAIL05",
    "safety_upgrade": "RAIL05",
    "safety_failure": "RAIL05",
    "safety_maintenance": "RAIL05",
    "safety_inspection": "RAIL05",
    "safety_compliance": "RAIL05",
    # Rail Structures
    "structure": "RAIL06",
    "bridge": "RAIL06",
    "tunnel": "RAIL06",
    "station": "RAIL06",
    "platform": "RAIL06",
    "viaduct": "RAIL06",
    "culvert": "RAIL06",
    "abutment": "RAIL06",
    "pier": "RAIL06",
    "foundation": "RAIL06",
    "structure_analysis": "RAIL06",
    "bridge_monitoring": "RAIL06",
    "tunnel_inspection": "RAIL06",
    "station_design": "RAIL06",
    "structure_audit": "RAIL06",
    "structure_compliance": "RAIL06",
    "structure_risk": "RAIL06",
    "structure_report": "RAIL06",
    "structure_upgrade": "RAIL06",
    "structure_failure": "RAIL06",
    "structure_maintenance": "RAIL06",
    "structure_inspection": "RAIL06",
    # Rolling Stock
    "rolling_stock": "RAIL07",
    "car": "RAIL07",
    "wagon": "RAIL07",
    "coach": "RAIL07",
    "bogie": "RAIL07",
    "axle": "RAIL07",
    "wheel": "RAIL07",
    "coupler": "RAIL07",
    "brake": "RAIL07",
    "door": "RAIL07",
    "rolling_stock_management": "RAIL07",
    "car_diagnostics": "RAIL07",
    "maintenance_tracking": "RAIL07",
    "fleet_analysis": "RAIL07",
    "rolling_stock_audit": "RAIL07",
    "rolling_stock_compliance": "RAIL07",
    "rolling_stock_risk": "RAIL07",
    "rolling_stock_report": "RAIL07",
    "rolling_stock_upgrade": "RAIL07",
    "rolling_stock_failure": "RAIL07",
    "rolling_stock_maintenance": "RAIL07",
    "rolling_stock_inspection": "RAIL07",
    # Electrification
    "electrification": "RAIL08",
    "catenary": "RAIL08",
    "substation": "RAIL08",
    "overhead": "RAIL08",
    "power": "RAIL08",
    "voltage": "RAIL08",
    "current": "RAIL08",
    "transformer": "RAIL08",
    "switchgear": "RAIL08",
    "electrification_design": "RAIL08",
    "power_supply_monitoring": "RAIL08",
    "catenary_analysis": "RAIL08",
    "substation_management": "RAIL08",
    "electrification_audit": "RAIL08",
    "electrification_compliance": "RAIL08",
    "electrification_risk": "RAIL08",
    "electrification_report": "RAIL08",
    "electrification_upgrade": "RAIL08",
    "electrification_failure": "RAIL08",
    "electrification_maintenance": "RAIL08",
    "electrification_inspection": "RAIL08",
    # Train Control
    "train_control": "RAIL09",
    "ptc": "RAIL09",
    "cbtc": "RAIL09",
    "dispatch": "RAIL09",
    "schedule": "RAIL09",
    "movement": "RAIL09",
    "routing": "RAIL09",
    "control": "RAIL09",
    "authority": "RAIL09",
    "train_control_systems": "RAIL09",
    "automatic_train_operation": "RAIL09",
    "ptc_monitoring": "RAIL09",
    "dispatch_management": "RAIL09",
    "train_control_audit": "RAIL09",
    "train_control_compliance": "RAIL09",
    "train_control_risk": "RAIL09",
    "train_control_report": "RAIL09",
    "train_control_upgrade": "RAIL09",
    "train_control_failure": "RAIL09",
    "train_control_maintenance": "RAIL09",
    "train_control_inspection": "RAIL09",
    # Yard Operations
    "yard": "RAIL10",
    "switching": "RAIL10",
    "classification": "RAIL10",
    "hump": "RAIL10",
    "retarder": "RAIL10",
    "arrival": "RAIL10",
    "departure": "RAIL10",
    "shunting": "RAIL10",
    "yard_management": "RAIL10",
    "yard_congestion_analysis": "RAIL10",
    "yard_audit": "RAIL10",
    "yard_compliance": "RAIL10",
    "yard_risk": "RAIL10",
    "yard_report": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_maintenance": "RAIL10",
    "yard_inspection": "RAIL10",
    # Passenger Rail
    "passenger": "RAIL11",
    "ticket": "RAIL11",
    "schedule": "RAIL11",
    "service": "RAIL11",
    "complaint": "RAIL11",
    "coach": "RAIL11",
    "car": "RAIL11",
    "platform": "RAIL11",
    "boarding": "RAIL11",
    "fare": "RAIL11",
    "passenger_scheduling": "RAIL11",
    "ticketing": "RAIL11",
    "customer_service": "RAIL11",
    "passenger_complaint_analysis": "RAIL11",
    "passenger_audit": "RAIL11",
    "passenger_compliance": "RAIL11",
    "passenger_risk": "RAIL11",
    "passenger_report": "RAIL11",
    "passenger_upgrade": "RAIL11",
    "passenger_failure": "RAIL11",
    "passenger_maintenance": "RAIL11",
    "passenger_inspection": "RAIL11",
    # Additional domain keywords (for 200+ rules)
    "weather": "RAIL05",
    "weather_impact": "RAIL05",
    "environmental": "RAIL05",
    "environmental_hazard": "RAIL05",
    "regulatory": "RAIL05",
    "regulatory_compliance": "RAIL05",
    "security": "RAIL05",
    "security_breach": "RAIL05",
    "material": "RAIL04",
    "material_shortage": "RAIL04",
    "equipment": "RAIL07",
    "equipment_failure": "RAIL07",
    "operational": "RAIL04",
    "operational_bottleneck": "RAIL04",
    "customer": "RAIL11",
    "customer_service": "RAIL11",
    "incident_report": "RAIL05",
    "system_upgrade": "RAIL09",
    "data_integrity": "RAIL09",
    # Expand with more synonyms and related terms for each domain
    "railway": "RAIL01",
    "railroad": "RAIL01",
    "train": "RAIL09",
    "rolling": "RAIL07",
    "stock": "RAIL07",
    "freight_car": "RAIL04",
    "passenger_car": "RAIL11",
    "yard_switch": "RAIL10",
    "yard_hump": "RAIL10",
    "yard_retarder": "RAIL10",
    "yard_shunting": "RAIL10",
    "yard_arrival": "RAIL10",
    "yard_departure": "RAIL10",
    "yard_classification": "RAIL10",
    "yard_management_system": "RAIL10",
    "yard_congestion": "RAIL10",
    "yard_delay": "RAIL10",
    "yard_optimization": "RAIL10",
    "yard_safety": "RAIL10",
    "yard_audit": "RAIL10",
    "yard_report": "RAIL10",
    "yard_risk": "RAIL10",
    "yard_compliance": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_maintenance": "RAIL10",
    "yard_inspection": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_analysis": "RAIL10",
    "yard_design": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_profile": "RAIL10",
    "yard_clearance": "RAIL10",
    "yard_gradient": "RAIL10",
    "yard_geometry": "RAIL10",
    "yard_alignment": "RAIL10",
    "yard_gauge": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
    "yard_monitoring": "RAIL10",
    "yard_condition": "RAIL10",
    "yard_utilization": "RAIL10",
    "yard_capacity": "RAIL10",
    "yard_speed": "RAIL10",
    "yard_life": "RAIL10",
    "yard_wear": "RAIL10",
    "yard_survey": "RAIL10",
    "yard_replacement": "RAIL10",
    "yard_upgrade": "RAIL10",
    "yard_repair": "RAIL10",
    "yard_failure": "RAIL10",
}

# =============================================================
# DOCTRINE CACHE
# =============================================================

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
        topic="Track Geometry Gauge and Cross-Level Standards",
        keywords=["track geometry", "gauge", "cross-level", "alignment", "profile", "twist", "FRA", "AREMA"],
        conclusion_template=(
            "Maintaining track gauge within FRA and AREMA standards ensures safe train operations by "
            "preventing derailments caused by gauge widening or narrowing. Cross-level tolerances must "
            "be controlled to reduce dynamic forces on rolling stock and track components."
        ),
        reasoning_framework=(
            "Track gauge is a critical parameter defining the distance between the inner faces of the rails. "
            "According to FRA regulations (49 CFR Part 213), standard gauge is 56.5 inches with allowable "
            "tolerances depending on track class. Excessive gauge widening leads to increased risk of wheel "
            "drop and derailment, while narrowing can cause flange climb. Cross-level, the difference in elevation "
            "between two rails, affects lateral stability and ride comfort. AREMA Manual for Railway Engineering "
            "specifies maximum cross-level variations to limit lateral forces and prevent track component fatigue. "
            "Alignment and profile deviations influence dynamic loading and wear patterns. Twist, or differential "
            "cross-level over a short distance, can induce wheel unloading and increase derailment risk. "
            "Regular measurement using track geometry cars and tamping machines is essential for maintaining "
            "these parameters within limits. Failure to comply with these standards has been linked to multiple "
            "FRA accident investigations (FRA Safety Advisory 2014-01). The reasoning integrates mechanical "
            "engineering principles, vehicle-track interaction dynamics, and regulatory compliance to ensure "
            "operational safety and infrastructure longevity."
        ),
        key_factors=[
            "Gauge tolerance limits per FRA class",
            "Cross-level maximum variation",
            "Alignment curvature and superelevation",
            "Profile smoothness and vertical irregularities",
            "Twist limits over specified chord lengths",
            "Measurement frequency and instrumentation",
            "Maintenance procedures (tamping, lining)",
            "Impact on derailment risk and ride quality"
        ],
        primary_authority=[
            "49 CFR Part 213 - Track Safety Standards",
            "AREMA Manual for Railway Engineering, Chapter 30",
            "FRA Safety Advisory 2014-01",
            "Transportation Research Board - Track Geometry Handbook",
            "Federal Railroad Administration Track Safety Standards Compliance Manual"
        ],
        burden_holder="Track Owner and Maintenance Entity",
        adversary_position=(
            "Some argue that slight deviations in gauge and cross-level do not significantly affect safety "
            "and that maintenance costs outweigh benefits."
        ),
        counter_arguments=[
            "Empirical data links gauge deviations to derailments",
            "Dynamic simulations show increased lateral forces with cross-level errors",
            "Regulatory mandates require adherence regardless of cost",
            "Long-term infrastructure degradation accelerates with poor geometry",
            "Passenger comfort and freight integrity depend on stable geometry"
        ],
        resolution_strategy=(
            "Implement continuous track geometry monitoring, enforce maintenance schedules, "
            "and conduct risk-based inspections to prioritize corrective actions."
        ),
        entity_scope="Track Engineering Departments and Maintenance Contractors",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FRA Track Safety Standards Enforcement Actions (2010-2020)"
    ),
    DoctrineBlock(
        topic="Locomotive Diesel-Electric Traction Motor Power Systems",
        keywords=["locomotive", "diesel-electric", "traction motor", "AC", "DC", "power", "efficiency", "EMD", "GE"],
        conclusion_template=(
            "Optimizing diesel-electric locomotive traction motor power systems through selection of AC or DC "
            "motors directly impacts tractive effort, efficiency, and maintenance costs."
        ),
        reasoning_framework=(
            "Diesel-electric locomotives convert diesel engine mechanical power into electrical energy to drive "
            "traction motors connected to the wheels. Historically, DC traction motors were standard due to "
            "simplicity and robustness. However, modern locomotives increasingly use AC traction motors, "
            "which offer better adhesion control, higher reliability, and reduced maintenance. AC motors utilize "
            "inverters and sophisticated control electronics to modulate power delivery, improving tractive "
            "effort at low speeds and reducing wheel slip. The choice between AC and DC systems affects "
            "performance characteristics such as starting tractive effort, continuous tractive effort, "
            "thermal management, and regenerative braking capabilities. Manufacturers like Electro-Motive "
            "Diesel (EMD) and General Electric (GE) have developed proprietary AC traction systems that "
            "comply with EPA Tier 4 emissions standards and optimize fuel consumption. The reasoning involves "
            "electrical engineering principles, thermal dynamics, and operational requirements. "
            "Regulatory compliance with emissions and noise standards also influences system design."
        ),
        key_factors=[
            "Traction motor type (AC vs DC)",
            "Power rating and continuous tractive effort",
            "Adhesion control and wheel slip prevention",
            "Thermal management and cooling systems",
            "Regenerative braking capability",
            "Maintenance intervals and costs",
            "Compatibility with locomotive control systems",
            "Emissions compliance and fuel efficiency"
        ],
        primary_authority=[
            "EPA Tier 4 Locomotive Emission Standards",
            "Association of American Railroads (AAR) Locomotive Manual",
            "IEEE Std 115 - AC Traction Motor Standards",
            "Electro-Motive Diesel Technical Bulletins",
            "General Electric Transportation Locomotive Specifications"
        ],
        burden_holder="Locomotive Manufacturer and Operator",
        adversary_position=(
            "Some stakeholders claim DC traction motors are more cost-effective and simpler to maintain "
            "despite lower efficiency."
        ),
        counter_arguments=[
            "AC motors reduce lifecycle maintenance costs",
            "Improved adhesion control reduces wheel wear",
            "Regenerative braking recovers energy",
            "AC systems comply better with modern emissions standards",
            "Operational flexibility and performance gains justify initial investment"
        ],
        resolution_strategy=(
            "Adopt AC traction motor systems for new locomotives and retrofit where feasible, "
            "while maintaining DC systems in legacy fleets with optimized maintenance."
        ),
        entity_scope="Locomotive Engineering and Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA Locomotive Emission Regulations and AAR Technical Standards"
    ),
    DoctrineBlock(
        topic="Signal Systems: Positive Train Control (PTC) Implementation",
        keywords=["signal systems", "positive train control", "PTC", "CBTC", "interlocking", "wayside", "FRA", "safety"],
        conclusion_template=(
            "Implementing Positive Train Control systems significantly enhances rail safety by preventing "
            "collisions, overspeed derailments, and unauthorized movements through automated train control."
        ),
        reasoning_framework=(
            "Positive Train Control (PTC) is a federally mandated safety overlay system designed to automatically "
            "stop or slow trains to prevent accidents. PTC integrates GPS, wireless communications, onboard "
            "computers, and wayside interface units to monitor train positions and enforce movement authorities. "
            "The system interfaces with existing signal interlockings and dispatch systems to override human "
            "error. The complexity of PTC implementation involves interoperability among different railroads, "
            "integration with legacy signal systems, and compliance with FRA deadlines. Communications-based "
            "train control (CBTC) systems, while more common in transit, share similar principles for train "
            "spacing and control. The reasoning includes safety engineering, systems integration, and regulatory "
            "compliance. FRA regulations (49 CFR Part 236 Subpart I) specify technical standards and implementation "
            "requirements. The system reduces risk of collisions, derailments due to overspeed, and incursions "
            "into work zones, thereby improving overall network safety."
        ),
        key_factors=[
            "System interoperability and standardization",
            "Accuracy and reliability of GPS and communications",
            "Integration with existing signal interlockings",
            "Human factors and operator interface",
            "Regulatory compliance deadlines",
            "Cybersecurity and data integrity",
            "Fail-safe design and redundancy",
            "Training and operational procedures"
        ],
        primary_authority=[
            "49 CFR Part 236 Subpart I - Positive Train Control Systems",
            "FRA PTC Implementation Guidelines",
            "Association of American Railroads PTC Technical Standards",
            "Federal Transit Administration CBTC Standards",
            "Railway Safety Act and Amendments"
        ],
        burden_holder="Railroad Operators and Signal System Vendors",
        adversary_position=(
            "Critics argue PTC implementation costs are excessive and cause operational delays."
        ),
        counter_arguments=[
            "PTC prevents costly and fatal accidents",
            "Regulatory mandates require implementation",
            "Long-term operational efficiencies offset costs",
            "Improved safety enhances public confidence",
            "Technological advancements reduce complexity over time"
        ],
        resolution_strategy=(
            "Phased deployment with rigorous testing, operator training, and continuous system improvement."
        ),
        entity_scope="Signal Engineering and Operations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="FRA Enforcement of PTC Implementation Deadlines (2015-2020)"
    ),
    DoctrineBlock(
        topic="Freight Operations: Unit Train Scheduling and Intermodal Coordination",
        keywords=["freight operations", "unit train", "intermodal", "manifest", "scheduling", "capacity", "logistics"],
        conclusion_template=(
            "Efficient scheduling of unit trains and intermodal services optimizes network capacity, reduces dwell times, "
            "and improves supply chain reliability."
        ),
        reasoning_framework=(
            "Freight rail operations rely heavily on the efficient scheduling of unit trains—trains carrying a single commodity "
            "from origin to destination without intermediate switching—and intermodal trains that transport containers or trailers. "
            "Unit trains maximize throughput by reducing handling and transit times, while intermodal operations require precise "
            "coordination with ports, terminals, and trucking networks. Scheduling must consider track capacity, yard availability, "
            "crew assignments, and maintenance windows. Advanced software tools and real-time data analytics enable dynamic "
            "rescheduling to respond to disruptions. Manifest trains, carrying mixed freight, require complex sorting and switching, "
            "which impacts network fluidity. The reasoning integrates logistics management, capacity planning, and operational "
            "research. Regulatory constraints such as hours of service and safety inspections also influence scheduling. "
            "Optimizing these operations reduces costs, improves asset utilization, and enhances customer service."
        ),
        key_factors=[
            "Train type (unit, intermodal, manifest)",
            "Terminal and yard capacity",
            "Track network constraints",
            "Crew and locomotive availability",
            "Regulatory compliance (hours of service)",
            "Real-time traffic management systems",
            "Customer delivery requirements",
            "Maintenance and inspection scheduling"
        ],
        primary_authority=[
            "Association of American Railroads Freight Operations Manual",
            "Federal Railroad Administration Hours of Service Regulations",
            "Transportation Research Board - Freight Rail Scheduling Studies",
            "Surface Transportation Board Rate and Service Rules",
            "Intermodal Association of North America Guidelines"
        ],
        burden_holder="Freight Rail Operators and Logistics Planners",
        adversary_position=(
            "Some stakeholders claim that rigid scheduling reduces flexibility and responsiveness."
        ),
        counter_arguments=[
            "Predictable schedules improve network fluidity",
            "Dynamic rescheduling tools enhance responsiveness",
            "Compliance with safety regulations mandates structured operations",
            "Customer expectations require reliable delivery windows",
            "Efficient scheduling reduces operational costs and congestion"
        ],
        resolution_strategy=(
            "Implement integrated scheduling platforms with real-time data feeds and collaborative planning among stakeholders."
        ),
        entity_scope="Freight Operations and Network Planning",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="STB Cases on Freight Service Performance and Scheduling (2010-2020)"
    ),
    DoctrineBlock(
        topic="Railroad Safety: FRA Defect Detection and Inspection Protocols",
        keywords=["railroad safety", "FRA", "defect detection", "inspection", "track", "rolling stock", "maintenance"],
        conclusion_template=(
            "Adherence to FRA defect detection and inspection protocols is essential to identify and mitigate safety risks "
            "before they result in accidents."
        ),
        reasoning_framework=(
            "The Federal Railroad Administration mandates comprehensive inspection regimes for track, rolling stock, "
            "and signal systems to detect defects that could compromise safety. Track inspections include visual "
            "examinations, ultrasonic rail flaw detection, geometry measurements, and ballast condition assessments. "
            "Rolling stock inspections cover brake systems, wheels, couplers, and structural components. The FRA "
            "Track Safety Standards (49 CFR Part 213) specify inspection frequencies based on track class and traffic. "
            "Defect detection technologies such as ultrasonic testing, eddy current, and acoustic monitoring enable "
            "early identification of internal rail flaws, wheel defects, and component fatigue. The reasoning involves "
            "materials science, non-destructive testing methods, and risk management. Timely detection and repair "
            "prevent derailments and equipment failures. Non-compliance can result in enforcement actions and increased "
            "liability. Coordination between maintenance crews, inspectors, and operations is critical to minimize "
            "service disruptions while ensuring safety."
        ),
        key_factors=[
            "Inspection frequency and methods",
            "Defect detection technologies",
            "Track class and traffic density",
            "Maintenance response times",
            "Training and certification of inspectors",
            "Data management and reporting",
            "Integration with safety management systems",
            "Regulatory compliance and enforcement"
        ],
        primary_authority=[
            "49 CFR Part 213 - Track Safety Standards",
            "FRA Motive Power and Equipment Safety Standards (49 CFR Part 229)",
            "AREMA Manual for Railway Engineering - Inspection Chapters",
            "FRA Safety Advisory 2017-03 on Defect Detection",
            "Transportation Technology Center, Inc. (TTCI) Research Reports"
        ],
        burden_holder="Railroad Safety and Maintenance Departments",
        adversary_position=(
            "Some operators argue that inspection costs and service interruptions outweigh benefits."
        ),
        counter_arguments=[
            "Early defect detection prevents catastrophic failures",
            "Regulatory mandates require compliance",
            "Improved inspection technologies reduce downtime",
            "Safety incidents have high human and financial costs",
            "Data-driven maintenance optimizes resource allocation"
        ],
        resolution_strategy=(
            "Adopt advanced defect detection technologies, train personnel rigorously, "
            "and integrate inspection data into predictive maintenance systems."
        ),
        entity_scope="Safety and Maintenance Operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="FRA Enforcement Actions and Safety Recommendations (2010-2022)"
    ),
    DoctrineBlock(
        topic="Rail Structures: Bridge Load Rating and Structural Assessment",
        keywords=["bridge", "tunnel", "viaduct", "load rating", "structural assessment", "NBI", "AASHTO", "FRA"],
        conclusion_template=(
            "Accurate load rating and structural assessment of rail bridges and tunnels ensure safe passage of trains "
            "and compliance with regulatory standards."
        ),
        reasoning_framework=(
            "Railroad bridges and tunnels are critical infrastructure components requiring periodic structural assessment "
            "to determine their load carrying capacity and identify deterioration. Load rating involves evaluating "
            "structural elements against current and projected loads, including static and dynamic train loads, "
            "environmental effects, and fatigue. The National Bridge Inventory (NBI) provides standardized data collection "
            "protocols. AASHTO Manual for Railway Engineering and FRA Bridge Safety Standards guide assessment methodologies. "
            "Structural engineers perform visual inspections, non-destructive testing, and load testing to detect "
            "cracks, corrosion, and material degradation. The reasoning incorporates structural mechanics, materials science, "
            "and safety engineering. Accurate load ratings prevent overloading and potential failures. Rehabilitation "
            "or replacement decisions rely on these assessments. Compliance with FRA Bridge Safety Standards (49 CFR Part 237) "
            "is mandatory. Coordination with track maintenance and operations is necessary to minimize service impacts."
        ),
        key_factors=[
            "Load rating methodologies and standards",
            "Inspection frequency and techniques",
            "Material condition and deterioration",
            "Dynamic effects of train loading",
            "Environmental impacts (corrosion, freeze-thaw)",
            "Fatigue and fracture mechanics",
            "Rehabilitation and retrofit options",
            "Regulatory compliance and documentation"
        ],
        primary_authority=[
            "49 CFR Part 237 - Bridge Safety Standards",
            "AASHTO Manual for Railway Engineering, Chapter 7",
            "National Bridge Inventory (NBI) Guidelines",
            "FRA Bridge Safety Program Reports",
            "Transportation Research Board Structural Engineering Publications"
        ],
        burden_holder="Railroad Engineering and Bridge Maintenance Departments",
        adversary_position=(
            "Some argue that load rating processes are overly conservative, leading to unnecessary costly repairs."
        ),
        counter_arguments=[
            "Safety of life and equipment mandates conservative design",
            "Aging infrastructure requires rigorous assessment",
            "Load increases from modern trains exceed original design loads",
            "Failure consequences justify preventive maintenance",
            "Regulatory compliance is legally binding"
        ],
        resolution_strategy=(
            "Employ risk-based inspection and load rating combined with condition monitoring to optimize maintenance."
        ),
        entity_scope="Railroad Structural Engineering",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA Bridge Safety Enforcement and NTSB Bridge Failure Investigations"
    ),
    DoctrineBlock(
        topic="Rolling Stock: Freight Car Types and Maintenance Requirements",
        keywords=["rolling stock", "freight car", "tank car", "hopper", "gondola", "intermodal", "maintenance", "AAR"],
        conclusion_template=(
            "Proper classification and maintenance of freight car types ensure operational efficiency and regulatory compliance."
        ),
        reasoning_framework=(
            "Freight rolling stock comprises various car types designed for specific commodities and loading methods. "
            "Tank cars transport liquids and gases, requiring stringent safety standards including pressure relief devices "
            "and periodic inspections per DOT regulations. Hopper cars carry bulk commodities like coal or grain, "
            "with maintenance focusing on structural integrity and unloading mechanisms. Gondola cars handle heavy bulk materials "
            "with open tops, necessitating corrosion protection and structural inspections. Intermodal cars support containerized "
            "freight, requiring compatibility with handling equipment and securement systems. The Association of American Railroads "
            "(AAR) sets maintenance standards and interchange rules. Maintenance includes wheelset inspections, brake system checks, "
            "and structural repairs. Proper classification affects routing, loading, and safety compliance. The reasoning integrates "
            "mechanical engineering, materials science, and regulatory frameworks. Failure to maintain rolling stock can lead to "
            "accidents, cargo loss, and regulatory penalties."
        ),
        key_factors=[
            "Freight car type and design features",
            "Commodity-specific safety requirements",
            "Inspection and maintenance intervals",
            "Brake system functionality",
            "Wheel and axle condition",
            "Structural integrity and corrosion control",
            "Interchange rules and documentation",
            "Compatibility with loading/unloading equipment"
        ],
        primary_authority=[
            "AAR Interchange Rules",
            "49 CFR Parts 179 and 180 - Tank Car Safety Standards",
            "FRA Motive Power and Equipment Safety Standards (49 CFR Part 229)",
            "AAR Manual of Standards and Recommended Practices",
            "Federal Hazardous Materials Regulations"
        ],
        burden_holder="Railroad Rolling Stock Maintenance and Operations",
        adversary_position=(
            "Some operators delay maintenance to reduce downtime and costs."
        ),
        counter_arguments=[
            "Deferred maintenance increases accident risk",
            "Regulatory inspections enforce compliance",
            "Proper maintenance extends equipment life",
            "Safety incidents cause greater financial loss",
            "Customer confidence depends on reliable equipment"
        ],
        resolution_strategy=(
            "Implement predictive maintenance programs and strict adherence to AAR and FRA standards."
        ),
        entity_scope="Rolling Stock Maintenance and Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA Enforcement Actions on Rolling Stock Defects"
    ),
    DoctrineBlock(
        topic="Rail Electrification: Catenary and Third Rail Systems",
        keywords=["electrification", "catenary", "third rail", "substation", "transformer", "AC", "DC", "power supply"],
        conclusion_template=(
            "Design and maintenance of electrification systems, including catenary and third rail, are vital for reliable "
            "electric train operations and safety."
        ),
        reasoning_framework=(
            "Rail electrification systems provide power to electric locomotives and multiple units through overhead catenary wires "
            "or third rail conductors. Catenary systems typically operate at high voltage AC (e.g., 25 kV 60 Hz), requiring substations "
            "to step down and convert power. Third rail systems use lower voltage DC power (e.g., 750 V DC) and are common in urban "
            "transit. Design considerations include electrical clearances, mechanical tensioning of wires, insulation, and "
            "protection from environmental factors. Transformers and substations must maintain voltage stability and handle "
            "load variations. Maintenance includes inspection of contact wires, insulators, support structures, and electrical "
            "components. Safety protocols address risks of electrocution and system failures. The reasoning involves electrical "
            "engineering, power systems analysis, and safety standards such as IEEE Std 80 and NFPA 130. Proper design and "
            "maintenance ensure operational reliability and minimize downtime."
        ),
        key_factors=[
            "Voltage and current specifications",
            "Catenary wire tension and sag",
            "Substation transformer capacity",
            "Insulation and clearance requirements",
            "Environmental exposure and corrosion",
            "Safety protocols and grounding",
            "Maintenance schedules and inspection",
            "Compatibility with rolling stock"
        ],
        primary_authority=[
            "IEEE Std 80 - Guide for Safety in AC Substation Grounding",
            "NFPA 130 - Standard for Fixed Guideway Transit and Passenger Rail Systems",
            "AREMA Manual for Railway Engineering - Electrification Chapter",
            "FRA Regulations on Electrified Railroads",
            "National Electrical Safety Code (NESC)"
        ],
        burden_holder="Rail Electrification Engineering and Maintenance",
        adversary_position=(
            "Some argue that electrification infrastructure costs and maintenance complexity are prohibitive."
        ),
        counter_arguments=[
            "Electric traction reduces emissions and operating costs",
            "Reliability improvements justify investment",
            "Safety standards mitigate risks",
            "Long-term infrastructure benefits outweigh initial costs",
            "Electrification supports higher speeds and capacity"
        ],
        resolution_strategy=(
            "Adopt robust design standards, implement preventive maintenance, and invest in staff training."
        ),
        entity_scope="Rail Electrification Systems Engineering",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FRA Electrification Safety Guidelines and Industry Best Practices"
    ),
    DoctrineBlock(
        topic="Train Control: European Train Control System (ETCS) and Speed Enforcement",
        keywords=["train control", "ETCS", "positive train control", "speed enforcement", "signaling", "safety", "EULYNX"],
        conclusion_template=(
            "Implementing ETCS and advanced speed enforcement systems enhances interoperability and safety across rail networks."
        ),
        reasoning_framework=(
            "The European Train Control System (ETCS) is a standardized train control system designed to replace various national "
            "signaling systems and enable interoperability across European rail networks. ETCS provides continuous speed supervision, "
            "movement authority enforcement, and train position monitoring using balises, radio communications, and onboard units. "
            "Speed enforcement prevents overspeed derailments by automatically applying brakes if limits are exceeded. ETCS levels "
            "range from trackside signals with limited cab signaling (Level 1) to full radio-based control without lineside signals "
            "(Level 3). The system supports interoperability, reduces human error, and improves capacity. The reasoning involves "
            "control systems engineering, safety analysis, and international regulatory harmonization. European Union directives "
            "mandate ETCS implementation for interoperability and safety. The system's design principles inform similar systems "
            "globally, including PTC in the US. Integration challenges include legacy system compatibility and cybersecurity."
        ),
        key_factors=[
            "ETCS system levels and capabilities",
            "Speed supervision algorithms",
            "Train position detection accuracy",
            "Communication reliability and latency",
            "Interoperability standards (ERTMS)",
            "Human-machine interface design",
            "Cybersecurity measures",
            "Regulatory compliance and certification"
        ],
        primary_authority=[
            "European Union Directive 2016/797/EU - Interoperability of the Rail System",
            "ERTMS/ETCS System Specifications",
            "UIC Leaflet 720 - ETCS Implementation Guidelines",
            "European Railway Agency Safety Certification",
            "Railway Safety and Interoperability Regulations"
        ],
        burden_holder="Rail Infrastructure Managers and Train Operators",
        adversary_position=(
            "Concerns about high implementation costs and complexity limit adoption."
        ),
        counter_arguments=[
            "ETCS improves safety and interoperability",
            "Long-term operational savings offset costs",
            "Mandated by EU regulations",
            "Enhanced capacity and punctuality benefits",
            "Technological maturity reduces risks"
        ],
        resolution_strategy=(
            "Phased ETCS deployment with stakeholder collaboration and continuous training."
        ),
        entity_scope="Train Control and Signaling",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EU Railway Interoperability Directive and ERA Certification"
    ),
    DoctrineBlock(
        topic="Yard Operations: Classification, Hump, and Flat Switching",
        keywords=["yard operations", "classification yard", "hump yard", "flat switching", "locomotive assignment", "car sorting"],
        conclusion_template=(
            "Optimizing yard operations through appropriate classification methods and locomotive assignment improves throughput and reduces delays."
        ),
        reasoning_framework=(
            "Rail yards serve as nodes for sorting, classifying, and assembling trains. Classification yards use hump or flat switching methods. "
            "Hump yards utilize a raised track section (hump) where cars are pushed over and roll by gravity into sorting tracks, enabling "
            "efficient high-volume classification. Flat switching involves locomotives moving cars on level tracks, suitable for smaller yards "
            "or specialized operations. Locomotive assignment considers power requirements, crew availability, and operational constraints. "
            "Efficient yard operations reduce dwell times and improve network fluidity. The reasoning integrates operations research, mechanical "
            "engineering, and labor management. Safety considerations include car retarders, switching signals, and employee training. "
            "Technological advancements such as automated switching and remote control locomotives enhance efficiency. Regulatory compliance "
            "includes FRA safety standards for yard movements and employee qualifications."
        ),
        key_factors=[
            "Yard type and layout",
            "Switching method (hump vs flat)",
            "Locomotive power and control systems",
            "Car sorting algorithms and software",
            "Crew scheduling and qualifications",
            "Safety systems and protocols",
            "Throughput capacity and bottlenecks",
            "Maintenance of yard infrastructure"
        ],
        primary_authority=[
            "FRA Yard Safety Rules (49 CFR Part 218)",
            "Association of American Railroads Yard Operations Manual",
            "Transportation Research Board Yard Operations Studies",
            "Federal Railroad Administration Safety Advisories",
            "Railway Association of North America Best Practices"
        ],
        burden_holder="Yard Operations Management and Locomotive Assignment Teams",
        adversary_position=(
            "Some argue that automation reduces employment and increases complexity."
        ),
        counter_arguments=[
            "Automation improves safety and efficiency",
            "Training programs mitigate employment impacts",
            "Operational complexity requires advanced systems",
            "Improved throughput benefits overall network",
            "Safety incidents decrease with modern controls"
        ],
        resolution_strategy=(
            "Balance automation with workforce development and continuous process improvement."
        ),
        entity_scope="Rail Yard Operations and Locomotive Management",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="FRA Enforcement of Yard Safety Regulations and Industry Case Studies"
    ),
    DoctrineBlock(
        topic="Passenger Rail: Commuter and High-Speed Rail Station Design",
        keywords=["passenger rail", "commuter rail", "high-speed rail", "station design", "platforms", "accessibility", "capacity"],
        conclusion_template=(
            "Effective station design for commuter and high-speed rail enhances passenger experience, operational efficiency, and safety."
        ),
        reasoning_framework=(
            "Passenger rail stations serve as critical interfaces between the rail network and the public. Commuter rail stations prioritize "
            "accessibility, capacity, and integration with local transit. High-speed rail stations require specialized design to accommodate "
            "longer trains, higher passenger volumes, and security requirements. Platform height, length, and clearance must comply with "
            "Americans with Disabilities Act (ADA) standards and FRA guidelines. Station layout affects passenger flow, safety, and dwell times. "
            "Facilities include ticketing, waiting areas, and intermodal connections. Structural design considers seismic, wind, and load factors. "
            "Security measures include surveillance, controlled access, and emergency egress. The reasoning combines architectural design, civil "
            "engineering, human factors, and regulatory compliance. Station design impacts operational efficiency, ridership growth, and public "
            "perception."
        ),
        key_factors=[
            "Platform dimensions and ADA compliance",
            "Passenger flow and crowd management",
            "Intermodal connectivity",
            "Safety and security features",
            "Structural and environmental design",
            "Capacity planning and scalability",
            "Ticketing and passenger amenities",
            "Emergency evacuation procedures"
        ],
        primary_authority=[
            "Americans with Disabilities Act (ADA) Standards",
            "FRA Passenger Equipment Safety Standards",
            "Transportation Research Board Station Design Guidelines",
            "Federal Transit Administration Station Planning Manuals",
            "National Fire Protection Association (NFPA) Codes"
        ],
        burden_holder="Passenger Rail Operators and Station Designers",
        adversary_position=(
            "Some stakeholders prioritize cost savings over comprehensive station design."
        ),
        counter_arguments=[
            "Well-designed stations improve safety and accessibility",
            "Enhanced passenger experience increases ridership",
            "Regulatory compliance is mandatory",
            "Poor design leads to operational delays",
            "Security requirements necessitate robust design"
        ],
        resolution_strategy=(
            "Incorporate stakeholder input, adhere to standards, and apply best practices in station design."
        ),
        entity_scope="Passenger Rail Infrastructure and Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FRA Station Safety Guidelines and ADA Enforcement Cases"
    ),
    DoctrineBlock(
        topic="Rail Metallurgy: Head Hardened and Premium Rail Steel",
        keywords=["rail metallurgy", "head hardened", "premium steel", "continuous welded rail", "fatigue", "wear", "microstructure"],
        conclusion_template=(
            "Utilizing head hardened and premium rail steels in continuous welded rail enhances durability and reduces maintenance."
        ),
        reasoning_framework=(
            "Rail metallurgy focuses on the material properties of rail steel to withstand mechanical stresses and environmental conditions. "
            "Head hardened rails undergo heat treatment to increase surface hardness, improving wear resistance and extending service life. "
            "Premium steels incorporate alloying elements and controlled microstructures to enhance toughness and fatigue resistance. "
            "Continuous welded rail (CWR) benefits from these metallurgical improvements by reducing rail defects such as head checks, "
            "squats, and rolling contact fatigue. Metallurgical analysis involves understanding phase transformations, grain size, and "
            "inclusion content. The reasoning integrates materials science, mechanical engineering, and failure analysis. "
            "Standards such as AREMA and ASTM specify metallurgical requirements. Proper selection and quality control reduce lifecycle "
            "costs and improve safety by minimizing rail failures."
        ),
        key_factors=[
            "Heat treatment processes and parameters",
            "Alloy composition and microstructure",
            "Surface hardness and wear resistance",
            "Fatigue crack initiation and propagation",
            "Compatibility with welding and maintenance",
            "Environmental effects (corrosion, temperature)",
            "Quality control and testing methods",
            "Standards compliance (AREMA, ASTM)"
        ],
        primary_authority=[
            "AREMA Manual for Railway Engineering - Rail Metallurgy Chapter",
            "ASTM A759 - Specification for Head Hardened Rail Steel",
            "FRA Track Safety Standards",
            "Railway Technical Research Institute (RTRI) Publications",
            "Transportation Research Board Rail Material Studies"
        ],
        burden_holder="Rail Manufacturers and Track Maintenance Entities",
        adversary_position=(
            "Some argue premium steels increase initial costs without proportional benefits."
        ),
        counter_arguments=[
            "Reduced maintenance and longer rail life offset costs",
            "Improved safety through defect reduction",
            "Enhanced performance under heavy axle loads",
            "Compatibility with modern track technologies",
            "Industry standards recommend premium materials"
        ],
        resolution_strategy=(
            "Adopt premium rail steels in critical track segments and monitor performance through metallurgical testing."
        ),
        entity_scope="Rail Material Engineering and Track Maintenance",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FRA Rail Defect Investigations and AREMA Recommendations"
    ),
    DoctrineBlock(
        topic="Switches, Turnouts, and Crossing Diamonds: Design and Maintenance",
        keywords=["switch", "turnout", "crossing diamond", "grade crossing", "protection", "maintenance", "FRA", "AREMA"],
        conclusion_template=(
            "Proper design and maintenance of switches, turnouts, and crossing diamonds are critical to safe and efficient train movements."
        ),
        reasoning_framework=(
            "Switches and turnouts enable trains to move from one track to another and are complex mechanical assemblies subject to high dynamic loads. "
            "Crossing diamonds allow intersecting tracks to cross at grade. Design parameters include frog angles, switch point geometry, and guard rails. "
            "Maintenance focuses on lubrication, wear measurement, alignment, and timely replacement of components. Grade crossing protection involves "
            "signaling, gates, and warning systems to prevent collisions with road traffic. FRA regulations (49 CFR Part 234) govern grade crossing safety. "
            "AREMA provides detailed design and maintenance standards. Failures in these components can cause derailments or collisions. "
            "The reasoning integrates mechanical engineering, safety analysis, and human factors. Regular inspections and predictive maintenance "
            "reduce failure risks. Coordination with signal systems enhances protection."
        ),
        key_factors=[
            "Switch geometry and frog design",
            "Wear and lubrication practices",
            "Inspection frequency and criteria",
            "Grade crossing warning systems",
            "Signal integration and interlocking",
            "Component replacement thresholds",
            "Environmental effects on components",
            "Compliance with FRA and AREMA standards"
        ],
        primary_authority=[
            "49 CFR Part 234 - Grade Crossing Signal Systems and Devices",
            "AREMA Manual for Railway Engineering - Turnout and Crossing Chapters",
            "FRA Track Safety Standards",
            "National Transportation Safety Board (NTSB) Accident Reports",
            "Railway Association of North America Maintenance Guidelines"
        ],
        burden_holder="Track Maintenance and Signal Departments",
        adversary_position=(
            "Some operators defer maintenance citing operational disruptions and costs."
        ),
        counter_arguments=[
            "Deferred maintenance increases derailment risk",
            "Regulatory enforcement mandates compliance",
            "Proper maintenance extends component life",
            "Safety incidents have high human and financial costs",
            "Integrated signaling improves crossing safety"
        ],
        resolution_strategy=(
            "Implement scheduled inspections, predictive maintenance, and coordinate with signal systems."
        ),
        entity_scope="Track Maintenance and Signal Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FRA Enforcement Actions and NTSB Investigations on Switch Failures"
    ),
    DoctrineBlock(
        topic="Rail Grinding and Profiling: Defect Removal and Preventive Maintenance",
        keywords=["rail grinding", "profiling", "defect removal", "preventive maintenance", "wheel-rail interface", "wear", "fatigue"],
        conclusion_template=(
            "Regular rail grinding and profiling effectively remove defects and extend rail life by maintaining optimal wheel-rail contact."
        ),
        reasoning_framework=(
            "Rail grinding is a preventive maintenance process that removes surface defects such as corrugations, head checks, and squats, "
            "restoring the rail profile to optimal geometry. Proper rail profile ensures uniform wheel-rail contact, reducing dynamic forces, "
            "noise, and wear. Grinding also mitigates rolling contact fatigue by removing crack initiation sites. Profiling adjusts rail head "
            "shape to compensate for wear and maintain gauge. The process involves specialized grinding trains equipped with precise measurement "
            "and control systems. The reasoning incorporates materials science, tribology, and mechanical engineering. Studies show that "
            "regular grinding reduces maintenance costs and improves ride quality. AREMA and FRA provide guidelines on grinding frequency and "
            "techniques. Improper grinding can damage rails or accelerate defects."
        ),
        key_factors=[
            "Grinding frequency and scheduling",
            "Rail defect types and severity",
            "Grinding techniques and equipment",
            "Rail profile standards",
            "Impact on wheel-rail contact mechanics",
            "Noise and vibration reduction",
            "Safety and environmental considerations",
            "Compliance with FRA and AREMA guidelines"
        ],
        primary_authority=[
            "AREMA Manual for Railway Engineering - Rail Grinding Chapter",
            "FRA Track Safety Standards",
            "Transportation Research Board Rail Grinding Studies",
            "Railway Association of North America Maintenance Best Practices",
            "Federal Railroad Administration Safety Advisories"
        ],
        burden_holder="Track Maintenance Departments",
        adversary_position=(
            "Some argue grinding costs and service interruptions outweigh benefits."
        ),
        counter_arguments=[
            "Grinding prevents costly rail failures",
            "Improves ride quality and reduces noise",
            "Extends rail service life",
            "Regulatory guidelines support preventive grinding",
            "Reduces dynamic forces and maintenance needs"
        ],
        resolution_strategy=(
            "Implement condition-based grinding programs using rail defect monitoring data."
        ),
        entity_scope="Track Maintenance and Engineering",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA Enforcement and Industry Case Studies on Rail Grinding"
    ),
    DoctrineBlock(
        topic="Wheel-Rail Interaction: Contact Mechanics, Creep, and Adhesion",
        keywords=["wheel-rail interaction", "contact mechanics", "creep", "adhesion", "friction", "wear", "dynamics"],
        conclusion_template=(
            "Understanding wheel-rail interaction mechanics is essential to optimize adhesion, minimize wear, and ensure safe train operations."
        ),
        reasoning_framework=(
            "The wheel-rail interface is a complex contact zone where mechanical forces, friction, and material properties interact. "
            "Contact mechanics govern the stress distribution and deformation at the interface. Creep refers to the micro-slip between "
            "wheel and rail surfaces, generating traction forces necessary for acceleration and braking. Adhesion depends on surface "
            "conditions, contamination, and material properties. Excessive creep leads to wear, rolling contact fatigue, and noise. "
            "Dynamic forces from track irregularities and vehicle suspensions influence contact conditions. Research in tribology and "
            "vehicle dynamics informs maintenance practices such as lubrication, rail grinding, and wheel profiling. The reasoning "
            "integrates mechanical engineering, materials science, and physics. Optimizing adhesion improves energy efficiency and safety. "
            "Standards and guidelines from AREMA and FRA provide operational thresholds."
        ),
        key_factors=[
            "Contact patch size and stress distribution",
            "Creep force generation and limits",
            "Surface roughness and contamination",
            "Lubrication and friction modifiers",
            "Wear mechanisms and fatigue crack initiation",
            "Dynamic loading and vibration effects",
            "Material properties of wheel and rail",
            "Environmental factors (weather, debris)"
        ],
        primary_authority=[
            "AREMA Manual for Railway Engineering - Wheel-Rail Interaction Chapter",
            "Transportation Research Board Wheel-Rail Interaction Studies",
            "FRA Track Safety Standards",
            "International Union of Railways (UIC) Leaflets",
            "Railway Technical Research Institute (RTRI) Publications"
        ],
        burden_holder="Vehicle and Track Engineering Departments",
        adversary_position=(
            "Some claim that adhesion issues are primarily operational and cannot be engineered."
        ),
        counter_arguments=[
            "Engineering controls significantly influence adhesion",
            "Maintenance practices mitigate wear and fatigue",
            "Material selection affects contact mechanics",
            "Environmental management reduces contamination",
            "Operational procedures complement engineering solutions"
        ],
        resolution_strategy=(
            "Integrate vehicle and track maintenance with environmental controls and operational protocols."
        ),
        entity_scope="Vehicle Dynamics and Track Engineering",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FRA Safety Advisories and Research Board Publications"
    ),
    DoctrineBlock(
        topic="Coupler Systems: Draft Gear, Knuckle, and Buff Force Analysis",
        keywords=["coupler", "draft gear", "knuckle", "drawbar", "buff force", "impact", "dynamic loads", "AAR"],
        conclusion_template=(
            "Proper design and maintenance of coupler systems and draft gear are critical to manage buff forces and ensure train integrity."
        ),
        reasoning_framework=(
            "Railcar couplers connect cars and transmit forces during train operations. The knuckle coupler is the standard design, "
            "allowing automatic coupling and uncoupling. Draft gear absorbs impact forces (buff forces) during coupling and train "
            "acceleration or braking. Buff force analysis involves evaluating dynamic loads transmitted through couplers to prevent "
            "damage or derailment. Excessive buff forces can cause structural failures or slack action leading to train handling issues. "
            "AAR standards specify coupler strength, draft gear performance, and inspection criteria. The reasoning includes mechanical "
            "engineering, dynamics, and materials science. Proper maintenance ensures coupler alignment, lubrication, and draft gear "
            "functionality. Failure to manage buff forces has been implicated in multiple accident investigations."
        ),
        key_factors=[
            "Coupler design and strength ratings",
            "Draft gear energy absorption capacity",
            "Dynamic buff force magnitudes",
            "Inspection and maintenance intervals",
            "Slack action and train handling",
            "Material fatigue and wear",
            "Compatibility with rolling stock",
            "Regulatory compliance (AAR)"
        ],
        primary_authority=[
            "AAR Manual of Standards and Recommended Practices",
            "FRA Motive Power and Equipment Safety Standards",
            "Transportation Research Board Coupler Dynamics Studies",
            "National Transportation Safety Board (NTSB) Accident Reports",
            "Railway Association of North America Maintenance Guidelines"
        ],
        burden_holder="Rolling Stock Maintenance and Operations",
        adversary_position=(
            "Some operators minimize coupler maintenance to reduce downtime."
        ),
        counter_arguments=[
            "Poor maintenance increases risk of failures",
            "Regulatory inspections enforce standards",
            "Proper draft gear reduces impact damage",
            "Improved train handling enhances safety",
            "Failure consequences are severe and costly"
        ],
        resolution_strategy=(
            "Implement scheduled inspections, maintenance, and operator training on slack management."
        ),
        entity_scope="Rolling Stock Maintenance and Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FRA Enforcement and NTSB Coupler Failure Investigations"
    ),
    DoctrineBlock(
        topic="Air Brake Systems: Train Line Control and Emergency Brake Application",
        keywords=["air brake system", "train line", "control valve", "emergency brake", "pressure", "FRA", "maintenance"],
        conclusion_template=(
            "Reliable air brake system control and emergency brake functionality are essential for train safety and regulatory compliance."
        ),
        reasoning_framework=(
            "The air brake system is the primary train braking mechanism, using compressed air to apply and release brakes on each car. "
            "The train line pressure controls brake application via control valves on locomotives and cars. Emergency brake application "
            "occurs when train line pressure drops rapidly, triggering full brake application. Proper system design ensures fail-safe "
            "operation and redundancy. Maintenance includes inspection of reservoirs, valves, brake cylinders, and piping for leaks "
            "and wear. FRA regulations (49 CFR Part 232) specify testing, inspection, and performance standards. The reasoning involves "
            "fluid dynamics, mechanical engineering, and safety systems analysis. Failures in air brake systems have caused accidents, "
            "highlighting the need for rigorous maintenance and operational procedures."
        ),
        key_factors=[
            "Train line pressure and control valve function",
            "Brake cylinder performance and leakage",
            "Emergency brake application triggers",
            "Inspection and testing intervals",
            "System redundancy and fail-safe design",
            "Operator training and procedures",
            "Regulatory compliance (FRA Part 232)",
            "Maintenance documentation and reporting"
        ],
        primary_authority=[
            "49 CFR Part 232 - Brake System Safety Standards",
            "Association of American Railroads Air Brake Manual",
            "FRA Safety Advisories on Brake System Failures",
            "Transportation Research Board Brake System Studies",
            "Federal Railroad Administration Inspection Guidelines"
        ],
        burden_holder="Locomotive and Rolling Stock Maintenance",
        adversary_position=(
            "Some operators delay brake system maintenance to reduce costs."
        ),
        counter_arguments=[
            "Brake failures pose severe safety risks",
            "Regulatory mandates require compliance",
            "Proper maintenance extends system reliability",
            "Emergency brake functionality is critical",
            "Safety incidents lead to high penalties"
        ],
        resolution_strategy=(
            "Enforce strict maintenance schedules, operator training, and compliance audits."
        ),
        entity_scope="Train Brake Systems and Maintenance",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="FRA Enforcement Actions and NTSB Brake Failure Investigations"
    ),
    DoctrineBlock(
        topic="Rail Transportation Economics: Rate, Tariff, Revenue, and Costing",
        keywords=["rail transportation", "economics", "rate", "tariff", "revenue", "costing", "STB", "pricing"],
        conclusion_template=(
            "Effective rail transportation economics management balances rates, tariffs, and costs to ensure profitability and regulatory compliance."
        ),
        reasoning_framework=(
            "Rail transportation economics involves setting rates and tariffs that recover costs, generate revenue, and remain competitive. "
            "Costing includes fixed infrastructure, variable operational costs, and capital investments. The Surface Transportation Board (STB) "
            "regulates rate reasonableness and tariff filings to prevent anti-competitive practices. Economic models incorporate demand elasticity, "
            "service quality, and market conditions. Revenue management strategies optimize asset utilization and pricing. Regulatory compliance "
            "requires transparent accounting and reporting. The reasoning integrates microeconomics, regulatory policy, and financial analysis. "
            "Balancing cost recovery with customer affordability is critical for sustainable operations."
        ),
        key_factors=[
            "Rate setting methodologies",
            "Tariff structures and classifications",
            "Cost allocation and accounting",
            "Revenue management strategies",
            "Regulatory compliance (STB)",
            "Market competition and demand elasticity",
            "Service quality and reliability",
            "Capital investment and depreciation"
        ],
        primary_authority=[
            "Surface Transportation Board (STB) Regulations",
            "Interstate Commerce Act",
            "Association of American Railroads Economic Reports",
            "Transportation Research Board Economic Studies",
            "Federal Railroad Administration Financial Oversight"
        ],
        burden_holder="Railroad Financial and Regulatory Departments",
        adversary_position=(
            "Shippers may argue rates are excessive or discriminatory."
        ),
        counter_arguments=[
            "Rates reflect cost and market conditions",
            "Regulatory oversight ensures fairness",
            "Service quality justifies pricing",
            "Transparent accounting supports rate setting",
            "Competitive markets discipline pricing"
        ],
        resolution_strategy=(
            "Engage in transparent rate filings, stakeholder consultations, and regulatory compliance."
        ),
        entity_scope="Railroad Economics and Regulatory Affairs",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="STB Rate Cases and Interstate Commerce Commission Precedents"
    ),
    DoctrineBlock(
        topic="Environmental Impact: Railroad Noise, Vibration, and Emissions Mitigation",
        keywords=["environmental", "noise", "vibration", "emissions", "mitigation", "EPA", "FRA", "community impact"],
        conclusion_template=(
            "Implementing noise, vibration, and emissions mitigation strategies minimizes environmental impact and improves community relations."
        ),
        reasoning_framework=(
            "Railroads generate environmental impacts including noise from wheel-rail contact and horns, ground vibration from train passage, "
            "and emissions from diesel locomotives. Regulatory agencies such as the Environmental Protection Agency (EPA) and FRA set standards "
            "and guidelines for acceptable levels. Noise barriers, rail lubrication, and wheel maintenance reduce noise and vibration. "
            "Emission controls include Tier 4 compliant engines, idling restrictions, and alternative fuels. Environmental impact assessments "
            "evaluate effects on communities and ecosystems. The reasoning integrates environmental engineering, acoustics, and regulatory policy. "
            "Mitigation strategies balance operational needs with environmental stewardship. Community engagement and monitoring programs "
            "support compliance and social license to operate."
        ),
        key_factors=[
            "Noise source identification and measurement",
            "Vibration transmission and attenuation",
            "Locomotive emission standards (EPA Tier 4)",
            "Mitigation technologies and practices",
            "Regulatory compliance and reporting",
            "Community impact assessments",
            "Monitoring and enforcement mechanisms",
            "Sustainability and corporate responsibility"
        ],
        primary_authority=[
            "EPA Locomotive Emission Standards",
            "FRA Noise and Vibration Guidelines",
            "National Environmental Policy Act (NEPA)",
            "Transportation Research Board Environmental Studies",
            "Federal Transit Administration Environmental Guidance"
        ],
        burden_holder="Railroad Environmental Compliance Departments",
        adversary_position=(
            "Some operators minimize mitigation to reduce costs."
        ),
        counter_arguments=[
            "Regulatory mandates require mitigation",
            "Community opposition affects operations",
            "Mitigation improves public health",
            "Sustainability goals support investments",
            "Long-term benefits outweigh costs"
        ],
        resolution_strategy=(
            "Develop comprehensive environmental management plans and invest in mitigation technologies."
        ),
        entity_scope="Environmental Compliance and Community Relations",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="EPA Enforcement Actions and FRA Environmental Reviews"
    ),
    DoctrineBlock(
        topic="Railroad Regulation: STB, FRA, AAR Interchange Rules",
        keywords=["railroad regulation", "STB", "FRA", "AAR", "interchange rules", "compliance", "safety", "operations"],
        conclusion_template=(
            "Compliance with STB, FRA, and AAR regulations and interchange rules is mandatory for safe and efficient railroad operations."
        ),
        reasoning_framework=(
            "Railroad operations are governed by multiple regulatory bodies. The Surface Transportation Board (STB) oversees economic regulation including rates and service. "
            "The Federal Railroad Administration (FRA) regulates safety standards for track, equipment, and operations. The Association of American Railroads (AAR) "
            "develops interchange rules facilitating equipment and freight interchange among carriers. Compliance ensures safety, interoperability, and fair competition. "
            "Regulations cover inspection, maintenance, reporting, and operational procedures. Non-compliance results in penalties and operational restrictions. "
            "The reasoning involves legal analysis, regulatory policy, and operational management. Coordination among regulatory agencies and industry stakeholders "
            "supports consistent enforcement and continuous improvement."
        ),
        key_factors=[
            "STB economic regulations and rate oversight",
            "FRA safety standards and enforcement",
            "AAR interchange rules and equipment standards",
            "Reporting and documentation requirements",
            "Inspection and maintenance compliance",
            "Training and certification standards",
            "Incident investigation and response",
            "Interagency coordination"
        ],
        primary_authority=[
            "Surface Transportation Board Regulations",
            "Federal Railroad Administration Regulations (49 CFR Parts 200-299)",
            "Association of American Railroads Interchange Rules",
            "Rail Safety Improvement Act of 2008",
            "National Transportation Safety Board (NTSB) Recommendations"
        ],
        burden_holder="Railroad Compliance and Legal Departments",
        adversary_position=(
            "Some operators challenge regulatory interpretations or enforcement."
        ),
        counter_arguments=[
            "Regulations are legally binding",
            "Safety and economic benefits justify rules",
            "Enforcement ensures industry standards",
            "Stakeholder engagement improves regulations",
            "Legal precedents support regulatory authority"
        ],
        resolution_strategy=(
            "Maintain proactive compliance programs and engage in regulatory dialogue."
        ),
        entity_scope="Railroad Regulatory Compliance",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="Federal Court Decisions Upholding FRA and STB Authority"
    ),
    DoctrineBlock(
        topic="Track Maintenance: Tamping, Surfacing, Ballast Undercutting",
        keywords=["track maintenance", "tamping", "surfacing", "ballast", "undercutting", "track geometry", "FRA", "AREMA"],
        conclusion_template=(
            "Regular track maintenance including tamping, surfacing, and ballast undercutting maintains track geometry and ensures safe operations."
        ),
        reasoning_framework=(
            "Track maintenance activities such as tamping and surfacing restore track geometry by correcting alignment, cross-level, and profile deviations. "
            "Tamping machines compact ballast under sleepers to stabilize track position. Ballast undercutting removes fouled ballast and restores drainage. "
            "Proper ballast condition supports track loads and prevents settlement. AREMA and FRA provide maintenance standards and tolerances. "
            "Maintenance frequency depends on traffic, track class, and environmental conditions. The reasoning integrates geotechnical engineering, "
            "mechanical engineering, and safety management. Effective maintenance prevents track failures, reduces derailment risk, and extends infrastructure life."
        ),
        key_factors=[
            "Track geometry measurement and tolerances",
            "Tamping machine capabilities and procedures",
            "Ballast condition and drainage",
            "Maintenance scheduling and prioritization",
            "Environmental impacts on track stability",
            "Inspection and defect detection",
            "Safety protocols during maintenance",
            "Regulatory compliance"
        ],
        primary_authority=[
            "AREMA Manual for Railway Engineering - Track Maintenance Chapters",
            "FRA Track Safety Standards",
            "Transportation Research Board Track Maintenance Studies",
            "Federal Railroad Administration Maintenance Guidelines",
            "Railway Association of North America Best Practices"
        ],
        burden_holder="Track Maintenance Departments",
        adversary_position=(
            "Some operators defer maintenance citing cost and operational disruptions."
        ),
        counter_arguments=[
            "Deferred maintenance increases safety risks",
            "Regulatory mandates require adherence",
            "Proper maintenance extends track life",
            "Improves ride quality and reduces costs",
            "Safety incidents have high consequences"
        ],
        resolution_strategy=(
            "Implement condition-based maintenance and optimize scheduling to minimize disruptions."
        ),
        entity_scope="Track Maintenance and Engineering",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA Enforcement and Industry Case Studies"
    ),
    DoctrineBlock(
        topic="Locomotive Fuel Efficiency: Trip Optimizer and Energy Management Systems",
        keywords=["locomotive", "fuel efficiency", "trip optimizer", "energy management system", "EMS", "cruise control", "emissions"],
        conclusion_template=(
            "Deploying trip optimizer and energy management systems enhances locomotive fuel efficiency and reduces emissions."
        ),
        reasoning_framework=(
            "Locomotive trip optimizer systems use algorithms to regulate throttle and dynamic braking to minimize fuel consumption while maintaining schedule adherence. "
            "Energy Management Systems (EMS) integrate data from train consist, track profile, and real-time conditions to optimize power usage. "
            "Cruise control maintains efficient speeds on varying grades. These systems reduce fuel costs and emissions, contributing to environmental goals. "
            "The reasoning involves control systems engineering, thermodynamics, and operational research. Studies demonstrate significant fuel savings and emission reductions. "
            "Integration with locomotive control systems and operator training are critical. Regulatory incentives encourage adoption. "
            "Challenges include system complexity and interoperability with legacy equipment."
        ),
        key_factors=[
            "Algorithm accuracy and adaptability",
            "Integration with locomotive controls",
            "Operator acceptance and training",
            "Track profile and grade data accuracy",
            "Fuel consumption and emission metrics",
            "Maintenance and system reliability",
            "Regulatory incentives and compliance",
            "Cost-benefit analysis"
        ],
        primary_authority=[
            "EPA Locomotive Emission Regulations",
            "Association of American Railroads Fuel Efficiency Reports",
            "Transportation Research Board Energy Management Studies",
            "Federal Railroad Administration Technology Demonstrations",
            "Locomotive Manufacturer Technical Specifications"
        ],
        burden_holder="Locomotive Operations and Engineering",
        adversary_position=(
            "Some operators resist adoption due to perceived complexity and upfront costs."
        ),
        counter_arguments=[
            "Fuel savings justify investment",
            "Emission reductions meet regulatory goals",
            "Improved operational consistency",
            "Positive environmental impact",
            "Technological maturity reduces risks"
        ],
        resolution_strategy=(
            "Implement phased adoption with operator training and performance monitoring."
        ),
        entity_scope="Locomotive Operations and Engineering",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="EPA and FRA Technology Adoption Programs"
    ),
    DoctrineBlock(
        topic="Derailment Investigation: Root Cause Analysis of Track and Vehicle Interaction",
        keywords=["derailment", "investigation", "root cause", "track-vehicle interaction", "FRA", "NTSB", "failure analysis"],
        conclusion_template=(
            "Comprehensive derailment investigations focusing on track and vehicle interaction identify root causes and inform prevention strategies."
        ),
        reasoning_framework=(
            "Derailment investigations analyze physical evidence, track conditions, vehicle dynamics, and operational factors to determine root causes. "
            "Track-vehicle interaction is a critical focus area, examining track geometry, rail defects, wheel conditions, and dynamic forces. "
            "FRA and NTSB protocols guide evidence collection, data analysis, and reporting. Investigations use simulations, metallurgical analysis, "
            "and human factors evaluation. The reasoning integrates forensic engineering, materials science, and safety management. "
            "Findings inform corrective actions, regulatory enforcement, and industry best practices. Accurate root cause identification prevents recurrence "
            "and improves safety culture."
        ),
        key_factors=[
            "Track geometry and condition at derailment site",
            "Vehicle wheel and suspension condition",
            "Dynamic forces and train handling",
            "Human factors and operational context",
            "Environmental and weather conditions",
            "Maintenance and inspection history",
            "Data from event recorders and sensors",
            "Regulatory compliance and reporting"
        ],
        primary_authority=[
            "FRA Derailment Investigation Procedures",
            "National Transportation Safety Board (NTSB) Accident Reports",
            "Transportation Research Board Derailment Studies",
            "Federal Railroad Administration Safety Advisories",
            "Railway Association of North America Investigation Guidelines"
        ],
        burden_holder="Railroad Safety and Engineering Departments",
        adversary_position=(
            "Operators may dispute findings or attribute causes to external factors."
        ),
        counter_arguments=[
            "Objective evidence supports root cause findings",
            "Regulatory oversight ensures thorough investigations",
            "Corrective actions improve safety",
            "Transparency builds public trust",
            "Lessons learned prevent future incidents"
        ],
        resolution_strategy=(
            "Conduct multidisciplinary investigations with independent oversight and implement recommendations."
        ),
        entity_scope="Railroad Safety and Accident Investigation",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="FRA and NTSB Derailment Investigation Reports"
    ),
    DoctrineBlock(
        topic="Hazardous Materials Transportation: Placarding, Routing, and Emergency Response",
        keywords=["hazmat", "transportation", "placard", "routing", "emergency response", "DOT", "FRA", "49 CFR"],
        conclusion_template=(
            "Compliance with hazmat placarding, routing, and emergency response protocols ensures safe transportation of hazardous materials by rail."
        ),
        reasoning_framework=(
            "Transportation of hazardous materials by rail is strictly regulated to prevent accidents and mitigate consequences. "
            "Placarding provides visual identification of hazardous cargo per DOT regulations (49 CFR Parts 172 and 174). "
            "Routing considers population density, environmental sensitivity, and infrastructure constraints to minimize risk. "
            "Emergency response plans coordinate among railroads, local authorities, and federal agencies to manage incidents. "
            "FRA and Pipeline and Hazardous Materials Safety Administration (PHMSA) provide regulatory frameworks. "
            "The reasoning involves regulatory compliance, risk assessment, and emergency management. Proper training, communication, "
            "and equipment are essential. Failure to comply can result in severe penalties and catastrophic incidents."
        ),
        key_factors=[
            "Hazmat classification and placarding requirements",
            "Routing restrictions and approvals",
            "Emergency response planning and coordination",
            "Training and certification of personnel",
            "Incident reporting and investigation",
            "Equipment standards and maintenance",
            "Community right-to-know and notification",
            "Regulatory compliance and enforcement"
        ],
        primary_authority=[
            "49 CFR Parts 172, 174, and 177 - Hazardous Materials Regulations",
            "Federal Railroad Administration Hazmat Safety Guidelines",
            "Pipeline and Hazardous Materials Safety Administration (PHMSA)",
            "National Fire Protection Association (NFPA) Standards",
            "Transportation Security Administration (TSA) Rail Security Regulations"
        ],
        burden_holder="Railroad Hazmat Operations and Safety Departments",
        adversary_position=(
            "Some operators may underreport or inadequately train for hazmat handling."
        ),
        counter_arguments=[
            "Regulatory mandates require compliance",
            "Safety risks are significant",
            "Training reduces incident likelihood",
            "Community safety depends on transparency",
            "Penalties deter non-compliance"
        ],
        resolution_strategy=(
            "Implement rigorous training, compliance audits, and emergency drills."
        ),
        entity_scope="Hazardous Materials Transportation and Safety",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="FRA and PHMSA Enforcement Actions"
    ),
    DoctrineBlock(
        topic="Railroad Communications: Radio, PTC Network, and Dispatch Systems",
        keywords=["railroad communications", "radio", "PTC network", "dispatch", "wireless", "FRA", "safety", "interoperability"],
        conclusion_template=(
            "Robust railroad communications infrastructure supports safe and efficient operations, including PTC and dispatch functions."
        ),
        reasoning_framework=(
            "Railroad communications systems encompass radio networks, PTC data links, and dispatch control centers. "
            "Reliable wireless communication ensures real-time train control, emergency response, and operational coordination. "
            "PTC networks require secure, low-latency data transmission compliant with FRA standards. Dispatch systems manage train movements "
            "and crew assignments. Interoperability among different carriers and equipment is essential. Communications infrastructure "
            "includes base stations, mobile radios, and network management systems. The reasoning involves telecommunications engineering, "
            "cybersecurity, and safety management. Failures in communications have contributed to accidents, underscoring the need for "
            "redundancy and monitoring. Regulatory frameworks govern spectrum use and system certification."
        ),
        key_factors=[
            "Radio frequency allocation and management",
            "Network reliability and redundancy",
            "Data security and encryption",
            "Interoperability standards",
            "Dispatch system integration",
            "Maintenance and monitoring protocols",
            "Regulatory compliance (FRA, FCC)",
            "Training and operational procedures"
        ],
        primary_authority=[
            "Federal Communications Commission (FCC) Regulations",
            "Federal Railroad Administration Communications Standards",
            "Association of American Railroads Communications Guidelines",
            "Transportation Research Board Communications Studies",
            "Railway Safety and Interoperability Regulations"
        ],
        burden_holder="Railroad Communications and Operations Departments",
        adversary_position=(
            "Some operators underinvest in communications infrastructure."
        ),
        counter_arguments=[
            "Reliable communications are critical for safety",
            "Regulatory mandates require compliance",
            "Operational efficiency depends on communications",
            "Cybersecurity protects against threats",
            "Failures have severe consequences"
        ],
        resolution_strategy=(
            "Invest in modern communications technology, implement cybersecurity measures, and conduct regular training."
        ),
        entity_scope="Railroad Communications and Dispatch",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA Communications System Enforcement and FCC Regulations"
    ),
    DoctrineBlock(
        topic="Track Construction: New Line Development and Rehabilitation",
        keywords=["track construction", "new line", "rehabilitation", "grade crossing", "earthworks", "ballast", "FRA", "AREMA"],
        conclusion_template=(
            "Adhering to best practices in track construction and rehabilitation ensures infrastructure durability and operational safety."
        ),
        reasoning_framework=(
            "Track construction involves earthworks, subgrade preparation, ballast placement, sleeper installation, and rail laying. "
            "New line development requires alignment studies, environmental assessments, and design compliance with FRA and AREMA standards. "
            "Rehabilitation addresses aging infrastructure through rail replacement, ballast cleaning, and geometry correction. "
            "Grade crossings require special design considerations for safety and accessibility. The reasoning integrates civil engineering, "
            "geotechnical analysis, and construction management. Quality control during construction affects long-term performance. "
            "Coordination with utilities, environmental agencies, and stakeholders is essential. Regulatory compliance includes permits and inspections."
        ),
        key_factors=[
            "Subgrade and earthwork quality",
            "Ballast selection and compaction",
            "Rail and sleeper installation standards",
            "Grade crossing design and safety",
            "Environmental and permitting requirements",
            "Construction quality assurance",
            "Coordination with stakeholders",
            "Regulatory compliance and inspections"
        ],
        primary_authority=[
            "AREMA Manual for Railway Engineering - Track Construction Chapters",
            "Federal Railroad Administration Construction Guidelines",
            "Transportation Research Board Construction Studies",
            "Environmental Protection Agency (EPA) Regulations",
            "Occupational Safety and Health Administration (OSHA) Standards"
        ],
        burden_holder="Railroad Construction and Engineering Departments",
        adversary_position=(
            "Cost pressures may lead to shortcuts in construction quality."
        ),
        counter_arguments=[
            "Poor construction leads to premature failures",
            "Regulatory inspections enforce standards",
            "Quality construction reduces lifecycle costs",
            "Safety depends on construction integrity",
            "Stakeholder expectations require compliance"
        ],
        resolution_strategy=(
            "Implement rigorous quality control, training, and stakeholder engagement."
        ),
        entity_scope="Track Construction and Engineering",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA Construction Compliance and Industry Best Practices"
    ),
    DoctrineBlock(
        topic="Train Dynamics: Longitudinal Forces, Coupler Slack, and Run-In Effects",
        keywords=["train dynamics", "longitudinal forces", "coupler slack", "run-in", "in-train forces", "braking", "acceleration"],
        conclusion_template=(
            "Managing longitudinal forces and coupler slack is essential to prevent equipment damage and ensure train handling safety."
        ),
        reasoning_framework=(
            "Train dynamics involve complex interactions of forces along the train length during acceleration, braking, and slack action. "
            "Coupler slack allows relative movement between cars, but excessive slack or run-in forces can cause impact damage. "
            "Longitudinal forces depend on train mass, grade, speed, and braking effort. Understanding these forces informs train handling procedures "
            "and equipment design. Dynamic simulations and field measurements guide operational limits. The reasoning integrates mechanical engineering, "
            "vehicle dynamics, and safety analysis. Proper train makeup, braking strategies, and operator training mitigate risks. "
            "Standards from AAR and FRA provide guidelines on in-train forces."
        ),
        key_factors=[
            "Train mass and length",
            "Grade and curvature effects",
            "Braking system performance",
            "Coupler slack and draft gear characteristics",
            "Operator handling and procedures",
            "Dynamic force measurement and modeling",
            "Equipment strength and fatigue limits",
            "Regulatory guidelines and limits"
        ],
        primary_authority=[
            "Association of American Railroads Train Handling Manual",
            "FRA Safety Standards on Train Dynamics",
            "Transportation Research Board Train Dynamics Studies",
            "Railway Technical Research Institute (RTRI) Publications",
            "National Transportation Safety Board (NTSB) Accident Reports"
        ],
        burden_holder="Train Operations and Engineering",
        adversary_position=(
            "Some operators underestimate the impact of longitudinal forces."
        ),
        counter_arguments=[
            "Excessive forces cause equipment damage and derailments",
            "Regulatory limits must be observed",
            "Proper training reduces risks",
            "Dynamic modeling improves understanding",
            "Equipment design accommodates expected forces"
        ],
        resolution_strategy=(
            "Implement training, monitoring, and operational procedures to manage longitudinal forces."
        ),
        entity_scope="Train Operations and Engineering",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FRA Enforcement and NTSB Investigations"
    ),
    DoctrineBlock(
        topic="Railroad Bridge Inspection: Load Rating and Capacity Evaluation",
        keywords=["railroad bridge", "inspection", "load rating", "capacity evaluation", "FRA", "NBI", "structural health"],
        conclusion_template=(
            "Regular inspection and load rating of railroad bridges ensure structural integrity and safe train operations."
        ),
        reasoning_framework=(
            "Railroad bridge inspection programs assess structural condition and load carrying capacity. Inspections include visual, "
            "non-destructive testing, and load testing. Load rating evaluates the maximum permissible loads based on structural analysis "
            "and condition data. The National Bridge Inventory (NBI) provides standardized data collection. FRA regulations mandate "
            "inspection frequencies and reporting. Structural health monitoring technologies enhance assessment accuracy. The reasoning "
            "combines civil engineering, materials science, and safety management. Accurate load ratings prevent overloading and failures. "
            "Inspection findings guide maintenance, rehabilitation, or replacement decisions."
        ),
        key_factors=[
            "Inspection methods and intervals",
            "Structural analysis and load rating",
            "Material condition and deterioration",
            "Environmental effects",
            "Load history and traffic patterns",
            "Monitoring technologies",
            "Regulatory compliance",
            "Maintenance and rehabilitation planning"
        ],
        primary_authority=[
            "49 CFR Part 237 - Bridge Safety Standards",
            "National Bridge Inventory (NBI) Guidelines",
            "AASHTO Manual for Railway Engineering",
            "FRA Bridge Safety Program",
            "Transportation Research Board Structural Health Monitoring Studies"
        ],
        burden_holder="Railroad Engineering and Maintenance",
        adversary_position=(
            "Some argue inspection costs are excessive."
        ),
        counter_arguments=[
            "Safety and regulatory compliance justify costs",
            "Early detection prevents catastrophic failures",
            "Load rating ensures operational safety",
            "Monitoring reduces inspection frequency",
            "Maintenance planning optimizes expenditures"
        ],
        resolution_strategy=(
            "Implement risk-based inspection and monitoring programs."
        ),
        entity_scope="Bridge Engineering and Maintenance",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="FRA Bridge Safety Enforcement and NTSB Investigations"
    ),
    DoctrineBlock(
        topic="Tunnel Ventilation, Fire Safety, and Emergency Evacuation",
        keywords=["tunnel", "ventilation", "fire safety", "emergency evacuation", "NFPA", "FRA", "smoke control", "safety systems"],
        conclusion_template=(
            "Effective tunnel ventilation and fire safety systems are critical for safe emergency evacuation and operational continuity."
        ),
        reasoning_framework=(
            "Rail tunnels pose unique risks due to confined spaces and limited egress. Ventilation systems control airflow to manage smoke and heat "
            "in fire scenarios. Fire detection and suppression systems provide early warning and mitigation. Emergency evacuation plans and "
            "infrastructure ensure passenger safety. NFPA 130 and FRA regulations specify design and operational requirements. Engineering "
            "considerations include airflow modeling, smoke extraction, and system redundancy. Coordination with emergency responders is essential. "
            "The reasoning integrates fire protection engineering, mechanical engineering, and safety management. Regular drills and system testing "
            "maintain readiness. Failure to provide adequate systems has led to severe incidents."
        ),
        key_factors=[
            "Ventilation system capacity and control",
            "Fire detection and suppression technologies",
            "Emergency egress routes and signage",
            "Smoke control and extraction",
            "System redundancy and reliability",
            "Coordination with emergency services",
            "Regulatory compliance (NFPA, FRA)",
            "Training and emergency drills"
        ],
        primary_authority=[
            "NFPA 130 - Standard for Fixed Guideway Transit and Passenger Rail Systems",
            "49 CFR Part 238 - Passenger Equipment Safety Standards",
            "Federal Railroad Administration Safety Guidelines",
            "Transportation Research Board Tunnel Safety Studies",
            "National Fire Protection Association Codes"
        ],
        burden_holder="Railroad Safety and Infrastructure Departments",
        adversary_position=(
            "Some operators underinvest in tunnel safety systems."
        ),
        counter_arguments=[
            "Regulatory mandates require compliance",
            "Safety incidents have high human costs",
            "Proper systems reduce operational disruptions",
            "Emergency preparedness builds public confidence",
            "Technological advances improve effectiveness"
        ],
        resolution_strategy=(
            "Invest in system upgrades, training, and coordination with emergency responders."
        ),
        entity_scope="Tunnel Safety and Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA Tunnel Safety Enforcement and Incident Investigations"
    ),
    DoctrineBlock(
        topic="Railroad Cybersecurity: Signal System, PTC Data Protection",
        keywords=["railroad cybersecurity", "signal system", "PTC", "data protection", "network security", "FRA", "NIST", "ICS"],
        conclusion_template=(
            "Robust cybersecurity measures protect railroad signal and PTC systems from cyber threats, ensuring operational safety and data integrity."
        ),
        reasoning_framework=(
            "Railroad signal and PTC systems increasingly rely on digital networks and control systems vulnerable to cyber attacks. "
            "Protecting these critical infrastructures requires implementing cybersecurity frameworks aligned with NIST standards and FRA guidance. "
            "Measures include network segmentation, intrusion detection, encryption, and access controls. Industrial Control Systems (ICS) security "
            "principles apply. Cyber incidents can disrupt operations, compromise safety, and cause financial losses. The reasoning integrates information "
            "security, systems engineering, and risk management. Regulatory agencies emphasize cybersecurity as a component of safety management systems. "
            "Continuous monitoring, incident response planning, and employee training are essential components."
        ),
        key_factors=[
            "Network architecture and segmentation",
            "Access control and authentication",
            "Intrusion detection and prevention",
            "Data encryption and integrity",
            "Incident response and recovery plans",
            "Employee cybersecurity training",
            "Regulatory compliance (FRA, NIST)",
            "Vendor and supply chain security"
        ],
        primary_authority=[
            "Federal Railroad Administration Cybersecurity Guidance",
            "NIST Cybersecurity Framework",
            "Transportation Security Administration (TSA) Rail Security Regulations",
            "Department of Homeland Security ICS-CERT Guidelines",
            "Railway Safety and Security Standards"
        ],
        burden_holder="Railroad IT and Operations Technology Departments",
        adversary_position=(
            "Some organizations underprioritize cybersecurity investments."
        ),
        counter_arguments=[
            "Cyber threats pose real operational risks",
            "Regulatory mandates require compliance",
            "Incident consequences are severe",
            "Proactive security reduces downtime",
            "Industry best practices support investments"
        ],
        resolution_strategy=(
            "Implement comprehensive cybersecurity programs with continuous monitoring and training."
        ),
        entity_scope="Railroad IT and Operations Technology",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FRA Cybersecurity Enforcement and Industry Guidelines"
    ),
    # Additional doctrine blocks would continue similarly to reach 40+ total
]


def get_doctrine_by_topic(topic: str) -> DoctrineBlock:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    raise ValueError(f"Doctrine with topic '{topic}' not found.")


def search_doctrines_by_keyword(keyword: str) -> List[DoctrineBlock]:
    keyword

class SubEngineState(Enum):
    OPEN = auto()
    HALF_OPEN = auto()
    CLOSED = auto()

class SubEngineStatus(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    UNKNOWN = auto()

class RoutingMode(Enum):
    PARALLEL = auto()
    CASCADE = auto()
    SINGLE = auto()

class IssueCategory(Enum):
    TRACK_ENGINEERING = "Track Engineering"
    LOCOMOTIVE_SYSTEMS = "Locomotive Systems"
    SIGNAL_SYSTEMS = "Signal Systems"
    FREIGHT_OPERATIONS = "Freight Operations"
    RAIL_SAFETY = "Rail Safety"
    RAIL_STRUCTURES = "Rail Structures"
    ROLLING_STOCK = "Rolling Stock"
    ELECTRIFICATION = "Electrification"
    TRAIN_CONTROL = "Train Control"
    YARD_OPERATIONS = "Yard Operations"
    PASSENGER_RAIL = "Passenger Rail"
    GENERAL = "General"

class QueryRequest:
    def __init__(self, text: str, user_id: str, mode: RoutingMode = RoutingMode.PARALLEL, metadata: Optional[dict] = None):
        self.text = text
        self.user_id = user_id
        self.mode = mode
        self.metadata = metadata or {}

class RoutingDecision:
    def __init__(self, engines: List[str], categories: List[IssueCategory], mode: RoutingMode, reason: str = ""):
        self.engines = engines
        self.categories = categories
        self.mode = mode
        self.reason = reason

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, categories: List[IssueCategory], priority: int = 1):
        self.engine_id = engine_id
        self.url = url
        self.categories = categories
        self.priority = priority

class SubEngineResponse:
    def __init__(self, engine_id: str, status: SubEngineStatus, data: Any, latency: float, error: Optional[str] = None):
        self.engine_id = engine_id
        self.status = status
        self.data = data
        self.latency = latency
        self.error = error

# --- SubEngine Registry (Mocked) ---

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "RAIL01": SubEngineConfig("RAIL01", "http://rail01/track", [IssueCategory.TRACK_ENGINEERING]),
    "RAIL02": SubEngineConfig("RAIL02", "http://rail02/locomotive", [IssueCategory.LOCOMOTIVE_SYSTEMS]),
    "RAIL03": SubEngineConfig("RAIL03", "http://rail03/signal", [IssueCategory.SIGNAL_SYSTEMS]),
    "RAIL04": SubEngineConfig("RAIL04", "http://rail04/freight", [IssueCategory.FREIGHT_OPERATIONS]),
    "RAIL05": SubEngineConfig("RAIL05", "http://rail05/safety", [IssueCategory.RAIL_SAFETY]),
    "RAIL06": SubEngineConfig("RAIL06", "http://rail06/structures", [IssueCategory.RAIL_STRUCTURES]),
    "RAIL07": SubEngineConfig("RAIL07", "http://rail07/rolling", [IssueCategory.ROLLING_STOCK]),
    "RAIL08": SubEngineConfig("RAIL08", "http://rail08/electrification", [IssueCategory.ELECTRIFICATION]),
    "RAIL09": SubEngineConfig("RAIL09", "http://rail09/traincontrol", [IssueCategory.TRAIN_CONTROL]),
    "RAIL10": SubEngineConfig("RAIL10", "http://rail10/yard", [IssueCategory.YARD_OPERATIONS]),
    "RAIL11": SubEngineConfig("RAIL11", "http://rail11/passenger", [IssueCategory.PASSENGER_RAIL]),
}

# --- Circuit Breaker Implementation ---

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.state = SubEngineState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = 0

    def record_success(self):
        self.failure_count = 0
        if self.state in [SubEngineState.OPEN, SubEngineState.HALF_OPEN]:
            self.state = SubEngineState.CLOSED

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = SubEngineState.OPEN

    def can_attempt(self):
        if self.state == SubEngineState.CLOSED:
            return True
        elif self.state == SubEngineState.OPEN:
            if (time.time() - self.last_failure_time) > self.recovery_timeout:
                self.state = SubEngineState.HALF_OPEN
                return True
            return False
        elif self.state == SubEngineState.HALF_OPEN:
            return True
        return False

    def __repr__(self):
        return f"CircuitBreaker(state={self.state}, failures={self.failure_count})"

# --- SubEngine Health Monitor ---

class SubEngineHealthMonitor:
    def __init__(self, registry: Dict[str, SubEngineConfig], ttl: int = 30):
        self.registry = registry
        self.health_cache: Dict[str, Tuple[SubEngineStatus, float]] = {}
        self.ttl = ttl
        self.circuit_breakers: Dict[str, CircuitBreaker] = {eid: CircuitBreaker() for eid in registry}

    async def _ping_engine(self, url: str, timeout: int = 3) -> SubEngineStatus:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url + "/health", timeout=timeout) as resp:
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
        except Exception as e:
            return SubEngineStatus.UNHEALTHY

    async def check_health(self, engine_id: str) -> SubEngineStatus:
        now = time.time()
        if engine_id in self.health_cache:
            status, ts = self.health_cache[engine_id]
            if now - ts < self.ttl:
                return status
        config = self.registry.get(engine_id)
        if not config:
            return SubEngineStatus.UNKNOWN
        status = await self._ping_engine(config.url)
        self.health_cache[engine_id] = (status, now)
        cb = self.circuit_breakers[engine_id]
        if status == SubEngineStatus.HEALTHY:
            cb.record_success()
        else:
            cb.record_failure()
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
            cb = self.circuit_breakers[eid]
            if not cb.can_attempt():
                continue
            if eid in self.health_cache:
                status, ts = self.health_cache[eid]
                if now - ts < self.ttl and status == SubEngineStatus.HEALTHY:
                    healthy.append(eid)
        return healthy

    def get_circuit_breaker(self, engine_id: str) -> CircuitBreaker:
        return self.circuit_breakers[engine_id]

# --- Query Router ---

class QueryRouter:
    CATEGORY_KEYWORDS = {
        IssueCategory.TRACK_ENGINEERING: ["track", "railbed", "ballast", "alignment", "gauge", "curve", "switch", "turnout"],
        IssueCategory.LOCOMOTIVE_SYSTEMS: ["locomotive", "engine", "traction", "diesel", "electric motor", "prime mover"],
        IssueCategory.SIGNAL_SYSTEMS: ["signal", "interlocking", "wayside", "block", "aspect", "cab signal"],
        IssueCategory.FREIGHT_OPERATIONS: ["freight", "cargo", "consist", "manifest", "waybill", "load", "shipment"],
        IssueCategory.RAIL_SAFETY: ["safety", "incident", "accident", "derailment", "inspection", "compliance"],
        IssueCategory.RAIL_STRUCTURES: ["bridge", "tunnel", "culvert", "viaduct", "structure", "abutment"],
        IssueCategory.ROLLING_STOCK: ["car", "wagon", "coach", "hopper", "tanker", "flatcar", "rolling stock"],
        IssueCategory.ELECTRIFICATION: ["catenary", "overhead", "third rail", "electrification", "substation"],
        IssueCategory.TRAIN_CONTROL: ["atc", "ptc", "train control", "automatic train", "dispatch", "block system"],
        IssueCategory.YARD_OPERATIONS: ["yard", "shunting", "switching", "classification", "hump", "flat yard"],
        IssueCategory.PASSENGER_RAIL: ["passenger", "commuter", "intercity", "high-speed", "ticket", "schedule"],
    }

    def __init__(self, registry: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.registry = registry
        self.health_monitor = health_monitor
        self.routing_rules = []  # Placeholder for advanced rules

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text_l = text.lower()
        matched = set()
        for cat, keywords in self.CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in text_l:
                    matched.add(cat)
        if not matched:
            matched.add(IssueCategory.GENERAL)
        return list(matched)

    def _select_engines(self, categories: List[IssueCategory], mode: RoutingMode) -> List[SubEngineConfig]:
        healthy_eids = self.health_monitor.get_healthy_engines()
        selected = []
        for eid, config in self.registry.items():
            if eid not in healthy_eids:
                continue
            if IssueCategory.GENERAL in categories:
                selected.append(config)
            else:
                if any(cat in config.categories for cat in categories):
                    selected.append(config)
        if mode == RoutingMode.SINGLE and selected:
            selected = [max(selected, key=lambda c: c.priority)]
        return selected

    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        # Placeholder for advanced rules
        # For now, no custom rules, just default
        return []

    def _score_engine_relevance(self, engine: SubEngineConfig, query: QueryRequest) -> float:
        categories = self._classify_domain(query.text)
        score = 0.0
        for cat in categories:
            if cat in engine.categories:
                score += 1.0
        score += engine.priority * 0.1
        return score

    def _handle_engine_failure(self, engine_id: str, error: str) -> List[str]:
        # Fallback: remove failed engine, try others in same category
        failed_config = self.registry.get(engine_id)
        if not failed_config:
            return []
        fallback = []
        for eid, config in self.registry.items():
            if eid == engine_id:
                continue
            if any(cat in config.categories for cat in failed_config.categories):
                cb = self.health_monitor.get_circuit_breaker(eid)
                if cb.can_attempt():
                    fallback.append(eid)
        return fallback

    def route_query(self, query: QueryRequest) -> RoutingDecision:
        categories = self._classify_domain(query.text)
        rule_engines = self._apply_routing_rules(query)
        if rule_engines:
            engines = rule_engines
            reason = "Matched routing rule"
        else:
            selected = self._select_engines(categories, query.mode)
            engines = [c.engine_id for c in selected]
            reason = "Selected by category and health"
        return RoutingDecision(engines, categories, query.mode, reason)

# --- SubEngine Orchestrator ---

class SubEngineOrchestrator:
    def __init__(self, registry: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.registry = registry
        self.health_monitor = health_monitor
        self.logger = logging.getLogger("SubEngineOrchestrator")

    async def _call_sub_engine(self, engine_config: SubEngineConfig, query: QueryRequest) -> SubEngineResponse:
        cb = self.health_monitor.get_circuit_breaker(engine_config.engine_id)
        if not cb.can_attempt():
            return SubEngineResponse(engine_config.engine_id, SubEngineStatus.UNHEALTHY, None, 0, "Circuit open")
        url = engine_config.url + "/query"
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "text": query.text,
                    "user_id": query.user_id,
                    "metadata": query.metadata
                }
                async with session.post(url, json=payload, timeout=10) as resp:
                    latency = time.time() - start
                    if resp.status == 200:
                        data = await resp.json()
                        cb.record_success()
                        return SubEngineResponse(engine_config.engine_id, SubEngineStatus.HEALTHY, data, latency)
                    else:
                        cb.record_failure()
                        return SubEngineResponse(engine_config.engine_id, SubEngineStatus.UNHEALTHY, None, latency, f"HTTP {resp.status}")
        except Exception as e:
            cb.record_failure()
            latency = time.time() - start
            return SubEngineResponse(engine_config.engine_id, SubEngineStatus.UNHEALTHY, None, latency, str(e))

    async def dispatch_query(self, query: QueryRequest, engines: List[str]) -> List[SubEngineResponse]:
        configs = [self.registry[eid] for eid in engines if eid in self.registry]
        responses = []
        for config in configs:
            resp = await self._call_sub_engine(config, query)
            responses.append(resp)
        return responses

    async def dispatch_parallel(self, query: QueryRequest, engines: List[str]) -> Dict[str, Any]:
        configs = [self.registry[eid] for eid in engines if eid in self.registry]
        tasks = [self._call_sub_engine(config, query) for config in configs]
        responses = await asyncio.gather(*tasks)
        return self._merge_responses(responses)

    async def dispatch_cascade(self, query: QueryRequest, engines: List[str]) -> Any:
        configs = [self.registry[eid] for eid in engines if eid in self.registry]
        for config in configs:
            resp = await self._call_sub_engine(config, query)
            if resp.status == SubEngineStatus.HEALTHY and resp.data:
                return resp.data
        return {"error": "No successful response from cascade"}

    def _merge_responses(self, responses: List[SubEngineResponse]) -> Dict[str, Any]:
        merged = {}
        for resp in responses:
            merged[resp.engine_id] = {
                "status": resp.status.name,
                "latency": resp.latency,
                "data": resp.data,
                "error": resp.error
            }
        consensus = self._resolve_conflicts(responses)
        merged["consensus"] = consensus
        return merged

    def _resolve_conflicts(self, responses: List[SubEngineResponse]) -> Any:
        # Simple consensus: majority answer, or first non-error
        valid = [r for r in responses if r.status == SubEngineStatus.HEALTHY and r.data]
        if not valid:
            return {"error": "No valid responses"}
        # Try to find majority answer
        answer_counts = defaultdict(int)
        answer_map = {}
        for r in valid:
            key = str(r.data)
            answer_counts[key] += 1
            answer_map[key] = r.data
        max_count = max(answer_counts.values())
        consensus_keys = [k for k, v in answer_counts.items() if v == max_count]
        # Return the most common answer
        return answer_map[consensus_keys[0]]

# --- END OF PART 3 ---

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
    AuthorityLevel.CASE_LAW: 50,
    AuthorityLevel.TREATISE: 30,
    AuthorityLevel.PRACTICE: 10,
}

def resolve_authority_conflict(sources):
    """
    sources: list of tuples (authority_level: AuthorityLevel, source_id: str)
    Returns dominant authority source_id with highest weight.
    """
    if not sources:
        return None
    max_weight = -1
    dominant_source = None
    for level, source_id in sources:
        weight = authority_weights.get(level, 0)
        if weight > max_weight:
            max_weight = weight
            dominant_source = source_id
    return dominant_source

# -------------------------------
# EPISTEMIC GUARDRAILS
# -------------------------------

BANNED_PHRASES = [
    "clearly", "obviously", "without doubt", "undeniably", "unquestionably",
    "beyond question", "incontrovertibly", "manifestly", "patently", "evidently",
    "plainly", "decidedly", "categorically", "indisputably", "irrefutably",
    "unequivocally", "incontestably", "absolutely", "definitely", "surely",
    "infallibly", "inarguably", "beyond dispute", "without fail", "no doubt",
    "no question", "undoubtedly", "incontrovertible", "incontestable", "incontestably",
    "beyond any doubt", "without reservation", "without exception"
]

BANNED_PHRASES_PATTERN = re.compile(
    r'\b(' + '|'.join(re.escape(p) for p in BANNED_PHRASES) + r')\b', re.IGNORECASE
)

class ConfidenceLevel(Enum):
    DEFENSIBLE = 1
    AGGRESSIVE = 2
    DISCLOSURE = 3
    HIGH_RISK = 4

def apply_epistemic_guardrails(text):
    """
    Remove banned phrases and append disclosure caveat if any removed.
    """
    cleaned_text, n = BANNED_PHRASES_PATTERN.subn('', text)
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()
    disclosure_caveat = ""
    if n > 0:
        disclosure_caveat = "\n\n[Note: Certain absolute or overly confident terms were removed to maintain epistemic humility.]"
    return cleaned_text + disclosure_caveat

def confidence_stratification(score):
    """
    score: float 0-1 confidence score
    Returns ConfidenceLevel
    """
    if score >= 0.9:
        return ConfidenceLevel.DEFENSIBLE
    elif score >= 0.75:
        return ConfidenceLevel.AGGRESSIVE
    elif score >= 0.5:
        return ConfidenceLevel.DISCLOSURE
    else:
        return ConfidenceLevel.HIGH_RISK

# -------------------------------
# DEEP ANALYSIS
# -------------------------------

def multi_doctrine_decomposition(query):
    """
    Decompose query into sub-issues based on doctrine keywords and patterns.
    Returns list of sub-issue strings.
    """
    # Example simplistic decomposition based on keywords
    keywords = [
        "liability", "negligence", "contract", "damages", "jurisdiction",
        "statute of limitations", "due process", "evidence", "intent",
        "breach", "causation", "remedies", "defenses", "standing",
        "preemption", "sovereign immunity", "arbitration", "waiver",
        "estoppel", "agency", "property", "tort", "criminal", "civil",
        "procedure", "jurisprudence", "precedent", "statutory interpretation",
        "regulation", "constitutionality", "enforcement", "liability",
        "contract formation", "contract performance", "contract breach",
        "damages calculation", "punitive damages", "compensatory damages",
        "injunction", "declaratory relief", "class action", "discovery",
        "summary judgment", "trial", "appeal", "remand"
    ]
    query_lower = query.lower()
    issues = []
    for kw in keywords:
        if kw in query_lower:
            issues.append(kw)
    if not issues:
        issues.append("general inquiry")
    return issues

def build_interaction_dag(issues):
    """
    Build dependency graph (DAG) of issues.
    Returns dict: {issue: set(dependent_issues)}
    """
    # Simplistic static dependencies for demo
    dependencies = {
        "contract breach": {"contract formation", "contract performance"},
        "damages calculation": {"contract breach", "liability"},
        "liability": {"negligence", "intent"},
        "negligence": {"duty", "breach"},
        "breach": {"contract formation"},
        "injunction": {"remedies"},
        "appeal": {"trial"},
        "trial": {"discovery", "summary judgment"},
        "summary judgment": {"discovery"},
    }
    dag = defaultdict(set)
    for issue in issues:
        deps = dependencies.get(issue, set())
        filtered_deps = set(d for d in deps if d in issues)
        dag[issue] = filtered_deps
    return dag

def eight_step_resolution(query, doctrines, sub_engine_results):
    """
    Perform full analysis combining query, doctrines, and sub-engine results.
    Returns comprehensive analysis string.
    """
    # Steps (simplified):
    # 1. Identify issues
    # 2. Gather relevant doctrines
    # 3. Analyze facts
    # 4. Evaluate authority levels
    # 5. Cross-check sub-engine outputs
    # 6. Resolve conflicts
    # 7. Formulate conclusions
    # 8. Apply epistemic guardrails

    issues = multi_doctrine_decomposition(query)
    dag = build_interaction_dag(issues)

    # Aggregate sub-engine results by issue
    aggregated_results = defaultdict(list)
    for res in sub_engine_results:
        for issue, analysis in res.items():
            aggregated_results[issue].append(analysis)

    # Resolve conflicts by authority for each issue
    final_analysis = {}
    for issue in issues:
        analyses = aggregated_results.get(issue, [])
        if not analyses:
            final_analysis[issue] = "No analysis available."
            continue
        # Simplified: pick analysis with highest authority
        best = None
        best_weight = -1
        for analysis in analyses:
            sources = analysis.get("sources", [])
            dominant_source = resolve_authority_conflict(sources)
            level = None
            for lvl, src in sources:
                if src == dominant_source:
                    level = lvl
                    break
            weight = authority_weights.get(level, 0)
            if weight > best_weight:
                best_weight = weight
                best = analysis.get("text", "")
        if best is None:
            best = analyses[0].get("text", "")
        final_analysis[issue] = best

    # Compose final text
    composed = []
    for issue in issues:
        composed.append(f"Issue: {issue}\nAnalysis: {final_analysis.get(issue, '')}\n")

    combined_text = "\n".join(composed)
    cleaned_text = apply_epistemic_guardrails(combined_text)
    return cleaned_text

def zoned_analysis(conclusion):
    """
    Tag conclusion with zones: PLANNING, REPORTING, AUDIT
    Returns dict {zone: tagged_text}
    """
    zones = {
        "PLANNING": "[PLANNING] " + conclusion,
        "REPORTING": "[REPORTING] " + conclusion,
        "AUDIT": "[AUDIT] " + conclusion,
    }
    return zones

# -------------------------------
# FACT FRAGILITY SCORING
# -------------------------------

def score_fact_fragility(fact):
    """
    fact: dict with keys 'verifiability', 'recharacterization_risk', 'testimony_dependence'
    Each value 0-1 float.
    Returns dict with fragility scores.
    """
    verifiability = fact.get('verifiability', 0.5)
    rechar_risk = fact.get('recharacterization_risk', 0.5)
    testimony_dep = fact.get('testimony_dependence', 0.5)

    # Fragility increases with low verifiability, high rechar risk, high testimony dependence
    fragility_score = (1 - verifiability) * 0.4 + rechar_risk * 0.4 + testimony_dep * 0.2
    fragility_score = min(max(fragility_score, 0), 1)

    return {
        "verifiability": verifiability,
        "recharacterization_risk": rechar_risk,
        "testimony_dependence": testimony_dep,
        "fragility_score": fragility_score
    }

# -------------------------------
# SEMANTIC NORMALIZATION
# -------------------------------

DOMAIN_TERM_MAPPINGS = {
    "plaintiff": "claimant",
    "defendant": "respondent",
    "contract breach": "breach of contract",
    "statute of limitations": "limitation period",
    "damages": "compensatory damages",
    "negligence": "tort negligence",
    "liability": "legal responsibility",
    "injunction": "equitable relief",
    "appeal": "judicial review",
    "trial": "court hearing",
    "evidence": "proof material",
    "jurisdiction": "legal authority",
    "due process": "procedural fairness",
    "breach": "violation",
    "remedies": "legal remedies",
    "defenses": "legal defenses",
    "standing": "legal capacity",
    "preemption": "federal preemption",
    "sovereign immunity": "government immunity",
    "arbitration": "alternative dispute resolution",
    "waiver": "voluntary relinquishment",
    "estoppel": "legal estoppel",
    "agency": "principal-agent relationship",
    "property": "real property",
    "tort": "civil wrong",
    "criminal": "criminal offense",
    "civil": "civil matter",
    "procedure": "legal procedure",
    "jurisprudence": "legal theory",
    "precedent": "binding authority",
    "statutory interpretation": "law interpretation",
    "regulation": "administrative rule",
    "constitutionality": "constitutional validity",
    "enforcement": "law enforcement",
    "contract formation": "contract creation",
    "contract performance": "contract execution",
    "punitive damages": "exemplary damages",
    "compensatory damages": "actual damages",
    "declaratory relief": "declaratory judgment",
    "class action": "group litigation",
    "discovery": "pre-trial evidence gathering",
    "summary judgment": "pre-trial ruling",
    "remand": "case return",
    "damages calculation": "damage assessment",
    "intent": "mens rea",
    "causation": "cause in fact",
    "liability insurance": "risk coverage",
    "settlement": "case resolution",
    "litigation": "legal proceeding",
    "juror": "trial jury member",
    "testimony": "witness statement",
    "cross-examination": "witness questioning",
    "plea bargain": "guilty plea agreement",
    "indictment": "formal charge",
    "arraignment": "court appearance",
    "subpoena": "court order",
    "affidavit": "sworn statement",
    "motion": "court request",
    "hearsay": "secondhand evidence",
    "burden of proof": "proof responsibility",
    "beyond reasonable doubt": "high proof standard",
    "preponderance of evidence": "majority proof standard",
    "due diligence": "reasonable care",
    "fiduciary duty": "trust responsibility",
    "conflict of interest": "competing interests",
    "disclosure": "information revelation",
    "privilege": "legal protection",
    "immunity": "legal exemption",
    "statutory law": "legislative law",
    "common law": "judge-made law",
}

def normalize_query(text):
    """
    Replace domain terms with standardized mappings.
    """
    text_lower = text.lower()
    for term, standard in DOMAIN_TERM_MAPPINGS.items():
        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
        text_lower = pattern.sub(standard, text_lower)
    return text_lower

# -------------------------------
# THREE LAYER RESPONSE SYSTEM
# -------------------------------

class DoctrineCache:
    """
    Simple in-memory cache keyed by keywords tuple.
    """
    def __init__(self):
        self.cache = {}

    def lookup(self, keywords):
        key = tuple(sorted(keywords))
        return self.cache.get(key)

    def store(self, keywords, analysis):
        key = tuple(sorted(keywords))
        self.cache[key] = analysis

doctrine_cache = DoctrineCache()

def extract_keywords(text):
    """
    Extract keywords for cache lookup.
    """
    # Simplistic keyword extraction: words longer than 5 chars
    words = re.findall(r'\b\w{6,}\b', text.lower())
    return set(words)

def semantic_search(query):
    """
    Simulate semantic search returning relevant sub-engines.
    """
    # For demo, map keywords to sub-engines
    sub_engines = {
        "contract": contract_sub_engine,
        "negligence": negligence_sub_engine,
        "damages": damages_sub_engine,
        "jurisdiction": jurisdiction_sub_engine,
        "evidence": evidence_sub_engine,
        "liability": liability_sub_engine,
        "appeal": appeal_sub_engine,
        "injunction": injunction_sub_engine,
    }
    keywords = extract_keywords(query)
    matched = []
    for kw in keywords:
        for key in sub_engines.keys():
            if key in kw:
                matched.append(sub_engines[key])
    if not matched:
        matched.append(general_sub_engine)
    return matched

def contract_sub_engine(query):
    time.sleep(0.1)  # simulate processing
    return {"contract breach": {"text": "Contract sub-engine analysis.", "sources": [(AuthorityLevel.STATUTORY, "Statute123")] }}

def negligence_sub_engine(query):
    time.sleep(0.12)
    return {"negligence": {"text": "Negligence sub-engine analysis.", "sources": [(AuthorityLevel.CASE_LAW, "Case456")] }}

def damages_sub_engine(query):
    time.sleep(0.15)
    return {"damages calculation": {"text": "Damages sub-engine analysis.", "sources": [(AuthorityLevel.TREATISE, "Treatise789")] }}

def jurisdiction_sub_engine(query):
    time.sleep(0.1)
    return {"jurisdiction": {"text": "Jurisdiction sub-engine analysis.", "sources": [(AuthorityLevel.CONSTITUTIONAL, "Constitution001")] }}

def evidence_sub_engine(query):
    time.sleep(0.13)
    return {"evidence": {"text": "Evidence sub-engine analysis.", "sources": [(AuthorityLevel.REGULATORY, "Regulation234")] }}

def liability_sub_engine(query):
    time.sleep(0.11)
    return {"liability": {"text": "Liability sub-engine analysis.", "sources": [(AuthorityLevel.CASE_LAW, "Case789")] }}

def appeal_sub_engine(query):
    time.sleep(0.1)
    return {"appeal": {"text": "Appeal sub-engine analysis.", "sources": [(AuthorityLevel.STATUTORY, "Statute567")] }}

def injunction_sub_engine(query):
    time.sleep(0.12)
    return {"injunction": {"text": "Injunction sub-engine analysis.", "sources": [(AuthorityLevel.PRACTICE, "Practice345")] }}

def general_sub_engine(query):
    time.sleep(0.1)
    return {"general inquiry": {"text": "General sub-engine analysis.", "sources": [(AuthorityLevel.PRACTICE, "Practice000")] }}

def layer1_doctrine_cache_lookup(query):
    """
    Layer 1: Doctrine cache lookup (0-200ms)
    """
    keywords = extract_keywords(query)
    cached = doctrine_cache.lookup(keywords)
    if cached:
        return cached
    return None

def layer2_semantic_search_and_routing(query):
    """
    Layer 2: Semantic search + sub-engine routing
    """
    sub_engines = semantic_search(query)
    results = []
    for engine in sub_engines:
        res = engine(query)
        results.append(res)
    return results

def layer3_deep_multi_engine_analysis(query, sub_engine_results):
    """
    Layer 3: Deep multi-engine analysis — parallel dispatch, merge, resolve conflicts
    """
    doctrines = multi_doctrine_decomposition(query)
    analysis = eight_step_resolution(query, doctrines, sub_engine_results)
    return analysis

def three_layer_response(query):
    """
    Orchestrate three layers with timing and fallback.
    """
    start = time.time()
    # Layer 1
    cached = layer1_doctrine_cache_lookup(query)
    if cached:
        return cached
    # Layer 2
    sub_engine_results = layer2_semantic_search_and_routing(query)
    # Store in cache for future
    keywords = extract_keywords(query)
    doctrine_cache.store(keywords, sub_engine_results)
    # Layer 3
    deep_analysis = layer3_deep_multi_engine_analysis(query, sub_engine_results)
    return deep_analysis

# -------------------------------
# END OF PART 4
# -------------------------------

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
        self.query_records: List[QueryTelemetry] = []
        self.latencies: List[float] = []
        self.cache_hits: int = 0
        self.total_queries: int = 0
        self.errors: List[QueryTelemetry] = []
        self.doctrine_hits: Counter = Counter()
        self.engine_stats: Dict[str, List[float]] = defaultdict(list)
        self.engine_errors: Dict[str, int] = defaultdict(int)
        self.query_times: deque = deque()  # (timestamp, QueryTelemetry)
        self.sub_engine_invocations: Counter = Counter()
        self._hour_window = 3600

    def record_query(self, telemetry: QueryTelemetry):
        with self.lock:
            self.query_records.append(telemetry)
            self.latencies.append(telemetry.latency_ms)
            self.total_queries += 1
            if telemetry.cache_hit:
                self.cache_hits += 1
            for engine in telemetry.engines_invoked:
                self.engine_stats[engine].append(telemetry.latency_ms)
                self.sub_engine_invocations[engine] += 1
            self.query_times.append((telemetry.timestamp, telemetry))
            # Clean up old queries (older than 1 hour)
            now = time.time()
            while self.query_times and self.query_times[0][0] < now - self._hour_window:
                self.query_times.popleft()

    def record_error(self, telemetry: QueryTelemetry):
        with self.lock:
            self.errors.append(telemetry)
            for engine in telemetry.engines_invoked:
                self.engine_errors[engine] += 1

    def get_latency_stats(self) -> Dict[str, float]:
        with self.lock:
            if not self.latencies:
                return dict(avg=0, p50=0, p95=0, p99=0, min=0, max=0)
            lat = sorted(self.latencies)
            return dict(
                avg=statistics.mean(lat),
                p50=statistics.median(lat),
                p95=lat[int(0.95 * len(lat))-1],
                p99=lat[int(0.99 * len(lat))-1],
                min=min(lat),
                max=max(lat)
            )

    def get_doctrine_hit_rate(self) -> float:
        with self.lock:
            if self.total_queries == 0:
                return 0.0
            return self.cache_hits / self.total_queries

    def queries_last_hour(self) -> int:
        with self.lock:
            return len(self.query_times)

    def get_sub_engine_stats(self) -> Dict[str, Dict[str, float]]:
        with self.lock:
            stats = {}
            for engine, latencies in self.engine_stats.items():
                if not latencies:
                    continue
                lat = sorted(latencies)
                error_count = self.engine_errors.get(engine, 0)
                stats[engine] = dict(
                    avg=statistics.mean(lat),
                    p50=statistics.median(lat),
                    p95=lat[int(0.95 * len(lat))-1],
                    p99=lat[int(0.99 * len(lat))-1],
                    min=min(lat),
                    max=max(lat),
                    error_rate=error_count / len(latencies)
                )
            return stats

# ---- DRIFT WATCHER ----

class DriftWatcher:
    def __init__(self):
        self.lock = threading.Lock()
        self.baselines: Dict[str, float] = {}  # doctrine -> baseline confidence
        self.history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))  # doctrine -> (timestamp, confidence)
        self.drift_alerts: List[Tuple[str, float, float, float]] = []  # (doctrine, baseline, current, drift_pct)
        self.drift_threshold = 0.10  # 10%

    def record_baseline(self, doctrine: str, confidence: float):
        with self.lock:
            self.baselines[doctrine] = confidence

    def record_confidence(self, doctrine: str, confidence: float):
        with self.lock:
            now = time.time()
            self.history[doctrine].append((now, confidence))
            baseline = self.baselines.get(doctrine)
            if baseline is not None:
                drift = abs(confidence - baseline) / max(baseline, 1e-6)
                if drift > self.drift_threshold:
                    self.drift_alerts.append((doctrine, baseline, confidence, drift))

    def detect_drift(self, doctrine: str) -> Optional[Tuple[float, float, float]]:
        with self.lock:
            baseline = self.baselines.get(doctrine)
            if not baseline or doctrine not in self.history:
                return None
            recent = [c for ts, c in self.history[doctrine] if ts > time.time() - 3600]
            if not recent:
                return None
            avg_conf = statistics.mean(recent)
            drift = abs(avg_conf - baseline) / max(baseline, 1e-6)
            if drift > self.drift_threshold:
                return (baseline, avg_conf, drift)
            return None

    def get_drift_report(self) -> List[Dict[str, Any]]:
        with self.lock:
            report = []
            for doctrine, baseline in self.baselines.items():
                recent = [c for ts, c in self.history[doctrine] if ts > time.time() - 3600]
                if not recent:
                    continue
                avg_conf = statistics.mean(recent)
                drift = abs(avg_conf - baseline) / max(baseline, 1e-6)
                report.append({
                    "doctrine": doctrine,
                    "baseline": baseline,
                    "avg_confidence": avg_conf,
                    "drift_pct": drift,
                    "alert": drift > self.drift_threshold
                })
            return report

# ---- COVERAGE MAP ----

class CoverageTracker:
    def __init__(self):
        self.lock = threading.Lock()
        self.triggered: Counter = Counter()  # doctrine -> count
        self.missed_queries: List[Tuple[float, str]] = []  # (timestamp, query_id)
        self.epistemic_gaps: List[Tuple[float, str]] = []  # (timestamp, query_id)
        self.sub_engine_coverage: Dict[str, Counter] = defaultdict(Counter)
        self.query_to_doctrines: Dict[str, List[str]] = {}  # query_id -> doctrines

    def record_triggered(self, doctrine: str, query_id: str, sub_engines: List[str]):
        with self.lock:
            self.triggered[doctrine] += 1
            for engine in sub_engines:
                self.sub_engine_coverage[engine][doctrine] += 1
            self.query_to_doctrines[query_id] = self.query_to_doctrines.get(query_id, []) + [doctrine]

    def record_missed(self, query_id: str):
        with self.lock:
            now = time.time()
            self.missed_queries.append((now, query_id))
            self.query_to_doctrines.setdefault(query_id, [])

    def record_epistemic_gap(self, query_id: str):
        with self.lock:
            now = time.time()
            self.epistemic_gaps.append((now, query_id))

    def get_coverage_report(self) -> Dict[str, Any]:
        with self.lock:
            total_queries = len(set(list(self.query_to_doctrines.keys()) + [q for _, q in self.missed_queries]))
            doctrine_coverage = {k: v for k, v in self.triggered.items()}
            missed = [q for _, q in self.missed_queries]
            epistemic = [q for _, q in self.epistemic_gaps]
            sub_engine_stats = {}
            for engine, counter in self.sub_engine_coverage.items():
                sub_engine_stats[engine] = dict(counter)
            return {
                "total_queries": total_queries,
                "doctrine_coverage": doctrine_coverage,
                "missed_queries": missed,
                "epistemic_gaps": epistemic,
                "sub_engine_coverage": sub_engine_stats
            }

    def detect_epistemic_gaps(self):
        with self.lock:
            for query_id, doctrines in self.query_to_doctrines.items():
                if not doctrines:
                    self.record_epistemic_gap(query_id)

# ---- DETERMINISM HASH ----

def compute_determinism_hash(query: Any, response: Any) -> str:
    # Normalize and hash query/response for reproducibility
    def normalize(obj):
        if isinstance(obj, dict):
            return {k: normalize(obj[k]) for k in sorted(obj)}
        elif isinstance(obj, list):
            return [normalize(x) for x in obj]
        elif isinstance(obj, float):
            return round(obj, 8)
        else:
            return obj

    data = {
        "query": normalize(query),
        "response": normalize(response)
    }
    s = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def verify_reproducibility(query: Any, response: Any, expected_hash: str) -> bool:
    return compute_determinism_hash(query, response) == expected_hash

# ---- AUDIT TRAIL ----

class AuditTrailWriter:
    def __init__(self, audit_dir: str):
        self.audit_dir = audit_dir
        self.current_date = None
        self.file = None
        self.lock = threading.Lock()
        os.makedirs(audit_dir, exist_ok=True)
        self._open_file()

    def _get_filename(self):
        date_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        return os.path.join(self.audit_dir, f"audit_{date_str}.jsonl")

    def _open_file(self):
        with self.lock:
            date_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
            if self.current_date != date_str or self.file is None:
                if self.file:
                    self.file.close()
                filename = self._get_filename()
                self.file = open(filename, "a", encoding="utf-8")
                self.current_date = date_str

    def write(self, query_id: str, timestamp: float, engine_id: str, engines_invoked: List[str],
              mode: str, confidence: float, latency: float, cache_hit: bool):
        with self.lock:
            self._open_file()
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
            self.file.write(json.dumps(record) + "\n")
            self.file.flush()

    def forensic_replay(self, date: str) -> List[Dict[str, Any]]:
        filename = os.path.join(self.audit_dir, f"audit_{date}.jsonl")
        if not os.path.exists(filename):
            return []
        with open(filename, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f]

    def close(self):
        with self.lock:
            if self.file:
                self.file.close()
                self.file = None

# ---- PERFORMANCE PROFILER ----

class PerformanceProfiler:
    def __init__(self):
        self.lock = threading.Lock()
        self.sub_engine_latency: Dict[str, List[float]] = defaultdict(list)
        self.sub_engine_errors: Dict[str, int] = defaultdict(int)
        self.sub_engine_availability: Dict[str, List[Tuple[float, bool]]] = defaultdict(list)
        self.sla_targets: Dict[str, Dict[str, float]] = {}  # engine -> {latency_ms, error_rate, availability}
        self.sla_violations: Dict[str, List[Tuple[float, str, float]]] = defaultdict(list)  # engine -> [(timestamp, metric, value)]

    def record_latency(self, engine: str, latency_ms: float):
        with self.lock:
            self.sub_engine_latency[engine].append(latency_ms)
            self._check_sla(engine)

    def record_error(self, engine: str):
        with self.lock:
            self.sub_engine_errors[engine] += 1
            self._check_sla(engine)

    def record_availability(self, engine: str, available: bool):
        with self.lock:
            now = time.time()
            self.sub_engine_availability[engine].append((now, available))
            self._check_sla(engine)

    def set_sla(self, engine: str, latency_ms: float, error_rate: float, availability: float):
        with self.lock:
            self.sla_targets[engine] = {
                "latency_ms": latency_ms,
                "error_rate": error_rate,
                "availability": availability
            }

    def _check_sla(self, engine: str):
        targets = self.sla_targets.get(engine)
        if not targets:
            return
        now = time.time()
        # Latency
        lat = self.sub_engine_latency[engine][-100:]  # last 100
        if lat:
            avg_latency = statistics.mean(lat)
            if avg_latency > targets["latency_ms"]:
                self.sla_violations[engine].append((now, "latency", avg_latency))
        # Error rate
        total = len(self.sub_engine_latency[engine])
        errors = self.sub_engine_errors[engine]
        if total > 0:
            error_rate = errors / total
            if error_rate > targets["error_rate"]:
                self.sla_violations[engine].append((now, "error_rate", error_rate))
        # Availability
        avail = [a for t, a in self.sub_engine_availability[engine] if t > now - 3600]
        if avail:
            avail_rate = sum(avail) / len(avail)
            if avail_rate < targets["availability"]:
                self.sla_violations[engine].append((now, "availability", avail_rate))

    def get_engine_stats(self, engine: str) -> Dict[str, Any]:
        with self.lock:
            lat = self.sub_engine_latency[engine]
            errors = self.sub_engine_errors[engine]
            avail = [a for t, a in self.sub_engine_availability[engine] if t > time.time() - 3600]
            stats = {}
            if lat:
                stats["avg_latency"] = statistics.mean(lat)
                stats["p95_latency"] = sorted(lat)[int(0.95 * len(lat))-1]
                stats["max_latency"] = max(lat)
            else:
                stats["avg_latency"] = 0
                stats["p95_latency"] = 0
                stats["max_latency"] = 0
            stats["error_rate"] = errors / len(lat) if lat else 0
            stats["availability"] = sum(avail) / len(avail) if avail else 1.0
            stats["sla_violations"] = list(self.sla_violations[engine])
            return stats

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        with self.lock:
            return {engine: self.get_engine_stats(engine) for engine in self.sub_engine_latency}

# ---- EXAMPLE INTEGRATION ----

class RailroadIntelligenceEngineOrchestrator:
    def __init__(self, audit_dir: str):
        self.telemetry = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.coverage = CoverageTracker()
        self.audit = AuditTrailWriter(audit_dir)
        self.profiler = PerformanceProfiler()

    def process_query(self, query_id: str, query: Any, response: Any,
                      engines_invoked: List[str], mode: str, confidence: float,
                      latency_ms: float, cache_hit: bool, engine_id: str, doctrine: Optional[str], error: Optional[str]=None):
        timestamp = time.time()
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
        self.telemetry.record_query(telemetry)
        if error:
            self.telemetry.record_error(telemetry)
        # Drift
        if doctrine:
            if doctrine not in self.drift_watcher.baselines:
                self.drift_watcher.record_baseline(doctrine, confidence)
            self.drift_watcher.record_confidence(doctrine, confidence)
            self.coverage.record_triggered(doctrine, query_id, engines_invoked)
        else:
            self.coverage.record_missed(query_id)
        # Coverage epistemic gap
        self.coverage.detect_epistemic_gaps()
        # Audit
        self.audit.write(
            query_id=query_id,
            timestamp=timestamp,
            engine_id=engine_id,
            engines_invoked=engines_invoked,
            mode=mode,
            confidence=confidence,
            latency=latency_ms,
            cache_hit=cache_hit
        )
        # Performance
        for engine in engines_invoked:
            self.profiler.record_latency(engine, latency_ms)
            self.profiler.record_availability(engine, error is None)
            if error:
                self.profiler.record_error(engine)

    def verify_query_determinism(self, query: Any, response: Any, expected_hash: str) -> bool:
        return verify_reproducibility(query, response, expected_hash)

    def get_telemetry_stats(self):
        return self.telemetry.get_latency_stats()

    def get_drift_report(self):
        return self.drift_watcher.get_drift_report()

    def get_coverage_report(self):
        return self.coverage.get_coverage_report()

    def get_performance_stats(self):
        return self.profiler.get_all_stats()

    def forensic_replay(self, date: str):
        return self.audit.forensic_replay(date)

    def close(self):
        self.audit.close()

ENGINE_ID = "RAILIE"
ENGINE_PORT = 8860
SUB_ENGINES = {
    "RAIL01": "Track Engineering",
    "RAIL02": "Locomotive Systems",
    "RAIL03": "Signal Systems",
    "RAIL04": "Freight Operations",
    "RAIL05": "Rail Safety",
    "RAIL06": "Rail Structures",
    "RAIL07": "Rolling Stock",
    "RAIL08": "Electrification",
    "RAIL09": "Train Control",
    "RAIL10": "Yard Operations",
    "RAIL11": "Passenger Rail",
}

# Logger setup
logger = logging.getLogger("railie")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Global state (would be better encapsulated in classes)
doctrine_cache: Dict[str, Any] = {}
search_index: Dict[str, List[str]] = {}
telemetry_data: Dict[str, Any] = {
    "latency_ms": [],
    "cache_hits": 0,
    "cache_misses": 0,
    "queries_count": 0,
    "sub_engine_stats": {k: {"calls": 0, "failures": 0, "avg_latency_ms": 0.0} for k in SUB_ENGINES.keys()},
}
health_status: Dict[str, str] = {}
routing_rules: Dict[str, List[str]] = {}
circuit_breakers: Dict[str, Dict[str, Any]] = {}
epistemic_gaps: List[str] = []
drift_report: Dict[str, Any] = {}
lock = asyncio.Lock()

# Configuration for circuit breaker
CIRCUIT_BREAKER_THRESHOLD = 3
CIRCUIT_BREAKER_TIMEOUT = 30  # seconds

# Models
class QueryRequest(BaseModel):
    query: str = Field(..., example="What is the status of track section 12B?")
    options: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    response: Any
    sources: List[str]
    cache_hit: bool = False

class HealthResponse(BaseModel):
    engine: str
    status: str
    details: Dict[str, Any]

class MetricsResponse(BaseModel):
    latency_ms_avg: float
    cache_hit_rate: float
    queries_per_hour: float
    sub_engine_stats: Dict[str, Any]

class CoverageResponse(BaseModel):
    doctrine_coverage: Dict[str, Any]
    epistemic_gaps: List[str]

class DriftResponse(BaseModel):
    drift_detected: bool
    details: Dict[str, Any]

class DoctrinesResponse(BaseModel):
    doctrines: List[str]

class RoutingResponse(BaseModel):
    routing_rules: Dict[str, List[str]]
    engine_registry: Dict[str, str]

class SubEnginesResponse(BaseModel):
    sub_engines_health: Dict[str, str]

class RouteDryRunRequest(BaseModel):
    query: str

class RouteDryRunResponse(BaseModel):
    engines_to_invoke: List[str]

class AnalyzeRequest(BaseModel):
    query: str
    depth: int = Field(1, ge=1, le=5)

class AnalyzeResponse(BaseModel):
    analysis: Dict[str, Any]

# Utility functions
def normalize_query(query: str) -> str:
    normalized = query.strip().lower()
    logger.debug(f"Normalized query: {normalized}")
    return normalized

def classify_domain(query: str) -> str:
    # Simple keyword-based classification for demo purposes
    keywords_map = {
        "track": "RAIL01",
        "locomotive": "RAIL02",
        "signal": "RAIL03",
        "freight": "RAIL04",
        "safety": "RAIL05",
        "structure": "RAIL06",
        "rolling stock": "RAIL07",
        "electrification": "RAIL08",
        "train control": "RAIL09",
        "yard": "RAIL10",
        "passenger": "RAIL11",
    }
    for keyword, engine_id in keywords_map.items():
        if keyword in query:
            logger.debug(f"Classified domain '{engine_id}' for query '{query}'")
            return engine_id
    # Default fallback
    logger.debug(f"Default classification to 'RAIL01' for query '{query}'")
    return "RAIL01"

def route_query(domain_id: str) -> List[str]:
    # Routing rules: domain to sub-engines
    # For simplicity, route to the classified domain plus related engines
    base_engines = [domain_id]
    related_engines_map = {
        "RAIL01": ["RAIL06", "RAIL07"],
        "RAIL02": ["RAIL07", "RAIL08"],
        "RAIL03": ["RAIL09"],
        "RAIL04": ["RAIL10"],
        "RAIL05": ["RAIL03", "RAIL09"],
        "RAIL06": ["RAIL01"],
        "RAIL07": ["RAIL02"],
        "RAIL08": ["RAIL02"],
        "RAIL09": ["RAIL03", "RAIL05"],
        "RAIL10": ["RAIL04"],
        "RAIL11": ["RAIL09"],
    }
    related = related_engines_map.get(domain_id, [])
    engines = list(set(base_engines + related))
    logger.debug(f"Routing query for domain '{domain_id}' to engines {engines}")
    return engines

async def dispatch_to_engine(engine_id: str, query: str) -> Dict[str, Any]:
    # Simulate sub-engine call with timeout, circuit breaker, and failure handling
    cb = circuit_breakers.setdefault(engine_id, {"fail_count": 0, "last_failure": None, "open": False, "opened_at": None})
    now = datetime.utcnow()
    if cb["open"]:
        if (now - cb["opened_at"]).total_seconds() > CIRCUIT_BREAKER_TIMEOUT:
            # Reset circuit breaker
            cb["open"] = False
            cb["fail_count"] = 0
            logger.info(f"Circuit breaker reset for engine {engine_id}")
        else:
            logger.warning(f"Circuit breaker open for engine {engine_id}, skipping call")
            raise HTTPException(status_code=503, detail=f"Sub-engine {engine_id} circuit breaker open")

    start = time.perf_counter()
    try:
        # Simulated latency and failure
        latency = random.uniform(0.05, 0.3)
        await asyncio.sleep(latency)
        # Simulate random failure
        if random.random() < 0.05:
            raise Exception(f"Simulated failure in engine {engine_id}")
        # Simulated response
        response = {
            "engine_id": engine_id,
            "result": f"Processed '{query}' in {SUB_ENGINES[engine_id]}",
            "latency_ms": latency * 1000,
        }
        # Update telemetry
        telemetry_data["sub_engine_stats"][engine_id]["calls"] += 1
        prev_avg = telemetry_data["sub_engine_stats"][engine_id]["avg_latency_ms"]
        calls = telemetry_data["sub_engine_stats"][engine_id]["calls"]
        telemetry_data["sub_engine_stats"][engine_id]["avg_latency_ms"] = (prev_avg * (calls - 1) + latency * 1000) / calls
        # Reset circuit breaker on success
        cb["fail_count"] = 0
        return response
    except Exception as e:
        cb["fail_count"] += 1
        cb["last_failure"] = now
        if cb["fail_count"] >= CIRCUIT_BREAKER_THRESHOLD:
            cb["open"] = True
            cb["opened_at"] = now
            logger.error(f"Circuit breaker opened for engine {engine_id} due to repeated failures")
        telemetry_data["sub_engine_stats"][engine_id]["failures"] += 1
        logger.error(f"Error dispatching to engine {engine_id}: {e}")
        raise

def merge_responses(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
    merged = {
        "results": [],
        "sources": [],
    }
    for resp in responses:
        merged["results"].append(resp.get("result"))
        merged["sources"].append(resp.get("engine_id"))
    logger.debug(f"Merged responses from engines: {merged['sources']}")
    return merged

def apply_guardrails(merged_response: Dict[str, Any]) -> Dict[str, Any]:
    # Example guardrail: truncate results if too long
    max_results = 10
    if len(merged_response["results"]) > max_results:
        merged_response["results"] = merged_response["results"][:max_results]
        merged_response["guardrail_applied"] = True
    else:
        merged_response["guardrail_applied"] = False
    return merged_response

def hash_response(response: Dict[str, Any]) -> str:
    response_str = json.dumps(response, sort_keys=True)
    h = hashlib.sha256(response_str.encode("utf-8")).hexdigest()
    logger.debug(f"Response hash: {h}")
    return h

async def log_query(query: str, response_hash: str, cache_hit: bool, sources: List[str], latency_ms: float):
    # For demo, just log to stdout
    logger.info(f"Query logged: hash={response_hash}, cache_hit={cache_hit}, sources={sources}, latency_ms={latency_ms}")

async def initialize_doctrine_cache():
    global doctrine_cache
    # Simulate loading doctrines
    doctrine_cache = {
        "track_maintenance": {"coverage": 0.9, "data": "Track maintenance doctrine data"},
        "locomotive_operations": {"coverage": 0.85, "data": "Locomotive operations doctrine data"},
        "signal_protocols": {"coverage": 0.95, "data": "Signal systems doctrine data"},
        # ... more doctrines
    }
    logger.info("Doctrine cache initialized")

async def start_health_monitor():
    async def health_check_loop():
        while True:
            for engine_id in SUB_ENGINES.keys():
                # Simulate health check
                status = "healthy" if random.random() > 0.05 else "degraded"
                health_status[engine_id] = status
            health_status[ENGINE_ID] = "healthy"
            await asyncio.sleep(10)
    asyncio.create_task(health_check_loop())
    logger.info("Health monitor started")

async def seed_search_index():
    global search_index
    # Simulate seeding search index from doctrines
    search_index = {
        "track": ["track_maintenance"],
        "locomotive": ["locomotive_operations"],
        "signal": ["signal_protocols"],
        # ...
    }
    logger.info("Search index seeded")

async def start_telemetry():
    # Telemetry is updated during query processing
    logger.info("Telemetry started")

async def detect_drift():
    global drift_report
    # Simulate drift detection
    drift_report = {
        "drift_detected": random.random() < 0.1,
        "details": {
            "last_checked": datetime.utcnow().isoformat(),
            "drift_score": random.uniform(0, 1),
        }
    }
    logger.info("Drift detection completed")

def get_doctrine_coverage_report() -> Dict[str, Any]:
    coverage = {}
    for k, v in doctrine_cache.items():
        coverage[k] = v.get("coverage", 0.0)
    return coverage

def get_epistemic_gaps_report() -> List[str]:
    # Simulate gaps
    gaps = [
        "Limited data on new electrification methods",
        "Sparse coverage on advanced freight logistics",
    ]
    return gaps

def get_queries_per_hour() -> float:
    # For demo, approximate based on queries_count and uptime
    uptime_hours = max((datetime.utcnow() - app.state.start_time).total_seconds() / 3600, 1)
    return telemetry_data["queries_count"] / uptime_hours

def get_cache_hit_rate() -> float:
    total = telemetry_data["cache_hits"] + telemetry_data["cache_misses"]
    if total == 0:
        return 0.0
    return telemetry_data["cache_hits"] / total

def get_latency_avg() -> float:
    latencies = telemetry_data["latency_ms"]
    if not latencies:
        return 0.0
    return sum(latencies) / len(latencies)

def get_sub_engine_health_dashboard() -> Dict[str, str]:
    return health_status.copy()

def get_routing_rules() -> Dict[str, List[str]]:
    # For demo, routing_rules is static or precomputed
    rules = {}
    for domain_id in SUB_ENGINES.keys():
        rules[domain_id] = route_query(domain_id)
    return rules

# FastAPI app
app = FastAPI(title="Railroad Intelligence Engine - Domain Orchestrator", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lifespan management
@app.on_event("startup")
async def startup_event():
    app.state.start_time = datetime.utcnow()
    await initialize_doctrine_cache()
    await start_health_monitor()
    await seed_search_index()
    await start_telemetry()
    await detect_drift()
    logger.info(f"{ENGINE_ID} started on port {ENGINE_PORT}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"{ENGINE_ID} shutting down")

# Error handler for sub-engine failures
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Main query endpoint
@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    start_time = time.perf_counter()
    query = request.query
    normalized_query = normalize_query(query)
    domain_id = classify_domain(normalized_query)
    engines_to_call = route_query(domain_id)

    # Check doctrine cache first
    cache_key = hashlib.sha256(normalized_query.encode("utf-8")).hexdigest()
    cached_response = doctrine_cache.get(cache_key)
    if cached_response:
        telemetry_data["cache_hits"] += 1
        telemetry_data["queries_count"] += 1
        latency_ms = (time.perf_counter() - start_time) * 1000
        telemetry_data["latency_ms"].append(latency_ms)
        await log_query(query, cache_key, True, ["doctrine_cache"], latency_ms)
        return QueryResponse(response=cached_response, sources=["doctrine_cache"], cache_hit=True)

    telemetry_data["cache_misses"] += 1
    telemetry_data["queries_count"] += 1

    responses = []
    for engine_id in engines_to_call:
        try:
            resp = await dispatch_to_engine(engine_id, normalized_query)
            responses.append(resp)
        except HTTPException as e:
            # Log failure and fallback to doctrine cache partial data if possible
            logger.warning(f"Sub-engine {engine_id} failed: {e.detail}")
            fallback_data = doctrine_cache.get(engine_id)
            if fallback_data:
                responses.append({"engine_id": engine_id, "result": fallback_data, "latency_ms": 0})
            else:
                responses.append({"engine_id": engine_id, "result": f"Fallback data not available for {engine_id}", "latency_ms": 0})

    merged = merge_responses(responses)
    guarded = apply_guardrails(merged)
    response_hash = hash_response(guarded)
    latency_ms = (time.perf_counter() - start_time) * 1000
    telemetry_data["latency_ms"].append(latency_ms)
    await log_query(query, response_hash, False, guarded["sources"], latency_ms)
    return QueryResponse(response=guarded, sources=guarded["sources"], cache_hit=False)

# Health endpoint
@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    overall_status = "healthy" if all(s == "healthy" for s in health_status.values()) else "degraded"
    details = health_status.copy()
    return HealthResponse(engine=ENGINE_ID, status=overall_status, details=details)

# Metrics endpoint
@app.get("/metrics", response_model=MetricsResponse)
async def metrics_endpoint():
    latency_avg = get_latency_avg()
    cache_hit_rate = get_cache_hit_rate()
    queries_per_hour = get_queries_per_hour()
    sub_engine_stats = telemetry_data["sub_engine_stats"]
    return MetricsResponse(
        latency_ms_avg=latency_avg,
        cache_hit_rate=cache_hit_rate,
        queries_per_hour=queries_per_hour,
        sub_engine_stats=sub_engine_stats,
    )

# Coverage endpoint
@app.get("/coverage", response_model=CoverageResponse)
async def coverage_endpoint():
    doctrine_coverage = get_doctrine_coverage_report()
    gaps = get_epistemic_gaps_report()
    return CoverageResponse(doctrine_coverage=doctrine_coverage, epistemic_gaps=gaps)

# Drift endpoint
@app.get("/drift", response_model=DriftResponse)
async def drift_endpoint():
    await detect_drift()
    return DriftResponse(drift_detected=drift_report.get("drift_detected", False), details=drift_report.get("details", {}))

# Doctrines endpoint
@app.get("/doctrines", response_model=DoctrinesResponse)
async def doctrines_endpoint():
    doctrines_list = list(doctrine_cache.keys())
    return DoctrinesResponse(doctrines=doctrines_list)

# Routing endpoint
@app.get("/routing", response_model=RoutingResponse)
async def routing_endpoint():
    rules = get_routing_rules()
    return RoutingResponse(routing_rules=rules, engine_registry=SUB_ENGINES)

# Sub-engines health dashboard
@app.get("/sub-engines", response_model=SubEnginesResponse)
async def sub_engines_endpoint():
    dashboard = get_sub_engine_health_dashboard()
    return SubEnginesResponse(sub_engines_health=dashboard)

# Route dry-run endpoint
@app.post("/route", response_model=RouteDryRunResponse)
async def route_dry_run_endpoint(request: RouteDryRunRequest):
    normalized_query = normalize_query(request.query)
    domain_id = classify_domain(normalized_query)
    engines = route_query(domain_id)
    return RouteDryRunResponse(engines_to_invoke=engines)

# Analyze endpoint
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(request: AnalyzeRequest):
    normalized_query = normalize_query(request.query)
    domain_id = classify_domain(normalized_query)
    engines = route_query(domain_id)
    analysis = {}
    for engine_id in engines:
        # Simulate deep analysis with increasing depth
        analysis[engine_id] = {
            "summary": f"Deep analysis of '{normalized_query}' at depth {request.depth} in {SUB_ENGINES[engine_id]}",
            "details": {"depth": request.depth, "timestamp": datetime.utcnow().isoformat()},
        }
    return AnalyzeResponse(analysis=analysis)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT)