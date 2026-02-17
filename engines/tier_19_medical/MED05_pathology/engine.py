import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple, Set
from enum import Enum, auto
from datetime import datetime, timedelta
import json
import threading

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
    CBC = "COMPLETE_BLOOD_COUNT"
    COAGULATION = "COAGULATION"
    METABOLIC_PANEL = "METABOLIC_PANEL"
    CARDIAC_BIOMARKERS = "CARDIAC_BIOMARKERS"
    THYROID_FUNCTION = "THYROID_FUNCTION"
    LIPID_PANEL = "LIPID_PANEL"
    URINALYSIS = "URINALYSIS"
    BLOOD_GAS = "BLOOD_GAS"
    HEMOGLOBIN_A1C = "HEMOGLOBIN_A1C"
    BLOOD_CULTURE = "BLOOD_CULTURE"
    CSF_ANALYSIS = "CSF_ANALYSIS"
    TUMOR_MARKERS = "TUMOR_MARKERS"
    IRON_STUDIES = "IRON_STUDIES"
    AUTOIMMUNE_PANEL = "AUTOIMMUNE_PANEL"
    HEPATITIS_SEROLOGY = "HEPATITIS_SEROLOGY"
    HIV_TESTING = "HIV_TESTING"
    DRUG_SCREENING = "DRUG_SCREENING"
    MOLECULAR_DIAGNOSTICS = "MOLECULAR_DIAGNOSTICS"
    FLOW_CYTOMETRY = "FLOW_CYTOMETRY"
    OTHER = "OTHER"

# =========================
# METRICS COLLECTOR
# =========================

class METRICS_COLLECTOR:
    def __init__(self):
        self.queries = []
        self.errors = []
        self.doctrine_hits = {}
        self.lock = threading.Lock()

    def record_query(self, doctrine_hit: Optional[str], latency: float):
        with self.lock:
            self.queries.append((datetime.utcnow(), doctrine_hit, latency))
            if doctrine_hit:
                self.doctrine_hits[doctrine_hit] = self.doctrine_hits.get(doctrine_hit, 0) + 1

    def record_error(self, error_type: str):
        with self.lock:
            self.errors.append((datetime.utcnow(), error_type))

    def get_latency_stats(self):
        with self.lock:
            latencies = [l for _, _, l in self.queries[-100:]]
            if not latencies:
                return {"mean_ms": 0, "p95_ms": 0}
            latencies.sort()
            mean = sum(latencies) / len(latencies)
            p95 = latencies[int(0.95 * len(latencies))-1]
            return {"mean_ms": mean, "p95_ms": p95}

    def get_doctrine_hit_rate(self):
        with self.lock:
            total = len(self.queries)
            doctrine_hits = sum(1 for _, d, _ in self.queries if d)
            return doctrine_hits / total if total else 0

    def queries_last_hour(self):
        cutoff = datetime.utcnow() - timedelta(hours=1)
        with self.lock:
            return len([t for t, _, _ in self.queries if t > cutoff])

metrics = METRICS_COLLECTOR()

# =========================
# PYDANTIC MODELS
# =========================

class QueryRequest(BaseModel):
    scenario: str = Field(..., description="Clinical scenario or question")
    mode: ResponseMode = Field(..., description="Response mode")
    entity_type: str = Field(..., description="Entity type (e.g. patient, sample, population)")
    complexity: int = Field(..., description="Complexity level 1-5")

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
    position_zone: PositionZone
    issue_category: IssueCategory

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="CBC Differential Interpretation",
        keywords=["CBC", "differential", "WBC", "neutrophilia", "lymphocytosis"],
        conclusion_template="Interpretation of the CBC with differential requires assessment of total and differential white cell counts, hemoglobin, hematocrit, and platelet count. Neutrophilia often indicates bacterial infection or inflammation, while lymphocytosis may suggest viral infection or lymphoproliferative disorder. Anemia patterns and thrombocytopenia must be contextualized with clinical findings.",
        reasoning_framework=(
            "1. Review total WBC count and differential: elevated WBC with neutrophilia suggests acute bacterial infection, stress, or corticosteroid effect.\n"
            "2. Lymphocytosis is commonly seen in viral infections (e.g., EBV, CMV), pertussis, or chronic lymphocytic leukemia (CLL).\n"
            "3. Eosinophilia may indicate allergic disorders, parasitic infections, or certain neoplasms.\n"
            "4. Monocytosis can be reactive (chronic infection, recovery phase) or neoplastic (CMML).\n"
            "5. Anemia patterns: microcytic (iron deficiency, thalassemia), normocytic (chronic disease, acute blood loss), macrocytic (B12/folate deficiency).\n"
            "6. Thrombocytopenia: consider pseudothrombocytopenia (EDTA effect), immune thrombocytopenia, DIC, or marrow failure.\n"
            "7. Always correlate with clinical context, medication history, and prior CBCs.\n"
            "8. Consider repeat testing if results are unexpected or inconsistent with clinical findings.\n"
            "9. Peripheral smear review is essential for abnormal findings (blasts, schistocytes, spherocytes).\n"
            "10. Consult hematology for persistent unexplained cytopenias or cytoses."
        ),
        key_factors=[
            "Total WBC and differential counts",
            "Hemoglobin and hematocrit levels",
            "Platelet count",
            "Peripheral smear findings",
            "Clinical context and history"
        ],
        primary_authority=[
            "Henry's Clinical Diagnosis and Management by Laboratory Methods, 24th Ed.",
            "Hoffbrand AV, Moss PAH. Essential Haematology. 8th Ed.",
            "Williams Hematology, 10th Ed."
        ],
        burden_holder="Ordering clinician",
        adversary_position="CBC changes are nonspecific and may not reflect acute pathology",
        counter_arguments=[
            "CBC findings may be transient or due to non-pathologic causes",
            "Laboratory error or sample artifact can confound results",
            "Medications may alter counts independently of disease",
            "Chronic conditions may mask acute changes",
            "Peripheral smear not always performed"
        ],
        resolution_strategy="Integrate CBC findings with clinical assessment and, if indicated, further diagnostic testing or specialist referral.",
        entity_scope="Patient",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Henry's Clinical Diagnosis, 24th Ed., Ch 2",
            "Hoffbrand, Essential Haematology, Ch 3"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.CBC
    ),
    DoctrineBlock(
        topic="Coagulation Studies: PT, INR, PTT, Fibrinogen, D-dimer",
        keywords=["PT", "INR", "PTT", "fibrinogen", "D-dimer", "coagulation"],
        conclusion_template="Interpretation of coagulation studies requires analysis of PT/INR, PTT, fibrinogen, and D-dimer in the context of bleeding or thrombotic risk. Prolonged PT/INR suggests extrinsic pathway defects, while prolonged PTT implicates the intrinsic pathway. D-dimer elevation is sensitive but nonspecific for thrombosis.",
        reasoning_framework=(
            "1. Prolonged PT/INR: consider vitamin K deficiency, warfarin therapy, liver dysfunction, or factor VII deficiency.\n"
            "2. Prolonged PTT: evaluate for heparin effect, lupus anticoagulant, hemophilia A/B, or factor XI/XII deficiency.\n"
            "3. Both PT and PTT prolonged: suggests common pathway defect (e.g., DIC, severe liver failure, multiple factor deficiencies).\n"
            "4. Low fibrinogen: seen in DIC, advanced liver disease, or massive transfusion.\n"
            "5. Elevated D-dimer: sensitive for DIC, VTE, but not specific; consider in context of pretest probability.\n"
            "6. Mixing studies can distinguish factor deficiencies from inhibitors.\n"
            "7. Always correlate with bleeding history, medication exposure, and clinical status.\n"
            "8. Repeat testing if results are discordant with clinical suspicion or if sample is hemolyzed.\n"
            "9. Consider additional assays (e.g., factor assays, thrombin time) if initial studies are inconclusive.\n"
            "10. Consult hematology for complex or unexplained coagulopathies."
        ),
        key_factors=[
            "PT/INR and PTT values",
            "Fibrinogen concentration",
            "D-dimer level",
            "Medication and bleeding history",
            "Clinical context (bleeding, thrombosis, liver disease)"
        ],
        primary_authority=[
            "Kitchens CS, et al. Consultative Hemostasis and Thrombosis, 4th Ed.",
            "Rodak BF, et al. Hematology: Clinical Principles and Applications, 6th Ed.",
            "ASH Guidelines on VTE and DIC"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Abnormal coagulation tests may not correlate with clinical bleeding or thrombosis",
        counter_arguments=[
            "D-dimer is nonspecific and elevated in many conditions",
            "Liver disease can affect multiple coagulation factors",
            "Heparin contamination can artifactually prolong PTT",
            "Acute phase response can elevate fibrinogen",
            "Mixing studies may be inconclusive"
        ],
        resolution_strategy="Interpret results in clinical context; pursue additional testing or specialist input as indicated.",
        entity_scope="Patient",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ASH DIC Guidelines 2018",
            "Kitchens, Consultative Hemostasis, Ch 5"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.COAGULATION
    ),
    DoctrineBlock(
        topic="Basic Metabolic Panel (BMP) Interpretation",
        keywords=["BMP", "electrolytes", "glucose", "BUN", "creatinine"],
        conclusion_template="The BMP provides essential information on electrolyte balance, renal function, and glucose status. Interpretation should consider sodium, potassium, chloride, bicarbonate, BUN, creatinine, and glucose in the context of volume status, renal perfusion, and metabolic derangements.",
        reasoning_framework=(
            "1. Evaluate sodium: hyponatremia may result from SIADH, heart failure, or diuretics; hypernatremia from dehydration or DI.\n"
            "2. Potassium: hypokalemia often due to GI/renal losses or diuretics; hyperkalemia from renal failure, ACE inhibitors, or hemolysis.\n"
            "3. Chloride and bicarbonate: assess for acid-base disorders (e.g., metabolic acidosis/alkalosis).\n"
            "4. BUN and creatinine: elevated in renal dysfunction, hypovolemia, or high protein intake; consider BUN/Cr ratio.\n"
            "5. Glucose: hyperglycemia in diabetes, stress, or steroids; hypoglycemia from insulin or critical illness.\n"
            "6. Anion gap calculation aids in identifying metabolic acidosis causes.\n"
            "7. Always correlate with clinical context, medications, and comorbidities.\n"
            "8. Repeat abnormal results to exclude laboratory error, especially for potassium.\n"
            "9. Consider additional tests (e.g., osmolality, urine electrolytes) for complex cases.\n"
            "10. Consult nephrology for persistent or unexplained electrolyte or renal abnormalities."
        ),
        key_factors=[
            "Sodium, potassium, chloride, bicarbonate levels",
            "BUN and creatinine",
            "Glucose concentration",
            "Volume status and medications",
            "Acid-base status"
        ],
        primary_authority=[
            "Kumar & Clark's Clinical Medicine, 10th Ed.",
            "Brenner & Rector's The Kidney, 11th Ed.",
            "Goldman-Cecil Medicine, 26th Ed."
        ],
        burden_holder="Ordering clinician",
        adversary_position="Electrolyte abnormalities may be transient or artifact",
        counter_arguments=[
            "Hemolysis can falsely elevate potassium",
            "Volume status assessment may be subjective",
            "Medications can confound interpretation",
            "Acid-base disorders may be mixed",
            "Renal function may not reflect acute changes"
        ],
        resolution_strategy="Integrate BMP findings with clinical assessment and repeat or expand testing as needed.",
        entity_scope="Patient",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Kumar & Clark, Ch 3",
            "Brenner & Rector, Ch 7"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.METABOLIC_PANEL
    ),
    DoctrineBlock(
        topic="Comprehensive Metabolic Panel (CMP) and Liver Enzymes",
        keywords=["CMP", "liver enzymes", "ALT", "AST", "albumin", "alkaline phosphatase"],
        conclusion_template="The CMP extends the BMP with liver enzymes and proteins. Elevated transaminases suggest hepatocellular injury, while alkaline phosphatase elevation indicates cholestasis or bone disease. Albumin and bilirubin reflect synthetic and excretory liver function.",
        reasoning_framework=(
            "1. ALT and AST: elevations suggest hepatocellular injury (e.g., viral hepatitis, ischemia, toxins).\n"
            "2. AST>ALT may indicate alcoholic liver disease; ALT>AST in viral hepatitis.\n"
            "3. Alkaline phosphatase: elevated in cholestasis, biliary obstruction, or bone turnover (Paget's, metastasis).\n"
            "4. GGT can help distinguish hepatic from bone sources of alkaline phosphatase.\n"
            "5. Albumin: low levels reflect chronic liver disease, malnutrition, or nephrotic syndrome.\n"
            "6. Total and direct bilirubin: elevated in hemolysis, hepatocellular dysfunction, or cholestasis.\n"
            "7. Assess for synthetic dysfunction (prolonged PT/INR, low albumin) in chronic liver disease.\n"
            "8. Always correlate with clinical findings and risk factors (alcohol, hepatitis, medications).\n"
            "9. Repeat abnormal results to confirm and trend over time.\n"
            "10. Consider imaging or specialist referral for persistent or unexplained abnormalities."
        ),
        key_factors=[
            "ALT, AST, alkaline phosphatase, GGT",
            "Albumin and bilirubin",
            "Clinical risk factors",
            "Synthetic function (PT/INR, albumin)",
            "Pattern and magnitude of enzyme elevation"
        ],
        primary_authority=[
            "Zakim & Boyer’s Hepatology, 7th Ed.",
            "Goldman-Cecil Medicine, 26th Ed.",
            "AASLD Practice Guidelines"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Mild enzyme elevations may be nonspecific or transient",
        counter_arguments=[
            "Enzyme elevations may be due to non-hepatic sources",
            "Chronicity and trend are critical for interpretation",
            "Medications and supplements can alter results",
            "Alcohol use may confound findings",
            "Synthetic dysfunction may lag behind injury"
        ],
        resolution_strategy="Interpret CMP in context; trend results and pursue further workup if indicated.",
        entity_scope="Patient",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Zakim & Boyer, Ch 5",
            "AASLD Guidelines 2021"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.METABOLIC_PANEL
    ),
    DoctrineBlock(
        topic="Cardiac Biomarkers: Troponin, BNP, CK-MB",
        keywords=["troponin", "BNP", "CK-MB", "myocardial infarction", "heart failure"],
        conclusion_template="Cardiac biomarkers are essential for diagnosing acute coronary syndromes and heart failure. Troponin is highly sensitive and specific for myocardial injury, while BNP reflects ventricular stretch and is useful in heart failure assessment.",
        reasoning_framework=(
            "1. Troponin: elevation above the 99th percentile is diagnostic for myocardial injury; trend serially to distinguish acute from chronic elevation.\n"
            "2. CK-MB: less specific than troponin; may be useful in reinfarction.\n"
            "3. BNP/NT-proBNP: elevated in heart failure, renal failure, and other causes of ventricular stretch.\n"
            "4. Interpret biomarkers in the context of symptoms, ECG, and imaging.\n"
            "5. Non-cardiac causes of troponin elevation include sepsis, PE, myocarditis, renal failure.\n"
            "6. Serial measurements are critical for ACS diagnosis (rise and/or fall).\n"
            "7. BNP thresholds vary with age, obesity, and renal function.\n"
            "8. High-sensitivity troponin assays improve early rule-out but may detect minor injury.\n"
            "9. Always correlate with clinical presentation and risk factors.\n"
            "10. Consult cardiology for ambiguous or high-risk cases."
        ),
        key_factors=[
            "Troponin and BNP/NT-proBNP levels",
            "Serial trends",
            "Clinical presentation and ECG findings",
            "Renal function",
            "Timing of symptom onset"
        ],
        primary_authority=[
            "Thygesen K, et al. Fourth Universal Definition of MI. Circulation. 2018.",
            "Braunwald’s Heart Disease, 12th Ed.",
            "ACC/AHA Guidelines for ACS and HF"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Biomarker elevations may be non-specific",
        counter_arguments=[
            "Renal failure can elevate troponin and BNP",
            "Sepsis and PE can cause biomarker elevation",
            "Obesity lowers BNP levels",
            "CK-MB is less specific than troponin",
            "Chronic elevations may not indicate acute pathology"
        ],
        resolution_strategy="Integrate biomarkers with clinical, ECG, and imaging findings; trend serially.",
        entity_scope="Patient",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Circulation. 2018;138:e618–e651",
            "Braunwald, Ch 27"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.CARDIAC_BIOMARKERS
    ),
    DoctrineBlock(
        topic="Thyroid Function Tests: TSH, Free T4, T3",
        keywords=["TSH", "free T4", "T3", "thyroid", "hypothyroidism", "hyperthyroidism"],
        conclusion_template="Thyroid function is best assessed with TSH and free T4. TSH is the most sensitive marker for primary thyroid dysfunction. Free T4 and T3 help distinguish between primary, secondary, and tertiary disorders.",
        reasoning_framework=(
            "1. High TSH, low free T4: primary hypothyroidism (e.g., Hashimoto's, post-ablation).\n"
            "2. Low TSH, high free T4/T3: hyperthyroidism (e.g., Graves', toxic nodular goiter).\n"
            "3. Low TSH, normal free T4/T3: subclinical hyperthyroidism or non-thyroidal illness.\n"
            "4. High TSH, normal free T4: subclinical hypothyroidism.\n"
            "5. Low TSH, low free T4: secondary (pituitary) or tertiary (hypothalamic) hypothyroidism.\n"
            "6. T3 toxicosis: elevated T3 with normal T4, suppressed TSH.\n"
            "7. Non-thyroidal illness can alter results (euthyroid sick syndrome).\n"
            "8. Medications (amiodarone, steroids, biotin) can interfere with assays.\n"
            "9. Repeat abnormal results if inconsistent with clinical picture.\n"
            "10. Consider thyroid autoantibodies for autoimmune etiology."
        ),
        key_factors=[
            "TSH, free T4, and T3 levels",
            "Clinical symptoms",
            "Medication and supplement history",
            "Pituitary function",
            "Autoantibody status"
        ],
        primary_authority=[
            "Ross DS, et al. 2016 ATA Guidelines for Hypothyroidism.",
            "Braverman LE, Cooper DS. Werner & Ingbar's The Thyroid, 11th Ed.",
            "Goldman-Cecil Medicine, 26th Ed."
        ],
        burden_holder="Ordering clinician",
        adversary_position="Abnormal results may reflect non-thyroidal illness or assay interference",
        counter_arguments=[
            "Acute illness can suppress TSH",
            "Biotin supplementation can cause assay artifacts",
            "Pituitary disease may cause discordant results",
            "Medications can alter thyroid function",
            "Subclinical states may not require treatment"
        ],
        resolution_strategy="Interpret in clinical context; repeat or expand testing if indicated.",
        entity_scope="Patient",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ATA Guidelines 2016",
            "Werner & Ingbar, Ch 8"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.THYROID_FUNCTION
    ),
    DoctrineBlock(
        topic="Lipid Panel Interpretation",
        keywords=["lipid panel", "cholesterol", "LDL", "HDL", "triglycerides"],
        conclusion_template="Lipid panels assess cardiovascular risk. Elevated LDL is atherogenic, while high HDL is protective. Hypertriglyceridemia increases pancreatitis risk at very high levels.",
        reasoning_framework=(
            "1. LDL cholesterol: primary target for atherosclerotic risk reduction; goal depends on risk stratification.\n"
            "2. HDL cholesterol: low levels associated with increased risk; raising HDL has not shown outcome benefit.\n"
            "3. Triglycerides: very high levels (>500 mg/dL) increase pancreatitis risk; moderate elevations are a CVD risk factor.\n"
            "4. Non-fasting samples may elevate triglycerides.\n"
            "5. Secondary causes (diabetes, hypothyroidism, nephrotic syndrome, medications) should be excluded.\n"
            "6. Statin therapy is first-line for elevated LDL; fibrates or omega-3s for severe hypertriglyceridemia.\n"
            "7. Repeat testing is recommended for confirmation and monitoring.\n"
            "8. Family history and clinical risk factors should guide management.\n"
            "9. Consider genetic dyslipidemias in severe or refractory cases.\n"
            "10. Lifestyle modification is foundational for all lipid disorders."
        ),
        key_factors=[
            "LDL, HDL, and triglyceride levels",
            "Fasting status",
            "Secondary causes",
            "Cardiovascular risk factors",
            "Family history"
        ],
        primary_authority=[
            "Grundy SM, et al. 2018 AHA/ACC Cholesterol Guidelines.",
            "Goldman-Cecil Medicine, 26th Ed.",
            "Braunwald’s Heart Disease, 12th Ed."
        ],
        burden_holder="Ordering clinician",
        adversary_position="Single measurements may not reflect long-term risk",
        counter_arguments=[
            "Acute illness can lower lipid levels",
            "Non-fasting samples may confound triglycerides",
            "Genetic factors may require specialized testing",
            "Lifestyle factors are often underestimated",
            "Medication adherence can affect results"
        ],
        resolution_strategy="Repeat and confirm abnormal results; address secondary causes and initiate guideline-based therapy.",
        entity_scope="Patient",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "AHA/ACC Guidelines 2018",
            "Braunwald, Ch 44"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.LIPID_PANEL
    ),
    DoctrineBlock(
        topic="Urinalysis: Dipstick, Microscopy, and Culture",
        keywords=["urinalysis", "dipstick", "microscopy", "urine culture", "UTI"],
        conclusion_template="Urinalysis is a key diagnostic tool for renal and urinary tract disorders. Dipstick detects protein, blood, leukocyte esterase, and nitrites. Microscopy identifies cells, casts, and crystals. Culture confirms infection.",
        reasoning_framework=(
            "1. Dipstick: positive leukocyte esterase/nitrites suggests UTI; proteinuria may indicate glomerular disease.\n"
            "2. Microscopy: RBCs suggest hematuria; WBCs indicate infection or inflammation; casts point to renal origin.\n"
            "3. Crystals may suggest metabolic disorders (uric acid, oxalate, cystine).\n"
            "4. Bacteria on microscopy support infection but are not definitive without culture.\n"
            "5. Contamination can cause false positives; clean-catch technique is essential.\n"
            "6. Urine culture is gold standard for UTI diagnosis; >10^5 CFU/mL is significant in most cases.\n"
            "7. Asymptomatic bacteriuria does not always require treatment except in pregnancy or prior to urologic procedures.\n"
            "8. Repeat testing if results are inconsistent with clinical findings.\n"
            "9. Consider imaging for persistent hematuria or proteinuria.\n"
            "10. Consult nephrology or urology for complex cases."
        ),
        key_factors=[
            "Dipstick findings (leukocyte esterase, nitrites, protein, blood)",
            "Microscopy (cells, casts, crystals)",
            "Culture results",
            "Collection technique",
            "Clinical symptoms"
        ],
        primary_authority=[
            "National Kidney Foundation KDOQI Guidelines",
            "Goldman-Cecil Medicine, 26th Ed.",
            "Roberts JA, et al. UTI Guidelines"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Contamination and false positives are common",
        counter_arguments=[
            "Improper collection can confound results",
            "Asymptomatic bacteriuria may not require treatment",
            "Dipstick is less sensitive than culture",
            "Microscopy is operator-dependent",
            "Non-infectious causes of hematuria/proteinuria"
        ],
        resolution_strategy="Correlate urinalysis with clinical findings; confirm infection with culture.",
        entity_scope="Patient",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "KDOQI Guidelines 2020",
            "Roberts JA, UTI Guidelines"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.URINALYSIS
    ),
    DoctrineBlock(
        topic="Blood Gas Analysis: ABG and VBG",
        keywords=["ABG", "VBG", "pH", "pCO2", "bicarbonate", "acid-base"],
        conclusion_template="Arterial and venous blood gases assess acid-base and respiratory status. ABG is preferred for precise oxygenation and acid-base analysis. VBG can approximate pH and CO2 but not oxygenation.",
        reasoning_framework=(
            "1. ABG: assess pH, pCO2, pO2, HCO3-; identify primary disorder (acidosis/alkalosis, respiratory/metabolic).\n"
            "2. Calculate anion gap for metabolic acidosis; assess for compensation using Winter's formula or expected compensation rules.\n"
            "3. VBG: pH and pCO2 are ~0.03-0.05 lower/higher than ABG; not reliable for pO2.\n"
            "4. Mixed acid-base disorders are common in critically ill patients.\n"
            "5. Oxygenation (PaO2) only accurately measured on ABG.\n"
            "6. Consider clinical context: shock, respiratory failure, DKA, renal failure.\n"
            "7. Repeat sampling if results are unexpected or inconsistent.\n"
            "8. Pre-analytical errors (air bubbles, delayed analysis) can alter results.\n"
            "9. Use blood gas in conjunction with clinical and laboratory data.\n"
            "10. Consult critical care or nephrology for complex acid-base disorders."
        ),
        key_factors=[
            "pH, pCO2, pO2, HCO3- values",
            "Anion gap calculation",
            "Compensation assessment",
            "Clinical scenario",
            "Sampling technique"
        ],
        primary_authority=[
            "Kraut JA, Madias NE. N Engl J Med 2018;378:2129-38.",
            "Goldman-Cecil Medicine, 26th Ed.",
            "UpToDate: Acid-base disorders"
        ],
        burden_holder="Ordering clinician",
        adversary_position="VBG is not a substitute for ABG in all cases",
        counter_arguments=[
            "VBG cannot assess oxygenation",
            "Pre-analytical errors are common",
            "Mixed disorders may be missed",
            "Compensation formulas are approximations",
            "Clinical context is essential"
        ],
        resolution_strategy="Use ABG for definitive analysis; VBG for trend or when ABG not feasible.",
        entity_scope="Patient",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "NEJM 2018;378:2129-38",
            "Goldman-Cecil, Ch 98"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.BLOOD_GAS
    ),
    DoctrineBlock(
        topic="Hemoglobin A1c for Diabetes Monitoring",
        keywords=["hemoglobin A1c", "diabetes", "glycemic control", "chronic hyperglycemia"],
        conclusion_template="Hemoglobin A1c reflects average glycemia over ~3 months. It is used for diagnosis and monitoring of diabetes. Values ≥6.5% are diagnostic, but interpretation must consider hemoglobinopathies and red cell turnover.",
        reasoning_framework=(
            "1. A1c ≥6.5% on two occasions or with symptoms is diagnostic of diabetes.\n"
            "2. A1c reflects mean glucose over prior 2-3 months; does not capture acute fluctuations.\n"
            "3. Conditions affecting red cell turnover (hemolysis, recent transfusion, anemia) can falsely lower or raise A1c.\n"
            "4. Hemoglobin variants may interfere with some assays.\n"
            "5. Target A1c individualized based on age, comorbidities, and hypoglycemia risk.\n"
            "6. A1c <7% is typical goal for most non-pregnant adults; less stringent for elderly or high-risk patients.\n"
            "7. Repeat testing every 3-6 months based on control and therapy changes.\n"
            "8. Use in conjunction with SMBG/CGM for comprehensive assessment.\n"
            "9. Consider alternative markers (fructosamine) if A1c is unreliable.\n"
            "10. Consult endocrinology for discordant or unexplained results."
        ),
        key_factors=[
            "A1c value and assay method",
            "Red cell turnover status",
            "Hemoglobin variants",
            "Clinical context",
            "Therapy and monitoring frequency"
        ],
        primary_authority=[
            "ADA Standards of Medical Care in Diabetes—2023.",
            "Goldman-Cecil Medicine, 26th Ed.",
            "UpToDate: Hemoglobin A1c"
        ],
        burden_holder="Ordering clinician",
        adversary_position="A1c may be inaccurate in certain conditions",
        counter_arguments=[
            "Hemolytic anemia lowers A1c",
            "Recent transfusion confounds results",
            "Assay interference by hemoglobinopathies",
            "A1c does not reflect acute control",
            "Individualized targets required"
        ],
        resolution_strategy="Interpret A1c in clinical context; use alternative markers if indicated.",
        entity_scope="Patient",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ADA Standards 2023",
            "Goldman-Cecil, Ch 229"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.HEMOGLOBIN_A1C
    ),
    DoctrineBlock(
        topic="Blood Culture Identification and Sensitivity",
        keywords=["blood culture", "bacteremia", "sepsis", "antibiotic sensitivity"],
        conclusion_template="Blood cultures are the gold standard for diagnosing bacteremia and guiding antibiotic therapy. Timely collection prior to antibiotics and proper technique are essential for accuracy. Sensitivity testing directs optimal therapy.",
        reasoning_framework=(
            "1. Collect at least two sets from separate sites prior to antibiotics.\n"
            "2. Aseptic technique reduces contamination; false positives can occur with skin flora.\n"
            "3. Growth in multiple bottles and rapid time to positivity suggest true bacteremia.\n"
            "4. Identification of organism guides therapy; Gram stain provides early clues.\n"
            "5. Sensitivity (MIC) testing determines antibiotic selection; consider local resistance patterns.\n"
            "6. Repeat cultures may be needed to document clearance, especially in endocarditis or device infections.\n"
            "7. Negative cultures do not exclude infection, especially with prior antibiotics or fastidious organisms.\n"
            "8. Fungal and mycobacterial cultures may be indicated in immunocompromised hosts.\n"
            "9. Always correlate with clinical findings and other laboratory/imaging data.\n"
            "10. Infectious diseases consultation is advised for complex cases."
        ),
        key_factors=[
            "Number and timing of cultures",
            "Aseptic technique",
            "Organism identification",
            "Sensitivity results",
            "Clinical context"
        ],
        primary_authority=[
            "IDSA Guidelines for Bloodstream Infections 2023",
            "Mandell, Douglas, and Bennett's Principles and Practice of Infectious Diseases, 9th Ed.",
            "Goldman-Cecil Medicine, 26th Ed."
        ],
        burden_holder="Ordering clinician",
        adversary_position="Contaminants may be misinterpreted as pathogens",
        counter_arguments=[
            "Skin flora can contaminate cultures",
            "Prior antibiotics reduce sensitivity",
            "Fastidious organisms may not grow",
            "Repeat cultures may be required",
            "Interpretation requires clinical context"
        ],
        resolution_strategy="Use strict collection technique; integrate results with clinical and other laboratory data.",
        entity_scope="Patient",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "IDSA Guidelines 2023",
            "Mandell, Ch 69"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.BLOOD_CULTURE
    ),
    DoctrineBlock(
        topic="CSF Analysis: Cell Count, Protein, Glucose",
        keywords=["CSF", "cell count", "protein", "glucose", "meningitis"],
        conclusion_template="CSF analysis is critical for diagnosing CNS infections and inflammatory disorders. Cell count, protein, and glucose help differentiate bacterial, viral, and other etiologies.",
        reasoning_framework=(
            "1. Elevated WBC with neutrophilic predominance, low glucose, and high protein suggest bacterial meningitis.\n"
            "2. Lymphocytic predominance with normal glucose and mildly elevated protein suggests viral meningitis.\n"
            "3. Low glucose may also be seen in TB, fungal, or neoplastic meningitis.\n"
            "4. Xanthochromia indicates subarachnoid hemorrhage or old blood.\n"
            "5. Opening pressure aids in diagnosis (elevated in infection, malignancy, pseudotumor).\n"
            "6. Gram stain and culture are essential for pathogen identification.\n"
            "7. PCR and antigen testing increase diagnostic yield for viral and atypical pathogens.\n"
            "8. Traumatic tap can confound cell count; correction formulas may be used.\n"
            "9. Always interpret in clinical context and with neuroimaging findings.\n"
            "10. Urgent empiric therapy is indicated if bacterial meningitis is suspected."
        ),
        key_factors=[
            "Cell count and differential",
            "Protein and glucose levels",
            "Opening pressure",
            "Gram stain, culture, PCR",
            "Clinical presentation"
        ],
        primary_authority=[
            "Tunkel AR, et al. IDSA Guidelines for Meningitis 2017.",
            "Goldman-Cecil Medicine, 26th Ed.",
            "UpToDate: CSF analysis"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Traumatic tap may confound interpretation",
        counter_arguments=[
            "Blood contamination affects cell count and protein",
            "Prior antibiotics reduce culture yield",
            "PCR may be required for viral pathogens",
            "Glucose may be low in non-infectious etiologies",
            "Clinical urgency may preclude full analysis"
        ],
        resolution_strategy="Correlate CSF findings with clinical and imaging data; initiate empiric therapy as indicated.",
        entity_scope="Patient",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "IDSA Guidelines 2017",
            "Goldman-Cecil, Ch 410"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.CSF_ANALYSIS
    ),
    DoctrineBlock(
        topic="Tumor Markers: PSA, CEA, CA-125, AFP",
        keywords=["tumor markers", "PSA", "CEA", "CA-125", "AFP"],
        conclusion_template="Tumor markers aid in diagnosis, prognosis, and monitoring of malignancies. They are not diagnostic alone and must be interpreted in clinical context. PSA for prostate, CEA for colon, CA-125 for ovarian, and AFP for liver/germ cell tumors.",
        reasoning_framework=(
            "1. PSA: elevated in prostate cancer, BPH, prostatitis; age and race-specific reference ranges.\n"
            "2. CEA: elevated in colorectal cancer, but also in smokers, inflammation, and other cancers.\n"
            "3. CA-125: useful for ovarian cancer monitoring; elevated in benign conditions (endometriosis, menstruation).\n"
            "4. AFP: marker for hepatocellular carcinoma and nonseminomatous germ cell tumors.\n"
            "5. Tumor markers are most useful for monitoring response or recurrence, not screening.\n"
            "6. Serial measurements and trends are more informative than single values.\n"
            "7. False positives and negatives are common; always correlate with imaging and histology.\n"
            "8. Use guideline-based thresholds and algorithms for interpretation.\n"
            "9. Consider assay variability and laboratory reference ranges.\n"
            "10. Oncology consultation for abnormal or rising markers."
        ),
        key_factors=[
            "Marker type and value",
            "Clinical context",
            "Serial trends",
            "Assay method and reference range",
            "Imaging and histology correlation"
        ],
        primary_authority=[
            "NCCN Guidelines: Prostate, Colorectal, Ovarian, Liver Cancers",
            "Goldman-Cecil Medicine, 26th Ed.",
            "UpToDate: Tumor markers"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Markers are not specific or sensitive for early detection",
        counter_arguments=[
            "Benign conditions can elevate markers",
            "Single measurements may be misleading",
            "Assay variability affects results",
            "Markers may not be elevated in all cases",
            "Imaging/histology required for diagnosis"
        ],
        resolution_strategy="Use tumor markers for monitoring and prognosis; confirm diagnosis with tissue and imaging.",
        entity_scope="Patient",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "NCCN Guidelines 2023",
            "Goldman-Cecil, Ch 241"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.TUMOR_MARKERS
    ),
    DoctrineBlock(
        topic="Iron Studies: Ferritin, TIBC, Transferrin Saturation",
        keywords=["iron studies", "ferritin", "TIBC", "transferrin saturation", "iron deficiency"],
        conclusion_template="Iron studies differentiate iron deficiency, anemia of chronic disease, and iron overload. Ferritin reflects stores, TIBC and transferrin saturation assess transport and availability.",
        reasoning_framework=(
            "1. Low ferritin is diagnostic of iron deficiency unless confounded by inflammation.\n"
            "2. High TIBC and low transferrin saturation support iron deficiency.\n"
            "3. Anemia of chronic disease: low/normal iron, low TIBC, normal/high ferritin.\n"
            "4. Iron overload (hemochromatosis): high ferritin, high transferrin saturation, low TIBC.\n"
            "5. Ferritin is an acute phase reactant; may be elevated in inflammation, liver disease, malignancy.\n"
            "6. Always interpret in context of CBC and clinical findings.\n"
            "7. Repeat testing if results are discordant or unexpected.\n"
            "8. Consider genetic testing for suspected hemochromatosis.\n"
            "9. Gastrointestinal evaluation for iron deficiency in adults.\n"
            "10. Specialist referral for refractory or complex cases."
        ),
        key_factors=[
            "Ferritin, TIBC, serum iron, transferrin saturation",
            "CBC findings",
            "Inflammatory markers",
            "Clinical context",
            "Genetic risk factors"
        ],
        primary_authority=[
            "WHO Guidelines on Iron Deficiency 2020",
            "Goldman-Cecil Medicine, 26th Ed.",
            "Hoffbrand AV, Essential Haematology, 8th Ed."
        ],
        burden_holder="Ordering clinician",
        adversary_position="Ferritin may be elevated in inflammation",
        counter_arguments=[
            "Acute phase response confounds ferritin",
            "Transferrin saturation may fluctuate",
            "Iron studies affected by recent transfusion",
            "Chronic disease may mask iron deficiency",
            "Genetic factors may require specialized testing"
        ],
        resolution_strategy="Interpret iron studies with inflammatory markers and clinical context; pursue further testing as indicated.",
        entity_scope="Patient",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "WHO Guidelines 2020",
            "Hoffbrand, Ch 5"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.IRON_STUDIES
    ),
    DoctrineBlock(
        topic="Autoimmune Panel: ANA, anti-dsDNA, RF, CCP",
        keywords=["autoimmune panel", "ANA", "anti-dsDNA", "RF", "CCP", "autoimmunity"],
        conclusion_template="Autoimmune serology aids in diagnosing SLE, RA, and related disorders. ANA is sensitive but not specific for SLE. Anti-dsDNA is more specific. RF and anti-CCP are markers for RA.",
        reasoning_framework=(
            "1. ANA: positive in SLE, other CTDs, and healthy individuals; titer and pattern provide additional information.\n"
            "2. Anti-dsDNA: specific for SLE, correlates with disease activity.\n"
            "3. RF: positive in RA, but also in other diseases and elderly.\n"
            "4. Anti-CCP: high specificity for RA; may be positive before clinical onset.\n"
            "5. False positives are common; always interpret in clinical context.\n"
            "6. Additional antibodies (ENA, SSA, SSB, RNP, Sm) may be indicated based on presentation.\n"
            "7. Repeat testing not recommended unless clinical change.\n"
            "8. Laboratory methods (ELISA, immunofluorescence) affect sensitivity/specificity.\n"
            "9. Specialist input (rheumatology) is essential for diagnosis and management.\n"
            "10. Do not diagnose autoimmune disease based on serology alone."
        ),
        key_factors=[
            "ANA, anti-dsDNA, RF, anti-CCP results",
            "Clinical presentation",
            "Assay method",
            "Additional autoantibodies",
            "Specialist input"
        ],
        primary_authority=[
            "ACR/EULAR Classification Criteria",
            "Goldman-Cecil Medicine, 26th Ed.",
            "UpToDate: Autoantibody testing"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Serology is not diagnostic in isolation",
        counter_arguments=[
            "False positives are common",
            "Assay variability affects results",
            "Clinical correlation is essential",
            "Repeat testing rarely indicated",
            "Other diseases can cause positive serology"
        ],
        resolution_strategy="Use autoimmune panel as adjunct to clinical diagnosis; consult rheumatology.",
        entity_scope="Patient",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ACR/EULAR Criteria 2019",
            "Goldman-Cecil, Ch 263"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.AUTOIMMUNE_PANEL
    ),
    DoctrineBlock(
        topic="Hepatitis Serology: HBsAg, anti-HBs, anti-HCV",
        keywords=["hepatitis serology", "HBsAg", "anti-HBs", "anti-HCV", "liver infection"],
        conclusion_template="Hepatitis serology distinguishes acute, chronic, and resolved infection. HBsAg indicates active HBV infection; anti-HBs indicates immunity. Anti-HCV suggests exposure; RNA testing confirms active infection.",
        reasoning_framework=(
            "1. HBsAg: positive in acute or chronic HBV infection.\n"
            "2. Anti-HBs: positive after recovery or vaccination; indicates immunity.\n"
            "3. Anti-HBc IgM: marker of acute infection; total anti-HBc persists for life.\n"
            "4. Anti-HCV: indicates exposure; HCV RNA required to confirm active infection.\n"
            "5. Window period: HBsAg negative, anti-HBs negative, anti-HBc IgM positive.\n"
            "6. Isolated anti-HBc may indicate resolved infection, false positive, or window period.\n"
            "7. Vaccination status must be considered in interpretation.\n"
            "8. False positives can occur; confirmatory testing is essential.\n"
            "9. Always correlate with clinical and risk factor assessment.\n"
            "10. Specialist referral for chronic infection or unclear serology."
        ),
        key_factors=[
            "HBsAg, anti-HBs, anti-HBc, anti-HCV results",
            "Clinical and vaccination history",
            "HCV RNA testing",
            "Risk factors",
            "Timing of exposure"
        ],
        primary_authority=[
            "CDC Hepatitis B and C Guidelines",
            "Goldman-Cecil Medicine, 26th Ed.",
            "AASLD Guidelines"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Serology may be indeterminate in window period",
        counter_arguments=[
            "False positives/negatives are possible",
            "Vaccination confounds anti-HBs interpretation",
            "RNA testing required for HCV diagnosis",
            "Chronic infection may be asymptomatic",
            "Clinical context is essential"
        ],
        resolution_strategy="Interpret serology with clinical and exposure history; confirm with nucleic acid testing as needed.",
        entity_scope="Patient",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "CDC Guidelines 2021",
            "AASLD Guidelines 2018"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.HEPATITIS_SEROLOGY
    ),
    DoctrineBlock(
        topic="HIV Testing Algorithm: 4th Generation Combo",
        keywords=["HIV testing", "4th generation", "antigen", "antibody", "algorithm"],
        conclusion_template="The 4th generation HIV test detects both p24 antigen and antibodies. It reduces the window period and is the recommended screening method. Reactive results require confirmatory testing.",
        reasoning_framework=(
            "1. 4th generation assay detects p24 antigen and HIV-1/2 antibodies; window period ~2 weeks.\n"
            "2. Reactive screening test is followed by HIV-1/HIV-2 differentiation immunoassay.\n"
            "3. Indeterminate or discordant results require nucleic acid testing (HIV RNA).\n"
            "4. False positives can occur; always confirm before diagnosis.\n"
            "5. Acute infection may be missed if testing is too early; repeat if high suspicion.\n"
            "6. Antigen detection allows earlier diagnosis than antibody-only tests.\n"
            "7. Pre-exposure prophylaxis and ART can affect seroconversion and test results.\n"
            "8. Always correlate with risk factors and clinical findings.\n"
            "9. Counseling and linkage to care are essential for positive results.\n"
            "10. Follow CDC/WHO algorithms for interpretation and follow-up."
        ),
        key_factors=[
            "Screening and confirmatory test results",
            "Timing of exposure",
            "Risk factors",
            "ART/PrEP status",
            "Clinical presentation"
        ],
        primary_authority=[
            "CDC HIV Testing Guidelines 2021",
            "WHO Consolidated Guidelines on HIV Testing",
            "Goldman-Cecil Medicine, 26th Ed."
        ],
        burden_holder="Ordering clinician",
        adversary_position="False positives and early window period may confound results",
        counter_arguments=[
            "Acute infection may be missed if tested too early",
            "ART/PrEP can delay seroconversion",
            "Indeterminate results require RNA testing",
            "Counseling is essential",
            "Algorithm adherence required"
        ],
        resolution_strategy="Follow CDC/WHO algorithms; confirm all reactive results and provide counseling.",
        entity_scope="Patient",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "CDC Guidelines 2021",
            "WHO Guidelines 2019"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.HIV_TESTING
    ),
    DoctrineBlock(
        topic="Drug Screening: Immunoassay and GC-MS Confirmation",
        keywords=["drug screening", "immunoassay", "GC-MS", "toxicology", "false positive"],
        conclusion_template="Drug screening uses immunoassay for rapid detection and GC-MS for confirmation. Immunoassays are sensitive but may yield false positives. GC-MS provides definitive identification.",
        reasoning_framework=(
            "1. Immunoassay screens for common drugs of abuse; rapid but not specific.\n"
            "2. False positives due to cross-reactivity (e.g., poppy seeds, cold medications).\n"
            "3. GC-MS is gold standard for confirmation; required for legal or employment decisions.\n"
            "4. Detection windows vary by substance and chronicity of use.\n"
            "5. Negative screen does not exclude recent or intermittent use.\n"
            "6. Sample adulteration or dilution can affect results; validity testing is essential.\n"
            "7. Always interpret in clinical and social context.\n"
            "8. Chain of custody must be maintained for forensic testing.\n"
            "9. Repeat or alternative testing if results are unexpected or contested.\n"
            "10. Toxicology consultation for complex or disputed cases."
        ),
        key_factors=[
            "Screening and confirmatory test results",
            "Detection window",
            "Sample validity",
            "Clinical and social context",
            "Chain of custody"
        ],
        primary_authority=[
            "SAMHSA Guidelines for Drug Testing",
            "Goldman-Cecil Medicine, 26th Ed.",
            "UpToDate: Drug screening"
        ],
        burden_holder="Ordering clinician/laboratory",
        adversary_position="Immunoassay results may be false positive or negative",
        counter_arguments=[
            "Cross-reactivity leads to false positives",
            "Detection windows are variable",
            "Sample tampering is possible",
            "GC-MS required for confirmation",
            "Legal/occupational consequences of misinterpretation"
        ],
        resolution_strategy="Confirm all positive screens with GC-MS; interpret in context and maintain chain of custody.",
        entity_scope="Patient/Sample",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "SAMHSA Guidelines 2020",
            "Goldman-Cecil, Ch 31"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.DRUG_SCREENING
    ),
    DoctrineBlock(
        topic="Molecular Diagnostics: PCR, FISH, NGS",
        keywords=["molecular diagnostics", "PCR", "FISH", "NGS", "genetic testing"],
        conclusion_template="Molecular diagnostics enable detection of pathogens, mutations, and chromosomal abnormalities. PCR is rapid and sensitive for nucleic acid detection. FISH identifies chromosomal changes. NGS allows high-throughput sequencing.",
        reasoning_framework=(
            "1. PCR: detects specific DNA/RNA sequences; used for infectious diseases, genetic mutations, minimal residual disease.\n"
            "2. FISH: visualizes chromosomal abnormalities (translocations, deletions, amplifications); used in hematologic and solid tumors.\n"
            "3. NGS: high-throughput sequencing for gene panels, exomes, or genomes; enables precision medicine.\n"
            "4. Pre-analytical factors (sample type, quality) affect sensitivity and specificity.\n"
            "5. Interpretation requires knowledge of assay limitations, variant classification, and clinical context.\n"
            "6. False positives/negatives can occur; confirmatory testing may be needed.\n"
            "7. Incidental findings and variants of uncertain significance require careful counseling.\n"
            "8. Laboratory accreditation and quality control are essential.\n"
            "9. Genetic counseling recommended for heritable findings.\n"
            "10. Multidisciplinary input for complex or actionable results."
        ),
        key_factors=[
            "Assay type and target",
            "Sample quality",
            "Variant/pathogen detected",
            "Clinical context",
            "Confirmatory testing"
        ],
        primary_authority=[
            "ACMG Standards and Guidelines",
            "Goldman-Cecil Medicine, 26th Ed.",
            "UpToDate: Molecular diagnostics"
        ],
        burden_holder="Ordering clinician/laboratory",
        adversary_position="Assay limitations and incidental findings may complicate interpretation",
        counter_arguments=[
            "Sample quality affects results",
            "Variants of uncertain significance",
            "False positives/negatives possible",
            "Counseling required for genetic findings",
            "Laboratory accreditation essential"
        ],
        resolution_strategy="Interpret molecular results with clinical and laboratory context; confirm and counsel as indicated.",
        entity_scope="Patient/Sample",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ACMG Guidelines 2021",
            "Goldman-Cecil, Ch 32"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.MOLECULAR_DIAGNOSTICS
    ),
    DoctrineBlock(
        topic="Flow Cytometry: Immunophenotyping in Lymphoma/Leukemia",
        keywords=["flow cytometry", "immunophenotyping", "lymphoma", "leukemia", "CD markers"],
        conclusion_template="Flow cytometry is essential for immunophenotyping hematologic malignancies. It identifies cell lineage, clonality, and aberrant antigen expression, guiding diagnosis and classification.",
        reasoning_framework=(
            "1. Flow cytometry analyzes surface and cytoplasmic antigens (CD markers) on single cells.\n"
            "2. Distinguishes B-cell, T-cell, and myeloid lineage; detects aberrant or clonal populations.\n"
            "3. Essential for diagnosis and classification of acute and chronic leukemias, lymphomas, and myelodysplastic syndromes.\n"
            "4. Sample quality (fresh, viable cells) is critical for accurate analysis.\n"
            "5. Panel selection (antibodies) tailored to clinical suspicion and morphology.\n"
            "6. Results must be integrated with morphology, cytogenetics, and molecular studies.\n"
            "7. Minimal residual disease assessment by flow cytometry guides therapy and prognosis.\n"
            "8. False positives/negatives possible due to technical or biological factors.\n"
            "9. Laboratory expertise and standardization are essential.\n"
            "10. Hematopathology consultation for interpretation and reporting."
        ),
        key_factors=[
            "CD marker expression",
            "Lineage and clonality",
            "Sample quality",
            "Panel selection",
            "Integration with other studies"
        ],
        primary_authority=[
            "WHO Classification of Tumours of Haematopoietic and Lymphoid Tissues, 5th Ed.",
            "Goldman-Cecil Medicine, 26th Ed.",
            "UpToDate: Flow cytometry"
        ],
        burden_holder="Ordering clinician/laboratory",
        adversary_position="Results may be confounded by sample quality or technical factors",
        counter_arguments=[
            "Sample degradation affects analysis",
            "Panel selection may miss rare entities",
            "Interpretation requires expertise",
            "False positives/negatives possible",
            "Integration with other modalities required"
        ],
        resolution_strategy="Ensure optimal sample handling; integrate flow cytometry with morphology and molecular data.",
        entity_scope="Patient/Sample",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "WHO Classification 2022",
            "Goldman-Cecil, Ch 104"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.FLOW_CYTOMETRY
    ),
    # ... (Add additional doctrine blocks as needed for full coverage)
]

# =========================
# AUTHORITY HARDENING
# =========================

AUTHORITY_WEIGHTS = {
    "CDC": 1.0,
    "WHO": 1.0,
    "IDSA": 0.95,
    "AASLD": 0.95,
    "ADA": 0.95,
    "AHA": 0.95,
    "ACC": 0.95,
    "NCCN": 0.95,
    "ACMG": 0.95,
    "ASH": 0.95,
    "KDOQI": 0.9,
    "UpToDate": 0.85,
    "Goldman-Cecil": 0.9,
    "Braunwald": 0.9,
    "Hoffbrand": 0.9,
    "Williams": 0.9,
    "Mandell": 0.9,
    "SAMHSA": 0.9,
    "Roberts": 0.85,
    "Kumar & Clark": 0.85,
    "Brenner & Rector": 0.85,
    "Zakim & Boyer": 0.85,
    "Tunkel": 0.85,
    "Ross": 0.85,
    "Thygesen": 0.85,
    "Grundy": 0.85,
    "Kitchens": 0.85,
    "Other": 0.8,
}

def resolve_authority_conflict(authorities: List[str]) -> Tuple[str, float]:
    max_weight = 0
    selected = ""
    for auth in authorities:
        for key in AUTHORITY_WEIGHTS:
            if key.lower() in auth.lower():
                if AUTHORITY_WEIGHTS[key] > max_weight:
                    max_weight = AUTHORITY_WEIGHTS[key]
                    selected = auth
    if not selected and authorities:
        selected = authorities[0]
        max_weight = 0.8
    return selected, max_weight

# =========================
# SEMANTIC NORMALIZATION
# =========================

SEMANTIC_MAP = {
    "CBC": ["complete blood count", "hemogram", "full blood count"],
    "WBC": ["white blood cell", "leukocyte"],
    "PLT": ["platelet", "thrombocyte"],
    "HbA1c": ["hemoglobin A1c", "glycated hemoglobin"],
    "PT": ["prothrombin time"],
    "INR": ["international normalized ratio"],
    "BMP": ["basic metabolic panel"],
    "CMP": ["comprehensive metabolic panel"],
    "ALT": ["alanine aminotransferase"],
    "AST": ["aspartate aminotransferase"],
    "BNP": ["B-type natriuretic peptide"],
    "CK-MB": ["creatine kinase-MB"],
    "TSH": ["thyroid stimulating hormone"],
    "T4": ["thyroxine"],
    "T3": ["triiodothyronine"],
    "LDL": ["low density lipoprotein"],
    "HDL": ["high density lipoprotein"],
    "UA": ["urinalysis"],
    "ABG": ["arterial blood gas"],
    "VBG": ["venous blood gas"],
    "ANA": ["antinuclear antibody"],
    "RF": ["rheumatoid factor"],
    "CCP": ["cyclic citrullinated peptide"],
    "HBsAg": ["hepatitis B surface antigen"],
    "anti-HBs": ["hepatitis B surface antibody"],
    "anti-HCV": ["hepatitis C antibody"],
    "PCR": ["polymerase chain reaction"],
    "FISH": ["fluorescence in situ hybridization"],
    "NGS": ["next generation sequencing"],
    "PSA": ["prostate specific antigen"],
    "CEA": ["carcinoembryonic antigen"],
    "CA-125": ["cancer antigen 125"],
    "AFP": ["alpha-fetoprotein"],
    "TIBC": ["total iron binding capacity"],
    "GGT": ["gamma-glutamyl transferase"],
    "MIC": ["minimum inhibitory concentration"],
    "MRD": ["minimal residual disease"],
    "CD": ["cluster of differentiation"],
}

def normalize_term(term: str) -> str:
    term = term.lower()
    for k, vlist in SEMANTIC_MAP.items():
        if term == k.lower() or term in [v.lower() for v in vlist]:
            return k
    return term

def semantic_expand(term: str) -> Set[str]:
    term = term.upper()
    expanded = set([term])
    if term in SEMANTIC_MAP:
        expanded.update([v.upper() for v in SEMANTIC_MAP[term]])
    return expanded

# =========================
# EPISTEMIC GUARDRAILS
# =========================

BANNED_PHRASES = [
    "always", "never", "definitely", "certainly", "guaranteed", "must", "no doubt", "impossible", "cannot fail"
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "[REDACTED]")
    return text

# =========================
# FACT FRAGILITY SCORING
# =========================

def score_fact_fragility(doctrine: DoctrineBlock) -> Dict[str, float]:
    verifiability = 1.0 if doctrine.primary_authority else 0.7
    recharacterization_risk = 0.2 if doctrine.confidence_zone == ConfidenceZone.DEFENSIBLE else 0.5
    testimony_dependence = 0.3 if "UpToDate" in " ".join(doctrine.primary_authority) else 0.1
    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence
    }

# =========================
# THREE LAYER RESPONSE
# =========================

def doctrine_layer(scenario: str) -> Optional[DoctrineBlock]:
    scenario_norm = scenario.lower()
    for doctrine in DOCTRINE_CACHE:
        for kw in doctrine.keywords:
            if kw.lower() in scenario_norm:
                return doctrine
    return None

def semantic_search_layer(scenario: str) -> Optional[DoctrineBlock]:
    scenario_terms = set(normalize_term(word) for word in scenario.split())
    best_score = 0
    best_doctrine = None
    for doctrine in DOCTRINE_CACHE:
        doctrine_terms = set(normalize_term(kw) for kw in doctrine.keywords)
        score = len(scenario_terms & doctrine_terms)
        if score > best_score:
            best_score = score
            best_doctrine = doctrine
    return best_doctrine

def deep_analysis_layer(scenario: str) -> Optional[DoctrineBlock]:
    # Decompose scenario into issue categories, match to doctrine, and simulate interaction DAG
    for doctrine in DOCTRINE_CACHE:
        if doctrine.issue_category.value.lower() in scenario.lower():
            return doctrine
    return None

# =========================
# DEEP ANALYSIS
# =========================

def multi_doctrine_decomposition(scenario: str) -> List[DoctrineBlock]:
    hits = []
    for doctrine in DOCTRINE_CACHE:
        for kw in doctrine.keywords:
            if kw.lower() in scenario.lower():
                hits.append(doctrine)
                break
    return hits

def interaction_dag(doctrines: List[DoctrineBlock]) -> Dict[str, Any]:
    dag = {}
    for doctrine in doctrines:
        dag[doctrine.topic] = {
            "depends_on": [],
            "conflicts_with": [],
            "reinforces": []
        }
        for other in doctrines:
            if other is doctrine:
                continue
            if set(doctrine.keywords) & set(other.keywords):
                dag[doctrine.topic]["reinforces"].append(other.topic)
    return dag

def eight_step_resolution(doctrines: List[DoctrineBlock], scenario: str) -> str:
    steps = [
        "1. Identify relevant doctrines based on scenario keywords.",
        "2. Map scenario to doctrine issue categories.",
        "3. Assess authority and confidence for each doctrine.",
        "4. Score fact fragility and epistemic risk.",
        "5. Resolve conflicts using authority hardening.",
        "6. Integrate reasoning frameworks and key factors.",
        "7. Apply epistemic guardrails to all conclusions.",
        "8. Synthesize a primary conclusion and resolution strategy."
    ]
    conclusion = ""
    for doctrine in doctrines:
        conclusion += f"{doctrine.topic}: {apply_epistemic_guardrails(doctrine.conclusion_template)}\n"
    return "\n".join(steps) + "\n\n" + conclusion

# =========================
# COVERAGE MAP
# =========================

def coverage_map(scenario: str) -> Dict[str, Any]:
    triggered = []
    missed = []
    for doctrine in DOCTRINE_CACHE:
        if any(kw.lower() in scenario.lower() for kw in doctrine.keywords):
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

DRIFT_BASELINE = [d.topic for d in DOCTRINE_CACHE]

def drift_watcher() -> Dict[str, Any]:
    current = [d.topic for d in DOCTRINE_CACHE]
    drift = set(DRIFT_BASELINE) ^ set(current)
    return {
        "baseline": DRIFT_BASELINE,
        "current": current,
        "drift_detected": bool(drift),
        "drift_topics": list(drift)
    }

# =========================
# AUDIT TRAIL
# =========================

AUDIT_LOG_PATH = Path(__file__).parent / "audit_log.jsonl"
AUDIT_LOCK = threading.Lock()

def log_audit(query: QueryRequest, response: QueryResponse):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query": query.dict(),
        "response": response.dict()
    }
    with AUDIT_LOCK:
        with open(AUDIT_LOG_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")

# =========================
# DETERMINISM HASH
# =========================

def determinism_hash(query: QueryRequest, doctrine: DoctrineBlock) -> str:
    m = hashlib.sha256()
    m.update(json.dumps(query.dict(), sort_keys=True).encode())
    m.update(json.dumps({
        "topic": doctrine.topic,
        "conclusion_template": doctrine.conclusion_template,
        "reasoning_framework": doctrine.reasoning_framework,
        "primary_authority": doctrine.primary_authority
    }, sort_keys=True).encode())
    return m.hexdigest()

# =========================
# FASTAPI APP
# =========================

app = FastAPI(
    title="Clinical Pathology Engine (ECHO OMEGA PRIME)",
    description="Clinical chemistry, hematology, microbiology, and molecular diagnostics engine.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    logger.info("Clinical Pathology Engine started.")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Clinical Pathology Engine shutting down.")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    query_id = str(uuid.uuid4())
    start = datetime.utcnow()
    try:
        doctrine = doctrine_layer(request.scenario)
        doctrine_hit = "Layer1"
        if not doctrine:
            doctrine = semantic_search_layer(request.scenario)
            doctrine_hit = "Layer2"
        if not doctrine:
            doctrine = deep_analysis_layer(request.scenario)
            doctrine_hit = "Layer3"
        if not doctrine:
            doctrines = multi_doctrine_decomposition(request.scenario)
            if doctrines:
                doctrine = doctrines[0]
                doctrine_hit = "Multi"
            else:
                doctrine = DOCTRINE_CACHE[0]
                doctrine_hit = "Default"
        latency = (datetime.utcnow() - start).total_seconds() * 1000
        metrics.record_query(doctrine_hit, latency)
        primary_authority, authority_weight = resolve_authority_conflict(doctrine.primary_authority)
        fragility = score_fact_fragility(doctrine)
        conclusion = apply_epistemic_guardrails(doctrine.conclusion_template)
        reasoning = apply_epistemic_guardrails(doctrine.reasoning_framework)
        response = QueryResponse(
            engine_id="MED05",
            query_id=query_id,
            mode=request.mode,
            confidence=doctrine.confidence * authority_weight * (1 - fragility["recharacterization_risk"]),
            confidence_zone=doctrine.confidence_zone,
            position_zone=doctrine.position_zone,
            primary_conclusion=conclusion,
            reasoning_framework=reasoning,
            key_factors=doctrine.key_factors,
            primary_authority=doctrine.primary_authority,
            counter_arguments=doctrine.counter_arguments,
            resolution_strategy=doctrine.resolution_strategy,
            determinism_hash=determinism_hash(request, doctrine)
        )
        log_audit(request, response)
        return response
    except Exception as e:
        logger.error(f"Query error: {e}")
        metrics.record_error(str(e))
        raise

@app.get("/health")
async def health():
    return {"status": "ok", "engine_id": "MED05"}

@app.get("/metrics")
async def metrics_endpoint():
    return {
        "latency": metrics.get_latency_stats(),
        "doctrine_hit_rate": metrics.get_doctrine_hit_rate(),
        "queries_last_hour": metrics.queries_last_hour(),
        "errors": len(metrics.errors)
    }

@app.get("/coverage")
async def coverage_endpoint(scenario: Optional[str] = None):
    if not scenario:
        return {"error": "scenario required"}
    return coverage_map(scenario)

@app.get("/drift")
async def drift_endpoint():
    return drift_watcher()

@app.get("/doctrines")
async def doctrines_endpoint():
    return [
        {
            "topic": d.topic,
            "keywords": d.keywords,
            "confidence": d.confidence,
            "confidence_zone": d.confidence_zone,
            "position_zone": d.position_zone,
            "issue_category": d.issue_category
        }
        for d in DOCTRINE_CACHE
    ]
