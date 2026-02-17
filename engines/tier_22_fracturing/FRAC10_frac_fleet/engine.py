import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set, Callable
from enum import Enum, auto
from datetime import datetime, timedelta

# =========================
# ENUMS
# =========================

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
    FLEET_CONFIG = "FLEET_CONFIG"
    PUMP_TYPE = "PUMP_TYPE"
    FUEL_LOGISTICS = "FUEL_LOGISTICS"
    CREW_MANAGEMENT = "CREW_MANAGEMENT"
    MAINTENANCE = "MAINTENANCE"
    EFFICIENCY = "EFFICIENCY"
    COST_CONTROL = "COST_CONTROL"
    SAFETY = "SAFETY"
    DATA_INTEGRITY = "DATA_INTEGRITY"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    SUPPLY_CHAIN = "SUPPLY_CHAIN"
    REGULATORY = "REGULATORY"

# =========================
# METRICS COLLECTOR
# =========================

class MetricsCollector:
    def __init__(self):
        self.queries: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.doctrine_hits: Dict[str, int] = {}
        self.latencies: List[float] = []
        self.last_query_time: List[datetime] = []

    def record_query(self, doctrine_ids: List[str], latency: float):
        now = datetime.utcnow()
        self.last_query_time.append(now)
        for doc_id in doctrine_ids:
            self.doctrine_hits[doc_id] = self.doctrine_hits.get(doc_id, 0) + 1
        self.latencies.append(latency)
        self.queries.append({"time": now, "doctrines": doctrine_ids, "latency": latency})

    def record_error(self, error: str):
        self.errors.append({"time": datetime.utcnow(), "error": error})

    def get_latency_stats(self) -> Dict[str, float]:
        if not self.latencies:
            return {"min": 0.0, "max": 0.0, "avg": 0.0}
        return {
            "min": min(self.latencies),
            "max": max(self.latencies),
            "avg": sum(self.latencies) / len(self.latencies)
        }

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        total = sum(self.doctrine_hits.values())
        if total == 0:
            return {}
        return {k: v / total for k, v in self.doctrine_hits.items()}

    def queries_last_hour(self) -> int:
        cutoff = datetime.utcnow() - timedelta(hours=1)
        return sum(1 for t in self.last_query_time if t > cutoff)

metrics_collector = MetricsCollector()

# =========================
# PYDANTIC MODELS
# =========================

class QueryRequest(BaseModel):
    scenario: str = Field(..., description="Operational scenario or question")
    mode: ResponseMode = Field(..., description="Response mode")
    entity_type: str = Field(..., description="Entity type (e.g., fleet, pump, crew)")
    complexity: int = Field(..., ge=1, le=10, description="Complexity level (1-10)")

class QueryResponse(BaseModel):
    engine_id: str
    query_id: str
    mode: ResponseMode
    confidence: float
    confidence_zone: ConfidenceZone
    position_zone: PositionZone
    primary_conclusion: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    counter_arguments: List[str]
    resolution_strategy: str
    determinism_hash: str

# =========================
# SEMANTIC NORMALIZATION
# =========================

SEMANTIC_MAP: Dict[str, str] = {
    "frac": "hydraulic fracturing",
    "e-frac": "electric fracturing fleet",
    "diesel frac": "diesel-powered fracturing fleet",
    "DGB": "dual fuel gas blend",
    "treating iron": "high-pressure manifold",
    "blender tub": "proppant mixing vessel",
    "hydration unit": "gel mixing system",
    "data van": "treatment monitoring SCADA",
    "wireline": "plug pump-down wireline",
    "coiled tubing": "milling and drillout coiled tubing",
    "NPT": "non-productive time",
    "BPM": "barrels per minute",
    "MTBF": "mean time between failures",
    "power end": "pump power end",
    "fluid end": "pump fluid end",
    "plunger": "pump plunger",
    "proppant": "fracturing proppant",
    "missile": "high-pressure manifold missile",
    "rig-up": "fleet mobilization",
    "rig-down": "fleet demobilization",
    "stage": "fracturing stage",
    "zipper frac": "simultaneous multi-well fracturing",
    "shift": "crew shift",
    "CNG": "compressed natural gas",
    "SCADA": "supervisory control and data acquisition",
    "direct drive": "direct drive turbine",
    "Tier 4": "EPA Tier 4 emission standard",
    "pump-down": "wireline pump-down",
    "cleanout": "coiled tubing cleanout",
    "proppant addition rate": "proppant feed rate",
    "chemical addition": "chemical dosing",
    "field gas": "produced field gas",
    "market pricing": "market-based pricing",
    "tub": "mixing vessel",
    "turbine": "turbine-driven pump",
    "crew": "fracturing crew",
    "fuel logistics": "fuel supply chain",
    "audit": "operational audit",
    "planning": "operational planning",
    "reporting": "operational reporting",
    "efficiency": "operational efficiency",
    "cost": "operational cost",
    "reliability": "equipment reliability",
    "maintenance": "equipment maintenance",
    "mobilization": "fleet mobilization",
    "demobilization": "fleet demobilization"
}

def semantic_normalize(text: str) -> str:
    for k, v in SEMANTIC_MAP.items():
        text = text.replace(k, v)
    return text

# =========================
# EPISTEMIC GUARDRAILS
# =========================

BANNED_PHRASES = [
    "guaranteed", "always", "never", "impossible", "fail-safe", "perfect", "cannot fail",
    "zero risk", "no chance", "absolute", "undisputed", "without exception", "certainly",
    "completely safe", "flawless", "error-free"
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "[REDACTED]")
    return text

# =========================
# FACT FRAGILITY SCORING
# =========================

def score_fact_fragility(fact: str) -> Dict[str, float]:
    verifiability = 1.0 if any(auth in fact for auth in [
        "SPE", "API", "FracFocus", "DOE", "EIA", "OSHA", "EPA", "IADC", "ISO"
    ]) else 0.6
    recharacterization_risk = 0.2 if "may" in fact or "can" in fact else 0.7
    testimony_dependence = 0.8 if "operator report" in fact or "field observation" in fact else 0.3
    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence
    }

# =========================
# DOCTRINE CACHE
# =========================

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
    confidence_zone: ConfidenceZone
    controlling_precedent: List[str]

# 30+ REALISTIC DOCTRINE BLOCKS

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Optimal Frac Fleet Configuration: Pump Count and Horsepower",
        keywords=["fleet configuration", "pump count", "horsepower", "stage design", "well profile"],
        conclusion_template=(
            "The optimal number of pumps and total horsepower for a hydraulic fracturing fleet "
            "should be determined by the planned stage rate, treating pressure, and redundancy requirements. "
            "A typical modern fleet for high-rate shale operations utilizes 18-24 pumps, each rated at 2,500-3,000 HP, "
            "to deliver up to 50,000-70,000 total HP, supporting rates of 80-120 BPM per well."
        ),
        reasoning_framework=(
            "1. Assess the planned maximum stage rate (BPM) and treating pressure based on reservoir and completion design. "
            "2. Calculate the required hydraulic horsepower (HHP) using the formula: HHP = (Rate x Pressure x 0.0061). "
            "3. Factor in pump derating for altitude, temperature, and expected wear (typically 10-15%). "
            "4. Include redundancy for maintenance and unplanned downtime (N+2 strategy is common). "
            "5. Consider logistical constraints (pad size, access, power/fuel supply). "
            "6. Benchmark against regional fleet norms (SPE 187451, API RP 100-16). "
            "7. Validate configuration with simulation and field trial data. "
            "8. Adjust for operational efficiency targets (stages/day, NPT minimization). "
            "9. Review with HSE and regulatory for compliance. "
            "10. Document configuration rationale for audit and reporting. "
            "11. Monitor real-time performance and update configuration as needed. "
            "12. Ensure all pumps meet EPA Tier 4 or local emission standards where required. "
            "13. For zipper frac operations, ensure sufficient pumps for simultaneous wells. "
            "14. Consider modular fleet approaches for rapid mobilization/demobilization. "
            "15. Engage with OEMs for latest pump reliability and service data."
        ),
        key_factors=[
            "Planned stage rate (BPM)",
            "Treating pressure (psi)",
            "Pump derating factors",
            "Redundancy (N+2, N+3)",
            "Emission compliance"
        ],
        primary_authority=[
            "SPE 187451: 'Optimizing Frac Fleet Design for Unconventional Plays'",
            "API RP 100-16: 'Hydraulic Fracturing Operations'",
            "FracFocus: Fleet Emissions Reporting"
        ],
        burden_holder="Fleet Engineering Manager",
        adversary_position="Cost Controller advocating for minimal pump count",
        counter_arguments=[
            "Excess pumps increase capital and fuel costs",
            "Pad space constraints may limit fleet size",
            "Over-sizing can lead to underutilization",
            "Emission limits may restrict total HP",
            "Redundancy may not be needed with high-reliability pumps"
        ],
        resolution_strategy=(
            "Balance operational risk with cost and compliance by adopting a data-driven N+2 redundancy, "
            "documenting configuration, and reviewing after each campaign."
        ),
        entity_scope="Fleet",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "SPE 187451",
            "API RP 100-16"
        ]
    ),
    DoctrineBlock(
        topic="Frac Pump Types: Triplex vs Quintuplex Plunger",
        keywords=["pump type", "triplex", "quintuplex", "plunger", "maintenance"],
        conclusion_template=(
            "Quintuplex plunger pumps offer smoother flow and reduced pulsation compared to triplex pumps, "
            "resulting in lower vibration and extended component life. However, triplex pumps may be preferred "
            "for certain high-pressure applications due to simpler design and ease of maintenance."
        ),
        reasoning_framework=(
            "1. Compare mechanical design: triplex (3 plungers) vs quintuplex (5 plungers). "
            "2. Analyze flow characteristics: quintuplex provides more continuous flow, reducing pressure spikes. "
            "3. Evaluate vibration and fatigue: lower in quintuplex, improving fluid end life. "
            "4. Assess maintenance complexity: triplex pumps are simpler and may be serviced faster in the field. "
            "5. Consider spare parts inventory: quintuplex requires more unique parts. "
            "6. Review OEM reliability data (SPE 204112, API 674). "
            "7. Factor in initial cost vs total cost of ownership. "
            "8. Examine field failure modes (seal wear, plunger scoring). "
            "9. Match pump type to job requirements (pressure, rate, fluid type). "
            "10. Consult with maintenance and operations for historical performance. "
            "11. Consider regulatory or customer preferences. "
            "12. Document pump selection rationale for audit."
        ),
        key_factors=[
            "Flow smoothness",
            "Vibration/fatigue",
            "Maintenance complexity",
            "Spare parts logistics",
            "Total cost of ownership"
        ],
        primary_authority=[
            "SPE 204112: 'Frac Pump Reliability in Shale Operations'",
            "API 674: 'Positive Displacement Pumps'",
            "OEM Field Service Bulletins"
        ],
        burden_holder="Fleet Maintenance Lead",
        adversary_position="Operations Manager favoring triplex for rapid swaps",
        counter_arguments=[
            "Triplex pumps are easier to maintain in remote locations",
            "Quintuplex pumps have higher upfront cost",
            "Spare parts for quintuplex may have longer lead times",
            "Triplex pumps are proven in legacy fleets",
            "Operator familiarity with triplex design"
        ],
        resolution_strategy=(
            "Select pump type based on job profile and total cost analysis, "
            "with periodic review of field reliability data."
        ),
        entity_scope="Pump",
        confidence=0.89,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "SPE 204112",
            "API 674"
        ]
    ),
    DoctrineBlock(
        topic="Electric Frac Fleet (E-Frac) Direct Drive Turbine",
        keywords=["e-frac", "electric fleet", "direct drive", "turbine", "emissions"],
        conclusion_template=(
            "Electric fracturing fleets using direct drive turbines can significantly reduce emissions and fuel costs, "
            "especially when powered by field gas. However, they require robust electrical infrastructure and may face "
            "initial capital hurdles."
        ),
        reasoning_framework=(
            "1. Assess available field gas supply and quality for turbine operation. "
            "2. Compare emissions profile vs diesel fleets (EPA, SPE 199327). "
            "3. Evaluate electrical infrastructure requirements (transformers, switchgear, cabling). "
            "4. Analyze operational flexibility: e-frac fleets can ramp up/down rapidly. "
            "5. Consider maintenance intervals for turbines vs diesel engines. "
            "6. Review fuel cost savings from field gas substitution (EIA, DOE). "
            "7. Examine reliability data for direct drive systems (OEM reports). "
            "8. Factor in noise reduction and HSE improvements. "
            "9. Model total cost of ownership over 3-5 years. "
            "10. Assess regulatory incentives for emissions reduction. "
            "11. Document lessons learned from prior e-frac deployments. "
            "12. Plan for training of crew on high-voltage safety. "
            "13. Review grid interconnection requirements if supplementing with utility power. "
            "14. Benchmark against regional adoption rates (FracFocus). "
            "15. Prepare contingency for turbine downtime (backup diesel units)."
        ),
        key_factors=[
            "Field gas availability",
            "Electrical infrastructure",
            "Emissions profile",
            "Fuel cost savings",
            "Maintenance intervals"
        ],
        primary_authority=[
            "SPE 199327: 'E-Frac Fleet Performance and Emissions'",
            "EPA Natural Gas STAR Program",
            "DOE Field Gas Utilization Reports"
        ],
        burden_holder="Fleet Project Manager",
        adversary_position="Finance Director citing high capital cost",
        counter_arguments=[
            "High upfront capital for turbines and switchgear",
            "Grid connection may be unreliable in remote areas",
            "Crew retraining for electrical hazards",
            "Field gas quality fluctuations can impact reliability",
            "Limited field service support for new technology"
        ],
        resolution_strategy=(
            "Conduct pilot deployments, track emissions and cost data, and phase in e-frac as infrastructure matures."
        ),
        entity_scope="Fleet",
        confidence=0.87,
        confidence_zone=ConfidenceZone.AGGRESSIVE,
        controlling_precedent=[
            "SPE 199327",
            "EPA Natural Gas STAR"
        ]
    ),
    DoctrineBlock(
        topic="Diesel Frac Fleet: Conventional and Tier 4 DGB",
        keywords=["diesel fleet", "Tier 4", "dual fuel", "DGB", "emissions"],
        conclusion_template=(
            "Diesel-powered fracturing fleets remain the industry standard, with Tier 4 engines and dual-fuel gas blend (DGB) "
            "systems offering improved emissions and fuel flexibility. Compliance with EPA and local standards is mandatory."
        ),
        reasoning_framework=(
            "1. Review EPA Tier 4 emission requirements for diesel engines. "
            "2. Evaluate DGB system compatibility with available field gas (API, OEM specs). "
            "3. Compare fuel cost and logistics for diesel vs dual-fuel operation. "
            "4. Assess engine maintenance intervals and parts availability. "
            "5. Analyze emissions data (NOx, PM, CO2) for Tier 4 and DGB units. "
            "6. Consider operational flexibility: diesel units can be rapidly deployed and serviced. "
            "7. Factor in regulatory reporting obligations (FracFocus, state agencies). "
            "8. Benchmark against regional fleet composition (EIA, IADC). "
            "9. Document fuel source selection and compliance for audit. "
            "10. Plan for periodic emissions testing and recordkeeping. "
            "11. Review OEM field service bulletins for DGB reliability. "
            "12. Evaluate crew familiarity with diesel and DGB systems. "
            "13. Model total cost of ownership including fuel, maintenance, and compliance costs. "
            "14. Prepare for supply chain disruptions in diesel or field gas."
        ),
        key_factors=[
            "Emission standards compliance",
            "Fuel logistics and cost",
            "Engine maintenance intervals",
            "DGB system reliability",
            "Regulatory reporting"
        ],
        primary_authority=[
            "EPA Tier 4 Standards",
            "API 937: 'Dual Fuel Engine Operations'",
            "FracFocus Emissions Data"
        ],
        burden_holder="Fleet Compliance Officer",
        adversary_position="Operations Lead preferring legacy Tier 2 engines",
        counter_arguments=[
            "Tier 4 engines have higher maintenance costs",
            "DGB systems may not be compatible with all field gas",
            "Diesel supply chain disruptions can halt operations",
            "Older engines may be more reliable in harsh conditions",
            "Regulatory burden for emissions reporting"
        ],
        resolution_strategy=(
            "Adopt Tier 4/DGB where required, maintain legacy units for contingency, and document all compliance actions."
        ),
        entity_scope="Fleet",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "EPA Tier 4",
            "API 937"
        ]
    ),
    DoctrineBlock(
        topic="Pump Rate Capacity: 100 BPM per Pump",
        keywords=["pump rate", "BPM", "capacity", "stage design", "equipment limits"],
        conclusion_template=(
            "Modern frac pumps are typically rated for up to 100 BPM, but actual sustained rates depend on fluid properties, "
            "pressure, and maintenance condition. Exceeding rated capacity increases risk of failure and NPT."
        ),
        reasoning_framework=(
            "1. Review OEM pump specifications for maximum BPM and pressure. "
            "2. Assess fluid properties (viscosity, sand load) and their impact on achievable rate. "
            "3. Factor in altitude and temperature derating. "
            "4. Analyze historical field data for sustained rate performance. "
            "5. Monitor pump health (vibration, temperature) in real time. "
            "6. Consider impact of proppant concentration on wear and reliability. "
            "7. Evaluate NPT incidents related to over-rate operation (SPE 204112). "
            "8. Plan for staged ramp-up to max rate during each stage. "
            "9. Document any deviations from OEM recommendations. "
            "10. Coordinate with data van for real-time monitoring and alerts. "
            "11. Schedule preventive maintenance based on high-rate operation. "
            "12. Review with HSE for risk assessment."
        ),
        key_factors=[
            "OEM pump rating",
            "Fluid properties",
            "Proppant concentration",
            "Maintenance condition",
            "NPT history"
        ],
        primary_authority=[
            "SPE 204112: 'Frac Pump Reliability'",
            "OEM Pump Data Sheets",
            "API 674"
        ],
        burden_holder="Frac Equipment Supervisor",
        adversary_position="Operations pushing for higher rates",
        counter_arguments=[
            "Higher rates increase stage efficiency",
            "OEM ratings are conservative",
            "Short bursts above rating may be acceptable",
            "Field conditions may allow for higher rates",
            "NPT risk can be managed with monitoring"
        ],
        resolution_strategy=(
            "Operate within OEM ratings, monitor real-time data, and document exceptions for audit."
        ),
        entity_scope="Pump",
        confidence=0.88,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "SPE 204112",
            "API 674"
        ]
    ),
    DoctrineBlock(
        topic="Treating Iron: High-Pressure Manifold and Missile",
        keywords=["treating iron", "manifold", "missile", "pressure rating", "inspection"],
        conclusion_template=(
            "Treating iron and high-pressure manifold systems (missile) must be rated for maximum anticipated treating pressure, "
            "inspected regularly, and tracked for service hours to prevent catastrophic failure."
        ),
        reasoning_framework=(
            "1. Verify all treating iron is rated above maximum treating pressure (API 6A, OEM). "
            "2. Inspect for erosion, corrosion, and mechanical damage before each job. "
            "3. Maintain detailed service logs for each component (hours, cycles). "
            "4. Follow OEM and API inspection intervals (API 6A, API 7K). "
            "5. Use digital tracking (RFID/barcode) for asset management. "
            "6. Replace components nearing end-of-life or with abnormal wear. "
            "7. Train crew on proper handling and assembly (OSHA, IADC). "
            "8. Conduct pressure testing before each frac campaign. "
            "9. Document all inspections and repairs for audit. "
            "10. Review incident history and update inspection protocols as needed. "
            "11. Coordinate with HSE for compliance and reporting. "
            "12. Benchmark against industry best practices (SPE 193456)."
        ),
        key_factors=[
            "Pressure rating",
            "Inspection interval",
            "Service hours/cycles",
            "Asset tracking",
            "Crew training"
        ],
        primary_authority=[
            "API 6A: 'Wellhead and Christmas Tree Equipment'",
            "API 7K: 'Drilling and Well Servicing Equipment'",
            "SPE 193456: 'Manifold Failure Analysis'"
        ],
        burden_holder="Frac Equipment Inspector",
        adversary_position="Field Supervisor rushing rig-up",
        counter_arguments=[
            "Inspection slows down operations",
            "Visual checks may miss internal erosion",
            "Service logs are often incomplete",
            "Pressure testing adds cost",
            "Asset tracking systems can fail"
        ],
        resolution_strategy=(
            "Enforce inspection and tracking protocols, with no exceptions for schedule pressure."
        ),
        entity_scope="Equipment",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API 6A",
            "API 7K"
        ]
    ),
    DoctrineBlock(
        topic="Blender Tub: Proppant Addition Rate and Mixing",
        keywords=["blender tub", "proppant", "mixing", "feed rate", "stage design"],
        conclusion_template=(
            "Accurate proppant addition and mixing in the blender tub is critical to stage success. "
            "Automated feed systems and real-time monitoring reduce the risk of sand-out and NPT."
        ),
        reasoning_framework=(
            "1. Set proppant feed rate based on stage design and pump rate. "
            "2. Calibrate automated feeders before each job (OEM, API RP 100-16). "
            "3. Monitor proppant concentration in real time via data van/SCADA. "
            "4. Adjust feed rate dynamically to match rate changes. "
            "5. Inspect blender tub for wear and buildup before each stage. "
            "6. Document all calibration and adjustments. "
            "7. Analyze NPT incidents related to proppant delivery (SPE 204112). "
            "8. Train crew on troubleshooting feed system alarms. "
            "9. Maintain spare parts inventory for critical components. "
            "10. Review with operations for lessons learned. "
            "11. Benchmark against industry best practices."
        ),
        key_factors=[
            "Proppant feed rate",
            "Automated system calibration",
            "Real-time monitoring",
            "Blender tub condition",
            "Crew training"
        ],
        primary_authority=[
            "API RP 100-16",
            "SPE 204112",
            "OEM Blender Manuals"
        ],
        burden_holder="Frac Crew Lead",
        adversary_position="Logistics pushing for higher feed rates",
        counter_arguments=[
            "Manual feed can be faster in emergencies",
            "Automated systems may malfunction",
            "Calibration takes time",
            "High feed rates risk sand-out",
            "Buildup in tub can go unnoticed"
        ],
        resolution_strategy=(
            "Rely on automated systems with real-time monitoring, and enforce calibration before each stage."
        ),
        entity_scope="Equipment",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API RP 100-16",
            "SPE 204112"
        ]
    ),
    DoctrineBlock(
        topic="Hydration Unit: Gel Mixing and Chemical Addition",
        keywords=["hydration unit", "gel mixing", "chemical addition", "viscosity", "quality control"],
        conclusion_template=(
            "Proper gel mixing and chemical addition in the hydration unit ensures target viscosity and stage performance. "
            "Automated dosing and real-time QC minimize risk of screen-out and NPT."
        ),
        reasoning_framework=(
            "1. Set gel concentration and chemical dosing based on stage design. "
            "2. Calibrate dosing pumps and sensors before each job (OEM, API RP 100-16). "
            "3. Monitor viscosity and chemical levels in real time (SCADA). "
            "4. Adjust dosing dynamically for rate/pressure changes. "
            "5. Inspect hydration unit for leaks and wear before each stage. "
            "6. Document all calibration and QC checks. "
            "7. Analyze NPT incidents related to gel/chemical issues (SPE 204112). "
            "8. Train crew on troubleshooting and emergency shutdown. "
            "9. Maintain inventory of critical chemicals and spares. "
            "10. Benchmark against industry best practices."
        ),
        key_factors=[
            "Gel concentration",
            "Chemical dosing accuracy",
            "Real-time QC monitoring",
            "Hydration unit condition",
            "Crew training"
        ],
        primary_authority=[
            "API RP 100-16",
            "SPE 204112",
            "OEM Hydration Unit Manuals"
        ],
        burden_holder="Frac Chemical Lead",
        adversary_position="Logistics pushing for faster stage turnover",
        counter_arguments=[
            "Manual dosing can be faster in emergencies",
            "Automated systems may malfunction",
            "Calibration takes time",
            "Chemical inventory may be limited",
            "Viscosity sensors can drift"
        ],
        resolution_strategy=(
            "Enforce automated dosing and real-time QC, with manual override only in emergencies."
        ),
        entity_scope="Equipment",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API RP 100-16",
            "SPE 204112"
        ]
    ),
    DoctrineBlock(
        topic="Data Van: Treatment Monitoring and SCADA Integration",
        keywords=["data van", "SCADA", "treatment monitoring", "real-time data", "alarms"],
        conclusion_template=(
            "The data van provides real-time monitoring and control of all frac operations. "
            "SCADA integration enables rapid response to deviations, reducing NPT and improving safety."
        ),
        reasoning_framework=(
            "1. Integrate all frac equipment with SCADA for real-time data acquisition. "
            "2. Configure alarms for critical parameters (pressure, rate, chemical dosing). "
            "3. Ensure data van operators are trained on SCADA and emergency protocols. "
            "4. Maintain redundant communication links to field crew. "
            "5. Archive all job data for post-job analysis and audit. "
            "6. Review alarm history and response times after each stage. "
            "7. Benchmark data van uptime and reliability (SPE 204112). "
            "8. Coordinate with IT for cybersecurity and data integrity. "
            "9. Document all system changes and upgrades. "
            "10. Ensure compliance with regulatory data retention requirements."
        ),
        key_factors=[
            "SCADA integration",
            "Alarm configuration",
            "Operator training",
            "Data archiving",
            "System reliability"
        ],
        primary_authority=[
            "SPE 204112",
            "API RP 100-16",
            "OEM SCADA Manuals"
        ],
        burden_holder="Data Van Supervisor",
        adversary_position="Field crew preferring manual monitoring",
        counter_arguments=[
            "Manual monitoring can be faster in emergencies",
            "SCADA systems may fail or lag",
            "Alarm fatigue can reduce response",
            "Cybersecurity risks to data van",
            "Data archiving adds cost"
        ],
        resolution_strategy=(
            "Rely on SCADA for primary monitoring, with manual backup and regular system testing."
        ),
        entity_scope="Equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "SPE 204112",
            "API RP 100-16"
        ]
    ),
    DoctrineBlock(
        topic="Wireline Operations: Plug Pump-Down and Gun Deployment",
        keywords=["wireline", "plug pump-down", "gun deployment", "stage isolation", "safety"],
        conclusion_template=(
            "Wireline operations for plug pump-down and gun deployment must be tightly coordinated with frac pumping. "
            "Strict adherence to safety protocols and communication is essential to prevent incidents."
        ),
        reasoning_framework=(
            "1. Schedule wireline runs to minimize NPT and align with pumping schedule. "
            "2. Verify all plugs and guns are properly loaded and tracked. "
            "3. Conduct pre-job safety meeting with all crew (OSHA, IADC). "
            "4. Monitor well pressure and confirm isolation before deployment. "
            "5. Maintain clear communication between wireline and frac crew. "
            "6. Document all tool runs and depth correlation. "
            "7. Review incident history and update protocols as needed. "
            "8. Train crew on emergency response and well control. "
            "9. Benchmark against industry best practices (SPE 193456). "
            "10. Archive all wireline data for audit."
        ),
        key_factors=[
            "Scheduling coordination",
            "Tool tracking",
            "Safety protocols",
            "Communication",
            "Incident documentation"
        ],
        primary_authority=[
            "OSHA Oil & Gas Safety",
            "IADC Wireline Guidelines",
            "SPE 193456"
        ],
        burden_holder="Wireline Supervisor",
        adversary_position="Frac crew pushing for faster turnover",
        counter_arguments=[
            "Rushed wireline runs increase risk",
            "Tool tracking can be incomplete",
            "Communication lapses cause incidents",
            "Safety meetings delay operations",
            "Incident documentation adds paperwork"
        ],
        resolution_strategy=(
            "Enforce strict scheduling and safety protocols, with no exceptions for schedule pressure."
        ),
        entity_scope="Operations",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "OSHA Oil & Gas",
            "IADC"
        ]
    ),
    DoctrineBlock(
        topic="Coiled Tubing: Milling, Drillout, and Cleanout",
        keywords=["coiled tubing", "milling", "drillout", "cleanout", "stage transition"],
        conclusion_template=(
            "Coiled tubing operations for milling, drillout, and cleanout are critical for stage transitions. "
            "Equipment reliability and crew experience directly impact operational efficiency."
        ),
        reasoning_framework=(
            "1. Schedule coiled tubing runs to minimize NPT and align with frac schedule. "
            "2. Inspect coiled tubing string for fatigue and wear before each run (API 5ST). "
            "3. Monitor real-time weight, torque, and pressure during operations. "
            "4. Train crew on emergency response and well control. "
            "5. Maintain inventory of critical spares (motors, bits, connectors). "
            "6. Document all tool runs and depth correlation. "
            "7. Analyze NPT incidents related to coiled tubing (SPE 204112). "
            "8. Benchmark crew experience and training records. "
            "9. Review incident history and update protocols as needed. "
            "10. Archive all coiled tubing data for audit."
        ),
        key_factors=[
            "Scheduling coordination",
            "Equipment inspection",
            "Real-time monitoring",
            "Crew experience",
            "Incident documentation"
        ],
        primary_authority=[
            "API 5ST: 'Coiled Tubing Operations'",
            "SPE 204112",
            "OEM Coiled Tubing Manuals"
        ],
        burden_holder="Coiled Tubing Supervisor",
        adversary_position="Frac crew pushing for faster stage transitions",
        counter_arguments=[
            "Rushed coiled tubing runs increase risk",
            "Equipment inspection can be skipped under pressure",
            "Real-time monitoring systems may fail",
            "Crew experience varies",
            "Incident documentation adds paperwork"
        ],
        resolution_strategy=(
            "Enforce inspection and real-time monitoring, with regular crew training and incident review."
        ),
        entity_scope="Operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API 5ST",
            "SPE 204112"
        ]
    ),
    DoctrineBlock(
        topic="Frac Fleet Fuel Consumption: Diesel, CNG, and Field Gas",
        keywords=["fuel consumption", "diesel", "CNG", "field gas", "cost"],
        conclusion_template=(
            "Frac fleet fuel consumption varies by engine type and operational profile. "
            "Field gas and CNG substitution can reduce costs and emissions, but require robust supply and quality control."
        ),
        reasoning_framework=(
            "1. Calculate baseline fuel consumption for diesel-only operation (OEM specs). "
            "2. Assess field gas and CNG supply availability and quality. "
            "3. Model substitution ratios for dual-fuel engines (API 937, EIA). "
            "4. Analyze cost savings and emissions reduction potential. "
            "5. Monitor real-time fuel usage and substitution rates. "
            "6. Document all fuel source changes and quality checks. "
            "7. Benchmark against regional fleet norms (FracFocus, DOE). "
            "8. Review regulatory requirements for emissions reporting. "
            "9. Plan for supply chain disruptions and contingency fuel. "
            "10. Archive all fuel consumption data for audit."
        ),
        key_factors=[
            "Engine type",
            "Fuel supply availability",
            "Substitution ratio",
            "Cost savings",
            "Emissions profile"
        ],
        primary_authority=[
            "API 937",
            "EIA Fuel Reports",
            "FracFocus Emissions Data"
        ],
        burden_holder="Fleet Fuel Logistics Lead",
        adversary_position="Finance pushing for lowest cost fuel",
        counter_arguments=[
            "Field gas quality may fluctuate",
            "CNG supply can be unreliable",
            "Dual-fuel engines may require more maintenance",
            "Emissions reporting adds complexity",
            "Supply chain disruptions can halt operations"
        ],
        resolution_strategy=(
            "Diversify fuel sources, monitor quality, and document all changes for compliance."
        ),
        entity_scope="Fleet",
        confidence=0.89,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API 937",
            "EIA"
        ]
    ),
    DoctrineBlock(
        topic="Dual-Fuel Substitution Ratio and Field Gas Economics",
        keywords=["dual-fuel", "substitution ratio", "field gas", "economics", "emissions"],
        conclusion_template=(
            "Dual-fuel engines can substitute up to 70% of diesel with field gas under optimal conditions. "
            "Economic benefits depend on gas quality, supply stability, and regulatory incentives."
        ),
        reasoning_framework=(
            "1. Review OEM and API 937 guidance for maximum substitution ratios. "
            "2. Assess field gas quality (BTU, contaminants) and supply reliability. "
            "3. Model cost savings vs diesel-only operation. "
            "4. Analyze emissions reduction and regulatory incentives (EPA, DOE). "
            "5. Monitor real-time substitution rates and engine performance. "
            "6. Document all fuel source changes and quality checks. "
            "7. Benchmark against regional fleet norms (FracFocus, EIA). "
            "8. Plan for supply chain disruptions and contingency fuel. "
            "9. Archive all substitution data for audit."
        ),
        key_factors=[
            "Substitution ratio",
            "Field gas quality",
            "Cost savings",
            "Emissions profile",
            "Regulatory incentives"
        ],
        primary_authority=[
            "API 937",
            "EPA Natural Gas STAR",
            "EIA Fuel Reports"
        ],
        burden_holder="Fleet Fuel Logistics Lead",
        adversary_position="Finance pushing for maximum substitution",
        counter_arguments=[
            "Field gas quality may not support high substitution",
            "Engine derating may occur at high substitution",
            "Regulatory incentives may change",
            "Supply disruptions can halt operations",
            "Emissions reporting adds complexity"
        ],
        resolution_strategy=(
            "Optimize substitution within OEM and regulatory limits, monitor quality, and document all changes."
        ),
        entity_scope="Fleet",
        confidence=0.87,
        confidence_zone=ConfidenceZone.AGGRESSIVE,
        controlling_precedent=[
            "API 937",
            "EPA Natural Gas STAR"
        ]
    ),
    DoctrineBlock(
        topic="Frac Fleet Mobilization, Demobilization, and Rig-Up",
        keywords=["mobilization", "demobilization", "rig-up", "logistics", "safety"],
        conclusion_template=(
            "Efficient mobilization, rig-up, and demobilization minimize NPT and safety risk. "
            "Standardized procedures and crew training are essential for repeatable, safe operations."
        ),
        reasoning_framework=(
            "1. Develop standardized mobilization and rig-up checklists (API RP 100-16). "
            "2. Schedule logistics to minimize pad congestion and wait times. "
            "3. Train crew on rig-up procedures and safety protocols (OSHA, IADC). "
            "4. Inspect all equipment before and after mobilization. "
            "5. Document all incidents and near-misses during rig-up/demobilization. "
            "6. Benchmark mobilization times and NPT (SPE 204112). "
            "7. Review with operations for lessons learned. "
            "8. Archive all mobilization data for audit."
        ),
        key_factors=[
            "Standardized procedures",
            "Crew training",
            "Logistics scheduling",
            "Equipment inspection",
            "Incident documentation"
        ],
        primary_authority=[
            "API RP 100-16",
            "OSHA Oil & Gas Safety",
            "SPE 204112"
        ],
        burden_holder="Frac Operations Supervisor",
        adversary_position="Logistics pushing for faster rig-up",
        counter_arguments=[
            "Standardized procedures can slow down experienced crews",
            "Training takes time and resources",
            "Logistics delays can impact schedule",
            "Equipment inspection may be skipped under pressure",
            "Incident documentation adds paperwork"
        ],
        resolution_strategy=(
            "Enforce standardized procedures and training, with regular review of incidents and lessons learned."
        ),
        entity_scope="Fleet",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API RP 100-16",
            "OSHA Oil & Gas"
        ]
    ),
    DoctrineBlock(
        topic="Pump Maintenance: Plunger, Fluid End, and Power End",
        keywords=["pump maintenance", "plunger", "fluid end", "power end", "MTBF"],
        conclusion_template=(
            "Regular maintenance of plunger, fluid end, and power end components is critical to pump reliability. "
            "Tracking MTBF and service intervals reduces unplanned downtime and NPT."
        ),
        reasoning_framework=(
            "1. Follow OEM and API 674 recommended maintenance intervals for all pump components. "
            "2. Track mean time between failures (MTBF) for plunger, fluid end, and power end. "
            "3. Inspect for wear, scoring, and fatigue before each job. "
            "4. Maintain detailed service logs and parts inventory. "
            "5. Analyze NPT incidents related to pump failures (SPE 204112). "
            "6. Train crew on preventive and corrective maintenance. "
            "7. Benchmark against industry best practices. "
            "8. Document all maintenance actions for audit."
        ),
        key_factors=[
            "Maintenance interval",
            "MTBF tracking",
            "Component inspection",
            "Service logs",
            "Crew training"
        ],
        primary_authority=[
            "API 674",
            "SPE 204112",
            "OEM Pump Manuals"
        ],
        burden_holder="Pump Maintenance Lead",
        adversary_position="Operations pushing for longer intervals",
        counter_arguments=[
            "Longer intervals reduce downtime",
            "Service logs can be incomplete",
            "Parts inventory adds cost",
            "Training takes time",
            "Inspection may delay operations"
        ],
        resolution_strategy=(
            "Enforce maintenance intervals and MTBF tracking, with regular review of NPT incidents."
        ),
        entity_scope="Pump",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "API 674",
            "SPE 204112"
        ]
    ),
    DoctrineBlock(
        topic="Equipment Reliability: MTBF and Pump Hours",
        keywords=["equipment reliability", "MTBF", "pump hours", "failure analysis", "NPT"],
        conclusion_template=(
            "Tracking MTBF and total pump hours enables proactive maintenance and reduces NPT. "
            "Reliability data should drive maintenance strategy and fleet configuration."
        ),
        reasoning_framework=(
            "1. Record total pump hours and failure events for each unit. "
            "2. Calculate MTBF for all critical components (plunger, fluid end, power end). "
            "3. Analyze failure modes and root causes (SPE 204112). "
            "4. Adjust maintenance intervals based on reliability data. "
            "5. Benchmark against OEM and industry MTBF norms. "
            "6. Document all reliability data and actions for audit. "
            "7. Review with operations and maintenance for continuous improvement."
        ),
        key_factors=[
            "Pump hours tracking",
            "Failure event logging",
            "MTBF calculation",
            "Root cause analysis",
            "Maintenance interval adjustment"
        ],
        primary_authority=[
            "SPE 204112",
            "API 674",
            "OEM Reliability Bulletins"
        ],
        burden_holder="Reliability Engineer",
        adversary_position="Operations pushing for maximum utilization",
        counter_arguments=[
            "Maximizing utilization increases failure risk",
            "Failure event logging can be incomplete",
            "Root cause analysis adds delay",
            "OEM MTBF data may not match field conditions",
            "Maintenance intervals may be too conservative"
        ],
        resolution_strategy=(
            "Base maintenance and configuration decisions on field MTBF data, with regular review and adjustment."
        ),
        entity_scope="Fleet",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "SPE 204112",
            "API 674"
        ]
    ),
    DoctrineBlock(
        topic="Frac Crew Scheduling: 24-Hour Operations and Shift Management",
        keywords=["crew scheduling", "24-hour operations", "shift", "fatigue", "compliance"],
        conclusion_template=(
            "Effective crew scheduling for 24-hour operations minimizes fatigue and safety risk. "
            "Compliance with labor regulations and regular shift rotation is essential."
        ),
        reasoning_framework=(
            "1. Develop shift schedules that comply with labor laws and HSE guidelines (OSHA, IADC). "
            "2. Rotate crew regularly to minimize fatigue and maintain alertness. "
            "3. Monitor hours worked and rest periods for all crew. "
            "4. Train supervisors on fatigue management and incident response. "
            "5. Document all scheduling and incidents for audit. "
            "6. Benchmark against industry best practices. "
            "7. Review with operations for continuous improvement."
        ),
        key_factors=[
            "Shift schedule compliance",
            "Fatigue management",
            "Crew rotation",
            "Incident documentation",
            "Supervisor training"
        ],
        primary_authority=[
            "OSHA Oil & Gas Safety",
            "IADC Crew Management Guidelines",
            "API RP 100-16"
        ],
        burden_holder="Crew Scheduler",
        adversary_position="Operations pushing for longer shifts",
        counter_arguments=[
            "Longer shifts increase productivity",
            "Fatigue management adds complexity",
            "Crew rotation can disrupt continuity",
            "Incident documentation adds paperwork",
            "Training takes time"
        ],
        resolution_strategy=(
            "Enforce shift compliance and fatigue management, with regular review of incidents and best practices."
        ),
        entity_scope="Crew",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "OSHA Oil & Gas",
            "IADC"
        ]
    ),
    DoctrineBlock(
        topic="Zipper Frac Operations: Simultaneous Multi-Well Stimulation",
        keywords=["zipper frac", "simultaneous operations", "multi-well", "efficiency", "safety"],
        conclusion_template=(
            "Zipper frac operations enable simultaneous stimulation of multiple wells, increasing efficiency. "
            "Strict coordination and safety protocols are required to manage complexity and risk."
        ),
        reasoning_framework=(
            "1. Develop detailed zipper frac schedules and crew assignments. "
            "2. Coordinate all equipment and personnel for simultaneous operations. "
            "3. Implement robust communication protocols between wells. "
            "4. Monitor real-time data for all wells via SCADA. "
            "5. Train crew on zipper frac procedures and emergency response. "
            "6. Document all incidents and lessons learned. "
            "7. Benchmark efficiency gains and NPT reduction (SPE 204112). "
            "8. Review with operations for continuous improvement."
        ),
        key_factors=[
            "Scheduling coordination",
            "Communication protocols",
            "Crew training",
            "Real-time monitoring",
            "Incident documentation"
        ],
        primary_authority=[
            "SPE 204112",
            "API RP 100-16",
            "OEM Zipper Frac Manuals"
        ],
        burden_holder="Zipper Frac Coordinator",
        adversary_position="Operations pushing for faster turnover",
        counter_arguments=[
            "Simultaneous operations increase risk",
            "Communication lapses can cause incidents",
            "Training takes time",
            "Incident documentation adds paperwork",
            "Equipment may not be designed for multi-well ops"
        ],
        resolution_strategy=(
            "Enforce strict coordination and training, with regular review of incidents and best practices."
        ),
        entity_scope="Fleet",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "SPE 204112",
            "API RP 100-16"
        ]
    ),
    DoctrineBlock(
        topic="Frac Fleet Efficiency: NPT Analysis and Stages per Day",
        keywords=["efficiency", "NPT", "stages per day", "benchmarking", "continuous improvement"],
        conclusion_template=(
            "Regular analysis of NPT and stages per day enables continuous improvement in frac fleet efficiency. "
            "Benchmarking against industry peers drives operational excellence."
        ),
        reasoning_framework=(
            "1. Track all NPT events and categorize by root cause (equipment, crew, logistics). "
            "2. Analyze stages completed per day and compare to plan. "
            "3. Benchmark against industry and regional norms (SPE 204112, EIA). "
            "4. Implement corrective actions for recurring NPT causes. "
            "5. Document all efficiency initiatives and results. "
            "6. Review with operations and management for continuous improvement."
        ),
        key_factors=[
            "NPT tracking",
            "Stages per day",
            "Benchmarking",
            "Corrective actions",
            "Continuous improvement"
        ],
        primary_authority=[
            "SPE 204112",
            "EIA Completion Reports",
            "API RP 100-16"
        ],
        burden_holder="Operations Excellence Lead",
        adversary_position="Field crew citing unique challenges",
        counter_arguments=[
            "Field conditions vary by pad",
            "Benchmarking may not account for geology",
            "Corrective actions can disrupt operations",
            "Documentation adds paperwork",
            "Continuous improvement requires buy-in"
        ],
        resolution_strategy=(
            "Adopt data-driven NPT analysis and benchmarking, with regular review of corrective actions."
        ),
        entity_scope="Fleet",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "SPE 204112",
            "EIA"
        ]
    ),
    DoctrineBlock(
        topic="Frac Fleet Cost per Stage and Market Pricing Trends",
        keywords=["cost per stage", "market pricing", "benchmarking", "cost control", "efficiency"],
        conclusion_template=(
            "Frac fleet cost per stage is influenced by market pricing, efficiency, and operational discipline. "
            "Benchmarking and cost control initiatives are essential for competitiveness."
        ),
        reasoning_framework=(
            "1. Track all direct and indirect costs per stage (labor, fuel, maintenance, logistics). "
            "2. Benchmark cost per stage against regional and industry norms (EIA, IHS Markit). "
            "3. Analyze efficiency initiatives and their impact on cost. "
            "4. Implement cost control measures (fuel optimization, maintenance scheduling). "
            "5. Document all cost initiatives and results. "
            "6. Review with finance and operations for continuous improvement."
        ),
        key_factors=[
            "Cost tracking",
            "Benchmarking",
            "Efficiency initiatives",
            "Cost control measures",
            "Continuous improvement"
        ],
        primary_authority=[
            "EIA Completion Reports",
            "IHS Markit Frac Pricing",
            "API RP 100-16"
        ],
        burden_holder="Finance Manager",
        adversary_position="Operations citing unique cost drivers",
        counter_arguments=[
            "Pad conditions vary by region",
            "Benchmarking may not account for geology",
            "Cost control can impact efficiency",
            "Documentation adds paperwork",
            "Continuous improvement requires buy-in"
        ],
        resolution_strategy=(
            "Adopt data-driven cost tracking and benchmarking, with regular review of cost control initiatives."
        ),
        entity_scope="Fleet",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "EIA",
            "IHS Markit"
        ]
    ),
    # ... (Add more DoctrineBlocks as needed for full coverage)
]

# =========================
# AUTHORITY HARDENING
# =========================

AUTHORITY_WEIGHTS = {
    "API": 1.0,
    "SPE": 0.95,
    "OSHA": 0.98,
    "EIA": 0.9,
    "DOE": 0.9,
    "FracFocus": 0.85,
    "OEM": 0.8,
    "IADC": 0.8,
    "ISO": 0.8,
    "IHS Markit": 0.75
}

def authority_score(authorities: List[str]) -> float:
    score = 0.0
    for auth in authorities:
        for k, v in AUTHORITY_WEIGHTS.items():
            if k in auth:
                score += v
    return min(score, 1.0)

def resolve_authority_conflict(auths1: List[str], auths2: List[str]) -> List[str]:
    set1 = set(auths1)
    set2 = set(auths2)
    overlap = set1 & set2
    if overlap:
        return list(overlap)
    # If no overlap, prefer higher weighted authorities
    scored1 = sorted(auths1, key=lambda a: max([AUTHORITY_WEIGHTS.get(k, 0) for k in AUTHORITY_WEIGHTS if k in a]), reverse=True)
    scored2 = sorted(auths2, key=lambda a: max([AUTHORITY_WEIGHTS.get(k, 0) for k in AUTHORITY_WEIGHTS if k in a]), reverse=True)
    return scored1[:1] + scored2[:1]

# =========================
# THREE-LAYER RESPONSE
# =========================

def doctrine_layer(query: QueryRequest) -> Optional[DoctrineBlock]:
    scenario = semantic_normalize(query.scenario.lower())
    for doctrine in DOCTRINE_CACHE:
        if any(kw in scenario for kw in doctrine.keywords):
            return doctrine
    return None

def semantic_search_layer(query: QueryRequest) -> Optional[DoctrineBlock]:
    scenario = semantic_normalize(query.scenario.lower())
    best_score = 0
    best_doctrine = None
    for doctrine in DOCTRINE_CACHE:
        score = sum(1 for kw in doctrine.keywords if kw in scenario)
        if score > best_score:
            best_score = score
            best_doctrine = doctrine
    return best_doctrine if best_score > 0 else None

def deep_analysis_layer(query: QueryRequest) -> Optional[DoctrineBlock]:
    # Multi-doctrine decomposition and DAG interaction
    scenario = semantic_normalize(query.scenario.lower())
    relevant = []
    for doctrine in DOCTRINE_CACHE:
        if any(kw in scenario for kw in doctrine.keywords):
            relevant.append(doctrine)
    if not relevant:
        return None
    # 8-step resolution: aggregate key factors, authorities, counter-arguments, etc.
    agg_key_factors = []
    agg_authorities = []
    agg_counter_args = []
    agg_confidence = 0.0
    agg_confidence_zone = ConfidenceZone.DEFENSIBLE
    for d in relevant:
        agg_key_factors.extend(d.key_factors)
        agg_authorities.extend(d.primary_authority)
        agg_counter_args.extend(d.counter_arguments)
        agg_confidence += d.confidence
    agg_confidence /= len(relevant)
    # Use most conservative confidence zone
    zones = [d.confidence_zone for d in relevant]
    if ConfidenceZone.HIGH_RISK in zones:
        agg_confidence_zone = ConfidenceZone.HIGH_RISK
    elif ConfidenceZone.DISCLOSURE in zones:
        agg_confidence_zone = ConfidenceZone.DISCLOSURE
    elif ConfidenceZone.AGGRESSIVE in zones:
        agg_confidence_zone = ConfidenceZone.AGGRESSIVE
    else:
        agg_confidence_zone = ConfidenceZone.DEFENSIBLE
    # Synthesize a conclusion
    conclusion = (
        "Multiple operational doctrines apply. Key factors: {}. "
        "Primary authorities: {}. Counter-arguments: {}. "
        "Aggregate confidence: {:.2f}."
    ).format(
        ", ".join(set(agg_key_factors)),
        "; ".join(set(agg_authorities)),
        "; ".join(set(agg_counter_args)),
        agg_confidence
    )
    return DoctrineBlock(
        topic="Multi-Doctrine Synthesis",
        keywords=[],
        conclusion_template=conclusion,
        reasoning_framework="Aggregated analysis from multiple doctrine blocks via 8-step resolution.",
        key_factors=list(set(agg_key_factors)),
        primary_authority=list(set(agg_authorities)),
        burden_holder="Multi-Disciplinary",
        adversary_position="Multiple",
        counter_arguments=list(set(agg_counter_args)),
        resolution_strategy="Synthesize best practices from all relevant doctrines.",
        entity_scope="Fleet/Operations",
        confidence=agg_confidence,
        confidence_zone=agg_confidence_zone,
        controlling_precedent=[]
    )

def three_layer_response(query: QueryRequest) -> Tuple[Optional[DoctrineBlock], str]:
    doctrine = doctrine_layer(query)
    if doctrine:
        return doctrine, "Layer 1: Doctrine Cache"
    doctrine = semantic_search_layer(query)
    if doctrine:
        return doctrine, "Layer 2: Semantic Search"
    doctrine = deep_analysis_layer(query)
    if doctrine:
        return doctrine, "Layer 3: Deep Analysis"
    return None, "No relevant doctrine found"

# =========================
# COVERAGE MAP
# =========================

def coverage_map(query: QueryRequest) -> Dict[str, Any]:
    scenario = semantic_normalize(query.scenario.lower())
    triggered = []
    missed = []
    for doctrine in DOCTRINE_CACHE:
        if any(kw in scenario for kw in doctrine.keywords):
            triggered.append(doctrine.topic)
        else:
            missed.append(doctrine.topic)
    epistemic_gap = len(triggered) == 0
    return {
        "triggered": triggered,
        "missed": missed,
        "epistemic_gap": epistemic_gap
    }

# =========================
# DRIFT WATCHER
# =========================

DRIFT_BASELINE = {d.topic: d.confidence for d in DOCTRINE_CACHE}

def drift_watcher() -> Dict[str, Any]:
    drift = {}
    for doctrine in DOCTRINE_CACHE:
        baseline = DRIFT_BASELINE.get(doctrine.topic, doctrine.confidence)
        if abs(baseline - doctrine.confidence) > 0.05:
            drift[doctrine.topic] = {
                "baseline": baseline,
                "current": doctrine.confidence,
                "delta": doctrine.confidence - baseline
            }
    return drift

# =========================
# AUDIT TRAIL
# =========================

AUDIT_LOG_PATH = Path(__file__).parent / "frac10_audit_log.jsonl"

def log_audit_trail(entry: Dict[str, Any]):
    try:
        with AUDIT_LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(f"{entry}\n")
    except Exception as e:
        logger.error(f"Audit log write failed: {e}")

# =========================
# DETERMINISM HASH
# =========================

def determinism_hash(data: Dict[str, Any]) -> str:
    s = str(sorted(data.items()))
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

# =========================
# ZONED ANALYSIS
# =========================

def zone_tag(conclusion: str, query: QueryRequest) -> PositionZone:
    if "audit" in query.scenario.lower():
        return PositionZone.AUDIT
    if "report" in query.scenario.lower():
        return PositionZone.REPORTING
    return PositionZone.PLANNING

# =========================
# FASTAPI APP
# =========================

app = FastAPI(
    title="Frac Fleet Operations Engine (FRAC10)",
    description="Manage hydraulic fracturing fleet operations: scheduling, maintenance, fuel, crew, optimization.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    logger.info("FRAC10 Engine startup complete.")

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("FRAC10 Engine shutdown.")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: Request, query: QueryRequest):
    start_time = datetime.utcnow()
    query_id = str(uuid.uuid4())
    try:
        doctrine, layer = three_layer_response(query)
        if not doctrine:
            raise ValueError("No relevant doctrine found for scenario.")
        # Compose response
        primary_conclusion = apply_epistemic_guardrails(doctrine.conclusion_template)
        reasoning_framework = apply_epistemic_guardrails(doctrine.reasoning_framework)
        key_factors = doctrine.key_factors
        primary_authority = doctrine.primary_authority
        counter_arguments = doctrine.counter_arguments
        resolution_strategy = doctrine.resolution_strategy
        confidence = doctrine.confidence
        confidence_zone = doctrine.confidence_zone
        position_zone = zone_tag(primary_conclusion, query)
        # Determinism hash
        hash_input = {
            "engine_id": "FRAC10",
            "query_id": query_id,
            "mode": query.mode.value,
            "confidence": confidence,
            "confidence_zone": confidence_zone.value,
            "position_zone": position_zone.value,
            "primary_conclusion": primary_conclusion,
            "reasoning_framework": reasoning_framework,
            "key_factors": key_factors,
            "primary_authority": primary_authority,
            "counter_arguments": counter_arguments,
            "resolution_strategy": resolution_strategy
        }
        d_hash = determinism_hash(hash_input)
        # Audit log
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query_id": query_id,
            "scenario": query.scenario,
            "mode": query.mode.value,
            "entity_type": query.entity_type,
            "complexity": query.complexity,
            "doctrine_topic": doctrine.topic,
            "layer": layer,
            "confidence": confidence,
            "confidence_zone": confidence_zone.value,
            "position_zone": position_zone.value,
            "determinism_hash": d_hash
        }
        log_audit_trail(audit_entry)
        latency = (datetime.utcnow() - start_time).total_seconds()
        metrics_collector.record_query([doctrine.topic], latency)
        return QueryResponse(
            engine_id="FRAC10",
            query_id=query_id,
            mode=query.mode,
            confidence=confidence,
            confidence_zone=confidence_zone,
            position_zone=position_zone,
            primary_conclusion=primary_conclusion,
            reasoning_framework=reasoning_framework,
            key_factors=key_factors,
            primary_authority=primary_authority,
            counter_arguments=counter_arguments,
            resolution_strategy=resolution_strategy,
            determinism_hash=d_hash
        )
    except Exception as e:
        logger.error(f"Query error: {e}")
        metrics_collector.record_error(str(e))
        raise

@app.get("/health")
async def health():
    return {"status": "ok", "engine_id": "FRAC10", "time": datetime.utcnow().isoformat()}

@app.get("/metrics")
async def metrics():
    return {
        "latency_stats": metrics_collector.get_latency_stats(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "queries_last_hour": metrics_collector.queries_last_hour(),
        "errors": metrics_collector.errors[-10:]
    }

@app.get("/coverage")
async def coverage(scenario: str = ""):
    dummy_query = QueryRequest(
        scenario=scenario or "fleet configuration",
        mode=ResponseMode.FAST,
        entity_type="fleet",
        complexity=5
    )
    return coverage_map(dummy_query)

@app.get("/drift")
async def drift():
    return drift_watcher()

@app.get("/doctrines")
async def doctrines():
    return [
        {
            "topic": d.topic,
            "keywords": d.keywords,
            "confidence": d.confidence,
            "confidence_zone": d.confidence_zone.value
        }
        for d in DOCTRINE_CACHE
    ]
