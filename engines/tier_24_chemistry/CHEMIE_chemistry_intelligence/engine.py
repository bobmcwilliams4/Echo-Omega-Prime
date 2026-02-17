import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request, Response, HTTPException
from pydantic import BaseModel, Field, validator
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field as dataclass_field
from typing import List, Dict, Optional, Any, Union, Tuple
import enum
from datetime import datetime, timedelta
import asyncio
import aiohttp
import json
import time
import statistics
import collections

# Engine Constants
ENGINE_ID = "CHEMIE"
ENGINE_PORT = 8852
ENGINE_NAME = "Chemistry Intelligence Engine — Domain Orchestrator"
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
    SYNTHESIS = "SYNTHESIS"
    ANALYSIS = "ANALYSIS"
    POLYMER = "POLYMER"
    ELECTROCHEMISTRY = "ELECTROCHEMISTRY"
    THERMODYNAMICS = "THERMODYNAMICS"
    KINETICS = "KINETICS"
    SPECTROSCOPY = "SPECTROSCOPY"
    CRYSTALLOGRAPHY = "CRYSTALLOGRAPHY"
    COMPUTATIONAL = "COMPUTATIONAL"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    INORGANIC = "INORGANIC"
    BIOCHEMISTRY = "BIOCHEMISTRY"
    MATERIALS = "MATERIALS"
    NUCLEAR = "NUCLEAR"
    SURFACE = "SURFACE"
    PHOTOCHEMISTRY = "PHOTOCHEMISTRY"
    GEOCHEMISTRY = "GEOCHEMISTRY"
    FOOD = "FOOD"
    FORENSIC = "FORENSIC"
    INDUSTRIAL = "INDUSTRIAL"
    SAFETY = "SAFETY"
    REGULATORY = "REGULATORY"
    QUALITY = "QUALITY"
    EDUCATION = "EDUCATION"
    PATENTS = "PATENTS"
    LITERATURE = "LITERATURE"
    TOXICOLOGY = "TOXICOLOGY"
    PROCESS = "PROCESS"
    CATALYSIS = "CATALYSIS"
    NANOTECHNOLOGY = "NANOTECHNOLOGY"

class SubEngineStatus(enum.Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

# Pydantic Models
class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    question: str
    context: Optional[str]
    response_mode: ResponseMode = ResponseMode.FAST
    position_zone: PositionZone = PositionZone.PLANNING
    confidence_zone: ConfidenceZone = ConfidenceZone.DEFENSIBLE
    issue_category: Optional[IssueCategory]
    metadata: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query_id: str
    engine_id: str
    subengine_id: str
    answer: str
    confidence: float
    response_mode: ResponseMode
    position_zone: PositionZone
    confidence_zone: ConfidenceZone
    issue_category: Optional[IssueCategory]
    latency_ms: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class SubEngineConfig(BaseModel):
    engine_id: str
    name: str
    port: int
    health_url: str
    capabilities: List[str]
    weight: float = 1.0
    status: SubEngineStatus = SubEngineStatus.UNKNOWN
    domains: List[str]

class RoutingDecision(BaseModel):
    query_id: str
    selected_engine_id: str
    selected_domains: List[str]
    rationale: str
    routing_score: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decision: RoutingDecision
    subengine_response: Optional[QueryResponse]
    orchestration_latency_ms: int
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# Sub-Engine Registry
SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "CHEM01": SubEngineConfig(
        engine_id="CHEM01",
        name="Organic Synthesis",
        port=8853,
        health_url="http://localhost:8853/health",
        capabilities=["reaction design", "retrosynthesis", "organic mechanisms", "named reactions"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["synthesis", "organic", "reaction", "mechanism", "retrosynthesis", "named reaction"]
    ),
    "CHEM02": SubEngineConfig(
        engine_id="CHEM02",
        name="Analytical Methods",
        port=8854,
        health_url="http://localhost:8854/health",
        capabilities=["chromatography", "spectrometry", "titration", "elemental analysis"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["analysis", "analytical", "chromatography", "spectrometry", "titration", "elemental"]
    ),
    "CHEM03": SubEngineConfig(
        engine_id="CHEM03",
        name="Polymer Science",
        port=8855,
        health_url="http://localhost:8855/health",
        capabilities=["polymerization", "polymer properties", "macromolecules"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["polymer", "polymerization", "macromolecule", "plastics", "elastomer", "copolymer"]
    ),
    "CHEM04": SubEngineConfig(
        engine_id="CHEM04",
        name="Electrochemistry",
        port=8856,
        health_url="http://localhost:8856/health",
        capabilities=["redox", "electrolysis", "batteries", "fuel cells"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["electrochemistry", "redox", "electrolysis", "battery", "fuel cell", "electrode"]
    ),
    "CHEM05": SubEngineConfig(
        engine_id="CHEM05",
        name="Thermodynamics",
        port=8857,
        health_url="http://localhost:8857/health",
        capabilities=["enthalpy", "entropy", "gibbs free energy", "phase diagrams"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["thermodynamics", "enthalpy", "entropy", "gibbs", "phase diagram", "calorimetry"]
    ),
    "CHEM06": SubEngineConfig(
        engine_id="CHEM06",
        name="Kinetics",
        port=8858,
        health_url="http://localhost:8858/health",
        capabilities=["reaction rate", "mechanism", "activation energy"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["kinetics", "rate", "mechanism", "activation energy", "rate law", "catalysis"]
    ),
    "CHEM07": SubEngineConfig(
        engine_id="CHEM07",
        name="Spectroscopy",
        port=8859,
        health_url="http://localhost:8859/health",
        capabilities=["NMR", "IR", "UV-Vis", "mass spectrometry"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["spectroscopy", "NMR", "IR", "UV-Vis", "mass spec", "Raman", "EPR"]
    ),
    "CHEM08": SubEngineConfig(
        engine_id="CHEM08",
        name="Crystallography",
        port=8860,
        health_url="http://localhost:8860/health",
        capabilities=["X-ray", "structure determination", "diffraction"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["crystallography", "X-ray", "diffraction", "structure", "unit cell", "lattice"]
    ),
    "CHEM09": SubEngineConfig(
        engine_id="CHEM09",
        name="Computational Chemistry",
        port=8861,
        health_url="http://localhost:8861/health",
        capabilities=["DFT", "molecular modeling", "quantum chemistry"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["computational", "DFT", "molecular modeling", "quantum", "simulation", "ab initio"]
    ),
    "CHEM10": SubEngineConfig(
        engine_id="CHEM10",
        name="Environmental Chemistry",
        port=8862,
        health_url="http://localhost:8862/health",
        capabilities=["pollution", "remediation", "atmospheric chemistry"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["environmental", "pollution", "remediation", "atmosphere", "water", "soil", "ecotoxicology"]
    ),
    "CHEM11": SubEngineConfig(
        engine_id="CHEM11",
        name="Inorganic Chemistry",
        port=8863,
        health_url="http://localhost:8863/health",
        capabilities=["coordination", "organometallics", "main group"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["inorganic", "coordination", "organometallic", "main group", "transition metal"]
    ),
    "CHEM12": SubEngineConfig(
        engine_id="CHEM12",
        name="Biochemistry",
        port=8864,
        health_url="http://localhost:8864/health",
        capabilities=["enzymes", "metabolism", "proteins", "nucleic acids"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["biochemistry", "enzyme", "metabolism", "protein", "DNA", "RNA", "lipid"]
    ),
    "CHEM13": SubEngineConfig(
        engine_id="CHEM13",
        name="Materials Science",
        port=8865,
        health_url="http://localhost:8865/health",
        capabilities=["materials", "nanomaterials", "composites"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["materials", "composite", "nanomaterial", "ceramic", "alloy", "semiconductor"]
    ),
    "CHEM14": SubEngineConfig(
        engine_id="CHEM14",
        name="Nuclear Chemistry",
        port=8866,
        health_url="http://localhost:8866/health",
        capabilities=["radioactivity", "isotopes", "nuclear reactions"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["nuclear", "radioactivity", "isotope", "fission", "fusion", "decay"]
    ),
    "CHEM15": SubEngineConfig(
        engine_id="CHEM15",
        name="Surface Chemistry",
        port=8867,
        health_url="http://localhost:8867/health",
        capabilities=["adsorption", "interfaces", "colloids"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["surface", "adsorption", "interface", "colloid", "emulsion", "surfactant"]
    ),
    "CHEM16": SubEngineConfig(
        engine_id="CHEM16",
        name="Photochemistry",
        port=8868,
        health_url="http://localhost:8868/health",
        capabilities=["photoreactions", "photophysics", "photosensitizers"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["photochemistry", "photoreaction", "photophysics", "photosensitizer", "fluorescence", "phosphorescence"]
    ),
    "CHEM17": SubEngineConfig(
        engine_id="CHEM17",
        name="Geochemistry",
        port=8869,
        health_url="http://localhost:8869/health",
        capabilities=["mineralogy", "isotope geochemistry", "petrology"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["geochemistry", "mineralogy", "petrology", "isotope", "geological", "earth"]
    ),
    "CHEM18": SubEngineConfig(
        engine_id="CHEM18",
        name="Food Chemistry",
        port=8870,
        health_url="http://localhost:8870/health",
        capabilities=["nutrition", "food additives", "flavor chemistry"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["food", "nutrition", "additive", "flavor", "preservative", "food safety"]
    ),
    "CHEM19": SubEngineConfig(
        engine_id="CHEM19",
        name="Forensic Chemistry",
        port=8871,
        health_url="http://localhost:8871/health",
        capabilities=["toxicology", "trace analysis", "drug identification"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["forensic", "toxicology", "trace", "drug", "crime", "evidence"]
    ),
    "CHEM20": SubEngineConfig(
        engine_id="CHEM20",
        name="Industrial Chemistry",
        port=8872,
        health_url="http://localhost:8872/health",
        capabilities=["process chemistry", "scale-up", "chemical engineering"],
        weight=1.0,
        status=SubEngineStatus.UNKNOWN,
        domains=["industrial", "process", "scale-up", "engineering", "plant", "manufacturing"]
    ),
}

# Routing Rules (domain keyword to engine_id mapping)
ROUTING_RULES: Dict[str, str] = {
    # CHEM01 Organic Synthesis
    "synthesis": "CHEM01",
    "retrosynthesis": "CHEM01",
    "organic": "CHEM01",
    "reaction": "CHEM01",
    "mechanism": "CHEM01",
    "named reaction": "CHEM01",
    "aldol": "CHEM01",
    "grignard": "CHEM01",
    "friedel-crafts": "CHEM01",
    "wittig": "CHEM01",
    "diels-alder": "CHEM01",
    "oxidation": "CHEM01",
    "reduction": "CHEM01",
    "esterification": "CHEM01",
    "amide": "CHEM01",
    "alkylation": "CHEM01",
    "acylation": "CHEM01",
    "elimination": "CHEM01",
    "substitution": "CHEM01",
    "aromatic": "CHEM01",
    "alkene": "CHEM01",
    "alkyne": "CHEM01",
    "carbocation": "CHEM01",
    "carbanion": "CHEM01",
    "enolate": "CHEM01",
    "organolithium": "CHEM01",
    "organometallic": "CHEM11",
    # CHEM02 Analytical Methods
    "analysis": "CHEM02",
    "analytical": "CHEM02",
    "chromatography": "CHEM02",
    "hplc": "CHEM02",
    "gc": "CHEM02",
    "titration": "CHEM02",
    "spectrometry": "CHEM02",
    "elemental": "CHEM02",
    "quantification": "CHEM02",
    "calibration": "CHEM02",
    "standard curve": "CHEM02",
    "detection limit": "CHEM02",
    "precision": "CHEM02",
    "accuracy": "CHEM02",
    "validation": "CHEM02",
    "method development": "CHEM02",
    "sample preparation": "CHEM02",
    "extraction": "CHEM02",
    "mass spectrometry": "CHEM07",
    # CHEM03 Polymer Science
    "polymer": "CHEM03",
    "polymerization": "CHEM03",
    "macromolecule": "CHEM03",
    "plastic": "CHEM03",
    "elastomer": "CHEM03",
    "copolymer": "CHEM03",
    "block copolymer": "CHEM03",
    "thermoplastic": "CHEM03",
    "thermoset": "CHEM03",
    "crosslinking": "CHEM03",
    "polyethylene": "CHEM03",
    "polypropylene": "CHEM03",
    "polystyrene": "CHEM03",
    "polyamide": "CHEM03",
    "polyester": "CHEM03",
    # CHEM04 Electrochemistry
    "electrochemistry": "CHEM04",
    "redox": "CHEM04",
    "electrolysis": "CHEM04",
    "battery": "CHEM04",
    "fuel cell": "CHEM04",
    "electrode": "CHEM04",
    "voltammetry": "CHEM04",
    "potentiometry": "CHEM04",
    "galvanic": "CHEM04",
    "electroplating": "CHEM04",
    "corrosion": "CHEM04",
    # CHEM05 Thermodynamics
    "thermodynamics": "CHEM05",
    "enthalpy": "CHEM05",
    "entropy": "CHEM05",
    "gibbs": "CHEM05",
    "free energy": "CHEM05",
    "phase diagram": "CHEM05",
    "calorimetry": "CHEM05",
    "heat capacity": "CHEM05",
    "spontaneity": "CHEM05",
    "equilibrium": "CHEM05",
    "vapor pressure": "CHEM05",
    "boiling point": "CHEM05",
    "melting point": "CHEM05",
    "triple point": "CHEM05",
    # CHEM06 Kinetics
    "kinetics": "CHEM06",
    "rate": "CHEM06",
    "activation energy": "CHEM06",
    "rate law": "CHEM06",
    "catalysis": "CHEM06",
    "catalyst": "CHEM06",
    "reaction order": "CHEM06",
    "half-life": "CHEM06",
    "arrhenius": "CHEM06",
    "transition state": "CHEM06",
    "mechanistic": "CHEM06",
    # CHEM07 Spectroscopy
    "spectroscopy": "CHEM07",
    "nmr": "CHEM07",
    "ir": "CHEM07",
    "uv-vis": "CHEM07",
    "raman": "CHEM07",
    "epr": "CHEM07",
    "fluorescence": "CHEM16",
    "phosphorescence": "CHEM16",
    "absorbance": "CHEM07",
    "emission": "CHEM07",
    "chemical shift": "CHEM07",
    "coupling constant": "CHEM07",
    "multiplet": "CHEM07",
    # CHEM08 Crystallography
    "crystallography": "CHEM08",
    "x-ray": "CHEM08",
    "diffraction": "CHEM08",
    "structure": "CHEM08",
    "unit cell": "CHEM08",
    "lattice": "CHEM08",
    "space group": "CHEM08",
    "crystal system": "CHEM08",
    "miller index": "CHEM08",
    "single crystal": "CHEM08",
    "powder diffraction": "CHEM08",
    # CHEM09 Computational Chemistry
    "computational": "CHEM09",
    "dft": "CHEM09",
    "molecular modeling": "CHEM09",
    "quantum": "CHEM09",
    "simulation": "CHEM09",
    "ab initio": "CHEM09",
    "molecular dynamics": "CHEM09",
    "monte carlo": "CHEM09",
    "force field": "CHEM09",
    "basis set": "CHEM09",
    "gaussian": "CHEM09",
    "orca": "CHEM09",
    # CHEM10 Environmental Chemistry
    "environmental": "CHEM10",
    "pollution": "CHEM10",
    "remediation": "CHEM10",
    "atmosphere": "CHEM10",
    "water": "CHEM10",
    "soil": "CHEM10",
    "ecotoxicology": "CHEM10",
    "pesticide": "CHEM10",
    "waste": "CHEM10",
    "biodegradation": "CHEM10",
    "green chemistry": "CHEM10",
    # CHEM11 Inorganic Chemistry
    "inorganic": "CHEM11",
    "coordination": "CHEM11",
    "main group": "CHEM11",
    "transition metal": "CHEM11",
    "complex": "CHEM11",
    "ligand": "CHEM11",
    "crystal field": "CHEM11",
    "organometallic": "CHEM11",
    "bioinorganic": "CHEM11",
    "cluster": "CHEM11",
    "metal carbonyl": "CHEM11",
    # CHEM12 Biochemistry
    "biochemistry": "CHEM12",
    "enzyme": "CHEM12",
    "metabolism": "CHEM12",
    "protein": "CHEM12",
    "dna": "CHEM12",
    "rna": "CHEM12",
    "lipid": "CHEM12",
    "carbohydrate": "CHEM12",
    "amino acid": "CHEM12",
    "peptide": "CHEM12",
    "nucleic acid": "CHEM12",
    "glycolysis": "CHEM12",
    "krebs": "CHEM12",
    "photosynthesis": "CHEM12",
    "cell signaling": "CHEM12",
    # CHEM13 Materials Science
    "materials": "CHEM13",
    "composite": "CHEM13",
    "nanomaterial": "CHEM13",
    "ceramic": "CHEM13",
    "alloy": "CHEM13",
    "semiconductor": "CHEM13",
    "superconductor": "CHEM13",
    "thin film": "CHEM13",
    "coating": "CHEM13",
    "hardness": "CHEM13",
    "tensile": "CHEM13",
    "fracture": "CHEM13",
    # CHEM14 Nuclear Chemistry
    "nuclear": "CHEM14",
    "radioactivity": "CHEM14",
    "isotope": "CHEM14",
    "fission": "CHEM14",
    "fusion": "CHEM14",
    "decay": "CHEM14",
    "half-life": "CHEM14",
    "alpha particle": "CHEM14",
    "beta decay": "CHEM14",
    "gamma ray": "CHEM14",
    "radiation": "CHEM14",
    "nuclear reactor": "CHEM14",
    # CHEM15 Surface Chemistry
    "surface": "CHEM15",
    "adsorption": "CHEM15",
    "interface": "CHEM15",
    "colloid": "CHEM15",
    "emulsion": "CHEM15",
    "surfactant": "CHEM15",
    "micelle": "CHEM15",
    "zeta potential": "CHEM15",
    "contact angle": "CHEM15",
    "surface tension": "CHEM15",
    # CHEM16 Photochemistry
    "photochemistry": "CHEM16",
    "photoreaction": "CHEM16",
    "photophysics": "CHEM16",
    "photosensitizer": "CHEM16",
    "fluorescence": "CHEM16",
    "phosphorescence": "CHEM16",
    "excited state": "CHEM16",
    "singlet": "CHEM16",
    "triplet": "CHEM16",
    "photoisomerization": "CHEM16",
    # CHEM17 Geochemistry
    "geochemistry": "CHEM17",
    "mineralogy": "CHEM17",
    "petrology": "CHEM17",
    "isotope geochemistry": "CHEM17",
    "geological": "CHEM17",
    "earth": "CHEM17",
    "rock": "CHEM17",
    "sediment": "CHEM17",
    "ore": "CHEM17",
    "geothermal": "CHEM17",
    # CHEM18 Food Chemistry
    "food": "CHEM18",
    "nutrition": "CHEM18",
    "additive": "CHEM18",
    "flavor": "CHEM18",
    "preservative": "CHEM18",
    "food safety": "CHEM18",
    "allergen": "CHEM18",
    "spoilage": "CHEM18",
    "colorant": "CHEM18",
    "sweetener": "CHEM18",
    "emulsifier": "CHEM18",
    "stabilizer": "CHEM18",
    # CHEM19 Forensic Chemistry
    "forensic": "CHEM19",
    "toxicology": "CHEM19",
    "trace": "CHEM19",
    "drug": "CHEM19",
    "crime": "CHEM19",
    "evidence": "CHEM19",
    "explosive": "CHEM19",
    "arson": "CHEM19",
    "gunshot": "CHEM19",
    "blood": "CHEM19",
    "fiber": "CHEM19",
    # CHEM20 Industrial Chemistry
    "industrial": "CHEM20",
    "process": "CHEM20",
    "scale-up": "CHEM20",
    "engineering": "CHEM20",
    "plant": "CHEM20",
    "manufacturing": "CHEM20",
    "chemical engineering": "CHEM20",
    "process safety": "CHEM20",
    "process optimization": "CHEM20",
    "pilot plant": "CHEM20",
    "production": "CHEM20",
    # Cross-domain
    "patent": "CHEM01",
    "literature": "CHEM01",
    "education": "CHEM12",
    "regulatory": "CHEM10",
    "quality": "CHEM02",
    "safety": "CHEM20",
    "toxicity": "CHEM19",
    "risk assessment": "CHEM10",
    "nanotechnology": "CHEM13",
    "nanoparticle": "CHEM13",
    "catalyst": "CHEM06",
    "catalysis": "CHEM06",
    "process control": "CHEM20",
    "scale-up": "CHEM20",
    "biodegradation": "CHEM10",
    "green chemistry": "CHEM10",
    "bioinorganic": "CHEM11",
    "bioorganic": "CHEM01",
    "enzyme kinetics": "CHEM12",
    "metabolite": "CHEM12",
    "pharmacology": "CHEM19",
    "clinical chemistry": "CHEM02",
    "diagnostic": "CHEM02",
    "pharmaceutical": "CHEM01",
    "drug design": "CHEM09",
    "QSAR": "CHEM09",
    "structure-activity": "CHEM09",
    "cheminformatics": "CHEM09",
    "data analysis": "CHEM02",
    "statistical analysis": "CHEM02",
    "validation": "CHEM02",
    "compliance": "CHEM10",
    "waste management": "CHEM10",
    "hazard": "CHEM20",
    "incident": "CHEM20",
    "incident investigation": "CHEM20",
    "root cause": "CHEM20",
    "corrective action": "CHEM20",
    "preventive action": "CHEM20",
    "audit": "CHEM20",
    "inspection": "CHEM02",
    "sampling": "CHEM02",
    "batch": "CHEM20",
    "lot": "CHEM20",
    "traceability": "CHEM20",
    "inventory": "CHEM20",
    "supply chain": "CHEM20",
    "logistics": "CHEM20",
    "distribution": "CHEM20",
    "storage": "CHEM20",
    "packaging": "CHEM20",
    "labeling": "CHEM20",
    "documentation": "CHEM20",
    "recordkeeping": "CHEM20",
    "training": "CHEM12",
    "competency": "CHEM12",
    "qualification": "CHEM12",
    "certification": "CHEM12",
    "accreditation": "CHEM02",
    "proficiency": "CHEM02",
    "interlaboratory": "CHEM02",
    "round robin": "CHEM02",
    "reference material": "CHEM02",
    "standard": "CHEM02",
    "method": "CHEM02",
    "procedure": "CHEM02",
    "protocol": "CHEM02",
    "guideline": "CHEM02",
    "policy": "CHEM10",
    "regulation": "CHEM10",
    "law": "CHEM10",
    "compliance": "CHEM10",
    "inspection": "CHEM02",
    "audit": "CHEM20",
    "review": "CHEM20",
    "incident": "CHEM20",
    "investigation": "CHEM20",
    "root cause": "CHEM20",
    "corrective action": "CHEM20",
    "preventive action": "CHEM20",
    "CAPA": "CHEM20",
    "deviation": "CHEM20",
    "out of specification": "CHEM02",
    "OOS": "CHEM02",
    "out of trend": "CHEM02",
    "OOT": "CHEM02",
    "change control": "CHEM20",
    "risk management": "CHEM10",
    "hazard analysis": "CHEM20",
    "failure mode": "CHEM20",
    "FMEA": "CHEM20",
    "root cause analysis": "CHEM20",
    "CAPA": "CHEM20",
    "management review": "CHEM20",
    "continuous improvement": "CHEM20",
    "lean": "CHEM20",
    "six sigma": "CHEM20",
    "kaizen": "CHEM20",
    "process mapping": "CHEM20",
    "value stream": "CHEM20",
    "5S": "CHEM20",
    "GMP": "CHEM20",
    "GLP": "CHEM02",
    "GCP": "CHEM02",
    "GDP": "CHEM20",
    "SOP": "CHEM20",
    "work instruction": "CHEM20",
    "training record": "CHEM12",
    "competency assessment": "CHEM12",
    "qualification protocol": "CHEM12",
    "validation protocol": "CHEM02",
    "IQ": "CHEM20",
    "OQ": "CHEM20",
    "PQ": "CHEM20",
    "commissioning": "CHEM20",
    "decommissioning": "CHEM20",
    "calibration": "CHEM02",
    "maintenance": "CHEM20",
    "preventive maintenance": "CHEM20",
    "corrective maintenance": "CHEM20",
    "spare part": "CHEM20",
    "asset management": "CHEM20",
    "equipment": "CHEM20",
    "instrument": "CHEM02",
    "device": "CHEM02",
    "tool": "CHEM02",
    "facility": "CHEM20",
    "building": "CHEM20",
    "utility": "CHEM20",
    "HVAC": "CHEM20",
    "water system": "CHEM20",
    "compressed air": "CHEM20",
    "steam": "CHEM20",
    "wastewater": "CHEM10",
    "effluent": "CHEM10",
    "emission": "CHEM10",
    "discharge": "CHEM10",
    "permit": "CHEM10",
    "license": "CHEM10",
    "registration": "CHEM10",
    "notification": "CHEM10",
    "report": "CHEM20",
    "record": "CHEM20",
    "log": "CHEM20",
    "form": "CHEM20",
    "template": "CHEM20",
    "checklist": "CHEM20",
    "worksheet": "CHEM20",
    "spreadsheet": "CHEM20",
    "database": "CHEM09",
    "LIMS": "CHEM02",
    "ELN": "CHEM09",
    "ERP": "CHEM20",
    "MES": "CHEM20",
    "SCADA": "CHEM20",
    "PLC": "CHEM20",
    "automation": "CHEM20",
    "robotics": "CHEM20",
    "digital": "CHEM09",
    "AI": "CHEM09",
    "machine learning": "CHEM09",
    "deep learning": "CHEM09",
    "data science": "CHEM09",
    "big data": "CHEM09",
    "cloud": "CHEM09",
    "cybersecurity": "CHEM09",
    "IT": "CHEM09",
    "informatics": "CHEM09",
    "bioinformatics": "CHEM12",
    "cheminformatics": "CHEM09",
    "statistical": "CHEM02",
    "statistics": "CHEM02",
    "data mining": "CHEM09",
    "visualization": "CHEM09",
    "presentation": "CHEM20",
    "communication": "CHEM20",
    "meeting": "CHEM20",
    "agenda": "CHEM20",
    "minutes": "CHEM20",
    "action item": "CHEM20",
    "project": "CHEM20",
    "task": "CHEM20",
    "milestone": "CHEM20",
    "timeline": "CHEM20",
    "budget": "CHEM20",
    "cost": "CHEM20",
    "finance": "CHEM20",
    "procurement": "CHEM20",
    "purchase": "CHEM20",
    "order": "CHEM20",
    "invoice": "CHEM20",
    "payment": "CHEM20",
    "contract": "CHEM20",
    "agreement": "CHEM20",
    "supplier": "CHEM20",
    "vendor": "CHEM20",
    "customer": "CHEM20",
    "client": "CHEM20",
    "stakeholder": "CHEM20",
    "user": "CHEM20",
    "operator": "CHEM20",
    "manager": "CHEM20",
    "supervisor": "CHEM20",
    "director": "CHEM20",
    "executive": "CHEM20",
    "board": "CHEM20",
    "committee": "CHEM20",
    "team": "CHEM20",
    "group": "CHEM20",
    "department": "CHEM20",
    "division": "CHEM20",
    "organization": "CHEM20",
    "company": "CHEM20",
    "corporation": "CHEM20",
    "enterprise": "CHEM20",
    "industry": "CHEM20",
    "market": "CHEM20",
    "competition": "CHEM20",
    "trend": "CHEM20",
    "forecast": "CHEM20",
    "strategy": "CHEM20",
    "plan": "CHEM20",
    "roadmap": "CHEM20",
    "innovation": "CHEM20",
    "R&D": "CHEM20",
    "research": "CHEM01",
    "development": "CHEM01",
    "discovery": "CHEM01",
    "invention": "CHEM01",
    "patent": "CHEM01",
    "intellectual property": "CHEM01",
    "IP": "CHEM01",
    "copyright": "CHEM01",
    "trademark": "CHEM01",
    "brand": "CHEM20",
    "marketing": "CHEM20",
    "advertising": "CHEM20",
    "promotion": "CHEM20",
    "sales": "CHEM20",
    "distribution": "CHEM20",
    "retail": "CHEM20",
    "wholesale": "CHEM20",
    "export": "CHEM20",
    "import": "CHEM20",
    "logistics": "CHEM20",
    "shipping": "CHEM20",
    "freight": "CHEM20",
    "transportation": "CHEM20",
    "delivery": "CHEM20",
    "supply": "CHEM20",
    "demand": "CHEM20",
    "inventory": "CHEM20",
    "stock": "CHEM20",
    "warehouse": "CHEM20",
    "storage": "CHEM20",
    "handling": "CHEM20",
    "packaging": "CHEM20",
    "labeling": "CHEM20",
    "barcoding": "CHEM20",
    "serialization": "CHEM20",
    "traceability": "CHEM20",
    "recall": "CHEM20",
    "complaint": "CHEM20",
    "return": "CHEM20",
    "refund": "CHEM20",
    "replacement": "CHEM20",
    "service": "CHEM20",
    "support": "CHEM20",
    "helpdesk": "CHEM20",
    "ticket": "CHEM20",
    "issue": "CHEM20",
    "problem": "CHEM20",
    "incident": "CHEM20",
    "outage": "CHEM20",
    "downtime": "CHEM20",
    "uptime": "CHEM20",
    "availability": "CHEM20",
    "reliability": "CHEM20",
    "performance": "CHEM20",
    "scalability": "CHEM20",
    "flexibility": "CHEM20",
    "adaptability": "CHEM20",
    "resilience": "CHEM20",
    "robustness": "CHEM20",
    "redundancy": "CHEM20",
    "backup": "CHEM20",
    "restore": "CHEM20",
    "disaster recovery": "CHEM20",
    "business continuity": "CHEM20",
    "emergency": "CHEM20",
    "crisis": "CHEM20",
    "contingency": "CHEM20",
    "risk": "CHEM10",
    "hazard": "CHEM20",
    "threat": "CHEM20",
    "vulnerability": "CHEM20",
    "exposure": "CHEM20",
    "impact": "CHEM20",
    "likelihood": "CHEM20",
    "severity": "CHEM20",
    "consequence": "CHEM20",
    "mitigation": "CHEM20",
    "control": "CHEM20",
    "prevention": "CHEM20",
    "protection": "CHEM20",
    "detection": "CHEM02",
    "response": "CHEM20",
    "recovery": "CHEM20",
    "remediation": "CHEM10",
    "compensation": "CHEM20",
    "insurance": "CHEM20",
    "coverage": "CHEM20",
    "policy": "CHEM10",
    "procedure": "CHEM02",
    "protocol": "CHEM02",
    "guideline": "CHEM02",
    "standard": "CHEM02",
    "specification": "CHEM02",
    "requirement": "CHEM02",
    "criteria": "CHEM02",
    "benchmark": "CHEM02",
    "best practice": "CHEM02",
    "lesson learned": "CHEM20",
    "case study": "CHEM20",
    "example": "CHEM20",
    "template": "CHEM20",
    "toolkit": "CHEM20",
    "resource": "CHEM20",
    "reference": "CHEM02",
    "manual": "CHEM20",
    "handbook": "CHEM20",
    "guide": "CHEM20",
    "catalog": "CHEM20",
    "directory": "CHEM20",
    "database": "CHEM09",
    "repository": "CHEM09",
    "archive": "CHEM09",
    "library": "CHEM09",
    "collection": "CHEM09",
    "dataset": "CHEM09",
    "record": "CHEM20",
    "document": "CHEM20",
    "file": "CHEM20",
    "report": "CHEM20",
    "summary": "CHEM20",
    "overview": "CHEM20",
    "review": "CHEM20",
    "assessment": "CHEM10",
    "evaluation": "CHEM10",
    "analysis": "CHEM02",
    "interpretation": "CHEM02",
    "recommendation": "CHEM20",
    "conclusion": "CHEM20",
    "finding": "CHEM20",
    "observation": "CHEM20",
    "comment": "CHEM20",
    "note": "CHEM20",
    "remark": "CHEM20",
    "annotation": "CHEM20",
    "tag": "CHEM20",
    "keyword": "CHEM20",
    "index": "CHEM20",
    "classification": "CHEM20",
    "categorization": "CHEM20",
    "taxonomy": "CHEM20",
    "ontology": "CHEM20",
    "schema": "CHEM09",
    "model": "CHEM09",
    "framework": "CHEM09",
    "architecture": "CHEM09",
    "design": "CHEM09",
    "structure": "CHEM08",
    "system": "CHEM09",
    "platform": "CHEM09",
    "solution": "CHEM09",
    "application": "CHEM09",
    "software": "CHEM09",
    "hardware": "CHEM09",
    "device": "CHEM02",
    "instrument": "CHEM02",
    "equipment": "CHEM20",
    "machine": "CHEM20",
    "apparatus": "CHEM20",
    "tool": "CHEM02",
    "component": "CHEM20",
    "part": "CHEM20",
    "module": "CHEM09",
    "unit": "CHEM20",
    "assembly": "CHEM20",
    "subsystem": "CHEM09",
    "integration": "CHEM09",
    "interface": "CHEM15",
    "connection": "CHEM20",
    "network": "CHEM09",
    "communication": "CHEM20",
    "protocol": "CHEM02",
    "standard": "CHEM02",
    "specification": "CHEM02",
    "requirement": "CHEM02",
    "criteria": "CHEM02",
    "benchmark": "CHEM02",
    "performance": "CHEM20",
    "efficiency": "CHEM20",
    "effectiveness": "CHEM20",
    "productivity": "CHEM20",
    "quality": "CHEM02",
    "reliability": "CHEM20",
    "availability": "CHEM20",
    "maintainability": "CHEM20",
    "serviceability": "CHEM20",
    "usability": "CHEM20",
    "scalability": "CHEM20",
    "flexibility": "CHEM20",
    "adaptability": "CHEM20",
    "portability": "CHEM20",
    "compatibility": "CHEM20",
    "interoperability": "CHEM20",
    "security": "CHEM09",
    "privacy": "CHEM09",
    "confidentiality": "CHEM09",
    "integrity": "CHEM09",
    "availability": "CHEM20",
    "authenticity": "CHEM09",
    "accountability": "CHEM20",
    "auditability": "CHEM20",
    "traceability": "CHEM20",
    "compliance": "CHEM10",
    "governance": "CHEM20",
    "risk": "CHEM10",
    "hazard": "CHEM20",
    "threat": "CHEM20",
    "vulnerability": "CHEM20",
    "incident": "CHEM20",
    "event": "CHEM20",
    "alert": "CHEM20",
    "alarm": "CHEM20",
    "notification": "CHEM10",
    "escalation": "CHEM20",
    "response": "CHEM20",
    "recovery": "CHEM20",
    "remediation": "CHEM10",
    "mitigation": "CHEM20",
    "prevention": "CHEM20",
    "protection": "CHEM20",
    "detection": "CHEM02",
    "correction": "CHEM20",
    "compensation": "CHEM20",
    "insurance": "CHEM20",
    "coverage": "CHEM20",
    "liability": "CHEM20",
    "claim": "CHEM20",
    "settlement": "CHEM20",
    "dispute": "CHEM20",
    "litigation": "CHEM20",
    "arbitration": "CHEM20",
    "mediation": "CHEM20",
    "negotiation": "CHEM20",
    "agreement": "CHEM20",
    "contract": "CHEM20",
    "obligation": "CHEM20",
    "commitment": "CHEM20",
    "responsibility": "CHEM20",
    "accountability": "CHEM20",
    "ownership": "CHEM20",
    "stakeholder": "CHEM20",
    "interest": "CHEM20",
    "expectation": "CHEM20",
    "requirement": "CHEM02",
    "need": "CHEM20",
    "demand": "CHEM20",
    "satisfaction": "CHEM20",
    "feedback": "CHEM20",
    "complaint": "CHEM20",
    "suggestion": "CHEM20",
    "recommendation": "CHEM20",
    "improvement": "CHEM20",
    "innovation": "CHEM20",
    "change": "CHEM20",
    "transformation": "CHEM20",
    "transition": "CHEM20",
    "migration": "CHEM20",
    "upgrade": "CHEM20",
    "update": "CHEM20",
    "patch": "CHEM20",
    "fix": "CHEM20",
    "maintenance": "CHEM20",
    "support": "CHEM20",
    "service": "CHEM20",
    "operation": "CHEM20",
    "management": "CHEM20",
    "administration": "CHEM20",
    "coordination": "CHEM20",
    "supervision": "CHEM20",
    "monitoring": "CHEM20",
    "control": "CHEM20",
    "regulation": "CHEM10",
    "policy": "CHEM10",
    "procedure": "CHEM02",
    "protocol": "CHEM02",
    "guideline": "CHEM02",
    "standard": "CHEM02",
    "specification": "CHEM02",
    "requirement": "CHEM02",
    "criteria": "CHEM02",
    "benchmark": "CHEM02",
    "best practice": "CHEM02",
    "lesson learned": "CHEM20",
    "case study": "CHEM20",
    "example": "CHEM20",
    "template": "CHEM20",
    "toolkit": "CHEM20",
    "resource": "CHEM20",
    "reference": "CHEM02",
    "manual": "CHEM20",
    "handbook": "CHEM20",
    "guide": "CHEM20",
    "catalog": "CHEM20",
    "directory": "CHEM20",
    "database": "CHEM09",
    "repository": "CHEM09",
    "archive": "CHEM09",
    "library": "CHEM09",
    "collection": "CHEM09",
    "dataset": "CHEM09",
    "record": "CHEM20",
    "document": "CHEM20",
    "file": "CHEM20",
    "report": "CHEM20",
    "summary": "CHEM20",
    "overview": "CHEM20",
    "review": "CHEM20",
    "assessment": "CHEM10",
    "evaluation": "CHEM10",
    "analysis": "CHEM02",
    "interpretation": "CHEM02",
    "recommendation": "CHEM20",
    "conclusion": "CHEM20",
    "finding": "CHEM20",
    "observation": "CHEM20",
    "comment": "CHEM20",
    "note": "CHEM20",
    "remark": "CHEM20",
    "annotation": "CHEM20",
    "tag": "CHEM20",
    "keyword": "CHEM20",
    "index": "CHEM20",
    "classification": "CHEM20",
    "categorization": "CHEM20",
    "taxonomy": "CHEM20",
    "ontology": "CHEM20",
    "schema": "CHEM09",
    "model": "CHEM09",
    "framework": "CHEM09",
    "architecture": "CHEM09",
    "design": "CHEM09",
    "structure": "CHEM08",
    "system": "CHEM09",
    "platform": "CHEM09",
    "solution": "CHEM09",
    "application": "CHEM09",
    "software": "CHEM09",
    "hardware": "CHEM09",
    "device": "CHEM02",
    "instrument": "CHEM02",
    "equipment": "CHEM20",
    "machine": "CHEM20",
    "apparatus": "CHEM20",
    "tool": "CHEM02",
    "component": "CHEM20",
    "part": "CHEM20",
    "module": "CHEM09",
    "unit": "CHEM20",
    "assembly": "CHEM20",
    "subsystem": "CHEM09",
    "integration": "CHEM09",
    "interface": "CHEM15",
    # ... (total 2000+ rules, truncated for brevity)
}

# Metrics Collector
class MetricsCollector:
    def __init__(self):
        self.query_log = collections.deque()
        self.error_log = collections.deque()
        self.latency_log = collections.deque()
        self.lock = asyncio.Lock()

    async def record_query(self, query_id: str, latency_ms: int):
        now = datetime.utcnow()
        async with self.lock:
            self.query_log.append((now, query_id, latency_ms))
            self.latency_log.append(latency_ms)
            # Remove old entries
            cutoff = now - timedelta(hours=1)
            while self.query_log and self.query_log[0][0] < cutoff:
                self.query_log.popleft()
            while self.latency_log and len(self.latency_log) > 10000:
                self.latency_log.popleft()

    async def record_error(self, query_id: str, error: str):
        now = datetime.utcnow()
        async with self.lock:
            self.error_log.append((now, query_id, error))
            cutoff = now - timedelta(hours=1)
            while self.error_log and self.error_log[0][0] < cutoff:
                self.error_log.popleft()

    async def get_latency_stats(self) -> Dict[str, Any]:
        async with self.lock:
            if not self.latency_log:
                return {"count": 0, "mean": None, "stdev": None, "min": None, "max": None}
            data = list(self.latency_log)
            return {
                "count": len(data),
                "mean": statistics.mean(data),
                "stdev": statistics.stdev(data) if len(data) > 1 else 0.0,
                "min": min(data),
                "max": max(data)
            }

    async def queries_last_hour(self) -> int:
        now = datetime.utcnow()
        cutoff = now - timedelta(hours=1)
        async with self.lock:
            return sum(1 for t, _, _ in self.query_log if t >= cutoff)

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
        topic="Organic Synthesis Retrosynthetic Analysis",
        keywords=["retrosynthesis", "disconnection", "functional group interconversion", "synthesis planning", "strategic bond formation", "protecting groups", "reagents selection"],
        conclusion_template=(
            "Retrosynthetic analysis enables systematic deconstruction of target molecules into simpler precursors, "
            "facilitating efficient synthetic route design. By identifying key disconnections and functional group "
            "transformations, chemists can optimize synthesis pathways with improved yield and selectivity."
        ),
        reasoning_framework=(
            "Retrosynthetic analysis is a fundamental methodology in organic synthesis that involves breaking down a complex "
            "target molecule into simpler, readily available starting materials through a series of logical disconnections. "
            "The process relies on identifying strategic bonds whose cleavage simplifies the molecular architecture while "
            "preserving synthetic feasibility. Functional group interconversions (FGIs) are employed to transform functional "
            "groups into more reactive or compatible moieties, enabling subsequent bond formations. Protecting groups are "
            "utilized to mask reactive sites, preventing undesired side reactions during multi-step syntheses. The selection "
            "of reagents and conditions is guided by chemoselectivity, regioselectivity, and stereoselectivity principles. "
            "The approach is iterative, often requiring evaluation of alternative disconnections and synthetic equivalents "
            "to optimize route efficiency, minimize steps, and reduce cost and waste. Literature precedent, such as Corey’s "
            "seminal work on retrosynthesis (Corey, 1967), provides foundational strategies. Modern computational tools "
            "augment retrosynthetic planning by predicting feasible pathways and reaction outcomes. The integration of "
            "retrosynthesis with green chemistry principles further enhances sustainability in organic synthesis."
        ),
        key_factors=[
            "Identification of strategic bonds for disconnection",
            "Functional group compatibility and interconversion",
            "Use of protecting groups to control reactivity",
            "Selection of reagents and reaction conditions",
            "Synthetic route efficiency and step economy",
            "Stereochemical considerations",
            "Availability and cost of starting materials"
        ],
        primary_authority=[
            "E. J. Corey, 'The Logic of Chemical Synthesis', Wiley, 1989",
            "Smith, M. B., 'March's Advanced Organic Chemistry', 7th Ed., Wiley, 2013",
            "Nicolaou, K. C., and Sorensen, E. J., 'Classics in Total Synthesis', Wiley-VCH, 1996",
            "Wipke, W. T., and Corey, E. J., 'Computer-Assisted Design of Complex Organic Syntheses', Science, 1969",
            "Green, T. W., and Wuts, P. G. M., 'Protective Groups in Organic Synthesis', Wiley, 1999"
        ],
        burden_holder="Synthetic chemist or process development team",
        adversary_position="Claims that retrosynthetic analysis is too theoretical and impractical for complex molecules",
        counter_arguments=[
            "Retrosynthetic analysis is validated by decades of successful total syntheses",
            "Computational tools enhance practical applicability",
            "Allows systematic identification of synthetic bottlenecks",
            "Facilitates cost-effective and scalable synthesis",
            "Enables incorporation of stereochemical control"
        ],
        resolution_strategy=(
            "Demonstrate retrosynthetic analysis through case studies of complex molecule synthesis, "
            "highlighting practical route optimization and successful scale-up."
        ),
        entity_scope="Organic synthesis laboratories, pharmaceutical process development, academic research",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Corey, E. J. (1967). 'General Methods for the Construction of Complex Molecules'. Pure Appl. Chem."
    ),
    DoctrineBlock(
        topic="Chromatography Method Validation in Analytical Chemistry",
        keywords=["chromatography", "HPLC", "GC-MS", "LC-MS", "method validation", "ICH guidelines", "accuracy", "precision", "limit of detection"],
        conclusion_template=(
            "Chromatographic methods must be rigorously validated according to ICH guidelines to ensure accuracy, precision, "
            "specificity, and robustness, thereby guaranteeing reliable analytical results for quality control and regulatory compliance."
        ),
        reasoning_framework=(
            "Chromatography is a cornerstone analytical technique in chemistry, employed for separation, identification, and quantification "
            "of analytes in complex mixtures. Method validation is essential to establish the reliability and reproducibility of chromatographic "
            "methods such as High-Performance Liquid Chromatography (HPLC), Gas Chromatography-Mass Spectrometry (GC-MS), and Liquid Chromatography-Mass Spectrometry (LC-MS). "
            "The International Council for Harmonisation (ICH) Q2(R1) guidelines provide a comprehensive framework for method validation, "
            "covering parameters including specificity, linearity, accuracy, precision (repeatability and intermediate precision), detection and quantitation limits, "
            "range, and robustness. Specificity ensures the method distinguishes analytes from impurities and matrix components. Linearity confirms proportional response "
            "over a defined concentration range. Accuracy and precision validate the method's correctness and reproducibility. Robustness assesses method resilience to "
            "small variations in parameters. Validation requires rigorous experimental design, statistical analysis, and documentation. Failure to validate methods "
            "can lead to erroneous data, regulatory non-compliance, and compromised product quality. Regulatory agencies such as FDA and EMA mandate adherence to these standards."
        ),
        key_factors=[
            "Specificity and selectivity of the chromatographic method",
            "Linearity over the analytical range",
            "Accuracy and recovery studies",
            "Precision including repeatability and intermediate precision",
            "Limits of detection and quantitation",
            "Robustness under variable conditions",
            "System suitability testing"
        ],
        primary_authority=[
            "ICH Q2(R1) Validation of Analytical Procedures: Text and Methodology, 2005",
            "FDA Guidance for Industry: Analytical Procedures and Methods Validation, 2015",
            "Snyder, L. R., Kirkland, J. J., and Dolan, J. W., 'Introduction to Modern Liquid Chromatography', Wiley, 2011",
            "Gross, M. L., 'Mass Spectrometry: A Textbook', Springer, 2011",
            "Poole, C. F., 'Gas Chromatography', Elsevier, 2012"
        ],
        burden_holder="Analytical chemist or quality control laboratory",
        adversary_position="Claims that method validation is overly burdensome and delays product release",
        counter_arguments=[
            "Validated methods ensure data integrity and regulatory compliance",
            "Prevents costly product recalls and investigations",
            "Improves confidence in analytical results",
            "Facilitates method transfer and reproducibility",
            "Supports robust quality control systems"
        ],
        resolution_strategy=(
            "Implement streamlined validation protocols aligned with ICH guidelines and leverage automation to reduce timelines "
            "while maintaining rigorous standards."
        ),
        entity_scope="Pharmaceutical quality control, environmental analysis, food safety laboratories",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ICH Q2(R1), FDA Analytical Procedures Guidance"
    ),
    DoctrineBlock(
        topic="Polymer Chain Growth and Step Growth Polymerization",
        keywords=["polymerization", "chain growth", "step growth", "copolymerization", "molecular weight", "degree of polymerization", "polydispersity", "kinetics"],
        conclusion_template=(
            "Understanding the mechanisms of chain growth and step growth polymerization is critical for controlling polymer molecular weight, structure, "
            "and properties, enabling tailored material design for specific applications."
        ),
        reasoning_framework=(
            "Polymerization mechanisms fundamentally influence polymer architecture and properties. Chain growth polymerization involves the successive addition "
            "of monomer units to an active center, typically a radical, cation, or anion. This process is characterized by rapid chain propagation and termination steps. "
            "Molecular weight distribution is influenced by initiation and termination kinetics, often resulting in narrow polydispersity indices (PDI). "
            "Step growth polymerization proceeds via reactions between functional groups of monomers, oligomers, or polymers, without active centers. "
            "Polymer chains grow by stepwise coupling, often requiring high conversion to achieve high molecular weights. PDIs tend to be broader due to random coupling. "
            "Copolymerization introduces multiple monomer types, affecting sequence distribution and properties. Control over molecular weight and distribution is achieved "
            "through reaction conditions, monomer ratios, and catalysts. Techniques such as Gel Permeation Chromatography (GPC) quantify molecular weight and PDI. "
            "Kinetic models describe polymer growth rates and molecular weight evolution, essential for process optimization. Understanding these mechanisms enables "
            "design of polymers with desired mechanical, thermal, and chemical properties."
        ),
        key_factors=[
            "Polymerization mechanism (chain vs step growth)",
            "Monomer reactivity and functionality",
            "Initiation and termination kinetics",
            "Molecular weight and polydispersity",
            "Copolymer composition and sequence distribution",
            "Reaction conditions (temperature, solvent, catalysts)",
            "Analytical characterization methods"
        ],
        primary_authority=[
            "Odian, G., 'Principles of Polymerization', 4th Ed., Wiley, 2004",
            "Flory, P. J., 'Principles of Polymer Chemistry', Cornell University Press, 1953",
            "Billmeyer, F. W., 'Textbook of Polymer Science', Wiley, 1984",
            "Matyjaszewski, K., 'Atom Transfer Radical Polymerization', Chem. Rev., 2001",
            "Carraher, C. E., 'Introduction to Polymer Chemistry', CRC Press, 2013"
        ],
        burden_holder="Polymer chemist or materials scientist",
        adversary_position="Claims that polymerization mechanisms are too complex for practical control",
        counter_arguments=[
            "Mechanistic understanding enables reproducible polymer synthesis",
            "Kinetic models allow prediction and tuning of polymer properties",
            "Analytical techniques provide feedback for process control",
            "Controlled polymerization methods have revolutionized materials design",
            "Empirical data supports mechanistic theories"
        ],
        resolution_strategy=(
            "Integrate mechanistic studies with analytical characterization and process control to optimize polymer synthesis."
        ),
        entity_scope="Polymer manufacturing, materials research, industrial chemistry",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Flory, P. J. (1953). Principles of Polymer Chemistry."
    ),
    DoctrineBlock(
        topic="Electrochemistry: Nernst Equation and Cyclic Voltammetry",
        keywords=["electrochemistry", "Nernst equation", "cyclic voltammetry", "redox potential", "galvanic cell", "electrolytic cell", "electron transfer", "electrode kinetics"],
        conclusion_template=(
            "The Nernst equation quantitatively relates electrode potential to ion concentrations, while cyclic voltammetry provides dynamic insights into redox processes and electron transfer kinetics."
        ),
        reasoning_framework=(
            "Electrochemistry studies the interplay between electrical energy and chemical change, central to energy storage, sensors, and corrosion science. "
            "The Nernst equation defines the equilibrium potential (E) of an electrode reaction as a function of standard potential (E°), temperature, number of electrons transferred (n), "
            "and activities or concentrations of reactants and products: E = E° - (RT/nF)lnQ, where Q is the reaction quotient. This relationship enables prediction of cell potential under non-standard conditions. "
            "Cyclic voltammetry (CV) is a potent electroanalytical technique where the electrode potential is swept linearly with time, cycling between set limits. "
            "The resulting current-potential curves reveal redox potentials, reaction reversibility, and electron transfer kinetics. Peak currents and potentials inform on diffusion coefficients and reaction mechanisms. "
            "Galvanic cells generate electrical energy spontaneously via redox reactions, while electrolytic cells consume electrical energy to drive non-spontaneous reactions. "
            "Electrode kinetics, including charge transfer resistance and double-layer capacitance, influence electrochemical response. "
            "Understanding these principles is vital for designing batteries, fuel cells, electroplating, and sensors."
        ),
        key_factors=[
            "Standard electrode potentials and redox couples",
            "Ion concentration and activity coefficients",
            "Temperature dependence of electrode potential",
            "Scan rate effects in cyclic voltammetry",
            "Reversibility and kinetics of electron transfer",
            "Diffusion and mass transport phenomena",
            "Electrode surface characteristics"
        ],
        primary_authority=[
            "Bard, A. J., and Faulkner, L. R., 'Electrochemical Methods: Fundamentals and Applications', Wiley, 2000",
            "Atkins, P., and de Paula, J., 'Physical Chemistry', 10th Ed., Oxford University Press, 2014",
            "Koryta, J., et al., 'Electrochemical Methods', Wiley, 1993",
            "Compton, R. G., and Banks, C. E., 'Understanding Voltammetry', Imperial College Press, 2011",
            "Schmickler, W., and Santos, E., 'Interfacial Electrochemistry', Springer, 2010"
        ],
        burden_holder="Electrochemist or analytical chemist",
        adversary_position="Argues that electrochemical data are too complex and ambiguous for practical application",
        counter_arguments=[
            "Standardized techniques and equations provide reproducible data",
            "CV allows mechanistic elucidation of redox processes",
            "Nernst equation is fundamental and universally applicable",
            "Electrochemical methods are widely used in industry and research",
            "Advanced instrumentation improves data quality and interpretation"
        ],
        resolution_strategy=(
            "Provide training on electrochemical theory and instrumentation, supported by case studies demonstrating practical applications."
        ),
        entity_scope="Energy storage, sensors, corrosion, electroplating industries",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Bard, A. J., and Faulkner, L. R. (2000). Electrochemical Methods."
    ),
    DoctrineBlock(
        topic="Thermodynamics: Enthalpy, Entropy, and Gibbs Free Energy",
        keywords=["thermodynamics", "enthalpy", "entropy", "Gibbs free energy", "equilibrium", "spontaneity", "heat capacity", "phase transitions"],
        conclusion_template=(
            "Thermodynamic parameters such as enthalpy, entropy, and Gibbs free energy govern chemical equilibria and reaction spontaneity, enabling prediction and control of chemical processes."
        ),
        reasoning_framework=(
            "Thermodynamics provides the framework to understand energy changes and equilibria in chemical systems. Enthalpy (H) represents the heat content at constant pressure, reflecting bond energies and phase changes. "
            "Entropy (S) quantifies system disorder or the number of accessible microstates, influencing the directionality of processes. Gibbs free energy (G), defined as G = H - TS, combines enthalpy and entropy to predict reaction spontaneity at constant temperature and pressure. "
            "A negative ΔG indicates a spontaneous process, while ΔG = 0 defines equilibrium. Thermodynamic data are obtained experimentally via calorimetry, vapor pressure measurements, and equilibrium constants. "
            "Heat capacity (Cp) describes the temperature dependence of enthalpy and entropy. Phase transitions involve characteristic enthalpy and entropy changes, governed by thermodynamic principles. "
            "The Van't Hoff equation relates equilibrium constants to temperature, enabling prediction of reaction behavior under varying conditions. "
            "Thermodynamics does not provide kinetic information but sets the limits within which reactions occur. "
            "Accurate thermodynamic data underpin chemical engineering, materials science, and biochemical pathway analysis."
        ),
        key_factors=[
            "Standard enthalpy and entropy values",
            "Temperature and pressure conditions",
            "Reaction quotient and equilibrium constant",
            "Heat capacity and phase behavior",
            "Effect of solvents and mixtures",
            "Calorimetric measurement accuracy",
            "Thermodynamic consistency of data"
        ],
        primary_authority=[
            "Atkins, P., and de Paula, J., 'Physical Chemistry', 10th Ed., Oxford University Press, 2014",
            "Laidler, K. J., Meiser, J. H., and Sanctuary, B. C., 'Physical Chemistry', 4th Ed., Houghton Mifflin, 1999",
            "Smith, J. M., Van Ness, H. C., and Abbott, M. M., 'Introduction to Chemical Engineering Thermodynamics', 7th Ed., McGraw-Hill, 2005",
            "Callen, H. B., 'Thermodynamics and an Introduction to Thermostatistics', 2nd Ed., Wiley, 1985",
            "IUPAC, 'Compendium of Chemical Terminology', 2nd Ed. (the 'Gold Book'), 1997"
        ],
        burden_holder="Chemical engineer or physical chemist",
        adversary_position="Claims thermodynamic predictions are unreliable due to experimental variability",
        counter_arguments=[
            "Thermodynamic principles are universally validated",
            "Standardized methods improve data reliability",
            "Thermodynamics provides essential equilibrium constraints",
            "Data reproducibility is ensured by rigorous protocols",
            "Thermodynamics complements kinetic studies"
        ],
        resolution_strategy=(
            "Employ standardized experimental techniques and cross-validate thermodynamic data with computational methods."
        ),
        entity_scope="Chemical process design, materials development, biochemical systems",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Atkins, P., and de Paula, J. (2014). Physical Chemistry."
    ),
    DoctrineBlock(
        topic="Chemical Kinetics: Rate Laws and Arrhenius Equation",
        keywords=["chemical kinetics", "rate law", "reaction order", "Arrhenius equation", "activation energy", "transition state theory", "rate constant", "temperature dependence"],
        conclusion_template=(
            "Chemical kinetics elucidates reaction rates and mechanisms through rate laws and temperature dependence modeled by the Arrhenius equation, facilitating reaction optimization."
        ),
        reasoning_framework=(
            "Chemical kinetics studies the speed of chemical reactions and the factors influencing them. The rate law expresses the reaction rate as a function of reactant concentrations raised to powers corresponding to reaction orders, which are experimentally determined. "
            "The rate constant (k) encapsulates the intrinsic speed of the reaction under given conditions. The Arrhenius equation, k = A exp(-Ea/RT), relates the rate constant to temperature (T), activation energy (Ea), and frequency factor (A), providing insight into the energy barrier of the reaction. "
            "Transition state theory further refines the understanding of reaction rates by considering the activated complex and its energy relative to reactants. "
            "Kinetic experiments involve monitoring concentration changes over time using spectroscopic or chromatographic methods. "
            "Data analysis includes plotting ln(k) versus 1/T to extract Ea and A. Reaction mechanisms are proposed based on kinetic orders and intermediates. "
            "Kinetics informs reactor design, catalyst development, and safety assessments by predicting reaction behavior under varying conditions."
        ),
        key_factors=[
            "Reaction order and molecularity",
            "Rate constant and its temperature dependence",
            "Activation energy and frequency factor",
            "Experimental determination of rate laws",
            "Transition state and reaction coordinate",
            "Catalyst effects on kinetics",
            "Influence of solvent and pressure"
        ],
        primary_authority=[
            "Laidler, K. J., 'Chemical Kinetics', 3rd Ed., Harper & Row, 1987",
            "Espenson, J. H., 'Chemical Kinetics and Reaction Mechanisms', McGraw-Hill, 1995",
            "Steinfeld, J. I., Francisco, J. S., and Hase, W. L., 'Chemical Kinetics and Dynamics', 2nd Ed., Prentice Hall, 1999",
            "Fersht, A., 'Structure and Mechanism in Protein Science', W. H. Freeman, 1999",
            "IUPAC, 'Compendium of Chemical Terminology', 2nd Ed. (the 'Gold Book'), 1997"
        ],
        burden_holder="Kineticist or reaction engineer",
        adversary_position="Argues that kinetic models oversimplify complex reaction networks",
        counter_arguments=[
            "Kinetic models are validated by experimental data",
            "Mechanistic insights guide model refinement",
            "Models predict reaction behavior under diverse conditions",
            "Complex networks can be decomposed into elementary steps",
            "Computational methods complement experimental kinetics"
        ],
        resolution_strategy=(
            "Combine experimental kinetics with computational modeling to iteratively improve mechanistic understanding."
        ),
        entity_scope="Chemical manufacturing, catalysis, environmental chemistry",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Laidler, K. J. (1987). Chemical Kinetics."
    ),
    DoctrineBlock(
        topic="Spectroscopy: NMR, IR, UV-Vis, and Mass Spectrometry Interpretation",
        keywords=["spectroscopy", "NMR", "infrared", "UV-Vis", "mass spectrometry", "chemical shifts", "vibrational modes", "chromophores", "fragmentation patterns"],
        conclusion_template=(
            "Spectroscopic techniques provide complementary structural and compositional information essential for molecular identification and characterization."
        ),
        reasoning_framework=(
            "Spectroscopy encompasses a range of techniques exploiting interaction of electromagnetic radiation with matter to elucidate molecular structure and composition. "
            "Nuclear Magnetic Resonance (NMR) spectroscopy probes nuclear spin environments, yielding chemical shifts, coupling constants, and integration data that reveal molecular connectivity and stereochemistry. "
            "Infrared (IR) spectroscopy detects vibrational transitions of molecular bonds, identifying functional groups via characteristic absorption bands. "
            "Ultraviolet-Visible (UV-Vis) spectroscopy measures electronic transitions, useful for studying conjugated systems and chromophores. "
            "Mass spectrometry (MS) ionizes molecules and analyzes mass-to-charge ratios, providing molecular weight and fragmentation patterns that assist in structural elucidation. "
            "Interpretation requires understanding of selection rules, instrumental parameters, and sample preparation. "
            "Combining data from multiple spectroscopic methods enhances confidence in molecular assignments. "
            "Advances such as 2D NMR, FTIR, and high-resolution MS have expanded analytical capabilities. "
            "Expertise in spectral interpretation is critical for organic synthesis, natural product chemistry, and quality control."
        ),
        key_factors=[
            "Chemical shift and coupling patterns in NMR",
            "Characteristic IR absorption frequencies",
            "UV-Vis absorption maxima and molar absorptivity",
            "Mass spectral fragmentation and isotopic patterns",
            "Sample purity and preparation",
            "Instrument calibration and resolution",
            "Complementarity of spectroscopic data"
        ],
        primary_authority=[
            "Silverstein, R. M., Webster, F. X., and Kiemle, D. J., 'Spectrometric Identification of Organic Compounds', 7th Ed., Wiley, 2005",
            "Pavia, D. L., Lampman, G. M., and Kriz, G. S., 'Introduction to Spectroscopy', 4th Ed., Cengage Learning, 2008",
            "Claridge, T. D. W., 'High-Resolution NMR Techniques in Organic Chemistry', 3rd Ed., Elsevier, 2016",
            "Gross, M. L., 'Mass Spectrometry: A Textbook', Springer, 2011",
            "Smith, E., and Dent, G., 'Modern Raman Spectroscopy', Wiley, 2005"
        ],
        burden_holder="Analytical chemist or spectroscopist",
        adversary_position="Claims spectral data are ambiguous and prone to misinterpretation",
        counter_arguments=[
            "Standardized protocols and databases improve reliability",
            "Multimodal spectroscopy reduces ambiguity",
            "Experienced interpretation minimizes errors",
            "Instrumental advances enhance spectral resolution",
            "Spectral simulation and computational methods assist assignments"
        ],
        resolution_strategy=(
            "Train analysts in spectral interpretation and utilize complementary techniques for robust molecular characterization."
        ),
        entity_scope="Pharmaceutical analysis, natural products, materials characterization",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Silverstein, R. M. et al. (2005). Spectrometric Identification of Organic Compounds."
    ),
    DoctrineBlock(
        topic="X-ray Crystallography: Bragg Diffraction and Unit Cell Analysis",
        keywords=["X-ray crystallography", "Bragg diffraction", "unit cell", "space group", "electron density", "crystal lattice", "structure determination", "reciprocal space"],
        conclusion_template=(
            "X-ray crystallography enables precise determination of molecular and crystal structures through analysis of diffraction patterns and unit cell parameters."
        ),
        reasoning_framework=(
            "X-ray crystallography is the definitive technique for elucidating three-dimensional molecular and crystal structures. "
            "When X-rays interact with a crystalline material, constructive interference occurs at specific angles satisfying Bragg's law: nλ = 2d sinθ, where λ is wavelength, d is interplanar spacing, and θ is diffraction angle. "
            "Diffraction patterns are collected and analyzed to determine the unit cell dimensions and symmetry, described by space groups. "
            "Electron density maps are computed via Fourier transforms of diffraction data, revealing atomic positions. "
            "Refinement procedures minimize differences between observed and calculated patterns, improving structural accuracy. "
            "Reciprocal space concepts facilitate interpretation of diffraction data. "
            "Crystallographic data provide insights into molecular conformation, packing, intermolecular interactions, and disorder. "
            "Limitations include need for high-quality crystals and potential for twinning or disorder complicating analysis. "
            "Advances in synchrotron sources and detectors have enhanced resolution and speed."
        ),
        key_factors=[
            "Crystal quality and purity",
            "Accurate measurement of diffraction intensities",
            "Unit cell parameter determination",
            "Space group assignment",
            "Electron density map interpretation",
            "Refinement statistics (R-factors)",
            "Data completeness and resolution"
        ],
        primary_authority=[
            "Girolami, G. S., Rauchfuss, T. B., and Angelici, R. J., 'Synthesis and Technique in Inorganic Chemistry', University Science Books, 1999",
            "Cullity, B. D., and Stock, S. R., 'Elements of X-Ray Diffraction', 3rd Ed., Prentice Hall, 2001",
            "Glusker, J. P., Lewis, M., and Rossi, M., 'Crystal Structure Analysis for Chemists and Biologists', Wiley, 1994",
            "International Tables for Crystallography, Vol. A, 'Space-group symmetry', Wiley, 2006",
            "Drenth, J., 'Principles of Protein X-ray Crystallography', 3rd Ed., Springer, 2007"
        ],
        burden_holder="Crystallographer or structural chemist",
        adversary_position="Claims crystallography is limited by crystal growth challenges and data interpretation complexity",
        counter_arguments=[
            "Crystallography remains the gold standard for structure determination",
            "Techniques for crystal growth and data collection have advanced",
            "Computational tools assist in data processing and interpretation",
            "Complementary methods validate crystallographic models",
            "Extensive databases support structure verification"
        ],
        resolution_strategy=(
            "Invest in crystal growth optimization and training in crystallographic software to overcome challenges."
        ),
        entity_scope="Structural chemistry, materials science, pharmaceutical development",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Cullity, B. D., and Stock, S. R. (2001). Elements of X-Ray Diffraction."
    ),
    DoctrineBlock(
        topic="Computational Chemistry: Density Functional Theory and Molecular Dynamics",
        keywords=["computational chemistry", "density functional theory", "molecular dynamics", "force fields", "ab initio", "potential energy surface", "quantum chemistry", "simulation"],
        conclusion_template=(
            "Computational chemistry methods such as DFT and molecular dynamics provide atomistic insights into molecular structure, energetics, and dynamics, complementing experimental data."
        ),
        reasoning_framework=(
            "Computational chemistry employs theoretical models and numerical methods to simulate chemical systems. Density Functional Theory (DFT) approximates electronic structure by modeling electron density, balancing accuracy and computational cost. "
            "DFT is widely used for geometry optimization, energy calculations, and reaction mechanism studies. Molecular dynamics (MD) simulates atomic motions over time using classical force fields, capturing conformational changes, diffusion, and thermodynamic properties. "
            "Force fields parameterize bonded and non-bonded interactions, enabling simulations of large biomolecules and materials. "
            "Ab initio methods, including Hartree-Fock and post-Hartree-Fock techniques, provide high-accuracy quantum mechanical calculations but are computationally intensive. "
            "Potential energy surfaces derived from these methods guide understanding of reaction pathways and transition states. "
            "Integration of computational and experimental approaches enhances interpretation and prediction of chemical phenomena. "
            "Limitations include approximations inherent in models and computational resource demands. "
            "Continuous development of algorithms and hardware expands applicability."
        ),
        key_factors=[
            "Choice of computational method and basis set",
            "Accuracy of force field parameters",
            "System size and simulation timescale",
            "Treatment of solvent and environment",
            "Validation against experimental data",
            "Computational resource availability",
            "Interpretation of simulation results"
        ],
        primary_authority=[
            "Jensen, F., 'Introduction to Computational Chemistry', 3rd Ed., Wiley, 2017",
            "Leach, A. R., 'Molecular Modelling: Principles and Applications', 2nd Ed., Pearson, 2001",
            "Cramer, C. J., 'Essentials of Computational Chemistry', 2nd Ed., Wiley, 2004",
            "Frenkel, D., and Smit, B., 'Understanding Molecular Simulation', 2nd Ed., Academic Press, 2002",
            "Szabo, A., and Ostlund, N. S., 'Modern Quantum Chemistry', Dover Publications, 1996"
        ],
        burden_holder="Computational chemist or theoretical chemist",
        adversary_position="Claims computational results lack experimental validation and are unreliable",
        counter_arguments=[
            "Computational methods are benchmarked against experimental data",
            "Simulations provide mechanistic insights inaccessible experimentally",
            "Method development improves accuracy continuously",
            "Hybrid quantum/classical methods enhance realism",
            "Computational predictions guide experimental design"
        ],
        resolution_strategy=(
            "Employ rigorous validation and iterative feedback between computation and experiment."
        ),
        entity_scope="Drug design, materials science, catalysis research",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Jensen, F. (2017). Introduction to Computational Chemistry."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry: Fate, Transport, and Remediation of Contaminants",
        keywords=["environmental chemistry", "contaminant fate", "transport mechanisms", "remediation technologies", "biodegradation", "adsorption", "chemical transformation", "risk assessment"],
        conclusion_template=(
            "Understanding contaminant fate and transport mechanisms is essential for designing effective remediation strategies and mitigating environmental impact."
        ),
        reasoning_framework=(
            "Environmental chemistry focuses on the behavior and effects of chemical species in natural environments. Contaminant fate involves physical, chemical, and biological processes that alter chemical form and concentration. "
            "Transport mechanisms include advection, diffusion, dispersion, and sorption to soils and sediments. Chemical transformations such as hydrolysis, photolysis, and redox reactions modify contaminant toxicity and mobility. "
            "Biodegradation by microorganisms plays a critical role in natural attenuation and engineered bioremediation. "
            "Remediation technologies encompass physical removal, chemical oxidation/reduction, adsorption, and biological treatments. "
            "Site-specific factors such as soil composition, hydrology, and climate influence contaminant behavior. "
            "Risk assessment integrates exposure pathways and toxicological data to evaluate human and ecological risks. "
            "Regulatory frameworks like the US EPA Superfund program guide remediation efforts. "
            "Analytical monitoring and modeling support decision-making and effectiveness evaluation."
        ),
        key_factors=[
            "Chemical properties of contaminants",
            "Environmental media characteristics",
            "Transport and transformation rates",
            "Microbial community and biodegradation potential",
            "Remediation technology suitability",
            "Regulatory standards and guidelines",
            "Monitoring and modeling accuracy"
        ],
        primary_authority=[
            "Mackay, D., and Shiu, W. Y., 'Handbook of Physical-Chemical Properties and Environmental Fate for Organic Chemicals', CRC Press, 1981",
            "Manahan, S. E., 'Environmental Chemistry', 9th Ed., CRC Press, 2017",
            "US EPA, 'Risk Assessment Guidance for Superfund', 1989",
            "Schnoor, J. L., 'Environmental Modeling: Fate and Transport of Pollutants in Water, Air, and Soil', Wiley, 1996",
            "Alexander, M., 'Biodegradation and Bioremediation', Academic Press, 1999"
        ],
        burden_holder="Environmental chemist or remediation engineer",
        adversary_position="Contends that remediation technologies are ineffective or economically unfeasible",
        counter_arguments=[
            "Remediation technologies are selected based on site-specific assessments",
            "Combination of methods enhances effectiveness",
            "Economic analyses include long-term environmental benefits",
            "Regulatory incentives support remediation efforts",
            "Continuous technology development improves cost-effectiveness"
        ],
        resolution_strategy=(
            "Conduct comprehensive site assessments and pilot studies to tailor remediation approaches."
        ),
        entity_scope="Environmental consulting, regulatory agencies, industrial waste management",
        confidence=0.90,
        confidence_zone="Moderate to High",
        controlling_precedent="US EPA Risk Assessment Guidance for Superfund, 1989"
    ),
    DoctrineBlock(
        topic="Coordination Chemistry: Ligand Field Theory and Crystal Field Splitting",
        keywords=["coordination chemistry", "ligand field theory", "crystal field splitting", "d-orbitals", "spectrochemical series", "octahedral complexes", "electronic transitions", "magnetic properties"],
        conclusion_template=(
            "Ligand field theory explains the electronic structure and properties of coordination complexes through crystal field splitting of d-orbitals influenced by ligand environment."
        ),
        reasoning_framework=(
            "Coordination chemistry studies complexes formed between metal centers and ligands. Ligand Field Theory (LFT) extends Crystal Field Theory (CFT) by incorporating covalent interactions to explain electronic structures. "
            "In an octahedral field, the degeneracy of metal d-orbitals splits into t2g and eg sets due to electrostatic interactions with ligands. The magnitude of splitting (Δoct) depends on ligand identity, described by the spectrochemical series. "
            "This splitting influences electronic transitions observed in UV-Vis spectra, magnetic properties, and reactivity. "
            "High-spin and low-spin configurations arise from the balance between crystal field splitting and electron pairing energy. "
            "LFT accounts for π-backbonding and covalency effects, refining predictions of complex stability and spectra. "
            "Understanding these principles is critical for catalyst design, bioinorganic chemistry, and materials science. "
            "Magnetic susceptibility measurements and electronic absorption spectroscopy provide experimental validation."
        ),
        key_factors=[
            "Metal oxidation state and d-electron count",
            "Ligand field strength and geometry",
            "Crystal field splitting energy (Δoct, Δtet)",
            "Electron pairing energy",
            "Spectrochemical series ranking",
            "Electronic transitions and selection rules",
            "Magnetic behavior (paramagnetism vs diamagnetism)"
        ],
        primary_authority=[
            "Miessler, G. L., Fischer, P. J., and Tarr, D. A., 'Inorganic Chemistry', 5th Ed., Pearson, 2013",
            "Cotton, F. A., and Wilkinson, G., 'Advanced Inorganic Chemistry', 6th Ed., Wiley, 1999",
            "Lever, A. B. P., 'Inorganic Electronic Spectroscopy', 2nd Ed., Elsevier, 1984",
            "Ballhausen, C. J., 'Introduction to Ligand Field Theory', McGraw-Hill, 1962",
            "Figgis, B. N., and Hitchman, M. A., 'Ligand Field Theory and Its Applications', Wiley-VCH, 2000"
        ],
        burden_holder="Inorganic chemist or spectroscopist",
        adversary_position="Claims ligand field theory oversimplifies complex bonding in coordination compounds",
        counter_arguments=[
            "LFT provides predictive power for electronic and magnetic properties",
            "Combines with molecular orbital theory for comprehensive understanding",
            "Supported by extensive spectroscopic and magnetic data",
            "Useful for rational catalyst and material design",
            "Continually refined with computational chemistry"
        ],
        resolution_strategy=(
            "Integrate LFT with advanced computational methods and experimental techniques for detailed analysis."
        ),
        entity_scope="Inorganic synthesis, catalysis, bioinorganic chemistry",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Miessler, G. L. et al. (2013). Inorganic Chemistry."
    ),
    DoctrineBlock(
        topic="Biochemistry: Enzyme Kinetics and Michaelis-Menten Model",
        keywords=["enzyme kinetics", "Michaelis-Menten", "substrate concentration", "Vmax", "Km", "catalysis", "inhibition", "reaction velocity"],
        conclusion_template=(
            "The Michaelis-Menten model quantitatively describes enzyme-catalyzed reaction rates, enabling determination of kinetic parameters critical for understanding enzyme function."
        ),
        reasoning_framework=(
            "Enzyme kinetics investigates the rates of biochemical reactions catalyzed by enzymes. The Michaelis-Menten model describes the relationship between reaction velocity (v) and substrate concentration ([S]) through the equation: v = (Vmax [S])/(Km + [S]), where Vmax is the maximum velocity and Km is the Michaelis constant. "
            "Km reflects the substrate concentration at half Vmax, indicating enzyme affinity for substrate. "
            "The model assumes formation of an enzyme-substrate complex (ES) in rapid equilibrium, followed by rate-limiting product formation. "
            "Kinetic parameters are determined experimentally via initial rate measurements at varying substrate concentrations and analyzed using Lineweaver-Burk or Eadie-Hofstee plots. "
            "Enzyme inhibitors affect kinetics by altering Vmax and/or Km, classified as competitive, noncompetitive, or uncompetitive. "
            "Understanding enzyme kinetics informs drug design, metabolic regulation, and biotechnology applications. "
            "Limitations include assumptions of steady-state and single-substrate reactions; more complex models address multi-substrate and allosteric enzymes."
        ),
        key_factors=[
            "Substrate concentration and enzyme saturation",
            "Initial reaction velocity measurement",
            "Determination of Vmax and Km",
            "Types and mechanisms of inhibition",
            "Assumptions of steady-state kinetics",
            "Enzyme concentration and purity",
            "Environmental factors (pH, temperature)"
        ],
        primary_authority=[
            "Segel, I. H., 'Enzyme Kinetics: Behavior and Analysis of Rapid Equilibrium and Steady-State Enzyme Systems', Wiley, 1993",
            "Cornish-Bowden, A., 'Fundamentals of Enzyme Kinetics', 4th Ed., Wiley-Blackwell, 2012",
            "Copeland, R. A., 'Enzymes: A Practical Introduction to Structure, Mechanism, and Data Analysis', 2nd Ed., Wiley, 2000",
            "Michaelis, L., and Menten, M. L., 'Die Kinetik der Invertinwirkung', Biochem. Z., 1913",
            "Fersht, A., 'Structure and Mechanism in Protein Science', W. H. Freeman, 1999"
        ],
        burden_holder="Biochemist or enzymologist",
        adversary_position="Asserts Michaelis-Menten kinetics oversimplify complex enzymatic behavior",
        counter_arguments=[
            "Model provides foundational framework for enzyme kinetics",
            "Extensions and modifications address complex systems",
            "Experimental data often fit Michaelis-Menten kinetics well",
            "Useful for comparative and mechanistic studies",
            "Supports rational inhibitor design"
        ],
        resolution_strategy=(
            "Apply Michaelis-Menten as baseline model and incorporate advanced kinetics for complex enzymes."
        ),
        entity_scope="Biotechnology, pharmaceutical development, metabolic engineering",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Michaelis, L., and Menten, M. L. (1913). Biochem. Z."
    ),
    DoctrineBlock(
        topic="Materials Characterization: SEM, TEM, XRD, and Thermal Analysis",
        keywords=["materials characterization", "scanning electron microscopy", "transmission electron microscopy", "X-ray diffraction", "thermal analysis", "microstructure", "phase identification", "thermal stability"],
        conclusion_template=(
            "Comprehensive materials characterization using SEM, TEM, XRD, and thermal analysis provides critical insights into microstructure, phase composition, and thermal properties."
        ),
        reasoning_framework=(
            "Materials characterization employs a suite of analytical techniques to elucidate structural, compositional, and thermal properties. Scanning Electron Microscopy (SEM) provides high-resolution surface imaging by scanning an electron beam and detecting secondary or backscattered electrons, revealing morphology and topography. "
            "Transmission Electron Microscopy (TEM) transmits electrons through thin samples, enabling atomic-scale imaging and diffraction studies. "
            "X-ray Diffraction (XRD) identifies crystalline phases and determines lattice parameters via diffraction patterns analyzed with Bragg's law. "
            "Thermal analysis techniques, including Differential Scanning Calorimetry (DSC) and Thermogravimetric Analysis (TGA), assess thermal transitions, decomposition, and stability. "
            "Integration of these methods enables correlation of microstructure with material properties and performance. "
            "Sample preparation, instrument calibration, and data interpretation require expertise. "
            "Applications span metallurgy, ceramics, polymers, and nanomaterials."
        ),
        key_factors=[
            "Sample preparation and representativeness",
            "Instrument resolution and calibration",
            "Phase identification and quantification",
            "Morphological and microstructural analysis",
            "Thermal transition temperatures and enthalpies",
            "Decomposition temperatures and kinetics",
            "Correlation of structural and thermal data"
        ],
        primary_authority=[
            "Williams, D. B., and Carter, C. B., 'Transmission Electron Microscopy: A Textbook for Materials Science', 2nd Ed., Springer, 2009",
            "Cullity, B. D., and Stock, S. R., 'Elements of X-Ray Diffraction', 3rd Ed., Prentice Hall, 2001",
            "Goldstein, J. I., et al., 'Scanning Electron Microscopy and X-Ray Microanalysis', 3rd Ed., Springer, 2003",
            "Brown, M. E., 'Introduction to Thermal Analysis: Techniques and Applications', Springer, 2001",
            "Callister, W. D., and Rethwisch, D. G., 'Materials Science and Engineering: An Introduction', 9th Ed., Wiley, 2013"
        ],
        burden_holder="Materials scientist or analytical technician",
        adversary_position="Claims characterization techniques are costly and provide redundant information",
        counter_arguments=[
            "Each technique provides unique and complementary information",
            "Characterization guides material design and quality control",
            "Advances have reduced costs and improved accessibility",
            "Data integration enhances understanding of material behavior",
            "Essential for failure analysis and innovation"
        ],
        resolution_strategy=(
            "Develop integrated characterization protocols tailored to material and application requirements."
        ),
        entity_scope="Materials research, manufacturing, quality assurance",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Williams, D. B., and Carter, C. B. (2009). Transmission Electron Microscopy."
    ),
    DoctrineBlock(
        topic="Radioactivity: Decay, Nuclear Fission, Fusion, and Isotope Applications",
        keywords=["radioactivity", "nuclear decay", "fission", "fusion", "radioisotopes", "half-life", "radiation detection", "nuclear medicine"],
        conclusion_template=(
            "Radioactive decay processes underpin nuclear fission and fusion technologies, while radioisotopes have diverse applications in medicine, industry, and research."
        ),
        reasoning_framework=(
            "Radioactivity involves spontaneous nuclear decay emitting alpha, beta, or gamma radiation, characterized by half-life and decay modes. Nuclear fission splits heavy nuclei into lighter fragments, releasing energy harnessed in reactors and weapons. "
            "Nuclear fusion combines light nuclei at high temperatures and pressures, powering stars and pursued for clean energy generation. "
            "Radioisotopes serve as tracers, diagnostic agents, and therapeutic tools in nuclear medicine, as well as in industrial radiography and dating techniques. "
            "Radiation detection employs scintillation counters, Geiger-Müller tubes, and semiconductor detectors. "
            "Safety protocols and regulatory frameworks govern handling and disposal of radioactive materials. "
            "Understanding nuclear processes requires quantum mechanics and nuclear physics principles. "
            "Advances in isotope production and detection expand applications in science and technology."
        ),
        key_factors=[
            "Types and modes of radioactive decay",
            "Half-life and decay kinetics",
            "Energy release in fission and fusion",
            "Production and purification of radioisotopes",
            "Radiation detection and measurement",
            "Applications in medicine and industry",
            "Radiation safety and regulatory compliance"
        ],
        primary_authority=[
            "Krane, K. S., 'Introductory Nuclear Physics', Wiley, 1987",
            "Choppin, G., Liljenzin, J.-O., and Rydberg, J., 'Radiochemistry and Nuclear Chemistry', 3rd Ed., Butterworth-Heinemann, 2002",
            "Knoll, G. F., 'Radiation Detection and Measurement', 4th Ed., Wiley, 2010",
            "Nuclear Regulatory Commission (NRC), 'Radiation Protection Regulations', 10 CFR Part 20",
            "IAEA, 'Radiation Protection and Safety of Radiation Sources', Safety Standards Series No. GSR Part 3, 2014"
        ],
        burden_holder="Nuclear chemist or radiological safety officer",
        adversary_position="Claims nuclear technologies pose unacceptable risks and costs",
        counter_arguments=[
            "Strict safety standards mitigate risks effectively",
            "Nuclear medicine provides life-saving diagnostics and treatments",
            "Fusion research aims for clean energy with minimal waste",
            "Regulatory oversight ensures responsible use",
            "Public education improves acceptance and understanding"
        ],
        resolution_strategy=(
            "Implement comprehensive safety programs and transparent communication to balance benefits and risks."
        ),
        entity_scope="Nuclear energy, medical imaging, radiopharmaceuticals, environmental monitoring",
        confidence=0.91,
        confidence_zone="Moderate to High",
        controlling_precedent="Krane, K. S. (1987). Introductory Nuclear Physics."
    ),
    DoctrineBlock(
        topic="Surface Chemistry: Adsorption, Catalysis, BET and Langmuir Isotherms",
        keywords=["surface chemistry", "adsorption", "catalysis", "BET isotherm", "Langmuir isotherm", "surface area", "heterogeneous catalysis", "adsorption kinetics"],
        conclusion_template=(
            "Surface chemistry principles including adsorption isotherms and catalytic mechanisms are essential for understanding and optimizing heterogeneous catalytic processes."
        ),
        reasoning_framework=(
            "Surface chemistry examines phenomena occurring at interfaces, particularly adsorption of molecules onto solid surfaces. "
            "Adsorption isotherms describe the relationship between adsorbate concentration and surface coverage at constant temperature. "
            "The Langmuir isotherm models monolayer adsorption on homogeneous surfaces with finite sites, assuming no interactions between adsorbed molecules. "
            "The BET (Brunauer-Emmett-Teller) isotherm extends this to multilayer adsorption, enabling determination of specific surface area from gas adsorption data. "
            "Catalysis often involves adsorption of reactants on catalyst surfaces, facilitating bond breaking and formation. "
            "Heterogeneous catalysis depends on surface properties, active sites, and adsorption-desorption kinetics. "
            "Understanding adsorption energetics and kinetics guides catalyst design and process optimization. "
            "Techniques such as temperature-programmed desorption and chemisorption measurements provide experimental data. "
            "Surface characterization complements adsorption studies to elucidate structure-activity relationships."
        ),
        key_factors=[
            "Surface site availability and heterogeneity",
            "Adsorption energy and enthalpy",
            "Monolayer vs multilayer adsorption",
            "Surface area and porosity",
            "Catalyst active site nature",
            "Adsorption and desorption kinetics",
            "Effect of temperature and pressure"
        ],
        primary_authority=[
            "Adamson, A. W., and Gast, A. P., 'Physical Chemistry of Surfaces', 6th Ed., Wiley, 1997",
            "Brunauer, S., Emmett, P. H., and Teller, E., 'Adsorption of Gases in Multimolecular Layers', J. Am. Chem. Soc., 1938",
            "Langmuir, I., 'The Adsorption of Gases on Plane Surfaces of Glass, Mica and Platinum', J. Am. Chem. Soc., 1918",
            "Somorjai, G. A., and Li, Y., 'Introduction to Surface Chemistry and Catalysis', 2nd Ed., Wiley, 2010",
            "Bartholomew, C. H., 'Mechanisms of Catalyst Deactivation', Appl. Catal. A, 2001"
        ],
        burden_holder="Surface chemist or catalyst developer",
        adversary_position="Claims adsorption models are oversimplified and not predictive for real systems",
        counter_arguments=[
            "Models provide useful approximations for many systems",
            "Experimental validation supports model applicability",
            "Extensions and modifications address complexities",
            "Combined with surface characterization for accuracy",
            "Essential for rational catalyst design"
        ],
        resolution_strategy=(
            "Use adsorption models as starting points and refine with empirical data and advanced simulations."
        ),
        entity_scope="Catalysis, materials science, environmental remediation",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Brunauer, S. et al. (1938). J. Am. Chem. Soc."
    ),
    DoctrineBlock(
        topic="Photochemistry: Excited States, Quantum Yield, and Photosensitization",
        keywords=["photochemistry", "excited states", "quantum yield", "photosensitization", "photophysical processes", "fluorescence", "phosphorescence", "energy transfer"],
        conclusion_template=(
            "Photochemical processes involving excited states and photosensitization govern reaction pathways and efficiencies, quantified by quantum yield measurements."
        ),
        reasoning_framework=(
            "Photochemistry studies chemical reactions initiated by absorption of light, promoting molecules to electronically excited states. "
            "Excited states can undergo radiative decay (fluorescence, phosphorescence), non-radiative decay, or participate in chemical transformations. "
            "Quantum yield defines the efficiency of a photochemical process as the ratio of events (e.g., product formation) to photons absorbed. "
            "Photosensitization involves transfer of excitation energy from a sensitizer to a substrate, enabling reactions otherwise inaccessible. "
            "Photophysical processes include intersystem crossing, internal conversion, and energy transfer mechanisms. "
            "Understanding excited state lifetimes, energy levels, and reaction pathways is critical for applications in photodynamic therapy, solar energy conversion, and synthetic photochemistry. "
            "Spectroscopic techniques such as time-resolved fluorescence and transient absorption spectroscopy characterize excited states. "
            "Control of wavelength, intensity, and environment influences photochemical outcomes."
        ),
        key_factors=[
            "Absorption spectra and molar absorptivity",
            "Excited state energy and lifetime",
            "Quantum yield determination",
            "Photosensitizer-substrate interactions",
            "Radiative and non-radiative decay pathways",
            "Environmental effects (solvent, oxygen)",
            "Light source characteristics"
        ],
        primary_authority=[
            "Turro, N. J., Ramamurthy, V., and Scaiano, J. C., 'Principles of Molecular Photochemistry', University Science Books, 2009",
            "Lakowicz, J. R., 'Principles of Fluorescence Spectroscopy', 3rd Ed., Springer, 2006",
            "Crespo-Hernández, C. E., et al., 'Photochemistry of Nucleic Acids', Chem. Rev., 2004",
            "Meyer, T. J., and Huynh, M. H. V., 'Photosensitization and Photocatalysis', Chem. Rev., 2010",
            "Parker, C. A., 'Photoluminescence of Solutions', Elsevier, 1968"
        ],
        burden_holder="Photochemist or materials scientist",
        adversary_position="Asserts photochemical processes are too complex for quantitative control",
        counter_arguments=[
            "Quantum yield and mechanistic studies enable quantitative understanding",
            "Spectroscopic techniques provide detailed excited state information",
            "Photosensitization is exploited in diverse applications",
            "Controlled experimental conditions improve reproducibility",
            "Computational photochemistry aids interpretation"
        ],
        resolution_strategy=(
            "Combine experimental photophysics with theoretical modeling to optimize photochemical systems."
        ),
        entity_scope="Photodynamic therapy, solar energy, synthetic photochemistry",
        confidence=0.90,
        confidence_zone="Moderate to High",
        controlling_precedent="Turro, N. J. et al. (2009). Principles of Molecular Photochemistry."
    ),
    DoctrineBlock(
        topic="Geochemistry: Mineral Weathering, Isotope Geochemistry, and Petrology",
        keywords=["geochemistry", "mineral weathering", "isotope geochemistry", "petrology", "elemental cycling", "radiogenic isotopes", "stable isotopes", "geochemical modeling"],
        conclusion_template=(
            "Geochemical processes including mineral weathering and isotope fractionation provide insights into Earth's composition, history, and environmental changes."
        ),
        reasoning_framework=(
            "Geochemistry applies chemical principles to Earth materials and processes. Mineral weathering alters rock composition through physical and chemical mechanisms, influencing soil formation and nutrient cycling. "
            "Isotope geochemistry utilizes variations in stable and radiogenic isotopes to trace sources, processes, and timescales. Stable isotopes (e.g., C, O, S) fractionate during physical and biological processes, serving as environmental proxies. "
            "Radiogenic isotopes (e.g., U-Pb, Rb-Sr) provide geochronological information. "
            "Petrology studies rock origin, composition, and transformation, integrating geochemical data to interpret geological history. "
            "Geochemical modeling simulates elemental transport, reaction kinetics, and isotope evolution. "
            "Analytical techniques include mass spectrometry, electron microprobe, and spectroscopy. "
            "Understanding these processes informs resource exploration, climate studies, and environmental management."
        ),
        key_factors=[
            "Mineral stability and weathering rates",
            "Isotope fractionation mechanisms",
            "Radiogenic decay systems and half-lives",
            "Elemental mobility and cycling",
            "Analytical precision and accuracy",
            "Geochemical modeling assumptions",
            "Integration with geological context"
        ],
        primary_authority=[
            "Faure, G., and Mensing, T. M., 'Isotopes: Principles and Applications', 3rd Ed., Wiley, 2005",
            "White, W. M., 'Geochemistry', 2nd Ed., Wiley-Blackwell, 2013",
            "Rollinson, H., 'Using Geochemical Data: Evaluation, Presentation, Interpretation', Routledge, 1993",
            "Drever, J. I., 'The Geochemistry of Natural Waters', 3rd Ed., Prentice Hall, 1997",
            "Faure, G., 'Principles of Isotope Geology', 2nd Ed., Wiley, 1986"
        ],
        burden_holder="Geochemist or earth scientist",
        adversary_position="Claims isotope data are too variable and geochemical models oversimplify complex systems",
        counter_arguments=[
            "Isotope systems are well-characterized with known fractionation factors",
            "Models incorporate uncertainties and are validated by observations",
            "Multiple isotope systems provide cross-validation",
            "Analytical advances improve data quality",
            "Geochemical interpretations are integrated with geological evidence"
        ],
        resolution_strategy=(
            "Apply multi-disciplinary approaches combining isotope geochemistry, petrology, and modeling."
        ),
        entity_scope="Earth sciences, environmental studies, resource exploration",
        confidence=0.89,
        confidence_zone="Moderate to High",
        controlling_precedent="Faure, G., and Mensing, T. M. (2005). Isotopes: Principles and Applications."
    ),
    DoctrineBlock(
        topic="Food Chemistry: Maillard Reaction, Browning, Oxidation, Preservation, and Additives",
        keywords=["food chemistry", "Maillard reaction", "browning", "lipid oxidation", "food preservation", "food additives", "antioxidants", "flavor development"],
        conclusion_template=(
            "Chemical reactions such as Maillard browning and lipid oxidation significantly affect food quality, while preservation techniques and additives mitigate spoilage and enhance safety."
        ),
        reasoning_framework=(
            "Food chemistry examines chemical processes affecting food composition, quality, and safety. The Maillard reaction involves non-enzymatic browning between reducing sugars and amino acids, producing flavor and color compounds but potentially harmful advanced glycation end-products. "
            "Lipid oxidation leads to rancidity, off-flavors, and nutrient loss, catalyzed by oxygen, light, and metals. "
            "Food preservation methods including thermal processing, refrigeration, and chemical additives inhibit microbial growth and chemical degradation. "
            "Additives such as antioxidants (e.g., BHA, BHT), preservatives (e.g., sorbates, nitrates), and flavor enhancers improve shelf life and sensory attributes. "
            "Regulatory agencies set limits and approve additives based on safety evaluations. "
            "Analytical techniques monitor reaction products and additive levels. "
            "Understanding reaction mechanisms guides formulation and processing to optimize food quality."
        ),
        key_factors=[
            "Reaction conditions (temperature, pH, water activity)",
            "Reactant concentrations and food matrix",
            "Oxygen exposure and metal catalysts",
            "Additive type and concentration",
            "Processing and storage conditions",
            "Regulatory compliance",
            "Sensory and nutritional impacts"
        ],
        primary_authority=[
            "Fennema, O. R., 'Food Chemistry', 4th Ed., CRC Press, 1996",
            "Damodaran, S., Parkin, K. L., and Fennema, O. R., 'Fennema's Food Chemistry', 5th Ed., CRC Press, 2017",
            "Belitz, H.-D., Grosch, W., and Schieberle, P., 'Food Chemistry', 4th Ed., Springer, 2009",
            "FDA, 'Food Additives Status List', 2023",
            "Mottram, D. S., 'The Maillard Reaction: Chemistry, Biochemistry and Implications', Royal Society of Chemistry, 2001"
        ],
        burden_holder="Food chemist or quality control specialist",
        adversary_position="Claims chemical additives pose health risks and natural preservation is preferable",
        counter_arguments=[
            "Additives are rigorously tested and regulated for safety",
            "Preservation extends shelf life and reduces food waste",
            "Chemical reactions are controlled to minimize harmful products",
            "Natural preservation methods have limitations",
            "Consumer safety and product quality are priorities"
        ],
        resolution_strategy=(
            "Balance additive use with consumer preferences and safety through transparent labeling and research."
        ),
        entity_scope="Food manufacturing, quality assurance, regulatory agencies",
        confidence=0.91,
        confidence_zone="Moderate to High",
        controlling_precedent="Fennema, O. R. (1996). Food Chemistry."
    ),
    DoctrineBlock(
        topic="Forensic Chemistry: Trace Analysis, Drug Identification, Toxicology Screening",
        keywords=["forensic chemistry", "trace analysis", "drug identification", "toxicology", "mass spectrometry", "chromatography", "sample preparation", "evidential standards"],
        conclusion_template=(
            "Forensic chemical analysis employs sensitive and specific techniques for trace detection and identification of substances, supporting legal investigations."
        ),
        reasoning_framework=(
            "Forensic chemistry applies analytical chemistry to legal matters, focusing on detection and identification of trace evidence including drugs, poisons, and explosives. "
            "Sample preparation methods such as solid-phase extraction and microextraction concentrate analytes from complex matrices. "
            "Chromatographic techniques (GC, LC) coupled with mass spectrometry provide high sensitivity and specificity for compound identification. "
            "Spectroscopic methods complement chromatographic data. "
            "Toxicology screening assesses biological samples for presence and concentration of toxic substances. "
            "Chain of custody, method validation, and quality assurance ensure data admissibility in court. "
            "Interpretation considers matrix effects, detection limits, and potential interferences. "
            "Standardized protocols and accreditation maintain analytical integrity."
        ),
        key_factors=[
            "Sample integrity and chain of custody",
            "Sensitivity and specificity of analytical methods",
            "Method validation and calibration",
            "Matrix effects and interferences",
            "Data interpretation and reporting",
            "Legal and regulatory requirements",
            "Quality control and accreditation"
        ],
        primary_authority=[
            "Siegel, J. A., 'Forensic Science: The Basics', 2nd Ed., CRC Press, 2015",
            "Houck, M. M., and Siegel, J. A., 'Fundamentals of Forensic Science', 3rd Ed., Academic Press, 2015",
            "Coyle, H. M., and Ennis, B. J., 'Forensic Chemistry', Wiley, 2018",
            "SWGDRUG, 'Scientific Working Group for the Analysis of Seized Drugs Guidelines', 2019",
            "ASTM E2329-16, 'Standard Guide for Interpretation of Mass Spectra in Forensic Chemistry', ASTM International, 2016"
        ],
        burden_holder="Forensic chemist or toxicologist",
        adversary_position="Challenges reliability of trace evidence and analytical methods",
        counter_arguments=[
            "Validated methods ensure reliability and reproducibility",
            "Quality assurance programs maintain analytical standards",
            "Multiple complementary techniques confirm findings",
            "Expert testimony explains limitations and confidence",
            "Legal precedents support admissibility of evidence"
        ],
        resolution_strategy=(
            "Maintain rigorous validation, documentation, and expert training to uphold evidential standards."
        ),
        entity_scope="Forensic laboratories, law enforcement, legal system",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Siegel, J. A. (2015). Forensic Science: The Basics."
    ),
    DoctrineBlock(
        topic="Industrial Chemistry: Process Optimization, Reactor Design, Scale-up, and Yield Improvement",
        keywords=["industrial chemistry", "process optimization", "reactor design", "scale-up", "chemical yield", "mass transfer", "heat transfer", "process control"],
        conclusion_template=(
            "Optimizing industrial chemical processes through reactor design and scale-up strategies enhances yield, efficiency, and safety."
        ),
        reasoning_framework=(
            "Industrial chemistry focuses on large-scale chemical production, requiring optimization of reaction conditions, reactor configurations, and process parameters. "
            "Reactor design considers kinetics, thermodynamics, mass and heat transfer, mixing, and catalyst performance to maximize conversion and selectivity. "
            "Scale-up from laboratory to pilot and production scale involves addressing changes in hydrodynamics, heat removal, and safety hazards. "
            "Process control systems monitor and adjust variables to maintain optimal operation. "
            "Yield improvement strategies include catalyst optimization, feedstock purity, and reaction condition fine-tuning. "
            "Economic and environmental considerations drive process intensification and waste minimization. "
            "Computational modeling and simulation support design and troubleshooting. "
            "Regulatory compliance and safety standards guide industrial operations."
        ),
        key_factors=[
            "Reaction kinetics and mechanism",
            "Heat and mass transfer limitations",
            "Reactor type and configuration",
            "Scale-up challenges and solutions",
            "Process monitoring and control",
            "Catalyst selection and stability",
            "Safety and environmental compliance"
        ],
        primary_authority=[
            "Fogler, H. S., 'Elements of Chemical Reaction Engineering', 5th Ed., Prentice Hall, 2016",
            "Levenspiel, O., 'Chemical Reaction Engineering', 3rd Ed., Wiley, 1999",
            "Nauman, E. B., 'Chemical Reactor Design, Optimization, and Scaleup', McGraw-Hill, 2002",
            "Smith, J. M., 'Chemical Engineering Kinetics', 3rd Ed., McGraw-Hill, 1981",
            "Towler, G., and Sinnott, R., 'Chemical Engineering Design', 2nd Ed., Elsevier, 2012"
        ],
        burden_holder="Process engineer or industrial chemist",
        adversary_position="Asserts scale-up introduces unpredictable issues compromising yield and safety",
        counter_arguments=[
            "Systematic scale-up methodologies mitigate risks",
            "Pilot plant studies identify and resolve issues",
            "Process simulation predicts scale effects",
            "Robust control systems maintain safe operation",
            "Continuous improvement enhances process reliability"
        ],
        resolution_strategy=(
            "Employ integrated experimental and modeling approaches for scale-up and process optimization."
        ),
        entity_scope="Chemical manufacturing, pharmaceuticals, petrochemicals",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Fogler, H. S. (2016). Elements of Chemical Reaction Engineering."
    ),
    DoctrineBlock(
        topic="Green Chemistry: Twelve Principles, Atom Economy, and Solvent Selection",
        keywords=["green chemistry", "sustainability", "atom economy", "solvent selection", "waste minimization", "renewable feedstocks", "energy efficiency", "benign synthesis"],
        conclusion_template=(
            "Green chemistry principles guide the design of chemical processes that minimize environmental impact through efficient use of materials and safer solvents."
        ),
        reasoning_framework=(
            "Green chemistry aims to reduce or eliminate hazardous substances in chemical production and use, promoting sustainability. "
            "The twelve principles, articulated by Anastas and Warner, include prevention of waste, atom economy, less hazardous synthesis, safer solvents, energy efficiency, and use of renewable feedstocks. "
            "Atom economy measures the efficiency of a reaction in incorporating all atoms of reactants into the final product, encouraging reactions with minimal by-products. "
            "Solvent selection prioritizes non-toxic, biodegradable, and renewable solvents, reducing environmental and health risks. "
            "Process intensification and catalysis improve energy efficiency and selectivity. "
            "Life cycle assessment evaluates environmental impacts from raw materials to disposal. "
            "Implementation requires interdisciplinary collaboration, regulatory support, and economic incentives. "
            "Green chemistry advances innovation in pharmaceuticals, materials, and industrial processes."
        ),
        key_factors=[
            "Reaction efficiency and atom economy",
            "Hazardous reagent and solvent avoidance",
            "Energy consumption and process conditions",
            "Renewable and sustainable feedstocks",
            "Waste generation and treatment",
            "Product biodegradability and toxicity",
            "Regulatory and economic considerations"
        ],
        primary_authority=[
            "Anastas, P. T., and Warner, J. C., 'Green Chemistry: Theory and Practice', Oxford University Press, 1998",
            "Constable, D. J. C., et al., 'Green Chemistry Metrics: Measuring and Monitoring Sustainable Processes', Green Chem., 2007",
            "Clark, J. H., and Macquarrie, D. J., 'Handbook of Green Chemistry and Technology', Wiley, 2002",
            "Sheldon, R. A., 'Green and Sustainable Manufacture of Chemicals', Chem. Soc. Rev., 2012",
            "US EPA, 'Green Chemistry Program', 2023"
        ],
        burden_holder="Process chemist or sustainability officer",
        adversary_position="Claims green chemistry compromises performance and increases costs",
        counter_arguments=[
            "Green chemistry enhances efficiency and reduces waste disposal costs",
            "Innovations improve performance and sustainability simultaneously",
            "Regulatory trends favor green processes",
            "Consumer demand drives adoption",
            "Long-term benefits outweigh initial investments"
        ],
        resolution_strategy=(
            "Integrate green chemistry principles early in process development and leverage economic incentives."
        ),
        entity_scope="Chemical industry, pharmaceuticals, academia",
        confidence=0.90,
        confidence_zone="Moderate to High",
        controlling_precedent="Anastas, P. T., and Warner, J. C. (1998). Green Chemistry."
    ),
    DoctrineBlock(
        topic="Supramolecular Chemistry: Host-Guest Complexes and Molecular Recognition",
        keywords=["supramolecular chemistry", "host-guest", "self-assembly", "molecular recognition", "non-covalent interactions", "cavitands", "cyclodextrins", "binding affinity"],
        conclusion_template=(
            "Supramolecular chemistry exploits non-covalent interactions to create host-guest complexes with specific molecular recognition properties, enabling functional assemblies."
        ),
        reasoning_framework=(
            "Supramolecular chemistry studies organized entities formed by intermolecular interactions rather than covalent bonds. "
            "Host-guest chemistry involves a host molecule selectively binding a guest through hydrogen bonding, van der Waals forces, π-π stacking, and electrostatic interactions. "
            "Self-assembly processes lead to complex architectures with emergent properties. "
            "Molecular recognition underpins biological systems and synthetic receptors, enabling selective sensing, catalysis, and transport. "
            "Binding affinity and selectivity depend on complementarity in shape, charge, and functional groups. "
            "Characterization techniques include NMR, ITC, UV-Vis titrations, and X-ray crystallography. "
            "Applications span drug delivery, molecular machines, and nanotechnology. "
            "Design principles focus on thermodynamics and kinetics of assembly and disassembly."
        ),
        key_factors=[
            "Nature and strength of non-covalent interactions",
            "Host and guest molecular complementarity",
            "Thermodynamic parameters (ΔG, ΔH, ΔS)",
            "Kinetic stability and exchange rates",
            "Environmental conditions (solvent, pH)",
            "Analytical characterization methods",
            "Functional application requirements"
        ],
        primary_authority=[
            "Lehn, J.-M., 'Supramolecular Chemistry: Concepts and Perspectives', Wiley-VCH, 1995",
            "Steed, J. W., and Atwood, J. L., 'Supramolecular Chemistry', 2nd Ed., Wiley, 2009",
            "Hunter, C. A., 'Molecular Recognition in Chemical and Biological Systems', Chem. Soc. Rev., 1994",
            "Cram, D. J., 'The Design of Molecular Hosts, Guests, and Their Complexes', Science, 1983",
            "Rebek, J., 'Molecular Behavior in Small Spaces', Acc. Chem. Res., 2009"
        ],
        burden_holder="Supramolecular chemist or nanotechnologist",
        adversary_position="Claims supramolecular assemblies lack stability and practical utility",
        counter_arguments=[
            "Many host-guest systems exhibit high affinity and selectivity",
            "Applications demonstrate functional stability under relevant conditions",
            "Dynamic assemblies enable responsive materials",
            "Design strategies improve robustness",
            "Experimental evidence supports utility"
        ],
        resolution_strategy=(
            "Develop tailored supramolecular systems with optimized stability and functionality for target applications."
        ),
        entity_scope="Nanotechnology, drug delivery, sensor development",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="Lehn, J.-M. (1995). Supramolecular Chemistry."
    ),
    DoctrineBlock(
        topic="Quantum Chemistry: Schrödinger Equation, Orbital Theory, and Chemical Bonding",
        keywords=["quantum chemistry", "Schrödinger equation", "molecular orbitals", "bonding theory", "electron density", "wavefunction", "computational methods", "chemical reactivity"],
        conclusion_template=(
            "Quantum chemistry provides a fundamental framework for understanding molecular structure and bonding through solutions of the Schrödinger equation and orbital theory."
        ),
        reasoning_framework=(
            "Quantum chemistry applies quantum mechanics to chemical systems, describing electrons and nuclei by wavefunctions governed by the Schrödinger equation. "
            "Exact solutions exist only for the hydrogen atom; approximate methods such as Hartree-Fock and post-Hartree-Fock techniques are used for multi-electron systems. "
            "Molecular orbital theory constructs orbitals as linear combinations of atomic orbitals, explaining bonding, antibonding, and nonbonding interactions. "
            "Electron density distributions derived from wavefunctions inform on chemical reactivity and properties. "
            "Computational quantum chemistry employs basis sets and numerical methods to solve equations, predicting geometries, energies, spectra, and reaction pathways. "
            "Theoretical insights complement experimental observations and guide molecular design. "
            "Limitations include computational cost and approximations inherent in methods. "
            "Advances in algorithms and hardware continue to expand applicability."
        ),
        key_factors=[
            "Formulation and solution of Schrödinger equation",
            "Choice of basis sets and computational methods",
            "Interpretation of molecular orbitals",
            "Electron correlation and exchange effects",
            "Energy minimization and geometry optimization",
            "Prediction of spectroscopic properties",
            "Computational resource considerations"
        ],
        primary_authority=[
            "Szabo, A., and Ostlund, N. S., 'Modern Quantum Chemistry', Dover Publications, 1996",
            "Levine, I. N., 'Quantum Chemistry', 7th Ed., Pearson, 2013",
            "Jensen, F., 'Introduction to Computational Chemistry', 3rd Ed., Wiley, 2017",
            "McQuarrie, D. A., 'Quantum Chemistry', University Science Books, 2007",
            "Helgaker, T., Jørgensen, P., and Olsen, J., 'Molecular Electronic-Structure Theory', Wiley, 2000"
        ],
        burden_holder="Theoretical chemist or computational chemist",
        adversary_position="Claims quantum chemical methods are too abstract and computationally intensive for practical use",
        counter_arguments=[
            "Quantum chemistry underpins modern molecular science",
            "Computational advances enable routine calculations",
            "Theoretical predictions guide experimental design",
            "Approximate methods balance accuracy and cost",
            "Extensive validation against experimental data"
        ],
        resolution_strategy=(
            "Leverage scalable computational methods and integrate theory with experiment."
        ),
        entity_scope="Molecular modeling, drug design, materials science",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Szabo, A., and Ostlund, N. S. (1996). Modern Quantum Chemistry."
    ),
    DoctrineBlock(
        topic="Colloid Chemistry: Emulsions, Suspensions, Sol-Gel Processes, and Nanoparticles",
        keywords=["colloid chemistry", "emulsions", "suspensions", "sol-gel", "nanoparticles", "surface charge", "stability", "aggregation"],
        conclusion_template=(
            "Colloid chemistry principles govern the formation, stability, and properties of dispersed systems "
            "including emulsions, suspensions, sols, and gels. DLVO theory predicts colloidal stability "
            "based on the balance of van der Waals attraction and electrostatic repulsion."
        ),
        reasoning_framework=(
            "Colloidal systems are dispersions where particles (1-1000 nm) are distributed in a continuous "
            "medium. Stability depends on surface charge (zeta potential), steric stabilization, and the "
            "balance of attractive and repulsive forces described by DLVO theory."
        ),
        key_factors=["Particle size and distribution", "Zeta potential and surface charge", "DLVO forces", "Steric stabilization", "Medium properties"],
        primary_authority=["DLVO Theory (Derjaguin, Landau, Verwey, Overbeek)", "Hunter, R.J. Foundations of Colloid Science"],
        burden_holder="Formulator",
        adversary_position="System is thermodynamically stable without stabilization agents.",
        counter_arguments=["Kinetic stability differs from thermodynamic stability", "Zeta potential alone doesn't predict stability", "Multiple stabilization mechanisms may be needed"],
        resolution_strategy="Apply DLVO analysis, measure zeta potential, test stability under conditions of use.",
        entity_scope="Colloid scientists, formulators, materials engineers",
        confidence=0.88,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="DLVO Theory"
    ),
]

# =============================================
# SUB-ENGINE ORCHESTRATION
# =============================================

ENGINE_IDS = [
    "CHEM01", "CHEM02", "CHEM03", "CHEM04", "CHEM05", "CHEM06", "CHEM07", "CHEM08", "CHEM09", "CHEM10",
    "CHEM11", "CHEM12", "CHEM13", "CHEM14", "CHEM15", "CHEM16", "CHEM17", "CHEM18", "CHEM19", "CHEM20"
]

ENGINE_URLS = {
    "CHEM01": "http://localhost:8001",
    "CHEM02": "http://localhost:8002",
    "CHEM03": "http://localhost:8003",
    "CHEM04": "http://localhost:8004",
    "CHEM05": "http://localhost:8005",
    "CHEM06": "http://localhost:8006",
    "CHEM07": "http://localhost:8007",
    "CHEM08": "http://localhost:8008",
    "CHEM09": "http://localhost:8009",
    "CHEM10": "http://localhost:8010",
    "CHEM11": "http://localhost:8011",
    "CHEM12": "http://localhost:8012",
    "CHEM13": "http://localhost:8013",
    "CHEM14": "http://localhost:8014",
    "CHEM15": "http://localhost:8015",
    "CHEM16": "http://localhost:8016",
    "CHEM17": "http://localhost:8017",
    "CHEM18": "http://localhost:8018",
    "CHEM19": "http://localhost:8019",
    "CHEM20": "http://localhost:8020"
}

ENGINE_DOMAINS = {
    "CHEM01": "Organic Synthesis",
    "CHEM02": "Analytical Methods",
    "CHEM03": "Polymer Science",
    "CHEM04": "Electrochemistry",
    "CHEM05": "Thermodynamics",
    "CHEM06": "Kinetics",
    "CHEM07": "Spectroscopy",
    "CHEM08": "Crystallography",
    "CHEM09": "Computational Chemistry",
    "CHEM10": "Environmental Chemistry",
    "CHEM11": "Inorganic Chemistry",
    "CHEM12": "Biochemistry",
    "CHEM13": "Materials Science",
    "CHEM14": "Nuclear Chemistry",
    "CHEM15": "Surface Chemistry",
    "CHEM16": "Photochemistry",
    "CHEM17": "Geochemistry",
    "CHEM18": "Food Chemistry",
    "CHEM19": "Forensic Chemistry",
    "CHEM20": "Industrial Chemistry"
}

DOMAIN_KEYWORDS = {
    "Organic Synthesis": ["synthesis", "organic", "reaction", "reagent", "product", "yield", "mechanism"],
    "Analytical Methods": ["analysis", "spectrometry", "chromatography", "titration", "quantitative", "qualitative"],
    "Polymer Science": ["polymer", "macromolecule", "polymerization", "chain", "copolymer", "monomer"],
    "Electrochemistry": ["electrochemical", "electrode", "potential", "current", "redox", "voltage"],
    "Thermodynamics": ["thermodynamics", "enthalpy", "entropy", "energy", "temperature", "heat", "free energy"],
    "Kinetics": ["kinetics", "rate", "reaction", "speed", "order", "mechanism", "activation energy"],
    "Spectroscopy": ["spectroscopy", "spectra", "absorption", "emission", "wavelength", "frequency", "NMR", "IR", "UV"],
    "Crystallography": ["crystal", "structure", "x-ray", "diffraction", "lattice", "unit cell"],
    "Computational Chemistry": ["computational", "simulation", "modeling", "quantum", "molecular", "DFT", "ab initio"],
    "Environmental Chemistry": ["environmental", "pollution", "contaminant", "remediation", "ecosystem", "toxicity"],
    "Inorganic Chemistry": ["inorganic", "metal", "complex", "coordination", "salt", "mineral"],
    "Biochemistry": ["biochemistry", "enzyme", "protein", "DNA", "RNA", "metabolism", "cell"],
    "Materials Science": ["material", "property", "composite", "ceramic", "alloy", "nanomaterial"],
    "Nuclear Chemistry": ["nuclear", "radioactive", "isotope", "decay", "radiation", "fission", "fusion"],
    "Surface Chemistry": ["surface", "adsorption", "interface", "catalysis", "layer", "coating"],
    "Photochemistry": ["photochemistry", "light", "photo", "excited", "absorption", "emission"],
    "Geochemistry": ["geochemistry", "mineral", "rock", "soil", "element", "earth", "isotope"],
    "Food Chemistry": ["food", "nutrition", "ingredient", "flavor", "additive", "processing"],
    "Forensic Chemistry": ["forensic", "crime", "evidence", "analysis", "toxicology", "drug"],
    "Industrial Chemistry": ["industrial", "process", "manufacturing", "scale", "production", "plant"]
}

# --- Enums and Data Classes ---

class SubEngineStatus(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    UNKNOWN = auto()

class CircuitBreakerState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class IssueCategory(Enum):
    ORGANIC_SYNTHESIS = auto()
    ANALYTICAL_METHODS = auto()
    POLYMER_SCIENCE = auto()
    ELECTROCHEMISTRY = auto()
    THERMODYNAMICS = auto()
    KINETICS = auto()
    SPECTROSCOPY = auto()
    CRYSTALLOGRAPHY = auto()
    COMPUTATIONAL_CHEMISTRY = auto()
    ENVIRONMENTAL_CHEMISTRY = auto()
    INORGANIC_CHEMISTRY = auto()
    BIOCHEMISTRY = auto()
    MATERIALS_SCIENCE = auto()
    NUCLEAR_CHEMISTRY = auto()
    SURFACE_CHEMISTRY = auto()
    PHOTOCHEMISTRY = auto()
    GEOCHEMISTRY = auto()
    FOOD_CHEMISTRY = auto()
    FORENSIC_CHEMISTRY = auto()
    INDUSTRIAL_CHEMISTRY = auto()

CATEGORY_TO_ENGINE = {
    IssueCategory.ORGANIC_SYNTHESIS: "CHEM01",
    IssueCategory.ANALYTICAL_METHODS: "CHEM02",
    IssueCategory.POLYMER_SCIENCE: "CHEM03",
    IssueCategory.ELECTROCHEMISTRY: "CHEM04",
    IssueCategory.THERMODYNAMICS: "CHEM05",
    IssueCategory.KINETICS: "CHEM06",
    IssueCategory.SPECTROSCOPY: "CHEM07",
    IssueCategory.CRYSTALLOGRAPHY: "CHEM08",
    IssueCategory.COMPUTATIONAL_CHEMISTRY: "CHEM09",
    IssueCategory.ENVIRONMENTAL_CHEMISTRY: "CHEM10",
    IssueCategory.INORGANIC_CHEMISTRY: "CHEM11",
    IssueCategory.BIOCHEMISTRY: "CHEM12",
    IssueCategory.MATERIALS_SCIENCE: "CHEM13",
    IssueCategory.NUCLEAR_CHEMISTRY: "CHEM14",
    IssueCategory.SURFACE_CHEMISTRY: "CHEM15",
    IssueCategory.PHOTOCHEMISTRY: "CHEM16",
    IssueCategory.GEOCHEMISTRY: "CHEM17",
    IssueCategory.FOOD_CHEMISTRY: "CHEM18",
    IssueCategory.FORENSIC_CHEMISTRY: "CHEM19",
    IssueCategory.INDUSTRIAL_CHEMISTRY: "CHEM20"
}

class QueryRequest:
    def __init__(self, text: str, mode: str = "default", metadata: Optional[Dict[str, Any]] = None):
        self.text = text
        self.mode = mode
        self.metadata = metadata or {}

class RoutingDecision:
    def __init__(self, engine_ids: List[str], reason: str, fallback: Optional[List[str]] = None):
        self.engine_ids = engine_ids
        self.reason = reason
        self.fallback = fallback or []

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, domain: str):
        self.engine_id = engine_id
        self.url = url
        self.domain = domain

class SubEngineResponse:
    def __init__(self, engine_id: str, response: Any, status: SubEngineStatus, latency: float):
        self.engine_id = engine_id
        self.response = response
        self.status = status
        self.latency = latency

# --- CircuitBreaker Implementation ---

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 30.0):
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.last_failure_time = 0.0
        self.recovery_timeout = recovery_timeout
        self.lock = threading.Lock()

    def record_failure(self):
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitBreakerState.OPEN

    def record_success(self):
        with self.lock:
            self.failure_count = 0
            self.state = CircuitBreakerState.CLOSED

    def can_attempt(self):
        with self.lock:
            if self.state == CircuitBreakerState.OPEN:
                elapsed = time.time() - self.last_failure_time
                if elapsed >= self.recovery_timeout:
                    self.state = CircuitBreakerState.HALF_OPEN
                    return True
                return False
            return True

    def attempt_result(self, success: bool):
        with self.lock:
            if self.state == CircuitBreakerState.HALF_OPEN:
                if success:
                    self.state = CircuitBreakerState.CLOSED
                    self.failure_count = 0
                else:
                    self.state = CircuitBreakerState.OPEN
                    self.last_failure_time = time.time()
            elif self.state == CircuitBreakerState.CLOSED:
                if not success:
                    self.record_failure()
            elif self.state == CircuitBreakerState.OPEN:
                pass

    def get_state(self):
        with self.lock:
            return self.state

# --- SubEngineHealthMonitor ---

class SubEngineHealthMonitor:
    def __init__(self, engine_urls: Dict[str, str], ttl: float = 60.0):
        self.engine_urls = engine_urls
        self.ttl = ttl
        self.health_cache: Dict[str, Tuple[SubEngineStatus, float]] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {
            eid: CircuitBreaker() for eid in engine_urls.keys()
        }
        self.lock = threading.Lock()

    async def _ping_engine(self, url: str, timeout: float = 2.0) -> SubEngineStatus:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}/health", timeout=timeout) as resp:
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

    def check_health(self, engine_id: str) -> SubEngineStatus:
        now = time.time()
        with self.lock:
            if engine_id in self.health_cache:
                status, ts = self.health_cache[engine_id]
                if now - ts < self.ttl:
                    return status
        url = self.engine_urls.get(engine_id)
        if not url:
            return SubEngineStatus.UNKNOWN
        breaker = self.circuit_breakers[engine_id]
        if not breaker.can_attempt():
            return SubEngineStatus.UNHEALTHY
        loop = asyncio.get_event_loop()
        status = loop.run_until_complete(self._ping_engine(url))
        with self.lock:
            self.health_cache[engine_id] = (status, now)
        if status == SubEngineStatus.HEALTHY:
            breaker.record_success()
        else:
            breaker.record_failure()
        return status

    def check_all_health(self) -> Dict[str, SubEngineStatus]:
        now = time.time()
        results = {}
        with self.lock:
            for eid in self.engine_urls.keys():
                if eid in self.health_cache:
                    status, ts = self.health_cache[eid]
                    if now - ts < self.ttl:
                        results[eid] = status
                        continue
                url = self.engine_urls[eid]
                breaker = self.circuit_breakers[eid]
                if not breaker.can_attempt():
                    results[eid] = SubEngineStatus.UNHEALTHY
                    continue
                loop = asyncio.get_event_loop()
                status = loop.run_until_complete(self._ping_engine(url))
                self.health_cache[eid] = (status, now)
                if status == SubEngineStatus.HEALTHY:
                    breaker.record_success()
                else:
                    breaker.record_failure()
                results[eid] = status
        return results

    def get_healthy_engines(self) -> List[str]:
        health = self.check_all_health()
        return [eid for eid, status in health.items() if status == SubEngineStatus.HEALTHY]

    def get_circuit_breaker(self, engine_id: str) -> CircuitBreaker:
        return self.circuit_breakers[engine_id]

# --- QueryRouter ---

class QueryRouter:
    def __init__(self, health_monitor: SubEngineHealthMonitor):
        self.health_monitor = health_monitor

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text_lower = text.lower()
        matched_categories = []
        for domain, keywords in DOMAIN_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    cat = self._domain_to_category(domain)
                    if cat and cat not in matched_categories:
                        matched_categories.append(cat)
        if not matched_categories:
            matched_categories.append(IssueCategory.ANALYTICAL_METHODS)
        return matched_categories

    def _domain_to_category(self, domain: str) -> Optional[IssueCategory]:
        for cat in IssueCategory:
            if domain.replace(" ", "_").upper() == cat.name:
                return cat
        return None

    def _select_engines(self, categories: List[IssueCategory], mode: str) -> List[SubEngineConfig]:
        healthy = self.health_monitor.get_healthy_engines()
        configs = []
        for cat in categories:
            eid = CATEGORY_TO_ENGINE.get(cat)
            if eid and eid in healthy:
                configs.append(SubEngineConfig(eid, ENGINE_URLS[eid], ENGINE_DOMAINS[eid]))
        if not configs:
            for cat in categories:
                eid = CATEGORY_TO_ENGINE.get(cat)
                if eid:
                    configs.append(SubEngineConfig(eid, ENGINE_URLS[eid], ENGINE_DOMAINS[eid]))
        if mode == "broad":
            configs = [SubEngineConfig(eid, ENGINE_URLS[eid], ENGINE_DOMAINS[eid]) for eid in ENGINE_IDS]
        return configs

    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        categories = self._classify_domain(query.text)
        configs = self._select_engines(categories, query.mode)
        return [cfg.engine_id for cfg in configs]

    def _score_engine_relevance(self, engine_id: str, query: QueryRequest) -> float:
        domain = ENGINE_DOMAINS[engine_id]
        keywords = DOMAIN_KEYWORDS[domain]
        text = query.text.lower()
        score = sum([text.count(kw) for kw in keywords])
        return score / (len(keywords) + 1)

    def _handle_engine_failure(self, engine_id: str, error: Exception) -> List[str]:
        breaker = self.health_monitor.get_circuit_breaker(engine_id)
        breaker.record_failure()
        healthy = self.health_monitor.get_healthy_engines()
        fallback = [eid for eid in healthy if eid != engine_id]
        return fallback

    def route_query(self, query: QueryRequest) -> RoutingDecision:
        engine_ids = self._apply_routing_rules(query)
        reason = f"Matched categories for query '{query.text}'"
        fallback = []
        for eid in engine_ids:
            status = self.health_monitor.check_health(eid)
            if status != SubEngineStatus.HEALTHY:
                fallback += self._handle_engine_failure(eid, Exception("Engine unhealthy"))
        fallback = list(set(fallback))
        return RoutingDecision(engine_ids, reason, fallback)

# --- SubEngineOrchestrator ---

class SubEngineOrchestrator:
    def __init__(self, health_monitor: SubEngineHealthMonitor):
        self.health_monitor = health_monitor

    async def _call_sub_engine(self, engine_config: SubEngineConfig, query: QueryRequest) -> SubEngineResponse:
        breaker = self.health_monitor.get_circuit_breaker(engine_config.engine_id)
        if not breaker.can_attempt():
            return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, 0.0)
        url = f"{engine_config.url}/query"
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json={"text": query.text, "mode": query.mode, "metadata": query.metadata}, timeout=5.0) as resp:
                    latency = time.time() - start
                    if resp.status == 200:
                        data = await resp.json()
                        breaker.attempt_result(True)
                        return SubEngineResponse(engine_config.engine_id, data, SubEngineStatus.HEALTHY, latency)
                    else:
                        breaker.attempt_result(False)
                        return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, latency)
        except Exception:
            breaker.attempt_result(False)
            return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, time.time() - start)

    async def dispatch_query(self, query: QueryRequest, engines: List[SubEngineConfig]) -> List[SubEngineResponse]:
        responses = []
        for engine in engines:
            resp = await self._call_sub_engine(engine, query)
            responses.append(resp)
        return responses

    async def dispatch_parallel(self, query: QueryRequest, engines: List[SubEngineConfig]) -> List[SubEngineResponse]:
        tasks = [self._call_sub_engine(engine, query) for engine in engines]
        responses = await asyncio.gather(*tasks)
        return responses

    async def dispatch_cascade(self, query: QueryRequest, engines: List[SubEngineConfig]) -> Optional[SubEngineResponse]:
        for engine in engines:
            resp = await self._call_sub_engine(engine, query)
            if resp.status == SubEngineStatus.HEALTHY and resp.response is not None:
                return resp
        return None

    def _merge_responses(self, responses: List[SubEngineResponse]) -> Any:
        merged = {}
        for resp in responses:
            if resp.status == SubEngineStatus.HEALTHY and resp.response is not None:
                merged[resp.engine_id] = resp.response
        return merged

    def _resolve_conflicts(self, responses: List[SubEngineResponse]) -> Any:
        healthy_responses = [resp.response for resp in responses if resp.status == SubEngineStatus.HEALTHY and resp.response is not None]
        if not healthy_responses:
            return None
        if len(healthy_responses) == 1:
            return healthy_responses[0]
        consensus = self._consensus_algorithm(healthy_responses)
        return consensus

    def _consensus_algorithm(self, responses: List[Any]) -> Any:
        # Simple majority voting for demonstration
        from collections import Counter
        if all(isinstance(r, dict) and 'answer' in r for r in responses):
            answers = [r['answer'] for r in responses]
            most_common = Counter(answers).most_common(1)
            if most_common:
                return {'answer': most_common[0][0], 'votes': most_common[0][1]}
        return responses[0]

# --- Example Usage ---

# health_monitor = SubEngineHealthMonitor(ENGINE_URLS)
# router = QueryRouter(health_monitor)
# orchestrator = SubEngineOrchestrator(health_monitor)

# query = QueryRequest("What is the mechanism of the Diels-Alder reaction?")
# decision = router.route_query(query)
# engines = [SubEngineConfig(eid, ENGINE_URLS[eid], ENGINE_DOMAINS[eid]) for eid in decision.engine_ids]

# loop = asyncio.get_event_loop()
# responses = loop.run_until_complete(orchestrator.dispatch_parallel(query, engines))
# merged = orchestrator._merge_responses(responses)
# consensus = orchestrator._resolve_conflicts(responses)

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
    returns dominant authority_level and list of dominant sources
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
    dominant_sources = [src for lvl, src in sources if lvl == dominant_level]
    return dominant_level, dominant_sources

# -------------------------
# EPISTEMIC GUARDRAILS
# -------------------------

BANNED_PHRASES = [
    "clearly", "obviously", "without doubt", "undeniably", "unquestionably",
    "definitely", "absolutely", "certainly", "beyond question", "incontrovertibly",
    "irrefutably", "unequivocally", "incontestably", "manifestly", "patently",
    "categorically", "infallibly", "invariably", "decisively", "indisputably",
    "incontrovertible", "without fail", "without exception", "unambiguously",
    "conclusively", "undoubtedly", "beyond any doubt", "without reservation",
    "incontestable", "unassailably", "incontestably", "without question"
]

CONFIDENCE_LEVELS = Enum('ConfidenceLevel', 'DEFENSIBLE AGGRESSIVE DISCLOSURE HIGH_RISK')

def apply_epistemic_guardrails(text):
    """
    Removes banned phrases and appends a disclosure caveat.
    """
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, BANNED_PHRASES)) + r')\b', re.IGNORECASE)
    cleaned_text = pattern.sub('', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    disclosure_caveat = (" Note: This analysis is provided with epistemic humility and "
                         "should be considered within the bounds of current knowledge and evidence.")
    return cleaned_text + disclosure_caveat

def confidence_stratification(score):
    """
    Stratify confidence based on a numeric score (0-1).
    Returns one of DEFENSIBLE, AGGRESSIVE, DISCLOSURE, HIGH_RISK
    """
    if score >= 0.85:
        return CONFIDENCE_LEVELS.DEFENSIBLE
    elif score >= 0.65:
        return CONFIDENCE_LEVELS.AGGRESSIVE
    elif score >= 0.4:
        return CONFIDENCE_LEVELS.DISCLOSURE
    else:
        return CONFIDENCE_LEVELS.HIGH_RISK

# -------------------------
# FACT FRAGILITY SCORING
# -------------------------

def score_fact_fragility(fact):
    """
    fact: dict with keys 'verifiability', 'recharacterization_risk', 'testimony_dependence'
    Each key expected to be a float 0-1
    Returns dict with same keys and overall fragility score 0-1
    """
    verifiability = fact.get('verifiability', 0.5)
    recharacterization_risk = fact.get('recharacterization_risk', 0.5)
    testimony_dependence = fact.get('testimony_dependence', 0.5)

    # Fragility increases with lower verifiability, higher recharacterization risk, higher testimony dependence
    fragility = ( (1 - verifiability) * 0.5 +
                  recharacterization_risk * 0.3 +
                  testimony_dependence * 0.2 )
    fragility = min(max(fragility, 0), 1)
    return {
        'verifiability': verifiability,
        'recharacterization_risk': recharacterization_risk,
        'testimony_dependence': testimony_dependence,
        'overall_fragility': fragility
    }

# -------------------------
# SEMANTIC NORMALIZATION
# -------------------------

DOMAIN_TERM_MAPPINGS = {
    # Base terms
    "acid": "acid",
    "base": "base",
    "alkali": "base",
    "alkaline": "base",
    "alkaline earth metal": "alkaline_earth_metal",
    "alkaline earth metals": "alkaline_earth_metal",
    "alkali metal": "alkali_metal",
    "alkali metals": "alkali_metal",
    "oxidation state": "oxidation_state",
    "oxidation number": "oxidation_state",
    "redox": "redox_reaction",
    "reduction-oxidation": "redox_reaction",
    "redox reaction": "redox_reaction",
    "redox reactions": "redox_reaction",
    "covalent bond": "covalent_bond",
    "ionic bond": "ionic_bond",
    "metallic bond": "metallic_bond",
    "molecular orbital": "molecular_orbital",
    "molecular orbitals": "molecular_orbital",
    "electron configuration": "electron_configuration",
    "periodic table": "periodic_table",
    "periodic trend": "periodic_trend",
    "periodic trends": "periodic_trend",
    "enthalpy": "enthalpy",
    "entropy": "entropy",
    "gibbs free energy": "gibbs_free_energy",
    "activation energy": "activation_energy",
    "reaction mechanism": "reaction_mechanism",
    "reaction mechanisms": "reaction_mechanism",
    "catalyst": "catalyst",
    "catalysts": "catalyst",
    "equilibrium constant": "equilibrium_constant",
    "equilibrium": "equilibrium",
    "le chatelier's principle": "le_chatelier_principle",
    "le chatelier principle": "le_chatelier_principle",
    "stoichiometry": "stoichiometry",
    "molarity": "molarity",
    "molality": "molality",
    "normality": "normality",
    "solubility": "solubility",
    "precipitation": "precipitation",
    "oxidation": "oxidation",
    "reduction": "reduction",
    "acid dissociation constant": "ka",
    "base dissociation constant": "kb",
    "ka": "ka",
    "kb": "kb",
    "ph": "ph",
    "pka": "pka",
    "pkb": "pkb",
    "buffer": "buffer",
    "buffer solution": "buffer",
    "buffer solutions": "buffer",
    "hydrolysis": "hydrolysis",
    "electronegativity": "electronegativity",
    "polar covalent bond": "polar_covalent_bond",
    "nonpolar covalent bond": "nonpolar_covalent_bond",
    "dipole moment": "dipole_moment",
    "molecular geometry": "molecular_geometry",
    "valence shell electron pair repulsion": "vsepr",
    "vsepr theory": "vsepr",
    "intermolecular forces": "intermolecular_forces",
    "hydrogen bonding": "hydrogen_bonding",
    "van der waals forces": "van_der_waals_forces",
    "van der waals interactions": "van_der_waals_forces",
    "chemical kinetics": "chemical_kinetics",
    "rate law": "rate_law",
    "reaction rate": "reaction_rate",
    "first order reaction": "first_order_reaction",
    "second order reaction": "second_order_reaction",
    "zero order reaction": "zero_order_reaction",
    "equilibrium": "equilibrium",
    "le chatelier's principle": "le_chatelier_principle",
    "enthalpy change": "enthalpy_change",
    "heat of reaction": "enthalpy_change",
    "exothermic": "exothermic",
    "endothermic": "endothermic",
    "oxidation number": "oxidation_state",
    "oxidation states": "oxidation_state",
    "oxidation numbers": "oxidation_state",
    "mole": "mole",
    "moles": "mole",
    "avogadro's number": "avogadro_number",
    "avogadro number": "avogadro_number",
    "ideal gas law": "ideal_gas_law",
    "ideal gas equation": "ideal_gas_law",
    "partial pressure": "partial_pressure",
    "dalton's law": "daltons_law",
    "dalton law": "daltons_law",
    "colligative properties": "colligative_properties",
    "osmotic pressure": "osmotic_pressure",
    "boiling point elevation": "boiling_point_elevation",
    "freezing point depression": "freezing_point_depression",
    "molecular mass": "molecular_mass",
    "molar mass": "molar_mass",
    "empirical formula": "empirical_formula",
    "molecular formula": "molecular_formula",
    "percent composition": "percent_composition",
    "chemical formula": "chemical_formula",
    "chemical equations": "chemical_equation",
    "chemical equation": "chemical_equation",
    "oxidizing agent": "oxidizing_agent",
    "reducing agent": "reducing_agent",
    "oxidation-reduction": "redox_reaction",
    "redox reaction": "redox_reaction",
    "redox reactions": "redox_reaction",
    "solvent": "solvent",
    "solute": "solute",
    "solution": "solution",
    "aqueous solution": "aqueous_solution",
    "precipitate": "precipitate",
    "precipitation reaction": "precipitation_reaction",
    "precipitation reactions": "precipitation_reaction",
    "chemical equilibrium": "chemical_equilibrium",
    "chemical potential": "chemical_potential",
    "chemical potential energy": "chemical_potential_energy",
    "enthalpy of formation": "enthalpy_of_formation",
    "standard enthalpy": "standard_enthalpy",
    "standard enthalpy change": "standard_enthalpy_change",
    "standard temperature and pressure": "stp",
    "stp": "stp",
    "molar volume": "molar_volume",
    "molecular weight": "molecular_weight",
    "molecular geometry": "molecular_geometry",
    "molecular shape": "molecular_geometry",
    "valence electrons": "valence_electrons",
    "electron affinity": "electron_affinity",
    "ionization energy": "ionization_energy",
    "periodic law": "periodic_law",
    "periodic properties": "periodic_properties",
}

def normalize_query(text):
    """
    Normalize domain-specific terms in the input text.
    """
    text_lower = text.lower()
    # Sort keys by length descending to replace longer phrases first
    sorted_terms = sorted(DOMAIN_TERM_MAPPINGS.keys(), key=len, reverse=True)
    for term in sorted_terms:
        pattern = r'\b' + re.escape(term) + r'\b'
        replacement = DOMAIN_TERM_MAPPINGS[term]
        text_lower = re.sub(pattern, replacement, text_lower)
    return text_lower

# -------------------------
# DEEP ANALYSIS
# -------------------------

def multi_doctrine_decomposition(query):
    """
    Decompose query into sub-issues based on doctrine keywords.
    Returns list of sub-issues (strings).
    """
    # For chemistry, doctrines might be reaction types, principles, laws, etc.
    doctrine_keywords = [
        "acid-base", "redox", "stoichiometry", "equilibrium", "kinetics",
        "thermodynamics", "molecular structure", "bonding", "periodic trends",
        "solubility", "electrochemistry", "organic chemistry", "inorganic chemistry",
        "physical chemistry", "analytical chemistry", "nuclear chemistry",
        "spectroscopy", "polymer chemistry", "biochemistry", "reaction mechanism"
    ]
    query_norm = normalize_query(query)
    sub_issues = []
    for keyword in doctrine_keywords:
        norm_keyword = normalize_query(keyword)
        if norm_keyword in query_norm:
            sub_issues.append(keyword)
    if not sub_issues:
        # fallback: split by sentences or clauses
        sub_issues = re.split(r'[;,.]\s*', query)
    return list(filter(None, sub_issues))

def build_interaction_dag(issues):
    """
    Build a dependency graph (DAG) of issues.
    For simplicity, assume linear dependencies or based on keyword heuristics.
    Returns dict: {issue: [dependent_issues]}
    """
    dag = defaultdict(list)
    # Simple heuristic: if issue A contains words that appear in issue B, A -> B
    for i, issue_a in enumerate(issues):
        for j, issue_b in enumerate(issues):
            if i == j:
                continue
            words_a = set(issue_a.lower().split())
            words_b = set(issue_b.lower().split())
            if words_a & words_b and len(words_b) > len(words_a):
                dag[issue_a].append(issue_b)
    # Remove cycles and duplicates
    for key in dag:
        dag[key] = list(set(dag[key]))
    return dict(dag)

def eight_step_resolution(query, doctrines, sub_engine_results):
    """
    Perform a full analysis in 8 steps:
    1. Normalize query
    2. Decompose doctrines
    3. Build interaction DAG
    4. Dispatch sub-queries to sub-engines
    5. Collect sub-engine results
    6. Merge results resolving conflicts
    7. Apply epistemic guardrails
    8. Return final tagged analysis
    """
    normalized_query = normalize_query(query)
    decomposed_issues = doctrines or multi_doctrine_decomposition(normalized_query)
    dag = build_interaction_dag(decomposed_issues)

    # Step 4 & 5: sub_engine_results is input param, assumed dict {issue: result}
    # Step 6: merge results resolving conflicts (simplified)
    merged_results = {}
    for issue in decomposed_issues:
        results = sub_engine_results.get(issue, [])
        if not results:
            merged_results[issue] = "No data available."
            continue
        # Resolve conflicts by authority
        sources = []
        for res in results:
            lvl = res.get('authority_level', AuthorityLevel.PRACTICE)
            src_id = res.get('source_id', 'unknown')
            sources.append((lvl, src_id))
        dominant_level, dominant_sources = resolve_authority_conflict(sources)
        dominant_texts = [res['text'] for res in results if res.get('authority_level') == dominant_level]
        merged_text = " ".join(dominant_texts)
        merged_results[issue] = merged_text

    # Step 7: Apply epistemic guardrails to merged results
    guarded_results = {}
    for issue, text in merged_results.items():
        guarded_results[issue] = apply_epistemic_guardrails(text)

    # Step 8: Tag analysis zones (PLANNING/REPORTING/AUDIT)
    tagged_analysis = zoned_analysis(guarded_results)

    return tagged_analysis

def zoned_analysis(conclusion_dict):
    """
    Tag conclusions as PLANNING, REPORTING, or AUDIT based on keywords and context.
    Returns dict {issue: {'text': str, 'zone': str}}
    """
    planning_keywords = ['plan', 'strategy', 'propose', 'recommend', 'suggest', 'future']
    reporting_keywords = ['observed', 'measured', 'found', 'detected', 'reported', 'data']
    audit_keywords = ['verify', 'audit', 'check', 'validate', 'confirm', 'review']

    zones = {}
    for issue, text in conclusion_dict.items():
        text_lower = text.lower()
        score = {'PLANNING': 0, 'REPORTING': 0, 'AUDIT': 0}
        for kw in planning_keywords:
            if kw in text_lower:
                score['PLANNING'] += 1
        for kw in reporting_keywords:
            if kw in text_lower:
                score['REPORTING'] += 1
        for kw in audit_keywords:
            if kw in text_lower:
                score['AUDIT'] += 1
        max_zone = max(score, key=score.get)
        if score[max_zone] == 0:
            max_zone = 'REPORTING'  # default zone
        zones[issue] = {'text': text, 'zone': max_zone}
    return zones

# -------------------------
# THREE LAYER RESPONSE SYSTEM
# -------------------------

class DoctrineCache:
    """
    Simple in-memory cache for doctrine analyses keyed by keywords.
    """
    def __init__(self):
        self.cache = {}
        self.lock = threading.Lock()

    def lookup(self, keywords):
        """
        Lookup cache by keywords (list or set).
        Returns cached analysis or None.
        """
        key = tuple(sorted(set(keywords)))
        with self.lock:
            return self.cache.get(key)

    def store(self, keywords, analysis):
        key = tuple(sorted(set(keywords)))
        with self.lock:
            self.cache[key] = analysis

doctrine_cache = DoctrineCache()

def doctrine_cache_lookup(query, timeout_ms=200):
    """
    Layer 1: Attempt to find cached doctrine analysis within timeout.
    Returns cached analysis or None.
    """
    start = time.time()
    keywords = extract_keywords(query)
    cached = doctrine_cache.lookup(keywords)
    elapsed_ms = (time.time() - start) * 1000
    if elapsed_ms > timeout_ms:
        return None
    return cached

def extract_keywords(text):
    """
    Extract keywords from text for cache lookup.
    Simple heuristic: tokenize and filter stopwords.
    """
    stopwords = {
        'the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'of', 'for', 'in',
        'to', 'with', 'by', 'as', 'from', 'that', 'this', 'it', 'be', 'are',
        'was', 'were', 'or', 'but', 'if', 'then', 'else', 'when', 'while',
        'do', 'does', 'did', 'has', 'have', 'had', 'not', 'no', 'yes', 'can',
        'could', 'should', 'would', 'may', 'might', 'will', 'shall'
    }
    tokens = re.findall(r'\b\w+\b', text.lower())
    keywords = [t for t in tokens if t not in stopwords and len(t) > 2]
    return keywords

def semantic_search_and_route(query):
    """
    Layer 2: Semantic search + sub-engine routing.
    Returns dict {sub_engine_name: [sub_queries]}
    """
    # For simplicity, route based on normalized keywords matching sub-engine domains
    sub_engines = {
        'acid_base_engine': ['acid', 'base', 'ph', 'ka', 'kb', 'buffer'],
        'redox_engine': ['redox', 'oxidation', 'reduction', 'oxidizing_agent', 'reducing_agent'],
        'kinetics_engine': ['kinetics', 'rate_law', 'reaction_rate', 'activation_energy'],
        'thermodynamics_engine': ['enthalpy', 'entropy', 'gibbs_free_energy', 'exothermic', 'endothermic'],
        'equilibrium_engine': ['equilibrium', 'le_chatelier_principle', 'equilibrium_constant'],
        'bonding_engine': ['covalent_bond', 'ionic_bond', 'metallic_bond', 'molecular_orbital'],
        'periodic_table_engine': ['periodic_table', 'periodic_trend', 'electronegativity', 'atomic_radius'],
        'solubility_engine': ['solubility', 'precipitation', 'solvent', 'solute'],
        'organic_chemistry_engine': ['organic_chemistry', 'reaction_mechanism', 'functional_group'],
        'analytical_chemistry_engine': ['spectroscopy', 'chromatography', 'titration'],
    }
    query_norm = normalize_query(query)
    routing = defaultdict(list)
    for engine, keywords in sub_engines.items():
        for kw in keywords:
            if kw in query_norm:
                routing[engine].append(query)
                break
    if not routing:
        routing['general_engine'].append(query)
    return dict(routing)

def deep_multi_engine_analysis(query, sub_engines):
    """
    Layer 3: Parallel dispatch to multiple sub-engines, merge and resolve conflicts.
    sub_engines: dict {engine_name: [queries]}
    Returns merged analysis dict.
    """
    results = defaultdict(list)
    def run_engine(engine_name, queries):
        # Placeholder for actual sub-engine call
        # Simulate result with dummy data
        engine_results = []
        for q in queries:
            engine_results.append({
                'text': f"Analysis by {engine_name} on '{q}'",
                'authority_level': AuthorityLevel.STATUTORY,
                'source_id': f"{engine_name}_source_1"
            })
        return engine_results

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_engine = {executor.submit(run_engine, eng, qs): eng for eng, qs in sub_engines.items()}
        for future in as_completed(future_to_engine):
            eng = future_to_engine[future]
            try:
                res = future.result()
                results[eng].extend(res)
            except Exception:
                results[eng] = []

    # Merge results by engine name
    merged_texts = []
    for eng, res_list in results.items():
        texts = [r['text'] for r in res_list]
        merged_texts.append(" ".join(texts))

    merged_analysis = " ".join(merged_texts)
    # Apply epistemic guardrails on merged text
    guarded_analysis = apply_epistemic_guardrails(merged_analysis)
    return guarded_analysis

def three_layer_response_system(query):
    """
    Implements the three-layer response system:
    Layer 1: Doctrine cache lookup
    Layer 2: Semantic search + sub-engine routing
    Layer 3: Deep multi-engine analysis
    Returns final analysis text.
    """
    # Layer 1
    cached = doctrine_cache_lookup(query)
    if cached:
        return cached

    # Layer 2
    routing = semantic_search_and_route(query)
    if len(routing) == 1 and 'general_engine' in routing:
        # If only general engine, skip to layer 3 with that
        analysis = deep_multi_engine_analysis(query, routing)
        doctrine_cache.store(extract_keywords(query), analysis)
        return analysis

    # Layer 3
    analysis = deep_multi_engine_analysis(query, routing)
    doctrine_cache.store(extract_keywords(query), analysis)
    return analysis

# -------------------------
# END OF PART 4
# -------------------------

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
        self._doctrine_hits: Counter = Counter()
        self._doctrine_total: Counter = Counter()
        self._sub_engine_stats: DefaultDict[str, List[float]] = defaultdict(list)
        self._sub_engine_errors: DefaultDict[str, int] = defaultdict(int)
        self._query_time_index: List[Tuple[float, int]] = []  # (timestamp, idx)
        self._query_id_map: Dict[str, int] = {}
        self._errors: List[Tuple[float, str, str]] = []  # (timestamp, query_id, error)
        self._cache_hits: int = 0
        self._cache_total: int = 0

    def record_query(self, telemetry: QueryTelemetry):
        with self._lock:
            idx = len(self._queries)
            self._queries.append(telemetry)
            self._query_time_index.append((telemetry.timestamp, idx))
            self._query_id_map[telemetry.query_id] = idx
            for engine in telemetry.engines_invoked:
                self._sub_engine_stats[engine].append(telemetry.latency_ms)
            if telemetry.cache_hit:
                self._cache_hits += 1
            self._cache_total += 1
            for engine in telemetry.engines_invoked:
                self._doctrine_hits[engine] += 1
            for engine in telemetry.engines_invoked:
                self._doctrine_total[engine] += 1
            if telemetry.error:
                for engine in telemetry.engines_invoked:
                    self._sub_engine_errors[engine] += 1

    def record_error(self, query_id: str, error: str):
        with self._lock:
            idx = self._query_id_map.get(query_id)
            if idx is not None:
                telemetry = self._queries[idx]
                self._queries[idx] = QueryTelemetry(
                    query_id=telemetry.query_id,
                    timestamp=telemetry.timestamp,
                    latency_ms=telemetry.latency_ms,
                    cache_hit=telemetry.cache_hit,
                    engines_invoked=telemetry.engines_invoked,
                    mode=telemetry.mode,
                    confidence=telemetry.confidence,
                    error=error
                )
                for engine in telemetry.engines_invoked:
                    self._sub_engine_errors[engine] += 1
            self._errors.append((time.time(), query_id, error))

    def get_latency_stats(self) -> Dict[str, float]:
        with self._lock:
            latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
            if not latencies:
                return dict(avg=0, p50=0, p95=0, p99=0, min=0, max=0)
            latencies.sort()
            n = len(latencies)
            avg = sum(latencies) / n
            p50 = latencies[int(0.5 * n)]
            p95 = latencies[int(0.95 * n)-1]
            p99 = latencies[int(0.99 * n)-1]
            return dict(
                avg=avg,
                p50=p50,
                p95=p95,
                p99=p99,
                min=latencies[0],
                max=latencies[-1]
            )

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        with self._lock:
            rates = {}
            for doctrine in self._doctrine_total:
                total = self._doctrine_total[doctrine]
                hits = self._doctrine_hits[doctrine]
                rates[doctrine] = hits / total if total else 0.0
            return rates

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        with self._lock:
            idx = bisect.bisect_left(self._query_time_index, (one_hour_ago, 0))
            return len(self._query_time_index) - idx

    def get_sub_engine_stats(self) -> Dict[str, Dict[str, float]]:
        with self._lock:
            stats = {}
            for engine, latencies in self._sub_engine_stats.items():
                if not latencies:
                    stats[engine] = dict(avg=0, p50=0, p95=0, p99=0, min=0, max=0, errors=0)
                    continue
                lats = sorted(latencies)
                n = len(lats)
                stats[engine] = dict(
                    avg=sum(lats)/n,
                    p50=lats[int(0.5*n)],
                    p95=lats[int(0.95*n)-1],
                    p99=lats[int(0.99*n)-1],
                    min=lats[0],
                    max=lats[-1],
                    errors=self._sub_engine_errors[engine]
                )
            return stats

# --- 2. DRIFT_WATCHER ---

class DriftWatcher:
    def __init__(self):
        self._lock = threading.Lock()
        self._baselines: Dict[str, float] = {}  # doctrine -> baseline_confidence
        self._history: DefaultDict[str, deque] = defaultdict(lambda: deque(maxlen=1000))  # doctrine -> deque of (timestamp, confidence)
        self._alerts: List[Tuple[float, str, float, float]] = []  # (timestamp, doctrine, baseline, current)

    def record_baseline(self, doctrine: str, baseline_confidence: float):
        with self._lock:
            self._baselines[doctrine] = baseline_confidence

    def record_confidence(self, doctrine: str, confidence: float):
        with self._lock:
            now = time.time()
            self._history[doctrine].append((now, confidence))
            baseline = self._baselines.get(doctrine)
            if baseline is not None:
                recent = [c for t, c in self._history[doctrine] if t > now - 3600]
                if recent:
                    avg_recent = sum(recent) / len(recent)
                    drift = abs(avg_recent - baseline) / (baseline if baseline else 1)
                    if drift > 0.1:
                        self._alerts.append((now, doctrine, baseline, avg_recent))

    def detect_drift(self, doctrine: str) -> Optional[float]:
        with self._lock:
            baseline = self._baselines.get(doctrine)
            if baseline is None:
                return None
            now = time.time()
            recent = [c for t, c in self._history[doctrine] if t > now - 3600]
            if not recent:
                return None
            avg_recent = sum(recent) / len(recent)
            drift = (avg_recent - baseline) / (baseline if baseline else 1)
            return drift

    def get_drift_report(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            report = {}
            for doctrine in self._baselines:
                baseline = self._baselines[doctrine]
                now = time.time()
                recent = [c for t, c in self._history[doctrine] if t > now - 3600]
                if recent:
                    avg_recent = sum(recent) / len(recent)
                    drift = (avg_recent - baseline) / (baseline if baseline else 1)
                else:
                    avg_recent = None
                    drift = None
                report[doctrine] = dict(
                    baseline=baseline,
                    avg_recent=avg_recent,
                    drift=drift
                )
            report['alerts'] = list(self._alerts)
            return report

# --- 3. COVERAGE_MAP ---

class CoverageTracker:
    def __init__(self):
        self._lock = threading.Lock()
        self._doctrine_triggered: Counter = Counter()
        self._doctrine_missed: Counter = Counter()
        self._missed_queries: List[Tuple[str, float]] = []  # (query_id, timestamp)
        self._query_to_doctrines: Dict[str, Set[str]] = {}
        self._sub_engine_coverage: DefaultDict[str, Counter] = defaultdict(Counter)

    def record_triggered(self, query_id: str, doctrines: List[str], sub_engines: List[str]):
        with self._lock:
            self._query_to_doctrines[query_id] = set(doctrines)
            for doctrine in doctrines:
                self._doctrine_triggered[doctrine] += 1
            for se in sub_engines:
                self._sub_engine_coverage[se]['triggered'] += 1

    def record_missed(self, query_id: str, timestamp: Optional[float] = None, sub_engines: Optional[List[str]] = None):
        with self._lock:
            self._missed_queries.append((query_id, timestamp or time.time()))
            for se in (sub_engines or []):
                self._sub_engine_coverage[se]['missed'] += 1

    def get_coverage_report(self) -> Dict[str, Any]:
        with self._lock:
            total = sum(self._doctrine_triggered.values()) + sum(self._doctrine_missed.values())
            doctrine_coverage = {}
            for doctrine in set(list(self._doctrine_triggered.keys()) + list(self._doctrine_missed.keys())):
                triggered = self._doctrine_triggered[doctrine]
                missed = self._doctrine_missed[doctrine]
                doctrine_coverage[doctrine] = dict(
                    triggered=triggered,
                    missed=missed,
                    coverage=triggered / (triggered + missed) if (triggered + missed) else 0.0
                )
            epistemic_gap = [q for q, _ in self._missed_queries if not self._query_to_doctrines.get(q)]
            sub_engine_stats = {}
            for se, ctr in self._sub_engine_coverage.items():
                trig = ctr['triggered']
                miss = ctr['missed']
                sub_engine_stats[se] = dict(
                    triggered=trig,
                    missed=miss,
                    coverage=trig / (trig + miss) if (trig + miss) else 0.0
                )
            return dict(
                doctrine_coverage=doctrine_coverage,
                epistemic_gap=epistemic_gap,
                sub_engine_coverage=sub_engine_stats
            )

    def identify_epistemic_gap(self) -> List[str]:
        with self._lock:
            return [q for q, _ in self._missed_queries if not self._query_to_doctrines.get(q)]

# --- 4. DETERMINISM_HASH ---

def compute_determinism_hash(query: Any, response: Any) -> str:
    def canonicalize(obj):
        if isinstance(obj, dict):
            return {k: canonicalize(obj[k]) for k in sorted(obj)}
        elif isinstance(obj, list):
            return [canonicalize(x) for x in obj]
        elif isinstance(obj, float):
            # Round floats for stability
            return round(obj, 8)
        else:
            return obj
    canonical = dict(
        query=canonicalize(query),
        response=canonicalize(response)
    )
    s = json.dumps(canonical, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def verify_reproducibility(query: Any, response: Any, expected_hash: str) -> bool:
    return compute_determinism_hash(query, response) == expected_hash

# --- 5. AUDIT_TRAIL ---

class AuditTrailWriter:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self._lock = threading.Lock()
        self._current_date = None
        self._file = None
        self._file_path = None
        self._open_file()

    def _get_today(self):
        return datetime.datetime.utcnow().strftime('%Y-%m-%d')

    def _open_file(self):
        with self._lock:
            today = self._get_today()
            if self._current_date != today:
                if self._file:
                    self._file.close()
                self._current_date = today
                os.makedirs(self.base_dir, exist_ok=True)
                self._file_path = os.path.join(self.base_dir, f'audit_{today}.jsonl')
                self._file = open(self._file_path, 'a', encoding='utf-8')

    def write(self, query_id: str, timestamp: float, engine_id: str, engines_invoked: List[str], mode: str,
              confidence: float, latency: float, cache_hit: bool):
        self._open_file()
        entry = dict(
            query_id=query_id,
            timestamp=timestamp,
            engine_id=engine_id,
            engines_invoked=engines_invoked,
            mode=mode,
            confidence=confidence,
            latency=latency,
            cache_hit=cache_hit
        )
        with self._lock:
            self._file.write(json.dumps(entry, separators=(',', ':')) + '\n')
            self._file.flush()

    def forensic_replay(self, date: Optional[str] = None) -> List[Dict[str, Any]]:
        if date is None:
            date = self._get_today()
        path = os.path.join(self.base_dir, f'audit_{date}.jsonl')
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
    def __init__(self):
        self._lock = threading.Lock()
        self._latency: DefaultDict[str, List[float]] = defaultdict(list)
        self._errors: DefaultDict[str, int] = defaultdict(int)
        self._invocations: DefaultDict[str, int] = defaultdict(int)
        self._availability: DefaultDict[str, List[Tuple[float, bool]]] = defaultdict(list)  # (timestamp, available)

    def record(self, sub_engine: str, latency_ms: float, error: Optional[str], available: bool):
        with self._lock:
            self._latency[sub_engine].append(latency_ms)
            self._invocations[sub_engine] += 1
            if error:
                self._errors[sub_engine] += 1
            self._availability[sub_engine].append((time.time(), available))

    def get_latency_stats(self, sub_engine: str) -> Dict[str, float]:
        with self._lock:
            lats = self._latency[sub_engine]
            if not lats:
                return dict(avg=0, p50=0, p95=0, p99=0, min=0, max=0)
            lats_sorted = sorted(lats)
            n = len(lats_sorted)
            return dict(
                avg=sum(lats_sorted)/n,
                p50=lats_sorted[int(0.5*n)],
                p95=lats_sorted[int(0.95*n)-1],
                p99=lats_sorted[int(0.99*n)-1],
                min=lats_sorted[0],
                max=lats_sorted[-1]
            )

    def get_error_rate(self, sub_engine: str) -> float:
        with self._lock:
            inv = self._invocations[sub_engine]
            err = self._errors[sub_engine]
            return err / inv if inv else 0.0

    def get_availability(self, sub_engine: str, window_sec: int = 3600) -> float:
        with self._lock:
            now = time.time()
            records = [avail for t, avail in self._availability[sub_engine] if t > now - window_sec]
            if not records:
                return 1.0
            return sum(1 for a in records if a) / len(records)

    def get_sla_report(self, sla_latency_ms: float, sla_availability: float, sla_error_rate: float) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            report = {}
            for se in self._latency:
                lats = self._latency[se]
                if lats:
                    avg_latency = sum(lats) / len(lats)
                else:
                    avg_latency = 0
                error_rate = self.get_error_rate(se)
                availability = self.get_availability(se)
                report[se] = dict(
                    avg_latency=avg_latency,
                    error_rate=error_rate,
                    availability=availability,
                    sla_latency_met=avg_latency <= sla_latency_ms,
                    sla_error_rate_met=error_rate <= sla_error_rate,
                    sla_availability_met=availability >= sla_availability
                )
            return report

# --- END OF PART 5 ---

ENGINE_ID = "CHEMIE"
ENGINE_PORT = 8852

SUB_ENGINES = {
    "CHEM01": "Organic Synthesis",
    "CHEM02": "Analytical Methods",
    "CHEM03": "Polymer Science",
    "CHEM04": "Electrochemistry",
    "CHEM05": "Thermodynamics",
    "CHEM06": "Kinetics",
    "CHEM07": "Spectroscopy",
    "CHEM08": "Crystallography",
    "CHEM09": "Computational Chemistry",
    "CHEM10": "Environmental Chemistry",
    "CHEM11": "Inorganic Chemistry",
    "CHEM12": "Biochemistry",
    "CHEM13": "Materials Science",
    "CHEM14": "Nuclear Chemistry",
    "CHEM15": "Surface Chemistry",
    "CHEM16": "Photochemistry",
    "CHEM17": "Geochemistry",
    "CHEM18": "Food Chemistry",
    "CHEM19": "Forensic Chemistry",
    "CHEM20": "Industrial Chemistry",
}

# ---------------------------
# Logging Setup
# ---------------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("CHEMIE-Orchestrator")

# ---------------------------
# Data Models
# ---------------------------

class QueryRequest(BaseModel):
    query: str
    options: Optional[Dict[str, Any]] = None

class RouteDryRunRequest(BaseModel):
    query: str

class AnalyzeRequest(BaseModel):
    query: str
    depth: Optional[int] = 3
    options: Optional[Dict[str, Any]] = None

class SubEngineResponse(BaseModel):
    engine_id: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    latency_ms: Optional[int] = None

class HealthStatus(BaseModel):
    status: str
    details: Optional[Dict[str, Any]] = None

class MetricsResponse(BaseModel):
    latency_ms_avg: float
    latency_ms_p95: float
    cache_hit_rate: float
    queries_per_hour: float
    sub_engine_metrics: Dict[str, Dict[str, Any]]

class CoverageReport(BaseModel):
    doctrine_coverage_percent: float
    epistemic_gaps: List[str]

class DriftReport(BaseModel):
    drift_detected: bool
    drift_score: float
    details: Optional[Dict[str, Any]] = None

class DoctrineInfo(BaseModel):
    doctrine_id: str
    description: str
    last_updated: str

class RoutingInfo(BaseModel):
    routing_rules: Dict[str, Any]
    engine_registry: Dict[str, str]

class SubEngineHealth(BaseModel):
    engine_id: str
    status: str
    last_checked: str
    latency_ms: Optional[int] = None
    error: Optional[str] = None

# ---------------------------
# Global State and Cache
# ---------------------------

class DoctrineCache:
    def __init__(self):
        self._cache = {}
        self._lock = asyncio.Lock()

    async def initialize(self):
        # Simulate loading doctrines from DB or file
        await asyncio.sleep(0.5)
        doctrines = {
            f"doctrine_{i}": {
                "id": f"doctrine_{i}",
                "description": f"Doctrine description {i}",
                "content": f"Some chemistry knowledge content {i}",
                "last_updated": datetime.utcnow().isoformat()
            }
            for i in range(1, 101)
        }
        async with self._lock:
            self._cache = doctrines
        logger.info("Doctrine cache initialized with %d doctrines", len(doctrines))

    async def get_doctrine(self, doctrine_id: str) -> Optional[Dict[str, Any]]:
        async with self._lock:
            return self._cache.get(doctrine_id)

    async def list_doctrines(self) -> List[DoctrineInfo]:
        async with self._lock:
            return [
                DoctrineInfo(
                    doctrine_id=d["id"],
                    description=d["description"],
                    last_updated=d["last_updated"]
                ) for d in self._cache.values()
            ]

    async def coverage_report(self) -> CoverageReport:
        # Simulate coverage calculation
        total = 100
        covered = random.randint(80, 95)
        gaps = [f"Gap in topic {i}" for i in range(1, total - covered + 1)]
        return CoverageReport(
            doctrine_coverage_percent=covered,
            epistemic_gaps=gaps
        )

doctrine_cache = DoctrineCache()

# ---------------------------
# Health Monitor
# ---------------------------

class HealthMonitor:
    def __init__(self):
        self._statuses = {}
        self._lock = asyncio.Lock()
        self._running = False
        self._task = None

    async def start(self):
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._monitor_loop())
            logger.info("Health monitor started")

    async def stop(self):
        self._running = False
        if self._task:
            await self._task
            logger.info("Health monitor stopped")

    async def _monitor_loop(self):
        while self._running:
            await self._check_all_sub_engines()
            await asyncio.sleep(10)

    async def _check_all_sub_engines(self):
        results = {}
        for engine_id in SUB_ENGINES.keys():
            try:
                # Simulate health check latency and random failures
                latency = random.randint(10, 100)
                await asyncio.sleep(latency / 1000)
                if random.random() < 0.05:
                    raise Exception("Simulated failure")
                status = "healthy"
                error = None
            except Exception as e:
                status = "unhealthy"
                error = str(e)
                latency = None
            results[engine_id] = {
                "status": status,
                "last_checked": datetime.utcnow().isoformat(),
                "latency_ms": latency,
                "error": error
            }
        async with self._lock:
            self._statuses = results

    async def get_status(self, engine_id: str) -> SubEngineHealth:
        async with self._lock:
            s = self._statuses.get(engine_id)
            if not s:
                return SubEngineHealth(
                    engine_id=engine_id,
                    status="unknown",
                    last_checked="never",
                    latency_ms=None,
                    error="No data"
                )
            return SubEngineHealth(
                engine_id=engine_id,
                status=s["status"],
                last_checked=s["last_checked"],
                latency_ms=s["latency_ms"],
                error=s["error"]
            )

    async def get_all_statuses(self) -> List[SubEngineHealth]:
        async with self._lock:
            return [
                SubEngineHealth(
                    engine_id=eid,
                    status=info["status"],
                    last_checked=info["last_checked"],
                    latency_ms=info["latency_ms"],
                    error=info["error"]
                ) for eid, info in self._statuses.items()
            ]

health_monitor = HealthMonitor()

# ---------------------------
# Telemetry and Metrics
# ---------------------------

class Telemetry:
    def __init__(self):
        self._latencies = deque(maxlen=1000)
        self._cache_hits = 0
        self._cache_misses = 0
        self._query_timestamps = deque(maxlen=3600)  # store timestamps of last hour queries
        self._sub_engine_stats = defaultdict(lambda: {
            "calls": 0,
            "failures": 0,
            "avg_latency_ms": 0.0
        })
        self._lock = asyncio.Lock()

    async def record_latency(self, latency_ms: int):
        async with self._lock:
            self._latencies.append(latency_ms)

    async def record_cache_hit(self):
        async with self._lock:
            self._cache_hits += 1

    async def record_cache_miss(self):
        async with self._lock:
            self._cache_misses += 1

    async def record_query(self):
        async with self._lock:
            self._query_timestamps.append(datetime.utcnow())

    async def record_sub_engine_call(self, engine_id: str, latency_ms: Optional[int], success: bool):
        async with self._lock:
            stats = self._sub_engine_stats[engine_id]
            stats["calls"] += 1
            if not success:
                stats["failures"] += 1
            if latency_ms is not None:
                # Update average latency with simple moving average
                prev_avg = stats["avg_latency_ms"]
                n = stats["calls"]
                stats["avg_latency_ms"] = (prev_avg * (n - 1) + latency_ms) / n

    async def get_metrics(self) -> MetricsResponse:
        async with self._lock:
            latencies = list(self._latencies)
            if latencies:
                avg_latency = sum(latencies) / len(latencies)
                p95_latency = sorted(latencies)[int(len(latencies)*0.95)-1]
            else:
                avg_latency = 0.0
                p95_latency = 0.0
            total_cache = self._cache_hits + self._cache_misses
            cache_hit_rate = (self._cache_hits / total_cache) if total_cache > 0 else 0.0
            now = datetime.utcnow()
            one_hour_ago = now - timedelta(hours=1)
            queries_last_hour = [t for t in self._query_timestamps if t > one_hour_ago]
            qph = len(queries_last_hour)
            sub_engine_metrics = dict(self._sub_engine_stats)
            return MetricsResponse(
                latency_ms_avg=avg_latency,
                latency_ms_p95=p95_latency,
                cache_hit_rate=cache_hit_rate,
                queries_per_hour=qph,
                sub_engine_metrics=sub_engine_metrics
            )

telemetry = Telemetry()

# ---------------------------
# Search Index (Seed)
# ---------------------------

class SearchIndex:
    def __init__(self):
        self._index = {}
        self._lock = asyncio.Lock()

    async def seed(self):
        # Simulate seeding index with doctrine cache content
        doctrines = await doctrine_cache.list_doctrines()
        async with self._lock:
            self._index = {d.doctrine_id: d.description for d in doctrines}
        logger.info("Search index seeded with %d entries", len(self._index))

    async def search(self, query: str) -> List[str]:
        # Simple substring search simulation
        async with self._lock:
            results = [k for k, v in self._index.items() if query.lower() in v.lower()]
        return results

search_index = SearchIndex()

# ---------------------------
# Drift Detection
# ---------------------------

class DriftDetector:
    def __init__(self):
        self._last_drift_score = 0.0
        self._lock = asyncio.Lock()

    async def detect(self) -> DriftReport:
        # Simulate drift detection with random score
        await asyncio.sleep(0.1)
        score = random.uniform(0, 1)
        drifted = score > 0.7
        async with self._lock:
            self._last_drift_score = score
        return DriftReport(
            drift_detected=drifted,
            drift_score=score,
            details={"threshold": 0.7}
        )

drift_detector = DriftDetector()

# ---------------------------
# Routing Rules and Engine Registry
# ---------------------------

class Router:
    def __init__(self):
        # Example routing rules by keywords (very simplified)
        self._rules = {
            "synthesis": ["CHEM01"],
            "analysis": ["CHEM02"],
            "polymer": ["CHEM03"],
            "electro": ["CHEM04"],
            "thermo": ["CHEM05"],
            "kinetic": ["CHEM06"],
            "spectro": ["CHEM07"],
            "crystal": ["CHEM08"],
            "compute": ["CHEM09"],
            "environment": ["CHEM10"],
            "inorganic": ["CHEM11"],
            "bio": ["CHEM12"],
            "material": ["CHEM13"],
            "nuclear": ["CHEM14"],
            "surface": ["CHEM15"],
            "photo": ["CHEM16"],
            "geo": ["CHEM17"],
            "food": ["CHEM18"],
            "forensic": ["CHEM19"],
            "industrial": ["CHEM20"],
        }
        self._engine_registry = SUB_ENGINES.copy()

    async def classify(self, query: str) -> List[str]:
        # Simple keyword-based classification
        query_lower = query.lower()
        matched_engines = set()
        for keyword, engines in self._rules.items():
            if keyword in query_lower:
                matched_engines.update(engines)
        if not matched_engines:
            # Fallback to all engines if no keyword matched
            matched_engines = set(self._engine_registry.keys())
        return list(matched_engines)

    async def route(self, classified_engines: List[str]) -> List[str]:
        # For now routing is direct from classification
        return classified_engines

    async def get_routing_info(self) -> RoutingInfo:
        return RoutingInfo(
            routing_rules=self._rules,
            engine_registry=self._engine_registry
        )

router = Router()

# ---------------------------
# Sub-Engine Dispatcher
# ---------------------------

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_time_sec=30):
        self.failure_threshold = failure_threshold
        self.recovery_time_sec = recovery_time_sec
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF-OPEN

    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_failure_time = None

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

    def can_call(self):
        if self.state == "OPEN":
            if self.last_failure_time and (datetime.utcnow() - self.last_failure_time).total_seconds() > self.recovery_time_sec:
                self.state = "HALF-OPEN"
                return True
            return False
        return True

circuit_breakers = {eid: CircuitBreaker() for eid in SUB_ENGINES.keys()}

async def call_sub_engine(engine_id: str, query: str, timeout_sec=2) -> SubEngineResponse:
    cb = circuit_breakers.get(engine_id)
    if cb and not cb.can_call():
        return SubEngineResponse(
            engine_id=engine_id,
            success=False,
            error="Circuit breaker open",
            latency_ms=None
        )
    start = time.perf_counter()
    try:
        # Simulate sub-engine call with random latency and failure
        simulated_latency = random.uniform(0.1, 1.5)
        if simulated_latency > timeout_sec:
            raise asyncio.TimeoutError("Timeout")
        await asyncio.sleep(simulated_latency)
        if random.random() < 0.1:
            raise Exception("Simulated sub-engine failure")
        # Simulated response data
        data = {
            "engine": engine_id,
            "result": f"Processed query '{query[:30]}...' with engine {engine_id}"
        }
        latency_ms = int((time.perf_counter() - start) * 1000)
        cb.record_success()
        await telemetry.record_sub_engine_call(engine_id, latency_ms, True)
        return SubEngineResponse(
            engine_id=engine_id,
            success=True,
            data=data,
            latency_ms=latency_ms
        )
    except asyncio.TimeoutError as e:
        latency_ms = int((time.perf_counter() - start) * 1000)
        cb.record_failure()
        await telemetry.record_sub_engine_call(engine_id, latency_ms, False)
        return SubEngineResponse(
            engine_id=engine_id,
            success=False,
            error="Timeout",
            latency_ms=latency_ms
        )
    except Exception as e:
        latency_ms = int((time.perf_counter() - start) * 1000)
        cb.record_failure()
        await telemetry.record_sub_engine_call(engine_id, latency_ms, False)
        return SubEngineResponse(
            engine_id=engine_id,
            success=False,
            error=str(e),
            latency_ms=latency_ms
        )

# ---------------------------
# Query Processing Pipeline
# ---------------------------

async def normalize_query(query: str) -> str:
    # Basic normalization: strip, lowercase, remove extra spaces
    normalized = ' '.join(query.strip().lower().split())
    return normalized

async def classify_query(query: str) -> List[str]:
    return await router.classify(query)

async def route_query(classified_engines: List[str]) -> List[str]:
    return await router.route(classified_engines)

async def dispatch_query(routed_engines: List[str], query: str) -> List[SubEngineResponse]:
    tasks = []
    for engine_id in routed_engines:
        tasks.append(call_sub_engine(engine_id, query))
    responses = await asyncio.gather(*tasks, return_exceptions=False)
    return responses

async def merge_responses(responses: List[SubEngineResponse]) -> Dict[str, Any]:
    merged = {
        "results": [],
        "errors": []
    }
    for resp in responses:
        if resp.success and resp.data:
            merged["results"].append(resp.data)
        elif resp.error:
            merged["errors"].append({
                "engine_id": resp.engine_id,
                "error": resp.error
            })
    return merged

async def apply_guardrails(merged_response: Dict[str, Any]) -> Dict[str, Any]:
    # Example guardrail: limit number of results to 10
    if "results" in merged_response:
        merged_response["results"] = merged_response["results"][:10]
    return merged_response

async def hash_response(response: Dict[str, Any]) -> str:
    # Hash the response JSON string for logging
    import json
    response_str = json.dumps(response, sort_keys=True)
    return hashlib.sha256(response_str.encode('utf-8')).hexdigest()

async def log_query(query: str, response_hash: str, routed_engines: List[str], latency_ms: int):
    logger.info(f"Query processed: hash={response_hash}, engines={routed_engines}, latency_ms={latency_ms}, query='{query[:50]}'")

async def fallback_to_doctrine_cache(query: str) -> Dict[str, Any]:
    # Simulate fallback by searching doctrine cache
    results = await search_index.search(query)
    return {"fallback_results": results}

# ---------------------------
# FastAPI Application Setup
# ---------------------------

app = FastAPI(title="Chemistry Intelligence Engine - Domain Orchestrator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Lifespan Management
# ---------------------------

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Chemistry Intelligence Engine Orchestrator...")
    await doctrine_cache.initialize()
    await search_index.seed()
    await health_monitor.start()
    # Telemetry could have startup logic if needed
    logger.info("Startup complete.")
    yield
    # Shutdown
    logger.info("Shutting down Chemistry Intelligence Engine Orchestrator...")
    await health_monitor.stop()
    logger.info("Shutdown complete.")

app.router.lifespan_context = lifespan

# ---------------------------
# API Endpoints
# ---------------------------

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    start_time = time.perf_counter()
    query_raw = request.query
    try:
        # Normalize
        query_norm = await normalize_query(query_raw)
        # Classify
        classified_engines = await classify_query(query_norm)
        # Route
        routed_engines = await route_query(classified_engines)
        # Dispatch
        responses = await dispatch_query(routed_engines, query_norm)
        # Merge
        merged = await merge_responses(responses)
        # Guardrails
        guarded = await apply_guardrails(merged)
        # Hash
        response_hash = await hash_response(guarded)
        # Log
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        await log_query(query_norm, response_hash, routed_engines, latency_ms)
        # Telemetry
        await telemetry.record_latency(latency_ms)
        await telemetry.record_query()
        # Cache hit/miss simulation: if any sub-engine succeeded, count as miss, else hit
        if any(r.success for r in responses):
            await telemetry.record_cache_miss()
        else:
            await telemetry.record_cache_hit()
            # Fallback to doctrine cache
            fallback_results = await fallback_to_doctrine_cache(query_norm)
            guarded["fallback"] = fallback_results
        return JSONResponse(content=guarded)
    except Exception as e:
        logger.error(f"Error processing query: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_endpoint():
    # Self health
    self_health = HealthStatus(status="healthy")
    # Sub-engines health
    sub_health_list = await health_monitor.get_all_statuses()
    sub_health = {h.engine_id: h.status for h in sub_health_list}
    return {
        "engine_id": ENGINE_ID,
        "status": self_health.status,
        "sub_engines": sub_health
    }

@app.get("/metrics")
async def metrics_endpoint():
    metrics = await telemetry.get_metrics()
    return metrics.dict()

@app.get("/coverage")
async def coverage_endpoint():
    coverage = await doctrine_cache.coverage_report()
    return coverage.dict()

@app.get("/drift")
async def drift_endpoint():
    drift = await drift_detector.detect()
    return drift.dict()

@app.get("/doctrines")
async def doctrines_endpoint():
    doctrines = await doctrine_cache.list_doctrines()
    return [d.dict() for d in doctrines]

@app.get("/routing")
async def routing_endpoint():
    routing_info = await router.get_routing_info()
    return routing_info.dict()

@app.get("/sub-engines")
async def sub_engines_endpoint():
    statuses = await health_monitor.get_all_statuses()
    return [s.dict() for s in statuses]

@app.post("/route")
async def route_dry_run_endpoint(request: RouteDryRunRequest):
    query_norm = await normalize_query(request.query)
    classified = await classify_query(query_norm)
    routed = await route_query(classified)
    return {
        "query": request.query,
        "normalized_query": query_norm,
        "classified_engines": classified,
        "routed_engines": routed
    }

@app.post("/analyze")
async def analyze_endpoint(request: AnalyzeRequest):
    query_norm = await normalize_query(request.query)
    depth = request.depth or 3
    options = request.options or {}

    analysis_results = []

    # For demonstration, perform multiple rounds of classification, routing, dispatch, merge
    current_query = query_norm
    for i in range(depth):
        classified = await classify_query(current_query)
        routed = await route_query(classified)
        responses = await dispatch_query(routed, current_query)
        merged = await merge_responses(responses)
        guarded = await apply_guardrails(merged)
        analysis_results.append({
            "round": i+1,
            "classified": classified,
            "routed": routed,
            "merged": guarded
        })
        # For next round, simulate refining query by appending some info
        current_query += " " + " ".join(classified)

    return {
        "original_query": request.query,
        "normalized_query": query_norm,
        "depth": depth,
        "analysis": analysis_results
    }

# ---------------------------
# Error Handlers
# ---------------------------

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error"}
    )

# ---------------------------
# Server Startup
# ---------------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=ENGINE_PORT, log_level="info")