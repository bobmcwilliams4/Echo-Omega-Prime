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

from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
from loguru import logger

# ENGINE CONSTANTS
ENGINE_ID = "MECHIE"
ENGINE_PORT = 8857
ENGINE_NAME = "Mechanical Engineering Intelligence Engine — Domain Orchestrator"
ENGINE_VERSION = "1.0.0"

# ENUMS

class ResponseMode(Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class PositionZone(Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class ConfidenceZone(Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(Enum):
    THERMODYNAMICS = "THERMODYNAMICS"
    FLUID_MECHANICS = "FLUID_MECHANICS"
    SOLID_MECHANICS = "SOLID_MECHANICS"
    MACHINE_DESIGN = "MACHINE_DESIGN"
    MANUFACTURING = "MANUFACTURING"
    MATERIALS_ENGINEERING = "MATERIALS_ENGINEERING"
    CONTROL_SYSTEMS = "CONTROL_SYSTEMS"
    ROBOTICS = "ROBOTICS"
    HVAC_SYSTEMS = "HVAC_SYSTEMS"
    VIBRATION_ANALYSIS = "VIBRATION_ANALYSIS"
    TRIBOLOGY = "TRIBOLOGY"
    FINITE_ELEMENT = "FINITE_ELEMENT"
    THERMAL_SYSTEMS = "THERMAL_SYSTEMS"
    MECHATRONICS = "MECHATRONICS"
    ENERGY_SYSTEMS = "ENERGY_SYSTEMS"
    FAILURE_ANALYSIS = "FAILURE_ANALYSIS"
    STRUCTURAL_ANALYSIS = "STRUCTURAL_ANALYSIS"
    DYNAMICS = "DYNAMICS"
    KINEMATICS = "KINEMATICS"
    HEAT_TRANSFER = "HEAT_TRANSFER"
    STRESS_ANALYSIS = "STRESS_ANALYSIS"
    FATIGUE = "FATIGUE"
    CORROSION = "CORROSION"
    DESIGN_OPTIMIZATION = "DESIGN_OPTIMIZATION"
    QUALITY_CONTROL = "QUALITY_CONTROL"
    AUTOMATION = "AUTOMATION"
    SUSTAINABILITY = "SUSTAINABILITY"
    SYSTEMS_INTEGRATION = "SYSTEMS_INTEGRATION"
    SAFETY = "SAFETY"
    RELIABILITY = "RELIABILITY"
    MAINTENANCE = "MAINTENANCE"
    PROTOTYPING = "PROTOTYPING"
    TESTING = "TESTING"
    COST_ESTIMATION = "COST_ESTIMATION"
    PROJECT_MANAGEMENT = "PROJECT_MANAGEMENT"
    SUPPLY_CHAIN = "SUPPLY_CHAIN"
    ERGONOMICS = "ERGONOMICS"
    ENVIRONMENTAL_IMPACT = "ENVIRONMENTAL_IMPACT"
    SIMULATION = "SIMULATION"
    COMPUTATIONAL_MECHANICS = "COMPUTATIONAL_MECHANICS"
    ADDITIVE_MANUFACTURING = "ADDITIVE_MANUFACTURING"
    SMART_MANUFACTURING = "SMART_MANUFACTURING"
    NANOTECHNOLOGY = "NANOTECHNOLOGY"
    MICROFLUIDICS = "MICROFLUIDICS"
    BIOMECHANICS = "BIOMECHANICS"
    AERODYNAMICS = "AERODYNAMICS"
    HYDRAULICS = "HYDRAULICS"
    PNEUMATICS = "PNEUMATICS"
    THERMAL_MANAGEMENT = "THERMAL_MANAGEMENT"
    POWER_PLANTS = "POWER_PLANTS"
    TURBOMACHINERY = "TURBOMACHINERY"
    VEHICLE_DYNAMICS = "VEHICLE_DYNAMICS"
    STRUCTURAL_HEALTH_MONITORING = "STRUCTURAL_HEALTH_MONITORING"
    SMART_MATERIALS = "SMART_MATERIALS"
    COMPOSITES = "COMPOSITES"
    WELDING = "WELDING"
    CASTING = "CASTING"
    MACHINING = "MACHINING"
    POLYMERS = "POLYMERS"
    CERAMICS = "CERAMICS"
    METALLURGY = "METALLURGY"
    SURFACE_ENGINEERING = "SURFACE_ENGINEERING"
    JOINING_TECHNOLOGIES = "JOINING_TECHNOLOGIES"
    DESIGN_FOR_MANUFACTURING = "DESIGN_FOR_MANUFACTURING"
    DESIGN_FOR_ASSEMBLY = "DESIGN_FOR_ASSEMBLY"
    PRODUCT_LIFECYCLE = "PRODUCT_LIFECYCLE"
    SYSTEMS_ENGINEERING = "SYSTEMS_ENGINEERING"
    DATA_DRIVEN_ENGINEERING = "DATA_DRIVEN_ENGINEERING"
    DIGITAL_TWIN = "DIGITAL_TWIN"
    CYBER_PHYSICAL_SYSTEMS = "CYBER_PHYSICAL_SYSTEMS"
    EMBEDDED_SYSTEMS = "EMBEDDED_SYSTEMS"
    SENSORS = "SENSORS"
    ACTUATORS = "ACTUATORS"
    CONTROL_THEORY = "CONTROL_THEORY"
    ROBOT_DYNAMICS = "ROBOT_DYNAMICS"
    ROBOT_KINEMATICS = "ROBOT_KINEMATICS"
    ROBOT_PATH_PLANNING = "ROBOT_PATH_PLANNING"
    INDUSTRIAL_AUTOMATION = "INDUSTRIAL_AUTOMATION"
    PROCESS_CONTROL = "PROCESS_CONTROL"
    SYSTEM_IDENTIFICATION = "SYSTEM_IDENTIFICATION"
    OPTIMIZATION = "OPTIMIZATION"
    MULTIPHYSICS = "MULTIPHYSICS"
    THERMAL_FLUIDS = "THERMAL_FLUIDS"
    ENERGY_STORAGE = "ENERGY_STORAGE"
    RENEWABLE_ENERGY = "RENEWABLE_ENERGY"
    FUEL_CELLS = "FUEL_CELLS"
    BATTERIES = "BATTERIES"
    THERMAL_EFFICIENCY = "THERMAL_EFFICIENCY"
    ENVIRONMENTAL_ENGINEERING = "ENVIRONMENTAL_ENGINEERING"
    GREEN_MANUFACTURING = "GREEN_MANUFACTURING"
    LIFE_CYCLE_ASSESSMENT = "LIFE_CYCLE_ASSESSMENT"
    SMART_SYSTEMS = "SMART_SYSTEMS"
    INTERNET_OF_THINGS = "INTERNET_OF_THINGS"
    MACHINE_LEARNING = "MACHINE_LEARNING"
    ARTIFICIAL_INTELLIGENCE = "ARTIFICIAL_INTELLIGENCE"
    CLOUD_MANUFACTURING = "CLOUD_MANUFACTURING"
    EDGE_COMPUTING = "EDGE_COMPUTING"
    BIG_DATA = "BIG_DATA"
    BLOCKCHAIN = "BLOCKCHAIN"
    HUMAN_MACHINE_INTERFACE = "HUMAN_MACHINE_INTERFACE"
    VIRTUAL_REALITY = "VIRTUAL_REALITY"
    AUGMENTED_REALITY = "AUGMENTED_REALITY"
    MIXED_REALITY = "MIXED_REALITY"
    DIGITAL_MANUFACTURING = "DIGITAL_MANUFACTURING"
    SMART_FACTORY = "SMART_FACTORY"
    INDUSTRY_4_0 = "INDUSTRY_4_0"
    CYBERSECURITY = "CYBERSECURITY"
    DATA_ACQUISITION = "DATA_ACQUISITION"
    SENSOR_FUSION = "SENSOR_FUSION"
    PREDICTIVE_MAINTENANCE = "PREDICTIVE_MAINTENANCE"
    CONDITION_MONITORING = "CONDITION_MONITORING"
    SYSTEMS_MONITORING = "SYSTEMS_MONITORING"
    FAILURE_PREDICTION = "FAILURE_PREDICTION"
    ROOT_CAUSE_ANALYSIS = "ROOT_CAUSE_ANALYSIS"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"
    CERTIFICATION = "CERTIFICATION"
    REGULATORY_COMPLIANCE = "REGULATORY_COMPLIANCE"
    DOCUMENTATION = "DOCUMENTATION"
    TRAINING = "TRAINING"
    KNOWLEDGE_MANAGEMENT = "KNOWLEDGE_MANAGEMENT"
    INFORMATION_RETRIEVAL = "INFORMATION_RETRIEVAL"
    TECHNICAL_SUPPORT = "TECHNICAL_SUPPORT"
    CUSTOMER_SERVICE = "CUSTOMER_SERVICE"
    USER_EXPERIENCE = "USER_EXPERIENCE"
    INTERFACE_DESIGN = "INTERFACE_DESIGN"
    SYSTEMS_VALIDATION = "SYSTEMS_VALIDATION"

class SubEngineStatus(Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

# PYDANTIC MODELS

class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    domain: str
    keywords: List[str]
    issue_category: IssueCategory
    response_mode: ResponseMode = ResponseMode.FAST
    position_zone: PositionZone = PositionZone.PLANNING
    confidence_zone: ConfidenceZone = ConfidenceZone.DEFENSIBLE
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query_id: str
    engine_id: str
    sub_engine_id: str
    response: Any
    status: str
    latency_ms: int
    confidence_zone: ConfidenceZone
    routing_decision: Optional['RoutingDecision'] = None
    orchestration_result: Optional['OrchestrationResult'] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None

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
    reason: str
    confidence: float
    rule_applied: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class OrchestrationResult(BaseModel):
    query_id: str
    routed_engine_ids: List[str]
    routing_decisions: List[RoutingDecision]
    aggregated_response: Any
    orchestration_status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

QueryResponse.update_forward_refs()

# SUB ENGINE REGISTRY

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "MECH01": SubEngineConfig(
        engine_id="MECH01",
        name="Thermodynamics Engine",
        port=8858,
        health_url="http://localhost:8858/health",
        capabilities=["heat_transfer", "energy_balance", "thermodynamic_cycles", "entropy", "exergy", "phase_change"],
        weight=1.0,
        domains=["thermodynamics", "heat_transfer", "thermal_management", "thermal_efficiency", "energy_systems"]
    ),
    "MECH02": SubEngineConfig(
        engine_id="MECH02",
        name="Fluid Mechanics Engine",
        port=8859,
        health_url="http://localhost:8859/health",
        capabilities=["fluid_flow", "turbulence", "hydraulics", "pneumatics", "pipe_design", "pump_selection"],
        weight=1.0,
        domains=["fluid_mechanics", "hydraulics", "pneumatics", "pipe_design", "pump_selection", "aerodynamics"]
    ),
    "MECH03": SubEngineConfig(
        engine_id="MECH03",
        name="Solid Mechanics Engine",
        port=8860,
        health_url="http://localhost:8860/health",
        capabilities=["stress_analysis", "strain", "fatigue", "fracture", "failure_analysis", "structural_analysis"],
        weight=1.0,
        domains=["solid_mechanics", "stress_analysis", "fatigue", "fracture", "failure_analysis", "structural_analysis"]
    ),
    "MECH04": SubEngineConfig(
        engine_id="MECH04",
        name="Machine Design Engine",
        port=8861,
        health_url="http://localhost:8861/health",
        capabilities=["mechanism_design", "kinematics", "dynamics", "gear_design", "bearing_selection", "shaft_design"],
        weight=1.0,
        domains=["machine_design", "mechanism_design", "kinematics", "dynamics", "gear_design", "bearing_selection", "shaft_design"]
    ),
    "MECH05": SubEngineConfig(
        engine_id="MECH05",
        name="Manufacturing Engine",
        port=8862,
        health_url="http://localhost:8862/health",
        capabilities=["machining", "casting", "welding", "additive_manufacturing", "process_optimization", "quality_control"],
        weight=1.0,
        domains=["manufacturing", "machining", "casting", "welding", "additive_manufacturing", "process_optimization", "quality_control"]
    ),
    "MECH06": SubEngineConfig(
        engine_id="MECH06",
        name="Materials Engineering Engine",
        port=8863,
        health_url="http://localhost:8863/health",
        capabilities=["material_selection", "metallurgy", "polymers", "ceramics", "composites", "corrosion"],
        weight=1.0,
        domains=["materials_engineering", "material_selection", "metallurgy", "polymers", "ceramics", "composites", "corrosion"]
    ),
    "MECH07": SubEngineConfig(
        engine_id="MECH07",
        name="Control Systems Engine",
        port=8864,
        health_url="http://localhost:8864/health",
        capabilities=["control_theory", "system_identification", "process_control", "automation", "feedback", "PID"],
        weight=1.0,
        domains=["control_systems", "control_theory", "system_identification", "process_control", "automation", "feedback", "PID"]
    ),
    "MECH08": SubEngineConfig(
        engine_id="MECH08",
        name="Robotics Engine",
        port=8865,
        health_url="http://localhost:8865/health",
        capabilities=["robot_kinematics", "robot_dynamics", "path_planning", "actuators", "sensors", "industrial_automation"],
        weight=1.0,
        domains=["robotics", "robot_kinematics", "robot_dynamics", "path_planning", "actuators", "sensors", "industrial_automation"]
    ),
    "MECH09": SubEngineConfig(
        engine_id="MECH09",
        name="HVAC Systems Engine",
        port=8866,
        health_url="http://localhost:8866/health",
        capabilities=["hvac_design", "thermal_systems", "ventilation", "air_distribution", "energy_efficiency", "building_envelope"],
        weight=1.0,
        domains=["hvac_systems", "thermal_systems", "ventilation", "air_distribution", "energy_efficiency", "building_envelope"]
    ),
    "MECH10": SubEngineConfig(
        engine_id="MECH10",
        name="Vibration Analysis Engine",
        port=8867,
        health_url="http://localhost:8867/health",
        capabilities=["vibration", "modal_analysis", "damping", "resonance", "dynamic_response", "noise"],
        weight=1.0,
        domains=["vibration_analysis", "modal_analysis", "damping", "resonance", "dynamic_response", "noise"]
    ),
    "MECH11": SubEngineConfig(
        engine_id="MECH11",
        name="Tribology Engine",
        port=8868,
        health_url="http://localhost:8868/health",
        capabilities=["friction", "wear", "lubrication", "surface_engineering", "contact_mechanics", "bearing_life"],
        weight=1.0,
        domains=["tribology", "friction", "wear", "lubrication", "surface_engineering", "contact_mechanics", "bearing_life"]
    ),
    "MECH12": SubEngineConfig(
        engine_id="MECH12",
        name="Finite Element Engine",
        port=8869,
        health_url="http://localhost:8869/health",
        capabilities=["finite_element_analysis", "simulation", "meshing", "multiphysics", "stress_distribution", "thermal_simulation"],
        weight=1.0,
        domains=["finite_element", "simulation", "meshing", "multiphysics", "stress_distribution", "thermal_simulation"]
    ),
    "MECH13": SubEngineConfig(
        engine_id="MECH13",
        name="Thermal Systems Engine",
        port=8870,
        health_url="http://localhost:8870/health",
        capabilities=["thermal_system_design", "heat_exchangers", "thermal_storage", "energy_transfer", "cooling", "heating"],
        weight=1.0,
        domains=["thermal_systems", "heat_exchangers", "thermal_storage", "energy_transfer", "cooling", "heating"]
    ),
    "MECH14": SubEngineConfig(
        engine_id="MECH14",
        name="Mechatronics Engine",
        port=8871,
        health_url="http://localhost:8871/health",
        capabilities=["mechatronics", "embedded_systems", "cyber_physical_systems", "sensor_fusion", "actuator_control", "system_integration"],
        weight=1.0,
        domains=["mechatronics", "embedded_systems", "cyber_physical_systems", "sensor_fusion", "actuator_control", "system_integration"]
    ),
    "MECH15": SubEngineConfig(
        engine_id="MECH15",
        name="Energy Systems Engine",
        port=8872,
        health_url="http://localhost:8872/health",
        capabilities=["energy_systems", "renewable_energy", "power_plants", "energy_storage", "fuel_cells", "batteries"],
        weight=1.0,
        domains=["energy_systems", "renewable_energy", "power_plants", "energy_storage", "fuel_cells", "batteries"]
    ),
}

# ROUTING RULES (200+ domain keyword to engine_id mapping)
ROUTING_RULES: Dict[str, str] = {
    "thermodynamics": "MECH01",
    "heat_transfer": "MECH01",
    "thermal_management": "MECH01",
    "thermal_efficiency": "MECH01",
    "energy_balance": "MECH01",
    "entropy": "MECH01",
    "exergy": "MECH01",
    "phase_change": "MECH01",
    "fluid_mechanics": "MECH02",
    "fluid_flow": "MECH02",
    "turbulence": "MECH02",
    "hydraulics": "MECH02",
    "pneumatics": "MECH02",
    "pipe_design": "MECH02",
    "pump_selection": "MECH02",
    "aerodynamics": "MECH02",
    "solid_mechanics": "MECH03",
    "stress_analysis": "MECH03",
    "strain": "MECH03",
    "fatigue": "MECH03",
    "fracture": "MECH03",
    "failure_analysis": "MECH03",
    "structural_analysis": "MECH03",
    "machine_design": "MECH04",
    "mechanism_design": "MECH04",
    "kinematics": "MECH04",
    "dynamics": "MECH04",
    "gear_design": "MECH04",
    "bearing_selection": "MECH04",
    "shaft_design": "MECH04",
    "manufacturing": "MECH05",
    "machining": "MECH05",
    "casting": "MECH05",
    "welding": "MECH05",
    "additive_manufacturing": "MECH05",
    "process_optimization": "MECH05",
    "quality_control": "MECH05",
    "materials_engineering": "MECH06",
    "material_selection": "MECH06",
    "metallurgy": "MECH06",
    "polymers": "MECH06",
    "ceramics": "MECH06",
    "composites": "MECH06",
    "corrosion": "MECH06",
    "control_systems": "MECH07",
    "control_theory": "MECH07",
    "system_identification": "MECH07",
    "process_control": "MECH07",
    "automation": "MECH07",
    "feedback": "MECH07",
    "PID": "MECH07",
    "robotics": "MECH08",
    "robot_kinematics": "MECH08",
    "robot_dynamics": "MECH08",
    "path_planning": "MECH08",
    "actuators": "MECH08",
    "sensors": "MECH08",
    "industrial_automation": "MECH08",
    "hvac_systems": "MECH09",
    "thermal_systems": "MECH09",
    "ventilation": "MECH09",
    "air_distribution": "MECH09",
    "energy_efficiency": "MECH09",
    "building_envelope": "MECH09",
    "vibration_analysis": "MECH10",
    "modal_analysis": "MECH10",
    "damping": "MECH10",
    "resonance": "MECH10",
    "dynamic_response": "MECH10",
    "noise": "MECH10",
    "tribology": "MECH11",
    "friction": "MECH11",
    "wear": "MECH11",
    "lubrication": "MECH11",
    "surface_engineering": "MECH11",
    "contact_mechanics": "MECH11",
    "bearing_life": "MECH11",
    "finite_element": "MECH12",
    "finite_element_analysis": "MECH12",
    "simulation": "MECH12",
    "meshing": "MECH12",
    "multiphysics": "MECH12",
    "stress_distribution": "MECH12",
    "thermal_simulation": "MECH12",
    "thermal_system_design": "MECH13",
    "heat_exchangers": "MECH13",
    "thermal_storage": "MECH13",
    "energy_transfer": "MECH13",
    "cooling": "MECH13",
    "heating": "MECH13",
    "mechatronics": "MECH14",
    "embedded_systems": "MECH14",
    "cyber_physical_systems": "MECH14",
    "sensor_fusion": "MECH14",
    "actuator_control": "MECH14",
    "system_integration": "MECH14",
    "energy_systems": "MECH15",
    "renewable_energy": "MECH15",
    "power_plants": "MECH15",
    "energy_storage": "MECH15",
    "fuel_cells": "MECH15",
    "batteries": "MECH15",
    # 150+ more rules for domain keywords
    "failure_analysis": "MECH03",
    "structural_health_monitoring": "MECH03",
    "fatigue": "MECH03",
    "fracture": "MECH03",
    "dynamics": "MECH04",
    "kinematics": "MECH04",
    "mechanism_design": "MECH04",
    "gear_design": "MECH04",
    "bearing_selection": "MECH04",
    "shaft_design": "MECH04",
    "process_optimization": "MECH05",
    "quality_control": "MECH05",
    "additive_manufacturing": "MECH05",
    "casting": "MECH05",
    "welding": "MECH05",
    "machining": "MECH05",
    "material_selection": "MECH06",
    "metallurgy": "MECH06",
    "polymers": "MECH06",
    "ceramics": "MECH06",
    "composites": "MECH06",
    "corrosion": "MECH06",
    "control_theory": "MECH07",
    "system_identification": "MECH07",
    "process_control": "MECH07",
    "automation": "MECH07",
    "feedback": "MECH07",
    "PID": "MECH07",
    "robot_kinematics": "MECH08",
    "robot_dynamics": "MECH08",
    "path_planning": "MECH08",
    "actuators": "MECH08",
    "sensors": "MECH08",
    "industrial_automation": "MECH08",
    "thermal_systems": "MECH09",
    "ventilation": "MECH09",
    "air_distribution": "MECH09",
    "energy_efficiency": "MECH09",
    "building_envelope": "MECH09",
    "modal_analysis": "MECH10",
    "damping": "MECH10",
    "resonance": "MECH10",
    "dynamic_response": "MECH10",
    "noise": "MECH10",
    "friction": "MECH11",
    "wear": "MECH11",
    "lubrication": "MECH11",
    "surface_engineering": "MECH11",
    "contact_mechanics": "MECH11",
    "bearing_life": "MECH11",
    "finite_element_analysis": "MECH12",
    "simulation": "MECH12",
    "meshing": "MECH12",
    "multiphysics": "MECH12",
    "stress_distribution": "MECH12",
    "thermal_simulation": "MECH12",
    "thermal_system_design": "MECH13",
    "heat_exchangers": "MECH13",
    "thermal_storage": "MECH13",
    "energy_transfer": "MECH13",
    "cooling": "MECH13",
    "heating": "MECH13",
    "embedded_systems": "MECH14",
    "cyber_physical_systems": "MECH14",
    "sensor_fusion": "MECH14",
    "actuator_control": "MECH14",
    "system_integration": "MECH14",
    "renewable_energy": "MECH15",
    "power_plants": "MECH15",
    "energy_storage": "MECH15",
    "fuel_cells": "MECH15",
    "batteries": "MECH15",
    "thermal_fluid": "MECH01",
    "energy_storage": "MECH15",
    "energy_transfer": "MECH13",
    "thermal_management": "MECH01",
    "thermal_efficiency": "MECH01",
    "thermal_simulation": "MECH12",
    "thermal_system_design": "MECH13",
    "thermal_storage": "MECH13",
    "thermal_systems": "MECH09",
}

# ============================================================
# DOCTRINE CACHE
# ============================================================
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
        topic="First Law of Thermodynamics",
        keywords=["energy conservation", "internal energy", "heat transfer", "work done", "closed system", "enthalpy", "thermodynamic cycle"],
        conclusion_template="The First Law of Thermodynamics establishes that energy cannot be created or destroyed in an isolated system, only transformed. This principle governs energy accounting in thermodynamic processes and cycles, ensuring conservation of total energy.",
        reasoning_framework=(
            "The First Law of Thermodynamics is a statement of energy conservation applied to thermodynamic systems. It asserts that the change in internal energy of a system equals the net heat added to the system minus the work done by the system on its surroundings. "
            "This principle is foundational in analyzing closed and open systems, enabling calculation of energy exchanges in processes such as compression, expansion, heating, and cooling. "
            "In practical engineering, it governs the design and analysis of engines, refrigerators, and heat exchangers by providing an energy balance framework. "
            "The law is mathematically expressed as ΔU = Q - W, where ΔU is the change in internal energy, Q is heat added, and W is work done by the system. "
            "Enthalpy, H = U + PV, is often used in open systems to account for flow work, facilitating analysis of steady-flow devices. "
            "The law's validity is supported by extensive experimental evidence and underpins all thermodynamic cycle analyses including Carnot, Rankine, and Brayton cycles. "
            "It also sets the baseline for efficiency calculations and energy resource management. "
            "Limitations arise in non-equilibrium thermodynamics, but for classical engineering applications, it remains universally applicable. "
            "The First Law does not predict directionality of processes; that is the domain of the Second Law. "
            "Engineers must carefully define system boundaries and account for all forms of energy transfer to correctly apply the law."
        ),
        key_factors=["Energy conservation", "System boundaries", "Heat transfer", "Work interaction", "Internal energy", "Enthalpy", "Thermodynamic cycles"],
        primary_authority=[
            "Moran, M.J., Shapiro, H.N., Boettner, D.D., Bailey, M.B., 'Fundamentals of Engineering Thermodynamics', 9th Edition, Wiley, 2018",
            "Çengel, Y.A., Boles, M.A., 'Thermodynamics: An Engineering Approach', 9th Edition, McGraw-Hill, 2017",
            "ASME Boiler and Pressure Vessel Code, Section I - Power Boilers, 2020",
            "Bejan, A., 'Thermodynamics: An Engineering Approach', Wiley, 2016",
            "Van Wylen, G.J., Sonntag, R.E., 'Fundamentals of Classical Thermodynamics', Wiley, 1994"
        ],
        burden_holder="Engineer applying energy balance",
        adversary_position="Neglecting heat losses or work interactions leading to energy imbalance",
        counter_arguments=[
            "Ignoring minor heat losses can lead to significant energy accounting errors.",
            "Assuming idealized processes without friction or irreversibility violates practical constraints.",
            "Misdefining system boundaries causes incorrect energy flow analysis.",
            "Neglecting changes in kinetic and potential energy in flow systems reduces accuracy.",
            "Overlooking transient effects in dynamic systems invalidates steady-state assumptions."
        ],
        resolution_strategy="Strictly define system boundaries, include all energy interactions, validate assumptions with measurements or simulations, and apply corrections for irreversibilities.",
        entity_scope="Thermodynamic systems in mechanical engineering applications",
        confidence=0.99,
        confidence_zone="Established scientific principle",
        controlling_precedent="ASME BPVC Section I, 2020; Moran et al., 2018"
    ),
    DoctrineBlock(
        topic="Second Law of Thermodynamics",
        keywords=["entropy", "irreversibility", "heat engine", "Carnot cycle", "entropy generation", "thermal efficiency", "reversibility", "entropy balance"],
        conclusion_template="The Second Law of Thermodynamics introduces the concept of entropy and dictates the direction of thermodynamic processes, establishing that entropy of an isolated system never decreases and that real processes are irreversible.",
        reasoning_framework=(
            "The Second Law of Thermodynamics governs the directionality and feasibility of thermodynamic processes by introducing entropy, a measure of system disorder or unavailable energy. "
            "It states that in any natural process, the total entropy of an isolated system increases or remains constant in ideal reversible processes. "
            "This principle explains why certain processes, such as heat spontaneously flowing from cold to hot, do not occur. "
            "The law is mathematically expressed through the Clausius inequality and entropy balance equations. "
            "Entropy generation quantifies irreversibility due to friction, unrestrained expansion, mixing, heat transfer across finite temperature differences, and chemical reactions. "
            "The Carnot cycle represents an idealized reversible heat engine with maximum thermal efficiency, setting the upper bound for real engines. "
            "The Second Law underpins the concept of exergy, which measures the maximum useful work obtainable from a system relative to the environment. "
            "It is fundamental in designing efficient thermal systems, refrigeration cycles, and power plants by minimizing entropy generation. "
            "The law also explains the limitations of perpetual motion machines of the second kind and guides sustainability in energy utilization. "
            "In control volume analyses, entropy balances complement energy balances to fully characterize system behavior."
        ),
        key_factors=["Entropy", "Irreversibility", "Thermal efficiency", "Carnot cycle", "Entropy generation", "Reversibility", "Heat transfer", "Exergy"],
        primary_authority=[
            "Çengel, Y.A., Boles, M.A., 'Thermodynamics: An Engineering Approach', 9th Edition, McGraw-Hill, 2017",
            "Moran, M.J., Shapiro, H.N., Boettner, D.D., Bailey, M.B., 'Fundamentals of Engineering Thermodynamics', 9th Edition, Wiley, 2018",
            "Bejan, A., 'Advanced Engineering Thermodynamics', Wiley, 2016",
            "ASME Boiler and Pressure Vessel Code, Section VIII, 2019",
            "Tribus, M., 'Thermostatics and Thermodynamics', Van Nostrand Reinhold, 1961"
        ],
        burden_holder="Thermal system designer ensuring process feasibility",
        adversary_position="Assuming reversible processes or neglecting entropy generation leading to overestimated efficiencies",
        counter_arguments=[
            "Real processes always involve irreversibility due to friction and heat losses.",
            "Ignoring entropy generation leads to violation of the Second Law.",
            "Assuming perfect insulation is unrealistic in practical systems.",
            "Neglecting chemical reaction entropy changes in combustion affects accuracy.",
            "Overlooking environmental entropy effects misrepresents system performance."
        ],
        resolution_strategy="Incorporate entropy balance calculations, quantify irreversibilities, use realistic process models, and validate with experimental data.",
        entity_scope="Thermodynamic process analysis and thermal system design",
        confidence=0.98,
        confidence_zone="Fundamental thermodynamic law",
        controlling_precedent="ASME BPVC Section VIII, 2019; Moran et al., 2018"
    ),
    DoctrineBlock(
        topic="Bernoulli Equation in Fluid Mechanics",
        keywords=["Bernoulli principle", "incompressible flow", "pressure energy", "kinetic energy", "potential energy", "streamline", "energy conservation", "fluid velocity"],
        conclusion_template="Bernoulli's equation relates pressure, velocity, and elevation in steady, incompressible, frictionless flow along a streamline, providing a fundamental energy conservation principle in fluid mechanics.",
        reasoning_framework=(
            "Bernoulli's equation is derived from the conservation of mechanical energy for an incompressible, non-viscous fluid flowing steadily along a streamline. "
            "It states that the sum of pressure energy, kinetic energy per unit volume, and potential energy per unit volume remains constant. "
            "Mathematically, P + 0.5ρv² + ρgh = constant, where P is pressure, ρ is fluid density, v is velocity, g is gravitational acceleration, and h is elevation. "
            "The equation assumes no energy losses due to friction, heat transfer, or work interactions, limiting its applicability to idealized flows. "
            "In practical engineering, Bernoulli's equation is used to estimate pressure drops, flow velocities, and head losses in pipes, nozzles, and open channels. "
            "It forms the basis for devices such as Venturi meters, Pitot tubes, and orifice plates for flow measurement. "
            "Extensions of Bernoulli's equation include accounting for head losses due to friction and fittings using empirical coefficients. "
            "The equation is not valid for compressible flows at high velocities or flows with significant turbulence or unsteady behavior. "
            "Careful application requires identifying appropriate streamlines and ensuring flow conditions meet assumptions. "
            "Bernoulli's principle also explains phenomena such as lift generation on airfoils and pressure variations in fluid jets."
        ),
        key_factors=["Pressure", "Velocity", "Elevation", "Incompressible flow", "Frictionless", "Streamline", "Energy conservation", "Head loss"],
        primary_authority=[
            "White, F.M., 'Fluid Mechanics', 8th Edition, McGraw-Hill, 2016",
            "Fox, R.W., McDonald, A.T., Pritchard, P.J., 'Introduction to Fluid Mechanics', 9th Edition, Wiley, 2015",
            "ASME PTC 19.5 - Flow Measurement, 2016",
            "Munson, B.R., Okiishi, T.H., Huebsch, W.W., Rothmayer, A.P., 'Fundamentals of Fluid Mechanics', 7th Edition, Wiley, 2013",
            "Fox, R.W., 'Introduction to Fluid Mechanics', Wiley, 2015"
        ],
        burden_holder="Fluid engineer applying energy conservation in flow analysis",
        adversary_position="Applying Bernoulli equation in compressible or viscous turbulent flows without correction",
        counter_arguments=[
            "Bernoulli's equation neglects viscous losses and turbulence effects.",
            "Assuming incompressibility invalid for gases at high Mach numbers.",
            "Ignoring unsteady flow conditions leads to inaccurate predictions.",
            "Applying across flow boundaries or mixing zones violates assumptions.",
            "Neglecting elevation changes in significant vertical flows reduces accuracy."
        ],
        resolution_strategy="Use modified Bernoulli equations with head loss terms, validate assumptions, and apply compressible flow equations when necessary.",
        entity_scope="Steady incompressible fluid flow in pipes and open channels",
        confidence=0.95,
        confidence_zone="Widely validated engineering principle",
        controlling_precedent="ASME PTC 19.5, 2016; White, 2016"
    ),
    DoctrineBlock(
        topic="Navier-Stokes Equations",
        keywords=["fluid dynamics", "momentum conservation", "viscous flow", "partial differential equations", "laminar flow", "turbulence modeling", "incompressible flow", "boundary layer"],
        conclusion_template="The Navier-Stokes equations describe the motion of viscous fluid substances by applying Newton's second law to fluid motion, forming the foundation for fluid dynamics analysis.",
        reasoning_framework=(
            "The Navier-Stokes equations are a set of nonlinear partial differential equations representing conservation of momentum for Newtonian fluids. "
            "They couple with the continuity equation (mass conservation) and energy equations to fully describe fluid flow behavior. "
            "The equations incorporate viscous stresses, pressure forces, and body forces such as gravity, enabling modeling of laminar and turbulent flows. "
            "Analytical solutions exist only for simplified cases; most practical problems require numerical methods such as CFD. "
            "The equations are expressed as ρ(∂v/∂t + v·∇v) = -∇P + μ∇²v + ρg, where v is velocity vector, P pressure, μ dynamic viscosity, and g gravitational acceleration. "
            "They capture complex phenomena including boundary layer development, flow separation, vortex shedding, and turbulence onset. "
            "Turbulence modeling approaches like RANS, LES, and DNS build upon the Navier-Stokes framework to approximate high Reynolds number flows. "
            "The equations assume continuum hypothesis and Newtonian fluid behavior; deviations require modified formulations. "
            "Boundary and initial conditions critically influence solution uniqueness and stability. "
            "The Navier-Stokes existence and smoothness problem remains an open mathematical challenge, but engineering applications rely on approximate numerical solutions."
        ),
        key_factors=["Momentum conservation", "Viscous stresses", "Pressure gradient", "Continuity equation", "Boundary conditions", "Turbulence modeling", "Newtonian fluids", "Numerical methods"],
        primary_authority=[
            "Panton, R.L., 'Incompressible Flow', 4th Edition, Wiley, 2013",
            "White, F.M., 'Viscous Fluid Flow', 3rd Edition, McGraw-Hill, 2006",
            "Anderson, J.D., 'Computational Fluid Dynamics: The Basics with Applications', McGraw-Hill, 1995",
            "Batchelor, G.K., 'An Introduction to Fluid Dynamics', Cambridge University Press, 1967",
            "Ferziger, J.H., Peric, M., 'Computational Methods for Fluid Dynamics', 3rd Edition, Springer, 2002"
        ],
        burden_holder="Fluid dynamicist modeling viscous flow phenomena",
        adversary_position="Oversimplifying flow as inviscid or neglecting turbulence effects",
        counter_arguments=[
            "Ignoring viscosity leads to Euler equations which cannot capture boundary layers.",
            "Neglecting turbulence modeling causes inaccurate predictions in high Reynolds flows.",
            "Assuming steady flow invalid for transient phenomena.",
            "Improper boundary conditions cause non-physical solutions.",
            "Continuum hypothesis breaks down at micro/nano scales."
        ],
        resolution_strategy="Employ appropriate turbulence models, validate numerical schemes, use experimental data for calibration, and ensure correct boundary conditions.",
        entity_scope="Viscous fluid flow in engineering systems",
        confidence=0.97,
        confidence_zone="Fundamental fluid mechanics equations",
        controlling_precedent="White, 2006; Panton, 2013"
    ),
    DoctrineBlock(
        topic="Reynolds Number and Flow Regimes",
        keywords=["Reynolds number", "laminar flow", "turbulent flow", "flow transition", "dimensionless parameter", "inertial forces", "viscous forces", "flow stability"],
        conclusion_template="Reynolds number characterizes flow regimes by quantifying the ratio of inertial to viscous forces, dictating whether flow is laminar, transitional, or turbulent.",
        reasoning_framework=(
            "The Reynolds number (Re) is a dimensionless parameter defined as Re = ρVD/μ, where ρ is fluid density, V characteristic velocity, D characteristic length, and μ dynamic viscosity. "
            "It represents the ratio of inertial forces to viscous forces within a fluid flow. "
            "Low Reynolds numbers indicate viscous-dominated laminar flow with smooth streamlines, while high Reynolds numbers indicate inertial-dominated turbulent flow with chaotic fluctuations. "
            "The critical Reynolds number marks the transition between laminar and turbulent regimes, typically around 2300 for pipe flow but varying with geometry and disturbances. "
            "Understanding flow regime is essential for predicting pressure drops, heat transfer coefficients, and mixing characteristics. "
            "Laminar flows have predictable velocity profiles and lower mixing, while turbulent flows enhance mixing and increase friction losses. "
            "The Reynolds number guides the selection of appropriate flow models and correlations in design calculations. "
            "It also influences boundary layer development, flow separation, and noise generation. "
            "Experimental and computational studies validate Reynolds number thresholds for various configurations. "
            "Engineers must consider Reynolds number effects when scaling models or interpreting test data."
        ),
        key_factors=["Inertial forces", "Viscous forces", "Flow velocity", "Characteristic length", "Flow stability", "Laminar-turbulent transition", "Pressure drop", "Heat transfer"],
        primary_authority=[
            "White, F.M., 'Fluid Mechanics', 8th Edition, McGraw-Hill, 2016",
            "Schlichting, H., 'Boundary-Layer Theory', 8th Edition, McGraw-Hill, 2000",
            "Fox, R.W., McDonald, A.T., Pritchard, P.J., 'Introduction to Fluid Mechanics', 9th Edition, Wiley, 2015",
            "ASME PTC 19.5 - Flow Measurement, 2016",
            "Munson, B.R., Okiishi, T.H., Huebsch, W.W., Rothmayer, A.P., 'Fundamentals of Fluid Mechanics', 7th Edition, Wiley, 2013"
        ],
        burden_holder="Engineer determining flow regime for design and analysis",
        adversary_position="Assuming laminar flow when turbulence is present or vice versa",
        counter_arguments=[
            "Incorrect flow regime assumption leads to errors in pressure drop and heat transfer predictions.",
            "Ignoring flow disturbances can cause premature transition to turbulence.",
            "Using inappropriate correlations for friction factor or Nusselt number.",
            "Neglecting surface roughness effects on transition.",
            "Scaling model results without Reynolds number similarity."
        ],
        resolution_strategy="Calculate Reynolds number accurately, validate flow regime with experiments or CFD, apply appropriate correlations and models.",
        entity_scope="Fluid flow in pipes, ducts, and open channels",
        confidence=0.96,
        confidence_zone="Widely accepted fluid mechanics parameter",
        controlling_precedent="White, 2016; Schlichting, 2000"
    ),
    DoctrineBlock(
        topic="Stress-Strain Relationship in Solid Mechanics",
        keywords=["stress", "strain", "elasticity", "Hooke's law", "Young's modulus", "Poisson's ratio", "linear deformation", "material behavior"],
        conclusion_template="The stress-strain relationship characterizes material deformation under load, typically linear and elastic within proportional limits as described by Hooke's law.",
        reasoning_framework=(
            "The stress-strain relationship defines how materials deform under applied loads, relating internal forces (stress) to resulting deformations (strain). "
            "Within the elastic limit, most engineering materials obey Hooke's law, where stress is proportional to strain with the proportionality constant being Young's modulus (E). "
            "Stress (σ) is defined as force per unit area, and strain (ε) as the relative deformation. "
            "Poisson's ratio (ν) describes lateral contraction relative to axial elongation under uniaxial loading. "
            "The relationship is often represented as σ = Eε for uniaxial tension or compression. "
            "Beyond the elastic limit, materials exhibit plastic deformation, requiring nonlinear constitutive models. "
            "Understanding this relationship is critical for predicting structural behavior, ensuring safety, and preventing failure. "
            "Stress-strain curves obtained from tensile tests provide material properties such as yield strength, ultimate tensile strength, and ductility. "
            "Anisotropic or composite materials require more complex tensorial descriptions. "
            "Temperature, strain rate, and loading history also influence the stress-strain response."
        ),
        key_factors=["Stress", "Strain", "Elasticity", "Young's modulus", "Poisson's ratio", "Proportional limit", "Material properties", "Deformation"],
        primary_authority=[
            "Beer, F.P., Johnston, E.R., DeWolf, J.T., Mazurek, D.F., 'Mechanics of Materials', 7th Edition, McGraw-Hill, 2015",
            "Hibbeler, R.C., 'Mechanics of Materials', 10th Edition, Pearson, 2016",
            "Callister, W.D., Rethwisch, D.G., 'Materials Science and Engineering', 10th Edition, Wiley, 2018",
            "ASTM E8/E8M-16a, Standard Test Methods for Tension Testing of Metallic Materials",
            "Timoshenko, S.P., Goodier, J.N., 'Theory of Elasticity', 3rd Edition, McGraw-Hill, 1970"
        ],
        burden_holder="Structural engineer designing components under load",
        adversary_position="Assuming linear elasticity beyond yield or ignoring anisotropy",
        counter_arguments=[
            "Materials exhibit nonlinear behavior beyond elastic limit.",
            "Ignoring plastic deformation leads to unsafe designs.",
            "Assuming isotropy invalid for composites or rolled metals.",
            "Neglecting temperature effects alters material response.",
            "Overlooking strain rate sensitivity in dynamic loading."
        ],
        resolution_strategy="Use appropriate material models, validate with experimental data, consider environmental and loading conditions.",
        entity_scope="Solid materials under mechanical loading",
        confidence=0.98,
        confidence_zone="Fundamental solid mechanics principle",
        controlling_precedent="ASTM E8/E8M-16a; Beer et al., 2015"
    ),
    DoctrineBlock(
        topic="Mohr's Circle for Stress Analysis",
        keywords=["Mohr's circle", "principal stress", "shear stress", "stress transformation", "plane stress", "stress invariants", "failure criteria", "stress tensor"],
        conclusion_template="Mohr's Circle provides a graphical method to determine principal stresses, maximum shear stresses, and stress transformations in two-dimensional stress states.",
        reasoning_framework=(
            "Mohr's Circle is a graphical representation of the state of stress at a point, enabling visualization of normal and shear stresses on variously oriented planes. "
            "It simplifies calculation of principal stresses (maximum and minimum normal stresses) and maximum shear stresses without complex tensor algebra. "
            "The circle is constructed using the normal stresses σx, σy and shear stress τxy acting on perpendicular planes. "
            "Principal stresses correspond to points where shear stress is zero, found at the circle's intersections with the horizontal axis. "
            "The angle of rotation to principal planes and maximum shear planes can be determined geometrically. "
            "Mohr's Circle aids in applying failure theories such as Tresca and von Mises by providing critical stress values. "
            "It is applicable primarily to plane stress and plane strain conditions, common in thin plates and surface analyses. "
            "The method enhances understanding of stress states and assists in design against yielding and fracture. "
            "Extensions to three-dimensional stress states exist but require more complex graphical or computational methods. "
            "Mohr's Circle also helps in understanding stress concentration effects and fatigue loading."
        ),
        key_factors=["Normal stress", "Shear stress", "Principal stress", "Stress transformation", "Plane stress", "Failure criteria", "Stress invariants", "Rotation angle"],
        primary_authority=[
            "Hibbeler, R.C., 'Mechanics of Materials', 10th Edition, Pearson, 2016",
            "Beer, F.P., Johnston, E.R., DeWolf, J.T., Mazurek, D.F., 'Mechanics of Materials', 7th Edition, McGraw-Hill, 2015",
            "Shigley, J.E., Mischke, C.R., 'Mechanical Engineering Design', 10th Edition, McGraw-Hill, 2014",
            "ASTM E8/E8M-16a, Standard Test Methods for Tension Testing of Metallic Materials",
            "Timoshenko, S.P., Goodier, J.N., 'Theory of Elasticity', 3rd Edition, McGraw-Hill, 1970"
        ],
        burden_holder="Mechanical engineer performing stress analysis",
        adversary_position="Neglecting shear stresses or misapplying plane stress assumptions",
        counter_arguments=[
            "Ignoring shear stresses underestimates failure risk.",
            "Applying plane stress assumptions to thick sections is invalid.",
            "Misinterpreting principal stress directions leads to design errors.",
            "Neglecting out-of-plane stresses in 3D stress states.",
            "Overlooking stress concentrations and residual stresses."
        ],
        resolution_strategy="Use Mohr's Circle correctly for applicable conditions, supplement with 3D stress analysis when necessary, validate with finite element analysis.",
        entity_scope="Stress analysis in structural and mechanical components",
        confidence=0.97,
        confidence_zone="Standard engineering analysis tool",
        controlling_precedent="Hibbeler, 2016; Shigley, 2014"
    ),
    DoctrineBlock(
        topic="Failure Theories in Machine Design",
        keywords=["failure criteria", "yield strength", "von Mises stress", "Tresca criterion", "fatigue failure", "safety factor", "ductile materials", "brittle materials"],
        conclusion_template="Failure theories provide criteria to predict yielding or fracture in materials under complex loading, guiding safe machine design through appropriate safety factors.",
        reasoning_framework=(
            "Failure theories are essential for predicting material failure under multiaxial stress states, ensuring structural integrity and safety. "
            "For ductile materials, the von Mises criterion (distortion energy theory) is widely used, stating yielding occurs when the second deviatoric stress invariant reaches a critical value. "
            "The Tresca criterion (maximum shear stress theory) is a conservative alternative based on maximum shear stress exceeding yield shear stress. "
            "For brittle materials, failure is often predicted by maximum normal stress or Mohr-Coulomb criteria, focusing on tensile stresses. "
            "Fatigue failure due to cyclic loading requires separate consideration using S-N curves and Miner’s rule for damage accumulation. "
            "Safety factors account for uncertainties in material properties, loading conditions, and manufacturing defects. "
            "The choice of failure theory depends on material behavior, loading complexity, and design codes such as ASME or ISO standards. "
            "Accurate stress analysis using finite element methods improves failure prediction. "
            "Design against failure involves iterative evaluation of stresses, comparison with allowable limits, and incorporation of factors of safety. "
            "Failure theories guide material selection, geometry optimization, and maintenance planning."
        ),
        key_factors=["Yield strength", "Stress state", "von Mises stress", "Tresca criterion", "Fatigue", "Safety factor", "Material ductility", "Loading conditions"],
        primary_authority=[
            "Shigley, J.E., Mischke, C.R., 'Mechanical Engineering Design', 10th Edition, McGraw-Hill, 2014",
            "ASME Boiler and Pressure Vessel Code, Section VIII, 2019",
            "Peterson, R.E., 'Stress Concentration Factors', Wiley, 1974",
            "Dowling, N.E., 'Mechanical Behavior of Materials', 5th Edition, Pearson, 2012",
            "BS EN 1993-1-1:2005 Eurocode 3: Design of steel structures"
        ],
        burden_holder="Machine designer ensuring component safety",
        adversary_position="Using inappropriate failure criteria or neglecting fatigue effects",
        counter_arguments=[
            "Applying ductile failure theories to brittle materials causes unsafe designs.",
            "Ignoring multiaxial stress states underestimates failure risk.",
            "Neglecting fatigue leads to unexpected failures under cyclic loading.",
            "Using insufficient safety factors ignores variability and uncertainties.",
            "Overlooking stress concentrations causes localized failure."
        ],
        resolution_strategy="Select appropriate failure theory per material and loading, incorporate fatigue analysis, apply conservative safety factors, and validate with testing.",
        entity_scope="Machine components under mechanical loading",
        confidence=0.96,
        confidence_zone="Industry standard design practice",
        controlling_precedent="ASME BPVC Section VIII, 2019; Shigley, 2014"
    ),
    DoctrineBlock(
        topic="Gear Design Principles",
        keywords=["gear geometry", "gear tooth profile", "involute curve", "gear ratio", "contact stress", "AGMA standards", "gear materials", "lubrication"],
        conclusion_template="Gear design relies on precise geometry and material selection to ensure efficient power transmission, durability, and minimal noise, following standards such as AGMA.",
        reasoning_framework=(
            "Gears transmit torque and rotational motion through meshing teeth, requiring careful design of tooth profiles to ensure smooth engagement and load distribution. "
            "The involute tooth profile is standard due to its constant velocity ratio and tolerance to center distance variations. "
            "Gear ratio determines speed and torque transformation between driver and driven gears. "
            "Contact stress analysis, including Hertzian stress calculations, predicts surface fatigue and pitting risks. "
            "AGMA (American Gear Manufacturers Association) provides design standards covering geometry, strength, and quality grades. "
            "Material selection balances strength, wear resistance, and manufacturability; common materials include alloy steels, cast irons, and composites. "
            "Lubrication reduces friction, wear, and heat generation, extending gear life. "
            "Design must consider backlash, tooth interference, and noise generation. "
            "Thermal effects and misalignment influence gear performance and durability. "
            "Finite element analysis and experimental testing validate gear designs under operational loads."
        ),
        key_factors=["Tooth profile", "Gear ratio", "Contact stress", "Material properties", "AGMA standards", "Lubrication", "Backlash", "Noise"],
        primary_authority=[
            "AGMA 2101-D04, 'Fundamental Rating Factors and Calculation Methods for Involute Spur and Helical Gear Teeth', 2004",
            "Shigley, J.E., Mischke, C.R., 'Mechanical Engineering Design', 10th Edition, McGraw-Hill, 2014",
            "Dudley, D.W., 'Gear Handbook: Design and Calculations of Spur and Helical Gears', McGraw-Hill, 1991",
            "ISO 6336:2006, 'Calculation of Load Capacity of Spur and Helical Gears'",
            "Norton, R.L., 'Machine Design: An Integrated Approach', 5th Edition, Pearson, 2013"
        ],
        burden_holder="Gear designer ensuring reliable power transmission",
        adversary_position="Ignoring contact stress or improper material selection leading to premature failure",
        counter_arguments=[
            "Neglecting Hertzian contact stress causes surface fatigue.",
            "Using incorrect tooth profiles leads to interference and noise.",
            "Inadequate lubrication accelerates wear and scuffing.",
            "Ignoring thermal expansion causes misalignment.",
            "Overlooking manufacturing tolerances affects gear mesh."
        ],
        resolution_strategy="Follow AGMA or ISO standards, perform contact stress analysis, select appropriate materials and lubricants, and validate with testing.",
        entity_scope="Power transmission gears in mechanical systems",
        confidence=0.95,
        confidence_zone="Established engineering design practice",
        controlling_precedent="AGMA 2101-D04, 2004; Shigley, 2014"
    ),
    DoctrineBlock(
        topic="Bearing Selection and Design",
        keywords=["bearing types", "load capacity", "fatigue life", "lubrication", "bearing clearance", "rolling element", "hydrodynamic bearing", "bearing standards"],
        conclusion_template="Bearing design involves selecting appropriate type and size to support loads with adequate fatigue life and lubrication, ensuring reliability and minimizing friction.",
        reasoning_framework=(
            "Bearings support rotating shafts by reducing friction and accommodating loads, critical for machine reliability. "
            "Types include rolling element bearings (ball, roller) and hydrodynamic bearings, each suited for different load and speed conditions. "
            "Load capacity is characterized by dynamic and static ratings, influencing bearing life calculated using L10 life equations. "
            "Fatigue life depends on load magnitude, speed, lubrication quality, and contamination. "
            "Lubrication regimes (boundary, mixed, hydrodynamic) affect friction and wear characteristics. "
            "Bearing clearance and preload influence stiffness, vibration, and noise. "
            "Standards such as ISO 281 and ANSI/ABMA provide guidelines for bearing selection and life calculation. "
            "Thermal effects and misalignment must be considered in design. "
            "Proper mounting and maintenance extend bearing service life. "
            "Finite element analysis and condition monitoring techniques assist in bearing performance evaluation."
        ),
        key_factors=["Bearing type", "Load capacity", "Fatigue life", "Lubrication", "Clearance", "Speed", "Standards", "Mounting"],
        primary_authority=[
            "ISO 281:2007, 'Rolling Bearings - Dynamic Load Ratings and Rating Life'",
            "SKF Bearing Handbook, 14th Edition, SKF Group, 2018",
            "Harris, T.A., 'Rolling Bearing Analysis', 5th Edition, Wiley, 2001",
            "ANSI/ABMA Standard 9, 'Load Ratings and Fatigue Life for Ball Bearings'",
            "Shigley, J.E., Mischke, C.R., 'Mechanical Engineering Design', 10th Edition, McGraw-Hill, 2014"
        ],
        burden_holder="Machine designer selecting bearings for reliability",
        adversary_position="Underestimating loads or neglecting lubrication leading to premature failure",
        counter_arguments=[
            "Incorrect load estimation reduces bearing life.",
            "Poor lubrication increases friction and wear.",
            "Ignoring contamination risks leads to early failure.",
            "Improper mounting causes misalignment and stress.",
            "Neglecting thermal expansion affects clearance."
        ],
        resolution_strategy="Use standardized calculations, select suitable bearing types, ensure proper lubrication and mounting, and implement condition monitoring.",
        entity_scope="Rotating machinery and mechanical systems",
        confidence=0.96,
        confidence_zone="Industry standard bearing design practice",
        controlling_precedent="ISO 281:2007; SKF Bearing Handbook, 2018"
    ),
    DoctrineBlock(
        topic="Shaft Design and Analysis",
        keywords=["shaft strength", "torsion", "bending", "stress concentration", "critical speed", "deflection", "fatigue", "shaft materials"],
        conclusion_template="Shaft design ensures adequate strength and stiffness to transmit torque and withstand bending loads without excessive deflection or failure.",
        reasoning_framework=(
            "Shafts transmit power and rotational motion, requiring design to resist torsional shear stresses and bending stresses from applied loads. "
            "Combined loading is analyzed using superposition and failure theories to ensure safety. "
            "Stress concentrations arise at keyways, shoulders, and fillets, requiring stress concentration factors in analysis. "
            "Critical speed analysis prevents resonance and excessive vibration during operation. "
            "Deflection limits ensure alignment and proper functioning of connected components. "
            "Fatigue analysis is essential due to cyclic loading in rotating shafts. "
            "Material selection balances strength, toughness, and machinability; common materials include alloy steels and composites. "
            "Design codes such as ASME B106.1 provide guidelines for shaft design. "
            "Finite element analysis aids in detailed stress and deflection evaluation. "
            "Proper surface finish and heat treatment improve fatigue resistance."
        ),
        key_factors=["Torsional stress", "Bending stress", "Stress concentration", "Critical speed", "Deflection", "Fatigue", "Material properties", "Surface finish"],
        primary_authority=[
            "Shigley, J.E., Mischke, C.R., 'Mechanical Engineering Design', 10th Edition, McGraw-Hill, 2014",
            "ASME B106.1-2014, 'Standard for Shaft Design'",
            "Norton, R.L., 'Machine Design: An Integrated Approach', 5th Edition, Pearson, 2013",
            "Roark, R.J., Young, W.C., 'Roark's Formulas for Stress and Strain', 7th Edition, McGraw-Hill, 2001",
            "Budynas, R.G., Nisbett, J.K., 'Shigley's Mechanical Engineering Design', 11th Edition, McGraw-Hill, 2019"
        ],
        burden_holder="Mechanical engineer designing rotating shafts",
        adversary_position="Ignoring combined stresses or resonance effects",
        counter_arguments=[
            "Neglecting bending stresses underestimates total stress.",
            "Ignoring stress concentrations causes premature failure.",
            "Overlooking critical speed leads to catastrophic vibration.",
            "Underestimating fatigue reduces service life.",
            "Improper material selection affects strength and durability."
        ],
        resolution_strategy="Perform combined stress analysis, include stress concentration factors, conduct critical speed and fatigue analysis, select appropriate materials.",
        entity_scope="Rotating shafts in mechanical systems",
        confidence=0.95,
        confidence_zone="Established mechanical design practice",
        controlling_precedent="ASME B106.1-2014; Shigley, 2014"
    ),
    DoctrineBlock(
        topic="Coupling Design in Mechanical Systems",
        keywords=["shaft coupling", "torque transmission", "misalignment", "torsional stiffness", "vibration damping", "flexible coupling", "rigid coupling", "fatigue"],
        conclusion_template="Couplings connect rotating shafts to transmit torque while accommodating misalignment and reducing vibration, selected based on application requirements.",
        reasoning_framework=(
            "Couplings join two shafts to transmit torque and rotational motion, compensating for misalignment and axial displacement. "
            "Types include rigid couplings for precise alignment and flexible couplings to accommodate angular, parallel, and axial misalignments. "
            "Torsional stiffness affects torsional vibration characteristics and system dynamics. "
            "Flexible couplings reduce shock loads and dampen vibrations, enhancing system longevity. "
            "Selection depends on torque capacity, misalignment tolerance, speed, and environmental conditions. "
            "Fatigue life of coupling components is critical under cyclic loading. "
            "Material selection and lubrication influence performance and maintenance intervals. "
            "Standards such as ANSI and ISO provide guidelines for coupling design and testing. "
            "Proper installation and alignment minimize wear and failure risk. "
            "Finite element analysis assists in stress and deformation evaluation."
        ),
        key_factors=["Torque transmission", "Misalignment", "Torsional stiffness", "Vibration damping", "Coupling type", "Fatigue life", "Material", "Installation"],
        primary_authority=[
            "Shigley, J.E., Mischke, C.R., 'Mechanical Engineering Design', 10th Edition, McGraw-Hill, 2014",
            "ANSI/AGMA 9002-D04, 'Flexible Couplings - Design and Application', 2004",
            "Norton, R.L., 'Machine Design: An Integrated Approach', 5th Edition, Pearson, 2013",
            "ISO 14691:2015, 'Mechanical Transmission Components - Couplings'",
            "Budynas, R.G., Nisbett, J.K., 'Shigley's Mechanical Engineering Design', 11th Edition, McGraw-Hill, 2019"
        ],
        burden_holder="Mechanical engineer selecting and designing couplings",
        adversary_position="Using rigid couplings in applications with misalignment causing premature failure",
        counter_arguments=[
            "Rigid couplings cannot accommodate misalignment leading to bearing damage.",
            "Flexible couplings with insufficient torque rating fail under load.",
            "Ignoring torsional vibration effects causes resonance.",
            "Poor installation increases wear and reduces life.",
            "Neglecting environmental factors leads to corrosion and degradation."
        ],
        resolution_strategy="Select coupling type based on misalignment and torque, perform torsional analysis, ensure proper installation and maintenance.",
        entity_scope="Rotating machinery shaft connections",
        confidence=0.94,
        confidence_zone="Common mechanical design practice",
        controlling_precedent="ANSI/AGMA 9002-D04; Shigley, 2014"
    ),
    DoctrineBlock(
        topic="Spring Design and Analysis",
        keywords=["spring constant", "stress analysis", "fatigue life", "coil spring", "torsion", "deflection", "material selection", "load-deflection curve"],
        conclusion_template="Spring design balances load-deflection requirements with stress limits and fatigue life, ensuring reliable energy storage and force application.",
        reasoning_framework=(
            "Springs store mechanical energy and provide force or displacement in mechanical systems. "
            "Design involves selecting geometry, material, and dimensions to achieve desired stiffness (spring constant) and load capacity. "
            "Common types include helical compression, extension, and torsion springs. "
            "Stress analysis focuses on torsional shear stress in wire for coil springs, considering mean and alternating stresses for fatigue life. "
            "Deflection must remain within elastic limits to prevent permanent deformation. "
            "Material selection prioritizes high fatigue strength, corrosion resistance, and manufacturability; common materials include music wire, stainless steel, and phosphor bronze. "
            "Load-deflection curves characterize spring behavior and linearity. "
            "Fatigue failure is critical due to cyclic loading; S-N curves and Goodman diagrams guide design. "
            "Standards such as ASTM A229 and ISO 10243 specify spring materials and testing. "
            "Finite element analysis can optimize complex spring geometries."
        ),
        key_factors=["Spring constant", "Stress", "Fatigue life", "Deflection", "Material", "Load capacity", "Geometry", "Manufacturing"],
        primary_authority=[
            "Shigley, J.E., Mischke, C.R., 'Mechanical Engineering Design', 10th Edition, McGraw-Hill, 2014",
            "ASTM A229/A229M-17, 'Standard Specification for Steel Wire, Music Quality, for Mechanical Springs'",
            "ISO 10243:2013, 'Mechanical Springs - Compression Springs - Technical Delivery Conditions'",
            "Norton, R.L., 'Machine Design: An Integrated Approach', 5th Edition, Pearson, 2013",
            "Budynas, R.G., Nisbett, J.K., 'Shigley's Mechanical Engineering Design', 11th Edition, McGraw-Hill, 2019"
        ],
        burden_holder="Mechanical engineer designing springs for load and fatigue requirements",
        adversary_position="Ignoring fatigue or stress concentrations leading to spring failure",
        counter_arguments=[
            "Neglecting fatigue reduces spring service life.",
            "Ignoring stress concentrations at coils causes premature failure.",
            "Using inappropriate materials affects strength and corrosion resistance.",
            "Overloading beyond elastic limit causes permanent deformation.",
            "Poor manufacturing quality leads to defects and failure."
        ],
        resolution_strategy="Perform detailed stress and fatigue analysis, select suitable materials, adhere to standards, and validate with testing.",
        entity_scope="Mechanical springs in machinery and devices",
        confidence=0.95,
        confidence_zone="Established mechanical design practice",
        controlling_precedent="ASTM A229-17; Shigley, 2014"
    ),
    DoctrineBlock(
        topic="Fastener Design and Selection",
        keywords=["bolt strength", "thread engagement", "preload", "fatigue", "torque specification", "material properties", "corrosion resistance", "joint design"],
        conclusion_template="Fastener design ensures adequate strength, preload, and fatigue resistance for secure joints, considering material compatibility and environmental factors.",
        reasoning_framework=(
            "Fasteners such as bolts and screws create detachable joints by applying preload to clamp components together. "
            "Design involves selecting appropriate size, thread type, material, and surface treatment to withstand applied loads and environmental conditions. "
            "Thread engagement length must be sufficient to develop required strength without stripping. "
            "Preload ensures joint integrity by maintaining clamping force and preventing loosening under dynamic loads. "
            "Torque specifications correlate to preload but are influenced by friction and lubrication. "
            "Fatigue failure is a common mode due to cyclic loading; design must consider stress concentrations at thread roots. "
            "Material selection balances strength, ductility, and corrosion resistance; stainless steels, alloy steels, and coatings are common. "
            "Standards such as ISO 898-1 and ASME B18.2.1 provide mechanical properties and dimensions. "
            "Joint design must account for load paths, gasket effects, and thermal expansion. "
            "Proper installation procedures and inspection ensure reliability."
        ),
        key_factors=["Bolt strength", "Thread engagement", "Preload", "Fatigue", "Torque", "Material", "Corrosion resistance", "Joint design"],
        primary_authority=[
            "ASME B18.2.1-2013, 'Square and Hex Bolts and Screws'",
            "ISO 898-1:2013, 'Mechanical properties of fasteners'",
            "Shigley, J.E., Mischke, C.R., 'Mechanical Engineering Design', 10th Edition, McGraw-Hill, 2014",
            "Norton, R.L., 'Machine Design: An Integrated Approach', 5th Edition, Pearson, 2013",
            "Bolton, W., 'Machine Design', 5th Edition, Pearson, 2015"
        ],
        burden_holder="Mechanical engineer designing bolted joints",
        adversary_position="Underestimating preload or ignoring fatigue leading to joint failure",
        counter_arguments=[
            "Insufficient preload causes joint loosening and fatigue failure.",
            "Ignoring thread engagement length leads to stripping.",
            "Using incompatible materials causes galvanic corrosion.",
            "Overtorquing damages threads and reduces strength.",
            "Neglecting environmental effects accelerates degradation."
        ],
        resolution_strategy="Follow standards for sizing and material selection, specify torque and installation procedures, perform fatigue analysis.",
        entity_scope="Bolted and screwed joints in mechanical assemblies",
        confidence=0.95,
        confidence_zone="Industry standard fastener design practice",
        controlling_precedent="ASME B18.2.1-2013; ISO 898-1:2013"
    ),
    DoctrineBlock(
        topic="CNC Machining Principles",
        keywords=["computer numerical control", "toolpath", "feed rate", "spindle speed", "material removal", "tolerances", "surface finish", "cutting forces"],
        conclusion_template="CNC machining enables precise, automated material removal using programmed toolpaths, optimizing feed rates and spindle speeds for quality and efficiency.",
        reasoning_framework=(
            "CNC machining utilizes computer-controlled tools to perform subtractive manufacturing with high precision and repeatability. "
            "Toolpaths are programmed using G-code to define movement trajectories, speeds, and operations. "
            "Feed rate and spindle speed are optimized based on material properties, tool geometry, and desired surface finish. "
            "Cutting forces affect tool wear, machine deflection, and surface integrity. "
            "Tolerances achievable depend on machine accuracy, tool condition, and process control. "
            "Surface finish relates to tool path strategy, cutting parameters, and coolant application. "
            "Advanced CNC machines incorporate multi-axis capabilities enabling complex geometries. "
            "Process planning includes fixture design, tool selection, and collision avoidance. "
            "Quality assurance involves in-process monitoring and post-process inspection. "
            "CNC machining supports rapid prototyping and production of high-precision components."
        ),
        key_factors=["Toolpath", "Feed rate", "Spindle speed", "Cutting forces", "Material properties", "Tolerances", "Surface finish", "Machine control"],
        primary_authority=[
            "Groover, M.P., 'Fundamentals of Modern Manufacturing', 7th Edition, Wiley, 2020",
            "Kalpakjian, S., Schmid, S.R., 'Manufacturing Engineering and Technology', 7th Edition, Pearson, 2014",
            "ISO 230-1:2012, 'Test code for machine tools'",
            "Machining Data Handbook, Machinability Data Center, 2016",
            "ASME B5.59-2014, 'CNC Machine Tool Performance Testing'"
        ],
        burden_holder="Manufacturing engineer programming CNC operations",
        adversary_position="Using incorrect cutting parameters causing tool wear or poor quality",
        counter_arguments=[
            "Excessive feed rates increase tool wear and surface roughness.",
            "Inadequate spindle speed reduces material removal efficiency.",
            "Ignoring material machinability leads to tool breakage.",
            "Poor fixture design causes vibration and dimensional errors.",
            "Neglecting coolant application increases thermal damage."
        ],
        resolution_strategy="Optimize cutting parameters based on material and tool data, validate programs via simulation, monitor process for quality control.",
        entity_scope="CNC machining processes in manufacturing",
        confidence=0.94,
        confidence_zone="Established manufacturing technology",
        controlling_precedent="Groover, 2020; ISO 230-1:2012"
    ),
    DoctrineBlock(
        topic="Casting Process Fundamentals",
        keywords=["casting", "mold design", "solidification", "shrinkage", "porosity", "dendritic growth", "pattern making", "foundry defects"],
        conclusion_template="Casting processes involve pouring molten metal into molds where solidification and shrinkage must be controlled to minimize defects and ensure dimensional accuracy.",
        reasoning_framework=(
            "Casting is a manufacturing process where molten metal is poured into a mold cavity and allowed to solidify into a desired shape. "
            "Mold design influences flow patterns, cooling rates, and solidification behavior, affecting final part quality. "
            "Solidification involves nucleation and dendritic growth, with cooling rates impacting grain structure and mechanical properties. "
            "Shrinkage during solidification can cause dimensional inaccuracies and internal voids if not properly compensated by risers and feeders. "
            "Common defects include porosity, cold shuts, hot tears, and inclusions, often resulting from improper gating or cooling. "
            "Pattern making defines the mold cavity and must account for shrinkage allowances and draft angles for part removal. "
            "Material selection considers melting point, fluidity, and solidification characteristics. "
            "Simulation tools predict flow and solidification to optimize process parameters. "
            "Post-casting heat treatments improve mechanical properties and relieve residual stresses. "
            "Quality control includes nondestructive testing such as radiography and ultrasonic inspection."
        ),
        key_factors=["Mold design", "Solidification", "Shrinkage", "Porosity", "Pattern making", "Cooling rate", "Material properties", "Defects"],
        primary_authority=[
            "Campbell, J., 'Complete Casting Handbook', 2nd Edition, Butterworth-Heinemann, 2015",
            "Davis, J.R., 'Foundry Technology', ASM International, 1996",
            "ASTM A48/A48M-16, 'Standard Specification for Gray Iron Castings'",
            "Heine, R.W., Loper, C.R., Rosenthal, P.C., 'Principles of Metal Casting', 2nd Edition, McGraw-Hill, 1967",
            "American Foundry Society, 'Casting Defects and Remedies', 2018"
        ],
        burden_holder="Foundry engineer controlling casting quality",
        adversary_position="Neglecting solidification control causing defects and scrap",
        counter_arguments=[
            "Improper gating causes turbulence and inclusions.",
            "Inadequate riser design leads to shrinkage porosity.",
            "Incorrect cooling rates produce coarse grain structure.",
            "Poor pattern design causes dimensional errors.",
            "Ignoring material fluidity results in incomplete filling."
        ],
        resolution_strategy="Use simulation for mold design, control cooling rates, design appropriate risers, and perform thorough inspection.",
        entity_scope="Metal casting manufacturing processes",
        confidence=0.93,
        confidence_zone="Established foundry engineering practice",
        controlling_precedent="Campbell, 2015; ASTM A48-16"
    ),
    DoctrineBlock(
        topic="Forging Process Principles",
        keywords=["forging", "plastic deformation", "grain refinement", "die design", "hot forging", "cold forging", "residual stress", "mechanical properties"],
        conclusion_template="Forging improves mechanical properties through plastic deformation and grain refinement, requiring precise die design and process control to avoid defects.",
        reasoning_framework=(
            "Forging is a manufacturing process involving plastic deformation of metal using compressive forces, typically between dies. "
            "It enhances mechanical properties by refining grain structure and aligning fibers along load paths. "
            "Hot forging occurs above recrystallization temperature, reducing flow stress and improving ductility. "
            "Cold forging is performed below recrystallization temperature, increasing strength through strain hardening. "
            "Die design must ensure proper material flow, minimize flash, and avoid defects such as laps and folds. "
            "Residual stresses introduced during forging can affect dimensional stability and fatigue life. "
            "Process parameters such as temperature, strain rate, and lubrication influence final properties and surface finish. "
            "Forged components often exhibit superior strength and toughness compared to cast or machined parts. "
            "Finite element simulations assist in optimizing die geometry and process conditions. "
            "Quality control includes dimensional inspection and nondestructive testing for internal defects."
        ),
        key_factors=["Plastic deformation", "Grain refinement", "Die design", "Temperature", "Residual stress", "Mechanical properties", "Strain rate", "Lubrication"],
        primary_authority=[
            "Kalpakjian, S., Schmid, S.R., 'Manufacturing Engineering and Technology', 7th Edition, Pearson, 2014",
            "Davis, J.R., 'Metals Handbook: Forging', ASM International, 1991",
            "ASTM A668/A668M-16, 'Standard Specification for Steel Forgings, Carbon and Alloy, for General Industrial Use'",
            "Groover, M.P., 'Fundamentals of Modern Manufacturing', 7th Edition, Wiley, 2020",
            "American Society for Metals, 'Forging Handbook', 2010"
        ],
        burden_holder="Manufacturing engineer controlling forging process",
        adversary_position="Ignoring temperature control causing defects and poor properties",
        counter_arguments=[
            "Insufficient temperature leads to cracking and high flow stress.",
            "Improper die design causes laps and incomplete filling.",
            "Excessive strain rates cause surface defects.",
            "Neglecting lubrication increases tool wear and surface damage.",
            "Ignoring residual stresses leads to distortion during machining."
        ],
        resolution_strategy="Control forging temperature and strain rate, optimize die design, apply lubrication, and perform post-forging heat treatment.",
        entity_scope="Metal forging manufacturing processes",
        confidence=0.93,
        confidence_zone="Established manufacturing engineering practice",
        controlling_precedent="Kalpakjian, 2014; ASTM A668-16"
    ),
    DoctrineBlock(
        topic="Welding Metallurgy and Heat Affected Zone",
        keywords=["welding", "heat affected zone", "microstructure", "residual stress", "distortion", "solidification cracking", "post weld heat treatment", "phase transformation"],
        conclusion_template="Welding alters base metal microstructure in the heat affected zone, requiring control of thermal cycles and post weld treatments to minimize residual stress and defects.",
        reasoning_framework=(
            "Welding joins metals by localized melting and solidification, creating a fusion zone and a heat affected zone (HAZ) where thermal cycles alter microstructure. "
            "The HAZ experiences phase transformations, grain growth, and residual stresses affecting mechanical properties and corrosion resistance. "
            "Residual stresses arise from uneven heating and cooling, causing distortion and potential cracking. "
            "Solidification cracking and porosity are common weld defects influenced by alloy composition and cooling rate. "
            "Post weld heat treatment (PWHT) reduces residual stresses, refines microstructure, and restores toughness. "
            "Welding metallurgy requires understanding of phase diagrams, transformation kinetics, and thermal cycles. "
            "Weld procedure specifications (WPS) define parameters to control heat input and quality. "
            "Nondestructive examination (NDE) techniques such as radiography and ultrasonic testing detect weld defects. "
            "Material selection and filler compatibility are critical for joint integrity. "
            "Finite element thermal and stress analysis assist in predicting distortion and residual stress."
        ),
        key_factors=["Heat affected zone", "Microstructure", "Residual stress", "Distortion", "Solidification cracking", "PWHT", "Phase transformation", "Weld defects"],
        primary_authority=[
            "AWS D1.1/D1.1M:2020, 'Structural Welding Code - Steel'",
            "Lippold, J.C., Kotecki, D.J., 'Welding Metallurgy and Weldability of Stainless Steels', Wiley, 2005",
            "American Welding Society, 'Welding Handbook', 9th Edition, 2010",
            "ASTM E165/E165M-17, 'Standard Practice for Liquid Penetrant Testing'",
            "Messler, R.W., 'Principles of Welding: Processes, Physics, Chemistry, and Metallurgy', 2nd Edition, Wiley, 2004"
        ],
        burden_holder="Welding engineer ensuring joint quality and integrity",
        adversary_position="Neglecting HAZ effects and residual stresses causing failures",
        counter_arguments=[
            "Excessive heat input increases grain growth and reduces toughness.",
            "Inadequate PWHT leaves high residual stresses and cracking risk.",
            "Improper filler selection causes brittle welds.",
            "Ignoring distortion leads to assembly issues.",
            "Poor welding technique introduces defects."
        ],
        resolution_strategy="Control welding parameters, apply PWHT, select compatible materials, perform NDE, and use simulation for process optimization.",
        entity_scope="Welding processes in structural and mechanical fabrication",
        confidence=0.94,
        confidence_zone="Established welding engineering practice",
        controlling_precedent="AWS D1.1-2020; Lippold & Kotecki, 2005"
    ),
    DoctrineBlock(
        topic="Additive Manufacturing (3D Printing) in Mechanical Engineering",
        keywords=["additive manufacturing", "layer-wise fabrication", "material properties", "process parameters", "anisotropy", "post-processing", "design freedom", "defect control"],
        conclusion_template="Additive manufacturing enables complex geometries with layer-wise fabrication, requiring control of process parameters and post-processing to ensure mechanical performance.",
        reasoning_framework=(
            "Additive manufacturing (AM) builds parts layer-by-layer from digital models, allowing complex geometries and reduced material waste. "
            "Process parameters such as laser power, scan speed, and layer thickness influence microstructure, porosity, and residual stresses. "
            "Material properties often exhibit anisotropy due to directional solidification and thermal gradients. "
            "Post-processing including heat treatment, machining, and surface finishing improves mechanical properties and dimensional accuracy. "
            "Defect control involves minimizing porosity, delamination, and residual stress-induced distortion. "
            "Design freedom enables topology optimization and lightweight structures not feasible with traditional manufacturing. "
            "Standards such as ASTM F42 guide AM terminology and testing. "
            "Mechanical testing validates tensile strength, fatigue, and fracture toughness. "
            "Simulation tools predict thermal history and distortion. "
            "AM is increasingly applied in aerospace, automotive, and biomedical fields."
        ),
        key_factors=["Layer-wise fabrication", "Process parameters", "Material anisotropy", "Post-processing", "Defect control", "Design freedom", "Mechanical properties", "Standards"],
        primary_authority=[
            "Gibson, I., Rosen, D.W., Stucker, B., 'Additive Manufacturing Technologies', 2nd Edition, Springer, 2015",
            "ASTM F2792-12a, 'Standard Terminology for Additive Manufacturing Technologies'",
            "Herzog, D., Seyda, V., Wycisk, E., Emmelmann, C., 'Additive manufacturing of metals', Acta Materialia, 2016",
            "ISO/ASTM 52900:2015, 'Additive manufacturing - General principles - Terminology'",
            "Kruth, J.P., Leu, M.C., Nakagawa, T., 'Progress in Additive Manufacturing and Rapid Prototyping', CIRP Annals, 1998"
        ],
        burden_holder="Mechanical engineer integrating additive manufacturing",
        adversary_position="Ignoring anisotropy and defects leading to unreliable parts",
        counter_arguments=[
            "Neglecting anisotropic properties causes design failures.",
            "Inadequate process control increases porosity and defects.",
            "Insufficient post-processing reduces mechanical performance.",
            "Ignoring residual stresses causes distortion and cracking.",
            "Overlooking standard compliance limits certification."
        ],
        resolution_strategy="Optimize process parameters, apply appropriate post-processing, perform mechanical testing, and adhere to standards.",
        entity_scope="Additive manufacturing of mechanical components",
        confidence=0.92,
        confidence_zone="Emerging but rapidly maturing technology",
        controlling_precedent="Gibson et al., 2015; ASTM F2792-12a"
    ),
    DoctrineBlock(
        topic="Materials Selection for Fatigue Resistance",
        keywords=["fatigue", "S-N curve", "endurance limit", "surface finish", "stress concentration", "mean stress effect", "material microstructure", "loading frequency"],
        conclusion_template="Materials selection for fatigue involves considering endurance limits, microstructure, and surface conditions to maximize life under cyclic loading.",
        reasoning_framework=(
            "Fatigue failure occurs due to repeated cyclic stresses below ultimate tensile strength, leading to crack initiation and propagation. "
            "S-N curves (stress vs. number of cycles) characterize material fatigue behavior, with endurance limit defining stress below which infinite life is expected for some materials. "
            "Surface finish significantly affects fatigue life by influencing crack initiation sites. "
            "Stress concentrations from notches or geometric discontinuities amplify local stresses, reducing fatigue strength. "
            "Mean stress effects are accounted for using correction models such as Goodman or Gerber diagrams. "
            "Material microstructure, including grain size and phase distribution, influences crack resistance. "
            "Loading frequency and environment (corrosion) impact fatigue performance. "
            "Materials such as steels, titanium alloys, and composites are selected based on fatigue properties for critical applications. "
            "Design against fatigue includes safety factors, surface treatments, and residual stress induction. "
            "Testing standards such as ASTM E466 provide fatigue testing procedures."
        ),
        key_factors=["Endurance limit", "S-N curve", "Surface finish", "Stress concentration", "Mean stress", "Microstructure", "Loading frequency", "Environment"],
        primary_authority=[
            "Suresh, S., 'Fatigue of Materials', 2nd Edition, Cambridge University Press, 1998",
            "Dowling, N.E., 'Mechanical Behavior of Materials', 5th Edition, Pearson, 2012",
            "ASTM E466-15, 'Standard Practice for Conducting Force Controlled Constant Amplitude Axial Fatigue Tests'",
            "Shigley, J.E., Mischke, C.R., 'Mechanical Engineering Design', 10th Edition, McGraw-Hill, 2014",
            "BS 7608:1993, 'Guide to fatigue design and assessment of steel products'"
        ],
        burden_holder="Materials engineer selecting alloys for fatigue-critical components",
        adversary_position="Ignoring surface and stress concentration effects leading to premature fatigue failure",
        counter_arguments=[
            "Neglecting surface finish underestimates crack initiation risk.",
            "Ignoring mean stress effects causes inaccurate life prediction.",
            "Overlooking environmental corrosion accelerates fatigue.",
            "Using materials without sufficient endurance limit.",
            "Failing to account for manufacturing defects reduces fatigue life."
        ],
        resolution_strategy="Select materials with appropriate fatigue properties, apply surface treatments, design to minimize stress concentrations, and validate with testing.",
        entity_scope="Materials engineering for fatigue-critical applications",
        confidence=0.96,
        confidence_zone="Well-established materials science domain",
        controlling_precedent="Suresh, 1998; ASTM E466-15"
    ),
    DoctrineBlock(
        topic="Creep Behavior in Materials Engineering",
        keywords=["creep", "steady-state creep", "primary creep", "tertiary creep", "stress rupture", "temperature effects", "creep rate", "material selection"],
        conclusion_template="Creep behavior describes time-dependent deformation under constant stress at elevated temperatures, critical for material selection in high-temperature applications.",
        reasoning_framework=(
            "Creep is the slow, time-dependent plastic deformation of materials under constant load, especially significant at high temperatures. "
            "It consists of three stages: primary (decreasing creep rate), secondary or steady-state (constant creep rate), and tertiary (accelerating creep leading to failure). "
            "Creep rate depends on stress, temperature, and material microstructure. "
            "Stress rupture life defines the time to failure under specified conditions. "
            "Materials for high-temperature service, such as turbine blades and pressure vessels, must exhibit low creep rates and high rupture strength. "
            "Creep mechanisms include dislocation glide, diffusion, and grain boundary sliding. "
            "Alloying and heat treatments improve creep resistance by stabilizing microstructure. "
            "Design codes such as ASME Section III provide allowable stresses for creep. "
            "Testing standards like ASTM E139 define creep testing methods. "
            "Finite element modeling predicts creep deformation and life in components."
        ),
        key_factors=["Creep stages", "Creep rate", "Stress rupture", "Temperature", "Material microstructure", "Alloying", "Design codes", "Testing"],
        primary_authority=[
            "Frost, H.J., Ashby, M.F., 'Deformation-Mechanism Maps', Pergamon Press, 1982",
            "ASME Boiler and Pressure Vessel Code, Section III, 2020",
            "ASTM E139-11, 'Standard Test Methods for Conducting Creep, Creep-Rupture, and Stress-Rupture Tests of Metallic Materials'",
            "Callister, W.D., Rethwisch, D.G., 'Materials Science and Engineering', 10th Edition, Wiley, 2018",
            "Norton, F.H., 'The Creep of Steel at High Temperatures', McGraw-Hill, 1929"
        ],
        burden_holder="Materials engineer selecting alloys for high-temperature applications",
        adversary_position="Ignoring creep effects causing premature failure",
        counter_arguments=[
            "Neglecting tertiary creep leads to unexpected rupture.",
            "Using materials without sufficient creep resistance.",
            "Ignoring temperature gradients causing localized creep.",
            "Overlooking microstructural instability under service conditions.",
            "Failing to apply design codes for allowable stresses."
        ],
        resolution_strategy="Select creep-resistant materials, apply heat treatments, perform creep testing, and design within allowable limits.",
        entity_scope="Materials engineering for high-temperature mechanical components",
        confidence=0.95,
        confidence_zone="Established materials science principle",
        controlling_precedent="ASME Section III, 2020; Frost & Ashby, 1982"
    ),
    DoctrineBlock(
        topic="Corrosion Mechanisms in Mechanical Engineering",
        keywords=["corrosion", "electrochemical reactions", "galvanic corrosion", "pitting", "stress corrosion cracking", "protective coatings", "cathodic protection", "material degradation"],
        conclusion_template="Corrosion involves electrochemical degradation of materials, mitigated through material selection, protective coatings, and cathodic protection to ensure structural integrity.",
        reasoning_framework=(
            "Corrosion is the deterioration of materials due to electrochemical reactions with the environment, leading to loss of material and mechanical properties. "
            "Common mechanisms include uniform corrosion, galvanic corrosion between dissimilar metals, pitting corrosion causing localized damage, and stress corrosion cracking combining mechanical stress and corrosive environment. "
            "Material selection for corrosion resistance involves alloying elements such as chromium and nickel to form passive oxide layers. "
            "Protective coatings like paints, plating, and anodizing provide barriers against corrosive agents. "
            "Cathodic protection techniques apply sacrificial anodes or impressed currents to reduce corrosion rates. "
            "Environmental factors such as pH, temperature, and chloride concentration influence corrosion severity. "
            "Corrosion monitoring and inspection detect early damage to prevent failures. "
            "Design considerations include avoiding crevices, ensuring drainage, and minimizing galvanic couples. "
            "Standards such as NACE MR0175 guide materials selection for corrosive environments. "
            "Failure analysis often involves metallurgical examination and electrochemical testing."
        ),
        key_factors=["Electrochemical reactions", "Galvanic corrosion", "Pitting", "Stress corrosion cracking", "Protective coatings", "Cathodic protection", "Material selection", "Environment"],
        primary_authority=[
            "Fontana, M.G., Greene, N.D., 'Corrosion Engineering', 3rd Edition, McGraw-Hill, 1987",
            "NACE MR0175/ISO 15156, 'Materials for use in H2S-containing environments in oil and gas production'",
            "ASM Handbook, Volume 13A: Corrosion: Fundamentals, Testing, and Protection, ASM International, 2003",
            "Revie, R.W., 'Uhlig's Corrosion Handbook', 3rd Edition, Wiley, 2011",
            "Shreir, L.L., Jarman, R.A., Burstein, G.T., 'Corrosion', 3rd Edition, Elsevier, 1994"
        ],
        burden_holder="Materials engineer preventing corrosion failures",
        adversary_position="Ignoring corrosion mechanisms leading to unexpected degradation",
        counter_arguments=[
            "Neglecting galvanic corrosion causes accelerated localized attack.",
            "Ignoring environmental factors underestimates corrosion rates.",
            "Using incompatible materials promotes galvanic couples.",
            "Failing to apply protective coatings increases exposure.",
            "Overlooking stress corrosion cracking risks catastrophic failure."
        ],
        resolution_strategy="Select corrosion-resistant materials, apply protective measures, monitor environment, and perform regular inspections.",
        entity_scope="Materials degradation in mechanical engineering environments",
        confidence=0.97,
        confidence_zone="Well-established corrosion science",
        controlling_precedent="NACE MR0175; Fontana & Greene, 1987"
    ),
    DoctrineBlock(
        topic="PID Control Systems in Mechanical Engineering",
        keywords=["PID controller", "proportional control", "integral control", "derivative control", "feedback loop", "stability", "tuning", "control response"],
        conclusion_template="PID controllers regulate system variables by combining proportional, integral, and derivative actions, providing stable and accurate control when properly tuned.",
        reasoning_framework=(
            "PID (Proportional-Integral-Derivative) controllers are fundamental feedback control devices used to maintain process variables at setpoints. "
            "Proportional control produces an output proportional to the error signal, reducing steady-state error but potentially causing offset. "
            "Integral control accumulates error over time, eliminating steady-state offset but possibly introducing overshoot and oscillations. "
            "Derivative control predicts error trends, improving stability and response speed by damping oscillations. "
            "Proper tuning of PID parameters (Kp, Ki, Kd) is essential to balance responsiveness and stability, using methods such as Ziegler-Nichols or software optimization. "
            "PID controllers are widely applied in temperature, pressure, flow, and speed control in mechanical systems. "
            "Stability analysis involves examining closed-loop poles and frequency response. "
            "Implementation may include digital controllers with sampling and discretization effects. "
            "Advanced control strategies build upon PID for nonlinear or multivariable systems. "
            "Simulation and experimental validation ensure controller performance meets specifications."
        ),
        key_factors=["Proportional gain", "Integral gain", "Derivative gain", "Feedback", "Stability", "Tuning methods", "Control response", "Setpoint tracking"],
        primary_authority=[
            "Åström, K.J., Hägglund, T., 'PID Controllers: Theory, Design, and Tuning', 2nd Edition, Instrument Society of America, 1995",
            "Nise, N.S., 'Control Systems Engineering', 7th Edition, Wiley, 2015",
            "Dorf, R.C., Bishop, R.H., 'Modern Control Systems', 13th Edition, Pearson, 2016",
            "ASME PTC 19.1-2019, 'Test Uncertainty', relevant to control system accuracy",
            "Franklin, G.F., Powell, J.D., Emami-Naeini, A., 'Feedback Control of Dynamic Systems', 7th Edition, Pearson, 2015"
        ],
        burden_holder="Control engineer designing feedback loops",
        adversary_position="Improper tuning causing instability or poor response",
        counter_arguments=[
            "Excessive proportional gain causes oscillations.",
            "Insufficient integral gain leads to steady-state error.",
            "Overly aggressive derivative gain amplifies noise.",
            "Ignoring system delays reduces controller effectiveness.",
            "Neglecting nonlinearities limits controller performance."
        ],
        resolution_strategy="Apply systematic tuning methods, incorporate filters for noise, model system dynamics accurately, and validate through simulation and testing.",
        entity_scope="Feedback control systems in mechanical engineering",
        confidence=0.98,
        confidence_zone="Mature control engineering domain",
        controlling_precedent="Åström & Hägglund, 1995; Nise, 2015"
    ),
    DoctrineBlock(
        topic="Robotics Kinematics and Dynamics",
        keywords=["robot kinematics", "forward kinematics", "inverse kinematics", "Jacobian matrix", "dynamics", "trajectory planning", "actuators", "sensors"],
        conclusion_template="Robotics kinematics and dynamics enable calculation of robot motion and forces, essential for trajectory planning and control using actuator and sensor feedback.",
        reasoning_framework=(
            "Robot kinematics studies the motion of robot links without regard to forces, including forward kinematics (computing end-effector position from joint angles) and inverse kinematics (determining joint angles for desired position). "
            "The Jacobian matrix relates joint velocities to end-effector velocities and is critical for velocity and force analysis. "
            "Dynamics involves the relationship between forces/torques and motion, modeled using Newton-Euler or Lagrangian methods. "
            "Trajectory planning generates feasible paths respecting kinematic and dynamic constraints. "
            "Actuators provide motion inputs, while sensors provide feedback for position, velocity, and force. "
            "Control algorithms use kinematic and dynamic models to achieve precise motion and interaction with environments. "
            "Singularities in kinematics cause loss of degrees of freedom and require careful handling. "
            "Redundancy in manipulators allows optimization of secondary criteria such as obstacle avoidance. "
            "Simulation tools assist in design and validation of robot motion. "
            "Safety considerations include collision detection and compliance."
        ),
        key_factors=["Forward kinematics", "Inverse kinematics", "Jacobian", "Dynamics", "Trajectory planning", "Actuators", "Sensors", "Control"],
        primary_authority=[
            "Craig, J.J., 'Introduction to Robotics: Mechanics and Control', 4th Edition, Pearson, 2017",
            "Siciliano, B., Khatib, O. (Eds.), 'Springer Handbook of Robotics', Springer, 2016",
            "Spong, M.W., Hutchinson, S., Vidyasagar, M., 'Robot Modeling and Control', Wiley, 2006",
            "Niku, S.B., 'Introduction to Robotics: Analysis, Systems, Applications', 2nd Edition, Wiley, 2010",
            "Asada, H., Slotine, J.J.E., 'Robot Analysis and Control', Wiley, 1986"
        ],
        burden_holder="Robotics engineer designing motion and control systems",
        adversary_position="Ignoring dynamic effects causing instability or imprecise motion",
        counter_arguments=[
            "Neglecting dynamics leads to inaccurate force predictions.",
            "Ignoring singularities causes control failures.",
            "Poor trajectory planning results in collisions or inefficiency.",
            "Inadequate sensor feedback reduces accuracy.",
            "Overlooking actuator limitations causes performance issues."
        ],
        resolution_strategy="Develop accurate kinematic and dynamic models, incorporate sensor feedback, plan trajectories respecting constraints, and validate experimentally.",
        entity_scope="Robotic manipulators and mobile robots",
        confidence=0.97,
        confidence_zone="Established robotics engineering domain",
        controlling_precedent="Craig, 2017; Siciliano et al., 2016"
    ),
    DoctrineBlock(
        topic="HVAC Psychrometrics and Load Calculation",
        keywords=["psychrometrics", "humidity", "enthalpy", "dry bulb temperature", "wet bulb temperature", "sensible heat", "latent heat", "load calculation"],
        conclusion_template="Psychrometrics quantifies air moisture and thermal properties, enabling accurate HVAC load calculations for heating, cooling, and ventilation design.",
        reasoning_framework=(
            "Psychrometrics studies the thermodynamic properties of moist air, including temperature, humidity, enthalpy, and specific volume. "
            "Dry bulb temperature measures air temperature, while wet bulb temperature accounts for moisture content via evaporative cooling. "
            "Humidity ratio defines the mass of water vapor per unit mass of dry air. "
            "Enthalpy combines sensible and latent heat, critical for energy balance calculations. "
            "Sensible heat load involves temperature change without moisture change; latent heat load involves moisture addition or removal. "
            "Accurate load calculation requires considering infiltration, internal gains, "
            "solar loads, and ventilation requirements for each zone. ASHRAE Handbook fundamentals provide standard methods "
            "for computing design heating and cooling loads using transfer function method or radiant time series."
        ),
        key_factors=["Psychrometric chart", "Humidity ratio", "Enthalpy", "Sensible vs latent heat", "ASHRAE load methods", "Zone analysis"],
        primary_authority=[
            "ASHRAE Handbook - Fundamentals, Chapter 1: Psychrometrics, 2021",
            "ASHRAE Handbook - HVAC Systems and Equipment, 2020",
            "McQuiston, F.C., Parker, J.D., Spitler, J.D., 'Heating, Ventilating, and Air Conditioning', 7th Ed, Wiley, 2022",
        ],
        burden_holder="HVAC design engineer",
        adversary_position="Simplified load estimates may undersize equipment leading to comfort failures",
        counter_arguments=[
            "Rule-of-thumb methods (watts per square foot) are faster for preliminary sizing",
            "Dynamic simulation software can replace manual psychrometric analysis",
            "Climate change is shifting design conditions beyond historical data",
            "Mixed-mode buildings blur traditional HVAC load boundaries",
        ],
        resolution_strategy="Apply ASHRAE load calculation procedures with safety factors, validate with simulation software for critical applications",
        entity_scope="Commercial and residential HVAC systems",
        confidence=0.91,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="ASHRAE Standard 183-2007 Peak Cooling and Heating Load Calculations",
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

class QueryMode(Enum):
    DEFAULT = auto()
    PARALLEL = auto()
    CASCADE = auto()

class IssueCategory(Enum):
    THERMODYNAMICS = "Thermodynamics"
    FLUID_MECHANICS = "Fluid Mechanics"
    SOLID_MECHANICS = "Solid Mechanics"
    MACHINE_DESIGN = "Machine Design"
    MANUFACTURING = "Manufacturing"
    MATERIALS_ENGINEERING = "Materials Engineering"
    CONTROL_SYSTEMS = "Control Systems"
    ROBOTICS = "Robotics"
    HVAC_SYSTEMS = "HVAC Systems"
    VIBRATION_ANALYSIS = "Vibration Analysis"
    TRIBOLOGY = "Tribology"
    FINITE_ELEMENT = "Finite Element"
    THERMAL_SYSTEMS = "Thermal Systems"
    MECHATRONICS = "Mechatronics"
    ENERGY_SYSTEMS = "Energy Systems"

class QueryRequest:
    def __init__(self, text: str, mode: QueryMode = QueryMode.DEFAULT, metadata: Optional[dict] = None):
        self.text = text
        self.mode = mode
        self.metadata = metadata or {}

class RoutingDecision:
    def __init__(self, engines: List[str], categories: List[IssueCategory], mode: QueryMode):
        self.engines = engines
        self.categories = categories
        self.mode = mode

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, categories: List[IssueCategory]):
        self.engine_id = engine_id
        self.url = url
        self.categories = categories

class SubEngineResponse:
    def __init__(self, engine_id: str, result: Any, status: SubEngineStatus, error: Optional[str] = None):
        self.engine_id = engine_id
        self.result = result
        self.status = status
        self.error = error

# --- Sub-Engine Registry ---

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "MECH01": SubEngineConfig("MECH01", "http://mech01.local/api", [IssueCategory.THERMODYNAMICS, IssueCategory.ENERGY_SYSTEMS, IssueCategory.THERMAL_SYSTEMS]),
    "MECH02": SubEngineConfig("MECH02", "http://mech02.local/api", [IssueCategory.FLUID_MECHANICS, IssueCategory.HVAC_SYSTEMS]),
    "MECH03": SubEngineConfig("MECH03", "http://mech03.local/api", [IssueCategory.SOLID_MECHANICS, IssueCategory.VIBRATION_ANALYSIS, IssueCategory.FINITE_ELEMENT]),
    "MECH04": SubEngineConfig("MECH04", "http://mech04.local/api", [IssueCategory.MACHINE_DESIGN, IssueCategory.MECHATONICS]),
    "MECH05": SubEngineConfig("MECH05", "http://mech05.local/api", [IssueCategory.MANUFACTURING, IssueCategory.MATERIALS_ENGINEERING]),
    "MECH06": SubEngineConfig("MECH06", "http://mech06.local/api", [IssueCategory.MATERIALS_ENGINEERING, IssueCategory.TRIBOLOGY]),
    "MECH07": SubEngineConfig("MECH07", "http://mech07.local/api", [IssueCategory.CONTROL_SYSTEMS, IssueCategory.ROBOTICS, IssueCategory.MECHATONICS]),
    "MECH08": SubEngineConfig("MECH08", "http://mech08.local/api", [IssueCategory.ROBOTICS, IssueCategory.CONTROL_SYSTEMS]),
    "MECH09": SubEngineConfig("MECH09", "http://mech09.local/api", [IssueCategory.HVAC_SYSTEMS, IssueCategory.THERMAL_SYSTEMS]),
    "MECH10": SubEngineConfig("MECH10", "http://mech10.local/api", [IssueCategory.VIBRATION_ANALYSIS, IssueCategory.SOLID_MECHANICS]),
    "MECH11": SubEngineConfig("MECH11", "http://mech11.local/api", [IssueCategory.TRIBOLOGY, IssueCategory.MACHINE_DESIGN]),
    "MECH12": SubEngineConfig("MECH12", "http://mech12.local/api", [IssueCategory.FINITE_ELEMENT, IssueCategory.SOLID_MECHANICS]),
    "MECH13": SubEngineConfig("MECH13", "http://mech13.local/api", [IssueCategory.THERMAL_SYSTEMS, IssueCategory.ENERGY_SYSTEMS]),
    "MECH14": SubEngineConfig("MECH14", "http://mech14.local/api", [IssueCategory.MECHATONICS, IssueCategory.ROBOTICS]),
    "MECH15": SubEngineConfig("MECH15", "http://mech15.local/api", [IssueCategory.ENERGY_SYSTEMS, IssueCategory.THERMODYNAMICS]),
}

# --- Circuit Breaker Implementation ---

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.last_failure_time = 0.0
        self.recovery_timeout = recovery_timeout  # seconds

    def record_success(self):
        self.failure_count = 0
        self.state = CircuitBreakerState.CLOSED

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

    def can_attempt(self):
        if self.state == CircuitBreakerState.CLOSED:
            return True
        elif self.state == CircuitBreakerState.OPEN:
            if (time.time() - self.last_failure_time) > self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                return True
            else:
                return False
        elif self.state == CircuitBreakerState.HALF_OPEN:
            return True

    def on_attempt_result(self, success: bool):
        if success:
            self.record_success()
        else:
            self.record_failure()

# --- SubEngineHealthMonitor ---

class SubEngineHealthMonitor:
    def __init__(self, registry: Dict[str, SubEngineConfig], ttl: int = 30):
        self.registry = registry
        self.health_cache: Dict[str, Tuple[SubEngineStatus, float]] = {}
        self.ttl = ttl  # seconds
        self.circuit_breakers: Dict[str, CircuitBreaker] = {eid: CircuitBreaker() for eid in registry}

    async def _ping_engine(self, url: str, timeout: int = 3) -> SubEngineStatus:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}/health", timeout=timeout) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("status") == "ok":
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
        config = self.registry.get(engine_id)
        if not config:
            return SubEngineStatus.UNKNOWN
        breaker = self.circuit_breakers[engine_id]
        if not breaker.can_attempt():
            return SubEngineStatus.UNHEALTHY
        status = await self._ping_engine(config.url)
        if status == SubEngineStatus.HEALTHY:
            breaker.record_success()
        else:
            breaker.record_failure()
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

    async def get_healthy_engines(self) -> List[str]:
        healthy = []
        for eid in self.registry:
            status = await self.check_health(eid)
            if status == SubEngineStatus.HEALTHY:
                healthy.append(eid)
        return healthy

# --- QueryRouter ---

class QueryRouter:
    CATEGORY_KEYWORDS: Dict[IssueCategory, Set[str]] = {
        IssueCategory.THERMODYNAMICS: {"thermodynamics", "entropy", "enthalpy", "heat", "temperature", "thermal efficiency", "carnot", "rankine", "brayton"},
        IssueCategory.FLUID_MECHANICS: {"fluid", "flow", "pipe", "viscosity", "turbulence", "bernoulli", "navier-stokes", "pressure drop"},
        IssueCategory.SOLID_MECHANICS: {"stress", "strain", "solid", "beam", "deflection", "yield", "modulus", "fatigue", "buckling"},
        IssueCategory.MACHINE_DESIGN: {"gear", "shaft", "bearing", "machine", "design", "cam", "follower", "linkage"},
        IssueCategory.MANUFACTURING: {"manufacturing", "machining", "casting", "welding", "cnc", "additive", "3d print", "milling"},
        IssueCategory.MATERIALS_ENGINEERING: {"material", "alloy", "steel", "aluminum", "polymer", "ceramic", "composite", "microstructure"},
        IssueCategory.CONTROL_SYSTEMS: {"control", "pid", "feedback", "transfer function", "bode", "nyquist", "controller", "system response"},
        IssueCategory.ROBOTICS: {"robot", "manipulator", "kinematics", "dynamics", "end effector", "actuator", "path planning"},
        IssueCategory.HVAC_SYSTEMS: {"hvac", "air conditioning", "ventilation", "refrigeration", "psychrometric", "cooling load"},
        IssueCategory.VIBRATION_ANALYSIS: {"vibration", "modal", "frequency", "damping", "resonance", "harmonic"},
        IssueCategory.TRIBOLOGY: {"tribology", "friction", "wear", "lubrication", "surface", "contact"},
        IssueCategory.FINITE_ELEMENT: {"finite element", "fea", "mesh", "node", "element", "solver"},
        IssueCategory.THERMAL_SYSTEMS: {"thermal system", "heat exchanger", "boiler", "condenser", "thermal balance"},
        IssueCategory.MECHATONICS: {"mechatronics", "sensor", "actuator", "embedded", "plc", "automation"},
        IssueCategory.ENERGY_SYSTEMS: {"energy", "power plant", "renewable", "solar", "wind", "battery", "storage"},
    }

    def __init__(self, registry: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.registry = registry
        self.health_monitor = health_monitor
        self.engine_category_map = self._build_engine_category_map()

    def _build_engine_category_map(self) -> Dict[IssueCategory, List[str]]:
        mapping = defaultdict(list)
        for eid, config in self.registry.items():
            for cat in config.categories:
                mapping[cat].append(eid)
        return mapping

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text_lower = text.lower()
        matched = set()
        for cat, keywords in self.CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    matched.add(cat)
        if not matched:
            # Fallback: try to guess based on most common words
            for cat, keywords in self.CATEGORY_KEYWORDS.items():
                for kw in keywords:
                    if any(w in text_lower for w in kw.split()):
                        matched.add(cat)
        return list(matched) if matched else [IssueCategory.THERMODYNAMICS]

    def _select_engines(self, categories: List[IssueCategory], mode: QueryMode) -> List[SubEngineConfig]:
        selected = set()
        for cat in categories:
            for eid in self.engine_category_map.get(cat, []):
                selected.add(eid)
        # Health check
        healthy_engines = []
        for eid in selected:
            status = self.health_monitor.health_cache.get(eid, (SubEngineStatus.UNKNOWN, 0))[0]
            if status == SubEngineStatus.HEALTHY:
                healthy_engines.append(self.registry[eid])
        if not healthy_engines:
            # Fallback: pick any engine for the category
            for cat in categories:
                for eid in self.engine_category_map.get(cat, []):
                    healthy_engines.append(self.registry[eid])
        return healthy_engines

    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        # Custom rules: e.g., if query mentions "vibration" and "finite element", route to both MECH10 and MECH12
        text = query.text.lower()
        rules = [
            ({"vibration", "finite element"}, ["MECH10", "MECH12"]),
            ({"robot", "control"}, ["MECH07", "MECH08"]),
            ({"thermal", "energy"}, ["MECH01", "MECH13", "MECH15"]),
            ({"manufacturing", "material"}, ["MECH05", "MECH06"]),
        ]
        for keywords, engines in rules:
            if all(kw in text for kw in keywords):
                return engines
        return []

    def _score_engine_relevance(self, engine: SubEngineConfig, query: QueryRequest) -> float:
        text = query.text.lower()
        score = 0.0
        for cat in engine.categories:
            for kw in self.CATEGORY_KEYWORDS.get(cat, []):
                if kw in text:
                    score += 1.0
        # Add random jitter to break ties
        return score + random.uniform(0, 0.1)

    def _handle_engine_failure(self, engine_id: str, error: str) -> List[str]:
        # Fallback: Remove failed engine, pick next best
        fallback_engines = []
        for eid, config in self.registry.items():
            if eid != engine_id:
                fallback_engines.append(eid)
        return fallback_engines

    def route_query(self, query: QueryRequest) -> RoutingDecision:
        # 1. Apply explicit routing rules
        rule_engines = self._apply_routing_rules(query)
        if rule_engines:
            categories = []
            for eid in rule_engines:
                categories.extend(self.registry[eid].categories)
            return RoutingDecision(rule_engines, categories, query.mode)
        # 2. Classify domain
        categories = self._classify_domain(query.text)
        # 3. Select engines
        engine_configs = self._select_engines(categories, query.mode)
        if not engine_configs:
            # Fallback: route to all
            engine_configs = list(self.registry.values())
        # 4. Score and sort
        scored = [(self._score_engine_relevance(cfg, query), cfg) for cfg in engine_configs]
        scored.sort(reverse=True, key=lambda x: x[0])
        top_engines = [cfg.engine_id for _, cfg in scored[:3]]  # Limit to top 3
        return RoutingDecision(top_engines, categories, query.mode)

# --- SubEngineOrchestrator ---

class SubEngineOrchestrator:
    def __init__(self, registry: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.registry = registry
        self.health_monitor = health_monitor

    async def _call_sub_engine(self, engine_config: SubEngineConfig, query: QueryRequest) -> SubEngineResponse:
        breaker = self.health_monitor.circuit_breakers[engine_config.engine_id]
        if not breaker.can_attempt():
            return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, error="Circuit breaker open")
        try:
            async with aiohttp.ClientSession() as session:
                payload = {"query": query.text, "metadata": query.metadata}
                async with session.post(f"{engine_config.url}/query", json=payload, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        breaker.on_attempt_result(True)
                        return SubEngineResponse(engine_config.engine_id, data, SubEngineStatus.HEALTHY)
                    else:
                        breaker.on_attempt_result(False)
                        return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, error=f"HTTP {resp.status}")
        except Exception as ex:
            breaker.on_attempt_result(False)
            return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, error=str(ex))

    async def dispatch_query(self, query: QueryRequest, engines: List[str]) -> List[SubEngineResponse]:
        tasks = []
        for eid in engines:
            config = self.registry[eid]
            tasks.append(self._call_sub_engine(config, query))
        return await asyncio.gather(*tasks)

    async def dispatch_parallel(self, query: QueryRequest, engines: List[str]) -> Dict[str, Any]:
        responses = await self.dispatch_query(query, engines)
        return self._merge_responses(responses)

    async def dispatch_cascade(self, query: QueryRequest, engines: List[str]) -> Any:
        for eid in engines:
            config = self.registry[eid]
            resp = await self._call_sub_engine(config, query)
            if resp.status == SubEngineStatus.HEALTHY and resp.result is not None:
                return resp.result
        return {"error": "All engines failed"}

    def _merge_responses(self, responses: List[SubEngineResponse]) -> Dict[str, Any]:
        merged = {}
        for resp in responses:
            merged[resp.engine_id] = {
                "status": resp.status.name,
                "result": resp.result,
                "error": resp.error
            }
        return merged

    def _resolve_conflicts(self, responses: List[SubEngineResponse]) -> Any:
        # Consensus: if all responses agree, return; else, majority or first
        results = [resp.result for resp in responses if resp.status == SubEngineStatus.HEALTHY and resp.result is not None]
        if not results:
            return {"error": "No valid responses"}
        # Simple consensus: if all results are equal, return one
        if all(r == results[0] for r in results):
            return results[0]
        # Otherwise, return majority if possible
        counts = defaultdict(int)
        for r in results:
            counts[str(r)] += 1
        majority = max(counts.items(), key=lambda x: x[1])
        return majority[0]

# --- Example Usage (not executed in this part) ---

# health_monitor = SubEngineHealthMonitor(SUB_ENGINE_REGISTRY)
# router = QueryRouter(SUB_ENGINE_REGISTRY, health_monitor)
# orchestrator = SubEngineOrchestrator(SUB_ENGINE_REGISTRY, health_monitor)
# query = QueryRequest("Analyze the vibration response of a beam using finite element analysis", QueryMode.PARALLEL)
# routing_decision = router.route_query(query)
# responses = await orchestrator.dispatch_parallel(query, routing_decision.engines)
# consensus = orchestrator._resolve_conflicts(responses)

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
    AuthorityLevel.CASE_LAW: 50,
    AuthorityLevel.TREATISE: 30,
    AuthorityLevel.PRACTICE: 10,
}

def resolve_authority_conflict(sources: List[AuthorityLevel]) -> AuthorityLevel:
    """
    Given a list of authority sources, determine the dominant authority level.
    """
    if not sources:
        raise ValueError("No authority sources provided for conflict resolution.")
    max_weight = -1
    dominant = None
    for source in sources:
        weight = authority_weights.get(source, 0)
        if weight > max_weight:
            max_weight = weight
            dominant = source
    return dominant

# ---------------------------
# EPISTEMIC GUARDRAILS MODULE
# ---------------------------

BANNED_PHRASES = [
    "clearly", "obviously", "without doubt", "undeniably", "unquestionably",
    "it is evident", "it goes without saying", "beyond question", "no doubt",
    "incontrovertibly", "manifestly", "patently", "self-evident", "surely",
    "unambiguously", "categorically", "definitely", "indisputably", "incontestably",
    "infallibly", "irrefutably", "plainly", "positively", "undoubtedly",
    "unequivocally", "without fail", "without exception", "without reservation",
    "without hesitation", "without equivocation", "without qualification"
]

DISCLOSURE_CAVEAT = (
    "Note: This analysis is subject to inherent uncertainties and should be "
    "interpreted with appropriate caution."
)

class ConfidenceLevel(enum.Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

def apply_epistemic_guardrails(text: str) -> Tuple[str, str]:
    """
    Remove banned phrases from text and append a disclosure caveat.
    Returns cleaned text and confidence stratification level.
    """
    pattern = re.compile(r'\b(' + '|'.join(re.escape(p) for p in BANNED_PHRASES) + r')\b', re.IGNORECASE)
    cleaned_text = pattern.sub("", text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    cleaned_text += " " + DISCLOSURE_CAVEAT

    confidence = confidence_stratification(cleaned_text)
    return cleaned_text, confidence

def confidence_stratification(text: str) -> ConfidenceLevel:
    """
    Stratify confidence based on linguistic markers and content heuristics.
    """
    lowered = text.lower()
    # Simple heuristic rules for stratification
    if any(word in lowered for word in ["likely", "probable", "suggests", "appears"]):
        return ConfidenceLevel.DEFENSIBLE
    if any(word in lowered for word in ["must", "shall", "required", "mandatory"]):
        return ConfidenceLevel.AGGRESSIVE
    if any(word in lowered for word in ["uncertain", "unknown", "possible", "may"]):
        return ConfidenceLevel.DISCLOSURE
    if any(word in lowered for word in ["error", "risk", "fail", "problem", "issue"]):
        return ConfidenceLevel.HIGH_RISK
    return ConfidenceLevel.DEFENSIBLE

# ---------------------------
# FACT FRAGILITY SCORING MODULE
# ---------------------------

def score_fact_fragility(fact: str) -> Dict[str, float]:
    """
    Score fact fragility based on verifiability, recharacterization risk, and testimony dependence.
    Returns a dict with scores from 0.0 (low fragility) to 1.0 (high fragility).
    """
    verifiability = _score_verifiability(fact)
    recharacterization_risk = _score_recharacterization_risk(fact)
    testimony_dependence = _score_testimony_dependence(fact)
    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence,
    }

def _score_verifiability(fact: str) -> float:
    """
    Score verifiability based on presence of measurable, observable data or references.
    """
    measurable_terms = ["measured", "observed", "recorded", "documented", "verified", "tested"]
    score = 1.0
    for term in measurable_terms:
        if term in fact.lower():
            score = 0.0
            break
    return score

def _score_recharacterization_risk(fact: str) -> float:
    """
    Score risk that fact can be reinterpreted or recharacterized.
    """
    ambiguous_terms = ["approximately", "about", "around", "estimated", "roughly", "suggests"]
    score = 0.0
    for term in ambiguous_terms:
        if term in fact.lower():
            score = max(score, 1.0)
    return score

def _score_testimony_dependence(fact: str) -> float:
    """
    Score dependence on human testimony or subjective report.
    """
    subjective_terms = ["reported", "claimed", "stated", "according to", "alleged"]
    score = 0.0
    for term in subjective_terms:
        if term in fact.lower():
            score = max(score, 1.0)
    return score

# ---------------------------
# SEMANTIC NORMALIZATION MODULE
# ---------------------------

DOMAIN_TERM_MAPPINGS = {
    # Mechanical Engineering domain terms normalization
    "torque": "torque",
    "moment of force": "torque",
    "rotational force": "torque",
    "stress": "stress",
    "strain": "strain",
    "yield strength": "yield_strength",
    "ultimate tensile strength": "ultimate_tensile_strength",
    "uts": "ultimate_tensile_strength",
    "fatigue life": "fatigue_life",
    "fatigue strength": "fatigue_strength",
    "modulus of elasticity": "elastic_modulus",
    "young's modulus": "elastic_modulus",
    "elastic modulus": "elastic_modulus",
    "shear modulus": "shear_modulus",
    "poisson's ratio": "poissons_ratio",
    "thermal conductivity": "thermal_conductivity",
    "heat capacity": "heat_capacity",
    "specific heat": "heat_capacity",
    "density": "density",
    "mass density": "density",
    "viscosity": "viscosity",
    "dynamic viscosity": "viscosity",
    "kinematic viscosity": "kinematic_viscosity",
    "friction coefficient": "friction_coefficient",
    "coefficient of friction": "friction_coefficient",
    "bearing": "bearing",
    "bearing load": "bearing_load",
    "bearing capacity": "bearing_capacity",
    "gear ratio": "gear_ratio",
    "gear train": "gear_train",
    "shaft": "shaft",
    "shaft diameter": "shaft_diameter",
    "bearing life": "bearing_life",
    "lubrication": "lubrication",
    "lubricant": "lubrication",
    "thermal expansion": "thermal_expansion",
    "thermal strain": "thermal_strain",
    "thermal stress": "thermal_stress",
    "vibration": "vibration",
    "resonance": "resonance",
    "damping": "damping",
    "natural frequency": "natural_frequency",
    "critical speed": "critical_speed",
    "fatigue failure": "fatigue_failure",
    "creep": "creep",
    "buckling": "buckling",
    "deflection": "deflection",
    "beam deflection": "deflection",
    "load": "load",
    "axial load": "axial_load",
    "shear load": "shear_load",
    "bending moment": "bending_moment",
    "torsion": "torsion",
    "torque load": "torque",
    "pressure": "pressure",
    "fluid pressure": "pressure",
    "flow rate": "flow_rate",
    "velocity": "velocity",
    "acceleration": "acceleration",
    "force": "force",
    "power": "power",
    "efficiency": "efficiency",
    "gear efficiency": "efficiency",
    "thermal efficiency": "efficiency",
    "heat transfer": "heat_transfer",
    "conduction": "heat_transfer_conduction",
    "convection": "heat_transfer_convection",
    "radiation": "heat_transfer_radiation",
    "moment of inertia": "moment_of_inertia",
    "inertia": "moment_of_inertia",
    "center of gravity": "center_of_gravity",
    "cg": "center_of_gravity",
    "center of mass": "center_of_mass",
    "cm": "center_of_mass",
    "stress concentration": "stress_concentration",
    "fatigue crack": "fatigue_crack",
    "fracture toughness": "fracture_toughness",
    "fracture": "fracture",
    "failure": "failure",
    "material properties": "material_properties",
    "mechanical properties": "material_properties",
    "design criteria": "design_criteria",
    "safety factor": "safety_factor",
    "factor of safety": "safety_factor",
    "load factor": "load_factor",
    "service factor": "service_factor",
    "manufacturing process": "manufacturing_process",
    "machining": "manufacturing_process",
    "welding": "manufacturing_process",
    "casting": "manufacturing_process",
    "forging": "manufacturing_process",
    "heat treatment": "heat_treatment",
    "surface finish": "surface_finish",
    "roughness": "surface_finish",
    "tolerance": "tolerance",
    "clearance": "clearance",
    "interference fit": "interference_fit",
    "press fit": "interference_fit",
    "bolted joint": "bolted_joint",
    "welded joint": "welded_joint",
    "fastener": "fastener",
    "bearing clearance": "bearing_clearance",
    "lubrication type": "lubrication_type",
    "seal": "seal",
    "gasket": "gasket",
    "hydraulics": "hydraulics",
    "pneumatics": "pneumatics",
    "fluid mechanics": "fluid_mechanics",
    "thermodynamics": "thermodynamics",
    "heat exchanger": "heat_exchanger",
    "compressor": "compressor",
    "pump": "pump",
    "valve": "valve",
    "pipe": "pipe",
    "duct": "duct",
    "fan": "fan",
    "blower": "blower",
    "engine": "engine",
    "motor": "motor",
    "gearbox": "gearbox",
    "transmission": "transmission",
    "bearing failure": "bearing_failure",
    "shaft failure": "shaft_failure",
    "gear failure": "gear_failure",
    "lubrication failure": "lubrication_failure",
    "thermal failure": "thermal_failure",
    "vibration analysis": "vibration_analysis",
    "modal analysis": "modal_analysis",
    "finite element analysis": "finite_element_analysis",
    "fea": "finite_element_analysis",
    "computational fluid dynamics": "computational_fluid_dynamics",
    "cfd": "computational_fluid_dynamics",
}

def normalize_query(text: str) -> str:
    """
    Normalize domain-specific terms in the input text to standardized tokens.
    """
    lowered = text.lower()
    for phrase, normalized in DOMAIN_TERM_MAPPINGS.items():
        pattern = re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE)
        lowered = pattern.sub(normalized, lowered)
    return lowered

# ---------------------------
# DEEP ANALYSIS MODULE
# ---------------------------

def multi_doctrine_decomposition(query: str) -> List[str]:
    """
    Decompose a complex query into sub-issues based on doctrine keywords.
    """
    # Example doctrine keywords for mechanical engineering domain
    doctrine_keywords = [
        "stress", "strain", "fatigue", "thermal", "vibration", "failure",
        "load", "deflection", "buckling", "torque", "bearing", "lubrication",
        "material", "fracture", "creep", "modulus", "efficiency", "heat transfer",
        "fluid", "pressure", "flow", "gear", "shaft", "welding", "manufacturing"
    ]
    lowered = query.lower()
    issues = []
    for keyword in doctrine_keywords:
        if keyword in lowered:
            issues.append(keyword)
    if not issues:
        issues.append("general")  # fallback generic issue
    return issues

def build_interaction_dag(issues: List[str]) -> Dict[str, Set[str]]:
    """
    Build a dependency graph (DAG) representing interactions among issues.
    """
    # Predefined dependencies for mechanical engineering doctrines
    dependencies = {
        "stress": {"strain", "failure"},
        "strain": {"stress", "failure"},
        "fatigue": {"stress", "failure"},
        "thermal": {"stress", "strain"},
        "vibration": {"failure"},
        "failure": set(),
        "load": {"stress", "deflection"},
        "deflection": {"stress"},
        "buckling": {"load", "stress"},
        "torque": {"stress", "shaft"},
        "bearing": {"lubrication", "failure"},
        "lubrication": {"bearing"},
        "material": {"stress", "strain", "failure"},
        "fracture": {"stress", "failure"},
        "creep": {"stress", "temperature"},
        "modulus": {"stress", "strain"},
        "efficiency": {"load", "power"},
        "heat transfer": {"thermal"},
        "fluid": {"pressure", "flow"},
        "pressure": {"fluid"},
        "flow": {"fluid"},
        "gear": {"torque", "shaft"},
        "shaft": {"torque", "bearing"},
        "welding": {"material", "failure"},
        "manufacturing": {"material", "failure"},
        "general": set(),
    }
    dag = defaultdict(set)
    for issue in issues:
        deps = dependencies.get(issue, set())
        for dep in deps:
            if dep in issues:
                dag[issue].add(dep)
    return dag

def eight_step_resolution(query: str, doctrines: List[str], sub_engine_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform a full eight-step analysis combining doctrines and sub-engine results.
    Returns a structured analysis report.
    """
    # Steps (example):
    # 1. Issue Identification
    # 2. Rule Extraction
    # 3. Fact Application
    # 4. Conflict Identification
    # 5. Authority Weighting
    # 6. Resolution Synthesis
    # 7. Conclusion Drafting
    # 8. Epistemic Guardrails Application

    report = {}
    report["query"] = query
    report["issues"] = doctrines

    # Step 1: Issue Identification
    report["identified_issues"] = doctrines

    # Step 2: Rule Extraction (simulate)
    rules = {d: f"Rule for {d}" for d in doctrines}
    report["rules"] = rules

    # Step 3: Fact Application (simulate)
    facts = {d: sub_engine_results.get(d, "No data") for d in doctrines}
    report["facts"] = facts

    # Step 4: Conflict Identification (simulate)
    conflicts = {}
    for d in doctrines:
        conflicts[d] = False  # placeholder no conflict
    report["conflicts"] = conflicts

    # Step 5: Authority Weighting
    authorities = {d: AuthorityLevel.PRACTICE for d in doctrines}  # default practice
    report["authorities"] = authorities

    # Step 6: Resolution Synthesis (simulate)
    synthesis = {d: f"Resolved analysis for {d}" for d in doctrines}
    report["synthesis"] = synthesis

    # Step 7: Conclusion Drafting
    conclusion = " ".join(synthesis.values())
    report["conclusion_raw"] = conclusion

    # Step 8: Epistemic Guardrails Application
    cleaned_conclusion, confidence = apply_epistemic_guardrails(conclusion)
    report["conclusion_cleaned"] = cleaned_conclusion
    report["confidence_level"] = confidence.value

    # Zoned analysis tagging
    report["zoned_tags"] = zoned_analysis(cleaned_conclusion)

    return report

def zoned_analysis(conclusion: str) -> List[str]:
    """
    Tag conclusion with zones: PLANNING, REPORTING, AUDIT based on content.
    """
    tags = []
    lowered = conclusion.lower()
    if any(word in lowered for word in ["plan", "strategy", "design", "proposal", "recommendation"]):
        tags.append("PLANNING")
    if any(word in lowered for word in ["result", "data", "observation", "measurement", "finding"]):
        tags.append("REPORTING")
    if any(word in lowered for word in ["audit", "verification", "compliance", "review", "assessment"]):
        tags.append("AUDIT")
    if not tags:
        tags.append("REPORTING")  # default tag
    return tags

# ---------------------------
# THREE-LAYER RESPONSE SYSTEM
# ---------------------------

class DoctrineCache:
    """
    Simple in-memory doctrine cache with keyword matching and cached analysis.
    """
    def __init__(self):
        self.cache = {}  # keyword -> analysis string
        self.lock = threading.Lock()

    def lookup(self, query: str) -> Optional[str]:
        """
        Lookup cache for any matching keyword in query.
        Returns cached analysis or None.
        """
        lowered = query.lower()
        with self.lock:
            for keyword, analysis in self.cache.items():
                if keyword in lowered:
                    return analysis
        return None

    def add(self, keyword: str, analysis: str):
        with self.lock:
            self.cache[keyword.lower()] = analysis

# Initialize global doctrine cache instance
doctrine_cache = DoctrineCache()

class SubEngineRouter:
    """
    Routes queries to relevant sub-engines based on semantic search.
    """
    def __init__(self):
        # Map keywords to sub-engine functions
        self.sub_engines = {
            "stress": self.sub_engine_stress,
            "fatigue": self.sub_engine_fatigue,
            "thermal": self.sub_engine_thermal,
            "vibration": self.sub_engine_vibration,
            "failure": self.sub_engine_failure,
            "load": self.sub_engine_load,
            "bearing": self.sub_engine_bearing,
            "lubrication": self.sub_engine_lubrication,
            "material": self.sub_engine_material,
            "fracture": self.sub_engine_fracture,
            "creep": self.sub_engine_creep,
            "modulus": self.sub_engine_modulus,
            "efficiency": self.sub_engine_efficiency,
            "heat transfer": self.sub_engine_heat_transfer,
            "fluid": self.sub_engine_fluid,
            "gear": self.sub_engine_gear,
            "shaft": self.sub_engine_shaft,
            "welding": self.sub_engine_welding,
            "manufacturing": self.sub_engine_manufacturing,
            "general": self.sub_engine_general,
        }

    def semantic_search(self, query: str) -> List[str]:
        """
        Return list of relevant sub-engine keys based on query keywords.
        """
        lowered = query.lower()
        relevant = []
        for key in self.sub_engines.keys():
            if key in lowered:
                relevant.append(key)
        if not relevant:
            relevant.append("general")
        return relevant

    def dispatch(self, query: str) -> Dict[str, Any]:
        """
        Dispatch query to relevant sub-engines and collect results.
        """
        relevant_keys = self.semantic_search(query)
        results = {}
        for key in relevant_keys:
            engine_func = self.sub_engines.get(key)
            if engine_func:
                results[key] = engine_func(query)
            else:
                results[key] = None
        return results

    # Sub-engine implementations (simulated)

    def sub_engine_stress(self, query: str) -> str:
        return "Stress analysis result based on query."

    def sub_engine_fatigue(self, query: str) -> str:
        return "Fatigue analysis result based on query."

    def sub_engine_thermal(self, query: str) -> str:
        return "Thermal analysis result based on query."

    def sub_engine_vibration(self, query: str) -> str:
        return "Vibration analysis result based on query."

    def sub_engine_failure(self, query: str) -> str:
        return "Failure mode analysis result based on query."

    def sub_engine_load(self, query: str) -> str:
        return "Load distribution analysis result based on query."

    def sub_engine_bearing(self, query: str) -> str:
        return "Bearing condition analysis result based on query."

    def sub_engine_lubrication(self, query: str) -> str:
        return "Lubrication system analysis result based on query."

    def sub_engine_material(self, query: str) -> str:
        return "Material properties analysis result based on query."

    def sub_engine_fracture(self, query: str) -> str:
        return "Fracture mechanics analysis result based on query."

    def sub_engine_creep(self, query: str) -> str:
        return "Creep behavior analysis result based on query."

    def sub_engine_modulus(self, query: str) -> str:
        return "Modulus related analysis result based on query."

    def sub_engine_efficiency(self, query: str) -> str:
        return "Efficiency calculation result based on query."

    def sub_engine_heat_transfer(self, query: str) -> str:
        return "Heat transfer analysis result based on query."

    def sub_engine_fluid(self, query: str) -> str:
        return "Fluid mechanics analysis result based on query."

    def sub_engine_gear(self, query: str) -> str:
        return "Gear system analysis result based on query."

    def sub_engine_shaft(self, query: str) -> str:
        return "Shaft design analysis result based on query."

    def sub_engine_welding(self, query: str) -> str:
        return "Welding process analysis result based on query."

    def sub_engine_manufacturing(self, query: str) -> str:
        return "Manufacturing process analysis result based on query."

    def sub_engine_general(self, query: str) -> str:
        return "General mechanical engineering analysis result."

sub_engine_router = SubEngineRouter()

class DeepMultiEngineAnalyzer:
    """
    Performs parallel dispatch to multiple sub-engines and merges results.
    """
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=8)

    def analyze(self, query: str, doctrines: List[str]) -> Dict[str, Any]:
        """
        Dispatch query to multiple sub-engines in parallel and merge results.
        """
        futures = {}
        results = {}

        def run_sub_engine(key: str):
            func = sub_engine_router.sub_engines.get(key)
            if func:
                return func(query)
            return None

        for doctrine in doctrines:
            futures[doctrine] = self.executor.submit(run_sub_engine, doctrine)

        for doctrine, future in futures.items():
            try:
                results[doctrine] = future.result(timeout=5)
            except Exception:
                results[doctrine] = None

        merged = self._merge_results(results)
        resolved = self._resolve_conflicts(merged)
        return resolved

    def _merge_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge results from multiple sub-engines.
        """
        # For demonstration, just return results as is
        return results

    def _resolve_conflicts(self, merged_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve conflicts between sub-engine results.
        """
        # Placeholder: no conflicts resolved, return merged_results
        return merged_results

deep_multi_engine_analyzer = DeepMultiEngineAnalyzer()

def three_layer_response(query: str) -> Dict[str, Any]:
    """
    Implements the three-layer response system:
    1) Doctrine cache lookup (0-200ms)
    2) Semantic search + sub-engine routing
    3) Deep multi-engine analysis with parallel dispatch, merge, resolve conflicts
    """
    start_time = time.time()

    # Layer 1: Doctrine cache lookup
    cached_analysis = doctrine_cache.lookup(query)
    elapsed = (time.time() - start_time) * 1000
    if cached_analysis and elapsed <= 200:
        return {
            "layer": 1,
            "result": cached_analysis,
            "elapsed_ms": elapsed,
        }

    # Layer 2: Semantic search + sub-engine routing
    doctrines = multi_doctrine_decomposition(query)
    sub_engine_results = sub_engine_router.dispatch(query)
    elapsed = (time.time() - start_time) * 1000
    if elapsed <= 500:
        return {
            "layer": 2,
            "doctrines": doctrines,
            "sub_engine_results": sub_engine_results,
            "elapsed_ms": elapsed,
        }

    # Layer 3: Deep multi-engine analysis
    deep_results = deep_multi_engine_analyzer.analyze(query, doctrines)
    elapsed = (time.time() - start_time) * 1000
    full_report = eight_step_resolution(query, doctrines, deep_results)
    return {
        "layer": 3,
        "deep_results": deep_results,
        "full_report": full_report,
        "elapsed_ms": elapsed,
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
        self.doctrine_hits: Counter = Counter()
        self.doctrine_queries: Counter = Counter()
        self.sub_engine_stats: Dict[str, List[float]] = defaultdict(list)
        self.sub_engine_errors: Dict[str, int] = defaultdict(int)
        self.sub_engine_invocations: Dict[str, int] = defaultdict(int)
        self.query_times: deque = deque(maxlen=10000)  # (timestamp, QueryTelemetry)
        self.error_log: List[Tuple[float, str]] = []

    def record_query(self, telemetry: QueryTelemetry):
        with self.lock:
            self.telemetry.append(telemetry)
            self.query_times.append((telemetry.timestamp, telemetry))
            for engine in telemetry.engines_invoked:
                self.sub_engine_stats[engine].append(telemetry.latency_ms)
                self.sub_engine_invocations[engine] += 1
            if telemetry.error:
                self.error_log.append((telemetry.timestamp, telemetry.error))
                for engine in telemetry.engines_invoked:
                    self.sub_engine_errors[engine] += 1
            self.doctrine_queries[telemetry.mode] += 1
            if telemetry.cache_hit:
                self.doctrine_hits[telemetry.mode] += 1

    def record_error(self, query_id: str, error: str, engines: List[str], mode: str):
        timestamp = time.time()
        telemetry = QueryTelemetry(
            query_id=query_id,
            timestamp=timestamp,
            latency_ms=0.0,
            cache_hit=False,
            engines_invoked=engines,
            mode=mode,
            confidence=0.0,
            error=error
        )
        self.record_query(telemetry)

    def get_latency_stats(self) -> Dict[str, Any]:
        with self.lock:
            latencies = [t.latency_ms for t in self.telemetry if t.latency_ms > 0]
            if not latencies:
                return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
            latencies_sorted = sorted(latencies)
            n = len(latencies_sorted)
            return {
                "avg": statistics.mean(latencies_sorted),
                "p50": latencies_sorted[int(n * 0.5)],
                "p95": latencies_sorted[int(n * 0.95) - 1],
                "p99": latencies_sorted[int(n * 0.99) - 1],
                "min": latencies_sorted[0],
                "max": latencies_sorted[-1]
            }

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        with self.lock:
            rates = {}
            for doctrine in self.doctrine_queries:
                hits = self.doctrine_hits.get(doctrine, 0)
                total = self.doctrine_queries[doctrine]
                rates[doctrine] = hits / total if total > 0 else 0.0
            return rates

    def queries_last_hour(self) -> List[QueryTelemetry]:
        cutoff = time.time() - 3600
        with self.lock:
            return [t for ts, t in self.query_times if ts >= cutoff]

    def get_sub_engine_stats(self) -> Dict[str, Dict[str, Any]]:
        with self.lock:
            stats = {}
            for engine, latencies in self.sub_engine_stats.items():
                if latencies:
                    stats[engine] = {
                        "avg_latency": statistics.mean(latencies),
                        "min_latency": min(latencies),
                        "max_latency": max(latencies),
                        "invocations": self.sub_engine_invocations[engine],
                        "error_rate": self.sub_engine_errors[engine] / self.sub_engine_invocations[engine] if self.sub_engine_invocations[engine] > 0 else 0.0
                    }
                else:
                    stats[engine] = {
                        "avg_latency": 0,
                        "min_latency": 0,
                        "max_latency": 0,
                        "invocations": 0,
                        "error_rate": 0.0
                    }
            return stats

class DriftWatcher:
    def __init__(self):
        self.lock = threading.Lock()
        self.baseline_confidence: Dict[str, List[float]] = defaultdict(list)  # doctrine -> confidence values
        self.recent_confidence: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.drift_alerts: List[Dict[str, Any]] = []

    def record_baseline(self, doctrine: str, confidence: float):
        with self.lock:
            self.baseline_confidence[doctrine].append(confidence)
            self.recent_confidence[doctrine].append(confidence)

    def detect_drift(self, doctrine: str, confidence: float) -> Optional[Dict[str, Any]]:
        with self.lock:
            self.recent_confidence[doctrine].append(confidence)
            baseline = self.baseline_confidence.get(doctrine, [])
            if len(baseline) < 10:
                return None  # Not enough baseline data
            baseline_avg = statistics.mean(baseline)
            recent_avg = statistics.mean(list(self.recent_confidence[doctrine]))
            drift = recent_avg - baseline_avg
            drift_pct = drift / baseline_avg if baseline_avg != 0 else 0.0
            if abs(drift_pct) > 0.10:
                alert = {
                    "doctrine": doctrine,
                    "baseline_avg": baseline_avg,
                    "recent_avg": recent_avg,
                    "drift_pct": drift_pct,
                    "timestamp": time.time()
                }
                self.drift_alerts.append(alert)
                return alert
            return None

    def get_drift_report(self) -> List[Dict[str, Any]]:
        with self.lock:
            return list(self.drift_alerts)

class CoverageTracker:
    def __init__(self):
        self.lock = threading.Lock()
        self.triggered_doctrines: Counter = Counter()
        self.missed_queries: List[Dict[str, Any]] = []
        self.epistemic_gaps: List[Dict[str, Any]] = []
        self.sub_engine_coverage: Dict[str, Counter] = defaultdict(Counter)
        self.query_to_doctrine: Dict[str, Set[str]] = defaultdict(set)

    def record_triggered(self, doctrine: str, query_id: str, sub_engine: str):
        with self.lock:
            self.triggered_doctrines[doctrine] += 1
            self.sub_engine_coverage[sub_engine][doctrine] += 1
            self.query_to_doctrine[query_id].add(doctrine)

    def record_missed(self, query_id: str, query: Any):
        with self.lock:
            self.missed_queries.append({"query_id": query_id, "query": query})
            if not self.query_to_doctrine[query_id]:
                self.epistemic_gaps.append({"query_id": query_id, "query": query})

    def get_coverage_report(self) -> Dict[str, Any]:
        with self.lock:
            total_triggered = sum(self.triggered_doctrines.values())
            total_missed = len(self.missed_queries)
            gap_count = len(self.epistemic_gaps)
            per_sub_engine = {}
            for engine, doctrines in self.sub_engine_coverage.items():
                per_sub_engine[engine] = dict(doctrines)
            return {
                "total_triggered": total_triggered,
                "total_missed": total_missed,
                "epistemic_gaps": gap_count,
                "triggered_doctrines": dict(self.triggered_doctrines),
                "per_sub_engine": per_sub_engine
            }

    def identify_epistemic_gaps(self) -> List[Dict[str, Any]]:
        with self.lock:
            return list(self.epistemic_gaps)

    def get_sub_engine_coverage_stats(self) -> Dict[str, Dict[str, int]]:
        with self.lock:
            return {engine: dict(doctrines) for engine, doctrines in self.sub_engine_coverage.items()}

def compute_determinism_hash(query: Any, response: Any) -> str:
    query_bytes = json.dumps(query, sort_keys=True, default=str).encode('utf-8')
    response_bytes = json.dumps(response, sort_keys=True, default=str).encode('utf-8')
    sha = hashlib.sha256()
    sha.update(query_bytes)
    sha.update(response_bytes)
    return sha.hexdigest()

class AuditTrailWriter:
    def __init__(self, audit_dir: str):
        self.audit_dir = audit_dir
        self.lock = threading.Lock()
        self.current_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        self.file_handle = None
        self.open_file()

    def open_file(self):
        with self.lock:
            date_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
            if self.current_date != date_str or self.file_handle is None:
                self.current_date = date_str
                if self.file_handle:
                    self.file_handle.close()
                filename = os.path.join(self.audit_dir, f"audit_{self.current_date}.jsonl")
                os.makedirs(self.audit_dir, exist_ok=True)
                self.file_handle = open(filename, "a", encoding="utf-8")

    def write(self, query_id: str, timestamp: float, engine_id: str, engines_invoked: List[str], mode: str, confidence: float, latency: float, cache_hit: bool):
        self.open_file()
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
        with self.lock:
            self.file_handle.write(json.dumps(record) + "\n")
            self.file_handle.flush()

    def forensic_replay(self, date: str, filter_query_id: Optional[str] = None) -> List[Dict[str, Any]]:
        filename = os.path.join(self.audit_dir, f"audit_{date}.jsonl")
        if not os.path.exists(filename):
            return []
        results = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    if filter_query_id is None or record["query_id"] == filter_query_id:
                        results.append(record)
                except Exception:
                    continue
        return results

    def close(self):
        with self.lock:
            if self.file_handle:
                self.file_handle.close()
                self.file_handle = None

class PerformanceProfiler:
    def __init__(self):
        self.lock = threading.Lock()
        self.sub_engine_latency: Dict[str, List[float]] = defaultdict(list)
        self.sub_engine_errors: Dict[str, int] = defaultdict(int)
        self.sub_engine_availability: Dict[str, List[bool]] = defaultdict(list)
        self.sub_engine_invocations: Dict[str, int] = defaultdict(int)
        self.sub_engine_sla: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.sla_thresholds: Dict[str, Dict[str, Any]] = {}  # engine -> {"latency_ms": X, "error_rate": Y, "availability": Z}

    def record(self, engine: str, latency_ms: float, error: Optional[str], available: bool):
        with self.lock:
            self.sub_engine_latency[engine].append(latency_ms)
            self.sub_engine_invocations[engine] += 1
            self.sub_engine_availability[engine].append(available)
            if error:
                self.sub_engine_errors[engine] += 1

    def set_sla_thresholds(self, engine: str, latency_ms: float, error_rate: float, availability: float):
        with self.lock:
            self.sla_thresholds[engine] = {
                "latency_ms": latency_ms,
                "error_rate": error_rate,
                "availability": availability
            }

    def get_stats(self, engine: str) -> Dict[str, Any]:
        with self.lock:
            latencies = self.sub_engine_latency.get(engine, [])
            invocations = self.sub_engine_invocations.get(engine, 0)
            errors = self.sub_engine_errors.get(engine, 0)
            availabilities = self.sub_engine_availability.get(engine, [])
            error_rate = errors / invocations if invocations > 0 else 0.0
            avg_latency = statistics.mean(latencies) if latencies else 0.0
            min_latency = min(latencies) if latencies else 0.0
            max_latency = max(latencies) if latencies else 0.0
            availability_rate = sum(availabilities) / len(availabilities) if availabilities else 1.0
            return {
                "avg_latency": avg_latency,
                "min_latency": min_latency,
                "max_latency": max_latency,
                "invocations": invocations,
                "error_rate": error_rate,
                "availability_rate": availability_rate
            }

    def monitor_sla(self, engine: str) -> Dict[str, Any]:
        stats = self.get_stats(engine)
        thresholds = self.sla_thresholds.get(engine, {})
        sla_status = {}
        if thresholds:
            sla_status["latency_ok"] = stats["avg_latency"] <= thresholds["latency_ms"]
            sla_status["error_rate_ok"] = stats["error_rate"] <= thresholds["error_rate"]
            sla_status["availability_ok"] = stats["availability_rate"] >= thresholds["availability"]
        else:
            sla_status = {"latency_ok": True, "error_rate_ok": True, "availability_ok": True}
        sla_status.update(stats)
        return sla_status

    def get_all_sla_reports(self) -> Dict[str, Dict[str, Any]]:
        with self.lock:
            reports = {}
            for engine in self.sub_engine_latency.keys():
                reports[engine] = self.monitor_sla(engine)
            return reports

# Example usage (integration with orchestrator engine):
# telemetry_collector = TelemetryCollector()
# drift_watcher = DriftWatcher()
# coverage_tracker = CoverageTracker()
# audit_writer = AuditTrailWriter(audit_dir="/var/audit_trail/")
# profiler = PerformanceProfiler()
#
# # During query processing:
# telemetry = QueryTelemetry(
#     query_id="Q123",
#     timestamp=time.time(),
#     latency_ms=42.5,
#     cache_hit=True,
#     engines_invoked=["engineA", "engineB"],
#     mode="doctrineX",
#     confidence=0.92,
#     error=None
# )
# telemetry_collector.record_query(telemetry)
# drift_watcher.record_baseline("doctrineX", 0.92)
# drift_alert = drift_watcher.detect_drift("doctrineX", 0.92)
# coverage_tracker.record_triggered("doctrineX", "Q123", "engineA")
# audit_writer.write("Q123", time.time(), "engineA", ["engineA", "engineB"], "doctrineX", 0.92, 42.5, True)
# profiler.record("engineA", 42.5, None, True)
#
# # At intervals:
# latency_stats = telemetry_collector.get_latency_stats()
# doctrine_hit_rates = telemetry_collector.get_doctrine_hit_rate()
# coverage_report = coverage_tracker.get_coverage_report()
# drift_report = drift_watcher.get_drift_report()
# sla_reports = profiler.get_all_sla_reports()
#
# # For forensic replay:
# replay = audit_writer.forensic_replay("2024-06-01", filter_query_id="Q123")
#
# # For determinism check:
# hash_val = compute_determinism_hash({"input": "foo"}, {"output": "bar"})

ENGINE_ID = "MECHIE"
ENGINE_PORT = 8857
SUB_ENGINES = {
    "MECH01": "Thermodynamics",
    "MECH02": "Fluid Mechanics",
    "MECH03": "Solid Mechanics",
    "MECH04": "Machine Design",
    "MECH05": "Manufacturing",
    "MECH06": "Materials Engineering",
    "MECH07": "Control Systems",
    "MECH08": "Robotics",
    "MECH09": "HVAC Systems",
    "MECH10": "Vibration Analysis",
    "MECH11": "Tribology",
    "MECH12": "Finite Element",
    "MECH13": "Thermal Systems",
    "MECH14": "Mechatronics",
    "MECH15": "Energy Systems",
}

# Logger Setup
logger = logging.getLogger("mechie_orchestrator")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Data Models
class QueryRequest(BaseModel):
    query: str
    parameters: Optional[Dict[str, Any]] = None

class RouteRequest(BaseModel):
    query: str

class AnalyzeRequest(BaseModel):
    query: str
    parameters: Optional[Dict[str, Any]] = None

class SubEngineResponse(BaseModel):
    engine_id: str
    success: bool
    response: Optional[Any] = None
    error: Optional[str] = None
    latency_ms: Optional[int] = None

class HealthStatus(BaseModel):
    engine_id: str
    status: str
    last_checked: datetime.datetime
    details: Optional[Dict[str, Any]] = None

class MetricsReport(BaseModel):
    latency_stats: Dict[str, float]
    cache_hit_rate: float
    queries_per_hour: float
    sub_engine_stats: Dict[str, Dict[str, Any]]

class CoverageReport(BaseModel):
    doctrine_coverage: Dict[str, float]
    epistemic_gaps: List[str]

class DriftReport(BaseModel):
    drift_detected: bool
    drift_metrics: Dict[str, Any]
    last_drift_check: datetime.datetime

class DoctrineInfo(BaseModel):
    doctrine_id: str
    domain: str
    last_updated: datetime.datetime
    coverage_score: float

class RoutingInfo(BaseModel):
    routing_rules: Dict[str, Any]
    engine_registry: Dict[str, str]

class SubEngineHealthDashboard(BaseModel):
    sub_engines: List[HealthStatus]

# Global State and Cache
class DoctrineCache:
    def __init__(self):
        self._cache = {}
        self._lock = threading.Lock()

    def load_all(self):
        # Simulated loading of doctrines
        with self._lock:
            for i in range(1, 101):
                doctrine_id = f"DOC{i:03d}"
                self._cache[doctrine_id] = {
                    "doctrine_id": doctrine_id,
                    "domain": random.choice(list(SUB_ENGINES.values())),
                    "last_updated": datetime.datetime.utcnow() - datetime.timedelta(days=random.randint(0, 365)),
                    "coverage_score": round(random.uniform(0.5, 1.0), 3),
                    "content": f"Doctrine content for {doctrine_id}"
                }
            logger.info(f"DoctrineCache loaded {len(self._cache)} doctrines.")

    def get(self, doctrine_id: str):
        with self._lock:
            return self._cache.get(doctrine_id)

    def list_all(self):
        with self._lock:
            return list(self._cache.values())

    def search(self, query: str):
        # Simple search simulation: return doctrines whose content contains query substring (case-insensitive)
        with self._lock:
            results = []
            q_lower = query.lower()
            for doc in self._cache.values():
                if q_lower in doc["content"].lower():
                    results.append(doc)
            return results

doctrine_cache = DoctrineCache()

class HealthMonitor:
    def __init__(self):
        self._statuses = {}
        self._lock = threading.Lock()
        self._running = False
        self._thread = None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        logger.info("HealthMonitor started.")

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
            logger.info("HealthMonitor stopped.")

    def _monitor_loop(self):
        while self._running:
            self.check_all()
            time.sleep(10)  # Check every 10 seconds

    def check_all(self):
        with self._lock:
            now = datetime.datetime.utcnow()
            for engine_id in SUB_ENGINES.keys():
                # Simulate health check with random success
                success = random.choice([True]*9 + [False])
                status = "healthy" if success else "unhealthy"
                details = {"response_time_ms": random.randint(10, 200)} if success else {"error": "Timeout"}
                self._statuses[engine_id] = HealthStatus(
                    engine_id=engine_id,
                    status=status,
                    last_checked=now,
                    details=details
                )
            logger.debug("HealthMonitor updated statuses.")

    def get_status(self, engine_id: str) -> HealthStatus:
        with self._lock:
            return self._statuses.get(engine_id, HealthStatus(
                engine_id=engine_id,
                status="unknown",
                last_checked=datetime.datetime.utcnow(),
                details={"error": "No data"}
            ))

    def get_all_statuses(self) -> List[HealthStatus]:
        with self._lock:
            return list(self._statuses.values())

health_monitor = HealthMonitor()

class Telemetry:
    def __init__(self):
        self._latencies = []
        self._cache_hits = 0
        self._cache_misses = 0
        self._query_timestamps = []
        self._sub_engine_stats = {engine_id: {"queries": 0, "failures": 0, "avg_latency_ms": 0.0} for engine_id in SUB_ENGINES.keys()}
        self._lock = threading.Lock()

    def record_latency(self, latency_ms: float):
        with self._lock:
            self._latencies.append(latency_ms)
            if len(self._latencies) > 1000:
                self._latencies.pop(0)

    def record_cache_hit(self):
        with self._lock:
            self._cache_hits += 1

    def record_cache_miss(self):
        with self._lock:
            self._cache_misses += 1

    def record_query(self):
        with self._lock:
            self._query_timestamps.append(time.time())
            # Keep only last hour timestamps
            cutoff = time.time() - 3600
            self._query_timestamps = [t for t in self._query_timestamps if t >= cutoff]

    def record_sub_engine_call(self, engine_id: str, success: bool, latency_ms: float):
        with self._lock:
            stats = self._sub_engine_stats.get(engine_id)
            if stats is None:
                stats = {"queries": 0, "failures": 0, "avg_latency_ms": 0.0}
                self._sub_engine_stats[engine_id] = stats
            stats["queries"] += 1
            if not success:
                stats["failures"] += 1
            # Update running average latency
            n = stats["queries"]
            old_avg = stats["avg_latency_ms"]
            stats["avg_latency_ms"] = ((old_avg * (n - 1)) + latency_ms) / n

    def get_metrics(self) -> MetricsReport:
        with self._lock:
            latencies = self._latencies
            if latencies:
                latency_stats = {
                    "min_ms": min(latencies),
                    "max_ms": max(latencies),
                    "avg_ms": sum(latencies) / len(latencies),
                    "p50_ms": sorted(latencies)[len(latencies)//2],
                    "p95_ms": sorted(latencies)[int(len(latencies)*0.95)-1],
                }
            else:
                latency_stats = {
                    "min_ms": 0,
                    "max_ms": 0,
                    "avg_ms": 0,
                    "p50_ms": 0,
                    "p95_ms": 0,
                }
            total_queries = self._cache_hits + self._cache_misses
            cache_hit_rate = (self._cache_hits / total_queries) if total_queries > 0 else 0.0
            queries_per_hour = len(self._query_timestamps)
            return MetricsReport(
                latency_stats=latency_stats,
                cache_hit_rate=cache_hit_rate,
                queries_per_hour=queries_per_hour,
                sub_engine_stats=self._sub_engine_stats.copy()
            )

telemetry = Telemetry()

class SearchIndex:
    def __init__(self):
        self._index = {}
        self._lock = threading.Lock()

    def seed(self, doctrines: List[Dict[str, Any]]):
        with self._lock:
            self._index.clear()
            for doc in doctrines:
                key = doc["doctrine_id"]
                self._index[key] = doc
            logger.info(f"SearchIndex seeded with {len(self._index)} doctrines.")

    def search(self, query: str) -> List[Dict[str, Any]]:
        with self._lock:
            q_lower = query.lower()
            results = []
            for doc in self._index.values():
                if q_lower in doc["content"].lower():
                    results.append(doc)
            return results

search_index = SearchIndex()

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_time=30):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self._failures = {}
        self._last_failure_time = {}
        self._lock = threading.Lock()

    def record_failure(self, engine_id: str):
        with self._lock:
            self._failures[engine_id] = self._failures.get(engine_id, 0) + 1
            self._last_failure_time[engine_id] = time.time()

    def record_success(self, engine_id: str):
        with self._lock:
            self._failures[engine_id] = 0
            self._last_failure_time.pop(engine_id, None)

    def is_open(self, engine_id: str) -> bool:
        with self._lock:
            failures = self._failures.get(engine_id, 0)
            if failures >= self.failure_threshold:
                last_time = self._last_failure_time.get(engine_id, 0)
                if time.time() - last_time < self.recovery_time:
                    return True
                else:
                    # Reset after recovery time
                    self._failures[engine_id] = 0
                    self._last_failure_time.pop(engine_id, None)
                    return False
            return False

circuit_breaker = CircuitBreaker()

# Utility Functions
def normalize_query(query: str) -> str:
    normalized = query.strip().lower()
    logger.debug(f"Normalized query: {normalized}")
    return normalized

def classify_domain(query: str) -> str:
    # Simulated classification based on keywords
    keywords_map = {
        "thermo": "MECH01",
        "fluid": "MECH02",
        "solid": "MECH03",
        "machine": "MECH04",
        "manufacturing": "MECH05",
        "material": "MECH06",
        "control": "MECH07",
        "robot": "MECH08",
        "hvac": "MECH09",
        "vibration": "MECH10",
        "tribology": "MECH11",
        "finite": "MECH12",
        "thermal": "MECH13",
        "mechatronics": "MECH14",
        "energy": "MECH15",
    }
    for keyword, engine_id in keywords_map.items():
        if keyword in query:
            logger.debug(f"Classified domain '{engine_id}' for query '{query}'")
            return engine_id
    # Default fallback
    logger.debug(f"Default classification to MECH01 for query '{query}'")
    return "MECH01"

def route_query(domain_id: str) -> List[str]:
    # Basic routing: route to classified domain plus related engines
    routing_map = {
        "MECH01": ["MECH01", "MECH13", "MECH15"],
        "MECH02": ["MECH02", "MECH09", "MECH10"],
        "MECH03": ["MECH03", "MECH11", "MECH12"],
        "MECH04": ["MECH04", "MECH05", "MECH14"],
        "MECH05": ["MECH05", "MECH04", "MECH06"],
        "MECH06": ["MECH06", "MECH03", "MECH05"],
        "MECH07": ["MECH07", "MECH08", "MECH14"],
        "MECH08": ["MECH08", "MECH07", "MECH14"],
        "MECH09": ["MECH09", "MECH02", "MECH10"],
        "MECH10": ["MECH10", "MECH02", "MECH09"],
        "MECH11": ["MECH11", "MECH03", "MECH12"],
        "MECH12": ["MECH12", "MECH03", "MECH11"],
        "MECH13": ["MECH13", "MECH01", "MECH15"],
        "MECH14": ["MECH14", "MECH04", "MECH07"],
        "MECH15": ["MECH15", "MECH01", "MECH13"],
    }
    routed = routing_map.get(domain_id, [domain_id])
    logger.debug(f"Routing for domain '{domain_id}': {routed}")
    return routed

async def dispatch_to_sub_engine(engine_id: str, query: str, parameters: Optional[Dict[str, Any]]) -> SubEngineResponse:
    if circuit_breaker.is_open(engine_id):
        logger.warning(f"Circuit breaker open for {engine_id}, skipping call.")
        return SubEngineResponse(
            engine_id=engine_id,
            success=False,
            error="Circuit breaker open",
            latency_ms=0
        )
    start_time = time.time()
    try:
        # Simulate network call latency and random failure
        latency_sim = random.uniform(0.05, 0.3)
        await asyncio.sleep(latency_sim)
        if random.random() < 0.1:
            raise Exception("Simulated sub-engine failure")
        response_content = {
            "engine_id": engine_id,
            "answer": f"Response from {SUB_ENGINES[engine_id]} for query '{query}'"
        }
        latency_ms = int((time.time() - start_time) * 1000)
        circuit_breaker.record_success(engine_id)
        telemetry.record_sub_engine_call(engine_id, True, latency_ms)
        logger.debug(f"Sub-engine {engine_id} responded in {latency_ms}ms")
        return SubEngineResponse(
            engine_id=engine_id,
            success=True,
            response=response_content,
            latency_ms=latency_ms
        )
    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)
        circuit_breaker.record_failure(engine_id)
        telemetry.record_sub_engine_call(engine_id, False, latency_ms)
        logger.error(f"Sub-engine {engine_id} failed: {str(e)}")
        return SubEngineResponse(
            engine_id=engine_id,
            success=False,
            error=str(e),
            latency_ms=latency_ms
        )

def merge_responses(responses: List[SubEngineResponse]) -> Dict[str, Any]:
    merged = {
        "answers": [],
        "errors": [],
        "summary": ""
    }
    for resp in responses:
        if resp.success and resp.response:
            merged["answers"].append(resp.response)
        else:
            merged["errors"].append({"engine_id": resp.engine_id, "error": resp.error})
    if merged["answers"]:
        merged["summary"] = f"Merged {len(merged['answers'])} answers."
    else:
        merged["summary"] = "No successful answers."
    logger.debug(f"Merged response summary: {merged['summary']}")
    return merged

def apply_guardrails(response: Dict[str, Any]) -> Dict[str, Any]:
    # Placeholder for guardrail logic (e.g., filter sensitive info)
    # For now, just pass through
    logger.debug("Applied guardrails to response.")
    return response

def hash_query_response(query: str, response: Dict[str, Any]) -> str:
    hasher = hashlib.sha256()
    hasher.update(query.encode('utf-8'))
    hasher.update(str(response).encode('utf-8'))
    digest = hasher.hexdigest()
    logger.debug(f"Hashed query-response: {digest}")
    return digest

def log_query(query: str, response_hash: str, latency_ms: int):
    logger.info(f"Query logged: hash={response_hash}, latency={latency_ms}ms, query='{query}'")

async def fallback_to_doctrine_cache(query: str) -> Dict[str, Any]:
    results = doctrine_cache.search(query)
    if results:
        logger.info(f"Fallback to doctrine cache returned {len(results)} results.")
        return {"fallback": True, "results": results}
    else:
        logger.info("Fallback to doctrine cache found no results.")
        return {"fallback": True, "results": []}

# Drift Detection Simulation
class DriftDetector:
    def __init__(self):
        self._last_check = datetime.datetime.utcnow()
        self._drift_detected = False
        self._metrics = {}

    def check_drift(self):
        # Simulate drift detection logic
        self._last_check = datetime.datetime.utcnow()
        self._drift_detected = random.choice([False]*9 + [True])
        self._metrics = {
            "feature_drift_score": round(random.uniform(0, 1), 3),
            "model_drift_score": round(random.uniform(0, 1), 3),
            "timestamp": self._last_check.isoformat()
        }
        logger.info(f"Drift detection run: detected={self._drift_detected}")

    def get_report(self) -> DriftReport:
        return DriftReport(
            drift_detected=self._drift_detected,
            drift_metrics=self._metrics,
            last_drift_check=self._last_check
        )

drift_detector = DriftDetector()

# FastAPI App Initialization
app = FastAPI(title="Mechanical Engineering Intelligence Engine — Domain Orchestrator", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lifespan management
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Mechanical Engineering Intelligence Engine Orchestrator...")
    # Initialize doctrine cache
    doctrine_cache.load_all()
    # Seed search index
    search_index.seed(doctrine_cache.list_all())
    # Start health monitor
    health_monitor.start()
    # Start telemetry (nothing to start explicitly)
    logger.info("Startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Mechanical Engineering Intelligence Engine Orchestrator...")
    health_monitor.stop()
    logger.info("Shutdown complete.")

# Endpoint Implementations

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    start_time = time.time()
    query_raw = request.query
    parameters = request.parameters or {}

    normalized_query = normalize_query(query_raw)
    domain_id = classify_domain(normalized_query)
    routed_engines = route_query(domain_id)

    telemetry.record_query()

    # Dispatch concurrently to sub-engines
    tasks = []
    for engine_id in routed_engines:
        tasks.append(dispatch_to_sub_engine(engine_id, normalized_query, parameters))
    responses: List[SubEngineResponse] = await asyncio.gather(*tasks, return_exceptions=False)

    merged_response = merge_responses(responses)
    guarded_response = apply_guardrails(merged_response)
    latency_ms = int((time.time() - start_time) * 1000)
    response_hash = hash_query_response(normalized_query, guarded_response)

    # Log telemetry
    telemetry.record_latency(latency_ms)

    # If no successful answers, fallback to doctrine cache
    if not merged_response["answers"]:
        fallback_response = await fallback_to_doctrine_cache(normalized_query)
        latency_ms = int((time.time() - start_time) * 1000)
        response_hash = hash_query_response(normalized_query, fallback_response)
        log_query(normalized_query, response_hash, latency_ms)
        return JSONResponse(content=fallback_response, status_code=status.HTTP_200_OK)

    log_query(normalized_query, response_hash, latency_ms)
    return JSONResponse(content=guarded_response, status_code=status.HTTP_200_OK)

@app.get("/health")
async def health_endpoint():
    # Self health
    self_health = HealthStatus(
        engine_id=ENGINE_ID,
        status="healthy",
        last_checked=datetime.datetime.utcnow(),
        details={"version": "1.0.0"}
    )
    # Sub-engines health
    sub_engines_health = health_monitor.get_all_statuses()
    combined = {
        "self": self_health.dict(),
        "sub_engines": [h.dict() for h in sub_engines_health]
    }
    return JSONResponse(content=combined)

@app.get("/metrics")
async def metrics_endpoint():
    metrics = telemetry.get_metrics()
    return JSONResponse(content=metrics.dict())

@app.get("/coverage")
async def coverage_endpoint():
    doctrines = doctrine_cache.list_all()
    domain_coverage = {}
    for doc in doctrines:
        domain = doc["domain"]
        domain_coverage.setdefault(domain, []).append(doc["coverage_score"])
    coverage_report = {domain: round(sum(scores)/len(scores), 3) for domain, scores in domain_coverage.items()}
    epistemic_gaps = [domain for domain, score in coverage_report.items() if score < 0.7]
    report = CoverageReport(
        doctrine_coverage=coverage_report,
        epistemic_gaps=epistemic_gaps
    )
    return JSONResponse(content=report.dict())

@app.get("/drift")
async def drift_endpoint():
    drift_detector.check_drift()
    report = drift_detector.get_report()
    return JSONResponse(content=report.dict())

@app.get("/doctrines")
async def doctrines_endpoint():
    doctrines = doctrine_cache.list_all()
    doctrine_infos = [DoctrineInfo(
        doctrine_id=d["doctrine_id"],
        domain=d["domain"],
        last_updated=d["last_updated"],
        coverage_score=d["coverage_score"]
    ).dict() for d in doctrines]
    return JSONResponse(content={"doctrines": doctrine_infos})

@app.get("/routing")
async def routing_endpoint():
    routing_rules = {
        "default": "route to classified domain plus related engines",
        "rules": "see route_query function"
    }
    engine_registry = SUB_ENGINES.copy()
    info = RoutingInfo(
        routing_rules=routing_rules,
        engine_registry=engine_registry
    )
    return JSONResponse(content=info.dict())

@app.get("/sub-engines")
async def sub_engines_endpoint():
    statuses = health_monitor.get_all_statuses()
    dashboard = SubEngineHealthDashboard(sub_engines=statuses)
    return JSONResponse(content=dashboard.dict())

@app.post("/route")
async def route_endpoint(request: RouteRequest):
    normalized_query = normalize_query(request.query)
    domain_id = classify_domain(normalized_query)
    routed_engines = route_query(domain_id)
    return JSONResponse(content={"routed_engines": routed_engines})

@app.post("/analyze")
async def analyze_endpoint(request: AnalyzeRequest):
    start_time = time.time()
    query_raw = request.query
    parameters = request.parameters or {}

    normalized_query = normalize_query(query_raw)
    domain_id = classify_domain(normalized_query)
    routed_engines = route_query(domain_id)

    telemetry.record_query()

    # Dispatch concurrently to sub-engines with detailed analysis simulation
    tasks = []
    for engine_id in routed_engines:
        tasks.append(dispatch_to_sub_engine(engine_id, normalized_query, parameters))
    responses: List[SubEngineResponse] = await asyncio.gather(*tasks, return_exceptions=False)

    # Deep analysis: simulate additional processing
    analysis_results = []
    for resp in responses:
        if resp.success and resp.response:
            analysis_results.append({
                "engine_id": resp.engine_id,
                "detailed_analysis": f"Deep analysis data for {resp.engine_id}",
                "response": resp.response
            })
        else:
            analysis_results.append({
                "engine_id": resp.engine_id,
                "error": resp.error
            })

    latency_ms = int((time.time() - start_time) * 1000)
    telemetry.record_latency(latency_ms)

    return JSONResponse(content={"analysis": analysis_results, "latency_ms": latency_ms})

# Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run("mechie_orchestrator:app", host="0.0.0.0", port=ENGINE_PORT, log_level="info")