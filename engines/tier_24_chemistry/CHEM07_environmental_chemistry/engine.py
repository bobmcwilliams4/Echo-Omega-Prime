import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import json
import threading

# =========================
# ENUMS
# =========================

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
    WATER_CHEMISTRY = "WATER_CHEMISTRY"
    WATER_TREATMENT = "WATER_TREATMENT"
    WASTEWATER_TREATMENT = "WASTEWATER_TREATMENT"
    AIR_POLLUTION = "AIR_POLLUTION"
    ATMOSPHERIC_CHEMISTRY = "ATMOSPHERIC_CHEMISTRY"
    SOIL_CONTAMINATION = "SOIL_CONTAMINATION"
    GROUNDWATER_CONTAMINATION = "GROUNDWATER_CONTAMINATION"
    REMEDIATION_TECHNOLOGIES = "REMEDIATION_TECHNOLOGIES"
    SAMPLING_QAQC = "SAMPLING_QAQC"
    ENVIRONMENTAL_REGULATIONS = "ENVIRONMENTAL_REGULATIONS"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"
    ECOLOGICAL_RISK = "ECOLOGICAL_RISK"
    ENV_MONITORING = "ENV_MONITORING"
    PBT_ASSESSMENT = "PBT_ASSESSMENT"
    GREEN_CHEMISTRY = "GREEN_CHEMISTRY"
    LIFE_CYCLE_ASSESSMENT = "LIFE_CYCLE_ASSESSMENT"
    FATE_TRANSPORT = "FATE_TRANSPORT"
    ANALYTICAL_METHODS = "ANALYTICAL_METHODS"
    EIA = "EIA"
    CARBON_FOOTPRINT = "CARBON_FOOTPRINT"

# =========================
# METRICS COLLECTOR
# =========================

class MetricsCollector:
    def __init__(self):
        self.query_log: List[Dict[str, Any]] = []
        self.error_log: List[Dict[str, Any]] = []
        self.doctrine_hits: Dict[str, int] = {}
        self.lock = threading.Lock()

    def record_query(self, query_id: str, timestamp: datetime, doctrine_ids: List[str], latency: float):
        with self.lock:
            self.query_log.append({
                "query_id": query_id,
                "timestamp": timestamp,
                "doctrine_ids": doctrine_ids,
                "latency": latency
            })
            for did in doctrine_ids:
                self.doctrine_hits[did] = self.doctrine_hits.get(did, 0) + 1

    def record_error(self, query_id: str, error: str, timestamp: datetime):
        with self.lock:
            self.error_log.append({
                "query_id": query_id,
                "error": error,
                "timestamp": timestamp
            })

    def get_latency_stats(self) -> Dict[str, float]:
        with self.lock:
            latencies = [q["latency"] for q in self.query_log[-100:]]
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
            return sum(1 for q in self.query_log if q["timestamp"] > cutoff)

metrics_collector = MetricsCollector()

# =========================
# PYDANTIC MODELS
# =========================

class QueryRequest(BaseModel):
    scenario: str = Field(..., description="Environmental chemistry scenario or question")
    mode: ResponseMode = Field(..., description="Response mode")
    entity_type: str = Field(..., description="Entity type (facility, site, region, etc.)")
    complexity: int = Field(..., description="Scenario complexity (1-5)")

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
# DOCTRINE CACHE
# =========================

@dataclass
class DoctrineBlock:
    doctrine_id: str
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

doctrine_cache: Dict[str, DoctrineBlock] = {}

def _add_doctrine(block: DoctrineBlock):
    doctrine_cache[block.doctrine_id] = block

# =========================
# DOCTRINE BLOCKS (30+)
# =========================

_add_doctrine(DoctrineBlock(
    doctrine_id="DC01",
    topic="Water Chemistry: pH",
    keywords=["pH", "water chemistry", "acid-base", "buffer", "alkalinity"],
    conclusion_template="The pH of water is a critical parameter affecting chemical speciation, biological activity, and treatment efficacy. Regulatory standards require pH to be maintained within specific ranges for potable and effluent waters.",
    reasoning_framework=(
        "pH is a logarithmic measure of hydrogen ion concentration. In natural waters, pH is influenced by carbonate equilibrium, organic acids, and anthropogenic inputs. "
        "Low pH increases metal solubility and toxicity; high pH can promote ammonia formation and scaling. Buffering capacity (alkalinity) modulates pH changes. "
        "Treatment processes such as lime addition or acid dosing are employed to adjust pH. Regulatory limits (e.g., EPA NPDES: 6.0-9.0) are enforced to protect aquatic life and human health. "
        "Continuous monitoring is recommended due to diurnal and seasonal fluctuations. "
        "Laboratory analysis uses glass electrode potentiometry, with QA/QC protocols per EPA 150.1. "
        "Site-specific factors include source water composition, industrial discharge, and biological activity. "
        "Risk assessment considers pH-dependent contaminant mobility and corrosion potential. "
        "Confounding factors include temperature, ionic strength, and presence of interfering substances. "
        "Resolution involves integrating field and laboratory data, regulatory guidance, and treatment optimization."
    ),
    key_factors=[
        "Hydrogen ion concentration",
        "Buffering capacity (alkalinity)",
        "Regulatory pH limits",
        "Source water characteristics",
        "Treatment process efficacy"
    ],
    primary_authority=[
        "EPA 150.1 (pH by Electrometric Method)",
        "WHO Guidelines for Drinking-water Quality, 4th Ed.",
        "NPDES Permit Requirements"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge pH stability or compliance",
    counter_arguments=[
        "Natural variability in source water",
        "Measurement uncertainty",
        "Temporal fluctuations",
        "Interference from industrial discharge",
        "Buffering limitations"
    ],
    resolution_strategy="Integrate continuous monitoring, laboratory QA/QC, and regulatory guidance to ensure pH compliance.",
    entity_scope="Water treatment facilities, surface water, groundwater",
    confidence=0.98,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 150.1",
        "WHO Drinking-water Quality",
        "NPDES"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC02",
    topic="Water Chemistry: Alkalinity",
    keywords=["alkalinity", "buffer", "carbonate", "acid neutralizing", "water chemistry"],
    conclusion_template="Alkalinity represents the acid-neutralizing capacity of water, primarily due to bicarbonate, carbonate, and hydroxide ions. It is essential for buffering pH changes and is a key parameter in water treatment and aquatic ecosystem health.",
    reasoning_framework=(
        "Alkalinity is measured as mg/L CaCO3 and reflects the sum of bicarbonate, carbonate, and hydroxide ions. "
        "It stabilizes pH against acid inputs, protecting aquatic life and infrastructure. "
        "Low alkalinity increases vulnerability to acidification; high alkalinity can promote scaling and reduce treatment efficiency. "
        "Sources include geological substrate, atmospheric deposition, and anthropogenic inputs. "
        "Treatment may involve lime addition or acid dosing to adjust alkalinity. "
        "EPA and WHO recommend minimum alkalinity levels for potable water. "
        "Analytical methods include titration with strong acid (EPA 2310B). "
        "QA/QC involves calibration, blanks, and replicate samples. "
        "Risk assessment considers acid rain, industrial discharge, and biological activity. "
        "Resolution integrates field measurements, laboratory QA/QC, and regulatory standards."
    ),
    key_factors=[
        "Bicarbonate and carbonate concentration",
        "Buffering capacity",
        "Source water geology",
        "Treatment process",
        "Regulatory minimums"
    ],
    primary_authority=[
        "EPA 2310B (Alkalinity by Titration)",
        "WHO Drinking-water Quality",
        "Standard Methods for the Examination of Water and Wastewater"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge alkalinity adequacy or measurement accuracy",
    counter_arguments=[
        "Natural variability",
        "Measurement uncertainty",
        "Interference from organic acids",
        "Temporal changes",
        "Treatment limitations"
    ],
    resolution_strategy="Apply robust QA/QC, integrate field and laboratory data, and optimize treatment for regulatory compliance.",
    entity_scope="Water treatment, surface water, groundwater",
    confidence=0.97,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 2310B",
        "WHO Drinking-water Quality",
        "Standard Methods"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC03",
    topic="Water Chemistry: Hardness",
    keywords=["hardness", "calcium", "magnesium", "scale", "water chemistry"],
    conclusion_template="Water hardness is determined by the concentration of calcium and magnesium ions. It affects scaling, corrosion, and treatment processes, with regulatory guidance for potable water and industrial applications.",
    reasoning_framework=(
        "Hardness is measured as mg/L CaCO3 and primarily reflects calcium and magnesium concentrations. "
        "High hardness leads to scaling in pipes and boilers, reducing efficiency and increasing maintenance costs. "
        "Low hardness increases corrosion risk and may affect taste. "
        "Sources include geological substrate and industrial discharge. "
        "Treatment options include ion exchange, lime softening, and reverse osmosis. "
        "EPA and WHO provide guidance on acceptable hardness levels for drinking water. "
        "Analytical methods include titration with EDTA (EPA 130.2). "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers infrastructure, health, and operational impacts. "
        "Resolution integrates field and laboratory data, treatment optimization, and regulatory compliance."
    ),
    key_factors=[
        "Calcium and magnesium concentration",
        "Scaling potential",
        "Corrosion risk",
        "Treatment process",
        "Regulatory guidance"
    ],
    primary_authority=[
        "EPA 130.2 (Hardness by EDTA Titration)",
        "WHO Drinking-water Quality",
        "Standard Methods"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge hardness measurement or treatment efficacy",
    counter_arguments=[
        "Natural variability",
        "Measurement uncertainty",
        "Treatment limitations",
        "Infrastructure constraints",
        "Temporal fluctuations"
    ],
    resolution_strategy="Apply robust QA/QC, optimize treatment, and ensure regulatory compliance.",
    entity_scope="Water treatment, potable water, industrial water",
    confidence=0.96,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 130.2",
        "WHO Drinking-water Quality",
        "Standard Methods"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC04",
    topic="Water Chemistry: Dissolved Oxygen",
    keywords=["dissolved oxygen", "DO", "water chemistry", "BOD", "aquatic life"],
    conclusion_template="Dissolved oxygen (DO) is a critical parameter for aquatic life and water quality. Regulatory standards require minimum DO levels to prevent hypoxia and support ecosystem health.",
    reasoning_framework=(
        "DO is measured in mg/L and reflects the oxygen available for aquatic organisms. "
        "Low DO causes hypoxia, fish kills, and disrupts ecosystem function. "
        "Sources of DO include atmospheric diffusion, photosynthesis, and mechanical aeration. "
        "Consumption occurs via biological oxygen demand (BOD), chemical oxygen demand (COD), and respiration. "
        "EPA and state standards require minimum DO levels (e.g., >5 mg/L for aquatic life). "
        "Analytical methods include membrane electrode (EPA 360.1) and Winkler titration. "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers temperature, salinity, organic load, and stratification. "
        "Resolution integrates field monitoring, laboratory QA/QC, and regulatory guidance."
    ),
    key_factors=[
        "DO concentration",
        "BOD and COD",
        "Temperature and salinity",
        "Aeration and photosynthesis",
        "Regulatory minimums"
    ],
    primary_authority=[
        "EPA 360.1 (DO by Membrane Electrode)",
        "WHO Drinking-water Quality",
        "State Water Quality Standards"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge DO measurement or compliance",
    counter_arguments=[
        "Measurement uncertainty",
        "Temporal and spatial variability",
        "Interference from organic matter",
        "Equipment calibration",
        "Natural stratification"
    ],
    resolution_strategy="Apply robust QA/QC, integrate field and laboratory data, and optimize aeration for compliance.",
    entity_scope="Surface water, wastewater, aquatic ecosystems",
    confidence=0.95,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 360.1",
        "WHO Drinking-water Quality",
        "State Standards"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC05",
    topic="Water Treatment: Coagulation and Flocculation",
    keywords=["coagulation", "flocculation", "water treatment", "turbidity", "particles"],
    conclusion_template="Coagulation and flocculation are essential processes for removing suspended solids and reducing turbidity in water treatment. Proper chemical dosing and mixing are critical for process efficacy.",
    reasoning_framework=(
        "Coagulation involves destabilizing colloidal particles using coagulants (e.g., alum, ferric chloride). "
        "Flocculation promotes aggregation of destabilized particles into larger flocs via gentle mixing. "
        "Process efficacy depends on pH, alkalinity, coagulant dose, mixing intensity, and temperature. "
        "EPA and WHO provide guidance on coagulant selection and dosing. "
        "Analytical methods include jar testing and turbidity measurement (EPA 180.1). "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers source water variability, organic load, and operational constraints. "
        "Resolution integrates pilot testing, laboratory QA/QC, and regulatory guidance."
    ),
    key_factors=[
        "Coagulant type and dose",
        "Mixing intensity",
        "pH and alkalinity",
        "Turbidity reduction",
        "Regulatory guidance"
    ],
    primary_authority=[
        "EPA 180.1 (Turbidity by Nephelometry)",
        "WHO Drinking-water Quality",
        "Standard Methods"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge process efficacy or compliance",
    counter_arguments=[
        "Source water variability",
        "Measurement uncertainty",
        "Operational limitations",
        "Chemical availability",
        "Process optimization"
    ],
    resolution_strategy="Apply pilot testing, robust QA/QC, and optimize process for regulatory compliance.",
    entity_scope="Water treatment facilities",
    confidence=0.94,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 180.1",
        "WHO Drinking-water Quality",
        "Standard Methods"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC06",
    topic="Water Treatment: Sedimentation and Filtration",
    keywords=["sedimentation", "filtration", "water treatment", "turbidity", "particles"],
    conclusion_template="Sedimentation and filtration remove suspended solids and reduce turbidity in water treatment. Process design and operational control are critical for achieving regulatory standards.",
    reasoning_framework=(
        "Sedimentation relies on gravity to settle suspended particles after coagulation/flocculation. "
        "Filtration removes remaining particles via media (sand, anthracite, GAC). "
        "Process efficacy depends on hydraulic loading, particle size, media type, and operational control. "
        "EPA and WHO provide guidance on design and performance standards. "
        "Analytical methods include turbidity measurement (EPA 180.1) and particle counting. "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers source water variability, operational constraints, and maintenance. "
        "Resolution integrates pilot testing, laboratory QA/QC, and regulatory guidance."
    ),
    key_factors=[
        "Hydraulic loading rate",
        "Media type and depth",
        "Turbidity reduction",
        "Operational control",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 180.1 (Turbidity by Nephelometry)",
        "WHO Drinking-water Quality",
        "Standard Methods"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge process efficacy or compliance",
    counter_arguments=[
        "Source water variability",
        "Measurement uncertainty",
        "Operational limitations",
        "Media fouling",
        "Maintenance constraints"
    ],
    resolution_strategy="Apply pilot testing, robust QA/QC, and optimize process for regulatory compliance.",
    entity_scope="Water treatment facilities",
    confidence=0.93,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 180.1",
        "WHO Drinking-water Quality",
        "Standard Methods"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC07",
    topic="Water Treatment: Disinfection",
    keywords=["disinfection", "chlorine", "UV", "water treatment", "pathogens"],
    conclusion_template="Disinfection is essential for pathogen control in water treatment. Chlorine, UV, and ozone are commonly used, with regulatory standards for residuals and byproducts.",
    reasoning_framework=(
        "Disinfection inactivates pathogens using chemical (chlorine, chloramines, ozone) or physical (UV) methods. "
        "Process efficacy depends on dose, contact time, water quality, and pathogen type. "
        "EPA and WHO set standards for disinfectant residuals and byproducts (e.g., THMs, HAAs). "
        "Analytical methods include chlorine residual measurement (EPA 4500-Cl) and microbial assays. "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers pathogen risk, disinfection byproducts, and operational constraints. "
        "Resolution integrates field monitoring, laboratory QA/QC, and regulatory guidance."
    ),
    key_factors=[
        "Disinfectant type and dose",
        "Contact time",
        "Pathogen risk",
        "Byproduct formation",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 4500-Cl (Chlorine Residual)",
        "WHO Drinking-water Quality",
        "Standard Methods"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge disinfection efficacy or byproduct control",
    counter_arguments=[
        "Measurement uncertainty",
        "Operational limitations",
        "Pathogen variability",
        "Byproduct formation",
        "Treatment optimization"
    ],
    resolution_strategy="Apply robust QA/QC, optimize process, and ensure regulatory compliance.",
    entity_scope="Water treatment facilities",
    confidence=0.92,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 4500-Cl",
        "WHO Drinking-water Quality",
        "Standard Methods"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC08",
    topic="Wastewater Treatment: Activated Sludge",
    keywords=["activated sludge", "wastewater treatment", "BOD", "microbial", "aeration"],
    conclusion_template="Activated sludge is a biological process for removing organic matter and nutrients from wastewater. Process control and monitoring are critical for regulatory compliance.",
    reasoning_framework=(
        "Activated sludge uses aerobic microorganisms to degrade organic matter (BOD, COD) and nutrients (N, P). "
        "Process efficacy depends on aeration, sludge age, F/M ratio, and operational control. "
        "EPA and state standards set effluent limits for BOD, TSS, N, P. "
        "Analytical methods include BOD (EPA 405.1), TSS (EPA 160.2), and nutrient assays. "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers influent variability, operational constraints, and sludge management. "
        "Resolution integrates field monitoring, laboratory QA/QC, and regulatory guidance."
    ),
    key_factors=[
        "Aeration rate",
        "Sludge age",
        "F/M ratio",
        "Effluent quality",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 405.1 (BOD)",
        "EPA 160.2 (TSS)",
        "State Wastewater Standards"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge process efficacy or compliance",
    counter_arguments=[
        "Influent variability",
        "Measurement uncertainty",
        "Operational limitations",
        "Sludge management",
        "Process optimization"
    ],
    resolution_strategy="Apply robust QA/QC, optimize process, and ensure regulatory compliance.",
    entity_scope="Wastewater treatment plants",
    confidence=0.91,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 405.1",
        "EPA 160.2",
        "State Standards"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC09",
    topic="Wastewater Treatment: Trickling Filter",
    keywords=["trickling filter", "wastewater treatment", "BOD", "biofilm", "secondary treatment"],
    conclusion_template="Trickling filters use biofilms on media to degrade organic matter in wastewater. Process design and operational control are critical for achieving regulatory standards.",
    reasoning_framework=(
        "Trickling filters pass wastewater over media (rock, plastic) supporting biofilm growth. "
        "Microbial communities degrade organic matter (BOD, COD) and nutrients. "
        "Process efficacy depends on hydraulic loading, media type, temperature, and operational control. "
        "EPA and state standards set effluent limits for BOD, TSS, N, P. "
        "Analytical methods include BOD (EPA 405.1), TSS (EPA 160.2), and nutrient assays. "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers influent variability, media fouling, and operational constraints. "
        "Resolution integrates field monitoring, laboratory QA/QC, and regulatory guidance."
    ),
    key_factors=[
        "Hydraulic loading rate",
        "Media type",
        "Biofilm development",
        "Effluent quality",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 405.1 (BOD)",
        "EPA 160.2 (TSS)",
        "State Wastewater Standards"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge process efficacy or compliance",
    counter_arguments=[
        "Influent variability",
        "Measurement uncertainty",
        "Media fouling",
        "Operational limitations",
        "Process optimization"
    ],
    resolution_strategy="Apply robust QA/QC, optimize process, and ensure regulatory compliance.",
    entity_scope="Wastewater treatment plants",
    confidence=0.90,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 405.1",
        "EPA 160.2",
        "State Standards"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC10",
    topic="Wastewater Treatment: UASB Reactor",
    keywords=["UASB", "anaerobic", "wastewater treatment", "BOD", "biogas"],
    conclusion_template="Upflow Anaerobic Sludge Blanket (UASB) reactors treat wastewater using anaerobic digestion. Process control and monitoring are critical for biogas production and regulatory compliance.",
    reasoning_framework=(
        "UASB reactors use anaerobic microorganisms to degrade organic matter (BOD, COD) and produce biogas (CH4, CO2). "
        "Process efficacy depends on hydraulic loading, temperature, sludge retention, and operational control. "
        "EPA and state standards set effluent limits for BOD, TSS, N, P. "
        "Analytical methods include BOD (EPA 405.1), TSS (EPA 160.2), biogas measurement. "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers influent variability, operational constraints, and biogas management. "
        "Resolution integrates field monitoring, laboratory QA/QC, and regulatory guidance."
    ),
    key_factors=[
        "Hydraulic loading rate",
        "Sludge retention time",
        "Biogas production",
        "Effluent quality",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 405.1 (BOD)",
        "EPA 160.2 (TSS)",
        "State Wastewater Standards"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge process efficacy or biogas management",
    counter_arguments=[
        "Influent variability",
        "Measurement uncertainty",
        "Operational limitations",
        "Biogas management",
        "Process optimization"
    ],
    resolution_strategy="Apply robust QA/QC, optimize process, and ensure regulatory compliance.",
    entity_scope="Wastewater treatment plants",
    confidence=0.89,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 405.1",
        "EPA 160.2",
        "State Standards"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC11",
    topic="Wastewater Treatment: Membrane Bioreactor (MBR)",
    keywords=["MBR", "membrane bioreactor", "wastewater treatment", "BOD", "TSS"],
    conclusion_template="Membrane bioreactors (MBR) combine biological treatment and membrane filtration for high-quality effluent. Process control and membrane maintenance are critical for regulatory compliance.",
    reasoning_framework=(
        "MBRs integrate activated sludge with membrane filtration (microfiltration, ultrafiltration) to remove BOD, TSS, and pathogens. "
        "Process efficacy depends on membrane integrity, fouling control, aeration, and operational control. "
        "EPA and state standards set effluent limits for BOD, TSS, N, P. "
        "Analytical methods include BOD (EPA 405.1), TSS (EPA 160.2), and membrane integrity tests. "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers influent variability, membrane fouling, and operational constraints. "
        "Resolution integrates field monitoring, laboratory QA/QC, and regulatory guidance."
    ),
    key_factors=[
        "Membrane integrity",
        "Fouling control",
        "Aeration rate",
        "Effluent quality",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 405.1 (BOD)",
        "EPA 160.2 (TSS)",
        "State Wastewater Standards"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge membrane integrity or process efficacy",
    counter_arguments=[
        "Influent variability",
        "Measurement uncertainty",
        "Membrane fouling",
        "Operational limitations",
        "Process optimization"
    ],
    resolution_strategy="Apply robust QA/QC, optimize process, and ensure regulatory compliance.",
    entity_scope="Wastewater treatment plants",
    confidence=0.88,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 405.1",
        "EPA 160.2",
        "State Standards"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC12",
    topic="Air Pollution: SOx and NOx",
    keywords=["SOx", "NOx", "air pollution", "acid rain", "emissions"],
    conclusion_template="Sulfur oxides (SOx) and nitrogen oxides (NOx) are major air pollutants contributing to acid rain and respiratory health issues. Regulatory standards limit emissions from industrial and vehicular sources.",
    reasoning_framework=(
        "SOx and NOx are produced from combustion of fossil fuels and industrial processes. "
        "SOx (SO2, SO3) contribute to acid rain, particulate formation, and respiratory irritation. "
        "NOx (NO, NO2) contribute to ozone formation, smog, and respiratory health impacts. "
        "EPA and CAA set emission limits and require control technologies (scrubbers, catalytic reduction). "
        "Analytical methods include continuous emission monitoring (EPA 40 CFR Part 60) and ambient air sampling. "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers source strength, meteorology, and population exposure. "
        "Resolution integrates monitoring, control technology, and regulatory compliance."
    ),
    key_factors=[
        "Emission rates",
        "Control technology",
        "Ambient concentrations",
        "Meteorology",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 40 CFR Part 60",
        "Clean Air Act (CAA)",
        "WHO Air Quality Guidelines"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge emission control or compliance",
    counter_arguments=[
        "Measurement uncertainty",
        "Control technology limitations",
        "Meteorological variability",
        "Source variability",
        "Regulatory interpretation"
    ],
    resolution_strategy="Apply robust QA/QC, optimize control technology, and ensure regulatory compliance.",
    entity_scope="Industrial facilities, urban areas",
    confidence=0.97,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 40 CFR Part 60",
        "CAA",
        "WHO Air Quality"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC13",
    topic="Air Pollution: VOCs",
    keywords=["VOC", "volatile organic compounds", "air pollution", "ozone", "health"],
    conclusion_template="Volatile organic compounds (VOCs) are precursors to ozone and smog formation and pose health risks. Regulatory standards limit emissions and require monitoring and control.",
    reasoning_framework=(
        "VOCs are emitted from industrial processes, vehicles, and solvent use. "
        "They react with NOx under sunlight to form ozone and photochemical smog. "
        "Health impacts include respiratory irritation, carcinogenicity, and neurotoxicity. "
        "EPA and CAA set emission limits and require control technologies (carbon adsorption, thermal oxidation). "
        "Analytical methods include EPA TO-15 (GC/MS) and ambient air sampling. "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers source strength, meteorology, and population exposure. "
        "Resolution integrates monitoring, control technology, and regulatory compliance."
    ),
    key_factors=[
        "Emission rates",
        "Control technology",
        "Ambient concentrations",
        "Meteorology",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA TO-15 (VOCs by GC/MS)",
        "Clean Air Act (CAA)",
        "WHO Air Quality Guidelines"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge emission control or compliance",
    counter_arguments=[
        "Measurement uncertainty",
        "Control technology limitations",
        "Meteorological variability",
        "Source variability",
        "Regulatory interpretation"
    ],
    resolution_strategy="Apply robust QA/QC, optimize control technology, and ensure regulatory compliance.",
    entity_scope="Industrial facilities, urban areas",
    confidence=0.96,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA TO-15",
        "CAA",
        "WHO Air Quality"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC14",
    topic="Air Pollution: Particulate Matter",
    keywords=["particulate matter", "PM2.5", "PM10", "air pollution", "health"],
    conclusion_template="Particulate matter (PM2.5, PM10) is a major air pollutant affecting respiratory and cardiovascular health. Regulatory standards limit ambient concentrations and require control technologies.",
    reasoning_framework=(
        "PM2.5 and PM10 are emitted from combustion, industrial processes, and natural sources. "
        "Health impacts include respiratory disease, cardiovascular effects, and mortality. "
        "EPA and CAA set ambient air quality standards (NAAQS) and require control technologies (filters, cyclones, electrostatic precipitators). "
        "Analytical methods include EPA 40 CFR Part 50 (gravimetric) and continuous monitoring. "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers source strength, meteorology, and population exposure. "
        "Resolution integrates monitoring, control technology, and regulatory compliance."
    ),
    key_factors=[
        "Ambient concentrations",
        "Control technology",
        "Source strength",
        "Meteorology",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 40 CFR Part 50",
        "Clean Air Act (CAA)",
        "WHO Air Quality Guidelines"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge control technology or compliance",
    counter_arguments=[
        "Measurement uncertainty",
        "Control technology limitations",
        "Meteorological variability",
        "Source variability",
        "Regulatory interpretation"
    ],
    resolution_strategy="Apply robust QA/QC, optimize control technology, and ensure regulatory compliance.",
    entity_scope="Industrial facilities, urban areas",
    confidence=0.95,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 40 CFR Part 50",
        "CAA",
        "WHO Air Quality"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC15",
    topic="Air Pollution: Ozone",
    keywords=["ozone", "O3", "air pollution", "photochemical smog", "health"],
    conclusion_template="Ozone (O3) is a secondary air pollutant formed by VOC and NOx reactions under sunlight. Regulatory standards limit ambient concentrations to protect public health.",
    reasoning_framework=(
        "Ozone is formed by photochemical reactions between VOCs and NOx under sunlight. "
        "Health impacts include respiratory irritation, asthma exacerbation, and reduced lung function. "
        "EPA and CAA set ambient air quality standards (NAAQS) for ozone. "
        "Analytical methods include UV photometry (EPA 40 CFR Part 50) and continuous monitoring. "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers source strength, meteorology, and population exposure. "
        "Resolution integrates monitoring, emission control, and regulatory compliance."
    ),
    key_factors=[
        "Ambient concentrations",
        "Source strength",
        "Meteorology",
        "Emission control",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 40 CFR Part 50",
        "Clean Air Act (CAA)",
        "WHO Air Quality Guidelines"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge emission control or compliance",
    counter_arguments=[
        "Measurement uncertainty",
        "Meteorological variability",
        "Source variability",
        "Regulatory interpretation",
        "Emission control limitations"
    ],
    resolution_strategy="Apply robust QA/QC, optimize emission control, and ensure regulatory compliance.",
    entity_scope="Urban areas, industrial facilities",
    confidence=0.94,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 40 CFR Part 50",
        "CAA",
        "WHO Air Quality"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC16",
    topic="Atmospheric Chemistry: Photochemical Smog",
    keywords=["photochemical smog", "ozone", "VOCs", "NOx", "sunlight"],
    conclusion_template="Photochemical smog results from VOC and NOx reactions under sunlight, producing ozone and secondary pollutants. Regulatory strategies focus on emission reduction and air quality monitoring.",
    reasoning_framework=(
        "Photochemical smog forms when VOCs and NOx react under sunlight, producing ozone, PAN, and other secondary pollutants. "
        "Health impacts include respiratory irritation, asthma, and reduced visibility. "
        "EPA and CAA set emission limits and require air quality monitoring. "
        "Analytical methods include ambient air sampling, UV photometry, and GC/MS for VOCs. "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers source strength, meteorology, and population exposure. "
        "Resolution integrates emission reduction, monitoring, and regulatory compliance."
    ),
    key_factors=[
        "Emission rates",
        "Meteorology",
        "Ambient concentrations",
        "Air quality monitoring",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 40 CFR Part 50",
        "Clean Air Act (CAA)",
        "WHO Air Quality Guidelines"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge emission reduction or compliance",
    counter_arguments=[
        "Measurement uncertainty",
        "Meteorological variability",
        "Source variability",
        "Regulatory interpretation",
        "Emission reduction limitations"
    ],
    resolution_strategy="Apply robust QA/QC, optimize emission reduction, and ensure regulatory compliance.",
    entity_scope="Urban areas, industrial facilities",
    confidence=0.93,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 40 CFR Part 50",
        "CAA",
        "WHO Air Quality"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC17",
    topic="Atmospheric Chemistry: Acid Rain",
    keywords=["acid rain", "SOx", "NOx", "precipitation", "ecosystem"],
    conclusion_template="Acid rain results from atmospheric SOx and NOx reacting with water vapor, lowering precipitation pH and impacting ecosystems. Regulatory strategies focus on emission reduction and ecosystem monitoring.",
    reasoning_framework=(
        "Acid rain forms when SOx and NOx react with water vapor, producing sulfuric and nitric acids. "
        "Impacts include soil acidification, aquatic ecosystem damage, and infrastructure corrosion. "
        "EPA and CAA set emission limits and require ecosystem monitoring. "
        "Analytical methods include precipitation pH measurement, ion chromatography for sulfate and nitrate. "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers emission sources, meteorology, and ecosystem vulnerability. "
        "Resolution integrates emission reduction, monitoring, and regulatory compliance."
    ),
    key_factors=[
        "Emission rates",
        "Precipitation pH",
        "Ecosystem vulnerability",
        "Monitoring",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA Acid Rain Program",
        "Clean Air Act (CAA)",
        "WHO Air Quality Guidelines"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge emission reduction or ecosystem monitoring",
    counter_arguments=[
        "Measurement uncertainty",
        "Meteorological variability",
        "Source variability",
        "Regulatory interpretation",
        "Ecosystem complexity"
    ],
    resolution_strategy="Apply robust QA/QC, optimize emission reduction, and ensure regulatory compliance.",
    entity_scope="Industrial facilities, ecosystems",
    confidence=0.92,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA Acid Rain Program",
        "CAA",
        "WHO Air Quality"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC18",
    topic="Atmospheric Chemistry: Greenhouse Gases",
    keywords=["greenhouse gases", "CO2", "CH4", "N2O", "global warming"],
    conclusion_template="Greenhouse gases (CO2, CH4, N2O) contribute to global warming and climate change. Regulatory strategies focus on emission reduction, inventory, and reporting.",
    reasoning_framework=(
        "Greenhouse gases trap infrared radiation, raising global temperatures. "
        "Sources include fossil fuel combustion, agriculture, and industrial processes. "
        "EPA and international agreements (Kyoto Protocol, Paris Agreement) set emission reduction targets and reporting requirements. "
        "Analytical methods include continuous emission monitoring, gas chromatography, and inventory estimation. "
        "QA/QC involves calibration, blanks, and replicates. "
        "Risk assessment considers emission sources, climate impacts, and mitigation strategies. "
        "Resolution integrates emission reduction, inventory, and regulatory compliance."
    ),
    key_factors=[
        "Emission rates",
        "Inventory accuracy",
        "Mitigation strategies",
        "Reporting requirements",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA Greenhouse Gas Reporting Program",
        "Kyoto Protocol",
        "Paris Agreement"
    ],
    burden_holder="Facility operator",
    adversary_position="Regulator may challenge inventory accuracy or emission reduction",
    counter_arguments=[
        "Measurement uncertainty",
        "Inventory estimation limitations",
        "Source variability",
        "Regulatory interpretation",
        "Mitigation feasibility"
    ],
    resolution_strategy="Apply robust QA/QC, optimize inventory, and ensure regulatory compliance.",
    entity_scope="Industrial facilities, national inventories",
    confidence=0.91,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA GHG Reporting",
        "Kyoto Protocol",
        "Paris Agreement"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC19",
    topic="Soil Contamination: Heavy Metals",
    keywords=["heavy metals", "soil contamination", "lead", "cadmium", "arsenic"],
    conclusion_template="Heavy metal contamination in soil poses risks to human health and ecosystems. Regulatory standards set cleanup levels and require monitoring and remediation.",
    reasoning_framework=(
        "Heavy metals (Pb, Cd, As, Hg) accumulate in soil from industrial, agricultural, and urban sources. "
        "Health impacts include neurotoxicity, carcinogenicity, and ecosystem disruption. "
        "EPA and CERCLA set cleanup levels and require monitoring and remediation. "
        "Analytical methods include EPA 6010 (ICP-AES), EPA 6020 (ICP-MS), and soil sampling protocols. "
        "QA/QC involves calibration, blanks, replicates, and chain of custody. "
        "Risk assessment considers exposure pathways, bioavailability, and population vulnerability. "
        "Resolution integrates monitoring, remediation, and regulatory compliance."
    ),
    key_factors=[
        "Contaminant concentration",
        "Bioavailability",
        "Exposure pathways",
        "Cleanup levels",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 6010 (ICP-AES)",
        "EPA 6020 (ICP-MS)",
        "CERCLA"
    ],
    burden_holder="Site owner",
    adversary_position="Regulator may challenge cleanup adequacy or monitoring",
    counter_arguments=[
        "Measurement uncertainty",
        "Bioavailability variability",
        "Exposure pathway complexity",
        "Regulatory interpretation",
        "Remediation limitations"
    ],
    resolution_strategy="Apply robust QA/QC, optimize remediation, and ensure regulatory compliance.",
    entity_scope="Contaminated sites, industrial facilities",
    confidence=0.97,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 6010",
        "EPA 6020",
        "CERCLA"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC20",
    topic="Soil Contamination: Hydrocarbons",
    keywords=["hydrocarbons", "soil contamination", "petroleum", "PAH", "remediation"],
    conclusion_template="Hydrocarbon contamination in soil results from spills and leaks. Regulatory standards set cleanup levels and require monitoring and remediation.",
    reasoning_framework=(
        "Hydrocarbons (petroleum, PAH) contaminate soil from spills, leaks, and industrial activities. "
        "Health impacts include carcinogenicity, ecosystem disruption, and groundwater contamination. "
        "EPA and CERCLA set cleanup levels and require monitoring and remediation. "
        "Analytical methods include EPA 8015 (GC/FID), EPA 8270 (GC/MS), and soil sampling protocols. "
        "QA/QC involves calibration, blanks, replicates, and chain of custody. "
        "Risk assessment considers exposure pathways, bioavailability, and population vulnerability. "
        "Resolution integrates monitoring, remediation, and regulatory compliance."
    ),
    key_factors=[
        "Contaminant concentration",
        "Bioavailability",
        "Exposure pathways",
        "Cleanup levels",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 8015 (GC/FID)",
        "EPA 8270 (GC/MS)",
        "CERCLA"
    ],
    burden_holder="Site owner",
    adversary_position="Regulator may challenge cleanup adequacy or monitoring",
    counter_arguments=[
        "Measurement uncertainty",
        "Bioavailability variability",
        "Exposure pathway complexity",
        "Regulatory interpretation",
        "Remediation limitations"
    ],
    resolution_strategy="Apply robust QA/QC, optimize remediation, and ensure regulatory compliance.",
    entity_scope="Contaminated sites, industrial facilities",
    confidence=0.96,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 8015",
        "EPA 8270",
        "CERCLA"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC21",
    topic="Soil Contamination: Pesticides",
    keywords=["pesticides", "soil contamination", "organophosphates", "chlorinated", "remediation"],
    conclusion_template="Pesticide contamination in soil poses risks to human health and ecosystems. Regulatory standards set cleanup levels and require monitoring and remediation.",
    reasoning_framework=(
        "Pesticides (organophosphates, chlorinated) contaminate soil from agricultural and urban sources. "
        "Health impacts include neurotoxicity, carcinogenicity, and ecosystem disruption. "
        "EPA and CERCLA set cleanup levels and require monitoring and remediation. "
        "Analytical methods include EPA 8081 (GC/ECD), EPA 8151 (GC/FID), and soil sampling protocols. "
        "QA/QC involves calibration, blanks, replicates, and chain of custody. "
        "Risk assessment considers exposure pathways, bioavailability, and population vulnerability. "
        "Resolution integrates monitoring, remediation, and regulatory compliance."
    ),
    key_factors=[
        "Contaminant concentration",
        "Bioavailability",
        "Exposure pathways",
        "Cleanup levels",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 8081 (GC/ECD)",
        "EPA 8151 (GC/FID)",
        "CERCLA"
    ],
    burden_holder="Site owner",
    adversary_position="Regulator may challenge cleanup adequacy or monitoring",
    counter_arguments=[
        "Measurement uncertainty",
        "Bioavailability variability",
        "Exposure pathway complexity",
        "Regulatory interpretation",
        "Remediation limitations"
    ],
    resolution_strategy="Apply robust QA/QC, optimize remediation, and ensure regulatory compliance.",
    entity_scope="Contaminated sites, agricultural areas",
    confidence=0.95,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 8081",
        "EPA 8151",
        "CERCLA"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC22",
    topic="Soil Contamination: PFAS",
    keywords=["PFAS", "perfluorinated", "soil contamination", "remediation", "health"],
    conclusion_template="Per- and polyfluoroalkyl substances (PFAS) are persistent soil contaminants with health risks. Regulatory standards set cleanup levels and require monitoring and remediation.",
    reasoning_framework=(
        "PFAS (PFOA, PFOS) accumulate in soil from industrial, firefighting, and consumer sources. "
        "Health impacts include carcinogenicity, endocrine disruption, and ecosystem effects. "
        "EPA and CERCLA set cleanup levels and require monitoring and remediation. "
        "Analytical methods include EPA 537 (LC/MS/MS), EPA 8327 (LC/MS/MS), and soil sampling protocols. "
        "QA/QC involves calibration, blanks, replicates, and chain of custody. "
        "Risk assessment considers exposure pathways, bioavailability, and population vulnerability. "
        "Resolution integrates monitoring, remediation, and regulatory compliance."
    ),
    key_factors=[
        "Contaminant concentration",
        "Bioavailability",
        "Exposure pathways",
        "Cleanup levels",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 537 (LC/MS/MS)",
        "EPA 8327 (LC/MS/MS)",
        "CERCLA"
    ],
    burden_holder="Site owner",
    adversary_position="Regulator may challenge cleanup adequacy or monitoring",
    counter_arguments=[
        "Measurement uncertainty",
        "Bioavailability variability",
        "Exposure pathway complexity",
        "Regulatory interpretation",
        "Remediation limitations"
    ],
    resolution_strategy="Apply robust QA/QC, optimize remediation, and ensure regulatory compliance.",
    entity_scope="Contaminated sites, industrial facilities",
    confidence=0.94,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 537",
        "EPA 8327",
        "CERCLA"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC23",
    topic="Groundwater Contamination: DNAPL",
    keywords=["DNAPL", "dense non-aqueous phase liquid", "groundwater contamination", "plume", "remediation"],
    conclusion_template="DNAPL contamination in groundwater poses complex remediation challenges due to plume migration and persistence. Regulatory standards require monitoring and remediation.",
    reasoning_framework=(
        "DNAPLs (chlorinated solvents, PCBs) sink below the water table, forming persistent plumes. "
        "Health impacts include carcinogenicity, ecosystem disruption, and drinking water contamination. "
        "EPA and CERCLA set cleanup levels and require monitoring and remediation. "
        "Analytical methods include EPA 8260 (GC/MS), EPA 8270 (GC/MS), and groundwater sampling protocols. "
        "QA/QC involves calibration, blanks, replicates, and chain of custody. "
        "Risk assessment considers plume migration, exposure pathways, and population vulnerability. "
        "Resolution integrates monitoring, remediation, and regulatory compliance."
    ),
    key_factors=[
        "Plume migration",
        "Contaminant concentration",
        "Exposure pathways",
        "Cleanup levels",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 8260 (GC/MS)",
        "EPA 8270 (GC/MS)",
        "CERCLA"
    ],
    burden_holder="Site owner",
    adversary_position="Regulator may challenge remediation adequacy or monitoring",
    counter_arguments=[
        "Measurement uncertainty",
        "Plume complexity",
        "Exposure pathway variability",
        "Regulatory interpretation",
        "Remediation limitations"
    ],
    resolution_strategy="Apply robust QA/QC, optimize remediation, and ensure regulatory compliance.",
    entity_scope="Contaminated sites, groundwater",
    confidence=0.97,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 8260",
        "EPA 8270",
        "CERCLA"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC24",
    topic="Groundwater Contamination: LNAPL",
    keywords=["LNAPL", "light non-aqueous phase liquid", "groundwater contamination", "plume", "remediation"],
    conclusion_template="LNAPL contamination in groundwater poses remediation challenges due to plume migration and persistence. Regulatory standards require monitoring and remediation.",
    reasoning_framework=(
        "LNAPLs (petroleum, BTEX) float on the water table, forming plumes that migrate with groundwater flow. "
        "Health impacts include carcinogenicity, ecosystem disruption, and drinking water contamination. "
        "EPA and CERCLA set cleanup levels and require monitoring and remediation. "
        "Analytical methods include EPA 8015 (GC/FID), EPA 8021 (GC/MS), and groundwater sampling protocols. "
        "QA/QC involves calibration, blanks, replicates, and chain of custody. "
        "Risk assessment considers plume migration, exposure pathways, and population vulnerability. "
        "Resolution integrates monitoring, remediation, and regulatory compliance."
    ),
    key_factors=[
        "Plume migration",
        "Contaminant concentration",
        "Exposure pathways",
        "Cleanup levels",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA 8015 (GC/FID)",
        "EPA 8021 (GC/MS)",
        "CERCLA"
    ],
    burden_holder="Site owner",
    adversary_position="Regulator may challenge remediation adequacy or monitoring",
    counter_arguments=[
        "Measurement uncertainty",
        "Plume complexity",
        "Exposure pathway variability",
        "Regulatory interpretation",
        "Remediation limitations"
    ],
    resolution_strategy="Apply robust QA/QC, optimize remediation, and ensure regulatory compliance.",
    entity_scope="Contaminated sites, groundwater",
    confidence=0.96,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA 8015",
        "EPA 8021",
        "CERCLA"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC25",
    topic="Groundwater Contamination: Plume Migration",
    keywords=["plume migration", "groundwater contamination", "hydrogeology", "remediation", "monitoring"],
    conclusion_template="Plume migration in groundwater is governed by hydrogeology, contaminant properties, and remediation strategies. Regulatory standards require monitoring and modeling.",
    reasoning_framework=(
        "Plume migration is influenced by hydraulic gradient, permeability, contaminant properties, and remediation activities. "
        "EPA and CERCLA require monitoring wells, modeling, and remediation. "
        "Analytical methods include groundwater sampling, tracer tests, and modeling (MODFLOW, MT3DMS). "
        "QA/QC involves calibration, blanks, replicates, and chain of custody. "
        "Risk assessment considers exposure pathways, plume stability, and population vulnerability. "
        "Resolution integrates monitoring, modeling, and regulatory compliance."
    ),
    key_factors=[
        "Hydraulic gradient",
        "Permeability",
        "Contaminant properties",
        "Monitoring",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA Groundwater Monitoring Guidance",
        "CERCLA",
        "USGS MODFLOW Documentation"
    ],
    burden_holder="Site owner",
    adversary_position="Regulator may challenge monitoring adequacy or modeling",
    counter_arguments=[
        "Measurement uncertainty",
        "Modeling limitations",
        "Hydrogeologic complexity",
        "Regulatory interpretation",
        "Remediation limitations"
    ],
    resolution_strategy="Apply robust QA/QC, optimize monitoring and modeling, and ensure regulatory compliance.",
    entity_scope="Contaminated sites, groundwater",
    confidence=0.95,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA Groundwater Guidance",
        "CERCLA",
        "USGS MODFLOW"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC26",
    topic="Remediation Technologies: Bioremediation",
    keywords=["bioremediation", "remediation", "microbial", "contaminant", "soil"],
    conclusion_template="Bioremediation uses microorganisms to degrade contaminants in soil and groundwater. Regulatory standards require monitoring and performance validation.",
    reasoning_framework=(
        "Bioremediation employs indigenous or introduced microorganisms to degrade organic contaminants (hydrocarbons, solvents, pesticides). "
        "Process efficacy depends on contaminant properties, microbial activity, environmental conditions, and operational control. "
        "EPA and CERCLA require monitoring and performance validation. "
        "Analytical methods include contaminant concentration measurement, microbial assays, and soil/water sampling. "
        "QA/QC involves calibration, blanks, replicates, and chain of custody. "
        "Risk assessment considers contaminant bioavailability, microbial activity, and population vulnerability. "
        "Resolution integrates monitoring, optimization, and regulatory compliance."
    ),
    key_factors=[
        "Microbial activity",
        "Contaminant properties",
        "Environmental conditions",
        "Monitoring",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA Bioremediation Guidance",
        "CERCLA",
        "ASTM E1943"
    ],
    burden_holder="Site owner",
    adversary_position="Regulator may challenge performance validation or monitoring",
    counter_arguments=[
        "Measurement uncertainty",
        "Microbial activity variability",
        "Environmental limitations",
        "Regulatory interpretation",
        "Remediation limitations"
    ],
    resolution_strategy="Apply robust QA/QC, optimize bioremediation, and ensure regulatory compliance.",
    entity_scope="Contaminated sites, soil, groundwater",
    confidence=0.97,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA Bioremediation Guidance",
        "CERCLA",
        "ASTM E1943"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC27",
    topic="Remediation Technologies: Phytoremediation",
    keywords=["phytoremediation", "remediation", "plants", "contaminant", "soil"],
    conclusion_template="Phytoremediation uses plants to remove or degrade contaminants in soil and groundwater. Regulatory standards require monitoring and performance validation.",
    reasoning_framework=(
        "Phytoremediation employs plants to uptake, degrade, or stabilize contaminants (heavy metals, hydrocarbons, pesticides). "
        "Process efficacy depends on plant species, contaminant properties, environmental conditions, and operational control. "
        "EPA and CERCLA require monitoring and performance validation. "
        "Analytical methods include contaminant concentration measurement, plant tissue analysis, and soil/water sampling. "
        "QA/QC involves calibration, blanks, replicates, and chain of custody. "
        "Risk assessment considers contaminant bioavailability, plant uptake, and population vulnerability. "
        "Resolution integrates monitoring, optimization, and regulatory compliance."
    ),
    key_factors=[
        "Plant species",
        "Contaminant properties",
        "Environmental conditions",
        "Monitoring",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA Phytoremediation Guidance",
        "CERCLA",
        "ASTM E2893"
    ],
    burden_holder="Site owner",
    adversary_position="Regulator may challenge performance validation or monitoring",
    counter_arguments=[
        "Measurement uncertainty",
        "Plant uptake variability",
        "Environmental limitations",
        "Regulatory interpretation",
        "Remediation limitations"
    ],
    resolution_strategy="Apply robust QA/QC, optimize phytoremediation, and ensure regulatory compliance.",
    entity_scope="Contaminated sites, soil, groundwater",
    confidence=0.96,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA Phytoremediation Guidance",
        "CERCLA",
        "ASTM E2893"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC28",
    topic="Remediation Technologies: Chemical Oxidation",
    keywords=["chemical oxidation", "remediation", "oxidant", "contaminant", "soil"],
    conclusion_template="Chemical oxidation uses oxidants to degrade contaminants in soil and groundwater. Regulatory standards require monitoring and performance validation.",
    reasoning_framework=(
        "Chemical oxidation employs oxidants (permanganate, hydrogen peroxide, ozone) to degrade organic contaminants (hydrocarbons, solvents, pesticides). "
        "Process efficacy depends on oxidant dose, contaminant properties, environmental conditions, and operational control. "
        "EPA and CERCLA require monitoring and performance validation. "
        "Analytical methods include contaminant concentration measurement, oxidant residuals, and soil/water sampling. "
        "QA/QC involves calibration, blanks, replicates, and chain of custody. "
        "Risk assessment considers contaminant reactivity, oxidant distribution, and population vulnerability. "
        "Resolution integrates monitoring, optimization, and regulatory compliance."
    ),
    key_factors=[
        "Oxidant dose",
        "Contaminant properties",
        "Environmental conditions",
        "Monitoring",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA Chemical Oxidation Guidance",
        "CERCLA",
        "ASTM E2596"
    ],
    burden_holder="Site owner",
    adversary_position="Regulator may challenge performance validation or monitoring",
    counter_arguments=[
        "Measurement uncertainty",
        "Oxidant distribution variability",
        "Environmental limitations",
        "Regulatory interpretation",
        "Remediation limitations"
    ],
    resolution_strategy="Apply robust QA/QC, optimize chemical oxidation, and ensure regulatory compliance.",
    entity_scope="Contaminated sites, soil, groundwater",
    confidence=0.95,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA Chemical Oxidation Guidance",
        "CERCLA",
        "ASTM E2596"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC29",
    topic="Environmental Sampling: Chain of Custody and QA/QC",
    keywords=["sampling", "chain of custody", "QA/QC", "field blanks", "laboratory"],
    conclusion_template="Chain of custody and QA/QC are essential for environmental sampling integrity. Regulatory standards require documentation, field blanks, and laboratory QA/QC.",
    reasoning_framework=(
        "Chain of custody documents sample handling from collection to analysis, ensuring integrity and traceability. "
        "QA/QC includes field blanks, duplicates, calibration, and laboratory controls. "
        "EPA and Standard Methods require documentation and QA/QC protocols. "
        "Analytical methods include sample log forms, field blank analysis, and laboratory QA/QC checks. "
        "Risk assessment considers sample contamination, handling errors, and data integrity. "
        "Resolution integrates documentation, QA/QC, and regulatory compliance."
    ),
    key_factors=[
        "Chain of custody documentation",
        "Field blanks",
        "Laboratory QA/QC",
        "Sample handling",
        "Regulatory standards"
    ],
    primary_authority=[
        "EPA SW-846",
        "Standard Methods",
        "ISO 17025"
    ],
    burden_holder="Sampling team",
    adversary_position="Regulator may challenge sample integrity or QA/QC",
    counter_arguments=[
        "Documentation errors",
        "Sample contamination",
        "QA/QC variability",
        "Regulatory interpretation",
        "Laboratory limitations"
    ],
    resolution_strategy="Apply robust documentation, QA/QC, and ensure regulatory compliance.",
    entity_scope="Environmental sampling, laboratory analysis",
    confidence=0.97,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "EPA SW-846",
        "Standard Methods",
        "ISO 17025"
    ]
))

_add_doctrine(DoctrineBlock(
    doctrine_id="DC30",
    topic="Environmental Regulations: CERCLA, RCRA, CWA, CAA, TSCA",
    keywords=["CERCLA", "RCRA", "CWA", "CAA", "TSCA", "regulations"],
    conclusion_template="CERCLA, RCRA, CWA, CAA, and TSCA are major US environmental regulations governing contamination, waste, water, air, and toxic substances. Compliance requires monitoring, reporting, and remediation.",
    reasoning_framework=(
        "CERCLA governs hazardous site cleanup and liability. "
        "RCRA regulates hazardous waste generation, storage, and disposal. "
        "CWA sets water quality standards and discharge permits. "
        "CAA sets air quality standards and emission limits. "
        "TSCA regulates toxic substances and chemical inventory. "
        "EPA enforces compliance, monitoring, reporting, and remediation. "
        "Analytical methods include environmental sampling, monitoring, and reporting protocols. "
        "QA/QC involves calibration, blanks, replicates, and chain of custody. "
        "Risk assessment considers regulatory requirements, site-specific factors, and population vulnerability. "
        "Resolution integrates compliance, monitoring, and remediation."
    ),
    key_factors=[
        "Regulatory requirements",
        "Monitoring",
        "Reporting",
        "Remediation",
        "Compliance"
    ],
    primary_authority=[
        "CERCLA",
        "RCRA",
        "CWA",
        "CAA",
        "TSCA"
    ],
    burden_holder="Facility/site owner",
    adversary_position="Regulator may challenge compliance or reporting",
    counter_arguments=[
        "Regulatory interpretation",
        "Reporting errors",
        "Monitoring limitations",
        "Remediation constraints",
        "Site-specific complexity"
    ],
    resolution_strategy="Apply robust monitoring, reporting, and remediation for regulatory compliance.",
    entity_scope="Industrial facilities, contaminated sites",
    confidence=0.98,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "CERCLA",
        "RCRA",
        "CWA",
        "CAA",
        "TSCA"
    ]
))

# =========================
# AUTHORITY HARDENING
# =========================

authority_weights = {
    "EPA": 1.0,
    "WHO": 0.95,
    "State Standards": 0.9,
    "Standard Methods": 0.85,
    "ISO": 0.8,
    "USGS": 0.75,
    "ASTM": 0.7,
    "Kyoto Protocol": 0.65,
    "Paris Agreement": 0.65,
    "CERCLA": 1.0,
    "RCRA": 1.0,
    "CWA": 1.0,
    "CAA": 1.0,
    "TSCA": 1.0
}

def resolve_authority_conflict(authorities: List[str]) -> List[str]:
    sorted_auth = sorted(authorities, key=lambda x: authority_weights.get(x.split()[0], 0), reverse=True)
    return sorted_auth

# =========================
# SEMANTIC NORMALIZATION
# =========================

domain_term_mappings = {
    "pH": "hydrogen ion concentration",
    "alkalinity": "acid neutralizing capacity",
    "hardness": "calcium and magnesium concentration",
    "DO": "dissolved oxygen",
    "BOD": "biological oxygen demand",
    "COD": "chemical oxygen demand",
    "coagulation": "particle destabilization",
    "flocculation": "particle aggregation",
    "sedimentation": "gravity settling",
    "filtration": "media particle removal",
    "disinfection": "pathogen inactivation",
    "activated sludge": "aerobic biological treatment",
    "trickling filter": "biofilm-based secondary treatment",
    "UASB": "anaerobic digestion",
    "MBR": "membrane bioreactor",
    "SOx": "sulfur oxides",
    "NOx": "nitrogen oxides",
    "VOC": "volatile organic compounds",
    "PM2.5": "fine particulate matter",
    "PM10": "coarse particulate matter",
    "ozone": "O3",
    "photochemical smog": "secondary air pollution",
    "acid rain": "low pH precipitation",
    "greenhouse gases": "CO2, CH4, N2O",
    "heavy metals": "lead, cadmium, arsenic, mercury",
    "hydrocarbons": "petroleum and PAH",
    "pesticides": "organophosphates and chlorinated compounds",
    "PFAS": "perfluorinated substances",
    "DNAPL": "dense non-aqueous phase liquid",
    "LNAPL": "light non-aqueous phase liquid",
    "plume migration": "contaminant transport",
    "bioremediation": "microbial degradation",
    "phytoremediation": "plant-based remediation",
    "chemical oxidation": "oxidant-based degradation",
    "sampling": "sample collection",
    "chain of custody": "sample tracking",
    "QA/QC": "quality assurance and quality control",
    "field blanks": "contamination check samples",
    "regulations": "statutory requirements",
    "risk assessment": "exposure and hazard evaluation",
    "ERA": "ecological risk assessment",
    "bioaccumulation": "trophic transfer",
    "monitoring": "ambient and continuous measurement",
    "PBT": "persistence, bioaccumulation, toxicity",
    "green chemistry": "12 principles",
    "LCA": "life cycle assessment",
    "fate and transport": "contaminant movement",
    "Henry's law": "partition coefficient",
    "EPA 500 series": "drinking water methods",
    "EPA 600 series": "wastewater methods",
    "EPA 8000 series": "hazardous waste methods",
    "EIA": "environmental impact assessment",
    "NEPA": "National Environmental Policy Act",
    "carbon footprint": "greenhouse gas inventory",
    "Scope 1": "direct emissions",
    "Scope 2": "indirect emissions",
    "Scope 3": "value chain emissions"
}

def normalize_terms(text: str) -> str:
    for k, v in domain_term_mappings.items():
        text = text.replace(k, v)
    return text

# =========================
# EPISTEMIC GUARDRAILS
# =========================

BANNED_PHRASES = [
    "always", "never", "cannot", "impossible", "guaranteed", "no risk", "perfect", "absolute", "certain", "zero", "100%"
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "")
    return text

# =========================
# FACT FRAGILITY SCORING
# =========================

def score_fact_fragility(fact: str) -> Dict[str, float]:
    verifiability = 1.0 if any(auth in fact for auth in authority_weights) else 0.7
    recharacterization_risk = 0.2 if "uncertainty" in fact or "variability" in fact else 0.05
    testimony_dependence = 0.15 if "QA/QC" in fact or "chain of custody" in fact else 0.05
    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence
    }

# =========================
# THREE-LAYER RESPONSE
# =========================

def doctrine_layer(query: QueryRequest) -> Tuple[DoctrineBlock, float]:
    for block in doctrine_cache.values():
        if any(k in query.scenario.lower() for k in block.keywords):
            return block, block.confidence
    return None, 0.0

def semantic_layer(query: QueryRequest) -> Tuple[DoctrineBlock, float]:
    scenario_norm = normalize_terms(query.scenario.lower())
    for block in doctrine_cache.values():
        if any(normalize_terms(k) in scenario_norm for k in block.keywords):
            return block, block.confidence * 0.95
    return None, 0.0

def deep_analysis_layer(query: QueryRequest) -> Tuple[DoctrineBlock, float]:
    scenario_norm = normalize_terms(query.scenario.lower())
    best_block = None
    best_score = 0.0
    for block in doctrine_cache.values():
        score = sum(1 for k in block.keywords if normalize_terms(k) in scenario_norm)
        if score > best_score:
            best_block = block
            best_score = score
    if best_block:
        return best_block, best_block.confidence * 0.9
    return None, 0.0

# =========================
# DEEP ANALYSIS
# =========================

def multi_doctrine_decomposition(query: QueryRequest) -> List[DoctrineBlock]:
    scenario_norm = normalize_terms(query.scenario.lower())
    blocks = []
    for block in doctrine_cache.values():
        if any(normalize_terms(k) in scenario_norm for k in block.keywords):
            blocks.append(block)
    return blocks

def issue_category_mapping(query: QueryRequest) -> IssueCategory:
    scenario_norm = normalize_terms(query.scenario.lower())
    for cat in IssueCategory:
        if cat.value.lower() in scenario_norm:
            return cat
    return IssueCategory.ENVIRONMENTAL_REGULATIONS

def interaction_dag(blocks: List[DoctrineBlock]) -> Dict[str, List[str]]:
    dag
