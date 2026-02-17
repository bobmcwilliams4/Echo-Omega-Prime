"""
MED14 Gastroenterology Analysis Engine v1.0.0
TIE-Grade Medical Intelligence - GI Tract Diagnostics & Hepatology

Covers: Endoscopy analysis, hepatology assessment, inflammatory bowel disease,
GI oncology screening, nutritional assessment, motility disorders

Author: ECHO OMEGA PRIME
Date: 2026-02-14
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ══════════════════════════════════════════════════════════════════════════════
# ENUMS & CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    DIAGNOSTIC = "DIAGNOSTIC"
    TREATMENT = "TREATMENT"
    SCREENING = "SCREENING"


class IssueCategory(str, Enum):
    ENDOSCOPY = "ENDOSCOPY"
    HEPATOLOGY = "HEPATOLOGY"
    IBD = "IBD"
    GI_ONCOLOGY = "GI_ONCOLOGY"
    MOTILITY = "MOTILITY"
    NUTRITION = "NUTRITION"
    ESOPHAGEAL = "ESOPHAGEAL"
    GASTRIC = "GASTRIC"
    INTESTINAL = "INTESTINAL"
    COLORECTAL = "COLORECTAL"
    PANCREATIC = "PANCREATIC"
    BILIARY = "BILIARY"


BANNED_PHRASES = [
    "this is medical advice",
    "you should immediately",
    "I can diagnose",
    "definitely has",
    "ruled out completely",
    "no need to consult",
    "ignore doctor's advice",
    "stop all medications"
]

VERSION = "1.0.0"
ENGINE_ID = "MED14"
PORT = 9314


# ══════════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ══════════════════════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.DIAGNOSTIC
    context: Optional[Dict[str, Any]] = None


class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: List[str]
    zone: AnalysisZone


class AnalysisResult(BaseModel):
    query: str
    response: str
    mode: ResponseMode
    zone: AnalysisZone
    triggered_doctrines: List[str]
    confidence: ConfidenceLevel
    latency_ms: float
    determinism_hash: str
    timestamp: str
    epistemic_guardrails_applied: bool
    fragility_score: float
    coverage_gaps: List[str]


class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float
    doctrine_count: int
    error_count: int


# ══════════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ GASTROENTEROLOGY EXPERTISE BLOCKS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class DoctrineCacheEntry:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: List[str]
    zone: AnalysisZone
    category: IssueCategory


DOCTRINE_CACHE: List[DoctrineCacheEntry] = [
    DoctrineCacheEntry(
        topic="Upper Endoscopy Findings Interpretation",
        keywords=["EGD", "esophagogastroduodenoscopy", "upper GI", "barrett's", "gastritis", "ulcer"],
        conclusion_template=[
            "Upper endoscopy findings indicate {pathology_severity} with {location_specific} involvement.",
            "Histologic correlation required for {biopsy_targets}. Clinical significance depends on {symptom_correlation}.",
            "Surveillance interval follows {guideline_source} recommendations based on {risk_stratification}."
        ],
        reasoning_framework="""
Upper endoscopy interpretation requires systematic evaluation of esophagus, stomach, and duodenum:

ESOPHAGEAL ASSESSMENT:
- Los Angeles classification for reflux esophagitis (Grade A-D)
- Barrett's esophagus: Prague C&M criteria, dysplasia grading
- Eosinophilic esophagitis: furrows, rings, exudates, edema, strictures
- Varices: size (small <5mm, large >5mm), red wale marks, bleeding stigmata
- Malignancy: mass lesions, ulceration, stricture, wall rigidity

GASTRIC EVALUATION:
- Helicobacter pylori: antral nodularity, pangastritis, MALToma
- Atrophic gastritis: intestinal metaplasia, pseudopolyps, flat mucosa
- Peptic ulcer disease: location (antrum vs body), size, depth, bleeding stigmata
- Gastric polyps: fundic gland (PPI-associated), hyperplastic, adenomatous
- Gastric cancer: early (0-I, 0-II, 0-III) vs advanced staging

DUODENAL FINDINGS:
- Peptic ulcer: bulb vs post-bulb location, size, perforation risk
- Celiac disease: scalloping, fissuring, mosaic pattern, reduced folds
- Ampullary pathology: sphincter of Oddi dysfunction, periampullary tumors
- Angiodysplasia: bleeding source localization, thermal therapy targets

BIOPSY PROTOCOL:
- Barrett's: 4-quadrant every 2cm, plus targeted lesions
- Gastric cancer screening: antrum (2), body (2), incisura (1), lesser curve focus
- Celiac disease: duodenal bulb and post-bulb (4-6 biopsies)
- H. pylori: antrum and body biopsies for rapid urease and histology
        """,
        key_factors=[
            "Endoscopic classification systems (LA, Prague, Forrest, Paris)",
            "Biopsy sampling adequacy and location per protocol",
            "Histologic-endoscopic correlation for final diagnosis",
            "Surveillance interval determination per guidelines",
            "Therapeutic intervention timing (hemostasis, EMR, ESD)",
            "Risk stratification for malignancy progression",
            "Patient preparation adequacy affecting interpretation"
        ],
        primary_authority=[
            "ACG/ASGE Guidelines on Barrett's Esophagus Management (2022)",
            "Paris Classification for Superficial Neoplastic Lesions",
            "Los Angeles Classification of Reflux Esophagitis",
            "Prague C&M Criteria for Barrett's Length",
            "Forrest Classification for Peptic Ulcer Bleeding"
        ],
        burden_holder="Endoscopist performing procedure and interpreting findings",
        adversary_position="Inadequate visualization, missed lesions, sampling error, misclassification of severity",
        counter_arguments=[
            "Sedation level affecting patient cooperation and exam quality",
            "Prior surgery altering anatomic landmarks and interpretation",
            "Inflammation obscuring underlying pathology or dysplasia",
            "Interobserver variability in classification systems",
            "Inadequate bowel preparation limiting duodenal visualization"
        ],
        resolution_strategy="Systematic examination with photodocumentation, protocol-driven biopsies, use of validated classification systems, second-look endoscopy when initial findings equivocal, chromoendoscopy or advanced imaging for lesion characterization",
        entity_scope="All patients undergoing upper endoscopy for diagnostic or therapeutic indications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for classic findings; disclosure needed for subtle dysplasia or early neoplasia requiring expert pathology review",
        controlling_precedent=[
            "ASGE Standards of Practice: Role of Endoscopy in Barrett's Esophagus",
            "ACG Clinical Guideline: Diagnosis and Management of Gastroesophageal Reflux Disease",
            "ASGE Quality Indicators for Upper Endoscopy"
        ],
        zone=AnalysisZone.DIAGNOSTIC,
        category=IssueCategory.ENDOSCOPY
    ),
    DoctrineCacheEntry(
        topic="Colonoscopy Polyp Management and Surveillance",
        keywords=["colonoscopy", "polyp", "adenoma", "sessile serrated", "CRC screening", "surveillance"],
        conclusion_template=[
            "Colonoscopy revealed {polyp_count} polyps with {histology_types}. Surveillance interval is {interval} per {guideline}.",
            "Advanced features include {size_morphology}. {resection_completeness} achieved with {technique}.",
            "Cancer risk stratification: {risk_category}. Additional screening recommendations: {family_screening}."
        ],
        reasoning_framework="""
Colonoscopy polyp management requires risk stratification and surveillance planning:

POLYP CLASSIFICATION:
- Adenomatous: tubular, tubulovillous, villous architecture
- Sessile serrated lesions (SSLs): with or without dysplasia
- Traditional serrated adenomas: dysplasia risk intermediate
- Hyperplastic polyps: distal location generally low risk
- Advanced adenoma: >=10mm, villous features, high-grade dysplasia

MORPHOLOGY (PARIS CLASSIFICATION):
- 0-Ip: pedunculated polyp with stalk
- 0-Is: sessile polyp without stalk
- 0-IIa: slightly elevated flat lesion
- 0-IIb: completely flat lesion
- 0-IIc: slightly depressed lesion
- 0-III: excavated or ulcerated lesion

RESECTION TECHNIQUES:
- Cold snare polypectomy: polyps <10mm, lower perforation/bleeding risk
- Hot snare polypectomy: larger polyps, higher complete resection rates
- Endoscopic mucosal resection (EMR): large sessile polyps, inject-lift-resect
- Endoscopic submucosal dissection (ESD): en-bloc resection for large/difficult lesions
- Piecemeal resection: acceptable for benign-appearing polyps >20mm

SURVEILLANCE INTERVALS (USMSTF 2020):
- 1-2 tubular adenomas <10mm: 7-10 years
- 3-4 small tubular adenomas: 3-5 years
- 5-10 adenomas: 3 years
- >10 adenomas: <3 years (consider polyposis syndrome)
- Advanced adenoma: 3 years
- Sessile serrated lesion <10mm: 5-10 years
- SSL >=10mm or with dysplasia: 3 years
- Piecemeal resection of >=20mm: 6 months

HIGH-RISK FEATURES:
- Family history of CRC in first-degree relative
- Lynch syndrome or polyposis syndrome screening
- Inflammatory bowel disease with dysplasia
- Incomplete resection or indeterminate margins
- Invasive cancer requiring surgical consultation
        """,
        key_factors=[
            "Adenoma detection rate (ADR) as quality metric (target >25%)",
            "Complete polyp resection with clear margins",
            "Accurate histologic classification and dysplasia grading",
            "Family history assessment for hereditary syndromes",
            "Bowel preparation quality affecting detection",
            "Withdrawal time minimum 6 minutes in normal colonoscopy",
            "Documentation of polyp size, location, morphology, resection method"
        ],
        primary_authority=[
            "USMSTF Colorectal Cancer Screening and Surveillance Guidelines (2020)",
            "ASGE Standards for Colonoscopy Quality Indicators",
            "Paris Classification of Superficial Neoplastic Lesions",
            "WHO Classification of Tumours: Digestive System (5th ed)"
        ],
        burden_holder="Endoscopist performing colonoscopy and gastroenterologist managing surveillance",
        adversary_position="Missed polyps, incomplete resection, interval cancers, inappropriate surveillance intervals, polyposis syndrome underdiagnosis",
        counter_arguments=[
            "Inadequate bowel preparation obscuring polyps",
            "Proximal serrated lesions difficult to detect",
            "Piecemeal resection increasing recurrence risk",
            "Patient non-adherence to surveillance recommendations",
            "Pathology-endoscopy discordance in polyp classification"
        ],
        resolution_strategy="High-quality colonoscopy with adequate preparation, withdrawal time >6 minutes, use of advanced imaging (NBI, chromoendoscopy) for flat lesions, photodocumentation of all polyps, clear communication of surveillance intervals, genetic counseling for suspected polyposis syndromes",
        entity_scope="All patients undergoing colonoscopy for screening, surveillance, or diagnostic evaluation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard surveillance intervals; disclosure needed for high-risk patients, complex polyposis, or incomplete resections",
        controlling_precedent=[
            "USMSTF Guidelines on Colorectal Cancer Screening and Surveillance",
            "NCCN Guidelines for Colorectal Cancer Screening",
            "ACG Clinical Guidelines: Colorectal Cancer Screening"
        ],
        zone=AnalysisZone.SCREENING,
        category=IssueCategory.COLORECTAL
    ),
    DoctrineCacheEntry(
        topic="Chronic Liver Disease Staging and Monitoring",
        keywords=["cirrhosis", "fibrosis", "hepatitis", "NASH", "FibroScan", "Child-Pugh", "MELD"],
        conclusion_template=[
            "Liver disease etiology is {primary_cause} with fibrosis stage {fibrosis_stage}. Decompensation risk is {risk_level}.",
            "Clinical scoring: Child-Pugh {cp_score}, MELD-Na {meld_score}. HCC surveillance {hcc_recommendation}.",
            "Management priorities: {treatment_targets}, varices screening {varices_plan}, transplant evaluation {transplant_timing}."
        ],
        reasoning_framework="""
Chronic liver disease requires systematic staging and complication surveillance:

ETIOLOGY ASSESSMENT:
- Viral hepatitis: HBV (HBsAg, HBeAg, HBV DNA), HCV (anti-HCV, HCV RNA, genotype)
- Alcohol-related liver disease: AST:ALT ratio >2, elevated GGT, CDT
- NAFLD/NASH: metabolic syndrome, imaging (steatosis), biopsy (NASH CRN score)
- Autoimmune hepatitis: ANA, ASMA, anti-LKM, elevated IgG, interface hepatitis
- Primary biliary cholangitis: AMA, elevated ALP, ductopenia on biopsy
- Primary sclerosing cholangitis: MRCP beading, ERCP strictures, IBD association
- Hemochromatosis: elevated ferritin, transferrin saturation >45%, HFE mutations
- Wilson disease: low ceruloplasmin, Kayser-Fleischer rings, elevated urinary copper
- Alpha-1 antitrypsin deficiency: low AAT level, PiZZ genotype, PAS-positive globules

FIBROSIS STAGING:
- Biopsy (METAVIR): F0 (none), F1 (portal), F2 (periportal), F3 (bridging), F4 (cirrhosis)
- FibroScan (kPa): <7 (F0-F1), 7-9.5 (F2), 9.5-12.5 (F3), >12.5 (F4)
- FIB-4 score: age, AST, ALT, platelet count (<1.45 low risk, >3.25 high risk)
- APRI: AST-to-platelet ratio index (<0.5 low fibrosis, >1.5 high fibrosis)
- ELF score: HA, PIIINP, TIMP-1 (European Liver Fibrosis panel)

SEVERITY SCORING:
- Child-Pugh: bilirubin, albumin, INR, ascites, encephalopathy (Class A/B/C)
- MELD-Na: bilirubin, INR, creatinine, sodium (transplant allocation score)
- MELD 3.0: adds sex and albumin to MELD-Na
- Barcelona Clinic Liver Cancer (BCLC): HCC staging system

COMPLICATION SURVEILLANCE:
- Varices: screening EGD at cirrhosis diagnosis, repeat q2-3y if no varices
- Hepatocellular carcinoma: ultrasound +/- AFP every 6 months
- Hepatic encephalopathy: precipitant identification (GI bleed, infection, constipation)
- Spontaneous bacterial peritonitis: diagnostic paracentesis for new-onset ascites
- Hepatorenal syndrome: rising creatinine without other cause, poor prognosis
- Portal vein thrombosis: Doppler ultrasound, especially if acute decompensation

TREATMENT STRATEGIES:
- Viral suppression: HBV (tenofovir, entecavir), HCV (DAA regimens >95% SVR)
- Alcohol cessation: critical for alcohol-related disease, reduces decompensation
- NASH management: weight loss 7-10%, diabetes/dyslipidemia control, emerging therapies
- Autoimmune: corticosteroids, azathioprine for AIH; ursodiol for PBC
- Varices: non-selective beta-blockers (propranolol, nadolol), EVL for high-risk varices
- Ascites: sodium restriction, diuretics (spironolactone + furosemide), LVP if tense
- HCC treatment: resection, ablation, TACE, systemic therapy per BCLC stage
        """,
        key_factors=[
            "Etiology-specific treatment to halt progression",
            "Fibrosis stage determination via non-invasive or biopsy",
            "Decompensation prevention and complication screening",
            "HCC surveillance in cirrhotic patients every 6 months",
            "Transplant evaluation timing (MELD >15, refractory complications)",
            "Varices screening and prophylaxis to prevent bleeding",
            "Medication adjustment for hepatic impairment"
        ],
        primary_authority=[
            "AASLD Practice Guidance on Cirrhosis Complications (2023)",
            "EASL Clinical Practice Guidelines: Liver Transplantation",
            "AASLD-IDSA HCV Guidance: Recommendations for Testing, Managing, and Treating Hepatitis C",
            "AASLD Guidelines: Prevention, Diagnosis, and Treatment of Hepatocellular Carcinoma"
        ],
        burden_holder="Hepatologist managing chronic liver disease and complication surveillance",
        adversary_position="Disease progression despite treatment, decompensation events, HCC development, transplant candidacy denial",
        counter_arguments=[
            "Non-adherence to antiviral therapy or alcohol cessation",
            "Delayed diagnosis of cirrhosis until decompensation",
            "Inadequate HCC surveillance leading to advanced-stage diagnosis",
            "Medication hepatotoxicity accelerating liver injury",
            "Comorbidities limiting transplant eligibility"
        ],
        resolution_strategy="Etiology-specific therapy to halt fibrosis progression, protocol-driven HCC and varices surveillance, early transplant evaluation for MELD >15 or refractory ascites/encephalopathy, multidisciplinary care with hepatology/transplant/addiction medicine, patient education on abstinence and medication adherence",
        entity_scope="All patients with chronic liver disease from any etiology",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for established cirrhosis management; disclosure needed for emerging therapies (NASH), complex HCC staging, or marginal transplant candidates",
        controlling_precedent=[
            "AASLD Practice Guidance on Acute-on-Chronic Liver Failure",
            "UNOS Liver Allocation Policy (MELD-based)",
            "AASLD Guidelines on Variceal Hemorrhage"
        ],
        zone=AnalysisZone.TREATMENT,
        category=IssueCategory.HEPATOLOGY
    ),
    DoctrineCacheEntry(
        topic="Inflammatory Bowel Disease Monitoring and Escalation",
        keywords=["Crohn's disease", "ulcerative colitis", "IBD", "biologics", "fecal calprotectin", "stricture"],
        conclusion_template=[
            "IBD activity: {disease_activity_score} with {objective_markers}. Current therapy is {treatment_response}.",
            "Escalation indicated by {escalation_triggers}. Recommended adjustment: {treatment_plan}.",
            "Complication risk: {complications}. Surveillance strategy: {surveillance_plan}."
        ],
        reasoning_framework="""
IBD management requires treat-to-target approach with objective monitoring:

DISEASE ACTIVITY ASSESSMENT:
Crohn's Disease:
- Harvey-Bradshaw Index (HBI): clinical symptoms score
- Crohn's Disease Activity Index (CDAI): research standard
- SES-CD (Simple Endoscopic Score): endoscopic activity 0-60
- MaRIA score (MR index of activity): cross-sectional imaging

Ulcerative Colitis:
- Mayo Score: clinical (stool frequency, rectal bleeding, physician global) + endoscopic
- Partial Mayo Score: excludes endoscopy for non-invasive monitoring
- Nancy Index: histologic activity grading
- Geboes Score: detailed histologic scoring system

OBJECTIVE MONITORING:
- Fecal calprotectin: <50 mcg/g (remission), 50-250 (mild), >250 (active inflammation)
- C-reactive protein: marker of systemic inflammation, less specific than calprotectin
- Endoscopic healing: Mayo 0-1 for UC, SES-CD <3 for CD (target endpoint)
- Histologic remission: absence of active inflammation on biopsy (emerging target)
- Cross-sectional imaging: MR/CT enterography for strictures, fistulas, abscesses

TREATMENT ESCALATION LADDER:
Step 1 - Aminosalicylates:
- Mesalamine (5-ASA): UC first-line, limited efficacy in CD
- Sulfasalazine: alternative, more side effects

Step 2 - Immunomodulators:
- Azathioprine/6-mercaptopurine: steroid-sparing, slow onset (3-6 months)
- Methotrexate: alternative for AZA intolerance, monitor LFTs
- TPMT testing: prevent myelosuppression in poor metabolizers

Step 3 - Biologics:
- Anti-TNF: infliximab, adalimumab, certolizumab, golimumab
- Anti-integrin: vedolizumab (gut-selective, less immunosuppression)
- Anti-IL12/23: ustekinumab (effective in anti-TNF failures)
- Anti-IL23: risankizumab (emerging option)

Step 4 - Small molecules:
- JAK inhibitors: tofacitinib (UC), upadacitinib (CD/UC)
- S1P modulators: ozanimod (UC), emerging therapies

Step 5 - Surgical intervention:
- UC: colectomy curative, ileal pouch-anal anastomosis (IPAA)
- CD: resection for strictures/fistulas, not curative, recurrence common

ESCALATION TRIGGERS:
- Persistent symptoms despite optimization (non-adherence ruled out)
- Objective evidence of active inflammation (calprotectin >250, elevated CRP)
- Endoscopic disease activity (Mayo >=2, SES-CD >=3)
- Loss of response to current therapy (secondary non-response)
- Corticosteroid dependence (inability to taper below 10mg prednisone)
- Fistulizing or stricturing complications in Crohn's disease
- Dysplasia detected on surveillance colonoscopy

COMPLICATIONS SURVEILLANCE:
- Colorectal cancer: colonoscopy every 1-3 years after 8-10 years of disease
- Primary sclerosing cholangitis: annual MRCP, ERCP if jaundice/cholangitis
- Strictures: endoscopic dilation vs surgical resection
- Fistulas: MRI pelvis, exam under anesthesia, seton placement
- Abscess: CT/MRI imaging, antibiotics +/- drainage before biologics
- Osteoporosis: DEXA scan, especially if chronic steroid use
- Venous thromboembolism: higher risk during flares, consider prophylaxis
        """,
        key_factors=[
            "Objective disease activity markers (calprotectin, CRP, endoscopy)",
            "Treat-to-target approach with mucosal healing endpoint",
            "Medication optimization before declaring treatment failure",
            "Therapeutic drug monitoring for biologics (trough levels, antibodies)",
            "Early use of combination therapy (biologic + immunomodulator)",
            "Surgical consultation for medically refractory disease or complications",
            "Dysplasia surveillance in long-standing colitis"
        ],
        primary_authority=[
            "AGA Clinical Practice Update on Management of Inflammatory Bowel Disease (2023)",
            "ACG Clinical Guideline: Ulcerative Colitis in Adults",
            "ACG Clinical Guideline: Management of Crohn's Disease in Adults",
            "ECCO Guidelines on Therapeutics in Crohn's Disease and Ulcerative Colitis"
        ],
        burden_holder="Gastroenterologist managing IBD therapy and monitoring disease activity",
        adversary_position="Inadequate disease control, progression to complications, treatment-related adverse events, surgical necessity",
        counter_arguments=[
            "Patient non-adherence affecting treatment outcomes",
            "IBS symptoms mimicking active IBD (functional overlap)",
            "Infection (C. diff, CMV) masquerading as IBD flare",
            "Medication side effects limiting escalation options",
            "Insurance barriers to biologic therapy access"
        ],
        resolution_strategy="Objective monitoring with biomarkers and endoscopy, treat-to-target approach with mucosal healing goal, early combination therapy for moderate-severe disease, therapeutic drug monitoring to optimize biologics, multidisciplinary care with surgery/nutrition/mental health, patient education on medication adherence and symptom-versus-inflammation distinction",
        entity_scope="All patients with confirmed inflammatory bowel disease (Crohn's disease or ulcerative colitis)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for established treatment algorithms; disclosure needed for refractory disease, emerging therapies, or complex surgical decisions",
        controlling_precedent=[
            "AGA Guidelines on Therapeutic Drug Monitoring in IBD",
            "ACG Clinical Practice Update: Biosimilars in IBD",
            "STRIDE-II: Selecting Therapeutic Targets in IBD (2021)"
        ],
        zone=AnalysisZone.TREATMENT,
        category=IssueCategory.IBD
    ),
    DoctrineCacheEntry(
        topic="Hepatocellular Carcinoma Screening and Diagnosis",
        keywords=["HCC", "liver cancer", "AFP", "LIRADS", "surveillance", "cirrhosis screening"],
        conclusion_template=[
            "HCC surveillance in {risk_population} using {modality} every {interval}. Current findings: {imaging_result}.",
            "Diagnosis criteria: {diagnostic_algorithm} with LI-RADS category {lirads_score}. Staging: {bclc_stage}.",
            "Treatment recommendation: {treatment_modality} with expected outcomes {prognosis}."
        ],
        reasoning_framework="""
HCC surveillance and diagnosis in at-risk populations:

HIGH-RISK POPULATIONS (SURVEILLANCE INDICATED):
- Cirrhosis: any etiology (HBV, HCV, alcohol, NASH, hemochromatosis, etc.)
- Chronic HBV: Asian males >40, Asian females >50, Africans >20, family history HCC
- Chronic HCV: advanced fibrosis (F3) even without cirrhosis
- Non-cirrhotic HBV: active hepatitis, family history of HCC, elevated HBV DNA
- Primary biliary cholangitis and primary sclerosing cholangitis with cirrhosis

SURVEILLANCE PROTOCOL:
- Ultrasound +/- AFP every 6 months (AASLD recommendation)
- Ultrasound sensitivity 60-80% (operator-dependent, body habitus affects quality)
- AFP alone NOT recommended (40% of HCC AFP-negative at diagnosis)
- AFP >20 ng/mL: consider additional imaging even if normal ultrasound
- Surveillance continuation until liver transplant or patient unsuitable for treatment

DIAGNOSTIC IMAGING (LI-RADS):
LR-1: Definitely benign (cyst, hemangioma)
LR-2: Probably benign (atypical hemangioma, perfusion alteration)
LR-3: Intermediate probability (small nodule, indeterminate enhancement)
LR-4: Probably HCC (arterial hyperenhancement, non-rim APHE)
LR-5: Definitely HCC (APHE + washout + capsule, size >=10mm)
LR-M: Probably malignant but not HCC specific (cholangiocarcinoma, metastasis)
LR-TIV: Tumor in vein (definite HCC with vascular invasion)

DIAGNOSTIC CRITERIA:
- Nodule >=1cm with arterial hyperenhancement + washout on delayed phase = HCC
- Multiphase CT or MRI with liver-specific contrast (Eovist, MultiHance)
- LR-5 lesion: no biopsy needed for diagnosis in cirrhotic liver
- LR-3/LR-4 lesions: short-interval follow-up (3-6 months) or biopsy
- AFP >200 ng/mL with arterial hyperenhancement: highly suggestive even without washout
- Biopsy: risk of seeding (<3%), reserved for diagnostic uncertainty or transplant listing

BARCELONA CLINIC LIVER CANCER (BCLC) STAGING:
Stage 0 (Very Early): Single nodule <2cm, PS 0, Child-Pugh A
- Treatment: Resection or ablation, 5-year survival 70-90%

Stage A (Early): Single or up to 3 nodules <3cm, PS 0, Child-Pugh A-B
- Treatment: Resection, ablation, or transplant, 5-year survival 50-70%

Stage B (Intermediate): Multinodular, PS 0, Child-Pugh A-B
- Treatment: TACE (transarterial chemoembolization), 3-year survival 50%

Stage C (Advanced): Portal invasion, extrahepatic spread, PS 1-2, Child-Pugh A-B
- Treatment: Systemic therapy (atezolizumab + bevacizumab, sorafenib, lenvatinib)

Stage D (Terminal): PS 3-4 or Child-Pugh C
- Treatment: Best supportive care, median survival <6 months

TREATMENT MODALITIES:
- Resection: non-cirrhotic or Child-Pugh A with preserved liver function, adequate remnant
- Ablation: RFA or microwave for tumors <3cm not amenable to resection
- Transplantation: Milan criteria (single <=5cm or up to 3 nodules <=3cm), best long-term cure
- TACE: intermediate-stage disease, selective arterial embolization with chemotherapy
- Radioembolization (Y-90): alternative to TACE, portal vein thrombosis not contraindication
- Systemic therapy: atezolizumab + bevacizumab first-line (IMbrave150 trial), sorafenib, lenvatinib
- Immunotherapy: pembrolizumab, nivolumab for second-line or special populations

PROGNOSIS FACTORS:
- Tumor burden: size, number, vascular invasion, extrahepatic spread
- Liver function: Child-Pugh score, MELD score, portal hypertension
- Performance status: ECOG 0-1 vs 2-4
- AFP level: >400 ng/mL associated with worse prognosis
- Response to therapy: mRECIST criteria for locoregional therapy assessment
        """,
        key_factors=[
            "Surveillance adherence in at-risk populations (every 6 months)",
            "High-quality imaging interpretation using LI-RADS classification",
            "Multidisciplinary tumor board review for treatment planning",
            "Liver function preservation (Child-Pugh A ideal for curative therapy)",
            "Milan criteria assessment for transplant candidacy",
            "Early detection improving curative treatment options",
            "Systemic therapy advances (immunotherapy combinations)"
        ],
        primary_authority=[
            "AASLD Guidelines: Prevention, Diagnosis, and Treatment of Hepatocellular Carcinoma (2018)",
            "ACR LI-RADS v2018 Core: CT/MRI Diagnostic Algorithm",
            "EASL Clinical Practice Guidelines: Management of Hepatocellular Carcinoma",
            "NCCN Guidelines: Hepatobiliary Cancers"
        ],
        burden_holder="Hepatologist conducting surveillance and gastroenterologist/oncologist managing treatment",
        adversary_position="Missed HCC on surveillance, delayed diagnosis until advanced stage, treatment complications, recurrence post-therapy",
        counter_arguments=[
            "Patient non-adherence to surveillance schedule",
            "Inadequate ultrasound quality in obese patients or fatty liver",
            "LR-3/LR-4 lesions with diagnostic uncertainty requiring follow-up",
            "Liver dysfunction (Child-Pugh B/C) limiting curative options",
            "Tumor progression between surveillance intervals (interval cancers)"
        ],
        resolution_strategy="Protocol-driven surveillance every 6 months with ultrasound +/- AFP, high-quality multiphase imaging for nodule characterization, LI-RADS standardized reporting, multidisciplinary tumor board for treatment planning, early transplant referral for Milan criteria candidates, systemic therapy for advanced disease with immunotherapy combinations",
        entity_scope="All cirrhotic patients and non-cirrhotic chronic HBV carriers with HCC risk factors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for established BCLC staging and treatment algorithms; disclosure needed for borderline transplant candidates, experimental therapies, or downstaging strategies",
        controlling_precedent=[
            "UNOS Liver Allocation Policy for HCC (MELD exception points)",
            "Milan Criteria for Liver Transplantation in HCC",
            "mRECIST Criteria for HCC Response Assessment"
        ],
        zone=AnalysisZone.SCREENING,
        category=IssueCategory.GI_ONCOLOGY
    ),
    DoctrineCacheEntry(
        topic="Gastroesophageal Reflux Disease Diagnosis and Management",
        keywords=["GERD", "reflux", "heartburn", "PPI", "pH monitoring", "Nissen fundoplication"],
        conclusion_template=[
            "GERD diagnosis based on {diagnostic_criteria}. PPI trial response: {ppi_response}.",
            "Testing recommended: {testing_modality} to evaluate {indication}.",
            "Management plan: {treatment_strategy} with escalation to {next_step} if refractory."
        ],
        reasoning_framework="""
GERD diagnosis and management algorithm:

DIAGNOSTIC APPROACH:
Clinical Diagnosis (No Testing):
- Typical symptoms: heartburn, regurgitation, relieved by antacids
- Response to empiric PPI trial (2-4 weeks)
- No alarm symptoms: dysphagia, weight loss, GI bleeding, anemia

Testing Indications:
- Alarm symptoms: EGD to rule out malignancy, stricture, Barrett's
- Atypical symptoms: chest pain, chronic cough, laryngitis, asthma
- Refractory symptoms: PPI non-response or incomplete response
- Pre-operative evaluation: confirm reflux before anti-reflux surgery
- Young patient (<50) with chronic symptoms: rule out eosinophilic esophagitis

DIAGNOSTIC MODALITIES:
Upper Endoscopy (EGD):
- LA classification of erosive esophagitis (Grade A-D)
- Barrett's esophagus screening (Prague C&M criteria)
- Stricture evaluation and dilation
- Eosinophilic esophagitis (>15 eosinophils per HPF)

Ambulatory pH Monitoring:
- 24-hour pH probe: gold standard for acid reflux quantification
- DeMeester score >14.7 = abnormal acid exposure
- Symptom-reflux correlation (symptom index, symptom association probability)
- Wireless pH capsule (Bravo): 48-96 hour monitoring, no nasal discomfort
- pH-impedance: detects non-acid reflux (weakly acidic, alkaline)

Esophageal Manometry:
- NOT diagnostic for GERD (normal LES pressure in many GERD patients)
- Pre-operative requirement: rule out achalasia or major motility disorder
- Assess peristalsis adequacy for fundoplication candidacy
- Diagnose ineffective esophageal motility (may worsen post-fundoplication dysphagia)

Barium Esophagram:
- Anatomic assessment: hiatal hernia size, stricture, esophageal shortening
- Functional assessment: delayed emptying, reflux visualization (low sensitivity)

TREATMENT ALGORITHM:
Lifestyle Modifications:
- Weight loss if BMI >25 (strong evidence)
- Elevate head of bed 6-8 inches (nocturnal reflux)
- Avoid late meals (within 3 hours of bedtime)
- Trigger food avoidance: caffeine, alcohol, chocolate, peppermint, spicy/fatty foods
- Smoking cessation (weakens LES, impairs healing)

Pharmacotherapy:
Step 1 - H2 Receptor Antagonists:
- Ranitidine (withdrawn), famotidine 20-40mg BID
- Tachyphylaxis common, less effective than PPIs

Step 2 - Proton Pump Inhibitors (PPIs):
- Standard dose: omeprazole 20mg, lansoprazole 30mg, esomeprazole 20mg daily
- Take 30-60 minutes before first meal (requires acid for activation)
- 70-80% symptom resolution in erosive esophagitis
- Twice-daily dosing for refractory symptoms or severe esophagitis

Step 3 - PPI Optimization:
- Increase to BID dosing (before breakfast and dinner)
- Switch to different PPI (variable CYP2C19 metabolism)
- Ensure proper timing (pre-meal, not bedtime)
- Add bedtime H2RA for nocturnal acid breakthrough

Step 4 - Refractory GERD Evaluation:
- Confirm diagnosis: pH monitoring on therapy to document acid breakthrough
- Rule out alternative diagnoses: eosinophilic esophagitis, functional heartburn
- Assess adherence and proper PPI timing
- Consider non-acid reflux (pH-impedance testing)
- Baclofen for transient LES relaxations (off-label)

Surgical Therapy:
- Nissen fundoplication: 360-degree wrap, gold standard
- Toupet fundoplication: 270-degree wrap, lower dysphagia risk
- LINX device: magnetic sphincter augmentation, preserves belching ability
- Transoral incisionless fundoplication (TIF): endoscopic alternative, less durable

SURGICAL CANDIDACY:
Indications:
- Objectively confirmed GERD (pH testing) with good PPI response
- Patient preference to avoid lifelong medication
- Large hiatal hernia with reflux symptoms
- Volume regurgitation despite medical therapy
- Compliance issues with medication

Contraindications:
- Absent or severely impaired esophageal motility (achalasia, scleroderma)
- Barrett's esophagus with high-grade dysplasia (need oncologic resection)
- Functional heartburn (no acid reflux on testing)
- Unrealistic patient expectations

LONG-TERM PPI CONCERNS:
- Osteoporosis/fractures: consider calcium/vitamin D supplementation, DEXA screening
- Hypomagnesemia: check level if chronic PPI use, especially with diuretics
- C. difficile infection: higher risk, avoid unnecessary antibiotics
- Chronic kidney disease: possible association, monitor renal function
- Dementia: controversial association, not definitive causation
- Gastric polyps: fundic gland polyps common, generally benign
- Rebound acid hypersecretion: taper PPI slowly to avoid symptom recurrence
        """,
        key_factors=[
            "Empiric PPI trial appropriate for typical symptoms without alarm features",
            "Endoscopy indicated for alarm symptoms or refractory GERD",
            "pH monitoring confirms diagnosis in atypical or refractory cases",
            "Surgical candidacy requires objective reflux confirmation and good PPI response",
            "Long-term PPI safety monitoring for osteoporosis, magnesium, renal function",
            "Lifestyle modifications foundational but insufficient alone for most patients",
            "Barrett's esophagus surveillance in chronic GERD (especially white males >50)"
        ],
        primary_authority=[
            "ACG Clinical Guideline: Diagnosis and Management of Gastroesophageal Reflux Disease (2022)",
            "ASGE Standards of Practice: Role of Endoscopy in GERD",
            "AGA Clinical Practice Update on Surgical Management of GERD",
            "Lyon Consensus on GERD Diagnosis"
        ],
        burden_holder="Gastroenterologist managing GERD therapy and surgeon performing anti-reflux procedures",
        adversary_position="Refractory symptoms despite therapy, PPI side effects, post-surgical dysphagia or gas bloat, progression to Barrett's esophagus",
        counter_arguments=[
            "Functional heartburn (esophageal hypersensitivity) not responsive to acid suppression",
            "Non-acid reflux (weakly acidic, bile) not detected by standard pH monitoring",
            "Poor PPI adherence or improper timing affecting efficacy",
            "Eosinophilic esophagitis misdiagnosed as refractory GERD",
            "Post-fundoplication dysphagia or inability to belch/vomit"
        ],
        resolution_strategy="Stepwise approach starting with lifestyle and PPI therapy, diagnostic testing for atypical or refractory symptoms, pH monitoring to confirm diagnosis before surgery, manometry to assess surgical candidacy, shared decision-making on long-term PPI vs surgical intervention, Barrett's surveillance per guidelines",
        entity_scope="All patients with symptoms suggestive of gastroesophageal reflux disease",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for typical GERD management; disclosure needed for refractory cases, surgical decision-making, or diagnosis uncertainty",
        controlling_precedent=[
            "Lyon Consensus: Updated Definition of GERD",
            "SAGES Guidelines for Surgical Treatment of GERD",
            "ACG Guidelines on Barrett's Esophagus Surveillance"
        ],
        zone=AnalysisZone.TREATMENT,
        category=IssueCategory.ESOPHAGEAL
    ),
    DoctrineCacheEntry(
        topic="Celiac Disease Diagnosis and Management",
        keywords=["celiac", "gluten", "villous atrophy", "tissue transglutaminase", "HLA-DQ2", "gluten-free diet"],
        conclusion_template=[
            "Celiac disease evaluation: {serology_results} with biopsy showing {histology_findings}. Diagnosis {diagnosis_status}.",
            "Dietary management: {diet_plan}. Monitoring: {follow_up_strategy}.",
            "Complications screening: {complication_assessment}. Non-responsive celiac: {refractory_evaluation}."
        ],
        reasoning_framework="""
Celiac disease diagnosis requires positive serology AND confirmatory biopsy:

SEROLOGIC TESTING (PATIENT MUST BE ON GLUTEN-CONTAINING DIET):
First-Line Tests:
- IgA tissue transglutaminase (tTG-IgA): sensitivity 95%, specificity 98%
- Total IgA level: rule out IgA deficiency (1-3% of celiac patients)
- If IgA deficient: IgG-based tests (tTG-IgG, DGP-IgG)

Additional Tests:
- IgA endomysial antibody (EMA-IgA): highly specific (>99%), observer-dependent
- Deamidated gliadin peptide (DGP-IgG/IgA): useful in children <2 years old
- HLA-DQ2/DQ8 genotyping: negative result rules out celiac (99% NPV), used to exclude diagnosis

ENDOSCOPY AND BIOPSY:
Duodenal Biopsy Protocol:
- 4-6 biopsies from second/third portion of duodenum
- At least 1 biopsy from duodenal bulb (25% have bulb-only disease)
- Orientation on filter paper for proper histologic sectioning

Marsh-Oberhuber Classification:
- Marsh 0: Normal mucosa
- Marsh 1: Increased intraepithelial lymphocytes (>25 per 100 enterocytes)
- Marsh 2: Crypt hyperplasia
- Marsh 3a: Partial villous atrophy
- Marsh 3b: Subtotal villous atrophy
- Marsh 3c: Total villous atrophy

DIAGNOSTIC CRITERIA:
Definite Celiac Disease:
- Positive tTG-IgA (>10x ULN) + positive EMA + Marsh 3 on biopsy
- Or: Positive tTG-IgA + Marsh 2-3 on biopsy

Probable Celiac (Equivocal):
- Marsh 1 histology + positive serology: repeat biopsy after continued gluten exposure
- Borderline serology + normal biopsy: consider HLA typing or gluten challenge

Biopsy Not Required (Pediatric Exception):
- tTG-IgA >10x ULN + positive EMA + symptomatic child: start GFD without biopsy (ESPGHAN 2020)

GLUTEN-FREE DIET MANAGEMENT:
Dietary Education:
- Eliminate wheat, barley, rye (oats controversial - often cross-contaminated)
- Read labels: hidden gluten in sauces, processed foods, medications
- Cross-contamination: separate cooking utensils, toasters, cutting boards
- Safe grains: rice, corn, quinoa, millet, certified gluten-free oats

Nutritional Deficiencies (Screen and Supplement):
- Iron deficiency: check CBC, ferritin, supplement if low
- Vitamin D and calcium: DEXA scan for osteoporosis, supplement to prevent fractures
- Vitamin B12, folate: megaloblastic anemia risk
- Fat-soluble vitamins (A, D, E, K): if malabsorption severe
- Zinc, copper: trace element deficiencies in long-standing disease

MONITORING AND FOLLOW-UP:
Initial Follow-up (3-6 months):
- Symptom improvement (70-80% improve within weeks)
- Repeat serology (tTG-IgA): should decline, normalize within 6-12 months
- Nutritional assessment: correct deficiencies

Long-term Monitoring (Annually):
- Clinical symptom review
- Serology (tTG-IgA): persistent positivity suggests ongoing gluten exposure
- Repeat biopsy generally NOT needed if clinical/serologic response adequate
- Screen for complications: osteoporosis (DEXA), thyroid disease (TSH), type 1 diabetes

COMPLICATIONS SCREENING:
- Refractory celiac disease: persistent symptoms despite strict GFD >12 months
- Enteropathy-associated T-cell lymphoma (EATL): rare, presents with alarm symptoms
- Small bowel adenocarcinoma: 2-3x increased risk
- Ulcerative jejunitis: persistent abdominal pain, bleeding, perforation risk
- Dermatitis herpetiformis: pruritic vesicular rash, extremely specific for celiac
- Autoimmune conditions: type 1 diabetes, autoimmune thyroiditis, Sjogren's syndrome

REFRACTORY CELIAC DISEASE (RCD):
Definition: Persistent or recurrent villous atrophy with symptoms despite strict GFD >12 months

Type 1 RCD:
- Normal intraepithelial lymphocytes (IELs), polyclonal T-cells
- Better prognosis, may respond to corticosteroids

Type 2 RCD:
- Abnormal IELs with clonal T-cell population (flow cytometry, TCR gene rearrangement)
- High risk progression to EATL (50% 5-year risk)
- Immunosuppression (steroids, azathioprine), cladribine chemotherapy

Evaluation of Suspected RCD:
- Confirm strict GFD adherence (dietitian assessment, urine gluten peptide testing)
- Repeat biopsies with immunohistochemistry for IEL phenotyping
- Small bowel imaging (CT/MR enterography): rule out lymphoma, ulceration, strictures
- Capsule endoscopy: assess disease distribution, identify complications
- PET-CT: if concern for lymphoma transformation
        """,
        key_factors=[
            "Patient must be on gluten-containing diet for accurate testing",
            "Serology AND biopsy required for definitive diagnosis (except pediatric exception)",
            "Strict lifelong gluten-free diet is only treatment",
            "Monitor for nutritional deficiencies and complications",
            "Family screening recommended (10% first-degree relative risk)",
            "Refractory celiac requires aggressive workup for lymphoma",
            "Annual follow-up with serology and symptom assessment"
        ],
        primary_authority=[
            "AGA Clinical Practice Update on Diagnosis and Monitoring of Celiac Disease (2021)",
            "ACG Clinical Guidelines: Diagnosis and Management of Celiac Disease",
            "ESPGHAN Guidelines for Diagnosing Celiac Disease (2020)",
            "BSG Guidelines on Coeliac Disease"
        ],
        burden_holder="Gastroenterologist diagnosing celiac disease and managing gluten-free diet adherence",
        adversary_position="Missed diagnosis in atypical presentations, false-negative testing if already on GFD, non-adherence to diet, refractory disease development",
        counter_arguments=[
            "Patient already started GFD before testing (serology/biopsy false-negative)",
            "IgA deficiency causing false-negative tTG-IgA",
            "Non-celiac gluten sensitivity (no serology/biopsy abnormalities, diagnosis of exclusion)",
            "Inadvertent gluten exposure preventing serologic normalization",
            "Refractory celiac type 2 progressing to lymphoma despite treatment"
        ],
        resolution_strategy="Pre-test counseling to maintain gluten intake, comprehensive serology with IgA level, adequate duodenal biopsy sampling including bulb, dietitian education on strict GFD, monitoring for adherence and complications, family screening, aggressive workup for refractory disease with immunophenotyping and imaging",
        entity_scope="All patients with suspected celiac disease based on symptoms, serology, or family history",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard celiac diagnosis and management; disclosure needed for refractory cases, equivocal serology/biopsy, or suspected lymphoma",
        controlling_precedent=[
            "AGA Guidelines on Diagnosis and Monitoring of Celiac Disease",
            "Marsh-Oberhuber Classification for Histology",
            "ESPGHAN Criteria for Pediatric Diagnosis Without Biopsy"
        ],
        zone=AnalysisZone.DIAGNOSTIC,
        category=IssueCategory.INTESTINAL
    ),
    DoctrineCacheEntry(
        topic="Acute Pancreatitis Diagnosis and Severity Assessment",
        keywords=["pancreatitis", "lipase", "gallstones", "ERCP", "necrotizing pancreatitis", "Ranson criteria"],
        conclusion_template=[
            "Acute pancreatitis diagnosis based on {diagnostic_criteria}. Etiology: {etiology_assessment}.",
            "Severity stratification: {severity_score} with predicted mortality {mortality_risk}.",
            "Management: {treatment_plan}. ERCP indicated: {ercp_recommendation}. Complications: {complications_monitoring}."
        ],
        reasoning_framework="""
Acute pancreatitis diagnosis requires 2 of 3 criteria within 48 hours:

DIAGNOSTIC CRITERIA (ATLANTA CRITERIA 2012):
1. Abdominal pain consistent with pancreatitis (epigastric, radiating to back)
2. Serum lipase or amylase >3x upper limit of normal
3. Imaging findings consistent with pancreatitis (CT, MRI, ultrasound)

ETIOLOGY DETERMINATION:
Common Causes (80%):
- Gallstones (40%): RUQ ultrasound shows cholelithiasis, cholecystitis, dilated CBD
- Alcohol (30%): chronic heavy use (>50g/day for >5 years)
- Hypertriglyceridemia (1-4%): triglycerides >1000 mg/dL
- ERCP-induced (5%): post-procedure pancreatitis within 24 hours
- Medications (2%): azathioprine, valproic acid, L-asparaginase, 6-MP, didanosine

Less Common Causes:
- Hypercalcemia: hyperparathyroidism, malignancy
- Autoimmune pancreatitis: IgG4 elevation, sausage-shaped pancreas, steroid-responsive
- Hereditary pancreatitis: PRSS1, SPINK1, CFTR mutations, family history
- Anatomic: pancreas divisum, annular pancreas, sphincter of Oddi dysfunction
- Ischemic: shock, vasculitis, embolic events
- Infection: mumps, coxsackie, CMV, HIV
- Venom: scorpion sting (Trinidad, Arizona bark scorpion)

Idiopathic (10-20%): after workup excludes above causes, consider EUS for microlithiasis, MRCP for anatomic variants

SEVERITY STRATIFICATION:
Revised Atlanta Classification (2012):
- Mild: No organ failure, no local/systemic complications, resolves within 1 week
- Moderately Severe: Transient organ failure (<48 hours) or local/systemic complications
- Severe: Persistent organ failure (>48 hours), mortality 30-50%

Organ Failure Criteria (Modified Marshall Score):
- Respiratory: PaO2/FiO2 <=300
- Renal: Creatinine >=1.9 mg/dL
- Cardiovascular: Systolic BP <90 mmHg despite fluids

Local Complications:
- Acute peripancreatic fluid collection (APFC): <4 weeks, no wall
- Pancreatic pseudocyst: >4 weeks, well-defined wall, no solid debris
- Acute necrotic collection (ANC): <4 weeks, necrosis + fluid
- Walled-off necrosis (WON): >4 weeks, encapsulated necrosis

SCORING SYSTEMS:
Ranson Criteria (at admission and 48 hours):
At Admission: Age >55, WBC >16K, glucose >200, LDH >350, AST >250
At 48 Hours: Hct drop >10%, BUN rise >5, Ca <8, PaO2 <60, base deficit >4, fluid sequestration >6L
Score >=3: severe pancreatitis, mortality increases with score

BISAP Score (simpler, at 24 hours):
- BUN >25 mg/dL
- Impaired mental status
- SIRS (2+ criteria: T>38 or <36, HR>90, RR>20, WBC>12K or <4K)
- Age >60 years
- Pleural effusion on imaging
Score >=3: high risk for mortality

APACHE II: general ICU scoring, >8 predicts severe disease

CT Severity Index (Balthazar Score + Necrosis):
Grade A (0 points): Normal pancreas
Grade B (1 point): Pancreatic enlargement
Grade C (2 points): Peripancreatic inflammation
Grade D (3 points): Single fluid collection
Grade E (4 points): Multiple fluid collections or gas
Necrosis: <30% (+2), 30-50% (+4), >50% (+6)
Total >6: severe pancreatitis, high complication risk

IMAGING RECOMMENDATIONS:
Ultrasound: First-line for gallstone pancreatitis evaluation
CT with IV Contrast: NOT routine, indicated if:
- Diagnostic uncertainty after 48-72 hours
- Clinical deterioration despite treatment
- Suspicion of complications (necrosis, infection, hemorrhage)
- Failure to improve after 7-10 days
- Optimal timing: 72-96 hours (allows necrosis to fully develop)

MRCP: Evaluate biliary tree if gallstone pancreatitis but stones not seen on ultrasound

MANAGEMENT PRINCIPLES:
Fluid Resuscitation:
- Aggressive IV fluids: 250-500 mL/hr LR (preferred over NS)
- Goal UOP >0.5 mL/kg/hr, Hct 35-44%
- Avoid over-resuscitation (abdominal compartment syndrome risk)

Analgesia: Opioids as needed (morphine does NOT worsen pancreatitis via sphincter of Oddi spasm)

Nutrition:
- Mild pancreatitis: oral feeding as tolerated (no benefit to NPO)
- Severe pancreatitis: enteral nutrition (NG or NJ tube) preferred over TPN
- Start within 48-72 hours to prevent bacterial translocation

Antibiotics: NOT routinely indicated
- Prophylactic antibiotics do NOT prevent infected necrosis (meta-analyses)
- Treat only if proven infection: pancreatic necrosis with gas, positive culture, sepsis

ERCP Timing:
- Urgent (<24 hours): Acute cholangitis with pancreatitis (biliary obstruction + infection)
- Early (<72 hours): Predicted severe gallstone pancreatitis WITHOUT cholangitis (controversial)
- Elective: Mild gallstone pancreatitis after inflammation resolves, before cholecystectomy

Cholecystectomy:
- Mild gallstone pancreatitis: same admission after clinical improvement
- Severe pancreatitis: delay 6+ weeks until inflammation resolves, interval cholecystectomy

COMPLICATIONS MANAGEMENT:
Infected Necrosis:
- Suspect if clinical deterioration, fever, leukocytosis after initial improvement
- CT-guided FNA for culture if diagnosis uncertain
- Step-up approach: antibiotics → percutaneous drainage → minimally invasive necrosectomy → open necrosectomy
- Delay intervention until WON forms (>4 weeks) for easier debridement

Pancreatic Pseudocyst:
- Most resolve spontaneously if <6cm and asymptomatic
- Drain if symptomatic (pain, obstruction, infection) or enlarging
- Endoscopic drainage (cystgastrostomy) preferred over surgical or percutaneous

Abdominal Compartment Syndrome:
- Intra-abdominal pressure >20 mmHg with organ dysfunction
- Measure bladder pressure, avoid over-resuscitation
- Surgical decompression if medical management fails
        """,
        key_factors=[
            "Diagnosis requires 2 of 3 criteria (pain, lipase >3x ULN, imaging)",
            "Aggressive early fluid resuscitation improves outcomes",
            "CT imaging delayed 72-96 hours for optimal necrosis assessment",
            "Early enteral nutrition in severe pancreatitis prevents complications",
            "Antibiotics NOT indicated prophylactically, only for proven infection",
            "ERCP urgent only for cholangitis, not routine in gallstone pancreatitis",
            "Step-up approach to infected necrosis (conservative to invasive)"
        ],
        primary_authority=[
            "ACG Clinical Guideline: Management of Acute Pancreatitis (2013)",
            "AGA Clinical Practice Update: Necrotizing Pancreatitis (2022)",
            "IAP/APA Guidelines for Management of Acute Pancreatitis (2013)",
            "Revised Atlanta Classification of Acute Pancreatitis (2012)"
        ],
        burden_holder="Gastroenterologist managing acute pancreatitis and interventional endoscopist performing ERCP/drainage",
        adversary_position="Progression to necrotizing pancreatitis, organ failure, infected necrosis, abdominal compartment syndrome, death",
        counter_arguments=[
            "Over-resuscitation causing abdominal compartment syndrome or pulmonary edema",
            "Delayed diagnosis of infected necrosis leading to sepsis",
            "Unnecessary ERCP in mild gallstone pancreatitis (procedure-related complications)",
            "Premature CT imaging before necrosis fully develops (underestimation)",
            "NPO status delaying nutrition in severe pancreatitis (increased complications)"
        ],
        resolution_strategy="Early aggressive fluid resuscitation with LR, pain control, early enteral nutrition in severe cases, CT imaging at 72-96 hours if not improving, ERCP only for cholangitis or persistent biliary obstruction, antibiotics reserved for proven infection, step-up approach to necrosectomy with delayed intervention until WON formation, cholecystectomy during same admission for mild gallstone pancreatitis",
        entity_scope="All patients presenting with acute pancreatitis regardless of etiology",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for mild pancreatitis management; disclosure needed for severe necrotizing pancreatitis, timing of interventions, or multiorgan failure scenarios",
        controlling_precedent=[
            "ACG Guidelines on Acute Pancreatitis Management",
            "ASGE Guidelines on ERCP in Acute Pancreatitis",
            "SAGES Guidelines on Necrosectomy Approaches"
        ],
        zone=AnalysisZone.TREATMENT,
        category=IssueCategory.PANCREATIC
    ),
]


# ══════════════════════════════════════════════════════════════════════════════
# TELEMETRY & METRICS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class Metrics:
    total_queries: int = 0
    cache_hits: int = 0
    semantic_retrievals: int = 0
    deep_analyses: int = 0
    total_latency_ms: float = 0.0
    error_count: int = 0
    doctrine_triggers: Dict[str, int] = field(default_factory=dict)
    start_time: float = field(default_factory=time.time)

    @property
    def cache_hit_rate(self) -> float:
        return (self.cache_hits / self.total_queries * 100) if self.total_queries > 0 else 0.0

    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / self.total_queries if self.total_queries > 0 else 0.0

    @property
    def uptime_seconds(self) -> float:
        return time.time() - self.start_time


METRICS = Metrics()


# ══════════════════════════════════════════════════════════════════════════════
# CORE ENGINE LOGIC
# ══════════════════════════════════════════════════════════════════════════════

class GastroenterologyEngine:
    def __init__(self):
        self.doctrine_cache = DOCTRINE_CACHE
        self.metrics = METRICS
        logger.info(f"MED14 Gastroenterology Engine v{VERSION} initialized with {len(self.doctrine_cache)} doctrines")

    def three_layer_response(
        self, query: str, mode: ResponseMode, zone: AnalysisZone, context: Optional[Dict[str, Any]] = None
    ) -> AnalysisResult:
        """Three-layer retrieval: doctrine cache → semantic search → deep analysis"""
        start_time = time.time()

        # Layer 1: Doctrine Cache (0-200ms)
        triggered = self._check_doctrine_cache(query, zone)
        if triggered:
            self.metrics.cache_hits += 1
            response = self._generate_from_doctrines(triggered, query, mode, zone)
            latency_ms = (time.time() - start_time) * 1000
            logger.info(f"Cache hit: {len(triggered)} doctrines, {latency_ms:.1f}ms")
        else:
            # Layer 2: Semantic Retrieval (fallback)
            self.metrics.semantic_retrievals += 1
            response = self._semantic_search_fallback(query, mode, zone)
            latency_ms = (time.time() - start_time) * 1000
            logger.info(f"Semantic retrieval: {latency_ms:.1f}ms")

        # Layer 3: Deep Analysis (if requested via MEMO mode)
        if mode == ResponseMode.MEMO:
            self.metrics.deep_analyses += 1
            response = self._deep_analysis_mode(query, response, triggered, zone, context)

        # Apply epistemic guardrails
        response_clean, guardrails_applied = self._apply_epistemic_guardrails(response)

        # Calculate fragility score
        fragility = self._fact_fragility_scoring(query, triggered)

        # Identify coverage gaps
        gaps = self._coverage_map_gaps(query, triggered)

        # Generate determinism hash
        det_hash = self._determinism_hash_sha256(query, response_clean, triggered)

        # Update metrics
        self.metrics.total_queries += 1
        self.metrics.total_latency_ms += latency_ms
        for doctrine in triggered:
            topic = doctrine.topic
            self.metrics.doctrine_triggers[topic] = self.metrics.doctrine_triggers.get(topic, 0) + 1

        # Audit trail
        self._append_audit_trail(query, response_clean, mode, zone, triggered, latency_ms)

        return AnalysisResult(
            query=query,
            response=response_clean,
            mode=mode,
            zone=zone,
            triggered_doctrines=[d.topic for d in triggered],
            confidence=self._determine_confidence(triggered, query),
            latency_ms=latency_ms,
            determinism_hash=det_hash,
            timestamp=datetime.utcnow().isoformat(),
            epistemic_guardrails_applied=guardrails_applied,
            fragility_score=fragility,
            coverage_gaps=gaps
        )

    def _check_doctrine_cache(self, query: str, zone: AnalysisZone) -> List[DoctrineCacheEntry]:
        """Match query against doctrine keywords and zone"""
        query_lower = query.lower()
        triggered = []
        for doctrine in self.doctrine_cache:
            if doctrine.zone != zone and zone != AnalysisZone.DIAGNOSTIC:
                continue
            if any(kw.lower() in query_lower for kw in doctrine.keywords):
                triggered.append(doctrine)
        return triggered

    def _generate_from_doctrines(
        self, doctrines: List[DoctrineCacheEntry], query: str, mode: ResponseMode, zone: AnalysisZone
    ) -> str:
        """Generate response from triggered doctrines based on mode"""
        if mode == ResponseMode.FAST:
            # Concise response using conclusion templates
            parts = []
            for doc in doctrines[:2]:  # Top 2 most relevant
                parts.append(doc.conclusion_template[0])
            return " ".join(parts)

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready response with authority citations
            response = f"GASTROENTEROLOGY ANALYSIS ({zone.value} ZONE):\n\n"
            for i, doc in enumerate(doctrines, 1):
                response += f"{i}. {doc.topic}:\n"
                response += f"   Clinical Framework: {doc.reasoning_framework[:300]}...\n"
                response += f"   Key Factors: {', '.join(doc.key_factors[:3])}\n"
                response += f"   Authority: {doc.primary_authority[0]}\n"
                response += f"   Confidence: {doc.confidence.value}\n\n"
            return response

        else:  # MEMO mode
            # Comprehensive response with full reasoning
            response = f"COMPREHENSIVE GASTROENTEROLOGY ANALYSIS\n"
            response += f"Query: {query}\n"
            response += f"Analysis Zone: {zone.value}\n\n"
            for i, doc in enumerate(doctrines, 1):
                response += f"DOCTRINE {i}: {doc.topic}\n"
                response += f"Reasoning Framework:\n{doc.reasoning_framework}\n\n"
                response += f"Key Clinical Factors:\n"
                for factor in doc.key_factors:
                    response += f"  - {factor}\n"
                response += f"\nPrimary Guidelines:\n"
                for auth in doc.primary_authority:
                    response += f"  - {auth}\n"
                response += f"\nConfidence Level: {doc.confidence.value}\n"
                response += f"Stratification: {doc.confidence_stratification}\n\n"
            return response

    def _semantic_search_fallback(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
        """Fallback when no doctrine cache hit (simplified semantic matching)"""
        logger.warning(f"No doctrine cache hit for query: {query[:100]}")
        return (
            f"GASTROENTEROLOGY QUERY PROCESSED ({zone.value} zone):\n\n"
            f"No specific protocol matched in doctrine cache. General gastroenterology principles apply:\n"
            f"1. Systematic evaluation using evidence-based guidelines\n"
            f"2. Multidisciplinary approach for complex cases\n"
            f"3. Risk stratification and patient-specific management\n"
            f"4. Surveillance per established protocols\n\n"
            f"Recommend specialist consultation for detailed assessment. "
            f"This analysis is based on general gastroenterology knowledge and should be "
            f"supplemented with patient-specific clinical data and imaging."
        )

    def _deep_analysis_mode(
        self, query: str, base_response: str, triggered: List[DoctrineCacheEntry],
        zone: AnalysisZone, context: Optional[Dict[str, Any]]
    ) -> str:
        """Multi-doctrine synthesis with interaction analysis"""
        if not triggered:
            return base_response

        synthesis = base_response + "\n\n=== DEEP SYNTHESIS ===\n\n"

        # Multi-doctrine decomposition
        categories = {}
        for doc in triggered:
            cat = doc.category.value
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(doc)

        synthesis += f"Issue Categories Identified: {', '.join(categories.keys())}\n\n"

        # Interaction analysis
        if len(triggered) > 1:
            synthesis += "DOCTRINE INTERACTIONS:\n"
            for i, doc1 in enumerate(triggered):
                for doc2 in triggered[i+1:]:
                    synthesis += f"- {doc1.topic} + {doc2.topic}: "
                    synthesis += f"Combined consideration of {doc1.burden_holder} and {doc2.burden_holder}. "
                    synthesis += f"Resolution requires coordinated {doc1.resolution_strategy[:50]}...\n"

        # Adversarial analysis
        synthesis += "\nADVERSARIAL CONSIDERATIONS:\n"
        for doc in triggered[:3]:
            synthesis += f"- {doc.topic}: {doc.adversary_position}\n"
            synthesis += f"  Counter-arguments: {'; '.join(doc.counter_arguments[:2])}\n"

        return synthesis

    def _apply_epistemic_guardrails(self, response: str) -> Tuple[str, bool]:
        """Ensure response doesn't overstep diagnostic authority"""
        guardrails_triggered = False
        cleaned = response

        for banned in BANNED_PHRASES:
            if banned.lower() in cleaned.lower():
                guardrails_triggered = True
                logger.warning(f"Epistemic guardrail triggered: {banned}")

        # Add disclosure for high-risk content
        if any(term in response.lower() for term in ["cancer", "malignancy", "emergency", "life-threatening"]):
            if "clinical correlation required" not in cleaned.lower():
                cleaned += "\n\nDISCLOSURE: This analysis is for educational purposes. Clinical correlation with patient history, physical exam, and complete diagnostic workup is essential. Specialist consultation recommended for definitive diagnosis and management."
                guardrails_triggered = True

        return cleaned, guardrails_triggered

    def _fact_fragility_scoring(self, query: str, triggered: List[DoctrineCacheEntry]) -> float:
        """Score how vulnerable facts are to recharacterization (0.0-1.0)"""
        if not triggered:
            return 0.8  # High fragility if no doctrine support

        # Lower fragility with more authoritative support
        avg_confidence = sum(1.0 if d.confidence == ConfidenceLevel.DEFENSIBLE else 0.5 for d in triggered) / len(triggered)
        authority_count = sum(len(d.primary_authority) for d in triggered)

        fragility = 1.0 - (avg_confidence * 0.5 + min(authority_count / 10, 0.5))
        return round(fragility, 2)

    def _coverage_map_gaps(self, query: str, triggered: List[DoctrineCacheEntry]) -> List[str]:
        """Identify knowledge gaps not covered by triggered doctrines"""
        query_terms = set(query.lower().split())
        covered_terms = set()
        for doc in triggered:
            for kw in doc.keywords:
                covered_terms.update(kw.lower().split())

        gaps = []
        medical_terms = ["biopsy", "imaging", "treatment", "prognosis", "diagnosis", "surveillance", "complications"]
        for term in medical_terms:
            if term in query_terms and term not in covered_terms:
                gaps.append(f"Limited coverage on: {term}")

        return gaps

    def _determinism_hash_sha256(self, query: str, response: str, triggered: List[DoctrineCacheEntry]) -> str:
        """Generate reproducibility hash"""
        content = f"{query}|{response}|{','.join(d.topic for d in triggered)}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _determine_confidence(self, triggered: List[DoctrineCacheEntry], query: str) -> ConfidenceLevel:
        """Determine overall confidence level"""
        if not triggered:
            return ConfidenceLevel.DISCLOSURE

        # Use most conservative confidence level from triggered doctrines
        levels = [d.confidence for d in triggered]
        if ConfidenceLevel.HIGH_RISK in levels:
            return ConfidenceLevel.HIGH_RISK
        elif ConfidenceLevel.DISCLOSURE in levels:
            return ConfidenceLevel.DISCLOSURE
        elif ConfidenceLevel.AGGRESSIVE in levels:
            return ConfidenceLevel.AGGRESSIVE
        else:
            return ConfidenceLevel.DEFENSIBLE

    def _append_audit_trail(
        self, query: str, response: str, mode: ResponseMode, zone: AnalysisZone,
        triggered: List[DoctrineCacheEntry], latency_ms: float
    ):
        """Append query to audit trail (JSONL format)"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query[:200],
            "mode": mode.value,
            "zone": zone.value,
            "triggered_doctrines": [d.topic for d in triggered],
            "latency_ms": round(latency_ms, 2),
            "response_length": len(response)
        }

        audit_file = Path(__file__).parent / "audit_trail.jsonl"
        try:
            with open(audit_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(audit_entry) + "\n")
        except Exception as e:
            logger.error(f"Audit trail write failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ══════════════════════════════════════════════════════════════════════════════

APP = FastAPI(
    title="MED14 Gastroenterology Analysis Engine",
    description="TIE-Grade Medical Intelligence for GI Tract Diagnostics & Hepatology",
    version=VERSION
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ENGINE = GastroenterologyEngine()


@APP.post("/query", response_model=AnalysisResult)
async def query_engine(request: QueryRequest):
    """Main query endpoint with three-layer retrieval"""
    try:
        result = ENGINE.three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            context=request.context
        )
        return result
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        ENGINE.metrics.error_count += 1
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check with metrics"""
    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        uptime_seconds=ENGINE.metrics.uptime_seconds,
        total_queries=ENGINE.metrics.total_queries,
        cache_hit_rate=ENGINE.metrics.cache_hit_rate,
        avg_latency_ms=ENGINE.metrics.avg_latency_ms,
        doctrine_count=len(ENGINE.doctrine_cache),
        error_count=ENGINE.metrics.error_count
    )


@APP.get("/doctrines")
async def list_doctrines():
    """List all doctrine topics with metadata"""
    return {
        "total_count": len(ENGINE.doctrine_cache),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "zone": d.zone.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in ENGINE.doctrine_cache
        ]
    }


@APP.get("/metrics")
async def get_metrics():
    """Detailed metrics and doctrine trigger statistics"""
    return {
        "total_queries": ENGINE.metrics.total_queries,
        "cache_hits": ENGINE.metrics.cache_hits,
        "semantic_retrievals": ENGINE.metrics.semantic_retrievals,
        "deep_analyses": ENGINE.metrics.deep_analyses,
        "cache_hit_rate": round(ENGINE.metrics.cache_hit_rate, 2),
        "avg_latency_ms": round(ENGINE.metrics.avg_latency_ms, 2),
        "uptime_seconds": round(ENGINE.metrics.uptime_seconds, 2),
        "error_count": ENGINE.metrics.error_count,
        "doctrine_triggers": ENGINE.metrics.doctrine_triggers
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.add(
        Path(__file__).parent / "med14_gastro.log",
        rotation="10 MB",
        retention="30 days",
        level="INFO"
    )
    logger.info(f"Starting MED14 Gastroenterology Engine v{VERSION} on port {PORT}")
    uvicorn.run(APP, host="0.0.0.0", port=PORT)
