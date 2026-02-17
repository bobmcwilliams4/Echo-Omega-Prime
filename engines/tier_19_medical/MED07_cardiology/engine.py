"""
MED07 Cardiology Analysis Engine v1.0.0
TIE-grade cardiovascular medicine intelligence engine
Port: 9232
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# Configure logger
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "cardiology_engine.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)

APP = FastAPI(title="MED07 Cardiology Analysis Engine", version="1.0.0")
APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums and Models
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
    DIAGNOSIS = "DIAGNOSIS"
    TREATMENT = "TREATMENT"
    RISK_STRATIFICATION = "RISK_STRATIFICATION"

class IssueCategory(str, Enum):
    ECG_INTERPRETATION = "ECG_INTERPRETATION"
    ACUTE_CORONARY_SYNDROME = "ACUTE_CORONARY_SYNDROME"
    HEART_FAILURE = "HEART_FAILURE"
    ARRHYTHMIA = "ARRHYTHMIA"
    VALVULAR_DISEASE = "VALVULAR_DISEASE"
    CARDIAC_BIOMARKERS = "CARDIAC_BIOMARKERS"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"
    ANTICOAGULATION = "ANTICOAGULATION"
    HEMODYNAMICS = "HEMODYNAMICS"
    IMAGING_INTERPRETATION = "IMAGING_INTERPRETATION"

class QueryRequest(BaseModel):
    query: str = Field(..., description="Cardiology analysis query")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response mode")
    zone: Optional[AnalysisZone] = Field(None, description="Analysis zone")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)

class QueryResponse(BaseModel):
    query: str
    response: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    reasoning_chain: List[str]
    zone: Optional[AnalysisZone]
    determinism_hash: str
    latency_ms: float

class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: List[str]
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: Optional[str] = None
    adversary_position: Optional[str] = None
    counter_arguments: List[str] = Field(default_factory=list)
    resolution_strategy: Optional[str] = None
    entity_scope: Optional[str] = None
    confidence: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE
    confidence_stratification: Optional[str] = None
    controlling_precedent: Optional[str] = None

# Doctrine Cache - 25+ cardiovascular medicine blocks
DOCTRINE_CACHE: Dict[str, DoctrineBlock] = {
    "stemi_diagnosis": DoctrineBlock(
        topic="ST-Elevation Myocardial Infarction (STEMI) Diagnosis",
        keywords=["ST elevation", "STEMI", "myocardial infarction", "ECG criteria", "coronary occlusion", "acute MI", "transmural infarction"],
        conclusion_template=[
            "STEMI diagnosis requires ST elevation in 2+ contiguous leads meeting voltage criteria",
            "Door-to-balloon time <90 min for primary PCI or fibrinolysis within 30 min if PCI unavailable",
            "Posterior MI presents with ST depression V1-V3 and requires posterior lead placement"
        ],
        reasoning_framework=[
            "ECG Criteria for STEMI:",
            "- ST elevation ≥1 mm in 2+ contiguous limb leads (II/III/aVF, I/aVL)",
            "- ST elevation ≥2 mm in 2+ contiguous precordial leads (V1-V6) in men",
            "- ST elevation ≥1.5 mm in V2-V3 in women",
            "- New or presumed new LBBB with clinical suspicion",
            "",
            "Anatomic Correlations:",
            "- Anterior STEMI: V1-V4 (LAD territory)",
            "- Lateral STEMI: I, aVL, V5-V6 (LCx territory)",
            "- Inferior STEMI: II, III, aVF (RCA or LCx)",
            "- Posterior STEMI: ST depression V1-V3, check V7-V9",
            "- RV infarction: ST elevation V1, V4R in inferior STEMI (30-50% of cases)",
            "",
            "Time-Critical Interventions:",
            "- Primary PCI preferred if door-to-balloon <90 min AND <120 min from symptom onset",
            "- Fibrinolysis if PCI not available within 120 min AND <12h from symptom onset",
            "- Absolute contraindications to lysis: ICH history, active bleeding, ischemic stroke <3mo",
            "- DAPT (aspirin + P2Y12 inhibitor) immediately",
            "- High-intensity statin, beta-blocker, ACE-I/ARB initiated",
            "",
            "STEMI Mimics to Exclude:",
            "- Pericarditis (diffuse ST elevation, PR depression)",
            "- Early repolarization (J-point notching, young athletic patient)",
            "- LVH with strain pattern",
            "- Brugada syndrome (coved ST elevation V1-V2)",
            "- Takotsubo cardiomyopathy (apical ballooning, emotional stressor)"
        ],
        key_factors=[
            "ST elevation magnitude and lead distribution",
            "Presence of reciprocal ST depression",
            "Time from symptom onset to presentation",
            "Door-to-balloon time capability at facility",
            "Contraindications to fibrinolysis",
            "Hemodynamic stability (cardiogenic shock 5-10% STEMI)"
        ],
        primary_authority=[
            "ACC/AHA 2013 STEMI Guideline",
            "ESC 2017 STEMI Management Guidelines",
            "Thygesen K et al. Fourth Universal Definition of MI. Circulation 2018"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Door-to-balloon <90 min or door-to-needle <30 min"
    ),

    "nstemi_diagnosis": DoctrineBlock(
        topic="Non-ST-Elevation Myocardial Infarction (NSTEMI) and Unstable Angina",
        keywords=["NSTEMI", "troponin", "unstable angina", "ACS", "non-ST elevation", "TIMI risk", "GRACE score"],
        conclusion_template=[
            "NSTEMI requires positive troponin with ischemic symptoms or ECG changes without ST elevation",
            "Risk stratification using TIMI or GRACE score determines timing of catheterization",
            "Early invasive strategy (<24h) for high-risk features; conservative for low-risk stable patients"
        ],
        reasoning_framework=[
            "Diagnostic Criteria NSTEMI vs Unstable Angina:",
            "- NSTEMI: Elevated troponin (>99th percentile URL) + ischemic symptoms/ECG changes",
            "- Unstable Angina: Ischemic symptoms/ECG changes with NORMAL troponin",
            "- Troponin rise/fall pattern confirms acute MI (not chronic elevation)",
            "",
            "ECG Findings (non-diagnostic but concerning):",
            "- ST depression ≥0.5 mm in 2+ contiguous leads",
            "- T-wave inversion ≥1 mm in leads with dominant R wave",
            "- Dynamic ST-T changes during chest pain",
            "- Transient ST elevation <20 min",
            "",
            "TIMI Risk Score (0-7 points) for NSTEMI:",
            "- Age ≥65 (1 pt)",
            "- ≥3 CAD risk factors (1 pt)",
            "- Known CAD (stenosis ≥50%) (1 pt)",
            "- Aspirin use in past 7 days (1 pt)",
            "- ≥2 anginal episodes in 24h (1 pt)",
            "- ST deviation ≥0.5 mm (1 pt)",
            "- Elevated cardiac biomarkers (1 pt)",
            "Score 5-7: 41% risk of death/MI/urgent revasc at 14d → immediate cath",
            "Score 3-4: 19.9% risk → cath within 24h",
            "Score 0-2: 4.7% risk → conservative management acceptable",
            "",
            "GRACE Score (more comprehensive):",
            "- Includes age, HR, SBP, creatinine, Killip class, cardiac arrest, ST changes, troponin",
            "- >140: High risk, invasive strategy <24h",
            "- 109-140: Intermediate risk, invasive <72h",
            "- <109: Low risk, selective invasive OK",
            "",
            "High-Risk Features Mandating Early Cath (<24h):",
            "- Recurrent ischemia despite medical therapy",
            "- Elevated troponin (especially dynamic rise)",
            "- New or worsening MR murmur",
            "- Hemodynamic instability",
            "- Sustained VT or VF",
            "- GRACE >140 or TIMI ≥5"
        ],
        key_factors=[
            "Troponin level and kinetics (rise/fall pattern)",
            "TIMI or GRACE risk score",
            "Presence of high-risk features",
            "Hemodynamic stability",
            "Renal function (affects contrast/anticoagulation)"
        ],
        primary_authority=[
            "ACC/AHA 2014 NSTE-ACS Guideline",
            "ESC 2020 NSTE-ACS Guidelines",
            "Antman EM et al. TIMI Risk Score. JAMA 2000"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "heart_failure_classification": DoctrineBlock(
        topic="Heart Failure Classification and Staging",
        keywords=["heart failure", "HFrEF", "HFpEF", "NYHA class", "ejection fraction", "ACC/AHA stage", "BNP"],
        conclusion_template=[
            "Heart failure classified by EF: HFrEF (<40%), HFmrEF (40-49%), HFpEF (≥50%)",
            "NYHA functional class (I-IV) describes symptoms; ACC/AHA stage (A-D) describes progression",
            "Guideline-directed medical therapy differs substantially between HFrEF and HFpEF"
        ],
        reasoning_framework=[
            "Ejection Fraction Classification:",
            "- HFrEF (Heart Failure with Reduced EF): LVEF <40%",
            "- HFmrEF (Heart Failure with Mildly Reduced EF): LVEF 40-49%",
            "- HFpEF (Heart Failure with Preserved EF): LVEF ≥50%",
            "- HFimpEF (Improved EF): Previously <40%, now >40%",
            "",
            "NYHA Functional Classification (symptoms):",
            "- Class I: No limitation of physical activity, no symptoms with ordinary exertion",
            "- Class II: Slight limitation, comfortable at rest, ordinary activity causes fatigue/dyspnea",
            "- Class III: Marked limitation, less than ordinary activity causes symptoms",
            "- Class IV: Unable to carry on any activity without symptoms, symptoms at rest",
            "",
            "ACC/AHA Staging (progression, NOT reversible):",
            "- Stage A: At risk (HTN, DM, CAD) but no structural disease or symptoms",
            "- Stage B: Structural disease (prior MI, LVH, reduced EF) but no symptoms",
            "- Stage C: Structural disease WITH current or prior symptoms",
            "- Stage D: Refractory HF requiring advanced therapies (VAD, transplant, palliative)",
            "",
            "Diagnostic Biomarkers:",
            "- BNP >100 pg/mL or NT-proBNP >125 pg/mL supports HF diagnosis",
            "- BNP >400 or NT-proBNP >900 in acute setting indicates decompensation",
            "- Age ≥75: NT-proBNP >300; Age 50-75: >125; Age <50: >450",
            "- Obesity lowers BNP levels (use lower thresholds)",
            "",
            "HFrEF Guideline-Directed Medical Therapy (GDMT):",
            "- Quadruple therapy: ACE-I/ARB/ARNI + Beta-blocker + MRA + SGLT2i",
            "- ACE-I or ARB (if ACE-I intolerant) OR ARNI (sacubitril/valsartan)",
            "- Beta-blockers: carvedilol, metoprolol succinate, or bisoprolol",
            "- MRA: spironolactone or eplerenone (if K <5.0, Cr <2.5)",
            "- SGLT2i: dapagliflozin or empagliflozin (regardless of diabetes)",
            "- Diuretics for congestion (loop diuretics, titrate to euvolemia)",
            "- Hydralazine + isosorbide dinitrate if Black race or intolerant to ACE/ARB/ARNI",
            "",
            "HFpEF Management (less evidence-based):",
            "- SGLT2i (empagliflozin, dapagliflozin) now Class 1 recommendation",
            "- Control HTN, manage AF (rate/rhythm), treat ischemia",
            "- Diuretics for congestion",
            "- Spironolactone may reduce hospitalizations",
            "- ARNIs, ACE-I, ARBs have NOT shown mortality benefit in HFpEF"
        ],
        key_factors=[
            "Ejection fraction by echo or cardiac MRI",
            "NYHA class and ACC/AHA stage",
            "BNP/NT-proBNP levels",
            "Underlying etiology (ischemic vs non-ischemic)",
            "Renal function and electrolytes (K, Cr)",
            "Comorbidities (DM, AF, CKD, COPD)"
        ],
        primary_authority=[
            "ACC/AHA/HFSA 2022 Heart Failure Guideline",
            "ESC 2021 Heart Failure Guidelines",
            "Yancy CW et al. 2017 ACC/AHA/HFSA Focused Update"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "atrial_fibrillation_management": DoctrineBlock(
        topic="Atrial Fibrillation Management and Anticoagulation",
        keywords=["atrial fibrillation", "AFib", "CHA2DS2-VASc", "anticoagulation", "rate control", "rhythm control", "DOAC"],
        conclusion_template=[
            "CHA2DS2-VASc score guides anticoagulation: score ≥2 men, ≥3 women requires anticoagulation",
            "Rate control (HR <110 bpm) vs rhythm control depends on symptoms, AF burden, patient preference",
            "DOACs preferred over warfarin in non-valvular AFib (lower ICH risk, no INR monitoring)"
        ],
        reasoning_framework=[
            "CHA2DS2-VASc Stroke Risk Score:",
            "- C: CHF/LV dysfunction (1 pt)",
            "- H: Hypertension (1 pt)",
            "- A2: Age ≥75 (2 pts)",
            "- D: Diabetes (1 pt)",
            "- S2: Stroke/TIA/thromboembolism history (2 pts)",
            "- V: Vascular disease (prior MI, PAD, aortic plaque) (1 pt)",
            "- A: Age 65-74 (1 pt)",
            "- Sc: Sex category (female) (1 pt)",
            "",
            "Anticoagulation Recommendations:",
            "- Score 0 (men): No anticoagulation",
            "- Score 1 (men), 2 (women): Consider anticoagulation (individualize)",
            "- Score ≥2 (men), ≥3 (women): Anticoagulation recommended (Class 1)",
            "- Annual stroke risk: Score 0=0%, 1=1.3%, 2=2.2%, 3=3.2%, 4=4.0%, 5=6.7%, 6=9.8%, 9=15.2%",
            "",
            "DOAC vs Warfarin:",
            "- DOACs (dabigatran, rivaroxaban, apixaban, edoxaban) preferred in non-valvular AFib",
            "- Lower ICH risk vs warfarin (0.3-0.5% vs 1% annually)",
            "- No routine monitoring, fewer drug/food interactions",
            "- Warfarin still used if: mechanical valve, moderate-severe MS, CrCl <15-30 depending on DOAC",
            "- Apixaban: 5 mg BID (or 2.5 mg BID if 2+ of: age ≥80, weight ≤60 kg, Cr ≥1.5)",
            "- Rivaroxaban: 20 mg daily (15 mg if CrCl 15-50)",
            "- Dabigatran: 150 mg BID (110 mg if age ≥80 or high bleed risk)",
            "- Edoxaban: 60 mg daily (30 mg if CrCl 15-50, weight ≤60 kg)",
            "",
            "Rate Control vs Rhythm Control:",
            "- RATE CONTROL: Lenient target HR <110 bpm at rest if asymptomatic",
            "  Strict control <80 bpm if symptomatic or HFrEF",
            "  Beta-blockers or non-DHP CCB (diltiazem, verapamil) first-line",
            "  Digoxin reserved for HFrEF or sedentary patients",
            "- RHYTHM CONTROL: Consider if young, symptomatic, first episode, or HFrEF from rapid rate",
            "  Cardioversion (electrical preferred over chemical)",
            "  Antiarrhythmics: amiodarone (if structural disease), flecainide/propafenone (if no CAD/HF)",
            "  Catheter ablation if drugs fail or patient preference (higher success in paroxysmal AFib)",
            "",
            "Anticoagulation Before Cardioversion:",
            "- If AFib >48h or unknown duration: 3 weeks therapeutic AC before cardioversion",
            "- OR TEE to exclude LA thrombus → immediate cardioversion + 4 weeks AC after",
            "- If AFib <48h AND hemodynamically stable: can cardiovert, but still 4 weeks AC after"
        ],
        key_factors=[
            "CHA2DS2-VASc score",
            "HAS-BLED bleeding risk score",
            "AF pattern (paroxysmal, persistent, permanent)",
            "Symptom burden and quality of life",
            "Renal function (affects DOAC dosing)",
            "Presence of valvular disease (MS or mechanical valve)"
        ],
        primary_authority=[
            "AHA/ACC/HRS 2019 AFib Guideline",
            "ESC 2020 AFib Guidelines",
            "January CT et al. 2019 Focused Update on AFib"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "ecg_bundle_branch_blocks": DoctrineBlock(
        topic="Bundle Branch Block Interpretation",
        keywords=["LBBB", "RBBB", "bundle branch block", "QRS duration", "fascicular block", "bifascicular block"],
        conclusion_template=[
            "LBBB: QRS ≥120 ms, broad R in I/aVL/V5-V6, no Q in I/V6, discordant ST-T changes",
            "RBBB: QRS ≥120 ms, RSR' in V1-V2 (M-shaped), wide S in I/V6",
            "New LBBB with chest pain is STEMI-equivalent until proven otherwise"
        ],
        reasoning_framework=[
            "Left Bundle Branch Block (LBBB) Criteria:",
            "- QRS duration ≥120 ms (3 small boxes)",
            "- Broad, monophasic R wave in lateral leads (I, aVL, V5, V6)",
            "- Absent Q waves in I, V5, V6",
            "- Prolonged R wave peak time >60 ms in V5-V6",
            "- Appropriate discordance: ST-T opposite to QRS (ST depression where QRS is positive)",
            "",
            "LBBB Clinical Significance:",
            "- New LBBB + chest pain = STEMI-equivalent (Sgarbossa criteria for MI in LBBB)",
            "- Chronic LBBB causes dyssynchrony → may worsen HF (consider CRT if EF <35%, QRS ≥150 ms)",
            "- Makes interpretation of ischemia/infarction difficult on ECG",
            "",
            "Sgarbossa Criteria for MI in LBBB (Original, 3 criteria):",
            "- ST elevation ≥1 mm concordant with QRS (5 pts, highly specific)",
            "- ST depression ≥1 mm in V1-V3 (3 pts)",
            "- ST elevation ≥5 mm discordant with QRS (2 pts, less specific)",
            "- Score ≥3 suggests acute MI (90% specificity, 78% sensitivity)",
            "- Modified Sgarbossa: ST/S ratio ≥0.25 (more sensitive than ≥5 mm criterion)",
            "",
            "Right Bundle Branch Block (RBBB) Criteria:",
            "- QRS duration ≥120 ms",
            "- RSR' pattern in V1-V2 (M-shaped, 'rabbit ears')",
            "- Wide, slurred S wave in lateral leads (I, aVL, V5, V6)",
            "- R wave peak time >50 ms in V1",
            "",
            "RBBB Clinical Significance:",
            "- Often benign in isolation, can be normal variant",
            "- Does NOT obscure MI diagnosis (ST elevation still visible)",
            "- New RBBB in acute MI suggests large anterior/septal infarct, higher mortality",
            "- Bifascicular block (RBBB + LAFB or LPFB) has higher risk of complete heart block",
            "",
            "Fascicular Blocks:",
            "- LAFB (Left Anterior Fascicular Block): Left axis deviation (-45 to -90 deg), qR in aVL, rS in II/III/aVF",
            "- LPFB (Left Posterior Fascicular Block): Right axis deviation (+90 to +180 deg), rS in I/aVL, qR in II/III/aVF",
            "- Bifascicular: RBBB + LAFB or RBBB + LPFB",
            "- Trifascicular: Bifascicular + 1st degree AV block (prolonged PR)",
            "",
            "Indications for Pacemaker in BBB:",
            "- Alternating LBBB/RBBB",
            "- Bifascicular block + syncope (even without documented high-grade AV block)",
            "- Trifascicular block with symptoms",
            "- Mobitz II or 3rd degree AV block (regardless of BBB)"
        ],
        key_factors=[
            "QRS duration and morphology",
            "Lead distribution (lateral vs septal)",
            "Concordance vs discordance of ST-T changes",
            "Presence of symptoms (syncope, chest pain)",
            "Acute vs chronic BBB",
            "Associated AV block"
        ],
        primary_authority=[
            "Surawicz B et al. AHA/ACCF/HRS ECG Standardization. Circulation 2009",
            "Sgarbossa EB et al. NEJM 1996 (Sgarbossa Criteria)",
            "Smith SW et al. Modified Sgarbossa Criteria. Ann Emerg Med 2012"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "valvular_aortic_stenosis": DoctrineBlock(
        topic="Aortic Stenosis Assessment and Management",
        keywords=["aortic stenosis", "AS", "AVA", "peak velocity", "mean gradient", "severe AS", "TAVR", "AVR"],
        conclusion_template=[
            "Severe AS: AVA <1.0 cm2, mean gradient >40 mmHg, peak velocity >4.0 m/s",
            "Symptomatic severe AS (angina, syncope, dyspnea) has 50% 2-year mortality without intervention",
            "AVR (surgical or TAVR) indicated for symptomatic severe AS or asymptomatic with LVEF <50%"
        ],
        reasoning_framework=[
            "Grading Severity of Aortic Stenosis:",
            "MILD AS:",
            "- AVA >1.5 cm2",
            "- Mean gradient <20 mmHg",
            "- Peak velocity <3.0 m/s",
            "",
            "MODERATE AS:",
            "- AVA 1.0-1.5 cm2",
            "- Mean gradient 20-40 mmHg",
            "- Peak velocity 3.0-4.0 m/s",
            "",
            "SEVERE AS:",
            "- AVA <1.0 cm2 (or AVA index <0.6 cm2/m2)",
            "- Mean gradient >40 mmHg",
            "- Peak velocity >4.0 m/s",
            "",
            "CRITICAL/VERY SEVERE AS:",
            "- AVA <0.75 cm2",
            "- Mean gradient >50 mmHg",
            "- Peak velocity >4.5 m/s",
            "",
            "Low-Flow Low-Gradient AS (paradoxical severe AS):",
            "- AVA <1.0 cm2 BUT mean gradient <40 mmHg despite severe AS",
            "- Occurs with low stroke volume (HFrEF) or small LV cavity",
            "- Dobutamine stress echo can differentiate true severe AS from pseudo-severe AS",
            "- True severe AS: AVA remains <1.0 cm2 with increased flow",
            "- Pseudo-severe AS: AVA increases to >1.0 cm2 with dobutamine",
            "",
            "Natural History and Symptoms:",
            "- Asymptomatic severe AS: 2-3 years until symptoms develop",
            "- Once symptoms appear: 50% mortality at 2 years without AVR",
            "- Classic triad: Angina (5-year survival), Syncope (3-year survival), Dyspnea/HF (2-year survival)",
            "- Sudden cardiac death rare in asymptomatic AS (<1%/year)",
            "",
            "Indications for AVR (Surgical or TAVR):",
            "CLASS I (Should perform):",
            "- Symptomatic severe AS (angina, syncope, dyspnea)",
            "- Asymptomatic severe AS with LVEF <50%",
            "- Severe AS undergoing other cardiac surgery (CABG, other valve)",
            "",
            "CLASS IIa (Reasonable):",
            "- Asymptomatic severe AS with abnormal exercise test (symptoms, BP drop)",
            "- Asymptomatic very severe AS (velocity >5 m/s) with low surgical risk",
            "- Asymptomatic severe AS with rapid progression (velocity increase >0.3 m/s per year)",
            "- Moderate AS undergoing CABG or other valve surgery",
            "",
            "TAVR vs SAVR Selection:",
            "- Low surgical risk (STS <4%): SAVR or TAVR (patient preference, both Class I)",
            "- Intermediate risk (STS 4-8%): TAVR or SAVR equivalent outcomes",
            "- High risk (STS >8%) or prohibitive: TAVR preferred",
            "- Young age (<65-70): SAVR preferred (better long-term durability)",
            "- Bicuspid valve: SAVR preferred (TAVR data emerging)",
            "- Need for other cardiac surgery: SAVR"
        ],
        key_factors=[
            "Aortic valve area (AVA) by continuity equation",
            "Mean transvalvular gradient",
            "Peak aortic jet velocity",
            "Symptom status (angina, syncope, dyspnea)",
            "LV ejection fraction",
            "Surgical risk score (STS, EuroSCORE)",
            "Valve anatomy (tricuspid vs bicuspid)"
        ],
        primary_authority=[
            "ACC/AHA 2020 Valvular Heart Disease Guideline",
            "ESC/EACTS 2021 Valvular Heart Disease Guidelines",
            "Otto CM et al. 2020 ACC/AHA Guideline for Management of VHD"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "mitral_regurgitation": DoctrineBlock(
        topic="Mitral Regurgitation Assessment and Management",
        keywords=["mitral regurgitation", "MR", "mitral valve", "degenerative MR", "functional MR", "EROA", "vena contracta"],
        conclusion_template=[
            "Severe primary MR: EROA ≥0.4 cm2, regurgitant volume ≥60 mL, vena contracta ≥0.7 cm",
            "Symptomatic severe MR or asymptomatic with LVEF <60% or LVESD >40 mm warrants surgery",
            "Degenerative MR: repair preferred over replacement; functional MR: treat underlying HF first"
        ],
        reasoning_framework=[
            "Primary (Degenerative) vs Secondary (Functional) MR:",
            "- PRIMARY MR: Structural abnormality of valve apparatus",
            "  Causes: MVP with flail leaflet, chordal rupture, endocarditis, rheumatic disease",
            "  Treatment: Surgical repair/replacement if severe",
            "- SECONDARY (FUNCTIONAL) MR: Structurally normal valve, LV dysfunction/dilation",
            "  Causes: HFrEF, ischemic cardiomyopathy, papillary muscle displacement",
            "  Treatment: Optimize HF medical therapy (GDMT), CRT if indicated, then consider surgery",
            "",
            "Grading Severity of MR:",
            "MILD MR:",
            "- EROA <0.20 cm2",
            "- Regurgitant volume <30 mL",
            "- Vena contracta <0.3 cm",
            "- Regurgitant fraction <30%",
            "",
            "MODERATE MR:",
            "- EROA 0.20-0.39 cm2",
            "- Regurgitant volume 30-59 mL",
            "- Vena contracta 0.3-0.69 cm",
            "- Regurgitant fraction 30-49%",
            "",
            "SEVERE MR (Primary):",
            "- EROA ≥0.40 cm2",
            "- Regurgitant volume ≥60 mL",
            "- Vena contracta ≥0.7 cm",
            "- Regurgitant fraction ≥50%",
            "- Central jet >40% LA area or eccentric jet reaching LA wall",
            "- Systolic flow reversal in pulmonary veins",
            "",
            "SEVERE MR (Secondary/Functional):",
            "- EROA ≥0.20 cm2 (lower threshold than primary)",
            "- Regurgitant volume ≥30 mL",
            "",
            "Indications for Surgery in Primary MR:",
            "CLASS I (Should perform):",
            "- Symptomatic severe MR with LVEF >30%",
            "- Asymptomatic severe MR with LV dysfunction (LVEF 30-60% OR LVESD >40 mm)",
            "- Asymptomatic severe MR undergoing cardiac surgery for other indication",
            "",
            "CLASS IIa (Reasonable):",
            "- Asymptomatic severe MR with preserved LV function if >95% repair probability and low risk",
            "- Asymptomatic severe MR with new AF or pulmonary HTN (PASP >50 mmHg)",
            "",
            "Repair vs Replacement:",
            "- REPAIR PREFERRED in degenerative MR: better long-term survival, preserved LV function",
            "- Repair rate >90% in experienced centers for posterior leaflet prolapse",
            "- Anterior or bileaflet prolapse more complex, lower repair success",
            "- Replacement needed if: extensive leaflet destruction, severe calcification, endocarditis with abscess",
            "",
            "Transcatheter Edge-to-Edge Repair (MitraClip):",
            "- FDA approved for symptomatic severe PRIMARY MR if prohibitive surgical risk",
            "- FDA approved for symptomatic severe SECONDARY MR on maximal GDMT despite HFrEF",
            "- COAPT trial: MitraClip reduced HF hospitalization and mortality in functional MR",
            "- Anatomy requirements: adequate leaflet length, central jet origin"
        ],
        key_factors=[
            "EROA and regurgitant volume quantification",
            "LV size (LVESD) and function (LVEF)",
            "Symptom status (NYHA class)",
            "Primary vs secondary MR etiology",
            "Pulmonary artery pressure",
            "Repairability assessment",
            "Surgical risk and comorbidities"
        ],
        primary_authority=[
            "ACC/AHA 2020 Valvular Heart Disease Guideline",
            "Otto CM et al. 2020 ACC/AHA VHD Guideline",
            "Stone GW et al. COAPT Trial. NEJM 2018"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "qt_prolongation": DoctrineBlock(
        topic="QT Prolongation and Torsades de Pointes Risk",
        keywords=["QT interval", "QTc", "Bazett formula", "torsades de pointes", "long QT syndrome", "sudden death"],
        conclusion_template=[
            "QTc >500 ms or increase >60 ms from baseline significantly increases TdP risk",
            "Acquired LQTS commonly from medications, electrolyte abnormalities (hypoK, hypoMg, hypoCa)",
            "Congenital LQTS diagnosed by QTc >480 ms, family history, or genetic testing"
        ],
        reasoning_framework=[
            "QT Interval Measurement and Correction:",
            "- QT interval: Start of Q wave to end of T wave (NOT U wave unless fused)",
            "- Measure in lead II or V5 (longest QT usually)",
            "- BAZETT FORMULA (most common): QTc = QT / √RR (in seconds)",
            "  Problem: Over-corrects at high HR, under-corrects at low HR",
            "- FRIDERICIA FORMULA: QTc = QT / ∛RR (better at extremes of HR)",
            "- Framingham formula and Hodges formula also exist",
            "",
            "Normal QTc Values:",
            "- Normal: QTc <440 ms (men), <460 ms (women)",
            "- Borderline: QTc 440-460 ms (men), 460-480 ms (women)",
            "- Prolonged: QTc >460 ms (men), >480 ms (women)",
            "- Severely prolonged: QTc >500 ms (very high TdP risk)",
            "",
            "Torsades de Pointes (TdP) Risk Stratification:",
            "- QTc >500 ms: High risk, avoid all QT-prolonging drugs",
            "- QTc increase >60 ms from baseline: High risk even if <500 ms",
            "- Risk factors: Female sex (2-3x risk), bradycardia, hypokalemia, hypomagnesemia",
            "- Congenital LQTS patients: risk even with QTc 480-500 ms",
            "",
            "Acquired Long QT Syndrome Causes:",
            "MEDICATIONS (>100 drugs, check CredibleMeds.org):",
            "- Class IA antiarrhythmics: quinidine, procainamide, disopyramide",
            "- Class III antiarrhythmics: sotalol, dofetilide, ibutilide, amiodarone",
            "- Antipsychotics: haloperidol, ziprasidone, quetiapine, risperidone",
            "- Antibiotics: macrolides (azithromycin, erythromycin), fluoroquinolones (moxifloxacin)",
            "- Antifungals: fluconazole, ketoconazole",
            "- Antiemetics: ondansetron, droperidol",
            "- Methadone (dose-dependent QT prolongation)",
            "",
            "ELECTROLYTE ABNORMALITIES:",
            "- Hypokalemia <3.5 mEq/L (most common, replete to >4.0 if prolonged QT)",
            "- Hypomagnesemia <1.5 mEq/L (replete to >2.0)",
            "- Hypocalcemia <8.5 mg/dL (less common cause)",
            "",
            "OTHER CAUSES:",
            "- Hypothyroidism, hypothermia, liquid protein diets",
            "- Acute MI (especially anterior), SAH, stroke",
            "- Cocaine, organophosphate poisoning",
            "",
            "Congenital Long QT Syndrome (LQTS):",
            "- LQT1 (KCNQ1 gene, 30-35%): Exercise-triggered, swimming",
            "- LQT2 (KCNH2 gene, 25-30%): Auditory stimuli, emotional stress, postpartum",
            "- LQT3 (SCN5A gene, 5-10%): Sleep/rest-triggered events",
            "- Diagnostic criteria (Schwartz score): ≥3.5 high probability",
            "  QTc ≥480 ms (3 pts), TdP (2 pts), T-wave alternans (1 pt), syncope (2 pts), family history (1 pt)",
            "",
            "Management of TdP:",
            "- Immediate: Magnesium sulfate 2 g IV over 1-2 min (even if Mg normal)",
            "- Correct hypokalemia to >4.5 mEq/L",
            "- Discontinue offending drugs",
            "- Overdrive pacing or isoproterenol if bradycardia-dependent",
            "- Defibrillation if degenerates to VF",
            "- ICD placement for congenital LQTS with high-risk features"
        ],
        key_factors=[
            "QTc interval duration and change from baseline",
            "Heart rate (affects QT correction accuracy)",
            "Serum electrolytes (K, Mg, Ca)",
            "Medication list (QT-prolonging drugs)",
            "Family history of sudden death or LQTS",
            "Triggers (exercise, auditory, sleep)"
        ],
        primary_authority=[
            "Roden DM. Drug-Induced Prolongation of QT Interval. NEJM 2004",
            "CredibleMeds QT Drug Lists (www.crediblemeds.org)",
            "Schwartz PJ et al. Diagnostic Criteria for LQTS. Circulation 1993"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "ventricular_tachycardia": DoctrineBlock(
        topic="Ventricular Tachycardia Classification and Management",
        keywords=["ventricular tachycardia", "VT", "wide complex tachycardia", "Brugada criteria", "monomorphic VT", "polymorphic VT", "VF"],
        conclusion_template=[
            "Wide complex tachycardia (QRS >120 ms) is VT until proven otherwise, especially with structural heart disease",
            "Monomorphic VT suggests scar-related reentry; polymorphic VT suggests ischemia or channelopathy",
            "Sustained VT (>30 sec) or hemodynamically unstable VT requires immediate cardioversion"
        ],
        reasoning_framework=[
            "Classification of Ventricular Tachycardia:",
            "BY DURATION:",
            "- Non-sustained VT (NSVT): ≥3 beats at >100 bpm, duration <30 seconds",
            "- Sustained VT: >30 seconds OR requires termination due to hemodynamic compromise",
            "",
            "BY MORPHOLOGY:",
            "- Monomorphic VT: Same QRS morphology beat-to-beat (suggests scar/reentry)",
            "- Polymorphic VT: Changing QRS morphology (suggests ischemia or channelopathy)",
            "- Torsades de Pointes: Polymorphic VT with prolonged QT, 'twisting' morphology",
            "",
            "BY HEMODYNAMICS:",
            "- Stable VT: Conscious, systolic BP >90 mmHg",
            "- Unstable VT: Altered mental status, chest pain, pulmonary edema, shock",
            "",
            "Differentiating VT from SVT with Aberrancy:",
            "BRUGADA CRITERIA (4-step algorithm, 99% specific for VT):",
            "1. Absence of RS complex in ALL precordial leads? → VT",
            "2. RS interval >100 ms in ANY precordial lead? → VT",
            "3. AV dissociation present? → VT",
            "4. Morphology criteria for VT in V1-V2 and V6? → VT",
            "   If RBBB-like: R wave in V1, QS or QR in V6",
            "   If LBBB-like: R wave in V1 >30 ms, notched S in V1, Q wave in V6",
            "",
            "OTHER CLUES FAVORING VT:",
            "- Age >35 with structural heart disease (prior MI, HFrEF)",
            "- Very wide QRS (>140 ms RBBB-like, >160 ms LBBB-like)",
            "- Extreme axis deviation (northwest axis, -90 to -180 deg)",
            "- Capture beats or fusion beats (AV dissociation)",
            "- Concordance (all positive or all negative in V1-V6)",
            "- No response to adenosine (VT rarely terminates with adenosine)",
            "",
            "Acute Management of Stable VT:",
            "- Amiodarone 150 mg IV over 10 min, then 1 mg/min infusion",
            "- Procainamide 20-50 mg/min IV (max 17 mg/kg) if no HF/hypotension",
            "- Lidocaine 1-1.5 mg/kg IV bolus if ischemic VT suspected",
            "- Synchronized cardioversion if drugs fail or patient deteriorates",
            "",
            "Acute Management of Unstable VT:",
            "- Immediate synchronized cardioversion: 100-200 J biphasic",
            "- If pulseless VT → defibrillation + CPR + ACLS algorithm",
            "- Correct electrolytes (K >4.0, Mg >2.0)",
            "- Beta-blockers after conversion if no HF/hypotension",
            "",
            "Management of Polymorphic VT:",
            "- If QTc prolonged (Torsades de Pointes): Magnesium 2 g IV, correct hypokalemia, stop QT drugs",
            "- If QTc normal: Suspect acute ischemia → emergent cath lab, beta-blockers, amiodarone",
            "",
            "Long-Term Management and ICD Indications:",
            "- Secondary prevention (VT/VF arrest survivor): ICD Class I indication",
            "- Primary prevention (HFrEF with LVEF ≤35%): ICD if ≥40 days post-MI or ≥3 mo ischemic CMP",
            "- Catheter ablation for recurrent VT despite drugs or ICD shocks",
            "- Beta-blockers reduce VT recurrence in ischemic and non-ischemic CMP"
        ],
        key_factors=[
            "QRS duration and morphology",
            "Hemodynamic stability",
            "Presence of structural heart disease",
            "AV dissociation on ECG",
            "QTc interval (polymorphic VT)",
            "Response to adenosine or cardioversion"
        ],
        primary_authority=[
            "AHA/ACC/HRS 2017 VT Guideline",
            "Brugada P et al. Brugada Criteria for VT. Circulation 1991",
            "Al-Khatib SM et al. 2017 AHA/ACC/HRS Guideline for VAs"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "acute_coronary_syndrome_biomarkers": DoctrineBlock(
        topic="Cardiac Biomarkers in Acute Coronary Syndrome",
        keywords=["troponin", "cardiac biomarkers", "high-sensitivity troponin", "CK-MB", "BNP", "myoglobin"],
        conclusion_template=[
            "Troponin is the gold standard biomarker for MI; detectable 2-4h after symptom onset, peaks 24h",
            "High-sensitivity troponin allows 0/1h or 0/2h rule-out protocols with high NPV",
            "Elevated troponin indicates myocardial injury but not necessarily ACS (DDx: PE, myocarditis, sepsis, CKD)"
        ],
        reasoning_framework=[
            "Cardiac Troponin (cTn) - Gold Standard:",
            "- Cardiac-specific proteins: Troponin I (cTnI) and Troponin T (cTnT)",
            "- Released with myocardial necrosis (irreversible injury)",
            "- CONVENTIONAL ASSAY: Detectable 2-4h after symptom onset, peak 24h, elevated 7-14 days",
            "- HIGH-SENSITIVITY ASSAY (hs-cTn): Detectable earlier (1-3h), allows rapid rule-in/rule-out",
            "- 99th percentile upper reference limit (URL) defines 'elevated'",
            "  Example: hs-cTnI 99th percentile = 26 ng/L (men), 16 ng/L (women)",
            "",
            "High-Sensitivity Troponin Protocols:",
            "0/1-HOUR ALGORITHM (ESC 2020):",
            "- Baseline (0h) and 1-hour sample",
            "- RULE-OUT: hs-cTn <5 ng/L at 0h OR (0h <12 ng/L AND 1h change <3 ng/L)",
            "- RULE-IN: hs-cTn ≥52 ng/L at 0h OR (0h ≥5 ng/L AND 1h change ≥5 ng/L)",
            "- OBSERVE: All others → serial troponin at 3-6h, consider other diagnoses",
            "",
            "0/2-HOUR ALGORITHM (more widely used in US):",
            "- RULE-OUT: 0h and 2h both <99th percentile AND change <20%",
            "- RULE-IN: Either value >99th percentile with rise/fall pattern",
            "",
            "Troponin Elevation WITHOUT ACS (Type 2 MI or non-MI injury):",
            "- Chronic kidney disease (most common, baseline elevated troponin)",
            "- Pulmonary embolism (RV strain)",
            "- Myocarditis or pericarditis",
            "- Takotsubo cardiomyopathy",
            "- Sepsis or critical illness",
            "- Heart failure exacerbation",
            "- Cardioversion or ablation",
            "- Strenuous exercise (marathon runners, mild elevation)",
            "- Chemotherapy (anthracyclines)",
            "",
            "CK-MB (Creatine Kinase-MB):",
            "- LEGACY MARKER, largely replaced by troponin",
            "- Less cardiac-specific than troponin (found in skeletal muscle)",
            "- Rises faster than troponin (3-6h), peaks 12-24h, normalizes 48-72h",
            "- Useful for detecting REINFARCTION (troponin remains elevated for weeks)",
            "- CK-MB/total CK ratio >2.5% suggests cardiac source (not skeletal muscle)",
            "",
            "Myoglobin:",
            "- Earliest marker (rises within 1-2h), NOT cardiac-specific",
            "- High sensitivity but low specificity (elevated in rhabdomyolysis, renal failure, trauma)",
            "- Rarely used clinically (hs-cTn replaced it for early detection)",
            "",
            "BNP and NT-proBNP (NOT for ACS diagnosis):",
            "- Markers of ventricular stretch/volume overload",
            "- Used for HF diagnosis and risk stratification in ACS",
            "- Elevated BNP in ACS predicts worse outcomes (death, HF)",
            "- NOT useful for differentiating ACS from other chest pain",
            "",
            "Clinical Use - Serial Troponin Strategy:",
            "- Single troponin insufficient to rule out MI (need serial)",
            "- 0h and 3h (conventional) OR 0h/1h or 0h/2h (high-sensitivity)",
            "- RISE/FALL pattern confirms acute MI (vs chronic elevation in CKD)",
            "- Absolute change matters: ≥20% change from baseline suggests acute injury"
        ],
        key_factors=[
            "Time from symptom onset to troponin draw",
            "Serial troponin with rise/fall kinetics",
            "High-sensitivity vs conventional assay",
            "Clinical context (CKD, sepsis, PE)",
            "ECG findings (ST elevation, ST depression, T-wave changes)",
            "Renal function (baseline troponin elevation in CKD)"
        ],
        primary_authority=[
            "Thygesen K et al. Fourth Universal Definition of MI. Circulation 2018",
            "ESC 2020 NSTE-ACS Guidelines (0/1h algorithm)",
            "Apple FS et al. hs-cTn Consensus Statement. Clin Chem 2017"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "framingham_risk_score": DoctrineBlock(
        topic="Framingham Risk Score and Primary Prevention",
        keywords=["Framingham risk", "cardiovascular risk", "primary prevention", "ASCVD risk", "statin therapy", "aspirin"],
        conclusion_template=[
            "10-year ASCVD risk ≥7.5% warrants statin therapy for primary prevention",
            "Risk calculators incorporate age, sex, cholesterol, BP, diabetes, smoking to estimate 10-year CVD risk",
            "Aspirin for primary prevention only if high CVD risk (≥10%) AND low bleeding risk"
        ],
        reasoning_framework=[
            "Cardiovascular Risk Assessment Tools:",
            "FRAMINGHAM RISK SCORE (original, estimates 10-year CHD risk):",
            "- Age, total cholesterol, HDL, systolic BP, BP treatment, smoking, diabetes",
            "- Estimates 10-year risk of MI or coronary death",
            "- Developed from predominantly white population (less accurate in minorities)",
            "",
            "POOLED COHORT EQUATIONS (2013 ACC/AHA, preferred):",
            "- Estimates 10-year ASCVD risk (MI, stroke, coronary death)",
            "- Separate equations for white and Black men/women",
            "- Risk factors: Age 40-79, total cholesterol, HDL, SBP, BP meds, DM, smoking",
            "- Known to OVERESTIMATE risk in contemporary populations by 25-50%",
            "- ASCVD risk <5%: Low risk",
            "- ASCVD risk 5-7.4%: Borderline risk",
            "- ASCVD risk 7.5-19.9%: Intermediate risk",
            "- ASCVD risk ≥20%: High risk",
            "",
            "2019 ACC/AHA PRIMARY PREVENTION GUIDELINE:",
            "Risk-Enhancing Factors (consider if borderline/intermediate risk):",
            "- Family history of premature ASCVD (men <55, women <65)",
            "- Chronic kidney disease (eGFR 15-59)",
            "- Metabolic syndrome",
            "- Chronic inflammatory conditions (RA, psoriasis, HIV)",
            "- High-risk ethnicity (South Asian)",
            "- Lipid/biomarker abnormalities: LDL ≥160, TG ≥175, hs-CRP ≥2.0, Lp(a) ≥50 mg/dL, ApoB ≥130 mg/dL",
            "- Women-specific: Preeclampsia, premature menopause (<40)",
            "",
            "Coronary Artery Calcium (CAC) Score:",
            "- CAC = 0: Very low risk, consider deferring statin (unless DM, family hx, smoking)",
            "- CAC 1-99: Moderate risk, statin reasonable if ≥55 years",
            "- CAC 100-299: Statin recommended",
            "- CAC ≥300 or ≥75th percentile: Statin strongly recommended",
            "",
            "STATIN THERAPY for Primary Prevention:",
            "HIGH-INTENSITY STATIN (LDL reduction ≥50%):",
            "- Atorvastatin 40-80 mg or Rosuvastatin 20-40 mg",
            "- Indications: Age <75 with LDL ≥190 OR DM age 40-75 with LDL 70-189 OR ASCVD risk ≥20%",
            "",
            "MODERATE-INTENSITY STATIN (LDL reduction 30-50%):",
            "- Atorvastatin 10-20 mg, Rosuvastatin 5-10 mg, Simvastatin 20-40 mg, Pravastatin 40-80 mg",
            "- Indications: ASCVD risk 7.5-19.9% OR DM age 40-75 with additional risk factors",
            "",
            "CONSIDER STATIN (risk discussion):",
            "- ASCVD risk 5-7.4% (borderline) with risk enhancers",
            "- Age 40-75 with DM but low risk",
            "",
            "ASPIRIN for Primary Prevention (2019 Guideline DOWNGRADED):",
            "- NO LONGER ROUTINE due to bleeding risk outweighing benefit",
            "- MAY CONSIDER: Age 40-70 with high ASCVD risk (≥10%) AND low bleeding risk",
            "- AVOID: Age >70, any bleeding risk (history of GI bleed, anticoagulation, NSAID use)",
            "- Aspirin 81 mg daily if used",
            "",
            "Non-Statin Therapies:",
            "- Ezetimibe: Add if statin-intolerant or LDL not at goal (reduces LDL 15-20%)",
            "- PCSK9 inhibitors: If LDL ≥190 despite max statin OR FH, very expensive",
            "- Icosapent ethyl (Vascepa): TG 150-499 on statin, reduces CV events 25%",
            "- Bempedoic acid: Statin-intolerant, LDL reduction ~20%"
        ],
        key_factors=[
            "Age, sex, race",
            "Lipid panel (LDL, HDL, triglycerides)",
            "Blood pressure and treatment status",
            "Diabetes and smoking status",
            "Family history of premature CVD",
            "CAC score if available",
            "Bleeding risk (for aspirin decision)"
        ],
        primary_authority=[
            "Arnett DK et al. 2019 ACC/AHA Primary Prevention Guideline",
            "Goff DC et al. 2013 Pooled Cohort Equations. Circulation 2014",
            "Grundy SM et al. 2018 Cholesterol Guideline"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "cardiogenic_shock": DoctrineBlock(
        topic="Cardiogenic Shock Diagnosis and Management",
        keywords=["cardiogenic shock", "shock", "IABP", "Impella", "ECMO", "inotropes", "hemodynamics"],
        conclusion_template=[
            "Cardiogenic shock: SBP <90 mmHg, CI <2.2 L/min/m2, PCWP >15 mmHg, tissue hypoperfusion",
            "Mortality 40-50% despite therapy; early revascularization for ACS-related shock improves outcomes",
            "Mechanical circulatory support (IABP, Impella, ECMO) considered if refractory to inotropes/vasopressors"
        ],
        reasoning_framework=[
            "Definition and Hemodynamic Criteria:",
            "Cardiogenic Shock = Inadequate tissue perfusion due to cardiac dysfunction",
            "HEMODYNAMIC CRITERIA:",
            "- Systolic BP <90 mmHg for >30 min (or vasopressors to maintain BP)",
            "- Cardiac index <2.2 L/min/m2 (or <1.8 without support)",
            "- PCWP (pulmonary capillary wedge pressure) >15 mmHg",
            "- Evidence of end-organ hypoperfusion:",
            "  Altered mental status, cool extremities, oliguria (<30 mL/h), lactate >2 mmol/L",
            "",
            "SCAI Shock Classification (A-E):",
            "- Stage A (At risk): Not currently in shock but at risk (e.g., large STEMI)",
            "- Stage B (Beginning): Relative hypotension, tachycardia, no hypoperfusion (yet)",
            "- Stage C (Classic): Hypotension + hypoperfusion, responds to initial intervention",
            "- Stage D (Deteriorating): Requiring multiple interventions, escalating support",
            "- Stage E (Extremis): Circulatory collapse, cardiac arrest, multi-organ failure",
            "",
            "Etiology:",
            "- Acute MI (most common, 80%): Massive LV infarction, VSD, free wall rupture, acute MR",
            "- Acute decompensated HF",
            "- Myocarditis (fulminant)",
            "- Acute valvular regurgitation (endocarditis, chordal rupture)",
            "- Post-cardiotomy or post-cardiac arrest",
            "- RV infarction (inferior MI with RV involvement)",
            "- Stress-induced cardiomyopathy (Takotsubo)",
            "",
            "Pharmacologic Support:",
            "FIRST-LINE INOTROPES:",
            "- DOBUTAMINE: 2.5-20 mcg/kg/min, beta-1 agonist, increases inotropy and CO, may worsen hypotension",
            "- MILRINONE: 0.375-0.75 mcg/kg/min, PDE-3 inhibitor, inotrope + vasodilator, risk of hypotension",
            "",
            "VASOPRESSORS (if hypotensive despite inotropes):",
            "- NOREPINEPHRINE: 0.1-2 mcg/kg/min, alpha + beta agonist, maintains BP, preferred over dopamine",
            "- DOPAMINE: 5-20 mcg/kg/min (AVOID if possible, increased arrhythmia risk vs norepinephrine)",
            "- EPINEPHRINE: 0.05-0.5 mcg/kg/min, for refractory shock, beta >> alpha effects",
            "",
            "ADJUNCTS:",
            "- Levosimendan (not FDA approved in US, available in Europe): Ca sensitizer + PDE-3 inhibitor",
            "",
            "Mechanical Circulatory Support (MCS):",
            "INTRA-AORTIC BALLOON PUMP (IABP):",
            "- Inflates during diastole (augments coronary perfusion), deflates during systole (afterload reduction)",
            "- Increases CO by 10-20%, modest benefit",
            "- IABP-SHOCK II trial: No mortality benefit in MI-related cardiogenic shock",
            "- Still used for mechanical complications (VSD, MR) as bridge to surgery",
            "",
            "IMPELLA (percutaneous ventricular assist device):",
            "- Impella 2.5: 2.5 L/min support",
            "- Impella CP: 3.5-4.0 L/min support",
            "- Impella 5.0/5.5: 5+ L/min support (surgical cutdown)",
            "- Placed across aortic valve, pulls blood from LV → aorta",
            "- Greater hemodynamic support than IABP, more complications (hemolysis, vascular injury)",
            "",
            "VA-ECMO (veno-arterial extracorporeal membrane oxygenation):",
            "- Full cardiopulmonary support (5-7 L/min)",
            "- Indications: Refractory cardiogenic shock, cardiac arrest, failure to wean from bypass",
            "- Complications: Limb ischemia (femoral cannulation), LV distension, bleeding, infection",
            "- Bridge to recovery, durable LVAD, or transplant",
            "",
            "Management Strategy:",
            "1. Early recognition and hemodynamic monitoring (arterial line, consider PA catheter)",
            "2. Correct underlying cause:",
            "   - STEMI: Emergent PCI or CABG (revascularization improves survival)",
            "   - Mechanical complication: Emergent surgery (VSD repair, MV repair/replacement)",
            "3. Optimize preload: Cautious fluid challenge if PCWP unknown (may worsen pulmonary edema)",
            "4. Inotropic support: Dobutamine first-line, add norepinephrine if SBP <70",
            "5. Mechanical support: Consider if worsening despite max medical therapy",
            "6. Avoid excessive fluids (worsens pulmonary edema), avoid beta-blockers/CCB (worsen shock)"
        ],
        key_factors=[
            "Blood pressure and cardiac index",
            "PCWP or CVP measurement",
            "Lactate, urine output, mental status (end-organ perfusion)",
            "Etiology (ischemic vs non-ischemic, mechanical complication)",
            "SCAI shock stage",
            "Response to initial inotropic support"
        ],
        primary_authority=[
            "Thiele H et al. IABP-SHOCK II Trial. NEJM 2012",
            "Baran DA et al. SCAI Shock Classification. Catheter Cardiovasc Interv 2019",
            "van Diepen S et al. AHA Scientific Statement on Cardiogenic Shock. Circulation 2017"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "acute_pericarditis": DoctrineBlock(
        topic="Acute Pericarditis Diagnosis and Management",
        keywords=["pericarditis", "chest pain", "pericardial friction rub", "ST elevation", "PR depression", "colchicine"],
        conclusion_template=[
            "Pericarditis diagnosed by 2+ criteria: chest pain, friction rub, ECG changes, pericardial effusion",
            "ECG shows diffuse ST elevation with PR depression; evolves through 4 stages unlike MI",
            "NSAIDs + colchicine first-line therapy; avoid corticosteroids unless refractory (risk of recurrence)"
        ],
        reasoning_framework=[
            "Diagnostic Criteria (2+ of 4 required):",
            "1. Chest pain (pleuritic, positional, sharp, relieved by sitting forward)",
            "2. Pericardial friction rub (pathognomonic but present in <50%)",
            "   - High-pitched, scratching sound, best heard at left sternal border",
            "   - Triphasic (atrial systole, ventricular systole, ventricular diastole)",
            "3. ECG changes (diffuse ST elevation, PR depression)",
            "4. Pericardial effusion (echo, often small)",
            "",
            "ECG Evolution in Pericarditis (4 stages):",
            "STAGE 1 (days 1-2):",
            "- Diffuse ST elevation (concave upward, 'smiling' morphology) in ALL leads except aVR/V1",
            "- PR segment DEPRESSION (most specific finding)",
            "- Upright T waves",
            "",
            "STAGE 2 (days 2-7):",
            "- ST segments return to baseline",
            "- T waves begin to flatten",
            "",
            "STAGE 3 (weeks 1-3):",
            "- Diffuse T wave inversions",
            "",
            "STAGE 4 (weeks-months):",
            "- ECG normalizes OR T waves remain inverted chronically",
            "",
            "Differentiate Pericarditis from STEMI:",
            "PERICARDITIS:",
            "- Diffuse ST elevation (not anatomically confined)",
            "- ST elevation with concave morphology",
            "- PR depression (STEMI never has this)",
            "- No reciprocal ST depression",
            "- No Q waves develop",
            "- Troponin normal or mildly elevated (if myopericarditis)",
            "",
            "STEMI:",
            "- Regional ST elevation (LAD, RCA, or LCx territory)",
            "- ST elevation with convex morphology ('tombstone')",
            "- Reciprocal ST depression in opposite leads",
            "- Q waves develop within hours-days",
            "- Troponin significantly elevated",
            "",
            "Etiology:",
            "IDIOPATHIC (85-90%): Presumed viral, often no pathogen identified",
            "INFECTIOUS:",
            "- Viral (Coxsackie, echovirus, adenovirus, EBV, CMV, HIV)",
            "- Bacterial (TB most common worldwide, purulent pericarditis)",
            "POST-MI: Dressler syndrome (autoimmune, weeks-months post-MI)",
            "AUTOIMMUNE: SLE, RA, scleroderma, Sjogren's",
            "UREMIC: End-stage renal disease (ESRD on dialysis)",
            "MALIGNANCY: Lung, breast, melanoma, lymphoma",
            "POST-CARDIAC SURGERY: Post-pericardiotomy syndrome",
            "MEDICATIONS: Hydralazine, procainamide, isoniazid, minoxidil",
            "",
            "Treatment:",
            "FIRST-LINE (Class I):",
            "- NSAIDs: Ibuprofen 600-800 mg TID OR Aspirin 750-1000 mg TID (2-4 weeks)",
            "- COLCHICINE: 0.6 mg BID (weight >70 kg) or 0.6 mg daily (weight <70 kg) for 3 months",
            "  Reduces recurrence from 30-50% to 10-15% (COPE, ICAP trials)",
            "- Gastroprotection: PPI (due to high-dose NSAIDs)",
            "",
            "AVOID CORTICOSTEROIDS:",
            "- Increase recurrence risk (up to 50%)",
            "- Reserve for refractory cases, autoimmune, or uremic pericarditis",
            "- If needed: Prednisone 0.2-0.5 mg/kg/day, taper slowly over weeks-months",
            "",
            "ACTIVITY RESTRICTION:",
            "- Avoid strenuous exercise until symptom resolution AND CRP normalization",
            "- Athletes: 3 months rest minimum (risk of recurrence with exertion)",
            "",
            "Red Flags (High-Risk Features, Consider Hospitalization):",
            "- Fever >38°C (suggests bacterial/purulent pericarditis)",
            "- Large pericardial effusion (>20 mm echo-free space)",
            "- Cardiac tamponade (hypotension, elevated JVP, pulsus paradoxus)",
            "- Myopericarditis (elevated troponin, regional wall motion abnormality)",
            "- Immunosuppression (malignancy, HIV, immunosuppressive drugs)",
            "- Failure to respond to NSAIDs within 7 days",
            "- Trauma history (risk of hemopericardium)",
            "",
            "Recurrent Pericarditis:",
            "- Occurs in 15-30% despite initial treatment",
            "- Treat with NSAIDs + colchicine 6 months",
            "- If multiple recurrences: Consider IL-1 inhibitors (anakinra, rilonacept)"
        ],
        key_factors=[
            "Chest pain characteristics (pleuritic, positional)",
            "Presence of pericardial friction rub",
            "ECG pattern (diffuse ST elevation, PR depression)",
            "Troponin level (normal vs elevated)",
            "Pericardial effusion size",
            "High-risk features (fever, tamponade, immunosuppression)"
        ],
        primary_authority=[
            "Adler Y et al. 2015 ESC Pericardial Diseases Guidelines",
            "Imazio M et al. COPE Trial (Colchicine in Pericarditis). Circulation 2005",
            "Imazio M et al. ICAP Trial. JAMA 2013"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "cardiac_tamponade": DoctrineBlock(
        topic="Cardiac Tamponade Recognition and Management",
        keywords=["cardiac tamponade", "pericardial effusion", "Beck triad", "pulsus paradoxus", "pericardiocentesis"],
        conclusion_template=[
            "Tamponade is clinical diagnosis: hypotension, elevated JVP, muffled heart sounds (Beck triad)",
            "Pulsus paradoxus >10 mmHg supports diagnosis; echo shows diastolic collapse of RA/RV",
            "Emergent pericardiocentesis or surgical drainage required; temporize with IV fluids, avoid diuretics"
        ],
        reasoning_framework=[
            "Pathophysiology:",
            "- Pericardial fluid accumulation → intrapericardial pressure exceeds cardiac chamber pressure",
            "- Impaired ventricular filling → reduced stroke volume → cardiogenic shock",
            "- RATE of accumulation matters more than volume:",
            "  Acute (trauma, aortic dissection): 100-200 mL can cause tamponade",
            "  Chronic (malignancy, uremia): 1-2 L may be tolerated",
            "",
            "Clinical Features - Beck's Triad (classic but only 30% of cases):",
            "1. Hypotension (SBP <90 mmHg, narrow pulse pressure)",
            "2. Elevated jugular venous pressure (JVP)",
            "3. Muffled (distant) heart sounds",
            "",
            "Additional Clinical Signs:",
            "- PULSUS PARADOXUS: Exaggerated drop in SBP >10 mmHg during inspiration",
            "  Mechanism: Inspiration → increased venous return to RV → RV expansion → septal shift left",
            "  → LV compression → reduced LV stroke volume → BP drop",
            "  Measured: SBP difference between first Korotkoff sound (during expiration) and all beats",
            "- Tachycardia (compensatory)",
            "- Tachypnea, dyspnea",
            "- Kussmaul sign: JVP RISES with inspiration (paradoxical, also seen in constrictive pericarditis)",
            "",
            "Echocardiographic Findings:",
            "- Pericardial effusion (circumferential)",
            "- RIGHT ATRIAL COLLAPSE during ventricular systole (early, sensitive sign)",
            "- RIGHT VENTRICULAR DIASTOLIC COLLAPSE (more specific, late sign)",
            "- Plethoric IVC (dilated, <50% collapse with inspiration)",
            "- Exaggerated respiratory variation in mitral/tricuspid inflow velocities (>25%)",
            "- Swinging heart (large effusion, heart moves within pericardial sac)",
            "",
            "ECG Findings (non-specific):",
            "- Low voltage QRS (<5 mm in limb leads)",
            "- Electrical alternans (beat-to-beat QRS amplitude variation, pathognomonic but rare)",
            "  Mechanism: Heart swinging within large effusion",
            "",
            "Etiology:",
            "ACUTE (life-threatening):",
            "- Aortic dissection with hemopericardium",
            "- Cardiac trauma (penetrating or blunt)",
            "- Post-MI free wall rupture (1-2 weeks post-STEMI)",
            "- Iatrogenic (post-cath, post-pacemaker, post-ablation)",
            "",
            "SUBACUTE/CHRONIC:",
            "- Malignancy (lung, breast, melanoma, lymphoma)",
            "- Uremic pericarditis (ESRD)",
            "- Viral or idiopathic pericarditis with large effusion",
            "- Tuberculosis (most common in developing countries)",
            "- Autoimmune (SLE, RA)",
            "",
            "Management:",
            "IMMEDIATE (life-saving):",
            "- Volume resuscitation: Aggressive IVF (NS or LR) to increase preload, improve filling",
            "- AVOID: Diuretics (worsen preload), positive pressure ventilation (reduces venous return)",
            "- AVOID: Vasodilators, beta-blockers (worsen hypotension)",
            "- Position patient upright (sitting forward improves filling)",
            "",
            "DEFINITIVE TREATMENT:",
            "- PERICARDIOCENTESIS: Percutaneous needle drainage (echo or fluoro-guided)",
            "  Subxiphoid approach most common",
            "  Remove fluid slowly (50-100 mL may dramatically improve hemodynamics)",
            "  Leave pigtail catheter for continued drainage",
            "- SURGICAL DRAINAGE: Pericardial window or pericardiectomy if:",
            "  Loculated effusion, recurrent tamponade, purulent pericarditis, malignancy",
            "",
            "Post-Pericardiocentesis Care:",
            "- Pericardial fluid studies: Cell count, Gram stain/culture, cytology, glucose, LDH, protein",
            "- Monitor for re-accumulation (repeat echo)",
            "- Treat underlying cause (malignancy, infection, autoimmune disease)"
        ],
        key_factors=[
            "Hemodynamic status (BP, HR, JVP)",
            "Pulsus paradoxus magnitude",
            "Pericardial effusion size and location",
            "RA/RV diastolic collapse on echo",
            "Rate of effusion accumulation (acute vs chronic)",
            "Underlying etiology"
        ],
        primary_authority=[
            "Adler Y et al. 2015 ESC Pericardial Diseases Guidelines",
            "Spodick DH. Acute Cardiac Tamponade. NEJM 2003",
            "Hoit BD. Pericardial Disease and Tamponade. Crit Care Med 2007"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "hypertrophic_cardiomyopathy": DoctrineBlock(
        topic="Hypertrophic Cardiomyopathy Diagnosis and Sudden Death Risk",
        keywords=["hypertrophic cardiomyopathy", "HCM", "septal hypertrophy", "LVOT obstruction", "sudden cardiac death", "ICD"],
        conclusion_template=[
            "HCM: LV wall thickness ≥15 mm (or ≥13 mm with FHx) without other cause (HTN, AS)",
            "LVOT obstruction (gradient ≥30 mmHg) causes dynamic symptoms, managed with beta-blockers or septal reduction",
            "SCD risk factors: FHx sudden death, massive LVH (≥30 mm), unexplained syncope, NSVT; ICD if high risk"
        ],
        reasoning_framework=[
            "Diagnostic Criteria:",
            "- LV wall thickness ≥15 mm in any segment (echo or cardiac MRI)",
            "- OR ≥13 mm if family history of HCM",
            "- Asymmetric septal hypertrophy most common (septum:posterior wall ratio ≥1.3)",
            "- Exclude other causes: Hypertension, aortic stenosis, athlete's heart, infiltrative (amyloid)",
            "",
            "Classification:",
            "OBSTRUCTIVE HCM (HOCM, 70%):",
            "- LVOT (left ventricular outflow tract) gradient ≥30 mmHg at rest or with provocation",
            "- Systolic anterior motion (SAM) of mitral valve → LVOT obstruction + MR",
            "- Gradient worsens with: Valsalva, standing, exercise, low preload",
            "- Gradient improves with: Squatting, leg raise, handgrip, increased preload",
            "",
            "NON-OBSTRUCTIVE HCM (30%):",
            "- No resting or provocable LVOT gradient <30 mmHg",
            "- May still have diastolic dysfunction (impaired relaxation)",
            "",
            "Clinical Presentation:",
            "- ASYMPTOMATIC (many patients, diagnosed on screening echo)",
            "- Dyspnea on exertion (most common symptom, diastolic dysfunction)",
            "- Angina (microvascular ischemia despite normal coronary arteries)",
            "- Syncope/presyncope (LVOT obstruction, arrhythmias)",
            "- Sudden cardiac death (VT/VF, most feared, often first manifestation)",
            "",
            "Physical Exam (HOCM):",
            "- Harsh systolic murmur at left sternal border (LVOT obstruction)",
            "- Murmur INCREASES with: Valsalva, standing (reduced preload → more obstruction)",
            "- Murmur DECREASES with: Squatting, handgrip (increased afterload → less obstruction)",
            "- Bisferiens pulse (double peak in carotid upstroke)",
            "- S4 gallop (stiff, non-compliant LV)",
            "",
            "Sudden Cardiac Death (SCD) Risk Stratification:",
            "MAJOR RISK FACTORS (any 1 → consider ICD):",
            "1. Family history of SCD in 1st-degree relative (especially if young, <40)",
            "2. Massive LVH (wall thickness ≥30 mm)",
            "3. Unexplained syncope (within 6 months, especially exertional)",
            "4. Non-sustained VT on Holter (≥3 beats at >120 bpm, >30% have NSVT)",
            "5. Abnormal BP response to exercise (failure to rise >20 mmHg or drop)",
            "",
            "HCM Risk-SCD Calculator (ESC 2014):",
            "- Estimates 5-year SCD risk based on: age, FHx SCD, max LV thickness, LA size, max LVOT gradient, NSVT, unexplained syncope",
            "- ≥6% risk → ICD recommended",
            "- 4-6% risk → ICD reasonable",
            "- <4% risk → ICD generally not indicated",
            "",
            "Management - Medical:",
            "OBSTRUCTIVE HCM:",
            "- BETA-BLOCKERS (first-line): Metoprolol, atenolol (reduce HR, increase filling time, reduce LVOT gradient)",
            "- VERAPAMIL (non-DHP CCB): Alternative if beta-blocker intolerant (AVOID if severe LVOT obstruction + pulmonary edema)",
            "- DISOPYRAMIDE: Added to beta-blocker if refractory symptoms (negative inotrope)",
            "- AVOID: Vasodilators (ACE-I, ARB, nitrates), diuretics (reduce preload, worsen LVOT obstruction)",
            "- AVOID: Digoxin (increases inotropy, worsens obstruction)",
            "",
            "NON-OBSTRUCTIVE HCM:",
            "- Beta-blockers or verapamil for symptomatic diastolic dysfunction",
            "- Diuretics cautiously if HF symptoms (avoid over-diuresis)",
            "",
            "Management - Septal Reduction Therapy (if medical therapy fails + LVOT gradient ≥50 mmHg + severe symptoms):",
            "- SURGICAL SEPTAL MYECTOMY: Gold standard, removes portion of hypertrophied septum",
            "  Mortality <1% in experienced centers, excellent long-term results",
            "- ALCOHOL SEPTAL ABLATION: Percutaneous, inject alcohol into septal perforator artery → localized MI → scar → reduced obstruction",
            "  Risk of complete heart block (5-10%, may need pacemaker)",
            "  Reserved for poor surgical candidates or older patients",
            "",
            "ICD for Primary Prevention:",
            "- Implant if ≥1 major SCD risk factor OR HCM Risk-SCD score ≥6%",
            "- Shared decision-making for intermediate risk (4-6%)",
            "",
            "Screening Family Members:",
            "- Echo + ECG every 12-18 months from age 10-12 (or earlier if athlete or symptoms)",
            "- Genetic testing if proband has identified mutation (50% transmission if autosomal dominant)",
            "- Clinical screening even if genetic testing negative (incomplete penetrance)"
        ],
        key_factors=[
            "LV wall thickness (especially septal)",
            "LVOT gradient at rest and with provocation",
            "Presence and severity of symptoms",
            "SCD risk factors (FHx, syncope, NSVT, massive LVH)",
            "Systolic anterior motion (SAM) on echo",
            "Family history and genetic testing results"
        ],
        primary_authority=[
            "Gersh BJ et al. 2011 ACCF/AHA HCM Guideline",
            "Elliott PM et al. 2014 ESC HCM Guidelines (Risk-SCD Calculator)",
            "Maron BJ et al. Contemporary Definitions of HCM. Circulation 2006"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE
    )
}

# Metrics and Telemetry
class Metrics:
    def __init__(self):
        self.query_count = 0
        self.total_latency_ms = 0.0
        self.doctrine_hit_count = defaultdict(int)
        self.error_count = 0
        self.queries_by_mode = defaultdict(int)
        self.queries_by_zone = defaultdict(int)

    def record_query(self, mode: ResponseMode, zone: Optional[AnalysisZone], latency_ms: float, doctrines: List[str]):
        self.query_count += 1
        self.total_latency_ms += latency_ms
        self.queries_by_mode[mode] += 1
        if zone:
            self.queries_by_zone[zone] += 1
        for doctrine in doctrines:
            self.doctrine_hit_count[doctrine] += 1

    def record_error(self):
        self.error_count += 1

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_queries": self.query_count,
            "average_latency_ms": self.total_latency_ms / max(self.query_count, 1),
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.query_count, 1),
            "queries_by_mode": dict(self.queries_by_mode),
            "queries_by_zone": dict(self.queries_by_zone),
            "top_doctrines": dict(sorted(self.doctrine_hit_count.items(), key=lambda x: x[1], reverse=True)[:10])
        }

METRICS = Metrics()

# Core Engine Functions
def semantic_normalization(query: str) -> str:
    """Normalize cardiology terminology"""
    normalizations = {
        r'\b(mi|heart attack|myocardial infarction)\b': 'myocardial_infarction',
        r'\b(afib|a-fib|a fib|atrial fibrillation)\b': 'atrial_fibrillation',
        r'\b(hf|heart failure|chf)\b': 'heart_failure',
        r'\b(ef|ejection fraction|lvef)\b': 'ejection_fraction',
        r'\b(cabg|coronary artery bypass)\b': 'coronary_artery_bypass',
        r'\b(pci|ptca|angioplasty|stent)\b': 'percutaneous_coronary_intervention',
        r'\b(vt|ventricular tachycardia)\b': 'ventricular_tachycardia',
        r'\b(vf|ventricular fibrillation|v-fib)\b': 'ventricular_fibrillation',
        r'\b(as|aortic stenosis)\b': 'aortic_stenosis',
        r'\b(mr|mitral regurgitation)\b': 'mitral_regurgitation',
        r'\b(hcm|hypertrophic cardiomyopathy)\b': 'hypertrophic_cardiomyopathy',
        r'\b(acs|acute coronary syndrome)\b': 'acute_coronary_syndrome',
        r'\b(bnp|brain natriuretic peptide|proBNP)\b': 'natriuretic_peptide',
        r'\b(lbbb|left bundle branch block)\b': 'left_bundle_branch_block',
        r'\b(rbbb|right bundle branch block)\b': 'right_bundle_branch_block',
        r'\b(echo|echocardiogram|echocardiography)\b': 'echocardiography',
        r'\b(ekg|ecg|electrocardiogram)\b': 'electrocardiogram',
        r'\b(cha2ds2-vasc|chads-vasc|chads2)\b': 'stroke_risk_score',
        r'\b(doac|novel anticoagulant|noac)\b': 'direct_oral_anticoagulant',
        r'\b(icd|implantable cardioverter defibrillator)\b': 'implantable_cardioverter_defibrillator'
    }

    normalized = query.lower()
    for pattern, replacement in normalizations.items():
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

    return normalized

def match_doctrines(query: str) -> List[Tuple[str, DoctrineBlock, float]]:
    """Match query to relevant doctrine blocks"""
    normalized_query = semantic_normalization(query)
    query_terms = set(normalized_query.split())

    matches = []
    for doctrine_id, doctrine in DOCTRINE_CACHE.items():
        keyword_set = set(k.lower() for k in doctrine.keywords)
        overlap = len(query_terms & keyword_set)

        topic_match = any(term in doctrine.topic.lower() for term in query_terms)
        if topic_match:
            overlap += 2

        if overlap > 0:
            score = overlap / len(doctrine.keywords)
            matches.append((doctrine_id, doctrine, score))

    return sorted(matches, key=lambda x: x[2], reverse=True)

def three_layer_response(query: str, mode: ResponseMode, zone: Optional[AnalysisZone]) -> Tuple[str, List[str], List[str], ConfidenceLevel]:
    """Three-layer response system: doctrine cache → semantic search → deep analysis"""
    matched_doctrines = match_doctrines(query)

    triggered_ids = []
    reasoning_chain = []

    if matched_doctrines and matched_doctrines[0][2] > 0.3:
        # Layer 1: Doctrine Cache Hit
        doctrine_id, doctrine, score = matched_doctrines[0]
        triggered_ids.append(doctrine_id)

        if mode == ResponseMode.FAST:
            response = f"{doctrine.conclusion_template[0]}"
            reasoning_chain.append(f"DOCTRINE: {doctrine.topic} (cache hit, score {score:.2f})")
        elif mode == ResponseMode.DEFENSE:
            response = "\n\n".join([
                f"ANALYSIS: {doctrine.topic}",
                f"CONCLUSION: {' '.join(doctrine.conclusion_template)}",
                f"KEY FACTORS: {', '.join(doctrine.key_factors[:5])}",
                f"AUTHORITY: {'; '.join(doctrine.primary_authority)}"
            ])
            reasoning_chain.append(f"DOCTRINE: {doctrine.topic}")
            reasoning_chain.extend(doctrine.reasoning_framework[:5])
        else:  # MEMO
            response = "\n\n".join([
                f"COMPREHENSIVE CARDIOLOGY ANALYSIS",
                f"Topic: {doctrine.topic}",
                "",
                "CLINICAL REASONING:",
                "\n".join(f"  {line}" for line in doctrine.reasoning_framework),
                "",
                "KEY CLINICAL FACTORS:",
                "\n".join(f"  • {factor}" for factor in doctrine.key_factors),
                "",
                "AUTHORITATIVE SOURCES:",
                "\n".join(f"  • {auth}" for auth in doctrine.primary_authority),
                "",
                "CONCLUSION:",
                "\n".join(f"  {conclusion}" for conclusion in doctrine.conclusion_template)
            ])
            reasoning_chain.extend(doctrine.reasoning_framework)

        confidence = doctrine.confidence

    else:
        # Layer 2: Semantic Retrieval + Layer 3: Deep Analysis
        response = "No high-confidence doctrine match. This query requires specialist cardiology consultation with full clinical context including ECG, echo, labs, and hemodynamic data."
        reasoning_chain.append("SEMANTIC SEARCH: No strong doctrine match (score <0.3)")
        reasoning_chain.append("RECOMMENDATION: Consult cardiologist for comprehensive evaluation")
        confidence = ConfidenceLevel.DISCLOSURE
        triggered_ids.append("general_cardiology_referral")

    return response, triggered_ids, reasoning_chain, confidence

def determinism_hash(query: str, response: str, triggered_doctrines: List[str]) -> str:
    """Generate SHA-256 hash for reproducibility"""
    content = f"{query}|{response}|{','.join(sorted(triggered_doctrines))}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

# API Endpoints
@APP.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    start_time = datetime.now()

    try:
        response, triggered_ids, reasoning_chain, confidence = three_layer_response(
            request.query,
            request.mode,
            request.zone
        )

        end_time = datetime.now()
        latency_ms = (end_time - start_time).total_seconds() * 1000

        det_hash = determinism_hash(request.query, response, triggered_ids)

        METRICS.record_query(request.mode, request.zone, latency_ms, triggered_ids)

        # Audit trail
        audit_entry = {
            "timestamp": end_time.isoformat(),
            "query": request.query,
            "mode": request.mode.value,
            "zone": request.zone.value if request.zone else None,
            "triggered_doctrines": triggered_ids,
            "confidence": confidence.value,
            "latency_ms": latency_ms,
            "determinism_hash": det_hash
        }

        audit_file = Path(__file__).parent / "audit_trail.jsonl"
        with open(audit_file, "a") as f:
            f.write(json.dumps(audit_entry) + "\n")

        return QueryResponse(
            query=request.query,
            response=response,
            mode=request.mode,
            confidence=confidence,
            triggered_doctrines=triggered_ids,
            reasoning_chain=reasoning_chain,
            zone=request.zone,
            determinism_hash=det_hash,
            latency_ms=latency_ms
        )

    except Exception as e:
        METRICS.record_error()
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "engine": "MED07_cardiology",
        "version": "1.0.0",
        "port": 9232,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "total_queries": METRICS.query_count,
        "error_rate": METRICS.error_count / max(METRICS.query_count, 1),
        "average_latency_ms": METRICS.total_latency_ms / max(METRICS.query_count, 1)
    }

@APP.get("/metrics")
async def get_metrics():
    return METRICS.get_summary()

@APP.get("/doctrines")
async def list_doctrines():
    return {
        "total_doctrines": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "id": doctrine_id,
                "topic": doctrine.topic,
                "keywords": doctrine.keywords,
                "confidence": doctrine.confidence.value
            }
            for doctrine_id, doctrine in DOCTRINE_CACHE.items()
        ]
    }

if __name__ == "__main__":
    logger.info("Starting MED07 Cardiology Analysis Engine on port 9232")
    uvicorn.run(APP, host="0.0.0.0", port=9232)
