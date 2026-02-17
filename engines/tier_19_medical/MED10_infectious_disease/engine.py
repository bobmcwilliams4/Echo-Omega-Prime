"""
MED10 Infectious Disease Analysis Engine v1.0.0
TIE-Grade Intelligence Engine for Infectious Disease Clinical Decision Support

Port: 9235
Domain: Antimicrobial stewardship, sepsis management, diagnostic microbiology,
        infection control, antimicrobial resistance patterns

Authority: IDSA guidelines, Surviving Sepsis Campaign, CDC NHSN criteria,
          DHHS HIV/AIDS guidelines, WHO resistance surveillance
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field


# ============================================================================
# ENUMS & DATA MODELS
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
    SEPSIS_MANAGEMENT = "SEPSIS_MANAGEMENT"
    ANTIMICROBIAL_STEWARDSHIP = "ANTIMICROBIAL_STEWARDSHIP"
    DIAGNOSTIC_MICROBIOLOGY = "DIAGNOSTIC_MICROBIOLOGY"
    INFECTION_CONTROL = "INFECTION_CONTROL"
    ANTIMICROBIAL_RESISTANCE = "ANTIMICROBIAL_RESISTANCE"
    HIV_TREATMENT = "HIV_TREATMENT"
    TB_MANAGEMENT = "TB_MANAGEMENT"
    HEALTHCARE_ASSOCIATED_INFECTIONS = "HEALTHCARE_ASSOCIATED_INFECTIONS"
    IMMUNOCOMPROMISED_HOST = "IMMUNOCOMPROMISED_HOST"
    ANTIBIOTIC_DOSING = "ANTIBIOTIC_DOSING"
    BLOOD_CULTURE_INTERPRETATION = "BLOOD_CULTURE_INTERPRETATION"
    CDIFF_MANAGEMENT = "CDIFF_MANAGEMENT"


class AnalysisZone(str, Enum):
    ACUTE_MANAGEMENT = "ACUTE_MANAGEMENT"
    STEWARDSHIP_REVIEW = "STEWARDSHIP_REVIEW"
    INFECTION_CONTROL_AUDIT = "INFECTION_CONTROL_AUDIT"


@dataclass
class DoctrineBlock:
    """Individual doctrine block with clinical reasoning"""
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
    controlling_precedent: str
    issue_category: IssueCategory
    zone: AnalysisZone


@dataclass
class QueryMetrics:
    """Telemetry data for each query"""
    query_id: str
    timestamp: float
    mode: ResponseMode
    cache_hit: bool
    cache_latency_ms: float
    semantic_latency_ms: float
    deep_latency_ms: float
    total_latency_ms: float
    doctrines_triggered: List[str]
    confidence_level: ConfidenceLevel
    error_domain: Optional[str] = None


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., description="Clinical question or scenario")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    patient_context: Optional[Dict[str, Any]] = Field(default=None, description="Patient-specific factors")
    zone: Optional[AnalysisZone] = Field(default=None, description="Clinical context zone")


class QueryResponse(BaseModel):
    query_id: str
    answer: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    doctrines_applied: List[str]
    authorities_cited: List[str]
    reasoning_chain: Optional[List[str]] = None
    latency_ms: float
    determinism_hash: str
    epistemic_caveats: List[str]
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrine_count: int
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float
    uptime_seconds: float


# ============================================================================
# DOCTRINE CACHE - 25+ REAL INFECTIOUS DISEASE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Sepsis-3 Criteria and qSOFA Screening",
        keywords=["sepsis", "qsofa", "sofa", "sirs", "organ dysfunction", "septic shock", "lactate"],
        conclusion_template=[
            "Sepsis-3 criteria define sepsis as life-threatening organ dysfunction caused by dysregulated host response to infection (SOFA score increase >=2 points).",
            "qSOFA (quick SOFA) is a bedside screening tool: altered mental status, SBP <=100 mmHg, respiratory rate >=22/min; 2+ suggests sepsis risk.",
            "Septic shock requires vasopressors to maintain MAP >=65 mmHg AND lactate >2 mmol/L despite adequate fluid resuscitation."
        ],
        reasoning_framework="""
1. SIRS criteria (1991) overly sensitive, replaced by Sepsis-3 (2016) focusing on organ dysfunction
2. SOFA score components: PaO2/FiO2, platelets, bilirubin, MAP/vasopressors, GCS, creatinine/urine output
3. qSOFA designed for rapid screening outside ICU, NOT diagnostic, triggers full SOFA assessment
4. Lactate >2 mmol/L indicates tissue hypoperfusion, >4 mmol/L severe shock
5. Sequential organ failure assessment (SOFA) baseline score 0, increase >=2 defines sepsis
6. Septic shock mortality 40%, sepsis without shock 10-20%
7. Early recognition (within 1 hour) critical for outcomes per Surviving Sepsis Campaign
8. Do NOT delay antibiotics to obtain cultures if sepsis suspected
9. Blood cultures x2 sets (aerobic + anaerobic) before antibiotics if possible within 45 min
10. Procalcitonin (PCT) >0.5 ng/mL supports bacterial infection, guides antibiotic duration
11. qSOFA score 0-1: low risk, 2-3: high risk, triggers ICU evaluation
12. Hypotension (SBP <90 or MAP <65) requires immediate fluid resuscitation 30 mL/kg crystalloid
13. Central venous pressure (CVP) monitoring controversial, dynamic measures (pulse pressure variation) preferred
14. Surviving Sepsis 1-hour bundle: lactate, blood cultures, broad-spectrum antibiotics, 30 mL/kg crystalloid if hypotensive
15. SOFA cardiovascular: MAP <70 = 1, dopamine <5 or dobutamine = 2, dopamine 5-15 or epi/norepi <=0.1 = 3, >15 or >0.1 = 4
16. Renal SOFA: Cr 1.2-1.9 = 1, 2.0-3.4 = 2, 3.5-4.9 = 3, >5.0 = 4
17. Coagulation SOFA: platelets <150 = 1, <100 = 2, <50 = 3, <20 = 4
18. Hepatic SOFA: bilirubin 1.2-1.9 = 1, 2.0-5.9 = 2, 6.0-11.9 = 3, >=12.0 = 4
19. Neurologic SOFA: GCS 13-14 = 1, 10-12 = 2, 6-9 = 3, <6 = 4
20. Respiratory SOFA: PaO2/FiO2 <400 = 1, <300 = 2, <200 with vent = 3, <100 with vent = 4
21. Sepsis-induced hypotension defined as SBP <90 mmHg or SBP decrease >40 mmHg from baseline
22. Cryptic shock: lactate >2 mmol/L without hypotension, still requires aggressive resuscitation
23. Time to antibiotics: every hour delay increases mortality 7.6% (Kumar et al.)
24. Source control (drain abscess, remove infected device) essential, ideally within 12 hours
25. Norepinephrine first-line vasopressor, target MAP 65 mmHg, add vasopressin or epinephrine if refractory
        """,
        key_factors=[
            "SOFA score increase >=2 points from baseline",
            "qSOFA: 2+ of altered mental status, SBP <=100, RR >=22",
            "Lactate >2 mmol/L with vasopressor need defines septic shock",
            "1-hour bundle: cultures, antibiotics, lactate, 30 mL/kg fluid if hypotensive",
            "Time to antibiotics directly correlates with mortality",
            "Source control within 12 hours when indicated"
        ],
        primary_authority=[
            "Sepsis-3 Consensus Definitions (JAMA 2016)",
            "Surviving Sepsis Campaign Guidelines 2021",
            "Singer M et al. JAMA 2016;315(8):801-810"
        ],
        burden_holder="Clinician identifying and treating sepsis",
        adversary_position="Over-diagnosis leads to unnecessary antibiotics and resistance",
        counter_arguments=[
            "qSOFA less sensitive than SIRS for early sepsis detection",
            "SOFA requires lab values not available at bedside",
            "Lactate can be elevated from non-septic causes (seizure, liver disease, metformin)"
        ],
        resolution_strategy="Use qSOFA for rapid screening, confirm with full SOFA, initiate empiric antibiotics within 1 hour if suspected sepsis regardless of score",
        entity_scope="All patients with suspected infection in acute care settings",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High-quality RCT and consensus guidelines, universally accepted criteria",
        controlling_precedent="Sepsis-3 definitions (2016) supersede Sepsis-1 (1991) and Sepsis-2 (2001)",
        issue_category=IssueCategory.SEPSIS_MANAGEMENT,
        zone=AnalysisZone.ACUTE_MANAGEMENT
    ),

    DoctrineBlock(
        topic="Empiric Antibiotic Selection for Sepsis",
        keywords=["empiric antibiotics", "broad spectrum", "source control", "piperacillin-tazobactam", "vancomycin", "cefepime", "meropenem"],
        conclusion_template=[
            "Empiric antibiotics must cover likely pathogens based on infection source, local resistance patterns, and patient risk factors.",
            "Combination therapy typically vancomycin (MRSA coverage) + broad-spectrum beta-lactam (piperacillin-tazobactam, cefepime, or carbapenem).",
            "De-escalate based on culture results and clinical response within 48-72 hours per antimicrobial stewardship principles."
        ],
        reasoning_framework="""
1. Source-directed therapy: UTI (gram-negatives, Enterococcus), pneumonia (S. pneumoniae, H. influenzae, atypicals), intra-abdominal (anaerobes + gram-negatives)
2. Hospital-acquired/healthcare-associated infections require broader coverage for Pseudomonas, MRSA, resistant gram-negatives
3. Vancomycin 15-20 mg/kg IV q8-12h for MRSA coverage (pneumonia, skin/soft tissue, endocarditis), target trough 15-20 mcg/mL for serious infections
4. Piperacillin-tazobactam 3.375g-4.5g IV q6h covers Pseudomonas, anaerobes, most Enterobacterales, but NOT ESBL or AmpC producers
5. Cefepime 2g IV q8h covers Pseudomonas, Enterobacterales, S. pneumoniae, but NOT anaerobes or ESBL
6. Meropenem 1g IV q8h for ESBL, severe sepsis, or critically ill; avoid overuse to prevent carbapenem resistance
7. Azithromycin 500mg IV x1 or fluoroquinolone for atypical coverage in severe pneumonia
8. Immunocompromised patients need antifungal coverage (echinocandin or amphotericin) if febrile neutropenia
9. Linezolid 600mg IV q12h alternative to vancomycin for MRSA pneumonia (better lung penetration)
10. Ceftriaxone 2g IV q24h suitable for community-acquired infections without MRSA/Pseudomonas risk
11. Metronidazole 500mg IV q8h for anaerobic coverage if not using pip-tazo or carbapenem
12. Aminoglycosides (gentamicin, tobramycin) for synergy in endocarditis or severe Pseudomonas, monitor nephrotoxicity
13. Fluoroquinolones (levofloxacin 750mg IV q24h) for atypicals, UTI, but resistance increasing, avoid in MDRO risk
14. Antipseudomonal coverage essential if: ICU patient, prior Pseudomonas, structural lung disease, broad-spectrum antibiotic exposure <90 days
15. Local antibiogram guides empiric choices: if MRSA prevalence >10-20% in blood cultures, add vancomycin empirically
16. Duration typically 7-10 days for most infections, procalcitonin-guided therapy can shorten courses safely
17. De-escalation critical: narrow from pip-tazo to ceftriaxone, stop vancomycin if cultures negative for MRSA
18. Allergies: penicillin allergy 10% true IgE-mediated, most can receive cephalosporins; severe allergy use aztreonam + vancomycin
19. Renal dosing adjustments mandatory for beta-lactams, vancomycin, aminoglycosides to prevent toxicity and ensure efficacy
20. Obesity dosing: vancomycin use actual body weight, beta-lactams standard dosing or extended infusion
        """,
        key_factors=[
            "Infection source determines likely pathogens",
            "Local antibiogram and resistance patterns guide selection",
            "MRSA coverage if healthcare-associated, severe infection, or high local prevalence",
            "Antipseudomonal coverage for ICU, structural lung disease, or prior Pseudomonas",
            "De-escalation within 48-72 hours based on cultures",
            "Renal dosing adjustments to prevent toxicity"
        ],
        primary_authority=[
            "IDSA Clinical Practice Guidelines",
            "Surviving Sepsis Campaign 2021",
            "Sanford Guide to Antimicrobial Therapy 2024"
        ],
        burden_holder="Prescribing clinician and antimicrobial stewardship team",
        adversary_position="Unnecessary broad-spectrum antibiotics drive resistance",
        counter_arguments=[
            "Narrower spectrum may miss resistant pathogens",
            "Early de-escalation risks treatment failure if cultures false-negative"
        ],
        resolution_strategy="Start broad based on source and risk factors, obtain cultures before antibiotics, de-escalate aggressively based on culture data and clinical improvement",
        entity_scope="All patients with sepsis or severe infection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Evidence-based guidelines with strong consensus",
        controlling_precedent="IDSA guidelines and institutional antibiograms",
        issue_category=IssueCategory.ANTIMICROBIAL_STEWARDSHIP,
        zone=AnalysisZone.ACUTE_MANAGEMENT
    ),

    DoctrineBlock(
        topic="Blood Culture Interpretation - True Positive vs Contaminant",
        keywords=["blood culture", "contaminant", "coagulase-negative staph", "bacillus", "propionibacterium", "corynebacterium"],
        conclusion_template=[
            "Single positive blood culture with skin flora (CoNS, Bacillus, Corynebacterium, Propionibacterium) likely contaminant unless prosthetic device or immunocompromised.",
            "True bacteremia criteria: same organism in >=2 blood culture sets, clinical signs of infection, organism typical pathogen (S. aureus, E. coli, Streptococcus).",
            "Treat contaminants with repeat cultures and clinical assessment, not antibiotics, to avoid unnecessary therapy and resistance."
        ],
        reasoning_framework="""
1. Blood culture contamination rate should be <3% per CAP/CLSI benchmarks, >3% indicates poor collection technique
2. Common contaminants: coagulase-negative Staphylococcus (CoNS), Bacillus spp, Corynebacterium, Cutibacterium (Propionibacterium), Micrococcus
3. True pathogens: S. aureus (99% pathogenic), E. coli, Klebsiella, Enterococcus, Streptococcus, Candida, anaerobes
4. CoNS pathogenic if: prosthetic device (pacemaker, LVAD, prosthetic valve), intravascular catheter-related, >=2 positive sets, immunocompromised
5. Time to positivity (TTP): earlier positivity (<12 hours) suggests high-inoculum true bacteremia, late (>24 hours) suggests contaminant
6. Differential time to positivity (DTP): catheter vs peripheral blood cultures; catheter positive >=2 hours earlier suggests CRBSI
7. Clinical correlation essential: fever, leukocytosis, hemodynamic instability support true bacteremia
8. Single positive bottle of 4 drawn = contaminant unless organism is S. aureus, E. coli, or S. pneumoniae
9. Repeat cultures if contaminant suspected, especially if patient clinically improving without antibiotics
10. Do NOT treat CoNS from single culture unless device present; unnecessary vancomycin drives VRE resistance
11. Bacillus cereus or B. anthracis are pathogens (anthrax, endophthalmitis); other Bacillus spp usually contaminants
12. Candida in blood culture ALWAYS significant, requires antifungal therapy and ophthalmology consult for endophthalmitis
13. Anaerobes (Bacteroides, Clostridium, Peptostreptococcus) in blood culture always significant, source often intra-abdominal or pelvic
14. Viridans streptococci can be contaminants or cause endocarditis; 2+ positive cultures + murmur suggest endocarditis
15. Collection technique: strict sterile prep with chlorhexidine or iodine, 2 sets from separate sites, 8-10 mL per bottle (aerobic + anaerobic)
16. Contamination risk factors: inadequate skin prep, phlebotomy from IV line, insufficient volume, single venipuncture site
17. Polymicrobial bacteremia: if 3+ organisms, likely contaminant or GI source (translocation, perforation)
18. Continuous bacteremia (endocarditis, intravascular infection): organisms present in all culture sets drawn over hours
19. Transient bacteremia (dental work, GI procedure): single positive culture, resolves spontaneously
20. Fungemia workup: ophthalmology exam, echocardiography, remove central lines, prolonged antifungal therapy (14 days minimum after clearance)
        """,
        key_factors=[
            "Organism identity (CoNS, Bacillus = likely contaminant; S. aureus, E. coli = pathogen)",
            "Number of positive sets (1 set = contaminant unless S. aureus; >=2 sets = true bacteremia)",
            "Time to positivity (<12 hours = high inoculum true infection)",
            "Clinical context (fever, hemodynamic instability, prosthetic device)",
            "Contamination rate <3% institutional benchmark"
        ],
        primary_authority=[
            "Clinical and Laboratory Standards Institute (CLSI) M47",
            "IDSA Blood Culture Guidelines",
            "Bates DW et al. Arch Intern Med 1991;151(9):1769-1774"
        ],
        burden_holder="Clinician interpreting blood culture results",
        adversary_position="Treating all positive cultures avoids missing true infections",
        counter_arguments=[
            "CoNS can cause true bacteremia in immunocompromised or device patients",
            "Single positive S. epidermidis may be early endocarditis"
        ],
        resolution_strategy="Use clinical criteria and number of positive sets to distinguish pathogen from contaminant; repeat cultures if uncertain; avoid antibiotics for likely contaminants",
        entity_scope="All patients with positive blood cultures",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Evidence-based criteria with consensus guidelines",
        controlling_precedent="CLSI M47 and IDSA blood culture interpretation standards",
        issue_category=IssueCategory.DIAGNOSTIC_MICROBIOLOGY,
        zone=AnalysisZone.STEWARDSHIP_REVIEW
    ),

    DoctrineBlock(
        topic="MRSA Management and Vancomycin Dosing",
        keywords=["mrsa", "vancomycin", "trough", "auc/mic", "linezolid", "daptomycin", "ceftaroline"],
        conclusion_template=[
            "MRSA infections require vancomycin (first-line), linezolid (pneumonia), daptomycin (bacteremia), or ceftaroline (resistant MRSA).",
            "Vancomycin dosing: 15-20 mg/kg IV q8-12h, target AUC/MIC >400 or trough 15-20 mcg/mL for serious infections (bacteremia, pneumonia, meningitis).",
            "Monitor renal function and vancomycin troughs; nephrotoxicity risk increases with trough >20 mcg/mL or concomitant nephrotoxins."
        ],
        reasoning_framework="""
1. MRSA prevalence varies by institution (10-50% of S. aureus isolates), require contact precautions
2. Vancomycin MIC <=1 mcg/mL susceptible, 2 mcg/mL intermediate, >=4 resistant
3. AUC/MIC target >400 associated with better outcomes, calculate using Bayesian software or trough-based estimate
4. Loading dose 25-30 mg/kg IV x1 for severe infections to rapidly achieve therapeutic levels
5. Trough-based dosing: draw trough before 4th dose at steady state (48 hours), target 15-20 for pneumonia/bacteremia, 10-15 for skin/soft tissue
6. Nephrotoxicity risk: baseline CrCl <50, trough >20, concurrent aminoglycosides/NSAIDs/contrast, obesity
7. Linezolid 600mg IV/PO q12h for MRSA pneumonia (better lung penetration than vancomycin), avoid >14 days (myelosuppression, lactic acidosis)
8. Daptomycin 6-10 mg/kg IV q24h for MRSA bacteremia or endocarditis (higher dose for complex infections), monitor CPK weekly
9. Ceftaroline 600mg IV q8h for MRSA with vancomycin MIC >=2 (vancomycin-intermediate S. aureus, VISA)
10. Do NOT use daptomycin for pneumonia (inactivated by surfactant), use linezolid or vancomycin
11. Persistent MRSA bacteremia: increase vancomycin dose, switch to daptomycin 8-10 mg/kg, add ceftaroline or rifampin for synergy
12. Source control critical: drain abscesses, remove infected catheters/devices, debride osteomyelitis
13. Duration: skin/soft tissue 7-14 days, bacteremia 14 days minimum (uncomplicated) or 4-6 weeks (endocarditis, osteomyelitis)
14. Decolonization (nasal mupirocin + chlorhexidine baths) for recurrent MRSA or pre-operative prophylaxis in carriers
15. Tedizolid 200mg IV/PO q24h alternative to linezolid, shorter course (6 days), less myelosuppression
16. Vancomycin-resistant S. aureus (VRSA) rare, use daptomycin + ceftaroline or linezolid
17. Renal dosing: CrCl 30-50 q12h, CrCl 10-30 q24h, HD 15-20 mg/kg load then redose based on levels
18. Obesity dosing: use actual body weight for loading dose, adjusted body weight or AUC-based for maintenance
19. Red man syndrome: histamine-mediated infusion reaction, slow infusion rate to 1g over 90-120 min, premedicate with antihistamine
20. Thrombocytopenia, neutropenia: monitor CBC on linezolid >7-10 days, reversible on discontinuation
        """,
        key_factors=[
            "Vancomycin AUC/MIC >400 or trough 15-20 mcg/mL for serious MRSA infections",
            "Linezolid preferred for MRSA pneumonia due to superior lung penetration",
            "Daptomycin for bacteremia/endocarditis, dose 8-10 mg/kg for complex infections",
            "Source control (drain, debride, remove devices) essential",
            "Monitor renal function and drug levels to prevent nephrotoxicity"
        ],
        primary_authority=[
            "IDSA MRSA Guidelines 2011",
            "Vancomycin Consensus Guidelines (ASHP/IDSA/SIDP) 2020",
            "Liu C et al. Clin Infect Dis 2011;52(3):e18-e55"
        ],
        burden_holder="Clinician treating MRSA infection",
        adversary_position="Empiric vancomycin in all skin infections drives resistance",
        counter_arguments=[
            "AUC-based dosing complex, not universally implemented",
            "Trough >20 increases nephrotoxicity risk"
        ],
        resolution_strategy="Use vancomycin for confirmed MRSA with appropriate dosing and monitoring; switch to alternative agents for vancomycin failure or intolerance; de-escalate if cultures show MSSA",
        entity_scope="Patients with MRSA infections or high risk for MRSA",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Strong guideline recommendations with therapeutic drug monitoring",
        controlling_precedent="IDSA MRSA guidelines and vancomycin consensus statements",
        issue_category=IssueCategory.ANTIMICROBIAL_RESISTANCE,
        zone=AnalysisZone.ACUTE_MANAGEMENT
    ),

    DoctrineBlock(
        topic="C. difficile Infection Diagnosis and Management",
        keywords=["c diff", "clostridium difficile", "cdiff", "fidaxomicin", "vancomycin oral", "fecal microbiota transplant", "bezlotoxumab"],
        conclusion_template=[
            "C. difficile infection diagnosed by diarrhea (>=3 unformed stools/24h) plus toxin assay or PCR positive, or pseudomembranes on colonoscopy.",
            "Treatment: initial episode vancomycin 125mg PO q6h x10 days or fidaxomicin 200mg PO q12h x10 days; severe or fulminant add IV metronidazole 500mg q8h.",
            "Recurrent CDI (2+ episodes): fidaxomicin, vancomycin taper/pulse, or fecal microbiota transplant (FMT) after 2nd recurrence."
        ],
        reasoning_framework="""
1. C. difficile toxin-mediated colitis, risk factors: antibiotics (clindamycin, fluoroquinolones, cephalosporins), PPI, advanced age, hospitalization
2. Diagnostic algorithm: glutamate dehydrogenase (GDH) screen + toxin EIA, or nucleic acid amplification test (NAAT/PCR)
3. PCR high sensitivity but detects colonization, false-positive in asymptomatic carriers; toxin EIA more specific but less sensitive
4. Do NOT test asymptomatic patients or test of cure (toxin persists weeks after treatment)
5. Severity assessment: WBC <15K and Cr <1.5 = non-severe; WBC >=15K or Cr >=1.5 = severe; hypotension, ileus, megacolon = fulminant
6. Initial episode non-severe: vancomycin 125mg PO q6h x10 days (preferred) or fidaxomicin 200mg PO q12h x10 days
7. Severe CDI: vancomycin 125mg PO q6h x10-14 days, consider adding IV metronidazole 500mg q8h if ileus/toxic megacolon
8. Fulminant CDI: vancomycin 500mg PO/NG q6h + IV metronidazole 500mg q8h + vancomycin enema 500mg in 100 mL NS q6h PR if ileus; surgical consult if no improvement 5 days
9. Metronidazole 500mg PO q8h no longer first-line (inferior outcomes vs vancomycin), use only if vancomycin/fidaxomicin unavailable
10. First recurrence: vancomycin 125mg PO q6h x10 days or fidaxomicin 200mg PO q12h x10 days
11. Second recurrence: fidaxomicin 200mg PO q12h x10 days (preferred), or vancomycin taper/pulse regimen
12. Vancomycin taper: 125mg q6h x10-14 days, then q12h x7 days, then daily x7 days, then every 2-3 days x2-8 weeks
13. Bezlotoxumab 10 mg/kg IV x1 monoclonal antibody against toxin B, reduces recurrence 40%, give during antibiotic treatment for high-risk recurrence
14. Fecal microbiota transplant (FMT): 80-90% cure rate after 2+ recurrences, administered via colonoscopy, capsules, or nasogastric tube
15. Surgery (subtotal colectomy with ileostomy) for refractory fulminant CDI with peritonitis, perforation, or toxic megacolon
16. Imaging: CT shows colonic wall thickening, pericolonic stranding, ascites; avoid oral contrast (worsens diarrhea)
17. Pseudomembranous colitis on colonoscopy: yellow-white plaques, diagnostic even if toxin assay negative
18. Stop inciting antibiotics if possible, avoid antimotility agents (loperamide increases toxic megacolon risk)
19. Infection control: contact precautions, dedicated equipment, bleach cleaning (alcohol gel ineffective against spores)
20. Procalcitonin typically low in CDI (toxin-mediated, not invasive bacteremia), helps differentiate from bacterial sepsis
        """,
        key_factors=[
            "Diarrhea >=3 unformed stools/24h plus positive toxin or PCR",
            "Vancomycin 125mg PO q6h or fidaxomicin first-line treatment",
            "Severe CDI: WBC >=15K or Cr >=1.5, consider IV metronidazole if ileus",
            "Recurrent CDI (>=2 episodes): fidaxomicin, vancomycin taper, or FMT",
            "Bezlotoxumab reduces recurrence in high-risk patients",
            "Surgery for fulminant CDI with peritonitis or toxic megacolon"
        ],
        primary_authority=[
            "IDSA/SHEA C. difficile Guidelines 2021",
            "McDonald LC et al. Clin Infect Dis 2018;66(7):e1-e48",
            "Johnson S et al. Clin Infect Dis 2021;73(5):e1029-e1044"
        ],
        burden_holder="Clinician diagnosing and treating CDI",
        adversary_position="Overdiagnosis due to PCR detecting colonization, not disease",
        counter_arguments=[
            "Vancomycin more expensive than metronidazole but superior outcomes",
            "FMT risk of transmitting multidrug-resistant organisms or pathogens"
        ],
        resolution_strategy="Diagnose with clinical criteria + toxin/PCR; treat initial episode with vancomycin or fidaxomicin; use FMT for multiple recurrences; surgical consult for fulminant cases",
        entity_scope="Patients with suspected or confirmed C. difficile infection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Strong evidence from RCTs and consensus guidelines",
        controlling_precedent="IDSA/SHEA 2021 CDI guidelines",
        issue_category=IssueCategory.CDIFF_MANAGEMENT,
        zone=AnalysisZone.ACUTE_MANAGEMENT
    ),

    DoctrineBlock(
        topic="Antimicrobial Stewardship Program Core Elements",
        keywords=["antimicrobial stewardship", "asp", "prior authorization", "audit and feedback", "prospective review", "antibiogram"],
        conclusion_template=[
            "Antimicrobial stewardship programs (ASP) optimize antibiotic use to improve patient outcomes, reduce resistance, and decrease costs.",
            "CDC Core Elements: leadership commitment, accountability (physician + pharmacist champions), drug expertise, action (prior authorization or prospective audit-feedback), tracking/reporting, education.",
            "Effective interventions include formulary restriction, dose optimization, IV-to-oral switch, automatic stop orders, and pathogen-directed de-escalation."
        ],
        reasoning_framework="""
1. ASP reduces inappropriate antibiotic use 20-30%, decreases C. diff infections 50%, saves $200K-$900K per hospital annually
2. Leadership commitment: dedicated budget, protected time for ASP pharmacist/physician, endorsement by medical staff
3. Accountability: single physician leader + pharmacist co-lead with ID expertise and stewardship training
4. Drug expertise: ASP pharmacist provides real-time consultation, optimizes dosing (renal, obesity), monitors therapeutic drug levels
5. Action: prior authorization (restrictive) or prospective audit with feedback (persuasive), both equally effective
6. Prior authorization: obtain approval before dispensing broad-spectrum agents (carbapenems, daptomycin, echinocandins, linezolid)
7. Prospective audit-feedback: ASP reviews all patients on restricted antibiotics 48-72h after initiation, recommends de-escalation/discontinuation
8. Tracking: days of therapy (DOT) per 1000 patient-days, defined daily dose (DDD), antibiotic consumption by class
9. Reporting: quarterly antibiogram with susceptibility data, resistance trends, C. diff rates, ASP intervention acceptance rate
10. Education: annual antibiotic prescribing guidelines, case-based learning, audit results shared with prescribers
11. Automatic stop orders: 72-hour hard stops for empiric therapy, force reassessment with cultures and clinical response
12. IV-to-oral switch: bioavailable oral antibiotics (fluoroquinolones, linezolid, metronidazole) switch when hemodynamically stable, tolerating PO
13. Dose optimization: extended-infusion beta-lactams (pip-tazo 3.375g over 4 hours), aminoglycoside once-daily dosing, vancomycin AUC-based
14. Antibiogram: annual report of local susceptibility patterns, stratifies by ICU vs non-ICU, guides empiric therapy
15. Pathogen-directed therapy: narrow from meropenem to ceftriaxone if ESBL-negative E. coli, stop vancomycin if MSSA
16. Diagnostic stewardship: reduce unnecessary urine cultures (asymptomatic bacteriuria), blood cultures (not from lines), respiratory viral panels overuse
17. Rapid diagnostics: MRSA nasal PCR (discharge vancomycin if negative 24h), blood culture Gram stain/MALDI-TOF (early ID), syndromic panels (Film Array)
18. Pharmacokinetic/pharmacodynamic optimization: beta-lactams time-dependent (maximize time >MIC), aminoglycosides concentration-dependent (maximize peak/MIC)
19. Allergy assessment: 90% penicillin allergies are not true IgE-mediated, de-labeling allows use of preferred beta-lactams vs suboptimal alternatives
20. Outpatient stewardship: delayed prescriptions for URI, shorter courses for uncomplicated infections (3 days for cystitis, 5 days for CAP)
        """,
        key_factors=[
            "Leadership support and dedicated ASP resources (physician + pharmacist champions)",
            "Prior authorization or prospective audit-feedback for restricted antibiotics",
            "Tracking antibiotic consumption (DOT/1000 patient-days) and resistance trends",
            "Education and guideline dissemination to prescribers",
            "Rapid diagnostics and pathogen-directed de-escalation",
            "Dose optimization and IV-to-oral switch protocols"
        ],
        primary_authority=[
            "CDC Core Elements of Hospital Antibiotic Stewardship 2019",
            "IDSA/SHEA Antimicrobial Stewardship Guidelines 2016",
            "Barlam TF et al. Clin Infect Dis 2016;62(10):e51-e77"
        ],
        burden_holder="Hospital administration and ASP team",
        adversary_position="Restrictive policies delay treatment and harm patients",
        counter_arguments=[
            "Prior authorization can delay appropriate therapy if approval process slow",
            "De-escalation may miss resistant organisms if cultures inadequate"
        ],
        resolution_strategy="Implement CDC Core Elements with leadership support; use prospective audit-feedback for high acceptance; track outcomes and resistance patterns; educate prescribers continuously",
        entity_scope="All hospitals and healthcare systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Strong evidence from systematic reviews and national guidelines",
        controlling_precedent="CDC Core Elements and IDSA/SHEA guidelines",
        issue_category=IssueCategory.ANTIMICROBIAL_STEWARDSHIP,
        zone=AnalysisZone.STEWARDSHIP_REVIEW
    ),

    DoctrineBlock(
        topic="Procalcitonin-Guided Antibiotic Therapy",
        keywords=["procalcitonin", "pct", "antibiotic duration", "de-escalation", "biomarker", "bacterial infection"],
        conclusion_template=[
            "Procalcitonin (PCT) is a biomarker of bacterial infection; PCT >0.5 ng/mL suggests bacterial sepsis, <0.5 supports viral or non-infectious etiology.",
            "PCT-guided algorithms safely reduce antibiotic duration in sepsis, pneumonia, and respiratory infections by 20-30% without increasing mortality.",
            "Serial PCT measurements: discontinue antibiotics when PCT decreases >80% from peak or falls below 0.5 ng/mL, if clinically improving."
        ],
        reasoning_framework="""
1. Procalcitonin is prohormone of calcitonin, produced by parathyroid C-cells and upregulated by bacterial endotoxin and inflammatory cytokines
2. PCT rises within 4-6 hours of bacterial infection, peaks 12-24 hours, half-life 24-30 hours
3. PCT cutoffs: <0.1 ng/mL normal, 0.1-0.5 low risk bacterial, 0.5-2.0 moderate risk, >2.0 high risk severe bacterial sepsis
4. Viral infections, autoimmune diseases, chronic inflammation typically PCT <0.5 ng/mL
5. PCT >2 ng/mL in sepsis associated with higher mortality, need for vasopressors, organ failure
6. ProCESS, ProACT, SAPS trials: PCT-guided therapy reduced antibiotic exposure 1-3 days without increasing mortality or treatment failure
7. PCT algorithm: start antibiotics if PCT >0.5 or sepsis suspected, recheck PCT daily, discontinue if PCT <0.5 or decreased >80% and clinically stable
8. Do NOT use PCT alone to withhold antibiotics in sepsis or severe infection; clinical judgment overrides low PCT
9. PCT useful in respiratory infections (COPD exacerbation, CAP) to distinguish bacterial from viral etiology and guide duration
10. PCT-guided discontinuation in ICU: stop antibiotics when PCT <0.5 or >80% decrease from peak, even if initially high
11. False elevations: severe trauma, surgery, burns, heat stroke, massive transfusion, small cell lung cancer, medullary thyroid cancer
12. Renal failure does NOT significantly elevate PCT (unlike CRP); PCT remains valid biomarker in dialysis patients
13. Immunocompromised patients may have blunted PCT response; less reliable in neutropenia, transplant
14. CRP (C-reactive protein) less specific than PCT for bacterial infection, slower kinetics (peak 48h, half-life 19h), useful for monitoring inflammation
15. Lactate reflects tissue hypoperfusion, not infection type; PCT superior for bacterial vs viral differentiation
16. PCT <0.25 ng/mL at ICU admission predicts low risk of bacterial infection, consider antibiotic discontinuation if alternative diagnosis
17. Serial PCT monitoring: measure on days 0, 1, 3, 5, 7; persistent elevation suggests source control failure or resistant organism
18. Cost-effectiveness: PCT testing $20-30 per assay, reduced antibiotic days save $100-200 per patient in drug/monitoring costs
19. PCT protocols require education and buy-in from prescribers; standalone PCT values without algorithm ineffective at reducing antibiotic use
20. PCT NOT useful for: fungal infections, localized infections (cellulitis, abscess), mycobacterial infections, chronic osteomyelitis
        """,
        key_factors=[
            "PCT >0.5 ng/mL supports bacterial infection diagnosis",
            "Serial PCT measurements guide antibiotic discontinuation (stop when <0.5 or >80% decrease)",
            "PCT-guided therapy reduces antibiotic duration 20-30% safely",
            "Clinical judgment overrides PCT; do not withhold antibiotics in sepsis based on low PCT alone",
            "False elevations: trauma, surgery, burns, malignancy"
        ],
        primary_authority=[
            "Schuetz P et al. Lancet Infect Dis 2017;17(12):1279-1287",
            "de Jong E et al. Lancet Infect Dis 2016;16(7):819-827",
            "Wirz Y et al. Clin Chem Lab Med 2018;56(9):1473-1484"
        ],
        burden_holder="Clinician managing antibiotic therapy",
        adversary_position="Biomarkers cannot replace clinical judgment; premature discontinuation risks relapse",
        counter_arguments=[
            "PCT variability in immunocompromised or localized infections limits utility",
            "Cost of daily PCT assays may exceed antibiotic cost savings in low-risk patients"
        ],
        resolution_strategy="Use PCT as adjunct to clinical assessment; implement PCT algorithm with provider education; measure serially to guide duration; override with clinical judgment if discordant",
        entity_scope="Patients with suspected bacterial infections, sepsis, or pneumonia",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High-quality RCTs and meta-analyses support PCT-guided therapy",
        controlling_precedent="Multiple large RCTs (ProCESS, ProACT, SAPS) and meta-analyses",
        issue_category=IssueCategory.ANTIMICROBIAL_STEWARDSHIP,
        zone=AnalysisZone.STEWARDSHIP_REVIEW
    ),

    DoctrineBlock(
        topic="HIV Treatment - Antiretroviral Therapy (ART) Initiation and Regimens",
        keywords=["hiv", "art", "haart", "integrase inhibitor", "bictegravir", "dolutegravir", "tenofovir", "emtricitabine"],
        conclusion_template=[
            "All HIV-positive patients should start ART immediately regardless of CD4 count to reduce transmission and improve outcomes (START trial).",
            "Recommended initial regimens: integrase strand transfer inhibitor (INSTI) + 2 NRTIs (bictegravir/tenofovir AF/emtricitabine or dolutegravir/abacavir/lamivudine).",
            "Viral load suppression (<50 copies/mL) expected within 12-24 weeks; monitor adherence, resistance, and drug interactions closely."
        ],
        reasoning_framework="""
1. HIV treatment goals: viral suppression <50 copies/mL, immune reconstitution (CD4 >200), prevent transmission, reduce comorbidities
2. START trial: immediate ART vs deferred (CD4 <350) reduced AIDS events 57%, mortality 72%, regardless of baseline CD4
3. U=U (undetectable = untransmittable): viral load <200 copies/mL for 6+ months eliminates sexual transmission risk
4. Initial regimen classes: integrase inhibitor (INSTI, preferred), NNRTI (efavirenz, older), protease inhibitor (boosted darunavir, third-line)
5. First-line single-tablet regimens: bictegravir/TAF/FTC (Biktarvy), dolutegravir/abacavir/3TC (Triumeq), dolutegravir/3TC (Dovato, 2-drug regimen)
6. Nucleoside reverse transcriptase inhibitors (NRTIs): tenofovir alafenamide (TAF, less renal/bone toxicity) or tenofovir disoproxil fumarate (TDF) + emtricitabine (FTC) or lamivudine (3TC)
7. Integrase inhibitors: bictegravir (BIC), dolutegravir (DTG), raltegravir (RAL), elvitegravir/cobicistat (EVG/c); high barrier to resistance, minimal drug interactions
8. Abacavir (ABC) requires HLA-B*5701 testing before use; positive test = contraindicated (hypersensitivity reaction risk)
9. Baseline labs: HIV RNA (viral load), CD4 count, genotype resistance testing, HLA-B*5701, HBV/HCV screening, pregnancy test, CrCl, lipids, glucose
10. Genotype resistance testing before ART initiation to detect transmitted mutations (K103N for NNRTI, M184V for 3TC/FTC)
11. Resistance mutations: INSTI Q148H/R, NRTI M184V, NNRTI K103N, PI major mutations (I54V, V82A)
12. Drug interactions: rifampin decreases INSTI levels (avoid with BIC/DTG or increase DTG to 50mg BID), tenofovir + boosted PIs increase tenofovir levels
13. Monitoring: viral load at 4 weeks, 12 weeks, 24 weeks, then every 3-6 months if suppressed; CD4 annually once >200 and stable
14. Virologic failure: 2 consecutive viral loads >200 copies/mL after 24 weeks, or rebound after suppression; check adherence, then genotype for resistance
15. ART in pregnancy: start immediately, preferred regimen dolutegravir-based or raltegravir + 2 NRTIs, avoid efavirenz (teratogenic)
16. Opportunistic infection prophylaxis: PCP prophylaxis (TMP-SMX) if CD4 <200, toxoplasmosis prophylaxis if CD4 <100, MAC prophylaxis (azithromycin) if CD4 <50
17. Immune reconstitution inflammatory syndrome (IRIS): paradoxical worsening of infections (TB, CMV, PCP) after starting ART due to immune recovery, manage with steroids if severe
18. Side effects: INSTI weight gain, NNRTI CNS symptoms (vivid dreams, dizziness), PI GI intolerance, TDF renal/bone toxicity
19. PrEP (pre-exposure prophylaxis): tenofovir/emtricitabine daily for HIV-negative high-risk individuals, reduces infection 99% if adherent
20. Post-exposure prophylaxis (PEP): start within 72 hours of high-risk exposure, 28 days tenofovir/emtricitabine + raltegravir or dolutegravir
        """,
        key_factors=[
            "Start ART immediately in all HIV-positive patients regardless of CD4 count",
            "First-line regimens: INSTI (bictegravir or dolutegravir) + 2 NRTIs (TAF/FTC or ABC/3TC)",
            "Baseline genotype resistance testing to guide regimen selection",
            "Viral load suppression <50 copies/mL within 12-24 weeks expected",
            "Monitor adherence, drug interactions, and resistance mutations",
            "U=U: sustained viral suppression eliminates transmission risk"
        ],
        primary_authority=[
            "DHHS HIV/AIDS Guidelines 2024",
            "START Trial (INSIGHT Group) N Engl J Med 2015",
            "IAS-USA Antiretroviral Guidelines 2022"
        ],
        burden_holder="HIV treatment provider",
        adversary_position="Immediate ART may increase side effects before patient ready",
        counter_arguments=[
            "Integrase inhibitors associated with weight gain in some patients",
            "Drug interactions require careful monitoring with comedications"
        ],
        resolution_strategy="Initiate ART immediately with INSTI-based regimen; obtain baseline resistance testing; monitor viral load and adherence; adjust for drug interactions; provide adherence support",
        entity_scope="All HIV-positive patients",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Strong evidence from RCTs and consensus guidelines",
        controlling_precedent="DHHS guidelines and START trial",
        issue_category=IssueCategory.HIV_TREATMENT,
        zone=AnalysisZone.ACUTE_MANAGEMENT
    ),

    DoctrineBlock(
        topic="Tuberculosis Diagnosis and RIPE Therapy",
        keywords=["tuberculosis", "tb", "ripe", "rifampin", "isoniazid", "pyrazinamide", "ethambutol", "latent tb"],
        conclusion_template=[
            "Active TB diagnosed by AFB smear, culture, and nucleic acid amplification (GeneXpert); CXR shows upper lobe infiltrates, cavitation, or miliary pattern.",
            "Standard treatment (RIPE): rifampin, isoniazid, pyrazinamide, ethambutol x2 months intensive phase, then rifampin + isoniazid x4 months continuation (6 months total).",
            "Latent TB (LTBI) treated with rifampin 4 months, isoniazid 9 months, or 3-month isoniazid + rifapentine weekly to prevent progression to active disease."
        ],
        reasoning_framework="""
1. TB transmission: airborne droplet nuclei from pulmonary or laryngeal TB, close contact (household, congregate settings), immunocompromised at highest risk
2. TB screening: tuberculin skin test (TST) or interferon-gamma release assay (IGRA, QuantiFERON, T-SPOT), positive if >=5mm (HIV, close contact), >=10mm (high-risk), >=15mm (low-risk)
3. Chest X-ray: upper lobe infiltrates, cavitation (high bacillary load), miliary TB (disseminated hematogenous spread), hilar lymphadenopathy
4. Microbiologic diagnosis: AFB smear (rapid, low sensitivity 50-60%), culture (gold standard, 2-6 weeks), GeneXpert (NAAT, 2 hours, detects rifampin resistance)
5. GeneXpert MTB/RIF: 88% sensitivity, 98% specificity, detects rpoB mutations conferring rifampin resistance in 2 hours
6. AFB smear-negative TB common in HIV, extrapulmonary TB; do NOT exclude TB if smear negative but high clinical suspicion
7. RIPE therapy: Rifampin 10 mg/kg (max 600mg), Isoniazid 5 mg/kg (max 300mg), Pyrazinamide 25 mg/kg (max 2g), Ethambutol 15 mg/kg (max 1600mg)
8. Intensive phase: RIPE x2 months daily, then continuation phase rifampin + isoniazid x4 months (6 months total for drug-susceptible pulmonary TB)
9. Directly observed therapy (DOT): in-person administration to ensure adherence, recommended for all TB patients
10. Drug resistance: test baseline isolate for rifampin, isoniazid, pyrazinamide, ethambutol, fluoroquinolones, aminoglycosides (GeneXpert + culture-based DST)
11. Multidrug-resistant TB (MDR-TB): resistance to rifampin + isoniazid, requires 9-20 month regimen with fluoroquinolone, bedaquiline, linezolid, clofazimine
12. Extensively drug-resistant TB (XDR-TB): MDR-TB + resistance to fluoroquinolone + aminoglycoside, use bedaquiline, pretomanid, linezolid (BPaL regimen 6 months)
13. Extrapulmonary TB: meningitis, pericarditis, disseminated TB require 9-12 months therapy; CNS TB add steroids (dexamethasone) to reduce inflammation
14. TB meningitis: rifampin, isoniazid, pyrazinamide, ethambutol x2 months, then rifampin + isoniazid x7-10 months (9-12 months total), dexamethasone taper 6-8 weeks
15. Latent TB infection (LTBI): positive TST/IGRA without active disease, treat to prevent progression (5-10% lifetime risk, highest in first 2 years)
16. LTBI regimens: rifampin 600mg daily x4 months (preferred), isoniazid 300mg daily x9 months, 3HP (isoniazid + rifapentine weekly x12 weeks)
17. Rifampin drug interactions: induces CYP3A4, decreases levels of antiretrovirals (integrase inhibitors, protease inhibitors), warfarin, contraceptives, antifungals
18. Isoniazid hepatotoxicity: monitor LFTs monthly, discontinue if ALT >3x ULN with symptoms or >5x ULN asymptomatic, give pyridoxine (B6) 25-50mg daily to prevent neuropathy
19. Pyrazinamide: uric acid elevation (gout), hepatotoxicity; avoid in pregnancy (not teratogenic but data limited)
20. Ethambutol: optic neuritis (dose-dependent), baseline and monthly visual acuity and color vision testing, avoid if CrCl <30 or unable to monitor vision
        """,
        key_factors=[
            "Diagnose with AFB smear, culture, and GeneXpert (detects rifampin resistance)",
            "RIPE therapy x2 months intensive, then rifampin + isoniazid x4 months continuation",
            "Directly observed therapy (DOT) essential for adherence",
            "Test for drug resistance; MDR-TB requires prolonged multidrug regimen",
            "Latent TB treated with rifampin 4 months or isoniazid 9 months to prevent progression",
            "Monitor LFTs, visual acuity; manage drug interactions (rifampin induces CYP3A4)"
        ],
        primary_authority=[
            "CDC TB Treatment Guidelines 2023",
            "WHO TB Guidelines 2022",
            "Nahid P et al. Clin Infect Dis 2016;63(7):e147-e195"
        ],
        burden_holder="TB treatment provider and public health authorities",
        adversary_position="Long treatment duration leads to poor adherence and resistance",
        counter_arguments=[
            "LTBI treatment has hepatotoxicity risk, benefits may not outweigh risks in low-risk populations",
            "Rifampin drug interactions complicate HIV co-infection treatment"
        ],
        resolution_strategy="Diagnose with GeneXpert and culture; initiate RIPE therapy empirically; use DOT; test for resistance; adjust regimen for MDR-TB; treat LTBI in high-risk contacts; monitor toxicity and adherence",
        entity_scope="Patients with active or latent tuberculosis",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Strong evidence-based guidelines from CDC and WHO",
        controlling_precedent="CDC TB treatment guidelines",
        issue_category=IssueCategory.TB_MANAGEMENT,
        zone=AnalysisZone.ACUTE_MANAGEMENT
    ),

    DoctrineBlock(
        topic="Carbapenem-Resistant Enterobacterales (CRE) Management",
        keywords=["cre", "kpc", "carbapenemase", "meropenem", "ceftazidime-avibactam", "meropenem-vaborbactam", "colistin"],
        conclusion_template=[
            "CRE are multidrug-resistant gram-negative bacteria producing carbapenemases (KPC, NDM, OXA-48); associated with high mortality (40-50%).",
            "Treatment options: ceftazidime-avibactam (KPC, OXA-48), meropenem-vaborbactam (KPC), imipenem-relebactam (KPC), or polymyxins (colistin) if no alternatives.",
            "Infection control critical: contact precautions, dedicated equipment, terminal cleaning, cohorting to prevent transmission."
        ],
        reasoning_framework="""
1. CRE defined as resistance to >=1 carbapenem (meropenem, imipenem, doripenem, ertapenem) or carbapenemase production
2. Carbapenemase classes: KPC (Klebsiella pneumoniae carbapenemase, most common US), NDM (New Delhi metallo-beta-lactamase), OXA-48, VIM, IMP
3. CRE prevalence increasing: 4% of Enterobacterales in US hospitals, endemic in long-term care facilities, international travel risk
4. Risk factors: prolonged hospitalization, ICU stay, mechanical ventilation, central lines, prior carbapenem or broad-spectrum antibiotic use, solid organ transplant
5. Carbapenemase detection: molecular testing (PCR for blaKPC, blaNDM, blaOXA-48), modified carbapenem inactivation method (mCIM), Carba-NP
6. Ceftazidime-avibactam 2.5g IV q8h (CrCl >50) for KPC, OXA-48 CRE; avibactam inhibits KPC, OXA-48 but NOT NDM metallo-beta-lactamases
7. Meropenem-vaborbactam 4g IV q8h for KPC CRE; vaborbactam inhibits KPC, superior to polymyxins in RCTs, lower nephrotoxicity
8. Imipenem-relebactam 1.25g IV q6h for KPC CRE; relebactam inhibits KPC, alternative to meropenem-vaborbactam
9. Polymyxins (colistin 5 mg/kg loading, then 2.5 mg/kg q12h) for NDM or pan-resistant CRE; high nephrotoxicity (30-60%), last resort
10. Combination therapy for CRE bacteremia: ceftazidime-avibactam + meropenem, or polymyxin + tigecycline + meropenem, synergy may reduce mortality
11. Tigecycline 100mg IV x1, then 50mg IV q12h for CRE UTI or intra-abdominal; NOT for bacteremia (low blood levels, high mortality)
12. Plazomicin 15 mg/kg IV q24h aminoglycoside for CRE UTI, active against some KPC but not NDM, nephrotoxicity monitoring required
13. Aztreonam + ceftazidime-avibactam for NDM CRE: aztreonam stable to metallo-beta-lactamases, avibactam protects from other beta-lactamases
14. CRE UTI: ceftazidime-avibactam or meropenem-vaborbactam first-line, avoid fosfomycin (resistance develops rapidly on monotherapy)
15. CRE pneumonia: ceftazidime-avibactam + inhaled colistin or amikacin, poor lung penetration of polymyxins requires adjunctive therapy
16. Mortality CRE bacteremia: 40-50%, higher if inappropriate empiric therapy, delay in active agent, septic shock at presentation
17. Infection control: contact precautions for duration of hospitalization, dedicated equipment (stethoscope, BP cuff), single room or cohort, terminal cleaning with bleach
18. Active surveillance cultures: rectal swabs on admission for high-risk units (ICU, transplant), weekly screening to detect colonization
19. CRE colonization vs infection: colonized patients (rectal swab positive, no symptoms) do NOT need antibiotics, only infection control measures
20. Antimicrobial stewardship: restrict carbapenem use, enforce prior authorization, promote IV-to-oral switch, de-escalate when susceptibilities available
        """,
        key_factors=[
            "CRE produce carbapenemases (KPC, NDM, OXA-48) conferring resistance to carbapenems",
            "Ceftazidime-avibactam or meropenem-vaborbactam first-line for KPC CRE",
            "Aztreonam + ceftazidime-avibactam for NDM CRE (metallo-beta-lactamase)",
            "Polymyxins (colistin) last resort with high nephrotoxicity risk",
            "Combination therapy may improve outcomes in severe infections",
            "Contact precautions and infection control essential to prevent transmission"
        ],
        primary_authority=[
            "CDC CRE Guidelines 2019",
            "IDSA Guidance on CRE 2017",
            "Tamma PD et al. Clin Infect Dis 2022;74(11):2089-2096"
        ],
        burden_holder="Infection control team and treating clinician",
        adversary_position="New agents expensive, use should be restricted to confirmed CRE",
        counter_arguments=[
            "Combination therapy lacks high-quality RCT evidence for mortality benefit",
            "Resistance to ceftazidime-avibactam emerging in KPC producers"
        ],
        resolution_strategy="Identify CRE by carbapenemase testing; treat KPC with ceftazidime-avibactam or meropenem-vaborbactam; use aztreonam + ceftazidime-avibactam for NDM; implement strict contact precautions; stewardship to reduce carbapenem use",
        entity_scope="Patients with CRE infection or colonization",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Evidence-based guidelines with emerging RCT data on new agents",
        controlling_precedent="CDC and IDSA CRE guidelines",
        issue_category=IssueCategory.ANTIMICROBIAL_RESISTANCE,
        zone=AnalysisZone.ACUTE_MANAGEMENT
    ),

    DoctrineBlock(
        topic="Healthcare-Associated Infections (HAI) Prevention",
        keywords=["hai", "clabsi", "cauti", "vap", "ssi", "central line bundle", "ventilator bundle"],
        conclusion_template=[
            "Healthcare-associated infections (HAI) include CLABSI, CAUTI, VAP, SSI; preventable with evidence-based bundles and adherence.",
            "CLABSI prevention: hand hygiene, maximal barrier precautions, chlorhexidine skin prep, optimal catheter site (subclavian preferred), daily necessity review.",
            "CAUTI prevention: avoid unnecessary catheters, aseptic insertion, maintain closed system, remove when no longer needed."
        ],
        reasoning_framework="""
1. HAI burden: 1 in 31 hospital patients has HAI (CDC), 99K deaths/year, $28-45 billion annual costs
2. Central line-associated bloodstream infection (CLABSI): 30K cases/year, mortality 12-25%, $46K per event
3. CLABSI prevention bundle (5 components): hand hygiene, maximal sterile barrier, chlorhexidine skin antisepsis, optimal site selection, daily line necessity review
4. Maximal sterile barrier: cap, mask, sterile gown, sterile gloves, large sterile drape covering patient head-to-toe
5. Chlorhexidine 2% in alcohol for skin prep (superior to povidone-iodine), allow to dry 2 minutes before insertion
6. Central line site selection: subclavian lowest infection risk, internal jugular intermediate, femoral highest risk (avoid if possible)
7. Daily necessity review: remove central line when no longer needed (vasopressors off, adequate peripheral access), reduces CLABSI 50%
8. Catheter-associated urinary tract infection (CAUTI): most common HAI, 75% associated with indwelling catheter
9. CAUTI prevention: avoid catheter if possible (use alternatives: external catheter, intermittent catheterization), aseptic insertion, maintain closed system, remove catheter when no longer needed
10. Appropriate catheter indications: urinary retention, hourly UOP monitoring (ICU, shock), perioperative (prolonged surgery, large fluid volumes), end-of-life comfort
11. Inappropriate catheter indications: incontinence management, convenience for nursing staff, urine collection for culture (can use clean-catch)
12. Ventilator-associated pneumonia (VAP): 10-25% of mechanically ventilated patients, mortality 20-50%, prolongs ICU stay 7-9 days
13. VAP prevention bundle: head of bed elevation 30-45 degrees, daily sedation vacation and spontaneous breathing trial, oral care with chlorhexidine, peptic ulcer prophylaxis, DVT prophylaxis
14. Spontaneous breathing trial (SBT): daily assessment for extubation readiness reduces VAP risk by shortening ventilation duration
15. Subglottic secretion drainage: endotracheal tube with dorsal lumen for continuous suctioning, reduces VAP 50% in cardiac surgery patients
16. Surgical site infection (SSI): 2-5% of surgeries, increases hospital stay 7-10 days, $20K additional cost per event
17. SSI prevention: preoperative antibiotic within 60 min of incision, appropriate hair removal (clippers, not razors), normothermia, glycemic control (<200 mg/dL perioperatively)
18. Preoperative chlorhexidine bath: 4% chlorhexidine gluconate skin wash night before and morning of surgery reduces SSI 50%
19. Hand hygiene: single most effective HAI prevention measure, <50% compliance in most hospitals, alcohol-based hand rub preferred (faster, better compliance)
20. Contact precautions for MDRO (MRSA, VRE, CRE): gown and gloves on entry, dedicated equipment, daily chlorhexidine baths reduce MDRO acquisition 30%
        """,
        key_factors=[
            "CLABSI prevention: hand hygiene, maximal barrier, chlorhexidine, subclavian site, daily necessity review",
            "CAUTI prevention: avoid unnecessary catheters, aseptic insertion, remove when not needed",
            "VAP prevention: HOB elevation, daily SBT, oral chlorhexidine, subglottic suctioning",
            "SSI prevention: timely antibiotics, chlorhexidine bath, normothermia, glycemic control",
            "Hand hygiene most effective single measure, compliance <50% in most hospitals",
            "Contact precautions for MDRO prevent transmission"
        ],
        primary_authority=[
            "CDC HAI Prevention Guidelines",
            "SHEA Compendium of Strategies to Prevent HAI 2022",
            "Pronovost PJ et al. N Engl J Med 2006;355(26):2725-2732 (Michigan Keystone CLABSI)"
        ],
        burden_holder="Hospital infection control and clinical staff",
        adversary_position="Bundle compliance adds time and cost without proven benefit in all settings",
        counter_arguments=[
            "Not all bundle components equally effective; hand hygiene and chlorhexidine most critical",
            "Daily necessity review depends on physician engagement, often incomplete"
        ],
        resolution_strategy="Implement evidence-based bundles with auditing and feedback; enforce hand hygiene; remove devices when unnecessary; use contact precautions for MDRO; track and report HAI rates",
        entity_scope="All hospitalized patients at risk for HAI",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Strong evidence from RCTs and quality improvement studies",
        controlling_precedent="CDC HAI prevention guidelines and SHEA Compendium",
        issue_category=IssueCategory.HEALTHCARE_ASSOCIATED_INFECTIONS,
        zone=AnalysisZone.INFECTION_CONTROL_AUDIT
    ),

    DoctrineBlock(
        topic="Febrile Neutropenia Management",
        keywords=["febrile neutropenia", "neutropenic fever", "chemotherapy", "anc", "cefepime", "filgrastim", "gcsf"],
        conclusion_template=[
            "Febrile neutropenia defined as single temperature >=38.3C or >=38.0C for >=1 hour with absolute neutrophil count (ANC) <500 cells/mcL or expected to fall <500.",
            "High-risk patients (prolonged neutropenia, hypotension, mucositis, pneumonia) require IV antibiotics (cefepime or pip-tazo) and hospitalization.",
            "Low-risk patients (MASCC score >=21, expected short neutropenia, no comorbidities) can receive oral fluoroquinolone + amoxicillin-clavulanate outpatient."
        ],
        reasoning_framework="""
1. Febrile neutropenia occurs in 10-50% of chemotherapy patients, mortality 5-20% if untreated, <5% with prompt antibiotics
2. Absolute neutrophil count (ANC) = WBC x (% neutrophils + % bands); ANC <500 defines neutropenia, <100 profound neutropenia
3. Fever definition: single oral temp >=38.3C (101F) or >=38.0C (100.4F) sustained >=1 hour
4. High-risk criteria: expected neutropenia >7 days, ANC <100, hemodynamic instability, pneumonia, abdominal pain, mucositis, catheter infection, age >65, MASCC score <21
5. MASCC score (Multinational Association for Supportive Care in Cancer): predicts low-risk febrile neutropenia, score >=21 identifies candidates for outpatient therapy
6. MASCC components: burden of illness (mild=5, moderate=3), no hypotension (5), no COPD (4), solid tumor or lymphoma no prior fungal (4), outpatient status (3), no dehydration (3), age <60 (2)
7. Empiric antibiotics high-risk: cefepime 2g IV q8h or piperacillin-tazobactam 4.5g IV q6h monotherapy, covers Pseudomonas and gram-negatives
8. Add vancomycin 15-20 mg/kg IV q8-12h if: catheter infection, skin/soft tissue infection, pneumonia, hemodynamic instability, mucositis, prior MRSA colonization
9. Add antifungal (echinocandin or amphotericin) if: persistent fever >=4-7 days despite broad-spectrum antibiotics, high risk for invasive fungal infection
10. Granulocyte colony-stimulating factor (G-CSF, filgrastim 5 mcg/kg SC daily): shortens neutropenia duration, use if high-risk features or neutropenia expected >7 days
11. Duration of antibiotics: until ANC >500 and afebrile >=48 hours; do NOT stop at 7-10 days if still neutropenic
12. Prophylactic fluoroquinolone (levofloxacin 500mg daily) during expected neutropenia reduces febrile neutropenia 50% but increases resistance
13. Antifungal prophylaxis (fluconazole or posaconazole) for acute leukemia or allogeneic stem cell transplant reduces invasive fungal infections
14. Blood cultures x2 sets (peripheral and catheter if present) before antibiotics, urine culture, respiratory cultures if symptoms
15. Do NOT delay antibiotics for imaging or cultures if febrile neutropenia suspected; obtain cultures rapidly then start antibiotics within 1 hour
16. Imaging: chest X-ray for respiratory symptoms (CT chest if X-ray normal and symptoms persist, higher sensitivity for fungal pneumonia)
17. Pneumocystis jirovecii pneumonia (PCP) prophylaxis: TMP-SMX DS 1 tab daily or 3x/week during chemotherapy if CD4 <200 or high-dose steroids
18. Catheter-related bloodstream infection (CRBSI): if same organism from catheter and peripheral blood, or DTP >=2 hours, remove catheter if S. aureus, Candida, or Pseudomonas
19. Hepatosplenic candidiasis (chronic disseminated candidiasis): fever, RUQ pain, elevated alk phos during neutropenia recovery, CT shows liver/spleen microabscesses, requires prolonged antifungal (6-12 months)
20. Breakthrough bacteremia on prophylaxis: organisms often resistant (fluoroquinolone-resistant E. coli), use broad-spectrum empiric therapy (carbapenem or pip-tazo)
        """,
        key_factors=[
            "Febrile neutropenia: fever >=38.3C with ANC <500 or expected to fall <500",
            "High-risk: neutropenia >7 days, hypotension, pneumonia, mucositis, MASCC <21",
            "Empiric IV antibiotics (cefepime or pip-tazo) within 1 hour, hospitalization for high-risk",
            "Add vancomycin if catheter infection, MRSA risk, or hemodynamic instability",
            "G-CSF (filgrastim) if high-risk features or neutropenia >7 days expected",
            "Continue antibiotics until ANC >500 and afebrile >=48 hours"
        ],
        primary_authority=[
            "IDSA Febrile Neutropenia Guidelines 2011",
            "NCCN Hematopoietic Growth Factors Guidelines 2024",
            "Freifeld AG et al. Clin Infect Dis 2011;52(4):e56-e93"
        ],
        burden_holder="Oncology and infectious disease clinicians",
        adversary_position="Prophylactic fluoroquinolones increase resistance, benefits uncertain",
        counter_arguments=[
            "MASCC score requires validation in different populations, misclassification risk",
            "Outpatient management requires reliable patient with close follow-up"
        ],
        resolution_strategy="Assess risk using MASCC score; hospitalize high-risk patients with IV antibiotics (cefepime ± vancomycin); use G-CSF if high-risk; outpatient oral therapy for low-risk only with close follow-up",
        entity_scope="Chemotherapy patients with febrile neutropenia",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Evidence-based guidelines with RCT support",
        controlling_precedent="IDSA febrile neutropenia guidelines",
        issue_category=IssueCategory.IMMUNOCOMPROMISED_HOST,
        zone=AnalysisZone.ACUTE_MANAGEMENT
    ),

    DoctrineBlock(
        topic="Antibiotic Dosing in Renal Impairment",
        keywords=["renal dosing", "creatinine clearance", "dialysis", "beta-lactam", "vancomycin", "aminoglycoside"],
        conclusion_template=[
            "Most antibiotics require renal dose adjustments for CrCl <50 mL/min to prevent toxicity and maintain efficacy.",
            "Beta-lactams: extend interval (e.g., cefepime q24h instead of q8h) or reduce dose; vancomycin: adjust based on levels and CrCl; aminoglycosides: extend interval to q24-48h.",
            "Hemodialysis removes many antibiotics (beta-lactams, vancomycin, aminoglycosides); dose after dialysis or use supplemental dose."
        ],
        reasoning_framework="""
1. Creatinine clearance (CrCl) estimation: Cockcroft-Gault formula most widely used for drug dosing, eGFR (MDRD, CKD-EPI) less accurate for extremes
2. Cockcroft-Gault: CrCl (mL/min) = [(140 - age) x IBW (kg)] / (72 x SCr) x 0.85 if female
3. Ideal body weight (IBW): males 50 + 2.3 kg per inch over 5 ft, females 45.5 + 2.3 kg per inch over 5 ft
4. Obesity: use adjusted body weight for CrCl = IBW + 0.4 x (actual - IBW)
5. Beta-lactams renally eliminated: cefepime, ceftazidime, pip-tazo, meropenem, imipenem require dose adjustment CrCl <50
6. Cefepime renal dosing: CrCl 30-60 q12h, 11-29 q24h, <10 q48h; neurotoxicity risk if overdosed (seizures, encephalopathy)
7. Pip-tazo renal dosing: CrCl 20-40 give 3.375g q8h, <20 give 2.25g q8h; adjust for dialysis 2.25g q12h + 0.75g after each HD
8. Meropenem renal dosing: CrCl 26-50 q12h, 10-25 half dose q12h, <10 half dose q24h
9. Vancomycin renal dosing: loading dose 25-30 mg/kg regardless of renal function, then adjust based on CrCl and levels
10. Vancomycin maintenance: CrCl 50-90 q12h, 30-50 q24h, 15-30 q48h, <15 q96h or redose when level <15 mcg/mL
11. Aminoglycosides (gentamicin, tobramycin): extend interval dosing q24h if CrCl >60, q36h if 40-60, q48h if 20-40, monitor peak/trough
12. Aminoglycoside levels: peak 5-10 mcg/mL (drawn 30 min after infusion), trough <2 mcg/mL (drawn before next dose)
13. Fluoroquinolones: levofloxacin 750mg → 500mg daily if CrCl 20-49, 500mg q48h if CrCl 10-19; ciprofloxacin less renal adjustment needed
14. Aztreonam: CrCl 10-30 give half dose at normal interval, <10 give 1/4 dose at normal interval
15. Linezolid: no renal adjustment needed, not removed by dialysis, ideal for MRSA in ESRD
16. Daptomycin: CrCl <30 give q48h instead of q24h, HD/CRRT give 6-10 mg/kg after dialysis (3x/week dosing)
17. Ceftaroline: CrCl 30-50 give 400mg q12h, 15-30 give 300mg q12h, <15 give 200mg q12h
18. TMP-SMX: reduce dose by 50% if CrCl 15-30, avoid if <15 (sulfa metabolite accumulation, crystalluria risk)
19. Hemodialysis removal: beta-lactams (dose after HD), vancomycin (dose after HD with level monitoring), aminoglycosides (dose after HD)
20. CRRT (continuous renal replacement therapy): typically requires standard or higher doses due to continuous clearance; therapeutic drug monitoring essential
        """,
        key_factors=[
            "CrCl <50 mL/min requires dose adjustments for most renally eliminated antibiotics",
            "Beta-lactams: extend interval or reduce dose based on CrCl",
            "Vancomycin: loading dose unchanged, adjust maintenance by CrCl and levels",
            "Aminoglycosides: extend interval dosing q24-48h, monitor peak/trough",
            "Hemodialysis: dose beta-lactams, vancomycin, aminoglycosides after dialysis",
            "CRRT: standard or higher doses due to continuous clearance"
        ],
        primary_authority=[
            "Sanford Guide to Antimicrobial Therapy 2024",
            "Lexicomp/UpToDate Renal Dosing Database",
            "Matzke GR et al. Pharmacotherapy 2011;31(10):912-921"
        ],
        burden_holder="Prescribing clinician and pharmacist",
        adversary_position="Standard dosing risks toxicity; underdosing risks treatment failure",
        counter_arguments=[
            "Cockcroft-Gault overestimates CrCl in obesity, underestimates in elderly",
            "CRRT clearance variable, therapeutic drug monitoring preferred over nomograms"
        ],
        resolution_strategy="Calculate CrCl using Cockcroft-Gault with IBW (or adjusted if obese); adjust antibiotic doses per renal function; monitor drug levels (vancomycin, aminoglycosides); dose after dialysis for HD patients; use TDM for CRRT",
        entity_scope="Patients with renal impairment receiving antibiotics",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Evidence-based dosing guidelines with pharmacokinetic studies",
        controlling_precedent="Sanford Guide and Lexicomp renal dosing recommendations",
        issue_category=IssueCategory.ANTIBIOTIC_DOSING,
        zone=AnalysisZone.STEWARDSHIP_REVIEW
    ),

    DoctrineBlock(
        topic="Infection Control - Isolation Precautions",
        keywords=["isolation", "contact precautions", "droplet", "airborne", "n95", "mrsa", "cdiff", "tuberculosis"],
        conclusion_template=[
            "Standard precautions apply to all patients (hand hygiene, PPE for blood/body fluid exposure); transmission-based precautions for specific pathogens.",
            "Contact precautions (MRSA, VRE, CRE, C. diff): gown and gloves, dedicated equipment, single room or cohort.",
            "Droplet precautions (influenza, COVID-19): surgical mask, eye protection; Airborne precautions (TB, measles, varicella): N95 respirator, negative pressure room."
        ],
        reasoning_framework="""
1. Standard precautions: hand hygiene before/after patient contact, PPE based on anticipated exposure (gloves for body fluids, gown for splash risk, mask/eye protection for aerosols)
2. Hand hygiene: alcohol-based hand rub preferred (faster, better compliance, less skin irritation), soap/water if hands visibly soiled or C. diff (alcohol does not kill spores)
3. Contact precautions: organisms spread by direct contact or contaminated surfaces (MRSA, VRE, CRE, ESBL, C. diff, scabies, lice)
4. Contact precautions PPE: gown and gloves on room entry, remove before exiting, dedicated equipment (stethoscope, BP cuff, thermometer) or disinfect after use
5. Contact precautions duration: until discharge or 3 negative surveillance cultures 1 week apart (varies by institution, CDC does not recommend routine decolonization for most MDRO)
6. Droplet precautions: pathogens in large respiratory droplets (>5 microns) that travel <6 ft (influenza, RSV, pertussis, meningococcus, COVID-19 as droplet + contact)
7. Droplet precautions PPE: surgical mask, eye protection (goggles or face shield), gown/gloves if contact with secretions expected
8. Droplet precautions room: private room preferred, or cohort, door can remain open (droplets do not remain airborne)
9. Airborne precautions: pathogens in small droplet nuclei (<5 microns) that remain airborne and travel >6 ft (Mycobacterium tuberculosis, measles, varicella, disseminated zoster)
10. Airborne precautions PPE: N95 respirator (fit-tested), negative pressure airborne infection isolation room (AIIR, >=12 air changes/hour)
11. Airborne precautions duration: TB until 3 negative AFB sputum smears on separate days + 2 weeks effective therapy + clinical improvement
12. N95 respirator fit testing: annual quantitative or qualitative fit test required, seal check each use, discard if wet or soiled
13. COVID-19 isolation: contact + droplet precautions, N95 for aerosol-generating procedures (intubation, bronchoscopy, nebulizer), discontinue after 10 days + resolution of fever + improving symptoms
14. C. diff isolation: contact precautions, soap and water hand hygiene (alcohol does not kill spores), bleach cleaning (1:10 dilution sodium hypochlorite)
15. MRSA decolonization: nasal mupirocin 2% BID x5 days + chlorhexidine baths daily x5 days, reduces MRSA SSI in cardiac/orthopedic surgery, does NOT eliminate carriage long-term
16. VRE colonization: contact precautions, no decolonization regimen proven effective, environmental cleaning critical (VRE survives on surfaces weeks)
17. Scabies: contact precautions until 24 hours after treatment (permethrin 5% cream), bag clothes/linens in plastic 3 days
18. Varicella (chickenpox): airborne + contact precautions until all lesions crusted (5-7 days after rash onset), contagious 1-2 days before rash
19. Measles: airborne precautions for 4 days after rash onset in immunocompetent, duration of illness in immunocompromised
20. Visitors: limit visitors for airborne/contact precautions, require PPE for contact/droplet, screen for symptoms, no visitors if visitor has symptoms
        """,
        key_factors=[
            "Standard precautions for all patients: hand hygiene, PPE for exposure risk",
            "Contact precautions (gown + gloves): MRSA, VRE, CRE, ESBL, C. diff",
            "Droplet precautions (surgical mask): influenza, COVID-19, meningococcus",
            "Airborne precautions (N95 + AIIR): TB, measles, varicella",
            "C. diff requires soap/water hand hygiene and bleach cleaning (alcohol/routine disinfectants ineffective)",
            "N95 fit testing required annually, seal check each use"
        ],
        primary_authority=[
            "CDC Isolation Precautions Guidelines 2007 (updated 2019)",
            "Siegel JD et al. HICPAC Guideline 2007",
            "CDC Guideline for Disinfection and Sterilization 2008"
        ],
        burden_holder="Infection control and clinical staff",
        adversary_position="Isolation precautions reduce nurse-patient contact time and patient satisfaction",
        counter_arguments=[
            "Universal gown/glove use for all patients not cost-effective and reduces compliance",
            "Prolonged isolation for MDRO colonization may not reduce transmission if environmental cleaning robust"
        ],
        resolution_strategy="Apply standard precautions universally; use transmission-based precautions per pathogen; hand hygiene with alcohol-based rub (soap/water for C. diff); N95 + AIIR for airborne pathogens; dedicate equipment for contact precautions",
        entity_scope="All healthcare settings and patients",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Evidence-based CDC guidelines with strong consensus",
        controlling_precedent="CDC HICPAC isolation precautions guidelines",
        issue_category=IssueCategory.INFECTION_CONTROL,
        zone=AnalysisZone.INFECTION_CONTROL_AUDIT
    ),
]


# ============================================================================
# ENGINE CORE
# ============================================================================

class MED10InfectiousDiseaseEngine:
    """TIE-Grade Infectious Disease Analysis Engine"""

    def __init__(self):
        self.version = "1.0.0"
        self.port = 9235
        self.start_time = time.time()
        self.total_queries = 0
        self.cache_hits = 0
        self.metrics_log: List[QueryMetrics] = []

        # Build keyword index for fast doctrine lookup
        self.keyword_index = self._build_keyword_index()

        logger.info(f"MED10 Infectious Disease Engine v{self.version} initialized on port {self.port}")
        logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")

    def _build_keyword_index(self) -> Dict[str, List[int]]:
        """Build inverted index of keywords to doctrine indices"""
        index = defaultdict(list)
        for idx, doctrine in enumerate(DOCTRINE_CACHE):
            for keyword in doctrine.keywords:
                index[keyword.lower()].append(idx)
        return index

    def _normalize_query(self, query: str) -> str:
        """Normalize query terms for semantic matching"""
        query = query.lower()
        # Infectious disease term normalization
        replacements = {
            "c. diff": "clostridium difficile",
            "cdiff": "clostridium difficile",
            "c diff": "clostridium difficile",
            "mrsa": "methicillin resistant staphylococcus aureus",
            "mssa": "methicillin sensitive staphylococcus aureus",
            "vre": "vancomycin resistant enterococcus",
            "esbl": "extended spectrum beta lactamase",
            "kpc": "klebsiella pneumoniae carbapenemase",
            "cre": "carbapenem resistant enterobacterales",
            "hiv": "human immunodeficiency virus",
            "art": "antiretroviral therapy",
            "tb": "tuberculosis",
            "ripe": "rifampin isoniazid pyrazinamide ethambutol",
            "vap": "ventilator associated pneumonia",
            "clabsi": "central line associated bloodstream infection",
            "cauti": "catheter associated urinary tract infection",
            "hai": "healthcare associated infection",
            "ssi": "surgical site infection",
            "pct": "procalcitonin",
            "sofa": "sequential organ failure assessment",
            "qsofa": "quick sofa",
        }
        for old, new in replacements.items():
            query = query.replace(old, new)
        return query

    def _match_doctrines(self, query: str) -> List[Tuple[int, float]]:
        """Match query to relevant doctrines with confidence scores"""
        normalized = self._normalize_query(query)
        tokens = set(normalized.split())

        scores = []
        for idx, doctrine in enumerate(DOCTRINE_CACHE):
            # Keyword overlap score
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in normalized)
            keyword_score = keyword_matches / len(doctrine.keywords)

            # Topic relevance score
            topic_score = 1.0 if any(word in doctrine.topic.lower() for word in tokens) else 0.0

            # Combined score
            total_score = (keyword_score * 0.7) + (topic_score * 0.3)

            if total_score > 0.1:
                scores.append((idx, total_score))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:5]  # Top 5 matches

    def _format_response(self, doctrines: List[DoctrineBlock], mode: ResponseMode) -> str:
        """Format response based on mode and matched doctrines"""
        if mode == ResponseMode.FAST:
            # Concise summary
            parts = []
            for doctrine in doctrines[:2]:
                parts.extend(doctrine.conclusion_template)
            return " ".join(parts)

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready with authorities
            parts = []
            for doctrine in doctrines:
                parts.append(f"**{doctrine.topic}**")
                parts.extend(doctrine.conclusion_template)
                parts.append("\nAuthorities: " + "; ".join(doctrine.primary_authority))
                parts.append("\nKey Factors: " + "; ".join(doctrine.key_factors))
                parts.append("")
            return "\n".join(parts)

        else:  # MEMO
            # Full documentation with reasoning
            parts = []
            for doctrine in doctrines:
                parts.append(f"# {doctrine.topic}")
                parts.append("\n## Conclusion")
                parts.extend(doctrine.conclusion_template)
                parts.append("\n## Reasoning Framework")
                parts.append(doctrine.reasoning_framework)
                parts.append("\n## Key Factors")
                for factor in doctrine.key_factors:
                    parts.append(f"- {factor}")
                parts.append("\n## Primary Authority")
                for auth in doctrine.primary_authority:
                    parts.append(f"- {auth}")
                parts.append("\n## Risk Stratification")
                parts.append(f"Confidence: {doctrine.confidence.value}")
                parts.append(f"Stratification: {doctrine.confidence_stratification}")
                parts.append("")
            return "\n".join(parts)

    def _calculate_determinism_hash(self, query: str, answer: str, doctrines: List[str]) -> str:
        """Calculate SHA-256 hash for reproducibility verification"""
        content = f"{query}|{answer}|{sorted(doctrines)}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _get_epistemic_caveats(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Generate epistemic caveats based on confidence levels"""
        caveats = []

        high_risk_count = sum(1 for d in doctrines if d.confidence == ConfidenceLevel.HIGH_RISK)
        disclosure_count = sum(1 for d in doctrines if d.confidence == ConfidenceLevel.DISCLOSURE)

        if high_risk_count > 0:
            caveats.append("Analysis involves high-risk clinical scenarios requiring specialist consultation")

        if disclosure_count > 0:
            caveats.append("Evolving evidence base - guidelines subject to updates as new data emerges")

        if any("meta-analysis" in auth.lower() for d in doctrines for auth in d.primary_authority):
            caveats.append("Recommendations based on systematic reviews and meta-analyses")

        caveats.append("Clinical judgment and patient-specific factors override general guidelines")

        return caveats

    async def query(self, request: QueryRequest) -> QueryResponse:
        """Process infectious disease query with three-layer response"""
        start = time.time()
        query_id = hashlib.md5(f"{request.query}{time.time()}".encode()).hexdigest()[:12]

        self.total_queries += 1

        # LAYER 1: Doctrine cache (0-200ms)
        cache_start = time.time()
        matched = self._match_doctrines(request.query)
        cache_latency = (time.time() - cache_start) * 1000

        cache_hit = len(matched) > 0
        if cache_hit:
            self.cache_hits += 1

        # Retrieve doctrine blocks
        doctrines = [DOCTRINE_CACHE[idx] for idx, score in matched]

        # LAYER 2: Semantic retrieval (fallback if cache miss - not implemented in this version)
        semantic_latency = 0.0

        # LAYER 3: Deep analysis (not needed for doctrine cache hits)
        deep_latency = 0.0

        # Format response
        answer = self._format_response(doctrines, request.mode)

        # Extract metadata
        doctrines_applied = [d.topic for d in doctrines]
        authorities = list(set(auth for d in doctrines for auth in d.primary_authority))

        # Determine overall confidence
        confidence = doctrines[0].confidence if doctrines else ConfidenceLevel.DISCLOSURE

        # Calculate determinism hash
        det_hash = self._calculate_determinism_hash(request.query, answer, doctrines_applied)

        # Get epistemic caveats
        caveats = self._get_epistemic_caveats(doctrines)

        total_latency = (time.time() - start) * 1000

        # Log metrics
        metrics = QueryMetrics(
            query_id=query_id,
            timestamp=time.time(),
            mode=request.mode,
            cache_hit=cache_hit,
            cache_latency_ms=cache_latency,
            semantic_latency_ms=semantic_latency,
            deep_latency_ms=deep_latency,
            total_latency_ms=total_latency,
            doctrines_triggered=doctrines_applied,
            confidence_level=confidence
        )
        self.metrics_log.append(metrics)

        logger.info(f"Query {query_id}: {len(doctrines)} doctrines, {total_latency:.1f}ms, cache_hit={cache_hit}")

        return QueryResponse(
            query_id=query_id,
            answer=answer,
            mode=request.mode,
            confidence=confidence,
            doctrines_applied=doctrines_applied,
            authorities_cited=authorities[:10],  # Limit to top 10
            reasoning_chain=[d.reasoning_framework[:200] + "..." for d in doctrines[:3]] if request.mode == ResponseMode.MEMO else None,
            latency_ms=total_latency,
            determinism_hash=det_hash,
            epistemic_caveats=caveats,
            timestamp=datetime.utcnow().isoformat()
        )

    def get_health(self) -> HealthResponse:
        """Return comprehensive health status"""
        uptime = time.time() - self.start_time
        cache_hit_rate = (self.cache_hits / self.total_queries * 100) if self.total_queries > 0 else 0.0
        avg_latency = sum(m.total_latency_ms for m in self.metrics_log) / len(self.metrics_log) if self.metrics_log else 0.0

        return HealthResponse(
            status="operational",
            engine="MED10_Infectious_Disease_Analysis",
            version=self.version,
            port=self.port,
            doctrine_count=len(DOCTRINE_CACHE),
            total_queries=self.total_queries,
            cache_hit_rate=round(cache_hit_rate, 2),
            avg_latency_ms=round(avg_latency, 2),
            uptime_seconds=round(uptime, 2)
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(title="MED10 Infectious Disease Analysis Engine", version="1.0.0")

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ENGINE = MED10InfectiousDiseaseEngine()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Process infectious disease clinical query"""
    try:
        return await ENGINE.query(request)
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Engine health and metrics"""
    return ENGINE.get_health()


@APP.get("/doctrines")
async def doctrines_endpoint():
    """Return all doctrine topics and metadata"""
    return {
        "count": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "category": d.issue_category.value,
                "zone": d.zone.value,
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }


@APP.get("/metrics")
async def metrics_endpoint():
    """Return detailed query metrics"""
    return {
        "total_queries": ENGINE.total_queries,
        "cache_hits": ENGINE.cache_hits,
        "cache_hit_rate": round((ENGINE.cache_hits / ENGINE.total_queries * 100) if ENGINE.total_queries > 0 else 0.0, 2),
        "recent_queries": [
            {
                "query_id": m.query_id,
                "mode": m.mode.value,
                "latency_ms": round(m.total_latency_ms, 2),
                "cache_hit": m.cache_hit,
                "doctrines_triggered": len(m.doctrines_triggered)
            }
            for m in ENGINE.metrics_log[-20:]
        ]
    }


if __name__ == "__main__":
    logger.add("med10_infectious_disease.log", rotation="100 MB", retention="30 days", level="INFO")
    logger.info("Starting MED10 Infectious Disease Analysis Engine v1.0.0 on port 9235")

    uvicorn.run(
        APP,
        host="0.0.0.0",
        port=9235,
        log_level="info",
        access_log=True
    )
