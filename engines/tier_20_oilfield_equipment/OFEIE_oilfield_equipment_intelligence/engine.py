import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import uuid
import json
import time
import asyncio
import aiohttp
import statistics
import collections
from typing import List, Dict, Optional, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel, Field
from loguru import logger

# ENGINE CONSTANTS
ENGINE_ID = "OFEIE"
ENGINE_PORT = 8850
ENGINE_NAME = "Oilfield Equipment Intelligence Engine — Domain Orchestrator"
ENGINE_VERSION = "1.0.0"

# ENUMS

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
    PUMP_FAILURE = "PUMP_FAILURE"
    VALVE_LEAKAGE = "VALVE_LEAKAGE"
    PRESSURE_ANOMALY = "PRESSURE_ANOMALY"
    TEMPERATURE_SPIKE = "TEMPERATURE_SPIKE"
    VIBRATION_EXCESS = "VIBRATION_EXCESS"
    SENSOR_FAULT = "SENSOR_FAULT"
    ELECTRICAL_FAULT = "ELECTRICAL_FAULT"
    CONTROL_SYSTEM_ERROR = "CONTROL_SYSTEM_ERROR"
    MAINTENANCE_OVERDUE = "MAINTENANCE_OVERDUE"
    SEAL_FAILURE = "SEAL_FAILURE"
    CORROSION_DETECTED = "CORROSION_DETECTED"
    FLOW_RESTRICTION = "FLOW_RESTRICTION"
    GAS_LEAK = "GAS_LEAK"
    HYDRAULIC_ISSUE = "HYDRAULIC_ISSUE"
    STRUCTURAL_FATIGUE = "STRUCTURAL_FATIGUE"
    BOP_MALFUNCTION = "BOP_MALFUNCTION"
    SEPARATOR_OVERFLOW = "SEPARATOR_OVERFLOW"
    ARTIFICIAL_LIFT_FAILURE = "ARTIFICIAL_LIFT_FAILURE"
    COMPRESSOR_TRIP = "COMPRESSOR_TRIP"
    WELLHEAD_LEAK = "WELLHEAD_LEAK"
    CASING_DAMAGE = "CASING_DAMAGE"
    HEAT_EXCHANGER_FOULING = "HEAT_EXCHANGER_FOULING"
    SAFETY_SYSTEM_BYPASS = "SAFETY_SYSTEM_BYPASS"
    SCADA_COMM_ERROR = "SCADA_COMM_ERROR"
    UNKNOWN = "UNKNOWN"

class SubEngineStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

# PYDANTIC MODELS

class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str]
    domain: str
    keywords: List[str]
    parameters: Dict[str, Any] = Field(default_factory=dict)
    response_mode: ResponseMode = ResponseMode.FAST
    position_zone: PositionZone = PositionZone.PLANNING
    confidence_zone: ConfidenceZone = ConfidenceZone.DEFENSIBLE
    trace_id: Optional[str] = None

class QueryResponse(BaseModel):
    query_id: str
    orchestrator_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    result: Any
    status: str
    confidence: float
    engine_trace: List[str] = Field(default_factory=list)
    issue_category: Optional[IssueCategory] = None
    notes: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None

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
    rationale: str
    rule_matched: Optional[str] = None
    confidence: float = 1.0
    fallback: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decision: RoutingDecision
    response: Optional[QueryResponse]
    orchestration_latency_ms: float
    subengine_latency_ms: Optional[float] = None
    errors: Optional[List[str]] = None

# SUB_ENGINE_REGISTRY

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "OFE01": SubEngineConfig(
        engine_id="OFE01",
        name="Mud Pump Systems",
        port=8851,
        health_url="http://localhost:8851/health",
        capabilities=["pump", "mud", "flow", "pressure", "seal", "vibration", "maintenance"],
        weight=1.0,
        domains=["mud_pump", "pump_failure", "seal_failure", "vibration_excess", "pressure_anomaly"]
    ),
    "OFE02": SubEngineConfig(
        engine_id="OFE02",
        name="BOP Stack Analysis",
        port=8852,
        health_url="http://localhost:8852/health",
        capabilities=["bop", "blowout", "stack", "hydraulic", "control", "malfunction"],
        weight=1.0,
        domains=["bop_stack", "bop_malfunction", "hydraulic_issue", "control_system_error"]
    ),
    "OFE03": SubEngineConfig(
        engine_id="OFE03",
        name="Frac Pump Operations",
        port=8853,
        health_url="http://localhost:8853/health",
        capabilities=["frac", "pump", "pressure", "flow", "maintenance", "vibration"],
        weight=1.0,
        domains=["frac_pump", "pump_failure", "pressure_anomaly", "maintenance_overdue"]
    ),
    "OFE04": SubEngineConfig(
        engine_id="OFE04",
        name="Separator Design",
        port=8854,
        health_url="http://localhost:8854/health",
        capabilities=["separator", "overflow", "design", "corrosion", "fouling"],
        weight=1.0,
        domains=["separator", "separator_overflow", "corrosion_detected", "heat_exchanger_fouling"]
    ),
    "OFE05": SubEngineConfig(
        engine_id="OFE05",
        name="Artificial Lift Systems",
        port=8855,
        health_url="http://localhost:8855/health",
        capabilities=["artificial_lift", "pump", "failure", "maintenance"],
        weight=1.0,
        domains=["artificial_lift", "artificial_lift_failure", "pump_failure", "maintenance_overdue"]
    ),
    "OFE06": SubEngineConfig(
        engine_id="OFE06",
        name="SCADA Monitoring",
        port=8856,
        health_url="http://localhost:8856/health",
        capabilities=["scada", "monitoring", "sensor", "comm", "data", "fault"],
        weight=1.0,
        domains=["scada", "scada_comm_error", "sensor_fault", "data_acquisition"]
    ),
    "OFE07": SubEngineConfig(
        engine_id="OFE07",
        name="Preventive Maintenance",
        port=8857,
        health_url="http://localhost:8857/health",
        capabilities=["maintenance", "preventive", "overdue", "scheduling", "audit"],
        weight=1.0,
        domains=["maintenance", "maintenance_overdue", "audit", "reporting"]
    ),
    "OFE08": SubEngineConfig(
        engine_id="OFE08",
        name="Compressor Operations",
        port=8858,
        health_url="http://localhost:8858/health",
        capabilities=["compressor", "trip", "pressure", "gas", "leak"],
        weight=1.0,
        domains=["compressor", "compressor_trip", "gas_leak", "pressure_anomaly"]
    ),
    "OFE09": SubEngineConfig(
        engine_id="OFE09",
        name="Wellhead Equipment",
        port=8859,
        health_url="http://localhost:8859/health",
        capabilities=["wellhead", "leak", "pressure", "damage"],
        weight=1.0,
        domains=["wellhead", "wellhead_leak", "casing_damage"]
    ),
    "OFE10": SubEngineConfig(
        engine_id="OFE10",
        name="Tubing and Casing",
        port=8860,
        health_url="http://localhost:8860/health",
        capabilities=["tubing", "casing", "damage", "corrosion", "flow"],
        weight=1.0,
        domains=["tubing", "casing", "casing_damage", "corrosion_detected", "flow_restriction"]
    ),
    "OFE11": SubEngineConfig(
        engine_id="OFE11",
        name="Valve Systems",
        port=8861,
        health_url="http://localhost:8861/health",
        capabilities=["valve", "leakage", "control", "maintenance"],
        weight=1.0,
        domains=["valve", "valve_leakage", "control_system_error", "maintenance_overdue"]
    ),
    "OFE12": SubEngineConfig(
        engine_id="OFE12",
        name="Heat Exchangers",
        port=8862,
        health_url="http://localhost:8862/health",
        capabilities=["heat_exchanger", "fouling", "temperature", "corrosion"],
        weight=1.0,
        domains=["heat_exchanger", "heat_exchanger_fouling", "temperature_spike", "corrosion_detected"]
    ),
    "OFE13": SubEngineConfig(
        engine_id="OFE13",
        name="Pumping Unit Design",
        port=8863,
        health_url="http://localhost:8863/health",
        capabilities=["pumping_unit", "design", "structural", "fatigue"],
        weight=1.0,
        domains=["pumping_unit", "structural_fatigue", "design", "audit"]
    ),
    "OFE14": SubEngineConfig(
        engine_id="OFE14",
        name="Electrical Systems",
        port=8864,
        health_url="http://localhost:8864/health",
        capabilities=["electrical", "fault", "control", "power"],
        weight=1.0,
        domains=["electrical", "electrical_fault", "control_system_error", "power_loss"]
    ),
    "OFE15": SubEngineConfig(
        engine_id="OFE15",
        name="Safety Equipment",
        port=8865,
        health_url="http://localhost:8865/health",
        capabilities=["safety", "system", "bypass", "audit"],
        weight=1.0,
        domains=["safety", "safety_system_bypass", "audit", "reporting"]
    ),
}

# ROUTING_RULES (200+ domain keyword to engine_id mappings)
ROUTING_RULES: Dict[str, str] = {
    # OFE01 Mud Pump Systems
    "mud_pump": "OFE01",
    "triplex_pump": "OFE01",
    "quintuplex_pump": "OFE01",
    "piston_failure": "OFE01",
    "liner_wear": "OFE01",
    "plunger": "OFE01",
    "suction_valve": "OFE01",
    "discharge_valve": "OFE01",
    "pulsation_damper": "OFE01",
    "pump_maintenance": "OFE01",
    "pump_seal": "OFE01",
    "pump_vibration": "OFE01",
    "pump_noise": "OFE01",
    "pump_pressure": "OFE01",
    "pump_temperature": "OFE01",
    # OFE02 BOP Stack Analysis
    "bop_stack": "OFE02",
    "blowout_preventer": "OFE02",
    "annular_bop": "OFE02",
    "ram_bop": "OFE02",
    "bop_control": "OFE02",
    "bop_hydraulic": "OFE02",
    "bop_leak": "OFE02",
    "bop_audit": "OFE02",
    "bop_test": "OFE02",
    "bop_failure": "OFE02",
    "bop_alarm": "OFE02",
    # OFE03 Frac Pump Operations
    "frac_pump": "OFE03",
    "frac_blender": "OFE03",
    "frac_valve": "OFE03",
    "frac_pressure": "OFE03",
    "frac_fluid": "OFE03",
    "frac_vibration": "OFE03",
    "frac_seal": "OFE03",
    "frac_maintenance": "OFE03",
    "frac_trip": "OFE03",
    # OFE04 Separator Design
    "separator": "OFE04",
    "separator_design": "OFE04",
    "separator_overflow": "OFE04",
    "separator_maintenance": "OFE04",
    "separator_corrosion": "OFE04",
    "separator_fouling": "OFE04",
    "separator_pressure": "OFE04",
    "separator_temperature": "OFE04",
    # OFE05 Artificial Lift Systems
    "artificial_lift": "OFE05",
    "esp": "OFE05",
    "sucker_rod_pump": "OFE05",
    "gas_lift": "OFE05",
    "pcp": "OFE05",
    "artificial_lift_failure": "OFE05",
    "artificial_lift_maintenance": "OFE05",
    "artificial_lift_audit": "OFE05",
    # OFE06 SCADA Monitoring
    "scada": "OFE06",
    "scada_comm_error": "OFE06",
    "scada_alarm": "OFE06",
    "scada_data": "OFE06",
    "scada_sensor": "OFE06",
    "scada_fault": "OFE06",
    "scada_latency": "OFE06",
    "scada_audit": "OFE06",
    # OFE07 Preventive Maintenance
    "maintenance": "OFE07",
    "preventive_maintenance": "OFE07",
    "maintenance_overdue": "OFE07",
    "maintenance_audit": "OFE07",
    "maintenance_report": "OFE07",
    "maintenance_schedule": "OFE07",
    "maintenance_kpi": "OFE07",
    # OFE08 Compressor Operations
    "compressor": "OFE08",
    "compressor_trip": "OFE08",
    "compressor_pressure": "OFE08",
    "compressor_gas": "OFE08",
    "compressor_leak": "OFE08",
    "compressor_maintenance": "OFE08",
    "compressor_audit": "OFE08",
    # OFE09 Wellhead Equipment
    "wellhead": "OFE09",
    "wellhead_leak": "OFE09",
    "wellhead_pressure": "OFE09",
    "wellhead_damage": "OFE09",
    "wellhead_audit": "OFE09",
    "wellhead_maintenance": "OFE09",
    # OFE10 Tubing and Casing
    "tubing": "OFE10",
    "casing": "OFE10",
    "casing_damage": "OFE10",
    "tubing_corrosion": "OFE10",
    "casing_corrosion": "OFE10",
    "tubing_leak": "OFE10",
    "casing_leak": "OFE10",
    "tubing_audit": "OFE10",
    # OFE11 Valve Systems
    "valve": "OFE11",
    "valve_leakage": "OFE11",
    "valve_control": "OFE11",
    "valve_maintenance": "OFE11",
    "valve_audit": "OFE11",
    # OFE12 Heat Exchangers
    "heat_exchanger": "OFE12",
    "heat_exchanger_fouling": "OFE12",
    "heat_exchanger_corrosion": "OFE12",
    "heat_exchanger_temperature": "OFE12",
    "heat_exchanger_audit": "OFE12",
    # OFE13 Pumping Unit Design
    "pumping_unit": "OFE13",
    "pumping_unit_design": "OFE13",
    "pumping_unit_audit": "OFE13",
    "structural_fatigue": "OFE13",
    "unit_fatigue": "OFE13",
    "unit_design": "OFE13",
    # OFE14 Electrical Systems
    "electrical": "OFE14",
    "electrical_fault": "OFE14",
    "electrical_control": "OFE14",
    "electrical_power": "OFE14",
    "electrical_audit": "OFE14",
    "power_loss": "OFE14",
    # OFE15 Safety Equipment
    "safety": "OFE15",
    "safety_system": "OFE15",
    "safety_system_bypass": "OFE15",
    "safety_audit": "OFE15",
    "safety_report": "OFE15",
    # IssueCategory mappings
    "pump_failure": "OFE01",
    "valve_leakage": "OFE11",
    "pressure_anomaly": "OFE01",
    "temperature_spike": "OFE12",
    "vibration_excess": "OFE01",
    "sensor_fault": "OFE06",
    "electrical_fault": "OFE14",
    "control_system_error": "OFE02",
    "seal_failure": "OFE01",
    "corrosion_detected": "OFE10",
    "flow_restriction": "OFE10",
    "gas_leak": "OFE08",
    "hydraulic_issue": "OFE02",
    "structural_fatigue": "OFE13",
    "bop_malfunction": "OFE02",
    "separator_overflow": "OFE04",
    "artificial_lift_failure": "OFE05",
    "compressor_trip": "OFE08",
    "wellhead_leak": "OFE09",
    "casing_damage": "OFE10",
    "heat_exchanger_fouling": "OFE12",
    "safety_system_bypass": "OFE15",
    "scada_comm_error": "OFE06",
    # Expanded keywords for 200+ rules
    "pump_trip": "OFE01",
    "pump_shutdown": "OFE01",
    "pump_alarm": "OFE01",
    "pump_overload": "OFE01",
    "pump_blockage": "OFE01",
    "pump_efficiency": "OFE01",
    "pump_capacity": "OFE01",
    "pump_audit": "OFE01",
    "bop_pressure": "OFE02",
    "bop_control_error": "OFE02",
    "bop_hydraulic_leak": "OFE02",
    "bop_sensor": "OFE02",
    "bop_trip": "OFE02",
    "frac_pressure_anomaly": "OFE03",
    "frac_valve_failure": "OFE03",
    "frac_sensor_fault": "OFE03",
    "frac_data": "OFE03",
    "frac_audit": "OFE03",
    "separator_trip": "OFE04",
    "separator_alarm": "OFE04",
    "separator_sensor": "OFE04",
    "separator_data": "OFE04",
    "separator_audit": "OFE04",
    "esp_failure": "OFE05",
    "sucker_rod_failure": "OFE05",
    "gas_lift_valve": "OFE05",
    "pcp_failure": "OFE05",
    "artificial_lift_alarm": "OFE05",
    "scada_trip": "OFE06",
    "scada_overload": "OFE06",
    "scada_blockage": "OFE06",
    "scada_efficiency": "OFE06",
    "scada_capacity": "OFE06",
    "scada_shutdown": "OFE06",
    "maintenance_trip": "OFE07",
    "maintenance_alarm": "OFE07",
    "maintenance_sensor": "OFE07",
    "maintenance_data": "OFE07",
    "maintenance_shutdown": "OFE07",
    "compressor_overload": "OFE08",
    "compressor_shutdown": "OFE08",
    "compressor_alarm": "OFE08",
    "compressor_blockage": "OFE08",
    "compressor_efficiency": "OFE08",
    "compressor_capacity": "OFE08",
    "compressor_sensor": "OFE08",
    "compressor_data": "OFE08",
    "compressor_audit": "OFE08",
    "wellhead_overload": "OFE09",
    "wellhead_shutdown": "OFE09",
    "wellhead_alarm": "OFE09",
    "wellhead_sensor": "OFE09",
    "wellhead_data": "OFE09",
    "wellhead_audit": "OFE09",
    "tubing_overload": "OFE10",
    "tubing_shutdown": "OFE10",
    "tubing_alarm": "OFE10",
    "tubing_sensor": "OFE10",
    "tubing_data": "OFE10",
    "tubing_audit": "OFE10",
    "valve_overload": "OFE11",
    "valve_shutdown": "OFE11",
    "valve_alarm": "OFE11",
    "valve_sensor": "OFE11",
    "valve_data": "OFE11",
    "valve_audit": "OFE11",
    "heat_exchanger_overload": "OFE12",
    "heat_exchanger_shutdown": "OFE12",
    "heat_exchanger_alarm": "OFE12",
    "heat_exchanger_sensor": "OFE12",
    "heat_exchanger_data": "OFE12",
    "heat_exchanger_audit": "OFE12",
    "pumping_unit_overload": "OFE13",
    "pumping_unit_shutdown": "OFE13",
    "pumping_unit_alarm": "OFE13",
    "pumping_unit_sensor": "OFE13",
    "pumping_unit_data": "OFE13",
    "pumping_unit_audit": "OFE13",
    "electrical_overload": "OFE14",
    "electrical_shutdown": "OFE14",
    "electrical_alarm": "OFE14",
    "electrical_sensor": "OFE14",
    "electrical_data": "OFE14",
    "electrical_audit": "OFE14",
    "safety_overload": "OFE15",
    "safety_shutdown": "OFE15",
    "safety_alarm": "OFE15",
    "safety_sensor": "OFE15",
    "safety_data": "OFE15",
    "safety_audit": "OFE15",
    # Add more as needed to reach 200+ rules
}

# METRICS COLLECTOR

class MetricsCollector:
    def __init__(self):
        self.query_times = collections.deque(maxlen=10000)
        self.error_times = collections.deque(maxlen=10000)
        self.latencies = collections.deque(maxlen=10000)
        self.query_counts = collections.Counter()
        self.error_counts = collections.Counter()
        self.lock = asyncio.Lock()

    async def record_query(self, query_id: str, latency_ms: float):
        async with self.lock:
            now = time.time()
            self.query_times.append((now, query_id))
            self.latencies.append(latency_ms)
            self.query_counts[datetime.utcnow().date()] += 1

    async def record_error(self, query_id: str, error_msg: str):
        async with self.lock:
            now = time.time()
            self.error_times.append((now, query_id, error_msg))
            self.error_counts[datetime.utcnow().date()] += 1

    async def get_latency_stats(self) -> Dict[str, Any]:
        async with self.lock:
            if not self.latencies:
                return {"min": None, "max": None, "avg": None, "p95": None, "count": 0}
            lats = list(self.latencies)
            return {
                "min": min(lats),
                "max": max(lats),
                "avg": statistics.mean(lats),
                "p95": statistics.quantiles(lats, n=100)[94] if len(lats) >= 100 else None,
                "count": len(lats),
            }

    async def queries_last_hour(self) -> int:
        async with self.lock:
            cutoff = time.time() - 3600
            return len([t for t, _ in self.query_times if t >= cutoff])

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
        topic="Triplex Mud Pump Operation Fluid End Power End Maintenance",
        keywords=[
            "triplex mud pump",
            "fluid end",
            "power end",
            "maintenance",
            "wear components",
            "seal integrity",
            "bearing lubrication",
            "API 674"
        ],
        conclusion_template=(
            "Effective maintenance of triplex mud pumps requires rigorous inspection and "
            "replacement of fluid end components to prevent failure, alongside scheduled "
            "power end lubrication and bearing checks. Adherence to API 674 standards "
            "ensures operational reliability and safety."
        ),
        reasoning_framework=(
            "Triplex mud pumps are critical for drilling fluid circulation, operating under "
            "high pressures and abrasive conditions. The fluid end, comprising liners, pistons, "
            "and valves, is subject to severe wear due to abrasive drilling mud and requires "
            "frequent inspection and timely replacement to avoid catastrophic failure. The power "
            "end, including crankshaft, crossheads, and bearings, must be regularly lubricated "
            "and monitored for vibration and temperature anomalies to prevent mechanical breakdowns. "
            "API 674 provides comprehensive guidelines for design, operation, and maintenance, "
            "emphasizing the importance of scheduled inspections and preventive maintenance. "
            "Failure to maintain the fluid end can lead to seal failures causing fluid leaks, "
            "environmental hazards, and operational downtime. Similarly, neglecting power end "
            "maintenance risks bearing seizure and crankshaft damage, which are costly to repair. "
            "A structured maintenance program integrating condition monitoring, oil analysis, "
            "and component replacement intervals based on operating hours and performance data "
            "maximizes pump uptime and safety. Operators must balance maintenance costs against "
            "the risk of unplanned failures, considering the criticality of mud pumps in drilling "
            "operations."
        ),
        key_factors=[
            "Fluid end wear rate",
            "Power end lubrication schedule",
            "Operating pressure and cycles",
            "API 674 compliance",
            "Condition monitoring data",
            "Seal integrity",
            "Bearing temperature and vibration",
            "Maintenance record accuracy"
        ],
        primary_authority=[
            "API Standard 674: Positive Displacement Pumps - Reciprocating",
            "API RP 13B-1: Recommended Practice for Field Testing Water-Based Drilling Fluids",
            "API RP 53: Blowout Prevention Equipment Systems for Drilling Wells",
            "Schlumberger Oilfield Glossary - Mud Pumps",
            "Petroleum Engineering Handbook, SPE"
        ],
        burden_holder="Maintenance and Operations Team",
        adversary_position="Cost minimization leading to deferred maintenance",
        counter_arguments=[
            "Deferred maintenance increases risk of catastrophic failure",
            "Unplanned downtime costs exceed maintenance expenses",
            "Non-compliance with API standards risks regulatory penalties",
            "Safety hazards from fluid leaks and mechanical failures",
            "Reduced pump efficiency impacts drilling performance"
        ],
        resolution_strategy=(
            "Implement a risk-based maintenance program with scheduled inspections, "
            "condition monitoring, and adherence to API 674. Use predictive analytics "
            "to optimize maintenance intervals and justify expenditures through "
            "reliability and safety improvements."
        ),
        entity_scope="Oilfield drilling operations utilizing triplex mud pumps",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 674 compliance enforcement and industry best practices"
    ),
    DoctrineBlock(
        topic="BOP Blowout Preventer Ram Annular Blind Shear Test Requirements",
        keywords=[
            "BOP",
            "blowout preventer",
            "ram preventer",
            "annular preventer",
            "blind shear ram",
            "pressure testing",
            "API 16A",
            "shear test"
        ],
        conclusion_template=(
            "Blowout preventers must undergo rigorous pressure and shear testing in "
            "accordance with API 16A to ensure integrity under well control scenarios. "
            "Blind shear rams require validated shear capability to sever drill pipe "
            "and seal the wellbore effectively."
        ),
        reasoning_framework=(
            "Blowout preventers (BOPs) are critical safety devices designed to prevent "
            "uncontrolled release of formation fluids during drilling operations. The "
            "ram preventers, including blind shear rams, must be capable of shearing "
            "through drill pipe and sealing the wellbore under extreme pressures. "
            "API 16A specifies design, testing, and performance requirements for BOP "
            "equipment, mandating pressure testing and shear testing at defined intervals. "
            "Pressure testing validates the sealing capability of the annular and ram "
            "preventers under simulated well pressures, while shear testing confirms the "
            "mechanical ability of blind shear rams to cut through drill pipe. These tests "
            "are essential to verify equipment readiness and compliance with regulatory "
            "standards such as OSHA and BSEE requirements. Failure to conduct or pass these "
            "tests can result in equipment malfunction during a well control event, "
            "potentially leading to blowouts, environmental damage, and loss of life. "
            "Proper documentation and certification of test results are mandatory for "
            "regulatory inspections and operational audits. Operators must ensure that "
            "testing is performed by qualified personnel using calibrated equipment and "
            "that any deficiencies are addressed immediately."
        ),
        key_factors=[
            "Test pressure levels",
            "Frequency of testing",
            "Shear ram cutting force",
            "Equipment certification",
            "Regulatory compliance",
            "Test procedure adherence",
            "Documentation and traceability",
            "Qualified testing personnel"
        ],
        primary_authority=[
            "API Spec 16A: Specification for Drill-through Equipment",
            "BSEE 30 CFR Part 250 Subpart Q - Blowout Preventer Systems",
            "OSHA 29 CFR 1910.119 - Process Safety Management",
            "NORSOK D-010: Well Integrity in Drilling and Well Operations",
            "Offshore Technology Conference Papers on BOP Testing"
        ],
        burden_holder="Wellsite Safety and Maintenance Personnel",
        adversary_position="Testing delays and cost avoidance",
        counter_arguments=[
            "Testing ensures functional integrity and prevents catastrophic failures",
            "Regulatory non-compliance risks fines and operational shutdowns",
            "Unverified BOPs compromise personnel safety",
            "Proper testing maintains insurance and liability coverage",
            "Early detection of equipment defects reduces long-term costs"
        ],
        resolution_strategy=(
            "Establish mandatory testing schedules aligned with API 16A and regulatory "
            "requirements, ensure qualified personnel conduct tests, and maintain "
            "comprehensive records for audits. Leverage automated test equipment to "
            "reduce time and improve accuracy."
        ),
        entity_scope="Drilling rigs equipped with BOP stacks",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="API 16A and BSEE regulatory mandates on BOP testing"
    ),
    DoctrineBlock(
        topic="Frac Pump High Pressure Positive Displacement Plunger Packing",
        keywords=[
            "frac pump",
            "high pressure",
            "positive displacement",
            "plunger packing",
            "seal integrity",
            "abrasion resistance",
            "API 674",
            "maintenance"
        ],
        conclusion_template=(
            "Maintaining plunger packing integrity in high-pressure frac pumps is essential "
            "to prevent fluid leaks and maintain operational efficiency. Use of abrasion-resistant "
            "materials and scheduled inspections per API 674 guidelines is recommended."
        ),
        reasoning_framework=(
            "Frac pumps operate at extremely high pressures to inject fracturing fluids into "
            "reservoir formations. The positive displacement design relies on plungers sealed "
            "with packing materials to prevent fluid leakage during reciprocating motion. "
            "Plunger packing is subject to wear from abrasive fluids, high temperature, and "
            "pressure cycling. Failure of packing leads to leaks, loss of pressure, and "
            "potential environmental contamination. API 674 provides standards for reciprocating "
            "pumps including material selection and maintenance practices. Selecting packing "
            "materials with high abrasion resistance, chemical compatibility, and thermal "
            "stability extends service life. Regular inspection and replacement schedules "
            "based on operating hours and fluid characteristics are critical. Additionally, "
            "monitoring for leakage and pressure drops can indicate packing degradation. "
            "Proper installation techniques and lubrication reduce wear rates. Ignoring "
            "packing maintenance risks costly downtime and safety hazards."
        ),
        key_factors=[
            "Packing material properties",
            "Operating pressure and temperature",
            "Fluid abrasiveness",
            "Inspection frequency",
            "Installation quality",
            "Lubrication methods",
            "API 674 compliance",
            "Leak detection systems"
        ],
        primary_authority=[
            "API Standard 674: Positive Displacement Pumps - Reciprocating",
            "NACE MR0175/ISO 15156: Materials for Use in H2S-containing Environments",
            "Schlumberger Frac Pump Maintenance Manuals",
            "SPE Technical Papers on Frac Pump Reliability",
            "Petroleum Equipment Institute Guidelines"
        ],
        burden_holder="Pump Maintenance Team",
        adversary_position="Extended packing use to reduce replacement costs",
        counter_arguments=[
            "Worn packing increases leak risk and environmental exposure",
            "Packing failure causes unplanned downtime and repair costs",
            "Non-compliance with API 674 risks regulatory action",
            "Safety hazards from high-pressure leaks",
            "Reduced pump efficiency impacts fracturing effectiveness"
        ],
        resolution_strategy=(
            "Implement a proactive maintenance program using condition monitoring, "
            "scheduled packing replacement, and adherence to API 674. Train personnel "
            "on proper packing installation and inspection."
        ),
        entity_scope="Hydraulic fracturing operations using positive displacement pumps",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 674 and NACE MR0175 standards on pump packing"
    ),
    DoctrineBlock(
        topic="Separator Horizontal Vertical Three-Phase FWKO Design Sizing",
        keywords=[
            "separator",
            "horizontal separator",
            "vertical separator",
            "three-phase separation",
            "FWKO",
            "design sizing",
            "fluid dynamics",
            "API 12J"
        ],
        conclusion_template=(
            "Proper design and sizing of three-phase separators, including FWKOs, must "
            "consider fluid properties, flow rates, and separation efficiency to optimize "
            "oil, gas, and water separation. API 12J provides guidelines for design parameters."
        ),
        reasoning_framework=(
            "Three-phase separators are essential for separating oil, gas, and water phases "
            "from produced fluids. Horizontal and vertical separators have different design "
            "advantages based on flow regime and space constraints. Free Water Knockout "
            "(FWKO) units are specialized separators designed to remove free water from "
            "oil streams to meet pipeline specifications. Design sizing must account for "
            "fluid properties such as density, viscosity, and surface tension, as well as "
            "flow rates and expected gas-oil-water ratios. API 12J provides empirical and "
            "analytical methods for sizing separators, including retention times, weir "
            "heights, and inlet device configurations. The choice between horizontal and "
            "vertical separators depends on factors such as footprint, ease of maintenance, "
            "and separation efficiency for specific fluid characteristics. Proper sizing "
            "ensures adequate residence time for phase separation, minimizes carryover, "
            "and reduces downstream equipment fouling. Computational fluid dynamics (CFD) "
            "and pilot testing can enhance design accuracy. Oversizing increases capital "
            "costs, while undersizing risks operational inefficiency and equipment damage."
        ),
        key_factors=[
            "Fluid flow rates and composition",
            "Density and viscosity of phases",
            "Gas-oil-water ratios",
            "Retention time requirements",
            "Separator orientation and footprint",
            "API 12J design parameters",
            "Inlet device design",
            "Operational pressure and temperature"
        ],
        primary_authority=[
            "API Standard 12J: Oil and Gas Separators",
            "ASME Boiler and Pressure Vessel Code Section VIII",
            "SPE Papers on Separator Design Optimization",
            "Petroleum Production Engineering, SPE Textbook",
            "Chevron Engineering Standards for Separators"
        ],
        burden_holder="Process Engineering and Design Teams",
        adversary_position="Minimizing separator size to reduce CAPEX",
        counter_arguments=[
            "Undersized separators cause poor phase separation and operational issues",
            "Increased maintenance and downtime due to carryover",
            "Non-compliance with pipeline specifications for water content",
            "Higher long-term operational costs from fouling and corrosion",
            "Safety risks from gas carryover and pressure surges"
        ],
        resolution_strategy=(
            "Adopt API 12J guidelines with conservative design margins, validate with "
            "CFD and pilot tests, and incorporate operational flexibility in sizing. "
            "Engage multidisciplinary teams for holistic design."
        ),
        entity_scope="Oil and gas production facilities with three-phase separation",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 12J and ASME Section VIII compliance in separator design"
    ),
    DoctrineBlock(
        topic="Artificial Lift ESP Rod Pump Gas Lift Plunger Selection Criteria",
        keywords=[
            "artificial lift",
            "ESP",
            "rod pump",
            "gas lift",
            "plunger selection",
            "lift efficiency",
            "well conditions",
            "SPE guidelines"
        ],
        conclusion_template=(
            "Selection of artificial lift methods and plunger types must be based on "
            "well production characteristics, fluid properties, and operational constraints "
            "to maximize lift efficiency and minimize downtime."
        ),
        reasoning_framework=(
            "Artificial lift systems such as Electric Submersible Pumps (ESP), rod pumps, "
            "and gas lift are employed to enhance hydrocarbon production from wells with "
            "insufficient natural reservoir pressure. The selection of the appropriate lift "
            "method and plunger type depends on multiple factors including well depth, "
            "fluid composition, gas-liquid ratio, sand production, and production rate. "
            "ESP systems are suitable for high-volume wells with low gas content but are "
            "sensitive to solids and gas interference. Rod pumps are versatile and can "
            "handle higher gas volumes but have mechanical limitations at great depths. "
            "Gas lift is effective for wells with high gas content and can be adjusted "
            "for varying production rates. Plunger design in rod pumps affects sealing "
            "efficiency, wear resistance, and ability to handle gas interference. SPE "
            "guidelines recommend evaluating well parameters such as bottom hole pressure, "
            "fluid viscosity, and gas volume fraction to select the optimal artificial lift "
            "and plunger configuration. Proper selection reduces operational costs, "
            "improves production rates, and extends equipment life."
        ),
        key_factors=[
            "Well depth and pressure",
            "Fluid composition and viscosity",
            "Gas-liquid ratio",
            "Production rate",
            "Sand and solids content",
            "Equipment availability and cost",
            "SPE artificial lift selection criteria",
            "Maintenance requirements"
        ],
        primary_authority=[
            "SPE Artificial Lift Handbook",
            "API RP 11S: Recommended Practice for Subsurface Safety Valve Installation",
            "Schlumberger Artificial Lift Engineering Guides",
            "Petroleum Production Systems, SPE Textbook",
            "Journal of Petroleum Technology Articles on Lift Optimization"
        ],
        burden_holder="Production Engineering and Well Operations",
        adversary_position="Selecting lowest cost lift method without full analysis",
        counter_arguments=[
            "Improper lift selection leads to frequent failures and downtime",
            "Reduced production and reservoir damage risk",
            "Higher lifecycle costs outweigh initial savings",
            "Safety hazards from equipment malfunction",
            "Non-optimized lift reduces recovery efficiency"
        ],
        resolution_strategy=(
            "Conduct comprehensive well evaluation using SPE guidelines, "
            "simulate lift performance, and select plunger and lift method "
            "based on technical and economic analysis."
        ),
        entity_scope="Oil and gas wells employing artificial lift systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE artificial lift best practices and field case studies"
    ),
    DoctrineBlock(
        topic="SCADA Supervisory Control Remote Monitoring Alarm Management",
        keywords=[
            "SCADA",
            "supervisory control",
            "remote monitoring",
            "alarm management",
            "cybersecurity",
            "data acquisition",
            "real-time control",
            "ISA 18.2"
        ],
        conclusion_template=(
            "Effective SCADA systems require robust supervisory control, real-time remote "
            "monitoring, and structured alarm management per ISA 18.2 to enhance operational "
            "safety and efficiency."
        ),
        reasoning_framework=(
            "SCADA (Supervisory Control and Data Acquisition) systems are integral to modern "
            "oilfield equipment management, enabling centralized monitoring and control of "
            "distributed assets. Remote monitoring facilitates real-time data acquisition on "
            "pressure, temperature, flow rates, and equipment status, allowing proactive "
            "intervention. Alarm management is critical to prevent alarm flooding and ensure "
            "operator attention to critical events. ISA 18.2 provides a framework for alarm "
            "management lifecycle including alarm philosophy, rationalization, and performance "
            "monitoring. Properly designed SCADA systems incorporate cybersecurity measures "
            "to protect against unauthorized access and data breaches, complying with NIST "
            "and IEC 62443 standards. Integration with predictive maintenance and analytics "
            "enhances decision-making. Poorly managed alarms can lead to operator fatigue, "
            "missed critical events, and safety incidents. Therefore, continuous review and "
            "optimization of alarm settings, operator training, and system redundancy are "
            "essential. SCADA systems must also ensure data integrity and availability for "
            "regulatory reporting and operational audits."
        ),
        key_factors=[
            "Alarm prioritization and rationalization",
            "Real-time data acquisition accuracy",
            "Cybersecurity compliance",
            "Operator interface usability",
            "System redundancy and failover",
            "ISA 18.2 alarm management lifecycle",
            "Integration with maintenance systems",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ISA 18.2-2016: Management of Alarm Systems for the Process Industries",
            "NIST Cybersecurity Framework",
            "IEC 62443: Industrial Communication Networks - Network and System Security",
            "API RP 1165: Recommended Practice for SCADA Security",
            "SANS Institute Industrial Control Systems Security Guidelines"
        ],
        burden_holder="Operations and IT Security Teams",
        adversary_position="Underinvestment in alarm management and cybersecurity",
        counter_arguments=[
            "Increased risk of safety incidents from alarm overload",
            "Potential for cyber attacks and operational disruption",
            "Regulatory non-compliance penalties",
            "Reduced operational efficiency and decision-making",
            "Loss of data integrity and auditability"
        ],
        resolution_strategy=(
            "Implement ISA 18.2 compliant alarm management, conduct regular cybersecurity "
            "audits, train operators, and maintain system redundancy. Use analytics to "
            "optimize alarm settings and reduce nuisance alarms."
        ),
        entity_scope="Oilfield SCADA systems for equipment monitoring and control",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="ISA 18.2 adoption and cybersecurity standards enforcement"
    ),
    DoctrineBlock(
        topic="Preventive Maintenance PM Scheduling Reliability Centered Maintenance",
        keywords=[
            "preventive maintenance",
            "PM scheduling",
            "reliability centered maintenance",
            "RCM",
            "equipment lifecycle",
            "failure modes",
            "maintenance optimization",
            "API RP 580"
        ],
        conclusion_template=(
            "Preventive maintenance scheduling guided by reliability centered maintenance "
            "principles optimizes equipment availability and reduces lifecycle costs."
        ),
        reasoning_framework=(
            "Preventive Maintenance (PM) is a proactive approach to equipment upkeep aimed "
            "at preventing unexpected failures and extending asset life. Reliability Centered "
            "Maintenance (RCM) is a structured methodology that prioritizes maintenance tasks "
            "based on failure modes, consequences, and risk assessment. RCM identifies critical "
            "components and defines maintenance strategies including preventive, predictive, "
            "and run-to-failure approaches. API RP 580 outlines risk-based inspection and "
            "maintenance planning in the petroleum industry. Effective PM scheduling requires "
            "accurate failure data, condition monitoring inputs, and operational context. "
            "Balancing maintenance frequency against operational disruptions and costs is "
            "key. Over-maintenance wastes resources, while under-maintenance risks failures "
            "and safety incidents. Implementing computerized maintenance management systems "
            "(CMMS) facilitates scheduling, tracking, and analysis. Continuous improvement "
            "through feedback loops and performance metrics such as MTBF and MTTR enhances "
            "maintenance effectiveness. Integration with predictive maintenance technologies "
            "such as vibration analysis and oil condition monitoring further refines PM plans."
        ),
        key_factors=[
            "Failure mode and effects analysis (FMEA)",
            "Equipment criticality ranking",
            "Condition monitoring data",
            "Maintenance resource availability",
            "API RP 580 risk-based inspection",
            "CMMS utilization",
            "MTBF and MTTR metrics",
            "Operational impact assessment"
        ],
        primary_authority=[
            "API RP 580: Risk-Based Inspection",
            "MIL-STD-2173: Reliability Centered Maintenance",
            "SPE Papers on Maintenance Optimization",
            "ISO 55000: Asset Management",
            "Reliability Engineering Handbook, Wiley"
        ],
        burden_holder="Maintenance Planning and Reliability Engineering",
        adversary_position="Reactive maintenance culture and budget constraints",
        counter_arguments=[
            "Reactive maintenance leads to higher downtime and repair costs",
            "Increased safety risks from unexpected failures",
            "Non-compliance with industry standards",
            "Reduced equipment life and efficiency",
            "Higher total cost of ownership"
        ],
        resolution_strategy=(
            "Adopt RCM methodology for PM scheduling, invest in condition monitoring, "
            "and use CMMS for data-driven maintenance planning. Educate stakeholders "
            "on long-term benefits."
        ),
        entity_scope="Oilfield equipment maintenance programs",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="API RP 580 and MIL-STD-2173 implementation in maintenance"
    ),
    DoctrineBlock(
        topic="Compressor Reciprocating Screw Centrifugal Gas Lift Operations",
        keywords=[
            "compressor",
            "reciprocating compressor",
            "screw compressor",
            "centrifugal compressor",
            "gas lift",
            "operational efficiency",
            "vibration analysis",
            "API 618"
        ],
        conclusion_template=(
            "Selection and operation of compressors for gas lift must consider compressor "
            "type, operational parameters, and maintenance to ensure efficiency and reliability."
        ),
        reasoning_framework=(
            "Compressors are essential in gas lift operations to inject gas into the wellbore "
            "to reduce hydrostatic pressure and enhance fluid production. Reciprocating, screw, "
            "and centrifugal compressors each have distinct operational characteristics. "
            "Reciprocating compressors provide high pressure ratios and are suitable for "
            "variable flow but require significant maintenance due to moving parts. Screw "
            "compressors offer smooth flow and lower maintenance but are limited in pressure "
            "range. Centrifugal compressors are efficient at high flow rates but less suitable "
            "for high pressure ratios. API 618 provides standards for reciprocating compressors, "
            "covering design, testing, and maintenance. Operational efficiency depends on "
            "correct compressor selection based on gas composition, flow rate, pressure "
            "requirements, and duty cycle. Vibration analysis and condition monitoring are "
            "critical to detect early mechanical issues such as bearing wear or imbalance. "
            "Proper lubrication, alignment, and cooling systems extend compressor life. "
            "Failure to maintain compressors can lead to gas lift interruptions, production "
            "loss, and safety hazards from gas leaks or overpressure."
        ),
        key_factors=[
            "Compressor type and design",
            "Gas composition and pressure requirements",
            "Flow rate and duty cycle",
            "Maintenance and lubrication",
            "Vibration and condition monitoring",
            "API 618 compliance",
            "Cooling and filtration systems",
            "Operational environment"
        ],
        primary_authority=[
            "API Standard 618: Reciprocating Compressors for Petroleum, Chemical, and Gas Industry Services",
            "ASME PTC 10: Performance Test Code for Compressors and Exhausters",
            "SPE Papers on Gas Lift Compressor Optimization",
            "Compressor Handbook, Gulf Publishing",
            "API RP 14C: Analysis, Design, Installation, and Testing of Safety Systems for Offshore Production Facilities"
        ],
        burden_holder="Operations and Maintenance Teams",
        adversary_position="Using inappropriate compressor types to cut costs",
        counter_arguments=[
            "Incorrect compressor selection reduces efficiency and increases failures",
            "Higher maintenance and downtime costs",
            "Safety risks from gas leaks and pressure surges",
            "Non-compliance with API standards",
            "Production losses from gas lift interruptions"
        ],
        resolution_strategy=(
            "Conduct thorough engineering analysis for compressor selection, "
            "implement condition monitoring, and adhere to API 618 maintenance "
            "guidelines."
        ),
        entity_scope="Gas lift operations in oil and gas production facilities",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 618 and industry best practices for compressor operation"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Christmas Tree Valve Manifold Pressure Ratings",
        keywords=[
            "wellhead equipment",
            "Christmas tree",
            "valve manifold",
            "pressure ratings",
            "API 6A",
            "pressure integrity",
            "material selection",
            "pressure testing"
        ],
        conclusion_template=(
            "Wellhead and Christmas tree equipment must be selected and maintained to "
            "withstand maximum anticipated pressures, adhering to API 6A standards to "
            "ensure pressure integrity and operational safety."
        ),
        reasoning_framework=(
            "The wellhead and Christmas tree assemblies are critical pressure-containing "
            "components installed at the surface of oil and gas wells. They provide pressure "
            "control, flow regulation, and access points for well intervention. Valve manifolds "
            "integrated into the Christmas tree must be rated for the maximum anticipated "
            "surface pressure (MAASP) and tested to verify integrity. API 6A sets forth "
            "specifications for materials, design, testing, and performance of wellhead "
            "equipment. Pressure ratings depend on design pressure class, temperature, "
            "material strength, and corrosion allowances. Material selection must consider "
            "environmental factors such as sour service and H2S exposure per NACE MR0175. "
            "Pressure testing, including hydrostatic and pneumatic tests, validate equipment "
            "integrity before installation and during maintenance. Failure to comply with "
            "pressure rating requirements risks catastrophic failure, blowouts, and safety "
            "incidents. Proper documentation and traceability of equipment certification "
            "are mandatory for regulatory compliance."
        ),
        key_factors=[
            "Maximum anticipated surface pressure (MAASP)",
            "API 6A design and material specifications",
            "Corrosion and sour service considerations",
            "Pressure testing protocols",
            "Valve manifold configuration",
            "Temperature ratings",
            "Equipment traceability and certification",
            "Maintenance and inspection schedules"
        ],
        primary_authority=[
            "API Spec 6A: Wellhead and Christmas Tree Equipment",
            "NACE MR0175/ISO 15156: Materials for Use in H2S-containing Environments",
            "ASME Boiler and Pressure Vessel Code Section VIII",
            "BSEE Regulations 30 CFR Part 250 Subpart H",
            "Offshore Technology Conference Papers on Wellhead Integrity"
        ],
        burden_holder="Wellhead Equipment Engineering and Maintenance",
        adversary_position="Using equipment with insufficient pressure rating to reduce cost",
        counter_arguments=[
            "Under-rated equipment risks catastrophic failure and blowouts",
            "Non-compliance with API 6A and regulatory standards",
            "Increased safety and environmental hazards",
            "Higher long-term costs from failures and downtime",
            "Insurance and liability implications"
        ],
        resolution_strategy=(
            "Strictly enforce API 6A pressure rating compliance, conduct rigorous "
            "pressure testing, and maintain detailed equipment certification records."
        ),
        entity_scope="Oil and gas wellhead and Christmas tree installations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="API 6A compliance and BSEE wellhead equipment regulations"
    ),
    DoctrineBlock(
        topic="Tubing Casing Design Collapse Burst Tension API Connections",
        keywords=[
            "tubing design",
            "casing design",
            "collapse pressure",
            "burst pressure",
            "tension load",
            "API connections",
            "mechanical integrity",
            "wellbore stability"
        ],
        conclusion_template=(
            "Tubing and casing must be designed considering collapse, burst, and tension "
            "loads with API connection standards to maintain wellbore mechanical integrity "
            "and operational safety."
        ),
        reasoning_framework=(
            "Tubing and casing strings provide structural support and pressure containment "
            "within the wellbore. Design must accommodate external collapse pressure from "
            "formation loads and internal burst pressure from well fluids and injection. "
            "Tension loads arise from well depth, thermal expansion, and operational forces. "
            "API specifications such as API 5CT and API 5B define material properties and "
            "connection designs to ensure mechanical integrity. Collapse resistance depends "
            "on wall thickness, grade, and external pressure conditions. Burst resistance "
            "is a function of material strength and internal pressure. Tension capacity "
            "depends on yield strength and connection design. Connections must maintain "
            "seal and mechanical strength under combined loading. Failure to properly design "
            "tubing and casing can result in wellbore instability, fluid migration, and "
            "potential blowouts. Finite element analysis and wellbore modeling assist in "
            "optimizing design. Regular inspection and pressure testing verify integrity "
            "during operations."
        ),
        key_factors=[
            "Collapse pressure rating",
            "Burst pressure rating",
            "Tension load capacity",
            "API 5CT and 5B standards",
            "Material grade and properties",
            "Connection design and torque",
            "Wellbore pressure and temperature",
            "Operational load conditions"
        ],
        primary_authority=[
            "API Spec 5CT: Specification for Casing and Tubing",
            "API Spec 5B: Threading, Gauging, and Thread Inspection of Casing and Tubing",
            "SPE Papers on Tubing and Casing Design",
            "Petroleum Engineering Handbook, SPE",
            "ASME B31.3: Process Piping"
        ],
        burden_holder="Well Design and Completion Engineering",
        adversary_position="Selecting lower grade or thinner tubing to reduce cost",
        counter_arguments=[
            "Inadequate tubing/casing leads to collapse or burst failures",
            "Compromised well integrity and safety risks",
            "Non-compliance with API standards",
            "Increased remediation and downtime costs",
            "Environmental hazards from leaks"
        ],
        resolution_strategy=(
            "Follow API design guidelines, perform rigorous load analysis, "
            "and verify connection integrity through testing and inspection."
        ),
        entity_scope="Oil and gas well completions and tubular design",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="API 5CT and 5B standards enforcement in tubular design"
    ),
    DoctrineBlock(
        topic="Valve Gate Globe Ball Check Butterfly Pressure Rating Materials",
        keywords=[
            "valve systems",
            "gate valve",
            "globe valve",
            "ball valve",
            "check valve",
            "butterfly valve",
            "pressure rating",
            "material selection"
        ],
        conclusion_template=(
            "Valve selection must consider type, pressure rating, and material compatibility "
            "to ensure reliable flow control and safety in oilfield operations."
        ),
        reasoning_framework=(
            "Valves control fluid flow in oilfield systems and must be selected based on "
            "application, pressure, temperature, and fluid characteristics. Gate valves "
            "provide full bore flow with minimal pressure drop, suitable for on/off service. "
            "Globe valves offer precise throttling control but higher pressure drop. Ball "
            "valves provide quick quarter-turn operation and tight shutoff. Check valves "
            "prevent backflow and protect equipment. Butterfly valves are compact and used "
            "for large diameter lines with moderate pressure. Pressure ratings are defined "
            "by API 6D and ASME B16.34 standards and depend on valve design and materials. "
            "Material selection must consider corrosion resistance, temperature limits, and "
            "mechanical strength. Common materials include carbon steel, stainless steel, "
            "and alloys compliant with NACE MR0175 for sour service. Improper valve selection "
            "can cause leakage, equipment damage, and safety hazards. Regular inspection and "
            "testing verify valve integrity and performance."
        ),
        key_factors=[
            "Valve type and function",
            "Pressure and temperature ratings",
            "Material compatibility",
            "API 6D and ASME B16.34 compliance",
            "Corrosion and sour service resistance",
            "Flow characteristics",
            "Maintenance and inspection history",
            "Installation environment"
        ],
        primary_authority=[
            "API Spec 6D: Specification for Pipeline Valves",
            "ASME B16.34: Valves - Flanged, Threaded, and Welding End",
            "NACE MR0175/ISO 15156",
            "Valve Manufacturers Association Technical Papers",
            "SPE Papers on Valve Selection and Maintenance"
        ],
        burden_holder="Process Engineering and Maintenance",
        adversary_position="Using valves with inadequate pressure rating or materials",
        counter_arguments=[
            "Valve failure risks leaks and operational shutdown",
            "Non-compliance with industry standards",
            "Safety and environmental hazards",
            "Increased maintenance and replacement costs",
            "Reduced system reliability"
        ],
        resolution_strategy=(
            "Select valves per API 6D and ASME standards, verify material compatibility, "
            "and conduct regular testing and maintenance."
        ),
        entity_scope="Oilfield valve systems for flow control",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 6D and ASME B16.34 standards in valve selection"
    ),
    DoctrineBlock(
        topic="Heat Exchanger Shell Tube Plate Frame Fouling LMTD Design",
        keywords=[
            "heat exchanger",
            "shell and tube",
            "plate and frame",
            "fouling",
            "log mean temperature difference",
            "LMTD",
            "thermal design",
            "API 660"
        ],
        conclusion_template=(
            "Heat exchanger design must account for fouling factors and LMTD calculations "
            "to ensure thermal efficiency and operational reliability."
        ),
        reasoning_framework=(
            "Heat exchangers transfer thermal energy between fluids and are critical in "
            "oilfield processing. Shell and tube and plate and frame are common types. "
            "Design involves calculating the Log Mean Temperature Difference (LMTD) to "
            "determine heat transfer area and performance. Fouling, the accumulation of "
            "deposits on heat transfer surfaces, reduces efficiency and increases pressure "
            "drop. API 660 provides standards for shell and tube heat exchangers including "
            "design, fabrication, and testing. Fouling factors must be included in design "
            "to maintain performance over time. Material selection affects fouling rates "
            "and corrosion resistance. Regular cleaning and monitoring are necessary to "
            "mitigate fouling effects. Thermal design must consider fluid properties, "
            "flow rates, and temperature profiles. Failure to account for fouling and "
            "accurate LMTD leads to undersized exchangers, operational inefficiency, "
            "and increased energy costs."
        ),
        key_factors=[
            "Heat transfer area",
            "LMTD calculation accuracy",
            "Fouling factors",
            "Material compatibility",
            "API 660 compliance",
            "Fluid properties and flow rates",
            "Cleaning and maintenance schedules",
            "Pressure drop considerations"
        ],
        primary_authority=[
            "API Standard 660: Shell-and-Tube Heat Exchangers",
            "TEMA Standards for Heat Exchanger Design",
            "ASME Boiler and Pressure Vessel Code Section VIII",
            "SPE Papers on Heat Exchanger Fouling and Cleaning",
            "Chemical Engineering Textbooks on Heat Transfer"
        ],
        burden_holder="Process Engineering and Maintenance Teams",
        adversary_position="Ignoring fouling in design to reduce initial costs",
        counter_arguments=[
            "Fouling reduces heat transfer efficiency and increases operating costs",
            "Increased pressure drop affects pump and compressor loads",
            "Non-compliance with API and TEMA standards",
            "Shortened equipment life and increased downtime",
            "Safety risks from overheating or thermal stress"
        ],
        resolution_strategy=(
            "Incorporate conservative fouling factors in design, schedule regular "
            "cleaning, and monitor performance to optimize heat exchanger operation."
        ),
        entity_scope="Oilfield process heat exchanger systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 660 and TEMA standards in heat exchanger design"
    ),
    DoctrineBlock(
        topic="Pumping Unit Beam Conventional Mark II Air Balanced Geometry",
        keywords=[
            "pumping unit",
            "beam pump",
            "conventional design",
            "Mark II",
            "air balanced",
            "geometry",
            "stroke length",
            "load balancing"
        ],
        conclusion_template=(
            "Pumping unit design utilizing air balanced Mark II geometry optimizes load "
            "distribution and stroke efficiency for rod pumping operations."
        ),
        reasoning_framework=(
            "Beam pumping units are widely used for artificial lift in oil wells, converting "
            "rotary motion into reciprocating motion to drive downhole pumps. The conventional "
            "Mark II design incorporates an air-balanced system to counterbalance the weight "
            "of the sucker rods and fluid column, reducing motor load and improving energy "
            "efficiency. Geometry considerations such as walking beam length, pitman arm, "
            "and horsehead shape affect stroke length and pump fill efficiency. Proper load "
            "balancing minimizes mechanical stress on components and extends equipment life. "
            "Design must account for well depth, fluid properties, and production rates. "
            "Dynamic analysis of the pumping unit ensures smooth operation and reduces "
            "vibration and wear. Advances in materials and control systems enhance performance. "
            "Regular inspection and maintenance of bearings, gearboxes, and counterweights "
            "are essential to maintain reliability."
        ),
        key_factors=[
            "Beam length and geometry",
            "Air balancing system design",
            "Stroke length and speed",
            "Load distribution",
            "Motor power requirements",
            "Well depth and fluid characteristics",
            "Maintenance and inspection",
            "Operational efficiency"
        ],
        primary_authority=[
            "API RP 11L: Recommended Practice for Design and Operation of Beam Pumping Units",
            "SPE Papers on Beam Pumping Optimization",
            "Schlumberger Artificial Lift Engineering Manuals",
            "Petroleum Engineering Handbook, SPE",
            "Oilfield Equipment Manufacturers’ Technical Guides"
        ],
        burden_holder="Artificial Lift Engineering and Operations",
        adversary_position="Using undersized or poorly balanced pumping units",
        counter_arguments=[
            "Increased mechanical wear and failure rates",
            "Higher energy consumption",
            "Reduced production efficiency",
            "Increased maintenance costs",
            "Safety risks from mechanical failures"
        ],
        resolution_strategy=(
            "Design pumping units per API RP 11L, perform dynamic load analysis, "
            "and implement regular maintenance and balancing adjustments."
        ),
        entity_scope="Rod pumping artificial lift systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 11L and industry best practices for beam pumps"
    ),
    DoctrineBlock(
        topic="Electrical Systems Motor Control Center VFD Switchgear NEC Codes",
        keywords=[
            "electrical systems",
            "motor control center",
            "VFD",
            "variable frequency drive",
            "switchgear",
            "NEC codes",
            "electrical safety",
            "equipment protection"
        ],
        conclusion_template=(
            "Electrical systems for oilfield equipment must comply with NEC codes, "
            "incorporate motor control centers and VFDs for efficient operation and "
            "ensure safety through proper switchgear design."
        ),
        reasoning_framework=(
            "Electrical systems in oilfield operations power motors, pumps, compressors, "
            "and control equipment. Motor Control Centers (MCCs) provide centralized control "
            "and protection for motors, integrating starters, overload relays, and control "
            "devices. Variable Frequency Drives (VFDs) allow speed control of motors, "
            "improving energy efficiency and process control. Switchgear assemblies protect "
            "electrical circuits from overloads, short circuits, and faults. Compliance with "
            "the National Electrical Code (NEC) ensures installation safety, grounding, "
            "and equipment protection. NEC Articles 430 (motors), 440 (VFDs), and 450 "
            "(transformers) are particularly relevant. Proper sizing, coordination, and "
            "maintenance of electrical components prevent failures and hazards such as "
            "arc flash and electrical fires. Explosion-proof and intrinsically safe designs "
            "may be required in hazardous locations per NEC Article 500. Regular inspection "
            "and testing of electrical systems maintain reliability and compliance."
        ),
        key_factors=[
            "NEC code compliance",
            "MCC design and components",
            "VFD application and settings",
            "Switchgear protection ratings",
            "Hazardous location classification",
            "Grounding and bonding",
            "Electrical maintenance programs",
            "Operator training and safety"
        ],
        primary_authority=[
            "National Electrical Code (NEC) NFPA 70",
            "IEEE Std 519: Harmonic Control in Electrical Power Systems",
            "API RP 500: Electrical Installations in Hazardous Locations",
            "IEC 61800-5-1: Adjustable Speed Electrical Power Drive Systems",
            "OSHA Electrical Safety Standards"
        ],
        burden_holder="Electrical Engineering and Safety Teams",
        adversary_position="Non-compliance to reduce installation costs",
        counter_arguments=[
            "Increased risk of electrical hazards and fires",
            "Regulatory penalties and shutdowns",
            "Equipment damage and operational downtime",
            "Safety risks to personnel",
            "Higher long-term repair costs"
        ],
        resolution_strategy=(
            "Ensure design and installation per NEC and API standards, conduct regular "
            "inspections, and provide operator training on electrical safety."
        ),
        entity_scope="Oilfield electrical power and control systems",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="NEC enforcement and API electrical safety guidelines"
    ),
    DoctrineBlock(
        topic="Safety Equipment PSV PRV Fire Suppression Gas Detection H2S",
        keywords=[
            "safety equipment",
            "PSV",
            "PRV",
            "fire suppression",
            "gas detection",
            "H2S",
            "emergency response",
            "API 520"
        ],
        conclusion_template=(
            "Safety equipment including pressure safety valves, fire suppression systems, "
            "and gas detection must be designed and maintained to protect personnel and "
            "assets from hazards such as overpressure and H2S exposure."
        ),
        reasoning_framework=(
            "Pressure Safety Valves (PSVs) and Pressure Relief Valves (PRVs) are critical "
            "for preventing overpressure in vessels and piping, protecting equipment and "
            "personnel. API 520 provides sizing and selection guidelines. Fire suppression "
            "systems, including deluge and foam systems, mitigate fire risks common in "
            "oilfield operations. Gas detection systems monitor for hazardous gases such "
            "as hydrogen sulfide (H2S), enabling early warning and evacuation. H2S is highly "
            "toxic and requires continuous monitoring with sensors calibrated to detect "
            "low ppm levels. Safety equipment must comply with OSHA, EPA, and API standards "
            "including API RP 14C and API 2218. Regular testing, maintenance, and drills "
            "ensure functionality during emergencies. Integration with SCADA and alarm "
            "systems enhances response. Failure or malfunction of safety equipment can "
            "result in catastrophic incidents, regulatory penalties, and loss of life."
        ),
        key_factors=[
            "PSV/PRV sizing and set pressure",
            "Fire suppression system type and coverage",
            "Gas detection sensor placement and sensitivity",
            "API 520 and API RP 14C compliance",
            "Maintenance and testing frequency",
            "Emergency response procedures",
            "Personnel training",
            "Integration with control systems"
        ],
        primary_authority=[
            "API Standard 520: Sizing, Selection, and Installation of Pressure-Relieving Devices",
            "OSHA 29 CFR 1910.119: Process Safety Management",
            "API RP 14C: Analysis, Design, Installation, and Testing of Safety Systems",
            "NFPA 30: Flammable and Combustible Liquids Code",
            "NIOSH Guidelines for H2S Exposure"
        ],
        burden_holder="Safety and Operations Management",
        adversary_position="Underinvestment in safety equipment and maintenance",
        counter_arguments=[
            "Increased risk of overpressure incidents and fires",
            "Potential for toxic gas exposure and fatalities",
            "Regulatory non-compliance and fines",
            "Operational shutdowns and reputational damage",
            "Higher insurance premiums and liability"
        ],
        resolution_strategy=(
            "Implement comprehensive safety equipment programs with regular testing, "
            "training, and compliance audits. Integrate safety systems with monitoring "
            "and emergency response."
        ),
        entity_scope="Oilfield facilities and production sites",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="API 520 and OSHA PSM enforcement in safety equipment"
    ),
    DoctrineBlock(
        topic="API Standards 6A 6D 11E 11AX 53 Specification Compliance",
        keywords=[
            "API standards",
            "6A",
            "6D",
            "11E",
            "11AX",
            "53",
            "specification compliance",
            "quality assurance"
        ],
        conclusion_template=(
            "Compliance with API standards 6A, 6D, 11E, 11AX, and 53 is mandatory for "
            "ensuring equipment quality, safety, and interoperability in oilfield operations."
        ),
        reasoning_framework=(
            "API standards provide industry-recognized specifications for design, "
            "manufacture, testing, and maintenance of oilfield equipment. API 6A covers "
            "wellhead and Christmas tree equipment, API 6D covers pipeline valves, API 11E "
            "and 11AX address surface safety valves and subsurface safety valves respectively, "
            "and API 53 covers blowout prevention equipment systems. Adherence to these "
            "standards ensures equipment meets minimum safety and performance criteria, "
            "facilitates interoperability, and reduces operational risks. Non-compliance "
            "can lead to equipment failure, safety incidents, regulatory penalties, and "
            "loss of operational licenses. Quality assurance programs must include "
            "verification of materials, dimensional checks, pressure testing, and "
            "documentation audits. Suppliers and operators share responsibility for "
            "compliance. Continuous updates to API standards require ongoing training "
            "and process adjustments."
        ),
        key_factors=[
            "Standard-specific design requirements",
            "Material and manufacturing quality",
            "Testing and inspection protocols",
            "Documentation and traceability",
            "Supplier certification",
            "Regulatory enforcement",
            "Training and competency",
            "Audit and compliance monitoring"
        ],
        primary_authority=[
            "API Spec 6A: Wellhead and Christmas Tree Equipment",
            "API Spec 6D: Pipeline Valves",
            "API Spec 11E: Surface Safety Valves",
            "API Spec 11AX: Subsurface Safety Valve Equipment",
            "API RP 53: Blowout Prevention Equipment Systems"
        ],
        burden_holder="Equipment Manufacturers and Operators",
        adversary_position="Cutting corners on specification compliance to reduce costs",
        counter_arguments=[
            "Non-compliant equipment risks safety and operational failures",
            "Regulatory fines and operational shutdowns",
            "Damage to corporate reputation",
            "Increased liability and insurance costs",
            "Loss of customer and stakeholder trust"
        ],
        resolution_strategy=(
            "Enforce strict quality assurance and supplier audits, maintain up-to-date "
            "training on API standards, and integrate compliance checks into procurement "
            "and operational processes."
        ),
        entity_scope="Oilfield equipment manufacturing and operations",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="API standards enforcement and industry certification programs"
    ),
    DoctrineBlock(
        topic="Corrosion Control Cathodic Protection Chemical Treatment Monitoring",
        keywords=[
            "corrosion control",
            "cathodic protection",
            "chemical treatment",
            "monitoring",
            "corrosion rate",
            "API RP 571",
            "NACE standards",
            "inspection"
        ],
        conclusion_template=(
            "Effective corrosion control requires integrated cathodic protection, chemical "
            "treatment, and continuous monitoring to prevent equipment degradation and failure."
        ),
        reasoning_framework=(
            "Corrosion is a major cause of equipment degradation in oilfield operations, "
            "leading to leaks, failures, and safety hazards. Cathodic protection (CP) "
            "systems, including impressed current and sacrificial anodes, mitigate external "
            "corrosion by controlling electrochemical reactions. Chemical treatments such "
            "as corrosion inhibitors reduce internal corrosion in pipelines and vessels. "
            "Monitoring corrosion rates through probes, coupons, and inspection techniques "
            "is essential to assess effectiveness and adjust treatments. API RP 571 provides "
            "guidelines on corrosion mechanisms and mitigation. NACE standards define CP "
            "design, installation, and monitoring practices. Integration of CP and chemical "
            "treatment programs optimizes corrosion control. Failure to implement effective "
            "corrosion control results in costly repairs, environmental damage, and safety "
            "incidents. Regular inspection and data analysis support proactive maintenance "
            "and risk management."
        ),
        key_factors=[
            "Cathodic protection system design",
            "Chemical inhibitor selection and dosage",
            "Corrosion rate monitoring",
            "API RP 571 and NACE compliance",
            "Inspection and maintenance frequency",
            "Environmental conditions",
            "Material susceptibility",
            "Data analysis and reporting"
        ],
        primary_authority=[
            "API RP 571: Damage Mechanisms Affecting Fixed Equipment in the Refining Industry",
            "NACE SP0169: Control of External Corrosion on Underground or Submerged Metallic Piping Systems",
            "NACE TM0284: Corrosion Monitoring Techniques",
            "SPE Papers on Corrosion Control in Oilfield Operations",
            "Materials Performance Journal"
        ],
        burden_holder="Corrosion Engineering and Maintenance",
        adversary_position="Underfunding corrosion control programs",
        counter_arguments=[
            "Increased risk of leaks and catastrophic failures",
            "Environmental and safety hazards",
            "Higher repair and replacement costs",
            "Regulatory non-compliance",
            "Reduced equipment life and reliability"
        ],
        resolution_strategy=(
            "Implement integrated corrosion control programs combining CP, chemical "
            "treatment, and monitoring with regular audits and data-driven adjustments."
        ),
        entity_scope="Oilfield pipelines, vessels, and equipment",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 571 and NACE standards in corrosion control"
    ),
    DoctrineBlock(
        topic="Vibration Analysis Predictive Maintenance Bearing Failure Analysis",
        keywords=[
            "vibration analysis",
            "predictive maintenance",
            "bearing failure",
            "condition monitoring",
            "FFT analysis",
            "ISO 10816",
            "fault diagnosis",
            "maintenance optimization"
        ],
        conclusion_template=(
            "Vibration analysis is a key predictive maintenance tool for early detection "
            "of bearing failures, enabling timely interventions and reducing unplanned downtime."
        ),
        reasoning_framework=(
            "Bearings are critical components in rotating equipment such as pumps, compressors, "
            "and motors. Bearing failures can cause catastrophic equipment damage and production "
            "loss. Vibration analysis uses sensors to detect characteristic frequencies and "
            "amplitudes associated with bearing defects such as outer race, inner race, and "
            "rolling element faults. Fast Fourier Transform (FFT) analysis decomposes vibration "
            "signals into frequency components for fault diagnosis. ISO 10816 provides standards "
            "for vibration severity levels and evaluation. Predictive maintenance programs "
            "integrate vibration data with other condition monitoring techniques to schedule "
            "repairs before failure. Early detection reduces maintenance costs, extends equipment "
            "life, and improves safety. Skilled analysts and calibrated equipment are essential "
            "for accurate diagnosis. Data trending and alarm thresholds support decision-making."
        ),
        key_factors=[
            "Vibration sensor placement",
            "FFT and time waveform analysis",
            "ISO 10816 severity thresholds",
            "Historical vibration trends",
            "Equipment operating conditions",
            "Analyst expertise",
            "Integration with CMMS",
            "Maintenance scheduling"
        ],
        primary_authority=[
            "ISO 10816: Mechanical Vibration - Evaluation of Machine Vibration",
            "API RP 686: Machinery Installation and Installation Design",
            "SPE Papers on Predictive Maintenance",
            "Vibration Institute Guidelines",
            "Machinery Failure Analysis and Troubleshooting, McGraw-Hill"
        ],
        burden_holder="Maintenance and Reliability Engineering",
        adversary_position="Reactive maintenance culture ignoring vibration data",
        counter_arguments=[
            "Increased unplanned downtime and repair costs",
            "Higher risk of catastrophic equipment failure",
            "Reduced equipment availability and production",
            "Safety hazards from sudden failures",
            "Inefficient maintenance resource allocation"
        ],
        resolution_strategy=(
            "Implement vibration analysis programs with trained analysts, integrate "
            "data into maintenance planning, and establish alarm thresholds per ISO 10816."
        ),
        entity_scope="Rotating equipment maintenance in oilfield operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="ISO 10816 and API RP 686 in predictive maintenance"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Equipment Iron Manifold Zipper Manifold",
        keywords=[
            "hydraulic fracturing",
            "iron manifold",
            "zipper manifold",
            "equipment configuration",
            "flow control",
            "pressure rating",
            "API RP 100-2",
            "safety"
        ],
        conclusion_template=(
            "Hydraulic fracturing manifold design, including iron and zipper manifolds, "
            "must ensure flow control, pressure integrity, and safety compliance per API RP 100-2."
        ),
        reasoning_framework=(
            "Hydraulic fracturing operations utilize complex manifold systems to distribute "
            "high-pressure fracturing fluids to multiple stages and zones. Iron manifolds "
            "are rigid piping assemblies designed for high pressure and flow rates. Zipper "
            "manifolds provide modular, flexible configurations allowing selective isolation "
            "and flow control of individual stages. Proper design must consider pressure "
            "ratings, flow balancing, and ease of operation. API RP 100-2 provides recommended "
            "practices for fracturing equipment including manifold design and safety. "
            "Manifolds must be constructed from materials resistant to corrosion and erosion "
            "due to abrasive fracturing fluids. Pressure testing and inspection ensure integrity. "
            "Safety features such as pressure relief valves and emergency shutdowns are critical. "
            "Operator training on manifold operation and emergency procedures reduces risks. "
            "Poor manifold design or operation can lead to pressure surges, leaks, and equipment "
            "failures, jeopardizing well integrity and personnel safety."
        ),
        key_factors=[
            "Manifold pressure rating",
            "Flow control valve configuration",
            "Material selection and corrosion resistance",
            "API RP 100-2 compliance",
            "Pressure testing and inspection",
            "Operator training",
            "Emergency shutdown systems",
            "Maintenance and repair protocols"
        ],
        primary_authority=[
            "API RP 100-2: Recommended Practice for Hydraulic Fracturing Equipment",
            "SPE Hydraulic Fracturing Technical Papers",
            "OSHA Process Safety Management Standards",
            "Manufacturer Technical Manuals for Manifold Systems",
            "Industry Safety Case Studies"
        ],
        burden_holder="Fracturing Operations and Safety Teams",
        adversary_position="Using undersized or poorly maintained manifolds",
        counter_arguments=[
            "Increased risk of pressure failures and leaks",
            "Operational inefficiencies and downtime",
            "Safety hazards to personnel",
            "Regulatory non-compliance",
            "Higher maintenance and replacement costs"
        ],
        resolution_strategy=(
            "Design manifolds per API RP 100-2, conduct regular inspections and tests, "
            "and provide comprehensive operator training."
        ),
        entity_scope="Hydraulic fracturing surface equipment",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 100-2 and OSHA PSM in fracturing equipment safety"
    ),
    DoctrineBlock(
        topic="Production Equipment Optimization Downtime Reduction MTBF MTTR",
        keywords=[
            "production equipment",
            "optimization",
            "downtime reduction",
            "MTBF",
            "MTTR",
            "reliability",
            "maintenance",
            "performance metrics"
        ],
        conclusion_template=(
            "Optimizing production equipment involves improving MTBF and reducing MTTR "
            "to minimize downtime and maximize operational efficiency."
        ),
        reasoning_framework=(
            "Production equipment reliability is measured by Mean Time Between Failures (MTBF) "
            "and Mean Time To Repair (MTTR). Higher MTBF indicates longer operational periods "
            "without failure, while lower MTTR reflects faster recovery from failures. "
            "Optimization strategies include preventive and predictive maintenance, equipment "
            "upgrades, operator training, and process improvements. Data collection and analysis "
            "of failure modes enable targeted interventions. Reducing downtime improves "
            "production rates and reduces costs. Reliability engineering tools such as RCM "
            "and FMEA support optimization. Integration of CMMS and real-time monitoring "
            "facilitates proactive maintenance scheduling. Continuous improvement cycles "
            "and benchmarking against industry standards drive performance gains."
        ),
        key_factors=[
            "MTBF and MTTR data accuracy",
            "Failure mode analysis",
            "Preventive and predictive maintenance",
            "Operator training",
            "Equipment upgrades",
            "CMMS utilization",
            "Process improvements",
            "Benchmarking"
        ],
        primary_authority=[
            "SPE Papers on Production Equipment Reliability",
            "MIL-STD-2173: Reliability Centered Maintenance",
            "ISO 55000: Asset Management",
            "Reliability Engineering Handbook",
            "API RP 580: Risk-Based Inspection"
        ],
        burden_holder="Operations and Maintenance Management",
        adversary_position="Reactive maintenance and ignoring reliability data",
        counter_arguments=[
            "Increased unplanned downtime and costs",
            "Reduced production and profitability",
            "Higher safety risks",
            "Equipment life reduction",
            "Loss of competitive advantage"
        ],
        resolution_strategy=(
            "Implement data-driven reliability programs, invest in training, and "
            "utilize technology for predictive maintenance."
        ),
        entity_scope="Oilfield production equipment operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Reliability engineering best practices and industry standards"
    ),
    DoctrineBlock(
        topic="Well Testing Equipment DST Flowback Choke Management",
        keywords=[
            "well testing",
            "DST",
            "flowback",
            "choke management",
            "pressure control",
            "flow rate",
            "equipment integrity",
            "SPE guidelines"
        ],
        conclusion_template=(
            "Well testing equipment and flowback choke management must be carefully "
            "controlled to ensure accurate data collection and maintain equipment integrity."
        ),
        reasoning_framework=(
            "Drill Stem Testing (DST) and flowback operations require specialized equipment "
            "to measure formation pressures, permeability, and fluid characteristics. "
            "Choke management during flowback controls flow rates and pressures to prevent "
            "equipment damage and ensure safety. Proper selection and operation of chokes "
            "minimize sand production and erosion. SPE guidelines recommend monitoring "
            "pressure and flow parameters continuously and adjusting choke settings accordingly. "
            "Equipment must be rated for expected pressures and corrosive fluids. Data "
            "accuracy depends on stable flow conditions and calibrated instruments. Failure "
            "to manage chokes properly can lead to equipment failure, inaccurate test results, "
            "and safety incidents. Training and procedural adherence are critical."
        ),
        key_factors=[
            "Choke size and type",
            "Pressure and flow monitoring",
            "Equipment pressure ratings",
            "SPE well testing guidelines",
            "Sand and solids management",
            "Operator training",
            "Data acquisition accuracy",
            "Safety protocols"
        ],
        primary_authority=[
            "SPE Well Testing Handbook",
            "API RP 53: Blowout Prevention Equipment Systems",
            "OSHA Process Safety Management Standards",
            "Manufacturer Equipment Manuals",
            "Industry Case Studies on Well Testing"
        ],
        burden_holder="Well Testing and Operations Personnel",
        adversary_position="Inadequate choke management to speed operations",
        counter_arguments=[
            "Increased risk of equipment damage and failure",
            "Inaccurate formation evaluation data",
            "Safety hazards from uncontrolled flow",
            "Regulatory non-compliance",
            "Higher operational costs"
        ],
        resolution_strategy=(
            "Implement SPE-recommended choke management procedures, continuous "
            "monitoring, and operator training."
        ),
        entity_scope="Well testing and flowback operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SPE guidelines and API RP 53 in well testing safety"
    ),
    DoctrineBlock(
        topic="Sand Control Screens Gravel Pack Frac Pack Design",
        keywords=[
            "sand control",
            "screens",
            "gravel pack",
            "frac pack",
            "wellbore protection",
            "formation sand",
            "API RP 19C",
            "completion design"
        ],
        conclusion_template=(
            "Sand control design using screens, gravel packs, and frac packs must be "
            "tailored to formation characteristics to prevent sand production and maintain well integrity."
        ),
        reasoning_framework=(
            "Sand production can damage equipment, reduce production, and cause wellbore "
            "instability. Sand control methods include mechanical screens, gravel packs, "
            "and frac packs. Screens provide a physical barrier to sand ingress. Gravel packs "
            "involve placing sized gravel around the screen to stabilize the formation and "
            "filter sand. Frac packs combine hydraulic fracturing with gravel packing to "
            "enhance conductivity and sand control in unconsolidated formations. API RP 19C "
            "provides guidelines for sand control equipment and design. Selection depends on "
            "formation properties, production rates, and completion type. Proper design "
            "minimizes formation damage and maximizes production. Installation techniques "
            "and quality control are critical. Monitoring sand production post-completion "
            "informs maintenance and remediation."
        ),
        key_factors=[
            "Formation sand characteristics",
            "Screen type and slot size",
            "Gravel size and distribution",
            "Frac pack design parameters",
            "API RP 19C compliance",
            "Completion method",
            "Installation quality",
            "Post-completion monitoring"
        ],
        primary_authority=[
            "API RP 19C: Sand Control Equipment and Procedures",
            "SPE Papers on Sand Control Techniques",
            "Petroleum Engineering Handbook, SPE",
            "Completion Engineering Textbooks",
            "Industry Case Studies on Sand Control"
        ],
        burden_holder="Completion Engineering and Operations",
        adversary_position="Minimizing sand control investment to reduce costs",
        counter_arguments=[
            "Increased equipment erosion and failures",
            "Reduced production and well life",
            "Higher remediation and workover costs",
            "Safety risks from wellbore instability",
            "Non-compliance with API standards"
        ],
        resolution_strategy=(
            "Design sand control systems per API RP 19C, conduct thorough formation "
            "evaluation, and monitor sand production continuously."
        ),
        entity_scope="Well completion and sand control operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 19C and SPE best practices in sand control"
    ),
    DoctrineBlock(
        topic="Chemical Injection Systems Corrosion Scale Paraffin Demulsifier",
        keywords=[
            "chemical injection",
            "corrosion inhibitors",
            "scale inhibitors",
            "paraffin control",
            "demulsifiers",
            "flow assurance",
            "API RP 751",
            "injection equipment"
        ],
        conclusion_template=(
            "Chemical injection systems must be designed and operated to deliver corrosion, "
            "scale, paraffin, and emulsion control chemicals effectively for flow assurance."
        ),
        reasoning_framework=(
            "Chemical injection is vital for managing flow assurance challenges in oilfield "
            "production. Corrosion inhibitors protect metal surfaces from degradation. Scale "
            "inhibitors prevent mineral deposits that restrict flow. Paraffin control chemicals "
            "reduce wax deposition, and demulsifiers separate water from oil to improve processing. "
            "API RP 751 provides guidelines for chemical injection equipment design, operation, "
            "and safety. Injection systems must ensure accurate dosing, compatibility with "
            "chemicals, and reliable operation under field conditions. Monitoring chemical "
            "effectiveness and injection rates is essential. Equipment selection includes pumps, "
            "meters, and control valves designed for corrosive fluids. Safety considerations "
            "include handling hazardous chemicals and preventing leaks. Integration with SCADA "
            "systems enhances control and monitoring."
        ),
        key_factors=[
            "Chemical compatibility and selection",
            "Injection rate accuracy",
            "Equipment material selection",
            "API RP 751 compliance",
            "Flow assurance requirements",
            "Monitoring and control systems",
            "Safety and environmental controls",
            "Operator training"
        ],
        primary_authority=[
            "API RP 751: Safe Operation of Chemical Injection Systems",
            "SPE Papers on Flow Assurance and Chemical Treatment",
            "NACE Standards on Corrosion Inhibitors",
            "Manufacturer Equipment Specifications",
            "Industry Case Studies on Chemical Injection"
        ],
        burden_holder="Production Chemistry and Operations",
        adversary_position="Under-dosing or inadequate chemical injection systems",
        counter_arguments=[
            "Increased corrosion and equipment failures",
            "Scale and paraffin buildup reducing flow",
            "Emulsion issues affecting processing",
            "Safety and environmental risks",
            "Higher remediation and replacement costs"
        ],
        resolution_strategy=(
            "Design injection systems per API RP 751, monitor chemical effectiveness, "
            "and train personnel on safe operation."
        ),
        entity_scope="Oilfield chemical injection operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 751 and NACE standards in chemical injection"
    ),
    DoctrineBlock(
        topic="Metering Equipment Orifice Turbine Coriolis Custody Transfer",
        keywords=[
            "metering equipment",
            "orifice meter",
            "turbine meter",
            "Coriolis meter",
            "custody transfer",
            "flow measurement",
            "API MPMS",
            "accuracy"
        ],
        conclusion_template=(
            "Metering equipment selection for custody transfer must ensure accuracy and "
            "compliance with API MPMS standards to guarantee fair measurement and billing."
        ),
        reasoning_framework=(
            "Accurate flow measurement is critical for custody transfer of hydrocarbons. "
            "Orifice meters measure differential pressure across an orifice plate to infer "
            "flow rate. Turbine meters use rotor speed proportional to flow velocity. Coriolis "
            "meters measure mass flow directly using vibration frequency changes. Each meter "
            "type has advantages and limitations regarding accuracy, pressure drop, and fluid "
            "compatibility. API Manual of Petroleum Measurement Standards (MPMS) provides "
            "detailed procedures for meter selection, installation, calibration, and maintenance. "
            "Custody transfer requires high accuracy and traceability to prevent disputes. "
            "Regular calibration and verification against standards are mandatory. Environmental "
            "conditions, fluid properties, and installation effects must be considered. Data "
            "integration with SCADA and billing systems ensures transparency. Failure to maintain "
            "meter accuracy risks financial losses and legal challenges."
        ),
        key_factors=[
            "Meter type and suitability",
            "Measurement accuracy and uncertainty",
            "API MPMS compliance",
            "Calibration and verification",
            "Installation effects",
            "Fluid properties",
            "Data integration",
            "Maintenance and inspection"
        ],
        primary_authority=[
            "API MPMS Chapter 5: Orifice Metering of Natural Gas and Other Related Hydrocarbon Fluids",
            "API MPMS Chapter 14: Turbine Metering",
            "API MPMS Chapter 19: Coriolis Metering",
            "NIST Handbook 44: Specifications and Tolerances for Weighing and Measuring Devices",
            "SPE Papers on Flow Measurement Accuracy"
        ],
        burden_holder="Measurement and Control Engineering",
        adversary_position="Using uncalibrated or inappropriate meters to reduce costs",
        counter_arguments=[
            "Financial losses due to inaccurate measurement",
            "Legal disputes over custody transfer",
            "Regulatory non-compliance",
            "Operational inefficiencies",
            "Loss of customer trust"
        ],
        resolution_strategy=(
            "Select meters per API MPMS, implement rigorous calibration programs, "
            "and integrate data with control systems."
        ),
        entity_scope="Oil and gas custody transfer metering systems",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="API MPMS standards and regulatory requirements"
    ),
    DoctrineBlock(
        topic="Pipeline Equipment Pig Launcher Receiver Inline Inspection",
        keywords=[
            "pipeline equipment",
            "pig launcher",
            "pig receiver",
            "inline inspection",
            "pipeline integrity",
            "API 1163",
            "smart pigs",
            "maintenance"
        ],
        conclusion_template=(
            "Pipeline pig launcher and receiver systems must be designed and maintained "
            "to facilitate inline inspection and ensure pipeline integrity per API 1163."
        ),
        reasoning_framework=(
            "Pipeline integrity management relies on regular inline inspections using "
            "pigs—devices that travel through pipelines to clean or inspect. Pig launchers "
            "and receivers provide access points for inserting and retrieving pigs. Design "
            "must accommodate pig sizes, pressure ratings, and operational conditions. "
            "API 1163 specifies requirements for inline inspection systems and procedures. "
            "Smart pigs equipped with sensors detect corrosion, cracks, and deformation. "
            "Proper launcher and receiver design ensures safe pigging operations without "
            "interrupting flow. Maintenance includes pressure testing, valve inspection, "
            "and leak detection. Failure to maintain pigging equipment compromises inspection "
            "effectiveness and pipeline safety. Operator training and procedural compliance "
            "are vital."
        ),
        key_factors=[
            "Launcher and receiver design and pressure rating",
            "API 1163 compliance",
            "Pig compatibility and sizing",
            "Inspection technology",
            "Maintenance and testing",
            "Operator training",
            "Safety protocols",
            "Data analysis and reporting"
        ],
        primary_authority=[
            "API RP 1163: In-Line Inspection Systems Qualification",
            "ASME B31.8: Gas Transmission and Distribution Piping Systems",
            "SPE Papers on Pipeline Integrity Management",
            "Pipeline and Hazardous Materials Safety Administration (PHMSA) Regulations",
            "Industry Best Practices for Pigging Operations"
        ],
        burden_holder="Pipeline Operations and Integrity Teams",
        adversary_position="Neglecting pigging equipment maintenance to reduce costs",
        counter_arguments=[
            "Reduced inspection effectiveness and pipeline risk",
            "Increased likelihood of leaks and failures",
            "Regulatory non-compliance",
            "Higher remediation and repair costs",
            "Safety and environmental hazards"
        ],
        resolution_strategy=(
            "Design and maintain pigging equipment per API 1163, conduct regular "
            "inspections, and train operators on safe pigging procedures."
        ),
        entity_scope="Oil and gas pipeline systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 1163 and PHMSA pipeline integrity regulations"
    ),
    DoctrineBlock(
        topic="Tank Battery Storage Atmospheric Pressure Vessel Inspection",
        keywords=[
            "tank battery",
            "storage tanks",
            "atmospheric pressure vessels",
            "inspection",
            "API 653",
            "corrosion monitoring",
            "leak detection",
            "maintenance"
        ],
        conclusion_template=(
            "Inspection and maintenance of tank battery atmospheric pressure vessels "
            "must comply with API 653 to ensure structural integrity and prevent leaks."
        ),
        reasoning_framework=(
            "Tank batteries consist of multiple storage tanks and associated equipment "
            "for produced fluids. Atmospheric pressure vessels store oil, water, and other "
            "fluids at near atmospheric pressure. API 653 provides guidelines for inspection, "
            "repair, alteration, and reconstruction of aboveground storage tanks. Regular "
            "inspection includes visual, ultrasonic thickness measurements, and corrosion "
            "monitoring. Leak detection systems and secondary containment reduce environmental "
            "risks. Maintenance programs address corrosion, structural damage, and operational "
            "issues. Failure to comply with API 653 risks tank failure, spills, and regulatory "
            "penalties. Documentation and inspection records support asset management and "
            "regulatory audits."
        ),
        key_factors=[
            "API 653 inspection intervals",
            "Corrosion rate monitoring",
            "Structural integrity assessment",
            "Leak detection systems",
            "Secondary containment",
            "Maintenance and repair history",
            "Documentation and record keeping",
            "Operator training"
        ],
        primary_authority=[
            "API Standard 653: Tank Inspection, Repair, Alteration, and Reconstruction",
            "EPA Spill Prevention, Control, and Countermeasure (SPCC) Rule",
            "OSHA Process Safety Management Standards",
            "SPE Papers on Tank Battery Management",
            "Industry Best Practices for Storage Tank Maintenance"
        ],
        burden_holder="Facility Operations and Maintenance",
        adversary_position="Delaying inspections to reduce operational costs",
        counter_arguments=[
            "Increased risk of tank failure and environmental spills",
            "Regulatory non-compliance and fines",
            "Higher repair and remediation costs",
            "Safety hazards to personnel",
            "Loss of operational licenses"
        ],
        resolution_strategy=(
            "Adhere to API 653 inspection schedules, implement corrosion monitoring, "
            "and maintain thorough documentation."
        ),
        entity_scope="Oilfield storage tank batteries and atmospheric vessels",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="API 653 and EPA SPCC compliance in tank maintenance"
    ),
    DoctrineBlock(
        topic="Crane Rigging Equipment Load Charts Inspection Certification",
        keywords=[
            "crane equipment",
            "rigging",
            "load charts",
            "inspection",
            "certification",
            "safety",
            "OSHA 1926",
            "NCCCO"
        ],
        conclusion_template=(
            "Crane and rigging equipment must be operated within load chart limits and "
            "undergo regular inspection and certification to ensure safe lifting operations."
        ),
        reasoning_framework=(
            "Cranes and rigging are essential for lifting heavy equipment in oilfield "
            "operations. Load charts specify maximum allowable loads at various boom lengths "
            "and angles to prevent overloading. Operators must understand and adhere to these "
            "limits. OSHA 1926 Subpart CC regulates crane operations on construction sites, "
            "requiring load-rated capacity indicators, anti-two-block devices, and competent "
            "person inspections. API RP 2D provides recommended practices for crane operations "
            "in the oilfield. Regular inspection and certification by qualified agencies ensure "
            "structural integrity and operational safety. Proper rigging selection, including "
            "slings, shackles, and spreader bars, must match the load characteristics."
        ),
        key_factors=[
            "Load chart compliance and capacity planning",
            "OSHA 1926 Subpart CC regulatory compliance",
            "Inspection frequency and certification validity",
            "Rigging selection and working load limit verification",
            "Operator competency and training records"
        ],
        primary_authority=[
            "OSHA 29 CFR 1926 Subpart CC - Cranes and Derricks",
            "API RP 2D - Recommended Practice for Operation and Maintenance of Offshore Cranes",
            "ASME B30 series - Safety Standard for Cableways, Cranes, Derricks, Hoists"
        ],
        burden_holder="Crane operator and site supervisor",
        adversary_position="Equipment is within manufacturer specifications and requires no additional inspection.",
        counter_arguments=[
            "Load chart limits apply to ideal conditions; field conditions may reduce capacity",
            "Third-party certification adds verification beyond operator self-assessment",
            "Rigging must be inspected independently from the crane",
            "Environmental factors (wind, temperature) affect safe lifting capacity",
            "Documentation trail provides audit evidence for regulatory compliance"
        ],
        resolution_strategy="Apply OSHA, API, and ASME standards for crane and rigging safety; verify certifications; match rigging to loads.",
        entity_scope="Crane operators, riggers, site supervisors, and safety personnel",
        confidence=0.91,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="OSHA 29 CFR 1926 Subpart CC"
    ),
]

# =============================================
# SUB-ENGINE ORCHESTRATION
# =============================================

class SubEngineStatus(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    UNKNOWN = auto()

class CircuitBreakerState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class RoutingMode(Enum):
    AUTO = auto()
    MANUAL = auto()
    BROADCAST = auto()
    CASCADE = auto()

class IssueCategory(Enum):
    MUD_PUMP = auto()
    BOP_STACK = auto()
    FRAC_PUMP = auto()
    SEPARATOR = auto()
    ARTIFICIAL_LIFT = auto()
    SCADA = auto()
    PREVENTIVE_MAINT = auto()
    COMPRESSOR = auto()
    WELLHEAD = auto()
    TUBING_CASING = auto()
    VALVE = auto()
    HEAT_EXCHANGER = auto()
    PUMPING_UNIT = auto()
    ELECTRICAL = auto()
    SAFETY = auto()
    UNKNOWN = auto()

QueryRequest = namedtuple("QueryRequest", ["id", "text", "mode", "user", "metadata"])
RoutingDecision = namedtuple("RoutingDecision", ["engines", "categories", "mode", "reason"])
SubEngineConfig = namedtuple("SubEngineConfig", ["id", "url", "categories", "priority"])

# --- SubEngine Registry ---

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "OFE01": SubEngineConfig("OFE01", "http://ofe01-mudpump/api/query", [IssueCategory.MUD_PUMP], 10),
    "OFE02": SubEngineConfig("OFE02", "http://ofe02-bop/api/query", [IssueCategory.BOP_STACK], 10),
    "OFE03": SubEngineConfig("OFE03", "http://ofe03-fracpump/api/query", [IssueCategory.FRAC_PUMP], 9),
    "OFE04": SubEngineConfig("OFE04", "http://ofe04-separator/api/query", [IssueCategory.SEPARATOR], 8),
    "OFE05": SubEngineConfig("OFE05", "http://ofe05-artlift/api/query", [IssueCategory.ARTIFICIAL_LIFT], 8),
    "OFE06": SubEngineConfig("OFE06", "http://ofe06-scada/api/query", [IssueCategory.SCADA], 7),
    "OFE07": SubEngineConfig("OFE07", "http://ofe07-pm/api/query", [IssueCategory.PREVENTIVE_MAINT], 7),
    "OFE08": SubEngineConfig("OFE08", "http://ofe08-compressor/api/query", [IssueCategory.COMPRESSOR], 7),
    "OFE09": SubEngineConfig("OFE09", "http://ofe09-wellhead/api/query", [IssueCategory.WELLHEAD], 7),
    "OFE10": SubEngineConfig("OFE10", "http://ofe10-tubing/api/query", [IssueCategory.TUBING_CASING], 7),
    "OFE11": SubEngineConfig("OFE11", "http://ofe11-valve/api/query", [IssueCategory.VALVE], 7),
    "OFE12": SubEngineConfig("OFE12", "http://ofe12-heatex/api/query", [IssueCategory.HEAT_EXCHANGER], 7),
    "OFE13": SubEngineConfig("OFE13", "http://ofe13-pumpingunit/api/query", [IssueCategory.PUMPING_UNIT], 7),
    "OFE14": SubEngineConfig("OFE14", "http://ofe14-electrical/api/query", [IssueCategory.ELECTRICAL], 7),
    "OFE15": SubEngineConfig("OFE15", "http://ofe15-safety/api/query", [IssueCategory.SAFETY], 10),
}

CATEGORY_KEYWORDS: Dict[IssueCategory, List[str]] = {
    IssueCategory.MUD_PUMP: ["mud pump", "slurry", "piston", "liner", "plunger"],
    IssueCategory.BOP_STACK: ["bop", "blowout preventer", "annular", "ram", "shear"],
    IssueCategory.FRAC_PUMP: ["frac pump", "fracking", "fracturing", "high pressure pump"],
    IssueCategory.SEPARATOR: ["separator", "oil-water", "gas separator", "phase separator"],
    IssueCategory.ARTIFICIAL_LIFT: ["artificial lift", "esp", "sucker rod", "gas lift", "plunger lift"],
    IssueCategory.SCADA: ["scada", "remote monitoring", "data acquisition", "plc"],
    IssueCategory.PREVENTIVE_MAINT: ["preventive maintenance", "pm", "maintenance schedule", "inspection"],
    IssueCategory.COMPRESSOR: ["compressor", "reciprocating", "centrifugal compressor", "booster"],
    IssueCategory.WELLHEAD: ["wellhead", "christmas tree", "casing head", "tubing head"],
    IssueCategory.TUBING_CASING: ["tubing", "casing", "string", "pipe", "drill pipe"],
    IssueCategory.VALVE: ["valve", "gate valve", "check valve", "choke", "control valve"],
    IssueCategory.HEAT_EXCHANGER: ["heat exchanger", "cooler", "heater", "shell and tube"],
    IssueCategory.PUMPING_UNIT: ["pumping unit", "beam pump", "horsehead", "walking beam"],
    IssueCategory.ELECTRICAL: ["electrical", "motor", "vfd", "transformer", "breaker"],
    IssueCategory.SAFETY: ["safety", "ppe", "alarm", "emergency", "shutdown"],
}

# --- Circuit Breaker Implementation ---

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=30, half_open_successes=2):
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.last_failure_time = 0
        self.recovery_timeout = recovery_timeout
        self.half_open_successes = 0
        self.half_open_successes_needed = half_open_successes

    def allow_request(self):
        if self.state == CircuitBreakerState.CLOSED:
            return True
        elif self.state == CircuitBreakerState.OPEN:
            if (time.time() - self.last_failure_time) > self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                self.half_open_successes = 0
                return True
            else:
                return False
        elif self.state == CircuitBreakerState.HALF_OPEN:
            return True

    def record_success(self):
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.half_open_successes += 1
            if self.half_open_successes >= self.half_open_successes_needed:
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
                self.half_open_successes = 0

    def record_failure(self):
        self.failure_count += 1
        if self.state == CircuitBreakerState.CLOSED:
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitBreakerState.OPEN
                self.last_failure_time = time.time()
        elif self.state == CircuitBreakerState.HALF_OPEN:
            self.state = CircuitBreakerState.OPEN
            self.last_failure_time = time.time()
            self.half_open_successes = 0

    def get_state(self):
        return self.state

# --- SubEngineHealthMonitor ---

class SubEngineHealthMonitor:
    def __init__(self, registry: Dict[str, SubEngineConfig], ttl: int = 30):
        self.registry = registry
        self.status_cache: Dict[str, Tuple[SubEngineStatus, float]] = {}
        self.ttl = ttl
        self.circuit_breakers: Dict[str, CircuitBreaker] = {
            eid: CircuitBreaker() for eid in registry
        }

    async def check_health(self, engine_id: str) -> SubEngineStatus:
        now = time.time()
        if engine_id in self.status_cache:
            status, timestamp = self.status_cache[engine_id]
            if now - timestamp < self.ttl:
                return status
        config = self.registry.get(engine_id)
        if not config:
            return SubEngineStatus.UNKNOWN
        cb = self.circuit_breakers[engine_id]
        if not cb.allow_request():
            self.status_cache[engine_id] = (SubEngineStatus.UNHEALTHY, now)
            return SubEngineStatus.UNHEALTHY
        try:
            healthy = await self._ping_engine(config.url, timeout=2.0)
            status = SubEngineStatus.HEALTHY if healthy else SubEngineStatus.UNHEALTHY
            if healthy:
                cb.record_success()
            else:
                cb.record_failure()
        except Exception:
            status = SubEngineStatus.UNHEALTHY
            cb.record_failure()
        self.status_cache[engine_id] = (status, now)
        return status

    async def check_all_health(self) -> Dict[str, SubEngineStatus]:
        results = {}
        tasks = []
        for eid in self.registry:
            tasks.append(self.check_health(eid))
        statuses = await asyncio.gather(*tasks)
        for eid, status in zip(self.registry.keys(), statuses):
            results[eid] = status
        return results

    def get_healthy_engines(self) -> List[str]:
        now = time.time()
        healthy = []
        for eid, config in self.registry.items():
            if eid in self.status_cache:
                status, timestamp = self.status_cache[eid]
                if now - timestamp < self.ttl and status == SubEngineStatus.HEALTHY:
                    healthy.append(eid)
        return healthy

    async def _ping_engine(self, url: str, timeout: float = 2.0) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url.replace("/api/query", "/api/health"), timeout=timeout) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("status", "").lower() == "ok":
                            return True
        except Exception:
            pass
        return False

    def get_circuit_breaker(self, engine_id: str) -> CircuitBreaker:
        return self.circuit_breakers[engine_id]

# --- QueryRouter ---

class QueryRouter:
    def __init__(self, registry: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.registry = registry
        self.health_monitor = health_monitor
        self.routing_rules = []  # Placeholder for advanced rules

    def route_query(self, query: QueryRequest) -> RoutingDecision:
        categories = self._classify_domain(query.text)
        mode = query.mode if query.mode else RoutingMode.AUTO
        engines = self._select_engines(categories, mode)
        if not engines:
            # Fallback: try all healthy engines
            healthy_ids = self.health_monitor.get_healthy_engines()
            engines = [self.registry[eid] for eid in healthy_ids]
            reason = "No matching engines found, fallback to healthy engines"
        else:
            reason = "Engines selected based on categories and routing mode"
        return RoutingDecision([e.id for e in engines], categories, mode, reason)

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text_l = text.lower()
        matched = set()
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in text_l:
                    matched.add(cat)
        if not matched:
            matched.add(IssueCategory.UNKNOWN)
        return list(matched)

    def _select_engines(self, categories: List[IssueCategory], mode: RoutingMode) -> List[SubEngineConfig]:
        selected = []
        for eid, config in self.registry.items():
            if any(cat in config.categories for cat in categories):
                selected.append(config)
        if mode == RoutingMode.BROADCAST:
            # All healthy engines
            healthy_ids = self.health_monitor.get_healthy_engines()
            selected = [self.registry[eid] for eid in healthy_ids]
        elif mode == RoutingMode.CASCADE:
            # Prioritize by priority
            selected = sorted(selected, key=lambda c: -c.priority)
        elif mode == RoutingMode.AUTO:
            # Score and pick top N
            scored = [(self._score_engine_relevance(config, categories), config) for config in selected]
            scored = sorted(scored, key=lambda x: -x[0])
            selected = [c for s, c in scored if s > 0]
        return selected

    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        # Placeholder for advanced rules (e.g., user, metadata, time)
        return []

    def _score_engine_relevance(self, engine: SubEngineConfig, categories: List[IssueCategory]) -> float:
        score = 0.0
        for cat in categories:
            if cat in engine.categories:
                score += 1.0
        score += engine.priority * 0.1
        return score

    def _handle_engine_failure(self, engine_id: str, error: Exception) -> List[str]:
        # Fallback: remove failed engine, try next
        cb = self.health_monitor.get_circuit_breaker(engine_id)
        cb.record_failure()
        healthy = self.health_monitor.get_healthy_engines()
        return healthy

# --- SubEngineOrchestrator ---

class SubEngineOrchestrator:
    def __init__(self, registry: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.registry = registry
        self.health_monitor = health_monitor

    async def dispatch_query(self, query: QueryRequest, engines: List[str]) -> List[Dict[str, Any]]:
        tasks = []
        for eid in engines:
            config = self.registry.get(eid)
            if config:
                tasks.append(self._call_sub_engine(config, query))
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def dispatch_parallel(self, query: QueryRequest, engines: List[str]) -> Dict[str, Any]:
        responses = await self.dispatch_query(query, engines)
        return self._merge_responses(responses)

    async def dispatch_cascade(self, query: QueryRequest, engines: List[str]) -> Any:
        for eid in engines:
            config = self.registry.get(eid)
            if not config:
                continue
            try:
                resp = await self._call_sub_engine(config, query)
                if resp and resp.get("status", "").lower() == "ok":
                    return resp
            except Exception:
                continue
        return {"status": "fail", "reason": "No sub-engine succeeded"}

    async def _call_sub_engine(self, engine_config: SubEngineConfig, query: QueryRequest) -> Dict[str, Any]:
        cb = self.health_monitor.get_circuit_breaker(engine_config.id)
        if not cb.allow_request():
            return {"engine": engine_config.id, "status": "fail", "reason": "Circuit breaker open"}
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "query_id": query.id,
                    "text": query.text,
                    "user": query.user,
                    "metadata": query.metadata,
                }
                async with session.post(engine_config.url, json=payload, timeout=5.0) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        cb.record_success()
                        return {"engine": engine_config.id, "status": "ok", "data": data}
                    else:
                        cb.record_failure()
                        return {"engine": engine_config.id, "status": "fail", "reason": f"HTTP {resp.status}"}
        except Exception as e:
            cb.record_failure()
            return {"engine": engine_config.id, "status": "fail", "reason": str(e)}

    def _merge_responses(self, responses: List[Any]) -> Dict[str, Any]:
        # Aggregate all successful responses
        merged = {"status": "ok", "responses": []}
        for resp in responses:
            if isinstance(resp, dict) and resp.get("status", "").lower() == "ok":
                merged["responses"].append(resp)
        if not merged["responses"]:
            merged["status"] = "fail"
            merged["reason"] = "No successful responses"
        return merged

    def _resolve_conflicts(self, responses: List[Any]) -> Dict[str, Any]:
        # Simple consensus: majority agreement on answer field
        answers = defaultdict(int)
        for resp in responses:
            if isinstance(resp, dict) and resp.get("status", "").lower() == "ok":
                answer = resp.get("data", {}).get("answer")
                if answer:
                    answers[answer] += 1
        if not answers:
            return {"status": "fail", "reason": "No consensus"}
        consensus = max(answers.items(), key=lambda x: x[1])
        return {"status": "ok", "answer": consensus[0], "votes": consensus[1]}

# --- Example Usage (not executed here) ---

# health_monitor = SubEngineHealthMonitor(SUB_ENGINE_REGISTRY)
# router = QueryRouter(SUB_ENGINE_REGISTRY, health_monitor)
# orchestrator = SubEngineOrchestrator(SUB_ENGINE_REGISTRY, health_monitor)

# query = QueryRequest(id="q123", text="Why is my mud pump losing pressure?", mode=RoutingMode.AUTO, user="alice", metadata={})
# decision = router.route_query(query)
# responses = await orchestrator.dispatch_parallel(query, decision.engines)
# consensus = orchestrator._resolve_conflicts(responses["responses"])

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
    Given a list of authority sources, return the dominant authority level.
    If multiple have the same highest weight, return the one with highest enum value.
    """
    if not sources:
        return None
    max_weight = -1
    dominant_authority = None
    for source in sources:
        weight = authority_weights.get(source, 0)
        if weight > max_weight:
            max_weight = weight
            dominant_authority = source
        elif weight == max_weight:
            # Tie-breaker: higher enum value wins
            if source.value > dominant_authority.value:
                dominant_authority = source
    return dominant_authority

# ---------------------------
# EPISTEMIC GUARDRAILS
# ---------------------------

BANNED_PHRASES = [
    "clearly", "obviously", "without doubt", "undeniably", "unquestionably",
    "incontrovertibly", "beyond question", "manifestly", "patently", "categorically",
    "definitely", "absolutely", "unequivocally", "incontestably", "inarguably",
    "indisputably", "irrefutably", "beyond dispute", "without reservation", "without exception",
    "infallibly", "certainly", "positively", "decisively", "categorically",
    "explicitly", "conclusively", "firmly", "resolutely", "unambiguously",
    "without fail", "without hesitation"
]

DISCLOSURE_CAVEAT = (
    "Note: The analysis avoids absolute assertions and acknowledges potential uncertainties."
)

class ConfidenceLevel(enum.Enum):
    DEFENSIBLE = 1
    AGGRESSIVE = 2
    DISCLOSURE = 3
    HIGH_RISK = 4

def apply_epistemic_guardrails(text: str) -> Tuple[str, ConfidenceLevel]:
    """
    Remove banned phrases from text and append disclosure caveat.
    Determine confidence stratification based on presence of certain keywords.
    """
    lowered_text = text.lower()
    found_banned = False
    for phrase in BANNED_PHRASES:
        pattern = re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE)
        if pattern.search(text):
            found_banned = True
            text = pattern.sub("[REDACTED]", text)

    # Confidence stratification logic
    # If banned phrases found -> HIGH_RISK
    # If hedging words present -> DISCLOSURE
    # If assertive words present -> AGGRESSIVE
    # Else DEFENSIBLE

    hedging_words = ["may", "might", "could", "possibly", "suggests", "appears", "likely", "probable"]
    assertive_words = ["will", "must", "shall", "definitely", "certainly", "undoubtedly"]

    lowered_text = text.lower()
    hedging_found = any(word in lowered_text for word in hedging_words)
    assertive_found = any(word in lowered_text for word in assertive_words)

    if found_banned:
        confidence = ConfidenceLevel.HIGH_RISK
    elif hedging_found:
        confidence = ConfidenceLevel.DISCLOSURE
    elif assertive_found:
        confidence = ConfidenceLevel.AGGRESSIVE
    else:
        confidence = ConfidenceLevel.DEFENSIBLE

    if confidence in (ConfidenceLevel.HIGH_RISK, ConfidenceLevel.DISCLOSURE):
        if DISCLOSURE_CAVEAT not in text:
            text = text.strip() + "\n\n" + DISCLOSURE_CAVEAT

    return text, confidence

# ---------------------------
# FACT FRAGILITY SCORING
# ---------------------------

def score_fact_fragility(fact: str) -> Dict[str, float]:
    """
    Score fact fragility on three dimensions:
    - verifiability: 0.0 (not verifiable) to 1.0 (fully verifiable)
    - recharacterization_risk: 0.0 (low risk) to 1.0 (high risk)
    - testimony_dependence: 0.0 (no dependence) to 1.0 (high dependence)
    """
    # Simple heuristics based on keywords and structure

    verifiability = 0.5
    recharacterization_risk = 0.5
    testimony_dependence = 0.0

    fact_lower = fact.lower()

    # Verifiability heuristics
    if any(word in fact_lower for word in ["documented", "recorded", "measured", "logged", "verified"]):
        verifiability = min(1.0, verifiability + 0.4)
    if any(word in fact_lower for word in ["alleged", "claimed", "reported", "said", "stated"]):
        verifiability = max(0.0, verifiability - 0.3)
        testimony_dependence = min(1.0, testimony_dependence + 0.5)

    # Recharacterization risk heuristics
    if any(word in fact_lower for word in ["approximate", "estimated", "around", "about", "roughly"]):
        recharacterization_risk = min(1.0, recharacterization_risk + 0.4)
    if any(word in fact_lower for word in ["exact", "precise", "definitive", "confirmed"]):
        recharacterization_risk = max(0.0, recharacterization_risk - 0.4)

    # Testimony dependence heuristics
    if any(word in fact_lower for word in ["witness", "testified", "deposed", "sworn"]):
        testimony_dependence = min(1.0, testimony_dependence + 0.7)

    # Clamp values between 0 and 1
    verifiability = max(0.0, min(1.0, verifiability))
    recharacterization_risk = max(0.0, min(1.0, recharacterization_risk))
    testimony_dependence = max(0.0, min(1.0, testimony_dependence))

    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence,
    }

# ---------------------------
# SEMANTIC NORMALIZATION
# ---------------------------

DOMAIN_TERM_MAPPINGS = {
    # 50+ domain term mappings for oilfield equipment intelligence domain
    "blowout preventer": "BOP",
    "blowout preventers": "BOP",
    "drill pipe": "DP",
    "drill pipes": "DP",
    "mud pump": "MudPump",
    "mud pumps": "MudPump",
    "rotary table": "RotaryTable",
    "rotary tables": "RotaryTable",
    "casing": "Casing",
    "casings": "Casing",
    "drill bit": "DrillBit",
    "drill bits": "DrillBit",
    "wellhead": "Wellhead",
    "well heads": "Wellhead",
    "top drive": "TopDrive",
    "top drives": "TopDrive",
    "kelly": "Kelly",
    "kellys": "Kelly",
    "derrick": "Derrick",
    "derricks": "Derrick",
    "mud logger": "MudLogger",
    "mud loggers": "MudLogger",
    "shale shaker": "ShaleShaker",
    "shale shakers": "ShaleShaker",
    "drilling fluid": "DrillingFluid",
    "drilling fluids": "DrillingFluid",
    "hydraulic fracturing": "HydraulicFracturing",
    "frac": "HydraulicFracturing",
    "frac job": "HydraulicFracturing",
    "fracturing job": "HydraulicFracturing",
    "packer": "Packer",
    "packers": "Packer",
    "production tubing": "ProductionTubing",
    "production tubings": "ProductionTubing",
    "well logging": "WellLogging",
    "well logs": "WellLogging",
    "logging while drilling": "LWD",
    "lwd": "LWD",
    "measurement while drilling": "MWD",
    "mwd": "MWD",
    "mud gas separator": "MudGasSeparator",
    "mud gas separators": "MudGasSeparator",
    "choke manifold": "ChokeManifold",
    "choke manifolds": "ChokeManifold",
    "annulus": "Annulus",
    "annuli": "Annulus",
    "flowline": "Flowline",
    "flowlines": "Flowline",
    "subsea": "Subsea",
    "subsea equipment": "Subsea",
    "well control": "WellControl",
    "well controls": "WellControl",
    "hydrocarbon": "Hydrocarbon",
    "hydrocarbons": "Hydrocarbon",
    "pressure control": "PressureControl",
    "pressure controls": "PressureControl",
    "mud weight": "MudWeight",
    "mud weights": "MudWeight",
    "drill string": "DrillString",
    "drill strings": "DrillString",
    "wireline": "Wireline",
    "wirelines": "Wireline",
    "coring": "Coring",
    "core sample": "Coring",
    "core samples": "Coring",
}

def normalize_query(text: str) -> str:
    """
    Normalize domain-specific terms in the query text to standardized terms.
    """
    text_lower = text.lower()
    for phrase, standard in DOMAIN_TERM_MAPPINGS.items():
        pattern = re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE)
        text_lower = pattern.sub(standard, text_lower)
    return text_lower

# ---------------------------
# DEEP ANALYSIS
# ---------------------------

def multi_doctrine_decomposition(query: str) -> List[str]:
    """
    Decompose query into sub-issues based on doctrine keywords and domain terms.
    """
    # Simple heuristic: split by semicolon, "and", "or", commas if multiple issues
    separators = [r';', r'\band\b', r'\bor\b', r',']
    pattern = '|'.join(separators)
    parts = re.split(pattern, query, flags=re.IGNORECASE)
    sub_issues = []
    for part in parts:
        part = part.strip()
        if part:
            sub_issues.append(part)
    return sub_issues

def build_interaction_dag(issues: List[str]) -> Dict[str, Set[str]]:
    """
    Build a dependency graph (DAG) of issues.
    For simplicity, assume issues mentioning other issues are dependent on them.
    """
    dag = defaultdict(set)
    issue_set = set(issues)
    for issue in issues:
        for other in issues:
            if other != issue and other in issue:
                dag[issue].add(other)
    # Remove cycles if any (simple approach)
    def has_cycle():
        visited = set()
        stack = set()
        def visit(node):
            if node in stack:
                return True
            if node in visited:
                return False
            stack.add(node)
            for neighbor in dag[node]:
                if visit(neighbor):
                    return True
            stack.remove(node)
            visited.add(node)
            return False
        for node in dag:
            if visit(node):
                return True
        return False
    if has_cycle():
        # Naive cycle break: remove all edges
        dag = defaultdict(set)
    return dag

def eight_step_resolution(query: str, doctrines: List[str], sub_engine_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform a full eight-step analysis:
    1. Identify issues
    2. Gather facts
    3. Apply doctrines
    4. Analyze conflicts
    5. Score fragility
    6. Resolve authority conflicts
    7. Synthesize conclusions
    8. Tag zones
    """
    # 1. Identify issues
    issues = multi_doctrine_decomposition(query)

    # 2. Gather facts (simulate from sub_engine_results)
    facts = []
    for res in sub_engine_results.values():
        facts.extend(res.get("facts", []))

    # 3. Apply doctrines (simulate application)
    doctrine_applications = {}
    for doctrine in doctrines:
        doctrine_applications[doctrine] = f"Applied doctrine {doctrine} to query."

    # 4. Analyze conflicts (simulate)
    conflicts = []
    for key1, res1 in sub_engine_results.items():
        for key2, res2 in sub_engine_results.items():
            if key1 != key2:
                # naive conflict detection
                if res1.get("conclusion") != res2.get("conclusion"):
                    conflicts.append((key1, key2))

    # 5. Score fragility
    fragility_scores = [score_fact_fragility(fact) for fact in facts]

    # 6. Resolve authority conflicts
    all_authorities = []
    for res in sub_engine_results.values():
        all_authorities.extend(res.get("authorities", []))
    dominant_authority = resolve_authority_conflict(all_authorities)

    # 7. Synthesize conclusions
    conclusions = []
    for res in sub_engine_results.values():
        conclusions.append(res.get("conclusion", "No conclusion"))
    # Simple merge: majority vote or fallback
    conclusion_counts = defaultdict(int)
    for c in conclusions:
        conclusion_counts[c] += 1
    if conclusion_counts:
        final_conclusion = max(conclusion_counts.items(), key=lambda x: x[1])[0]
    else:
        final_conclusion = "No conclusion"

    # 8. Tag zones
    tagged = zoned_analysis(final_conclusion)

    return {
        "issues": issues,
        "facts": facts,
        "doctrine_applications": doctrine_applications,
        "conflicts": conflicts,
        "fragility_scores": fragility_scores,
        "dominant_authority": dominant_authority,
        "final_conclusion": final_conclusion,
        "tagged_analysis": tagged,
    }

def zoned_analysis(conclusion: str) -> Dict[str, Any]:
    """
    Tag conclusion with zones: PLANNING, REPORTING, AUDIT
    Heuristic: keywords determine zone
    """
    zones = []
    conclusion_lower = conclusion.lower()
    if any(word in conclusion_lower for word in ["plan", "strategy", "forecast", "prepare", "design"]):
        zones.append("PLANNING")
    if any(word in conclusion_lower for word in ["report", "record", "document", "log", "summary"]):
        zones.append("REPORTING")
    if any(word in conclusion_lower for word in ["audit", "review", "inspection", "compliance", "verification"]):
        zones.append("AUDIT")
    if not zones:
        zones.append("REPORTING")  # default zone
    return {"zones": zones, "conclusion": conclusion}

# ---------------------------
# THREE LAYER RESPONSE SYSTEM
# ---------------------------

# Simulated doctrine cache for layer 1
DOCTRINE_CACHE = {
    "pressure control": "Cached analysis on pressure control doctrine.",
    "blowout preventer": "Cached analysis on BOP doctrine.",
    "drill pipe failure": "Cached analysis on drill pipe failure doctrine.",
}

# Simulated sub-engines for layer 2
def sub_engine_pressure_control(query: str) -> Dict[str, Any]:
    time.sleep(0.1)  # simulate processing delay
    return {
        "conclusion": "Pressure control is within operational parameters.",
        "facts": ["pressure readings documented", "valve status logged"],
        "authorities": [AuthorityLevel.REGULATORY],
    }

def sub_engine_bop(query: str) -> Dict[str, Any]:
    time.sleep(0.15)
    return {
        "conclusion": "BOP functioned correctly during incident.",
        "facts": ["BOP activation recorded", "maintenance logs verified"],
        "authorities": [AuthorityLevel.CASE_LAW, AuthorityLevel.PRACTICE],
    }

def sub_engine_drill_pipe(query: str) -> Dict[str, Any]:
    time.sleep(0.2)
    return {
        "conclusion": "Drill pipe failure due to material fatigue.",
        "facts": ["material fatigue analysis", "inspection reports"],
        "authorities": [AuthorityLevel.TREATISE],
    }

SUB_ENGINES = {
    "pressure control": sub_engine_pressure_control,
    "bop": sub_engine_bop,
    "drill pipe": sub_engine_drill_pipe,
}

def doctrine_cache_lookup(query: str) -> str:
    """
    Layer 1: Lookup doctrine cache for keywords in query.
    Return cached analysis if found within 200ms.
    """
    start = time.time()
    for keyword, analysis in DOCTRINE_CACHE.items():
        if keyword in query.lower():
            elapsed = (time.time() - start) * 1000
            if elapsed <= 200:
                return analysis
    return None

def semantic_search_sub_engine_routing(query: str) -> List[str]:
    """
    Layer 2: Semantic search to identify relevant sub-engines.
    Return list of keys for sub-engines to dispatch.
    """
    query_norm = normalize_query(query)
    matched_engines = []
    for key in SUB_ENGINES.keys():
        if key in query_norm:
            matched_engines.append(key)
    if not matched_engines:
        # fallback: dispatch all
        matched_engines = list(SUB_ENGINES.keys())
    return matched_engines

def deep_multi_engine_analysis(query: str, engines: List[str]) -> Dict[str, Any]:
    """
    Layer 3: Parallel dispatch to sub-engines, merge results, resolve conflicts.
    """
    results = {}
    with ThreadPoolExecutor(max_workers=len(engines)) as executor:
        future_to_engine = {executor.submit(SUB_ENGINES[engine], query): engine for engine in engines}
        for future in as_completed(future_to_engine):
            engine = future_to_engine[future]
            try:
                result = future.result()
                results[engine] = result
            except Exception:
                results[engine] = {"conclusion": "Error in sub-engine", "facts": [], "authorities": []}
    # Conflict resolution and merging done in eight_step_resolution or here simplified
    return results

def three_layer_response(query: str) -> Dict[str, Any]:
    """
    Execute the three-layer response system:
    1. Doctrine cache lookup
    2. Semantic search + sub-engine routing
    3. Deep multi-engine analysis and merge
    """
    # Layer 1
    cached = doctrine_cache_lookup(query)
    if cached:
        return {"layer": 1, "response": cached}

    # Layer 2
    engines_to_call = semantic_search_sub_engine_routing(query)
    if len(engines_to_call) == 1:
        # Single engine, call directly
        result = SUB_ENGINES[engines_to_call[0]](query)
        return {"layer": 2, "response": result}

    # Layer 3
    results = deep_multi_engine_analysis(query, engines_to_call)
    doctrines = list(DOCTRINE_CACHE.keys())
    full_analysis = eight_step_resolution(query, doctrines, results)
    return {"layer": 3, "response": full_analysis}

# ---------------------------
# MODULE TESTING (disabled)
# ---------------------------

# if __name__ == "__main__":
#     test_query = "Evaluate the blowout preventer and pressure control during the drill pipe failure incident."
#     response = three_layer_response(test_query)
#     print(response)

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
        self._doctrine_hits: Counter = Counter()
        self._doctrine_total: Counter = Counter()
        self._sub_engine_stats: DefaultDict[str, List[float]] = defaultdict(list)
        self._sub_engine_errors: DefaultDict[str, int] = defaultdict(int)
        self._sub_engine_invocations: DefaultDict[str, int] = defaultdict(int)
        self._query_deque: deque = deque()  # (timestamp, QueryTelemetry)
        self._query_id_map: Dict[str, QueryTelemetry] = {}

    def record_query(self, telemetry: QueryTelemetry):
        with self._lock:
            self._queries.append(telemetry)
            self._query_deque.append((telemetry.timestamp, telemetry))
            self._query_id_map[telemetry.query_id] = telemetry
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
            latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
            if not latencies:
                return {
                    "avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None
                }
            lat_sorted = sorted(latencies)
            n = len(lat_sorted)
            def percentile(p):
                if n == 0: return None
                k = int(round(p * n + 0.5)) - 1
                return lat_sorted[min(max(k, 0), n-1)]
            return {
                "avg": statistics.mean(lat_sorted),
                "p50": percentile(0.5),
                "p95": percentile(0.95),
                "p99": percentile(0.99),
                "min": lat_sorted[0],
                "max": lat_sorted[-1]
            }

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        with self._lock:
            rates = {}
            for mode in self._doctrine_total:
                total = self._doctrine_total[mode]
                hits = self._doctrine_hits[mode]
                rates[mode] = hits / total if total else 0.0
            return rates

    def queries_last_hour(self) -> List[QueryTelemetry]:
        cutoff = time.time() - 3600
        with self._lock:
            while self._query_deque and self._query_deque[0][0] < cutoff:
                self._query_deque.popleft()
            return [qt for _, qt in self._query_deque]

    def get_sub_engine_stats(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            stats = {}
            for engine, lats in self._sub_engine_stats.items():
                if not lats:
                    stats[engine] = {
                        "avg_latency": None,
                        "p95_latency": None,
                        "invocations": 0,
                        "errors": self._sub_engine_errors[engine]
                    }
                else:
                    lats_sorted = sorted(lats)
                    n = len(lats_sorted)
                    p95 = lats_sorted[int(n*0.95)-1] if n > 0 else None
                    stats[engine] = {
                        "avg_latency": statistics.mean(lats_sorted),
                        "p95_latency": p95,
                        "invocations": self._sub_engine_invocations[engine],
                        "errors": self._sub_engine_errors[engine]
                    }
            return stats

    def get_query_by_id(self, query_id: str) -> Optional[QueryTelemetry]:
        with self._lock:
            return self._query_id_map.get(query_id)

    def get_all_queries(self) -> List[QueryTelemetry]:
        with self._lock:
            return list(self._queries)

    def get_all_errors(self) -> List[QueryTelemetry]:
        with self._lock:
            return list(self._errors)

# --- 2. DRIFT_WATCHER ---

class DriftWatcher:
    def __init__(self, window_size: int = 100):
        self._lock = threading.Lock()
        self._baseline_confidence: Dict[str, float] = {}  # doctrine -> baseline
        self._recent_confidences: DefaultDict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self._drift_alerts: List[Tuple[str, float, float, float, float]] = []  # (doctrine, prev, curr, shift, timestamp)
        self._window_size = window_size

    def record_baseline(self, doctrine: str, confidence: float):
        with self._lock:
            self._baseline_confidence[doctrine] = confidence

    def record_confidence(self, doctrine: str, confidence: float):
        with self._lock:
            dq = self._recent_confidences[doctrine]
            dq.append(confidence)
            if len(dq) == dq.maxlen:
                prev_avg = self._baseline_confidence.get(doctrine, None)
                curr_avg = sum(dq) / len(dq)
                if prev_avg is not None:
                    shift = abs(curr_avg - prev_avg) / (prev_avg + 1e-8)
                    if shift > 0.10:
                        self._drift_alerts.append((doctrine, prev_avg, curr_avg, shift, time.time()))
                        self._baseline_confidence[doctrine] = curr_avg

    def detect_drift(self, doctrine: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            if doctrine not in self._recent_confidences or doctrine not in self._baseline_confidence:
                return None
            dq = self._recent_confidences[doctrine]
            if not dq:
                return None
            curr_avg = sum(dq) / len(dq)
            prev_avg = self._baseline_confidence[doctrine]
            shift = abs(curr_avg - prev_avg) / (prev_avg + 1e-8)
            if shift > 0.10:
                return {
                    "doctrine": doctrine,
                    "baseline": prev_avg,
                    "current": curr_avg,
                    "shift": shift,
                    "alert": True
                }
            return {
                "doctrine": doctrine,
                "baseline": prev_avg,
                "current": curr_avg,
                "shift": shift,
                "alert": False
            }

    def get_drift_report(self) -> List[Dict[str, Any]]:
        with self._lock:
            report = []
            for doctrine in self._recent_confidences:
                res = self.detect_drift(doctrine)
                if res:
                    report.append(res)
            return report

    def get_drift_alerts(self) -> List[Tuple[str, float, float, float, float]]:
        with self._lock:
            return list(self._drift_alerts)

    def reset_alerts(self):
        with self._lock:
            self._drift_alerts.clear()

# --- 3. COVERAGE_MAP ---

class CoverageTracker:
    def __init__(self):
        self._lock = threading.Lock()
        self._doctrine_triggered: Counter = Counter()
        self._doctrine_missed: Counter = Counter()
        self._epistemic_gap_queries: List[str] = []
        self._sub_engine_coverage: DefaultDict[str, Counter] = defaultdict(Counter)
        self._query_to_doctrines: Dict[str, Set[str]] = {}
        self._query_to_subengines: Dict[str, Set[str]] = {}

    def record_triggered(self, query_id: str, doctrine: str, sub_engine: Optional[str] = None):
        with self._lock:
            self._doctrine_triggered[doctrine] += 1
            if sub_engine:
                self._sub_engine_coverage[sub_engine][doctrine] += 1
            if query_id not in self._query_to_doctrines:
                self._query_to_doctrines[query_id] = set()
            self._query_to_doctrines[query_id].add(doctrine)
            if sub_engine:
                if query_id not in self._query_to_subengines:
                    self._query_to_subengines[query_id] = set()
                self._query_to_subengines[query_id].add(sub_engine)

    def record_missed(self, query_id: str):
        with self._lock:
            self._doctrine_missed[query_id] += 1
            if query_id not in self._query_to_doctrines or not self._query_to_doctrines[query_id]:
                self._epistemic_gap_queries.append(query_id)

    def get_coverage_report(self) -> Dict[str, Any]:
        with self._lock:
            doctrine_total = sum(self._doctrine_triggered.values())
            doctrine_coverage = {
                doctrine: count / doctrine_total if doctrine_total else 0.0
                for doctrine, count in self._doctrine_triggered.items()
            }
            sub_engine_coverage = {
                se: dict(c) for se, c in self._sub_engine_coverage.items()
            }
            return {
                "doctrine_coverage": doctrine_coverage,
                "sub_engine_coverage": sub_engine_coverage,
                "epistemic_gap_queries": list(self._epistemic_gap_queries)
            }

    def get_epistemic_gap_queries(self) -> List[str]:
        with self._lock:
            return list(self._epistemic_gap_queries)

    def get_per_sub_engine_coverage(self) -> Dict[str, Dict[str, int]]:
        with self._lock:
            return {se: dict(c) for se, c in self._sub_engine_coverage.items()}

    def get_query_doctrines(self, query_id: str) -> Set[str]:
        with self._lock:
            return self._query_to_doctrines.get(query_id, set())

    def get_query_subengines(self, query_id: str) -> Set[str]:
        with self._lock:
            return self._query_to_subengines.get(query_id, set())

# --- 4. DETERMINISM_HASH ---

def compute_determinism_hash(query: Any, response: Any) -> str:
    """
    Compute a SHA-256 hash of the normalized query and response.
    Ensures reproducibility verification.
    """
    def normalize(obj):
        if isinstance(obj, dict):
            return {k: normalize(obj[k]) for k in sorted(obj)}
        elif isinstance(obj, list):
            return [normalize(x) for x in obj]
        elif isinstance(obj, float):
            # Round floats for determinism
            return round(obj, 8)
        else:
            return obj
    norm_query = normalize(query)
    norm_response = normalize(response)
    data = json.dumps({"query": norm_query, "response": norm_response}, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def verify_reproducibility(query: Any, response: Any, expected_hash: str) -> bool:
    return compute_determinism_hash(query, response) == expected_hash

# --- 5. AUDIT_TRAIL ---

class AuditTrailWriter:
    def __init__(self, log_dir: str):
        self.log_dir = log_dir
        self._lock = threading.Lock()
        self._current_date = None
        self._file = None
        self._open_new_file()

    def _get_log_path(self, date: datetime.date) -> str:
        fname = f"oilfield_audit_{date.isoformat()}.jsonl"
        return os.path.join(self.log_dir, fname)

    def _open_new_file(self):
        today = datetime.date.today()
        if self._current_date != today:
            if self._file:
                self._file.close()
            os.makedirs(self.log_dir, exist_ok=True)
            path = self._get_log_path(today)
            self._file = open(path, 'a', encoding='utf-8')
            self._current_date = today

    def write(self, query_id: str, timestamp: float, engine_id: str,
              engines_invoked: List[str], mode: str, confidence: float,
              latency: float, cache_hit: bool):
        with self._lock:
            self._open_new_file()
            entry = {
                "query_id": query_id,
                "timestamp": timestamp,
                "engine_id": engine_id,
                "engines_invoked": engines_invoked,
                "mode": mode,
                "confidence": confidence,
                "latency": latency,
                "cache_hit": cache_hit
            }
            self._file.write(json.dumps(entry, separators=(',', ':')) + '\n')
            self._file.flush()

    def forensic_replay(self, date: Optional[datetime.date] = None) -> List[Dict[str, Any]]:
        if date is None:
            date = datetime.date.today()
        path = self._get_log_path(date)
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return [json.loads(line) for line in f]

    def close(self):
        with self._lock:
            if self._file:
                self._file.close()
                self._file = None

# --- 6. PERFORMANCE_PROFILER ---

class PerformanceProfiler:
    def __init__(self, window_size: int = 1000):
        self._lock = threading.Lock()
        self._sub_engine_latency: DefaultDict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self._sub_engine_errors: DefaultDict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self._sub_engine_availability: DefaultDict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self._sub_engine_sla: Dict[str, Dict[str, float]] = {}  # engine -> {'max_latency': x, 'max_error_rate': y, 'min_availability': z}
        self._sla_violations: List[Dict[str, Any]] = []

    def record(self, engine: str, latency: float, error: bool, available: bool):
        with self._lock:
            self._sub_engine_latency[engine].append(latency)
            self._sub_engine_errors[engine].append(1 if error else 0)
            self._sub_engine_availability[engine].append(1 if available else 0)
            self._check_sla(engine)

    def set_sla(self, engine: str, max_latency: float, max_error_rate: float, min_availability: float):
        with self._lock:
            self._sub_engine_sla[engine] = {
                "max_latency": max_latency,
                "max_error_rate": max_error_rate,
                "min_availability": min_availability
            }

    def _check_sla(self, engine: str):
        if engine not in self._sub_engine_sla:
            return
        lats = self._sub_engine_latency[engine]
        errs = self._sub_engine_errors[engine]
        avails = self._sub_engine_availability[engine]
        if not lats or not avails:
            return
        avg_latency = statistics.mean(lats)
        error_rate = sum(errs) / len(errs) if errs else 0.0
        availability = sum(avails) / len(avails) if avails else 0.0
        sla = self._sub_engine_sla[engine]
        violation = False
        reasons = []
        if avg_latency > sla["max_latency"]:
            violation = True
            reasons.append(f"latency {avg_latency:.2f} > {sla['max_latency']}")
        if error_rate > sla["max_error_rate"]:
            violation = True
            reasons.append(f"error_rate {error_rate:.3f} > {sla['max_error_rate']}")
        if availability < sla["min_availability"]:
            violation = True
            reasons.append(f"availability {availability:.3f} < {sla['min_availability']}")
        if violation:
            self._sla_violations.append({
                "engine": engine,
                "timestamp": time.time(),
                "avg_latency": avg_latency,
                "error_rate": error_rate,
                "availability": availability,
                "reasons": reasons
            })

    def get_sub_engine_performance(self, engine: str) -> Dict[str, Any]:
        with self._lock:
            lats = self._sub_engine_latency[engine]
            errs = self._sub_engine_errors[engine]
            avails = self._sub_engine_availability[engine]
            if not lats:
                return {
                    "avg_latency": None,
                    "p95_latency": None,
                    "error_rate": None,
                    "availability": None
                }
            lats_sorted = sorted(lats)
            n = len(lats_sorted)
            p95 = lats_sorted[int(n*0.95)-1] if n > 0 else None
            error_rate = sum(errs) / len(errs) if errs else 0.0
            availability = sum(avails) / len(avails) if avails else 0.0
            return {
                "avg_latency": statistics.mean(lats_sorted),
                "p95_latency": p95,
                "error_rate": error_rate,
                "availability": availability
            }

    def get_all_performance(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return {
                engine: self.get_sub_engine_performance(engine)
                for engine in self._sub_engine_latency
            }

    def get_sla_violations(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._sla_violations)

    def reset_sla_violations(self):
        with self._lock:
            self._sla_violations.clear()

# --- END OF PART 5 ---

ENGINE_ID = "OFEIE"
ENGINE_PORT = 8850
SUB_ENGINES = {
    "OFE01": "Mud Pump Systems",
    "OFE02": "BOP Stack Analysis",
    "OFE03": "Frac Pump Operations",
    "OFE04": "Separator Design",
    "OFE05": "Artificial Lift Systems",
    "OFE06": "SCADA Monitoring",
    "OFE07": "Preventive Maintenance",
    "OFE08": "Compressor Operations",
    "OFE09": "Wellhead Equipment",
    "OFE10": "Tubing and Casing",
    "OFE11": "Valve Systems",
    "OFE12": "Heat Exchangers",
    "OFE13": "Pumping Unit Design",
    "OFE14": "Electrical Systems",
    "OFE15": "Safety Equipment",
}

# Timeout for sub-engine calls in seconds
SUB_ENGINE_TIMEOUT = 5

# Circuit breaker thresholds
CIRCUIT_BREAKER_FAILURE_THRESHOLD = 3
CIRCUIT_BREAKER_RESET_TIMEOUT = 60  # seconds

# -------------------------
# Logger Setup
# -------------------------

logger = logging.getLogger("OFEIE_Orchestrator")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# -------------------------
# Data Models
# -------------------------

class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class RouteDryRunRequest(BaseModel):
    query: str

class AnalyzeRequest(BaseModel):
    query: str
    depth: Optional[int] = 3
    engines: Optional[List[str]] = None

class SubEngineResponse(BaseModel):
    engine_id: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    latency_ms: Optional[int] = None

class HealthStatus(BaseModel):
    engine_id: str
    status: str
    last_checked: datetime
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
    details: Optional[Dict[str, Any]] = None

class DoctrineInfo(BaseModel):
    doctrine_id: str
    description: str
    last_updated: datetime

class RoutingRule(BaseModel):
    rule_id: str
    description: str
    engines: List[str]

class RoutingInfo(BaseModel):
    routing_rules: List[RoutingRule]
    engine_registry: Dict[str, str]

class SubEngineHealthDashboard(BaseModel):
    sub_engines: List[HealthStatus]

# -------------------------
# Global State and Caches
# -------------------------

class CircuitBreaker:
    def __init__(self):
        self.failure_count = 0
        self.last_failure_time = None
        self.open_until = None
        self.lock = threading.Lock()

    def record_failure(self):
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = datetime.utcnow()
            if self.failure_count >= CIRCUIT_BREAKER_FAILURE_THRESHOLD:
                self.open_until = datetime.utcnow() + timedelta(seconds=CIRCUIT_BREAKER_RESET_TIMEOUT)
                logger.warning(f"Circuit breaker opened until {self.open_until}")

    def record_success(self):
        with self.lock:
            self.failure_count = 0
            self.open_until = None

    def is_open(self):
        with self.lock:
            if self.open_until is None:
                return False
            if datetime.utcnow() >= self.open_until:
                self.failure_count = 0
                self.open_until = None
                return False
            return True

class DoctrineCache:
    def __init__(self):
        self.cache = {}
        self.lock = threading.Lock()

    def initialize(self):
        # Simulate doctrine cache initialization
        with self.lock:
            self.cache = {
                "doctrine_001": {
                    "description": "Mud Pump operational parameters",
                    "last_updated": datetime.utcnow() - timedelta(days=1),
                    "coverage": 0.95,
                },
                "doctrine_002": {
                    "description": "BOP Stack safety protocols",
                    "last_updated": datetime.utcnow() - timedelta(days=2),
                    "coverage": 0.90,
                },
                # ... more doctrines ...
            }
        logger.info("Doctrine cache initialized with %d doctrines", len(self.cache))

    def get_all(self):
        with self.lock:
            return self.cache.copy()

    def get(self, doctrine_id):
        with self.lock:
            return self.cache.get(doctrine_id)

class SearchIndex:
    def __init__(self):
        self.index = {}
        self.lock = threading.Lock()

    def seed(self):
        # Simulate seeding search index
        with self.lock:
            self.index = {
                "mud pump": ["OFE01"],
                "bop stack": ["OFE02"],
                "frac pump": ["OFE03"],
                "separator": ["OFE04"],
                "artificial lift": ["OFE05"],
                "scada": ["OFE06"],
                "maintenance": ["OFE07"],
                "compressor": ["OFE08"],
                "wellhead": ["OFE09"],
                "tubing": ["OFE10"],
                "valve": ["OFE11"],
                "heat exchanger": ["OFE12"],
                "pumping unit": ["OFE13"],
                "electrical": ["OFE14"],
                "safety": ["OFE15"],
            }
        logger.info("Search index seeded with %d keywords", len(self.index))

    def search(self, query: str) -> List[str]:
        # Simple keyword matching to sub-engines
        with self.lock:
            matched_engines = set()
            query_lower = query.lower()
            for keyword, engines in self.index.items():
                if keyword in query_lower:
                    matched_engines.update(engines)
            return list(matched_engines)

class Telemetry:
    def __init__(self):
        self.query_count = 0
        self.cache_hits = 0
        self.latencies = []
        self.lock = threading.Lock()

    def record_query(self, latency_ms: int, cache_hit: bool):
        with self.lock:
            self.query_count += 1
            if cache_hit:
                self.cache_hits += 1
            self.latencies.append(latency_ms)
            if len(self.latencies) > 1000:
                self.latencies.pop(0)

    def get_metrics(self):
        with self.lock:
            count = self.query_count
            hits = self.cache_hits
            latencies = self.latencies.copy()
        hit_rate = hits / count if count > 0 else 0.0
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        p95_latency = sorted(latencies)[int(len(latencies)*0.95)] if latencies else 0.0
        queries_per_hour = count / ((time.time() - start_time) / 3600) if start_time else 0.0
        return {
            "total_queries": count,
            "cache_hit_rate": hit_rate,
            "average_latency_ms": avg_latency,
            "p95_latency_ms": p95_latency,
            "queries_per_hour": queries_per_hour,
        }

# -------------------------
# Sub-Engine Client Simulations
# -------------------------

class SubEngineClient:
    def __init__(self, engine_id: str, name: str):
        self.engine_id = engine_id
        self.name = name
        self.circuit_breaker = CircuitBreaker()
        self.lock = threading.Lock()
        self.last_health_check = None
        self.status = "unknown"
        self.failure_count = 0
        self.success_count = 0

    async def query(self, query: str, context: Optional[Dict[str, Any]] = None) -> SubEngineResponse:
        if self.circuit_breaker.is_open():
            logger.warning(f"Sub-engine {self.engine_id} circuit breaker is open. Failing fast.")
            return SubEngineResponse(
                engine_id=self.engine_id,
                success=False,
                error="Circuit breaker open",
                latency_ms=0,
            )
        start = time.time()
        try:
            # Simulate network call latency and possible failure
            await asyncio.sleep(random.uniform(0.1, 0.5))
            # Simulate failure with 10% chance
            if random.random() < 0.1:
                raise Exception("Simulated sub-engine failure")
            # Simulated response data
            data = {
                "engine_id": self.engine_id,
                "result": f"Processed query '{query}' in {self.name}",
                "details": {
                    "processed_at": datetime.utcnow().isoformat()
                }
            }
            latency_ms = int((time.time() - start) * 1000)
            self.circuit_breaker.record_success()
            with self.lock:
                self.success_count += 1
            return SubEngineResponse(
                engine_id=self.engine_id,
                success=True,
                data=data,
                latency_ms=latency_ms,
            )
        except Exception as e:
            latency_ms = int((time.time() - start) * 1000)
            self.circuit_breaker.record_failure()
            with self.lock:
                self.failure_count += 1
            logger.error(f"Sub-engine {self.engine_id} failed: {str(e)}")
            return SubEngineResponse(
                engine_id=self.engine_id,
                success=False,
                error=str(e),
                latency_ms=latency_ms,
            )

    async def health_check(self) -> HealthStatus:
        # Simulate health check
        await asyncio.sleep(random.uniform(0.05, 0.2))
        status = "healthy" if random.random() > 0.05 else "degraded"
        self.last_health_check = datetime.utcnow()
        self.status = status
        return HealthStatus(
            engine_id=self.engine_id,
            status=status,
            last_checked=self.last_health_check,
            details={
                "success_count": self.success_count,
                "failure_count": self.failure_count,
                "circuit_breaker_open": self.circuit_breaker.is_open(),
            }
        )

    def get_stats(self):
        with self.lock:
            return {
                "success_count": self.success_count,
                "failure_count": self.failure_count,
                "circuit_breaker_open": self.circuit_breaker.is_open(),
            }

# -------------------------
# Orchestrator Core Logic
# -------------------------

class Orchestrator:
    def __init__(self):
        self.doctrine_cache = DoctrineCache()
        self.search_index = SearchIndex()
        self.telemetry = Telemetry()
        self.sub_engines = {
            eid: SubEngineClient(eid, name)
            for eid, name in SUB_ENGINES.items()
        }
        self.routing_rules = [
            RoutingRule(
                rule_id="rule_001",
                description="Route queries containing 'pump' to pump-related engines",
                engines=["OFE01", "OFE03", "OFE13"]
            ),
            RoutingRule(
                rule_id="rule_002",
                description="Route queries containing 'safety' to safety and BOP engines",
                engines=["OFE02", "OFE15"]
            ),
            RoutingRule(
                rule_id="rule_003",
                description="Route queries containing 'compressor' to compressor engine",
                engines=["OFE08"]
            ),
            # ... more rules ...
        ]
        self.lock = threading.Lock()

    async def lifespan_startup(self):
        logger.info("Orchestrator lifespan startup initiated.")
        self.doctrine_cache.initialize()
        self.search_index.seed()
        # Start health monitor and telemetry background tasks
        self.health_monitor_task = asyncio.create_task(self.health_monitor())
        self.telemetry_task = asyncio.create_task(self.telemetry_reporter())
        logger.info("Orchestrator lifespan startup completed.")

    async def lifespan_shutdown(self):
        logger.info("Orchestrator lifespan shutdown initiated.")
        self.health_monitor_task.cancel()
        self.telemetry_task.cancel()
        try:
            await self.health_monitor_task
        except asyncio.CancelledError:
            pass
        try:
            await self.telemetry_task
        except asyncio.CancelledError:
            pass
        logger.info("Orchestrator lifespan shutdown completed.")

    async def health_monitor(self):
        while True:
            try:
                await asyncio.gather(*[
                    se.health_check() for se in self.sub_engines.values()
                ])
                await asyncio.sleep(30)
            except asyncio.CancelledError:
                logger.info("Health monitor task cancelled.")
                break
            except Exception as e:
                logger.error(f"Health monitor error: {str(e)}")
                await asyncio.sleep(30)

    async def telemetry_reporter(self):
        while True:
            try:
                metrics = self.telemetry.get_metrics()
                logger.info(f"Telemetry metrics: {metrics}")
                await asyncio.sleep(60)
            except asyncio.CancelledError:
                logger.info("Telemetry reporter task cancelled.")
                break
            except Exception as e:
                logger.error(f"Telemetry reporter error: {str(e)}")
                await asyncio.sleep(60)

    def normalize_query(self, query: str) -> str:
        # Basic normalization: strip, lowercase
        normalized = query.strip().lower()
        logger.debug(f"Normalized query: {normalized}")
        return normalized

    def classify_domain(self, query: str) -> List[str]:
        # Use search index to find relevant sub-engines
        engines = self.search_index.search(query)
        logger.debug(f"Classified domain engines: {engines}")
        return engines

    def route_query(self, classified_engines: List[str]) -> List[str]:
        # Apply routing rules to refine engine list
        routed_engines = set()
        for rule in self.routing_rules:
            if any(engine in classified_engines for engine in rule.engines):
                routed_engines.update(rule.engines)
        if not routed_engines:
            routed_engines = set(classified_engines)
        logger.debug(f"Routed engines: {routed_engines}")
        return list(routed_engines)

    async def dispatch_query(self, query: str, engines: List[str], context: Optional[Dict[str, Any]] = None) -> List[SubEngineResponse]:
        tasks = []
        for engine_id in engines:
            client = self.sub_engines.get(engine_id)
            if client:
                tasks.append(
                    asyncio.wait_for(client.query(query, context), timeout=SUB_ENGINE_TIMEOUT)
                )
        responses = []
        for task in asyncio.as_completed(tasks):
            try:
                resp = await task
                responses.append(resp)
            except asyncio.TimeoutError:
                logger.error("Sub-engine query timed out")
                responses.append(SubEngineResponse(
                    engine_id="unknown",
                    success=False,
                    error="Timeout",
                    latency_ms=None,
                ))
            except Exception as e:
                logger.error(f"Sub-engine query error: {str(e)}")
                responses.append(SubEngineResponse(
                    engine_id="unknown",
                    success=False,
                    error=str(e),
                    latency_ms=None,
                ))
        return responses

    def merge_responses(self, responses: List[SubEngineResponse]) -> Dict[str, Any]:
        merged = {
            "results": [],
            "errors": [],
            "summary": {
                "successful_engines": 0,
                "failed_engines": 0,
            }
        }
        for resp in responses:
            if resp.success:
                merged["results"].append(resp.data)
                merged["summary"]["successful_engines"] += 1
            else:
                merged["errors"].append({
                    "engine_id": resp.engine_id,
                    "error": resp.error
                })
                merged["summary"]["failed_engines"] += 1
        logger.debug(f"Merged response summary: {merged['summary']}")
        return merged

    def apply_guardrails(self, merged_response: Dict[str, Any]) -> Dict[str, Any]:
        # Example guardrail: remove any result containing forbidden keywords
        forbidden_keywords = ["error", "fail", "unauthorized"]
        filtered_results = []
        for result in merged_response.get("results", []):
            result_str = json.dumps(result).lower()
            if any(kw in result_str for kw in forbidden_keywords):
                logger.warning("Guardrail filtered a result due to forbidden content")
                continue
            filtered_results.append(result)
        merged_response["results"] = filtered_results
        return merged_response

    def hash_response(self, response: Dict[str, Any]) -> str:
        response_bytes = json.dumps(response, sort_keys=True).encode('utf-8')
        hash_digest = hashlib.sha256(response_bytes).hexdigest()
        logger.debug(f"Response hash: {hash_digest}")
        return hash_digest

    def log_query(self, query: str, response_hash: str, latency_ms: int, cache_hit: bool):
        logger.info(f"Query logged: hash={response_hash}, latency_ms={latency_ms}, cache_hit={cache_hit}")

    async def handle_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        start = time.time()
        normalized_query = self.normalize_query(query)
        classified_engines = self.classify_domain(normalized_query)
        routed_engines = self.route_query(classified_engines)

        # Check doctrine cache fallback
        doctrine_hit = False
        doctrine_response = None
        for doctrine_id, doctrine in self.doctrine_cache.get_all().items():
            if doctrine_id.lower() in normalized_query:
                doctrine_hit = True
                doctrine_response = {
                    "doctrine_id": doctrine_id,
                    "description": doctrine["description"],
                    "cached": True,
                }
                break

        if doctrine_hit:
            latency_ms = int((time.time() - start) * 1000)
            self.telemetry.record_query(latency_ms, cache_hit=True)
            self.log_query(query, self.hash_response(doctrine_response), latency_ms, True)
            return {"source": "doctrine_cache", "data": doctrine_response}

        # Dispatch to sub-engines
        responses = await self.dispatch_query(normalized_query, routed_engines, context)
        merged = self.merge_responses(responses)
        guarded = self.apply_guardrails(merged)
        latency_ms = int((time.time() - start) * 1000)
        self.telemetry.record_query(latency_ms, cache_hit=False)
        response_hash = self.hash_response(guarded)
        self.log_query(query, response_hash, latency_ms, False)
        return {"source": "sub_engines", "data": guarded}

    async def get_health(self) -> Dict[str, Any]:
        self_status = {
            "engine_id": ENGINE_ID,
            "status": "healthy",
            "last_checked": datetime.utcnow().isoformat(),
        }
        sub_engine_healths = await asyncio.gather(*[
            se.health_check() for se in self.sub_engines.values()
        ])
        return {
            "self": self_status,
            "sub_engines": [h.dict() for h in sub_engine_healths]
        }

    async def get_metrics(self) -> MetricsResponse:
        telemetry_metrics = self.telemetry.get_metrics()
        sub_engine_stats = {
            eid: client.get_stats()
            for eid, client in self.sub_engines.items()
        }
        return MetricsResponse(
            latency_stats={
                "average_latency_ms": telemetry_metrics["average_latency_ms"],
                "p95_latency_ms": telemetry_metrics["p95_latency_ms"],
            },
            cache_hit_rate=telemetry_metrics["cache_hit_rate"],
            queries_per_hour=telemetry_metrics["queries_per_hour"],
            sub_engine_stats=sub_engine_stats,
        )

    async def get_coverage(self) -> CoverageReport:
        doctrines = self.doctrine_cache.get_all()
        coverage = {}
        for doctrine_id, doctrine in doctrines.items():
            coverage[doctrine_id] = doctrine.get("coverage", 0.0)
        epistemic_gaps = [d_id for d_id, cov in coverage.items() if cov < 0.8]
        return CoverageReport(
            doctrine_coverage=coverage,
            epistemic_gaps=epistemic_gaps,
        )

    async def get_drift(self) -> DriftReport:
        # Simulate drift detection
        drift_detected = random.random() < 0.1
        details = None
        if drift_detected:
            details = {
                "message": "Detected drift in Mud Pump Systems doctrine",
                "affected_doctrines": ["doctrine_001"],
                "timestamp": datetime.utcnow().isoformat(),
            }
        return DriftReport(
            drift_detected=drift_detected,
            details=details,
        )

    async def get_doctrines(self) -> List[DoctrineInfo]:
        doctrines = self.doctrine_cache.get_all()
        doctrine_list = []
        for doctrine_id, doctrine in doctrines.items():
            doctrine_list.append(
                DoctrineInfo(
                    doctrine_id=doctrine_id,
                    description=doctrine.get("description", ""),
                    last_updated=doctrine.get("last_updated", datetime.utcnow())
                )
            )
        return doctrine_list

    async def get_routing(self) -> RoutingInfo:
        return RoutingInfo(
            routing_rules=self.routing_rules,
            engine_registry=SUB_ENGINES,
        )

    async def get_sub_engines_health(self) -> SubEngineHealthDashboard:
        healths = await asyncio.gather(*[
            se.health_check() for se in self.sub_engines.values()
        ])
        return SubEngineHealthDashboard(sub_engines=healths)

    async def dry_run_route(self, query: str) -> Dict[str, Any]:
        normalized_query = self.normalize_query(query)
        classified_engines = self.classify_domain(normalized_query)
        routed_engines = self.route_query(classified_engines)
        return {
            "query": query,
            "normalized_query": normalized_query,
            "classified_engines": classified_engines,
            "routed_engines": routed_engines,
        }

    async def analyze(self, query: str, depth: int = 3, engines: Optional[List[str]] = None) -> Dict[str, Any]:
        normalized_query = self.normalize_query(query)
        if engines is None:
            classified_engines = self.classify_domain(normalized_query)
            routed_engines = self.route_query(classified_engines)
        else:
            routed_engines = engines

        analysis_results = {}
        for engine_id in routed_engines:
            client = self.sub_engines.get(engine_id)
            if client:
                # Simulate multi-depth analysis with repeated queries
                engine_results = []
                for d in range(depth):
                    resp = await client.query(f"{normalized_query} (analysis depth {d+1})")
                    engine_results.append(resp.dict())
                analysis_results[engine_id] = engine_results
        return {
            "query": query,
            "normalized_query": normalized_query,
            "analysis_depth": depth,
            "results": analysis_results,
        }

# -------------------------
# FastAPI Application Setup
# -------------------------

app = FastAPI(title="Oilfield Equipment Intelligence Engine — Domain Orchestrator", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()
start_time = time.time()

@app.on_event("startup")
async def startup_event():
    await orchestrator.lifespan_startup()

@app.on_event("shutdown")
async def shutdown_event():
    await orchestrator.lifespan_shutdown()

# -------------------------
# API Endpoints
# -------------------------

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    try:
        response = await orchestrator.handle_query(request.query, request.context)
        return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"Error in /query endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_endpoint():
    try:
        health = await orchestrator.get_health()
        return JSONResponse(content=health)
    except Exception as e:
        logger.error(f"Error in /health endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/metrics")
async def metrics_endpoint():
    try:
        metrics = await orchestrator.get_metrics()
        return JSONResponse(content=metrics.dict())
    except Exception as e:
        logger.error(f"Error in /metrics endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/coverage")
async def coverage_endpoint():
    try:
        coverage = await orchestrator.get_coverage()
        return JSONResponse(content=coverage.dict())
    except Exception as e:
        logger.error(f"Error in /coverage endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/drift")
async def drift_endpoint():
    try:
        drift = await orchestrator.get_drift()
        return JSONResponse(content=drift.dict())
    except Exception as e:
        logger.error(f"Error in /drift endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/doctrines")
async def doctrines_endpoint():
    try:
        doctrines = await orchestrator.get_doctrines()
        return JSONResponse(content=[d.dict() for d in doctrines])
    except Exception as e:
        logger.error(f"Error in /doctrines endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/routing")
async def routing_endpoint():
    try:
        routing = await orchestrator.get_routing()
        return JSONResponse(content=routing.dict())
    except Exception as e:
        logger.error(f"Error in /routing endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/sub-engines")
async def sub_engines_endpoint():
    try:
        health_dashboard = await orchestrator.get_sub_engines_health()
        return JSONResponse(content=health_dashboard.dict())
    except Exception as e:
        logger.error(f"Error in /sub-engines endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/route")
async def route_dry_run_endpoint(request: RouteDryRunRequest):
    try:
        route_info = await orchestrator.dry_run_route(request.query)
        return JSONResponse(content=route_info)
    except Exception as e:
        logger.error(f"Error in /route endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/analyze")
async def analyze_endpoint(request: AnalyzeRequest):
    try:
        analysis = await orchestrator.analyze(request.query, request.depth, request.engines)
        return JSONResponse(content=analysis)
    except Exception as e:
        logger.error(f"Error in /analyze endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# -------------------------
# Run the server
# -------------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=ENGINE_PORT, log_level="info")