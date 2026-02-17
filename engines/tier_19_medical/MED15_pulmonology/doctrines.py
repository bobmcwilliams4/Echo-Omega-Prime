from dataclasses import dataclass
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
        topic="Spirometry Interpretation - Obstructive Pattern",
        keywords=["spirometry", "obstructive", "FEV1", "FVC", "FEV1/FVC", "COPD", "asthma"],
        conclusion_template="Obstructive pattern is present if FEV1/FVC ratio is below the lower limit of normal.",
        reasoning_framework="""
1. Review spirometry results, focusing on FEV1, FVC, and FEV1/FVC ratio.
2. Compare FEV1/FVC ratio to reference values (lower limit of normal, typically <0.70 for adults).
3. Assess reversibility with bronchodilator challenge.
4. Consider clinical context (symptoms, risk factors).
5. Differentiate between asthma and COPD based on age, smoking history, reversibility, and symptom pattern.
6. Exclude confounding factors such as poor effort or technical errors.
7. Document findings and correlate with clinical diagnosis.
8. Use GOLD or ATS/ERS guidelines for interpretation.
9. If obstruction is confirmed, grade severity based on FEV1 % predicted.
10. Re-evaluate if results are inconsistent with clinical picture.
""",
        key_factors=["FEV1/FVC ratio", "FEV1 % predicted", "bronchodilator response", "clinical context", "reference values"],
        primary_authority=["ATS/ERS Spirometry Guidelines", "GOLD Report", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Obstructive pattern may be due to technical error or restrictive disease.",
        counter_arguments=[
            "Restrictive disease can also reduce FEV1/FVC if FVC is disproportionately reduced.",
            "Poor patient effort may mimic obstruction.",
            "Mixed patterns may confound interpretation."
        ],
        resolution_strategy="Repeat spirometry with coaching, use full PFTs to clarify pattern, correlate with clinical findings.",
        entity_scope="adult and pediatric patients undergoing spirometry",
        confidence=0.97,
        confidence_zone="high",
        controlling_precedent="ATS/ERS 2019 Spirometry Standard"
    ),
    DoctrineBlock(
        topic="Diffusing Capacity (DLCO) Interpretation",
        keywords=["DLCO", "diffusing capacity", "lung function", "ILD", "emphysema", "anemia"],
        conclusion_template="Reduced DLCO indicates impaired gas exchange, commonly seen in interstitial lung disease, emphysema, or pulmonary vascular disease.",
        reasoning_framework="""
1. Review DLCO value and compare to predicted reference.
2. Assess clinical context: symptoms, risk factors, imaging.
3. Consider causes of reduced DLCO: parenchymal disease (ILD), emphysema, pulmonary hypertension, anemia.
4. Adjust for hemoglobin concentration if available.
5. Evaluate for isolated reduction (suggests vascular disease) vs. combined reduction (suggests parenchymal disease).
6. Consider increased DLCO in asthma, polycythemia, or alveolar hemorrhage.
7. Integrate with other PFTs: restrictive pattern with reduced DLCO suggests ILD; obstructive pattern with reduced DLCO suggests emphysema.
8. Document findings and correlate with clinical diagnosis.
9. Use ATS/ERS guidelines for interpretation.
10. Re-evaluate if results are inconsistent with clinical picture.
""",
        key_factors=["DLCO value", "hemoglobin adjustment", "clinical context", "other PFTs", "reference values"],
        primary_authority=["ATS/ERS Diffusing Capacity Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="DLCO reduction may be due to technical error or extrapulmonary causes.",
        counter_arguments=[
            "Anemia can falsely lower DLCO.",
            "Poor breath-hold technique may affect results.",
            "Cardiac output changes can influence DLCO."
        ],
        resolution_strategy="Repeat DLCO with hemoglobin adjustment, ensure proper technique, correlate with imaging and clinical findings.",
        entity_scope="patients undergoing pulmonary function testing",
        confidence=0.95,
        confidence_zone="high",
        controlling_precedent="ATS/ERS 2017 Diffusing Capacity Standard"
    ),
    DoctrineBlock(
        topic="Asthma Diagnosis and Phenotyping",
        keywords=["asthma", "phenotype", "spirometry", "bronchodilator", "allergy", "eosinophilia"],
        conclusion_template="Asthma diagnosis is based on reversible airway obstruction and compatible clinical history; phenotyping guides therapy.",
        reasoning_framework="""
1. Obtain detailed history: episodic symptoms, triggers, nocturnal symptoms, atopy.
2. Perform spirometry: look for reversible obstruction (FEV1 increase ≥12% and ≥200 mL post-bronchodilator).
3. Assess for alternative diagnoses (COPD, vocal cord dysfunction).
4. Evaluate for phenotypes: allergic, eosinophilic, non-eosinophilic, obesity-related, late-onset.
5. Use biomarkers: blood eosinophils, FeNO, IgE.
6. Consider allergy testing for atopic phenotype.
7. Integrate imaging and other tests as needed.
8. Document findings and classify phenotype.
9. Use GINA or NHLBI guidelines for diagnostic criteria.
10. Re-evaluate if response to therapy is atypical.
""",
        key_factors=["reversible obstruction", "clinical history", "phenotype markers", "spirometry", "biomarkers"],
        primary_authority=["GINA Guidelines", "NHLBI Asthma Guidelines", "American Academy of Allergy, Asthma & Immunology"],
        burden_holder="clinician",
        adversary_position="Symptoms may be due to other causes; phenotyping may not alter therapy.",
        counter_arguments=[
            "COPD can mimic asthma in older adults.",
            "Non-eosinophilic asthma may not respond to steroids.",
            "Overlap syndromes complicate diagnosis."
        ],
        resolution_strategy="Use comprehensive history, objective testing, and response to therapy to clarify diagnosis and phenotype.",
        entity_scope="patients with suspected asthma",
        confidence=0.96,
        confidence_zone="high",
        controlling_precedent="GINA 2023 Asthma Report"
    ),
    DoctrineBlock(
        topic="COPD Diagnosis and Severity Grading",
        keywords=["COPD", "spirometry", "GOLD", "FEV1", "smoking", "severity"],
        conclusion_template="COPD is diagnosed by persistent airflow limitation (FEV1/FVC <0.70) and graded by FEV1 % predicted.",
        reasoning_framework="""
1. Obtain history: chronic cough, sputum, dyspnea, risk factors (smoking, occupational exposure).
2. Perform spirometry: confirm persistent airflow limitation (post-bronchodilator FEV1/FVC <0.70).
3. Exclude asthma and other causes of obstruction.
4. Grade severity: GOLD 1 (FEV1 ≥80%), GOLD 2 (50-79%), GOLD 3 (30-49%), GOLD 4 (<30%).
5. Assess symptoms using CAT or mMRC.
6. Evaluate exacerbation history.
7. Integrate imaging (chest CT) if needed.
8. Document findings and assign GOLD stage.
9. Use GOLD guidelines for diagnosis and grading.
10. Re-evaluate if clinical picture is inconsistent.
""",
        key_factors=["FEV1/FVC ratio", "FEV1 % predicted", "symptom assessment", "exacerbation history", "risk factors"],
        primary_authority=["GOLD Report", "ATS/ERS COPD Guidelines"],
        burden_holder="clinician",
        adversary_position="Airflow limitation may be reversible or due to other causes.",
        counter_arguments=[
            "Asthma-COPD overlap complicates diagnosis.",
            "Spirometry may not reflect symptoms.",
            "Non-smoking related COPD exists."
        ],
        resolution_strategy="Use comprehensive history, objective testing, and guideline-based grading.",
        entity_scope="patients with suspected COPD",
        confidence=0.97,
        confidence_zone="high",
        controlling_precedent="GOLD 2023 COPD Report"
    ),
    DoctrineBlock(
        topic="Interstitial Lung Disease (ILD) Diagnostic Approach",
        keywords=["ILD", "interstitial", "HRCT", "lung biopsy", "autoimmune", "fibrosis"],
        conclusion_template="ILD diagnosis requires integration of clinical, radiologic, and histopathologic data.",
        reasoning_framework="""
1. Obtain detailed history: exposures, autoimmune symptoms, family history.
2. Perform physical exam: crackles, clubbing, signs of connective tissue disease.
3. Order HRCT: look for patterns (UIP, NSIP, OP, LIP).
4. Exclude mimics: heart failure, infection, malignancy.
5. Consider serologic testing for autoimmune disease.
6. Multidisciplinary discussion (pulmonology, radiology, pathology).
7. Lung biopsy if diagnosis remains unclear.
8. Document findings and classify ILD subtype.
9. Use ATS/ERS guidelines for diagnostic criteria.
10. Re-evaluate if clinical course is atypical.
""",
        key_factors=["HRCT pattern", "clinical history", "serologic tests", "biopsy findings", "multidisciplinary input"],
        primary_authority=["ATS/ERS ILD Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Imaging and histology may be non-specific; biopsy risks.",
        counter_arguments=[
            "Overlap syndromes complicate diagnosis.",
            "HRCT may not distinguish all subtypes.",
            "Biopsy may not be feasible."
        ],
        resolution_strategy="Use multidisciplinary approach, integrate all available data, avoid unnecessary biopsy.",
        entity_scope="patients with suspected ILD",
        confidence=0.93,
        confidence_zone="moderate-high",
        controlling_precedent="ATS/ERS 2018 ILD Guideline"
    ),
    DoctrineBlock(
        topic="Pulmonary Hypertension Classification and Diagnosis",
        keywords=["pulmonary hypertension", "PAH", "right heart cath", "WHO group", "echo"],
        conclusion_template="Pulmonary hypertension is classified by WHO group and confirmed by right heart catheterization.",
        reasoning_framework="""
1. Obtain history: dyspnea, syncope, chest pain, risk factors (connective tissue disease, liver disease).
2. Perform physical exam: signs of right heart failure.
3. Order echocardiogram: estimate pulmonary pressures, assess RV function.
4. Exclude left heart disease, lung disease, chronic thromboembolism.
5. Confirm diagnosis with right heart catheterization (mean PAP ≥25 mmHg).
6. Classify by WHO group (1-5) based on etiology.
7. Consider additional testing: V/Q scan, PFTs, serology.
8. Document findings and assign classification.
9. Use ESC/ERS guidelines for diagnosis and classification.
10. Re-evaluate if clinical picture is inconsistent.
""",
        key_factors=["right heart cath", "WHO group", "echo findings", "clinical history", "exclusion of secondary causes"],
        primary_authority=["ESC/ERS Pulmonary Hypertension Guidelines", "American College of Cardiology"],
        burden_holder="clinician",
        adversary_position="Echocardiogram may overestimate pressures; secondary causes may confound diagnosis.",
        counter_arguments=[
            "Left heart disease is a common confounder.",
            "Chronic lung disease may mimic PAH.",
            "Non-invasive tests are not definitive."
        ],
        resolution_strategy="Use right heart catheterization for confirmation, comprehensive workup for classification.",
        entity_scope="patients with suspected pulmonary hypertension",
        confidence=0.95,
        confidence_zone="high",
        controlling_precedent="ESC/ERS 2022 PH Guideline"
    ),
    DoctrineBlock(
        topic="Sleep Apnea Diagnosis and Therapy",
        keywords=["sleep apnea", "OSA", "polysomnography", "CPAP", "AHI", "snoring"],
        conclusion_template="Obstructive sleep apnea is diagnosed by polysomnography (AHI ≥5) and treated with CPAP or alternative therapies.",
        reasoning_framework="""
1. Obtain history: snoring, witnessed apneas, daytime sleepiness, comorbidities.
2. Screen with questionnaires (Epworth, STOP-BANG).
3. Order polysomnography: measure AHI, oxygen desaturation, sleep architecture.
4. Classify severity: mild (AHI 5-15), moderate (15-30), severe (>30).
5. Evaluate for central sleep apnea if indicated.
6. Assess for comorbidities (obesity, hypertension, heart failure).
7. Initiate CPAP therapy; consider alternatives (oral appliance, surgery) if CPAP intolerant.
8. Document findings and therapy response.
9. Use AASM guidelines for diagnosis and management.
10. Re-evaluate if symptoms persist.
""",
        key_factors=["AHI", "polysomnography", "clinical history", "CPAP response", "comorbidities"],
        primary_authority=["AASM Sleep Apnea Guidelines", "American Academy of Sleep Medicine"],
        burden_holder="clinician",
        adversary_position="Symptoms may be due to other sleep disorders; CPAP intolerance.",
        counter_arguments=[
            "Insomnia or restless legs may mimic OSA.",
            "CPAP adherence is often poor.",
            "Alternative therapies may be less effective."
        ],
        resolution_strategy="Use objective testing, patient education, and tailored therapy.",
        entity_scope="patients with suspected sleep apnea",
        confidence=0.94,
        confidence_zone="high",
        controlling_precedent="AASM 2021 OSA Guideline"
    ),
    DoctrineBlock(
        topic="Mechanical Ventilation: Modes and Initial Settings",
        keywords=["mechanical ventilation", "modes", "settings", "ARDS", "tidal volume", "PEEP"],
        conclusion_template="Initial mechanical ventilation settings should prioritize lung protection: low tidal volume, appropriate PEEP, and mode selection based on patient needs.",
        reasoning_framework="""
1. Assess indication for mechanical ventilation: hypoxemia, hypercapnia, airway protection.
2. Choose mode: volume-controlled, pressure-controlled, or spontaneous.
3. Set tidal volume: 6-8 mL/kg predicted body weight (lower for ARDS).
4. Set PEEP: start at 5 cm H2O, titrate based on oxygenation and compliance.
5. Set FiO2: start at 100%, titrate down to maintain SpO2 >92%.
6. Set respiratory rate: based on pCO2 and patient comfort.
7. Monitor plateau pressure: keep <30 cm H2O.
8. Assess for patient-ventilator synchrony.
9. Reassess settings frequently and adjust as needed.
10. Use ARDSnet or ATS guidelines for lung protection.
""",
        key_factors=["tidal volume", "PEEP", "FiO2", "mode", "plateau pressure"],
        primary_authority=["ARDSnet Protocol", "ATS Mechanical Ventilation Guidelines"],
        burden_holder="clinician",
        adversary_position="Higher tidal volumes may improve comfort; low PEEP may risk hypoxemia.",
        counter_arguments=[
            "Patient-specific factors may require deviation.",
            "ARDS may require higher PEEP.",
            "Spontaneous modes may be preferable in some cases."
        ],
        resolution_strategy="Individualize settings, prioritize lung protection, monitor closely.",
        entity_scope="critically ill patients requiring mechanical ventilation",
        confidence=0.98,
        confidence_zone="very high",
        controlling_precedent="ARDSnet 2000 Protocol"
    ),
    DoctrineBlock(
        topic="Pleural Effusion Analysis and Light's Criteria",
        keywords=["pleural effusion", "Light's criteria", "transudate", "exudate", "thoracentesis"],
        conclusion_template="Light's criteria distinguish exudative from transudative pleural effusions based on protein and LDH ratios.",
        reasoning_framework="""
1. Obtain history: heart failure, infection, malignancy, liver disease.
2. Perform thoracentesis: analyze pleural fluid for protein, LDH, cell count, pH, glucose.
3. Apply Light's criteria:
   - Pleural fluid protein/serum protein >0.5
   - Pleural fluid LDH/serum LDH >0.6
   - Pleural fluid LDH >2/3 upper limit of normal serum LDH
4. If any criterion is met, effusion is exudative.
5. Consider alternative causes if criteria are borderline.
6. Integrate clinical context and imaging.
7. Document findings and guide management.
8. Use ATS guidelines for pleural disease.
9. Re-evaluate if diagnosis is unclear.
""",
        key_factors=["protein ratio", "LDH ratio", "clinical context", "thoracentesis", "imaging"],
        primary_authority=["ATS Pleural Disease Guidelines", "Light's Criteria Original Publication"],
        burden_holder="clinician",
        adversary_position="Light's criteria may misclassify effusions in diuretic-treated patients.",
        counter_arguments=[
            "Diuretics can concentrate protein/LDH.",
            "Borderline values require clinical judgment.",
            "Alternative tests (cholesterol, albumin gradient) may help."
        ],
        resolution_strategy="Use clinical context, repeat testing if needed, consider additional markers.",
        entity_scope="patients with pleural effusion",
        confidence=0.96,
        confidence_zone="high",
        controlling_precedent="Light RW, NEJM 1972"
    ),
    DoctrineBlock(
        topic="Lung Cancer Screening and Staging",
        keywords=["lung cancer", "screening", "LDCT", "staging", "TNM", "smoking"],
        conclusion_template="Lung cancer screening is recommended for high-risk individuals using LDCT; staging uses TNM system.",
        reasoning_framework="""
1. Identify high-risk individuals: age 50-80, ≥20 pack-years, current/former smokers.
2. Recommend annual low-dose CT (LDCT) for screening.
3. If nodule is detected, assess size, characteristics, and risk factors.
4. Use TNM system for staging: T (tumor size), N (nodal involvement), M (metastasis).
5. Order PET-CT, brain MRI, and mediastinal sampling as indicated.
6. Multidisciplinary discussion for management.
7. Document findings and assign stage.
8. Use NCCN or ATS guidelines for screening and staging.
9. Re-evaluate if clinical picture changes.
""",
        key_factors=["LDCT", "TNM staging", "risk factors", "multidisciplinary input", "imaging"],
        primary_authority=["NCCN Lung Cancer Guidelines", "ATS Lung Cancer Screening Guidelines"],
        burden_holder="clinician",
        adversary_position="Screening may lead to overdiagnosis; staging may miss micrometastases.",
        counter_arguments=[
            "False positives may lead to unnecessary procedures.",
            "TNM staging may underestimate disease.",
            "Screening may not reduce mortality in low-risk groups."
        ],
        resolution_strategy="Use guideline-based screening, multidisciplinary staging, and shared decision-making.",
        entity_scope="high-risk individuals and patients with lung cancer",
        confidence=0.95,
        confidence_zone="high",
        controlling_precedent="NCCN 2023 Lung Cancer Guideline"
    ),
    DoctrineBlock(
        topic="Acute Exacerbation of COPD (AECOPD) Management",
        keywords=["AECOPD", "COPD", "exacerbation", "steroids", "antibiotics", "oxygen"],
        conclusion_template="AECOPD is managed with bronchodilators, steroids, antibiotics if indicated, and oxygen therapy.",
        reasoning_framework="""
1. Assess severity: increased dyspnea, cough, sputum, hypoxemia.
2. Initiate short-acting bronchodilators.
3. Start systemic steroids (prednisone 40 mg daily x5 days).
4. Consider antibiotics if sputum purulence or increased volume.
5. Provide supplemental oxygen to maintain SpO2 88-92%.
6. Monitor for respiratory failure; consider noninvasive ventilation.
7. Evaluate for underlying triggers (infection, heart failure).
8. Document response and adjust therapy.
9. Use GOLD guidelines for management.
10. Re-evaluate if no improvement.
""",
        key_factors=["bronchodilator response", "steroid therapy", "antibiotic indication", "oxygen saturation", "severity assessment"],
        primary_authority=["GOLD Report", "ATS/ERS COPD Guidelines"],
        burden_holder="clinician",
        adversary_position="Antibiotics may be overused; steroids have side effects.",
        counter_arguments=[
            "Viral exacerbations do not require antibiotics.",
            "Steroid overuse increases complications.",
            "Oxygen therapy may worsen hypercapnia."
        ],
        resolution_strategy="Use guideline-based criteria for therapy, monitor closely, individualize treatment.",
        entity_scope="patients with COPD exacerbation",
        confidence=0.97,
        confidence_zone="high",
        controlling_precedent="GOLD 2023 COPD Report"
    ),
    DoctrineBlock(
        topic="Bronchiectasis Diagnosis and Management",
        keywords=["bronchiectasis", "HRCT", "chronic cough", "sputum", "antibiotics"],
        conclusion_template="Bronchiectasis is diagnosed by HRCT showing airway dilation and managed with airway clearance and antibiotics.",
        reasoning_framework="""
1. Obtain history: chronic cough, sputum, recurrent infections.
2. Perform physical exam: crackles, wheezing.
3. Order HRCT: look for airway dilation, wall thickening, lack of tapering.
4. Exclude mimics: COPD, asthma, cystic fibrosis.
5. Assess for underlying causes: immunodeficiency, infection, autoimmune disease.
6. Initiate airway clearance techniques (chest physiotherapy).
7. Use antibiotics for exacerbations or chronic infection.
8. Consider inhaled therapies for symptom control.
9. Document findings and therapy response.
10. Use BTS or ATS guidelines for management.
""",
        key_factors=["HRCT findings", "airway clearance", "antibiotic therapy", "underlying causes", "symptom assessment"],
        primary_authority=["BTS Bronchiectasis Guidelines", "ATS Bronchiectasis Guidelines"],
        burden_holder="clinician",
        adversary_position="HRCT may not distinguish bronchiectasis from other diseases; chronic antibiotics risk resistance.",
        counter_arguments=[
            "COPD and asthma may mimic bronchiectasis.",
            "Long-term antibiotics increase resistance.",
            "Airway clearance may not be effective in all patients."
        ],
        resolution_strategy="Use comprehensive evaluation, guideline-based therapy, monitor for complications.",
        entity_scope="patients with bronchiectasis",
        confidence=0.94,
        confidence_zone="high",
        controlling_precedent="BTS 2019 Bronchiectasis Guideline"
    ),
    DoctrineBlock(
        topic="Pulmonary Embolism Diagnosis and Risk Stratification",
        keywords=["pulmonary embolism", "PE", "CTPA", "D-dimer", "risk stratification", "Wells score"],
        conclusion_template="PE diagnosis is based on clinical probability, D-dimer, and imaging; risk stratification guides therapy.",
        reasoning_framework="""
1. Assess clinical probability using Wells score or Geneva score.
2. If low/intermediate probability, order D-dimer.
3. If D-dimer positive or high probability, order CTPA or V/Q scan.
4. Confirm diagnosis with imaging.
5. Stratify risk: hemodynamic stability, RV dysfunction, troponin.
6. Initiate anticoagulation if PE confirmed.
7. Consider thrombolysis for high-risk (massive) PE.
8. Document findings and risk category.
9. Use ESC or ACCP guidelines for diagnosis and management.
10. Re-evaluate if clinical picture changes.
""",
        key_factors=["clinical probability", "D-dimer", "imaging", "risk stratification", "anticoagulation"],
        primary_authority=["ESC PE Guidelines", "ACCP PE Guidelines"],
        burden_holder="clinician",
        adversary_position="D-dimer may be falsely elevated; imaging may miss small emboli.",
        counter_arguments=[
            "D-dimer is non-specific in hospitalized patients.",
            "CTPA may miss subsegmental PE.",
            "Anticoagulation risks bleeding."
        ],
        resolution_strategy="Use guideline-based algorithms, individualize therapy, monitor for complications.",
        entity_scope="patients with suspected PE",
        confidence=0.96,
        confidence_zone="high",
        controlling_precedent="ESC 2019 PE Guideline"
    ),
    DoctrineBlock(
        topic="Sarcoidosis Diagnosis and Treatment",
        keywords=["sarcoidosis", "granuloma", "biopsy", "ACE", "steroids", "multisystem"],
        conclusion_template="Sarcoidosis is diagnosed by compatible clinical, radiologic, and histopathologic findings; steroids are first-line therapy.",
        reasoning_framework="""
1. Obtain history: multisystem symptoms, cough, dyspnea, skin, eye involvement.
2. Perform physical exam: lymphadenopathy, skin lesions.
3. Order imaging: chest X-ray, HRCT for hilar/mediastinal lymphadenopathy.
4. Obtain biopsy: non-caseating granulomas.
5. Exclude mimics: TB, fungal infection, lymphoma.
6. Assess organ involvement: eyes, heart, CNS.
7. Initiate steroids for symptomatic or organ-threatening disease.
8. Consider steroid-sparing agents if needed.
9. Document findings and therapy response.
10. Use ATS guidelines for diagnosis and management.
""",
        key_factors=["biopsy findings", "imaging", "clinical history", "organ involvement", "steroid therapy"],
        primary_authority=["ATS Sarcoidosis Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Granulomas may be due to other causes; steroids have side effects.",
        counter_arguments=[
            "TB and fungal infections can mimic sarcoidosis.",
            "Steroid therapy risks metabolic complications.",
            "Biopsy may not be feasible."
        ],
        resolution_strategy="Use comprehensive evaluation, exclude mimics, individualize therapy.",
        entity_scope="patients with suspected sarcoidosis",
        confidence=0.93,
        confidence_zone="moderate-high",
        controlling_precedent="ATS 2020 Sarcoidosis Guideline"
    ),
    DoctrineBlock(
        topic="Pneumonia Severity Assessment and Antibiotic Selection",
        keywords=["pneumonia", "severity", "CURB-65", "PSI", "antibiotics", "CAP"],
        conclusion_template="Pneumonia severity is assessed with CURB-65 or PSI; antibiotic selection is based on risk factors and local resistance.",
        reasoning_framework="""
1. Assess severity using CURB-65 or PSI score.
2. Determine site of care: outpatient, inpatient, ICU.
3. Obtain history: comorbidities, risk factors for resistant organisms.
4. Choose empiric antibiotics based on guidelines and local resistance.
5. Adjust therapy based on microbiology and clinical response.
6. Monitor for complications: sepsis, respiratory failure.
7. Document findings and therapy response.
8. Use ATS/IDSA guidelines for management.
9. Re-evaluate if no improvement.
""",
        key_factors=["severity score", "site of care", "antibiotic selection", "risk factors", "clinical response"],
        primary_authority=["ATS/IDSA Pneumonia Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Severity scores may not capture all risk; empiric antibiotics risk resistance.",
        counter_arguments=[
            "Severity scores may underestimate risk in elderly.",
            "Empiric therapy may miss atypical pathogens.",
            "Antibiotic overuse increases resistance."
        ],
        resolution_strategy="Use guideline-based assessment, tailor antibiotics, monitor closely.",
        entity_scope="patients with pneumonia",
        confidence=0.95,
        confidence_zone="high",
        controlling_precedent="ATS/IDSA 2019 CAP Guideline"
    ),
    DoctrineBlock(
        topic="Chronic Cough Evaluation",
        keywords=["chronic cough", "evaluation", "asthma", "GERD", "postnasal drip", "ACE inhibitor"],
        conclusion_template="Chronic cough evaluation requires systematic assessment of common causes and targeted therapy.",
        reasoning_framework="""
1. Obtain history: duration, triggers, associated symptoms.
2. Exclude ACE inhibitor use.
3. Assess for asthma, GERD, postnasal drip (upper airway cough syndrome).
4. Perform spirometry and chest imaging.
5. Trial therapy for common causes.
6. Refer to specialist if cough persists.
7. Document findings and therapy response.
8. Use ACCP guidelines for evaluation.
9. Re-evaluate if no improvement.
""",
        key_factors=["history", "common causes", "spirometry", "imaging", "trial therapy"],
        primary_authority=["ACCP Chronic Cough Guidelines", "American College of Chest Physicians"],
        burden_holder="clinician",
        adversary_position="Cough may be due to rare causes; empiric therapy may not be effective.",
        counter_arguments=[
            "Rare causes (ILD, malignancy) may be missed.",
            "Empiric therapy may delay diagnosis.",
            "Patient compliance may be poor."
        ],
        resolution_strategy="Use systematic evaluation, escalate to specialist as needed.",
        entity_scope="patients with chronic cough",
        confidence=0.92,
        confidence_zone="moderate-high",
        controlling_precedent="ACCP 2006 Chronic Cough Guideline"
    ),
    DoctrineBlock(
        topic="Oxygen Therapy Prescription and Monitoring",
        keywords=["oxygen therapy", "prescription", "monitoring", "hypoxemia", "pulse oximetry"],
        conclusion_template="Oxygen therapy is prescribed to maintain SpO2 >88% and monitored for efficacy and safety.",
        reasoning_framework="""
1. Assess indication: hypoxemia (SpO2 <88%, PaO2 <55 mmHg).
2. Choose delivery device: nasal cannula, mask, high-flow.
3. Set flow rate to achieve target saturation.
4. Monitor SpO2 and clinical response.
5. Adjust therapy based on activity, sleep, and comorbidities.
6. Educate patient on device use and safety.
7. Document prescription and monitoring plan.
8. Use ATS guidelines for oxygen therapy.
9. Re-evaluate if clinical status changes.
""",
        key_factors=["indication", "delivery device", "flow rate", "monitoring", "patient education"],
        primary_authority=["ATS Oxygen Therapy Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Oxygen may worsen hypercapnia in COPD; overuse risks toxicity.",
        counter_arguments=[
            "COPD patients risk CO2 retention.",
            "Long-term oxygen therapy may not improve outcomes in mild hypoxemia.",
            "Device misuse may cause complications."
        ],
        resolution_strategy="Use guideline-based prescription, monitor closely, educate patient.",
        entity_scope="patients requiring oxygen therapy",
        confidence=0.96,
        confidence_zone="high",
        controlling_precedent="ATS 2020 Oxygen Therapy Guideline"
    ),
    DoctrineBlock(
        topic="Pulmonary Nodule Biopsy Techniques",
        keywords=["pulmonary nodule", "biopsy", "CT-guided", "bronchoscopy", "transthoracic", "diagnosis"],
        conclusion_template="Biopsy technique selection depends on nodule size, location, and patient risk factors.",
        reasoning_framework="""
1. Assess nodule characteristics: size, location, risk of malignancy.
2. Choose technique: CT-guided transthoracic, bronchoscopic, or surgical.
3. Consider patient comorbidities and risk of complications.
4. Use imaging to guide biopsy.
5. Document findings and complications.
6. Use multidisciplinary discussion for technique selection.
7. Use ATS guidelines for nodule management.
8. Re-evaluate if diagnosis remains unclear.
""",
        key_factors=["nodule size", "location", "biopsy technique", "patient risk", "imaging"],
        primary_authority=["ATS Pulmonary Nodule Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Biopsy risks complications; technique may not yield diagnosis.",
        counter_arguments=[
            "Small or deep nodules may be inaccessible.",
            "Complications include pneumothorax, bleeding.",
            "Non-diagnostic biopsies may require repeat."
        ],
        resolution_strategy="Use multidisciplinary approach, weigh risks and benefits, consider alternative diagnostic strategies.",
        entity_scope="patients with pulmonary nodules",
        confidence=0.93,
        confidence_zone="moderate-high",
        controlling_precedent="ATS 2013 Nodule Guideline"
    ),
    DoctrineBlock(
        topic="Restrictive Lung Disease PFT Pattern",
        keywords=["restrictive", "PFT", "spirometry", "TLC", "ILD", "neuromuscular"],
        conclusion_template="Restrictive pattern is defined by reduced TLC; spirometry alone is insufficient.",
        reasoning_framework="""
1. Review spirometry: reduced FVC, normal or increased FEV1/FVC.
2. Confirm restriction with lung volumes: TLC <80% predicted.
3. Assess clinical context: ILD, chest wall, neuromuscular disease.
4. Exclude pseudo-restriction (poor effort, obesity).
5. Document findings and correlate with clinical diagnosis.
6. Use ATS/ERS guidelines for interpretation.
7. Re-evaluate if results are inconsistent.
""",
        key_factors=["TLC", "spirometry", "clinical context", "exclusion of pseudo-restriction", "reference values"],
        primary_authority=["ATS/ERS PFT Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Spirometry may misclassify restriction; TLC measurement required.",
        counter_arguments=[
            "Obesity may cause pseudo-restriction.",
            "Poor effort may mimic restriction.",
            "Mixed patterns may confound interpretation."
        ],
        resolution_strategy="Use full PFTs, correlate with clinical findings, repeat testing if needed.",
        entity_scope="patients with suspected restrictive lung disease",
        confidence=0.95,
        confidence_zone="high",
        controlling_precedent="ATS/ERS 2019 PFT Standard"
    ),
    DoctrineBlock(
        topic="Hemoptysis Evaluation",
        keywords=["hemoptysis", "evaluation", "bronchoscopy", "CT", "infection", "malignancy"],
        conclusion_template="Hemoptysis evaluation prioritizes airway protection, identification of cause, and urgent intervention if massive.",
        reasoning_framework="""
1. Assess severity: volume, frequency, hemodynamic stability.
2. Secure airway if massive hemoptysis.
3. Obtain history: infection, malignancy, vascular disease.
4. Perform physical exam: signs of bleeding, underlying disease.
5. Order imaging: chest X-ray, CT, bronchoscopy.
6. Identify source and cause.
7. Initiate therapy: antibiotics, embolization, surgery as indicated.
8. Document findings and response.
9. Use ACCP guidelines for evaluation.
10. Re-evaluate if bleeding persists.
""",
        key_factors=["severity", "airway protection", "imaging", "bronchoscopy", "cause identification"],
        primary_authority=["ACCP Hemoptysis Guidelines", "American College of Chest Physicians"],
        burden_holder="clinician",
        adversary_position="Source may be unidentified; interventions risk complications.",
        counter_arguments=[
            "Bleeding source may be inaccessible.",
            "Bronchoscopy may not localize bleeding.",
            "Interventions may worsen bleeding."
        ],
        resolution_strategy="Use systematic evaluation, escalate to intervention as needed, monitor closely.",
        entity_scope="patients with hemoptysis",
        confidence=0.94,
        confidence_zone="high",
        controlling_precedent="ACCP 2007 Hemoptysis Guideline"
    ),
    # Additional doctrines for comprehensive coverage
    DoctrineBlock(
        topic="Pulmonary Rehabilitation in Chronic Respiratory Disease",
        keywords=["pulmonary rehabilitation", "chronic respiratory disease", "exercise", "education", "COPD"],
        conclusion_template="Pulmonary rehabilitation improves symptoms, exercise tolerance, and quality of life in chronic respiratory disease.",
        reasoning_framework="""
1. Assess indication: COPD, ILD, bronchiectasis, post-COVID.
2. Refer to multidisciplinary pulmonary rehab program.
3. Include exercise training, education, nutrition, psychosocial support.
4. Monitor outcomes: dyspnea, exercise tolerance, quality of life.
5. Adjust program based on patient needs.
6. Use ATS/ERS guidelines for rehabilitation.
7. Document participation and outcomes.
8. Re-evaluate if symptoms persist.
""",
        key_factors=["indication", "exercise training", "education", "outcomes", "multidisciplinary input"],
        primary_authority=["ATS/ERS Pulmonary Rehabilitation Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Access to rehabilitation may be limited; benefits may vary.",
        counter_arguments=[
            "Not all patients benefit equally.",
            "Program access may be limited.",
            "Adherence may be poor."
        ],
        resolution_strategy="Individualize program, address barriers, monitor outcomes.",
        entity_scope="patients with chronic respiratory disease",
        confidence=0.92,
        confidence_zone="moderate-high",
        controlling_precedent="ATS/ERS 2015 Pulmonary Rehabilitation Guideline"
    ),
    DoctrineBlock(
        topic="Idiopathic Pulmonary Fibrosis (IPF) Diagnosis and Management",
        keywords=["IPF", "idiopathic pulmonary fibrosis", "HRCT", "antifibrotic", "UIP"],
        conclusion_template="IPF is diagnosed by HRCT showing UIP pattern and managed with antifibrotic therapy.",
        reasoning_framework="""
1. Obtain history: chronic cough, dyspnea, risk factors.
2. Perform physical exam: crackles, clubbing.
3. Order HRCT: look for UIP pattern (subpleural, basal, honeycombing).
4. Exclude secondary causes: autoimmune, environmental exposure.
5. Multidisciplinary discussion for diagnosis.
6. Initiate antifibrotic therapy (pirfenidone, nintedanib).
7. Monitor for disease progression and side effects.
8. Document findings and therapy response.
9. Use ATS/ERS guidelines for diagnosis and management.
10. Re-evaluate if clinical course is atypical.
""",
        key_factors=["HRCT pattern", "antifibrotic therapy", "exclusion of secondary causes", "multidisciplinary input", "monitoring"],
        primary_authority=["ATS/ERS IPF Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="HRCT may not distinguish IPF from other ILDs; antifibrotics have side effects.",
        counter_arguments=[
            "Other ILDs may mimic UIP pattern.",
            "Antifibrotic therapy risks GI and liver toxicity.",
            "Biopsy may be required in atypical cases."
        ],
        resolution_strategy="Use multidisciplinary approach, guideline-based therapy, monitor closely.",
        entity_scope="patients with suspected IPF",
        confidence=0.93,
        confidence_zone="moderate-high",
        controlling_precedent="ATS/ERS 2018 IPF Guideline"
    ),
    DoctrineBlock(
        topic="Noninvasive Ventilation (NIV) in Acute Respiratory Failure",
        keywords=["NIV", "noninvasive ventilation", "acute respiratory failure", "COPD", "hypercapnia"],
        conclusion_template="NIV is indicated for acute hypercapnic respiratory failure, especially in COPD exacerbations.",
        reasoning_framework="""
1. Assess indication: acute respiratory failure with hypercapnia, COPD exacerbation, cardiogenic pulmonary edema.
2. Initiate NIV (BiPAP or CPAP) with appropriate settings.
3. Monitor for improvement: pCO2, pH, respiratory rate, comfort.
4. Exclude contraindications: altered mental status, inability to protect airway, hemodynamic instability.
5. Adjust settings based on response.
6. Document findings and therapy response.
7. Use ATS/ERS guidelines for NIV.
8. Re-evaluate if no improvement.
""",
        key_factors=["indication", "settings", "monitoring", "contraindications", "response"],
        primary_authority=["ATS/ERS NIV Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="NIV may delay intubation; contraindications limit use.",
        counter_arguments=[
            "Delayed intubation increases mortality.",
            "Patient tolerance may be poor.",
            "NIV may not be effective in all cases."
        ],
        resolution_strategy="Use guideline-based criteria, monitor closely, escalate to invasive ventilation if needed.",
        entity_scope="patients with acute respiratory failure",
        confidence=0.95,
        confidence_zone="high",
        controlling_precedent="ATS/ERS 2017 NIV Guideline"
    ),
    DoctrineBlock(
        topic="Pulmonary Function Testing Quality Assurance",
        keywords=["PFT", "quality assurance", "spirometry", "calibration", "ATS"],
        conclusion_template="PFT quality assurance requires regular calibration, technician training, and adherence to ATS/ERS standards.",
        reasoning_framework="""
1. Calibrate equipment daily according to manufacturer and ATS/ERS guidelines.
2. Train technicians in proper technique and patient coaching.
3. Monitor for acceptability and reproducibility criteria.
4. Review results for technical errors.
5. Document calibration and quality checks.
6. Use ATS/ERS standards for quality assurance.
7. Re-evaluate if results are inconsistent.
""",
        key_factors=["calibration", "technician training", "acceptability criteria", "documentation", "standards"],
        primary_authority=["ATS/ERS PFT Standards", "American Thoracic Society"],
        burden_holder="lab personnel",
        adversary_position="Quality lapses may affect results; standards may be difficult to maintain.",
        counter_arguments=[
            "Patient factors may affect reproducibility.",
            "Equipment malfunction may go unnoticed.",
            "Technician turnover affects quality."
        ],
        resolution_strategy="Regular training, strict adherence to standards, frequent audits.",
        entity_scope="PFT laboratories",
        confidence=0.97,
        confidence_zone="high",
        controlling_precedent="ATS/ERS 2019 PFT Standard"
    ),
    DoctrineBlock(
        topic="Alpha-1 Antitrypsin Deficiency Screening in COPD",
        keywords=["alpha-1 antitrypsin", "COPD", "screening", "genetic", "emphysema"],
        conclusion_template="All COPD patients should be screened for alpha-1 antitrypsin deficiency at least once.",
        reasoning_framework="""
1. Identify COPD patients, especially with early onset, minimal smoking, or family history.
2. Order alpha-1 antitrypsin level and genotype.
3. Refer to genetics if deficiency detected.
4. Consider augmentation therapy for severe deficiency.
5. Document screening and results.
6. Use ATS/ERS guidelines for screening.
7. Re-evaluate if clinical picture changes.
""",
        key_factors=["COPD diagnosis", "screening", "genotype", "augmentation therapy", "documentation"],
        primary_authority=["ATS/ERS Alpha-1 Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Screening may not alter therapy in mild deficiency.",
        counter_arguments=[
            "Augmentation therapy is costly.",
            "Genotype may not correlate with phenotype.",
            "Screening may not be cost-effective in all populations."
        ],
        resolution_strategy="Screen all COPD patients, individualize therapy, monitor outcomes.",
        entity_scope="COPD patients",
        confidence=0.94,
        confidence_zone="high",
        controlling_precedent="ATS/ERS 2016 Alpha-1 Guideline"
    ),
    DoctrineBlock(
        topic="Pulmonary Vasodilator Therapy in PAH",
        keywords=["pulmonary vasodilator", "PAH", "therapy", "prostacyclin", "endothelin", "phosphodiesterase"],
        conclusion_template="Pulmonary vasodilator therapy is indicated for WHO Group 1 PAH and tailored based on risk stratification.",
        reasoning_framework="""
1. Confirm diagnosis of WHO Group 1 PAH with right heart catheterization.
2. Stratify risk: low, intermediate, high.
3. Initiate therapy: endothelin receptor antagonists, phosphodiesterase inhibitors, prostacyclin analogs.
4. Monitor for efficacy and side effects.
5. Adjust therapy based on response and risk.
6. Document therapy and outcomes.
7. Use ESC/ERS guidelines for PAH management.
8. Re-evaluate if clinical status changes.
""",
        key_factors=["PAH diagnosis", "risk stratification", "therapy selection", "monitoring", "side effects"],
        primary_authority=["ESC/ERS PAH Guidelines", "American College of Cardiology"],
        burden_holder="clinician",
        adversary_position="Therapy risks hypotension; not all patients respond.",
        counter_arguments=[
            "Side effects may limit therapy.",
            "Combination therapy increases complexity.",
            "Cost and access may be barriers."
        ],
        resolution_strategy="Individualize therapy, monitor closely, address barriers.",
        entity_scope="patients with PAH",
        confidence=0.95,
        confidence_zone="high",
        controlling_precedent="ESC/ERS 2022 PAH Guideline"
    ),
    DoctrineBlock(
        topic="Tuberculosis Diagnosis and Treatment",
        keywords=["tuberculosis", "TB", "diagnosis", "treatment", "sputum", "culture"],
        conclusion_template="TB diagnosis requires microbiologic confirmation; treatment uses multi-drug regimen for at least 6 months.",
        reasoning_framework="""
1. Obtain history: risk factors, symptoms, exposure.
2. Perform physical exam: signs of TB.
3. Order sputum AFB smear and culture.
4. Use nucleic acid amplification for rapid diagnosis.
5. Initiate empiric therapy if high suspicion.
6. Monitor for drug resistance.
7. Document diagnosis and therapy.
8. Use CDC and WHO guidelines for management.
9. Re-evaluate if response is inadequate.
""",
        key_factors=["microbiologic confirmation", "multi-drug therapy", "drug resistance", "monitoring", "documentation"],
        primary_authority=["CDC TB Guidelines", "WHO TB Guidelines"],
        burden_holder="clinician",
        adversary_position="Empiric therapy risks resistance; diagnosis may be delayed.",
        counter_arguments=[
            "Drug resistance complicates therapy.",
            "Culture may take weeks.",
            "Side effects may limit adherence."
        ],
        resolution_strategy="Use rapid diagnostics, guideline-based therapy, monitor closely.",
        entity_scope="patients with suspected or confirmed TB",
        confidence=0.93,
        confidence_zone="moderate-high",
        controlling_precedent="CDC 2022 TB Guideline"
    ),
    DoctrineBlock(
        topic="Lung Transplantation Candidate Evaluation",
        keywords=["lung transplantation", "candidate", "evaluation", "end-stage", "criteria"],
        conclusion_template="Lung transplantation candidate evaluation requires assessment of disease severity, comorbidities, and psychosocial factors.",
        reasoning_framework="""
1. Identify end-stage lung disease: COPD, IPF, cystic fibrosis, PAH.
2. Assess disease severity and prognosis.
3. Evaluate comorbidities and contraindications.
4. Assess psychosocial support and adherence.
5. Refer to transplant center for multidisciplinary evaluation.
6. Document findings and eligibility.
7. Use ISHLT guidelines for candidate selection.
8. Re-evaluate if clinical status changes.
""",
        key_factors=["disease severity", "comorbidities", "psychosocial factors", "multidisciplinary input", "eligibility"],
        primary_authority=["ISHLT Lung Transplant Guidelines", "International Society for Heart and Lung Transplantation"],
        burden_holder="transplant center",
        adversary_position="Comorbidities may preclude transplantation; psychosocial factors limit eligibility.",
        counter_arguments=[
            "Limited donor availability.",
            "Contraindications may change over time.",
            "Adherence may be poor."
        ],
        resolution_strategy="Comprehensive evaluation, regular reassessment, address barriers.",
        entity_scope="patients with end-stage lung disease",
        confidence=0.91,
        confidence_zone="moderate-high",
        controlling_precedent="ISHLT 2020 Lung Transplant Guideline"
    ),
    DoctrineBlock(
        topic="Antifungal Therapy in Pulmonary Aspergillosis",
        keywords=["antifungal", "aspergillosis", "therapy", "voriconazole", "diagnosis"],
        conclusion_template="Antifungal therapy is indicated for invasive pulmonary aspergillosis and tailored based on severity and resistance.",
        reasoning_framework="""
1. Confirm diagnosis: clinical, radiologic, microbiologic evidence.
2. Initiate antifungal therapy: voriconazole first-line.
3. Monitor for efficacy and side effects.
4. Adjust therapy based on resistance and severity.
5. Document therapy and outcomes.
6. Use IDSA guidelines for management.
7. Re-evaluate if clinical status changes.
""",
        key_factors=["diagnosis", "therapy selection", "monitoring", "resistance", "side effects"],
        primary_authority=["IDSA Aspergillosis Guidelines", "Infectious Diseases Society of America"],
        burden_holder="clinician",
        adversary_position="Therapy risks toxicity; resistance may limit efficacy.",
        counter_arguments=[
            "Side effects may limit therapy.",
            "Resistance complicates management.",
            "Diagnosis may be delayed."
        ],
        resolution_strategy="Use guideline-based therapy, monitor closely, address resistance.",
        entity_scope="patients with pulmonary aspergillosis",
        confidence=0.92,
        confidence_zone="moderate-high",
        controlling_precedent="IDSA 2016 Aspergillosis Guideline"
    ),
    DoctrineBlock(
        topic="Pulmonary Artery Catheter Use in Critical Care",
        keywords=["pulmonary artery catheter", "critical care", "hemodynamics", "monitoring"],
        conclusion_template="Pulmonary artery catheter use is reserved for complex hemodynamic assessment in select critically ill patients.",
        reasoning_framework="""
1. Assess indication: shock, complex hemodynamics, unclear volume status.
2. Weigh risks and benefits.
3. Insert catheter with sterile technique.
4. Monitor pressures and cardiac output.
5. Adjust therapy based on data.
6. Document findings and outcomes.
7. Use SCCM and ATS guidelines for use.
8. Re-evaluate if clinical status changes.
""",
        key_factors=["indication", "risk-benefit", "monitoring", "therapy adjustment", "documentation"],
        primary_authority=["SCCM Pulmonary Artery Catheter Guidelines", "American Thoracic Society"],
        burden_holder="critical care team",
        adversary_position="Catheter risks complications; benefit may be limited.",
        counter_arguments=[
            "Infection and thrombosis risks.",
            "Data may not alter therapy.",
            "Noninvasive monitoring may suffice."
        ],
        resolution_strategy="Use strict criteria, monitor closely, remove catheter promptly.",
        entity_scope="critically ill patients",
        confidence=0.90,
        confidence_zone="moderate",
        controlling_precedent="SCCM 2017 Pulmonary Artery Catheter Guideline"
    ),
    DoctrineBlock(
        topic="Smoking Cessation in Pulmonary Disease",
        keywords=["smoking cessation", "pulmonary disease", "COPD", "asthma", "therapy"],
        conclusion_template="Smoking cessation is the most effective intervention for preventing and managing pulmonary disease.",
        reasoning_framework="""
1. Assess smoking status in all patients.
2. Offer counseling and pharmacotherapy (nicotine replacement, bupropion, varenicline).
3. Monitor for relapse and provide ongoing support.
4. Document cessation attempts and outcomes.
5. Use guideline-based interventions.
6. Re-evaluate at each visit.
""",
        key_factors=["smoking status", "counseling", "pharmacotherapy", "monitoring", "documentation"],
        primary_authority=["CDC Smoking Cessation Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Relapse rates are high; therapy may not be effective.",
        counter_arguments=[
            "Patient motivation varies.",
            "Pharmacotherapy risks side effects.",
            "Socioeconomic factors affect success."
        ],
        resolution_strategy="Use comprehensive approach, tailor interventions, monitor outcomes.",
        entity_scope="patients with pulmonary disease",
        confidence=0.97,
        confidence_zone="high",
        controlling_precedent="CDC 2022 Smoking Cessation Guideline"
    ),
    DoctrineBlock(
        topic="Immunosuppressive Therapy in Connective Tissue Disease-Associated ILD",
        keywords=["immunosuppressive therapy", "connective tissue disease", "ILD", "management"],
        conclusion_template="Immunosuppressive therapy is indicated for progressive CTD-ILD and tailored based on disease severity and organ involvement.",
        reasoning_framework="""
1. Confirm diagnosis of CTD-ILD.
2. Assess disease severity and organ involvement.
3. Initiate immunosuppressive therapy: steroids, mycophenolate, azathioprine.
4. Monitor for efficacy and side effects.
5. Adjust therapy based on response.
6. Document therapy and outcomes.
7. Use ATS/ERS guidelines for management.
8. Re-evaluate if clinical status changes.
""",
        key_factors=["diagnosis", "therapy selection", "monitoring", "side effects", "organ involvement"],
        primary_authority=["ATS/ERS CTD-ILD Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Therapy risks infection; efficacy may be limited.",
        counter_arguments=[
            "Side effects may limit therapy.",
            "Disease may progress despite therapy.",
            "Diagnosis may be delayed."
        ],
        resolution_strategy="Use guideline-based therapy, monitor closely, adjust as needed.",
        entity_scope="patients with CTD-ILD",
        confidence=0.93,
        confidence_zone="moderate-high",
        controlling_precedent="ATS/ERS 2020 CTD-ILD Guideline"
    ),
    DoctrineBlock(
        topic="Bronchoscopy Indications and Safety",
        keywords=["bronchoscopy", "indications", "safety", "diagnosis", "complications"],
        conclusion_template="Bronchoscopy is indicated for diagnosis and therapy in pulmonary disease; safety requires proper technique and monitoring.",
        reasoning_framework="""
1. Assess indication: diagnosis, therapy, airway management.
2. Review contraindications and patient risk factors.
3. Perform procedure with proper technique and sedation.
4. Monitor for complications: bleeding, pneumothorax, infection.
5. Document findings and outcomes.
6. Use ATS guidelines for bronchoscopy.
7. Re-evaluate if complications occur.
""",
        key_factors=["indication", "contraindications", "technique", "monitoring", "documentation"],
        primary_authority=["ATS Bronchoscopy Guidelines", "American Thoracic Society"],
        burden_holder="bronchoscopy team",
        adversary_position="Procedure risks complications; benefit may be limited.",
        counter_arguments=[
            "Complications may occur despite precautions.",
            "Procedure may not yield diagnosis.",
            "Patient tolerance may be poor."
        ],
        resolution_strategy="Use strict criteria, monitor closely, address complications promptly.",
        entity_scope="patients undergoing bronchoscopy",
        confidence=0.95,
        confidence_zone="high",
        controlling_precedent="ATS 2017 Bronchoscopy Guideline"
    ),
    DoctrineBlock(
        topic="Inhaled Corticosteroid Use in Asthma",
        keywords=["inhaled corticosteroid", "asthma", "therapy", "guidelines", "side effects"],
        conclusion_template="Inhaled corticosteroids are first-line therapy for persistent asthma, titrated to lowest effective dose.",
        reasoning_framework="""
1. Confirm diagnosis of persistent asthma.
2. Initiate inhaled corticosteroid at guideline-recommended dose.
3. Monitor for efficacy and side effects.
4. Adjust dose based on control and exacerbations.
5. Document therapy and outcomes.
6. Use GINA guidelines for management.
7. Re-evaluate at each visit.
""",
        key_factors=["diagnosis", "dose", "monitoring", "side effects", "adjustment"],
        primary_authority=["GINA Asthma Guidelines", "American Academy of Allergy, Asthma & Immunology"],
        burden_holder="clinician",
        adversary_position="Side effects may limit use; adherence may be poor.",
        counter_arguments=[
            "Patient adherence is variable.",
            "Side effects include oral thrush, dysphonia.",
            "Some phenotypes may not respond."
        ],
        resolution_strategy="Educate patient, monitor closely, adjust therapy as needed.",
        entity_scope="patients with asthma",
        confidence=0.97,
        confidence_zone="high",
        controlling_precedent="GINA 2023 Asthma Report"
    ),
    DoctrineBlock(
        topic="Antibiotic Stewardship in Respiratory Infections",
        keywords=["antibiotic stewardship", "respiratory infection", "CAP", "COPD", "resistance"],
        conclusion_template="Antibiotic stewardship requires appropriate selection, dosing, and duration to minimize resistance.",
        reasoning_framework="""
1. Confirm diagnosis of respiratory infection.
2. Assess risk factors for resistant organisms.
3. Choose empiric therapy based on guidelines and local resistance.
4. Adjust therapy based on microbiology and clinical response.
5. Limit duration to guideline recommendations.
6. Monitor for side effects and complications.
7. Document therapy and outcomes.
8. Use ATS/IDSA guidelines for stewardship.
9. Re-evaluate if clinical status changes.
""",
        key_factors=["diagnosis", "risk factors", "therapy selection", "duration", "monitoring"],
        primary_authority=["ATS/IDSA Antibiotic Stewardship Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Empiric therapy risks resistance; stewardship may limit options.",
        counter_arguments=[
            "Delayed therapy risks complications.",
            "Resistance may limit options.",
            "Patient factors may require deviation."
        ],
        resolution_strategy="Use guideline-based therapy, monitor closely, adjust as needed.",
        entity_scope="patients with respiratory infections",
        confidence=0.96,
        confidence_zone="high",
        controlling_precedent="ATS/IDSA 2019 Stewardship Guideline"
    ),
    DoctrineBlock(
        topic="Vaccination in Pulmonary Disease",
        keywords=["vaccination", "pulmonary disease", "influenza", "pneumococcal", "COVID-19"],
        conclusion_template="Vaccination reduces morbidity and mortality in pulmonary disease; annual influenza and pneumococcal vaccines are recommended.",
        reasoning_framework="""
1. Assess vaccination status in all patients with pulmonary disease.
2. Recommend annual influenza vaccine.
3. Recommend pneumococcal vaccine per guidelines.
4. Recommend COVID-19 vaccine as indicated.
5. Document vaccination and outcomes.
6. Use CDC and ATS guidelines for vaccination.
7. Re-evaluate at each visit.
""",
        key_factors=["vaccination status", "recommendation", "documentation", "outcomes", "guidelines"],
        primary_authority=["CDC Vaccination Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Vaccine hesitancy may limit uptake; efficacy may vary.",
        counter_arguments=[
            "Patient hesitancy is common.",
            "Efficacy may be reduced in immunocompromised.",
            "Side effects may limit use."
        ],
        resolution_strategy="Educate patient, monitor closely, address barriers.",
        entity_scope="patients with pulmonary disease",
        confidence=0.97,
        confidence_zone="high",
        controlling_precedent="CDC 2022 Vaccination Guideline"
    ),
    DoctrineBlock(
        topic="Pulmonary Nodule Surveillance",
        keywords=["pulmonary nodule", "surveillance", "LDCT", "follow-up", "malignancy"],
        conclusion_template="Pulmonary nodule surveillance uses risk-based follow-up intervals and imaging per guidelines.",
        reasoning_framework="""
1. Assess nodule size, characteristics, and risk factors.
2. Use guideline-based intervals for follow-up imaging.
3. Document findings and changes.
4. Refer to multidisciplinary team if risk increases.
5. Use ATS and Fleischner guidelines for surveillance.
6. Re-evaluate if nodule changes.
""",
        key_factors=["nodule size", "risk factors", "imaging interval", "documentation", "guidelines"],
        primary_authority=["ATS Pulmonary Nodule Guidelines", "Fleischner Society"],
        burden_holder="clinician",
        adversary_position="Surveillance may miss rapid progression; overuse risks radiation.",
        counter_arguments=[
            "Rapidly growing nodules may be missed.",
            "Radiation exposure increases with frequent imaging.",
            "Patient anxiety may increase."
        ],
        resolution_strategy="Use guideline-based intervals, monitor closely, address patient concerns.",
        entity_scope="patients with pulmonary nodules",
        confidence=0.95,
        confidence_zone="high",
        controlling_precedent="Fleischner 2017 Nodule Guideline"
    ),
    DoctrineBlock(
        topic="High-Resolution CT (HRCT) in ILD Diagnosis",
        keywords=["HRCT", "ILD", "diagnosis", "imaging", "pattern"],
        conclusion_template="HRCT is essential for ILD diagnosis and classification; patterns guide management.",
        reasoning_framework="""
1. Order HRCT for suspected ILD.
2. Assess for patterns: UIP, NSIP, OP, LIP.
3. Correlate imaging with clinical and histopathologic data.
4. Document findings and classification.
5. Use ATS/ERS guidelines for interpretation.
6. Re-evaluate if clinical course changes.
""",
        key_factors=["HRCT pattern", "clinical correlation", "documentation", "guidelines", "classification"],
        primary_authority=["ATS/ERS ILD Guidelines", "American Thoracic Society"],
        burden_holder="radiologist",
        adversary_position="Patterns may be non-specific; imaging may not distinguish all ILDs.",
        counter_arguments=[
            "Overlap syndromes complicate classification.",
            "Imaging may not be definitive.",
            "Biopsy may be required."
        ],
        resolution_strategy="Use multidisciplinary approach, integrate all data, avoid unnecessary biopsy.",
        entity_scope="patients with suspected ILD",
        confidence=0.94,
        confidence_zone="high",
        controlling_precedent="ATS/ERS 2018 ILD Guideline"
    ),
    DoctrineBlock(
        topic="Pulmonary Hypertension in Left Heart Disease",
        keywords=["pulmonary hypertension", "left heart disease", "group 2", "diagnosis", "management"],
        conclusion_template="Pulmonary hypertension due to left heart disease (Group 2) is managed by optimizing cardiac function; pulmonary vasodilators are not indicated.",
        reasoning_framework="""
1. Confirm diagnosis of left heart disease: heart failure, valvular disease.
2. Assess for pulmonary hypertension with echo and right heart cath.
3. Optimize cardiac function: diuretics, ACE inhibitors, beta-blockers.
4. Avoid pulmonary vasodilators unless indicated for other reasons.
5. Document findings and therapy.
6. Use ESC/ERS guidelines for management.
7. Re-evaluate if clinical status changes.
""",
        key_factors=["left heart disease", "pulmonary hypertension", "cardiac optimization", "documentation", "guidelines"],
        primary_authority=["ESC/ERS Pulmonary Hypertension Guidelines", "American College of Cardiology"],
        burden_holder="cardiology team",
        adversary_position="Pulmonary vasodilators may be used off-label; diagnosis may be unclear.",
        counter_arguments=[
            "Overlap with Group 1 PAH complicates management.",
            "Therapy may not improve outcomes.",
            "Diagnosis may be delayed."
        ],
        resolution_strategy="Use guideline-based management, optimize cardiac function, avoid off-label vasodilators.",
        entity_scope="patients with left heart disease and pulmonary hypertension",
        confidence=0.93,
        confidence_zone="moderate-high",
        controlling_precedent="ESC/ERS 2022 PH Guideline"
    ),
    DoctrineBlock(
        topic="Pulmonary Complications of Connective Tissue Disease",
        keywords=["pulmonary complications", "connective tissue disease", "ILD", "pulmonary hypertension"],
        conclusion_template="Connective tissue diseases may cause ILD, pulmonary hypertension, and pleural disease; early diagnosis improves outcomes.",
        reasoning_framework="""
1. Assess for pulmonary symptoms in CTD patients.
2. Order imaging and PFTs.
3. Screen for pulmonary hypertension.
4. Initiate therapy based on diagnosis.
5. Document findings and outcomes.
6. Use ATS/ERS guidelines for management.
7. Re-evaluate if clinical status changes.
""",
        key_factors=["CTD diagnosis", "pulmonary symptoms", "imaging", "PFTs", "therapy"],
        primary_authority=["ATS/ERS CTD Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Diagnosis may be delayed; therapy risks complications.",
        counter_arguments=[
            "Overlap syndromes complicate diagnosis.",
            "Therapy may not improve outcomes.",
            "Side effects may limit therapy."
        ],
        resolution_strategy="Use comprehensive evaluation, guideline-based therapy, monitor closely.",
        entity_scope="patients with CTD",
        confidence=0.92,
        confidence_zone="moderate-high",
        controlling_precedent="ATS/ERS 2020 CTD Guideline"
    ),
    DoctrineBlock(
        topic="Pulmonary Edema Evaluation and Management",
        keywords=["pulmonary edema", "evaluation", "management", "heart failure", "ARDS"],
        conclusion_template="Pulmonary edema evaluation distinguishes cardiogenic from non-cardiogenic causes; management is tailored accordingly.",
        reasoning_framework="""
1. Assess history: heart failure, ARDS, risk factors.
2. Perform physical exam: crackles, jugular venous distension.
3. Order imaging: chest X-ray, echo.
4. Distinguish cardiogenic from non-cardiogenic edema.
5. Initiate therapy: diuretics for cardiogenic, supportive for non-cardiogenic.
6. Document findings and outcomes.
7. Use ATS and ESC guidelines for management.
8. Re-evaluate if clinical status changes.
""",
        key_factors=["history", "imaging", "distinction", "therapy", "documentation"],
        primary_authority=["ATS Pulmonary Edema Guidelines", "ESC Heart Failure Guidelines"],
        burden_holder="clinician",
        adversary_position="Diagnosis may be unclear; therapy risks complications.",
        counter_arguments=[
            "Overlap syndromes complicate distinction.",
            "Diuretics may worsen renal function.",
            "Supportive therapy may not suffice."
        ],
        resolution_strategy="Use comprehensive evaluation, guideline-based therapy, monitor closely.",
        entity_scope="patients with pulmonary edema",
        confidence=0.93,
        confidence_zone="moderate-high",
        controlling_precedent="ATS 2017 Pulmonary Edema Guideline"
    ),
    DoctrineBlock(
        topic="Pulmonary Infection in Immunocompromised Hosts",
        keywords=["pulmonary infection", "immunocompromised", "diagnosis", "therapy", "fungal"],
        conclusion_template="Pulmonary infection in immunocompromised hosts requires broad differential, rapid diagnosis, and empiric therapy.",
        reasoning_framework="""
1. Assess immunocompromised status: HIV, transplant, chemotherapy.
2. Obtain history and physical exam.
3. Order imaging and microbiologic tests.
4. Initiate empiric therapy for bacterial, viral, and fungal pathogens.
5. Adjust therapy based on results.
6. Document findings and outcomes.
7. Use IDSA and ATS guidelines for management.
8. Re-evaluate if clinical status changes.
""",
        key_factors=["immunocompromised status", "diagnosis", "empiric therapy", "monitoring", "documentation"],
        primary_authority=["IDSA Immunocompromised Host Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Empiric therapy risks resistance; diagnosis may be delayed.",
        counter_arguments=[
            "Resistance complicates therapy.",
            "Diagnosis may be delayed.",
            "Side effects may limit therapy."
        ],
        resolution_strategy="Use broad empiric therapy, rapid diagnostics, monitor closely.",
        entity_scope="immunocompromised patients",
        confidence=0.92,
        confidence_zone="moderate-high",
        controlling_precedent="IDSA 2019 Immunocompromised Host Guideline"
    ),
    DoctrineBlock(
        topic="Pulmonary Rehabilitation Post-COVID",
        keywords=["pulmonary rehabilitation", "post-COVID", "exercise", "quality of life", "recovery"],
        conclusion_template="Pulmonary rehabilitation improves recovery and quality of life post-COVID.",
        reasoning_framework="""
1. Assess indication: post-COVID respiratory symptoms.
2. Refer to multidisciplinary pulmonary rehab program.
3. Include exercise training, education, nutrition, psychosocial support.
4. Monitor outcomes: dyspnea, exercise tolerance, quality of life.
5. Adjust program based on patient needs.
6. Document participation and outcomes.
7. Use ATS guidelines for rehabilitation.
8. Re-evaluate if symptoms persist.
""",
        key_factors=["indication", "exercise training", "education", "outcomes", "multidisciplinary input"],
        primary_authority=["ATS Pulmonary Rehabilitation Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Access to rehabilitation may be limited; benefits may vary.",
        counter_arguments=[
            "Not all patients benefit equally.",
            "Program access may be limited.",
            "Adherence may be poor."
        ],
        resolution_strategy="Individualize program, address barriers, monitor outcomes.",
        entity_scope="post-COVID patients",
        confidence=0.91,
        confidence_zone="moderate-high",
        controlling_precedent="ATS 2021 Pulmonary Rehabilitation Guideline"
    ),
    DoctrineBlock(
        topic="Pleural Disease in Connective Tissue Disorders",
        keywords=["pleural disease", "connective tissue disorder", "effusion", "diagnosis", "management"],
        conclusion_template="Pleural disease in CTD requires diagnosis of underlying disorder and tailored management.",
        reasoning_framework="""
1. Assess for pleural symptoms in CTD patients.
2. Order imaging and pleural fluid analysis.
3. Diagnose underlying CTD.
4. Initiate therapy based on diagnosis.
5. Document findings and outcomes.
6. Use ATS guidelines for management.
7. Re-evaluate if clinical status changes.
""",
        key_factors=["CTD diagnosis", "pleural symptoms", "imaging", "fluid analysis", "therapy"],
        primary_authority=["ATS Pleural Disease Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Diagnosis may be delayed; therapy risks complications.",
        counter_arguments=[
            "Overlap syndromes complicate diagnosis.",
            "Therapy may not improve outcomes.",
            "Side effects may limit therapy."
        ],
        resolution_strategy="Use comprehensive evaluation, guideline-based therapy, monitor closely.",
        entity_scope="patients with CTD and pleural disease",
        confidence=0.91,
        confidence_zone="moderate-high",
        controlling_precedent="ATS 2017 Pleural Disease Guideline"
    ),
    DoctrineBlock(
        topic="Pulmonary Complications of HIV Infection",
        keywords=["pulmonary complications", "HIV", "infection", "diagnosis", "therapy"],
        conclusion_template="Pulmonary complications of HIV include infection, malignancy, and ILD; early diagnosis and therapy improve outcomes.",
        reasoning_framework="""
1. Assess HIV status and CD4 count.
2. Obtain history and physical exam.
3. Order imaging and microbiologic tests.
4. Initiate empiric therapy for common pathogens.
5. Screen for malignancy and ILD.
6. Document findings and outcomes.
7. Use IDSA and ATS guidelines for management.
8. Re-evaluate if clinical status changes.
""",
        key_factors=["HIV status", "diagnosis", "empiric therapy", "malignancy", "monitoring"],
        primary_authority=["IDSA HIV Guidelines", "American Thoracic Society"],
        burden_holder="clinician",
        adversary_position="Empiric therapy risks resistance; diagnosis may be delayed.",
        counter_arguments=[
            "Resistance complicates therapy.",
            "Diagnosis may be delayed.",
            "Side effects may limit therapy."
        ],
        resolution_strategy="Use broad empiric therapy, rapid diagnostics, monitor closely.",
        entity_scope="patients with HIV",
        confidence=0.92,
        confidence_zone="moderate-high",
        controlling_precedent="IDSA 2019 HIV Guideline"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]