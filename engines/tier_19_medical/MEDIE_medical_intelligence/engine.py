import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hashlib
import uuid
import dataclasses
import typing
from typing import List, Dict, Optional, Any, Union
import enum
import datetime
import asyncio
import aiohttp
import json
import time
import statistics
import collections
from fastapi import FastAPI
from pydantic import BaseModel, Field
from loguru import logger

# Engine Constants
ENGINE_ID = "MEDIE"
ENGINE_PORT = 8856
ENGINE_NAME = "Medical Intelligence Engine — Domain Orchestrator"
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
    DRUG_INTERACTION = "DRUG_INTERACTION"
    TOXIC_EXPOSURE = "TOXIC_EXPOSURE"
    EMERGENCY_TRIAGE = "EMERGENCY_TRIAGE"
    RADIOLOGY_FINDING = "RADIOLOGY_FINDING"
    PATHOLOGY_DIAGNOSIS = "PATHOLOGY_DIAGNOSIS"
    INFECTION_CONTROL = "INFECTION_CONTROL"
    SURGICAL_COMPLICATION = "SURGICAL_COMPLICATION"
    CARDIAC_EVENT = "CARDIAC_EVENT"
    NEUROLOGICAL_DEFICIT = "NEUROLOGICAL_DEFICIT"
    ONCOLOGY_STAGE = "ONCOLOGY_STAGE"
    PEDIATRIC_ALERT = "PEDIATRIC_ALERT"
    OBSTETRIC_RISK = "OBSTETRIC_RISK"
    PSYCHIATRIC_EMERGENCY = "PSYCHIATRIC_EMERGENCY"
    ORTHOPEDIC_INJURY = "ORTHOPEDIC_INJURY"
    DERMATOLOGIC_LESION = "DERMATOLOGIC_LESION"
    GASTROINTESTINAL_BLEED = "GASTROINTESTINAL_BLEED"
    RENAL_FAILURE = "RENAL_FAILURE"
    PULMONARY_EMBOLISM = "PULMONARY_EMBOLISM"
    ENDOCRINE_CRISIS = "ENDOCRINE_CRISIS"
    IMMUNOLOGIC_REACTION = "IMMUNOLOGIC_REACTION"
    GENETIC_VARIANT = "GENETIC_VARIANT"
    MEDICATION_ERROR = "MEDICATION_ERROR"
    LABORATORY_ALERT = "LABORATORY_ALERT"
    VITAL_SIGN_ABNORMALITY = "VITAL_SIGN_ABNORMALITY"
    PROCEDURAL_COMPLICATION = "PROCEDURAL_COMPLICATION"
    SYSTEMIC_INFLAMMATION = "SYSTEMIC_INFLAMMATION"
    TRANSFUSION_REACTION = "TRANSFUSION_REACTION"
    HEMATOLOGIC_DISORDER = "HEMATOLOGIC_DISORDER"
    AUTOIMMUNE_EVENT = "AUTOIMMUNE_EVENT"
    INFANT_DISTRESS = "INFANT_DISTRESS"
    MATERNAL_HEALTH = "MATERNAL_HEALTH"
    MENTAL_STATUS_CHANGE = "MENTAL_STATUS_CHANGE"
    FRACTURE_RISK = "FRACTURE_RISK"
    SKIN_INFECTION = "SKIN_INFECTION"
    LIVER_DYSFUNCTION = "LIVER_DYSFUNCTION"
    SEPSIS_ALERT = "SEPSIS_ALERT"
    CARDIAC_ARREST = "CARDIAC_ARREST"
    RESPIRATORY_FAILURE = "RESPIRATORY_FAILURE"
    CANCER_PROGRESSION = "CANCER_PROGRESSION"
    PEDIATRIC_GROWTH = "PEDIATRIC_GROWTH"
    OBSTETRIC_LABOR = "OBSTETRIC_LABOR"
    SUICIDAL_IDEATION = "SUICIDAL_IDEATION"
    JOINT_DISLOCATION = "JOINT_DISLOCATION"
    ALLERGIC_REACTION = "ALLERGIC_REACTION"
    GASTRIC_ULCER = "GASTRIC_ULCER"
    KIDNEY_STONE = "KIDNEY_STONE"
    ASTHMA_EXACERBATION = "ASTHMA_EXACERBATION"
    DIABETIC_KETOACIDOSIS = "DIABETIC_KETOACIDOSIS"
    IMMUNODEFICIENCY = "IMMUNODEFICIENCY"
    GENETIC_SCREENING = "GENETIC_SCREENING"

class SubEngineStatus(enum.Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

# Pydantic Models

class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
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
    sub_engine_id: str
    result: Any
    status: str
    latency_ms: float
    confidence: float
    issue_category: Optional[IssueCategory] = None
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    orchestration_trace: Optional[List[str]] = None
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
    rule_id: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    trace: Optional[List[str]] = None

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decision: RoutingDecision
    responses: List[QueryResponse]
    overall_status: str
    orchestration_latency_ms: float
    errors: Optional[List[str]] = None
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

# Sub-Engine Registry

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "MED01": SubEngineConfig(
        engine_id="MED01",
        name="Pharmacology Engine",
        port=8857,
        health_url="http://localhost:8857/health",
        capabilities=["drug_interaction", "medication_error", "pharmacokinetics", "pharmacodynamics"],
        weight=1.0,
        domains=["pharmacology", "medication", "drug", "prescription", "dose", "side effect"]
    ),
    "MED02": SubEngineConfig(
        engine_id="MED02",
        name="Toxicology Engine",
        port=8858,
        health_url="http://localhost:8858/health",
        capabilities=["toxic_exposure", "poisoning", "overdose", "antidote"],
        weight=1.0,
        domains=["toxicology", "poison", "overdose", "toxicity", "antidote", "intoxication"]
    ),
    "MED03": SubEngineConfig(
        engine_id="MED03",
        name="Emergency Medicine Engine",
        port=8859,
        health_url="http://localhost:8859/health",
        capabilities=["emergency_triage", "resuscitation", "trauma", "shock"],
        weight=1.0,
        domains=["emergency", "triage", "resuscitation", "trauma", "shock", "code blue"]
    ),
    "MED04": SubEngineConfig(
        engine_id="MED04",
        name="Radiology Engine",
        port=8860,
        health_url="http://localhost:8860/health",
        capabilities=["radiology_finding", "imaging", "xray", "ct", "mri"],
        weight=1.0,
        domains=["radiology", "imaging", "xray", "ct", "mri", "ultrasound"]
    ),
    "MED05": SubEngineConfig(
        engine_id="MED05",
        name="Pathology Engine",
        port=8861,
        health_url="http://localhost:8861/health",
        capabilities=["pathology_diagnosis", "biopsy", "histology", "cytology"],
        weight=1.0,
        domains=["pathology", "biopsy", "histology", "cytology", "specimen"]
    ),
    "MED06": SubEngineConfig(
        engine_id="MED06",
        name="Infectious Disease Engine",
        port=8862,
        health_url="http://localhost:8862/health",
        capabilities=["infection_control", "antibiotic", "antiviral", "sepsis"],
        weight=1.0,
        domains=["infection", "antibiotic", "antiviral", "sepsis", "infectious disease"]
    ),
    "MED07": SubEngineConfig(
        engine_id="MED07",
        name="Surgery Engine",
        port=8863,
        health_url="http://localhost:8863/health",
        capabilities=["surgical_complication", "operation", "procedure", "perioperative"],
        weight=1.0,
        domains=["surgery", "operation", "procedure", "perioperative", "postoperative"]
    ),
    "MED08": SubEngineConfig(
        engine_id="MED08",
        name="Cardiology Engine",
        port=8864,
        health_url="http://localhost:8864/health",
        capabilities=["cardiac_event", "arrhythmia", "myocardial_infarction", "heart_failure"],
        weight=1.0,
        domains=["cardiology", "heart", "arrhythmia", "myocardial infarction", "heart failure", "ecg"]
    ),
    "MED09": SubEngineConfig(
        engine_id="MED09",
        name="Neurology Engine",
        port=8865,
        health_url="http://localhost:8865/health",
        capabilities=["neurological_deficit", "stroke", "seizure", "headache"],
        weight=1.0,
        domains=["neurology", "stroke", "seizure", "headache", "neurological"]
    ),
    "MED10": SubEngineConfig(
        engine_id="MED10",
        name="Oncology Engine",
        port=8866,
        health_url="http://localhost:8866/health",
        capabilities=["oncology_stage", "tumor", "chemotherapy", "radiation"],
        weight=1.0,
        domains=["oncology", "cancer", "tumor", "chemotherapy", "radiation"]
    ),
    "MED11": SubEngineConfig(
        engine_id="MED11",
        name="Pediatrics Engine",
        port=8867,
        health_url="http://localhost:8867/health",
        capabilities=["pediatric_alert", "growth", "vaccination", "development"],
        weight=1.0,
        domains=["pediatrics", "child", "infant", "growth", "vaccination"]
    ),
    "MED12": SubEngineConfig(
        engine_id="MED12",
        name="Obstetrics Engine",
        port=8868,
        health_url="http://localhost:8868/health",
        capabilities=["obstetric_risk", "labor", "pregnancy", "prenatal"],
        weight=1.0,
        domains=["obstetrics", "pregnancy", "labor", "prenatal", "maternal"]
    ),
    "MED13": SubEngineConfig(
        engine_id="MED13",
        name="Psychiatry Engine",
        port=8869,
        health_url="http://localhost:8869/health",
        capabilities=["psychiatric_emergency", "suicidal_ideation", "psychosis", "depression"],
        weight=1.0,
        domains=["psychiatry", "mental health", "depression", "psychosis", "suicide"]
    ),
    "MED14": SubEngineConfig(
        engine_id="MED14",
        name="Orthopedics Engine",
        port=8870,
        health_url="http://localhost:8870/health",
        capabilities=["orthopedic_injury", "fracture", "dislocation", "joint"],
        weight=1.0,
        domains=["orthopedics", "fracture", "dislocation", "joint", "bone"]
    ),
    "MED15": SubEngineConfig(
        engine_id="MED15",
        name="Dermatology Engine",
        port=8871,
        health_url="http://localhost:8871/health",
        capabilities=["dermatologic_lesion", "rash", "skin_infection", "ulcer"],
        weight=1.0,
        domains=["dermatology", "rash", "skin", "lesion", "ulcer"]
    ),
    "MED16": SubEngineConfig(
        engine_id="MED16",
        name="Gastroenterology Engine",
        port=8872,
        health_url="http://localhost:8872/health",
        capabilities=["gastrointestinal_bleed", "ulcer", "liver_dysfunction", "pancreatitis"],
        weight=1.0,
        domains=["gastroenterology", "gastrointestinal", "liver", "ulcer", "pancreatitis"]
    ),
    "MED17": SubEngineConfig(
        engine_id="MED17",
        name="Nephrology Engine",
        port=8873,
        health_url="http://localhost:8873/health",
        capabilities=["renal_failure", "nephritis", "kidney_stone", "dialysis"],
        weight=1.0,
        domains=["nephrology", "renal", "kidney", "dialysis", "nephritis"]
    ),
    "MED18": SubEngineConfig(
        engine_id="MED18",
        name="Pulmonology Engine",
        port=8874,
        health_url="http://localhost:8874/health",
        capabilities=["pulmonary_embolism", "asthma", "copd", "respiratory_failure"],
        weight=1.0,
        domains=["pulmonology", "pulmonary", "asthma", "copd", "respiratory"]
    ),
    "MED19": SubEngineConfig(
        engine_id="MED19",
        name="Endocrinology Engine",
        port=8875,
        health_url="http://localhost:8875/health",
        capabilities=["endocrine_crisis", "diabetes", "thyroid", "adrenal"],
        weight=1.0,
        domains=["endocrinology", "diabetes", "thyroid", "adrenal", "hormone"]
    ),
    "MED20": SubEngineConfig(
        engine_id="MED20",
        name="Immunology Engine",
        port=8876,
        health_url="http://localhost:8876/health",
        capabilities=["immunologic_reaction", "autoimmune_event", "immunodeficiency", "allergy"],
        weight=1.0,
        domains=["immunology", "autoimmune", "allergy", "immunodeficiency", "immune"]
    ),
    "MED21": SubEngineConfig(
        engine_id="MED21",
        name="Genetics Engine",
        port=8877,
        health_url="http://localhost:8877/health",
        capabilities=["genetic_variant", "genetic_screening", "hereditary_disease", "genome"],
        weight=1.0,
        domains=["genetics", "genome", "hereditary", "variant", "mutation"]
    ),
}

# Routing Rules (domain keyword to engine_id mapping)
# For brevity, only a sample is shown; in production, this would be 200+ rules.
ROUTING_RULES: Dict[str, str] = {
    # Pharmacology
    "drug": "MED01",
    "medication": "MED01",
    "dose": "MED01",
    "side effect": "MED01",
    "pharmacokinetics": "MED01",
    "pharmacodynamics": "MED01",
    "interaction": "MED01",
    "prescription": "MED01",
    "antibiotic": "MED06",
    "antiviral": "MED06",
    "antifungal": "MED06",
    "antidote": "MED02",
    "overdose": "MED02",
    "poison": "MED02",
    "toxicity": "MED02",
    "intoxication": "MED02",
    "toxin": "MED02",
    # Emergency Medicine
    "emergency": "MED03",
    "triage": "MED03",
    "resuscitation": "MED03",
    "trauma": "MED03",
    "shock": "MED03",
    "code blue": "MED03",
    "cardiac arrest": "MED08",
    # Radiology
    "radiology": "MED04",
    "imaging": "MED04",
    "xray": "MED04",
    "ct": "MED04",
    "mri": "MED04",
    "ultrasound": "MED04",
    "pet scan": "MED04",
    "angiogram": "MED04",
    # Pathology
    "pathology": "MED05",
    "biopsy": "MED05",
    "histology": "MED05",
    "cytology": "MED05",
    "specimen": "MED05",
    "slide": "MED05",
    # Infectious Disease
    "infection": "MED06",
    "sepsis": "MED06",
    "infectious disease": "MED06",
    "bacteria": "MED06",
    "virus": "MED06",
    "fungus": "MED06",
    "parasite": "MED06",
    # Surgery
    "surgery": "MED07",
    "operation": "MED07",
    "procedure": "MED07",
    "perioperative": "MED07",
    "postoperative": "MED07",
    "complication": "MED07",
    # Cardiology
    "cardiology": "MED08",
    "heart": "MED08",
    "arrhythmia": "MED08",
    "myocardial infarction": "MED08",
    "heart failure": "MED08",
    "ecg": "MED08",
    "stemi": "MED08",
    "nstemi": "MED08",
    # Neurology
    "neurology": "MED09",
    "stroke": "MED09",
    "seizure": "MED09",
    "headache": "MED09",
    "neurological": "MED09",
    "tbi": "MED09",
    "epilepsy": "MED09",
    # Oncology
    "oncology": "MED10",
    "cancer": "MED10",
    "tumor": "MED10",
    "chemotherapy": "MED10",
    "radiation": "MED10",
    "metastasis": "MED10",
    "carcinoma": "MED10",
    # Pediatrics
    "pediatrics": "MED11",
    "child": "MED11",
    "infant": "MED11",
    "growth": "MED11",
    "vaccination": "MED11",
    "neonate": "MED11",
    "adolescent": "MED11",
    # Obstetrics
    "obstetrics": "MED12",
    "pregnancy": "MED12",
    "labor": "MED12",
    "prenatal": "MED12",
    "maternal": "MED12",
    "fetal": "MED12",
    "gestation": "MED12",
    # Psychiatry
    "psychiatry": "MED13",
    "mental health": "MED13",
    "depression": "MED13",
    "psychosis": "MED13",
    "suicide": "MED13",
    "anxiety": "MED13",
    "bipolar": "MED13",
    # Orthopedics
    "orthopedics": "MED14",
    "fracture": "MED14",
    "dislocation": "MED14",
    "joint": "MED14",
    "bone": "MED14",
    "osteoporosis": "MED14",
    "arthritis": "MED14",
    # Dermatology
    "dermatology": "MED15",
    "rash": "MED15",
    "skin": "MED15",
    "lesion": "MED15",
    "ulcer": "MED15",
    "psoriasis": "MED15",
    "eczema": "MED15",
    # Gastroenterology
    "gastroenterology": "MED16",
    "gastrointestinal": "MED16",
    "liver": "MED16",
    "ulcer": "MED16",
    "pancreatitis": "MED16",
    "colitis": "MED16",
    "hepatitis": "MED16",
    # Nephrology
    "nephrology": "MED17",
    "renal": "MED17",
    "kidney": "MED17",
    "dialysis": "MED17",
    "nephritis": "MED17",
    "glomerulonephritis": "MED17",
    "kidney stone": "MED17",
    # Pulmonology
    "pulmonology": "MED18",
    "pulmonary": "MED18",
    "asthma": "MED18",
    "copd": "MED18",
    "respiratory": "MED18",
    "emphysema": "MED18",
    "bronchitis": "MED18",
    # Endocrinology
    "endocrinology": "MED19",
    "diabetes": "MED19",
    "thyroid": "MED19",
    "adrenal": "MED19",
    "hormone": "MED19",
    "pituitary": "MED19",
    "insulin": "MED19",
    # Immunology
    "immunology": "MED20",
    "autoimmune": "MED20",
    "allergy": "MED20",
    "immunodeficiency": "MED20",
    "immune": "MED20",
    "lupus": "MED20",
    "rheumatoid": "MED20",
    # Genetics
    "genetics": "MED21",
    "genome": "MED21",
    "hereditary": "MED21",
    "variant": "MED21",
    "mutation": "MED21",
    "genetic": "MED21",
    "screening": "MED21",
    # Additional rules (sample expansion)
    "hypertension": "MED08",
    "hyperlipidemia": "MED08",
    "tachycardia": "MED08",
    "bradycardia": "MED08",
    "migraine": "MED09",
    "parkinson": "MED09",
    "multiple sclerosis": "MED09",
    "lymphoma": "MED10",
    "leukemia": "MED10",
    "sarcoma": "MED10",
    "bronchiolitis": "MED18",
    "pneumonia": "MED18",
    "tuberculosis": "MED18",
    "cystic fibrosis": "MED18",
    "crohn": "MED16",
    "ulcerative colitis": "MED16",
    "cirrhosis": "MED16",
    "glomerulopathy": "MED17",
    "nephrotic": "MED17",
    "nephritic": "MED17",
    "hyperthyroidism": "MED19",
    "hypothyroidism": "MED19",
    "cushing": "MED19",
    "addison": "MED19",
    "anaphylaxis": "MED20",
    "urticaria": "MED20",
    "angioedema": "MED20",
    "down syndrome": "MED21",
    "cystic fibrosis gene": "MED21",
    "brca": "MED21",
    "sickle cell": "MED21",
    "thalassemia": "MED21",
    # ... (expand to 200+ rules as needed)
}

# Metrics Collector

class MetricsCollector:
    def __init__(self):
        self.query_times = collections.deque(maxlen=10000)
        self.error_counts = collections.deque(maxlen=10000)
        self.query_timestamps = collections.deque(maxlen=10000)
        self.lock = asyncio.Lock()

    async def record_query(self, latency_ms: float):
        async with self.lock:
            self.query_times.append(latency_ms)
            self.query_timestamps.append(time.time())

    async def record_error(self):
        async with self.lock:
            self.error_counts.append(time.time())

    async def get_latency_stats(self) -> Dict[str, float]:
        async with self.lock:
            if not self.query_times:
                return {"mean": 0.0, "median": 0.0, "p95": 0.0, "count": 0}
            data = list(self.query_times)
            return {
                "mean": statistics.mean(data),
                "median": statistics.median(data),
                "p95": statistics.quantiles(data, n=100)[94] if len(data) >= 20 else max(data),
                "count": len(data)
            }

    async def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        async with self.lock:
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
        topic="Pharmacokinetics - Absorption",
        keywords=["pharmacokinetics", "absorption", "bioavailability", "oral administration", "first-pass metabolism", "drug formulation", "gastrointestinal tract"],
        conclusion_template=(
            "The absorption phase critically determines the onset and intensity of drug action. "
            "Optimizing bioavailability requires understanding of gastrointestinal physiology and drug properties. "
            "Formulation and route of administration must be tailored to maximize therapeutic efficacy while minimizing variability."
        ),
        reasoning_framework=(
            "Absorption is the process by which a drug moves from the site of administration into the bloodstream. "
            "Oral absorption is influenced by drug solubility, stability in gastric pH, permeability across intestinal mucosa, and first-pass metabolism in the liver. "
            "Factors such as gastric emptying time, presence of food, and interactions with other substances can alter absorption kinetics. "
            "The Biopharmaceutics Classification System (BCS) categorizes drugs based on solubility and permeability, guiding formulation strategies. "
            "For example, drugs with low solubility but high permeability (BCS Class II) benefit from formulations enhancing dissolution rate. "
            "First-pass metabolism can significantly reduce bioavailability, necessitating alternative routes or prodrug design. "
            "Clinical pharmacokinetics integrates these variables to predict plasma concentration-time profiles, informing dosing regimens. "
            "Interindividual variability due to genetic polymorphisms in metabolizing enzymes (e.g., CYP450 isoforms) further complicates absorption outcomes. "
            "Therapeutic drug monitoring may be required for drugs with narrow therapeutic indices. "
            "Regulatory guidelines (FDA, EMA) emphasize rigorous bioavailability and bioequivalence studies during drug development. "
            "Understanding absorption dynamics is essential for optimizing drug efficacy and safety."
        ),
        key_factors=[
            "Drug solubility and stability",
            "Gastrointestinal pH and motility",
            "First-pass hepatic metabolism",
            "Formulation and excipients",
            "Patient-specific factors (age, genetics)",
            "Drug-drug and food interactions"
        ],
        primary_authority=[
            "Shargel L, Wu-Pong S, Yu ABC. Applied Biopharmaceutics & Pharmacokinetics. 7th ed. McGraw-Hill; 2012.",
            "FDA Guidance for Industry: Bioavailability and Bioequivalence Studies for Orally Administered Drug Products — General Considerations, 2014.",
            "EMA Guideline on the Investigation of Bioequivalence, 2010.",
            "Rowland M, Tozer TN. Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications. 4th ed. Lippincott Williams & Wilkins; 2010."
        ],
        burden_holder="Pharmaceutical developer and clinical pharmacologist",
        adversary_position="Assumption that oral administration guarantees consistent systemic exposure without accounting for variability",
        counter_arguments=[
            "Interindividual variability in absorption due to genetic polymorphisms",
            "Influence of gastrointestinal diseases altering mucosal integrity",
            "Impact of food and concomitant medications on drug dissolution and transport",
            "Limitations of in vitro dissolution tests to predict in vivo absorption",
            "Variability in first-pass metabolism among populations"
        ],
        resolution_strategy=(
            "Employ population pharmacokinetic modeling and therapeutic drug monitoring to individualize dosing. "
            "Use alternative routes or prodrug strategies when oral absorption is inadequate. "
            "Conduct thorough bioequivalence studies and consider patient-specific factors in clinical protocols."
        ),
        entity_scope="Pharmacology, Clinical Pharmacokinetics, Drug Development",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FDA Guidance on Bioavailability and Bioequivalence, 2014"
    ),
    DoctrineBlock(
        topic="Pharmacokinetics - Distribution",
        keywords=["pharmacokinetics", "distribution", "volume of distribution", "plasma protein binding", "tissue permeability", "blood-brain barrier", "drug reservoirs"],
        conclusion_template=(
            "Drug distribution determines the extent and duration of drug action by influencing tissue exposure. "
            "Understanding volume of distribution and binding characteristics is essential for dose optimization and toxicity prevention."
        ),
        reasoning_framework=(
            "Distribution refers to the reversible transfer of a drug between systemic circulation and tissues. "
            "The volume of distribution (Vd) is a theoretical volume that relates the amount of drug in the body to plasma concentration, reflecting tissue binding and permeability. "
            "Plasma protein binding, primarily to albumin and alpha-1 acid glycoprotein, affects free (active) drug concentration and clearance. "
            "Highly protein-bound drugs have lower free fractions, potentially leading to drug interactions when displaced. "
            "Tissue permeability is influenced by physicochemical properties such as lipophilicity and molecular size. "
            "The blood-brain barrier (BBB) restricts passage of many drugs, necessitating specific transport mechanisms or lipophilic properties for CNS penetration. "
            "Certain tissues act as drug reservoirs (e.g., fat, bone), prolonging half-life and affecting dosing intervals. "
            "Pathological states such as hypoalbuminemia or inflammation alter distribution patterns. "
            "Pharmacokinetic models (one-, two-, multi-compartment) describe distribution kinetics to guide therapeutic drug monitoring. "
            "Drug redistribution can cause termination of action or delayed toxicity. "
            "Clinical implications include dose adjustment in obesity, renal or hepatic impairment, and critical illness."
        ),
        key_factors=[
            "Volume of distribution (Vd)",
            "Plasma protein binding affinity",
            "Tissue permeability and affinity",
            "Blood-brain barrier permeability",
            "Pathophysiological alterations",
            "Drug physicochemical properties"
        ],
        primary_authority=[
            "Rowland M, Tozer TN. Clinical Pharmacokinetics and Pharmacodynamics. 4th ed. Lippincott Williams & Wilkins; 2010.",
            "Shargel L, Wu-Pong S, Yu ABC. Applied Biopharmaceutics & Pharmacokinetics. 7th ed. McGraw-Hill; 2012.",
            "Benet LZ, Hoener BA. Changes in plasma protein binding have little clinical relevance. Clin Pharmacol Ther. 2002;71(3):115-121.",
            "Pardridge WM. Blood-brain barrier drug targeting: the future of brain drug development. Mol Interv. 2003;3(2):90-105."
        ],
        burden_holder="Clinical pharmacologist and prescriber",
        adversary_position="Neglecting distribution variability leading to subtherapeutic or toxic drug levels",
        counter_arguments=[
            "Variability in plasma protein levels due to disease states",
            "Drug displacement interactions altering free drug concentration",
            "Altered tissue perfusion in critical illness affecting distribution",
            "Inadequate consideration of BBB in CNS drug therapy",
            "Obesity and edema affecting Vd estimates"
        ],
        resolution_strategy=(
            "Incorporate patient-specific factors and therapeutic drug monitoring. "
            "Use pharmacokinetic modeling to adjust dosing in altered physiological states. "
            "Consider alternative formulations or routes for CNS-active drugs."
        ),
        entity_scope="Pharmacology, Clinical Therapeutics",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Benet and Hoener, Clin Pharmacol Ther, 2002"
    ),
    DoctrineBlock(
        topic="Pharmacokinetics - Metabolism",
        keywords=["pharmacokinetics", "metabolism", "hepatic enzymes", "CYP450", "phase I reactions", "phase II reactions", "first-pass effect", "enzyme induction", "enzyme inhibition"],
        conclusion_template=(
            "Drug metabolism transforms lipophilic compounds into more hydrophilic metabolites for excretion. "
            "Understanding metabolic pathways and enzyme interactions is critical to predict drug clearance and potential interactions."
        ),
        reasoning_framework=(
            "Metabolism primarily occurs in the liver via enzymatic biotransformation, converting drugs into metabolites that are more water-soluble. "
            "Phase I reactions (oxidation, reduction, hydrolysis) often involve cytochrome P450 enzymes (CYP450), notably CYP3A4, CYP2D6, CYP2C9 among others. "
            "Phase II reactions (conjugation) include glucuronidation, sulfation, acetylation, and glutathione conjugation, facilitating renal or biliary excretion. "
            "First-pass metabolism can drastically reduce oral bioavailability, necessitating dose adjustments or alternative routes. "
            "Genetic polymorphisms in CYP450 enzymes cause variability in metabolic rates, influencing efficacy and toxicity. "
            "Enzyme induction (e.g., rifampin) accelerates metabolism, potentially reducing drug levels, while enzyme inhibition (e.g., ketoconazole) can cause toxicity. "
            "Drug-drug interactions at the metabolic level are a major cause of adverse drug reactions. "
            "Non-hepatic metabolism (e.g., intestinal wall, plasma esterases) also contributes to clearance. "
            "Metabolic profiling is essential during drug development to predict pharmacokinetics and interaction potential. "
            "Regulatory agencies require detailed metabolism studies including identification of active or toxic metabolites."
        ),
        key_factors=[
            "CYP450 isoenzyme specificity",
            "Phase I and II metabolic pathways",
            "Genetic polymorphisms",
            "Enzyme induction and inhibition",
            "First-pass effect magnitude",
            "Drug-drug interactions"
        ],
        primary_authority=[
            "Guengerich FP. Cytochrome P450 and chemical toxicology. Chem Res Toxicol. 2008;21(1):70-83.",
            "FDA Guidance for Industry: Drug Interaction Studies — Study Design, Data Analysis, and Implications for Dosing and Labeling, 2020.",
            "Zanger UM, Schwab M. Cytochrome P450 enzymes in drug metabolism: regulation of gene expression, enzyme activities, and impact of genetic variation. Pharmacol Ther. 2013;138(1):103-141.",
            "Testa B, Krämer SD. The biochemistry of drug metabolism - an introduction: part 1. Principles and overview. Chem Biodivers. 2007;4(3): 217-252."
        ],
        burden_holder="Drug developer and clinical pharmacologist",
        adversary_position="Underestimating metabolic variability and interaction risks",
        counter_arguments=[
            "Significant interindividual variability in CYP450 activity",
            "Polypharmacy increasing risk of metabolic interactions",
            "Non-hepatic metabolism contributing to clearance",
            "Active metabolites altering therapeutic outcomes",
            "Environmental factors (e.g., smoking) affecting enzyme induction"
        ],
        resolution_strategy=(
            "Perform comprehensive metabolic profiling and interaction studies. "
            "Use genotyping and phenotyping to individualize therapy. "
            "Monitor for adverse effects and adjust dosing accordingly."
        ),
        entity_scope="Pharmacology, Clinical Therapeutics, Drug Development",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FDA Drug Interaction Guidance, 2020"
    ),
    DoctrineBlock(
        topic="Pharmacokinetics - Excretion",
        keywords=["pharmacokinetics", "excretion", "renal clearance", "biliary excretion", "glomerular filtration", "tubular secretion", "enterohepatic circulation", "drug elimination"],
        conclusion_template=(
            "Excretion is the final elimination of drugs and metabolites from the body, primarily via renal and biliary routes. "
            "Accurate assessment of excretion pathways is essential for dose adjustment, especially in organ dysfunction."
        ),
        reasoning_framework=(
            "Excretion removes drugs and metabolites from the systemic circulation, terminating pharmacologic activity. "
            "Renal excretion involves glomerular filtration, active tubular secretion, and passive reabsorption. "
            "Drugs with high renal clearance require dose adjustment in renal impairment to avoid accumulation and toxicity. "
            "Biliary excretion eliminates drugs into the gastrointestinal tract, sometimes followed by enterohepatic recirculation prolonging half-life. "
            "Factors affecting renal excretion include urine pH, flow rate, and transporter activity (e.g., OATs, OCTs). "
            "Non-renal routes include pulmonary excretion (volatile anesthetics), sweat, saliva, and breast milk. "
            "Pharmacokinetic parameters such as clearance and half-life depend on excretion efficiency. "
            "In patients with renal or hepatic failure, altered excretion necessitates therapeutic drug monitoring and dose modification. "
            "Clinical guidelines provide dosing recommendations based on creatinine clearance or estimated glomerular filtration rate (eGFR). "
            "Understanding excretion mechanisms aids in predicting drug interactions and adverse effects."
        ),
        key_factors=[
            "Renal function and clearance",
            "Biliary excretion and enterohepatic cycling",
            "Tubular secretion and reabsorption",
            "Non-renal elimination routes",
            "Impact of organ dysfunction",
            "Drug physicochemical properties"
        ],
        primary_authority=[
            "Benet LZ, Hoener BA. Changes in plasma protein binding have little clinical relevance. Clin Pharmacol Ther. 2002;71(3):115-121.",
            "Rowland M, Tozer TN. Clinical Pharmacokinetics and Pharmacodynamics. 4th ed. Lippincott Williams & Wilkins; 2010.",
            "FDA Guidance for Industry: Pharmacokinetics in Patients with Impaired Renal Function — Study Design, Data Analysis, and Impact on Dosing and Labeling, 2020.",
            "Nolin TD, Naud J, Leblond FA, Pichette V. Emerging evidence of the impact of kidney disease on drug metabolism and transport. Clin Pharmacol Ther. 2008;83(6):898-903."
        ],
        burden_holder="Prescribing clinician and clinical pharmacologist",
        adversary_position="Failure to adjust dosing in renal or hepatic impairment leading to toxicity",
        counter_arguments=[
            "Inaccurate estimation of renal function in special populations",
            "Variable biliary excretion complicating clearance prediction",
            "Drug interactions affecting transporter-mediated secretion",
            "Non-renal elimination routes often overlooked",
            "Impact of altered urine pH on drug reabsorption"
        ],
        resolution_strategy=(
            "Use validated renal function estimates to guide dosing. "
            "Monitor drug levels and clinical response in organ dysfunction. "
            "Consider alternative elimination pathways and adjust therapy accordingly."
        ),
        entity_scope="Pharmacology, Nephrology, Hepatology",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FDA Renal Impairment Guidance, 2020"
    ),
    DoctrineBlock(
        topic="Toxicology - Dose-Response Relationship",
        keywords=["toxicology", "dose-response", "LD50", "threshold", "toxicity", "therapeutic index", "dose-effect", "toxicity curve"],
        conclusion_template=(
            "The dose-response relationship defines the correlation between the amount of a substance and its biological effect. "
            "Understanding this relationship is fundamental for risk assessment and therapeutic window determination."
        ),
        reasoning_framework=(
            "Toxicology studies the adverse effects of chemical substances on living organisms, with dose-response relationships central to this discipline. "
            "The LD50 (lethal dose for 50% of subjects) is a classical metric quantifying acute toxicity. "
            "Dose-response curves typically exhibit a sigmoidal shape, with a threshold below which no effect is observed and a plateau at maximal effect. "
            "The therapeutic index (TI) compares the toxic dose to the effective dose, guiding safe dosing ranges. "
            "Variability in individual susceptibility, exposure duration, and route influence toxicity outcomes. "
            "Nonlinear kinetics and cumulative effects complicate dose-response predictions. "
            "Risk assessment incorporates margin of safety calculations and uncertainty factors to protect sensitive populations. "
            "Mechanistic toxicology explores molecular targets and pathways mediating toxicity, enabling biomarker development. "
            "Regulatory toxicology uses dose-response data to establish exposure limits such as NOAEL (No Observed Adverse Effect Level) and LOAEL (Lowest Observed Adverse Effect Level). "
            "Understanding dose-response relationships informs antidote development and clinical management of poisoning."
        ),
        key_factors=[
            "Dose magnitude and exposure duration",
            "Route of exposure",
            "Individual susceptibility and genetics",
            "Therapeutic index and safety margin",
            "Mechanism of toxicity",
            "Environmental and co-exposure factors"
        ],
        primary_authority=[
            "Casarett & Doull's Toxicology: The Basic Science of Poisons. 9th ed. McGraw-Hill; 2018.",
            "Goldfrank LR et al. Goldfrank's Toxicologic Emergencies. 12th ed. McGraw-Hill; 2017.",
            "Environmental Protection Agency (EPA). Guidelines for Carcinogen Risk Assessment, 2005.",
            "WHO IPCS. Principles for Evaluating Health Risks from Chemicals During Infancy and Early Childhood, 2006."
        ],
        burden_holder="Toxicologist and regulatory authority",
        adversary_position="Assuming linear dose-response without threshold or ignoring individual variability",
        counter_arguments=[
            "Non-monotonic dose-response curves in endocrine disruptors",
            "Cumulative and delayed toxicity effects",
            "Species differences limiting extrapolation",
            "Variability in absorption and metabolism affecting toxicity",
            "Interaction with other chemicals altering response"
        ],
        resolution_strategy=(
            "Use comprehensive dose-response modeling including threshold and non-threshold effects. "
            "Incorporate uncertainty factors and sensitive population data in risk assessment. "
            "Apply mechanistic insights to improve predictive toxicology."
        ),
        entity_scope="Toxicology, Risk Assessment, Regulatory Science",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA Guidelines for Carcinogen Risk Assessment, 2005"
    ),
    DoctrineBlock(
        topic="Toxicology - Antidote and Poison Management",
        keywords=["toxicology", "antidote", "poison management", "decontamination", "supportive care", "specific antidotes", "toxicity reversal", "emergency treatment"],
        conclusion_template=(
            "Effective poison management requires prompt identification and administration of specific antidotes alongside supportive care. "
            "Decontamination and monitoring are critical components to optimize patient outcomes."
        ),
        reasoning_framework=(
            "Poison management involves a systematic approach including identification of the toxic agent, assessment of exposure severity, and initiation of treatment. "
            "Decontamination methods include activated charcoal administration, gastric lavage, and skin or eye irrigation depending on the exposure route and timing. "
            "Specific antidotes act by various mechanisms: receptor antagonism (naloxone for opioids), enzyme reactivation (pralidoxime for organophosphates), or chemical binding (chelation for heavy metals). "
            "Supportive care addresses airway, breathing, circulation, and correction of metabolic disturbances. "
            "Monitoring for delayed toxicity and complications is essential, often requiring serial laboratory tests and clinical observation. "
            "Protocols such as the American Academy of Clinical Toxicology guidelines standardize management approaches. "
            "Toxicokinetic and toxicodynamic principles guide antidote dosing and timing. "
            "In some poisonings, extracorporeal removal techniques (hemodialysis, hemoperfusion) are indicated. "
            "Education and prevention strategies reduce incidence and severity of poisonings."
        ),
        key_factors=[
            "Identification of toxic agent",
            "Timing and route of exposure",
            "Availability and mechanism of antidote",
            "Supportive care and monitoring",
            "Decontamination methods",
            "Toxicokinetic considerations"
        ],
        primary_authority=[
            "Goldfrank LR et al. Goldfrank's Toxicologic Emergencies. 12th ed. McGraw-Hill; 2017.",
            "American Academy of Clinical Toxicology (AACT) and European Association of Poisons Centres and Clinical Toxicologists (EAPCCT) Position Papers.",
            "Gosselin S, Juurlink DN, Kielstein JT. Critical Care Toxicology: Diagnosis and Management of the Critically Poisoned Patient. 2nd ed. Elsevier; 2017.",
            "World Health Organization. WHO Guidelines for Poison Control, 2010."
        ],
        burden_holder="Emergency physician and toxicologist",
        adversary_position="Delays in antidote administration or reliance solely on supportive care",
        counter_arguments=[
            "Limited availability or high cost of specific antidotes",
            "Uncertainty in toxic agent identification",
            "Risks associated with decontamination procedures",
            "Variable efficacy of antidotes depending on timing",
            "Potential adverse effects of antidotes"
        ],
        resolution_strategy=(
            "Implement rapid diagnostic protocols and maintain antidote stocks. "
            "Use evidence-based guidelines to balance risks and benefits of interventions. "
            "Train healthcare providers in poison management and toxicology."
        ),
        entity_scope="Toxicology, Emergency Medicine, Critical Care",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Goldfrank's Toxicologic Emergencies, 2017"
    ),
    DoctrineBlock(
        topic="Emergency Medicine - Trauma Management (ATLS)",
        keywords=["emergency medicine", "trauma", "ATLS", "triage", "resuscitation", "airway management", "hemorrhage control", "shock"],
        conclusion_template=(
            "Advanced Trauma Life Support (ATLS) protocols provide a systematic approach to trauma care emphasizing rapid assessment and intervention. "
            "Prioritization of airway, breathing, and circulation is essential to reduce mortality."
        ),
        reasoning_framework=(
            "Trauma is a leading cause of morbidity and mortality worldwide, necessitating structured management protocols. "
            "ATLS provides a standardized approach beginning with primary survey focusing on airway maintenance with cervical spine protection, breathing and ventilation assessment, circulation with hemorrhage control, disability (neurologic status), and exposure/environmental control. "
            "Rapid identification and management of life-threatening injuries improves survival. "
            "Triage systems prioritize patients based on injury severity and resource availability, optimizing outcomes in mass casualty incidents. "
            "Resuscitation includes fluid replacement, blood transfusion, and correction of coagulopathy. "
            "Imaging adjuncts such as FAST ultrasound aid in rapid diagnosis. "
            "Secondary survey involves detailed head-to-toe examination and history taking. "
            "Continuous reassessment is critical due to dynamic patient status. "
            "Evidence supports early hemorrhage control using tourniquets and damage control surgery. "
            "Multidisciplinary coordination and trauma system organization enhance care delivery."
        ),
        key_factors=[
            "Airway patency and cervical spine protection",
            "Breathing adequacy and oxygenation",
            "Circulatory status and hemorrhage control",
            "Neurologic assessment",
            "Triage accuracy",
            "Resuscitation protocols"
        ],
        primary_authority=[
            "American College of Surgeons Committee on Trauma. Advanced Trauma Life Support (ATLS) Student Course Manual. 10th ed. 2018.",
            "Sauaia A, Moore FA, Moore EE, et al. Epidemiology of trauma deaths: a reassessment. J Trauma. 1995;38(2):185-193.",
            "Kauvar DS, Lefering R, Wade CE. Impact of hemorrhage on trauma outcome: an overview of epidemiology, clinical presentations, and therapeutic considerations. J Trauma. 2006;60(6 Suppl):S3-11.",
            "American College of Emergency Physicians. Clinical Policy: Critical Issues in the Evaluation and Management of Adult Patients Presenting to the Emergency Department with Acute Blunt Abdominal Trauma. Ann Emerg Med. 2015."
        ],
        burden_holder="Emergency physician and trauma team",
        adversary_position="Failure to adhere to systematic trauma protocols leading to missed injuries",
        counter_arguments=[
            "Variability in provider training and experience",
            "Resource limitations in prehospital and hospital settings",
            "Delays in definitive hemorrhage control",
            "Inadequate triage in mass casualty events",
            "Complications from aggressive resuscitation"
        ],
        resolution_strategy=(
            "Implement widespread ATLS training and certification. "
            "Develop trauma systems with coordinated prehospital and hospital care. "
            "Use evidence-based protocols and continuous quality improvement."
        ),
        entity_scope="Emergency Medicine, Trauma Surgery",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="American College of Surgeons ATLS Manual, 2018"
    ),
    DoctrineBlock(
        topic="Radiology - CT Imaging Interpretation",
        keywords=["radiology", "CT imaging", "computed tomography", "contrast enhancement", "radiation dose", "image artifacts", "diagnostic accuracy", "cross-sectional imaging"],
        conclusion_template=(
            "Computed Tomography (CT) imaging provides high-resolution cross-sectional images critical for diagnosis. "
            "Interpretation requires understanding of anatomy, pathology, and imaging physics to optimize diagnostic accuracy."
        ),
        reasoning_framework=(
            "CT imaging uses X-ray beams and detectors rotating around the patient to produce cross-sectional images. "
            "Contrast agents enhance visualization of vascular structures and lesions. "
            "Interpretation involves assessing tissue density (Hounsfield units), morphology, and enhancement patterns. "
            "Artifacts such as beam hardening, motion, and metal implants can degrade image quality and mimic pathology. "
            "Radiation dose considerations necessitate ALARA (As Low As Reasonably Achievable) principles, balancing diagnostic benefit and risk. "
            "Protocols vary by clinical indication, including trauma, oncology staging, and vascular imaging. "
            "Multiplanar reconstructions and 3D imaging aid in surgical planning. "
            "Radiologists integrate clinical information with imaging findings for accurate diagnosis. "
            "Advances include dual-energy CT and iterative reconstruction techniques improving image quality and reducing dose. "
            "Quality assurance and standardized reporting (e.g., RADS systems) enhance communication and patient care."
        ),
        key_factors=[
            "Image acquisition parameters",
            "Contrast agent use and timing",
            "Recognition of artifacts",
            "Radiation dose management",
            "Clinical context integration",
            "Advanced reconstruction techniques"
        ],
        primary_authority=[
            "Brant WE, Helms CA. Fundamentals of Diagnostic Radiology. 4th ed. Lippincott Williams & Wilkins; 2012.",
            "American College of Radiology. ACR Appropriateness Criteria®.",
            "McCollough CH, et al. CT dose reduction and dose management tools: overview of available options. Radiographics. 2011;31(2): 503-512.",
            "Kalra MK, Maher MM, Toth TL, et al. Strategies for CT radiation dose optimization. Radiology. 2004;230(3):619-628."
        ],
        burden_holder="Radiologist and imaging technologist",
        adversary_position="Overreliance on imaging without clinical correlation or ignoring radiation safety",
        counter_arguments=[
            "Incidental findings leading to unnecessary interventions",
            "Radiation exposure risks especially in pediatric populations",
            "Misinterpretation due to artifacts or technical limitations",
            "Contrast-induced nephropathy risk",
            "Variability in protocol adherence"
        ],
        resolution_strategy=(
            "Adhere to evidence-based imaging protocols and dose optimization. "
            "Correlate imaging with clinical findings. "
            "Educate providers on appropriate use and risks."
        ),
        entity_scope="Radiology, Diagnostic Imaging",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ACR Appropriateness Criteria and Dose Management Guidelines"
    ),
    DoctrineBlock(
        topic="Pathology - Histology and Cytology in Diagnosis",
        keywords=["pathology", "histology", "cytology", "biopsy", "microscopic examination", "tissue architecture", "cell morphology", "diagnostic accuracy"],
        conclusion_template=(
            "Histological and cytological examination of tissue samples is fundamental for definitive diagnosis. "
            "Accurate interpretation requires expertise in morphology and clinical correlation."
        ),
        reasoning_framework=(
            "Histology involves microscopic examination of tissue architecture and cellular detail, typically from biopsy or surgical specimens. "
            "Cytology studies individual cells or small clusters, often from less invasive sampling such as fine needle aspiration or exfoliative cytology. "
            "Preparation techniques (fixation, staining) affect specimen quality and diagnostic yield. "
            "Pathologists assess features such as cellular atypia, mitotic activity, necrosis, and stromal changes to differentiate benign from malignant processes. "
            "Immunohistochemistry and molecular pathology augment morphological diagnosis by identifying specific markers and genetic alterations. "
            "Sampling error and interpretive variability are challenges, necessitating multidisciplinary discussion. "
            "Standardized reporting systems (e.g., Bethesda system for cervical cytology) improve communication. "
            "Quality control and proficiency testing maintain diagnostic accuracy. "
            "Histopathology guides treatment decisions and prognostication. "
            "Advances in digital pathology and AI-assisted interpretation hold promise for enhanced diagnostics."
        ),
        key_factors=[
            "Specimen collection and processing quality",
            "Morphological criteria for diagnosis",
            "Use of ancillary techniques",
            "Correlation with clinical and radiologic data",
            "Standardized reporting systems",
            "Pathologist expertise"
        ],
        primary_authority=[
            "Robbins Basic Pathology. Kumar V, Abbas AK, Aster JC. 10th ed. Elsevier; 2017.",
            "Koss LG, Melamed MR. Koss' Diagnostic Cytology and Its Histopathologic Bases. 5th ed. Lippincott Williams & Wilkins; 2006.",
            "College of American Pathologists (CAP) guidelines and checklists.",
            "National Cancer Institute. Bethesda System for Reporting Cervical Cytology, 2014."
        ],
        burden_holder="Pathologist and clinical team",
        adversary_position="Overreliance on morphology without molecular or clinical correlation",
        counter_arguments=[
            "Sampling errors leading to false negatives",
            "Interobserver variability in interpretation",
            "Limitations of cytology in certain tumor types",
            "Delay in ancillary testing availability",
            "Potential for overdiagnosis and overtreatment"
        ],
        resolution_strategy=(
            "Use multimodal diagnostic approaches integrating morphology, immunohistochemistry, and molecular data. "
            "Implement quality assurance programs and multidisciplinary case review."
        ),
        entity_scope="Pathology, Diagnostic Medicine",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="CAP guidelines and Bethesda System, 2014"
    ),
    DoctrineBlock(
        topic="Infectious Disease - Antibiotic Resistance",
        keywords=["infectious disease", "antibiotic resistance", "mechanisms", "multidrug resistance", "antimicrobial stewardship", "beta-lactamases", "efflux pumps", "horizontal gene transfer"],
        conclusion_template=(
            "Antibiotic resistance threatens effective infection management globally. "
            "Understanding resistance mechanisms and implementing stewardship programs are essential to preserve antimicrobial efficacy."
        ),
        reasoning_framework=(
            "Antibiotic resistance arises from genetic mutations and acquisition of resistance genes via horizontal gene transfer (plasmids, transposons). "
            "Mechanisms include enzymatic drug inactivation (e.g., beta-lactamases), target site modification, decreased permeability, and active efflux. "
            "Multidrug-resistant organisms (MDROs) complicate therapy, increasing morbidity, mortality, and healthcare costs. "
            "Selective pressure from inappropriate antibiotic use accelerates resistance development. "
            "Surveillance programs monitor resistance patterns to guide empirical therapy. "
            "Antimicrobial stewardship promotes rational antibiotic use, optimizing selection, dose, and duration to minimize resistance emergence. "
            "Infection control measures prevent transmission of resistant pathogens in healthcare settings. "
            "Research into novel antimicrobials and alternative therapies (phage therapy, immunomodulation) is ongoing. "
            "Global collaboration is required to address resistance as a public health crisis."
        ),
        key_factors=[
            "Genetic mechanisms of resistance",
            "Patterns of multidrug resistance",
            "Antimicrobial stewardship implementation",
            "Surveillance and infection control",
            "Selective pressure from antibiotic use",
            "Development of new therapies"
        ],
        primary_authority=[
            "World Health Organization. Global Action Plan on Antimicrobial Resistance, 2015.",
            "Centers for Disease Control and Prevention (CDC). Antibiotic Resistance Threats in the United States, 2019.",
            "Davies J, Davies D. Origins and evolution of antibiotic resistance. Microbiol Mol Biol Rev. 2010;74(3):417-433.",
            "Ventola CL. The antibiotic resistance crisis: part 1: causes and threats. P T. 2015;40(4):277-283."
        ],
        burden_holder="Infectious disease specialists, healthcare providers, and public health authorities",
        adversary_position="Overuse and misuse of antibiotics without stewardship",
        counter_arguments=[
            "Patient demand and expectations for antibiotics",
            "Diagnostic uncertainty leading to empirical broad-spectrum use",
            "Limited access to rapid diagnostic tests",
            "Economic incentives favoring antibiotic sales",
            "Global disparities in antibiotic regulation"
        ],
        resolution_strategy=(
            "Implement stewardship programs with education and audit-feedback. "
            "Enhance diagnostics to guide targeted therapy. "
            "Strengthen infection control and surveillance. "
            "Promote global policy and research initiatives."
        ),
        entity_scope="Infectious Disease, Microbiology, Public Health",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="WHO Global Action Plan on AMR, 2015"
    ),
    DoctrineBlock(
        topic="Surgery - Aseptic Technique",
        keywords=["surgery", "aseptic technique", "sterilization", "infection prevention", "surgical site infection", "hand hygiene", "barrier precautions", "sterile field"],
        conclusion_template=(
            "Aseptic technique is fundamental to preventing surgical site infections and ensuring patient safety. "
            "Strict adherence to sterilization and barrier methods reduces microbial contamination during operative procedures."
        ),
        reasoning_framework=(
            "Surgical site infections (SSIs) significantly increase morbidity, mortality, and healthcare costs. "
            "Aseptic technique encompasses hand hygiene, use of sterile gloves, gowns, drapes, and instruments to create and maintain a sterile field. "
            "Sterilization methods include autoclaving, chemical sterilants, and gas sterilization, validated to eliminate all microbial life including spores. "
            "Environmental controls such as laminar airflow and operating room traffic limitation reduce airborne contamination. "
            "Proper skin antisepsis of the patient and surgical team preparation are critical. "
            "Adherence to protocols such as WHO Surgical Safety Checklist improves outcomes. "
            "Education and training of surgical teams reinforce aseptic principles. "
            "Monitoring and surveillance of SSIs guide quality improvement initiatives. "
            "Antimicrobial prophylaxis complements aseptic technique but does not replace it. "
            "Breaks in aseptic technique require immediate correction to prevent contamination."
        ),
        key_factors=[
            "Hand hygiene compliance",
            "Sterilization of instruments and materials",
            "Maintenance of sterile field",
            "Environmental controls in OR",
            "Patient skin preparation",
            "Team training and protocol adherence"
        ],
        primary_authority=[
            "Mangram AJ, Horan TC, Pearson ML, et al. Guideline for Prevention of Surgical Site Infection, 1999. Infect Control Hosp Epidemiol. 1999;20(4):250-278.",
            "World Health Organization. Global Guidelines for the Prevention of Surgical Site Infection, 2016.",
            "Centers for Disease Control and Prevention. Guideline for Hand Hygiene in Health-Care Settings, 2002.",
            "Association of periOperative Registered Nurses (AORN) Guidelines for Sterile Technique."
        ],
        burden_holder="Surgical team and hospital infection control",
        adversary_position="Inconsistent or incomplete aseptic practices leading to SSIs",
        counter_arguments=[
            "Time pressures and emergency situations compromising technique",
            "Resource limitations in sterilization equipment",
            "Noncompliance with hand hygiene protocols",
            "Breaks in sterile field unnoticed or uncorrected",
            "Environmental contamination from OR traffic"
        ],
        resolution_strategy=(
            "Implement continuous education and auditing. "
            "Ensure availability and maintenance of sterilization equipment. "
            "Enforce strict adherence to aseptic protocols with leadership support."
        ),
        entity_scope="Surgery, Infection Control",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="WHO Global Guidelines for SSI Prevention, 2016"
    ),
    DoctrineBlock(
        topic="Cardiology - Electrocardiography (ECG) Interpretation",
        keywords=["cardiology", "ECG", "electrocardiography", "arrhythmia", "myocardial infarction", "conduction abnormalities", "ST segment", "QT interval"],
        conclusion_template=(
            "ECG interpretation is essential for diagnosing cardiac arrhythmias, ischemia, and conduction disorders. "
            "Accurate analysis of waveforms and intervals guides clinical management."
        ),
        reasoning_framework=(
            "Electrocardiography records the electrical activity of the heart through surface electrodes, producing characteristic waveforms: P wave, QRS complex, and T wave. "
            "Interpretation involves assessing rhythm, rate, axis, intervals (PR, QRS duration, QT), and morphology. "
            "Arrhythmias such as atrial fibrillation, ventricular tachycardia, and heart blocks have distinct ECG patterns. "
            "Ischemic changes include ST segment elevation or depression, T wave inversion, and pathological Q waves. "
            "Electrolyte disturbances and drug effects can prolong QT interval, predisposing to torsades de pointes. "
            "ECG findings must be correlated with clinical presentation and biomarkers for accurate diagnosis. "
            "Serial ECGs improve detection of dynamic changes. "
            "Automated interpretation aids but does not replace expert analysis. "
            "Training and standardized criteria (e.g., Minnesota Code) enhance diagnostic consistency. "
            "ECG is a cornerstone in emergency cardiology and outpatient cardiac evaluation."
        ),
        key_factors=[
            "Waveform morphology and intervals",
            "Rhythm and rate analysis",
            "Ischemic and infarction patterns",
            "Conduction abnormalities",
            "Electrolyte and drug effects",
            "Clinical correlation"
        ],
        primary_authority=[
            "Goldman L, Schafer AI. Goldman-Cecil Medicine. 25th ed. Elsevier; 2016.",
            "Wagner GS. Marriott's Practical Electrocardiography. 12th ed. Lippincott Williams & Wilkins; 2014.",
            "American Heart Association. ECG Interpretation Guidelines.",
            "Thygesen K, Alpert JS, Jaffe AS, et al. Fourth Universal Definition of Myocardial Infarction (2018). Circulation. 2018;138(20):e618-e651."
        ],
        burden_holder="Cardiologist and emergency physician",
        adversary_position="Misinterpretation leading to missed or incorrect diagnosis",
        counter_arguments=[
            "Artifact and technical errors affecting ECG quality",
            "Atypical presentations of ischemia or arrhythmia",
            "Limitations of single ECG snapshot",
            "Overreliance on automated interpretation",
            "Confounding electrolyte or drug effects"
        ],
        resolution_strategy=(
            "Ensure high-quality ECG acquisition. "
            "Use serial ECGs and clinical data integration. "
            "Provide ongoing training and expert consultation."
        ),
        entity_scope="Cardiology, Emergency Medicine",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Fourth Universal Definition of MI, 2018"
    ),
    DoctrineBlock(
        topic="Neurology - Stroke Evaluation and Management",
        keywords=["neurology", "stroke", "ischemic stroke", "hemorrhagic stroke", "thrombolysis", "neuroimaging", "NIH Stroke Scale", "time window"],
        conclusion_template=(
            "Rapid evaluation and management of stroke are critical to minimize neurological damage. "
            "Neuroimaging and clinical scales guide therapeutic decisions including thrombolysis."
        ),
        reasoning_framework=(
            "Stroke is a leading cause of disability and death, classified as ischemic or hemorrhagic based on etiology. "
            "Initial assessment includes airway, breathing, circulation, and neurologic examination using standardized tools like the NIH Stroke Scale (NIHSS). "
            "Neuroimaging (non-contrast CT or MRI) differentiates ischemic from hemorrhagic stroke, essential for treatment selection. "
            "Intravenous thrombolysis with tissue plasminogen activator (tPA) is effective within a narrow time window (generally 4.5 hours from symptom onset). "
            "Mechanical thrombectomy extends treatment options for large vessel occlusions up to 24 hours in selected patients. "
            "Blood pressure management, glucose control, and prevention of complications are integral. "
            "Secondary prevention includes antiplatelet therapy, anticoagulation for cardioembolic sources, and risk factor modification. "
            "Multidisciplinary stroke units improve outcomes. "
            "Timely recognition and transport to stroke centers are critical. "
            "Ongoing research focuses on neuroprotection and rehabilitation strategies."
        ),
        key_factors=[
            "Rapid clinical assessment and NIHSS scoring",
            "Neuroimaging differentiation",
            "Time-sensitive thrombolytic therapy",
            "Blood pressure and metabolic management",
            "Secondary prevention strategies",
            "Multidisciplinary care"
        ],
        primary_authority=[
            "Powers WJ, Rabinstein AA, Ackerson T, et al. 2018 Guidelines for the Early Management of Patients With Acute Ischemic Stroke. Stroke. 2018;49(3):e46-e110.",
            "American Heart Association/American Stroke Association. Guidelines for the Management of Spontaneous Intracerebral Hemorrhage, 2015.",
            "Hacke W, Kaste M, Bluhmki E, et al. Thrombolysis with alteplase 3 to 4.5 hours after acute ischemic stroke. N Engl J Med. 2008;359(13):1317-1329.",
            "Goyal M, Menon BK, van Zwam WH, et al. Endovascular thrombectomy after large-vessel ischaemic stroke: a meta-analysis of individual patient data from five randomised trials. Lancet. 2016;387(10029):1723-1731."
        ],
        burden_holder="Neurologist and emergency care team",
        adversary_position="Delays in diagnosis or inappropriate treatment leading to poor outcomes",
        counter_arguments=[
            "Uncertainty in symptom onset time",
            "Contraindications to thrombolysis",
            "Limited access to stroke centers",
            "Risk of hemorrhagic transformation",
            "Variability in stroke mimics"
        ],
        resolution_strategy=(
            "Implement prehospital stroke recognition and rapid transport. "
            "Use standardized protocols for imaging and treatment. "
            "Educate providers and public on stroke signs and urgency."
        ),
        entity_scope="Neurology, Emergency Medicine",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AHA/ASA Stroke Management Guidelines, 2018"
    ),
    DoctrineBlock(
        topic="Oncology - Cancer Staging and Classification",
        keywords=["oncology", "cancer staging", "TNM classification", "tumor grading", "metastasis", "prognosis", "treatment planning", "AJCC"],
        conclusion_template=(
            "Accurate cancer staging and classification are essential for prognosis determination and treatment planning. "
            "The TNM system provides a standardized framework for describing tumor extent."
        ),
        reasoning_framework=(
            "Cancer staging assesses the size and extent of primary tumor (T), regional lymph node involvement (N), and distant metastasis (M). "
            "The American Joint Committee on Cancer (AJCC) and Union for International Cancer Control (UICC) provide standardized TNM staging manuals. "
            "Tumor grading evaluates histologic differentiation and aggressiveness, complementing staging. "
            "Staging guides therapeutic decisions including surgery, chemotherapy, radiotherapy, and targeted therapies. "
            "Accurate staging requires integration of clinical examination, imaging, and pathological findings. "
            "Prognostic models incorporate staging with molecular markers to personalize treatment. "
            "Periodic restaging assesses treatment response and disease progression. "
            "Standardized reporting improves clinical trial comparability and epidemiologic surveillance. "
            "Limitations include variability in staging accuracy and applicability to rare tumors. "
            "Emerging imaging and molecular techniques enhance staging precision."
        ),
        key_factors=[
            "Tumor size and local invasion (T)",
            "Lymph node involvement (N)",
            "Distant metastasis (M)",
            "Histologic tumor grade",
            "Imaging and pathology correlation",
            "Molecular and genetic markers"
        ],
        primary_authority=[
            "Amin MB, Edge SB, Greene FL, et al., editors. AJCC Cancer Staging Manual. 8th ed. Springer; 2017.",
            "Brierley JD, Gospodarowicz MK, Wittekind C, editors. TNM Classification of Malignant Tumors. 8th ed. Wiley-Blackwell; 2017.",
            "National Comprehensive Cancer Network (NCCN) Clinical Practice Guidelines in Oncology.",
            "Edge SB, Compton CC. The American Joint Committee on Cancer: the 7th edition of the AJCC cancer staging manual and the future of TNM. Ann Surg Oncol. 2010;17(6):1471-1474."
        ],
        burden_holder="Oncologist and multidisciplinary cancer team",
        adversary_position="Inaccurate or incomplete staging leading to suboptimal treatment",
        counter_arguments=[
            "Imaging limitations in detecting micrometastases",
            "Interobserver variability in tumor grading",
            "Heterogeneity of tumor biology",
            "Delays in obtaining complete diagnostic information",
            "Applicability of staging systems to novel therapies"
        ],
        resolution_strategy=(
            "Use multimodal diagnostic approaches and multidisciplinary review. "
            "Incorporate molecular profiling and advanced imaging. "
            "Update staging according to latest guidelines and evidence."
        ),
        entity_scope="Oncology, Pathology, Radiology",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AJCC Cancer Staging Manual, 8th Edition, 2017"
    ),
    DoctrineBlock(
        topic="Pediatrics - Growth and Development Monitoring",
        keywords=["pediatrics", "growth monitoring", "developmental milestones", "growth charts", "nutritional assessment", "screening", "early intervention", "developmental delay"],
        conclusion_template=(
            "Regular monitoring of growth and developmental milestones is essential for early identification of abnormalities. "
            "Timely intervention improves long-term outcomes."
        ),
        reasoning_framework=(
            "Growth monitoring involves serial measurement of anthropometric parameters (weight, height, head circumference) plotted on standardized growth charts (WHO, CDC). "
            "Deviations from expected growth trajectories may indicate nutritional deficiencies, chronic illness, or genetic disorders. "
            "Developmental surveillance assesses attainment of age-appropriate milestones in motor, language, social, and cognitive domains. "
            "Screening tools (e.g., Denver Developmental Screening Test) facilitate early detection of delays. "
            "Early intervention services improve outcomes in developmental disorders. "
            "Nutritional assessment includes dietary history and laboratory evaluation to identify malnutrition or obesity. "
            "Growth and development are influenced by genetic, environmental, and socioeconomic factors. "
            "Regular well-child visits provide opportunities for anticipatory guidance and immunization. "
            "Failure to monitor growth and development can delay diagnosis of serious conditions such as endocrine disorders or neurodevelopmental disabilities."
        ),
        key_factors=[
            "Anthropometric measurements accuracy",
            "Standardized growth charts usage",
            "Developmental milestone assessment",
            "Nutritional status evaluation",
            "Screening and early intervention",
            "Family and environmental context"
        ],
        primary_authority=[
            "American Academy of Pediatrics. Bright Futures Guidelines, 4th Edition, 2017.",
            "WHO Child Growth Standards, 2006.",
            "Sheldrick RC, Perrin EC. Developmental Screening in Primary Care: The Effectiveness of Current Practice and Recommendations for Improvement. Pediatrics. 2013;131(3):e751-e758.",
            "Centers for Disease Control and Prevention. Developmental Milestones, 2020."
        ],
        burden_holder="Pediatrician and primary care provider",
        adversary_position="Inadequate surveillance leading to missed developmental disorders",
        counter_arguments=[
            "Variability in milestone attainment",
            "Limited access to screening tools",
            "Parental underreporting or lack of awareness",
            "Cultural differences in development expectations",
            "Resource constraints in primary care"
        ],
        resolution_strategy=(
            "Implement standardized screening protocols and training. "
            "Engage families in education and follow-up. "
            "Refer promptly to specialists for abnormal findings."
        ),
        entity_scope="Pediatrics, Primary Care",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AAP Bright Futures Guidelines, 2017"
    ),
    DoctrineBlock(
        topic="Obstetrics - Prenatal Care and High-Risk Pregnancy Management",
        keywords=["obstetrics", "prenatal care", "high-risk pregnancy", "fetal monitoring", "maternal complications", "gestational diabetes", "preeclampsia", "ultrasound"],
        conclusion_template=(
            "Comprehensive prenatal care including risk assessment and fetal monitoring is vital to optimize maternal and fetal outcomes. "
            "Management of high-risk pregnancies requires multidisciplinary coordination."
        ),
        reasoning_framework=(
            "Prenatal care involves regular assessment of maternal and fetal health through history, physical examination, laboratory tests, and imaging. "
            "Identification of high-risk factors such as advanced maternal age, preexisting medical conditions, or obstetric complications allows tailored surveillance. "
            "Gestational diabetes and preeclampsia are common high-risk conditions requiring early detection and management to prevent adverse outcomes. "
            "Fetal monitoring includes ultrasound for growth and anatomy, non-stress tests, and biophysical profiles. "
            "Interventions may include pharmacologic therapy, lifestyle modification, and planned delivery timing and mode. "
            "Multidisciplinary teams including obstetricians, maternal-fetal medicine specialists, neonatologists, and social workers improve care. "
            "Patient education and psychosocial support are integral. "
            "Evidence-based guidelines inform screening intervals and management protocols. "
            "Documentation and communication across care providers ensure continuity. "
            "Emerging technologies such as telemedicine enhance access and monitoring."
        ),
        key_factors=[
            "Maternal risk factor identification",
            "Fetal growth and well-being assessment",
            "Screening for gestational diabetes and hypertension",
            "Multidisciplinary care coordination",
            "Patient education and support",
            "Use of evidence-based guidelines"
        ],
        primary_authority=[
            "American College of Obstetricians and Gynecologists (ACOG). Practice Bulletin No. 202: Gestational Hypertension and Preeclampsia, 2019.",
            "American Diabetes Association. Management of Diabetes in Pregnancy: Standards of Medical Care in Diabetes—2023.",
            "World Health Organization. WHO Recommendations on Antenatal Care for a Positive Pregnancy Experience, 2016.",
            "NICE Guidelines CG62: Antenatal Care for Uncomplicated Pregnancies, 2019."
        ],
        burden_holder="Obstetrician and maternal-fetal medicine team",
        adversary_position="Inadequate risk assessment leading to preventable complications",
        counter_arguments=[
            "Variability in access to prenatal care",
            "Patient noncompliance or late presentation",
            "Limitations in diagnostic accuracy",
            "Resource constraints in high-risk monitoring",
            "Psychosocial barriers affecting care"
        ],
        resolution_strategy=(
            "Implement standardized screening and monitoring protocols. "
            "Enhance patient education and engagement. "
            "Facilitate multidisciplinary collaboration and referral."
        ),
        entity_scope="Obstetrics, Maternal-Fetal Medicine",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ACOG Practice Bulletins, 2019"
    ),
    DoctrineBlock(
        topic="Psychiatry - DSM Diagnosis and Assessment",
        keywords=["psychiatry", "DSM-5", "diagnosis", "psychopathology", "clinical assessment", "differential diagnosis", "comorbidity", "structured interview"],
        conclusion_template=(
            "Accurate psychiatric diagnosis using DSM-5 criteria requires comprehensive clinical assessment and consideration of differential diagnoses. "
            "Structured interviews and standardized tools improve diagnostic reliability."
        ),
        reasoning_framework=(
            "The Diagnostic and Statistical Manual of Mental Disorders, Fifth Edition (DSM-5) provides standardized criteria for psychiatric diagnoses. "
            "Clinical assessment includes detailed history, mental status examination, and collateral information. "
            "Differential diagnosis considers medical, neurological, and substance-induced conditions that may mimic psychiatric disorders. "
            "Comorbidity is common and complicates diagnosis and treatment planning. "
            "Structured diagnostic interviews (e.g., SCID) enhance reliability and validity. "
            "Cultural and contextual factors influence symptom presentation and interpretation. "
            "Assessment of severity and functional impairment guides treatment urgency and modality. "
            "Ongoing evaluation is necessary due to symptom fluctuation and treatment response. "
            "Integration of biological, psychological, and social factors supports a biopsychosocial approach. "
            "Ethical considerations include informed consent and confidentiality."
        ),
        key_factors=[
            "Use of DSM-5 diagnostic criteria",
            "Comprehensive clinical assessment",
            "Differential diagnosis exclusion",
            "Assessment of comorbidities",
            "Use of structured interviews",
            "Cultural and contextual considerations"
        ],
        primary_authority=[
            "American Psychiatric Association. Diagnostic and Statistical Manual of Mental Disorders, 5th Edition (DSM-5). 2013.",
            "First MB, Williams JBW, Karg RS, Spitzer RL. Structured Clinical Interview for DSM-5 Disorders (SCID-5). 2015.",
            "Sadock BJ, Sadock VA, Ruiz P. Kaplan & Sadock's Synopsis of Psychiatry. 11th ed. Wolters Kluwer; 2015.",
            "World Health Organization. ICD-11 Classification of Mental and Behavioural Disorders, 2019."
        ],
        burden_holder="Psychiatrist and mental health clinician",
        adversary_position="Diagnostic overshadowing or misclassification leading to inappropriate treatment",
        counter_arguments=[
            "Symptom overlap among psychiatric disorders",
            "Influence of cultural factors on symptom expression",
            "Limitations of self-report and collateral information",
            "Variability in clinician expertise",
            "Stigma affecting disclosure and assessment"
        ],
        resolution_strategy=(
            "Employ standardized diagnostic tools and training. "
            "Incorporate multidisciplinary evaluation. "
            "Maintain cultural competence and ethical standards."
        ),
        entity_scope="Psychiatry, Clinical Psychology",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="DSM-5, APA, 2013"
    ),
    DoctrineBlock(
        topic="Orthopedics - Fracture Management and Healing",
        keywords=["orthopedics", "fracture", "bone healing", "reduction", "immobilization", "callus formation", "complications", "rehabilitation"],
        conclusion_template=(
            "Effective fracture management requires appropriate reduction and immobilization to facilitate bone healing. "
            "Monitoring for complications and rehabilitation optimize functional recovery."
        ),
        reasoning_framework=(
            "Bone fractures disrupt structural integrity, requiring realignment (reduction) and stabilization (immobilization) to restore function. "
            "Healing progresses through inflammatory, reparative (soft and hard callus formation), and remodeling phases. "
            "Factors influencing healing include fracture type, blood supply, patient age, comorbidities (e.g., diabetes), and mechanical stability. "
            "Complications such as nonunion, malunion, infection, and compartment syndrome must be anticipated and managed. "
            "Imaging guides assessment of alignment and healing progression. "
            "Surgical fixation (internal or external) is indicated for unstable or complex fractures. "
            "Early mobilization and physical therapy reduce stiffness and muscle atrophy. "
            "Pain management and prevention of thromboembolism are integral. "
            "Patient education on weight-bearing and activity restrictions improves outcomes. "
            "Advances include biologic adjuncts (bone grafts, growth factors) and minimally invasive techniques."
        ),
        key_factors=[
            "Fracture type and location",
            "Reduction quality and stability",
            "Biological factors affecting healing",
            "Complication prevention and management",
            "Rehabilitation protocols",
            "Imaging follow-up"
        ],
        primary_authority=[
            "Rockwood and Green's Fractures in Adults. 8th ed. Wolters Kluwer; 2015.",
            "Court-Brown CM, Caesar B. Epidemiology of adult fractures: a review. Injury. 2006;37(8):691-697.",
            "Brinker MR, O'Connor DP, Jensen MR, et al. The biology of fracture healing. Orthop Clin North Am. 2015;46(1):1-9.",
            "American Academy of Orthopaedic Surgeons (AAOS) Clinical Practice Guidelines."
        ],
        burden_holder="Orthopedic surgeon and rehabilitation team",
        adversary_position="Inadequate stabilization leading to poor healing or deformity",
        counter_arguments=[
            "Patient noncompliance with immobilization",
            "Delayed presentation or diagnosis",
            "Infection risk in open fractures",
            "Comorbidities impairing healing",
            "Inadequate pain control affecting rehabilitation"
        ],
        resolution_strategy=(
            "Ensure proper fracture assessment and stabilization. "
            "Educate patients and monitor compliance. "
            "Implement multidisciplinary rehabilitation and complication surveillance."
        ),
        entity_scope="Orthopedics, Rehabilitation Medicine",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Rockwood and Green's Fractures in Adults, 2015"
    ),
    DoctrineBlock(
        topic="Dermatology - Skin Lesion Biopsy and Diagnosis",
        keywords=["dermatology", "skin lesion", "biopsy", "histopathology", "dermatoscopy", "malignant melanoma", "basal cell carcinoma", "squamous cell carcinoma"],
        conclusion_template=(
            "Skin lesion biopsy is essential for definitive diagnosis of suspicious lesions. "
            "Integration of clinical and histopathologic findings guides management."
        ),
        reasoning_framework=(
            "Dermatologic evaluation of skin lesions includes clinical examination and dermatoscopy to assess morphology and vascular patterns. "
            "Biopsy techniques (shave, punch, excisional) are selected based on lesion characteristics and diagnostic needs. "
            "Histopathologic examination differentiates benign from malignant lesions and subtypes of skin cancer. "
            "Early detection of malignant melanoma significantly improves prognosis. "
            "Basal cell carcinoma and squamous cell carcinoma are common non-melanoma skin cancers with distinct histologic features. "
            "Margin assessment guides surgical management. "
            "Adjunctive immunohistochemical stains may aid diagnosis. "
            "Patient education on sun protection and skin surveillance reduces incidence. "
            "Teledermatology and AI tools are emerging for lesion assessment. "
            "Multidisciplinary collaboration with oncology and surgery optimizes care."
        ),
        key_factors=[
            "Clinical and dermatoscopic evaluation",
            "Appropriate biopsy technique",
            "Histopathologic interpretation",
            "Early detection of malignancy",
            "Margin status and surgical planning",
            "Patient education and follow-up"
        ],
        primary_authority=[
            "Fitzpatrick's Dermatology in General Medicine. 9th ed. McGraw-Hill; 2019.",
            "American Academy of Dermatology Guidelines for the Management of Melanoma.",
            "Dermatologic Surgery. Alam M, Ratner D. 2011.",
            "National Comprehensive Cancer Network (NCCN) Guidelines for Skin Cancer."
        ],
        burden_holder="Dermatologist and pathologist",
        adversary_position="Delayed or inadequate biopsy leading to missed diagnosis",
        counter_arguments=[
            "Sampling error in partial biopsies",
            "Interpretive variability among pathologists",
            "Patient reluctance for invasive procedures",
            "Overlap of benign and malignant features",
            "Limitations of dermatoscopy in certain lesions"
        ],
        resolution_strategy=(
            "Select biopsy method tailored to lesion. "
            "Use expert histopathologic review. "
            "Educate patients on importance of early diagnosis."
        ),
        entity_scope="Dermatology, Pathology",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AAD Guidelines for Melanoma Management"
    ),
    DoctrineBlock(
        topic="Gastroenterology - Endoscopy in Liver and Pancreas Disease",
        keywords=["gastroenterology", "endoscopy", "liver disease", "pancreatitis", "ERCP", "endoscopic ultrasound", "biliary obstruction", "variceal bleeding"],
        conclusion_template=(
            "Endoscopic procedures are vital for diagnosis and management of hepatobiliary and pancreatic diseases. "
            "Techniques such as ERCP and endoscopic ultrasound provide therapeutic and diagnostic capabilities."
        ),
        reasoning_framework=(
            "Endoscopy allows direct visualization and intervention in gastrointestinal tract and associated organs. "
            "Endoscopic retrograde cholangiopancreatography (ERCP) combines endoscopy and fluoroscopy to diagnose and treat biliary and pancreatic ductal diseases. "
            "Endoscopic ultrasound (EUS) provides high-resolution imaging and facilitates fine needle aspiration of lesions. "
            "Management of esophageal varices via band ligation or sclerotherapy reduces bleeding risk in portal hypertension. "
            "Endoscopic interventions can relieve biliary obstruction, drain pseudocysts, and manage strictures. "
            "Complications include pancreatitis, infection, and perforation, requiring careful patient selection and technique. "
            "Pre-procedure assessment includes coagulation status and sedation risk. "
            "Multidisciplinary collaboration with radiology and surgery enhances care. "
            "Advances in technology improve diagnostic yield and safety. "
            "Guidelines recommend endoscopic surveillance in high-risk populations."
        ),
        key_factors=[
            "Indications and contraindications for endoscopy",
            "Technical expertise and equipment",
            "Risk assessment and complication prevention",
            "Therapeutic capabilities (e.g., stenting, ligation)",
            "Integration with imaging and pathology",
            "Patient monitoring and follow-up"
        ],
        primary_authority=[
            "American Society for Gastrointestinal Endoscopy (ASGE) Guidelines.",
            "European Society of Gastrointestinal Endoscopy (ESGE) Clinical Guidelines.",
            "Cotton PB, et al. ERCP complications: prevention and management. Gastrointest Endosc. 2009;70(1):1-15.",
            "Sarin SK, et al. Prevention and management of gastroesophageal varices and variceal hemorrhage in cirrhosis. Hepatology. 2016."
        ],
        burden_holder="Gastroenterologist and endoscopy team",
        adversary_position="Inappropriate use or technique leading to complications",
        counter_arguments=[
            "Procedure-related risks in coagulopathic patients",
            "Incomplete visualization or sampling",
            "Patient intolerance or sedation complications",
            "Delayed recognition of adverse events",
            "Resource limitations affecting access"
        ],
        resolution_strategy=(
            "Adhere to guideline-based indications and protocols. "
            "Ensure skilled operators and appropriate patient preparation. "
            "Implement post-procedure monitoring and complication management."
        ),
        entity_scope="Gastroenterology, Hepatology",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASGE and ESGE Guidelines"
    ),
    DoctrineBlock(
        topic="Nephrology - Dialysis and Transplantation",
        keywords=["nephrology", "dialysis", "renal replacement therapy", "hemodialysis", "peritoneal dialysis", "kidney transplantation", "immunosuppression", "graft rejection"],
        conclusion_template=(
            "Dialysis and kidney transplantation are cornerstone therapies for end-stage renal disease. "
            "Optimizing modality selection and immunosuppressive management improves patient outcomes."
        ),
        reasoning_framework=(
            "End-stage renal disease (ESRD) requires renal replacement therapy to sustain life. "
            "Hemodialysis involves extracorporeal blood filtration, requiring vascular access and anticoagulation. "
            "Peritoneal dialysis uses the peritoneum as a dialysis membrane, allowing home-based therapy. "
            "Selection depends on patient factors, comorbidities, and lifestyle. "
            "Kidney transplantation offers superior survival and quality of life but requires lifelong immunosuppression. "
            "Immunosuppressive regimens balance rejection prevention with infection and malignancy risk. "
            "Graft rejection is monitored by clinical, laboratory, and biopsy findings. "
            "Complications include cardiovascular disease, mineral bone disorder, and anemia. "
            "Multidisciplinary care including nephrologists, surgeons, and transplant coordinators is essential. "
            "Advances in immunogenetics and desensitization protocols expand transplant eligibility."
        ),
        key_factors=[
            "Modality selection criteria",
            "Vascular and peritoneal access management",
            "Immunosuppressive therapy optimization",
            "Rejection monitoring and management",
            "Complication prevention",
            "Multidisciplinary coordination"
        ],
        primary_authority=[
            "National Kidney Foundation. KDOQI Clinical Practice Guidelines for Hemodialysis Adequacy, 2015.",
            "KDIGO Clinical Practice Guideline for the Care of Kidney Transplant Recipients, 2020.",
            "Daugirdas JT, Blake PG, Ing TS. Handbook of Dialysis. 5th ed. Wolters Kluwer; 2015.",
            "Meier-Kriesche HU, Kaplan B. Waiting time on dialysis as the strongest modifiable risk factor for renal transplant outcomes: a paired donor kidney analysis. Transplantation. 2002."
        ],
        burden_holder="Nephrologist and transplant team",
        adversary_position="Inadequate dialysis or immunosuppression leading to morbidity",
        counter_arguments=[
            "Patient nonadherence to treatment regimens",
            "Infection risk from immunosuppression",
            "Access complications and thrombosis",
            "Limited donor organ availability",
            "Complexity of managing comorbid conditions"
        ],
        resolution_strategy=(
            "Individualize dialysis and transplant plans. "
            "Provide patient education and support. "
            "Monitor closely for complications and adjust therapy."
        ),
        entity_scope="Nephrology, Transplant Medicine",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="KDIGO Guidelines, 2020"
    ),
    DoctrineBlock(
        topic="Pulmonology - Management of COPD and Asthma",
        keywords=["pulmonology", "COPD", "asthma", "bronchodilators", "inhaled corticosteroids", "pulmonary function tests", "exacerbation", "smoking cessation"],
        conclusion_template=(
            "Effective management of COPD and asthma requires accurate diagnosis, pharmacologic therapy, and lifestyle modification. "
            "Pulmonary function testing guides treatment and monitors disease progression."
        ),
        reasoning_framework=(
            "Chronic obstructive pulmonary disease (COPD) and asthma are common obstructive airway diseases with distinct pathophysiology. "
            "Diagnosis relies on clinical history, spirometry demonstrating airflow limitation, and exclusion of differential diagnoses. "
            "Pharmacologic treatment includes bronchodilators (beta-agonists, anticholinergics) and inhaled corticosteroids to reduce inflammation. "
            "Smoking cessation is the most effective intervention in COPD. "
            "Management of exacerbations involves systemic corticosteroids, antibiotics if indicated, and oxygen therapy. "
            "Pulmonary rehabilitation improves exercise tolerance and quality of life. "
            "Asthma control is assessed by symptom frequency, lung function, and exacerbation history. "
            "Stepwise therapy adjustments are based on control level. "
            "Patient education on inhaler technique and trigger avoidance is essential. "
            "Guidelines such as GOLD and GINA provide evidence-based management frameworks."
        ),
        key_factors=[
            "Accurate diagnosis with spirometry",
            "Pharmacologic therapy adherence",
            "Smoking cessation and environmental control",
            "Exacerbation prevention and management",
            "Pulmonary rehabilitation",
            "Patient education"
        ],
        primary_authority=[
            "Global Initiative for Chronic Obstructive Lung Disease (GOLD) Report, 2023.",
            "Global Initiative for Asthma (GINA) Report, 2023.",
            "Rabe KF, Watz H. Chronic obstructive pulmonary disease. Lancet. 2017;389(10082):1931-1940.",
            "National Asthma Education and Prevention Program Expert Panel Report 3 (EPR-3), 2007."
        ],
        burden_holder="Pulmonologist and primary care provider",
        adversary_position="Underdiagnosis and undertreatment leading to exacerbations",
        counter_arguments=[
            "Poor patient adherence to inhaler therapy",
            "Misdiagnosis or overlap syndromes",
            "Environmental and occupational exposures",
            "Limited access to pulmonary rehabilitation",
            "Comorbidities complicating management"
        ],
        resolution_strategy=(
            "Implement guideline-based diagnosis and treatment. "
            "Enhance patient education and support. "
            "Coordinate multidisciplinary care and follow-up."
        ),
        entity_scope="Pulmonology, Primary Care",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GOLD and GINA Guidelines, 2023"
    ),
    DoctrineBlock(
        topic="Endocrinology - Diabetes Mellitus Management",
        keywords=["endocrinology", "diabetes mellitus", "glycemic control", "insulin therapy", "oral hypoglycemics", "complications", "HbA1c", "self-monitoring"],
        conclusion_template=(
            "Comprehensive diabetes management includes glycemic control, complication prevention, and patient education. "
            "Individualized therapy optimizes outcomes."
        ),
        reasoning_framework=(
            "Diabetes mellitus is characterized by chronic hyperglycemia due to insulin deficiency or resistance. "
            "Management aims to maintain blood glucose within target ranges to prevent microvascular and macrovascular complications. "
            "Glycated hemoglobin (HbA1c) reflects average glycemia over preceding months and guides therapy adjustments. "
            "Treatment includes lifestyle modification, oral hypoglycemic agents (metformin, sulfonylureas, SGLT2 inhibitors), and insulin therapy. "
            "Monitoring for complications such as retinopathy, nephropathy, neuropathy, and cardiovascular disease is essential. "
            "Self-monitoring of blood glucose and continuous glucose monitoring enhance control. "
            "Patient education on diet, exercise, and medication adherence improves outcomes. "
            "Management is tailored to type 1 or type 2 diabetes and comorbidities. "
            "Emerging therapies target novel pathways and offer cardiovascular benefits. "
            "Multidisciplinary care including endocrinologists, diabetes educators, and dietitians is recommended."
        ),
        key_factors=[
            "Glycemic targets and monitoring",
            "Pharmacologic therapy selection",
            "Complication screening and prevention",
            "Patient education and self-management",
            "Individualized treatment plans",
            "Multidisciplinary care"
        ],
        primary_authority=[
            "American Diabetes Association. Standards of Medical Care in Diabetes—2023.",
            "International Diabetes Federation. IDF Diabetes Atlas, 10th Edition, 2021.",
            "Nathan DM, et al. Medical management of hyperglycemia in type 2 diabetes: a consensus algorithm. Diabetes Care. 2015.",
            "UK Prospective Diabetes Study (UKPDS) Group. Intensive blood-glucose control and risk of complications in type 2 diabetes. Lancet. 1998."
        ],
        burden_holder="Endocrinologist and primary care provider",
        adversary_position="Poor glycemic control due to inadequate therapy or adherence",
        counter_arguments=[
            "Patient barriers including socioeconomic factors",
            "Hypoglycemia risk limiting intensive control",
            "Therapeutic inertia among providers",
            "Comorbid conditions complicating management",
            "Limited access to diabetes education"
        ],
        resolution_strategy=(
            "Implement individualized treatment goals. "
            "Enhance patient education and support. "
            "Use multidisciplinary teams and regular follow-up."
        ),
        entity_scope="Endocrinology, Primary Care",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ADA Standards of Care, 2023"
    ),
    DoctrineBlock(
        topic="Immunology - Autoimmune Disease Pathogenesis and Management",
        keywords=["immunology", "autoimmune disease", "immune tolerance", "autoantibodies", "immunosuppression", "inflammation", "diagnosis", "treatment"],
        conclusion_template=(
            "Autoimmune diseases result from loss of immune tolerance leading to tissue damage. "
            "Diagnosis and management require immunologic evaluation and tailored immunosuppressive therapy."
        ),
        reasoning_framework=(
            "Autoimmune diseases arise when the immune system mounts a response against self-antigens due to breakdown of central or peripheral tolerance. "
            "Pathogenesis involves genetic predisposition, environmental triggers, and dysregulated immune responses including autoantibody production and T-cell mediated injury. "
            "Common diseases include systemic lupus erythematosus, rheumatoid arthritis, and multiple sclerosis. "
            "Diagnosis relies on clinical features, serologic markers (ANA, RF, anti-CCP), and imaging. "
            "Management includes immunosuppressive agents (corticosteroids, DMARDs, biologics) to control inflammation and prevent organ damage. "
            "Monitoring for treatment efficacy and adverse effects is critical. "
            "Emerging therapies target specific immune pathways to improve safety and efficacy. "
            "Patient education on disease course and infection risk is essential. "
            "Multidisciplinary care optimizes outcomes. "
            "Research continues to elucidate mechanisms and novel treatments."
        ),
        key_factors=[
            "Loss of immune tolerance mechanisms",
            "Autoantibody and cellular immune responses",
            "Clinical and serologic diagnosis",
            "Immunosuppressive therapy selection",
            "Monitoring and managing adverse effects",
            "Patient education and support"
        ],
        primary_authority=[
            "Rose NR, Mackay IR. The Autoimmune Diseases. 5th ed. Elsevier; 2014.",
            "Firestein GS, Budd RC, Gabriel SE, et al. Kelley’s Textbook of Rheumatology. 10th ed. Elsevier; 2017.",
            "American College of Rheumatology Guidelines.",
            "National Institute of Allergy and Infectious Diseases (NIAID) Autoimmune Disease Research."
        ],
        burden_holder="Immunologist and treating physician",
        adversary_position="Delayed diagnosis or inadequate immunosuppression leading to progression",
        counter_arguments=[
            "Heterogeneity of autoimmune disease presentations",
            "Risk of infection and malignancy with immunosuppression",
            "Patient adherence challenges",
            "Overlap syndromes complicating diagnosis",
            "Limited access to specialized care"
        ],
        resolution_strategy=(
            "Use comprehensive diagnostic evaluation. "
            "Tailor immunosuppressive regimens and monitor closely. "
            "Educate patients and coordinate multidisciplinary care."
        ),
        entity_scope="Immunology, Rheumatology",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ACR Guidelines and Rose & Mackay, 2014"
    ),
    DoctrineBlock(
        topic="Genetics - DNA Mutation and Inheritance Counseling",
        keywords=["genetics", "DNA mutation", "inheritance", "genetic counseling", "autosomal dominant", "autosomal recessive", "penetrance", "expressivity"],
        conclusion_template="Genetic counseling integrates molecular genetics, inheritance patterns, and risk assessment to guide clinical decision-making for patients and families affected by genetic conditions.",
        reasoning_framework="Genetic disorders arise from mutations in DNA including point mutations, deletions, insertions, and chromosomal abnormalities. Inheritance follows Mendelian patterns (autosomal dominant, autosomal recessive, X-linked) or complex multifactorial inheritance. Penetrance and expressivity affect phenotypic manifestation.",
        key_factors=["Mutation type and location", "Inheritance pattern", "Penetrance and expressivity", "Family history", "Genetic testing availability"],
        primary_authority=["ACMG Standards and Guidelines", "GeneReviews", "OMIM - Online Mendelian Inheritance in Man"],
        burden_holder="Genetic counselor and ordering physician",
        adversary_position="Genetic testing is unnecessary or the variant is of uncertain significance.",
        counter_arguments=["Family history pattern strongly suggests genetic etiology", "Genetic testing informs treatment decisions", "Cascade testing protects at-risk relatives"],
        resolution_strategy="Apply ACMG variant classification guidelines; integrate family history and clinical features with molecular results.",
        entity_scope="Genetic counselors, medical geneticists, patients and families",
        confidence=0.88,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="ACMG Standards and Guidelines for Clinical Genetics"
    ),
]

# =============================================
# SUB-ENGINE ORCHESTRATION
# =============================================

ENGINE_CONFIGS = {
    "MED01": {"name": "Pharmacology", "url": "http://med01/api"},
    "MED02": {"name": "Toxicology", "url": "http://med02/api"},
    "MED03": {"name": "Emergency Medicine", "url": "http://med03/api"},
    "MED04": {"name": "Radiology", "url": "http://med04/api"},
    "MED05": {"name": "Pathology", "url": "http://med05/api"},
    "MED06": {"name": "Infectious Disease", "url": "http://med06/api"},
    "MED07": {"name": "Surgery", "url": "http://med07/api"},
    "MED08": {"name": "Cardiology", "url": "http://med08/api"},
    "MED09": {"name": "Neurology", "url": "http://med09/api"},
    "MED10": {"name": "Oncology", "url": "http://med10/api"},
    "MED11": {"name": "Pediatrics", "url": "http://med11/api"},
    "MED12": {"name": "Obstetrics", "url": "http://med12/api"},
    "MED13": {"name": "Psychiatry", "url": "http://med13/api"},
    "MED14": {"name": "Orthopedics", "url": "http://med14/api"},
    "MED15": {"name": "Dermatology", "url": "http://med15/api"},
    "MED16": {"name": "Gastroenterology", "url": "http://med16/api"},
    "MED17": {"name": "Nephrology", "url": "http://med17/api"},
    "MED18": {"name": "Pulmonology", "url": "http://med18/api"},
    "MED19": {"name": "Endocrinology", "url": "http://med19/api"},
    "MED20": {"name": "Immunology", "url": "http://med20/api"},
    "MED21": {"name": "Genetics", "url": "http://med21/api"},
}

DOMAIN_KEYWORDS = {
    "Pharmacology": ["drug", "medication", "dose", "pharmacokinetics", "pharmacodynamics", "side effect"],
    "Toxicology": ["poison", "toxicity", "overdose", "antidote", "toxin"],
    "Emergency Medicine": ["trauma", "resuscitation", "emergency", "acute", "shock"],
    "Radiology": ["x-ray", "MRI", "CT", "ultrasound", "imaging"],
    "Pathology": ["biopsy", "histology", "cytology", "pathology", "specimen"],
    "Infectious Disease": ["infection", "virus", "bacteria", "antibiotic", "sepsis"],
    "Surgery": ["operation", "surgical", "procedure", "incision", "anesthesia"],
    "Cardiology": ["heart", "cardiac", "ECG", "arrhythmia", "myocardial"],
    "Neurology": ["brain", "neurological", "stroke", "seizure", "nerve"],
    "Oncology": ["cancer", "tumor", "chemotherapy", "malignancy", "oncology"],
    "Pediatrics": ["child", "pediatric", "infant", "neonate", "adolescent"],
    "Obstetrics": ["pregnancy", "labor", "delivery", "obstetric", "gestation"],
    "Psychiatry": ["mental", "psychiatric", "depression", "anxiety", "psychosis"],
    "Orthopedics": ["bone", "fracture", "joint", "orthopedic", "ligament"],
    "Dermatology": ["skin", "rash", "dermatology", "eczema", "psoriasis"],
    "Gastroenterology": ["liver", "gut", "stomach", "intestine", "gastro"],
    "Nephrology": ["kidney", "renal", "nephrology", "dialysis", "glomerulus"],
    "Pulmonology": ["lung", "respiratory", "asthma", "COPD", "pulmonary"],
    "Endocrinology": ["hormone", "diabetes", "thyroid", "endocrine", "insulin"],
    "Immunology": ["immune", "immunology", "antibody", "autoimmune", "immunosuppression"],
    "Genetics": ["gene", "genetic", "mutation", "chromosome", "hereditary"],
}

ENGINE_DOMAIN_MAP = {eid: cfg["name"] for eid, cfg in ENGINE_CONFIGS.items()}

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

class IssueCategory(str, Enum):
    PHARMACOLOGY = "Pharmacology"
    TOXICOLOGY = "Toxicology"
    EMERGENCY_MEDICINE = "Emergency Medicine"
    RADIOLOGY = "Radiology"
    PATHOLOGY = "Pathology"
    INFECTIOUS_DISEASE = "Infectious Disease"
    SURGERY = "Surgery"
    CARDIOLOGY = "Cardiology"
    NEUROLOGY = "Neurology"
    ONCOLOGY = "Oncology"
    PEDIATRICS = "Pediatrics"
    OBSTETRICS = "Obstetrics"
    PSYCHIATRY = "Psychiatry"
    ORTHOPEDICS = "Orthopedics"
    DERMATOLOGY = "Dermatology"
    GASTROENTEROLOGY = "Gastroenterology"
    NEPHROLOGY = "Nephrology"
    PULMONOLOGY = "Pulmonology"
    ENDOCRINOLOGY = "Endocrinology"
    IMMUNOLOGY = "Immunology"
    GENETICS = "Genetics"

class QueryRequest:
    def __init__(self, text: str, mode: str = "default", meta: Optional[Dict[str, Any]] = None):
        self.text = text
        self.mode = mode
        self.meta = meta or {}

class RoutingDecision:
    def __init__(self, engines: List[str], categories: List[IssueCategory], scores: Dict[str, float]):
        self.engines = engines
        self.categories = categories
        self.scores = scores

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, domain: str):
        self.engine_id = engine_id
        self.url = url
        self.domain = domain

class SubEngineResponse:
    def __init__(self, engine_id: str, response: Any, status: SubEngineStatus, meta: Optional[Dict[str, Any]] = None):
        self.engine_id = engine_id
        self.response = response
        self.status = status
        self.meta = meta or {}

# --- Circuit Breaker ---

class CircuitBreaker:
    def __init__(self, engine_id: str, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.engine_id = engine_id
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.last_failure_time = 0
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

    def allow_request(self) -> bool:
        with self.lock:
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
            else:
                return False

    def handle_result(self, success: bool):
        if success:
            self.record_success()
        else:
            self.record_failure()

# --- SubEngine Health Monitor ---

class SubEngineHealthMonitor:
    def __init__(self, engine_configs: Dict[str, Dict[str, Any]], ttl: int = 60):
        self.engine_configs = engine_configs
        self.ttl = ttl
        self.health_cache: Dict[str, Tuple[SubEngineStatus, float]] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {
            eid: CircuitBreaker(eid) for eid in engine_configs
        }

    async def _ping_engine(self, url: str, timeout: int = 5) -> SubEngineStatus:
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
        if engine_id in self.health_cache:
            status, ts = self.health_cache[engine_id]
            if now - ts < self.ttl:
                return status
        url = self.engine_configs[engine_id]["url"]
        loop = asyncio.get_event_loop()
        status = loop.run_until_complete(self._ping_engine(url))
        self.health_cache[engine_id] = (status, now)
        return status

    def check_all_health(self) -> Dict[str, SubEngineStatus]:
        now = time.time()
        results = {}
        loop = asyncio.get_event_loop()
        for eid, cfg in self.engine_configs.items():
            if eid in self.health_cache:
                status, ts = self.health_cache[eid]
                if now - ts < self.ttl:
                    results[eid] = status
                    continue
            status = loop.run_until_complete(self._ping_engine(cfg["url"]))
            self.health_cache[eid] = (status, now)
            results[eid] = status
        return results

    def get_healthy_engines(self) -> List[str]:
        healths = self.check_all_health()
        healthy = [
            eid for eid, status in healths.items()
            if status == SubEngineStatus.HEALTHY and self.circuit_breakers[eid].allow_request()
        ]
        return healthy

    def get_circuit_breaker(self, engine_id: str) -> CircuitBreaker:
        return self.circuit_breakers[engine_id]

# --- Query Router ---

class QueryRouter:
    def __init__(self, engine_configs: Dict[str, Dict[str, Any]], health_monitor: SubEngineHealthMonitor):
        self.engine_configs = engine_configs
        self.health_monitor = health_monitor

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text_lower = text.lower()
        matched_categories = []
        for domain, keywords in DOMAIN_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in text_lower:
                    matched_categories.append(IssueCategory(domain))
                    break
        if not matched_categories:
            matched_categories.append(IssueCategory.EMERGENCY_MEDICINE)
        return matched_categories

    def _select_engines(self, categories: List[IssueCategory], mode: str) -> List[SubEngineConfig]:
        healthy_eids = self.health_monitor.get_healthy_engines()
        selected = []
        for cat in categories:
            for eid, cfg in self.engine_configs.items():
                if cfg["name"] == cat and eid in healthy_eids:
                    selected.append(SubEngineConfig(eid, cfg["url"], cfg["name"]))
        if not selected:
            for eid in healthy_eids:
                cfg = self.engine_configs[eid]
                selected.append(SubEngineConfig(eid, cfg["url"], cfg["name"]))
        return selected

    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        # Example: if query.meta has 'urgent', always include Emergency Medicine
        rules_engines = []
        if query.meta.get("urgent"):
            for eid, cfg in self.engine_configs.items():
                if cfg["name"] == "Emergency Medicine":
                    rules_engines.append(eid)
        return rules_engines

    def _score_engine_relevance(self, engine: SubEngineConfig, query: QueryRequest) -> float:
        domain_keywords = DOMAIN_KEYWORDS.get(engine.domain, [])
        text_lower = query.text.lower()
        score = 0.0
        for kw in domain_keywords:
            if kw.lower() in text_lower:
                score += 1.0
        if engine.domain == "Emergency Medicine" and query.meta.get("urgent"):
            score += 2.0
        return score

    def _handle_engine_failure(self, engine_id: str, error: Exception) -> List[str]:
        # Fallback: Remove failed engine, try closest domain
        failed_domain = self.engine_configs[engine_id]["name"]
        fallback_engines = []
        for eid, cfg in self.engine_configs.items():
            if cfg["name"] != failed_domain and self.health_monitor.get_circuit_breaker(eid).allow_request():
                fallback_engines.append(eid)
        return fallback_engines

    def route_query(self, query: QueryRequest) -> RoutingDecision:
        categories = self._classify_domain(query.text)
        selected_configs = self._select_engines(categories, query.mode)
        rule_engines = self._apply_routing_rules(query)
        selected_eids = [cfg.engine_id for cfg in selected_configs]
        for eid in rule_engines:
            if eid not in selected_eids:
                selected_eids.append(eid)
        scores = {}
        for cfg in selected_configs:
            scores[cfg.engine_id] = self._score_engine_relevance(cfg, query)
        for eid in rule_engines:
            cfg = self.engine_configs[eid]
            scores[eid] = scores.get(eid, 0.0) + 2.0
        return RoutingDecision(selected_eids, categories, scores)

# --- SubEngine Orchestrator ---

class SubEngineOrchestrator:
    def __init__(self, engine_configs: Dict[str, Dict[str, Any]], health_monitor: SubEngineHealthMonitor):
        self.engine_configs = engine_configs
        self.health_monitor = health_monitor

    async def _call_sub_engine(self, engine_config: SubEngineConfig, query: QueryRequest) -> SubEngineResponse:
        cb = self.health_monitor.get_circuit_breaker(engine_config.engine_id)
        if not cb.allow_request():
            return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, {"circuit_breaker": "open"})
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{engine_config.url}/query",
                    json={"text": query.text, "mode": query.mode, "meta": query.meta},
                    timeout=10
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        cb.handle_result(True)
                        return SubEngineResponse(engine_config.engine_id, data, SubEngineStatus.HEALTHY)
                    else:
                        cb.handle_result(False)
                        return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, {"http_status": resp.status})
        except Exception as e:
            cb.handle_result(False)
            return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, {"error": str(e)})

    async def dispatch_query(self, query: QueryRequest, engines: List[SubEngineConfig]) -> List[SubEngineResponse]:
        tasks = [self._call_sub_engine(cfg, query) for cfg in engines]
        responses = await asyncio.gather(*tasks)
        return responses

    async def dispatch_parallel(self, query: QueryRequest, engines: List[SubEngineConfig]) -> Dict[str, Any]:
        responses = await self.dispatch_query(query, engines)
        merged = self._merge_responses(responses)
        return merged

    async def dispatch_cascade(self, query: QueryRequest, engines: List[SubEngineConfig]) -> Any:
        for cfg in engines:
            resp = await self._call_sub_engine(cfg, query)
            if resp.status == SubEngineStatus.HEALTHY and resp.response is not None:
                return resp.response
        return {"error": "All sub-engines failed"}

    def _merge_responses(self, responses: List[SubEngineResponse]) -> Dict[str, Any]:
        merged = {}
        for resp in responses:
            merged[resp.engine_id] = resp.response
        return merged

    def _resolve_conflicts(self, responses: List[SubEngineResponse]) -> Any:
        # Example: Majority consensus, fallback to Emergency Medicine
        valid_resps = [resp for resp in responses if resp.status == SubEngineStatus.HEALTHY and resp.response is not None]
        if not valid_resps:
            return {"error": "No valid responses"}
        response_values = [resp.response for resp in valid_resps]
        # Simple consensus: if all responses are dicts with 'answer', pick most common
        answers = [r.get("answer") for r in response_values if isinstance(r, dict) and "answer" in r]
        if answers:
            from collections import Counter
            most_common = Counter(answers).most_common(1)
            if most_common:
                return {"answer": most_common[0][0], "consensus": most_common[0][1]}
        # Fallback: first valid response
        return response_values[0]

# --- Example Usage ---

# health_monitor = SubEngineHealthMonitor(ENGINE_CONFIGS)
# router = QueryRouter(ENGINE_CONFIGS, health_monitor)
# orchestrator = SubEngineOrchestrator(ENGINE_CONFIGS, health_monitor)

# query = QueryRequest("Patient with acute chest pain and ECG changes", mode="default", meta={"urgent": True})
# routing_decision = router.route_query(query)
# selected_engines = [SubEngineConfig(eid, ENGINE_CONFIGS[eid]["url"], ENGINE_CONFIGS[eid]["name"]) for eid in routing_decision.engines]

# loop = asyncio.get_event_loop()
# responses = loop.run_until_complete(orchestrator.dispatch_parallel(query, selected_engines))
# consensus = orchestrator._resolve_conflicts([SubEngineResponse(eid, responses[eid], SubEngineStatus.HEALTHY) for eid in responses])
# print(consensus)

class AuthorityLevel(Enum):
    CONSTITUTIONAL = auto()
    STATUTORY = auto()
    REGULATORY = auto()
    CASE_LAW = auto()
    TREATISE = auto()
    PRACTICE = auto()

# Authority weights for conflict resolution (higher is more authoritative)
authority_weights: Dict[AuthorityLevel, int] = {
    AuthorityLevel.CONSTITUTIONAL: 100,
    AuthorityLevel.STATUTORY: 90,
    AuthorityLevel.REGULATORY: 80,
    AuthorityLevel.CASE_LAW: 70,
    AuthorityLevel.TREATISE: 60,
    AuthorityLevel.PRACTICE: 50,
}

def resolve_authority_conflict(sources: List[AuthorityLevel]) -> AuthorityLevel:
    """
    Given a list of authority sources, return the dominant authority level.
    If multiple have the same weight, return the one with highest enum order.
    """
    if not sources:
        raise ValueError("No authority sources provided")
    max_weight = -1
    dominant = None
    for source in sources:
        weight = authority_weights.get(source, 0)
        if weight > max_weight:
            max_weight = weight
            dominant = source
        elif weight == max_weight:
            # Tie-breaker: higher enum value wins (later declared is more specific)
            if source.value > dominant.value:
                dominant = source
    return dominant

# ----------------------------------------
# EPISTEMIC GUARDRAILS
# ----------------------------------------

BANNED_PHRASES = [
    "clearly",
    "obviously",
    "without doubt",
    "undeniably",
    "incontrovertibly",
    "unequivocally",
    "beyond question",
    "without question",
    "certainly",
    "definitely",
    "absolutely",
    "incontestably",
    "indisputably",
    "categorically",
    "unquestionably",
    "manifestly",
    "patently",
    "decidedly",
    "irrefutably",
    "infallibly",
    "inarguably",
    "plainly",
    "evidently",
    "surely",
    "positively",
    "undoubtedly",
    "conclusively",
    "resolutely",
    "firmly",
    "assuredly",
    "clearly evident",
    "without any doubt",
]

def apply_epistemic_guardrails(text: str) -> Tuple[str, str]:
    """
    Remove banned phrases from text and append a disclosure caveat.
    Returns cleaned_text and disclosure_caveat.
    """
    pattern = re.compile(r'\b(' + '|'.join(re.escape(p) for p in BANNED_PHRASES) + r')\b', flags=re.IGNORECASE)
    cleaned_text = pattern.sub("", text)
    # Remove extra spaces after removal
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()
    disclosure_caveat = ("Note: This analysis avoids absolute assertions and acknowledges "
                         "the inherent uncertainty and variability in medical and legal interpretations.")
    return cleaned_text, disclosure_caveat

class ConfidenceLevel(Enum):
    DEFENSIBLE = auto()
    AGGRESSIVE = auto()
    DISCLOSURE = auto()
    HIGH_RISK = auto()

def confidence_stratification(confidence_score: float, risk_factors: Dict[str, Any]) -> ConfidenceLevel:
    """
    Stratify confidence based on score and risk factors.
    confidence_score: 0.0 to 1.0
    risk_factors: dict with keys like 'data_quality', 'source_reliability', 'conflict_level'
    """
    # Basic thresholds
    if confidence_score >= 0.85 and risk_factors.get('conflict_level', 0) < 0.2:
        return ConfidenceLevel.DEFENSIBLE
    elif confidence_score >= 0.65:
        return ConfidenceLevel.AGGRESSIVE
    elif confidence_score >= 0.4:
        return ConfidenceLevel.DISCLOSURE
    else:
        return ConfidenceLevel.HIGH_RISK

# ----------------------------------------
# FACT FRAGILITY SCORING
# ----------------------------------------

def score_fact_fragility(fact: str) -> Dict[str, float]:
    """
    Score a fact for:
    - verifiability (0-1, higher is more verifiable)
    - recharacterization_risk (0-1, higher is more risk)
    - testimony_dependence (0-1, higher means more dependent on witness/testimony)
    """
    # Placeholder heuristics:
    verifiability = 0.5
    recharacterization_risk = 0.5
    testimony_dependence = 0.5

    # Verifiability heuristics: presence of numeric data, references, citations
    if re.search(r'\b(study|trial|data|evidence|report|citation|reference|meta-analysis|RCT|randomized)\b', fact, re.I):
        verifiability += 0.3
    if re.search(r'\b(\d{4}|\d+ patients|percent|%)\b', fact):
        verifiability += 0.2

    # Recharacterization risk heuristics: vague terms, subjective adjectives
    vague_terms = ['often', 'sometimes', 'may', 'could', 'likely', 'possible', 'suggests', 'appears']
    if any(term in fact.lower() for term in vague_terms):
        recharacterization_risk += 0.3

    # Testimony dependence heuristics: mentions of witness, patient report, subjective experience
    if re.search(r'\b(patient report|witness|testimony|subjective|self-reported|interview)\b', fact, re.I):
        testimony_dependence += 0.3

    # Clamp values between 0 and 1
    verifiability = min(max(verifiability, 0.0), 1.0)
    recharacterization_risk = min(max(recharacterization_risk, 0.0), 1.0)
    testimony_dependence = min(max(testimony_dependence, 0.0), 1.0)

    return {
        'verifiability': verifiability,
        'recharacterization_risk': recharacterization_risk,
        'testimony_dependence': testimony_dependence,
    }

# ----------------------------------------
# SEMANTIC NORMALIZATION
# ----------------------------------------

# 50+ domain term mappings for medical and legal domain normalization
DOMAIN_TERM_MAPPINGS = {
    "myocardial infarction": "heart attack",
    "cerebrovascular accident": "stroke",
    "hypertension": "high blood pressure",
    "diabetes mellitus": "diabetes",
    "chronic obstructive pulmonary disease": "COPD",
    "coronary artery disease": "CAD",
    "atrial fibrillation": "AFib",
    "gastroesophageal reflux disease": "GERD",
    "acute respiratory distress syndrome": "ARDS",
    "congestive heart failure": "CHF",
    "computed tomography": "CT scan",
    "magnetic resonance imaging": "MRI",
    "electrocardiogram": "ECG",
    "electroencephalogram": "EEG",
    "blood pressure": "BP",
    "body mass index": "BMI",
    "intravenous": "IV",
    "oral administration": "PO",
    "intramuscular": "IM",
    "subcutaneous": "SC",
    "prescription": "Rx",
    "over the counter": "OTC",
    "placebo controlled trial": "RCT",
    "randomized controlled trial": "RCT",
    "adverse event": "side effect",
    "non-steroidal anti-inflammatory drug": "NSAID",
    "acetaminophen": "paracetamol",
    "computed tomography angiography": "CTA",
    "positron emission tomography": "PET scan",
    "standard of care": "SOC",
    "intensive care unit": "ICU",
    "emergency room": "ER",
    "primary care physician": "PCP",
    "electronic health record": "EHR",
    "patient reported outcome": "PRO",
    "health related quality of life": "HRQoL",
    "pharmacokinetics": "PK",
    "pharmacodynamics": "PD",
    "placebo": "inactive treatment",
    "double blind": "double-blind",
    "single blind": "single-blind",
    "adverse drug reaction": "ADR",
    "clinical practice guideline": "CPG",
    "informed consent": "IC",
    "institutional review board": "IRB",
    "health insurance portability and accountability act": "HIPAA",
    "food and drug administration": "FDA",
    "center for disease control and prevention": "CDC",
    "world health organization": "WHO",
    "medical device": "device",
    "health care provider": "HCP",
    "electronic medical record": "EMR",
    "patient safety": "safety",
}

def normalize_query(text: str) -> str:
    """
    Normalize domain-specific terms in the input text to standardized terms.
    Case insensitive replacement.
    """
    normalized_text = text.lower()
    # Sort keys by length descending to avoid partial replacements
    sorted_terms = sorted(DOMAIN_TERM_MAPPINGS.keys(), key=len, reverse=True)
    for term in sorted_terms:
        replacement = DOMAIN_TERM_MAPPINGS[term]
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        normalized_text = pattern.sub(replacement, normalized_text)
    return normalized_text

# ----------------------------------------
# DEEP ANALYSIS
# ----------------------------------------

def multi_doctrine_decomposition(query: str) -> List[str]:
    """
    Decompose a complex query into sub-issues based on doctrine keywords.
    For medical legal domain, doctrines might be: consent, negligence, causation, damages, etc.
    """
    doctrines = [
        "informed consent",
        "standard of care",
        "causation",
        "damages",
        "negligence",
        "liability",
        "statute of limitations",
        "medical malpractice",
        "patient autonomy",
        "confidentiality",
        "risk disclosure",
        "treatment efficacy",
        "adverse event",
        "clinical trial validity",
        "evidence admissibility",
        "causal link",
        "proximate cause",
        "breach of duty",
        "comparative fault",
        "res ipsa loquitur",
    ]
    sub_issues = []
    lowered = query.lower()
    for doctrine in doctrines:
        if doctrine in lowered:
            sub_issues.append(doctrine)
    # If no doctrines matched, fallback to splitting by punctuation and keywords
    if not sub_issues:
        # Simple heuristic: split by commas and "and"
        parts = re.split(r',| and | or ', query)
        sub_issues = [part.strip() for part in parts if len(part.strip()) > 10]
    return sub_issues

def build_interaction_dag(issues: List[str]) -> nx.DiGraph:
    """
    Build a dependency graph (DAG) of issues.
    For simplicity, assume some generic dependencies based on known doctrine relations.
    """
    dag = nx.DiGraph()
    for issue in issues:
        dag.add_node(issue)

    # Example dependencies (hardcoded for demo)
    dependencies = {
        "causation": ["negligence"],
        "damages": ["causation"],
        "liability": ["negligence", "damages"],
        "breach of duty": ["standard of care"],
        "standard of care": ["informed consent"],
        "risk disclosure": ["informed consent"],
        "comparative fault": ["liability"],
        "proximate cause": ["causation"],
        "res ipsa loquitur": ["negligence"],
    }

    for dependent, prereqs in dependencies.items():
        if dependent in issues:
            for prereq in prereqs:
                if prereq in issues:
                    dag.add_edge(prereq, dependent)

    # Ensure DAG is acyclic, if cycles detected, remove edges arbitrarily
    try:
        cycles = list(nx.find_cycle(dag, orientation='original'))
        for edge in cycles:
            dag.remove_edge(edge[0], edge[1])
    except nx.NetworkXNoCycle:
        pass

    return dag

def eight_step_resolution(query: str, doctrines: List[str], sub_engine_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform an eight-step resolution process:
    1. Issue identification
    2. Rule statement
    3. Application of facts
    4. Counterarguments
    5. Authority weighing
    6. Confidence stratification
    7. Epistemic guardrails application
    8. Conclusion synthesis
    """
    resolution = {}

    # 1. Issue identification
    resolution['issues'] = doctrines

    # 2. Rule statement (simplified: fetch from sub_engine_results or doctrine database)
    rules = {}
    for doctrine in doctrines:
        rules[doctrine] = sub_engine_results.get(doctrine, {}).get('rule', f"Rule for {doctrine} not found.")
    resolution['rules'] = rules

    # 3. Application of facts (simplified: gather facts from sub_engine_results)
    facts_application = {}
    for doctrine in doctrines:
        facts_application[doctrine] = sub_engine_results.get(doctrine, {}).get('facts', "No facts applied.")
    resolution['facts_application'] = facts_application

    # 4. Counterarguments (simplified: from sub_engine_results)
    counterarguments = {}
    for doctrine in doctrines:
        counterarguments[doctrine] = sub_engine_results.get(doctrine, {}).get('counterarguments', "No counterarguments.")
    resolution['counterarguments'] = counterarguments

    # 5. Authority weighing
    authority_sources = []
    for doctrine in doctrines:
        auths = sub_engine_results.get(doctrine, {}).get('authority_sources', [])
        authority_sources.extend(auths)
    dominant_authority = resolve_authority_conflict(authority_sources) if authority_sources else None
    resolution['dominant_authority'] = dominant_authority.name if dominant_authority else "Unknown"

    # 6. Confidence stratification
    # Aggregate confidence scores from sub_engine_results
    confidence_scores = [sub_engine_results.get(d, {}).get('confidence', 0.5) for d in doctrines]
    avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
    risk_level = max(sub_engine_results.get(d, {}).get('risk_level', 0) for d in doctrines) if doctrines else 0
    confidence_level = confidence_stratification(avg_confidence, {'conflict_level': risk_level})
    resolution['confidence_level'] = confidence_level.name

    # 7. Epistemic guardrails application
    conclusion_text = sub_engine_results.get('conclusion', "No conclusion provided.")
    cleaned_text, caveat = apply_epistemic_guardrails(conclusion_text)
    resolution['cleaned_conclusion'] = cleaned_text
    resolution['disclosure_caveat'] = caveat

    # 8. Conclusion synthesis
    resolution['final_conclusion'] = f"{cleaned_text} {caveat}"

    return resolution

def zoned_analysis(conclusion: str) -> Dict[str, Any]:
    """
    Tag conclusion with zones: PLANNING, REPORTING, AUDIT
    Based on keywords and content.
    """
    zones = set()
    lower_conclusion = conclusion.lower()
    if any(word in lower_conclusion for word in ['plan', 'recommend', 'suggest', 'propose']):
        zones.add('PLANNING')
    if any(word in lower_conclusion for word in ['report', 'findings', 'results', 'observed']):
        zones.add('REPORTING')
    if any(word in lower_conclusion for word in ['audit', 'review', 'compliance', 'verification']):
        zones.add('AUDIT')
    if not zones:
        zones.add('REPORTING')  # default zone
    return {
        'zones': list(zones),
        'tagged_conclusion': conclusion,
    }

# ----------------------------------------
# THREE-LAYER RESPONSE SYSTEM
# ----------------------------------------

# Simulated doctrine cache with keywords and cached analysis
DOCTRINE_CACHE = {
    "informed consent": {
        "keywords": ["informed consent", "consent", "disclosure"],
        "analysis": "Cached analysis on informed consent doctrine.",
        "timestamp": time.time(),
    },
    "negligence": {
        "keywords": ["negligence", "duty of care", "breach"],
        "analysis": "Cached analysis on negligence doctrine.",
        "timestamp": time.time(),
    },
    "causation": {
        "keywords": ["causation", "cause", "effect"],
        "analysis": "Cached analysis on causation doctrine.",
        "timestamp": time.time(),
    },
    # Add more cached doctrines as needed
}

def doctrine_cache_lookup(query: str, timeout_ms: int = 200) -> Optional[str]:
    """
    Layer 1: Doctrine cache lookup within 0-200ms.
    Match keywords and return cached analysis if found.
    """
    start_time = time.time()
    lowered_query = query.lower()
    for doctrine, data in DOCTRINE_CACHE.items():
        for keyword in data['keywords']:
            if keyword in lowered_query:
                elapsed_ms = (time.time() - start_time) * 1000
                if elapsed_ms <= timeout_ms:
                    return data['analysis']
                else:
                    return None
    return None

# Simulated sub-engines for semantic search and routing
class SubEngine:
    def __init__(self, name: str):
        self.name = name

    def analyze(self, query: str) -> Dict[str, Any]:
        """
        Simulate analysis by sub-engine.
        """
        # Placeholder: return dummy results with some delay
        time.sleep(0.05)  # simulate processing delay
        return {
            'rule': f"Rule extracted by {self.name} for query.",
            'facts': f"Facts applied by {self.name}.",
            'counterarguments': f"Counterarguments by {self.name}.",
            'authority_sources': [AuthorityLevel.STATUTORY],
            'confidence': 0.75,
            'risk_level': 0.1,
        }

SUB_ENGINES = {
    "consent_engine": SubEngine("ConsentEngine"),
    "negligence_engine": SubEngine("NegligenceEngine"),
    "causation_engine": SubEngine("CausationEngine"),
    "damages_engine": SubEngine("DamagesEngine"),
    "default_engine": SubEngine("DefaultEngine"),
}

def semantic_search_and_sub_engine_routing(query: str) -> Dict[str, Any]:
    """
    Layer 2: Semantic search + sub-engine routing.
    Dispatch to relevant sub-engines based on keywords.
    """
    lowered_query = query.lower()
    results = {}
    # Simple keyword based routing
    if any(k in lowered_query for k in ["consent", "disclosure", "autonomy"]):
        results['informed consent'] = SUB_ENGINES["consent_engine"].analyze(query)
    if any(k in lowered_query for k in ["negligence", "duty", "breach"]):
        results['negligence'] = SUB_ENGINES["negligence_engine"].analyze(query)
    if any(k in lowered_query for k in ["cause", "causation", "effect"]):
        results['causation'] = SUB_ENGINES["causation_engine"].analyze(query)
    if any(k in lowered_query for k in ["damages", "compensation", "loss"]):
        results['damages'] = SUB_ENGINES["damages_engine"].analyze(query)
    if not results:
        # Default engine fallback
        results['default'] = SUB_ENGINES["default_engine"].analyze(query)
    return results

def deep_multi_engine_analysis(query: str, doctrines: List[str]) -> Dict[str, Any]:
    """
    Layer 3: Deep multi-engine analysis.
    Parallel dispatch to sub-engines, merge results, resolve conflicts.
    """
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_doctrine = {}
        for doctrine in doctrines:
            # Select sub-engine based on doctrine name
            engine_key = None
            if "consent" in doctrine:
                engine_key = "consent_engine"
            elif "negligence" in doctrine:
                engine_key = "negligence_engine"
            elif "causation" in doctrine:
                engine_key = "causation_engine"
            elif "damages" in doctrine:
                engine_key = "damages_engine"
            else:
                engine_key = "default_engine"
            engine = SUB_ENGINES.get(engine_key, SUB_ENGINES["default_engine"])
            future = executor.submit(engine.analyze, query)
            future_to_doctrine[future] = doctrine

        for future in concurrent.futures.as_completed(future_to_doctrine):
            doctrine = future_to_doctrine[future]
            try:
                result = future.result()
                results[doctrine] = result
            except Exception:
                results[doctrine] = {
                    'rule': "Error in analysis.",
                    'facts': "",
                    'counterarguments': "",
                    'authority_sources': [],
                    'confidence': 0.0,
                    'risk_level': 1.0,
                }

    # Conflict resolution example: if multiple doctrines have conflicting authority sources, resolve
    all_authorities = []
    for res in results.values():
        all_authorities.extend(res.get('authority_sources', []))
    dominant_authority = resolve_authority_conflict(all_authorities) if all_authorities else None
    results['dominant_authority'] = dominant_authority.name if dominant_authority else "Unknown"

    return results

def three_layer_response_system(query: str) -> Dict[str, Any]:
    """
    Orchestrate the three-layer response system:
    1. Doctrine cache lookup (0-200ms)
    2. Semantic search + sub-engine routing
    3. Deep multi-engine analysis
    """
    # Layer 1: Doctrine cache lookup
    cached_analysis = doctrine_cache_lookup(query)
    if cached_analysis:
        return {
            'layer': 1,
            'analysis': cached_analysis,
        }

    # Layer 2: Semantic search + sub-engine routing
    semantic_results = semantic_search_and_sub_engine_routing(query)
    if semantic_results and len(semantic_results) > 1:
        # If multiple doctrines matched, proceed to layer 3 for deep analysis
        doctrines = list(semantic_results.keys())
        deep_results = deep_multi_engine_analysis(query, doctrines)
        return {
            'layer': 3,
            'analysis': deep_results,
        }
    else:
        # Return semantic results directly if single doctrine matched
        return {
            'layer': 2,
            'analysis': semantic_results,
        }

# ----------------------------------------
# MODULE TESTING (if needed)
# ----------------------------------------

if __name__ == "__main__":
    test_query = ("Evaluate the negligence and causation in the context of informed consent "
                  "for a patient who suffered myocardial infarction after a failed disclosure.")
    normalized_query = normalize_query(test_query)
    print("Normalized Query:", normalized_query)

    # Run three layer response system
    response = three_layer_response_system(normalized_query)
    print("Three Layer Response System Output:")
    print(response)

    # Decompose doctrines
    doctrines = multi_doctrine_decomposition(normalized_query)
    print("Decomposed Doctrines:", doctrines)

    # Build DAG
    dag = build_interaction_dag(doctrines)
    print("DAG Edges:", list(dag.edges()))

    # Deep analysis with dummy sub-engine results
    sub_engine_results = deep_multi_engine_analysis(normalized_query, doctrines)
    print("Deep Multi-Engine Analysis Results:")
    print(sub_engine_results)

    # Eight step resolution
    resolution = eight_step_resolution(normalized_query, doctrines, sub_engine_results)
    print("Eight Step Resolution:")
    print(resolution)

    # Zoned analysis
    zone = zoned_analysis(resolution.get('final_conclusion', ''))
    print("Zoned Analysis:")
    print(zone)

    # Fact fragility scoring example
    fact = "The patient reported chest pain and shortness of breath, which may indicate myocardial infarction."
    fragility_scores = score_fact_fragility(fact)
    print("Fact Fragility Scores:")
    print(fragility_scores)

    # Epistemic guardrails example
    text = "It is clearly evident that the treatment is effective without doubt."
    cleaned_text, caveat = apply_epistemic_guardrails(text)
    print("Epistemic Guardrails Applied:")
    print(cleaned_text)
    print(caveat)

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
        self._lock = threading.RLock()
        self._queries: deque = deque(maxlen=100_000)
        self._errors: deque = deque(maxlen=10_000)
        self._doctrine_hits: Counter = Counter()
        self._doctrine_total: Counter = Counter()
        self._sub_engine_latency: DefaultDict[str, List[float]] = defaultdict(list)
        self._sub_engine_invocations: DefaultDict[str, int] = defaultdict(int)
        self._sub_engine_errors: DefaultDict[str, int] = defaultdict(int)
        self._query_by_id: Dict[str, QueryTelemetry] = {}
        self._query_times: deque = deque(maxlen=100_000)

    def record_query(self, telemetry: QueryTelemetry):
        with self._lock:
            self._queries.append(telemetry)
            self._query_by_id[telemetry.query_id] = telemetry
            self._query_times.append(telemetry.timestamp)
            for engine in telemetry.engines_invoked:
                self._sub_engine_latency[engine].append(telemetry.latency_ms)
                self._sub_engine_invocations[engine] += 1
            if telemetry.error:
                self._errors.append(telemetry)
                for engine in telemetry.engines_invoked:
                    self._sub_engine_errors[engine] += 1
            # Doctrine hit/total tracking
            if telemetry.mode in ("doctrine", "doctrine+fallback"):
                for engine in telemetry.engines_invoked:
                    self._doctrine_total[engine] += 1
                    if telemetry.cache_hit:
                        self._doctrine_hits[engine] += 1

    def record_error(self, query_id: str, error: str):
        with self._lock:
            if query_id in self._query_by_id:
                telemetry = self._query_by_id[query_id]
                telemetry.error = error
                self._errors.append(telemetry)
                for engine in telemetry.engines_invoked:
                    self._sub_engine_errors[engine] += 1

    def get_latency_stats(self) -> Dict[str, Any]:
        with self._lock:
            latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
            if not latencies:
                return {}
            latencies_sorted = sorted(latencies)
            n = len(latencies_sorted)
            return {
                "avg": statistics.mean(latencies_sorted),
                "p50": latencies_sorted[int(n*0.5)],
                "p95": latencies_sorted[int(n*0.95)-1],
                "p99": latencies_sorted[int(n*0.99)-1],
                "min": latencies_sorted[0],
                "max": latencies_sorted[-1],
                "count": n
            }

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        with self._lock:
            rates = {}
            for engine in self._doctrine_total:
                total = self._doctrine_total[engine]
                hits = self._doctrine_hits[engine]
                rates[engine] = hits / total if total > 0 else 0.0
            return rates

    def queries_last_hour(self) -> int:
        cutoff = time.time() - 3600
        with self._lock:
            return sum(1 for t in self._query_times if t >= cutoff)

    def get_sub_engine_stats(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            stats = {}
            for engine in self._sub_engine_invocations:
                latencies = self._sub_engine_latency[engine]
                errors = self._sub_engine_errors[engine]
                invocations = self._sub_engine_invocations[engine]
                stats[engine] = {
                    "invocations": invocations,
                    "errors": errors,
                    "error_rate": errors / invocations if invocations > 0 else 0.0,
                    "latency_avg": statistics.mean(latencies) if latencies else None,
                    "latency_p95": statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 100 else None,
                    "latency_max": max(latencies) if latencies else None,
                }
            return stats

    def get_query(self, query_id: str) -> Optional[QueryTelemetry]:
        with self._lock:
            return self._query_by_id.get(query_id)

    def get_recent_queries(self, n: int = 100) -> List[QueryTelemetry]:
        with self._lock:
            return list(self._queries)[-n:]

    def get_error_log(self, n: int = 100) -> List[QueryTelemetry]:
        with self._lock:
            return list(self._errors)[-n:]

# --- 2. DRIFT_WATCHER ---

class DriftWatcher:
    def __init__(self):
        self._lock = threading.RLock()
        self._baseline_confidence: Dict[str, float] = {}
        self._confidence_history: DefaultDict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self._drift_alerts: List[Dict[str, Any]] = []

    def record_baseline(self, doctrine: str, confidence: float):
        with self._lock:
            self._baseline_confidence[doctrine] = confidence
            self._confidence_history[doctrine].append(confidence)

    def record_confidence(self, doctrine: str, confidence: float, timestamp: Optional[float] = None):
        with self._lock:
            self._confidence_history[doctrine].append((timestamp or time.time(), confidence))

    def detect_drift(self, doctrine: str, window: int = 100) -> Optional[Dict[str, Any]]:
        with self._lock:
            history = list(self._confidence_history[doctrine])
            if len(history) < window:
                return None
            # Only use confidence values
            confidences = [c[1] if isinstance(c, tuple) else c for c in history[-window:]]
            avg_conf = statistics.mean(confidences)
            baseline = self._baseline_confidence.get(doctrine)
            if baseline is None:
                return None
            drift = avg_conf - baseline
            percent_shift = 100.0 * drift / baseline if baseline != 0 else 0.0
            if abs(percent_shift) > 10.0:
                alert = {
                    "doctrine": doctrine,
                    "baseline": baseline,
                    "current_avg": avg_conf,
                    "drift": drift,
                    "percent_shift": percent_shift,
                    "timestamp": time.time()
                }
                self._drift_alerts.append(alert)
                return alert
            return None

    def get_drift_report(self) -> List[Dict[str, Any]]:
        with self._lock:
            report = []
            for doctrine in self._confidence_history:
                alert = self.detect_drift(doctrine)
                if alert:
                    report.append(alert)
            return report

    def get_history(self, doctrine: str) -> List[Tuple[float, float]]:
        with self._lock:
            return list(self._confidence_history[doctrine])

    def get_alerts(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._drift_alerts)

# --- 3. COVERAGE_MAP ---

class CoverageTracker:
    def __init__(self):
        self._lock = threading.RLock()
        self._triggered: DefaultDict[str, int] = defaultdict(int)
        self._missed: deque = deque(maxlen=10_000)
        self._sub_engine_coverage: DefaultDict[str, int] = defaultdict(int)
        self._epistemic_gap_queries: deque = deque(maxlen=10_000)
        self._query_to_doctrines: Dict[str, Set[str]] = {}
        self._doctrine_to_queries: DefaultDict[str, Set[str]] = defaultdict(set)

    def record_triggered(self, doctrine: str, query_id: str):
        with self._lock:
            self._triggered[doctrine] += 1
            self._doctrine_to_queries[doctrine].add(query_id)
            self._query_to_doctrines.setdefault(query_id, set()).add(doctrine)

    def record_missed(self, query_id: str):
        with self._lock:
            self._missed.append(query_id)

    def record_sub_engine_coverage(self, sub_engine: str):
        with self._lock:
            self._sub_engine_coverage[sub_engine] += 1

    def record_epistemic_gap(self, query_id: str):
        with self._lock:
            self._epistemic_gap_queries.append(query_id)

    def get_coverage_report(self) -> Dict[str, Any]:
        with self._lock:
            total_queries = len(set(self._query_to_doctrines.keys()) | set(self._missed))
            doctrine_coverage = {k: v for k, v in self._triggered.items()}
            sub_engine_coverage = {k: v for k, v in self._sub_engine_coverage.items()}
            epistemic_gap = list(self._epistemic_gap_queries)
            missed = list(self._missed)
            return {
                "total_queries": total_queries,
                "doctrine_coverage": doctrine_coverage,
                "sub_engine_coverage": sub_engine_coverage,
                "epistemic_gap_count": len(epistemic_gap),
                "epistemic_gap_queries": epistemic_gap,
                "missed_queries": missed
            }

    def identify_epistemic_gaps(self, query_id: str, matched_doctrines: List[str]):
        with self._lock:
            if not matched_doctrines:
                self.record_epistemic_gap(query_id)
                self.record_missed(query_id)

    def get_per_sub_engine_coverage(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._sub_engine_coverage)

    def get_per_doctrine_coverage(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._triggered)

    def get_queries_for_doctrine(self, doctrine: str) -> Set[str]:
        with self._lock:
            return set(self._doctrine_to_queries[doctrine])

    def get_doctrines_for_query(self, query_id: str) -> Set[str]:
        with self._lock:
            return set(self._query_to_doctrines.get(query_id, set()))

# --- 4. DETERMINISM_HASH ---

def compute_determinism_hash(query: Any, response: Any) -> str:
    # Deterministically serialize query and response
    def _serialize(obj):
        if isinstance(obj, dict):
            return {k: _serialize(obj[k]) for k in sorted(obj)}
        elif isinstance(obj, list):
            return [_serialize(x) for x in obj]
        elif isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        elif hasattr(obj, "__dict__"):
            return _serialize(vars(obj))
        else:
            return str(obj)
    payload = {
        "query": _serialize(query),
        "response": _serialize(response)
    }
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    sha = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    return sha

# --- 5. AUDIT_TRAIL ---

class AuditTrailWriter:
    def __init__(self, log_dir: str = "./audit_trail"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self._lock = threading.RLock()
        self._current_date = self._get_date_str()
        self._file = self._open_file(self._current_date)

    def _get_date_str(self):
        return datetime.datetime.utcnow().strftime("%Y-%m-%d")

    def _get_log_path(self, date_str: str):
        return os.path.join(self.log_dir, f"audit_{date_str}.jsonl")

    def _open_file(self, date_str: str):
        path = self._get_log_path(date_str)
        return open(path, "a", encoding="utf-8")

    def write(self, query_id: str, timestamp: float, engine_id: str, engines_invoked: List[str],
              mode: str, confidence: float, latency: float, cache_hit: bool):
        with self._lock:
            date_str = self._get_date_str()
            if date_str != self._current_date:
                self._file.close()
                self._current_date = date_str
                self._file = self._open_file(date_str)
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
            self._file.write(json.dumps(record, separators=(",", ":")) + "\n")
            self._file.flush()

    def forensic_replay(self, date_str: str, query_id: Optional[str] = None) -> List[Dict[str, Any]]:
        path = self._get_log_path(date_str)
        if not os.path.exists(path):
            return []
        results = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    if query_id is None or record.get("query_id") == query_id:
                        results.append(record)
                except Exception:
                    continue
        return results

    def close(self):
        with self._lock:
            if self._file:
                self._file.close()
                self._file = None

# --- 6. PERFORMANCE_PROFILER ---

class PerformanceProfiler:
    def __init__(self):
        self._lock = threading.RLock()
        self._latency: DefaultDict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self._errors: DefaultDict[str, int] = defaultdict(int)
        self._invocations: DefaultDict[str, int] = defaultdict(int)
        self._availability: DefaultDict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self._sla_thresholds: Dict[str, Dict[str, float]] = {}  # e.g., {"sub_engine": {"latency_p95": 200, "error_rate": 0.01}}

    def record(self, sub_engine: str, latency: float, error: bool, available: bool):
        with self._lock:
            self._latency[sub_engine].append(latency)
            self._invocations[sub_engine] += 1
            if error:
                self._errors[sub_engine] += 1
            self._availability[sub_engine].append(1 if available else 0)

    def set_sla(self, sub_engine: str, latency_p95: float, error_rate: float):
        with self._lock:
            self._sla_thresholds[sub_engine] = {
                "latency_p95": latency_p95,
                "error_rate": error_rate
            }

    def get_latency_stats(self, sub_engine: str) -> Dict[str, Any]:
        with self._lock:
            latencies = list(self._latency[sub_engine])
            if not latencies:
                return {}
            latencies_sorted = sorted(latencies)
            n = len(latencies_sorted)
            return {
                "avg": statistics.mean(latencies_sorted),
                "p50": latencies_sorted[int(n*0.5)],
                "p95": latencies_sorted[int(n*0.95)-1] if n >= 20 else None,
                "p99": latencies_sorted[int(n*0.99)-1] if n >= 100 else None,
                "min": latencies_sorted[0],
                "max": latencies_sorted[-1],
                "count": n
            }

    def get_error_rate(self, sub_engine: str) -> float:
        with self._lock:
            errors = self._errors[sub_engine]
            invocations = self._invocations[sub_engine]
            return errors / invocations if invocations > 0 else 0.0

    def get_availability(self, sub_engine: str) -> float:
        with self._lock:
            avail = list(self._availability[sub_engine])
            if not avail:
                return 1.0
            return sum(avail) / len(avail)

    def get_sla_report(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            report = {}
            for sub_engine in self._invocations:
                stats = self.get_latency_stats(sub_engine)
                error_rate = self.get_error_rate(sub_engine)
                availability = self.get_availability(sub_engine)
                sla = self._sla_thresholds.get(sub_engine, {})
                sla_breach = False
                breach_reasons = []
                if sla:
                    if stats.get("p95") is not None and stats["p95"] > sla["latency_p95"]:
                        sla_breach = True
                        breach_reasons.append(f"latency_p95>{sla['latency_p95']}")
                    if error_rate > sla["error_rate"]:
                        sla_breach = True
                        breach_reasons.append(f"error_rate>{sla['error_rate']}")
                report[sub_engine] = {
                    "latency_stats": stats,
                    "error_rate": error_rate,
                    "availability": availability,
                    "sla": sla,
                    "sla_breach": sla_breach,
                    "breach_reasons": breach_reasons
                }
            return report

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            stats = {}
            for sub_engine in self._invocations:
                stats[sub_engine] = {
                    "latency": self.get_latency_stats(sub_engine),
                    "error_rate": self.get_error_rate(sub_engine),
                    "availability": self.get_availability(sub_engine)
                }
            return stats

    def reset(self):
        with self._lock:
            self._latency.clear()
            self._errors.clear()
            self._invocations.clear()
            self._availability.clear()

# --- END OF PART 5 ---

ENGINE_ID = "MEDIE"
ENGINE_PORT = 8856
SUB_ENGINES = {
    "MED01": "Pharmacology",
    "MED02": "Toxicology",
    "MED03": "Emergency Medicine",
    "MED04": "Radiology",
    "MED05": "Pathology",
    "MED06": "Infectious Disease",
    "MED07": "Surgery",
    "MED08": "Cardiology",
    "MED09": "Neurology",
    "MED10": "Oncology",
    "MED11": "Pediatrics",
    "MED12": "Obstetrics",
    "MED13": "Psychiatry",
    "MED14": "Orthopedics",
    "MED15": "Dermatology",
    "MED16": "Gastroenterology",
    "MED17": "Nephrology",
    "MED18": "Pulmonology",
    "MED19": "Endocrinology",
    "MED20": "Immunology",
    "MED21": "Genetics",
}
MAX_SUBENGINE_TIMEOUT = 5.0  # seconds
CIRCUIT_BREAKER_THRESHOLD = 3  # failures before open
CIRCUIT_BREAKER_RESET_TIME = 60  # seconds

# Logging setup
logger = logging.getLogger("medie_orchestrator")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Data Models
class QueryRequest(BaseModel):
    query: str
    metadata: Optional[Dict[str, Any]] = None

class RouteDryRunRequest(BaseModel):
    query: str

class AnalyzeRequest(BaseModel):
    query: str
    depth: Optional[int] = 3

class SubEngineResponse(BaseModel):
    engine_id: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    latency_ms: Optional[float] = None

class HealthStatus(BaseModel):
    status: str
    details: Optional[Dict[str, Any]] = None

class MetricsResponse(BaseModel):
    latency_stats: Dict[str, float]
    cache_hit_rate: float
    queries_per_hour: float
    sub_engine_stats: Dict[str, Dict[str, Any]]

class CoverageReport(BaseModel):
    doctrine_coverage: Dict[str, float]
    epistemic_gaps: List[str]

class DriftReport(BaseModel):
    drift_detected: bool
    details: Optional[Dict[str, Any]] = None

class DoctrinesList(BaseModel):
    doctrines: List[str]

class RoutingInfo(BaseModel):
    routing_rules: Dict[str, Any]
    engine_registry: Dict[str, str]

class SubEnginesHealth(BaseModel):
    sub_engines: Dict[str, HealthStatus]

# Global State and Caches
doctrine_cache: Dict[str, Any] = {}
search_index: Dict[str, List[str]] = {}
telemetry_data: Dict[str, Any] = {
    "latencies": [],
    "cache_hits": 0,
    "cache_misses": 0,
    "queries": [],
    "sub_engine_stats": {eid: {"calls": 0, "failures": 0, "latencies": []} for eid in SUB_ENGINES.keys()},
}
health_monitor_status: Dict[str, HealthStatus] = {}
routing_rules: Dict[str, Any] = {}
circuit_breakers: Dict[str, Dict[str, Any]] = {}
query_logs: List[Dict[str, Any]] = []

# Helper Functions
def normalize_query(query: str) -> str:
    normalized = query.strip().lower()
    logger.debug(f"Normalized query: {normalized}")
    return normalized

def classify_domain(query: str) -> List[str]:
    # Dummy classifier based on keywords
    keywords_map = {
        "pharma": "MED01",
        "toxic": "MED02",
        "emergency": "MED03",
        "radiology": "MED04",
        "pathology": "MED05",
        "infection": "MED06",
        "surgery": "MED07",
        "cardio": "MED08",
        "neuro": "MED09",
        "oncology": "MED10",
        "pediatrics": "MED11",
        "obstetrics": "MED12",
        "psychiatry": "MED13",
        "ortho": "MED14",
        "derma": "MED15",
        "gastro": "MED16",
        "nephro": "MED17",
        "pulmo": "MED18",
        "endocrine": "MED19",
        "immuno": "MED20",
        "genetics": "MED21",
    }
    matched_engines = set()
    for kw, eid in keywords_map.items():
        if kw in query:
            matched_engines.add(eid)
    if not matched_engines:
        # fallback to all engines for unknown queries
        matched_engines = set(SUB_ENGINES.keys())
    logger.debug(f"Classified domains: {matched_engines}")
    return list(matched_engines)

def route_query(domains: List[str]) -> List[str]:
    # For now, routing is direct: all classified domains are routed
    logger.debug(f"Routing to sub-engines: {domains}")
    return domains

async def dispatch_to_sub_engine(engine_id: str, query: str) -> SubEngineResponse:
    # Simulate sub-engine call with latency and possible failure
    start = time.time()
    try:
        # Circuit breaker check
        cb = circuit_breakers.get(engine_id, {"failures": 0, "state": "closed", "last_failure_time": None})
        if cb["state"] == "open":
            elapsed = time.time() - cb["last_failure_time"]
            if elapsed > CIRCUIT_BREAKER_RESET_TIME:
                cb["state"] = "half-open"
                circuit_breakers[engine_id] = cb
            else:
                logger.warning(f"Circuit breaker open for {engine_id}, skipping call")
                return SubEngineResponse(
                    engine_id=engine_id,
                    success=False,
                    error="Circuit breaker open",
                    latency_ms=0,
                )
        # Simulate latency
        latency = random.uniform(0.1, 1.5)
        await asyncio.sleep(latency)
        # Simulate random failure
        if random.random() < 0.1:
            raise Exception("Simulated sub-engine failure")
        # Simulated response data
        data = {
            "answer": f"Response from {SUB_ENGINES[engine_id]} for query '{query}'",
            "details": {"engine_id": engine_id, "query": query},
        }
        latency_ms = (time.time() - start) * 1000
        # Reset circuit breaker on success
        if cb["state"] in ["open", "half-open"]:
            cb["failures"] = 0
            cb["state"] = "closed"
            circuit_breakers[engine_id] = cb
        telemetry_data["sub_engine_stats"][engine_id]["calls"] += 1
        telemetry_data["sub_engine_stats"][engine_id]["latencies"].append(latency_ms)
        return SubEngineResponse(
            engine_id=engine_id,
            success=True,
            data=data,
            latency_ms=latency_ms,
        )
    except Exception as e:
        latency_ms = (time.time() - start) * 1000
        # Update circuit breaker on failure
        cb["failures"] += 1
        cb["last_failure_time"] = time.time()
        if cb["failures"] >= CIRCUIT_BREAKER_THRESHOLD:
            cb["state"] = "open"
            logger.error(f"Circuit breaker opened for {engine_id}")
        circuit_breakers[engine_id] = cb
        telemetry_data["sub_engine_stats"][engine_id]["failures"] += 1
        telemetry_data["sub_engine_stats"][engine_id]["calls"] += 1
        logger.error(f"Sub-engine {engine_id} failed: {str(e)}")
        return SubEngineResponse(
            engine_id=engine_id,
            success=False,
            error=str(e),
            latency_ms=latency_ms,
        )

def merge_responses(responses: List[SubEngineResponse]) -> Dict[str, Any]:
    merged = {"responses": [], "summary": ""}
    answers = []
    for resp in responses:
        if resp.success and resp.data:
            merged["responses"].append({resp.engine_id: resp.data})
            answers.append(resp.data.get("answer", ""))
        else:
            merged["responses"].append({resp.engine_id: {"error": resp.error}})
    merged["summary"] = " | ".join(answers) if answers else "No successful responses"
    logger.debug(f"Merged response summary: {merged['summary']}")
    return merged

def apply_guardrails(response: Dict[str, Any]) -> Dict[str, Any]:
    # Example guardrail: redact any occurrence of 'error' keys in responses
    for r in response.get("responses", []):
        for engine_id, content in r.items():
            if isinstance(content, dict) and "error" in content:
                content["error"] = "Redacted due to guardrail policy"
    return response

def hash_query_response(query: str, response: Dict[str, Any]) -> str:
    hasher = hashlib.sha256()
    hasher.update(query.encode('utf-8'))
    hasher.update(json.dumps(response, sort_keys=True).encode('utf-8'))
    digest = hasher.hexdigest()
    logger.debug(f"Hashed query-response: {digest}")
    return digest

def log_query(query: str, response: Dict[str, Any], query_hash: str, latency_ms: float):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "query": query,
        "response_hash": query_hash,
        "latency_ms": latency_ms,
    }
    query_logs.append(entry)
    logger.info(f"Logged query: {entry}")

async def initialize_doctrine_cache():
    # Simulate loading doctrines
    global doctrine_cache
    doctrine_cache = {
        "doctrine1": {"content": "Pharmacology rules"},
        "doctrine2": {"content": "Toxicology rules"},
        "doctrine3": {"content": "Emergency Medicine protocols"},
    }
    logger.info("Doctrine cache initialized")

async def start_health_monitor():
    # Simulate health monitor startup
    global health_monitor_status
    for eid in SUB_ENGINES.keys():
        health_monitor_status[eid] = HealthStatus(status="healthy")
    logger.info("Health monitor started")

async def seed_search_index():
    # Simulate search index seeding
    global search_index
    search_index = {
        "pharma": ["doctrine1"],
        "toxic": ["doctrine2"],
        "emergency": ["doctrine3"],
    }
    logger.info("Search index seeded")

async def start_telemetry():
    # Simulate telemetry startup
    telemetry_data["start_time"] = time.time()
    logger.info("Telemetry started")

async def perform_health_check() -> HealthStatus:
    # Self health check
    return HealthStatus(status="healthy")

async def get_sub_engines_health() -> Dict[str, HealthStatus]:
    # Return health status of all sub-engines
    return health_monitor_status

async def get_metrics() -> MetricsResponse:
    latencies = telemetry_data["latencies"]
    latency_stats = {
        "min_ms": min(latencies) if latencies else 0.0,
        "max_ms": max(latencies) if latencies else 0.0,
        "avg_ms": sum(latencies) / len(latencies) if latencies else 0.0,
    }
    total_calls = telemetry_data["cache_hits"] + telemetry_data["cache_misses"]
    cache_hit_rate = telemetry_data["cache_hits"] / total_calls if total_calls > 0 else 0.0
    elapsed_hours = (time.time() - telemetry_data.get("start_time", time.time())) / 3600
    queries_per_hour = len(telemetry_data["queries"]) / elapsed_hours if elapsed_hours > 0 else 0.0
    sub_engine_stats = telemetry_data["sub_engine_stats"]
    return MetricsResponse(
        latency_stats=latency_stats,
        cache_hit_rate=cache_hit_rate,
        queries_per_hour=queries_per_hour,
        sub_engine_stats=sub_engine_stats,
    )

async def get_coverage_report() -> CoverageReport:
    # Dummy coverage and epistemic gaps
    coverage = {k: random.uniform(0.7, 1.0) for k in doctrine_cache.keys()}
    gaps = ["Rare infectious diseases", "Novel oncology treatments"]
    return CoverageReport(doctrine_coverage=coverage, epistemic_gaps=gaps)

async def get_drift_report() -> DriftReport:
    # Dummy drift detection
    drift_detected = random.choice([True, False])
    details = None
    if drift_detected:
        details = {"feature": "query distribution", "change": "significant"}
    return DriftReport(drift_detected=drift_detected, details=details)

async def get_doctrines_list() -> DoctrinesList:
    return DoctrinesList(doctrines=list(doctrine_cache.keys()))

async def get_routing_info() -> RoutingInfo:
    # Dummy routing rules
    rules = {
        "default": "route to all classified sub-engines",
        "emergency": ["MED03"],
        "oncology": ["MED10"],
    }
    return RoutingInfo(routing_rules=rules, engine_registry=SUB_ENGINES)

async def dry_run_routing(query: str) -> List[str]:
    normalized = normalize_query(query)
    domains = classify_domain(normalized)
    routes = route_query(domains)
    return routes

async def deep_multi_engine_analysis(query: str, depth: int) -> Dict[str, Any]:
    # Simulate deep analysis by querying multiple engines multiple times
    results = {}
    for d in range(depth):
        domains = classify_domain(query + f" depth{d}")
        routes = route_query(domains)
        responses = []
        for eid in routes:
            resp = await dispatch_to_sub_engine(eid, query)
            responses.append(resp)
        merged = merge_responses(responses)
        results[f"depth_{d}"] = merged
    return results

# FastAPI App and Lifespan
app = FastAPI(title="Medical Intelligence Engine - Domain Orchestrator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Medical Intelligence Engine - Domain Orchestrator")
    await initialize_doctrine_cache()
    await start_health_monitor()
    await seed_search_index()
    await start_telemetry()
    yield
    logger.info("Shutting down Medical Intelligence Engine - Domain Orchestrator")

app.router.lifespan_context = lifespan

# Endpoint Implementations
@app.post("/query")
async def query_endpoint(request: QueryRequest):
    start_time = time.time()
    query = request.query
    normalized_query = normalize_query(query)
    domains = classify_domain(normalized_query)
    routes = route_query(domains)

    # Check doctrine cache fallback
    if normalized_query in doctrine_cache:
        telemetry_data["cache_hits"] += 1
        cached_response = doctrine_cache[normalized_query]
        latency_ms = (time.time() - start_time) * 1000
        query_hash = hash_query_response(normalized_query, cached_response)
        log_query(normalized_query, cached_response, query_hash, latency_ms)
        return JSONResponse(content={"cached": True, "response": cached_response})

    telemetry_data["cache_misses"] += 1

    # Dispatch concurrently to sub-engines with timeout and error handling
    tasks = []
    for eid in routes:
        tasks.append(dispatch_to_sub_engine(eid, normalized_query))
    try:
        responses: List[SubEngineResponse] = await asyncio.wait_for(
            asyncio.gather(*tasks, return_exceptions=False),
            timeout=MAX_SUBENGINE_TIMEOUT
        )
    except asyncio.TimeoutError:
        # Timeout fallback to doctrine cache if available
        if normalized_query in doctrine_cache:
            cached_response = doctrine_cache[normalized_query]
            latency_ms = (time.time() - start_time) * 1000
            query_hash = hash_query_response(normalized_query, cached_response)
            log_query(normalized_query, cached_response, query_hash, latency_ms)
            return JSONResponse(content={"cached": True, "response": cached_response})
        else:
            raise HTTPException(status_code=504, detail="Sub-engine timeout and no cache fallback available")

    merged_response = merge_responses(responses)
    guarded_response = apply_guardrails(merged_response)
    latency_ms = (time.time() - start_time) * 1000
    query_hash = hash_query_response(normalized_query, guarded_response)
    log_query(normalized_query, guarded_response, query_hash, latency_ms)
    telemetry_data["latencies"].append(latency_ms)
    telemetry_data["queries"].append(normalized_query)
    return JSONResponse(content={"cached": False, "response": guarded_response})

@app.get("/health")
async def health_endpoint():
    self_health = await perform_health_check()
    sub_engines_health = await get_sub_engines_health()
    combined = {
        "self": self_health.dict(),
        "sub_engines": {eid: status.dict() for eid, status in sub_engines_health.items()},
    }
    return combined

@app.get("/metrics")
async def metrics_endpoint():
    metrics = await get_metrics()
    return metrics.dict()

@app.get("/coverage")
async def coverage_endpoint():
    coverage = await get_coverage_report()
    return coverage.dict()

@app.get("/drift")
async def drift_endpoint():
    drift = await get_drift_report()
    return drift.dict()

@app.get("/doctrines")
async def doctrines_endpoint():
    doctrines = await get_doctrines_list()
    return doctrines.dict()

@app.get("/routing")
async def routing_endpoint():
    routing = await get_routing_info()
    return routing.dict()

@app.get("/sub-engines")
async def sub_engines_endpoint():
    health = await get_sub_engines_health()
    return {eid: status.dict() for eid, status in health.items()}

@app.post("/route")
async def route_dry_run_endpoint(request: RouteDryRunRequest):
    routes = await dry_run_routing(request.query)
    return {"would_invoke": routes}

@app.post("/analyze")
async def analyze_endpoint(request: AnalyzeRequest):
    analysis = await deep_multi_engine_analysis(request.query, request.depth or 3)
    return analysis

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(status_code=500, content={"error": "Internal server error"})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=ENGINE_PORT, log_level="info")