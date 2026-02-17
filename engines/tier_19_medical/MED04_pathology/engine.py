import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple, Set, Union
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
    CBC_INTERPRETATION = "CBC_INTERPRETATION"
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
    MISC = "MISC"

# =========================
# METRICS COLLECTOR
# =========================

class MetricsCollector:
    def __init__(self):
        self.queries = []
        self.errors = []
        self.doctrine_hits = {}
        self.lock = threading.Lock()

    def record_query(self, query_id: str, doctrine_ids: List[str], latency: float):
        with self.lock:
            self.queries.append({
                "timestamp": datetime.utcnow(),
                "query_id": query_id,
                "doctrines": doctrine_ids,
                "latency": latency
            })
            for d in doctrine_ids:
                self.doctrine_hits[d] = self.doctrine_hits.get(d, 0) + 1

    def record_error(self, query_id: str, error: str):
        with self.lock:
            self.errors.append({
                "timestamp": datetime.utcnow(),
                "query_id": query_id,
                "error": error
            })

    def get_latency_stats(self) -> Dict[str, float]:
        with self.lock:
            if not self.queries:
                return {"avg": 0, "min": 0, "max": 0}
            latencies = [q["latency"] for q in self.queries]
            return {
                "avg": sum(latencies) / len(latencies),
                "min": min(latencies),
                "max": max(latencies)
            }

    def get_doctrine_hit_rate(self) -> Dict[str, int]:
        with self.lock:
            return dict(self.doctrine_hits)

    def queries_last_hour(self) -> int:
        cutoff = datetime.utcnow() - timedelta(hours=1)
        with self.lock:
            return sum(1 for q in self.queries if q["timestamp"] > cutoff)

metrics_collector = MetricsCollector()

# =========================
# PYDANTIC MODELS
# =========================

class QueryRequest(BaseModel):
    scenario: str = Field(..., description="Clinical scenario or question")
    mode: ResponseMode = Field(..., description="Response mode")
    entity_type: str = Field(..., description="Type of entity (e.g. patient, sample)")
    complexity: int = Field(..., description="Complexity level (1-5)")

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
    position_zone: PositionZone
    issue_category: IssueCategory

# Domain doctrine blocks (EXCERPT: 30+ authoritative blocks)
DOCTRINE_CACHE: Dict[str, DoctrineBlock] = {}

def _init_doctrines():
    # CBC Differential Interpretation
    DOCTRINE_CACHE["CBC_DIFF_01"] = DoctrineBlock(
        doctrine_id="CBC_DIFF_01",
        topic="CBC Differential Interpretation",
        keywords=["CBC", "differential", "neutrophilia", "lymphocytosis", "leukocytosis", "anemia", "thrombocytopenia"],
        conclusion_template="A complete blood count with differential provides critical information regarding the patient's hematologic status. Interpretation must consider age, clinical context, and reference ranges. Abnormalities such as neutrophilia or lymphocytosis may indicate infection, inflammation, or hematologic malignancy.",
        reasoning_framework="""
1. Review the total white blood cell (WBC) count and compare to age-specific reference ranges (Hoffbrand AV et al., 2019).
2. Evaluate the relative and absolute counts of neutrophils, lymphocytes, monocytes, eosinophils, and basophils.
3. Assess for patterns: neutrophilia often suggests bacterial infection or stress; lymphocytosis may indicate viral infection or chronic lymphocytic leukemia (CLL).
4. Consider anemia: low hemoglobin/hematocrit may result from blood loss, hemolysis, or marrow failure.
5. Thrombocytopenia or thrombocytosis should be interpreted in the context of acute phase reactants, infection, or myeloproliferative disorders.
6. Examine red cell indices (MCV, MCH, MCHC) for microcytic, normocytic, or macrocytic anemia.
7. Correlate findings with clinical presentation, medications, and comorbidities.
8. Rule out pseudoleukopenia or pseudothrombocytopenia due to sample artifact (e.g., EDTA-induced clumping).
9. If abnormal cells (blasts, atypical lymphocytes) are present, consider further workup with flow cytometry or bone marrow biopsy.
10. Use serial CBCs to monitor trends and response to therapy.
11. Reference: Bain BJ. Blood Cells: A Practical Guide. 6th Ed. Wiley-Blackwell, 2015.
12. Reference: Hoffbrand AV, Higgs DR, Keeling DM, Mehta AB. Postgraduate Haematology. 7th Ed. Wiley, 2019.
        """,
        key_factors=[
            "WBC differential patterns",
            "Red cell indices",
            "Platelet count",
            "Clinical context",
            "Sample artifact"
        ],
        primary_authority=[
            "Bain BJ. Blood Cells: A Practical Guide. 6th Ed. Wiley-Blackwell, 2015.",
            "Hoffbrand AV, Higgs DR, Keeling DM, Mehta AB. Postgraduate Haematology. 7th Ed. Wiley, 2019.",
            "WHO Laboratory Manual for the Examination and Processing of Human Blood, 2021."
        ],
        burden_holder="Interpreter/Ordering Clinician",
        adversary_position="Overinterpretation of minor abnormalities without clinical correlation.",
        counter_arguments=[
            "CBC results may be affected by sample handling errors.",
            "Reference ranges vary by age, sex, and laboratory.",
            "Transient changes may not reflect underlying disease.",
            "Automated differentials may miss rare abnormal cells.",
            "Clinical context is essential for interpretation."
        ],
        resolution_strategy="Correlate laboratory findings with clinical scenario and, if needed, repeat testing or perform confirmatory studies.",
        entity_scope="Patient sample",
        confidence=0.98,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Bain BJ. Blood Cells: A Practical Guide. 6th Ed. Wiley-Blackwell, 2015.",
            "Hoffbrand AV et al., Postgraduate Haematology, 2019."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.CBC_INTERPRETATION
    )
    # Coagulation Studies: PT, INR, PTT, Fibrinogen, D-dimer
    DOCTRINE_CACHE["COAG_01"] = DoctrineBlock(
        doctrine_id="COAG_01",
        topic="Coagulation Studies Interpretation",
        keywords=["PT", "INR", "PTT", "fibrinogen", "D-dimer", "coagulopathy", "bleeding", "thrombosis"],
        conclusion_template="Coagulation studies are essential for evaluating bleeding and thrombotic disorders. Prolonged PT/INR or PTT may indicate factor deficiencies, liver disease, or anticoagulant therapy. Elevated D-dimer suggests active fibrinolysis but is not specific for thrombosis.",
        reasoning_framework="""
1. Assess PT/INR for extrinsic pathway (factors VII, X, V, II, fibrinogen) and PTT for intrinsic pathway (factors XII, XI, IX, VIII).
2. Prolonged PT/INR with normal PTT suggests factor VII deficiency or warfarin effect.
3. Prolonged PTT with normal PT/INR suggests hemophilia A/B or heparin effect.
4. Both prolonged: consider liver disease, DIC, vitamin K deficiency, or multiple factor deficiencies.
5. Low fibrinogen and elevated D-dimer support diagnosis of DIC (Taylor FB et al., 2001).
6. D-dimer is sensitive but not specific for VTE; negative D-dimer rules out VTE in low-risk patients (Kearon C et al., 2016).
7. Mixing studies distinguish factor deficiency from inhibitor presence.
8. Always correlate with clinical bleeding or thrombosis risk.
9. Reference: Kearon C, Akl EA, Ornelas J, et al. Antithrombotic Therapy for VTE Disease: CHEST Guideline and Expert Panel Report. Chest. 2016.
10. Reference: Taylor FB, Toh CH, Hoots WK, Wada H, Levi M. Towards definition, clinical and laboratory criteria, and a scoring system for disseminated intravascular coagulation. Thromb Haemost. 2001.
        """,
        key_factors=[
            "PT/INR and PTT results",
            "Fibrinogen level",
            "D-dimer value",
            "Mixing study outcome",
            "Clinical bleeding/thrombosis risk"
        ],
        primary_authority=[
            "Kearon C, Akl EA, Ornelas J, et al. CHEST Guideline and Expert Panel Report. Chest. 2016.",
            "Taylor FB, Toh CH, Hoots WK, Wada H, Levi M. Thromb Haemost. 2001.",
            "Lowe GD, et al. Guidelines on measurement of D-dimers in plasma. Br J Haematol. 2000."
        ],
        burden_holder="Ordering Physician",
        adversary_position="Assuming abnormal results always indicate clinical disease.",
        counter_arguments=[
            "D-dimer is elevated in many non-thrombotic conditions.",
            "Liver disease can affect multiple coagulation factors.",
            "Anticoagulant therapy alters results.",
            "Acute phase response can increase fibrinogen.",
            "Preanalytical variables (e.g., underfilling tubes) can artifactually prolong PT/PTT."
        ],
        resolution_strategy="Interpret in clinical context; confirm with additional studies if indicated.",
        entity_scope="Patient coagulation status",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Kearon C et al., Chest, 2016.",
            "Taylor FB et al., Thromb Haemost, 2001."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.COAGULATION
    )
    # Basic Metabolic Panel (BMP)
    DOCTRINE_CACHE["BMP_01"] = DoctrineBlock(
        doctrine_id="BMP_01",
        topic="Basic Metabolic Panel Interpretation",
        keywords=["BMP", "electrolytes", "glucose", "BUN", "creatinine", "renal function", "acid-base"],
        conclusion_template="The basic metabolic panel evaluates renal function, electrolyte balance, and glucose status. Abnormalities must be interpreted in the context of hydration, medications, and comorbidities.",
        reasoning_framework="""
1. Review sodium, potassium, chloride, and bicarbonate for electrolyte disturbances (Kraut JA, Madias NE, 2007).
2. Assess glucose for hypo/hyperglycemia; consider diabetes, stress, or iatrogenic causes.
3. Evaluate BUN and creatinine for renal function; calculate BUN/Cr ratio for pre-renal, renal, or post-renal causes.
4. Examine anion gap for metabolic acidosis; high anion gap suggests lactic acidosis, ketoacidosis, or toxins.
5. Consider medications (diuretics, ACE inhibitors) and comorbidities (heart failure, liver disease).
6. Check for pseudohyponatremia or pseudohyperkalemia due to lab artifact.
7. Serial monitoring is essential for acute changes.
8. Reference: Kraut JA, Madias NE. Disorders of Acid-Base Balance. N Engl J Med. 2007.
9. Reference: KDIGO 2012 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease.
        """,
        key_factors=[
            "Electrolyte levels",
            "Renal function markers",
            "Glucose value",
            "Anion gap",
            "Medication effects"
        ],
        primary_authority=[
            "Kraut JA, Madias NE. N Engl J Med. 2007.",
            "KDIGO 2012 CKD Guideline.",
            "UpToDate: Overview of the basic metabolic panel."
        ],
        burden_holder="Ordering Clinician",
        adversary_position="Misattributing chronic abnormalities to acute illness.",
        counter_arguments=[
            "Lab artifacts can cause spurious results.",
            "Chronic kidney disease alters baseline values.",
            "Medications can affect electrolytes.",
            "Acute illness may transiently affect glucose.",
            "Reference ranges differ by laboratory."
        ],
        resolution_strategy="Correlate with clinical status and repeat abnormal results if unexpected.",
        entity_scope="Patient serum chemistry",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Kraut JA, Madias NE. N Engl J Med. 2007.",
            "KDIGO 2012 CKD Guideline."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.METABOLIC_PANEL
    )
    # Comprehensive Metabolic Panel (CMP)
    DOCTRINE_CACHE["CMP_01"] = DoctrineBlock(
        doctrine_id="CMP_01",
        topic="Comprehensive Metabolic Panel Interpretation",
        keywords=["CMP", "liver enzymes", "albumin", "alkaline phosphatase", "bilirubin", "AST", "ALT"],
        conclusion_template="The comprehensive metabolic panel extends the BMP to include liver function tests. Elevated transaminases, alkaline phosphatase, or bilirubin require correlation with hepatic and biliary disease.",
        reasoning_framework="""
1. Review AST, ALT for hepatocellular injury; ALT is more liver-specific (Giannini EG et al., 2005).
2. Alkaline phosphatase elevation suggests cholestasis or bone disease; check GGT to confirm hepatic origin.
3. Elevated total and direct bilirubin may indicate hemolysis, hepatocellular dysfunction, or biliary obstruction.
4. Low albumin reflects chronic liver disease, malnutrition, or nephrotic syndrome.
5. Consider acute vs. chronic patterns; acute hepatitis shows marked transaminase elevation.
6. Correlate with clinical findings (jaundice, pruritus, RUQ pain).
7. Review medications and toxins (acetaminophen, statins).
8. Reference: Giannini EG, Testa R, Savarino V. Liver enzyme alteration: a guide for clinicians. CMAJ. 2005.
9. Reference: AASLD Guidelines for the Diagnosis and Management of Liver Disease.
        """,
        key_factors=[
            "Transaminase levels",
            "Alkaline phosphatase",
            "Bilirubin fractions",
            "Albumin concentration",
            "Clinical context"
        ],
        primary_authority=[
            "Giannini EG, Testa R, Savarino V. CMAJ. 2005.",
            "AASLD Guidelines.",
            "UpToDate: Approach to abnormal liver biochemical and function tests."
        ],
        burden_holder="Interpreting Clinician",
        adversary_position="Assuming all enzyme elevations are hepatic in origin.",
        counter_arguments=[
            "Muscle injury can raise AST/ALT.",
            "Alkaline phosphatase is not liver-specific.",
            "Gilbert syndrome causes benign hyperbilirubinemia.",
            "Low albumin may be non-hepatic.",
            "Drug-induced liver injury must be considered."
        ],
        resolution_strategy="Integrate laboratory and clinical findings; consider imaging or biopsy if diagnosis unclear.",
        entity_scope="Patient serum chemistry",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Giannini EG et al., CMAJ, 2005.",
            "AASLD Guidelines."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.METABOLIC_PANEL
    )
    # Cardiac Biomarkers: Troponin, BNP, CK-MB
    DOCTRINE_CACHE["CARDIAC_01"] = DoctrineBlock(
        doctrine_id="CARDIAC_01",
        topic="Cardiac Biomarkers Interpretation",
        keywords=["troponin", "BNP", "CK-MB", "myocardial infarction", "heart failure", "acute coronary syndrome"],
        conclusion_template="Cardiac biomarkers are essential for diagnosing acute coronary syndromes and heart failure. Troponin is the preferred marker for myocardial injury, while BNP reflects cardiac wall stress.",
        reasoning_framework="""
1. Troponin (I or T) is highly sensitive and specific for myocardial injury; serial measurements improve diagnostic accuracy (Thygesen K et al., 2018).
2. Elevation above the 99th percentile upper reference limit is diagnostic for myocardial infarction in the appropriate clinical context.
3. CK-MB is less specific but may be useful if troponin is unavailable.
4. BNP and NT-proBNP are elevated in heart failure but may be increased in renal failure, pulmonary embolism, or sepsis.
5. Troponin can be elevated in non-ischemic conditions (myocarditis, renal failure, sepsis).
6. Always interpret in conjunction with ECG and clinical findings.
7. Serial changes (rise/fall) are more informative than isolated values.
8. Reference: Thygesen K, Alpert JS, Jaffe AS, et al. Fourth Universal Definition of Myocardial Infarction. Circulation. 2018.
9. Reference: Januzzi JL, McGill DA, et al. Natriuretic Peptide Testing for Heart Failure. J Am Coll Cardiol. 2019.
        """,
        key_factors=[
            "Troponin kinetics",
            "BNP/NT-proBNP value",
            "Clinical presentation",
            "Renal function",
            "ECG findings"
        ],
        primary_authority=[
            "Thygesen K, Alpert JS, Jaffe AS, et al. Circulation. 2018.",
            "Januzzi JL, McGill DA, et al. J Am Coll Cardiol. 2019.",
            "UpToDate: Cardiac biomarkers for detection of myocardial injury."
        ],
        burden_holder="Ordering Physician",
        adversary_position="Assuming all troponin elevations are due to MI.",
        counter_arguments=[
            "Troponin can be elevated in non-cardiac conditions.",
            "Renal failure increases BNP/NT-proBNP.",
            "CK-MB is less specific than troponin.",
            "Timing of sampling affects interpretation.",
            "Assay interference may cause false positives."
        ],
        resolution_strategy="Use serial measurements and clinical correlation for diagnosis.",
        entity_scope="Patient serum biomarkers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Thygesen K et al., Circulation, 2018.",
            "Januzzi JL et al., J Am Coll Cardiol, 2019."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.CARDIAC_BIOMARKERS
    )
    # Thyroid Function Tests: TSH, Free T4, T3
    DOCTRINE_CACHE["THYROID_01"] = DoctrineBlock(
        doctrine_id="THYROID_01",
        topic="Thyroid Function Tests Interpretation",
        keywords=["TSH", "free T4", "T3", "hypothyroidism", "hyperthyroidism", "subclinical"],
        conclusion_template="Thyroid function tests assess for hypo- and hyperthyroidism. TSH is the most sensitive marker; free T4 and T3 clarify the functional status.",
        reasoning_framework="""
1. TSH is the initial test; elevated TSH with low free T4 indicates primary hypothyroidism (Garber JR et al., 2012).
2. Suppressed TSH with high free T4/T3 suggests hyperthyroidism.
3. Subclinical hypothyroidism: elevated TSH, normal free T4.
4. Subclinical hyperthyroidism: low TSH, normal free T4/T3.
5. Non-thyroidal illness and medications (amiodarone, steroids) can alter results.
6. T3 toxicosis: low TSH, normal free T4, high T3.
7. Central (secondary) hypothyroidism: low/normal TSH, low free T4.
8. Reference: Garber JR, Cobin RH, Gharib H, et al. Clinical Practice Guidelines for Hypothyroidism. Endocr Pract. 2012.
9. Reference: Ross DS, Burch HB, Cooper DS, et al. 2016 American Thyroid Association Guidelines.
        """,
        key_factors=[
            "TSH value",
            "Free T4 and T3",
            "Clinical symptoms",
            "Medication effects",
            "Pituitary status"
        ],
        primary_authority=[
            "Garber JR, Cobin RH, Gharib H, et al. Endocr Pract. 2012.",
            "Ross DS, Burch HB, Cooper DS, et al. Thyroid. 2016.",
            "UpToDate: Interpretation of thyroid function tests."
        ],
        burden_holder="Ordering Clinician",
        adversary_position="Misinterpretation due to non-thyroidal illness.",
        counter_arguments=[
            "Acute illness can suppress TSH transiently.",
            "Medications may alter thyroid function tests.",
            "Pituitary disease can cause central hypothyroidism.",
            "Reference ranges differ by assay.",
            "Pregnancy alters thyroid physiology."
        ],
        resolution_strategy="Repeat testing after recovery from illness; consider clinical context.",
        entity_scope="Patient endocrine status",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Garber JR et al., Endocr Pract, 2012.",
            "Ross DS et al., Thyroid, 2016."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.THYROID_FUNCTION
    )
    # Lipid Panel
    DOCTRINE_CACHE["LIPID_01"] = DoctrineBlock(
        doctrine_id="LIPID_01",
        topic="Lipid Panel Interpretation",
        keywords=["lipid panel", "cholesterol", "LDL", "HDL", "triglycerides", "cardiovascular risk"],
        conclusion_template="Lipid panel assesses cardiovascular risk. Elevated LDL is atherogenic; high HDL is protective. Triglycerides are a risk factor for pancreatitis.",
        reasoning_framework="""
1. Review total cholesterol, LDL, HDL, and triglycerides (Grundy SM et al., 2018).
2. Elevated LDL is the primary target for therapy; calculate non-HDL cholesterol if triglycerides >400 mg/dL.
3. Low HDL is an independent risk factor for ASCVD.
4. High triglycerides (>500 mg/dL) increase risk for pancreatitis.
5. Secondary causes (hypothyroidism, nephrotic syndrome, diabetes, medications) must be excluded.
6. Fasting is preferred but non-fasting samples are acceptable for screening.
7. Reference: Grundy SM, Stone NJ, Bailey AL, et al. 2018 AHA/ACC Cholesterol Guideline. J Am Coll Cardiol. 2019.
8. Reference: Catapano AL, Graham I, De Backer G, et al. 2016 ESC/EAS Guidelines for the Management of Dyslipidaemias.
        """,
        key_factors=[
            "LDL cholesterol",
            "HDL cholesterol",
            "Triglyceride level",
            "Secondary causes",
            "Fasting status"
        ],
        primary_authority=[
            "Grundy SM, Stone NJ, Bailey AL, et al. J Am Coll Cardiol. 2019.",
            "Catapano AL, Graham I, De Backer G, et al. Eur Heart J. 2016.",
            "UpToDate: Lipid management in adults."
        ],
        burden_holder="Ordering Physician",
        adversary_position="Overemphasis on total cholesterol.",
        counter_arguments=[
            "Non-fasting samples may affect triglycerides.",
            "Genetic dyslipidemias may require specialized testing.",
            "Secondary causes must be ruled out.",
            "HDL can be affected by acute illness.",
            "LDL calculation is inaccurate at high triglycerides."
        ],
        resolution_strategy="Address secondary causes; use risk calculators for therapy decisions.",
        entity_scope="Patient lipid profile",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Grundy SM et al., J Am Coll Cardiol, 2019.",
            "Catapano AL et al., Eur Heart J, 2016."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.LIPID_PANEL
    )
    # Urinalysis: Dipstick, Microscopy, Culture
    DOCTRINE_CACHE["URINE_01"] = DoctrineBlock(
        doctrine_id="URINE_01",
        topic="Urinalysis Interpretation",
        keywords=["urinalysis", "dipstick", "microscopy", "bacteria", "pyuria", "hematuria", "proteinuria"],
        conclusion_template="Urinalysis provides rapid assessment of renal and urinary tract health. Dipstick and microscopy findings must be interpreted with clinical context.",
        reasoning_framework="""
1. Dipstick detects protein, blood, leukocyte esterase, nitrite, glucose, and ketones (Simerville JA et al., 2005).
2. Microscopy identifies cells (RBCs, WBCs), casts, crystals, and bacteria.
3. Pyuria and bacteriuria suggest urinary tract infection; confirm with culture.
4. Hematuria may be glomerular (dysmorphic RBCs, casts) or non-glomerular.
5. Proteinuria requires quantification; transient proteinuria may occur with fever or exercise.
6. False positives/negatives can occur due to contamination or technical error.
7. Reference: Simerville JA, Maxted WC, Pahira JJ. Urinalysis: A Comprehensive Review. Am Fam Physician. 2005.
8. Reference: Fogazzi GB, Garigali G. The clinical art and science of urine microscopy. Curr Opin Nephrol Hypertens. 2013.
        """,
        key_factors=[
            "Dipstick findings",
            "Microscopy results",
            "Clinical symptoms",
            "Sample collection method",
            "Culture confirmation"
        ],
        primary_authority=[
            "Simerville JA, Maxted WC, Pahira JJ. Am Fam Physician. 2005.",
            "Fogazzi GB, Garigali G. Curr Opin Nephrol Hypertens. 2013.",
            "UpToDate: Urinalysis in the diagnosis of kidney disease."
        ],
        burden_holder="Ordering Clinician",
        adversary_position="Overreliance on dipstick without microscopy.",
        counter_arguments=[
            "Contaminated samples may yield false positives.",
            "Dipstick is less sensitive for low-level proteinuria.",
            "Microscopy is operator-dependent.",
            "Transient findings may not indicate disease.",
            "Culture is required for definitive infection diagnosis."
        ],
        resolution_strategy="Correlate findings with clinical context and confirm with culture if indicated.",
        entity_scope="Patient urine sample",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Simerville JA et al., Am Fam Physician, 2005.",
            "Fogazzi GB, Curr Opin Nephrol Hypertens, 2013."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.URINALYSIS
    )
    # Blood Gas Analysis: ABG, VBG
    DOCTRINE_CACHE["BLOODGAS_01"] = DoctrineBlock(
        doctrine_id="BLOODGAS_01",
        topic="Blood Gas Analysis",
        keywords=["ABG", "VBG", "pH", "pCO2", "pO2", "bicarbonate", "acid-base"],
        conclusion_template="Arterial and venous blood gas analysis provides information on acid-base status, ventilation, and oxygenation. Interpretation requires systematic evaluation of pH, pCO2, and HCO3.",
        reasoning_framework="""
1. Assess pH: <7.35 indicates acidemia, >7.45 alkalemia (Kraut JA, Madias NE, 2012).
2. Evaluate pCO2 and HCO3 to determine primary disorder: respiratory or metabolic.
3. Calculate expected compensatory response (Winter's formula for metabolic acidosis).
4. Anion gap calculation aids in identifying causes of metabolic acidosis.
5. Evaluate oxygenation (pO2, O2 saturation) for hypoxemia.
6. VBG can be used for pH and pCO2 estimation but not for pO2.
7. Mixed acid-base disorders are common in critically ill patients.
8. Reference: Kraut JA, Madias NE. Approach to the evaluation of acid-base disorders. UpToDate, 2022.
9. Reference: Adrogué HJ, Madias NE. Management of life-threatening acid-base disorders. N Engl J Med. 1998.
        """,
        key_factors=[
            "pH value",
            "pCO2 and HCO3",
            "Anion gap",
            "Oxygenation status",
            "Compensatory mechanisms"
        ],
        primary_authority=[
            "Kraut JA, Madias NE. UpToDate, 2022.",
            "Adrogué HJ, Madias NE. N Engl J Med. 1998.",
            "UpToDate: Arterial blood gases in clinical practice."
        ],
        burden_holder="Ordering Clinician",
        adversary_position="Misinterpretation of mixed disorders.",
        counter_arguments=[
            "VBG is not reliable for oxygenation assessment.",
            "Compensation is rarely complete.",
            "Acute vs. chronic disorders differ in compensation.",
            "Sampling errors can affect results.",
            "Clinical correlation is essential."
        ],
        resolution_strategy="Use systematic approach and clinical context for interpretation.",
        entity_scope="Patient blood gas sample",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Kraut JA, Madias NE. UpToDate, 2022.",
            "Adrogué HJ, Madias NE. N Engl J Med. 1998."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.BLOOD_GAS
    )
    # Hemoglobin A1c
    DOCTRINE_CACHE["A1C_01"] = DoctrineBlock(
        doctrine_id="A1C_01",
        topic="Hemoglobin A1c Interpretation",
        keywords=["A1c", "diabetes", "glycemic control", "chronic hyperglycemia", "monitoring"],
        conclusion_template="Hemoglobin A1c reflects average glycemia over 2-3 months. It is used for diagnosis and monitoring of diabetes mellitus.",
        reasoning_framework="""
1. A1c ≥6.5% is diagnostic for diabetes in the absence of confounding factors (ADA, 2023).
2. A1c targets are individualized based on age, comorbidities, and risk of hypoglycemia.
3. Conditions affecting red cell turnover (hemolytic anemia, recent transfusion) may yield inaccurate results.
4. A1c does not reflect acute changes in glycemia.
5. Use in conjunction with self-monitoring or continuous glucose monitoring.
6. Reference: American Diabetes Association. Standards of Medical Care in Diabetes—2023. Diabetes Care. 2023.
7. Reference: Little RR, Rohlfing CL, Sacks DB. Status of hemoglobin A1c measurement and goals for improvement. Clin Chem. 2011.
        """,
        key_factors=[
            "A1c value",
            "Red cell lifespan",
            "Comorbid conditions",
            "Glycemic targets",
            "Monitoring methods"
        ],
        primary_authority=[
            "American Diabetes Association. Diabetes Care. 2023.",
            "Little RR, Rohlfing CL, Sacks DB. Clin Chem. 2011.",
            "UpToDate: Hemoglobin A1c measurement in diabetes."
        ],
        burden_holder="Ordering Clinician",
        adversary_position="Relying solely on A1c for glycemic assessment.",
        counter_arguments=[
            "A1c is unreliable in hemoglobinopathies.",
            "Acute illness may affect A1c accuracy.",
            "Recent transfusion alters results.",
            "Ethnic differences in glycation rates.",
            "A1c does not reflect glycemic variability."
        ],
        resolution_strategy="Use alternative measures if A1c is unreliable; combine with glucose monitoring.",
        entity_scope="Patient glycemic status",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "ADA, Diabetes Care, 2023.",
            "Little RR et al., Clin Chem, 2011."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.HEMOGLOBIN_A1C
    )
    # Blood Culture Identification and Sensitivity
    DOCTRINE_CACHE["BLOOD_CULTURE_01"] = DoctrineBlock(
        doctrine_id="BLOOD_CULTURE_01",
        topic="Blood Culture Interpretation",
        keywords=["blood culture", "bacteremia", "contamination", "sensitivity", "antibiotic susceptibility"],
        conclusion_template="Blood cultures are critical for diagnosing bacteremia. Interpretation requires distinguishing true pathogens from contaminants and integrating susceptibility results for therapy.",
        reasoning_framework="""
1. Positive blood cultures must be evaluated for clinical significance (Mermel LA et al., 2009).
2. Common contaminants: coagulase-negative staphylococci, Corynebacterium spp., Bacillus spp.
3. Multiple positive sets with the same organism increase likelihood of true bacteremia.
4. Susceptibility testing guides antibiotic selection; consider local resistance patterns.
5. Time to positivity may indicate organism load and virulence.
6. Repeat cultures may be needed to document clearance.
7. Reference: Mermel LA, Allon M, Bouza E, et al. Clinical practice guidelines for the diagnosis and management of intravascular catheter-related infection. Clin Infect Dis. 2009.
8. Reference: Weinstein MP. Blood culture contamination: persisting problems and partial progress. J Clin Microbiol. 2003.
        """,
        key_factors=[
            "Organism identified",
            "Number of positive sets",
            "Time to positivity",
            "Susceptibility results",
            "Clinical context"
        ],
        primary_authority=[
            "Mermel LA et al. Clin Infect Dis. 2009.",
            "Weinstein MP. J Clin Microbiol. 2003.",
            "UpToDate: Interpretation of blood cultures."
        ],
        burden_holder="Ordering Clinician",
        adversary_position="Treating contaminants as true infection.",
        counter_arguments=[
            "Single positive set may represent contamination.",
            "Skin flora are common contaminants.",
            "Prior antibiotics may yield false negatives.",
            "Time to positivity is not absolute.",
            "Immunosuppressed patients may have atypical presentations."
        ],
        resolution_strategy="Correlate with clinical findings and repeat cultures if needed.",
        entity_scope="Patient blood sample",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Mermel LA et al., Clin Infect Dis, 2009.",
            "Weinstein MP, J Clin Microbiol, 2003."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.BLOOD_CULTURE
    )
    # CSF Analysis
    DOCTRINE_CACHE["CSF_01"] = DoctrineBlock(
        doctrine_id="CSF_01",
        topic="CSF Analysis",
        keywords=["CSF", "cell count", "protein", "glucose", "meningitis", "encephalitis", "subarachnoid hemorrhage"],
        conclusion_template="CSF analysis is vital for diagnosing CNS infections and hemorrhage. Interpretation requires integration of cell count, protein, glucose, and microbiology.",
        reasoning_framework="""
1. Elevated WBCs suggest infection; neutrophilic predominance indicates bacterial, lymphocytic viral or fungal (Tunkel AR et al., 2017).
2. High protein and low glucose are typical of bacterial/fungal meningitis.
3. Xanthochromia suggests subarachnoid hemorrhage.
4. Compare CSF glucose to serum glucose; <40 mg/dL or <2/3 serum is abnormal.
5. Gram stain and culture are essential for pathogen identification.
6. PCR may be required for viral etiologies.
7. Opening pressure provides additional diagnostic information.
8. Reference: Tunkel AR, Glaser CA, Bloch KC, et al. The management of encephalitis: clinical practice guidelines. Clin Infect Dis. 2008.
9. Reference: UpToDate: Cerebrospinal fluid findings in central nervous system infections.
        """,
        key_factors=[
            "CSF WBC count and differential",
            "Protein and glucose levels",
            "Microbiology results",
            "Opening pressure",
            "Clinical presentation"
        ],
        primary_authority=[
            "Tunkel AR et al. Clin Infect Dis. 2008.",
            "UpToDate: CSF findings in CNS infections.",
            "CDC: CSF analysis guidelines."
        ],
        burden_holder="Ordering Clinician",
        adversary_position="Overinterpretation of mild abnormalities.",
        counter_arguments=[
            "Traumatic tap can elevate RBCs and protein.",
            "Prior antibiotics may alter findings.",
            "Viral infections may have normal glucose.",
            "Xanthochromia may be delayed.",
            "PCR is required for some pathogens."
        ],
        resolution_strategy="Integrate clinical, laboratory, and imaging findings.",
        entity_scope="Patient CSF sample",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Tunkel AR et al., Clin Infect Dis, 2008.",
            "UpToDate: CSF findings in CNS infections."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.CSF_ANALYSIS
    )
    # Tumor Markers
    DOCTRINE_CACHE["TUMOR_01"] = DoctrineBlock(
        doctrine_id="TUMOR_01",
        topic="Tumor Markers Interpretation",
        keywords=["tumor markers", "PSA", "CEA", "CA-125", "AFP", "cancer diagnosis", "monitoring"],
        conclusion_template="Tumor markers are adjuncts for diagnosis and monitoring of malignancy. They lack specificity and should not be used for screening in asymptomatic individuals.",
        reasoning_framework="""
1. PSA is used for prostate cancer monitoring but can be elevated in benign conditions (NCCN, 2022).
2. CEA is elevated in colorectal and other cancers but also in smokers and benign disease.
3. CA-125 is useful for ovarian cancer monitoring but is non-specific.
4. AFP is elevated in hepatocellular carcinoma and germ cell tumors.
5. Tumor marker trends are more informative than isolated values.
6. Reference: National Comprehensive Cancer Network (NCCN) Guidelines: Prostate Cancer, 2022.
7. Reference: Duffy MJ. Tumor markers in clinical practice: a review focusing on common solid cancers. Med Princ Pract. 2013.
        """,
        key_factors=[
            "Type of marker",
            "Clinical context",
            "Serial trends",
            "Benign causes of elevation",
            "Assay specificity"
        ],
        primary_authority=[
            "NCCN Guidelines: Prostate Cancer, 2022.",
            "Duffy MJ. Med Princ Pract. 2013.",
            "UpToDate: Tumor markers in cancer diagnosis and monitoring."
        ],
        burden_holder="Ordering Physician",
        adversary_position="Using tumor markers for screening.",
        counter_arguments=[
            "Markers lack specificity for cancer.",
            "Benign conditions can elevate markers.",
            "Screening asymptomatic patients is not recommended.",
            "Assay variability affects results.",
            "Trends are more important than single values."
        ],
        resolution_strategy="Use as adjuncts; base diagnosis on clinical and imaging findings.",
        entity_scope="Patient serum markers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "NCCN Guidelines: Prostate Cancer, 2022.",
            "Duffy MJ, Med Princ Pract, 2013."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.TUMOR_MARKERS
    )
    # Iron Studies
    DOCTRINE_CACHE["IRON_01"] = DoctrineBlock(
        doctrine_id="IRON_01",
        topic="Iron Studies Interpretation",
        keywords=["iron studies", "ferritin", "TIBC", "transferrin saturation", "iron deficiency", "anemia"],
        conclusion_template="Iron studies differentiate iron deficiency anemia from anemia of chronic disease. Ferritin is the most sensitive marker but is also an acute phase reactant.",
        reasoning_framework="""
1. Low ferritin (<30 ng/mL) is diagnostic for iron deficiency unless confounded by inflammation (Guyatt GH et al., 1992).
2. High TIBC and low transferrin saturation support iron deficiency.
3. Anemia of chronic disease: low serum iron, low TIBC, normal/increased ferritin.
4. Elevated ferritin may reflect inflammation, liver disease, or hemochromatosis.
5. Transferrin saturation <15% is highly suggestive of iron deficiency.
6. Reference: Guyatt GH, Oxman AD, Ali M, et al. Laboratory diagnosis of iron-deficiency anemia: an overview. J Gen Intern Med. 1992.
7. Reference: Camaschella C. Iron-deficiency anemia. N Engl J Med. 2015.
        """,
        key_factors=[
            "Ferritin value",
            "TIBC",
            "Transferrin saturation",
            "Inflammatory status",
            "Clinical context"
        ],
        primary_authority=[
            "Guyatt GH et al. J Gen Intern Med. 1992.",
            "Camaschella C. N Engl J Med. 2015.",
            "UpToDate: Diagnosis and evaluation of iron deficiency anemia."
        ],
        burden_holder="Ordering Clinician",
        adversary_position="Relying on ferritin alone in inflammatory states.",
        counter_arguments=[
            "Ferritin is an acute phase reactant.",
            "Liver disease can elevate ferritin.",
            "Transferrin saturation is affected by fasting status.",
            "TIBC may be low in chronic disease.",
            "Reference ranges vary by laboratory."
        ],
        resolution_strategy="Interpret in context of inflammation and clinical findings.",
        entity_scope="Patient iron status",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Guyatt GH et al., J Gen Intern Med, 1992.",
            "Camaschella C, N Engl J Med, 2015."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.IRON_STUDIES
    )
    # Autoimmune Panel
    DOCTRINE_CACHE["AUTOIMMUNE_01"] = DoctrineBlock(
        doctrine_id="AUTOIMMUNE_01",
        topic="Autoimmune Panel Interpretation",
        keywords=["autoimmune panel", "ANA", "anti-dsDNA", "RF", "CCP", "lupus", "rheumatoid arthritis"],
        conclusion_template="Autoimmune panels aid in diagnosing systemic autoimmune diseases. Positive results must be interpreted in clinical context due to limited specificity.",
        reasoning_framework="""
1. ANA is sensitive but not specific for SLE; low titers are common in healthy individuals (Pisetsky DS et al., 2011).
2. Anti-dsDNA is highly specific for SLE; high titers correlate with disease activity.
3. RF is sensitive but not specific for RA; anti-CCP is more specific.
4. False positives occur in infections, aging, and other autoimmune diseases.
5. Clinical correlation is essential; do not diagnose based on serology alone.
6. Reference: Pisetsky DS, Spencer DM, Lipsky PE, Rovin BH. ANA testing in rheumatic diseases. Arthritis Res Ther. 2011.
7. Reference: UpToDate: Overview of autoantibodies in systemic autoimmune disease.
        """,
        key_factors=[
            "ANA titer and pattern",
            "Anti-dsDNA level",
            "RF and anti-CCP",
            "Clinical features",
            "Other causes of positivity"
        ],
        primary_authority=[
            "Pisetsky DS et al. Arthritis Res Ther. 2011.",
            "UpToDate: Autoantibodies in systemic autoimmune disease.",
            "ACR Guidelines: Rheumatoid Arthritis, 2021."
        ],
        burden_holder="Ordering Clinician",
        adversary_position="Diagnosing autoimmune disease based on serology alone.",
        counter_arguments=[
            "Low-titer ANA is common in healthy people.",
            "RF is not specific for RA.",
            "Viral infections can cause transient positivity.",
            "Assay variability affects results.",
            "Clinical features are paramount."
        ],
        resolution_strategy="Integrate serology with clinical and imaging findings.",
        entity_scope="Patient autoimmune status",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Pisetsky DS et al., Arthritis Res Ther, 2011.",
            "ACR Guidelines: Rheumatoid Arthritis, 2021."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.AUTOIMMUNE_PANEL
    )
    # Hepatitis Serology
    DOCTRINE_CACHE["HEP_SEROLOGY_01"] = DoctrineBlock(
        doctrine_id="HEP_SEROLOGY_01",
        topic="Hepatitis Serology Interpretation",
        keywords=["hepatitis", "HBsAg", "anti-HBs", "anti-HCV", "serology", "infection", "immunity"],
        conclusion_template="Hepatitis serology differentiates acute, chronic, and resolved infection. Interpretation requires understanding of marker kinetics and combinations.",
        reasoning_framework="""
1. HBsAg indicates active hepatitis B infection; anti-HBs indicates immunity (CDC, 2023).
2. Anti-HBc IgM suggests acute infection; total anti-HBc persists for life.
3. Anti-HCV indicates exposure; confirm with HCV RNA for active infection.
4. Window period: anti-HBc may be the only positive marker.
5. Vaccination yields isolated anti-HBs positivity.
6. Reference: CDC. Interpretation of Hepatitis B Serologic Test Results. 2023.
7. Reference: UpToDate: Hepatitis B and C serology.
        """,
        key_factors=[
            "HBsAg status",
            "Anti-HBs and anti-HBc",
            "Anti-HCV and HCV RNA",
            "Vaccination history",
            "Clinical context"
        ],
        primary_authority=[
            "CDC. Hepatitis B Serology, 2023.",
            "UpToDate: Hepatitis B and C serology.",
            "WHO Guidelines: Hepatitis B and C Testing, 2017."
        ],
        burden_holder="Ordering Clinician",
        adversary_position="Misinterpreting window period or isolated markers.",
        counter_arguments=[
            "False positives can occur in low prevalence settings.",
            "Acute infection may lack anti-HBs.",
            "Immunosuppressed patients may not mount antibody response.",
            "Assay cross-reactivity.",
            "Vaccination status affects interpretation."
        ],
        resolution_strategy="Use marker combinations and confirmatory testing.",
        entity_scope="Patient viral serology",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "CDC, Hepatitis B Serology, 2023.",
            "WHO Guidelines: Hepatitis B and C Testing, 2017."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.HEPATITIS_SEROLOGY
    )
    # HIV Testing Algorithm
    DOCTRINE_CACHE["HIV_01"] = DoctrineBlock(
        doctrine_id="HIV_01",
        topic="HIV Testing Algorithm",
        keywords=["HIV", "4th generation", "antigen", "antibody", "algorithm", "window period"],
        conclusion_template="The 4th generation HIV test detects both antigen and antibody, reducing the window period. Reactive results require confirmatory testing.",
        reasoning_framework="""
1. 4th generation assays detect p24 antigen and HIV-1/2 antibodies (CDC, 2021).
2. Window period is ~2 weeks; earlier than antibody-only tests.
3. Reactive screening test is followed by a differentiation assay.
4. Indeterminate results may require nucleic acid testing (NAT).
5. False positives are rare but possible; always confirm before diagnosis.
6. Reference: CDC. Laboratory Testing for the Diagnosis of HIV Infection: Updated Recommendations. 2021.
7. Reference: UpToDate: Acute and early HIV infection: Diagnostic testing.
        """,
        key_factors=[
            "Screening assay result",
            "Confirmatory testing",
            "Window period",
            "Clinical risk factors",
            "NAT availability"
        ],
        primary_authority=[
            "CDC. HIV Testing Recommendations, 2021.",
            "UpToDate: Acute and early HIV infection.",
            "WHO: Consolidated guidelines on HIV testing services, 2019."
        ],
        burden_holder="Ordering Clinician",
        adversary_position="Diagnosing HIV on screening test alone.",
        counter_arguments=[
            "False positives in low prevalence populations.",
            "Recent exposure may yield negative result.",
            "Indeterminate results require further testing.",
            "Assay sensitivity varies.",
            "Window period must be considered."
        ],
        resolution_strategy="Follow algorithm and confirmatory testing before diagnosis.",
        entity_scope="Patient HIV status",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "CDC, HIV Testing Recommendations, 2021.",
            "WHO: HIV testing guidelines, 2019."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.HIV_TESTING
    )
    # Drug Screening
    DOCTRINE_CACHE["DRUG_SCREEN_01"] = DoctrineBlock(
        doctrine_id="DRUG_SCREEN_01",
        topic="Drug Screening Interpretation",
        keywords=["drug screen", "immunoassay", "GC-MS", "false positive", "confirmation", "toxicology"],
        conclusion_template="Drug screening by immunoassay is rapid but prone to false positives. Confirmation by GC-MS is required for definitive identification.",
        reasoning_framework="""
1. Immunoassays detect drug classes but may cross-react with structurally similar compounds (Jannetto PJ et al., 2018).
2. False positives: dextromethorphan for PCP, poppy seeds for opiates, sertraline for benzodiazepines.
3. GC-MS or LC-MS/MS provides definitive identification and quantification.
4. Timing of ingestion, metabolism, and specimen type affect detection.
5. Clinical context and medication history are essential for interpretation.
6. Reference: Jannetto PJ, Helander A, Garg U, et al. The role of mass spectrometry and chromatography in clinical laboratories. Clin Chem Lab Med. 2018.
7. Reference: UpToDate: Urine drug testing: Practical guide for clinicians.
        """,
        key_factors=[
            "Immunoassay result",
            "Confirmation by GC-MS",
            "Medication history",
            "Timing of exposure",
            "Cross-reactivity"
        ],
        primary_authority=[
            "Jannetto PJ et al. Clin Chem Lab Med. 2018.",
            "UpToDate: Urine drug testing.",
            "SAMHSA: Urine Drug Testing Guidelines, 2017."
        ],
        burden_holder="Ordering Clinician",
        adversary_position="Acting on immunoassay results alone.",
        counter_arguments=[
            "False positives are common.",
            "Recent ingestion may not be detected.",
            "Metabolites may persist after drug effect.",
            "Specimen adulteration is possible.",
            "Assay limitations must be understood."
        ],
        resolution_strategy="Confirm positive screens with GC-MS and review medication history.",
        entity_scope="Patient toxicology status",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Jannetto PJ et al., Clin Chem Lab Med, 2018.",
            "SAMHSA: Urine Drug Testing Guidelines, 2017."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.DRUG_SCREENING
    )
    # Molecular Diagnostics: PCR, FISH, NGS
    DOCTRINE_CACHE["MOLECULAR_01"] = DoctrineBlock(
        doctrine_id="MOLECULAR_01",
        topic="Molecular Diagnostics Interpretation",
        keywords=["molecular diagnostics", "PCR", "FISH", "NGS", "mutation", "pathogen detection"],
        conclusion_template="Molecular diagnostics enable sensitive detection of pathogens and genetic alterations. Results must be interpreted in clinical context due to potential for contamination and incidental findings.",
        reasoning_framework="""
1. PCR amplifies specific nucleic acid sequences; highly sensitive for pathogen detection (Mackay IM, Arden KE, Nitsche A, 2002).
2. FISH identifies chromosomal abnormalities in cancer and genetic disease.
3. NGS allows broad mutation detection but may yield variants of uncertain significance.
4. False positives may result from contamination; false negatives from inhibitors or low target load.
5. Clinical correlation and confirmatory testing are often required.
6. Reference: Mackay IM, Arden KE, Nitsche A. Real-time PCR in virology. Nucleic Acids Res. 2002.
7. Reference: Rehm HL, et al. ACMG clinical laboratory standards for next-generation sequencing. Genet Med. 2013.
        """,
        key_factors=[
            "Assay type (PCR, FISH, NGS)",
            "Target detected",
            "Clinical context",
            "Contamination risk",
            "Variant interpretation"
        ],
        primary_authority=[
            "Mackay IM, Arden KE, Nitsche A. Nucleic Acids Res. 2002.",
            "Rehm HL et al. Genet Med. 2013.",
            "UpToDate: Principles of molecular diagnostics."
        ],
        burden_holder="Ordering Clinician",
        adversary_position="Overinterpretation of incidental findings.",
        counter_arguments=[
            "Variants of uncertain significance are common.",
            "Contamination can yield false positives.",
            "Assay sensitivity varies by target.",
            "Negative result does not exclude disease.",
            "Clinical correlation is required."
        ],
        resolution_strategy="Integrate molecular results with clinical and other laboratory findings.",
        entity_scope="Patient molecular status",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Mackay IM et al., Nucleic Acids Res, 2002.",
            "Rehm HL et al., Genet Med, 2013."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.MOLECULAR_DIAGNOSTICS
    )
    # Flow Cytometry
    DOCTRINE_CACHE["FLOW_01"] = DoctrineBlock(
        doctrine_id="FLOW_01",
        topic="Flow Cytometry Interpretation",
        keywords=["flow cytometry", "immunophenotyping", "lymphoma", "leukemia", "blasts", "cell markers"],
        conclusion_template="Flow cytometry enables immunophenotyping of hematologic malignancies. Interpretation requires integration of marker expression, clinical, and morphologic findings.",
        reasoning_framework="""
1. Flow cytometry identifies cell populations based on surface and cytoplasmic markers (Craig FE, Foon KA, 2008).
2. Aberrant expression patterns suggest malignancy (e.g., CD19+CD5+ in CLL).
3. Blasts are characterized by CD34, TdT, and other markers.
4. Results must be correlated with morphology and clinical presentation.
5. Minimal residual disease detection requires highly sensitive panels.
6. Reference: Craig FE, Foon KA. Flow cytometric immunophenotyping for hematologic neoplasms. Blood. 2008.
7. Reference: Swerdlow SH, Campo E, Harris NL, et al. WHO Classification of Tumours of Haematopoietic and Lymphoid Tissues, 2017.
        """,
        key_factors=[
            "Marker expression profile",
            "Cell population distribution",
            "Morphologic findings",
            "Clinical context",
            "Panel sensitivity"
        ],
        primary_authority=[
            "Craig FE, Foon KA. Blood. 2008.",
            "Swerdlow SH et al. WHO Classification, 2017.",
            "UpToDate: Flow cytometry in hematologic malignancies."
        ],
        burden_holder="Interpreting Pathologist",
        adversary_position="Overcalling minor aberrancies as malignant.",
        counter_arguments=[
            "Reactive lymphocytosis can mimic malignancy.",
            "Marker expression may overlap in benign and malignant cells.",
            "Technical artifacts affect results.",
            "Panel selection impacts sensitivity.",
            "Clinical correlation is essential."
        ],
        resolution_strategy="Correlate flow cytometry with morphology and clinical findings.",
        entity_scope="Patient hematologic status",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Craig FE, Foon KA, Blood, 2008.",
            "Swerdlow SH et al., WHO, 2017."
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.FLOW_CYTOMETRY
    )
    # Add more doctrine blocks as needed for coverage (minimum 30).
_init_doctrines()

# =========================
# AUTHORITY HARDENING
# =========================

AUTHORITY_WEIGHTS = {
    "CDC": 1.0,
    "WHO": 1.0,
    "AASLD": 0.9,
    "ADA": 0.95,
    "NCCN": 0.95,
    "KDIGO": 0.95,
    "AHA": 0.9,
    "ACR": 0.9,
    "UpToDate": 0.8,
    "Textbook": 0.7,
    "Journal": 0.85
}

def resolve_authority_conflicts(authorities: List[str]) -> List[str]:
    weighted = []
    for auth in authorities:
        for k, w in AUTHORITY_WEIGHTS.items():
            if k in auth:
                weighted.append((w, auth))
                break
        else:
            weighted.append((0.5, auth))
    weighted.sort(reverse=True)
    return [a for _, a in weighted]

# =========================
# SEMANTIC NORMALIZATION
# =========================

SEMANTIC_MAP = {
    "CBC": ["complete blood count", "hemogram"],
    "WBC": ["white blood cell", "leukocyte"],
    "RBC": ["red blood cell", "erythrocyte"],
    "PLT": ["platelet", "thrombocyte"],
    "PT": ["prothrombin time"],
    "INR": ["international normalized ratio"],
    "PTT": ["partial thromboplastin time", "aPTT"],
    "BMP": ["basic metabolic panel"],
    "CMP": ["comprehensive metabolic panel"],
    "AST": ["aspartate aminotransferase"],
    "ALT": ["alanine aminotransferase"],
    "BNP": ["B-type natriuretic peptide"],
    "CK-MB": ["creatine kinase-MB"],
    "TSH": ["thyroid stimulating hormone"],
    "A1c": ["hemoglobin A1c", "glycated hemoglobin"],
    "ANA": ["antinuclear antibody"],
    "RF": ["rheumatoid factor"],
    "CCP": ["cyclic citrullinated peptide"],
    "HBsAg": ["hepatitis B surface antigen"],
    "anti-HBs": ["hepatitis B surface antibody"],
    "anti-HCV": ["hepatitis C antibody"],
    "PCR": ["polymerase chain reaction"],
    "FISH": ["fluorescence in situ hybridization"],
    "NGS": ["next generation sequencing"],
    "VBG": ["venous blood gas"],
    "ABG": ["arterial blood gas"],
    "TIBC": ["total iron binding capacity"],
    "AFP": ["alpha-fetoprotein"],
    "CEA": ["carcinoembryonic antigen"],
    "CA-125": ["cancer antigen 125"]
}

def normalize_term(term: str) -> str:
    for k, vals in SEMANTIC_MAP.items():
        if term.lower() == k.lower() or term.lower() in [v.lower() for v in vals]:
            return k
    return term

# =========================
# EPISTEMIC GUARDRAILS
# =========================

BANNED_PHRASES = [
    "always", "never", "prove", "guarantee", "certain", "no doubt", "must", "cannot be", "definitely", "without exception"
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "[EPISTEMIC_FILTERED]")
    return text

# =========================
# FACT FRAGILITY SCORING
# =========================

def score_fact_fragility(fact: str) -> Dict[str, float]:
    verifiability = 1.0 if any(auth in fact for auth in AUTHORITY_WEIGHTS) else 0.7
    recharacterization_risk = 0.2 if "may" in fact or "can" in fact else 0.5
    testimony_dependence = 0.3 if "UpToDate" in fact or "Textbook" in fact else 0.7
    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence
    }

# =========================
# THREE LAYER RESPONSE
# =========================

def doctrine_layer(query: QueryRequest) -> Tuple[Optional[DoctrineBlock], float]:
    # Exact match by keyword/topic
    for block in DOCTRINE_CACHE.values():
        for kw in block.keywords:
            if kw.lower() in query.scenario.lower():
                return block, 0.99
        if block.topic.lower() in query.scenario.lower():
            return block, 0.97
    return None, 0.0

def semantic_layer(query: QueryRequest) -> Tuple[Optional[DoctrineBlock], float]:
    # Semantic normalization and fuzzy matching
    scenario_norm = [normalize_term(w) for w in query.scenario.split()]
    for block in DOCTRINE_CACHE.values():
        block_norm = [normalize_term(w) for w in block.keywords]
        if any(w in block_norm for w in scenario_norm):
            return block, 0.92
    return None, 0.0

def deep_analysis_layer(query: QueryRequest) -> Tuple[Optional[DoctrineBlock], float]:
    # Multi-doctrine decomposition and DAG analysis
    best_block = None
    best_score = 0.0
    for block in DOCTRINE_CACHE.values():
        score = 0
        for kw in block.keywords:
            if kw.lower() in query.scenario.lower():
                score += 1
        if score > best_score:
            best_block = block
            best_score = score
    if best_block and best_score > 0:
        return best_block, 0.85 + 0.02 * min(best_score, 5)
    return None, 0.0

# =========================
# DEEP ANALYSIS
# =========================

def multi_doctrine_decomposition(query: QueryRequest) -> List[DoctrineBlock]:
    hits = []
    for block in DOCTRINE_CACHE.values():
        if any(kw.lower() in query.scenario.lower() for kw in block.keywords):
            hits.append(block)
    return hits

def issue_category_dag(blocks: List[DoctrineBlock]) -> Dict[str, List[str]]:
    dag = {}
    for block in blocks:
        dag.setdefault(block.issue_category, []).append(block.doctrine_id)
    return dag

def eight_step_resolution(blocks: List[DoctrineBlock], query: QueryRequest) -> Dict[str, Any]:
    # 1. Identify all relevant doctrines
    # 2. Map issue categories
    # 3. Evaluate authority hierarchy
    # 4. Score fact fragility
    # 5. Detect epistemic gaps
    # 6. Resolve conflicts
    # 7. Synthesize conclusion
    # 8. Assign confidence/zone
    relevant = blocks
    categories = issue_category_dag(relevant)
    authorities = []
    for b in relevant:
        authorities.extend(b.primary_authority)
    authorities = resolve_authority_conflicts(authorities)
    fragility = [score_fact_fragility(b.reasoning_framework) for b in relevant]
    epistemic_gap = len(relevant) == 0
    conflicts = []
    for i, b1 in enumerate(relevant):
        for b2 in relevant[i+1:]:
            if b1.topic == b2.topic and b1.conclusion_template != b2.conclusion_template:
                conflicts.append((b1.doctrine_id, b2.doctrine_id))
    conclusion = "; ".join(apply_epistemic_guardrails(b.conclusion_template) for b in relevant)
    confidence = min(0.99, sum(b.confidence for b in relevant) / (len(relevant) or 1))
    zone = relevant[0].confidence_zone if relevant else ConfidenceZone.DISCLOSURE
    pos_zone = relevant[0].position_zone if relevant else PositionZone.PLANNING
    return {
        "categories": categories,
        "authorities": authorities,
        "fragility": fragility,
        "epistemic_gap": epistemic_gap,
        "conflicts": conflicts,
        "conclusion": conclusion,
        "confidence": confidence,
        "confidence_zone": zone,
        "position_zone": pos_zone
    }

# =========================
# COVERAGE MAP
# =========================

def coverage_map(query: QueryRequest) -> Dict[str, Any]:
    triggered = []
    missed = []
    for block in DOCTRINE_CACHE.values():
        if any(kw.lower() in query.scenario.lower() for kw in block.keywords):
            triggered.append(block.doctrine_id)
        else:
            missed.append(block.doctrine_id)
    epistemic_gap = len(triggered) == 0
    return {
        "triggered": triggered,
        "missed": missed,
        "epistemic_gap": epistemic_gap
    }

# =========================
# DRIFT WATCHER
# =========================

DRIFT_BASELINE = {k: v.confidence for k, v in DOCTRINE_CACHE.items()}

def drift_watcher() -> Dict[str, Any]:
    drift = {}
    for k, v in DOCTRINE_CACHE.items():
        baseline = DRIFT_BASELINE.get(k, v.confidence)
        if abs(v.confidence - baseline) > 0.05:
            drift[k] = {"baseline": baseline, "current": v.confidence}
    return drift

# =========================
# AUDIT TRAIL
# =========================

AUDIT_LOG_PATH = Path(__file__).parent / "clinical_pathology_audit.jsonl"
AUDIT_LOCK = threading.Lock()

def log_audit(entry: Dict[str, Any]):
    with AUDIT_LOCK:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")

# =========================
# DETERMINISM HASH
# =========================

def determinism_hash(data: Any) -> str:
    if isinstance(data, dict):
        data_str = json.dumps(data, sort_keys=True)
    else:
        data_str = str(data)
    return hashlib.sha256(data_str.encode("utf-8")).hexdigest()

# =========================
# FASTAPI APP
# =========================

app = FastAPI(title="Clinical Pathology Engine", version="1.0", docs_url="/docs", redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup_event():
    logger.info("Clinical Pathology Engine (MED04) started.")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Clinical Pathology Engine (MED04) shutting down.")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    query_id = str(uuid.uuid4())
    start_time = datetime.utcnow()
    try:
        # Layer 1: Doctrine cache
        block, conf = doctrine_layer(request)
        doctrine_ids = []
        if block:
            doctrine_ids.append(block.doctrine_id)
        else:
            # Layer 2: Semantic
            block, conf = semantic_layer(request)
            if block:
                doctrine_ids.append(block.doctrine_id)
            else:
                # Layer 3: Deep analysis
                block, conf = deep_analysis_layer(request)
                if block:
                    doctrine_ids.append(block.doctrine_id)
        if not block:
            # Multi-doctrine deep analysis
            blocks = multi_doctrine_decomposition(request)
            analysis = eight_step_resolution(blocks, request)
            primary_conclusion = analysis["conclusion"]
            reasoning_framework = "Multi-doctrine analysis:\n" + "\n".join(
                [b.reasoning_framework for b in blocks]
            )
            key_factors = [kf for b in blocks for kf in b.key_factors]
            primary_authority = analysis["authorities"]
            counter_arguments = [ca for b in blocks for ca in b.counter_arguments]
            resolution_strategy = "; ".join(b.resolution_strategy for b in blocks)
            confidence = analysis["confidence"]
            confidence_zone = analysis["confidence_zone"]
            position_zone = analysis["position_zone"]
        else:
            primary_conclusion = apply_epistemic_guardrails(block.conclusion_template)
            reasoning_framework = apply_epistemic_guardrails(block.reasoning_framework)
            key_factors = block.key_factors
            primary_authority = resolve_authority_conflicts(block.primary_authority)
            counter_arguments = block.counter_arguments
            resolution_strategy = block.resolution_strategy
            confidence = block.confidence
            confidence_zone = block.confidence_zone
            position_zone = block.position_zone
        # Determinism hash
        resp_dict = {
            "engine_id": "MED04",
            "query_id": query_id,
            "mode": request.mode,
            "confidence": confidence,
            "confidence_zone": confidence_zone,
            "position_zone": position_zone,
            "primary_conclusion": primary_conclusion,
            "reasoning_framework": reasoning_framework,
            "key_factors": key_factors,
            "primary_authority": primary_authority,
            "counter_arguments": counter_arguments,
            "resolution_strategy": resolution_strategy
        }
        resp_dict["determinism_hash"] = determinism_hash(resp_dict)
        t1 = datetime.utcnow()
        latency = (t1 - start_time).total_seconds()
        metrics_collector.record_query(query_id, doctrine_ids, latency)
        log_audit({
            "timestamp": t1.isoformat(),
            "query_id": query_id,
            "scenario": request.scenario,
            "mode": request.mode.value,
            "confidence": resp_dict["confidence"],
            "determinism_hash": resp_dict["determinism_hash"]
        })
        return QueryResponse(**resp_dict)
    except Exception as e:
        metrics_collector.record_error(query_id, str(e))
        logger.error(f"Query error: {e}")
        raise

@app.get("/health")
async def health_endpoint():
    return {
        "status": "ok",
        "engine_id": "MED04",
        "version": "1.0.0",
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "time": datetime.utcnow().isoformat()
    }

@app.get("/metrics")
async def metrics_endpoint():
    return {
        "latency_stats": metrics_collector.get_latency_stats(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "queries_last_hour": metrics_collector.queries_last_hour(),
        "total_queries": len(metrics_collector.queries),
        "total_errors": len(metrics_collector.errors)
    }

@app.get("/coverage")
async def coverage_endpoint():
    cov = coverage_map(QueryRequest(scenario="", mode=ResponseMode.FAST, entity_type="", complexity=1))
    return cov

@app.get("/drift")
async def drift_endpoint():
    return drift_watcher()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8504)
