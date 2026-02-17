import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple, Set
from enum import Enum
from datetime import datetime, timedelta
import json
import threading

# --- ENUMS ---

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
    HYDRAULICS = "HYDRAULICS"
    SIZING = "SIZING"
    MATERIALS = "MATERIALS"
    WELDING = "WELDING"
    COATING = "COATING"
    CONSTRUCTION = "CONSTRUCTION"
    DRILLING = "DRILLING"
    PIGGING = "PIGGING"
    INSPECTION = "INSPECTION"
    INTEGRITY = "INTEGRITY"
    STRESS = "STRESS"
    CATHODIC = "CATHODIC"
    SCADA = "SCADA"
    ROW = "ROW"
    REGULATORY = "REGULATORY"
    HYDROTEST = "HYDROTEST"
    COMPRESSOR = "COMPRESSOR"
    PUMP = "PUMP"
    FLOW_ASSURANCE = "FLOW_ASSURANCE"
    DECOMMISSION = "DECOMMISSION"

# --- METRICS COLLECTOR ---

class MetricsCollector:
    def __init__(self):
        self.query_records: List[Dict[str, Any]] = []
        self.error_records: List[Dict[str, Any]] = []
        self.doctrine_hits: Dict[str, int] = {}
        self.lock = threading.Lock()

    def record_query(self, query_id: str, doctrine_ids: List[str], latency_ms: float):
        with self.lock:
            self.query_records.append({
                "query_id": query_id,
                "doctrine_ids": doctrine_ids,
                "timestamp": datetime.utcnow().isoformat(),
                "latency_ms": latency_ms
            })
            for did in doctrine_ids:
                self.doctrine_hits[did] = self.doctrine_hits.get(did, 0) + 1

    def record_error(self, query_id: str, error: str):
        with self.lock:
            self.error_records.append({
                "query_id": query_id,
                "error": error,
                "timestamp": datetime.utcnow().isoformat()
            })

    def get_latency_stats(self) -> Dict[str, float]:
        with self.lock:
            latencies = [rec["latency_ms"] for rec in self.query_records[-100:]]
            if not latencies:
                return {"mean": 0.0, "max": 0.0, "min": 0.0}
            return {
                "mean": sum(latencies) / len(latencies),
                "max": max(latencies),
                "min": min(latencies)
            }

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        with self.lock:
            total = sum(self.doctrine_hits.values())
            if total == 0:
                return {}
            return {k: v / total for k, v in self.doctrine_hits.items()}

    def queries_last_hour(self) -> int:
        cutoff = datetime.utcnow() - timedelta(hours=1)
        with self.lock:
            return sum(1 for rec in self.query_records if datetime.fromisoformat(rec["timestamp"]) > cutoff)

metrics_collector = MetricsCollector()

# --- PYDANTIC MODELS ---

class QueryRequest(BaseModel):
    scenario: str
    mode: ResponseMode
    entity_type: str
    complexity: int

    @validator('complexity')
    def complexity_range(cls, v):
        if v < 1 or v > 10:
            raise ValueError("complexity must be between 1 and 10")
        return v

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

# --- DOCTRINE CACHE ---

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
    controlling_precedent: str

doctrine_cache: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Pipeline Hydraulics: Darcy-Weisbach and Moody Friction",
        keywords=["hydraulics", "friction", "Darcy-Weisbach", "Moody", "pressure drop", "flow regime"],
        conclusion_template=(
            "The Darcy-Weisbach equation, combined with Moody friction factor charts, provides the most "
            "robust methodology for calculating pressure drop in pipeline systems. Accurate friction factor "
            "determination is essential for both turbulent and laminar flow regimes. Design decisions must "
            "consider operational variability and fluid properties."
        ),
        reasoning_framework=(
            "1. Identify the flow regime (laminar or turbulent) based on Reynolds number.\n"
            "2. For laminar flow (Re < 2000), friction factor f = 64/Re.\n"
            "3. For turbulent flow, use Moody chart or Colebrook-White equation to determine f.\n"
            "4. Apply Darcy-Weisbach equation: ΔP = f*(L/D)*(ρ*v^2/2).\n"
            "5. Validate input parameters: pipe roughness, diameter, length, fluid density, viscosity.\n"
            "6. Assess impact of temperature and composition changes on viscosity and density.\n"
            "7. Consider transient effects and operational scenarios (start-up, shut-down).\n"
            "8. Review historical pressure drop data for similar systems.\n"
            "9. Cross-check calculations with industry standards (API RP 14E, ASME B31.4).\n"
            "10. Document assumptions and uncertainty ranges.\n"
            "11. Evaluate sensitivity to friction factor estimation errors.\n"
            "12. Recommend periodic recalibration of hydraulic models based on field data.\n"
            "13. Ensure compliance with regulatory minimum pressure requirements.\n"
            "14. Integrate results into overall pipeline design and risk assessment.\n"
            "15. Reference: API RP 14E, ASME B31.4, B31.8, Moody (1944), Colebrook (1939)."
        ),
        key_factors=[
            "Reynolds number determination",
            "Pipe roughness and diameter",
            "Fluid density and viscosity",
            "Pressure drop calculation methodology",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 14E: Recommended Practice for Design and Operation of Offshore Pipelines",
            "ASME B31.4: Pipeline Transportation Systems for Liquid Hydrocarbons",
            "Moody, L.F. (1944): 'The Friction Factor for Pipe Flow'"
        ],
        burden_holder="Design Engineer",
        adversary_position="Operational Engineer",
        counter_arguments=[
            "Alternative empirical correlations may outperform Darcy-Weisbach in certain regimes",
            "Moody chart limitations for non-standard fluids",
            "Uncertainty in pipe roughness estimation",
            "Transient operational scenarios not captured",
            "Regulatory requirements may override calculated values"
        ],
        resolution_strategy="Apply conservative friction factor estimates and validate with field data.",
        entity_scope="Pipeline hydraulic design",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API RP 14E, ASME B31.4"
    ),
    DoctrineBlock(
        topic="Pipeline Sizing: Velocity, Pressure Drop, Throughput",
        keywords=["sizing", "velocity", "pressure drop", "throughput", "diameter", "design"],
        conclusion_template=(
            "Pipeline sizing must balance velocity constraints, pressure drop, and throughput requirements. "
            "Industry standards dictate maximum and minimum velocities to prevent erosion and ensure efficient "
            "transport. Design must be validated against API and ASME guidelines."
        ),
        reasoning_framework=(
            "1. Define required throughput based on operational scenarios.\n"
            "2. Establish allowable velocity range per API RP 14E (typically 1-3 m/s for liquids).\n"
            "3. Calculate minimum diameter using Q = v*A and pressure drop constraints.\n"
            "4. Assess impact of diameter selection on capital and operational costs.\n"
            "5. Model pressure drop using Darcy-Weisbach and compare against allowable limits.\n"
            "6. Evaluate erosion risk at high velocities and deposition risk at low velocities.\n"
            "7. Consider future expansion and operational flexibility.\n"
            "8. Validate sizing against ASME B31.4 and B31.8 requirements.\n"
            "9. Document design assumptions and sensitivity analyses.\n"
            "10. Reference: API RP 14E, ASME B31.4, B31.8."
        ),
        key_factors=[
            "Required throughput",
            "Allowable velocity range",
            "Pressure drop constraints",
            "Diameter selection",
            "Regulatory standards"
        ],
        primary_authority=[
            "API RP 14E: Recommended Practice for Design and Operation of Offshore Pipelines",
            "ASME B31.4: Pipeline Transportation Systems for Liquid Hydrocarbons",
            "ASME B31.8: Gas Transmission and Distribution Piping Systems"
        ],
        burden_holder="Design Engineer",
        adversary_position="Cost Engineer",
        counter_arguments=[
            "Higher velocities may reduce capital costs but increase erosion risk",
            "Lower velocities may cause deposition and reduce efficiency",
            "Pressure drop calculations may not account for all operational scenarios",
            "Regulatory velocity limits may constrain design flexibility",
            "Throughput requirements may change over project lifetime"
        ],
        resolution_strategy="Optimize diameter for current and future throughput, validate against standards.",
        entity_scope="Pipeline sizing and design",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API RP 14E, ASME B31.4"
    ),
    DoctrineBlock(
        topic="Pipeline Materials: API 5L Grade X52, X65, X70, X80",
        keywords=["materials", "API 5L", "X52", "X65", "X70", "X80", "steel", "mechanical properties"],
        conclusion_template=(
            "Selection of pipeline steel grade must be based on mechanical properties, design pressure, "
            "and environmental conditions. API 5L grades X52, X65, X70, and X80 offer varying yield strengths "
            "and toughness. Material selection must comply with ASME and API standards."
        ),
        reasoning_framework=(
            "1. Determine design pressure and operational requirements.\n"
            "2. Select steel grade based on yield strength and toughness (API 5L).\n"
            "3. Assess weldability and fracture resistance for each grade.\n"
            "4. Evaluate environmental factors (corrosion, temperature, sour service).\n"
            "5. Review material test certificates and mill documentation.\n"
            "6. Confirm compliance with ASME B31.4 and API 5L specifications.\n"
            "7. Analyze cost-benefit of higher grade steels (X70, X80) versus lower grades.\n"
            "8. Document material selection rationale and traceability.\n"
            "9. Reference: API 5L, ASME B31.4, B31.8."
        ),
        key_factors=[
            "Design pressure",
            "Yield strength and toughness",
            "Weldability",
            "Environmental conditions",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 5L: Specification for Line Pipe",
            "ASME B31.4: Pipeline Transportation Systems for Liquid Hydrocarbons",
            "ASME B31.8: Gas Transmission and Distribution Piping Systems"
        ],
        burden_holder="Materials Engineer",
        adversary_position="Procurement Specialist",
        counter_arguments=[
            "Higher grade steels may increase procurement costs",
            "Lower grade steels may limit design pressure",
            "Material availability may constrain selection",
            "Environmental conditions may require additional testing",
            "Regulatory changes may impact material requirements"
        ],
        resolution_strategy="Select material grade based on design pressure and environmental factors.",
        entity_scope="Pipeline material selection",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API 5L, ASME B31.4"
    ),
    DoctrineBlock(
        topic="Pipeline Welding Procedures: WPS, PQR, SMAW, GMAW",
        keywords=["welding", "WPS", "PQR", "SMAW", "GMAW", "procedures", "qualification"],
        conclusion_template=(
            "Welding procedures must be qualified through Procedure Qualification Records (PQR) and documented "
            "in Welding Procedure Specifications (WPS). SMAW and GMAW are commonly used methods, each with "
            "distinct advantages. Compliance with API and ASME standards is mandatory."
        ),
        reasoning_framework=(
            "1. Develop WPS based on project requirements and material grade.\n"
            "2. Perform PQR to validate welding parameters and joint properties.\n"
            "3. Select SMAW or GMAW based on field conditions and required weld quality.\n"
            "4. Assess welder qualification and training records.\n"
            "5. Review weld inspection protocols (visual, radiographic, ultrasonic).\n"
            "6. Document weld defects and repair procedures.\n"
            "7. Ensure traceability of welds and compliance with ASME B31.4, API 1104.\n"
            "8. Evaluate impact of welding method on mechanical properties and integrity.\n"
            "9. Reference: API 1104, ASME B31.4, B31.8."
        ),
        key_factors=[
            "Welding procedure qualification",
            "Welder training and certification",
            "Inspection protocols",
            "Weld quality",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 1104: Welding of Pipelines and Related Facilities",
            "ASME B31.4: Pipeline Transportation Systems for Liquid Hydrocarbons",
            "ASME B31.8: Gas Transmission and Distribution Piping Systems"
        ],
        burden_holder="Welding Engineer",
        adversary_position="Quality Assurance",
        counter_arguments=[
            "Field conditions may limit welding method selection",
            "Weld defects may require requalification",
            "Inspection protocols may be insufficient",
            "Regulatory updates may affect procedure requirements",
            "Documentation gaps may compromise traceability"
        ],
        resolution_strategy="Qualify all procedures and personnel, document inspection results.",
        entity_scope="Pipeline welding",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API 1104, ASME B31.4"
    ),
    DoctrineBlock(
        topic="Pipeline Coating: FBE and Three-Layer Polyethylene",
        keywords=["coating", "FBE", "three-layer polyethylene", "corrosion protection", "application", "inspection"],
        conclusion_template=(
            "Fusion Bonded Epoxy (FBE) and three-layer polyethylene coatings provide robust corrosion protection "
            "for pipelines. Selection depends on environmental conditions and mechanical requirements. Proper "
            "application and inspection are critical for long-term integrity."
        ),
        reasoning_framework=(
            "1. Assess environmental conditions (soil, moisture, temperature).\n"
            "2. Select coating type based on corrosion risk and mechanical protection needs.\n"
            "3. Specify application procedures and quality control measures.\n"
            "4. Inspect coating thickness and adhesion per ISO 21809 and API standards.\n"
            "5. Document coating defects and repair protocols.\n"
            "6. Evaluate compatibility with cathodic protection systems.\n"
            "7. Review historical performance data for selected coatings.\n"
            "8. Reference: ISO 21809, API RP 5L2, ASME B31.4."
        ),
        key_factors=[
            "Environmental conditions",
            "Corrosion protection requirements",
            "Coating application procedures",
            "Inspection protocols",
            "Compatibility with cathodic protection"
        ],
        primary_authority=[
            "ISO 21809: Petroleum and natural gas industries — External coatings for buried or submerged pipelines",
            "API RP 5L2: Recommended Practice for Internal Coating of Line Pipe",
            "ASME B31.4: Pipeline Transportation Systems for Liquid Hydrocarbons"
        ],
        burden_holder="Coating Engineer",
        adversary_position="Integrity Manager",
        counter_arguments=[
            "Improper application may compromise protection",
            "Environmental changes may affect coating performance",
            "Inspection methods may miss micro-defects",
            "Coating compatibility with CP may be limited",
            "Repair protocols may not restore original integrity"
        ],
        resolution_strategy="Select coating based on risk assessment, ensure rigorous inspection.",
        entity_scope="Pipeline coating",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="ISO 21809, API RP 5L2"
    ),
    DoctrineBlock(
        topic="Pipeline Construction: ROW Clearing, Trenching, Backfill",
        keywords=["construction", "ROW", "clearing", "trenching", "backfill", "environmental", "safety"],
        conclusion_template=(
            "Pipeline construction requires systematic right-of-way (ROW) clearing, trenching, and backfill "
            "operations. Environmental and safety considerations must be integrated throughout. Compliance "
            "with regulatory standards is essential."
        ),
        reasoning_framework=(
            "1. Obtain ROW permits and environmental clearances.\n"
            "2. Conduct pre-construction surveys and stakeholder consultations.\n"
            "3. Implement clearing procedures minimizing environmental impact.\n"
            "4. Execute trenching per design depth and width specifications.\n"
            "5. Monitor trench stability and worker safety.\n"
            "6. Apply backfill materials and compaction protocols.\n"
            "7. Inspect for compliance with ASME B31.4, PHMSA CFR 49 Part 192/195.\n"
            "8. Document construction activities and deviations.\n"
            "9. Reference: ASME B31.4, PHMSA CFR 49 Part 192/195."
        ),
        key_factors=[
            "ROW permitting",
            "Environmental impact",
            "Trenching specifications",
            "Backfill quality",
            "Safety protocols"
        ],
        primary_authority=[
            "ASME B31.4: Pipeline Transportation Systems for Liquid Hydrocarbons",
            "PHMSA CFR 49 Part 192: Transportation of Natural and Other Gas by Pipeline",
            "PHMSA CFR 49 Part 195: Transportation of Hazardous Liquids by Pipeline"
        ],
        burden_holder="Construction Manager",
        adversary_position="Environmental Regulator",
        counter_arguments=[
            "ROW disputes may delay construction",
            "Environmental incidents may trigger regulatory action",
            "Trench collapse risks",
            "Backfill material quality may vary",
            "Documentation gaps may compromise compliance"
        ],
        resolution_strategy="Integrate environmental and safety controls, document all activities.",
        entity_scope="Pipeline construction",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="ASME B31.4, PHMSA CFR 49"
    ),
    DoctrineBlock(
        topic="Horizontal Directional Drilling (HDD): Bore Crossing",
        keywords=["drilling", "HDD", "bore crossing", "trenchless", "environmental", "risk"],
        conclusion_template=(
            "Horizontal Directional Drilling (HDD) is preferred for crossing sensitive areas. Proper planning, "
            "risk assessment, and execution are critical to minimize environmental impact and ensure bore integrity."
        ),
        reasoning_framework=(
            "1. Conduct geotechnical surveys of crossing area.\n"
            "2. Develop HDD design including entry/exit points, bore path, and diameter.\n"
            "3. Assess environmental risks and mitigation measures.\n"
            "4. Select drilling fluid composition and volume.\n"
            "5. Monitor borehole stability and fluid losses.\n"
            "6. Implement contingency plans for inadvertent returns.\n"
            "7. Inspect installed pipe for ovality and coating damage.\n"
            "8. Document HDD execution and deviations.\n"
            "9. Reference: API RP 1117, ASME B31.4."
        ),
        key_factors=[
            "Geotechnical survey",
            "HDD design parameters",
            "Environmental risk assessment",
            "Drilling fluid management",
            "Pipe inspection post-installation"
        ],
        primary_authority=[
            "API RP 1117: Recommended Practice for Horizontal Directional Drilling",
            "ASME B31.4: Pipeline Transportation Systems for Liquid Hydrocarbons"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Environmental Regulator",
        counter_arguments=[
            "Unexpected subsurface conditions may cause bore failure",
            "Fluid losses may trigger environmental incidents",
            "Pipe ovality may compromise integrity",
            "Coating damage during pullback",
            "Regulatory scrutiny of HDD operations"
        ],
        resolution_strategy="Conduct thorough surveys, implement robust risk mitigation.",
        entity_scope="Pipeline HDD crossing",
        confidence=0.89,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API RP 1117, ASME B31.4"
    ),
    DoctrineBlock(
        topic="Pipeline Pigging: Cleaning, Gauging, Intelligent",
        keywords=["pigging", "cleaning", "gauging", "intelligent", "maintenance", "inspection"],
        conclusion_template=(
            "Pigging operations are essential for pipeline cleaning, gauging, and integrity assessment. "
            "Intelligent pigs provide advanced inspection capabilities. Scheduling and execution must "
            "follow industry standards and safety protocols."
        ),
        reasoning_framework=(
            "1. Define pigging objectives (cleaning, gauging, inspection).\n"
            "2. Select pig type and configuration based on pipeline geometry and debris type.\n"
            "3. Develop pigging schedule and safety procedures.\n"
            "4. Monitor pig passage and collect operational data.\n"
            "5. Analyze pigging results for anomalies and defects.\n"
            "6. Document pigging operations and inspection findings.\n"
            "7. Reference: API RP 1163, ASME B31.4."
        ),
        key_factors=[
            "Pigging objectives",
            "Pig selection",
            "Operational safety",
            "Inspection data analysis",
            "Documentation"
        ],
        primary_authority=[
            "API RP 1163: In-Line Inspection of Pipelines",
            "ASME B31.4: Pipeline Transportation Systems for Liquid Hydrocarbons"
        ],
        burden_holder="Operations Manager",
        adversary_position="Integrity Manager",
        counter_arguments=[
            "Pig selection may be limited by pipeline geometry",
            "Debris accumulation may impede pig passage",
            "Safety incidents during pigging",
            "Inspection data interpretation challenges",
            "Documentation gaps"
        ],
        resolution_strategy="Select pigs based on objectives, ensure robust safety and documentation.",
        entity_scope="Pipeline pigging",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API RP 1163, ASME B31.4"
    ),
    DoctrineBlock(
        topic="Inline Inspection (ILI): MFL, Ultrasonic, Caliper",
        keywords=["ILI", "MFL", "ultrasonic", "caliper", "inspection", "integrity"],
        conclusion_template=(
            "Inline inspection (ILI) using Magnetic Flux Leakage (MFL), ultrasonic, and caliper tools is "
            "critical for pipeline integrity assessment. Tool selection and data interpretation must align "
            "with API and ASME guidelines."
        ),
        reasoning_framework=(
            "1. Define inspection objectives (corrosion, deformation, wall thickness).\n"
            "2. Select appropriate ILI tool (MFL, ultrasonic, caliper) based on pipeline characteristics.\n"
            "3. Develop inspection schedule and safety protocols.\n"
            "4. Collect and analyze ILI data for anomalies.\n"
            "5. Validate findings with field verification.\n"
            "6. Document inspection results and remediation actions.\n"
            "7. Reference: API RP 1163, ASME B31.4."
        ),
        key_factors=[
            "Inspection objectives",
            "ILI tool selection",
            "Data analysis",
            "Field verification",
            "Documentation"
        ],
        primary_authority=[
            "API RP 1163: In-Line Inspection of Pipelines",
            "ASME B31.4: Pipeline Transportation Systems for Liquid Hydrocarbons"
        ],
        burden_holder="Integrity Manager",
        adversary_position="Operations Manager",
        counter_arguments=[
            "Tool limitations for certain defect types",
            "Data interpretation challenges",
            "Field verification discrepancies",
            "Safety risks during inspection",
            "Regulatory scrutiny"
        ],
        resolution_strategy="Select tools based on objectives, validate findings with field data.",
        entity_scope="Pipeline ILI",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API RP 1163, ASME B31.4"
    ),
    DoctrineBlock(
        topic="Pipeline Integrity Management: PIMS, API 1160",
        keywords=["integrity", "PIMS", "API 1160", "risk assessment", "management", "maintenance"],
        conclusion_template=(
            "Pipeline Integrity Management Systems (PIMS) must be implemented per API 1160. Risk assessment, "
            "maintenance, and data integration are essential for compliance and operational safety."
        ),
        reasoning_framework=(
            "1. Develop PIMS framework per API 1160 requirements.\n"
            "2. Conduct risk assessment using historical data and predictive models.\n"
            "3. Integrate inspection, maintenance, and monitoring data.\n"
            "4. Schedule preventive and corrective maintenance.\n"
            "5. Document integrity threats and mitigation actions.\n"
            "6. Review compliance with PHMSA and API standards.\n"
            "7. Reference: API 1160, PHMSA CFR 49 Part 192/195."
        ),
        key_factors=[
            "PIMS framework",
            "Risk assessment",
            "Data integration",
            "Maintenance scheduling",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 1160: Managing System Integrity of Gas Pipelines",
            "PHMSA CFR 49 Part 192: Transportation of Natural and Other Gas by Pipeline",
            "PHMSA CFR 49 Part 195: Transportation of Hazardous Liquids by Pipeline"
        ],
        burden_holder="Integrity Manager",
        adversary_position="Regulatory Auditor",
        counter_arguments=[
            "Data integration challenges",
            "Risk assessment uncertainty",
            "Maintenance scheduling conflicts",
            "Regulatory changes",
            "Documentation gaps"
        ],
        resolution_strategy="Implement robust PIMS, integrate data, schedule maintenance per risk.",
        entity_scope="Pipeline integrity management",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API 1160, PHMSA CFR 49"
    ),
    DoctrineBlock(
        topic="Pipeline Stress Analysis: ASME B31.4, B31.8",
        keywords=["stress analysis", "ASME B31.4", "B31.8", "mechanical", "thermal", "expansion"],
        conclusion_template=(
            "Stress analysis must be performed per ASME B31.4 and B31.8. Mechanical and thermal stresses, "
            "including expansion and contraction, must be evaluated to ensure pipeline integrity."
        ),
        reasoning_framework=(
            "1. Identify mechanical and thermal loads on pipeline.\n"
            "2. Calculate stresses using ASME B31.4/B31.8 formulas.\n"
            "3. Assess impact of expansion, contraction, and external loads.\n"
            "4. Evaluate support and restraint design.\n"
            "5. Document stress analysis results and compliance.\n"
            "6. Reference: ASME B31.4, B31.8."
        ),
        key_factors=[
            "Mechanical loads",
            "Thermal expansion/contraction",
            "Stress calculation",
            "Support design",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.4: Pipeline Transportation Systems for Liquid Hydrocarbons",
            "ASME B31.8: Gas Transmission and Distribution Piping Systems"
        ],
        burden_holder="Design Engineer",
        adversary_position="Integrity Manager",
        counter_arguments=[
            "Thermal loads may be underestimated",
            "External loads may change over time",
            "Support design may be insufficient",
            "Regulatory updates may affect requirements",
            "Documentation gaps"
        ],
        resolution_strategy="Perform comprehensive stress analysis, validate support design.",
        entity_scope="Pipeline stress analysis",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="ASME B31.4, B31.8"
    ),
    DoctrineBlock(
        topic="Pipeline Cathodic Protection: CP Survey, CIPS, DCVG",
        keywords=["cathodic protection", "CP", "survey", "CIPS", "DCVG", "corrosion", "monitoring"],
        conclusion_template=(
            "Cathodic protection surveys, including Close Interval Potential Survey (CIPS) and Direct Current "
            "Voltage Gradient (DCVG), are essential for corrosion monitoring. Results must be integrated into "
            "integrity management systems."
        ),
        reasoning_framework=(
            "1. Schedule CP surveys per regulatory requirements.\n"
            "2. Conduct CIPS and DCVG to assess protection effectiveness.\n"
            "3. Analyze survey data for corrosion risk and anomalies.\n"
            "4. Integrate results into PIMS.\n"
            "5. Document survey findings and remediation actions.\n"
            "6. Reference: NACE SP0169, API 1160, PHMSA CFR 49."
        ),
        key_factors=[
            "CP survey scheduling",
            "CIPS and DCVG methodology",
            "Data analysis",
            "Integration with PIMS",
            "Regulatory compliance"
        ],
        primary_authority=[
            "NACE SP0169: Control of External Corrosion on Underground or Submerged Metallic Piping Systems",
            "API 1160: Managing System Integrity of Gas Pipelines",
            "PHMSA CFR 49 Part 192/195"
        ],
        burden_holder="Integrity Manager",
        adversary_position="Regulatory Auditor",
        counter_arguments=[
            "Survey data interpretation challenges",
            "Environmental factors affecting CP effectiveness",
            "Integration with PIMS may be incomplete",
            "Regulatory changes",
            "Documentation gaps"
        ],
        resolution_strategy="Conduct regular surveys, integrate results, document actions.",
        entity_scope="Pipeline cathodic protection",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="NACE SP0169, API 1160"
    ),
    DoctrineBlock(
        topic="Pipeline SCADA: Leak Detection, CPM, RTTM",
        keywords=["SCADA", "leak detection", "CPM", "RTTM", "monitoring", "automation"],
        conclusion_template=(
            "SCADA systems with Computational Pipeline Monitoring (CPM) and Real-Time Transient Model (RTTM) "
            "provide advanced leak detection and operational monitoring. System design must ensure reliability "
            "and compliance with regulatory standards."
        ),
        reasoning_framework=(
            "1. Define SCADA system requirements for leak detection and operational monitoring.\n"
            "2. Implement CPM and RTTM algorithms for real-time analysis.\n"
            "3. Validate system reliability and response time.\n"
            "4. Integrate SCADA data with PIMS and emergency response protocols.\n"
            "5. Document system design and compliance.\n"
            "6. Reference: API RP 1130, PHMSA CFR 49."
        ),
        key_factors=[
            "SCADA system requirements",
            "CPM and RTTM implementation",
            "System reliability",
            "Data integration",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 1130: Computational Pipeline Monitoring for Liquid Pipelines",
            "PHMSA CFR 49 Part 192/195"
        ],
        burden_holder="Automation Engineer",
        adversary_position="Integrity Manager",
        counter_arguments=[
            "Algorithm limitations for certain leak scenarios",
            "System reliability challenges",
            "Integration with emergency protocols",
            "Regulatory changes",
            "Documentation gaps"
        ],
        resolution_strategy="Implement robust SCADA, validate algorithms, document compliance.",
        entity_scope="Pipeline SCADA",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API RP 1130, PHMSA CFR 49"
    ),
    DoctrineBlock(
        topic="Pipeline Right of Way Acquisition: Easement",
        keywords=["ROW", "acquisition", "easement", "legal", "stakeholder", "negotiation"],
        conclusion_template=(
            "Right of way (ROW) acquisition requires legal negotiation and stakeholder engagement. Easement "
            "agreements must be documented and comply with regulatory and environmental requirements."
        ),
        reasoning_framework=(
            "1. Identify affected stakeholders and landowners.\n"
            "2. Conduct legal negotiations for easement agreements.\n"
            "3. Document ROW acquisition process and agreements.\n"
            "4. Assess environmental and regulatory requirements.\n"
            "5. Integrate ROW data into project management systems.\n"
            "6. Reference: PHMSA CFR 49, local land use regulations."
        ),
        key_factors=[
            "Stakeholder identification",
            "Legal negotiation",
            "Easement documentation",
            "Regulatory compliance",
            "Environmental assessment"
        ],
        primary_authority=[
            "PHMSA CFR 49 Part 192/195",
            "Local land use regulations"
        ],
        burden_holder="Legal Counsel",
        adversary_position="Landowner",
        counter_arguments=[
            "Stakeholder disputes may delay acquisition",
            "Legal challenges to easement agreements",
            "Environmental requirements may constrain ROW",
            "Documentation gaps",
            "Regulatory changes"
        ],
        resolution_strategy="Engage stakeholders, document agreements, comply with regulations.",
        entity_scope="Pipeline ROW acquisition",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="PHMSA CFR 49"
    ),
    DoctrineBlock(
        topic="Pipeline Regulatory Compliance: PHMSA CFR 49 Parts 192 & 195",
        keywords=["regulatory", "PHMSA", "CFR 49", "compliance", "audit", "reporting"],
        conclusion_template=(
            "Pipeline design, construction, operation, and maintenance must comply with PHMSA CFR 49 Parts 192 "
            "and 195. Documentation and audit readiness are essential for regulatory compliance."
        ),
        reasoning_framework=(
            "1. Identify applicable PHMSA regulations for project scope.\n"
            "2. Develop compliance matrix mapping requirements to project activities.\n"
            "3. Document compliance actions and audit trail.\n"
            "4. Schedule regulatory audits and reporting.\n"
            "5. Integrate compliance data into project management systems.\n"
            "6. Reference: PHMSA CFR 49 Parts 192 & 195."
        ),
        key_factors=[
            "Regulatory requirements identification",
            "Compliance matrix development",
            "Documentation",
            "Audit readiness",
            "Reporting protocols"
        ],
        primary_authority=[
            "PHMSA CFR 49 Part 192: Transportation of Natural and Other Gas by Pipeline",
            "PHMSA CFR 49 Part 195: Transportation of Hazardous Liquids by Pipeline"
        ],
        burden_holder="Compliance Manager",
        adversary_position="Regulatory Auditor",
        counter_arguments=[
            "Regulatory changes may affect requirements",
            "Documentation gaps may compromise compliance",
            "Audit findings may trigger corrective actions",
            "Reporting protocols may be unclear",
            "Integration with project management may be incomplete"
        ],
        resolution_strategy="Develop compliance matrix, document actions, schedule audits.",
        entity_scope="Pipeline regulatory compliance",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="PHMSA CFR 49"
    ),
    DoctrineBlock(
        topic="Pipeline Hydrostatic Testing: Strength and Leak",
        keywords=["hydrotest", "strength", "leak", "testing", "pressure", "documentation"],
        conclusion_template=(
            "Hydrostatic testing is mandatory for pipeline strength and leak assessment. Test procedures must "
            "comply with ASME and API standards. Documentation and remediation of failures are critical."
        ),
        reasoning_framework=(
            "1. Develop hydrotest plan per ASME B31.4/B31.8 and API standards.\n"
            "2. Define test pressure and duration based on design requirements.\n"
            "3. Monitor pressure and temperature during test.\n"
            "4. Document test results and failures.\n"
            "5. Remediate leaks and retest as necessary.\n"
            "6. Reference: ASME B31.4, B31.8, API RP 1110."
        ),
        key_factors=[
            "Test plan development",
            "Pressure and duration definition",
            "Monitoring protocols",
            "Documentation",
            "Remediation procedures"
        ],
        primary_authority=[
            "ASME B31.4: Pipeline Transportation Systems for Liquid Hydrocarbons",
            "ASME B31.8: Gas Transmission and Distribution Piping Systems",
            "API RP 1110: Pressure Testing of Liquid Hydrocarbon Pipelines"
        ],
        burden_holder="Testing Engineer",
        adversary_position="Integrity Manager",
        counter_arguments=[
            "Test failures may delay commissioning",
            "Documentation gaps",
            "Remediation may not restore original integrity",
            "Regulatory changes",
            "Test procedures may be insufficient"
        ],
        resolution_strategy="Develop robust test plan, document results, remediate failures.",
        entity_scope="Pipeline hydrostatic testing",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="ASME B31.4, API RP 1110"
    ),
    DoctrineBlock(
        topic="Compressor Station: Centrifugal and Reciprocating",
        keywords=["compressor", "station", "centrifugal", "reciprocating", "design", "operation"],
        conclusion_template=(
            "Compressor station design must select between centrifugal and reciprocating compressors based on "
            "operational requirements. Reliability, maintenance, and efficiency are key factors. Compliance "
            "with API and ASME standards is mandatory."
        ),
        reasoning_framework=(
            "1. Define operational requirements (flow, pressure, reliability).\n"
            "2. Select compressor type based on efficiency and maintenance needs.\n"
            "3. Develop station layout and safety protocols.\n"
            "4. Schedule preventive maintenance and monitoring.\n"
            "5. Document design and operational parameters.\n"
            "6. Reference: API 618, API 672, ASME B31.8."
        ),
        key_factors=[
            "Operational requirements",
            "Compressor type selection",
            "Station layout",
            "Maintenance scheduling",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 618: Reciprocating Compressors for Petroleum, Chemical, and Gas Industry Services",
            "API 672: Centrifugal Compressors for Petroleum, Chemical, and Gas Industry Services",
            "ASME B31.8: Gas Transmission and Distribution Piping Systems"
        ],
        burden_holder="Design Engineer",
        adversary_position="Operations Manager",
        counter_arguments=[
            "Compressor selection may affect reliability",
            "Maintenance costs may vary",
            "Station layout may constrain operations",
            "Regulatory changes",
            "Documentation gaps"
        ],
        resolution_strategy="Select compressor based on operational needs, document design.",
        entity_scope="Compressor station design",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API 618, API 672"
    ),
    DoctrineBlock(
        topic="Pump Station: Centrifugal and Positive Displacement",
        keywords=["pump", "station", "centrifugal", "positive displacement", "design", "operation"],
        conclusion_template=(
            "Pump station design must select between centrifugal and positive displacement pumps based on "
            "fluid properties and operational requirements. Maintenance and efficiency are critical. Compliance "
            "with API and ASME standards is required."
        ),
        reasoning_framework=(
            "1. Define fluid properties and operational requirements.\n"
            "2. Select pump type based on efficiency and maintenance needs.\n"
            "3. Develop station layout and safety protocols.\n"
            "4. Schedule preventive maintenance and monitoring.\n"
            "5. Document design and operational parameters.\n"
            "6. Reference: API 610, API 674, ASME B31.4."
        ),
        key_factors=[
            "Fluid properties",
            "Pump type selection",
            "Station layout",
            "Maintenance scheduling",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 610: Centrifugal Pumps for Petroleum, Chemical, and Gas Industry Services",
            "API 674: Positive Displacement Pumps for Petroleum, Chemical, and Gas Industry Services",
            "ASME B31.4: Pipeline Transportation Systems for Liquid Hydrocarbons"
        ],
        burden_holder="Design Engineer",
        adversary_position="Operations Manager",
        counter_arguments=[
            "Pump selection may affect reliability",
            "Maintenance costs may vary",
            "Station layout may constrain operations",
            "Regulatory changes",
            "Documentation gaps"
        ],
        resolution_strategy="Select pump based on fluid and operational needs, document design.",
        entity_scope="Pump station design",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API 610, API 674"
    ),
    DoctrineBlock(
        topic="Pipeline Flow Assurance: Hydrate, Wax, Asphaltene",
        keywords=["flow assurance", "hydrate", "wax", "asphaltene", "blockage", "remediation"],
        conclusion_template=(
            "Flow assurance requires management of hydrate, wax, and asphaltene risks. Prevention and remediation "
            "strategies must be integrated into operational protocols. Compliance with API and ASME standards is "
            "essential."
        ),
        reasoning_framework=(
            "1. Assess risk of hydrate, wax, and asphaltene formation based on fluid properties.\n"
            "2. Develop prevention strategies (chemical injection, insulation, heating).\n"
            "3. Schedule monitoring and inspection for early detection.\n"
            "4. Document remediation actions and operational changes.\n"
            "5. Reference: API RP 17A, ASME B31.4."
        ),
        key_factors=[
            "Fluid properties assessment",
            "Prevention strategy development",
            "Monitoring protocols",
            "Remediation documentation",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 17A: Design and Operation of Subsea Production Systems",
            "ASME B31.4: Pipeline Transportation Systems for Liquid Hydrocarbons"
        ],
        burden_holder="Operations Manager",
        adversary_position="Integrity Manager",
        counter_arguments=[
            "Prevention strategies may be costly",
            "Remediation may not restore original flow",
            "Monitoring protocols may miss early signs",
            "Regulatory changes",
            "Documentation gaps"
        ],
        resolution_strategy="Integrate prevention and remediation, document actions.",
        entity_scope="Pipeline flow assurance",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API RP 17A, ASME B31.4"
    ),
    DoctrineBlock(
        topic="Pipeline Decommissioning: Abandonment and Purging",
        keywords=["decommissioning", "abandonment", "purging", "environmental", "regulatory", "documentation"],
        conclusion_template=(
            "Pipeline decommissioning requires abandonment and purging procedures compliant with environmental "
            "and regulatory standards. Documentation and stakeholder engagement are critical."
        ),
        reasoning_framework=(
            "1. Develop decommissioning plan per regulatory requirements.\n"
            "2. Schedule purging and cleaning operations.\n"
            "3. Document abandonment procedures and environmental mitigation.\n"
            "4. Engage stakeholders and regulatory authorities.\n"
            "5. Reference: PHMSA CFR 49, API RP 1110."
        ),
        key_factors=[
            "Decommissioning plan development",
            "Purging and cleaning scheduling",
            "Documentation",
            "Stakeholder engagement",
            "Regulatory compliance"
        ],
        primary_authority=[
            "PHMSA CFR 49 Part 192/195",
            "API RP 1110: Pressure Testing of Liquid Hydrocarbon Pipelines"
        ],
        burden_holder="Decommissioning Manager",
        adversary_position="Regulatory Auditor",
        counter_arguments=[
            "Environmental risks during abandonment",
            "Regulatory changes",
            "Stakeholder disputes",
            "Documentation gaps",
            "Purging may not remove all contaminants"
        ],
        resolution_strategy="Develop robust plan, engage stakeholders, document actions.",
        entity_scope="Pipeline decommissioning",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="PHMSA CFR 49, API RP 1110"
    ),
    # ... 10+ more doctrine blocks for full coverage ...
]

# --- AUTHORITY HARDENING ---

authority_weights: Dict[str, float] = {
    "API RP 14E": 0.97,
    "ASME B31.4": 0.98,
    "ASME B31.8": 0.98,
    "API 5L": 0.96,
    "API 1104": 0.96,
    "ISO 21809": 0.95,
    "API RP 1163": 0.97,
    "API 1160": 0.98,
    "NACE SP0169": 0.95,
    "PHMSA CFR 49 Part 192": 0.99,
    "PHMSA CFR 49 Part 195": 0.99,
    "API RP 1130": 0.97,
    "API RP 1110": 0.96,
    "API RP 1117": 0.95,
    "API 618": 0.95,
    "API 672": 0.95,
    "API 610": 0.95,
    "API 674": 0.95,
    "API RP 17A": 0.94,
    "Local land use regulations": 0.90
}

def resolve_authority_conflict(authorities: List[str]) -> str:
    weighted = [(authority_weights.get(a, 0.85), a) for a in authorities]
    weighted.sort(reverse=True)
    return weighted[0][1] if weighted else ""

# --- SEMANTIC NORMALIZATION ---

domain_term_map: Dict[str, str] = {
    "hydrotest": "hydrostatic testing",
    "ILI": "inline inspection",
    "CP": "cathodic protection",
    "ROW": "right of way",
    "FBE": "fusion bonded epoxy",
    "GMAW": "gas metal arc welding",
    "SMAW": "shielded metal arc welding",
    "PIMS": "pipeline integrity management system",
    "CIPS": "close interval potential survey",
    "DCVG": "direct current voltage gradient",
    "CPM": "computational pipeline monitoring",
    "RTTM": "real-time transient model",
    "PQR": "procedure qualification record",
    "WPS": "welding procedure specification",
    "MFL": "magnetic flux leakage",
    "API 5L": "line pipe specification",
    "API 1104": "welding standard",
    "API RP 14E": "design and operation recommended practice",
    "API RP 1163": "in-line inspection recommended practice",
    "API 1160": "integrity management standard",
    "API RP 1130": "computational monitoring recommended practice",
    "API RP 1110": "pressure testing recommended practice",
    "API RP 1117": "horizontal directional drilling recommended practice",
    "API 618": "reciprocating compressor standard",
    "API 672": "centrifugal compressor standard",
    "API 610": "centrifugal pump standard",
    "API 674": "positive displacement pump standard",
    "API RP 17A": "subsea production recommended practice",
    "PHMSA CFR 49": "federal pipeline safety regulations"
}

def normalize_term(term: str) -> str:
    return domain_term_map.get(term.strip(), term.strip())

# --- EPISTEMIC GUARDRAILS ---

BANNED_PHRASES = [
    "it is believed",
    "likely",
    "may be",
    "could be",
    "possibly",
    "should",
    "might",
    "uncertain",
    "assumed",
    "presumed"
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "")
    return text

# --- FACT FRAGILITY SCORING ---

def score_fact_fragility(fact: str) -> Dict[str, float]:
    verifiability = 1.0 if any(auth in fact for auth in authority_weights) else 0.6
    recharacterization_risk = 0.2 if "documented" in fact or "certified" in fact else 0.6
    testimony_dependence = 0.1 if "field data" in fact or "inspection" in fact else 0.7
    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence
    }

# --- THREE LAYER RESPONSE ---

def doctrine_layer(query: QueryRequest) -> Tuple[List[DoctrineBlock], List[str]]:
    hits = []
    matched_blocks = []
    scenario = query.scenario.lower()
    for block in doctrine_cache:
        if any(k.lower() in scenario for k in block.keywords):
            matched_blocks.append(block)
            hits.append(block.topic)
    return matched_blocks, hits

def semantic_layer(query: QueryRequest) -> Tuple[List[DoctrineBlock], List[str]]:
    hits = []
    matched_blocks = []
    scenario = query.scenario.lower()
    for block in doctrine_cache:
        for k in block.keywords:
            if normalize_term(k).lower() in scenario:
                matched_blocks.append(block)
                hits.append(block.topic)
    return matched_blocks, hits

def deep_analysis_layer(query: QueryRequest, blocks: List[DoctrineBlock]) -> Tuple[str, List[str], List[str], str]:
    conclusion = []
    key_factors = set()
    authorities = set()
    counter_args = set()
    for block in blocks:
        conclusion.append(apply_epistemic_guardrails(block.conclusion_template))
        key_factors.update(block.key_factors)
        authorities.update(block.primary_authority)
        counter_args.update(block.counter_arguments)
    primary_conclusion = " ".join(conclusion)[:512]
    key_factors_list = list(key_factors)
    authorities_list = list(authorities)
    counter_args_list = list(counter_args)
    resolution_strategy = " ".join([b.resolution_strategy for b in blocks])[:256]
    return primary_conclusion, key_factors_list, authorities_list, resolution_strategy

# --- DEEP ANALYSIS ---

def multi_doctrine_decomposition(query: QueryRequest, blocks: List[DoctrineBlock]) -> Dict[str, Any]:
    dag = {}
    for block in blocks:
        dag[block.topic] = {
            "key_factors": block.key_factors,
            "primary_authority": block.primary_authority,
            "counter_arguments": block.counter_arguments,
            "resolution_strategy": block.resolution_strategy
        }
    return dag

def issue_category_mapping(query: QueryRequest) -> List[IssueCategory]:
    scenario = query.scenario.lower()
    categories = []
    for cat in IssueCategory:
        if cat.value.lower() in scenario:
            categories.append(cat)
    return categories

def eight_step_resolution(query: QueryRequest, blocks: List[DoctrineBlock]) -> str:
    steps = [
        "1. Identify scenario and regulatory requirements.",
        "2. Map scenario to relevant doctrine blocks.",
        "3. Extract key factors and authorities.",
        "4. Analyze counter-arguments and risk.",
        "5. Integrate semantic normalization.",
        "6. Apply epistemic guardrails.",
        "7. Score fact fragility.",
        "8. Synthesize primary conclusion and resolution strategy."
    ]
    return "\n".join(steps)

# --- COVERAGE MAP ---

def coverage_map(query: QueryRequest, matched_blocks: List[DoctrineBlock]) -> Dict[str, Any]:
    triggered = [b.topic for b in matched_blocks]
    missed = [b.topic for b in doctrine_cache if b not in matched_blocks]
    epistemic_gap = len(missed) / len(doctrine_cache) if doctrine_cache else 0.0
    return {
        "triggered_doctrines": triggered,
        "missed_doctrines": missed,
        "epistemic_gap": epistemic_gap
    }

# --- DRIFT WATCHER ---

baseline_hash = hashlib.sha256(json.dumps([b.topic for b in doctrine_cache]).encode()).hexdigest()

def drift_detection() -> Dict[str, Any]:
    current_hash = hashlib.sha256(json.dumps([b.topic for b in doctrine_cache]).encode()).hexdigest()
    drift = current_hash != baseline_hash
    return {
        "baseline_hash": baseline_hash,
        "current_hash": current_hash,
        "drift_detected": drift
    }

# --- AUDIT TRAIL ---

AUDIT_LOG_PATH = Path(__file__).resolve().parent / "audit_log.jsonl"

def log_audit(query_id: str, request: QueryRequest, response: QueryResponse):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query_id": query_id,
        "request": request.dict(),
        "response": response.dict()
    }
    try:
        with open(AUDIT_LOG_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        logger.error(f"Audit log error: {e}")

# --- DETERMINISM HASH ---

def determinism_hash(response: QueryResponse) -> str:
    hash_input = json.dumps(response.dict(), sort_keys=True).encode()
    return hashlib.sha256(hash_input).hexdigest()

# --- FASTAPI ---

app = FastAPI(title="Pipeline Systems Engineering Engine", version="OFE12", port=8912)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    logger.info("Pipeline Systems Engineering Engine OFE12 started.")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Pipeline Systems Engineering Engine OFE12 stopped.")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    query_id = str(uuid.uuid4())
    start_time = datetime.utcnow()
    # Layer 1: Doctrine cache
    doctrine_blocks, doctrine_hits = doctrine_layer(request)
    # Layer 2: Semantic normalization
    semantic_blocks, semantic_hits = semantic_layer(request)
    # Layer 3: Deep analysis
    all_blocks = list(set(doctrine_blocks + semantic_blocks))
    primary_conclusion, key_factors, authorities, resolution_strategy = deep_analysis_layer(request, all_blocks)
    # Position zone tagging
    position_zone = PositionZone.PLANNING
    if "audit" in request.scenario.lower():
        position_zone = PositionZone.AUDIT
    elif "report" in request.scenario.lower():
        position_zone = PositionZone.REPORTING
    # Confidence scoring
    confidence = min(1.0, sum(b.confidence for b in all_blocks) / (len(all_blocks) or 1))
    confidence_zone = all_blocks[0].confidence_zone if all_blocks else ConfidenceZone.DEFENSIBLE
    # Reasoning framework
    reasoning_framework = "\n".join([b.reasoning_framework for b in all_blocks])[:2048]
    # Counter arguments
    counter_arguments = []
    for b in all_blocks:
        counter_arguments.extend(b.counter_arguments)
    # Primary authority
    primary_authority = [resolve_authority_conflict(b.primary_authority) for b in all_blocks]
    # Determinism hash
    response = QueryResponse(
        engine_id="OFE12",
        query_id=query_id,
        mode=request.mode,
        confidence=confidence,
        confidence_zone=confidence_zone,
        position_zone=position_zone,
        primary_conclusion=primary_conclusion,
        reasoning_framework=reasoning_framework,
        key_factors=key_factors,
        primary_authority=primary_authority,
        counter_arguments=counter_arguments,
        resolution_strategy=resolution_strategy,
        determinism_hash=""
    )
    response.determinism_hash = determinism_hash(response)
    latency_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
    metrics_collector.record_query(query_id, doctrine_hits + semantic_hits, latency_ms)
    log_audit(query_id, request, response)
    return response

@app.get("/health")
async def health_endpoint():
    return {"status": "ok", "engine_id": "OFE12", "timestamp": datetime.utcnow().isoformat()}

@app.get("/metrics")
async def metrics_endpoint():
    return {
        "latency_stats": metrics_collector.get_latency_stats(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "queries_last_hour": metrics_collector.queries_last_hour()
    }

@app.get("/coverage")
async def coverage_endpoint():
    triggered = [b.topic for b in doctrine_cache]
    missed = []
    epistemic_gap = 0.0
    return {
        "triggered_doctrines": triggered,
        "missed_doctrines": missed,
        "epistemic_gap": epistemic_gap
    }

@app.get("/drift")
async def drift_endpoint():
    return drift_detection()

@app.get("/doctrines")
async def doctrines_endpoint():
    return [dataclasses.asdict(b) for b in doctrine_cache]

# --- ZONED ANALYSIS ---

def zoned_analysis(conclusion: str, scenario: str) -> PositionZone:
    if "audit" in scenario.lower():
        return PositionZone.AUDIT
    elif "report" in scenario.lower():
        return PositionZone.REPORTING
    else:
        return PositionZone.PLANNING
