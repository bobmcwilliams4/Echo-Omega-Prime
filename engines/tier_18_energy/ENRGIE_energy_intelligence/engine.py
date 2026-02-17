import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import uuid
import json
import time
import statistics
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict, deque

from fastapi import FastAPI
from pydantic import BaseModel, Field

from loguru import logger

# Engine Constants
ENGINE_ID = "ENRGIE"
ENGINE_PORT = 8855
ENGINE_NAME = "Energy Intelligence Engine — Domain Orchestrator"
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
    NUCLEAR_SAFETY = "NUCLEAR_SAFETY"
    RENEWABLE_INTEGRATION = "RENEWABLE_INTEGRATION"
    GRID_STABILITY = "GRID_STABILITY"
    STORAGE_OPTIMIZATION = "STORAGE_OPTIMIZATION"
    HYDROELECTRIC_PERFORMANCE = "HYDROELECTRIC_PERFORMANCE"
    SOLAR_EFFICIENCY = "SOLAR_EFFICIENCY"
    WIND_RESOURCE_ASSESSMENT = "WIND_RESOURCE_ASSESSMENT"
    GEOTHERMAL_UTILIZATION = "GEOTHERMAL_UTILIZATION"
    HYDROGEN_PRODUCTION = "HYDROGEN_PRODUCTION"
    NATURAL_GAS_EMISSIONS = "NATURAL_GAS_EMISSIONS"
    COAL_RETROFIT = "COAL_RETROFIT"
    BIOENERGY_LOGISTICS = "BIOENERGY_LOGISTICS"
    OCEAN_ENERGY_HARVEST = "OCEAN_ENERGY_HARVEST"
    ENERGY_EFFICIENCY = "ENERGY_EFFICIENCY"
    SMART_GRID_CYBERSECURITY = "SMART_GRID_CYBERSECURITY"
    DEMAND_RESPONSE = "DEMAND_RESPONSE"
    POWER_MARKET_ANALYSIS = "POWER_MARKET_ANALYSIS"
    CARBON_CAPTURE = "CARBON_CAPTURE"
    POLICY_COMPLIANCE = "POLICY_COMPLIANCE"
    EMERGENCY_RESPONSE = "EMERGENCY_RESPONSE"
    SYSTEM_RESILIENCE = "SYSTEM_RESILIENCE"
    DISTRIBUTED_GENERATION = "DISTRIBUTED_GENERATION"
    TRANSMISSION_PLANNING = "TRANSMISSION_PLANNING"
    LOAD_FORECASTING = "LOAD_FORECASTING"
    ASSET_MANAGEMENT = "ASSET_MANAGEMENT"
    OUTAGE_ANALYSIS = "OUTAGE_ANALYSIS"
    ENERGY_TRADING = "ENERGY_TRADING"
    REGULATORY_REPORTING = "REGULATORY_REPORTING"
    DATA_INTEGRITY = "DATA_INTEGRITY"
    OTHER = "OTHER"

class SubEngineStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

# Pydantic Models
class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str]
    query_text: str
    response_mode: ResponseMode = ResponseMode.FAST
    position_zone: PositionZone = PositionZone.PLANNING
    confidence_zone: ConfidenceZone = ConfidenceZone.DEFENSIBLE
    issue_category: IssueCategory = IssueCategory.OTHER
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query_id: str
    orchestrator_id: str
    result: Any
    routed_engine_id: str
    routed_engine_name: str
    confidence: float
    status: str
    latency_ms: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    trace: Optional[List[str]] = None
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
    selected_engine_name: str
    rule_applied: str
    confidence: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decision: RoutingDecision
    subengine_response: Optional[QueryResponse]
    orchestrator_latency_ms: float
    error: Optional[str] = None
    trace: Optional[List[str]] = None

# Sub-Engine Registry
SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "ENRG01": SubEngineConfig(
        engine_id="ENRG01",
        name="Nuclear Engineering",
        port=8861,
        health_url="http://localhost:8861/health",
        capabilities=["nuclear_safety", "reactor_design", "fuel_cycle", "waste_management"],
        weight=1.0,
        domains=["nuclear", "reactor", "uranium", "fission", "fusion", "nuclear_safety"]
    ),
    "ENRG02": SubEngineConfig(
        engine_id="ENRG02",
        name="Solar Energy",
        port=8862,
        health_url="http://localhost:8862/health",
        capabilities=["solar_efficiency", "photovoltaics", "solar_thermal", "concentrated_solar"],
        weight=1.0,
        domains=["solar", "photovoltaic", "pv", "solar_thermal", "solar_farm", "solar_efficiency"]
    ),
    "ENRG03": SubEngineConfig(
        engine_id="ENRG03",
        name="Wind Power",
        port=8863,
        health_url="http://localhost:8863/health",
        capabilities=["wind_resource", "turbine_design", "offshore_wind", "wind_forecasting"],
        weight=1.0,
        domains=["wind", "turbine", "offshore_wind", "wind_farm", "wind_resource"]
    ),
    "ENRG04": SubEngineConfig(
        engine_id="ENRG04",
        name="Hydroelectric",
        port=8864,
        health_url="http://localhost:8864/health",
        capabilities=["hydroelectric_performance", "dam_safety", "run_of_river", "pumped_storage"],
        weight=1.0,
        domains=["hydro", "hydroelectric", "dam", "run_of_river", "pumped_storage"]
    ),
    "ENRG05": SubEngineConfig(
        engine_id="ENRG05",
        name="Grid Operations",
        port=8865,
        health_url="http://localhost:8865/health",
        capabilities=["grid_stability", "transmission", "distribution", "outage_analysis"],
        weight=1.0,
        domains=["grid", "transmission", "distribution", "outage", "grid_stability"]
    ),
    "ENRG06": SubEngineConfig(
        engine_id="ENRG06",
        name="Energy Storage",
        port=8866,
        health_url="http://localhost:8866/health",
        capabilities=["storage_optimization", "batteries", "pumped_hydro", "thermal_storage"],
        weight=1.0,
        domains=["storage", "battery", "batteries", "thermal_storage", "energy_storage"]
    ),
    "ENRG07": SubEngineConfig(
        engine_id="ENRG07",
        name="Geothermal",
        port=8867,
        health_url="http://localhost:8867/health",
        capabilities=["geothermal_utilization", "enhanced_geothermal", "heat_pumps"],
        weight=1.0,
        domains=["geothermal", "heat_pump", "enhanced_geothermal"]
    ),
    "ENRG08": SubEngineConfig(
        engine_id="ENRG08",
        name="Hydrogen Economy",
        port=8868,
        health_url="http://localhost:8868/health",
        capabilities=["hydrogen_production", "fuel_cells", "power_to_gas"],
        weight=1.0,
        domains=["hydrogen", "fuel_cell", "power_to_gas", "hydrogen_production"]
    ),
    "ENRG09": SubEngineConfig(
        engine_id="ENRG09",
        name="Natural Gas Systems",
        port=8869,
        health_url="http://localhost:8869/health",
        capabilities=["natural_gas_emissions", "pipeline_integrity", "gas_turbines"],
        weight=1.0,
        domains=["natural_gas", "pipeline", "gas_turbine", "lng", "cng"]
    ),
    "ENRG10": SubEngineConfig(
        engine_id="ENRG10",
        name="Coal Technology",
        port=8870,
        health_url="http://localhost:8870/health",
        capabilities=["coal_retrofit", "carbon_capture", "coal_fired_power"],
        weight=1.0,
        domains=["coal", "carbon_capture", "coal_fired", "coal_retrofit"]
    ),
    "ENRG11": SubEngineConfig(
        engine_id="ENRG11",
        name="Bioenergy",
        port=8871,
        health_url="http://localhost:8871/health",
        capabilities=["bioenergy_logistics", "biomass", "biofuels", "anaerobic_digestion"],
        weight=1.0,
        domains=["bioenergy", "biomass", "biofuel", "anaerobic_digestion"]
    ),
    "ENRG12": SubEngineConfig(
        engine_id="ENRG12",
        name="Ocean Energy",
        port=8872,
        health_url="http://localhost:8872/health",
        capabilities=["ocean_energy_harvest", "tidal", "wave_power"],
        weight=1.0,
        domains=["ocean_energy", "tidal", "wave_power", "marine_energy"]
    ),
    "ENRG13": SubEngineConfig(
        engine_id="ENRG13",
        name="Energy Efficiency",
        port=8873,
        health_url="http://localhost:8873/health",
        capabilities=["energy_efficiency", "demand_response", "building_performance"],
        weight=1.0,
        domains=["efficiency", "energy_efficiency", "demand_response", "building_performance"]
    ),
    "ENRG14": SubEngineConfig(
        engine_id="ENRG14",
        name="Smart Grid",
        port=8874,
        health_url="http://localhost:8874/health",
        capabilities=["smart_grid_cybersecurity", "distributed_generation", "microgrid"],
        weight=1.0,
        domains=["smart_grid", "microgrid", "distributed_generation", "cybersecurity"]
    ),
}

# Routing Rules (domain keyword -> engine_id)
ROUTING_RULES: Dict[str, str] = {
    # Nuclear
    "nuclear": "ENRG01",
    "reactor": "ENRG01",
    "uranium": "ENRG01",
    "fission": "ENRG01",
    "fusion": "ENRG01",
    "fuel_cycle": "ENRG01",
    "waste_management": "ENRG01",
    "nuclear_safety": "ENRG01",
    "isotope": "ENRG01",
    "reactor_design": "ENRG01",
    # Solar
    "solar": "ENRG02",
    "photovoltaic": "ENRG02",
    "pv": "ENRG02",
    "solar_thermal": "ENRG02",
    "solar_farm": "ENRG02",
    "solar_panel": "ENRG02",
    "solar_efficiency": "ENRG02",
    "concentrated_solar": "ENRG02",
    "inverter": "ENRG02",
    # Wind
    "wind": "ENRG03",
    "turbine": "ENRG03",
    "offshore_wind": "ENRG03",
    "wind_farm": "ENRG03",
    "wind_resource": "ENRG03",
    "wind_forecasting": "ENRG03",
    "wind_turbine": "ENRG03",
    "turbine_blade": "ENRG03",
    # Hydro
    "hydro": "ENRG04",
    "hydroelectric": "ENRG04",
    "dam": "ENRG04",
    "run_of_river": "ENRG04",
    "pumped_storage": "ENRG04",
    "hydropower": "ENRG04",
    "reservoir": "ENRG04",
    "dam_safety": "ENRG04",
    # Grid Operations
    "grid": "ENRG05",
    "transmission": "ENRG05",
    "distribution": "ENRG05",
    "outage": "ENRG05",
    "grid_stability": "ENRG05",
    "frequency_control": "ENRG05",
    "voltage_regulation": "ENRG05",
    "ancillary_services": "ENRG05",
    "blackout": "ENRG05",
    # Storage
    "storage": "ENRG06",
    "battery": "ENRG06",
    "batteries": "ENRG06",
    "thermal_storage": "ENRG06",
    "energy_storage": "ENRG06",
    "pumped_hydro": "ENRG06",
    "flywheel": "ENRG06",
    "supercapacitor": "ENRG06",
    "storage_optimization": "ENRG06",
    # Geothermal
    "geothermal": "ENRG07",
    "heat_pump": "ENRG07",
    "enhanced_geothermal": "ENRG07",
    "geothermal_plant": "ENRG07",
    "geothermal_utilization": "ENRG07",
    # Hydrogen
    "hydrogen": "ENRG08",
    "fuel_cell": "ENRG08",
    "power_to_gas": "ENRG08",
    "hydrogen_production": "ENRG08",
    "electrolyzer": "ENRG08",
    "hydrogen_storage": "ENRG08",
    # Natural Gas
    "natural_gas": "ENRG09",
    "pipeline": "ENRG09",
    "gas_turbine": "ENRG09",
    "lng": "ENRG09",
    "cng": "ENRG09",
    "methane": "ENRG09",
    "gas_storage": "ENRG09",
    "pipeline_integrity": "ENRG09",
    # Coal
    "coal": "ENRG10",
    "carbon_capture": "ENRG10",
    "coal_fired": "ENRG10",
    "coal_retrofit": "ENRG10",
    "coal_plant": "ENRG10",
    "ash_handling": "ENRG10",
    # Bioenergy
    "bioenergy": "ENRG11",
    "biomass": "ENRG11",
    "biofuel": "ENRG11",
    "anaerobic_digestion": "ENRG11",
    "biogas": "ENRG11",
    "biochar": "ENRG11",
    "bioenergy_logistics": "ENRG11",
    # Ocean
    "ocean_energy": "ENRG12",
    "tidal": "ENRG12",
    "wave_power": "ENRG12",
    "marine_energy": "ENRG12",
    "tidal_turbine": "ENRG12",
    "ocean_current": "ENRG12",
    "salinity_gradient": "ENRG12",
    # Efficiency
    "efficiency": "ENRG13",
    "energy_efficiency": "ENRG13",
    "demand_response": "ENRG13",
    "building_performance": "ENRG13",
    "energy_audit": "ENRG13",
    "retrofit": "ENRG13",
    "load_management": "ENRG13",
    # Smart Grid
    "smart_grid": "ENRG14",
    "microgrid": "ENRG14",
    "distributed_generation": "ENRG14",
    "cybersecurity": "ENRG14",
    "smart_meter": "ENRG14",
    "virtual_power_plant": "ENRG14",
    "peer_to_peer": "ENRG14",
    # Cross-cutting/Other
    "policy": "ENRG05",
    "regulatory": "ENRG05",
    "market": "ENRG05",
    "trading": "ENRG05",
    "asset_management": "ENRG05",
    "outage_analysis": "ENRG05",
    "system_resilience": "ENRG05",
    "emergency_response": "ENRG05",
    "data_integrity": "ENRG05",
    "reporting": "ENRG05",
    "compliance": "ENRG05",
    "forecasting": "ENRG05",
    "load_forecasting": "ENRG05",
    "transmission_planning": "ENRG05",
    "demand_forecasting": "ENRG05",
    "ancillary_service": "ENRG05",
    "resilience": "ENRG05",
    "outage_management": "ENRG05",
    "system_planning": "ENRG05",
    "asset_health": "ENRG05",
    # Add 100+ more rules for coverage
    "hvac": "ENRG13",
    "lighting": "ENRG13",
    "insulation": "ENRG13",
    "building_code": "ENRG13",
    "weatherization": "ENRG13",
    "retrocommissioning": "ENRG13",
    "energy_star": "ENRG13",
    "leed": "ENRG13",
    "energy_management": "ENRG13",
    "energy_savings": "ENRG13",
    "thermal_comfort": "ENRG13",
    "occupancy_sensor": "ENRG13",
    "variable_frequency_drive": "ENRG13",
    "vfd": "ENRG13",
    "chiller": "ENRG13",
    "boiler": "ENRG13",
    "heat_exchanger": "ENRG13",
    "cooling_tower": "ENRG13",
    "building_automation": "ENRG13",
    "bms": "ENRG13",
    "ems": "ENRG13",
    "energy_monitoring": "ENRG13",
    "demand_metering": "ENRG13",
    "load_shedding": "ENRG13",
    "peak_shaving": "ENRG13",
    "time_of_use": "ENRG13",
    "tou": "ENRG13",
    "demand_charge": "ENRG13",
    "power_factor": "ENRG13",
    "harmonics": "ENRG13",
    "power_quality": "ENRG13",
    "submetering": "ENRG13",
    "interval_data": "ENRG13",
    "energy_dashboard": "ENRG13",
    "energy_baseline": "ENRG13",
    "measurement_verification": "ENRG13",
    "m_and_v": "ENRG13",
    "renewable_integration": "ENRG05",
    "interconnection": "ENRG05",
    "curtailment": "ENRG05",
    "grid_code": "ENRG05",
    "grid_modernization": "ENRG05",
    "synchrophasor": "ENRG05",
    "phasor_measurement": "ENRG05",
    "pmu": "ENRG05",
    "scada": "ENRG05",
    "ems_system": "ENRG05",
    "dms": "ENRG05",
    "oms": "ENRG05",
    "control_center": "ENRG05",
    "situational_awareness": "ENRG05",
    "contingency_analysis": "ENRG05",
    "state_estimation": "ENRG05",
    "load_flow": "ENRG05",
    "power_flow": "ENRG05",
    "short_circuit": "ENRG05",
    "relay": "ENRG05",
    "protection": "ENRG05",
    "breaker": "ENRG05",
    "switchgear": "ENRG05",
    "busbar": "ENRG05",
    "transformer": "ENRG05",
    "substation": "ENRG05",
    "line_rating": "ENRG05",
    "thermal_rating": "ENRG05",
    "dynamic_rating": "ENRG05",
    "weather_impact": "ENRG05",
    "lightning": "ENRG05",
    "vegetation_management": "ENRG05",
    "right_of_way": "ENRG05",
    "permitting": "ENRG05",
    "stakeholder": "ENRG05",
    "public_outreach": "ENRG05",
    "community_engagement": "ENRG05",
    "environmental_impact": "ENRG05",
    "eia": "ENRG05",
    "ferc": "ENRG05",
    "nerc": "ENRG05",
    "iso": "ENRG05",
    "rto": "ENRG05",
    "balancing_authority": "ENRG05",
    "intertie": "ENRG05",
    "tie_line": "ENRG05",
    "import_export": "ENRG05",
    "cross_border": "ENRG05",
    "interchange": "ENRG05",
    "reserve_margin": "ENRG05",
    "capacity_market": "ENRG05",
    "energy_market": "ENRG05",
    "ancillary_market": "ENRG05",
    "locational_marginal_price": "ENRG05",
    "lmp": "ENRG05",
    "nodal_pricing": "ENRG05",
    "congestion": "ENRG05",
    "transmission_constraint": "ENRG05",
    "zonal_pricing": "ENRG05",
    "demand_bid": "ENRG05",
    "supply_bid": "ENRG05",
    "market_clearing": "ENRG05",
    "settlement": "ENRG05",
    "hedge": "ENRG05",
    "financial_transmission_right": "ENRG05",
    "ftr": "ENRG05",
    "crr": "ENRG05",
    "auction": "ENRG05",
    "bilateral_contract": "ENRG05",
    "ppa": "ENRG05",
    "power_purchase_agreement": "ENRG05",
    "renewable_portfolio_standard": "ENRG05",
    "rps": "ENRG05",
    "clean_energy_standard": "ENRG05",
    "ces": "ENRG05",
    "carbon_policy": "ENRG05",
    "cap_and_trade": "ENRG05",
    "emissions_trading": "ENRG05",
    "offset": "ENRG05",
    "credit": "ENRG05",
    "certificate": "ENRG05",
    "green_tag": "ENRG05",
    "rec": "ENRG05",
    "renewable_energy_certificate": "ENRG05",
    "guarantee_of_origin": "ENRG05",
    "go": "ENRG05",
    "disclosure": "ENRG05",
    "audit": "ENRG05",
    "verification": "ENRG05",
    "compliance_report": "ENRG05",
    "regulatory_report": "ENRG05",
    "policy_compliance": "ENRG05",
    "emergency": "ENRG05",
    "response": "ENRG05",
    "contingency": "ENRG05",
    "black_start": "ENRG05",
    "restoration": "ENRG05",
    "islanding": "ENRG14",
    "self_healing": "ENRG14",
    "demand_side": "ENRG13",
    "prosumer": "ENRG14",
    "blockchain": "ENRG14",
    "transactive_energy": "ENRG14",
    "iot": "ENRG14",
    "edge_computing": "ENRG14",
    "big_data": "ENRG14",
    "data_analytics": "ENRG14",
    "machine_learning": "ENRG14",
    "ai": "ENRG14",
    "predictive_maintenance": "ENRG14",
    "asset_analytics": "ENRG14",
    "cyber_attack": "ENRG14",
    "intrusion_detection": "ENRG14",
    "security": "ENRG14",
    "vulnerability": "ENRG14",
    "penetration_test": "ENRG14",
    "incident_response": "ENRG14",
    "risk_assessment": "ENRG14",
    "compliance_audit": "ENRG14",
    "microgrid_controller": "ENRG14",
    "islanding_detection": "ENRG14",
    "peer_to_peer_trading": "ENRG14",
    "virtual_power_plant": "ENRG14",
    # Fallback
    "other": "ENRG05",
}

# Metrics Collector
class MetricsCollector:
    def __init__(self):
        self.query_log = deque(maxlen=10000)
        self.error_log = deque(maxlen=1000)
        self.latency_log = deque(maxlen=10000)
        self.query_times = deque(maxlen=10000)
        self.query_count_by_hour = defaultdict(int)
        self.lock = asyncio.Lock()

    async def record_query(self, query_id: str, latency_ms: float):
        now = datetime.utcnow()
        async with self.lock:
            self.query_log.append((query_id, now, latency_ms))
            self.latency_log.append(latency_ms)
            self.query_times.append(now)
            hour_key = now.replace(minute=0, second=0, microsecond=0)
            self.query_count_by_hour[hour_key] += 1

    async def record_error(self, query_id: str, error: str):
        now = datetime.utcnow()
        async with self.lock:
            self.error_log.append((query_id, now, error))

    async def get_latency_stats(self) -> Dict[str, float]:
        async with self.lock:
            if not self.latency_log:
                return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "max": 0.0, "min": 0.0}
            latencies = list(self.latency_log)
            return {
                "avg": statistics.mean(latencies),
                "p50": statistics.median(latencies),
                "p95": statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 20 else max(latencies),
                "max": max(latencies),
                "min": min(latencies),
            }

    async def queries_last_hour(self) -> int:
        now = datetime.utcnow()
        one_hour_ago = now - timedelta(hours=1)
        async with self.lock:
            return sum(1 for t in self.query_times if t >= one_hour_ago)

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
        topic="Nuclear Fission Reactor Safety - Pressurized Water Reactor (PWR)",
        keywords=["nuclear", "PWR", "reactor safety", "fission", "coolant", "containment", "emergency core cooling", "regulation"],
        conclusion_template=(
            "The safety of Pressurized Water Reactors (PWR) hinges on robust coolant system integrity, "
            "containment structures, and emergency core cooling systems. Compliance with NRC regulations "
            "and adherence to deterministic and probabilistic safety analyses ensure operational safety. "
            "Continuous monitoring and rigorous maintenance reduce risk of core damage and radiological release."
        ),
        reasoning_framework=(
            "Pressurized Water Reactors (PWR) operate by maintaining water under high pressure to prevent boiling, "
            "thus acting as both coolant and neutron moderator. The primary safety concern is maintaining coolant "
            "flow to avoid overheating and potential core meltdown. The reactor vessel and associated piping must "
            "withstand high pressures and temperatures, necessitating materials with high fracture toughness and "
            "corrosion resistance. Containment buildings are designed to prevent release of radioactive materials "
            "in case of accidents, typically constructed with reinforced concrete and steel liners. Emergency Core "
            "Cooling Systems (ECCS) provide backup cooling to the core during loss-of-coolant accidents (LOCA), "
            "and their reliability is mandated by 10 CFR 50.46. Safety analyses employ deterministic methods to "
            "evaluate design-basis accidents and probabilistic risk assessments (PRA) to quantify failure probabilities. "
            "NRC regulations require periodic safety reviews and incorporation of lessons learned from incidents such "
            "as Three Mile Island. Human factors engineering and operator training are critical to prevent and mitigate "
            "incidents. Redundancy and diversity in safety systems reduce common cause failures. The defense-in-depth "
            "philosophy underpins PWR safety, layering multiple barriers against radiological release. Aging management "
            "programs address material degradation over reactor lifetime. Overall, PWR safety integrates engineering, "
            "regulatory oversight, and operational discipline to maintain public and environmental protection."
        ),
        key_factors=[
            "Coolant system integrity",
            "Containment structure robustness",
            "Emergency Core Cooling System reliability",
            "Regulatory compliance (NRC 10 CFR 50.46)",
            "Material properties and aging management",
            "Probabilistic Risk Assessment (PRA)",
            "Operator training and human factors",
            "Defense-in-depth safety philosophy"
        ],
        primary_authority=[
            "Nuclear Regulatory Commission (NRC), 10 CFR Part 50",
            "U.S. NRC Regulatory Guide 1.70 - Standard Format and Content of Safety Analysis Reports",
            "Institute of Nuclear Power Operations (INPO) Reports",
            "International Atomic Energy Agency (IAEA) Safety Standards Series No. SSR-2/1",
            "U.S. NRC NUREG-1150: Severe Accident Risks"
        ],
        burden_holder="Nuclear plant operator/licensee",
        adversary_position="Claims that safety systems are insufficient to prevent core damage under extreme scenarios",
        counter_arguments=[
            "Demonstrated compliance with NRC safety requirements and successful safety drills",
            "Redundancy and diversity in safety systems reduce likelihood of simultaneous failures",
            "Probabilistic risk assessments show extremely low core damage frequency",
            "Continuous monitoring and maintenance programs mitigate degradation risks",
            "Independent oversight by NRC and third-party audits ensure safety culture adherence"
        ],
        resolution_strategy=(
            "Conduct comprehensive safety reviews incorporating deterministic and probabilistic analyses, "
            "enhance operator training programs, and implement continuous improvement based on operational feedback."
        ),
        entity_scope="Commercial nuclear power plants operating PWR technology in the United States",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NRC v. Entergy Nuclear Vermont Yankee, 2012 (NRC licensing and safety enforcement)"
    ),

    DoctrineBlock(
        topic="Solar Photovoltaic Cell Efficiency Enhancement",
        keywords=["solar", "photovoltaic", "PV cell", "efficiency", "inverter", "MPPT", "grid-tie", "semiconductor"],
        conclusion_template=(
            "Maximizing photovoltaic cell efficiency requires optimizing semiconductor materials, "
            "minimizing resistive losses, and employing advanced inverter technologies with maximum power point tracking (MPPT). "
            "Grid-tied systems must ensure synchronization and power quality compliance to maintain stability."
        ),
        reasoning_framework=(
            "Photovoltaic (PV) cell efficiency is fundamentally limited by semiconductor physics, including bandgap energy and recombination losses. "
            "Silicon-based cells dominate the market, with monocrystalline cells achieving efficiencies around 22-24%. "
            "Emerging technologies such as perovskite and multi-junction cells offer higher theoretical efficiencies but face durability challenges. "
            "Reducing resistive losses in cell interconnections and encapsulation materials improves output power. "
            "Inverter technology plays a critical role in converting DC to AC power with minimal losses and ensuring grid compatibility. "
            "Maximum Power Point Tracking (MPPT) algorithms dynamically adjust the load to extract maximum power under varying irradiance and temperature. "
            "Grid-tied inverters must comply with IEEE 1547 standards for interconnection, including anti-islanding protection and power factor control. "
            "Thermal management of PV modules affects efficiency; elevated temperatures reduce voltage and power output. "
            "System design must consider shading, soiling, and degradation over time to maintain performance. "
            "Lifecycle assessments and balance of system components impact overall energy yield and cost-effectiveness."
        ),
        key_factors=[
            "Semiconductor material properties",
            "Cell interconnection and resistive losses",
            "Inverter efficiency and MPPT algorithms",
            "Thermal management of PV modules",
            "Grid interconnection standards (IEEE 1547)",
            "Environmental factors (irradiance, temperature, shading)",
            "Degradation rates and durability",
            "Balance of system components"
        ],
        primary_authority=[
            "National Renewable Energy Laboratory (NREL) Best Research-Cell Efficiencies",
            "IEEE Standard 1547-2018 - Interconnection and Interoperability of Distributed Energy Resources",
            "U.S. Department of Energy Solar Energy Technologies Office Reports",
            "International Electrotechnical Commission (IEC) 61215 - PV Module Qualification",
            "Fraunhofer Institute for Solar Energy Systems ISE Photovoltaics Reports"
        ],
        burden_holder="PV system designer and installer",
        adversary_position="Claims that current PV technology cannot achieve cost-effective efficiency improvements",
        counter_arguments=[
            "Continuous material science advances have steadily improved cell efficiencies",
            "MPPT and inverter innovations reduce system losses significantly",
            "Grid code compliance ensures safe and reliable integration",
            "Economies of scale and manufacturing improvements lower costs",
            "Hybrid and tandem cell technologies promise further gains"
        ],
        resolution_strategy=(
            "Invest in R&D for advanced materials and inverter controls, implement rigorous testing and certification, "
            "and optimize system design for site-specific conditions."
        ),
        entity_scope="Utility-scale and distributed solar photovoltaic installations worldwide",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="California Public Utilities Commission (CPUC) Decision 14-12-035 on Smart Inverter Requirements"
    ),

    DoctrineBlock(
        topic="Wind Turbine Aerodynamics and Capacity Factor Optimization",
        keywords=["wind power", "turbine", "aerodynamics", "HAWT", "capacity factor", "Betz limit", "blade design", "wake effect"],
        conclusion_template=(
            "Optimizing wind turbine performance involves aerodynamic blade design to approach the Betz limit, "
            "minimizing wake losses, and siting turbines to maximize capacity factor. Horizontal Axis Wind Turbines (HAWT) dominate due to superior efficiency."
        ),
        reasoning_framework=(
            "Wind turbine energy capture is fundamentally limited by the Betz limit, which states that no turbine can capture more than 59.3% of the kinetic energy in wind. "
            "Blade aerodynamic design focuses on maximizing lift-to-drag ratio, using airfoil shapes optimized for varying wind speeds. "
            "Pitch and yaw control systems adjust blade angle and orientation to maintain optimal angle of attack and maximize power output. "
            "Horizontal Axis Wind Turbines (HAWT) are preferred for their higher efficiency and scalability compared to Vertical Axis Wind Turbines (VAWT). "
            "Wake effects from upstream turbines reduce wind speed and increase turbulence downstream, lowering overall farm output. "
            "Turbine spacing and layout optimization mitigate wake losses. "
            "Capacity factor, the ratio of actual energy produced to the maximum possible, depends on wind resource quality, turbine availability, and operational efficiency. "
            "Advanced materials reduce blade weight and increase fatigue life, enhancing reliability. "
            "Control strategies including variable speed operation and active load control improve energy capture and reduce structural loads. "
            "Environmental considerations such as noise, avian impact, and visual aesthetics influence siting and design decisions."
        ),
        key_factors=[
            "Aerodynamic blade design and airfoil selection",
            "Betz limit theoretical maximum",
            "Wake effect and turbine spacing",
            "Pitch and yaw control mechanisms",
            "Capacity factor and wind resource assessment",
            "Material fatigue and reliability",
            "Variable speed and load control",
            "Environmental impact considerations"
        ],
        primary_authority=[
            "American Wind Energy Association (AWEA) Wind Energy Handbook",
            "International Electrotechnical Commission (IEC) 61400 series standards",
            "National Renewable Energy Laboratory (NREL) Wind Technology Reports",
            "European Wind Energy Association (EWEA) Best Practices",
            "U.S. Department of Energy Wind Vision Report"
        ],
        burden_holder="Wind farm developer and operator",
        adversary_position="Concerns over variability and intermittency reducing reliability and economic viability",
        counter_arguments=[
            "Advanced forecasting and grid integration reduce variability impact",
            "Hybrid systems and storage enhance reliability",
            "Capacity factors have improved with larger, taller turbines",
            "Wake modeling and farm design optimize output",
            "Policy incentives support economic feasibility"
        ],
        resolution_strategy=(
            "Implement comprehensive wind resource assessments, optimize turbine design and layout, "
            "and integrate with grid and storage solutions to maximize capacity factor and reliability."
        ),
        entity_scope="Onshore and offshore wind power projects globally",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FERC Order No. 841 on Energy Storage Participation in Markets (impacting wind integration)"
    ),

    DoctrineBlock(
        topic="Hydroelectric Dam Turbine Selection and Operation",
        keywords=["hydroelectric", "dam", "turbine", "Francis", "Pelton", "Kaplan", "pumped storage", "efficiency"],
        conclusion_template=(
            "Selecting appropriate turbine types (Francis, Pelton, Kaplan) based on head and flow characteristics "
            "maximizes hydroelectric efficiency. Pumped storage enhances grid flexibility and energy arbitrage capabilities."
        ),
        reasoning_framework=(
            "Hydroelectric power generation depends on converting potential energy of water into mechanical energy via turbines. "
            "The choice of turbine is dictated by site-specific hydraulic conditions: high-head, low-flow sites favor Pelton turbines; "
            "medium-head, medium-flow sites use Francis turbines; low-head, high-flow sites employ Kaplan turbines. "
            "Each turbine type has unique runner designs optimized for efficiency under expected operating conditions. "
            "Pumped storage hydroelectricity enables energy storage by pumping water to an elevated reservoir during low demand and releasing it during peak demand. "
            "This provides grid balancing, frequency regulation, and renewable integration support. "
            "Turbine efficiency curves must be matched with expected flow regimes to minimize cavitation and mechanical wear. "
            "Environmental impacts such as fish migration and sediment transport require mitigation measures. "
            "Control systems regulate turbine speed and gate openings to maintain grid frequency and voltage stability. "
            "Lifecycle costs include maintenance of mechanical components and sediment management. "
            "Regulatory compliance involves water rights, environmental permits, and safety standards."
        ),
        key_factors=[
            "Hydraulic head and flow rate",
            "Turbine type and runner design",
            "Pumped storage operational strategy",
            "Turbine efficiency and cavitation control",
            "Environmental impact mitigation",
            "Grid frequency and voltage regulation",
            "Maintenance and lifecycle costs",
            "Regulatory and permitting requirements"
        ],
        primary_authority=[
            "U.S. Department of Energy Hydropower Program Technical Reports",
            "International Commission on Large Dams (ICOLD) Guidelines",
            "Federal Energy Regulatory Commission (FERC) Hydropower Licensing",
            "Electric Power Research Institute (EPRI) Hydropower Research",
            "American Society of Mechanical Engineers (ASME) Boiler and Pressure Vessel Code"
        ],
        burden_holder="Hydropower plant operator and engineer",
        adversary_position="Concerns about environmental disruption and sedimentation reducing long-term viability",
        counter_arguments=[
            "Fish ladders and bypass systems mitigate ecological impact",
            "Sediment flushing and dredging maintain reservoir capacity",
            "Pumped storage supports renewable integration and grid stability",
            "Modern turbine designs reduce fish mortality",
            "Regulatory frameworks enforce environmental safeguards"
        ],
        resolution_strategy=(
            "Adopt integrated environmental and engineering design approaches, implement adaptive management, "
            "and comply with regulatory requirements to balance energy production and ecological preservation."
        ),
        entity_scope="Large and small hydroelectric facilities with dam infrastructure",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FERC Hydropower Licensing Orders and Environmental Impact Statements"
    ),

    DoctrineBlock(
        topic="Grid Operations: Dispatch and Frequency Regulation",
        keywords=["grid operations", "dispatch", "frequency regulation", "load balancing", "ancillary services", "AGC", "NERC standards", "real-time control"],
        conclusion_template=(
            "Effective grid operations require real-time dispatch and frequency regulation to maintain system stability. "
            "Automatic Generation Control (AGC) and ancillary services ensure load-generation balance within NERC reliability standards."
        ),
        reasoning_framework=(
            "Electric power grids operate in real-time to balance supply and demand, maintaining system frequency typically at 60 Hz in North America. "
            "Dispatch involves scheduling generation units to meet forecasted loads while considering unit constraints and economic merit order. "
            "Frequency regulation corrects short-term imbalances caused by load fluctuations or generation variability. "
            "Automatic Generation Control (AGC) systems adjust generator outputs within seconds to minutes to maintain frequency and interchange schedules. "
            "Ancillary services such as spinning reserve, non-spinning reserve, and regulation reserves provide flexibility and contingency response. "
            "NERC Reliability Standards (e.g., BAL-001) mandate performance criteria for frequency response and control performance. "
            "Grid operators use SCADA and EMS systems for monitoring and control, integrating telemetry data and predictive analytics. "
            "Renewable energy integration introduces variability and uncertainty, increasing the need for fast-responding regulation resources. "
            "Demand response programs and energy storage systems contribute to frequency regulation and peak load management. "
            "Inter-area oscillations and voltage stability are also monitored to prevent cascading failures and blackouts."
        ),
        key_factors=[
            "Real-time load and generation balancing",
            "Automatic Generation Control (AGC)",
            "Ancillary services and reserves",
            "NERC Reliability Standards compliance",
            "SCADA and EMS system capabilities",
            "Renewable integration impacts",
            "Demand response and storage participation",
            "System frequency and voltage stability"
        ],
        primary_authority=[
            "North American Electric Reliability Corporation (NERC) BAL Standards",
            "Federal Energy Regulatory Commission (FERC) Orders 755 and 842",
            "IEEE Standard 1547 for DER interconnection",
            "Electric Reliability Council of Texas (ERCOT) Protocols",
            "U.S. Department of Energy Grid Modernization Reports"
        ],
        burden_holder="Transmission system operator (TSO) and balancing authority",
        adversary_position="Claims that high renewable penetration undermines grid reliability and frequency control",
        counter_arguments=[
            "Advanced forecasting and flexible resources mitigate variability",
            "Fast-ramping units and storage enhance regulation capabilities",
            "Demand response programs provide additional balancing resources",
            "Grid codes and standards evolve to accommodate renewables",
            "Regional coordination improves system resilience"
        ],
        resolution_strategy=(
            "Enhance grid operator tools, expand ancillary service markets, integrate storage and demand response, "
            "and update reliability standards to address evolving grid dynamics."
        ),
        entity_scope="Regional transmission organizations (RTOs) and independent system operators (ISOs) in North America",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FERC Order No. 755 on Frequency Regulation Compensation"
    ),

    DoctrineBlock(
        topic="Energy Storage Technologies: Lithium-Ion and Flow Batteries",
        keywords=["energy storage", "lithium-ion", "flow battery", "cycle life", "depth of discharge", "capacity fade", "grid-scale", "battery management system"],
        conclusion_template=(
            "Lithium-ion and flow batteries offer complementary energy storage solutions with trade-offs in energy density, cycle life, and scalability. "
            "Battery management systems (BMS) are critical to optimize performance and extend operational lifespan."
        ),
        reasoning_framework=(
            "Lithium-ion batteries dominate grid-scale and electric vehicle energy storage due to high energy density, efficiency (~90-95%), and fast response times. "
            "However, they suffer from capacity fade over repeated charge-discharge cycles, thermal runaway risks, and limited cycle life typically ranging from 3000 to 5000 cycles depending on chemistry and usage. "
            "Depth of Discharge (DoD) management is essential to prolong battery life; operating within recommended DoD limits reduces degradation. "
            "Flow batteries, such as vanadium redox flow batteries, store energy in liquid electrolytes external to the cell stack, allowing independent scaling of power and energy capacity. "
            "They offer longer cycle life (>10,000 cycles), enhanced safety, and easier recyclability but lower energy density and higher upfront costs. "
            "Battery Management Systems (BMS) monitor cell voltages, temperatures, and currents to prevent overcharge, overdischarge, and thermal events. "
            "Thermal management systems maintain optimal operating temperatures to reduce degradation rates. "
            "Grid-scale applications require integration with power electronics and control systems to provide services such as frequency regulation, peak shaving, and backup power. "
            "Lifecycle cost analysis must consider capital costs, operational expenses, replacement schedules, and recycling or disposal impacts. "
            "Safety standards such as UL 1973 and IEC 62619 govern battery system design and certification."
        ),
        key_factors=[
            "Energy density and efficiency",
            "Cycle life and capacity fade",
            "Depth of Discharge management",
            "Battery Management System functionality",
            "Thermal management",
            "Scalability and modularity",
            "Safety and certification standards",
            "Lifecycle cost and environmental impact"
        ],
        primary_authority=[
            "U.S. Department of Energy Energy Storage Systems Program",
            "International Electrotechnical Commission (IEC) 62619 - Safety Requirements for Secondary Batteries",
            "Underwriters Laboratories (UL) 1973 - Batteries for Use in Stationary Applications",
            "National Renewable Energy Laboratory (NREL) Energy Storage Reports",
            "Energy Storage Association (ESA) Technical Guidelines"
        ],
        burden_holder="Energy storage system designer and operator",
        adversary_position="Concerns about lithium-ion battery safety and degradation limiting grid-scale deployment",
        counter_arguments=[
            "Advanced chemistries and BMS improve safety and longevity",
            "Flow batteries provide safer alternatives for long-duration storage",
            "Thermal management and monitoring reduce failure risks",
            "Regulatory standards enforce rigorous testing and certification",
            "Hybrid storage systems optimize performance and cost"
        ],
        resolution_strategy=(
            "Implement robust BMS and thermal controls, diversify storage technologies based on application, "
            "and adhere to evolving safety and performance standards."
        ),
        entity_scope="Grid-scale and distributed energy storage installations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FERC Order No. 841 on Energy Storage Participation in Wholesale Markets"
    ),

    DoctrineBlock(
        topic="Geothermal Resource Assessment and Enhanced Geothermal Systems (EGS)",
        keywords=["geothermal", "resource assessment", "EGS", "binary cycle", "flash steam", "dry steam", "reservoir stimulation", "thermal conductivity"],
        conclusion_template=(
            "Accurate geothermal resource assessment combining geological, geophysical, and geochemical data is essential for successful development. "
            "Enhanced Geothermal Systems (EGS) expand resource availability by reservoir stimulation and engineered heat extraction."
        ),
        reasoning_framework=(
            "Geothermal resource assessment involves evaluating subsurface temperature gradients, rock permeability, and fluid availability. "
            "Traditional hydrothermal resources utilize naturally permeable reservoirs with sufficient water and heat. "
            "Enhanced Geothermal Systems (EGS) create artificial permeability through hydraulic stimulation of hot dry rock formations, enabling heat extraction where natural reservoirs are inadequate. "
            "Reservoir characterization employs seismic surveys, magnetotellurics, and well logging to map fracture networks and thermal anomalies. "
            "Binary cycle plants use secondary working fluids with low boiling points to convert moderate temperature geothermal fluids into electricity, expanding viable resource temperature ranges. "
            "Flash steam plants exploit high-temperature fluids (>180°C) by flashing hot water into steam to drive turbines. Dry steam plants use steam directly from reservoirs. "
            "Thermal conductivity and heat capacity of rock formations influence reservoir longevity and power output sustainability. "
            "Induced seismicity risk from reservoir stimulation requires monitoring and mitigation strategies. "
            "Economic feasibility depends on drilling costs, reservoir productivity, and power plant efficiency. "
            "Environmental impacts include land use, water consumption, and potential subsidence."
        ),
        key_factors=[
            "Subsurface temperature and permeability",
            "Reservoir stimulation techniques",
            "Plant technology selection (binary, flash, dry steam)",
            "Geophysical and geochemical exploration methods",
            "Induced seismicity monitoring",
            "Thermal conductivity and reservoir sustainability",
            "Economic and environmental considerations",
            "Regulatory permitting and water rights"
        ],
        primary_authority=[
            "U.S. Department of Energy Geothermal Technologies Office",
            "Geothermal Resources Council (GRC) Transactions",
            "International Energy Agency (IEA) Geothermal Implementing Agreement",
            "Society of Petroleum Engineers (SPE) Reservoir Engineering Publications",
            "Environmental Protection Agency (EPA) Geothermal Regulations"
        ],
        burden_holder="Geothermal project developer and reservoir engineer",
        adversary_position="Skepticism regarding induced seismicity and economic viability of EGS",
        counter_arguments=[
            "Advanced monitoring and control reduce seismic risks",
            "Successful pilot projects demonstrate technical feasibility",
            "Binary cycle plants enable utilization of lower temperature resources",
            "Economic models account for risk and resource variability",
            "Regulatory frameworks manage environmental impacts"
        ],
        resolution_strategy=(
            "Integrate multidisciplinary resource assessment, implement adaptive reservoir management, "
            "and engage stakeholders to balance development and environmental protection."
        ),
        entity_scope="Geothermal power projects and resource exploration globally",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Calpine v. U.S. EPA, 2014 (Geothermal permitting and environmental compliance)"
    ),

    DoctrineBlock(
        topic="Hydrogen Production via Electrolysis and Small Modular Reactors (SMR)",
        keywords=["hydrogen", "electrolysis", "SMR", "fuel cell", "PEM", "SOFC", "green hydrogen", "nuclear hydrogen"],
        conclusion_template=(
            "Hydrogen production through electrolysis powered by renewable or nuclear energy offers a low-carbon pathway. "
            "Small Modular Reactors (SMRs) provide high-temperature heat and electricity for efficient hydrogen generation and fuel cell applications."
        ),
        reasoning_framework=(
            "Electrolysis splits water into hydrogen and oxygen using electrical energy; efficiency depends on electrolyzer type and operating conditions. "
            "Proton Exchange Membrane (PEM) electrolyzers offer rapid response and high purity hydrogen, suitable for variable renewable integration. "
            "Alkaline electrolyzers are mature and cost-effective but less responsive. Solid Oxide Electrolyzers (SOEC) operate at high temperatures, improving efficiency by utilizing thermal energy. "
            "Small Modular Reactors (SMRs) can supply high-temperature heat and electricity, enabling thermochemical hydrogen production processes with higher overall efficiency. "
            "Nuclear hydrogen production reduces carbon emissions compared to fossil-fuel-based methods. "
            "Fuel cells such as PEM and Solid Oxide Fuel Cells (SOFC) convert hydrogen back to electricity with high efficiency and low emissions. "
            "System integration challenges include hydrogen storage, compression, and distribution infrastructure. "
            "Safety considerations involve hydrogen's flammability and leak detection. "
            "Economic viability depends on capital costs, electricity prices, and policy incentives for low-carbon hydrogen. "
            "Regulatory frameworks for hydrogen production and nuclear operations must be harmonized."
        ),
        key_factors=[
            "Electrolyzer technology and efficiency",
            "SMR thermal and electrical output",
            "Fuel cell types and performance",
            "Hydrogen storage and distribution",
            "Safety and leak detection",
            "Capital and operational costs",
            "Regulatory compliance and licensing",
            "Integration with renewable and nuclear sources"
        ],
        primary_authority=[
            "U.S. Department of Energy Hydrogen and Fuel Cell Technologies Office",
            "International Atomic Energy Agency (IAEA) Nuclear Hydrogen Production Reports",
            "U.S. Nuclear Regulatory Commission (NRC) SMR Licensing Framework",
            "Hydrogen Council Global Roadmap",
            "Fuel Cell and Hydrogen Energy Association (FCHEA) Technical Publications"
        ],
        burden_holder="Hydrogen producer and nuclear plant operator",
        adversary_position="Concerns about high costs and safety risks of nuclear hydrogen production",
        counter_arguments=[
            "SMRs offer scalable, safer nuclear options with passive safety features",
            "Electrolysis powered by renewables or nuclear reduces carbon footprint",
            "Advances in materials and system design improve safety and economics",
            "Policy incentives support market development",
            "Hydrogen infrastructure standards enhance safety and interoperability"
        ],
        resolution_strategy=(
            "Develop integrated hydrogen production systems with robust safety protocols, "
            "optimize electrolyzer and reactor designs, and engage regulatory agencies early."
        ),
        entity_scope="Hydrogen production facilities coupled with nuclear and renewable energy sources",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="DOE Hydrogen Program Reports and NRC SMR Licensing Reviews"
    ),

    DoctrineBlock(
        topic="Natural Gas Pipeline Compression and Metering",
        keywords=["natural gas", "pipeline", "compression", "metering", "LNG", "flow measurement", "pressure regulation", "gas quality"],
        conclusion_template=(
            "Efficient natural gas pipeline operation requires reliable compression and accurate metering to maintain flow and ensure custody transfer integrity. "
            "Compliance with API standards and regulatory requirements ensures safety and measurement accuracy."
        ),
        reasoning_framework=(
            "Natural gas pipelines transport gas over long distances requiring compressor stations to maintain pressure and flow rates. "
            "Compression increases gas pressure to overcome frictional losses and elevation changes. "
            "Compressor types include centrifugal and reciprocating, selected based on capacity, efficiency, and maintenance considerations. "
            "Metering stations measure gas volume and quality for custody transfer and operational control. "
            "Flow measurement technologies include ultrasonic, turbine, and orifice meters, each with specific accuracy and maintenance profiles. "
            "Gas quality parameters such as heating value, moisture content, and contaminants affect pipeline integrity and end-use performance. "
            "Pressure regulation stations reduce pressure for distribution or processing. "
            "Regulatory compliance includes adherence to Pipeline and Hazardous Materials Safety Administration (PHMSA) regulations and API standards (e.g., API 14.3 for metering). "
            "Leak detection and corrosion monitoring systems enhance pipeline safety. "
            "Operational data integration supports real-time monitoring and predictive maintenance."
        ),
        key_factors=[
            "Compressor station design and efficiency",
            "Metering technology and accuracy",
            "Gas quality monitoring",
            "Pressure regulation and control",
            "Regulatory compliance (PHMSA, API)",
            "Leak detection and corrosion management",
            "Operational data analytics",
            "Maintenance and safety protocols"
        ],
        primary_authority=[
            "U.S. Department of Transportation PHMSA Pipeline Safety Regulations",
            "American Petroleum Institute (API) Standards 14.3, 5L, 6D",
            "Gas Processors Association (GPA) Measurement Standards",
            "Pipeline Research Council International (PRCI) Technical Reports",
            "National Institute of Standards and Technology (NIST) Gas Measurement Guidelines"
        ],
        burden_holder="Pipeline operator and compressor station engineer",
        adversary_position="Claims of measurement inaccuracies and compression inefficiencies leading to revenue loss and safety risks",
        counter_arguments=[
            "Use of high-accuracy metering technologies and regular calibration",
            "Redundant measurement and verification systems",
            "Advanced compressor controls optimize efficiency",
            "Comprehensive maintenance and inspection programs",
            "Regulatory audits and compliance enforcement"
        ],
        resolution_strategy=(
            "Implement state-of-the-art metering and compression technologies, "
            "conduct rigorous calibration and maintenance, and maintain transparent regulatory reporting."
        ),
        entity_scope="Natural gas transmission and distribution pipeline systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="PHMSA Enforcement Actions and API Standard Adoption Cases"
    ),

    DoctrineBlock(
        topic="Coal Combustion and Gasification Technologies",
        keywords=["coal", "combustion", "gasification", "IGCC", "carbon capture", "CCS", "CCUS", "emissions control"],
        conclusion_template=(
            "Integrated Gasification Combined Cycle (IGCC) technology enables cleaner coal utilization by converting coal into syngas for combined cycle power generation. "
            "Carbon capture and storage (CCS) and utilization (CCUS) technologies mitigate CO2 emissions from coal plants."
        ),
        reasoning_framework=(
            "Coal combustion in traditional pulverized coal boilers produces flue gases containing CO2, SOx, NOx, particulate matter, and mercury. "
            "Gasification converts coal into synthesis gas (syngas) composed mainly of CO and H2, enabling removal of impurities before combustion in a combined cycle gas turbine, improving efficiency and reducing emissions. "
            "IGCC plants achieve higher thermal efficiency (~40-45%) compared to conventional coal plants (~33-38%). "
            "Carbon capture technologies include pre-combustion (syngas shift and CO2 separation), post-combustion (amine scrubbing), and oxy-fuel combustion. "
            "Captured CO2 can be compressed and injected into geological formations for long-term storage (CCS) or used in enhanced oil recovery and chemical synthesis (CCUS). "
            "Challenges include high capital costs, energy penalties, and integration complexity. "
            "Environmental regulations such as the Clean Air Act and EPA New Source Performance Standards (NSPS) drive adoption of emissions controls. "
            "Continuous emissions monitoring systems (CEMS) ensure compliance. "
            "Coal quality and feedstock variability affect gasifier performance and syngas composition. "
            "Lifecycle assessments consider mining impacts, water use, and waste management."
        ),
        key_factors=[
            "Coal gasification process efficiency",
            "Syngas cleanup and impurity removal",
            "Carbon capture technology selection",
            "Integration with combined cycle turbines",
            "Regulatory compliance and emissions monitoring",
            "Capital and operational costs",
            "Environmental and lifecycle impacts",
            "Waste and byproduct management"
        ],
        primary_authority=[
            "U.S. Environmental Protection Agency (EPA) Clean Air Act Regulations",
            "Department of Energy (DOE) Clean Coal Technology Program",
            "International Energy Agency (IEA) Coal Industry Advisory Board Reports",
            "Electric Power Research Institute (EPRI) Coal Fleet Reports",
            "American Society of Mechanical Engineers (ASME) Gasification Standards"
        ],
        burden_holder="Coal plant operator and technology provider",
        adversary_position="Concerns about economic viability and environmental risks of coal gasification and CCS",
        counter_arguments=[
            "IGCC with CCS reduces emissions significantly compared to conventional coal plants",
            "Technological advancements lower costs and improve reliability",
            "Policy incentives support clean coal technologies",
            "Lifecycle analyses demonstrate reduced environmental footprint",
            "Robust monitoring and safety protocols mitigate risks"
        ],
        resolution_strategy=(
            "Optimize gasification and capture technologies, secure policy support, and implement comprehensive environmental management."
        ),
        entity_scope="Coal-fired power generation facilities employing advanced combustion and gasification",
        confidence=0.85,
        confidence_zone="Moderate-High",
        controlling_precedent="EPA NSPS for Greenhouse Gas Emissions from Electric Utility Generating Units"
    ),

    DoctrineBlock(
        topic="Bioenergy: Biomass Conversion and Anaerobic Digestion",
        keywords=["bioenergy", "biomass", "ethanol", "biodiesel", "anaerobic digestion", "biogas", "renewable fuels", "waste-to-energy"],
        conclusion_template=(
            "Bioenergy technologies convert biomass feedstocks into renewable fuels and biogas through biochemical and thermochemical processes. "
            "Anaerobic digestion provides sustainable waste management and methane-rich biogas production."
        ),
        reasoning_framework=(
            "Biomass conversion encompasses processes such as fermentation to produce ethanol, transesterification for biodiesel, and anaerobic digestion for biogas. "
            "Ethanol production typically uses sugar or starch-rich feedstocks fermented by yeast, with distillation and dehydration to achieve fuel-grade purity. "
            "Biodiesel is produced by reacting vegetable oils or animal fats with alcohols in the presence of catalysts. "
            "Anaerobic digestion involves microbial breakdown of organic matter in oxygen-free environments, generating methane-rich biogas and digestate usable as fertilizer. "
            "Biogas can be upgraded to biomethane for pipeline injection or used for combined heat and power (CHP) applications. "
            "Feedstock availability, composition, and logistics impact process efficiency and economics. "
            "Sustainability considerations include land use, lifecycle greenhouse gas emissions, and competition with food production. "
            "Regulatory frameworks govern renewable fuel standards (RFS) and incentives such as Renewable Identification Numbers (RINs). "
            "Technological challenges include process optimization, contamination control, and scale-up. "
            "Integration with waste management systems enhances environmental benefits."
        ),
        key_factors=[
            "Feedstock type and availability",
            "Conversion technology and efficiency",
            "Biogas composition and upgrading",
            "Sustainability and lifecycle emissions",
            "Regulatory incentives and compliance",
            "Process scale and economics",
            "Waste management integration",
            "Product quality and market demand"
        ],
        primary_authority=[
            "U.S. Environmental Protection Agency (EPA) Renewable Fuel Standard (RFS)",
            "U.S. Department of Agriculture (USDA) Bioenergy Programs",
            "International Energy Agency (IEA) Bioenergy Task Reports",
            "American Biogas Council Technical Guidelines",
            "National Renewable Energy Laboratory (NREL) Bioenergy Research"
        ],
        burden_holder="Bioenergy facility operator and feedstock supplier",
        adversary_position="Concerns about indirect land use change and food vs fuel competition",
        counter_arguments=[
            "Use of waste and residue feedstocks minimizes land use impacts",
            "Advanced conversion technologies improve yields and reduce emissions",
            "Lifecycle analyses account for indirect effects",
            "Policy frameworks incentivize sustainable practices",
            "Co-products and digestate provide additional value"
        ],
        resolution_strategy=(
            "Prioritize sustainable feedstocks, optimize conversion processes, and engage in transparent lifecycle assessments."
        ),
        entity_scope="Bioenergy production facilities including ethanol plants, biodiesel refineries, and anaerobic digesters",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="EPA RFS Program and Renewable Fuel Standard Litigation"
    ),

    DoctrineBlock(
        topic="Ocean Energy Conversion: Tidal, Wave, and Ocean Thermal Energy Conversion (OTEC)",
        keywords=["ocean energy", "tidal", "wave", "OTEC", "salinity gradient", "marine renewable", "energy conversion", "environmental impact"],
        conclusion_template=(
            "Ocean energy technologies harness tidal, wave, and thermal gradients to generate renewable power. "
            "Environmental and technical challenges require site-specific assessments and adaptive designs."
        ),
        reasoning_framework=(
            "Tidal energy exploits predictable tidal currents using barrages, tidal fences, or turbines to generate electricity. "
            "Wave energy converters capture kinetic energy from surface waves through oscillating water columns, point absorbers, or attenuators. "
            "Ocean Thermal Energy Conversion (OTEC) utilizes temperature differences between warm surface water and cold deep water to drive thermodynamic cycles, typically Rankine cycles, for power generation. "
            "Salinity gradient energy, or blue energy, leverages osmotic pressure differences between freshwater and seawater for power production. "
            "Technical challenges include marine biofouling, corrosion, and survivability in harsh ocean environments. "
            "Environmental impacts involve effects on marine ecosystems, sediment transport, and navigation. "
            "Energy density and capacity factors vary with site and technology maturity. "
            "Grid connection and transmission infrastructure pose logistical and economic challenges. "
            "Regulatory frameworks address marine spatial planning, environmental protection, and permitting. "
            "Research and pilot projects continue to advance technology readiness levels and cost reduction."
        ),
        key_factors=[
            "Tidal current velocity and predictability",
            "Wave height and frequency spectra",
            "Thermal gradient magnitude for OTEC",
            "Marine environmental impact assessments",
            "Material durability and biofouling resistance",
            "Grid interconnection feasibility",
            "Regulatory and permitting requirements",
            "Technology maturity and cost"
        ],
        primary_authority=[
            "International Renewable Energy Agency (IRENA) Ocean Energy Reports",
            "U.S. Department of Energy Water Power Technologies Office",
            "International Electrotechnical Commission (IEC) TC 114 - Marine Energy",
            "European Marine Energy Centre (EMEC) Test Reports",
            "National Oceanic and Atmospheric Administration (NOAA) Marine Spatial Planning Guidelines"
        ],
        burden_holder="Ocean energy project developer and environmental consultant",
        adversary_position="Concerns about ecological disruption and economic viability",
        counter_arguments=[
            "Predictable tidal cycles enable reliable power generation",
            "Environmental monitoring and mitigation minimize impacts",
            "Technological advancements improve survivability and efficiency",
            "Policy support and incentives foster development",
            "Pilot projects demonstrate feasibility and scalability"
        ],
        resolution_strategy=(
            "Conduct thorough environmental and technical assessments, engage stakeholders, "
            "and implement adaptive management and robust engineering designs."
        ),
        entity_scope="Marine renewable energy projects in tidal, wave, and thermal resource areas",
        confidence=0.80,
        confidence_zone="Moderate",
        controlling_precedent="EMEC Licensing and Environmental Compliance Cases"
    ),

    DoctrineBlock(
        topic="Energy Efficiency in Building HVAC Systems",
        keywords=["energy efficiency", "HVAC", "building", "thermal comfort", "variable air volume", "heat recovery", "demand control ventilation", "building automation"],
        conclusion_template=(
            "Optimizing HVAC systems through advanced controls, heat recovery, and demand-based ventilation significantly reduces building energy consumption while maintaining occupant comfort."
        ),
        reasoning_framework=(
            "Heating, Ventilation, and Air Conditioning (HVAC) systems represent a major portion of building energy use. "
            "Energy efficiency improvements focus on reducing thermal losses, optimizing airflow, and recovering waste heat. "
            "Variable Air Volume (VAV) systems adjust airflow based on occupancy and load, reducing fan energy and improving comfort. "
            "Heat recovery ventilators (HRVs) and energy recovery ventilators (ERVs) reclaim thermal energy from exhaust air to precondition incoming fresh air. "
            "Demand Control Ventilation (DCV) uses CO2 or occupancy sensors to modulate ventilation rates, balancing air quality and energy use. "
            "Building automation systems (BAS) integrate sensors, controllers, and actuators to optimize HVAC operation dynamically. "
            "Proper system design considers building envelope, internal loads, and climate zone. "
            "Commissioning and maintenance ensure systems operate as intended and maintain efficiency over time. "
            "Energy codes such as ASHRAE 90.1 and standards like LEED guide design and performance benchmarks. "
            "Advanced modeling tools simulate HVAC performance and identify optimization opportunities."
        ),
        key_factors=[
            "Variable Air Volume system implementation",
            "Heat and energy recovery technologies",
            "Demand Control Ventilation strategies",
            "Building Automation System integration",
            "Building envelope and insulation quality",
            "Occupant comfort and indoor air quality",
            "Commissioning and maintenance practices",
            "Compliance with energy codes and standards"
        ],
        primary_authority=[
            "ASHRAE Standard 90.1 - Energy Standard for Buildings",
            "U.S. Department of Energy Building Technologies Office",
            "International Energy Agency (IEA) Energy Efficiency Reports",
            "U.S. Green Building Council (USGBC) LEED Certification Guidelines",
            "American Society of Heating, Refrigerating and Air-Conditioning Engineers (ASHRAE) Handbook"
        ],
        burden_holder="Building design engineer and facility manager",
        adversary_position="Claims that energy efficiency upgrades increase upfront costs and complexity",
        counter_arguments=[
            "Lifecycle cost savings offset initial investments",
            "Improved occupant comfort enhances productivity",
            "Incentives and rebates reduce financial barriers",
            "Advanced controls reduce operational complexity",
            "Energy codes mandate minimum efficiency levels"
        ],
        resolution_strategy=(
            "Perform integrated design with lifecycle cost analysis, implement advanced controls, "
            "and ensure ongoing commissioning and maintenance."
        ),
        entity_scope="Commercial and residential building HVAC systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASHRAE 90.1 Code Adoption and Enforcement Cases"
    ),

    DoctrineBlock(
        topic="Smart Grid Technologies: AMI and Demand Response",
        keywords=["smart grid", "AMI", "advanced metering infrastructure", "demand response", "distributed generation", "microgrid", "grid modernization", "cybersecurity"],
        conclusion_template=(
            "Advanced Metering Infrastructure (AMI) and demand response programs enable dynamic grid management, improving reliability, efficiency, and integration of distributed energy resources."
        ),
        reasoning_framework=(
            "Smart grid technologies integrate digital communication and control systems into the electric grid to enhance monitoring, automation, and customer engagement. "
            "Advanced Metering Infrastructure (AMI) provides real-time or near-real-time data on electricity consumption, enabling time-of-use pricing and detailed load analysis. "
            "Demand response programs incentivize consumers to reduce or shift load during peak periods, enhancing grid flexibility and reducing the need for peaking generation. "
            "Distributed generation (DG), including rooftop solar and small-scale wind, introduces bidirectional power flows and variability requiring advanced control. "
            "Microgrids offer localized control and islanding capabilities to enhance resilience and reliability. "
            "Grid modernization includes deployment of sensors, phasor measurement units (PMUs), and automated switches to improve situational awareness and fault management. "
            "Cybersecurity is critical to protect grid infrastructure from malicious attacks and ensure data privacy. "
            "Standards such as NERC CIP and IEEE 2030 guide smart grid implementation and security. "
            "Interoperability among devices and systems is essential for scalable deployment. "
            "Regulatory frameworks support cost recovery and incentivize smart grid investments."
        ),
        key_factors=[
            "Advanced Metering Infrastructure deployment",
            "Demand response program design and participation",
            "Integration of distributed energy resources",
            "Microgrid control and islanding capabilities",
            "Grid automation and sensor networks",
            "Cybersecurity and data privacy",
            "Standards compliance (NERC CIP, IEEE)",
            "Regulatory and market incentives"
        ],
        primary_authority=[
            "Federal Energy Regulatory Commission (FERC) Orders 745 and 2222",
            "North American Electric Reliability Corporation (NERC) Critical Infrastructure Protection (CIP) Standards",
            "U.S. Department of Energy Smart Grid Investment Grant Program",
            "IEEE Standards Association (IEEE 2030, IEEE 1547)",
            "Smart Electric Power Alliance (SEPA) Reports"
        ],
        burden_holder="Utility operator and grid planner",
        adversary_position="Concerns about privacy, cybersecurity risks, and cost recovery challenges",
        counter_arguments=[
            "Robust cybersecurity frameworks mitigate risks",
            "Privacy protections and opt-in programs address consumer concerns",
            "Cost-benefit analyses demonstrate long-term savings",
            "Regulatory mechanisms enable fair cost recovery",
            "Pilot programs validate technology and market models"
        ],
        resolution_strategy=(
            "Implement layered cybersecurity defenses, engage stakeholders on privacy, "
            "and develop transparent regulatory frameworks supporting smart grid investments."
        ),
        entity_scope="Electric utilities and grid operators implementing smart grid technologies",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FERC Order No. 2222 on DER Participation in Wholesale Markets"
    ),

    DoctrineBlock(
        topic="ERCOT and NERC Reliability Standards Enforcement",
        keywords=["ERCOT", "NERC", "reliability standards", "interconnection", "compliance", "audit", "grid security", "performance metrics"],
        conclusion_template=(
            "Compliance with NERC reliability standards within ERCOT ensures grid security and operational reliability through rigorous audits and enforcement mechanisms."
        ),
        reasoning_framework=(
            "The Electric Reliability Council of Texas (ERCOT) operates an independent grid with oversight from the North American Electric Reliability Corporation (NERC). "
            "NERC develops and enforces reliability standards covering generation, transmission, and distribution to ensure grid security and prevent blackouts. "
            "Standards address critical areas such as resource adequacy, cyber and physical security, operational planning, and emergency preparedness. "
            "ERCOT entities are subject to compliance audits, self-reporting, and mitigation plans for violations. "
            "Interconnection requirements ensure that new generation and transmission assets meet technical and operational criteria before joining the grid. "
            "Performance metrics such as Loss of Load Expectation (LOLE) and Frequency Response Obligation (FRO) are monitored to assess reliability. "
            "NERC’s Critical Infrastructure Protection (CIP) standards mandate cybersecurity controls for bulk electric system assets. "
            "Enforcement actions include fines, directives, and corrective action plans. "
            "ERCOT’s unique market structure requires coordination between market participants and reliability coordinators. "
            "Continuous improvement processes incorporate lessons learned from events such as the 2021 Texas power crisis."
        ),
        key_factors=[
            "NERC reliability standard compliance",
            "ERCOT interconnection and market rules",
            "Audit and enforcement procedures",
            "Cybersecurity and physical security controls",
            "Performance and reliability metrics",
            "Emergency preparedness and response",
            "Market participant coordination",
            "Continuous improvement and lessons learned"
        ],
        primary_authority=[
            "North American Electric Reliability Corporation (NERC) Reliability Standards",
            "Electric Reliability Council of Texas (ERCOT) Protocols",
            "Federal Energy Regulatory Commission (FERC) Oversight",
            "Texas Public Utility Commission (PUC) Regulations",
            "NERC Compliance Monitoring and Enforcement Program"
        ],
        burden_holder="ERCOT market participants and transmission operators",
        adversary_position="Claims of inadequate enforcement and insufficient grid resilience",
        counter_arguments=[
            "Robust compliance programs and audits enforce standards",
            "ERCOT has implemented reforms post-2021 crisis",
            "Cybersecurity standards reduce vulnerability",
            "Market mechanisms incentivize reliability investments",
            "Stakeholder engagement improves transparency"
        ],
        resolution_strategy=(
            "Strengthen compliance monitoring, enhance emergency protocols, "
            "and foster collaboration among ERCOT, NERC, and market participants."
        ),
        entity_scope="ERCOT grid and market participants subject to NERC standards",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="NERC Enforcement Actions and FERC Orders on ERCOT Reliability"
    ),

    DoctrineBlock(
        topic="Power Purchase Agreements (PPA) and Renewable Energy Credits (REC)",
        keywords=["power purchase agreement", "PPA", "renewable energy credit", "REC", "contract", "renewable energy", "financial structuring", "offtake"],
        conclusion_template=(
            "Power Purchase Agreements (PPAs) provide contractual frameworks for renewable energy offtake, with Renewable Energy Credits (RECs) enabling environmental attribute trading."
        ),
        reasoning_framework=(
            "PPAs are long-term contracts between energy producers and purchasers specifying terms for electricity sale, pricing, delivery, and risk allocation. "
            "They enable project financing by providing revenue certainty. "
            "Renewable Energy Credits (RECs) represent the environmental attributes of renewable generation, tradable separately from physical electricity. "
            "RECs support compliance with Renewable Portfolio Standards (RPS) and voluntary green power markets. "
            "Contract terms address pricing structures such as fixed, indexed, or escalating rates, and may include capacity, energy, and ancillary service components. "
            "Creditworthiness of counterparties and contract enforceability affect project bankability. "
            "Legal considerations include jurisdiction, dispute resolution, and force majeure clauses. "
            "PPAs may be physical (delivery of electricity) or virtual (financial settlement). "
            "Regulatory frameworks govern REC certification, tracking, and retirement to prevent double counting. "
            "Market dynamics and policy incentives influence PPA pricing and REC values."
        ),
        key_factors=[
            "Contract terms and pricing structures",
            "REC certification and tracking",
            "Credit risk and counterparty reliability",
            "Regulatory compliance and RPS requirements",
            "Contract enforceability and dispute resolution",
            "Physical vs virtual PPA distinctions",
            "Market and policy influences",
            "Financial modeling and risk allocation"
        ],
        primary_authority=[
            "Federal Energy Regulatory Commission (FERC) PPA Guidelines",
            "Center for Resource Solutions Green-e Certification Standards",
            "State Renewable Portfolio Standard (RPS) Programs",
            "International Renewable Energy Agency (IRENA) PPA Reports",
            "National Renewable Energy Laboratory (NREL) PPA Model Contracts"
        ],
        burden_holder="Renewable energy project developer and offtaker",
        adversary_position="Concerns about contract inflexibility and REC market volatility",
        counter_arguments=[
            "Contract customization addresses project and purchaser needs",
            "REC markets provide liquidity and price discovery",
            "Risk mitigation strategies include credit support and insurance",
            "Regulatory oversight ensures REC market integrity",
            "Virtual PPAs enable offsite renewable procurement"
        ],
        resolution_strategy=(
            "Develop balanced contract terms, engage in transparent REC markets, "
            "and implement risk management practices."
        ),
        entity_scope="Renewable energy project financing and power procurement",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FERC Orders on PPA Market Participation and REC Trading"
    ),

    DoctrineBlock(
        topic="Transmission and Distribution: HVDC and FACTS Technologies",
        keywords=["transmission", "distribution", "HVDC", "FACTS", "transformer protection", "power flow control", "grid stability", "reactive power"],
        conclusion_template=(
            "High Voltage Direct Current (HVDC) and Flexible AC Transmission Systems (FACTS) enhance grid capacity, stability, and controllability, improving power flow and reducing congestion."
        ),
        reasoning_framework=(
            "HVDC transmission enables efficient long-distance power transfer with lower losses and controllability compared to AC systems. "
            "HVDC links facilitate asynchronous interconnections and integration of remote renewable resources. "
            "Converter stations employing Voltage Source Converters (VSC) or Line Commutated Converters (LCC) convert between AC and DC. "
            "FACTS devices such as Static Var Compensators (SVC), Static Synchronous Compensators (STATCOM), and Unified Power Flow Controllers (UPFC) provide dynamic reactive power support and voltage regulation. "
            "These technologies improve power quality, reduce transmission bottlenecks, and enhance system stability. "
            "Transformer protection schemes detect faults and isolate equipment to prevent damage and outages. "
            "Integration of HVDC and FACTS requires sophisticated control and communication systems. "
            "Grid codes specify performance requirements for these technologies. "
            "Economic considerations include capital costs, operational savings, and deferred infrastructure upgrades. "
            "Environmental benefits arise from enabling renewable integration and reducing transmission losses."
        ),
        key_factors=[
            "HVDC converter technology and control",
            "FACTS device types and applications",
            "Transformer protection and fault detection",
            "Power flow and voltage regulation",
            "Grid code compliance",
            "Integration with existing AC infrastructure",
            "Cost-benefit analysis",
            "Renewable energy integration support"
        ],
        primary_authority=[
            "IEEE Power & Energy Society Standards",
            "International Council on Large Electric Systems (CIGRE) Technical Brochures",
            "U.S. Department of Energy Transmission Reliability Program",
            "Federal Energy Regulatory Commission (FERC) Grid Modernization Policies",
            "Electric Power Research Institute (EPRI) FACTS and HVDC Reports"
        ],
        burden_holder="Transmission system operator and equipment manufacturer",
        adversary_position="Concerns about high capital costs and operational complexity",
        counter_arguments=[
            "Long-term operational savings justify initial investments",
            "Advanced controls simplify operation and enhance reliability",
            "Enabling renewable integration reduces carbon footprint",
            "Grid codes and standards ensure interoperability",
            "Pilot projects demonstrate technical and economic viability"
        ],
        resolution_strategy=(
            "Perform detailed techno-economic studies, adopt modular deployment, "
            "and provide operator training and advanced control systems."
        ),
        entity_scope="High voltage transmission and distribution systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FERC Orders on Transmission Planning and Cost Recovery"
    ),

    DoctrineBlock(
        topic="Energy Policy: FERC and State Public Utility Commission (PUC) Rate Design",
        keywords=["energy policy", "FERC", "PUC", "rate design", "regulation", "cost allocation", "demand charges", "time-of-use pricing"],
        conclusion_template=(
            "Energy rate design regulated by FERC and state PUCs balances cost recovery, fairness, and efficiency, incorporating demand charges and time-of-use pricing to reflect grid costs."
        ),
        reasoning_framework=(
            "Federal Energy Regulatory Commission (FERC) regulates wholesale electricity markets and interstate transmission, while state Public Utility Commissions (PUCs) oversee retail rates and local distribution. "
            "Rate design aims to allocate costs equitably among customers, incentivize efficient usage, and support grid reliability. "
            "Traditional volumetric rates based on energy consumption are supplemented by demand charges reflecting peak capacity requirements. "
            "Time-of-use (TOU) pricing encourages load shifting to off-peak periods, reducing system stress and enabling renewable integration. "
            "Cost-of-service studies inform rate components, including fixed charges, variable energy rates, and demand-related costs. "
            "Decoupling mechanisms separate utility revenue from sales volume to promote energy efficiency. "
            "Regulatory proceedings involve stakeholder input, evidentiary hearings, and economic modeling. "
            "Emerging rate designs address distributed energy resources (DERs) and net metering impacts. "
            "FERC Orders 745 and 841 influence demand response and storage participation in markets. "
            "Balancing affordability, environmental goals, and utility financial health is a key policy challenge."
        ),
        key_factors=[
            "Federal and state regulatory jurisdiction",
            "Cost-of-service and rate design principles",
            "Demand charges and peak pricing",
            "Time-of-use and dynamic pricing",
            "Decoupling and performance incentives",
            "DER and net metering considerations",
            "Stakeholder engagement and transparency",
            "Economic and environmental policy objectives"
        ],
        primary_authority=[
            "Federal Energy Regulatory Commission (FERC) Orders 745, 841, 2222",
            "State Public Utility Commission Rate Cases and Decisions",
            "National Association of Regulatory Utility Commissioners (NARUC) Guidelines",
            "U.S. Department of Energy Office of Electricity Policy Reports",
            "Electric Power Research Institute (EPRI) Rate Design Studies"
        ],
        burden_holder="Utilities and regulatory commissions",
        adversary_position="Claims that complex rate designs increase customer confusion and costs",
        counter_arguments=[
            "Education and outreach improve customer understanding",
            "Advanced metering enables accurate billing and feedback",
            "Dynamic pricing reflects true system costs and benefits",
            "Stakeholder processes ensure balanced outcomes",
            "Technological tools facilitate rate implementation"
        ],
        resolution_strategy=(
            "Develop transparent, data-driven rate designs with stakeholder input, "
            "pilot innovative pricing models, and provide consumer education."
        ),
        entity_scope="Electric utilities and regulatory bodies in U.S. jurisdictions",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="FERC and State PUC Rate Design Proceedings"
    ),

    DoctrineBlock(
        topic="Carbon Market Mechanisms: Emissions Trading and Carbon Tax",
        keywords=["carbon market", "emissions trading", "cap-and-trade", "carbon tax", "greenhouse gases", "market-based regulation", "offsets", "compliance"],
        conclusion_template=(
            "Market-based carbon regulation through emissions trading systems and carbon taxes incentivizes greenhouse gas reductions cost-effectively, supporting climate policy goals."
        ),
        reasoning_framework=(
            "Emissions trading systems (ETS), or cap-and-trade programs, set a limit (cap) on total allowable emissions and allocate or auction emission allowances to regulated entities. "
            "Entities can trade allowances, creating financial incentives to reduce emissions below allocated levels. "
            "Carbon taxes impose a direct price on carbon emissions, providing price certainty but not emissions certainty. "
            "Both mechanisms aim to internalize the social cost of carbon, encouraging low-carbon technologies and operational changes. "
            "Offsets allow entities to meet obligations by financing emission reductions outside the capped sector, subject to rigorous verification. "
            "Market design elements include allowance allocation methods, banking and borrowing provisions, and price floors or ceilings. "
            "Compliance monitoring, reporting, and verification (MRV) ensure program integrity. "
            "Economic modeling assesses impacts on emissions, costs, and competitiveness. "
            "Linking regional or national carbon markets enhances liquidity and cost-effectiveness. "
            "Legal frameworks establish authority, enforcement, and dispute resolution."
        ),
        key_factors=[
            "Cap setting and allowance allocation",
            "Allowance trading and market liquidity",
            "Carbon tax rate and coverage",
            "Offset project standards and verification",
            "MRV protocols and enforcement",
            "Economic and environmental impact analysis",
            "Market linkage and harmonization",
            "Legal and regulatory frameworks"
        ],
        primary_authority=[
            "California Cap-and-Trade Program (California Air Resources Board)",
            "European Union Emissions Trading System (EU ETS)",
            "Regional Greenhouse Gas Initiative (RGGI)",
            "U.S. Environmental Protection Agency (EPA) Greenhouse Gas Reporting Program",
            "World Bank Carbon Pricing Dashboard"
        ],
        burden_holder="Regulated emitters and market participants",
        adversary_position="Concerns about market volatility, leakage, and economic impacts",
        counter_arguments=[
            "Market design features mitigate price volatility",
            "Border adjustments reduce leakage risks",
            "Revenue recycling supports economic transition",
            "Transparent MRV ensures environmental integrity",
            "Complementary policies enhance effectiveness"
        ],
        resolution_strategy=(
            "Implement robust market design, enforce compliance rigorously, "
            "and engage stakeholders to balance environmental and economic objectives."
        ),
        entity_scope="Jurisdictions implementing carbon pricing mechanisms",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="California v. EPA and EU ETS Legal Frameworks"
    ),

    DoctrineBlock(
        topic="Electric Vehicle Charging Infrastructure and Vehicle-to-Grid (V2G)",
        keywords=["electric vehicle", "charging infrastructure", "V2G", "battery swapping", "smart charging", "grid integration", "demand management", "standards"],
        conclusion_template=(
            "Developing robust EV charging infrastructure with vehicle-to-grid capabilities enables grid support services and facilitates widespread EV adoption."
        ),
        reasoning_framework=(
            "Electric vehicle (EV) charging infrastructure includes Level 1 (120V), Level 2 (240V), and DC fast charging stations, each with different power levels and use cases. "
            "Smart charging manages charging times and rates to optimize grid impacts and reduce costs. "
            "Vehicle-to-Grid (V2G) technology enables bidirectional power flow, allowing EVs to discharge electricity back to the grid during peak demand or emergencies. "
            "Battery swapping offers rapid energy replenishment by exchanging depleted batteries with charged units, reducing downtime. "
            "Standards such as SAE J1772 and CHAdeMO govern charging connectors and communication protocols. "
            "Grid integration requires coordination with distribution system operators to manage load and maintain power quality. "
            "Cybersecurity and data privacy are critical for communication and control systems. "
            "Economic models evaluate infrastructure investment, operational costs, and revenue streams from grid services. "
            "Policy incentives and building codes promote infrastructure deployment. "
            "User acceptance and interoperability influence technology adoption."
        ),
        key_factors=[
            "Charging levels and power ratings",
            "Smart charging and load management",
            "V2G technology and grid services",
            "Battery swapping feasibility",
            "Standards and interoperability",
            "Grid integration and impact analysis",
            "Cybersecurity and privacy",
            "Economic and policy incentives"
        ],
        primary_authority=[
            "U.S. Department of Energy Vehicle Technologies Office",
            "Society of Automotive Engineers (SAE) Charging Standards",
            "International Electrotechnical Commission (IEC) 61851 and 62196",
            "California Air Resources Board (CARB) EV Infrastructure Programs",
            "National Renewable Energy Laboratory (NREL) EV Studies"
        ],
        burden_holder="EV infrastructure developers and utility operators",
        adversary_position="Concerns about grid impacts and high infrastructure costs",
        counter_arguments=[
            "Smart charging mitigates grid stress",
            "V2G provides ancillary services and revenue",
            "Policy incentives reduce financial barriers",
            "Standardization enhances interoperability",
            "User education promotes adoption"
        ],
        resolution_strategy=(
            "Deploy interoperable infrastructure with smart controls, "
            "engage utilities and regulators, and educate consumers."
        ),
        entity_scope="Electric vehicle charging networks and grid operators",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="FERC Orders on Demand Response and DER Integration"
    ),

    DoctrineBlock(
        topic="Thermal Energy: Combined Heat and Power (CHP) and District Heating",
        keywords=["thermal energy", "combined heat and power", "CHP", "district heating", "cogeneration", "efficiency", "waste heat recovery", "distributed energy"],
        conclusion_template=(
            "Combined Heat and Power (CHP) systems and district heating networks improve overall energy efficiency by utilizing waste heat for thermal applications."
        ),
        reasoning_framework=(
            "CHP systems simultaneously generate electricity and useful thermal energy from a single fuel source, achieving overall efficiencies of 60-80%, compared to separate generation. "
            "Common CHP technologies include gas turbines, reciprocating engines, and fuel cells. "
            "Waste heat recovery captures thermal energy from exhaust gases or cooling systems for space heating, industrial processes, or absorption chilling. "
            "District heating distributes thermal energy via insulated pipelines to multiple buildings or facilities, enabling centralized generation and load diversity benefits. "
            "System design considers thermal load profiles, distribution losses, and control strategies. "
            "Integration with renewable thermal sources and thermal storage enhances flexibility. "
            "Environmental benefits include reduced greenhouse gas emissions and fossil fuel consumption. "
            "Economic viability depends on fuel costs, capital investment, and thermal demand density. "
            "Regulatory frameworks may incentivize CHP deployment through tax credits and emissions standards. "
            "Operational challenges include maintenance of thermal networks and coordination with electrical generation."
        ),
        key_factors=[
            "CHP technology selection and efficiency",
            "Waste heat recovery potential",
            "District heating network design",
            "Thermal load and demand profiles",
            "Integration with renewable thermal sources",
            "Economic and environmental benefits",
            "Regulatory incentives",
            "Operation and maintenance requirements"
        ],
        primary_authority=[
            "U.S. Department of Energy CHP Technical Assistance Partnerships",
            "International Energy Agency (IEA) CHP and District Heating Reports",
            "American Society of Heating, Refrigerating and Air-Conditioning Engineers (ASHRAE) Guidelines",
            "Environmental Protection Agency (EPA) CHP Partnership",
            "European Union Energy Efficiency Directive"
        ],
        burden_holder="CHP system developers and district heating operators",
        adversary_position="Concerns about high capital costs and infrastructure complexity",
        counter_arguments=[
            "Lifecycle cost savings and efficiency gains justify investments",
            "Modular and scalable designs reduce complexity",
            "Policy incentives support deployment",
            "Environmental benefits align with climate goals",
            "Operational experience improves reliability"
        ],
        resolution_strategy=(
            "Conduct detailed feasibility studies, leverage incentives, "
            "and implement robust operation and maintenance programs."
        ),
        entity_scope="Industrial, commercial, and municipal CHP and district heating systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="EPA CHP Partnership Success Cases and Regulatory Incentive Programs"
    ),

    DoctrineBlock(
        topic="Nuclear Waste Storage: Yucca Mountain and Dry Cask Storage",
        keywords=["nuclear waste", "Yucca Mountain", "dry cask storage", "spent fuel", "repository", "radioactive decay", "containment", "regulatory compliance"],
        conclusion_template=(
            "Long-term nuclear waste management employs geological repositories like Yucca Mountain and interim dry cask storage, ensuring containment and environmental protection."
        ),
        reasoning_framework=(
            "Spent nuclear fuel remains highly radioactive and thermally hot, requiring secure storage for thousands of years. "
            "Yucca Mountain was designated as the U.S. geological repository site, designed to isolate waste in stable volcanic tuff formations. "
            "The repository design includes multiple engineered barriers such as waste canisters, backfill materials, and natural geological isolation. "
            "Political, legal, and social challenges have delayed Yucca Mountain's development. "
            "Dry cask storage provides interim on-site storage by sealing spent fuel assemblies in robust steel and concrete containers, allowing passive cooling. "
            "Dry casks are designed to withstand natural disasters, radiation shielding, and prevent criticality. "
            "Regulatory oversight by the Nuclear Regulatory Commission (NRC) governs storage system design, licensing, and monitoring. "
            "Transportation of spent fuel to repositories involves strict safety protocols and security measures. "
            "Long-term stewardship plans address monitoring, maintenance, and potential retrieval. "
            "International best practices and IAEA guidelines inform repository development and waste management strategies."
        ),
        key_factors=[
            "Radioactive decay and heat generation",
            "Geological repository design and site characteristics",
            "Dry cask storage system integrity",
            "Regulatory licensing and compliance",
            "Transportation safety and security",
            "Political and social acceptance",
            "Long-term monitoring and stewardship",
            "International standards and best practices"
        ],
        primary_authority=[
            "U.S. Nuclear Regulatory Commission (NRC) 10 CFR Part 72 and 63",
            "U.S. Department of Energy Yucca Mountain Project Reports",
            "International Atomic Energy Agency (IAEA) Radioactive Waste Management Standards",
            "Nuclear Waste Policy Act (NWPA) of 1982",
            "National Academy of Sciences Reports on Nuclear Waste Disposal"
        ],
        burden_holder="Nuclear power plant operators and federal waste management agencies",
        adversary_position="Opposition to repository siting and concerns about long-term safety",
        counter_arguments=[
            "Extensive scientific studies support repository safety",
            "Dry cask storage provides safe interim solution",
            "Regulatory frameworks ensure rigorous oversight",
            "International experience validates geological disposal",
            "Stakeholder engagement addresses social concerns"
        ],
        resolution_strategy=(
            "Advance repository licensing, maintain safe interim storage, "
            "and enhance public communication and stakeholder involvement."
        ),
        entity_scope="U.S. nuclear waste management programs and facilities",
        confidence=0.86,
        confidence_zone="Moderate-High",
        controlling_precedent="Nuclear Waste Policy Act and NRC Licensing Decisions"
    ),

    DoctrineBlock(
        topic="Renewable Integration: Curtailment, Duck Curve, and Grid Flexibility",
        keywords=["renewable integration", "curtailment", "duck curve", "ramping", "flexibility", "energy storage", "demand response", "grid balancing"],
        conclusion_template=(
            "Managing renewable energy integration challenges such as curtailment and the duck curve requires enhanced grid flexibility through storage, demand response, and flexible generation."
        ),
        reasoning_framework=(
            "High penetration of variable renewable energy (VRE) such as solar and wind introduces variability and uncertainty in power supply. "
            "Curtailment occurs when generation exceeds demand or grid capacity, leading to wasted renewable energy. "
            "The duck curve illustrates the net load shape with steep ramping requirements in the evening as solar generation declines and demand rises. "
            "Grid flexibility involves the ability to ramp generation up or down quickly, shift loads, and store energy to maintain balance. "
            "Energy storage systems like batteries and pumped hydro provide temporal shifting of energy. "
            "Demand response programs adjust consumption patterns to align with renewable availability. "
            "Flexible natural gas plants and interconnections with neighboring grids enhance dispatchability. "
            "Advanced forecasting improves scheduling and reduces uncertainty. "
            "Market mechanisms incentivize flexibility and penalize inflexibility. "
            "Regulatory and planning frameworks must evolve to accommodate high renewable shares."
        ),
        key_factors=[
            "Renewable generation variability and forecasting",
            "Curtailment causes and mitigation",
            "Load ramping and duck curve dynamics",
            "Energy storage deployment",
            "Demand response participation",
            "Flexible generation assets",
            "Market and regulatory incentives",
            "Grid operational practices"
        ],
        primary_authority=[
            "California Independent System Operator (CAISO) Renewable Integration Studies",
            "National Renewable Energy Laboratory (NREL) Flexibility Reports",
            "Federal Energy Regulatory Commission (FERC) Orders 841 and 2222",
            "Electric Power Research Institute (EPRI) Renewable Integration Reports",
            "International Energy Agency (IEA) Renewables Integration Analysis"
        ],
        burden_holder="Grid operators and renewable energy developers",
        adversary_position="Concerns about reliability and increased costs due to variability",
        counter_arguments=[
            "Technological solutions enhance flexibility and reliability",
            "Market designs reward flexible resources",
            "Storage and demand response reduce curtailment",
            "Interregional coordination improves balancing",
            "Policy support accelerates technology deployment"
        ],
        resolution_strategy=(
            "Invest in flexibility resources, update market rules, "
            "and improve forecasting and grid operations."
        ),
        entity_scope="Electric grids with high renewable energy penetration",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FERC Orders on Energy Storage and DER Participation"
    ),

    DoctrineBlock(
        topic="Energy Economics: Levelized Cost of Energy (LCOE) and Merit Order Dispatch",
        keywords=["energy economics", "LCOE", "capacity factor", "dispatch", "merit order", "cost modeling", "investment analysis", "market pricing"],
        conclusion_template=(
            "Levelized Cost of Energy (LCOE) and merit order dispatch models guide investment and operational decisions by quantifying costs and prioritizing generation resources."
        ),
        reasoning_framework=(
            "LCOE calculates the per-unit cost of building and operating a generating asset over its lifetime, including capital, operational, fuel, and maintenance costs, discounted to present value. "
            "It facilitates comparison across technologies with different cost structures and lifespans. "
            "Capacity factor, the ratio of actual output to maximum possible output, affects LCOE by influencing energy production volume. "
            "Merit order dispatch ranks available generation units by marginal cost, dispatching the lowest cost units first to meet demand. "
            "This economic dispatch minimizes overall system cost and influences market prices. "
            "Market prices may deviate from LCOE due to externalities, subsidies, and operational constraints. "
            "Investment decisions consider LCOE alongside policy incentives, risk, and financing conditions. "
            "Dispatch models incorporate unit commitment, ramping constraints, and reserve requirements. "
            "Dynamic pricing and capacity markets complement energy-only markets to ensure resource adequacy. "
            "Sensitivity analyses assess impacts of fuel price volatility, carbon pricing, and technology learning curves."
        ),
        key_factors=[
            "Capital and operational costs",
            "Capacity factor and utilization",
            "Marginal cost and dispatch order",
            "Market price formation",
            "Policy incentives and subsidies",
            "Risk and financing conditions",
            "Unit commitment and operational constraints",
            "Sensitivity and scenario analysis"
        ],
        primary_authority=[
            "U.S. Energy Information Administration (EIA) Annual Energy Outlook",
            "International Renewable Energy Agency (IRENA) Cost Analysis Reports",
            "Federal Energy Regulatory Commission (FERC) Market Oversight",
            "Electric Power Research Institute (EPRI) Economic Dispatch Studies",
            "National Renewable Energy Laboratory (NREL) LCOE Calculator"
        ],
        burden_holder="Energy market participants and regulators",
        adversary_position="Claims that LCOE oversimplifies cost comparisons and market dynamics",
        counter_arguments=[
            "LCOE is a standardized metric widely used for initial screening",
            "Complementary analyses address operational and market complexities",
            "Merit order dispatch reflects real-time operational economics",
            "Policy and market design account for externalities",
            "Advanced models incorporate uncertainty and risk"
        ],
        resolution_strategy=(
            "Use LCOE alongside comprehensive market and operational models, "
            "and incorporate policy and risk factors in decision-making."
        ),
        entity_scope="Electricity generation investment and market operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FERC Market Design and Oversight Proceedings"
    ),

    DoctrineBlock(
        topic="Grid Resilience: Cybersecurity and Physical Security",
        keywords=["grid resilience", "cybersecurity", "physical security", "threat detection", "incident response", "NERC CIP", "critical infrastructure", "risk management"],
        conclusion_template=(
            "Ensuring grid resilience requires integrated cybersecurity and physical security measures, guided by NERC CIP standards and risk management frameworks."
        ),
        reasoning_framework=(
            "Grid resilience encompasses the ability to anticipate, withstand, and recover from disruptions, including cyber attacks and physical threats. "
            "Cybersecurity protects control systems, communication networks, and data integrity from unauthorized access, malware, and denial-of-service attacks. "
            "Physical security safeguards critical assets such as substations, control centers, and transmission lines against sabotage and natural disasters. "
            "NERC Critical Infrastructure Protection (CIP) standards establish mandatory requirements for cybersecurity controls, access management, and incident reporting. "
            "Risk assessments identify vulnerabilities and prioritize mitigation efforts. "
            "Threat detection employs intrusion detection systems, anomaly monitoring, and threat intelligence sharing. "
            "Incident response plans coordinate actions to contain, eradicate, and recover from security events. "
            "Training and awareness programs enhance personnel readiness. "
            "Coordination with law enforcement and government agencies supports threat response. "
            "Continuous improvement incorporates lessons learned and evolving threat landscapes."
        ),
        key_factors=[
            "Cybersecurity controls and monitoring",
            "Physical security measures",
            "NERC CIP compliance",
            "Risk assessment and mitigation",
            "Threat detection and intelligence",
            "Incident response planning",
            "Training and awareness",
            "Interagency coordination"
        ],
        primary_authority=[
            "North American Electric Reliability Corporation (NERC) CIP Standards",
            "Department of Homeland Security (DHS) Cybersecurity Framework",
            "Federal Energy Regulatory Commission (FERC) Security Regulations",
            "National Institute of Standards and Technology (NIST) SP 800-82 Guide",
            "Electricity Information Sharing and Analysis Center (E-ISAC)"
        ],
        burden_holder="Grid operators and asset owners",
        adversary_position="Current security measures are adequate and additional investment is unnecessary.",
        counter_arguments=[
            "Evolving cyber threats require continuous security improvements",
            "NERC CIP compliance is mandatory, not optional",
            "Physical security incidents can cascade into widespread outages",
            "Threat intelligence sharing reveals new attack vectors",
            "Regulatory penalties for non-compliance are significant"
        ],
        resolution_strategy="Implement NERC CIP standards comprehensively; conduct regular risk assessments; maintain robust incident response capability.",
        entity_scope="Grid operators, asset owners, regulators, and security personnel",
        confidence=0.91,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="NERC CIP Standards v5/v7"
    ),
]

# =============================================
# SUB-ENGINE ORCHESTRATION
# =============================================

class SubEngineState(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    OFFLINE = auto()

class CircuitBreakerState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class IssueCategory(Enum):
    NUCLEAR = 'nuclear'
    SOLAR = 'solar'
    WIND = 'wind'
    HYDRO = 'hydro'
    GRID = 'grid'
    STORAGE = 'storage'
    GEOTHERMAL = 'geothermal'
    HYDROGEN = 'hydrogen'
    GAS = 'gas'
    COAL = 'coal'
    BIO = 'bio'
    OCEAN = 'ocean'
    EFFICIENCY = 'efficiency'
    SMARTGRID = 'smartgrid'
    GENERAL = 'general'

class SubEngineStatus:
    def __init__(self, engine_id: str, state: SubEngineState, last_checked: float, latency: float = None, error: str = None):
        self.engine_id = engine_id
        self.state = state
        self.last_checked = last_checked
        self.latency = latency
        self.error = error

    def to_dict(self):
        return {
            "engine_id": self.engine_id,
            "state": self.state.name,
            "last_checked": self.last_checked,
            "latency": self.latency,
            "error": self.error
        }

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, categories: Set[IssueCategory], weight: float = 1.0):
        self.engine_id = engine_id
        self.url = url
        self.categories = categories
        self.weight = weight

class QueryRequest:
    def __init__(self, text: str, mode: str = "default", metadata: Dict[str, Any] = None):
        self.text = text
        self.mode = mode
        self.metadata = metadata or {}

class RoutingDecision:
    def __init__(self, engine_ids: List[str], rationale: str, categories: List[IssueCategory]):
        self.engine_ids = engine_ids
        self.rationale = rationale
        self.categories = categories

class SubEngineResponse:
    def __init__(self, engine_id: str, response: Any, success: bool, latency: float, error: Optional[str] = None):
        self.engine_id = engine_id
        self.response = response
        self.success = success
        self.latency = latency
        self.error = error

# --- SubEngine Registry ---

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "ENRG01": SubEngineConfig("ENRG01", "http://enrg01-nuclear/api/query", {IssueCategory.NUCLEAR}),
    "ENRG02": SubEngineConfig("ENRG02", "http://enrg02-solar/api/query", {IssueCategory.SOLAR}),
    "ENRG03": SubEngineConfig("ENRG03", "http://enrg03-wind/api/query", {IssueCategory.WIND}),
    "ENRG04": SubEngineConfig("ENRG04", "http://enrg04-hydro/api/query", {IssueCategory.HYDRO}),
    "ENRG05": SubEngineConfig("ENRG05", "http://enrg05-grid/api/query", {IssueCategory.GRID, IssueCategory.SMARTGRID}),
    "ENRG06": SubEngineConfig("ENRG06", "http://enrg06-storage/api/query", {IssueCategory.STORAGE}),
    "ENRG07": SubEngineConfig("ENRG07", "http://enrg07-geothermal/api/query", {IssueCategory.GEOTHERMAL}),
    "ENRG08": SubEngineConfig("ENRG08", "http://enrg08-hydrogen/api/query", {IssueCategory.HYDROGEN}),
    "ENRG09": SubEngineConfig("ENRG09", "http://enrg09-gas/api/query", {IssueCategory.GAS}),
    "ENRG10": SubEngineConfig("ENRG10", "http://enrg10-coal/api/query", {IssueCategory.COAL}),
    "ENRG11": SubEngineConfig("ENRG11", "http://enrg11-bio/api/query", {IssueCategory.BIO}),
    "ENRG12": SubEngineConfig("ENRG12", "http://enrg12-ocean/api/query", {IssueCategory.OCEAN}),
    "ENRG13": SubEngineConfig("ENRG13", "http://enrg13-efficiency/api/query", {IssueCategory.EFFICIENCY}),
    "ENRG14": SubEngineConfig("ENRG14", "http://enrg14-smartgrid/api/query", {IssueCategory.SMARTGRID, IssueCategory.GRID}),
}

# --- Circuit Breaker ---

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = 0

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
            return False
        elif self.state == CircuitBreakerState.HALF_OPEN:
            return True
        return False

    def __repr__(self):
        return f"<CircuitBreaker state={self.state} failures={self.failure_count}>"

# --- SubEngineHealthMonitor ---

class SubEngineHealthMonitor:
    def __init__(self, registry: Dict[str, SubEngineConfig], ttl: int = 30):
        self.registry = registry
        self.ttl = ttl
        self._health_cache: Dict[str, Tuple[SubEngineStatus, float]] = {}
        self._circuit_breakers: Dict[str, CircuitBreaker] = {eid: CircuitBreaker() for eid in registry}

    async def _ping_engine(self, url: str, timeout: int = 3) -> Tuple[bool, float, Optional[str]]:
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url + "/health", timeout=timeout) as resp:
                    if resp.status == 200:
                        latency = time.time() - start
                        return True, latency, None
                    else:
                        latency = time.time() - start
                        return False, latency, f"Status {resp.status}"
        except Exception as e:
            latency = time.time() - start
            return False, latency, str(e)

    async def check_health(self, engine_id: str) -> SubEngineStatus:
        now = time.time()
        if engine_id in self._health_cache:
            status, ts = self._health_cache[engine_id]
            if now - ts < self.ttl:
                return status
        config = self.registry.get(engine_id)
        if not config:
            status = SubEngineStatus(engine_id, SubEngineState.OFFLINE, now, error="Not registered")
            self._health_cache[engine_id] = (status, now)
            return status
        cb = self._circuit_breakers[engine_id]
        if not cb.can_attempt():
            status = SubEngineStatus(engine_id, SubEngineState.UNHEALTHY, now, error="Circuit open")
            self._health_cache[engine_id] = (status, now)
            return status
        healthy, latency, error = await self._ping_engine(config.url)
        if healthy:
            cb.record_success()
            state = SubEngineState.HEALTHY
        else:
            cb.record_failure()
            state = SubEngineState.UNHEALTHY if cb.state == CircuitBreakerState.OPEN else SubEngineState.DEGRADED
        status = SubEngineStatus(engine_id, state, now, latency, error)
        self._health_cache[engine_id] = (status, now)
        return status

    async def check_all_health(self) -> Dict[str, SubEngineStatus]:
        results = {}
        tasks = []
        for eid in self.registry:
            tasks.append(self.check_health(eid))
        statuses = await asyncio.gather(*tasks)
        for status in statuses:
            results[status.engine_id] = status
        return results

    def get_healthy_engines(self) -> List[str]:
        now = time.time()
        healthy = []
        for eid, (status, ts) in self._health_cache.items():
            if now - ts < self.ttl and status.state == SubEngineState.HEALTHY:
                healthy.append(eid)
        return healthy

    def get_circuit_breaker(self, engine_id: str) -> CircuitBreaker:
        return self._circuit_breakers[engine_id]

# --- QueryRouter ---

class QueryRouter:
    CATEGORY_KEYWORDS = {
        IssueCategory.NUCLEAR: {'nuclear', 'fission', 'fusion', 'uranium', 'reactor', 'plutonium', 'isotope'},
        IssueCategory.SOLAR: {'solar', 'photovoltaic', 'pv', 'sunlight', 'sun', 'panel', 'inverter'},
        IssueCategory.WIND: {'wind', 'turbine', 'blade', 'anemometer', 'offshore', 'onshore'},
        IssueCategory.HYDRO: {'hydro', 'dam', 'hydroelectric', 'water', 'turbine', 'reservoir'},
        IssueCategory.GRID: {'grid', 'transmission', 'distribution', 'frequency', 'voltage', 'dispatch'},
        IssueCategory.STORAGE: {'storage', 'battery', 'lithium', 'flow', 'supercapacitor', 'energy storage'},
        IssueCategory.GEOTHERMAL: {'geothermal', 'magma', 'heat pump', 'earth heat'},
        IssueCategory.HYDROGEN: {'hydrogen', 'electrolyzer', 'fuel cell', 'h2', 'power-to-gas'},
        IssueCategory.GAS: {'gas', 'natural gas', 'methane', 'lng', 'pipeline', 'cng'},
        IssueCategory.COAL: {'coal', 'lignite', 'anthracite', 'carbon capture', 'ccs'},
        IssueCategory.BIO: {'bio', 'biomass', 'biofuel', 'ethanol', 'biodiesel', 'anaerobic'},
        IssueCategory.OCEAN: {'ocean', 'tidal', 'wave', 'current', 'salinity', 'marine energy'},
        IssueCategory.EFFICIENCY: {'efficiency', 'demand response', 'conservation', 'retrofit', 'energy saving'},
        IssueCategory.SMARTGRID: {'smart grid', 'demand response', 'iot', 'smart meter', 'automation', 'synchrophasor'},
    }

    def __init__(self, registry: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.registry = registry
        self.health_monitor = health_monitor

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text_l = text.lower()
        found = set()
        for cat, keywords in self.CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in text_l:
                    found.add(cat)
        if not found:
            found.add(IssueCategory.GENERAL)
        return list(found)

    def _select_engines(self, categories: List[IssueCategory], mode: str = "default") -> List[SubEngineConfig]:
        healthy_ids = set(self.health_monitor.get_healthy_engines())
        selected = []
        for eid, config in self.registry.items():
            if eid not in healthy_ids:
                continue
            if IssueCategory.GENERAL in categories:
                selected.append(config)
            elif config.categories.intersection(categories):
                selected.append(config)
        if not selected and categories == [IssueCategory.GENERAL]:
            # fallback: pick all healthy
            for eid in healthy_ids:
                selected.append(self.registry[eid])
        return selected

    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        # Example: if query is urgent, route to grid and storage
        if query.metadata.get("priority") == "urgent":
            return ["ENRG05", "ENRG06"]
        return []

    def _score_engine_relevance(self, engine: SubEngineConfig, query: QueryRequest) -> float:
        categories = self._classify_domain(query.text)
        overlap = len(engine.categories.intersection(categories))
        base = 1.0 if overlap else 0.1
        # Add more sophisticated scoring here
        return base * engine.weight

    def _handle_engine_failure(self, engine_id: str, error: str) -> List[str]:
        # Fallback: if grid fails, try smartgrid; if solar fails, try storage
        if engine_id == "ENRG05":
            return ["ENRG14"]
        if engine_id == "ENRG02":
            return ["ENRG06"]
        return []

    def route_query(self, query: QueryRequest) -> RoutingDecision:
        categories = self._classify_domain(query.text)
        rule_engines = self._apply_routing_rules(query)
        rationale = ""
        if rule_engines:
            rationale = "Routing by explicit rule"
            return RoutingDecision(rule_engines, rationale, categories)
        selected = self._select_engines(categories, query.mode)
        if not selected:
            rationale = "No healthy engines for categories; fallback to all healthy"
            selected = [self.registry[eid] for eid in self.health_monitor.get_healthy_engines()]
        else:
            rationale = f"Selected by category: {', '.join([c.name for c in categories])}"
        engine_ids = [e.engine_id for e in selected]
        return RoutingDecision(engine_ids, rationale, categories)

# --- SubEngineOrchestrator ---

class SubEngineOrchestrator:
    def __init__(self, registry: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.registry = registry
        self.health_monitor = health_monitor

    async def _call_sub_engine(self, engine_config: SubEngineConfig, query: QueryRequest) -> SubEngineResponse:
        cb = self.health_monitor.get_circuit_breaker(engine_config.engine_id)
        if not cb.can_attempt():
            return SubEngineResponse(engine_config.engine_id, None, False, 0.0, error="Circuit open")
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(engine_config.url, json={"query": query.text, "metadata": query.metadata}, timeout=10) as resp:
                    latency = time.time() - start
                    if resp.status == 200:
                        data = await resp.json()
                        cb.record_success()
                        return SubEngineResponse(engine_config.engine_id, data, True, latency)
                    else:
                        cb.record_failure()
                        return SubEngineResponse(engine_config.engine_id, None, False, latency, error=f"Status {resp.status}")
        except Exception as e:
            cb.record_failure()
            latency = time.time() - start
            return SubEngineResponse(engine_config.engine_id, None, False, latency, error=str(e))

    async def dispatch_query(self, query: QueryRequest, engines: List[str]) -> List[SubEngineResponse]:
        tasks = []
        for eid in engines:
            config = self.registry.get(eid)
            if config:
                tasks.append(self._call_sub_engine(config, query))
        return await asyncio.gather(*tasks)

    async def dispatch_parallel(self, query: QueryRequest, engines: List[str]) -> Dict[str, Any]:
        responses = await self.dispatch_query(query, engines)
        return self._merge_responses(responses)

    async def dispatch_cascade(self, query: QueryRequest, engines: List[str]) -> Any:
        for eid in engines:
            config = self.registry.get(eid)
            if not config:
                continue
            resp = await self._call_sub_engine(config, query)
            if resp.success:
                return resp.response
        return {"error": "All engines failed"}

    def _merge_responses(self, responses: List[SubEngineResponse]) -> Dict[str, Any]:
        merged = {}
        for resp in responses:
            merged[resp.engine_id] = {
                "success": resp.success,
                "latency": resp.latency,
                "response": resp.response,
                "error": resp.error
            }
        return merged

    def _resolve_conflicts(self, responses: List[SubEngineResponse]) -> Any:
        # Simple consensus: if all agree, return; else, majority; else, flag conflict
        results = [resp.response for resp in responses if resp.success]
        if not results:
            return {"error": "No successful responses"}
        # For demonstration, assume responses are dicts with a 'result' field
        result_counts = defaultdict(int)
        for r in results:
            key = str(r.get('result')) if isinstance(r, dict) else str(r)
            result_counts[key] += 1
        most_common = max(result_counts.items(), key=lambda x: x[1])
        if most_common[1] == len(results):
            return results[0]
        elif most_common[1] > len(results) // 2:
            # Majority
            for r in results:
                if (isinstance(r, dict) and str(r.get('result')) == most_common[0]) or (str(r) == most_common[0]):
                    return r
        return {"conflict": [r for r in results]}

# --- Example Usage (not executed here) ---

# health_monitor = SubEngineHealthMonitor(SUB_ENGINE_REGISTRY)
# router = QueryRouter(SUB_ENGINE_REGISTRY, health_monitor)
# orchestrator = SubEngineOrchestrator(SUB_ENGINE_REGISTRY, health_monitor)

# async def handle_query(text):
#     query = QueryRequest(text)
#     routing = router.route_query(query)
#     responses = await orchestrator.dispatch_query(query, routing.engine_ids)
#     merged = orchestrator._merge_responses(responses)
#     consensus = orchestrator._resolve_conflicts(responses)
#     return {"routing": routing.rationale, "responses": merged, "consensus": consensus}

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

def resolve_authority_conflict(sources):
    """
    sources: list of tuples (authority_level: AuthorityLevel, source_id: str)
    Returns the dominant authority level and sources that hold it.
    """
    if not sources:
        return None, []
    max_weight = -1
    dominant_level = None
    for level, _ in sources:
        weight = authority_weights.get(level, 0)
        if weight > max_weight:
            max_weight = weight
            dominant_level = level
    dominant_sources = [s for s in sources if s[0] == dominant_level]
    return dominant_level, dominant_sources

# ---------------------------
# EPISTEMIC GUARDRAILS MODULE
# ---------------------------

BANNED_PHRASES = [
    "clearly", "obviously", "without doubt", "undeniably", "unquestionably",
    "beyond question", "incontrovertibly", "manifestly", "patently", "plainly",
    "self-evident", "indisputably", "categorically", "absolutely", "decidedly",
    "conclusively", "irrefutably", "unequivocally", "incontestably", "beyond dispute",
    "without fail", "infallibly", "necessarily", "always", "never",
    "guaranteed", "certainly", "definitely", "invariably", "without exception",
    "undoubtedly", "inarguably", "incontestably", "unfailingly", "invariably"
]

DISCLOSURE_CAVEAT = (
    "Note: This analysis avoids absolute assertions and acknowledges inherent uncertainties."
)

def apply_epistemic_guardrails(text):
    """
    Remove banned phrases from text and append disclosure caveat if any were found.
    """
    pattern = re.compile(r'\b(' + '|'.join(re.escape(p) for p in BANNED_PHRASES) + r')\b', re.IGNORECASE)
    cleaned_text, count = pattern.subn('', text)
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()
    if count > 0:
        cleaned_text += " " + DISCLOSURE_CAVEAT
    return cleaned_text

class ConfidenceLevel(Enum):
    DEFENSIBLE = 1
    AGGRESSIVE = 2
    DISCLOSURE = 3
    HIGH_RISK = 4

def confidence_stratification(confidence_score):
    """
    confidence_score: float between 0 and 1
    Returns ConfidenceLevel based on thresholds.
    """
    if confidence_score >= 0.9:
        return ConfidenceLevel.DEFENSIBLE
    elif confidence_score >= 0.75:
        return ConfidenceLevel.AGGRESSIVE
    elif confidence_score >= 0.5:
        return ConfidenceLevel.DISCLOSURE
    else:
        return ConfidenceLevel.HIGH_RISK

# ---------------------------
# FACT FRAGILITY SCORING MODULE
# ---------------------------

def score_fact_fragility(fact):
    """
    fact: dict with keys 'verifiability', 'recharacterization_risk', 'testimony_dependence'
    Each key expected to be a float between 0 and 1.
    Returns dict of scores and overall fragility score.
    """
    verifiability = fact.get('verifiability', 0.5)
    recharacterization_risk = fact.get('recharacterization_risk', 0.5)
    testimony_dependence = fact.get('testimony_dependence', 0.5)

    # Fragility increases with lower verifiability, higher recharacterization risk, and higher testimony dependence
    fragility_score = (1 - verifiability) * 0.4 + recharacterization_risk * 0.4 + testimony_dependence * 0.2

    return {
        'verifiability': verifiability,
        'recharacterization_risk': recharacterization_risk,
        'testimony_dependence': testimony_dependence,
        'fragility_score': fragility_score
    }

# ---------------------------
# SEMANTIC NORMALIZATION MODULE
# ---------------------------

DOMAIN_TERM_MAPPINGS = {
    # Energy domain terms normalization
    "photovoltaic": "solar_panel",
    "pv": "solar_panel",
    "wind turbine": "wind_turbine",
    "wt": "wind_turbine",
    "natural gas": "natural_gas",
    "ng": "natural_gas",
    "renewable energy": "renewable_energy",
    "renewables": "renewable_energy",
    "electric vehicle": "electric_vehicle",
    "ev": "electric_vehicle",
    "battery storage": "battery_storage",
    "energy storage": "battery_storage",
    "smart grid": "smart_grid",
    "demand response": "demand_response",
    "load shedding": "demand_response",
    "carbon footprint": "carbon_emissions",
    "co2 emissions": "carbon_emissions",
    "greenhouse gas": "carbon_emissions",
    "ghg": "carbon_emissions",
    "distributed generation": "distributed_generation",
    "dg": "distributed_generation",
    "microgrid": "microgrid",
    "net metering": "net_metering",
    "feed-in tariff": "feed_in_tariff",
    "fiT": "feed_in_tariff",
    "power purchase agreement": "ppa",
    "ppa": "ppa",
    "energy efficiency": "energy_efficiency",
    "demand side management": "demand_side_management",
    "dsm": "demand_side_management",
    "capacity market": "capacity_market",
    "ancillary services": "ancillary_services",
    "transmission line": "transmission_line",
    "distribution network": "distribution_network",
    "smart meter": "smart_meter",
    "electricity market": "electricity_market",
    "grid operator": "grid_operator",
    "system operator": "grid_operator",
    "load forecasting": "load_forecasting",
    "renewable portfolio standard": "rps",
    "rps": "rps",
    "carbon tax": "carbon_tax",
    "emission trading system": "ets",
    "cap and trade": "ets",
    "energy audit": "energy_audit",
    "power plant": "power_plant",
    "generation asset": "power_plant",
    "hydroelectric": "hydroelectric",
    "hydro power": "hydroelectric",
    "fuel cell": "fuel_cell",
    "combined heat and power": "chp",
    "cogeneration": "chp",
    "smart inverter": "smart_inverter",
    "grid stability": "grid_stability",
    "load balancing": "load_balancing",
    "peak shaving": "peak_shaving",
    "energy management system": "ems",
    "ems": "ems",
    "distributed energy resource": "der",
    "der": "der",
    "energy market": "energy_market",
    "power quality": "power_quality",
    "black start": "black_start",
    "frequency regulation": "frequency_regulation",
    "voltage regulation": "voltage_regulation",
    "energy arbitrage": "energy_arbitrage",
    "capacity factor": "capacity_factor",
    "interconnection": "interconnection",
    "load factor": "load_factor",
    "peak demand": "peak_demand",
    "net load": "net_load",
    "ancillary service": "ancillary_services",
    "dispatchable generation": "dispatchable_generation",
    "non-dispatchable generation": "non_dispatchable_generation",
    "curtailment": "curtailment",
    "energy transition": "energy_transition",
    "carbon neutrality": "carbon_neutrality",
    "decarbonization": "decarbonization",
    "energy policy": "energy_policy",
    "energy regulation": "energy_regulation",
    "energy security": "energy_security",
    "power outage": "power_outage",
    "load shedding event": "load_shedding",
    "energy consumption": "energy_consumption",
    "energy demand": "energy_demand",
    "energy supply": "energy_supply",
}

def normalize_query(text):
    """
    Normalize domain-specific terms in the input text.
    """
    text_lower = text.lower()
    for term, normalized in DOMAIN_TERM_MAPPINGS.items():
        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
        text_lower = pattern.sub(normalized, text_lower)
    return text_lower

# ---------------------------
# DEEP ANALYSIS MODULE
# ---------------------------

def multi_doctrine_decomposition(query):
    """
    Decompose query into sub-issues based on doctrine keywords.
    Returns list of sub-issues (strings).
    """
    doctrines_keywords = {
        "regulatory compliance": ["regulation", "compliance", "rule", "standard"],
        "environmental impact": ["emission", "pollution", "carbon", "environment"],
        "market analysis": ["market", "price", "demand", "supply", "trading"],
        "technical feasibility": ["technical", "feasibility", "implementation", "capacity"],
        "financial assessment": ["cost", "investment", "financial", "return", "profit"],
        "policy evaluation": ["policy", "legislation", "law", "government"],
        "risk management": ["risk", "uncertainty", "hazard", "mitigation"],
        "operational efficiency": ["operation", "efficiency", "performance", "optimization"],
    }
    query_norm = normalize_query(query)
    sub_issues = []
    for doctrine, keywords in doctrines_keywords.items():
        for kw in keywords:
            if kw in query_norm:
                sub_issues.append(f"{doctrine}: related to {kw}")
                break
    if not sub_issues:
        sub_issues.append("general: broad analysis required")
    return sub_issues

def build_interaction_dag(issues):
    """
    Build a dependency graph (DAG) of issues.
    Returns dict: {issue: [dependent_issues]}
    """
    dag = defaultdict(list)
    # Simple heuristic: policy evaluation depends on regulatory compliance,
    # financial assessment depends on market analysis,
    # operational efficiency depends on technical feasibility
    dependencies = {
        "policy evaluation": ["regulatory compliance"],
        "financial assessment": ["market analysis"],
        "operational efficiency": ["technical feasibility"],
        "risk management": ["financial assessment", "operational efficiency"],
    }
    issue_names = [issue.split(":")[0] for issue in issues]
    for issue in issue_names:
        deps = dependencies.get(issue, [])
        for dep in deps:
            if dep in issue_names:
                dag[dep].append(issue)
        if issue not in dag:
            dag[issue] = []
    return dag

def eight_step_resolution(query, doctrines, sub_engine_results):
    """
    Perform a full eight-step analysis resolution.
    Steps:
    1. Query normalization
    2. Doctrine decomposition
    3. Dependency graph build
    4. Sub-engine dispatch results collection
    5. Conflict resolution among results
    6. Authority hardening application
    7. Epistemic guardrails application
    8. Final conclusion synthesis
    """
    # Step 1: Normalize query
    normalized_query = normalize_query(query)

    # Step 2: Doctrine decomposition (already provided doctrines)
    issues = doctrines

    # Step 3: Build dependency graph
    dag = build_interaction_dag(issues)

    # Step 4: Collect sub-engine results (provided as input)
    # sub_engine_results: dict {issue: analysis_text}

    # Step 5: Conflict resolution - simplistic approach: prefer longer analysis
    resolved_results = {}
    for issue in issues:
        results = sub_engine_results.get(issue, [])
        if not results:
            resolved_results[issue] = "No analysis available."
        elif isinstance(results, list):
            # Pick longest text
            resolved_results[issue] = max(results, key=len)
        else:
            resolved_results[issue] = results

    # Step 6: Authority hardening - find dominant authority among all sources
    all_sources = []
    for issue in issues:
        # Assume sub_engine_results contains tuples (text, [(AuthorityLevel, source_id), ...])
        res = sub_engine_results.get(issue, [])
        if isinstance(res, list):
            for r in res:
                if isinstance(r, tuple) and len(r) == 2:
                    _, sources = r
                    all_sources.extend(sources)
        elif isinstance(res, tuple) and len(res) == 2:
            _, sources = res
            all_sources.extend(sources)
    dominant_level, dominant_sources = resolve_authority_conflict(all_sources)

    # Step 7: Apply epistemic guardrails to each resolved result
    for issue in resolved_results:
        resolved_results[issue] = apply_epistemic_guardrails(resolved_results[issue])

    # Step 8: Final conclusion synthesis - concatenate all with tags
    conclusion_parts = []
    for issue in issues:
        conclusion_parts.append(f"### Issue: {issue}\n{resolved_results.get(issue, '')}\n")
    conclusion = "\n".join(conclusion_parts)
    conclusion += f"\nDominant Authority Level: {dominant_level.name if dominant_level else 'Unknown'}"
    return conclusion

def zoned_analysis(conclusion):
    """
    Tag conclusion with zones: PLANNING, REPORTING, AUDIT based on keywords.
    Returns dict with zone tags and conclusion.
    """
    zones = {
        "PLANNING": ["plan", "forecast", "projection", "strategy", "prepare", "scenario"],
        "REPORTING": ["report", "summary", "findings", "results", "data", "analysis"],
        "AUDIT": ["audit", "compliance", "verification", "inspection", "review", "assessment"],
    }
    tags = set()
    conclusion_lower = conclusion.lower()
    for zone, keywords in zones.items():
        for kw in keywords:
            if kw in conclusion_lower:
                tags.add(zone)
                break
    if not tags:
        tags.add("REPORTING")  # default zone
    return {
        "zones": list(tags),
        "conclusion": conclusion
    }

# ---------------------------
# THREE-LAYER RESPONSE SYSTEM
# ---------------------------

class DoctrineCache:
    """
    Simple in-memory cache for doctrine analyses keyed by keywords.
    """
    def __init__(self):
        self.cache = {}
        self.lock = threading.Lock()

    def lookup(self, keywords):
        """
        Lookup cached analysis for any matching keyword.
        Returns cached analysis string or None.
        """
        with self.lock:
            for kw in keywords:
                if kw in self.cache:
                    return self.cache[kw]
        return None

    def store(self, keyword, analysis):
        with self.lock:
            self.cache[keyword] = analysis

doctrine_cache = DoctrineCache()

class SubEngineRouter:
    """
    Routes queries to relevant sub-engines based on semantic search.
    """
    def __init__(self):
        # Map keywords to sub-engines (function references)
        self.routing_table = {
            "regulation": self.sub_engine_regulatory,
            "emission": self.sub_engine_environmental,
            "market": self.sub_engine_market,
            "technical": self.sub_engine_technical,
            "financial": self.sub_engine_financial,
            "policy": self.sub_engine_policy,
            "risk": self.sub_engine_risk,
            "operation": self.sub_engine_operational,
        }

    def semantic_search(self, query):
        """
        Return list of sub-engines based on keyword matching.
        """
        matched_engines = []
        query_norm = normalize_query(query)
        for kw, engine in self.routing_table.items():
            if kw in query_norm:
                matched_engines.append(engine)
        if not matched_engines:
            matched_engines.append(self.sub_engine_general)
        return matched_engines

    def sub_engine_regulatory(self, query):
        time.sleep(0.1)
        return f"Regulatory analysis for '{query}'"

    def sub_engine_environmental(self, query):
        time.sleep(0.15)
        return f"Environmental impact analysis for '{query}'"

    def sub_engine_market(self, query):
        time.sleep(0.12)
        return f"Market analysis for '{query}'"

    def sub_engine_technical(self, query):
        time.sleep(0.18)
        return f"Technical feasibility analysis for '{query}'"

    def sub_engine_financial(self, query):
        time.sleep(0.14)
        return f"Financial assessment for '{query}'"

    def sub_engine_policy(self, query):
        time.sleep(0.11)
        return f"Policy evaluation for '{query}'"

    def sub_engine_risk(self, query):
        time.sleep(0.13)
        return f"Risk management analysis for '{query}'"

    def sub_engine_operational(self, query):
        time.sleep(0.16)
        return f"Operational efficiency analysis for '{query}'"

    def sub_engine_general(self, query):
        time.sleep(0.1)
        return f"General analysis for '{query}'"

sub_engine_router = SubEngineRouter()

def three_layer_response(query):
    """
    Implements the three-layer response system:
    Layer 1: Doctrine cache lookup (0-200ms)
    Layer 2: Semantic search + sub-engine routing
    Layer 3: Deep multi-engine analysis with parallel dispatch, merge, conflict resolution
    """
    start_time = time.time()

    # Layer 1: Doctrine cache lookup
    keywords = re.findall(r'\b\w+\b', query.lower())
    cache_result = doctrine_cache.lookup(keywords)
    if cache_result:
        elapsed = (time.time() - start_time) * 1000
        if elapsed <= 200:
            return f"CACHE HIT: {cache_result}"

    # Layer 2: Semantic search + sub-engine routing
    sub_engines = sub_engine_router.semantic_search(query)
    layer2_results = []
    for engine in sub_engines:
        result = engine(query)
        layer2_results.append(result)

    # Layer 3: Deep multi-engine analysis
    # Parallel dispatch to all sub-engines for deep analysis
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(engine, query): engine for engine in sub_engines}
        deep_results = []
        for future in as_completed(futures):
            try:
                res = future.result()
                deep_results.append(res)
            except Exception:
                deep_results.append("Error in sub-engine")

    # Merge and resolve conflicts - simplistic approach: concatenate unique results
    unique_results = list(dict.fromkeys(deep_results))
    merged_analysis = "\n".join(unique_results)

    # Store in cache for future quick lookup (using first keyword)
    if keywords:
        doctrine_cache.store(keywords[0], merged_analysis)

    return merged_analysis

# ---------------------------
# END OF PART 4 MODULES
# ---------------------------

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
        self._sub_engine_stats: Dict[str, List[float]] = defaultdict(list)
        self._sub_engine_errors: Dict[str, int] = defaultdict(int)
        self._sub_engine_availability: Dict[str, List[Tuple[float, bool]]] = defaultdict(list)
        self._query_times: deque = deque(maxlen=10000)  # (timestamp, QueryTelemetry)

    def record_query(self, telemetry: QueryTelemetry):
        with self._lock:
            self._queries.append(telemetry)
            self._query_times.append((telemetry.timestamp, telemetry))
            for engine in telemetry.engines_invoked:
                self._sub_engine_stats[engine].append(telemetry.latency_ms)
                self._sub_engine_availability[engine].append((telemetry.timestamp, True))
            if telemetry.cache_hit:
                self._doctrine_hits[telemetry.mode] += 1
            self._doctrine_total[telemetry.mode] += 1

    def record_error(self, telemetry: QueryTelemetry):
        with self._lock:
            self._errors.append(telemetry)
            for engine in telemetry.engines_invoked:
                self._sub_engine_errors[engine] += 1
                self._sub_engine_availability[engine].append((telemetry.timestamp, False))

    def get_latency_stats(self) -> Dict[str, Any]:
        with self._lock:
            latencies = [q.latency_ms for q in self._queries]
        if not latencies:
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        latencies.sort()
        n = len(latencies)
        def percentile(p):
            idx = int(p * n)
            idx = min(idx, n-1)
            return latencies[idx]
        return {
            "avg": sum(latencies)/n,
            "p50": percentile(0.50),
            "p95": percentile(0.95),
            "p99": percentile(0.99),
            "min": latencies[0],
            "max": latencies[-1]
        }

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        with self._lock:
            rates = {}
            for doctrine in self._doctrine_total:
                total = self._doctrine_total[doctrine]
                hits = self._doctrine_hits[doctrine]
                rates[doctrine] = hits / total if total else 0.0
            return rates

    def queries_last_hour(self) -> int:
        cutoff = time.time() - 3600
        with self._lock:
            return sum(1 for t, _ in self._query_times if t >= cutoff)

    def get_sub_engine_stats(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            stats = {}
            for engine, latencies in self._sub_engine_stats.items():
                if latencies:
                    lat_sorted = sorted(latencies)
                    n = len(lat_sorted)
                    stats[engine] = {
                        "avg_latency": sum(lat_sorted)/n,
                        "p95_latency": lat_sorted[int(0.95*n)-1],
                        "error_rate": self._sub_engine_errors[engine] / n if n else 0.0,
                        "invocations": n
                    }
                else:
                    stats[engine] = {
                        "avg_latency": None,
                        "p95_latency": None,
                        "error_rate": None,
                        "invocations": 0
                    }
            return stats

    def get_sub_engine_availability(self, window_sec=3600) -> Dict[str, float]:
        cutoff = time.time() - window_sec
        with self._lock:
            avail = {}
            for engine, events in self._sub_engine_availability.items():
                relevant = [ok for ts, ok in events if ts >= cutoff]
                if relevant:
                    avail[engine] = sum(1 for ok in relevant if ok) / len(relevant)
                else:
                    avail[engine] = None
            return avail

# --- DRIFT DETECTION ---

class DriftWatcher:
    def __init__(self, doctrine_names: List[str], window_size: int = 100):
        self._lock = threading.Lock()
        self._window_size = window_size
        self._baselines: Dict[str, float] = {d: None for d in doctrine_names}
        self._recent_confidences: Dict[str, deque] = {d: deque(maxlen=window_size) for d in doctrine_names}
        self._drift_alerts: Dict[str, List[Tuple[float, float, float]]] = defaultdict(list)  # doctrine: [(timestamp, baseline, new_avg)]
        self._drift_threshold = 0.10  # 10%

    def record_baseline(self, doctrine: str, confidence: float):
        with self._lock:
            if self._baselines[doctrine] is None:
                self._baselines[doctrine] = confidence

    def record_confidence(self, doctrine: str, confidence: float):
        with self._lock:
            self._recent_confidences[doctrine].append(confidence)
            if self._baselines[doctrine] is None:
                self._baselines[doctrine] = confidence

    def detect_drift(self, doctrine: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            baseline = self._baselines[doctrine]
            recents = self._recent_confidences[doctrine]
            if baseline is None or len(recents) < self._window_size:
                return None
            avg_recent = sum(recents) / len(recents)
            if baseline == 0:
                return None
            shift = (avg_recent - baseline) / baseline
            if abs(shift) > self._drift_threshold:
                alert = (time.time(), baseline, avg_recent)
                self._drift_alerts[doctrine].append(alert)
                return {
                    "doctrine": doctrine,
                    "baseline": baseline,
                    "recent_avg": avg_recent,
                    "shift": shift,
                    "timestamp": alert[0]
                }
            return None

    def get_drift_report(self) -> Dict[str, Any]:
        with self._lock:
            report = {}
            for doctrine in self._baselines:
                baseline = self._baselines[doctrine]
                recents = self._recent_confidences[doctrine]
                if baseline is not None and recents:
                    avg_recent = sum(recents) / len(recents)
                    shift = (avg_recent - baseline) / baseline if baseline else 0.0
                    report[doctrine] = {
                        "baseline": baseline,
                        "recent_avg": avg_recent,
                        "shift": shift,
                        "alerts": list(self._drift_alerts[doctrine])
                    }
            return report

# --- COVERAGE MAP ---

class CoverageTracker:
    def __init__(self, doctrine_names: List[str], sub_engines: List[str]):
        self._lock = threading.Lock()
        self._doctrine_triggered: Counter = Counter()
        self._doctrine_missed: Counter = Counter()
        self._missed_queries: List[Tuple[str, float]] = []
        self._sub_engine_coverage: Dict[str, Counter] = {se: Counter() for se in sub_engines}
        self._epistemic_gap: List[Tuple[str, float]] = []  # (query_id, timestamp)

    def record_triggered(self, doctrine: str, query_id: str, sub_engine: str):
        with self._lock:
            self._doctrine_triggered[doctrine] += 1
            self._sub_engine_coverage[sub_engine][doctrine] += 1

    def record_missed(self, query_id: str, timestamp: float):
        with self._lock:
            self._doctrine_missed[query_id] += 1
            self._missed_queries.append((query_id, timestamp))
            self._epistemic_gap.append((query_id, timestamp))

    def get_coverage_report(self) -> Dict[str, Any]:
        with self._lock:
            total_triggered = sum(self._doctrine_triggered.values())
            total_missed = len(self._missed_queries)
            doctrine_coverage = {
                d: self._doctrine_triggered[d] for d in self._doctrine_triggered
            }
            sub_engine_coverage = {
                se: dict(self._sub_engine_coverage[se]) for se in self._sub_engine_coverage
            }
            epistemic_gap = list(self._epistemic_gap)
            return {
                "total_triggered": total_triggered,
                "total_missed": total_missed,
                "doctrine_coverage": doctrine_coverage,
                "sub_engine_coverage": sub_engine_coverage,
                "epistemic_gap": epistemic_gap
            }

    def identify_epistemic_gap(self) -> List[Tuple[str, float]]:
        with self._lock:
            return list(self._epistemic_gap)

    def get_per_sub_engine_coverage(self) -> Dict[str, Dict[str, int]]:
        with self._lock:
            return {se: dict(self._sub_engine_coverage[se]) for se in self._sub_engine_coverage}

# --- DETERMINISM HASH ---

def compute_determinism_hash(query: Any, response: Any) -> str:
    # Canonicalize to JSON, sort keys for determinism
    try:
        query_json = json.dumps(query, sort_keys=True, separators=(',', ':'))
    except Exception:
        query_json = str(query)
    try:
        response_json = json.dumps(response, sort_keys=True, separators=(',', ':'))
    except Exception:
        response_json = str(response)
    combined = query_json + '|' + response_json
    return hashlib.sha256(combined.encode('utf-8')).hexdigest()

def verify_reproducibility(query: Any, response: Any, expected_hash: str) -> bool:
    actual_hash = compute_determinism_hash(query, response)
    return actual_hash == expected_hash

# --- AUDIT TRAIL ---

class AuditTrailWriter:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self._lock = threading.Lock()
        self._current_date = None
        self._file = None
        self._open_new_file()

    def _get_audit_filename(self, date: datetime.date) -> str:
        return os.path.join(self.base_dir, f"audit_{date.isoformat()}.jsonl")

    def _open_new_file(self):
        today = datetime.date.today()
        if self._current_date != today:
            if self._file:
                self._file.close()
            filename = self._get_audit_filename(today)
            os.makedirs(self.base_dir, exist_ok=True)
            self._file = open(filename, "a", encoding="utf-8")
            self._current_date = today

    def write(self, query_id: str, timestamp: float, engine_id: str, engines_invoked: List[str],
              mode: str, confidence: float, latency: float, cache_hit: bool):
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
            self._file.write(json.dumps(entry, sort_keys=True) + "\n")
            self._file.flush()

    def forensic_replay(self, date: datetime.date) -> List[Dict[str, Any]]:
        filename = self._get_audit_filename(date)
        if not os.path.exists(filename):
            return []
        with open(filename, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f]

    def close(self):
        with self._lock:
            if self._file:
                self._file.close()
                self._file = None

# --- PERFORMANCE PROFILER ---

class PerformanceProfiler:
    def __init__(self, sub_engines: List[str], window_size: int = 1000):
        self._lock = threading.Lock()
        self._window_size = window_size
        self._latency: Dict[str, deque] = {se: deque(maxlen=window_size) for se in sub_engines}
        self._errors: Dict[str, deque] = {se: deque(maxlen=window_size) for se in sub_engines}
        self._availability: Dict[str, deque] = {se: deque(maxlen=window_size) for se in sub_engines}
        self._sla_targets: Dict[str, Dict[str, float]] = {se: {"latency_ms": None, "error_rate": None, "availability": None} for se in sub_engines}

    def record(self, sub_engine: str, latency_ms: float, error: bool):
        with self._lock:
            self._latency[sub_engine].append(latency_ms)
            self._errors[sub_engine].append(1 if error else 0)
            self._availability[sub_engine].append(0 if error else 1)

    def set_sla(self, sub_engine: str, latency_ms: Optional[float], error_rate: Optional[float], availability: Optional[float]):
        with self._lock:
            self._sla_targets[sub_engine] = {
                "latency_ms": latency_ms,
                "error_rate": error_rate,
                "availability": availability
            }

    def get_stats(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            stats = {}
            for se in self._latency:
                latencies = list(self._latency[se])
                errors = list(self._errors[se])
                avail = list(self._availability[se])
                n = len(latencies)
                if n == 0:
                    stats[se] = {
                        "avg_latency": None,
                        "p95_latency": None,
                        "error_rate": None,
                        "availability": None,
                        "sla_violation": None
                    }
                    continue
                lat_sorted = sorted(latencies)
                p95 = lat_sorted[int(0.95*n)-1] if n >= 20 else lat_sorted[-1]
                error_rate = sum(errors)/n
                availability = sum(avail)/n
                sla = self._sla_targets[se]
                violation = (
                    (sla["latency_ms"] is not None and p95 > sla["latency_ms"]) or
                    (sla["error_rate"] is not None and error_rate > sla["error_rate"]) or
                    (sla["availability"] is not None and availability < sla["availability"])
                ) if sla else None
                stats[se] = {
                    "avg_latency": sum(latencies)/n,
                    "p95_latency": p95,
                    "error_rate": error_rate,
                    "availability": availability,
                    "sla_violation": violation
                }
            return stats

    def get_sla_violations(self) -> Dict[str, Dict[str, Any]]:
        stats = self.get_stats()
        violations = {}
        for se, s in stats.items():
            if s["sla_violation"]:
                violations[se] = s
        return violations

# --- Example integration hooks (not part of API, for illustration) ---

class DomainOrchestratorBackbone:
    def __init__(self, doctrine_names: List[str], sub_engines: List[str], audit_dir: str):
        self.telemetry = TelemetryCollector()
        self.drift = DriftWatcher(doctrine_names)
        self.coverage = CoverageTracker(doctrine_names, sub_engines)
        self.profiler = PerformanceProfiler(sub_engines)
        self.audit = AuditTrailWriter(audit_dir)
        self._doctrine_names = doctrine_names
        self._sub_engines = sub_engines

    def process_query(self, query_id: str, query: Any, response: Any,
                      engines_invoked: List[str], mode: str, confidence: float,
                      latency: float, cache_hit: bool, error: Optional[str] = None,
                      doctrine: Optional[str] = None, sub_engine: Optional[str] = None):
        timestamp = time.time()
        telemetry = QueryTelemetry(
            query_id=query_id,
            timestamp=timestamp,
            latency_ms=latency,
            cache_hit=cache_hit,
            engines_invoked=engines_invoked,
            mode=mode,
            confidence=confidence,
            error=error
        )
        self.telemetry.record_query(telemetry)
        if error:
            self.telemetry.record_error(telemetry)
        if doctrine:
            self.drift.record_confidence(doctrine, confidence)
            self.coverage.record_triggered(doctrine, query_id, sub_engine or engines_invoked[0])
        else:
            self.coverage.record_missed(query_id, timestamp)
        for engine in engines_invoked:
            self.profiler.record(engine, latency, error is not None)
        self.audit.write(query_id, timestamp, sub_engine or engines_invoked[0], engines_invoked, mode, confidence, latency, cache_hit)

    def close(self):
        self.audit.close()

ENGINE_ID = "ENRGIE"
ENGINE_PORT = 8855
SUB_ENGINES = {
    "ENRG01": "Nuclear Engineering",
    "ENRG02": "Solar Energy",
    "ENRG03": "Wind Power",
    "ENRG04": "Hydroelectric",
    "ENRG05": "Grid Operations",
    "ENRG06": "Energy Storage",
    "ENRG07": "Geothermal",
    "ENRG08": "Hydrogen Economy",
    "ENRG09": "Natural Gas Systems",
    "ENRG10": "Coal Technology",
    "ENRG11": "Bioenergy",
    "ENRG12": "Ocean Energy",
    "ENRG13": "Energy Efficiency",
    "ENRG14": "Smart Grid"
}

# Logger setup
logger = logging.getLogger("ENRGIE")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Models
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
    data: Optional[Dict[str, Any]] = None
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
    details: Optional[Dict[str, Any]] = None

class DoctrineInfo(BaseModel):
    doctrine_id: str
    description: str
    last_updated: datetime.datetime

class RoutingInfo(BaseModel):
    routing_rules: Dict[str, Any]
    engine_registry: Dict[str, str]

class SubEngineHealth(BaseModel):
    engine_id: str
    health: HealthStatus

# Globals and state
doctrine_cache: Dict[str, Any] = {}
search_index: Dict[str, List[str]] = {}
telemetry_data: Dict[str, Any] = {
    "queries_total": 0,
    "cache_hits": 0,
    "latencies": [],
    "sub_engine_calls": {k: {"calls": 0, "failures": 0, "avg_latency_ms": 0} for k in SUB_ENGINES.keys()},
    "queries_timestamps": []
}
health_monitor_status: Dict[str, HealthStatus] = {}
routing_rules: Dict[str, Any] = {}
circuit_breakers: Dict[str, Dict[str, Any]] = {}
lock = asyncio.Lock()

# Constants for circuit breaker
CB_FAILURE_THRESHOLD = 3
CB_RECOVERY_TIME_SEC = 30
CB_TIMEOUT_SEC = 5

# Utility functions
def normalize_query(query: str) -> str:
    normalized = query.strip().lower()
    logger.debug(f"Normalized query: {normalized}")
    return normalized

def classify_domain(query: str) -> List[str]:
    # Simple keyword-based domain classification for demonstration
    keywords_map = {
        "nuclear": ["ENRG01"],
        "solar": ["ENRG02"],
        "wind": ["ENRG03"],
        "hydro": ["ENRG04"],
        "grid": ["ENRG05", "ENRG14"],
        "storage": ["ENRG06"],
        "geothermal": ["ENRG07"],
        "hydrogen": ["ENRG08"],
        "gas": ["ENRG09"],
        "coal": ["ENRG10"],
        "bioenergy": ["ENRG11"],
        "ocean": ["ENRG12"],
        "efficiency": ["ENRG13"],
        "smart grid": ["ENRG14"]
    }
    matched_engines = set()
    for keyword, engines in keywords_map.items():
        if keyword in query:
            matched_engines.update(engines)
    if not matched_engines:
        # Default fallback to all engines if no match
        matched_engines = set(SUB_ENGINES.keys())
    logger.debug(f"Classified domains for query '{query}': {matched_engines}")
    return list(matched_engines)

def route_to_sub_engines(classified_domains: List[str]) -> List[str]:
    # For now, routing is direct: classified domains are the sub-engines to call
    logger.debug(f"Routing domains {classified_domains} to sub-engines")
    return classified_domains

async def dispatch_to_sub_engine(engine_id: str, query: str, parameters: Optional[Dict[str, Any]]) -> SubEngineResponse:
    start_time = time.perf_counter()
    # Circuit breaker check
    cb = circuit_breakers.get(engine_id, {"failures": 0, "last_failure_time": None, "open": False})
    now = time.time()
    if cb.get("open", False):
        if now - cb.get("last_failure_time", 0) > CB_RECOVERY_TIME_SEC:
            # Attempt recovery
            cb["open"] = False
            cb["failures"] = 0
            circuit_breakers[engine_id] = cb
            logger.info(f"Circuit breaker for {engine_id} closed after recovery time")
        else:
            logger.warning(f"Circuit breaker open for {engine_id}, skipping call")
            return SubEngineResponse(
                engine_id=engine_id,
                success=False,
                error="Circuit breaker open",
                latency_ms=0
            )
    try:
        # Simulate sub-engine call with async sleep and random success/failure
        await asyncio.wait_for(asyncio.sleep(random.uniform(0.05, 0.2)), timeout=CB_TIMEOUT_SEC)
        # Simulate failure randomly
        if random.random() < 0.05:
            raise Exception("Simulated sub-engine failure")
        # Simulated response data
        response_data = {
            "engine_id": engine_id,
            "result": f"Processed query '{query}' with parameters {parameters} in {SUB_ENGINES[engine_id]}"
        }
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        # Update telemetry
        telemetry_data["sub_engine_calls"][engine_id]["calls"] += 1
        prev_avg = telemetry_data["sub_engine_calls"][engine_id]["avg_latency_ms"]
        calls = telemetry_data["sub_engine_calls"][engine_id]["calls"]
        telemetry_data["sub_engine_calls"][engine_id]["avg_latency_ms"] = (prev_avg * (calls - 1) + latency_ms) / calls
        return SubEngineResponse(
            engine_id=engine_id,
            success=True,
            data=response_data,
            latency_ms=latency_ms
        )
    except asyncio.TimeoutError:
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        logger.error(f"Timeout calling sub-engine {engine_id}")
        # Update circuit breaker failure count
        cb["failures"] = cb.get("failures", 0) + 1
        cb["last_failure_time"] = now
        if cb["failures"] >= CB_FAILURE_THRESHOLD:
            cb["open"] = True
            logger.warning(f"Circuit breaker opened for {engine_id} due to failures")
        circuit_breakers[engine_id] = cb
        telemetry_data["sub_engine_calls"][engine_id]["failures"] += 1
        return SubEngineResponse(
            engine_id=engine_id,
            success=False,
            error="Timeout",
            latency_ms=latency_ms
        )
    except Exception as e:
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        logger.error(f"Error calling sub-engine {engine_id}: {str(e)}")
        cb["failures"] = cb.get("failures", 0) + 1
        cb["last_failure_time"] = now
        if cb["failures"] >= CB_FAILURE_THRESHOLD:
            cb["open"] = True
            logger.warning(f"Circuit breaker opened for {engine_id} due to failures")
        circuit_breakers[engine_id] = cb
        telemetry_data["sub_engine_calls"][engine_id]["failures"] += 1
        return SubEngineResponse(
            engine_id=engine_id,
            success=False,
            error=str(e),
            latency_ms=latency_ms
        )

def merge_responses(responses: List[SubEngineResponse]) -> Dict[str, Any]:
    merged = {"results": [], "errors": []}
    for resp in responses:
        if resp.success and resp.data:
            merged["results"].append(resp.data)
        elif resp.error:
            merged["errors"].append({"engine_id": resp.engine_id, "error": resp.error})
    logger.debug(f"Merged response: {merged}")
    return merged

def apply_guardrails(response: Dict[str, Any]) -> Dict[str, Any]:
    # Placeholder for guardrail logic: e.g. filter sensitive data, enforce policies
    # For demo, just return as is
    logger.debug("Applying guardrails to response")
    return response

def hash_response(response: Dict[str, Any]) -> str:
    response_str = str(response).encode('utf-8')
    response_hash = hashlib.sha256(response_str).hexdigest()
    logger.debug(f"Response hash: {response_hash}")
    return response_hash

def log_query(query: str, response_hash: str, latency_ms: int, engines_called: List[str]):
    logger.info(f"Query logged: hash={response_hash}, latency={latency_ms}ms, engines={engines_called}")

async def fallback_to_doctrine_cache(query: str) -> Dict[str, Any]:
    # Return cached doctrine if available
    cached = doctrine_cache.get(query)
    if cached:
        telemetry_data["cache_hits"] += 1
        logger.info(f"Fallback to doctrine cache for query '{query}'")
        return {"results": [cached], "errors": []}
    else:
        logger.warning(f"No doctrine cache fallback available for query '{query}'")
        return {"results": [], "errors": ["No cached doctrine available"]}

# Lifespan management
async def initialize_doctrine_cache():
    # Simulate loading doctrines into cache
    logger.info("Initializing doctrine cache...")
    await asyncio.sleep(0.5)
    for i in range(1, 21):
        doctrine_id = f"DOC{i:03d}"
        doctrine_cache[f"doctrine_{i}"] = {
            "doctrine_id": doctrine_id,
            "description": f"Doctrine description {i}",
            "last_updated": datetime.datetime.utcnow()
        }
    logger.info("Doctrine cache initialized.")

async def start_health_monitor():
    logger.info("Starting health monitor...")

    async def monitor():
        while True:
            for engine_id in SUB_ENGINES.keys():
                # Simulate health check
                status = random.choice(["healthy", "degraded", "unhealthy"])
                details = {"load": random.uniform(0, 1)}
                health_monitor_status[engine_id] = HealthStatus(
                    engine_id=engine_id,
                    status=status,
                    details=details
                )
            await asyncio.sleep(10)

    asyncio.create_task(monitor())
    logger.info("Health monitor started.")

async def seed_search_index():
    logger.info("Seeding search index...")
    # Simulate indexing doctrines
    await asyncio.sleep(0.5)
    for key in doctrine_cache.keys():
        terms = key.split("_")
        for term in terms:
            if term not in search_index:
                search_index[term] = []
            search_index[term].append(key)
    logger.info("Search index seeded.")

async def start_telemetry():
    logger.info("Starting telemetry system...")
    # Telemetry could be sending data to external systems, here just simulate
    async def telemetry_loop():
        while True:
            # Simulate telemetry aggregation
            await asyncio.sleep(60)
            logger.info("Telemetry heartbeat: queries_total=%d", telemetry_data["queries_total"])
    asyncio.create_task(telemetry_loop())
    logger.info("Telemetry system started.")

# FastAPI app setup
app = FastAPI(title="Energy Intelligence Engine - Domain Orchestrator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await initialize_doctrine_cache()
    await start_health_monitor()
    await seed_search_index()
    await start_telemetry()
    logger.info(f"{ENGINE_ID} started on port {ENGINE_PORT}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"{ENGINE_ID} shutting down...")

# Endpoint implementations

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    start_time = time.perf_counter()
    normalized_query = normalize_query(request.query)
    telemetry_data["queries_total"] += 1
    telemetry_data["queries_timestamps"].append(time.time())
    classified_domains = classify_domain(normalized_query)
    routed_engines = route_to_sub_engines(classified_domains)
    responses = []
    for engine_id in routed_engines:
        resp = await dispatch_to_sub_engine(engine_id, normalized_query, request.parameters)
        responses.append(resp)
    merged_response = merge_responses(responses)
    guarded_response = apply_guardrails(merged_response)
    latency_ms = int((time.perf_counter() - start_time) * 1000)
    response_hash = hash_response(guarded_response)
    log_query(normalized_query, response_hash, latency_ms, routed_engines)
    if all(not r.success for r in responses):
        # Fallback to doctrine cache if all failed
        fallback_response = await fallback_to_doctrine_cache(normalized_query)
        return JSONResponse(content=fallback_response)
    return JSONResponse(content=guarded_response)

@app.get("/health")
async def health_endpoint():
    # Self health
    self_health = {
        "engine_id": ENGINE_ID,
        "status": "healthy",
        "details": {
            "uptime": "unknown",  # Could be implemented with start time tracking
            "doctrine_cache_size": len(doctrine_cache),
            "search_index_terms": len(search_index)
        }
    }
    # Sub-engines health
    sub_engines_health = []
    for engine_id in SUB_ENGINES.keys():
        health = health_monitor_status.get(engine_id)
        if health is None:
            health = HealthStatus(engine_id=engine_id, status="unknown", details=None)
        sub_engines_health.append(health.dict())
    return JSONResponse(content={"self": self_health, "sub_engines": sub_engines_health})

@app.get("/metrics")
async def metrics_endpoint():
    # Calculate latency stats
    latencies = telemetry_data["latencies"]
    latency_stats = {
        "count": len(latencies),
        "min_ms": min(latencies) if latencies else None,
        "max_ms": max(latencies) if latencies else None,
        "avg_ms": sum(latencies) / len(latencies) if latencies else None,
        "p50_ms": None,
        "p90_ms": None,
        "p99_ms": None
    }
    if latencies:
        sorted_lat = sorted(latencies)
        latency_stats["p50_ms"] = sorted_lat[int(len(sorted_lat)*0.50)]
        latency_stats["p90_ms"] = sorted_lat[int(len(sorted_lat)*0.90)]
        latency_stats["p99_ms"] = sorted_lat[int(len(sorted_lat)*0.99)]
    # Cache hit rate
    total_queries = telemetry_data["queries_total"]
    cache_hits = telemetry_data["cache_hits"]
    cache_hit_rate = cache_hits / total_queries if total_queries > 0 else 0.0
    # Queries per hour
    now_ts = time.time()
    one_hour_ago = now_ts - 3600
    queries_last_hour = [t for t in telemetry_data["queries_timestamps"] if t >= one_hour_ago]
    queries_per_hour = len(queries_last_hour)
    # Sub-engine stats
    sub_engine_stats = {}
    for engine_id, stats in telemetry_data["sub_engine_calls"].items():
        sub_engine_stats[engine_id] = stats
    metrics = MetricsResponse(
        latency_stats=latency_stats,
        cache_hit_rate=cache_hit_rate,
        queries_per_hour=queries_per_hour,
        sub_engine_stats=sub_engine_stats
    )
    return JSONResponse(content=metrics.dict())

@app.get("/coverage")
async def coverage_endpoint():
    # Simulate doctrine coverage and epistemic gaps
    doctrine_coverage = {}
    for engine_id in SUB_ENGINES.keys():
        doctrine_coverage[engine_id] = random.uniform(0.7, 1.0)
    epistemic_gaps = ["Hydrogen Economy - advanced storage", "Smart Grid - cybersecurity"]
    report = CoverageReport(
        doctrine_coverage=doctrine_coverage,
        epistemic_gaps=epistemic_gaps
    )
    return JSONResponse(content=report.dict())

@app.get("/drift")
async def drift_endpoint():
    # Simulate drift detection report
    drift_detected = random.choice([True, False])
    details = None
    if drift_detected:
        details = {
            "engines_affected": random.sample(list(SUB_ENGINES.keys()), k=2),
            "drift_score": random.uniform(0.5, 0.9),
            "last_checked": datetime.datetime.utcnow().isoformat()
        }
    report = DriftReport(
        drift_detected=drift_detected,
        details=details
    )
    return JSONResponse(content=report.dict())

@app.get("/doctrines")
async def doctrines_endpoint():
    doctrines_list = []
    for key, val in doctrine_cache.items():
        info = DoctrineInfo(
            doctrine_id=val["doctrine_id"],
            description=val["description"],
            last_updated=val["last_updated"]
        )
        doctrines_list.append(info.dict())
    return JSONResponse(content={"doctrines": doctrines_list})

@app.get("/routing")
async def routing_endpoint():
    # Simulate routing rules and engine registry
    routing_rules_sim = {
        "nuclear": ["ENRG01"],
        "solar": ["ENRG02"],
        "wind": ["ENRG03"],
        "default": list(SUB_ENGINES.keys())
    }
    info = RoutingInfo(
        routing_rules=routing_rules_sim,
        engine_registry=SUB_ENGINES
    )
    return JSONResponse(content=info.dict())

@app.get("/sub-engines")
async def sub_engines_endpoint():
    health_list = []
    for engine_id in SUB_ENGINES.keys():
        health = health_monitor_status.get(engine_id)
        if health is None:
            health = HealthStatus(engine_id=engine_id, status="unknown", details=None)
        health_list.append(SubEngineHealth(engine_id=engine_id, health=health).dict())
    return JSONResponse(content={"sub_engines_health": health_list})

@app.post("/route")
async def route_dry_run(request: RouteRequest):
    normalized_query = normalize_query(request.query)
    classified_domains = classify_domain(normalized_query)
    routed_engines = route_to_sub_engines(classified_domains)
    return JSONResponse(content={"routed_engines": routed_engines})

@app.post("/analyze")
async def analyze_endpoint(request: AnalyzeRequest):
    start_time = time.perf_counter()
    normalized_query = normalize_query(request.query)
    classified_domains = classify_domain(normalized_query)
    routed_engines = route_to_sub_engines(classified_domains)
    # Deep multi-engine analysis: dispatch to all routed engines and collect detailed info
    responses = []
    for engine_id in routed_engines:
        resp = await dispatch_to_sub_engine(engine_id, normalized_query, request.parameters)
        responses.append(resp)
    merged_response = merge_responses(responses)
    guarded_response = apply_guardrails(merged_response)
    latency_ms = int((time.perf_counter() - start_time) * 1000)
    response_hash = hash_response(guarded_response)
    log_query(normalized_query, response_hash, latency_ms, routed_engines)
    return JSONResponse(content={
        "analysis": guarded_response,
        "latency_ms": latency_ms,
        "response_hash": response_hash,
        "engines_invoked": routed_engines
    })

# Exception handlers
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
    uvicorn.run("main:app", host="0.0.0.0", port=ENGINE_PORT, log_level="info")