"""
MED13 Pediatrics Analysis Engine v1.0.0
TIE-Grade Intelligence Engine for Pediatric Medicine

Covers: Pediatric diagnostics, growth/development assessment, immunization protocols,
neonatal care analysis, pediatric pharmacology dosing, childhood disease management.

Port: 9313
"""

import asyncio
import hashlib
import json
import re
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict, Counter

# CRITICAL: Add parent to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field
import uvicorn

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_VERSION = "1.0.0"
ENGINE_NAME = "MED13_PEDIATRICS"
PORT = 9313

# Configure loguru
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "logs" / "pediatrics_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(str, Enum):
    GROWTH_DEVELOPMENT = "GROWTH_DEVELOPMENT"
    IMMUNIZATION = "IMMUNIZATION"
    NEONATAL_CARE = "NEONATAL_CARE"
    PEDIATRIC_PHARMACOLOGY = "PEDIATRIC_PHARMACOLOGY"
    INFECTIOUS_DISEASE = "INFECTIOUS_DISEASE"
    DEVELOPMENTAL_DISORDERS = "DEVELOPMENTAL_DISORDERS"
    NUTRITION = "NUTRITION"
    RESPIRATORY = "RESPIRATORY"
    CARDIOLOGY = "CARDIOLOGY"
    NEUROLOGY = "NEUROLOGY"
    EMERGENCY = "EMERGENCY"
    CHRONIC_DISEASE = "CHRONIC_DISEASE"

class AnalysisZone(str, Enum):
    DIAGNOSTIC = "DIAGNOSTIC"
    TREATMENT = "TREATMENT"
    PREVENTIVE = "PREVENTIVE"

class QueryRequest(BaseModel):
    query: str = Field(..., description="Pediatric medicine question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    patient_age_months: Optional[int] = Field(None, description="Patient age in months")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional clinical context")

class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    category: IssueCategory
    zone: AnalysisZone
    fact_fragility_score: float = Field(ge=0.0, le=1.0)

class AnalysisResponse(BaseModel):
    query: str
    mode: ResponseMode
    answer: str
    confidence: ConfidenceLevel
    categories: List[IssueCategory]
    zone: AnalysisZone
    doctrines_triggered: List[str]
    reasoning_chain: List[str]
    authority_citations: List[str]
    determinism_hash: str
    telemetry: Dict[str, Any]
    epistemic_caveats: List[str]
    timestamp: str

# ============================================================================
# DOCTRINE CACHE - PEDIATRIC MEDICINE EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    # GROWTH & DEVELOPMENT
    DoctrineBlock(
        topic="Growth Chart Percentile Interpretation",
        keywords=["growth chart", "percentile", "height", "weight", "head circumference", "BMI", "growth velocity"],
        conclusion_template=[
            "Growth percentiles assess child's physical development relative to population norms",
            "Crossing two major percentile lines warrants further evaluation",
            "Consistent tracking along a percentile curve indicates normal growth pattern"
        ],
        reasoning_framework="""
        Growth assessment framework:
        1. Plot measurements on WHO (0-2y) or CDC (2-20y) growth charts
        2. Evaluate percentile rankings (3rd, 5th, 10th, 25th, 50th, 75th, 90th, 95th, 97th)
        3. Assess growth velocity over time
        4. Compare height/weight ratio to screen for nutritional issues
        5. Monitor head circumference in infants (microcephaly/macrocephaly)

        Red flags:
        - Crossing >2 major percentile lines upward or downward
        - Height <3rd percentile or >97th percentile
        - Weight-for-height discordance >2 percentile categories
        - Deceleration in head circumference growth
        - BMI >95th percentile (obesity) or <5th percentile (underweight)

        Normal variants:
        - Constitutional growth delay: slow growth with delayed bone age, family history
        - Familial short stature: proportionate short stature, normal bone age
        - Catch-up growth: rapid growth after illness or malnutrition correction
        """,
        key_factors=[
            "Age-appropriate growth chart selection",
            "Serial measurements over time",
            "Mid-parental height calculation",
            "Bone age assessment when indicated",
            "Nutritional intake evaluation",
            "Endocrine screening if abnormal pattern",
            "Genetic syndrome consideration"
        ],
        primary_authority=[
            "WHO Child Growth Standards (2006)",
            "CDC Growth Charts (2000)",
            "AAP Recommendations for Preventive Pediatric Health Care (2023)",
            "Growth Hormone Research Society Guidelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.GROWTH_DEVELOPMENT,
        zone=AnalysisZone.DIAGNOSTIC,
        fact_fragility_score=0.15
    ),

    DoctrineBlock(
        topic="Developmental Milestone Assessment",
        keywords=["milestones", "developmental delay", "motor skills", "language", "social", "cognitive", "Ages and Stages"],
        conclusion_template=[
            "Developmental screening identifies children at risk for delays requiring intervention",
            "Gross motor, fine motor, language, and social-emotional domains assessed separately",
            "Early intervention before age 3 years maximizes neuroplasticity benefits"
        ],
        reasoning_framework="""
        Milestone assessment approach:
        1. Use validated screening tools (ASQ, PEDS, M-CHAT for autism)
        2. Assess four developmental domains at each well-child visit
        3. Compare to age-expected milestones with 2-month windows
        4. Distinguish developmental delay from developmental disorder

        Key milestones by age:
        2 months: social smile, tracks objects, coos
        4 months: head control, reaches for objects, laughs
        6 months: sits with support, transfers objects, babbles
        9 months: crawls, pincer grasp, stranger anxiety
        12 months: stands alone, first words, follows simple commands
        18 months: walks independently, 10-word vocabulary, uses spoon
        24 months: runs, 50-word vocabulary, 2-word phrases, parallel play
        36 months: pedals tricycle, 200-word vocabulary, 3-word sentences, interactive play
        48 months: hops on one foot, draws person with 3 parts, tells stories
        60 months: skips, prints letters, counts to 10, friends important

        Red flags requiring immediate referral:
        - No babbling by 12 months
        - No single words by 16 months
        - No 2-word phrases by 24 months
        - Loss of previously acquired skills at any age
        - No social smile by 3 months
        - Hand preference before 18 months (may indicate hemiparesis)
        - Inability to walk by 18 months
        """,
        key_factors=[
            "Corrected age for prematurity until 24 months",
            "Parent concerns are highly predictive",
            "Cultural and linguistic considerations",
            "Standardized screening tool administration",
            "Early intervention referral pathways",
            "Medical causes evaluation (hearing, vision, metabolic)",
            "Autism spectrum disorder screening at 18 and 24 months"
        ],
        primary_authority=[
            "AAP Developmental Surveillance and Screening Guidelines (2020)",
            "CDC Developmental Milestones Checklist",
            "M-CHAT-R/F for Autism Screening",
            "ASQ-3 and ASQ:SE-2 Screening Tools"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.DEVELOPMENTAL_DISORDERS,
        zone=AnalysisZone.DIAGNOSTIC,
        fact_fragility_score=0.20
    ),

    # IMMUNIZATION
    DoctrineBlock(
        topic="Routine Childhood Immunization Schedule",
        keywords=["vaccine", "immunization", "CDC schedule", "catch-up", "contraindications", "ACIP"],
        conclusion_template=[
            "ACIP immunization schedule protects against 14 vaccine-preventable diseases",
            "Delayed vaccines require catch-up schedule following minimum intervals",
            "True contraindications are rare; anaphylaxis to previous dose is absolute contraindication"
        ],
        reasoning_framework="""
        Immunization schedule framework (CDC/ACIP 2024):

        Birth: Hepatitis B #1

        2 months: DTaP, IPV, Hib, PCV15/PCV20, Rotavirus, Hepatitis B #2

        4 months: DTaP, IPV, Hib, PCV15/PCV20, Rotavirus

        6 months: DTaP, IPV (6-18mo), Hib, PCV15/PCV20, Rotavirus, Hepatitis B #3 (6-18mo)

        12-15 months: MMR #1, Varicella #1, Hib, PCV15/PCV20

        15-18 months: DTaP #4

        12-23 months: Hepatitis A (2 doses, 6-18 months apart)

        4-6 years: DTaP #5, IPV #4, MMR #2, Varicella #2

        11-12 years: Tdap, HPV (2-3 doses), MenACWY #1

        16 years: MenACWY #2, MenB (2-3 doses)

        Annual: Influenza (6 months and older)

        Contraindications:
        - Anaphylaxis to vaccine component or previous dose
        - Encephalopathy within 7 days of pertussis vaccine
        - Severe immunodeficiency (live vaccines only)
        - Pregnancy (live vaccines only)

        Precautions (not contraindications):
        - Moderate/severe acute illness
        - Recent immunoglobulin administration (live vaccines)
        - Thrombocytopenia (MMR consideration)

        Common misconceptions (NOT contraindications):
        - Mild illness, low-grade fever
        - Antibiotic use
        - Egg allergy (influenza vaccine safe)
        - Family history of adverse events
        - Breastfeeding
        """,
        key_factors=[
            "Minimum intervals between doses",
            "Catch-up schedule for delayed vaccines",
            "Simultaneous administration safety",
            "Vaccine storage and handling requirements",
            "Documentation in state registry",
            "Parental education on expected side effects",
            "VAERS reporting for adverse events"
        ],
        primary_authority=[
            "CDC Immunization Schedule (2024)",
            "ACIP Recommendations",
            "AAP Red Book (2024)",
            "Vaccine Information Statements (VIS)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.IMMUNIZATION,
        zone=AnalysisZone.PREVENTIVE,
        fact_fragility_score=0.10
    ),

    # NEONATAL CARE
    DoctrineBlock(
        topic="Neonatal Jaundice Management",
        keywords=["jaundice", "hyperbilirubinemia", "phototherapy", "kernicterus", "bilirubin", "Coombs test"],
        conclusion_template=[
            "Physiologic jaundice peaks at 3-5 days and resolves by 2 weeks in term infants",
            "Phototherapy initiation based on hour-specific bilirubin nomogram and risk factors",
            "Severe hyperbilirubinemia requires urgent intervention to prevent kernicterus"
        ],
        reasoning_framework="""
        Neonatal jaundice assessment:

        Risk stratification:
        - Low risk: >=38 weeks, well, exclusive breastfeeding established
        - Medium risk: 38 weeks, well, some feeding issues
        - High risk: 35-37 6/7 weeks, hemolysis, significant bruising, cephalohematoma

        Jaundice onset timing:
        - <24 hours: PATHOLOGIC (hemolysis, infection) - immediate evaluation
        - 24-72 hours: Physiologic peak expected
        - >2 weeks (term) or >3 weeks (preterm): PROLONGED - evaluate for cholestasis

        Phototherapy thresholds (total serum bilirubin, mg/dL):

        Age 24h:
        - Low risk: 12, Medium: 10, High: 8

        Age 48h:
        - Low risk: 15, Medium: 13, High: 11

        Age 72h:
        - Low risk: 18, Medium: 16, High: 14

        Age 96h+:
        - Low risk: 20, Medium: 18, High: 15

        Exchange transfusion typically 4-5 mg/dL above phototherapy threshold

        Evaluation components:
        - Blood type and Coombs (mother and infant)
        - Total and direct bilirubin
        - Complete blood count with smear
        - G6PD if high-risk ethnicity
        - Sepsis workup if clinically indicated

        Direct hyperbilirubinemia (>1 mg/dL if total <5, or >20% of total):
        - Biliary atresia (acholic stools, dark urine)
        - Neonatal hepatitis
        - Metabolic disorders
        - Sepsis
        URGENT hepatology referral required
        """,
        key_factors=[
            "Hour-specific nomogram use",
            "Gestational age and risk factors",
            "Direct vs indirect bilirubin",
            "Hemolysis identification",
            "Adequate hydration and feeding",
            "Transcutaneous vs serum bilirubin",
            "Neurotoxicity risk assessment"
        ],
        primary_authority=[
            "AAP Clinical Practice Guideline for Hyperbilirubinemia (2022)",
            "Bhutani Nomogram",
            "AAP Subcommittee on Hyperbilirubinemia"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.NEONATAL_CARE,
        zone=AnalysisZone.TREATMENT,
        fact_fragility_score=0.12
    ),

    DoctrineBlock(
        topic="Neonatal Sepsis Evaluation",
        keywords=["sepsis", "fever", "neonate", "meningitis", "lumbar puncture", "blood culture", "GBS"],
        conclusion_template=[
            "Fever in neonate <28 days requires full sepsis workup and empiric antibiotics",
            "Group B Streptococcus and E. coli are most common early-onset pathogens",
            "Late-onset sepsis presentation more variable; consider HSV and viral etiologies"
        ],
        reasoning_framework="""
        Neonatal sepsis framework:

        Early-onset sepsis (0-72 hours):
        - Transmission: Vertical from maternal GBS, E. coli
        - Risk factors: Maternal fever, prolonged rupture of membranes >18h, chorioamnionitis, GBS colonization
        - Clinical: Respiratory distress, temperature instability, poor feeding, lethargy

        Late-onset sepsis (>72 hours to 28 days):
        - Transmission: Horizontal from environment, caregivers
        - Pathogens: GBS, E. coli, Listeria, Staph aureus, HSV, enteroviruses
        - Clinical: Fever (>38C rectal) or hypothermia, irritability, poor feeding, rash

        Full sepsis workup in febrile neonate <28 days:
        1. Blood culture (1-2 mL minimum)
        2. Urine culture (catheterized specimen, not bag)
        3. Lumbar puncture with CSF culture, cell count, glucose, protein
        4. Complete blood count with differential
        5. C-reactive protein (limited utility early)

        Empiric antibiotic therapy:
        - Ampicillin 50 mg/kg IV q8h (covers GBS, Listeria, Enterococcus)
        - Gentamicin 4-5 mg/kg IV q24h OR Cefotaxime 50 mg/kg IV q8h (covers E. coli, gram-negatives)
        - Add Acyclovir 20 mg/kg IV q8h if ANY concern for HSV (vesicles, seizures, CSF pleocytosis, maternal history)

        Meningitis dosing adjustments:
        - Ampicillin 100 mg/kg IV q6h
        - Cefotaxime 50 mg/kg IV q6h

        Well-appearing criteria (Rochester, Philadelphia, Boston criteria variations):
        - Term infant (>=37 weeks)
        - Previously healthy
        - Nontoxic appearance
        - No focal infection
        - WBC 5,000-15,000
        - Absolute band count <1,500
        - Urine <10 WBC/hpf
        - CSF <8 WBC (if obtained)

        Even well-appearing neonates <28 days typically hospitalized for observation
        """,
        key_factors=[
            "Age-specific risk stratification",
            "Maternal history review",
            "Temperature measurement method",
            "Lumbar puncture timing and technique",
            "Empiric coverage adequacy",
            "HSV consideration threshold",
            "Admission vs discharge decision"
        ],
        primary_authority=[
            "AAP Committee on Fetus and Newborn",
            "Pediatric Infectious Diseases Society Guidelines",
            "Rochester Criteria (1985)",
            "Step-by-Step Algorithm (2021)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.NEONATAL_CARE,
        zone=AnalysisZone.DIAGNOSTIC,
        fact_fragility_score=0.18
    ),

    # PEDIATRIC PHARMACOLOGY
    DoctrineBlock(
        topic="Weight-Based Medication Dosing",
        keywords=["dosing", "mg/kg", "pediatric dose", "maximum dose", "medication error", "pharmacokinetics"],
        conclusion_template=[
            "Pediatric medication doses calculated by weight prevent underdosing and toxicity",
            "Maximum adult dose applies even if weight-based calculation exceeds it",
            "Dose verification by second provider reduces medication errors"
        ],
        reasoning_framework="""
        Pediatric dosing principles:

        1. Weight-based calculation: dose (mg) = patient weight (kg) x dose (mg/kg)

        2. Maximum dose rule: Use lesser of weight-based dose or adult maximum dose

        3. Common medication doses:

        Acetaminophen:
        - 10-15 mg/kg PO/PR q4-6h (max 75 mg/kg/day, not to exceed 4000 mg/day)

        Ibuprofen:
        - 10 mg/kg PO q6-8h (max 40 mg/kg/day, not to exceed 2400 mg/day)

        Amoxicillin:
        - Standard: 40-45 mg/kg/day divided q8-12h
        - High-dose (otitis media, pneumonia): 80-90 mg/kg/day divided q12h
        - Max: 3000 mg/day

        Azithromycin:
        - Day 1: 10 mg/kg (max 500 mg)
        - Days 2-5: 5 mg/kg (max 250 mg)

        Ceftriaxone:
        - 50-100 mg/kg/day IV/IM q12-24h (max 4000 mg/day)
        - Meningitis: 100 mg/kg/day divided q12h

        Ondansetron:
        - 8-15 kg: 2 mg
        - 15-30 kg: 4 mg
        - >30 kg: 8 mg (adult dose)

        Epinephrine (anaphylaxis):
        - 0.01 mg/kg IM (1:1000 concentration = 0.01 mL/kg)
        - Max single dose: 0.5 mg

        Albuterol nebulizer:
        - <10 kg: 1.25 mg
        - 10-20 kg: 2.5 mg
        - >20 kg: 2.5-5 mg

        4. Age-specific considerations:
        - Neonates: Immature hepatic/renal function, longer dosing intervals
        - Infants: Higher metabolic rate, may need higher mg/kg doses
        - Obesity: Some drugs dosed on ideal body weight, others on actual weight

        5. High-risk medications requiring extra caution:
        - Digoxin, theophylline (narrow therapeutic index)
        - Chemotherapy agents (often per protocol)
        - Sedatives/opioids (respiratory depression risk)
        - Insulin (hypoglycemia risk)
        """,
        key_factors=[
            "Accurate current weight in kilograms",
            "Indication-specific dosing",
            "Renal/hepatic function assessment",
            "Drug-drug interaction check",
            "Age-appropriate formulation",
            "Independent double-check process",
            "Parent education on administration"
        ],
        primary_authority=[
            "AAP Pediatric Dosage Handbook",
            "Lexicomp Pediatric Drug Reference",
            "Harriet Lane Handbook (23rd Edition)",
            "WHO Model Formulary for Children"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PEDIATRIC_PHARMACOLOGY,
        zone=AnalysisZone.TREATMENT,
        fact_fragility_score=0.08
    ),

    # INFECTIOUS DISEASE
    DoctrineBlock(
        topic="Acute Otitis Media Diagnosis and Treatment",
        keywords=["ear infection", "otitis media", "otalgia", "tympanic membrane", "amoxicillin", "watchful waiting"],
        conclusion_template=[
            "AOM diagnosis requires acute onset, middle ear effusion, and inflammation signs",
            "High-dose amoxicillin remains first-line therapy for most cases",
            "Observation without antibiotics appropriate for select low-risk children over 6 months"
        ],
        reasoning_framework="""
        Acute otitis media (AOM) framework:

        Diagnostic criteria (all 3 required):
        1. Acute onset of symptoms (<48 hours)
        2. Middle ear effusion (bulging TM, limited mobility, air-fluid level, otorrhea)
        3. Middle ear inflammation (TM erythema, otalgia interfering with sleep/activity)

        Common pathogens:
        - Streptococcus pneumoniae (30-40%)
        - Haemophilus influenzae (20-30%)
        - Moraxella catarrhalis (10-15%)
        - Viral (20-30%)

        Treatment decision algorithm:

        Immediate antibiotics indicated:
        - Age <6 months (all cases)
        - Severe illness (otalgia >48h, temp >39C/102.2F)
        - Bilateral AOM in children <24 months
        - AOM with otorrhea

        Observation option (with close follow-up):
        - Age 6-24 months with unilateral, non-severe AOM
        - Age >=24 months with any non-severe AOM
        - Requires reliable parent, accessible follow-up
        - Reevaluate in 48-72 hours if no improvement

        First-line antibiotic therapy:
        - Amoxicillin 80-90 mg/kg/day divided q12h x 5-10 days
        - Duration: 10 days if <24 months or severe; 5-7 days if >=24 months and mild

        Amoxicillin-clavulanate 90 mg/kg/day (amoxicillin component) if:
        - Amoxicillin failure after 48-72 hours
        - Amoxicillin use in past 30 days
        - Concurrent purulent conjunctivitis
        - Recurrent AOM

        Penicillin allergy alternatives:
        - Non-type 1 (rash): Cefdinir, cefuroxime, cefpodoxime
        - Type 1 (anaphylaxis): Azithromycin or levofloxacin

        Treatment failure definition:
        - Persistent symptoms after 48-72 hours of therapy
        - Consider tympanocentesis for culture in multiple failures
        - Evaluate for mastoiditis, cholesteatoma, immunodeficiency

        Recurrent AOM (>=3 episodes in 6 months or >=4 in 12 months):
        - ENT referral for tympanostomy tube consideration
        - Address risk factors: daycare, smoke exposure, pacifier use, bottle propping
        """,
        key_factors=[
            "Pneumatic otoscopy skill",
            "Distinguishing AOM from OME",
            "Age-based treatment decisions",
            "Symptom severity assessment",
            "Antibiotic resistance patterns",
            "Parent reliability for observation",
            "Pain management with analgesics"
        ],
        primary_authority=[
            "AAP Clinical Practice Guideline for AOM (2013, reaffirmed 2022)",
            "Pediatric Infectious Diseases Society",
            "Cochrane Review on AOM Antibiotics"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.INFECTIOUS_DISEASE,
        zone=AnalysisZone.TREATMENT,
        fact_fragility_score=0.16
    ),

    DoctrineBlock(
        topic="Streptococcal Pharyngitis Management",
        keywords=["strep throat", "pharyngitis", "Centor criteria", "rapid strep", "penicillin", "rheumatic fever"],
        conclusion_template=[
            "Group A Streptococcus diagnosed by rapid antigen test or throat culture",
            "Penicillin or amoxicillin for 10 days prevents acute rheumatic fever",
            "Clinical scoring systems reduce unnecessary testing and antibiotic use"
        ],
        reasoning_framework="""
        Streptococcal pharyngitis approach:

        Modified Centor criteria (McIsaac score):
        - Fever >38C: +1 point
        - Absence of cough: +1 point
        - Tonsillar exudates: +1 point
        - Tender anterior cervical lymphadenopathy: +1 point
        - Age 3-14 years: +1 point
        - Age 15-44 years: 0 points
        - Age >=45 years: -1 point

        Testing recommendations:
        - Score 0-1: No testing, viral etiology likely
        - Score 2-3: Rapid antigen detection test (RADT)
        - Score >=4: Consider RADT or empiric treatment

        Diagnostic testing:
        - Rapid strep test: 95% specificity, 70-90% sensitivity
        - If RADT negative in child: Back-up throat culture recommended
        - If RADT negative in adult: No backup culture needed (lower prevalence)
        - Culture is gold standard: 90-95% sensitivity

        Treatment indications:
        - Positive RADT or culture
        - Prevents acute rheumatic fever (most important reason)
        - Reduces symptom duration by ~1 day
        - Decreases contagiousness
        - Prevents suppurative complications (peritonsillar abscess, retropharyngeal abscess)

        First-line antibiotic therapy:
        - Penicillin V 250 mg PO BID-TID x 10 days (child <27 kg)
        - Penicillin V 500 mg PO BID-TID x 10 days (child >=27 kg and adult)
        - Amoxicillin 50 mg/kg once daily (max 1000 mg) x 10 days (better taste, compliance)
        - Benzathine penicillin G 600,000 units IM once (if compliance concern) for <27 kg
        - Benzathine penicillin G 1.2 million units IM once for >=27 kg

        Penicillin allergy:
        - Non-severe: Cephalexin 20 mg/kg q12h x 10 days, Cefadroxil
        - Severe (anaphylaxis): Azithromycin 12 mg/kg once daily x 5 days (max 500 mg) OR Clindamycin

        Treatment failure:
        - Persistent symptoms after 48-72 hours
        - Consider non-compliance, resistant organism, re-exposure, carrier state
        - Alternative: Amoxicillin-clavulanate, cephalosporin, clindamycin

        Return to school/daycare:
        - After 24 hours of antibiotics and fever-free

        Complications prevented by treatment:
        - Acute rheumatic fever (rare in US but serious)
        - Post-streptococcal glomerulonephritis (NOT prevented by antibiotics)
        - Peritonsillar abscess
        - Cervical lymphadenitis
        - Scarlet fever progression
        """,
        key_factors=[
            "Clinical prediction rule application",
            "Test interpretation accuracy",
            "Ten-day treatment duration importance",
            "Compliance strategies",
            "Contact tracing for recurrent cases",
            "Carrier state recognition",
            "Tonsillectomy criteria if recurrent"
        ],
        primary_authority=[
            "IDSA Clinical Practice Guideline for Group A Strep Pharyngitis (2012)",
            "AAP Red Book Recommendations",
            "Cochrane Review on Antibiotics for Sore Throat"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.INFECTIOUS_DISEASE,
        zone=AnalysisZone.DIAGNOSTIC,
        fact_fragility_score=0.14
    ),

    # RESPIRATORY
    DoctrineBlock(
        topic="Asthma Severity Classification and Management",
        keywords=["asthma", "wheezing", "bronchodilator", "inhaled corticosteroid", "exacerbation", "controller", "rescue"],
        conclusion_template=[
            "Asthma severity guides initial controller therapy selection",
            "Inhaled corticosteroids are preferred controller medication for persistent asthma",
            "Asthma control assessment drives treatment step-up or step-down decisions"
        ],
        reasoning_framework="""
        Asthma classification and management:

        Severity classification (for initial treatment selection):

        Intermittent:
        - Symptoms <=2 days/week
        - Nighttime awakenings <=2x/month
        - SABA use <=2 days/week
        - No interference with activity
        - FEV1 >80% predicted
        Treatment: SABA as needed only

        Mild Persistent:
        - Symptoms >2 days/week but not daily
        - Nighttime awakenings 3-4x/month
        - SABA use >2 days/week but not daily
        - Minor activity limitation
        - FEV1 >80% predicted
        Treatment: Low-dose ICS or as-needed ICS-formoterol

        Moderate Persistent:
        - Daily symptoms
        - Nighttime awakenings >1x/week but not nightly
        - Daily SABA use
        - Some activity limitation
        - FEV1 60-80% predicted
        Treatment: Low-dose ICS-LABA or medium-dose ICS

        Severe Persistent:
        - Symptoms throughout day
        - Nighttime awakenings nightly or 7x/week
        - SABA use several times daily
        - Extremely limited activity
        - FEV1 <60% predicted
        Treatment: High-dose ICS-LABA plus consider add-on therapy

        Stepwise approach (0-11 years):

        Step 1: As-needed SABA only

        Step 2: Add low-dose ICS or SABA plus ICS each use

        Step 3: Medium-dose ICS OR low-dose ICS plus LABA (age >=4)

        Step 4: Medium-dose ICS-LABA, consider add-on (LTRA, theophylline)

        Step 5: High-dose ICS-LABA plus oral corticosteroid

        Step 6: High-dose ICS-LABA plus oral corticosteroid plus biologic (omalizumab if IgE-mediated)

        ICS dosing (fluticasone equivalent):
        - Low: 88-176 mcg/day (age 5-11), 100-200 mcg/day (age >=12)
        - Medium: 176-352 mcg/day (age 5-11), 200-500 mcg/day (age >=12)
        - High: >352 mcg/day (age 5-11), >500 mcg/day (age >=12)

        Acute exacerbation management:

        Mild (can speak sentences, no accessory muscles):
        - Albuterol 2-4 puffs q20min x 3 doses OR 2.5-5 mg nebulizer q20min x 3
        - If good response: Continue q3-4h PRN, PO corticosteroid if no controller therapy

        Moderate (speaks phrases, accessory muscles, SpO2 90-95%):
        - Albuterol q20min x 3 doses plus ipratropium 0.5 mg nebulizer
        - Oral corticosteroid (prednisolone 1-2 mg/kg, max 60 mg) for 3-5 days
        - Consider ED/urgent care evaluation

        Severe (speaks words, accessory muscles, SpO2 <90%, drowsy):
        - Immediate ED transfer
        - Continuous albuterol nebulizer
        - Ipratropium
        - IV/PO corticosteroid
        - Supplemental oxygen
        - Consider IV magnesium sulfate
        - Consider terbutaline, heliox, BiPAP, ICU if refractory
        """,
        key_factors=[
            "Spirometry for diagnosis in age >=5 years",
            "Controller medication adherence",
            "Inhaler technique assessment",
            "Trigger identification and avoidance",
            "Asthma action plan for every patient",
            "Annual influenza vaccination",
            "Step-down attempt if controlled >=3 months"
        ],
        primary_authority=[
            "NHLBI Asthma Guidelines (2020)",
            "GINA Global Strategy for Asthma (2024)",
            "AAP Recommendations for Pediatric Asthma"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.RESPIRATORY,
        zone=AnalysisZone.TREATMENT,
        fact_fragility_score=0.13
    ),

    DoctrineBlock(
        topic="Bronchiolitis Clinical Management",
        keywords=["bronchiolitis", "RSV", "wheezing infant", "respiratory distress", "supportive care"],
        conclusion_template=[
            "Bronchiolitis is clinical diagnosis in infants with first wheezing episode and URI prodrome",
            "Supportive care with hydration and oxygen is mainstay; bronchodilators not routinely indicated",
            "Hospitalization criteria include hypoxemia, dehydration, apnea, or high-risk factors"
        ],
        reasoning_framework="""
        Bronchiolitis management framework:

        Definition and epidemiology:
        - Age <24 months with first episode of wheezing
        - Viral URI prodrome (rhinorrhea, cough) followed by wheezing and respiratory distress
        - Peak incidence: November-March (RSV season)
        - Most common cause: RSV (70%), also rhinovirus, parainfluenza, adenovirus, metapneumovirus

        Clinical presentation:
        - Prodrome: Rhinorrhea, congestion, cough, low-grade fever (1-3 days)
        - Progressive: Tachypnea, wheezing, crackles, increased work of breathing
        - Respiratory distress signs: Nasal flaring, intercostal/subcostal retractions, grunting
        - Feeding difficulty, decreased urine output
        - Hypoxemia in severe cases

        High-risk factors for severe disease:
        - Age <12 weeks (especially <6 weeks)
        - Prematurity (<37 weeks, especially <32 weeks or <29 weeks)
        - Chronic lung disease (BPD)
        - Hemodynamically significant congenital heart disease
        - Immunodeficiency
        - Neurologic disease

        Diagnostic testing:
        - Clinical diagnosis; testing not routinely needed
        - Viral testing (RSV, multiplex PCR): For hospitalized patients, cohorting, palivizumab eligibility
        - Chest X-ray: NOT routine; consider if uncertain diagnosis, severe distress, concern for complication

        Treatment approach:

        Supportive care (ONLY proven effective therapies):
        1. Hydration: Oral preferred if tolerating; IV/NG if dehydrated or unable to feed
        2. Oxygen: Maintain SpO2 >=90% (some guidelines >=88% acceptable if otherwise well)
        3. Suctioning: Nasal saline drops plus bulb suction, especially before feeds
        4. Monitoring: Respiratory rate, work of breathing, hydration status

        NOT RECOMMENDED (evidence shows no benefit):
        - Albuterol/bronchodilators: No consistent benefit, AAP recommends against routine use
        - Systemic corticosteroids: Not effective
        - Racemic epinephrine: May cause transient improvement but no impact on outcomes
        - Chest physiotherapy: No benefit
        - Antibiotics: Unless concurrent bacterial infection (rare)
        - Ribavirin: Reserved for immunocompromised only

        Hospitalization criteria:
        - SpO2 <90% on room air (persistently)
        - Moderate-severe respiratory distress
        - Apnea or apnea history
        - Dehydration or inability to maintain oral intake (<50% normal)
        - Age <3 months (especially <6 weeks)
        - High-risk underlying condition
        - Caregiver inability to manage at home

        Discharge criteria:
        - SpO2 >=90% on room air
        - Adequate oral intake
        - Improving respiratory distress
        - Reliable caregiver with transportation
        - Close follow-up arranged

        Prevention:
        - Palivizumab (Synagis) for high-risk infants during RSV season
        - Nirsevimab (Beyfortus) - new long-acting monoclonal for all infants <8 months entering first RSV season
        - Hand hygiene, avoid sick contacts, no smoking exposure
        """,
        key_factors=[
            "First wheezing episode distinction",
            "Avoiding unnecessary interventions",
            "Dehydration assessment",
            "Hypoxemia monitoring",
            "Parent education on course",
            "RSV prophylaxis eligibility",
            "Return precautions counseling"
        ],
        primary_authority=[
            "AAP Clinical Practice Guideline for Bronchiolitis (2014, update 2024 pending)",
            "Cochrane Reviews on Bronchiolitis Interventions",
            "Choosing Wisely Recommendations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.RESPIRATORY,
        zone=AnalysisZone.TREATMENT,
        fact_fragility_score=0.11
    ),

    # NUTRITION
    DoctrineBlock(
        topic="Infant Feeding and Breastfeeding Support",
        keywords=["breastfeeding", "formula", "lactation", "newborn feeding", "weight loss", "jaundice"],
        conclusion_template=[
            "Exclusive breastfeeding recommended for first 6 months with continued breastfeeding through 12 months",
            "Newborn weight loss up to 7% expected; >10% requires feeding evaluation",
            "Iron-fortified formula is acceptable alternative when breastfeeding not possible"
        ],
        reasoning_framework="""
        Infant feeding framework:

        Breastfeeding recommendations:
        - Exclusive breastfeeding 0-6 months
        - Continued breastfeeding through 12 months and beyond as mutually desired
        - Benefits: Optimal nutrition, immune protection, maternal-infant bonding, reduced SIDS risk

        Early breastfeeding support:
        - Initiate within first hour after birth (skin-to-skin)
        - Rooming-in to allow on-demand feeding
        - No supplements unless medically indicated
        - Lactation consultant support for all mothers

        Normal newborn feeding pattern:
        - Day 1: 1-2 feedings (colostrum, small volume)
        - Day 2: 2-3 feedings
        - Day 3: 8-12 feedings per 24 hours
        - Feed every 2-3 hours, or on demand
        - 10-15 minutes per breast, or until infant satisfied

        Adequacy assessment:
        - Weight: 5-7% loss normal, back to birth weight by 2 weeks
        - Wet diapers: 6+ per day by day 5-6
        - Stools: Yellow, seedy by day 5; 3-4+ per day initially
        - Feeding duration: 10-20 minutes total
        - Infant contentment between feeds

        Excessive weight loss (>7-10%):
        - Assess latch, positioning, milk transfer
        - Check for tongue-tie (ankyloglossia)
        - Evaluate maternal milk production
        - Consider supplementation if >10% loss: Expressed breast milk > donor milk > formula
        - Close follow-up until weight gain established

        Medical indications for supplementation:
        - Hypoglycemia unresponsive to breastfeeding alone
        - Dehydration (>10% weight loss, hypernatremia)
        - Severe hyperbilirubinemia
        - Maternal medications incompatible with breastfeeding (chemotherapy, radioactive compounds)

        Formula feeding:
        - Iron-fortified cow milk formula for most infants
        - Standard concentration: 20 cal/oz
        - Volume: 1.5-3 oz per feed in first weeks, advancing to 6-8 oz by 6 months
        - Total: ~2-2.5 oz/lb/day (150 mL/kg/day)
        - NO cow milk, goat milk, or homemade formula before 12 months

        Special formulas:
        - Soy formula: Galactosemia, vegetarian preference (NOT for milk protein allergy)
        - Extensively hydrolyzed: Cow milk protein allergy (CMPA)
        - Amino acid-based: Severe CMPA, eosinophilic disorders
        - Lactose-free: Temporary after severe gastroenteritis (rare indication)

        Introduction of solids:
        - Start at 4-6 months (preferably 6 months if exclusively breastfed)
        - Developmental readiness: Sits with support, head control, interest in food
        - Iron-rich foods first: Iron-fortified cereal, pureed meats
        - Introduce one new food every 3-5 days
        - Continue breast milk or formula as primary nutrition until 12 months

        Complementary feeding principles:
        - Variety of textures and flavors
        - Family foods modified for infant
        - Self-feeding encouraged
        - Avoid honey before 12 months (botulism risk)
        - Avoid choking hazards (whole grapes, nuts, popcorn, hot dogs)
        - No juice before 12 months; limit to 4 oz/day after
        """,
        key_factors=[
            "Latch assessment",
            "Maternal milk supply evaluation",
            "Infant weight monitoring",
            "Tongue-tie identification",
            "Cultural feeding practices",
            "Vitamin D supplementation",
            "Iron supplementation if exclusively breastfed beyond 4 months"
        ],
        primary_authority=[
            "AAP Policy on Breastfeeding (2022)",
            "WHO Infant Feeding Recommendations",
            "Academy of Breastfeeding Medicine Protocols",
            "USDA Dietary Guidelines for Infants"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.NUTRITION,
        zone=AnalysisZone.PREVENTIVE,
        fact_fragility_score=0.17
    ),

    # EMERGENCY MEDICINE
    DoctrineBlock(
        topic="Pediatric Febrile Seizure Management",
        keywords=["febrile seizure", "fever", "convulsion", "recurrence risk", "epilepsy", "lumbar puncture"],
        conclusion_template=[
            "Simple febrile seizures are benign events with excellent prognosis",
            "Lumbar puncture indicated if meningeal signs or age <12 months with incomplete immunization",
            "Recurrence risk 30% but does not increase epilepsy risk in otherwise normal children"
        ],
        reasoning_framework="""
        Febrile seizure framework:

        Definition:
        - Seizure associated with fever (>=38C/100.4F)
        - Age 6 months to 5 years
        - No CNS infection, metabolic abnormality, or prior afebrile seizures
        - Incidence: 2-5% of children

        Simple febrile seizure (90-95%):
        - Generalized tonic-clonic
        - Duration <15 minutes
        - Does not recur within 24 hours
        - No postictal focal neurologic deficits

        Complex febrile seizure (5-10%):
        - Focal features (one side of body, head/eye deviation)
        - Duration >=15 minutes
        - Recurs within 24 hours (or same febrile illness)
        - Postictal paralysis (Todd paralysis)

        Emergency management:
        - Position on side, protect from injury
        - Do NOT restrain or place objects in mouth
        - Time the seizure duration
        - If >5 minutes: Benzodiazepine (lorazepam 0.1 mg/kg IV/IM, midazolam 0.2 mg/kg IN/IM, diazepam 0.3 mg/kg PR)
        - Assess for fever source and treat

        Diagnostic evaluation:

        Lumbar puncture indications:
        - Meningeal signs (nuchal rigidity, Kernig/Brudzinski sign, bulging fontanelle)
        - Concern for meningitis (ill-appearing, petechiae, prolonged altered mental status)
        - Age <12 months: Strongly consider (may not have classic meningeal signs)
        - Age 12-18 months: Consider if incomplete vaccination (especially Hib, pneumococcal)
        - Age >18 months: Not routinely indicated if well-appearing, no meningeal signs

        Neuroimaging (CT/MRI):
        - NOT routinely indicated for simple febrile seizure
        - Consider if: Focal seizure, postictal focal deficit, concern for trauma, neurocutaneous disorder

        EEG:
        - NOT routinely indicated
        - Does not predict recurrence or epilepsy risk
        - Consider if: Prolonged postictal state, concern for afebrile seizure, multiple complex features

        Laboratory studies:
        - Identify fever source (urine, blood cultures as indicated)
        - Electrolytes if severe vomiting/diarrhea, concern for electrolyte imbalance
        - Glucose if prolonged altered mental status

        Prognosis and recurrence:
        - Overall recurrence risk: 30-40%
        - Higher recurrence risk: Age <18 months at first seizure, family history, lower fever at seizure, shorter duration of fever before seizure
        - Risk of epilepsy: 1-2% (similar to general population) if simple febrile seizures only
        - Risk of epilepsy increased if: Complex features, neurodevelopmental abnormalities, family history of epilepsy

        Parent education:
        - Febrile seizures are scary but typically benign
        - Seizure itself does not cause brain damage
        - Aggressive fever reduction does NOT prevent recurrence
        - How to manage if seizure recurs: Position safely, time duration, call 911 if >5 minutes
        - No activity restrictions needed

        Prophylactic anticonvulsants:
        - NOT recommended for simple febrile seizures
        - Daily phenobarbital or valproate reduces recurrence but has significant side effects
        - Rescue diazepam (rectal or nasal) for prolonged or recurrent seizures in select cases
        """,
        key_factors=[
            "Simple vs complex distinction",
            "Age-based LP decision-making",
            "Immunization history review",
            "Fever source identification",
            "Family history of epilepsy",
            "Parental anxiety management",
            "Recurrence risk counseling"
        ],
        primary_authority=[
            "AAP Clinical Practice Guideline for Febrile Seizures (2011)",
            "American Academy of Neurology Practice Parameter",
            "Febrile Seizures Guideline Team"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.EMERGENCY,
        zone=AnalysisZone.DIAGNOSTIC,
        fact_fragility_score=0.19
    ),

    # Additional doctrines for comprehensive coverage
    DoctrineBlock(
        topic="Attention-Deficit/Hyperactivity Disorder Diagnosis",
        keywords=["ADHD", "attention deficit", "hyperactivity", "inattention", "Vanderbilt", "DSM-5"],
        conclusion_template=[
            "ADHD diagnosis requires symptoms in multiple settings causing functional impairment",
            "Behavior rating scales from parents and teachers are essential diagnostic tools",
            "Comorbid conditions such as learning disabilities and anxiety disorders are common"
        ],
        reasoning_framework="""
        ADHD diagnostic framework (DSM-5 criteria):

        Three presentations:
        1. Predominantly Inattentive
        2. Predominantly Hyperactive-Impulsive
        3. Combined (most common)

        Diagnostic criteria:
        - Age of onset: Symptoms present before age 12
        - Duration: Symptoms for >=6 months
        - Settings: Symptoms in >=2 settings (home, school, activities)
        - Impairment: Clear evidence of interference with functioning
        - Not better explained by another disorder

        Inattention symptoms (>=6 for age <17, >=5 for age >=17):
        - Fails to give close attention to details, careless mistakes
        - Difficulty sustaining attention in tasks or play
        - Does not seem to listen when spoken to directly
        - Does not follow through on instructions, fails to finish
        - Difficulty organizing tasks and activities
        - Avoids tasks requiring sustained mental effort
        - Loses things necessary for tasks
        - Easily distracted by extraneous stimuli
        - Forgetful in daily activities

        Hyperactivity-Impulsivity symptoms (>=6 for age <17, >=5 for age >=17):
        - Fidgets, squirms in seat
        - Leaves seat when remaining seated expected
        - Runs/climbs inappropriately (restlessness in adolescents/adults)
        - Unable to play quietly
        - Always on the go, as if driven by motor
        - Talks excessively
        - Blurts out answers before questions completed
        - Difficulty waiting turn
        - Interrupts or intrudes on others

        Evaluation process:
        1. Comprehensive history: Developmental, medical, family, psychosocial
        2. Rating scales: Vanderbilt, Conners, NICHQ (from parent AND teacher)
        3. Physical exam: Rule out medical causes (vision, hearing, thyroid, sleep disorders)
        4. School performance review: Grades, standardized testing, IEP/504 plan
        5. Comorbidity screening: Learning disabilities, anxiety, depression, ODD, autism

        Differential diagnosis:
        - Normal developmental variation
        - Learning disabilities
        - Anxiety disorders
        - Depression
        - Autism spectrum disorder
        - Sleep disorders
        - Hearing/vision impairment
        - Thyroid disorder
        - Lead exposure
        - Adverse childhood experiences/trauma

        Common comorbidities (present in 60-80%):
        - Learning disabilities (30-50%)
        - Oppositional defiant disorder (40-60%)
        - Anxiety disorders (30-40%)
        - Depression (20-30%)
        - Autism spectrum disorder (20-50% overlap)

        Treatment approach (multimodal):

        Preschool (age 4-5):
        - Behavior therapy FIRST (parent training)
        - Methylphenidate if severe impairment and behavior therapy insufficient

        School-age (6-11):
        - FDA-approved medication AND behavior therapy
        - School accommodations (504 plan or IEP)

        Adolescents:
        - FDA-approved medication with adolescent's assent
        - Behavior therapy less evidence but still recommended

        Medication options:

        Stimulants (first-line, 70-80% response):
        - Methylphenidate: Short-acting (Ritalin 2.5-10 mg BID-TID), Long-acting (Concerta 18-54 mg QAM)
        - Amphetamine: Short-acting (Adderall 5-30 mg BID), Long-acting (Adderall XR, Vyvanse)
        - Start low, titrate weekly based on response

        Non-stimulants:
        - Atomoxetine (Strattera): 0.5-1.2 mg/kg/day, takes 4-6 weeks
        - Guanfacine XR (Intuniv): 1-4 mg QAM
        - Clonidine XR (Kapvay): 0.1-0.4 mg

        Monitoring:
        - Height, weight, blood pressure, heart rate every 3-6 months
        - Rating scales every 3-6 months to assess response
        - Academic and social functioning
        - Side effects: Appetite suppression, sleep disturbance, tics, mood changes
        """,
        key_factors=[
            "Multi-informant assessment",
            "Symptom duration and pervasiveness",
            "Functional impairment documentation",
            "Comorbidity identification",
            "School collaboration",
            "Medication monitoring",
            "Behavior therapy access"
        ],
        primary_authority=[
            "AAP Clinical Practice Guideline for ADHD (2019)",
            "DSM-5 Diagnostic Criteria",
            "NICE Guidelines on ADHD"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.DEVELOPMENTAL_DISORDERS,
        zone=AnalysisZone.DIAGNOSTIC,
        fact_fragility_score=0.22
    ),

    DoctrineBlock(
        topic="Pediatric Dehydration Assessment and Fluid Management",
        keywords=["dehydration", "gastroenteritis", "oral rehydration", "IV fluids", "hyponatremia", "hypernatremia"],
        conclusion_template=[
            "Dehydration severity guides rehydration strategy: oral preferred for mild-moderate",
            "Isotonic IV fluids are standard for severe dehydration or shock",
            "Rapid correction of hypernatremic dehydration risks cerebral edema"
        ],
        reasoning_framework="""
        Pediatric dehydration framework:

        Dehydration severity assessment:

        Mild (3-5% weight loss):
        - Slightly dry mucous membranes
        - Normal vital signs
        - Normal urine output
        - Alert and responsive

        Moderate (6-9% weight loss):
        - Dry mucous membranes
        - Decreased tears
        - Sunken eyes, sunken fontanelle (infant)
        - Delayed capillary refill (2-3 seconds)
        - Decreased skin turgor
        - Decreased urine output
        - Irritable or lethargic

        Severe (>=10% weight loss):
        - Very dry mucous membranes
        - Absent tears
        - Deeply sunken eyes/fontanelle
        - Prolonged capillary refill (>3 seconds)
        - Tenting skin turgor
        - Minimal or no urine output
        - Altered mental status, weak pulse
        - Tachycardia, hypotension (late sign)

        Clinical Dehydration Scale (validated):
        - Appearance: Normal (0), Thirsty/restless (1), Lethargic (2)
        - Eyes: Normal (0), Slightly sunken (1), Very sunken (2)
        - Mucous membranes: Moist (0), Sticky (1), Dry (2)
        - Tears: Present (0), Decreased (1), Absent (2)
        Score 0: No dehydration
        Score 1-4: Some dehydration
        Score 5-8: Moderate to severe dehydration

        Fluid deficit calculation:
        Deficit (mL) = % dehydration x weight (kg) x 1000
        Example: 10 kg child with 5% dehydration = 0.05 x 10 x 1000 = 500 mL deficit

        Oral rehydration therapy (ORT):

        Indications: Mild to moderate dehydration, able to tolerate oral intake

        Solution: Oral rehydration solution (ORS) such as Pedialyte
        - Composition: 45-90 mEq/L sodium, 20 g/L glucose (optimal for absorption)
        - NOT: Sports drinks (too much sugar, too little sodium), juice, soda

        Rehydration phase (first 4 hours):
        - 50 mL/kg for mild dehydration
        - 100 mL/kg for moderate dehydration
        - Give frequently in small volumes: 5 mL every 2-5 minutes
        - Advance as tolerated

        Maintenance phase (ongoing losses):
        - 10 mL/kg for each diarrheal stool
        - 2 mL/kg for each emesis
        - Continue usual diet, do not restrict

        Antiemetics to facilitate ORT:
        - Ondansetron 0.15 mg/kg PO (max 8 mg) x 1 dose
        - Allows successful ORT in 70-80% of vomiting children

        IV fluid therapy:

        Indications:
        - Severe dehydration or shock
        - Persistent vomiting despite ORT and antiemetic
        - Altered mental status
        - Ileus or surgical abdomen
        - Failed ORT

        Resuscitation (if shock):
        - 20 mL/kg bolus of isotonic fluid (NS or LR) over 20 minutes
        - Reassess, repeat boluses as needed
        - Monitor for fluid overload

        Deficit replacement (after shock corrected):
        - Replace over 24-48 hours
        - Add maintenance fluids
        - Formula: Deficit + Maintenance + Ongoing losses

        Maintenance fluid calculation (Holliday-Segar):
        - 100 mL/kg/day for first 10 kg
        - 50 mL/kg/day for next 10 kg (11-20 kg)
        - 20 mL/kg/day for each kg >20 kg

        Fluid composition:
        - Isotonic saline (0.9% NS) for deficit replacement
        - 0.45% NS with 20 mEq/L KCl after urine output established (maintenance)
        - 5% dextrose added if unable to take PO

        Special considerations:

        Hypernatremic dehydration (Na >150 mEq/L):
        - Correct SLOWLY over 48 hours
        - Risk: Too rapid correction causes cerebral edema
        - Maximum Na decrease: 10-12 mEq/L per 24 hours

        Hyponatremic dehydration (Na <130 mEq/L):
        - Usually from free water replacement of isotonic losses
        - Risk: Seizures if severe (<120 mEq/L)
        - Isotonic saline for correction
        - If symptomatic: 3% saline 2-4 mL/kg over 10 minutes
        """,
        key_factors=[
            "Weight-based severity assessment",
            "ORT attempt before IV fluids",
            "Isotonic fluid for resuscitation",
            "Electrolyte monitoring",
            "Ongoing loss replacement",
            "Hypernatremia correction rate",
            "Return to normal diet early"
        ],
        primary_authority=[
            "AAP Clinical Practice Guideline for Acute Gastroenteritis (2016)",
            "WHO Diarrhea Treatment Guidelines",
            "CDC Oral Rehydration Therapy Recommendations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.EMERGENCY,
        zone=AnalysisZone.TREATMENT,
        fact_fragility_score=0.14
    ),

    DoctrineBlock(
        topic="Sudden Infant Death Syndrome Prevention",
        keywords=["SIDS", "safe sleep", "back to sleep", "co-sleeping", "suffocation", "sleep position"],
        conclusion_template=[
            "Supine sleep position reduces SIDS risk by 50%",
            "Room-sharing without bed-sharing recommended for first 6-12 months",
            "Soft bedding, bumpers, and prone positioning increase SIDS risk"
        ],
        reasoning_framework="""
        SIDS prevention framework:

        AAP safe sleep recommendations:

        1. BACK TO SLEEP for every sleep (naps and nighttime):
        - Supine position until 12 months of age
        - Side sleeping not safe (can roll to prone)
        - Once infant can roll both ways, supine start but allow to find comfortable position

        2. Firm sleep surface:
        - Crib, bassinet, or play yard with firm mattress
        - Fitted sheet only
        - NO adult beds, couches, armchairs, waterbeds, pillows

        3. Room-sharing WITHOUT bed-sharing:
        - Infant sleeps in parents' room for at least 6 months, ideally 12 months
        - Separate sleep surface (crib/bassinet beside parent bed)
        - Reduces SIDS risk by 50%

        4. Keep soft objects out of sleep area:
        - NO pillows, blankets, quilts, bumper pads, stuffed animals
        - Sleep sack or wearable blanket preferred over loose blankets
        - If blanket used: Thin, tucked under mattress, reaches only to chest

        5. Pacifier use:
        - Offer at nap and bedtime after breastfeeding established (3-4 weeks)
        - Protective even if falls out after sleep onset
        - Do not force if infant refuses
        - Do not reinsert after infant asleep

        6. Avoid overheating:
        - Room temperature comfortable for lightly clothed adult
        - One layer more than adult wears
        - No hat indoors
        - Signs of overheating: Sweating, damp hair, flushed cheeks, heat rash

        7. Avoid smoke exposure:
        - No smoking during pregnancy
        - No smoking in home or car
        - Keep infant away from smokers

        8. Avoid alcohol and illicit drug use:
        - Impairs arousal, increases bed-sharing risk

        9. Breastfeeding:
        - Protective effect against SIDS
        - Any duration better than none

        10. Prenatal care:
        - Regular prenatal visits associated with reduced SIDS risk

        11. Immunizations:
        - Up-to-date vaccines associated with 50% SIDS reduction

        12. Supervised tummy time when awake:
        - Prevents positional plagiocephaly
        - Strengthens neck/shoulder muscles
        - Start from birth, 3-5 minutes 2-3x daily, increase as tolerated

        NOT RECOMMENDED:
        - Home cardiorespiratory monitors for SIDS prevention
        - Wedges, positioners (risk of suffocation)
        - Crib bumpers (no safety benefit, suffocation risk)
        - Swaddling after 8 weeks or when rolling attempts begin

        High-risk situations:
        - Bed-sharing: Especially on soft surface, with smoker, alcohol/drug use, extreme fatigue
        - Couch/armchair sleeping: 50x higher risk than crib
        - Prone or side sleeping
        - Prematurity
        - Second-hand smoke exposure
        - No prenatal care

        SIDS epidemiology:
        - Peak age: 2-4 months (90% occur <6 months)
        - Higher risk: Males, Native American/Alaska Native, African American
        - Decreased since Back to Sleep campaign (1994): 50% reduction
        - Current rate: ~40 deaths per 100,000 live births
        """,
        key_factors=[
            "Consistent supine positioning",
            "Room-sharing education",
            "Bed-sharing risk counseling",
            "Swaddling cessation timing",
            "Smoking cessation support",
            "Safe sleep environment audit",
            "Cultural practice discussions"
        ],
        primary_authority=[
            "AAP Policy on Safe Sleep and SIDS Prevention (2022)",
            "NICHD Safe to Sleep Campaign",
            "CDC Sudden Unexpected Infant Death Guidelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.NEONATAL_CARE,
        zone=AnalysisZone.PREVENTIVE,
        fact_fragility_score=0.09
    ),
]

# ============================================================================
# SEMANTIC NORMALIZATION
# ============================================================================

TERM_NORMALIZATIONS = {
    # Measurements
    "inches": "in.",
    "inch": "in.",
    "centimeters": "cm",
    "centimeter": "cm",
    "kilograms": "kg",
    "kilogram": "kg",
    "pounds": "lbs",
    "pound": "lb",

    # Growth terms
    "growth curve": "growth chart",
    "percentile ranking": "percentile",
    "head size": "head circumference",
    "OFC": "head circumference",

    # Developmental terms
    "developmental screening": "milestone assessment",
    "language delay": "speech delay",
    "gross motor": "large motor",
    "fine motor": "small motor",

    # Vaccine terms
    "vaccination": "immunization",
    "shot": "vaccine",
    "MMR": "measles mumps rubella",
    "DTaP": "diphtheria tetanus pertussis",

    # Disease terms
    "ear infection": "otitis media",
    "strep throat": "streptococcal pharyngitis",
    "RSV": "respiratory syncytial virus",
    "stomach flu": "gastroenteritis",

    # Common abbreviations
    "ADHD": "attention deficit hyperactivity disorder",
    "ASD": "autism spectrum disorder",
    "URI": "upper respiratory infection",
    "UTI": "urinary tract infection",
}

def normalize_query(text: str) -> str:
    """Normalize pediatric terminology for consistent matching."""
    normalized = text.lower()
    for term, replacement in TERM_NORMALIZATIONS.items():
        normalized = re.sub(r'\b' + re.escape(term.lower()) + r'\b', replacement, normalized)
    return normalized

# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class TelemetryCollector:
    def __init__(self):
        self.query_count = 0
        self.doctrine_hits = Counter()
        self.category_distribution = Counter()
        self.response_times = []
        self.error_count = 0

    def record_query(self, categories: List[IssueCategory], doctrines: List[str], duration_ms: float):
        self.query_count += 1
        for cat in categories:
            self.category_distribution[cat.value] += 1
        for doc in doctrines:
            self.doctrine_hits[doc] += 1
        self.response_times.append(duration_ms)

    def record_error(self):
        self.error_count += 1

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_queries": self.query_count,
            "total_errors": self.error_count,
            "avg_response_time_ms": sum(self.response_times) / len(self.response_times) if self.response_times else 0,
            "most_common_categories": dict(self.category_distribution.most_common(5)),
            "most_triggered_doctrines": dict(self.doctrine_hits.most_common(5)),
        }

telemetry = TelemetryCollector()

# ============================================================================
# DOCTRINE MATCHING ENGINE
# ============================================================================

def match_doctrines(query: str, patient_age_months: Optional[int] = None) -> List[DoctrineBlock]:
    """Match relevant doctrine blocks based on query keywords and patient age."""
    normalized_query = normalize_query(query)
    query_words = set(normalized_query.split())

    matches = []
    for doctrine in DOCTRINE_CACHE:
        # Keyword matching
        keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in normalized_query)

        # Age-specific filtering
        age_relevant = True
        if patient_age_months is not None:
            # Example age filtering logic
            if "neonatal" in doctrine.topic.lower() and patient_age_months > 1:
                age_relevant = False
            elif "infant" in doctrine.topic.lower() and patient_age_months > 24:
                age_relevant = False

        if keyword_matches >= 2 and age_relevant:
            matches.append((doctrine, keyword_matches))

    # Sort by relevance
    matches.sort(key=lambda x: x[1], reverse=True)
    return [m[0] for m in matches[:5]]  # Top 5 matches

# ============================================================================
# THREE-LAYER RESPONSE SYSTEM
# ============================================================================

def doctrine_cache_lookup(query: str, patient_age_months: Optional[int]) -> Optional[str]:
    """Layer 1: Fast doctrine cache lookup (0-200ms)."""
    matched_doctrines = match_doctrines(query, patient_age_months)
    if matched_doctrines:
        top_doctrine = matched_doctrines[0]
        return " ".join(top_doctrine.conclusion_template)
    return None

def semantic_retrieval(query: str) -> str:
    """Layer 2: Semantic vector search (200-2000ms)."""
    # Placeholder for vector search integration
    return "Semantic retrieval would provide additional context from knowledge base."

def deep_analysis(query: str, matched_doctrines: List[DoctrineBlock], mode: ResponseMode) -> str:
    """Layer 3: Deep multi-source synthesis (2000ms+)."""
    if not matched_doctrines:
        return "Insufficient doctrine coverage for this query. Consult pediatric specialist."

    primary = matched_doctrines[0]

    if mode == ResponseMode.FAST:
        response = f"CLINICAL ASSESSMENT:\n{' '.join(primary.conclusion_template)}\n\n"
        response += f"KEY FACTORS: {', '.join(primary.key_factors[:3])}"

    elif mode == ResponseMode.DEFENSE:
        response = f"CLINICAL ASSESSMENT:\n{' '.join(primary.conclusion_template)}\n\n"
        response += f"REASONING FRAMEWORK:\n{primary.reasoning_framework}\n\n"
        response += f"KEY FACTORS:\n" + "\n".join(f"- {kf}" for kf in primary.key_factors) + "\n\n"
        response += f"AUTHORITATIVE SOURCES:\n" + "\n".join(f"- {auth}" for auth in primary.primary_authority)

    else:  # MEMO
        response = f"PEDIATRIC CLINICAL MEMORANDUM\n\n"
        response += f"TOPIC: {primary.topic}\n"
        response += f"CATEGORY: {primary.category.value}\n"
        response += f"ZONE: {primary.zone.value}\n\n"
        response += f"CLINICAL ASSESSMENT:\n{' '.join(primary.conclusion_template)}\n\n"
        response += f"DETAILED REASONING FRAMEWORK:\n{primary.reasoning_framework}\n\n"
        response += f"CRITICAL FACTORS:\n" + "\n".join(f"{i+1}. {kf}" for i, kf in enumerate(primary.key_factors)) + "\n\n"
        response += f"AUTHORITATIVE SOURCES:\n" + "\n".join(f"- {auth}" for auth in primary.primary_authority) + "\n\n"

        if len(matched_doctrines) > 1:
            response += f"RELATED CONSIDERATIONS:\n"
            for doc in matched_doctrines[1:3]:
                response += f"- {doc.topic}: {doc.conclusion_template[0]}\n"

    return response

# ============================================================================
# MAIN QUERY PROCESSOR
# ============================================================================

async def process_query(request: QueryRequest) -> AnalysisResponse:
    """Main entry point for pediatric analysis queries."""
    start_time = datetime.now()

    try:
        # Layer 1: Doctrine cache
        cache_result = doctrine_cache_lookup(request.query, request.patient_age_months)

        # Match all relevant doctrines
        matched_doctrines = match_doctrines(request.query, request.patient_age_months)

        # Determine response based on mode
        if request.mode == ResponseMode.FAST and cache_result:
            answer = cache_result
        else:
            answer = deep_analysis(request.query, matched_doctrines, request.mode)

        # Extract metadata
        categories = list(set(d.category for d in matched_doctrines)) if matched_doctrines else []
        zone = matched_doctrines[0].zone if matched_doctrines else AnalysisZone.DIAGNOSTIC
        confidence = matched_doctrines[0].confidence if matched_doctrines else ConfidenceLevel.DISCLOSURE

        # Epistemic caveats
        epistemic_caveats = [
            "This analysis is for educational purposes and does not constitute medical advice",
            "Individual patient circumstances may require different approaches",
            "Consult with a board-certified pediatrician for specific clinical decisions"
        ]

        # Determinism hash
        hash_input = f"{request.query}|{request.mode}|{ENGINE_VERSION}"
        determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        # Telemetry
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        telemetry.record_query(categories, [d.topic for d in matched_doctrines], duration_ms)

        response = AnalysisResponse(
            query=request.query,
            mode=request.mode,
            answer=answer,
            confidence=confidence,
            categories=categories,
            zone=zone,
            doctrines_triggered=[d.topic for d in matched_doctrines],
            reasoning_chain=[d.reasoning_framework[:200] + "..." for d in matched_doctrines[:2]],
            authority_citations=[auth for d in matched_doctrines for auth in d.primary_authority][:5],
            determinism_hash=determinism_hash,
            telemetry={
                "processing_time_ms": duration_ms,
                "doctrines_evaluated": len(DOCTRINE_CACHE),
                "doctrines_matched": len(matched_doctrines),
                "patient_age_months": request.patient_age_months,
            },
            epistemic_caveats=epistemic_caveats,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

        logger.info(f"Query processed: {request.query[:50]}... | Mode: {request.mode} | Duration: {duration_ms:.2f}ms")
        return response

    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        telemetry.record_error()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="MED13 Pediatrics Analysis Engine",
    description="TIE-Grade Intelligence Engine for Pediatric Medicine",
    version=ENGINE_VERSION
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@APP.post("/query", response_model=AnalysisResponse)
async def query_endpoint(request: QueryRequest):
    """Primary query endpoint for pediatric analysis."""
    return await process_query(request)

@APP.get("/health")
async def health_check():
    """Comprehensive health check endpoint."""
    stats = telemetry.get_stats()
    return {
        "status": "healthy",
        "engine": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": PORT,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "categories": [c.value for c in IssueCategory],
        "telemetry": stats,
        "uptime_queries": telemetry.query_count,
    }

@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics."""
    return {
        "total_doctrines": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "zone": d.zone.value,
                "keywords": d.keywords[:5],
            }
            for d in DOCTRINE_CACHE
        ]
    }

@APP.get("/")
async def root():
    """Root endpoint with engine information."""
    return {
        "engine": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "description": "TIE-Grade Pediatrics Analysis Engine",
        "port": PORT,
        "endpoints": {
            "query": "/query (POST)",
            "health": "/health (GET)",
            "doctrines": "/doctrines (GET)",
        }
    }

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")

    uvicorn.run(
        APP,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
