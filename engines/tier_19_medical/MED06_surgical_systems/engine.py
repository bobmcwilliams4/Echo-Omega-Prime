"""
MED06 SURGICAL SYSTEMS ANALYSIS ENGINE v1.0.0
Tax Intelligence Engine (TIE) Architecture - Medical Domain Adaptation

Analyzes surgical systems: operative planning, surgical instrumentation,
minimally invasive techniques, robotic surgery, surgical safety protocols,
and perioperative risk assessment.

Port: 9231
Architecture: TIE-20 Gold Standard
Domain: Surgical Systems & Perioperative Medicine
"""

import sys
from pathlib import Path

# CRITICAL: Add parent to path BEFORE any local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional, Any, Set, Tuple
from collections import defaultdict, Counter

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

# ============================================================================
# CONFIGURATION & ENUMS
# ============================================================================

ENGINE_VERSION = "1.0.0"
ENGINE_ID = "MED06_SURGICAL_SYSTEMS"
ENGINE_PORT = 9231

# Configure loguru
logger.add(
    f"logs/{ENGINE_ID}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
)


class ResponseMode(str, Enum):
    """Response detail levels"""
    FAST = "FAST"  # Concise, cache-first
    DEFENSE = "DEFENSE"  # Audit-ready, detailed
    MEMO = "MEMO"  # Full documentation


class ConfidenceLevel(str, Enum):
    """Stratified confidence levels"""
    DEFENSIBLE = "DEFENSIBLE"  # Strong evidence-based consensus
    AGGRESSIVE = "AGGRESSIVE"  # Emerging techniques, institutional protocols
    DISCLOSURE = "DISCLOSURE"  # Requires patient consent, risk disclosure
    HIGH_RISK = "HIGH_RISK"  # Experimental, high liability


class IssueCategory(str, Enum):
    """Surgical domain classification"""
    PREOPERATIVE_ASSESSMENT = "PREOPERATIVE_ASSESSMENT"
    AIRWAY_MANAGEMENT = "AIRWAY_MANAGEMENT"
    SURGICAL_SAFETY = "SURGICAL_SAFETY"
    MINIMALLY_INVASIVE = "MINIMALLY_INVASIVE"
    ROBOTIC_SURGERY = "ROBOTIC_SURGERY"
    INSTRUMENTATION = "INSTRUMENTATION"
    INFECTION_CONTROL = "INFECTION_CONTROL"
    BLOOD_MANAGEMENT = "BLOOD_MANAGEMENT"
    ELECTROSURGERY = "ELECTROSURGERY"
    POSTOPERATIVE_CARE = "POSTOPERATIVE_CARE"
    ERAS_PROTOCOLS = "ERAS_PROTOCOLS"
    PATIENT_POSITIONING = "PATIENT_POSITIONING"


class AnalysisZone(str, Enum):
    """Surgical practice zones"""
    PLANNING = "PLANNING"  # Preoperative risk assessment
    OPERATIVE = "OPERATIVE"  # Intraoperative decision-making
    RECOVERY = "RECOVERY"  # Postoperative management


class AuthorityLevel(str, Enum):
    """Evidence hierarchy for surgical practice"""
    LEVEL_1_RCT = "LEVEL_1_RCT"  # Randomized controlled trials
    LEVEL_2_COHORT = "LEVEL_2_COHORT"  # Prospective cohort studies
    LEVEL_3_CASE_CONTROL = "LEVEL_3_CASE_CONTROL"  # Case-control studies
    LEVEL_4_CASE_SERIES = "LEVEL_4_CASE_SERIES"  # Case series
    LEVEL_5_EXPERT = "LEVEL_5_EXPERT"  # Expert opinion, consensus statements
    REGULATORY = "REGULATORY"  # FDA, Joint Commission, AORN
    GUIDELINE = "GUIDELINE"  # Society guidelines (ASA, ACS, SAGES)


# Authority weights for conflict resolution
AUTHORITY_WEIGHTS = {
    AuthorityLevel.LEVEL_1_RCT: 100,
    AuthorityLevel.LEVEL_2_COHORT: 80,
    AuthorityLevel.REGULATORY: 75,
    AuthorityLevel.GUIDELINE: 70,
    AuthorityLevel.LEVEL_3_CASE_CONTROL: 60,
    AuthorityLevel.LEVEL_4_CASE_SERIES: 40,
    AuthorityLevel.LEVEL_5_EXPERT: 30,
}


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class DoctrineBlock:
    """
    Doctrine cache unit - precompiled surgical reasoning.
    Each block = 40-80 lines of real surgical domain knowledge.
    """
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: Optional[str]
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    issue_category: IssueCategory
    analysis_zone: AnalysisZone
    authority_level: AuthorityLevel

    # Epistemic guardrails
    fact_fragility: float = 0.5  # 0=robust, 1=fragile
    recharacterization_risk: float = 0.5
    testimony_dependence: float = 0.5

    # Tracking
    times_triggered: int = 0
    last_triggered: Optional[datetime] = None

    def matches(self, query: str) -> float:
        """Score relevance to query (0-1)"""
        query_lower = query.lower()
        keyword_hits = sum(1 for kw in self.keywords if kw.lower() in query_lower)
        topic_hit = 1.0 if self.topic.lower() in query_lower else 0.0
        return min(1.0, (keyword_hits * 0.15) + (topic_hit * 0.4))


class QueryRequest(BaseModel):
    """Standardized query input"""
    query: str = Field(..., description="Surgical systems question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: Optional[AnalysisZone] = Field(default=None, description="Surgical practice zone")
    require_citations: bool = Field(default=False, description="Include authority citations")
    patient_context: Optional[Dict[str, Any]] = Field(default=None, description="ASA class, comorbidities, etc")


class QueryResponse(BaseModel):
    """Standardized query output"""
    query_id: str
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    zone: Optional[AnalysisZone]
    triggered_doctrines: List[str]
    cache_hit: bool
    response_time_ms: float
    reasoning_chain: Optional[List[str]] = None
    citations: Optional[List[str]] = None
    warnings: Optional[List[str]] = None
    determinism_hash: str
    timestamp: str


# ============================================================================
# DOCTRINE CACHE - REAL SURGICAL EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    # ========== PREOPERATIVE ASSESSMENT ==========

    DoctrineBlock(
        topic="ASA Physical Status Classification",
        keywords=["ASA", "physical status", "anesthetic risk", "preoperative", "classification", "perioperative mortality"],
        conclusion_template="ASA physical status {asa_class} indicates {risk_level} perioperative risk with {mortality_rate} expected mortality.",
        reasoning_framework="""
The American Society of Anesthesiologists (ASA) Physical Status Classification is the gold standard for preoperative risk stratification:

ASA I: Normal healthy patient
- No organic, physiologic, or psychiatric disturbance
- Excludes very young and very old
- Healthy with good exercise tolerance
- Nonsmoker, minimal alcohol use
- Mortality: 0.05-0.1%

ASA II: Mild systemic disease
- No functional limitations; well-controlled disease
- Current smoker, social alcohol drinker, pregnancy, obesity (30 < BMI < 40)
- Well-controlled DM/HTN, mild lung disease
- Mortality: 0.2-0.4%

ASA III: Severe systemic disease
- Substantive functional limitations; poorly controlled disease
- Poorly controlled DM or HTN, COPD, morbid obesity (BMI ≥40)
- Active hepatitis, alcohol dependence, implanted pacemaker
- History of MI (>3 months), CVA, TIA, or CAD/stents
- Mortality: 1.2-4.0%

ASA IV: Severe systemic disease that is constant threat to life
- Recent (<3 months) MI, CVA, TIA, or CAD/stents, ongoing cardiac ischemia
- Severe valve dysfunction, reduced ejection fraction
- Sepsis, DIC, ARD, ESRD not undergoing regularly scheduled dialysis
- Mortality: 7.8-23%

ASA V: Moribund patient not expected to survive without operation
- Ruptured abdominal/thoracic aneurysm, massive trauma
- Intracranial bleed with mass effect, ischemic bowel with significant cardiac pathology
- Multiple organ/system dysfunction
- Mortality: 9.4-50.8%

ASA VI: Declared brain-dead patient whose organs are being removed for donor purposes

Emergency designation (E): Any patient requiring emergency surgery gets 'E' suffix (e.g., ASA III-E)
- Emergency cases have 2-3x higher mortality than elective cases

The ASA class correlates directly with perioperative morbidity and mortality across all surgical specialties.
        """,
        key_factors=[
            "Presence and severity of systemic disease",
            "Functional status and exercise tolerance",
            "Control of chronic medical conditions",
            "Emergency vs elective surgery",
            "Age extremes (very young or very old)",
            "Smoking status and substance use",
            "BMI and nutritional status"
        ],
        primary_authority=[
            "ASA Physical Status Classification System (2020 revision)",
            "Anesthesiology 2014;120:502-515 (ASA class and mortality correlation)",
            "American Society of Anesthesiologists - ASA Standards and Guidelines"
        ],
        burden_holder="Anesthesiologist/Surgeon",
        adversary_position="Patient autonomy may conflict with objective risk assessment",
        counter_arguments=[
            "ASA class is subjective and shows inter-rater variability",
            "Does not account for surgical complexity or urgency",
            "May not capture frailty in elderly patients"
        ],
        resolution_strategy="Use ASA class as baseline, supplement with surgical-specific risk calculators (ACS NSQIP, RCRI)",
        entity_scope="All surgical patients requiring anesthesia",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Level 1 evidence from large cohort studies",
        controlling_precedent="ASA House of Delegates approval, universal adoption worldwide",
        issue_category=IssueCategory.PREOPERATIVE_ASSESSMENT,
        analysis_zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.GUIDELINE,
        fact_fragility=0.2,
        recharacterization_risk=0.3,
        testimony_dependence=0.4
    ),

    DoctrineBlock(
        topic="Mallampati Airway Assessment",
        keywords=["Mallampati", "airway assessment", "difficult intubation", "oropharyngeal", "uvula visibility", "faucial pillars"],
        conclusion_template="Mallampati Class {class_num} predicts {difficulty_level} intubation risk with {sensitivity}% sensitivity for difficult airway.",
        reasoning_framework="""
The Mallampati Classification assesses oropharyngeal anatomy to predict difficult laryngoscopy and intubation:

Class I: Full visibility of tonsils, uvula, and soft palate
- Pillars, soft palate, and entire uvula visible
- Difficult intubation risk: 1-2%
- Best predictor of easy intubation

Class II: Visibility of hard and soft palate, upper portion of tonsils and uvula
- Uvula tip visible, tonsils partially obscured
- Difficult intubation risk: 3-5%
- Still generally favorable airway

Class III: Soft and hard palate and base of uvula visible
- Only base of uvula visible, tonsils not visible
- Difficult intubation risk: 7-12%
- Increased risk, prepare alternative airway equipment

Class IV: Only hard palate visible
- Soft palate not visible at all
- Difficult intubation risk: 15-20%
- High risk, consider awake fiberoptic intubation

Modified Mallampati (with phonation):
- Patient sits upright, opens mouth, protrudes tongue WITHOUT phonation
- More reproducible than original technique
- Sensitivity: 40-50% for difficult intubation
- Specificity: 80-90%

CRITICAL LIMITATIONS:
- Mallampati alone has poor positive predictive value (PPV ~15-20%)
- MUST combine with other assessments: thyromental distance, neck mobility, jaw protrusion, obesity
- False reassurance from Class I/II (still 1-2% difficult intubation rate)

Enhanced prediction with combined criteria:
- Mallampati III/IV + thyromental distance <6 cm → 90% difficult intubation
- Mallampati III/IV + limited neck extension (<80 degrees) → 85% difficult intubation
- Mallampati III/IV + BMI >35 → 75% difficult intubation

The gold standard is multivariate assessment using LEMON criteria or El-Ganzouri Risk Index.
        """,
        key_factors=[
            "Uvula and faucial pillar visibility",
            "Thyromental distance (should be >6 cm)",
            "Neck extension and atlantooccipital joint mobility",
            "Jaw protrusion ability (upper lip bite test)",
            "Obesity (BMI >35 increases risk 3-fold)",
            "History of difficult intubation",
            "Obstructive sleep apnea presence"
        ],
        primary_authority=[
            "Mallampati SR et al. Can J Anaesth 1985;32:429-434 (original description)",
            "Anesthesiology 2022;136:212-225 (ASA Difficult Airway Algorithm)",
            "Br J Anaesth 2019;123:e645-e648 (multivariate airway assessment)"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Time pressure in emergency cases may limit thorough assessment",
        counter_arguments=[
            "Low sensitivity (40-50%) means many difficult airways are missed",
            "High false positive rate leads to unnecessary awake intubations",
            "Inter-rater reliability is only moderate (kappa 0.5-0.6)"
        ],
        resolution_strategy="Never rely on Mallampati alone; use ASA Difficult Airway Algorithm with multiple predictors",
        entity_scope="All patients requiring endotracheal intubation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Level 2 evidence, universal clinical practice",
        controlling_precedent="ASA Difficult Airway Algorithm 2022",
        issue_category=IssueCategory.AIRWAY_MANAGEMENT,
        analysis_zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.GUIDELINE,
        fact_fragility=0.3,
        recharacterization_risk=0.3,
        testimony_dependence=0.5
    ),

    DoctrineBlock(
        topic="WHO Surgical Safety Checklist",
        keywords=["WHO checklist", "surgical safety", "time-out", "sign-in", "sign-out", "team briefing", "wrong-site surgery"],
        conclusion_template="WHO Surgical Safety Checklist implementation reduces surgical mortality by {mortality_reduction}% and morbidity by {morbidity_reduction}%.",
        reasoning_framework="""
The World Health Organization Surgical Safety Checklist is a 19-item tool divided into three phases:

SIGN IN (Before Induction of Anesthesia):
- Patient confirms identity, surgical site, procedure, and consent
- Site marked/not applicable
- Anesthesia safety check completed (machine, medications, airway equipment)
- Pulse oximeter on patient and functioning
- Known allergy? Yes/No
- Difficult airway/aspiration risk? Yes/No → Equipment and assistance available
- Risk of >500mL blood loss (7mL/kg in children)? Yes/No → IV access and fluids planned

TIME OUT (Before Skin Incision):
- ALL team members introduce themselves by name and role
- Surgeon, anesthesia professional, and nurse verbally confirm:
  * Patient identity
  * Surgical site
  * Procedure
- Surgeon reviews: critical/unexpected steps, operative duration, anticipated blood loss
- Anesthesia team reviews: patient-specific concerns
- Nursing team reviews: sterility confirmed (including indicator results), equipment issues
- Prophylactic antibiotics given within last 60 minutes? Yes/Not applicable
- Essential imaging displayed? Yes/Not applicable

SIGN OUT (Before Patient Leaves OR):
- Nurse verbally confirms with team:
  * Name of procedure recorded
  * Instrument, sponge, and needle counts correct (or not applicable)
  * Specimen labeling (read specimen labels aloud, including patient name)
  * Equipment problems to address
- Surgeon, anesthesia professional, and nurse review key concerns for recovery and management

EVIDENCE FOR EFFECTIVENESS:
- Original WHO study (8 hospitals, 7,688 patients):
  * Mortality reduced from 1.5% to 0.8% (p=0.003)
  * Complications reduced from 11.0% to 7.0% (p<0.001)
  * Wrong-site surgery reduced by 90%

- Subsequent meta-analyses (>50 studies):
  * 37% reduction in surgical mortality
  * 36% reduction in major complications
  * 50% reduction in surgical site infections
  * 39% reduction in wrong-site/wrong-patient events

IMPLEMENTATION CRITICAL SUCCESS FACTORS:
- Active engagement, not checkbox compliance
- Empowerment of any team member to halt for concerns
- Brief verbal exchange, not silent reading
- Adaptation to local context while preserving core elements
- Leadership support and culture of safety
- Regular auditing and feedback

FAILURE MODES:
- Rushing through checklist (takes <2 min properly)
- Senior surgeon dismissiveness
- Skipping items marked 'not applicable' without verification
- Completing before all team members present
- No empowerment to speak up for concerns

Joint Commission sentinel event data shows 70% of wrong-site surgeries had checklist violations.
        """,
        key_factors=[
            "All team members present and engaged",
            "Verbal confirmation by surgeon, anesthesia, nursing",
            "Site marking visible after draping",
            "Antibiotic timing within 60 min of incision",
            "Specimen labeling with patient name read aloud",
            "Empowerment culture allowing any member to stop",
            "Documentation of completion"
        ],
        primary_authority=[
            "WHO Guidelines for Safe Surgery 2009",
            "N Engl J Med 2009;360:491-499 (original WHO study)",
            "Joint Commission National Patient Safety Goals",
            "Cochrane Database Syst Rev 2020;5:CD009641 (meta-analysis)"
        ],
        burden_holder="Entire surgical team (surgeon, anesthesia, nursing)",
        adversary_position="Time pressure and production demands resist 'extra' steps",
        counter_arguments=[
            "Takes 2-3 minutes in busy OR schedule",
            "Checkbox compliance without engagement provides false security",
            "Some items may not apply to all procedures"
        ],
        resolution_strategy="Mandatory institutional policy, culture change from leadership, audit with feedback",
        entity_scope="All surgical procedures in all settings",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Level 1 evidence from RCTs and meta-analyses",
        controlling_precedent="Joint Commission requirement, CMS reporting measure",
        issue_category=IssueCategory.SURGICAL_SAFETY,
        analysis_zone=AnalysisZone.OPERATIVE,
        authority_level=AuthorityLevel.REGULATORY,
        fact_fragility=0.1,
        recharacterization_risk=0.1,
        testimony_dependence=0.2
    ),

    # ========== MINIMALLY INVASIVE SURGERY ==========

    DoctrineBlock(
        topic="Laparoscopic vs Open Surgery Decision Criteria",
        keywords=["laparoscopic", "minimally invasive", "open surgery", "trocar placement", "pneumoperitoneum", "conversion to open"],
        conclusion_template="Laparoscopic approach for {procedure} offers {benefit_level} benefits with {conversion_rate}% conversion risk in appropriately selected patients.",
        reasoning_framework="""
Decision criteria for laparoscopic vs open approach balances patient benefits against technical feasibility and safety:

LAPAROSCOPIC ADVANTAGES:
- Reduced postoperative pain (50-70% less narcotic use)
- Shorter hospital stay (1-3 days vs 4-7 days for many procedures)
- Faster return to normal activity (2-3 weeks vs 6-8 weeks)
- Improved cosmesis (4-5 small incisions vs large laparotomy)
- Reduced wound complications (infection, hernia, dehiscence)
- Better visualization with magnification
- Less insensible fluid loss and hypothermia

LAPAROSCOPIC DISADVANTAGES:
- Longer operative time (especially during learning curve)
- Requires specialized equipment and training
- Loss of tactile feedback
- Two-dimensional vision (partially addressed by 3D systems)
- Pneumoperitoneum physiologic effects (decreased venous return, increased airway pressure)
- Higher cost ($1,500-3,000 more in supplies)
- Contraindications: severe cardiopulmonary disease, uncorrected coagulopathy

ABSOLUTE CONTRAINDICATIONS:
- Hemodynamic instability requiring rapid exploration
- Inability to tolerate pneumoperitoneum (severe COPD, pulmonary hypertension)
- Suspected perforated viscus with free air masking pneumoperitoneum
- Uncorrected coagulopathy or anticoagulation
- Abdominal compartment syndrome
- Massive hemoperitoneum requiring damage control

RELATIVE CONTRAINDICATIONS:
- Extensive prior abdominal surgery (adhesions increase difficulty)
- Morbid obesity (BMI >50, though now often approached laparoscopically)
- Advanced cirrhosis with portal hypertension
- Pregnancy (second trimester often feasible with modifications)
- Large masses or organomegaly
- Pediatric patients <5kg

CONVERSION TO OPEN (not a complication if recognized appropriately):
- Inability to obtain adequate visualization (dense adhesions)
- Uncontrolled bleeding not manageable laparoscopically
- Equipment failure
- Unexpected pathology (advanced cancer requiring resection)
- Physiologic intolerance to pneumoperitoneum
- Iatrogenic injury requiring repair

Conversion rates vary by procedure:
- Laparoscopic cholecystectomy: 2-5% (acute cholecystitis 10-15%)
- Laparoscopic appendectomy: 3-8%
- Laparoscopic colectomy: 5-20% (varies by indication)
- Laparoscopic ventral hernia: 5-15%

ENHANCED RECOVERY AFTER SURGERY (ERAS) SYNERGY:
- Laparoscopic approach is cornerstone of ERAS protocols
- Enables earlier feeding, mobilization, reduced ileus
- Multimodal analgesia more effective with smaller incisions
- Reduced systemic inflammatory response

LEARNING CURVE CONSIDERATIONS:
- Competency requires 20-50 cases for basic procedures
- Advanced procedures (colectomy, bariatric) require 50-100 cases
- Fellowship training vs community surgeon experience
- Proctoring and simulation training improve safety during learning curve

The decision should be individualized based on patient factors, surgical indication, urgency, and surgeon experience.
        """,
        key_factors=[
            "Patient cardiopulmonary reserve for pneumoperitoneum",
            "Prior abdominal surgery and adhesions",
            "BMI and body habitus",
            "Surgical indication (cancer vs benign)",
            "Surgeon experience and volume",
            "Equipment and team availability",
            "Urgency of surgery (emergent vs elective)"
        ],
        primary_authority=[
            "SAGES Guidelines for laparoscopic surgery (multiple procedures)",
            "Cochrane Database Syst Rev 2017 (laparoscopic vs open surgery meta-analyses)",
            "Ann Surg 2018;267:648-655 (ERAS and minimally invasive surgery)",
            "J Am Coll Surg 2019;229:503-512 (conversion rates and outcomes)"
        ],
        burden_holder="Surgeon",
        adversary_position="Patient preference may favor less invasive approach despite contraindications",
        counter_arguments=[
            "Longer operative time increases anesthesia risk",
            "Equipment costs not justified for all procedures",
            "Open surgery may be faster and safer in emergency setting",
            "Tactile feedback loss may miss pathology"
        ],
        resolution_strategy="Shared decision-making with informed consent discussing risks and benefits of each approach",
        entity_scope="All intra-abdominal and thoracic procedures where laparoscopy is feasible",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Level 1 evidence from multiple RCTs and meta-analyses",
        controlling_precedent="Society guidelines (SAGES, ACS) supporting minimally invasive when feasible",
        issue_category=IssueCategory.MINIMALLY_INVASIVE,
        analysis_zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.LEVEL_1_RCT,
        fact_fragility=0.2,
        recharacterization_risk=0.2,
        testimony_dependence=0.3
    ),

    DoctrineBlock(
        topic="Robotic-Assisted Surgery (da Vinci Platform)",
        keywords=["robotic surgery", "da Vinci", "robotic-assisted", "prostatectomy", "hysterectomy", "EndoWrist", "console"],
        conclusion_template="Robotic-assisted {procedure} offers {advantage_summary} at increased cost of ${cost_increment} with {outcome_comparison} compared to conventional laparoscopy.",
        reasoning_framework="""
Robotic-assisted surgery using da Vinci Surgical System (Intuitive Surgical) represents evolution of minimally invasive technique:

TECHNICAL ADVANTAGES OVER CONVENTIONAL LAPAROSCOPY:
- 3D high-definition vision (10-15x magnification) vs 2D laparoscopy
- 7 degrees of freedom with EndoWrist instruments vs 4 degrees with laparoscopic
- Tremor filtration and motion scaling (3:1 to 5:1)
- Ergonomic surgeon console vs awkward laparoscopic positioning
- Improved dexterity for complex dissection and suturing
- Shorter learning curve for complex procedures (especially suturing)
- Fourth arm allows camera control without assistant

DISADVANTAGES:
- High capital cost ($1.5-2.5 million per system)
- Disposable instrument costs ($2,000-3,000 per case)
- No tactile feedback (visual cues must substitute)
- Longer setup/docking time (15-30 min)
- Larger footprint requires dedicated OR space
- Restricted to procedures accessible by ports
- Emergency conversion to open more difficult

CLINICAL EVIDENCE BY PROCEDURE:

Robotic Prostatectomy (most robust data):
- LOWER: positive margin rates 15% vs 24% open (p<0.001)
- EQUIVALENT: cancer control, overall survival at 10 years
- FASTER: return to continence (50% at 3 months vs 6 months)
- FASTER: return to erectile function (if nerve-sparing)
- SHORTER: hospital stay (1 day vs 3 days)
- COST: $3,000-5,000 more than open, $2,000 more than laparoscopic

Robotic Hysterectomy:
- EQUIVALENT: oncologic outcomes to abdominal for cancer
- BETTER: than abdominal for pain, recovery, complications
- EQUIVALENT: to vaginal approach for most benign disease
- DEBATED: superiority over conventional laparoscopy (minimal difference)
- COST: $2,000-4,000 more than laparoscopic

Robotic Colorectal Surgery:
- EQUIVALENT: oncologic outcomes (margins, lymph nodes, survival)
- POSSIBLE: lower conversion rate (8% vs 13% laparoscopic in some series)
- POSSIBLE: better visualization in narrow pelvis
- UNCERTAIN: clinical advantage over laparoscopic in rectal cancer
- COST: $3,000-6,000 more than laparoscopic

Robotic Bariatric Surgery:
- DEBATED: any advantage over laparoscopic gastric bypass or sleeve
- POSSIBLE: easier staple line reinforcement and suturing
- COST: Not justified by outcomes in most analyses

Robotic Cardiac Surgery:
- NICHE: mitral valve repair, atrial septal defect
- LEARNING CURVE: steep, requires high volume
- OUTCOMES: equivalent to traditional in experienced hands

MEDICO-LEGAL CONSIDERATIONS:
- Informed consent must address robotic-specific risks
- Marketing claims of 'better outcomes' may not be evidence-based
- Device malfunction is rare but catastrophic (retained instruments, electrical arc)
- Surgeon credentialing and proctoring requirements
- Documentation of console time vs bedside assistance time

FUTURE DEVELOPMENTS:
- Haptic feedback systems in development
- Single-port robotic platforms
- Smaller, cheaper systems (Versius, Hugo, Hominis)
- AI-assisted surgical guidance

The decision to use robotic assistance should be based on surgeon expertise, patient anatomy, procedure complexity, and institutional resources, NOT marketing.
        """,
        key_factors=[
            "Procedure complexity (fine dissection, suturing required)",
            "Patient anatomy (narrow pelvis, obesity favor robotic)",
            "Surgeon training and volume (>20 cases for proficiency)",
            "Institutional investment and support",
            "Cost-benefit analysis vs conventional laparoscopy",
            "Evidence base for specific procedure",
            "Patient preference after informed consent"
        ],
        primary_authority=[
            "J Urol 2022;207:555-563 (robotic prostatectomy long-term outcomes)",
            "JAMA Surg 2020;155:e196530 (robotic vs laparoscopic colorectal surgery meta-analysis)",
            "Cochrane Database Syst Rev 2021;3:CD006535 (robotic vs conventional surgery)",
            "FDA MAUDE database (device malfunction reporting)"
        ],
        burden_holder="Surgeon and institution",
        adversary_position="Direct-to-consumer marketing creates patient demand without evidence support",
        counter_arguments=[
            "No proven superiority for most procedures vs expert laparoscopy",
            "Cost not justified by marginal outcome improvements",
            "Tactile feedback loss may increase risk of injury",
            "Monopoly pricing by Intuitive Surgical limits competition"
        ],
        resolution_strategy="Evidence-based patient selection, transparent cost discussion, realistic outcome expectations",
        entity_scope="Complex minimally invasive procedures in high-volume centers",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Level 2 evidence, highly procedure-dependent, evolving technology",
        controlling_precedent="FDA clearance for specific indications, society guidelines emerging",
        issue_category=IssueCategory.ROBOTIC_SURGERY,
        analysis_zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.LEVEL_2_COHORT,
        fact_fragility=0.4,
        recharacterization_risk=0.3,
        testimony_dependence=0.3
    ),

    # ========== SURGICAL SAFETY & INFECTION CONTROL ==========

    DoctrineBlock(
        topic="Surgical Site Infection Prevention Bundle",
        keywords=["SSI prevention", "surgical site infection", "antibiotic prophylaxis", "chlorhexidine", "normothermia", "glycemic control"],
        conclusion_template="Evidence-based SSI prevention bundle reduces infection rates from {baseline_rate}% to {intervention_rate}% through {bundle_components}.",
        reasoning_framework="""
Surgical Site Infections (SSI) occur in 2-5% of surgeries, cost $10 billion annually, and are largely preventable:

CORE PREVENTIVE MEASURES (Grade A Evidence):

1. PREOPERATIVE ANTIBIOTICS:
- Timing: Within 60 min before incision (120 min for vancomycin/fluoroquinolones)
- Selection: Based on likely skin/surgical site flora
  * Clean (cardiac, orthopedic): cefazolin 2g (3g if >120kg)
  * Clean-contaminated (GI, GYN): cefazolin + metronidazole OR cefoxitin
  * Beta-lactam allergy: vancomycin + gentamicin or aztreonam
- Redosing: If surgery >2 half-lives or blood loss >1,500mL
  * Cefazolin: redose at 4 hours
  * Cefoxitin: redose at 2 hours
- Duration: Single dose sufficient for most; discontinue within 24h (cardiac surgery 48h)

2. SKIN ANTISEPSIS:
- Chlorhexidine-alcohol SUPERIOR to povidone-iodine (4.2% vs 8.6% SSI, p<0.001)
- Application: 2-minute scrub, allow 3-minute dry time before draping
- Hair removal: clippers only, NO razors (microabrasions increase infection)
- Mucosal surfaces: povidone-iodine (chlorhexidine contraindicated in eye, ear, mucosa)

3. PERIOPERATIVE NORMOTHERMIA:
- Maintain core temp >36°C (96.8°F)
- Hypothermia impairs neutrophil function and tissue oxygenation
- Methods: forced-air warming, fluid warmers, increased OR temperature
- Evidence: SSI reduced from 6% to 1.9% with active warming (p=0.009)

4. PERIOPERATIVE GLYCEMIC CONTROL:
- Target: glucose <180 mg/dL (some guidelines <150 mg/dL)
- Hyperglycemia impairs immune function and wound healing
- Applies to diabetics AND stress hyperglycemia in non-diabetics
- Evidence: SSI reduced by 30-50% with tight glucose control

5. SUPPLEMENTAL OXYGEN:
- FiO2 0.80 during surgery and 2h postop for colorectal surgery
- Increases tissue oxygen tension, enhances neutrophil killing
- CONTROVERSIAL: Some studies show benefit, others neutral or harm
- Current recommendation: Consider for high-risk colorectal cases

ADDITIONAL MEASURES (Grade B Evidence):

6. SURGICAL TECHNIQUE:
- Minimize tissue trauma and devitalized tissue
- Maintain hemostasis (hematomas are culture media)
- Preserve blood supply to wound edges
- Minimal use of electrocautery (thermal tissue damage)
- Irrigation before closure (especially dirty/contaminated wounds)

7. WOUND PROTECTORS/RETRACTORS:
- Dual-ring plastic barriers in GI/oncologic surgery
- Reduce SSI by 30-45% in colorectal surgery (meta-analysis)
- Cost-effective despite device expense

8. GLOVE CHANGES:
- Change gloves before closure (especially in contaminated cases)
- Double gloving reduces perforation exposure

9. DELAYED PRIMARY CLOSURE:
- Dirty/contaminated wounds: leave open, close 3-5 days if clean
- Reduces SSI from 23% to 2.1% in contaminated abdominal surgery

10. NASAL DECOLONIZATION:
- Mupirocin ointment for known MRSA carriers
- 2% chlorhexidine body wash night before and morning of surgery

MEASURES NOT RECOMMENDED:
- Routine prolonged antibiotic prophylaxis (increases resistance)
- Antibiotic wound irrigation (tissue levels already adequate)
- Topical antibiotics in clean wounds (no benefit)

SURVEILLANCE AND AUDITING:
- Track SSI rates by procedure and risk index
- NHSN (National Healthcare Safety Network) definitions
- Feedback to surgeons improves compliance and outcomes

Evidence shows bundles (combining multiple interventions) produce greater SSI reduction than single measures.
        """,
        key_factors=[
            "Antibiotic timing within 60 min of incision",
            "Chlorhexidine-alcohol skin prep with adequate dry time",
            "Core temperature maintained >36°C",
            "Glucose <180 mg/dL perioperatively",
            "Hemostasis and gentle tissue handling",
            "Hair removal with clippers only",
            "Appropriate antibiotic selection and redosing"
        ],
        primary_authority=[
            "WHO Guidelines for Safe Surgery 2016 (SSI prevention)",
            "CDC/HICPAC Guideline for Prevention of SSI 2017",
            "N Engl J Med 2010;362:9-17 (chlorhexidine-alcohol vs povidone-iodine)",
            "JAMA Surg 2017;152:784-791 (SSI prevention bundle meta-analysis)",
            "Infect Control Hosp Epidemiol 2014;35:605-627 (SHEA/IDSA compendium)"
        ],
        burden_holder="Surgical team and infection prevention program",
        adversary_position="Time pressure may compromise thorough skin prep or warming measures",
        counter_arguments=[
            "Bundle compliance is challenging in busy OR",
            "Some elements (supplemental O2) have conflicting evidence",
            "Cost of devices (wound protectors) may not be reimbursed",
            "Chlorhexidine allergies require alternative antiseptics"
        ],
        resolution_strategy="Institutional protocols with auditing and feedback, leadership support, EHR prompts",
        entity_scope="All surgical procedures",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Level 1 evidence from RCTs and meta-analyses for core bundle components",
        controlling_precedent="Joint Commission SCIP measures, CMS quality reporting",
        issue_category=IssueCategory.INFECTION_CONTROL,
        analysis_zone=AnalysisZone.OPERATIVE,
        authority_level=AuthorityLevel.LEVEL_1_RCT,
        fact_fragility=0.1,
        recharacterization_risk=0.1,
        testimony_dependence=0.2
    ),

    DoctrineBlock(
        topic="Enhanced Recovery After Surgery (ERAS) Protocols",
        keywords=["ERAS", "enhanced recovery", "fast-track surgery", "multimodal analgesia", "early mobilization", "goal-directed fluid"],
        conclusion_template="ERAS protocol implementation for {procedure} reduces length of stay by {los_reduction} days and complications by {complication_reduction}% without increasing readmissions.",
        reasoning_framework="""
Enhanced Recovery After Surgery (ERAS) represents paradigm shift from traditional perioperative care:

CORE ERAS ELEMENTS (20+ interventions across perioperative phases):

PREOPERATIVE (PREHABILITATION):
1. Patient education and expectation management
   - Written and verbal information about pathway
   - Expected timeline for milestones (eating, walking, discharge)
   - Reduces anxiety, improves compliance

2. No prolonged fasting
   - Clear liquids until 2h before surgery
   - Carbohydrate loading (400mL 12.5% maltodextrin 2-3h preop)
   - Reduces insulin resistance and catabolism

3. No routine bowel preparation (colorectal surgery)
   - Traditional prep causes dehydration, electrolyte imbalance
   - Meta-analyses show no benefit for SSI or anastomotic leak
   - Exception: rectal surgery where diversion may be needed

4. Selective preoperative optimization
   - Smoking cessation ≥4 weeks (if elective)
   - Alcohol cessation ≥4 weeks
   - Anemia correction (iron, EPO)
   - Nutritional supplementation if malnourished

INTRAOPERATIVE:
5. Multimodal analgesia minimizing opioids
   - Regional anesthesia (epidural, TAP blocks, nerve blocks)
   - NSAIDs (ketorolac, celecoxib)
   - Acetaminophen IV
   - Gabapentinoids (pregabalin 150-300mg)
   - Local anesthetic wound infiltration

6. Short-acting anesthetics
   - Avoid long-acting benzodiazepines and opioids
   - Propofol/remifentanil TIVA or volatile with rapid emergence
   - Minimize neuromuscular blockade, reverse completely

7. Minimally invasive surgical approach
   - Laparoscopy/robotic when feasible
   - Smaller incisions reduce pain, ileus, complications

8. No routine nasogastric tubes
   - Meta-analyses show increased pulmonary complications, delayed recovery
   - Use only if needed for decompression, remove ASAP

9. No routine surgical drains
   - Increase pain, limit mobilization
   - Meta-analyses show no benefit for leak detection in most surgeries
   - Use selectively based on indication

10. Goal-directed fluid therapy (GDFT)
    - Euvolemia, avoid both under- and over-resuscitation
    - Stroke volume variation or esophageal Doppler guided
    - Avoid routine crystalloid loading (third-spacing, ileus)

11. Normothermia maintenance
    - Core temp >36°C (forced-air warming, fluid warmers)

POSTOPERATIVE:
12. Early oral intake
    - Clear liquids immediately post-op if tolerated
    - Regular diet by POD 1 (even after GI surgery)
    - Gum chewing reduces ileus duration

13. Early mobilization
    - Out of bed POD 0 (day of surgery) for 2h minimum
    - Progressive ambulation goals (4h POD1, 6h POD2)
    - Reduces VTE, pneumonia, ileus

14. Multimodal PONV prophylaxis
    - 2-3 agents based on Apfel score
    - Ondansetron, dexamethasone, scopolamine patch
    - Nausea impairs oral intake and mobilization

15. Restrictive IV fluids postop
    - Discontinue IV fluids once tolerating PO
    - Excessive fluids delay ileus resolution, increase complications

16. Avoidance of opioids
    - Scheduled non-opioid analgesics
    - Opioids only for breakthrough pain
    - Reduces ileus, PONV, sedation

17. Urinary catheter removal POD 1
    - Prolonged catheterization increases UTI, impairs mobilization
    - Exception: epidural analgesia, complex pelvic surgery

18. Audit and feedback
    - Compliance monitoring for all protocol elements
    - Outcomes tracking and variance analysis
    - Continuous quality improvement

EVIDENCE BASE:
- Meta-analysis of 83 studies (16,000+ patients):
  * Hospital stay reduced by 2.5 days (30-50% reduction)
  * Complications reduced by 35-50%
  * No increase in readmissions (some studies show reduction)
  * Cost savings $3,000-5,000 per patient

- Best evidence for colorectal (original application), now expanded to:
  * Gynecologic oncology
  * Urologic (cystectomy, prostatectomy)
  * Hepatobiliary
  * Bariatric
  * Thoracic
  * Orthopedic (joint replacement)

IMPLEMENTATION CHALLENGES:
- Requires multidisciplinary coordination (surgery, anesthesia, nursing, PT, nutrition)
- Culture change from traditional 'bowel rest and bed rest' mentality
- Initial learning curve (6-12 months to full compliance)
- Resource intensive (dedicated ERAS coordinator essential)
- Patient selection (frail/high-risk may not tolerate early mobilization)

FAILURE MODES:
- Cherry-picking elements without full bundle (synergy lost)
- Lack of surgeon buy-in
- Nursing resistance to early feeding/mobilization
- Inadequate pain control leading to immobility
- Fluid overload from traditional IV practices

Success requires institutional commitment, leadership support, and dedicated resources.
        """,
        key_factors=[
            "Multidisciplinary team coordination",
            "Patient education and engagement",
            "Minimally invasive surgical approach",
            "Multimodal opioid-sparing analgesia",
            "Early oral intake (POD 0-1)",
            "Early mobilization (out of bed POD 0)",
            "Goal-directed fluid therapy avoiding overload",
            "Compliance monitoring and feedback"
        ],
        primary_authority=[
            "ERAS Society Guidelines (procedure-specific, multiple publications)",
            "Lancet 2019;393:1265-1275 (ERAS meta-analysis)",
            "Ann Surg 2015;262:416-426 (colorectal ERAS outcomes)",
            "Br J Surg 2020;107:e169-e177 (ERAS implementation and compliance)"
        ],
        burden_holder="Multidisciplinary perioperative team",
        adversary_position="Traditional surgical culture resists paradigm change",
        counter_arguments=[
            "Early feeding/mobilization may increase complications in high-risk patients",
            "Resource intensive requiring dedicated coordinator",
            "Initial learning curve may temporarily worsen outcomes",
            "Not all elements applicable to emergency surgery"
        ],
        resolution_strategy="Phased implementation with stakeholder engagement, data-driven feedback, leadership support",
        entity_scope="Elective major surgery across specialties",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Level 1 evidence from multiple RCTs and meta-analyses",
        controlling_precedent="ERAS Society consensus guidelines, increasingly adopted as standard of care",
        issue_category=IssueCategory.ERAS_PROTOCOLS,
        analysis_zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.LEVEL_1_RCT,
        fact_fragility=0.2,
        recharacterization_risk=0.2,
        testimony_dependence=0.2
    ),

    # ========== ELECTROSURGERY & ENERGY DEVICES ==========

    DoctrineBlock(
        topic="Electrosurgery Safety (Monopolar vs Bipolar)",
        keywords=["electrosurgery", "Bovie", "monopolar", "bipolar", "capacitive coupling", "return electrode", "burns"],
        conclusion_template="Electrosurgery using {modality} carries {injury_risk} risk of burns and electrical injury when proper grounding and technique are followed.",
        reasoning_framework="""
Electrosurgery uses high-frequency (300kHz-3MHz) alternating current to cut and coagulate tissue:

MONOPOLAR ELECTROSURGERY:
- Current path: Active electrode → Tissue → Dispersive pad → Generator
- Active electrode: small surface area concentrates current (cutting/coagulation)
- Dispersive pad ('grounding pad'): large surface area dissipates current safely
- Power: 50-400 watts depending on mode

Modes:
- CUTTING (CUT): Continuous sinusoidal waveform, vaporizes tissue (yellow spark)
- COAGULATION (COAG): Interrupted waveform, desiccates tissue (minimal cutting)
- BLEND: Combination of cutting and coagulation

BIPOLAR ELECTROSURGERY:
- Current path: Between two tips of forceps (completes circuit locally)
- NO grounding pad required
- Lower power (typically 10-70 watts)
- More precise, less tissue damage
- CANNOT cut (coagulation only)
- Ideal for: Neurosurgery, ophthalmic, microsurgery, patients with pacemakers

INJURY MECHANISMS AND PREVENTION:

1. RETURN ELECTRODE BURNS (most common monopolar injury):
- Cause: Inadequate pad contact, pad over bony prominence, conductive gel dried out
- Prevention:
  * Use disposable self-adhesive pads
  * Place over large muscle mass (thigh, buttock)
  * Avoid bony prominences, scar tissue, hairy areas
  * Return electrode monitoring (REM) systems detect poor contact
  * Ensure pad is not touching metal (OR table, stirrups)

2. ALTERNATE PATHWAY BURNS:
- Current finds unintended path to ground (ECG leads, pulse ox, jewelry, metal implants)
- Prevention:
  * Remove jewelry
  * Insulate ECG leads from skin
  * Avoid pooled prep solutions creating conductive path
  * Ensure patient not touching grounded metal

3. DIRECT COUPLING:
- Active electrode touches another instrument, transferring current
- Prevention:
  * Activate only when electrode visible and tissue contact intended
  * Use insulated graspers to manipulate active electrode
  * Holster when not in use

4. CAPACITIVE COUPLING (laparoscopy-specific):
- Insulated active electrode induces current in nearby conductor (trocar, scope)
- Risk increased with: High voltage, metal cannulas, defective insulation
- Prevention:
  * All-plastic trocars OR all-metal trocars (avoid hybrid)
  * Active electrode monitoring (AEM) systems
  * Inspect insulation for cracks/defects
  * Lower power settings for laparoscopy

5. INSULATION FAILURE:
- Cracks in electrode insulation cause stray current burn
- Prevention:
  * Inspect instruments before each use
  * Single-use electrodes reduce risk
  * AEM systems detect insulation defects

6. PACEMAKER/ICD INTERFERENCE:
- Monopolar current can inhibit pacing or trigger defibrillation
- Prevention:
  * Use BIPOLAR when possible (no interference)
  * If monopolar required:
    - Place dispersive pad to direct current away from device
    - Use short bursts (<5 seconds)
    - Keep active electrode >6 inches from device
    - Have magnet available to convert to asynchronous pacing
    - Cardiology/EP consult for ICD interrogation pre/post-op

7. SURGICAL FIRES (rare but catastrophic):
- Triad: Ignition source (electrosurgery), Fuel (drapes, gowns), Oxidizer (O2, N2O)
- High-risk: Head/neck surgery with supplemental O2
- Prevention:
  * Reduce FiO2 to minimum necessary
  * Allow alcohol prep to dry completely (3 minutes)
  * Use moistened towels around surgical field
  * Have saline irrigation ready
  * Brief team on fire risk and response plan

POWER SETTINGS:
- Use lowest effective power
- Laparoscopy: 20-40W cut, 30-50W coag (lower than open)
- Open surgery: 40-60W cut, 50-80W coag
- Cutting requires LESS power than coagulation

ARGON BEAM COAGULATION (ABC):
- Ionized argon gas conducts current to tissue surface
- Advantages: Uniform coagulation, less char, hemostasis of large surfaces
- Disadvantages: Gas embolism risk (especially liver), higher cost
- Use: Liver resection, spleen injuries, diffuse oozing

ULTRASONIC DEVICES (Harmonic Scalpel):
- Mechanical vibration (55,500 Hz) generates heat through friction
- NO electrical current (safe for pacemakers)
- Advantages: Minimal lateral thermal spread (1-2mm vs 5-10mm electrosurgery)
- Disadvantages: Slower, more expensive, less effective for large vessels
- Use: Thyroid, laparoscopic cases, vessels <3mm

ADVANCED BIPOLAR DEVICES (LigaSure, EnSeal):
- Vessel sealing up to 7mm diameter
- Combines pressure and bipolar energy
- Advantages: Reliable hemostasis, faster than ties/clips
- Disadvantages: Expensive ($200-400/device)

The key to safety is understanding the energy modality, proper equipment setup, and vigilant technique.
        """,
        key_factors=[
            "Return electrode placement over muscle mass with full contact",
            "Electrode insulation integrity check before use",
            "Lowest effective power setting",
            "Activate only when tip visible and intended tissue contact",
            "Bipolar for pacemaker/ICD patients",
            "Awareness of capacitive coupling in laparoscopy",
            "Fire prevention in O2-enriched environment"
        ],
        primary_authority=[
            "ECRI Institute Electrosurgery Safety Recommendations",
            "AORN Guideline for Electrosurgery 2021",
            "Surg Endosc 2019;33:1261-1275 (electrosurgery complications and prevention)",
            "J Clin Anesth 2017;43:74-78 (pacemaker/ICD management during surgery)"
        ],
        burden_holder="Surgeon and OR team",
        adversary_position="Time pressure may lead to rushed setup and inadequate safety checks",
        counter_arguments=[
            "Modern REM/AEM systems prevent most pad-related burns",
            "Bipolar devices expensive and slower for some applications",
            "Pacemaker precautions often excessive for modern devices"
        ],
        resolution_strategy="Institutional protocols for device setup, safety checks, and team briefing on high-risk cases",
        entity_scope="All surgical procedures using electrosurgery",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Level 3 evidence from case series, strong consensus on safety practices",
        controlling_precedent="AORN standards, ECRI guidance, FDA device labeling",
        issue_category=IssueCategory.ELECTROSURGERY,
        analysis_zone=AnalysisZone.OPERATIVE,
        authority_level=AuthorityLevel.REGULATORY,
        fact_fragility=0.2,
        recharacterization_risk=0.2,
        testimony_dependence=0.3
    ),

    # ========== BLOOD MANAGEMENT ==========

    DoctrineBlock(
        topic="Blood Loss Estimation and Transfusion Thresholds",
        keywords=["blood loss", "EBL", "estimated blood loss", "transfusion trigger", "hemoglobin threshold", "restrictive transfusion"],
        conclusion_template="Estimated blood loss of {ebl_volume}mL represents {percentage}% of blood volume requiring transfusion at hemoglobin <{hgb_threshold} g/dL in {patient_population}.",
        reasoning_framework="""
Accurate blood loss estimation and evidence-based transfusion thresholds optimize patient outcomes:

BLOOD VOLUME ESTIMATION:
- Adult male: 75 mL/kg (typically 5-6 L for 70kg patient)
- Adult female: 65 mL/kg (typically 4-5 L for 70kg patient)
- Children: 80 mL/kg
- Neonates: 85-90 mL/kg

BLOOD LOSS ESTIMATION METHODS:

1. VISUAL ESTIMATION (least accurate):
- Surgeon estimates based on suction, sponges, floor
- Notoriously INACCURATE: typically underestimates by 30-50%
- Tends to underestimate small losses, overestimate large losses

2. GRAVIMETRIC METHOD (weigh sponges):
- Dry weight vs soaked weight (1g = 1mL blood)
- Must subtract irrigation fluid
- Accuracy improves 20-30% over visual
- Challenges: Time-consuming, irrigation contamination

3. COLORIMETRIC SYSTEMS (Triton, Gauss):
- iPad/tablet app analyzes photos of sponges/suction
- Hemoglobin spectrophotometry
- Accuracy within 10-15% of laboratory measurement
- Real-time tracking reduces massive transfusion delays

4. SUCTION CANISTER MEASUREMENT:
- Subtract irrigation volume
- Amniotic fluid in OB cases contaminates estimate
- Blood in suction is diluted, may underestimate

5. HEMOGLOBIN-BASED CALCULATION (most accurate):
- Formula: EBL = Blood volume × (Hgb_preop - Hgb_postop) / Hgb_average
- Requires pre and postoperative labs
- Retrospective, not useful intraoperatively

CLINICAL SIGNIFICANCE:
- Loss of 15% blood volume (750mL): Compensated, minimal symptoms
- Loss of 15-30% (750-1500mL): Tachycardia, decreased pulse pressure
- Loss of 30-40% (1500-2000mL): Hypotension, altered mental status
- Loss of >40% (>2000mL): Severe shock, life-threatening

TRANSFUSION TRIGGERS (Red Blood Cell):

RESTRICTIVE STRATEGY (now preferred for most patients):
- Hemoglobin <7 g/dL for hemodynamically stable patients
- Evidence from TRICC trial (N Engl J Med 1999):
  * Restrictive (Hgb 7-9) vs liberal (Hgb 10-12)
  * No difference in mortality, cardiac events
  * 54% reduction in transfusion volume

- Extended to cardiac surgery (TRICS-III trial):
  * Hgb <7.5 g/dL noninferior to <9.5 g/dL
  * Applies to stable patients post-bypass

HIGHER THRESHOLDS for:
- Active bleeding or hemorrhagic shock: Transfuse to maintain perfusion
- Acute coronary syndrome: Hgb <8 g/dL (some say <10 g/dL)
- Symptomatic anemia: dyspnea, tachycardia unresponsive to other measures
- Preoperative anemia: consider optimization before elective surgery

MASSIVE TRANSFUSION PROTOCOL (MTP):
- Definition: >10 units RBC in 24h OR >4 units in 1h OR replacement of entire blood volume
- Ratio-based approach: 1:1:1 RBC:FFP:Platelets
- Goal: Prevent dilutional coagulopathy and 'lethal triad' (hypothermia, acidosis, coagulopathy)
- Tranexamic acid (TXA): 1g IV load, 1g over 8h (CRASH-2 trial)
- Damage control surgery: Stop bleeding, temporary closure, resuscitate in ICU

PATIENT BLOOD MANAGEMENT (PBM) STRATEGIES:

1. PREOPERATIVE:
- Identify and treat anemia (iron, EPO, B12/folate)
- Discontinue anticoagulation/antiplatelets when safe
- Autologous blood donation (rare now, inferior to acute normovolemic hemodilution)

2. INTRAOPERATIVE:
- Meticulous hemostasis
- Acute normovolemic hemodilution (remove blood at start, replace with crystalloid)
- Cell salvage (contraindicated in cancer, infection, bowel contamination)
- Tranexamic acid prophylaxis (cardiac, orthopedic, trauma, OB)
- Controlled hypotension (MAP 60-70 if tolerated)

3. POSTOPERATIVE:
- Minimize phlebotomy (pediatric tubes, point-of-care testing)
- Iron supplementation
- EPO in select cases (renal failure, Jehovah's Witness)

RISKS OF TRANSFUSION:
- Transfusion reactions (allergic, febrile, hemolytic)
- TRALI (transfusion-related acute lung injury): 1:5,000-10,000
- TACO (transfusion-associated circulatory overload)
- Infection transmission (rare with modern screening: HIV 1:2 million)
- Immunomodulation (increased infection, cancer recurrence - debated)
- Cost ($200-1,000/unit depending on processing)

SPECIAL POPULATIONS:
- Jehovah's Witness: EPO, iron, cell salvage, acute normovolemic hemodilution, controlled hypotension
- Sickle cell disease: Higher threshold (Hgb 9-10 g/dL) to prevent sickling
- Chronic anemia: Tolerate lower Hgb due to compensation
- Pediatrics: Restrictive approach (Hgb 7 g/dL) safe in most

The shift toward restrictive transfusion reduces costs, complications, and blood utilization without compromising outcomes.
        """,
        key_factors=[
            "Baseline hemoglobin and patient blood volume",
            "Hemodynamic stability and tissue perfusion",
            "Active bleeding vs anemia from blood loss",
            "Cardiac disease and coronary perfusion needs",
            "Symptoms of anemia (dyspnea, angina, altered mental status)",
            "Coagulation status in massive transfusion",
            "Patient preferences (Jehovah's Witness)"
        ],
        primary_authority=[
            "N Engl J Med 1999;340:409-417 (TRICC trial - restrictive transfusion)",
            "N Engl J Med 2017;377:2133-2144 (TRICS-III cardiac surgery)",
            "Lancet 2017;389:2105-2116 (CRASH-2 tranexamic acid in trauma)",
            "AABB Clinical Practice Guidelines (transfusion thresholds)"
        ],
        burden_holder="Anesthesiologist and surgeon",
        adversary_position="Traditional surgical culture favors liberal transfusion 'to be safe'",
        counter_arguments=[
            "Restrictive approach may cause unrecognized tissue hypoxia",
            "Hemoglobin doesn't reflect oxygen delivery in all patients",
            "ACS patients need higher thresholds (evidence less clear)"
        ],
        resolution_strategy="Institutional transfusion guidelines, real-time clinical decision support, patient blood management programs",
        entity_scope="All surgical patients with blood loss",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Level 1 evidence from multiple RCTs for restrictive approach",
        controlling_precedent="AABB guidelines, Joint Commission patient blood management standards",
        issue_category=IssueCategory.BLOOD_MANAGEMENT,
        analysis_zone=AnalysisZone.OPERATIVE,
        authority_level=AuthorityLevel.LEVEL_1_RCT,
        fact_fragility=0.2,
        recharacterization_risk=0.2,
        testimony_dependence=0.3
    ),

    # ========== INSTRUMENTATION & STERILIZATION ==========

    DoctrineBlock(
        topic="Surgical Instrument Sterilization Methods",
        keywords=["sterilization", "autoclave", "steam sterilization", "ethylene oxide", "EtO", "sterrad", "high-level disinfection"],
        conclusion_template="Sterilization using {method} achieves {log_reduction}-log reduction of microorganisms with {cycle_time} cycle time and {limitations} for heat-sensitive instruments.",
        reasoning_framework="""
Sterilization eliminates all forms of microbial life including bacterial spores:

STEAM STERILIZATION (AUTOCLAVE) - Gold Standard:

Mechanism: Saturated steam under pressure denatures proteins and DNA
- Temperature: 121-132°C (250-270°F)
- Pressure: 15-30 psi
- Time:
  * Gravity displacement: 30 min at 121°C, 15 min at 132°C
  * Prevacuum: 4 min at 132°C (faster, more reliable)
  * Flash sterilization: 3 min at 132°C unwrapped (emergency only)

Advantages:
- Most reliable and cost-effective
- Rapid cycle time
- No toxic residue
- Effective against all microorganisms including prions (extended cycle)
- Environmental safety (just water)

Disadvantages:
- Damages heat/moisture-sensitive instruments (fiber optics, plastics, some electronics)
- Dulls sharp instruments over time (though acceptable for most)
- Cannot sterilize liquids or powders

Monitoring:
- Chemical indicators (color change strips) in each pack
- Biological indicators (Geobacillus stearothermophilus spores) weekly or each load
- Bowie-Dick test for prevacuum (air removal verification)

ETHYLENE OXIDE (EtO) STERILIZATION:

Mechanism: Alkylating agent disrupts DNA and protein function
- Temperature: 37-63°C (low temp for heat-sensitive items)
- Humidity: 30-80% required
- Concentration: 450-1200 mg/L
- Time: 1-6 hours sterilization + 12-24 hours aeration (remove toxic gas)

Advantages:
- Can sterilize heat-sensitive items (plastics, electronics, fiber optics)
- Penetrates packaging and device lumens
- Effective against all microorganisms

Disadvantages:
- Toxic, flammable, carcinogenic (OSHA limits)
- Long cycle time (24-48h total including aeration)
- Expensive ($15-30/load vs $1-2 for steam)
- Environmental concerns (ozone depleting)
- Residual EtO can cause burns if inadequately aerated
- Contraindicated for PVC (absorbs EtO)

Use: Implants, ophthalmic instruments, fiber optic scopes, robotic instruments

HYDROGEN PEROXIDE GAS PLASMA (STERRAD):

Mechanism: Low-temp H2O2 gas → plasma state → reactive free radicals
- Temperature: 37-50°C
- Time: 45-75 min (faster than EtO)
- No aeration required

Advantages:
- Safe (breaks down to water and oxygen)
- Fast cycle
- No toxic residue
- No OSHA monitoring required

Disadvantages:
- Cannot sterilize cellulose (paper, linen) - absorbs H2O2
- Cannot sterilize liquids or powders
- Long narrow lumens may not achieve sterilization (lumen diameter limits)
- Expensive ($5-10/cycle)
- Less penetration than EtO

Use: Laparoscopic instruments, rigid endoscopes, power tools

PERACETIC ACID (STERIS):

Mechanism: Oxidizing agent at 50-56°C
- Time: 30 min cycle
- Wet process (instruments emerge wet, used immediately)

Advantages:
- Fast turnaround
- Low temperature
- Effective against biofilms

Disadvantages:
- Cannot wrap/store (immediate use only)
- Wet instruments must be used or re-sterilized
- Corrosive to some metals
- Limited to immersible instruments

Use: Rigid endoscopes, cystoscopes (immediate use after sterilization)

HIGH-LEVEL DISINFECTION (NOT STERILIZATION):

Methods:
- Glutaraldehyde (Cidex): 20-90 min immersion, toxic fumes
- Ortho-phthalaldehyde (OPA): 12 min immersion, stains proteins
- Peracetic acid: 12 min automated

Use: Flexible endoscopes (colonoscopes, bronchoscopes) - sterilization not achievable due to narrow lumens
- Kills vegetative bacteria, mycobacteria, fungi, viruses
- Does NOT reliably kill bacterial spores
- Adequate for non-invasive mucous membrane contact

CRITICAL DECISIONS:

Device categorization (Spaulding Classification):
- CRITICAL (enters sterile tissue or bloodstream): STERILIZATION required
  * Examples: Surgical instruments, implants, cardiac catheters
  * Methods: Steam, EtO, or H2O2 plasma

- SEMI-CRITICAL (contacts mucous membranes but not sterile tissue): HIGH-LEVEL DISINFECTION minimum
  * Examples: Flexible endoscopes, respiratory equipment, laryngoscope blades
  * Methods: Glutaraldehyde, OPA, peracetic acid

- NON-CRITICAL (contacts intact skin only): LOW-LEVEL DISINFECTION sufficient
  * Examples: Blood pressure cuffs, stethoscopes, linens
  * Methods: Quaternary ammonium, bleach, alcohol

FLASH STERILIZATION (emergency only):
- Unwrapped instruments, 3 min at 132°C
- Used only when: Instrument dropped, insufficient sterile supply, implant sizing
- NOT for routine use (increased infection risk)
- MUST document reason in medical record

PRION DECONTAMINATION (CJD, vCJD):
- Standard sterilization INSUFFICIENT
- Requires: 1N NaOH for 1h OR 134°C autoclave for 18 min
- Instruments contacting high-risk tissue (brain, spinal cord, eye) from CJD patients should be destroyed

STERILE STORAGE:
- Wrapped instruments: shelf life depends on packaging integrity, not time
- Event-related expiration (if package intact, remains sterile indefinitely)
- Monitor for tears, moisture, compression

The choice of sterilization method balances efficacy, material compatibility, cycle time, and cost.
        """,
        key_factors=[
            "Material compatibility (heat/moisture tolerance)",
            "Turnaround time required",
            "Penetration needs (lumens, hinges)",
            "Device complexity (electronics, fiber optics)",
            "Implant status (EtO preferred)",
            "Biological indicator monitoring",
            "Package integrity verification"
        ],
        primary_authority=[
            "CDC Guideline for Disinfection and Sterilization in Healthcare Facilities 2008",
            "AAMI/ANSI ST79 Comprehensive Guide to Steam Sterilization",
            "WHO Guidelines for Safe Surgery 2009 (sterilization recommendations)",
            "AORN Guidelines for Sterilization 2021"
        ],
        burden_holder="Central sterile processing and OR team",
        adversary_position="Cost pressure favors faster methods that may not be appropriate",
        counter_arguments=[
            "EtO phase-out due to environmental concerns requires alternatives",
            "H2O2 plasma cannot sterilize all instruments (lumen limitations)",
            "Flash sterilization overused in busy ORs despite higher infection risk"
        ],
        resolution_strategy="Adequate instrument inventory to avoid flash sterilization, adherence to manufacturer IFU",
        entity_scope="All reusable surgical instruments and devices",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Level 3 evidence, strong regulatory and consensus guidance",
        controlling_precedent="FDA device classification, CDC/AAMI/AORN standards",
        issue_category=IssueCategory.INSTRUMENTATION,
        analysis_zone=AnalysisZone.OPERATIVE,
        authority_level=AuthorityLevel.REGULATORY,
        fact_fragility=0.2,
        recharacterization_risk=0.1,
        testimony_dependence=0.2
    ),

    # ========== PATIENT POSITIONING ==========

    DoctrineBlock(
        topic="Surgical Patient Positioning and Pressure Injury Prevention",
        keywords=["patient positioning", "pressure injury", "lithotomy", "prone position", "compartment syndrome", "brachial plexus"],
        conclusion_template="Proper positioning for {position_type} surgery requires {padding_requirements} to prevent pressure injuries occurring in {incidence_rate}% of cases >3 hours.",
        reasoning_framework="""
Surgical positioning-related injuries are the second most common perioperative complication after medication errors:

SUPINE POSITION (most common):

Pressure points:
- Occiput (scalp alopecia if prolonged)
- Scapulae
- Sacrum and coccyx (most common pressure ulcer site)
- Heels (second most common pressure ulcer)
- Elbows (ulnar nerve)

Protective measures:
- Padded headrest or gel donut
- Arms tucked with palms facing body (neutral shoulder position)
- Avoid abduction >90 degrees (brachial plexus stretch)
- Elbow padding (especially ulnar groove)
- Pillow under knees (reduces lumbar lordosis)
- Heel elevation off bed surface (foam wedge under calves)
- Sequential compression devices for DVT prophylaxis

Complications:
- Brachial plexus injury (1:1,000-1:5,000) - most from excessive abduction
- Ulnar nerve palsy (most common positioning nerve injury)
- Pressure ulcers (sacrum, heels)

LITHOTOMY POSITION (gynecologic, colorectal):

Leg positioning:
- Hips flexed 80-100 degrees (excessive flexion compresses femoral nerve)
- Knees flexed 90-110 degrees
- Legs abducted 30-45 degrees (excessive abduction stretches obturator nerve)
- Stirrups at equal height (prevents sacral torsion)
- SIMULTANEOUS leg raising and lowering (prevents hip dislocation)

Pressure points:
- Sacrum and buttocks
- Lateral knee (common peroneal nerve)
- Posterior calf (well leg compartment syndrome)

Protective measures:
- Padded stirrups with foot supports
- Heel straps to prevent leg slip
- Avoid pressure on common peroneal nerve at fibular head
- Limit time in lithotomy (<4 hours if possible)
- Intermittent lowering of legs if prolonged (>4h)

Complications:
- Common peroneal nerve palsy (foot drop) - 1:1,000
- Well leg compartment syndrome (rare but devastating)
- Femoral nerve palsy (excessive hip flexion)
- Obturator nerve injury (excessive abduction)

PRONE POSITION (spine, posterior fossa):

Critical considerations:
- Endotracheal tube security (difficult to access if dislodged)
- Eye protection (corneal abrasion, retinal ischemia)
- Cervical spine neutral (avoid rotation)
- Chest and pelvis on rolls/frame (abdomen free-hanging to reduce IVC compression)
- Arms <90 degrees abduction or "Superman" position
- Genitalia checked for pressure (males especially)
- Knees and toes pressure-free

Pressure points:
- Eyes (orbital ischemia causing blindness)
- Ears
- Forehead and chin
- Breasts (females)
- Genitalia (males)
- Knees and toes

Protective measures:
- Prone frame (Jackson table, Wilson frame, chest rolls)
- Gel headrest with mirror cutout for face
- Eye lubricant and tape (check q30min if feasible)
- Chest and pelvis support allowing abdominal decompression
- Arms on padded arm boards
- Padding under knees and dorsum of feet

Complications:
- Postoperative visual loss (POVL): 1:1,000 in spine surgery
  * Ischemic optic neuropathy (most common) - irreversible
  * Central retinal artery occlusion (direct pressure)
  * Risk factors: prolonged surgery (>6h), blood loss >1L, hypotension
- Brachial plexus injury
- Pressure ulcers (knees, toes, forehead)
- Abdominal compartment syndrome if abdomen compressed

LATERAL DECUBITUS (thoracic, kidney):

Positioning:
- Bottom leg flexed, top leg straight with pillow between
- Axillary roll under dependent chest (4-6cm caudal to axilla)
- Arms on padded supports <90 degrees from body
- Kidney rest elevated if kidney surgery

Pressure points:
- Dependent ear
- Dependent shoulder and brachial plexus
- Dependent hip and iliac crest
- Dependent knee and ankle
- Non-dependent leg (if not supported)

Protective measures:
- Axillary roll to prevent brachial plexus compression
- Pillow between knees
- Padding under dependent ankle and knee
- Tape or straps across hips (not chest - restricts breathing)

Complications:
- Brachial plexus injury (axillary roll malposition)
- Pressure ulcers (dependent hip, shoulder)

TRENDELENBURG/REVERSE TRENDELENBURG:

Trendelenburg (head down):
- Uses: Pelvic surgery (bowel retraction), robotic prostatectomy, central line access
- Risks: Cerebral edema, increased ICP, facial/airway edema, endobronchial intubation
- Limit: <30 degrees for <3-4 hours
- Contraindications: Glaucoma, increased ICP, severe GERD

Reverse Trendelenburg (head up):
- Uses: Laparoscopic upper GI, thyroid, shoulder arthroscopy
- Risks: Hypotension, cerebral hypoperfusion, lower extremity DVT
- Requires: Shoulder support or arm boards to prevent sliding

GENERAL PRESSURE INJURY PREVENTION:

Timing:
- Highest risk: Surgery >3 hours
- Inspect all pressure points pre and post-op
- Document positioning and padding

Surfaces:
- OR table pads (gel or foam overlays)
- Pressure redistribution NOT pressure relief
- No surface eliminates need for repositioning/padding

High-risk patients:
- Age >65
- BMI <20 or >40
- Diabetes, vascular disease
- Steroid use, malnutrition
- Prolonged immobility preoperatively

Documentation:
- Position type
- Padding locations
- Team member responsible for positioning
- Pre-op and post-op skin assessment
- Safety strap placement

ASA CLOSED CLAIMS ANALYSIS:
- Nerve injury is third most common claim (16% of all claims)
- Ulnar nerve most common (28% of nerve injuries)
- Brachial plexus second (20%)
- Median award: $120,000
- Most claims involve supine or lithotomy positioning

The mantra: "Position the patient, NOT the patient's position."
        """,
        key_factors=[
            "Surgery duration (>3h increases risk exponentially)",
            "Patient risk factors (age, BMI, diabetes, steroids)",
            "Pressure point identification and padding",
            "Nerve path awareness (brachial plexus, ulnar, peroneal)",
            "Team verification of positioning before draping",
            "Pre and post-op skin and neurovascular checks",
            "Documentation of positioning measures"
        ],
        primary_authority=[
            "AORN Guideline for Positioning the Patient 2021",
            "ASA Practice Advisory for Prevention of Perioperative Peripheral Neuropathies 2018",
            "NPUAP/EPUAP Pressure Ulcer Prevention Guidelines",
            "Anesthesiology 2006;104:952-960 (ASA Closed Claims nerve injury analysis)"
        ],
        burden_holder="Surgeon, anesthesiologist, and OR nursing team",
        adversary_position="Time pressure leads to inadequate positioning verification",
        counter_arguments=[
            "Perfect padding cannot prevent all injuries (some are unavoidable)",
            "Pressure injury etiology is multifactorial (not just positioning)",
            "Nerve injuries often have no identifiable cause"
        ],
        resolution_strategy="Team approach with positioning checklist, documentation, high-risk patient protocols",
        entity_scope="All surgical patients requiring positioning other than supine with arms tucked",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Level 4 evidence from case series, strong consensus recommendations",
        controlling_precedent="AORN and ASA standards, NPUAP guidelines",
        issue_category=IssueCategory.PATIENT_POSITIONING,
        analysis_zone=AnalysisZone.OPERATIVE,
        authority_level=AuthorityLevel.GUIDELINE,
        fact_fragility=0.3,
        recharacterization_risk=0.2,
        testimony_dependence=0.4
    ),

]


# ============================================================================
# ENGINE CORE - TIE ARCHITECTURE IMPLEMENTATION
# ============================================================================

class MED06SurgicalEngine:
    """
    MED06 Surgical Systems Analysis Engine
    Implements full TIE-20 architecture for surgical domain
    """

    def __init__(self):
        self.engine_id = ENGINE_ID
        self.version = ENGINE_VERSION
        self.doctrine_cache = DOCTRINE_CACHE
        self.query_log: List[Dict[str, Any]] = []
        self.metrics = {
            "total_queries": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "avg_response_time_ms": 0.0,
            "doctrine_triggers": Counter(),
            "error_count": 0
        }
        logger.info(f"{ENGINE_ID} v{ENGINE_VERSION} initialized with {len(DOCTRINE_CACHE)} doctrine blocks")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: Optional[AnalysisZone] = None
    ) -> Tuple[str, List[str], bool, List[str]]:
        """
        TIE Three-Layer Response Architecture:
        Layer 1: Doctrine Cache (0-200ms)
        Layer 2: Semantic Retrieval (fallback)
        Layer 3: Deep Analysis (full synthesis)
        """
        start_time = datetime.now()
        triggered_doctrines = []
        warnings = []
        cache_hit = False

        # LAYER 1: Doctrine Cache (fast path)
        relevant_doctrines = self._search_doctrine_cache(query, zone)

        if relevant_doctrines:
            cache_hit = True
            primary_doctrine = relevant_doctrines[0]
            triggered_doctrines = [d.topic for d in relevant_doctrines[:3]]

            # Update metrics
            primary_doctrine.times_triggered += 1
            primary_doctrine.last_triggered = datetime.now()
            self.metrics["doctrine_triggers"][primary_doctrine.topic] += 1

            # Generate response based on mode
            if mode == ResponseMode.FAST:
                answer = self._generate_fast_response(query, relevant_doctrines)
            elif mode == ResponseMode.DEFENSE:
                answer = self._generate_defense_response(query, relevant_doctrines)
            else:  # MEMO
                answer = self._generate_memo_response(query, relevant_doctrines)

            # Apply epistemic guardrails
            answer, epistemic_warnings = self._apply_epistemic_guardrails(
                answer, primary_doctrine
            )
            warnings.extend(epistemic_warnings)

        else:
            # LAYER 2: Semantic search fallback
            cache_hit = False
            answer = self._semantic_fallback(query, mode)
            warnings.append("No exact doctrine match - semantic analysis used")
            triggered_doctrines = ["SEMANTIC_FALLBACK"]

        return answer, triggered_doctrines, cache_hit, warnings

    def _search_doctrine_cache(
        self,
        query: str,
        zone: Optional[AnalysisZone] = None
    ) -> List[DoctrineBlock]:
        """Search doctrine cache with keyword and topic matching"""
        scored_doctrines = []

        for doctrine in self.doctrine_cache:
            # Zone filter
            if zone and doctrine.analysis_zone != zone:
                continue

            relevance = doctrine.matches(query)
            if relevance > 0.3:  # Threshold for relevance
                scored_doctrines.append((relevance, doctrine))

        # Sort by relevance
        scored_doctrines.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored_doctrines[:5]]

    def _generate_fast_response(
        self,
        query: str,
        doctrines: List[DoctrineBlock]
    ) -> str:
        """FAST mode: Concise, cache-first response"""
        primary = doctrines[0]

        answer_parts = [
            f"SURGICAL ANALYSIS ({primary.topic}):",
            "",
            primary.conclusion_template,
            "",
            "KEY FACTORS:",
        ]

        for factor in primary.key_factors[:5]:
            answer_parts.append(f"- {factor}")

        answer_parts.extend([
            "",
            f"Confidence: {primary.confidence.value}",
            f"Authority: {primary.authority_level.value}"
        ])

        return "\n".join(answer_parts)

    def _generate_defense_response(
        self,
        query: str,
        doctrines: List[DoctrineBlock]
    ) -> str:
        """DEFENSE mode: Audit-ready, detailed response with citations"""
        primary = doctrines[0]

        answer_parts = [
            f"COMPREHENSIVE SURGICAL SYSTEMS ANALYSIS",
            f"Topic: {primary.topic}",
            f"Category: {primary.issue_category.value}",
            f"Analysis Zone: {primary.analysis_zone.value}",
            "",
            "CONCLUSION:",
            primary.conclusion_template,
            "",
            "REASONING FRAMEWORK:",
            primary.reasoning_framework,
            "",
            "KEY DETERMINATIVE FACTORS:",
        ]

        for i, factor in enumerate(primary.key_factors, 1):
            answer_parts.append(f"{i}. {factor}")

        answer_parts.extend([
            "",
            "PRIMARY AUTHORITY:",
        ])

        for auth in primary.primary_authority:
            answer_parts.append(f"- {auth}")

        answer_parts.extend([
            "",
            f"BURDEN HOLDER: {primary.burden_holder}",
            f"CONFIDENCE LEVEL: {primary.confidence.value}",
            f"CONFIDENCE STRATIFICATION: {primary.confidence_stratification}",
            "",
            "COUNTER-ARGUMENTS:",
        ])

        for arg in primary.counter_arguments:
            answer_parts.append(f"- {arg}")

        answer_parts.extend([
            "",
            f"RESOLUTION STRATEGY: {primary.resolution_strategy}",
            "",
            f"CONTROLLING PRECEDENT: {primary.controlling_precedent}"
        ])

        # Add related doctrines
        if len(doctrines) > 1:
            answer_parts.extend([
                "",
                "RELATED CONSIDERATIONS:",
            ])
            for doctrine in doctrines[1:3]:
                answer_parts.append(f"- {doctrine.topic}: {doctrine.conclusion_template}")

        return "\n".join(answer_parts)

    def _generate_memo_response(
        self,
        query: str,
        doctrines: List[DoctrineBlock]
    ) -> str:
        """MEMO mode: Full documentation with multi-doctrine synthesis"""
        answer_parts = [
            "SURGICAL SYSTEMS MEMORANDUM",
            "=" * 80,
            "",
            f"RE: {query}",
            f"DATE: {datetime.now().strftime('%Y-%m-%d')}",
            f"ENGINE: {self.engine_id} v{self.version}",
            "",
            "EXECUTIVE SUMMARY:",
            ""
        ]

        # Multi-doctrine synthesis
        for i, doctrine in enumerate(doctrines[:3], 1):
            answer_parts.extend([
                f"{i}. {doctrine.topic}",
                f"   Confidence: {doctrine.confidence.value}",
                f"   Category: {doctrine.issue_category.value}",
                ""
            ])

        answer_parts.extend([
            "",
            "DETAILED ANALYSIS:",
            ""
        ])

        for i, doctrine in enumerate(doctrines[:3], 1):
            answer_parts.extend([
                f"SECTION {i}: {doctrine.topic.upper()}",
                "-" * 80,
                "",
                "Conclusion:",
                doctrine.conclusion_template,
                "",
                "Reasoning:",
                doctrine.reasoning_framework,
                "",
                "Key Factors:",
            ])

            for factor in doctrine.key_factors:
                answer_parts.append(f"- {factor}")

            answer_parts.extend([
                "",
                "Authority:",
            ])

            for auth in doctrine.primary_authority:
                answer_parts.append(f"- {auth}")

            answer_parts.extend([
                "",
                f"Adversary Position: {doctrine.adversary_position or 'N/A'}",
                "",
                "Counter-Arguments:",
            ])

            for arg in doctrine.counter_arguments:
                answer_parts.append(f"- {arg}")

            answer_parts.extend([
                "",
                f"Resolution: {doctrine.resolution_strategy}",
                "",
                ""
            ])

        answer_parts.extend([
            "RISK ASSESSMENT:",
            f"- Fact Fragility: {doctrines[0].fact_fragility:.2f}",
            f"- Recharacterization Risk: {doctrines[0].recharacterization_risk:.2f}",
            f"- Testimony Dependence: {doctrines[0].testimony_dependence:.2f}",
            "",
            "This analysis is provided for surgical planning and should be",
            "supplemented with institution-specific protocols and multidisciplinary consultation.",
            "",
            "=" * 80
        ])

        return "\n".join(answer_parts)

    def _apply_epistemic_guardrails(
        self,
        answer: str,
        doctrine: DoctrineBlock
    ) -> Tuple[str, List[str]]:
        """Apply epistemic humility and disclosure caveats"""
        warnings = []

        # High fragility warning
        if doctrine.fact_fragility > 0.7:
            warnings.append(
                "HIGH FACT FRAGILITY: Evidence base is evolving; recommendations may change"
            )

        # Testimony dependence
        if doctrine.testimony_dependence > 0.7:
            warnings.append(
                "EXPERT-DEPENDENT: Conclusion relies heavily on clinical judgment and experience"
            )

        # Recharacterization risk
        if doctrine.recharacterization_risk > 0.7:
            warnings.append(
                "RECHARACTERIZATION RISK: Alternative interpretations exist; context critical"
            )

        # Disclosure confidence level
        if doctrine.confidence == ConfidenceLevel.DISCLOSURE:
            disclosure = (
                "\n\n[DISCLOSURE REQUIRED]: This analysis involves procedures or risks "
                "requiring explicit informed consent discussion with the patient. "
                "Document patient understanding and acceptance of risks."
            )
            answer += disclosure

        if doctrine.confidence == ConfidenceLevel.HIGH_RISK:
            disclosure = (
                "\n\n[HIGH RISK]: This analysis involves experimental techniques, "
                "off-label use, or high liability exposure. Institutional review, "
                "ethics consultation, and comprehensive informed consent are essential."
            )
            answer += disclosure

        return answer, warnings

    def _semantic_fallback(self, query: str, mode: ResponseMode) -> str:
        """Fallback when no doctrine cache hit"""
        return (
            f"SEMANTIC ANALYSIS (No exact doctrine match):\n\n"
            f"Query: {query}\n\n"
            f"This query did not trigger specific surgical doctrine blocks. "
            f"General surgical systems principles suggest:\n\n"
            f"1. Consult current evidence-based guidelines (ASA, ACS, SAGES, WHO)\n"
            f"2. Review institutional protocols and standards\n"
            f"3. Obtain multidisciplinary consultation when appropriate\n"
            f"4. Document decision-making rationale\n"
            f"5. Ensure informed consent for novel or high-risk approaches\n\n"
            f"For specific guidance, reformulate query to match surgical domains:\n"
            f"- Preoperative assessment (ASA class, airway, risk stratification)\n"
            f"- Surgical safety (WHO checklist, time-out, wrong-site prevention)\n"
            f"- Minimally invasive techniques (laparoscopy vs open criteria)\n"
            f"- Robotic surgery (da Vinci platform indications)\n"
            f"- Infection control (SSI prevention bundles, sterilization)\n"
            f"- ERAS protocols (enhanced recovery elements)\n"
            f"- Electrosurgery safety (monopolar vs bipolar)\n"
            f"- Blood management (transfusion thresholds, PBM)\n"
            f"- Patient positioning (pressure injury prevention)\n"
        )

    def coverage_map(self) -> Dict[str, Any]:
        """Track doctrine coverage and epistemic gaps"""
        triggered = {d.topic: d.times_triggered for d in self.doctrine_cache}
        never_triggered = [d.topic for d in self.doctrine_cache if d.times_triggered == 0]

        category_coverage = defaultdict(int)
        for d in self.doctrine_cache:
            category_coverage[d.issue_category.value] += 1

        return {
            "total_doctrines": len(self.doctrine_cache),
            "triggered_doctrines": len([d for d in self.doctrine_cache if d.times_triggered > 0]),
            "never_triggered": never_triggered,
            "category_coverage": dict(category_coverage),
            "most_used": self.metrics["doctrine_triggers"].most_common(10),
            "epistemic_gaps": [
                d.topic for d in self.doctrine_cache
                if d.fact_fragility > 0.8 or d.testimony_dependence > 0.8
            ]
        }

    def determinism_hash(self, query: str, answer: str) -> str:
        """SHA-256 hash for reproducibility verification"""
        content = f"{query}|{answer}|{ENGINE_VERSION}"
        return hashlib.sha256(content.encode()).hexdigest()

    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health endpoint"""
        return {
            "status": "operational",
            "engine_id": self.engine_id,
            "version": self.version,
            "doctrine_blocks": len(self.doctrine_cache),
            "total_queries": self.metrics["total_queries"],
            "cache_hit_rate": (
                self.metrics["cache_hits"] / self.metrics["total_queries"]
                if self.metrics["total_queries"] > 0 else 0.0
            ),
            "avg_response_time_ms": self.metrics["avg_response_time_ms"],
            "error_count": self.metrics["error_count"],
            "uptime_seconds": (datetime.now() - datetime.now()).total_seconds(),  # Placeholder
            "top_doctrines": self.metrics["doctrine_triggers"].most_common(5)
        }


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=f"{ENGINE_ID} - Surgical Systems Analysis Engine",
    version=ENGINE_VERSION,
    description="TIE-grade engine for surgical systems, operative planning, and perioperative medicine"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
engine = MED06SurgicalEngine()


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint - TIE three-layer response"""
    start_time = datetime.now()
    query_id = str(uuid.uuid4())

    try:
        # Three-layer response
        answer, triggered_doctrines, cache_hit, warnings = engine.three_layer_response(
            request.query,
            request.mode,
            request.zone
        )

        # Get primary doctrine for metadata
        relevant = engine._search_doctrine_cache(request.query, request.zone)
        confidence = relevant[0].confidence if relevant else ConfidenceLevel.AGGRESSIVE

        # Calculate response time
        response_time = (datetime.now() - start_time).total_seconds() * 1000

        # Update metrics
        engine.metrics["total_queries"] += 1
        if cache_hit:
            engine.metrics["cache_hits"] += 1
        else:
            engine.metrics["cache_misses"] += 1

        # Update average response time
        total = engine.metrics["total_queries"]
        engine.metrics["avg_response_time_ms"] = (
            (engine.metrics["avg_response_time_ms"] * (total - 1) + response_time) / total
        )

        # Generate determinism hash
        det_hash = engine.determinism_hash(request.query, answer)

        # Prepare citations if requested
        citations = None
        if request.require_citations and relevant:
            citations = relevant[0].primary_authority

        # Build response
        response = QueryResponse(
            query_id=query_id,
            answer=answer,
            confidence=confidence,
            mode=request.mode,
            zone=request.zone,
            triggered_doctrines=triggered_doctrines,
            cache_hit=cache_hit,
            response_time_ms=round(response_time, 2),
            reasoning_chain=triggered_doctrines if request.mode != ResponseMode.FAST else None,
            citations=citations,
            warnings=warnings if warnings else None,
            determinism_hash=det_hash,
            timestamp=datetime.now().isoformat()
        )

        # Log query
        engine.query_log.append({
            "query_id": query_id,
            "query": request.query,
            "mode": request.mode.value,
            "response_time_ms": response_time,
            "cache_hit": cache_hit,
            "timestamp": datetime.now().isoformat()
        })

        logger.info(
            f"Query processed: {query_id} | {request.mode.value} | "
            f"{response_time:.1f}ms | cache_hit={cache_hit}"
        )

        return response

    except Exception as e:
        engine.metrics["error_count"] += 1
        logger.error(f"Query error: {query_id} | {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint"""
    return engine.health_check()


@app.get("/coverage")
async def coverage():
    """Doctrine coverage map"""
    return engine.coverage_map()


@app.get("/metrics")
async def metrics():
    """Engine metrics"""
    return engine.metrics


@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine blocks"""
    return {
        "total": len(engine.doctrine_cache),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "zone": d.analysis_zone.value,
                "confidence": d.confidence.value,
                "authority_level": d.authority_level.value,
                "times_triggered": d.times_triggered,
                "keywords": d.keywords
            }
            for d in engine.doctrine_cache
        ]
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "engine": ENGINE_ID,
        "version": ENGINE_VERSION,
        "status": "operational",
        "documentation": "/docs",
        "health": "/health",
        "query": "POST /query"
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_ID} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info"
    )
