from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from pathlib import Path

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
        topic="Sepsis-3 Criteria and qSOFA Screening",
        keywords=["sepsis", "qSOFA", "SOFA", "organ dysfunction", "infection", "screening"],
        conclusion_template="A patient with suspected infection and an acute increase in SOFA score ≥2 meets Sepsis-3 criteria; qSOFA score ≥2 suggests high risk of poor outcome.",
        reasoning_framework=(
            "1. Assess for suspected or documented infection.\n"
            "2. Calculate SOFA score; an acute increase of ≥2 points indicates organ dysfunction.\n"
            "3. Use qSOFA (altered mentation, systolic BP ≤100 mmHg, RR ≥22/min) as a bedside prompt for sepsis risk.\n"
            "4. Recognize that qSOFA is a screening tool, not diagnostic; a positive qSOFA warrants further evaluation.\n"
            "5. Confirm sepsis diagnosis with full SOFA assessment and clinical correlation.\n"
            "6. Initiate prompt management if criteria are met."
        ),
        key_factors=["SOFA score", "qSOFA score", "clinical suspicion of infection", "organ dysfunction"],
        primary_authority=["Singer M et al., JAMA 2016", "Surviving Sepsis Campaign 2021"],
        burden_holder="Clinician",
        adversary_position="qSOFA is insufficiently sensitive for early sepsis detection.",
        counter_arguments=[
            "qSOFA is intended as a prompt, not a definitive diagnostic tool.",
            "SOFA score remains the gold standard for organ dysfunction assessment."
        ],
        resolution_strategy="Use qSOFA for rapid screening and SOFA for definitive diagnosis.",
        entity_scope="Adult inpatients and ED patients with suspected infection.",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Sepsis-3 Consensus Definitions (Singer et al., 2016)"
    ),
    DoctrineBlock(
        topic="Empiric Antibiotic Selection for Sepsis",
        keywords=["antibiotics", "sepsis", "empiric therapy", "broad-spectrum", "timing"],
        conclusion_template="Initiate broad-spectrum empiric antibiotics within 1 hour of sepsis recognition, tailored to likely pathogens and local resistance patterns.",
        reasoning_framework=(
            "1. Recognize sepsis or septic shock based on clinical and laboratory criteria.\n"
            "2. Identify likely source of infection (e.g., lung, urinary tract, abdomen).\n"
            "3. Review patient risk factors for resistant organisms (recent hospitalization, prior antibiotics, immunosuppression).\n"
            "4. Select empiric antibiotics covering both Gram-positive and Gram-negative organisms, and anaerobes if indicated.\n"
            "5. Consider local antibiogram data and guidelines.\n"
            "6. Administer antibiotics as soon as possible, ideally within 1 hour.\n"
            "7. Reassess and de-escalate therapy based on culture results and clinical response."
        ),
        key_factors=["timing of antibiotics", "local resistance patterns", "infection source", "patient risk factors"],
        primary_authority=["Surviving Sepsis Campaign 2021", "IDSA Sepsis Guidelines"],
        burden_holder="Treating physician",
        adversary_position="Delaying antibiotics until pathogen identification reduces resistance.",
        counter_arguments=[
            "Delays in antibiotics increase mortality in sepsis.",
            "Empiric therapy can be de-escalated once cultures are available."
        ],
        resolution_strategy="Start broad-spectrum empiric therapy immediately, then narrow based on data.",
        entity_scope="All patients with suspected or confirmed sepsis.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Surviving Sepsis Campaign Guidelines"
    ),
    DoctrineBlock(
        topic="Blood Culture Interpretation - True Positive vs Contaminant",
        keywords=["blood cultures", "contamination", "true infection", "bacteremia", "diagnosis"],
        conclusion_template="Interpret blood culture results in clinical context; single positive for common skin flora often represents contamination.",
        reasoning_framework=(
            "1. Review organism isolated (e.g., coagulase-negative staphylococci, Corynebacterium spp. are common contaminants).\n"
            "2. Assess number of positive culture sets and timing.\n"
            "3. Correlate with clinical signs of infection and laboratory markers.\n"
            "4. Consider patient risk factors for true bacteremia (immunosuppression, indwelling lines).\n"
            "5. Repeat cultures if contamination is suspected.\n"
            "6. Avoid unnecessary antibiotics for likely contaminants."
        ),
        key_factors=["organism type", "number of positive cultures", "clinical context", "patient risk factors"],
        primary_authority=["IDSA Bloodstream Infection Guidelines", "CDC Laboratory Standards"],
        burden_holder="Laboratory and clinician",
        adversary_position="All positive cultures should be treated as true infection.",
        counter_arguments=[
            "Overtreatment increases adverse events and resistance.",
            "Contaminants are common and rarely cause disease."
        ],
        resolution_strategy="Use clinical judgment and repeat cultures to distinguish true infection from contamination.",
        entity_scope="Hospitalized and outpatient populations.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IDSA Guidelines for Bloodstream Infections"
    ),
    DoctrineBlock(
        topic="MRSA Management and Vancomycin Dosing",
        keywords=["MRSA", "vancomycin", "dosing", "trough", "AUC", "monitoring"],
        conclusion_template="Treat MRSA infections with vancomycin dosed to achieve AUC/MIC 400-600; monitor renal function and adjust as needed.",
        reasoning_framework=(
            "1. Confirm MRSA infection by culture and susceptibility testing.\n"
            "2. Initiate vancomycin at weight-based dosing (15-20 mg/kg IV q8-12h).\n"
            "3. Target AUC/MIC ratio of 400-600 for efficacy and safety.\n"
            "4. Use Bayesian software or first-order PK equations to estimate AUC.\n"
            "5. Monitor serum creatinine and vancomycin levels (troughs or AUC-guided).\n"
            "6. Adjust dosing based on renal function and drug levels.\n"
            "7. Consider alternative agents if vancomycin intolerance or failure."
        ),
        key_factors=["AUC/MIC ratio", "renal function", "drug levels", "infection severity"],
        primary_authority=["IDSA MRSA Guidelines 2020", "ASHP Vancomycin Monitoring Consensus"],
        burden_holder="Prescribing clinician",
        adversary_position="Fixed dosing without monitoring is sufficient.",
        counter_arguments=[
            "Therapeutic drug monitoring reduces toxicity and improves outcomes.",
            "AUC-guided dosing is superior to trough-based monitoring."
        ],
        resolution_strategy="Implement AUC-guided vancomycin dosing with regular monitoring.",
        entity_scope="Adults and children with MRSA infections.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IDSA MRSA Treatment Guidelines"
    ),
    DoctrineBlock(
        topic="C. difficile Infection Diagnosis and Management",
        keywords=["Clostridioides difficile", "C. diff", "diagnosis", "treatment", "stool testing"],
        conclusion_template="Diagnose C. difficile infection with compatible symptoms and positive stool test; treat with oral vancomycin or fidaxomicin.",
        reasoning_framework=(
            "1. Suspect C. difficile in patients with new-onset, unexplained, ≥3 unformed stools in 24 hours.\n"
            "2. Order stool testing for C. difficile toxin and/or NAAT.\n"
            "3. Do not test asymptomatic patients or repeat tests during same episode.\n"
            "4. Initiate oral vancomycin (125 mg q6h) or fidaxomicin for 10 days.\n"
            "5. Avoid anti-motility agents.\n"
            "6. Implement contact precautions and environmental cleaning.\n"
            "7. Consider fecal microbiota transplantation for recurrent cases."
        ),
        key_factors=["diarrhea", "positive stool test", "recent antibiotics", "infection control"],
        primary_authority=["IDSA/SHEA C. difficile Guidelines 2021"],
        burden_holder="Clinician",
        adversary_position="Metronidazole is sufficient for all cases.",
        counter_arguments=[
            "Oral vancomycin and fidaxomicin are superior for initial episodes.",
            "Metronidazole reserved for non-severe cases if other agents unavailable."
        ],
        resolution_strategy="Use guideline-recommended agents and strict infection control.",
        entity_scope="Adult and pediatric inpatients and outpatients.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IDSA/SHEA C. difficile Guidelines"
    ),
    DoctrineBlock(
        topic="Antimicrobial Stewardship Program Core Elements",
        keywords=["antimicrobial stewardship", "ASP", "core elements", "program", "hospital"],
        conclusion_template="Implement ASPs with leadership commitment, accountability, drug expertise, action, tracking, reporting, and education.",
        reasoning_framework=(
            "1. Secure hospital leadership support for stewardship initiatives.\n"
            "2. Designate a single program leader (physician or pharmacist).\n"
            "3. Ensure access to individuals with antimicrobial expertise.\n"
            "4. Implement at least one intervention to improve antibiotic use (e.g., prospective audit and feedback).\n"
            "5. Track antibiotic prescribing and resistance patterns.\n"
            "6. Regularly report stewardship outcomes to staff.\n"
            "7. Provide ongoing education to prescribers and staff."
        ),
        key_factors=["leadership support", "accountability", "tracking", "education", "interventions"],
        primary_authority=["CDC Core Elements of Hospital ASPs", "The Joint Commission"],
        burden_holder="Hospital administration",
        adversary_position="Stewardship programs are resource-intensive and unnecessary.",
        counter_arguments=[
            "ASPs reduce resistance, adverse events, and costs.",
            "Regulatory bodies require stewardship programs."
        ],
        resolution_strategy="Adopt CDC core elements and tailor interventions to local needs.",
        entity_scope="All acute care hospitals.",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="CDC Core Elements of Hospital ASPs"
    ),
    DoctrineBlock(
        topic="Procalcitonin-Guided Antibiotic Therapy",
        keywords=["procalcitonin", "biomarker", "antibiotic stewardship", "therapy", "de-escalation"],
        conclusion_template="Use procalcitonin levels to guide initiation and discontinuation of antibiotics in lower respiratory tract infections and sepsis.",
        reasoning_framework=(
            "1. Measure baseline procalcitonin in patients with suspected bacterial infection.\n"
            "2. Use serial procalcitonin measurements to assess response to therapy.\n"
            "3. Discontinue antibiotics if procalcitonin falls below 0.25 ng/mL or decreases by ≥80% from peak.\n"
            "4. Do not use procalcitonin in isolation; consider clinical context.\n"
            "5. Recognize limitations (e.g., false positives in trauma, surgery, renal failure).\n"
            "6. Educate clinicians on interpretation and protocol adherence."
        ),
        key_factors=["procalcitonin trend", "clinical status", "infection type", "protocol adherence"],
        primary_authority=["IDSA Procalcitonin Guidance", "Surviving Sepsis Campaign"],
        burden_holder="Prescribing clinician",
        adversary_position="Procalcitonin is unreliable and should not guide therapy.",
        counter_arguments=[
            "RCTs show reduced antibiotic use without increased harm.",
            "Clinical judgment remains paramount."
        ],
        resolution_strategy="Integrate procalcitonin with clinical assessment for stewardship.",
        entity_scope="Adults with LRTI or sepsis.",
        confidence=0.93,
        confidence_zone="Moderate-High",
        controlling_precedent="IDSA Guidance on Procalcitonin Use"
    ),
    DoctrineBlock(
        topic="HIV Treatment - Antiretroviral Therapy (ART) Initiation and Regimens",
        keywords=["HIV", "ART", "antiretroviral therapy", "initiation", "regimens"],
        conclusion_template="Initiate ART in all HIV-infected individuals regardless of CD4 count; use integrase inhibitor-based regimens as first-line.",
        reasoning_framework=(
            "1. Confirm HIV diagnosis with appropriate testing.\n"
            "2. Counsel patient on benefits and expectations of ART.\n"
            "3. Initiate ART as soon as possible, ideally same day as diagnosis.\n"
            "4. Select regimen: typically two NRTIs plus an integrase inhibitor (e.g., TDF/FTC + dolutegravir).\n"
            "5. Screen for baseline resistance, HBV/HCV coinfection, renal and hepatic function.\n"
            "6. Monitor for adherence, toxicity, and virologic response."
        ),
        key_factors=["timing of ART", "regimen selection", "baseline labs", "adherence"],
        primary_authority=["DHHS HIV Guidelines", "IAS-USA Recommendations"],
        burden_holder="HIV care provider",
        adversary_position="Delay ART until advanced disease or opportunistic infection resolution.",
        counter_arguments=[
            "Early ART improves survival and reduces transmission.",
            "Exceptions are rare (e.g., cryptococcal meningitis)."
        ],
        resolution_strategy="Initiate ART promptly in most cases.",
        entity_scope="All people with HIV infection.",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="DHHS Guidelines for the Use of Antiretroviral Agents"
    ),
    DoctrineBlock(
        topic="Tuberculosis Diagnosis and RIPE Therapy",
        keywords=["tuberculosis", "TB", "diagnosis", "RIPE", "treatment"],
        conclusion_template="Diagnose TB with clinical, radiographic, and microbiologic evidence; treat with 2 months of RIPE followed by 4 months of INH and RIF.",
        reasoning_framework=(
            "1. Suspect TB in patients with cough, weight loss, night sweats, and risk factors.\n"
            "2. Obtain chest imaging and collect sputum for AFB smear and culture.\n"
            "3. Confirm diagnosis with positive culture or NAAT.\n"
            "4. Initiate RIPE therapy: rifampin, isoniazid, pyrazinamide, ethambutol for 2 months.\n"
            "5. Continue with isoniazid and rifampin for 4 additional months.\n"
            "6. Monitor for drug toxicity and adherence.\n"
            "7. Adjust regimen based on susceptibility results."
        ),
        key_factors=["microbiologic confirmation", "drug susceptibility", "treatment duration", "toxicity monitoring"],
        primary_authority=["CDC TB Guidelines", "WHO TB Treatment Guidelines"],
        burden_holder="TB program/clinician",
        adversary_position="Shorter or alternative regimens are equally effective.",
        counter_arguments=[
            "Standard 6-month regimen is most validated.",
            "Shorter regimens are only for select cases."
        ],
        resolution_strategy="Follow standard RIPE-based therapy unless contraindicated.",
        entity_scope="Adults and children with active TB.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="CDC Guidelines for the Treatment of Tuberculosis"
    ),
    DoctrineBlock(
        topic="Carbapenem-Resistant Enterobacterales (CRE) Management",
        keywords=["CRE", "carbapenem-resistant", "Enterobacterales", "treatment", "infection control"],
        conclusion_template="Manage CRE infections with novel β-lactam/β-lactamase inhibitor combinations and strict infection control.",
        reasoning_framework=(
            "1. Identify CRE by susceptibility testing and molecular diagnostics.\n"
            "2. Implement contact precautions and cohorting.\n"
            "3. Select therapy based on susceptibility: ceftazidime-avibactam, meropenem-vaborbactam, or imipenem-relebactam preferred.\n"
            "4. Consider combination therapy for severe infections.\n"
            "5. Remove or replace infected devices when possible.\n"
            "6. Monitor for resistance emergence and adverse effects."
        ),
        key_factors=["susceptibility results", "infection control", "antibiotic selection", "device management"],
        primary_authority=["IDSA CRE Guidelines", "CDC CRE Toolkit"],
        burden_holder="Infectious diseases specialist",
        adversary_position="Older agents (colistin, tigecycline) are adequate.",
        counter_arguments=[
            "Novel agents have better efficacy and safety.",
            "Colistin is nephrotoxic and less effective."
        ],
        resolution_strategy="Use novel β-lactam/β-lactamase inhibitors when available.",
        entity_scope="Hospitalized patients with CRE infection.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IDSA Guidance on Treatment of CRE"
    ),
    DoctrineBlock(
        topic="Healthcare-Associated Infections (HAI) Prevention",
        keywords=["HAI", "prevention", "infection control", "bundles", "hospital"],
        conclusion_template="Prevent HAIs with evidence-based bundles, hand hygiene, device management, and surveillance.",
        reasoning_framework=(
            "1. Implement hand hygiene as the cornerstone of HAI prevention.\n"
            "2. Use care bundles for central lines, ventilators, and urinary catheters.\n"
            "3. Limit device use and duration.\n"
            "4. Educate staff on infection prevention protocols.\n"
            "5. Conduct active surveillance and feedback.\n"
            "6. Rapidly investigate and respond to outbreaks."
        ),
        key_factors=["hand hygiene", "device bundles", "education", "surveillance"],
        primary_authority=["CDC HAI Guidelines", "The Joint Commission"],
        burden_holder="Hospital infection prevention team",
        adversary_position="HAIs are inevitable and not preventable.",
        counter_arguments=[
            "HAI rates decrease with evidence-based interventions.",
            "Regulatory penalties for preventable HAIs."
        ],
        resolution_strategy="Adopt and monitor adherence to prevention bundles.",
        entity_scope="All acute care hospitals.",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="CDC Guidelines for HAI Prevention"
    ),
    DoctrineBlock(
        topic="Febrile Neutropenia Management",
        keywords=["febrile neutropenia", "oncology", "empiric antibiotics", "risk stratification"],
        conclusion_template="Initiate empiric broad-spectrum antibiotics immediately in febrile neutropenic patients; risk stratify for outpatient vs inpatient management.",
        reasoning_framework=(
            "1. Define febrile neutropenia: fever ≥38.3°C or ≥38.0°C sustained for 1 hour with ANC <500/μL.\n"
            "2. Obtain blood cultures and relevant diagnostics before antibiotics.\n"
            "3. Start empiric IV antibiotics within 1 hour (e.g., cefepime, carbapenem).\n"
            "4. Assess risk (MASCC score, comorbidities) for outpatient eligibility.\n"
            "5. Monitor closely for complications and adjust therapy based on cultures."
        ),
        key_factors=["timing of antibiotics", "risk stratification", "ANC count", "infection source"],
        primary_authority=["IDSA Febrile Neutropenia Guidelines", "ASCO Recommendations"],
        burden_holder="Oncology/hematology provider",
        adversary_position="Wait for culture results before starting antibiotics.",
        counter_arguments=[
            "Delays in antibiotics increase mortality.",
            "Empiric therapy is standard of care."
        ],
        resolution_strategy="Immediate empiric antibiotics with risk-based management.",
        entity_scope="Cancer patients with neutropenia and fever.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IDSA Guidelines for Febrile Neutropenia"
    ),
    DoctrineBlock(
        topic="Antibiotic Dosing in Renal Impairment",
        keywords=["antibiotic dosing", "renal impairment", "adjustment", "creatinine clearance"],
        conclusion_template="Adjust antibiotic dosing based on renal function to avoid toxicity and ensure efficacy.",
        reasoning_framework=(
            "1. Estimate renal function using Cockcroft-Gault or MDRD equations.\n"
            "2. Review antibiotic pharmacokinetics and need for adjustment.\n"
            "3. Use dosing nomograms or guidelines for specific agents.\n"
            "4. Monitor drug levels for narrow therapeutic index antibiotics (e.g., vancomycin, aminoglycosides).\n"
            "5. Reassess renal function regularly and adjust dosing as needed."
        ),
        key_factors=["renal function", "drug clearance", "toxicity risk", "therapeutic monitoring"],
        primary_authority=["Sanford Guide", "IDSA Guidance"],
        burden_holder="Prescriber and pharmacist",
        adversary_position="Standard dosing is adequate for all patients.",
        counter_arguments=[
            "Renal impairment increases risk of toxicity.",
            "Underdosing may lead to treatment failure."
        ],
        resolution_strategy="Individualize dosing based on renal function.",
        entity_scope="Patients with acute or chronic kidney disease.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Sanford Guide to Antimicrobial Therapy"
    ),
    DoctrineBlock(
        topic="Infection Control - Isolation Precautions",
        keywords=["infection control", "isolation", "precautions", "contact", "droplet", "airborne"],
        conclusion_template="Apply appropriate isolation precautions based on pathogen transmission route to prevent healthcare-associated spread.",
        reasoning_framework=(
            "1. Assess suspected or confirmed pathogen and mode of transmission.\n"
            "2. Implement standard precautions for all patients.\n"
            "3. Use contact precautions for MDROs, C. difficile, norovirus.\n"
            "4. Use droplet precautions for influenza, meningococcus, pertussis.\n"
            "5. Use airborne precautions for TB, measles, varicella.\n"
            "6. Educate staff and post signage to ensure compliance."
        ),
        key_factors=["pathogen", "transmission route", "facility resources", "staff compliance"],
        primary_authority=["CDC Isolation Precautions", "WHO Infection Control"],
        burden_holder="Infection prevention team",
        adversary_position="Universal precautions are sufficient for all pathogens.",
        counter_arguments=[
            "Transmission-based precautions reduce HAI risk.",
            "Universal precautions do not address all transmission routes."
        ],
        resolution_strategy="Match isolation level to pathogen and educate staff.",
        entity_scope="All healthcare settings.",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="CDC Guidelines for Isolation Precautions"
    ),
    DoctrineBlock(
        topic="Antibiotic De-escalation in Sepsis",
        keywords=["antibiotic de-escalation", "sepsis", "stewardship", "narrow-spectrum"],
        conclusion_template="De-escalate antibiotics in sepsis based on culture results and clinical improvement to reduce resistance and toxicity.",
        reasoning_framework=(
            "1. Start broad-spectrum empiric antibiotics for sepsis.\n"
            "2. Review microbiology results and clinical response at 48-72 hours.\n"
            "3. Narrow therapy to target identified pathogens.\n"
            "4. Discontinue unnecessary agents.\n"
            "5. Monitor for recurrence or new infection."
        ),
        key_factors=["culture results", "clinical status", "antibiotic spectrum", "resistance risk"],
        primary_authority=["Surviving Sepsis Campaign", "IDSA Guidelines"],
        burden_holder="Treating physician",
        adversary_position="Continue broad-spectrum therapy for full course.",
        counter_arguments=[
            "De-escalation reduces adverse events and resistance.",
            "No increase in mortality with de-escalation."
        ],
        resolution_strategy="Reassess and narrow therapy as soon as possible.",
        entity_scope="All patients with sepsis.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Surviving Sepsis Campaign Guidelines"
    ),
    DoctrineBlock(
        topic="Duration of Antibiotic Therapy for Common Infections",
        keywords=["antibiotic duration", "pneumonia", "UTI", "cellulitis", "short-course"],
        conclusion_template="Use shortest effective antibiotic duration for common infections: 5 days for CAP, 7 days for pyelonephritis, 5-6 days for cellulitis.",
        reasoning_framework=(
            "1. Review evidence for optimal duration by infection type.\n"
            "2. Monitor clinical response to therapy.\n"
            "3. Avoid unnecessarily prolonged courses.\n"
            "4. Educate prescribers on short-course efficacy.\n"
            "5. Adjust duration for complications or slow response."
        ),
        key_factors=["infection type", "clinical response", "guideline recommendations", "complications"],
        primary_authority=["IDSA Guidelines", "Sanford Guide"],
        burden_holder="Prescriber",
        adversary_position="Longer courses prevent relapse.",
        counter_arguments=[
            "RCTs show short courses are equally effective.",
            "Longer therapy increases adverse events."
        ],
        resolution_strategy="Follow guideline-recommended durations.",
        entity_scope="Immunocompetent adults with common infections.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IDSA Guidelines for Common Infections"
    ),
    DoctrineBlock(
        topic="Catheter-Associated Urinary Tract Infection (CAUTI) Prevention",
        keywords=["CAUTI", "urinary catheter", "prevention", "infection control", "bundle"],
        conclusion_template="Prevent CAUTI by limiting catheter use, maintaining aseptic insertion, and daily review of necessity.",
        reasoning_framework=(
            "1. Insert urinary catheters only for appropriate indications.\n"
            "2. Use aseptic technique during insertion and maintenance.\n"
            "3. Review catheter necessity daily and remove promptly when no longer needed.\n"
            "4. Educate staff on CAUTI prevention bundle.\n"
            "5. Monitor CAUTI rates and provide feedback."
        ),
        key_factors=["catheter indication", "aseptic technique", "duration of use", "staff education"],
        primary_authority=["CDC CAUTI Guidelines", "The Joint Commission"],
        burden_holder="Nursing and medical staff",
        adversary_position="Catheters are necessary for all immobile patients.",
        counter_arguments=[
            "Most CAUTIs are preventable.",
            "Alternatives (e.g., external catheters) are often appropriate."
        ],
        resolution_strategy="Strict adherence to CAUTI prevention bundle.",
        entity_scope="All hospitalized patients with urinary catheters.",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="CDC Guidelines for CAUTI Prevention"
    ),
    DoctrineBlock(
        topic="Central Line-Associated Bloodstream Infection (CLABSI) Prevention",
        keywords=["CLABSI", "central line", "bloodstream infection", "prevention", "bundle"],
        conclusion_template="Prevent CLABSI by using maximal sterile barriers, chlorhexidine skin prep, and daily review of line necessity.",
        reasoning_framework=(
            "1. Insert central lines only for appropriate indications.\n"
            "2. Use maximal sterile barrier precautions during insertion.\n"
            "3. Prep skin with chlorhexidine.\n"
            "4. Maintain sterile technique during access and dressing changes.\n"
            "5. Review line necessity daily and remove promptly.\n"
            "6. Monitor CLABSI rates and provide feedback."
        ),
        key_factors=["sterile technique", "chlorhexidine prep", "line necessity", "staff training"],
        primary_authority=["CDC CLABSI Guidelines", "The Joint Commission"],
        burden_holder="Nursing and medical staff",
        adversary_position="Central lines are low risk and do not require strict protocols.",
        counter_arguments=[
            "CLABSI bundles reduce infection rates.",
            "Strict protocols are cost-effective."
        ],
        resolution_strategy="Implement and monitor CLABSI prevention bundle.",
        entity_scope="All patients with central venous catheters.",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="CDC Guidelines for CLABSI Prevention"
    ),
    DoctrineBlock(
        topic="Surgical Site Infection (SSI) Prevention",
        keywords=["SSI", "surgical site infection", "prevention", "antibiotic prophylaxis", "skin prep"],
        conclusion_template="Prevent SSI by appropriate antibiotic prophylaxis, skin antisepsis, and glycemic control.",
        reasoning_framework=(
            "1. Administer prophylactic antibiotics within 60 minutes before incision.\n"
            "2. Use appropriate agent and dosing based on procedure and patient factors.\n"
            "3. Prep skin with alcohol-based chlorhexidine.\n"
            "4. Maintain perioperative normothermia and glycemic control.\n"
            "5. Minimize operating room traffic and maintain sterile technique."
        ),
        key_factors=["timing of antibiotics", "skin prep", "glycemic control", "sterile technique"],
        primary_authority=["CDC SSI Guidelines", "WHO Surgical Safety Checklist"],
        burden_holder="Surgical team",
        adversary_position="SSI rates are unaffected by prophylaxis timing.",
        counter_arguments=[
            "Proper timing reduces SSI risk.",
            "Multimodal prevention is most effective."
        ],
        resolution_strategy="Adhere to SSI prevention bundle.",
        entity_scope="All surgical patients.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="CDC Guidelines for SSI Prevention"
    ),
    DoctrineBlock(
        topic="Ventilator-Associated Pneumonia (VAP) Prevention",
        keywords=["VAP", "ventilator-associated pneumonia", "prevention", "bundle", "ICU"],
        conclusion_template="Prevent VAP with head-of-bed elevation, daily sedation interruption, oral care, and minimizing ventilation duration.",
        reasoning_framework=(
            "1. Elevate head of bed to 30-45 degrees.\n"
            "2. Perform regular oral care with chlorhexidine.\n"
            "3. Interrupt sedation daily to assess readiness to extubate.\n"
            "4. Avoid unnecessary ventilation and minimize duration.\n"
            "5. Use subglottic suctioning endotracheal tubes when possible."
        ),
        key_factors=["head-of-bed elevation", "oral care", "sedation interruption", "ventilation duration"],
        primary_authority=["CDC VAP Guidelines", "The Joint Commission"],
        burden_holder="ICU team",
        adversary_position="VAP is unavoidable in ventilated patients.",
        counter_arguments=[
            "VAP bundles reduce incidence.",
            "Prevention is cost-effective."
        ],
        resolution_strategy="Implement and monitor VAP prevention bundle.",
        entity_scope="All mechanically ventilated patients.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="CDC Guidelines for VAP Prevention"
    ),
    DoctrineBlock(
        topic="Contact Precautions for Multidrug-Resistant Organisms (MDROs)",
        keywords=["contact precautions", "MDRO", "infection control", "isolation", "transmission"],
        conclusion_template="Use contact precautions for patients colonized or infected with MDROs to prevent transmission.",
        reasoning_framework=(
            "1. Identify patients with MDRO colonization or infection (e.g., MRSA, VRE, CRE).\n"
            "2. Place patient in single room or cohort with same organism.\n"
            "3. Require gown and gloves for all room entry.\n"
            "4. Dedicate equipment to the patient or disinfect between uses.\n"
            "5. Educate staff and visitors on precautions."
        ),
        key_factors=["MDRO status", "isolation resources", "staff compliance", "equipment handling"],
        primary_authority=["CDC MDRO Guidelines", "WHO Infection Control"],
        burden_holder="Infection prevention team",
        adversary_position="Standard precautions are sufficient for MDROs.",
        counter_arguments=[
            "Contact precautions reduce MDRO transmission.",
            "Standard precautions do not address environmental contamination."
        ],
        resolution_strategy="Strict implementation of contact precautions.",
        entity_scope="All healthcare settings.",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="CDC Guidelines for MDRO Control"
    ),
    DoctrineBlock(
        topic="Outpatient Parenteral Antimicrobial Therapy (OPAT) Best Practices",
        keywords=["OPAT", "outpatient", "IV antibiotics", "monitoring", "safety"],
        conclusion_template="Ensure OPAT safety with appropriate patient selection, monitoring, and clear communication.",
        reasoning_framework=(
            "1. Select patients who are clinically stable and able to adhere to OPAT.\n"
            "2. Choose antimicrobials with suitable dosing intervals and stability.\n"
            "3. Establish monitoring plan for labs, adverse events, and line complications.\n"
            "4. Provide education to patient and caregivers.\n"
            "5. Maintain clear communication between OPAT team, patient, and primary provider."
        ),
        key_factors=["patient selection", "antibiotic choice", "monitoring plan", "education"],
        primary_authority=["IDSA OPAT Guidelines"],
        burden_holder="OPAT team",
        adversary_position="All patients can be managed with OPAT.",
        counter_arguments=[
            "Inappropriate selection increases risk of complications.",
            "Close monitoring is essential for safety."
        ],
        resolution_strategy="Follow best practices and monitor outcomes.",
        entity_scope="Patients receiving IV antibiotics outside hospital.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IDSA Guidelines for OPAT"
    ),
    DoctrineBlock(
        topic="Antibiotic Allergy Assessment and De-labeling",
        keywords=["antibiotic allergy", "penicillin", "de-labeling", "assessment", "stewardship"],
        conclusion_template="Assess reported antibiotic allergies with history and testing; de-label when true allergy is unlikely.",
        reasoning_framework=(
            "1. Obtain detailed history of reported antibiotic allergy.\n"
            "2. Distinguish between true IgE-mediated allergy and adverse reactions.\n"
            "3. Consider skin testing for penicillin allergy.\n"
            "4. Remove allergy label if testing is negative or history inconsistent.\n"
            "5. Educate patient and update medical record."
        ),
        key_factors=["allergy history", "testing results", "reaction type", "patient education"],
        primary_authority=["IDSA Antibiotic Allergy Guidance", "AAAAI Position Statements"],
        burden_holder="Prescriber and allergy specialist",
        adversary_position="All reported allergies must be honored.",
        counter_arguments=[
            "Most reported allergies are not true allergies.",
            "De-labeling improves antibiotic choices and outcomes."
        ],
        resolution_strategy="Implement structured allergy assessment and testing.",
        entity_scope="All patients with reported antibiotic allergies.",
        confidence=0.94,
        confidence_zone="Moderate-High",
        controlling_precedent="IDSA Guidance on Antibiotic Allergy"
    ),
    DoctrineBlock(
        topic="Infective Endocarditis Prophylaxis",
        keywords=["endocarditis", "prophylaxis", "dental procedures", "high risk", "antibiotics"],
        conclusion_template="Provide endocarditis prophylaxis only for high-risk patients undergoing high-risk dental procedures.",
        reasoning_framework=(
            "1. Identify high-risk cardiac conditions (prosthetic valves, prior endocarditis, certain congenital heart diseases).\n"
            "2. Determine if procedure involves manipulation of gingival tissue or periapical region.\n"
            "3. Prescribe amoxicillin 2g orally 30-60 minutes before procedure (or alternative if allergic).\n"
            "4. Avoid routine prophylaxis for low-risk patients or procedures."
        ),
        key_factors=["cardiac risk", "procedure type", "antibiotic selection", "timing"],
        primary_authority=["AHA Endocarditis Prophylaxis Guidelines"],
        burden_holder="Dentist or proceduralist",
        adversary_position="Prophylaxis should be given to all patients.",
        counter_arguments=[
            "Prophylaxis benefits only high-risk groups.",
            "Overuse increases resistance and adverse events."
        ],
        resolution_strategy="Restrict prophylaxis to guideline-defined indications.",
        entity_scope="Patients with high-risk cardiac conditions.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AHA Guidelines for Endocarditis Prophylaxis"
    ),
    DoctrineBlock(
        topic="Management of Asymptomatic Bacteriuria",
        keywords=["asymptomatic bacteriuria", "screening", "treatment", "pregnancy", "catheter"],
        conclusion_template="Treat asymptomatic bacteriuria only in pregnancy and prior to urologic procedures.",
        reasoning_framework=(
            "1. Screen for bacteriuria in pregnant women and before urologic procedures with anticipated mucosal bleeding.\n"
            "2. Do not screen or treat non-pregnant, asymptomatic adults, including those with catheters.\n"
            "3. Treat with appropriate antibiotics if indicated.\n"
            "4. Avoid unnecessary antibiotics to reduce resistance."
        ),
        key_factors=["patient population", "pregnancy status", "procedure risk", "symptoms"],
        primary_authority=["IDSA Asymptomatic Bacteriuria Guidelines"],
        burden_holder="Clinician",
        adversary_position="All bacteriuria should be treated.",
        counter_arguments=[
            "Treatment outside indications offers no benefit.",
            "Increases adverse events and resistance."
        ],
        resolution_strategy="Restrict treatment to guideline indications.",
        entity_scope="Adults with asymptomatic bacteriuria.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IDSA Guidelines for Asymptomatic Bacteriuria"
    ),
    DoctrineBlock(
        topic="Screening and Management of Latent Tuberculosis Infection (LTBI)",
        keywords=["LTBI", "latent TB", "screening", "treatment", "INH", "rifampin"],
        conclusion_template="Screen high-risk individuals for LTBI and treat with INH or rifampin-based regimens.",
        reasoning_framework=(
            "1. Identify high-risk populations (close contacts, immunosuppressed, recent immigrants).\n"
            "2. Screen with tuberculin skin test (TST) or interferon-gamma release assay (IGRA).\n"
            "3. Exclude active TB with symptom review and chest imaging.\n"
            "4. Treat LTBI with INH for 6-9 months or rifampin-based short-course regimens.\n"
            "5. Monitor for adherence and hepatotoxicity."
        ),
        key_factors=["risk factors", "screening test", "treatment regimen", "toxicity monitoring"],
        primary_authority=["CDC LTBI Guidelines", "WHO LTBI Guidance"],
        burden_holder="Public health provider",
        adversary_position="LTBI treatment is unnecessary.",
        counter_arguments=[
            "LTBI treatment prevents progression to active TB.",
            "Short-course regimens improve adherence."
        ],
        resolution_strategy="Screen and treat per guidelines.",
        entity_scope="High-risk adults and children.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CDC Guidelines for LTBI"
    ),
    DoctrineBlock(
        topic="Management of Influenza in Hospitalized Patients",
        keywords=["influenza", "antivirals", "oseltamivir", "hospitalized", "treatment"],
        conclusion_template="Treat all hospitalized patients with confirmed or suspected influenza with neuraminidase inhibitors.",
        reasoning_framework=(
            "1. Test for influenza in hospitalized patients with compatible symptoms during flu season.\n"
            "2. Start oseltamivir as soon as possible, ideally within 48 hours, but benefit exists even if started later.\n"
            "3. Continue treatment for at least 5 days or longer if immunosuppressed.\n"
            "4. Implement droplet precautions to prevent nosocomial spread."
        ),
        key_factors=["timing of therapy", "diagnostic testing", "infection control", "immunosuppression"],
        primary_authority=["CDC Influenza Guidelines", "IDSA Influenza Guidance"],
        burden_holder="Hospitalist",
        adversary_position="Antivirals are only effective if started within 48 hours.",
        counter_arguments=[
            "Hospitalized patients benefit even with later initiation.",
            "Reduces complications and mortality."
        ],
        resolution_strategy="Treat all hospitalized patients regardless of symptom duration.",
        entity_scope="Hospitalized adults and children with influenza.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="CDC Guidelines for Influenza Management"
    ),
    DoctrineBlock(
        topic="Management of Community-Acquired Pneumonia (CAP)",
        keywords=["CAP", "community-acquired pneumonia", "antibiotics", "diagnosis", "severity"],
        conclusion_template="Diagnose CAP clinically and radiographically; treat with guideline-recommended empiric antibiotics based on severity.",
        reasoning_framework=(
            "1. Diagnose CAP based on symptoms (cough, fever, dyspnea) and chest imaging.\n"
            "2. Assess severity using CURB-65 or PSI to determine site of care.\n"
            "3. Outpatient: amoxicillin, doxycycline, or macrolide (if local resistance <25%).\n"
            "4. Inpatient: β-lactam plus macrolide or respiratory fluoroquinolone.\n"
            "5. Treat for 5 days minimum and reassess clinical stability."
        ),
        key_factors=["diagnosis", "severity assessment", "antibiotic selection", "treatment duration"],
        primary_authority=["IDSA/ATS CAP Guidelines"],
        burden_holder="Primary care or hospitalist",
        adversary_position="All CAP requires hospitalization and IV antibiotics.",
        counter_arguments=[
            "Most CAP can be managed outpatient.",
            "Oral therapy is effective for many patients."
        ],
        resolution_strategy="Risk stratify and treat per guidelines.",
        entity_scope="Adults with community-acquired pneumonia.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IDSA/ATS Guidelines for CAP"
    ),
    DoctrineBlock(
        topic="Management of Hospital-Acquired and Ventilator-Associated Pneumonia (HAP/VAP)",
        keywords=["HAP", "VAP", "hospital-acquired pneumonia", "ventilator-associated pneumonia", "antibiotics"],
        conclusion_template="Treat HAP/VAP with empiric antibiotics covering MRSA and Pseudomonas, tailored to local resistance patterns.",
        reasoning_framework=(
            "1. Diagnose HAP/VAP based on new infiltrate plus clinical features (fever, purulent secretions, leukocytosis).\n"
            "2. Start empiric therapy with anti-MRSA and anti-pseudomonal agents.\n"
            "3. Adjust regimen based on local antibiogram and risk factors.\n"
            "4. De-escalate therapy based on culture results and clinical response.\n"
            "5. Treat for 7 days unless complications."
        ),
        key_factors=["diagnosis", "local resistance", "antibiotic selection", "de-escalation"],
        primary_authority=["IDSA/ATS HAP/VAP Guidelines"],
        burden_holder="Hospitalist/ICU team",
        adversary_position="Narrow-spectrum therapy is sufficient for all cases.",
        counter_arguments=[
            "Broad empiric coverage reduces mortality.",
            "De-escalation minimizes resistance."
        ],
        resolution_strategy="Start broad, then narrow based on data.",
        entity_scope="Hospitalized patients with HAP/VAP.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IDSA/ATS Guidelines for HAP/VAP"
    ),
    DoctrineBlock(
        topic="Management of Acute Uncomplicated Cystitis in Women",
        keywords=["cystitis", "UTI", "women", "antibiotics", "uncomplicated"],
        conclusion_template="Treat acute uncomplicated cystitis in women with short-course oral antibiotics: nitrofurantoin, TMP-SMX, or fosfomycin.",
        reasoning_framework=(
            "1. Diagnose based on symptoms (dysuria, frequency, urgency) without complicating factors.\n"
            "2. Do not require urine culture for typical cases.\n"
            "3. First-line agents: nitrofurantoin (5 days), TMP-SMX (3 days), fosfomycin (single dose).\n"
            "4. Avoid fluoroquinolones due to adverse effects.\n"
            "5. Reserve cultures for recurrent or complicated cases."
        ),
        key_factors=["diagnosis", "antibiotic selection", "treatment duration", "complicating factors"],
        primary_authority=["IDSA UTI Guidelines"],
        burden_holder="Primary care provider",
        adversary_position="All UTIs require long courses and cultures.",
        counter_arguments=[
            "Short courses are effective.",
            "Cultures not needed for typical cases."
        ],
        resolution_strategy="Use short-course therapy per guidelines.",
        entity_scope="Non-pregnant women with uncomplicated cystitis.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IDSA Guidelines for Acute Cystitis"
    ),
    DoctrineBlock(
        topic="Management of Infective Endocarditis",
        keywords=["infective endocarditis", "diagnosis", "antibiotics", "surgery", "Duke criteria"],
        conclusion_template="Diagnose infective endocarditis with Duke criteria; treat with prolonged IV antibiotics and consider surgery for complications.",
        reasoning_framework=(
            "1. Suspect endocarditis in patients with fever and risk factors (prosthetic valve, IVDU).\n"
            "2. Use Duke criteria (major and minor) for diagnosis.\n"
            "3. Obtain multiple blood cultures before antibiotics.\n"
            "4. Treat with pathogen-directed IV antibiotics for 4-6 weeks.\n"
            "5. Refer for surgery if heart failure, uncontrolled infection, or embolic risk."
        ),
        key_factors=["diagnosis", "pathogen", "treatment duration", "surgical indications"],
        primary_authority=["AHA/IDSA Endocarditis Guidelines"],
        burden_holder="Infectious diseases specialist",
        adversary_position="Short oral therapy is sufficient.",
        counter_arguments=[
            "Prolonged IV therapy is standard of care.",
            "Surgery is lifesaving in select cases."
        ],
        resolution_strategy="Follow guideline-based therapy and multidisciplinary approach.",
        entity_scope="Adults with suspected or confirmed endocarditis.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AHA/IDSA Guidelines for Infective Endocarditis"
    ),
    DoctrineBlock(
        topic="Management of Meningitis in Adults",
        keywords=["meningitis", "bacterial", "antibiotics", "steroids", "diagnosis"],
        conclusion_template="Treat suspected bacterial meningitis with empiric IV antibiotics and adjunctive dexamethasone; tailor therapy by age and risk factors.",
        reasoning_framework=(
            "1. Recognize symptoms (fever, neck stiffness, altered mental status).\n"
            "2. Obtain blood cultures and lumbar puncture before antibiotics if safe.\n"
            "3. Start empiric therapy: vancomycin plus ceftriaxone (add ampicillin if >50 years or immunocompromised).\n"
            "4. Give dexamethasone before or with first antibiotic dose.\n"
            "5. Adjust therapy based on CSF and culture results."
        ),
        key_factors=["age", "risk factors", "timing of therapy", "adjunctive steroids"],
        primary_authority=["IDSA Meningitis Guidelines"],
        burden_holder="Hospitalist/ED provider",
        adversary_position="Steroids are unnecessary.",
        counter_arguments=[
            "Dexamethasone improves outcomes in pneumococcal meningitis.",
            "Early antibiotics are lifesaving."
        ],
        resolution_strategy="Empiric therapy with age/risk-based modifications.",
        entity_scope="Adults with suspected bacterial meningitis.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IDSA Guidelines for Bacterial Meningitis"
    ),
    DoctrineBlock(
        topic="Management of Clostridioides difficile Recurrence",
        keywords=["C. difficile", "recurrence", "treatment", "FMT", "vancomycin taper"],
        conclusion_template="Treat first recurrence with vancomycin or fidaxomicin; consider vancomycin taper or FMT for multiple recurrences.",
        reasoning_framework=(
            "1. Confirm recurrent C. difficile with compatible symptoms and positive test.\n"
            "2. For first recurrence, use vancomycin (standard or tapered) or fidaxomicin.\n"
            "3. For multiple recurrences, consider vancomycin taper or fecal microbiota transplantation (FMT).\n"
            "4. Avoid unnecessary antibiotics and maintain infection control."
        ),
        key_factors=["number of recurrences", "treatment history", "FMT availability", "infection control"],
        primary_authority=["IDSA/SHEA C. difficile Guidelines"],
        burden_holder="Treating clinician",
        adversary_position="Metronidazole is adequate for recurrences.",
        counter_arguments=[
            "Vancomycin and fidaxomicin are superior.",
            "FMT is highly effective for multiple recurrences."
        ],
        resolution_strategy="Escalate therapy per recurrence number and guidelines.",
        entity_scope="Adults with recurrent C. difficile infection.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IDSA/SHEA Guidelines for C. difficile"
    ),
    DoctrineBlock(
        topic="Management of Methicillin-Sensitive Staphylococcus aureus (MSSA) Bacteremia",
        keywords=["MSSA", "bacteremia", "antibiotics", "β-lactam", "treatment duration"],
        conclusion_template="Treat MSSA bacteremia with IV β-lactam antibiotics for at least 14 days; avoid vancomycin if susceptible.",
        reasoning_framework=(
            "1. Confirm MSSA by blood culture and susceptibility testing.\n"
            "2. Use IV nafcillin, oxacillin, or cefazolin as preferred agents.\n"
            "3. Treat uncomplicated cases for at least 14 days; longer for endocarditis or metastatic infection.\n"
            "4. Remove infected devices when possible.\n"
            "5. Avoid vancomycin if β-lactam susceptible."
        ),
        key_factors=["antibiotic selection", "treatment duration", "source control", "device removal"],
        primary_authority=["IDSA Staphylococcus aureus Bacteremia Guidelines"],
        burden_holder="Treating physician",
        adversary_position="Vancomycin is equally effective.",
        counter_arguments=[
            "β-lactams are superior to vancomycin for MSSA.",
            "Shorter therapy increases relapse risk."
        ],
        resolution_strategy="Use β-lactams and treat for guideline-recommended duration.",
        entity_scope="Adults with MSSA bacteremia.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IDSA Guidelines for S. aureus Bacteremia"
    ),
    DoctrineBlock(
        topic="Management of Neutropenic Fever in Hematologic Malignancy",
        keywords=["neutropenic fever", "hematologic malignancy", "empiric antibiotics", "Pseudomonas"],
        conclusion_template="Initiate empiric anti-pseudomonal β-lactam antibiotics immediately in neutropenic fever; add antifungals for persistent fever.",
        reasoning_framework=(
            "1. Define neutropenic fever as single temp ≥38.3°C or ≥38.0°C for 1 hour with ANC <500/μL.\n"
            "2. Start empiric IV anti-pseudomonal β-lactam (e.g., cefepime, meropenem) within 1 hour.\n"
            "3. Add vancomycin if concern for catheter infection, skin/soft tissue infection, or MRSA risk.\n"
            "4. Add antifungal therapy if fever persists >4-7 days without source.\n"
            "5. Monitor for complications and adjust therapy based on cultures."
        ),
        key_factors=["timing of antibiotics", "antibiotic selection", "fungal risk", "complications"],
        primary_authority=["IDSA Guidelines for Neutropenic Fever"],
        burden_holder="Oncology/hematology provider",
        adversary_position="Wait for cultures before starting antibiotics.",
        counter_arguments=[
            "Delays increase mortality.",
            "Empiric therapy is standard of care."
        ],
        resolution_strategy="Immediate empiric antibiotics with escalation as needed.",
        entity_scope="Patients with hematologic malignancy and neutropenic fever.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IDSA Guidelines for Neutropenic Fever"
    ),
    DoctrineBlock(
        topic="Management of HIV-Related Opportunistic Infections",
        keywords=["HIV", "opportunistic infections", "prophylaxis", "treatment", "CD4 count"],
        conclusion_template="Initiate prophylaxis and treat OIs based on CD4 count and clinical presentation; start ART after acute OI management.",
        reasoning_framework=(
            "1. Assess CD4 count and risk for specific OIs (e.g., PCP, Toxoplasma, MAC).\n"
            "2. Initiate prophylaxis when indicated (e.g., TMP-SMX for PCP if CD4 <200).\n"
            "3. Treat acute OIs with appropriate antimicrobials.\n"
            "4. Start ART after stabilization of acute OI (timing varies by OI).\n"
            "5. Monitor for IRIS and adjust management as needed."
        ),
        key_factors=["CD4 count", "OI risk", "timing of ART", "prophylaxis"],
        primary_authority=["DHHS HIV Guidelines", "CDC OI Guidelines"],
        burden_holder="HIV care provider",
        adversary_position="Start ART immediately in all cases.",
        counter_arguments=[
            "Delayed ART initiation reduces IRIS risk in some OIs.",
            "Prophylaxis prevents OI morbidity and mortality."
        ],
        resolution_strategy="Individualize ART timing and OI management.",
        entity_scope="HIV-infected patients with OIs.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="DHHS Guidelines for OI Management"
    ),
    DoctrineBlock(
        topic="Management of COVID-19 in Hospitalized Patients",
        keywords=["COVID-19", "SARS-CoV-2", "hospitalized", "dexamethasone", "remdesivir"],
        conclusion_template="Treat hospitalized COVID-19 patients requiring oxygen with dexamethasone; consider remdesivir and supportive care.",
        reasoning_framework=(
            "1. Confirm COVID-19 diagnosis with PCR or antigen testing.\n"
            "2. Assess severity and oxygen requirement.\n"
            "3. Start dexamethasone (6 mg daily for up to 10 days) if requiring supplemental oxygen.\n"
            "4. Consider remdesivir for patients not on mechanical ventilation.\n"
            "5. Provide supportive care and monitor for complications."
        ),
        key_factors=["oxygen requirement", "timing of therapy", "drug selection", "complications"],
        primary_authority=["NIH COVID-19 Guidelines", "IDSA COVID-19 Guidance"],
        burden_holder="Hospitalist/ID specialist",
        adversary_position="Steroids are harmful in viral infections.",
        counter_arguments=[
            "RCTs show mortality benefit with dexamethasone.",
            "Remdesivir shortens recovery in select patients."
        ],
        resolution_strategy="Follow evolving guidelines and evidence.",
        entity_scope="Hospitalized adults with COVID-19.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NIH Guidelines for COVID-19 Treatment"
    ),
    DoctrineBlock(
        topic="Management of Acute Bacterial Skin and Soft Tissue Infections (SSTI)",
        keywords=["SSTI", "cellulitis", "abscess", "antibiotics", "incision and drainage"],
        conclusion_template="Treat uncomplicated cellulitis with oral antibiotics; perform incision and drainage for abscesses.",
        reasoning_framework=(
            "1. Diagnose SSTI based on clinical findings (erythema, warmth, swelling, pain).\n"
            "2. For abscesses, perform incision and drainage as primary therapy.\n"
            "3. Use oral antibiotics for non-purulent cellulitis (e.g., cephalexin, dicloxacillin).\n"
            "4. Cover MRSA if risk factors present.\n"
            "5. Hospitalize for severe or rapidly progressive infections."
        ),
        key_factors=["SSTI type", "abscess presence", "antibiotic selection", "MRSA risk"],
        primary_authority=["IDSA SSTI Guidelines"],
        burden_holder="Primary care or ED provider",
        adversary_position="All SSTIs require IV antibiotics.",
        counter_arguments=[
            "Oral therapy is effective for most cases.",
            "I&D is definitive for abscesses."
        ],
        resolution_strategy="Individualize therapy based on severity and risk factors.",
        entity_scope="Adults and children with SSTI.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IDSA Guidelines for SSTI"
    ),
    DoctrineBlock(
        topic="Management of Tick-Borne Diseases (Lyme, Anaplasmosis, Babesiosis)",
        keywords=["tick-borne", "Lyme", "anaplasmosis", "babesiosis", "treatment"],
        conclusion_template="Treat Lyme disease with doxycycline; use atovaquone plus azithromycin for babesiosis.",
        reasoning_framework=(
            "1. Diagnose tick-borne diseases based on clinical features and epidemiology.\n"
            "2. For Lyme disease, treat with doxycycline (10-21 days depending on stage).\n"
            "3. For anaplasmosis, use doxycycline for 10 days.\n"
            "4. For babesiosis, use atovaquone plus azithromycin for 7-10 days.\n"
            "5. Monitor for complications and coinfections."
        ),
        key_factors=["disease type", "clinical features", "antibiotic selection", "duration"],
        primary_authority=["CDC Tick-Borne Disease Guidelines"],
        burden_holder="Primary care or ID provider",
        adversary_position="Empiric therapy is unnecessary without laboratory confirmation.",
        counter_arguments=[
            "Early therapy prevents complications.",
            "Diagnosis is often clinical."
        ],
        resolution_strategy="Treat based on clinical suspicion and epidemiology.",
        entity_scope="Patients with suspected tick-borne disease.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CDC Guidelines for Tick-Borne Diseases"
    ),
    DoctrineBlock(
        topic="Management of Hepatitis B Reactivation in Immunosuppressed Patients",
        keywords=["hepatitis B", "reactivation", "immunosuppression", "antiviral prophylaxis"],
        conclusion_template="Screen for hepatitis B before immunosuppression; start antiviral prophylaxis if at risk for reactivation.",
        reasoning_framework=(
            "1. Screen for HBsAg, anti-HBc, and anti-HBs before starting immunosuppressive therapy.\n"
            "2. Assess risk based on serology and planned immunosuppression.\n"
            "3. Start antiviral prophylaxis (e.g., entecavir, tenofovir) for high-risk patients.\n"
            "4. Monitor HBV DNA and liver function during and after therapy.\n"
            "5. Continue prophylaxis for at least 6 months after immunosuppression ends."
        ),
        key_factors=["HBV serology", "immunosuppression type", "antiviral selection", "monitoring"],
        primary_authority=["AASLD HBV Guidelines", "CDC Recommendations"],
        burden_holder="Prescribing physician",
        adversary_position="Prophylaxis is unnecessary without active infection.",
        counter_arguments=[
            "Reactivation can cause severe hepatitis.",
            "Prophylaxis is safe and effective."
        ],
        resolution_strategy="Screen and prophylax per guidelines.",
        entity_scope="Patients undergoing immunosuppression.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AASLD Guidelines for HBV Reactivation"
    ),
    DoctrineBlock(
        topic="Management of Acute HIV Infection",
        keywords=["acute HIV", "diagnosis", "ART", "transmission", "seroconversion"],
        conclusion_template="Diagnose acute HIV with antigen/antibody and RNA testing; initiate ART immediately to reduce transmission and preserve immunity.",
        reasoning_framework=(
            "1. Suspect acute HIV in patients with recent high-risk exposure and flu-like illness.\n"
            "2. Use 4th generation antigen/antibody and HIV RNA testing for diagnosis.\n"
            "3. Counsel patient on transmission risk and importance of early ART.\n"
            "4. Initiate integrase inhibitor-based ART as soon as possible.\n"
            "5. Monitor for seroconversion and ART response."
        ),
        key_factors=["diagnostic testing", "timing of ART", "transmission risk", "counseling"],
        primary_authority=["DHHS HIV Guidelines"],
        burden_holder="HIV care provider",
        adversary_position="Delay ART until confirmatory testing.",
        counter_arguments=[
            "Early ART reduces viral set point and transmission.",
            "Diagnosis can be made with current assays."
        ],
        resolution_strategy="Start ART immediately after diagnosis.",
        entity_scope="Patients with acute HIV infection.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="DHHS Guidelines for Acute HIV"
    ),
    DoctrineBlock(
        topic="Management of Herpes Simplex Virus (HSV) Encephalitis",
        keywords=["HSV", "encephalitis", "acyclovir", "diagnosis", "PCR"],
        conclusion_template="Treat suspected HSV encephalitis with empiric IV acyclovir pending PCR confirmation.",
        reasoning_framework=(
            "1. Suspect HSV encephalitis in patients with acute encephalopathy, fever, and temporal lobe findings.\n"
            "2. Obtain CSF for PCR testing.\n"
            "3. Start empiric IV acyclovir (10 mg/kg q8h) immediately.\n"
            "4. Continue therapy for 14-21 days if confirmed.\n"
            "5. Monitor for renal toxicity and adjust dose for renal impairment."
        ),
        key_factors=["clinical suspicion", "PCR testing", "timing of therapy", "renal function"],
        primary_authority=["IDSA Encephalitis Guidelines"],
        burden_holder="Hospitalist/neurologist",
        adversary_position="Wait for PCR results before starting therapy.",
        counter_arguments=[
            "Delays increase morbidity and mortality.",
            "Empiric therapy is low risk."
        ],
        resolution_strategy="Start empiric acyclovir for all suspected cases.",
        entity_scope="Adults and children with suspected HSV encephalitis.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IDSA Guidelines for Encephalitis"
    ),
    DoctrineBlock(
        topic="Prevention of Surgical Antimicrobial Prophylaxis-Related Adverse Events",
        keywords=["surgical prophylaxis", "adverse events", "antibiotic selection", "timing", "duration"],
        conclusion_template="Limit surgical antimicrobial prophylaxis to a single preoperative dose to minimize adverse events and resistance.",
        reasoning_framework=(
            "1. Select prophylactic antibiotic based on procedure and patient allergies.\n"
            "2. Administer within 60 minutes before incision.\n"
            "3. Do not continue prophylaxis beyond 24 hours postoperatively.\n"
            "4. Monitor for allergic reactions and C. difficile infection."
        ),
        key_factors=["antibiotic selection", "timing", "duration", "adverse event monitoring"],
        primary_authority=["CDC SSI Guidelines", "IDSA Surgical Prophylaxis Guidance"],
        burden_holder="Surgical team",
        adversary_position="Prolonged prophylaxis reduces SSI risk.",
        counter_arguments=[
            "Prolonged use increases adverse events and resistance.",
            "Single dose is effective for most procedures."
        ],
        resolution_strategy="Restrict prophylaxis to recommended timing and duration.",
        entity_scope="All surgical patients.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="CDC Guidelines for SSI Prevention"
    ),
    DoctrineBlock(
        topic="Management of Multidrug-Resistant Gram-Negative Infections",
        keywords=["multidrug-resistant", "gram-negative", "antibiotics", "novel agents", "susceptibility"],
        conclusion_template="Treat MDR gram-negative infections with novel β-lactam/β-lactamase inhibitors guided by susceptibility testing.",
        reasoning_framework=(
            "1. Identify MDR gram-negative organisms by susceptibility testing.\n"
            "2. Use novel agents (ceftazidime-avibactam, meropenem-vaborbactam, imipenem-relebactam) if susceptible.\n"
            "3. Avoid older, more toxic agents (colistin, aminoglycosides) if alternatives exist.\n"
            "4. Consult infectious diseases for complex cases.\n"
            "5. Monitor for resistance emergence and adverse events."
        ),
        key_factors=["susceptibility results", "antibiotic selection", "toxicity risk", "ID consultation"],
        primary_authority=["IDSA Guidance on Gram-Negative Infections"],
        burden_holder="Treating physician",
        adversary_position="Older agents are adequate and less costly.",
        counter_arguments=[
            "Novel agents are more effective and safer.",
            "Toxicity of older agents is significant."
        ],
        resolution_strategy="Use novel agents when available and indicated.",
        entity_scope="Hospitalized patients with MDR gram-negative infections.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IDSA Guidance on MDR Gram-Negative Infections"
    ),
    DoctrineBlock(
        topic="Prevention of Occupational Exposure to Bloodborne Pathogens",
        keywords=["occupational exposure", "bloodborne pathogens", "needle stick", "post-exposure prophylaxis", "PPE"],
        conclusion_template="Prevent occupational exposure with PPE, safe needle practices, and prompt post-exposure management.",
        reasoning_framework=(
            "1. Use gloves, gowns, masks, and eye protection as indicated.\n"
            "2. Avoid recapping needles and dispose in sharps containers.\n"
            "3. Wash exposed area immediately after exposure.\n"
            "4. Report exposure and seek evaluation for post-exposure prophylaxis (PEP).\n"
            "5. Follow up for serologic testing and counseling."
        ),
        key_factors=["PPE use", "safe practices", "PEP protocols", "reporting"],
        primary_authority=["CDC Bloodborne Pathogen Standards", "OSHA"],
        burden_holder="Healthcare worker and employer",
        adversary_position="PPE is unnecessary for routine care.",
        counter_arguments=[
            "PPE and safe practices prevent transmission.",
            "Prompt PEP reduces infection risk."
        ],
        resolution_strategy="Strict adherence to exposure prevention protocols.",
        entity_scope="All healthcare settings.",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="CDC/OSHA Bloodborne Pathogen Standards"
    ),
    DoctrineBlock(
        topic="Management of Viral Hepatitis C Infection",
        keywords=["hepatitis C", "HCV", "DAA", "treatment", "screening"],
        conclusion_template="Treat all chronic HCV infections with direct-acting antivirals (DAAs) after confirming genotype and fibrosis stage.",
        reasoning_framework=(
            "1. Screen all adults for HCV at least once.\n"
            "2. Confirm chronic infection with HCV RNA testing.\n"
            "3. Assess genotype and liver fibrosis (e.g., FibroScan).\n"
            "4. Initiate DAA therapy (e.g., sofosbuvir/velpatasvir) for 8-12 weeks.\n"
            "5. Monitor for cure (SVR12) and manage comorbidities."
        ),
        key_factors=["HCV RNA", "genotype", "fibrosis stage", "DAA selection"],
        primary_authority=["AASLD/IDSA HCV Guidelines"],
        burden_holder="Hepatologist/ID provider",
        adversary_position="Treatment is only for advanced liver disease.",
        counter_arguments=[
            "DAAs are safe, effective, and curative for most patients.",
            "Early treatment prevents complications and transmission."
        ],
        resolution_strategy="Treat all eligible patients with DAAs.",
        entity_scope="Adults with chronic HCV infection.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AASLD/IDSA Guidelines for HCV"
    ),
    DoctrineBlock(
        topic="Prevention of Healthcare-Associated Fungal Infections",
        keywords=["fungal infection", "HAI", "prevention", "immunosuppressed", "antifungal prophylaxis"],
        conclusion_template="Prevent healthcare-associated fungal infections with environmental controls and antifungal prophylaxis in high-risk patients.",
        reasoning_framework=(
            "1. Identify high-risk patients (e.g., neutropenia, transplant recipients).\n"
            "2. Implement HEPA filtration and minimize construction dust exposure.\n"
            "3. Use antifungal prophylaxis (e.g., fluconazole, posaconazole) in select populations.\n"
            "4. Monitor for breakthrough infections and adjust prophylaxis as needed."
        ),
        key_factors=["patient risk", "environmental controls", "prophylaxis selection", "monitoring"],
        primary_authority=["CDC Fungal Infection Guidelines", "IDSA Prophylaxis Guidance"],
        burden_holder="Infection prevention team",
        adversary_position="Fungal infections are rare and not preventable.",
        counter_arguments=[
            "Prophylaxis reduces morbidity and mortality.",
            "Environmental controls are effective."
        ],
        resolution_strategy="Target prevention to high-risk groups.",
        entity_scope="Immunosuppressed and high-risk hospitalized patients.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CDC Guidelines for Fungal Infection Prevention"
    ),
    DoctrineBlock(
        topic="Management of Non-Tuberculous Mycobacterial (NTM) Pulmonary Disease",
        keywords=["NTM", "pulmonary disease", "mycobacteria", "treatment", "macrolide"],
        conclusion_template="Treat NTM pulmonary disease with macrolide-based multidrug regimens guided by susceptibility testing.",
        reasoning_framework=(
            "1. Diagnose NTM pulmonary disease with clinical, radiographic, and microbiologic criteria.\n"
            "2. Identify NTM species and perform susceptibility testing.\n"
            "3. Use macrolide-based regimens (e.g., azithromycin, ethambutol, rifampin) for MAC.\n"
            "4. Treat for at least 12 months after culture conversion.\n"
            "5. Monitor for drug toxicity and response."
        ),
        key_factors=["NTM species", "susceptibility", "treatment duration", "toxicity monitoring"],
        primary_authority=["ATS/IDSA NTM Guidelines"],
        burden_holder="Pulmonologist/ID provider",
        adversary_position="Short-course therapy is sufficient.",
        counter_arguments=[
            "Prolonged multidrug therapy is required for cure.",
            "Short courses lead to relapse."
        ],
        resolution_strategy="Follow guideline-based regimens and monitoring.",
        entity_scope="Adults with NTM pulmonary disease.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ATS/IDSA Guidelines for NTM"
    ),
    DoctrineBlock(
        topic="Prevention of Perioperative Surgical Site Infections",
        keywords=["SSI", "prevention", "perioperative", "antibiotics", "skin prep"],
        conclusion_template="Prevent perioperative SSI with appropriate antibiotics, skin antisepsis, and glycemic control.",
        reasoning_framework=(
            "1. Administer prophylactic antibiotics within 60 minutes before incision.\n"
            "2. Prep skin with alcohol-based chlorhexidine.\n"
            "3. Maintain perioperative normothermia and glycemic control.\n"
            "4. Minimize operating room traffic and maintain sterile technique."
        ),
        key_factors=["antibiotic timing", "skin prep", "glycemic control", "sterile technique"],
        primary_authority=["CDC SSI Guidelines", "WHO Surgical Safety Checklist"],
        burden_holder="Surgical team",
        adversary_position="SSI rates are unaffected by prevention measures.",
        counter_arguments=[
            "Bundles reduce SSI rates.",
            "Multimodal prevention is most effective."
        ],
        resolution_strategy="Strict adherence to SSI prevention bundle.",
        entity_scope="All surgical patients.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="CDC Guidelines for SSI Prevention"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(query: str) -> List[DoctrineBlock]:
    results = []
    q = query.lower()
    for doctrine in DOCTRINE_CACHE:
        if (
            q in doctrine.topic.lower()
            or any(q in kw.lower() for kw in doctrine.keywords)
            or q in doctrine.reasoning_framework.lower()
            or q in doctrine.conclusion_template.lower()
        ):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]